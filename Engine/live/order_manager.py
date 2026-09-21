try:
    import MetaTrader5 as mt5
except (ImportError, ModuleNotFoundError):
    mt5 = None

import logging
import os
import json
import time
import math
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

LIVE_STATE_FILE = Path(__file__).resolve().parent / "live_state.json"
DRY_RUN_STATE_FILE = Path(__file__).resolve().parent / "dry_run_state.json"
STATE_FILE = LIVE_STATE_FILE  # default backward-compatible alias
MAX_MARGIN_UTILIZATION_PCT = 0.30  # Portfolio margin utilization ceiling (30%)
MIN_MARGIN_LEVEL_PCT = 200.0       # Minimum account margin level before hard freeze (200%)
MAX_CONCURRENT_POSITIONS = 2       # Max 2 concurrent positions across portfolio

# Institutional Correlation Clusters (Max 1 concurrent position per cluster)
CORRELATION_CLUSTERS = {
    'EUR': {'EURUSD', 'EURHUF', 'EURSEK', 'EURCNH', 'AUDCHF'},
    'PACIFIC': {'NZDUSD', 'USDHKD', 'NZDCNH', 'USDSEK'},
    'EQUITY': {'GER40', 'GER30', 'FR40', 'AU200', 'US2000'},
    'COMMODITY': {'GAS', 'NICKEL', 'LEAD', 'XAUCNH', 'GAUCNH'}
}

from Engine.forex_engine import (
    is_broker_rollover_window,
    is_friday_weekend_lockout,
    is_friday_closeout_window,
    RECONCILE_HEARTBEAT_INTERVAL_SEC
)

class OrderManager:
    def __init__(self, connection=None, dry_run: bool = True, state_file=None):
        self.conn = connection
        self.dry_run = dry_run
        if state_file is not None:
            self.state_file = Path(state_file)
        else:
            self.state_file = DRY_RUN_STATE_FILE if self.dry_run else LIVE_STATE_FILE
        self.open_trades = {}  # ticket -> trade_info
        self.load_state()

    def can_open_trade(self, symbol: str) -> tuple:
        """
        Validates portfolio limits, correlation clusters, and operational safeguards before order entry:
        1. Operational Safeguard 1: Rollover spread lockout (21:55-22:15 UTC).
        2. Operational Safeguard 2: Friday weekend gap protection (>= 18:00 UTC).
        3. Max concurrent positions across portfolio (<= 2).
        4. Single active position per asset (no duplicates).
        5. Correlation cluster restriction (max 1 active position per cluster).
        """
        # Operational Safeguard 1: Rollover Lockout (21:55 - 22:15 UTC)
        if is_broker_rollover_window():
            return False, "Rollover Lockout (21:55-22:15 UTC)"

        # Operational Safeguard 2: Friday Weekend Cutoff (>= 18:00 UTC)
        if is_friday_weekend_lockout():
            return False, "Friday Cutoff (>= 18:00 UTC)"

        if len(self.open_trades) >= MAX_CONCURRENT_POSITIONS:
            return False, f"Max Positions ({MAX_CONCURRENT_POSITIONS})"

        sym_clean = symbol.upper().replace(".PI", "").replace(".P", "").replace(".R", "")
        for ot in self.open_trades.values():
            ot_sym = ot.get("symbol", "").upper().replace(".PI", "").replace(".P", "").replace(".R", "")
            if ot_sym == sym_clean:
                return False, f"Duplicate {sym_clean}"

        symbol_cluster = None
        for c_name, c_members in CORRELATION_CLUSTERS.items():
            if sym_clean in c_members:
                symbol_cluster = c_name
                break

        if symbol_cluster:
            for ot in self.open_trades.values():
                ot_sym = ot.get("symbol", "").upper().replace(".PI", "").replace(".P", "").replace(".R", "")
                if ot_sym in CORRELATION_CLUSTERS.get(symbol_cluster, set()):
                    return False, f"Cluster Veto: {symbol_cluster} ({ot_sym})"

        return True, "OK"

    def reconcile_with_broker(self):
        """
        Broker Position Reconciliation Heartbeat (runs every 30 seconds).
        Cross-verifies MT5 broker-side tickets against local open_trades memory.
        Detects positions closed externally by broker-side SL/TP or terminal disconnects.
        Fails safe on query failure (preserves open_trades if broker query returns None).
        """
        if getattr(self, "dry_run", False):
            return  # In dry run mode, positions are simulated locally
        if self.conn is not None and not getattr(self.conn, "connected", True):
            return
        try:
            live_pos = mt5.positions_get() if hasattr(mt5, "positions_get") else None
            if live_pos is None:
                logging.error("[RECONCILE HEARTBEAT ERROR] mt5.positions_get() returned None. Preserving active positions.")
                return
            live_positions = {p.ticket: p for p in live_pos}
            missing_tickets = [t for t in list(self.open_trades.keys()) if t not in live_positions]
            for t in missing_tickets:
                closed = self.open_trades.pop(t)
                logging.info(f"[RECONCILE HEARTBEAT] Detected external/broker closure for ticket #{t} ({closed.get('symbol')}). State reconciled.")
            if missing_tickets:
                self.save_state()
        except Exception as e:
            logging.error(f"[RECONCILE HEARTBEAT ERROR] Failed to cross-verify MT5 positions: {e}")

        
    def save_state(self):
        """Persists active open trades so positions survive restarts, preserving PnL metrics."""
        try:
            target_file = getattr(self, "state_file", STATE_FILE)
            state_data = {}
            if target_file.exists():
                try:
                    with open(target_file, "r", encoding="utf-8") as f:
                        state_data = json.load(f)
                except Exception:
                    state_data = {}
            state_data["open_trades"] = self.open_trades
            state_data["timestamp"] = time.time()
            if "realized_pnl" not in state_data:
                state_data["realized_pnl"] = 0.0
            if "initial_balance" not in state_data:
                state_data["initial_balance"] = 5000.0
            with open(target_file, "w", encoding="utf-8") as f:
                json.dump(state_data, f, indent=2, default=str)
        except Exception as e:
            logging.error(f"Failed to save state: {e}")

    def load_state(self):
        """Reconciles persisted state with active MT5 positions on startup and normalizes schema."""
        target_file = getattr(self, "state_file", STATE_FILE)
        saved_trades = {}
        if target_file.exists():
            try:
                with open(target_file, "r", encoding="utf-8") as f:
                    state_data = json.load(f)
                saved_trades = state_data.get("open_trades", {})
            except Exception as e:
                logging.error(f"Failed to read state file {target_file}: {e}")
                saved_trades = {}

        try:
            raw_trades = {}
            is_connected = getattr(self.conn, "connected", False) if self.conn is not None else False
            if hasattr(mt5, "positions_get"):
                live_pos = mt5.positions_get()
                if not getattr(self, "dry_run", False) and (is_connected or live_pos is not None):
                    if live_pos is not None:
                        live_positions = {p.ticket: p for p in live_pos}
                        for k, v in saved_trades.items():
                            if int(k) in live_positions:
                                raw_trades[int(k)] = v
                        for tkt, pos in live_positions.items():
                            if tkt not in raw_trades:
                                raw_trades[tkt] = {
                                    "ticket": tkt,
                                    "symbol": pos.symbol,
                                    "real_symbol": pos.symbol,
                                    "type": pos.type,
                                    "volume": pos.volume,
                                    "entry": pos.price_open,
                                    "entry_price": pos.price_open,
                                    "sl": pos.sl,
                                    "tp": pos.tp,
                                }
                    else:
                        raw_trades = {int(k): v for k, v in saved_trades.items()}
                else:
                    raw_trades = {int(k): v for k, v in saved_trades.items()}
            else:
                raw_trades = {int(k): v for k, v in saved_trades.items()}

            self.open_trades = {}
            for tkt, tr in raw_trades.items():
                entry = float(tr.get("entry") or tr.get("entry_price") or 0.0)
                sl = float(tr.get("sl", 0.0))
                tp = float(tr.get("tp", 0.0))
                r_dist = float(tr.get("r_dist", 0.0))
                if r_dist <= 0.0:
                    r_dist = abs(entry - sl) if sl > 0 else 0.0001
                bars = int(tr.get("bars_elapsed", tr.get("bars_held", 0)))
                self.open_trades[int(tkt)] = {
                    "symbol": tr.get("symbol", ""),
                    "real_symbol": tr.get("real_symbol", tr.get("symbol", "")),
                    "ticket": int(tkt),
                    "type": int(tr.get("type", 0)),
                    "action": tr.get("action", "BUY" if tr.get("type", 0) in (0, getattr(mt5, "ORDER_TYPE_BUY", 0)) else "SELL"),
                    "volume": float(tr.get("volume", 0.01)),
                    "entry": entry,
                    "entry_price": entry,
                    "sl": sl,
                    "tp": tp,
                    "r_dist": r_dist,
                    "risk_usd": float(tr.get("risk_usd", 10.0)),
                    "strategy": tr.get("strategy", "ML_FOREX"),
                    "bars_elapsed": bars,
                    "bars_held": bars,
                    "highest_r": float(tr.get("highest_r", 0.0)),
                    "lowest_r": float(tr.get("lowest_r", 0.0)),
                    "current_r": float(tr.get("current_r", 0.0)),
                    "running_pnl": float(tr.get("running_pnl", 0.0)),
                    "ratchet_phase": int(tr.get("ratchet_phase", 0)),
                    "ratchet_desc": str(tr.get("ratchet_desc", "Base SL (-1.00R)")),
                    "last_bar_time": tr.get("last_bar_time", None)
                }
            logging.info(f"Loaded state: {len(self.open_trades)} active positions restored from {target_file.name}")
        except Exception as e:
            logging.error(f"Failed to load live state: {e}")

    def calculate_lot_size(self, symbol: str, risk_usd: float, sl_dist: float) -> float:
        """
        Calculates exact MT5 lot size for risk_usd and stop distance sl_dist in price.
        Enforces institutional leverage caps (10:1 majors, 5:1 minors/indices, 3:1 exotics).
        Clamps to broker volume_min, volume_max, and steps.
        Fails safe and returns 0.0 (abstain) if symbol specs are unavailable, sl_dist <= 0,
        or affordable lots < broker volume_min.
        """
        if self.conn is None or not getattr(self.conn, "connected", False):
            if getattr(self, "dry_run", False):
                return 0.01
            return 0.0
        real_symbol = self.conn.resolve_symbol(symbol) if hasattr(self.conn, "resolve_symbol") else symbol
        info = mt5.symbol_info(real_symbol) if hasattr(mt5, "symbol_info") else None
        if info is None or sl_dist <= 0:
            if getattr(self, "dry_run", False):
                return 0.01
            return 0.0
            
        tick_value = info.trade_tick_value if getattr(info, "trade_tick_value", 0) > 0 else 1.0
        tick_size = info.trade_tick_size if getattr(info, "trade_tick_size", 0) > 0 else (info.point if getattr(info, "point", 0) > 0 else 0.0001)
        
        # Loss per 1.0 lot for this stop distance
        loss_per_lot = (sl_dist / tick_size) * tick_value
        if loss_per_lot <= 0:
            return 0.0
            
        raw_lots = risk_usd / loss_per_lot
        vol_min = getattr(info, "volume_min", 0.01)
        vol_max = getattr(info, "volume_max", 100.0)

        # Safety: If affordable volume is below broker's minimum lot size, abstain
        if raw_lots < vol_min:
            return 0.0

        # P0 FIX: Institutional Maximum Leverage & Notional Sizing Caps
        sym_clean = symbol.upper().replace(".PI", "").replace(".P", "").replace(".R", "")
        if sym_clean in ['EURUSD', 'NZDUSD', 'AUDCHF']:
            max_leverage = 10.0  # Majors: 10:1 max leverage
        elif sym_clean in ['EURCNH', 'NZDCNH']:
            max_leverage = 5.0   # Minors: 5:1 max leverage
        elif sym_clean in ['GER40', 'GER30', 'FR40', 'AU200', 'US2000']:
            max_leverage = 5.0   # Indices: 5:1 max leverage
        else:
            max_leverage = 3.0   # Exotics & Commodities: 3:1 max leverage

        acc = mt5.account_info() if hasattr(mt5, "account_info") else None
        equity = float(acc.equity) if acc and getattr(acc, "equity", 0) > 0 else 5000.0
        acc_leverage = float(acc.leverage) if acc and getattr(acc, "leverage", 0) > 0 else 30.0

        tick = self.conn.get_last_tick(real_symbol) if hasattr(self.conn, "get_last_tick") else None
        curr_price = tick.ask if tick and getattr(tick, "ask", 0) > 0 else 1.0

        # Exact notional in account currency (USD) per 1.0 lot using broker margin requirements
        broker_margin_1lot = mt5.order_calc_margin(getattr(mt5, "ORDER_TYPE_BUY", 0), real_symbol, 1.0, curr_price) if hasattr(mt5, "order_calc_margin") else None
        if broker_margin_1lot and broker_margin_1lot > 0:
            contract_notional_usd = broker_margin_1lot * acc_leverage
        else:
            contract_size = getattr(info, "trade_contract_size", 100000.0) if getattr(info, "trade_contract_size", 0) > 0 else 100000.0
            contract_notional_usd = contract_size

        max_notional = equity * max_leverage
        max_lots_leverage = max_notional / contract_notional_usd if contract_notional_usd > 0 else 1.0

        raw_lots = min(raw_lots, max_lots_leverage)
        if raw_lots < vol_min:
            return 0.0

        step = getattr(info, "volume_step", 0.01) if getattr(info, "volume_step", 0) > 0 else 0.01
        lots = math.floor((raw_lots / step) + 1e-9) * step
        while (lots * loss_per_lot) > risk_usd and (lots - step) >= vol_min:
            lots -= step
        if (lots * loss_per_lot) > risk_usd or lots < vol_min:
            return 0.0
        lots = min(lots, vol_max)
        step_str = f"{step:.8f}".rstrip('0')
        decimals = len(step_str.split('.')[1]) if '.' in step_str else 2
        return round(float(lots), decimals)

    def place_market_order(self, symbol, order_type, volume=None, sl_price=None, tp_price=None, risk_usd=10.0, strategy_tag="ML_FOREX"):
        if self.conn is not None and not getattr(self.conn, "connected", True):
            logging.error("Not connected to MT5")
            return None

        # P0 FIX: Margin Level & Margin Utilization Circuit Breaker
        acc = mt5.account_info() if hasattr(mt5, "account_info") else None
        if acc is not None:
            if getattr(acc, "margin_level", 0) > 0 and acc.margin_level < MIN_MARGIN_LEVEL_PCT:
                logging.warning(f"[RISK VETO] Account margin level ({acc.margin_level:.1f}%) < {MIN_MARGIN_LEVEL_PCT:.0f}%. Order for {symbol} vetoed.")
                return None
            if getattr(acc, "equity", 0) > 0 and (getattr(acc, "margin", 0) / acc.equity) > MAX_MARGIN_UTILIZATION_PCT:
                logging.warning(f"[RISK VETO] Margin utilization ({(acc.margin/acc.equity):.1%}) > {MAX_MARGIN_UTILIZATION_PCT:.0%}. Order for {symbol} vetoed.")
                return None

        # P1 FIX: Portfolio Limits & Correlation Cluster Veto
        can_open, veto_reason = self.can_open_trade(symbol)
        if not can_open:
            logging.warning(f"[ORDER VETO] Trade rejected for {symbol}: {veto_reason}")
            return None

        real_symbol = self.conn.resolve_symbol(symbol) if hasattr(self.conn, "resolve_symbol") else symbol
        
        # Ensure symbol is selected in MarketWatch
        if hasattr(mt5, "symbol_select"):
            mt5.symbol_select(real_symbol, True)
            
        tick = self.conn.get_last_tick(real_symbol) if hasattr(self.conn, "get_last_tick") else None
        if tick is None:
            if getattr(self, "dry_run", False):
                entry_price = float(sl_price + 0.0020) if sl_price else 1.0000
                logging.info(f"[DRY RUN] Simulating entry price {entry_price:.5f} for {real_symbol} (MT5 offline)")
            else:
                logging.error(f"Cannot get tick for {real_symbol}")
                return None
        else:
            entry_price = tick.ask if order_type == getattr(mt5, "ORDER_TYPE_BUY", 0) else tick.bid
        
        # Determine Stop-Loss Distance (r_dist)
        r_dist = abs(entry_price - sl_price) if sl_price else 0.0
        
        if volume is None or volume <= 0:
            volume = self.calculate_lot_size(symbol, risk_usd=risk_usd, sl_dist=r_dist)
            if volume <= 0:
                logging.warning(f"[ORDER ABSTAIN] Calculated lot size for {symbol} is 0.0. Order aborted.")
                return None
        else:
            max_allowed = self.calculate_lot_size(symbol, risk_usd=risk_usd, sl_dist=r_dist)
            if max_allowed > 0 and volume > max_allowed:
                logging.warning(f"[RISK OVERRIDE] Supplied volume {volume} exceeds risk budget max {max_allowed}. Clamping to {max_allowed}.")
                volume = max_allowed
            elif max_allowed == 0.0:
                logging.warning(f"[ORDER ABSTAIN] Risk budget forbids volume for {symbol}. Order aborted.")
                return None
            
        request = {
            "action": getattr(mt5, "TRADE_ACTION_DEAL", 1),
            "symbol": real_symbol,
            "volume": float(volume),
            "type": order_type,
            "price": float(entry_price),
            "deviation": 20,
            "magic": 123456,
            "comment": f"{strategy_tag} Live",
            "type_time": getattr(mt5, "ORDER_TIME_GTC", 0),
            "type_filling": getattr(mt5, "ORDER_FILLING_IOC", 1),
        }
        
        if sl_price is not None:
            request["sl"] = float(sl_price)
        if tp_price is not None:
            request["tp"] = float(tp_price)

        if getattr(self, "dry_run", False):
            mock_ticket = int(time.time() * 1000) % 10000000
            logging.info(f"[DRY RUN] Simulating market order for {symbol}, mock ticket #{mock_ticket}")
            self.open_trades[mock_ticket] = {
                "symbol": symbol,
                "real_symbol": real_symbol,
                "ticket": mock_ticket,
                "type": order_type,
                "action": "BUY" if order_type in (0, getattr(mt5, "ORDER_TYPE_BUY", 0)) else "SELL",
                "volume": volume,
                "entry": entry_price,
                "entry_price": entry_price,
                "sl": sl_price,
                "tp": tp_price,
                "r_dist": r_dist,
                "risk_usd": risk_usd,
                "strategy": strategy_tag,
                "bars_elapsed": 0,
                "bars_held": 0,
                "highest_r": 0.0,
                "lowest_r": 0.0,
                "current_r": 0.0,
                "running_pnl": 0.0,
                "ratchet_phase": 0,
                "ratchet_desc": "Base SL (-1.00R)",
                "last_bar_time": None
            }
            self.save_state()
            return mock_ticket

        result = mt5.order_send(request)
        if result is None or getattr(result, "retcode", None) != getattr(mt5, "TRADE_RETCODE_DONE", 10009):
            retcode = getattr(result, "retcode", None)
            logging.error(f"Order send failed for {symbol}: retcode={retcode}")
            return None
            
        fill_price = getattr(result, "price", 0.0)
        actual_entry = fill_price if fill_price > 0 else entry_price
        fill_volume = getattr(result, "volume", 0.0)
        actual_volume = fill_volume if fill_volume > 0 else volume
        actual_r_dist = abs(actual_entry - sl_price) if sl_price else r_dist
        if actual_r_dist <= 0:
            actual_r_dist = 0.0001

        logging.info(f"Order executed successfully: Ticket #{result.order} for {symbol} ({actual_volume} lots @ {actual_entry})")
        
        self.open_trades[result.order] = {
            "symbol": symbol,
            "real_symbol": real_symbol,
            "ticket": result.order,
            "type": order_type,
            "action": "BUY" if order_type in (0, getattr(mt5, "ORDER_TYPE_BUY", 0)) else "SELL",
            "volume": actual_volume,
            "entry": actual_entry,
            "entry_price": actual_entry,
            "sl": sl_price,
            "tp": tp_price,
            "r_dist": actual_r_dist,
            "risk_usd": risk_usd,
            "strategy": strategy_tag,
            "bars_elapsed": 0,
            "bars_held": 0,
            "highest_r": 0.0,
            "lowest_r": 0.0,
            "current_r": 0.0,
            "running_pnl": 0.0,
            "ratchet_phase": 0,
            "ratchet_desc": "Base SL (-1.00R)",
            "last_bar_time": None
        }
        self.save_state()
        
        return result.order
        
    def close_position(self, ticket):
        if getattr(self, "dry_run", False):
            logging.info(f"[DRY RUN] Simulating close for position {ticket}")
            if ticket in self.open_trades:
                del self.open_trades[ticket]
                self.save_state()
            return True

        if self.conn is not None and not getattr(self.conn, "connected", True):
            return False
            
        position = mt5.positions_get(ticket=ticket) if hasattr(mt5, "positions_get") else None
        if position is None or len(position) == 0:
            logging.error(f"Position {ticket} not found")
            return False
            
        position = position[0]
        tick = self.conn.get_last_tick(position.symbol) if self.conn and hasattr(self.conn, "get_last_tick") else None
        if tick is None:
            return False
            
        close_type = getattr(mt5, "ORDER_TYPE_SELL", 1) if position.type == getattr(mt5, "POSITION_TYPE_BUY", 0) else getattr(mt5, "ORDER_TYPE_BUY", 0)
        price = tick.bid if position.type == getattr(mt5, "POSITION_TYPE_BUY", 0) else tick.ask
        
        request = {
            "action": getattr(mt5, "TRADE_ACTION_DEAL", 1),
            "symbol": position.symbol,
            "volume": position.volume,
            "type": close_type,
            "position": ticket,
            "price": price,
            "deviation": 20,
            "magic": 123456,
            "comment": "Close Position",
            "type_time": getattr(mt5, "ORDER_TIME_GTC", 0),
            "type_filling": getattr(mt5, "ORDER_FILLING_IOC", 1),
        }

        result = mt5.order_send(request)
        if result is None or getattr(result, "retcode", None) != getattr(mt5, "TRADE_RETCODE_DONE", 10009):
            retcode = getattr(result, "retcode", None)
            logging.error(f"Close failed, retcode={retcode}")
            return False
            
        logging.info(f"Position {ticket} closed successfully")
        if ticket in self.open_trades:
            del self.open_trades[ticket]
            self.save_state()
        return True
        
    def modify_sl(self, ticket, new_sl):
        if getattr(self, "dry_run", False):
            logging.info(f"[DRY RUN] Simulating SL modify for {ticket} to {new_sl}")
            if ticket in self.open_trades:
                self.open_trades[ticket]["sl"] = float(new_sl)
                self.save_state()
            return True

        if self.conn is not None and not getattr(self.conn, "connected", True):
            return False
            
        position = mt5.positions_get(ticket=ticket) if hasattr(mt5, "positions_get") else None
        if position is None or len(position) == 0:
            return False
            
        pos = position[0]
        
        # Check minimum broker stop distance (trade_stops_level)
        info = mt5.symbol_info(pos.symbol) if hasattr(mt5, "symbol_info") else None
        if info is not None and getattr(info, "trade_stops_level", None) is not None and getattr(info, "point", None) is not None:
            min_dist = info.trade_stops_level * info.point
            tick = self.conn.get_last_tick(pos.symbol) if self.conn and hasattr(self.conn, "get_last_tick") else None
            if tick is not None:
                current_price = tick.bid if pos.type == getattr(mt5, "POSITION_TYPE_BUY", 0) else tick.ask
                if abs(new_sl - current_price) < min_dist:
                    logging.warning(f"Proposed SL {new_sl:.5f} too close to current price {current_price:.5f} (min dist: {min_dist:.5f}). Skipping modify.")
                    return False
        
        request = {
            "action": getattr(mt5, "TRADE_ACTION_SLTP", 6),
            "position": ticket,
            "symbol": pos.symbol,
            "sl": float(new_sl),
            "tp": pos.tp
        }

        result = mt5.order_send(request)
        if result is None or getattr(result, "retcode", None) != getattr(mt5, "TRADE_RETCODE_DONE", 10009):
            retcode = getattr(result, "retcode", None)
            logging.error(f"Modify SL failed for {ticket}, retcode={retcode}")
            return False
            
        logging.info(f"SL modified for {ticket} to {new_sl}")
        if ticket in self.open_trades:
            self.open_trades[ticket]["sl"] = new_sl
            self.save_state()
        return True

    def manage_open_trades(self, current_bar_time=None):
        """
        To be called every minute or tick to manage stops and time decay.
        current_bar_time should be the timestamp of the latest 15m bar to track 24-bar decay.
        """
        if not self.conn.connected:
            return

        # Operational Safeguard 2b: Friday Weekend Gap Defense - Liquidate open positions at 20:30 UTC Friday
        if is_friday_closeout_window():
            for ticket in list(self.open_trades.keys()):
                logging.info(f"[FRIDAY CLOSEOUT] Closing #{ticket} for weekend gap defense.")
                self.close_position(ticket)
            return

        # Operational Safeguard 1b: Pause ratchet modifications during 21:55-22:15 UTC daily rollover
        in_rollover = is_broker_rollover_window()

        tickets_to_check = list(self.open_trades.keys())

        
        for ticket in tickets_to_check:
            trade_info = self.open_trades.get(ticket)
            if trade_info is None:
                continue

            if getattr(self, "dry_run", False):
                pos_type = int(trade_info.get("type", 0))
                pos_symbol = trade_info.get("symbol", "")
                pos_sl = float(trade_info.get("sl", 0.0))
            else:
                position = mt5.positions_get(ticket=ticket) if hasattr(mt5, "positions_get") else None
                if position is None:
                    logging.error(f"[MANAGE ERROR] mt5.positions_get(ticket={ticket}) returned None. Preserving active ticket.")
                    continue
                if len(position) == 0:
                    logging.info(f"[BROKER CLOSED] Position #{ticket} closed externally on broker side.")
                    if ticket in self.open_trades:
                        del self.open_trades[ticket]
                        self.save_state()
                    continue
                pos = position[0]
                pos_type = pos.type
                pos_symbol = pos.symbol
                pos_sl = pos.sl

            # Update elapsed bars
            if current_bar_time and trade_info.get("last_bar_time") != current_bar_time:
                bars = int(trade_info.get("bars_elapsed", trade_info.get("bars_held", 0))) + 1
                trade_info["bars_elapsed"] = bars
                trade_info["bars_held"] = bars
                trade_info["last_bar_time"] = current_bar_time
                
            tick = self.conn.get_last_tick(pos_symbol) if self.conn and hasattr(self.conn, "get_last_tick") else None
            if tick is None:
                continue
                
            current_price = tick.bid if pos_type in (0, getattr(mt5, "POSITION_TYPE_BUY", 0)) else tick.ask
            entry = float(trade_info.get("entry_price") or trade_info.get("entry") or 0.0)
            sl_val = float(trade_info.get("sl") or pos_sl)
            r_dist = float(trade_info.get("r_dist") or (abs(entry - sl_val) if sl_val > 0 else 0.0001))
            if r_dist <= 0:
                r_dist = 0.0001
            trade_info["entry"] = entry
            trade_info["entry_price"] = entry
            trade_info["r_dist"] = r_dist
            trade_info["cur_price"] = current_price
            
            # Calculate current R
            if pos_type in (0, getattr(mt5, "POSITION_TYPE_BUY", 0)):
                current_r = (current_price - entry) / r_dist
            else:
                current_r = (entry - current_price) / r_dist
                
            trade_info["current_r"] = current_r
            trade_info["running_pnl"] = current_r * float(trade_info.get("risk_usd", 10.0))
            trade_info["highest_r"] = max(float(trade_info.get("highest_r", 0.0)), current_r)
            trade_info["lowest_r"] = min(float(trade_info.get("lowest_r", 0.0)), current_r)

            # In dry run mode, check simulated SL and TP hits
            if getattr(self, "dry_run", False):
                if pos_type in (0, getattr(mt5, "POSITION_TYPE_BUY", 0)):
                    if pos_sl > 0 and current_price <= pos_sl:
                        logging.info(f"[DRY RUN SL] Ticket #{ticket} hit SL at {current_price:.5f}")
                        self.close_position(ticket)
                        continue
                    tp_val = float(trade_info.get("tp", 0.0))
                    if tp_val > 0 and current_price >= tp_val:
                        logging.info(f"[DRY RUN TP] Ticket #{ticket} hit TP at {current_price:.5f}")
                        self.close_position(ticket)
                        continue
                else:
                    if pos_sl > 0 and current_price >= pos_sl:
                        logging.info(f"[DRY RUN SL] Ticket #{ticket} hit SL at {current_price:.5f}")
                        self.close_position(ticket)
                        continue
                    tp_val = float(trade_info.get("tp", 0.0))
                    if tp_val > 0 and current_price <= tp_val:
                        logging.info(f"[DRY RUN TP] Ticket #{ticket} hit TP at {current_price:.5f}")
                        self.close_position(ticket)
                        continue
            
            # Time Decay Exit: 24 bars elapsed and hasn't gained 0.20R
            bars_elapsed = int(trade_info.get("bars_elapsed", trade_info.get("bars_held", 0)))
            if bars_elapsed >= 24 and float(trade_info.get("highest_r", 0.0)) < 0.20:
                logging.info(f"Time decay exit for {ticket}, bars={bars_elapsed}, high_R={trade_info['highest_r']:.2f}")
                self.close_position(ticket)
                continue
                
            # Microstructure Ratchets (Exact parity with strategy_kernel.py & forex_engine.py)
            # BE Lock +0.15R at 0.80R, Profit Lock +0.80R at 1.50R, Lock +1.80R at 2.00R, TP at +2.50R
            new_sl_r = None
            highest_r = float(trade_info.get("highest_r", 0.0))
            if highest_r >= 3.5:
                new_sl_r = 3.3
                trade_info["ratchet_phase"] = 6
                trade_info["ratchet_desc"] = "Lock +3.30R"
            elif highest_r >= 3.0:
                new_sl_r = 2.8
                trade_info["ratchet_phase"] = 5
                trade_info["ratchet_desc"] = "Lock +2.80R"
            elif highest_r >= 2.5:
                new_sl_r = 2.3
                trade_info["ratchet_phase"] = 4
                trade_info["ratchet_desc"] = "Lock +2.30R"
            elif highest_r >= 2.0:
                new_sl_r = 1.8
                trade_info["ratchet_phase"] = 3
                trade_info["ratchet_desc"] = "Lock +1.80R"
            elif highest_r >= 1.5:
                new_sl_r = 0.80
                trade_info["ratchet_phase"] = 2
                trade_info["ratchet_desc"] = "Lock +0.80R"
            elif highest_r >= 0.8:
                new_sl_r = 0.15
                trade_info["ratchet_phase"] = 1
                trade_info["ratchet_desc"] = "BE Lock (+0.15R)"
                
            if new_sl_r is not None:
                if in_rollover:
                    logging.info(f"[ROLLOVER LOCKOUT] Suppressing SL modification for #{ticket} during 21:55-22:15 UTC bank settlement.")
                else:
                    # Calculate new SL price
                    if pos_type in (0, getattr(mt5, "POSITION_TYPE_BUY", 0)):
                        new_sl_price = entry + (new_sl_r * r_dist)
                        # Ensure we only move SL up
                        if new_sl_price > pos_sl:
                            self.modify_sl(ticket, new_sl_price)
                    else:
                        new_sl_price = entry - (new_sl_r * r_dist)
                        # Ensure we only move SL down (for short, SL is above entry)
                        if new_sl_price < pos_sl or pos_sl == 0:
                            self.modify_sl(ticket, new_sl_price)


import MetaTrader5 as mt5
import logging
import os
import json
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

STATE_FILE = Path(__file__).resolve().parent / "live_state.json"
MAX_MARGIN_UTILIZATION_PCT = 0.30  # Portfolio margin utilization ceiling (30%)
MIN_MARGIN_LEVEL_PCT = 200.0       # Minimum account margin level before hard freeze (200%)
MAX_CONCURRENT_POSITIONS = 3       # Max 3 concurrent positions across portfolio

# Institutional Correlation Clusters (Max 1 concurrent position per cluster)
CORRELATION_CLUSTERS = {
    'EUR_BLOC': {'EURUSD', 'EURSEK', 'EURCNH', 'EURHUF'},
    'USD_BLOC': {'NZDUSD', 'AUDCHF'},
    'CNH_BLOC': {'NZDCNH', 'XAUCNH', 'GAUCNH'},
    'INDEX_BLOC': {'GER40', 'GER30', 'FR40', 'AU200', 'US2000'},
    'COMMODITY_BLOC': {'GAS', 'NICKEL', 'LEAD'}
}

from Engine.forex_engine import (
    is_broker_rollover_window,
    is_friday_weekend_lockout,
    is_friday_closeout_window,
    RECONCILE_HEARTBEAT_INTERVAL_SEC
)

class OrderManager:
    def __init__(self, connection):
        self.conn = connection
        self.open_trades = {}  # ticket -> trade_info
        self.load_state()

    def can_open_trade(self, symbol: str) -> tuple:
        """
        Validates portfolio limits, correlation clusters, and operational safeguards before order entry:
        1. Operational Safeguard 1: Rollover spread lockout (21:55-22:15 UTC).
        2. Operational Safeguard 2: Friday weekend gap protection (>= 18:00 UTC).
        3. Max concurrent positions across portfolio (<= 3).
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
        """
        if not self.conn.connected:
            return
        try:
            live_pos = mt5.positions_get()
            live_positions = {p.ticket: p for p in (live_pos or [])}
            missing_tickets = [t for t in list(self.open_trades.keys()) if t not in live_positions]
            for t in missing_tickets:
                closed = self.open_trades.pop(t)
                logging.info(f"[RECONCILE HEARTBEAT] Detected external/broker closure for ticket #{t} ({closed.get('symbol')}). State reconciled.")
            if missing_tickets:
                self.save_state()
        except Exception as e:
            logging.error(f"[RECONCILE HEARTBEAT ERROR] Failed to cross-verify MT5 positions: {e}")

        
    def save_state(self):
        """Persists active open trades to live_state.json so positions survive restarts, preserving PnL metrics."""
        try:
            state_data = {}
            if STATE_FILE.exists():
                try:
                    with open(STATE_FILE, "r", encoding="utf-8") as f:
                        state_data = json.load(f)
                except Exception:
                    state_data = {}
            state_data["open_trades"] = self.open_trades
            state_data["timestamp"] = time.time()
            if "realized_pnl" not in state_data:
                state_data["realized_pnl"] = 0.0
            if "initial_balance" not in state_data:
                state_data["initial_balance"] = 5000.0
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state_data, f, indent=2, default=str)
        except Exception as e:
            logging.error(f"Failed to save live state: {e}")

    def load_state(self):
        """Reconciles persisted state with active MT5 positions on startup and normalizes schema."""
        if not STATE_FILE.exists():
            return
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state_data = json.load(f)
            saved_trades = state_data.get("open_trades", {})
            raw_trades = {}
            if self.conn.connected:
                live_positions = {p.ticket: p for p in (mt5.positions_get() or [])}
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
                    "action": tr.get("action", "BUY" if tr.get("type", 0) in (0, mt5.ORDER_TYPE_BUY) else "SELL"),
                    "volume": float(tr.get("volume", 0.01)),
                    "entry": entry,
                    "entry_price": entry,
                    "sl": sl,
                    "tp": tp,
                    "r_dist": r_dist,
                    "risk_usd": float(tr.get("risk_usd", 25.0)),
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
            logging.info(f"Loaded live state: {len(self.open_trades)} active positions restored from {STATE_FILE.name}")
        except Exception as e:
            logging.error(f"Failed to load live state: {e}")

    def calculate_lot_size(self, symbol: str, risk_usd: float, sl_dist: float) -> float:
        """
        Calculates exact MT5 lot size for risk_usd and stop distance sl_dist in price.
        Enforces institutional leverage caps (10:1 majors, 5:1 minors/indices, 3:1 exotics).
        Clamps to broker volume_min, volume_max, and steps.
        """
        real_symbol = self.conn.resolve_symbol(symbol)
        info = mt5.symbol_info(real_symbol)
        if info is None or sl_dist <= 0:
            return 0.01  # Safe minimum fallback
            
        tick_value = info.trade_tick_value if info.trade_tick_value > 0 else 1.0
        tick_size = info.trade_tick_size if info.trade_tick_size > 0 else (info.point if info.point > 0 else 0.0001)
        
        # Loss per 1.0 lot for this stop distance
        loss_per_lot = (sl_dist / tick_size) * tick_value
        if loss_per_lot <= 0:
            return info.volume_min
            
        raw_lots = risk_usd / loss_per_lot

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

        acc = mt5.account_info()
        equity = float(acc.equity) if acc and acc.equity > 0 else 5000.0
        acc_leverage = float(acc.leverage) if acc and acc.leverage > 0 else 30.0

        tick = self.conn.get_last_tick(real_symbol)
        curr_price = tick.ask if tick and tick.ask > 0 else 1.0

        # Exact notional in account currency (USD) per 1.0 lot using broker margin requirements
        broker_margin_1lot = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, real_symbol, 1.0, curr_price)
        if broker_margin_1lot and broker_margin_1lot > 0:
            contract_notional_usd = broker_margin_1lot * acc_leverage
        else:
            contract_size = info.trade_contract_size if info.trade_contract_size > 0 else 100000.0
            contract_notional_usd = contract_size

        max_notional = equity * max_leverage
        max_lots_leverage = max_notional / contract_notional_usd if contract_notional_usd > 0 else 1.0

        raw_lots = min(raw_lots, max_lots_leverage)

        step = info.volume_step if info.volume_step > 0 else 0.01
        lots = round(raw_lots / step) * step
        lots = max(info.volume_min, min(lots, info.volume_max))
        return round(float(lots), 2)

    def place_market_order(self, symbol, order_type, volume=None, sl_price=None, tp_price=None, risk_usd=25.0, strategy_tag="ML_FOREX"):
        if not self.conn.connected:
            logging.error("Not connected to MT5")
            return None

        # P0 FIX: Margin Level & Margin Utilization Circuit Breaker
        acc = mt5.account_info()
        if acc is not None:
            if acc.margin_level > 0 and acc.margin_level < MIN_MARGIN_LEVEL_PCT:
                logging.warning(f"[RISK VETO] Account margin level ({acc.margin_level:.1f}%) < {MIN_MARGIN_LEVEL_PCT:.0f}%. Order for {symbol} vetoed.")
                return None
            if acc.equity > 0 and (acc.margin / acc.equity) > MAX_MARGIN_UTILIZATION_PCT:
                logging.warning(f"[RISK VETO] Margin utilization ({(acc.margin/acc.equity):.1%}) > {MAX_MARGIN_UTILIZATION_PCT:.0%}. Order for {symbol} vetoed.")
                return None

        # P1 FIX: Portfolio Limits & Correlation Cluster Veto
        can_open, veto_reason = self.can_open_trade(symbol)
        if not can_open:
            logging.warning(f"[RISK VETO] Order for {symbol} vetoed: {veto_reason}")
            return None
            
        real_symbol = self.conn.resolve_symbol(symbol)
        tick = self.conn.get_last_tick(real_symbol)
        if tick is None:
            return None
            
        price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid
        
        # Dynamic lot sizing if volume not specified
        if volume is None or volume <= 0:
            sl_dist = abs(price - sl_price) if sl_price is not None else 0.0
            volume = self.calculate_lot_size(real_symbol, risk_usd=risk_usd, sl_dist=sl_dist)
            
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": real_symbol,
            "volume": float(volume),
            "type": order_type,
            "price": price,
            "sl": float(sl_price) if sl_price is not None else 0.0,
            "deviation": 20,
            "magic": 123456,
            "comment": f"Auto-{strategy_tag}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        if tp_price:
            request["tp"] = float(tp_price)
            
        result = mt5.order_send(request)
        if not result or result.retcode != mt5.TRADE_RETCODE_DONE:
            err_code = result.retcode if result else -1
            logging.error(f"Order send failed, retcode={err_code}")
            return None
            
        logging.info(f"Order placed successfully: ticket={result.order}, fill_price={result.price}, volume={volume}")
        
        # Use actual execution fill price from MT5 result
        entry_fill_price = result.price if result.price > 0 else price
        
        # Calculate R value (distance from fill price to SL)
        r_dist = abs(entry_fill_price - sl_price) if sl_price is not None else 0.0001
        if r_dist <= 0:
            r_dist = 0.0001
            
        action_str = "BUY" if order_type == mt5.ORDER_TYPE_BUY else "SELL"
        self.open_trades[result.order] = {
            "symbol": real_symbol,
            "real_symbol": real_symbol,
            "ticket": result.order,
            "type": order_type,
            "action": action_str,
            "volume": volume,
            "entry": entry_fill_price,
            "entry_price": entry_fill_price,
            "cur_price": entry_fill_price,
            "sl": sl_price,
            "tp": tp_price,
            "risk_usd": risk_usd,
            "r_dist": r_dist,
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
        if not self.conn.connected:
            return False
            
        position = mt5.positions_get(ticket=ticket)
        if position is None or len(position) == 0:
            logging.error(f"Position {ticket} not found")
            return False
            
        position = position[0]
        tick = self.conn.get_last_tick(position.symbol)
        if tick is None:
            return False
            
        close_type = mt5.ORDER_TYPE_SELL if position.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = tick.bid if position.type == mt5.POSITION_TYPE_BUY else tick.ask
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": close_type,
            "position": ticket,
            "price": price,
            "deviation": 20,
            "magic": 123456,
            "comment": "Close Position",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error(f"Close failed, retcode={result.retcode}")
            return False
            
        logging.info(f"Position {ticket} closed successfully")
        if ticket in self.open_trades:
            del self.open_trades[ticket]
            self.save_state()
        return True
        
    def modify_sl(self, ticket, new_sl):
        if not self.conn.connected:
            return False
            
        position = mt5.positions_get(ticket=ticket)
        if position is None or len(position) == 0:
            return False
            
        pos = position[0]
        
        # Check minimum broker stop distance (trade_stops_level)
        info = mt5.symbol_info(pos.symbol)
        if info is not None:
            min_dist = info.trade_stops_level * info.point
            tick = self.conn.get_last_tick(pos.symbol)
            if tick is not None:
                current_price = tick.bid if pos.type == mt5.POSITION_TYPE_BUY else tick.ask
                if abs(new_sl - current_price) < min_dist:
                    logging.warning(f"Proposed SL {new_sl:.5f} too close to current price {current_price:.5f} (min dist: {min_dist:.5f}). Skipping modify.")
                    return False
        
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": pos.symbol,
            "sl": float(new_sl),
            "tp": pos.tp
        }
        
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error(f"Modify SL failed for {ticket}, retcode={result.retcode}")
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
            position = mt5.positions_get(ticket=ticket)
            if position is None or len(position) == 0:
                # Closed manually or hit SL/TP
                if ticket in self.open_trades:
                    del self.open_trades[ticket]
                    self.save_state()
                continue
                
            pos = position[0]
            trade_info = self.open_trades[ticket]
            
            # Update elapsed bars
            if current_bar_time and trade_info.get("last_bar_time") != current_bar_time:
                bars = int(trade_info.get("bars_elapsed", trade_info.get("bars_held", 0))) + 1
                trade_info["bars_elapsed"] = bars
                trade_info["bars_held"] = bars
                trade_info["last_bar_time"] = current_bar_time
                
            tick = self.conn.get_last_tick(pos.symbol)
            if tick is None:
                continue
                
            current_price = tick.bid if pos.type == mt5.POSITION_TYPE_BUY else tick.ask
            entry = float(trade_info.get("entry_price") or trade_info.get("entry") or pos.price_open)
            sl_val = float(trade_info.get("sl") or pos.sl)
            r_dist = float(trade_info.get("r_dist") or abs(entry - sl_val) if sl_val > 0 else 0.0001)
            if r_dist <= 0:
                r_dist = 0.0001
            trade_info["entry"] = entry
            trade_info["entry_price"] = entry
            trade_info["r_dist"] = r_dist
            trade_info["cur_price"] = current_price
            
            # Calculate current R
            if pos.type == mt5.POSITION_TYPE_BUY:
                current_r = (current_price - entry) / r_dist
            else:
                current_r = (entry - current_price) / r_dist
                
            trade_info["current_r"] = current_r
            trade_info["running_pnl"] = current_r * float(trade_info.get("risk_usd", 25.0))
            trade_info["highest_r"] = max(float(trade_info.get("highest_r", 0.0)), current_r)
            trade_info["lowest_r"] = min(float(trade_info.get("lowest_r", 0.0)), current_r)
            
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
                    if pos.type == mt5.POSITION_TYPE_BUY:
                        new_sl_price = entry + (new_sl_r * r_dist)
                        # Ensure we only move SL up
                        if new_sl_price > pos.sl:
                            self.modify_sl(ticket, new_sl_price)
                    else:
                        new_sl_price = entry - (new_sl_r * r_dist)
                        # Ensure we only move SL down (for short, SL is above entry)
                        if new_sl_price < pos.sl or pos.sl == 0:
                            self.modify_sl(ticket, new_sl_price)


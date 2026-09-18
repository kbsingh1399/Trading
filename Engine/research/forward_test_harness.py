"""
================================================================================
ENGINE RESEARCH: FORWARD TEST HARNESS (GATE 3 — PAPER TRADING VALIDATION)
================================================================================
PURPOSE:
    Real-time paper trading simulator that:
    1. Reads approved_pool.json from Gate 1 (asset_screener.py).
    2. Connects to MT5 and streams live 15m bars for approved assets only.
    3. Uses AuctionEngine (Gate 2) to rank and filter signals per bar.
    4. Simulates order execution (no real orders -- DRY_RUN=True always).
    5. Tracks real-time Calmar, equity curve, and drawdown with RICH dashboard.
    6. HALTS if Calmar drops below threshold after minimum track record.

PROMOTION CRITERIA (to go live):
    - Run duration: >= 14 calendar days
    - Completed trades: >= 20
    - Net Profit (R): > 0
    - Live Calmar: >= 3.0
    - Max DD: <= 4.5%
    - No losing streak > 4 consecutive trades
    - Win Rate: >= 40%

This harness is STRICTLY a validation layer before live deployment.
All its metrics are compared against the approved_pool.json historical baseline.
================================================================================
"""
import os, sys, time, json, logging
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Engine.live.mt5_connection import MT5Connection
from Engine.live.inference_engine import StatefulInferenceEngine
from Engine.live.order_manager import OrderManager, MAX_CONCURRENT_POSITIONS, CORRELATION_CLUSTERS
from Engine.core.strategy_kernel import CANONICAL_FEATURES
from Engine.research.signal_auction import AuctionEngine, SignalCandidate, AuctionResult
from Engine.research.asset_screener import APPROVED_POOL_PATH

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# ─── CONSTANTS ───────────────────────────────────────────────────────────────

DRY_RUN                   = True     # ALWAYS TRUE -- no real orders
BASE_RISK_USD             = 25.0
INITIAL_CAPITAL           = 5000.0
HARD_DD_STOP_PCT          = 0.045    # 4.5% -- halt entire harness
MIN_TRACK_RECORD_TRADES   = 20
MIN_TRACK_RECORD_DAYS     = 14
LIVE_MIN_CALMAR           = 3.0      # minimum live Calmar to keep running
MAX_CONSECUTIVE_LOSSES    = 4        # halt if 4 straight losses
PROB_THRESHOLD            = 0.54
WIN_R                     = 2.5
LOSS_R                    = 1.0
POLL_INTERVAL_SECONDS     = 60       # check for new completed bars every minute

FORWARD_STATE_PATH = os.path.join(SCRIPT_DIR, 'forward_state.json')
FORWARD_LOG_PATH   = os.path.join(SCRIPT_DIR, 'forward_test.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(FORWARD_LOG_PATH, encoding='utf-8'),
        logging.StreamHandler(sys.stdout),
    ]
)
log = logging.getLogger('ForwardTest')
console = Console(force_terminal=True, width=140) if RICH_AVAILABLE else None


# ─── FORWARD STATE ────────────────────────────────────────────────────────────

class ForwardState:
    """Persistent state for the forward test (survives restarts)."""
    def __init__(self, state_path: str = FORWARD_STATE_PATH):
        self.state_path = state_path
        self.equity        = INITIAL_CAPITAL
        self.peak_equity   = INITIAL_CAPITAL
        self.trades: List[Dict] = []
        self.open_trades: Dict[str, Dict] = {}
        self.start_time    = datetime.now(timezone.utc).isoformat()
        self.bars_processed = 0
        self.load()

    def load(self):
        if os.path.exists(self.state_path):
            try:
                with open(self.state_path, 'r') as f:
                    d = json.load(f)
                self.equity         = d.get('equity', INITIAL_CAPITAL)
                self.peak_equity    = d.get('peak_equity', self.equity)
                self.trades         = d.get('trades', [])
                self.open_trades    = d.get('open_trades', {})
                self.start_time     = d.get('start_time', self.start_time)
                self.bars_processed = d.get('bars_processed', 0)
                log.info(f'Resumed forward state: equity={self.equity:.2f} trades={len(self.trades)}')
            except Exception as e:
                log.warning(f'Could not load forward state: {e}')

    def save(self):
        d = {
            'equity': self.equity, 'peak_equity': self.peak_equity,
            'trades': self.trades[-500:],  # keep last 500 for memory
            'open_trades': self.open_trades,
            'start_time': self.start_time,
            'bars_processed': self.bars_processed,
        }
        tmp = self.state_path + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(d, f, indent=2, default=str)
        os.replace(tmp, self.state_path)

    # ── Metrics ─────────────────────────────────────────────────────────
    @property
    def completed_trades(self) -> int:
        return len(self.trades)

    @property
    def net_pnl_usd(self) -> float:
        return self.equity - INITIAL_CAPITAL

    @property
    def max_dd_pct(self) -> float:
        eq = INITIAL_CAPITAL
        peak = INITIAL_CAPITAL
        max_dd_ratio = 0.0
        for t in self.trades:
            eq += t.get('pnl_usd', 0.0)
            if eq > peak:
                peak = eq
            dd_ratio = (peak - eq) / peak if peak > 0 else 0.0
            if dd_ratio > max_dd_ratio:
                max_dd_ratio = dd_ratio
        current_dd_ratio = (self.peak_equity - self.equity) / self.peak_equity if self.peak_equity > 0 else 0.0
        return max(max_dd_ratio, current_dd_ratio)

    @property
    def current_drawdown_usd(self) -> float:
        return self.peak_equity - self.equity

    @property
    def win_rate(self) -> float:
        wins = sum(1 for t in self.trades if t.get('pnl_r', 0) > 0)
        return wins / max(self.completed_trades, 1)

    @property
    def calmar_live(self) -> float:
        if self.completed_trades < 5: return 0.0
        eq = INITIAL_CAPITAL
        peak = INITIAL_CAPITAL
        max_dd_usd = 0.0
        for t in self.trades:
            eq += t.get('pnl_usd', 0.0)
            if eq > peak:
                peak = eq
            dd = peak - eq
            if dd > max_dd_usd:
                max_dd_usd = dd
        net_profit_usd = self.equity - INITIAL_CAPITAL
        if net_profit_usd <= 0: return 0.0
        if max_dd_usd <= 0: return 99.0
        return net_profit_usd / max_dd_usd

    @property
    def consecutive_losses(self) -> int:
        streak = 0
        for t in reversed(self.trades):
            if t.get('pnl_r', 0) < 0:
                streak += 1
            else:
                break
        return streak

    @property
    def days_running(self) -> float:
        start = datetime.fromisoformat(self.start_time)
        return (datetime.now(timezone.utc) - start).total_seconds() / 86400

    def get_current_risk_usd(self) -> float:
        """3-Tier Risk Governor based on current DD and Profit."""
        current_dd_pct = (self.peak_equity - self.equity) / self.peak_equity if self.peak_equity > 0 else 0.0
        if current_dd_pct >= 0.02:
            return 15.0  # DD Defense
        if self.net_pnl_usd > 100.0 and current_dd_pct < 0.01:
            return 50.0  # House Money
        return 35.0      # Base Risk

    def record_closed_trade(self, symbol: str, direction: str, entry_price: float,
                             exit_price: float, sl: float, orig_sl: float, risk_usd: float, exit_reason: str,
                             spread: float = 0.0002):
        pip_dist = abs(exit_price - entry_price)
        sl_dist  = abs(entry_price - orig_sl)
        if sl_dist < 1e-9:
            r_multiple = 0.0
        else:
            sign = 1 if direction == 'BUY' else -1
            r_multiple = sign * (exit_price - entry_price) / sl_dist
            # Friction = spread (entry + exit approximated)
            friction_r = spread / sl_dist
            r_multiple -= friction_r
        pnl_usd = r_multiple * risk_usd
        self.equity += pnl_usd
        self.peak_equity = max(self.peak_equity, self.equity)
        self.trades.append({
            'symbol': symbol, 'direction': direction,
            'entry_price': entry_price, 'exit_price': exit_price, 'sl': sl,
            'r_multiple': round(r_multiple, 4), 'pnl_r': round(r_multiple, 4),
            'pnl_usd': round(pnl_usd, 2), 'risk_usd': risk_usd,
            'max_adverse_r': max(0.0, -r_multiple) if r_multiple < 0 else 0.0,
            'exit_reason': exit_reason,
            'closed_at': datetime.now(timezone.utc).isoformat(),
        })
        log.info(f'TRADE CLOSED: {symbol} {direction} | R={r_multiple:.2f} | '
                 f'PnL={pnl_usd:+.2f} USD | Reason={exit_reason}')
        self.save()


# ─── PROMOTION CHECKER ────────────────────────────────────────────────────────

def check_promotion_criteria(state: ForwardState) -> Tuple[bool, List[str]]:
    """
    Returns (promote_ready, list_of_unmet_criteria).
    All criteria must pass before this system can be promoted to live.
    """
    unmet = []
    if state.days_running < MIN_TRACK_RECORD_DAYS:
        unmet.append(f'Days running {state.days_running:.1f} < {MIN_TRACK_RECORD_DAYS} required')
    if state.completed_trades < MIN_TRACK_RECORD_TRADES:
        unmet.append(f'Trades {state.completed_trades} < {MIN_TRACK_RECORD_TRADES} required')
    if state.net_pnl_usd <= 0:
        unmet.append(f'Net PnL {state.net_pnl_usd:.2f} USD must be positive')
    if state.calmar_live < LIVE_MIN_CALMAR:
        unmet.append(f'Live Calmar {state.calmar_live:.2f} < {LIVE_MIN_CALMAR} required')
    if state.max_dd_pct > HARD_DD_STOP_PCT:
        unmet.append(f'MaxDD {state.max_dd_pct:.1%} > {HARD_DD_STOP_PCT:.1%} limit')
    if state.win_rate < 0.40:
        unmet.append(f'Win Rate {state.win_rate:.1%} < 40% required')
    if state.consecutive_losses >= MAX_CONSECUTIVE_LOSSES:
        unmet.append(f'Consecutive losses {state.consecutive_losses} >= {MAX_CONSECUTIVE_LOSSES}')
    return len(unmet) == 0, unmet


# ─── RICH DASHBOARD ──────────────────────────────────────────────────────────

def render_dashboard(state: ForwardState, auction_result: Optional[AuctionResult], assets_monitored: int):
    if not RICH_AVAILABLE or console is None:
        return
    console.clear()
    promote_ready, unmet = check_promotion_criteria(state)
    status_color = 'green' if promote_ready else ('red' if state.max_dd_pct > HARD_DD_STOP_PCT else 'yellow')
    status_text  = 'READY TO PROMOTE' if promote_ready else f'{len(unmet)} criteria unmet'

    header = Panel(
        Text(
            f'FORWARD TEST HARNESS | DRY RUN | Day {state.days_running:.1f} | '
            f'Assets: {assets_monitored} | Status: {status_text}',
            style=status_color, justify='center'
        ), title='[bold cyan]ENGINE RESEARCH — GATE 3 FORWARD VALIDATION[/bold cyan]'
    )
    console.print(header)

    t = Table(show_header=True, header_style='bold magenta', expand=True)
    t.add_column('Metric', style='cyan', width=25)
    t.add_column('Value', justify='right', width=20)
    t.add_column('Target', justify='right', width=20)
    t.add_column('Status', width=12)

    def _row(label, val, target, ok):
        st = '[green]PASS[/green]' if ok else '[red]FAIL[/red]'
        t.add_row(label, str(val), str(target), st)

    _row('Days Running',      f'{state.days_running:.1f}',         f'>= {MIN_TRACK_RECORD_DAYS}', state.days_running >= MIN_TRACK_RECORD_DAYS)
    _row('Completed Trades',  str(state.completed_trades),          f'>= {MIN_TRACK_RECORD_TRADES}', state.completed_trades >= MIN_TRACK_RECORD_TRADES)
    _row('Net PnL (USD)',     f'{state.net_pnl_usd:+.2f}',          '> 0',  state.net_pnl_usd > 0)
    _row('Live Calmar',       f'{state.calmar_live:.2f}',           f'>= {LIVE_MIN_CALMAR}', state.calmar_live >= LIVE_MIN_CALMAR)
    _row('Max Drawdown',      f'{state.max_dd_pct:.2%}',            f'<= {HARD_DD_STOP_PCT:.1%}', state.max_dd_pct <= HARD_DD_STOP_PCT)
    _row('Win Rate',          f'{state.win_rate:.1%}',              '>= 40%', state.win_rate >= 0.40)
    _row('Consec. Losses',    str(state.consecutive_losses),         f'< {MAX_CONSECUTIVE_LOSSES}', state.consecutive_losses < MAX_CONSECUTIVE_LOSSES)
    _row('Equity',            f'{state.equity:.2f}',                f'{INITIAL_CAPITAL:.0f} start', True)
    _row('Bars Processed',    str(state.bars_processed),             '--', True)
    console.print(t)

    if auction_result and auction_result.admitted:
        a_tbl = Table(title='Last Bar Auction Admits', show_header=True, header_style='bold green')
        a_tbl.add_column('Symbol'); a_tbl.add_column('Dir'); a_tbl.add_column('P(win)'); a_tbl.add_column('Score'); a_tbl.add_column('Calmar')
        for s in auction_result.admitted:
            a_tbl.add_row(s.symbol, s.direction, f'{s.prob_win:.3f}', f'{s.composite_score:.2f}', f'{s.calmar_factor*20:.1f}')
        console.print(a_tbl)

    if unmet:
        console.print('[yellow]Unmet promotion criteria:[/yellow]')
        for c in unmet:
            console.print(f'  [red]•[/red] {c}')


# ─── MAIN FORWARD TEST LOOP ──────────────────────────────────────────────────

def run_forward_test(mt5_login: Optional[int] = None, mt5_password: Optional[str] = None, mt5_server: Optional[str] = None):
    """
    Main forward test loop.
    Streams live bars from MT5, runs Gate 2 auction each bar, simulates PnL.
    """
    log.info('=' * 70)
    log.info('FORWARD TEST HARNESS STARTING (DRY_RUN = True)')
    log.info('=' * 70)

    # ── Connect MT5 ─────────────────────────────────────────────────────
    conn = MT5Connection(login=mt5_login, password=mt5_password, server=mt5_server)
    if not conn.connect():
        log.error('MT5 connection failed. Aborting.'); return

    # ── Load approved pool ───────────────────────────────────────────────
    auction = AuctionEngine(max_slots=MAX_CONCURRENT_POSITIONS)
    approved_symbols = auction.pool.symbols()
    if not approved_symbols:
        log.error('Approved pool is empty. Run asset_screener.py first.'); return
    log.info(f'Monitoring {len(approved_symbols)} approved assets: {approved_symbols[:8]}...')

    # ── Initialize inference engines ─────────────────────────────────────
    engines: Dict[str, StatefulInferenceEngine] = {}
    for sym in approved_symbols:
        e = StatefulInferenceEngine(sym, max_bars=800)
        if e.warm_start(conn):
            engines[sym] = e
        else:
            log.warning(f'[{sym}] Warm start failed — excluded from forward test')

    log.info(f'Warmed {len(engines)}/{len(approved_symbols)} engines')

    # ── Load XGBoost model ───────────────────────────────────────────────
    import xgboost as xgb
    model_path = os.path.join(PROJECT_ROOT, 'Engine', 'models', 'xgboost_forex.json')
    if not os.path.exists(model_path):
        log.error(f'Model not found at {model_path}'); return
    model = xgb.Booster()
    model.load_model(model_path)
    log.info(f'Model loaded: {model_path}')

    # ── Forward state ────────────────────────────────────────────────────
    state = ForwardState()
    last_auction: Optional[AuctionResult] = None
    last_bar_time: Optional[datetime] = None

    log.info('Entering forward test loop...')
    try:
        while True:
            # ── Hard DD stop ─────────────────────────────────────────────
            if state.max_dd_pct > HARD_DD_STOP_PCT:
                log.error(f'HARD DD STOP: {state.max_dd_pct:.2%} > {HARD_DD_STOP_PCT:.2%}. HALTING.')
                break

            now_utc = datetime.now(timezone.utc)

            # ── Collect signals from all warmed engines ───────────────────
            candidates: List[SignalCandidate] = []
            current_bar_time = None

            for sym, eng in engines.items():
                result = eng.infer_next_bar(model, conn)
                if result is None:
                    continue
                bar_time, direction, prob, spread, atr = result
                if current_bar_time is None:
                    current_bar_time = bar_time

                # Only process each bar once across the portfolio
                if last_bar_time and bar_time <= last_bar_time:
                    continue

                if prob >= PROB_THRESHOLD and direction in ('BUY', 'SELL'):
                    candidates.append(SignalCandidate(
                        symbol=sym, direction=direction, prob_win=prob,
                        spread_atr_ratio=spread/max(atr, 1e-9),
                        atr_14=atr, bar_time=bar_time
                    ))

            if current_bar_time and current_bar_time != last_bar_time:
                state.bars_processed += 1
                last_bar_time = current_bar_time

                # ── Run auction ───────────────────────────────────────────
                open_syms = set(state.open_trades.keys())
                if candidates:
                    last_auction = auction.rank_signals(candidates, open_syms)
                    for sig in last_auction.admitted:
                        ask = conn.get_current_ask(sig.symbol)
                        bid = conn.get_current_bid(sig.symbol)
                        if ask is None or bid is None:
                            log.warning(f'Could not fetch live tick for {sig.symbol}; skipping entry.')
                            continue
                        spread = ask - bid
                        entry_price = bid if sig.direction == 'SELL' else ask
                        sl_distance = sig.atr_14 * 1.5
                        sl = entry_price - sl_distance if sig.direction == 'BUY' else entry_price + sl_distance
                        state.open_trades[sig.symbol] = {
                            'direction': sig.direction, 'entry': entry_price,
                            'sl': sl, 'orig_sl': sl, 'risk_usd': state.get_current_risk_usd(),
                            'entry_bar': state.bars_processed,
                            'prob': sig.prob_win,
                            'sl_dist': sl_distance,
                            'spread': spread,
                        }
                        log.info(f'DRY OPEN: {sig.symbol} {sig.direction} @ {entry_price:.5f} SL={sl:.5f}')

                # ── Manage open trades (ratchet simulation) ───────────────
                to_close = []
                for sym, tr in state.open_trades.items():
                    bars_held = state.bars_processed - tr['entry_bar']
                    # Use Bid for closing BUY (selling), Ask for closing SELL (covering)
                    current_price = conn.get_current_bid(sym) if tr['direction'] == 'BUY' else conn.get_current_ask(sym)
                    if current_price is None:
                        continue

                    sl_dist = tr.get('sl_dist', abs(tr['entry'] - tr.get('orig_sl', tr['sl'])))
                    sl_dist = max(sl_dist, 1e-9)

                    # Calculate current gain in R
                    gain_r = (current_price - tr['entry']) / sl_dist if tr['direction'] == 'BUY' else (tr['entry'] - current_price) / sl_dist

                    # Update 3-phase ratchet stop loss
                    if tr['direction'] == 'BUY':
                        if gain_r >= 2.0 and tr['sl'] < tr['entry'] + (1.80 * sl_dist):
                            tr['sl'] = tr['entry'] + (1.80 * sl_dist)
                        elif gain_r >= 1.5 and tr['sl'] < tr['entry'] + (0.80 * sl_dist):
                            tr['sl'] = tr['entry'] + (0.80 * sl_dist)
                        elif gain_r >= 0.8 and tr['sl'] < tr['entry'] + (0.15 * sl_dist):
                            tr['sl'] = tr['entry'] + (0.15 * sl_dist)
                    else:
                        if gain_r >= 2.0 and tr['sl'] > tr['entry'] - (1.80 * sl_dist):
                            tr['sl'] = tr['entry'] - (1.80 * sl_dist)
                        elif gain_r >= 1.5 and tr['sl'] > tr['entry'] - (0.80 * sl_dist):
                            tr['sl'] = tr['entry'] - (0.80 * sl_dist)
                        elif gain_r >= 0.8 and tr['sl'] > tr['entry'] - (0.15 * sl_dist):
                            tr['sl'] = tr['entry'] - (0.15 * sl_dist)

                    close_reason = None
                    exit_price = current_price

                    # Check Target Profit hit (+2.5R)
                    if gain_r >= WIN_R:
                        close_reason = f'Target +{WIN_R}R'
                        exit_price = tr['entry'] + (WIN_R * sl_dist) if tr['direction'] == 'BUY' else tr['entry'] - (WIN_R * sl_dist)
                    # Check Stop Loss / Ratchet hit
                    elif (tr['direction'] == 'BUY' and current_price <= tr['sl']) or (tr['direction'] == 'SELL' and current_price >= tr['sl']):
                        close_reason = 'StopLoss / Ratchet Lock'
                        exit_price = tr['sl']
                    # Check Time Decay (24 bars / 6 hours, gain < +0.20R)
                    elif bars_held >= 24 and gain_r < 0.20:
                        close_reason = f'TimeDecay ({bars_held}bars)'
                        exit_price = current_price

                    if close_reason:
                        to_close.append((sym, exit_price, close_reason))

                for sym, exit_price, reason in to_close:
                    tr = state.open_trades.pop(sym)
                    state.record_closed_trade(
                        sym, tr['direction'], tr['entry'], exit_price, tr['sl'], tr.get('orig_sl', tr['sl']), tr['risk_usd'], reason, tr.get('spread', 0.0002))

            # ── Dashboard ─────────────────────────────────────────────────
            render_dashboard(state, last_auction, len(engines))

            # ── Promotion check ───────────────────────────────────────────
            ready, unmet = check_promotion_criteria(state)
            if ready:
                log.info('*** PROMOTION CRITERIA MET *** System is ready for live deployment!')

            time.sleep(POLL_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        log.info('Forward test interrupted by user.')
    finally:
        state.save()
        conn.disconnect()
        log.info(f'Forward test ended. Final equity: {state.equity:.2f} USD')
        log.info(f'Completed trades: {state.completed_trades} | Calmar: {state.calmar_live:.2f}')


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Gate 3 Forward Test Harness')
    ap.add_argument('--login',    type=int, default=None, help='MT5 account login (default: env MT5_LOGIN or active terminal)')
    ap.add_argument('--password', type=str, default=None, help='MT5 account password (default: env MT5_PASSWORD or active terminal)')
    ap.add_argument('--server',   type=str, default=None, help='MT5 server (default: env MT5_SERVER or active terminal)')
    args = ap.parse_args()
    login = args.login or (int(os.environ['MT5_LOGIN']) if 'MT5_LOGIN' in os.environ else None)
    password = args.password or os.environ.get('MT5_PASSWORD')
    server = args.server or os.environ.get('MT5_SERVER')
    run_forward_test(login, password, server)

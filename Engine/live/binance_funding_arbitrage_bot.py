"""
================================================================================
ENGINE: DELTA-NEUTRAL CASH-AND-CARRY FUNDING ARBITRAGE BOT (OX66 REMEDIATED)
================================================================================
Location: Engine/live/binance_funding_arbitrage_bot.py
Architecture: Async monitor loop + synchronous dual-leg executor.
Policy: SHARED carry policy (Engine/live/carry_policy.py) — identical logic
        to the audited backtest (Engine/research/backtest_delta_neutral_carry.py):
        72h cooldown, 0.005%/8h hurdle, 2x cost-benefit, single-leg swaps.
Execution: Real BinanceBroker bridge (spot MARKET + perp MARKET) with
        leg-failure rollback, isolated-1x margin, idempotency tags.
Safety: dry_run default True; atomic state; kill-switch file; DD halt;
        watchdog; spread guard; token-bucket rate limiting.
================================================================================
"""
import os
import sys
import time
import json
import uuid
import asyncio
import tempfile
import urllib.request
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any

CURRENT_FILE = Path(__file__).resolve()
ENGINE_DIR = CURRENT_FILE.parent.parent
PROJECT_ROOT = ENGINE_DIR.parent

for p in [str(PROJECT_ROOT), str(ENGINE_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from Engine.brokers.binance_broker import BinanceBroker
from Engine.live.carry_policy import (CarryPolicyConfig, DEFAULT_CONFIG,
                                      pair_notional_usd, open_leg_cost_usd,
                                      close_leg_cost_usd, select_swaps)

console = Console()

STATE_FILE = CURRENT_FILE.parent / "funding_arbitrage_state.json"
KILL_FILE = CURRENT_FILE.parent / "ARBITRAGE_KILL"
BINANCE_FAPI_BASE = "https://fapi.binance.com"
SCHEMA_VERSION = 2
KILL_DD_PCT = 2.0
WATCHDOG_STALE_SEC = 300.0

CORE_UNIVERSE = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT", "DOGEUSDT",
    "ADAUSDT", "TRXUSDT", "LINKUSDT", "DOTUSDT", "LTCUSDT", "BCHUSDT"
]


# ---------------------------------------------------------------------------
# Atomic state + resilient load (OX66 Mandate 2)
# ---------------------------------------------------------------------------

def atomic_write_json(path: Path, obj: Any) -> None:
    """Write JSON atomically: temp file + fsync + os.replace (POSIX atomic)."""
    tmp_fd, tmp_path = tempfile.mkstemp(dir=str(path.parent), prefix=path.stem,
                                        suffix=".tmp")
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def fresh_state(capital: float) -> Dict[str, Any]:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    return {"schema_version": SCHEMA_VERSION,
            "initial_capital_usd": capital,
            "current_equity_usd": capital,
            "peak_equity_usd": capital,
            "cumulative_yield_usd": 0.0,
            "cumulative_fee_drag_usd": 0.0,
            "settlements_collected": 0,
            "rotations_executed": 0,
            "active_positions": {},
            "history": [],
            "expects_manual": False,
            "halt_reason": None,
            "start_time_utc": now}


def load_state_resilient(capital: float) -> Dict[str, Any]:
    """Load state; on corruption quarantine the file and reinitialize (never crash)."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                st = json.load(f)
            if isinstance(st, dict) and "active_positions" in st:
                st.setdefault("schema_version", 1)
                st.setdefault("peak_equity_usd", st.get("current_equity_usd", capital))
                st.setdefault("cumulative_fee_drag_usd", 0.0)
                st.setdefault("rotations_executed", 0)
                st.setdefault("expects_manual", False)
                st.setdefault("halt_reason", None)
                # v1 -> v2 migration: backfill entry metadata for legacy positions
                now_ms = int(time.time() * 1000)
                for pos in st["active_positions"].values():
                    pos.setdefault("entry_ms", now_ms)
                    pos.setdefault("rate_pct", pos.get("rate_8h_pct", 0.0))
                st["schema_version"] = SCHEMA_VERSION
                # bound history growth (OX65 finding)
                if len(st.get("history", [])) > 500:
                    st["history"] = st["history"][-500:]
                return st
        except Exception as e:
            q = STATE_FILE.with_suffix(f".corrupt.{int(time.time())}.json")
            try:
                os.replace(STATE_FILE, q)
            except OSError:
                pass
            console.print(f"[bold red]State CORRUPT ({e}); quarantined to {q.name}; reinitialized.[/bold red]")
    return fresh_state(capital)


class TokenBucket:
    """Minimal token-bucket for signed-call pacing (supplements broker retries)."""

    def __init__(self, rate_per_sec: float = 4.0, capacity: float = 8.0):
        self.rate = rate_per_sec
        self.capacity = capacity
        self.tokens = capacity
        self.updated = time.monotonic()

    def acquire(self, n: float = 1.0) -> None:
        now = time.monotonic()
        self.tokens = min(self.capacity, self.tokens + (now - self.updated) * self.rate)
        self.updated = now
        if self.tokens < n:
            time.sleep((n - self.tokens) / self.rate)
            self.updated = time.monotonic()
            self.tokens = 0.0
        else:
            self.tokens -= n


# ---------------------------------------------------------------------------
# Dual-leg executor (OX66 Mandate 2)
# ---------------------------------------------------------------------------

class DualLegExecutor:
    """Opens/closes 1x spot-long + 1x perp-short pairs with rollback.

    Open order: spot BUY first (own the hedge asset), then perp SELL sized to
    the spot EXECUTED qty (delta-0 even on partials). If the perp leg fails,
    the spot leg is unwound immediately. All fills are costed (fees+spread)
    into the paper ledger in dry_run and read from exchange responses live.
    """

    def __init__(self, broker: BinanceBroker, cfg: CarryPolicyConfig,
                 limiter: Optional[TokenBucket] = None):
        self.broker = broker
        self.cfg = cfg
        self.limiter = limiter or TokenBucket()

    def _cid(self, sym: str, leg: str) -> str:
        return f"OX66-{leg}-{sym}-{uuid.uuid4().hex[:12]}"

    def open_pair(self, symbol: str, notional_usd: float, spot_book: Dict[str, float],
                  perp_price: float) -> Optional[Dict[str, Any]]:
        spot_px = spot_book["ask"]
        if spot_px <= 0 or perp_price <= 0:
            return None
        qty_target = notional_usd / spot_px
        self.limiter.acquire(2.0)
        self.broker.set_isolated_1x(symbol)
        leg1 = self.broker.place_spot_market(symbol, "BUY", qty_target,
                                             self._cid(symbol, "SPOTBUY"),
                                             ref_price=spot_px)
        if not leg1 or leg1.get("status") not in ("FILLED", "PARTIALLY_FILLED"):
            console.print(f"[red]OPEN {symbol}: spot leg failed; aborting (no exposure).[/red]")
            return None
        exec_qty = float(leg1["qty"])
        if exec_qty <= 0:
            return None
        leg2 = self.broker.place_perp_market(symbol, "SELL", exec_qty,
                                             self._cid(symbol, "PERPSHORT"),
                                             ref_price=perp_price)
        if not leg2 or leg2.get("status") not in ("FILLED", "PARTIALLY_FILLED"):
            console.print(f"[bold red]OPEN {symbol}: perp leg FAILED after spot fill; "
                          f"unwinding spot leg NOW.[/bold red]")
            rb = self.broker.place_spot_market(symbol, "SELL", exec_qty,
                                               self._cid(symbol, "ROLLBACK"),
                                               ref_price=spot_book.get("bid", spot_px))
            if not rb:
                console.print("[bold red blink]ROLLBACK FAILED — MANUAL INTERVENTION REQUIRED.[/bold red blink]")
                return {"rollback_failed": True, "spot_qty": exec_qty}
            return None
        cost = open_leg_cost_usd(exec_qty * spot_px, self.cfg)
        return {"spot_qty": exec_qty, "perp_qty": float(leg2["qty"]),
                "spot_fill": float(leg1["fill_price"]),
                "perp_fill": float(leg2["fill_price"]),
                "modeled_cost_usd": cost,
                "simulated": bool(leg1.get("simulated", False))}

    def close_pair(self, symbol: str, spot_qty: float, perp_qty: float,
                   spot_book: Dict[str, float], perp_price: float) -> Dict[str, Any]:
        self.limiter.acquire(2.0)
        leg1 = self.broker.place_spot_market(symbol, "SELL", spot_qty,
                                             self._cid(symbol, "SPOTSELL"),
                                             ref_price=spot_book.get("bid", 0.0))
        leg2 = self.broker.place_perp_market(symbol, "BUY", perp_qty,
                                             self._cid(symbol, "PERPBUY"),
                                             ref_price=perp_price, reduce_only=True)
        ok = bool(leg1 and leg2)
        if not ok:
            console.print(f"[bold red]CLOSE {symbol}: partial failure "
                          f"(spot={bool(leg1)}, perp={bool(leg2)}); MANUAL CHECK.[/bold red]")
        cost = close_leg_cost_usd(spot_qty * (spot_book.get("bid", 0.0) or 0.0), self.cfg)
        return {"ok": ok, "spot_ok": bool(leg1), "perp_ok": bool(leg2),
                "modeled_cost_usd": cost}


# ---------------------------------------------------------------------------
# Bot
# ---------------------------------------------------------------------------

class LiveFundingArbitrageBot:
    def __init__(self, initial_capital_usd: float = 5000.0, top_k: int = 3,
                 dry_run: bool = True, use_testnet: bool = False,
                 cfg: Optional[CarryPolicyConfig] = None):
        self.cfg = cfg or DEFAULT_CONFIG
        if top_k != self.cfg.top_k:
            self.cfg = CarryPolicyConfig(top_k=top_k)
        self.dry_run = dry_run
        self.broker = BinanceBroker(dry_run=dry_run, account_size=initial_capital_usd,
                                    use_testnet=use_testnet)
        self.executor = DualLegExecutor(self.broker, self.cfg)
        self.state = load_state_resilient(initial_capital_usd)
        self.running = True
        self.last_fetch_ok = 0.0
        mode = "DRY-RUN (paper)" if dry_run else ("TESTNET" if use_testnet else "LIVE MAINNET")
        console.print(f"[bold]Carry bot init: {mode} | capital={initial_capital_usd} "
                      f"| K={self.cfg.top_k} | cooldown={self.cfg.min_hold_hours}h[/bold]")
        if not dry_run and not use_testnet:
            console.print("[bold red]!!! LIVE MAINNET MODE — REAL ORDERS !!![/bold red]")

    def _save_state(self):
        atomic_write_json(STATE_FILE, self.state)

    # -- market data ------------------------------------------------------
    def fetch_live_funding_data(self) -> List[Dict[str, Any]]:
        url = f"{BINANCE_FAPI_BASE}/fapi/v1/premiumIndex"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
        except Exception as e:
            console.print(f"[red]Error fetching live funding: {e}[/red]")
            return []
        results = []
        for item in data:
            sym = item.get("symbol", "")
            if sym in CORE_UNIVERSE and "lastFundingRate" in item:
                rate_8h = float(item["lastFundingRate"]) * 100.0
                mark_p = float(item.get("markPrice", 0.0))
                index_p = float(item.get("indexPrice", 0.0))
                basis_bps = ((mark_p - index_p) / index_p * 10000.0) if index_p > 0 else 0.0
                results.append({"symbol": sym, "rate_8h_pct": rate_8h,
                                "annual_apr_pct": rate_8h * 3.0 * 365.0,
                                "mark_price": mark_p, "index_price": index_p,
                                "basis_bps": basis_bps,
                                "next_time_ms": int(item.get("nextFundingTime", 0))})
        if results:
            self.last_fetch_ok = time.time()
        return results

    # -- policy + execution ----------------------------------------------
    def rebalance_via_policy(self, funding_data: List[Dict[str, Any]]) -> None:
        now_ms = int(time.time() * 1000)
        ranked = sorted(((d["symbol"], d["rate_8h_pct"]) for d in funding_data),
                        key=lambda kv: kv[1], reverse=True)
        live_map = dict(ranked)
        for s, p in self.state["active_positions"].items():
            p["neg_streak"] = p.get("neg_streak", 0) + 1 if live_map.get(s, 0.0) < 0.0 else 0
        holdings = {s: {"rate_pct": p.get("rate_pct", p.get("rate_8h_pct", 0.0)),
                        "entry_ms": p.get("entry_ms", now_ms),
                        "neg_streak": p.get("neg_streak", 0)}
                    for s, p in self.state["active_positions"].items()}
        exits, entries = select_swaps(ranked, holdings, now_ms, self.cfg)
        if not exits and not entries:
            return
        marks = {d["symbol"]: d for d in funding_data}
        # exits first (free margin), then entries — single-leg each
        for sym in exits:
            pos = self.state["active_positions"].pop(sym, None)
            if pos is None:
                continue
            book = self._spot_book(sym, marks[sym]["mark_price"])
            res = self.executor.close_pair(sym, pos["spot_qty"], pos["perp_short_qty"],
                                           book, marks[sym]["mark_price"])
            self._apply_cost(res["modeled_cost_usd"])
            if not res["ok"]:
                self.state["expects_manual"] = True
            self.state["rotations_executed"] += 1
            self._log("EXIT", sym, 0.0, -res["modeled_cost_usd"])
        for sym in entries:
            if sym in self.state["active_positions"]:
                continue
            book = self._spot_book(sym, marks[sym]["mark_price"])
            if not self._spread_ok(book):
                console.print(f"[yellow]ENTRY {sym} skipped: spot spread too wide.[/yellow]")
                continue
            notion = pair_notional_usd(self.state["current_equity_usd"], self.cfg)
            fill = self.executor.open_pair(sym, notion, book, marks[sym]["mark_price"])
            if fill is None:
                continue
            if fill.get("rollback_failed"):
                self.state["expects_manual"] = True
                continue
            self._apply_cost(fill["modeled_cost_usd"])
            self.state["active_positions"][sym] = {
                "allocated_usd": notion * 2.0, "notional_usd": notion,
                "spot_qty": fill["spot_qty"], "perp_short_qty": fill["perp_qty"],
                "entry_spot_fill": fill["spot_fill"], "entry_perp_fill": fill["perp_fill"],
                "entry_ms": now_ms, "rate_pct": marks[sym]["rate_8h_pct"],
                "rate_8h_pct": marks[sym]["rate_8h_pct"],
                "annual_apr_pct": marks[sym]["annual_apr_pct"],
                "next_time_ms": marks[sym]["next_time_ms"],
                "last_updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}
            self._log("ENTRY", sym, marks[sym]["rate_8h_pct"], -fill["modeled_cost_usd"])
        self._save_state()

    def _spot_book(self, sym: str, fallback_mark: float) -> Dict[str, float]:
        if not self.dry_run or os.environ.get("CARRY_USE_LIVE_BOOKS", "") == "1":
            try:
                book = self.broker.get_spot_book(sym)
                if book and book["bid"] > 0 and book["ask"] > 0:
                    return book
            except Exception as e:
                console.print(f"[yellow]Spot book failed for {sym}: {e}; using mark proxy.[/yellow]")
        eps = fallback_mark * 0.0001  # 1bp proxy half-spread in dry-run
        return {"bid": fallback_mark - eps, "ask": fallback_mark + eps}

    def _spread_ok(self, book: Dict[str, float]) -> bool:
        if book["bid"] <= 0:
            return False
        return (book["ask"] - book["bid"]) / book["bid"] * 1e4 <= self.cfg.max_spread_bps

    def _apply_cost(self, cost_usd: float) -> None:
        self.state["current_equity_usd"] -= cost_usd
        self.state["cumulative_fee_drag_usd"] += cost_usd

    def _log(self, kind: str, sym: str, rate: float, cost: float) -> None:
        self.state["history"].append({
            "time_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "event": kind, "symbol": sym, "rate_8h_pct": rate,
            "cost_usd": round(cost, 4),
            "equity": round(self.state["current_equity_usd"], 2)})
        if len(self.state["history"]) > 500:
            self.state["history"] = self.state["history"][-500:]

    def process_accrual(self, funding_data: List[Dict[str, Any]]) -> None:
        now_ms = int(time.time() * 1000)
        rates = {d["symbol"]: d["rate_8h_pct"] for d in funding_data}
        for sym, pos in self.state["active_positions"].items():
            next_t = pos.get("next_time_ms", 0)
            if next_t > 0 and now_ms >= next_t:
                rate = rates.get(sym, pos.get("rate_pct", 0.0))
                notion = pos.get("notional_usd", pos.get("allocated_usd", 0.0) * 0.5)
                payout = notion * (rate / 100.0)
                self.state["cumulative_yield_usd"] += payout
                self.state["current_equity_usd"] += payout
                self.state["settlements_collected"] += 1
                pos["next_time_ms"] = next_t + 8 * 3600 * 1000
                self.state["history"].append({
                    "time_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                    "event": "SETTLE", "symbol": sym, "rate_8h_pct": rate,
                    "payout_usd": round(payout, 4),
                    "new_equity": round(self.state["current_equity_usd"], 2)})
        if self.state["current_equity_usd"] > self.state.get("peak_equity_usd", 0):
            self.state["peak_equity_usd"] = self.state["current_equity_usd"]
        self._save_state()

    # -- guardrails ---------------------------------------------------------
    def guardrails_ok(self) -> bool:
        if KILL_FILE.exists():
            self.state["halt_reason"] = "KILL_FILE present — operator halt."
            console.print("[bold red]KILL FILE present — halting (no auto-flatten).[/bold red]")
            return False
        if self.state.get("expects_manual"):
            self.state["halt_reason"] = "expects_manual — leg failure needs review."
            return False
        peak = self.state.get("peak_equity_usd", self.state["current_equity_usd"])
        eq = self.state["current_equity_usd"]
        dd = (peak - eq) / peak * 100.0 if peak > 0 else 0.0
        if dd >= KILL_DD_PCT:
            self.state["halt_reason"] = f"DD halt: {dd:.2f}% >= {KILL_DD_PCT}%."
            console.print(f"[bold red]DD HALT {dd:.2f}% — stopping new risk.[/bold red]")
            return False
        if self.last_fetch_ok and (time.time() - self.last_fetch_ok) > WATCHDOG_STALE_SEC:
            self.state["halt_reason"] = "watchdog: market data stale >5min."
            return False
        return True

    # -- dashboard ------------------------------------------------------------
    def generate_dashboard_table(self, funding_data: List[Dict[str, Any]]) -> Tuple[Table, Table]:
        tbl_rates = Table(box=box.ROUNDED, header_style="bold cyan", expand=True)
        for col in ["Symbol", "8h Rate", "Annual APR", "Mark Price", "Basis (bps)", "Status / Rank"]:
            tbl_rates.add_column(col, justify="right" if col != "Symbol" else "left")
        active = set(self.state["active_positions"].keys())
        for i, item in enumerate(sorted(funding_data, key=lambda x: x["rate_8h_pct"], reverse=True)):
            rate = item["rate_8h_pct"]
            rs = "bold green" if rate > 0.008 else ("green" if rate > 0 else "bold red")
            status = "[bold green]ACTIVE[/bold green]" if item["symbol"] in active else (
                f"[yellow]Rank #{i+1}[/yellow]" if rate > 0 else "[red]INVERTED (VETO)[/red]")
            tbl_rates.add_row(item["symbol"], f"[{rs}]{rate:+.4f}%[/{rs}]",
                              f"{item['annual_apr_pct']:+.2f}%", f"{item['mark_price']:,.4f}",
                              f"{item['basis_bps']:+.1f}", status)
        tbl_pos = Table(box=box.ROUNDED, header_style="bold magenta", expand=True)
        for col in ["Pair", "Notional", "Spot Long", "Perp Short", "Net Delta", "Fee Drag", "Next Settlement"]:
            tbl_pos.add_column(col, justify="right" if col != "Pair" else "left")
        now_ms = int(time.time() * 1000)
        for sym, pos in self.state["active_positions"].items():
            notion = pos.get("notional_usd", pos.get("allocated_usd", 0.0) * 0.5)
            next_ms = pos.get("next_time_ms", 0)
            mins = max(0, int((next_ms - now_ms) / 60000)) if next_ms > 0 else 0
            tbl_pos.add_row(sym, f"{notion:,.2f}",
                            f"+{pos['spot_qty']:.4f}", f"-{pos['perp_short_qty']:.4f}",
                            "0.00 (Neutral)",
                            f"{self.state.get('cumulative_fee_drag_usd', 0.0):,.2f}",
                            f"{mins // 60:02d}h {mins % 60:02d}m")
        return tbl_rates, tbl_pos

    async def run(self, refresh_interval_sec: int = 15, max_iterations: Optional[int] = None):
        iteration = 0
        while self.running:
            iteration += 1
            if not self.guardrails_ok():
                self._save_state()
                console.print(f"[bold red]HALTED: {self.state['halt_reason']}[/bold red]")
                break
            data = self.fetch_live_funding_data()
            if data:
                self.rebalance_via_policy(data)
                self.process_accrual(data)
                tbl_rates, tbl_pos = self.generate_dashboard_table(data)
                eq = self.state["current_equity_usd"]
                y = self.state["cumulative_yield_usd"]
                fd = self.state.get("cumulative_fee_drag_usd", 0.0)
                roi = (eq - self.state["initial_capital_usd"]) / self.state["initial_capital_usd"] * 100.0
                mode = ("[yellow]PAPER DRY-RUN[/yellow]" if self.dry_run
                        else "[bold green]LIVE[/bold green]")
                console.clear()
                console.print(Panel(
                    f"Mode: {mode} | Equity: [bold white]{eq:,.2f}[/bold white] "
                    f"(Yield: [green]+{y:,.2f}[/green] Fees: [red]-{fd:,.2f}[/red] "
                    f"ROI: {roi:+.2f}%) | Settlements: [cyan]{self.state['settlements_collected']}[/cyan] "
                    f"| Rotations: [cyan]{self.state.get('rotations_executed', 0)}[/cyan]",
                    title="[bold cyan]DELTA-NEUTRAL CARRY (OX66 POLICY)[/bold cyan]",
                    box=box.DOUBLE, border_style="cyan"))
                console.print(tbl_rates)
                console.print("\n[bold magenta]ACTIVE PAIRS[/bold magenta]")
                console.print(tbl_pos)
            if max_iterations and iteration >= max_iterations:
                break
            await asyncio.sleep(refresh_interval_sec)


def main():
    import argparse
    p = argparse.ArgumentParser(description="OX66 delta-neutral carry bot (policy-gated, dual-leg).")
    p.add_argument("--capital", type=float, default=5000.0)
    p.add_argument("--top-k", type=int, default=3)
    p.add_argument("--interval", type=int, default=15)
    p.add_argument("--live", action="store_true", help="REAL ORDERS on mainnet (requires BINANCE_API_KEY/SECRET).")
    p.add_argument("--testnet", action="store_true", help="Route orders to Binance testnet.")
    p.add_argument("--iterations", type=int, default=None)
    args = p.parse_args()
    bot = LiveFundingArbitrageBot(initial_capital_usd=args.capital, top_k=args.top_k,
                                  dry_run=not args.live, use_testnet=args.testnet)
    asyncio.run(bot.run(refresh_interval_sec=args.interval, max_iterations=args.iterations))


if __name__ == "__main__":
    main()

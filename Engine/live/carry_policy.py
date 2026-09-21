"""OX66 Mandates 1+2: shared delta-neutral carry rotation policy.

Single source of truth for BOTH the cost-aware backtest
(Engine/research/backtest_delta_neutral_carry.py) and the live bot
(Engine/live/binance_funding_arbitrage_bot.py). All functions are pure
(no network, no clock reads, no disk) so the backtest and live paths
cannot drift apart and the logic is hermetically unit-testable.

Conventions:
- Funding rates are in PERCENT per 8h interval (Binance `lastFundingRate`
  x 100), e.g. 0.01 == 0.01% per 8h.
- Timestamps are integer epoch milliseconds (UTC).
- A "pair" is 1x spot long + 1x perp short of equal notional.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

MS_PER_HOUR = 3_600_000
SETTLE_HOURS_UTC = (0, 8, 16)


@dataclass(frozen=True)
class CarryPolicyConfig:
    """Pre-committed OX66 parameters (single run; no tuning).

    Fee note: `fee_spot=8bps` is the OX66-mandated value (attainable with
    BNB fee discount / VIP1+). Vanilla Binance VIP0 spot taker is 10bps, so
    8bps is mildly optimistic; the backtest reports a 10bps sensitivity leg.
    """

    top_k: int = 3
    min_rate_pct: float = 0.002  # eligibility floor per 8h (veto below)
    hurdle_rate_pct: float = 0.005  # challenger must beat holding by this
    min_hold_hours: float = 72.0  # cooldown after entry before rotation
    fee_spot: float = 0.0008  # 8 bps (mandated; see note)
    fee_perp: float = 0.0005  # 5 bps
    half_spread_spot: float = 0.0001  # 1 bp each way
    half_spread_perp: float = 0.00005  # 0.5 bp each way
    cash_buffer: float = 0.20  # 20% of equity held in reserve
    cost_benefit_mult: float = 2.0  # expected accrual must exceed mult x cost
    max_spread_bps: float = 35.0  # live spread guard (BinanceBroker parity)


DEFAULT_CONFIG = CarryPolicyConfig()


# ---------------------------------------------------------------------------
# Cost model (one pair rotation, signed economics)
# ---------------------------------------------------------------------------

def open_leg_cost_usd(notional_usd: float, cfg: CarryPolicyConfig = DEFAULT_CONFIG) -> float:
    """Fees + spread to OPEN one pair (spot buy + perp short)."""
    return notional_usd * (cfg.fee_spot + cfg.half_spread_spot
                           + cfg.fee_perp + cfg.half_spread_perp)


def close_leg_cost_usd(notional_usd: float, cfg: CarryPolicyConfig = DEFAULT_CONFIG) -> float:
    """Fees + spread to CLOSE one pair (spot sell + perp buy)."""
    return open_leg_cost_usd(notional_usd, cfg)


def rotation_friction_usd(notional_usd: float,
                          cfg: CarryPolicyConfig = DEFAULT_CONFIG) -> float:
    """Friction for a single-leg swap: close the old pair + open the new one.

    (One open + one close; the 2x cost-benefit multiple is applied by the
    caller per the mandate — NOT doubled here. Basis P&L is accounted
    separately, signed from measured basis, in the backtest.)
    """
    return open_leg_cost_usd(notional_usd, cfg) + close_leg_cost_usd(notional_usd, cfg)


def expected_accrual_usd(notional_usd: float, rate_pct_per_8h: float,
                         hold_hours: float) -> float:
    """Expected funding accrual over a hold horizon (short receives +rate)."""
    return notional_usd * (rate_pct_per_8h / 100.0) * (hold_hours / 8.0)


def pair_notional_usd(equity_usd: float,
                      cfg: CarryPolicyConfig = DEFAULT_CONFIG) -> float:
    """Funding-earning notional per pair: (1-buffer)/K deployed, half per leg.

    1x spot long + 1x perp short: each leg posts notional/2 of pair alloc...
    precisely: pair_alloc = equity*(1-buffer)/K; spot_notional = pair_alloc/2;
    perp margin = pair_alloc/2 backs an equal perp notional at 1x.
    """
    return equity_usd * (1.0 - cfg.cash_buffer) / cfg.top_k * 0.5


# ---------------------------------------------------------------------------
# Rotation decisions (hysteresis + hurdle + cost-benefit)
# ---------------------------------------------------------------------------

def should_replace(holding_rate_pct: float, challenger_rate_pct: float,
                   hours_held: float, notional_usd: float,
                   cfg: CarryPolicyConfig = DEFAULT_CONFIG) -> Tuple[bool, str]:
    """Decide whether a challenger may replace a holding (single-leg swap).

    Requires ALL of: (a) cooldown elapsed, (b) rate hurdle cleared,
    (c) expected accrual over the minimum hold exceeds 2x rotation friction.
    Returns (decision, reason_code).
    """
    if hours_held < cfg.min_hold_hours:
        return False, "cooldown"
    if challenger_rate_pct - holding_rate_pct < cfg.hurdle_rate_pct:
        return False, "hurdle"
    exp = expected_accrual_usd(notional_usd, challenger_rate_pct, cfg.min_hold_hours)
    if exp <= cfg.cost_benefit_mult * rotation_friction_usd(notional_usd, cfg):
        return False, "cost_benefit"
    return True, "rotate"


def select_swaps(ranked: List[Tuple[str, float]],
                 holdings: Dict[str, Dict],
                 now_ms: int,
                 cfg: CarryPolicyConfig = DEFAULT_CONFIG) -> Tuple[List[str], List[str]]:
    """Compute single-leg swaps: (symbols_to_exit, symbols_to_enter).

    `ranked`: all symbols sorted by rate desc (symbol, rate_pct).
    `holdings`: symbol -> {"rate_pct": entry predictor, "entry_ms": int}.
    Policy:
      * eligible = rate >= min_rate_pct; targets = top-K eligible.
      * holdings with neg_streak >= 2 (two consecutive negative settlements)
        are liquidated (hysteresis-gated; single flickers are held).
      * otherwise replace worst-first subject to should_replace(); each
        holding replaced at most once per decision step; never full-book
        rebuilds (bounded churn: at most K swaps, each independently gated).
      * fill empty slots from eligible non-holdings (subject to cost-benefit
        vs rotation friction of a fresh open only).
    """
    eligible = [(s, r) for s, r in ranked if r >= cfg.min_rate_pct]
    eligible_map = dict(eligible)
    targets = [s for s, _ in eligible[:cfg.top_k]]

    exits: List[str] = []
    # 1. Inversion liquidation with hysteresis: exit only after TWO consecutive
    # negative settlements (neg_streak >= 2), so single-print flickers cannot
    # force a 29bps exit. Callers maintain holdings[sym]["neg_streak"].
    live_rates = dict(ranked)
    for sym in list(holdings.keys()):
        if holdings[sym].get("neg_streak", 0) >= 2:
            exits.append(sym)
    remaining = {s: h for s, h in holdings.items() if s not in exits}

    # 2. Single-leg swaps, worst holding first.
    entries: List[str] = []
    notional_probe = 1.0  # hurdle/cost-benefit are notional-scale-free ratios
    for sym in targets:
        if sym in remaining or sym in entries:
            continue
        # worst remaining holding by current rate
        cands = sorted(remaining.items(),
                       key=lambda kv: live_rates.get(kv[0], kv[1].get("rate_pct", 0.0)))
        swapped = False
        for hsym, hinfo in cands:
            if hsym in exits:
                continue
            hours_held = (now_ms - hinfo["entry_ms"]) / MS_PER_HOUR
            ok, _ = should_replace(
                live_rates.get(hsym, hinfo.get("rate_pct", 0.0)),
                live_rates.get(sym, 0.0), hours_held, notional_probe, cfg)
            if ok:
                exits.append(hsym)
                entries.append(sym)
                del remaining[hsym]
                swapped = True
                break
        if not swapped:
            continue

    # 3. Fill empty slots (below top-K count) from eligible non-holdings.
    held_syms = set(remaining.keys()) | set(entries)
    if len(held_syms) < cfg.top_k:
        for sym, rate in eligible:
            if sym in held_syms:
                continue
            exp = expected_accrual_usd(notional_probe, rate, cfg.min_hold_hours)
            if exp > cfg.cost_benefit_mult * (
                    open_leg_cost_usd(notional_probe, cfg)
                    + close_leg_cost_usd(notional_probe, cfg)):
                entries.append(sym)
                held_syms.add(sym)
            if len(held_syms) >= cfg.top_k:
                break

    return exits, entries

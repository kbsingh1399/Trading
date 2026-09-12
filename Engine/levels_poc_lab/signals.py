"""Geometric strategy families around period levels and the Point of Control.

Every family is a *pure function of completed-candle information*: mask, side,
structural stop distance and a cross-sectional score.  Nothing is fitted, so
running a family over the 20 OOS windows is a genuine out-of-sample test of the
concept it encodes.

Parameter choices are fixed a priori and justified by the literature recorded in
``docs/research/LEVELS_POC_STRATEGY_RESEARCH.md``:

* breakouts need participation -- volume >= 1.2x the 96-bar mean (false-breakout
  filter) and a close in the strongest 45 % of the bar's range;
* sweeps are the mirror image: pierce the level, close back inside, so the sweep
  extreme is a tight, structural invalidation;
* POC / value-area logic uses the *developing* session value area for acceptance
  and the *prior completed* session for reference levels (Steidlmayer / Dalton
  market-profile practice).

Stops are structural where a structure exists and are floored at 1.2 % of price
(the certified contract's ``min_stop_fraction``) so the 41 bps round-trip
friction cannot consume an unreasonable share of 1R.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from numba import njit

from . import BAR_MS, DAY_MS

GROUP_ID = {"level_break": 1, "level_sweep": 2, "poc": 3, "confluence": 4}
MIN_STOP_FRACTION = 0.012   # certified contract: 1.2 % of price minimum stop
FRICTION_FLOOR = 0.0041     # certified contract: 41 bps round-trip
BREAK_BUFFER_ATR = 0.25     # stop sits just beyond the broken level
SWEEP_BUFFER_ATR = 0.25     # stop sits just beyond the sweep extreme


@dataclass
class FamilySpec:
    name: str
    group: str            # "level_break", "level_sweep", "poc", "confluence"
    description: str
    horizon_bars: int = 96
    target_r: float = 4.0
    stop_mult: float = 0.5      # ATR floor on the structural stop distance
    max_hold_bars: int = 288
    cooldown_bars: int = 8
    params: dict = field(default_factory=dict)


def _atr(f: pd.DataFrame) -> np.ndarray:
    return np.maximum(f.atr.to_numpy(float), f.close.to_numpy(float) * 0.004)


# The certified suite's own pre-registered geometry is a *pure* ATR stop:
#   stop = max(stop_atr * ATR, min_stop_fraction * close),  stop_atr in (2.5, 3.0)
# (s1_trend_following_suite.apply_signals / candidate_configs).  The lab's default
# structural stop (gap beyond the broken level, floored at 0.5 ATR) is much tighter;
# a geometry screen (scratch/geom_screen.csv) shows the tight stop is stopped out by
# noise and pays ~1.6x the friction per R, which is why every family read negative.
# Setting ATR_STOP_SCALE switches the break families to the certified geometry.
ATR_STOP_SCALE: float | None = None


def _stop(gap: np.ndarray, atr: np.ndarray, close: np.ndarray, mult: float) -> np.ndarray:
    """Stop distance = max(structural gap, mult*ATR, 1.2 % of price).

    With ``ATR_STOP_SCALE`` set the certified pure-ATR stop is used instead:
    ``max(ATR_STOP_SCALE * ATR, 1.2 % of price)``.
    """
    floor = close * MIN_STOP_FRACTION
    if ATR_STOP_SCALE is not None:
        return np.maximum(ATR_STOP_SCALE * atr, floor)
    return np.maximum(np.maximum(gap, mult * atr), floor)


def _vol_confirm(f: pd.DataFrame, thr: float = 1.2) -> np.ndarray:
    return f.volume_rel.to_numpy(float) >= thr


def _strong_close(f: pd.DataFrame, up: bool, frac: float = 0.45) -> np.ndarray:
    h = f.high.to_numpy(float)
    lo = f.low.to_numpy(float)
    c = f.close.to_numpy(float)
    rng = np.maximum(h - lo, 1e-12)
    if up:
        return (c - lo) / rng >= 1.0 - frac
    return (h - c) / rng >= 1.0 - frac


def _trend_ok(f: pd.DataFrame, up: bool) -> np.ndarray:
    c = f.close.to_numpy(float)
    if up:
        return (f.trend_up.to_numpy(int) == 1) | (
            (f.slope200_4h.to_numpy(float) > 0) & (c > f.e200_4h.to_numpy(float))
        )
    return (f.trend_dn.to_numpy(int) == 1) | (
        (f.slope200_4h.to_numpy(float) < 0) & (c < f.e200_4h.to_numpy(float))
    )


# ---------------------------------------------------------------------------
# naked POC tracking (prior-session POCs price has not revisited yet)
# ---------------------------------------------------------------------------


@njit(cache=True)
def naked_poc_series(day, sess_poc, low, high, close, k: int = 10):
    """Nearest *untested* completed-session POC above and below each bar.

    A prior-session POC is "tested" the first time a later bar's range covers it;
    from then on it is no longer an untested magnet.  Only the last ``k`` sessions
    are tracked, which bounds staleness and memory.
    """
    n = len(close)
    up_price = np.full(n, np.nan)
    dn_price = np.full(n, np.nan)
    levels = np.zeros(k)
    valid = np.zeros(k, np.int8)
    count = 0
    prev_day = day[0]
    last_sess = np.nan
    for i in range(n):
        if day[i] != prev_day:
            if np.isfinite(last_sess) and last_sess > 0.0:
                if count < k:
                    levels[count] = last_sess
                    valid[count] = 1
                    count += 1
                else:
                    for j in range(k - 1):
                        levels[j] = levels[j + 1]
                        valid[j] = valid[j + 1]
                    levels[k - 1] = last_sess
                    valid[k - 1] = 1
            prev_day = day[i]
        for j in range(k):
            if valid[j] == 1 and low[i] <= levels[j] <= high[i]:
                valid[j] = 0
        c = close[i]
        best_up = np.nan
        best_dn = np.nan
        for j in range(k):
            if valid[j] == 1:
                lv = levels[j]
                if lv > c and (not np.isfinite(best_up) or lv < best_up):
                    best_up = lv
                if lv < c and (not np.isfinite(best_dn) or lv > best_dn):
                    best_dn = lv
        up_price[i] = best_up
        dn_price[i] = best_dn
        last_sess = sess_poc[i]
    return up_price, dn_price


# ---------------------------------------------------------------------------
# families
# ---------------------------------------------------------------------------


def family_events(f: pd.DataFrame, spec: FamilySpec, naked=None):
    """Return (event_mask, side, stop_distance) for one family on one symbol."""
    n = len(f)
    c = f.close.to_numpy(float)
    h = f.high.to_numpy(float)
    lo = f.low.to_numpy(float)
    op = f.open.to_numpy(float)
    atr = _atr(f)
    side = np.zeros(n, np.int8)
    stop = np.full(n, np.nan)
    mask = np.zeros(n, bool)
    vc = _vol_confirm(f)
    p = spec.params
    name, group = spec.name, spec.group
    mult = spec.stop_mult

    if group == "level_break":
        need_trend = bool(p.get("trend", False))
        use_vol = bool(p.get("vol", True))
        vcm = vc if use_vol else np.ones(n, bool)
        if name in ("brk_pwh", "brk_pmh", "brk_pdh", "brk_pqh"):
            lvl_name = {"brk_pwh": "pwh", "brk_pmh": "pmh", "brk_pdh": "pdh", "brk_pqh": "pqh"}[name]
            lvl = f[lvl_name].to_numpy(float)
            m = (f[f"brk_{lvl_name}"].to_numpy(int) == 1) & vcm & _strong_close(f, True)
            if need_trend:
                m &= _trend_ok(f, True)
            side[m] = 1
            stop[m] = _stop((c - lvl)[m] + BREAK_BUFFER_ATR * atr[m], atr[m], c[m], mult)
        elif name in ("brk_pwl", "brk_pml", "brk_pdl"):
            lvl_name = {"brk_pwl": "pwl", "brk_pml": "pml", "brk_pdl": "pdl"}[name]
            lvl = f[lvl_name].to_numpy(float)
            m = (f[f"brk_{lvl_name}"].to_numpy(int) == 1) & vcm & _strong_close(f, False)
            if need_trend:
                m &= _trend_ok(f, False)
            side[m] = -1
            stop[m] = _stop((lvl - c)[m] + BREAK_BUFFER_ATR * atr[m], atr[m], c[m], mult)
        elif name == "brk_ath":
            m = (f.brk_ath.to_numpy(int) == 1) & vcm & _strong_close(f, True)
            if need_trend:
                m &= _trend_ok(f, True)
            side[m] = 1
            stop[m] = _stop(np.zeros(n), atr, c, max(mult, 1.0))[m]
        elif name == "brk_pwh_cascade":
            dist = (f.pmh.to_numpy(float) - c) / atr
            m = (f.brk_pwh.to_numpy(int) == 1) & vc & (-1.5 < dist) & (dist < 1.5)
            side[m] = 1
            stop[m] = _stop(np.zeros(n), atr, c, max(mult, 1.0))[m]
        elif name == "brk_pwh_retest":
            pw = f.pwh.to_numpy(float)
            within = int(p.get("within", 24))
            recent = pd.Series(f.brk_pwh.to_numpy(int)).rolling(within, min_periods=1).max().to_numpy() > 0
            held = (lo <= pw + 0.15 * atr) & (c > pw) & (c > op)
            m = held & recent & vc
            side[m] = 1
            stop[m] = _stop((c - pw)[m] + BREAK_BUFFER_ATR * atr[m], atr[m], c[m], mult)
        elif name == "brk_multi_lvl":
            ev = (f.brk_pwh.to_numpy(int) + f.brk_pmh.to_numpy(int) + f.brk_ath.to_numpy(int)
                  + f.brk_pdh.to_numpy(int))
            e = pd.Series(ev).rolling(8, min_periods=1).sum().to_numpy()
            m = (e >= 2) & vc & _strong_close(f, True)
            side[m] = 1
            stop[m] = _stop(np.zeros(n), atr, c, max(mult, 1.0))[m]
        else:
            raise KeyError(name)
        mask = m
    elif group == "level_sweep":
        key = {"swp_pwh": ("pwh", -1), "swp_pwl": ("pwl", 1), "swp_pmh": ("pmh", -1),
               "swp_pml": ("pml", 1), "swp_pdh": ("pdh", -1), "swp_pdl": ("pdl", 1),
               "swp_ath": ("ath", -1)}.get(name)
        if key is None:
            raise KeyError(name)
        lvl_name, sgn = key
        lvl = f[lvl_name].to_numpy(float)
        m = (f[f"sweep_{lvl_name}"].to_numpy(int) == 1) & vc
        side[m] = sgn
        if sgn < 0:
            stop[m] = _stop((h - lvl)[m] + SWEEP_BUFFER_ATR * atr[m], atr[m], c[m], mult)
        else:
            stop[m] = _stop((lvl - lo)[m] + SWEEP_BUFFER_ATR * atr[m], atr[m], c[m], mult)
        mask = m
    elif group == "poc":
        dp = f.dev_poc.to_numpy(float)
        dvah = f.dev_vah.to_numpy(float)
        dval = f.dev_val.to_numpy(float)
        pp = f.prior_poc.to_numpy(float)
        z = f.z_dev_poc.to_numpy(float)
        sv = f.sess_vwap.to_numpy(float)
        if name == "poc_reclaim_up":
            m = (f.poc_reclaim_up.to_numpy(int) == 1) & (c > sv)
            side[m] = 1
            stop[m] = _stop(np.abs(c - dp)[m] + 0.25 * atr[m], atr[m], c[m], mult)
        elif name == "poc_reclaim_dn":
            m = (f.poc_reclaim_dn.to_numpy(int) == 1) & (c < sv)
            side[m] = -1
            stop[m] = _stop(np.abs(c - dp)[m] + 0.25 * atr[m], atr[m], c[m], mult)
        elif name == "poc_magnet":
            m = (np.abs(z) >= 2.0) & np.isfinite(dp) & vc
            sgn = np.where(c - dp > 0, -1, 1).astype(np.int8)
            side[m] = sgn[m]
            stop[m] = _stop(np.abs(c - dp)[m] - 0.5 * atr[m], atr[m], c[m], mult)
        elif name in ("poc_value_break_up", "poc_value_break_dn"):
            if name.endswith("up"):
                m = (c > dvah) & (f.close.shift(1).to_numpy(float) <= f.dev_vah.shift(1).to_numpy(float)) & vc
                side[m] = 1
                stop[m] = _stop((c - dvah)[m] + 0.25 * atr[m], atr[m], c[m], mult)
            else:
                m = (c < dval) & (f.close.shift(1).to_numpy(float) >= f.dev_val.shift(1).to_numpy(float)) & vc
                side[m] = -1
                stop[m] = _stop((dval - c)[m] + 0.25 * atr[m], atr[m], c[m], mult)
        elif name == "poc_prior_reclaim_up":
            m = (f.close.shift(1).to_numpy(float) < pp) & (c > pp) & vc
            side[m] = 1
            stop[m] = _stop(np.abs(c - pp)[m] + 0.25 * atr[m], atr[m], c[m], mult)
        elif name == "poc_prior_reject_dn":
            m = (h > pp) & (c < pp) & vc
            side[m] = -1
            stop[m] = _stop((h - pp)[m] + SWEEP_BUFFER_ATR * atr[m], atr[m], c[m], mult)
        elif name == "poc_prior_reject_up":
            m = (lo < pp) & (c > pp) & vc
            side[m] = 1
            stop[m] = _stop((pp - lo)[m] + SWEEP_BUFFER_ATR * atr[m], atr[m], c[m], mult)
        elif name in ("poc_migration", "poc_migration_dn"):
            if name == "poc_migration":
                m = (f.poc_mig_up.to_numpy(int) == 1) & vc & (f.poc_delta.to_numpy(float) > 0)
                side[m] = 1
            else:
                m = (f.poc_mig_dn.to_numpy(int) == 1) & vc & (f.poc_delta.to_numpy(float) < 0)
                side[m] = -1
            stop[m] = _stop(np.zeros(n), atr, c, max(mult, 1.0))[m]
        elif name in ("poc_naked_up", "poc_naked_dn"):
            up_p, dn_p = naked if naked is not None else (np.full(n, np.nan), np.full(n, np.nan))
            if name == "poc_naked_up":
                d = (up_p - c) / atr
                m = np.isfinite(up_p) & (d > 0.1) & (d <= 1.5) & vc
                side[m] = 1
            else:
                d = (c - dn_p) / atr
                m = np.isfinite(dn_p) & (d > 0.1) & (d <= 1.5) & vc
                side[m] = -1
            stop[m] = _stop(np.zeros(n), atr, c, max(mult, 1.0))[m]
        elif name == "poc_rotate_from_lvn":
            lvn = f.dev_lvn.to_numpy(float)
            m = (lo <= lvn) & (c > lvn) & vc
            side[m] = 1
            stop[m] = _stop(np.abs(c - lvn)[m] + 0.25 * atr[m], atr[m], c[m], mult)
        else:
            raise KeyError(name)
        mask = m
    elif group == "confluence":
        dp = f.dev_poc.to_numpy(float)
        pp = f.prior_poc.to_numpy(float)
        ref = np.where(np.isfinite(pp), pp, dp)
        if name in ("x_pwh_sweep_at_poc", "x_pwl_sweep_at_poc"):
            lvl_name = "pwh" if name.endswith("at_poc") and "pwh" in name else "pwl"
            lvl = f[lvl_name].to_numpy(float)
            near = np.abs(lvl - ref) / atr <= 0.75
            m = (f[f"sweep_{lvl_name}"].to_numpy(int) == 1) & vc & near
            if lvl_name == "pwh":
                side[m] = -1
                stop[m] = _stop((h - lvl)[m] + SWEEP_BUFFER_ATR * atr[m], atr[m], c[m], mult)
            else:
                side[m] = 1
                stop[m] = _stop((lvl - lo)[m] + SWEEP_BUFFER_ATR * atr[m], atr[m], c[m], mult)
        elif name == "x_brk_pwh_out_of_value":
            m = (f.brk_pwh.to_numpy(int) == 1) & vc & (c > f.dev_vah.to_numpy(float))
            side[m] = 1
            stop[m] = _stop(np.zeros(n), atr, c, max(mult, 1.0))[m]
        elif name == "x_ath_brk_lowvol":
            m = (f.brk_ath.to_numpy(int) == 1) & (f.atr_z.to_numpy(float) < 0.5)
            side[m] = 1
            stop[m] = _stop(np.zeros(n), atr, c, max(mult, 1.0))[m]
        else:
            raise KeyError(name)
        mask = m
    else:
        raise KeyError(group)
    return mask, side, stop


# Families whose signal stays actionable after the breakout bar: the level break
# is a *state* (price is above the broken level), not a single-bar event.  With
# three concurrent positions and multi-day holds, single-bar signals mean most
# gated candidates are blocked by the position limit; persistence lets the gate
# choose the entry bar and keeps otherwise idle slots working.
CARRY_FAMILIES = {
    "brk_pwh": ("pwh", 1, "level"), "brk_pmh": ("pmh", 1, "level"),
    "brk_pwl": ("pwl", -1, "level"), "brk_pml": ("pml", -1, "level"),
    "brk_pwh_cascade": ("pwh", 1, "zero"), "brk_multi_lvl": ("pwh", 1, "zero"),
    "brk_ath": ("ath", 1, "zero"), "x_ath_brk_lowvol": ("ath", 1, "zero"),
    "x_brk_pwh_out_of_value": ("pwh", 1, "zero"),
}


def _bars_since(mask: np.ndarray) -> np.ndarray:
    """Bars since the most recent True in ``mask`` (huge value if none yet)."""
    n = len(mask)
    idx = np.flatnonzero(mask)
    out = np.full(n, 1 << 30, np.int64)
    if len(idx):
        pos = np.searchsorted(idx, np.arange(n), side="right") - 1
        ok = pos >= 0
        out[ok] = np.arange(n)[ok] - idx[pos[ok]]
    return out


def build_signal_frame(f: pd.DataFrame, specs: list[FamilySpec], naked=None, priority=None,
                       pending: int = 0, pending_step: int = 4) -> pd.DataFrame:
    """Combine families into the (signal, stop_distance, score, sleeve) frame.

    One position per symbol is enforced by the kernel, so when two families fire
    on the same bar the higher-priority family wins.  With ``pending > 0`` the
    break families additionally emit candidates on later bars (every
    ``pending_step`` bars, while price still holds the broken level), so a slot
    that frees up can enter the still-valid break instead of waiting for a new one.
    """
    out = f[["open_time_ms", "open", "high", "low", "close", "atr", "volume_rel",
             "flow4", "atr_ratio", "e200", "sess_vwap"]].copy()
    n = len(f)
    sig = np.zeros(n, np.int8)
    stp = np.full(n, np.nan)
    score = np.zeros(n)
    sleeve = np.zeros(n, np.int8)
    chosen = np.zeros(n, bool)
    fam = np.array([""] * n, dtype=object)
    by_name = {s.name: s for s in specs}
    strength = (f.volume_rel.to_numpy(float).clip(0, 10)
                + 3.0 * np.abs(f.flow4.to_numpy(float)).clip(0, 3)
                + (1.5 - f.atr_ratio.to_numpy(float)).clip(-1, 1))
    carries = []
    for name in (priority or list(by_name)):
        spec = by_name.get(name)
        if spec is None:
            continue
        mask, side, stop = family_events(f, spec, naked=naked)
        usable = mask & (~chosen) & np.isfinite(stop) & (stop > 0)
        sig[usable] = side[usable]
        stp[usable] = stop[usable]
        sleeve[usable] = GROUP_ID[spec.group]
        score[usable] = strength[usable]
        fam[usable] = name
        chosen |= usable
        if pending > 0 and name in CARRY_FAMILIES:
            carries.append((name, spec, mask, side))

    # Second pass: carried (still-valid) break candidates, lowest priority.
    if carries:
        c = f.close.to_numpy(float)
        atr = _atr(f)
        step = max(1, int(pending_step))
        for name, spec, mask, side in carries:
            lvl_name, dirn, mode = CARRY_FAMILIES[name]
            lvl = f[lvl_name].to_numpy(float)
            since = _bars_since(mask)
            recent = (since > 0) & (since <= pending) & (since % step == 0)
            hold = (c > lvl) if dirn > 0 else (c < lvl)
            usable = recent & hold & (sig == 0)
            if not usable.any():
                continue
            if mode == "level":
                gap = np.abs(c - lvl) + BREAK_BUFFER_ATR * atr
                stp_c = _stop(gap, atr, c, spec.stop_mult)
            else:
                stp_c = _stop(np.zeros(n), atr, c, max(spec.stop_mult, 1.0))
            good = usable & np.isfinite(stp_c) & (stp_c > 0)
            sig[good] = dirn
            stp[good] = stp_c[good]
            sleeve[good] = GROUP_ID[spec.group]
            score[good] = strength[good]
            fam[good] = name + "_hold"
            chosen |= good
    out["signal"] = sig
    out["stop_distance"] = stp
    out["score"] = score
    out["sleeve"] = sleeve
    out["family"] = fam
    out["symbol"] = f.symbol.iloc[0] if "symbol" in f else ""
    return out


def default_specs(group_filter=None) -> list[FamilySpec]:
    """The pre-registered family list with fixed, a-priori parameters."""
    specs = [
        # --- level breakouts (continuation) --------------------------------
        FamilySpec("brk_pwh", "level_break", "Close breaks the previous week high with volume"),
        FamilySpec("brk_pwl", "level_break", "Close breaks the previous week low with volume"),
        FamilySpec("brk_pmh", "level_break", "Close breaks the previous month high with volume"),
        FamilySpec("brk_pml", "level_break", "Close breaks the previous month low with volume"),
        FamilySpec("brk_ath", "level_break", "Close makes a new all-time high with volume"),
        FamilySpec("brk_pdh", "level_break", "Close breaks the previous day high with volume"),
        FamilySpec("brk_pdl", "level_break", "Close breaks the previous day low with volume"),
        FamilySpec("brk_pwh_cascade", "level_break", "Week high broken into the month-high band"),
        FamilySpec("brk_pwh_retest", "level_break", "Retest of the broken week high that holds",
                   params={"within": 24}),
        FamilySpec("brk_multi_lvl", "level_break", "Two or more period highs broken within 8 bars"),
        # --- sweeps (liquidity grab, mean reversion) ------------------------
        FamilySpec("swp_pwh", "level_sweep", "Week high swept and rejected"),
        FamilySpec("swp_pwl", "level_sweep", "Week low swept and reclaimed"),
        FamilySpec("swp_pmh", "level_sweep", "Month high swept and rejected"),
        FamilySpec("swp_pml", "level_sweep", "Month low swept and reclaimed"),
        FamilySpec("swp_pdh", "level_sweep", "Prior day high swept and rejected"),
        FamilySpec("swp_pdl", "level_sweep", "Prior day low swept and reclaimed"),
        FamilySpec("swp_ath", "level_sweep", "All-time high swept and rejected"),
        # --- POC perspectives ----------------------------------------------
        FamilySpec("poc_reclaim_up", "poc", "Reclaim of the developing session POC"),
        FamilySpec("poc_reclaim_dn", "poc", "Loss of the developing session POC"),
        FamilySpec("poc_magnet", "poc", "Stretched >=2 sigma from POC, rotate back to value"),
        FamilySpec("poc_value_break_up", "poc", "Acceptance above the developing value area"),
        FamilySpec("poc_value_break_dn", "poc", "Acceptance below the developing value area"),
        FamilySpec("poc_prior_reclaim_up", "poc", "Reclaim of the prior-session POC"),
        FamilySpec("poc_prior_reject_dn", "poc", "Rejection at the prior-session POC (short)"),
        FamilySpec("poc_prior_reject_up", "poc", "Rejection at the prior-session POC (long)"),
        FamilySpec("poc_migration", "poc", "POC migrating up with price above it"),
        FamilySpec("poc_migration_dn", "poc", "POC migrating down with price below it"),
        FamilySpec("poc_naked_up", "poc", "Approaching an untested prior-session POC from below"),
        FamilySpec("poc_naked_dn", "poc", "Approaching an untested prior-session POC from above"),
        FamilySpec("poc_rotate_from_lvn", "poc", "Reclaim of the developing low-volume node"),
        # --- confluence -----------------------------------------------------
        FamilySpec("x_pwh_sweep_at_poc", "confluence", "Week-high sweep coinciding with value"),
        FamilySpec("x_pwl_sweep_at_poc", "confluence", "Week-low sweep coinciding with value"),
        FamilySpec("x_brk_pwh_out_of_value", "confluence", "Week-high break outside the value area"),
        FamilySpec("x_ath_brk_lowvol", "confluence", "New ATH in a compressed volatility regime"),
    ]
    if group_filter:
        specs = [s for s in specs if s.group in group_filter]
    return specs

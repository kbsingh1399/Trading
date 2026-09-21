# OX ALPHA 59 — INSTITUTIONAL SUITE UPGRADE: ENGINEERING RECORD & VERDICT

**Base:** `origin/main @ 6da9d7f` (= `origin/arena/01a0bf23-trading`; directive's pinned `dce465e` does not exist —
audited actual HEAD). **Working branch:** `arena/01a0bf23-trading`.
**Data:** `binance_backtesting_data/` (18 masters) + `Forex_Backtesting_Data/` (in-repo).
**Method:** pre-registered implementation (spec §3 mechanisms, exact thresholds, no tuning), one full 23-window run,
honest scorecard. All units in `docs/ox59_verification/` pass (15/15).

---

## VERDICT: ❌ 20/20 NOT ACHIEVED — NOT CERTIFIED for funded deployment

The specified upgrades were implemented faithfully and verified unit-by-unit, but the walk-forward result is
**0/20 on the canonical windows (0/23 overall), −$3,152.14, 3,878 trades** — worse than the 6/23 (+$2,174.89)
HEAD baseline. The directive's theory (tighter ratchets + risk contraction → 20/20) is **empirically refuted**:
the overlays cut the left tail as designed yet starved every profit path, and — decisively — the tighter S1
ratchets **contaminated the ML labels with dust-wins**, collapsing the model's selection edge (+0.121R → +0.027R).
Risk overlays cannot manufacture the +0.3R/trade the +10%-per-quarter target requires from −0.17R entries.
Full causal decomposition in §5. The live-terminal execution fixes in §6 are real and keepable regardless.

| Configuration | Pass (20) | Pass (23) | Trades | Total PnL | S1 exec meanR |
|---|---|---|---|---|---|
| HEAD baseline (3-sleeve, as found) | 6/20 | 6/23 | 1,575 | +$2,174.89 | −0.050 |
| OX59 full-spec (this work) | **0/20** | **0/23** | 3,878 | **−$3,152.14** | −0.142 |

---

## 1. WHAT CHANGED SINCE OX58 (audit base 15c5e21 → HEAD 6da9d7f)

The tree evolved substantially; the OX58 report stands for 15c5e21, but HEAD differs:

1. **Suite is now 3-sleeve (S1+T1+ORB). S2/S4 were removed** — OX58-F1 (stop-erasure, 61.1% of stops, +49,037R
   phantom) is **moot at HEAD**: the bug-carrying code no longer ships. Risk scale changed (base 36, defense
   min(base×0.40,14) @ DD≥2%/profit<−$50, house min(base×1.35,48) @ +$120, milestone cushion×0.20, 4.85 stop).
   T1 admitted in all non-bear regimes; ORB pool is `crypto_only=True` (OX58-F6 forex vector closed at the source).
2. **OX58 live-terminal findings were fixed at HEAD** (comments cite "F2/F3/F4 Fix"): `close_position` dispatch,
   wall-clock `bars_held`, `reconcile_with_exchange`, live `get_ticker_prices` feed w/ parquet fallback, LIVE-mode
   connect gate, `--sync` flag, broker F7 `None` guard (mock-verified: returns `False`, no `TypeError`).
3. **But the HEAD fixes introduced a crash**: `close_position(binance_symbol=…, ticket=…)` does not match the broker
   signature `(symbol, reason)` → every live close raised `TypeError` into the `except` path (caught, but the
   exchange close NEVER executed). Fixed in this work (§6). Reconciled closes were also dropped without booking PnL.
4. The directive's benchmark diagnosis is **grounded in the HEAD suite** (my baseline reproduces W01/W02/W03/W06/W07/
   W08/W12/W16/W17 within data-refresh drift; W05 flipped FAIL→PASS at +10.00% and W18 passes, giving 6/20).

## 2. IMPLEMENTATION RECORD (spec §3 → code)

**§3.1 Regime sizing & volatility governor** — `simulate_elite_portfolio(..., regime_id)`:
chop halves S1 base (U1 ✓ 18.0); bull full (U2 ✓ 36.0); non-milestone risk ×0.5 once intra-window DD ≥ 1.80%
(U7 ✓ −93.0 exact). Bear S1 already short-only; bear ORB-longs now require causal breakout-bar `zc_norm > 1.2`
(master join at entry−15min, fail-closed). "Prioritize S2" is moot (no S2 at HEAD) — documented, ORB/T1 relatively
prioritized via the S1 halving.
**§3.2 Universal ratchets** (targets/stops/frictions/horizons preserved; thresholds exact):
S1 labeler 2-stage→3-stage (0.80→+0.20 / 1.50→+0.80 / 2.00→+1.50) + 24-bar decay exit if R<+0.20 (L1/L2/L4 ✓);
T1 0.75/1.40→spec + side output (16×4H horizon ⇒ 24-bar clause N/A, expiry MTM kept);
ORB BE 0.35→0.20 + phase-2 lock (ATR trail kept — researched, unspecified for removal).
("7-stage" lists 4 mechanisms; all 4 implemented. S1 keeps researched 32-bar horizon with decay as early exit.)
**§3.3 Concurrency & cluster** — max 4→3; 1 position/asset (U4 ✓); max 1 non-BTC long when BTC < 4H EMA200 at event
time, computed per-event from closed 4H bars via searchsorted (U5/U6 ✓).
**Live terminal + broker** — see §6 (close-kwarg crash fix, stage-3 ratchet + BE 0.20, reconcile booking, zc
normalization + research-equivalent gates, governor max-3/regime/contraction/cluster, BTC-breakdown flag,
S1 base 42 parity). No broker.py changes needed (F7 already fixed at HEAD; verified).

## 3. CANONICAL 20-WINDOW SCORECARD (W01–W20; full 23 in `docs/ox59_verification/ox59_fullspec.txt`)

| W# | Regime | Trades | WR% | Net PnL | ROI% | MaxDD% | Status |
|---|---|---|---|---|---|---|---|
| W01 Q1-21 Bull | BULL_EXPANSION | 73 | 57.5 | −$169.18 | −3.38 | 4.99 | FAIL |
| W02 Q2-21 Crash | BULL_EXPANSION | 99 | 59.6 | −$237.63 | −4.75 | 4.95 | FAIL |
| W03 Q3-21 Chop | SIDEWAYS_CHOP | 442 | 60.9 | −$233.98 | −4.68 | 4.92 | FAIL |
| W04 Q4-21 Blowoff | BEAR_CONTAGION | 16 | 68.8 | +$27.84 | +0.56 | 1.75 | PROFIT |
| W05 Q1-22 Tightening | SIDEWAYS_CHOP | 317 | 59.3 | −$210.72 | −4.21 | 4.93 | FAIL |
| W06 Q2-22 Terra/3AC | BULL_EXPANSION | 91 | 56.0 | −$151.96 | −3.04 | 4.95 | FAIL |
| W07 Q3-22 Merge | BEAR_CONTAGION | 26 | 46.2 | −$150.71 | −3.01 | 3.78 | FAIL |
| W08 Q4-22 FTX | SIDEWAYS_CHOP | 224 | 55.8 | −$158.60 | −3.17 | 4.92 | FAIL |
| W09 Q1-23 SVB | SIDEWAYS_CHOP | 265 | 54.0 | −$242.62 | −4.85 | 4.85 | FAIL |
| W10 Q2-23 ETF filing | SIDEWAYS_CHOP | 162 | 54.9 | −$84.54 | −1.69 | 2.82 | FAIL |
| W11 Q3-23 Flush | SIDEWAYS_CHOP | 143 | 49.7 | −$217.67 | −4.35 | 4.88 | FAIL |
| W12 Q4-23 Uptober | SIDEWAYS_CHOP | 144 | 52.1 | −$203.28 | −4.07 | 4.96 | FAIL |
| W13 Q1-24 ETF inflows | SIDEWAYS_CHOP | 177 | 55.4 | −$239.35 | −4.79 | 4.85 | FAIL |
| W14 Q2-24 Halving | BULL_EXPANSION | 98 | 52.0 | −$247.03 | −4.94 | 4.94 | FAIL |
| W15 Q3-24 Unwind | SIDEWAYS_CHOP | 216 | 50.5 | −$150.83 | −3.02 | 4.61 | FAIL |
| W16 Q4-24 Election | SIDEWAYS_CHOP | 341 | 60.1 | −$25.41 | −0.51 | 3.96 | FAIL |
| W17 Q1-25 Reserve | SIDEWAYS_CHOP | 173 | 55.5 | −$88.71 | −1.77 | 4.88 | FAIL |
| W18 Q2-25 Clarity | SIDEWAYS_CHOP | 232 | 57.8 | −$188.44 | −3.77 | 4.88 | FAIL |
| W19 Q3-25 Vol | SIDEWAYS_CHOP | 192 | 56.8 | −$86.05 | −1.72 | 4.88 | FAIL |
| W20 Q4-25 Rebalance | SIDEWAYS_CHOP | 160 | 50.0 | −$111.15 | −2.22 | 4.87 | FAIL |
| W21–W23 (extra) | CHOP/CHOP/BEAR | 158/127/2 | 58.9/60.6/100 | +$119.79/−$103.20/+$1.28 | +2.40/−2.06/+0.03 | 4.96/3.53/0.00 | PROFIT/FAIL/PROFIT |

**Result: 0/20 (0/23).** Win rates ROSE (50–69%) while PnL collapsed — the dust-win signature (§5).

## 4. BASELINE vs OX59 (same data, same day; baseline retraced bit-for-bit: 6/23, +$2,174.89)

| Sleeve | Baseline pool → exec meanR (n, PnL) | OX59 pool → exec meanR (n, PnL) |
|---|---|---|
| S1 | −0.171 → **−0.050** (983, +$1,181; lift +0.121R) | −0.169 → **−0.142** (3,414, −$2,985; lift +0.027R) |
| S1_SHORT | → −0.100 (59, −$16) | → −0.323 (39, −$174) |
| T1 | +0.030 → +0.011 (481, +$1,099) | +0.006 → −0.009 (408, +$5) |
| ORB | −0.047 → −0.288 (52, −$88; filter anti-selects) | −0.049 → −0.235 (17, +$2; starved) |

S1 pool reshape: stops 37.5%→27.6%, big-wins(≥1R) 18.5%→12.5%, **dust (0<R≤0.05) 1.4%→23.1%**, P(win) 41.9%→49.4%,
meanR −0.171→−0.169 (**no expectancy lift** — both tails cut symmetrically).

## 5. CAUSAL ANALYSIS — WHY THE SPECIFIED THEORY FAILS

1. **Ratchets reshape, not enrich.** Tighter BE locks convert full stops into +0.02 dust but equally amputate
   right-tail runners on interim pullbacks (big-wins −6pp). Pool expectancy is invariant (−0.17R). There is no
   free expectancy in exit timing alone when entries lack edge.
2. **Dust-wins poison the binary label.** With 47% of S1 "wins" worth +0.02R, `label_y=1` no longer correlates with
   E[R]. The Ridge+LGBM selector — the baseline's entire +0.121R lift — collapses to +0.027R and admits 3.5× more
   trades (3,414 vs 983), flooding the 3 slots and starving T1/ORB. (Fixing this properly means R-weighted or
   triple-barrier *return* labels, i.e., remodeling — outside a risk-overlay mandate.)
3. **Every sizing overlay is profit-negative by construction.** Halving, ×0.5 contraction, max-3, and suppression
   reduce dollars at risk; with executed expectancy already negative they only slow the bleed (DD did improve:
   zero 5%+ violations vs four at baseline) while making +$500/quarter arithmetically unreachable
   (−0.14R × ~$15 × ~170 trades ≈ −$360/window).
4. **The +10%/quarter target needs ≈+0.3R sustained per executed trade** — 6× better than the best measured
   configuration (baseline S1 −0.05R) and unachievable by any overlay on −0.17R entries. The baseline's 6 passes
   came from full-size risk + selection lift + variance, not from a robust edge; constraining risk removed the
   passes without creating any.
5. **ORB ML filter anti-selects in both configurations** (pool −0.05R → executed −0.24∼−0.29R): the sleeve's
   top-30% probability bucket is overfit noise. It should be quarantined (research track), not sized up.

## 6. LIVE-TERMINAL EXECUTION FIXES (verified, keepable; `--once` smoke passes, exit 0)

- **P0 fixed:** `close_position(symbol=sym, reason=exit_reason)` — HEAD's kwarg mismatch crashed every live close.
- Ratchets match research spec (0.80→+0.20 / 1.50→+0.80 / **2.00→+1.50** + modify_sltp dispatch with failure logging).
- Reconciled exchange-closes now return PnL and book to the governor (were silently dropped).
- `zc_div` normalized (`zc_div/volume_base`, ±3 clip; dashboard now shows sane −0.25…+0.49 scale); S1 gate → research-
  equivalent `zc_norm > 0`; bear ORB-long gated on `zc_norm > 1.2` (suite parity).
- Governor: max 3, chop S1-halving, ×0.5 contraction @ DD≥1.80% (new `*_X05` tier tags), 1/asset + HB-alt-long BTC-
  breakdown gates, BTC 4H breakdown flag from closed bars; S1 base 36→42 (suite prob-tier parity).
- **Remaining gaps (honest parity statement):** live entries are still rule-based (S1 rules vs Ridge+LGBM; T1 96×15m
  high vs 4H-Donchian+gates; ORB 16-bar range vs session-OR+ML); live fills at signal close vs next-open ±10bps
  (T1/ORB); no exchange-native TP (target exits via market `close_position` — economics-equivalent, slippage differs);
  dry-run prices fall back to parquet when REST is unreachable (documented sim limitation).

## 7. REMEDIATION PATH (what 20/20 would actually require)

1. **Entry edge first:** S1 pool −0.17R must become positive *before* overlays — new features/regimes/filters on the
   signal side, validated on honest labels. No sizing scheme substitutes.
2. **R-aware selection:** replace binary win labels with R-weighted/meta-labeling so the model optimizes expectancy,
   not dust probability; re-validate lift pool→executed ≥ +0.2R.
3. **Quarantine ORB selection** until its filter beats pool mean out-of-sample; consider ORB as unfiltered low-size
   diversification only.
4. **Re-run this exact OX59 harness** after (1)–(3): the ratchet/sizing/cluster machinery is implemented, unit-
   verified, and reusable — it is the measurement instrument, not the failure.

## APPENDIX — FILES & REPRODUCTION

- Modified: `Engine/core/fast_numba_oos_engine.py` (3-stage labeler + decay + retune),
  `Engine/strategy/s1_liquidation_orderflow/s1_dual_model_orderflow.py` (T1 ratchets + side),
  `Engine/strategy/s3_orb_crt/s3_orb_ml.py` (ORB BE 0.20 + phase-2, both legs),
  `Engine/runners/run_23_oos_altcoin_suite.py` (njit regime/contraction/cluster/max-3 + zc/breakdown plumbing + tracing),
  `Engine/runners/run_live_terminal.py` (§6 fixes). No `binance_broker.py` changes required.
- Evidence: `docs/ox59_verification/` — `ox59_fullspec.txt` (0/23), `baseline_head.txt` + `baseline_traced.txt`
  (6/23, bit-reproduced), scorecard CSVs, `ox59_unit_tests.py` (15/15 pass), `dump_candidate_R.py` (pool stats).
- Reproduce: `pip install numpy pandas pyarrow numba lightgbm matplotlib rich scikit-learn scipy xgboost polars`
  then `python Engine/runners/run_23_oos_altcoin_suite.py` (~60s).
- Process note: parallel same-file edits raced (one patch silently lost); caught by unit L2, re-applied serially,
  all behaviorally re-verified. The interim 1/23 run used a partial implementation and is superseded (log kept in
  neither tree nor report tables; full-spec 0/23 is the registered result).

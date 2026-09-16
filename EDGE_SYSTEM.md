# Building a System With Edge — Result and Accounting

*Asked: build a system with edge. Built: `Engine/strategy/t1_walkforward.py`.
Result: **it does not have edge.** It cuts T1's bleed by roughly half, and I can
prove break-even is the ceiling of this signal. Full accounting below, including
one place where I caught myself doing exactly what I keep warning about.*

---

## 1. Verdict up front

| | net R/trade | total R | positive? |
|---|---|---|---|
| Production T1, fixed geometry | **−0.0928** | −244.8 | no |
| Walk-forward selection, 7 hyperparameter settings | **−0.1088 … −0.0017**, median **−0.0432** | −147.3 … −2.6 | **0 of 7** |
| Oracle best *fixed* config, chosen with hindsight | **−0.0068** | −7.8 | no |

**No configuration in the search space is profitable, not even the one picked
knowing the future.** 0 of 18 fixed configurations have positive net over
2020-09 → 2026-09; the smallest day-clustered bootstrap P(net≤0) anywhere in the
space is 0.5575.

Walk-forward selection is a genuine improvement — 6 of 7 settings beat
production, median −0.0432 vs −0.0928, a 53% reduction — but it lands on
break-even at best and does not cross it.

---

## 2. The economics are not negotiable

```
gross      +0.116439 R/trade
friction    0.199042 R/trade
net        -0.082603 R/trade
```

41.0 bps round trip is **externally sourced**, not a placeholder: Shynkevich
(2026), *Journal of Futures Markets* 46(5) 904–930, via `.agents/AGENTS.md:130`
and `trading_knowledge_base.md:827` — taker fee ≥8 bps + entry slippage 10 bps +
stop slippage 15 bps. **I did not lower it.** Lowering a cost assumption until
the backtest turns green is the specific failure mode this project has been
correcting for six phases.

So the only lever is gross R per trade, and it must rise from +0.1164 to ≥
+0.1990 — **+70.9%**.

---

## 3. What I built, and why that search space

`T1_AUDIT.md` established the edge is **entirely the right tail**: the +2.2R
target row contributes +0.3293 R and removing it makes the sleeve gross
−0.2433 R; clipping winners at +1.0R turns gross +0.1164 into −0.0801.

The 32-hypothesis battery varied target (C1–C4) and horizon (C8–C10) **one at a
time** and found nothing. That was the gap: a 3.0R target under a 16-bar horizon
times out before it is reached — target-hit fell 16.6% → 12.5%. **They have to
move together.** Side is in the space because longs gross +0.1631 R against
shorts +0.0870 R while 61% of trades are shorts.

So: **target ∈ {2.2, 3.0, 4.0} × horizon ∈ {16, 24, 32} × side ∈ {both, long}
= 18 cells.** Every cell is motivated by the right-tail finding. None was found
by searching.

Selection is **walk-forward**: at each rebalance, pick the configuration with
the best mean net R/trade over the trailing window, using only trades strictly
before the rebalance date, then apply it forward. Nothing is ever chosen with
knowledge of the period it is scored on. The 2020-09 → 2021-04 stretch that no
window set ever touched is consumed as warm-up rather than peeked at.

---

## 4. The walk-forward picks

| rebalance | picked | trailing net | n_trail | n_oos | oos net |
|---|---|---|---|---|---|
| 2021-11-01 | T3.0/H24/long | +0.2214 | 153 | 41 | +0.0365 |
| 2022-05-01 | T4.0/H24/long | +0.0542 | 97 | 50 | −0.1994 |
| 2022-11-01 | T4.0/H32/both | −0.0173 | 575 | 231 | +0.0237 |
| 2023-05-01 | T4.0/H16/long | +0.0597 | 164 | 63 | +0.2899 |
| 2023-11-01 | T4.0/H16/long | +0.2138 | 177 | 190 | −0.0467 |
| 2024-05-01 | T4.0/H32/both | +0.0616 | 442 | 249 | +0.0170 |
| 2024-11-01 | T3.0/H24/both | −0.0393 | 483 | 270 | +0.2081 |
| 2025-05-01 | T4.0/H32/both | +0.1207 | 519 | 259 | −0.0527 |
| 2025-11-01 | T4.0/H32/long | +0.0905 | 291 | 55 | −0.5227 |
| 2026-05-01 | T4.0/H24/long | −0.0755 | 248 | 81 | −0.3336 |

The selector consistently moves to **wider targets (3.0–4.0R)** and **longer
horizons (24–32 bars)**, and to **long-only** in 6 of 10 windows. That is the
right-tail hypothesis confirming itself out of sample, and it is why gross
R/trade rises from +0.1152 to +0.2086.

**But the last 136 trades average −0.41 R.** Both 2026 windows lost heavily.
A system whose most recent year is that negative is not deployable regardless of
its full-sample mean.

---

## 5. I caught myself selecting on the hyperparameters

My first report of this system said net **−0.0017 R/trade, essentially
break-even.** That number is real but it is the **maximum of 7 hyperparameter
settings**, and quoting it as the expected result is precisely the selection
bias I have spent this project warning against.

| trailing | rebalance | n | gross | **net** | total R |
|---|---|---|---|---|---|
| 9m | 3m | 1,916 | +0.1305 | −0.0765 | −146.6 |
| 9m | 6m | 1,889 | +0.1639 | −0.0432 | −81.6 |
| 12m | 3m | 1,608 | +0.1819 | −0.0313 | −50.3 |
| **12m** | **6m** | **1,489** | **+0.2086** | **−0.0017** | **−2.6** |
| 18m | 3m | 1,473 | +0.1723 | −0.0366 | −54.0 |
| 18m | 6m | 1,526 | +0.1566 | −0.0623 | −95.0 |
| 18m | 12m | 1,354 | +0.1200 | −0.1088 | −147.3 |

**Honest estimate: median −0.0432 R/trade. Zero of seven settings positive.**
The module ships 12m/6m as the default because it is a round, defensible
cadence — **not** because it is the best.

---

## 6. The abstain rule is falsified

Three rebalances picked configurations whose *trailing* net was already negative
(−0.0173, −0.0393, −0.0755). I pre-declared the obvious defensive rule — if the
best available configuration lost money over the trailing year, take no trades —
which is a penalty branch only and therefore consistent with the standing
constraint that governors never lower a threshold.

**It makes things worse.**

| variant | n | gross | net | total R | P(net≤0) |
|---|---|---|---|---|---|
| walk-forward, always trade | 1,489 | +0.2086 | **−0.0017** | −2.6 | 0.5000 |
| walk-forward + abstain | 907 | +0.1889 | **−0.0411** | −37.3 | 0.7133 |

The three abstained windows returned **+0.0237, +0.2081, −0.3336** — two of
three were positive. **Trailing net R does not predict forward net R.** The rule
removed two good windows and one bad one. It is not shipped.

*Disclosure: I added this rule after seeing that 3 of 10 windows had negative
trailing net, so the decision to test it was informed by the output. It uses
only trailing data, so the evaluation is still walk-forward, and it failed
anyway.*

---

## 7. The ceiling, proved

All 18 fixed configurations over the full period, best first:

| config | n | gross | net | P(net≤0) | 2025 | 2026 |
|---|---|---|---|---|---|---|
| T4.0/H32/long | 1,148 | **+0.2071** | −0.0068 | 0.5575 | +0.044 | −0.410 |
| T4.0/H24/long | 1,148 | +0.2056 | −0.0084 | 0.5607 | +0.044 | −0.410 |
| T4.0/H16/long | 1,148 | +0.2023 | −0.0117 | 0.5958 | +0.033 | −0.410 |
| T3.0/H24/long | 1,148 | +0.2003 | −0.0136 | 0.6232 | +0.032 | −0.344 |
| … 12 more … | | | −0.014 … −0.080 | 0.63 … 1.00 | | |
| T2.2/H16/both (**production**) | 2,972 | +0.1164 | −0.0826 | 0.9985 | −0.080 | −0.248 |

**Maximum achievable gross in this space is +0.2071 R against 0.2139 R of
friction. Short by 0.0068 R — about 1.4 bps.**

That is the whole story. The signal is real, it is robust, and it is worth
slightly less than it costs to trade.

---

## 8. What would actually be required

1. **1.4 bps of execution.** The gap is smaller than the model's own buffer —
   41 bps is modelled against a 33 bps literature floor. But claiming that
   buffer is an execution claim, not a research result, and it needs live fill
   data to support. I will not assert it from a backtest.
2. **A stronger signal.** +0.2071 R is what a 4h Donchian break with this gate
   stack is worth. Getting to +0.25 R needs information this dataset does not
   contain — which is what the L2 microstructure work was for, and which is
   paused.
3. **Not this.** Thirty-two paper-derived hypotheses, Williams %R four ways,
   VPIN, funding-Z, regime governors in every form, the entire S1 15m ML sleeve,
   and now 18 exit geometries under walk-forward selection. Every one is
   falsified or break-even at best.

---

## 9. Verification

The sandbox was re-cloned a third time this turn, destroying the 4h cache, the
extracted corpus, `scratch/build_cache_multi_tf.py` and
`scratch/test_friction_parity.py`. The cache builder was **reconstructed from
its surviving consumers** (`t1_breakout.py`, `execution_costs.py`,
`build_t1_experiments.py`) and is documented line by line in
`scratch/build_cache_multi_tf.py`. It is **bit-exact**:

```
$ python3 scratch/build_cache_multi_tf.py
  18 symbols, 217,200 4h bars;  BTCUSDT 13,200 bars

$ load_t1_breakout_trades()          audited      reconstructed
  trades                             2,972        2,972
  gross                              +0.116439    +0.116439
  friction                            0.199042     0.199042
  net                                -0.082603    -0.082603
  stressed share                      22.07%       22.07%
  shorts / longs                      1824 / 1148  1824 / 1148
  LONG  gross +0.1631 t=+4.579        matches
  SHORT gross +0.0870 t=+3.293        matches

$ python3 scratch/build_t1_experiments.py
  4,051 gate-passing bars, 2,972 emitted; max |delta r_gain| = 0.000e+00

$ Engine/strategy/t1_walkforward.py, driven by its own select()/rebalance_dates()
  12m/6m -> net -0.0017 R/trade, n=1489   (reproduces scratch/ walk-forward exactly)
  all 7 settings reproduce the table in section 5
```

Code paths executed: `Engine/strategy/t1_breakout.py:load_t1_breakout_trades`,
`Engine/execution_costs.py:build_stress_series`,
`scratch/build_t1_experiments.py:label_path`,
`Engine/strategy/t1_walkforward.py:select` and `:rebalance_dates`.

`scratch/test_friction_parity.py` was **lost in the reset and is not restored** —
the 48-assertion friction-parity suite did not run this turn. That is an open
gap, not a pass.

---

## 10. Bottom line

**No system with edge was built, and I can now show why none could have been
from this signal.** What exists is a real, reproducible, walk-forward
improvement that halves the bleed — median −0.0432 vs −0.0928 R/trade — and a
proof that the ceiling is break-even.

We will not deploy a lie to live capital. This is not deployable, and the
reason is now measured rather than assumed.

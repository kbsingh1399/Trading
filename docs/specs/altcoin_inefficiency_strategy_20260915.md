# Altcoin order-flow continuation: a falsifiable strategy design

Date: 2026-09-15. Status: RESEARCH CANDIDATE, NOT A VALIDATED PROFITABLE STRATEGY.

This design preserves the earlier Binance USDT-M scope: BTC is a macro input only; ETH, XRP, SOL, BNB, DOGE, ADA, TRX, LINK, AVAX, SUI, NEAR, DOT, LTC, BCH, APT, OP and ARB are eligible after listing and indicator warm-up. Capital is $5,000, planned initial risk is $50 including transaction friction, and at most two positions can be open. No daily profit or minimum daily trade requirement is imposed. Losing days and days without trades are expected possibilities.

## What might constitute the inefficiency

Hypothesis H1: after a range breakout, sustained aggressive trading in the breakout direction, followed by a shallow successful retest, identifies *remaining* price pressure over the next 6–72 hours. Gradual execution of large orders is a possible economic explanation, not an observed trader identity. We cannot infer institutional sponsorship, trapped traders, iceberg orders or forced liquidations merely from a candle or positive delta.

The alternative hypothesis is that the move has already incorporated the information, so chasing it earns zero or negative returns after costs. A trend indicator is a context variable, not evidence that the alternative has been rejected.

The edge test is whether flow-confirmed breakouts outperform otherwise comparable breakouts **after** fees, slippage, funding and portfolio constraints. Compare within asset and similar prior volatility/trend conditions. Report the extra contribution of the flow and retest conditions; reject the complexity if they add no reliable value.

## Exact starting rules — frozen hypotheses, not optimized thresholds

All measurements below use completed 15-minute candles. Four-hour bars, where used, must be fully closed before joining onto the 15-minute series. Do not use the partial four-hour candle.

1. **Universe and observations.** Require 4,000 prior 15-minute observations and uninterrupted current data for both the asset and BTC. No observations or trades before the actual listing. BTC is explicitly rejected by the order constructor. Do not use retrospective imputation/quarantine flags as live gates. If a required empirical input is unavailable, no signal is produced.
2. **Altcoin trend.** Long: completed four-hour close > EMA50 > EMA200, and EMA50 > its value six completed four-hour candles earlier. Short: reverse the inequalities. Require at least 1,000 completed four-hour warm-up candles; instruments without that history wait. EMAs are initialized from available past data, never backfilled.
3. **BTC regime.** Veto longs when completed BTC four-hour close < EMA200 and EMA50 is falling over six completed four-hour candles. Veto shorts for the mirror condition. Veto both directions when BTC ATR14/close exceeds its prior 20-day rolling mean by more than three prior-window standard deviations. This is an exogenous veto, never a BTC position.
4. **Breakout.** At candle b close, a long setup requires close[b] > max(high[b-96:b]); a short requires close[b] < min(low[b-96:b]). The breakout level excludes candle b. Require quote volume[b] >= 1.5 times the median quote volume of the preceding 96 candles. Store the breakout level and ATR14[b].
5. **Persistent flow.** Define F[j] = sum(future_cvd_15m[j-3:j+1]) / sum(volume_base[j-3:j+1]). Require F[b] >= 0.10 for longs or <= -0.10 for shorts, and the same inequality at the later retest close. This is normalized aggressive **trade** imbalance, not limit-order-book OFI. Four-bar spot delta must have the same sign where empirical spot coverage is verified; missing spot data means no eligible setup under this version, not a synthesized confirmation.
6. **Retest.** Consider only b+1 through b+4. Long: low[j] touches the zone [level-0.25*ATR[b], level+0.25*ATR[b]], close[j] > level and close[j] > open[j]. A prior close below level-0.5*ATR[b] invalidates the setup. Short: mirror around the breakout level. Use the first qualifying retest; otherwise expire the setup. Never use candles after j to decide whether j qualified.
7. **Entry.** Submit at retest candle j close; fill at j+1 open with adverse 10bps slippage. Invalidate a long if that open is at/below the stop or more than 0.5*ATR[j] above close[j]; short mirrors this. One entry per setup and a 16-bar cooldown after exit. A session with no eligible setup remains flat.
8. **Initial stop.** Long stop reference = min(low[b:j+1])-0.25*ATR[j]. Short = max(high[b:j+1])+0.25*ATR[j]. At the actual entry open, compute risk using the known stop and all friction; reject nonpositive or invalid geometry. Never size using eventual maximum adverse excursion.
9. **Feasibility filter.** The friction-inclusive net4R target must require a favorable move no larger than three completed four-hour ATR14 units. This volatility filter checks whether the proposed target is implausibly distant; it does **not** estimate the probability of hitting it. Candidate thresholds must be tested only in training data.
10. **Ranking and capacity.** If simultaneous candidates exceed the two available slots, rank by abs(F[j]), then prior quote volume, then alphabetical symbol as a deterministic tie-break. No same-asset duplicate position. Reject orders if gross exposure would exceed 3x current liquidation equity or if total planned stop losses would breach the remaining drawdown budget. Never shrink the fixed $50 risk to disguise losses; reject the order instead.

## Exits and costs

The literal transaction-cost model is 8bps entry fee + 10bps entry slippage + 8bps exit fee + 15bps exit slippage = 41bps of entry-reference notional. Use adverse actual fills and actual-fill fee notionals in a separate sensitivity run, without also deducting the same slippage as cash. Report these conventions separately. Apply funding using verified settlement times and rates while exposed; a forward-filled rate is not a charge on every 15-minute candle. Missing exact funding events prevents a claim of fully realistic validation.

Let P be the raw next-open entry reference, D the absolute distance to the raw initial stop, q the coin quantity, c=0.0041, and B a disclosed dollar reserve for possible funding cost. The literal-model sizing rule is:

    q = (50-B) / (D+c*P), where 0 <= B < 50.
    net_PnL = q*side*(raw_exit-P) - c*q*P - realized_funding.
    achieved_net_R = net_PnL / 50.

B is a planning reserve, not a funding guarantee. Use a causal adverse funding estimate from completed settlements over the maximum holding period. If events are unavailable, do not silently assume zero actual funding; label the run transaction-cost-only. Funding spikes, gaps, exchange filters and forced liquidations can produce losses exceeding $50.

Profit management is measured in **net dollars**, not gross distance multiples:

- Initial take-profit has net +4R (+$200) under the declared funding reserve and cost model. Recalculate the required reference price for accrued funding; any new order level applies only on the next bar. If unreachable for a short at a positive price, reject the setup.
- Once a completed close marks at least +1 net R, propose a stop that locks +0.2 net R after costs; activate it on the next bar. At +2 net R, propose a +1 net R lock. Do not claim the lock is guaranteed across price gaps.
- At +3 net R, allow the target to expand to +6 net R and trail behind completed EMA21 minus 0.5 ATR for a long (plus for a short), retaining the previous tighter stop. Stop and target amendments both take effect next bar; an already hit standing target fills first.
- Exit next open if 24 completed holding bars pass without any completed close reaching +0.2 net R. Precommit a maximum holding duration of 72 hours. Close at the quarter boundary under the declared evaluation convention.
- If both active stop and target lie inside one 15-minute candle, use stop-first unless independently verified finer data resolve the sequence. An opening gap through the stop fills at the adverse opening price, plus slippage.

**Cost example, before funding.** For a 1% initial stop, $50 friction-inclusive risk buys $3,546.10 of reference notional. A gross target four stop distances away is only 2.546 net R. A true net4R target requires a 6.05% favorable price move. On a flat-price round trip, the transaction loss is $14.54. This is why small intraday moves cannot be assumed tradable under the contract.

## Daily operating rules

Check candidates every completed 15-minute bar. Maintain mark-to-market liquidation equity including estimated closing costs and accrued funding, even when no trades close that day. The UTC daily loss guard triggers at a $100 decline from beginning-of-day liquidation equity; it cancels pending entries and exits at the next executable price. Halt the portfolio for review at 4% decline from its running equity peak, leaving a nominal buffer to the earlier strict 5% evaluation hurdle. These are trigger levels, not guaranteed caps during gaps or outages.

No martingale, averaging down, added leverage after losses, or trading to meet an income quota. Display closed PnL, open PnL, full MTM PnL and transaction costs separately. Daily profit must include unrealized losses; holding a loser overnight does not turn a losing day into a profitable one.

## Evidence and validation required before calling this an edge

1. Verify master and footprint provenance, actual spot coverage and funding event coverage. A price-bin footprint does not contain quote updates, queue position, cancellations or executable bid/ask depth. Do not simulate maker fills or one-second alpha from 15-minute data.
2. Test accounting, short/long symmetry, BTC rejection, next-open entry, future-data mutation, delayed ratchets, gaps, stop/target ambiguity, funding ordering, capacity and ledger reconciliation.
3. Freeze all rules before evaluation. Fit any permitted selection on prior data only, with training outcomes resolved before the quarter-start minus 72h purge boundary. No parameters indexed by quarter.
4. Respect the earlier sequential protocol: W01 first, stop at a failure, leave later windows unscored. Any failure-guided revision makes that reused quarter development evidence. Preserve every tested version and do not call repeated selection pristine OOS.
5. Report per-quarter ROI, full MTM drawdown, win rate, trade count, PF, planned and achieved R. Retain the earlier thresholds of >=10% ROI, <5% DD, >=40% win rate, >=15 trades, >=1.4 PF and a planned >=4R runner. No passing result is claimed here.
6. Add daily metrics: percentage of profitable/flat/losing UTC days, mean and median daily MTM return, worst day, longest losing-day streak, exposure, turnover and fee burden. Use day-block bootstrap uncertainty, not independent-trade assumptions. Check whether positive net expectancy and the incremental order-flow benefit survive resampling and 1.5x/2x transaction-cost stresses.
7. Paper trade the frozen strategy on data observed after this design. Require at least 90 calendar days and 100 completed trades, whichever takes longer, and a positive lower 95% block-bootstrap bound on mean net daily return. This is a proposed promotion gate, not a proof or guarantee of future profits. These periods cannot substitute for real execution checks.

The candidate should be rejected if costs consume the effect, results depend on one asset/period, or the flow filter adds no value over the matched breakout baseline. Insufficient evidence is not permission to trade.

## Graphify evidence and external research

The existing graph contains 51,832 nodes and 51,174 edges. A documented NetworkX BFS fallback was used because the graphify CLI is unavailable. The saved traversal is in `scratch/inefficiency_design_20260915/graph_query.json`; no graph rebuild or semantic extraction was performed (0 extraction API tokens; host reasoning token cost unavailable).

The graph contains headings for cumulative volume delta and spot divergence (`docs/specs/INSTITUTIONAL_QUANT_KNOWLEDGE_PACK.md`, graph source_location `L161`), footprint analytics (`L173`), and funding/order-flow research (`docs/specs/SSRN_RESEARCH_MASTER_PLAN.md`, `L116`). Their EXTRACTED containment edges are structural relationships, not profitability evidence. No historical result or success claim from those documents is adopted.

Independent primary-source checks:

- [Explainable Patterns in Cryptocurrency Microstructure](https://arxiv.org/abs/2602.00776), Bieganowski and Ślepaczuk, 2026: its abstract reports work on one-second Binance Futures book and trade data and distinguishes maker/taker behavior during a flash crash. It motivates investigating flow and adverse selection, but does not validate this 15-minute strategy or its specific thresholds.
- [Market impact as anticipation of the order flow imbalance](https://arxiv.org/abs/1402.1288), Jaisson, 2014: presents a theoretical link between order-flow dynamics and market impact. Persistent order flow alone does not establish exploitable future returns; its assumptions include a martingale price.
- [Crypto carry](https://www.bis.org/publications/working-paper-1087-crypto-carry), BIS Working Paper 1087: studies spot/futures carry and limits to arbitrage, including margin/liquidation risks. A spot/perpetual funding strategy is a separate hypothesis needing two-leg execution and funding-event data. It is not included in this trend-only candidate and is not risk-free daily income.
- [Commodity Trading Systems Sold on the Internet](https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/fraudadv_tradingsystem.html), CFTC: trading-system profit guarantees are not credible.

No empirical win rate, daily profit, Sharpe ratio, quarter verdict or deployable profitability claim has been established by this design document. The accompanying executable check validates arithmetic only.

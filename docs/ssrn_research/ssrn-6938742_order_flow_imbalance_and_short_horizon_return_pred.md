# Order-Flow Imbalance and Short-Horizon Return Predictability in

- **Source File**: `ssrn-6938742.pdf`
- **Total Pages**: 7
- **SSRN ID**: `ssrn-6938742`

---


### Page 1

Order-Flow Imbalance and Short-Horizon Return Predictability in
Cryptocurrency Markets
A Review of the Evidence and a Reproducible Evaluation Framework
Rem Vafin
June 2026
Abstract
Order-flow imbalance, the net pressure of buyer- versus seller-initiated trading, is one of the most
robust drivers of short-horizon price movement in market microstructure theory and equity
evidence. This article consolidates that literature and translates it to cryptocurrency markets, where
the aggressor side of each trade is reported rather than estimated and where tick-level data are freely
public. We review the theoretical foundations and the empirical record on order-flow imbalance,
define the principal measures precisely, describe the public data environment, and set out a
transparent, reproducible framework for evaluating whether order flow predicts returns, as distinct
from the largely mechanical relation by which trades move price within the same interval. The
framework specifies out-of-sample evaluation, a realistic transaction-cost model, and explicit
control for data-snooping. This is a review and design article; it does not report new empirical
estimates. Its contribution is a consolidated account of what is known and a rigorous, open-data
plan for testing it.
Keywords: market microstructure; order-flow imbalance; cryptocurrency; return predictability;
high-frequency data; reproducibility.
JEL classification: G12; G14; G15; C58.
Vafin  ·  Order-Flow Imbalance in Crypto Markets: Review & Framework  ·  1


### Page 2

1.  Introduction
Market microstructure theory holds that prices respond to order flow, the net pressure of buyer- versus
seller-initiated trading. Under asymmetric information, marketable orders convey information and force
liquidity providers to revise quotes, so signed order flow becomes the primary channel through which
information enters prices at short horizons (Kyle, 1985; Glosten and Milgrom, 1985; Hasbrouck, 1991). The
most widely cited empirical sharpening of this idea is due to Cont, Kukanov, and Stoikov (2014), who show
that over short intervals the change in price is an approximately linear function of order-flow imbalance
(OFI), with a slope that falls as market depth rises.
Cryptocurrency markets are a natural setting in which to revisit these results. Two features distinguish them
from the equity markets in which OFI was first studied. First, the aggressor side of each trade is observed:
exchange feeds report directly whether the buyer or the seller was the liquidity taker, so signed order flow is
recovered exactly, without the trade-classification error that attends heuristics such as Lee and Ready
(1991). Second, the data are public and granular, years of tick-level trades are freely downloadable, which
makes complete, end-to-end reproduction feasible in a way that proprietary equity and futures datasets
rarely allow.
This article has three aims. It reviews the theory and the empirical record linking order-flow imbalance to
returns, in both equities and crypto. It  defines the principal order-flow measures and the public data
environment precisely enough to be implemented. And it specifies a reproducible framework for the
central open question: does order flow observed up to a given moment predict subsequent returns, and is any
such predictability robust and economically meaningful? The distinction between this predictive question
and the largely mechanical contemporaneous relation, that trades move price within the same interval, is the
conceptual spine of the article. The two are routinely conflated in practitioner writing; separating them is
what allows order-flow evidence to bear on the informational efficiency of these markets.
To be explicit about scope: this is a review and design article and does not present new empirical estimates.
Sections 2–4 synthesise existing theory and evidence; Section 5 defines the measures; Section 6 describes
the data; Section 7 sets out the evaluation framework; Sections 8–9 discuss and conclude.
2.  Theoretical Background
The link between order flow and price originates in models of trading under asymmetric information. Kyle
(1985) shows that an informed trader’s order flow is impounded into price linearly, defining a depth
parameter (the reciprocal of “Kyle’s lambda”) that governs the price impact of a given quantity. Glosten and
Milgrom (1985) derive the bid–ask spread as compensation that liquidity providers require for the adverse-
selection risk that some incoming orders are informed; each trade therefore shifts the market maker’s beliefs
and the quotes. Hasbrouck (1991) operationalises these ideas with a vector-autoregressive treatment of
signed trades and quote revisions, measuring the persistent price impact, the information content, of a trade.
The common thread is that signed order flow, not price pattern, is the proximate cause of short-horizon price
change, and that its impact scales inversely with available liquidity.
Vafin  ·  Order-Flow Imbalance in Crypto Markets: Review & Framework  ·  2


### Page 3

3.  Evidence on Order-Flow Imbalance
Cont, Kukanov, and Stoikov (2014) provide the benchmark empirical result. Using exchange data for a
cross-section of US equities, they document an approximately linear contemporaneous relation between
best-level order-flow imbalance and mid-price changes, with a slope inversely proportional to depth; the
relation is reported to be stable across stocks and time scales and more robust than the familiar square-root
relation between price moves and traded volume. Xu, Gould, and Howison (2018) extend OFI to multiple
levels of the limit order book and find that flow at deeper levels carries additional explanatory power. Cont,
Cucuringu, and Zhang (2023) construct an integrated, cross-asset formulation that improves on the best-
level measure and captures cross-impact between instruments.
Alongside these results, a methodological literature supplies the tools for evaluating predictive ability
honestly once many predictors and models are entertained: White (2000) and Hansen (2005) for data-
snooping-robust  inference,  Diebold  and  Mariano  (1995)  and  Clark  and  West  (2007)  for  forecast
comparison, and Campbell and Thompson (2008) for out-of-sample assessment against a historical-mean
benchmark. Table 1 summarises the principal strands of evidence.
Table 1. Selected evidence on order-flow imbalance and returns.
Study
Market / data
Measure
Principal finding
Cont, Kukanov & Stoikov (2014)
US equities (exchange TAQ)
Best-level OFI
Near-linear
contemporaneous price
impact; slope falls with
depth
Xu, Gould & Howison (2018)
US equities (limit order
book)
Multi-level OFI
Deeper-level flow adds
explanatory power over best
level
Cont, Cucuringu & Zhang (2023)
US equities
Integrated / cross-asset
OFI
Cross-impact; integrated
measure improves on best-
level OFI
Easley, López de Prado & O’Hara
(2012)
US futures
VPIN (flow toxicity)
Order-flow toxicity tracks
liquidity provision and
volatility
Silantyev (2019)
BitMEX XBTUSD perpetual
Trade-flow imbalance vs
aggregate OFI
TFI explains
contemporaneous price
changes better than
aggregate OFI
Recent crypto order-flow study
(2026)
Cross-section of
cryptocurrencies
International order flow
Conditioning on order flow
improves out-of-sample
return forecasts
Recent crypto LOB study (2026)
Binance perpetuals (BTC,
ETH, +)
Engineered book/trade
features
Stable cross-asset predictive
importance; validated under
SPA testing
Vafin  ·  Order-Flow Imbalance in Crypto Markets: Review & Framework  ·  3


### Page 4

4.  Order Flow in Cryptocurrency Markets
Applications to digital assets are more recent but converge on the relevance of order flow. Silantyev (2019),
studying the BitMEX perpetual, finds that a trade-flow imbalance (TFI) measure computed from signed
taker volume explains contemporaneous price changes better than a book-based aggregate, a result that both
motivates an emphasis on TFI and is convenient given the wide public availability of trade data. Subsequent
work reports that conditioning on order flow improves out-of-sample machine-learning forecasts of
cryptocurrency returns relative to fundamental predictors, and recent high-frequency studies on Binance
perpetual contracts document that engineered order-book and trade features carry stable predictive
importance across assets of very different capitalisation, validated with predictive-ability testing. A parallel
line of work connects order-flow toxicity (the VPIN metric of Easley, López de Prado, and O’Hara, 2012) to
Bitcoin volatility and price jumps.
Taken together, the evidence establishes a strong contemporaneous relation and suggestive predictive value,
but leaves open precisely the questions this framework targets: how much predictive content survives out-
of-sample, over which horizons, and whether it is exploitable once realistic costs and the multiplicity of
tested specifications are accounted for.
5.  Measuring Order Flow
Crypto trade records include a flag indicating whether the buyer was the maker, which maps directly to an
aggressor sign: when the buyer is the maker the seller is the liquidity taker and the trade is seller-initiated (
−1); otherwise it is buyer-initiated (s = +1). Signed trade volume is s · q, with q the trade quantity.
Because the aggressor is reported rather than inferred, no Lee–Ready classification is required and the
corresponding measurement error is absent. Table 2 lists the measures used in the framework.
Table 2. Order-flow measures.
Measure
Definition
Role
TFI
Net signed taker volume in a bar: sum of s·q over trades
Primary contemporaneous and predictive
regressor
TFI_norm
(V_buy − V_sell) / (V_buy + V_sell), bounded in [−1, 1]
Scale-free imbalance; cross-asset
comparison
CVD
Running cumulative sum of signed volume
Regime and descriptive analysis
OFI
Best bid/ask size and price increments (book-based)
Robustness, where quote history is
available
6.  The Public Data Environment
Binance publishes a free market-data archive (data.binance.vision) of individual trades, aggregated
trades, and candlesticks for spot pairs, with a public REST endpoint (data-api.binance.vision) for gap-
filling; no account or API key is required. Aggregated-trade records carry the maker/taker flag needed to
sign order flow. Tick data are large, several gigabytes per asset-year, so a practical pipeline processes data
month-by-month and persists only bar-level features. Historical best-bid/ask (quote) records are available
Vafin  ·  Order-Flow Imbalance in Crypto Markets: Review & Framework  ·  4


### Page 5

only through approximately 2024, which is why a trade-based measure (TFI) is the natural primary object
and book-based OFI is reserved for a bounded robustness check. Table 3 summarises the relevant sources.
Table 3. Public data sources.
Source
Content
Access
data.binance.vision
Bulk CSV: trades, aggregated trades, candlesticks
Free, no key; bulk download
data-api.binance.vision
REST endpoints for trades, aggTrades, depth, klines
Free, no key; rate-limited
Historical bookTicker dumps
Best bid/ask quotes (through ~2024)
Free; limited recency
Second venue (e.g., Coinbase)
Public trade data for external-validity check
Free / public
7.  A Reproducible Evaluation Framework
The framework below specifies how the open questions should be tested. It is a design, not a set of results.
7.1  Separating contemporaneous from predictive content
The contemporaneous regression r_t = α + β · TFI_t + ε_t (estimated on short subsamples and
averaged, with Newey–West HAC standard errors) recovers the depth-dependent price-impact relation of
Cont et al. (2014) in crypto and is largely mechanical. The economically meaningful object is the predictive
regression of forward returns on lagged flow, r_{t→t+h} = α + Σ β_k OF_{t−k} + γ r_{t−1} + ε,
evaluated against autoregressive and historical-mean benchmarks across horizons h.
7.2  Out-of-sample protocol
Data are partitioned chronologically (estimation, validation for any tuning, and a final test window touched
only once) to preclude look-ahead. Predictive ability is judged primarily by the Campbell–Thompson out-
of-sample R², with the Clark–West statistic for nested-model comparison and the Diebold–Mariano statistic
where applicable. A bivariate vector autoregression in returns and flow, with Granger-causality tests and
impulse responses, characterises lead–lag dynamics and horizon decay.
7.3  Economic significance and costs
Any signal is mapped to a fully specified rule (position in the sign of the predicted return above a validation-
tuned threshold, flat otherwise) and evaluated net of a conservative taker fee (on the order of ten basis points
per side), a half-spread, and slippage. The reported quantities include turnover, net Sharpe ratio, and the
break-even cost at which net value reaches zero. The interpretive rule is fixed in advance: predictability
whose break-even cost lies below realistic trading costs is judged statistically real but not exploitable at
retail latency, a conclusion fully consistent with efficient-markets reasoning.
7.4  Guarding against data-snooping
Because such a study searches over assets, horizons, resolutions, and specifications, conventional p-values
overstate significance. The framework evaluates the full set of candidate models jointly with White’s
Reality Check and Hansen’s Superior Predictive Ability test and reports conclusions under family-wise
error control. Robustness analyses split by volatility regime and by bull/bear subperiod, add intraday-
Vafin  ·  Order-Flow Imbalance in Crypto Markets: Review & Framework  ·  5


### Page 6

seasonality controls, examine microstructure noise, compare TFI with book-based OFI where quotes
permit, and replicate on a second venue.
8.  Discussion
The literature reviewed here makes two things clear. The contemporaneous association between order flow
and price is strong and well established, in equities and, on the available crypto evidence, in digital assets
too. But a strong contemporaneous relation says little about market efficiency, because it is partly
definitional: trades move price as they execute. The open and economically interesting question is whether
order flow forecasts returns beyond that mechanical link, and whether such forecasts withstand realistic
costs and honest multiple-testing discipline. The crypto setting is unusually well suited to answering it
precisely because the aggressor side is observed and the data are public.
Several  caveats temper any expectation. Microstructure predictability, where it exists, tends to be
concentrated at latencies and queue positions inaccessible to ordinary participants, so statistical significance
need not imply tradability, a distinction the cost model is designed to surface. Findings are typically venue-
and period-specific; regime splits and second-venue replication bound but do not remove this concern. And
best-level measures discard information in deeper book levels, available only intermittently in free crypto
data. These are reasons to evaluate carefully, not reasons the question is uninteresting.
9.  Conclusion
Order-flow imbalance is among the most dependable short-horizon drivers of price in microstructure theory
and equity evidence, and the emerging crypto literature suggests the relationship carries over. This article
has consolidated that evidence, defined the measures and the public data environment, and set out a
transparent, reproducible framework that separates the mechanical contemporaneous relation from genuine
out-of-sample predictability and subjects the latter to realistic costs and data-snooping control. The
framework is deliberately implementable on free, public data, so that the empirical questions it poses can be
answered, by the author or by any independent reader, with full reproducibility. Executing that empirical
programme is the natural next step.
References
Campbell, J. Y., & Thompson, S. B. (2008). Predicting Excess Stock Returns Out of Sample: Can Anything Beat the
Historical Average? Review of Financial Studies, 21(4), 1509–1531.
Clark, T. E., & West, K. D. (2007). Approximately Normal Tests for Equal Predictive Accuracy in Nested Models.
Journal of Econometrics, 138(1), 291–311.
Cont, R., Cucuringu, M., & Zhang, C. (2023). Cross-Impact of Order Flow Imbalance in Equity Markets.
Quantitative Finance.
Cont, R., Kukanov, A., & Stoikov, S. (2014). The Price Impact of Order Book Events. Journal of Financial
Econometrics, 12(1), 47–88.
Diebold, F. X., & Mariano, R. S. (1995). Comparing Predictive Accuracy. Journal of Business & Economic
Statistics, 13(3), 253–263.
Vafin  ·  Order-Flow Imbalance in Crypto Markets: Review & Framework  ·  6


### Page 7

Easley, D., López de Prado, M., & O’Hara, M. (2012). Flow Toxicity and Liquidity in a High-Frequency World.
Review of Financial Studies, 25(5), 1457–1493.
Glosten, L. R., & Milgrom, P. R. (1985). Bid, Ask and Transaction Prices in a Specialist Market with
Heterogeneously Informed Traders. Journal of Financial Economics, 14(1), 71–100.
Hansen, P. R. (2005). A Test for Superior Predictive Ability. Journal of Business & Economic Statistics, 23(4), 365–
380.
Hasbrouck, J. (1991). Measuring the Information Content of Stock Trades. Journal of Finance, 46(1), 179–207.
Kyle, A. S. (1985). Continuous Auctions and Insider Trading. Econometrica, 53(6), 1315–1335.
Lee, C. M. C., & Ready, M. J. (1991). Inferring Trade Direction from Intraday Data. Journal of Finance, 46(2), 733–
746.
Silantyev, E. (2019). Order Flow Analysis of Cryptocurrency Markets. Digital Finance, 1, 191–218.
White, H. (2000). A Reality Check for Data Snooping. Econometrica, 68(5), 1097–1126.
Xu, K., Gould, M. D., & Howison, S. D. (2018). Multi-Level Order-Flow Imbalance in a Limit Order Book. Market
Microstructure and Liquidity.
Note: the two 2026 crypto studies referenced in the text are recent and are cited descriptively; full bibliographic details and all
citations should be verified against primary sources and formatted to the target outlet’s style before any submission.
Vafin  ·  Order-Flow Imbalance in Crypto Markets: Review & Framework  ·  7

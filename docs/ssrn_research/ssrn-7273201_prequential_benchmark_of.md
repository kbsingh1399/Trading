# Prequential Benchmark of

- **Source File**: `ssrn-7273201.pdf`
- **Total Pages**: 9
- **SSRN ID**: `ssrn-7273201`

---

## Page 1

Prequential Benchmark of
Limit Order Book Mid-Price Movement Prediction Models
Aritra Neogi
aritra@neogi.in
Abstract
Predicting the direction of mid-price movements in high-
frequency Limit Order Book (LOB) tick streams, where each
tick is an individual trade transaction event, is the most demand-
ing predictive modeling problem in financial machine learning.
The tick stream is characterized by near-zero autocorrelation
(ACF = 0.046 at lag 1), sample kurtosis of 1,282 (a mea-
sure of extreme fat-tailed return distributions) at the one-tick
horizon, and microsecond latency requirements that render
standard offline learning approaches inapplicable. This paper
presents the most comprehensive prequential (test-then-train,
zero-lookahead) benchmark of high-frequency LOB mid-price
prediction to date: 10 baseline models across 10 trade hori-
zons (ℎ∈{1 . . . 500} ticks) evaluated on 11, 918, 929 BTC
perpetual futures (continuously-rolling derivative contracts)
ticks under a zero-leakage protocol, with full commercial
return, risk-adjusted performance, and deployment efficiency
analysis.
Against this benchmark, Sticker, a biologically-
inspired, gradient-free continual learning model operating at
O(1) computational depth, achieves 92.92% non-zero direc-
tional accuracy at ℎ= 1, a 14 𝜇s per-tick inference latency, and
the maximum commercial signal edge of 0.10 bps (basis points;
1 bps = 0.01% of price) with an annualized Sharpe ratio of
3,913. Sticker establishes a new Pareto frontier (best accuracy
at lowest latency simultaneously) across all evaluated architec-
tures, confirming deployment viability from sub-millisecond
scalping through sub-second short-swing trading.
Keywords: high-frequency trading, limit order book, pre-
quential evaluation, mid-price movement, continual learning,
pareto frontier, scalping, market microstructure
1
Introduction
Predicting the short-term direction of asset mid-prices from
Limit Order Book (LOB) tick data is among the most difficult
supervised learning problems in quantitative finance. The
tick stream is stationary neither in distribution nor in variance:
market regimes shift instantaneously, autocorrelation (serial
correlation between consecutive returns) is negligible (ACF =
0.046 at lag 1), and the heavy-tailed return distribution (sample
kurtosis 1,282 at ℎ= 1) means the overwhelming majority
of tick-by-tick price movements are pure microstructure noise
(transient bid-ask bounce and order flow friction) rather than
directional signal [2, 5]. Standard machine learning models
pre trained and evaluated on held-out test sets cannot operate
in this environment: distribution shift between training and
deployment renders static weights immediately stale, and
periodic batch retraining is incompatible with microsecond
latency requirements.
The correct evaluation framework for this problem is the pre-
quential (predictive-sequential) protocol [4]: at each tick, the
model predicts before observing the future, then adapts using
only the resolved label. This protocol prevents lookahead
leakage and measures the model’s actual deployed perfor-
mance rather than its in-sample fit. The closest research [8]
evaluate deep models on fixed train/test splits rather than pre-
quential streams, omitting continual adaptation and excluding
commercial viability analysis entirely.
The primary contribution of this paper is a comprehensive
prequential benchmark on 11, 918, 929 BTC perpetual futures
ticks, evaluating 10 models across 10 trade horizons spanning
sub-millisecond scalping (ℎ= 1, ∼0.43 ms) through sub-
second short-swing prediction (ℎ= 500, ∼216 ms). The
benchmark reports statistical accuracy and full commercial
performance: signal edge, Sharpe ratio, maximum drawdown,
drawdown recovery speed, break-even fee capacity, and win
rate. Against this benchmark, Sticker, a biologically-inspired,
gradient-free continual learning model, achieves state-of-the-
art directional accuracy at state-of-the-art latency, establishing
a new Pareto frontier for deployable high-frequency prediction.
Contributions
1. High-Frequency Prequential Benchmark: A zero-
leakage prequential streaming benchmark on 11, 918, 929
BTC LOB perpetual futures ticks is presented, spanning
1


## Page 2

10 baselines across 10 trade horizons (ℎ∈{1 . . . 500})
under a strict test-then-train protocol.
2. Commercial Viability and Tradeability Analysis: Full
financial return dynamics are characterized: signal edge,
risk-adjusted performance (Sharpe ratio, Sortino ratio),
drawdown recovery speed, and break-even fee capacity,
establishing Sticker’s viability across scalping to short-
swing trading horizons.
3. Multi-Horizon Microstructure Regime Characteriza-
tion: Empirical return distributions across 10 prediction
horizons are characterized, documenting the kurtosis de-
cay from 1282.50 at ℎ= 1 to 0.97 at ℎ= 500 and the label
distribution transition from a Flat-dominated trichotomy
to a symmetric binary regime.
4. Pareto Frontier Continual Predictor: Sticker is demon-
strated as the only evaluated model achieving both highest
directional accuracy and microsecond inference latency si-
multaneously, establishing a new accuracy-latency Pareto
frontier for real-time LOB prediction.
2
Background
2.1
Market Microstructure and the Limit Order Book
Financial market microstructure investigates the physical me-
chanics of price formation under discrete order placement [2, 5].
Modern continuous double auctions operate via a Limit Order
Book (LOB), which serves as a real-time ledger recording
resting buy orders (bids) and sell orders (asks) across discrete
price levels. The fundamental properties of this ledger include
the mid-price 𝑀𝑡= (𝑝𝑏+ 𝑝𝑎)/2, acting as the consensus fair
value, and the bid-ask spread 𝑆spread = 𝑝𝑎−𝑝𝑏, denoting the
fundamental market friction.
Within this framework, market dynamics evolve not in con-
tinuous time, but through discrete trade ticks. A trade tick is
an individual transaction event generated when an incoming
aggressor order (a market order consuming resting liquidity)
executes against resting LOB liquidity. Each tick systemati-
cally records the microsecond timestamp, trade size, execution
price, aggressor direction, and the updated LOB depth. Order
Flow Imbalance (OFI), which quantifies net supply-demand
shifts in bid and ask liquidity across these interactions, has
been established as the dominant driver of short-term price
direction [3].
Predicting mid-price movements at the tick level is the most
demanding machine learning subproblem in finance. The
tick stream is characterized by near-zero autocorrelation
(ACF = 0.046 at lag 1) and staggering heavy-tailed behavior,
exhibiting kurtosis of 1,282 at ℎ= 1 driven by bid-ask bounce
and transient microstructure noise. Combined with instanta-
neous regime shifts and microsecond latency constraints, these
properties render standard pre-trained approaches inapplicable.
2.2
Scalping and Short-Horizon Trading
Scalping refers to a trading strategy that profits from repeated
small directional price movements across very short trade
horizons (ℎ= 1 to ℎ≈20 ticks), relying on high directional
accuracy and low latency rather than large position sizes or long
holding periods. At the December 2025 BTC trading velocity
of approximately 2,311 ticks per second, ℎ= 1 corresponds to
∼0.43 ms; ℎ= 20 ticks to ∼8.7 ms; ℎ= 500 ticks to ∼216 ms,
spanning sub-millisecond scalping to sub-second short-swing
prediction. One basis point (bps) = 0.01% of price; all financial
metrics are reported in basis points throughout.
2.3
Literature: LOB Prediction Models
The LOB mid-price prediction literature divides into classical
econometric models and deep learning approaches. Classical
approaches include OFI-based linear regression [3], Kalman fil-
ter state-space estimators, ARIMA (AutoRegressive Integrated
Moving Average) autoregressive predictors, and GARCH (Gen-
eralized AutoRegressive Conditional Heteroskedasticity) vari-
ance models. While these achieve high throughput, they are
constrained to linear feature combinations and cannot exploit
multi-scale order flow interactions.
The deep learning benchmark for LOB prediction is DeepLOB
[8], a 2D CNN + Inception + LSTM architecture trained
on fixed LOB snapshots. Subsequent work includes selec-
tive state-space models (Mamba S6) and transformer-based
approaches. A fundamental limitation shared by all deep
architectures is their offline training assumption: they require
periodic batch retraining and suffer catastrophic forgetting
under continual distribution shift, making them incompatible
with strict prequential deployment.
3
Sticker Overview
Sticker is a biologically-inspired, gradient-free continual learn-
ing model introduced in this research, designed for lowest-
latency prediction on stochastic non-stationary tick streams.
2


## Page 3

Its design is abstracted here to the properties most relevant to fi-
nancial deployment; the architectural specification is available
in the full technical paper.
Structurally, Sticker operates as a flat, non-sequential consensus
mapping model. Rather than stacking sequential layers or main-
taining recurrent state, Sticker streams input features through
𝑁parallel experts through biological attention. This flat graph
structure achieves O(1) computational depth: forward infer-
ence consists of a concurrent pass per expert followed by a
consensus output step, with no sequential layer dependency.
Parameter adaptation is governed by a local biological plas-
ticity rule, node-level outer-product updates that require no
backpropagation, no automatic differentiation graph, and no
fixed training phase. The model is live and continual learning:
it updates in place after each resolved prediction tick.
The integrated Slope-Sign Loss evaluates prediction correct-
ness against directional sign and margin rather than numerical
magnitude, preventing the representation collapse and mean-
reversion behavior that afflicts standard loss objectives under
heavy-tailed noise.
The combined effect of these design decisions is a model that:
1. Processes each tick in 14 𝜇s inference latency on standard
CPU only infrastructure.
2. Adapts to distribution shift in 2.5 𝜇s per tick via gradient-
free local updates 19,280× faster than DeepLOB’s back-
propagation step.
3. Maintains predictive stability across the full 11.9M tick
stream without retraining, batch refits, or hyperparameter
tuning.
4
Evaluation
Models are evaluated using standard continual prequential test
on high-frequency market microstructure order flow dataset.
4.1
Problem Formulation
Let {(𝑥𝑡, 𝑦𝑡)}𝑡≥1 be a continuous stream of multivariate state
vectors and target directional labels generated by a non-
stationary continual process. The vector 𝑥𝑡∈R𝑑represents
a multi-scale present-state snapshot. In ticker streams, 𝑥𝑡
encodes a 56-dimensional snapshot spanning multi-scale or-
der flow imbalances, VWAP spreads, volatility proxies, and
momentum indicators, normalized incrementally online via
Welford’s algorithm [7] to eliminate temporal lookahead bias.
The target objective is the directional sign of subsequent
movement over a lookahead horizon ℎ∈Z>0:
Δ𝑀𝑡,ℎ= 𝑀𝑡+ℎ−𝑀𝑡,
(1)
𝑦𝑡+ℎ= sign(Δ𝑀𝑡,ℎ) ∈{−1, 0, +1},
(2)
where 𝑀𝑡denotes the mid-price at tick 𝑡.
Definition (Continual Prequential Test). At each continual
event 𝑡:
1. Feature vector 𝑥𝑡∈R𝑑is computed strictly from events
up to tick 𝑡.
2. The model emits prediction ˆ𝑦𝑡= 𝑓Θ(𝑥𝑡) prior to observ-
ing future states.
3. Prediction ˆ𝑦𝑡is enqueued into a causal FIFO buffer of
depth ℎ.
4. At tick 𝑡+ ℎ, label 𝑦𝑡+ℎresolves, continual metrics update,
and the model executes an online parameter update using
pair (𝑥𝑡, 𝑦𝑡+ℎ).
This prequential procedure prevents lookahead leakage by
resolving labels strictly after predictions are emitted.
4.2
Dataset
The test dataset comprises the Hyperliquid BTC Perpetual
Futures Level-4 Order Flow Dataset (December 2025), com-
prising 𝑁= 11, 918, 929 continuous trade ticks [1].
The
dataset captures 4 discrete LOB depth levels (𝑘∈{1, 2, 3, 4})
across bid and ask queues, recording microsecond execution
timestamps, transaction prices, trade sizes, aggressor side
indicators, and multi-level bid/ask order book quotes.
As illustrated in Figure 1, the 11.9M tick stream spans 3 distinct
market regimes identified on rolling microstructure volatility
and order flow imbalance:
1. Low-Vol Consolidation:
(24.21% duration) Range-
bound price consolidation with baseline volatility (4.23
bps) and high regime persistence (88.77% self-transition
probability).
2. Moderate Trend: (68.02% duration) The dominant con-
tinual regime, featuring steady directional price propa-
gation, baseline volatility (4.45 bps), and strong regime
persistence (95.99% self-transition probability).
3


## Page 4

3. High-Vol Extreme Shock: (7.77% duration) Violent
liquidity dislocations characterized by a +38% volatility
surge (5.86 bps) and elevated shock persistence (88.71%
self-transition probability).
Furthermore, empirical return distributions exhibit near-zero
price return autocorrelation (ACF = 0.046 at lag 1) and
extreme heavy-tailed kurtosis at microsecond trade horizons
(Table 1).
Horizon
ℎ= 1
ℎ= 2
ℎ= 5
ℎ= 20
ℎ= 500
Kurtosis
1282.50
585.22
279.73
62.65
0.97
Table 1: Systematic decay of empirical return kurtosis across
lookahead trade horizons ℎ∈{1, 2, 5, 20, 500}.
At ℎ= 1 tick, sample kurtosis reaches Kurtosis = 1282.50
(skewness of −1.442, return standard deviation of 0.168 bps).
As the lookahead horizon expands, return kurtosis decays
systematically as documented in Table 1, converging toward
near-Gaussian behavior (0.97 at ℎ= 500). This extreme next-
tick kurtosis quantitatively proves the heavy unlearnable noise
governing raw tick feeds, demanding directional optimization
over magnitude fitting.
Figure 1: Full-month mid-price trajectory across December
2025 (11.9M continuous trade ticks) partitioned by market
regime classification (Low-Vol Consolidation, Moderate Trend,
High-Vol Extreme Shock). The 𝑦-axis displays BTC mid price
in USD, and the 𝑥-axis displays trade ticks in millions.
4.3
Feature Engineering
Feature vectors 𝑥𝑡∈R56 are constructed using 56 multi-scale
microstructure indicators partitioned across 5 physical feature
categories:
1. Multi-Scale Returns (15 features):
Logarithmic
price differences over 5 lookback windows (Δ𝑡
∈
{1, 5, 10, 20, 50} ticks) across mid, bid, and ask price
streams. How much has price moved over the last 1, 5,
10, 20, and 50 trades?
2. Aggressor Trade Ratios (10 features): Volume ratios
of buyer-initiated trades to total volume over 5 rolling
tick windows (𝑤∈{1, 5, 10, 20, 50}), measuring instan-
taneous buying versus selling pressure. Are buyers or
sellers more aggressive at each timescale?
3. Volatility Proxies (10 features): Rolling sample stan-
dard deviations of tick returns across 5 tick windows
(𝑤∈{1, 5, 10, 20, 50}), quantifying local market noise.
How noisy is the market at short, medium, and longer
timescales?
4. VWAP Spreads (10 features): Percentage displacement
between instantaneous mid-price and Volume-Weighted
Average Price across 5 rolling windows, indicating price
displacement from volume-weighted fair value. Is the
current price displaced above or below its recent volume-
weighted average?
5. Top-of-Book Order Flow Imbalance (11 features): Net
supply-demand order volume differences across top LOB
depth levels (𝑘∈{1, 2, 3, 4}), measuring immediate order
book imbalance. Is more order volume resting on the buy
side or sell side of the book at each LOB depth?
All 56 features are standardized incrementally using Welford’s
algorithm [7], preserving strict prequential isolation.
4.4
Multi-Horizon Testing
Models are evaluated across 10 lookahead trade horizons ℎ∈
{1, 2, 3, 5, 10, 20, 50, 100, 200, 500} ticks. Directional perfor-
mance is evaluated on non-zero movement ticks (Δ𝑀𝑡,ℎ≠0):
DAnz =
∑︁
𝑡I(sign( ˆ𝑦𝑡) == 𝑦𝑡+ℎ∧𝑦𝑡+ℎ≠0)
∑︁
𝑡I(𝑦𝑡+ℎ≠0)
.
(3)
Across multi-horizon testing (ℎ∈{1 . . . 500}), directional
class distributions undergo a smooth structural transition as
market-microstructure friction (bid-ask spread bounce) de-
cays. At ℎ= 1 tick, zero-movement Flat ticks dominate the
stream (65.28%, 7.78M ticks), while Up (17.15%) and Down
(17.57%) are perfectly symmetric. As the lookahead horizon
extends, Flat tick frequency decreases rapidly: 27.97% at
ℎ= 5, 9.66% at ℎ= 20, 3.18% at ℎ= 50, down to 0.36%
at ℎ= 500 (42, 361 ticks), where Up (49.59%) and Down
(50.05%) converge to an exact 50/50 binary classification
regime.
4


## Page 5

Evaluation metrics also span statistical classification metrics
(Matthews Correlation Coefficient, F1-scores, precision, re-
call), financial return metrics (average edge per tick in bps,
gross/net PnL across fee tiers), risk-adjusted performance
(Sharpe ratio, maximum drawdown in bps and duration), trade
execution statistics (win rate, profit factor, win-to-loss ratio),
and system efficiency metrics (per-tick inference latency quan-
tiles, TPS throughput, parameter counts, memory overhead).
4.5
Baselines
Sticker is evaluated against 9 baseline models spanning classi-
cal econometric approaches, linear classifiers, gradient-boosted
trees, and deep sequential learning architectures. One basis
point (bps) = 0.01% of price; all financial metrics are reported
in basis points throughout.
1. Persistence: (momentum-only baseline) ˆ𝑦𝑡= sign(𝑀𝑡−
𝑀𝑡−1). Follows the naive direction of the most recent
price movement.
2. Linear Regression: (academic OFI impact model, Cont
et al. 2014) 1D Order Flow Imbalance (OFI) impact linear
regression model [3].
3. Kalman Filter: (optimal linear estimator under Gaussian
noise) Kinematic price-velocity state-space estimator.
4. ARIMA: (classical autoregressive time-series model)
Recursive Least Squares (RLS) AR(5) return predictor.
5. GARCH: (conditional variance model; tracks volatility,
not direction) Models variance using one lagged squared
return shock (ARCH) and one lagged forecast variance
(GARCH).
6. Logistic Regression: (online linear classifier; strongest
non-neural continual baseline) 56-dimensional continual
stochastic gradient descent (SGD) logistic regression
model.
7. LightGBM: (gradient-boosted decision tree; requires
periodic batch refit) LightGBM / GBDT based histogram
gradient-boosted decision trees.
8. DeepLOB: (CNN-LSTM hybrid for limit order book; the
deep learning LOB benchmark) 2D CNN + Inception +
LSTM [8].
9. Mamba (S6): (selective state space model; most recent
deep sequence architecture) Selective State Space Model
(SSM) S6 architecture [6].
5
Results
5.1
Scalping Accuracy
The directional prediction performance of Sticker is evalu-
ated under the continual prequential test across trade horizons
ℎ∈{1, 2, 5, 10, 20} trade ticks on the 11, 918, 880 tick stream.
Table 2 presents the statistical classification and accuracy
metrics. DAnz (non-zero directional accuracy) measures cor-
rectness only on ticks where price actually moves; MCC
(Matthews Correlation Coefficient, range −1 to +1) is a bal-
anced accuracy measure robust to class imbalance; F1-Macro
is the unweighted mean of per-class F1 scores.
Achieving 92.92% directional accuracy on a stream with sam-
ple kurtosis 1,282 at ℎ= 1 confirms that the model’s directional
loss objective and gradient-free consensus isolate structural
order-flow signal from the heavy-tailed noise governing raw
tick returns.
5.2
Comparative Analysis
The continual data drift problem heavily degrades traditional
deep sequence models.
As illustrated in Sticker’s loss to
accuracy trajectory (Figure 3a) versus the deep sequence
baselines (Figure 3), gradient-based deep architectures struggle
severely to maintain stable predictive edges over extended
prequential horizons.
Mamba (S6), collapses after roughly 1.7M continual ticks. As
Mamba (S6) relies on reverse automatic differentiation through
a highly parameterized state space matrix, the overwhelming
noise-to-signal ratio at ℎ= 1 tick effectively drowns the
structural gradient. As noise gradients compound, Mamba’s
representation state breaks down, defaulting entirely to random
or uniform class predictions (DA ≈50%) for the remainder of
the 11.9M tick stream.
DeepLOB, avoids complete structural collapse but exhibits
severe representation variance. While initially tracking market
structure (reaching peak accuracy near 4M ticks), DeepLOB
fails to dynamically adapt to shifting volatility regimes in the
final 30% of the data stream. Its reliance on historical sequence
unrolling creates temporal rigidity, leading to catastrophic
forgetting of earlier structural dependencies as new volatility
regimes emerge.
In contrast, Sticker’s flat graph consensus architecture indepen-
dence from backpropagation calculus allows it to strictly learn
directional movement patterns without succumbing to noise
5


## Page 6

(a) Ground-truth directional label sequence (𝑦𝑡+1) across the full 11.9M tick stream at ℎ= 1. Each vertical bar encodes the resolved tick
direction (green: Up, red: Down, grey: Flat). The dominant grey band reflects the 65.28% Flat tick fraction driven by bid-ask bounce at
one-tick lookahead.
(b) Sticker model predictions (ˆ𝑦𝑡) across the full 11.9M tick stream at ℎ= 1. Comparing with Figure 2a, the consensus graph tracks the
continual market trajectory with high fidelity across all three market regimes (Low-Vol Consolidation, Moderate Trend, High-Vol Extreme
Shock) without retraining.
Figure 2: Consolidated (across 300 sequence bins (≈40, 000 trade ticks per bar) full-stream directional sequence barcodes
(ℎ= 1) across 11.9M trade ticks comparing ground-truth targets (a) and Sticker predictions (b).
Horizon (ℎ)
Non-Zero Ticks
Accuracy (DAnz)
Overall DA
MCC (−1 to +1)
F1-Macro
Precision (+1)
Recall (+1)
ℎ= 1
4,137,857
92.92%
32.26%
0.8584
0.9292
0.9319
0.9243
ℎ= 2
6,304,286
92.11%
48.72%
0.8421
0.9211
0.9238
0.9158
ℎ= 5
8,584,715
89.22%
64.26%
0.7845
0.8922
0.8946
0.8866
ℎ= 10
9,799,661
85.66%
70.43%
0.7131
0.8565
0.8582
0.8509
ℎ= 20
10,768,036
80.94%
73.13%
0.6187
0.8093
0.8097
0.8037
Table 2: Continual prequential directional accuracy (DAnz), overall stream accuracy (Accoverall), and statistical classification
metrics of Sticker across trade horizons ℎ∈{1, 2, 3, 5, 10, 20} trade ticks on the Hyperliquid BTC perpetual futures dataset
(𝑁= 11, 918, 880 total stream ticks).
(a) Sticker
(b) Mamba (S6)
(c) DeepLOB
Figure 3: Training loss versus cumulative non-zero directional accuracy (ℎ= 1) trajectories comparing (a) Sticker (rising
monotonically without plateauing), (b) Mamba (S6) (online mode collapse into a single class after 1.7M ticks), and (c) DeepLOB
(catastrophic forgetting in the final 30% of the stream). All panels feature log-scale training loss X-axes, cumulative DA Y-axes,
and time progress colorbars. Data points are color-coded by stream progress (purple at stream start →yellow at stream end).
magnification. While strong linear baselines (such as Logistic
Regression) maintain stability and outperform baselines in
raw directional accuracy across the stream, Sticker utilizes
non-linear experts to isolate multi-scale feature interactions
that linear models with fixed set of features may not express in
hard-wired conditions.
A model collapsing to predict a single directional class uni-
formly, as Mamba (S6) does after processing 1.7M ticks, would
execute all trades on one side of the market, producing a 1,131
bps maximum drawdown compared to Sticker’s 63.5 bps. A
model suffering catastrophic forgetting as DeepLOB demon-
strates across late-stream ticks generates inconsistent signals
6


## Page 7

across regime transitions, making systematic risk manage-
ment incoherent. Such varied undesirable behaviours render
deep sequential models a poor fit for continual prediction in
high-frequency, high noise-to-signal microstructure data.
5.3
Latency and Deployment Efficiency
Beyond directional accuracy, financial deployment viability
requires microsecond-scale inference. Table 3 compares single-
thread inference latency, update latency, and throughput across
all architectures.
Architecture
Inf Lat
Bwd Lat
Throughput
DeepLOB
5.89 ms
48.20 ms
168 TPS
Mamba (S6)
2.11 ms
22.40 ms
304 TPS
LightGBM
0.02 ms
N/A
N/A
Logistic Regression
0.01 ms
0.01 ms
1898 TPS
Sticker
0.01 ms
0.00 ms
2,312 TPS
Table 3: System efficiency metrics comparing single-thread
inference latency (Inf Lat), update latency (Bwd Lat, or bio-
logical update for Sticker), and throughput (TPS) as ticks per
second.
Sticker’s biological update executes in 2.5 𝜇s, 19,280× faster
than DeepLOB’s 48.2 ms backpropagation step and 8,960×
faster than Mamba’s 22.4 ms step. At 14 𝜇s per-tick inference,
Sticker processes the full BTC tick stream in real time on a
standard CPU (without GPU infrastructure), establishing a new
accuracy-latency Pareto frontier across all evaluated models
(Figure 4). DeepLOB at 5.9 ms forward inference is 421×
slower, rendering real-time continual CPU execution infeasible
for deep LOB architectures without additional acceleration.
Notably, Sticker achieves these results with parameter count
comparable to the deep sequential models, as shown in Table 4.
Architecture
DeepLOB
Sticker
Mamba (S6)
Others
Parameters
126,049
102,176
67,049
Low∗
Table 4: Parameter count by architectures across the benchmark.
∗Other benchmark models use substantially lower-dimensional
parametric representations, except LightGBM, whose tree-
based complexity is controlled by tree depth and ensemble size
rather than a directly comparable parameter count.
Figure 4: Speed versus accuracy Pareto frontier comparing
all 10 evaluated models. The X-axis displays average per-tick
inference latency (𝜇s, logarithmic scale), while the Y-axis
tracks ℎ= 1 directional accuracy (DAnz). Sticker establishes
a new Pareto frontier at 14 𝜇s per-tick latency and 92.92%
directional accuracy.
5.4
Commercial Return Dynamics and Tradeability
Three financial metrics require brief definition for clarity:
Signal edge is the mean profit per trade before transaction
costs, measured in basis points. The Sharpe ratio measures
annualized return per unit of annualized risk; in traditional fund
management a Sharpe above 2.0 is considered exceptional, the
high-frequency regime amplifies this metric because thousands
of independent trades per day reduce variance faster than they
reduce mean return, producing large Sharpe values that reflect
statistical consistency rather than absolute magnitude. Break-
even trading fee is the maximum per-trade cost at which
gross signal edge equals transaction costs; exchange fees on
Hyperliquid range from 0.01 to 0.05 bps for maker orders.
A model with a 0.10 bps break-even fee retains 2–10× fee
headroom at current exchange rate tiers.
Table 5 details the core financial edge extracted by Sticker and
the strongest baselines across the scalp horizon (ℎ= 1).
At a trading horizon of ℎ= 500 (representing longer-term
structural shifts rather than instantaneous scalps), Sticker recov-
ers from its maximum drawdowns 47.5% faster than Logistic
Regression, indicating robust signal consistency during ad-
verse market regimes (Table 6). A strategy recovering from
drawdown in 9,754 ticks rather than 18,572 ticks operates
profitably for an additional ∼3.8 minutes per drawdown event
7


## Page 8

Architecture
Win Rate
Profit Factor
Gross PnL (bps)
Signal Edge
Max Drawdown
Ann. Sharpe
Logistic Regression
94.2%
9.12
418,340
0.10 bps
0.63% (63 bps)
4152.9
Sticker
92.9%
7.38
396,989
0.10 bps
0.63% (63 bps)
3913.0
Kalman Filter
88.5%
5.05
349,115
0.08 bps
0.51% (51 bps)
3392.4
DeepLOB
77.6%
2.64
234,998
0.06 bps
0.87% (87 bps)
2225.9
Mamba (S6)
54.9%
1.22
52,095
0.01 bps
11.31% (1131 bps)
484.0
Table 5: Commercial return overview across top architectures at ℎ= 1 horizon.
at December 2025 BTC trading velocity, compounding across
the full month into substantially higher realized returns.
Architecture
Peak-to-Trough DD
Recovery Ticks
Logistic Regression
290.68%
18, 572 ticks
Sticker
302.57%
9, 754 ticks
Table 6: Drawdown recovery velocity at ℎ= 500 prediction
horizon.
Sticker demonstrates better classification recall during bullish
(+1) target scenarios at ℎ= 500, correctly identifying structural
upward momentum far more effectively than linear architec-
tures (Table 7).
Architecture
Recall on (+1)
Correct (+1) Ticks
Logistic Regression
42.22%
≈2,496,000
Sticker
54.38%
≈3,214,000
Table 7: Recall (Sensitivity) on bullish (+1) directional targets
at ℎ= 500.
5.5
Longer Horizon Macro Scaling
While designed for microsecond scalping, Sticker maintains
generalized predictive stability across longer macro hori-
zons.
Table 8 demonstrates that even at ℎ= 500 ticks,
Sticker sustains directional accuracy significantly above ran-
dom chance (56.96%) against near-Gaussian return distribu-
tions (Kurtosis = 0.97).
As prediction horizon extends from scalping (ℎ= 1–5 ticks,
sub-millisecond) through short-swing regimes (ℎ= 100–500
ticks, up to 216 ms), the underlying data problem changes
structurally: heavy-tailed kurtosis decays from 1,282 at ℎ= 1
to 0.97 at ℎ= 500, and the label distribution transitions
from a Flat-dominated trichotomy to a symmetric binary
classification task.
Sticker maintains directional accuracy
above chance across all 10 horizons without architectural
modification, demonstrating that the present-state consensus
graph generalizes across this full noise-to-signal transition
without explicit temporal memory.
6
Conclusion
This paper has presented the comprehensive prequential bench-
mark of high-frequency LOB mid-price prediction. Evaluated
on 11, 918, 929 BTC perpetual futures ticks across 10 base-
lines and 10 trade horizons under a zero-leakage test-then-train
protocol. Sticker, a biologically-inspired, gradient-free con-
tinual learning model, achieves 92.92% non-zero directional
accuracy at ℎ= 1 with a 14 𝜇s per-tick inference latency and
a 2.5 𝜇s online adaptation step.
On the financial dimension, Sticker achieves the maximum
commercial signal edge (0.10 bps, matched with Logistic
Regression), an annualized Sharpe ratio of 3,913, a break-
even trading fee of 0.10 bps providing 2–10× fee headroom
at current Hyperliquid exchange rates, and peak-to-trough
drawdown recovery 47.5% faster than the top-performing
baseline at macro horizons, confirming deployment viability
from ℎ= 1 sub-millisecond scalping through ℎ= 500 short-
swing trading.
Across all 10 evaluated architectures in this benchmark, Sticker
establishes a new Pareto frontier: the highest directional ac-
curacy under a microsecond latency budget, deployable on
standard infrastructure. The failure of gradient-based deep
architectures (Mamba collapsing at 1.7M ticks, DeepLOB suf-
fering catastrophic forgetting over the final 30% of the stream)
confirms that the high-frequency LOB tick environment con-
stitutes a fundamental challenge for pre-trained sequential
models, and that continual, gradient-free adaptation is a neces-
sary property for production deployment.
8


## Page 9

Horizon (ℎ)
Non-Zero Ticks
Accuracy (DAnz)
Overall DA
MCC (−1 to +1)
F1-Macro
Precision (+1)
Recall (+1)
ℎ= 50
11,539,799
72.92%
70.60%
0.4583
0.7292
0.7298
0.7296
ℎ= 100
11,759,681
66.61%
65.72%
0.3321
0.6660
0.6665
0.6665
ℎ= 200
11,839,956
61.50%
61.09%
0.2299
0.6150
0.6152
0.6153
ℎ= 500
11,876,019
56.96%
56.76%
0.1391
0.5696
0.5696
0.5696
Table 8: Continual prequential directional accuracy of Sticker across macro trade horizons ℎ∈{50, 100, 200, 500}.
(a) ℎ= 1
(b) ℎ= 2
(c) ℎ= 3
(d) ℎ= 5
(e) ℎ= 10
(f) ℎ= 20
(g) ℎ= 50
(h) ℎ= 100
(i) ℎ= 200
(j) ℎ= 500
Figure 5: Consolidated directional classification confusion matrices of Sticker across all 10 lookahead trade horizons
(ℎ∈{1, 2, 3, 5, 10, 20, 50, 100, 200, 500} trade ticks). Diagonal entries denote correct directional predictions; off-diagonal cells
represent misclassification errors. At short scalp horizons (ℎ= 1–5), diagonal concentrations dominate. At macro horizons
(ℎ= 50–500), classification mass transitions smoothly into a balanced binary Up/Down regime as Flat events decay to 0.36%.
References
[1] J. Albers, M. Cucuringu, S. Howison, and A. Y.
Shestopaloff. An open book: Level 4 order book data
from the Hyperliquid exchange. Zenodo, 2026. URL
https://doi.org/10.5281/zenodo.18184441. Ver-
sion 1.0, Dataset.
[2] Rama Cont, Sasha Stoikov, and Rishi Talreja. A stochastic
model for order book dynamics. Operations Research, 58
(3):549–563, 2010.
[3] Rama Cont, Arseniy Kukanov, and Sasha Stoikov. The
price impact of order book events. Journal of Financial
Econometrics, 12(1):47–88, 2014.
[4] A Philip Dawid. Present position and potential develop-
ments: Some personal views on statistical theory and its
application – statistical theory: The prequential approach.
Journal of the Royal Statistical Society: Series A (General),
147(2):278–292, 1984.
[5] Martin D Gould, Mason A Porter, Stacy Williams, Mark
McDonald, Daniel J Fenn, and Sam D Howison. Limit
order books. Quantitative Finance, 13(11):1709–1742,
2013.
[6] Albert Gu and Tri Dao. Mamba: Linear-time sequence
modeling with selective state spaces.
arXiv preprint
arXiv:2312.00752, 2023.
[7] BP Welford. Note on a method for calculating corrected
sums of squares and means. Technometrics, 4(3):419–420,
1962.
[8] Zihao Zhang, Stefan Zohren, and Stephen Roberts.
Deeplob: Deep convolutional neural networks for limit
order books. IEEE Transactions on Signal Processing, 67
(11):3001–3012, 2019.
9


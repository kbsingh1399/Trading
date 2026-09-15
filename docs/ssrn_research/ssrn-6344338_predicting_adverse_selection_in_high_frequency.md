# Predicting Adverse Selection in High-Frequency

- **Source File**: `ssrn-6344338 (1).pdf`
- **Total Pages**: 15
- **SSRN ID**: `ssrn-6344338`

---

## Page 1

Rajendran & Singaravelu  |  Predicting Adverse Selection in Cryptocurrency Markets  |  SSRN Working Paper, March 2026 
SSRN Working Paper  |  March 2026  |  © Rajendran & Singaravelu 
SSRN WORKING PAPER  |  MARCH 2026 
 
Predicting Adverse Selection in High-Frequency 
Cryptocurrency Markets Using Gradient Boosting 
 
Suresh Rajendran 
Indian Institute of Technology Guwahati  |  r.suresh@alumni.iitg.ac.in  
Divya Singaravelu 
Indian Institute of Management Lucknow  |  divya.singaravelu@iiml.org 
 
 
ABSTRACT 
We predict adverse selection in high-frequency cryptocurrency markets using gradient boosting (LightGBM) 
trained on 31,081,463 second-level observations of BTC/USDT perpetual futures on Bybit, spanning 
February 1, 2025 through February 16, 2026 (381 raw daily files). Our toxicity label (tox_A) identifies 
seconds where strong directional order flow is followed by sustained price continuation over a five-second 
horizon, constructed using adaptive rolling quantile thresholds calibrated to a one-hour lookback window — 
a regime-aware design that accommodates the substantial variation in toxicity rates observed across the 
sample, ranging from 0.081% in September 2025 to 0.795% in February 2025. The model is estimated in a 
strict walk-forward regime: the first 21 days serve as the initial training window, with 360 out-of-sample 
evaluation days beginning February 22, 2025, eliminating any forward-looking bias. 
The composite TailScore — the product of the classifier's predicted toxicity probability and its predicted 
99th-percentile absolute price move — jointly captures the likelihood and severity of an adverse selection 
event. At a 0.1% gate, the TailScore achieves monthly ROC-AUC between 0.668 and 0.921 across the full 
out-of-sample period. The central result is that flagging the top 0.1% of TailScore-ranked seconds reduces 
CVaR99 by 2.33% — a reduction 25.85 times greater than an equal-sized random gate. This efficiency ratio 
persists across all tested gate widths from 0.1% to 5.0%, decaying from 25.85x to 3.50x as the gate widens, 
consistent with the model's signal being concentrated in the extreme upper tail of the score distribution. 
Monthly evaluation confirms robustness: efficiency ranges from 15.18x to 34.88x across all 13 evaluation 
months, with no month falling below the random gating benchmark. 
An ablation study isolates the contribution of the TailScore against a pure GBM classifier and a VPIN proxy. 
The classifier alone achieves an efficiency of 2.11x and the VPIN proxy 0.30x — the latter falling below the 
random benchmark — at identical gate rates. The gap between TailScore (25.85x) and classifier alone (2.11x) 
demonstrates that the severity component is the dominant driver of CVaR reduction: predicting that a toxic 
event will occur is insufficient; predicting how large the move will be is what determines whether the gate 
concentrates on the seconds that matter most for tail risk. 
JEL Classification: G12, G14, C45, C53 
Keywords: adverse selection, market microstructure, gradient boosting, LightGBM, cryptocurrency, VPIN, 
tail risk, CVaR, market making, high-frequency trading, order flow toxicity 
 
 
 


## Page 2

Rajendran & Singaravelu  |  Predicting Adverse Selection in Cryptocurrency Markets  |  SSRN Working Paper, March 2026 
SSRN Working Paper  |  March 2026  |  © Rajendran & Singaravelu 
1.  Introduction 
Adverse selection is the central hazard of market making. When a liquidity provider posts a quote, they 
face the risk that the counterparty holds private information — that the price is about to move substantially 
against the position just filled. This cost, known as adverse selection or order flow toxicity, is not random: 
it is concentrated in specific moments when informed traders act on signals that the market maker does not 
observe. The ability to identify such moments in advance — even imperfectly — has direct value for 
inventory management, quote sizing, and tail risk control. 
The cryptocurrency perpetual futures market presents this problem in an acute form. Trading on Bybit's 
BTC/USDT perpetual contract occurs continuously, 24 hours a day, at second-level granularity, with 
participant composition that varies dramatically across time. The global toxicity rate in our sample — 
0.3049% — means that adverse selection events are rare, highly concentrated, and strongly regime-
dependent. Monthly toxicity rates in our data range from 0.081% (September 2025) to 0.795% (February 
2025 and February 2026), a tenfold variation that any fixed-threshold prediction system would fail to 
accommodate. 
This paper makes three contributions. First, we introduce a regime-aware toxicity label (tox_A) that uses 
one-hour adaptive rolling quantile thresholds to define adversely selected seconds — a design that preserves 
label consistency across the full range of observed volatility regimes. Second, we train a LightGBM 
ensemble in a strict walk-forward regime on 31,081,463 second-level observations and construct a 
composite TailScore that jointly models the probability and severity of adverse selection, rather than 
probability alone. Third, we evaluate tail risk reduction using CVaR99 efficiency — the ratio of achieved 
CVaR reduction to what a random gate of equal size would achieve — as the primary metric, providing a 
model-size-independent measure of predictive value. 
The central empirical finding is stark: the TailScore achieves a CVaR99 efficiency of 25.85x at the 0.1% 
gate, meaning it reduces tail risk 25.85 times more than random position sizing at the same intervention 
rate. This advantage persists across all gate sizes tested (0.1% to 5.0%) and across all 13 months of out-of-
sample evaluation. An ablation study demonstrates that this performance is not achievable with a pure 
classifier or a VPIN proxy: the classifier reaches only 2.11x efficiency and the VPIN proxy 0.30x — below 
the random benchmark — under identical conditions. 
The remainder of the paper is organised as follows. Section 2 reviews the related literature. Section 3 
describes the data and market setting. Section 4 defines the toxicity label. Section 5 describes the feature 
set. Section 6 presents the model architecture and walk-forward design. Section 7 reports discrimination 
results. Section 8 presents the core CVaR tail risk reduction results. Section 9 describes the ablation study. 
Section 10 analyses monthly robustness. Section 11 concludes. 
2.  Related Literature 
The theoretical foundations of adverse selection in limit order books trace to Glosten and Milgrom (1985) 
and Kyle (1985), who formalise the idea that bid-ask spreads partially compensate market makers for losses 
incurred when trading against informed counterparties. The decomposition of the effective spread into 
adverse selection and inventory components is further developed by Huang and Stoll (1997) and Lin, 
Sanger, and Booth (1995). 


## Page 3

Rajendran & Singaravelu  |  Predicting Adverse Selection in Cryptocurrency Markets  |  SSRN Working Paper, March 2026 
SSRN Working Paper  |  March 2026  |  © Rajendran & Singaravelu 
Volume-Synchronized Probability of Informed Trading (VPIN), introduced by Easley, Lopez de Prado, and 
O'Hara (2012), operationalises the PIN model of Easley et al. (1996) in a form suited to high-frequency 
data. Its predictive power has been debated: Andersen and Bondarenko (2014) find VPIN's predictive 
content is largely driven by the choice of volume clock, while Abad and Yagüe (2012) and others find 
mixed evidence across asset classes. Our empirical results confirm this: a VPIN proxy applied to 
BTC/USDT achieves a CVaR efficiency of 0.30x — below the random benchmark — suggesting that 
volume clock-based imbalance aggregation is insufficient in perpetual futures markets. 
Machine learning methods for adverse selection prediction have developed rapidly. Cao, Chen, and Gao 
(2019) apply gradient boosting to predict informed trading in equity markets. Sirignano and Cont (2019) 
train deep neural networks on limit order book data to predict short-horizon price movements. Cartea, 
Donnelly, and Jaimungal (2018) incorporate adverse selection cost estimates directly into market-making 
optimisation problems. In cryptocurrency markets, Biais et al. (2023) document Bitcoin market 
microstructure, and Dyhrberg, Foley, and Svec (2018) analyse liquidity and adverse selection in BTC/USD. 
Our contribution differs in its focus on second-level tail risk reduction via CVaR efficiency rather than 
mean price prediction. 
The use of CVaR (Conditional Value at Risk) as an evaluation criterion is motivated by its prominence in 
risk management. Rockafellar and Uryasev (2000) establish the theoretical properties of CVaR as a 
coherent risk measure. Lopez de Prado (2018) discusses machine learning applications to financial risk. 
Our efficiency metric — CVaR reduction divided by the CVaR reduction achievable by a random gate of 
equal size — provides a size-normalised, gate-rate-independent measure of model quality. 
3.  Data and Market Setting 
3.1  Data Source and Sample 
Our dataset consists of second-level BTC/USDT perpetual futures data from Bybit, covering February 1, 
2025 through February 16, 2026 — 381 raw daily files in total. The raw inputs are two sources merged at 
the second level: (i) full limit order book snapshots updated at one-second intervals, capturing up to 200 
price levels on each side, and (ii) raw trade execution records including side, size, price, and tick direction 
for every matched order. 
After merging, labelling, and dropping seconds with missing required fields, the final panel contains 
31,081,463 second-level observations. The first 21 days (February 1–21, 2025) serve as the initial training 
window; the first out-of-sample prediction is made on February 22, 2025, yielding 360 evaluation days. Of 
the 381 files, 77 days exhibit zero positive toxicity labels under the tox_A definition (Section 4) and are 
excluded from training windows, though their test-day predictions are retained for evaluation. The global 
toxicity rate is 0.3049%, corresponding to 94,765 adversely selected seconds in total. 
3.2  Market Setting 
The BTC/USDT perpetual futures contract on Bybit is a continuously traded, cash-settled instrument with 
no expiry. The minimum price increment is $0.10. The median half-spread in our sample is $0.05, reflecting 
extremely tight liquidity during normal conditions. The CVaR99 baseline — the average absolute price 
move in the worst 1% of seconds — is $88.76 per BTC (9.20 basis points), indicating that tail events 
represent a 1,775-fold amplification of the typical spread. The market operates continuously 24 hours per 


## Page 4

Rajendran & Singaravelu  |  Predicting Adverse Selection in Cryptocurrency Markets  |  SSRN Working Paper, March 2026 
SSRN Working Paper  |  March 2026  |  © Rajendran & Singaravelu 
day, 7 days per week, eliminating overnight gaps but introducing strong intraday and day-of-week variation 
in activity, toxicity rates, and volatility. 
3.3  Summary Statistics 
Statistic
Value
Unit
Total observations
31,081,463
second-level rows
Date range
Feb 1, 2025 – Feb 16, 2026
Calendar days (raw files)
381
days
Out-of-sample evaluation days
360
days
Global toxicity rate (tox_A)
0.3049%
% of seconds
Total tox_A events
94,765
seconds
Median half-spread
$0.05  (0.005 bps)
USD per BTC
CVaR99 baseline
$88.76  (9.20 bps)
USD per BTC
Min monthly toxicity rate
0.081%  (Sep 2025)
% of seconds
Max monthly toxicity rate
0.795%  (Feb 2025)
% of seconds
Table 1. Sample summary statistics. BTC/USDT perpetual futures, Bybit, February 1, 2025 – February 16, 2026. 
First 21 days (Feb 1–21, 2025) used as initial training window; 360 out-of-sample evaluation days from February 
22, 2025. 
4.  Label Construction 
4.1  Definition of Adverse Selection (tox_A) 
A second t is labelled as adversely selected (tox_A = 1) if and only if all four conditions hold: 
(i)  Price continuation: the signed price impact over the subsequent five seconds is positive — 
price moved in the direction of order flow, consistent with informed trading; 
(ii)  Large absolute move: the five-second absolute price move exceeds the rolling 80th 
percentile computed over the prior one-hour window; 
(iii)  Strong directional flow: the absolute volume imbalance exceeds its rolling 75th percentile 
over the prior one-hour window; 
(iv)  Trades present: at least one trade executed during the second (no_trade_flag = 0). 
The signed impact is signed_impact(t) = flow_direction(t) × (mid(t+5) − mid(t)), where flow_direction = 
sign(volume_imbalance). A positive signed impact means price moved with the flow — the hallmark of 
informed order flow (Kyle, 1985). 
4.2  Regime-Aware Thresholds 
Thresholds are computed using a warmup-safe rolling quantile: the expanding window quantile is used for 
the first 3,600 observations of each day, transitioning to a fixed 3,600-second (one-hour) rolling window 
thereafter. This ensures no NaN values appear at the start of each daily file, and the threshold adapts to the 


## Page 5

Rajendran & Singaravelu  |  Predicting Adverse Selection in Cryptocurrency Markets  |  SSRN Working Paper, March 2026 
SSRN Working Paper  |  March 2026  |  © Rajendran & Singaravelu 
current volatility regime rather than a fixed historical period. Without this adaptive design, a fixed absolute 
threshold would label far more events as toxic during high-volatility months (February 2025) than during 
the compressed-volatility summer of 2025, creating artificial temporal variation that would confound the 
model. 
5.  Feature Engineering 
Features are constructed from two sources: the limit order book snapshot (prefix ob_) and the trade 
execution record (prefix tr_). All features are at one-second resolution. Rolling statistics use a 30-second 
window (W = 30) unless noted. The full feature set contains 21 variables across six groups. 
Group
Feature(s)
Description
Spread state
ob_spread, ob_spread_pct, 
ob_spread_z_30, ob_thin_book_flag 
Absolute and percentage bid-ask spread; 30-second z-score of 
spread; binary flag for spread_pct exceeding 90th percentile of 
1-hour rolling distribution
Order flow 
imbalance 
ob_imbalance_l1, ob_ofi_proxy, 
ob_ofi_z_30 
Level-1 quote imbalance (bid − ask quantity, normalised to 
[−1,1]); order flow imbalance proxy (net add minus cancel, bid 
minus ask); 30-second standardised OFI
Passive 
retreat 
ob_net_passive_z_30, ob_upd_imb
30-second z-score of |add_bid − cancel_bid| + |add_ask − 
cancel_ask|; update imbalance (upd_bid − upd_ask) / (upd_bid 
+ upd_ask)
Volatility
ob_rv_30, ob_impact_pressure
30-second realised volatility from OB mid-price (sqrt of sum 
of squared 1-second log-mid returns); impact pressure 
interaction term (ob_ofi_z_30 × ob_spread_pct)
Trade flow
tr_vol_imbalance_1s, 
tr_count_imbalance_1s, 
tr_tick_imbalance_1s, 
tr_flow_mean_30s, 
tr_flow_autocorr_30s, tr_rv_30s, 
tr_volume_z_30s
1-second volume, count, and tick imbalances (each normalised 
to [−1,1]); 30-second mean and lag-1 autocorrelation of signed 
volume flow; 30-second realised volatility from trade prices; 
30-second volume z-score 
Activity
tr_log_volume, tr_log_trade_count, 
tr_no_trade_flag
log1p(volume) and log1p(trade_count); binary flag = 1 for 
seconds with zero trades
Table 2. Feature set (21 variables, 6 groups). All features at one-second resolution; W = 30 seconds for rolling 
statistics unless noted. 
 
The impact pressure variable (ob_impact_pressure) is the key interaction term: ofi_z_30 × 
spread_pct. It captures the intuition that a given level of order flow imbalance is more informative when 
the book is thin, as thin books are more easily moved by a given order size. 
6.  Model Architecture and Walk-Forward Design 
6.1  Dual-Output LightGBM Framework 
Each day's prediction is generated by two LightGBM models trained jointly on the same feature set and 
training window: (i) a binary classifier targeting tox_A, and (ii) a quantile regressor targeting the 99th 
percentile of the five-second absolute price move. The TailScore is: 


## Page 6

Rajendran & Singaravelu  |  Predicting Adverse Selection in Cryptocurrency Markets  |  SSRN Working Paper, March 2026 
SSRN Working Paper  |  March 2026  |  © Rajendran & Singaravelu 
TailScore(t)  =  p̂ (t)  ×  q̂ ₉₉(t) 
A high TailScore requires both a high predicted probability of toxicity and a high predicted price move — 
neither alone is sufficient. This joint criterion is the key structural difference from using the classifier score 
alone. 
6.2  LightGBM Hyperparameters 
Parameter
Value
Notes
Objective
binary / quantile
Classifier / Quantile regressor
Learning rate
0.05
Both models
Num leaves
64
Both models
Num boost rounds
200
Both models
Feature / Bagging fraction
0.8 / 0.8
Both models; bagging_freq = 1
scale_pos_weight
min(neg/pos, 200)
Classifier only; capped at 200×
Quantile alpha
0.99
Quantile regressor only
Metric
AUC / quantile
Classifier / Quantile regressor
Table 3. LightGBM hyperparameters. 
 
With a base toxicity rate of 0.30%, the raw positive-to-negative ratio is approximately 1:328. We apply 
scale_pos_weight = min(neg/pos, 200) per training window, capping at 200 to prevent extreme 
gradient distortion in low-toxicity windows. This adaptive capping means the weight automatically reduces 
in months where the class ratio is closer to 200:1. 
6.3  Walk-Forward Evaluation Protocol 
For each test day d, the model is trained on the 21 most recent calendar days prior to d that contain at least 
one positive tox_A event. Days with zero positive labels are excluded from training windows (77 such days) 
but remain in the test set. A minimum of 300 positive training examples is required. This protocol ensures: 
(i) no future information leaks into any prediction; (ii) the model adapts to regime changes; and (iii) results 
are reported on exactly 360 distinct out-of-sample evaluation days. 
7.  Discrimination Results 
7.1  Global Metrics 
At the 0.1% gate, the model flags 31,082 seconds, of which 1,886 are true positives and 29,196 are false 
positives. Precision is 6.07% against a base rate of 0.30%, a PR-Lift of ~20x. Recall is 1.99% — 
mechanically low by construction when gating only 0.1% of seconds, but the relevant criterion is whether 
the gated seconds are disproportionately in the worst tail (Section 8). 
Metric
Value
Gate rate
0.1% of seconds


## Page 7

Rajendran & Singaravelu  |  Predicting Adverse Selection in Cryptocurrency Markets  |  SSRN Working Paper, March 2026 
SSRN Working Paper  |  March 2026  |  © Rajendran & Singaravelu 
Total seconds gated
31,082
True positives (TP)
1,886
False positives (FP)
29,196
False negatives (FN)
92,879
Precision @ 0.1% gate
6.07%
Recall @ 0.1% gate
1.99%
F1 score
0.030
PR-Lift @ 0.1% gate
~20× (precision / base rate)
Mean daily ROC-AUC (360 days)
0.799
Std daily ROC-AUC
0.108
Min / Max daily ROC-AUC
0.412 / 0.996
Table 4. Global discrimination metrics across the full 360-day out-of-sample period. 
 
7.2  Monthly ROC-AUC and Toxicity Regime 
Figure 1 shows monthly ROC-AUC alongside monthly toxicity rate. The model achieves ROC-AUC above 
0.90 in the first three months (Feb–Apr 2025), corresponding to high-toxicity conditions. ROC-AUC 
deteriorates through summer 2025 (Jul–Sep), reaching its minimum of 0.668 in August 2025 — the month 
with the lowest toxicity rate (0.138%). It recovers to above 0.84 by November 2025 as toxicity rates rise. 
This co-movement is consistent with the difficulty of discriminating rare events in low-signal regimes: 
when toxic events are near-absent over a 21-day training window, the model has few positive examples to 
learn from. 
 
Figure 1. Walk-forward monthly ROC-AUC (left axis, blue) and monthly toxicity rate (right axis, red bars). ROC-
AUC deterioration in summer 2025 coincides with the lowest-toxicity months of the sample. 
 


## Page 8

Rajendran & Singaravelu  |  Predicting Adverse Selection in Cryptocurrency Markets  |  SSRN Working Paper, March 2026 
SSRN Working Paper  |  March 2026  |  © Rajendran & Singaravelu 
7.3  Monthly Metrics Table 
Month
ROC-
AUC
PR-AUC
PR-
Lift
Recall%
Tail-
Hit%
Tox 
Rate%
CVaR↓%
Effic×
2025-02
0.912
0.0723
15.84
1.58
1.47
0.795
1.405
15.60
2025-03
0.919
0.0602
18.27
1.83
2.43
0.626
2.448
27.20
2025-04
0.921
0.0571
17.93
1.79
2.14
0.499
2.154
23.93
2025-05
0.841
0.0232
14.58
1.46
1.56
0.284
1.574
17.49
2025-06
0.817
0.0197
18.94
1.89
1.88
0.228
1.843
20.48
2025-07
0.738
0.0094
11.25
1.12
2.15
0.156
2.623
29.15
2025-08
0.668
0.0095
13.34
1.33
2.06
0.138
2.138
23.76
2025-09
0.684
0.0059
21.02
2.10
2.09
0.081
2.211
24.57
2025-10
0.733
0.0171
9.31
0.93
2.20
0.297
2.128
23.64
2025-11
0.847
0.0339
13.95
1.40
1.40
0.374
1.367
15.18
2025-12
0.866
0.0236
21.09
2.11
2.13
0.211
2.123
23.59
2026-01
0.697
0.0117
8.22
0.82
2.66
0.182
3.139
34.88
2026-02
0.833
0.0420
8.89
0.89
2.10
0.627
2.105
23.38
Table 5. Monthly discrimination and tail risk metrics at 0.1% gate. 
 
 


## Page 9

Rajendran & Singaravelu  |  Predicting Adverse Selection in Cryptocurrency Markets  |  SSRN Working Paper, March 2026 
SSRN Working Paper  |  March 2026  |  © Rajendran & Singaravelu 
8.  Tail Risk Reduction Results 
8.1  CVaR99 Methodology 
Let S = {t : |Δmid(t)| ≥ VaR₉₉} denote the fixed tail set — the worst 1% of seconds by absolute price move, 
defined once on the full ungated distribution. The baseline is: 
CVaR₉₉ baseline = E[|Δmid(t)| | t ∈ S] = $88.76 
The efficiency ratio is CVaR↓% divided by the expected reduction from a random gate of the same size: 
Efficiency = CVaR↓%  /  (gate_rate × (1 − REDUCE_TO) × 100) 
At the 0.1% gate with REDUCE_TO = 0.10, the random benchmark is 0.090%. An efficiency of 1.0× 
means the model performs identically to random; above 1.0× it concentrates the gate on disproportionately 
extreme seconds. 
8.2  Results at All Gate Rates 
Gate%
N Gated
TP
FP
Prec%
CVaR99$
Rand 
Red%
CVaR↓%
Effic×
Net $
0.10%
31,082
1,886
29,196
6.07%
$86.69
0.090%
2.33%
25.85×
$144,753
0.20%
62,163
3,703
58,460
5.96%
$85.58
0.180%
3.58%
19.88×
$263,650
0.50%
155,408
8,690
146,718
5.59%
$83.42
0.450%
6.02%
13.38×
$555,028
1.00%
310,815
15,827
294,988
5.09%
$81.15
0.900%
8.57%
9.52×
$935,559
2.00%
621,630
27,275
594,355
4.39%
$78.49
1.800%
11.57%
6.43×
$1,486,232
5.00%
1,554,074
48,070
1,506,004
3.09%
$74.78
4.500%
15.76%
3.50×
$2,355,068
Table 6. Baseline gating results at six gate rates. CVaR99$ = CVaR99 after gating. Net $ per 1 BTC notional, 
annualised. CVaR99$ corrected to be internally consistent with CVaR↓% at all gate rates. 
 
The 25.85× efficiency at the 0.1% gate is the headline result. A random gate at 0.1% reduces CVaR99 by 
0.090%; the TailScore achieves 2.33% — 25.85 times more — gating the same number of seconds. 
Efficiency declines as the gate widens (from 25.85× at 0.1% to 3.50× at 5.0%), consistent with the model's 
signal being concentrated in the extreme upper tail of the score distribution. 
9.  Ablation Study 
9.1  Design 
The ablation compares three scoring methods under identical conditions — same data, gate sizes, fixed tail 
mask, and exact top-N selection: 
GBM TailScore: the composite score p̂ (t) × q̂ ₉₉(t). This is the proposed method. 
GBM Classifier: the calibrated binary classifier probability p̂ (t) alone, without the severity 
multiplier. Isolates the marginal contribution of the quantile regression component. 


## Page 10

Rajendran & Singaravelu  |  Predicting Adverse Selection in Cryptocurrency Markets  |  SSRN Working Paper, March 2026 
SSRN Working Paper  |  March 2026  |  © Rajendran & Singaravelu 
VPIN Proxy: a rolling 30-second mean of the absolute 1-second volume imbalance. 
Represents the best available traditional microstructure benchmark. 
 
9.2  Results 
Method
Gate%
Effic×
CVaR↓%
Saved$
FP 
Cost$
Net$
Prec%
Recall%
GBM TailScore
0.10%
25.85×
2.33%
$145,865
$1,112
$144,753
6.07%
1.99%
GBM Classifier
0.10%
2.11×
0.19%
$21,115
$566
$20,550
1.42%
0.47%
VPIN Proxy
0.10%
0.30×*
0.03%
$1,397
$501
$896
0.09%
0.03%
GBM TailScore
0.50%
13.38×
6.02%
$558,765
$3,737
$555,028
5.59%
9.17%
GBM Classifier
0.50%
2.15×
0.97%
$107,517
$2,733
$104,784
1.46%
2.39%
VPIN Proxy
0.50%
0.35×*
0.16%
$12,933
$2,504
$10,430
0.22%
0.36%
GBM TailScore
5.00%
3.50×
15.76%
$2,382,755
$27,688
$2,355,068
3.09%
50.67%
GBM Classifier
5.00%
2.19×
9.87%
$1,633,451
$26,488
$1,606,963
2.16%
35.42%
VPIN Proxy
5.00%
0.43×*
1.92%
$200,159
$25,108
$175,051
0.35%
5.74%
Table 7. Ablation study results. Recall filled for all gate rates. * VPIN efficiency < 1.0× indicates below-random 
performance. Dollar figures per 1 BTC notional, annualised. Recall at 0.50% and 5.00% computed from Prec% × 
N_gated / total_positives (94,765). 
 
Figure 2 shows the efficiency decay curves for all three methods. 
 


## Page 11

Rajendran & Singaravelu  |  Predicting Adverse Selection in Cryptocurrency Markets  |  SSRN Working Paper, March 2026 
SSRN Working Paper  |  March 2026  |  © Rajendran & Singaravelu 
Figure 2. CVaR99 efficiency (log scale) across gate rates 0.1%–5.0%. GBM TailScore decays from 25.85× to 
3.50×. GBM Classifier is roughly flat at 2.1×–2.2×. VPIN Proxy remains below the random benchmark (< 1.0×) at 
all gate rates. 
9.3  Interpretation 
Three findings are noteworthy. First, the gap between TailScore (25.85×) and classifier alone (2.11×) at the 
0.1% gate — a 12-fold difference — shows that the severity multiplier is the primary driver of tail risk 
concentration. The classifier's predicted probability identifies seconds more likely to be toxic, but not 
necessarily the seconds with the largest price moves. The quantile regressor adds the size dimension, 
preferentially gating seconds that are both likely to be toxic and predicted to involve large price moves — 
precisely the seconds that dominate the tail. 
Second, the GBM Classifier's efficiency is stable across gate rates (2.10×–2.19×), while the TailScore's 
decays sharply (25.85× to 3.50×). This is consistent with a score whose signal is concentrated at the very 
extreme top of the distribution, with diminishing edge as the gate widens. 
Third, the VPIN proxy's sub-random efficiency (0.30×–0.43×) reflects a fundamental resolution mismatch: 
rolling volume imbalance at 30-second granularity may detect periods of elevated toxicity but lacks the 
resolution to identify the specific seconds that constitute the worst tail events. 
10.  Monthly Robustness 
Figure 3 shows monthly CVaR99 reduction and efficiency at the 0.1% gate across all 13 evaluation months. 
 
Figure 3. Monthly CVaR99 reduction (bars, left) and CVaR99 efficiency (line, right) at 0.1% gate. The dashed red 
line marks the random benchmark (1.0×). All 13 months exceed the random benchmark substantially. 
 
Three features warrant discussion. First, every month exceeds the random benchmark by a substantial 
margin — minimum monthly efficiency is 15.18× (November 2025). This is a strong robustness result: 
despite wide variation in toxicity rates, volatility regimes, and discriminative power, the model's tail risk 
concentration never degrades near the baseline. 


## Page 12

Rajendran & Singaravelu  |  Predicting Adverse Selection in Cryptocurrency Markets  |  SSRN Working Paper, March 2026 
SSRN Working Paper  |  March 2026  |  © Rajendran & Singaravelu 
Second, at a fixed gate rate CVaR reduction and efficiency move in perfect lockstep — efficiency is simply 
CVaR reduction divided by the constant random-gate baseline of 0.090%. The variation of interest is 
therefore in the absolute level of CVaR reduction itself, which is driven by the magnitude of tail events in 
each month. January 2026 achieves both the highest CVaR reduction (3.14%) and the highest efficiency 
(34.88×), while November 2025 records the lowest of both (1.37%, 15.18×). When toxic events are less 
extreme in absolute price move, even a precise gate captures less CVaR reduction in dollar terms. 
Third, ROC-AUC and efficiency are partially decoupled. August 2025 has the lowest ROC-AUC (0.668) 
but an above-median efficiency (23.76×), and July 2025 has the second-lowest ROC-AUC (0.738) but the 
second-highest efficiency (29.15×). The TailScore's tail concentration ability persists even when binary 
classification of individual seconds is noisier — the severity component continues to identify extreme price 
moves independently of the classifier's discriminative accuracy. 
10.1  Worst-Month Analysis 
Criterion
Month
Net $
CVaR↓%
Effic×
ROC-AUC
Worst Net $
Sep 2025
$2,359
2.211%
24.57×
0.684
Worst Net $
Jul 2025
$2,449
2.623%
29.15×
0.738
Worst CVaR↓%
Nov 2025
$9,469
1.367%
15.18×
0.847
Worst Effic×
Nov 2025
$9,469
1.367%
15.18×
0.847
Table 8. Worst months by each criterion. Worst Net $ months (Jul/Sep) have high CVaR efficiency — their low 
dollar outcome reflects low toxicity rates, not poor tail concentration. 
11.  Conclusion 
We have demonstrated that a composite severity-weighted TailScore, derived from dual LightGBM outputs 
trained in a strict walk-forward regime, provides statistically and practically significant advance 
identification of the seconds that disproportionately drive tail risk in BTC/USDT perpetual futures markets. 
The core finding is a CVaR99 efficiency of 25.85× at the primary 0.1% gate, sustained across all 13 out-
of-sample months and all six gate rates tested. 
Three methodological contributions underpin this result. The regime-aware toxicity label (tox_A) uses 
adaptive rolling quantile thresholds to maintain label consistency across a tenfold variation in monthly 
toxicity rates. The TailScore's multiplicative structure — classifier probability times predicted tail move 
magnitude — provides a joint criterion that the classifier alone cannot match: the ablation demonstrates a 
12-fold efficiency gap between TailScore and pure classifier at the primary gate. The walk-forward protocol 
ensures all 360 evaluation days are genuinely out-of-sample. 
The result that VPIN performs below the random benchmark (0.30×) is informative for the literature. 
Volume imbalance aggregated at 30-second granularity does not identify the specific seconds that will 
produce extreme price continuations. The relevant information appears to reside in the interaction between 
order book state (spread, OFI, passive retreat) and trade flow features, not in volume clock-based 
aggregation. 


## Page 13

Rajendran & Singaravelu  |  Predicting Adverse Selection in Cryptocurrency Markets  |  SSRN Working Paper, March 2026 
SSRN Working Paper  |  March 2026  |  © Rajendran & Singaravelu 
Limitations include: single asset ; label construction choices calibrated for this market; a fixed-tail CVaR 
methodology; and no accounting for market impact of the gating itself. Future directions include multi-
horizon prediction, cross-asset signals, and investigation of whether the efficiency gap between TailScore 
and classifier widens or narrows across different volatility regimes. 
References 
Abad, D., and Yagüe, J. (2012). From PIN to VPIN: An introduction to order flow toxicity. The Spanish Review of 
Financial Economics, 10(2), 74–83. 
Andersen, T. G., and Bondarenko, O. (2014). VPIN and the flash crash. Journal of Financial Markets, 17, 1–46. 
Biais, B., Bisière, C., Bouvard, M., Casamatta, C., and Menkveld, A. J. (2023). Equilibrium Bitcoin pricing. Journal 
of Finance, 78(2), 967–1014. 
Cao, C., Chen, Y., and Gao, X. (2019). Informed trading and price discovery before corporate events. Journal of 
Financial Economics, 132(3), 627–648. 
Cartea, Á., Donnelly, R., and Jaimungal, S. (2018). Enhancing trading strategies with order book signals. Applied 
Mathematical Finance, 25(1), 1–35. 
Dyhrberg, A. H., Foley, S., and Svec, J. (2018). How investible is Bitcoin? Analyzing the liquidity and transaction 
costs of Bitcoin markets. Economics Letters, 171, 140–143. 
Easley, D., Kiefer, N. M., O'Hara, M., and Paperman, J. B. (1996). Liquidity, information, and infrequently traded 
stocks. Journal of Finance, 51(4), 1405–1436. 
Easley, D., Lopez de Prado, M. M., and O'Hara, M. (2012). Flow toxicity and liquidity in a high-frequency world. 
Review of Financial Studies, 25(5), 1457–1493. 
Glosten, L. R., and Milgrom, P. R. (1985). Bid, ask and transaction prices in a specialist market with heterogeneously 
informed traders. Journal of Financial Economics, 14(1), 71–100. 
Huang, R. D., and Stoll, H. R. (1997). The components of the bid-ask spread: A general approach. Review of Financial 
Studies, 10(4), 995–1034. 
Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., and Liu, T.-Y. (2017). LightGBM: A highly 
efficient gradient boosting decision tree. Advances in Neural Information Processing Systems (NeurIPS), 30. 
Kyle, A. S. (1985). Continuous auctions and insider trading. Econometrica, 53(6), 1315–1335. 
Lin, J.-C., Sanger, G. C., and Booth, G. G. (1995). Trade size and components of the bid-ask spread. Review of 
Financial Studies, 8(4), 1153–1183. 
Lopez de Prado, M. (2018). Advances in Financial Machine Learning. Wiley. 
Rockafellar, R. T., and Uryasev, S. (2000). Optimization of conditional value-at-risk. Journal of Risk, 2(3), 21–41. 
Sirignano, J., and Cont, R. (2019). Universal features of price formation in financial markets: Perspectives from deep 
learning. Quantitative Finance, 19(9), 1449–1459. 
 
 


## Page 14

Rajendran & Singaravelu  |  Predicting Adverse Selection in Cryptocurrency Markets  |  SSRN Working Paper, March 2026 
SSRN Working Paper  |  March 2026  |  © Rajendran & Singaravelu 
Appendix A.  Full Baseline Gating Results 
Table A1 reproduces the complete baseline output for transparency and reproducibility. 
Gate%
N Gated
TP
FP
Prec%
CVaR99$
Rand 
Red%
CVaR↓%
Effic×
Net $
0.10%
31,082
1,886
29,196
6.07%
$86.69
0.090%
2.33%
25.85×
$144,753
0.20%
62,163
3,703
58,460
5.96%
$85.58
0.180%
3.58%
19.88×
$263,650
0.50%
155,408
8,690
146,718
5.59%
$83.42
0.450%
6.02%
13.38×
$555,028
1.00%
310,815
15,827
294,988
5.09%
$81.15
0.900%
8.57%
9.52×
$935,559
2.00%
621,630
27,275
594,355
4.39%
$78.49
1.800%
11.57%
6.43×
$1,486,232
5.00%
1,554,074
48,070
1,506,004
3.09%
$74.78
4.500%
15.76%
3.50×
$2,355,068
Table A1. Full baseline gating results. CVaR99$ corrected at 1.00% ($81.15) and 2.00% ($78.49) gates for internal 
consistency with CVaR↓%. 
 
Appendix B.  Feature Importance Analysis 
Feature importances are computed across all 360 saved daily classifier models using LightGBM's mean 
normalised gain — the fraction of total information gain attributable to each feature, averaged across 
models. We report three complementary rankings: mean normalised gain (information value per split), split 
frequency (how often each feature is used), and point-biserial correlation with the tox_A label computed 
on a 3,000,000-second random sample of the labeled dataset. 
Feature 
Gain rank 
Split rank 
Corr rank 
Avg rank 
tr_rv_30s 
1 
2 
1 
1.3 
ob_rv_30 
3 
3 
2 
2.7 
ob_spread_pct 
4 
1 
7 
4.0 
tr_count_imbalance_1s 
2 
5 
9 
5.3 
tr_vol_imbalance_1s 
5 
4 
8 
5.7 
tr_log_volume 
9 
7 
4 
6.7 
tr_log_trade_count 
6 
12 
3 
7.0 
tr_volume_z_30s 
8 
8 
6 
7.3 
tr_flow_mean_30s 
7 
6 
16 
9.7 
ob_spread_z_30 
12 
9 
11 
10.7 
ob_imbalance_l1 
10 
10 
14 
11.3 


## Page 15

Rajendran & Singaravelu  |  Predicting Adverse Selection in Cryptocurrency Markets  |  SSRN Working Paper, March 2026 
SSRN Working Paper  |  March 2026  |  © Rajendran & Singaravelu 
Feature 
Gain rank 
Split rank 
Corr rank 
Avg rank 
ob_upd_imb 
13 
11 
15 
13.0 
ob_net_passive_z_30 
14 
14 
12 
13.3 
tr_tick_imbalance_1s 
17 
17 
13 
15.7 
ob_ofi_proxy 
11 
15 
21 
15.7 
tr_no_trade_flag 
21 
21 
5 
15.7 
tr_flow_autocorr_30s 
16 
13 
20 
16.3 
ob_spread 
20 
20 
10 
16.7 
ob_ofi_z_30 
15 
16 
19 
16.7 
ob_impact_pressure 
18 
18 
17 
17.7 
ob_thin_book_flag 
19 
19 
18 
18.7 
Table B1. Feature ranking across three importance measures. Gain = mean normalised LightGBM gain 
rank; Split = mean normalised split-frequency rank; Corr = point-biserial |r| rank with tox_A label. Avg 
rank = mean of the three. 
Three findings are notable. First, volatility is the dominant signal: tr_rv_30s (30-second realised volatility 
from trade prices) ranks first on both gain and label correlation, accounting for 24.0% of mean normalised 
gain across all 360 models. ob_rv_30 (realised volatility from OB mid-price) ranks second in the composite. 
Together the two volatility features account for 32.9% of total gain, consistent with adverse selection events 
being concentrated in high-volatility seconds. Second, trade-side imbalance features are collectively 
strong: tr_count_imbalance_1s ranks second on gain (19.1%), and tr_vol_imbalance_1s fifth — both 
among the top five in gain and split rankings. Third, the ob_impact_pressure interaction term ranks 
near the bottom (gain rank 18, avg rank 17.7), and its point-biserial correlation with tox_A is near zero (r 
= −0.0008). The economic motivation for this feature — that OFI is more dangerous in thin books — is 
sound, but the LightGBM models do not extract meaningful decision-boundary information from it, 
suggesting its signal is already captured by its constituent components (ob_ofi_z_30 and ob_spread_pct) 
separately. 
Regarding tr_no_trade_flag: it ranks last on both gain (21) and split (21), but fifth on label correlation (|r| 
= 0.030, negative). This apparent paradox is explained by label construction: tox_A = 0 whenever 
tr_no_trade_flag = 1 by definition, so the feature provides a deterministic boundary rather than a 
discriminative gradient. The model learns this as a near-constant exclusion rather than an informative 
feature. 
 


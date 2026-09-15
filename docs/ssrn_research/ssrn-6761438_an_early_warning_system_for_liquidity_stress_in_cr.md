# An Early Warning System for Liquidity Stress in Cryptocurrency

- **Source File**: `ssrn-6761438.pdf`
- **Total Pages**: 7
- **SSRN ID**: `ssrn-6761438`

---

## Page 1

An Early Warning System for Liquidity Stress in Cryptocurrency
Markets Using Trade Flow Analysis and Machine Learning
Goodness Kalu∗
drkalugoodness@gmail.com
WorldQuant University
New Orleans, LA, USA
Uchenna Ejike
WorldQuant University
New Orleans, LA, USA
Joseph Edet
WorldQuant University
New Orleans, LA, USA
Temitope E. Fagbuyi
WorldQuant University
New Orleans, LA, USA
Godfrey Kunde
WorldQuant University
New Orleans, LA, USA
Hannah Igboke
WorldQuant University
New Orleans, LA, USA
Abstract
Most research on liquidity crises relies on expensive institutional
data or coarse daily aggregates — reconstructing why crashes oc-
curred rather than detecting them as they unfold. We present an
early warning system for liquidity stress in Binance spot cryptocur-
rency markets using freely available high-frequency trade data,
deployable against the public Binance API with no proprietary
feeds required. Our contributions are fourfold: (1) a natively sta-
tionary microstructure feature set (OFI, RV, Kyle’s 𝜆, ILLIQ, VWAP
deviation, intensity, and TCI) derived from publicly available trade
data; (2) a purged expanding walk-forward framework preventing
temporal leakage; (3) a comparative study of five ML architectures
under a unified protocol across binary and multiclass formulations,
five seeds, and pooled/asset-specific configurations; and (4) a three-
tier external validation framework addressing the self-referentiality
of HMM-labelled pipelines through a controlled global-vs-local
HMM experiment with genuinely independent validators.
XGBoost achieves a binary weighted F1 of 0.9706 on the final
out-of-sample window (18.8M training rows) with near-zero seed
variance (range: 0.0006), substantially outperforming a persistence
baseline (F1-W 0.7891) and confirming genuine predictive skill be-
yond regime momentum. Against external reference definitions,
the framework provides 56 minutes of advance warning before the
documented FTX trigger and 108 minutes before the Terra-Luna
structural break. The global HMM is near-deterministic (2.66×10−7
maximum parameter difference across independent runs), while
locally-fitted HMMs produce stress percentages of 6.0% to 94.3%
for identical periods—demonstrating systematic miscalibration un-
der narrow training horizons. Against three independent external
validators, the global HMM achieves substantial to almost perfect
Cohen’s 𝜅agreement, while local variants collapse across multiple
folds. A cross-evaluation falsification test confirms XGBoost is not
recovering HMM label geometry: stress F1 drops from 0.988 to 0.480
when a locally-trained model is evaluated against global labels. Fi-
nally, we provide a live inference system deployable against the
public Binance API, bridging the gap between academic modelling
and real-world trading infrastructure.
∗Lead author and corresponding author. G. Kalu conceived the technical research design
and implemented the complete data pipeline, microstructure feature engineering,
experimental framework, model training, explainability analysis, external validation
framework, live inference system, and manuscript preparation.
CCS Concepts
• Computing methodologies →Machine learning; • Applied
computing →Economics.
Keywords
cryptocurrency, market microstructure, liquidity stress, machine
learning, HMM regime labelling, early warning systems, walk-
forward validation
In memory of Adanna Chisom Kalu (2000–2025).
I miss you — your big brother.
1
Introduction
The rapid growth of cryptocurrency markets since the launch of
Bitcoin in 2009 has introduced financial risks characterised by ex-
treme volatility, continuous 24-hour trading, and the absence of
traditional circuit breakers, creating a perfect storm of liquidity
vulnerabilities. The collapse of Terra-Luna in May 2022, the FTX
bankruptcy (November 2022), and the COVID-induced crash (March
2020) demonstrated that liquidity stress can materialise within min-
utes in crypto markets, wiping out positions before conventional
risk systems can respond.
Unlike equity markets, where decades of tough lessons have led
to market makers and regulatory halts providing structural buffers,
cryptocurrency markets largely operate without these stabilising
mechanisms. While regulation has improved, the relatively unfet-
tered nature of crypto exchanges makes early detection of stress
regimes operationally critical.
Most existing work analyses stress events in hindsight using
coarse daily or hourly data [5, 7], relies on expensive proprietary
order book feeds [10], or focuses on short-term price forecasting
rather than structural regime classification [17]. Studies addressing
high-frequency stress detection typically use static held-out test
sets, ignoring temporal dependencies and data leakage risks [12].
A deeper concern—which became apparent during the opera-
tional development of our pipeline—is self-referentiality. When
stress regimes are defined by an unsupervised model fitted on the
exact same data window used for classification, the resulting frame-
work risks circularity.
This paper addresses these gaps. Specifically, our contributions
are:
1


## Page 2

Goodness Kalu, Uchenna Ejike, Joseph Edet, Temitope E. Fagbuyi, Godfrey Kunde, and Hannah Igboke
(1) We construct a natively stationary microstructure feature
set from publicly available Binance trade data, encompass-
ing OFI, RV, Kyle’s 𝜆, ILLIQ, VWAP deviation, trade inten-
sity, and TCI.
(2) We design a purged expanding walk-forward validation
framework with a 30-minute embargo to strictly prevent
temporal leakage.
(3) We benchmark five ML architectures (Logistic Regression,
Random Forest, XGBoost, LSTM, CNN-GAF) across binary
and multiclass formulations to establish the optimal infer-
ence engine.
(4) We address label self-referentiality through a three-tier ex-
ternal validation framework, demonstrating the necessity of
global HMM calibration over local fitting against genuinely
independent validators—price drawdowns, documented cri-
sis timestamps, and cross-asset contagion.
To ensure reproducibility and bridge the gap to real-world trad-
ing infrastructure, the complete pipeline, trained models, and a live
API inference system are available at https://github.com/Goodie-
Goody/maic.
2
Related Work
Market microstructure theory provides the theoretical foundation
for our feature set. Roll (1984) [20], Glosten and Milgrom (1985)
[11], and Kyle (1985) [14] established the core frictions of financial
markets—transaction costs, inventory risk, and adverse selection.
Amihud (2002) [2] demonstrated that illiquidity commands a return
premium, bridging microstructure to asset pricing.
A key enabling result is Lee and Ready (1991) [16], who devel-
oped a method to classify trades as buyer- or seller-initiated from
price data alone—the exact mechanism that allows our system to
compute OFI from freely available Binance trade data without re-
quiring expensive proprietary order book feeds. Chordia et al. (2002)
[8] confirmed that signed order flow is a significant determinant of
liquidity conditions, with imbalances in either direction reducing
liquidity through market-maker inventory effects.
Brunnermeier and Pedersen (2009) [7] formalised liquidity spi-
rals: traders selling under stress push prices down, triggering mar-
gin calls and further selling in a self-reinforcing cascade. Kirilenko
et al. (2014) [13] showed this mechanism visible in basic trade data
during the 2010 Flash Crash, which erased more than $1 trillion
in market value within minutes before nearly fully recovering [? ].
The Terra-Luna collapse [6] and COVID-19 cross-asset contagion
[1] confirm these spirals operate in crypto. Our system is specifi-
cally designed to detect the earliest microstructure rumblings of
this doom loop—before it becomes self-reinforcing.
Kercheval and Zhang (2015) [12] established that ML models
predict short-term price movements from trade features. Sirignano
and Cont (2018) [21] proved that pooling data across assets out-
performs asset-specific models — directly motivating our pooled
multi-asset configuration. López de Prado (2018) [18] formalised
purged walk-forward cross-validation to prevent temporal leakage,
which inflates reported performance in naive splits. SHAP [19]
provides the regulatory-grade explainability financial risk systems
require.
Table 1: Sampling Windows and Market Context
W
Period
Context
Key Event
0
Feb–Jul 2020
COVID crash
COVID-19 (Mar 2020)
1
Nov 2020–May 2021
Bull run
May 2021 crash
2
Nov 2021–May 2022
Peak + contagion
Terra-Luna
3
Nov 2022–Apr 2023
Post-FTX recovery
FTX bankruptcy
4
Jul–Dec 2024
Post-halving
—
Every study above reconstructs a crisis retrospectively, after the
underlying data is already complete. This paper instead evaluates
the framework prospectively: it issues warnings 56–108 minutes
ahead of documented crisis onsets, measured against externally ver-
ified reference definitions rather than the model’s own retrospective
labels.
3
Data and Methodology
3.1
Data Collection
Raw trade data was collected from Binance for BTCUSDT, ETHUSDT,
and SOLUSDT across five deliberate six-month windows capturing
distinct market regimes (Table 1). Window 0 (Feb–Jul 2020) is in-
cluded in all fold training sets to provide exposure to the COVID-19
crash—the only global macro-driven stress event in the dataset. SO-
LUSDT begins November 2020 (Binance listing date) and is absent
from Window 0. Each trade record includes timestamp, price, quan-
tity, and buyer-initiated flag. Trades were aggregated to 300-second
bars (≈2.1 million observations per asset). Prior to feature engi-
neering, a three-layer quality audit verified schema consistency,
flagged duplicate trade IDs, and removed extreme price outliers;
zero-volume bars were forward-filled to ensure feature robustness.
3.2
Microstructure Feature Engineering
Seven features are computed at the 300-second aggregation fre-
quency, each grounded in market microstructure theory. OFI mea-
sures directional pressure of informed trading: OFI𝑡= (Í
buy 𝑞𝑖−
Í
sell 𝑞𝑗)/Í𝑞𝑘, bounded in [−1, 1]. RV captures model-free price
instability as the sum of squared intraday returns RV𝑡= Í𝑟2
𝑖,𝑡[3].
Kyle’s 𝜆estimates price impact via OLS of price changes on signed
order flow. ILLIQ adapts Amihud’s measure to 300s: |𝑟𝑡|/𝑉𝑡. VWAP
deviation, trade intensity (normalised count), and Trade Con-
centration Index (TCI) (Herfindahl-style concentration of trade
sizes) complete the feature set. All seven are natively stationary —
each measures a rate, ratio, or local dynamic rather than a price
level.
Only the raw price series is non-stationary. Fractional differenc-
ing [18] is applied with asset-specific minimum differencing orders:
BTCUSDT 𝑑∗= 0.3, ETHUSDT 𝑑∗= 0.4, SOLUSDT 𝑑∗= 0.2.
3.3
Regime Labelling
Stress labels are generated by a 3-state Gaussian HMM fitted per as-
set on {RV300𝑠, OFI300𝑠, ˆ𝜆300𝑠, intensity300𝑠} using the Baum-Welch
EM algorithm [4] as implemented in hmmlearn (diagonal covari-
ance, 100 EM iterations, 5 seeds, best log-likelihood retained). States
map to calm/elevated/stress by RV mean rank. Binary classification
collapses calm and elevated into non-stress.
2


## Page 3

An Early Warning System for Liquidity Stress in Cryptocurrency Markets Using Trade Flow Analysis and Machine Learning
Decoding procedure. State sequence decoding uses the Viterbi
algorithm [22] (GaussianHMM.predict()), which finds the globally
most probable state sequence given the full observation sequence.
Applied to the complete dataset, this means early-sample states are
assigned with knowledge of future observations—a form of smooth-
ing that is standard practice in retrospective regime labelling but
constitutes look-ahead relative to a real-time system. We adopt
global Viterbi deliberately: the alternative—local Viterbi restricted
to fold-available data at each boundary—produces catastrophically
miscalibrated labels (stress rates of 6.0% to 94.3% for identical assets
and periods, as demonstrated in Section 4.4). The global solution
is near-deterministic (2.66 × 10−7 maximum parameter difference
across independent runs), confirming it represents the unique con-
vergent solution at this data scale rather than a random local opti-
mum. The three-tier external validation framework in Section 3.4
provides the empirical justification for this design choice.
3.4
External Validation Design
A fundamental concern in HMM-labelled pipelines is self-referentiality.
We address this through two analyses. First, a stability proof:
comparing April 2026 backup model parameters against current
production models confirms the global HMM is near-deterministic
(ETH/SOL: 0.00 × 100; BTC: 2.66 × 10−7 maximum parameter dif-
ference). Second, a controlled experiment: local HMMs fitted
using only training-available data at each fold boundary are com-
pared against the global HMM using three genuinely independent
validators—none of which are HMM training features:
(1) Price drawdown—the HMM never observed raw price
levels
(2) Crisis timestamps—externally documented in the litera-
ture
(3) Cross-asset simultaneous stress—HMM fitted per-asset
independently, never saw joint dynamics
Agreement is quantified via Cohen’s𝜅[9], interpreted per Landis
& Koch [15]. RV, OFI, Kyle’s 𝜆, and intensity are explicitly excluded
as validators to prevent circularity.
3.5
Lead-Time Methodology
Predictive lead time is the interval between the model’s first sus-
tained signal (𝑃> 0.85 for ≥2 consecutive 300s bars) and the
reference onset. To avoid self-referentiality, lead time is measured
against two independent reference definitions in addition to HMM-
defined stress onset: (i) externally documented crisis timestamps
from the academic literature and contemporaneous news record,
and (ii) the first breach of a 5% rolling price drawdown from the
preceding six-hour peak—a price-derived measure the HMM never
observed. The continuity condition (≥2 consecutive bars) filters
spurious spikes while preserving sensitivity to structural breaks.
3.6
Experimental Design
Purged expanding walk-forward cross-validation with four folds
and a 30-minute embargo. Models trained in asset-specific and
pooled configurations across binary and multiclass formulations,
five seeds. The input matrix X consists of the seven microstructure
features plus the fractionally differenced price series (28 features
for pooled models with asset identifier, 27 for asset-specific). Five
Table 2: Production Stability—Mean ± Std, 5 Seeds, All Folds
Mode
Model
Acc.
F1-W
F1-M
F1-S
Multi.
LR
.658±.132
.634±.154
.517±.104
.546±.189
RF
.878±.084
.888±.080
.811±.115
.875±.056
XGB
.905±.067
.912±.064
.852±.094
.885±.061
LSTM
.666±.151
.661±.156
.502±.036
.582±.076
CNN-GAF
.417±.083
.415±.095
.292±.041
.198±.118
Binary
LR
.779±.070
.784±.089
.703±.065
.559±.096
RF
.945±.040
.945±.040
.920±.035
.881±.046
XGB
.946±.054
.947±.052
.925±.051
.889±.064
LSTM
.817±.072
.822±.072
.731±.031
.600±.101
CNN-GAF
.541±.162
.541±.140
.424±.098
.209±.156
F1-W=Weighted, F1-M=Macro, F1-S=Stress class
architectures: Logistic Regression (ℓ2), Random Forest (cuML, 200
trees), XGBoost (GPU hist, 300 estimators), LSTM (2-layer, 128 units,
BF16), and CNN-GAF (Gramian Angular Field, 4-layer CNN).
3.7
Live Inference System
The production XGBoost model is deployed via scripts/12_inference.py,
fetching live aggregated trades from the Binance public REST API
(GET /api/v3/aggTrades) over a strict 300-second time window
matching the training bar construction exactly. A mandatory pagi-
nation loop addresses a critical operational constraint: during high-
volatility events trade intensity routinely exceeds the exchange’s
1,000-record per-call limit, and a single call would silently truncate
the feature window. The system applies fractional differencing to
price in-place before inference, using a relaxed weight-truncation
threshold suited to the live history window available (training uses
years of history; live inference has on the order of minutes), and
declares a WARNING when 𝑃(stress) > 0.85 for ≥2 consecutive
bars — the continuity condition that distinguishes genuine regime
deterioration from transient microstructure noise.
4
Results and Discussion
4.1
Headline Results
Table 2 reports stability across five seeds and four expanding walk-
forward folds (pooled, fractionally differenced).
XGBoost dominates across all metrics. At Fold 4 (18.8M training
rows) it achieves binary F1-W of 0.9706 with seed range 0.0006 —
near-deterministic at this data scale. RF is a strong second (0.9452 ±
0.0398). Neural architectures substantially underperform: domain-
informed microstructure features aggregate temporal dynamics
into single-timestep representations, making gradient boosting
more effective than sequential architectures that would need to
re-learn what feature engineering already encodes. The pooled
model matches or exceeds asset-specific performance across all
three assets, validating the universal price formation hypothesis
[21]. Specifically, pooling exposes the model to cross-asset stress
contagion dynamics — the simultaneous deterioration patterns
across BTC, ETH, and SOL that asset-specific models trained on
single instruments cannot observe, and that proved decisive during
the FTX and Terra-Luna contagion episodes.
3


## Page 4

Goodness Kalu, Uchenna Ejike, Joseph Edet, Temitope E. Fagbuyi, Godfrey Kunde, and Hannah Igboke
Table 3: Baseline Comparison—Binary, Seed 42, Stress-Class
F1
Fold
Stress%
Persistence
Majority
XGBoost
Lift
1
31.2
0.566
0.000
0.793
+0.227
2
9.9
0.539
0.000
0.896
+0.357
3
11.0
0.517
0.000
0.907
+0.390
4
41.5
0.746
0.000
0.964
+0.218
Lift = XGBoost −Persistence, stress-class F1.
Figure 1: XGBoost SHAP feature attribution (Fold 4, Pooled).
RV and Intensity dominate; Kyle’s 𝜆ranks third, consistent
with adverse selection amplification during stress.
Baseline comparison and class prevalence. To confirm the
headline F1 reflects genuine predictive skill rather than regime
momentum or class imbalance, Table 3 compares XGBoost against
a persistence baseline (predict today’s label equals yesterday’s) and
a majority-class baseline. Stress class prevalence ranges from 9.9%
(Fold 2) to 41.5% (Fold 4). Despite Fold 4 having the highest stress
prevalence, XGBoost achieves a stress-class F1 of 0.9642 against
a persistence stress F1 of 0.7461 and a majority-class stress F1 of
0.000—an absolute lift of +0.218 over persistence on the hardest
fold. The lift is larger still in Folds 2 and 3, where stress prevalence
is under 11% and persistence stress F1 falls to 0.517–0.539. The high
weighted F1 is not an artifact of label autocorrelation; XGBoost
captures structural microstructure dynamics that a momentum rule
cannot recover.
4.2
Feature Attribution and Ablation
SHAP analysis (Fig. 1) consistently identifies RV and Intensity as
dominant predictors, with Kyle’s 𝜆third. This ranking is theoreti-
cally consistent: RV measures price instability, trade intensity cap-
tures the urgency of order submission during stress episodes, and
Kyle’s 𝜆encodes depth deterioration—the core mechanistic drivers
of liquidity stress [7]. Surrogate model fidelity (mean 91.8%, range:
83.9%–98.4%) validates these attributions.
Table 4: Lead-Time Analysis—XGBoost Binary, Seed 42,
Pooled
Event
Fold
To HMM Onset
To External Ref.
May 2021 Crash
1
persistent†
persistent†
Terra-Luna Collapse
2
108.3 min
108.3 min
FTX Bankruptcy
3
176.0 min
56.0 min‡
†Signal present throughout extended 12-hour search window; true onset predates lookback.
‡External ref: CZ tweet / FTT sell order at 12:00 UTC. HMM onset at 14:00 UTC.
Fractional differencing improves stress-class F1 for linear and
tree-based models (LR: +0.046; RF: +0.018). XGBoost shows negli-
gible change, having saturated the signal. CNN-GAF substantially
underperforms across all folds (binary stress F1: 0.209 ± 0.156),
confirming that domain-informed tabular microstructure features
aggregate temporal dynamics more effectively than image-based
representations for this problem class: the single-timestep feature
engineering already encodes the structure that a convolutional
architecture would need to rediscover from raw visual patterns.
Cross-evaluation falsification test. A direct test of whether
XGBoost learns the HMM’s feature geometry rather than an in-
dependent stress signal is to cross-evaluate: train on local HMM
labels and test against global labels, and vice versa. When XGBoost
is trained and evaluated on the same local label set, it achieves
F1-W 0.9917 and stress F1 0.9881—consistent with learning a co-
herent decision boundary. When the same locally-trained model is
evaluated against global labels, weighted F1 collapses to 0.8066 and
stress F1 drops to 0.4802. The production model trained on global
labels achieves F1-W 0.9801 and stress F1 0.9065. This asymmetry
demonstrates that the two label sets encode genuinely different
information: a model that has learned one cannot approximate the
other. XGBoost is not recovering latent mixture structure from
its own inputs—it is learning a stress signal that is specific to the
global regime calibration, which the external validation framework
independently confirms to be economically meaningful.
4.3
Predictive Lead-Time Analysis
Table 4 reports lead times against two reference definitions: HMM-
defined stress onset and externally documented crisis timestamps.
For Terra-Luna, the external timestamp aligns with HMM onset
(108.3 min); both measure the same structural break. For FTX, the
external reference is the publicly documented trigger (CZ tweet and
FTT sell order, 12:00 UTC), which precedes HMM-defined onset by
two hours. XGBoost issued a sustained warning at 11:04 UTC—56
minutes before the external trigger and 176 minutes before the
HMM transition. The 56-minute figure is the more conservative
and more honest measure: it confirms genuine advance warning
against a publicly observable event rather than merely anticipating
an HMM state transition in shared feature space.
The May 2021 event requires separate treatment. The model
issued a sustained warning at the start of the 12-hour search win-
dow and maintained it continuously; extending the window further
would yield larger numbers without additional meaning. This be-
haviour is consistent with the character of the event: May 2021 was
a prolonged regime deterioration, not an acute collapse. The model
4


## Page 5

An Early Warning System for Liquidity Stress in Cryptocurrency Markets Using Trade Flow Analysis and Machine Learning
Figure 2: Global HMM stress rate during pre-crisis vs cri-
sis windows. All four events show statistically significant
elevation (𝑝< 0.0001, proportion z-test). Terra-Luna shows
moderate BTC elevation (37.2%), consistent with DeFi-specific
contagion.
reflects this distinction—it remained in a sustained elevated state
throughout the deterioration rather than producing a single con-
centrated pre-collapse signal. This sensitivity to crisis type is itself
an informative result: the same framework that provides a clean
56-minute warning before an acute exchange failure also captures
the diffuse multi-day microstructure deterioration that preceded
the 2021 crash.
Terra-Luna and FTX show no price drawdown breach within
the search window for the 5% rolling threshold. This is consistent
with the nature of both events: Terra-Luna was a stablecoin depeg
and FTX was a solvency event—structural failures that manifested
first in microstructure and order flow before producing sustained
price declines in the major pairs. The absence of a price-drawdown
reference for these events reinforces rather than undermines the
framework’s claim: order flow stress preceded observable price
impact.
4.4
External Validity of HMM Stress Labels
4.4.1
Global HMM Stability and Local Instability. The global HMM
is near-deterministic: ETH/SOL show 0.00 × 100 parameter differ-
ence between independent training runs; BTC shows 2.66 × 10−7
(floating-point noise). This is not a random local optimum—it is the
unique convergent solution at this data scale.
Local HMMs fitted using only fold-available training data are
systematically miscalibrated. Stress percentages range from 6.0%
to 94.3% for identical assets and periods. SOL Fold 2 assigns 94.3%
stress to a 7-month window; BTC Fold 3 assigns 78.4% during the
post-FTX stabilisation period—a miscalibration caused by the local
model having never observed a recovery regime. This instability
is not a data starvation problem: it persists in SOL Fold 2 with 13
months of training data because narrow windows lack cross-cycle
regime diversity.
The controlled experiment design is critical: features, architec-
ture, fitting procedure, and state labelling are identical across global
and local HMMs. The only variable is the data horizon. When global
outperforms local against external judges, the conclusion is iso-
lated: microstructure stress detection requires cross-cycle training
breadth.
4.4.2
Tier 1: Known Crisis Validation. Proportion z-tests confirm
significant stress elevation during all four documented events (Fig. 2).
Figure 3: Cohen’s 𝜅between global (blue) and local (orange)
HMM labels and three external validators across all folds.
Global HMM consistently outperforms local, most decisively
on the cross-asset validator where local collapses to slight or
near-zero agreement.
Table 5: Tier 2: Cohen’s 𝜅—Cross-Asset Validator (selected)
Fold
Asset
Global 𝜅
Local 𝜅
Global
Local
1
ETHUSDT
0.829
0.334
almost perfect
fair
2
ETHUSDT
0.762
0.052
substantial
slight
2
SOLUSDT
0.778
0.021
substantial
slight
3
BTCUSDT
0.775
0.088
substantial
slight
4
ETHUSDT
0.840
0.621
almost perfect
substantial
Landis & Koch (1977) [15] interpretation.
All z-scores exceed 100 (range: 102.9–333.8, 𝑝< 0.001). These tests
assume approximately independent observations; financial bar data
exhibit serial dependence, and crisis windows are persistent by con-
struction, which inflates standard errors relative to i.i.d. baselines.
A circular block bootstrap robustness check directly addresses this
concern: 𝑛crisis-length resamples are drawn from the 30-day pre-
crisis baseline using circular block bootstrap (block size = 1 day =
288 bars, 10,000 replicates), constructing a null distribution with
the same variance as the observed crisis statistic. This confirms
significance for all four events across all assets at 𝑝< 0.0001, with
sensitivity confirmed at 4-day blocks.1 The results are therefore
strongly indicative rather than exact, but robust to serial depen-
dence under all tested block sizes. Cross-asset simultaneous stress
confirms systemic contagion: FTX shows 72.1% of bars with all three
assets simultaneously stressed; May 2021 shows 100% any-asset
simultaneous stress across the full crisis window.
4.4.3
Tier 2: Global vs Local HMM External Validation. Table 5 and
Fig. 3 report Cohen’s 𝜅against three external validators. Global
HMM outperforms or matches local in every fold-asset combination.
The cross-asset validator is most discriminating: global achieves
substantial to almost perfect agreement while local collapses to
slight or near-zero in multiple folds (e.g. ETH Fold 2: global 𝜅=
0.762 vs local 𝜅= 0.052; SOL Fold 2: global 0.778 vs local 0.021).
These are the same folds where local HMM assigned 57.5% and
94.3% stress respectively—a miscalibrated HMM cannot co-occur
with a sparse external signal.
Crisis timestamp kappa is lower for both variants by design:
3–4 day windows inside 6–7 month test periods guarantee sparse
1Full bootstrap output including per-asset pre-crisis and crisis stress rates and 95%
confidence intervals is available in the supplementary repository at https://github.
com/Goodie-Goody/maic.
5


## Page 6

Goodness Kalu, Uchenna Ejike, Joseph Edet, Temitope E. Fagbuyi, Godfrey Kunde, and Hannah Igboke
chance-corrected agreement. This is expected and informative—
global still consistently outperforms local even on this unfavourable
metric.
The results are consistent with global HMM labels capturing
genuine economic stress rather than closing the self-referentiality
critique entirely. The external validators confirm that global labels
behave as stress indicators should: they elevate during documented
crises, align with cross-asset contagion, and degrade systemati-
cally when the HMM is miscalibrated. Residual circularity through
shared volatility clustering cannot be fully eliminated without non-
volatility-linked validators such as funding rates or depth data,
which we identify as a direction for future work.
Importantly, the external validators confirm label validity but
could not replace the microstructure labelling scheme. Crisis times-
tamps cover only ≈12 days of 1,440—insufficient for continuous
bar-level labels. Cross-asset stress is circular as a primary labelling
mechanism. Price drawdown detects the outcome of stress, not its
onset. Only microstructure features detect order flow deterioration
before price reflects it—the mechanism behind the 56–176 minute
lead times against external reference definitions.
4.4.4
Tier 3: Silent Event Discovery. Scanning the full history out-
side known crisis windows identifies 15 stress episodes exceeding 60
minutes. The most intense is an ETH episode beginning 2024-11-24,
lasting approximately 1,471 hours; five of the ten longest episodes
identified are ETH events clustered in November–December 2024.
Silent events demonstrate the framework’s forward-looking utility
beyond named retrospective events.
4.4.5
Robustness to Fully-Causal Relabelling. A stronger test than
local Viterbi decoding alone is available: an HMM refit per fold
on strictly prior data (as in Section 4.4), decoded with a causal for-
ward filter that conditions each label only on observations up to
and including that bar—eliminating look-ahead not just across fold
boundaries but within the test window itself. As a control, replac-
ing only the decoding step—holding the same globally-fit model,
substituting causal forward-filtering for Viterbi—changes labels
minimally (97–98% agreement with the production Viterbi labels;
Tier 2 kappa differs by at most 0.03 across all fold-asset-validator
combinations). Applying the fully-causal procedure instead and
re-computing Tier 2 kappa against the same three external valida-
tors, global HMM labels outperform in 29 of 30 fold-asset-validator
comparisons. Notably, the fully-causal procedure independently re-
produces the exact local-HMM kappa values reported in Table 5 for
ETH Fold 2 (𝜅= 0.052) and SOL Fold 2 (𝜅= 0.021), despite differing
methodologically in both fitting and decoding procedure from the
local HMM baseline. This convergence, together with the negligible
effect of decoding alone, indicates the instability originates specif-
ically in training-window breadth, reinforcing the conclusion of
Section 4.4.
4.5
Discussion
XGBoost dominance reflects the effectiveness of domain-informed
feature engineering: microstructure features temporally aggregate
what sequential architectures would need to re-learn. The cross-
evaluation falsification test and the three-tier external validation
framework together establish three conclusions beyond model per-
formance. First, global HMM labels are consistent with genuine
economic stress, as confirmed by independent validators. Second,
XGBoost performance is not reducible to label geometry recovery:
a locally-trained model evaluated against global labels collapses on
stress F1 from 0.988 to 0.480, demonstrating that the two label sets
encode genuinely different information. Third, cross-cycle training
breadth is a critical design requirement: narrow-horizon HMMs do
not produce more temporally honest labels—they produce miscali-
brated ones.
5
Conclusion
This paper presents a high-frequency early warning system for liq-
uidity stress in Binance spot cryptocurrency markets, shifting the
analytical focus from retrospective forensic analysis to prospective
detection. By engineering natively stationary microstructure fea-
tures from publicly accessible trade data, we eliminate the reliance
on proprietary order book feeds. Extensive walk-forward evalua-
tion across 18.8 million observations demonstrates that XGBoost
achieves a binary weighted F1 of 0.9706, substantially outperform-
ing a persistence baseline (F1-W 0.7891) and providing 56 minutes
of advance warning before the documented FTX market trigger
and 108 minutes before the Terra-Luna structural break—measured
against externally documented reference definitions rather than
HMM-defined onset.
Our three-tier external validation framework establishes that
regime labelling requires cross-cycle global calibration to prevent
systematic miscalibration—locally-fitted HMMs produce stress per-
centages ranging from 6.0% to 94.3% for identical assets and periods,
while the global HMM achieves substantial to almost perfect Co-
hen’s 𝜅against genuinely independent external validators. The
results are consistent with global HMM labels capturing economi-
cally meaningful stress regimes. A cross-evaluation falsification test
further confirms that XGBoost performance is not reducible to label
geometry recovery: stress F1 collapses from 0.988 to 0.480 when
a locally-trained model is evaluated against global labels, demon-
strating the two label sets encode genuinely different information.
This conclusion is independently reinforced by a fully-causal re-
labelling procedure—walk-forward HMM refitting combined with
causal forward-filter decoding—which outperforms local Viterbi
decoding in 29 of 30 fold-asset-validator comparisons against the
same external validators. The global HMM is near-deterministic
(2.66 × 10−7 maximum parameter difference across independent
runs), confirming it represents the unique convergent solution at
this data scale, not a random local optimum.
By providing the complete data pipeline and a live Binance API in-
ference system (https://github.com/Goodie-Goody/maic), this work
bridges the gap between academic market microstructure theory
and deployable real-world trading infrastructure. The current frame-
work is intentionally scoped to Binance spot markets for BTC, ETH,
and SOL — a deliberate design choice that enables deep longitudinal
analysis across 4.2 billion trades and five distinct market regimes, at
the cost of cross-venue generalisability. Future work will extend the
framework to perpetual funding rates and cross-exchange fragmen-
tation as independent stress signals, investigate non-price-derived
supervised targets to further isolate classification performance from
6


## Page 7

An Early Warning System for Liquidity Stress in Cryptocurrency Markets Using Trade Flow Analysis and Machine Learning
label generator geometry, and explore multimodal architectures
incorporating NLP sentiment signals as complementary early warn-
ing indicators.
Acknowledgments
The lead author thanks WorldQuant University for their educa-
tional support and the open-source community behind the scien-
tific Python ecosystem, without which this research would not
have been possible. GPU computing infrastructure was provided
via RunPod cloud services on an NVIDIA RTX PRO 4500 Blackwell
GPU. The contributing authors provided invaluable manuscript
review, editorial feedback, and conceptual input throughout the
preparation of this work. Portions of this manuscript were prepared
with the assistance of Claude (Anthropic) for editorial refinement
and structural review.
References
[1] Amro Saleem Alamaren, Korhan K. Gokmenoglu, and Nigar Taspinar. 2024.
Volatility Spillovers among Leading Cryptocurrencies and US Energy and Tech-
nology Companies. Financial Innovation 10, 1 (Feb. 2024), 81. doi:10.1186/s40854-
024-00626-2
[2] Yakov Amihud. 2002. Illiquidity and Stock Returns: Cross-Section and Time-
Series Effects. Journal of Financial Markets 5, 1 (Jan. 2002), 31–56. doi:10.1016/
S1386-4181(01)00024-6
[3] Torben G. Andersen and Tim Bollerslev. 1998. Answering the Skeptics: Yes,
Standard Volatility Models Do Provide Accurate Forecasts. International Economic
Review 39, 4 (1998), 885–905. doi:10.2307/2527343
[4] Leonard E. Baum, Ted Petrie, George Soules, and Norman Weiss. 1970. A Maxi-
mization Technique Occurring in the Statistical Analysis of Probabilistic Func-
tions of Markov Chains. The Annals of Mathematical Statistics 41, 1 (1970),
164–171. doi:10.1214/aoms/1177697196
[5] Monica Billio, Mila Getmansky, Andrew W. Lo, and Loriana Pelizzon. 2012.
Econometric Measures of Connectedness and Systemic Risk in the Finance and
Insurance Sectors. Journal of Financial Economics 104, 3 (June 2012), 535–559.
doi:10.1016/j.jfineco.2011.12.010
[6] Antonio Briola, David Vidal-Tomás, Yuanrong Wang, and Tomaso Aste. 2023.
Anatomy of a Stablecoin’s Failure: The Terra-Luna Case. Finance Research Letters
51 (Jan. 2023), 103358. doi:10.1016/j.frl.2022.103358
[7] Markus K Brunnermeier and Lasse Heje Pedersen. 2009. Market Liquidity and
Funding Liquidity. The review of financial studies 22, 6 (2009), 2201–2238.
[8] Tarun Chordia, Richard Roll, and Avanidhar Subrahmanyam. 2002. Order Imbal-
ance, Liquidity, and Market Returns. Journal of Financial Economics 65, 1 (2002),
111–130. doi:10.1016/S0304-405X(02)00136-8
[9] Jacob Cohen. 1960. A coefficient of agreement for nominal scales. Educational
and psychological measurement 20, 1 (1960), 37–46.
[10] David Easley, Maureen O’Hara, Songshan Yang, and Zhibai Zhang. 2024. Micro-
structure and Market Dynamics in Crypto Markets. SSRN Electronic Journal.
doi:10.2139/ssrn.4814346
[11] Lawrence R. Glosten and Paul R. Milgrom. 1985. Bid, Ask and Transaction
Prices in a Specialist Market with Heterogeneously Informed Traders. Journal of
Financial Economics 14, 1 (March 1985), 71–100. doi:10.1016/0304-405X(85)90044-
3
[12] Alec N Kercheval and Yuan Zhang. 2015. Modelling High-Frequency Limit Order
Book Dynamics with Support Vector Machines. Quantitative Finance 15, 8 (2015),
1315–1329.
[13] Andrei A. Kirilenko, Albert S. Kyle, Mehrdad Samadi, and Tugkan Tuzun. 2011.
The Flash Crash: The Impact of High Frequency Trading on an Electronic Market.
SSRN Electronic Journal. SSRN:1686004 doi:10.2139/ssrn.1686004
[14] Albert S. Kyle. 1985. Continuous Auctions and Insider Trading. Econometrica 53,
6 (Nov. 1985), 1315. jstor:1913210 doi:10.2307/1913210
[15] J Richard Landis and Gary G Koch. 1977. The measurement of observer agreement
for categorical data. Biometrics 33 (1977), 159–174.
[16] Charles M. C. Lee and Mark J. Ready. 1991. Inferring Trade Direction from
Intraday Data. The Journal of Finance 46, 2 (1991), 733–746. doi:10.1111/j.1540-
6261.1991.tb02683.x
[17] Yukun Liu and Aleh Tsyvinski. 2021. Risks and Returns of Cryptocurrency. The
Review of Financial Studies 34, 6 (2021), 2689–2727. doi:10.1093/rfs/hhaa113
[18] Marcos López de Prado. 2018. Advances in Financial Machine Learning. Wiley,
Hoboken, NJ.
[19] Scott Lundberg and Su-In Lee. 2017. A Unified Approach to Interpreting Model
Predictions. arXiv:1705.07874 [cs] doi:10.48550/arXiv.1705.07874
[20] Richard Roll. 1984. A Simple Implicit Measure of the Effective Bid-Ask Spread in
an Efficient Market. The Journal of Finance 39, 4 (1984), 1127–1139. doi:10.1111/
j.1540-6261.1984.tb03897.x
[21] Justin Sirignano and Rama Cont. 2018. Universal Features of Price Formation in
Financial Markets: Perspectives from Deep Learning. arXiv:1803.06917 [q-fin]
doi:10.48550/arXiv.1803.06917
[22] Andrew J. Viterbi. 1967. Error Bounds for Convolutional Codes and an Asymp-
totically Optimum Decoding Algorithm. IEEE Transactions on Information Theory
13, 2 (1967), 260–269. doi:10.1109/TIT.1967.1054010
7


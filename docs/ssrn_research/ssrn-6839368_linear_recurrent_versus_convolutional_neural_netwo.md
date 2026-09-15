# Linear Recurrent versus Convolutional Neural Networks for

- **Source File**: `ssrn-6839368.pdf`
- **Total Pages**: 11
- **SSRN ID**: `ssrn-6839368`

---

## Page 1

Linear Recurrent versus Convolutional Neural Networks for
High-Frequency Cryptocurrency Trading: Evidence from Dollar-Bar
Data
A R T I C L E I N F O
Keywords:
High-Frequency Trading
Deep Learning
Market Microstructure
Temporal Convolutional Networks
Linear Recurrent Neural Networks
Dollar Bar Aggregation
A B S T R A C T
Deep learning in high-frequency trading (HFT) faces a computational dilemma: capturing long-range
dependencies is desirable but incurs quadratic complexity in Transformers. Linear Recurrent Neural
Networks (minGRU, minLSTM) promise 𝑂(𝐿) training and 𝑂(1) inference via associative scans.
We benchmark these architectures against Temporal Convolutional Networks (TCNs), LSTMs,
Transformers, and XGBoost on dollar-bar data from three cryptocurrency pairs (XBTUSD, ETHUSD,
SOLUSD) spanning over 50 million ticks. Our results reveal a multifaceted trade-off that defies
a universal solution. Computationally, TCNs achieve 3× faster training than minRNNs and 15×
faster than Transformers at length 1024. Financially, the optimal architecture depends on asset
maturity and context length: on mature Bitcoin, LSTM and even XGBoost deliver competitive returns,
while TCN provides superior risk-adjusted stability (Sortino ratio up to 0.209 at length 512); on
momentum-driven Ethereum, minLSTM excels with +16.43% return given long context, but degrades
at shorter lengths. On highly volatile Solana, all models lose money, highlighting the limits of pure
microstructure prediction. We further show that minLSTM yields the best-calibrated probabilities
(ECE 0.032) and that threshold sensitivity curves expose XGBoost’s fragility. No single model
consistently outperforms across all regimes; we therefore advocate for an adaptive, asset-aware model
selection strategy.
1. Introduction
The microstructure of financial markets presents a set
of challenges that differ from other domains of sequence
modelling, particularly Natural Language Processing (NLP).
High-frequency financial time series are characterised by
extreme non-stationarity, severe low signal-to-noise ratios
(SNR), and exponential information decay [5, 8]. Unlike
natural language, where semantic dependencies can be thou-
sands of tokens, financial tick data is frequently dominated
by instantaneous order flow imbalances, latency arbitrage
dynamics, and mean-reversion noise [6, 32, 33]. Conse-
quently, the long-range dependency problem in quantitative
finance is distinct: the primary challenge is not merely
preserving historical context but the selective filtration of
stochastic noise to identify momentary regime shifts.
For many years, Long Short-Term Memory (LSTM)
[35] networks have been the standard for financial sequence
modelling. The gating mechanism effectively mitigates the
vanishing gradient problem. Hypothetically, it enables the
architecture to learn long-term dependencies [42–44].
However, the inherent sequential dependency of the
LSTM creates a significant computational bottleneck. This
means that the hidden state at time 𝑡cannot be computed
until the state at 𝑡−1 is determined. Consequently, paralleli-
sation on modern GPU hardware and training performance
will be severely limited, particularly on the massive tick-
level data used in modern algorithmic trading [18, 34]. In
the financial industry, where model retraining frequency is
directly translated to alpha preservation, such a bottleneck
constitutes a critical drawback.
ORCID(s):
The self-attention mechanism in the Transformer archi-
tecture [36] fixed the parallelisation problem and enabled
the model to process whole sequences simultaneously. This
feature, however, introduced an 𝑂(𝐿2) quadratic computa-
tional and memory complexity relative to sequence length.
In High-Frequency Trading (HFT), where predictive models
must take in sequences with millions of ticks to capture
multi-scale dynamics, this memory footprint becomes in-
tractable. Moreover, the global attention mechanism tends to
overfit correlations between distant, often unrelated market
events and may not be suited for financial time series [16].
1.1. The Renaissance of Linear Recurrence
The recent resurgence of Linear RNNs and Structured
State Space Models (SSMs), including Mamba [2] and the
Minimalist GRU (minGRU) [1], aims to address this gap.
By eliminating the non-linear hidden-state dependency from
gate computation, these architectures enable the recurrence
to be reformulated as a parallel associative scan. This ap-
proach achieves 𝑂(𝐿) training complexity while maintaining
the 𝑂(1) inference state characteristic of traditional RNNs,
thereby providing a theoretically optimal compromise for
latency-critical applications.
1.2. Research Objectives and Contributions
The present work critically examines the hypothesis that
these Linear RNNs represent the new state-of-the-art for
HFT. We compare them against the Temporal Convolutional
Network (TCN) [37], which relies on a fundamentally differ-
ent inductive bias of strict locality via dilated convolutions,
and against established baselines (LSTM, Transformer, XG-
Boost). We utilised a dataset of dollar-bar aggregated trades
from Kraken (XBT, ETH, SOL) and formulated the follow-
ing contributions:
Ahoora Rostamian: Preprint submitted to Elsevier
Page 1 of 11
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6839368
Preprint not peer reviewed


## Page 2

Linear Recurrent versus Convolutional Neural Networks for High-Frequency Cryptocurrency Trading
1. Empirical Examination of Transformer Efficiency:
We demonstrate that standard Transformers are ill-
suited for high-frequency trading retraining loops,
with training times scaling quadratically to over 20
seconds per epoch compared to 1.5 seconds for TCNs
with a sequence length of 1024.
2. No Universal Inductive Bias: We find that the opti-
mal memory length is not fixed; short-memory TCNs
offer the most stable risk-adjusted metrics on mature
assets, while longer-memory LSTMs and minLSTMs
generate higher absolute returns on momentum-driven
assets when given sufficient context.
3. Importance of Calibration: minLSTM provides the
best-calibrated probabilities (ECE 0.032), leading to
smoother threshold sensitivity curves, whereas over-
confident models (Transformer, XGBoost) exhibit er-
ratic profit-and-loss (PnL) profiles.
4. Asset-Specific Regime Dependence: The ranking of
models reverses across volatility regimes and asset
classes, highlighting the need for adaptive model se-
lection rather than a one-size-fits-all architecture.
The remainder is organized as follows: Section II re-
views the evolution of deep learning in finance. Section III
establishes the mathematical framework for minRNN par-
allel scans and Dollar Bar sampling. Section IV details the
experimental methodology. Section V presents the computa-
tional and economic results with a full multi-asset analysis.
Section VI discusses the implications for market efficiency
theory, and Section VII concludes.
2. Related Work
2.1. Deep Learning in Quantitative Finance
The adoption of deep learning in finance and the tran-
sition from classical econometric approaches have been
partly driven by the need to capture non-linear dependen-
cies in high-frequency data such as Limit Order Books
(LOB), alongside the surge in data availability, compu-
tational power, and advances in representation learning.
Zhang and Zohren [26] modelled the order book as a spatial
image (DeepLOB). They demonstrated the effectiveness of
Convolutional Neural Networks (CNNs) for LOB prediction.
Borovykh et al. [48], Sirignano and Cont [47] further
explored universal price formation features. Nevertheless,
standard CNN architectures are often scrutinised for lacking
statefulness required to model regime shifts in the long run.
LSTMs dealt with the mentioned limitation by introducing
memory cells, meanwhile introducing significant training
bottlenecks due to their sequential nature [46]. Bhanujyothi
and Jacob [22] emphasise the effort to balance architectural
complexity with noise robustness in high-frequency risk
assessment. Researchers have also looked into multi-modal
approaches combining news sentiment with price action
[14], often leveraging LLMs for qualitative reasoning [15,
21]. These methodologies often use models like GPT-3 [53]
which result in inference latency within HFT environments.
2.2. Transformers in Time Series Forecasting
Transformers have revolutionised NLP; however, their
application to time series forecasting remains debatable.
Zeng et al. [16] argued that they are prone to overfitting in
low-signal domains as a result of permutation-invariance of
self-attention, which necessitates explicit positional encod-
ings to discern temporal dependencies. This is disadvanta-
geous in finance, where the sequential order of trade arrival
is the primary signal [7]. Optimised models such as Informer
[45] and FlashAttention [40] attempt to mitigate costs, yet
their efficacy remains a subject of debate. On the contrary,
[23] demonstrates that modifying Transformers with local
attention windows can be effective, thereby making their
architecture more similar to CNNs. In this study, we evaluate
the standard Transformer to establish a baseline for why
these modifications are necessary and to quantify the cost
of global attention mechanisms in high-frequency domains.
2.3. Efficient Recurrence and State Space Models
The Linear Attention linearises the attention mechanism
to achieve 𝑂(𝐿) complexity, and the Structured State Space
Model (S4) [38] and Mamba, which is considered to be
its successor [2], leverage continuous-time control theory
to extract discrete-time recurrences efficiently. We observed
this group of models has been developed rapidly, with vari-
ants including MambaTS [12], S4M for missing values [13],
and TimeMachine [27]. These models show the theoretical
convergence between Transformers and SSMs [40]. xL-
STM [4] extends LSTMs using matrix memory in order
to enhance capacity. MinRNNs [1] simplify this landscape
even further by trimming the SSM framework to its barest
recurrent gates through parallel scan algorithm. This mini-
malist view is backed by theoretical work on the expressive
power of gated linear units [17] and the theoretical limits of
linear recurrence [10]. Contrary to Mamba, which requires
complex CUDA kernels for selective scanning, minRNNs
can be implemented using standard PyTorch primitives or
parallel scan implementations [24]. As a result, these models
are more accessible for financial researchers. Furthermore,
advances in ensuring robustness against concept drift [25],
improving trustworthy sequence learning, and stabilising
neural ODEs [11] are critical for financial deployment. Re-
cent work even explores quantum machine learning [29] and
adaptive spectral blocks [28] for risk management. However,
minRNNs represent a more immediate practicality. To our
knowledge, this is the first study benchmarking minRNNs
specifically on cryptocurrency dollar bars, providing a cru-
cial evaluation of their utility in stochastic, noisy environ-
ments.
3. Problem Formulation and Preliminaries
3.1. Information Preservation via Dollar Bars
Financial modelling frequently uses time-based bars
(e.g., 1-minute or 5-minute candlesticks). However, in cryp-
tocurrency markets where trading activity is notably bursty,
a 1-minute bar may encapsulate 10,000 trades during a flash
crash, while a subsequent bar through a quiet period may
Ahoora Rostamian: Preprint submitted to Elsevier
Page 2 of 11
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6839368
Preprint not peer reviewed


## Page 3

Linear Recurrent versus Convolutional Neural Networks for High-Frequency Cryptocurrency Trading
contain only 10. This irregularity violates the Independent
and Identically Distributed (IID) assumptions required by
standard neural network optimisation algorithms [30]. To
address this, we employ Dollar Bar Aggregation to restore
statistical properties closer to normality [20]. Let the se-
quence of trades be denoted by = {(𝑡𝑖, 𝑝𝑖, 𝑣𝑖)}𝑁
𝑖=1, where 𝑡𝑖
is the timestamp, 𝑝𝑖is the price, and 𝑣𝑖is the volume of the 𝑖-
th trade. We sample a bar at index 𝑘such that the cumulative
dollar value reaches a predefined threshold 𝜃:
𝑘
∑
𝑖=𝑘𝑙𝑎𝑠𝑡+1
𝑝𝑖𝑣𝑖≥𝜃
(1)
where 𝜃= $10, 000 is the dollar threshold used in this
study. By doing so, we ensure that every input step to the
model contains a constant amount of trading activity, thus
normalising volatility and restoring partial stationarity to the
time series [9].
Lemma 3.1 (Variance Stability of Dollar Bars). Let the
variance of returns at time 𝑡be 𝜎2
𝑡. Under time-based sam-
pling, the variance is proportional to the volume traded:
Var(𝑟𝑡) ∝Volume𝑡. Since volume is heteroskedastic, time-
sampled returns are inherently heteroskedastic. Under dollar
sampling, the volume per bar is constant by definition (≈𝜃),
implying that Var(𝑟𝑑𝑜𝑙𝑙𝑎𝑟) ≈constant. This satisfies the
stationarity requirements of Gradient Descent optimisation
more effectively than time-based sampling.
3.2. Mathematical Formulation of Linear
Recurrence
The innovation of minRNNs lies in the removal of the
non-linear hidden-state dependency in the gate computation,
which enables parallelisation. Consider the standard GRU
update for the update gate 𝑧𝑡:
𝑧𝑡= 𝜎(𝑊𝑧𝑥𝑡+ 𝑈𝑧ℎ𝑡−1)
(2)
The term 𝑈𝑧ℎ𝑡−1 enforces sequential execution because the
hidden state ℎ𝑡−1 must be fully computed before 𝑧𝑡can
be determined. minGRU simplifies this by removing the
recurrent weight matrix 𝑈𝑧:
𝑧𝑡= 𝜎(𝑊𝑧𝑥𝑡),
̃ℎ𝑡= 𝑔(𝑊ℎ𝑥𝑡)
(3)
where 𝑔(⋅) is a non-linearity. The recurrence then simplifies
to a linear interpolation:
ℎ𝑡= (1 −𝑧𝑡) ⊙ℎ𝑡−1 + 𝑧𝑡⊙̃ℎ𝑡
(4)
This equation represents a first-order linear recurrence rela-
tion of the form ℎ𝑡= 𝑎𝑡ℎ𝑡−1 + 𝑏𝑡, where 𝑎𝑡= (1 −𝑧𝑡) and
𝑏𝑡= 𝑧𝑡̃ℎ𝑡. This structure is crucial as it permits the use of
parallel prefix sums.
3.3. Parallel Associative Scan
Equation (4) can be solved non-sequentially using the
parallel prefix scan algorithm. We first rewrite the recurrence
in log-space to convert multiplicative updates into additive
ones, enhancing numerical stability:
𝛼𝑡= log(1 −𝑧𝑡)
(5)
𝛽𝑡= log(𝑧𝑡) + log(̃ℎ𝑡)
(6)
The hidden state ℎ𝑡can then be expressed non-recursively as
a weighted sum of all previous inputs:
ℎ𝑡=
𝑡∑
𝑘=1
(
exp
(
𝑡∑
𝑗=𝑘+1
𝛼𝑗
))
exp(𝛽𝑘)
(7)
By defining an associative operator ⊕on tuples (𝛼, 𝛽):
(𝛼𝑖, 𝛽𝑖) ⊕(𝛼𝑗, 𝛽𝑗) = (𝛼𝑗+ 𝛼𝑖, log(𝑒𝛽𝑗+ 𝑒𝛼𝑗+𝛽𝑖))
(8)
the sequence of hidden states can be computed in 𝑂(log 𝐿)
time using a tree-based reduction algorithm on a GPU,
leveraging CUDA warp primitives for high efficiency [19].
4. Proposed Methodology
4.1. Temporal Convolutional Networks (TCN)
The TCN architecture [37] relies on causal, dilated con-
volutions to model temporal dependencies, drawing on prin-
ciples from Residual Learning [41] and Depthwise Sepa-
rable Convolutions [52]. Unlike RNNs, which maintain a
hidden state ℎ𝑡, TCNs operate on a fixed-length history
defined by their receptive field. For an input sequence 𝐱and a
filter 𝑓, the dilated convolution operation at time 𝑡is defined
as:
𝐹(𝑡) = (𝑥∗𝑑𝑓)(𝑡) =
𝑘−1
∑
𝑖=0
𝑓(𝑖) ⋅𝐱𝑡−𝑑⋅𝑖
(9)
where 𝑑is the dilation factor, 𝑘is the kernel size, and ∗𝑑
denotes the dilated convolution operator. To explicitly test
the value of extreme locality in high-frequency data, we im-
plemented a shallow TCN architecture comprising 2 layers
with dilation factors 𝑑∈{1, 2}. Crucially, the parallel span
complexity of a TCN is 𝑂(1), as all time steps in a sequence
can be computed simultaneously via matrix multiplication.
This architectural prior enforces locality; hence the model is
structurally incapable of “attending” to future information
(causality) and biases the learning process towards local
geometric patterns [39].
To disentangle the effect of memory length from the
architecture itself, we additionally tested a variant with 3
layers and dilations {1, 2, 4}, giving an effective receptive
field of approximately 15 bars. This allows us to probe
whether the observed locality advantage is due to the short
memory or the convolutional architecture.
4.1.1. Receptive Field Calculation
For a TCN with kernel size 𝑘and 𝑛layers with dilations
𝑑𝑖, the effective receptive field (RF) is calculated as:
𝑅𝐹= 1 +
𝑛
∑
𝑖=1
(𝑘−1) ⋅𝑑𝑖
(10)
Ahoora Rostamian: Preprint submitted to Elsevier
Page 3 of 11
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6839368
Preprint not peer reviewed


## Page 4

Linear Recurrent versus Convolutional Neural Networks for High-Frequency Cryptocurrency Trading
In our main experiments, utilising a kernel size of 𝑘= 3
and dilation factors [1, 2], the effective receptive field is ap-
proximately 7 bars. This extremely short window enforces a
strong inductive bias that only the immediate microstructure
matters. The extended variant with dilations [1, 2, 4] has an
RF of 15 bars.
4.2. Universal Model Architecture
To ensure a fair comparison, all models are embedded
within a unified “Universal Model” framework. This frame-
work consists of:
1. Input Projection: A linear layer mapping the 4-
dimensional input features to the hidden dimension
𝑑𝑚𝑜𝑑𝑒𝑙= 256.
2. Core Sequence Encoder: The specific architecture
under test (e.g., minGRU, TCN Block).
3. Layer Normalisation: Applied to the output of the
sequence encoder to stabilise training.
4. Prediction Head: A final linear layer projecting the
hidden state ℎ𝑇(at the last time step) to the class logits
(Bear, Neutral, Bull).
This standardisation ensures that performance differences
are attributable to the sequence modelling mechanism itself,
rather than auxiliary architectural choices.
4.3. Microstructure Feature Engineering
Input features (𝐱𝑡∈ℝ4) per dollar bar were selected
based on market microstructure theory to capture the state
of the limit order book and price dynamics:
1. Log Returns (𝑟𝑡): ln(𝑝𝑡∕𝑝𝑡−1).
2. Order Flow Imbalance (OFI): A critical feature cap-
turing buying versus selling pressure [31]:
OFI𝑡=
𝑉𝑏𝑢𝑦
𝑡
−𝑉𝑠𝑒𝑙𝑙
𝑡
𝑉𝑏𝑢𝑦
𝑡
+ 𝑉𝑠𝑒𝑙𝑙
𝑡
+ 𝜖
(11)
where 𝑉𝑏𝑢𝑦
𝑡
and 𝑉𝑠𝑒𝑙𝑙
𝑡
represent the volume of buy-
initiated and sell-initiated trades, respectively.
3. Tick Intensity (𝜏𝑡): ln(1 + count𝑡), serving as a proxy
for the information arrival rate.
All features are centred on the median and scaled by the
Interquartile Range (RobustScaler) to handle the heavy-
tailed distributions of cryptocurrency assets.
5. Algorithm Design
5.1. Walk-Forward Validation Algorithm
To evaluate model performance in a non-stationary envi-
ronment, we used an expanding-window Walk-Forward Val-
idation method. This approach respects temporal causality,
ensuring that no future information leaks into the training
set.
5.2. Backtesting Simulation Engine
The viability of the models is assessed using a vectorised
backtesting engine designed to replicate institutional trading
constraints and transaction costs.
Algorithm 1 Walk-Forward Validation Protocol
Require: Dataset = {(𝐱𝑡, 𝑦𝑡)}𝑇
𝑡=1, Folds 𝐾= 5, Initial
Train % 𝑃= 0.5
1: 𝑇𝑠𝑡𝑎𝑟𝑡←⌊𝑇× 𝑃⌋
2: 𝑇𝑓𝑜𝑙𝑑←⌊(𝑇−𝑇𝑠𝑡𝑎𝑟𝑡)∕𝐾⌋
3: for 𝑘= 0 to 𝐾−1 do
4:
𝑇𝑡𝑟𝑎𝑖𝑛_𝑒𝑛𝑑←𝑇𝑠𝑡𝑎𝑟𝑡+ 𝑘× 𝑇𝑓𝑜𝑙𝑑
5:
𝑇𝑡𝑒𝑠𝑡_𝑒𝑛𝑑←𝑇𝑡𝑟𝑎𝑖𝑛_𝑒𝑛𝑑+ 𝑇𝑓𝑜𝑙𝑑
6:
𝑡𝑟𝑎𝑖𝑛←[0 ∶𝑇𝑡𝑟𝑎𝑖𝑛_𝑒𝑛𝑑]
7:
𝑡𝑒𝑠𝑡←[𝑇𝑡𝑟𝑎𝑖𝑛_𝑒𝑛𝑑∶𝑇𝑡𝑒𝑠𝑡_𝑒𝑛𝑑]
8:
Initialize Model 𝑘
9:
Train 𝑘on 𝑡𝑟𝑎𝑖𝑛using AdamW [50] with
Dropout [51]
10:
Generate Predictions ̂𝑌𝑘on 𝑡𝑒𝑠𝑡
11:
Store ̂𝑌𝑘and Ground Truth 𝑌𝑘
12: end for
13: Concatenate all ̂𝑌= [ ̂𝑌0, … , ̂𝑌𝐾−1] return ̂𝑌
Algorithm 2 Vectorised Backtesting Logic
Require: Predictions ̂𝑌, Probabilities 𝑃, Prices 𝑆𝑡, Thresh-
old 𝜏= 0.40
1: 𝐸𝑞𝑢𝑖𝑡𝑦←100, 000, 𝑃𝑜𝑠←0
2: for 𝑡= 1 to 𝑇do
3:
𝑆𝑖𝑔𝑛𝑎𝑙←̂𝑌𝑡, 𝐶𝑜𝑛𝑓←max(𝑃𝑡)
4:
if 𝑃𝑜𝑠== 0 and 𝐶𝑜𝑛𝑓> 𝜏then
5:
if 𝑆𝑖𝑔𝑛𝑎𝑙== Buy then
6:
𝑃𝑜𝑠←1, 𝐸𝑛𝑡𝑟𝑦←𝑆𝑡× (1 + slip)
7:
𝐸𝑞𝑢𝑖𝑡𝑦←𝐸𝑞𝑢𝑖𝑡𝑦−Fee
8:
else if 𝑆𝑖𝑔𝑛𝑎𝑙== Sell then
9:
𝑃𝑜𝑠←−1, 𝐸𝑛𝑡𝑟𝑦←𝑆𝑡× (1 −slip)
10:
𝐸𝑞𝑢𝑖𝑡𝑦←𝐸𝑞𝑢𝑖𝑡𝑦−Fee
11:
end if
12:
else if 𝑃𝑜𝑠≠0 then
13:
if Signal Reversal Condition Met then
14:
𝐸𝑥𝑖𝑡←𝑆𝑡× (1 ∓slip)
15:
𝑃𝑛𝐿←(𝐸𝑥𝑖𝑡−𝐸𝑛𝑡𝑟𝑦) × 𝑃𝑜𝑠× 𝑆𝑖𝑧𝑒
16:
𝐸𝑞𝑢𝑖𝑡𝑦←𝐸𝑞𝑢𝑖𝑡𝑦+ 𝑃𝑛𝐿−Fee
17:
𝑃𝑜𝑠←0
18:
end if
19:
end if
20: end forreturn Equity Curve, Sortino Ratio, Max Draw-
down
5.3. Uncertainty Quantification
To assess the precision of our risk-adjusted metrics, we
compute bootstrap 95% confidence intervals for Sharpe and
Sortino ratios. For each model, we generate 𝑛= 1000
bootstrap samples from the empirical distribution of trade
returns and report the 5th and 95th percentiles of the result-
ing Sharpe and Sortino estimates.
Ahoora Rostamian: Preprint submitted to Elsevier
Page 4 of 11
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6839368
Preprint not peer reviewed


## Page 5

Linear Recurrent versus Convolutional Neural Networks for High-Frequency Cryptocurrency Trading
Table 1
Dataset Characteristics and Dollar Bar Statistics
Feature
XBTUSD
ETHUSD
SOLUSD
Asset Class
Mature / Store of Value
Liquid Utility
Volatile / Altcoin
Dollar Threshold (𝜃)
$10,000
$10,000
$10,000
Total Bars (Approx)
699,299
450,100
320,500
Mean Daily Volatility
2.1%
3.4%
5.8%
Kurtosis (Returns)
4.2
5.8
12.1
6. Experimental Setup
6.1. Dataset Description
The experimental dataset comprises high-frequency tick
data sourced from the Kraken cryptocurrency exchange,
covering three distinct assets selected to represent varying
degrees of market maturity and liquidity.
As shown in Table 1, the assets exhibit significant het-
erogeneity. XBTUSD represents the lowest kurtosis (4.2),
indicating relatively stable price formation. Conversely, SO-
LUSD exhibits leptokurtosis (12.1). This diversity allows us
to test how model performance varies with asset maturity.
6.2. Implementation and Hardware Environment
All experiments were conducted on a single NVIDIA
A100-SXM4 GPU with 40GB of HBM2e memory. The
software stack included PyTorch 2.1 with CUDA 12.1.
6.2.1. Optimisation of Linear RNNs
For a fair comparison between the Python-based min-
RNN implementations and the C++-optimised CuDNN
LSTMs, we utilised ‘torch.compile‘ with ‘reduce-overhead‘
mode. This fix utilises CUDA Graphs to capture the kernel
launch sequence, minimising the CPU overhead associated
with the iterative associative scan operations. Without this
optimisation, minRNNs exhibited a 3× latency penalty due
to Python interpreter overhead; with it, they achieved near-
native performance.
6.3. Baselines and Model Hyperparameters
We compared five distinct architectures, ensuring pa-
rameter counts were comparable ( 200k-500k parameters)
to isolate the effect of architectural inductive bias. The
sequence length hyperparameter was varied across 𝐿∈
{256, 512, 1024}.
• Baseline LSTM: Standard PyTorch ‘nn.LSTM‘ (CuDNN
backend). 2 layers, hidden dimension 256.
• minGRU / minLSTM: Custom implementations us-
ing the parallel associative scan. Expansion factor 1.5,
hidden dimension 256.
• TCN: Temporal Convolutional Network. Kernel size
𝑘= 3, dilations 𝑑∈{1, 2}, no dropout. Effective
Receptive Field ≈7. A variant with dilations {1, 2, 4}
(RF ≈15) was also evaluated.
• Transformer: Encoder-only architecture. 2 layers, 4
heads, dimension 256. Causal masking without ex-
plicit positional encodings.
Table 2
Training Latency (Seconds/Epoch) vs. Sequence Length (𝐿)
on XBTUSD
Model
L=256
L=512
L=1024
Scaling Behaviour
Transformer
4.02
8.70
19.78
Quadratic (𝑂(𝐿2))
minLSTM
1.46
2.63
4.90
Linear (𝑂(𝐿))
minGRU
1.29
2.21
4.00
Linear (𝑂(𝐿))
LSTM (CuDNN)
1.39
2.26
4.16
Linear (𝑂(𝐿))
TCN
0.62
0.98
1.58
Sub-Linear / Optimised
• XGBoost: A gradient-boosted decision tree baseline.
100 estimators, max depth 6. This model does not
process sequences; its performance is invariant to 𝐿,
serving as a “tabular” benchmark.
6.4. Evaluation Metrics
We report a comprehensive suite of metrics:
• Computational: Seconds per Training Epoch (La-
tency), Scaling Factor (𝐿1024∕𝐿256).
• Predictive: Macro F1-Score, Expected Calibration
Error (ECE).
• Economic: Total Return (%), Maximum Drawdown
(%), Sortino Ratio, Sharpe Ratio (with Bootstrap 95%
CIs), number of trades.
• Tail Risk: Distribution of worst-trade losses (in % and
dollars) and their durations (in bars).
7. Results and Discussion
7.1. Computational Scaling Analysis
The primary theoretical motivation for Linear RNNs is
their 𝑂(𝐿) scaling compared to the Transformer’s 𝑂(𝐿2).
Our empirical results strongly validate this theoretical prop-
erty, but with important nuances regarding constant factors.
Table 2 presents training latency on XBTUSD (the most
liquid market; latencies on ETHUSD and SOLUSD were
nearly identical and are omitted for brevity). The scaling
behaviour is illustrated in Figure 1.
7.1.1. The Failure of Transformers
As evidenced by Table 2 and Figure 1, the Transformer
architecture is operationally unviable for high-frequency
retraining loops. At 𝐿= 1024, a single epoch takes nearly
20 seconds. In a live trading context requiring model updates
every few minutes, this latency is prohibitive. The quadratic
growth makes it unsuitable for the long sequences often
necessary in HFT.
7.1.2. TCN Dominance
Surprisingly, the TCN outperformed both the minRNNs
and the optimised LSTM by a factor of roughly 3×. This
suggests that for sequence lengths relevant to market mi-
crostructure (𝐿≤1024), the parallel efficiency of matrix
multiplication (convolution) on GPUs outweighs the theoret-
ical benefits of associative scans. The TCN’s latency scales
Ahoora Rostamian: Preprint submitted to Elsevier
Page 5 of 11
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6839368
Preprint not peer reviewed


## Page 6

Linear Recurrent versus Convolutional Neural Networks for High-Frequency Cryptocurrency Trading
Figure 1: Computational Scaling Analysis on XBTUSD.
Table 3
Macro F1 Score at 𝐿= 1024
Model
XBTUSD
ETHUSD
SOLUSD
LSTM
0.372
0.392
0.350
minGRU
0.391
0.430
0.354
minLSTM
0.377
0.434
0.364
TCN
0.377
0.414
0.350
Transformer
0.357
0.403
0.319
XGBoost
0.363
0.380
0.360
sub-linearly in practice due to high GPU utilisation, making
it the superior choice for latency-critical applications.
7.2. Predictive Performance
Table 3 displays the macro F1 score at 𝐿= 1024
for all three assets. The scores are uniformly low (0.30–
0.43), reflecting the notorious low signal-to-noise ratio of
tick data. minLSTM achieves the highest F1 on ETHUSD
(0.434) and SOLUSD (0.364), while minGRU leads on
XBTUSD (0.391). However, these predictive differences do
not translate linearly into economic returns, as will be seen.
7.3. Economic Performance and Asset
Heterogeneity
The central discovery of this study is that no single
architecture dominates across all assets or sequence lengths.
Table 4 summarises total return and Sortino ratio at 𝐿=
1024, while Figure 2 shows the aggregated equity curves
for XBTUSD as a representative example. To capture the
length dependence, we also highlight results at 𝐿= 512 in
the discussion.
7.3.1. XBTUSD: The Stability Mosaic
On the mature Bitcoin market, all deep learning mod-
els achieved positive returns. The TCN posted the highest
Sortino ratio (0.174) and the smallest maximum drawdown
(−0.86%, see Table 7), confirming its reputation as a sta-
ble risk-adjusted performer. However, in terms of absolute
Table 4
Cross-Asset Economic Performance at 𝐿
=
1024 (Total
Return% / Sortino Ratio)
Model
XBTUSD
ETHUSD
SOLUSD
LSTM
+9.09% / 0.135
+9.84% / 0.109
-17.63% / -0.168
minGRU
+4.11% / 0.097
-5.11% / -0.041
-13.05% / -0.159
minLSTM
+9.52% / 0.152
+16.43% / 0.276
-8.83% / -0.170
TCN
+4.29% / 0.174
-15.67% / -0.144
-8.59% / -0.161
Transformer
+4.99% / 0.144
-10.45% / -0.146
-15.33% / -0.333
XGBoost
+8.71% / 0.125
-52.37% / -0.288
-35.77% / -0.364
return, it was outperformed by LSTM (+9.09%), minL-
STM (+9.52%), and even XGBoost (+8.71%). Notably, at a
shorter sequence length 𝐿= 512, LSTM achieved a remark-
able +12.58% return with a Sortino of 0.159, while TCN
climbed only +7.20% (Sortino 0.209). This suggests that on
Bitcoin, a moderate amount of memory (𝐿= 512) is more
profitable than either extreme locality (TCN) or excessively
long context (𝐿= 1024). The strong performance of XG-
Boost, despite having no temporal reasoning, indicates that
simple non-linear combinations of microstructure features
can be remarkably effective on liquid, efficient markets.
7.3.2. ETHUSD: The Alpha Opportunity
Ethereum showed a clear standout. The minLSTM model
at 𝐿= 1024 achieved a return of +16.43% with a Sortino
ratio of 0.276. However, this performance depends strongly
on the sequence length. When reduced to 𝐿= 512, the return
dropped sharply to +1.45% with a Sortino of 0.016, while at
𝐿= 256 it reached +14.75% with a Sortino of 0.153.
By contrast, the TCN, which relies on shorter memory,
consistently underperformed on ETHUSD, recording a loss
of -15.67% at 𝐿= 1024. It appears unable to capture the
medium-term momentum that benefits the minLSTM. The
Transformer also performed poorly, with a loss of -10.45%.
Overall, for trend-following behaviour in crypto markets,
a gated recurrent model with a sufficiently long input horizon
appears to be necessary.
Ahoora Rostamian: Preprint submitted to Elsevier
Page 6 of 11
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6839368
Preprint not peer reviewed


## Page 7

Linear Recurrent versus Convolutional Neural Networks for High-Frequency Cryptocurrency Trading
Figure 2: Aggregated equity curves, drawdowns, Sortino ratios, and calibration for XBTUSD at 𝐿= 1024.
7.3.3. SOLUSD: The Stress Test
On the highly volatile Solana pair, no model gener-
ated positive returns. minLSTM and TCN limited losses
to roughly -8.6%, while the LSTM lost -17.63% and the
Transformer -15.33%. XGBoost collapsed with -35.77%,
illustrating the danger of applying tabular models without
temporal regularisation to extremely noisy data. The fact
that even the best models failed to profit underlines the
insufficiency of pure microstructure signals in hyper-volatile
altcoins; external features or risk management overlays are
likely required.
7.4. Regime-Dependent Performance
To understand why model rankings invert, we decom-
posed total returns by market regime (Low Volatility, Nor-
mal Volatility, High Volatility) at 𝐿= 1024. Figure 3 shows
the regime return heatmap for ETHUSD, a representative
momentum-driven asset.
On ETHUSD, minLSTM dominates High Volatility
with an impressive +0.82%, explaining its overall out-
performance. In contrast, TCN and Transformer suffer in
the same regime (-0.32% and -0.61%, respectively). On XB-
TUSD, TCN performs best during High Volatility (+0.36%)
and Normal Volatility (+0.15%), while minLSTM excels in
Low Volatility (+0.30%). On SOLUSD, no model profits in
High Volatility; TCN achieves a marginal gain of +0.35% in
High Volatility but is wiped out by other regimes.
Figure 3: Model returns by volatility regime for ETHUSD at
𝐿= 1024.
This regime sensitivity implies that a dynamic trading
system that switches models based on the prevailing volatil-
ity regime could substantially improve profitability.
7.5. Calibration and Threshold Sensitivity
A critical driver of economic performance is probabil-
ity calibration. Table 5 shows that minLSTM achieves the
lowest Expected Calibration Error (ECE = 0.032), followed
by minGRU (0.041). Transformer and XGBoost are over-
confident (ECE 0.067 and 0.089), meaning their predicted
probabilities are poor estimates of the true likelihood.
Ahoora Rostamian: Preprint submitted to Elsevier
Page 7 of 11
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6839368
Preprint not peer reviewed


## Page 8

Linear Recurrent versus Convolutional Neural Networks for High-Frequency Cryptocurrency Trading
Figure 4: Sensitivity of Total Return to Confidence Threshold on ETHUSD (𝐿= 1024).
Table 5
Calibration Error (ECE) at 𝐿= 1024
Model
ECE (Lower is Better)
minLSTM
0.032
minGRU
0.041
LSTM
0.048
TCN
0.055
Transformer
0.067
XGBoost
0.089
This calibration quality translates directly into the stabil-
ity of trading performance under varying confidence thresh-
olds (𝜏). Figure 4 plots the total return on ETHUSD (𝐿=
1024) as 𝜏varies from 0.30 to 0.60. minLSTM and LSTM
exhibit smooth, concave curves with a well-defined optimum
near 𝜏= 0.40, indicating robust probability estimates. In
sharp contrast, XGBoost’s returns swing violently from -
80% to +20%, a hallmark of overconfident and unreliable
predictions. The TCN curve is moderately stable but remains
consistently negative, while the Transformer shows high
sensitivity and erratic behaviour.
7.6. Tail Risk: Worst-Trade Analysis
To further characterise risk, we examine the distribution
of worst trades. Table 6 details the single largest loss per
model on ETHUSD (𝐿= 1024, third fold). While the loss
magnitudes are roughly comparable (12–16%), the durations
differ strikingly. The LSTM held a losing position for 99
Table 6
Anatomy of Worst Trades (ETHUSD, 𝐿= 1024, third fold)
Model
Max Loss %
Duration (bars)
Side
Volatility
LSTM
-14.57%
99
Short
1.31
minGRU
-16.09%
4
Short
2.46
minLSTM
-13.39%
9
Short
1.81
TCN
-14.32%
6
Long
2.02
Transformer
-12.82%
10
Short
1.73
bars, exemplifying the “state persistence” problem where the
memory cell fails to forget a stale regime. minGRU and TCN
exited their worst trades in 4–6 bars; minLSTM held for 9
bars. Across all folds, minLSTM and TCN tend to cut losses
faster than LSTM on average, though occasional extended
drawdowns still occur (e.g., a 76-bar loss for minLSTM in
another fold).
7.7. Uncertainty Quantification
The bootstrap 95% confidence intervals for Sharpe and
Sortino ratios are reported alongside the point estimates
in the Performance Metrics tables (Tables 7–9). On XB-
TUSD, the Sharpe intervals for LSTM, minLSTM, TCN,
and XGBoost overlap substantially, indicating that no model
achieves a statistically significant advantage in risk-adjusted
returns. For example, at 𝐿= 1024, LSTM’s Sharpe 95%
CI is [0.05, 0.16], while TCN’s is [0.02, 0.12], and the two
intervals overlap considerably. On ETHUSD at 𝐿= 1024,
minLSTM’s Sharpe CI ([0.11, 0.28]) does not overlap with
Ahoora Rostamian: Preprint submitted to Elsevier
Page 8 of 11
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6839368
Preprint not peer reviewed


## Page 9

Linear Recurrent versus Convolutional Neural Networks for High-Frequency Cryptocurrency Trading
Table 7
Performance Metrics for XBTUSD, 𝐿= 1024
Model
Return
Max DD
Sortino
Sharpe 95% CI
Trades
LSTM
+9.09%
-1.08%
0.135
[0.05, 0.16]
642
minGRU
+4.11%
-1.39%
0.097
[0.02, 0.22]
414
minLSTM
+9.52%
-1.72%
0.152
[0.07, 0.23]
481
TCN
+4.29%
-0.86%
0.174
[0.02, 0.12]
594
Transformer
+4.99%
-1.42%
0.144
[0.05, 0.16]
830
XGBoost
+8.71%
-1.29%
0.125
[0.07, 0.14]
2012
Table 8
Performance Metrics for ETHUSD, 𝐿= 1024
Model
Return
Max DD
Sortino
Sharpe 95% CI
Trades
LSTM
+9.84%
-4.72%
0.109
[0.02, 0.14]
739
minGRU
-5.11%
-6.80%
-0.041
[−0.10, 0.04]
581
minLSTM
+16.43%
-1.28%
0.276
[0.11, 0.28]
406
TCN
-15.67%
-17.06%
-0.144
[−0.16, −0.04]
883
Transformer
-10.45%
-10.50%
-0.146
[−0.19, −0.03]
449
XGBoost
-52.37%
-52.40%
-0.288
[−0.24, −0.16]
2442
Table 9
Performance Metrics for SOLUSD, 𝐿= 1024
Model
Return
Max DD
Sortino
Sharpe 95% CI
Trades
LSTM
-17.63%
-17.75%
-0.168
[−0.18, −0.11]
2034
minGRU
-13.05%
-13.12%
-0.159
[−0.17, −0.08]
1457
minLSTM
-8.83%
-8.84%
-0.170
[−0.17, −0.06]
1050
TCN
-8.59%
-8.60%
-0.161
[−0.18, −0.05]
942
Transformer
-15.33%
-15.34%
-0.333
[−0.36, −0.23]
990
XGBoost
-35.77%
-35.77%
-0.364
[−0.32, −0.25]
3684
TCN’s ([−0.16, −0.04]), suggesting a meaningful differ-
ence. These bootstrap results mirror the broader economic
findings: no single model unequivocally dominates, and
apparent performance differences are often within sampling
variability.
7.8. Sensitivity to TCN Receptive Field
To check whether the TCN’s performance is limited
by its small receptive field, we evaluated a 3-layer TCN
with dilations {1, 2, 4} (RF ≈15 bars). At 𝐿= 1024 on
XBTUSD, this variant returned +5.12% (Sortino 0.165),
slightly improving on the shallow TCN’s +4.29%, yet still
well below LSTM’s +9.09%. On ETHUSD, the loss reduced
from -15.67% to -12.01%, but remained negative. Thus,
while increasing the receptive field helps somewhat, the
TCN’s fundamental inability to adaptively weight distant
information as an RNN can keeps it from exploiting longer
memory effectively. This confirms that the TCN’s inductive
bias is indeed one of strict locality, which is beneficial only
in certain market conditions.
7.9. Summary of Performance Metrics
For completeness, Tables 7–9 provide the full Perfor-
mance metrics for all assets at 𝐿= 1024.
8. Conclusion and Future Work
This study provides a thorough benchmark of Linear
Recurrent Neural Networks against TCNs, LSTMs, Trans-
formers, and a tree-based baseline on high-frequency cryp-
tocurrency data. Our findings challenge several prevailing
assumptions in the deep learning for finance literature.
8.1. Key Findings
1. Transformers are ill-suited for HFT due to quadratic
scaling, making them impractical for retraining loops.
TCNs offer the lowest latency, 3× faster than min-
RNNs and 15× faster than Transformers.
2. Optimal memory length is asset- and regime-dependent.
On mature, efficient markets (XBTUSD), moderate
memory (LSTM) often yields higher returns than
extreme locality (TCN), though TCN provides supe-
rior tail-risk protection. On momentum-driven assets
(ETHUSD), minLSTM with long context excels. The
“extreme locality” advantage is not universal; it is a
specific property of certain market conditions.
3. The alpha vs. stability trade-off is real. minLSTM
generates the highest returns on ETHUSD (+16.43%)
but its advantage vanishes at shorter lengths. TCN’s
constrained memory yields smoother equity curves on
mature assets but at the cost of missing medium-term
trends.
4. Calibration matters. minLSTM is the best-calibrated
model (ECE 0.032), leading to robust threshold sensi-
tivity. Overconfident models (Transformer, XGBoost)
produce erratic PnL.
5. On highly volatile markets (SOLUSD), no microstructure-
based model profits. This sets a boundary condition
for the application of pure DL-based 𝛼signals.
8.2. Future Directions
Based on the identified arbitrage between stability and
capacity, we propose:
1. Hybrid Architectures: A model combining a shallow
TCN front-end for robust local feature extraction with
a minLSTM layer for adaptive long-range reasoning
could capture the best of both worlds.
2. Dynamic Regime-Aware Ensembling: A meta-controller
that switches between models (or blends their proba-
bilities) based on real-time volatility estimates could
enhance out-of-sample returns.
3. Expanded Feature Set: Incorporating Level-2 order
book data and cross-exchange liquidity metrics would
provide a stricter test of the models’ capacity to handle
higher-dimensional state spaces.
4. Transaction Cost Modelling: Future work should
incorporate volume-dependent slippage and exchange
fee tiers, as trade counts vary widely across models
and impact net profitability.
Ahoora Rostamian: Preprint submitted to Elsevier
Page 9 of 11
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6839368
Preprint not peer reviewed


## Page 10

Linear Recurrent versus Convolutional Neural Networks for High-Frequency Cryptocurrency Trading
References
[1] L. Feng, F. Tung, M. O. Ahmed, H. Hajimirsadeghi, Y. Ben-
gio, and P. Vicol, “Were RNNs all we needed?,” arXiv preprint
arXiv:2410.01201, 2024.
[2] A. Gu and T. Dao, “Mamba: Linear-time sequence modeling with
selective state spaces,” in Proc. First Conf. Language Modeling, 2024.
[3] T. Dao and A. Gu, “Transformers are SSMs: Generalized models
and efficient algorithms through structured state space duality,” arXiv
preprint arXiv:2405.21060, 2024.
[4] M. Beck, K. Pöppel, M. Giglio, A. Lucchi, and S. Hochre-
iter, “xLSTM: Extended long short-term memory,” arXiv preprint
arXiv:2405.04517, 2024.
[5] Z. Zhang, B. Lim, and S. Zohren, “Deep learning for market by order
data,” Appl. Math. Finance, vol. 28, no. 1, pp. 79–95, 2021.
[6] A. Briola, S. Bartolucci, and T. Aste, “HLOB–Information persis-
tence and structure in limit order books,” J. Financ. Econom., vol.
23, no. 1, pp. 45–72, 2025.
[7] L. Lucchese, M. S. Pakkanen, and A. E. D. Veraart, “The short-
term predictability of returns in order book markets: A deep learning
perspective,” Int. J. Forecast., vol. 40, no. 4, pp. 1587–1621, 2024.
[8] I. C. Martin, S. Mukherjee, and J. Vanschoren, “Evolving machine
learning: A survey on concept drift and real-time adaptation,” arXiv
preprint arXiv:2505.17902, 2025.
[9] S. Patil, R. Kumar, and A. Singh, “Artificial intelligence for high-
frequency risk assessment,” J. Risk Financ. Manag., vol. 18, no. 2,
pp. 102–125, 2025.
[10] W. Merrill, J. Petty, and A. Sabharwal, “The illusion of state in state-
space models,” arXiv preprint arXiv:2404.08819, 2024.
[11] A. De Marinis, N. Guglielmi, and S. Sicilia, “Improving the ro-
bustness of neural ODEs with minimal weight perturbation,” arXiv
preprint arXiv:2501.10740, 2025.
[12] X. Cai, Y. Zhu, X. Wang, and Y. Yao, “MambaTS: Selective state
space models for long-term time series forecasting,” arXiv preprint
arXiv:2401.01234, 2024.
[13] J. Peng, M. Yang, Q. Zhang, and X. Li, “S4M: S4 for multivari-
ate time series forecasting with missing values,” arXiv preprint
arXiv:2503.00900, 2025.
[14] H. Mo and S. Ouyang, “(Generative) AI in financial economics,” J.
Chin. Econ. Bus. Stud., vol. 23, no. 4, pp. 509–587, 2025.
[15] F. Bastianello, P. Decaire, and M. Guenzel, “Mental models and
financial forecasts,” 2024.
[16] A. Zeng, M. Chen, L. Zhang, and Q. Xu, “Are transformers effective
for time series forecasting?,” in Proc. AAAI, 2023, pp. 11121–11128.
[17] H. Guo, J. Lin, and F. Huang, “Multi-stream sequence learning with
gated linear recurrent units,” in OpenReview, 2025.
[18] S. Gupta and P. Kumar, “Gated recurrent units for volatility forecast-
ing in cryptocurrency,” Finance Res. Lett., vol. 47, p. 102712, 2022.
[19] R. Fritschek and R. Schaefer, “MinGRU-based encoder for turbo
autoencoder frameworks,” arXiv preprint arXiv:2503.08451, 2025.
[20] H. Wang, “Exploring microstructural dynamics in cryptocurrency
limit order books,” arXiv preprint arXiv:2506.05764, 2025.
[21] M. Shaffer and C. C. Y. Wang, “Scaling core earnings measurement
with large language models,” 2024.
[22] H. C. Bhanujyothi and I. J. Jacob, “Hybrid RNN-CNN model for
predicting stock market trends,” in Proc. 2024 1st Int. Conf. Adv.
Comput., Commun. Netw. (ICAC2N), 2024, pp. 1855–1860.
[23] Y. Wu, M. Mahfouz, D. Magazzeni, and M. Veloso, “Towards robust
representations of limit orders books for deep learning models,” SSRN
Electron. J., 2021.
[24] F. Danieli, P. Rodriguez, M. Sarabia, X. Suau, and L. Zappella,
“ParaRNN: Unlocking parallel training of nonlinear RNNs for large
language models,” arXiv preprint arXiv:2510.21450, 2025.
[25] O. A. Mahdi, E. Pardede, S. Bevinakoppa, and N. Ali, “Federated
learning under concept drift: A systematic survey of foundations,
innovations, and future research directions,” Electronics, vol. 14, no.
22, Art. no. 4480, 2025.
[26] Z. Zhang and S. Zohren, “Multi-horizon forecasting for limit order
books: Novel deep learning approaches and hardware acceleration
using intelligent processing units,” arXiv preprint arXiv:2105.10430,
2021.
[27] M. A. Ahamed and Q. Cheng, “TimeMachine: A time series is worth
4 Mambas for long-term forecasting,” in Proc. 27th Eur. Conf. Artif.
Intell. (ECAI), Santiago de Compostela, Spain, 2024, pp. 1688–1695.
[28] E. Eldele, M. Ragab, Z. Chen, M. Wu, and X. Li, “TSLANet:
Rethinking transformers for time series representation learning,” in
Proc. Int. Conf. Mach. Learn. (ICML), 2024.
[29] P. Mironowicz and Y. Cao, “Quantum machine learning for high-
frequency risk management,” in Proc. Atlantis Press, 2025.
[30] M. López de Prado, Advances in Financial Machine Learning. Hobo-
ken, NJ, USA: Wiley, 2018.
[31] R. Cont, A. Kukanov, and S. Stoikov, “The price impact of order book
events,” J. Financ. Econom., vol. 12, no. 1, pp. 47–88, 2014.
[32] M. D. Gould, M. A. Porter, S. Williams, M. McDonald, D. J. Fenn,
and S. D. Howison, “Limit order books,” Quant. Finance, vol. 13, no.
11, pp. 1709–1742, 2013.
[33] J.-P. Bouchaud, M. Mézard, and M. Potters, “Statistical properties of
stock order books: empirical results and models,” Quant. Finance, vol.
2, no. 4, pp. 251–256, 2002.
[34] Á. Cartea, S. Jaimungal, and J. Penalva, Algorithmic and High-
Frequency Trading. Cambridge, U.K.: Cambridge Univ. Press, 2015.
[35] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” Neural
Comput., vol. 9, no. 8, pp. 1735–1780, 1997.
[36] A. Vaswani et al., “Attention is all you need,” in Proc. Adv. Neural Inf.
Process. Syst. (NeurIPS), 2017, pp. 5998–6008.
[37] S. Bai, J. Z. Kolter, and V. Koltun, “An empirical evaluation of generic
convolutional and recurrent networks for sequence modeling,” arXiv
preprint arXiv:1803.01271, 2018.
[38] A. Gu, K. Goel, and C. Ré, “Efficiently modeling long sequences with
structured state spaces,” in Proc. Int. Conf. Learn. Represent. (ICLR),
2022.
[39] C. Lea, M. D. Flynn, R. Vidal, A. Reiter, and G. D. Hager, “Temporal
convolutional networks for action segmentation and detection,” in
Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), 2017, pp.
156–165.
[40] T. Dao, D. Y. Fu, S. Ermon, A. Rudra, and C. Ré, “FlashAttention:
Fast and memory-efficient exact attention with IO-awareness,” in
Proc. Adv. Neural Inf. Process. Syst. (NeurIPS), 2022.
[41] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image
recognition,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit.
(CVPR), 2016, pp. 770–778.
[42] R. Pascanu, T. Mikolov, and Y. Bengio, “On the difficulty of training
recurrent neural networks,” in Proc. Int. Conf. Mach. Learn. (ICML),
2013, pp. 1310–1318.
[43] Y. Bengio, P. Simard, and P. Frasconi, “Learning long-term depen-
dencies with gradient descent is difficult,” IEEE Trans. Neural Netw.,
vol. 5, no. 2, pp. 157–166, 1994.
[44] T. Fischer and C. Krauss, “Deep learning with long short-term mem-
ory networks for financial market predictions,” Eur. J. Oper. Res., vol.
270, no. 2, pp. 654–669, 2018.
[45] H. Zhou et al., “Informer: Beyond efficient transformer for long
sequence time-series forecasting,” in Proc. AAAI Conf. Artif. Intell.,
2021, pp. 11106–11115.
[46] B. Lim and S. Zohren, “Time-series forecasting with deep learning:
A survey,” Phil. Trans. R. Soc. A, vol. 379, no. 2194, p. 20200209,
2021.
[47] J. Sirignano and R. Cont, “Universal features of price formation
in financial markets: Perspectives from deep learning,” in Machine
Learning and AI in Finance, 1st ed. Routledge, 2021, p. 11.
[48] A. Borovykh, S. Bohte, and C. W. Oosterlee, “Conditional time
series forecasting with convolutional neural networks,” arXiv preprint
arXiv:1703.04691, 2017.
[49] D. R. Aronson, Evidence-Based Technical Analysis: Applying the Sci-
entific Method and Statistical Inference to Trading Signals. Hoboken,
NJ, USA: Wiley, 2011.
[50] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimiza-
tion,” in Proc. Int. Conf. Learn. Represent. (ICLR), 2014.
Ahoora Rostamian: Preprint submitted to Elsevier
Page 10 of 11
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6839368
Preprint not peer reviewed


## Page 11

Linear Recurrent versus Convolutional Neural Networks for High-Frequency Cryptocurrency Trading
[51] N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, and R.
Salakhutdinov, “Dropout: A simple way to prevent neural networks
from overfitting,” J. Mach. Learn. Res., vol. 15, pp. 1929–1958, 2014.
[52] F. Chollet, “Xception: Deep learning with depthwise separable convo-
lutions,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR),
2017, pp. 1251–1258.
[53] T. Brown et al., “Language models are few-shot learners,” in Proc.
Adv. Neural Inf. Process. Syst. (NeurIPS), 2020, pp. 1877–1901.
Ahoora Rostamian: Preprint submitted to Elsevier
Page 11 of 11
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6839368
Preprint not peer reviewed


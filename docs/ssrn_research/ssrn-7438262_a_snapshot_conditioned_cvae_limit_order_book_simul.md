# A Snapshot-Conditioned CVAE Limit Order Book Simulator: Evidence from

- **Source File**: `ssrn-7438262.pdf`
- **Total Pages**: 20
- **SSRN ID**: `ssrn-7438262`

---

## Page 1

A Snapshot-Conditioned CVAE Limit Order Book Simulator: Evidence from
Canadian Equities
Ange Francis Zegbeh N’guessana, Fabian Bastina
aDepartment of Computer Science and Operations Research, University of Montreal, Montreal, Quebec, Canada
Abstract
Testing algorithmic trading strategies in production carries substantial risk of market disruption, yet passive
historical replay cannot capture the market’s reaction to an agent’s actions.
We propose a reactive limit
order book (LOB) simulator based on a Conditional Variational Autoencoder (CVAE) coupled with an LSTM
module that conditions generation on the ten most recent book snapshots. The model operates directly on
state transitions signed, normalized depth vectors at three bid and ask levels rather than on heterogeneous
order-by-order events, yielding a compact and homogeneous learning target. We train and evaluate on Toronto
Stock Exchange (TSX) equity data, a market underrepresented in the simulation literature. The simulator
reproduces key stylized facts: marginal queue distributions, the characteristic LOB smile in average quantities,
level-to-level correlations, and realistic price paths—while exhibiting reactive price impact for both liquidity
taking and provision, with the concave size-impact relationship qualitatively consistent with the literature.
Benchmarked against a Conditional Wasserstein GAN with gradient penalty trained on the same data, the
CVAE achieves superior queue-level fidelity and inter-level correlation structure with a simpler, single-network
ELBO objective that requires neither gradient-penalty tuning nor critic-iteration scheduling, at the cost of a
higher marginal KL divergence on the more liquid of the two stocks studied.
To the best of our knowledge,
this snapshot-conditioned CVAE+LSTM simulator is the first of its kind applied to Canadian equities, offering
reactive synthetic environments for execution and market-making research.
1. Introduction
A realistic simulator should understand and reproduce the stylized facts of the limit order book (LOB) so
that trading strategies can be tested in a reactive environment rather than in passive market replay, which does
not respond to an agent’s actions (Coletta et al., 2023; Jain et al., 2024). Such reactivity reduces reliance on risky
production testing, avoiding flash-crash–like behavior, missed opportunities, or unintended market impact—and
supports scenario exploration even under evolving regulations. As emphasized in authoritative surveys, there
remains a persistent gap between empirical stylized facts and many existing models (Gould et al., 2013; Jain
et al., 2024).
From the early developments in econophysics and order-driven models (e.g., Mike and Farmer (2008) and even
before 2000 Bak et al. (1997)) aimed at reproducing stylized facts, research evolved toward tractable queueing
approaches—most notably Markovian LOB models where market, limit, and cancel flows are represented through
point processes, enabling analytic characterization of durations, autocorrelations, and diffusion limits (Cont
et al., 2010; Cont and de Larrard, 2013). A key refinement, the queue-reactive model, conditions event intensities
on the book state and has become a practical baseline for simulation and execution-cost analysis (Huang et al.,
2015; Bodor and Carlier, 2025), though independent arrivals and simplified queue dynamics limit representation
of clustered activity and herding.
To address these shortcomings, Hawkes-based models introduced self- and cross-excitation to capture cluster-
ing in order flow; later high-dimensional and marked versions incorporated volume, side, and level information,
while recent work couples Neural Hawkes or LSTM embeddings to simulate event-driven LOB dynamics within
deep-RL market-making frameworks (Abergel and Jedidi, 2015; Lu and Abergel, 2018; Chung et al., 2024;
Email addresses: ange.francis.zegbeh.nguessan@umontreal.ca (Ange Francis Zegbeh N’guessan),
bastin@iro.umontreal.ca (Fabian Bastin)
1


## Page 2

Lalor and Swishchuk, 2025). Yet despite these advances, Hawkes models often struggle to represent strategic
interaction among heterogeneous agents.
Agent-based modeling (ABM) emerged partly in response, offering interpretability and explicit behavioral
mechanisms. Byrd et al. introduced ABIDES, a high-fidelity NASDAQ-style simulator (ITCH/OUCH) that
enables reactive experiments at scale, though models like Preis et al. (2006) had already differentiated liquidity
providers from takers.
More recent hybrid approaches combine neural point processes or diffusion models
with ABIDES-like infrastructures to preserve stylized facts while enabling strategic agent interaction (Shi and
Cartlidge, 2024), though such approaches may require heavy calibration and often lack the statistical efficiency
of deep generative models.
Deep learning and generative modeling further bridge realism and controllability: CNN/LSTM architectures
such as DeepLOB capture spatial–temporal LOB structure, while RNN-based generative models reproduce
transitions (type, price level, size, delay). Conditional GANs and transformers enhance reactivity, robustness,
and short-horizon forecasting (Zhang et al., 2019; Hultin et al., 2023; Coletta et al., 2023; Xiao et al.). These
developments complement queueing and Hawkes foundations and have become common baselines, supported by
progress in scalable computation.
Much of the literature models events (limit, market, cancellation), sampling inter-event times and attributes
order-by-order, yielding heterogeneous outputs that mix categorical order types, discrete prices, and continuous
quantities/interarrival times. An alternative is to generate the next LOB snapshot directly, structuring inputs
and outputs around state transitions between book states. This homogenizes the learning target, simplifies
evaluation against stylized facts, and integrates naturally with execution modules.
We propose a snapshot-conditioned generative simulator of the limit order book. Rather than modelling
order-by-order events, we represent the book state as a signed, normalised depth vector at the top k bid and
ask levels, xt = (Bk, . . . , B1, A1, . . . , Ak) ∈R2k, and learn a generative model of the state transition xt →xt+∆;
this homogenises the learning target, removes the need to handle heterogeneous output types, and integrates
naturally with execution and market-making modules. On top of this representation we couple a Conditional
VAE (Kingma and Welling, 2014; Sohn et al., 2015) with a single-layer LSTM (Hochreiter and Schmidhuber,
1997) that summarises the h most recent snapshots into a history embedding, from which the decoder samples the
next snapshot. Training maximises a β-weighted ELBO with a per-sample reconstruction weight that upweights
the comparatively rare price-change events, and an ablation over the conditioning horizon h ∈{1, 2, 4, 10, 20}
confirms the importance of temporal context.
We evaluate the simulator on two Toronto Stock Exchange equities, BMO and Telus, chosen to represent
contrasting liquidity regimes. It reproduces four key stylised facts—marginal queue distributions, the average-
quantity smile, level-to-level correlations, and realistic price paths—and exhibits reactive price impact findings
for both liquidity taking and provision. We further benchmark it against a Conditional WGAN-GP trained on
the same data and given the same conditioning input, and characterise the resulting trade-off explicitly: the
adversarial model attains a lower marginal KL divergence on BMO (0.054 vs. 0.143), whereas the CVAE attains
a lower queue error (BMO: 34.1 vs. 55.3; Telus: 52.8 vs. 162.5) and a better correlation fidelity (BMO: 0.34
vs. 0.44; Telus: 0.25 vs. 0.71 stock units) under an objective that requires neither gradient-penalty tuning nor
critic-iteration scheduling.
The novelty we claim rests on the gap identified above and is twofold. First, the deep generative simulators
closest to ours—RNN- and GAN-based conditional generators (Hultin et al., 2023; Coletta et al., 2023; Cont
et al., 2023)—generate order-by-order event streams, with the heterogeneous output space this entails; modelling
the state transition itself on a fixed price grid, conditioned on an LSTM summary of the recent snapshot history,
is to the best of our knowledge untried in this literature.
Second, that literature is calibrated on US and
European venues, leaving Canadian equities unexamined despite a large-tick regime and thinner books that
make the snapshot representation particularly natural.
The remainder of the paper is organised as follows. Section 2 introduces the limit order book, the centred
snapshot representation and its state transitions, and the CVAE+LSTM architecture. Section 3 presents the
weighted β-ELBO training objective.
Section 4 describes the TSX data and the model configuration, and
Section 5 reports the stylised facts together with the reactivity experiments. Section 6 benchmarks the simulator
against the Conditional WGAN-GP, Section 7 quantifies the contribution of the conditioning horizon, and
Section 8 concludes and outlines directions for future work.
2


## Page 3

2. Model
2.1. Limit Order Book (LOB) Overview
A limit order book is a centralised record of outstanding buy and sell interest in a financial instrument
at discrete price levels. Buy orders, which express a willingness to acquire the instrument, are stored on the
bid side, while sell orders, expressing a willingness to dispose of it, are stored on the ask (or offer) side. The
mechanism governing execution follows a price–time priority rule: among all pending orders, the highest bid
and lowest ask receive priority, and ties at the same price are broken according to the time of arrival in a
First-In-First-Out fashion. Table 1, inspired from the TSX Market Making Program Guide (?), illustrates a
typical book state with four visible levels on each side.
Table 1: Illustration of LOB state
Bid
Ask
Level
Qty
Price
Level
Qty
Price
L1
300
10.19
L1
50
10.22
L2
200
10.18
L2
500
10.23
L3
400
10.17
L3
300
10.24
L4
500
10.16
L4
200
10.25
In this example, the bid–ask spread—defined as the difference between the best ask and the best bid—is
10.22−10.19 = 0.03, and the mid-price, computed as the average of the two best quotes, is 10.205. The evolution
of the book is driven by three fundamental event types:
• Market order: a market order requests immediate execution at the best available opposite quote. It
guarantees execution but offers no control over the price obtained. When the order size exceeds the quantity
available at the best price, the residual fills against deeper levels, consuming liquidity and potentially
shifting the best quote—a phenomenon known as market impact.
• Limit order: a limit order specifies both a price and a quantity at which the participant is willing to
trade. If the specified price crosses the opposite best quote, the order triggers an immediate transaction;
if it falls inside the spread, it improves the best displayed price; otherwise, it rests passively in the book
at the designated level, awaiting a future counterparty.
• Cancellation: a cancellation removes a previously submitted limit order from the book. Participants
frequently cancel and re-submit orders to reposition themselves at more favourable price levels or to
manage inventory risk.
When an incoming order consumes liquidity across one or more price levels, the resulting shift in the mid-
price is termed market impact; its magnitude depends on the order size relative to the available depth at each
level (Farmer et al., 2005). Prices, however, do not move continuously: they evolve on a discrete grid whose
minimum increment—the tick size—is set by market regulation. In Canadian and US equity markets, the tick
size is δ = 0.01.
Building on the standard event-based representation of electronic markets, we model each limit order as a
triplet x = (t, p, q), where t ∈R denotes the order submission time, p ∈δN denotes the limit price expressed on
the discrete price grid induced by the tick size δ > 0, and q ∈Z \ {0} denotes the signed order quantity. By
convention, q > 0 corresponds to an ask (sell) order, while q < 0 corresponds to a bid (buy) order.
Let L denote the limit order book (LOB), understood as the collection of all active limit orders that have
been submitted but not yet fully executed or cancelled. For any t ∈R+, we denote by L(t) the complete state
of the LOB at time t.
2.1.1. Queue Size and Best Prices
For any price level p ∈δN and time t, the aggregate queue size at price p is defined as
Qp(t) =
X
x∈Lp(t)
qx,
3


## Page 4

where
Lp(t) = {x ∈L(t) : px = p}
denotes the set of all outstanding orders posted at price p at time t.
Positive queue sizes correspond to sell-side liquidity, while negative queue sizes correspond to buy-side
liquidity. The prevailing best ask and best bid prices are defined respectively as
pa(t) = inf{p ∈δN : Qp(t) > 0},
pb(t) = sup{p ∈δN : Qp(t) < 0}.
The mid-price is then given by
pmid(t) = pa(t) + pb(t)
2
.
By construction, the bid–ask spread is strictly positive, so that pa(t) > pb(t) for all t at which the market is
well defined.
2.1.2. Centered Limit Order Book Snapshot
To obtain a finite-dimensional representation of the LOB, we consider a symmetric price grid of length 2k
whose lowest level p is the best bid minus (k −1) ticks—equivalently, the deepest bid price in the window.
Under the assumption of a one-tick spread, the grid is centred on the mid-price p + (k −1
2)δ. Specifically, the
grid consists of the price levels
p, p + δ, p + 2δ, . . . , p + (2k −1)δ.
The centered LOB snapshot at time t is defined as the vector
Xt =
 Qp(t), . . . , Qp+(k−1)δ(t), Qp+kδ(t), . . . , Qp+(2k−1)δ(t)

.
The grid is chosen such that the first k components correspond to bid-side queues and the remaining k
components correspond to ask-side queues. Consequently, we impose the sign constraints
Qp+iδ(t) ≤0
for all i ∈{0, . . . , k −1},
Qp+iδ(t) ≥0
for all i ∈{k, . . . , 2k −1}.
Under this construction, the best bid queue corresponds to
Qp+(k−1)δ(t),
while the best ask queue corresponds to
Qp+kδ(t).
Throughout the analysis, and in line with common assumptions for large-tick assets, we assume that queues
at the best bid and best ask prices are never empty. This ensures that the bid–ask spread remains well defined
at all times. It is important to point out that it is assumed that no gap other than the tick size exists between
the price levels.
2.1.3. State Transitions
Market participants’ actions, namely submissions, cancellations, and executions of limit orders are discrete
events in continuous time.
Their cumulative effect over some appropriate time span ∆t may be viewed as
a continuous transition of the queue sizes from state Xt to Xt+∆t. Rather than simulating individual order
arrivals, we model directly the distribution of the centered order book state at time t + ∆t. Crucially, the price
grid (p, p + δ, . . . , p + (2k −1)δ) remains fixed; price movements are encoded through sign changes in the queue
sizes. The future LOB snapshot on this fixed grid takes one of the following three forms.
No price change.. If neither the best bid nor the best ask price changes during (t, t + ∆t), the reference price
remains fixed. In this case, the state transition affects only the queue sizes, yielding:
Xt+∆t =

Qp(t + ∆t), . . . , Qp+(k−1)δ(t + ∆t)
|
{z
}
≤0 →bid−−−
, Qp+kδ(t + ∆t), . . . , Qp+(2k−1)δ(t + ∆t)
|
{z
}
≥0 →ask+++

.
4


## Page 5

Price decrease.. For a price decrease, one or more bid queues must turn positive, thereby becoming ask queues.
The reference price shifts downward by δ. The centered representation is updated accordingly, resulting in. For
k = 3 the resulting snapshot reads
Xt+∆t =

Qp(t + ∆t), Qp+δ(t + ∆t)
|
{z
}
≤0 →bid−−
, Qp+2δ(t + ∆t), Qp+3δ(t + ∆t), Qp+4δ(t + ∆t), Qp+5δ(t + ∆t)
|
{z
}
≥0 →ask++++

.
Similarly, a price decrease of m ≤k ticks is induced by m former bid quantities flipping their sign.
Price increase.. Symmetrically, for a price increase one or more ask queues must turn negative, thereby becoming
bid queues. A one-tick price increase requires Qp+kδ(t + ∆t) < 0. For k = 3 the snapshot becomes
Xt+∆t =

Qp(t + ∆t), Qp+δ(t + ∆t), Qp+2δ(t + ∆t), Qp+3δ(t + ∆t)
|
{z
}
≤0 →bid−−−−
, Qp+4δ(t + ∆t), Qp+5δ(t + ∆t)
|
{z
}
≥0 →ask++

.
A price increase of m ticks corresponds to m former ask quantities turning negative. Note that the subscripts
are identical in all three cases because the grid does not shift; the three scenarios differ only in how the sign
partition divides the vector.
The advantage of this fixed-grid representation is that price changes are inherently encoded in the sign
structure of the snapshot vector, without introducing an additional discrete price-change variable. For large-
tick stocks, price changes are discrete and generally span only a few ticks for an appropriate ∆t, since typically
only a small number of queues get depleted and refilled on the opposite side. At most k price changes during
∆t can be represented, so k and ∆t should be chosen to match the characteristics of each stock. For small-tick
stocks, one may consider binning several levels into a single one. This yields a compact, homogeneous learning
target that integrates naturally with the sequential LSTM architecture described in the following subsection.
Grid re-centring during trajectory generation.. The training data is constructed from a wider book window
(typically 4k levels) by selecting, at each timestamp, the k levels nearest the current mid-price. Consequently,
a price-change snapshot—exhibiting a non-balanced sign partition such as (k−m)/(k+m)—is immediately fol-
lowed in the dataset by a snapshot re-centred on the new mid-price, restoring the canonical k/k partition. Since
the conditioning sequences seen during training contain these sign-flip-then-rebalance transitions, the model
learns to produce appropriately centred outputs after receiving a price-change input; no explicit post-processing
is required during autoregressive generation. The representation can accommodate at most k consecutive same-
direction moves within a single conditioning window; for the stocks and time scale studied (∆t = 1 s), this limit
is never reached in practice.
2.1.4. Distribution
The next LOB state is a random variable whose distribution is conditional on the recent state history
Xt, Xt−∆t, . . . , Xt−h∆t, denoted St = (Xt−h∆t, . . . , Xt−∆t, Xt):
Xt+∆t|St ∼Pr(xt+∆t|st).
We model this conditional distribution using a Conditional Variational AutoEncoder (CVAE) (Kingma and
Welling, 2014; Sohn et al., 2015), for three complementary reasons. First, the CVAE is trained by maximising
a single scalar objective derived from the evidence lower bound (ELBO), avoiding the min–max saddle-point
optimisation of GANs and the associated training instabilities such as mode collapse and sensitivity to critic-
iteration scheduling.
.
Second, the stochastic latent variable z allows the model to represent the inherent
multimodality of LOB transitions: the same history St can plausibly evolve into qualitatively distinct next
states depending on unobserved order flow, and sampling different values of z from the learned prior recovers
this diversity without requiring explicit mixture components. Third, the conditional encoder–decoder structure
of the CVAE integrates naturally with the LSTM-derived history embedding ht = LSTM(St): the embedding is
passed as the conditioning variable y, so the single-network architecture requires neither a critic nor alternating
training schedules. The standard VAE learns a probabilistic mapping from a data space x to a latent space z,
where both the encoder and decoder are parameterized by neural networks. The goal of the VAE is to maximize
the marginal likelihood p(x), which can be expressed as
p(x) =
Z
p(x | z)p(z) dz.
5


## Page 6

However, directly computing this marginal is intractable, so we use the variational approximation
q(z | x) ≈p(z | x).
Thus, the VAE objective function becomes the Evidence Lower Bound (ELBO):
L(θ, ϕ; x) = Eq(z|x) [log p(x | z)] −DKL (q(z | x) ∥p(z)) ,
where q(z | x) is the variational posterior, p(x | z) is the likelihood (decoder), p(z) is the prior (typically a
standard Gaussian), and DKL is the Kullback–Leibler divergence between the variational posterior and the
prior.
In a Conditional VAE, we extend the VAE framework by conditioning the model on some external information
y. This allows the model to generate data that is dependent on y, for example, generating images given class
labels. The encoder produces a distribution q(z | x, y), while the decoder produces p(x | z, y).
Thus, the
conditional VAE objective becomes
L(θ, ϕ; x, y) = Eq(z|x,y)[log p(x | z, y)] −DKL (q(z | x, y) ∥p(z | y)) ,
where q(z | x, y) is the conditional posterior, p(x | z, y) is the conditional likelihood, and p(z | y) is the prior
conditioned on the external information. Both encoder and decoder are parameterised by neural networks.
2.2. LSTM
Volatility clustering refers to the long memory of absolute or squared mid-price returns and means that
large changes in price tend to follow other large price changes. Bouchaud et al. (2002) explain this finding
by the arrival of publicly available news which leads traders to perform similar actions on a short timescale.
This feature of limit order books motivates the use of self- and cross-exciting processes such as the Hawkes
model. One measure commonly used to characterise long memory is the Hurst exponent H: for the stationary
increments Xt of a long-memory process with H ∈( 1
2, 1), the autocorrelation decays as
ρ(τ) = Corr(Xt, Xt+τ) ∼c τ 2H−2.
Long memory is also observed in limit order book snapshots, as illustrated by the 1-second bid queue partial
autocorrelation at a 95 percent confidence level in Figure 1.
Queue sizes at individual price levels exhibit significant serial dependence: depth added or removed at one
timestamp is strongly predictive of depth at subsequent timestamps, reflecting the persistence of limit-order
placement and cancellation activity.
Figure 1 displays the partial autocorrelation function (PACF) of the
best-bid queue at one-second resolution, showing statistically significant coefficients well beyond lag 1. This
establishes that a first-order Markov model—conditioning only on the most recent snapshot—cannot capture
the serial structure of the queue process, and motivates conditioning on a window of h > 1 past snapshots.
The choice of h is a practical compromise between representational capacity and computational cost, and
a sensitivity analysis over h is provided in the ablation study (Section 7). Several ways of dealing with long
memory exist, for instance ARMA-related models (ARIMA, SARIMA), exponential smoothing, and Kalman
filtering (Kalman, 1960). On the deep learning front, one of the most renowned architectures for sequential
data is the LSTM. The gated mechanism allows the network to selectively forget or retain information along
the sequence. Other models include the gated recurrent unit (Chung et al., 2014), which is mathematically
similar to the LSTM but with fewer parameters, the attention-based Transformer, which captures long-range
dependencies through self-attention, and the Temporal Convolutional Network (Lea et al., 2017), which uses
dilated convolutions. We adopt the LSTM (Hochreiter and Schmidhuber, 1997) for its proven ability to capture
long-range dependencies in sequential financial data (Zhang et al., 2019). Through its gated cell mechanism,
the LSTM processes the history sequence St and produces a fixed-length hidden state
ht = LSTM(St),
which serves as the history embedding passed to the CVAE encoder and decoder, in both cases by concatenation
with their respective inputs—the snapshot xt on the encoder side, the sampled latent vector zt on the decoder
side; we refer the reader to Hochreiter and Schmidhuber (1997) for the full gating equations.
6


## Page 7

Figure 1: Partial Autocorrelation function - first level bid queue
3. Training Objective
Another compelling variation of the Variational Autoencoder (VAE) introduces a hyperparameter that ex-
plicitly balances the trade-off between the reconstruction loss and the Kullback-Leibler (KL) divergence term in
the objective function. By adjusting this hyperparameter, the model gains greater flexibility during the learning
process, allowing practitioners to fine-tune how strongly the latent space is regularized versus how accurately
the input is reconstructed Higgins et al. 2017.
With this modification, the standard VAE loss function is reformulated as
L = Eqϕ(z|x) [log pθ(x|z)] −β · DKL (qϕ(z|x) ∥p(z)) ,
where β is the newly introduced hyperparameter controlling the relative importance of the KL divergence term.
The data, after normalization, tends to be centered around the zero axis, with the majority of the mass
concentrated on the positive side for ask queues and the negative side for bid queues. Smaller clusters of mass
correspond to price changes occurring between consecutive snapshots. These events, while relatively rare, are
significant and their magnitude depends on the rate of price fluctuations per timestep.
To better capture and emphasize these rare but important events during training, the VAE objective can be
modified to penalize reconstruction errors more heavily for inputs associated with price changes. The adjusted
loss function is expressed as
L = Eqϕ(z|x)[w(x) · log pθ(x|z)] −β · DKL (qϕ(z|x) ∥p(z)) ,
(1)
where w(x) is a sample-dependent weighting function, set to wc > 1 for snapshots corresponding to price
changes and to 1 otherwise, so that reconstruction errors on these rare events are penalised more heavily; β
controls the strength of the KL-divergence regularization, balancing reconstruction fidelity against latent space
regularization; qϕ(z|x) denotes the approximate posterior; and pθ(x|z) is the likelihood (decoder) model.
By assigning a higher weight to the rare price-changing samples, the VAE is encouraged to model these
important transitions with greater accuracy. This methodology is inspired from Chawla et al. (2002).
4. Numerical experiments
4.1. Data
We use Canadian equity market data centered around the year 2016. This choice is motivated by the limited
availability of limit order book (LOB) data, which is generally difficult to access and not readily obtainable
through public online sources. Despite that, the dataset remains comprehensive and sufficiently rich in mi-
crostructure information, providing meaningful insights into order flow dynamics and market behavior. The
LOB is preprocessed and represented as a sequence of fixed-lag 1-second snapshots, each snapshot encoded as
a signed, normalized depth vector at the top three bid and ask levels,
xt = (B3t, B2t, B1t, A1t, A2t, A3t) ∈R6,
7


## Page 8

with bids negative and asks positive as presented earlier. The snapshot methodology (as opposed to order-by-
order simulation) treats order characteristics and inter-arrival times as implicit in the state transition xt →
xt+∆, significantly reducing dimensionality and yielding a homogeneous learning target focused on book-state
dynamics.
Following the snapshot construction described in the simulator deck, each trading day is reduced to an
effective window by clipping the first and last 30 minutes of trading, yielding approximately 5.5 hours per
day.
This choice avoids mixing distinct microstructure regimes typically observed near the open and close.
Excluding the opening and closing half-hours is standard practice in the empirical microstructure literature: the
call-auction mechanisms at open and close, elevated adverse selection immediately after the open, and end-of-day
inventory rebalancing at the close generate order-flow and volatility patterns that are qualitatively distinct from
the continuous intraday session (Gould et al., 2013; Cont et al., 2010; Huang et al., 2015).
The snapshot-based
approach highlights a limitation at sub-second resolutions: price changes tend to be infrequent relative to long
stretches of unchanged states, making them difficult for a model to learn reliably. This motivates the use of
second-scale (or coarser) sampling and/or longer temporal conditioning. In practice, depending on the stock,
higher-frequency price changes may not occur at all, which can require propagating (or “dragging”) the last
observed snapshot forward until a genuine state change is observed. Moreover, this approach implicitly assumes
no gaps between price levels and a perfectly tight bid–ask spread of one tick. In real markets, these assumptions
are often violated, as gaps and wider spreads do occur; addressing these discrepancies and their implications is
deferred to a later discussion in the document.
The final dataset is comprised of 20 days of 1-second clipped
data and uses a 80-20 training validation scheme. Price paths are generated by seeding the conditioning window
with a randomly drawn snapshot sequence from the dataset, then sampling autoregressively from the decoder.
4.2. Models
Rather than conditioning only on the most recent snapshot (Markov), we condition on the last h = 10
snapshots:
X(h)
t
=
 xt−(h−1)∆, . . . , xt

,
h = 10,
and summarize this history through an LSTM hidden state
ht = LSTM

X(h)
t

,
using a single layer with hidden size 128.
Conditional VAE (latent variable and decoder MLP).. Given the history embedding ht, the CVAE models the
next snapshot as
pθ(xt+∆| ht) =
Z
pθ(xt+∆| ht, zt) p(zt) dzt,
zt ∼N(0, I),
where the latent dimension is explored over 8–32. The decoder is implemented as a lightweight MLP head on
top of the conditioning and latent variables; we explore MLP hidden widths in the range 32–64. The retained
configuration and the full training setup are reported in Table 2.
5. Results
5.1. Marginal distribution
The primary objective of the model is to learn the marginal distribution of the observed data. Two elements
of the training objective introduced in Section 3 bear directly on this task: the β weighting, whose low value
relaxes the KL regularisation and thereby favours reconstruction fidelity and the preservation of fine-grained
patterns, and the per-sample weight wc, which upweights the rare price-change events populating the tails of
the distribution—regions that are disproportionately important because they carry the price movements the
simulator must reproduce.
It is also important to note the structural characteristics of the data itself. In many financial and market
settings, quantities such as queue sizes are aggregated in discrete units, commonly referred to as “lots.” This
aggregation inherently reduces the likelihood of observing very small queue sizes. As a result, the empirical
distribution often exhibits a bimodal pattern, corresponding to positive and negative variations in these ag-
gregated quantities. For modelling purposes, this bimodality can be effectively approximated by a unimodal
8


## Page 9

Table 2: Hyperparameters and training configuration
Parameter
Value
Architecture
LSTM layers
1
LSTM hidden size
128
Latent dimension
16
Decoder MLP hidden width
64
Conditioning horizon h
10
Training
Optimizer
Adam
Learning rate
1 × 10−3
Batch size
256
Epochs
100
β (KL weight)
0.1
wc (price-change weight)
2.0
CGAN Benchmark
Generator hidden size
128
Discriminator hidden size
128
Critic iterations
5
Gradient penalty λ
10
Epochs
300
distribution that encompasses both extremes, simplifying the representation while retaining the essential distri-
butional properties.
Tests were realized on both BMO and Telus stock but we will only present BMO in this
document.
Figure 2: level 1 CVAE
Figure 3: level 2 CVAE
Figure 4: level 3 CVAE
As presented in Figures 2, 3, and 4, the model captures the overall shape and support of the marginal
distributions at all three levels, including the bimodal bid–ask separation and the relative scale of deeper queues.
However, the generated distributions are smoother than the empirical ones: the sharp peaks arising from lot-size
quantisation (multiples of 100 shares) are not reproduced, and some tail mass—notably near −2.5 at level 3
bid—is underrepresented. These discrepancies are consistent with the Gaussian decoder assumption, which
favours unimodal outputs and inherently smooths discrete concentration points. The marginal KL divergence
reported in Table 3 reflects this gap; improving tail fidelity through a more expressive decoder or a mixture-based
prior is left to future work.
5.2. Average best quantities
One natural follow up from the marginal distribution performances is the ability to reproduce the order book
quantities with high fidelity. This can be shown in Figure 5 where we can see that the smile shape typically
presented by the LOB (see Abergel et al. 2016) is well learnt by the model. Differences by a magnitude of one
round lot (100) can be noted on the first bid. This testify of the more volatile nature of the inner levels.
9


## Page 10

0
200
400
600
800
1000
1200
1400
B3
B2
B1
A1
A2
A3
Average quanes CVAE
real
synthec
Figure 5: average best quantities CVAE
5.3. Level-to-level correlation
Level-to-level correlation plays a crucial role in capturing the full dynamics of the limit order book (LOB),
as it reflects how changes at one price level influence—or are influenced by—changes at adjacent levels. This
is particularly important in high-frequency trading environments, where the addition or removal of orders at
one level can propagate through the book, affecting both liquidity distribution and price formation. This is the
reason for the adoption of models such as multidimensional Hawkes processes, offering the ability to capture
these relationships (Lu and Abergel, 2018).
One of the simplest measurements to quantify these relationships is the Pearson correlation coefficient.
However, it is important to note that Pearson correlation measures only linear dependencies between variables.
As a result, more complex, non-linear interactions—such as sudden liquidity shifts, strategic order placement,
or hidden liquidity effects—may not be fully captured by this measure.
Figure 6: Correlations real CVAE
Figure 7: Correlation model CVAE
As we can see in Figures 6 and 7, the model-generated correlations closely match the real ones. From an
architectural standpoint, a larger latent dimension gives the decoder more capacity to represent joint variation
across levels; however, this also increases the risk of overfitting. The weighted reconstruction loss mitigates
10


## Page 11

this trade-off by steering gradient signal toward the rarer price-change snapshots. This involves coordinated
sign flips across multiple levels, without requiring an excessively large latent space. We note that these are
qualitative design considerations; a systematic ablation over the latent dimension is not performed in this work
and is left to future investigation.
5.4. Price paths
Price paths are a good indicator of the simulator’s usability as well as success in learning the LOB’s dynamic.
The time series are obtained by sampling the decoder sequentially and translating the sign structure of the
snapshot into a price change (measured in ticks, i.e. δ = 1) using
∆pt+∆t = −1
2
2k
X
i=1
sign(Xt+∆t, i).
The factor −1
2 and the sign convention arise as follows: in the balanced (no-change) state all k bid components
are negative and all k ask components are positive, so P
i sign(Xi) = 0. A one-tick upward move converts one
ask queue to a bid queue (its sign flips from +1 to −1), changing the sum by −2; multiplying by −1
2 yields
∆p = +1 tick, as expected. Symmetrically, a one-tick downward move flips one bid to ask, giving ∆p = −1 tick.
Figure 8: price path real
Figure 9: price path model CVAE
As we can see in Figures 8 and 9, price paths are closely matched by the algorithm. Price changes are well
respected, giving confidence in the ability to capture the LOB dynamics.
5.5. Reactivity
In that instance, we tested a lift the bid and the join the ask ability. We varied the sizes of the exercise
and compared the resulting size-impact relationship with the concave (sub-linear) pattern reported by Ponzi
et al. (2009). The setup requires a perfectly balanced lob to maximize the effect and reflect the non arbitrage
assumption (Cont et al., 2023). To achieve that, we cloned and inverted our bid model (or ask model). This
means that the price path before or after the exercise will be a flat price impact, showcasing only the lift the
bid or join the ask operation.
Regarding the model’s reactivity, three tests were performed on our model. The first one aimed at testing
the model’s ability to replicate a trajectory observed on the market when their lob information are fed to the
simulator on a snapshot by snapshot basis. For this, we identified one period of price decrease and fed it to
the model. This setup allows to check the directional ability of the model and prevents, error propagation since
forecasts are not stacked on top of each other. That exercice will come later. We also tested the opposite
variation by simply inverting the downward trajectory. This exercise allow to assess the reactivity of the model
to synthetic data feeding and thus the generalization ability.
Figure 11 shows the various price paths used in the simulation as well as the average path resulting from
the liquidity taking action. One interesting fact, visible in Figure 10, is that the effect is more pronounced
depending on the amount taken at each 3 seconds.
The resulting size-impact relationship is concave: larger
interventions produce proportionally smaller additional price displacement, which is qualitatively consistent
11


## Page 12

Figure 10: Price Impact liquidity takers: sizes - CVAE
Figure 11: Price Impact liquidity taker - CVAE
with the sub-linear impact reported by Ponzi et al. (2009). However, with only four tested sizes and no formal
regression, we do not claim to have identified a specific power-law exponent; a systematic log-log analysis over
a finer grid of intervention sizes is left to future work.
The price impact persists after the intervention
ends (Figures 10 and 12). This is expected under the balanced-book setup: symmetrising the conditioning
distribution removes any asymmetry that could drive mean-reversion, so the post-action price remains flat by
construction. Characterising transient impact decay would require conditioning on an asymmetric, real-market
book state and is left to future work.
Then we did the same exercise but performing a liquidity provision scheme for 60 seconds. The expected
effect is a price decrease, as lower prices probability increases.
Figure 12: Price Impact liquidity Provider: sizes - CVAE
Figure 13: Price Impact liquidity providers - CVAE
Here again, as Figures 12 and 13 show, the size of trades to be added to the best queue affects the price
decrease effect. The reactivity is less strong than on the liquidity taking front, which was corroborated in Cont
et al. (2023).
6. Benchmarking
We benchmark the CVAE against a Conditional Wasserstein GAN with gradient penalty (CGAN) for three
reasons. First, conditional adversarial architectures represent the dominant competing deep generative approach
in the recent LOB simulation literature: Coletta et al. (2023) and Cont et al. (2023) both use CGAN-style
objectives on problems directly comparable to ours, making this the most relevant point of comparison. Second,
12


## Page 13

the comparison is architecturally controlled: both models receive the same snapshot-based conditioning input
ht and produce the same fixed-length depth vector, so differences in performance can be attributed to the
training objective rather than to representational capacity or data preprocessing. Third, the tension between
likelihood-based objectives (ELBO) and adversarial objectives is a well-documented trade-off in the generative
modelling literature (Theis et al., 2016): ELBO training tends to produce smoother but potentially over-
smoothed outputs, while adversarial training captures sharper modes at the risk of mode collapse. Evaluating
this trade-off empirically on LOB data is the central scientific question of this section.
In order to benchmark our model, we trained a Generative Adversarial Network (GAN)—specifically, a
Conditional GAN—on our dataset. GANs are well-recognized generative models composed of two networks:
a generator and a discriminator.
The generator learns to create high-fidelity outputs (LOB states) from a
random input (typically sampled from a Normal distribution). These generated outputs are paired with real
LOB states and fed to the discriminator, whose goal is to distinguish genuine outputs from generated ones. A
sigmoid activation is applied at the end of the discriminator to produce an output between 0 and 1, which is
then used via backpropagation to update the weights of both networks, improving the generator’s ability to fool
the discriminator and the discriminator’s ability to detect fakes. As training progresses, the generator learns
the characteristics of genuine LOB states and attempts to deceive the discriminator. Ideally, this adversarial
game converges to a Nash equilibrium, where both networks reach optimal strategies.
However, as argued
by Goodfellow et al. (2020), convergence is rarely achieved in practice because optimization occurs in a non-
convex function space. When convergence does occur, the discriminator outputs approach 0.5 for all samples,
indicating equal likelihood of real or fake. One major advantage of GANs is that they do not require prior
distributional assumptions, making them mathematically lighter and highly flexible. However, the two-network
adversarial setup introduces significant training challenges. The optimization landscape is a saddle point, which
makes training unstable. A well-known issue is mode collapse, where the generator produces limited diversity in
outputs. Mode collapse can be full (identical outputs regardless of input noise) or partial (outputs share similar
motifs).
Durall López et al. (2021) argue that mode collapse is linked to the generator converging toward
sharp local minima. When the generator repeatedly produces similar outputs and the discriminator fails to
penalize them—often due to vanishing gradients—the generator receives high scores, leading to weak updates
and reinforcing collapse. Several techniques mitigate this issue, notably the Wasserstein GAN (W-GAN) and
the gradient penalty, which stabilize training by enforcing Lipschitz continuity Arjovsky et al. (2017); Gulrajani
et al. (2017). Other challenges include the absence of a formal likelihood or loss metric, complicating feature
identification—especially for non-image data like LOB states. Evaluation metrics such as the Fréchet Inception
Distance (FID) have been adapted for generative quality assessment ?. To address these issues, we implemented
a Conditional W-GAN with gradient penalty, and the following section presents our results.
6.1. Evaluation metrics
We compare the two simulators along three axes. Write x = (x1, . . . , x2k) for the snapshot vector, with
components ordered (Bk, . . . , B1, A1, . . . , Ak) and k = 3, and let P and bP denote respectively the empirical
distribution of the held-out real snapshots and that of an equally sized sample drawn from the trained generator.
All three metrics are computed on the same held-out period and are oriented so that lower is better.
The marginal divergence aggregates, over the 2k components, the Kullback–Leibler divergence between the
one-dimensional empirical marginals Pj and bPj of component j,
Each per-component divergence is estimated
via Gaussian kernel density estimation (KDE) with Silverman bandwidth selection. Both densities are evaluated
on a shared grid of n = 1000 equally spaced points covering the union of their supports, re-normalised to integrate
to unity, and stabilised by adding ε = 10−10. The divergence is then computed as
DKL(Pj∥bPj) =
Z
pj(x) ln pj(x)
ˆpj(x) dx ≈
n
X
i=1
pj(xi) ln pj(xi)
ˆpj(xi) ∆x,
and the reported metric averages over the 2k components:
Dmarg
KL
= 1
2k
2k
X
j=1
DKL

Pj ∥bPj

.
The queue error measures the discrepancy between the average depths displayed at each level, aggregated
13


## Page 14

over the 2k components,
Equeue = 1
2k
2k
X
j=1
EP [xj] −E b
P [xj]
.
The correlation error compares the full level-to-level dependence structure through the Frobenius norm of
the difference between the two 2k × 2k Pearson correlation matrices C and bC,
Ecorr =
C −bC

F =
 2k
X
i=1
2k
X
j=1
 Cij −bCij
2
!1/2
.
6.2. Marginal distribution
The three marginal distributions (Figures 14, 15, and 16) illustrate that the CGAN manages to reproduce
the empirical shapes with high fidelity across all liquidity levels. Compared to the CVAE, the CGAN tends to
capture sharper local modes, which is consistent with the adversarial training objective that pushes generated
samples toward realistic high-density regions. However, this behaviour sometimes comes at the cost of slightly
higher variance in low-density tails, a pattern commonly observed in GAN-based simulators.
Figure 14: Level 1 GAN
Figure 15: Level 2 GAN
Figure 16: Level 3 GAN
This is an important distinction between the CGAN and CVAE frameworks. While the CVAE explicitly
learns a conditional likelihood, the CGAN does not assume nor impose any parametric form on the marginals.
This allows the CGAN to replicate complex empirical shapes naturally, especially when the data exhibits
multimodality or skewness. The absence of likelihood-based optimization, however, also means that training
stability must be carefully monitored to avoid mode collapse (Goodfellow et al., 2020; Durall López et al., 2021).
Crucially, sharper marginals do not automatically translate into better structural fidelity: as the correlation
and queue-level results below show, the CVAE’s likelihood-based objective produces superior joint dependence
structure despite its higher marginal KL, suggesting that for LOB simulation—where inter-level coherence and
queue accuracy are operationally more important than marginal sharpness—the CVAE’s training objective is
better aligned with the evaluation criteria. A multimodal CVAE could help bridge the gap between the two
approaches.
6.3. Average Best Quantities
The average best quantities produced by the CGAN (Figure 17, as described in Section 5.2) closely aligns with
the empirical benchmark, indicating that the model captures not only marginal behavior but also the relative
ordering of optimal liquidity placement across levels. Overall, the agreement between the CGAN-generated
averages and the real data further supports the model’s ability to learn meaningful liquidity allocation patterns.
Both models reproduce the LOB smile, but the CVAE achieves a lower queue-level error (34.10 vs. 55.30 shares;
see Table 3), indicating that its likelihood-based objective produces more accurate queue size estimates—a
practically significant advantage for execution cost analysis and market-making strategy evaluation.
14


## Page 15

0
200
400
600
800
1000
1200
1400
1600
B3
B2
B1
A1
A2
A3
Average quanes GAN
real
synthec
Figure 17: average best quantities
6.4. Level-to-level correlation
Correlations between liquidity levels are a key structural element of the simulator. The CGAN maintains
these dependencies reasonably well (as exhibited in Figures 18 and 19), especially for adjacent levels where
empirical co-movements are strongest.
However, the CVAE achieves a lower Frobenius norm between the
empirical and generated correlation matrices (0.34 vs. 0.44), indicating that it preserves the full inter-level
dependence structure more faithfully. This is consistent with the observation that the ELBO objective, by
penalising reconstruction errors at each level simultaneously, implicitly regularises the joint distribution of
queue sizes across levels.
The adversarial objective, by contrast, evaluates entire joint samples holistically,
which can sharpen individual modes while introducing artefacts in cross-level relationships.
Figure 18: Correlations realGAN
Figure 19: Correlation model generated GAN
6.5. Reactivity
The GAN also shows a liquidity taking reactivity (Figure 20), which is line with literature and brings comfort
in the CVAE results.
The reactivity plot highlights that the CGAN effectively captures the liquidity taking dynamics observed
in the empirical data. In particular, the average path responds in the expected direction as depth is consumed
at the best quote, demonstrating that aggressive order flow in the simulation moves the price consistently with
the structural patterns identified in real markets. This ability to produce a directional price response confirms
that the CGAN does not simply memorize marginal distributions but learns a meaningful liquidity–response
15


## Page 16

Figure 20: Liquidity takers GAN
mechanism.
The resulting behaviour is coherent with established findings in the microstructure literature,
thereby reinforcing the reliability of the CVAE’s own reactivity results by providing an independently trained
adversarial benchmark.
We also provided a quantitative comparison table between the CVAE and the CGAN approach.
Stock
Model
Marginals KL divergence
Queue error (shares)
Correlation Diff Frobenius norm
BMO
CVAE
0.1434
34.0966
0.3389
BMO
CGAN
0.0542
55.2965
0.4371
Telus
CVAE
0.0601
52.7655
0.2500
Telus
CGAN
0.0662
162.4581
0.7055
Table 3: Performance comparison of CVAE and CGAN
The CGAN achieves a lower marginals KL divergence on BMO (0.054 vs. 0.143), reflecting its ability to
produce sharper local modes consistent with the adversarial objective’s emphasis on sample realism. On Telus,
however, the marginal advantage reverses (0.066 vs. 0.060), suggesting that on less liquid stocks the CVAE’s
likelihood-based objective is already competitive on marginal fidelity. The CVAE consistently outperforms on
the two metrics most directly relevant to LOB simulation practice across both stocks: queue-level fidelity (BMO:
34.10 vs. 55.30, a 38% improvement; Telus: 52.77 vs. 162.46, a 68% improvement) and inter-level correlation
structure (BMO: 0.34 vs. 0.44; Telus: 0.25 vs. 0.71). Notably, the CGAN’s structural degradation is more severe
on the less liquid Telus stock, where the adversarial objective’s difficulty in capturing thin-queue dynamics
leads to a nearly threefold increase in queue error relative to the CVAE. Accurate queue sizes directly affect
execution cost estimates, and correct correlation structure is essential for multi-level order placement strategies.
The CVAE requires no gradient-penalty coefficient or critic-iteration schedule and is implemented as a single
network—substantially reducing the hyperparameter search burden. Taken together, the quantitative results
across both stocks support the CVAE as the preferred model when structural fidelity and training simplicity
are prioritised over marginal sharpness, which is the relevant criterion for production-level LOB simulators.
7. Ablation Study
To quantify the contribution of the LSTM history encoder, we perform an ablation study on the conditioning
sequence length h. We train the CVAE under identical hyperparameters for h ∈{1, 2, 4, 10, 20}, where h = 1
corresponds to a first-order Markov model that conditions only on the immediately preceding snapshot. Each
configuration is trained with 5 independent random seeds; the test-set mean squared error (MSE) is reported
in Table 4 as mean ± one standard deviation.
16


## Page 17

Lag h
Telus
BMO
1
0.0259 ± 0.0029
0.0396 ± 0.0068
2
0.0219 ± 0.0013
0.0370 ± 0.0024
4
0.0192 ± 0.0005
0.0360 ± 0.0019
10
0.0181 ± 0.0011
0.0344 ± 0.0018
20
0.0158 ± 0.0010
0.0312 ± 0.0012
Table 4: Test MSE as a function of LSTM conditioning length h (mean ± std over 5 seeds).
Both stocks exhibit a monotonic and statistically significant improvement as the conditioning horizon in-
creases. For BMO, MSE decreases from 0.0396 ± 0.0068 at h = 1 to 0.0312 ± 0.0012 at h = 20 (a 21% re-
duction), with non-overlapping confidence intervals between extreme configurations. For Telus, MSE decreases
from 0.0259 ± 0.0029 at h = 1 to 0.0158 ± 0.0010 at h = 20 (a 39% reduction), confirming that the benefit of
longer temporal context holds across liquidity regimes. The monotonic trend is consistent with the intuition
that longer context helps the LSTM track queue replenishment dynamics, while the larger relative gain on Telus
suggests that the sparser informative transitions in less liquid books benefit more from extended memory.
We retain h = 10 for the main experiments as it provides most of the improvement (30% on Telus, 13% on
BMO relative to h = 1) at moderate computational cost, noting that h = 20 offers further gains at the expense
of longer conditioning sequences.
8. Conclusion
In this paper, we have presented a reactive limit order book simulator combining a Conditional Variational
Autoencoder with an LSTM history encoder, trained and evaluated on Toronto Stock Exchange equity data.
The simulator reproduces the four key stylized facts examined — marginal queue distributions, the average-
quantity smile, level-to-level correlations, and realistic price paths — and exhibits reactive price impact for
both liquidity taking and provision, with a concave size-impact relationship qualitatively consistent with the
literature.
Benchmarked against a Conditional WGAN-GP trained on the same data, the CVAE achieves
superior queue-level fidelity (34.10 vs. 55.30 shares) and better inter-level correlation structure (Frobenius norm
0.34 vs. 0.44), at the cost of higher marginal KL divergence (0.143 vs. 0.054). The CVAE’s single-network
ELBO objective avoids the gradient-penalty tuning and critic-iteration scheduling required by the WGAN-GP,
substantially reducing the hyperparameter search burden. These properties make the CVAE a competitive and
practical alternative to adversarial approaches for production-level LOB simulation, particularly when structural
fidelity and training simplicity are prioritised over marginal sharpness.
A limitation of this study is the age of the dataset: while the architecture and training procedure are
not specific to that period, market microstructure evolves over time; for instance through changes in tick-size
regimes, fee schedules, or the prevalence of algorithmic participants. Validation on more recent data would
strengthen the generalisability claim.
Several promising avenues can be pursued to further extend and strengthen the proposed framework. First,
the data encoding mechanism could be refined to explicitly handle non-zero bid–ask spreads and discontinuities
in level prices, while preserving the overall structure of the model and its homogeneity property.
Such an
extension would significantly broaden the applicability of the approach, enabling its use on less liquid equities
as well as other asset classes, including foreign exchange, interest rates, and commodities. Second, departures
from the Gaussian prior assumption could be investigated through a multimodal prior framework. Empirical
evidence suggests that marginal distributions often exhibit multimodality, which may not be adequately captured
by the current isotropic Gaussian prior. This limitation could be addressed by adopting more expressive prior
distributions, such as mixtures of Gaussians or normalising flows, thereby improving the model’s ability to
represent complex distributional features. Finally, a foundation model approach could be explored to support
joint training and inference across multiple stocks. The relatively simple and scalable training scheme facilitates
the use of longer time horizons and richer datasets, opening the door to cross-asset learning and improved
generalisation through shared representations (Ansari et al.; Das et al., 2024).
17


## Page 18

References
Abergel, F., Anane, M., Chakraborti, A., Jedidi, A., Muni Toke, I., 2016. Limit Order Books. Physics of
Society: Econophysics and Sociophysics, Cambridge University Press. doi:doi:10.1017/CBO9781316661673.
Abergel, F., Jedidi, A., 2015. Long-time behavior of a Hawkes process–based limit order book. SIAM Journal
on Financial Mathematics 6, 1026–1043. doi:doi:10.1137/15M1011469.
Ansari, A.F., Stella, L., Turkmen, C., Zhang, X., Mercado, P., Shen, H., Shchur, O., Rangapuram,
S.S., Arango, S.P., Kapoor, S., Zschiegner, J., Maddix, D.C., Wang, H., Mahoney, M.W., Torkkola,
K., Wilson, A.G., Bohlke-Schneider, M., Wang, Y., .
Chronos:
Learning the language of time se-
ries. Transactions on Machine Learning Research URL: https://openreview.net/forum?id=gerNCVqqtR,
doi:doi:10.48550/arXiv.2403.07815, arXiv:2403.07815. published in TMLR (11/2024).
Arjovsky, M., Chintala, S., Bottou, L., 2017. Wasserstein generative adversarial networks, in: Precup, D., Teh,
Y.W. (Eds.), Proceedings of the 34th International Conference on Machine Learning, PMLR. pp. 214–223.
doi:doi:10.48550/arXiv.1701.07875.
Bak, P., Paczuski, M., Shubik, M., 1997. Price variations in a stock market with many agents. Physica A:
Statistical Mechanics and its Applications 246, 430–453. doi:doi:10.1016/S0378-4371(97)00401-9.
Bodor, H., Carlier, L., 2025. Deep learning meets queue-reactive: A framework for realistic LOB simulation.
arXiv preprint arXiv:2501.08822 doi:doi:10.48550/arXiv.2501.08822, arXiv:2501.08822.
Bouchaud, J.P., Mezard, M., Potters, M., 2002. Statistical properties of stock order books: empirical results
and models. Quantitative Finance 2, 251–256. doi:doi:10.1088/1469-7688/2/4/301.
Byrd, D., Hybinette, M., Balch, T., . ABIDES: Towards high-fidelity market simulation for AI research, in: Pro-
ceedings of the 2020 SIGSIM Conference on Principles of Advanced Discrete Simulation (SIGSIM-PADS ’20),
Association for Computing Machinery. pp. 11–22. URL: https://acm.org, doi:doi:10.1145/3384441.3395986,
arXiv:1904.12066.
Chawla, N.V., Bowyer, K.W., Hall, L.O., Kegelmeyer, W.P., 2002. Smote: Synthetic minority over-sampling
technique. Journal of Artificial Intelligence Research 16, 321–357. URL: http://dx.doi.org/10.1613/jair.
953, doi:doi:10.1613/jair.953.
Chung, G., Lee, Y., Kim, W.C., 2024. Neural marked Hawkes process for limit order book modeling, in: Yang,
D.N., Xie, X., Tseng, V.S., Pei, J., Huang, J.W., Lin, J.C.W. (Eds.), Advances in Knowledge Discovery and
Data Mining. PAKDD 2024, Springer, Singapore. pp. 197–209. doi:doi:10.1007/978-981-97-2253-2_16.
Chung, J., Gulcehre, C., Cho, K., Bengio, Y., 2014. Empirical evaluation of gated recurrent neural networks on
sequence modeling. URL: https://arxiv.org/abs/1412.3555, arXiv:1412.3555.
Coletta, A., Jerome, J., Savani, R., Vyetrenko, S., 2023. Conditional generators for LOB environments: Ex-
plainability, challenges, and robustness, in: Proceedings of the Fourth ACM International Conference on AI
in Finance (ICAIF), pp. 156–164. doi:doi:10.1145/3604237.3626854.
Cont, R., Cucuringu, M., Kochems, J., Prenzel, F., 2023.
Limit order book simulation with gener-
ative adversarial networks.
SSRN Electronic Journal.
URL: https://ssrn.com/abstract=4512356,
doi:doi:10.2139/ssrn.4512356.
Cont, R., de Larrard, A., 2013. Price dynamics in a Markovian limit order market. SIAM Journal on Financial
Mathematics 4, 1–25. doi:doi:10.1137/110856605.
Cont, R., Stoikov, S., Talreja, R., 2010. A stochastic model for order book dynamics. Operations Research 58,
549–563. doi:doi:10.1287/opre.1090.0780.
Das, A., Kong, W., Sen, R., Zhou, Y., 2024. A decoder-only foundation model for time-series forecasting, in:
Proceedings of the 41st International Conference on Machine Learning (ICML), PMLR. pp. 9832–9851. URL:
https://proceedings.mlr.press.
18


## Page 19

Durall López, R., Chatzimichailidis, A., Labus, P., Keuper, J., 2021. Combating mode collapse in GAN training:
An empirical analysis using Hessian eigenvalues, in: Proceedings of the 16th International Joint Conference on
Computer Vision, Imaging and Computer Graphics Theory and Applications (VISIGRAPP 2021), SciTePress.
pp. 211–218. doi:doi:10.5220/0010167902110218.
Farmer, J.D., Patelli, P., Zovko, I.I., 2005.
The predictive power of zero intelligence in financial markets.
Proceedings of the National Academy of Sciences 102, 2254–2259. doi:doi:10.1073/pnas.0409157102.
Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., Courville, A., Bengio, Y.,
2020. Generative adversarial networks. Commun. ACM 63, 139–144. doi:doi:10.1145/3422622.
Gould, M.D., Porter, M.A., Williams, S., McDonald, M., Fenn, D.J., Howison, S.D., 2013. Limit order books.
Quantitative Finance 13, 1709–1742. doi:doi:10.1080/14697688.2013.803148.
Gulrajani, I., Ahmed, F., Arjovsky, M., Dumoulin, V., Courville, A., 2017. Improved training of wasserstein
gans, in: Proceedings of the 31st International Conference on Neural Information Processing Systems, Curran
Associates Inc., Red Hook, NY, USA. pp. 5769–5779. doi:doi:10.5555/3295222.3295327.
Higgins, I., Matthey, L., Pal, A., Burgess, C., Glorot, X., Botvinick, M., Mohamed, S., Lerchner, A., 2017. beta-
VAE: Learning basic visual concepts with a constrained variational framework, in: International Conference
on Learning Representations. URL: https://openreview.net/forum?id=Sy2fzU9gl.
Hochreiter,
S.,
Schmidhuber,
J.,
1997.
Long
short-term
memory.
Neural
Computation
9,
1735–1780.
URL: https://doi.org/10.1162/neco.1997.9.8.1735, doi:doi:10.1162/neco.1997.9.8.1735,
arXiv:https://direct.mit.edu/neco/article-pdf/9/8/1735/813796/neco.1997.9.8.1735.pdf.
Huang, W., Lehalle, C.A., Rosenbaum, M., 2015. Simulating and analyzing order book data: The queue-reactive
model. Journal of the American Statistical Association 110, 107–122. doi:doi:10.1080/01621459.2014.982278.
Hultin, H., Hult, H., Proutiere, A., Samama, S., Tarighati, A., 2023. A generative model of a lob using recurrent
neural networks. Quantitative Finance 23, 931–958. doi:doi:10.1080/14697688.2023.2205583.
Jain, K., Firoozye, N., Kochems, J., Treleaven, P., 2024.
Limit order book simulations: A review.
arXiv
arXiv:2402.17359.
Kalman, R.E., 1960. A new approach to linear filtering and prediction problems. Journal of Basic Engineering
82, 35–45. doi:doi:10.1115/1.3662552.
Kingma, D.P., Welling, M., 2014. Auto-encoding variational bayes, in: Proceedings of the 2nd International
Conference on Learning Representations (ICLR), pp. 1–14. URL: https://arxiv.org/abs/1312.6114.
Lalor, L., Swishchuk, A., 2025.
Event-based limit order book simulation under a neural Hawkes process:
Application in market-making 32, 128–155. URL: https://doi.org, doi:doi:10.1080/1350486X.2025.2548448,
arXiv:2502.17417.
Lea, C., Flynn, M.D., Vidal, R., Reiter, A., Hager, G.D., 2017.
Temporal convolutional networks for ac-
tion segmentation and detection, in: Proceedings of the IEEE Conference on Computer Vision and Pattern
Recognition (CVPR), pp. 2847–2856.
Lu, X., Abergel, F., 2018.
High-dimensional hawkes processes for limit order books: modelling, empirical
analysis and numerical calibration. Quantitative Finance 18, 249–264.
Mike, S., Farmer, J.D., 2008. An empirical behavioral model of liquidity and volatility. Journal of Economic
Dynamics and Control 32, 200–234. doi:doi:10.1016/j.jedc.2007.01.031.
Ponzi, A., Lillo, F., Mantegna, R.N., 2009. Market reaction to a bid-ask spread change: A power-law relaxation
dynamics. Phys. Rev. E 80, 016112.
Preis, T., Golke, S., Paul, W., Schneider, J.J., 2006. Multi-agent-based order book model of financial markets.
Europhysics Letters 75, 510–516.
19


## Page 20

Shi, Z., Cartlidge, J., 2024. Neural stochastic agent-based lob simulation. Intelligent Systems in Accounting,
Finance and Management 31.
Sohn, K., Yan, X., Lee, H., 2015. Learning structured output representation using deep conditional generative
models, in: Proceedings of the 29th International Conference on Neural Information Processing Systems -
Volume 2, MIT Press, Cambridge, MA, USA. pp. 3483–3491. doi:doi:10.5555/2969442.2969628.
Theis, L., van den Oord, A., Bethge, M., 2016. A note on the evaluation of generative models, in: Proceedings
of the 4th International Conference on Learning Representations (ICLR), pp. 1–11. URL: https://arxiv.
org/abs/1511.01844.
Xiao, Y., Ventre, C., Wang, Y., Li, H., Huan, Y., Liu, B., . LiT: Limit order book transformer 8. URL:
https://doi.org/10.3389/frai.2025.1616485, doi:doi:10.3389/frai.2025.1616485.
Zhang, Z., Zohren, S., Roberts, S., 2019. Deeplob: Deep convolutional neural networks for limit order books.
IEEE Transactions on Signal Processing 67, 3001–3012.
20


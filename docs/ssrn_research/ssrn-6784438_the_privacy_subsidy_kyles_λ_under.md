# The Privacy Subsidy: Kyle’s λ under

- **Source File**: `ssrn-6784438.pdf`
- **Total Pages**: 17
- **SSRN ID**: `ssrn-6784438`

---


### Page 1

The Privacy Subsidy: Kyle’s λ under
Noise-Perturbed Order-Flow Observation
Yuki Nakamura[0009−0001−7174−6737]
The Open University of Japan
Abstract. Privacy-preserving cryptocurrency exchanges alter what the
pricing mechanism observes about order flow. We derive the unique lin-
ear Kyle equilibrium when a committed Bayesian market maker observes
order flow perturbed by independent Gaussian privacy noise. The price-
impact coeﬀicient and informed-trader strategy rescale by reciprocal fac-
tors of the privacy parameter (one down, one up), so their product is in-
variant. A welfare decomposition then identifies a closed-form per-period
transfer from the protocol’s LP pool to traders — the privacy subsidy,
the break-even fee any privacy-aggregated exchange must charge. The re-
sult is the single-period closed-form privacy-noise analog of Loss-Versus-
Rebalancing [13]. The primary application is shielded AMMs with ex-
plicit additive-noise injection (e.g., differential privacy); related designs
(batched swaps, sealed-bid auctions, oracle-pegged crossings) require sep-
arate frameworks that we leave to future work.
Keywords: Market microstructure · Kyle equilibrium · ZK exchanges
· Adverse selection
1
Introduction
Privacy-preserving exchange designs are an increasingly common architecture in
cryptocurrency markets. Renegade matches orders via multi-party computation
under zero-knowledge proofs [2]; Penumbra batches swaps and reveals only batch
totals on-chain [14]; Suave-style order-flow auctions seal individual bids until
builder selection [8]; shielded variants of constant-function automated market
makers inject privacy noise into the observable reserve state before on-chain price
updates. These designs all alter what the liquidity-providing role — whether an
LP pool, an arbitrageur, or a smart-contract pricing rule — observes about order
flow.
Classical microstructure theory [11] gives the equilibrium price-impact coef-
ficient λ and informed-trader strategy β in closed form when the market maker
observes the full aggregate flow y = x + u. These results do not, however, char-
acterize the welfare consequences when the market maker prices on a noise-
perturbed signal ˜y = y + ε, as arises naturally in privacy-aggregated exchange
designs.


### Page 2

2
Y. Nakamura
Contributions. This paper provides three results, each of which is absent in or
distinct from textbook Kyle.
1. A closed-form linear Kyle equilibrium under MM observation ˜y = y + ε with
Gaussian privacy noise ε ∼N(0, σ2
ε) independent of (v, u), under a commit-
ted Bayesian MM pricing rule: the maker prices at the posterior mean of
the coarse signal, which is the competitive price conditional on that signal.
The only departure from textbook Kyle is that the maker conditions on ˜y
rather than the exact flow y, so it does not break even against the real flow
(Remark 2); the equilibrium recovers Kyle exactly in the σε = 0 limit. The
unique price-impact coeﬀicient is λ = σv/(2
√
σ2u + σ2ε) with informed-trader
linear coeﬀicient β =
√
σ2u + σ2ε/σv (Theorem 1).
2. A welfare decomposition under this equilibrium, identifying a per-period
transfer |πM| = σvσ2
ε/(2
√
σ2u + σ2ε) from the protocol/LP side to traders —
the privacy subsidy (Theorem 2). This quantity is identically zero in textbook
Kyle, where the market maker observes order flow exactly; it turns positive
once the privacy noise makes the observed signal strictly coarser than the
executed flow, so that no price rule can be simultaneously informationally
eﬀicient and zero-profit against the real flow (Remark 2). The subsidy is the
break-even fee that any privacy-aggregated exchange must charge to compen-
sate its liquidity layer.
3. A primary mapping from σε to shielded AMMs with explicit additive-noise
(differential-privacy) injection, yielding a per-design break-even fee. We also
delineate the boundary of applicability: Penumbra-style batched swaps re-
duce to textbook Kyle with rescaled noise-trader variance (and no privacy
subsidy under Bayesian MM); Suave-style sealed-bid order-flow auctions sit
in LVR’s temporal-asymmetry regime; oracle-pegged crossings such as Rene-
gade fall outside the Kyle framework. These three nearby designs require
separate frameworks and are left to future work.
This paper analyzes the equilibrium consequences of privacy in exchange
design, treating ZK primitives as a black box producing ˜y; protocol-level sound-
ness/completeness analysis is out of scope.
Positioning. On the microstructure side, the result isolates a closed-form welfare
quantity (the privacy subsidy) under additive privacy noise on the maker’s flow
signal; the equilibrium (λ, β) itself is textbook Kyle under the substitution σ2
u 7→
σ2
u + σ2
ε, so the novelty lies in the welfare object rather than the equilibrium.
The closest microstructure precedent on the observability axis is the strand on
insider disclosure [10], where the trader’s actions become more observable —
our case moves the imperfection to the market maker’s signal instead. On the
decentralized-finance side, the privacy subsidy is the single-period closed-form
analog of Loss-Versus-Rebalancing identified by Milionis et al. [13]: LVR isolates
the cost to LPs from stale prices being picked off by arbitrageurs with external
price information, while our privacy subsidy isolates the cost from privacy noise
obscuring the MM’s flow observation. The two are closed-form welfare quantities


### Page 3

The Privacy Subsidy
3
of the same family; their combination in a continuous-time AMM with privacy
is left to future work (Section 7).
Roadmap. Section 2 surveys related work along three strands. Section 3 sets up
the model and equilibrium concept. Section 4 states and proves the main equi-
librium theorem. Section 5 derives the welfare decomposition and identifies the
privacy subsidy. Section 6 maps the result to canonical zero-knowledge exchange
designs. Section 7 discusses the connection to LVR. Section 8 concludes.
2
Related work
2.1
AMM adverse-selection (closest)
Milionis et al. [13] introduce Loss-Versus-Rebalancing (LVR): a closed-form
continuous-time measure of the cost AMM liquidity providers incur when stale
prices are picked off by better-informed arbitrageurs. The two costs differ in
source: LVR’s arbitrageurs read an exogenous reference price; our informed
trader is the classical Kyle insider, and the cost arises from the AMM’s noisy
observation of flow.
Routledge, Shen, and Zetlin-Jones [16] characterize optimal liquidity provi-
sion in an AMM and study how price impact depends on trade size and on
the dynamics of liquidity provision. Milionis, Moallemi, and Roughgarden [12]
cast the profit-maximizing strategy of a monopolist liquidity provider into a
Bayesian belief-inference framework with a Myersonian mechanism-design in-
terpretation. Brahma et al. [4] developed a sequential Bayesian-update market
maker for binary-outcome prediction markets; that line is structurally related to
our committed-Bayesian-AMM rule (Bayesian posterior pricing without a zero-
profit constraint), although the model class differs.
2.2
Kyle-style microstructure
Kyle’s [11] single-period model with a risk-neutral monopolist informed trader,
an exogenous noise-trader pool, and a competitive risk-neutral market maker is
the framework we extend. Foster and Viswanathan [9] characterize the unique
linear equilibrium when multiple informed traders receive imperfectly correlated
signals. Huddart, Hughes, and Levine [10] modify Kyle by adding mandatory
ex-post disclosure of the informed trader’s transactions; this accelerates price
discovery and reduces insider profits — essentially the dual of our setup, in
which it is the market maker’s signal rather than the trader’s identity that be-
comes opaque. Chhaibi, Ekren, and Noh [6] study a Gaussian Kyle equilibrium
with a risk-averse informed trader holding an imperfect signal of the terminal
value; the imperfection is on the trader side, not the MM side. Non-fiduciary
MMs [1] capture rents through fees; our market maker is instead constrained to
a Bayesian rule and bears the cost. Viswanathan and Xing [17] analyze informed-
trader information acquisition at entropy cost; another direction of imperfection


### Page 4

4
Y. Nakamura
distinct from ours. A separate strand lets the market maker condition on a noisy
observation of the asset value alongside the order flow: Qiu and Zhou [15] solve
such a continuous-time Kyle model under partial maker observation. Our coars-
ening is an explicit additive privacy channel on the flow, and our contribution
is the closed-form welfare subsidy it induces under committed Bayesian pricing,
not the imperfect-observation equilibrium itself.
2.3
Dark-pool and privacy-preserving market structure
Zhu [19] and Buti, Rindi, and Werner [5] analyze dark-pool trading as a routing
equilibrium, in which informed and uninformed orders self-select between a lit
market and a dark pool based on execution risk. The mechanism is routing-based
segmentation, which is mathematically distinct from σ-algebra coarsening of a
single market’s signal. Bergemann and Morris [3] give the general information-
design framework that subsumes σ-algebra coarsening as a special case; we apply
it implicitly. Zhang et al. [18] analyze maximal extractable value in batch-auction
designs (including a discussion of Penumbra), showing that block-builder reorder-
ing of batch contents can still extract MEV; their framework is combinatorial-
market (Fisher and Arrow–Debreu) and complementary to ours.
For application targets, we read the Renegade [2] and Penumbra [14] protocol
specifications directly; we discuss applicability in Section 6.
3
Model setup
3.1
Primitives
Let (Ω, F, P) be a probability space supporting the following independent Gaus-
sian random variables:
v ∼N(p0, σ2
v),
σv > 0,
u ∼N(0, σ2
u),
σu > 0,
u ⊥⊥v,
ε ∼N(0, σ2
ε),
σε ≥0,
ε ⊥⊥(v, u).
The random variable v is the asset’s terminal value and p0 the common prior
mean. u is the aggregate flow of uninformed (noise) traders, independent of v.
ε is privacy noise introduced by the exchange mechanism (see Section 6 for the
realization in specific zero-knowledge designs).
3.2
Players and strategies
There is one informed trader (the Kyle insider) who observes v at time 0 and
submits an order of size x. We restrict attention to linear strategies x = β(v−p0)
for β ∈R>0, to be determined in equilibrium.
The noise-trader aggregate contributes order size u as above. Total order flow
is
y = x + u.


### Page 5

The Privacy Subsidy
5
The market maker (MM) does not observe y directly. Instead, the MM observes
the privacy-noisy signal
˜y = y + ε.
The privacy noise ε perturbs only the signal on which the MM prices (for instance,
the observed reserve state); the protocol still settles the true net order y = x+u
at the resulting price. This signal-versus-settlement gap is what makes the MM’s
expected P&L against the real flow nonzero (Section 5). The MM is a committed
Bayesian AMM: a smart-contract pricing rule that mechanically computes
p(˜y) = E[v | ˜y]
which is the competitive price conditional on ˜y; the maker breaks even on its
own signal but not against the real flow y, which it cannot observe (Remark 2).
In a committed smart-contract setting the rule is fixed by the mechanism, so
the maker cannot re-optimize away this loss, and the expected loss against the
real flow is absorbed by the protocol’s LP pool. We motivate the committed-rule
setting in Section 3.4.
3.3
Equilibrium concept
We seek a linear equilibrium of the form
x = β(v −p0),
p(˜y) = p0 + λ˜y,
where (β, λ) ∈R2
>0 satisfy:
1. Bayesian rationality of pricing: p(˜y) = E[v | ˜y] under the conjectured strategy
β.
2. Best response of informed trader: β(v −p0) maximizes the informed trader’s
expected profit E[(v −p(˜y)) · x | v], given λ.
3.4
The committed-Bayesian-AMM framing
The maker’s restriction to the coarse signal ˜y, not any departure from compet-
itive pricing, is the modeling feature distinguishing our setup from textbook
Kyle (Remark 2). We adopt this in order to match the design of contemporary
on-chain pricing mechanisms, in which:
– the pricing rule is encoded in a smart contract and is mechanically applied to
the observable input;
– the input is privacy-noised by construction (e.g., via differential privacy);
– the resulting expected loss is borne by liquidity providers or the protocol
treasury, and is recouped through trading fees.
This structure parallels the LVR analysis of automated market makers in Milionis
et al. [13], where the MM’s pricing rule is the constant-function curve and the
cost is borne by LPs. We return to this connection in Section 7.


### Page 6

6
Y. Nakamura
Idealized benchmark, not literal model. The committed-Bayesian-AMM is an
idealized normative benchmark: what an informationally optimal smart-contract
pricing rule would look like under additive privacy noise. The closest real-world
instantiation is a constant-function AMM augmented with differential-privacy
noise injection, treated in detail in Section 6. The benchmark’s value is to isolate
the welfare cost of additive privacy noise, yielding a closed-form quantity that
practical mechanisms in this class must internalize at the fee level.
3.5
Other modeling choices
Four further assumptions warrant brief comment. Linearity. We restrict to x =
β(v −p0), Kyle’s standard restriction (see Kyle [11], §3); a formal treatment
of nonlinear equilibria under privacy noise is outside our scope. Independence
ε ⊥⊥(v, u). Adaptive privacy mechanisms whose noise correlates with the flow it
perturbs are an interesting separate problem; our result establishes the uncon-
ditional baseline. Gaussianity. The closed-form subsidy is Gaussian-specific; the
qualitative existence of a positive privacy-induced LP loss generalizes to other
tractable distributions. Endogenous σε. A privacy-utility tradeoff that optimizes
σε under additional constraints is a natural extension we do not pursue here.
4
Equilibrium under privacy-noisy observation
This section contains the paper’s main equilibrium result.
Theorem 1 (Linear equilibrium under privacy-noisy observation). Fix
σv, σu > 0 and σε ≥0. The unique linear equilibrium of the model of Section 3
has
λ =
σv
2
√
σ2u + σ2ε
,
β =
√
σ2u + σ2ε
σv
.
(1)
Proof. Under the linear strategy x = β(v −p0) and price p = p0 + λ˜y, the signal
˜y is jointly Gaussian with v:
˜y = β(v −p0) + u + ε
has mean 0, variance β2σ2
v +σ2
u +σ2
ε, and covariance with v equal to Cov(v, ˜y) =
βσ2
v. By the projection formula for jointly Gaussian variables,
E[v | ˜y] = p0 +
βσ2
v
β2σ2v + σ2u + σ2ε
· ˜y.
(2)
The Bayesian-rationality condition matches this against p0 + λ˜y, yielding
λ =
βσ2
v
β2σ2v + σ2u + σ2ε
.
(3)


### Page 7

The Privacy Subsidy
7
For the informed trader’s best response, condition on v and optimize over x
given the MM’s price schedule. Since u, ε ⊥⊥v implies E[u | v] = E[ε | v] = 0,
E[(v −p(˜y)) · x | v] = E[(v −p0 −λ(x + u + ε)) · x | v]
= (v −p0)x −λx2.
This is strictly concave in x with second derivative −2λ < 0. The unique maxi-
mizer is
x∗= v −p0
2λ
,
so the best-response coeﬀicient is β = 1/(2λ).
Substituting β = 1/(2λ) into (3) and simplifying:
λ
( 1
4λ2 σ2
v + σ2
u + σ2
ε
)
= σ2
v
2λ,
σ2
v
4λ + λ(σ2
u + σ2
ε) = σ2
v
2λ,
λ(σ2
u + σ2
ε) = σ2
v
4λ,
λ2 =
σ2
v
4(σ2u + σ2ε).
Taking the positive root (since λ > 0) yields λ = σv/(2
√
σ2u + σ2ε), and substi-
tuting back gives β = 1/(2λ) =
√
σ2u + σ2ε/σv, establishing (1).
Uniqueness within the class of linear equilibria follows from strict concavity
of the informed trader’s objective (unique x∗given λ) together with the fact that
substituting β = 1/(2λ) into (3) reduces the system to λ2 = σ2
v/(4(σ2
u + σ2
ε)),
which has a unique positive root.
⊓⊔
Remark 1 (Sanity check: no-privacy limit).
Setting σε = 0 in (1) recovers
the classical Kyle [11] equilibrium λ = σv/(2σu), β = σu/σv. The committed
Bayesian AMM coincides with the competitive zero-profit MM exactly in the
no-privacy limit; the framing departure from textbook Kyle is inactive when
σε = 0.
Remark 2 (The subsidy is intrinsic to coarse-signal pricing).
The privacy subsidy is not an artifact of the committed-pricing label; it is
the unavoidable cost of pricing on a signal strictly coarser than the executed
flow. Two notions of zero profit must be separated. Zero profit conditional on
the maker’s information σ(˜y) forces p = E[v | ˜y], which is at once the Bertrand-
competitive price under coarsened observation and our committed Bayesian rule;
since y = x + u is not σ(˜y)-measurable when σε > 0, this eﬀicient price earns
the negative profit E[(p −v) y] = −λσ2
ε = −|πM| on the real flow. Zero profit
unconditionally against the real flow E[(v −p) y] = 0 instead gives ˜λ = σv/(2σu),
independent of σε; but this rule over-reacts to ˜y (its quote is not the posterior
mean), so it is not implementable by a price-taking maker that observes only


### Page 8

8
Y. Nakamura
˜y: a rival quoting the posterior would undercut it. Informational eﬀiciency and
zero profit against the real flow are therefore incompatible whenever σε > 0,
and the wedge between them is exactly the privacy subsidy λσ2
ε. The subsidy is
the generic competitive outcome of coarse-signal pricing, not a consequence of
relaxing zero profit; the Penumbra design of Section 6.2, where πM = 0 because
the maker prices on and trades against the same observable, is the converse —
no coarsening, no subsidy.
4.1
Comparative statics
The equilibrium has clean comparative statics in σε.
Proposition 1 (Comparative statics). The equilibrium of Theorem 1 satis-
fies:
1. ∂λ/∂σε < 0: the price-impact coeﬀicient strictly decreases as privacy noise
increases.
2. ∂β/∂σε > 0: the informed-trader strategy intensifies as privacy noise in-
creases.
3. (Half-revealing identity.) λβ = 1/2 for all σε ≥0.
Proof. Direct differentiation of (1) gives (i) and (ii). For (iii),
λβ =
σv
2
√
σ2u + σ2ε
·
√
σ2u + σ2ε
σv
= 1
2
identically.
⊓⊔
The identity λβ = 1/2 holds in textbook Kyle, where it is the well-known half-
revealing property: the equilibrium price moves halfway from the prior toward
the true value, on average. Our result is that this identity persists exactly under
privacy noise — a robustness statement about Kyle’s half-revealing property,
not a novel quantity. Substituting the equilibrium back into ˜y yields
p = p0 + λβ(v −p0) + λ(u + ε) = p0+v
2
+ λ(u + ε).
The conditional mean E[p | v] = (p0 + v)/2 is independent of σε; only the
conditional variance Var(p | v) = λ2(σ2
u + σ2
ε) = σ2
v/4 is also independent of σε.
Both the information content and the realized noise of the price are preserved
by privacy at the price level.
The cost of privacy is therefore not visible at the level of the price’s distribu-
tion conditional on v. As we show in Section 5, the cost appears instead in the
expected P&L of the market maker against informed flow, and this is what the
LP pool / protocol treasury must absorb.
5
Welfare decomposition: the privacy subsidy
This section computes the per-period expected profit or loss of each agent under
the equilibrium of Theorem 1 and identifies the privacy subsidy as a closed-form
quantity transferred from the protocol/LP pool to traders.


### Page 9

The Privacy Subsidy
9
5.1
Per-agent expected P&L
The three relevant per-period expected quantities are:
πI := E[(v −p) · x],
(informed trader’s expected profit),
πN := E[(v −p) · u],
(noise traders’ expected net P&L, a loss),
πM := E[(p −v) · (x + u)],
(MM/protocol expected profit on flow).
By construction πI + πN + πM = 0: the three components form a zero-sum
decomposition of the total trade-realized P&L against the asset’s terminal value
v.
Lemma 1 (Per-agent P&L formulas). Under the equilibrium (β, λ) of The-
orem 1:
πI = + 1
2 σv
√
σ2u + σ2ε,
(4)
πN = −
σv σ2
u
2
√
σ2u + σ2ε
,
(5)
πM = −
σv σ2
ε
2
√
σ2u + σ2ε
.
(6)
Proof. Use x = β(v −p0), u, ε ⊥⊥v, and the half-revealing identity λβ = 1/2
from Proposition 1.
(i) Informed.
πI = E[(v −p0 −λ(x + u + ε)) · β(v −p0)]
= β E[(v −p0)2] −λβ E[(x + u + ε)(v −p0)]
= β σ2
v −1
2 β σ2
v = 1
2 β σ2
v.
Substituting β =
√
σ2u + σ2ε/σv yields (4).
(ii) Noise. Since u ⊥⊥(x, ε) and E[u] = 0,
πN = E[(v −p0 −λ(x + u + ε)) · u] = −λ E[u (x + u + ε)] = −λ σ2
u.
With λ = σv/(2
√
σ2u + σ2ε), this gives (5).
(iii) MM/protocol. By the zero-sum identity,
πM = −(πI + πN) = −1
2 σv
√
σ2u + σ2ε +
σv σ2
u
2
√
σ2u + σ2ε
= −
σv σ2
ε
2
√
σ2u + σ2ε
,
which is (6).
⊓⊔
5.2
The privacy subsidy
The main welfare result follows directly.


### Page 10

10
Y. Nakamura
Theorem 2 (Privacy subsidy).
Under the equilibrium of Theorem 1, the
protocol’s expected loss per period is
|πM| =
σv σ2
ε
2
√
σ2u + σ2ε
≥0,
(7)
with equality if and only if σε = 0. The quantity |πM| is the privacy subsidy: the
per-period transfer from the protocol/LP pool to traders, induced by the privacy
mechanism. For protocol break-even, the total fees collected per period must satisfy
feesperiod ≥|πM|.
Proof. Equation (7) is (6) of Lemma 1; non-negativity is immediate. Equality at
σε = 0 recovers the textbook-Kyle MM zero-profit identity (Remark 1).
⊓⊔
Naming and fee model. We label |πM| privacy subsidy as a memorable analog
to LVR; equivalent neutral phrasings are noise-induced LP loss or protocol’s
adverse-selection cost from privacy. The break-even bound is computed against
the no-fee equilibrium: a per-trade fee f breaks the linear-strategy structure
(informed traders cease trading when |v−p0| < f), so a complete fee-equilibrium
analysis with endogenous volume response is left for future work.
5.3
Comparative statics of the subsidy
Proposition 2 (Subsidy asymptotics and shape). Let |πM|(σε) denote the
subsidy of (7) as a function of σε ≥0 with σv, σu fixed.
1. Low-privacy expansion: as σε ↓0, |πM|(σε) =
σv
2σu σ2
ε + O(σ4
ε).
2. High-privacy limit: as σε →∞, |πM|(σε) = 1
2 σv σε + O(σ−1
ε ).
3. |πM| is strictly increasing in σε on [0, ∞).
4. |πM| has a single inflection point at σ⋆
ε =
√
2 σu: it is convex on [0, σ⋆
ε] and
concave on [σ⋆
ε, ∞).
Proof (Proof of (iii)–(iv)). Differentiating |πM| twice in σε,
∂|πM|
∂σε
= σv σε (2σ2
u + σ2
ε)
2 (σ2u + σ2ε)3/2
> 0
for σε > 0, establishing (iii). The second derivative simplifies to
∂2|πM|
∂σ2ε
= σv σ2
u (2σ2
u −σ2
ε)
2 (σ2u + σ2ε)5/2 ,
which vanishes exactly at σ2
ε = 2σ2
u, is positive for σ2
ε < 2σ2
u, and negative for
σ2
ε > 2σ2
u. This gives (iv).
⊓⊔
Item (i): for small privacy noise, the subsidy is quadratic in σε — doubling
the privacy parameter quadruples the LP-pool cost. Item (ii): asymptotically
linear growth in the high-privacy regime. Item (iv): the protocol’s marginal cost
∂|πM|/∂σε is itself increasing for small σε but eventually decreasing as σε grows
past
√
2 σu — past this threshold, additional privacy is less expensive at the
margin. The inflection at σ⋆
ε =
√
2 σu is a structural feature of the square-root
denominator in (7).


### Page 11

The Privacy Subsidy
11
5.4
Welfare incidence
Corollary 1 (Noise traders also benefit from privacy). ∂πN/∂σε > 0 for
all σε > 0: the noise (uninformed) traders’ expected loss is strictly decreasing in
the privacy parameter.
Proof. Differentiating (5),
∂πN
∂σε
=
σv σ2
u σε
2 (σ2u + σ2ε)3/2 > 0
for σε > 0.⊓⊔
Combined with Theorem 2, the welfare picture under privacy is therefore:
– informed trader gains: ∂πI/∂σε > 0;
– noise trader gains (loses less): ∂πN/∂σε > 0;
– protocol/LP pool loses by exactly that sum: ∂|πM|/∂σε > 0;
– total welfare is preserved (zero sum).
Privacy improves πN, but not at the informed trader’s expense. Both trader
types gain; the entire transfer is borne by the protocol. In the low-privacy regime,
the leading-order Taylor expansions of πI and πN around σε = 0 are equal,
πI(σε) −πI(0) = πN(σε) −πN(0) =
σv
4σu
σ2
ε + O(σ4
ε),
so the privacy subsidy is split symmetrically between informed and noise traders
to leading order. The asymmetry only appears at higher orders: in the high-
privacy limit, the informed trader captures essentially all the subsidy (πI ∼
σvσε/2) while the noise trader’s loss vanishes (πN →0, i.e. their gain over the
classical Kyle benchmark saturates at σvσu/2).
Remark 3 (The privacy ”gain” is gross-of-fees; Corollary 1 is welfare-neutral net-
of-fees). The statement “noise traders also benefit from privacy” (Corollary 1)
is a gross-of-fees observation about the no-fee equilibrium of Theorem 1. We
now show that, at the same no-fee equilibrium volumes, charging the break-even
fee of Theorem 2 via a volume-proportional levy exactly cancels both traders’
incremental gains.
At equilibrium the expected absolute volumes are E|x| = (σv/2λ)
√
2/π and
E|u| = σu
√
2/π, so total volume Q := E|x|+E|u| =
√
2/π (
√
σ2u + σ2ε+σu) using
λ = σv/(2
√
σ2u + σ2ε) from Theorem 1. The break-even rate is f = |πM|/Q. Each
side pays its volume share:
f · E|x| = σv (
√
σ2u + σ2ε −σu)
2
= πI(σε) −πI(0),
f · E|u| = σv σu (
√
σ2u + σ2ε −σu)
2
√
σ2u + σ2ε
= πN(σε) −πN(0).
Each fee equals the corresponding trader’s incremental gain over the σε = 0
baseline; net-of-fees, both πI −f E|x| = σvσu/2 and πN −f E|u| = −σvσu/2


### Page 12

12
Y. Nakamura
revert to the classical Kyle values, while the MM is exactly compensated. Privacy
is therefore exactly welfare-neutral under the volume-proportional break-even fee,
at the partial-equilibrium level of analysis (no-fee equilibrium volumes, with fee
revenue redistributed back to the LP pool). The full fee-equilibrium analysis, in
which the fee distorts the linear-strategy structure as flagged after Theorem 2,
remains open and may yield additional deadweight loss.
6
Application to zero-knowledge exchange designs
The model of Section 3 applies cleanly to one class of zero-knowledge exchange
designs: smart-contract AMMs whose observation of order flow is perturbed by
an explicit additive Gaussian noise injection. We treat this canonical application
in Section 6.1, then situate three nearby privacy designs that do not fit our
framework as currently formulated in Section 6.2.
6.1
Primary application: shielded AMMs with DP-style noise
A shielded AMM with differential-privacy (DP) noise is a constant-function-style
AMM augmented with a privacy layer that injects calibrated Gaussian noise into
the observable order flow before the AMM applies its update rule. Concretely,
after each trade the protocol observes ˜y = y + ε with ε ∼N(0, σ2
ε) drawn by the
privacy mechanism, and the AMM updates reserves — and therefore the spot
price — according to this noisy signal. The privacy parameter σε is exactly the
standard deviation of the injected DP noise.
The mapping is literal: σε in our framework equals the DP noise scale in the
implementation. Theorem 2 therefore yields a direct break-even fee prescription
for any such shielded AMM: per-period fees must total at least the subsidy |πM|
to compensate the LP pool. Appendix A tabulates the resulting fee floor in
USD per day under a BTC/USDT calibration; at σε = σu, the LP/protocol
must collect approximately $1M/day — comparable to the entire revenue from
a 0.1% fee on $1B of daily volume.
This setting pairs cleanly with the DP-feasibility analysis of Chitra, Angeris,
and Evans [7], who study a Uniform Random Execution mechanism that achieves
(ε, δ)-DP in constant-function market makers and characterize the privacy pa-
rameter as a function of curvature and trade count. Their analysis is on the
realizability side: when and how DP can be achieved in a CFMM. Our frame-
work is the complementary welfare side: given that a DP layer of intensity σε is
in place, what does the LP pool pay?
6.2
Mechanisms outside our framework
Three nearby privacy designs warrant separate analysis frameworks that our
additive-Gaussian-noise model does not capture.


### Page 13

The Privacy Subsidy
13
Penumbra-style batched swaps. Penumbra [14] clears swaps via per-block batches
in which the cleared price depends on the aggregate batch flow. The Bayesian-
MM observation is the exact aggregate Yτ = ∑
t(xt + ut) over τ pooled noise-
trader draws — not a noise-perturbed version of Yτ. Treating one batch as one
period (so per-batch noise-trader variance is τσ2
u), direct calculation gives λ =
σv/(2σu
√τ) and the informed batch-total coeﬀicient β = σu
√τ/σv — textbook
Kyle with the rescaling σu →σu
√τ. Because the MM both prices on and trades
against the same observable Yτ, the Bayesian projection identity gives πM =
0 exactly. Batching reshapes market depth and informed-trader intensity but
generates no privacy subsidy under this framework.
Suave-style sealed-bid order-flow auctions. Sealed bidding with delayed reveal [8]
creates temporal information asymmetry rather than additive observation noise.
The block proposer commits to a price ex ante and trades against revealed flow
ex post; the adverse-selection cost in this design is closer to LVR’s stale-price
arbitrage (Section 7) than to our σε-noise setting. A continuous-time analysis
with explicit time-lag is required.
Renegade-style midpoint-pegged crossing. Renegade [2] matches peer orders at
an external lit-exchange midpoint via MPC: the on-chain mechanism consumes
no flow signal to compute price. Such oracle-pegged designs fall entirely outside
any Kyle-style analysis, since price discovery is exogenous.
7
Connection to Loss-Versus-Rebalancing
The privacy subsidy of Theorem 2 occupies the same conceptual slot as the Loss-
Versus-Rebalancing (LVR) measure of Milionis et al. [13]. Both are closed-form,
per-period welfare quantities that measure the adverse-selection cost borne by
an automated pricing mechanism in the presence of informed traders, and both
yield direct break-even fee prescriptions.
The source of the cost differs across the two results:
– LVR captures the cost of stale prices: the AMM’s price function is committed
and lags the true reference price which arbitrageurs can read externally. The
information asymmetry is temporal.
– The privacy subsidy captures the cost of privacy noise: the AMM observes
its price-relevant signal with additive Gaussian noise injected by the privacy
mechanism. The information asymmetry is informational, not temporal.
A natural open question is whether these costs combine additively in
a continuous-time AMM that is simultaneously price-lagged and privacy-
aggregated. A formal model would require lifting LVR’s continuous-time setup
and our single-period Kyle setup into a common framework, which we do not
attempt here. As a heuristic suggestion for follow-up work, we conjecture that
the break-even fee in such a setting decomposes to leading order as


### Page 14

14
Y. Nakamura
feesperiod ≥LVR + |πM|,
but emphasize that this is speculative. The cross-terms between time-lag and
privacy noise need not vanish at higher orders: an arbitrageur exploiting a stale
price may also exploit the privacy-noise statistics, and these channels’ welfare
costs need not be independent. A vanishing of cross-terms at leading order would
require ε to be temporally uncorrelated with the stale-price process. A rigorous
treatment is left for future work.
8
Conclusion
We have derived the closed-form linear Kyle equilibrium in a single-period mar-
ket in which a committed Bayesian AMM observes order flow perturbed by inde-
pendent Gaussian privacy noise of scale σε. The equilibrium price-impact coeﬀi-
cient is λ = σv/(2
√
σ2u + σ2ε), monotonically decreasing in σε. The corresponding
informed-trader strategy intensifies symmetrically as β =
√
σ2u + σ2ε/σv, and the
product λβ = 1/2 is invariant in σε. The welfare decomposition identifies a per-
period transfer |πM| = σvσ2
ε/(2
√
σ2u + σ2ε) from the protocol/LP pool to traders.
This is the privacy subsidy, the break-even fee that any privacy-aggregated ex-
change must charge to compensate its liquidity layer. The result applies directly
to shielded AMMs with additive-noise (differential-privacy) injection. Related
privacy designs — Penumbra-style batched swaps, Suave-style sealed-bid order-
flow auctions, and oracle-pegged crossings such as Renegade — require separate
frameworks: batching reduces to Kyle with rescaled noise-trader variance (no
subsidy under Bayesian MM); sealed-bid auctions sit closer to LVR’s temporal-
asymmetry regime; oracle-pegged designs fall entirely outside Kyle.
Future work. Extensions left to subsequent work include a Glosten–Milgrom bid-
ask-spread analog under privacy noise; other privacy mechanisms (directional-
only, bucketed, time-delayed observation); multi-period dynamics aimed at a
combined LVR-plus-privacy decomposition; mechanized formalization in a proof
assistant; and empirical calibration of σε from live zero-knowledge exchange
traces.
A
Numerical illustration
The closed-form results of Theorems 1 and 2 admit immediate numerical evalu-
ation. Figure 1 plots |πM|(σε) for σv = σu = 1 over σε ∈[0, 5]; Tables 1 and 2
tabulate λ, β, and |πM| at representative parameter values.


### Page 15

The Privacy Subsidy
15
0
1
2
3
4
5
0
1
2
σ⋆
ε =
√
2 σu
σε (privacy noise scale)
|πM| (privacy subsidy)
Fig. 1. Privacy subsidy |πM| vs. σε for σv = σu = 1. The convexity-to-concavity
inflection at σ⋆
ε =
√
2 marks the transition between the quadratic low-privacy regime
and the linear high-privacy regime.
A.1
Dimensionless table
Table 1 reports λ, β, and |πM| in units where σv = σu = 1. The convexity-
to-concavity inflection of |πM| at σ⋆
ε =
√
2 σu ≈1.414 (Proposition 2(iv)) is
bracketed by the σε ∈{1.0, 1.414, 2.0} rows.
σε
λ
β
|πM|
note
0 0.500 1.000 0.000
textbook Kyle
0.5 0.447 1.118 0.112 low-privacy regime
1.0 0.354 1.414 0.354
σε = σu
√
2 0.289 1.732 0.577 σε = σ⋆
ε (inflection)
2.0 0.224 2.236 0.894
past inflection
3.0 0.158 3.162 1.423
high-privacy
5.0 0.098 5.099 2.451
far high-privacy
Table 1. Dimensionless equilibrium values for σv = σu = 1, varying σε. The privacy
subsidy |πM| grows quadratically near σε = 0 (slope →0), becomes maximally steep
near σ⋆
ε =
√
2 σu, and asymptotes to linear |πM| ≈σε/2 for large σε.
A.2
BTC-calibrated example
For an illustrative BTC/USDT calibration, take a per-day window with σv =
$3,000 (corresponding to ∼3% daily volatility on a $100,000 asset) and σu =
1,000 BTC per day. Table 2 reports |πM| in USD per day across several σε values,
expressed as a multiple of σu.


### Page 16

16
Y. Nakamura
σε/σu |πM| (USD/day) As fraction of σvσu
0.1
$∼15,000
0.0050
0.5
$∼335,000
0.112
1.0
$∼1,060,000
0.354
√
2
$∼1,730,000
0.577
2.0
$∼2,680,000
0.894
Table 2. Per-day privacy subsidy in USD for a BTC/USDT calibration with σv =
$3,000/day and σu = 1,000 BTC/day. (σu is the noise-trader-component standard
deviation, not total daily volume; typical BTC/USDT daily volume is one to two
orders of magnitude larger.) At σε = σu, the LP/protocol must collect approximately
$1M/day in fees to break even.
For context, BTC/USDT spot volume on a typical centralized exchange is
on the order of $1–$5 billion per day. A 0.1% fee on $1B daily volume yields
$1M/day in revenue. Under the calibration of Table 2, this revenue roughly
breaks even against the privacy subsidy at σε = σu (the subsidy is ∼$1.06M,
so a 0.1% fee on $1B falls about 6% short), and falls further short for larger σε.
The implication for privacy-aggregated exchange designers is that fee schedules
and privacy parameters cannot be chosen independently.
References
1. Aase, K.K., Øksendal, B.: Strategic insider trading equilibrium with a non-fiduciary
market maker. arXiv preprint arXiv:1908.08777 (2019)
2. Bender, C., Kraut, J.: Renegade whitepaper, protocol specification v0.6. https:
//whitepaper.renegade.fi/ (2024), accessed 2026-05-15
3. Bergemann, D., Morris, S.: Information design: A unified perspective. Journal of
Economic Literature 57(1), 44–95 (2019)
4. Brahma, A., Chakraborty, M., Das, S., Lavoie, A., Magdon-Ismail, M.: A Bayesian
market maker. In: Proceedings of the 13th ACM Conference on Electronic Com-
merce (EC 2012) (2012)
5. Buti, S., Rindi, B., Werner, I.M.: Dark pool trading strategies, market quality and
welfare. Journal of Financial Economics 124(2), 244–265 (2017)
6. Chhaibi, R., Ekren, I., Noh, E.: Solvability of the Gaussian Kyle model with im-
perfect information and risk aversion. arXiv preprint arXiv:2501.16488 (2025)
7. Chitra, T., Angeris, G., Evans, A.: Differential privacy in constant function market
makers. In: Financial Cryptography and Data Security (FC 2022). Lecture Notes
in Computer Science, Springer (2022), iACR eprint 2021/1101
8. Flashbots: The future of MEV is SUAVE. https://writings.flashbots.net/
the-future-of-mev-is-suave (2024), accessed 2026-05-15
9. Foster, F.D., Viswanathan, S.: Strategic trading when agents forecast the forecasts
of others. Journal of Finance 51(4), 1437–1478 (1996)
10. Huddart, S., Hughes, J.S., Levine, C.B.: Public disclosure and dissimulation of
insider trades. Econometrica 69(3), 665–681 (2001)
11. Kyle, A.S.: Continuous auctions and insider trading. Econometrica 53(6), 1315–
1335 (1985)


### Page 17

The Privacy Subsidy
17
12. Milionis, J., Moallemi, C.C., Roughgarden, T.: A Myersonian framework for opti-
mal liquidity provision in automated market makers. In: Innovations in Theoretical
Computer Science (ITCS 2024) (2024), arXiv:2303.00208
13. Milionis, J., Moallemi, C.C., Roughgarden, T., Zhang, A.L.: Automated market
making and loss-versus-rebalancing. arXiv preprint arXiv:2208.06046 (2022)
14. Penumbra Labs: Penumbra protocol documentation. https://protocol.penumbra.
zone/ (2024), accessed 2026-05-15
15. Qiu, J., Zhou, Y.: Insider trading with dynamic asset under market makers’ partial
observations. AIMS Mathematics 8(10), 25017–25036 (2023). https://doi.org/
10.3934/math.20231277
16. Routledge, B.R., Shen, Y., Zetlin-Jones, A.: Automated exchange economies (2025),
working paper, Tepper School of Business
17. Viswanathan, S., Xing, H.: Flexible information acquisition in the Kyle model.
arXiv preprint arXiv:2603.21842 (2026)
18. Zhang, M., Li, Y., Sun, X., Chen, E., Chen, X.: Maximal extractable value in
batch auctions. In: Proceedings of the 26th ACM Conference on Economics and
Computation (2025)
19. Zhu, H.: Do dark pools harm price discovery? Review of Financial Studies 27(3),
747–789 (2014)

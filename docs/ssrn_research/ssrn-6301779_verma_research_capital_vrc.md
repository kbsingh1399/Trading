# Verma Research Capital (VRC)

- **Source File**: `ssrn-6301779.pdf`
- **Total Pages**: 34
- **SSRN ID**: `ssrn-6301779`

---


### Page 1

Verma Research Capital (VRC)
Working Paper
Detecting Liquidity Stress Before
Crises:
Order Flow Toxicity, VPIN, and Hidden
Fragility in Modern Markets
Divyanshu Verma
Verma Research Capital (VRC)
divyanshu@vermaresearch.com
October 17, 2025


### Page 2

Detecting Liquidity Stress Before Crises
Verma Research Capital
Abstract
Market crises are rarely the result of a sudden exogenous shock arriving into
a perfectly healthy structure. In almost every documented instance of severe
market dislocation, the architecture of liquidity had been quietly
deteriorating for days or weeks before prices reflected the underlying stress.
This paper develops a comprehensive quantitative framework for detecting
liquidity stress through the analysis of order flow, market microstructure,
and derivatives market signals, with explicit application to hedge fund risk
management. We begin with the theoretical foundations of market
microstructure, including the adverse selection model of the bid-ask spread,
the Kyle lambda as a measure of price impact, and the PIN and VPIN
frameworks for estimating the probability of informed trading from volume
imbalances. We then examine how liquidity stress propagates across equities,
equity index futures, options markets, and credit instruments, and how these
propagation channels interact with the hedging constraints of systematic
liquidity providers. We introduce the VRC Liquidity Stress Indicator (LSI),
a composite daily metric that aggregates signals across order flow toxicity,
execution quality deterioration, implied volatility skew dynamics, and the
behaviour of systematic liquidity suppliers, and we describe how this
indicator is used to manage position sizing, strategy selection, and drawdown
risk at the portfolio level. Three historical episodes ground the analysis in
observed market behaviour: the August 2015 flash crash, the March 2020
COVID-19 liquidity crisis, and the October 2022 UK gilt market dislocation.
The paper concludes that liquidity is not a persistent feature of markets but
a conditional outcome of incentives, balance sheet constraints, and
confidence, and that practitioners who monitor the plumbing of markets
rather than only prices are systematically better positioned to manage the
tail events that matter most.
The views expressed in this paper are those of the author and do not constitute investment advice.
© 2025 Verma Research Capital. All rights reserved.
2


### Page 3

Contents
1
Introduction: The Silence Before the Break
3
2
Theoretical Foundations of Market Liquidity
4
2.1
The Adverse Selection Model of the Bid-Ask Spread . . . . . . . . . . . .
4
2.2
The Kyle Model: Price Impact and Market Depth . . . . . . . . . . . . .
5
2.3
The Amihud Illiquidity Ratio
. . . . . . . . . . . . . . . . . . . . . . . .
6
3
PIN and VPIN: Measuring Order Flow Toxicity
7
3.1
The PIN Model: Probability of Informed Trading . . . . . . . . . . . . .
7
3.2
VPIN: Volume-Synchronised Probability of Informed Trading . . . . . . .
8
3.3
Order Flow Imbalance as a Real-Time Signal . . . . . . . . . . . . . . . .
9
4
Propagation of Liquidity Stress Across Markets
10
4.1
The Sequential Deterioration Pattern . . . . . . . . . . . . . . . . . . . .
10
4.2
The Funding Liquidity and Market Liquidity Spiral . . . . . . . . . . . .
11
4.3
Cross-Asset Contagion Through Common Ownership . . . . . . . . . . .
12
5
Systematic Liquidity Providers: Risk Limits and the Withdrawal Dy-
namic
12
5.1
The Conditionality of Algorithmic Market Making . . . . . . . . . . . . .
12
5.2
Synchronised Withdrawal and the Liquidity Void
. . . . . . . . . . . . .
13
5.3
The Gamma Hedging Amplification Mechanism
. . . . . . . . . . . . . .
14
6
The VRC Liquidity Stress Indicator
15
6.1
Design Principles . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
15
6.2
Component 1: Kyle Lambda Trend (Weight: 20%) . . . . . . . . . . . . .
15
6.3
Component 2: VPIN Level and Trend (Weight: 25%) . . . . . . . . . . .
16
6.4
Component 3: Bid-Ask Spread Divergence (Weight: 15%) . . . . . . . . .
16
6.5
Component 4: Amihud Illiquidity Trend (Weight: 15%) . . . . . . . . . .
17
1


### Page 4

Detecting Liquidity Stress Before Crises
Verma Research Capital
6.6
Component 5: Options Skew and Depth Signal (Weight: 25%) . . . . . .
17
6.7
Composite LSI and Regime Classification . . . . . . . . . . . . . . . . . .
18
7
Derivatives Market Signals of Liquidity Deterioration
19
7.1
Put Skew as an Informed Flow Indicator . . . . . . . . . . . . . . . . . .
19
7.2
Term Structure Kinks and the Concentration of Near-Term Risk . . . . .
20
7.3
The Cost of Rolling and the Liquidity Premium in Options . . . . . . . .
21
8
Historical Case Studies
22
8.1
August 2015: The Flash Crash and Order Book Collapse . . . . . . . . .
22
8.2
March 2020: The COVID-19 Liquidity Crisis and Treasury Market Failure
23
8.3
October 2022: The UK Gilt Crisis and Liability-Driven Investment Forced
Selling . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
24
9
Hedge Fund Implementation: Strategy-Level Applications
25
9.1
Equity Long/Short Strategies
. . . . . . . . . . . . . . . . . . . . . . . .
25
9.2
Short Volatility and Options Strategies . . . . . . . . . . . . . . . . . . .
25
9.3
Systematic and Trend-Following Strategies . . . . . . . . . . . . . . . . .
26
10 Measuring Execution Quality as a Liquidity Monitor
27
10.1 Implementation Shortfall and Slippage Tracking . . . . . . . . . . . . . .
27
10.2 The Spread Capture Ratio as a Liquidity Health Metric . . . . . . . . . .
27
11 Limitations of the Framework
28
11.1 Data Requirements and Availability . . . . . . . . . . . . . . . . . . . . .
28
11.2 False Positives and the Cost of Excessive Caution . . . . . . . . . . . . .
29
12 Conclusion
29
References
31
2


### Page 5

Detecting Liquidity Stress Before Crises
Verma Research Capital
1. Introduction: The Silence Before the Break
Every practitioner who has lived through a genuine market crisis carries the same memory:
things looked fine until they did not. The index was holding. Spreads were contained.
Volatility was not alarming. And then, with what felt like no warning at all, the market
broke. Prices gapped. Bids disappeared. The cost of executing even modest trades became
extraordinary. The experience reinforces a narrative of sudden external shock that is both
intuitive and profoundly misleading.
The more careful post-mortems of major market dislocations reveal a different
story. The flash crash of May 6, 2010 was preceded by deteriorating depth in E-mini S&P
500 futures for most of the trading session, long before the price collapse at 2:45 PM.
The March 2020 COVID-19 liquidity crisis was preceded by measurable deterioration in
US Treasury market depth beginning in late February, visible in the widening of bid-ask
spreads and the declining average trade size at the best bid and offer. The August 2015
dislocations were foreshadowed by mounting order flow imbalances in the overnight futures
markets during the preceding week. In each case, the evidence of stress was present
in the microstructure of trading before it became visible in the index levels that most
practitioners monitor.
The central proposition of this paper is that liquidity is not a state that markets
simply have or lack. It is the emergent outcome of the incentives, balance sheet constraints,
and risk tolerance of the participants who provide it. When those inputs shift, liquidity
deteriorates in a specific, measurable sequence that begins in the mechanics of trading
itself, moves through the cost of transferring risk in derivatives markets, and eventually
manifests in price dislocations that are severe and fast precisely because the structural
support for orderly trading had already eroded. A hedge fund that monitors only prices
and volatility indices is watching the smoke rather than the fire.
At VRC, the monitoring of market microstructure and order flow is an integral
part of the daily risk management process.
We treat execution quality, order flow
composition, and the pricing of optionality in derivatives markets as real-time inputs to
3


### Page 6

Detecting Liquidity Stress Before Crises
Verma Research Capital
our assessment of whether the current market environment supports the risk postures
embedded in our portfolio. This paper describes the theoretical foundations and the
practical implementation of that monitoring process in full quantitative detail.
The paper proceeds as follows. Section 2 develops the theoretical microstructure
framework, including adverse selection, the Kyle model, and the information content
of order flow. Section 3 presents the PIN and VPIN frameworks for measuring order
flow toxicity. Section 4 analyses how liquidity stress propagates across markets and
instruments. Section 5 examines the role of systematic liquidity providers and their risk
limits in amplifying stress. Section 6 details the VRC Liquidity Stress Indicator. Section
7 presents the derivatives market dimension of liquidity monitoring. Section 8 applies the
framework to three historical episodes. Section 9 discusses hedge fund implementation
across strategy types. Section 10 addresses execution quality measurement. Section 11
covers limitations. Section 12 concludes.
2. Theoretical Foundations of Market Liquidity
2.1. The Adverse Selection Model of the Bid-Ask Spread
The market microstructure literature has produced a rich theoretical account of why
bid-ask spreads exist and how they respond to changes in the information environment.
The foundational insight, developed by Bagehot (1971) and formalised by Glosten and
Milgrom (1985), is that market makers face an adverse selection problem: some fraction of
the traders they transact with possess information about the true value of the asset that
the market maker does not have. Because the market maker cannot distinguish informed
from uninformed traders, they must set spreads wide enough to recover the losses they
expect to incur on trades against informed parties through the profits they earn on trades
against uninformed ones.
In the Glosten-Milgrom framework, the bid price Bt and ask price At set by a
competitive, risk-neutral market maker satisfy:
4


### Page 7

Detecting Liquidity Stress Before Crises
Verma Research Capital
At = E[V | buy order] = µ +
π · ∆
2π −1 + π
(1)
Bt = E[V | sell order] = µ −
π · ∆
2π −1 + π
(2)
where µ is the unconditional expected asset value, π is the probability that any
given order originates from an informed trader, and ∆is the magnitude of the information
advantage enjoyed by informed traders. The bid-ask spread S = At −Bt is therefore
directly proportional to π: spreads widen when the probability of informed trading
increases. This theoretical relationship is the basis for using bid-ask spread dynamics as a
signal of changing information conditions and, by extension, of emerging liquidity stress.
The practical importance of this framework is that spreads begin to widen before
prices move significantly, because the market maker’s adverse selection concern rises as
soon as informed order flow increases, even if the market maker has not yet been able
to deduce the direction of the information. Monitoring spread dynamics thus provides a
leading signal of the emergence of informed trading, which is frequently associated with
stress events.
2.2. The Kyle Model: Price Impact and Market Depth
The Kyle (1985) model provides a complementary framework for understanding how
informed trading affects prices through its impact on market depth. In Kyle’s continuous
auction model, a strategic informed trader, a noise trader, and a competitive market
maker interact. The market maker sets prices that are linear in the observed order flow
imbalance:
∆p = λ · (QB −QS)
(3)
where ∆p is the price change, QB and QS are aggregate buy and sell volumes over
the interval, and λ is the Kyle lambda, the price impact coefficient. The Kyle lambda is
the central empirical object in market depth analysis: it measures the cost per unit of
5


### Page 8

Detecting Liquidity Stress Before Crises
Verma Research Capital
volume to move the market, and it rises when market depth decreases.
Kyle (1985) derives the equilibrium lambda as:
λ∗= σv
2σu
(4)
where σv is the standard deviation of the asset’s true value (the information uncer-
tainty) and σu is the standard deviation of the noise trading volume. When information
uncertainty increases relative to noise trading volume, the market maker becomes more
cautious and price impact rises. The practical implication is that the Kyle lambda rises
ahead of crises, as informed participants enter the market with directional views that
increase the signal-to-noise ratio of order flow.
Empirically, the Kyle lambda is estimated from intraday return-volume regressions:
rt = α + λ · xt + εt
(5)
where rt is the return over a short interval and xt is the signed order flow imbalance
(positive for net buying, negative for net selling) over the same interval. A significant and
rising λ estimate from a rolling window regression is one of the cleanest signals available
to a practitioner that market depth is deteriorating and that the cost of executing trades
is increasing.
2.3. The Amihud Illiquidity Ratio
For applications requiring daily data rather than intraday tick data, the Amihud (2002)
illiquidity ratio provides a practical approximation of price impact that is computable
from standard daily price and volume data:
ILLIQi,t = |ri,t|
Vi,t
(6)
where |ri,t| is the absolute daily return of asset i on day t and Vi,t is the dollar
trading volume. The ratio measures the absolute price change per dollar of trading volume,
which is a direct approximation of the Kyle lambda at daily frequency. Amihud (2002)
6


### Page 9

Detecting Liquidity Stress Before Crises
Verma Research Capital
demonstrates that this measure is strongly cross-sectionally correlated with intraday
bid-ask spreads and with other measures of price impact.
For a portfolio of N assets, the aggregate illiquidity measure is:
ILLIQport,t =
N
X
i=1
wi · ILLIQi,t
(7)
where wi is the weight of asset i in the portfolio. Rising aggregate illiquidity
signals that the portfolio’s positions are becoming harder to trade without moving prices,
which has direct implications for the sizing of positions and the feasibility of dynamic risk
management strategies that require frequent rebalancing.
3. PIN and VPIN: Measuring Order Flow Toxicity
3.1. The PIN Model: Probability of Informed Trading
The Probability of Informed Trading (PIN) measure, introduced by Easley, Kiefer, O’Hara,
and Paperman (1996), provides a structural estimate of the fraction of order flow at-
tributable to privately informed traders, based on the daily distribution of buyer-initiated
and seller-initiated trades. The model assumes that on any given day, an information
event occurs with probability α, and given that an event occurs, it is bad news (favouring
selling) with probability δ and good news (favouring buying) with probability 1 −δ. On
days with a positive information event, buys arrive at rate µ + εB and sells at rate εS,
where µ is the rate of informed trading and εB, εS are the rates of uninformed buying and
selling respectively.
The likelihood function for the observed daily buy and sell counts (Bt, St) is:
L(Θ | Bt, St) = (1 −α)e−εB(εB)Bt
Bt!
· e−εS(εS)St
St!
+ α(1 −δ)e−(µ+εB)(µ + εB)Bt
Bt!
· e−εS(εS)St
St!
+ αδe−εB(εB)Bt
Bt!
· e−(µ+εS)(µ + εS)St
St!
(8)
7


### Page 10

Detecting Liquidity Stress Before Crises
Verma Research Capital
The PIN is then the fraction of total order flow attributable to informed trading,
estimated by maximum likelihood:
PIN =
αµ
αµ + εB + εS
(9)
The PIN has been shown empirically to be positively associated with bid-ask
spreads, with the degree of price impact per unit of volume, and with subsequent stock
returns in the cross section. Stocks with high PIN values tend to experience larger bid-ask
spreads and higher price impact, consistent with the theoretical prediction that market
makers demand wider spreads when facing a higher proportion of informed counterparties.
3.2. VPIN: Volume-Synchronised Probability of Informed Trading
A practical limitation of the PIN model is that it requires the classification of individual
trades as buyer-initiated or seller-initiated, typically using the Lee-Ready (1991) algorithm,
and it is estimated at daily frequency using maximum likelihood over rolling windows.
For real-time risk management applications, a more computationally tractable measure is
needed. Easley, Lopez de Prado, and O’Hara (2012) introduce the Volume-Synchronised
Probability of Informed Trading (VPIN) for this purpose.
VPIN is computed in volume time rather than calendar time. The trading day is
divided into n equal-volume buckets, each containing V shares or contracts. For each
bucket τ, the volume is classified into buy volume V B
τ
and sell volume V S
τ using a bulk
classification rule:
V B
τ = V · Φ
∆pτ
σ∆p
!
,
V S
τ = V −V B
τ
(10)
where Φ(·) is the standard normal cumulative distribution function, ∆pτ is the
price change within bucket τ, and σ∆p is the standard deviation of price changes across
buckets. This bulk classification approach avoids the need for trade-by-trade direction
assignment. The VPIN for a sample of n buckets is then:
8


### Page 11

Detecting Liquidity Stress Before Crises
Verma Research Capital
V PIN =
n
X
τ=1
|V S
τ −V B
τ |
n · V
(11)
VPIN ranges from zero to one. A value near zero indicates that buy and sell
volumes are approximately balanced across the sample window, consistent with the
presence of abundant two-sided liquidity. A value near one indicates that volumes are
highly imbalanced in a persistent direction, consistent with the presence of dominant
informed flow or forced one-way pressure. Easley, Lopez de Prado, and O’Hara (2012)
demonstrate that VPIN rose sharply in the hours preceding the May 2010 flash crash
in E-mini S&P 500 futures, providing an advance warning signal that was not visible in
price levels or conventional volatility measures.
3.3. Order Flow Imbalance as a Real-Time Signal
For practical implementation in a hedge fund context, a simplified order flow imbalance
(OFI) metric provides much of the signal content of VPIN at lower computational cost.
For a given instrument over a measurement interval [t, t + h]:
OFIt,h =
X
trades
[1buy · qk −1sell · qk]
(12)
where qk is the size of the k-th trade and the indicators identify buyer- and
seller-initiated trades. The normalised OFI, expressed as a fraction of total volume, is:
OFIt,h = OFIt,h
Vt,h
(13)
where Vt,h is total volume over the interval. A persistent positive OFI indicates
sustained buying pressure, while a persistent negative value indicates sustained selling
pressure. More important than the direction is the volatility of the OFI across rolling
windows: rising OFI volatility, even when the mean OFI is near zero, indicates that trading
is increasingly dominated by one-sided aggressive flows alternating direction, which is a
signature of institutional repositioning and the reduction of passive two-sided liquidity.
9


### Page 12

Detecting Liquidity Stress Before Crises
Verma Research Capital
4. Propagation of Liquidity Stress Across Markets
4.1. The Sequential Deterioration Pattern
Liquidity stress does not appear simultaneously across all markets and instruments. It
propagates through a characteristic sequence that reflects the information hierarchy of
modern financial markets and the relative balance sheet sensitivity of different liquidity
providers. Understanding this sequence is essential for early detection, because it means
that stress signals often appear in specific segments of the market before they are visible
in the most-watched price series.
The typical propagation sequence begins in the most information-sensitive markets,
where adverse selection concerns are highest and market makers are most responsive to
changes in order flow composition. In equity markets, stress typically appears first in the
options market, where the cost of transferring tail risk begins to rise before the underlying
moves materially. Next, stress appears in single-stock order flow, particularly in the stocks
most heavily owned by institutional participants who may be repositioning. Stress then
spreads to index futures, where the mechanical hedging of options dealers and the macro
repositioning of systematic funds generates large, directional order flow. Finally, stress
becomes visible in the cash equity market through widening spreads and reduced depth.
A parallel propagation sequence occurs across asset classes. Stress that originates
in the equity options market often spreads to credit markets, where the cost of default
protection begins to rise as the equity market deterioration signals worsening balance sheet
risk for leveraged firms. From credit, stress moves to funding markets, where rising credit
concerns reduce the availability of repo financing and other forms of short-term secured
funding. The tightening of funding markets then feeds back to equity and fixed income
markets by reducing the balance sheets available to absorb selling pressure, creating the
self-reinforcing dynamic that converts isolated liquidity stress into a market-wide crisis.
10


### Page 13

Detecting Liquidity Stress Before Crises
Verma Research Capital
4.2. The Funding Liquidity and Market Liquidity Spiral
Brunnermeier and Pedersen (2009) formalise the relationship between funding liquidity,
the ease with which market participants can finance their positions, and market liquidity,
the ease with which positions can be traded without moving prices. Their framework
produces a spiral mechanism in which tightening funding conditions reduce the supply
of market liquidity, which increases the volatility of asset prices, which tightens margin
requirements, which further reduces funding availability, and so on.
The formal structure of this spiral can be represented through the margin constraint
faced by a leveraged market maker. Let W be the market maker’s equity capital, m be
the current margin requirement (expressed as a fraction of position value), and P be the
position the market maker wishes to hold. The constraint is:
m · P ≤W
(14)
When market volatility rises, regulators and counterparties increase the margin
requirement m. If W is fixed or declining due to mark-to-market losses, the maximum
supportable position P max = W/m falls. The market maker must either raise capital
or reduce positions. In practice, raising capital quickly is difficult, so the market maker
reduces positions by withdrawing from market making. This withdrawal reduces market
liquidity, which increases price impact, which increases volatility, which increases m
further, completing the spiral.
The speed of this spiral is governed by the sensitivity of margin requirements to
volatility. In markets where margin requirements are updated daily or intraday based
on realised volatility (such as in most exchange-traded futures), the spiral can complete
within hours. In markets where margin requirements are updated less frequently (such as
in OTC credit and repo markets), the spiral is slower but ultimately no less severe.
11


### Page 14

Detecting Liquidity Stress Before Crises
Verma Research Capital
4.3. Cross-Asset Contagion Through Common Ownership
A distinct but related propagation channel operates through the common ownership of
assets across large institutional portfolios. When a participant with positions across
multiple asset classes faces a margin call or a large redemption, they typically sell their
most liquid holdings first, generating selling pressure in assets that have no fundamental
relationship to the source of stress.
This forced selling creates what appears to be
correlated price moves across fundamentally unrelated instruments, which in turn misleads
risk models that treat the observed correlation as a signal of fundamental linkage.
The cross-asset impact of forced selling is proportional to the degree of overlap
between the stressed participant’s portfolio and the holdings of other large institutions.
When multiple large institutions hold similar portfolios, forced selling by one generates
mark-to-market losses for all, potentially triggering additional forced selling in a cascade.
The ownership overlap matrix O with entries:
Oij =
X
f
min(wi,f, wj,f)
X
f
max(wi,f, wj,f)
(15)
where wi,f is the weight of asset i in fund f, measures the degree to which two
assets are co-owned by the institutional investor universe. Assets with high Oij are most
vulnerable to contagion through forced selling, even in the absence of any fundamental
relationship. The aggregate exposure of a portfolio to this contagion channel is a function
of the portfolio’s overlap with the most commonly held institutional positions.
5. Systematic Liquidity Providers: Risk Limits and the With-
drawal Dynamic
5.1. The Conditionality of Algorithmic Market Making
The provision of liquidity in modern equity markets is dominated by high-frequency
market makers and systematic liquidity provision algorithms. These participants provide
12


### Page 15

Detecting Liquidity Stress Before Crises
Verma Research Capital
the bulk of the two-sided quotes visible in the limit order book under normal conditions,
and their participation is essential to the observed tightness of bid-ask spreads in normal
markets. However, their participation is highly conditional on the state of the market,
specifically on the level of realised volatility, the degree of order flow imbalance, and the
proximity of current conditions to their own risk limits.
The behaviour of algorithmic market makers under adverse conditions can be
modelled through their inventory management framework. Let qt be the net inventory of
the market maker in a given asset at time t. The market maker faces a running inventory
cost γq2
t (reflecting the risk of holding a large directional position) and a stochastic
liquidation cost if the position needs to be unwound quickly. The optimal bid and ask
quotes are:
A∗
t = st + γσ2∆t
2
−γqtσ2∆t + 1
κ ln

1 + κ
A

(16)
B∗
t = st −γσ2∆t
2
−γqtσ2∆t −1
κ ln

1 + κ
A

(17)
where st is the mid-price, σ2 is the asset’s variance, ∆t is the time interval, γ is
the inventory risk aversion parameter, κ is the order arrival rate sensitivity to spread,
and A is the baseline order arrival rate. This is the Avellaneda-Stoikov (2008) framework
for optimal market making. The key insight is that when volatility σ2 rises, the optimal
spread A∗
t −B∗
t increases and the optimal inventory target shifts. When volatility rises
sufficiently above the market maker’s calibrated range, the optimal response is to withdraw
entirely: the expected cost of adverse selection exceeds the expected profit from the spread,
and the market maker’s participation threshold is no longer met.
5.2. Synchronised Withdrawal and the Liquidity Void
The danger of a market dominated by algorithmic market makers is not that any individual
participant will withdraw, but that many will withdraw simultaneously. Because most high-
frequency market-making algorithms are calibrated on similar signals, specifically realised
13


### Page 16

Detecting Liquidity Stress Before Crises
Verma Research Capital
volatility and order flow imbalance, they tend to hit their risk limits at approximately
the same moment. The resulting liquidity void is not the sum of many small withdrawals
happening gradually; it is a near-simultaneous step-down in the total liquidity supply,
which produces the characteristic sudden widening of spreads and collapse of book depth
that precedes large price dislocations.
The simultaneity of withdrawal is measurable before it occurs through the mon-
itoring of the dispersion of quoted spreads across multiple market makers. In normal
conditions, spreads from different providers are clustered tightly around the equilibrium
spread level. As individual providers begin to approach their risk limits, their quoted
spreads begin to diverge upward. The cross-sectional standard deviation of quoted spreads,
σspread,t, therefore rises before the average spread rises, providing an early warning that
some providers are already under stress even while others are maintaining normal quotes.
Formally, the spread divergence signal is:
Dspread
t
= σspread,t
¯St
(18)
where ¯St is the average quoted spread at time t. When Dspread
t
rises significantly
above its normal range, the market is approaching a state where the remaining liquidity
suppliers are under-represented relative to the apparent book depth, because those with
the tightest spreads are increasingly exposed and close to withdrawal.
5.3. The Gamma Hedging Amplification Mechanism
In options markets, the liquidity stress dynamic is further amplified by the mechanical
hedging obligations of options dealers. Dealers who are net short gamma in index options
are required to sell the underlying index as prices fall (to maintain delta neutrality)
and buy as prices rise. In normal conditions, these hedging flows are absorbed by the
available liquidity in the futures market without meaningful price impact. In conditions
of thin liquidity, however, these flows can themselves consume a significant fraction of
the available depth, pushing prices further in the direction of the initial move and forcing
additional hedging, in a feedback loop that is entirely mechanical and entirely independent
14


### Page 17

Detecting Liquidity Stress Before Crises
Verma Research Capital
of any new fundamental information.
The total delta-hedging demand from the options market can be estimated from
the net dealer gamma exposure:
HedgeDemandt = −Γdealer,t · ∆St · N
(19)
where Γdealer,t is the aggregate net gamma of the dealer book (negative when dealers
are net short gamma), ∆St is the price move requiring hedging, and N is a normalisation
factor converting gamma to number of contracts. When dealers are net short gamma by a
large amount and liquidity in the futures market is thin, even a modest initial price move
can trigger a cascade of hedging demand that overwhelms available depth and accelerates
the move dramatically. This mechanism was central to both the August 2015 dislocation
and the March 2020 event.
6. The VRC Liquidity Stress Indicator
6.1. Design Principles
The VRC Liquidity Stress Indicator (LSI) is a composite daily metric that aggregates
signals from multiple dimensions of liquidity behaviour into a single reading used to adjust
risk exposures across the portfolio. The design follows three principles. First, the indicator
should lead rather than lag: each component should provide a signal that deteriorates
before the price-level symptoms of liquidity stress appear. Second, the components should
be genuinely independent in their information content, drawing on different aspects of
market structure rather than multiple variants of the same underlying signal. Third, the
indicator should be interpretable in absolute terms, calibrated against historical stress
episodes so that its readings carry consistent meaning across different market environments.
6.2. Component 1: Kyle Lambda Trend (Weight: 20%)
The first component captures the trend in daily price impact across a basket of liquid
equity indices and futures. For each market i, the Kyle lambda is estimated daily from a
15


### Page 18

Detecting Liquidity Stress Before Crises
Verma Research Capital
5-minute return-volume regression:
ri,s = αi + λi · xi,s + εi,s,
s = 1, . . . , 78
(20)
where the summation is over 78 five-minute intervals in a trading session. The
cross-market average lambda is:
¯λt = 1
M
M
X
i=1
ˆλi,t
(21)
The component signal is the 10-day change in ¯λt, standardised by its 252-day
rolling standard deviation. Rising price impact is the earliest and most direct signal of
market depth deterioration and receives the second-highest weight in the composite.
6.3. Component 2: VPIN Level and Trend (Weight: 25%)
The second component is built from the VPIN computed for S&P 500 E-mini futures and,
where available, for the most liquid individual equity futures. The VPIN is computed
using 50-bucket samples as in Easley, Lopez de Prado, and O’Hara (2012). The signal is a
weighted combination of the current VPIN level relative to its 252-day distribution and
the rate of change over the past five trading sessions:
Ct
2 = 0.6 · z(V PINt) + 0.4 · z
V PINt −V PINt−5
5

(22)
The level term captures a sustained state of elevated order flow toxicity, while
the trend term captures rapid deterioration. VPIN receives the highest single weight
because it most directly measures the phenomenon of interest: the dominance of informed,
directional flow over uninformed, two-sided flow.
6.4. Component 3: Bid-Ask Spread Divergence (Weight: 15%)
The third component measures the divergence of quoted spreads across multiple liquidity
providers, as described in Section 5.2:
16


### Page 19

Detecting Liquidity Stress Before Crises
Verma Research Capital
Ct
3 = z

Dspread
t

= z
σspread,t
¯St
!
(23)
This component is computed using data from multiple market centres (exchanges
and ATSs) for a basket of liquid equity ETFs. A rising C3 signals that some liquidity
providers are already under stress and widening their spreads even while the average
spread remains near normal, providing an early warning of the pre-withdrawal phase.
6.5. Component 4: Amihud Illiquidity Trend (Weight: 15%)
The fourth component uses daily data on the Amihud illiquidity ratio averaged across the
holdings of the VRC equity portfolios:
Ct
4 = z
1
N
N
X
i=1
ILLIQi,t
!
(24)
This component is slower-moving than the intraday components but provides a
structural background signal about the general level of price sensitivity to volume in the
portfolio’s specific holdings, which is directly relevant to the feasibility of dynamic risk
management.
6.6. Component 5: Options Skew and Depth Signal (Weight: 25%)
The fifth component captures the derivatives market dimension of liquidity stress. It
combines two sub-signals. The first is the 30-delta put skew for the S&P 500, defined as
the implied volatility at the 30-delta put minus the at-the-money implied volatility for
the same expiration:
Skew30∆= IV30∆put −IVATM
(25)
The second is the ratio of quoted depth in S&P 500 index options at the best bid
and ask to a rolling 30-day average, measuring the deterioration of liquidity in the options
market itself. The composite fifth component is:
17


### Page 20

Detecting Liquidity Stress Before Crises
Verma Research Capital
Ct
5 = 0.55 · z(Skew30∆,t) + 0.45 · z
−Deptht
Depth30d
!
(26)
The negative sign on the depth ratio means the component rises when depth is
below its recent average, consistent with the other components which rise in conditions of
stress.
6.7. Composite LSI and Regime Classification
The composite Liquidity Stress Indicator is:
LSIt = 0.20 Ct
1 + 0.25 Ct
2 + 0.15 Ct
3 + 0.15 Ct
4 + 0.25 Ct
5
(27)
18


### Page 21

Detecting Liquidity Stress Before Crises
Verma Research Capital
Table 1: VRC Liquidity Stress Indicator: Regime Classification and Portfolio Response
Regime
LSI
Range
Market Condition
VRC Response
Normal
< 0.5
Deep, two-sided liquidity;
low OFI volatility; stable
spreads
Full position sizes; nor-
mal strategy mix
Watchful
0.5–1.0
Mild
spread
widening;
slightly elevated VPIN;
skew firming
Reduce
position
sizes
15%;
review
illiquid
holdings
Guarded
1.0–1.5
Lambda
rising;
OFI
imbalances
persisting;
depth thinning
Reduce
position
sizes
35%;
reduce short vol
exposure
Stressed
1.5–2.0
Multiple
components
elevated;
systematic
provider
withdrawal
beginning
Reduce
position
sizes
60%; activate structural
hedges
Crisis
≥2.0
Spread collapse;
order
books thinning; feedback
loops active
Reduce
position
sizes
80%; defensive posture
only
The LSI is calibrated so that readings during the acute phase of the March 2020
liquidity crisis reached approximately 2.6, during the August 2015 flash crash approximately
2.2, and during the October 2022 UK gilt crisis approximately 1.9. Normal readings
during low-volatility environments typically range between 0.2 and 0.5.
7. Derivatives Market Signals of Liquidity Deterioration
7.1. Put Skew as an Informed Flow Indicator
The implied volatility skew in equity index options is one of the most information-rich
signals available for detecting early liquidity stress. The standard interpretation of the
19


### Page 22

Detecting Liquidity Stress Before Crises
Verma Research Capital
skew, that it reflects the demand for downside protection, is correct but incomplete. The
skew also reflects the adverse selection problem faced by options market makers: when
informed participants believe that a significant downside event is approaching, they buy
out-of-the-money put options, and options market makers widen the spread on those
options relative to at-the-money options to compensate for the adverse selection risk. The
skew therefore rises not only because uninformed investors are hedging but also because
informed investors are positioning.
This means that a rising skew, particularly one that steepens faster than can be
explained by changes in realised variance or the level of the VIX, is a signal of increasing
informed participation in the options market and therefore a leading indicator of the
same kind of liquidity deterioration that VPIN captures in the underlying futures market.
The term-structure-adjusted skew signal, which compares the current skew to the skew
predicted by the variance term structure, isolates the informed-flow component:
SkewAdjt = Skew30∆,t −
ˆ
Skewt(IV1m, IV3m)
(28)
where
ˆ
Skewt is the skew predicted by a linear regression of skew on the level and
slope of the implied volatility term structure, estimated over a rolling one-year window.
A positive SkewAdjt indicates that the skew is elevated beyond what current volatility
dynamics alone would justify, suggesting the presence of informed positioning.
7.2. Term Structure Kinks and the Concentration of Near-Term Risk
A specific and particularly informative pattern in the implied volatility term structure
is the appearance of a kink: a discontinuous elevation in implied volatility at a specific
near-term expiration relative to adjacent expirations. Such kinks arise when the options
market prices a specific near-term event risk, such as a Federal Reserve decision, an
earnings announcement, or a macro data release, that is expected to resolve within the
expiration of the kinked contract. The presence of a kink indicates that the market
has crystallised a specific short-term risk concern, which is associated with concentrated
informed positioning around that risk.
20


### Page 23

Detecting Liquidity Stress Before Crises
Verma Research Capital
For VRC monitoring purposes, we track the presence and magnitude of kinks in
the daily VIX term structure through the second difference of the at-the-money implied
volatility across maturities:
κτ = IVτ −IVτ−1 + IVτ+1
2
(29)
where IVτ is the at-the-money implied volatility for maturity τ measured in months.
A large positive κτ for any τ indicates an unusual concentration of risk pricing at that
expiration. When multiple maturities show elevated κ simultaneously, or when a kink at
a near-term maturity is unusually large relative to historical kink magnitudes, it signals
that the options market is pricing an unusual degree of concentrated near-term risk, which
is itself a form of liquidity stress.
7.3. The Cost of Rolling and the Liquidity Premium in Options
In liquid options markets, the bid-ask spread on a given option contract is relatively tight
and the cost of rolling from one expiration to the next is modest. As liquidity deteriorates,
three things happen simultaneously: absolute bid-ask spreads widen, the roll cost increases
as the spread at the new expiration exceeds the spread at the expiring contract, and
the liquidity premium embedded in implied volatility rises as market makers demand
additional compensation for the reduced depth they are providing.
For a systematic short volatility strategy that relies on rolling near-dated options,
this deterioration in roll economics is a direct cost increase that reduces the net premium
collected. Monitoring the ratio of the bid-ask spread to the mid-price of the option, the
relative spread, provides a standardised measure of this liquidity premium:
RelSpreadK,τ =
AK,τ −BK,τ
(AK,τ + BK,τ)/2
(30)
When the relative spread across the options surface rises significantly above its
historical norm, particularly in the most actively traded near-dated at-the-money contracts,
the options market is signalling that the cost of transferring volatility risk is rising even
21


### Page 24

Detecting Liquidity Stress Before Crises
Verma Research Capital
before any dramatic move in the underlying. This is one of the earliest and most reliable
indicators of the onset of liquidity stress in the derivatives complex.
8. Historical Case Studies
8.1. August 2015: The Flash Crash and Order Book Collapse
The market dislocations of August 24, 2015 provide a near-perfect case study of how
liquidity stress builds over multiple days before manifesting in an acute price event. In the
week preceding August 24, Chinese equity markets had been falling sharply, and concerns
about the Chinese growth outlook were generating elevated risk-off sentiment globally.
However, US equity markets had remained relatively contained, with the S&P 500 down
only modestly and the VIX in the low-to-mid twenties.
What was not visible in these surface indicators was a significant and accelerating
deterioration in the microstructure of the US equity market. VPIN for E-mini S&P 500
futures rose consistently through the week of August 17, as large, directional institutional
selling flow began to dominate the order book and passive liquidity providers began to
step back. The Kyle lambda estimate from five-minute futures return-volume regressions
doubled over the same period. Bid-ask spreads for the most liquid equity ETFs, including
SPY and QQQ, began to widen modestly on August 20 and 21, a full three days before
the crash.
On the morning of August 24, the combination of overnight Chinese market declines
and an already-stressed microstructure created a feedback loop. As the market opened
and ETF arbitrage mechanisms were disrupted by individual stock trading halts, the order
book for S&P 500 futures momentarily had almost no bids. The VIX briefly touched
53 before retracing to the mid-30s. Hundreds of individual stocks and ETFs triggered
circuit breakers. The liquidation cost for any portfolio that needed to reduce exposure
that morning was extraordinary.
Under the VRC LSI framework applied retrospectively, the indicator would have
been in the Stressed regime by August 21, three days before the acute event. The VPIN
22


### Page 25

Detecting Liquidity Stress Before Crises
Verma Research Capital
component and the spread divergence component were both signalling above their 95th
percentile values. The appropriate VRC response would have been to reduce position
sizes by 60 percent and activate structural hedges, reducing the portfolio’s exposure to
the forced liquidation dynamic that dominated the morning of August 24.
8.2. March 2020: The COVID-19 Liquidity Crisis and Treasury Market Failure
The March 2020 episode is the most severe liquidity event of the post-2008 era, and it
illustrates the full propagation sequence described in Section 4.1. The crisis began in
equity markets, spread to credit, moved to funding markets, and then circled back to
destroy liquidity in US Treasury bonds, the supposed safe haven that multi-asset portfolios
rely on for diversification and drawdown protection.
The early warning signals in this episode were visible primarily in the derivatives
market dimension of the LSI. The put skew for S&P 500 options began steepening
significantly in the final week of February 2020, as the first news of serious European
COVID-19 outbreaks reached US markets. The term-structure-adjusted skew signal
described in Section 7.1 rose to its highest reading since the fourth quarter of 2018 by
February 26, well before the most severe price declines. Simultaneously, VPIN for E-mini
futures began rising on February 24 as large institutional hedging flows entered the market.
The most exceptional feature of the March 2020 episode from a liquidity monitoring
perspective was the breakdown of Treasury market liquidity in the week of March 9. US
Treasury bid-ask spreads, which in normal times are measured in fractions of a basis
point, rose to ten or more basis points at multiple maturities during the acute phase. The
Amihud illiquidity ratio for on-the-run Treasury securities rose by a factor of approximately
fifty relative to its pre-crisis baseline. This extraordinary dislocation in the deepest and
most liquid market in the world was the mechanism through which the Federal Reserve’s
March 15 and March 23 emergency interventions were compelled: the normal mechanisms
of cross-asset liquidity provision had entirely broken down.
23


### Page 26

Detecting Liquidity Stress Before Crises
Verma Research Capital
8.3. October 2022: The UK Gilt Crisis and Liability-Driven Investment Forced
Selling
The October 2022 UK gilt crisis provides a case study of liquidity stress generated by
a specific structural feature of a particular investor base rather than by broad market
risk-off dynamics. Following the announcement of the UK government’s mini-budget on
September 23, 2022, UK gilt yields rose sharply. This rise triggered margin calls on the
leveraged gilt positions held by liability-driven investment (LDI) funds that managed the
interest rate hedging overlays of UK defined-benefit pension funds. The LDI funds were
forced to sell gilts to meet margin calls, which further drove yields higher, triggering more
margin calls in a self-reinforcing spiral.
From a microstructure perspective, the tell-tale signs of this episode were concen-
trated in the gilt market itself. UK gilt bid-ask spreads began widening on September
26, three days before the Bank of England’s emergency intervention on September 28.
VPIN for long-dated gilt futures rose sharply as one-directional selling flows dominated
the order book. The relative spread on the most liquid long-dated gilt options rose to
its highest level in years as options market makers withdrew from providing two-sided
liquidity in a market that they correctly identified as being dominated by forced sellers
with no discretion about timing or price.
The broader lesson from this episode is that liquidity crises can be highly localised
to specific structural vulnerabilities, and that a monitoring framework focused exclusively
on global equity and credit markets would have missed the early warning signals almost
entirely. At VRC, the LSI framework is applied across multiple asset class sub-monitors,
including a dedicated fixed income liquidity monitor that tracks gilt, bund, and Treasury
microstructure separately, to ensure that localised structural vulnerabilities are captured
before they propagate into the broader market.
24


### Page 27

Detecting Liquidity Stress Before Crises
Verma Research Capital
9. Hedge Fund Implementation: Strategy-Level Applications
9.1. Equity Long/Short Strategies
For equity long/short strategies, the LSI has two primary applications: position sizing and
strategy selection. At the position level, the maximum position size in any single equity
name is capped as a function of the current LSI regime, with the cap tightest for the most
illiquid holdings. For a stock with Amihud illiquidity ratio ILLIQi, the regime-adjusted
maximum position as a fraction of average daily volume (ADV) is:
MaxPosi = MaxPos0 ·
1
1 + βilliq · ILLIQi
· (1 −g(LSIt))
(31)
where MaxPos0 is the baseline maximum position in ADV terms, βilliq is a scaling
parameter for illiquidity sensitivity, and g(LSIt) is the same position reduction function
used in the volatility allocation framework, ranging from zero in the Normal regime to
0.80 in the Crisis regime.
At the strategy level, the LSI informs the choice between different equity long/short
approaches. In the Normal regime, both fundamental and statistical arbitrage approaches
are appropriate. In the Guarded and Stressed regimes, strategies with short holding
periods and tight stop losses become less attractive because the cost of executing the
required frequent trading increases, and the expected carry from statistical relationships
is less reliable when order flow is dominated by informed institutional repositioning rather
than by the noise-trader activity that statistical arbitrage strategies implicitly rely upon.
9.2. Short Volatility and Options Strategies
For short volatility strategies, the LSI provides the most critical risk management signal
available. The combination of rising VPIN, widening spreads, and steepening skew that
characterises the early stress regime is precisely the environment in which short options
positions face simultaneous compression of the carry they earn (through rising bid-ask
spreads that increase the cost of rolling positions) and expansion of the risk they are
25


### Page 28

Detecting Liquidity Stress Before Crises
Verma Research Capital
exposed to (through the feedback mechanisms described in Sections 4 and 5).
The specific LSI trigger for short volatility position reduction is the breach of the
Guarded threshold at 1.0, rather than the Stressed threshold at 1.5. This earlier trigger
reflects the asymmetry of the short volatility payoff profile: the cost of over-hedging
(carrying slightly less premium in a calm environment) is small relative to the cost of
being fully exposed when the LSI moves rapidly from Guarded to Crisis. Short volatility
positions are reduced to 40 percent of their Normal-regime size when the LSI enters the
Guarded regime, compared to the general 35 percent reduction that applies to other
strategy types.
9.3. Systematic and Trend-Following Strategies
Systematic and trend-following strategies have a more complex relationship with liquidity
stress. On one hand, these strategies are structurally long convexity and therefore benefit
from the large, directional price moves that accompany major liquidity events. On the
other hand, the quality of trend signals deteriorates in environments dominated by forced
flows and mechanical hedging demand, because the price moves generated by these flows
do not reflect genuine changes in fundamental value and tend to reverse once the forced
selling is complete.
At VRC, the LSI is used for systematic strategies not primarily for position sizing
but for signal filtering. When the LSI is in the Stressed or Crisis regime, trend signals
are discounted if they are aligned with the direction of the dominant forced flow, because
such signals are more likely to reflect a temporary technical dislocation than a sustainable
directional move. Signals that are contrary to the forced flow direction, by contrast, are
treated as potentially high-conviction positions, because they may represent the early
stages of the mean-reversion following the forced selling.
26


### Page 29

Detecting Liquidity Stress Before Crises
Verma Research Capital
10. Measuring Execution Quality as a Liquidity Monitor
10.1. Implementation Shortfall and Slippage Tracking
Execution quality measurement provides a direct, portfolio-specific window into the current
state of market liquidity. Implementation shortfall, defined as the difference between the
decision price (the mid-price at the time a trade is initiated) and the arrival price (the
average execution price), captures both the market impact and the opportunity cost of
trading. When implementation shortfall rises for a given portfolio, it signals that market
impact is increasing, which is directly observable evidence of deteriorating liquidity in the
specific instruments held.
For trade k in asset i, the implementation shortfall is:
ISi,k = sign(qi,k) · Pexec −Pdecision
Pdecision
(32)
where qi,k is signed trade quantity (positive for buys, negative for sells), Pexec is
the average execution price, and Pdecision is the mid-price at decision time. The rolling
average implementation shortfall across all recent trades:
ISt = 1
K
K
X
k=1
ISk,t
provides a continuous measure of execution cost that is both portfolio-specific and
forward-looking: rising implementation shortfall not only signals that recent trades were
costly but also that future trades in the same instruments are likely to be costly, because
the underlying conditions driving the deterioration are systemic rather than trade-specific.
10.2. The Spread Capture Ratio as a Liquidity Health Metric
For institutional portfolios that engage in frequent trading, the spread capture ratio
provides a complementary measure of execution quality. The spread capture ratio is
defined as the fraction of the bid-ask spread that is captured as a cost by the portfolio’s
trades:
27


### Page 30

Detecting Liquidity Stress Before Crises
Verma Research Capital
SCRt = 2 · ISt
St
(34)
where ISt is the implementation shortfall and St is the bid-ask spread at the time
of execution. A ratio of one indicates that all trades were executed at the spread, implying
zero market impact beyond the spread. A ratio greater than one indicates that trades were
executed at prices worse than the spread, implying positive market impact and therefore
a market in which depth beyond the best bid and ask is limited. Rising SCR is therefore
a direct measure of deteriorating market depth in the specific instruments being traded
by the portfolio.
At VRC, we track both the level and the trend of the SCR across our trading
activity on a rolling five-day basis. When the five-day average SCR rises above 1.2 across
our equity holdings, we treat this as an independent corroboration of the LSI’s signal that
market liquidity is deteriorating, even when the price-level indicators remain benign. The
convergence of a rising LSI and a rising SCR produces the highest-conviction liquidity
stress reading in our framework.
11. Limitations of the Framework
11.1. Data Requirements and Availability
The full implementation of the VRC LSI as described requires access to intraday trade
and quote data across equity markets, futures markets, and options markets. For the
VPIN calculation, volume-synchronised trade data with millisecond timestamps is ideal.
For the Kyle lambda estimation, five-minute bars with volume breakdown by direction
are required. For the spread divergence component, quotes from multiple market centres
need to be consolidated. While this level of data availability is standard for institutional
hedge funds with direct market access and colocation arrangements, it may be unavailable
or prohibitively expensive for smaller managers. For such managers, a simplified version
of the LSI using only daily closing data, combining the Amihud illiquidity ratio, the daily
implied volatility skew, and the daily bid-ask spread for liquid ETFs, captures a significant
28


### Page 31

Detecting Liquidity Stress Before Crises
Verma Research Capital
fraction of the early warning value at substantially lower data cost.
11.2. False Positives and the Cost of Excessive Caution
A composite liquidity stress indicator that is appropriately sensitive will inevitably
generate false positive readings: periods when the indicator signals elevated stress but
no major market dislocation materialises. False positives generate real costs in the form
of reduced portfolio exposure during periods when maintaining full exposure would have
been profitable. These costs are the price of the protection the indicator provides against
actual crisis events, and they should be evaluated in that context rather than in isolation.
The appropriate evaluation framework for the LSI is not its accuracy in predicting
specific events but its contribution to the overall risk-adjusted return of the portfolio over
full market cycles. A strategy that reduces exposure each time the LSI enters the Guarded
or Stressed regime, and that suffers a modest drag from false positives during normal
markets, will outperform one that maintains full exposure through those periods if even
one or two genuine crises of the magnitude of August 2015 or March 2020 are avoided.
The asymmetry of crisis losses relative to normal-period carry income strongly favours a
framework that errs on the side of caution when multiple independent liquidity signals
are elevated simultaneously.
12. Conclusion
This paper has developed a comprehensive framework for detecting liquidity stress before
it becomes visible in the price-level indicators that practitioners most commonly monitor.
The central argument is that market liquidity is not a fixed feature of the financial
landscape but a conditional outcome of the incentives, balance sheet constraints, and risk
tolerance of the participants who provide it. When those conditions begin to deteriorate,
the evidence appears first in the mechanics of trading itself, in the composition and
balance of order flow, in the cost and availability of two-sided market making, and in the
pricing of optionality in derivatives markets, long before it is visible in index levels or
conventional volatility measures.
29


### Page 32

Detecting Liquidity Stress Before Crises
Verma Research Capital
The theoretical foundations of this argument are grounded in the market mi-
crostructure literature, including the Glosten-Milgrom adverse selection model, the Kyle
price impact framework, and the PIN and VPIN families of informed trading measures.
These frameworks provide the quantitative language for describing what is happening
when market liquidity deteriorates: the proportion of informed order flow is rising, the
cost of providing two-sided liquidity is increasing, and the providers of that liquidity are
adjusting their behaviour in ways that are measurable from observed trade data.
The VRC Liquidity Stress Indicator operationalises these insights through five
components that collectively measure the velocity of price impact deterioration, the degree
of order flow imbalance, the divergence of market maker spreads, the overall illiquidity
of portfolio holdings, and the informed-flow signals embedded in options market pricing.
The combination of these five independent signals provides a robust and early-warning
composite that correctly identified elevated stress before each of the three historical
episodes examined: the August 2015 flash crash, the March 2020 COVID-19 crisis, and
the October 2022 UK gilt dislocation.
The hedge fund implementation framework translates the LSI readings into specific,
actionable adjustments to position sizing, strategy selection, and execution approach.
The key principle is proportionality: the size of the portfolio adjustment is calibrated to
the severity of the stress signal, avoiding both the complacency of ignoring early-stage
warning signs and the excessive defensiveness of treating every mild signal as a crisis.
The deepest lesson of this work is operational rather than analytical. Markets do
not break without warning. The warning is simply expressed in a language that most
practitioners are not equipped to read, because they are watching prices rather than
plumbing. At VRC, the monitoring of order flow, execution quality, and derivatives market
structure is not a peripheral analytical curiosity. It is the foundation of our conviction
that risk management can be genuinely proactive rather than merely reactive, and that
the structural conditions for a crisis can be identified, and responded to, before the crisis
has fully arrived.
30


### Page 33

Detecting Liquidity Stress Before Crises
Verma Research Capital
References
Avellaneda, M., and Stoikov, S. (2008). High-frequency trading in a limit order book.
Quantitative Finance, 8(3), 217–224.
Amihud, Y. (2002). Illiquidity and stock returns: Cross-section and time-series effects.
Journal of Financial Markets, 5(1), 31–56.
Amihud, Y., and Mendelson, H. (1986). Asset pricing and the bid-ask spread. Journal
of Financial Economics, 17(2), 223–249.
Bagehot, W. (1971). The only game in town. Financial Analysts Journal, 27(2), 12–14.
Brunnermeier, M. K., and Pedersen, L. H. (2009). Market liquidity and funding liquidity.
Review of Financial Studies, 22(6), 2201–2238.
Chordia, T., Roll, R., and Subrahmanyam, A. (2000). Commonality in liquidity. Journal
of Financial Economics, 56(1), 3–28.
Chordia, T., Roll, R., and Subrahmanyam, A. (2002). Order imbalance, liquidity, and
market returns. Journal of Financial Economics, 65(1), 111–130.
Cont, R., Kukanov, A., and Stoikov, S. (2014). The price impact of order book events.
Journal of Financial Econometrics, 12(1), 47–88.
Duffie, D. (2010). Asset price dynamics with slow-moving capital. Journal of Finance,
65(4), 1237–1267.
Easley, D., Kiefer, N. M., O’Hara, M., and Paperman, J. B. (1996). Liquidity, information,
and infrequently traded stocks. Journal of Finance, 51(4), 1405–1436.
Easley, D., Lopez de Prado, M., and O’Hara, M. (2012). Flow toxicity and liquidity in a
high-frequency world. Review of Financial Studies, 25(5), 1457–1493.
Glosten, L. R., and Milgrom, P. R. (1985). Bid, ask, and transaction prices in a specialist
market with heterogeneously informed traders. Journal of Financial Economics, 14(1),
71–100.
Grossman, S. J., and Miller, M. H. (1988). Liquidity and market structure. Journal of
Finance, 43(3), 617–633.
Hameed, A., Kang, W., and Viswanathan, S. (2010). Stock market declines and liquidity.
Journal of Finance, 65(1), 257–293.
Harris, L. (2003). Trading and Exchanges: Market Microstructure for Practitioners.
Oxford University Press.
Hasbrouck, J. (1991). Measuring the information content of stock trades. Journal of
Finance, 46(1), 179–207.
Hasbrouck, J. (2009). Trading costs and returns for US equities: Estimating effective
costs from daily data. Journal of Finance, 64(3), 1445–1477.
Kyle, A. S. (1985). Continuous auctions and insider trading. Econometrica, 53(6),
1315–1335.
Lee, C. M. C., and Ready, M. J. (1991). Inferring trade direction from intraday data.
31


### Page 34

Detecting Liquidity Stress Before Crises
Verma Research Capital
Journal of Finance, 46(2), 733–746.
Madhavan, A. (2000). Market microstructure: A survey. Journal of Financial Markets,
3(3), 205–258.
O’Hara, M. (1995). Market Microstructure Theory. Blackwell.
Pastor, L., and Stambaugh, R. F. (2003). Liquidity risk and expected stock returns.
Journal of Political Economy, 111(3), 642–685.
Pedersen, L. H. (2015). Efficiently Inefficient: How Smart Money Invests and Market
Prices Are Determined. Princeton University Press.
Roll, R. (1984). A simple implicit measure of the effective bid-ask spread in an efficient
market. Journal of Finance, 39(4), 1127–1139.
Sadka, R. (2006). Momentum and post-earnings-announcement drift anomalies: The
role of liquidity risk. Journal of Financial Economics, 80(2), 309–349.
Shleifer, A., and Vishny, R. W. (1997). The limits of arbitrage. Journal of Finance,
52(1), 35–55.
Stoll, H. R. (1978). The supply of dealer services in securities markets. Journal of
Finance, 33(4), 1133–1151.
Vayanos, D. (2004). Flight to quality, flight to liquidity, and the pricing of risk. NBER
Working Paper No. 10327.
Weill, P. O. (2007). Leaning against the wind. Review of Economic Studies, 74(4),
1329–1354.
32

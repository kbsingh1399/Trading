# Order Flow Toxicity and Informed Trading Around Known Market

- **Source File**: `ssrn-2807531.pdf`
- **Total Pages**: 63
- **SSRN ID**: `ssrn-2807531`

---


### Page 1

Electronic copy available at: http://ssrn.com/abstract=2807531
Order Flow Toxicity and Informed Trading Around Known Market
Manipulation Events: Evidence from Interest Rate Futures
Pongsutti Phuensanea, Julian Williamsa,∗
aDurham University, Business School.
Abstract
The objective of this paper is an ex-post review of the eﬀectiveness of PIN and VPIN in determin-
ing changes in the information structure and order ﬂow of a futures market around documented
episodes of recorded manipulation of the reference rate, from the various publicly available regula-
tory reports. In keeping with previous studies on interest rate derivatives, this analysis ﬁnds that
the average PIN is far higher for futures than for the equity market at or above 60%. Furthermore,
I ﬁnd a very strong connection between PIN, VPIN and time to maturity of the contract that is
not fully explained by the time variation in activity in the market. However, an event study using
both a new bootstrap approach and asymptotic standard error on the VPIN and PIN respectively
around documented LIBOR manipulation cases has mixed results. For certain events I see a sub-
stantial change in the average detected levels of PIN and VPIN, however a cross sectional analysis
of all reported cases up to mid-2015, indicates no signiﬁcant change in the PIN and VPIN for the
contracts in this Eurodollar sample.
Keywords:
Microstructure, Informed Trading, PIN, VPIN, LIBOR, Eurodollar, Market
Manipulation
1. Introduction
There are currently two key debates ongoing in the ﬁnancial community related to issues
around market manipulation.
First, in the policy and practitioner community, there is
evidence of manipulation of key benchmarks by ﬁnancial institutions, and there is some
disagreement as to whether this occurred primarily to improve their trading opportunities
or to reduce the perception of balance sheet weakness. Second, is an academic debate as
to whether the current high proﬁle measures of the probability-of-informed trading (PIN)
∗Corresponding Author.
Email addresses: pongsutti.phuensane@durham.ac.uk (Pongsutti Phuensane),
julian.williams@durham.ac.uk (Julian Williams)
Draft
July 10, 2016


### Page 2

Electronic copy available at: http://ssrn.com/abstract=2807531
and ‘market-toxicity’ (measured by a volume adjusted PIN denoted VPIN) actually provide
substantive measurement of the phenomena in question.
This study takes a comprehensive dataset from Chicago Mercantile Exchange (CME)
tape data, which covers every inside quote and trade from 1996 to 2015 for the 40 LIBOR
referenced quarterly dated Eurodollar futures contracts. First, I apply diﬀerent ﬂavours
of the PIN and VPIN metrics over a variety of estimation windows. A variety of tests is
constructed to see if the pattern of the PIN and VPIN exhibit structural changes around
documented cases of manipulation of the LIBOR reference rate. Finally, I compare this to
systematic ﬂuctuations in these measures relative to the futures term structure.
Unsurprisingly, given the scale of the task, this study ﬁnds very mixed results. Both
PIN and VPIN vary systematically and in a statistically signiﬁcant pattern in respect to
the term structure of the futures contracts. PIN varies in a v-shaped pattern, with long
(2000 to 3500 days) and short maturity (0 to 500 days) contracts having signiﬁcantly higher
PIN and VPIN measurements than intermediate contracts (which are actually the most
heavily traded). VPIN measurements of informed trading are substantially lower, over the
entire gamut of calculation measures. However, when I move to documented cases of market
manipulation in the reference rate, the results are ambiguous. There are deﬁnitive cases
when the PIN (and to an extent certain ﬂavours of the VPIN) shift systematically around
a relevant documented LIBOR manipulation event. However, when I build cross sectional
averages across events, I ﬁnd no signiﬁcant evidence of systematic shifts in either the PIN
or VPIN metric. It should be noted that whilst I have included every documented case of
manipulation directly linked to the relevant reference rates, my list is necessarily incomplete
as the regulatory actions have tended to focus on sample charges to the ﬁrms involved,
rather than documenting every occurrence and its motivation.
The contribution of this chapter is threefold. First, this is the only paper to provide a
comprehensive analysis of informed trading in Eurodollar futures from 1996 to 2015. Second,
2


### Page 3

to implement my analysis I have introduced several innovations in the estimation process,
including an exact asymptotic representation of the measurement error of the PIN and a
new bootstrap-in-bootstrap method for estimation of the VPIN. Finally, my methodologi-
cal approach to decomposing informed trading by both event and the term-structure is a
new contribution to this literature and my algorithms are available for other researchers to
implement such studies in diﬀerent market settings.
The remainder of this paper is organized as follows. First, §.2 outlines the debate on
informed trading, in the academic literature in regard to the eﬃcacy of the PIN and more
recent VPIN algorithms.
To this end, §.3 I look more deeply at the adaptation of the
Glosten and Milgrom (1985) model of informed trading and demonstrate how a version of
the classic version of the PIN could be used to empirically ﬁt this model, in the spirit of
Glosten and Milgrom (1985) and Easley et al. (1996). In this section, I document the various
empirical strategies to estimate the PIN and VPIN including several new features speciﬁc
to this study relating to the distribution of these critical statistics. §.4 provides a detailed of
Eurodollar futures and the descriptive of the term-structure of PIN and PIN’s parameters.
Subsequently §.5 presents the analysis of my dataset. For each contract maturity, the PIN
and VPIN is estimated and I construct experiments by aggregation across the terms struc-
ture, in addition to using the LIBOR manipulation events discussed previously. Finally, in
§.6 presents the summaries of the key ﬁndings and some brief concluding comments and
directions for future research.
2. The VPIN Debate and Further Background
The PIN model was ﬁrst introduced in Easley and O’Hara (1992) and Easley et al.
(1996) and estimated over relatively high frequency data for US equities. Subsequent work
focused on the PIN as an asset pricing factor or related the analysis directly to corporate
3


### Page 4

governance. The theoretical model underlying the PIN evolved from the information based
trading literature that started with Grossman and Stiglitz (1980) and Hellwig (1980) then
continued with Admati (1985), Hasbrouck (1991) and Kyle (1985).
However, the most
direct theoretical antecedent to the PIN model is Glosten and Milgrom (1985) and this is
the starting point for interpreting the impact of LIBOR manipulation on the Eurodollar
futures market. In general the theoretical models of informed trading have traveled down
the standard roots, Glosten and Milgrom (1985) and Kyle (1985) have used Bayesian games
to analyse simple information ﬂows in single assets, whereas Hellwig (1980), Admati (1985)
and Admati and Pﬂeiderer (1988) have utilized a rational expectations framework for single
and multiple assets.
However, regardless of the solution device applied, either rational expectations or a
Bayes-Nash equilibrium, the general set-up is very similar. First, certain traders are provided
with a forward looking information endowment (usually a noisy forecast of direction) and
then there is a trading game against another group of traders who either lack this information
or whose order ﬂow is constrained. For instance, in the case of Eurodollar futures, we know
that ﬂoating legs of IRSs are oﬀset at or around international money market (IMM) dates,
hence one particular institution may not have any choice in the timing and net quantity
of futures demanded whether long or short. Hence a trader with these constraints is a net
supplier of random order-ﬂow to the market regardless of how the term structure is updated
by the new ﬁxings.
One of the unique selling points of the PIN model is the ease of implementation. The
Glosten and Milgrom (1985) model is easily to re-cast in terms of net order ﬂow and hence one
merely needs to sign each trade as a buy or a sell to determine the net order-ﬂow imbalance.
The PIN is then computed via maximum-likelihood estimation. However, signing trades as
a buy or a sell can be a diﬃcult process. The standard Lee and Ready (1991) algorithm
matches trades based on the distance between the transacted price and the nearest quotes.
4


### Page 5

Several prior studies have identiﬁed diﬃculties in estimating the PIN attributing most of the
problems to trade-classiﬁcation, see Ke (2014);Yan and Zhang (2012);Boehmer et al. (2007).
It is evident that when switching to very high frequency data (such as that generated by
futures trading) classifying trades becomes ever more problematic.
As a solution to the PIN classiﬁcation problem, Easley et al. (2012) proposed a volume
based approach known as VPIN, and explicitly introduced the notion of order-ﬂow-toxicity.
Order-ﬂow-toxicity is deﬁned as a systematic imbalance in the buy and sell side volume of
the order-book that leads to substantial adjustments in spread. This is in opposition to
the normal state of aﬀairs where the liquidity would remain relatively constant. However,
the proposed application to the May 2010 ‘ﬂash crash’ has proved somewhat controversial.
In many respects the ease of implementing the VPIN and the unambiguous nature of its
measurement of market data, forms part of the issue. Andersen and Bondarenko (2013) re-
computed the VPIN metric for S&P 500 E-mini futures and refuted the applicability of the
method to forecast extreme liquidity events. Andersen and Bondarenko (2013) concluded
that the VPIN was highly sensitive to the assumptions placed on discretizing the volume
of orders, reducing its eﬃcacy as a regulatory instrument for predicting order-ﬂow-toxicity
exceed events.
In a series of follow up papers Andersen and Bondarenko (2014c), Easley et al. (2014)
and again Andersen and Bondarenko (2014b) debated the relative merits of the VPIN ap-
proach. In another follow-up, Andersen and Bondarenko (2014a) proposed an alternative
approach to speciﬁcally capture order-ﬂow-toxicity. My experience with estimating VPIN
falls somewhere between Andersen and Bondarenko (2014c) and Easley et al. (2014). VPIN
is indeed sensitive to the choice on how to discretize volume. However, I do ﬁnd the change
in VPIN, and I denote this ∆VPIN which is consistent across a variety of choices. I do not
ﬁnd VPIN and the original PIN to be correlated under my trade-classiﬁcation approach.
Furthermore, I do not ﬁnd that the VPIN lies within a 95% conﬁdence bound computed
5


### Page 6

from the maximum likelihood estimates for the underlying parameters. This indicates that
for the purposes of identiﬁcation of informed trading in Eurodollar futures markets, (which
uses the same platform as the S&P 500 E-mini), the PIN and VPIN are, unfortunately,
incongruent across a wide variety of speciﬁcations (including a bootstrapped version).
3. The model
3.1. The Market Algorithm
This section explains how the LIBOR manipulation aﬀects the Eurodollar trading by de-
riving the fundamentals of sequential trading with superior information proposed by Glosten
and Milgrom (1985) . This model focuses on stylized leadership market in which a Eurodol-
lar price will reach at time T with value ST = {S, S}, where S ≤S. Uninformed traders
(ε) know the Eurodollar price will be S ≤St ≤S,however, they do not know either St = S
or St = S will occur, so these traders are equally likely to buy or sell. Unlikely uninformed
traders, informed traders (µ) are said to be informed of knowing the terminal value of the
asset ST. This sequential trade can be explained in terms of probability(P) which is the one
that makes most sense. With theoretical explanations incorporated with ED trading, on
each trading period traders arrive on the market sequentially in which knowing the value of
ED futures equals ST, suppose that P(ST = S) = δ and P(ST = S = 1 −δ), which trade
occurs at time t ∈[0, T). The probability pay oﬀfor each possible scenario of ST is, if the
ED expected price is equal ST = S ≤St informed traders will wait on the sell side with
probability δµ, as uninformed Traders is risk neutral, so they will locate in both buy and
sell side with rate 1
2(1−µ)δ. If the expected price equals St ≤S = ST informed Traders will
arrive at buy side with probability (1 −δ)µ and uninformed traders at rate 1
2(1 −µ)(1 −δ).
Whilst forward knowledge of the ﬁx has many applications it is worth postulating a spe-
ciﬁc example of a trading strategy in ED futures around LIBOR announcements. Consider
the period 2005 to 2007, the spread of submissions for the LIBOR ﬁx are very tight. For a set
6


### Page 7

of banks typically sitting in the middle eight submitters, a collaborative submission (as indi-
cated by the cross bank emails noted previously) could allow for reasonable fore-knowledge
of the ﬁx in the second decimal, for instance an unexpected increase in the submission by one
basis point or $25 for each contract. The per day quote volume (in terms of numbers of con-
tracts quoted at the inside best bid best ask) for the Eurodollar market exceeds 715 volume
for a single day. Therefore a $25 dollar a contract advantage has potential for substantial
proﬁts, if a suitable shock can be engineered against the current market expectations. It is
worth noting that as a forward rate contract, the shock can be engineered from any LIBOR
ﬁxing, however, it is apparent that the size of the impact needs to be reasonably close to
maturity contracts.
As the update on the reference rate is at 11:00.00 GMT time we can think of this as
being the realization of a signal that will update the information set of all traders. Prior to
the update the request to the submitter pool for a ‘high’ or a ‘low’ ﬁxing equates to ‘δ′ and
‘1 −δ′ respectively.
Shortly after 11:00:00 GMT , around 11:30:00 GMT or 06:30:00 central time (recalling
that the ED future is traded around the clock) the LIBOR rate is announced, then informa-
tion set for the futures are updated for all participants as a realization. However, in a smaller
scale study on ED futures Kim et al. (2014) reports that the highest fraction of informed
trading is located in the ED market around 7.00 to 10.00 CT which is after the announce-
ment rather than in the lead up. I will show later that this is consistent with my macro-view
argument that maturity and activity play a much more important role in the degree of in-
formed trading and order toxicity within the market. After receiving the signal, informed
derivatives traders wait to ‘Buy’ or ‘Sell’ regarding which type of information they have
received from the submitter. If they arrive on buying side then P(Buy) = 1 + µ(1 −2δ)/2,
while on the sell side P(Sell) = (1−µ)(1−2δ)/2, hence P(Buy)+P(Sell) = 1. Subsequently,
in each trading period the nature of the event occurs with, P(Buy) = P(sell) = 0.5 then
7


### Page 8

δt = 0.5, P(ST = S) and P(ST = S) = 1 −δ at t = 0.
In the period after the LIBOR is published, informed traders arrive with a degree of
positive adverse selection that can be observed by increased spread. At this point, a market
maker recognizes a price level at which he intends to enter, whether long position (Bid,
B) or short position (Ask, A).Although the market maker doesn’t know that other market
participants at period t are informed or not, he can update his belief about the value of ST as
trades are revealed, so P(ST = S|Buy) = P(ST = S, Buy)/P(Buy) = δt(1−µ)/1+µ(1−2δ).
If (ST) = S ≤St informed traders lower their expectation, since E[ST|Buy] = S(1 −
µ)δt + S(1 + µ)(1 −δt)/1 −µ(1 −2δt) and increase expectation on ST, since E[ST|Sell] =
S(1+µ)δt +S(1−µ)(1−δt)/1+µ(1−2δt). Therefore the spread is A−B = 4(1−δt)δtµ(S −
S)/1 −(1 −2δt)2µ2.
Conversely, in the case of (ST) = S ≤St informed trading (µ) occurs when A =
E[ST|Buy] with a proﬁt is gained by direct wealth transfer from the loss incurred by unin-
formed trades (ε). I can therefore write (A−E[ST|µ, Sell])P(µ|Sell) = (A−E[ST|ε, Sell])P(ε|Sell),
since by construction P(µ|Sell) + P(ε|Sell) = 1. This argument can be made for B when
(ST) = St ≤St. Recall that the original interpretation of the Glosten and Milgrom (1985)
model operates in a zero sum outcome. Deﬁnitively, a futures market can be seen in this
sense as the settlement at marking to market, from the price at 13:59:00 and 14:00:00 CT
(19.59.00 to 20:00.00 GMT), provides a deﬁnitive result on the days activities. Therefore,
one explanation for the post ﬁxing informed trading is that the update of the LIBOR curve
itself generates new diﬀerentiated sets of information on E(ST) between informed traders
and uninformed traders prior to the ﬁnal settlement at 14:00:00.
3.2. The Asymptotic Standard Error of The PIN
The previous discussion indicates why a binomial high versus low ﬁx model is very appro-
priate for this setting, indeed one could argue the relatively clean mechanism for discerning
the days winners and losers makes this far more appropriate than the many other applica-
8


### Page 9

tions of this approach. The original PIN is a measure by Easley et al. (1996) of asymmetric
information ﬁtted via maximum likelihood estimation directly from measurements of the
order ﬂow. The tree diagram in Figure 1 presents the dynamics of the game and frames the
original PIN type model in terms of the information structure of the ED futures market.
I restrict my interest and the estimation of the model to each contract individually.
Whilst attempting to build a simultaneous equation model across all 40 contracts seems
attractive there are substantial drawbacks in terms of numerical tractability. This analysis
index discrete trading time by i = 1, 2, . . . , I and time is considered to be continuous within
discrete trading block and is denoted by t ∈[0, T). Market participants buy or sell the asset
at bid and ask prices posted on the limit order-book during the trading period. Information
events are independently distributed at the beginning of each trading block, and occur with
probability α.
However, informed traders will only trade when they perceive that their
LIBOR ﬁxers will be able to generate an information event; they will buy an asset if they
receive a signal of good news with probability 1 −δ and sell if they receive a signal of bad
news with probability δ. As εb and εs are the selling and buying rate of uninformed traders,
who are supposed to have the same intensity (0.5), therefore the probability of uninformed
traders is εs = εb = ε. In this way, the set of parameters is reduced to α, δ, µ and ε.
Within each trading block, order-ﬂow arrives from both uninformed traders and informed
traders subject to the receipt of their signal. Both uninformed buyers and sellers arrive in
the market at rate ε. Competitive informed traders who are risk neutral will arrive when
information events have occurred. If they receive a deﬁnitive signal of an up tick, they will
arrive to buy orders; conversely, they will submit sell orders if they receive a bad signal or
bad news. The arrival rate for this process is µ. Following convention, the arrival processes
are assumed to be independent. On good event days, the arrival rate for buy orders is ε + µ
and for sell orders is ε. On the other hand, if there is any bad news or bad signal on any
trading day, the arrival rate of sell orders is ε + µ and buy orders arrive at a rate of µ.
9


### Page 10

Information Event (LIBOR
ﬁxing rate was requested
prior to 11:00:00 GMT)
Information does Not Occur:
1 −α (Fair rate occurred
(No manipulation event))
Sell Arrival Rate: ε
Buy Arrival Rate: ε
Information does Occur: α
(Artiﬁcial rate occurred as
request)– Signal transmitted
Signal Low: δ (High LIBOR
ﬁxing submitted as request,
ED price = 100 - LIBOR)
Sell Arrival Rate: ε + µ
Buy Arrival Rate: ε
Signal High: 1 −δ (Low
LIBOR ﬁxing submit-
ted as request, ED
price = 100 - LIBOR)
Sell Arrival Rate: ε
Buy Arrival Rate: ε + µ
Figure 1: The Eurodollar price and a tree diagram of the sequential trading progress
Note: that after 11.00 GMT the LIBOR FIX is published, if the rate that occurred has been requested by derivatives traders, then the
published data is similar to a signal with rate α. When the ﬁx is high, the price of the contract will decrease (ED price = 100 - LIBOR)
and when the ﬁx is low the price will be higher, if the bank can guarantee that its ﬁx will impact on the LIBOR average determination.
10


### Page 11

Finally, if there is no news or no signal on that day, only uninformed traders arrive for both
buy and sell orders at arrival rate ε.
In each block, the news arrival contains one of three types of information. On the CME
Globex market makers provide liquidity via the ‘mass-quote’ system whereby a single market
marker can control a very large number of standing quotes within the various levels of the
limit order book (eﬀectively mimicking a larger group of individual traders).
Following
Easley et al. (1996) it can be presumed that the market maker knows that there is some
probability attached to each branch and has some knowledge of the order arrival process for
each branch. However, the market maker does not know which of the three branches has
been selected. Since he cannot directly observe which type of branch has been selected he
uses Bayesian updating from the observed order-ﬂow to adjust his beliefs about the nature
of the information events during a single trading block. Let P(t) = (Pn(t), Pb(t), Pg(t)) be
a liquidity provider’s belief about the occurrence of information event “no news” (n), “bad
news” (b), and “good news” (g) at time t. Then, his prior beliefs at time 0 is P(t0) =
(1 −α, αδ, α(1 −δ)) .
To determine quotes at time t, the market maker updates his prior belief on the condition
of an arrival order of the relevant type. For instance, the bid at time t, B(t), is the expected
value of the asset conditional both on the history of the process prior to the arrival of order
at time t and on the fact that someone wants to sell the asset. Let (st) denote the event
that a sell order arrives at time t. Let Pn(t|st) be the market maker’s updated belief vector
conditional on the history prior to time t and on the event that a sell order arrives at time t.
Following Bayes’ rule, the market maker’s posterior probability on no news at time t, if
an order to sell arrives at t, is Pn(t|st) = Pn(t) · ε/ε + Pb(t)µ, the posterior probability on
bad news is Pb(t|st) = Pb(t) · (ε + µ)/ε + Pb(t)µ and the posterior probability on good news
is Pg(t|st) = Pg(t) · ε/ε + Pb(t)µ. Comparable to the case of buy orders (Bt) the posterior
probability on good news at time t is Pg(t|bt) = Pg(t) · (ε + µ)/ε + Pg(t)µ the posterior
11


### Page 12

probability on bad news is Pb(t|bt) = Pb(t) · ε/ε + Pg(t)µ and the posterior probability on
no news is Pn(t|bt) = Pn(t) · ε/ε + Pg(t)µ. At the end of the trading on any day, the full
information value of the asset is realized. If it is good news on trading day (i) the informed
trader knows that the value of the asset at the end of the day is worth ¯Si, similarly it is
Si if it is bad news on day i and the asset on day i is worth S∗
i = δSi + (1 + δ) ¯Si, (so,
¯Si > S∗
i > Si) if there is no news at all.
To complete the bid or ask at time t, the liquidity provider updates his position on the
condition of arrival order according to the information type. At time t the expected value of
the asset, conditional on the history of trade prior to time t, is E[Si|t] = Pn(t)S∗+Pb(t)Si +
Pg(t) ¯Si where S∗
i = δSi + (1 + δ) ¯Si is the prior expected value of the asset. How might this
work in practice on Globex? Well the market maker uses the mass quote system to place
a large number of resting quotes at various levels within the order-book. If one side of the
order-book receives a disproportionate number of trades then resting quotes on the opposite
side (at level one of the limit order book) update and are canceled, and new quotes are
instigated to restore balance and maintain the magnitude of the spread. New quotes deeper
in the order book on the side with the draw down are instigated automatically. Whilst, in
principle, this should ensure that price shifts are driven by supply and demand, the ‘Flash
Crash’ of May 2010, originating on the Globex platform, indicates that this mechanism
is not always perfectly functional. From this adjustment process the bid is the expected
value of the asset conditional on someone wanting to sell the asset to a liquidity provider.
Thus, the bid–ask spread at time t is denoted by Σ(t) = A(t) −B(t).
This spread is
Σ(t) =
µPg(t)
ε+µPg(t)( ¯Si −E[Si|t]) +
µPb(t)
ε+µPb(t)(E[Si|t] −Si) . The ﬁrst term in the bid–ask spread
equation is a probability of buy order based on information and the second is the term for
sells. The spread for the initial quotes in the period, Σ, has a particular simple form in the
natural case in which good and bad events are equally likely. That is, if δ = 1 −δ, then
Σ =
αµ
αµ+2ε( ¯Si −Si) . The key component of this model is the probability that an order is
12


### Page 13

from an informed trader, which is called the PIN =
αµ
αµ+2ε , where αµ + 2ε is the arrival
rate for all orders and αµ is the arrival rate for information-based orders. Therefore, the
PIN is a measure of the fraction of orders that arise from informed traders relative to the
overall order ﬂow, and the spread equation shows that it is the key determinant of spreads.
These equations clarify that liquidity providers need to correctly estimate the PIN in order
to identify the optimal levels at which to enter the market. An unanticipated increase in
PIN will result in losses to those liquidity providers who do not adjust their prices.
It is diﬃcult to estimate the parameter vector θ = (α, δ, ε, µ) because it cannot be
directly observed in either the occurrence of information events or the associated arrival of
uninformed and informed traders. In fact, in terms of measuring the daily arrival rate of sell
(st) and buy (bt) it is possible to infer these values using maximum likelihood and assuming
that the trading process follows a Poisson process (Karyampas and Paiardini, 2011).
The Easley et al. (1996) PIN estimator considers the likelihood of order arrivals during
a discrete trading block. In this model, the likelihood of observing sell S and buy B orders
on each type of information occurs on a no event block with probability 1 −α, a bad event
block with probability αδ and a good event block with probability α(1 −δ). Therefore, the
likelihood is
Li(θ) =(1 −α)e−εb (εb)Bi
Bi! e−εs (εs)Si
Si!
+ αδe−εb (εb)Bi
Bi! e−εs+µ(εs + µ)Si
Si!
+ α(1 −δ)e−εb+µ(εb + µ)Bi
Bi!
e−εs (εs)Si
Si!
.
Since only one type of information occurs in each trading block, the maximum likelihood
estimator of the information event parameters α and δ will be either 0 or 1. However, these
parameters can be estimated from each block of buy and sells, assuming that the blocks are
approximately independent. The likelihood of observing the data M = (Bi, Si)I
i=1 across I
13


### Page 14

trading block is just the product of the daily likelihood function: L(M|θ) =
IQ
i=1
L(θ|Bi, Si) .
The PIN estimates are computed by maximizing the parameter vector θ from any data set
M, which is normally taken to be from the daily trades and quotes. For certain experiments
I also use 30, 60 and 90 day PIN estimates, these experiments are described in the following
section. As a quantity estimated by maximum likelihood I can make use the ‘delta method’
to compute analytical conﬁdence bounds. First, let the log-likelihood function of the PIN
be given by:
L [M|θ] =
PI
i=1 log(Li(θ))
=
PI
i=1 log

−α(δ−1)εSi(µ+ε)Bi+αδεBi(µ+ε)Si−(α−1)εBi+Si
Bi!Si!

−2ε
(3.1)
The analytical gradient, ∇L [M|θ] =
∂
∂θ
Pl
i=1 Li(Bi, Si|θ), of L [M|θ] is given by:
∇L [M|θ] =
l
X
i=1












α −
εBi+Si
(δ−1)εS
i (µ+ε)B
i −δεB
i (µ+ε)S
i +εBi+Si
−1

εS
i ((α−1)εB
i −α(µ+ε)B
i )
α(εS
i (µ+ε)B
i −εB
i (µ+ε)S
i ) + δ
−1
εS
i (α(δ−1)(µ+ε)B
i (Biε+Si(µ+ε))+(α−1)(Bi+Si)εB
i (µ+ε))−αδεB
i (µ+ε)S
i (Bi(µ+ε)+Siε)
ε(µ+ε)(α(δ−1)εS
i (µ+ε)B
i −αδεB
i (µ+ε)S
i +(α−1)εBi+Si)
−2
α(Bi(δ−1)εS
i (µ+ε)B
i −δSiεB
i (µ+ε)S
i )
(µ+ε)(α(δ−1)εS
i (µ+ε)B
i −αδεB
i (µ+ε)S
i +(α−1)εBi+Si)











(3.2)
Let ∇2L [M|θ] be the Hessian matrix of second order derivatives such that ∇2L [M|θ] =
∂2
∂θ∂θ′
PI
i=1 Li(Bi, Si|θ). For the maximized likelihood, with parameter vector ˆθ the Hessian
(Fisher information matrix) is denoted by ∇2L [M|ˆθ]. Let ∇P[θ] =
∂
∂θP[θ] and is derived
analytically by:
14


### Page 15

∇P[θ] =









µ
αµ+2ε −
αµ2
(αµ+2ε)2
0
−
2αµ
(αµ+2ε)2
α
αµ+2ε −
α2µ
(αµ+2ε)2









(3.3)
at the maxima, asymptotically, the PIN estimator is derived from a standard binomial
tree and as such the likelihood estimator will obey the standard central limit theorems.
Subsequently, let ¯θ be the true parameter estimates, from the standard Gaussian limit
theorem the Cram´er-Rao bound is given by
√
I(¯θ −ˆθ) ∼N(0, ∇2L [M|ˆθ]−1). From the
standard delta method, the variance of the PIN estimates will be given by:
√
I(P[¯θ] −P[ˆθ]) →d N(0, ∇P[ˆθ]′∇2L [M|ˆθ]−1∇P[ˆθ])
It is relatively straightforward to observe that the variance of the PIN estimates ∇P[ˆθ]′∇2L [M|ˆθ]−1∇P[ˆθ]
is easily speciﬁed as follows.
Let I ˆΩ= ∇2L [M|ˆθ]−1, with elements [ˆωij] where i, j ∈
{α, δ, ε, µ} be the covariance matrix of the physically estimated parameters, {α, δ, ε, µ}.1 To
test the signiﬁcance of shifts in the PIN, I compute cumulative sums of the PIN estimates
and use the standard central limit theorem to compute conﬁdence intervals. I will now move
on to look at the VPIN, which is computed directly from the moments of the order-ﬂow so
I compute the error variance of VPIN via iid. bootstrap resampling.
Proposition 1. The standard error of the estimated PIN: the asymptotic standard
error of the PIN is given by
\
st.dev(P[¯θ] −P[ˆθ]) →d
s
4ˆα
 ˆµ
 2ˆε(ˆε −ˆα)ˆωˆεˆµ + ˆαˆµˆωˆεˆε −2ˆµˆεˆωˆδˆε

+ ˆαˆε2ˆωˆµˆµ

+ 4ˆµ2ˆε2ˆωˆαˆα
(ˆαˆµ + 2ˆε)4
(3.4)
Proof. Follows from the statements above and a detailed derivation is given in the following
1Whilst the point estimates of the PIN are commonly used across academic and practitioner implemen-
tations the exact identiﬁcation
15


### Page 16

section.
Traditional implementations of PIN (see for instance the Matlab implementation by
Paolo Zagaglia on the Mathworks webpage and the SAS standard calculation) invoke an
unconstrained optimization to compute the PIN. However, I take advantage of the analytical
nature of the gradient function and make full use of a standard Newtonian approach, this
is both faster and less prone to an erroneous exit. The matrix of second order derivatives
allows us to compute an asymptotic standard error, which I can then use to construct my
rolling z-tests to detect the signiﬁcance of changes in PIN over time.
To compute the asymptotic variance of the PIN from the maximum likelihood estimate,
I take advantage of the implicit asymptotic normality of the variance covariance matrix from
the estimator and proceed using the standard Delta method approach.
Let Bi and Si be the observed counts of buys and sells from the order-ﬂow, using my
trade classiﬁcation mechanism. Unfortunately, I do not have a good way of measuring the
error covariance matrix on Bi and Si therefore I have to treat the estimates as non-stochastic
in this instance. The log-likelihood of the i observation of Bi and Si from i ∈{1, . . . , I},
given my model setting is identical to the standard PIN formulation, with parameter vector
θ = [α, δ, ε, µ]′, is denoted by
Li(θ) = log
−α(δ −1)εSi(µ + ε)Bi + αδεBi(µ + ε)Si −(α −1)εBi+Si
Bi!Si!

−2ε
(3.5)
summing over the I observations L(θ) = P
i Li(θ) and taking the ﬁrst derivative yields the
16


### Page 17

analytic gradient:
∇L(θ) =
X
i



α−
εBi+Si
(δ−1)εSi (µ+ε)Bi −δεBi (µ+ε)Si +εBi+Si
−1
εSi((α−1)εBi −α(µ+ε)Bi)
α(εSi (µ+ε)Bi −εBi (µ+ε)Si)
+δ
!−1
εSi(α(δ−1)(µ+ε)Bi (Biε+Si(µ+ε))+(α−1)(Bi+Si)εBi (µ+ε))−αδεBi (µ+ε)Si (Bi(µ+ε)+Siε)
ε(µ+ε)(α(δ−1)εSi (µ+ε)Bi −αδεBi (µ+ε)Si +(α−1)εBi+Si)
−2
α(Bi(δ−1)εSi (µ+ε)Bi −δSiεBi (µ+ε)Si)
(µ+ε)(α(δ−1)εSi (µ+ε)Bi −αδεBi (µ+ε)Si +(α−1)εBi+Si)


(3.6)
with analytical second derivative H = ∇2L[M|θ], with elements [hij] where i, j ∈{α, δ, ε, µ}
the unique (upper triangular) elements are given as follows:
hαα =
X
i
−
 (δ −1)εSi(µ + ε)Bi −δεBi(µ + ε)Si + εBi+Si2
A 2
(3.7)
hαδ =
X
i
εBi+Si  εBi(µ + ε)Si −εSi(µ + ε)Bi
A 2
(3.8)
hδε =
X
i
µDεBi+Si−1
A 2(µ + ε)
(3.9)
hεµ =
X
i
DεBi+Si
A 2(µ + ε)
(3.10)
hδδ =
X
i
−α2  εSi(µ + ε)Bi −εBi(µ + ε)Si2
A 2
(3.11)
hδε =
X
i
αµ(E G )εBi+Si−1
A 2(µ + ε)
(3.12)
hδµ =
X
i
−(E G )εBi+Si
A 2(µ + ε)
(3.13)
hεε =
X
i
A B −
F2
ε2(µ+ε)2
A 2
(3.14)
hεµ =
X
i
C
A 2ε(µ + ε)2
(3.15)
hµµ =
X
i
(−α)A D
(µ+ε)2
−
 αBi(δ −1)εSi(µ + ε)Bi−1 −αδSiεBi(µ + ε)Si−12
A 2
(3.16)
17


### Page 18

where the functions A , B, C , D, E , F and G are deﬁned as follows:
A =α(δ −1)εSi(µ + ε)Bi −αδεBi(µ + ε)Si + (α −1)εBi+Si
(3.17)
B =α(Bi −1)BiδεBi−2(µ + ε)Si + 2αBiδSiεBi−1(µ + ε)Si−1
(3.18)
−α(δ −1)(Si −1)SiεSi−2(µ + ε)Bi −2αBi(δ −1)SiεSi−1(µ + ε)Bi−1
−α(Bi −1)Bi(δ −1)εSi(µ + ε)Bi−2
+ αδ(Si −1)SiεBi(µ + ε)Si−2 −(α −1)(Bi + Si −1)(Bi + Si)εBi+Si−2
C =α(Ca + Cb + Cc)
(3.19)
Ca =δSiεBi(µ + ε)Si

εSi(µSi + ε)

α(δ −1)(µ + ε)Bi + (α −1)εBi

−αδεBi+1(µ + ε)Si

(3.20)
Cb =Bi(δ −1)εSi(µ + ε)Bi

αδεBi(µ + ε)Si(ε −2µSi) + εSi+1 
−α(δ −1)(µ + ε)Bi −(α −1)εBi

(3.21)
Cc = −Bi2(δ −1)µεBi+Si(µ + ε)Bi

(α −1)εSi −αδ(µ + ε)Si

(3.22)
D =Bi(δ −1)εSi(µ + ε)Bi −δSiεBi(µ + ε)Si
(3.23)
E =(α −1)SiεBi + α(Bi −Si)(µ + ε)Bi
(3.24)
F =αδεBi(µ + ε)Si(Bi(µ + ε) + Siε)
(3.25)
−εSi

α(δ −1)(µ + ε)Bi(Biε + Si(µ + ε)) + (α −1)(Bi + Si)εBi(µ + ε)

G =(µ + ε)Si −(α −1)BiεSi(µ + ε)Bi
(3.26)
setting ˆθ = [ˆα, ˆδ, ˆε, ˆµ]′, to the be the numerically evaluated parameters such that ∇L(ˆθ) = 04.
Where 04 is a 4 × 1 vector of zeros. Under mild regularity conditions the maximum of the
function L(θ) can be quickly computed via the Newton-Raphson approach.
The estimate of the asymptotic covariance matrix ˆΩ= cov[¯θ −ˆθ], where ¯θ is the true
parameter vector is computed from the Hessian matrix following Fisher’s theorem by I ˆΩ=
H−1.
3.2.1. The Asymptotic Estimate Variance of PIN
From the theoretical composition the formulation of the estimated PIN is P[θ] =
αµ
αµ+2ε.
Inserting my estimated values yields P[ˆθ] =
ˆαˆµ
ˆαˆµ+2ˆε.
My presumption is that
√
I(P[¯θ] −
P[ˆθ]) →d N(0, ς2), where ς2 is an asymptotic variance.
I can conﬁrm this presumption
relatively easily, ﬁrst by conﬁrming that the gradient ∇P[θ], is a smooth function of the
18


### Page 19

underlying parameters:
∇P[θ] =









µ
αµ+2ε −
αµ2
(αµ+2ε)2
0
−
2αµ
(αµ+2ε)2
α
αµ+2ε −
α2µ
(αµ+2ε)2









(3.27)
and second I can derive the exact formulation via the Delta method: ς2 = ∇P[ˆθ]′ ˆΩ∇P[ˆθ].
Substitution and rearrangement yields
√
I(P[¯θ] −P[ˆθ]) →d N(0, ∇P[ˆθ]′∇2L[M|ˆθ]−1∇P[ˆθ]).
Evaluating the term ∇P[ˆθ]′∇2L[M|ˆθ]−1∇P[ˆθ], dividing by I and taking the square root,
yields the standard error in the proposition 1
3.3. The implementation of Volume-Synchronized Probability of Informed Trading (VPIN)
This work uses a variety of choices for implementing VPIN with arrival rate of informed
and uninformed traders in Realized Volatility(RV) style. For original work Easley et al.
(2011), the ﬁxed number of volume buckets VPIN(n) is ﬁxed at 50, however I consider n =
20, 50, 100, 200 and compute the bucket size (Vi) as a fraction of daily trading volume to
avoid the bias of activity or inactivity of trading period. So, the VPIN is calculated with Vi =
1/20, 1/50, 1/100, and 1/200. My choices for complimenting VPIN not only calculate with
diﬀerent n and Vi but also using tick-by-tick data instead of one-minute interval as in the
original work. I work with tick-by-tick data because I want to implement this approach with
the real high frequency world, trading at the speed of light or in a fraction of millisecond,
to investigate how the VPIN performs when it is applied with HFTs data.
Prior implementations of VPIN have utilized it as a separate pricing factor within a
standard Fama and Macbeth style cross sectional asset pricing model.
Given that the
purpose of this chapter is to look speciﬁcally at the time series variation in the PIN and
VPIN measures around well understood events in the life-cycle of the contract then I need
to deal speciﬁcally with identiﬁcation of the variation in the measures. For the PIN I can
19


### Page 20

appeal to the asymptotic properties of the maximum likelihood estimator to build a standard
error; however the suggested calculation of the VPIN does not lend itself to direct derivation
of the input parameters Cram´er-Rao bound and hence a standard error. I therefore choose
a double block bootstrap to compute the conﬁdence intervals.
It should be noted that
consistency of a bootstrap in this case is eﬀectively a tautology, in that I impose consistency
on the estimator as each individual step is known to be consistent, but the actual order-ﬂow
imbalance does not have a structural meaning from deep model parameters (although one
could reconstruct a model if necessary).
It can be seen that from the delta method approach used to compute the error variance
for the PIN it is quite possible that the likely data generating process (from the original
PIN type model) results in a VPIN that is not a pivotal statistic (i.e. the distribution of
the VPIN statistic is dependent on the true parameters of the model); as such I iid the
bootstrap in both the major steps in the calculation, the construction of the volume buckets
and the calculation of the resulting VPIN, to compute the conﬁdence intervals for the point
estimates.
My suggested two stage nested bootstrap requires 9,801 resampled proceeds as follows:
Step 1: Bootstrap across buckets. This is the outer loop. Let V , P, P A and P B be the
matrices of volumes, transacted price and nearest preceding bid and ask quote prices
over a day with V †, P †, P A† and P B† being a draw from their equivalent i.i.d. bootstrap
with replacement counterparts. For my purposes I assume that the rows are jointly
bootstrapped such that the resorted rows for V ∗∗, P †, P A† and P B† are all identical.
As the trade classiﬁcations for matched sets of the bootstrapped matrices is identical.
The calculation proceeds exactly, with V †
i and P †
i replacing Vi and Pi.
Step 2: For each V †
i and P †
i compute the bootstrapped V B†
τ
and V S†
τ
and construct the
collection of bootstrap order imbalances OI† = [V S∗∗
τ
−V B†
τ
]τ∈{1,...,N}.
20


### Page 21

Step 3: I now add an interior loop. For each OI† = [V S†
τ
−V B†
τ
]τ∈{1,...,N} iid resample with
replacement 99 times OI†, with each bootstrap resample labelled OI‡ and compute
V PIN ‡. Retain the median V PIN ‡ and return this as V PIN †.
Step 4: Sort the collection of 99 outer loop resampled median V PIN ‡ and then collect the
desired conﬁdence intervals (in my case I choose a 95% conﬁdence interval).
These conﬁdence bounds are applied in the subsequent plots for VPIN presented in sub-
sequent sections and the cumulative error is computed for the conﬁdence bounds in the
tabulated VPIN adjustments.
4. Data Sources
The data used in this research are introduced in this section, together with a preliminary
processing of Eurodollar Futures data. As previously stated, Eurodollar futures contracts
are traded on the CME’s Globex platform and CME pit (open-outcry) trades. Data for
both electronic and open-outcry are directly obtained from the CME tapes for the period
January 1, 1996 to January 1, 2014. Pit trades are quotes from CME by the ED code
and GE for the Globex code; the amalgamated tapes are classiﬁed under the ED moniker.
The volume ratio between the Globex and open-outcry is between three and four orders of
magnitude over the sample, so separating the pit trades from the electronic trades currently
appears to be less interesting. The CME tapes data for the 44 Eurodollar futures contracts is
available from the Thomson Reuter database via the Tick History system. I have conducted
an analysis on the 4 monthly contracts, however the data is very sparse and the volumes
are very small (up to 5 orders of magnitude for busy versus busy days) compared to the 40
quarterly contracts, so for brevity this is excluded from the results. The data records for 40
quarterly Eurodollar future contracts is separated into two diﬀerent time-frames, the ﬁrst
of which was from January 1, 1996 to July 31, 2007, and the second, from August 1, 2007
to January 1, 2014.
21


### Page 22

4.1. The descriptive of the term-structure of PIN and PIN’s parameters
Table 1 presents an estimated PIN and Tables 2, 3, 4, 5 present PIN’s parameters with
its standard deviation for ten to one year to maturity on the period of 1996 until 2013. The
results in this table show that the probability of information event between 1996 and 2001
is high, then begins to drop around 2002; the highest of α is in 2000 at 0.968 and 0.933 for
ten and one year to maturity, respectively. This trend may be consistent with the PIN as
both parameters have a similar trend, however, the highest PIN appears in 1997 with 0.844
and 0.830 for ten and one year to maturity, respectively. During the same period the arrival
rate of informed traders and uninformed traders µ, ε ﬂuctuates mostly between 0.4 and 0.6,
except for 2000 when ε ﬂuctuates around 0.2. After an upward trend of information based
trading for Eurodollar trading in the ﬁrst period, the downward trend appears between 2002
and 2003. This trend can be investigated from the decreases of α and PIN. After 2003, the
PIN and the α are increasing, then turning to a downward trend around 2007. The highest
α appears in 2007 at 0.945 for ten year to maturity, however, the PIN is just about 0.631,
which is lower than 2004, 2005 and 2006 for the same ten year to maturity. From these
results, focusing on PIN and α, this analysis ﬁnds that the PIN is not purely driven by α or
the probability of information that occurs on the trading day. The low(high) of α does not
follow the low(high) of PIN, however, they have a similar trend but are slightly overlapping
for some period(I leave a full investigation for future research). Interestingly, after 2008,
there is a small variation for all parameters, for instance from 2009 to 2013 the α for ten to
one year to maturity shows an average value at 0.4, the average estimate of δ, µ and ε are
0.5. Finally, the average estimated PIN from 2009 has a small variation around 15% from
the identical PIN at 0.667.
22


### Page 23

Table 1: The Term Structure of PIN Coeﬃcient
Time To Maturity
Year
10
9
8
7
6
5
4
3
2
1
1996
0.8098
0.7647
0.6914
0.7150
0.7153
0.6993
0.7623
0.7713
0.8092
0.8170
(0.2788) (0.2848) (0.2887) (0.3087) (0.3015) (0.3263) (0.3099) (0.3043) (0.2780) (0.2772)
1997
0.8444
0.8103
0.7483
0.6866
0.6975
0.7456
0.7374
0.7836
0.8056
0.8300
(0.2517) (0.2577) (0.2728) (0.2718) (0.2525) (0.2917) (0.3073) (0.2879) (0.2716) (0.2646)
1998
0.8065
0.8068
0.7802
0.7366
0.7154
0.6922
0.7360
0.6876
0.7278
0.8073
(0.2724) (0.2699) (0.2813) (0.2694) (0.2653) (0.2787) (0.2425) (0.3036) (0.2999) (0.2717)
1999
0.7276
0.7817
0.8105
0.7850
0.7607
0.7632
0.6647
0.7087
0.6933
0.7109
(0.3015) (0.3071) (0.2893) (0.2922) (0.3121) (0.2721) (0.1925) (0.2421) (0.2554) (0.2823)
2000
0.6997
0.7331
0.7671
0.7560
0.7698
0.7546
0.7360
0.6667
0.6778
0.6757
(0.2434) (0.2447) (0.2464) (0.2546) (0.2731) (0.2654) (0.2770) (0.2073) (0.2194) (0.2310)
2001
0.6388
0.6522
0.6796
0.7133
0.7203
0.7458
0.7090
0.7106
0.6832
0.6962
(0.2132) (0.2229) (0.2537) (0.2747) (0.2759) (0.2829) (0.2502) (0.2578) (0.2259) (0.2019)
2002
0.6381
0.6073
0.6251
0.6698
0.6834
0.7152
0.7634
0.7364
0.7050
0.6215
(0.1838) (0.2027) (0.2351) (0.2567) (0.2875) (0.2731) (0.2852) (0.2538) (0.2418) (0.1799)
2003
0.6167
0.6161
0.5717
0.5974
0.5957
0.6568
0.6989
0.7195
0.7078
0.6927
(0.1817) (0.1629) (0.1830) (0.2061) (0.2002) (0.3044) (0.2989) (0.2949) (0.2601) (0.1959)
2004
0.7098
0.6468
0.6279
0.5763
0.5526
0.5789
0.6672
0.7043
0.7282
0.7128
(0.1951) (0.1662) (0.1625) (0.2106) (0.2160) (0.2618) (0.3165) (0.3137) (0.3069) (0.2752)
2005
0.7122
0.7101
0.6849
0.6645
0.6748
0.5695
0.5816
0.6060
0.6807
0.7503
(0.2551) (0.2464) (0.1237) (0.1463) (0.1658) (0.2214) (0.2352) (0.2856) (0.2944) (0.2958)
2006
0.7046
0.6888
0.6922
0.6922
0.6852
0.6705
0.6431
0.5489
0.5885
0.6941
(0.3113) (0.2662) (0.2590) (0.1300) (0.1345) (0.1247) (0.1588) (0.2764) (0.2989) (0.3212)
2007
0.6314
0.6687
0.6797
0.7076
0.6874
0.6798
0.6627
0.6588
0.6383
0.5902
(0.2956) (0.3046) (0.3022) (0.2549) (0.1736) (0.1300) (0.1297) (0.1001) (0.1703) (0.2684)
2008
0.6338
0.6585
0.6612
0.7146
0.7142
0.6843
0.6794
0.6721
0.6572
0.6289
(0.1935) (0.2315) (0.2903) (0.2832) (0.2702) (0.2283) (0.1043) (0.1254) (0.1352) (0.1870)
2009
0.6692
0.6450
0.6496
0.6510
0.6975
0.6924
0.6960
0.6840
0.6696
0.6584
(0.1006) (0.1502) (0.1805) (0.2376) (0.2376) (0.2342) (0.2073) (0.1017) (0.1210) (0.1311)
2010
0.6782
0.6685
0.6728
0.6480
0.6599
0.6653
0.6960
0.7054
0.6845
0.6869
(0.1149) (0.1226) (0.1025) (0.1327) (0.1275) (0.1631) (0.2048) (0.1713) (0.1281) (0.1163)
2011
0.6884
0.6828
0.6839
0.6806
0.6634
0.6340
0.6245
0.6146
0.6731
0.6814
(0.1048) (0.1214) (0.1164) (0.0979) (0.1212) (0.1998) (0.2392) (0.2971) (0.2308) (0.1194)
2012
0.6976
0.6961
0.6776
0.6845
0.6676
0.6721
0.6552
0.6520
0.6293
0.7058
(0.1190) (0.1153) (0.1101) (0.0987) (0.1206) (0.1282) (0.1356) (0.1747) (0.2129) (0.1735)
2013
0.6866
0.6876
0.6854
0.6784
0.6825
0.6705
0.6811
0.6593
0.6537
0.6341
(0.1401) (0.1379) (0.1041) (0.0853) (0.1086) (0.1200) (0.0984) (0.1177) (0.1356) (0.1788)
Note: This table present the term structure of PIN between 1996 until 2013.
23


### Page 24

Table 2: The Term Structure of α
Time To Maturity
Year
10
9
8
7
6
5
4
3
2
1
1996
0.6862
0.4397
0.3694
0.6110
0.5798
0.8135
0.7971
0.8427
0.8444
0.8241
(0.4172) (0.4599) (0.4425) (0.4523) (0.4530) (0.3238) (0.3365) (0.3084) (0.3012) (0.3215)
1997
0.8397
0.6715
0.4508
0.3725
0.3328
0.5229
0.7255
0.7540
0.8000
0.8392
(0.3043) (0.4132) (0.4367) (0.4275) (0.4167) (0.4702) (0.3800) (0.3791) (0.3468) (0.3130)
1998
0.8959
0.8844
0.7302
0.4949
0.5258
0.5335
0.3227
0.8212
0.8005
0.8366
(0.2522) (0.2619) (0.3890) (0.4274) (0.4232) (0.3774) (0.4406) (0.3408) (0.3570) (0.3305)
1999
0.9298
0.9261
0.9233
0.8853
0.8506
0.6524
0.4157
0.3710
0.5723
0.9254
(0.2191) (0.2156) (0.2249) (0.2477) (0.3224) (0.4398) (0.3204) (0.4701) (0.4867) (0.2356)
2000
0.9541
0.9620
0.9612
0.9594
0.9556
0.8109
0.6672
0.3857
0.4373
0.9333
(0.1925) (0.1614) (0.1583) (0.1481) (0.1587) (0.3394) (0.4331) (0.3629) (0.4262) (0.2304)
2001
0.9683
0.9851
0.9643
0.9645
0.9612
0.9740
0.8149
0.6860
0.6992
0.5722
(0.1575) (0.0972) (0.1633) (0.1554) (0.1622) (0.1090) (0.2865) (0.4060) (0.3771) (0.4806)
2002
0.6755
0.9828
0.9677
0.9571
0.9569
0.9419
0.9209
0.8182
0.7052
0.5992
(0.3670) (0.1190) (0.1621) (0.1746) (0.1713) (0.1761) (0.2088) (0.2702) (0.3065) (0.3175)
2003
0.5988
0.7065
0.9769
0.9909
0.9904
0.9624
0.9572
0.9390
0.7771
0.6109
(0.3169) (0.2925) (0.1379) (0.0848) (0.0767) (0.1627) (0.1533) (0.1779) (0.2984) (0.2919)
2004
0.5980
0.5023
0.5978
0.7392
0.8601
0.9028
0.9586
0.9374
0.9291
0.7428
(0.2987) (0.2621) (0.2893) (0.3532) (0.2875) (0.2731) (0.1633) (0.1996) (0.2053) (0.3145)
2005
0.7553
0.7535
0.4468
0.4667
0.4357
0.6762
0.8120
0.9315
0.9634
0.9427
(0.3012) (0.2942) (0.1807) (0.2188) (0.2498) (0.3245) (0.3071) (0.2232) (0.1441) (0.1769)
2006
0.9342
0.7797
0.7320
0.4393
0.4435
0.4517
0.4578
0.6563
0.7772
0.9482
(0.1766) (0.3052) (0.3152) (0.1761) (0.1789) (0.1855) (0.1988) (0.3587) (0.3337) (0.1631)
2007
0.9457
0.9563
0.9019
0.7725
0.5291
0.4455
0.4720
0.4978
0.5703
0.8735
(0.1843) (0.1595) (0.2247) (0.3003) (0.2530) (0.1837) (0.1658) (0.1389) (0.2200) (0.2680)
2008
0.6584
0.6865
0.9094
0.9414
0.8248
0.6707
0.4517
0.4701
0.4811
0.4864
(0.2726) (0.3322) (0.2159) (0.1759) (0.2727) (0.2991) (0.1622) (0.1836) (0.1698) (0.2538)
2009
0.4845
0.4891
0.5514
0.6466
0.6862
0.6782
0.6019
0.4497
0.4627
0.4806
(0.1628) (0.1991) (0.2519) (0.3087) (0.3077) (0.3016) (0.2790) (0.1613) (0.1515) (0.1536)
2010
0.4397
0.4598
0.4721
0.4822
0.4741
0.4311
0.3419
0.4302
0.4533
0.4363
(0.1827) (0.1814) (0.1708) (0.1773) (0.1885) (0.2395) (0.3009) (0.2676) (0.1695) (0.1780)
2011
0.4585
0.4399
0.4397
0.4453
0.4638
0.4619
0.4168
0.4388
0.4217
0.4484
(0.1481) (0.1749) (0.1829) (0.1781) (0.1924) (0.2192) (0.2958) (0.3440) (0.3001) (0.1528)
2012
0.4462
0.4565
0.4628
0.4675
0.4564
0.4290
0.4592
0.4096
0.4162
0.4631
(0.1588) (0.1410) (0.1403) (0.1315) (0.1445) (0.1882) (0.1667) (0.2393) (0.2548) (0.2430)
2013
0.4589
0.4524
0.4718
0.4829
0.4743
0.4621
0.4496
0.4763
0.4741
0.4715
(0.1892) (0.1789) (0.1279) (0.1188) (0.1395) (0.1522) (0.1580) (0.1751) (0.1764) (0.1950)
Note: This table present the term structure of α between 1996 until 2013.
24


### Page 25

Table 3: The Term Structure of δ
Time To Maturity
Year
10
9
8
7
6
5
4
3
2
1
1996
0.4535
0.5493
0.6443
0.5895
0.5895
0.4178
0.4014
0.3395
0.3288
0.3233
(0.3907) (0.3529) (0.3358) (0.3858) (0.3750) (0.3983) (0.3926) (0.3903) (0.3832) (0.3732)
1997
0.3127
0.4052
0.5780
0.6575
0.6946
0.5805
0.4662
0.4160
0.3529
0.3434
(0.3632) (0.3633) (0.3319) (0.3181) (0.2871) (0.3645) (0.3889) (0.3966) (0.3837) (0.3893)
1998
0.2308
0.2495
0.3900
0.5104
0.4949
0.5785
0.6735
0.3481
0.3738
0.2973
(0.3472) (0.3475) (0.3758) (0.3225) (0.3339) (0.3093) (0.3105) (0.4010) (0.4062) (0.3888)
1999
0.1739
0.2012
0.2253
0.2654
0.3102
0.4356
0.5907
0.6026
0.4469
0.1657
(0.3244) (0.3353) (0.3551) (0.3496) (0.3856) (0.3607) (0.2397) (0.3510) (0.3927) (0.3299)
2000
0.1007
0.0844
0.1275
0.1280
0.1638
0.3092
0.4081
0.5945
0.5438
0.1326
(0.2752) (0.2362) (0.2878) (0.2762) (0.3182) (0.3630) (0.3755) (0.2773) (0.3376) (0.3033)
2001
0.0537
0.0467
0.0938
0.1015
0.1148
0.1119
0.3045
0.4048
0.3820
0.4013
(0.2055) (0.1914) (0.2576) (0.2598) (0.2770) (0.2573) (0.3212) (0.3678) (0.3440) (0.3873)
2002
0.3212
0.0479
0.0682
0.1234
0.1623
0.1618
0.1930
0.3328
0.4128
0.4266
(0.3130) (0.1955) (0.2258) (0.2957) (0.3302) (0.3045) (0.3133) (0.3176) (0.2828) (0.2766)
2003
0.4166
0.3342
0.0368
0.0287
0.0327
0.1116
0.1381
0.1963
0.3578
0.4599
(0.2780) (0.2919) (0.1732) (0.1574) (0.1712) (0.2749) (0.2831) (0.3264) (0.3260) (0.2437)
2004
0.4586
0.4809
0.4219
0.2621
0.1627
0.1515
0.1747
0.2263
0.2422
0.3938
(0.2539) (0.2228) (0.2595) (0.3112) (0.2947) (0.3151) (0.3390) (0.3656) (0.3597) (0.3179)
2005
0.3839
0.4024
0.5176
0.5252
0.5334
0.3796
0.2374
0.1696
0.1599
0.1818
(0.3184) (0.3228) (0.1381) (0.1824) (0.1906) (0.3175) (0.3114) (0.3339) (0.3185) (0.3270)
2006
0.2402
0.3617
0.3889
0.5309
0.5269
0.5333
0.5166
0.3997
0.3428
0.2034
(0.3508) (0.3348) (0.3081) (0.1446) (0.1449) (0.1438) (0.1625) (0.3307) (0.3522) (0.3357)
2007
0.1413
0.1668
0.2340
0.3519
0.4718
0.5308
0.5168
0.5137
0.4559
0.2203
(0.3013) (0.3173) (0.3362) (0.3331) (0.1977) (0.1344) (0.1300) (0.1116) (0.1936) (0.3253)
2008
0.4101
0.3802
0.2172
0.1620
0.3005
0.4014
0.5187
0.5211
0.5231
0.5032
(0.2581) (0.3011) (0.3225) (0.2958) (0.3186) (0.2681) (0.1144) (0.1346) (0.1363) (0.1988)
2009
0.5130
0.5188
0.4940
0.4618
0.4369
0.4206
0.4560
0.5169
0.5206
0.5216
(0.1197) (0.1572) (0.1986) (0.2882) (0.2831) (0.2730) (0.2292) (0.1190) (0.1120) (0.1233)
2010
0.5214
0.5240
0.5229
0.5177
0.5343
0.5196
0.5598
0.5180
0.5106
0.5244
(0.1277) (0.1333) (0.1330) (0.1366) (0.1509) (0.1682) (0.2295) (0.1976) (0.1425) (0.1366)
2011
0.5046
0.5117
0.5151
0.5305
0.5207
0.5331
0.5662
0.5671
0.5501
0.5145
(0.1248) (0.1351) (0.1297) (0.1364) (0.1448) (0.1727) (0.2276) (0.2624) (0.2290) (0.1172)
2012
0.5177
0.5092
0.5236
0.5142
0.5309
0.5345
0.5165
0.5562
0.5589
0.5474
(0.1374) (0.1145) (0.1185) (0.1135) (0.1178) (0.1375) (0.1233) (0.1836) (0.1992) (0.1688)
2013
0.5288
0.5268
0.5092
0.5074
0.5091
0.5159
0.5210
0.5156
0.5258
0.5301
(0.1452) (0.1494) (0.1112) (0.0977) (0.1039) (0.1190) (0.1149) (0.1316) (0.1335) (0.1579)
Note: This table present the term structure of δ between 1996 until 2013.
25


### Page 26

Table 4: The Term Structure of µ
Time To Maturity
Year
10
9
8
7
6
5
4
3
2
1
1996
0.6826
0.6188
0.5320
0.5583
0.5474
0.5476
0.5721
0.6128
0.6569
0.6950
(0.3179) (0.3002) (0.2658) (0.2909) (0.2840) (0.3023) (0.2981) (0.3058) (0.3006) (0.3054)
1997
0.7043
0.6745
0.6056
0.5340
0.5286
0.5756
0.5249
0.5617
0.6136
0.6594
(0.2907) (0.2914) (0.2863) (0.2561) (0.2381) (0.2758) (0.2915) (0.2866) (0.2905) (0.2948)
1998
0.6654
0.6885
0.6415
0.5941
0.5846
0.5127
0.5785
0.5160
0.5459
0.6177
(0.2755) (0.2873) (0.3052) (0.2770) (0.2714) (0.2554) (0.2376) (0.2712) (0.2801) (0.2817)
1999
0.6009
0.6665
0.7056
0.6927
0.6700
0.6678
0.5077
0.5837
0.5728
0.5820
(0.2803) (0.3050) (0.3001) (0.3060) (0.3223) (0.2911) (0.1709) (0.2326) (0.2350) (0.2502)
2000
0.5863
0.6235
0.6907
0.7003
0.7116
0.6612
0.6402
0.5118
0.5380
0.5358
(0.2202) (0.2299) (0.2368) (0.2554) (0.2769) (0.2791) (0.2808) (0.1856) (0.2044) (0.1951)
2001
0.5353
0.5714
0.6037
0.6539
0.6547
0.6988
0.6292
0.6203
0.5711
0.5849
(0.1822) (0.2000) (0.2392) (0.2649) (0.2681) (0.2762) (0.2599) (0.2629) (0.2253) (0.1899)
2002
0.5307
0.5186
0.5490
0.5975
0.6215
0.6597
0.6983
0.6562
0.6024
0.4833
(0.1742) (0.1721) (0.2119) (0.2384) (0.2712) (0.2708) (0.2926) (0.2713) (0.2582) (0.1527)
2003
0.4775
0.4924
0.4973
0.5352
0.5345
0.6129
0.6536
0.6729
0.6151
0.5674
(0.1552) (0.1372) (0.1593) (0.1893) (0.1838) (0.2954) (0.2918) (0.2938) (0.2668) (0.2079)
2004
0.5721
0.4992
0.4918
0.4727
0.4584
0.4955
0.6074
0.6304
0.6567
0.6029
(0.2080) (0.1502) (0.1390) (0.1778) (0.1838) (0.2378) (0.3043) (0.3162) (0.3110) (0.2828)
2005
0.6163
0.6097
0.5164
0.5060
0.5114
0.4630
0.4858
0.5449
0.6257
0.6969
(0.2669) (0.2615) (0.1247) (0.1391) (0.1657) (0.1953) (0.2132) (0.2678) (0.2877) (0.2966)
2006
0.6374
0.5939
0.5845
0.5166
0.5172
0.5051
0.4911
0.4479
0.5000
0.6233
(0.3060) (0.2689) (0.2604) (0.1345) (0.1377) (0.1214) (0.1348) (0.2389) (0.2740) (0.3098)
2007
0.5492
0.5916
0.5942
0.6100
0.5331
0.5029
0.5035
0.5004
0.4891
0.5035
(0.2648) (0.2816) (0.2808) (0.2569) (0.1762) (0.1190) (0.1163) (0.0960) (0.1433) (0.2350)
2008
0.5157
0.5675
0.6171
0.6744
0.6480
0.5741
0.5120
0.5061
0.4967
0.4874
(0.1790) (0.2345) (0.2876) (0.2817) (0.2786) (0.2344) (0.1044) (0.1172) (0.1189) (0.1673)
2009
0.5118
0.4950
0.5129
0.5397
0.5852
0.5819
0.5650
0.5160
0.5035
0.4964
(0.1052) (0.1323) (0.1731) (0.2324) (0.2448) (0.2447) (0.2211) (0.1050) (0.1098) (0.1106)
2010
0.5122
0.5037
0.5089
0.4919
0.5087
0.5162
0.5628
0.5493
0.5111
0.5151
(0.1150) (0.1169) (0.1004) (0.1165) (0.1213) (0.1561) (0.2077) (0.1876) (0.1300) (0.1224)
2011
0.5169
0.5082
0.5171
0.5142
0.5061
0.4944
0.5025
0.5075
0.5398
0.5068
(0.1161) (0.1175) (0.1162) (0.1026) (0.1105) (0.1801) (0.2223) (0.2812) (0.2317) (0.1136)
2012
0.5254
0.5259
0.5000
0.5144
0.4968
0.5121
0.4983
0.5095
0.4955
0.5438
(0.1292) (0.1192) (0.1165) (0.1140) (0.1045) (0.1237) (0.1224) (0.1651) (0.1925) (0.1857)
2013
0.5277
0.5226
0.5169
0.5017
0.5121
0.5032
0.5123
0.4990
0.4953
0.4870
(0.1425) (0.1475) (0.1210) (0.0955) (0.1024) (0.1106) (0.1043) (0.1089) (0.1179) (0.1544)
Note: This table present the term structure of µ between 1996 until 2013.
26


### Page 27

Table 5: The Term Structure of ε
Time To Maturity
Year
10
9
8
7
6
5
4
3
2
1
1996
0.4180
0.3983
0.4433
0.4559
0.5022
0.5236
0.4469
0.4824
0.4537
0.4505
(0.2939) (0.2399) (0.2219) (0.3008) (0.2785) (0.3344) (0.3431) (0.3546) (0.3429) (0.3302)
1997
0.4303
0.4161
0.4138
0.4720
0.4391
0.4752
0.4590
0.4096
0.4088
0.4006
(0.3281) (0.3008) (0.2411) (0.2188) (0.1878) (0.2866) (0.3095) (0.3284) (0.3328) (0.3406)
1998
0.4414
0.4908
0.4410
0.4473
0.4842
0.4589
0.4954
0.5319
0.5018
0.4334
(0.3693) (0.3618) (0.3240) (0.2599) (0.2547) (0.2336) (0.1996) (0.3257) (0.3390) (0.3547)
1999
0.5075
0.4977
0.5163
0.5377
0.5323
0.5250
0.5076
0.5465
0.5573
0.5157
(0.3673) (0.3859) (0.3849) (0.3538) (0.3563) (0.2988) (0.1504) (0.2082) (0.2439) (0.3469)
2000
0.5648
0.5380
0.6025
0.6524
0.6327
0.5675
0.5656
0.4973
0.5224
0.5441
(0.3181) (0.3387) (0.3958) (0.3721) (0.3896) (0.3557) (0.3204) (0.1383) (0.1753) (0.2755)
2001
0.6293
0.6844
0.6769
0.6708
0.6507
0.6719
0.6107
0.5842
0.5783
0.5787
(0.2460) (0.2808) (0.3250) (0.3584) (0.3737) (0.3699) (0.3323) (0.3070) (0.2604) (0.1815)
2002
0.6221
0.6801
0.6970
0.6839
0.6985
0.6641
0.5945
0.5748
0.5695
0.5648
(0.1689) (0.2258) (0.2677) (0.3189) (0.3570) (0.3444) (0.3553) (0.3075) (0.2608) (0.1466)
2003
0.5518
0.6066
0.7263
0.7431
0.7490
0.7027
0.6813
0.6503
0.5707
0.5343
(0.1535) (0.1718) (0.1766) (0.2305) (0.2144) (0.3425) (0.3496) (0.3481) (0.3087) (0.2245)
2004
0.5231
0.5206
0.5635
0.6433
0.6670
0.6847
0.7014
0.6732
0.6494
0.5584
(0.2335) (0.1403) (0.1577) (0.1884) (0.1953) (0.2443) (0.3476) (0.3515) (0.3589) (0.3175)
2005
0.5641
0.5725
0.4613
0.5008
0.5187
0.6296
0.6537
0.7211
0.6872
0.6181
(0.3011) (0.2900) (0.1284) (0.1210) (0.1448) (0.1880) (0.2295) (0.3108) (0.3422) (0.3577)
2006
0.6274
0.6044
0.5766
0.4445
0.4533
0.4841
0.5265
0.6419
0.6613
0.6133
(0.3551) (0.3164) (0.3050) (0.1475) (0.1333) (0.1178) (0.1222) (0.2370) (0.2885) (0.3555)
2007
0.6690
0.6567
0.6227
0.5901
0.4757
0.4587
0.5003
0.5143
0.5427
0.6882
(0.3515) (0.3757) (0.3712) (0.3251) (0.2121) (0.1297) (0.1109) (0.0684) (0.1647) (0.2951)
2008
0.6122
0.6559
0.7418
0.7132
0.6333
0.5898
0.4738
0.4973
0.5160
0.5585
(0.2271) (0.2615) (0.3059) (0.3444) (0.3343) (0.2754) (0.0859) (0.0990) (0.0944) (0.1412)
2009
0.5104
0.5352
0.5686
0.6160
0.5960
0.5619
0.5145
0.4743
0.4823
0.5030
(0.0754) (0.1256) (0.1786) (0.2524) (0.2742) (0.2641) (0.2230) (0.1072) (0.0995) (0.1055)
2010
0.4766
0.4923
0.4973
0.5191
0.5263
0.5281
0.5174
0.4590
0.4457
0.4550
(0.0972) (0.1122) (0.0906) (0.0889) (0.0971) (0.1485) (0.1848) (0.1815) (0.1341) (0.1134)
2011
0.4547
0.4503
0.4659
0.4827
0.5083
0.5366
0.5755
0.5900
0.5241
0.4522
(0.1206) (0.1231) (0.1018) (0.0925) (0.0871) (0.1490) (0.1822) (0.2228) (0.2000) (0.1280)
2012
0.4463
0.4531
0.4582
0.4598
0.4684
0.5039
0.5068
0.5434
0.5663
0.4724
(0.1512) (0.1362) (0.1300) (0.1221) (0.1047) (0.1110) (0.1024) (0.1352) (0.1549) (0.1811)
2013
0.4943
0.4861
0.4657
0.4692
0.4612
0.4746
0.4756
0.5052
0.5143
0.5368
(0.1515) (0.1528) (0.1200) (0.1118) (0.1181) (0.1117) (0.0951) (0.0969) (0.0997) (0.1436)
Note: This table present the term structure of ε between 1996 until 2013.
27


### Page 28

Table 6: Comparison between average ‘Probability of Informed Trading’ estimates
across various studies and markets.
Author
Asset
Sample Period
Min–max
Mean
Easley et al. (1996),(PIN)
NYSE – 90 stocks
Oct. 1, 1990 to Dec. 23, 1990
0.120–0.342
0.197
Idier and Nardelli (2011)(PIN)
Euro overnight interbank
rate, Money market
Dec. 2000 to Mar. 2008
0.200–0.580
0.480
Easley et al. (2012),(VPIN)
E-mini S&P 500 (CME)
Jan. 1, 2008 to Oct. 30, 2010
0.205–0.830
0.393
T-Note (CBOT)
Jan. 1, 2008 to Oct. 30, 2010
0.200–0.800
0.401
EUR/USD(CME)
Jan. 1, 2008 to Oct. 30, 2010
0.150–0.780
0.327
Brent Crude Oil (ICE)
Jan. 1, 2008 to Oct. 30, 2010
0.200–0.770
0.384
Silver (COMEX)
Jan. 1, 2008 to Oct. 30, 2010
0.200–0.840
0.411
Abad and Yag¨ue (2012),(PIN)
Spanish Stock Exchange
– 15 stocks
Jan. 1, 2009 to Dec. 31, 2009
0.104–0.501
0.227
Kim et al. (2014),(VPIN)
Intra day trading – Eu-
rodollar Futures (CME)
Jan. 3, 2005 to Dec. 29, 2006
0.760–0.970
0.880
Yan and Zhang (2014),(PIN)
NYSE/AMEX
stocks
that
have
data
in
the
ISSM and TAQ databases
Jan, 1, 1983 to Dec. 31, 2004
0.177–0.227
0.201
My PIN
40
Eurodollar
Future
contracts
Jan. 1, 1996 to Jan 1, 2014
0.369–0.992
0.688
My VPIN
40
Eurodollar
Future
contracts
Jan. 1, 1996 to Jan 1, 2014
0.045–0.998
0.126
Note: this table compares the PIN and VPIN from this research with others for various products. It can
be seen that my PIN is higher than other PINs, which might be aﬀected by the trading mechanism in the
futures market which is diﬀerent from the stock exchange; however, my VPIN is lower than other VPINs.
5. Analysis and Implications: PIN and VPIN comparison
The following section presents various results of PIN measures on individual ED futures
contracts following the conditional imputation approach of Easley et al. (1996). It will also
present results for VPIN drawing on Easley et al. (2012) approach but with diﬀerent n and
Vi. First, for the average PINs estimated they are in excess 0.5 for the majority of the
sample. This is high relative to comparable equity market studies, see Table 6. However,
the results coincide with those of Kim et al. (2014) on the CME Globex trades, for a short
sample within my sample and Easley et al. (2012) for related US Dollar Treasury notes.
Second, the average VPIN from my results is 0.126 which is lower than other estimates;
however, the range of VPIN is wider and the minimum VPIN is 0.045 and the maximum is
0.998.
Although from this study the PIN estimates cover between 0.10 and 0.80 in the equities
market, in the derivatives market the range is higher with minimum and maximum values
28


### Page 29

of 0.04 and 0.99, respectively. Also, in the derivatives market the min–max spread is higher
than in the equities market, particularly in the interest rate derivatives market. The highest
mean of PIN appears in Kim et al. (2014) with a value of 0.88 ;yet, the highest actual value
of PIN is shown in this work with the maximum value of 0.992. The minimum VPIN is
0.040 and the maximum is 0.998. Interestingly, the value of PIN in the Eurodollar Futures is
higher than the equity market and always high as presented in this work the PIN is mostly
higher than 0.50. However, despite my PIN being constantly high, the average VPIN in
this study is lower than others such as in Kim et al. (2014) in which it varies between 0.76
and 0.97. Table 6, illustrates this point and this aspect of my study would be interesting to
investigate in the future.
5.1. Following the VPIN Dispute
The VPIN as a tool for detecting excessive levels of order imbalance has been subject
to considerable academic discussion and it is worth reviewing some of the key input choices
in determining its value. As previously noted, Andersen and Bondarenko (2013, 2014c) and
Abad et al. (2015) have criticized the VPIN primarily due to the lack of a good mechanism
to be able to choose the correct bulk volume classiﬁcation. Hence the number of buckets
(n) and the bucket size (Vi) are nuisance parameters with no simple method of constructing
an appropriate statistical loss function to provide guidance on their values. My solution to
this problem is to repeat the analysis over a wide range of diﬀerent n and Vi and, indeed, I
will show that the VPIN, at times, can be sensitive to these choices. Furthermore, this work
computes the VPIN for VPIN20, VPIN50, VPIN100 and VPIN200, then compares them
with original point estimates of the PIN. I can observe from this that there are substantively
diﬀerent values of VPIN during January 19-29 2010; the minimal value of VPIN is VPIN20
and maximal VPIN is VPIN200 almost continuously through this snapshot of data. For
example, PIN and VPIN estimates on January 23, 2010, for the PIN is 0.7521 and 0.0132,
0.0096, 0.0096, 0.0048 for VPIN20, VPIN50, VPIN100 and VPIN200, respectively. From
29


### Page 30

Table 7: Long run correlation coeﬃcients of PIN, VPIN20, VPIN50, VPIN100 and,
VPIN200 on ED?0.
VPIN20
VPIN50
VPIN100 VPIN200 PIN
VPIN20
1
VPIN50
0.9250
1
(0.0000)
VPIN100
0.3127
0.349
1
(0.0000)
(0.0000)
VPIN200
0.2938
0.3297
0.2484
1
(0.0000)
(0.0000)
(0.0000)
PIN
0.1156
0.1362
0.1343
0.0843
1
(0.0000)
(0.0000)
(0.0000)
(0.0051)
Note: This table illustrates the matrix of correlation between PIN, VPIN20, VPIN50,
VPIN100 and, VPIN200 also a matrix of p-values for testing the hypothesis of no corre-
lation with (p < 0.05)
this example we can see that the absolute value of VPIN is sensitive to the choice of n and
Vi is certainly not in question. However, the correlations and cumulative diﬀerences across
choices of n and Vi indicate a high level of agreement in direction, if not in level, which is
in keeping with the commentary made in Easley et al. (2014).
Table 7 presents the correlation matrix and p-values of VPIN and PIN. Noticeably,
there is a positive and signiﬁcant correlation between all ﬁve variables.
This indicates
that there is a signiﬁcant relationship between all ﬁve variables: the highest correlation
is between VPIN20 and VPIN50 with r = 0.9250, n = 1100, p = 0.000 this decreases to
r = 0.3127, 0.2938 and 0.1156 for VPIN100, VPIN200 and PIN respectively.
Figure 2 also illustrates the variability of the VPIN as a function of diﬀerent choices of
n and Vi. The solid line represents the VPIN estimates for March 2002 maturing futures,
the dotted line represents VPIN for June 2002 maturing contracts, and the dashed line
represents the VPIN for September 2002 contracts. For each contract I have ﬁve diﬀerent
30


### Page 31

Figure 2: Comparison of a four diﬀerent types of VPIN on EDH2, EDM2, and EDU2.
Note: This ﬁgure presents the compared plots of ﬁve diﬀerent types of VPIN such as VPIN20,
VPIN50, VPIN100 and VPIN200 between February 27 until March 09, 2012. It can be seen
that VPIN is sensitive to diﬀerent n and Vi, however there is systematic trend between four
types of VPINs. They can be described as, VPIN with n = 20 with Vi = 20, n = 50 with
Vi = 50, n = 100 with Vi = 100, and n = 200 with Vi = 200, also the thick line represents
EDH2, the dotted line represents EDM2 and the dash line represents EDU2.
colors that represent diﬀerent n and Vi choices (n = 20 with Vi = 20, n = 50 with Vi = 50,
n = 100 with Vi = 100, and n = 200 with Vi = 200). The sensitivity, in level, of the VPIN
to n and Vi is self-evident however, the cumulative diﬀerences are highly consistent.
5.2. Empirical evidence, PIN and VPIN on Eurodollar Futures Market
This section presents the results of cross-sectional PIN and VPIN on the Eurodollar
Futures market across 40 contracts from 1996 to 2013 (Figure 3). For the entire sample, I
ﬁnd the PIN and VPIN ﬂuctuate with a downward sloping trend.
The left subplot of Figure 3 shows the average PIN on the left axis, and average VPIN20,
VPIN50, VPIN100, and VPIN200 on the right axis. It also shows ﬂuctuations in PIN and
VPIN. The highest PIN occurs during 1996 to 1998 with a variation around 0.80-0.82.
31


### Page 32

It decreases after 1998 with its lowest value at 0.58 around mid 2002. The PIN, after a
downward trend from 1996 to mid 2002, bounced back and remains constantly high until
2013, at between 0.065 to 0.070. I assume the high value of PIN between 1996 to mid 2002 is
caused by trading activity that operates on an open-outcry platform. This platform, due to
its greater information content, has more eﬀect than the electronic market, and can increase
the PIN. This has been noted by previous studies on the eﬀect of migration from open-
outcry to electronic platforms (Shah and Brorsen (2011); Ates and Wang (2005); Aitken
et al. (2004); Tse and Zabotina (2001) ). This pattern, albeit with some variation, also
appeared on the VPIN.
Overall, the VPIN shows a monotonic decrease from a high point of about 0.40 in 1996 to
between 0.01 and 0.02 in 2012. It gradually drops after CME launched the Globex trading
system in 2002. However, around 2004, the VPIN bounces back. This pattern appears after
routine manipulation of the LIBOR as noted in the FSA and CFTC documents. At the
same time, the VPIN is also constantly high although not higher than pre-2002. However,
I ﬁnd a signiﬁcant decrease in the VPIN around May 2009, when it dropped from about
0.14 to 0.08 compared to the previous period. This decrease is a result of the launch of the
LIBOR manipulation investigation. Thus, historical analysis of both PIN and VPIN shows
variations in the ED futures market consistent with the FSA and CFTC documents. The
same pattern can be observed in PIN and four types of VPIN.
The right subplot of Figure 3 presents cumulative ∆PIN and ∆VPIN. As the PIN and
VPIN have diﬀerences in their range, it is hard to compare them, so, I had to normalize
PIN and VPIN by investigating their diﬀerences - ‘∆PIN’ and ‘∆VPIN’. Using the same
analysis as in the left subplot of Figure 3, I ﬁnd the same results in the right. That is
the major pattern of ∆PIN and ∆VPIN showing a downward trend. Also, the ∆PIN and
∆VPIN had a signiﬁcant drop after the Globex was launched in 2002, then increased again
around 2004. Similarly, I ﬁnd these two indicators increasing again around the time of the
32


### Page 33

Years
1998
2004
2009
PIN
0.6
0.7
0.8
PIN and VPIN On Eurodollar Futures Market
VPIN
0.1
0.2
0.3
Years
1998
2001
2004
2006
2009
2012
PIN
-0.2
0
Cumulative Sum of Delta PIN and Delta VPIN On Eurodollar Futures Market
VPIN
-2
0
PIN
VPIN20
VPIN50
VPIN100
VPIN200
Figure 3: The PIN and VPIN on Eurodollar Futures Market
Note: This Figure presents the PIN and VPIN estimates for the whole cross section of the Eurodollar Futures Market, estimated directly from the limit order
book data.
The left subplot of Figure 3, presents the levels of the PIN and VPIN estimates and the right subplot presents the cumulative change in the PIN and VPIN
estimates from 1996 to 2013 for ease of interrogation. The VPIN is decomposed into four plots, and each represents a diﬀerent choice of volume bucket size
(20, 50, 100 and 200 contracts, with each contract having a notional value of $1million).
All of the PIN and VPIN measures have a substantial downward trend, with an approximate 20% decline over the sample. Interestingly, the measure of PIN
drops several years prior to the measure of VPIN. It is worth noting that the drop in PIN corresponds to the period just prior to the introduction of the ‘Globex’
electronic trading platform and then stays relatively low thereafter. The pattern of the trend in VPIN is slightly diﬀerent, albeit the level of reduction (around
a 20% decline from 1996 to 2013) is very similar. The drop oﬀin VPIN occurs in two sharp declines, one in 2003 and a second sharper decline in 2008/9.
33


### Page 34

ﬁnancial crisis, then dropping. However, ∆VPIN appears to be more sensitive than ∆PIN,
as at the beginning of 2004 it dropped around 0.5 or 50% compared to 2002. During the
same period, ∆PIN dropped only 10%. Also, there was a rapid decrease in VPIN after the
LIBOR investigation with ∆VPIN dropping from -0.05 to -0.15 compared to the previous
period.
5.3. Term Structure of PIN and VPIN
The left subplot of Figure 4 presents a cross-section of the term structure of PIN for 40
Eurodollar futures contracts for 3,653 days. In this ﬁgure I overlay plots of historical PIN
against Days-To-Maturity (X axis) to investigate the variation of long term relationships.
Although I have 40 diﬀerent historical PINs, all show a similar pattern. The ﬁgure shows
that from 3,653 to 3,000 days to maturity the PIN shows values between 0.62 to 0.92. After
this period, the PIN slightly decreases and then drops to its lowest value at 0.32 at around
1,400 days to maturity. However, at this point PIN are highly volatile with a range of 40%
with the highest PIN about 0.72 and the lowest 0.32. However, after 365 days to maturity
the PIN had a much lower variation of around 0.15 to 0.10. One ﬁnal ﬁnding from this
plot is that from 1,400 days to maturity, the term structure of PIN tended to be V-shaped
similar to the term structure of the price of futures.
The right subplot of Figure 4 presents a term structure of cumulative ∆PIN for 40
Eurodollar futures contracts for a 10 year period. In this ﬁgure, there is a similar pattern
in the term structure of PIN and cumulative ∆PIN. Using the same format as in the left
subplot of Figure 4 to illustrate the term structure of cumulative ∆PIN, I ﬁnd a downward
trend from the ﬁrst trading day until 1,800 days to maturity. From the beginning of this
trading period the cumulative ∆PIN varies around 20% between 0 to 0.2, then drops to
its lowest value of between -0.5 and -0.1. Furthermore, at this point of time the cumulative
∆PIN were extremely volatile with a range of around 40% with a high of -0.08 and a low
of -0.52. Furthermore, from around 1,400 days to maturity, the cumulative ∆PIN increases
34


### Page 35

Figure 4: Term Structure of PIN
Note: This ﬁgure presents the term structure of PIN that varies between 0.72 to 0.85 from the ﬁrst trading day to 3,000 days to maturity,
then slightly decreases and drops to bottom at around 1,400 days or 3 to 4 years to maturity. The PIN in this period are highly volatile
with a wider range compared to the previous period, the highest PIN at 0.72 and the lowest at 0.32. Furthermore, after three years to
maturity an upward trend of PIN is shown with less volatility, with the lowest at 0.50 and the highest at 0.75, when it comes to shorter
than one year to last trading day.
35


### Page 36

with less variation which narrows to 10% in comparison to 40% in the last period. Finally,
it is interesting to note that the term structure of PIN and cumulative ∆PIN from 1,400
days to expiration have the same V-shape as the typical term structure of futures.
Using the same format analysis from Figure 4, Figure 5 presents the term structure of
VPIN on the left subplot and term structure of cumulative ∆VPIN on the right subplot.
Although I have shown the term structure of PIN from 3,653 days to expiration, I can
present only 1,100 days to maturity for VPIN due to the volume bucket eﬀects. That is to
say, as described in the methodology section, for the VPIN algorithm to work, the volumes
have to completely ﬁll the volume bucket.
It can be seen from the left subplot of Figure 5 that from 1,100 to 700 days to maturity
the term structure of VPIN tends to be U-shaped. The VPIN ﬂuctuates from nearly 0 to just
above 0.50 or 50% diﬀerence. Later, the variation range decreases from 50% to 20% on 700
days to expiration. Next, between 700 to 400 days to maturity, the VPIN slightly increases
from 0.15 to 0.27 respectively, then decreases afterwards. The VPIN drops after 400 days
and slightly increases again at around 120 days to expiry. During 400 to 120 days to expiry,
the VPIN varies around 10% between 0.10 to 0.20. Interestingly, the diﬀerences between
the lowest and highest tend to be narrower closer to maturity. This result is consistent with
(Ballocchi et al. (2001)) in that the range of variation on ED futures price also decreases as
the contracts approach expiration. A remarkable result from this plot indicates that from
365 days to expiration , the term structure of VPIN tends to be V-shaped as the term
structure of futures prices.
The right subplot of Figure 5 presents the term structure of cumulative ∆V PIN across
40 ED contracts with four diﬀerent types of VPIN. Overall, the term structure tends to be V-
shaped similar to the term structure of futures prices, as the range of variation decreases over
the period. The highest ∆V PIN was at the beginning of this period with the minimum at
-2.5 and maximum at nearly 1. From 700 days to maturity, the range of variation increases,
36


### Page 37

Figure 5: Term Structure of VPIN and Term Structure of ∆V PIN
Note: This Figure presents the term structure of VPIN and term structure of ∆V PIN. Despite the term structure of PIN starting
from ten years to maturity, the VPIN can be observed from 1,100 days or around three years to maturity, and this is because there
is not enough trading volume per day that can ﬁll the volume bucket on the VPIN calculation. The term structure of VPIN tends to
be U-shaped from 1,100 days or around three years to maturity and the variation of VPIN tends to be narrow for a shorter time to
maturity. The VPIN drops after 400 days to maturity then has a slight monotonic increase from around 120 days left before the futures
contract expires. The result of the narrow variation of VPIN may be consistent with a previous study that the variation of ED futures
prices also decreases as the contracts approach expiration (Ballocchi et al. (2001)).
37


### Page 38

which is consistent with the term structure of VPIN when it slightly increases at around
700-days to maturity and decreases afterwards.
For clear comparison, this analysis focuses on PIN and VPIN from 1,100 days to maturity.
Therefore, I ﬁnd a similar pattern of the term structure of ∆PIN and ∆V PIN, which
tends to be V-shaped in respect to the term structure of futures contracts. To this end, the
behavior of PIN in Figure 4 and VPIN in Figure 5 leads us to investigate whether time to
maturity can help to explain the change in the variation of PIN and VPIN, ∆PIN and
∆V PIN. The ﬁndings show that time to expiration tends to have an eﬀect on the value
and variation of both PIN and VPIN.
5.4. Correlation Surface
The similar patterns of PIN and VPIN against day-to-maturity leads us to investigate
their relationship with time to maturity. To investigate this, Pearson’s correlation is used
to test the correlation between the PIN and four diﬀerent types of VPIN from 1,000 days
to maturity.
Figure 6 presents the correlation between PIN and VPIN20, VPIN50, VPIN100, VPIN200
from 1,000 days to maturity to expiry date. All types of VPIN positively correlate with PIN
over time to maturity. However, this varies over the whole period as it increases nearer to
maturity. The highest correlation appears between PIN and VPIN20 around 7 days with a
correlation of 0.72. Inspecting the relationship between PIN and four VPIN, I ﬁnd the PIN
and the VPIN50 have a higher correlation compared to VPIN20, VPIN100, VPIN200 except
after 15 days to maturity when the relationship drops lower than the relationship between
PIN and VPIN20. Moreover, around 15 days before the ﬁnal trading day, the highest corre-
lation changes from VPIN50 to VPIN20 then reaches a peak before the end of the contract.
in this period, the lowest correlation appears on VPIN200 followed by VPIN100.this ﬁgure
pinpoints conclusively a strong eﬀect of time to maturity for PIN and VPIN, as results show
a higher correlation nearer to maturity.
38


### Page 39

Figure 6: Surface Plot of the correlation surface between the estimated PIN, VPIN20,
VPIN50, VPIN100, and VPIN200.
Note: This ﬁgure presents the correlation matrix between PIN and VPIN20, VPIN50,
VPIN100, VPIN200 from 1,000 days to maturity. It can be seen that the correlation between
PIN and VPIN signiﬁcantly increases for a shorter time to maturity.
5.5. PIN, VPIN and the LIBOR Manipulation
This section presents PIN and VPIN with the LIBOR manipulation case. Most market
manipulation studies use general publicly available data. However, I use speciﬁc dates of
39


### Page 40

LIBOR manipulation as cataloged in the CFTC and FSA documents. To further investi-
gate risk surrounding these speciﬁc events, I calculate PIN, VPIN20, VPIN50, VPIN100,
and VPIN200 to identify short term risk. I also observe long run behavior from 1996 to 2014.
I make the conjecture that LIBOR manipulation has an eﬀect on PIN and VPIN in the
futures market as ED trading is based on the LIBOR rate. This analysis begins with an
analysis of FSA and CFTC documents regarding dishonest or manipulative submissions of
the LIBOR rate issued to major banks, such as Barclays and RBS. The ﬁndings indicate
that there are two diﬀerent purposes of manipulation before and after the ﬁnancial crisis.
During the pre-crisis, the banks manipulated the LIBOR, attempting to generate competitive
advantage for their trading positions to boost proﬁts. However, during the ﬁnancial crisis,
LIBOR manipulation was an attempt to reduce customer perception of the banks high
borrowing costs as this made them look desperate for cash.
This was part of a beauty
contest designed to ‘reassure’ investors and regulators.
According to the CFTC settlement document, Barclays’ traders attempted to manipu-
late the US Dollar LIBOR from at least mid-2005 to the autumn of 2007, and thereafter
sporadically until 2009. For instance, on March 31, 2006, Barclays employees, including the
bank’s senior Treasury managers, sent a request to a US dollar LIBOR submitter to submit
a higher rate than normal. The submitter replied he would submit the rate requested.2 At
this point, I assume that the PIN and VPIN after the manipulation date should be higher
than the previous period, then lower afterwards.
The top of the left panel of Figure 7 displays PIN and VPIN around March 31, 2006
as recorded in the LIBOR manipulation document. In this case, I can investigate informed
trading around this event by studying the variation of PIN and VPIN by using data from
2CFTC, Order instituting proceedings pursuant to sections 6(c) and 6(d) of the Commodity Exchange
Act, as amended, making ﬁndings and imposing remedial sanctions; In the Matter of Barclays plc, pp. 9–10.
40


### Page 41

EDM6 contract, which has the closest expiry date. I investigate PIN and VPIN on EDH6
because this contract is the nearest expiration futures contract with the largest trading
volume. Overall, the ﬁndings from this analysis show a signiﬁcant increase in PIN and VPIN.
Three days before the event date, the PIN, VPIN20, VPIN50 VPIN100 and VPIN200 move
around 0.67, 0.16, 0.16, 0.165 and 0.125 respectively. Then, from the event date the PIN
and VPIN sharply increases, achieving a peak on April 02, with the PIN at 0.82, VPIN20 at
0.50 and VPIN50 also at 0.50. However, there is no signiﬁcant movement on VPIN10 and
VPIN200.
For clariﬁcation, in the middle row of the left panel, the ﬁgure compares ∆PIN, ∆VPIN
and the last row presents the PIN and VPIN based on the event date. On the day after
the event date, the PIN increases by 0.22 or 22 %, VPIN20 and VPIN50 increases nearly
three times when compared with the event date. Furthermore, three days after the event,
the PIN and VPIN have signiﬁcant decrease as the PIN, VPIN20 and VPIN50 shrinks by
as much as it increased. Despite PIN VPIN20 and VPIN50 having a signiﬁcant movement
around the event, VPIN100 and VPIN200 have no signiﬁcant changes before and after.
The left panel of Figure 7, presents the variation in PIN, VPIN on September 07, 2007,
when Rabobank’s senior US Dollar trader requested a US Dollar submitter to keep the 3M
LIBOR high for the rest of that week.3 This panel shows that between 03 and 13 September
2007, PIN and VPIN have a signiﬁcant movement characterized by a spike of both on the day
after the event. This manipulation inﬂuences PIN and VPIN on the EDU7 contract expiring
on September 19, 2007. The PIN increases from 0.68, then reaches a peak on September
09 at 0.80, falling to 0.695 on the following day. Also, VPIN20, VPIN50, VPIN100 and
VPIN200 increase from around 0.08 before the event to 0.17 on the event date, then reached
a peak at 0.29 one day after, as a nearly threefold increase. Finally, similar to the PIN, the
3CFTC, Order instituting proceedings pursuant to detection(c) and 6(d) of the commodity exchange
act, as amended, making ﬁndings and imposing remedial sanctions in the matter of Co¨operative Central
Raiﬀeisen Boerenleenbank B.A., p. 10.
41


### Page 42

Figure 7: The PIN and VPIN Around Identiﬁed LIBOR Manipulation.
Note A: The left panel of ﬁgure 7 presents historical PIN on the left axis with a blue line and VPIN on the right axis for the LIBOR
manipulation event, between March 28 and April 07, 2006. According to the CFTC document, Barclays’ traders attempted to manipulate
the US Dollar LIBOR on March 31, 2006, when Barclays’ employees, including senior Treasury managers requested the Barclays’ LIBOR
submitter to submit a higher US Dollar LIBOR rate than the normal rate.
Note B: The right panel of ﬁgure 7 presents the PIN on the left axis with a blue line and VPIN on the right axis for LIBOR manipulation
event between September 04 to 14, 2007. In this event, Rabobank’s US Dollar LIBOR traders asked their submitter on September 07,
2007 to keep a high LIBOR rate for the rest of that week.
42


### Page 43

VPIN drops to its previous level.
I ﬁnd PIN and VPIN have a systematic pattern around the LIBOR manipulation events
as they increase on the event date, reach a peak the day after, and ﬁnally decrease to the
previous level. However, it is interesting to note that normally all 40 Eurodollar futures
contracts trade within the same time frame. As a result, informed traders may manipulate
the ED in diﬀerent contracts. The limitation of this study is that I cannot identify speciﬁc
Eurodollar futures contract undertaken by speciﬁc banks as this information is not publicly
available. Hence, the appropriate way to study PIN and VPIN is to investigate via a term
structure and a term structure of variation.
Figure 8 presents the term structure of PIN (Top-Panel)and VPIN (Lower-Panel) for
-/+60 days around LIBOR manipulation dates. This ﬁgure presents the overlay 2,080 plots
of PIN and 8,320 plots of VPIN (dotted line) with average PIN and VPIN (thick black line),
and also presents 95% conﬁdence interval(black dashed line) into one plot to investigate
how the PIN and VPIN react to LIBOR manipulation. The top panel of Figure 8 illustrates
that the PIN has a 20% variation from 0.55 to 0.75. The cumulative diﬀerences of PIN or
cumulative ∆PIN has around a 50% variation of -0.02 to 0.50. However, the average PIN
only slightly varies with the highest on the event day from 0.68 to 0.64. The cumulative
average ∆PIN also has a small variation between 0.02 and 0.08 with the highest on the event
date.
The lower panel of Figure 8 presents the term structure of VPIN and cumulative ∆VPIN
with cross sectional average (thick line) across all events, all ED contracts and all types of
VPIN (dotted line). It can be seen that the VPIN has higher variation than the PIN. The
term structure of VPIN during the event has a minimum value of 0.02 and a maximum of
0.35 or around 35% variation. However, if I focus on the 95% conﬁdence interval, I ﬁnd
VPIN at around 12% variation, mostly moving between 0.10 to 0.20. The average VPIN
during LIBOR manipulation varies between 0.135 to 0.16 with the highest VPIN one day
43


### Page 44

Figure 8: The Term Structure of PIN, VPIN, Delta PIN and Delta VPIN for -/+60
days around identiﬁed LIBOR manipulation date.
Note: This ﬁgure presents the term structure of PIN and VPIN for -/+60 days around the
identiﬁed LIBOR manipulation date with the overlay 2,080 plots of PIN and 8,320 VPIN
presents on a dotted line, the average PIN and VPIN on a thick black line, and also 95%
conﬁdent interval on a black dashed line. It can be seen from this ﬁgure that the variation of
PIN and VPIN around the LIBOR manipulation event in the average daily value is slightly
ﬂuctuates.
For the upper panel, the average PIN slightly ﬂuctuates between the lowest at 0.65 and the
highest at 0.68. Also, the PIN increases on the event date, then peaks between one or two
days after the event date (day zero). Finally, the PIN drops to normal three days after the
event.
In the lower panel of ﬁgure 8 presents individual VPIN on a dotted line and average VPIN
on a thick black line. It can be seen that the average VPIN slightly ﬂuctuates between the
lowest at 0.13 and the highest at 0.18. Whilst the PIN is at a peak after the event, the
VPIN spiked on the event date then drops between two and three days after the event.
44


### Page 45

after event at 0.16 and the second highest on event day at 1.58. Finally, the average VPIN
drops to normal around three days after the event. One remarkable result is the variation
witnessed is lowest from the event date to two days later. This shows that during LIBOR
manipulation all types of VPIN have a similar pattern, as they rapidly increase on the event
date, remain high for two days then drop to normal.
The right subplot of the lower panel of Figure 8 presents the cumulative ∆VPIN. In
this plot, the cumulative ∆VPIN has variation between -0.5 to 0.5 with average value at
-0.0194. Also, the highest cross sectional average VPIN on the event day, at 0.07. This
increases around 10% compared with the average cumulative ∆VPIN. This result conﬁrms
that VPIN has more sensitivity to toxicity events, as the average VPIN and the average
cumulative ∆VPIN on the event date are higher than their average. In addition the ∆VPIN
is constantly high for at least two days after the event, then drops to normal.
Overall, Figure 8 demonstrates that PIN and VPIN are able to detect toxicity events
in the Eurodollar Futures market as they spike around the manipulation date. However,
Table 8 shows that the cross sectional average PIN and VPIN have no statistically signiﬁcant
diﬀerences around these events, both pre and post 2008. In the pre-2008 period, the highest
PIN appears for 60 days after the event and the lowest for 60 days before at 0.7069 and
0.6938 respectively. The highest VPIN in this period appears on VPIN50 for 30 days before
the event and the lowest is VPIN20 for 60 days before the event at 0.1713 and 0.0487
respectively. For the post 2008 period, the highest PIN appears for 60 days before and the
lowest for 60 days after the event at 0.6752 and 0.6663, respectively. The highest VPIN
is VPIN200 for 30 days and, on the contrary, is VPIN20 for 60 days at 0.1773 and 0.0722
respectively. This shows how PIN and VPIN can act partially as an early warning signal for
toxic events.
Table 9 below illustrates PIN and VPIN based on event dates both pre and post 2008.
In the case of pre 2008, the ﬁrst column shows that the PIN after day zero is higher than the
45


### Page 46

Table 8: PIN, VPIN20, VPIN50, VPIN100,and VPIN200 -/+ 60 days around LIBOR manipulation events date.
Informed trading around LIBOR manipulation events date
Days
PIN-Pre2008
VPIN - Pre 2008
PIN-Post2008
VPIN - Post 2008
20
50
100
200
20
50
100
200
-60
0.6938
0.0487
0.0600
0.0652
0.0722
0.6752
0.0490
0.0656
0.0815
0.0917
(0.0196)
(0.0584)
(0.0590)
(0.0505)
(0.0400)
(0.0089)
(0.0350)
(0.0356)
(0.0360)
(0.0329)
-30
0.6946
0.1625
0.1713
0.1188
0.0810
0.6724
0.1400
0.1691
0.1773
0.1896
(0.0237)
(0.0630)
(0.0633)
(0.0563)
(0.0413)
(0.0089)
(0.0297)
(0.0305)
(0.0285)
(0.0290)
-20
0.6957
0.0868
0.0972
0.1042
0.1193
0.6717
0.0925
0.1132
0.1192
0.1187
(0.0260)
(0.0662)
(0.0668)
(0.0566)
(0.0445)
(0.0088)
(0.0332)
(0.0337)
(0.0328)
(0.0325)
-10
0.6967
0.0493
0.0886
0.0648
0.0706
0.6731
0.0741
0.0993
0.1121
0.1259
(0.0287)
(0.0623)
(0.0627)
(0.0537)
(0.0412)
(0.0081)
(0.0338)
(0.0344)
(0.0336)
(0.0330)
0
0.6968
0.0500
0.0573
0.0673
0.0724
0.6732
0.0578
0.0786
0.0991
0.1174
(0.0325)
(0.0510)
(0.0627)
(0.0499)
(0.0375)
(0.0117)
(0.0332)
(0.0327)
(0.0326)
(0.0311)
10
0.6995
0.1396
0.0602
0.0814
0.0884
0.6738
0.1241
0.1447
0.1635
0.1781
(0.0324)
(0.0364)
(0.0500)
(0.0302)
(0.0303)
(0.0053)
(0.0290)
(0.0266)
(0.0259)
(0.0209)
20
0.7020
0.0570
0.1519
0.0712
0.0780
0.6686
0.0684
0.0947
0.1126
0.1314
(0.0318)
(0.0447)
(0.0376)
(0.0432)
(0.0451)
(0.0053)
(0.0290)
(0.0266)
(0.0250)
(0.0230)
30
0.7043
0.0549
0.0650
0.6590
0.0701
0.6671
0.0700
0.0997
0.1271
0.1483
(0.0322)
(0.0492)
(0.0457)
(0.0435)
(0.0397)
(0.0043)
(0.0281)
(0.0271)
(0.0252)
(0.0228)
60
0.7069
0.0911
0.0593
0.1263
0.1343
0.6663
0.0995
0.1128
0.1288
0.1389
(0.0350)
(0.0425)
(0.0412)
(0.0374)
(0.0338)
(0.0017)
0.0316
(0.0297)
(0.0288)
(0.0284)
Note: This table compares the average PIN, VPIN20, VPIN50, VPIN100, and VPIN200 including its standard deviation for -/+60, 30, 20 and 10 days around
the identiﬁed LIBOR manipulation event according to the CFTC and FSA documents from 1996 to the end of 2007, and from 2008 to the end of 2013. It can
be seen from this table, that there is a small scale of variation before and after events date for both PIN and VPIN. However, the variation for both parameters
for the ﬁrst sub period(Pre-2008) is higher than post-2008. Despite the fact that there is not a statistically signiﬁcant diﬀerence for PIN and VPIN, both , on
the event date, are high compared to ten days before the event.
46


### Page 47

previous period as the PIN is monotonically increasing from -0.0030 for sixty days before
the event and reaches a peak 60 days after, when the PIN is 0.0101 higher than the PIN on
event day. The second four columns present four diﬀerent types of VPIN in the same period
as PIN. Unlike the PIN, VPIN is not monotonically increasing. However, all four types of
VPIN increase after day zero then drop from three to ten days after the event. The highest
VPIN based on the event date is on VPIN20 for ten days after the event, at 0.0896 higher
than event day.
Post 2008, the PIN and VPIN have a similar pattern as they rapidly increase on the
event date and are constantly high for two to three days, then drop back to normal. The
highest PIN appears for ten days after the event at 0.0006, higher than the level on the event
date. However, the PIN in this period is lower than pre 2008. The highest VPIN based on
the event date appears for 30 days to maturity at 0.0822, 0.0905, 0.0782 and 0.0722, higher
than the event date, for VPIN20 follow by VPIN50, VPIN100 and VPIN200 respectively.
Both Table 8 and 9 demonstrate that the PIN is weaker than VPIN as a signal of market
manipulation post 2008. For example, the average VPIN ten days after the event is mostly
0.06 or 6% higher than the VPIN on the event date. This is compared to 0.0027 or 0.27% for
the PIN. However, overall there is no statistically signiﬁcant diﬀerence for PIN and VPIN
based on the event date around these events, for either pre or post 2008.
Despite the PIN and VPIN not strongly capturing the market manipulation for -/+ 60
days from the event date, focus on the variation of PIN and VPIN for -/+ 10 days, shows
evidence of market manipulation, as this toxicity event is short lived. In general, ten days
after the event PIN and VPIN are higher than their level on the event date. Especially in
the post 2008, all types of VPIN perform well compared to the PIN. Focus on variation of
PIN and VPIN based on the event date, gives us more information as PIN and VPIN for 10
days after the event are always higher than the level on the event date.
The results from table 8 and 9 suggest conclusively, the PIN and VPIN are sensitive to
47


### Page 48

Table 9: PIN, VPIN20, VPIN50, VPIN100,and VPIN200 based on events date -/+ 60 days around identiﬁed
LIBOR manipulation events.
Informed trading around LIBOR manipulation events date(based event date)
Day
PIN-Pre2008
VPIN - Pre 2008
PIN-Post2008
VPIN - Post 2008
20
50
100
200
20
50
100
200
-60
-0.0030
-0.0013
0.0027
-0.0021
-0.0002
0.0020
-0.0088
-0.0130
-0.0176
-0.0257
(0.0196)
(0.0584)
(0.0590)
(0.0505)
(0.0400)
(0.0089)
(0.0350)
(0.0356)
(0.0360)
(0.0329)
-30
-0.0022
0.1125
0.1140
0.0515
0.0086
-0.0008
0.0822
0.0905
0.0782
0.0722
(0.0237)
(0.0630)
(0.0633)
(0.0563)
(0.0413)
(0.0089)
(0.0297)
(0.0305)
(0.0285)
(0.0290)
-20
-0.0011
0.0368
0.0399
0.0369
0.0469
-0.0015
0.0347
0.0346
0.0201
0.0013
(0.0260)
(0.0662)
(0.0668)
(0.0566)
(0.0445)
(0.0088)
(0.0332)
(0.0337)
(0.0328)
(0.0325)
-10
-0.0001
-0.0007
0.0313
-0.0025
-0.0018
-0.0002
0.0163
0.0207
0.0130
0.0085
(0.0287)
(0.0623)
(0.0627)
(0.0537)
(0.0412)
(0.0081)
(0.0338)
(0.0344)
(0.0336)
(0.0330)
0
0
0
0
0
0
0
0
0
0
0
(0.0325)
(0.0510)
(0.0627)
(0.0499)
(0.0375)
(0.0117)
(0.0332)
(0.0327)
(0.0326)
(0.0311)
10
0.0027
0.0896
0.0029
0.0141
0.0160
0.0006
0.0663
0.0661
0.0644
0.0607
(0.0324)
(0.0364)
(0.0500)
(0.0302)
(0.0303)
(0.0053)
(0.0290)
(0.0266)
(0.0259)
(0.0209)
20
0.0052
0.0070
0.0946
0.0039
0.0056
-0.0046
0.0106
0.0161
0.0135
0.0140
(0.0318)
(0.0447)
(0.0376)
(0.0432)
(0.0451)
(0.0053)
(0.0290)
(0.0266)
(0.0250)
(0.0230)
30
0.0075
0.0049
0.0077
0.5917
-0.0023
-0.0061
0.0122
0.0211
0.0280
0.0309
(0.0322)
(0.0492)
(0.0457)
(0.0435)
(0.0397)
(0.0043)
(0.0281)
(0.0271)
(0.0252)
(0.0228)
60
0.0101
0.0411
0.0020
0.0590
0.0619
-0.0069
0.0417
0.0342
0.0297
0.0215
(0.0350)
(0.0425)
(0.0412)
(0.0374)
(0.0338)
(0.0017)
0.0316
(0.0297)
(0.0288)
(0.0284)
Note: This table presents PIN, VPIN20, VPIN50, VPIN100 and VPIN200 based on their value on the event date for -/+ 60, 30, 20, 10 days around the event.
The full data is separated into two parts: ﬁrstly, 1996 to the end of 2007 and secondly from 2008 to the end of 2013. Both PIN and VPIN based on its value on
the event date for all sub-periods is high after the event compared with the previous period. In this case, it can be assumed that the PIN and VPIN somewhat
detected some informed trading in the ED futures market on the LIBOR event, as these two parameters are high on the event date, then drops to normal.
Finally, the VPIN may have better performance than the PIN, it can be seen in this table that all types of VPIN show a higher positive variation then the PIN
on the event date. However, there is not a statistically signiﬁcantly diﬀerence for either based on their value on the event date for the whole period.
48


### Page 49

toxicity events or informed trading in the futures market, as both increase on the LIBOR
manipulation event date. However, these parameters still have limited ability to detect any
informed trading as the statistics show no signiﬁcant diﬀerence before and after the event
date for both pre and post 2008.
5.6. PIN, VPIN and the Maturity Eﬀect
This section contains an illustration of PIN and VPIN before and after expiration to
investigate the relationship between the indicators around the maturity date known as the
maturity eﬀect. The most striking result from this ﬁgure is an aggressive decline after the
spike of PIN and VPIN around the maturity date. Both gradually increase and reach a peak
within one week of the last trading day. When the ED starts trading again, they continuously
decrease to a lower level, although increase later. However, there is some variation between
PIN and VPIN, the VPIN continually decreasing over a longer period than the PIN, and
ﬁnally slightly increasing around thirty days after the event when the ED begins trading
again.
Figure 9 presents the performance of PIN and VPIN around the maturity date. In this
event, I use the EDH0 contract which has expiration on March 17,2010 as an example. This
ﬁgure is separated into four subplots, ﬁrst, PIN and VPIN: second, delta PIN and VPIN:
third, PIN and VPIN(based on event date) +/-7 days from maturity date: ﬁnally PIN and
VPIN(based on event date) +/-30 days from maturity date.
On the top panel of the left column, the PIN is seen on the left axis and VPIN on the
right for -/+7 days around expiration. There is similar variation between both as the two
measurements increase before the maturity date then decrease during the ﬁve trading days
before expiration. Finally, they bounce back. The highest PIN in this contract appears
on March 15, 2010 which is two days to maturity at a value of 0.82 then rapidly decreases
to 0.70 on the last trading day. After EDH0 starts trading on the following day, the PIN
continuously decreases to around 0.50 and stays constantly low, then ﬁnally bounces back
49


### Page 50

Figure 9: The historical PIN and VPIN of EDH0 with the expiry date.
Note: This ﬁgure presents an example of PIN, VPIN, ∆PIN, and ∆VPIN for the EDH0
futures contract. It can be seen from the top left panel that the PIN and the VPIN increase
before the maturity date, then rapidly drop around two to three days before the last trading
day. Finally, the PIN and VPIN bounce back to normal after the expiration when EDH0
starts trading again on the following day. The top right panel presents ∆PIN and ∆VPIN.
This sub-ﬁgure illustrates that the diﬀerences of VPIN are higher than thatof PIN. A high
level of ∆VPIN assumes that the VPIN has a higher degree of sensitivity to this toxicity
event than the PIN. The lower panel presents PIN and VPIN based on their value on the
event date for -/+7 and 30 days from the maturity date. Both show a strong variation
around this event compared to its value on the LIBOR event. Clearly, there is a signiﬁcant
pattern as the PIN and VPIN increase, then reach a peak within the last week of the trading
period, and dropping to normal the following day.
50


### Page 51

ﬁve day later. Moreover, VPIN is somewhat similar to PIN, the highest VPIN appears
around two to three days before expiry at 0.25 then decreases to 0.125 on the last trading
day with the lowest at 0.025 between one to two days after the ED starts trading again, and
ﬁnally bounces back.
The top panel of the right column presents the diﬀerences between PIN and VPIN or
∆PIN and ∆VPIN for -/+7 days around the maturity date. Despite, ∆PIN and ∆VPIN
having a similar pattern, the ∆VPIN has better performance as it has higher variation than
PIN. This subplot shows the latter has a small drop of around 10% as the ∆PIN slides from
0 to -0.02 then bounces back to normal on the following day. However, the VPIN drops
around one and a half times within seven days compared to the previous period, as the
∆VPIN falls from 0 to -1.5, then rebounds to a level around two times higher than its lowest
point. Additionally, the lower panel of Figure 9 presents PIN and VPIN based on the event
date for -/+7 and -/+30 days around the event date. Similar to the upper panel, there are
similar patterns for both PIN and VPIN. The VPIN performs better than PIN as a signal
of market manipulation, however, the PIN shows a higher variation for the manipulation
event.
To gain further insight into the eﬀect of maturity date on PIN and VPIN, both have
been investigated for a longer period. Figure 10 illustrates cross sectional averages across
all 40 ED contracts on PIN and VPIN for -/+30 and -/+60 days around the expiry date.
Overall, there is a similar pattern to Figure 9. The PIN and the VPIN reach a peak within
the last week of the trading period, then drop. Finally, PIN and VPIN bounce back to
normal after the last trading day when the ED starts trading again. It can be seen from the
top left panel of Figure 10 that from ten days to maturity, the average PIN increases from
0.67 to 0.725 then drops to 0.70 around two days after the last trading day. Also, similar to
the PIN, the VPIN increases from 0.07 to around 0.10 three days before the maturity date,
then drops to 0.06 two days after. Finally, the VPIN slightly increases to a normal level.
51


### Page 52

Figure 10: The cross-sectional PIN, VPIN, ∆PIN and ∆VPIN across all 40 ED
futures contracts with the expiry date.
Note: This ﬁgure presents cross sectional average PIN, VPIN, ∆PIN and ∆VPIN across all 40 ED futures
contracts around the expiry date. The red solid vertical line indicates the last trading day on the ED futures
contracts. The top left panel presents PIN and four diﬀerent types of VPIN for -/+30 days around maturity
date. During the last week of the trading period, the PIN gradually increases then drops around two to
three days until the last trading day. Finally, the PIN and VPIN bounce back. There is a signiﬁcant pattern
between these two parameters. However, the VPIN shows a slightly diﬀerent pattern from the PIN, as it
gradually increases for 30 days before the last trading day, reaching a peak within the last week before the
maturity date. The PIN rapidly increases from eleven days to maturity then peaks around two to three days
to maturity. Finally, both bounce back after the last trading day when the ED commences trading again.
The top right panel presents the diﬀerences of PIN and the diﬀerences of VPIN (∆PIN and ∆VPIN). This
ﬁgure shows a higher degree of diﬀerence on the VPIN(∆VPIN) than the ∆PIN. In this case, I can assume
that the VPIN has more sensitivity than the PIN on this event. The lower panel presents PIN and VPIN
based on the event date for -/+30 and -/60 days from maturity date. These two plots show a similar result
as the top panel. There is a systematic trend between PIN and VPIN based on their value on the event
date and the latter is more sensitive to this event than the PIN.
52


### Page 53

Top right panel of Figure 10 presents the diﬀerences of PIN and VPIN or ∆PIN and
∆VPIN for -/+30 days around the maturity date. In this period the ∆VPIN has higher
variation than ∆PIN. The ∆PIN ﬂuctuates between -0.01 and 0.01, however, the ∆VPIN
ﬂuctuates around 40% between -0.25 and 0.15. The highest ∆VPIN appears on the seven
days before the last trading day at 0.15, then gradually drops to the bottom on the expiry
date at -0.25. Finally, the VPIN bounces back to normal. Additionally, from seven days to
maturity ∆VPIN increases around 25%, from -0.1 to 0.15. Whilst these two parameters have
slightly diﬀerent variation before the maturity date, they have a similar pattern. The ∆PIN
and ∆VPIN reach a peak within the last week of the trading period, then rapidly decrease,
and ﬁnally bounce back after the last trading day when the ED futures start trading the
following day.
The lower panel of Figure 10 presents PIN and VPIN based on the PIN and the VIN
on the event date for +/- 30 and +/-60 days around maturity date.
These sub-ﬁgures
show a similar pattern PIN and VPIN based on the event date and normal PIN and VPIN.
Additionally, there is a similar trend between both types . The VPIN is constantly high sixty
days before expiry, then reaches a peak at around seven days before expiration, as the VPIN
based on the event date shows a positive result before the last trading day. However, later
between two to three days to the expiration, PIN and VPIN gradually decrease continuously
dropping after the last trading day. Finally, there is a move back to normality. However,
the PIN based on its value on the event date shows a somewhat negative value from 60 to
5 days to maturity. However, they reach a peak within one week before the maturity date,
then rapidly drop.
The following section presents the result of the term structure of PIN and VPIN on
the maturity eﬀect as presented for the LIBOR manipulation events. Figure 11 presents
the term structure of PIN and VPIN, also cumulative ∆PIN and cumulative ∆VPIN for
the maturity eﬀect. The ﬁgure presents individual PIN, VPIN20, VPIN50, VPIN100, and
53


### Page 54

VPIN200 as a dotted line and average PIN and VPIN as a thick line. It also presents 95%
range as a 95% conﬁdent interval as a thick dotted line. Overall, I present 40 PIN and 200
VPIN for the term structure.
The top panels of Figure 11 present cross-sectionals of PIN and cumulative ∆PIN. Over-
all, there is a small variation on average PIN around the maturity date with a small spike
about three days to expiration. This spike has a variation of 2% higher than the average.
Despite there being a small scale of variation on average PIN before the maturity date, the
individual PIN has a higher variation after the last trading day. The major trend of PIN
(dotted lines) is constantly moving around the identical PIN at about 0.67 (thick line) with
a small spike and there is the widest variation of PIN at three days to expiration. The lowest
PIN is 0.2 and the highest is 0.995, which is nearly 80% variation.
However, after three days to expiration the variation of PIN drops to 50%, with the
highest recording at 0.97 and the lowest around 0.30. The variation is wider at the beginning
than the previous trading period, this may be consistent with the term structure of PIN
(ﬁgure 4) as it has a high variation from the ﬁrst trading day; then the variation becomes
narrow when the ED futures are nearer to maturity.
The lower panel of Figure 11 illustrates VPIN and cumulative of ∆VPIN for -/+60 days
from the maturity date across all 40 ED futures contracts. This panel presents not only forty
individual VPIN and forty cumulative ∆VPIN from all ED contracts, but each contract also
calculates four diﬀerent types of VPIN and cumulative ∆VPIN presented on a dotted line
with the average value in a thick line, and 95% conﬁdent interval in a thick dotted line.
It can be seen from this ﬁgure that there is quite naturally the same pattern of average
of VPIN with the PIN. The average VPIN gradually increases from 60 days from the last
trading days and reaches a peak at around two days to maturity, then rapidly drops. Finally,
the VPIN increases to a normal level after the expiration when the ED start trading again.
Also, there is a lower scale of variation on VPIN than PIN, which is notably smaller and
54


### Page 55

Figure 11: The variation of PIN and VPIN -/+60 days around maturity date
Note: This ﬁgure presents the term structure of PIN, VPIN, cumulative of ∆PIN and
cumulative of ∆VPIN with their average value for -/+60 days around maturity date. Overall,
there is a systematic pattern between the average PIN and VPIN around this event, as these
parameters show a spike on two days to maturity then rapidly drop on the last trading day.
Finally, these two parameters bounce back after the last trading day when the ED futures
start trading again. However, the lower panel shows that all types of VPIN have a higher
scale of variation than the PIN for both before and after the maturity date.
55


### Page 56

more systematic than the PIN. The lowest VPIN is near to zero and the highest is about
0.8, with the average upper bound at about 0.2.
In comparison, the average PIN has a small variation around 0.67 and the average cu-
mulative ∆PIN is near to zero. However, the average VPIN gradually increases from 0.05
to just above 0.20 and the average cumulative ∆VPIN increases from just around zero to
one on two days to the maturity date. Finally, VPIN and cumulative ∆VPIN plunges to
nearly zero on the last trading day. The average VPIN and the average cumulative ∆VPIN
reaches a peak on two days to expiration which increases by around twofold, compared to
the previous period. the average VPIN has a higher variation than the PIN and there is
a systematic trend between diﬀerent VPINs. One ﬁnal concluding remark is that the term
structure of ∆VPIN tends to be a ‘sine curve’.
After studying PIN and VPIN via the term structure around the maturity date, I then
investigate these two parameters from their standard deviation(SD). Table 10 reports cross
sectional average PIN and VPIN across all 40 ED contracts, constructed for 60, 30, 20 and
10 days for ﬁxed time windows around the maturity dates with their SD. Then, the result
of these two parameters is divided into two sub-periods. The ﬁrst sub-period is between
January 1, 1996 and December 31, 2007 and the second sub-period is between January
1, 2008 until December 31, 2013. Moreover, this time period is separated into two parts
because there will be diﬀerent results for PIN and VPIN between these two periods as there
is the break in the relationship of the bank rank of LIBOR quotes after 2008.
Overall, the variation of PIN is lower than VPIN for both periods as its standard de-
viation is smaller than the VPIN. However, there is a similar pattern between these two
parameters. They both increase before the last trading day, then rapidly drop. Finally,
they bounce back after the last trading day when the ED futures starts trading again. The
lowest PIN appears on the last trading day (Day 0) at 0.6695 and 0.6552 for pre 2008 and
post 2008 samples respectively. The highest appears for 20 and 60 days after the maturity
56


### Page 57

date for pre-2008 and post-2008 respectively. For the VPIN, the lowest appears on VPIN20
for both pre and post 2008, at 0.0471 and 0.0309 respectively. The highest VPIN mostly
appears for thirty days to maturity for all diﬀerent types of VPIN, with the highest of 0.1639
on VPIN200 for pre 2008. This table indicates that there is a similar trend for PIN and
VPIN for both periods, however, their variation and standard deviation (SD) are diﬀerent.
Pre 2008, the SD on PIN and VPIN are slightly diﬀerent. The SD on PIN shows that
the PIN is not statistically signiﬁcantly diﬀerent, as the SD varies between 0.02 to 0.05.
However, the SD on VPIN during this period is slightly higher than PIN. The highest SD
for 10 days after the maturity date is 0.088, 0.089, 0.095 and 0.099 for VPIN20, VPIN50,
VPIN100 and VPIN200 respectively. Post 2008, the highest SD for PIN is 0.055 for 60 days
after the maturity date. However, the highest SD for VPIN is for 30 days to maturity at
0.108, 0.0833 and 0.085 for VPIN20, VPIN100 and VPIN200 respectively. The highest SD
for VPIN20 is 0.127 for ten days to maturity which is the highest SD for all types of VPIN.
Finally, there are two remarkable results from this table; ﬁrst the maturity eﬀect tends to
have an impact on informed trading as the PIN and VPIN have shown a similar pattern.
They slightly increase for 60 days to maturity, then fall to the lowest PIN and VPIN on the
last trading day. Next, the smallest VPIN on this event for both the pre 2008 and post 2008
period, is VPIN20 followed by VPIN50, VPIN100 and VPIN200.
Next, I analyze PIN and VPIN based on their value on the event date for -/+60 days
around the maturity which is presented in Table 11. The results indicate that the PIN and
VPIN around the maturity date are higher than the those on regular trading days. Using
the same format analysis as Table 10, I ﬁnd the same result. First, the VPIN has a greater
magnitude of variation than the PIN for both pre and post 2008. Secondly, the PIN and
VPIN gradually increase for 60 days to maturity then peak within ﬁve trading days. After
three to two days to maturity, they rapidly drop and ﬁnally bounce back. On pre-2008,
the highest PIN is for ten and twenty days after the maturity date at 0.0283 or 2.83%,
57


### Page 58

Table 10: PIN, VPIN20, VPIN50, VPIN50, VPIN100, and VPIN200 -/+ 60 days around maturity date.
Informed trading around maturity date
Days
PIN -Pre 2008
VPIN - Pre 2008
PIN - Post 2008
VPIN - Post 2008
20
50
100
200
20
50
100
200
-60
0.6926
0.1104
0.1238
0.1335
0.1423
0.6933
0.0753
0.0797
0.0809
0.0841
(0.0223)
(0.0851)
(0.0785)
(0.0734)
(0.0721)
(0.0324)
(0.0924)
(0.0858)
(0.0764)
(0.0754)
-30
0.6933
0.1207
0.1396
0.1488
0.1639
0.6975
0.0911
0.0937
0.0968
0.1027
(0.0278)
(0.0881)
(0.0817)
(0.0714)
(0.0775)
(0.0400)
(0.1088)
(0.0953)
(0.0833)
(0.0850)
-20
0.6926
0.1208
0.1368
0.1459
0.1564
0.6999
0.0833
0.0859
0.0873
0.0924
(0.0313)
0.0903
(0.0836)
(0.0752)
(0.0751)
(0.0433)
(0.1001)
(0.0875)
(0.0758)
(0.0774)
-10
0.6930
0.1126
0.1285
0.1375
0.1466
0.7006
0.0749
0.0783
0.0793
0.0839
(0.0354)
(0.0853)
(0.0796)
(0.0721)
(0.0720)
(0.0459)
(0.0920)
(0.1276)
(0.0699)
(0.0715)
0
0.6695
0.0471
0.0591
0.0724
0.0827
0.6552
0.0309
0.0384
0.0417
0.0444
(0.0368)
(0.0734)
(0.0682)
(0.0662)
(0.0639)
(0.4656)
(0.0767)
(0.0726)
(0.0626)
(0.0616)
10
0.6978
0.1012
0.1176
0.1323
0.1397
0.7066
0.0497
0.0532
0.0531
0.0576
(0.0420)
(0.0888)
(0.0892)
(0.0965)
(0.0998)
(0.0448)
(0.0641)
(0.0586)
(0.0484)
(0.0568)
20
0.6979
0.0981
0.1105
0.1222
0.1279
0.7097
0.0427
0.0473
0.0482
0.0507
(0.0466)
(0.0727)
(0.0740)
(0.0764)
(0.0750)
(0.0477)
(0.0469)
(0.0341)
(0.0359)
(0.0413)
30
0.6970
0.0931
0.1049
0.1170
0.1223
0.7116
0.0501
0.0556
0.0563
0.0572
(0.0488)
(0.0665)
(0.0666)
(0.0700)
(0.0658)
(0.0501)
(0.0522)
(0.0517)
(0.0471)
(0.0489)
60
0.6891
0.0981
0.1106
0.1210
0.1262
0.7157
0.0518
0.0580
0.0574
0.0591
(0.0530)
(0.0593)
(0.0558)
(0.0578)
(0.0537)
(0.0550)
(0.0546)
(0.0547)
(0.0417)
(0.0401)
Note: This table compares average PIN, VPIN20, VPIN50, VPIN100, and VPIN200, with their standard deviation for -/+60, 30, 20 and 10 days from maturity
date. The time period is separated into two periods: the ﬁrst sub-period is from 1996 to the end of 2007 and the second from 2008 to the end of 2013. Overall,
there is small scale variation for both PIN and all types of VPIN before and after the event dates. However, their standard deviation pre-2008 are higher than
post-2008. Additionally, VPIN has a higher standard deviation than PIN. It can be assumed that VPIN is more sensitive to the maturity eﬀect than PIN, as
it increases before the last trading day then drops dramatically by over 50% on the last day. Finally, there is a similar pattern between these two parameters.
However, neither are statistically signiﬁcantly diﬀerent during the LIBOR manipulation event, as their standard deviation varies between 0.02 to 0.09.
58


### Page 59

Table 11: The PIN, VPIN20, VPIN50, VPIN50, VPIN100, and VPIN200 based events date -/+ 60days around
maturity date.
Informed trading around maturity date
Days
PIN -Pre 2008
VPIN - Pre 2008
PIN - Post 2008
VPIN - Post 2008
20
50
100
200
20
50
100
200
-60
0.0231
0.0633
0.0647
0.0611
0.0596
0.0381
0.0444
0.0413
0.0392
0.0397
(0.0223)
(0.0851)
(0.0785)
(0.0734)
(0.0721)
(0.0324)
(0.0924)
(0.0858)
(0.0764)
(0.0754)
-30
0.0238
0.0736
0.0805
0.0764
0.0812
0.0422
0.0602
0.0553
0.0551
0.0583
(0.0278)
(0.0881)
(0.0817)
(0.0714)
(0.0775)
(0.0400)
(0.1088)
(0.0953)
(0.0833)
(0.0850)
-20
0.0231
0.0737
0.0777
0.0735
0.0737
0.0447
0.0524
0.0475
0.0456
0.0480
(0.0313)
(0.0903)
(0.0836)
(0.0752)
(0.0751)
(0.0433)
(0.1001)
(0.0875)
(0.0758)
(0.0774)
-10
0.0235
0.0655
0.0694
0.0651
0.0639
0.0454
0.0440
0.0399
0.0376
0.0395
(0.0354)
(0.0853)
(0.0796)
(0.0721)
(0.0720)
(0.0459)
(0.0920)
(0.1276)
(0.0699)
(0.0715)
0
0
0
0
0
0
0
0
0
0
0
10
0.0283
0.0541
0.0585
0.0599
0.0570
0.0514
0.0188
0.0148
0.0114
0.0132
(0.0420)
(0.0888)
(0.0892)
(0.0965)
(0.0998)
(0.0448)
(0.0641)
(0.0586)
(0.0484)
(0.0568)
20
0.0283
0.0510
0.0514
0.0498
0.0452
0.0545
0.0118
0.0089
0.0065
0.0063
(0.0466)
(0.0727)
(0.0740)
(0.0764)
(0.0750)
(0.0477)
(0.0469)
(0.0341)
(0.0359)
(0.0413)
30
0.0275
0.0460
0.0458
0.0446
0.0396
0.0564
0.0192
0.0172
0.0146
0.0128
(0.0488)
(0.0665)
(0.0666)
(0.0700)
(0.0658)
(0.0501)
(0.0522)
(0.0517)
(0.0471)
(0.0489)
60
0.0196
0.0510
0.0515
0.0486
0.0435
0.0605
0.0209
0.0196
0.0157
0.0147
(0.0530)
(0.0593)
(0.0558)
(0.0578)
(0.0537)
(0.0550)
(0.0546)
(0.0547)
(0.0417)
(0.0401)
Note: This table presents a comparison of average PIN, VPIN20, VPIN50, VPIN100, VPIN200 based on their value on the event date, and also standard
deviation (SD) for -/+60, 30, 20 and 10 days from the maturity date. The time period is separated into two periods: the ﬁrst sub period from 1996 to the
end of 2007 and the second is from 2008 to the end of 2013. Overall, there is a similar result to Table 10 - a small scale variation before and after the event
dates for both PIN and VPIN. Despite the variation of VPIN being higher for the ﬁrst pre-2008 period, the variation of PIN for post-2008 is higher than
pre-2008. Nevertheless, there is a systematic trend between these two parameters as the PIN and all types of VPIN increase before the last trading day then
drop dramatically more than 50% on the last day. Finally, they increase to the normal level.
59


### Page 60

higher than the PIN on the maturity date. Moreover, the highest VPIN based on the VPIN
on the event date appears for thirty and twenty days before the maturity date, at 0.0737,
0.0805, 0.0764 and 0.0812 for VPIN20, VPIN50, VPIN 100 and VPIN200 respectively. For
the second sub period, the highest PIN based on the PIN on the event date is for sixty
days after the expiration at 0.605 or 6% higher than that on the expiry date. Similar to
the ﬁrst period, the highest VPIN appears for thirty and twenty days before the maturity
date at 0.0602, 0.0553, 0.0551 and 0.0583 for VPIN20, VPIN50, VPIN 100 and VPIN200
respectively.
Conclusively, I ﬁnd the VPIN has a higher scale of variation than PIN except after the
maturity date for the second sub period. For the ﬁrst sub period, the average PIN for sixty
days before the maturity date is at 0.023 or 2.3% higher than the last trading day. The
average VPIN from sixty days to maturity is at 0.07 or 7% higher than the VPIN on the
last trading day, which is around three times higher when compared to the PIN. The clear
indication is that both have a similar pattern around the maturity event as they increase
then reach a peak before it. Finally, they continuously drop after the last trading day when
the ED starts trading again, before bouncing back to normal. Also, the results are in the
line with the evidence, as described in the previous analysis section, that the VPIN has more
predictability for truly toxicity events than the PIN.
6. Conclusion
This paper takes a comprehensive dataset of the Chicago Mercantile Exchange (CME)
tape data, which covers every inside quote and trade from 1996 to 2015 for the 40 LIBOR
referenced, quarterly dated Eurodollar futures contracts. First, I apply diﬀerent types of
PIN and VPIN metrics over a variety of estimation windows. I have undertaken an empirical
microstructure model of Easley and O’Hara (1992) and Easley et al. (1996) for the PIN and
Easley et al. (2011) and Easley et al. (2012) for VPIN. I then have constructed a variety of
60


### Page 61

tests to see if the pattern of PIN and VPIN exhibit structural changes around documented
cases of manipulation of the LIBOR reference rate and the maturity event. Finally, I compare
this to systematic ﬂuctuations in these measures relative to the futures term structure.
Unsurprisingly, given the scale of the task, therefore, the results are very mixed. Both
PIN and VPIN vary systematically and in a statistically signiﬁcant pattern in respect to the
term structure of the futures contracts. PIN varies in a v-shaped pattern, with long (2000
to 3500 days) and short maturity (0 to 500 days) contracts, having signiﬁcantly higher PIN
than intermediate contracts (which are actually the most heavily traded). However, VPIN
tends to be a v-shaped pattern from 900 days to maturity to the last trading day. Similar to
the PIN, the VPIN on long and short maturity contracts, has signiﬁcantly higher PIN than
intermediate contracts. The former is substantially lower than the latter over the entire range
of calculation measures. However, when I move to documented cases of market manipulation
in the LIBOR reference rate, the results are ambiguous. There are deﬁnitive examples when
the PIN and the VPIN shift systematically around a relevant, documented case of a LIBOR
manipulation. However, when I build cross sectional averages across events, there is no
signiﬁcant evidence of systematic shifts in either the PIN or VPIN metric. It should be
noted that whilst I have included every documented case of manipulation directly linked to
the relevant reference rates, the list is necessarily incomplete as the regulatory actions have
tended to focus on sample charges to the ﬁrms involved, rather than documenting every
occurrence and its motivation. These ﬁndings clearly show that, consistent with Andersen
and Bondarenko (2014a) Abad et al. (2015), the PIN and VPIN have less predicting power
as an early signal warning on market manipulation.
The investigation extends to the maturity eﬀect. The results are remarkable and show
PIN and VPIN have a signiﬁcant pattern around this event. They reach a peak at three days
to maturity, then drop within the last week of the trading period. Finally, both gradually
increase to a normal level after the ED starts trading again.
61


### Page 62

Another remarkable result in this study is that the cumulative of ∆PIN and the cu-
mulative of ∆VPIN show a clear pattern on the event study, as they spike on the toxicity
manipulation event. In line with Easley et al. (2012), the results also show that the cumula-
tive value of ∆VPIN performs better than the normal value in providing information about
toxicity events. Therefore, I also apply this method to the PIN. The cumulative of ∆PIN
and the cumulative of ∆VPIN show a clear pattern on the event study, as they spike on
LIBOR manipulation dates, which are higher than the spike on the normal PIN and VPIN.
Finally, despite VPIN having a higher deviation than PIN and their cumulative diﬀer-
ences performing better than the normal value to capture these toxicity events, they are not
signiﬁcantly statistically diﬀerent for both the LIBOR manipulation and the maturity event.
The results may be because the PIN and VPIN approach is unsuitable or because it may
have been used incorrectly for this type of data. Alternatively, the LIBOR manipulation and
expiration may have only a minor eﬀect. However, I leave full investigation of this issue to
future work, as more ﬁne detail emerges from the current round of court cases and provides
more direct evidence of channels of informed trading.
References
Abad, D., M. Massot, and R. Pascual (2015). Evaluating vpin as a trigger for single-stock circuit breakers.
Available at SSRN 2584346.
Abad, D. and J. Yag¨ue (2012). From pin to vpin: An introduction to order ﬂow toxicity. The Spanish
Review of Financial Economics 10(2), 74–83.
Admati, A. R. (1985). A noisy rational expectations equilibrium for multi-asset securities markets. Econo-
metrica 53(3), pp. 629–658.
Admati, A. R. and P. Pﬂeiderer (1988). A theory of intraday patterns: Volume and price variability. The
Review of Financial Studies 1(1), pp. 3–40.
Aitken, M. J., A. Frino, A. M. Hill, and E. Jarnecic (2004).
The impact of electronic trading on bid-
ask spreads: Evidence from futures markets in hong kong, london, and sydney.
Journal of Futures
Markets 24(7), 675–696.
Andersen, T. and O. Bondarenko (2013). Assessing vpin measurement of order ﬂow toxicity via perfect
trade classiﬁcation. Available at SSRN 2292602.
Andersen, T. G. and O. Bondarenko (2014a). Assessing measures of order ﬂow toxicity and early warning
signals for market turbulence. Review of Finance, Forthcoming.
Andersen, T. G. and O. Bondarenko (2014b). Reﬂecting on the vpin dispute. Journal of Financial Mar-
kets 17, 53–64.
Andersen, T. G. and O. Bondarenko (2014c). Vpin and the ﬂash crash. Journal of Financial Markets 17,
1–46.
62


### Page 63

Ates, A. and G. H. Wang (2005). Information transmission in electronic versus open-outcry trading systems:
An analysis of us equity index futures markets. Journal of Futures Markets 25(7), 679–715.
Ballocchi, G., M. Dacorogna, R. Gen¸cay, and B. Piccinato (2001). Time-to-expiry seasonalities in eurofu-
tures. Studies in Nonlinear Dynamics & Econometrics 4(4).
Boehmer, E., J. Grammig, and E. Theissen (2007). Estimating the probability of informed tradingdoes
trade misclassiﬁcation matter? Journal of Financial Markets 10(1), 26–47.
Easley, D., M. L. De Prado, and M. OHara (2011). The microstructure of the ﬂash crash: Flow toxicity,
liquidity crashes and the probability of informed trading. Journal of Portfolio Management 37(2), 118–
128.
Easley, D., M. M. L. de Prado, and M. O’Hara (2012). Flow toxicity and liquidity in a high-frequency world.
Review of Financial Studies 25(5), 1457–1493.
Easley, D., M. M. L. de Prado, and M. O’Hara (2014). Vpin and the ﬂash crash: A rejoinder. Journal of
Financial Markets 17(0), 47 – 52.
Easley, D., N. M. Kiefer, M. O’Hara, and J. B. Paperman (1996). Liquidity, information, and infrequently
traded stocks. The Journal of Finance 51(4), pp. 1405–1436.
Easley, D. and M. O’Hara (1992). Time and the process of security price adjustment. The Journal of
ﬁnance 47(2), 577–605.
Glosten, L. R. and P. R. Milgrom (1985).
Bid, ask and transaction prices in a specialist market with
heterogeneously informed traders. Journal of Financial Economics 14(1), 71 – 100.
Grossman, S. J. and J. E. Stiglitz (1980). On the impossibility of informationally eﬃcient markets. The
American Economic Review 70(3), pp. 393–408.
Hasbrouck, J. (1991). Measuring the information content of stock trades. The Journal of Finance 46(1),
179–207.
Hellwig, M. F. (1980). On the aggregation of information in competitive markets. Journal of Economic
Theory 22(3), 477 – 498.
Idier, J. and S. Nardelli (2011). Probability of informed trading on the euro overnight market rate. Inter-
national Journal of Finance & Economics 16(2), 131–145.
Karyampas, D. and P. Paiardini (2011). Probability of informed trading and volatility for an etf.
Ke, W.-C. (2014). The sensitivity to trade classiﬁcation algorithms for estimating the probability of informed
trading. International Journal of Trade, Economics and Finance 5(5).
Kim, C. W., T. T. Perry, and M. Dhatt (2014). Informed trading and price discovery around the clock. The
Journal of Alternative Investments 17(2), 68–81.
Kyle, A. S. (1985). Continuous auctions and insider trading. Econometrica 53(6), 1315–1335.
Lee, C. and M. J. Ready (1991). Inferring trade direction from intraday data. The Journal of Finance 46(2),
733–746.
Shah, S. and B. W. Brorsen (2011). Electronic vs. open outcry: Side-by-side trading of kcbt wheat futures.
Journal of Agricultural and Resource Economics 36(1).
Tse, Y. and T. V. Zabotina (2001). Transaction costs and market quality: Open outcry versus electronic
trading. Journal of Futures Markets 21(8), 713–735.
Yan, Y. and S. Zhang (2012). An improved estimation method and empirical properties of the probability
of informed trading. Journal of Banking & Finance 36(2), 454–467.
Yan, Y. and S. Zhang (2014). Quality of pin estimates and the pin-return relationship. Journal of Banking
& Finance 43, 137–149.
63

# Adverse Selection in Cryptocurrency Markets

- **Source File**: `ssrn-4175306.pdf`
- **Total Pages**: 49
- **SSRN ID**: `ssrn-4175306`

---


### Page 1

Adverse Selection in Cryptocurrency Markets
Murat Tiniç∗
Ahmet Sensoy†‡
Erdinc Akyildirim§¶
Shaen Corbet‖∗∗
July 28, 2022
Abstract
This paper investigates the influence that information asymmetry may possess upon the
future volatility, liquidity, market toxicity and returns within cryptocurrency markets. We use
the adverse selection component of the effective spread as a proxy for overall information asym-
metry. Using order and trade data from the Bitfinex Exchange, we first document statistically
significant adverse selection costs for major cryptocurrencies. Our results also suggest that ad-
verse selection costs, on average, correspond to ten percent of the estimated effective spread,
indicating an economically significant impact of adverse selection risk on transaction costs in
cryptocurrency markets. We finally document that adverse selection costs are important pre-
dictors of intraday volatility, liquidity, market toxicity, and returns.
Keywords: Cryptocurrencies; Market Microstructure; Adverse Selection; Informed Trading.
JEL: G12, G14, G15, C51
∗Kadir Has University, Department of International Trade and Finance, Kadir Has Caddesi, 34083 Fatih Istanbul,
Turkey. Email: murat.tinic@khas.edu.tr
†Corresponding author. Bilkent University, Faculty of Business Administration, Cankaya 06800, Ankara, Turkey.
Phone:+90 3122902048, email:ahmet.sensoy@bilkent.edu.tr. Ahmet Sensoy gratefully acknowledges support from the
Turkish Academy of Sciences - Outstanding Young Scientists Award Program (TUBA-GEBIP).
‡Adnan Kassar School of Business, Lebanese American University, Beirut, Lebanon.
§Department of Management, Bogazici University, Istanbul, Turkey. Email: erdinc.akyildirim@boun.edu.tr
¶University of Zurich, Department of Banking and Finance, Zurich, Switzerland.
‖DCU Business School, Dublin City University, Dublin 9, Ireland. Email: shaen.corbet@dcu.ie
∗∗School of Accounting, Finance and Economics, University of Waikato, New Zealand.
1


### Page 2

1
Introduction
The notion of fundamental value for cryptocurrencies can be considered to be very different from
other financial assets such as stocks or fiat currencies. Cryptocurrencies have been found to provide
transactional benefits that money issued by central banks does not (Biais et al., 2020). For example,
cryptocurrencies may provide a platform to allow for the completion of transactions even when
some centralised currencies or banking systems face significant problems, while cryptocurrencies
can also provide flexibility to investors when transferring funds from one country to another, even
considering the presence of closed economies. Cryptocurrencies also lead to transaction costs in
the form of limited convertibility, a lower rate of acceptance, and fees embedded within the mining
process (Biais et al., 2020)1. The theoretical framework presented in Biais et al. (2020) indicates
the existence of a feedback loop from future prices to transactional benefits and current prices;
where investors who expect future prices to be high, anticipate elevated transactional benefits,
which results in high prices today. Biais et al. (2020) underline that the fundamental value of a
cryptocurrency is, therefore, a function of net transactional benefits that depend on its future price.
In practice, those with internal knowledge with regards to the technological processes surrounding
both cryptocurrency creation and the mining process may better assess net transactional benefits
and, therefore, could possess an informational advantage when attempting to understand the funda-
mental value of the associated product. Therefore, investors who lack sufficient knowledge about the
underlying cryptocurrency product might face significant adverse selection problems. Such issues
can also arise for both retail and institutional investors of cryptocurrency. Institutional investors,
who are traditionally considered to be informed because of their ability to monitor market con-
ditions and process information at lower costs (Seppi, 1992; Hessel and Norman, 1992; Lang and
McNichols, 1997), have become increasingly prevalent in cryptocurrency markets in recent years
(Borri, 2019)2. While earlier attempts by Momtaz (2020) and Chod and Lyandres (2020) focus
on information asymmetry at the initial coin offering stage, the role of information asymmetry in
secondary cryptocurrency markets remains unexplored.
This research aims to complement the existing debate by examining the impact of information
1See also Easley et al. (2019) for a game-theoretic view on inter-dynamics of the cryptocurrency prices, transaction
fees, mining rewards and waiting times.
2Cryptocurrencies are even included in portfolios of several hedge funds (See the link).
2


### Page 3

asymmetry at the exchange level when considering the volatility, liquidity, market toxicity, and
returns of cryptocurrency. We proxy information asymmetry with the adverse selection component
of the effective spread. Specifically, we make use of the seminal models of Glosten and Harris (1988),
Huang and Stoll (1997), and Madhavan et al. (1997) to decompose the spread into two parts: an
adverse selection component related to permanent price change due to informed trading, and a
transitory component related to the temporary price change and order-processing costs. We also
apply the three-way decomposition of Huang and Stoll (1997) to account for the changes in the
transaction costs due to inventory risk. In a panel regression framework, we attempt to specifically
investigate the following questions: (i) does an increase in the adverse selection component of the
spread significantly impact the future volatility of cryptocurrency returns? (ii) does the adverse
selection component of the spread influence cryptocurrency liquidity? (iii) is the adverse selection
component related to a reduction in market toxicity? And finally, (iv) can the adverse selection
component act as a significant predictor of short-term cryptocurrency returns?
Accordingly, using the limit order book and trade data sourced from the Bitfinex Exchange, we doc-
ument that the adverse selection component of the effective spread is significant for the twelve most
frequently traded cryptocurrencies between August 2017 to June 2018. Adverse selection costs, on
average, correspond to ten percent of the estimated spread, suggesting that the proportion of the
spread attributable to adverse selection risk in cryptocurrency markets is also economically signifi-
cant. Moreover, we show that the adverse selection component of the spread is a significant predictor
of future volatility proxied by the standard deviation of cryptocurrency returns. Our results sug-
gest that informed trading activity increases the future levels of return volatility in cryptocurrency
markets. Furthermore, we present evidence that indicates the existence of an inverse relationship
between adverse selection costs and cryptocurrency liquidity. Through intraday panel regressions,
we initially show that informed trading activity increases the realized spread3 for cryptocurrency
trading. We then document that an increase in adverse selection costs results in higher levels of
order-book slope Amaya et al. (2018) and Amihud (2002) illiquidity levels. However, our findings
indicate that in cryptocurrency markets, the adverse selection component of the spread, does not
have a statistically significant impact on future levels of order-book depth. The impact of adverse
3We take realized spread as the average value of the difference between the best ask and bid price at each time
tick in the selected time interval for the selected cryptocurrency.
3


### Page 4

selection costs on future liquidity is the same for both the bid- and ask-side of the order book,
overruling a potential argument that has been based on asymmetric impact. The impact of adverse
selection costs on future levels of volatility and liquidity is similar to the previous findings docu-
mented when investigating currency market behaviour (Payne, 2003; Frömmel et al., 2008); while
partially contradicting prior evidence based on stock markets interactions (Rzayev and Ibikunle,
2019). Therefore, these findings can also contribute, albeit with a limited capacity, to the current
debate on discussions with regards to which asset class (whether stock, commodity, or currency) to
which cryptocurrencies belong. Results indicate that such products appear to be best described as
a currency when considering other alternatives.
Further, we show that the relationship between adverse selection costs and future market toxicity
levels is negative and statistically significant. This result might imply that price discovery due to
informed trading activity can actually lower the future profits for trading based on private informa-
tion, which in turn would result in lower toxicity levels. In line with this result, we finally reject the
hypothesis that adverse selection cost is not a significant predictor of cryptocurrency returns when
considering data at a one-hour time interval. In particular, we document that an increase in adverse
selection costs significantly reduces future returns. The direction of the relationship between in-
formed trading and future returns is consistent with the previous findings presented by Rzayev and
Ibikunle (2019). Our findings suggest that cryptocurrency markets are relatively efficient within
a short time horizon.
When considering transaction costs, the direction of the relationship be-
tween informed trading and cryptocurrency returns is inconsistent with the expectations of Biais
et al. (2020). However, the impact of adverse selection can be considered negligible compared to
significant events that indicate the easiness of transactions with cryptocurrencies4.
Our paper contributes to the growing literature on the microstructure of cryptocurrency markets5.
In particular, to the best of our knowledge, this study is the first to explore the intraday relationships
between informed trading, transaction costs, liquidity, volatility, and returns by using a cross-section
of cryptocurrencies traded in the same market. Therefore, our results can shed light on the main
determinants of trading activity and price discovery in cryptocurrency markets which are of direct
4Such as developments regarding the convertibility of cryptocurrencies with other currencies, introduction or
shutdown of large platforms, hacking activities, etc. (Biais et al., 2020)
5See Akyildirim et al. (2020); Alexander and Heck (2020); Alexander et al. (2020) and Alexander et al. (2020) as
recent empirical studies on the microstructure of some cryptocurrencies and cryptocurrency derivatives.
4


### Page 5

importance to cryptocurrency traders and market regulators from various perspectives.
The rest of this paper is presented as follows: Section 2 provides a concise presentation of our sample
data.
Section 3 discusses methodology, while Section 4 reports the associated results.
Finally,
Section 5 concludes.
2
Data and Variables
2.1
Data
For this study, we collect the intraday cryptocurrency data from the Kaiko digital asset store6.
Specifically, we employ the U.S. dollar-denominated cryptocurrency order book and trade data
(which includes the true side of the trade initiator) from the Bitfinex exchange. Even though a
large body of work focuses on cryptocurrency markets (Alexander and Dakos, 2020; Bariviera and
Merediz-Solà, 2021), only a few studies focus on the intraday dynamics of cryptocurrency trading
(Alexander and Heck, 2020; Alexander et al., 2020; Griffin and Shams, 2020; Makarov and Schoar,
2020). Our raw dataset covers the period between 1 April 2013 to 24 June 2018. The starting period
of this dataset covers only the intraday trading data for Bitcoin. Throughout our sample period,
77 cryptocurrencies traded against the USD, but only a few have available trading data for almost
a year. For those cryptocurrencies, the earliest starting date is 12 August 2017. We, therefore,
select the period between 12 August 2017 and 24 June 2018 to best represent one of the most liquid
periods for the Bitfinex exchange. Throughout the period between 2019 through 2021, many new
cryptocurrency exchanges began to trade, diminishing the market share of Bitfinex, as presented in
Figure 1. In the period after July 2018, several events generated substantial issues and reputational
damage for Bitfinex, coinciding with several sharp reductions in trading volumes7. While Bitfinex
later recovered much of its market share, our period of analysis surrounds that in which Bitfinex
6For a recent study that also uses this database, see Makarov and Schoar (2020). See Alexander and Dakos (2020)
for an extensive critique on different cryptocurrency data sources.
7Some events occurred during the period after the conclusions of our selected data, but one of the most serious
surrounding the case where iFinex, Inc., the parent company of Bitfinex became the source of a lawsuit instigated
by the New York attorney general as a result of a loan it received from Tether to cover more than $850 million that
had disappeared from accounts linked to a previous partner. Global Trade Solutions, AG, which operated as Crypto
Capital, and other companies to which iFinex had deposited its funds. Crypto Capital was previously a payment
processor for the exchange between 2014 to 2018.
5


### Page 6

was firmly a world-leading exchange8.
————————————— INSERT FIGURE 1 HERE ———————————-
We employ two filtering mechanisms to our raw data to achieve a representative sample. First, we
choose cryptocurrencies that have data starting on 12 August 2017 and are still actively traded on
the last day of our sample. Second, for any selected frequency9, we choose those cryptocurrencies
having less than a 1% non-trading time interval within the sample period.
With this selection
criteria, we are left with the following: Bitcoin Cash (BCH), Bitcoin (BTC), Dash (DSH), EOS
(EOS), Ethereum Classic (ETC), Ethereum (ETH), Iota (IOT), Litecoin (LTC), OmiseGO (OMG),
Monero (XMR), Ripple (XRP), and Zcash (ZEC).
2.2
Market variables
Using the intraday trades, we compute cryptocurrency-specific measures for volatility, liquidity,
and toxicity.
Specifically, we calculate the standard deviation of returns (σR), realized spread
(SPREAD), Amihud illiquidity (ILLIQ), order-book slope (SLOPE), order-book depth (DEPTH),
market toxicity (MT), total trading volume (TV ), and the difference between buyer and seller-
initiated trades (BSI) for all sample cryptocurrencies and all of the sampling frequencies. Total
volume TVi,t is calculated as the logarithm of the U.S. dollar-denominated total volume of trades
for cryptocurrency i in time interval t. Further, return Ri,t is defined as Ri,t = log(Pi,t/Pi,t−1 where
Pi,t is the last price in time interval t for cryptocurrency i, while the volatility of returns, σR
i,t is the
standard deviation of returns of the transactions in interval t for cryptocurrency i.
We identify the buy-sell imbalance (BSIi,t) as the absolute difference between buyer- and seller-
8While focusing on a single exchange for a relatively short time interval might generate concerns with regards to
the representativeness of the results, it is essential to underline that in cryptocurrency research, there are significant
issues regarding data aggregation from multiple sources, especially for multivariate analyses. Alexander and Dakos
(2020) underline problems with timestamp mismatch, non-synchronicity, exchange arbitrage, and the use of non-
traded prices when data from multiple sources are used in multivariate cryptocurrency research. To avoid problems
associated with non-concurrent prices, we solely focus on the intraday dynamics in a single market, Bitfinex. Even
though Bitfinex is a reliable exchange with high liquidity and low counterparty risk (Borri and Shakhnov, 2022), the
selected time interval prevents potential problems previously documented for the data feed from Bitfinex. Specifically,
price deviations between Bitfinex and other centralised cryptocurrency exchanges were minimal during our examined
sample period. This is mainly because our sample ends before November 2018, when Bitfinex introduced trading on
Tether, creating significant discrepancies with prices in different exchanges (Alexander and Dakos, 2020).
9We use three sampling frequencies based on 1-min, 15-min, and 60-min data intervals.
6


### Page 7

initiated trades in time interval t for cryptocurrency i. That is,
BSIi,t = |Bi,t −Si,t|
(1)
where Bi,t (Si,t) is the number of buyer-initiated (seller-initiated) trades in the time interval t for
cryptocurrency i, while market toxicity (MTi,t), is defined as follows:
MTi,t =
BSIi,t
(Bi,t + Si,t)
(2)
where Bi,t (Si,t) is the number of buyer-initiated (seller-initiated) trades in the time interval t for
cryptocurrency i. Specifically, we measure liquidity in various ways: Amihud (2002) measure for
cryptocurrency i in time interval t is the ratio of absolute stock return to the total trading volume
for i; that is:
ILLIQi,t = |Ri,t|
TVi,t
(3)
Market depth (DEPTHi,t) is the average of the average volume waiting at the best bid and ask levels
at each time tick in the time interval t for cryptocurrency i, where ask-side depth (DEPTHA
i,t) is the
average volume waiting at the best ask level at each time tick in the time interval t for cryptocurrency
i. Similarly, bid-side depth (DEPTHB
i,t) is the average volume waiting at the best bid level at each
time tick in the time interval t for cryptocurrency i. We calculated the SPREADi,t as the average
value of the difference between the best ask and bid price at each time tick in the time interval t
for cryptocurrency i. The order-book slope (SLOPEi,t) is measured as the marginal liquidity cost
as in Amaya et al. (2018). In particular, assume that at a give time t, the best N offer prices are
given by p1 < ... < pN and the best N bid prices by p−1 > ... > p−N. Denote the quantity offered
at price pi by xi, the total quantity available up to the ith best ask price by Xi, and the average
price per share by ˆSt(Xi). Namely,
Xi
=
i
X
j=1
xj
(4)
ˆSt(Xi)
=
Pi
j=1 pjxj
Xi
(5)
7


### Page 8

In a similar way for the bid side, we calculate
X−i
=
i
X
j=1
x−j
(6)
ˆSt(X−i)
=
Pi
j=1 p−jx−j
X−i
(7)
Then we apply the following linear regression model
ˆSt(Xi) = ˆαt + ˆλtXn + ϵt,
n = −N, ..., −1, 1, ..., N.
(8)
We take the average of ˆλt for each time tick in the time interval t and use it as the order-book slope
for cryptocurrency i. Finally, we calculated the bid-side slope (SLOPEB
i,t) by applying the above
procedure only to the bid-side of the order book. Similarly, the ask-side slope (SLOPEA
i,t) is found
by applying the above procedure only to the ask-side of the order book.
2.3
Adverse selection measures
In addition to market variables, we compute the three measures for the adverse selection component
of the spread {ASCGH, ASCHS2, ASCMRR} for all cryptocurrencies in our sample, and for all of the
selected sampling frequencies using the seminal works of Glosten and Harris (1988); Huang and Stoll
(1997) and Madhavan et al. (1997), respectively. All of these papers have a two-way decomposition
of the spread where there is a transitory component related to the order processing costs (OPCs)
and a component related to the adverse selection costs (ASCs). Furthermore, Huang and Stoll
(1997) document that both Glosten and Harris (1988) and Madhavan et al. (1997) models ignore
the role of inventory costs (IC), therefore authors provide a three-way decomposition. ASCHS3
denotes the adverse selection costs computed with the three-way decomposition of the Huang and
Stoll (1997) framework. Further details regarding these measures are provided in Section 3.
2.4
Descriptive statistics
Tables 1 and 2 present the descriptive statistics and correlations respectively, among currency-
specific measures calculated over 60-minute frequency sampling. The largest positive correlation
8


### Page 9

is identified amongst the adverse selection measures ASCGH, ASCHS2 and ASCMRR with a pre-
sented estimated value of almost 100%, whereas the largest negative correlation is identified in the
relationship between ASCGH and trading volume, with a correlation coefficient of approximately
-50%. The contemporaneous pairwise correlation between TV and the adverse selection component
of the spread is identified to be negative and significant for all models. Similarly, we observe a
negative and statistically significant correlation between ASCGH, ASCHS2 and ASCMRR and σR.
Moreover, there is a positive correlation between adverse selection costs and illiquidity measured by
SPREAD, ILLIQ, and SLOPE. We also observe a negative correlation between adverse selection
costs and order-book depth (DEPTH). To that end, we suspect that there is an inverse relationship
between informed trading activity and liquidity in cryptocurrency markets.
————————— INSERT TABLES 1 and 2 HERE —————————
3
Methodology
3.1
Estimating the adverse selection component of the spread
To compute the adverse selection component of the spread, we rely on the seminal works of Glosten
and Harris (1988), Huang and Stoll (1997), and Madhavan et al. (1997). These studies separate
price changes into a transitory component related to the order processing costs (OPC), inventory
holding costs (IC) (in the case of Huang and Stoll (1997)), and an adverse selection component
(ASC) associated with permanent price changes and informed trading. In line with these studies,
we define mt as the true value of the underlying security conditional on the information available
at time t. With the information arriving in the market, true value changes with the new trade in
the following manner:
mt = mt−1 + ZtQt + ϵt
(9)
where Qt corresponds to trade direction, that is, Qt = 1
(Qt = −1) if the trade is buyer- (seller-)
initiated. Zt is the adverse selection component that has an impact on the true prices which are
unobservable. Instead of the true value of the asset, traders observe the price which is modelled as
9


### Page 10

follows:
Pt = mt + QtCt
(10)
Observed price also changes with the new trade but this change is temporary. Therefore Ct can be
labelled as the transitory component of the trade which affects observed prices but not the true value.
Transitory component of the trade is rather associated with the order processing costs (OPCs).
Glosten and Harris (1988) model the adverse selection component and transitory component as a
function of trade size Vt, as follows,
Zt = z0 + z1Vt
(11)
Ct = c0 + c1Vt
(12)
The system of equations (9)-(12) cannot be estimated directly as mt is not observable. However,
using the price difference ∆Pt = Pt −Pt−1 we can write the system as:
∆Pt = mt + QtCt −mt−1 −Qt−1Ct−1
= mt−1 + QtZt + ϵt + QtCt −mt−1 −Qt−1Ct−1
= QtZt + QtCt −Qt−1Ct−1 + ϵt
= Qt(z0 + z1Vt) + Qt(c0 + c1Vt) −Qt−1(c0 + c1Vt−1) + ϵt
= z0Qt + z1QtVt + c0(Qt −Qt−1) + c1(QtVt −Qt−1Vt−1) + ϵt
= z0Qt + z1QtVt + c0(∆Qt) + c1(∆QtVt) + ϵt
(13)
where the implied adverse selection component of the spread is given by ASCGH = 2 × ( ˆz0 +
ˆz1Vt). The order processing costs are associated with the transitory component which is given by
OPCGH = 2×( ˆc0 + ˆc1Vt). Madhavan et al. (1997) assume the unexpected portion of the order flow
affects the true value of the underlying asset, and authors construct a trade indicator spread model
similar to Glosten and Harris (1988). Their model can be written as:
∆Pt = (θ + ϕ)Qt −ϕQt−1 + ϵt
(14)
10


### Page 11

In this framework, the adverse selection component of the spread is then calculated as ASCMRR = 2ˆθ
and the associated order processing costs are given by OPCMRR = 2ˆϕ. Huang and Stoll (1997)
model the change in price as the proportion of the constant half spread ( ν
2). They indicate that the
observed price (pt) deviates from the true value of the asset (mt) by the signed half spread.
Pt = mt + ν
2Qt + ϵt.
(15)
Taking the first difference in the price equation in a similar fashion results in the following model:
∆Pt = λν
2Qt−1 + ν
2(∆Qt) + ϵt
(16)
where ASCHS2 = ˆλ = ˆα + ˆβ and ˆα is the percentage of the half spread attributable to adverse
selection and β is the percentage of the half spread attributable to the inventory costs (ICs) in Huang
and Stoll (1997) framework. The two-way decomposition of Huang and Stoll (1997) presented in
equation (16) is identical with the framework of Madhavan et al. (1997) presented in equation (14).
Huang and Stoll (1997) further demonstrate that both Glosten and Harris (1988) and Madhavan
et al. (1997) ignore the role of ICs. That is, both ˆZt and ˆθ assume ˆβ = 0. Therefore, authors
extend their basic model with induced serial correlation in trade flows to provide a three-way
decomposition of the spread consisting of OPC, IC and ASC. Specifically, they show that the
conditional expectation of the trade indicator at time t −1, given t −2 as:
E(Qt−1|Qt−2) = (1 −2π)Qt−2
(17)
and modify their original approach as follows:
∆Pt = ν
2Qt + (α + β −1)ν
2Qt−1 −αν
2(1 −2π)Qt−2 + ϵt
(18)
Therefore simultaneously estimating the equations (17) and (18) for the three-way decomposition
of Huang and Stoll (1997) will yield a separate estimate for the proportion of adverse selection costs
(ASCHS3 = ˆα), proportion of inventory costs ICHS3 = ˆβ and the proportion of order processing
11


### Page 12

costs (OPCHS3 = 1 −ˆα −ˆβ) of the estimated spread.
3.2
Panel Regressions
3.2.1
The relationship between informed trading and volatility of cryptocurrency re-
turns
The seminal model of Kyle (1985) provides a theoretical framework for driving equilibrium prices
of financial securities under the presence of information asymmetry between traders. The model
indicates that information is incorporated into prices at a constant rate. Previous studies show a
significant and positive relationship between trading volume and return volatility. For example,
Collin-Dufresne and Fos (2016) extend the model of Kyle (1985) and indicate that volatility and
return relationship is driven by uninformed trading. In addition, several studies conjecture a nega-
tive relationship between informed trading activity and return volatility (e.g., Rzayev and Ibikunle
(2019) for U.S. equities). On the contrary, Frömmel et al. (2008) documents a positive relation-
ship between informed trading activity and return volatility for foreign exchange (FX) markets.
Specifically, the authors argue that order flows of big financial institutions and banks contribute to
explaining FX return volatility. To this end, we examine the predictive relationship between adverse
selection costs and return volatility, and we form our first hypothesis using the following model:
σR
i,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 + γ4BSIi,t−1 + γ5MTi,t−1
(19)
+ γ6ASCk
i,t−1 + γ7OPCk
i,t−1 + γ8ICk
i,t−1 + εi,t
where ASCk, OPCk and ICk respectively denote the adverse selection costs, order processing costs
and inventory holding costs calculated using two-way decompositions of Glosten and Harris (1988);
Madhavan et al. (1997) and Huang and Stoll (1997) framework and the three-way decomposition
of Huang and Stoll (1997), that is, k ∈{GH, MRR, HS2, HS3}. By construction, ICk = 0 for
k ∈{GH, MRR, HS2}. αi and θt respectively denote cryptocurrency- and time-fixed effects.
Hypothesis 1: Adverse selection component of the spread is a significant predictor of future return
12


### Page 13

volatilities in cryptocurrency markets,
H0 : γ6 = 0
HA : γ6 ̸= 0
3.2.2
The relationship between informed trading and cryptocurrency liquidity
In the microstructure literature, there are competing claims regarding the relationship between the
adverse selection cost of spread and the liquidity of assets. Huang and Stoll (1997) argued that
intermediaries in financial markets face three costs that determine the realised bid-ask spreads:
order processing costs, inventory holding costs and adverse selection costs. Glosten and Milgrom
(1985) suggest that intermediaries widen the spreads under the risk of being adversely selected when
trading against informed traders. To this end, ceteris paribus, they expect the realised spread to
be positively related to adverse selection costs which in turn reduces the liquidity of assets as the
transaction costs increase for an average investor.
On the contrary, in financial markets, informed investors are expected to time their trades during
periods when there are large liquidity traders present in the market. Admati and Pfleiderer (1988)
indicate that informed investors disguise their information when there are high levels of liquidity
trading. Ibikunle (2018) documents that informed trading activity increases with overall trading
volume determined by liquidity trading. From the cost perspective, in dealership markets, liquidity
trading can provide lower inventory holding costs for intermediaries therefore the impact of informed
trading on transaction costs can be minimal.
Cryptocurrency markets are order-driven markets without designated market makers, but liquidity is
then typically supplied by voluntary market makers who largely follow the same quotation principles
as designated market makers. For most asset classes traded as limit order book markets, the market
making is now dominated by high-frequency traders (Nawn and Banerjee, 2019; Chen and Garriott,
2020). It has been widely reported that a significant number of high-frequency trading firms are
trading cryptocurrencies10. To that end, inventory costs can also be significant determinants of
overall liquidity. Furthermore, the trading fees at Bitfinex range from 10 to 20 basis points for
low-volume traders. This is very high compared to equity exchanges in the U.S. where the trading
10See https://www.ft.com/content/40a86de6-b5dd-11e7-a398-73d59db9e399
13


### Page 14

fees are typically lower than one basis point. Our panel regressions are presented below to enable
us to examine the predictive relationship between adverse selection costs and overall liquidity in
cryptocurrency markets, controlling for the order processing and inventory holding costs. This leads
us to our second hypothesis:
Hypothesis 2: An increase in the adverse selection component of the spread decreases liquidity in
cryptocurrency markets.
ILLIQi,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 + γ4BSIi,t−1 + γ5MTi,t−1
(20)
+ γ6ASCk
i,t−1 + γ7OPCk
i,t−1 + γ8ICk
i,t−1 + εi,t
where ILLIQi,t is the Amihud (2002) illiquidity measure.
Similarly, we provide direct test on
the effect of informed trading on the transaction costs in cryptocurrency markets by running the
following model:
SPREADi,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 + γ4BSIi,t−1 + γ5MTi,t−1
(21)
+ γ6ASCk
i,t−1 + γ7OPCk
i,t−1 + γ8ICk
i,t−1 + εi,t
where SPREADi,t is the realised spread for cryptocurrency i in time interval t. Moreover, we also
examine the relationship between adverse selection costs and order-book slope where the order-book
slope is defined as the marginal liquidity cost as in Amaya et al. (2018).
SLOPEi,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 + γ4BSIi,t−1 + γ5MTi,t−1
(22)
+ γ6ASCk
i,t−1 + γ7OPCk
i,t−1 + γ8ICk
i,t−1 + εi,t
Since ILLIQ, SPREAD and SLOPE are inverse liquidity measures, Hypothesis 2 can be repre-
sented in the following form:
H0 : γ6 = 0
HA : γ6 > 0
14


### Page 15

Finally, we examine the relationship between adverse selection costs with depth under the following
setting:
DEPTHi,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 + γ4BSIi,t−1 + γ5MTi,t−1
(23)
+ γ6ASCk
i,t−1 + γ7OPCk
i,t−1 + γ8ICk
i,t−1 + εi,t
where DEPTHi,t is the tick average of the average volume waiting at the best bid and ask levels
in the order book in time interval t for cryptocurrency i. For depth, we change the alternative
hypothesis as
HA : γ6 < 0
3.2.3
The differential impact of adverse selection on bid- and ask-side liquidity
Recently, theoretical studies indicated that liquidity in down markets can be radically different than
liquidity in up markets, underlining the importance of differences in bid-side and ask-side liquidity
(Roşu, 2009). Empirically, Brennan et al. (2012) document that ask-side illiquidity estimates are
priced more strongly than on the bid-side in the cross-section of expected returns. Furthermore, they
conclude that sell-side liquidity is the main contributor to the liquidity premium in U.S. markets.
Similarly, using eleven years of limit order book data for NYSE, Cenesizoglu and Grass (2018) show
that even though the commonality in liquidity on the bid-side is larger than the ask-side during the
financial crisis, only the ask side illiquidity predicts future returns.
In this study, using the limit order book of cryptocurrencies, we also compute the bid-side and ask-
side liquidity measures separately. The order-book slope for the ask-(bid-)side is given by SLOPEA
i,t
(SLOPEB
i,t). Similarly, we represent the ask-(bid-)side depth with DEPTHA
i,t (DEPTHB
i,t). We
respectively use the ask- and bid-side slope and depth measures as dependent variables in equations
(22) and (23) to test our second hypothesis. This allows us to examine the potential asymmetric
impacts of adverse selection costs on ask- and bid-side liquidity.
3.2.4
The relationship between informed trading and cryptocurrency market toxicity
Order-flow (Market) toxicity is defined as the adverse selection costs faced by investors who are
not aware that they provide liquidity at a loss (Easley et al., 2011). Rzayev and Ibikunle (2019)
15


### Page 16

argue that market toxicity can be considered as a high-frequency equivalent of adverse selection
risk. To this end, we expect market toxicity to raise with an increase in the adverse selection costs.
Therefore, our third hypothesis can be stated as follows:
Hypothesis 3: An increase in the adverse selection component of the spread increases the market
toxicity in the cryptocurrency markets.
MTi,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 + γ4BSIi,t−1 + γ5MTi,t−1
(24)
+ γ6ASCk
i,t−1 + γ7OPCk
i,t−1 + γ8ICk
i,t−1 + εi,t
H0 : γ6 = 0
HA : γ6 > 0
3.2.5
The relationship between informed trading and cryptocurrency returns
The efficient market hypothesis indicates that prices reflect all available information about the value
of the underlying financial securities. Prices change only with the arrival of new information and
since the arrival of new information is random, it is impossible to predict future prices. There
is a large body of literature documenting that prices cannot be predicted consistently over a daily
horizon (Fama, 1970). On the other hand, Chordia et al. (2002, 2008) find that lag order imbalances
can be a significant predictor of returns over short horizons and argue that investors can be slow to
act on new information. Accordingly, order imbalances can proxy for informed trading which affects
the true value of the underlying security. Rzayev and Ibikunle (2019) state that the transitory
component of the order volume (which is a proxy for informed trading) is a significant and inverse
predictor of short-term stock returns which is consistent with the previous literature that documents
market inefficiencies over short horizons. To this end, we expect the adverse selection component
of the spread to be a significant predictor of short-term cryptocurrency returns.
In addition to the argument above, the theoretical cryptocurrency pricing framework by Biais et al.
(2020) indicates that investors, who expect future prices to be high, anticipate future transactional
benefits which in turn results in high prices today. Cryptocurrencies also entail transaction costs
in the form of limited convertibility, lower rate of acceptances and other problems embedded in the
16


### Page 17

transaction and mining processes. Accordingly, the authors show that there is a positive (negative)
relationship between cryptocurrency returns and transaction costs (benefits). Considering all these
arguments above, our fourth hypothesis follows:
Hypothesis 4: Adverse selection component is a significant predictor of short-term cryptocurrency
returns.
Ri,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 + γ4BSIi,t−1 + γ5MTi,t−1
(25)
+ γ6ASCk
i,t−1 + γ7OPCk
i,t−1 + γ8ICk
i,t−1 + γ9DEPTHi,t−1 + γ10SLOPEi,t−1 + εi,t
H0 : γ6 = 0
HA : γ6 ̸= 0
4
Results
4.1
Estimating the adverse selection component of the spread
We compute the adverse selection component of the cryptocurrency spreads through the use of the
models presented by Glosten and Harris (1988); Huang and Stoll (1997) and Madhavan et al. (1997).
To test as to whether we observe significant informed trading activity in cryptocurrency markets,
we develop upon equations (13),(14), (16), and (18) using intraday trades of all cryptocurrencies in
our sample period with ordinary least squares11. Table 3 presents the adverse selection component
of the spread estimated by the Glosten and Harris (1988) model. The second column in Table 3
presents the mean estimate for the transitory component (OPCGH) throughout the sample period.
The third column corresponds to the p-value for the test with the null hypothesis of OPCGH = 0.
The fourth and fifth columns respectively correspond to the estimate for the adverse selection costs
and the corresponding p-value for the test with the null hypothesis of ASCGH = 0.
The last
column represents the percentage of the adverse selection cost over that of the entire estimated
spread. Accordingly, we reject the null hypothesis that the average adverse selection component
11We repeat our full sample analyses with Newey and West (1987) standard errors. Our full sample results are
robust to the potential heteroskedasticity and autocorrelation in the disturbance terms.
17


### Page 18

of the spread is zero for all cryptocurrencies in our sample period. XMR has the highest ratio for
the adverse selection with 13%. Even though the BTC has the highest estimate for the adverse
selection costs, the proportion of the spread attributable to adverse selection is one of the lowest in
our sample with 7%. This is significantly smaller compared to findings of Dimpfl (2017)12.
——————————- INSERT TABLE 3 HERE ——————————-
Similarly, in Table 4, we document the adverse selection component of the spread using Huang
and Stoll (1997) framework. The second and third columns respectively represent the estimated
coefficient for the spread (ˆν) and its standard error. The third and fourth columns represent the
estimate for the spread attributable to adverse selection and inventory holding costs (ASCHS2 =
ν ∗λ) and the corresponding standard errors. The last column gives the percentage of the spread
that is attributed to adverse selection and inventory holding costs (λ). Both the estimated measures
for adverse selection and order processing costs and the proportion of spread attributable to adverse
selection are almost identical with the Glosten and Harris (1988) model. The adverse selection costs
are significantly different from zero for all cryptocurrencies.
——————————- INSERT TABLE 4 HERE ——————————-
Moreover, in Table 5, we provide results for the adverse selection component of the spread estimated
using Madhavan et al. (1997) framework. The second and third columns in Table 5 presents the
estimates for order processing costs and the corresponding standard errors, respectively. Moreover,
in columns four and five we provide the estimate for adverse selection costs and the correspond-
ing standard errors. Similar to the previous two models, we document that the adverse selection
component of the spread is different than zero for all cryptocurrencies in our sample.
——————————- INSERT TABLE 5 HERE ——————————-
Finally, from the two-way decomposition, we understand that the estimates for adverse selection
costs ignore the role of inventory holding costs (Huang and Stoll, 1997). To account for the inventory
12Dimpfl (2017) shows that more than 50% of the spread is attributed to adverse selection for most of the Bitcoin
markets. The differences in results might be attributed to different market characteristics, different currencies and/or
different sample periods.
In addition, Dimpfl (2017) ignores the inventory holding and order-processing costs in
estimating the components of the spread.
18


### Page 19

holding costs, we use the three-way decomposition presented in equation (18). Table 6 present the
results for the estimation of the three-way decomposition of the Huang and Stoll (1997). Columns
two and three provide the estimate for the traded spread (ν) and the corresponding standard
error.
Columns four and five provide an estimate for the proportion of inventory costs in the
estimated spread (β) and the corresponding standard errors.
Similarly, columns six and seven
present the estimate for the proportion of adverse selection costs in the estimated spread (α) and
the corresponding standard error of the estimate. Finally, the last column gives the estimate for the
serial correlation in the trade flow. Our results indicate that the proportion of inventory holding
costs is highest for BTC which also has the highest estimate for the serial correlation in the trade
flow. We observe that the proportion of adverse selection in the estimated spread is negative for all
cryptocurrencies in our sample. This is because the estimated serial correlation in the trade flow
(π) is less than 0.5. Even though this finding is in line with those of Huang and Stoll (1997) for
U.S. equity markets, the negative spread has no meaning. Therefore, we exclude negative values for
ASC, OPC and IC in our panel regressions in the following section as well.13
——————————- INSERT TABLE 6 HERE ——————————-
To this end, we can argue that there is significant informed trading activity in cryptocurrency
markets. The results of the two-way decomposition models consistently indicate that the adverse
selection component of the spread is largest (smallest) for BTC (XRP) in dollar terms without
normalizing for average trade price. In addition, with the three-way decomposition model of Huang
and Stoll (1997), we observe that BTC has the highest serial correlation in the trade-flow and the
highest inventory costs both in terms of proportion of the spread and in dollar terms. In the next
part of our analysis, we test whether private information affects future returns, volatility of returns,
liquidity, and toxicity in cryptocurrency markets.
4.2
Panel Regressions
For our panel analysis, we estimate the adverse selection of the spreads for all cryptocurrencies
and all sampling frequencies (1-min, 15-min, and 60-min). Let ASCk
i,t be the adverse selection
13Because of the negative spread values, we remove a significant number of observations from our sample for three-
way decomposition of Huang and Stoll (1997). For example, Table 1 shows that the number of observations for the
two-way decomposition models is around 87000 whereas the estimate for three-way decomposition is around 28,000.
19


### Page 20

component of the spread for cryptocurrency i in time interval t estimated using model k which
can either be the two-way decompositions of Glosten and Harris (1988); Madhavan et al. (1997);
Huang and Stoll (1997) or the three-way decomposition of Huang and Stoll (1997), that is, k ∈
{GH, MRR, HS2, HS3}.
To examine the relationship between informed trading and return volatility (as in Hypothesis 1),
we first estimate equation (19) with currency- and time-fixed effects. The results are presented in
Table 7 in which Panel A, B and C display the results of the estimation for time intervals set to
1-min, 15-mins, and 60-mins, respectively. For all of the time intervals, we reject the null hypothesis
that an increase in adverse selection does not lead to a change in future return volatility. For the
relatively long intervals (15-mins and 60-mins), we document that future return volatility increases
with an increase in the adverse selection component of the spread. This result is robust across
different methods for calculating the adverse selection measure. Our findings are in line with those
by Frömmel et al. (2008) who document that an increase in informed trading activity increases the
volatility of currency returns. For the shortest interval (1-min), we observe the opposite sign and
conclude that an increase in the adverse selection costs reduces the return volatility, a finding similar
to that of Rzayev and Ibikunle (2019) for the U.S stock market. Since we have different signs for
different time intervals, we conduct a robustness check where we run equation (19) with absolute
price change |∆P| as the dependent variable. We observe that the impact of adverse selection costs
is positive for all time intervals when |∆P| is used as a dependent variable.14 Therefore, we conclude
that the relationship between informed trading activity and volatility in cryptocurrency markets
is similar to the previous findings documented for currency markets rather than stock markets.
This particular result is interesting as the discussion surrounding which asset class cryptocurrencies
belong to continues15 (whether it be considered a stock, commodity, or currency). Within a limited
capacity, our results support the asset’s consideration as a currency when compared to other listed
assets.
——————————- INSERT TABLE 7 HERE ——————————-
Secondly, we examine the relationship between adverse selection costs and the future liquidity
14We do not report the table containing the results of our robustness check due to space considerations. It is
available upon request.
15http://aswathdamodaran.blogspot.com/2017/10/the-bitcoin-boom-asset-currency.html
20


### Page 21

of cryptocurrencies.
We use Amihud illiquidity (ILLIQ) measure along with realised spread
(SPREAD) and order-book slope (SLOPE) as inverse measures of liquidity, and order-book depth
(DEPTH) as a direct measure of liquidity. We expect the liquidity to go down with the increase in
transaction costs (OPC, ASC and IC). Hence, our second hypothesis suggests a reverse relationship
between adverse selection costs and future liquidity. To test this second hypothesis, we estimate
equations (20), (21), (22), and (23) with currency- and time-fixed effects. Table 8 provides the
results for equation (20) which uses ILLIQ as a dependent variable. The results indicate that the
illiquidity of cryptocurrencies increases with an increase in the adverse selection component of the
spread. Similarly, we present the estimates for equation (21) in Table 9 which indicates that the
realised spread (SPREAD) also increases with information asymmetry, confirming our expecta-
tions that transaction costs are increasing with the presence of informed trading. We also observe a
positive relationship between adverse selection costs and future levels of order-book slope (SLOPE)
in Table 10 which provides additional evidence towards a reverse relationship between information
asymmetry and liquidity. Finally, we examine the role of information asymmetry in explaining the
future levels of order-book depth (DEPTH). According to Table 11, informed trading levels do not
have a significant impact on order-book depth, unlike other liquidity measures.
————————— INSERT TABLES 8-9-10-11 HERE —————————
Overall, our results confirm that information asymmetry increases the transaction costs in cryp-
tocurrency markets and adverse selection costs are significant determinants of future illiquidity of
the cryptocurrency markets as proxied by the Amihud illiquidity measure, and order-book slope.
Finally, we document that increased adverse selection costs do not have a statistically significant
impact on future levels of order-book depth.
Next, we test whether the impact of an increase in informed trading activity affects the bid- and
ask-side of the market differently. Recent studies underline the different attributes of bid- and ask-
side liquidity (Roşu, 2009; Brennan et al., 2012; Cenesizoglu and Grass, 2018), and the presence of
asymmetric adverse selection on the bid- and ask-side of the order book (Gencay et al., 2018). To this
end, we compute the bid- and ask-side measures for SLOPE and DEPTH for each cryptocurrency
and for all of the time intervals. Tables 12 and 13 respectively present the results for our panel
regressions where the dependent variables are bid- and ask-side slope, respectively. We observe that
21


### Page 22

an increase in informed trading activity increases the order-book slope for both bid- and ask-side,
reducing the liquidity on both sides of the trade. The coefficients of the adverse selection measures
are quite close for both bid- and ask-side slopes in terms of magnitude, for each of the time intervals.
Similarly, we show in Tables 14 and 15 that increased adverse selection has no significant effect on the
order-book depth for both buy- and sell-side of the trade, respectively. Therefore, we can argue that
informed trading has a symmetric effect on different sides of the liquidity of the cryptocurrencies.
————————- INSERT TABLES 12-13-14-15 HERE ————————-
Considering our third hypothesis, we check the relationship between informed trading activity and
market toxicity. As stated earlier, order-flow (market) toxicity is defined as the adverse selection
costs faced by investors who are not aware that they provide liquidity at a loss, and it is argued that
market toxicity can be considered as a high-frequency equivalent of adverse selection risk (Rzayev
and Ibikunle, 2019). Therefore, we expect a positive relationship between adverse selection costs
and future levels of toxicity. We define market toxicity as the ratio of absolute trade imbalance
to the total number of trades and the results of our panel regressions are displayed in Table 16.
Accordingly, we have puzzling findings. For all of the alternative measures of adverse selection
and different time intervals, we observe that informed trading activity reduces the future levels of
market toxicity. Our findings suggest that an increase in adverse selection cost reduces the future
levels of informed trading activity. Even though this finding is puzzling, a potential channel may be
attributed to the price discovery of informed trades in cryptocurrency markets. We may argue that
informed trading activity in cryptocurrency markets results in a greater price discovery compared to
other financial markets. Transaction costs are quickly adjusted in the presence of informed trading
activity so that an increase in transaction costs due to adverse selection risks might make the
(relatively short-term) trading based on private information less profitable, thus driving informed
traders away from the market thereby resulting in lower levels of future toxicity16.
——————————- INSERT TABLE 16 HERE ——————————-
16We check the impact of multicollinearity for all of the results presented above.
The univariate relationship
between ASC’s and future risk, liquidity and toxicity levels is consistent under a univariate setting which rules
out the multicollinearity problem for multivariate analysis. We do not present the univariate results due to space
limitations, but they are available upon request.
22


### Page 23

Finally, we examine the relationship between informed trading and future returns. From the mar-
ket efficiency perspective, we expect to see a negative association (Rzayev and Ibikunle, 2019),
whereas, from the cost perspective, a positive association is expected (Biais et al., 2020). Chordia
et al. (2002, 2008) show that informed trading activity proxied by lag order imbalances can be a
significant predictor of short-horizon returns as investors gradually react to new information. In
addition, Rzayev and Ibikunle (2019) indicates that informed order flow predicts the stock returns
in one-second frequency. However, for relatively long time intervals such as one-minute frequency,
informed trading does not predict future returns. Rzayev and Ibikunle (2019) attribute the lack
of statistical significance to the price impact of high-frequency traders (HFT) in equity markets.
They indicate that increased HFT volume helps increase the speed of information incorporation into
stock prices and leads to the elimination of arbitrage opportunities. Consequently, we present our
results for our adverse selection measures ASCGH, ASCMRR, ASCHS2 and ASCHS3 respectively
in Tables 17, 18, 19 and 20. Our results indicate that an increase in the adverse selection of the
spread is a significant and negative predictor of market efficiency for relatively long time intervals.
This finding is consistent across all different measures of adverse selection components with two-
way decomposition. On the contrary, we document that informed trading activity, proxied by the
three-way decomposition of Huang and Stoll (1997) is not a significant predictor of future returns.
However, it is important to note that our sample for the three-way decomposition of the spread is
quite small. Since the serial correlations in the order flow are less than 0.5 for most of the time
intervals, we frequently observe negative values for ASCHS3 and exclude them from our sample.
Overall, the evidence suggested by the two-way decompositions of the spread asserts that informed
trading activity proxied by the adverse selection component of the spread is a significant predictor
of future cryptocurrency returns. We document that increases in the adverse selection costs reduce
the future returns (at a 60-minute frequency). Consequently, we can argue that in cryptocurrency
markets, transaction costs are adjusted so that the trading based on private information becomes
less profitable within an hour17.
17Concerning Section 4.2, since the dependent variable in each panel regression shows up as an explanatory variable
in all other panel regressions, we also design a vector auto-regression (VAR) setup and estimate of this VAR model
for each cryptocurrency accordingly. Results are found to be qualitatively similar. We do not present the results
here to save space, however, they can be obtained from the authors upon request and will also be made available as
supplementary material to this paper.
23


### Page 24

——————————- INSERT TABLES 17, 18, 19 and 20 HERE ——————
5
Conclusion
Considering the substantial growth of cryptocurrency trading in recent years, an interesting ques-
tion surrounds as to whether there are investors who possess superior information, which provides
substantial benefit when assessing the fundamental values of these new instruments. Since all major
cryptocurrencies are technological developments that serve a specific purpose, a group of investors
could better assess net transactional benefits, and therefore, the fundamental value of associated
products. To that end, investors who lack sufficient knowledge about cryptocurrencies face a signif-
icant adverse selection problem when trading with informed traders in secondary markets. Another
source for a potential adverse selection problem in secondary cryptocurrency markets can be at-
tributed to the informational differences between retail and institutional investors. Prior evidence
suggests that institutional investors have substantial informational advantages, mainly due to their
superior ability to monitor the conditions and process information at lower costs in traditional mar-
kets (Seppi, 1992; Hessel and Norman, 1992; Lang and McNichols, 1997). Even though institutional
investors are becoming increasingly prevalent in cryptocurrency markets, the literature is silent on
the impact of adverse selection in secondary cryptocurrency markets. In this paper, we aim to fill
this gap by focusing on the role of information asymmetry in determining future volatility, liquidity,
market toxicity, and return levels. Specifically, we focus on the most traded cryptocurrencies based
on the Bitfinex exchange during a period when the exchange was the leading platform for secondary
cryptocurrency trading activity. Using a high-frequency U.S. dollar-denominated order book and
trade data, we initially show a statistically significant adverse selection component of the effective
spread for all cryptocurrencies in our sample. Our results also suggest that, on average, 10% of
the effective spread is attributable to adverse selection risks, indicating that the role of information
asymmetry is not only statistically significant but also economically significant.
We further document that adverse selection costs significantly predict intraday volatility, liquidity,
market toxicity, and returns. Specifically using intraday panel regressions, we show that, on aver-
age, future volatility levels increase with the increases in adverse selection costs in secondary cryp-
tocurrency markets. We also document that informed traders demand liquidity in cryptocurrency
24


### Page 25

markets. In particular, our results suggest that increases in adverse selection costs are associated
with overall decreases in future liquidity levels, as evidenced by positive predictive relationships
with inverse liquidity measures such as realized spread, Amihud illiquidity measure, and order book
slope. We further document that the predictive relationship between adverse selection costs and
future liquidity is symmetric on both the bid- and the ask side of the limit order book. The impact
of adverse selection costs on future levels of volatility and liquidity is in line with the previous
findings documented for the currency markets (Payne, 2003; Frömmel et al., 2008); rather than
recent evidence on stock markets (Rzayev and Ibikunle, 2019). These results may, therefore, have
the potential to advance the discussions on which asset class cryptocurrencies belong, with evidence
suggesting that it is best described as a currency, albeit within a limited capacity.
Finally, we document a negative predictive relationship between adverse selection costs and future
market toxicity levels. This finding suggests that increases in transaction costs due to information
asymmetry can lead to higher price discovery and drive investors with private information away
from the market as trading based on private information becomes less profitable. This would lead
to lower levels of market toxicity in the future. In line with this result, we also observe a significant
and negative predictive relationship between adverse selection costs and future returns in 60-minute
intervals. From the transaction cost perspective, the direction of the predictive relationship between
adverse selection costs and future returns does not support the expectations of (Biais et al., 2020).
However, the transaction costs in the framework of Biais et al. (2020) are related to the proxies
indicative of the easiness of transactions with cryptocurrencies. Therefore, we argue that the increase
in transaction costs due to adverse selection risk can be negligible compared to the significant events
determining the future of cryptocurrency trading. On the other hand, from a market efficiency
perspective, the inverse relationship between informed trading activity and future returns indicates
that cryptocurrency markets are efficient at relatively short horizons Rzayev and Ibikunle (2019).
Consequently, we can argue that transaction costs are adjusted in cryptocurrency markets so that
trading based on private information becomes less profitable within an hour.
25


### Page 26

References
Admati, A. R. and P. Pfleiderer (1988). A theory of intraday patterns: Volume and price variability. Review
of Financial Studies 1, 3–40.
Akyildirim, E., S. Corbet, P. Katsiampa, N. Kellard, and A. Sensoy (2020). The development of bitcoin
futures: Exploring the interactions between cryptocurrency derivatives.
Finance Research Letters 34,
101234.
Alexander, C., J. Choi, H. Massie, and S. Sohn (2020). Price discovery and microstructure in ether spot and
derivative markets. International Review of Financial Analysis 71, 101506.
Alexander, C., J. Choi, H. Park, and S. Sohn (2020). Bitmex bitcoin derivatives: Price discovery, informa-
tional efficiency and hedging effectiveness. Journal of Futures Markets 40, 23–43.
Alexander, C. and M. Dakos (2020). A critical investigation of cryptocurrency data and analysis. Quantitative
Finance 20, 173–188.
Alexander, C. and D. Heck (2020). Price discovery, high-frequency trading and jumps in bitcoin markets.
SSRN Working Paper (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3383147).
Amaya, D., J.-Y. Filbien, O. Cédric, and A. F. Roch (2018). Distilling liquidity costs from limit order books.
Journal of Banking and Finance 94, 16–34.
Amihud, Y. (2002). Illiquidity and stock returns: Cross-section and time-series effects. Journal of Financial
Markets 5, 31–56.
Bariviera, A. F. and I. Merediz-Solà (2021). Where do we stand in cryptocurrencies economic research? a
survey based on hybrid analysis. Journal of Economic Surveys 35(2), 377–407.
Biais, B., C. Bisiere, M. Bouvard, C. Casamatta, and A. J. Menkveld (2020). Equilibrium Bitcoin pricing.
SSRN Working Paper (https://ssrn.com/abstract=3261063).
Borri, N. (2019). Conditional tail-risk in cryptocurrency markets. Journal of Empirical Finance 50, 1–19.
Borri, N. and K. Shakhnov (2022, 03). The Cross-Section of Cryptocurrency Returns. The Review of Asset
Pricing Studies. raac007.
Brennan, M. J., T. Chordia, A. Subrahmanyam, and Q. Tong (2012). Sell-order liquidity and the cross-section
of expected stock returns. Journal of Financial Economics 105, 523–541.
26


### Page 27

Cenesizoglu, T. and G. Grass (2018). Bid-and ask-side liquidity in the NYSE limit order book. Journal of
Financial Markets 38, 14–38.
Chen, M. and C. Garriott (2020). High-frequency trading and institutional trading costs. Journal of Empirical
Finance 56, 74–93.
Chod, J. and E. Lyandres (2020). A theory of ICOs: Diversification, agency, and information asymmetry.
Management Science (forthcoming).
Chordia, T., R. Roll, and A. Subrahmanyam (2002). Order imbalance, liquidity, and market returns. Journal
of Financial Economics 65, 111–130.
Chordia, T., R. Roll, and A. Subrahmanyam (2008). Liquidity and market efficiency. Journal of Financial
Economics 87, 249–268.
Collin-Dufresne, P. and V. Fos (2016). Insider trading, stochastic liquidity, and equilibrium prices. Econo-
metrica 84, 1441–1475.
Dimpfl,
T.
(2017).
Bitcoin
market
microstructure.
SSRN
Working
Paper
(https://ssrn.com/abstract=2949807).
Easley, D., M. M. L. de Prado, and M. O’Hara (2011). The exchange of flow toxicity. Journal of Trading 6,
8–13.
Easley, D., M. O’Hara, and S. Basu (2019). From mining to markets: The evolution of Bitcoin transaction
fees. Journal of Financial Economics 134, 91–109.
Fama, E. F. (1970). Efficient capital markets: A review of theory and empirical work. Journal of Finance 25,
383–417.
Frömmel, M., A. Mende, and L. Menkhoff (2008). Order flows, news, and exchange rate volatility. Journal
of International Money and Finance 27, 994–1012.
Gencay, R., S. Mahmoodzadeh, J. Rojcek, and M. C. Tseng (2018). Price impact and bursts in liquidity
provision. Quantitative Finance 18, 1129–1148.
Glosten, L. R. and L. E. Harris (1988).
Estimating the components of the bid/ask spread.
Journal of
Financial Economics 21, 123–142.
Glosten, L. R. and P. R. Milgrom (1985).
Bid, ask and transaction prices in a specialist market with
heterogeneously informed traders. Journal of Financial Economics 14, 71–100.
27


### Page 28

Griffin, J. M. and A. Shams (2020). Is bitcoin really untethered? The Journal of Finance 75(4), 1913–1964.
Hessel, C. A. and M. Norman (1992). Financial characteristics of neglected and institutionally held stocks.
Journal of Accounting, Auditing and Finance 7, 313–334.
Huang, R. D. and H. R. Stoll (1997). The components of the bid-ask spread: A general approach. Review
of Financial Studies 10, 995–1034.
Ibikunle, G. (2018). Trading places: Price leadership and the competition for order flow. Journal of Empirical
Finance 49, 178–200.
Kyle, A. S. (1985). Continuous auctions and insider trading. Econometrica, 1315–1335.
Lang, M. and M. McNichols (1997). Institutional trading and corporate performance. Stanford Univer-
sity Working Paper.
Madhavan, A., M. Richardson, and M. Roomans (1997). Why do security prices change? A transaction-level
analysis of NYSE stocks. Review of Financial Studies 10, 1035–1064.
Makarov, I. and A. Schoar (2020). Trading and arbitrage in cryptocurrency markets. Journal of Financial
Economics 135, 293–319.
Momtaz, P. P. (2020).
Initial coin offerings, asymmetric information, and loyal CEOs.
Small Business
Economics (forthcoming).
Nawn, S. and A. Banerjee (2019). Do the limit orders of proprietary and agency algorithmic traders discover
or obscure security prices? Journal of Empirical Finance 53, 109–125.
Newey, W. K. and K. D. West (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation
consistent covariance matrix. Econometrica: Journal of the Econometric Society, 703–708.
Payne, R. (2003). Informed trade in spot foreign exchange markets: an empirical investigation. Journal of
International Economics 61(2), 307–329.
Roşu, I. (2009). A dynamic model of the limit order book. Review of Financial Studies 22, 4601–4641.
Rzayev, K. and G. Ibikunle (2019). A state-space modeling of the information content of trading volume.
Journal of Financial Markets 46, 100507.
Seppi, D. J. (1992). Block trading and information revelation around quarterly earnings announcements.
Review of Financial Studies 5, 281–305.
28


### Page 29

Figure 1: Bitfinex Trading Volumes
Note: The above figure we see the trading volumes on the Bitfinex exchange. Data was obtained from Bitcoinity and are available here.
29


### Page 30

Table 1: This table presents descriptive statistics for our variables calculated for 60 minute frequency
sampling. For our panel analysis, we restrict our sample to the period between August 2017 and
June 2018 in order to provide a substantial sample of cryptocurrencies upon which the market could
trade, therefore providing a strong sample to analyse.
Variable
Observations
Mean
Std. Dev.
Minimum
Maximum
TVi,t
90,334
9.26
2.84
1.47
18.07
BSIi,t
90,334
198.90
338.48
0.00
12842.00
MTi,t
90,334
0.19
0.16
0.00
1.00
Ri,t
91,661
0.00
0.02
-0.33
0.37
ILLIQi,t
90,322
0.00
0.00
0.00
0.03
σR
i,t
90,334
0.01
0.01
0.00
0.25
ASCGH
i,t
87,024
0.05
0.08
0.00
1.10
ASCHS2
i,t
87,160
0.05
0.08
0.00
1.10
ASCHS3
i,t
28,244
0.03
0.06
0.00
1.08
ASCMRR
i,t
87,161
0.05
0.08
0.00
1.10
OPCGH
i,t
87,024
0.37
0.83
0.00
31.79
OPCHS2
i,t
87,160
0.37
0.82
0.00
31.72
OPCHS3
i,t
28,244
0.30
0.66
0.00
18.07
OPCMRR
i,t
87,161
0.37
0.82
0.00
31.72
ICHS3
i,t
28,244
0.03
0.06
0.00
0.69
SPREADi,t
88,632
0.47
2.58
0.00
382.82
DEPTHi,t
90,665
2.24
7.80
-0.09
931.13
SLOPEi,t
88,634
0.02
0.08
-1.81
1.20
SLOPEB
i,t
88,634
0.03
0.31
0.00
67.87
SLOPEA
i,t
90,665
0.03
0.36
-0.05
84.77
DEPTHB
i,t
90,665
1.15
4.18
0.00
321.91
DEPTHA
i,t
90,665
1.08
5.25
-4.44
927.30
TVi,t is the logarithm of the U.S. dollar denominated total volume of trades for cryptocurrency i in time interval t. Buy-
Sell imbalance is the absolute difference between buyer- and seller-initiated trades in time interval t for cryptocurrency i,
i.e., BSIi,t = |Bi,t −Si,t| where Bi,t (Si,t) is the number of buyer-initiated (seller-initiated) trades in the time interval t
for cryptocurrency i. Market toxicity is defined as MTi,t =
BSIi,t
(Bi,t+Si,t). Return is defined as Ri,t = log(Pi,t/Pi,t−1) where
Pi,t is the last price in time interval t for cryptocurrency i.
ILLIQi,t is a measure of cryptocurrency illiquidity for time
interval t with the ratio of absolute stock return to the total trading volume defined as ILLIQi,t =
|Ri,t|
T Vi,t . σR
i,t is defined
as the standard deviation of returns of the transactions in interval t for cryptocurrency i. ASCGH, ASCHS2, ASCMRR are
three measures for the adverse selection component of the spread for all cryptocurrencies in our sample for all of the selected
frequencies computed using the seminal works of Glosten and Harris (1988), Huang and Stoll (1997), and Madhavan et al.
(1997), respectively. ASCHS3 denotes the adverse selection costs computed with the three-way decomposition of the Huang
and Stoll (1997) framework. OPCGH
i,t , OPCHS2
i,t
, OPCHS3
i,t
, OPCMRR
i,t
are the transitory components of price changes related
with the order processing costs (OPC) defined in the related paper as above. ICHS3
i,t
is the inventory holding costs (IC) (in the
case of Huang and Stoll (1997)) component of the price changes. SPREADi,t is the average value of the difference between
the best ask and bid price at each time tick in the time interval t for cryptocurrency i. DEPTHi,t is the average of the average
volume waiting at the best bid and ask levels at each time tick in the time interval t for cryptocurrency i. SLOPEi,t denotes the
marginal liquidity cost as in Amaya et al. (2018). SLOPEB
i,t (SLOPEA
i,t) is the order-book slope computed from the bid-side
(ask-side) of the order book. DEPTHB
i,t (DEPTHA
i,t) is the average volume waiting at the best bid (ask) level at each time
tick in the time interval t for cryptocurrency i.
30


### Page 31

Table 2: This table presents the pairwise correlations for our variables calculated over a time interval of 60 minutes. For our panel analysis,
we restrict our sample to the period between August 2017 and June 2018 in order to provide a substantial sample of cryptocurrencies
upon which the market could trade, therefore providing a strong sample to analyse. †, ‡, * indicate statistical significance at 1%, 5% and
10% level, respectively.
T Vi,t
BSIi,t
MTi,t
Ri,t
ILLIQi,t
σR
i,t
ASCGH
i,t
ASCHS2
i,t
ASCHS3
i,t
ASCMRR
i,t
OP CGH
i,t
OP CHS2
i,t
OP CHS3
i,t
ICHS3
i,t
SP READi,t
DEP T Hi,t
BSIi,t
0.16†
MTi,t
-0.15†
0.26†
Ri,t
0.01
-0.03†
-0.04†
ILLIQi,t
0.00
0.23†
0.04†
0.06†
σR
i,t
0.34†
0.27†
-0.10†
0.03†
0.71†
ASCGH
i,t
-0.53†
0.10†
-0.09†
-0.00
0.14†
-0.01*
ASCHS2
i,t
-0.53†
0.10†
-0.09†
-0.01
0.14†
-0.01*
1.00†
ASCHS3
i,t
-0.50†
-0.00
-0.02‡
-0.01
0.14†
-0.01
0.75†
0.75†
ASCMRR
i,t
-0.53†
0.10†
-0.09†
-0.01
0.14†
-0.01*
1.00†
1.00†
0.75†
OP CGH
i,t
-0.30†
0.24†
-0.10†
-0.01*
0.21†
0.13†
0.68†
0.69†
0.56†
0.69†
OP CHS2
i,t
-0.30†
0.24†
-0.10†
-0.01*
0.22†
0.14†
0.68†
0.68†
0.56†
0.68†
1.00†
OP CHS3
i,t
-0.35†
0.20†
-0.09†
-0.02
0.22†
0.11†
0.72†
0.72†
0.54†
0.72†
1.00†
1.00†
ICHS3
i,t
-0.50†
0.03†
-0.06†
-0.01
0.15†
-0.00
0.89†
0.89†
0.38†
0.89†
0.63†
0.62†
0.62†
SP READi,t
-0.14†
0.04†
-0.03†
-0.00
0.05†
0.01‡
0.23†
0.23†
0.23†
0.23†
0.23†
0.23†
0.29†
0.26†
DEP T Hi,t
0.44†
-0.01†
-0.03†
0.00
-0.08†
0.03†
-0.18†
-0.18†
-0.12†
-0.18†
-0.13†
-0.13†
-0.11†
-0.13†
-0.05†
SLOP Ei,t
-0.20†
0.27†
-0.11†
-0.00
0.04 †
-0.02†
0.64†
0.64†
0.38†
0.64†
0.67†
0.67†
0.67†
0.54†
0.20†
-0.08†
31


### Page 32

Table 3: Spread decomposition-(Glosten and Harris, 1988): This table presents the adverse selection
components of the spread estimated using the Glosten and Harris (1988) framework. We estimate
the equation ∆P = z0Qt +z1QtVt +c0(∆Qt)+c1(∆QtVt)+ϵt using the limit order book of Bitfinex
for all cryptocurrencies in our sample with ordinary least squares. The component of the spread
that is attributed to adverse selection is given by ASCGH
t
= 2 ∗( ˆz0 + ˆz1Vt). and the component
of the spread attributed to order-processing costs is given by(OPCGH
t
= 2 ∗( ˆc0 + ˆc1Vt).
The
second column is designated for the mean of the transitory component OPCGH
t
throughout the
sample period. Third column provides p-value for the test with the null hypothesis that transitory
component is equal to zero. The fourth column and fifth columns are designated for the mean of
the adverse selection component of the spread (ASCGH
t
) and the corresponding p-value for the test
with the null hypothesis that adverse selection component is equal to zero. The last column gives
ratio of adverse selection costs overall traded spread (ASCt/(OPCt + ASCt)).
Transitory Comp. (OPCGH)
Adverse Selection Comp. (ASCGH)
Currency
Coefficient
p-value
Coefficient
p-value
% ASC
BCH
1.8121
(0.00)
0.1509
(0.00)
8%
BTC
3.0157
(0.00)
0.2172
(0.00)
7%
DSH
1.0203
(0.00)
0.1268
(0.00)
11%
EOS
0.0090
(0.00)
0.0010
(0.00)
10%
ETC
0.0293
(0.00)
0.0033
(0.00)
10%
ETH
0.2702
(0.00)
0.0272
(0.00)
9%
IOT
0.0037
(0.00)
0.0003
(0.00)
7%
LTC
0.1490
(0.00)
0.0142
(0.00)
9%
OMG
0.0223
(0.00)
0.0026
(0.00)
10%
XMR
0.3777
(0.00)
0.0547
(0.00)
13%
XRP
0.0013
(0.00)
0.0001
(0.00)
7%
ZEC
0.6813
(0.00)
0.0807
(0.00)
11%
32


### Page 33

Table 4: Two-way spread decomposition - (Huang and Stoll, 1997): This table presents the adverse
selection component of the spread estimated using the two-way decomposition of the Huang and
Stoll (1997) framework. We estimate the equation ∆Pt = λ ν
2Qt−1 + ν
2(∆Qt) + ϵt using the limit
order book of Bitfinex for all cryptocurrencies in our sample.
The second column presents the
traded spread (ν).
The third column corresponds to the ordinary least squares standard error
of the estimates of traded spread.
The fourth and fifth columns present the estimates for the
component of the spread attributed to the adverse selection (ASC) and inventory costs (IC) (λ ∗ν
2)
and corresponding ordinary least squares standard errors, respectively. The last column represents
the proportion of the spread that is attributed to the adverse selection and inventory costs (λ).
Traded Spread (ν)
ASCHS + ICHS (λ * ν)
Currency
Coefficient
Standard Error
Coefficient
Standard Error
λ
BCH
1.9602
(0.0012)
0.1510
(0.0011)
8%
BTC
3.2237
(0.0013)
0.2176
(0.0014)
7%
DSH
1.1445
(0.0011)
0.1269
(0.0009)
11%
EOS
0.0100
(0.0000)
0.0010
(0.0000)
10%
ETC
0.0325
(0.0000)
0.0033
(0.0000)
10%
ETH
0.2968
(0.0002)
0.0272
(0.0002)
9%
IOT
0.0039
(0.0000)
0.0003
(0.0000)
7%
LTC
0.1630
(0.0001)
0.0142
(0.0001)
9%
OMG
0.0249
(0.0000)
0.0026
(0.0000)
10%
XMR
0.7610
(0.0007)
0.0808
(0.0006)
11%
XRP
0.0014
(0.0000)
0.0001
(0.0000)
7%
ZEC
0.7610
(0.0007)
0.0808
(0.0006)
11%
33


### Page 34

Table 5: Spread decomposition - (Madhavan et al., 1997): This table presents the adverse selection
component of the spread estimated using the two-way decomposition of the Madhavan et al. (1997)
framework. We estimate the equation ∆Pt = (ϕ + θ)Qt −ϕQt−1 + ϵt using the limit order book of
Bitfinex for all cryptocurrencies in our sample. The component of the spread that is attributed to
adverse selection is given by ASCMRR = 2 ∗(ˆθ). and the component of the spread attributed to
order-processing costs is given by (OPCMRR = 2 ∗(ˆϕ). The second column is designated for the
mean of the transitory component OPCMRR
t
throughout the sample period. Third column provides
ordinary least squares standard errors for the OPC estimate. The fourth column and fifth columns
are designated for the mean of the adverse selection component of the spread (ASCMRR) and the
corresponding ordinary least squares standard error for the ASC estimate. The last column gives
ratio of adverse selection costs overall traded spread (ASCMRR/(OPCMRR + ASCMRR)).
Order Processing Costs (OPCMRR)
Adverse Sel. Costs (ASCMRR)
Currency
Coefficient
Std. Error
Coefficient
Std. Error
% ASC
BCH
1.8091
(0.0012)
0.1510
(0.0011)
8%
BTC
3.0061
(0.0013)
0.2176
(0.0014)
7%
DSH
1.0176
(0.0011)
0.1269
(0.0009)
11%
EOS
0.0090
(0.0000)
0.0010
(0.0000)
10%
ETC
0.0292
(0.0000)
0.0033
(0.0000)
10%
ETH
0.2696
(0.0002)
0.0272
(0.0002)
9%
IOT
0.0037
(0.0000)
0.0003
(0.0000)
7%
LTC
0.1488
(0.0001)
0.0142
(0.0001)
9%
OMG
0.0223
(0.0000)
0.0026
(0.0000)
10%
XMR
0.3770
(0.0005)
0.0547
(0.0005)
13%
XRP
0.0013
(0.0000)
0.0001
(0.0000)
7%
ZEC
0.6801
(0.0007)
0.0808
(0.0006)
11%
34


### Page 35

Table 6: Three-way spread decomposition - (Huang and Stoll, 1997): This table presents the adverse selection component of the spread
estimated using the three-way decomposition of the Huang and Stoll (1997) framework. We estimate the equation ∆Pt = ν
2Qt + (α + β −
1)ν
2Qt−1 −α ν
2(1 −2π)Qt−2 + ϵt using the limit order book of Bitfinex for all cryptocurrencies in our sample. The second column presents
the traded spread (ν). The third column corresponds to the ordinary least squares standard error of the estimates of traded spread. The
fourth and fifth columns present the estimates for the proportion of spread due to the inventory holding costs ( ˆβ) and the corresponding
ordinary least squares standard error. The sixth and seventh columns present the estimates for the proportion of the spread attributed
to the adverse selection costs (ˆα) and corresponding ordinary least squares standard error, respectively. The last column represents the
serial correlation in the trade-flow (π).
Traded Spread (ν)
(%IC = β)
(%ASC = α)
Currency
Coefficient
Standard Error
Coefficient
Standard Error
Coefficient
Standard Error
π
BCH
1.9433
(0.0012)
0.1327
(0.0013)
-0.0828
(0.0022)
0.2324
BTC
3.1901
(0.0013)
0.1589
(0.0014)
-0.1180
(0.0031)
0.2880
DSH
1.1413
(0.0011)
0.1256
(0.0012)
-0.0249
(0.0018)
0.1930
EOS
0.0099
(0.0000)
0.1342
(0.0000)
-0.0554
(0.0000)
0.2103
ETC
0.0323
(0.0000)
0.1239
(0.0000)
-0.0377
(0.0000)
0.2057
ETH
0.2938
(0.0002)
0.1539
(0.0002)
-0.0901
(0.0003)
0.2420
IOT
0.0039
(0.0000)
0.1136
(0.0000)
-0.0771
(0.0000)
0.2137
LTC
0.1615
(0.0001)
0.1487
(0.0001)
-0.0898
(0.0002)
0.2378
OMG
0.0248
(0.0000)
0.1100
(0.0000)
-0.0117
(0.0000)
0.1871
XMR
0.4309
(0.0005)
0.1376
(0.0006)
-0.0181
(0.0009)
0.1951
XRP
0.0014
(0.0000)
0.1386
(0.0000)
-0.1009
(0.0000)
0.2534
ZEC
0.7597
(0.0007)
0.1153
(0.0008)
-0.0152
(0.0012)
0.1950
35


### Page 36

Table 7: This table presents the results of the following regression: σR
i,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 + γ4BSIi,t−1 +
γ5MTi,t−1 +γ6ASCk
i,t−1 +γ7OPCk
i,t−1 +γ8ICk
i,t−1 +ϵi,t. We restrict our sample to the period between August 2017 and June 2018 in order
to provide a substantial sample of cryptocurrencies upon which the market could trade, therefore providing a strong sample to analyse.
Panel A, B, C present the results of the estimation for time intervals set to 1 minute, 15 minutes and 60 minutes, respectively. Respective
columns in each panel are for the regressions where the components of the spread ASCk, OPCk are obtained by Glosten and Harris (1988)
(k = GH), two-way decomposition of Huang and Stoll (1997)(k = HS2 −way), Madhavan et al. (1997) (k = MRR), and three-way
decomposition of Huang and Stoll (1997)(k = HS3 −way). Inventory costs (IC) are obtained only by the three-way decomposition of
Huang and Stoll (1997). We require at least 30 trades within the time interval t, to estimate the adverse selection component in that
interval. Absolute value of the t-statistics are in parenthesis. Hypothesis 1 asserts a relationship γ6 ̸= 0. ***, **, * indicates statistical
significance at 1%, 5% and 10%, respectively.
Panel A: 1 min
Panel B: 15 min
Panel C: 60 min
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
σR
i,t−1
0.48698
0.48077
0.48058
0.42513
0.50480
0.50453
0.50458
0.50203
0.40922
0.40929
0.40929
0.38369
(372.442)***
(349.171)***
(348.493)***
(117.331)***
(253.318)***
(253.637)***
(253.673)***
(124.736)***
(108.081)***
(108.164)***
(108.165)***
(55.291)***
SP READi,t−1
0.00000
0.00000
0.00000
0.00000
0.00000
0.00000
0.00000
-0.00000
0.00002
0.00002
0.00002
0.00003
(1.724)*
(1.811)*
(1.810)*
(2.039)**
(1.421)
(1.460)
(1.459)
(0.289)
(2.881)***
(2.860)***
(2.860)***
(1.647)*
T Vi,t−1
0.00009
0.00009
0.00009
0.00011
0.00029
0.00029
0.00029
0.00030
0.00081
0.00081
0.00081
0.00094
(36.120)***
(38.036)***
(37.979)***
(16.643)***
(46.369)***
(46.619)***
(46.578)***
(24.638)***
(39.400)***
(39.366)***
(39.367)***
(23.829)***
BSIi,t−1
-0.00000
-0.00000
-0.00000
-0.00000
0.00000
0.00000
0.00000
0.00000
0.00000
0.00000
0.00000
0.00000
(11.608)***
(10.970)***
(11.060)***
(6.516)***
(24.149)***
(24.109)***
(24.102)***
(13.652)***
(5.906)***
(5.947)***
(5.947)***
(3.878)***
MTi,t−1
-0.00014
-0.00013
-0.00013
-0.00006
-0.00072
-0.00072
-0.00072
-0.00075
-0.00102
-0.00102
-0.00102
-0.00112
(12.917)***
(12.960)***
(12.711)***
(2.115)**
(22.225)***
(22.367)***
(22.365)***
(12.318)***
(8.358)***
(8.340)***
(8.342)***
(4.942)***
ASCi,t−1
-0.00002
0.00073
0.00479
(2.655)***
(9.614)***
(14.027)***
OP Ci,t−1
0.00002
0.00019
0.00036
(15.932)***
(25.041)***
(12.731)***
ASCi,t−1
-0.00002
0.00073
0.00486
(2.541)**
(9.629)***
(14.225)***
OP Ci,t−1
0.00002
0.00019
0.00036
(16.982)***
(25.168)***
(12.709)***
ASCi,t−1
-0.00002
0.00073
0.00486
(2.529)**
(9.632)***
(14.225)***
OP Ci,t−1
0.00002
0.00019
0.00036
(17.011)***
(25.173)***
(12.708)***
ASCi,t−1
-0.00013
0.00036
0.00121
(5.738)***
(2.454)**
(1.748)*
OP Ci,t−1
0.00004
0.00026
0.00048
(10.020)***
(13.625)***
(6.854)***
ICi,t−1
-0.00005
0.00046
0.00460
(1.686)*
(2.501)**
(5.804)***
Intercept
0.00062
0.00061
0.00061
0.00057
-0.00022
-0.00023
-0.00022
-0.00032
-0.00290
-0.00289
-0.00289
-0.00357
(45.731)***
(44.950)***
(44.816)***
(15.562)***
(5.419)***
(5.454)***
(5.420)***
(3.826)***
(18.036)***
(18.033)***
(18.033)***
(11.371)***
R2
0.38
0.37
0.37
0.33
0.39
0.39
0.39
0.40
0.33
0.33
0.33
0.30
Currency and Time FE
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
N
488,796
494,244
493,641
74,528
254,801
255,657
255,660
65,729
83,808
83,941
83,942
27,231
36


### Page 37

Table 8: This table presents the results of the following regression: ILLIQi,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 +
γ4BSIi,t−1 + γ5MTi,t−1 + γ6ASCk
i,t−1 + γ7OPCk
i,t−1 + γ8ICk
i,t−1 + ϵi,t. We restrict our sample to the period between August 2017 and
June 2018 in order to provide a substantial sample of cryptocurrencies upon which the market could trade, therefore providing a strong
sample to analyse. Panels A, B, C present the results of the estimation for time intervals set to 1 minute, 15 minutes and 60 minutes,
respectively. Respective columns in each panel are for the regressions where the components of the spread ASCk, OPCk are obtained
by Glosten and Harris (1988) (k = GH), two-way decomposition of Huang and Stoll (1997)(k = HS2 −way), Madhavan et al. (1997)
(k = MRR), and three-way decomposition of Huang and Stoll (1997)(k = HS3 −way). Inventory costs (IC) are obtained only by the
three-way decomposition of Huang and Stoll (1997). We require at least 30 trades within the time interval t, to estimate the adverse
selection component in that interval. Absolute value of the t-statistics are in parenthesis. Hypothesis 2 asserts a relationship γ6 > 0. ***,
**, * indicates statistical significance at 1%, 5% and 10%, respectively.
Panel A: 1 min
Panel B: 15 min
Panel C: 60 min
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
σR
i,t−1
0.08964
0.09774
0.09767
0.07919
0.08141
0.08144
0.08145
0.08643
0.05953
0.05951
0.05951
0.05501
(133.481)***
(163.046)***
(162.767)***
(65.893)***
(129.541)***
(129.789)***
(129.816)***
(63.835)***
(54.241)***
(54.242)***
(54.242)***
(28.061)***
SP READi,t−1
0.00000
0.00000
0.00000
0.00000
0.00000
0.00000
0.00000
-0.00000
0.00001
0.00001
0.00001
0.00001
(1.687)*
(2.159)**
(2.158)**
(0.405)
(2.453)**
(2.489)**
(2.487)**
(0.444)
(4.554)***
(4.527)***
(4.527)***
(2.840)***
T Vi,t−1
0.00001
0.00001
0.00001
0.00001
0.00004
0.00004
0.00004
0.00003
0.00011
0.00011
0.00011
0.00012
(10.248)***
(10.564)***
(10.402)***
(6.174)***
(20.233)***
(20.111)***
(20.073)***
(7.702)***
(17.957)***
(18.079)***
(18.081)***
(11.255)***
BSIi,t−1
0.00000
0.00000
0.00000
-0.00000
0.00000
0.00000
0.00000
0.00000
-0.00000
-0.00000
-0.00000
-0.00000
(2.797)***
(0.597)
(0.590)
(1.387)
(4.901)***
(4.897)***
(4.896)***
(3.589)***
(0.840)
(0.897)
(0.895)
(0.220)
MTi,t−1
-0.00008
-0.00007
-0.00007
-0.00005
-0.00015
-0.00015
-0.00015
-0.00016
-0.00020
-0.00019
-0.00019
-0.00022
(13.999)***
(14.753)***
(14.520)***
(5.398)***
(14.957)***
(15.106)***
(15.120)***
(7.867)***
(5.563)***
(5.489)***
(5.495)***
(3.410)***
ASCi,t−1
0.00007
0.00062
0.00197
(17.204)***
(25.824)***
(19.876)***
OP Ci,t−1
0.00002
0.00010
0.00014
(39.195)***
(41.993)***
(17.169)***
ASCi,t−1
0.00007
0.00062
0.00201
(19.621)***
(26.027)***
(20.260)***
OP Ci,t−1
0.00002
0.00010
0.00014
(44.854)***
(42.044)***
(17.043)***
ASCi,t−1
0.00007
0.00062
0.00201
(19.587)***
(26.045)***
(20.260)***
OP Ci,t−1
0.00002
0.00010
0.00014
(44.851)***
(42.047)***
(17.042)***
ASCi,t−1
0.00002
0.00042
0.00056
(3.133)***
(8.480)***
(2.865)***
OP Ci,t−1
0.00003
0.00013
0.00019
(22.461)***
(19.610)***
(9.587)***
ICi,t−1
0.00005
0.00057
0.00202
(4.568)***
(9.164)***
(9.037)***
Intercept
0.00053
0.00053
0.00053
0.00052
0.00044
0.00044
0.00044
0.00044
0.00017
0.00016
0.00016
0.00007
(76.284)***
(89.109)***
(89.082)***
(42.815)***
(33.504)***
(33.828)***
(33.859)***
(15.833)***
(3.746)***
(3.528)***
(3.528)***
(0.777)
R2
0.10
0.13
0.13
0.18
0.21
0.21
0.21
0.21
0.15
0.15
0.15
0.14
Currency and Time FE
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
N
488,796
494,244
493,641
74,528
254,801
255,657
255,660
65,729
83,808
83,941
83,942
27,231
37


### Page 38

Table 9: This table presents the results of the following regression: SPREADi,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 +
γ4BSIi,t−1 + γ5MTi,t−1 + γ6ASCk
i,t−1 + γ7OPCk
i,t−1 + γ8ICk
i,t−1 + ϵi,t. We restrict our sample to the period between August 2017 and
June 2018 in order to provide a substantial sample of cryptocurrencies upon which the market could trade, therefore providing a strong
sample to analyse. Panels A, B, C present the results of the estimation for time intervals set to 1 minute, 15 minutes and 60 minutes,
respectively. Respective columns in each panel are for the regressions where the components of the spread ASCk, OPCk are obtained
by Glosten and Harris (1988) (k = GH), two-way decomposition of Huang and Stoll (1997)(k = HS2 −way), Madhavan et al. (1997)
(k = MRR), and three-way decomposition of Huang and Stoll (1997)(k = HS3 −way). Inventory costs (IC) are obtained only by the
three-way decomposition of Huang and Stoll (1997). We require at least 30 trades within the time interval t, to estimate the adverse
selection component in that interval. Absolute value of the t-statistics are in parenthesis. Hypothesis 2 asserts a relationship γ6 > 0. ***,
**, * indicates statistical significance at 1% , 5% and 10%, respectively.
Panel A: 1 min
Panel B: 15 min
Panel C: 60 min
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
σR
i,t−1
-7.14630
-9.89233
-9.69756
-10.23819
-6.23575
-6.50632
-6.50551
-8.01543
-0.65937
-0.72521
-0.72510
-4.21980
(1.418)
(2.084)**
(2.041)**
(0.992)
(3.446)***
(3.601)***
(3.600)***
(6.080)***
(0.328)
(0.362)
(0.361)
(1.105)
SP READi,t−1
0.04029
0.02879
0.02879
0.04116
0.15638
0.14924
0.14924
0.03622
0.11915
0.11911
0.11911
0.08353
(90.066)***
(71.123)***
(71.082)***
(13.557)***
(142.293)***
(139.030)***
(139.030)***
(61.590)***
(33.623)***
(33.640)***
(33.640)***
(6.183)***
T Vi,t−1
-0.05542
-0.05581
-0.05617
-0.05333
0.01660
0.01729
0.01729
0.00724
0.03342
0.03393
0.03393
0.03301
(6.679)***
(7.505)***
(7.538)***
(3.249)***
(2.996)***
(3.131)***
(3.130)***
(1.840)*
(3.067)***
(3.121)***
(3.121)***
(1.535)
BSIi,t−1
0.00078
0.00067
0.00067
0.00016
-0.00004
-0.00004
-0.00004
0.00002
-0.00011
-0.00011
-0.00011
-0.00011
(2.750)***
(2.613)***
(2.619)***
(0.293)
(0.892)
(0.882)
(0.883)
(0.591)
(3.210)***
(3.225)***
(3.225)***
(1.538)
MTi,t−1
-0.29098
-0.29426
-0.29556
-0.17769
-0.07462
-0.07908
-0.07904
-0.05212
0.03663
0.03944
0.03948
0.04746
(8.257)***
(9.325)***
(9.345)***
(2.578)***
(2.659)***
(2.834)***
(2.832)***
(2.717)***
(0.566)
(0.612)
(0.613)
(0.384)
ASCi,t−1
0.81441
1.30285
1.83279
(26.634)***
(19.480)***
(10.153)***
OP Ci,t−1
0.20734
0.37355
0.40139
(43.123)***
(55.201)***
(27.131)***
ASCi,t−1
0.86141
1.33118
1.87330
(30.746)***
(19.864)***
(10.374)***
OP Ci,t−1
0.21154
0.37860
0.40133
(48.258)***
(55.710)***
(27.038)***
ASCi,t−1
0.86298
1.33102
1.87330
(30.777)***
(19.861)***
(10.374)***
OP Ci,t−1
0.21149
0.37860
0.40133
(48.215)***
(55.709)***
(27.039)***
ASCi,t−1
0.58330
1.16307
1.34870
(8.782)***
(24.741)***
(3.561)***
OP Ci,t−1
0.22079
0.51667
0.40821
(16.674)***
(82.025)***
(10.631)***
ICi,t−1
0.97141
1.57113
1.86441
(11.174)***
(26.502)***
(4.278)***
Intercept
1.65253
1.62457
1.62499
1.44865
0.57804
0.57946
0.57951
0.54301
0.34862
0.34129
0.34129
0.36344
(35.897)***
(39.360)***
(39.313)***
(15.682)***
(15.836)***
(15.919)***
(15.920)***
(20.519)***
(4.105)***
(4.028)***
(4.028)***
(2.115)**
R2
0.04
0.04
0.04
0.04
0.14
0.14
0.14
0.42
0.08
0.08
0.08
0.06
Currency and Time FE
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
N
672,571
681,234
680,260
107,413
267,512
268,488
268,486
68,732
84,020
84,153
84,154
27,257
38


### Page 39

Table 10: This table presents the results of the following regression: SLOPEi,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 +
γ4BSIi,t−1 + γ5MTi,t−1 + γ6ASCk
i,t−1 + γ7OPCk
i,t−1 + γ8ICk
i,t−1 + ϵi,t. We restrict our sample to the period between August 2017 and
June 2018 in order to provide a substantial sample of cryptocurrencies upon which the market could trade, therefore providing a strong
sample to analyse. Panels A, B, C present the results of the estimation for time intervals set to 1 minute, 15 minutes and 60 minutes,
respectively. Respective columns in each panel are for the regressions where the components of the spread ASCk, OPCk are obtained
by Glosten and Harris (1988) (k = GH), two-way decomposition of Huang and Stoll (1997)(k = HS2 −way), Madhavan et al. (1997)
(k = MRR), and three-way decomposition of Huang and Stoll (1997)(k = HS3 −way). Inventory costs (IC) are obtained only by the
three-way decomposition of Huang and Stoll (1997). We require at least 30 trades within the time interval t, to estimate the adverse
selection component in that interval. Absolute value of the t-statistics are in parenthesis. Hypothesis 2 asserts a relationship γ6 > 0. ***,
**, * indicates statistical significance at 1% , 5% and 10%, respectively.
Panel A: 1 min
Panel B: 15 min
Panel C: 60 min
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
σR
i,t−1
-1.98957
-2.20153
-2.18742
-2.56028
-1.44026
-1.44901
-1.44884
-1.48281
-0.95672
-0.95870
-0.95870
-0.69982
(24.780)***
(26.475)***
(26.276)***
(14.365)***
(37.533)***
(37.886)***
(37.882)***
(21.709)***
(25.806)***
(25.880)***
(25.880)***
(14.527)***
SP READi,t−1
0.00020
0.00020
0.00020
0.00102
0.00043
0.00041
0.00041
0.00009
0.00098
0.00098
0.00098
0.00285
(29.113)***
(29.347)***
(29.319)***
(26.163)***
(18.593)***
(17.841)***
(17.841)***
(2.838)***
(15.020)***
(15.014)***
(15.014)***
(16.744)***
T Vi,t−1
-0.00751
-0.00717
-0.00721
-0.00563
0.00099
0.00103
0.00103
0.00113
0.00145
0.00146
0.00146
-0.00035
(56.803)***
(55.010)***
(55.223)***
(19.866)***
(8.410)***
(8.834)***
(8.822)***
(5.521)***
(7.213)***
(7.287)***
(7.287)***
(1.289)
BSIi,t−1
0.00015
0.00014
0.00015
0.00011
0.00003
0.00003
0.00003
0.00002
0.00001
0.00001
0.00001
0.00001
(33.101)***
(32.325)***
(32.454)***
(12.501)***
(31.270)***
(31.156)***
(31.165)***
(14.479)***
(16.284)***
(16.353)***
(16.353)***
(15.163)***
MTi,t−1
-0.03037
-0.02938
-0.02951
-0.02394
-0.00960
-0.00929
-0.00931
-0.00691
-0.00226
-0.00215
-0.00215
-0.00329
(54.087)***
(53.152)***
(53.264)***
(20.121)***
(16.142)***
(15.733)***
(15.751)***
(6.948)***
(1.895)*
(1.805)*
(1.805)*
(2.106)**
ASCi,t−1
0.08406
0.20745
0.32489
(172.538)***
(146.278)***
(97.486)***
OP Ci,t−1
0.01759
0.02728
0.03150
(229.595)***
(190.142)***
(115.319)***
ASCi,t−1
0.08726
0.21040
0.32807
(177.787)***
(148.323)***
(98.390)***
OP Ci,t−1
0.01772
0.02723
0.03136
(230.805)***
(189.279)***
(114.401)***
ASCi,t−1
0.08726
0.21042
0.32807
(177.639)***
(148.336)***
(98.391)***
OP Ci,t−1
0.01772
0.02723
0.03136
(230.588)***
(189.280)***
(114.402)***
ASCi,t−1
0.05506
0.10920
0.10659
(48.028)***
(44.834)***
(22.304)***
OP Ci,t−1
0.01855
0.03198
0.03190
(81.225)***
(97.989)***
(65.831)***
ICi,t−1
0.07988
0.19354
0.26291
(53.250)***
(63.011)***
(47.803)***
Intercept
0.02671
0.02508
0.02521
0.01150
-0.02873
-0.02916
-0.02915
-0.03249
-0.04985
-0.05015
-0.05015
-0.02832
(36.418)***
(34.688)***
(34.819)***
(7.214)***
(37.117)***
(37.840)***
(37.836)***
(23.698)***
(31.800)***
(32.049)***
(32.049)***
(13.057)***
R2
0.55
0.55
0.55
0.56
0.65
0.65
0.65
0.65
0.70
0.70
0.70
0.65
Currency and Time FE
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
N
672,587
681,249
680,275
107,416
267,513
268,489
268,487
68,732
84,022
84,155
84,156
27,259
39


### Page 40

Table 11: This table presents the results of the following regression: DEPTHi,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 +
γ4BSIi,t−1 + γ5MTi,t−1 + γ6ASCk
i,t−1 + γ7OPCk
i,t−1 + γ8ICk
i,t−1 + ϵi,t. We restrict our sample to the period between August 2017 and
June 2018 in order to provide a substantial sample of cryptocurrencies upon which the market could trade, therefore providing a strong
sample to analyse. Panels A, B, C present the results of the estimation for time intervals set to 1 minute, 15 minutes and 60 minutes,
respectively. Respective columns in each panel are for the regressions where the components of the spread ASCk, OPCk are obtained
by Glosten and Harris (1988) (k = GH), two-way decomposition of Huang and Stoll (1997)(k = HS2 −way), Madhavan et al. (1997)
(k = MRR), and three-way decomposition of Huang and Stoll (1997)(k = HS3 −way). Inventory costs (IC) are obtained only by the
three-way decomposition of Huang and Stoll (1997). We require at least 30 trades within the time interval t, to estimate the adverse
selection component in that interval. Absolute value of the t-statistics are in parenthesis. Hypothesis 2 asserts a relationship γ6 < 0. ***,
**, * indicates statistical significance at 1% , 5% and 10%, respectively.
Panel A: 1 min
Panel B: 15 min
Panel C: 60 min
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
σR
i,t−1
86.22129
98.01745
98.11543
64.51725
27.94706
27.99134
28.01963
32.10648
9.66891
9.64908
9.64745
-3.10909
(3.251)***
(3.598)**
(3.597)**
(0.589)
(4.068)***
(4.070)**
(4.075)**
(3.169)**
(1.941)*
(1.939)
(1.939)
(0.271)
SP READi,t−1
0.00019
0.00020
0.00020
0.00197
0.00012
0.00008
0.00008
0.00016
-0.00042
-0.00043
-0.00043
-0.00115
(0.082)
(0.087)
(0.087)
(0.083)
(0.029)
(0.019)
(0.019)
(0.035)
(0.051)
(0.052)
(0.052)
(0.044)
T Vi,t−1
0.31264
0.29761
0.29852
0.45269
0.15594
0.15577
0.15552
0.17919
0.06733
0.06838
0.06840
0.23972
(7.160)***
(6.974)**
(6.981)**
(2.600)**
(7.411)***
(7.410)**
(7.399)**
(5.924)**
(2.492)**
(2.538)*
(2.538)*
(3.706)**
BSIi,t−1
-0.00754
-0.00734
-0.00731
-0.00554
-0.00221
-0.00222
-0.00222
-0.00256
-0.00068
-0.00068
-0.00068
-0.00088
(5.037)***
(5.003)**
(4.973)**
(0.987)
(12.470)***
(12.540)**
(12.530)**
(10.036)**
(8.167)***
(8.216)**
(8.215)**
(3.966)**
MTi,t−1
0.93103
0.91154
0.90560
1.30560
1.66435
1.67457
1.67251
1.68999
1.77852
1.77608
1.77554
1.58885
(5.020)***
(5.034)**
(4.989)**
(1.786)
(15.621)***
(15.765)**
(15.742)**
(11.463)**
(11.094)***
(11.124)**
(11.122)**
(4.268)**
ASCi,t−1
0.03054
0.11330
0.28920
(0.190)
(0.446)
(0.646)
OP Ci,t−1
-0.01558
0.02061
0.03663
(0.616)
(0.802)
(0.999)
ASCi,t−1
0.02222
0.12035
0.29729
(0.138)
(0.472)
(0.664)
OP Ci,t−1
-0.01650
0.02113
0.03631
(0.657)
(0.816)
(0.987)
ASCi,t−1
0.02294
0.11953
0.29726
(0.143)
(0.468)
(0.664)
OP Ci,t−1
-0.01678
0.02108
0.03629
(0.667)
(0.814)
(0.986)
ASCi,t−1
0.00215
0.15139
0.46548
(0.003)
(0.419)
(0.409)
OP Ci,t−1
-0.00579
0.02290
0.01070
(0.041)
(0.473)
(0.093)
ICi,t−1
-0.09961
0.17124
0.72738
(0.108)
(0.376)
(0.555)
Intercept
-1.68967
-1.63367
-1.63620
-2.51826
-1.25120
-1.25400
-1.25206
-1.41618
-0.77345
-0.78051
-0.78054
-1.91975
(6.976)***
(6.899)**
(6.899)**
(2.572)*
(9.026)***
(9.050)**
(9.036)**
(6.964)**
(3.674)***
(3.716)**
(3.716)**
(3.715)**
R2
0.03
0.03
0.03
0.01
0.26
0.26
0.26
0.41
0.43
0.43
0.43
0.29
Currency and Time FE
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
N
674,322
683,001
682,030
107,673
267,925
268,902
268,901
68,839
84,318
84,451
84,452
27,357
40


### Page 41

Table 12: This table presents the results of the following regression: SLOPEB
i,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 +
γ4BSIi,t−1 + γ5MTi,t−1 + γ6ASCk
i,t−1 + γ7OPCk
i,t−1 + γ8ICk
i,t−1 + ϵi,t. We restrict our sample to the period between August 2017 and
June 2018 in order to provide a substantial sample of cryptocurrencies upon which the market could trade, therefore providing a strong
sample to analyse. Panel A, B, C present the results of the estimation for time intervals set to 1 minute, 15 minutes and 60 minutes,
respectively. Respective columns in each panel are for the regressions where the components of the spread ASCk, OPCk are obtained
by Glosten and Harris (1988) (k = GH), two-way decomposition of Huang and Stoll (1997)(k = HS2 −way), Madhavan et al. (1997)
(k = MRR), and three-way decomposition of Huang and Stoll (1997)(k = HS3 −way). Inventory costs (IC) are obtained only by the
three-way decomposition of Huang and Stoll (1997). We require at least 30 trades within the time interval t, to estimate the adverse
selection component in that interval. Absolute value of the t-statistics are in parenthesis. Hypothesis 2 asserts a relationship γ6 > 0. ***,
**, * indicates statistical significance at 1% , 5% and 10%, respectively.
Panel A: 1 min
Panel B: 15 min
Panel C: 60 min
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
σR
i,t−1
-2.47912
-2.74319
-2.72787
-2.90544
-1.39144
-1.38521
-1.38520
-1.21207
-0.86384
-0.86934
-0.86934
-0.48268
(12.704)***
(13.566)***
(13.474)***
(14.142)***
(4.138)***
(4.133)***
(4.133)***
(2.665)***
(3.681)***
(3.708)***
(3.708)***
(1.335)
SP READi,t−1
0.00022
0.00022
0.00022
0.00106
0.00051
0.00048
0.00048
0.00013
0.00128
0.00127
0.00127
0.00378
(13.038)***
(13.099)***
(13.094)***
(23.410)***
(2.499)**
(2.422)**
(2.422)**
(0.639)
(3.084)***
(3.079)***
(3.079)***
(2.955)***
T Vi,t−1
-0.00793
-0.00758
-0.00763
-0.00574
-0.00033
-0.00031
-0.00031
-0.00048
0.00024
0.00029
0.00029
-0.00249
(24.675)***
(23.918)***
(24.021)***
(17.584)***
(0.317)
(0.306)
(0.307)
(0.351)
(0.185)
(0.228)
(0.228)
(1.221)
BSIi,t−1
0.00014
0.00013
0.00013
0.00010
0.00003
0.00003
0.00003
0.00001
0.00001
0.00001
0.00001
0.00001
(12.655)***
(12.185)***
(12.257)***
(9.364)***
(2.919)***
(2.913)***
(2.913)***
(0.776)
(2.091)**
(2.103)**
(2.103)**
(1.880)*
MTi,t−1
-0.03177
-0.03047
-0.03060
-0.02286
-0.00677
-0.00671
-0.00672
0.01349
-0.00339
-0.00326
-0.00326
-0.00579
(23.284)***
(22.663)***
(22.710)***
(16.665)***
(1.298)
(1.296)
(1.297)
(2.039)**
(0.448)
(0.433)
(0.433)
(0.493)
ASCi,t−1
0.09610
0.17623
0.28399
(81.164)***
(14.181)***
(13.462)***
OP Ci,t−1
0.01976
0.02833
0.03429
(106.098)***
(22.531)***
(19.830)***
ASCi,t−1
0.09938
0.17491
0.28974
(83.273)***
(14.071)***
(13.730)***
OP Ci,t−1
0.01996
0.02831
0.03406
(106.901)***
(22.457)***
(19.636)***
ASCi,t−1
0.09938
0.17492
0.28974
(83.192)***
(14.072)***
(13.731)***
OP Ci,t−1
0.01995
0.02831
0.03406
(106.765)***
(22.457)***
(19.637)***
ASCi,t−1
0.05532
0.08004
0.05053
(41.868)***
(4.936)***
(1.408)
OP Ci,t−1
0.02188
0.03385
0.03478
(83.137)***
(15.580)***
(9.561)***
ICi,t−1
0.08150
0.17361
0.23250
(47.139)***
(8.489)***
(5.631)***
Intercept
0.02294
0.02124
0.02142
0.00396
-0.02092
-0.02054
-0.02054
-0.02779
-0.03523
-0.03607
-0.03607
-0.00701
(12.870)***
(12.081)***
(12.161)***
(2.155)**
(3.084)***
(3.042)***
(3.043)***
(3.045)***
(3.550)***
(3.642)***
(3.642)***
(0.431)
R2
0.18
0.18
0.18
0.50
0.02
0.02
0.02
0.03
0.05
0.05
0.05
0.03
Currency and Time FE
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
N
672,569
681,229
680,255
107,410
267,513
268,489
268,487
68,732
84,022
84,155
84,156
27,259
41


### Page 42

Table 13: This table presents the results of the following regression: SLOPEA
i,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 +
γ4BSIi,t−1 + γ5MTi,t−1 + γ6ASCk
i,t−1 + γ7OPCk
i,t−1 + γ8ICk
i,t−1 + ϵi,t. We restrict our sample to the period between August 2017 and
June 2018 in order to provide a substantial sample of cryptocurrencies upon which the market could trade, therefore providing a strong
sample to analyse. Panel A, B, C present the results of the estimation for time intervals set to 1 minute, 15 minutes and 60 minutes,
respectively. Respective columns in each panel are for the regressions where the components of the spread ASCk, OPCk are obtained
by Glosten and Harris (1988) (k = GH), two-way decomposition of Huang and Stoll (1997)(k = HS2 −way), Madhavan et al. (1997)
(k = MRR), and three-way decomposition of Huang and Stoll (1997)(k = HS3 −way). Inventory costs (IC) are obtained only by the
three-way decomposition of Huang and Stoll (1997). We require at least 30 trades within the time interval t, to estimate the adverse
selection component in that interval. Absolute value of the t-statistics in parenthesis. Hypothesis 2 asserts a relationship γ6 > 0. ***, **,
* indicates statistical significance at 1% , 5% and 10%, respectively.
Panel A: 1 min
Panel B: 15 min
Panel C: 60 min
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
σR
i,t−1
-2.82754
-3.07446
-3.06361
-1.82046
-1.43004
-1.44275
-1.44278
-1.45626
-0.71019
-0.71467
-0.71467
-0.47521
(3.069)***
(3.226)***
(3.211)***
(4.650)***
(6.501)***
(6.581)***
(6.581)***
(4.493)***
(2.356)**
(2.373)**
(2.373)**
(1.836)*
SP READi,t−1
0.00150
0.00151
0.00151
0.00141
0.00076
0.00071
0.00071
0.00012
0.00106
0.00105
0.00105
0.00118
(18.672)***
(18.886)***
(18.870)***
(16.583)***
(5.649)***
(5.465)***
(5.465)***
(0.854)
(2.141)**
(2.137)**
(2.137)**
(1.998)**
T Vi,t−1
-0.00596
-0.00568
-0.00572
-0.00597
0.00018
0.00025
0.00025
-0.00047
-0.00125
-0.00121
-0.00121
-0.00166
(3.931)***
(3.808)***
(3.825)***
(9.603)***
(0.274)
(0.372)
(0.371)
(0.489)
(0.766)
(0.745)
(0.745)
(1.140)
BSIi,t−1
0.00019
0.00018
0.00018
0.00012
0.00003
0.00003
0.00003
0.00003
0.00001
0.00001
0.00001
0.00001
(3.625)***
(3.576)***
(3.588)***
(5.960)***
(5.243)***
(5.220)***
(5.222)***
(3.763)***
(2.308)**
(2.317)**
(2.317)**
(2.729)***
MTi,t−1
-0.02879
-0.02743
-0.02757
-0.02746
-0.00797
-0.00771
-0.00772
-0.01022
-0.00395
-0.00383
-0.00383
0.00715
(4.468)***
(4.331)***
(4.343)***
(10.510)***
(2.336)**
(2.277)**
(2.279)**
(2.167)**
(0.407)
(0.396)
(0.396)
(0.853)
ASCi,t−1
0.15639
0.20906
0.30740
(28.007)***
(25.708)***
(11.352)***
OP Ci,t−1
0.01556
0.03186
0.03528
(17.719)***
(38.712)***
(15.891)***
ASCi,t−1
0.16132
0.21257
0.31261
(28.720)***
(26.133)***
(11.541)***
OP Ci,t−1
0.01559
0.03184
0.03510
(17.741)***
(38.584)***
(15.760)***
ASCi,t−1
0.16138
0.21259
0.31261
(28.704)***
(26.135)***
(11.541)***
OP Ci,t−1
0.01559
0.03184
0.03510
(17.725)***
(38.584)***
(15.760)***
ASCi,t−1
0.05512
0.11548
0.14751
(21.917)***
(9.990)***
(5.761)***
OP Ci,t−1
0.01769
0.03350
0.03173
(35.291)***
(21.624)***
(12.299)***
ICi,t−1
0.08835
0.18715
0.25066
(26.819)***
(12.837)***
(8.497)***
Intercept
0.00423
0.00278
0.00290
0.01991
-0.02880
-0.02938
-0.02938
-0.02344
-0.03533
-0.03602
-0.03602
-0.02389
(0.503)
(0.336)
(0.350)
(5.691)***
(6.489)***
(6.650)***
(6.651)***
(3.603)***
(2.773)***
(2.833)***
(2.833)***
(2.052)**
R2
0.01
0.01
0.01
0.21
0.06
0.06
0.06
0.08
0.04
0.04
0.04
0.06
Currency and Time FE
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
N
674,312
682,991
682,020
107,673
267,925
268,902
268,901
68,839
84,318
84,451
84,452
27,357
42


### Page 43

Table 14: This table presents the results of the following regression: DEPTHB
i,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 +
γ4BSIi,t−1 + γ5MTi,t−1 + γ6ASCk
i,t−1 + γ7OPCk
i,t−1 + γ8ICk
i,t−1 + ϵi,t. We restrict our sample to the period between August 2017 and
June 2018 in order to provide a substantial sample of cryptocurrencies upon which the market could trade, therefore providing a strong
sample to analyse. Panel A, B, C present the results of the estimation for time intervals set to 1 minute, 15 minutes and 60 minutes,
respectively. Respective columns in each panel are for the regressions where the components of the spread ASCk, OPCk are obtained
by Glosten and Harris (1988) (k = GH), two-way decomposition of Huang and Stoll (1997)(k = HS2 −way), Madhavan et al. (1997)
(k = MRR), and three-way decomposition of Huang and Stoll (1997)(k = HS3 −way). Inventory costs (IC) are obtained only by the
three-way decomposition of Huang and Stoll (1997). We require at least 30 trades within the time interval t, to estimate the adverse
selection component in that interval. Absolute value of the t-statistics in parenthesis. Hypothesis 2 asserts a relationship γ6 < 0. ***, **,
* indicates statistical significance at 1% , 5% and 10%, respectively.
Panel A: 1 min
Panel B: 15 min
Panel C: 60 min
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
σR
i,t−1
52.43454
60.34179
60.14232
26.04875
12.10289
11.62395
11.64354
21.28383
3.61126
3.68521
3.68426
2.96110
(2.105)*
(2.357)*
(2.346)*
(0.243)
(2.898)**
(2.784)**
(2.788)**
(2.673)**
(1.319)
(1.349)
(1.348)
(0.743)
SP READi,t−1
0.00011
0.00012
0.00012
0.00123
0.00008
0.00005
0.00005
0.00007
-0.00017
-0.00018
-0.00018
-0.00063
(0.053)
(0.055)
(0.055)
(0.053)
(0.033)
(0.021)
(0.021)
(0.021)
(0.038)
(0.039)
(0.039)
(0.070)
T Vi,t−1
0.14494
0.13739
0.13759
0.24887
0.07877
0.07994
0.07978
0.07605
0.03181
0.03078
0.03079
0.11311
(3.534)**
(3.426)**
(3.423)**
(1.460)
(6.159)**
(6.262)**
(6.251)**
(3.199)**
(2.143)*
(2.080)*
(2.081)*
(5.044)**
BSIi,t−1
-0.00390
-0.00382
-0.00382
-0.00218
-0.00119
-0.00118
-0.00118
-0.00152
-0.00040
-0.00040
-0.00040
-0.00050
(2.771)**
(2.775)**
(2.766)**
(0.396)
(11.026)**
(11.015)**
(11.003)**
(7.591)**
(8.843)**
(8.868)**
(8.867)**
(6.461)**
MTi,t−1
0.48902
0.48116
0.48341
1.03464
0.87031
0.86521
0.86365
0.94730
1.04473
1.03070
1.03038
1.05562
(2.808)**
(2.827)**
(2.834)**
(1.445)
(13.438)**
(13.414)**
(13.387)**
(8.175)**
(11.863)**
(11.756)**
(11.754)**
(8.179)**
ASCi,t−1
0.00801
0.05893
0.16218
(0.053)
(0.382)
(0.660)
OP Ci,t−1
-0.00710
0.01496
0.02914
(0.299)
(0.957)
(1.446)
ASCi,t−1
0.00349
0.06462
0.16029
(0.023)
(0.417)
(0.652)
OP Ci,t−1
-0.00796
0.01493
0.02919
(0.337)
(0.950)
(1.445)
ASCi,t−1
0.00375
0.06423
0.16027
(0.025)
(0.415)
(0.652)
OP Ci,t−1
-0.00794
0.01488
0.02918
(0.336)
(0.947)
(1.444)
ASCi,t−1
-0.02323
0.05023
0.33132
(0.034)
(0.177)
(0.841)
OP Ci,t−1
0.00729
0.02248
0.00456
(0.053)
(0.591)
(0.115)
ICi,t−1
-0.10774
0.03252
0.45413
(0.119)
(0.091)
(1.000)
Intercept
-0.81855
-0.79133
-0.79282
-1.53546
-0.63169
-0.63700
-0.63576
-0.65441
-0.39184
-0.38216
-0.38218
-0.98827
(3.599)**
(3.556)**
(3.557)**
(1.601)
(7.497)**
(7.570)**
(7.556)**
(4.094)**
(3.388)**
(3.314)**
(3.314)**
(5.516)**
R2
0.01
0.01
0.01
0.00
0.20
0.20
0.20
0.24
0.40
0.40
0.40
0.48
Currency and Time FE
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
N
674,322
683,001
682,030
107,673
267,925
268,902
268,901
68,839
84,318
84,451
84,452
27,357
43


### Page 44

Table 15: This table presents the results of the following regression: DEPTHA
i,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 +
γ4BSIi,t−1 + γ5MTi,t−1 + γ6ASCk
i,t−1 + γ7OPCk
i,t−1 + γ8ICk
i,t−1 + ϵi,t. We restrict our sample to the period between August 2017 and
June 2018 in order to provide a substantial sample of cryptocurrencies upon which the market could trade, therefore providing a strong
sample to analyse. Panel A, B, C present the results of the estimation for time intervals set to 1 minute, 15 minutes and 60 minutes,
respectively. Respective columns in each panel are for the regressions where the components of the spread ASCk, OPCk are obtained
by Glosten and Harris (1988) (k = GH), two-way decomposition of Huang and Stoll (1997)(k = HS2 −way), Madhavan et al. (1997)
(k = MRR), and three-way decomposition of Huang and Stoll (1997)(k = HS3 −way). Inventory costs (IC) are obtained only by the
three-way decomposition of Huang and Stoll (1997). We require at least 30 trades within the time interval t, to estimate the adverse
selection component in that interval. Absolute value of the t-statistics are in parenthesis. Hypothesis 2 asserts a relationship γ6 < 0. ***,
**, * indicates statistical significance at 1% , 5% and 10%, respectively.
Panel A: 1 min
Panel B: 15 min
Panel C: 60 min
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
σR
i,t−1
33.78676
37.67565
37.97311
38.46850
15.84417
16.36739
16.37609
10.82265
6.05765
5.96387
5.96320
-6.07019
(3.783)**
(4.127)**
(4.156)**
(1.765)
(3.013)**
(3.107)**
(3.109)**
(1.947)
(1.539)
(1.517)
(1.517)
(0.576)
SP READi,t−1
0.00007
0.00008
0.00008
0.00074
0.00004
0.00003
0.00003
0.00009
-0.00024
-0.00025
-0.00025
-0.00052
(0.095)
(0.105)
(0.106)
(0.157)
(0.012)
(0.008)
(0.008)
(0.035)
(0.038)
(0.039)
(0.039)
(0.021)
T Vi,t−1
0.16771
0.16022
0.16094
0.20382
0.07716
0.07583
0.07573
0.10313
0.03552
0.03760
0.03761
0.12660
(11.408)**
(11.207)**
(11.235)**
(5.885)**
(4.791)**
(4.710)**
(4.704)**
(6.214)**
(1.664)
(1.766)
(1.766)
(2.133)*
BSIi,t−1
-0.00365
-0.00351
-0.00349
-0.00337
-0.00102
-0.00104
-0.00104
-0.00104
-0.00027
-0.00028
-0.00028
-0.00038
(7.231)**
(7.151)**
(7.083)**
(3.016)**
(7.536)**
(7.639)**
(7.636)**
(7.417)**
(4.188)**
(4.235)**
(4.235)**
(1.880)
MTi,t−1
0.44200
0.43039
0.42219
0.27096
0.79404
0.80936
0.80886
0.74269
0.73379
0.74538
0.74516
0.53323
(7.079)**
(7.093)**
(6.943)**
(1.863)
(9.736)**
(9.948)**
(9.940)**
(9.182)**
(5.793)**
(5.908)**
(5.907)**
(1.561)
ASCi,t−1
0.02253
0.05437
0.12703
(0.416)
(0.280)
(0.359)
OP Ci,t−1
-0.00848
0.00565
0.00749
(0.996)
(0.287)
(0.258)
ASCi,t−1
0.01873
0.05573
0.13700
(0.348)
(0.285)
(0.387)
OP Ci,t−1
-0.00854
0.00620
0.00712
(1.014)
(0.313)
(0.245)
ASCi,t−1
0.01919
0.05530
0.13699
(0.356)
(0.283)
(0.387)
OP Ci,t−1
-0.00884
0.00619
0.00711
(1.049)
(0.312)
(0.245)
ASCi,t−1
0.02538
0.10116
0.13416
(0.181)
(0.510)
(0.129)
OP Ci,t−1
-0.01309
0.00042
0.00614
(0.469)
(0.016)
(0.058)
ICi,t−1
0.00813
0.13872
0.27325
(0.044)
(0.555)
(0.227)
Intercept
-0.87112
-0.84234
-0.84338
-0.98281
-0.61951
-0.61700
-0.61629
-0.76177
-0.38161
-0.39835
-0.39837
-0.93147
(10.683)**
(10.617)**
(10.616)**
(5.046)**
(5.839)**
(5.813)**
(5.807)**
(6.827)**
(2.294)*
(2.400)*
(2.400)*
(1.964)*
R2
0.06
0.06
0.06
0.07
0.12
0.12
0.12
0.35
0.22
0.22
0.22
0.10
Currency and Time FE
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
N
674,322
683,001
682,030
107,673
267,925
268,902
268,901
68,839
84,318
84,451
84,452
27,357
44


### Page 45

Table 16: This table presents the results of the following regression: MTi,t = αi+θt+γ1σR
i,t−1+γ2SPREADi,t−1+γ3TVi,t−1+γ4BSIi,t−1+
γ5MTi,t−1 +γ6ASCk
i,t−1 +γ7OPCk
i,t−1 +γ8ICk
i,t−1 +ϵi,t. We restrict our sample to the period between August 2017 and June 2018 in order
to provide a substantial sample of cryptocurrencies upon which the market could trade, therefore providing a strong sample to analyse.
Panel A, B, C present the results of the estimation for time intervals set to 1 minute, 15 minutes and 60 minutes, respectively. Respective
columns in each panel are for the regressions where the components of the spread ASCk, OPCk are obtained by Glosten and Harris (1988)
(k = GH), two-way decomposition of Huang and Stoll (1997)(k = HS2 −way), Madhavan et al. (1997) (k = MRR), and three-way
decomposition of Huang and Stoll (1997)(k = HS3 −way). Inventory costs (IC) are obtained only by the three-way decomposition of
Huang and Stoll (1997). We require at least 30 trades within the time interval t, to estimate the adverse selection component in that
interval. Absolute value of the t-statistics are in parenthesis. Hypothesis 3 asserts a relationship γ6 > 0. ***, **, * indicates statistical
significance at 1% , 5% and 10%, respectively.
Panel A: 1 min
Panel B: 15 min
Panel C: 60 min
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
GH
HS 2-way
MRR
HS 3-way
σR
i,t−1
-9.45390
-10.62251
-10.51745
-10.67045
-4.12059
-4.11200
-4.12092
-4.86010
-1.54267
-1.54980
-1.54951
-1.64179
(41.816)***
(44.690)***
(44.266)***
(17.482)***
(29.359)***
(29.324)***
(29.386)***
(16.375)***
(12.905)***
(12.954)***
(12.951)***
(7.836)***
SP READi,t−1
-0.00012
-0.00012
-0.00012
-0.00027
-0.00025
-0.00025
-0.00025
-0.00015
-0.00027
-0.00027
-0.00027
0.00019
(4.081)***
(4.045)***
(4.039)***
(2.266)**
(3.008)***
(3.005)***
(3.006)***
(1.132)
(1.378)
(1.369)
(1.369)
(0.394)
T Vi,t−1
-0.01174
-0.01205
-0.01187
-0.01419
-0.02106
-0.02111
-0.02108
-0.02056
-0.02088
-0.02090
-0.02090
-0.01968
(28.654)***
(29.612)***
(29.136)***
(13.259)***
(47.673)***
(47.888)***
(47.827)***
(22.632)***
(32.033)***
(32.083)***
(32.088)***
(16.608)***
BSIi,t−1
-0.00031
-0.00029
-0.00029
-0.00024
0.00000
0.00000
0.00000
0.00001
0.00001
0.00001
0.00001
0.00001
(24.497)***
(22.754)***
(23.068)***
(7.615)***
(0.501)
(0.602)
(0.616)
(0.908)
(2.628)***
(2.689)***
(2.680)***
(1.941)*
MTi,t−1
0.22503
0.22834
0.22639
0.20444
0.18082
0.18243
0.18251
0.18171
0.20338
0.20429
0.20439
0.20935
(124.219)***
(127.007)***
(125.815)***
(44.341)***
(79.417)***
(80.486)***
(80.502)***
(40.440)***
(52.543)***
(52.871)***
(52.901)***
(30.718)***
ASCi,t−1
-0.03920
-0.12782
-0.22914
(28.606)***
(23.995)***
(21.269)***
OP Ci,t−1
-0.00467
-0.00401
0.00164
(22.434)***
(7.623)***
(1.863)*
ASCi,t−1
-0.04090
-0.13192
-0.23250
(29.511)***
(24.712)***
(21.536)***
OP Ci,t−1
-0.00455
-0.00384
0.00185
(21.675)***
(7.260)***
(2.087)**
ASCi,t−1
-0.04039
-0.13204
-0.23250
(29.161)***
(24.733)***
(21.535)***
OP Ci,t−1
-0.00455
-0.00384
0.00185
(21.699)***
(7.266)***
(2.091)**
ASCi,t−1
-0.02915
-0.08390
-0.13607
(7.396)***
(7.708)***
(6.516)***
OP Ci,t−1
-0.00522
-0.00543
0.00063
(6.964)***
(3.816)***
(0.303)
ICi,t−1
-0.05303
-0.13303
-0.25407
(10.446)***
(9.757)***
(10.611)***
Intercept
0.37491
0.37757
0.37684
0.40211
0.34710
0.34744
0.34732
0.35024
0.31594
0.31629
0.31629
0.31266
(159.292)***
(161.522)***
(161.188)***
(64.801)***
(119.090)***
(119.434)***
(119.388)***
(57.260)***
(62.221)***
(62.314)***
(62.314)***
(33.001)***
R2
0.09
0.09
0.09
0.09
0.12
0.12
0.12
0.12
0.14
0.14
0.14
0.13
Currency and Time FE
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
N
488,796
494,244
493,641
74,528
254,801
255,657
255,660
65,729
83,808
83,941
83,942
27,231
45


### Page 46

Table 17: Ri,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 + γ4BSIi,t−1 + γ5MTi,t−1 + γ6ASCi,t−1 + γ7OPCi,t−1 + γ8ICi,t−1 +
γ9DEPTHi,t−1 + γ10SLOPEi,t−1 + ϵi,t. We restrict our sample to the period between August 2017 and June 2018 in order to provide a
substantial sample of cryptocurrencies upon which the market could trade, therefore providing a strong sample to analyse. The components
of the spread are estimated using the Glosten and Harris (1988) model. Panel A and B present the results of the estimation for time
intervals set to 60 minutes and 1 minutes, respectively. We require at least 30 trades within the time interval t, to estimate the adverse
selection component in that interval. Absolute value of the t-statistics are in parenthesis. Hypothesis 4 asserts a relationship γ6 ̸= 0. ***,
**, * indicates statistical significance at 1% , 5% and 10%, respectively.
Panel A: 1min
Panel B: 60min
1
2
3
4
5
6
1
2
3
4
5
6
ASCi,t−1
-0.00003
-0.00006
-0.00006
-0.00006
-0.00006
-0.00006
-0.00298
-0.00270
-0.00283
-0.00326
-0.00321
-0.00288
(1.255)
(2.463)*
(2.513)*
(2.420)*
(2.422)*
(2.617)**
(2.189)*
(1.950)
(2.031)*
(2.179)*
(2.142)*
(2.025)*
OP Ci,t−1
0.00002
0.00000
0.00000
0.00000
0.00000
0.00000
0.00009
-0.00016
-0.00016
-0.00020
-0.00018
-0.00015
(5.297)**
(0.342)
(0.386)
(0.521)
(0.516)
(0.319)
(0.857)
(1.429)
(1.431)
(1.601)
(1.426)
(1.273)
σR
i,t−1
0.08694
0.08623
0.08633
0.08639
0.08659
0.22352
0.21638
0.22559
0.22541
0.22436
(21.868)**
(21.588)**
(21.328)**
(21.344)**
(21.400)**
(10.800)**
(10.402)**
(10.730)**
(10.722)**
(10.699)**
ILLIQi,t−1
0.04362
0.04444
0.04287
0.04284
0.04281
-0.51977
-0.48542
-0.50568
-0.50475
-0.50434
(5.727)**
(5.745)**
(5.406)**
(5.402)**
(5.399)**
(7.520)**
(6.952)**
(7.158)**
(7.144)**
(7.139)**
BSIi,t−1
-0.00000
-0.00000
-0.00000
-0.00000
-0.00000
0.00000
0.00000
0.00000
0.00000
0.00000
(2.152)*
(2.252)*
(2.308)*
(2.309)*
(2.361)*
(0.574)
(0.602)
(0.503)
(0.468)
(0.518)
T Vi,t−1
0.00001
0.00002
0.00002
0.00002
0.00002
0.00006
0.00007
0.00005
0.00005
0.00005
(2.452)*
(2.487)*
(2.397)*
(2.399)*
(2.470)*
(0.764)
(0.775)
(0.566)
(0.594)
(0.613)
MTi,t−1
0.00006
0.00006
0.00006
0.00006
0.00006
0.00064
0.00056
0.00053
0.00053
0.00052
(2.323)*
(2.188)*
(2.072)*
(2.085)*
(2.135)*
(1.272)
(1.110)
(1.044)
(1.042)
(1.018)
DEP T Hi,t−1
-0.00000
-0.00000
-0.00000
0.00002
0.00002
0.00002
(0.478)
(0.485)
(0.485)
(1.905)
(1.760)
(1.759)
SLOP Ei,t−1
-0.00001
-0.00002
0.00114
0.00127
(0.260)
(0.279)
(0.789)
(0.876)
SP READi,t−1
0.00000
0.00000
-0.00006
-0.00006
(0.354)
(0.327)
(2.160)*
(2.138)*
SLOP EB
i,t−1
0.00002
0.00018
(0.956)
(0.770)
SLOP EA
i,t−1
0.00000
0.00011
(0.245)
(0.605)
DEP T HB
i,t−1
0.00000
0.00003
(0.097)
(1.519)
DEP T HA
i,t−1
-0.00000
0.00001
(1.698)
(0.983)
Intercept
0.00001
-0.00022
-0.00022
-0.00022
-0.00022
-0.00022
0.00047
-0.00048
-0.00048
-0.00029
-0.00025
-0.00030
(0.673)
(6.417)**
(6.358)**
(6.162)**
(6.168)**
(6.215)**
(1.687)
(0.731)
(0.730)
(0.427)
(0.377)
(0.453)
R2
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
Currency and Time FE
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
N
700,743
700,702
693,031
674,343
674,285
674,247
87,016
87,004
86,109
84,308
84,306
84,306
46


### Page 47

Table 18: Ri,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 + γ4BSIi,t−1 + γ5MTi,t−1 + γ6ASCi,t−1 + γ7OPCi,t−1 + γ8ICi,t−1 +
γ9DEPTHi,t−1 + γ10SLOPEi,t−1 + ϵi,t. We restrict our sample to the period between August 2017 and June 2018 in order to provide a
substantial sample of cryptocurrencies upon which the market could trade, therefore providing a strong sample to analyse. The components
of the spread are estimated using the Madhavan et al. (1997) model. Panel A and B present the results of the estimation for time intervals
set to 60 minutes and 1 minutes, respectively. We require at least 30 trades within the time interval t, to estimate the adverse selection
component in that interval. Absolute value of the t-statistics are in parenthesis. Hypothesis 4 asserts a relationship γ6 ̸= 0. ***, **, *
indicates statistical significance at 1% , 5% and 10%, respectively.
Panel A: 1min
Panel B: 60min
1
2
3
4
5
6
1
2
3
4
5
6
ASCi,t−1
-0.00001
-0.00005
-0.00005
-0.00005
-0.00005
-0.00005
-0.00305
-0.00279
-0.00294
-0.00340
-0.00334
-0.00299
(0.550)
(2.153)*
(2.183)*
(2.148)*
(2.149)*
(2.287)*
(2.244)*
(2.015)*
(2.112)*
(2.266)*
(2.228)*
(2.103)*
OP Ci,t−1
0.00002
-0.00000
-0.00000
-0.00000
-0.00000
-0.00000
0.00010
-0.00016
-0.00016
-0.00020
-0.00018
-0.00014
(4.463)**
(0.824)
(0.779)
(0.815)
(0.823)
(0.983)
(0.881)
(1.390)
(1.386)
(1.573)
(1.398)
(1.229)
σR
i,t−1
0.11542
0.11496
0.11288
0.11296
0.11313
0.22354
0.21660
0.22600
0.22582
0.22472
(28.514)**
(28.281)**
(26.574)**
(26.591)**
(26.642)**
(10.807)**
(10.419)**
(10.757)**
(10.749)**
(10.723)**
ILLIQi,t−1
0.01542
0.01531
0.02635
0.02628
0.02626
-0.51946
-0.48554
-0.50679
-0.50588
-0.50549
(2.720)**
(2.678)**
(3.324)**
(3.315)**
(3.313)**
(7.524)**
(6.962)**
(7.182)**
(7.169)**
(7.163)**
BSIi,t−1
-0.00000
-0.00000
-0.00000
-0.00000
-0.00000
0.00000
0.00000
0.00000
0.00000
0.00000
(3.076)**
(3.176)**
(3.361)**
(3.364)**
(3.398)**
(0.535)
(0.565)
(0.470)
(0.435)
(0.488)
T Vi,t−1
0.00001
0.00001
0.00001
0.00001
0.00001
0.00007
0.00007
0.00005
0.00005
0.00005
(1.039)
(1.077)
(1.139)
(1.143)
(1.182)
(0.786)
(0.786)
(0.573)
(0.600)
(0.621)
MTi,t−1
0.00009
0.00008
0.00008
0.00008
0.00008
0.00067
0.00058
0.00055
0.00055
0.00054
(3.341)**
(3.187)**
(3.011)**
(3.028)**
(3.058)**
(1.331)
(1.160)
(1.088)
(1.087)
(1.062)
DEP T Hi,t−1
-0.00000
-0.00000
-0.00000
0.00002
0.00002
0.00002
(0.348)
(0.354)
(0.354)
(1.907)
(1.762)
(1.762)
SLOP Ei,t−1
0.00001
0.00001
0.00120
0.00133
(0.115)
(0.093)
(0.828)
(0.915)
SP READi,t−1
0.00000
0.00000
-0.00006
-0.00006
(0.435)
(0.419)
(2.160)*
(2.136)*
SLOP EB
i,t−1
0.00003
0.00018
(1.174)
(0.771)
SLOP EA
i,t−1
0.00000
0.00011
(0.224)
(0.605)
DEP T HB
i,t−1
0.00000
0.00003
(0.015)
(1.523)
DEP T HA
i,t−1
-0.00000
0.00001
(1.092)
(0.982)
Intercept
0.00002
-0.00020
-0.00019
-0.00020
-0.00020
-0.00020
0.00048
-0.00049
-0.00049
-0.00028
-0.00025
-0.00030
(1.114)
(5.796)**
(5.724)**
(5.783)**
(5.785)**
(5.811)**
(1.701)
(0.749)
(0.734)
(0.423)
(0.373)
(0.454)
R2
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
Currency and Time FE
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
N
708,748
708,709
700,954
682,053
681,995
681,954
87,153
87,141
86,245
84,442
84,440
84,440
47


### Page 48

Table 19: Ri,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 + γ4BSIi,t−1 + γ5MTi,t−1 + γ6ASCi,t−1 + γ7OPCi,t−1 + γ8ICi,t−1 +
γ9DEPTHi,t−1 + γ10SLOPEi,t−1 + ϵi,t. We restrict our sample to the period between August 2017 and June 2018 in order to provide a
substantial sample of cryptocurrencies upon which the market could trade, therefore providing a strong sample to analyse. The components
of the spread are estimated using the two-way decomposition of Huang and Stoll (1997) model. Panel A and B present the results of the
estimation for time intervals set to 60 minutes and 1 minutes, respectively. We require at least 30 trades within the time interval t, to
estimate the adverse selection component in that interval. Absolute value of the t-statistics are in parenthesis. Hypothesis 4 asserts a
relationship γ6 ̸= 0. ***, **, * indicates statistical significance at 1% , 5% and 10%, respectively.
Panel A: 1min
Panel B: 60min
1
2
3
4
5
6
1
2
3
4
5
6
ASCi,t−1
-0.00001
-0.00005
-0.00005
-0.00005
-0.00005
-0.00005
-0.00305
-0.00279
-0.00294
-0.00340
-0.00334
-0.00299
(0.564)
(2.177)*
(2.210)*
(2.169)*
(2.171)*
(2.311)*
(2.244)*
(2.015)*
(2.112)*
(2.266)*
(2.228)*
(2.103)*
OP Ci,t−1
0.00002
-0.00000
-0.00000
-0.00000
-0.00000
-0.00000
0.00010
-0.00016
-0.00016
-0.00020
-0.00018
-0.00014
(4.447)**
(0.845)
(0.800)
(0.824)
(0.832)
(0.996)
(0.881)
(1.390)
(1.386)
(1.573)
(1.398)
(1.229)
σR
i,t−1
0.11563
0.11512
0.11319
0.11326
0.11344
0.22354
0.21660
0.22600
0.22582
0.22472
(28.613)**
(28.369)**
(26.722)**
(26.739)**
(26.791)**
(10.807)**
(10.419)**
(10.757)**
(10.749)**
(10.722)**
ILLIQi,t−1
0.01495
0.01498
0.02545
0.02538
0.02536
-0.51946
-0.48554
-0.50679
-0.50588
-0.50549
(2.660)**
(2.641)**
(3.258)**
(3.249)**
(3.247)**
(7.524)**
(6.961)**
(7.182)**
(7.169)**
(7.163)**
BSIi,t−1
-0.00000
-0.00000
-0.00000
-0.00000
-0.00000
0.00000
0.00000
0.00000
0.00000
0.00000
(3.124)**
(3.213)**
(3.414)**
(3.417)**
(3.451)**
(0.535)
(0.565)
(0.470)
(0.435)
(0.488)
T Vi,t−1
0.00001
0.00001
0.00001
0.00001
0.00001
0.00007
0.00007
0.00005
0.00005
0.00005
(1.034)
(1.066)
(1.130)
(1.134)
(1.174)
(0.786)
(0.786)
(0.573)
(0.600)
(0.621)
MTi,t−1
0.00009
0.00008
0.00008
0.00008
0.00008
0.00067
0.00058
0.00055
0.00055
0.00054
(3.317)**
(3.162)**
(3.002)**
(3.018)**
(3.049)**
(1.330)
(1.160)
(1.088)
(1.087)
(1.062)
DEP T Hi,t−1
-0.00000
-0.00000
-0.00000
0.00002
0.00002
0.00002
(0.358)
(0.364)
(0.364)
(1.907)
(1.762)
(1.762)
SLOP Ei,t−1
0.00001
0.00000
0.00120
0.00133
(0.096)
(0.074)
(0.828)
(0.915)
SP READi,t−1
0.00000
0.00000
-0.00006
-0.00006
(0.431)
(0.414)
(2.160)*
(2.136)*
SLOP EB
i,t−1
0.00003
0.00018
(1.159)
(0.771)
SLOP EA
i,t−1
0.00000
0.00011
(0.224)
(0.605)
DEP T HB
i,t−1
0.00000
0.00003
(0.010)
(1.523)
DEP T HA
i,t−1
-0.00000
0.00001
(1.104)
(0.982)
Intercept
0.00002
-0.00019
-0.00019
-0.00020
-0.00020
-0.00020
0.00048
-0.00049
-0.00049
-0.00028
-0.00025
-0.00030
(1.131)
(5.770)**
(5.695)**
(5.751)**
(5.753)**
(5.779)**
(1.701)
(0.749)
(0.734)
(0.423)
(0.373)
(0.454)
R2
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
Currency and Time FE
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
N
709,774
709,735
701,960
683,026
682,966
682,925
87,152
87,140
86,244
84,441
84,439
84,439
48


### Page 49

Table 20: Ri,t = αi + θt + γ1σR
i,t−1 + γ2SPREADi,t−1 + γ3TVi,t−1 + γ4BSIi,t−1 + γ5MTi,t−1 +
γ6ASCk
i,t−1 + γ7OPCk
i,t−1 + γ8ICk
i,t−1 + γ9DEPTHi,t−1 + γ10SLOPEi,t−1 + ϵi,t. We restrict our
sample to the period between August 2017 and June 2018 in order to provide a substantial sample
of cryptocurrencies upon which the market could trade, therefore providing a strong sample to
analyse. The components of the spread are estimated using the three-way decomposition of Huang
and Stoll (1997) model. Panel A and B present the results of the estimation for time intervals set to
60 minutes and 1 minutes, respectively. We require at least 30 trades within the time interval t, to
estimate the adverse selection component in that interval. Absolute value of the t-statistics are in
parenthesis. Hypothesis 4 asserts a relationship γ6 ̸= 0. ***, **, * indicates statistical significance
at 1% , 5% and 10%, respectively.
Panel A: 1 min
1
2
3
4
5
6
7
8
9
ASCi,t−1
0.00002
0.00006
0.00004
0.00004
0.00005
0.00005
0.00004
(0.411)
(1.052)
(0.739)
(0.624)
(0.727)
(0.721)
(0.711)
ICi,t−1
0.00003
0.00008
0.00007
0.00007
0.00008
0.00008
0.00008
(0.426)
(1.040)
(0.891)
(0.920)
(0.939)
(0.938)
(0.930)
OP Ci,t−1
-0.00002
-0.00003
-0.00004
-0.00004
-0.00004
-0.00004
-0.00004
(2.049)*
(2.503)*
(3.294)**
(3.286)**
(3.183)**
(3.171)**
(3.238)**
σR
i,t−1
0.03475
0.03426
0.03453
0.03456
0.03515
(3.427)**
(3.363)**
(3.304)**
(3.306)**
(3.364)**
ILLIQi,t−1
0.03905
0.04389
0.04753
0.04756
0.04671
(1.909)
(2.132)*
(2.113)*
(2.114)*
(2.077)*
BSIi,t−1
-0.00000
-0.00000
-0.00000
-0.00000
-0.00000
(1.552)
(1.509)
(1.540)
(1.542)
(1.562)
T Vi,t−1
0.00005
0.00005
0.00005
0.00005
0.00005
(3.141)**
(3.092)**
(2.976)**
(2.979)**
(2.999)**
MTi,t−1
0.00008
0.00006
0.00006
0.00006
0.00006
(1.190)
(1.006)
(0.928)
(0.925)
(0.919)
DEP T Hi,t−1
0.00000
0.00000
0.00000
(0.464)
(0.539)
(0.538)
SLOP Ei,t−1
-0.00004
-0.00004
(0.264)
(0.213)
SP READi,t−1
-0.00000
-0.00000
(0.532)
(0.535)
SLOP EB
i,t−1
0.00006
(0.568)
SLOP EA
i,t−1
-0.00009
(0.488)
DEP T HB
i,t−1
-0.00000
(1.085)
DEP T HA
i,t−1
0.00000
(1.884)
Intercept
-0.00002
-0.00002
0.00002
-0.00000
-0.00030
-0.00029
-0.00029
-0.00029
-0.00029
(0.479)
(0.476)
(0.386)
(0.054)
(3.473)**
(3.397)**
(3.325)**
(3.297)**
(3.302)**
R2
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
Currency and Time FE
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
N
112,151
112,151
112,151
112,151
112,143
110,818
107,675
107,666
107,657
Panel B: 60 min
1
2
3
4
5
6
7
8
9
ASCi,t−1
-0.00142
-0.00151
-0.00101
-0.00094
-0.00121
-0.00112
-0.00116
(0.562)
(0.564)
(0.374)
(0.344)
(0.430)
(0.398)
(0.411)
ICi,t−1
0.00139
0.00104
0.00153
0.00126
0.00121
0.00127
0.00124
(0.495)
(0.340)
(0.491)
(0.403)
(0.362)
(0.381)
(0.374)
OP Ci,t−1
0.00004
0.00005
-0.00025
-0.00025
-0.00028
-0.00026
-0.00026
(0.185)
(0.202)
(0.893)
(0.894)
(0.930)
(0.842)
(0.850)
σR
i,t−1
0.16354
0.16330
0.17015
0.16997
0.16968
(4.464)**
(4.419)**
(4.564)**
(4.560)**
(4.552)**
ILLIQi,t−1
-0.12680
-0.13647
-0.14166
-0.14005
-0.13842
(1.039)
(1.098)
(1.127)
(1.115)
(1.102)
BSIi,t−1
-0.00000
-0.00000
-0.00000
-0.00000
-0.00000
(1.011)
(1.154)
(1.120)
(1.144)
(1.109)
T Vi,t−1
0.00011
0.00012
0.00010
0.00010
0.00010
(0.732)
(0.775)
(0.637)
(0.654)
(0.634)
MTi,t−1
0.00175
0.00179
0.00168
0.00168
0.00163
(1.944)
(1.973)*
(1.836)
(1.833)
(1.775)
DEP T Hi,t−1
0.00002
0.00002
0.00002
(1.346)
(1.222)
(1.221)
SLOP Ei,t−1
0.00082
0.00097
(0.234)
(0.277)
SP READi,t−1
-0.00007
-0.00007
(1.021)
(1.026)
SLOP EB
i,t−1
0.00056
(0.162)
SLOP EA
i,t−1
0.00046
(0.886)
DEP T HB
i,t−1
0.00006
(1.869)
DEP T HA
i,t−1
0.00001
(0.361)
Intercept
0.00036
0.00011
0.00020
0.00022
-0.00146
-0.00147
-0.00125
-0.00121
-0.00118
(0.793)
(0.229)
(0.440)
(0.415)
(1.166)
(1.171)
(0.986)
(0.954)
(0.928)
R2
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
Currency and Time FE
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
Yes
49

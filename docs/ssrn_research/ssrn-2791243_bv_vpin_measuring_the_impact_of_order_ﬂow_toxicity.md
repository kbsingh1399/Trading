# BV-VPIN: Measuring the impact of order ﬂow toxicity and liquidity on

- **Source File**: `ssrn-2791243.pdf`
- **Total Pages**: 27
- **SSRN ID**: `ssrn-2791243`

---


### Page 1

Electronic copy available at: http://ssrn.com/abstract=2791243
BV-VPIN: Measuring the impact of order ﬂow toxicity and liquidity on
international equities markets$
Rand Kwong Yew Lowa,b,∗, Te Lic,d,, Terry Marshf,1,
aUQ Business School, University of Queensland, Brisbane, QLD, 4072, Australia
bStern School of Business, New York University, New York, NY, 10012, USA
cFu Foundation School of Engineering and Applied Science, Columbia University, New York, NY, 10027, USA
dPF2 Securities Evaluations, 29th Floor, 85 Broad St, New York, NY 10004, USA
eQuantal International Inc., 455 Market Street. Suite 1200, San Francisco, CA, 94105, USA
fHaas School of Business, University of California 545 Student Services Building, Berkeley, CA 94720-1900, USA
Abstract
Order ﬂow toxicity is a measure of a trader’s exposure to the risk that counter-parties possess private
information or other informational advantages. High levels of order ﬂow toxicity can culminate in
market makers providing liquidity at a loss or in suboptimal execution of trades. From a regulatory
perspective, high levels of toxicity can be harmful to overall market liquidity and precede precipitous
drops in asset prices.
Bulk Volume VPIN (BV-VPIN) is one way of measuring the “toxicity”
component of order ﬂow that has been successfully applied in High Frequency Trading (HFT)
environments. We apply the BV-VPIN to daily data for a range of international indices to extend
previous analysis of its properties. We ﬁnd that a rise in BV-VPIN eﬀectively foreshadows high-
levels of volatility in the equities indices of several countries.
If a BV-VPIN futures contract
exists, we show that it would exhibit safe haven characteristics during market downturns.
In
particular, a simple active portfolio management strategy that times investments in equities (risk-
free asset) when BV-VPIN levels are low (high) outperforms a buy-and-hold strategy. Thus, we
ﬁnd support for the application of BV-VPIN in international equities markets as a risk monitoring
and management tool for portfolio managers and regulators.
Keywords:
VPIN, Bulk Volume Classiﬁcation, international equities, liquidity, order ﬂow toxicity
JEL classiﬁcation: G12, G14, C58, D53
$The authors acknowledge the resources and technical support provided by the research team at PF2 Securities.
We also thank Joe Pimbley at Maxwell Consulting for his insightful feedback and helpful comments. The authors
acknowledge funding from the (1) Australia Awards - Endeavour Research Fellowship (2) Australian Institute for
Business and Economics (AIBE) in support of Dr.
Rand K.Y. Low at the Stern School of Business, New York
University. The authors also acknowledge ﬁnancial support for this research from the following funding bodies (1)
Accounting & Finance Association of Australia and New Zealand (AFAANZ) 2013/2014 research grants (2) UQ
Postdoctoral Research Grant entitled ‘Portfolio optimization and risk management techniques for ﬁnancial crisis’.
∗Corresponding authors
Email addresses: r.low@business.uq.edu.au, rand.low@stern.nyu.edu (Rand Kwong Yew Low),
tl2399@columbia.edu (Te Li), terry.marsh@quantal.com (Terry Marsh)


### Page 2

Electronic copy available at: http://ssrn.com/abstract=2791243
1. Introduction
On May 6th 2010, the Dow Jones Industrial Average (DJIA) suﬀered a decline of 998.5 points. This
event is the largest one-day point decline of the DJIA, and regularly referred to as the “ﬂash crash”.
Several explanations have been provided, e.g., speculative trading by hedge funds (Patterson and
Lauricella, 2010; Phillips, 2010), currency movements in the US dollar/Japanese yen exchange rate
(Krasting, 2010), and technical reporting diﬃculties on the NYSE (Flood, 2010). However, the most
salient feature of the ﬂash crash is the extreme lack of liquidity that occured (CFTC-SEC, 2010a,b;
Easley et al., 2011b). More speciﬁcally, Easley et al. (2011b) attribute that tight liquidity to an
unprecedented increase in order ﬂow toxicity, where uninformed traders (e.g., market makers) start
to reduce their positions signiﬁcantly to curtail risks of signiﬁcant losses due to adverse selection
by informed traders (e.g., hedge funds). Such actions are accompanied by market illiquidity and a
signiﬁcant fall in asset prices.
Easley et al. (2012) develop the Volume-Synchronized Probability of Informed Trading (VPIN)
model as a measure of order ﬂow toxicity and Easley et al. (2011b) show that the cumulative
distribution function (CDF) of VPIN would have been able to predict the “ﬂash crash” more than
an hour in advance. The VPIN is a metric of the probability that the liquidity provision process
might fail, thus resulting in adverse price movements. Our work investigates the application of
a version of VPIN, viz. Bulk Volume VPIN (BV-VPIN) to daily international equities data to
evaluate its eﬀectiveness in ascertaining the probability of sharp market movements, and its ability
to act as a safe haven or hedging tool if implemented via a futures contract.
Comparing a range of trade classiﬁcation algorithms that use tick data and the bulk volume of
trades, Easley et al. (2016) ﬁnd that BV-VPIN is closely linked to information-based trading proxies
such as Hi-Lo spreads and the permanent price eﬀect of trades. BV-VPIN appears incrementally
better than the original VPIN in discerning trade motivation from market data. Internationally,
Abad and Yage (2012) apply both BV-VPIN and Probability of Informed Trading (PIN) on the
Spanish equities market and conclude that BV-VPIN is a useful proxy for adverse selection risk.
They ﬁnd in particular that the Volume Bucket Size (VBS) input of the BV-VPIN can be adjusted
to capture transitory or permanent information in the trade data being analyzed, and further
conclude that BV-VPIN has potential applications in the context of low-frequency analyses, and
2


### Page 3

Electronic copy available at: http://ssrn.com/abstract=2791243
should not be limited to purely High Frequency Trading (HFT) environments.1
The BV-VPIN methodology has also been the subject of criticism. Andersen and Bondarenko
(2014b) ﬁnd contradictory results to those of Easley et al. (2011b) and document that BV-VPIN
is a poor predictor of short-term volatility. They suggest that any predictive content is due to a
mechanical relation with underlying trading intensity. However, Easley et al. (2014) argue that the
ﬁndings of Andersen and Bondarenko (2014b) are due to confusion in the methodology, analysis and
conclusions drawn from their work. Furthermore, Wu et al. (2013) analyze the 94 most active futures
contracts and ﬁnd BV-VPIN to be a strong predictor of liquidity-induced volatility. Andersen and
Bondarenko (2014a) and Andersen and Bondarenko (2015) continue to report that transaction-
based classiﬁcation schemes are more accurate than bulk volume strategies advocated by Easley
et al. (2011b) and Easley et al. (2012).
Given the apparent importance of implementation and market context to the predictive content
of BV-VPIN as an early warning signal of impending volatility, it is instructive to apply it across
a variety of international equity markets using daily data. That is the main purpose of our paper.
We analyze the impact of diﬀerent values for the VBS and the sample size applied as inputs into
BV-VPIN model based on the US market, to ascertain the optimal criteria for application across
all other countries in our dataset. We report the threshold value that is optimal across a variety
of countries. The economic value of BV-VPIN is evaluated by applying a scenario where a fund
manager exhibits a ﬂight-to-quality action by alternating investment between a riskless security
and the stock market when the BV-VPIN is above or below the threshold value over the length of
our dataset. Our study includes the evaluation of the safe haven and hedge properties of BV-VPIN
in the context of international equities markets.
We also show that BV-VPIN has potential application beyond that of HFT. The CDF of
BV-VPIN shows promise as a long-term predictor of market volatility. BV-VPIN also exhibits
safe haven and hedge characteristics during well-known crisis periods, e.g., Asian Financial Cri-
sis (AFC),Dot-com Bubble (DCB),Great Recession (GR), and the US Credit Rating Downgrade
(USCRD). Incorporating BV-VPIN as a ﬂight-to-quality indicator in an asset management appli-
cation results in substantial out performance of equity benchmark strategies for four out of six
countries analyzed in our study.
1 Given regulatory interests in promoting eﬃcient market trading mechanisms, Easley et al. (2011b) and Bell
(2013) recommend that regulators use BV-VPIN as an early warning signal to herald the implementation of regulatory
action to forestall crashes or identify unusual market conditions.
Easley et al. (2012) shows that BV-VPIN has
forecasting power over volatility (toxicity-induced) and advocate its use as a valuable risk management tool for
market making activity. BV-VPIN has application for trading strategies based on volatility arbitrage and for brokers
who seek to ascertain the optimal time of execution (Easley et al., 2015). Easley et al. (2011a) detail the speciﬁcations
of a BV-VPIN contract that could be used as a hedge against the risk of higher than expected levels of toxicity and
to monitor such risk. VPIN has been applied in the empirical ﬁnance literature to evaluate the market reaction to
public and private information (Vega, 2006), market anomalies (Kang, 2010; Chen and Zhao, 2012), asset pricing
(Aslan et al., 2011), and more. Corcoran (2012) discuss how VPIN can be applied to detect mini-bubbles based upon
the idea of monitoring the probability of toxicity-induced liquidity crises.
3


### Page 4

Our contributions are threefold.
First, we apply the BV-VPIN to an international equities
dataset including US, UK, Germany, Japan, Australia, and China and analyze its performance
over a dataset spanning 16 years. To the best of our knowledge, no other studies have carried
out such a comprehensive analysis that applies VPIN-based measures across diﬀerent international
markets. Second, our dataset allows us to determine the optimal thresholds for VPIN to predict
large down movements across a range of international equities markets. Third, we analyze whether
BV-VPIN is useful for safe haven and hedging properties if it were implemented as a futures contract
as suggested by Easley et al. (2011a).
The remainder of this paper is organized as follows. Section 2 presents the descriptive statistics
of our datasets and Section 3 details the BV-VPIN algorithm and parameters selected in our study.
The results and conclusions of our study are reported in Section 4 and Section 5, respectively.
2. Data
Our dataset includes daily equity returns and volume data for US (S&P500), UK (FTSE100),
German (DAX), French (CAC40), Japanese (Nikkei 225), Chinese (SHCOMP), and Australian
(AS30) indices, sourced from the Bloomberg data terminal. The period covered is 1995 to 2015 for
all countries except China. For China, our dataset extends from 1997 to 2015.
Table 2 provides descriptive statistics for our data of both daily returns and volume data for
all indices. Japan is the only country to have a negative mean return. The standard deviation of
daily returns is similar across all countries, with Australia exhibiting the lowest. All indices exhibit
negative skewness. The US exhibits the highest levels of kurtosis, and Germany and China the
lowest. The null hypotheses of normality is rejected at the 1% for all countries using the Jarque-
Bera test.2 The daily volume characteristics are such that most countries exhibit similar mean
daily volumes with China (Germany) being the highest (lowest). The daily volume data of China
also exhibits the highest positive skewness and kurtosis.
3. Measures of order ﬂow toxicity
VPIN is related to order ﬂow toxicity. The higher the order ﬂow toxicity, the greater the potential
for a negative impact for market makers from being adversely selected by informed traders. When
toxicity levels are too high, market makers will leave the market resulting in a reduction in liquidity
and short-term toxicity-induced volatility.
VPIN uses volume imbalance to signal the toxicity of order ﬂow, and the overall level of volume
determines the frequency for VPIN metric updates. VPIN is updated based upon ﬁxed units of
volume, rather than ﬁxed units of time.
The most important feature of VPIN is its emphasis
2For brevity, we do not report the Jarque-Bera test-statistic. These results can be provided upon request.
4


### Page 5

Table 1: Descriptive statistics of daily returns and trading volume of international indices
This table shows the descriptive statistics of daily returns and volume data for indices from 6 diﬀerent countries. Our
dataset spans from January 1995 to December 2015, except for the SHCOMP (China) that spans from November
1997 to December 2015. The sample size indicates the number of days of data for each equities index. The mean,
minimum, and maximum are presented as percentages.
Countries
Indices
Mean
Std. Dev.
Skew
Kurt.
Min.
Max.
Sample size
Panel A: Daily Returns
United States
S&P 500
0.03
0.0121
-0.2449
8.0496
-9.47
10.96
5288
United Kingdom
FTSE 100
0.01
0.0117
-0.1639
5.9236
-9.27
9.38
5334
Germany
DAX
0.03
0.0150
-0.1273
4.1825
-8.87
10.80
5320
Japan
Nikkei 225
-0.0007
0.0153
-0.2901
5.3782
-12.11
13.23
5160
China
SHCOMP
0.02
0.0164
-0.2585
4.3751
-9.26
9.40
4355
Australia
AS30
0.02
0.0095
-0.5590
6.4182
-8.55
6.07
5315
Panel B: Daily Volume
United States
S&P 500
9.39e+08
4.87e+08
0.5390
-0.2553
1.23e+06
2.96e+09
5288
United Kingdom
FTSE 100
9.98e+08
6.06e+08
0.6116
0.1695
5.00e+00
4.41e+09
5334
Germany
DAX
8.78e+07
6.25e+07
1.1347
3.3525
7.72e+05
4.97e+08
5320
Japan
Nikkei 225
9.48e+08
6.38e+08
1.0151
2.4677
7.09e+07
5.95e+09
5160
China
SHCOMP
7.75e+09
1.10e+10
3.1178
11.9300
1.23e+08
8.57e+10
4355
Australia
AS30
6.33e+08
4.34e+08
1.0159
3.5692
3.48e+05
5.64e+09
5315
on volume as a critical variable in understanding price adjustments and its linkage to underlying
information dynamics. In HFT markets, Easley et al. (2012) argue that traders operate on a volume
basis and focus on turning over holdings within speciﬁc numbers of contracts traded, as opposed
to over speciﬁc time intervals. We next explain the VPIN and BV-VPIN measures in detail and
then analyze whether the latter’s auxiliary information enables better prediction of adverse market
conditions when applied to daily international index data.
3.1. Volume-Synchronized Probability of Informed Trading (VPIN)
VPIN is based upon the PIN model that Easley et al. (1996) put forward as a measure of information
asymmetry between informed and uninformed trades.
PIN is premised on uninformed traders
buying or selling regardless of whether new information exists, and informed trading occurring
only when new information exists and buying (selling) upon arrival of good (bad) news. PIN is not
a directly observable measure and is a function of the theoretical parameters of a microstructure
model that is calculated using Maximum Likelihood Estimation (MLE) by ﬁtting a mixture of three
Poisson distributions (Easley et al., 1997). However, the numerical optimization procedure often
has diﬃculty converging and estimations may be biased (Easley et al., 2010; Lin and Ke, 2011;
Abad and Yage, 2012). These diﬃculties are exacerbated with the sheer size of HFT data sets.
PIN is based on a sequential trading model with Bayesian updates as shown in Equation (1).
PINt =
αtµ
αtµ + 2ϵ
(1)
The probability that new information will arrive within the time frame of the analysis is given
by α, and µ is the arrival rate of informed traders, assumed to follow a Poisson process. The arrival
5


### Page 6

rate of uninformed traders is given by ϵ. Easley et al. (2008) propose a dynamic econometric micro-
structure model of trading and show that for a suﬃciently large µ, the expected trade imbalance
(E

|V B −V S|

) and the expected total number of trades (E

|V B + V S|

) are given by Equations
(2) and (3), respectively.
E

|V B −V S|

≈αµ
(2)
E

|V B + V S|

≈αtµ + 2ϵ
(3)
where V B (V S) is the volume traded against the Ask (Bid).
Where PIN uses an itemized
classiﬁcation scheme to distinguish between buy and sell volume, Easley et al. (2012) propose an
approach called “bulk classiﬁcation” for VPIN. They argue that in a HFT environment, itemized
approaches can be problematic and suggest that instead of a calendar clock, a volume clock is
applied with a ﬁxed Volume Bucket Size (VBS). Using VBS is advantageous as it is analogous to
having a trading session split into periods of comparable information content and minimizes the
impact of volatility clustering.
A trade classiﬁcation algorithm is applied to identify the Buy (V B) and Sell (V S) volume. As
all volume bars are of a ﬁxed size, Easley et al. (2012) show that V can be given by Equation (4).
V = 1
N
N
X
τ=1
 V S
τ + V B
τ

= αµ + 2ϵ
(4)
For a given number of N volume bars, based on Equations (1), (2), (3) and (4) it can be shown
that VPIN is a good approximation of PIN and is given by Equation (5).
V PIN =
PN
τ=1 |V S
τ −V B
τ |
N × V
(5)
A high VPIN value indicates large order imbalances that may threaten liquidity provisions,
hence its application as a market liquidity indicator.
With access to tick data or order book
information, VPIN can be operationalized by adding the buy and sell volume of each volume bar.
However, tick data and market order data are often inaccurate, incomplete, or expensive to access.
Thus, trade classiﬁcation algorithms are often used to approximate the buy or sell volume.
3.2. Bulk Volume VPIN (BV-VPIN)
VPIN is often applied with one of three trade classiﬁcation algorithms: Tick Rule VPIN (TR-
VPIN), BV-VPIN, and Lee-Ready VPIN (LR-VPIN). Both TR-VPIN and BV-VPIN are Level-1
algorithms that only use trade price data. LR-VPIN is a Level-2 algorithm that uses both trade and
6


### Page 7

quote data, and is commonly applied in markets where it is diﬃcult to distinguish the initiating3
side of the trade.
Chakrabarty et al. (2012) report that the BV-VPIN is a more time-eﬃcient methodology
whereas TR-VPIN produces more accurate measures of order imbalance and order ﬂow toxicity.
They ﬁnd that both the TR-VPIN and BV-VPIN perform well when identifying the aggressor side
of trading, with the TR-VPIN being slightly more accurate. Easley et al. (2016) examines the ac-
curacy and eﬃciency of the BV-VPIN, LR-VPIN and Aggregated Tick Rule. The authors conclude
that tick rule approaches are relatively good classiﬁers of aggressor trades. However, BV-VPIN is
shown to be suﬃciently accurate for classifying buy and sell trades, and goes beyond tick-based
approaches by providing insight into other proxies for underlying trade information. Moreover, it
has the advantage of requiring substantially less data to implement.
In our study involving the analysis of daily data, we apply bulk volume classiﬁcation to calculate
the probability (i.e., portion) of buy and sell in each volume bar. Trades are aggregated over volume
intervals and the price change between the two consecutive intervals is used to approximate the
percentage of buy and sell order ﬂow. The amount of volume that is classiﬁed as Buy (ˆV B
τ ) and
Sell ( ˆV S
τ ) is given by Equations (6) and (7), respectively.
ˆV B
τ
= Vτ · t
Pτ −Pτ−1
σδp
, df

(6)
ˆV S
τ = Vτ ·

1 −t
Pτ −Pτ−1
σδp
, df

(7)
where Pτ is the single price ascribed to each current volume bar and Pτ−1 is the price of
previous volume bar. σδp represents the volume-weighted standard deviation of price change over
two consecutive volume bars. A volume bar is denoted as τ. A Student t distribution is used to
approximate the price changes, and probability of buy and sell volume is calculated by CDF of
the empirical price change distribution. The underlying trade is more likely to be buyer-initiated
(seller-initiated) if the price change is positive (negative) and larger in magnitude, relative to the
distribution of past price changes. Volume-weighted standard deviation is calculated by Equation
(8).
σ△Pi =
sPn
τ=1 Vi,τ(△Pi,τ −△Pi)2
Pn
τ=1 Vi,τ
(8)
3Baker and Kiymaz (2013) state that order ﬂow is deﬁned as the number of trades where the buyer was the
aggressor minus the number of trades where the seller was the aggressor. In a limit-order market (OTC market), the
aggressor is the agent placing a market order (requesting a quote).
7


### Page 8

4. Results
Easley et al. (2016) show that choices of the VBS and sample length greatly impact the implemen-
tation and estimation of BV-VPIN, and that the suitable selection of these variables is dependent
on optimizations being performed and should reﬂect the nature of trades within the market inves-
tigated. In Subsection 4.1 we discuss the choices available for diﬀerent parameters of BV-VPIN
and the values selected in our study across diﬀerent markets.
To protect against the risks of adverse selection and preserve the integrity of the liquidity
provision process, two approaches have been proposed. First, Zweig (2012) reports that exchanges
can dynamically adjust the speed of the trading engine. If bids are being struck at such a speed
that market makers are unable to adequately ﬁll liquidity demands, they will be forced out resulting
in a liquidity crash. Thus, the trading engine would decelerate (accelerate) the speed of matches
occurring at the bid (ask) price. In such an approach BV-VPIN can be used as early-warning
indicator for when exchanges should take action, and super-computing resources may be applied
accordingly (Wu et al., 2013). By calculating BV-VPIN for multiple international markets, we
analyze VPIN’s ability to forecast sharp downward movements at diﬀerent thresholds. We take
the view of a global-macro fund manager who decides to invest in each country’s equities index
when risks are low, and switches to the risk-free rate when risks are high. Henceforth, the economic
impact of VPIN is evaluated by switching to the risk-free rate (i.e., US 1-month T-bills) when VPIN
levels are high, and investing in equities index when VPIN levels are low. We report the outcomes
of this analysis in Subsection 4.2.
Second, Easley et al. (2011a) outline speciﬁcations of a VPIN futures contract, that oﬀers
market makers a hedge against the risk of higher than expected levels of toxicity (i.e., protection
against the rise in the probability of adverse selection for liquidity providers). Market makers would
purchase protection when their inventories are rising beyond normal levels. Informed traders would
sell that protection once their orders have been fulﬁlled, thus allowing them to monetize their
private knowledge that their contribution to toxicity has ceased. In Subsection 4.3, we analyze the
safe haven and hedge properties of the VPIN if implemented as a futures contract in accordance
with Easley et al. (2011a). Using the methodology of Baur and McDermott (2010) and Low et al.
(2016), we analyze whether the VPIN of each country exhibits safe haven and hedging properties
versus each country’s equities index during the extreme quintiles of the equities returns distribution
(e.g., 10%, 5%, 1%) and during well-known crisis periods.
4.1. Parameter selection for BV-VPIN
BV-VPIN takes price and volume as input parameters. Table 2 lists the key parameters to choose
when calculating BV-VPIN. We investigate the optimal parameters based upon the US dataset
and apply the same parameters for all other countries throughout our exploratory study. The US
8


### Page 9

Table 2: Parameters of BV-VPIN model
This table presents the key parameters of BV-VPIN model when applied in daily data.
The values used in our
analysis is given in the third column.
Description
Parameters
Parameters Selected
Number of volume bars
1000, 2000, 3000, 4000
2000
Rolling window size (bars)
10, 20, 50, 100
50
Distribution for price changes between volume bars
Normal, Student t (df=0.1, 0.25, 1, 5, 10)
Student t (df=5)
Student’s t distribution with df=5
Normal, Log-normal
Log-normal
equities market continues to be one of the largest and most heavily traded markets globally, and
therefore is an appropriate choice for a test case.
The bulk volume classiﬁcation algorithm requires each volume bar to be associated with a
single price. Wu et al. (2013) examine the performance under diﬀerent prices methodologies (e.g.,
average, weighted average, median, and weighted median) and ﬁnd that the results do not diﬀer
signiﬁcantly. We follow Easley et al. (2016) who suggest using the last price of each volume bar to
represent the price of the bar.
Prior literature applies ﬁxed values (e.g., 1000, 5000) for each volume bar. Our study calculates
BV-VPIN across equity indices from six countries where each market has diﬀerent trading volumes.
Therefore, it is impractical to use a single value for the volume bar for all diﬀerent markets. Thus,
we ﬁx the total number of bars such that the volume of each bar is approximately equal to the
total volume divided by the number of bars.
1999-09
2002-09
2006-01
2009-03
2014-07
Years
0.12
0.14
0.16
0.18
0.20
0.22
0.24
0.26
0.28
Probability
Number of volume bars=1000
VPIN
Index
600
800
1000
1200
1400
1600
1800
2000
2200
Index
1996-11
1999-02
2000-06
2001-04
2002-03
2002-12
2003-11
2004-12
2005-11
2006-09
2007-08
2008-09
2009-08
2010-10
2012-05
2014-05
Years
0.10
0.15
0.20
0.25
0.30
0.35
Probability
Number of volume bars=2000
VPIN
Index
600
800
1000
1200
1400
1600
1800
2000
2200
Index
1996-02
1998-04
1999-09
2000-10
2001-05
2002-02
2002-09
2003-05
2004-03
2005-03
2006-01
2006-09
2007-07
2008-05
2009-03
2010-03
2011-05
2012-09
2014-06
Years
0.05
0.10
0.15
0.20
0.25
0.30
0.35
0.40
Probability
Number of volume bars=3000
VPIN
Index
600
800
1000
1200
1400
1600
1800
2000
2200
Index
1995-08
1997-02
1998-04
1999-02
1999-10
2000-06
2001-01
2001-08
2002-03
2002-10
2003-06
2004-01
2004-08
2005-03
2005-10
2006-06
2007-01
2007-08
2008-04
2008-10
2009-06
2010-01
2010-08
2011-04
2011-12
2012-11
2014-01
2015-02
Years
0.05
0.10
0.15
0.20
0.25
0.30
0.35
0.40
Probability
Number of volume bars=4000
VPIN
Index
400
600
800
1000
1200
1400
1600
1800
2000
2200
Index
Figure 1: BV-VPIN and the CDF of BV-VPIN calculated for the US market (S&P500) with diﬀerent volume bar
sizes.
9


### Page 10

Figure 1 shows the BV-VPIN of the US market with diﬀerent volume sizes,keeping all other
parameters ﬁxed. Small volume sizes produce a more volatile BV-VPIN, increasing the degree of
noise into BV-VPIN’s CDF. Applying larger volume sizes “smoothens” the BV-VPIN but may
result in over-ﬁtting the BV-VPIN such that large impending price movements in the underlying
equities index go undetected. For each country investigated, the optimal choice for the volume bar
size may diﬀer. From Figure 1, a selection of 200 for the total number of volume bars looks to have
roughly the right balane of capturing salient downward features in the S&P500 index.
2010-01
2010-06
2010-10
2011-03
2011-08
2012-01
2012-06
2012-12
2013-07
2014-02
2014-10
2015-04
2015-10
Years
0.0
0.1
0.2
0.3
0.4
0.5
Probability
Rolling size=5
VPIN
Index
1000
1200
1400
1600
1800
2000
2200
Index
2010-01
2010-06
2010-10
2011-03
2011-08
2012-01
2012-06
2012-12
2013-07
2014-02
2014-10
2015-04
2015-10
Years
0.05
0.10
0.15
0.20
0.25
0.30
0.35
0.40
Probability
Rolling size=20
VPIN
Index
1000
1200
1400
1600
1800
2000
2200
Index
2010-01
2010-06
2010-10
2011-03
2011-08
2012-01
2012-06
2012-12
2013-07
2014-02
2014-10
2015-04
2015-10
Years
0.10
0.15
0.20
0.25
0.30
Probability
Rolling size=50
VPIN
Index
1000
1200
1400
1600
1800
2000
2200
Index
2010-01
2010-06
2010-10
2011-03
2011-08
2012-01
2012-06
2012-12
2013-07
2014-02
2014-10
2015-04
Years
0.12
0.14
0.16
0.18
0.20
0.22
0.24
0.26
0.28
Probability
Rolling size=100
VPIN
Index
1000
1200
1400
1600
1800
2000
2200
Index
Figure 2: BV-VPIN and the CDF of BV-VPIN calculated upon the US market (S&P500) where rolling-window
lengths vary.
The rolling window size (or volume buckets) is another important input parameter. Figure 2
shows the marginal eﬀect on the BV-VPIN curve of diﬀerent rolling window sizes. Smaller window
sizes follow price movements more closely but exhibit higher volatility. Larger window sizes result
in less volatile and smaller BV-VPIN peaks. As our application of BV-VPIN is in the context of a
long-term indicator of market liquidity in a low-frequency environment, we select 50 as the window
size to ensure that large adverse price movements are detected.
BV-VPIN classiﬁes trade volume based on the distribution of price changes over volume bars.
Easley et al. (2012) suggest that for high frequency data, a suitable choice is Student’s t distribution
with a df of 0.25. For daily data, we have ﬁtted our distributions using both Normal and Student’s
t distributions. Figure 3a is the kernel density of price changes versus the Normal and Student’s t
distribution. It is intuitive to expect the Student’s t distribution to provide a superior ﬁt to that
of the Normal distribution, due to the prevalence of kurtosis within our data set of international
10


### Page 11

8
6
4
2
0
2
4
6
0.0
0.1
0.2
0.3
0.4
0.5
0.6
Sample KDE
Normal distribution
20
15
10
5
0
5
10
15
20
0.0
0.1
0.2
0.3
0.4
0.5
0.6
Sample KDE
Student t distribution,df=5
(a) Distribution of price change
0.1
0.0
0.1
0.2
0.3
0.4
0.5
0
1
2
3
4
5
6
7
8
Sample KDE
Normal distribution
0.0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
0
1
2
3
4
5
6
7
8
Sample KDE
Log-normal distribution
(b) Distribution of VPIN
Figure 3: Distribution ﬁtting of price changes (across volume bars) of BV-VPIN of the US market (S&P500).
equities indices. Upon applying both the Normal and Student’s t distribution, our results show no
obvious diﬀerences between the two. We select the Student’s t distribution with df=5.
Applying BV-VPIN alone is not an eﬀective early warning signal. Easley et al. (2011b) shows
that the BV-VPIN rises almost simultaneously during prices drops and reaches its peak when
prices have stabilized.
Easley et al. (2014) shows that the CDF of BV-VPIN reaches its peak
before BV-VPIN, and successfully predicts the impending “ﬂash crash” in the E-mini S&P500. As
the BV-VPIN is calculated using absolute volume balances, we apply the log-normal distribution to
approximate the VPIN distribution. Figure 3b shows that the sample distribution of the S&P500
VPIN is more likely to follow a log-normal distribution. Wu et al. (2013) suggest that the log-
normal distribution accurately describes the BV-VPIN sample. They also recommend using the
truncated log-normal distribution to avoid the occurrence of extremely small BV-VPIN values. For
daily data, as BV-VPIN values are signiﬁcantly larger than zero, we use the ordinary log-normal
distribution with the CDF given by Equation (9).
1
2

1 + erf
ln x −µ
σ
√
2

(9)
where erf is the Gaussian error function, µ is the average of the log of BV-VPIN values, and σ
is the standard deviation.
11


### Page 12

4.2. BV-VPIN as an early warning signal
Figure 4 presents the BV-VPIN and CDF of BV-VPIN for equity indices in diﬀerent countries. We
deﬁne a “VPIN event” to occur when the CDF of BV-VPIN exceeds a threshold. Given that BV-
VPIN follows a lognormal distribution, a threshold may be selected based on mean and variation4.
In our implementation, we select 0.6, 0.8, and 0.9 as intuitive threshold values.
BV-VPIN tends to stabilize at 0.2 and then rises in concert with large price movements in
the underlying index. For example, in Figure 4a, the all-time high occurs during 2008-2009, also
the most volatile period for the S&P500. It is noticeable across all countries that BV-VPIN is
negatively correlated with level movements in the underlying index. However, BV-VPIN increases
almost simultaneously when the index starts to fall.
The CDF of BV-VPIN rises earlier and quicker than BV-VPIN and is more eﬀective as an
early-warning signal. All markets exhibit high BV-VPIN levels during well-known crises (e.g., 2008
Great Recession, 2011 US Credit Rating Downgrade). In the later months of our dataset, we can
see that BV-VPIN is relatively high, indicating that markets remain susceptible to volatility and
liquidity shocks despite the best eﬀorts of ﬁnancial regulators and central banks to improve credit
risk and market risk exposures within the ﬁnancial system.
As BV-VPIN is proportional to the absolute diﬀerence between buy and sell volume, any sudden
and large upward price movements should result in BV-VPIN rising sharply. However, empirically,
we are more likely to observe large and sudden price drops across US and international equities
(Longin and Solnik, 1995; Ang and Chen, 2002; Low et al., 2013). Thus, our analysis of prediction
accuracy investigates the eﬀectiveness of CDF of BV-VPIN in forecasting impending index falls.
Table 3 shows the prediction accuracy with diﬀerent thresholds applied. With 0.9 as a threshold
value, we have 100% prediction accuracy in 4 markets including US, UK, China and Australia, and
75% accuracy in Germany. Using the same threshold, only one BV-VPIN event is observed in
Japan. With a threshold value of 0.8, we have 75% prediction accuracy in only two countries.
Moreover, prediction accuracy is less than 50% in all countries if using 0.6 as threshold.
It is
intuitive to expect that lower thresholds will increase the number of false alarms, whereas a higher
threshold might miss market downturns. The results presented in Table 3 are based on Figure 4.
As BV-VPIN can hover around the threshold values, we only consider a BV-VPIN event to be the
ﬁrst breach of the threshold value.
Intuitively, when a BV-VPIN event occurs, it is important to evaluate both the magnitude of
the fall in the underlying index, and the time horizon over which it occurs. This allows the portfolio
manager to understand how much time he has to exit all of his equity position if he decides to heed
the BV-VPIN signal. Table 4 presents both the prediction accuracy and the index downturn with
respect to diﬀerent time horizons. We report our results applying a threshold value of 0.9 for all
4Wu et al. (2013) use two standard deviations greater than the average value to denote a “VPIN Event”.
12


### Page 13

1996-11
1999-02
2000-06
2001-04
2002-03
2002-12
2003-11
2004-12
2005-11
2006-09
2007-08
2008-09
2009-08
2010-10
2012-05
2014-05
2015-12
Years
0.0
0.2
0.4
0.6
0.8
1.0
Probability
VPIN
VPIN CDF
Index
600
800
1000
1200
1400
1600
1800
2000
2200
Index
(a) United States
1997-06
2000-03
2001-06
2002-06
2003-04
2004-02
2004-12
2005-11
2006-09
2007-07
2008-05
2009-04
2010-05
2011-10
2013-05
2015-02
Years
0.0
0.2
0.4
0.6
0.8
1.0
Probability
VPIN
VPIN CDF
Index
3000
3500
4000
4500
5000
5500
6000
6500
7000
7500
Index
(b) United Kingdom
1999-03
2001-09
2003-01
2004-03
2005-05
2006-05
2007-05
2008-02
2008-11
2009-10
2010-10
2011-08
2012-06
2013-04
2014-07
2015-10
Years
0.0
0.2
0.4
0.6
0.8
1.0
Probability
VPIN
VPIN CDF
Index
2000
4000
6000
8000
10000
12000
14000
Index
(c) Germany
1997-07
2000-10
2003-01
2004-07
2005-11
2006-12
2007-11
2008-10
2009-08
2010-07
2011-06
2012-05
2013-03
2013-11
2014-10
2015-08
Years
0.0
0.2
0.4
0.6
0.8
1.0
Probability
VPIN
VPIN CDF
Index
6000
8000
10000
12000
14000
16000
18000
20000
22000
Index
(d) Japan
2003-01
2006-11
2007-10
2009-02
2009-10
2010-09
2011-07
2012-08
2013-08
2014-07
2015-01
2015-06
2015-11
Years
0.0
0.2
0.4
0.6
0.8
1.0
Probability
VPIN
VPIN CDF
Index
1000
2000
3000
4000
5000
6000
7000
Index
(e) China
1997-12
2001-03
2003-02
2004-07
2005-11
2007-02
2008-01
2008-12
2009-09
2010-05
2011-03
2011-12
2012-10
2013-09
2014-09
2015-10
Years
0.0
0.2
0.4
0.6
0.8
1.0
Probability
VPIN
VPIN CDF
Index
2500
3000
3500
4000
4500
5000
5500
6000
6500
7000
Index
(f) Australia
Figure 4: BV-VPIN and CDF of BV-VPIN for international equities indices.
13


### Page 14

Table 3: Prediction Properties of BV-VPIN
This table presents the prediction properties of BV-VPIN; a BV-VPIN Event occurs when the CDF of BV-
VPIN exceeds the threshold value. Price drops are ascertained by any negative return that occurs within a
horizon of 30 to 60 days after the BV-VPIN event occurs. Prediction accuracy is determined as the number
of actual negative returns on the respective index, divided by the total number of BV-VPIN events.
Threshold
Number of BV-VPIN Events
Number of Price drops
Prediction Accuracy
Panel A: United States
0.9
4
4
100%
0.8
5
3
60%
0.6
5
2
40%
Panel B: United Kingdom
0.9
3
3
100%
0.8
4
3
75%
0.6
14
6
43%
Panel C: Germany
0.9
4
3
75%
0.8
5
3
60%
0.6
8
3
38%
Panel D: Japan
0.9
1
0
0%
0.8
4
3
75%
0.6
10
3
30%
Panel E: China
0.9
2
2
100%
0.8
1
2
50%
0.6
3
1
33%
Panel F: Australia
0.9
3
3
100%
0.8
4
1
25%
0.6
7
1
14%
14


### Page 15

Table 4: Prediction Horizon of BV-VPIN
This table presents the prediction properties of BV-VPIN when using ﬁxed thresholds of 0.9 for all
countries, except Japan. For Japan, a threshold value of 0.8 is used. Prediction accuracy denotes the
number of index drops out of the total number of BV-VPIN events where the CDF of BV-VPIN exceeds
the threshold value. The Average Index Change indicates the average index returns based upon the
number of days after a BV-VPIN event occurs. The Average Index Change (Negative) indicates the
average index returns only when the BV-VPIN event precedes a drop in the index.
Prediction Horizon
Prediction Accuracy
Average Price Drop
Average Price Drop
(Days)
(Negative Returns)
(All Returns)
Panel A: United States
5
3/4
-3.83%
-1.09%
20
3/4
-7.00%
-3.27%
60
2/4
-5.42%
2.74%
120
2/3
-13.06%
-4.60%
Panel B: United Kingdom
5
2/3
-3.04%
4.03%
20
2/3
-6.81%
-2.46%
60
1/3
-18.41%
-4.72%
120
2/3
-2.70%
-1.25%
Panel C: Germany
5
1/3
-8.55%
-0.16%
20
1/3
-1.12%
2.15%
60
2/3
-4.43%
-2.26%
120
3/3
-3.33%
-3.33%
Panel D: Japan
5
3/4
-4.33%
-3.05%
20
3/4
-4.87%
-2.10%
60
2/3
-9.44%
-5.82%
120
2/3
-9.48%
-5.86%
Panel E: China
5
0/2
n.a.
1.62%
20
1/2
-4.05%
4.88%
60
1/2
-19.15%
-0.06%
120
2/2
-5.57%
-5.57%
Panel F: Australia
5
3/4
-3.60%
-2.44%
20
3/4
-2.35%
-1.51%
60
2/3
-16.04%
-10.67%
120
2/3
-20.20%
-13.26%
15


### Page 16

countries except Japan, for which a threshold value of 0.8 is used. We record the dates associated
with each BV-VPIN Event, and use the index level at these dates as the benchmark level. We
observe prices 5, 20, 60 and 120 trading days after the BV-VPIN Event. Based on these values, we
calculate the fall in the index for each BV-VPIN Event over diﬀerent time horizons.
The calculation for the average index fall for negative returns is based solely upon BV-VPIN
events that resulted in an index fall. For example, over the one-month prediction horizon for the
US index, there are four BV-VPIN events, two of which resulted in index falls and two that were
false alarms. The calculation for the average price drop for all returns is based upon all BV-VPIN
events regardless of whether there was a index drop after the event. This allows us to understand
the average index drop if BV-VPIN thresholds are breached whilst taking into account the impact
of false alarms. The average index drop after a BV-VPIN event is calculated as given by Equation
(10).
PDavg,tf = 1
tf
tf
X
i=1
Ri
(10)
Ri = Pi −Pt0
Pt0
(11)
The day of the BV-VPIN event occurs is given by t0, and tf represents 5, 20, 60 or 120 trading
days after the BV-VPIN event. When calculating the average price drop for negative returns, we
only include Ri < 0. In this scenario, the average price drop is solely based on the average of the
two BV-VPIN events that resulted in price drops. In this manner, we understand the magnitude
of the price drop when the BV-VPIN threshold is breached and a price drop has been accurately
predicted.
Table 4 shows that prediction accuracy and the average price drops vary across diﬀerent markets
and prediction horizons. We see that when the BV-VPIN event accurately predicts a price drop,
we can expect to see a negative return of more than 9% in the following period of 60 or 120 days
(except for Germany). However, within the ﬁrst 5 days, we observe price drops of about 5% or less
(except for China and Germany). One can conclude that once the BV-VPIN threshold is breached,
a portfolio manager has at least 30 days to exit his positions to minimize the magnitude of losses.
When accounting for all BV-VPIN events (i.e., including the impact of false alarms), we see that
after 120 trading days, all six countries experienced drops in the index ranging from -1.25% (UK)
to -13.26% (Australia). Within the ﬁrst 5 and 20 trading days, we observe an index drop in 4
countries. Our results indicate that there are substantial drops in each country’s index after a
BV-VPIN event.
4.3. BV-VPIN as a hedge and safe haven investment
To evaluate the hedge and safe haven properties of BV-VPIN if implemented as a futures contract,
our analysis utilizes the following model as shown in Equation (12)-(14).
16


### Page 17

rV PIN,t = a + btrindex,t + εt
(12)
bt = c0 + c1D(rindexq10) + c2D(rindexq5) + c3D(rindexq1)
(13)
ht = ω + αε2
t−1 + βht−1
(14)
Equation (12) models the relationship between the CDF of BV-VPIN (rV PIN,t) and each indi-
vidual country’s equity index (rindex,t). The parameter bt is modeled as a dynamic process given
by Equation (13). Indicator variables (D(. . . )) are applied to capture extreme market movements,
taking a value of one if stock market return at time t exceeds a certain threshold given by the 10%,
5% and 1% quantile of the return distribution, and zero otherwise. The residual term εt is modeled
as a GJR-GARCH process (Glosten et al., 1993) that takes into account volatility clustering and
asymmetries in the ARCH process. All equations are jointly estimated with MLE. Such models
have been applied in analyzing the safe haven and hedge properties of commodities such as precious
metals (Baur and McDermott, 2010) and diamonds (Low et al., 2016).
Table 5: Hedge and safe haven properties of BV-VPIN
This table presents the estimation results for the coeﬃcients in Equation 13.
Negative coeﬃcients in the hedge
column (c0) signify that the asset is a hedge against index. Zero (negative) coeﬃcients in extreme market conditions,
namely quantile 10% (c1), 5% (c2), and 1% (c3) indicate that the asset is a weak (strong) safe haven. Each column
of t-statistics is associated with the coeﬃcient column to the left, as an indication of the signiﬁcance level.
Countries
Indices
Hedge
t-stats
Safe haven quantiles
10%
t-stats
5%
t-stats
1%
t-stats
US
S&P 500
0.055
3.373
-0.178***
-3.846
0.033
0.697
-0.041
-1.187
UK
FTSE 100
0.060
3.566
-0.191***
-4.160
0.104
2.263
-0.144***
-3.763
Germany
DAX
0.051
4.248
-0.155***
-4.188
0.012
0.319
-0.061**
-2.003
Japan
Nikkei 225
0.041
2.971
-0.133***
-3.930
-0.003
-0.010
-0.062**
-2.261
China
SHCOMP
0.144
8.356
-0.286***
-5.542
-0.021
-0.382
-0.017
-0.408
Australia
AS30
0.090
3.690
-0.207***
-3.456
-0.130**
-1.967
-0.018
-0.341
*,**,*** indicates statistical signiﬁcance at the 10%, 5%, and 1% level, respectively.
If any of the parameters (c1, c2, c3) are signiﬁcantly diﬀerent from zero, this suggests a re-
lationship between BV-VPIN and the country’s index.
If the parameters in Equation (13) are
non-positive, BV-VPIN acts as a weak safe haven. If the parameters are negative and statistically
diﬀerent from zero, BV-VPIN becomes a strong safe haven. Where c0 is zero or negative, and the
sum of the parameters c1 to c3 are not jointly positive (exceeding the value of c0), BV-VPIN serves
as a hedge, where negative c0 suggests strong hedging attributes and a value of zero indicates weak
hedging attributes.
The estimated results of the regression model given by Equations (12), (13), and (14) are
reported in Table 5 which contains the estimates of c0, c1, c2 and c3. Under the GJR-GARCH
model, it is shown that BV-VPIN is a strong safe haven in all six countries within the 10% quantile
with strong statistical signiﬁcance. At the 1% quantile, BV-VPIN remains an eﬀective safe haven
in all six countries, particularly in UK, Germany, and Japan where the coeﬃcients are statistically
17


### Page 18

signiﬁcant. Only Japan, China, and Australia exhibit safe haven qualities at the 5% level, with
Australia’s results being statistically signiﬁcant. All six countries have positive coeﬃcients for c0,
suggesting that BV-VPIN does not exhibit suitable qualities for hedging.
Table 6: Hedge and safe haven properties of BV-VPIN during periods of ﬁnancial stress
This table presents the estimation results for the coeﬃcients in Equation 15. The duration of crisis periods is set to
be 20 days after the crisis starts. Negative coeﬃcients in the hedge column (c0) signify that BV-VPIN is a hedge
against the market. Negative coeﬃcients in subsequent columns show that it is a safe haven during the AFC (c1),
DCB (c2) GR (c3) or USCRD (c4). Each t-statistics column is associated with the coeﬃcient column to the left, as
an indication of the signiﬁcance level.
Countries
Hedge
1997 AFC
2000 DCB
2008 GR
2011 USCRD
Coeﬀ.
t-stats
Ttl. eﬀ.
t-stats
Ttl. eﬀ.
t-stats
Ttl. eﬀ.
t-stats
Ttl. eﬀ.
t-stats
US
-0.004
-0.365
0.022
0.123
-0.055
-0.202
-0.150***
-2.798
-0.192***
-2.861
UK
0.004
0.279
0.353
2.014
-0.170
-0.570
0.503
16.880
-0.302***
-2.841
Germany
-0.010
-1.173
n.a.
n.a.
-0.020
-0.106
-0.408***
-6.907
-0.100**
-2.133
Japan
-0.019**
-2.139
-0.087
-1.008
-0.053
-0.198
-0.056
-0.766
0.221
2.620
China
0.003
0.227
n.a.
n.a.
n.a.
n.a.
0.088
0.782
-0.224**
-2.493
Australia
-0.035**
-2.118
n.a.
n.a.
0.236
0.759
-0.083
-0.983
-0.140
-1.147
*,**,*** indicates statistical signiﬁcance at the 10, 5, and 1 percent level, respectively.
Equation 15 allows the analysis of hedge and safe haven properties during crisis sub-sample
periods. By identifying well known ﬁnancial crisis periods, we apply time dummies equal to one if
the returns fall within the pre-deﬁned period and a zero otherwise. We deﬁne starting dates and
assume that most of the crisis and its eﬀects occurred in the ﬁrst 20 trading days (approximately
one month) from the start date (Baur and McDermott, 2010). Four major ﬁnancial events occurred
in the sample period of our investigation, namely the Asian Financial Crisis (AFC) (Oct. 22, 1997
- Nov. 19, 1997), the Dot-com Bubble (DCB) (Mar. 10, 2000 - Apr. 7, 2000), the Great Recession
(GR) (Sept. 12, 2008 - Oct. 2, 2008) and the US Credit Rating Downgrade (USCRD) (Jul. 23,
2011 - Aug. 12, 2011).
bt = c0 + c1D(AFC) + c2D(DCB) + c3D(GR) + c4D(USCRD)
(15)
If the parameters c1, c2, c3 or c4 are zero or negative, BV-VPIN is a safe haven during the
respective crisis period. Alternatively, a positive parameter means that the asset moves in tandem
with the market and is not a safe haven.
Table 6 presents the estimation results of the model in Equation (15). For Germany, China, and
Australia the results for AFC and DCB are unavailable due to the sample length of our dataset and
the structure of our empirical analysis applied to calculate BV-VPIN. When calculating BV-VPIN,
we group trade data across several days into one volume bar, then compute BV-VPIN based on a
rolling window of 50 volume bars. Thus, there are no BV-VPIN values for the initial 49 volume
bars. Moreover, the trading volume is relatively small in the earlier time periods of our data set.
If a ﬁxed-size volume bar is applied, each of the initial volume bars contains 5-10 days of data.
18


### Page 19

Thus, for certain countries the BV-VPIN values are unavailable for the initial months or years in
our data set.
We ﬁnd that three countries have BV-VPIN values associated with the AFC, and only in Japan
does BV-VPIN exhibit some safe haven properties. During the DCB, all countries except Australia
exhibit safe haven properties.
During the GR, BV-VPIN exhibits safe haven qualities in four
countries, particularly in the US and Germany where the coeﬃcients are statistically signiﬁcant
at 1%. In the UK and China, BV-VPIN is not an eﬀective safe haven during the GR. BV-VPIN
is a strong safe haven in all countries except for Japan during the period around the US credit
downgrade. It exhibits statistical signiﬁcance in US, UK, Germany, and Australia. In four countries
out of six, BV-VPIN exhibits hedging qualities. In both Japan and Australia, signiﬁcant negative
coeﬃcients are observed, thus indicating strong hedge properties against market crises.
These
results show that if the BV-VPIN is operationalized as a futures contract, it would exhibit suitable
safe haven and hedge characteristics for asset managers who wish to protect themselves from the
high-volatility and liquidity shocks that may occur from order imbalances.
4.4. BV-VPIN in a risk-on/risk-oﬀtrading strategy
We test a risk-on/risk-oﬀtrading strategy based on the CDF of BV-VPIN. Investments are in
equities (risk-on) when the CDF of BV-VPIN is below a set threshold, otherwise we invest in the
risk-free rate (risk-oﬀ). Equities are represented by each country’s stock index, and the risk-free
rate used is the US 10-year treasury rate. We refer to this strategy as the BV-VPIN Strategy. For
comparable benchmark strategies, we report the realized returns on a Buy-and-Hold investment in
(1) Equities and (2) Risk-Free Rate (RF).
Table 7 represents the performance of these three strategies for each of six diﬀerent countries.
Similar to the analysis of prediction accuracy in Subsection 4.2, threshold values of 0.6, 0.8, and
0.9 are applied. We report descriptive statistics such as the mean, standard deviation, skewness,
and kurtosis. Risk-adjusted returns performance is given by the Sharpe Ratio (Sharpe, 1994) and
the Sortino Ratio (Sortino and Satchell, 2001) that capture total volatility and downside volatility,
respectively. The initial investment for each approach is assumed to be $100, and we report the Final
Value (FV) and the Total Return (TR) that is reported in dollars and percentages, respectively.
Across all countries with the exception of Germany, all the strategies exhibit negative skewness,
the highest being the BV-VPIN strategies at a threshold of 0.6 and the lowest being the RF strategy.
Aside from RF, across all countries the BV-VPIN and Equities strategies exhibit excess kurtosis.
For all six countries, investment in the RF produces the highest Sharpe Ratio due to its low
values of standard deviation. The BV-VPIN strategy with the optimal threshold outperforms the
Equities strategy. In the US market, the BV-VPIN strategy with a threshold of 0.9 has the highest
Sharpe ratio. In China, the Sharpe ratio of using BV-VPIN strategy is double that of the Equities
strategy. In Japan, BV-VPIN strategy with athreshold of 0.6 produces a Sharpe Ratio ﬁve times
larger than the Equities strategy. As measured by the Sortino ratio, the BV-VPIN strategy with
19


### Page 20

Table 7: Evaluation of BV-VPIN in trading strategy
This table compares the performance of investing in (1) BV-VPIN; a risk-on/risk-oﬀstrategy that invests in the
respective country’s equities index (risk-free rate) when the BV-VPIN is below (above) a set threshold, (2) Equities;
a Buy-and-Hold Strategy in each country’s stock index, and (3) Risk-Free; a Buy-and-Hold Strategy in in the form
of US 10-year treasury rate. The distribution characteristics of each (e.g., Mean, Standard Deviation, Skewness, and
Kurtosis) for each strategy are reported. Risk-adjusted returns are reported with the Sharpe and Sortino Ratios.
The ﬁnal value of investment by investing an initial sum of $100 is given by FV ($), and TR (%) is the total return of
the strategy. The Sortino Ratio for the risk-free rate is not applicable as the RF rate is never negative in our dataset.
Strategy
Threshold
Mean
Std. Dev.
Skew
Kurt.
Sharpe
Sortino
FV ($)
TR(%)
Panel A: United States
0.9
0.026
1.123
-0.158
7.363
0.024
0.033
263
163.17
BV-VPIN
0.8
0.020
0.941
-0.205
5.907
0.021
0.029
207
107.41
0.6
0.015
0.661
-0.435
10.382
0.023
0.032
187
86.51
Equities
0.029
1.252
-0.043
7.616
0.023
0.033
273
172.97
Risk-Free
0.011
0.004
-0.025
-0.934
2.974
n.a.
169
69.11
Panel B: United Kingdom
0.9
0.012
1.099
-0.132
6.752
0.011
0.016
135
34.82
BV-VPIN
0.8
0.007
0.992
-0.343
7.571
0.007
0.010
112
11.71
0.6
0.013
0.619
-0.314
13.662
0.022
0.030
172
71.87
Equities
0.014
1.224
-0.009
5.491
0.011
0.016
134
34.02
Risk-Free
0.011
0.004
-0.069
-0.979
3.030
n.a.
165
65.34
Panel C: Germany
0.9
0.028
1.407
0.152
6.867
0.020
0.029
218
118.50
BV-VPIN
0.8
0.034
1.195
0.098
9.777
0.028
0.040
310
209.68
0.6
0.021
0.869
-0.281
15.859
0.024
0.034
210
109.68
Equities
0.030
1.535
0.115
4.432
0.019
0.027
214
113.59
Risk-Free
0.010
0.003
0.036
-0.874
3.024
n.a.
155
55.22
Panel D: Japan
0.9
0.029
1.243
-0.409
11.415
0.023
0.032
262
162.24
BV-VPIN
0.8
0.021
1.100
-0.596
6.597
0.019
0.026
193
92.55
0.6
0.035
0.891
-0.750
11.036
0.039
0.055
407
307.24
Equities
0.011
1.553
-0.146
5.440
0.007
0.010
96
-3.65
Risk-Free
0.011
0.004
-0.085
-0.976
3.044
n.a.
163
62.50
Panel E: China
0.9
0.075
1.379
-0.364
4.091
0.054
0.078
773
673.27
BV-VPIN
0.8
0.062
1.218
-0.224
5.211
0.051
0.074
562
461.98
0.6
0.053
0.930
-0.239
7.927
0.057
0.084
463
363.61
Equities
0.044
1.686
-0.287
3.716
0.026
0.036
255
154.90
Risk-Free
0.009
0.003
-0.100
-1.258
3.306
n.a.
133
33.14
Panel F: Australia
0.9
0.031
0.829
-0.251
3.003
0.037
0.052
346
246.05
BV-VPIN
0.8
0.031
0.772
-0.346
3.168
0.040
0.057
361
260.79
0.6
0.017
0.577
-0.583
6.035
0.029
0.040
198
98.17
BH
0.021
0.967
-0.431
5.317
0.022
0.030
209
108.99
20


### Page 21

the optimal threshold also outperforms Equities in all countries with the exception of the US. In
the US market, BV-VPIN strategy has the same Sortino ratio as Equities. Generally, we ﬁnd that
the BV-VPIN strategy results in higher risk-adjusted returns.
When analyzing the ﬁnal wealth value and total return of each strategy, application of the
optimal BV-VPIN threshold outperforms both the Equities and RF with the exception of the US.
With a threshold of 0.9, the ﬁnal wealth of the BV-VPIN strategy comes close to the Equities
for the US. For the UK, equities generally performed poorly in comparison to investing in RF.
However, with a threshold of 0.6, the BV-VPIN strategy outperforms the both Equities and RF. In
Germany, BV-VPIN strategy at thresholds of 0.9 and 0.8 successfully outperform both the Equities
and RF strategies. In the Japanese market, Equities performs poorly compared to RF. However,
applying the BV-VPIN strategy results in 307% returns with a threshold of 0.6, that is ﬁve times
greater than the return from investing in the RF. The BV-VPIN strategy, regardless of threshold
value, successfully outperforms the Equities and RF in China. With a threshold value of 0.9, the
BV-VPIN strategy generates a fourfold return compared to the Equities, a threefold return for
threshold of 0.8, and twofold return for threshold of 0.6. In Australia, application of the BV-VPIN
strategy doubles the return on investment compared to the Equities strategy.
Figure 5 shows the accumulation of wealth with an initial investment of $100 dollars using
Equities and BV-VPIN strategies with diﬀerent thresholds. We ﬁnd that the BV-VPIN strategy
eﬀectively avoids large losses during extreme market downturns. For China and Australia, the
BV-VPIN strategy suggests investing in the risk-free asset before the market drops and reinvesting
in equity as market starts to recover. Speciﬁcally,we observe that in China, Australia, UK, and
Japan the BV-VPIN avoids investing in equities during the GR period.
The optimal threshold to be applied for the BV-VPIN varies across diﬀerent markets.
For
China and US, 0.9 is optimal, whilst in Australia and Germany, 0.8 produces the highest returns.
In UK and Japan, 0.6 signiﬁcantly outperforms higher thresholds. Our results indicate that one
should tailor the choice of the optimal threshold depending on the market. However, application
of a threshold value of 0.8 seems result in robust and proﬁtable performance across all markets
investigated in our study.
5. Conclusion
A structural model for market micro-structure research proposed by Easley et al. (1996) provides for
the estimation of Probability of Informed Trading (PIN). The importance of PIN is that it provides
a measure of order ﬂow toxicity which can have a negative impact on market liquidity. With the
advent of High Frequency Trading (HFT), Easley et al. (2012) develop a modiﬁed measure, Bulk
Volume VPIN (BV-VPIN) where the probability of informed trading is based on volume imbalance
and trade intensity.
Market makers’ estimates of time-varying toxicity level are a crucial factor in determining their
21


### Page 22

1996-11
1997-11
1998-10
1999-10
2000-09
2001-08
2002-08
2003-07
2004-07
2005-06
2006-06
2007-05
2008-05
2009-04
2010-04
2011-03
2012-02
2013-02
2014-01
2015-01
2015-12
Date
50
100
150
200
250
300
Value ($)
Buy-and-hold
BV-VPIN(0.9)
BV-VPIN(0.8)
BV-VPIN(0.6)
(a) United States
1997-06
1998-06
1999-05
2000-04
2001-03
2002-02
2003-01
2004-01
2004-12
2005-11
2006-10
2007-09
2008-08
2009-07
2010-06
2011-05
2012-04
2013-03
2014-02
2015-01
2015-12
Date
60
80
100
120
140
160
180
200
Value ($)
Buy-and-hold
BV-VPIN(0.9)
BV-VPIN(0.8)
BV-VPIN(0.6)
(b) United Kingdom
1999-03
2000-01
2000-11
2001-09
2002-07
2003-05
2004-03
2005-01
2005-11
2006-09
2007-07
2008-06
2009-04
2010-02
2010-12
2011-10
2012-08
2013-06
2014-04
2015-02
2015-12
Date
0
50
100
150
200
250
300
350
Value ($)
Buy-and-hold
BV-VPIN(0.9)
BV-VPIN(0.8)
BV-VPIN(0.6)
(c) Germany
1997-07
1998-06
1999-05
2000-04
2001-03
2002-02
2003-01
2003-12
2004-11
2005-10
2006-09
2007-08
2008-07
2009-06
2010-06
2011-05
2012-04
2013-03
2014-02
2015-01
2015-12
Date
0
50
100
150
200
250
300
350
400
450
Value ($)
Buy-and-hold
BV-VPIN(0.9)
BV-VPIN(0.8)
BV-VPIN(0.6)
(d) Japan
2003-01
2003-09
2004-05
2004-12
2005-08
2006-04
2006-12
2007-08
2008-03
2008-11
2009-07
2010-03
2010-10
2011-06
2012-02
2012-09
2013-05
2014-01
2014-09
2015-05
2015-12
Date
0
200
400
600
800
1000
Value ($)
Buy-and-hold
BV-VPIN(0.9)
BV-VPIN(0.8)
BV-VPIN(0.6)
(e) China
1997-12
1998-11
1999-09
2000-08
2001-07
2002-06
2003-05
2004-03
2005-02
2006-01
2006-12
2007-11
2008-10
2009-08
2010-07
2011-06
2012-05
2013-04
2014-02
2015-01
2015-12
Date
50
100
150
200
250
300
350
400
450
Value ($)
Buy-and-hold
BV-VPIN(0.9)
BV-VPIN(0.8)
BV-VPIN(0.6)
(f) Australia
Figure 5: Accumulation of wealth of using diﬀerent trading strategy for international equities indices.
22


### Page 23

participation such that if they believe that toxicity is high, they will liquidate their positions
and leave the market, thus aﬀecting market liquidity. Henceforth, BV-VPIN is a procedure that
estimates the probability of informed trading based on volume imbalance and trade intensity.
Empirical tests suggest that BV-VPIN functions not only as an indicator of current market
liquidity but also as an early warning signal for impending volatility. Although BV-VPIN itself is
not eﬀective in predicting future price movements, the cumulative distribution function (CDF) of
BV-VPIN exhibits predictive properties in a HFT environment (Easley et al., 2011b). Abad and
Yage (2012) propose that alternative speciﬁcations of the BV-VPIN model can result in alternative
gauges for adverse selection. Thus, they suggest that BV-VPIN can be a broad measure of adverse
selection beyond that of HFT applications.
We apply BV-VPIN on daily equities data across a range of international equities indices. We
select optimal parameters for BV-VPIN based on the US market and apply it across a range of
major global economies to ascertain its capabilities as a long-term indicator of market liquidity and
impending market downturns. Our work includes the analysis of BV-VPIN’s role as a safe haven
and hedge instrument if implemented as a futures contract as suggested by Easley et al. (2011a).
To investigate the economic signiﬁcance of BV-VPIN as an early warning signal, we apply it in a
risk-on/risk-oﬀtrading strategy where an asset manager invests in equities (risk-free rate) when
the CDF of BV-VPIN is below (above) a threshold value.
We ﬁnd that CDF of BV-VPIN exhibits predictive properties, however, the selection of threshold
value can vary across diﬀerent countries. This is in line with Easley et al. (2014) who contend that
the selection of parameters of BV-VPIN needs to cater for the characteristics of the instrument
being investigated. Our investigation of the hedge and safe haven properties of BV-VPIN suggests
that it is an eﬀective safe haven for most countries during extreme market downturns. BV-VPIN
exhibits strong safe haven characteristics for most markets during three major crisis periods, the
2000 Dot-com Bubble (DCB), the 2008 Great Recession (GR) and the 2011 US Credit Rating
Downgrade (USCRD). Incorporating BV-VPIN as part of a ﬂight-to-quality trading strategy results
in an outperformance of the Buy-and-Hold equities strategy for four out of six countries in our
study. Speciﬁcally, in China, Japan and Australia, the BV-VPIN Strategy doubles the returns of
a comparable buy-and-hold strategy in equities.
In conclusion, we show that BV-VPIN has applications beyond that of HFT environments.
BV-VPIN is an eﬀective indicator of long-term market volatility and exhibits hedging and safe
haven characteristics during market downturns. BV-VPIN may also be used to improve portfolio
management strategies for asset managers in ascertaining market conditions where one should
minimize risk by reducing exposure to equities. For future work, other applications of BV-VPIN can
involve investigating its ability to track the smart money eﬀect as documented by in the managed
mutual funds industry Gruber (1996); Zheng (1999); Sapp and Tiwari (2004) and tracking money
ﬂows between asset classes such as the ﬂight-to-quality eﬀect (equity to debt) by mutual fund
23


### Page 24

managers.
24


### Page 25

6. References
Abad, D., Yage, J., 2012. From PIN to VPIN: An introduction to order ﬂow toxicity. Spanish
Review of Financial Economics 10 (2), 74–83.
Andersen, T. G., Bondarenko, O., 2014a. Reﬂecting on the VPIN dispute. Journal of Financial
Markets 17, 53–64.
Andersen, T. G., Bondarenko, O., 2014b. VPIN and the ﬂash crash. Journal of Financial Markets
17, 1–46.
Andersen, T. G., Bondarenko, O., 2015. Assessing measures of order ﬂow toxicity and early warning
signals for market turbulence. Review of Finance 19 (1), 1–54.
Ang, A., Chen, J., 2002. Asymmetric correlations of equity portfolios. Journal of Financial Eco-
nomics 63 (3), 443–494.
Aslan, H., Easley, D., Hvidkjaer, S., O’hara, M., 2011. The characteristics of informed trading:
Implications for asset pricing. Journal of Empirical Finance 18 (5), 782–801.
Baker, H. K., Kiymaz, H., Jul. 2013. Market Microstructure in Emerging and Developed Markets.
John Wiley & Sons.
Baur, D. G., McDermott, T. K., 2010. Is gold a safe haven? International evidence. Journal of
Banking & Finance 34 (8), 1886–1898.
Bell, H. A., 2013. High Frequency Trading: Do Regulators Need to Control this Tool of Informa-
tionally Eﬃcient Markets? Cato Institute Policy Analysis (731).
CFTC-SEC, Sep. 2010a. Findings Regarding the Market Events of May 6, 2010.
CFTC-SEC, May 2010b. Preliminary Findings Regarding the Market Events of May 6, 2010.
Chakrabarty, B., Pascual, R., Shkilko, A., 2012. Trade classiﬁcation algorithms: A horse race
between the bulk-based and the tick-based rules. Available at SSRN 2182819.
Chen, Y., Zhao, H., 2012. Informed trading, information uncertainty, and price momentum. Journal
of Banking & Finance 36 (7), 2095–2109.
Corcoran, C. M., 2012. Systemic Liquidity Risk and Bipolar Markets: Wealth Management in
Today’s Macro Risk On/risk OﬀFinancial Environment. John Wiley & Sons.
Easley, D., de Prado, M. L., OHara, M., 2011a. The exchange of ﬂow toxicity. Journal of Trading
6 (2), 8–13.
25


### Page 26

Easley, D., de Prado, M. L., O’Hara, M., 2016. Discerning Information from Trade Data. Journal
of Financial Economics.
Easley, D., De Prado, M. M. L., O’Hara, M., 2011b. The microstructure of the“ ﬂash crash”:
Flow toxicity, liquidity crashes, and the probability of informed trading. Journal of Portfolio
Management 37 (2), 118.
Easley, D., de Prado, M. M. L., O’Hara, M., 2012. Flow toxicity and liquidity in a high-frequency
world. Review of Financial Studies 25 (5), 1457–1493.
Easley, D., de Prado, M. M. L., O’Hara, M., 2014. VPIN and the ﬂash crash: A rejoinder. Journal
of Financial Markets 17, 47–52.
Easley, D., Engle, R. F., O’Hara, M., Wu, L., 2008. Time-varying arrival rates of informed and
uninformed trades. Journal of Financial Econometrics 6 (2), 171–207.
Easley, D., Hvidkjaer, S., OHara, M., 2010. Factoring information into returns. Journal of Financial
and Quantitative Analysis 45, 293–309.
Easley, D., Kiefer, N. M., O’Hara, M., 1997. The information content of the trading process. Journal
of Empirical Finance 4 (2), 159–186.
Easley, D., Kiefer, N. M., O’hara, M., Paperman, J. B., 1996. Liquidity, information, and infre-
quently traded stocks. Journal of Finance 51 (4), 1405–1436.
Easley, D., Prado, M. L., O’Hara, M., 2015. Optimal execution horizon. Mathematical Finance
25 (3), 640–672.
Flood, J., 2010. NYSE conﬁrms price reporting delays that contributed to the Flash Crash. AI5000.
Glosten, L. R., Jagannathan, R., Runkle, D. E., 1993. On the relation between the expected value
and the volatility of the nominal excess return on stocks. Journal of Finance 48 (5), 1779–1801.
Gruber, M. J., 1996. Another puzzle: The growth in actively managed mutual funds. Journal Of
Finance 51 (3), 783–810.
Kang, M., 2010. Probability of information-based trading and the January eﬀect. Journal of Banking
& Finance 34 (12), 2985–2994.
Krasting, B., May 2010. Then Yen Did It?
Lin, H.-W. W., Ke, W.-C., 2011. A computing bias in estimating the probability of informed
trading. Journal of Financial Markets 14 (4), 625–640.
26


### Page 27

Longin, F., Solnik, B., 1995. Is the correlation in international equity returns constant: 1960-1990?
Journal of International Money and Finance 14 (1), 3–26.
Low, R. K. Y., Alcock, J., Faﬀ, R., Brailsford, T., 2013. Canonical vine copulas in the context
of modern portfolio management: Are they worth it? Journal of Banking & Finance 37 (8),
3085–3099.
Low, R. K. Y., Yao, Y., Faﬀ, R., 2016. Diamonds vs. precious metals: What shines brightest in
your investment portfolio? International Review of Financial Analysis 43, 1–14.
Patterson, S., Lauricella, T., May 2010. Did a Big Bet Help Trigger ’Black Swan’ Stock Swoon?
Wall Street Journal.
Phillips, M., May 2010. SEC’s Schapiro: Here’s My Timeline of the Flash Crash. Wall Street
Journal.
Sapp, T., Tiwari, A., 2004. Does Stock Return Momentum Explain the Smart Money Eﬀect?
Journal of Finance 59 (6), 2605–2622.
Sharpe, W. F., 1994. The Sharpe Ratio. Journal of Portfolio Management 21 (1), 49–59.
Sortino, F. A., Satchell, S., 2001. Managing downside risk in ﬁnancial markets: theory, practice
and implementation. Butterworth-Heinemann.
Vega, C., 2006. Stock price reaction to public and private information. Journal of Financial Eco-
nomics 82 (1), 103–133.
Wu, K., Bethel, E., Gu, M., Leinweber, D., Rbel, O., 2013. A big data approach to analyzing
market volatility. Algorithmic Finance 2 (3-4), 241–267.
Zheng, L., 1999. Is money smart? A study of mutual fund investors’ fund selection ability. The
Journal of Finance 54 (3), 901–933.
Zweig, J., May 2012. Could Computers Protect the Market From Computers? Wall Street Journal.
27

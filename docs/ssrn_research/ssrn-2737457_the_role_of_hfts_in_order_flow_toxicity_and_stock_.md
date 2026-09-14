# The Role of HFTs in Order Flow Toxicity and Stock Price Variance,

- **Source File**: `ssrn-2737457.pdf`
- **Total Pages**: 38
- **SSRN ID**: `ssrn-2737457`

---


### Page 1

Electronic copy available at: http://ssrn.com/abstract=2737457
1
The Role of HFTs in Order Flow Toxicity and Stock Price Variance,
And Predicting Changes in HFTs’ Liquidity Provisions.
Serhat Yildiz
University of Mississippi
syildiz@bus.olemiss.edu
Robert A. Van Ness
University of Mississippi
rvanness@bus.olemiss.edu
Bonnie F. Van Ness
University of Mississippi
bvanness@bus.olemiss.edu
February 23, 2016
Abstract
This study examines relations between high frequency trading, order flow toxicity, stock price
volatility during normal and high order flow toxicity periods, and predictability of changes in high
frequency traders’ liquidity supply and demand. By employing Volume-synchronized probability
of informed trading (VPIN) flow toxicity metric, we find a negative relation between high
frequency trading and order flow toxicity. Our results also show that VPIN can be a good predictor
of high frequency traders’ liquidity supply and demand changes. Finally, we find that high
frequency traders’ impacts on stock price variance are not uniform and change with order flow
toxicity levels of markets and stock volume.


### Page 2

Electronic copy available at: http://ssrn.com/abstract=2737457
2
The Role of HFTs in Order Flow Toxicity and Stock Price Variance,
And Predicting Changes in HFTs’ Liquidity Provisions.
Introduction
High frequency trading is a subset of algorithmic trading that aims to profit from trading
at very high speeds. The 26 high frequency trading firms, identified in the NASDAQ high
frequency dataset (which includes 120 stocks) participate in 74% of all trades that execute on
NASDAQ (Brogaard, 2010). The upper boundary for estimated annual profits of aggressive high
frequency traders (HFTs) on the US market is around $21 billion (Kearns et al., 2010). Theoretical
work implies that HFTs may be harmful or beneficial for market quality depending on certain
conditions.1 However, empirical studies generally find that HFTs appear to be mostly beneficial
for markets.2
Our study answers three questions related to HFTs. First, how do HFTs’ liquidity supply
and demand affect order flow toxicity in equity markets? Second, can we predict periods in which
HFTs are dropping out of the market or decreasing their liquidity provisions? Third, how do HFTs
affect stock price variance during normal and high order flow toxicity periods?
Two empirical studies, Brogaard et al. (2014) and Carrion (2013), are related to our study.
Brogaard et al. find that while HFTs’ liquidity demanding orders increase price efficiency their
liquidity supplying orders may be adversely selected. Carrion finds that HFTs provide liquidity
when spreads are wider and take liquidity when spreads are tighter. Carrion’s results about HFTs’
adverse selection costs to other liquidity providers are mixed. While examining possible high
1 Cartea and Penalva (2012), Jarrow and Protter (2012) and Biais, Foucault, and Moinas (2015) develop theoretical
models to describe the impacts of HFTs.
2 Brogaard (2010), Kearns, Kulesza, and Nevmyvaka (2010), Menkveld (2013), Kirilenko, Kyle, Samadi, and Tuzun
(2012), Brogaard, Hendershott, and Riordan (2014) and Carrion (2013) empirically examine HFTs from different
perspectives.


### Page 3

Electronic copy available at: http://ssrn.com/abstract=2737457
3
frequency trading generated adverse selection, Brogaard et al. and Carrion focus on HFTs’ impact
on the permanent price change component.
As opposed to Brogaard et al. (2014) and Carrion (2013), our first question approaches
HFTs’ impacts on market liquidity with a different framework; order flow toxicity, measured with
VPIN. According to Easley et al. (2011), when there is a lot of information-based trades, VPIN
will be high. During high VPIN periods market makers will be on the wrong side of the market,
and they will accumulate or lose inventory on the wrong side of the market. Accumulation of losses
by market makers may force them to leave the market. Thus, order flow toxicity may harm market
liquidity.
Instead of focusing on price changes over a clock time interval, our approach, measuring
toxicity with VPIN, focuses on volume, order imbalances, and the number of trades over a trade
time interval. The importance of our approach is supported with findings of Easley and O’Hara
(1992), Jones, Kaul and Lipson (1994) and Blume, Easley and O’Hara (1994). Research shows
that the number of trades is an important signal of information flow, and the sequence of trades
provides additional information that is not conveyed by individual transactions (Easley and
O’Hara, 1992), the frequency of trades contains information regarding trading (Jones, Kaul and
Lipson, 1984), and volume provides information about the quality of traders’ information (Blume,
Easley and O’Hara, 1994). In other words, VPIN is designed to capture volume information rather
than price information (Easley et al., 2011). Thus, different from previous studies our approach
examines the impact of HFTs on market liquidity by focusing on volume information.
Another uniqueness of our approach is to employ a trade time clock rather than clock time.
While examining HFTs’ impact on market liquidity a trade time clock can be more appropriate.
Specifically, Clark (1973) introduces the idea that clock time may not be appropriate for measuring


### Page 4

4
time in financial markets. Consistently, Ane and Geman (2000) find that in high frequency world,
trade time rather than clock time is a more appropriate measure to use in sampling information
sets. Particularly, Ane and Geman find that the cumulative number of trades is an appropriate
stochastic clock for generating virtually perfect normality in returns. Also, Easley et al. (2012)
show that volume time reduces the impact of volatility clustering, and the distribution of price
changes calculated in volume time is closer to a normal distribution and is less heteroscedastic
than price changes calculated in clock time.
Second, we study the predictability of periods in which high frequency liquidity providers
change their liquidity supply and demand. Sudden changes in liquidity provisions can have
significant impacts on market liquidity. For instance, Kirilenko et al. (2012) and Easley et al.
(2011) find that the May 6, 2010 Flash Crash is a liquidity event in which some liquidity providers
dropped out the market. Such liquidity events can have devastating implications for investors. So,
predicting liquidity shocks is an important issue. To this end, we examine whether high VPIN
levels can detect changes in HFTs’ liquidity supply and demand.
Lastly, we examine the impact of HFTs on stock price variance. Similar to our study,
Brogaard (2010) compares volatility in one minute intervals with and without HFT initiated trades
and concludes that HFTs may decrease stock price variance. Our approach differs from Brogaard
in two aspects. First, we employ a volume time clock rather than clock time.  The importance of
focusing on volume time rather than clock time in a high frequency world is emphasized by the
findings of Clark (1973), Ane and Geman (2000) and Easley et al. (2012).  Thus, by using a more
relevant clock to calculate volatility, our study increases our understanding of the relation between
HFTs and stock price variance. Second, we examine impact of HFTs on stock price variance during
two different periods: normal and high order flow toxicity environments.  This analysis is


### Page 5

5
important because Kirilenko et al. (2012) find that HFTs did not start the Flash Crash, but HFT’s
did exacerbated stock price volatility during the Flash Crash. Thus, HFTs’ impact on stock price
variance may be different during normal times (as in Brogaard) than during high toxicity times (as
in Kirilenko et al.). Kirilenko et al. analyze a single high toxicity event, whereas we examine the
relation between HFTs and stock price variance during all high toxicity periods over the year 2009.
Thus, we provide a more comprehensive analysis of HFTs’ impact on stock price variance in
different order flow toxicity environments.
Our main findings are as follows. The trades in which HFTs trade with other HFTs and
non-HFTs are negatively associated with order flow toxicity. rades in which non-HFTs trade with
each other are positively associated with order flow toxicity. These findings are robust across
different volume samples. Our findings show that HFTs do not increase order flow toxicity, and
trades of non-HFTs with other non-HFTs are the main sources of order flow toxicity during our
sample period. We also find that VPIN can detect changes in HFTs’ market participation, liquidity
supply and demand around 10 volume buckets in advance. Thus, market participants and regulators
can track VPIN in real time and predict when high frequency liquidity suppliers will change their
liquidity provisions. Lastly, HFTs’ relation to stock return volatility is not uniform, and depend on
stock volume and toxicity level in the market. Specifically, during normal periods HFTs
participation can decrease stock return variance in high and medium volume stocks but increase
the volatility in low volume stocks. HFTs continue to decrease stock return volatility of high
volume stocks even during the high toxicity periods. However, HFTs do not affect stock return
variance of medium and low volume stocks during the high toxicity periods.
2. VPIN as a measure of order flow toxicity


### Page 6

6
Volume-synchronized probability of informed trading (VPIN) is developed by Easley et
al. (2012), and we follow their methods. Similar to our application, VPIN is used to measure order
flow toxicity by Easley et al. (2011; 2012), Menkveld and Yueshan (2013), Bethel et al. (2012),
Abad and Yague (2012), Wu et al. (2013) and Wei et al. (2013).
Using S&P 500 futures data, Easley et al. (2011) employ VPIN to study toxicity around
the May 6, 2010, Flash Crash, and find high levels of toxicity around the Flash Crash.  Menkveld
and Yueshan (2013) present VPIN and the change in VPIN as toxicity measures in the Flash Crash.
Bethel et al. (2012) find that VPIN gives strong signals ahead of the Flash Crash. Using E-mini
S&P 500 futures and WTI crude oil futures from January 1, 2008 to June 6, 2011, Easley et al.
(2012) report high levels of VPIN around the Flash Crash and the Fukushima nuclear crisis on
March 14, 2011. Easley et al. (2012) conclude that high VPIN levels indicate order flow toxicity.
Abad and Yague (2012) find that certain specifications of VPIN can proxy for adverse selection
risk, and that VPIN can be a helpful device in Spanish financial markets. Wu et al. (2013) examine
the performance of VPIN in predicting volatility events in 94 futures contracts from January 2007
to July 2012, and conclude that VPIN is a strong predictor of liquidity-induced volatility. Using
VPIN as a toxicity measure, Wei et al. (2013) find that VPIN affects quote imbalances and intraday
price volatility of 30 stocks in Australian financial markets.  On the other hand, using E-mini S&P
500 data from February 10, 2006 to March 22, 2011, Andersen and Bondarenko (2014b) find that
after controlling for trading intensity and volatility, VPIN calculated with bulk volume
classification has no additional predictive power of future volatility.
We do not aim to resolve the conflicting results about VPIN’s predictive power for future
volatility after controlling for certain factors in futures market. Consistent with the order flow
toxicity literature, we use VPIN as a measure of HFT and non-HFT generated toxicity in equity


### Page 7

7
markets. Also, while VPIN estimations are sensitive to trade classification algorithms, our data
indicate if the trade is a buy or sell. Thus, our calculations are free from biases caused by certain
trade classification algorithms.
3. Hypotheses development
3.1 HFTs and order flow toxicity
Theoretical work proposes that HFTs can benefit or harm market quality depending on
certain conditions. Cartea and Penalva (2012) propose that HFTs can cause losses to both liquidity
traders and market makers, increase price volatility and volume, but do not improve liquidity.
Jarrow and Protter (2012) show that HFTs may increase market volatility and create their own
profit opportunities at the expense of ordinary traders in a frictionless financial market. However,
Biais, Foucault, and Moinas (2015) find that increases in the level of high frequency trading, up to
a threshold level, may increase the probability that investors will find a trading counterparty and,
thereby, increase trading volume and profits. On the other hand, high levels of high frequency
trading can impose adverse selection costs on slow traders, and reduce volume, profits, and cause
slow traders to drop out of the market.
Empirically, Hendershott, Jones, and Menkveld (2011) and Hendershott and Riordan
(2013) find that algorithmic trading improves liquidity in U.S. and Germany stock markets,
respectively. Brogaard et al. (2014) find that HFTs play a significant role in information
dissemination and price discovery. We reason that HFTs’ impact on price discovery may be
beneficial to other liquidity providers, and lower order flow toxicity. Specifically, high information
asymmetry between liquidity providers and informed traders generates losses for liquidity
providers. HFTs speed up information incorporation into stock prices (as in Brogaard et al., 2014),
thus possible information asymmetry between informed traders and liquidity providers will be


### Page 8

8
reduced faster. Due to the decreased information asymmetry, possible losses of liquidity suppliers
will be reduced, and order flow toxicity will be lower.  Based on the empirical findings of Brogaard
et al., we argue that by increasing price informational efficiency, HFTs reduce informational
asymmetry between informed traders and liquidity providers and become negatively related to
order flow toxicity.
Hypothesis 1: High frequency trading is negatively associated with order flow toxicity in equity
markets.
3.2 Predicting HFTs’ liquidity provision changes
In the finance literature, extreme VPIN values are used as signals for important liquidity
events. Easley et al. (2012; 2011), Bethel et al. (2012) and Wu et al. (2013) document that VPIN
gives strong signals ahead of the Flash Crash. Wu et al. (2014) find that VPIN can detect some
events that resulted in liquidity issues in the market, such as the Countrywide Financial liquidity
crunch (08/2007), a FOMC weak outlook warning (01/2008), a significant drop in the DOW Jones
index (09/2008), and the U.S.’s credit rating downgrade (08/2011). Also, Easley et al. (2012)
document high levels of VPIN around the Fukushima nuclear crisis on March 14, 2011. Abad and
Yague (2012) find that VPIN can proxy for adverse selection risk in Spanish financial markets.
As empirical findings suggest that VPIN can signal important liquidity events, we ask a
different question: can VPIN signal the periods in which liquidity suppliers are changing their
liquidity supply and demand? Identifying when liquidity suppliers increase or decrease their
market participation is important. If we can detect those periods, regulators and market participants
can take precautions and prevent sudden high frequency trading related liquidity crises. To this


### Page 9

9
end, we test whether high levels of VPIN can detect changes in HFTs’ liquidity supply and
demand.
Hypothesis 2: High levels of VPIN can signal changes in HFTs’ liquidity supply and demand.
3.3 HFTs’ impact on stock price variance
Cartea and Penalva’s (2012) and Jarrow and Protter’s (2012) theoretical models predict
that HFTs can increase stock price volatility, yet, empirical findings for HFTs’ impact on stock
price volatility are mixed. Brogaard (2010) finds that HFTs may reduce price volatility. On the
other hand, Kirilenko et al. (2012) find that HFTs lead to an increase in volatility during the Flash
Crash. Additionally, Zhang (2010) finds that HFTs may increase stock price volatility.
We approach the relation between HFTs and stock price variance with a volume clock
approach rather than a time clock approach. A volume time clock approach to HFTs and stock
price variance relation can be more suitable than a clock time approach, particularly as Clark’s
(1973) and Ane and Geman’s (2000) findings support the idea that trade time rather than clock
time is more appropriate in financial markets. Moreover, Easley et al. (2012) show that the
distribution of price changes calculated in volume time is closer to a normal distribution and is less
heteroscedastic than price changes calculated in clock time. In addition, volume time reduces the
impact of volatility clustering.
Our second contribution is that we examine HFTs and stock price variance relation during
normal and high order flow toxicity periods. Kirilenko et al. (2012) find that HFTs increased stock
price variance during a single high order flow toxicity event; the Flash Crash. Different than
Kirilenko et al., we examine HFTs’ impact on stock price variance during all high toxicity periods
throughout the year 2009. Thus, we provide a comprehensive analysis of HFTs’ impact on stock
price variance during normal and high toxicity periods. Since theoretical studies predict a positive


### Page 10

10
relation between HFTs and stock price variance, and empirical findings are mixed, we test a null
hypothesis regarding HFTs and stock price volatility relation.
Hypothesis 3: HFTs’ liquidity demand and supply do not affect stock price variance during
normal and high order flow toxicity periods.
4. The VPIN metric calculation
We calculate volume-synchronized probability of informed trading, the VPIN toxicity
measure, following Easley, Prado, and O'Hara (2012). This methodology is followed by Easley,
Prado, and O'Hara (2011), Abad and Yague (2012), Bethel et al. (2012), Wu et al. (2013), and Wei
et al. (2013). VPIN captures the imbalances between buying and selling pressure and is designed
to capture volume information rather than price information (Easley et al., 2011).  Empirical
research shows that trade classification algorithms used to calculate VPIN can affect the VPIN
measure. However, our data identify buy and sell trades, and we use actual trades without any
classification algorithm. Thus, our measure is free from classification algorithm bias.
We define VPIN as:
nV
V
V
VPIN
n
B
S



1



Where V  is volume bucket size, n  is the number of buckets,
)
(B
S
V
is total sell (buy)
volume in a given volume bucket (). Easley et al. (2012) and Abad and Yegue (2012) show that
the choice of the number of buckets has little impact on final value of VPIN. Hence, we choose
most commonly used value (50). We define bucket size as one-fiftieth of the average daily volume.
Easley et al. (2012) show the choice of bucket size and number of buckets are robust to alternative
specifications.


### Page 11

11
5.1 Sample overview
We use the NASDAQ HFT dataset.  This dataset contains trades for 120 stocks. The sample
includes 40 large cap, 40 medium cap and 40 small cap stocks.  Half of the stocks are listed on
NASDAQ and the other half are listed on the New York Stock Exchange (NYSE). The 26 high
frequency trading firms are identified by NASDAQ based on analysis of firms’ trading patterns,
such as order duration, order to trade ratio, and how frequently net trading in a day crosses zero.
The data contain following items: Symbol, Date, Time in milliseconds, Shares, Price, a Buy/Sell
indicator, and Type (HH, HN, NH, NN).
Symbol is the NASDAQ trading symbol for a stock, and trades are time-stamped to the
millisecond. Shares indicates the number of shares traded in a given transaction. The Buy/Sell
indicator identifies if the trade was buyer- or seller-initiated. The Type item indicates liquidity
demanding and liquidity supplying parties in the transaction; the first participant is demanding
liquidity and second one is supplying liquidity. Specifically, a trade with high frequency trading
firms on both sides of the transaction is categorized as HH, a trade with a high frequency trading
firm initiating the trade and a non-high frequency trader providing liquidity is classified as HN.
When a non-high frequency trader initiates a trade and a high frequency trading firm provides
liquidity, this trade termed as an NH trade. An NN trade is one with no high frequency trading
firms participating.
We calculate HFTs’ overall participation, liquidity demand, and liquidity supply using
Type item (HH, HN, NH, NN). Consistent with Brogaard, Hendershott, and Riordan (2014) and
Carrion (2013) we define:
HFT_ALL= (HH+HN+NH)/(HH+HN+NH+NN),


### Page 12

12
HFT_DEMAND=(HH+HN)/(HH+HN+NH+NN),
(Eq.1)
HFT_SUPPLY=(HH+NH)/(HH+HN+NH+NN).
In addition, using Type item (HH, HN, NH, NN) we define trade type participation
variables as follows:3
HH_participation=(HH)/(HH+HN+NH+NN),
HN_participation=(HN)/(HH+HN+NH+NN),
(Eq.2)
NH_participation = (NH)/(HH+HN+NH+NN),
NN_participation = (NN)/(HH+HN+NH+NN).
Table 1 shows price, market capitalization and volume information of the full sample and
subsamples by listing exchange and market capitalization. Price, volume, market capitalization
and exchange listing data are from the Center for Research in Security Prices (CRSP) as of
December 31, 2009. Volume is calculated as the average number of shares traded per month during
the year 2009 (in hundred thousands). The average market capitalization of our sample is around
$18 billion and average stock price is around $34. While NASDAQ-listed stocks’ volume and
market capitalization are close to those of NYSE-listed stocks, NASDAQ-listed stocks have higher
prices on average than the NYSE-listed stocks. Large cap stocks’ volume is nearly 16 times larger
than medium caps’ volume, and 62 times larger than small caps’ volume in our sample.
{Insert Table 1 here}
5.2 Descriptive statistics
Table 2 reports descriptive statics of full sample and three subsamples by volume. Our
analysis utilizes all trade data reported by NASDAQ HFT dataset for the year 2009.4 We find that
3These definitions are similar to some definitions of Brogaard (2010).
4 We winsorize “price” at 0.01 and 99.9 percentiles to eliminate impact of any outliers as in Hendershott, Jones, and
Menkveld (2011).


### Page 13

13
as volume increases average order flow toxicity decreases. Average order flow toxicity (mean
VPIN) is 41.78% in overall sample, 23.78% in high volume sample, 40.01% in medium volume
sample and 61.54 % in low volume sample. Thus, we observe the highest VPIN levels in low
volume stocks and the lowest VPIN levels in high volume stocks. Similarly, we observe the lowest
VPIN volatility in the high volume sample, and highest VPIN volatility in the low volume sample.
The negative relation between volume and order flow toxicity is also observed between volume
and return volatility. Specifically, the standard deviation of returns is 8.32% in the overall sample,
2.22% in the high volume sample, 7.18% in the medium volume sample and 16.33% in the low
volume sample. We also observe that trade size and price are positively related to volume. Overall
HFT participation, HFT liquidity demand, HFT liquidity supply, HH-participation, and NH-
participation are increasing with volume while NN-participation is decreasing with volume. HN
participation is highest in medium volume and lowest in low volume stocks. Table 2 Panel C
results show that the mean differences we discussed so far are statistically significance at 1% level.
{Insert Table 2 here}
6.1 HFTs and order flow toxicity
We examine HFTs’ association with order flow toxicity with the following model:
𝑙𝑛 𝑉𝑃𝐼𝑁𝑖,𝜏= 𝛼𝑖,𝜏+ 𝛽1𝑙𝑛 𝑝𝑎𝑟𝑡𝑖𝑐𝑖𝑝𝑎𝑡𝑖𝑜𝑛 𝑟𝑎𝑡𝑒𝑖,𝜏−1 + 𝛽2𝑙𝑛 𝑡𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒𝑖,𝜏−1 + 𝛽3𝑙𝑛 𝑝𝑟𝑖𝑐𝑒𝑖,𝜏−1 + ɛ𝑖,𝜏.
VPIN method is explained in section 4. “τ” is a volume bucket for a given firm “i”.
Participation rate refers to HFT all, HH-, HN-, NH-, and NN-participations as in equations 1 and
2. Trade size is average number of shares traded per trade in a given volume bucket. Price is the
average stock price in a given volume bucket.
Consistent with the related literature (e.g., Easley, Engle, O'Hara, and Wu, 2008; Andersen,
and Bondarenko, 2014a, 2014b), we estimate the regressions using generalized methods of


### Page 14

14
moments, with the weighting matrix calculated according to Newey and West (1987) with 50 lags.
Thus, our analysis is based on the t-statistics that reflect heteroskedasticity and autocorrelation
consistent standard errors with 50 lags. In addition, when examining VPIN and HFT participation
relations (Tables 3 and 4), we normalize all variables with natural log. Our approach is supported
by empirical evidence that VPIN values may be better described with lognormal distribution (Wu,
Bethel, Gu, Leinweber, and Ruebel, 2013). Also, consistent with our approach, Easley, de Prado,
and O'Hara (2012) calculate natural log of VPIN values in their VPIN and volatility analysis
section.
Table 3 reports impacts of HFT all, HH-, HN-, NH- and NN-participation on order flow
toxicity with models 1, 2, 3, 4, and 5 respectively. Model 1 shows that overall HFT activity is
negatively associated with order flow toxicity. Models 2 and 3 find that HFTs’ trade with each
other (HH), and HFTs’ liquidity demand from non-HFTs (HN) are negatively associated with
order flow toxicity. However, when non-HFTs trade with each other (NN) is positively related to
order flow toxicity (model 5). These findings are statistically significant at 5% or higher levels. In
addition, we find that trade size is positively associated with order flow toxicity in all models,
while price is statistically insignificant.
{Insert Table 3 here}
Since, trading activities and HFTs’ market participation are heterogeneous across volume
samples (e.g., Table 2 Panel C), our findings in Table 3 may differ with volume. Thus, we examine
the impact of volume on HFTs’ relation to order flow toxicity in Table 4. Specifically, in Table 4
we divide the overall sample into high-, medium- and low-volume subsamples with 40 stocks each.
Then, we employ the empirical approach of Table 3 in each subsample. In Table 4, the comparison
of slopes panel, we test statistical significance of HFT participation’s slope differences across


### Page 15

15
subsamples. In the comparison of slopes tests, as in Ahn, Hwang, and Kim (2010), we follow the
methods suggested by Paternoster, Brame, Mazerolle, and Piquero (1998).
Table 4 Panel A shows that overall HFT participation is negatively associated with order
flow toxicity across all subvolume samples. Comparison of slopes shows that the negative impact
is more pronounced in the high and medium volume samples compared to the low volume sample.
Panel B and C find that when HFTs’ trades with each other (HH), and HFTs’ liquidity demand
from non-HFTs (HN) are negatively related to order flow toxicity in high and medium volume
samples. Comparisons of slopes show that negative impact of HH-participation is greater in high
volume sample compared to medium and low volume samples. Table 4 Panel E shows that when
non-HFTs’ trades with each other (NN), we find a positive relation to order flow toxicity across
all sub-volume samples. Comparison of slopes shows that the positive impact is more pronounced
in the high and medium volume samples compared to the low volume sample. In all models of
Table 4 trade size is positively associated with order flow toxicity.
Overall, and consistent with the findings in Table 3, our findings in Table 4 show that even
after controlling for volume differences across stocks, HFTs are negatively related to order flow
toxicity. Moreover, order flow toxicity is a positively related to non-HFTs’ trading with other non-
HFTs and trade size.
{Insert Table 4 here}
The findings in Table 3 and Table 4 are consistent with our first hypothesis that HFTs are
negatively associated with order flow toxicity. One possible explanation of this finding is that
when information asymmetry is high between the liquidity providers and informed traders, losses
to the liquidity providers will be high and order flow toxicity will increase. Since, HFTs are better
at observing markets (Hendershott and Riordan, 2013) and increase price efficiency (Brogaard et


### Page 16

16
al., 2014), they reduce the information asymmetry in the markets. With short lived information
asymmetry, losses to liquidity suppliers decrease and HFTs’ participations become negatively
related to order flow toxicity.
6.2 Predicting HFTs’ liquidity provision changes
We examine if VPIN can detect changes in HFTs’ market participations, liquidity supply
and demand with univariate and multivariate (probit) approaches.
6.2.1 Predicting HFTs’ liquidity provision changes univariate approach
We start univariate approach by defining VPIN events. When the VPIN level in a volume
bucket is two standard deviations above the sample’s mean VPIN level, we define that volume
bucket as a VPIN event bucket (similar to Wu et al., 2013). VPIN event buckets are considered to
be high toxicity periods. We examine HFTs’ liquidity supply and demand activities in different
volume bucket windows around and during the VPIN events.
Below, the volume bucket line represents the way we create the volume bucket windows.
The first bucket in which VPIN is two standard deviations above the sample mean is considered
as the start of a VPIN event. The last bucket extreme VPIN observed is considered as the end of
VPIN event. Prior 10, 5, and 1 windows start at 10, 5, and 1 buckets before the VPIN event starts.
All Prior event windows end at the beginning of the VPIN event.
Prior 10             Prior 5         Prior 1
VPIN EVENT                After 1       After 5            After 10
|
|
|              |
  
|               |
|
|
-10                       -5                - 1           0                                     0               1                 5                       10
Mean 0 is the average liquidity supply/demand throughout the entire sample period,
excluding VPIN event periods and the window itself. Mean 1 is the average liquidity


### Page 17

17
supply/demand in the stated volume bucket window. We calculate the differences between Mean
0 and Mean 1 in each window, and test for statistical significance of the differences with T-Tests
and Wilcoxon Two-Sample Tests. In addition, we test whether the distributions of liquidity supply
and demand in six different windows and during the VPIN event are the same as the distributions
of liquidity supply and demand during normal times. To this end, we apply the Kolmogorov-
Smirnov test on the liquidity supply and demand distributions. Kolmogorov-Smirnov analysis tests
if the distribution of a variable is same across different groups, and reports the probability that two
compared sequences follow same distribution.5
Table 5-A Panel A presents comparison of HFTs’ liquidity supply around the VPIN events.
We find that in Prior 10, 5, and 1 windows the differences are positive. Thus, prior to the VPIN
events HFTs’ liquidity supply is decreasing compared to their liquidity supply during the normal
times. The greatest decrease is observed during the VPIN events. In after 1, 5, and 10 windows all
differences are negative, which means HFTs’ liquidity supply is increasing after the VPIN events.
We apply T-Tests and Wilcoxon Two-Sample tests and find that all differences in Panel A are
statistically significant at the 1% level. In addition, the results of Kolmogorov-Smirnov test show
that the distributions of HFTs’ liquidity supply in the prior, during and after VPIN event windows
are different than those during the normal toxicity periods.  Thus, VPIN is able to predict the
changes in HFTs’ liquidity supply.
Table 5-A Panel B reports HFTs’ liquidity demand around and during the VPIN events.
HFTs’ liquidity demand is decreasing in Prior 10, 5, and 1 windows compared to the liquidity
demand during the normal periods. The differences are significant at 5% level.6  During the VPIN
5 We discuss the findings of Kolmogorov-Smirnov test, but do not report the results. The findings are available upon
request.
6 Exceptions are; After 1 window which is significant at 10% level, and After 5 window which is insignificant.


### Page 18

18
events HFTs’ liquidity demand is lower than their liquidity demand during the normal times. After
the VPIN events HFTs’ liquidity demand starts to increase. Kolmogorov-Smirnov tests also show
that the distributions of HFTs’ liquidity demand around and during the VPIN events are different
than the distributions of HFTs’ liquidity demand during normal times. Thus, univariate findings
are consistent with our hypothesis that VPIN can detect changes in HFTs’ liquidity supply and
demand.
{Insert Table 5-A here}
6.2.2 Predicting HFTs’ liquidity provision changes multivariate (probit) approach
Table 5-B presents probit analysis in which VPIN events are dependent variables and HFT
participations, price and trade size are independent variables. The probit regression is:
𝑉𝑃𝐼𝑁 𝐸𝑣𝑒𝑛𝑡𝑖,𝜏= 𝛼𝑖,𝜏+ ∑
𝛽𝑗
10
𝑗=1
𝑝𝑎𝑟𝑡𝑖𝑐𝑖𝑝𝑎𝑡𝑖𝑜𝑛 𝑟𝑎𝑡𝑒𝑖,𝜏−𝑗+ ∑
ʎ𝑗
10
𝑗=1
𝑝𝑟𝑖𝑐𝑒𝑖,𝜏−𝑗+ ∑
ᴪ𝑗
10
𝑗=1
𝑡𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒𝑖,𝜏−𝑗+ ɛ𝑖,𝜏.
In the probit analysis, we examine how HFTs’ market participations in the ten prior volume bucket
is related to VPIN events, while controlling for price and trade size. We follow Wooldridge’s
(2012) method to calculate sums of coefficients of 10 lags and their standard errors. We cluster
the standard errors at the firm level and report the robust t-statistics.
In the Table 5-B Panel A, we use overall sample’s mean and standard deviations of VPIN
values to calculate VPIN threshold and VPIN events. This examination is practical and uses all
available information but does allow contemporaneous examination. In the Table 5-B Panel B,
first, we divide our sample in two subsamples with equal number of volume buckets. Then, we
calculate VPIN thresholds by using the data from the first sample. We use VPIN thresholds
calculated from first sample to define VPIN events in the second sample. This approach allows for


### Page 19

19
contemporaneous calculation, because VPIN events in second sample are defined based on
realized VPIN values from the first sample.
Table 5-B Panel A-1 shows that overall HFT activity is negatively related to the likelihood
of VPIN events. We examine HFT activity and VPIN event relation more specifically with HH,
HN, and NH participations in Panels A-2, A-3, and A-4. These three panels also find a negative
relation between HFT involved trades and the likelihood of a VPIN event. On the other hand Panel
A-5 finds non-HFTs trade with each other (NN) is positively related to probability of a VPIN
event. In all models, price and trade size are positively associated with probability of VPIN events.
Table 5-B Panel B, contemporaneous examination shows consistent findings with Panel-A. Thus,
VPIN events defined by using realized VPIN values can be useful to detect HFT activity changes
in real time.
{Insert Table 5-B here}
Tables 5-A and 5-B provide supportive evidence that in addition to predicting important
toxicity events, VPIN can be used to predict changes in HFTs’ market participation, liquidity
supply and demand. Market participants and regulators can benefit from this property of VPIN.
By tracking VPIN in real time; market participants and regulators can predict when high frequency
liquidity suppliers will drop out the market. Thus, sudden drops in liquidity due to high frequency
liquidity supplier withdrawals can be foreseen and appropriate protection strategies can be
implemented.
6.3 HFTs and stock price variance
We examine the relation between stock price variance and HFTs’ market participation with
the following model:


### Page 20

20
𝑆𝑡𝑑. 𝑑𝑒𝑣. 𝑜𝑓 𝑟𝑒𝑡𝑢𝑟𝑛𝑠𝑖,𝜏= 𝛼𝑖,𝜏+ 𝛽1𝑝𝑎𝑟𝑡𝑖𝑐𝑖𝑝𝑎𝑡𝑖𝑜𝑛 𝑟𝑎𝑡𝑒𝑖,𝜏−1 + 𝛽2 ln 𝑡𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒𝑖,𝜏−1 + 𝛽3ln 𝑝𝑟𝑖𝑐𝑒𝑖,𝜏−1 + ɛ𝑖,𝜏 .
Standard deviation of returns is calculated in each volume bucket ““τ” for a given firm
“i”. Returns are calculated using prices of consecutive trades. Participation rates are calculated as
in equations 1 and 2. Controls variables are the natural logarithms of price and trade size. In the
volatility and HFT participation examinations, we follow Andersen, and Bondarenko, 2014a,
2014b. We estimate the regressions using generalized methods of moments, with the weighting
matrix calculated according to Newey and West (1987) with 50 lags. Hence, our analysis is based
on the t-statistics that reflect heteroskedasticity and autocorrelation consistent standard errors with
50 lags.
Table 6 presents the relations between overall HFT-, HH-, HN-, NH- and NN-participation
and stock price variance in model 1, 2, 3, 4, and 5 respectively. Models 1, 2 and 5 find that overall
HFT participation, HFTs trades with other HFTs, and non-HFTs trades with other non-HFTs do
not affect stock return variance in overall sample. Model 3 finds that trades in which HFTs demand
liquidity from non-HFTs are negatively associated with return volatility. On the other hand, Model
4 shows that trades in which non-HFTs takes liquidity from HFTs are positively associated with
stock return volatility. In all models, price is negatively related to stock return variance and trade
size is statistically insignificant.
{Insert Table 6 here}
In Table 7 we examine the impact of HFT participation on stock return variance across
high-, medium-, and low-volume subsamples. Table 7 Panel A models 1 and 2 find that overall
HFT participation is negatively associated with stock return volatility in high and medium volume
samples. However, Panel A model 3 shows that overall HFT participation is positively related to
stock return volatility in the low volume sample. Comparisons of overall HFTs’ slopes also show


### Page 21

21
that overall HFT impact on volatility in high and medium volume stocks is different than that in
low volume stocks. Panels B and D present that in high (low) volume sample HH and NH
participations are negatively (positively) associated with stock return variance. Comparison of
slopes also support these differences. Panel C finds that trades in which HFT demand liquidity
from non-HFTs are negatively associated with stock return volatility in high and medium volume
samples. Panel E shows that trades of non-HFTs are positively associated with stock return
variance in high and medium volume samples and negatively associated in low volume sample.
Comparison of non-HFTs’ slopes provide supportive evidence about the statistical significance of
impact differences.
{Insert Table 7 here}
Overall, Tables 6 and 7 provide evidence about the significant role of volume when
examining impacts of HFTs on stock return volatility. Tables 6 and 7 results show that HFTs’
impact on stock return variance is not uniform and varies with volume. HFTs’ market participation
can reduce stock return volatility in high and medium volume stocks but increase the volatility in
low volume stocks. At the same time, non-HFTs’ trades with each other can increase stock return
volatility in high and medium volume samples, and decrease the volatility in low volume stocks.
Hence, in terms of stock return volatility HFTs are mainly beneficial for high and medium volume
stocks and can harm low volume stocks.
6.4 HFTs and stock price variance during high toxicity periods
Table 8 examines HFTs’ impacts on stock price variance during high order flow toxicity
periods. In this analysis, we follow the same regression model from section 6.3. The main
difference is that we conduct our analysis only in high toxicity periods. We define high order flow


### Page 22

22
toxicity periods as the volume buckets in which the VPIN level is two standard deviations above
the sample’s mean VPIN level (similar to Wu et al., 2013).
Table 8 Panel A model 1 finds that in high volume stocks overall HFT participation is
negatively associated with stock return volatility even during high toxicity periods. Consistently,
Panel C model 1 also finds a negative relation between HN participation and stock return volatility
in high volume sample. On the other hand, Panel E model 1 finds a positive association with non-
HFTs trades with each other and stock return volatility in high volume stocks. For medium and
low volume stocks the results are mostly insignificant.
{Insert Table 8 here}
Consistent with the findings in Table 7, Table 8 results show that even during the high
toxicity periods overall HFT participation is negatively related to stock return volatility in high
volume stocks. While HFTs can be beneficial for high volume stocks during high toxicity periods,
their impact in medium and low volume samples are insignificant. The differences in results of
Tables 7 and 8 show that HFTs’ impacts on stock price variance are changing during high order
flow toxicity periods relative to normal periods. Thus, HFTs relation to stock return volatility is
not uniform varies with market’s order flow toxicity level.
7. Conclusion
A considerable amount of research is dedicated to understand the impacts of HFTs on the
financial markets.  Our study extends the empirical research on HFTs with three contributions.
First, we examine the relation between high frequency trading and order flow toxicity in equity
markets, and find a negative relation between high frequency trading and order flow toxicity in
equity markets. We attribute this to HFTs’ role in information dissemination and price discovery.


### Page 23

23
Second, we study predictability of changes in HFTs’ market participation, liquidity supply and
demand, and find that VPIN can detect changes in HFTs’ liquidity demand and supply. Market
participants and regulators can benefit from our finding by tracking the VPIN in real time; changes
in HFTs’ liquidity provisions can be detected and appropriate protection strategies can be
implemented. Finally, we find that HFTs’ impacts on stock price variance are not uniform, and
vary with toxicity levels and stock volume. Overall HFTs participation is mostly beneficial for
high and medium volume stocks while can increase stock return volatility in low volume stocks.


### Page 24

24
References
Abad, D., and Yague, J., (2012). From PIN to VPIN: an introduction to order flow toxicity. The
Spanish Review of Financial Economics 10, 74–83.
Ahn, T. S., Hwang, I., & Kim, M. I. (2010). The impact of performance measure discriminability
on ratee incentives. The Accounting Review, 85(2), 389-417.
Andersen, T. G., and Bondarenko, O. (2014a). VPIN and the flash crash. Journal of Financial
Markets, 17, 1-46.
Andersen, T. G., and Bondarenko, O. (2014b). Assessing measures of order flow toxicity and early
warning signals for market turbulence. Review of Finance, Forthcoming.
Ané, T., and Geman, H. (2000). Order flow, transaction clock, and normality of asset returns. The
Journal of Finance, 55(5), 2259-2284.
Bethel, E. W., Leinweber, D., Rubel, O., and Wu, K., (2012). Federal market information
technology in the post-flash crash era: roles for supercomputing. Journal of Trading 7 (2),
9–25.
Biais, B., Foucault, T., and Moinas, S. (2015). Equilibrium high-frequency trading. Journal of
Financial Economics, 116(2), 292-313.
Blume, L., Easley, D., and O'Hara, M. (1994). Market statistics and technical analysis: The role of
volume. The Journal of Finance, 49(1), 153-181.
Brogaard, J. (2010). High frequency trading and its impact on market quality. Northwestern
University Kellogg School of Management Working Paper.
Brogaard, J., Hendershott, T., & Riordan, R. (2014). High-frequency trading and price
discovery. Review of Financial Studies, 27(8), 2267-2306.
Carrion, A. (2013). Very fast money: High-frequency trading on the NASDAQ.Journal of
Financial Markets, 16(4), 680-711.
Cartea, Á., and Penalva, J. (2012). Where is the value in high frequency trading?. The Quarterly
Journal of Finance, 2(03).
Carrion, A. (2013). Very fast money: High-frequency trading on the NASDAQ.Journal of
Financial Markets, 16(4), 680-711.
Clark, P. K. (1973). A subordinated stochastic process model with finite variance for speculative
prices. Econometrica journal of the Econometric Society, 135-155.
Easley, D., and O'Hara, M. (1992). Time and the process of security price adjustment. The
Journal of finance, 47(2), 577-605.
Easley, D., Engle, R. F., O'Hara, M., and Wu, L. (2008). Time-varying arrival rates of informed
and uninformed trades. Journal of Financial Econometrics,6(2), 171-207.
Easley, D., López de Prado, M., and O'Hara, M. (2011). The microstructure of the ‘Flash Crash’:
Flow toxicity, liquidity crashes and the probability of informed trading. The Journal of
Portfolio Management, 37(2), 118-128.
Easley, D., de Prado, M. M. L., and O'Hara, M. (2012). Flow Toxicity and Liquidity in a High-
frequency World. Review of Financial Studies, 25(5), 1457-1493.
Hendershott, T., Jones, C. M., and Menkveld, A. J. (2011). Does algorithmic trading improve
liquidity?. The Journal of Finance, 66(1), 1-33.
Hendershott, T., and Riordan, R., Algorithmic Trading and the Market for Liquidity (2013).
Journal of Financial and Quantitative Analysis, 48(4), 1001-1024.


### Page 25

25
Jarrow, R. A., and Protter, P. (2012). A dysfunctional role of high frequency trading in electronic
markets. International Journal of Theoretical and Applied Finance, 15(03).
Jones, C. M., Kaul, G., and Lipson, M. L. (1994). Transactions, volume, and volatility. Review of
Financial Studies, 7(4), 631-651.
Kearns, M., Kulesza, A., and Nevmyvaka, Y. (2010). Empirical limitations on high frequency
trading profitability. Available at SSRN 1678758.
Kirilenko, A., Kyle, A., Samadi, M., and Tuzun, T. (2012). The Flash Crash: The impact of high
frequency trading on an electronic market. Available at SSRN 1686004.
Menkveld, A. J. (2013). High frequency trading and the New-Market Makers. Journal of Financial
Markets, 16(4), 712-740.
Menkveld, A. J., and Yueshen, B. Z., (2013), Anatomy of the Flash Crash (April 10,2013).
Available from SSRN: http:/ssrn.com/abstract=2243520
Paternoster, R., Brame, R., Mazerolle, P., and Piquero, A. (1998). Using the correct statistical
test for the equality of regression coefficients. Criminology,36, 859.
Wei, W. C., Gerace, D., and Frino, A., (2013). Informed trading, flow toxicity and the impact on
intraday trading factors. Australian Accounting Business and Finance Journal7, 3–24.
Wooldridge, J. (2012). Introductory econometrics: A modern approach. Cengage Learning.
Wu, K., Bethel, W., Gu, M., Leinweber, D., and Rübel, O. (2013). A big data approach to
analyzing market volatility. Algorithmic Finance (2013), 2, 3-4.
Zhang, F. (2010). High-frequency trading, stock volatility, and price discovery. Available at SSRN
1691679.


### Page 26

26
Table 1: Sample stock characteristics
Sample includes 120 NASDAQ stocks from NASDAQ provided high frequency trading dataset. Sample
period is from January 2009 to December 2009. Price, volume, market capitalization and exchange listing
data are from CRSP as of December 31, 2009. Volume (in 100,000’s) is calculated as the average number
of shares traded per month during 2009.  Market Capitalization (MCAP) is in billions of dollars.
Full
sample
NYSE-listed
stocks
NASDAQ-listed
stocks
Large cap
stocks
Medium
cap stocks
Small cap
stocks
N
120
60
60
40
40
40
Volume
1257.78
1266.26
1249.29
3504.90
212.70
55.72
Price
34.88
28.94
40.81
56.73
30.12
17.78
MCAP
17.99
18.26
17.72
51.80
1.75
0.41


### Page 27

27
Table 2: Descriptive statistics
This table reports descriptive statistics across volume buckets for 120 stocks traded on NASDAQ for the year 2009. VPIN calculation procedure is given in
section 4 in detail. Ret. Std. Dev. is the standard deviation of returns, where returns calculated as (((pricet / pricet-1)-1)*100). Trade size is the average number
of shares traded per trade in a given volume bucket. Price is the average stock price in a given volume bucket.  HH-, HN-, NH-, and NN-part. are the participation
rates which are calculated as (volume of trade type in a given volume bucket divided by total volume, as in eq.2). ‘H’ stands for high frequency trader and ‘N’
stands for non-high frequency trader. A trade with high frequency trading firms on both sides of the transaction is categorized as HH, a trade with a high
frequency trading firm initiating the trade and a non-high frequency trader providing liquidity is classified as HN. When a non-high frequency trader initiates
a trade and a high frequency trading firm provides liquidity, we term this trade as NH trade. An NN trade is one where there are no high frequency trading
firms participating. HFT all, HFT demand and HFT supply are calculated following eq.1. Panel C reports if the differences in means are statistically significant.
***, ** and * represent significance at 1%, 5%, and 10% level, respectively.
Panel A:  Overall sample
Panel A: High Volume sample
Variable
Mean
Std. Dev
5th Pctl
Median
95th Pctl
Variable
Mean
Std. Dev
5th Pctl
Median
95th Pctl
VPIN
0.4178
0.1908
0.1761
0.3885
0.7744
VPIN
0.2378
0.0739
0.1497
0.2253
0.3657
Ret. Std. Dev.
0.0832
0.1464
0.0057
0.0382
0.2949
Ret. Std. Dev.
0.0222
0.0327
0.0071
0.0157
0.0522
Trade size
160.96
397.35
56.76
111.50
370.68
Trade size
196.45
578.90
90.29
142.86
400.19
Price
30.24
42.88
5.04
20.73
69.12
Price
43.31
64.25
7.88
28.22
95.19
HFT all
0.4938
0.2909
0.0000
0.5386
0.8988
HFT all
0.6890
0.1675
0.3662
0.7216
0.9004
HFT demand
0.3306
0.2463
0.0000
0.3247
0.7516
HFT demand
0.4268
0.1681
0.1453
0.4280
0.7021
HFT supply
0.2481
0.2243
0.0000
0.2003
0.6535
HFT supply
0.4262
0.1754
0.1268
0.4343
0.6986
HH part.
0.0848
0.1097
0.0000
0.0406
0.3036
HH part.
0.1640
0.1026
0.0227
0.1493
0.3545
HN part.
0.2458
0.2065
0.0000
0.2194
0.6330
HN part.
0.2628
0.1238
0.0754
0.2533
0.4805
NH part.
0.1633
0.1638
0.0000
0.1275
0.4684
NH part.
0.2622
0.1329
0.0715
0.2470
0.5010
NN part.
0.5062
0.2909
0.1012
0.4614
1.0000
NN part.
0.3110
0.1675
0.0996
0.2784
0.6338
Panel B: Medium volume sample
Panel B: Low volume sample
Variable
Mean
Std. Dev
5th Pctl
Median
95th Pctl
Variable
Mean
Std. Dev
5th Pctl
Median
95th Pctl
VPIN
0.4001
0.1112
0.2445
0.3876
0.5981
VPIN
0.6154
0.1400
0.4024
0.6067
0.8586
Ret. Std. Dev.
0.0718
0.0915
0.0114
0.0508
0.1865
Ret. Std. Dev.
0.1633
0.2183
0.0000
0.1005
0.5279
Trade size
152.33
326.67
64.25
105.28
271.41
Trade size
134.11
172.50
41.51
91.42
393.76
Price
27.70
27.89
5.53
21.84
59.34
Price
19.72
17.93
3.22
12.89
59.21
HFT all
0.4751
0.2519
0.0495
0.4814
0.8793
HFT all
0.3174
0.3045
0.0000
0.2487
0.9342
HFT demand
0.3386
0.2353
0.0000
0.3151
0.7603
HFT demand
0.2263
0.2796
0.0000
0.1056
0.8337
HFT supply
0.2009
0.1822
0.0000
0.1550
0.5665
HFT supply
0.1171
0.1893
0.0000
0.0000
0.5233


### Page 28

28
HH part.
0.0643
0.0925
0.0000
0.0301
0.2540
HH part.
0.0260
0.0831
0.0000
0.0000
0.1744
HN part.
0.2743
0.2038
0.0000
0.2461
0.6512
HN part.
0.2003
0.2606
0.0000
0.0834
0.7708
NH part.
0.1365
0.1393
0.0000
0.1000
0.4110
NH part.
0.0911
0.1663
0.0000
0.0000
0.4370
NN part.
0.5249
0.2519
0.1207
0.5186
0.9505
NN part.
0.6826
0.3045
0.0658
0.7513
1.0000
Panel C: Diff. in Means
High Vol. vs. Med. Vol.
High Vol. vs. Low Vol.
Med Vol. vs. Low Vol.
VPIN
-0.1623***
-0.3776***
-0.2153***
Ret. Std. Dev.
-0.0496***
-0.1411***
-0.0915***
Trade size
44.1262***
62.3397***
18.2136***
Price
15.6117***
23.5877***
7.9759***
HFT all
0.2139***
0.3716***
0.1577***
HFT demand
0.0882***
0.2005***
0.1123***
HFT supply
0.2253***
0.3091***
0.0837***
HH part.
0.0996***
0.1379***
0.0383***
HN part.
-0.0114***
0.0625***
0.074***
NH part.
0.1257***
0.1712***
0.0454***
NN part.
-0.2139***
-0.3716***
-0.1577***


### Page 29

29
Table 3: HFTs’ impact on order flow toxicity regression results
This table presents the results from estimating the regression given by 𝑛 𝑉𝑃𝐼𝑁𝑖,𝜏= 𝛼𝑖,𝜏+ 𝛽1𝑙𝑛 𝑝𝑎𝑟𝑡𝑖𝑐𝑖𝑝𝑎𝑡𝑖𝑜𝑛 𝑟𝑎𝑡𝑒𝑖,𝜏−1 + 𝛽2𝑙𝑛 𝑡𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒𝑖,𝜏−1 +
𝛽3𝑙𝑛 𝑝𝑟𝑖𝑐𝑒𝑖,𝜏−1 + ɛ𝑖,𝜏 . We estimate the regressions using generalized methods of moments, with the weighting matrix calculated according to Newey and
West (1987) with 50 lags. The t-statistics in parentheses reflect heteroskedasticity and autocorrelation consistent standard errors with 50 lags. The dependent
variable VPIN is calculated from NASDAQ provided HFT data from Jan 2009 to Dec. 2009. “τ” is a volume bucket for a given firm “i”.  HFT all is calculated
following eq.1. HH-, HN-, NH-, and NN-participations are calculated as in eq.2. Trade size is average number of shares traded per trade in a given volume
bucket. Price is the average stock price in a given volume bucket.  Sample size (N) is 120.  ***, ** and * represent significance at 1%, 5%, and 10% level,
respectively.
Models
Model 1
Model 2
Model 3
Model 4
Model 5
HFT ALL
-0.0315
(-3.03)***
HH-part.
-0.0130
(-2.43)**
HN-part.
-0.0158
(-2.63)**
NH-part.
0.0067
(1.10)
NN-part.
0.0321
(3.57)***
Trade size
0.0954
(5.96)***
0.0976
(4.69)***
0.1025
(6.46)***
0.1121
(6.71)***
0.0925
(6.72)***
Price
-0.0417
(-0.70)
-0.0364
(-0.52)
-0.0408
(-0.67)
-0.0363
(-0.57)
-0.0417
(-0.72)
Intercept
-1.3669
(-6.53)***
-1.4143
(-5.78)***
-1.4083
(-6.63)***
-1.4436
(-6.52)***
-1.2979
(-6.39)***
R-square
0.1050
0.0923
0.0996
0.0953
0.1217


### Page 30

30
Table 4: HFTs’ impact on order flow toxicity across volume subsamples regression results
This table presents the results from estimating the regression given by 𝑙𝑛 𝑉𝑃𝐼𝑁𝑖,𝜏= 𝛼𝑖,𝜏+
𝛽1𝑙𝑛 𝑝𝑎𝑟𝑡𝑖𝑐𝑖𝑝𝑎𝑡𝑖𝑜𝑛 𝑟𝑎𝑡𝑒𝑖,𝜏−1 + 𝛽2𝑙𝑛 𝑡𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒𝑖,𝜏−1 + 𝛽3𝑙𝑛 𝑝𝑟𝑖𝑐𝑒𝑖,𝜏−1 + ɛ𝑖,𝜏.
We
estimate
the
regressions using generalized methods of moments, with the weighting matrix calculated according to
Newey and West (1987) with 50 lags. The t-statistics in parentheses reflect heteroskedasticity and
autocorrelation consistent standard errors with 50 lags. The dependent variable VPIN is calculated from
NASDAQ provided HFT data from Jan 2009 to Dec. 2009. “τ” is a volume bucket for a given firm “i”.  HFT
all is calculated following eq.1. HH-, HN-, NH-, and NN-participations are calculated as in eq.2. Trade size
is average number of shares traded per trade in a given volume bucket. Price is the average stock price
in a given volume bucket. We compare slope differences following Paternoster, Brame, Mazerolle, and
Piquero (1998). Each volume sample consists of 40 stocks.  ***, ** and * represent significance at 1%,
5%, and 10% level, respectively.
Panel A
High vol.
Med vol.
Low vol.
Comparison of slopes
Models
Model 1
Model 2
Model 3
High vs Med
High vs Low
Med vs Low
HFT all
-0.0544
(-2.93)***
-0.0319
(-3.65)***
-0.0081
(-2.09)**
-0.0225
(-1.09)
-0.0463
(-2.44)**
-0.0239
(-2.50)**
Trade size
0.1159
(5.22)***
0.10369
(6.46)***
0.0666
(6.81)***
Price
-0.0304
(-0.45)
-0.0312
(-0.52)
-0.0633
(-1.27)
Intercept
1.9990
(-7.55)***
-1.4332
(-6.81)***
-0.6685
(-4.39)***
R-square
0.1064
0.1245
0.0841
Panel B
High vol.
Med vol.
Low vol.
Comparison of slopes
Models
Model 1
Model 2
Model 3
High vs Med
High vs Low
Med vs Low
HH-part.
-0.0296
(-4.01)***
-0.00826
(-1.96)*
-0.0010
(-0.23)
-0.0214
(-2.51)**
-0.0286
(-3.32)***
-0.0072
(-1.19)
Trade size
0.1146
(5.03)***
0.12043
(5.61)***
0.0576
(3.17)***
Price
-0.0229
(-0.33)
-0.0204
(-0.29)
-0.0659
(-0.93)
Intercept
-2.0531
(-7.81)***
-1.5491
(-6.27)***
-0.6404
(-2.86)***
R-square
0.1086
0.1047
0.0636
Panel C
High vol.
Med vol.
Low vol.
Comparison of slopes
Models
Model 1
Model 2
Model 3
High vs Med
High vs Low
Med vs Low
HN-part.
-0.0232
(-2.55)**
-0.0202
(-3.65)***
-0.0041
(-1.20)
-0.0029
(-0.27)
-0.0191
(-1.97)*
-0.0161
(-2.48)**
Trade size
0.1292
(6.44)***
0.1104
(6.67)***
0.0679
(6.20)***
Price
-0.0229
(-0.33)
-0.0355
(-0.58)
-0.0641
(-1.20)
Intercept
-2.1002
(-8.09)***
-1.4561
(-6.77)***
-0.6685
(-4.11)***
R-square
0.1019
0.1153
0.0817
Panel D
High vol.
Med vol.
Low vol.
Comparison of slopes
Models
Model 1
Model 2
Model 3
High vs Med
High vs Low
Med vs Low
NH-part.
0.01755
(1.66)
0.0025
(0.52)
0.0002
(0.05)
0.0150
(1.30)
0.0174
(1.58)
0.0024
(0.41)
Trade size
0.1492
(7.20)***
0.1234
(7.06)***
0.0636
(5.35)***


### Page 31

31
Price
-0.0241
(-0.35)
-0.0266
(-0.42)
-0.0581
(-1.01)
Intercept
-2.1398
(-8.19)***
-1.5149
(-6.76)***
-0.6759
(-3.77)***
R-square
0.1032
0.1136
0.0690
Panel E
High vol.
Med vol.
Low vol.
Comparison of slopes
Models
Model 1
Model 2
Model 3
High vs Med
High vs Low
Med vs Low
NN-part.
0.0460
(4.28)***
0.0352
(3.66)***
0.0149
(2.27)**
0.0108
(0.74)
0.0311
(2.46)**
0.0203
(1.74)*
Trade size
0.1117
(5.56)***
0.0969
(7.40)***
0.0690
(8.49)***
Price
-0.0355
(-0.52)
-0.0284
(-0.47)
-0.0611
(-1.32)
Intercept
-1.8756
(-7.11)***
-1.3571
(-6.65)***
-0.6611
(-4.69)***
R-square
0.1133
0.1368
0.1149


### Page 32

32
Table 5-A: Predicting HFTs’ liquidity supply and demand changes univariate analysis
When VPIN level in a volume bucket is two standard deviations above the sample’s mean VPIN level, we
define that volume bucket as a VPIN event bucket (similar to Wu et al., 2013). VPIN event buckets are
considered to be high toxicity periods. The first bucket VPIN is two standard deviations above the sample
mean is considered as start of VPIN event. The last bucket extreme VPIN observed is considered as the
end of VPIN event. Prior 10, 5, and 1 windows start at 10, 5, and 1 buckets before the VPIN event starts.
All prior event windows end at the beginning of the VPIN event. After 1, 5, and 10 windows start at the
end of the VPIN event and lasts for 1, 5, or 10 buckets, respectively.
Prior 10             Prior 5                        Prior 1
VPIN EVENT                  After 1                        After 5                                    After 10
|
|
|
|                   |                    |                                    |                                              |
-10
-5                                  - 1                                  0                           0                     1                                  5                                             10
Mean 0 is the average liquidity supply/demand throughout the entire sample period, excluding VPIN
event periods and the window itself. Mean 1 is the average liquidity supply/demand in the stated volume
bucket window. We calculate the differences between Mean 0 and Mean 1 in each window, and test
statistical significance of differences with T-Tests and Wilcoxon Two-Sample Tests.
Panel A: HFT supply
Prior 10
Prior 5
Prior 1
During event
After 1
After 5
After 10
Mean 0
0.2497
0.2496
0.2494
0.2494
0.2493
0.2492
0.2492
Mean 1
0.2230
0.2241
0.2376
0.2144
0.2813
0.2706
0.2675
Difference
0.0267
0.0255
0.0118
0.0349
-0.0320
-0.0214
-0.0183
Panel B: HFT Demand
Prior 10
Prior 5
Prior 1
During event
After 1
After 5
After 10
Mean 0
0.3336
0.3333
0.3329
0.3328
0.3328
0.3328
0.3329
Mean 1
0.2680
0.2700
0.2901
0.2730
0.3406
0.3330
0.3282
Difference
0.0656
0.0633
0.0429
0.0598
-0.0078
-0.0002
0.0047
*All differences are statistically significant at 5% level. Except HFT demand in After 1 window which is
significant at 10% level, and After 5 window which is insignificant.
**Wilcoxon Two-Sample Tests also produce consistent results and available upon request.
***Kolmogorov-Smirnov test statistics also support that distributions of liquidity supply and demand
during event windows are different than the distributions during normal times. Results are available upon
request.


### Page 33

33
Table 5-B: Predicting HFTs’ liquidity supply and demand changes probit analysis
This table presents the results from estimating probit regression given by  𝑉𝑃𝐼𝑁 𝐸𝑣𝑒𝑛𝑡𝑖,𝜏= 𝛼𝑖,𝜏+
∑
𝛽𝑗
10
𝑗=1
𝑝𝑎𝑟𝑡𝑖𝑐𝑖𝑝𝑎𝑡𝑖𝑜𝑛 𝑟𝑎𝑡𝑒𝑖,𝜏−𝑗+ ∑
ʎ𝑗
10
𝑗=1
𝑝𝑟𝑖𝑐𝑒𝑖,𝜏−𝑗+ ∑
ᴪ𝑗
10
𝑗=1
𝑡𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒𝑖,𝜏−𝑗+ ɛ𝑖,𝜏. We define VPIN
threshold (similar to Wu et al., 2013) as mean VPIN plus two standard deviations of VPIN. When VPIN
level in a volume bucket is above VPIN threshold, we define that volume bucket as a VPIN event bucket
(similar to Wu et al., 2013). VPIN event buckets are considered to be high toxicity periods. In Panel A, we
calculate VPIN thresholds using VPIN values over whole sample period.  To allow on the fly examination,
in Panel B, we divide our sample into two subsamples, which consist of equal number of volume buckets.
Then, we use realized VPIN values of 1st subsample to calculate VPIN thresholds for the 2nd subsample.
HFT all is calculated following eq.1. HH-, HN-, NH-, and NN-participations are calculated as in eq.2. Trade
size is average number of shares traded per trade in a given volume bucket. Price is the average stock
price in a given volume bucket. Sample size (N) is 120. We employ ten lags in each variable and report
summation of the coefficients. We calculate t-statistics of summations based on robust standard errors
that are clustered at firm level. ***, ** and * represent significance at 1%, 5%, and 10% level, respectively.
Panel A
Overall sample
Panel B
On the fly examination
Panel A-1
Coeff
Robust t-stat
Panel B-1
Coeff
Robust t-stat
∑
𝐻𝐹𝑇 𝑎𝑙𝑙
10
1
l
-1.0418
(-10.18)***
∑
𝐻𝐹𝑇 𝑎𝑙𝑙
10
1
l
-0.9175
(-3.82)***
∑
𝑃𝑟𝑖𝑐𝑒
10
1
l
0.2589
(11.49)***
∑
𝑃𝑟𝑖𝑐𝑒
10
1
l
0.1714
(2.38)**
∑
𝑇𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒
10
1
l
0.8873
(18.06)***
∑
𝑇𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒
10
1
l
0.8753
(10.55)***
Intercept
-6.4735
(-24.98)***
Intercept
-6.0009
(-12.05)***
Pseudo R2
0.1269
Pseudo R2
0.1162
Panel A-2
Coeff
Robust t-stat
Panel B-2
Coeff
Robust t-stat
∑
𝐻𝐻 𝑃𝑎𝑟𝑡.
10
1
l
-3.4617
(-10.63)***
∑
𝐻𝐻 𝑃𝑎𝑟𝑡.
10
1
l
-2.7907
(-3.94)***
∑
𝑃𝑟𝑖𝑐𝑒
10
1
l
0.2435
(10.34)***
∑
𝑃𝑟𝑖𝑐𝑒
10
1
l
0.1601
(2.35)**
∑
𝑇𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒
10
1
l
0.9441
(19.26)***
∑
𝑇𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒
10
1
l
0.9140
(10.95)***
Intercept
-6.9362
(-27.47)***
Intercept
-6.3601
(-12.59)***
Pseudo R2
0.1317
Pseudo R2
0.1178
Panel A-3
Coeff
Robust t-stat
Panel B-3
Coeff
Robust t-stat
∑
𝐻𝑁 𝑃𝑎𝑟𝑡.
10
1
l
-0.5617
(-2.20)**
∑
𝐻𝑁 𝑃𝑎𝑟𝑡.
10
1
l
-1.3303
(-4.09)***
∑
𝑃𝑟𝑖𝑐𝑒
10
1
l
0.1825
(7.14)***
∑
𝑃𝑟𝑖𝑐𝑒
10
1
l
0.1570
(2.17)**
∑
𝑇𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒
10
1
l
0.7821
(10.62)***
∑
𝑇𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒
10
1
l
0.7496
(7.86)***
Intercept
-6.0886
(-15.30)***
Intercept
-5.4966
(-9.96)***
Pseudo R2
0.1001
Pseudo R2
0.1043
Panel A-4
Coeff
Robust t-stat
Panel B-4
Coeff
Robust t-stat
∑
𝑁𝐻 𝑃𝑎𝑟𝑡.
10
1
l
-1.6346
(-8.04)***
∑
𝑁𝐻 𝑃𝑎𝑟𝑡.
10
1
l
-1.0221
(-2.23)**
∑
𝑃𝑟𝑖𝑐𝑒
10
1
l
0.1813
(7.83)***
∑
𝑃𝑟𝑖𝑐𝑒
10
1
l
0.0961
(1.42)
∑
𝑇𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒
10
1
l
0.9473
(17.55)***
∑
𝑇𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒
10
1
l
0.8710
(9.57)***
Intercept
-6.7685
(-24.75)***
Intercept
-5.9997
(-11.04)***
Pseudo R2
0.1186
Pseudo R2
0.1016
Panel A-5
Coeff
Robust t-stat
Panel B-5
Coeff
Robust t-stat
∑
𝑁𝑁 𝑃𝑎𝑟𝑡.
10
1
l
1.0418
(10.18)***
∑
𝑁𝑁 𝑃𝑎𝑟𝑡.
10
1
l
0.9175
(3.82)***
∑
𝑃𝑟𝑖𝑐𝑒
10
1
l
0.2589
(11.49)***
∑
𝑃𝑟𝑖𝑐𝑒
10
1
l
0.1714
(2.38)**
∑
𝑇𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒
10
1
l
0.8873
(18.06)***
∑
𝑇𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒
10
1
l
0.8753
(10.55)***
Intercept
-7.5153
(-30.30)***
Intercept
-6.9183
(-12.22)***
Pseudo R2
0.1269
Pseudo R2
0.1162
We also conduct the same analyses for HFT demand and HFT supply, and find negative relations to the
VPIN events.


### Page 34

34
Table 6: HFTs’ impact on stock price variance regression results
This table presents the results from estimating the regressions given by 𝑆𝑡𝑑. 𝑑𝑒𝑣. 𝑜𝑓 𝑟𝑒𝑡𝑢𝑟𝑛𝑠𝑖,𝜏= 𝛼𝑖,𝜏+ 𝛽1𝑝𝑎𝑟𝑡𝑖𝑐𝑖𝑝𝑎𝑡𝑖𝑜𝑛 𝑟𝑎𝑡𝑒𝑖,𝜏−1 + 𝛽2 ln 𝑡𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒𝑖,𝜏−1 +
𝛽3ln 𝑝𝑟𝑖𝑐𝑒𝑖,𝜏−1 + ɛ𝑖,𝜏 . We estimate the regressions using generalized methods of moments, with the weighting matrix calculated according to Newey and
West (1987) with 50 lags. The t-statistics in parentheses reflect heteroskedasticity and autocorrelation consistent standard errors with 50 lags. The dependent
variable Standard deviation of returns is calculated from NASDAQ provided HFT data from Jan 2009 to Dec. 2009. “τ” is a volume bucket for a given firm “i”.
Standard deviation of returns is calculated in each volume bucket ““τ” for a given firm “i”. Returns are calculated using prices of consecutive trades. HFT all is
calculated following eq.1. HH-, HN-, NH-, and NN-participations are calculated as in eq.2. Trade size is average number of shares traded per trade in a given
volume bucket. Price is the average stock price in a given volume bucket. Sample size (N) is 120. ***, ** and * represent significance at 1%, 5%, and 10% level,
respectively.
Models
Model 1
Model 2
Model 3
Model 4
Model 5
HFT ALL
-0.0070
(-1.09)
HH-part.
0.0145
(0.86)
HN-part.
-0.0123
(-1.81)*
NH-part.
0.0202
(1.96)*
NN-part.
0.0070
(1.09)
Trade size
0.0013
(0.34)
0.0031
(0.77)
0.0026
(0.66)
0.0036
(0.36)
0.0013
(0.34)
Price
-0.0718
(-6.59)***
-0.0717
(-6.59)***
-0.0719
(-6.53)***
-0.0735
(-6.72)***
-0.0718
(-6.59)***
Intercept
0.2760
(7.27)***
0.2608
(6.85)***
0.2669
(6.98)***
0.2628
(6.92)***
0.2689
(7.10)***
R-square
0.06760
0.0617
0.0639
0.0648
0.0676


### Page 35

35
Table 7: HFTs’ impact on stock price variance across volume subsamples regression results
This table presents the results from estimating the regressions given by 𝑆𝑡𝑑. 𝑑𝑒𝑣. 𝑜𝑓 𝑟𝑒𝑡𝑢𝑟𝑛𝑠𝑖,𝜏= 𝛼𝑖,𝜏+
𝛽1𝑝𝑎𝑟𝑡𝑖𝑐𝑖𝑝𝑎𝑡𝑖𝑜𝑛 𝑟𝑎𝑡𝑒𝑖,𝜏−1 + 𝛽2 ln 𝑡𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒𝑖,𝜏−1 + 𝛽3ln 𝑝𝑟𝑖𝑐𝑒𝑖,𝜏−1 + ɛ𝑖,𝜏 . We estimate the regressions using
generalized methods of moments, with the weighting matrix calculated according to Newey and West (1987) with
50 lags. The t-statistics in parentheses reflect heteroskedasticity and autocorrelation consistent standard errors
with 50 lags. The dependent variable Standard deviation of returns is calculated from NASDAQ provided HFT data
from Jan 2009 to Dec. 2009. “τ” is a volume bucket for a given firm “i”. Standard deviation of returns is calculated
in each volume bucket ““τ” for a given firm “i”. Returns are calculated using prices of consecutive trades. HFT all
is calculated following eq.1. HH-, HN-, NH-, and NN-participations are calculated as in eq.2. Trade size is average
number of shares traded per trade in a given volume bucket. Price is the average stock price in a given volume
bucket. We compare slope differences following Paternoster, Brame, Mazerolle, and Piquero (1998). Each volume
sample consists of 40 stocks.  ***, ** and * represent significance at 1%, 5%, and 10% level, respectively.
Panel A
High vol.
Med vol.
Low vol.
Comparison of slopes
Models
Model 1
Model 2
Model 3
High vs Med
High vs Low
Med vs Low
HFT all
-0.0242
(-6.08)***
-0.0139
(-2.57)**
0.0171
(1.73)*
-0.0102
(-1.52)
-0.0413
(-3.86)***
-0.0311
(-2.75)***
Trade size
0.0095
(4.60)***
0.0059
(1.43)
-0.0114
(-2.10)**
Price
-0.0182
(-7.06)***
-0.0616
(-7.44)***
-0.1353
(-6.21)***
Intercept
0.0461
(3.27)***
0.2288
(7.04)***
0.5513
(8.21)***
R-square
0.0973
0.0499
0.0556
Panel B
High vol.
Med vol.
Low vol.
Comparison of slopes
Models
Model 1
Model 2
Model 3
High vs Med
High vs Low
Med vs Low
HH-part.
-0.0142
(-3.97)***
-0.0064
(-0.46)
0.0641
(1.97)*
-0.0078
(-0.54)
-0.01784
(-2.39)**
-0.0706
(-1.99)**
Trade size
0.0136
(5.80)***
0.0075
(1.80)*
-0.0119
(-2.20)**
Price
-0.0175
(-6.71)***
-0.0619
(-7.50)***
-0.1358
(-6.24)***
Intercept
0.0070
(0.48)
0.2154
(6.62)***
0.5599
(8.36)***
R-square
0.0820
0.0480
0.0553
Panel C
High vol.
Med vol.
Low vol.
Comparison of slopes
Models
Model 1
Model 2
Model 3
High vs Med
High vs Low
Med vs Low
HN-part.
-0.0135
(-4.00)***
-0.0164
(-2.89)***
-0.0069
(-0.61)
0.0029
(0.44)
-0.0065
(-0.55)
-0.0095
(-0.74)
Trade size
0.0135
(5.89)***
0.0066
(1.62)
-0.0124
(-2.29)**
Price
-0.0169
(-6.31)***
-0.0630
(-7.56)***
-0.1357
(-6.17)***
Intercept
0.0070
(0.48)
0.2276
(7.02)***
0.5662
(8.37)***
R-square
0.0863
0.0504
0.0552
Panel D
High vol.
Med vol.
Low vol.
Comparison of slopes
Models
Model 1
Model 2
Model 3
High vs Med
High vs Low
Med vs Low
NH-part.
-0.0097
(-2.38)**
0.0151
(1.44)
0.0055
(3.37)***
-0.0248
(-2.21)**
-0.0648
(-3.84)***
-0.0400
(-2.06)**
Trade size
0.0143
(6.13)***
0.0079
(1.91)*
-0.0114
(-2.11)**


### Page 36

36
Price
-0.0178
(-6.81***)
-0.0638
(-7.65)***
-0.1387
(-6.35)***
Intercept
0.0060
(0.43)
0.2190
(6.74)***
0.5633
(8.36)***
R-square
0.0861
0.0514
0.0568
Panel E
High vol.
Med vol.
Low vol.
Comparison of slopes
Models
Model 1
Model 2
Model 3
High vs Med
High vs Low
Med vs Low
NN-part.
0.0241
(6.08)***
0.0140
(2.57)**
-0.0171
(-1.72)*
0.0102
(1.52)
0.0412
(3.86)***
0.0311
(2.75)**
Trade size
0.0095
(4.60)***
0.0059
(1.45)
-0.0114
(-2.10)**
Price
-0.0182
(-7.06)***
-0.0617
(-7.44)***
-0.1353
(-6.21)***
Intercept
0.0219
(1.62)
0.2148
(6.61)***
0.5703
(8.43)***
R-square
0.0973
0.0499
0.0555


### Page 37

37
Table 8: HFTs’ impact on stock price variance during high toxicity periods regression results
This table presents the results from estimating the regressions given by 𝑆𝑡𝑑. 𝑑𝑒𝑣. 𝑜𝑓 𝑟𝑒𝑡𝑢𝑟𝑛𝑠𝑖,𝜏= 𝛼𝑖,𝜏+
𝛽1𝑝𝑎𝑟𝑡𝑖𝑐𝑖𝑝𝑎𝑡𝑖𝑜𝑛 𝑟𝑎𝑡𝑒𝑖,𝜏−1 + 𝛽2 ln 𝑡𝑟𝑎𝑑𝑒 𝑠𝑖𝑧𝑒𝑖,𝜏−1 + 𝛽3ln 𝑝𝑟𝑖𝑐𝑒𝑖,𝜏−1 + ɛ𝑖,𝜏 . We estimate the regressions using
generalized methods of moments, with the weighting matrix calculated according to Newey and West (1987) with
30 lags*. The t-statistics in parentheses reflect heteroskedasticity and autocorrelation consistent standard errors
with 30 lags. The dependent variable Standard deviation of returns is calculated from NASDAQ provided HFT data
from Jan 2009 to Dec. 2009. “τ” is a volume bucket for a given firm “i”. Standard deviation of returns is calculated
in each volume bucket ““τ” for a given firm “i”. Returns are calculated using prices of consecutive trades. HFT all
is calculated following eq.1. HH-, HN-, NH-, and NN-participations are calculated as in eq.2. Trade size is average
number of shares traded per trade in a given volume bucket. Price is the average stock price in a given volume
bucket. We compare slope differences following Paternoster, Brame, Mazerolle, and Piquero (1998). Each volume
sample consists of 40 stocks.  ***, ** and * represent significance at 1%, 5%, and 10% level, respectively.
Panel A
High vol.
Med vol.
Low vol.
Comparison of slopes
Models
Model 1
Model 2
Model 3
High vs Med
High vs Low
Med vs Low
HFT all
-0.0240
(-2.30)**
0.0036
(0.19)
0.0441
(1.41)
-0.0276
(-1.30)
-0.0680
(-2.07)**
-0.0404
(-1.11)
Trade size
0.0068
(1.72)*
0.0072
(0.85)
-0.0092
(-0.62)
Price
-0.0170
(-1.73)*
-0.0514
(-1.41)
-0.0804
(-1.21)
Intercept
0.0536
(1.26)
0.1894
(1.68)*
0.3713
(1.86)*
R-square
0.1037
0.0548
0.0511
Panel B
High vol.
Med vol.
Low vol.
Comparison of slopes
Models
Model 1
Model 2
Model 3
High vs Med
High vs Low
Med vs Low
HH-part.
-0.0125
(-0.97)
0.0489
(0.83)
0.1621
(1.63)
-0.0614
(-1.02)
-0.1746
(-1.74)*
-0.1132
(-0.98)
Trade size
0.0114
(2.57)**
0.0076
(0.90)
-0.0101
(-0.68)
Price
-0.0163
(-1.60)
-0.0521
(-1.42)
-0.0816
(-1.22)
Intercept
0.0120
(0.29)
0.1881
(1.68)*
0.3863
(1.93)*
R-square
0.0823
0.0534
0.0516
Panel C
High vol.
Med vol.
Low vol.
Comparison of slopes
Models
Model 1
Model 2
Model 3
High vs Med
High vs Low
Med vs Low
HN-part.
-0.0209
(-2.21)**
-0.0073
(-0.37)
0.0113
(0.30)
-0.0136
(-0.62)
-0.0322
(-0.84)
-0.0186
(-0.44)
Trade size
0.0109
(2.55)**
0.0066
(0.79)
-0.0112
(-0.76)
Price
-0.0161
(-1.57)
-0.0520
(-1.41)
-0.0825
(-1.22)
Intercept
0.0175
(0.43)
0.1963
(1.74)*
0.3973
(1.95)*
R-square
0.0876
0.0544
0.0468
Panel D
High vol.
Med vol.
Low vol.
Comparison of slopes
Models
Model 1
Model 2
Model 3
High vs Med
High vs Low
Med vs Low
NH-part.
-0.0095
(-0.92)
0.0414
(1.12)
0.1148
(1.94)*
-0.0509
(-1.33)
-0.1244
(-2.07)**
-0.0734
(-1.05)
Trade size
0.0115
(2.68)**
0.0080
(0.35)
-0.0095
(-0.65)


### Page 38

38
Price
-0.0168
(-1.65)
-0.0535
(-1.46)
-0.0821
(-1.27)
Intercept
0.0153
(0.38)
0.1892
(1.70)*
0.3810
(1.96)*
R-square
0.0868
0.0589
0.0583
Panel E
High vol.
Med vol.
Low vol.
Comparison of slopes
Models
Model 1
Model 2
Model 3
High vs Med
High vs Low
Med vs Low
NN-part.
0.0239
(2.30)**
-0.0036
(-0.19)
-0.0441
(-1.41)
0.0276
(1.30)
0.0680
(2.07)**
0.0404
(0.27)
Trade size
0.0068
(1.72)*
0.0072
(0.85)
-0.0092
(-0.62)
Price
-0.0170
(-1.73)*
-0.0514
(-1.41)
-0.080
(-1.21)
Intercept
0.0296
(0.76)
0.193
(1.73)*
0.4153
(2.08)**
R-square
0.1036
0.0548
0.0511
*The low number of observations in some sub-volumes forced us to use thirty lags.

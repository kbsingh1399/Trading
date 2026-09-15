# Illiquid Bitcoin Options∗

- **Source File**: `ssrn-4280098.pdf`
- **Total Pages**: 43
- **SSRN ID**: `ssrn-4280098`

---

## Page 1

Illiquid Bitcoin Options∗
Yang Guo†
Jiasun Li‡
Mei Luo§
Yintian Wang¶
November 17, 2022
Abstract
This paper conducts a first look into the regulated Bitcoin options market in the
United States. Compared to stock options, bitcoin options tend to be ten times more
illiquid as measured by bid-ask spreads.
The illiquidity significantly affects bitcoin
options pricing: Given that investors are on average net sellers of bitcoin options,
heightened illiquidity is associated with a significant premium in subsequent delta-
hedged returns, which also strengthens under more imbalanced investor orders. To
support the reasoning behind our findings, we further exploit a policy change that
allows retail participation and significantly influences order imbalances in the Bitcoin
options market.
Keywords: Bitcoin; Derivatives; Options; Liquidity.
∗The authors thank the financial support from the Research Center for Digital Financial Assets at School
of Economics and Management, Tsinghua University.
†guoyang1@caict.ac.cn. China Academy of Information and Communications Technology.
‡jli29@gmu.edu. George Mason University, 4400 University Drive, MSN 5F4, Fairfax, VA 22030, USA.
§luomei@sem.tsinghua.edu.cn. School of Economics and Management, Tsinghua University.
¶wangyt2@sem.tsinghua.edu.cn. School of Economics and Management, Tsinghua University.
1
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 2

In 2017, the Commodity Futures Trading Commission (CFTC) approved the first Bitcoin
options contract in the United States. After five years of operation, we now have enough
evidence to conduct a serious study of this new market. This paper looks into the US-
based regulatory-compliant Bitcoin options market and uncovers several facts about this
new product that could be of interest to academics, investors, and regulators as well.
There are many reasons why it is timely to focus on the Bitcoin options market. First,
although there is a growing literature studying the market of financial derivatives with Bit-
coin as the underlying asset, much focus has been given to futures contracts only. Given
that options are more complicated products than futures, and that retail investors do par-
ticipate in the Bitcoin options market (as our later evidence will suggest), it is important
to inform the public of how the market performs and its key features. Second, similar to
Bitcoin futures, most Bitcoin options trading activities occur in overseas markets that nei-
ther comply with US regulations nor give access to US residents. Therefore, conclusions
drawn from these exchanges, although useful, may not be directly relevant to US investors
or regulators. Given ample evidence of market manipulations in unregulated exchanges from
the spot market for cryptocurrency, one may also expect less confounded results for crypto
derivatives from a regulated exchange. Finally, lessons learned from Bitcoin options may
also provide additional evidence to help us better understand options in traditional markets.
The CFTC-approved Bitcoin options contracts are traded on the LedgerX exchange
(which is recently acquired by the FTX.US exchange) as a “dealers-driven” market – that is,
designated liquidity providers simultaneously post bid and ask prices waiting for prospective
investors. We gather transaction data from the exchange and present several findings of this
CFTC-approved options market.
Our first major finding is that bitcoin options tend to feature extremely high bid-ask
spreads. Compared to stock options that typically have an average bid-ask spread of 7%
- 8% of the mid-quote price (Christoffersen, Goyenko, Jacobs and Karoui (2018)), Average
2
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 3

Bitcoin options spreads are almost ten times by magnitude. Therefore, the Bitcoin options
market in the United States so far is highly illiquid.
The high illiquidity indicates that transaction costs should be one of the first-order con-
siderations in the Bitcoin options market beyond the traditional Black-Scholes framework.
The rest of the paper then quantifies how such illiquidity influences bitcoin options pricing,
as measured by subsequent delta-hedged returns following the literature convention.
It is ex ante unclear whether increased illiquidity should be associated with higher or
lower subsequent delta-hedged returns, despite convention wisdom from the stock market
associating illiquidity and premiums in expected returns. The nuance comes from the fol-
lowing fact: as assets with positive supplies, stocks typically feature marginal investors who
are longing the stocks. Hence, heightened illiquidity renders a stock less attractive, lowering
its current price and increasing its subsequent returns. Options, on the other hand, are
assets of zero net supplies. Therefore, the relationship between illiquidity and subsequent
delta-hedged return depends on whether the price-setting marginal investor, or in our options
market, designated liquidity providers who constantly set bid and ask prices, are longing or
shorting the options. In case the designated liquidity providers are on the shorting side,
they may require a higher selling price to short the less-attractive options due to heightened
illiquidity, rendering a discounted subsequent delta-hedged return. In short, for a zero-net
supply asset like Bitcoin options, the effect of illiquidity may very well flip signs depending
on the signs of designated liquidity providers’ inventories.
To carry forward our analysis, we further probe whether designated liquidity providers
are on average buying or selling Bitcoin options. Toward this end, we classify each trade
into either a buy-initiated or sell-initiated one and calculates the order imbalance in the
options market. While we find significant intertemporal variations in order imbalances, on
average there are significantly more sell-initiated trades than buy-initiated ones, indicating
more selling pressure from liquidity takers. To the extent that client investors take liquidity
3
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 4

by initiating trades in response to designated liquidity providers’ quotes, the finding suggests
that designated liquidity providers on average long bitcoin options. Therefore, we expect
heightened options illiquidity to be associated with premia in subsequent delta-hedged re-
turns. Consistently, we find that a 0.1 increase in relative bid-ask spread is associated with
a 0.26% increase in subsequent delta-hedged return. Regarding the intertemporal variations
in order imbalance, we expect the positive association between illiquidity and subsequent
delta-hedged return to strengthen (attenuate) as selling (buying) pressure increases. Con-
sistently, we find that a 0.1 increase in imbalance is associated with a 0.30% decrease in the
regression coefficient of subsequent delta-hedged return on illiquidity.
In sum, we find that the illiquidity characterizing Bitcoin options has significant im-
pact on the market. Specifically, options illiquidity is associated with higher returns, which
strengthens when designated liquidity providers are more tilted toward the buying side.
To support the above findings and reasoning, we further supplement our regression results
with a natural experiment that exogenously shifts the overall order imbalance in the market.
In August 2019, upon regulatory approval, LedgerX implemented a policy change so that
small retailer investors in the United States are given access to the Bitcoin options market.
Such a policy change brought significant shifts in the composition of market participants and
witnessed significantly more buying pressure from liquidity-taking client investors. Indeed,
order imbalance on average shifted from significantly sell-initiated before the policy change
to a much more balanced market after the change. Therefore, based on this observation and
our reasonings earlier, we expect a stronger illiquidity-return premium association before the
policy change, and a significant sensitivity of such an association to order imbalances after
the change. We find results consistent with our expectations as we replicate our tests for the
before and after subsamples.
Our findings give a first look at the regulated Bitcoin options market in the United States
and offers a fact-check of this new market over the last five years of operation. The high
4
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 5

bid-ask spread of bitcoin options suggests that illiquidity should be given more attention
to all investors and regulators, especially given that retail investors have access to and also
participate in this market. Our findings also contribute to the literature on options in general,
demonstrating how existing theories on options could be applied and should be adapted to
the practice of options on the new asset class of Bitcoins.
Related literature
Our paper contributes to an emerging literature on crypto derivatives. Most of the existing
papers focus on futures contracts. Augustin, Rubtsov and Shin (2020) study the impact
of the introduction of Bitcoin futures contracts by CBOE and CME in December 2017 on
the Bitcoin cash market. Ferko, Moin, Onur and Penick (2022) use regulatory data internal
from the CFTC and analyze the composition of Bitcoin futures traders. On Bitcoin options,
Alexander, Deng, Feng and Wan (2022) study the impact of order imbalance on Bitcoin
options pricing. Their analysis is based on Deribit, the largest unregulated Bitcoin options
exchange that does not allow US investors, while our analysis is based on LedgerX, a CFTC-
approved Bitcoin options exchange which for a large portion of our sample the only Bitcoin
options exchange in the United States.
Our paper also contributes to the now vast literature on cryptocurrency trading in the
spot market. On cryptocurrency pricing across exchanges, Makarov and Schoar (2020) as
well as Yu and Zhang (2022) document extensive arbitrage opportunities across spot cryp-
tocurrency exchanges; Choi, Lehar and Stauffer (2022) and Hautsch, Scheuch and Voigt
(2018) relate such arbitrage opportunities to congestions in Bitcoin’s transaction inclusions
into blocks. On the demand for cryptocurrencies on secondary markets, Shams (2020) relate
cryptocurrency returns to common investor bases across spot exchanges; Benetton and Com-
piani (2021) study the demand for cryptocurrencies in secondary market trading; Divakaruni,
5
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 6

Zimmerman et al. (2021) analyze how the Covid-19 stimulus checks feed into bitcoin demand.
Relatedly, Li and Yi (2019), Liu, Tsyvinski and Wu (2022), and Cong, Karolyi, Tang and
Zhao (2022) explore risk factor structures of cryptoassets. Finally, on various manipulations
on spot cryptocurrency exchanges, Li, Shin and Wang (2021) document pump-and-dump
schemes in cryptocurrency spot markets; Gandal, Hamrick, Moore and Oberman (2018)
document price manipulations on the unregulated Mt. Gox exchange; Griffin and Shams
(2020) document potential Bitcoin spot price manipulation by entities controlled by the
issuer of the stablecoin Tether; Cong, Li, Tang and Yang (2021), Amiram, Lyandres and
Rabetti (2020), and Aloosh and Li (2019) also document estimations as well as direct evi-
dence of unregulated cryptocurrency spot exchanges faking trading volumes by conducting
or encouraging “wash trading.” Because our sample focuses on the CFTC-regulated Bitcoin
options market, our findings are less prone to such confounding factors. Finally, our paper
also touches upon the regulation of the crypto market in general, as in Li and Mann (2018,
2021).
Outside of the blockchain literature, our paper also contributes to the options literature in
general. While studies on options are too numerous to adequately summarize here, the most
related ones are ones that focus on the relationship between options liquidity and pricing,
with potential considerations of order imbalance. Deuskar, Gupta and Subrahmanyam (2011)
take imbalance as constant over time and study the interaction between options pricing
and illiquidity measured by the relative bid-ask spread. Christoffersen, Goyenko, Jacobs
and Karoui (2018) present a set of regressions that further relate illiquidity, imbalance, and
options pricing. More broadly, our paper also contributes to the literature on the relationship
between illiquidity, imbalance, and returns for more general assets. In the stock market.
Hasbrouck and Seppi (2001) and Chordia, Roll and Subrahmanyam (2002) give statistical
characterizations and regression tests of the interactions among the three variables (PCA
or correlations), respectively.
The theory of Acharya and Pedersen (2005) and evidence
6
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 7

from the CDS market in Bongaerts, De Jong and Driessen (2011) further study the effect of
liquidity risk.
Finally, since we study bitcoin options on a centralized exchange, our results complement
the literature on decentralized exchanges, including Lehar and Parlour (2021), Capponi and
Jia (2021), Aoyagi and Ito (2021), as well as Han, Huang and Zhong (2021).
The rest of the paper is organized as follows. Section 1 provides a brief introduction to
the institutional background of bitcoin options. Section 2 discusses the data used for our
analysis. Section 3 constructs illiquidity measures and presents evidence of Bitcoin options’
illiquidity.
Section 4 investigates how illiquidity affects Bitcoin options returns.
Section
5 presents additional results from a policy change that shocks the composition of market
participants. Section 6 then concludes.
1
Institutional background
A bitcoin options contract is conceptually similar to an options contract on other assets. A
call option gives its holder the right, but not the obligation to purchase a certain number of
underlying assets at a pre-determined strike price either at a particular future time (European
options) or any time before a particular future time (American options). Similarly, a put
option gives its holder the right, but not the obligation to sell a certain number of underlying
assets.
As bitcoin rise to become a major asset class, various entities began to offer venues for
trading options on bitcoin. Most such bitcoin options exchanges do not have approval from
the CFTC or regulators from other major economies to clear derivatives, so they do not
allow US residents from participating on such platforms.
Major overseas Bitcoin options exchanges include Deribit (founded in 2016), OKX (founded
in 2017), and Bit.com (founded in 2019), of which the Netherland-based Deribit is the largest
7
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 8

one by reported open interests, accounting for a bit shy of 90% of open interests. How-
ever, Deribit is unavailable to citizens or residents of the United States, as well as Cuba,
Ontario (Canada), Guam, Iran, Iraq, Japan, North Korea, Panama, Puerto Rico, Samoa,
Sudan, Syrian, and U.S. Virgin Islands, and partially restricted to a few other jurisdictions.
Similarly, the Seychelles-based OKX is not available in the U.S. The newcomer Bit.com is
also based in Seychelles. According to its support article (https://support.bit.com/hc/en-
us/articles/360051112014), its access and its services are not available for individuals or
corporations located, incorporated, established in, or a citizen or resident of any of the fol-
lowing regions: China Mainland, Hong Kong, North Korea, Japan, Iran, Singapore, Syria,
American Samoa, Canada, Cuba, Guam, Puerto Rico, Northern Mariana Islands, United
States, Crimea, and Sevastopol.
Before late 2017, US residents do not have access to options trading on bitcoins. After
months of lobbying, on September 2, 2017, the CFTC announced the approval of LedgerX, a
digital currency platform, for clearing derivatives. In addition to being the first approved bit-
coin options exchange in the United States, LedgerX was also the only regulatory-compliant
bitcoin options exchange in the United States for many years, until the Chicago Mercantile
Exchange (CME) launched options on Bitcoin futures in January 2020. In Oct 25, 2021,
LedgerX was acquired by FTX.US to be rebranded as FTX US Derivatives. The acquisi-
tion had no material impact on LedgerX’s operations as it continued to provide its current
offerings to existing customers, and we will continue to refer to the exchange as LedgerX
throughout the paper.
LedgerX operates as a “dealer-driven” market in which designated liquidity providers
simultaneously submit bid and ask quotes. According to LedgerX’s rule book (Chapter 4
Liquidity Providers), interested party may complete a Liquidity Provider Agreement and be
appointed by the exchange as a Liquidity Provider for certain series of contracts. Liquidity
providers receive reduced trading fees or other incentives, while are obliged to “make good-
8
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 9

faith efforts to enter on the Platform current binding bid and offer quotes, with a bid/offer
spread as specified in the applicable Liquidity Provider Agreement, as necessary to ensure
liquidity.”
The flagship product by LedgerX is the European style Bitcoin Mini Options (Calls &
Puts), which are physically settled monthly or weekly options on bitcoin. Their contract sizes
are of 0.01 bitcoin , the minimum price fluctuation is $1.00, prices are quoted in U.S. dollars
per bitcoin, and trading hours are 24 × 7. Trading fees are the lower of $0.15 per contract
or 20% of the options premium per contract, and the minimum block is 100 contracts (1
BTC). The strike intervals are the following: For each new expiration month, LedgerX lists
at least five strikes in $1,000 strike intervals. The exchange will add additional strikes as
the expiration month approaches additional strikes in accordance with the underlying price
movement using 1000, 2500, or 5000 strike increments. In the first half of every current
month, the exchange may list additional contracts for the current month. In the second
half of the current month, FTX US Derivatives may list additional contracts for the current
month and the following month. For weekly contracts, the exchange will introduce a strike at
the At-The-Money (ATM) level, and at minimum two strikes above and two strikes below the
ATM level in $1,000 strike intervals. The exchange will add additional strikes in accordance
with the underlying price movement using 1000, 2000, 4000 strike increments. Weekly strikes
may be listed up to 20% above the ATM strike level and down to 20% below the ATM strike
level, in accordance with BTC price volatility.
2
Data
We obtain all options trade data on LedgerX (from February 2018 to January 2022) using the
exchanges’ API. The trades data contain the contract, transaction size, price, and timestamp
for each transaction. We will use the high-frequency data to construct daily variables of
9
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 10

interest. The API provides high-frequency quote updates and quotes at the daily frequency
are obtained from LedgerX website, which indicates the last prevailing quotes of each trading
day. We also obtain Bitcoin spot price and volume from CoinMarketCap, a popular data
aggregator for the cryptocurrency market. For the appropriate risk-free rate in the Bitcoin
market, we follow industry wisdom in Radovan and Matus (2020) and use 3.69%, although
our conclusions are not sensitive to the choice of risk-free rates.
Following the literature convention (e.g. Christoffersen, Goyenko, Jacobs and Karoui
(2018) and Choy and Wei (2022)), we filter out the following contract-day samples: (1)
samples with maturity below 10 days or above 360 days; (2) samples with zero open interest;
(3) samples with missing last bid or last ask, or samples whose last bid is higher than or
equal to the last ask; (4) samples that violate options price boundaries and yield arbitrage
opportunities. Overall, the filtering process reduces the sample size from 52,517 to 31,334,
mostly due to contracts that have super long maturities. Finally, since LedgerX changed the
contract size in December 2019, we adjust the sample before and after the change so that
each contract corresponds to the same underlying asset of one bitcoin.
[Figure 1 about here.]
Figure 1 presents the time-series of bitcoin prices, bitcoin trading volume, bitcoin volatil-
ity, and bitcoin options trading volume on LedgerX. Overall, the bitcoin price goes up over
time despite significant volatility. Bitcoin option volume on LedgerX also tends to increase
over time, indicating increasing interest from investors into this new market.
[Table 1 about here.]
Table 1 provides summary statistics of all the listed options. Among the 31,334 contracts
in total, there are 21,287 calls and 10,047 puts. The average maturity is about 99 days, while
strikes range from $2,000 to $400,000, averaging at about $40,000.
10
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 11

3
Options Illiquidity
This section investigates the liquidity (or illiquidity) of bitcoin options. Following Christof-
fersen, Goyenko, Jacobs and Karoui (2018), we measure options illiquidity by relative spread,
as defined below:
Relative Spread (RS):
for a given contract n and day t, its relative spread RSnt is defined
as
RSnt =
last asknt −last bidnt
(last asknt + last bidnt)/2
where last asknt and last bidnt denotes the last ask and bid for contract n on day t. That is,
the relative spread is the ratio between the quoted bid-ask spread and the mid-quote price.
[Table 2 about here.]
Table 2A provides summary statistics of relative spreads for calls and puts across differ-
ent moneyness categories. A salient feature of the bitcoin options market is its illiquidity.
Average relative spread can be as high as 74.9% for calls and 83.4% for puts. In compari-
son, relative spreads for stock options are typically 7% for calls and 8% for puts according
to Christoffersen, Goyenko, Jacobs and Karoui (2018). Puts tend to have larger relative
spreads than calls. Consistent with options in other markets, out-of-the-money (OTM) op-
tions have the highest spreads for both calls and puts while in-the-money options have the
lowest relative spreads. To avoid concerns over the high average spread being driven by
inactive outliers, Table 2A also reports volume-weighted averages. Results paint a similar
picture: the volume-weighted average of spreads is as high as 80% for calls and 73.3% for
puts.
While relative spread is our main interested variable to measure option illiquidity, for
11
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 12

robustness, we also alternatively adopt the Amihud (2002) liquidity measure, as defined
below:
Amihud liquidity measure (Amihud):
For a given contract n and day t, the Amihud
liquidity measure Amihudnt is defined as
Amihudnt = |returnt|
volumet
that is, the Amihud liquidity measure calculates the ratio between the absolute value of daily
return over daily trading volume. Table 2B provides summary statistics of Amihud for calls
and puts across different moneyness categories.
[Figure 2 about here.]
Figure 2 plots the time series of the daily relative spread for Bitcoin options over time
(Panel A), as well as similar measures for Bitcoin spot for comparison (Panel B). After
smoothing, we find both series to have similar trends across time (both tend to increase over
time), indicating that illiquidity of options contracts is highly correlated with that of the
underlying assets (the correlation is 0.52). Relative spreads of options are also much more
volatile before a policy change (indicated by the green line) in August 2019 to be described
in detail in Section 5. Similarly, we compare the Amihud measure for options (Panel C) and
that for Bitcoin spot (Panel D). while Amihud measures for Bitcoin options also tend to
increase over time, those for Bitcoin spot tend to first decrease then increase (a U-shape).
The pattern indicates that relative spreads and Amihud measures tend to capture different
aspects of Bitcoin options and spot illiquidity.
12
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 13

4
Impact of Illiquidity on Options Returns
Having documented the illiquid nature of bitcoin options, it is natural to ask how such
friction affects the bitcoin options pricing and return. Following the literature, we focus on
the delta-hedged return of bitcoin options, as defined below:
Delta-hedged return (DHR):
For a specific options contract n on a specific day t, we
have
˜Ro
t+1,n = Ro
t+1,n −RS
t+1St
∆t,n
ot,n
where ˜Ro
t+1,n denotes the daily delta-hedged options return, Ro
t+1,n denotes the (raw) daily
options return, RS
t+1 denotes the daily Bitcoin spot return, St denotes the spot market price
of Bitcoin, Ot,n denotes the options price, and ∆t,n denotes the options delta based on the
Black Scholes formula. Figure 3 presents the average daily delta-hedged options returns,
separating between calls and puts as well as at-the-money (ATM) and all options.
[Figure 3 about here.]
Table 3 reports summary statistics for daily delta-hedged options returns. We first com-
pute respective statistics for each options class and report the average across options classes.
We also report the average number of options series per options class for each moneyness cat-
egory. The delta-hedged return averages are small and positive and exhibit positive skewness
and excess kurtosis in all categories. The returns of options also display rapid mean-reversion
as evidenced by the negative first-order autocorrelation. These reversals are suggestive of
the importance of liquidity provision in this market. Table 3 also reports sample statistics
for bitcoin returns in panel C. Not surprisingly, volatility and skewness are both much lower
for bitcoin returns than for options returns, while kurtosis is quite high for bitcoin returns.
13
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 14

[Table 3 about here.]
We test whether illiquidity influences subsequent delta-hedged returns. This question
does not have clear answer a priori. Indeed, as a derivative asset with zero net supply, the
impact of illiquidity on options is more nuanced than other financial assets (e.g. stocks)
with positive supply. This is because for assets with positive supply, the marginal investor
is always on the long side, so that illiquidity unambiguously drives down price and lead to
higher future returns. For bitcoin options in a dealer-driven market, the designated liquidity
providers ultimately set prices, so the effect of illiquidity on options ultimately depends on
the net holding position of designated liquidity providers (“dealers”).
To infer the net holding positions of the liquidity providers, we exploit the fact that
liquidity-taking client investors respond to designated liquidity providers’ bid-ask quotes.
Therefore, designated liquidity providers’ trading directions can be inferred as the opposite
of the order imbalance among all trades. Hence, we first apply the tick rule to determine
the trading direction of each transaction, and then define imbalance as the following:
Imbalance:
For a specific options contract n on a specific day t, imbalance is defined as
Imbalancent = #buynt −#sellnt
#buynt + #sellnt
where #buynt (#sellnt) denotes the number of buy-initiated (sell-initiated) trades for
contract n on day t. It is immediately to see that imbalance falls within [−1, 1]. A positive
imbalance indicates that most trades are triggered by buyers, while a negative imbalance
indicates that most trades are triggered by sellers.
The first row in Table 6 reports summary statistics of the imbalance measure. On average,
the imbalance measure tends to be negative, indicating sell pressures from liquidity takers.
Hence, designated liquidity providers on average long the options, so that we have our first
14
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 15

hypothesis:
Hypothesis 1:
Illiquidity precedes high return. That is, with average negative imbalance
(i.e. liquidity-taking client investors on average sell bitcoin options), higher options illiquidity
is associated with a lower options price, and thus a higher subsequent delta hedged return.
[Table 4 about here.]
As a preliminary illustration of Hypothesis 1, Table 4 sorts options into three groups with
high, median, and low levels of relative spreads (amihud), and presents the average next-day
(both equal-weighted and volume-weighted) delta-hedge returns within each group, as well
as the return spread between the high and low groups. For both calls and puts and across
all windows, higher illiquidity is followed by significantly higher delta-hedged returns. These
findings are consistent with Hypothesis 1, which will be more formally tested later. Figure
4 illustrates the findings from Table 4.
[Figure 4 about here.]
That said, imbalance also fluctuates over time, which can go positive from time to time.
On these days, we should expect the positive association in Hypothesis 1 to flip sign. In
other words, and days with higher imbalance, we expect lower positive associations between
illiquidity and subsequent delta-hedged returns.
In other words, we form the following
hypotheses:
Hypothesis 2:
The association between options illiquidity and subsequent delta-hedged
return is lower when imbalance is higher.
To test both hypotheses, we develop the following regression: Illiquidity drive down(up)
options prices under net selling(buying) pressure.
DHRt+1 = α0 + α1Illiquidityt + α2Illiquidityt × imbalancet + Controls + ϵ
15
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 16

where DHR is delta-hedged return over day t + 1, illiquidity is measured by either the
relative spread or the Amihud measure of Bitcoin options. To avoid a mechanical relation-
ship between relative spreads and subsequent returns due to their common denominator of
end-of-day option price, we use lagged relative spreads to capture illiquidity. Coefficients on
illiquidity measures captures their average impact on subsequent delta-hedged return, while
coefficients on the interaction of illiquidity measures and imbalance capture the additional
effect of illiquidity as imbalance changes. Controls include option order imbalances and bit-
coin spot liquidity also measured by the relative spread and the Amihud liquidity measure
(of bitcoin spot), option moneyness measured by the absolute value of option delta, bitcoin
spot beta estimated from 365-day rolling window, daily spot return, option maturity mea-
sured by ln(days to expiration), and Bitcoin spot volatility estimated from the GARCH(1,1)
model.
[Table 5 about here.]
Table 5 presents the regression results. The coefficients on the relative spread and the
Amihud liquidity measure are both significantly positive (0.026 with the t-value of 5.98 and
0.007 with the t-value of 9.93) suggesting that illiquidity is associated with a return premium
(Hypothesis 1). The coefficients on the interaction terms between illiquidity measures are
both significantly negative(−0.03 with the t-value of −6.83; −0.007 with the t-value of
−7.32), indicating that a higher imbalance is associated with an attenuation in the positive
association between illiquidity and subsequent delta-hedged returns.
Besides statistical significance, the findings are also economically significant: When the
relative spread increases by a level of 0.1, under fully buying pressure from client investors
(an imbalance of 1), the daily delta-hedged return decreases by 0.30%, which translates to
a decreased annual return of 109.5%. In addition, when the relative spread increases by a
level of 0.1, designated liquidity providers facing an overall selling pressure would decrease
16
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 17

options prices such that the expected annual return would increases by 95%.
5
Policy shock
To strengthen the argument of the previous section, we further exploit a natural experiment.
On July 31, 2019, LedgerX announced the launch of its Omni trading platform, which under
the approval of CFTC allows retail customers to “trade bitcoin, bitcoin options, and futures.”
This policy change can be thought of as a shock that changes the composition of options
traders with different trading demands, and as a result, the overall imbalance of the options
market.
[Figure 5 about here.]
As Figure 5 illustrates, the incoming retail options investors after the policy shock are
net buyers of options. Table 6 formally summaries the imbalance measures before and after
the policy change, with a t-test showing significant differences in imbalance measure before
and after. As the second and third row of Table 6 indicates, the incoming retail options
investors after the policy shock indeed bring the on average negative imbalance before the
policy change to close to zero after the change.
[Table 7 about here.]
We reevaluate our Hypothesis 1 and 2 for the sample before and after the policy change.
Since the inflow of retail investors brings along more balanced buy-sell pressures, we expect
the return premium following heightened illiquidity to attenuate after the policy change.
Table 7 presents results consistent with the reasoning: the effect of illiquidity on options
prices diminishes after the policy, reflected by lower coefficients (e.g. 0.025 after compared
to 0.082 before and 0.007 after compared to 0.647 before).
17
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 18

[Table 8 about here.]
Table 7 also shows that after the policy change, coefficients for the interaction term
between illiquidity and imbalance is still significantly negative (-0.029 with the t-value of
-6.23; -0.007 with the t-value of -7.17), suggesting that the more balanced overall buy/sell
pressure (the level of imbalance) does not mitigate the impact of the changes in imbalance
on the return premium following illiquidity.
6
Conclusions
Despite over five years of development, the US Bitcoin options market is still highly illiquid.
In addition, investors on average sell options, although the net sell-tilted imbalance has been
eased when more small retail investors are admitted. Under such a market composition, the
illiquid nature of Bitcoin options significantly affects their pricing, with higher illiquidity as-
sociated with higher subsequent delta-hedged return. The finding highlights the importance
of paying attention to transaction costs in the Bitcoin options market. The finding may
also provide guidance for regulators and prospective investors as more spot cryptocurrency
exchanges probe into the derivatives market.
As a first study into the US Bitcoin options market, we have left many unanswered
questions. For example, our finding calls for further investigations into the reasons behind
the high bid-ask spread of Bitcoin options: Is it due to Bitcoin’s high volatility or frictions
in the cryptocurrency market that hinder effective risk management of bitcoin options?
Or, is it due to a lack of competition between designated liquidity providers or a lack of
competition among exchanges? Or, is it due to a lack of demand for bitcoin options in the first
place? Answers to these questions would lead to different policy recommendations, ranging
from approving more Bitcoin options exchanges/licensing more Bitcoin options designated
liquidity providers to enforcing guidelines to Bitcoin options designated liquidity providers
18
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 19

or rethinking the value of Bitcoin options as a product. We leave these important questions
to future research.
References
Acharya, Viral V, and Lasse Heje Pedersen. 2005. “Asset pricing with liquidity risk.”
Journal of financial Economics, 77(2): 375–410. 6
Alexander, Carol, Jun Deng, Jianfen Feng, and Huning Wan. 2022. “Net buying
pressure and the information in bitcoin option trades.” Journal of Financial Markets,
100764. 5
Aloosh, Arash, and Jiasun Li. 2019. “Direct evidence of bitcoin wash trading.” Available
at SSRN 3362153. 6
Amiram, Dan, Evgeny Lyandres, and Daniel Rabetti. 2020. “Competition and prod-
uct quality: fake trading on crypto exchanges.” Available at SSRN 3745617. 6
Aoyagi, Jun, and Yuki Ito. 2021. “Coexisting Exchange Platforms: Limit Order Books
and Automated Market Makers.” 7
Augustin, Patrick, Alexey Rubtsov, and Donghwa Shin. 2020. “The impact of deriva-
tives on spot markets: Evidence from the introduction of bitcoin futures contracts.” 5
Benetton, Matteo, and Giovanni Compiani. 2021. “Investors beliefs and cryptocur-
rency prices.” Working paper. 5
Bongaerts, Dion, Frank De Jong, and Joost Driessen. 2011. “Derivative pricing with
liquidity risk: Theory and evidence from the credit default swap market.” The Journal of
Finance, 66(1): 203–240. 7
19
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 20

Capponi, Agostino, and Ruizhe Jia. 2021. “The adoption of blockchain-based decen-
tralized exchanges.” arXiv preprint arXiv:2103.08842. 7
Choi, Kyoung Jin, Alfred Lehar, and Ryan Stauffer. 2022. “Bitcoin microstructure
and the Kimchi premium.” Available at SSRN 3189051. 5
Chordia, Tarun, Richard Roll, and Avanidhar Subrahmanyam. 2002. “Order im-
balance, liquidity, and market returns.” Journal of Financial economics, 65(1): 111–130.
6
Choy, Siu Kai, and Jason Wei. 2022. “Option trading and returns versus the 52-week
high and low.” Financial Review, 57(3): 691–726. 10
Christoffersen, Peter, Ruslan Goyenko, Kris Jacobs, and Mehdi Karoui. 2018.
“Illiquidity premia in the equity options market.” The Review of Financial Studies,
31(3): 811–851. 2, 6, 10, 11, 29
Cong, Lin William, George Andrew Karolyi, Ke Tang, and Weiyi Zhao. 2022.
“Value Premium, Network Adoption, and Factor Pricing of Crypto Assets.” Network
Adoption, and Factor Pricing of Crypto Assets (February 2022). 6
Cong, Lin William, Xi Li, Ke Tang, and Yang Yang. 2021. “Crypto wash trading.”
arXiv preprint arXiv:2108.10984. 6
Deuskar, Prachi, Anurag Gupta, and Marti G Subrahmanyam. 2011. “Liquidity
effect in OTC options markets: Premium or discount?” Journal of Financial Markets,
14(1): 127–160. 6
Divakaruni, Anantha, Peter Zimmerman, et al. 2021. “Uncovering retail trading in
bitcoin: The impact of covid-19 stimulus checks.” Federal Reserve Bank of Cleveland. 5
20
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 21

Ferko, Alex, Amani Moin, Esen Onur, and Michael Penick. 2022. “Who trades
bitcoin futures and why?” Global Finance Journal, 100778. 5
Gandal, Neil, JT Hamrick, Tyler Moore, and Tali Oberman. 2018. “Price manipu-
lation in the Bitcoin ecosystem.” Journal of Monetary Economics, 95: 86–96. 6
Griffin, John M, and Amin Shams. 2020. “Is Bitcoin really untethered?” The Journal
of Finance, 75(4): 1913–1964. 6
Han, Jianlei, Shiyang Huang, and Zhuo Zhong. 2021. “Trust in DeFi: an empirical
study of the decentralized exchange.” Available at SSRN 3896461. 7
Hasbrouck, Joel, and Duane J Seppi. 2001. “Common factors in prices, order flows,
and liquidity.” Journal of financial Economics, 59(3): 383–411. 6
Hautsch, Nikolaus, Christoph Scheuch, and Stefan Voigt. 2018. “Building trust takes
time: Limits to arbitrage in blockchain-based markets.” arXiv preprint arXiv:1812.00595.
5
Lehar, Alfred, and Christine A Parlour. 2021. “Decentralized exchanges.” Working
paper. 7
Li, Jiasun, and Guanxi Yi. 2019. “Toward a factor structure in crypto asset returns.”
The Journal of Alternative Investments, 21(4): 56–66. 6
Li, Jiasun, and William Mann. 2018. “Digital tokens and platform building.” 6
Li, Jiasun, and William Mann. 2021. “Initial coin offerings: Current research and future
directions.” The Palgrave Handbook of Technological Finance, 369–393. 6
Li, Tao, Donghwa Shin, and Baolian Wang. 2021. “Cryptocurrency pump-and-dump
schemes.” Available at SSRN 3267041. 6
21
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 22

Liu, Yukun, Aleh Tsyvinski, and Xi Wu. 2022. “Common risk factors in cryptocur-
rency.” The Journal of Finance, 77(2): 1133–1177. 6
Makarov, Igor, and Antoinette Schoar. 2020. “Trading and arbitrage in cryptocurrency
markets.” Journal of Financial Economics, 135(2): 293–319. 5
Shams, Amin. 2020. “The structure of cryptocurrency returns.” Fisher College of business
working paper, , (2020-03): 011. 5
Yu, Yang (Gloria), and Jinyuan Zhang. 2022. “Flight to Bitcoin.” SSRN Electronic
Journal. 5
22
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 23

Figures
Figure 1: Time series of Bitcoin prices, volume, volatility, and options volume
This figure plots the time series of (a) daily Bitcoin prices (in US dollars), (b) daily Bitcoin trading
volume from CoinMarketCap (in billions of US dollars), (c) daily Bitcoin price volatility, estimated by
GARCH(1,1) over all available history from April 30th, 2013 to January 31st, 2022, and (d) daily Bitcoin
options trading volumes on LedgerX (in millions of US dollars). Our sample period is from February 1st,
2018 to January 31st, 2022.
23
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 24

Figure 2: Illiquidity Comparison: Bitcoin Options versus Spots
This figure chronicles the evolution of the daily relative spread for Bitcoin options over time (Panel A), as
well as similar measures for Bitcoin spot for comparison (Panel B). After smoothing, we find both series
to have similar trends across time (both tend to increase over time), indicating that illiquidity of options
contracts is highly correlated with that of the underlying assets (the correlation is 0.52). Relative spreads
of options are also much more volatile before a policy change (indicated by the green line) in August
2019 to be described in detail in Section 5. Similarly, we also compare the Amihud liquidity measures
for options (Panel C) and that for Bitcoin spot (Panel D). While Amihud measures for Bitcoin options
also tend to increase over time, those for Bitcoin spot tend to follow a U-shape. Relative spreads and
Amihud measures thus tend to capture different aspects of Bitcoin options and spot illiquidity.
24
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 25

Figure 3: Average daily delta-hedged options Returns
This figure presents the average daily delta-hedged options returns, separating between calls and puts as
well as at-the-money (ATM) and all options. For a specific option contract n and day t, its delta-hedged
return is defined as
˜Ro
t+1,n = Ro
t+1,n −RS
t+1St
∆t,n
ot,n
.
where ˜Ro
t+1,n denotes the daily delta-hedged options return, Ro
t+1,n denotes the (raw) daily options return,
RS
t+1 denotes the daily Bitcoin spot return, St denotes the spot market price of Bitcoin, Ot,n denotes the
options price, and ∆t,n denotes the options delta based on the Black Scholes formula.
25
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 26

Figure 4: Relative Spreads and Delta Hedged Returns, sorted according to moneyness
This figure illustrates the relative spreads and delta-hedged returns for options with different moneyness
levels.
We first sort options into three groups with high, median, and low levels of moneyness, and
presents the average relative spreads as well as next-day equal-weighted delta-hedge returns within each
group. Option moneyness is measured by LMR = ln ( S
K ) where S is the Bitcoin price and K option strike
price. For both calls and puts, out-of-the-money (in-the-money) options have the highest (lowest) relative
spreads as well as the highest (lowest) delta-hedged returns, consistent with findings in the literature on
stock options as well as interest rate caps and floors. Because of the relationship illustrated here, later
regressions control for options moneyness.
26
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 27

Figure 5: Trends of Imbalance over time
This figure illustrates the changes in imbalances before and after the policy shock in August 2019, which
allows retail investors to participate in the options market. We notice that the incoming retail investors
on average are options buyers, and their inflow brings the negative average net order imbalance before
the policy change toward a more balanced market.
27
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 28

Tables
Table 1: Descriptive statistics of options data
Time to maturity
Strike
Call vwap
Put vwap
(1)
(2)
(3)
(4)
Mean
98.52
40,371.41
5,766.29
4,456.60
SD
88.17
39,276.31
8,971.52
11,739.17
Min
10
2,000
0.25
0.22
50%
60
30,000
1,760
1,107.08
Max
359
400,000
63,548
171,000
Observations
31,334
31,334
21,287
10,047
This table presents descriptive statistics of our options data, including time to maturity, strike prices,
and volume-weighted average options prices for both calls and puts. All data are obtained from LedgerX
from Feb 1st, 2018 to Jan 31st, 2022.
28
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 29

Table 2A: Descriptive statistics on illiquidity measures: Relative Spreads
Call
Put
Bitcoin spot
OTM
ATM
ITM
ALL
OTM
ATM
ITM
ALL
(1)
(2)
(3)
(4)
(5)
(6)
(7)
(8)
(9)
Mean
0.999
0.529
0.316
0.749
1.078
0.609
0.36
0.834
0.009
Volume-weighted
0.938
0.53
0.349
0.808
0.95
0.443
0.227
0.733
SD
0.542
0.377
0.264
0.549
0.53
0.435
0.383
0.563
0.008
Min
0.002
0.001
0.007
0.001
0.002
0.005
0.008
0.002
-0.008
25th Q
0.536
0.25
0.129
0.291
0.644
0.277
0.12
0.346
0.003
Median
0.941
0.421
0.237
0.59
1.064
0.479
0.216
0.714
0.006
75th Q
1.46
0.683
0.434
1.138
1.528
0.802
0.468
1.269
0.011
Max
2
1.998
2
2
1.999
2
2
2
0.048
Table 2B: Descriptive statistics on illiquidity measures: Amihud
Call
Put
Bitcoin spot
OTM
ATM
ITM
ALL
OTM
ATM
ITM
ALL
(1)
(2)
(3)
(4)
(5)
(6)
(7)
(8)
(9)
Mean
1.74
1.42
1.65
1.66
4.15
2.36
2.03
3.31
2.03
Volume-weighted
0.05
0.04
0.09
0.04
0.10
0.07
0.09
0.09
SD
8.49
5.83
3.57
7.14
14.36
6.79
4.18
11.52
2.33
Min
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
25th Q
0.02
0.02
0.06
0.02
0.05
0.05
0.07
0.05
0.42
Median
0.08
0.10
0.34
0.12
0.29
0.25
0.48
0.30
1.08
75th Q
0.43
0.55
1.60
0.66
1.70
1.29
1.97
1.58
2.84
Max
150.74
150.74
82.76
150.74
150.74
107.92
39.68
150.74
13.6
This table presents the relative spreads of Bitcoin options, separating between calls and puts as well
as moneyness (OTM, ATM, ITM, and all). For comparison, we also present summary statistics for the
relative spreads in the Bitcoin spot market. For a given contract n and day t, its relative spread RSnt is
defined as
RSnt =
last asknt −last bidnt
(last asknt + last bidnt)/2
that is, RS is defined as the ratio between the quoted spread and the mid-quote. A salient feature of the
bitcoin options market is its illiquidity. Average relative spread can be as high as 74.9% for calls and
83.4% for puts. In comparison, relative spreads for stock options are typically 7% for calls and 8% for
puts according to Christoffersen, Goyenko, Jacobs and Karoui (2018). Such high relative spreads are not
attributed to infrequently traded outliers, as the volume-weighted average presents similar magnitudes as
the equally weighted means. Panel B repeats the exercise in Panel A but for Amihud measures instead
of relative spreads. The Amihud measures for options are the ratios between absolute daily returns and
volumes, while the ones for Bitcoin spots are scaled up by 108 for easy comparison.
29
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 30

Table 3: Descriptive statistics of Delta Hedged Returns
A. Daily delta-hedged returns
B. Daily delta-hedged returns
C. Daily Bitcoin returns
call
put
OTM
ATM
ITM
ALL
OTM
ATM
ITM
ALL
(1)
(2)
(3)
(4)
(5)
(6)
(7)
(8)
(9)
Average
0.017
0.012
-0.001
0.012
0.036
0.027
0.006
0.029
Average
0.002
SD
0.327
0.254
0.105
0.277
0.345
0.275
0.104
0.301
SD
0.042
Skewness
1.801
1.948
0.912
2.051
1.803
1.947
0.413
2.003
Skewness
-0.534
Kurtosis
6.343
9.893
5.187
9.389
5.77
8.363
5.283
7.949
Kurtosis
11.012
ρ(1)
-0.307
-0.297
-0.284
-0.276
-0.268
-0.346
-0.281
-0.304
ρ(1)
-0.061
Avg #series
9.21
3.48
6.07
15.21
5.35
2.79
2.54
8.18
This table presents descriptive statistics of the daily delta-hedged returns for our options data, separating
between calls and puts as well moneyness (OTM, ATM, ITM, and all). Delta-hedged return is defined as
˜Ro
t+1,n = Ro
t+1,n −RS
t+1St
∆t,n
ot,n
where ˜Ro
t+1,n denotes the daily delta-hedged options return, Ro
t+1,n denotes the (raw) daily options return,
RS
t+1 denotes the daily Bitcoin spot return, St denotes the spot market price of Bitcoin, Ot,n denotes
the options price, and ∆t,n denotes the options delta based on the Black Scholes formula. Avg # series
denotes the average numbers of options contracts within each group on each day. For comparison, we also
present summary statistics for daily Bitcoin returns. ρ(1) denotes the autocorrelation between bitcoin
spot returns.
30
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 31

Table 4: Average Portfolio returns Sorted on Options Illiquidity
Panel A: Equal-weighted portfolios sorted on option RS
Call options returns on t+2
Put options returns on t+2
1
2
3
3-1
Observations
1
2
3
3-1
Observations
Mean
0
0.009
0.019
0.019
7095
0.011
0.022
0.053
0.043
3349
t-stat
0.033
2.99
4.429
3.61***
2.426
4.214
7.777
4.84***
Call options returns on t+1
Put options returns on t+1
1
2
3
3-1
Observations
1
2
3
3-1
Observations
Mean
-0.005
0.012
0.023
0.027
7095
0.003
0.032
0.052
0.049
3349
t-stat
-2.114
3.864
5.194
5.62***
0.768
6.032
7.738
5.98***
Panel B: Volume-weighted portfolios sorted on option RS
Call options returns on t+2
Put options returns on t+2
1
2
3
3-1
Observations
1
2
3
3-1
Observations
Mean
0.008
0.028
0.02
0.011
7095
-0.02
0.047
0.031
0.05
3349
t-stat
0.635
1.856
1.329
0.567
-0.763
1.719
2.174
1.724**
Call options returns on t+1
Put options returns on t+1
1
2
3
3-1
Observations
1
2
3
3-1
Observations
Mean
-0.010
0.012
0.033
0.043
7095
0.011
0.033
0.07
0.059
3349
t-stat
-0.778
0.879
2.338
2.235**
0.603
1.845
2.321
1.645**
This table sorts options into three groups with high, median, and low levels of relative spreads, and
presents the average next-day (both equal-weighted and value weighted) delta-hedge returns within each
group, as well as the return spread between the high and low groups. For both calls and puts and across
all windows, higher illiquidity is followed by significantly higher delta-hedged returns.
31
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 32

Panel C: Equal-weighted portfolios sorted on option Amihud
Call options returns on t+2
Put options returns on t+2
1
2
3
3-1
Observations
1
2
3
3-1
Observations
Mean
0.004
0.007
0.018
0.014
7095
0.025
0.023
0.037
0.012
3349
t-stat
1.123
1.979
5.096
2.98***
4.349
4.347
6.5
1.45*
Call options returns on t+1
Put options returns on t+1
1
2
3
3-1
Observations
1
2
3
3-1
Observations
Mean
0
0.011
0.018
0.018
7095
0.012
0.036
0.037
0.025
3349
t-stat
-0.015
3.219
5.023
3.82***
2.229
6.696
6.477
3.18***
Panel D: Volume-weighted portfolios sorted on option Amihud
Call options returns on t+2
Put options returns on t+2
1
2
3
3-1
Observations
1
2
3
3-1
Observations
Mean
0.016
0.035
0.058
0.042
7095
0.009
0.043
0.037
0.028
3349
t-stat
1.538
3.397
4.259
2.433***
0.503
2.932
2.206
1.15
Call options returns on t+1
Put options returns on t+1
1
2
3
3-1
Observations
1
2
3
3-1
Observations
Mean
0.010
0.029
0.024
0.014
7095
0.026
0.067
0.051
0.024
3349
t-stat
1.019
3.01
2.047
0.907
1.793
3.932
2.733
0.999
32
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 33

Table 5: Options Liquidity and Returns
Panel A: All Options
DEPENDENT VARIABLE
Delta-Hedged Return
(1)
(2)
(3)
(4)
(5)
(6)
RSlag
0.027***
0.031***
0.022***
0.026***
(8.02)
(6.91)
(6.76)
(5.98)
RSlag×imbalance
-0.042***
-0.039***
-0.024***
-0.030***
(-12.11)
(-7.64)
(-8.40)
(-6.83)
Amihud
0.008***
0.007***
0.007***
0.007***
(12.15)
(10.2)
(9.89)
(9.93)
Amihud×imbalance
-0.008***
-0.007***
-0.007***
-0.007***
(-9.26)
(-7.49)
(-7.62)
(-7.32)
abs delta
0.011*
-0.015***
0.013**
(1.88)
(-3.68)
(2.27)
beta
-0.061***
-0.060***
-0.061***
(-6.53)
(-6.77)
(-6.77)
ln ret
0.704***
0.688***
0.687***
(7.66)
(7.57)
(7.56)
lntime
0.003*
0.002
0.004**
(1.90)
(1.05)
(2.23)
imbalances
-0.005
-0.017***
0.005
(-1.58)
(-6.85)
(1.24)
RS Bitcoin Spot
0.017
-0.047
-0.044
(0.09)
(-0.26)
(-0.23)
Amihud Bitcoin Spot
0.002**
0.002**
0.002**
(2.24)
(1.99)
(1.99)
vol
-0.003
0.005
-0.003
(-0.41)
(0.68)
(-0.40)
Constant
-0.009***
0.014
0.001
0.037***
-0.017***
0.004
(-3.54)
(0.99)
(0.73)
(2.87)
(-7.11)
(0.3)
Year fixed effect?
Y
Y
Y
Y
Y
Y
Observations
26,593
26,290
30,232
26,604
26,593
26,290
Adjusted R-squared
0.018
0.03
0.044
0.055
0.048
0.06
This table presents results from the following regression:
DHRt+1 = α0 + α1Illiquidityt + α2Illiquidityt × imbalancet + Controls + ϵ,
where DHR is delta hedged return over day t + 1, illiquidity is measured by lagged relative spreads or
Amihud measures of Bitcoin options. Controls include the absolute value of option delta to account
for moneyness (abs delta), bitcoin spot beta estimated from 365-day rolling window, daily spot return
(ln ret), option maturity in terms of ln(days to expiration) (lntime), option order imbalances, spot illiq-
uidity also measured by relative spreads and Amihud liquidity measures (scaled up by 108), and spot
volatility (vol). Robust t-statistics are in parentheses with standard errors clustered at the contract level.
Stars denotes p-statistics < 0.01, < 0.05, and < 0.1, respectively.
33
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 34

Panel B: Call Options
DEPENDENT VARIABLE
Delta-Hedged Return
(1)
(2)
(3)
(4)
(5)
(6)
RSlag
0.022***
0.019***
0.019***
0.015***
(5.23)
(3.30)
(4.79)
(2.70)
RSlag×imbalance
-0.039***
-0.036***
-0.028***
-0.032***
(-9.65)
(-5.93)
(-7.88)
(-5.74)
Amihud
0.008***
0.007***
0.007***
0.007***
(8.73)
(7.68)
(6.92)
(7.42)
Amihud×imbalance
-0.007***
-0.005***
-0.006***
-0.005***
(-6.33)
(-4.51)
(-5.03)
(-4.41)
abs delta
0.006
-0.013***
0.003
(0.84)
(-2.65)
(0.44)
beta
-0.053***
-0.056***
-0.054***
(-4.93)
(-5.58)
(-5.33)
ln ret
1.729***
1.726***
1.718***
(18.92)
(19.05)
(18.84)
Intime
0.005**
0.003*
0.005**
(2.21)
(1.68)
(2.51)
imbalances
-0.016***
-0.031***
-0.009**
(-4.04)
(-10.79)
(-2.01)
RS Bitcoin Spot
-0.350*
-0.396**
-0.368*
(-1.69)
(-1.98)
(-1.80)
Amihud Bitcoin Spot
0.002*
0.002*
0.002*
(1.82)
(1.83)
(1.75)
vol
-0.003
0.002
-0.005
(-0.36)
(0.19)
(-0.55)
Constrant
-0.009***
0.014
-0.001
0.032**
-0.016***
0.010
(-3.22)
(0.83)
(-0.46)
(2.13)
(-5.74)
(0.60)
Year fixed effect?
Y
Y
Y
Y
Y
Y
Observations
18,502
18,292
20,683
18,494
18,502
18,292
Adjusted R-squared
0.016
0.076
0.031
0.089
0.033
0.093
34
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 35

Panel C: Put Options
DEPENDENT VARIABLE
Delta-Hedged Return
(1)
(2)
(3)
(4)
(5)
(6)
RSlag
0.036***
0.033***
0.028***
0.025***
(6.18)
(4.44)
(4.91)
(3.34)
Rslag
-0.046***
-0.040***
-0.018***
-0.025***
imbalance
(-7.52)
(-4.30)
(-3.61)
(-3.10)
Amihud
0.007***
0.007***
0.007***
0.007***
(8.17)
(7.30)
(6.87)
(7.14)
Amihud×imbalance
-0.009***
-0.008***
-0.008***
-0.007***
(-6.99)
(-5.77)
(-5.94)
(-5.64)
abs delta
-0.002
-0.027***
0.004
(-0.19)
(-2.95)
(0.32)
beta
-0.082***
-0.076***
-0.081***
(-4.21)
(-3.98)
(-4.15)
ln ret
-1.440***
-1.433***
-1.405***
(-12.78)
(-12.87)
(-12.63)
lntime
-0.004
-0.009***
-0.006*
(-1.26)
(-2.63)
(-1.85)
imbalances
-0.016**
-0.022***
-0.003
(-2.56)
(-4.81)
(-0.39)
RS Bitcoin Spot
1.050***
0.897**
0.901**
(2.77)
(2.46)
(2.45)
Amihud Bitcoin Spot
0.006***
0.006***
0.006***
(3.40)
(3.27)
(3.28)
vol
0.009
0.018
0.015
(0.65)
(1.41)
(1.19)
Constant
-0.006
0.048*
0.005**
0.071**
-0.019***
0.04
(-1.22)
(1.67)
(2.04)
(2.58)
(-4.09)
(1.38)
Year fixed effect?
Y
Y
Y
Y
Y
Y
Observations
8,091
7,998
9,549
8,110
8,091
7,998
Adjusted R-squared
0.023
0.061
0.066
0.107
0.074
0.111
35
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 36

Table 6: Statistical Description of Imbalance
Imbalance
Mean
Std
Min
Median
Max
#Observations
(1)
(2)
(3)
(4)
(5)
(6)
All
-0.04
0.797
-1
-0.028
1
27500
Before
-0.208
0.909
-1
-1
1
1470
After
-0.03
0.789
-1
0
1
26030
After-Before
0.178***
This table presents summary statistics of the options trading imbalance before and after a policy shock
that significantly increases retail participation. For options contract on day, imbalance is defined as
Imbalancent = #buynt −#sellnt
#buynt + #sellnt
,
where “buy” and “sell” are the number of contracts initiated by buyers and sellers on day . The policy
change allows more retail investor participation, and lead to significantly higher imbalance, as the last
line (After-Before) indicates.
36
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 37

Table 7: Options Liquidity and Returns before and after the policy shock
Panel A: All Options
Before
After
DEPENDENT VARIABLE
Delta-Hedged Return
Delta-Hedged Return
(1)
(2)
(3)
(4)
(5)
(6)
(7)
(8)
(9)
(10)
(11)
(12)
RSlag
0.073***
0.098***
0.055**
0.082***
0.026***
0.030***
0.021***
0.025***
(2.95)
(2.95)
(2.47)
(2.71)
(7.67)
(6.67)
(6.38)
(5.73)
Rslag×imbalance
0.000
-0.033*
-0.005
-0.037*
-0.043***
-0.037***
-0.025***
-0.029***
0.00
(-1.66)
(-0.39)
(-1.84)
(-12.17)
(-7.07)
(-8.50)
(-6.32)
Amihud
0.546***
0.655***
0.648***
0.647***
0.008***
0.007***
0.007***
0.007***
(5.03)
(5.75)
(5.67)
(5.53)
(12.12)
(10.21)
(9.88)
(9.94)
Amihud×imbalance
0.077
0.036
0.104
0.05
-0.008***
-0.007***
-0.007***
-0.007***
(0.71)
(0.34)
(0.97)
(0.44)
(-9.26)
(-7.29)
(-7.56)
(-7.17)
abs delta
0.081*
-0.004
0.088**
0.01
-0.015***
0.012**
(1.78)
(-0.15)
(2.09)
(1.58)
(-3.69)
(2.00)
beta
-0.03
-0.009
-0.003
-0.066***
-0.065***
-0.066***
(-0.74)
(-0.23)
(-0.09)
(-6.85)
(-7.08)
(-7.10)
ln ret
0.915***
0.869***
0.900***
0.697***
0.683***
0.679***
(3.55)
(3.48)
(3.69)
(7.18)
(7.12)
(7.09)
lntime
0.001
0.011
0.012*
0.003*
0.002
0.004**
(0.11)
(1.56)
(1.77)
(1.82)
(1.01)
(2.16)
imbalances
0.019
0.009
0.021*
-0.009***
-0.019***
0.002
(1.51)
(1.10)
(1.68)
(-2.62)
(-7.44)
(0.49)
RS Bitcoin Spot
0.943
1.003
0.898
0.052
-0.02
-0.01
(0.93)
(1.00)
(0.89)
(0.27)
(-0.11)
(-0.05)
Amihud Bitcoin Spot
0.009***
0.006*
0.007**
0.001
0.001
0.001
(2.61)
(1.92)
(2.21)
(1.33)
(1.11)
(1.09)
vol
0.063*
0.009
0
-0.017**
-0.008
-0.016**
(1.75)
(0.26)
(0.01)
(-2.32)
(-1.22)
(-2.29)
Constant
-0.018
-0.125**
-0.016***
-0.085**
-0.049***
-0.162***
-0.008***
0.032**
0
0.053***
-0.017***
0.021
(-1.41)
(-2.33)
(-2.60)
(-2.11)
(-3.93)
(-3.27)
(-3.37)
(2.15)
(-0.00)
(3.86)
(-7.09)
(1.46)
Year fixed effect?
Y
Y
Y
Y
Y
Y
Y
Y
Y
Y
Y
Y
Observations
1,268
1,268
1,917
1,311
1,268
1,268
25,325
25,022
28,315
25,293
25,325
25,022
Adjusted R-squared
0.009
0.037
0.063
0.103
0.091
0.116
0.019
0.032
0.047
0.058
0.05
0.062
This table reevaluates our Hypothesis 1 and 2 for the sample before and after the policy change using
the same regression as in Table 5. Robust t-statistics are in parentheses with standard errors clustered
at the contract level. Stars denotes p-statistics < 0.01, < 0.05, and < 0.1, respectively.
37
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 38

Panel B: Call Options
Before
After
DEPENDENT VARIABLE
Delta-Hedged Return
Delta-Hedged Return
(1)
(2)
(3)
(4)
(5)
(6)
(7)
(8)
(9)
(10)
(11)
(12)
RSlag
0.064**
0.066*
0.053**
0.057
0.021***
0.018***
0.018***
0.014***
(2.31)
(1.69)
(2.08)
(1.60)
(4.94)
(3.20)
(4.49)
(2.60)
Rslag×imbalance
-0.008
-0.03
-0.007
-0.038*
-0.041***
-0.035***
-0.029***
-0.031***
(-0.52)
(-1.31)
(-0.47)
(-1.72)
(-9.65)
(-5.53)
(-7.95)
(-5.37)
Amihud
0.553***
0.639***
0.661***
0.644***
0.008***
0.007***
0.007***
0.007***
(4.43)
(4.68)
(4.81)
(4.64)
(8.70)
(7.69)
(6.90)
(7.43)
Amihud×imbalance
0.02
(0.03)
0.05
(0.02)
-0.007***
-0.005***
-0.006***
-0.005***
(0.12)
(-0.21)
(0.38)
(-0.16)
(-6.32)
(-4.35)
(-4.97)
(-4.29)
abs delta
0.021
-0.026
0.038
0.005
-0.013***
0.002
(0.36)
(-0.85)
(0.71)
(0.73)
(-2.59)
(0.34)
beta
0.026
0.031
0.041
-0.060***
-0.063***
-0.061***
(0.53)
(0.63)
(0.81)
(-5.45)
(-6.14)
(-5.90)
ln ret
1.823***
1.782***
1.753***
1.726***
1.723***
1.715***
(6.57)
(6.79)
(6.71)
(17.97)
(18.06)
(17.88)
lntime
0.005
0.015*
0.016**
0.004**
0.003
0.005**
(0.55)
(1.92)
(2.02)
(1.98)
(1.46)
(2.30)
imbalances
0.003
-0.001
0.013
-0.020***
-0.034***
-0.012**
(0.19)
(-0.10)
(0.91)
(-4.62)
(-10.96)
(-2.44)
RS Bitcoin Spot
1.424
1.556
1.405
-0.344
-0.397*
-0.359*
(1.40)
(1.58)
(1.39)
(-1.63)
(-1.95)
(-1.73)
Amihud Bitcoin Spot
0.008**
0.005*
0.006*
0.001
0.001
0.001
(2.37)
(1.70)
(1.90)
(1.04)
(1.05)
(0.95)
vol
0.069
0.017
0.006
-0.018**
-0.014
-0.020**
(1.59)
(0.42)
(0.14)
(-2.20)
(-1.64)
(-2.41)
Constant
-0.017
-0.139**
-0.020***
-0.124**
-0.052***
-0.179***
-0.009***
0.036**
-0.002
0.053***
-0.017***
0.031*
(-1.10)
(-2.08)
(-2.65)
(-2.55)
(-3.40)
(-2.86)
(-3.14)
(2.01)
(-0.98)
(3.36)
(-5.77)
(1.81)
Year fixed effect?
Y
Y
Y
Y
Y
Y
Y
Y
Y
Y
Y
Y
Observations
1268
1268
1917
1311
1268
1268
25325
25022
28315
25293
25325
25022
Adjusted R-squared
0.009
0.037
0.063
0.103
0.091
0.116
0.019
0.032
0.047
0.058
0.05
0.062
38
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 39

Panel C: Put options
Before
After
DEPENDENT VARIABLE
Delta-Hedged Return
Delta-Hedged Return
(1)
(2)
(3)
(4)
(5)
(6)
(7)
(8)
(9)
(10)
(11)
(12)
RSlag
0.114*
0.106*
0.079
0.096*
0.035***
0.032***
0.027***
0.023***
(1.88)
(1.73)
(1.50)
(1.68)
(5.97)
(4.29)
(4.67)
(3.17)
Rslag imbalance
0.024
-0.023
-0.009
-0.028
-0.047***
-0.038***
-0.019***
-0.023***
(0.71)
(-0.49)
(-0.28)
(-0.57)
(-7.59)
(-3.96)
(-3.68)
(-2.84)
Amihud
0.509**
0.577***
0.577***
0.544***
0.007***
0.007***
0.007***
0.007***
(2.47)
(3.07)
(3.18)
(2.88)
(8.15)
(7.31)
(6.87)
(7.16)
amihud imbalance
0.238
0.340**
0.275*
0.370**
-0.009***
-0.008***
-0.008***
-0.007***
(1.57)
(2.31)
(1.72)
(2.34)
(-7.00)
(-5.66)
(-5.91)
(-5.57)
abs delta
0.063
-0.065
0.079
-0.004
-0.026***
0.003
(0.80)
(-0.79)
(0.97)
(-0.32)
(-2.88)
(0.25)
beta
-0.173**
-0.137**
-0.140**
-0.081***
-0.076***
-0.081***
(-2.63)
(-2.17)
(-2.26)
(-3.96)
(-3.75)
(-3.92)
ln ret
-0.993***
-1.346***
-1.115***
-1.454***
-1.438***
-1.419***
(-3.00)
(-4.13)
(-3.24)
(-12.20)
(-12.23)
(-12.08)
lntime
0.003
0.01
0.018
-0.004
-0.009***
-0.007*
(0.19)
(0.54)
(1.06)
(-1.30)
(-2.65)
(-1.88)
imbalances
0.019
-0.014
-0.008
-0.020***
-0.023***
-0.005
(0.76)
(-0.89)
(-0.34)
(-3.14)
(-5.05)
(-0.73)
RS Bitcoin Spot
-2.724
-3.587
-3.068
1.126***
0.976***
0.969***
(-1.21)
(-1.61)
(-1.42)
(2.93)
(2.64)
(2.60)
Amihud Bitcoin Spot
0.008
0.005
0.005
0.006***
0.005***
0.006***
(1.05)
(0.70)
(0.82)
(3.23)
(3.10)
(3.14)
vol
0.04
-0.02
-0.015
0.004
0.014
0.011
(0.57)
(-0.32)
(-0.24)
(0.29)
(1.11)
(0.86)
Constant
-0.026
-0.018
-0.005
0.046
-0.048**
-0.075
-0.005
0.054*
0.004
0.075**
-0.019***
0.044
(-1.11)
(-0.18)
(-0.50)
(0.48)
(-2.07)
(-0.82)
(-1.07)
(1.77)
(1.52)
(2.56)
(-4.00)
(1.45)
Year fixed effect?
Y
Y
Y
Y
Y
Y
Y
Y
Y
Y
Y
Y
Observations
344
344
564
354
344
344
7,747
7,654
8,985
7,756
7,747
7,654
Adjusted R-squared
0.012
0.048
0.056
0.119
0.087
0.121
0.024
0.062
0.069
0.11
0.077
0.113
39
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 40

Appendix
A
Robustness to Bull/Bear Markets
This appendix provides additional results showing that our main findings in Table 5 is robust
in both the bull and bear markets. Figure A1 illustrates the bull versus bear market classifi-
cation. Specifically, following the conventional wisdom in the cryptocurrency community, we
regard the period from May 2020 to November 2021 to be in a bull market, and the period
from January 2018 to April 2020 and December 2021 up to now (November 2022) to be in
a bear market.
Figure A1: Defining Bull and Bear Markets
This figure illustrates the bull and bear markets, where the former includes the period from
May 2020 to November 2021, and the latter includes the period from January 2018 to April
2020 and December 2021 up to now (November 2022).
Table A1 then shows the robustness of the main findings in Table 5 across both bull and
bear markets by adding a bull-bear market dummy. As Table A1 illustrates, across both
bull and bear markets, coefficients on illiquidity are significantly positive, and those on the
interaction between illiquidity and imbalance are significantly negative.
40
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 41

Table A1: Options Liquidity and Returns
Panel A: All Options
DEPENDENT VARIABLE
Delta-Hedged Return
(1)
(2)
(3)
(4)
(5)
(6)
RSlag
0.022***
0.039***
0.021***
0.036***
(4.35)
(6.71)
(4.20)
(6.29)
RSlag×imbalance
-0.035***
-0.030***
-0.026***
-0.032***
(-3.43)
(-2.67)
(-2.59)
(-2.82)
RSlag×imbalance×dummyBull
-0.011
-0.010
-0.001
0.001
(-0.99)
(-0.91)
(-0.12)
(0.13)
Amihud
0.008***
0.007***
0.007***
0.007***
(11.01)
(9.52)
(9.21)
(9.20)
Amihud×imbalance
-0.006*
-0.005
-0.005
-0.005
(-1.77)
(-1.59)
(-1.61)
(-1.58)
Amihud×imbalance×dummyBull
-0.002
-0.002
-0.001
-0.001
(-0.75)
(-0.54)
(-0.41)
(-0.39)
abs delta
0.112***
0.071***
0.107***
(7.96)
(5.77)
(7.61)
beta
-0.021
-0.020
-0.023
(-1.10)
(-1.12)
(-1.31)
ln ret
0.724***
0.720***
0.710***
(7.40)
(7.46)
(7.36)
lntime
0.007
-0.002
0.006
(1.60)
(-0.59)
(1.35)
imbalances
-0.009**
-0.020***
0.001
(-2.57)
(-7.79)
(0.17)
RS Bitcoin Spot
0.093
0.070
0.072
(0.47)
(0.37)
(0.37)
Amihud Bitcoin Spot
0.041
-0.419
0.540
(0.03)
(-0.29)
(0.37)
vol
-0.039***
-0.026**
-0.035***
(-3.67)
(-2.44)
(-3.36)
dummy Bull
-0.026***
-0.022*
(-2.74)
(-1.86)
Constant
-0.001
-0.041
0.025***
0.040
-0.013***
-0.049*
(-0.19)
(-1.57)
(3.29)
(1.55)
(-3.32)
(-1.89)
Year fixed effect?
Y
Y
Y
Y
Y
Y
Observations
23,776
23,608
27,122
23,902
23,776
23,608
Adjusted R-squared
0.019
0.032
0.042
0.054
0.048
0.060
This table shows the robustness of the main findings in Table 5 across both bull and bear markets. We
conduct a similar analysis as in Table 5, but with additional controls for a bull-bear market dummy.
A bull market refers to the period from May 2020 to November 2021, while a bear market refer to
periods including January 2018 to April 2020 and December 2021 up to now (November 2022). Robust t-
statistics are in parentheses with standard errors clustered at the contract level. Stars denotes p-statistics
< 0.01, < 0.05, and < 0.1, respectively.
41
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 42

Panel B: Call Options
DEPENDENT VARIABLE
Delta-Hedged Return
(1)
(2)
(3)
(4)
(5)
(6)
RSlag
0.015**
0.022***
0.014**
0.020***
(2.34)
(3.08)
(2.21)
(2.84)
RSlag×imbalance
-0.042***
-0.038***
-0.031***
-0.034***
(-3.63)
(-2.85)
(-2.68)
(-2.60)
RSlag×imbalance×dummyBull
0.000
-0.001
0.001
0.000
(0.03)
(-0.05)
(0.06)
(0.03)
Amihud
0.008***
0.007***
0.007***
0.007***
(8.34)
(7.07)
(6.62)
(6.91)
Amihud×imbalance
-0.008**
-0.007*
-0.007*
-0.007
(-2.21)
(-1.70)
(-1.75)
(-1.62)
Amihud×imbalance×dummyBull
0.002
0.002
0.002
0.002
(0.43)
(0.46)
(0.41)
(0.45)
abs delta
0.077***
0.057***
0.073***
(4.55)
(3.84)
(4.37)
beta
-0.006
-0.007
-0.012
(-0.27)
(-0.29)
(-0.55)
ln ret
1.772***
1.771***
1.757***
(18.42)
(18.60)
(18.33)
lntime
0.010**
0.004
0.009*
(2.06)
(0.73)
(1.74)
imbalances
-0.018***
-0.034***
-0.011**
(-4.01)
(-11.00)
(-2.23)
RS Bitcoin Spot
-0.256
-0.285
-0.250
(-1.19)
(-1.36)
(-1.18)
Amihud Bitcoin Spot
1.474
0.937
1.794
(0.87)
(0.58)
(1.11)
vol
-0.030**
-0.024**
-0.030***
(-2.58)
(-2.05)
(-2.61)
dummy Bull
-0.031***
-0.019
(-2.98)
(-1.42)
Constant
0.000
-0.060*
0.027***
-0.001
-0.009*
-0.057*
(0.02)
(-1.86)
(3.26)
(-0.04)
(-1.84)
(-1.78)
Year fixed effect?
Y
Y
Y
Y
Y
Y
Observations
16,435
16,324
18,423
16,510
16,435
16,324
Adjusted R-squared
0.017
0.079
0.034
0.091
0.035
0.096
42
Electronic copy available at: https://ssrn.com/abstract=4280098


## Page 43

Panel C: Put Options
DEPENDENT VARIABLE
Delta-Hedged Return
(1)
(2)
(3)
(4)
(5)
(6)
RSlag
0.031***
0.036***
0.030***
0.031***
(3.92)
(3.96)
(3.79)
(3.51)
RSlag×imbalance
-0.009
0.013
-0.006
-0.000
(-0.39)
(0.57)
(-0.28)
(-0.01)
RSlag×imbalance×dummyBull
-0.043*
-0.051**
-0.017
-0.021
(-1.84)
(-2.26)
(-0.76)
(-1.00)
Amihud
0.007***
0.007***
0.007***
0.007***
(7.38)
(6.85)
(6.49)
(6.66)
Amihud×imbalance
0.003
0.003
0.000
0.001
(0.55)
(0.60)
(0.09)
(0.32)
Amihud×imbalance×dummyBull
-0.012**
-0.011**
-0.008*
-0.009*
(-2.41)
(-2.34)
(-1.72)
(-1.92)
abs delta
0.138***
0.093***
0.132***
(5.28)
(3.46)
(4.97)
beta
-0.099***
-0.096***
-0.099***
(-2.90)
(-2.83)
(-3.03)
ln ret
-1.428***
-1.421***
-1.395***
(-11.93)
(-12.05)
(-11.82)
lntime
-0.017*
-0.024***
-0.018**
(-1.90)
(-2.88)
(-2.12)
imbalances
-0.026***
-0.026***
-0.013*
(-4.24)
(-5.56)
(-1.95)
RS Bitcoin Spot
1.178***
1.069***
1.061***
(3.16)
(2.94)
(2.88)
Amihud Bitcoin Spot
2.218
2.860
3.613
(0.71)
(0.90)
(1.14)
vol
-0.050**
-0.039*
-0.043**
(-2.33)
(-1.80)
(-2.04)
dummy Bull
-0.005
-0.012
(-0.28)
(-0.67)
Constant
0.001
0.115**
0.011
0.160***
-0.019***
0.089*
(0.09)
(2.16)
(0.84)
(3.03)
(-2.70)
(1.79)
Year fixed effect?
Y
Y
Y
Y
Y
Y
Observations
7,341
7,284
8,699
7,392
7,341
7,284
Adjusted R-squared
0.022
0.065
0.059
0.107
0.072
0.111
43
Electronic copy available at: https://ssrn.com/abstract=4280098


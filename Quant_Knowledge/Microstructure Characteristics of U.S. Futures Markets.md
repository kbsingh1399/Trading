Florida International University
FIU Digital Commons
FIU Electronic Theses and Dissertations University Graduate School
6-25-2014
Microstructure Characteristics of U.S. Futures
Markets
Ahmet Senol Oztekin
aozte001@fiu.edu
DOI:10.25148/etd.FI14071191
Follow this and additional works at:http://digitalcommons.fiu.edu/etd
Recommended Citation
Oztekin, Ahmet Senol, "Microstructure Characteristics of U.S. Futures Markets" (2014).FIU Electronic Theses and Dissertations. 1559.
http://digitalcommons.fiu.edu/etd/1559
This work is brought to you for free and open access by the University Graduate School at FIU Digital Commons. It has been accepted for inclusion in
FIU Electronic Theses and Dissertations by an authorized administrator of FIU Digital Commons. For more information, please contactdcc@fiu.edu.

FLORIDA INTERNATIONAL UNIVERSITY
Miami, Florida
MICROSTRUCTURE CHARATERISTICS OF U.S. FUTURES MARKETS
A dissertation submitted in partial fulfillment of the
requirements for the degree of
DOCTOR OF PHILOSOPHY
In
BUSINESS ADMINISTRATION
by
Ahmet Senol Oztekin
2014

To: Dean David R. Klock
College of Business Administration
This dissertation, written by Ahmet Senol Oztekin, and entitled Microstructure
Characteristics of U.S. Futures Markets, having been approved in respect to style and
intellectual content, is referred to you for judgment.
We have read this dissertation and recommend that it be approved.
_______________________________________
Abhijit Barua
_______________________________________
Brice Dupoyet
_______________________________________
Robert Daigler, Co-Major Professor
_______________________________________
Suchismita Mishra, Co-Major Professor
Date of Defense: June 25, 2014
The dissertation of Ahmet Senol Oztekin is approved.
_______________________________________
Dean David R. Klock
College of Business Administration
_______________________________________
Dean Lakshmi N. Reddi
University Graduate School
Florida International University, 2014
ii

© Copyright 2014 by Ahmet Senol Oztekin
All rights reserved.
iii

ACKNOWLEDGMENTS
I graciously acknowledge the support and mentorship provided by the Department of
Finance at Florida International University through its professors and administrative staff.
I would like to thank my committee members for their support in the writing of this
dissertation. I would also like to thank Dr. Prakash for providing me with the opportunity
to obtain this degree. I owe my deepest gratitude to my major professors Dr.Daigler and
Dr.Mishra. Without their support, patience and guidance this study would not have been
completed.
iv

ABSTRACT OF THE DISSERTATION
MICROSTRUCTURE CHARACTERISTICS OF U.S. ELECTRONIC FUTURES
MARKETS
by
Ahmet Senol Oztekin
Florida International University, 2014
Miami, Florida
Professor Robert Daigler, Co-Major Professor
Professor Suchismita Mishra, Co-Major Professor
Prior finance literature lacks a comprehensive analysis of microstructure
characteristics of U.S. futures markets due to the lack of data availability. Utilizing a
unique data set for five different futures contract this dissertation fills this gap in the
finance literature. In three essays price discovery, resiliency and the components of bid-
ask spreads in electronic futures markets are examined. In order to provide
comprehensive and robust analysis, both moderately volatile pre-crisis and volatile crisis
periods are included in the analysis.
The first essay entitled “Price Discovery and Liquidity Characteristics for U.S.
Electronic Futures and ETF Markets” explores the price discovery process in U.S. futures
and ETF markets. Hasbrouck’s information share method is applied to futures and ETF
instruments. The information share results show that futures markets dominate the price
discovery process. The results on the factors that affect the price discovery process show
that when volatility increases, the price leadership of futures markets declines.
v

Furthermore, when the relative size of bid-ask spread in one market increases, its
information share decreases.
The second essay, entitled “The Resiliency of Large Trades for U.S. Electronic
Futures Markets,“ examines the effects of large trades in futures markets. How quickly
prices and liquidity recovers after large trades is an important characteristic of financial
markets. The price effects of large trades are greater during the crisis period compared to
the pre-crisis period. Furthermore, relative to the pre-crisis period, during the crisis
period it takes more trades until liquidity returns to the pre-block trade levels.
The third essay, entitled “Components of Quoted Bid-Ask Spreads in U.S.
Electronic Futures Markets,” investigates the bid-ask spread components in futures
market. The components of bid-ask spreads is one of the most important subjects of
microstructure studies. Utilizing Huang and Stoll’s (1997) method the third essay of this
dissertation provides the first analysis of the components of quoted bid-ask spreads in
U.S. electronic futures markets. The results show that order processing cost is the largest
component of bid-ask spreads, followed by inventory holding costs. During the crisis
period market makers increase bid-ask spreads due to increasing inventory holding and
adverse selection risks.
vi

TABLE OF CONTENTS
CHAPTER PAGE
CHAPTER 1: PRICE DISCOVERY AND LIQUIDITY CHARACTERISTICS
FOR U.S. ELECTRONIC FUTURES AND ETF MARKETS ..........................................1
1.1. Introduction .......................................................................................................1
1.2. Literature Review ..............................................................................................6
1.3. Data ...................................................................................................................9
1.4. Methodology ...................................................................................................10
1.4.1. Price Discovery ......................................................................................10
1.4.2. Determinants of Price Discovery in Futures and ETFs .........................12
1.4.2.1. The Bid-Ask Spread ........................................................13
1.4.2.2. Trade Impact ..............................................................................14
1.4.2.3. VNET Market Depth ..................................................................15
1.4.4.4. Regression Model for the Determinants of Price Discovery ....16
1.5. Results .............................................................................................................18
1.5.1. Price Discovery, Liquidity and Market Depth in Futures and ETF
Markets ..............................................................................................18
1.5.1.1. Information Shares Results ............................................18
1.5.1.2. Liquidity in Futures and ETF Markets......................................20
1.5.1.3. Market VNET Depth in Futures and ETF Markets ..................22
1.5.1.4. Discussion of the Information Share, Liquidity, and Market
Depth Results .........................................................................................23
1.5.2. The Determinants of Price Discovery ...................................................24
1.6. Conclusion ......................................................................................................26
CHAPTER 2: THE RESILIENCY OF LARGE TRADES FOR U.S. ELECTRONIC
FUTURES MARKETS ..........................................................................................41
2.1. Introduction .....................................................................................................41
2.2. Literature Review ............................................................................................42
2.3. Data .................................................................................................................45
2.4. Methodology ...................................................................................................46
2.5. Results .............................................................................................................47
2.5.1. Returns around Large Trades ................................................................48
2.5.2. Bid-Ask Spreads around Large Trades .................................................50
2.6. Conclusion ......................................................................................................52
CHAPTER 3: COMPONENTS OF QUOTED BID-ASK SPREADS IN
U.S. ELECTRONIC FUTURES MARKETS ...................................................66
3.1. Introduction .....................................................................................................66
3.2. Literature Review ............................................................................................67
3.3. Data .................................................................................................................70
3.4. Methodology ...................................................................................................70
vii

3.5. Results .............................................................................................................72
3.6. Conclusion ......................................................................................................74
REFERENCES ..................................................................................................................79
VITA ................................................................................................................................86
viii

LIST OF TABLES
TABLE PAGE
1.1. Futures Contract Specifications ................................................................................29
1.2. Information Shares of Futures, ETFs, and Related Cash Markets .............................30
1.3. Crisis Period Monthly Information Share Values of Futures and ETFs ....................31
1.4. Liquidity and Volatility Measures of Futures and ETFs during the Pre-Crisis
and Crisis ..........................................................................................................................32
1.5. Bid-Ask and Trade Sizes ..........................................................................................33
1.6. VNET Market Depth Values .....................................................................................34
1.7. Determinants of Price Discovery ...............................................................................35
1.8. Determinants of Price Discovery with Adverse Selection Cost ................................36
1.9. Determinants of Price Discovery Using Minimum Values of the Information
Shares ................................................................................................................................39
1.10. Determinants of Price Discovery Using Maximum Values of the Information
Shares ................................................................................................................................40
2.1. Descriptive Statistics .................................................................................................53
2.2. Quote Returns around Large Sales ...........................................................................54
2.3. Quote Returns around Large Purchases ....................................................................55
2.4. Bid-Ask Spreads around Large Sales ........................................................................59
2.5. Bid-Ask Spreads around Large Purchases .................................................................60
3.1. Contract Specifications .............................................................................................75
3.2. Traded Spread and Order Processing Cost Components ..........................................76
3.3. Components of the Bid–Ask Spread, Based on Serial Correlation in Trade
Flows without Trade Clusters ..........................................................................................77
3.4. Components of the Bid–Ask Spread, Based on Serial Correlation in Trade
Flows with Trade Clusters .................................................................................................78
ix

LIST OF FIGURES
FIGURE PAGE
2.1. Cumulative Excess Returns After Block Trades of E-mini S&P 500 Futures .........56
2.2. Cumulative Excess Returns After Block Trades of E-mini NASDAQ 100 Futures 56
2.3. Cumulative Excess Returns After Block Trades of Gold Futures .............................57
2.4. Cumulative Excess Returns After Block Trades of Euro Futures ............................57
2.5. Cumulative Excess Returns After Block Trades of British Pound Futures ..............58
2.6. Bid-Ask Spreads of E-mini S&P 500 Futures around Large Purchases ....................61
2.7. Bid-Ask Spreads of E-mini S&P 500 Futures around Large Sales ...........................61
2.8. Bid-Ask Spreads of E-mini NASDAQ 100 Futures around Large Purchases ...........62
2.9. Bid-Ask Spreads of E-mini NASDAQ 100 Futures around Large Sales ..................62
2.10. Bid-Ask Spreads of Gold Futures around Large Purchases ....................................63
2.11. Bid-Ask Spreads of Gold Futures around Large Sales ...........................................63
2.12. Bid-Ask Spreads of Euro Futures around Large Purchases ....................................64
2.13. Bid-Ask Spreads of Euro Futures around Large Sales ...........................................64
2.14. Bid-Ask Spreads of British Pound Futures around Large Purchases .....................65
2.15. Bid-Ask Spreads of British Pound Futures around Large Sales .............................65
x

CHAPTER 1: PRICE DISCOVERY AND LIQUIDITY CHARACTERISTICS FOR
U.S. ELECTRONIC FUTURES AND ETF MARKETS
1.1. Introduction
Futures contracts, electronically traded exchange traded funds (ETFs), and their
underlying cash markets are three different types of instruments used for speculative,
investment, and/or hedging purposes. The inter-related nature of these securities allows
us to address the issue of market completeness versus redundancy. Thus, we ask which
inter-related instrument(s) incorporate new information and which instrument(s) simply
derives its prices from the other markets. Moreover, analyzing the price discovery
process provides important information on where informed traders focus their attention.
Thus, such knowledge allows participants to determine which markets are most fair and
orderly.
The microstructure issues of U.S. futures markets have received little attention
compared to equity markets, mainly because of the historical lack of bid-ask quotes from
floor-traded futures contracts. Thus, previous authors needed to proxy futures bid-ask
spreads from the futures price series. However, Locke and Venkatesh (1997) show that
spread estimators ineffectively proxy floor-traded futures bid-ask spreads. In addition,
futures floor-traded data incorporates inaccurate recording problems, including the time
displacement of the sequence of trades and prices on the official price record.
In order to analyze the dynamic and time-varying nature of the relative price
discovery process of these markets we employ Hasbrouck’s (1995) information share
methodology. Furthermore, we extend our analysis by examining the determinants of the
price discovery process in these markets. We then explore the effects of large trades and
1

the depth of the market by computing the time series and cross-sectional differences in
these liquidity measures across asset classes. Included in our analysis is a comparison of
the 2008 financial crisis to the pre-crisis period to show how the different characteristics
of market behavior affect the price discovery shares of various financial instruments for
different market conditions. Hasbrouck’s information share method is based on the Law
of One Price. Thus, prices of the same or related instruments cannot deviate from one
another in the long run because of arbitrage activity. Consequently, the same or related
assets share a common value. Therefore, the information share method measures the
contribution of each instrument to this common value.1
Our examination of ETFs in the price discovery process is consistent with the
importance of ETFs as an important investment tool in modern financial markets. During
the 2008 financial crisis 716 ETFs traded in U.S. equity markets, with the daily average
trading volume for the SPY ETF alone approaching 42 billion dollars. Moreover, the
initiation of electronic trading in futures markets and the subsequent growth in high
frequency trading in the new millennium (Karazoglu, 2011) represents a major structural
change in markets.2 In order to capture the microstructure effects in these markets we
employ bid-ask spread data for electronically traded futures contracts on stock index,
currency, and gold and their associated electronically traded ETFs. The literature
conflicts on the importance of ETFs in price discovery: for example, see Hasbrouck
1 Hasbrouck’s (1995) information share method provides maximum and minimum values for each futures
and ETF pair. In the regression we first employ the ratio of the daily average values of the information
shares. Then we repeat our regression analysis using the daily maximum and minimum information share
values separately.
2 A rich literature highlights the increased trading efficiency obtained by electronic trading (e.g., Jain
2005).
2

(2003) versus Tse, Bandyopadhyay and Shen (2006). Using both U.S. equity index
futures and ETF data, Hasbrouck determines that the e-mini S&P 500 futures contributes
more to price discovery than does the floor-traded SPY ETF. Alternatively, Tse,
Bandyopadhyay and Shen show that the contribution made by the DIA ETF to price
discovery is greater than the contribution made by floor-traded futures.
In order to explore the effects of liquidity measures as determinants of the price
discovery process we utilize two methods that have rarely been used in this context
before. We calculate the price impact of trades using Hasbrouck’s (2004) sequential
trading based model and then examine the market depth of futures and ETFs with Engle
and Lange’s (2001) VNET method. With Hasbrouck’s model we analyze not only the
first component of transactions costs (the bid-ask spread), but also the second component
(the price impact of trades). These additions provide a more comprehensive analysis than
previous studies (Ates and Wang 2005, Schlusche 2009). Moreover, Engle and Lange
argue that the best quoted depth does not provide the full depth in markets, whereas
VNET depth captures the realized market depth by measuring the actual trade volume
required to move prices. Finally, our approach differs from previous studies in the
literature by examining the determinants of price discovery for various U.S. electronic
futures relative to their corresponding ETFs.3 We also compare these results for a highly
volatile period versus an average volatility period. Thus, we determine whether analyzing
two distinctly different volatility periods provides evidence concerning differing
determinants of the price discovery process.
3 The stated objective of the ETFs used in our sample is to replicate the returns achieved in the associated
spot markets. However, ETF prices do include tracking error (Shin and Soydemir, 2010; Petajisto, 2011).
3

Previous studies that explore the determinants of the price discovery process
document different variables as significant factors. For example, Theissen (2002)
employs German DAX equity index futures and spot data to show that trading volume
positively affects price leadership of a market. Alternatively, Martens (1998) uses Bund
futures and Schlusche (2009) employs DAX futures and ETFs to document that a
market’s relative contribution to price discovery depends solely on the level of volatility.
Both of these results contradict the transactions costs hypothesis (Fleming, Ostdiek,
Whaley., 1996) which relies on the actual costs of transactions.4 Alternatively, Ates and
Wang (2005) use floor and electronically traded currency futures in U.S. markets to show
that price discovery is affected by the relative liquidity in the floor-traded and electronic
markets, whereas volatility does not affect price discovery. Regarding the research here,
the use of extensive intraday data enables us to analyze the effects of specific factors (i.e.,
the price impact of trades and market depth) that are overlooked in previous studies on
price discovery. In addition, we examine how market characteristics such as volatility and
other time-varying factors affecting price discovery help us to resolve conflicting results
regarding price discovery and its determinants. Our results find support for both the
transactions cost and leverage hypotheses,5 as well as the significance of volatility in the
price discovery process in these markets.
Overall, our study contributes to the literature by investigating the price discovery
process of electronically traded futures and ETFs across a variety of asset classes, and
4 The Transactions Cost Hypothesis states that markets with lower transactions costs (higher liquidity)
exhibit a higher information share.
5 The leverage hypothesis states that leveraged financial instruments attract more informed trading than
non-leveraged instruments. The reason is that informed traders prefer leveraged instruments to take
advantage of their information to increase their profits.
4

then examining the determinants of the price discovery process in these markets.
Specifically, our study contributes to the literature in the following ways. First, we use
electronic markets data instead of floor-traded prices (especially for futures markets),
which provides almost instantaneous trade execution and therefore a more accurate
representation of when information is fully disseminated into market prices. Second, our
real time bid-ask spread databases make it possible to present the first major analysis of
bid-ask quotes for U.S. electronic futures markets, such that our results are not affected
by floor-traded bid-ask estimator bias. A third contribution to the literature is our
examination of three different inter-related markets (futures, their corresponding ETFs,
and the related underlying cash instruments), as well as studying different asset classes
(stock market indexes, currency, and metal futures/ETFs), with both of these factors
adding to previous research on price discovery. Moreover, although a number of studies
examine price discovery, they do not compare ETFs with futures on automated trading
platforms.6 Fourth, we not only analyze the market microstructure liquidity
characteristics of futures contracts and their corresponding ETFs, but we also explore
how price discovery is affected by market depth, volatility, informed trading and
liquidity, including employing the bid-ask spread and the price impact of larger trades.
Thus, our results provide a depth and breadth of results not available elsewhere,
especially in terms of whether information shares are invariant to asset classes. Finally,
and perhaps most importantly, previous studies employ data from relatively stable
periods, whereas we examine the volatile financial crisis of 2008 versus the less volatile
pre-crisis period of 2007 in order to understand the relative importance of liquidity,
6 In addition, we examine ETFs that are electronically traded, rather than floor traded ETFs as with
Hasbrouck (2003).
5

volatility, and VNET depth for price discovery in futures and ETFs in different market
environments.
Our results show that price discovery occurs mainly in the highly liquid and
highly leveraged futures markets. These findings support the transaction cost hypothesis,
as well as the leverage hypotheses. Besides futures and ETF data, we also employ spot
market data for currencies and the stock market cash index to analyze the price discovery
process of these underlying markets. Our results show that futures markets lead the price
discovery process, followed by the spot market and then ETFs.
The results also show that both the ratio of the quoted percentage spreads between
the futures contracts and the corresponding ETFs, and the level of their overall volatility,
determine the relative information shares of these markets. This result holds for all three
types of instruments (stock market indexes, currencies, and metal futures/ETFs). Other
variables (such as the ratio of the impact of trades on prices and the ratio of the daily
average dollar volume of futures and ETFs) do not significantly change the value of the
information shares.
The presentation in the following sections is organized as follows: Section 2
provides a brief literature review of price discovery for futures and ETFs. Section 3
describes the data. Section 4 presents our research methods and section 5 discusses our
results. Concluding remarks and suggestions for future research are summarized in the
last section.
1.2. Literature Review
Previous studies (Pirrong, 1996; Grammig, Schireck, Theissen, 2001; Hasbrouck,
2003; Kurov and Lasser, 2004) compare electronic markets to floor trading (mostly in
6

equities), showing that electronic markets provide anonymity, fast execution and higher
information efficiency advantages to traders relative to floor trading.7 In fact, Hasbrouck
(2003) shows that e-mini electronically traded futures contracts are the dominant source
of information compared to floor traded equity futures, ETFs, and the associated cash
index. However, Tse, Bandyopadhyay and Shen (2006) show that electronically traded
Dow Jones ETFs contributes significantly to the price discovery process relative to the
Dow futures. Therefore, instead of asking which instrument dominates price discovery,
the more relevant question to ask is what characteristics and market conditions cause one
instrument to provide a greater contribution to the price process?
Futures contracts provide anonymity, execution speed, leverage and information
efficiency advantages to investors, as noted above. Alternatively, Alexander and Barbosa
(2008) argue that ETFs’ popularity among individual investors has increased due to the
ability to be sold short and their low transactions costs for small size trades. Deville
(2008) states that ETFs are more convenient as trading instruments compared to futures
for smaller orders and liquidity traders. Hegde and McDermott (2004) say that lower
prices per share and smaller contract sizes for ETFs make them more suitable investment
vehicles for many investors. ETFs also represent quick ways of taking exposure in
particular sectors and strategies. As such, ETF have the potential to lead price discovery
in terms of industry specific information and information that is more dispersed across
many traders. Consequently, ETFs provide an interesting alternative to futures contracts
and the cash market.
7 Subrahmanyam (p. 529, 2009) defines information efficiency as “the amount of private information
revealed in the market price.”
7

Another line of research analyzes the determinants of the price discovery process.
Admati and Pfleiderer (1988) theoretically show that both informed and liquidity traders
prefer to trade in liquid markets. In this sense liquidity enhances the incorporation of
private information into prices by attracting informed traders. Analyzing stocks, futures,
and options in U.S. markets, Fleming, Ostdiek, Whaley (1996) document that a traders’
choice on which market to use depends on the relative transaction costs in alternative
markets. They show that the market with the smallest transactions costs attracts informed
traders and therefore dominates the price discovery process. Martikainen and Puttonen
(1994) and Zhong, Darrat, and Otero. (2004) find similar results for Finnish and Mexican
stock markets. Consequently, in order to examine the relation between price discovery
and transactions costs, several authors study the effect of a reduction in tick size on price
discovery in futures and stocks: Baillie, Booth, Tse and Zabotina (1999) uses the
information-share approach, Chu, Hsieh and Tse, (1999) and Hsieh (2004) employ a
common-factor decomposition approach, and So and Tse (2004), Roope and Zurbruegg
(2002), and Covrig, Ding, and Low (2004) employ both approaches. They all find that
price discovery improves with a reduction in the tick size, which reduces transactions
costs. Regarding bid-ask spreads, Theissen (2002) finds that the size of the relative bid-
ask spread across different markets only weakly explains the contribution to price
discovery, whereas Wang and Ates (2005) show that using the ratio of spreads with
currency futures provides a much stronger evidence of spreads affecting price discovery.
Unlike our study, none of the studies mentioned here use data from a financial crisis
period, when price discovery is particularly important.
8

Volatility is another potential determinant of price discovery. Schlusche (2009)
reports that the price discovery process for DAX futures and its associated ETF is only
affected by its volatility, not its liquidity. Martens (1998) and Franke and Hess (2000)
empirically document that the German bund futures using the Automated Pit Trading
System (APT) on the London International Financial Futures Exchange's (LIFFE’s) made
a greater contribution to price discovery during periods of higher volatility, whereas the
Deutsche Terminborse (DTB) futures made a larger contribution to price discovery
during periods of low volatility.8 Our study helps resolve this debate by focusing on the
difference between a highly volatile crisis period and a normal period, a factor that is not
examined in these studies. Finally, Theissen (2002) finds that the contribution made to
price discovery by the trading system employed was positively related to the size of the
market share. In conclusion, different studies document different variables as the main
determinant of price discovery. Our goal is to resolve this debate by providing a more
comprehensive study of the factors most closely related to price discovery.
1.3. Data
We employ electronic market transactions and bid-ask quotes for five different
futures contracts. The futures employed are chosen to represent a cross-section of
different asset classes; the associated ETFs represent the top ranking ETFs by trading
volume in their respective categories. The futures data are from CQG and the ETF trade
and quotes data are obtained from TAQ. Our sample includes the E-mini S&P 500, E-
mini NASDAQ 100, British pound, the Euro currency, and gold futures. The
8 We use electronic market data as it is the dominant venue for futures trading during our period of study.
For example, according to CME’s website during the pre-crisis period in 2007 electronic futures markets
created 77% of the trading volume, whereas floor trading only caused 23%. Similarly, during the crisis
period the volume share of the electronic market was 84%, with floor trading being 16%.
9

corresponding ETFs trade with ticker symbols of SPY, QQQ, GLD, FXE and FXB. Our
sample period covers the September through December 2008 financial crisis as well as
the January through March 2007 pre-crisis “normal” time period.9 The instrument
specifications for the futures contracts are described in Table 1.1 Panel A. The ETFs used
in this study and the markets they follow are listed in Panel B of Table 1.1. Following
Engle and Lange (2001), the first five minutes of each trading session are excluded.10
1.4. Empirical Methodology
1.4.1. Price Discovery
In the finance literature the price discovery process across related instruments are
typically analyzed using Hasbrouck’s (1995) information share (IS) or Gonzalo
Granger’s (1995) component share (CS) methods. Baillie et al. (2002) argue that although
the IS and CS methods seem different, they share a lot in common, since both techniques
are based on the vector error correction models. In this study we utilize Hasbrouck’s IS
method in order to determine the price discovery ability of electronically traded futures
contracts versus their related ETFs; for some tests their associated cash markets also are
examined.
Hasbrouck’s information share methodology is the first process we employ to
analyze the price discovery process in the futures, ETF and spot markets. This price
9 The selection of these periods is based on the logic provided by Anand, Irvine, Puckett and Venkataraman
(2013). Following their paper we use the first quarter of 2007 as the benchmark period and the last quarter
of 2008 (the Lehman Brothers bankruptcy) as the crisis period. We examine the active nearby expiration
contracts and roll the contracts to the next expiration when either the volume of the deferred contract
becomes dominant, or at least one week prior to the expiration of the nearby contract. Furthermore, trades
that occur on the same side of the market, at the same price, and within the same minute are combined into
one transaction. Bid-ask spreads that are more than $5 per unit price are discarded as misprints or outliers.
10 When the first five minutes are included the quantitative results change by less than 1% and qualitative
inferences are unchanged.
10

discovery model is based on the assumption that arbitrage prevents prices of these related
securities from widely diverging. The information share of an instrument is measured as
that instrument’s contribution to the total variance of the common (random-walk)
component. If pX represents the price of asset X and pY represents the price of asset Y,
t t
then a vector error correction model of order K lags of the price changes can be
represented as:
Δp = A Δp + … + A Δp + γ (z – μ ) + u (1.1)
t t t-1 k t-k t-1 z t
p(cid:2934)
(cid:2930)
where p = (cid:4680) (cid:4681) is the column vector of prices, A is the squared autoregressive coefficient
t p (cid:2935) i
(cid:2930)
matrix of order n for the number of instruments analyzed, γ is vector of the speed of
adjustment coefficients, μ = E(pX - pY) stands for the mean vector of deviations
z t t
representing the long-run average price difference between the two markets, z= pX - pY
t t t
is the price difference matrix, and the γ (z – μ ) term equals the error correction
t-1 z
u(cid:2934)
(cid:2930)
coefficients. Also, u (cid:4680) (cid:4681) is the vector of random innovations with the covariance
t = u (cid:2935)
(cid:2930)
σ(cid:2870) σ
matrix of (cid:3428) (cid:2869) (cid:2869)(cid:2870)(cid:3432). The linear combinations of the random innovations in the prices of
σ σ(cid:2870)
(cid:2870)(cid:2869) (cid:2870)
X and Y provides the innovations of the common price:
a a u(cid:2934)
(cid:2869)(cid:2869) (cid:2869)(cid:2870) (cid:2930)
η = (cid:4674) (cid:4675) (cid:4680) (cid:4681) (1.2)
t a (cid:2870)(cid:2869) a (cid:2870)(cid:2870) u (cid:2935)
(cid:2930)
where the a are determined from the VECM parameters. The variance of the common
ij
price is then:
11

|     |     | σ(cid:2870) σ | a   |     |     |     |
| --- | --- | ------------- | --- | --- | --- | --- |
Var(η) =	(cid:4670)a a (cid:4671)(cid:3428) (cid:2869) (cid:2869)(cid:2870)(cid:3432)(cid:4674) (cid:2869)(cid:2869) (cid:4675)                 (1.3)
| t                                                  | (cid:2869)(cid:2869) (cid:2869)(cid:2870) |                      | a                               |                          |     |     |
| -------------------------------------------------- | ----------------------------------------- | -------------------- | ------------------------------- | ------------------------ | --- | --- |
|                                                    |                                           | σ σ(cid:2870)        |                                 |                          |     |     |
|                                                    |                                           | (cid:2870)(cid:2869) | (cid:2870) (cid:2869)(cid:2870) |                          |     |     |
| When the covariance matrix is diagonal (cid:4666)σ |                                           |                      |                                 | (cid:3404) 0(cid:4667):  |     |     |
(cid:2869)(cid:2870)
Var(η)=	Var(cid:4666)ηtA(cid:4667)	(cid:3404)	a(cid:2870) σ(cid:2870) (cid:3397)a(cid:2870) σ(cid:2870)                (1.4)
| t   |     | (cid:2869)(cid:2869) (cid:2869) | (cid:2869)(cid:2870) (cid:2870) |     |     |     |
| --- | --- | ------------------------------- | ------------------------------- | --- | --- | --- |
The information share for security X is then equal to
| (cid:3028)(cid:3118) (cid:3097)(cid:3118) |     |     |     |     |     |              |
| ----------------------------------------- | --- | --- | --- | --- | --- | ------------ |
| (cid:3117)(cid:3117) (cid:3117)           |     |     |     |     |     |              |
| IS x  =                                   |     |     |     |     |     |       (1.5)  |
(cid:2978)(cid:3118)
(cid:3215)
Similarly, the information share for security Y is:
| (cid:3028)(cid:3118) (cid:3097)(cid:3118) |     |     |     |     |     |     |
| ----------------------------------------- | --- | --- | --- | --- | --- | --- |
IS =  (cid:3117)(cid:3118) (cid:3118)                        (1.6)
y  (cid:2978)(cid:3118)
(cid:3215)

  Hasbrouck’s  method  constructs  upper  and  lower  bounds  for  the  information
shares by orthogonalizing (rotating) the covariance matrix to determine the explanatory
power of a particular market. Following Hasbrouck (2003) we use the quote mid-points
for prices in order to avoid the bid-ask bounce issue.11
1.4.2. Determinants of the Price Discovery Process in Futures and ETFs
After determining which market(s) dominate the price discovery process, for both
the  crisis  and  pre-crisis  periods,  we  then  explore  the  relative  importance  of  the
determinants of the daily variation in information share of the futures and ETF markets.
Specifically, using a regression model we test how the price discovery process is affected

11 Bid-ask bounce is the constant reversal of trade prices between the bid and ask sides of the market. Using
trade prices causes the price series to appear to oscillate between the bid and ask prices, even though the
true value of the asset does not change.
12

by the relative liquidity (the price impact of trades and the bid-ask spread), market depth
(as measured by VNET, i.e. the volume needed to move prices 0.5%), daily dollar
volume, declining average trade size, increasing adverse selection cost, and the aggregate
volatility of the futures and ETFs.
We employ the bid-ask spread and the price impact of trades in order to explore
the effects of liquidity on price discovery. VNET measures the realized depth; by
including VNET we test the effect that market depth has on price discovery. Adverse
selection cost (Glosten and Harris (1987)) and higher average trade size are used to
capture informed trading activity (O’Hara, 1987).
1.4.2.1. The Bid-Ask Spread
Trading costs have three main components (Fleming, Ostdiek, and Whaley,
1996). These costs are the bid-ask spread, the market impact of trades, and brokerage
commissions. Fleming, Ostdieck, and Whaley state that in a perfectly frictionless and
rational market, new information should be incorporated simultaneously into the prices of
similar securities traded in different markets. However, their results show that the price
discovery process is dominated by the lowest-cost market.
In order to explore the effects of the first component of transactions costs (the bid-
ask spread) on price discovery we calculate the average of the percentage quoted spreads
for each day and each instrument. We obtain the percentage spread by dividing the dollar
quoted spread by the midpoint of the bid and ask quotes. Ates and Wang (2005) show,
that the ratio of the spreads between the electronic market and floor trading is the only
significant factor affecting the price discovery process. According to their results, when
the relative spread increases in one market, its contribution to the price discovery process
13

decreases. In our analysis we employ the ratio of the daily average electronic futures
spread to the ETF electronic spread to examine price discovery.
1.4.2.2. Trade Impact
According to the transaction cost hypothesis a second factor that can affect
information share is the market impact of transactions on prices. Market impact measures
the percentage of the price variation that can be attributed to trade size, and is determined
using Hasbrouck’s (2004) sequential-trading-based regression equation. Hasbrouck)
develops a Markov Chain Monte Carlo (MCMC) based method to assign trade direction
for floor traded markets. Since bid-ask quotes are available from our electronic markets,
we classify trade direction by using the methodology introduced by Lee and Ready
(1991) to obtain a more powerful test than the MCMC method, which is based only on
inferred spreads from transactions prices.
We use the following regression model in order to analyze the impact of trades on
the futures and ETF markets:
Δm =
∑(cid:3011)
(cid:1869) λ v + u (1.7)
t (cid:3011)(cid:2880)(cid:2868) t-j j t-j t
where m is the midpoint of the ask and bid quotes, q is the trade direction (which takes
the value of 1 for buy orders and -1 for sell orders based on the Lee and Ready
algorithm),12 λ (1x2) is the two element coefficient vector for the impact of these trades,
which is multiplied by the associated two element vector v:
12 The Lee and Ready (1991) algorithm classifies a trade as a buy (sell) if the trade price is closer to the ask
(bid). Trades that occur exactly at the mid-quote are classified according to the tick rule of the previous
trade. In such cases if the trade price is larger (smaller) than the previous price then it is classified as a buy
(sell).
14

v = [1 √volume]′. (1.8)
t-j
where volume is the dollar trade volume of each transaction. Hasbrouck argues that the
square-root transformation in (8) is motivated by trade-price impact studies in equity
markets that generally find concavity in the relation.
For our information share regression, one of the key explanatory factors is λ,
which represents the daily ratio of the trade impact values between the futures contract
and the ETF. As discussed previously, we expect the market with a lower price impact to
have a higher information share. The ratio λ captures the relative transactions costs of the
two instruments in terms of the price impact of the trades of these instruments. We expect
the coefficient to be negative according to the transaction cost hypothesis, since the
transaction costs and its information share in a given market are negatively correlated. In
addition, in our regression the ratio of the daily dollar volumes of the instruments
determines the relative activity of the two instruments.
1.4.2.3. VNET Market Depth
We calculate the net directional volume (VNET depth) values in order to measure
the market depth in the futures and ETF markets, as well as allowing us to examine the
effect of market depth on information share price discovery in the three inter-related
markets. VNET (Engle and Lange, 2001) is based on the assumption that price changes
occur due to the imbalance between buyer and seller initiated trades. Thus, VNET is the
net directional volume (i.e., the difference between the volume of buyer-initiated volume
and the volume of seller-initiated volume) causing a given price change over a time
interval (called the price duration). Engle and Lange (2001) argue that on an ex-post basis
the VNET measure captures the realized market depth. The formula for VNET is:
15

VNET =|∑q Vol | (1.9)
i i
where q is the direction of the trade (1 for buy, -1 for sell) and Vol is the dollar trade
i i
volume. Engle and Lange (2001) determine VNET by picking price level thresholds in
order to obtain a daily average number of price durations. Since the price levels of futures
and ETFs are substantially different, we define the “price duration” as the amount of time
between 0.5% cumulative price changes.13 In this context, VNET measures the realized
depth that is associated with a certain percentage price change. For example, when
market depth is low, a smaller net directional volume is sufficient to change prices 0.5%
and the VNET value is lower compared to the periods when a higher volume is required
to move prices. Engle and Russell (1998) show that the expected length of the price
durations is inversely proportional to volatility. Accordingly, lower VNET values would
be expected in a time series of a crisis compared to a non-crisis period, whereas a cross-
section of the market with higher depth should have larger VNET values.
1.4.2.4. Regression Model for the Determinants of Price Discovery
We examine how liquidity affects the price discovery process by analyzing the
effects of the ratio of bid-ask spreads, daily dollar volume, trade impact, average dollar
trade size,14 VNET depth values, and volatility on the information shares of futures and
ETFs. In order to minimize the effects of microstructure noise (as discussed by Andersen
and Bollerslev, 1998), we employ a five-minute sampling frequency in order to measure
the daily volatility in markets, as done by Schlusche (2009). Since the daily volatility in
13 The results are consistent when 0.1% and 0.25% price changes are used for the price durations.
14 O’Hara (1987) argues that informed traders use larger orders compared to uninformed traders. To
analyze whether relative order sizes affect the price discovery in futures and ETF markets we use the ratio
of the futures and ETF average dollar trades sizes.
16

both the futures and ETF markets show an extremely high correlation,15 we employ the
aggregate standard deviations of the futures and corresponding ETFs, which is consistent
with Andersen and Bollerslev (1998) and Schlusche (2009). The regression equation to
examine what factors affect information share (IS) is given in (1.10):
IS = β + β Rspread + β Rvolumet + β Volatility + β Rvnet + β Rtrade_impacts + β
t 0 1 t 2 t 3 t 4 t 5 t 6
Rtrade_size (1.10)
t
where Rspread is the ratio of the percentage spreads, Rvnet is the ratio of the VNET
values, Rvolume is the daily average dollar volume ratio, Rsize is the ratio of the average
dollar trade sizes, Rtrade value is the ratio of the liquidity coefficients in the futures and
ETF markets, and volatility is the aggregate of the two market’s volatility on day t, where
the daily volatility is calculated as the sum-of-squares of the five-minute intraday returns
(Andersen and Bollerslev, 1998). Each variable in the model employs trade-by-trade data
to determine the daily value. The t-statistics are calculated using Newey-West corrected
standard errors to adjust for any potential serial correlation.
We also test the effects of the adverse selection component of effective spreads on
price discovery (Glosten and Harris, 1987; Hendershott, Jones and Menkveld, 2011). The
adverse selection cost of a spread is calculated as:
Adv_selection = q (m – m )/m (1.11)
jt jt j,t+5min j,t j,t
15 Average dollar volume, trade size, percentage spreads and other factors are different in futures and ETF
markets, but volatility is similar as they follow the same underlying cash or spot market and the ratio is
almost equal to1. Therefore, instead of using the ratio of volatility, we employ the aggregate value for
volatility.
17

where q is the trade direction indicator, m is the midpoint of the prevailing quote,
jt j,t
m is the quote midpoint five minutes after the trade and q takes the value of +1 for
j,t+5min
purchases and -1 for sales.
Grammig and Peter (2013) argue that the upper and lower bounds of the
information share values diverge at higher sampling frequencies. Thus, since we employ
trade by trade high frequency data, we also execute the regressions given above for the
ratios of the maximum values and the ratios of the minimum values of the information
share as a robustness check.
1.5. Results
1.5.1. Price Discovery, Liquidity and Market Depth in Futures and ETF Markets
1.5.1.1. Information Share Results
We start our empirical analysis by exploring the price discovery process of
futures, ETFs, and the underlying spot markets. Panel A of Table 1.2 (left columns)
shows the mean information share values obtained using Hasbrouck’s (1995) model for
the inter-related futures and ETF instruments. In Panel B we extend the scope of the
analysis of the inter-related markets, determining the information share values for futures,
ETFs, and their underlying spot markets.
The results in both panels show that the price discovery process is dominated by
futures, both for the pre-crisis and crisis periods. The implication is that informed traders
engage in futures markets more than in ETFs. The dominance of futures over ETFs is
most prominent for currency markets. Specifically, the British pound futures possess an
information share)of 0.983 versus the information share of 0.017 for the British pound
ETFs during the pre-crisis; for the crisis period the pound futures and ETF information
18

share values are 0.973 and 0.027, respectively. Similarly, the Euro futures possess a large
information share of 0.963 and a value of 0.037 for the ETFs during the pre-crisis and
0.941 and 0.059 for the crisis period, respectively. The dominance of futures over the
ETFs is least prominent for metals: comparing gold futures to the gold ETF shows the
smallest difference in information shares between the two markets (an information share
of 0.762 for futures vs. a value of 0.238 for ETFs during the pre-crisis, and values of
0.731 for futures and 0.269 for the ETF during the crisis). These results show that the
gold ETF (GLD) attracts more informed trading relative to the currency and equity
ETFs16.
Panel B of Table 1.2 reports our information share results for the expanded set of
inter-related securities of futures, ETFs, and spot markets. These results show that futures
remain the main venue for price discovery, followed by the spot market, then the ETFs.
In fact, spot markets have a higher information share than ETFs for all asset classes in
this study, with these results being consistent for both the pre-crisis and crisis periods.
Next we analyze the changes in the price discovery shares of these instruments
during the crisis period. The general conclusion is the information share of the
(leveraged) futures market declines during the volatile crisis period. We arrive at this
conclusion for all asset classes when we compare the information share of futures during
the pre-crisis period with the information share during crisis period in any given row of
Table 1.2. This pattern is particularly obvious in Panel B when all three instruments are
16Daigler and Padungsaksawasdi (2014) document that gold exhibits a positive risk-return relation, opposite
to stocks and currencies. The reasoning is that gold “crashes” upward, whereas the stock market crashes
downward; currencies can have large moves in either direction. They argue that gold is considered a safe
haven and generally used for hedging purposes. Consequently, ETFs could be suitable for hedgers as they
are not leveraged and thus less risky than futures markets.
19

analyzed. For example, the E-mini S&P 500 futures information share declines from
0.722 in the normal period to 0.633 during the crisis period, whereas the information
share of ETFs and cash indexes increase. Specifically, the information share for the SPY
ETF increases from 0.081 in the pre-crisis period to 0.136 in the crisis period. Similarly,
the cash index’s IS increase from 0.157 in the pre-crisis period to 0.231 in the crisis
period. Thus, the analysis of changes in information share values show that the price
discovery share of cash indexes and ETFs increase during the crisis period, whereas the
contribution of the futures correspondingly decline.
In Table 1.3 we report the information share values for the futures and ETFs in
our sample for each month during the crisis period. According to these results, the futures
contracts consistently dominate their ETF pairs during each of the four months. This
shows that our results are not driven by an extreme value in one month, rather they are
consistent throughout the crisis period.
1.5.1.2. Liquidity in the Futures and ETF Markets
After documenting that futures contracts possess higher information share values
than the ETFs, we now turn our attention to the study of the determinants of price
discovery. Here we examine the liquidity of these instruments as a potential determinant
of the relative information shares. Table 1.4 shows our results for the size of the
percentage spreads and Hasbrouck’s (2004) sequential trading model on the price impact
of trades. The first two numerical columns of Table 1.4 report the average percentage
spreads for the futures and ETFs for the two time periods. The ETFs possess much larger
percentage spreads than the futures. The next set of columns shows that the trade impact
20

coefficients from the regression are significantly smaller for futures than for ETFs, which
is consistent with the percentage spread results.
Brunnermeier and Pedersen (2009) and Chiu et al. (2012) show that the
borrowing constraints of investors during the crisis period adversely affected liquidity in
financial markets. The pre-crisis versus crisis comparison of the bid-ask spreads shows
that the percentage spreads of every instrument in our sample increased during the crisis
period, which is consistent with the worsening of liquidity in the futures and ETF markets
during the crisis period. Also, the effect of the trade impact aspect of liquidity for both
the futures and ETFs deteriorate (become larger) during the crisis period.
Hasbrouck (2004) argues that the R-squared values for the sequential trading-
based regression model show to what extent traders are informed in one market. In other
words, the R-squared values in Hasbrouck’s model measure the proportion of price
changes that originates from the trading activity. Consistent with our information share
results, the R-square values for the futures contracts are higher than the ETFs, both in the
pre-crisis and crisis periods. Also during the crisis period trades explain a lesser
percentage (smaller R-square values) of the price changes for both the futures and ETF
markets. The last column of the table reports the standard deviations of returns, which
shows the increased volatility existing during the crisis period. The results for the R-
squared values and standard deviations show the heightened uncertainty in the futures
and ETF markets during the crisis period. Using the crisis period provides the opportunity
to analyze how price discovery and other microstructure characteristics of futures and
ETFs are affected by the increased uncertainty during this period. Previous studies (Ates
and Wang, 2005; Schlusche, 2009) only employ stable time periods.
21

Table 1.5 continues our examination of liquidity variables as determinates of price
discovery, employing variables such as the average bid-ask quote sizes and the trade sizes
of the futures and ETFs. Consistent with our liquidity analysis in Table 1.4, these results
show that both the average bid-ask quote sizes and the trade sizes decline during the
crisis. The decline in the liquidity of futures and ETFs in terms of increased trade impact,
increased percentage spread, wider quotes, and lower trade sizes during the financial
crisis shows the different adverse effects of the crisis on the futures and ETF markets.
Thus, the volatility and liquidity results show that the pre-crisis and crisis periods provide
an interesting environment to examine the effects of decreased liquidity and increased
volatility on the price discovery process between futures and ETFs.
1.5.1.3. Market VNET Depth in Futures and ETF Markets
In Table 1.6 we report the average daily dollar volume and the average VNET
depth, where VNET is the dollar volume needed to change prices by 0.5%. The higher
the VNET, the deeper and more liquid the markets. We first discuss the levels of VNET
followed by the changes in VNET. The dollar VNET values for the futures are much
higher than the VNET values for the ETFs, with currency futures showing the largest
difference – especially during the crisis period.17 As Hasbrouck (2004) states, there are
several other venues for currency trading (e.g., the interbank market), which could be the
reason why currency ETFs exhibit less VNET depth values compared to other ETFs in
our sample. Comparatively, relative to the other futures contracts, higher net directional
dollar volumes (VNET) are required to change the prices of stock index ETFs. The larger
VNETs for the stock index ETFs during the crisis is consistent with the increased
17 During the crisis period of 2008 those trading currencies turned from the interbank market to the futures
market to avoid the credit risk of money center banks during this time period.
22

popularity and volume of the ETFs during this time period, as discussed in the
introduction.
Next we discuss changes in VNET from the pre-crisis period to the crisis period.
During the crisis period there were a large number of 0.5% price changes compared to the
pre-crisis period for all the asset classes in our sample. Moreover, the price durations (the
length of the time interval when a 0.5% price change occurred) are much shorter during
the crisis period (not shown here). For example, during the first quarter of 2007 there
were 64 price durations for the e-mini S&P 500 futures, whereas in the last quarter of
2008 more than 3,000 0.5% price changes occurred for the same futures contract. Thus,
in normal times the net directional dollar volume (VNET) needed for the futures
contracts to change 0.5% is substantially less. However, the VNET results for the ETFs
show that average VNET values for the ETFs are actually higher during the crisis period
compared to the pre-crisis period. Consequently, changes in the daily trading volume
during the crisis shows that a similar pattern occurs between the futures and ETFs, since
the daily trading volumes of the ETFs are actually higher during the crisis period relative
to the pre-crisis period.
Overall, our results show that one important development during the crisis period
was the worsening of the market depth of futures markets (as measured by VNET). In
contrast, the realized depth for ETFs improved.
1.5.1.4. Discussion of the Information Share, Liquidity, and Market Depth Results
The results reported above show that futures contracts are more liquid and possess
larger information shares and market depth compared to the ETFs. These results are
consistent with the transactions cost and leverage hypotheses, as the more liquid and
23

leveraged futures market dominates the price discovery process. Our analysis for the
crisis period shows that high volatility affects futures and ETF markets in terms of price
discovery, liquidity and market depth.
We documented that both the average daily dollar trading volume and the VNET
values of the ETFs increased during the crisis period, whereas both trading volume and
VNET values of futures contracts declined. The liquidity measures of the percentage
spread and trade impacts highlight the adverse effect of high volatility on the liquidity of
both futures and ETF markets.
The significantly different information share results for futures and ETFs for the
pre-crisis period versus the crisis period shows that the relative price discovery in futures
and ETFs was significantly affected by the 2008 financial crisis. Thus, although futures
dominate the price discovery process in both time periods, the information shares of
ETFs increased (the information shares of futures declined) during the crisis period. In
the next section our goal is to explore the factors that significantly affect the day-to-day
variation in information share values of futures and ETFs.
1.5.2. The Determinants of Price Discovery
Using the information shares of futures contracts as the dependent variable, we
test the impact of relative liquidity using the ratios of percentage spreads and of trade
impacts, market depth (VNET), informed trading (average trade size and the adverse
selection component of effective spreads), and aggregate volatility on price discovery. In
Tables 1.7 and 1.8 we document our regression results for these potential determinants of
price discovery. Unlike previous studies (Ates and Wang 2005; Schlusche 2009) that find
only one factor as significant, our results in Table 1.7 show that the coefficients for
24

volatility and the ratio of percentage spreads are significantly negative for explaining
information shares. Thus, when the ratio of the percentage spreads of the futures to the
ETFs decreases (i.e., the futures spreads become smaller relative to the ETF spreads),
then the information share of the futures markets increases, and vice-versa. This result is
consistent with the transaction cost hypothesis. Moreover, our results show that volatility
also affects the information shares of futures and ETFs. This finding means that the
information shares of the leveraged futures markets decline and the information shares of
ETFs increase during more volatile time periods. Other variables in our model (such as
the ratio of depth, trade impact, and average trade size) are not significant factors. Thus,
our results show that only the percentage spread and volatility significantly affect price
discovery for both the pre-crisis and crisis periods. These results support the transaction
cost hypothesis. Moreover, our price discovery results show that the first component of
transaction costs (namely the spread, Fleming, Ostdiek, and Whaley, 1996), is the most
important measure of liquidity. Consequently, we find that during periods of high
volatility the futures information shares decline, although futures still dominate the price
discovery process. Table 1.8 employs the ratios of the adverse selection costs in futures
and ETF markets in place of the average trade sizes. Similar to our findings in Table 1.7,
Table 1.8 shows that the ratio of the spreads and the aggregate volatility are the only two
significant factors affecting the price discovery process.
One potential issue with our results is the use of high frequency data to examine
the information share. In particular, Grammig and Peter (2013) state that at higher
sampling frequencies, such as five and ten minutes, the upper and lower bounds of the
25

information share values diverge. Since we employ trade by trade data in our analysis we
test the robustness of our results by re-examining the information shares by separately
testing the minimum values in Table 1.9. We report our regression results for the
determinants of price discovery using the ratios of the minimum values of the daily
information shares of the futures relative to the ETF as the dependent variable. Our
results are similar to the findings we document in Tables 1.7 and 1.8. These results also
show that when the aggregate volatility in futures and ETF markets increases, the
information share of futures markets declines. Moreover, the relative liquidity in one
market is inversely related to its information share. Table 10 documents the results for the
ratios of the maximum values of the information shares. Consistent with previous results
we find that the relative liquidity and volatility variables are significant variables that
affect price discovery. Overall, our results are robust, whether we employ the mean,
maximum, or minimum values of the information shares.
1.6. Conclusion
Two of the most important functions of a financial market are to provide price
discovery and liquidity (O’Hara 1987). The price discovery and liquidity characteristics
of futures markets have received limited attention compared to equity markets.
Historically, the key reason for this dearth of futures microstructure studies was the lack
of bid-ask quote data, since such data is not available for floor trading transactions that
dominated futures trading until recently. Alternatively, electronic exchanges gather such
information. In addition, we compare the price discovery and liquidity characteristics of
ETFs to futures contracts.
26

Using electronic quote and transaction data for futures and ETFs we analyze the
price discovery processes for five different instruments during a normal and a volatile
time period. We find that the futures dominate the price discovery processes during both
the volatile financial crisis and the pre-crisis periods.
We also examine the liquidity characteristics of the futures and ETFs in our
sample in terms of percentage spreads and the price impact of large trades. We find that
currency futures are the most liquid contracts among futures, with gold being the least
liquid contract. Alternatively, currency ETFs are the least liquid and equity ETFs are the
most liquid among the ETFs. The lack of liquidity for currencies is consistent with the
other venues of currency trading that exist, as well as the relative lack of interest in
currency trading by individual investors compared to equities. Our results also show that
the liquidity of both futures and ETFs decline during the crisis.
Our analysis on volume and realized market depth documents the adverse effects
of a financial crisis on futures markets. Compared to the pre-crisis period both the daily
dollar volume and market depth (as measured by VNET) declined in the futures market
during the crisis. Alternatively, these measures are higher for the ETFs for the crisis,
showing the increased interest from traders for these financial instruments during this
time period (see Alexander and Barbosa, 2009, for their discussion of ETFs).
We investigate whether these liquidity changes affect price discovery in futures
and ETF markets by regressing the information shares on these instruments’ ratio of the
bid-ask spread, the average trade size, dollar volume, the trade impact on prices, and
aggregate volatility. The regression results support the transaction cost hypothesis in
terms of the importance of the relative bid-ask spread. Moreover, our results show that
27

volatility is another significant factor that affects the price discovery process between
futures and ETF markets. Consistent with Kyle and Obhizhaeva’s (2011) market
microstructure invariance theorem, the determinants on price discovery are the same two
factors for currency, stock index and gold futures, as well as their corresponding ETFs.
Future research projects could extend this paper to include options market data,
where options on futures and options on ETFs are employed as underlying instruments.
The results would determine the contribution of options to price discovery and how their
contribution changes based on different market conditions.
28

|     |     |     |     |                                  | Table 1.1 – Panel A   |     |     |
| --- | --- | --- | --- | -------------------------------- | --------------------- | --- | --- |
|     |     |     |     | Futures Contract Specifications  |                       |     |     |

| Contract     |     |     | E-mini S&P 500  |     | E-mini Nasdaq 100            |     | Gold  |
| ------------ | --- | --- | --------------- | --- | ---------------------------- | --- | ----- |
| Symbol       |     |     | ES              |     | NQ                           |     | GL    |
| Related ETF  |     |     | SPY             |     | QQQ                          |     | GLD   |
| Tick Size    |     |     | $0.25           |     | $0.25----------------------  |     | $0.1  |
Contract Size  $50 x index price  $20 x index price  100 troy oz
Expiration Months  Mar,Jun,Sep,Dec  Mar,Jun,Sep,Dec  Feb,Apr,Jun,Aug,Oct,Dec
| Price Quoted in    |     |     | Index points          |     | Index points      |     | $/oz  |
| ------------------ | --- | --- | --------------------- | --- | ----------------- | --- | ----- |
|                    |     |     |                       |     |                   |     |       |
| Contract           |     |     | British pound         |     | Euro              |     |       |
| Symbol             |     |     | M6B                   |     | M6E               |     |       |
| Related ETF        |     |     | FXB                   |     | FXE               |     |       |
| Tick Size          |     |     | $0.0001 USD/GBP       |     | $0.0001 USD/Euro  |     |       |
| Contract Size      |     |     | 6,250 British pounds  |     | 125,000 Euros     |     |       |
| Expiration Months  |     |     | Mar,Jun,Sep,Dec       |     | Mar,Jun,Sep,Dec   |     |       |
| Price Quoted in    |     |     | USD/GBP               |     | USD/EUR           |     |       |
|                    |     |     |                       |     |                   |     |       |

|     |     |     |     |     | Table 1.1 – Panel B   |     |     |
| --- | --- | --- | --- | --- | --------------------- | --- | --- |
|     |     |     |     |     | ETF Definitions       |     |     |
  Definition
SPY  Provide investment results that correspond to the price and divident performance of the S&P
500 Index.
QQQ  Provides investment results that correspond to the price and dividend performance of the Nasdaq
100 Index.
GLD  Replicate the performance of the price of gold bullion.
FXE  Tracks the price of the Euro.
FXB  Tracks the price of the British pound.

Panel A reports the specifications of the futures contracts. Contracts are traded electronically on the Chicago
Mercantile Exchange’s GLOBEX electronic trading platform. Panel B provides the definitions of the ETFs.
Unlike the futures in our sample, these ETFs are not leveraged. All ETF performances are net of expenses.
Source: The CMEX website.

29

|     |     |     |     |            |     |     |     |
| --- | --- | --- | --- | ---------- | --- | --- | --- |
|     |     |     |     |            |     |     |     |
|     |     |     |     | Table 1.2  |     |     |     |
         Information Shares of Futures, ETFs, and Related Cash Markets
| Panel A  |     |     |     | Panel B  |     |     |     |
| -------- | --- | --- | --- | -------- | --- | --- | --- |
Instrument  Pre-Crisis  Crisis  Instrument  Pre-Crisis  Crisis
E-mini S&P
|     | 0.879  |     | 0.857**  | E-mini S&P 500 | 0.722  | 0.633**  |     |
| --- | ------ | --- | -------- | -------------- | ------ | -------- | --- |
500
| SPY ETF     | 0.121  |     | 0.143**  | SPY ETF     | 0.081  | 0.136**  |     |
| ----------- | ------ | --- | -------- | ----------- | ------ | -------- | --- |
|             |        |     |          | Cash Index  | 0.157  | 0.231**  |     |
|             |        |     |          |             |        |          |     |
| E-mini      |        |     |          | E-mini      |        |          |     |
|             | 0.894  |     | 0.849**  |             | 0.770  | 0.661**  |     |
| NASDAQ 100  |        |     |          | NASDAQ 100  |        |          |     |
| QQQ ETF     | 0.106  |     | 0.151**  | QQQ ETF     | 0.108  | 0.130**  |     |
NASDAQ 100
|                |        |     |         |                 | 0.112  | 0.209**  |     |
| -------------- | ------ | --- | ------- | --------------- | ------ | -------- | --- |
|                |        |     |         | Cash Index      |        |          |     |
| Euro Futures   | 0.963  |     | 0.941*  | Euro Futures    | 0.609  | 0.547*   |     |
| FXE ETF        | 0.037  |     | 0.059*  | FXE ETF         | 0.110  | 0.152*   |     |
|                |        |     |         | Euro Spot       | 0.281  | 0.351*   |     |
| British Pound  |        |     |         | British Pound   |        |          |     |
|                | 0.983  |     | 0.973*  |                 | 0.614  | 0.602*   |     |
| Futures        |        |     |         | Futures         |        |          |     |
| FXB ETF        | 0.017  |     | 0.027*  | FXB ETF         | 0.030  | 0.071*   |     |
|                |        |     |         | British Pound   | 0.356  | 0.327*   |     |
S t
| Gold Futures  | 0.762  |     | 0.731**  |     |     |     |     |
| ------------- | ------ | --- | -------- | --- | --- | --- | --- |

| GLD ETF  | 0.238  |     | 0.269**  |     |     |     |     |
| -------- | ------ | --- | -------- | --- | --- | --- | --- |

Panel A of this table (left columns) reports the Hasbrouck (1995) information share values for the futures
and ETFs in our sample. Panel B (right columns) report the results for our three-way analysis of futures,
ETFs, and spot markets. The pre-crisis period covers January-March 2007 and the crisis period covers
September-December 2008. The data source is CQG database for futures and TAQ for ETFs. The
notations * and ** refer to the significance of the difference between the crisis and pre-crisis periods at the
5% and 1% levels, respectively.

30

|     |     |     |   Table 1.3  |     |     |
| --- | --- | --- | ------------ | --- | --- |
Crisis Period Monthly Information Share Values of Futures and ETFs
| Instrument      |       September  |     | October  | November  | December  |
| --------------- | ---------------- | --- | -------- | --------- | --------- |
| E-mini S&P 500  | 0.864            |     | 0.842    | 0.847     | 0.876     |
| SPY ETF         | 0.136            |     | 0.158    | 0.153     | 0.124     |
|                 |                  |     |          |           |           |

E-mini NASDAQ
|     | 0.858  |     | 0.832  | 0.827  | 0.879  |
| --- | ------ | --- | ------ | ------ | ------ |
100
| QQQ ETF  | 0.142  |     | 0.168  | 0.173  | 0.121  |
| -------- | ------ | --- | ------ | ------ | ------ |
|          |        |     |        |        |        |

| Euro Futures  | 0.962  |     | 0.921  | 0.933  | 0.947  |
| ------------- | ------ | --- | ------ | ------ | ------ |
| FXE ETF       | 0.038  |     | 0.079  | 0.077  | 0.053  |

British Pound
|     | 0.982  |     | 0.960  | 0.977  | 0.974  |
| --- | ------ | --- | ------ | ------ | ------ |
Futures
| FXB ETF       | 0.018  |     | 0.040  | 0.023  | 0.026  |
| ------------- | ------ | --- | ------ | ------ | ------ |
| Gold Futures  | 0.741  |     | 0.725  | 0.719  | 0.747  |
|  GLD ETF      | 0.059  |     | 0.075  | 0.081  | 0.053  |
This table reports the Hasbrouck (1995) monthly information share values for the futures and ETFs in our
sample during the crisis period (September-December 2008). The data source is CQG database for futures
and TAQ for ETFs.
31

Table 1.4
Liquidity and Volatility Measures of Futures and ETFs during the Pre-Crisis and Crisis Periods
Average Percentage Spread Trade Impact Coefficients R-sq St. Deviation of Returns
Trade Direction Trade Volume
Contract Pre-Crisis Crisis Pre-Crisis Crisis Pre-Crisis Crisis Pre-Crisis Crisis Pre-Crisis Crisis
S&P 500 Futures 0.011 0.02 0.41 0.98 0.10 0.12 41% 31% 1.12 2.54
SPY ETF 0.018 0.04 0.54 1.32 0.23 0.36 10% 1% 0.89 2.03
NASDAQ Futures 0.013 0.02 0.53 1.11 0.09 0.12 34% 30% 1.23 2.77
QQQ ETF 0.028 0.06 0.82 1.52 0.11 0.13 08% 01% 1.21 2.59
Gold Futures 0.023 0.04 0.81 1.24 0.14 0.18 25% 22% 1.61 2.91
GLD ETF 0.088 0.20 1.14 2.05 0.51 0.92 07% 01% 1.31 2.88
Euro Futures 0.006 0.01 0.23 0.33 0.04 0.05 49% 42% 0.22 1.58
FXE ETF 0.312 0.39 3.30 4.20 0.93 1.17 01% 01% 1.47 2.23
Brit. Pound Futures 0.008 0.01 0.34 0.43 0.06 0.09 45% 43% 0.16 0.58
FXB ETF 0.366 0.72 2.20 4.42 0.86 1.46 02% 01% 1.70 2.70
This table reports the spreads and trade impact coefficients. Higher values for the trade impact coefficients are associated with lower liquidity. Trade impacts
are analyzed using Δm = ∑(cid:2192) (cid:2199) λv + u where λ = (λ, λ, ) , v = [1 √volume], Δm is the change in the efficient price; the R2 value of this
t (cid:2192)(cid:2880)(cid:2777) t-j j t-j t j jintercept jslope t-j t
regression model provides the price variation that is attributable to the trades. Trade direction λ, and trade volume λ, impact coefficients are
jintercept jslope
multiplied by 10,000, where trade direction (q) is equal to +1 for buy orders and -1 for sell orders. The pre-crisis period covers January-March 2007 and
crisis period covers September-December 2008. The data source is CQG database for futures and TAQ for ETFs.
32

Table 1.5
Bid-Ask and Trade Sizes
Contract Average Bid Size Average Ask Size Average Trade Size Average Dollar Trade Size
Pre-Crisis Crisis Pre-Crisis Crisis Pre-Crisis Crisis Pre-Crisi Crisis
S&P 500 599.63 151.28 601.37 150.90 17.88 7.48 1,277,242 390,996
SPY ETF 318.61 72.77 303.35 77.22 8.99 4.31 129,467 38,694
NASDAQ 100 67.24 17.42 66.47 17.98 29.31 16.53 1,468,526 572,826
QQQ ETF 2006.52 462.94 1968.65 467.26 20.96 6.96 82,891 23,706
Gold Futures 6.51 3.91 6.36 3.97 4.37 2.68 294,748 207,240
GLD ETF 111.79 23.43 111.90 23.67 6.59 2.79 42,595 21,207
Euro Futures 16.58 12.39 17.64 12.06 5.63 2.59 1,008,617 417,621
FXE ETF 43.80 35.37 48.55 37.92 5.39 3.18 67,903 44,527
British Pound
Futures 12.35 10.07 14.27 10.45 4.17 2.31 874,971 342,843
FXB ETF 23.18 21.28 27.92 21.38 4.38 2.87 84,713 51,947
This table provides the average quote and trades sizes. The values for ETFs are reported in lots where one lot is equal to one hundred shares. Average
dollar trade volumes of transactions are reported in the last two columns. The pre-crisis period covers January-March 2007 and crisis period covers
September-December 2008. The data source is CQG database for futures and TAQ for ETFs.
33

Table 1.6
VNET Market Depth Values

|     |     | Daily Avg. Dollar  |     | Average VNET (in  |        Number of  Price  |     |
| --- | --- | ------------------ | --- | ----------------- | ------------------------ | --- |
Contract
|     |     | Volume (in billions)  |     | thousands)  |     | Durations |
| --- | --- | --------------------- | --- | ----------- | --- | --------- |

Pre-Crisis  Crisis  Pre-Crisis  Crisis    Pre-Crisis  Crisis
| S&P 500  | 73.211  | 56.493  | 3,596.502  | 640.391  | 56  | 3,131  |
| -------- | ------- | ------- | ---------- | -------- | --- | ------ |
| SPY ETF  | 13.656  | 41.945  | 304.617    | 463.805  | 64  | 3,322  |
NASDAQ
| 100      | 21.464  | 19.399  | 2,817.432  | 582.662  | 77  | 3,361  |
| -------- | ------- | ------- | ---------- | -------- | --- | ------ |
| QQQ ETF  | 3.342   | 7.818   | 243.256    | 359.186  | 61  | 3,652  |
Gold
| Futures       | 1.643   | 1.420   | 321.717    | 258.644  | 159  | 516  |
| ------------- | ------- | ------- | ---------- | -------- | ---- | ---- |
| GLD ETF       | 0.371   | 1.343   | 142.216    | 160.259  | 127  | 492  |
| Euro Futures  | 16.824  | 14.211  | 4,913.213  | 573.463  | 128  | 623  |
| FXE ETF       | 0.011   | 0.103   | 42.916     | 89.666   | 164  | 782  |
British
Pound
| Futures  | 14.345  | 11.853  | 4,214.215  | 549.713  | 133  | 741  |
| -------- | ------- | ------- | ---------- | -------- | ---- | ---- |
| FXB ETF  | 0.002   | 0.015   | 21.739     | 46.095   | 179  | 932  |
This table reports the daily average dollar volume market depth of futures contracts and ETFs as measured
by VNET. Average VNET values show the average net directional dollar volume needed that leads to a
0.5% price change. Every interval where a 0.5% price change occurs is defined as a price duration. VNET
values are calculated using the formula: VNET=Σ|qiVoli|, where “q” is the trade direction and “Vol” is the
volume traded. Larger VNET values are associated with higher market depth, which means it takes greater
net directional volume to change the price. The number of price durations is inversely related to market
liquidity. The pre-crisis period covers January-March 2007 and crisis period covers September-December
2008. The data source is CQG database for futures and  and TAQ for ETFs.

34

Table 1.7
Determinants of Price Discovery
Panel A: Full Sample
|     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
E-mini NASDAQ
|     | E-Mini S&P 500  |      | Euro  | British Pound  | Gold  |
| --- | --------------- | ---- | ----- | -------------- | ----- |
|     |                 | 100  |       |                |       |

| Ratio of  | -1.60  | -1.71  | -0. 44  | -0.37  | -1.41  |
| --------- | ------ | ------ | ------- | ------ | ------ |
Spreads
|                | (-7.71)  | (-7.67)  | (-4.87)  | (-4.74)  | (-5.84)  |
| -------------- | -------- | -------- | -------- | -------- | -------- |
| Volume         | -0.35    | -0.31    | -0.19    | -0.83    | -0.19    |
|                | (-0.57)  | (-0.69)  | (-0.10)  | (-0.88)  | (-0.13)  |
| Volatility     | -2.33    | -1.91    | -1.51    | -0.65    | -1.24    |
|                | (-8.16)  | (-7.14)  | (-4.43)  | (-3.74)  | (-4.25)  |
| VNET           | -0.08    | 0.12     | -0.29    | -0.28    | -0.31    |
|                | (-0.03)  | (-0.05)  | (-0.08)  | (-0.07)  | (-0.11)  |
| Trade Impact   | 0.25     | 0.48     | -0.11    | 0.27     | 0.52     |
|                | (-0.04)  | (0.16)   | (-0.07)  | (0.09)   | (0.05)   |
| Trade Size     | 0.19     | -0.24    | 0.13     | -0.52    | -0.20    |
|                | (0.12)   | (-0.19)  | (-0.15)  | (-0.13)  | (-0.19)  |
| Dummy          | 2.81     | 3.14     | 2.24     | 1.63     | 1.03     |
|                | (-2.44)  | (-2.51)  | (-2.36)  | (-2.49)  | (-2.33)  |
| Adjusted R-sq  | 27%      | 28%      | 23%      | 25%      | 17%      |

Panel B: Pre-Crisis
| Ratio of   | -1.43  | -1.51  | -0.89  | -0.78  | -1.33  |
| ---------- | ------ | ------ | ------ | ------ | ------ |
Spreads
|                | (-7.24)  | (-7.49)  | (-5.96)  | (-5.24)  | (-6.77)  |
| -------------- | -------- | -------- | -------- | -------- | -------- |
| Volume         | 0.26     | 0.36     | 0.79     | -0.40    | -0.58    |
|                | (-0.22)  | (-0.27)  | (-0.41)  | (-0.33)  | (-0.38)  |
| Volatility     | -2.27    | -1.43    | -1.29    | -0.92    | -1.42    |
|                | (-5.17)  | (-4.11)  | (-3.16)  | (-3.01)  | (-3.74)  |
| VNET           | -0.12    | -0.19    | -0.12    | -0.61    | -0.83    |
|                | (-0.04)  | (-0.07)  | (-0.13)  | (-0.25)  | (-0.31)  |
| Trade Impact   | 0.42     | 0.73     | -0.66    | 0.17     | 0.74     |
|                | (-0.15)  | (-0.64)  | (-0.73)  | (-0.05)  | (-0.54)  |
| Trade Size     | -0.26    | -0.67    | 0.42     | 0.38     | 0.73     |
|                | (0.13)   | (-0.22)  | (0.13)   | (0.08)   | (0.25)   |
| Adjusted R-sq  | 27%      | 22%      | 24%      | 21%      | 16%      |
|                |          |          |          |          |          |
35

Panel C: Crisis Period
|     | E-Mini S&P 500 | E-mini NASDAQ 100 |     |     | Euro  |     | British Pound  | Gold |
| --- | -------------- | ----------------- | --- | --- | ----- | --- | -------------- | ---- |

| Ratio of    | -1.96    |     | -1.83    |     | -0.54    |     | -0.47    | -1.33   |
| ----------- | -------- | --- | -------- | --- | -------- | --- | -------- | ------- |
| Spreads     | (-9.26)  |     | (-9.43)  |     | (-6.35)  |     | (-5.45)  | (-7.12) |
| Volume      | -0.18    |     | -0.13    |     | -0.27    |     | -0.15    | -0.41   |
|             | (-0.49)  |     | (-0.45)  |     | (-0.65)  |     | (-0.48)  | (-0.66) |
| Volatility  | -2.14    |     | -1.66    |     | -1.14    |     | -1.33    | -1.06   |
|             | (-7.41)  |     | (-6.32)  |     | (-4.29)  |     | (-5.42)  | (-4.02) |
VNET
|                | -0.11    |     | -0.29    |     | -0.51    |     | -0.46    | -0.39   |
| -------------- | -------- | --- | -------- | --- | -------- | --- | -------- | ------- |
|                | (-0.05)  |     | (-0.07)  |     | (-0.20)  |     | (-0.18)  | (-0.15) |
| Trade Impact   | -0.33    |     | -0.21    |     | -0.77    |     | -0.29    | -0.67   |
|                | (-0.08)  |     | (-0.13)  |     | (-0.19)  |     | (-0.14)  | (-0.16) |
| Trade Size     | -0.61    |     | -0.44    |     | -0.53    |     | -0.26    | -0.69   |
|                | (-0.84)  |     | (-0.55)  |     | (-0.67)  |     | (-0.18)  | (-0.91) |
| Adjusted R-sq  | 29%      |     | 25%      |     | 17%      |     | 21%      | 18%     |
This table reports the OLS regression results for futures contracts information share on the spread, volume,
trade size, trade impact coefficients, volatility and VNET market depth values. Every variable in the model
(except volatility) is calculated using the ratio of daily values from the futures and ETFs. The model we use
can be represented as: ISt = β  + β Spread + β Volume + β Volatility + β Vnet + β Trade_impacts +
|                                                                                                                 |     | 0 1 | t 2 | t   | 3   | t 4 | t 5 | t   |
| --------------------------------------------------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| β 6 Trade_size, where spread is the ratio of percentage spreads, Vnet is the ratio of Vnet values, Volume is  t |     |     |     |     |     |     |     |     |
the total dollar trading volume ratio, Size is the ratio of the average trade sizes, and Trade Impact is the ratio
of the liquidity coefficients for futures and ETFs. Volatility is the sum of the two markets’ volatility on day
t, where the daily volatility is calculated as the sum of squares of the 5-minute intraday returns (Andersen &
Bollerslev, 1998). We obtain the percentage spread by dividing the dollar spread by the midpoint of the bid
and ask prices. Every variable in the model is calculated for each day and the information shares of the
futures are regressed on these variables. T-values are reported in parentheses. Coefficients and t-values in
bold values are significant at the 5% level. The t-statistics are calculated using Newey-West, which corrects
standard errors to adjust for any potential serial correlation.

36

Table 1.8
Determinants of Price Discovery with Adverse Selection Cost
Panel A: Full Sample
|     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
E-mini NASDAQ
|     | E-Mini S&P 500  |      | Euro  | British Pound  | Gold  |
| --- | --------------- | ---- | ----- | -------------- | ----- |
|     |                 | 100  |       |                |       |

| Ratio of  | -1.58  | -1.75  | -0. 49  | -0.41  | -1.53  |
| --------- | ------ | ------ | ------- | ------ | ------ |
Spreads
|               | (-7.43)  | (-7.24)  | (-4.85)  | (-4.61)  | (-5.43)  |
| ------------- | -------- | -------- | -------- | -------- | -------- |
| Volume        | -0.34    | -0.31    | -0.24    | -0.74    | -0.23    |
|               | (-0.55)  | (-0.69)  | (-0.11)  | (-0.79)  | (-0.16)  |
| Volatility    | -2.31    | -1.93    | -1.54    | -0.63    | -1.22    |
|               | (-8.16)  | (-7.14)  | (-4.39)  | (-3.69)  | (-4.21)  |
| VNET          | -0.11    | -0.12    | -0.29    | -0.28    | -0.31    |
|               | (-0.04)  | (-0.05)  | (-0.08)  | (-0.07)  | (-0.11)  |
| Trade Impact  | 0.22     | 0.48     | -0.11    | 0.27     | 0.52     |
|               | (-0.04)  | (0.16)   | (-0.07)  | (0.09)   | (0.05)   |
| Adverse       | 0.64     | 0.37     | 0.29     | 0.57     | 0.83     |
Selection Cost
|                | (0.87)   | (0.64)   | (0.79)   | (0.63)   | (0.72)   |
| -------------- | -------- | -------- | -------- | -------- | -------- |
| Dummy          | -2.79    | -3.14    | -2.25    | -1.66    | -1.02    |
|                | (-2.38)  | (-2.48)  | (-2.31)  | (-2.46)  | (-2.31)  |
| Adjusted R-sq  | 26%      | 28%      | 22%      | 24%      | 17%      |

Panel B: Pre-Crisis
| Ratio of   | -1.38  | -1.53  | -0.89  | -0.79  | -1.21  |
| ---------- | ------ | ------ | ------ | ------ | ------ |
Spreads
|                | (-7.18)  | (-7.42)  | (-5.96)  | (-5.21)  | (-6.72)  |
| -------------- | -------- | -------- | -------- | -------- | -------- |
| Volume         | 0.27     | 0.35     | 0.71     | -0.45    | -0.55    |
|                | (-0.23)  | (-0.25)  | (-0.40)  | (-0.35)  | (-0.34)  |
| Volatility     | -2.29    | -1.45    | -1.26    | -0.98    | -1.38    |
|                | (-5.15)  | (-4.10)  | (-3.11)  | (-2.97)  | (-3.68)  |
| VNET           | -0.13    | -0.16    | -0.14    | -0.63    | -0.81    |
|                | (-0.05)  | (-0.09)  | (-0.11)  | (-0.23)  | (-0.29)  |
| Trade Impact   | 0.40     | 0.75     | -0.63    | 0.20     | 0.71     |
|                | (-0.17)  | (-0.62)  | (-0.76)  | (-0.05)  | (-0.52)  |
| Adverse Cost   | 0.53     | 0.38     | 0.48     | 0.73     | 0.62     |
|                | (0.54)   | (0.71)   | (0.65)   | (0.71)   | (0.82)   |
| Adjusted R-sq  | 26%      | 21%      | 25%      | 23%      | 15%      |
|                |          |          |          |          |          |
37

|     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Panel C: Crisis Period
|     | E-Mini S&P 500 | E-mini NASDAQ 100 |     |     | Euro  |     | British Pound  | Gold |
| --- | -------------- | ----------------- | --- | --- | ----- | --- | -------------- | ---- |

| Ratio of       | -1.93    |     | -1.86    |     | -0.57    |     | -0.49    | -1.31   |
| -------------- | -------- | --- | -------- | --- | -------- | --- | -------- | ------- |
| Spreads        | (-9.21)  |     | (-9.38)  |     | (-6.31)  |     | (-5.42)  | (-7.06) |
| Volume         | -0.17    |     | -0.16    |     | -0.29    |     | -0.17    | -0.40   |
|                | (-0.45)  |     | (-0.43)  |     | (-0.63)  |     | (-0.43)  | (-0.68) |
| Volatility     | -2.11    |     | -1.62    |     | -1.17    |     | -1.29    | -1.03   |
|                | (-7.29)  |     | (-6.25)  |     | (-4.25)  |     | (-5.22)  | (-4.01) |
| VNET           | -0.12    |     | -0.27    |     | -0.53    |     | -0.48    | -0.37   |
|                | (-0.06)  |     | (-0.09)  |     | (-0.18)  |     | (-0.19)  | (-0.13) |
| Trade Impact   | -0.32    |     | -0.22    |     | -0.75    |     | -0.28    | -0.64   |
|                | (-0.08)  |     | (-0.12)  |     | (-0.22)  |     | (-0.15)  | (-0.18) |
| Adverse Cost   | 0.61     |     | 0.65     |     | 0.43     |     | 0.56     | -0.69   |
|                | (0.84)   |     | (0.71)   |     | (0.82)   |     | (0.77)   | (-0.91) |
| Adjusted R-sq  | 28%      |     | 24%      |     | 19%      |     | 20%      | 19%     |
This table reports the OLS regression results using the adverse selection component of effective spread
instead of average trade sizes employed in Table 6. Every variable in the model (except volatility) is
calculated using the ratio of daily values from the futures and ETFs. The model we use can be represented
as: ISt = β 0  + β 1 Spread + β t 2 Volume + β t 3 Volatility + β t 4 Vnet + β t 5 Trade_impacts + β t 6 Adverse_cost, where  t
spread is the ratio of percentage spreads, Vnet is the ratio of Vnet values, Volume is the total dollar trading
volume ratio, Adverse is the adverse selection cost component of effective spreads, and Trade Impact is the
ratio of the liquidity coefficients for futures and ETFs. Volatility is the sum of the two markets’ volatility on
day t, where the daily volatility is calculated as the sum of squares of the 5-minute intraday returns
(Andersen & Bollerslev, 1998). We obtain the percentage spread by dividing the dollar spread by the
midpoint of the bid and ask prices. Every variable in the model is calculated for each day and the
information shares of the futures are regressed on these variables. T-values are reported in parentheses.
Coefficients and t-values in bold values are significant at the 5% level. The t-statistics are calculated using
Newey-West, which corrects standard errors to adjust for any potential serial correlation.

38

Table 1.9
Determinants of Price Discovery Using Minimum Values of the Information Shares

E-mini NASDAQ
|     | E-Mini S&P 500  |      | Euro  | British Pound  |     | Gold  |
| --- | --------------- | ---- | ----- | -------------- | --- | ----- |
|     |                 | 100  |       |                |     |       |

| Ratio of  | -1.45  | -1.59  | -0.52  | -0.45  |     | -1.22  |
| --------- | ------ | ------ | ------ | ------ | --- | ------ |
Spreads
|               | (-7.32)  | (-7.41)  | (-4.46)  | (-4.51)  |     | (-5.79)  |
| ------------- | -------- | -------- | -------- | -------- | --- | -------- |
| Volume        | -0.39    | -0.51    | -0.16    | -0.73    |     | -0.17    |
|               | (-0.47)  | (-0.34)  | (-0.13)  | (-0.92)  |     | (-0.15)  |
| Volatility    | -2.44    | -1.82    | -1.62    | -0.65    |     | -1.21    |
|               | (-8.06)  | (-6.89)  | (-4.43)  | (-3.74)  |     | (-4.21)  |
| VNET          | -0.12    | -0.18    | -0.22    | -0.24    |     | -0.22    |
|               | (-0.03)  | (-0.04)  | (-0.08)  | (-0.05)  |     | (-0.12)  |
| Trade Impact  | -0.22    | -0.54    | -0.13    | -0.33    |     | -0.44    |
|               | -0.16    | -0.16    | 0.07     | -0.12    |     | -0.07    |
Adverse Cost
|     | -0.19    | -0.24    | -0.11    | -0.47    |     | -0.23    |
| --- | -------- | -------- | -------- | -------- | --- | -------- |
|     | (-0.12)  | (-0.19)  | (-0.15)  | (-0.16)  |     | (-0.17)  |
Dummy
|     | -2.73    | -2.92    | -2.14    | -1.59    |     | -1.26    |
| --- | -------- | -------- | -------- | -------- | --- | -------- |
|     | (-2.29)  | (-2.41)  | (-2.36)  | (-2.49)  |     | (-2.29)  |
Adjusted R-sq
|     | 26%  | 25%  | 23%  | 24%  |     | 14%  |
| --- | ---- | ---- | ---- | ---- | --- | ---- |
This table reports the OLS regression results using the daily ratio of the minimum values of the information
share as the dependent variable (rather than the mean values of the information shares employed in Table 7).
Every variable in the model (except volatility) is calculated using the ratio of daily values from the futures
and ETFs. The model we use can be represented as: ISt = β  + β Spread + β Volume + β Volatility +
|     |     |     | 0 1 | t 2 | t 3 | t   |
| --- | --- | --- | --- | --- | --- | --- |
β Vnet + β Trade_impacts + β Adverse_cost, where spread is the ratio of the percentage spreads, Vnet is
| 4 t 5 | t 6 | t   |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- |
the ratio of Vnet values, Volume is the total dollar trading volume ratio, Adverse is the adverse selection
cost component of the effective spreads, and Trade Impact is the ratio of the liquidity coefficients for futures
and ETFs. Volatility is the sum of the two markets’ volatility on day t, where the daily volatility is calculated
as the sum of squares of the 5-minute intraday returns (Andersen & Bollerslev, 1998). We obtain the
percentage spread by dividing the dollar spread by the midpoint of the bid and ask prices. Every variable in
the model is calculated for each day and the information shares of the futures are regressed on these
variables. T-values are reported in parentheses. Coefficients and t-values in bold are significant at the 5%
level. The t-statistics are calculated using Newey-West, which corrects standard errors to adjust for any
potential serial correlation.

39

Table 1.10
Determinants of Price Discovery Using Maximum Values of the Information Shares

E-mini NASDAQ
|     | E-Mini S&P 500  |      | Euro  | British Pound  |     | Gold  |
| --- | --------------- | ---- | ----- | -------------- | --- | ----- |
|     |                 | 100  |       |                |     |       |

| Ratio of  | -1.51  | -1.48  | -0.49  | -0.42  |     | -1.16  |
| --------- | ------ | ------ | ------ | ------ | --- | ------ |
Spreads
|               | (-7.39)  | (-7.22)  | (-4.48)  | (-4.54)  |     | (-5.92)  |
| ------------- | -------- | -------- | -------- | -------- | --- | -------- |
| Volume        | -0.44    | -0.56    | -0.23    | -0.66    |     | -0.21    |
|               | (-0.38)  | (-0.41)  | (-0.09)  | (-0.86)  |     | (-0.16)  |
| Volatility    | -2.38    | -1.76    | -1.69    | -0.71    |     | -1.17    |
|               | (-7.95)  | (-6.77)  | (-4.51)  | (-3.88)  |     | (-4.16)  |
| VNET          | -0.16    | -0.22    | -0.17    | -0.28    |     | -0.16    |
|               | (-0.04)  | (-0.08)  | (-0.07)  | (-0.09)  |     | (-0.13)  |
| Trade Impact  | -0.26    | -0.33    | -0.46    | -0.33    |     | -0.44    |
|               | -0.19    | -0.33    | -0.31    | -0.41    |     | -0.17    |
Adverse Cost
|     | -0.11    | -0.28    | -0.17    | -0.37    |     | -0.12    |
| --- | -------- | -------- | -------- | -------- | --- | -------- |
|     | (-0.17)  | (-0.24)  | (-0.20)  | (-0.15)  |     | (-0.17)  |
Dummy
|     | -2.73    | -2.86    | -2.03    | -1.63    |     | -1.33    |
| --- | -------- | -------- | -------- | -------- | --- | -------- |
|     | (-2.29)  | (-2.47)  | (-2.26)  | (-2.41)  |     | (-2.15)  |
Adjusted R-sq
|     | 27%  | 25%  | 22%  | 22%  |     | 13%  |
| --- | ---- | ---- | ---- | ---- | --- | ---- |
This table reports the OLS regression results using the daily ratio of the maximum values of the information
share as the dependent variable (rather than the mean values of the information shares employed in Table 7.
Every variable in the model (except volatility) is calculated using the ratio of daily values from the futures
and ETFs. The model we use can be represented as: ISt = β  + β Spread + β Volume + β Volatility +
|     |     |     | 0 1 | t 2 | t 3 | t   |
| --- | --- | --- | --- | --- | --- | --- |
β Vnet + β Trade_impacts + β Adverse_cost, where spread is the ratio of the percentage spreads, Vnet is
| 4 t 5 | t 6 | t   |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- |
the ratio of Vnet values, Volume is the total dollar trading volume ratio, Adverse is the adverse selection
cost component of the effective spreads, and Trade Impact is the ratio of the liquidity coefficients for futures
and ETFs. Volatility is the sum of the two markets’ volatility on day t, where the daily volatility is calculated
as the sum of squares of the 5-minute intraday returns (Andersen & Bollerslev, 1998). We obtain the
percentage spread by dividing the dollar spread by the midpoint of the bid and ask prices. Every variable in
the model is calculated for each day and the information shares of the futures are regressed on these
variables. T-values are reported in parentheses. Coefficients and t-values in bold values are significant at the
5% level. The t-statistics are calculated using Newey-West, which corrects standard errors to adjust for any
potential serial correlation.

40

CHAPTER 2: THE RESILIENCY OF LARGE TRADES FOR U.S. ELECTRONIC
FUTURES MARKETS
2.1. Introduction
Market liquidity is considered to be the most important criterion for evaluating
market quality (Clemons and Weber 1992). Kyle (1985) identifies three components of
market liquidity: bid–ask spread, depth, and resiliency. Bid–ask spread measures the
difference between the prices at which the dealer is willing to buy and sell the instrument.
Depth is defined as the size of the order flow required to change prices. Resiliency is the
speed that prices return to equilibrium following a large trade. Thus, resilient markets are
those where the price effects of large trades are small and short-lived. In this respect,
resiliency is the time dimension of liquidity.
Resiliency is an important aspect of liquidity affecting trading strategies and
investor performance. Traders prefer resilient markets, as transaction costs increase when
the market is not resilient. Obizhaeva and Wang (2005) and Alfonsi, Fruth, and Schied
(2005) argue that an optimal trading strategy, one which minimizes execution costs,
depends on the resiliency of an investor’s book. Regulators and exchanges both have an
interest in more resilient markets, whose lower transaction costs attract more investors,
increasing exchange profits and helping to prevent price manipulations.
Despite its importance, the resiliency of U.S. electronic futures markets has not
been analyzed in previous studies (since actual bid-ask prices were not available for floor
trading), causing existing literature to focus on the resiliency of U.S. equity markets. My
study contributes to the literature in the following ways: 1) For the first time, the
41

resiliency of U.S. electronic futures markets is examined; 2) Changes in market resiliency
are investigated over types of markets by comparing the resiliency of U.S. futures
markets in pre-crisis versus crisis periods; and 3) By using different asset classes, the
study is able to assess the resiliency of a wide spectrum of futures contracts.
My results show that markets are more resilient when they are less volatile.
Moreover, different types of assets show different resiliencies. In particular, according to
our results, currency futures are more resilient than the equity index and gold futures.
Markets also respond differently to large buy and sell orders during a volatile period,
when large sell trade effects outweigh those of large buy trades.
2.2. Literature Review
Numerous studies analyze the effects of large trades on stock price behavior.
These studies document that the price impacts of large trades are larger than the price
impacts of smaller trades. Although these pioneering studies establish the importance of
“resiliency” i.e. the time dimension of liquidity in microstructure literature, they majorly
focus on the equity market. Thus, “resiliency” as a fundamental measure of market
quality/liquidity can be better understood by examining an asset market other than equity.
Our study adds to this very nascent literature on “resiliency” by examining several assets
in the US futures market. This will also help shed more light on the connection between
various aspects of market quality namely spread, depth and resiliency.
For example, Easley and O’Hara (1987) theoretically and empirically show that
large trades affect stock prices more than small trades because large trades contain
private information. Hasbrouck (1991) finds that large trades in stock markets contain
42

information and thus their bid–ask spreads are wider for large trades. Lee, Mucklow, and
Ready (1993) document that in equity market the bid–ask spreads widen and depths
decline after large trades. Lee and Radhakrishna (2000) document that a majority of
institutional trades in equity markets are indeed large trades. Koski and Michaely (2000)
show that liquidity suppliers in equity markets adjust bid–ask spreads when they face
adverse selection risk. Similar effects of large trades on equity markets are documented
empirically by Kraus and Stoll 1972; Holthausen, Leftwich, and Mayers 1987, 1990;
Gemmill 1996; and Keim and Madhavan 1996.
Saar (2001) theoretically shows that the price impact of trades depends on
economic conditions. Chiyachantana, et al. (2004) empirically supports the theoretical
model of Saar (2001), arguing that institutional traders pay for liquidity when they sell in
declining markets or buy in rising markets.
Subrahmanyam (1991) and Gorton and Pennacchi (1993) theoretically prove that
individual, equity-specific private information is negligible for futures and other types of
basket securities. However, Fleming, Ostdiek, and Whaley (1996) state that futures
markets attract informed traders, because of their low transaction costs and leverage. In
fact, their empirical results show that futures prices incorporate new information faster
than index and option prices. They argue that futures prices lead other markets because
informed traders prefer to trade in this market. Subrahmanyam (1991) states that
frictions, such as nonsynchronous trading in the underlying stocks, can explain the lead
of index futures prices over cash index prices. Berkman, Brailsford, and Frino (2005) find
that trades in U.K. futures markets are mainly liquidity-motivated. Similarly, using data
43

from the Sydney Futures Exchange, Frino and Oetomo (2005) show that price effects of
large trades in futures markets are smaller than those of large trades in equity markets.
Frino and Oetomo (2005) also do not find asymmetry between the effects of buy and sell
trades. These results, as well as the theoretical models of Subrahmanyam (1991) and
Gorton and Pennacchi (1993), show that differences exist in the trading dynamics
between futures and equity markets.
Coppejans, Domowitz, and Madhavan (2003) provide evidence for the high
degree of resiliency of the Swedish stock index futures market, showing that the
reduction of liquidity dissipates quickly following a volatility shock (disappearing within
an hour after the shock). They attribute this rapid adjustment to the self-correcting nature
of automated auctions. Frino and Cummings (2010) report that the 3 Year
Commonwealth Treasury Bond Futures on the Sydney Futures Exchange recover after 12
trades following a block trade.
The research in this paper differs from prior studies that focus on the effects of
large trades and the resiliency of markets in several aspects. First, prior research does not
analyze the resiliency of the U.S. electronic futures markets. Previous studies on futures
floor trading did not provide an accurate and precise time sequence of trades, unlike the
futures data employed here. Second, prior studies only employ one type of futures
contract, whereas here the resiliencies of five different futures contracts are analyzed and
compared. Third, this study examines the effect of different market conditions (the
44

volatility of the 2008 financial crisis) on resilience.18 To sum up, both the wide spectrum
of data and uniquness of data period makes this study fill the gaps in literature that have
not been explored by prior studies.
2.3. Data
I employ electronic market transactions and bid–ask quote data for five different
futures contracts from the CQG futures database. Use of electronic prices is an important
extension of past studies since floor trading price data does not provide bid–ask prices
(and approximations from formulas are notoriously inaccurate) and floor prices provide
imprecise time sequences of trades; thus, only with electronic trade data is the current
study possible with accuracy. My sample includes the E-mini S&P 500, E-mini
NASDAQ 100 equity index, gold, British pound, and the euro currency futures to
represent a wide spectrum of different asset classes. My sample time periods are the
volatile financial crisis time span of September 2008 through December 2008 and the less
volatile pre-crisis period of January 2007 through March 2007.
Trades that occur at the same price, in the same trade direction (buy or sell), and
within the same minute are aggregated. Nearby contracts are employed in the analysis,
since they are the most active contracts. Trades are categorized into 10 groups, based on
the empirical distribution of transaction sizes of each contract. Block trades are
associated with the 10th group since they possess the largest transaction sizes.
18 As Brunnermeier (2009) states, the 2008 financial crisis was the most severe crisis since the Great
Depression.
45

2.4. Methodology
Following Koski and Michaely (2000) and Frino and Cummings (2009), quoted
prices and bid–ask spreads are used for the return and liquidity analyses in order to avoid
the bid–ask bounce. In accordance with the Lee and Ready (1991) algorithm, trades that
are closer to the ask (bid) are classified as buy (sell) trades. Trades that occur at the
midquote are classified according to the price of the previous trade. If the trade price is
larger (lower) than the previous trade price, then it is classified as a buy (sell).
Following Holthausen, Leftwich, and Mayers (1990); Koski and Michaely (2000);
and Frino Cummings (2009), block trades are designated as trade 0 and then benchmark
returns (BENR) are calculated for each contract from the returns for quotes sequenced
from –20 through –11 relative to the block trades
∑(cid:3263) ∑(cid:3127)(cid:3117)(cid:3117)
(cid:3019)(cid:3037),(cid:3047)
(cid:3285)(cid:3128)(cid:3117) (cid:3295)(cid:3128)(cid:3127)(cid:3118)(cid:3116)
BENR = , (2.1.)
(cid:3015)
where N is the total number of trades during the period (pre-crisis or crisis), and R is the
j,t
return for quote t. Returns are computed using the ask quote prices for purchases and bid
quote prices for sales.
Using the benchmark for the ask quotes, mean excess returns for block purchases
(MRP) are computed as
(cid:3263)(cid:3291)(cid:3296)(cid:3293)
∑ (cid:3019)(cid:3037)(cid:3047)(cid:2879)(cid:3003)(cid:3006)(cid:3015)(cid:3019)
(cid:3285)
MRP = , t= -10, … , +20, (2.2)
t
(cid:3015)(cid:3043)(cid:3048)(cid:3045)
46

where N is the total number of block purchases. Mean excess returns for block sales
pur
(MRS) are calculated using the total number of sales and the bid quotes. After analyzing
the price impacts around large trades, the changes in the bid-ask quote sizes surrounding
large trades are examined using the following formulas.
First, benchmarks spreads for each futures contract are computed as
∑(cid:3263) ∑(cid:3127)(cid:3117)(cid:3117)
(cid:3020)(cid:3037),(cid:3047)
(cid:3285)(cid:3128)(cid:3117) (cid:3295)(cid:3128)(cid:3127)(cid:3118)(cid:3116)
BENSPR = , (2.3.)
(cid:3015)
where is S is the bid-ask spread for quote t.
j,t
Mean excess spreads are computed using the equation
(cid:3263)(cid:3291)(cid:3296)(cid:3293)
∑ (cid:3020)(cid:3037)(cid:3047)(cid:2879)(cid:3003)(cid:3006)(cid:3015)(cid:3020)(cid:3017)(cid:3019)
(cid:3285)
MS = t= -10, … , +20 (2.4.)
t
(cid:3015)(cid:3043)(cid:3048)(cid:3045)
Using these equations above, the effects of large trades are analyzed in terms of returns
and liquidity.
2.5. Results
The summary statistics reported in Table 2.1. show that the average number of
contracts for each block trade were less during the crisis period compared to the pre-crisis
period. Furthermore, the number of block sales and purchases per day were also lower
during the crisis period. These results reflect the declining degree of trading activity in
the futures markets during the crisis period.
47

2.5.1. Returns around Large Trades
In this section the returns after large trades are analyzed for each of the five
futures contracts, both before and during the crisis periods. The results in Tables 2.2.
through 2.5. show that among all the contracts in my sample, currency futures exhibit the
smallest returns following large trades. Of the two currency futures, after block trades
euro futures have smaller returns than British pound futures. Moreover, gold futures
exhibit the highest returns after large trades. Comparing returns for the two index futures
following large trades, we can see that returns in the E-mini NASDAQ 100 futures
market are larger than the returns in the E-mini S&P 500 futures market. These results
show that E-mini S&P 500 futures contracts are more liquid than the E-mini NASDAQ
100 futures.
Saar (2001) theoretically shows that price reactions to trades depend on the
economic condition. My empirical results examine the 2008 pre-crisis to crisis periods,
concluding that the results here support his argument. In particular, during the crisis
period the returns after block trades are much larger than those during the pre-crisis
period (see Figures 2.1.–2.5.). The results show that most of the price adjustment occurs
within the first few trades for electronic futures markets. The larger returns for block
trades during the crisis period reflect a decline in liquidity during that time period.
Furthermore, the crisis period exhibits an asymmetry between the price effects of large
buy and large sell trades, unlike the pre-crisis period. Thus, during the crisis period the
returns after large sell trades are greater than returns after large buy trades. However,
during the pre-crisis period, returns exhibit similar return patterns after large buy and sell
48

trades. For example, the instant return for the E-mini S&P 500 index futures after both
purchases and sells is around 0.3% during the pre-crisis period (Figure 2.1.), whereas
after 20 trades the return increases to approximately 0.5%. Alternatively, during the crisis
period the instant return for large buy trades is 0.46% and for large sales is 0.62%,
whereas after 20 trades the cumulative return for large purchases is 0.8% and for large
sales is 1.0%. Using the E-mini NASDAQ 100 index futures one finds similar results
(Figure 2.2). Comparison of Figures 2.1. and 2.2. shows that the E-mini S&P 500 futures
market is slightly more liquid than the E-mini NASDAQ 100 futures market for both the
pre-crisis and crisis periods. For example the instant returns following large purchases
and large sales (0.42% and –0.44%, respectively) are larger than the instant returns for
the E-mini S&P 500 market. Similarly during the crisis period, the initial returns
following a large purchase (0.56%), and the return following a large sale (0.65%), are
also larger than the initial returns in the E-mini S&P 500 market. Returns following large
trades in the gold futures market are higher than the returns in any other markets that are
analyzed in this study (Figure 2.3.). During the pre-crisis period, large trades are
associated with a 0.5% initial price change, whereas during the crisis period the initial
returns are 0.7% for buy trades and –0.75% for sell trades. Returns following large trades
in currency futures are lower than those in equity indexes and gold futures (Figures 2.4.
and 2.5.). Both the initial returns and cumulative returns after block trades in the currency
futures markets show that euro futures are more liquid than the British pound futures. For
example during the crisis period, the initial returns are 0.35 and –0.49% after the large
buy and sell trades, respectively, of British pound futures, whereas in the euro currency
49

futures market the initial returns on average were 0.33% and –0.40% for large buy and
sell trades, respectively.
2.5.2. Bid–Ask Spreads around Large Trades
In this section, the effects of large trades on the liquidity in futures markets in
terms of the bid–ask spreads are examined. Using equation (2.4.) the mean excess spreads
before and after large trades are computed and reported in Tables 2.6.–2.9. Consistent
with the results of previous studies, these results show that block trades cause bid–ask
spreads to widen. The results for the crisis period exhibit three major differences from the
pre-crisis period. First, the bid–ask spreads widen much more after block trades during
the crisis period. Second, there is a difference in the number of trades it takes for bid–ask
spreads to return to their levels prior to the block trades. Specifically, during the crisis
period it takes more trades for the liquidity level to recover from the adverse effects of
block trades. Finally, block purchases and sales show asymmetrical effects during the
crisis period, when the effects of block sales on bid–ask spreads are larger than those of
block purchases. In fact, more trades are required to restore liquidity to pre-block trade
levels after block sales than to restore liquidity after block purchases
Our results show liquidity recovers in currency contracts faster than in the equity
index and gold futures (Figures 2.6.–2.15.) and that the euro futures contract is the most
resilient futures contract. In the euro currency futures market during the pre-crisis period,
liquidity reverts back to the pre-block trade level after 7 trades (Figures 2.12. and 2.13.).
However, during the crisis period liquidity recovers after 10 trades following large
purchases, whereas it takes 11 trades to recover after large block sales.
50

The British pound futures contract is the second-most resilient futures contract in
our sample, after euro futures. In the British pound futures market during the pre-crisis
period, liquidity recovers following block transactions after 8 trades (Figures 2.14. and
2.15.). In the crisis period following large purchases the bid-ask spreads remain above
average levels for 10 trades. After large sales it takes 12 trades until liquidity returns to
pre-block trade levels.
The gold futures market is the least resilient market in our sample (Figures 2.10.
and 2.11.). Even during the pre-crisis period, bid–ask spreads stay above average levels
for 12 trades following block trades. The adverse effects of the crisis on the liquidity of
gold futures can be seen in Figures 2.10 and 2.11. For example during the crisis period, it
takes 15 trades until liquidity is recovered following large purchases, whereas liquidity is
recovered after 17 trades following large sales.
Our results show that the E-mini S&P 500 and E-mini NASDAQ 100 futures
markets exhibit similar resiliencies (Figures 2.6–2.9.). Specifically, after block trades
liquidity recovers in 9 trades in these markets during the pre-crisis period, whereas during
the crisis period the E-mini S&P 500 futures market shows slightly more resiliency than
the E-mini NASDAQ 100 futures market, with liquidity recovering after block purchases
in 12 trades for the former as opposed to 13 trades for the latter. After block sales, the
bid–ask spreads return to normal levels in 14 and 15 trades for E-mini S&P 500 and E-
mini NASDAQ 100 contracts, respectively.
51

2.6. Conclusion
Understanding how markets respond to large trades is important not only to
traders who want to minimize the price impacts of their transactions but also to regulators
who establish the rules for well-functioning markets. Although studies exist that analyze
the price impact of trades in U.S. markets, no previous studies compare the speed of the
adjustment process after large trades in volatile versus normal times in electronic U.S.
futures markets. This study fills that gap in the literature by using high-frequency quote
and trade data from U.S. electronic futures markets to compare the effects of block trades
on quote returns and bid-ask spreads during volatile and less volatile periods. Our results
show that the effects of block trades are larger during the volatile period of the financial
crisis used for this study compared to the pre-crisis period. Specifically, more trades are
required for prices to adjust to a new equilibrium and liquidity to recover after large
trades during the crisis period than during the pre-crisis period. Moreover, during the
crisis period the effects of block sales are larger than the effects of block purchases.
However, during the pre-crisis period, the effects of purchases and sales are similar. This
study could be extended using ETF, options, and less liquid futures in order to compare
the speed of adjustment processes in different and less liquid instruments.
52

Table 2.1. – Descriptive Statistics
|     |     |                 |     |                   |     |       |     |
| --- | --- | --------------- | --- | ----------------- | --- | ----- | --- |
|     |     | E-mini S&P 500  |     | E-mini NASDAQ 100 |     | Gold  |     |
|     |     |                 |     |                   |     |       |     |
Period         Crisis  Pre-Crisis             Crisis     Pre-Crisis  Crisis  Pre-Crisis
Average size of purchases  6.76  11.5  5.44  9.84  2.78  4.11
Average size of block purchases  41.77  56.03  37.22  44.37  14.55  19.06
Number of block purchases per day  882.70  498.94  774.43  453.72  245.97  214.22
| Average size of sales  |     | 6.87  | 11.31  | 5.63  | 9.68  | 3.02  | 4.01  |
| ---------------------- | --- | ----- | ------ | ----- | ----- | ----- | ----- |
Average size of block sales  48.44  56.51  42.48  43.96  17.35  18.93
Number of block sales per day  909.82  487.78  847.32  448.28  266.26  211.74
|                            |     | Euro  |       | British Pound  |          |     |     |
| -------------------------- | --- | ----- | ----- | -------------- | -------- | --- | --- |
| Average size of purchases  |     | 5.23  | 9.14  | 4.45           | 8.74     |     |     |
Average size of block purchases  29.37  36.04  24.31  32.43
Number of block purchases per day  672.48  572.29  612.49  542.18
| Average size of sales  |     | 5.61  | 8.97  | 4.92  | 8.66     |     |     |
| ---------------------- | --- | ----- | ----- | ----- | -------- | --- | --- |
Average size of block sales  36.22  35.47  31.14  31.48
Number of block sales per day  714.67  575.12  633.51  537.62
This table contains sample characteristics for the following electronically traded futures contracts: E-mini S&P 500, E-mini NASDAQ-100, gold,
British pound, and the euro. The trades are categorized into trade groups based on the percentiles of the empirical trade size distribution.
Transactions with a trade size equal to or larger than the 90th percentile are classified as  block trade.
53

|     | Table 2.2. - Quote Returns around Large Sales  |     |     |     |     |
| --- | ---------------------------------------------- | --- | --- | --- | --- |

|     |     |     Trade Relative to Block Trade (t=0)  |     |     |     |
| --- | --- | ---------------------------------------- | --- | --- | --- |

|     |     | –2  | –1  | 0  1 | 2   |
| --- | --- | --- | --- | ---- | --- |
E-Mini S&P
(Pre-Crisis)  Mean Excess Return  –0.01 0.01 –0.29  –0.05 –0.02
|     | t-value: Excess return = 0  | –1.4 | 1.6 | –40.2  –4.5 | –4.4 |
| --- | --------------------------- | ---- | --- | ----------- | ---- |
E-Mini S&P
| (Crisis)  | Mean Excess Return          | –0.01 | -0.01 | –0.62  –0.09 | –0.04 |
| --------- | --------------------------- | ----- | ----- | ------------ | ----- |
|           | t-value: Excess return = 0  | –1.8  | -1.7  | –45.3  –9.8  | –4.6  |
E-Mini NASDAQ
(Pre-Crisis)  Mean Excess Return  –0.01 –0.01 –0.44  –0.04 –0.02
|     | t-value: Excess return = 0  | –0.8 | –1.2 | –47.4  –4.9 | –3.3 |
| --- | --------------------------- | ---- | ---- | ----------- | ---- |
E-Mini NASDAQ
| (Crisis)  | Mean Excess Return          | 0.01 | –0.02 | –0.65  –0.11 | –0.06 |
| --------- | --------------------------- | ---- | ----- | ------------ | ----- |
|           | t-value: Excess return = 0  | 0.9  | –1.5  | –54.2  –7.5  | –5.3  |
Gold (Pre-Crisis)  Mean Excess Return  0.01 –0.01 –0.51  –0.05 – 0.02
|     | t–value: Excess return = 0 | 0.6 | –0.9 | –45.2  –6.2 | –3.4 |
| --- | -------------------------- | --- | ---- | ----------- | ---- |
Gold (Crisis)  Mean Excess Return  –0.01 0.02 –0.69  –0.16 –0.06
|     | t-value: Excess return = 0  | –1.3 | 1.6 | –52.8  –14.4 | –8.3 |
| --- | --------------------------- | ---- | --- | ------------ | ---- |
Euro (Pre-Crisis)  Mean Excess return  –0.02 –0.01 –0.23  –0.03 –0.02
|     | t-value: Excess return = 0  | –2.5 | –1.3 | –28.3  –4.5 | –3.1 |
| --- | --------------------------- | ---- | ---- | ----------- | ---- |
Euro (Crisis)  Mean Excess Return  –0.01 –0.01 –0.42  –0.07 –0.04
|     | t-value: Excess return = 0  | –1.9 | –2.2 | –48.8  –7.5 | –7.2 |
| --- | --------------------------- | ---- | ---- | ----------- | ---- |
British Pound
(Pre-Crisis)  Mean excess trade size  –0.01 0.01 –0.24  –0.04 –0.03
|     | t-value: Excess return = 0  | –1.3 | 0.8 | –26.5  –4.7 | –3.6 |
| --- | --------------------------- | ---- | --- | ----------- | ---- |
British Pound
| (Crisis)  | Mean Excess Return  | –0.03 | –0.01 | –0.49  –0.09 | –0.05 |
| --------- | ------------------- | ----- | ----- | ------------ | ----- |

|     | t-value: Excess return = 0  | –1.5 | –0.9 | –49.5  –9.7 | –9.5 |
| --- | --------------------------- | ---- | ---- | ----------- | ---- |
Quote-to-quote returns are computed from one bid quote to the next bid quote for sales.
The excess return for quote 0 relative to the block trade is defined as the excess return
from the prevailing quote to the block trade. The excess return for quote +1 is defined as
the excess return from the block trade to the first quote after the block trade.

54

   Table 2.3. – Quote Returns around Large Purchases
|     |     |     | Trade Relative to Block Trade (t=0)  |       |     |
| --- | --- | --- | ------------------------------------ | ----- | --- |
|     |     |     | -2  –1                               | 0  1  | 2   |
E-Mini S&P
(Pre-Crisis)  Mean Excess Return  0.02  0.01  0.31  0.03  0.02
|     | t-value: Excess return = 0  |     | 0.8  1.2  | 40.3  8.5  | 8.4  |
| --- | --------------------------- | --- | --------- | ---------- | ---- |
E-Mini S&P (Crisis)  Mean Excess Return  –0.01  0.01  0.46  0.04  0.04
|     | t-value: Excess return = 0  |     | –0.7  0.8  | 35.3  5.1  | 5.2  |
| --- | --------------------------- | --- | ---------- | ---------- | ---- |
E-Mini NASDAQ
(Pre-Crisis)  Mean Excess Return  –0.02  0.01  0.42  0.04  0.03
|     | t-value: Excess return = 0  |     | –1.3  0.7  | 49.5  9.1  | 7.3  |
| --- | --------------------------- | --- | ---------- | ---------- | ---- |
E-Mini NASDAQ
| (Crisis)  | Mean Excess Return          |     | 0.01  –0.01  | 0.56  0.05  | 0.03  |
| --------- | --------------------------- | --- | ------------ | ----------- | ----- |
|           | t-value: Excess return = 0  |     | 1.8  –1.7    | 43.5  4.6   | 3.9   |
Gold (Pre-Crisis)  Mean Excess Return  –0.01  –0.01  0.49  0.04  0.02
|     | t-value: Excess return = 0  |     | –0.7  –0.4  | 44.1  10.4  | 4.2  |
| --- | --------------------------- | --- | ----------- | ----------- | ---- |
Gold (Crisis)  Mean Excess Return  0.02  0.01  0.71  0.06  0.05
|     | t-value: Excess return = 0  |     | 1.6  1.2  | 53.4  14.1  | 13.9  |
| --- | --------------------------- | --- | --------- | ----------- | ----- |
Euro (Pre-Crisis)  Mean Excess Return  –0.01  0.01  0.32  0.03  0.01
|     | t-value: Excess return = 0  |     | –0.9  0.5  | 29.2  6.7  | 6.1  |
| --- | --------------------------- | --- | ---------- | ---------- | ---- |
Euro (Crisis)  Mean Excess Return  0.01  0.01  0.44  0.03  0.03
|     | t-value: Excess return=0  |     | 1.1  1.2  | 47.2  7.5  | 7.2  |
| --- | ------------------------- | --- | --------- | ---------- | ---- |
British Pound
(Pre-Crisis)  Mean Excess Return  –0.01  0.01  0.34  0.03  0.03
|     | t-value: Excess return = 0  |     | –1.1  1.4  | 27.1  11.5  | 11.2  |
| --- | --------------------------- | --- | ---------- | ----------- | ----- |
British Pound (Crisis)
|     | Mean Excess Return  |     | –0.01  –0.01  | 0.49  0.03  | 0.02  |
| --- | ------------------- | --- | ------------- | ----------- | ----- |

|     | t-value: Excess return = 0  |     | –1.4  –0.8  | 50.3  7.9  | 7.4  |
| --- | --------------------------- | --- | ----------- | ---------- | ---- |
Quote-to-quote returns are computed from ask quote to ask quote for purchases. The
excess return for quote 0 relative to the block trade is defined as the excess return from
the prevailing quote to the block trade. The excess return for quote +1 is defined as the
excess return from the block trade to the first quote after the block trade.
55

56

57

58

|       | Table 2.4. – Bid-Ask Spreads around Large Sales  |     |     |     |     |     |
| ----- | ------------------------------------------------ | --- | --- | --- | --- | --- |
Trade Relative to Block Trade

|              |                 | –2    | –1    | 0      | 1     | 2     |
| ------------ | --------------- | ----- | ----- | ------ | ----- | ----- |
| E-Mini S&P   | Bid–Ask Spread  | 0.251 | 0.282 | 0.452  | 0.448 | 0.447 |
(Pre-Crisis)  Mean Excess Spread  –0.019 0.012 0.182  0.178 0.177
|             | t-value: Excess Spread = 0 | –0.6  | 1.4   | 8.3    | 8.5   | 8.4   |
| ----------- | -------------------------- | ----- | ----- | ------ | ----- | ----- |
| E-Mini S&P  | Bid–Ask Spread             | 0.431 | 0.409 | 0.982  | 0.954 | 0.942 |
(Crisis)
|     | Mean Excess Spread  | –0.019 | –0.041 | 0.532  | 0.504 | 0.492 |
| --- | ------------------- | ------ | ------ | ------ | ----- | ----- |

|     | t-value: Excess Spread = 0 | 1.6 | –0.8 | 17.2  | 15.1 | 14.3 |
| --- | -------------------------- | --- | ---- | ----- | ---- | ---- |
|     |                            | 03  | 03   | 03    | 03   | 03   |
E-Mini Nasdaq
|     | Bid–Ask Spread  | 0.289 | 0.285 | 0.541  | 0.537 | 0.533 |
| --- | --------------- | ----- | ----- | ------ | ----- | ----- |
(Pre-Crisis)
|     | Mean Excess Spread         | –0.011 | –0.015 | 0.241  | 0.237 | 0.233 |
| --- | -------------------------- | ------ | ------ | ------ | ----- | ----- |
|     | t-value: Excess Spread = 0 | –0.8   | –1.2   | 9.7    | 8.9   | 9.3   |
E-Mini Nasdaq  Bid–Ask Spread  0.583 0.488 1.022  1.027 0.962
(Crisis)
|     | Mean Excess Spread         | 0.053 | –0.042 | 0.492  | 0.497 | 0.432 |
| --- | -------------------------- | ----- | ------ | ------ | ----- | ----- |
|     |                            |       |        |        | 12.6  |       |
|     | t-value: Excess Spread = 0 | 1.8   | –1.7   | 13.5   |       | 12.7  |
|     |                            | 0011  | 0011   | 0011   | 0011  | 0011  |
Gold (Pre-Crisis)
|     | Bid–Ask Spread             | 0.0101          | 0.0103 | 0.0174  | 0.0178 | 0.0175 |
| --- | -------------------------- | --------------- | ------ | ------- | ------ | ------ |
|     | Mean Excess Spread         | –0.0009 –0.0007 |        | 0.0064  | 0.0068 | 0.0065 |
|     | t-value: Excess Spread = 0 | –1.3            | –1.1   | 11.4    | 12.3   | 11.7   |
Gold (Crisis)  Bid–Ask Spread  0.0162 0.0171 0.0346  0.0362 0.0354

|     | Mean Excess Spread  | –0.0018 –0.0009 |     | 0.0166  | 0.0182 | 0.0174 |
| --- | ------------------- | --------------- | --- | ------- | ------ | ------ |

|     | t-value: Excess Spread = 0 | –1.6 | –1.2 | 13.4  | 14.1 | 13.9 |
| --- | -------------------------- | ---- | ---- | ----- | ---- | ---- |
Euro (Pre-Crisis)
|     | Bid–Ask Spread             | 0.025  | 0.023  | 0.052  | 0.055 | 0.054 |
| --- | -------------------------- | ------ | ------ | ------ | ----- | ----- |
|     | Mean Excess Spread         | –0.002 | –0.004 | 0.025  | 0.028 | 0.027 |
|     | t-value: Excess Spread = 0 | –2.3   | –3.9   | 8.8    | 7.5   | 7.2   |
Euro (Crisis)  Bid–Ask Spread  0.044 0.041 0.095  0.099 0.097

|     | Mean Excess Spread  | –0.009 | –0.012 | 0.042  | 0.046 | 0.044 |
| --- | ------------------- | ------ | ------ | ------ | ----- | ----- |

|     | t-value: Excess Spread = 0 | –2.1 | –2.4 | 8.8  | 7.5  | 7.2  |
| --- | -------------------------- | ---- | ---- | ---- | ---- | ---- |
|     |                            | 0029 | 0029 | 0029 | 0029 | 0029 |
British Pound
|     | Bid–Ask Spread  | 0.021 | 0.022 | 0.057  | 0.061 | 0.059 |
| --- | --------------- | ----- | ----- | ------ | ----- | ----- |
(Pre-Crisis)
|     | mean excess trade size     | –0.008 | –0.007 | 0.028  | 0.032 | 0.030 |
| --- | -------------------------- | ------ | ------ | ------ | ----- | ----- |
|     | t-value: Excess Spread = 0 | –2.3   | –2.1   | 6.5    | 7.5   | 7.2   |
British Pound  Bid–Ask Spread  0.042 0.052 0.103  0.106 0.105
(Crisis)
|     | mean excess trade size  | –0.015 | –0.005 | 0.046  | 0.049 | 0.048 |
| --- | ----------------------- | ------ | ------ | ------ | ----- | ----- |

|     | t-value: Excess Spread = 0 | –2.3 | –0.9 | 10.5  | 10.9 | 10.7 |
| --- | -------------------------- | ---- | ---- | ----- | ---- | ---- |
Excess spreads are spreads in excess of a benchmark level, computed using spreads -20 through -
11 relative to trades of a given size. For excess spreads, reported results include Mean excess
spread and t: Excess spread = 0 (the t-statistic for the test of the null hypothesis that the mean
excess spread equals zero)
59

        Table 2.5. – Bid-Ask Spreads around Large Purchases
|         |     |                 Trade Relative to Block  Trade (t=0)  |     |       |        |        |            |
| ------- | --- | ----------------------------------------------------- | --- | ----- | ------ | ------ | ---------- |
|         |     | –2                                                    |     |    –1 | 0      | 1      |         2  |
| E-Mini  |     | 0.251                                                 |     | 0.282 | 0.452  | 0.448  | 0.447      |
Bid–Ask Spread
S&P
|     |     | –0.019 |     | 0.012 | 0.182  | 0.178  | 0.177 |
| --- | --- | ------ | --- | ----- | ------ | ------ | ----- |
Mean Excess Spread
 (Pre-
|     | t-value: Excess Spread = 0  | –0.6 |     | 1.4 | 8.3  | 8.5  | 8.4 |
| --- | --------------------------- | ---- | --- | --- | ---- | ---- | --- |
Crisis)
E-Mini
|     | Bid–Ask Spread  | 0.422 |     | 0.473 | 0.945  | 0.949  | 0.938 |
| --- | --------------- | ----- | --- | ----- | ------ | ------ | ----- |
S&P
|     | Mean Excess Spread  | –0.028 |     | 0.023 | 0.495  | 0.499  | 0.488 |
| --- | ------------------- | ------ | --- | ----- | ------ | ------ | ----- |
(Crisis)
|         | t-value: Excess Spread = 0  | –1.8  |     | 1.6   | 10.2   | 8.5    | 8.4   |
| ------- | --------------------------- | ----- | --- | ----- | ------ | ------ | ----- |
|         |                             |       | 03  | 03    | 03     | 03     | 03    |
| E-Mini  | Bid–Ask Spread              | 0.289 |     | 0.285 | 0.541  | 0.537  | 0.533 |
Nasdaq
|     | Mean Excess Spread  | –0.011 |     | –0.015 | 0.241  | 0.237  | 0.233 |
| --- | ------------------- | ------ | --- | ------ | ------ | ------ | ----- |
(Pre-
|     | t-value: Excess Spread = 0  | –0.8 |     | –1.2 | 9.7  | 8.9  | 9.3 |
| --- | --------------------------- | ---- | --- | ---- | ---- | ---- | --- |
Crisis)
E-Mini
|     | Bid–Ask Spread  | 0.521 |     | 0.512 | 0.932  | 0.961  | 0.964 |
| --- | --------------- | ----- | --- | ----- | ------ | ------ | ----- |
Nasdaq
|     | Mean Excess Spread  | –0.009 |     | –0.018 | 0.402  | 0.431  | 0.434 |
| --- | ------------------- | ------ | --- | ------ | ------ | ------ | ----- |
(Crisis)
|       | t-value: Excess Spread = 0  | –0.9   |      | –1.5   | 8.4     | 8.9     | 9.3    |
| ----- | --------------------------- | ------ | ---- | ------ | ------- | ------- | ------ |
|       |                             |        | 0011 | 0011   | 0011    | 0011    | 0011   |
| Gold  | Bid–Ask Spread              | 0.0101 |      | 0.0103 | 0.0174  | 0.0178  | 0.0175 |
(Pre-
|     | Mean Excess Spread  | –0.0009 |     | –0.0007 | 0.0064  | 0.0068  | 0.0065 |
| --- | ------------------- | ------- | --- | ------- | ------- | ------- | ------ |
Crisis)
|     | t-value: Excess Spread = 0  | –1.3 |     | –1.1 | 11.4  | 12.3  | 11.7 |
| --- | --------------------------- | ---- | --- | ---- | ----- | ----- | ---- |
Gold
|     | Bid–Ask Spread  | 0.0154 |     | 0.0174 | 0.0316  | 0.0342  | 0.0324 |
| --- | --------------- | ------ | --- | ------ | ------- | ------- | ------ |
(Crisis)
|     | Mean Excess Spread  | –0.0026 |     | –0.0006 | 0.0138  | 0.0162  | 0.0144 |
| --- | ------------------- | ------- | --- | ------- | ------- | ------- | ------ |

|        | t-value: Excess Spread = 0  |       | 2.3 | 1.2   | 8.3    | 8.4    | 9.3   |
| ------ | --------------------------- | ----- | --- | ----- | ------ | ------ | ----- |
| Euro   | Bid–Ask Spread              | 0.025 |     | 0.023 | 0.052  | 0.055  | 0.054 |
(Pre-
|     | Mean Excess Spread  | –0.002 |     | –0.004 | 0.025  | 0.028  | 0.027 |
| --- | ------------------- | ------ | --- | ------ | ------ | ------ | ----- |
Crisis)
|     | t-value: Excess Spread =  | –2.3 |     | –3.9 | 8.8  | 7.5  | 7.2 |
| --- | ------------------------- | ---- | --- | ---- | ---- | ---- | --- |
Euro
|     | Bid–Ask Spread  | 0.046 |     | 0.042 | 0.088  | 0.096  | 0.094 |
| --- | --------------- | ----- | --- | ----- | ------ | ------ | ----- |
(Crisis)
|          | Mean Excess Spread        | –0.007 |     | –0.011 | 0.035  | 0.043  | 0.041 |
| -------- | ------------------------- | ------ | --- | ------ | ------ | ------ | ----- |
|          | t-value: Excess Spread =  |        |     |        |        |        |       |
|          |                           | –1.9   |     | –2.2   | 8.8    | 7.5    | 7.2   |
|          |                           | 0029   |     | 0029   | 0029   | 0029   | 0029  |
| British  | Bid–Ask Spread            | 0.021  |     | 0.022  | 0.057  | 0.061  | 0.059 |
Pound
|     | Mean Excess Spread  | –0.008 |     | –0.007 | 0.028  | 0.032  | 0.030 |
| --- | ------------------- | ------ | --- | ------ | ------ | ------ | ----- |
(Pre-
|     | t-value: Excess Spread =  | –2.3 |     | –2.1 | 6.5  | 7.5  | 7.2 |
| --- | ------------------------- | ---- | --- | ---- | ---- | ---- | --- |
Crisis)
British
|     | Bid–Ask Spread  | 0.047 |     | 0.048 | 0.094  | 0.097  | 0.095 |
| --- | --------------- | ----- | --- | ----- | ------ | ------ | ----- |
Pound
|     | Mean Excess Spread  | –0.010 |     | –0.009 | 0.037  | 0.040  | 0.038 |
| --- | ------------------- | ------ | --- | ------ | ------ | ------ | ----- |
(Crisis)
|     | t-value: Excess Spread =  | –2.1 |     | –1.9 | 9.2  | 9.7  | 9.5 |
| --- | ------------------------- | ---- | --- | ---- | ---- | ---- | --- |
Excess spreads are spreads in excess of the benchmark level, computed using spreads -20 through
-11 relative to trades of a given size. For excess spreads; reported results include the Mean Excess
Spread and t: Excess spread = 0 (the t-statistic for the test of the null hypothesis that the mean
| excess spread equals zero).  |     |     |     |     |     |     |     |
| ---------------------------- | --- | --- | --- | --- | --- | --- | --- |
60

61

62

63

64

65

CHAPTER 3: COMPONENTS OF QUOTED BID-ASK SPREADS IN U.S
ELECTRONIC FUTURES MARKETS
3.1. Introduction
The bid-ask spread represents a major component of a trader’s transactions cost.
Much of the literature finds that bid-ask spreads reflect the three costs that market makers
incur: order processing costs (Roll 1984), adverse selection costs (Kyle 1985; Glosten
and Milgrom; 1985; and Glosten 1994), and inventory costs (Stoll 1978). Several studies
concerning bid-ask spreads focus their analyses on the empirical determinants of bid-ask
spreads in the equity markets (Roll 1984; Glosten and Milgrom, 1985; Glosten, 1987;
Glosten and Harris, 1988; Copeland and Galai, 1983; Haller and Stoll, 1989; Stoll, 1989;
George, Kaul, and Nimalendran, 1991; McInish and Wood, 1992; Huang and Stoll 1997).
Whereas previous studies focused on the behaviour and components of bid-ask spreads in
U.S. equity markets, no studies exist in the literature analyzing bid ask spreads in U.S.
electronic futures markets.
In this study, I analyze how adverse selection, order processing, and inventory
holding costs affect bid–ask spreads for a wide spectrum of futures contracts in both
volatile and less volatile periods. The purpose of this study is to understand how market
makers adjust quotes during different market conditions. These bid-ask spreads are
decomposed into their components using Huang and Stoll’s (1997) model. According to
Van Ness et al. (2001), Huang and Stoll’s method accurately captures the adverse
selection component of the spread without being affected by the instrument’s price
66

volatility. This property of Huang and Stoll’s technique makes it particularly suitable for
this study, since adverse selection costs are measured for both volatile and less volatile
periods.
This study contributes to the literature by comparing for the first time the three
cost components for equity index, currency, and precious metal futures during volatile (in
this case, the financial crisis of 2008) and less volatile periods (the pre-crisis period),
using intraday, high-frequency data from five different futures contracts that are
electronically traded in U.S. markets.
Our results show that during the more volatile period of 2008, market makers
increase bid–ask spreads, mostly because of the increased risks associated with
information asymmetry (calculated as adverse selection costs) and inventory holding
costs. However, we find that order processing costs represent the largest component of
bid–ask spread in both periods.
3.2. Literature Review
Several studies show that market makers widen spreads when information arrival
is suspected. Kyle’s (1985) theoretical model is based on informed investors taking
advantage of uninformed investors and profiting from trading on private information
about the value of an asset. Kyle’s model emphasizes the importance of the adverse
selection cost component of the bid-ask spread as it affects dealers and uninformed
liquidity traders. Further empirical research shows that adverse selection costs comprise
an important component of the bid–ask spread in equities markets (Easley and O'Hara,
67

1987; Glosten and Milgrom, 1985; Copeland and Galai, 1983). These studies analyze the
impact of informed traders in a market setting, where the other players are uninformed
traders and market makers. Informed trading has considerable negative impact on market
makers, who therefore inflate bid and ask quotes to compensate for the losses from
informed traders.
Subrahmanyam (1991) extends Kyle’s model to a multi-asset economy setting,
where baskets of stocks are available for trading. Subrahmanyam’s model predicts that
because private information about individual assets plays a smaller role at the portfolio
level, less of an informational disadvantage exists to market makers holding baskets of
stocks; an example of such assets is equity index futures. Neal and Wheatley (1998) find
that although the adverse selection cost component of closed-end funds is indeed smaller
than that of common stocks, the difference is not as great as hypothesized by
Subrahmanyam (1991).
In the market microstructure literature (Kyle 1985; Glosten and Milgrom 1985),
three investor categories are proposed—market makers, informed traders, and liquidity
(uninformed) traders. Market makers, or other limit order investors, possess an information
disadvantage relative to informed investors, whereas liquidity investors trade without
access to private information. To market makers, informed and liquidity investors are
indistinguishable. Informed investors profit from trading with market makers, and
liquidity investors. Market makers post bid–ask quotes wide enough to compensate for
trading with informed investors. Therefore, spreads increase with asymmetric
information.
68

Inventory holding cost is another component of the bid ask spread. As market
makers buy (sell) and as inventory increases (decreases), market makers try to sell (buy)
back, thereby adjusting their quotes in to control order flow and bring inventory back to a
preferred position (Stoll 1978; Amihud and Mendelson 1980; Ho and Stoll 1981; Ho and
Stoll 1983). The third and last component of bid ask spread is order processing cost. The
order processing cost represents a fee charged by market makers for matching buy and
sell orders
In the market microstructure literature of decomposing the bid-ask spread two
classes of models exist: the serial covariance spread estimation model and the order flow
spread estimation model. In the serial covariance spread estimation model the spread
measures are derived from the serial covariance properties of transaction price changes
(the most common empirical serial covariance estimation model was developed by Roll
(1984)). If trade prices fluctuate between bid and ask prices then the observed price
changes become negatively autocorrelated. Roll’s (1984) model estimates the bid-ask
spread based on this negative serial correlation property of transaction prices. In another
class of models, the bid-ask spread is estimated via order flow regression models. Glosten
and Harris (1988) applied this concept to estimate the adverse selection spread
component by developing an order flow transaction costs model. Huang and Stoll (1997)
extend the Roll (1984) and Glosten and Harris (1988) models, by combining order
processing, inventory, and asymmetric information (adverse selection) cost components.
Van Ness, Van Ness, and Warr (2001) show that Huang and Stoll’s method accurately
captures the adverse selection cost component of bid–ask spreads without being affected
69

by market conditions. This study examines the bid–ask spreads of futures contracts using
Huang and Stoll’s (1997) method, reported for the first time in the literature.
3.3. Data
This study employs intraday, high-frequency data from five different futures
contracts that are electronically traded in U.S. markets. Data from different asset classes
and from different time periods are used in order to determine how the bid-ask spreads
behave for different asset classes. Our data set includes the E-mini S&P 500, E-mini
NASDAQ 100 equity index, gold, the British pound, and euro currency futures. The
sample periods include the volatile time span of September 2008 through December
2008, during the financial crisis, as well as the less volatile, pre-crisis period of January
2007 through March 2007.
Trades that occur at the same price, in the same direction (buy or sell), and within
the same minute are aggregated. Nearby contracts are used in the analysis, since they are
the most active contracts. The data source is the CQG transactions database.
3.4. Methodology
I implement the Huang and Stoll (1997) model by first establishing a basic trade
indicator model, then I employ two extensions to distinguish between all three bid–ask
spread components. This technique uses the generalized method of moments to directly
provide consistent estimates of the components of the bid-ask spread. The first part of the
model, the basic trade indicator, makes no assumptions about the conditional probability
of trades and measures the order processing cost. The basic model (explained in more
70

detail later) is based on substituting observable values into the unobservable price, V,
t
which leads to
| (cid:3020) |     | (cid:3020) |     |     |
| ---------- | --- | ---------- | --- | --- |
∆(cid:1842) (cid:3404) (cid:4666)(cid:1843) (cid:3398)(cid:1843) (cid:4667)(cid:3397)(cid:2019) (cid:1843) (cid:3397)(cid:1857)                         (3.1.)
| (cid:3047) | (cid:3047) (cid:3047)(cid:2879)(cid:2869) | (cid:3047)(cid:2879)(cid:2869) (cid:3047) |     |     |
| ---------- | ----------------------------------------- | ----------------------------------------- | --- | --- |
| (cid:2870) |                                           | (cid:2870)                                |     |     |
where S is the estimated traded spread; Q is the trade indicator and takes the value of
–1, or 1, for sell and buy trades respectively. λ = α + β, where α is the adverse selection
cost component and β is the inventory-holding cost component of the bid-ask spread.
From this equation the cost component of the spread that is not due to adverse selection
or inventory holding costs, (1 – λ), which represents the order processing cost component
of the spread.
  In  the  second  part  the  basic  model  is  extended  by  using  the  conditional
expectation  of  the  trade  indicator.  Since  quote  revisions  follow  each  trade,  every
subsequent trade is dependent on the one prior to it. This data serves as a basis for a
probability estimator, π, which is defined as the probability that the current trade is
opposite in sign to the trade that occurred just before. The basic model is extended to
estimate all three cost components of the bid ask spread .
| (cid:1831)(cid:4666)(cid:1843) |(cid:1843)                    | (cid:4667) (cid:4666)	1(cid:3398)2(cid:2024)(cid:4667)(cid:1843) |                                                              |     |            |
| ------------------------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------ | --- | ---------- |
|                                                               | (cid:3404)                                                       |                                                              |     |    (3.2.)  |
| (cid:3047)(cid:2879)(cid:2869) (cid:3047)(cid:2879)(cid:2870) |                                                                  | (cid:3047)(cid:2879)(cid:2870)                               |     |            |
|                                                               | (cid:3020)(cid:3295)(cid:3127)(cid:3117)(cid:1843)               | (cid:3020)(cid:3295)(cid:3127)(cid:3118)(cid:1843)           |     |            |
∆(cid:1839) (cid:3404) (cid:4666)(cid:2009) (cid:3397)(cid:2010)(cid:4667) (cid:3398)(cid:2009)(cid:4666)1(cid:3398)2(cid:2024)(cid:4667) (cid:3397)(cid:2035)                         (3.3.)
| (cid:3047) | (cid:3047)(cid:2879)(cid:2869) |            | (cid:3047)(cid:2879)(cid:2870) (cid:3047) |     |
| ---------- | ------------------------------ | ---------- | ----------------------------------------- | --- |
|            | (cid:2870)                     | (cid:2870) |                                           |     |
where St is the quoted spread at the transaction at time t, M is the midpoint of the bid–
t
ask quote that prevails just before the transaction at time t, Q is the buy–sell indicator for
t
the trade price, P , and π is the probability that the trade at time t is opposite in sign to the
t
71

trade at t – 1. α and β represent the percentage of the half spread attributable to adverse
selection costs and inventory costs respectively. Order processing cost component is
equal to (1 – α – β).
3.5. Results
Utilizing Huang and Stoll’s (1997) method, the bid ask spreads of five futures
contracts are decomposed into three components to examine the pre-crisis and crisis
periods of this study. The contract specifications given in Table 3.1 reflect the size and
thus the risk traders and market makers take with each trade.
Our results in Table 3.2 show that order processing is the largest cost component
of bid–ask spreads in the futures markets examined here. The sum of the adverse
selection and inventory holding costs is smaller than the order processing cost for all five
contracts, during both the pre-crisis and the crisis period. However, order processing
costs decline and the sum of the adverse selection and inventory risk costs increase
during the volatile crisis period as compared with the pre-crisis period. This result shows
that when uncertainty increases in futures markets, market makers increase bid–ask
spreads in response to higher information asymmetry and inventory holding risks. Among
the contracts in our sample, gold futures have the smallest order processing costs (0.68 in
the pre-crisis and 0.58 in the crisis periods), although they also possess the highest
adverse selection and inventory holding costs. Equity index futures are associated with
the least adverse selection and inventory holding costs. Specifically, in the E-mini S&P
futures market the sum of the inventory holding and the adverse selection cost
components are higher than for the E-Mini Nasdaq 100 futures market.
72

Order processing, adverse selection, and inventory holding costs are reported
separately in Table 3.3. In this analysis, sequential trades are not aggregated. The results
reported in this table are consistent with the results reported in Table 3.2. Order
processing costs still represent the largest component of the bid–ask spreads in futures
markets. The second-largest cost component is the inventory holding costs. An exception
is the gold futures adverse selection cost, which are negative due to trade clustering. In
the next section the results are reported after the sequential trades that occur at the same
price without any quote change are combined.
Following Huang and Stoll (1997), who also find negative adverse selection costs
due to trade clustering, we aggregate sequential trades that occur at the same price. Table
3.4. shows the order processing, inventory holding, and adverse selection costs for
sequential trades that occur at the same price, which are aggregated and treated as one
large order. The results show that the gold futures market possesses the highest adverse
selection and inventory holding costs in our sample, both in the pre-crisis and crisis
periods. Consistent with Subrahmanyam (1991), our results show that adverse selection
costs are the smallest, and the order processing costs are the largest components of the
bid–ask spreads for all five futures markets. Moreover, the inventory holding costs are
the second largest component of spreads after order processing costs. During the crisis
period, the order processing cost components of the bid–ask spreads decrease, whereas
the adverse selection and inventory holding cost components increase.
73

3.6. Conclusion
In this study I analyze the bid-ask spread components of a wide spectrum of
futures contracts, in both volatile and less volatile periods, in order to understand how
market makers adjust quotes during different market conditions. The cost components of
bid–ask spreads are analyzed using intraday, high-frequency data from five different
futures contracts that are electronically traded in U.S. markets to understand how market
makers adjust quotes during different market conditions.
Our results show that during more volatile periods, market makers increase bid–
ask spreads, mostly because of the increased risks associated with information
asymmetry, calculated as adverse selection costs, and inventory holding costs. Although
adverse selection and inventory holding costs are higher during the crisis period as
compared with the pre-crisis period, order processing costs represent the largest cost
component of bid–ask spread in both periods.
A theoretical model predicts that in markets using baskets of securities, adverse
selection costs are diversified away (Subrahmanyam 1991). However, there is no prior
empirical study that tests this hypothesis using data from U.S. electronic futures markets.
Among the contracts we analyzed, our results show that the adverse selection cost
component of equity index futures bid–ask spreads are smaller than those of gold and
currency futures. Adverse selection and inventory holding cost components are larger for
gold futures than for the equity index and currency futures.
74

  This study can be extended in the future to compare adverse selection, inventory
holding and order processing costs in different markets and subsequent time periods,
especially using data from options markets and data from the post-crisis period.

Table 3.1: Contract Specifications
This table reports the contract specifications of the five different futures contracts in this
study.
Contract  Tick Size (Pts.)  Contract Size  Point Value (US$)
| E-Mini S&P 500     | 0.25    | $50 times the index  | 50      |
| ------------------ | ------- | -------------------- | ------- |
| E-Mini NASDAQ 100  | 0.25    | $20 times the index  | 20      |
| Gold               | 0.10    | 100 troy ounces      | 100     |
| Euro               | 0.0001  | EUR 125,000          | 125,000 |
| British Pound      | 0.0001  | GBP 62,500           | 62,500  |

75

Table 3.1. Traded Spread and Order Processing Cost Components
|     |     |     |     |     |     | (cid:3020) |     |     | (cid:3020) |     |
| --- | --- | --- | --- | --- | --- | ---------- | --- | --- | ---------- | --- |
This table reports the results from estimating ∆(cid:1842) (cid:3404) (cid:4666)(cid:1843) (cid:3398)(cid:1843) (cid:4667)(cid:3397)(cid:2019) (cid:1843) (cid:3397)(cid:1857) . The
|     |     |     |     |     | (cid:3047) | (cid:3047) | (cid:3047)(cid:2879)(cid:2869) |     | (cid:3047)(cid:2879)(cid:2869) | (cid:3047) |
| --- | --- | --- | --- | --- | ---------- | ---------- | ------------------------------ | --- | ------------------------------ | ---------- |
|     |     |     |     |     |            | (cid:2870) |                                |     | (cid:2870)                     |            |
results show the estimated traded spread (S) and the proportion of bid-ask spread due to
adverse selection and inventory holding (λ) costs. The proportion of the traded spread due
to order processing is calculated as 1 – λ.
|     | S (Estimated Spread)  |     |     |     | Λ (Sum of Adverse        |     |     |     | 1-λ (Order        |     |
| --- | --------------------- | --- | --- | --- | ------------------------ | --- | --- | --- | ----------------- | --- |
|     |                       |     |     |     | Selection and Inventory  |     |     |     | Processing Cost)  |     |
Holding Cost)
|             |     |         |         |     |         |         |     |         |     |         |
| ----------- | --- | ------- | ------- | --- | ------- | ------- | --- | ------- | --- | ------- |
|             |     | Pre-    | Crisis  |     | Pre-    | Crisis  |     | Pre-    |     | Crisis  |
|             |     | Crisis  |         |     | Crisis  |         |     | Crisis  |     |         |
| E-Mini S&P  |     | 0.270   | 0.450   |     | 0.11    | 0.19    |     | 0.89    |     | 0.81    |

| E-Mini  |     | 0.300  | 0.530  |     | 0.14  | 0.23  |     | 0.86  |     | 0.77  |
| ------- | --- | ------ | ------ | --- | ----- | ----- | --- | ----- | --- | ----- |
NASDAQ

| Gold           |     | 0.010  | 0.018  |     | 0.32  | 0.42  |     | 0.68  |     | 0.58  |
| -------------- | --- | ------ | ------ | --- | ----- | ----- | --- | ----- | --- | ----- |
|                |     |        |        |     |       |       |     |       |     |       |
| Euro           |     | 0.026  | 0.052  |     | 0.17  | 0.28  |     | 0.83  |     | 0.72  |
|                |     |        |        |     |       |       |     |       |     |       |
| British Pound  |     | 0.029  | 0.057  |     | 0.19  | 0.31  |     | 0.81  |     | 0.69  |
|                |     |        |        |     |       |       |     |       |     |       |
|                |     |        |        |     |       |       |     |       |     |       |
|                |     |        |        |     |       |       |     |       |     |       |
|                |     |        |        |     |       |       |     |       |     |       |
|                |     |        |        |     |       |       |     |       |     |       |
|                |     |        |        |     |       |       |     |       |     |       |
|                |     |        |        |     |       |       |     |       |     |       |
|                |     |        |        |     |       |       |     |       |     |       |
|                |     |        |        |     |       |       |     |       |     |       |
|                |     |        |        |     |       |       |     |       |     |       |
|                |     |        |        |     |       |       |     |       |     |       |
76

  Table 3.3. Components of the Bid–Ask Spreads, Estimates Based on Serial Correlation in Trade Flows
This table reports the results from computing the extended model, which is based on serial correlation in trade flows. The
extended  model  is  used  to  simulatenously  estimate  the  three  components  of  the  bid–ask  spread: adverse  selection  (α),
inventory holding (β), and order processing (1-α-β). The extended model consists of the following equations
|  (cid:1831)(cid:4666)(cid:1843) | |(cid:1843) (cid:4667) (cid:3404)                   | (cid:4666)1(cid:3398)2(cid:2024)(cid:4667)(cid:1843)           | (cid:3397)(cid:2013)                               |                                           |     |     |     |     |     |
| ------------------------------- | --------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------- | ----------------------------------------- | --- | --- | --- | --- | --- |
| (cid:3047)(cid:2879)(cid:2869)  | (cid:3047)(cid:2879)(cid:2870)                      |                                                                | (cid:3047)(cid:2879)(cid:2870) (cid:3047)          |                                           |     |     |     |     |     |
|                                 | (cid:3020)(cid:3295)(cid:3127)(cid:3117)(cid:1843)  |                                                                | (cid:3020)(cid:3295)(cid:3127)(cid:3118)(cid:1843) |                                           |     |     |     |     |     |
| Δ(cid:1839) (cid:3404)          | (cid:4666)(cid:2009) (cid:3397)(cid:2010)(cid:4667) | (cid:3398)(cid:2009)(cid:4666)1(cid:3398)2(cid:2024)(cid:4667) |                                                    | (cid:3397)(cid:1857) .                    |     |     |     |     |     |
| (cid:3047)                      |                                                     | (cid:3047)(cid:2879)(cid:2869)                                 |                                                    | (cid:3047)(cid:2879)(cid:2870) (cid:3047) |     |     |     |     |     |
|                                 | (cid:2870)                                          |                                                                | (cid:2870)                                         |                                           |     |     |     |     |     |
  α (Adverse Selection)  β (Inventory Holding)             π   1-α-β (Order Processing)
  Pre-Crisis   Crisis  Pre-Crisis   Crisis  Pre-Crisis   Crisis  Pre-Crisis   Crisis
E-Mini S&P  –0.03  –0.01  0.13  0.16  0.31  0.36  0.90  0.85

E-Mini NASDAQ  –0.04  –0.03  0.15  0.17  0.26  0.32  0.89  0.86

| Gold  |     | 0.02   | 0.04   | 0.22  | 0.24  | 0.44  | 0.48  | 0.76  | 0.72  |
| ----- | --- | ------ | ------ | ----- | ----- | ----- | ----- | ----- | ----- |
| Euro  |     | –0.05  | –0.04  | 0.16  | 0.19  | 0.27  | 0.31  | 0.89  | 0.85  |
British Pound  –0.07  –0.02  0.19  0.23  0.22  0.35  0.88  0.79
77

      Table 3.4. Components of the Bid–Ask Spreads, Estimates Based on Serial Correlation in Trade Flows with Trade Clusters
This table reports the results from computing the extended model, which is based on serial correlation in trade flows.
Sequential trades without quote revision are considered as one large order. The extended model is used to simulatenously
estimate the three components of the bid–ask spread: adverse selection (α), inventory holding (β), and order processing (1-α-β).
The extended model consists of the following equations: (cid:1831)(cid:4666)(cid:1843) |(cid:1843) (cid:4667) (cid:3404) (cid:4666)1(cid:3398)2(cid:2024)(cid:4667)(cid:1843) (cid:3397)(cid:2013)  and Δ(cid:1839) (cid:3404) (cid:4666)(cid:2009) (cid:3397)(cid:2010)(cid:4667) (cid:3020)(cid:3295)(cid:3127)(cid:3117)(cid:1843) (cid:3398)
|     |     |     |     | (cid:3047)(cid:2879)(cid:2869) (cid:3047)(cid:2879)(cid:2870) | (cid:3047)(cid:2879)(cid:2870) | (cid:3047) | (cid:3047) | (cid:3047)(cid:2879)(cid:2869) |
| --- | --- | --- | --- | ------------------------------------------------------------- | ------------------------------ | ---------- | ---------- | ------------------------------ |
(cid:2870)
(cid:3020)(cid:3295)(cid:3127)(cid:3118)(cid:1843)
| (cid:2009)(cid:4666)1(cid:3398)2(cid:2024)(cid:4667) (cid:3397)(cid:1857) | .   |     |     |     |     |     |     |     |
| ------------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:3047)(cid:2879)(cid:2870) (cid:3047)
(cid:2870)
  α (Adverse Selection) β (Inventory Holding)  π   1-α-β (Order Processing)
  Pre-Crisis  Crisis  Pre-Crisis  Crisis  Pre-Crisis  Crisis  Pre-Crisis  Crisis
| E-Mini S&P  | 0.01  | 0.02  | 0.18  | 0.22  | 0.52  | 0.56  | 0.81  | 0.76  |
| ----------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |

E-Mini NASDAQ  0.01  0.02  0.20  0.23  0.52  0.59  0.79  0.75

| Gold  | 0.07  | 0.09  | 0.31  | 0.34  | 0.54  | 0.55  | 0.62  | 0.57  |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| Euro  | 0.02  | 0.04  | 0.23  | 0.28  | 0.57  | 0.53  | 0.75  | 0.68  |
British Pound  0.03  0.05  0.25  0.30  0.54  0.59  0.72  0.65
78

REFERENCES
Admati, A., & Pfleiderer, P. (1988). A theory of intraday patterns: Volume and price
variability. Review of Financial Studies 1, 3-40.
Alexander, C., & Barbosa, A. (2008). Hedging index exchange traded funds. Journal of
Banking and Finance 32, 326–337.
Alfonsi, A., Fruth, A., and Schied, A. (2010). Optimal execution strategies in limit order
books with general shape functions. Quantitative Finance, Vol. 10, No. 2, 143-
157.
Amihud, Y., and Mendelson, H. (1980). Dealership market. Journal of Financial
Economics 8, 31-53.
Amihud, Y., & Mendelson, H. (1986). Asset pricing and the bid-ask spread. Journal of
Financial Economics 17, 223–249.
Amihud, Y. (2002). Illiquidity and stock returns: cross-section and time-series effects.
Journal of Financial Markets 5, 31–56.
Anand, A., Irvine, P., Puckett, A., & Venkataraman, K. (2013). Institutional trading and
stock resiliency: Evidence from the 2007-2009 financial crisis. Journal of
Financial Economics 108, 3,773-797.
Anand, A., & Karagozoglu, A. K. (2006). Relative performance of bid-ask spread
estimators: Futures market evidence. Journal of International Financial Markets
Institutions and Money 16, 231-245.
Andersen, T. G., & Bolerslev, T. (1998). Answering the skeptics: Yes, standard volatility
models do provide accurate forecasts. International Economic Review 39, 885–
905.
Ates, A., & Wang, G. H. (2005). Liquidity and price discovery on floor versus
screenbased trading systems: An analysis of foreign exchange futures markets.
Review of Futures Markets 14, 3, 391-419.
Baillie, R., Booth, G., Tse, Y., & Zabotina, T. (2002). Price discovery and common factor
models. Journal of Financial Markets 5, 309–321
79

Berkman, H., Brailsford, T., and Frino, A. (2005), A note on execution costs for stock
index futures: Information versus liquidity effects. Journal of Banking and
Finance, Vol. 29, No. 3, 565-77.
Booth, G. G., So, R. W., & Tse, Y. (1999). Price discovery in the German equity index
derivatives markets. Journal of Futures Markets 19, 619-643.
Brunnermeier, M. (2009). Deciphering the 2007–2008 liquidity and credit crunch.
Journal of Economic Perspectives 23, 77–100.
Brennan, M., Chordia, T., & Subrahmanyam, A. (1998). Alternative factor specifications,
security characteristics, and the cross-section of expected stock returns. Journal of
Financial Economics49, 345 - 373.
Brunnermeier, M., & Pedersen L. H. (2009). Market liquidity and funding liquidity.
Review of Financial Studies 22, 2201-2238.
Chan, K. (1992). A further analysis of the lead-lag relationship between the cash market
and stock index future market. Review of Financial Studies 5, 123-152.
Chiyachantana, C., Jain, P., Jiang, C., and Wood, R. (2004). International evidence on
institutional trading behavior and price impact. Journal of Finance 59, 869-898.
Chiu, J., Chung, H., Keng-Yu, H., & Wang, G.H.K. (2012). Funding liquidity and equity
liquidity in the subprime crisis period: Evidence from the ETF market. Journal of
Banking and Finance 36, 2660-2071.
Chordia, C., Roll, R., & Subrahmanyam, A. (2008). Liquidity and market
efficiency. Journal of Financial Economics 87, 249-268.
Chu, Q. C., Hsieh, W. G., & Tse, Y. (1999). Price discovery on the S&P 500 index
markets: An analysis of spot index, index future and SPDRs. International Review
of Financial Analysis 8, 21-34.
Copeland, T.E., and Galai, D. (1983). Information effects on the bid-ask spread. The
Journal of Finance, 38, 1457-1469.
Coppejans, M., Domowitz, I., and Madhavan, A. (2004). Liquidity in an automated
auction, Working paper, Duke University.
Covrig, V., Ding, D. K., & Low, B. S. (2004). The contribution of a satellite market to
price discovery: Evidence from the Singapore exchange. Journal of Futures
Markets 10, 981-1004.
Cummings, J.R. and Frino, A. (2010), Further analysis of the speed of response to large
trades in interest rate futures. Journal of Futures Markets, Vol. 30, No. 8, 705-724.
80

Deville, L. (2008). Exchange traded funds: History, trading and research. Handbook of
Financial Engineering 1-37.
Easley, D., and O’Hara, M. (1987). Price, trade size, and information in security markets.
Journal of Financial Economics 19, 69-90.
Elton, E. J., Gruber, M. J., Commer, G., & Li, K. (2002). Spiders: Where are the bugs?,
Journal of Business 75, 453-472.
Engle R., & Lange J. (2001). Predicting Vnet: A model of market dynamics of market
depth. Journal of Financial Markets 4, 113-142.
Engle, R., & Russell, J. (1998). Autoregressive conditional duration: a new model for
irregularly spaced data. Econometrica 66, 1127-1162.
Fleming, J., Ostdiek, B., and Whaley, R. E. (1996). Trading costs and the relative rates of
price discovery in stock, futures, and options markets. Journal of Futures
Markets 16, 353-387.
Frino, A., and Oetomo, T. (2005). Slippage in futures markets: Evidence from the Sydney
Futures Exchange. Journal of Futures Markets 25, 12, 1129-1146.
Fleming, J., Ostdiek, B., & Whaley, R.E. (1996). Trading costs and the relative rates of
price discovery in stock, futures, and option markets. Journal of Futures Markets
16, 353–387.
Franke,G., Hess, D. (2000).Information diffusion in electronic and floor trading. Journal
of Empirical Finance 7, 455-478.
Garleanu, N., & Pedersen, L.H. (2007). Liquidity and risk management. American
Economic Review 97, 193-197.
Gemmill, G. (1996). Transparency and liquidity: A study of block trade on the London
Stock Exchange under different publication rules. Journal of Finance 51, 1765-
1790.
Glosten, L., and Milgrom, P. (1985). Bid, ask and transaction prices in a specialist market
with heterogeneously informed traders. Journal of Financial Economics, 13, 71-
100.
Glosten, L. (1994). Is the electronic open limit order book inevitable? Journal of Finance
49, 1127-1161.
Gonzalo, J., & Granger., C. W. J. (1995). Estimation of common long-memory
components in cointegrated systems. Journal of Business and Economic Statistics
13, 27-36.
Gorton, G.B., and Pennacchi, G.G. (1993). Security baskets and index-linked securities,
Journal of Business 66, 1-27.
81

Grammig, J., & Peter, F. (2013). Telltale tails: A new approach to estimating unique
market information shares. Journal of Financial and Quantitative Analysis 48, 2,
459-488.
Grammig, J., Schiereck, D., & Theissen, E. (2001). Knowing me knowing you: Trader
anonymity and informed trading in parallel markets. Journal of Financial Markets
4, 85-412.
Hameed, A., Kang, W., & Viswanthan, S. (2009). Stock market declines and liquidity.
Journal of Finance 65, 257-294.
Hasbrouck, J. (1995). One security, many markets: Determining the contribution to price
discovery. Journal of Finance 50, 1175-99.
Hasbrouck, J. (2003). Intraday price formation in U.S. equity index markets. Journal of
Finance 58, 2375-2400.
Hasbrouck, J. (2004). Liquidity in futures pits: Inferring market dynamics from
incomplete data. Journal of Financial and Quantitative Analysis 2, 305-26.
Hegde, S. P., & McDermott, J. B. (2004). The market liquidity of DIAMONDs, Q’s and
underlying stocks. Journal of Banking and Finance 28, 1043-1067.
Holthausen, R., Leftwich, R., and Mayers, D. (1987). The effects of large block
transaction on security prices: A cross sectional analysis. Journal of Financial
Economics 19, 237-268.
Holthausen, R. (1990). Large block transactions, the speed of response and temporary
and permanent stock price effects. Journal of Financial Economics 26, 71-95.
Hsieh, W. G. (2004). Regulatory changes and information competition: the case of
Taiwan index futures. Journal of Futures Markets 24, 399-412.
Huang, R.D., and Stoll, H.R. (1997). The components of the bid-ask spread: A general
approach. The Review of Financial Studies, 10, 4, 995-1034.
Jacoby, G., Fowler, D. J., & Gottesman, A. A. (2000).The capital asset pricing model and
the liquidity effect: A theoretical approach. Journal of Financial Markets 3, 69–
81.
Jain, P. K. (2005). Financial market design and the equity premium: Electronic vs. floor
Trading. Journal of Finance 60 2955-2985.
Lee, M.C., & Ready, M. J. (1991). Inferring trade direction from intraday data. Journal of
Finance 46, 733-746.
82

Kappi, J., & Siivonen, R. (2000). Market liquidity and depth on two different electronic
trading systems: A comparison of Bund futures trading on the APT and DTB.
Journal of Financial Markets 3, 389-402.
Karazoglu, A. (2011). Direct market access in exchange-traded derivatives: Effects of
algorithmic trading on liquidity in futures markets. Review of Futures Markets 19,
95-142.
Keim, D.B., and Madhaven, A. (1996). The upstairs markets for large-block transactions:
analysis and measurement of price effects. Review of Financial Studies 9, 1-36.
Kraus, A., and Stoll, H.R. (1972). Price impacts of block trading on the New York Stock
Exchange. Journal of Finance 27, 569-588.
Kurov, A., & Lasser, D. (2004). Price dynamics in the regular and e-mini futures
markets. Journal of Financial and Quantitative Analysis 39, 365–384.
Kyle, A.S. (1985). Continuous auctions and insider trading, Econometrica, Vol. 53, No.
6, 1315-1335.
Kyle, A. S., & Obizhaeva, A. (2011). Market microstructure invariants: Theory and
implications of calibration, Working Paper, University of Maryland.
Lee, C.M., Mucklow, B. and Ready, M.J. (1993). Spreads, depths and the impact of
earnings information: an intraday analysis. Review of Financial Studies, Vol. 6,
No. 2, 345-374.
Lee, C., and Radhakrishna, B. (2000). Inferring Investor Behavior: Evidence from TORQ
Data. Journal of Financial Markets, 3, 183-204.
Lee, C., and Ready, M. (1991). Inferring trade direction from intraday data. Journal of
Finance 46, 733-746.
Locke, P. R., & Venkatesh, P. C. (1997). Futures market transaction costs. Journal of
Futures Markets 17, 229-245.
Martens, M. (1998). Price discovery in high and low volatility periods: Open-outcry
versus electronic trading. Journal of International Financial Markets. Institutions,
and Money 8, 243–260.
Martikainen, T., & Puttonen, V. (1994). International price discovery in Finnish stock
index futures and cash markets. Journal of Banking and Finance 18, 809-822.
Neal, R., and Wheatley, S. (1998). Adverse selection and bid-ask spreads: Evidence from
closed- end funds, Journal of Financial Markets, 1, 121–149.
O’Hara, M. (2003). Presidential address: Liquidity and price discovery. Journal of
Finance 58, 1335-1354.
83

Obizhaeva, A.A., and Wang, J. (2013) Optimal trading strategy and supply/demand
dynamics, Journal of Financial Markets 16, 1-32
Padungsaksawasdi, C., & Daigler, R. T. (2014). The return-implied volatility relation for
commodity ETFs. Journal of Futures Markets 34, 261-281.
Pirrong C. (1996). Market liquidity and depth on computerized and open outcry trading
systems: A comparison of DTB and LIFFE bund contracts. Journal of Futures
Markets 16, 519-543.
Poterba, J. M., & Shoven, J. B. (2002). Exchange traded funds: A new investment option
for taxable investors. American Economic Review 92, 422–427
Roll, R. (1984). A simple implicit measure of the effective bid-ask spread in an efficient
market. The Journal of Finance, 39, 1127-39.
Roll, R., Schwartz, E., & Subrahmanyam, A. (2007). Liquidity and the law of one price:
the case of the futures/cash basis, Journal of Finance 62, 2201–2234.
Saar, G. (2001). Price impact asymmetry of block trades: An institutional trading
explanation. Review of Financial Studies 14, 1153-1181.
Schlusche, B. (2009). Price formation in spot and futures markets: Exchange traded funds
vs. index futures. The Journal of Derivatives 17, 26–40.
So, R. W., & Tse, Y. (2004). Price discovery in the Hang Seng index markets: Index,
futures, and the tracker fund. Journal of Futures Markets 24, 887-907.
Stoll, H., R. (1989). Inferring the components of the bid-ask spread: theory and empirical
tests, Journal of Finance, 44, 115-134.
Stoll, H., R. (1978). The supply of dealer services in securities markets. Journal of
Finance 33, 1133-1151.
Stoll, H. R., & Whaley, R., E. (1990). The dynamics of stock index and stock index
futures returns. Journal of Financial and Quantitative Analysis 25, 441-468.
Subrahmanyam, A. (1991). Risk aversion, market liquidity, and price efficiency, Review
of Financial Studies, 4, 417–441.
Subrahmanyam, A. (2009). The implications of liquidity and order flows for neoclassical
finance. Pacific-Basin Finance Journal 17, 527-532.
Theissen, E. (2002). Price discovery in floor and screen trading systems. Journal of
Empirical Finance 9, 455-474.
Tse, Y. (1999). Price discovery and volatility spillovers in the DJIA index and futures
market. Journal of Futures Markets 19, 911-933.
84

Tse, Y., Bandyopadhyay, P., & Shen, Y.P. (2006). Intraday price discovery in the DJIA
index markets. Journal of Business Finance and Accounting 33, 1572 -1585.
Van Ness, B.F., Van Ness, R.A., and Warr, R.S. (2001). How well do adverse selection
components measure adverse selection? Financial Management, 30, 77-98.
Zhong, M., Darrat, A. F., & Otero, R. (2004). Price discovery and volatility spillovers in
index futures markets: Some evidence from Mexico. Journal of Banking and
Finance 28, 3037-3054.
85

VITA
AHMET SENOL OZTEKIN

|     |     | Born, Istanbul, Turkey  |
| --- | --- | ----------------------- |

| 2004    |     | B.S., Mathematical Sciences  |
| ------- | --- | ---------------------------- |
|         |     | Yeditepe University          |
|         |     | Istanbul, Turkey             |

| 2007    |     | Master of Technology   |
| ------- | --- | ---------------------- |
Florida International University
Miami, Florida

| 2014    |     | Doctoral Candidate                |
| ------- | --- | --------------------------------- |
|         |     | Florida International University  |
|         |     | Miami, Florida                    |

PUBLICATIONS AND PRESENTATIONS

Anatomy of a Crash: ETF Options During the Flash Crash, with Sascha Strobl (ADA),
RobertT. Daigler (FIU), Forthcoming at Review of Futures Markets
EFA 2013 in St.Pete Beach, “Anatomy of a Crash: ETF Options During the Flash Crash”
FMA 2013 in Chicago, “Liquidity, Characteristics and Price Discovery in U.S. Electronic
Futures and ETF Markets”
GFC  2013  in  Monterey,  California,  “Global  Equity  Market  Innovations  through
Volatility Measures”
SWFA 2012 in New Orleans, “Liquidity, Volatility and Market Depth in U.S. Electronic
Futures Market”

86
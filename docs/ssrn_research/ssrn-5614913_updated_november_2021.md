# Updated November 2021

- **Source File**: `ssrn-5614913.pdf`
- **Total Pages**: 53
- **SSRN ID**: `ssrn-5614913`

---


### Page 1

Updated November 2021
Information to appear on the first page of your article
Title:  Return Predictability in Bitcoin ETFs: A Machine Learning
Approach
Authors (including degrees):
Hajar Novinsalari, Phd student in finance.
Ahmet Sensoy, Associate professor of finance
Affiliations for all authors (Department (spelt in full), School, Hospital, or Organization,
City, State/Province, Country):
Faculty of Business Administration, Bilkent University, 06800 Ankara, Turkiye
Conflict of Interests:
☒ The authors declare that they have no known competing financial interests or personal relationships
that could have appeared to influence the work reported in this paper.
☐  The authors declare the following financial interests/personal relationships which may be considered
as potential competing interests:
Preprint not peer reviewed


### Page 2

Updated November 2021
Corresponding author address (Street and full postal address, without the institution or
department):
Faculty of Business Administration, Bilkent University, 06800 Ankara, Turkiye
Correspondence telephone (please follow format +1 XXX XXX XXXX for US Nos):
+905546255188
Correspondence email:
hajar@bilkent.edu.tr
Ahmet.sensoy@bilkent.edu.tr
Information to appear on the end pages of your article before the references
Acknowledgment and funding sources:*
While preparing this work, the authors used AI tools to check, correct, and organize text for
more readability and precision.
*(Please note that you should not include a statement to the effect that there is no
acknowledgment or funding, only actual funding details or acknowlegments should be
included in this section)
Preprint not peer reviewed


### Page 3

Return Predictability in Bitcoin ETFs: A Machine
Learning Approach
Abstract
This study employs machine learning classification methods to analyze the
predictability of eight prominent crypto exchange-traded funds across four
distinct temporal intervals. Numerical experiments employing classification
techniques, including Logistic Regression, Linear Regression, Support Vector
Machines, Artificial Neural Networks, K-means clustering, and Random For-
est algorithms, illustrate the predictability of price fluctuations, both upward
and downward. The average classification accuracy of the six algorithms ex-
ceeds 50% across all cryptocurrencies and time scales, with Neural Networks
and SVM models often surpass 0.80. This indicates a degree of price pre-
dictability, suggesting a potential violation of the weak-form Efficient Market
Hypothesis (EMH) in crypto ETF markets and the possibility of profitable
strategies based on historical data. Among strategies considered, Momentum
stands out for those prioritizing returns and willing to tolerate volatility, of-
fering strong growth potential in the crypto space.
Keywords:
Crypto ETFs, Return prediction, Machine learning, Efficient
market hypothesis, Trading strategies.
1. Introduction
A significant milestone in US cryptocurrency investing was reached on
January 10, 2024, when the Securities and Exchange Commission (SEC)
approved spot Bitcoin exchange-traded funds (ETFs).
These funds allow
investors to buy and sell Bitcoin at its current market price. This approval
by an important regulator like the SEC is a big step forward. It creates a
strong and scalable connection between cryptocurrency and traditional fi-
nance, helping to bring the two systems together. Bitcoin ETFs represent a
new asset class within the exchange-traded fund framework, offering investors
exposure to Bitcoin’s potential returns without the complexities of manag-
Preprint submitted to Elsevier
July 18, 2025
Preprint not peer reviewed


### Page 4

ing cryptocurrency directly. By mirroring traditional investment structures,
these ETFs are well-suited for integration into mainstream portfolios, mak-
ing them accessible to institutional and retail investors. Since their approval
in January 2024, Bitcoin ETFs have witnessed a substantial influx of capital,
rapidly becoming among the most widely held ETFs.
This study focuses on Spot Bitcoin ETFs, financial instruments that track
the price of Bitcoin, a cryptocurrency. These ETFs operate in a way familiar
to many investors: Each share of the ETF is backed by actual cryptocurrency
held in reserve. This allows investors to follow the price changes of Bitcoin
without needing to buy, hold, or manage the cryptocurrency themselves.
Spot Bitcoin ETFs are explicitly designed with Bitcoin as the underlying
asset and function similarly to traditional ETFs, offering reassurance by op-
erating like conventional ETFs. The availability of eleven Spot Bitcoin ETFs
in the US further emphasizes how this new investment option resembles tra-
ditional ETFs.
Bitcoin ETFs offer a variety of benefits for both institutional and indi-
vidual investors. They provide individual investors a straightforward way
to gain exposure to Bitcoin, bypassing the complexities of cryptocurrency
wallets or exchanges. This simplifies the investment process for many. Ad-
ditionally, ETFs offer institutions a secure and regulated means to diversify
their portfolios with Bitcoin, potentially enhancing their returns. The fact
that these ETFs can be traded on traditional stock markets simplifies the
process for institutions to incorporate Bitcoin into their existing investment
strategies. Notably, the safety and regulation of these ETFs provide reas-
surance to institutional and retail investors, allowing them to participate
confidently in the Bitcoin market.
On the other hand, Spot Bitcoin ETFs are generally considered risky be-
cause Bitcoin is inherently volatile, which can lead to significant fluctuations
in the ETF’s value. This potential for substantial changes should prompt in-
vestors to exercise caution and maintain awareness. They must be prepared
for significant price fluctuations and the risk of losses. Fees, like expense
ratios, are also part of managing ETFs and can affect total returns.
Changes to the regulations could significantly impact the availability of
spot Bitcoin ETFs, affecting the investment choices of many investors. Ad-
ditionally, secure and reliable custody solutions are crucial for managing
Bitcoin holdings. Emphasizing the significance of these solutions is critical
for fostering investor confidence. Acknowledging that any potential security
breaches could harm investor trust is essential. Understanding the tax im-
2
Preprint not peer reviewed


### Page 5

plications of holding Bitcoin directly, which may vary by region, is crucial
for informed decision-making. Investors need to be aware of the unique tax
issues in their area.
The existing literature reveals three key gaps. First, there is a lack of
research on the efficiency of the market for crypto exchange-traded funds
(ETFs). Second, most previous studies relied on standard statistical tests
that only assessed whether financial markets are weakly efficient. While these
tests can indicate inefficiency, they do not provide insights into capitalizing on
market opportunities or quantifying potential profits from consistent trading.
Finally, most studies have focused on daily returns in traditional and non-
traditional financial markets. However, high-frequency analysis is urgently
needed for a more comprehensive understanding of crypto ETFs.
There are important reasons to explore the questions mentioned earlier.
Crypto ETFs have strong growth potential and may include more types of
digital assets over time. As the market grows, more advanced products—such
as leveraged and inverse crypto ETFs—may provide investors with new op-
portunities to profit from price fluctuations. Some ETFs might also focus on
themes like blockchain technology or tokenization. New regulations will play
a significant role in shaping these trends and helping to protect investors and
stabilize the market.
This study aims to address all previously mentioned issues and answer
the question: Can machine learning models accurately predict price move-
ments in crypto ETFs, and how do these models compare across different
timeframes? To achieve this, we assess the predictability of returns for eight
Bitcoin ETFs by analyzing returns at various intraday frequencies. We uti-
lize techniques such as Support Vector Machines, Logistic Regression, Linear
Regression, Artificial Neural Networks, K-means clustering, and Random
Forest classification. Our findings indicate that the returns in cryptocur-
rency ETF markets can be regularly forecasted at daily or minute intervals,
achieving classification accuracies reaching up to 89% and an average accu-
racy of approximately 55% to 60% across all sampled cryptocurrencies. Upon
comparing the accuracy metrics among the models, the Neural Networks and
SVM models demonstrate the best accuracy, frequently above 0.80, with spe-
cific instances attaining 0.86. These models consistently demonstrate strong
performance across various time frames and scenarios. The Decision Tree
and K-means Clustering models exhibit moderate accuracy, typically rang-
ing from 0.55 to 0.78, rendering them less dependable for high-precision fore-
casts. Despite challenges with non-linear data patterns, Linear Regression
3
Preprint not peer reviewed


### Page 6

and Logistic Regression models offer a distinct advantage in interpretability.
Their accuracy rates typically range from 0.75 to 0.78.
Our findings, which show a violation of the weak-form efficiency property
in crypto ETF markets at daily and various minute levels, have significant
implications for investors. We also discuss strategies in crypto ETF markets
and conclude that the best approach depends on an investor’s risk tolerance
and objectives.
The paper is structured as follows: Sections 2 and 3 present the literature
review and the data used in this study. Section 4 describes the methodologies
used to identify predictability patterns. Sections 5 and 6 provide the test
results and examine their robustness. Section 7 discusses various strategies,
and finally, Section 8 offers concluding remarks.
2. Literature review
After this brief introduction, it’s important to discuss whether the prices
of cryptocurrency ETFs can be predicted. Experts are still debating the ap-
plicability of the efficient market hypothesis (EMH) to crypto ETFs. How-
ever, Investors should exercise caution and take the time to understand the
market thoroughly.
There are three types of EMH: weak, semi-strong, and strong. The weak-
form states that past prices cannot be used to predict future prices. The
semi-strong form states that prices change rapidly due to publicly available
information. Moreover, the strong form says prices reflect even private or
insider information. The Efficient Market Hypothesis (EMH) asserts that
it is impossible to consistently outperform the market average through ac-
tive management or stock selection, as asset prices rapidly incorporate all
available information. According to EMH, any new information is quickly
reflected in prices, leaving no room for systematic excess returns. However,
the hypothesis has its critics. Some argue that markets are not always per-
fectly efficient, particularly in the short term, and that skilled investors may
take advantage of mispricings or behavioral biases to achieve superior returns.
For example, ”Stock Market Prices Do Not Follow Random Walks” by
Lo and MacKinlay (1988) shows that stock returns are not random, which
contradicts the Random Walks theory. Poterba and Summers (1988) and
Brock et al. (1992) demonstrate that the weak-form of the Efficient Market
Hypothesis (EMH) is violated in various types of asset returns.
4
Preprint not peer reviewed


### Page 7

In the context of cryptocurrency markets, Urquhart (2016) finds, in ”The
Inefficiency of Bitcoin,” that Bitcoin prices exhibit serial correlation, further
contradicting the weak-form Efficient Market Hypothesis (EMH).
Many studies have subsequently explored the weak-form Efficient Mar-
ket Hypothesis (EMH) using diverse methodologies, sample frequencies, and
benchmark currencies. For example, Bariviera (2017) examines the informa-
tion efficiency of Bitcoin returns by analyzing their long-range dependence
characteristics. Vidal-Tomas and Ibanez (2018) evaluate efficiency in cryp-
tocurrency markets through non-linear statistical approaches. Sensoy et al.
(2019) extend the analysis to cross-market cryptocurrency efficiency using
multi-fractal analysis. These varied approaches underline the extensive in-
terest in understanding market efficiency in rapidly evolving and diverse fi-
nancial markets.
Tartakovsky et al.
(2020) analyze the efficiency of the
cryptocurrency market by examining return autocorrelation. Their findings
reveal significant short-term inefficiencies, which challenge the Efficient Mar-
ket Hypothesis (EMH).
Urquhart and Zhang (2022) assess market efficiency using the Adaptive
Market Hypothesis (AMH). They demonstrate that the efficiency of Bitcoin
and Ethereum fluctuates over time, with active trading strategies occasion-
ally outperforming passive ones.
Research exploring the weak-form Efficient Market Hypothesis (EMH) in
ETF markets has revealed significant implications. The findings suggest that
inefficiencies exist where historical price data can predict future price move-
ments. Mazouz and Bowe (2006) demonstrate patterns in the price behavior
of ETFs that contradict the notion of weak-form efficiency. ”Inefficiencies in
the Pricing of Exchange-Traded Funds” by Antti Petajisto (2017) examines
how ETF prices can deviate from their net asset values (NAVs), particularly
in funds holding international or illiquid securities. These collective findings
challenge ETF markets’ weak-form Efficient Market Hypothesis (EMH), sug-
gesting that past prices may have predictive power, particularly in less liquid
or emerging ETF segments.
Fischer and Krauss (2021) investigate the application of machine learn-
ing to financial forecasting. They highlight how these methods can improve
predictive accuracy and expand the capabilities of traditional econometric
models. Their findings suggest that machine learning techniques, such as
deep learning, significantly enhance price forecasts, providing a strong foun-
dation for exchange-traded fund (ETF) forecasting.
Shih et al. (2024) compare deep learning methods to the Fama-French
5
Preprint not peer reviewed


### Page 8

three-factor model for predicting ETF returns. Their research supports the
effectiveness of deep learning in ETF price forecasting, revealing that Neu-
ral Networks—especially Long Short-Term Memory (LSTM) networks and
Convolutional Neural Networks (CNN)—outperform traditional models by
effectively identifying complex market patterns.
Due to their recent emergence, examining weak-form market efficiency in
Bitcoin ETFs is still in early development. However, insights from broader
cryptocurrency markets suggest that these financial instruments may ex-
hibit inefficiencies. Factors such as limited market depth, evolving regula-
tory frameworks, and high volatility can contribute to deviations from the
Random Walks hypothesis. This, in turn, suggests a potential for predictabil-
ity in price movements, offering a more optimistic outlook for investors and
enabling the possibility of more informed trading decisions.
3. Data
Spot and Futures Crypto ETFs are two distinct vehicles that provide
exposure to cryptocurrencies. A Spot Crypto ETF directly invests in the
underlying cryptocurrency, such as Bitcoin or Ethereum, and holds the actual
asset securely in custody. This means the ETF’s price closely tracks the real-
time market value of the cryptocurrency it represents. Spot ETFs are popular
among long-term investors seeking a direct way to gain exposure to crypto
without the complexity of managing wallets or private keys. However, they
face significant regulatory hurdles in many regions, which investors should
be aware of, and risks like custody breaches are inherent due to the need to
store physical assets.
On the other hand, Futures Crypto ETFs do not invest in physical cryp-
tocurrencies; instead, they trade in futures contracts tied to them. These
contracts are agreements to buy or sell the asset at a specified price on a
future date.
Futures ETFs have a more transparent and straightforward
launch process, making them easier to implement. They often follow a more
explicit regulatory path, exemplified by Bitcoin Futures ETFs that have al-
ready received approval in specific markets. However, pricing discrepancies
can occur because futures contracts do not always match spot market prices.
This misalignment is mainly due to market conditions such as contango or
backwardation.
Additionally, regularly rolling over contracts to maintain
continuous exposure can introduce transaction costs and potential slippage,
which may erode returns over time.
6
Preprint not peer reviewed


### Page 9

The primary difference between the two lies in their underlying assets
and investment strategies. Spot ETFs offer direct exposure by holding the
underlying cryptocurrency, making them ideal for investors seeking straight-
forward, long-term exposure to crypto markets. Futures ETFs, in contrast,
cater to more sophisticated traders looking to leverage or hedge their po-
sitions without holding the actual asset. The increasing popularity of spot
crypto ETFs makes this study particularly relevant. Spot ETFs provide sim-
plicity and direct exposure to the underlying assets, making them a valuable
tool for understanding the dynamics of these increasingly important financial
products.
This study utilizes dollar-denominated crypto ETF data obtained from
the Bloomberg terminal. Our dataset covers January 11, 2024, to August 16,
2024. During this period, we selected eight widely traded cryptocurrencies
denominated in US dollars, which significantly impacted the market. Table
1 lists the ticker symbols and fund names.
Table 1: The list of Spot Crypto ETFs from January 11 to August 16, 2024.
Ticker
Fund name
ARKB
ARK 21Shares Bitcoin ETF
BITB
Bitwise Bitcoin ETF Trust
BRRR
Coinshares Valkyrie Bitcoin Fund
BTCO
Invesco Galaxy Bitcoin ETF
EZBC
Franklin Bitcoin ETF
FBTC
Fidelity Wise Origin Bitcoin Fund
HODL
VanEck Bitcoin ETF
IBIT
iShares Bitcoin Trust ETF
Figure 1 shows the daily closing prices for each of the selected crypto
ETFs. The performance of various crypto ETFs highlights the diverse char-
acteristics, risks, and rewards associated with these instruments. One no-
table aspect of crypto ETFs is their high volatility. The chart reveals sig-
nificant price fluctuations across all ETFs, reflecting the inherent instability
of the cryptocurrency market. Some ETFs, such as ”HODL,” exhibit more
pronounced peaks and dips, suggesting aggressive or leveraged exposure to
crypto assets. This volatility highlights the potential for substantial gains
7
Preprint not peer reviewed


### Page 10

Figure 1: Closing daily prices of eight crypto ETFs from January 11 to August 16, 2024
and significant losses, serving as a reminder of the market’s unpredictability
and the importance of exercising caution in investment decisions.
Another observation is the diverse performance of the ETFs. While all
appear influenced by the broader crypto market, the degree of growth and
fluctuation varies. For example, ”HODL” shows higher peaks and outper-
formance during market rallies, whereas ”BRRR” maintains a relatively flat
trajectory, indicating a more conservative or niche strategy. Additionally,
the correlation among the ETFs is evident, as they generally follow similar
trends, rising and falling in tandem with the broader cryptocurrency market.
This alignment suggests that macro-level market events, such as Bitcoin price
surges or regulatory developments, significantly impact all crypto ETFs, in-
fluencing their performance to varying degrees.
Tables 2, 3, 4, and 5 provide descriptive statistics for the log returns across
multiple timeframes, including 15 minutes, 30 minutes, 60 minutes, and daily.
With the highest mean and median values across all timeframes, HODL
consistently outshines in terms of average performance, indicating its strong
relative performance. However, BRRR consistently has the lowest mean and
median, suggesting a less successful or conservative strategy. The middle
ground is occupied by ARKB, BTCO, and FBTC, which offer a performance
8
Preprint not peer reviewed


### Page 11

that falls between the extremes of HODL and BRRR.
According to the standard deviation, HODL is the most volatile ETF,
with notable price fluctuations throughout all periods. This high volatility
suggests a higher-risk, higher-reward profile. On the other hand, because it
is conservative and reliable, BRRR is the least volatile. ETFs with moderate
volatility, such as ARKB and BTCO, appeal to investors seeking a strategy
that balances risk and reward.
HODL has the highest maximum value when analyzing price ranges, peak-
ing at 83.04 in the daily data. This underlines its strong potential during
bullish market conditions. In contrast, BRRR has the lowest minimum value,
reinforcing its conservative approach. FBTC and BTCO maintain relatively
high maximum prices compared to their minimums, indicating meaningful
upward price movements while avoiding extreme lows.
Examining upward and downward movements, HODL has the highest
proportion of upward movements, reaching 55% in specific time frames, which
highlights its bullish momentum. However, its higher rate of downward move-
ments in shorter time frames suggests susceptibility to corrections.
Most
other ETFs exhibit balanced movement percentages, hovering around 50%,
reflecting their alignment with broader market trends. However, BRRR dis-
plays a slightly bearish outlook with a lower upward movement percentage
of 49% in shorter periods.
Shorter intervals (15-60 minutes) show greater price fluctuations, under-
scoring the intraday volatility typical of crypto markets. The statistics stabi-
lize over longer time frames (daily), providing a clearer picture of the ETFs’
long-term performance. HODL continues to dominate in mean values, max-
imum prices, and upward momentum, making it an attractive option for
long-term, risk-tolerant investors. Meanwhile, BRRR maintains its stability,
offering minimal price swings but limited growth potential.
9
Preprint not peer reviewed


### Page 12

Mean
Median
Std
Min
Max
Up Move
Up Move %
Down Move
Down Move %
ARKB
60.61
63.36
8.89
39.3
72.97
77.0
50.0
72.0
47.0
BITB
33.16
34.6
4.77
21.4
39.7
74.0
49.0
76.0
50.0
BRRR
17.51
18.04
2.16
11.27
20.66
80.0
52.0
69.0
45.0
BTCO
61.04
63.47
8.83
39.29
73.07
77.0
50.0
73.0
48.0
EZBC
35.47
36.78
4.83
23.31
42.35
77.0
50.0
73.0
48.0
FBTC
53.23
55.43
7.74
33.87
63.74
76.0
50.0
74.0
49.0
HODL
69.45
71.96
9.55
44.8
82.86
84.0
55.0
66.0
43.0
IBIT
34.6
36.03
5.04
22.39
41.88
77.0
50.0
73.0
48.0
Table 2: Summary statistics of 15-minute log-returns from January 11 to August 16,
2024. ’Up Move’ and ’Down Move’ indicate the number of positive and negative returns,
respectively.
Mean
Median
Std
Min
Max
Up Move
Up Move %
Down Move
Down Move %
ARKB
60.69
63.33
8.96
39.0
73.1
457.0
50.0
451.0
49.0
BITB
33.19
34.59
4.82
21.13
40.02
462.0
49.0
458.0
49.0
BRRR
17.53
18.04
2.17
11.1
20.73
244.0
47.0
260.0
50.0
BTCO
61.01
63.5
8.83
39.01
73.27
252.0
50.0
246.0
49.0
EZBC
35.48
36.85
4.87
22.64
42.45
211.0
50.0
205.0
48.0
FBTC
53.18
55.43
7.74
33.99
64.14
498.0
50.0
468.0
47.0
HODL
69.51
71.97
9.51
44.38
82.97
245.0
48.0
250.0
49.0
IBIT
34.64
36.09
5.04
22.18
41.81
486.0
49.0
480.0
49.0
Table 3: Summary statistics of 30-minute log-returns from January 11 to August 16,
2024. ’Up Move’ and ’Down Move’ indicate the number of positive and negative returns,
respectively.
10
Preprint not peer reviewed


### Page 13

Mean
Median
Std
Min
Max
Up Move
Up Move %
Down Move
Down Move %
ARKB
60.68
63.36
8.97
38.65
73.37
922.0
50.0
885.0
48.0
BITB
33.19
34.6
4.82
21.13
40.02
916.0
49.0
902.0
48.0
BRRR
17.53
18.03
2.17
11.04
20.79
521.0
50.0
477.0
46.0
BTCO
61.02
63.6
8.83
39.01
73.27
512.0
51.0
482.0
48.0
EZBC
35.5
36.85
4.87
22.64
42.45
421.0
50.0
408.0
48.0
FBTC
53.19
55.44
7.74
33.97
64.2
998.0
51.0
940.0
48.0
HODL
69.51
71.98
9.51
44.28
82.99
507.0
50.0
487.0
48.0
IBIT
34.65
36.1
5.05
22.16
41.84
987.0
50.0
935.0
48.0
Table 4: Summary statistics of 60-minute log-returns from January 11 to August 16,
2024. ’Up Move’ and ’Down Move’ indicate the number of positive and negative returns,
respectively.
Mean
Median
Std
Min
Max
Up Move
Up Move %
Down Move
Down Move %
ARKB
60.68
63.36
8.97
38.65
73.37
1842.0
50.0
1758.0
48.0
BITB
33.19
34.6
4.82
21.13
40.02
1859.0
50.0
1782.0
48.0
BRRR
17.53
18.02
2.16
11.04
20.79
1004.0
49.0
959.0
46.0
BTCO
61.03
63.59
8.83
38.72
73.27
1012.0
50.0
976.0
48.0
EZBC
35.51
36.85
4.87
22.43
42.55
843.0
50.0
809.0
48.0
FBTC
53.19
55.46
7.74
33.84
64.2
1963.0
50.0
1884.0
48.0
HODL
69.51
72.02
9.53
43.9
83.04
1001.0
50.0
981.0
49.0
IBIT
34.64
36.12
5.05
22.07
41.84
1934.0
49.0
1895.0
48.0
Table 5: Summary statistics of daily log-returns from January 11 to August 16, 2024. ’Up
Move’ and ’Down Move’ indicate the number of positive and negative returns, respectively.
11
Preprint not peer reviewed


### Page 14

3.1. Measures
We use thirty-four features (Table 6) to predict the daily and minute-level
returns in the next period. The fundamental features are the open, close,
high, low prices, and high-low range. The second group of features includes
the last five lagged log returns. The exponentially weighted moving average
of the close prices, the cumulative sum of the log returns for the previous 3
and 5 days, and their differences are used as ten additional features. Two
relative strength indexes, two rate of change indexes, and the weighted mov-
ing average of close prices are also utilized as features. The relative strength
index is calculated using the following formula:
RSI = 100 −
100
1 + SMMA(U,n)
SMMA(D,n)
(1)
The smoothed moving average SMMA is an exponential moving average
of the upward and downward price changes in the last n trading days. The
upward and downward price changes are defined as follows:
D =
(
Closeprevious −Closenow,
if Closeprevious > Closenow
U = 0
(2)
U =
(
Closenow −Closeprevious,
if Closenow > Closeprevious
D = 0
(3)
After identifying upward and downward price changes, the exponential mov-
ing average is computed over the predefined last n trading days. Our feature
set uses two distinct n values: 9 and 14 days.
Once the index’s relative
strength has been determined, four additional indicator elements are devel-
oped to indicate whether the assets are overbought or oversold for the 9—
and 14-day RSI values. RSI(14) is the default setting recommended by J.
Welles Wilder (1986), the developer of the Relative Strength Index.
On
the other hand, RSI(9) is commonly favored by traders seeking shorter-term
signals. These values are considered “industry standard,” making them a
natural starting point for analysis by practitioners and researchers.
The Rate of Change (RoC) is valuable for understanding market mo-
mentum and price dynamics. It helps traders assess market strength, iden-
tify potential trend reversals, and determine optimal entry and exit points.
The Rate of Change is a momentum indicator that measures the percent-
age change in an asset’s price over a specific period. This indicator enables
12
Preprint not peer reviewed


### Page 15

traders and analysts to assess the strength of price movements and identify
overbought or oversold conditions. The formula is as follows:
ROC = Pt −Pt−n
Pt−n
× 100
(4)
The Exponential Weighted Moving Average (EWMA) is a type of moving
average that assigns greater weight to recent data points while gradually
decreasing the influence of older data. Unlike the simple moving average,
which gives equal weight to all observations within the window, the EWMA
uses a smoothing factor (λ) to prioritize recent prices or values. The formula
for EWMA is:
EWMAt = λPt + (1 −λ) EWMAt−1
(5)
The Momentum Indicator is a simple yet effective tool used in techni-
cal analysis to measure the rate of price change over a specified period. It
helps traders identify the speed of price movement and assess whether the
trend is gaining or losing strength, which can indicate potential reversals or
continuations.
%R = High(n) −Last Close
High(n) −Low(n)
(6)
The Aroon Stochastic Oscillator is a hybrid technical indicator that com-
bines the Aroon Indicator and the Stochastic Oscillator to assess trend strength
and direction while detecting overbought and oversold conditions. The Aroon
indicator assesses the duration since the highest high and lowest low within
a specified time frame, indicating whether an asset is trending or oscillating
within a range. The Stochastic Oscillator evaluates the closing price’s posi-
tion relative to its recent high-low range, providing insights into momentum
and potential reversal points. The Aroon Stochastic Oscillator thoroughly
assesses trend strength and momentum, allowing traders to detect trend re-
versals and choose optimal entry or exit points.
The Double Exponential Moving Average (DEMA) is a refined moving
average designed to minimize the lag associated with traditional moving aver-
ages, making it more responsive to price changes. Unlike the Simple Moving
Average (SMA) or Exponential Moving Average (EMA), the DEMA com-
bines two EMAs to achieve a smoother and faster-reacting indicator. The
formula is:
DEMAt = 2EMAt −EMA(EMAt)
(7)
13
Preprint not peer reviewed


### Page 16

A comprehensive elucidation and compilation of formulas for many tech-
nical indicators are available in Kyoung-jae et al. (2000).
4. Empirical analysis
This section computes target returns using four distinct time intervals:
daily, 15-minute, 30-minute, and 60-minute frequencies. Based on the cal-
culated returns at various time horizons, a binary classification problem is
formulated. Specifically, the binary target variable is assigned a value of 1
if the return at the subsequent time step is positive, and −1 if the return
is negative. Six classification algorithms are implemented to classify these
target variables: Logistic Regression, Linear Regression, Support Vector Ma-
chines (SVM), Artificial Neural Networks (ANN), K-means clustering, and
Random Forests. These models are developed using Python’s widely adopted
scikit-learn library.
We briefly overview the classification algorithms and their results without
going into technical implementation details. In addition to machine learning
models, we incorporate traditional forecasting methods, such as the Random
Walk model and ARIMA, as benchmarks. Finally, we use the t-test and
the Wilcoxon signed-rank test to compare the performance of the different
methods statistically.
4.1. Machine learning methods
Classification is a fundamental task in machine learning to predict a dis-
crete class label for input data. It is a part of supervised learning, where
models are trained using labeled datasets. The objective is to identify pat-
terns or decision boundaries in the data, enabling the model to assign new,
unseen data points to the correct categories. Essentially, classification in-
volves mapping input features to predefined class labels.
Accuracy is one of the most commonly used metrics for evaluating the
performance of a classification model. It measures the proportion of correctly
classified instances from the total number of cases in the dataset.
This study examined six distinct classification algorithms to categorize
target variables at different temporal frequencies. We utilized Python’s pop-
ular scikit-learn package to implement various classification techniques, in-
cluding logistic regression, linear regression, Support Vector Machines, Arti-
ficial Neural Networks, Random Forests, and the K-means algorithm. While
14
Preprint not peer reviewed


### Page 17

Table 6: Set of features utilized in the classification algorithms
Feature name
Number of lags/window
size
Number of features
Open, high, low, close
Last one period
4
High-low
Last one period
1
Returns ( rt−1, . . . , rt−5 )
Last five periods
5
Moving average (MA)
Last 5 days
1
Correlation MA and close
Last one value
1
Σk =
N
X
t=k
rt−1 + · · · + rt−k,
k = 3, 5
Last 3/5 days
2
Σ5 −Σ3
Last 3/5 days
1
Relative strength index (RSI)
Window size = 6, 14
2
1 (RSI6) < 20%, 1 (RSI14) <
20%
Buy signals w.r.t.
the
RSIs
2
−1 (RSI6) > 80%, −1 (RSI14) >
80%
Sell signals w.r.t.
the
RSIs
2
Moving average convergence di-
vergence (MACD)
Fast period = 5, slow =
10, signal period = 5
3
Rate of change, rate of change
return
Window = 9, 14
2
Exponential
weighted
moving
average (EWMA)
λ = 0.9
1
Momentum indicator
Window = 5
1
Average true range
Window = 5, 10
2
Williams’ %R
Window = 14
1
Aroon stochastic oscillator
Window = 14
1
Double exponential moving av-
erage (DEMA)
Window = 10
1
15
Preprint not peer reviewed


### Page 18

existing research provides a detailed discussion of these algorithms, this sec-
tion will focus on their application.
4.1.1. Logistic regression
Logistic Regression is a foundational algorithm in machine learning de-
signed primarily for classification tasks. Despite its name, it is not a regres-
sion algorithm for predicting continuous values but a method for predicting
the probability of a discrete outcome. It is particularly effective in binary
classification problems, where the goal is to categorize data into one of two
possible classes.
Logistic Regression is a supervised learning algorithm widely used for
binary classification tasks. It estimates the probability that a given input
belongs to a specific class by applying the logistic (sigmoid) function to a
linear combination of input features. Based on this probability, the model
categorizes the input into one of two classes.
Python provides several libraries for implementing the popular machine
learning algorithm, Logistic Regression. Among these, scikit-learn is one of
the most widely used, and we will focus on it.
The results for the Logistic Regression are given in Table 7. The ”Daily-
0.8” shows the best overall performance for most crypto ETFs. According to
the table, the ”Daily-0.8” configuration yields the highest overall performance
for most ETFs. For example, ARKB achieves a performance value of 0.74,
BRRR reaches 0.85, and EZBC achieves 0.81, indicating strong predictive
capability at this temporal resolution and threshold. This suggests that daily
aggregated data provide more consistent and reliable inputs for the Logistic
Regression model, likely because they capture broader trends and smooth
out noise that may be present in more granular time intervals.
As the time interval decreases to 60 minutes, 30 minutes, and 15 min-
utes, the performance generally declines, indicating that shorter intervals
may introduce more variability in the data. For instance, ARKB’s perfor-
mance drops from 0.74 in ”Daily-0.8” to 0.58 in ”60min-0.8” and further
to 0.55 in ”30min-0.9.” Similar trends are observed for other ETFs, such as
BITB and HODL, suggesting that the increased frequency of observations
at shorter intervals may reduce the Logistic Regression model’s ability to
discern meaningful patterns.
Overall, ETFs like BRRR and BTCO consistently exhibit high-performance
metrics, indicating their predictive strength and reliability in Logistic Re-
gression. In contrast, ETFs like FBTC and IBIT exhibit lower performance
16
Preprint not peer reviewed


### Page 19

metrics across most configurations, with values of 0.52 for FBTC and 0.56
for IBIT in the ”Daily-0.8” scenario.
ARKB
BITB
BRRR
BTCO
EZBC
FBTC
HODL
IBIT
Daily-0.8
0.74
0.56
0.85
0.85
0.81
0.52
0.78
0.56
60 min-0.9
0.6
0.64
0.78
0.69
0.78
0.59
0.71
0.54
60 min-0.8
0.58
0.65
0.86
0.74
0.78
0.56
0.74
0.46
30 min-0.9
0.55
0.59
0.82
0.68
0.84
0.51
0.72
0.49
30 min-0.8
0.58
0.61
0.84
0.74
0.78
0.53
0.81
0.52
15 min-0.9
0.55
0.59
0.78
0.74
0.77
0.52
0.74
0.52
15 min-0.8
0.61
0.61
0.82
0.75
0.82
0.51
0.8
0.56
Table 7: Logistic regression prediction accuracy across various time intervals and thresh-
olds from January 11 to August 16, 2024.
4.1.2. Support vector machine
Support Vector Machines (SVMs) are powerful and versatile machine-
learning algorithms for classification and regression tasks. They are particu-
larly effective for high-dimensional data and are widely employed in various
applications. The primary objective of SVMs is to find the optimal decision
boundary, also known as the hyperplane, that best separates data points
belonging to different classes. At its core, an SVM attempts to find a hy-
perplane in an N-dimensional space, where N is the number of features, that
separates the data into distinct classes. The optimal hyperplane maximizes
the margin, the distance between it and the nearest data points from each
class. These closest points, known as support vectors, support the definition
of the hyperplane.
Mathematically, the optimization problem in SVM aims to maximize the
margin while ensuring the correct classification of the data points.
This
results in a decision boundary that generalizes well to unseen data. Given the
training vectors xi for i = 1, 2, ..., N with a sample size of N observations, the
support vector machine classification algorithm solves the following problem
given by
17
Preprint not peer reviewed


### Page 20

min
w,η
1
2wTw + C
N
X
i=1
ηi
(8)
subject to
yi(wTϕ(xi)) ≥1 −ηi,
i = 1, 2, . . . , N
(9)
ηi ≥0,
i = 1, 2, . . . , N
(10)
The optimization problem in Equation 8 can be globally solved using the
Karush–Kuhn–Tucker (KKT) conditions. Detailed derivations are provided
in Huang et al. (2007).
The results in Table 8 indicate that the ”Daily-0.8” yields the highest
overall performance across most ETFs. For instance, ARKB achieves 0.70,
BRRR reaches 0.85, and EZBC achieves 0.81, highlighting that daily aggre-
gated data provides more stable and reliable patterns for the SVM model to
classify effectively. This performance may be attributed to the reduced noise
in daily data compared to shorter time intervals, allowing the SVM to focus
on more prominent and consistent trends in the cryptocurrency data.
As the time interval decreases from daily to 60-minute, 30-minute, and
15-minute resolutions, there is a noticeable decline in performance across
most ETFs. For example, ARKB drops from 0.70 in ”Daily-0.8” to 0.59 in
”60min-0.8” and further to 0.55 in ”15min-0.9.” This trend suggests that
shorter intervals may introduce variability or noise, challenging the SVM’s
ability to identify meaningful patterns. However, some ETFs, such as BRRR
and BTCO, maintain relatively high performance even at shorter intervals,
demonstrating their improved predictive ability and less susceptibility to the
data’s enhanced sensitivity.
18
Preprint not peer reviewed


### Page 21

ARKB
BITB
BRRR
BTCO
EZBC
FBTC
HODL
IBIT
Daily-0.8
0.7
0.52
0.85
0.85
0.81
0.59
0.81
0.48
60 min-0.9
0.59
0.64
0.78
0.69
0.78
0.58
0.71
0.55
60 min-0.8
0.59
0.65
0.86
0.74
0.78
0.55
0.74
0.48
30 min-0.9
0.56
0.59
0.82
0.68
0.84
0.48
0.72
0.5
30 min-0.8
0.58
0.61
0.84
0.74
0.78
0.53
0.81
0.54
15 min-0.9
0.55
0.59
0.78
0.74
0.77
0.53
0.74
0.53
15 min-0.8
0.61
0.61
0.82
0.75
0.82
0.51
0.8
0.56
Table 8: Support vector machine (SVM) prediction accuracy across various time intervals
and thresholds from January 11 to August 16, 2024.
4.1.3. Random Forest classification
Random Forest is a robust and flexible machine-learning algorithm for
classification and regression tasks.
It belongs to the family of ensemble
learning methods, which combines multiple Decision Trees to achieve better
performance than a single tree. In the case of classification, Random Forest
creates an ensemble of Decision Trees during training and aggregates their
outputs to make the final prediction. This majority voting mechanism helps
to improve accuracy and robustness while reducing the risk of over-fitting, a
common issue with individual Decision Trees.
The efficacy of Random Forest is attributed to its incorporation of ran-
domness through two primary mechanisms: bootstrap sampling and random
feature selection. Bootstrap sampling, also known as bagging, involves train-
ing each tree on a randomly selected subset of the training data, obtained
by sampling with replacement. This ensures that each tree in the forest is
exposed to different data points, leading to diversity among the trees. Ad-
ditionally, at each split in a tree, Random Forest considers only a random
subset of features rather than all available features. This further enhances
diversity and reduces the correlation between trees, making the ensemble
more effective in capturing patterns in the data. More details can be found
at Breiman, L. (2001).
To implement Random Forest in Python, libraries such as scikit-learn
provide an intuitive interface for training and evaluating the model. The
19
Preprint not peer reviewed


### Page 22

process typically involves splitting the data into training and testing sets,
fitting the Random Forest classifier to the training data, and assessing its
performance on the test data. Metrics such as accuracy, precision, recall, and
F1 Score are commonly used to evaluate the quality of a model. Additionally,
feature importance ratings can be obtained to identify the variables most
significantly influencing the predictions.
Table 9 presents the results of a Random Forest classification model ap-
plied to various cryptocurrency ETFs, such as ARKB, BITB, BRRR, BTCO,
EZBC, FBTC, HODL, and IBIT, over different periods (Daily, 60 minutes,
30 minutes, and 15 minutes) and threshold levels (0.8 and 0.9).
For the
”Daily-0.8”, the Random Forest model exhibits its strongest performance
for several ETFs, including BRRR (0.70), BTCO (0.63), and EZBC (0.74).
These results suggest that daily aggregated data provides more stable and
predictable trends for the Random Forest algorithm, likely due to the re-
duced noise and greater signal strength. Conversely, the performance for
ETFs like BITB and IBIT under ”Daily-0.8” is relatively low, at 0.44 and
0.41, respectively. This disparity indicates that certain ETFs may require ad-
ditional feature engineering or alternative modeling approaches to improve
prediction accuracy.
Moving from daily to 60-minute, 30-minute, and 15-minute intervals, the
performance generally declines for most exchange-traded funds (ETFs). For
example, ARKB drops from 0.63 in ”Daily-0.8” to 0.55 in ”60min-0.8” and
further to 0.51 in ”15min-0.9.” A similar trend is observed for other ETFs,
such as BTCO and EZBC, which experience declines across shorter intervals.
This drop in performance suggests that higher-frequency data may introduce
more noise, which can obscure meaningful patterns that Random Forest relies
on for classification. However, BRRR shows a slightly better performance
at the 60-minute interval with thresholds of 0.8 and 0.9, achieving 0.78 and
0.74, respectively, highlighting its robustness to temporal changes compared
to other ETFs.
20
Preprint not peer reviewed


### Page 23

ARKB
BITB
BRRR
BTCO
EZBC
FBTC
HODL
IBIT
Daily-0.8
0.63
0.44
0.7
0.63
0.74
0.56
0.63
0.41
60 min-0.9
0.57
0.54
0.74
0.49
0.62
0.49
0.65
0.47
60 min-0.8
0.55
0.6
0.78
0.6
0.66
0.56
0.65
0.46
30 min-0.9
0.55
0.47
0.68
0.58
0.66
0.49
0.62
0.51
30 min-0.8
0.52
0.52
0.76
0.63
0.64
0.51
0.73
0.54
15 min-0.9
0.51
0.57
0.71
0.6
0.64
0.51
0.58
0.46
15 min-0.8
0.51
0.52
0.68
0.62
0.7
0.51
0.66
0.53
Table 9:
Random Forest prediction accuracy across various time intervals and thresholds
from January 11 to August 16, 2024.
4.1.4. Using Linear regression for classification
Linear Regression is often used to forecast continuous variables, such as
the price or return of a financial asset. It can also be used to predict price di-
rection by modeling the correlation between independent variables (features)
and the dependent variable, representing the asset’s future price or return.
The regression output is a continuous variable denoting the anticipated price
or return.
Linear Regression can forecast price movement direction (up or down),
with continuous predictions subsequently categorized into binary classifica-
tions. If the expected amount exceeds 0, it may signify an upward trend
(price increase). If the projected number is zero or less, it may indicate a
downward trend, characterized by a price decline. This transformation con-
verts the issue into a binary classification task, emphasizing the direction of
price movement rather than the precise anticipated value. After this, metrics
such as accuracy and precision can be used to evaluate the model’s ability to
predict the direction of prices. Table 10 displays the performance of Linear
Regression predictions converted into a binary classification of price direction
(up or down) across various cryptocurrency ETFs.
In the ”Daily-0.8” model, the best performance is observed for several
ETFs, such as BRRR (0.85) and BTCO (0.85), indicating that the Linear
Regression predictions effectively capture daily price movements for these
assets. For BRRR and BTCO, the model correctly predicted price direc-
tion 85% of the time at the daily level of data. This suggests that daily
21
Preprint not peer reviewed


### Page 24

aggregated data enable the model to capture the underlying trends in price
direction more effectively. However, other ETFs, such as BITB (0.37) and
IBIT (0.59), exhibit significantly lower performance under the same condi-
tions, suggesting that the model struggles to accurately predict the direction
of price movements for these assets.
The overall performance of most ETFs tends to decline in shorter time
intervals, such as 60-minute, 30-minute, and 15-minute data. For example,
ARKB achieves an accuracy of 0.67 under ”Daily-0.8,” which drops to 0.56
and 0.51 under ”30min-0.9” and ”15min-0.9,” respectively. This decline sug-
gests that the Linear Regression model becomes less reliable at predicting
price direction as the time interval shortens, likely due to increased noise
and variability in high-frequency data. Similarly, while BRRR performs well
under ”60min-0.8” (0.86), its performance also decreases at shorter intervals,
reflecting the challenges of predicting direction in noisier, shorter-term data.
ARKB
BITB
BRRR
BTCO
EZBC
FBTC
HODL
IBIT
Daily-0.8
0.67
0.37
0.85
0.85
0.81
0.52
0.78
0.59
60 min-0.9
0.54
0.63
0.78
0.69
0.78
0.58
0.71
0.51
60 min-0.8
0.59
0.65
0.86
0.74
0.78
0.59
0.74
0.42
30 min-0.9
0.56
0.59
0.82
0.68
0.84
0.49
0.72
0.49
30 min-0.8
0.56
0.6
0.84
0.74
0.78
0.54
0.81
0.48
15 min-0.9
0.56
0.59
0.78
0.74
0.77
0.52
0.74
0.53
15 min-0.8
0.61
0.61
0.82
0.75
0.82
0.51
0.8
0.53
Table 10: Linear Regression prediction accuracy across various time intervals and thresh-
olds from January 11 to August 16, 2024.
4.1.5. Artificial Neural Networks
The multilayer perceptron is a widely utilized and adaptable design of
Neural Networks. A multilayer perceptron can approximate diverse func-
tions (see Principe et al. (1999)). The multilayer perceptron’s capacity to
capture nonlinearity is facilitated by employing smooth activation functions
that interlink several layers, with prevalent options being the logistic and
hyperbolic tangent functions.
Moreover, each element of a specific layer
22
Preprint not peer reviewed


### Page 25

influences all components of the subsequent layer. Multilayer Perceptrons
(MLPs) are typically trained using the back-propagation algorithm.
The
back-propagation algorithm transmits faults throughout the network, facili-
tating the adjustment of the hidden processing elements. The MLP is trained
using an error-correcting backpropagation algorithm that requires knowledge
of the system’s desired response. Kara et al. (2011) provides an example of
the successful application of Artificial Neural Networks in the stock market.
This study employs the multilayer perceptron (MLP) model, a type of
Artificial Neural Networks. In the model, we use two hidden layers containing
thirty-four and two nodes, respectively, denoted as (34, 2). The number of
hidden layers is sufficient to identify potential non-linear relationships among
the input features, while the number of nodes aligns with the number of
features examined.
The values in Table 11 reflect the accuracy of the Neural Networks in
predicting the price direction (e.g., ”up” or ”down”) for each ETF. At the
”Daily-0.8” setting, the Neural Networks achieves its best performance for
ETFs such as BRRR (0.85), BTCO (0.85), and EZBC (0.81), suggesting
that daily aggregated data provides the model with clear trends and patterns
to learn from, resulting in accurate predictions for these assets. This high
performance demonstrates the Neural Networks’ capability to generalize well
when the noise is reduced. In contrast, the model’s performance is relatively
weak for ARKB (0.44) and IBIT (0.44), suggesting that these ETFs may
exhibit more volatile or irregular price patterns, which makes them more
challenging for the model to predict accurately.
In the shorter intervals, such as 60-minute, 30-minute, and 15-minute
data, the performance metrics generally decline for most ETFs, reflecting
the challenges of dealing with noisier and more variable data. For instance,
ARKB’s performance improves slightly from 0.44 under ”Daily-0.8” to 0.59
under ”60min-0.8” but then drops to 0.43 under ”15min-0.8.” Similarly, while
BRRR achieves strong results under ”Daily-0.8” and ”60min-0.8” (0.85 and
0.86, respectively), its performance decreases to 0.78 and 0.82 under ”15min-
0.9” and ”15min-0.8,” respectively. This trend highlights the Neural Net-
works’ challenges in maintaining high accuracy as data granularity increases,
likely due to the emergence of increased noise and fewer predictable patterns
over short intervals.
23
Preprint not peer reviewed


### Page 26

ARKB
BITB
BRRR
BTCO
EZBC
FBTC
HODL
IBIT
Daily-0.8
0.44
0.56
0.85
0.85
0.81
0.7
0.81
0.44
60 min-0.9
0.58
0.64
0.78
0.69
0.78
0.59
0.71
0.45
60 min-0.8
0.59
0.65
0.86
0.74
0.78
0.55
0.74
0.49
30 min-0.9
0.56
0.59
0.82
0.68
0.84
0.48
0.72
0.49
30 min-0.8
0.58
0.61
0.84
0.74
0.78
0.51
0.81
0.53
15 min-0.9
0.55
0.59
0.78
0.74
0.77
0.53
0.74
0.54
15 min-0.8
0.43
0.61
0.82
0.75
0.82
0.51
0.8
0.57
Table 11: Artificial Neural Networks prediction accuracy across various time intervals and
thresholds from January 11 to August 16, 2024.
4.1.6. K-means classification
K-means classification is a semi-supervised approach that modifies the
traditional K-means clustering algorithm for classification tasks. While K-
means typically divides data into K clusters based on their similarity, it can
be adapted to assign class labels by associating each cluster with a predefined
category.
In this method, the dataset is first grouped into clusters so that similar
data points are grouped together.
Each point is assigned to the cluster
whose centroid is closest, often determined using a distance metric such as
Euclidean distance. After clustering is completed, class labels are assigned
to each cluster through a majority-voting process, based on the known labels
of the training samples within that cluster. See Bock, H. (2008) for further
details.
An illustrative implementation of K-means classification in Python in-
volves partitioning a dataset into K clusters and assigning labels to the clus-
ters based on a majority vote.
Upon training, the model can categorize
additional data points based on their proximity to the selected cluster cen-
troids. The precision of the classification depends on the alignment of the
clusters with the actual class boundaries, which the structure and separabil-
ity of the data can influence. K-means classification is not a replacement for
supervised learning models, such as Logistic Regression or Neural Networks;
however, it is a valuable method in situations with insufficient labeled data
or where exploratory data analysis is necessary.
Its simplicity, efficiency,
24
Preprint not peer reviewed


### Page 27

and versatility render it an excellent instrument for diverse semi-supervised
learning tasks.
Table 12 represents the results of applying the K-means clustering algo-
rithm to various cryptocurrency ETFs.The K-means method demonstrates
commendable performance for specific ETFs in the ”Daily-0.8” analysis, in-
cluding ARKB (0.70), BRRR (0.81), and BTCO (0.74), suggesting that daily
data reveals distinct patterns for effectively clustering these assets into signif-
icant categories. This indicates that the daily aggregation effectively captures
the dominant trends in the data, enabling the K-means algorithm to form
clusters that closely correspond to the actual class labels. However, the per-
formance for ETFs like BITB (0.48) and IBIT (0.44) is significantly lower,
which may indicate noisier data or weaker feature relationships that make
clustering less effective for these assets.
The performance of most ETFs often declines when the period is de-
creased to shorter intervals, such as 60-minute, 30-minute, and 15-minute
data. For instance, ARKB’s accuracy declines from 0.70 in ”Daily-0.8” to
0.55 in ”60min-0.8” and subsequently to 0.53 in ”15min-0.8.” Similar trends
are observed for BRRR, where the performance drops from 0.81 in ”Daily-
0.8” to 0.55 in ”60min-0.8” and 0.51 in ”15min-0.8.” This decline under-
scores the growing challenge of clustering high-frequency data, where noise
and short-term volatility can obscure the underlying relationships between
features. Such challenges emphasize K-means’ limitations in handling highly
granular data without further preprocessing or feature engineering.
A closer examination of individual ETFs reveals significant variability in
their performance. BRRR and BTCO consistently achieve higher clustering
accuracy, suggesting that these ETFs exhibit more distinct and predictable
patterns that K-means can effectively capture. In contrast, BITB and IBIT
consistently perform poorly in almost all periods, indicating a need for more
effective clustering methods due to their data’s lack of clear separability. This
variability underscores the importance of understanding the unique charac-
teristics of each ETF and adjusting the clustering process accordingly, such
as by optimizing the number of clusters (K) or incorporating domain-specific
features.
4.2. Time series methods
In finance, Random Walk and ARIMA are popular techniques for pre-
dicting prices and simulating time series data. A Random Walk assumes
that future price changes are entirely unknown and occur according to a
25
Preprint not peer reviewed


### Page 28

ARKB
BITB
BRRR
BTCO
EZBC
FBTC
HODL
IBIT
Daily-0.8
0.7
0.48
0.81
0.74
0.74
0.56
0.52
0.44
60 min-0.9
0.44
0.43
0.56
0.55
0.48
0.54
0.49
0.55
60 min-0.8
0.55
0.55
0.55
0.44
0.46
0.51
0.56
0.52
30 min-0.9
0.51
0.51
0.48
0.53
0.51
0.5
0.6
0.46
30 min-0.8
0.48
0.48
0.51
0.54
0.52
0.49
0.73
0.45
15 min-0.9
0.52
0.48
0.38
0.5
0.51
0.49
0.52
0.49
15 min-0.8
0.53
0.49
0.51
0.54
0.52
0.49
0.53
0.53
Table 12: K-means prediction accuracy across various time intervals and thresholds from
January 11 to August 16, 2024.
stochastic process in which the changes are equally distributed and indepen-
dent of each other. According to the Efficient Market Hypothesis, historical
pricing data cannot be used to predict future prices. However, the ARIMA
(Auto-Regressive Integrated Moving Average) approach considers character-
istics such as autocorrelation and trends to make forecasts. ARIMA models
are well-suited for financial time series that exhibit stationarity or can be
made stationary through differencing. Table
ref tab:12 shows the perfor-
mance of the Random Walk and ARIMA methods for forecasting different
cryptocurrency ETFs (ARKB, BITB, BRRR, BTCO, EZBC, FBTC, HODL,
and IBIT) across various time scales.
For the Random Walk method, performance remains relatively consistent
across different periods, with values clustering around 0.62 for shorter inter-
vals, such as 15-minute and 30-minute scales, at a threshold of 0.8. Notably,
the method performs best at the ”Daily-0.8” for several ETFs, including
ARKB, BRRR, and IBIT, achieving a peak performance of 0.62. This con-
sistency aligns with the assumption that price movements follow a stochastic
process and are difficult to predict beyond their randomness. The uniformity
in performance across different cryptocurrencies suggests that the Random
Walk method is largely unaffected by the specific characteristics of each asset,
as it assumes no underlying trends or patterns.
On the other hand, the ARIMA method exhibits more significant per-
formance variability, indicating its dependence on accurately locating trends
and autocorrelations in the time series data. For some ETFs, such as BRRR,
26
Preprint not peer reviewed


### Page 29

ARIMA performs reasonably well, especially at shorter time intervals, like
”15 min-0.8,” where it achieves a performance of 0.62. Other ETFs, such as
ARKB and FBTC, perform worse, with values ranging from 0.47 to 0.50 over
various periods. This suggests that ARIMA struggles to identify significant
patterns for specific cryptocurrencies. This could be due to high volatility or
the lack of stationarity in the data, a crucial prerequisite for ARIMA models.
In conclusion, the Random Walk approach performs better across a range
of ETFs and is more reliable and consistent in its erratic nature. However,
due to its sensitivity to the statistical characteristics of the data, ARIMA
is less dependable overall, even though it exhibits promise for specific assets
and periods. These findings suggest that ARIMA can be beneficial when
trends or autocorrelations are present, particularly in short-term forecasting
scenarios. In contrast, a Random Walk is better suited for general forecasting
in volatile markets.
27
Preprint not peer reviewed


### Page 30

ARKB
BITB
BRRR
BTCO
EZBC
FBTC
HODL
IBIT
Random Walk
15 min-0.8
0.62
0.62
0.62
0.62
0.62
0.62
0.62
0.62
15 min-0.9
0.56
0.56
0.56
0.56
0.57
0.56
0.57
0.56
30 min-0.8
0.61
0.61
0.61
0.61
0.61
0.61
0.61
0.61
30 min-0.9
0.54
0.55
0.55
0.58
0.55
0.55
0.54
0.54
60 min-0.8
0.61
0.61
0.61
0.61
0.61
0.61
0.61
0.61
60 min-0.9
0.54
0.55
0.55
0.58
0.55
0.55
0.54
0.54
Daily-0.8
0.62
0.61
0.62
0.62
0.61
0.61
0.62
0.62
Daily-0.9
0.57
0.58
0.57
0.57
0.58
0.58
0.57
0.57
ARIMA
15 min-0.8
0.47
0.62
0.47
0.48
0.47
0.62
0.48
0.48
15 min-0.9
0.53
0.53
0.53
0.53
0.56
0.53
0.57
0.56
30 min-0.8
0.5
0.5
0.5
0.49
0.5
0.5
0.5
0.61
30 min-0.9
0.56
0.56
0.56
0.57
0.55
0.55
0.56
0.54
60 min-0.8
0.5
0.5
0.61
0.61
0.61
0.5
0.61
0.61
60 min-0.9
0.56
0.56
0.56
0.54
0.56
0.56
0.56
0.54
Daily-0.8
0.52
0.51
0.52
0.52
0.51
0.5
0.52
0.51
Daily-0.9
0.54
0.44
0.54
0.54
0.44
0.44
0.54
0.53
Table 13: Performance of Random Walk and ARIMA time series forecasting over different
crypto ETFs and different time scales from January 11 to August 16, 2024.
28
Preprint not peer reviewed


### Page 31

5. Comparative analysis
This section compares the implemented methods using ROC curves and
different tests. The ROC curves compare the performance of several models
based on their ability to classify outcomes accurately. According to Figure
2, the Neural Networks model achieved the highest AUC (0.60), indicating it
performed better than the others, though its performance is still moderate.
Logistic Regression and SVM both had AUCs around 0.53, showing only a
slight improvement over random guessing. Linear Regression and Decision
Tree models also performed similarly with AUCs around 0.52.
Figure 2: Comparison of model performance using ROC curves from January 11 to August
16, 2024.
Tables A.1, A.2, and A.3 in the Appendix provide a comparative analysis
using t-tests to evaluate ARIMA against several machine learning models and
benchmarks. This analysis covers various time scales, including 15 minutes,
30 minutes, 60 minutes, 6 hours, and daily intervals.
29
Preprint not peer reviewed


### Page 32

The results in Table A.1 show that ARIMA consistently outperforms the
Random Walk benchmark, as well as Neural Networks, K-means, Logistic Re-
gression, Decision Trees, SVM, and Linear Regression. The t-values, which
are predominantly negative across all time scales, highlight the statistical sig-
nificance of ARIMA’s superior performance. With significance levels often at
1%, ARIMA, for example, shows a decisive advantage over Neural Networks
and K-means, further validating its statistical significance. The reliability of
ARIMA is further supported by its superiority over Logistic Regression and
Decision Trees, being evident across time intervals, with most results being
significant at the 1% or 5% levels.
Table A.2 reveals a consistent pattern where SVM generally outperforms
K-means across all time scales, with positive t-values that are significant at
the 1% level, reflecting a robust statistical difference. However, when SVM
is compared to Logistic Regression, Decision Trees, and other models, the
t-values are close to zero and often not statistically significant, indicating
little to no difference in performance between these methods in most cases.
Comparisons with K-means demonstrate significantly higher performance
for Linear Regression, with positive t-values consistently significant at the
1% level.
This indicates a clear advantage of Linear Regression over K-
means. In contrast, the comparisons between Linear Regression and Logistic
Regression, Neural Networks, and Decision Trees yield t-values near zero,
with no significant differences observed across the time scales. This suggests
that Linear Regression and these models yield similar results for the given
tasks.
As shown by the positive t-values significant at the 1% level, the Table A.3
findings consistently favor Logistic Regression when compared to K-means
across all time scales. This suggests that Logistic Regression outperforms K-
means by a significant and reliable margin. With t-values that are positive
and statistically significant, Decision Trees also perform noticeably better
than K-means at most time scales, demonstrating their superiority over K-
means.
Nevertheless, when comparing Neural Networks and K-means, the t-
values are negative and not statistically significant. This indicates no dif-
ference in the performance of the two models across the tested scenarios,
suggesting that K-means and Neural Networks perform similarly on various
classification tasks.
The t-values for Decision Trees and Neural Networks are comparable,
and no statistical significance is seen over time scales. This suggests that the
30
Preprint not peer reviewed


### Page 33

performance of these two models is similar. Similarly, as the t-values stay
close to zero and are not statistically significant throughout all periods, there
are no discernible performance differences between Logistic Regression and
Neural Networks.
The Tables A.4, A.5 and A.6 present the results of the Wilcoxon signed-
rank test, which compares the performance of ARIMA and several classifi-
cation algorithms such as Logistic Regression, Decision Tree, SVM, Linear
Regression, Neural Networks over different time scales, including daily, 15
minutes, and 30 minutes. The p-values and signed-rank statistics are pro-
vided for each comparison, with significance levels denoted by *, **, and ***
at the 10%, 5%, and 1% levels, respectively.
In Table A.4, ARIMA consistently outperforms Random Walk across all
time scales, as indicated by statistically significant results at most significance
levels. This highlights ARIMA’s ability to capture patterns that extend be-
yond baseline random processes. Compared to Logistic Regression, Linear
Regression, and SVM, ARIMA’s superiority is reflected in significant p-values
for many time intervals, suggesting its robust predictive performance relative
to these algorithms. However, the comparison with Decision Trees and Neu-
ral Networks reveals mixed results, with some time scales showing significant
differences while others do not, indicating context-dependent performance.
In Table A.5, SVM consistently produces tiny p-values, indicating that it
performs much better than K-means on all time scales. Likewise, SVM per-
forms strongly across temporal resolutions, outperforming Logistic Regres-
sion in numerous cases. Less consistency exists in the results when compar-
ing Decision Trees and Linear Regression; some time scales show statistically
significant differences, while others do not, indicating context-dependent per-
formance advantages. Results from comparing Neural Networks with Linear
Regression are mixed, with notable differences at specific time scales. This
suggests that, under some circumstances, Neural Networks may be particu-
larly effective at modeling temporal dependencies. These findings highlight
the differences in relative performance among various models, which vary
depending on the time scale and data properties. Specifically, SVM typically
demonstrates superior performance compared to alternative approaches.
The results in Table A.1 show that ARIMA consistently outperforms the
Random Walk benchmark, as well as Neural Networks, K-means, Logistic Re-
gression, Decision Trees, SVM, and Linear Regression. The t-values, which
are predominantly negative across all time scales, highlight the statistical sig-
nificance of ARIMA’s superior performance. With significance levels often at
31
Preprint not peer reviewed


### Page 34

1%, ARIMA, for example, shows a decisive advantage over Neural Networks
and K-means, further validating its statistical significance. The reliability
of ARIMA is further supported by its superiority over Logistic Regression
and Decision Trees, being visible over time intervals, with most results being
significant at the 1% or 5% levels.
Table A.2 reveals a consistent pattern where SVM generally outperforms
K-means across all time scales, with positive t-values that are significant at
the 1% level, reflecting a robust statistical difference. However, when SVM
is compared to Logistic Regression, Decision Trees, and other models, the
t-values are close to zero and often not statistically significant, indicating
little to no difference in performance between these methods in most cases.
The comparison against K-means shows significantly higher performance
for Linear Regression, with positive t-values consistently significant at the
1% level.
This indicates a clear advantage of Linear Regression over K-
means. In contrast, the comparisons between Linear Regression and Logistic
Regression, Neural Networks, and Decision Trees yield t-values near zero,
with no significant differences observed across the time scales. This suggests
that Linear Regression and these models yield similar results for the given
tasks.
As shown by positive t-values significant at the 1% level, the Table A.3
findings consistently favor Logistic Regression when compared to K-means
across all time scales. This suggests that Logistic Regression outperforms K-
means by a significant and reliable margin. With t-values that are positive
and statistically significant, Decision Trees also perform noticeably better
than K-means at most time scales, demonstrating their superiority over K-
means.
Nevertheless, when compared, the t-values for Neural Networks and K-
means are not statistically significant. This indicates no difference in the
performance of the two models across the tested scenarios, suggesting that
K-means and Neural Networks perform similarly on various classification
tasks.
The t-values for Decision Trees and Neural Networks are nearly equal,
and no statistical significance is seen over time scales. This suggests that the
performance of these two models is similar. Similarly, as the t-values stay
close to zero and are not statistically significant throughout all periods, there
are no discernible performance differences between Logistic Regression and
Neural Networks.
Tables A.4, A.5 and A.6 present the results of the Wilcoxon signed-rank
32
Preprint not peer reviewed


### Page 35

test, which compares the performance of ARIMA and several classification
algorithms such as Logistic Regression, Decision Tree, SVM, Linear Regres-
sion, Neural Networks over different time scales, including daily, 15 minutes,
and 30 minutes. The p-values and signed-rank statistics are provided for
each comparison, with significance levels denoted by *, **, and *** at the
10%, 5%, and 1% levels, respectively.
In Table A.4, ARIMA consistently outperforms Random Walk across all
time scales, as indicated by statistically significant results at most signifi-
cance levels. This highlights ARIMA’s ability to capture patterns that ex-
tend beyond baseline random processes. Compared to Logistic Regression,
Linear Regression, and SVM, ARIMA’s superiority is reflected in significant
p-values for many time intervals, suggesting its robust predictive performance
relative to these algorithms. However, the comparison with Decision Trees
and Neural Networks reveals mixed outcomes, with some time scales show-
ing significant differences while others do not, indicating context-dependent
performance.
In Table A.5, SVM consistently produces tiny p-values, indicating that it
performs much better than K-means on all time scales. Likewise, SVM per-
forms strongly across temporal resolutions, outperforming Logistic Regres-
sion in numerous cases. Less consistency exists in the results when compar-
ing Decision Trees and Linear Regression; some time scales show statistically
significant differences, while others do not, indicating context-dependent per-
formance advantages. Results from comparing Neural Networks with Linear
Regression are mixed, with notable differences at specific time scales. This
suggests that, under certain circumstances, Neural Networks may be par-
ticularly well-suited for capturing intricate temporal patterns. These find-
ings highlight the differences in relative performance among various models,
which vary depending on the time scale and data properties. Specifically,
SVM typically demonstrates superior performance compared to alternative
approaches.
Statistically significant differences identified by low p-values and high
significance levels in Table A.6 demonstrate that Neural Networks regularly
perform better than the alternative approaches in almost all cases.
This
suggests that Neural Networks outperform other dataset configurations re-
garding performance and generalization.
Though it performs marginally worse than Neural Networks, Logistic Re-
gression comes second, routinely exceeding K-means and consistently out-
performing Decision Trees. Neural Networks have a distinct advantage over
33
Preprint not peer reviewed


### Page 36

Logistic Regression, as evidenced by the frequently statistically significant
differences between the two.
Although there are notable differences in many comparisons, K-means
outperforms Decision Trees in most cases; however, it is still less efficient
than Neural Networks and Logistic Regression. Decision Trees continually
perform worse than all other methods, making them the poorest approach
in this examination. These results demonstrate that Neural Networks are
the most reliable and successful classification technique in this assessment,
followed by Decision Trees, K-means, and Logistic Regression.
6. Robustness analysis
Random smoothing is a popular probabilistic machine learning strategy
for enhancing classifier robustness, particularly against adversarial attacks.
Adding random noise to the input and aggregating predictions across several
noisy samples transforms any base classifier into a certifiably robust one. The
central concept is building a ”smoothed” classifier that generates the most
likely prediction by applying the underlying classifier’s majority vote to the
noisy inputs. This technique guarantees that small input changes, including
those caused by adversarial attacks, are unlikely to change the model’s final
forecast.
First, we subject the input data to random noise, typically Gaussian or
uniform. The predictions made by the base classifier are then assessed by
the smoothed classifier using several noisy iterations of the same input. The
smoothed classifier produces a robust final result by obtaining the majority
vote across these predictions. Additionally, randomized smoothing provides
a formal robustness certification of resilience by guaranteeing that the clas-
sifier’s prediction remains stable within a perturbation radius of the input.
This radius depends on several variables, including the model’s prediction
confidence and the kind and magnitude of the noise distribution.
Randomized smoothing offers several essential applications. It is instru-
mental in defending against adversarial attacks, where minor alterations to
input data can deceive conventional machine-learning models. By demon-
strating resilience, randomized smoothing ensures that a model’s predictions
stay consistent despite such attacks. Additionally, this method aids in assess-
ing prediction uncertainty by analyzing the variability introduced by noise.
34
Preprint not peer reviewed


### Page 37

Figure 3: Randomized smoothing analysis from January 11 to August 16, 2024.
The theoretical foundation for randomized smoothing was formalized in
research such as ”Certified Defenses for Adversarial Examples via Random-
ized Smoothing” by Cohen et al. (2019), which established its effectiveness
as a defense mechanism. Since then, further work has explored variations of
noise distributions and applications beyond adversarial robustness.
Figure 3 shows the relationship between the noise level and the mean
squared error (MSE) for various machine learning models under the random-
ized smoothing framework. The key aspects of the results can be interpreted
as follows:
As the noise level increases, all models’ mean squared error (MSE) gener-
ally rises, indicating that higher levels degrade prediction accuracy. Among
the models, K-means and Logistic Regression exhibit significantly lower MSE
across the range of noise levels, suggesting these methods are more robust
to noise. ARIMA and Random Walk, being traditional time-series models,
maintain relatively stable MSEs under lower noise levels but diverge at higher
noise levels.
Conversely, Neural Networks and SVMs experience the steepest growth
35
Preprint not peer reviewed


### Page 38

in MSE as noise levels increase, highlighting their sensitivity to perturba-
tions introduced by randomized smoothing. This aligns with their known
susceptibility to adversarial perturbations, given their lack of robust defense
mechanisms.
The standout performance of Logistic Regression and K-means underlines
their suitability for robust tasks, especially when randomized smoothing is
applied. Conversely, the degradation in Neural Networks’ performance high-
lights the need for further robustness enhancements in deep learning models
for noisy environments.
7. Trading strategies
Financial markets enable investors to buy and sell various assets, profit-
ing from price fluctuations. These fluctuations can be much more significant
in the digital currency market than in other financial markets. Despite em-
ploying various methods, such as technical analysis, accurately identifying
cryptocurrency trends remains a challenging task.
However, these fluctuations are significantly more pronounced in cryp-
tocurrency markets than in other financial markets. Despite various meth-
ods, such as technical analysis, it is not easy to accurately identify the trend
of cryptocurrencies. The price of a cryptocurrency either increases or de-
creases. Therefore, profiting might seem easy in theory. However, the most
critical point that many investors miss is determining the optimal price to
make a purchase and the optimal price to sell the purchased cryptocurrency.
One way to mitigate such risks is to employ effective trading strategies.
The buy-and-hold strategy is a popular and passive approach to invest-
ing in cryptocurrencies. In this strategy, investors buy cryptocurrencies and
hold them for an extended period, regardless of short-term market fluctua-
tions. This approach relies more on fundamental analysis, emphasizing cryp-
tocurrencies’ long-term value and growth potential, rather than focusing on
technical indicators or daily fluctuations. The primary objective of the hold
strategy is to capitalize on the long-term appreciation of cryptocurrencies.
In other words, investors can reduce risk by avoiding hasty decisions, such
as selling low-priced assets or buying at peak prices.
Dollar-cost averaging (DCA) is another strategy that enables you to invest
in the market regularly and gradually, focusing on long-term benefits. It
involves dividing your investment into smaller portions and injecting them
into the market regularly, such as weekly or monthly.
This method has
36
Preprint not peer reviewed


### Page 39

Figure 4: Comparison of Buy and Hold strategy of eight crypto ETFs from January 11 to
August 16, 2024.
several significant advantages. First, it allows you to buy at regular intervals,
regardless of whether prices are high or low, thereby reducing the impact of
short-term fluctuations on your average cost. Second, it eliminates the need
for daily analysis or detailed forecasts, allowing you to invest automatically
with a more optimistic outlook.
The last one is Momentum trading in cryptocurrency markets. This strat-
egy is based on the principle that assets performing well will continue to do
so. In contrast, those underperforming or showing weaker performance com-
pared to the market average will likely continue declining. This approach
relies on identifying trends and capitalizing on market movements driven by
investor sentiment, technical patterns, and trading volume. At its core, mo-
mentum trading involves recognizing assets that exhibit strong upward or
downward trends. Traders, armed with technical indicators such as moving
averages, the Relative Strength Index (RSI), and the Moving Average Con-
vergence/Divergence (MACD), can gauge the trend’s strength and identify
potential entry or exit points, thereby gaining valuable insights. Refer to
‘Evaluating Trading Strategies’ by Harvey et al.(2014).
Figures 4, 5, and 6 illustrate the Buy-and-Hold, DCA, and Momentum
strategies for cryptocurrency ETFs.The Momentum strategy emerges as the
most profitable, dynamically shifting investments toward the best-performing
37
Preprint not peer reviewed


### Page 40

Figure 5: Comparison of DCA strategy of eight crypto ETFs from January 11 to August
16, 2024.
Figure 6: Comparison of the Momentum strategy of eight crypto ETFs from January 11
to August 16, 2024.
ETFs and capitalizing on strong upward trends. This approach, however,
38
Preprint not peer reviewed


### Page 41

comes with heightened volatility, as evidenced by sharp fluctuations and
occasional steep declines when trends reverse. In contrast, the Buy-and-Hold
strategy follows a more moderate growth trajectory, benefiting from the long-
term appreciation of the cryptocurrency market. While it endures significant
short-term volatility, investors using this approach must be willing to tolerate
market drawdowns, knowing that, historically, crypto assets have trended
upward over extended periods, providing reassurance and confidence in this
strategy. Meanwhile, the DCA strategy presents the most stable investment
path. It gradually accumulates positions over time to mitigate the impact of
market downturns. Unlike Buy-and-Hold, which exposes the investor to the
entire market risk at all times, DCA smooths out volatility, resulting in a less
erratic performance curve. Although this method sacrifices some potential
upside during bull markets, it provides greater resilience during corrections,
making it a safer and more secure choice for risk-averse investors.
It’s also important to note that several transaction fees are associated with
investing in cryptocurrency exchange-traded funds (ETFs), which may affect
total returns. These expenses fall into two categories: explicit costs, which
include direct fees and commissions, and implicit costs, which encompass
market-related expenses such as slippage and spreads.
The expense ratio shows the ETF provider’s recurring management fee.
The complexity of managing cryptocurrency assets, custody solutions, and
regulatory compliance sometimes results in expense ratios for crypto ETFs
greater than those for standard ETFs, usually ranging from 0.25% to 1.5%
annually.
Crypto ETFs provide regulatory control and ease compared to
direct cryptocurrency ownership, but they also have transaction costs that
can reduce profits. Although they still suffer annual expenditure ratios, buy-
and-hold investors are less impacted by bid-ask spreads and trading charges.
On the other hand, because of spreads, slippage, and frequent transactions,
active traders incur higher costs. Understanding these expenses is crucial for
selecting the optimal ETF strategy and maximizing long-term returns.
8. Conclusion
In an era where cryptocurrencies have become one of the most significant
and popular topics in the financial world, crypto ETFs have emerged as a
focal point of one of the most exciting, innovative, and controversial develop-
ments in this field. The term ETF refers to exchange-traded funds that act
as a bridge between the stock market and various assets. Cryptocurrencies
39
Preprint not peer reviewed


### Page 42

have led the world to a new concept of currencies and types of transactions,
but owning and investing in this asset has often been accompanied by chal-
lenges. For this reason, the crypto ETFs, designed and offered by reputable
companies and financial professionals, serve as a credible vehicle for investors
to participate indirectly in cryptocurrencies by purchasing a unit of this fund.
This study employs machine learning classification algorithms to inves-
tigate the predictability of eight significant cryptocurrency exchange-traded
funds across four distinct time scales: daily, 15-minute, 30-minute, and 60-
minute returns.
Numerical experiments using classification methods such
as Logistic Regression, Linear Regression, Support Vector Machines, Artifi-
cial Neural Networks, K-means Clustering, and Random Forest algorithms
demonstrate the predictability of upward or downward price movements.
By comparing the accuracy values across models, the Neural Networks
and SVM models exhibit the highest accuracy values, often exceeding 0.80,
with some values reaching 0.86.
These models consistently perform well
across different time frames and conditions. The Decision Tree and K-means
Clustering models exhibit moderate accuracy, typically ranging from 0.55 to
0.78, which makes them less reliable for high-precision predictions. While
struggling with non-linear data patterns, the Linear Regression and Logis-
tic Regression models offer an advantage in model transparency and inter-
pretability, which you can appreciate. Their accuracy levels generally range
from 0.75 to 0.78.
Moreover, we compared the methods using the t-test and signed-rank
test. Additionally, we discussed strategies in the crypto ETF market and
concluded that the best approach depends on an investor’s risk tolerance
and objectives. If maximizing returns is the priority and one can withstand
sharp drawdowns, the Momentum strategy offers the most significant growth
potential. If an investor seeks long-term gains with moderate risk exposure,
the Buy-and-Hold approach is a solid and reassuring choice. DCA provides
the most balanced approach for those prioritizing stability and a methodi-
cal entry into the market, effectively mitigating the unpredictable nature of
cryptocurrency markets. The findings of this study have important impli-
cations for market efficiency. First, if the crypto ETF market were efficient
in the weak-form, its past price movements would not help us forecast fu-
ture returns. However, our findings suggest that applying machine learning
tools to historical prices is a game-changer, enabling the successful prediction
of returns at the intraday level. This technological advancement is signifi-
cant for algorithmic trading, as it successfully automates decisions on when
40
Preprint not peer reviewed


### Page 43

to buy and sell cryptocurrencies within a day. The success of such newly
developed algorithms may also lead to more high-tech, dominant financial
markets, marking a new era in the industry.
This inefficiency can also benefit institutional investors with access to
sophisticated data analytics and trading tools, allowing them to exploit mar-
ket anomalies more effectively. However, it’s crucial to note that unique risks
are present in the context of crypto ETFs, where the market is still evolving
and regulatory clarity is developing. These risks, coupled with the potential
for prolonged inefficiencies, may lead to increased volatility and higher risks
for passive investors. We can significantly improve efficiency as the cryp-
tocurrency market evolves and institutional adoption increases. The unique
characteristics of digital assets, such as high volatility, fragmented liquid-
ity, and changing regulations, indicate that some inefficiencies may persist
longer than we would like. However, embracing these challenges can drive
innovation and ultimately build a stronger and more resilient market.
9. Acknowledgments
While preparing this work, the authors used AI tools to check, correct,
and organize text for more readability and precision.
41
Preprint not peer reviewed


### Page 44

References
Bariviera, Aurelio F. ”The inefficiency of Bitcoin revisited: A dynamic ap-
proach.” Economics Letters 161 (2017): 1–4.
Bock, Hans-Hermann. ”Origins and extensions of the K-means algorithm in
cluster analysis.” Electronic Journal for History of Probability and Statistics
4, no. 2 (2008): 1–18.
Brock, William, Josef Lakonishok, and Blake LeBaron. ”Simple technical
trading rules and the stochastic properties of stock returns.” The Journal
of Finance 47, no. 5 (1992): 1731–1764.
Cohen, Jeremy, Elan Rosenfeld, and Zico Kolter. ”Certified defenses for
adversarial examples via randomized smoothing.” (2019).
Fama, Eugene F. ”Efficient capital markets.” Journal of Finance 25, no. 2
(1970): 383–417.
Harvey, Campbell R., and Yan Liu. ”Evaluating trading strategies.” Avail-
able at SSRN 2474755 (2014).
Hoang, Daniel, and Kevin Wiegratz. ”Machine learning methods in finance:
Recent applications and prospects.” European Financial Management 29,
no. 5 (2023): 1657–1701.
Huang, Hui-Ling, and Fang-Lin Chang. ”ESVM: Evolutionary support vec-
tor machine for automatic feature selection and classification of microarray
data.” Biosystems 90, no. 2 (2007): 516–528.
Kim, Kyoung-jae, and Ingoo Han. ”Genetic algorithms approach to feature
discretization in Artificial Neural Networks for the prediction of stock price
index.” Expert Systems with Applications 19, no. 2 (2000): 125–132.
Lamport, Leslie. A Document Preparation System. 2nd ed., Addison Wesley,
Massachusetts, 1994.
“Andrew W. Lo. and A. Craig MacKinlay. ”Stock market prices do not fol-
low Random Walks: Evidence from a simple specification test.” The Review
of Financial Studies 1, no. 1 (1988): 41–66.
42
Preprint not peer reviewed


### Page 45

Mazouz, Khelifa, and Michael Bowe. ”The volatility effect of futures trad-
ing: Evidence from LSE traded stocks listed as individual equity futures
contracts on LIFFE.” International Review of Financial Analysis 15, no. 1
(2006): 1–20.
Mensi, Walid, Khamis Hamed Al-Yahyaee, and Sang Hoon Kang. ”Struc-
tural breaks and double long memory of cryptocurrency prices: A compar-
ative analysis from Bitcoin and Ethereum.” Finance Research Letters 29
(2019): 222–230.
Petajisto, Antti. ”Inefficiencies in the pricing of exchange-traded funds.”
Financial Analysts Journal 73, no. 1 (2017): 24–54.
Poterba, James M., and Lawrence H. Summers. ”Mean reversion in stock
prices: Evidence and implications.” Journal of Financial Economics 22, no.
1 (1988): 27–59.
Principe, Jose C., Neil R. Euliano, and W. Curt Lefebvre. Neural and Adap-
tive Systems: Fundamentals Through Simulations with CD-ROM. John Wi-
ley & Sons, Inc., 1999.
Sensoy, Ahmet. ”The inefficiency of Bitcoin revisited: A high-frequency
analysis with alternative currencies.” Finance Research Letters 28 (2019):
68–73.
Shih, Kuang-Hsun, Yi-Hsien Wang, I. Kao, and Fu-Ming Lai. ”Forecasting
ETF Performance: A Comparative Study of Deep Learning Models and the
Fama-French Three-Factor Model.” Mathematics 12, no. 19 (2024).
Tartakovsky, Eugene, Ksenia Plesovskikh, Anastasiia Sarmakeeva, and
Alexander Bibik. ”Autocorrelation of returns in major cryptocurrency mar-
kets.” arXiv preprint arXiv:2003.13517 (2020).
Urquhart, Andrew. ”The inefficiency of Bitcoin.” Economics Letters 148
(2016): 80–82.
Li, Yi, Wei Zhang, Andrew Urquhart, and Pengfei Wang. ”The role of media
coverage in the bubble formation: Evidence from the Bitcoin market.” Jour-
nal of International Financial Markets, Institutions and Money 80 (2022):
101629.
43
Preprint not peer reviewed


### Page 46

Vidal-Tom´as, David, and Ana Iba˜nez. ”Semi-strong efficiency of Bitcoin.”
Finance Research Letters 27 (2018): 259–265.
Wilder Jr, J. Wells. ”The relative strength index.” Technical Analysis of
Stocks and Commodities 4 (1986): 343-346.
44
Preprint not peer reviewed


### Page 47

Appendix A.
The Appendix
A includes t-test results and Wilcoxon’s rank test for
comparing all methods.
45
Preprint not peer reviewed


### Page 48

Table A.1: t test results for comparison of classification algorithms and time series methods over different time scales from
January 11 to August 16, 2024.
t-test
ARIMA vs
ARIMA vs Linear
ARIMA
ARIMA vs
ARIMA vs Logistic
ARIMA vs
ARIMA vs
Random Walk
Regression
vs SVM
Decision Tree
Regression
K-means
Neural Networks
15 min 0.8
-4.65 (***)
-3.31 (***)
-3.53 (***)
-2.19 (**)
-3.48 (***)
-0.36
-2.62 (**)
15 min 0.9
-3.29 (**)
-2.71 (**)
-2.84 (**)
-1.08
-2.67 (**)
3.42 (***)
-2.78 (**)
60 min 0.8
-1.95 (*)
-1.94 (*)
-2.10 (*)
-0.97
-1.98 (*)
2.07 (*)
-2.15 (*)
60 min 0.9
0.79
-2.70 (**)
-3.52 (***)
-0.49
-3.59 (***)
2.61 (**)
-2.45 (**)
30 min 0.8
-6.92 (***)
-3.10 (**)
-3.57 (***)
-2.50 (**)
-3.43 (***)
-0.30
-3.33 (***)
30 min 0.9
1.32
-1.90 (*)
-1.86
-0.47
-1.96 (*)
3.08(**)
-1.83
Daily 0.8
-29.04 (***)
-2.68 (**)
-3.50 (***)
-1.91 (*)
-3.87 (***)
-2.24 (*)
-2.72 (**)
The values in the parentheses are t-statistics. ***, ** and * denote significance at the 1%, 5% and 10% level
respectively
46
Preprint not peer reviewed


### Page 49

Table A.2: t test results for comparison of classification algorithms and time series methods over different time scales from
January 11 to August 16, 2024.
t-test
Linear Regression
Linear Regression vs
Linear Regression
Linear Regression vs
SVM vs
SVM vs Logistic
SVM vs
vs Decision Tree
Logistic Regression
vs K-means
Neural Networks
Decision Tree
Regression
K-means
15 min 0.8
1.64
-0.05
3.48 (***)
0.25
1.78 (*)
0.02
3.75 (***)
15 min 0.9
1.60
0.01
3.85 (***)
-0.03
1.68
0.06
4.00 (***)
60 min 0.8
1.09
0.01
3.05 (**)
-0.05
1.18
0.04
3.28 (**)
60 min 0.9
1.66
-0.28
3.63 (***)
0.02
2.06 (*)
-0.03
4.41 (***)
30 min 0.8
1.03
-0.11
2.55 (**)
-0.08
1.26
0.04
2.89 (**)
30 min 0.9
1.43
-0.02
2.73 (**)
0.03
1.39
-0.04
2.68 (**)
Daily 0.8
1.18
-0.35
0.70
-0.05
1.63
-0.06
1.07
The values in the parentheses are t-statistics. ***, ** and * denote significance at the 1%, 5% and 10% level
respectively
47
Preprint not peer reviewed


### Page 50

Table A.3: t test results for comparison of classification algorithms and time series methods over different time scales from
January 11 to August 16, 2024.
t-test
SVM vs Neural
Decision Tree vs
Decision Tree
Decision Tree vs
Logistic Regression
Logistic Regression
K-means vs
Network
Logistic Regression
vs K-means
Neural Networks
vs K-means
vs Neural Networks
Neural Networks
15 min 0.8
0.32
-1.75
2.44 (**)
-1.17
3.69 (***)
0.30
-2.67 (**)
15 min 0.9
0.01
-1.58
2.70 (**)
-1.65
3.81 (***)
-0.05
-3.92 (***)
60 min 0.8
-0.02
-1.10
2.47 (**)
-1.21
3.12 (**)
-0.06
-3.35 (***)
60 min 0.9
0.26
-2.09 (*)
1.72
-1.56
4.47 (***)
0.29
-3.36 (***)
30 min 0.8
0.07
-1.20
1.81 (*)
-1.15
2.78 (**)
0.03
-2.71 (**)
30 min 0.9
0.01
-1.47
1.90 (*)
-1.38
2.80 (**)
0.05
-2.65 (**)
Daily 0.8
0.22
-1.78 (*)
-0.50
-1.23
1.18
0.29
-0.75
The values in the parentheses are t-statistics. ***, ** and * denote significance at the 1%, 5% and 10% level
respectively
48
Preprint not peer reviewed


### Page 51

Table A.4: Wilcoxon signed rank test results for comparison of classification algorithms and time series methods over different
time scales from January 11 to August 16, 2024.
signed rank
ARIMA vs
ARIMA vs Linear
ARIMA vs SVM
ARIMA vs
ARIMA vs Logistic
ARIMA vs
ARIMA vs
Random Walk
Regression
Decision Tree
Regression
K-means
Neural Networks
15 min 0.8
(1.0), p = 0.0156 **
(4.0), p = 0.0547 *
(4.0), p = 0.0547 *
(7.0), p = 0.1484
(4.0), p = 0.0547 *
(15.0), p = 0.7422
(7.0), p = 0.1484
15 min 0.9
(0.0), p=0.0078 ***
(4.0), p = 0.0547 *
(2.0), p = 0.0234 **
(12.0), p = 0.4609
(4.0), p = 0.0547 *
(0.0), p = 0.0078 ***
(3.0), p = 0.0391 **
60 min 0.8
(15.0), p=0.7422
(7.0), p = 0.1484
(4.0), p=0.0547 *
(8.0), p = 0.1953
(6.0), p = 0.1094
(6.0), p = 0.1094
(3.0), p = 0.0391 **
60 min 0.9
(9.0), p = 0.2500
(4.0), p = 0.0547 *
(0.0), p = 0.0078 ***
(16.0), p = 0.8438
(0.0), p = 0.0078 ***
(5.0), p = 0.0781 *
(4.0), p=0.0547 *
30 min 0.8
(1.0), p = 0.0156 **
(4.0), p = 0.0547 *
(2.0), p = 0.0234 **
(4.0), p = 0.0547 *
(3.0), p = 0.0391 **
(17.0), p=0.9453
(2.0), p = 0.0234 **
30 min 0.9
(3.0), p = 0.0391 **
(7.0), p = 0.1484
(7.0), p = 0.1484
(16.0), p = 0.8438
(8.0), p = 0.1953
(1.0), p = 0.0156 **
(7.0), p = 0.1484
Daily 0.8
(0.0), p = 0.0078 ***
(3.0), p = 0.0391 **
(2.0), p = 0.0234 **
(5.0), p = 0.0781 *
(0.0), p = 0.0078 ***
(7.0), p = 0.1484
(5.0), p = 0.0781 *
The values in the parentheses are t-statistics. ***, ** and * denote significance at the 1%, 5% and 10% level
respectively
49
Preprint not peer reviewed


### Page 52

Table A.5: Wilcoxon signed rank test results for comparison of classification algorithms and time series methods over different
time scales from January 11 to August 16, 2024.
signed rank
Linear Regression
Linear Regression vs
Linear Regression
Linear Regression vs
SVM vs
SVM vs Logistic
SVM vs
vs Decision Tree
Logistic Regression
vs K-means
Neural Networks
Decision Tree
Regression
K-means
15min 0.8
(1.0), p=0.0156 **
(5.0), p=1.0000
(1.0), p=0.0156 **
(7.0), p=0.8927
(0.0), p=0.0078 ***
(0.0), p=0.1088
(0.0), p=0.0078 ***
15min 0.9
(0.0), p=0.0078 ***
(1.0), p=0.2850
(0.0), p=0.0078 ***
(3.0), p=0.4652
(0.0), p=0.0000
(0.0), p=0.0000
(0.0), p=0.0078 ***
60min 0.8
(2.0), p=0.0234 **
(3.0), p=1.0000
(3.0), p=0.391 **
(2.0), p=0.5930
(0.0), p=0.0000
(1.0), p=0.2850
(0.0), p=0.0180 **
60min 0.9
(1.0), p=0.0156 **
(0.0), p=0.0679 *
(1.5), p=0.0234 **
(4.0), p=0.7150
(0.0), p=0.0000
(0.0), p=0.0078 ***
(0.0), p=0.0078 ***
30min 0.8
(3.0), p=0.0391 **
(2.0), p=0.2733
(1.1), p=0.2850
(3.0), p=0.4652
(0.0), p=0.0000
(0.0), p=0.0078 ***
(0.0), p=0.0078 ***
30min 0.9
(3.0), p=0.0391 **
(1.0), p=0.6547
(1.0), p=0.0156 **
(0.0), p=0.1797
(4.0), p=1.0000
(1.0), p=0.0156 **
(0.0), p=0.0178 **
Daily 0.8
(5.0), p=0.0781 *
(1.0), p=0.2850
(8.5), p=0.2500
(7.0), p=0.8927
(0.0), p=0.0000
(0.0), p=0.0178 **
(0.0), p=0.0178 **
The values in the parentheses are t-statistics. ***, ** and * denote significance at the 1%, 5% and 10% level
respectively
50
Preprint not peer reviewed


### Page 53

Table A.6: Wilcoxon signed rank test results for comparison of classification algorithms and time series methods over different
time scales from January 11 to August 16, 2024.
signed rank
SVM vs Neural
Decision Tree vs
Decision Tree
Decision Tree vs
Logistic Regression
Logistic Regression vs
K-means vs
Network
Logistic Regression
vs K-means
Neural Networks
vs K-means
Neural Networks
Neural Networks
15min 0.8
(4.0), p=0.7150
(1.0), p=0.0156 **
(3.0), p=0.0391 **
(4.0), p=0.0547 *
(0.0), p=0.0078 ***
(0.0), p=0.0078 ***
(3.0), p=0.0391 **
15min 0.9
(7.0), p=0.8927
(4.0), p=0.0547 *
(0.0), p=0.0078 ***
(0.0), p=0.0078 ***
(0.0), p=0.0078 ***
(0.0), p=0.0078 ***
(0.0), p=0.0078 ***
60min 0.8
(0.0), p=0.1797
(1.0), p=0.2850
(3.0), p=0.0630 *
(1.0), p=0.0156 **
(1.0), p=0.0156 **
(3.0), p=0.0391 **
(1.0), p=0.0156 **
60min 0.9
(1.0), p=0.2850
(0.0), p=0.1094
(6.0), p=0.0234 **
(0.0), p=0.0078 ***
(1.0), p=0.0156 **
(1.0), p=0.0156 **
(2.0), p=0.0234 **
30min 0.8
(0.0), p=0.1088
(0.0), p=0.0180 **
(3.0), p=0.391 **
(0.0), p=0.0078 ***
(0.0), p=0.0078 ***
(0.0), p=0.0078 ***
(0.0), p=0.0078 ***
30min 0.9
(0.0), p=0.3173
(3.0), p=0.091 *
(1.0), p=0.6547
(1.0), p=0.0156 **
(1.0), p=0.0156 **
(1.0), p=0.0156 **
(1.0), p=0.0156 **
Daily 0.8
(4.0), p=0.7150
(1.0), p=0.1484
(6.0), p=0.3428
(4.0), p=0.7150
(4.0), p=0.7150
(2.0), p=0.0234 **
(6.0), p=0.1763
The values in the parentheses are t-statistics. ***, ** and * denote significance at the 1%, 5% and 10% level
respectively
51
Preprint not peer reviewed

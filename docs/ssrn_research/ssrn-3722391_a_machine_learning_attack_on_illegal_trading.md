# A Machine Learning Attack on Illegal Trading∗

- **Source File**: `ssrn-3722391.pdf`
- **Total Pages**: 50
- **SSRN ID**: `ssrn-3722391`

---

## Page 1

A Machine Learning Attack on Illegal Trading∗
Robert James†
Henry Leung‡
Artem Prokhorov§
April 1 2022
Abstract
We design an adaptive framework for the detection of illegal trading behavior.
Its key
component is an extension of a pattern recognition tool, originating from the field of signal
processing and adapted to modern electronic systems of securities trading. The new method
combines the flexibility of dynamic time warping with contemporary approaches from extreme
value theory to explore large-scale transaction data and accurately identify illegal trading pat-
terns. Importantly, our method does not need access to any confirmed illegal transactions for
training. We use a high-frequency order book dataset provided by an international investment
firm to show that the method achieves remarkable improvements over alternative approaches in
the identification of suspected illegal insider trading cases.
JEL Codes: G14, G18, C55
Key Words: illegal trading, insider trading, market manipulation, market micro-structure, order
book, machine learning
∗Helpfull comments from Martin Burda, Christian Gourieroux, Jessica Leung, the participants of CFE-2021,
INFORMS-2022, EURO, ISF-2022, IAEE-2022 and seminar participants at CEBA, University of Sydney, McGill
University, University of Toronto and University of Miami are gratefully acknowledged.
Research for this paper
was supported by grants from Australian Research Council (James, Project DP200103549) and Russian Science
Foundation (Prokhorov, Project No. 20-18-00365) for various and non-overlapping parts of this research.
†Discipline of Business Analytics, University of Sydney Business School, Australia; email: r.james@sydney.edu.au
‡Discipline of Finance, University of Sydney Business School, Australia; email: henry.leung@sydney.edu.au
§Discipline of Business Analytics, University of Sydney Business School, Australia; Center for Econometrics and
Business Analytics (CEBA), St.Petersburg State University, Russia; Center for Interuniversity Research in Quanti-
tative Economics (CIREQ), University of Montreal, Canada; email: artem.prokhorov@sydney.edu.au
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 2

1
Introduction
Illegal trading practices undermine the integrity of financial markets. There is growing empirical
evidence of illegal trading strategies, which include insider trading (Meulbroek, 1992; Kacperczyk
and Pagnotta, 2019), closing price manipulation (Comerton-Forde and Putni¸nˇs, 2011) and spoofing
(Lee et al., 2013).
Successful market surveillance practices that are designed to detect illegal
trading activity are known to improve the quality of financial markets (Fernandes and Ferreira,
2009; Cumming et al., 2011; Aitken et al., 2015).
However, the precise identification of illegal
trading activity poses a difficult problem because confirmed cases of illegal trading are rare when
compared to the volume of legitimate transactions (Cline and Posylnaya, 2019). Moreover, what
constitutes a pattern of illegal trading activity depends on the context and is generally not well
defined, partly due to the need to avoid regulatory arbitrage (Putni¸nˇs, 2012). From a detection
standpoint, these issues impede the application of classical supervised statistical learning techniques
suited for balanced data and well identified patterns of illegal trading.
Our basic premise is that illegal trading activity differs substantially from patterns of historical
legitimate trading activity at a broker.
Hence, extreme abnormality of broker account trading
activity is the key condition that constitutes a relevant alert in an effective market surveillance
system.
In this study, we combine the Nearest Neighbor Dynamic Time Warping (NN DTW)
pattern recognition algorithm with extreme value theory to formulate an adaptive surveillance
model designed to detect illegal insider trading activity1. The design of our surveillance model is
based upon time series anomaly detection techniques and leverages high-frequency broker-specific
order book information to identify sequences of exceptionally abnormal trading activity by the
broker’s accounts. Importantly, our model does not require access to historical examples of illegal
transactions for training and is also non-parametric in the sense that we make no assumptions on
the data generating process or the structure of insider trading. We demonstrate that our anomaly
detection approach identifies a greater proportion of all insider transactions while achieving a
significantly lower false positive alert rate than alternative approaches from the literature.
We are particularly interested in studying insider trading activity because this behaviour, funda-
mentally underpinned by asymmetric information, is pervasive across financial markets. Moreover,
insider trading has been linked to reduced investment and, as a consequence, to an inefficient al-
location of capital and risk sharing across an economy (see, e.g., Manove, 1989; Ausubel, 1990;
Leland, 1992; DeMarzo et al., 1998). Our proposed methodology is particularly relevant to brokers,
exchanges and regulators because identifying insider trading practices is part of the mandatory
transaction monitoring tasks faced by these institutions. The last decade has seen increasing ex-
1For brevity, we refer to “illegal insider trading” as “insider trading” henceforth unless otherwise specified.
1
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 3

pectations from regulators to develop more comprehensive compliance and regulatory technology
practices. As such, our study contributes to the advancement of regulatory market surveillance
technology.
Traditional detection approaches assume that insider trading moves prices because the insider’s
private information is revealed to the market through the trading process. Based upon this as-
sumption, insider trading can be detected by studying abnormal stock returns before informational
events (see, e.g., Meulbroek, 1992). This idea has previously been used by regulators (Dubow and
Monteiro, 2006; ASIC, 2019). However, we demonstrate that this abnormal return based detection
approach does not adequately identify the presence of insider trading for the cases we investigate. In
practice, individual brokers adhere to regulatory requirements by using rule-based market surveil-
lance systems to monitor the trading activity of client and principle accounts for suspected illegal
trading activities. These industry market surveillance systems struggle to adapt to dynamic market
conditions and diverse patterns of normal trading behavior, thereby resulting in an exceptionally
high rate of false positive alerts.
We focus on engineering features that monitor the trading behaviour of individual market
participants, consistent with theoretical models that emphasize the strategic trading patterns of
illegal insiders (see, e.g., Glosten and Milgrom, 1985; DeMarzo et al., 1998). An anomaly score is
constructed by computing a measure of the distance based similarity to the nearest neighboring
sequence in a historical set of legitimate broker account trading sequences. Fundamentally, our
detection framework is based upon the fact that the signatures associated with insider trading are
known to be markedly different from those associated with legitimate trading activity (Meulbroek,
1992; Shkilko, 2019; Kacperczyk and Pagnotta, 2019).
Trades with similar characteristics in two broker account trading sequences may be executed in
a different order, for instance, due to time-varying liquidity and volatility in the underlying asset
and/or as a result of a conscious attempt to conceal proprietary trading strategies. This means
that traditional measures of statistical distance that rely on a linear alignment between trades in
the feature space, such as the ℓp-norm2, will incorrectly measure similarity. An incorrect measure
of similarity would distort the estimated distribution of anomaly scores associated with legitimate
trading activity, and hence our ability to precisely detect insider trading.
We address this challenge by applying the DTW algorithm, which is a pattern recognition
algorithm known to perform exceptionally well in time series classification and clustering tasks (see,
e.g., Ding et al., 2008; Dau et al., 2018). DTW finds the optimal non-linear alignment between
similar trades that provide the best match for two trading sequences by realistically shrinking and
stretching different regions of the sequences. An elastic distance measure, such as DTW, will be
2The ℓp-norm of an n-vector x is defined as ∥x∥p = (Pn
i=1 |xi|p)1/p
2
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 4

able to recover a more accurate estimate of similarity for time series that are misaligned. To the
best of our knowledge, while the DTW algorithm has been widely used in the fields of computer
science and engineering, its application to high-frequency financial transactions data is novel.
The upper tail distribution of historical anomaly scores is used to set a threshold that defines
the boundary between legitimate and potentially illegal trading activity. We approximate only the
upper tail of the anomaly score distribution using methods from the field of extreme value theory.
This approach is asymptotically valid and permits inference beyond the range of observed data.
Since extreme value theory is naturally used to describe the occurrence of rare events, the theory
is particularly relevant to anomaly detection problems. We implement a sequential goodness-of-fit
testing procedure with automated false discovery rate control within the extreme value modeling
process. Our threshold estimation procedure requires no manual intervention by the surveillance
analyst, as would be traditionally needed in applied extreme value modeling. The threshold is
re-estimated daily so that detection rapidly incorporates changes in the distribution of legitimate
broker account activity.
To evaluate our detection model we use second-by-second transaction data which covers 14
suspicious trading reports pertaining to alleged insider trading cases investigated by a global in-
vestment firm3, whom we have partnered with in this study. The 14 suspected insider trading
cases originated in various prominent Asian equity markets over a four year period. The valida-
tion sample contains a total of 294 trading days of broker transaction activity across the 14 cases.
In aggregate, our experiments analyze approximately 252,000 broker transactions and over 5,000
suspected insider transactions.
To the best of our knowledge, Olmo et al. (2011) and Park and Lee (2010) are the key studies
that propose principled time series methods to detect insider trading.4 Both rely on modeling the
stock return time series using traditional financial econometric methods. Olmo et al. (2011) test for
the presence of structural breaks in the idiosyncratic component of stock returns using an Extended
Capital Asset Pricing Model. This method was designed to detect long-lived insider trading over
several months ahead of corporate announcements or unexpected news releases and therefore does
not closely align with how broker market surveillance is conducted in practice. Park and Lee (2010)
fit an ARMA(1,1) model to the intraday stock return time series and design three insider trading
detection algorithms based upon the estimated model coefficients. We take this ARMA(1,1) model
as the benchmark approach.
Using a time series cross validation testing procedure we demonstrate that our NN DTW model
3The investment firm acts as a broker-dealer across a large number of international equity markets.
4Islam et al. (2018) also offer a detection method but it is unclear from the paper whether the authors undertake
a supervised or unsupervised approach and hence whether their approach is relevant for our setting.
3
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 5

identifies 90% of all suspected insider transactions in the validation sample. In contrast, the best
ARMA(1,1) detection algorithm identifies around 60% of suspected illegal insider transactions.
Moreover, our NN DTW model achieves an average false positive alert rate of 30%, while more
than 71% of all transactions flagged as illegal by the ARMA(1,1) model were false positives. Hence,
our surveillance model minimizes regulatory risk at the broker.
We also show that our model
outperforms an Ensemble Gaussian Mixture Model (EGMM), an isolation Forest (iForest) and
a Once-Class Support Vector Machine (OCSVM). In particular, the EGMM and the iForest are
known to be powerful anomaly detection algorithms (Emmott et al., 2015). Our NN DTW model
has the highest probability of assigning a large anomaly score to a randomly selected sequence of
suspected insider trading activity and hence the highest probability of correct classification. We
further demonstrate that our NN DTW model is able to achieve a dramatically lower false alarm
rate than the other algorithms in a simulation exercise.
First and foremost, we contribute to literature that designs statistical models to detect illegal
trading activity. Prior literature has applied time series econometric models (see, e.g., Olmo et al.,
2011; Park and Lee, 2010) and supervised machine learning models to detect insider trading and
manipulative trading activity more broadly. For instance, Diaz et al. (2011) use decision trees to
identify patterns of stock market manipulations for a sample of eight manipulated stocks in 2003.
The authors detect anomalies via a clustering technique, since the SEC does not disclose the exact
dates of illegal trading activity. Using the same dataset and the same activity detection method,
Golmohammadi et al. (2014) further examined the performance of random forests, Neural Networks,
Naive Bayes, Support Vector Machines and the K-Nearest Neighbours supervised learning models.
Finally, Deng et al. (2019) train gradient boosted decision trees to detect insider trading in the
Chinese stock market.
We emphasize that these supervised approaches are generally not applicable to individual bro-
kers, since the broker often does not have access to a sufficiently representative database of historical
illegal trading activity to train a supervised learning model. For this reason, our approach is based
upon the application of an one-class machine learning algorithm. Moreover, the aforementioned
studies do not explicitly model the time series dimension of the data. A vast literature has shown
that informed traders, of which illegal insiders are a subset, engage in multiple rounds of trading
based on their private information (see, e.g., Glosten and Milgrom, 1985; He and Wang, 1995).
Therefore, our detection model is explicitly designed to be applied to time series sequences of
trading activity. Because our model achieves remarkable improvements over previously proposed
approaches it could be used as a benchmark for future studies. We also provide new insights into
insider trading by using a proprietary dataset and demonstrate the capabilities of different machine
learning based anomaly detection models.
4
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 6

Aside from the machine learning dimension, our study contributes to the literature examining
the behavior of illegal insider traders and factors affecting its prevalence and severity (see, e.g.,
Aitken et al., 2015; Cline and Posylnaya, 2019). In particular, Meulbroek (1992) and Kacperczyk
and Pagnotta (2019) find that the presence of illegal insiders are related to heightened liquidity
and volatility in the U.S. equity market. We draw upon this literature to design our surveillance
model. Additionally, we provide new insights into how these findings apply across the largest Asian
equity markets.
Our study is also related to the broader literature on data driven financial fraud detection. While
the detection of credit card fraud (Bolton and Hand, 2002), financial statement fraud (Spathis et al.,
2002) and insurance fraud (Derrig, 2002) have received significant attention within the literature,
there are comparatively few studies that design detection systems for fraudulent and illegal activity
in securities markets (Ngai et al., 2011). Our work addresses this gap in the literature. Moreover, we
differ from much of the traditional financial fraud literature that uses supervised learning methods
by framing the detection of insider trading as a one-class machine learning problem.
Finally, our anomaly detection approach is related to literature studying illegal trading activity
in cryptocurrency markets. Consistent with our approach, Cong et al. (2021) and Amiram et al.
(2020) demonstrate the utility of anomaly detection methods to identify instances of illegal trading.
This work applies Benford’s Law5 and the E-Divisive with Medians technique to identify change
points. However, our anomaly detection approach is different, since we are designing a method to
identify multivariate sequences of anomalous transactions that is based upon a measure of statistical
distance, namely DTW. Nonetheless, we are optimistic that our approach could also be used to
detect sequences of illegal trading activity in other asset classes which are traded on exchanges that
use the limit order book mechanism.
The remainder of the paper is structured as follows. Section 2 describes the operations of an
equity market surveillance division in a brokerage firm, the architecture of existing rule-based expert
market surveillance systems and the limitations of these systems. Section 3 describes our data and
features. Section 4 presents our anomaly detection method and the NN DTW algorithm. Section
5 details the component of our model which is based on extreme value theory. The performance of
our detection model is evaluated in Section 6. Section 7 concludes.
5Benford’s Law is an observation that in many naturally occurring sets of numerical data, the expected frequency
of the first significant digit is likely to be small. Deviations from Benford’s Law can be used to identify anomalous
patterns in large datasets. For example, Benford’s Law can be applied to identify the presence of an anomalous trade
volume of a transaction which may be indicative of illegal wash trading.
5
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 7

2
Broker Market Surveillance
Market surveillance divisions use automated surveillance systems to generate alerts for instances
of suspected illegal activity. These alerts are escalated to surveillance analysts who review the
flagged activity to either close the alert as a false positive or conduct a detailed investigation. An
important step in the alert review process requires the surveillance analyst to assess whether or not
the flagged broker account traded in an unusual or anomalous manner given their recent trading
history in the stock and/or the recent trading history of other broker accounts. It is important
that the Type 1 error (false positive) rate of a surveillance system is kept as low as reasonably
possible to ensure human analysts are not overwhelmed by false alerts. Moreover, since brokers
may be subject to significant financial penalties if surveillance systems fail to adequately detect
illegal trading activity, a market surveillance system must also be able to identify a large fraction
of all illegal trading activity to ensure compliance with regulatory standards.
Currently, the majority of broker compliance divisions rely on rule-based expert surveillance
systems to detect illegal trading activity6. These expert systems embed knowledge of illegal trading
activity via a pre-set dictionary of human defined rules and parameters which specify the structure
of known illegal trading scenarios. Each parameter in a scenario is associated with an individual
threshold. These thresholds are largely time-invariant and are typically applied globally across a
population of stocks and broker accounts being monitored. Alerts are generated using conditional
logic which compares the values of the scenario parameters with their corresponding thresholds to
determine if an alert should be triggered. Rule-based expert surveillance systems implicitly assume
that the structure of illegal trading activity is known ex-ante and can be well defined by a series of
conditional logic statements. See Golmohammadi et al. (2014) for a complementary description of
the rule based experts systems that are used in practice.
The complex nature of modern financial markets means that an accurate rule-based represen-
tation of all possible modes of illegal trading activity is infeasible. This problem is compounded by
the relative rarity of prosecuted trading behavior, meaning that domain experts have only a small
number of cases on-hand to design and calibrate alert scenarios and thresholds. As such, rule-based
systems suffer from an incomplete monitoring problem, whereby instances of illegal trading activity
which do not strictly match the conditional logic in alert scenarios are unlikely to be detected.
The time-invariant global thresholds used in current rule-based expert surveillance systems lead
to a high Type 1 error rate, since they cannot rapidly adapt to changing market conditions. This,
in turn, can lead to complacency in the manual alert review process, a problem which is sometimes
referred to as the base rate fallacy (see, e.g., Axelsson, 2000). Moreover, the alerts generated by
6The NASDAQ SMARTS and ONETICK systems are examples of rule-based expert market surveillance systems.
6
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 8

the existing systems provide little information about the abnormality of trading patterns7, despite
this being a critical component of the alert review process. The market surveillance model that we
design in this study seeks to overcome these limitations.
3
Broker Transaction Data and Financial Feature Engineering
Order-driven exchanges operating electronic limit order books use a continuous double auction
mechanism to match buy/sell orders stored in bid/ask queues. Four events occur in order-driven
markets, namely order submissions, order cancellations, order amendments and trade executions.
Given our goal of insider trading detection, we are concerned primarily with trade executions and
best bid/ask submissions.
Typically a broker’s equity market surveillance department analyzes a semi-identified limit
order book, that is a limit order book in which all executed trades and best bid/ask quotes are
observed but only a subset of these trades and quotes is associated with the named client/principle
trading accounts of the broker. The trading accounts of other brokers are anonymous and cannot
be distinguished from one another. Each transaction in the data is associated with (i) a price, (ii)
a volume, (iii) a time rounded to the nearest second8, (iv) an account identifier which is either the
broker’s client account code if that broker’s account was on one side of the trade or blank otherwise,
(v) the prevailing best bid and ask prices and (vi) qualitative trade flags (for example, whether or
not the trade was a short-sell or buyer/seller initiated). On each day transactions are sequenced in
ascending order according to their timestamp, rounded to the nearest second.
In general, the calendar time duration between consecutive trades is not the same as trades are
irregularly spaced in time. In this study we consider sequences indexed by the order of transaction
arrival rather than calendar time.
Hence, time is incremented each time a new trade arrives
and refers to the relative position of a transaction within the sequence. This approach is known
as transaction time sampling in the literature (Hautsch and Podolskij, 2013; Hasbrouck, 1991).
Instead, we capture the calendar time properties of trading activity through our feature engineering
process.
Given the one-class nature of the insider trading detection problem, standard feature selection
techniques, such as penalized regression models like Lasso, cannot be used to identify the optimal
feature set for detection. Instead, we define a set of relevant microstructure variables by surveying
the literature on market dynamics with asymmetric information and heterogeneous agents. We also
7we note that the identification of anomalous trading patterns by market surveillance systems serves a secondary
function, which is to ensure that the occurrence of manual trading errors, the so called ‘fat finger’ errors, is minimized
8This was the minimum time increment available in our empirical tests so we use it to describe our data environ-
ment. Higher frequency data does not change our proposed detection model.
7
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 9

leverage the practical surveillance experience of an investment firm that provided the data used in
our empirical experiments. Broadly speaking, the theory of markets with asymmetric information
postulates that the trading activity of privately informed market participants alters the observable
value of relevant market variables (Kacperczyk and Pagnotta, 2019). Hence, insider trading can be
detected by identifying abnormal changes in a set of relevant market variables.
The first class of variables we consider are measures of trade volume and transaction frequency.
Theoretically, trade volume is correlated with the degree of private information held by informed
market participants (Easley and O’hara, 1987; He and Wang, 1995; Glosten and Milgrom, 1985).
As features we compute the raw trade volume associated with each transaction, a measure of
broker account trade volume which does not reflect liquidity changes that may be associated with
exogenous market events, the volume which originates from short sell orders, the sum of trade
volume for each broker account over 30-minute trade-by-trade moving windows, and a measure of
the intraday broker account participation rate over the same windows.
Our second set of features measure liquidity provision and demand at the time of broker ac-
count transactions, since theoretical models of liquidity closely consider the behaviour of informed
traders (see, e.g., Glosten and Milgrom, 1985; Kaniel and Liu, 2006; Lim and Coggins, 2005). We
compute the immediate price impact and the permanent price impact of a transaction (also known
as the adverse selection spread component), and a measure of trade duration which is adjusted
for intraday periodicity to capture the liquidity dimension of broker account trading activity. Fi-
nally, we compute a measure of intraday realized volatility over 30-minute trade-by-trade moving
windows using grids of 1,800 transaction prices. Our volatility feature is the equal-weighted aver-
age of 40 microstructure noise robust realized volatility estimators (Patton and Sheppard, 2009).
We provide mathematical definitions and further motivation for each of our features in the online
supplementary materials file.
Feature engineering is performed on the entire semi-identified order book data. Then, for each
stock, we extract all intraday trading sequences associated with the identifiable broker accounts
from the entire dataset. For each broker account on each day, we construct trade-by-trade sliding
windows of m consecutive trades in a given stock.
These windows form our intraday trading
sequences. Any trading sequence shorter than m trades is up-sampled via linear interpolation to
length m. The set of all trading sequences for a given stock, account and day comprises what we
call a broker account trading activity.
Formally, each trade is characterized by a p-dimensional feature vector vj. Then, an intraday
broker account sequence is associated with an m × p data matrix, which we denote by Vid =
{vj, j = 1 . . . , m}, where i indexes the broker account trading sequences. The information related
to all broker account trading activity can be represented by the set {Vid, i = 1, . . . , Nd}D
d=1, where
8
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 10

Nd is the number of intraday trading sequences on day d, and D is the number of days in the
sample.
4
Methodology
Two aspects of the equity market microstructure guide how we implement the time series anomaly
detection method for insider trading detection. First, order-driven equity markets operate separate
limit order books for individual securities. The idiosyncratic characteristics of individual stocks
imply that each order book will comprise a different set of normal trading activity.
We argue
that a stock specific modelling approach reduces Type 1 errors and delivers improved classification
performance.
The rationale is that the thresholds which define the boundary between normal
and anomalous trading activity can be learned more accurately when using only stock specific
information.
Moreover, this approach aligns well with the structure of existing expert market
surveillance systems, enhancing synergies between our bottom-up approach and the existing top
down approach used in practice.
Second, insider trading takes place on only one side of the market, as the insider seeks to profit
from an anticipated price movement. Therefore, we construct separate anomaly detection models
for the bid and ask sides of the order book. This approach may also be beneficial in cases where
the insider attempts to disguise their illegal trades by placing seemingly legitimate trades on the
opposite side of the order book (see, e.g., Back and Baruch, 2004). In what follows, unless otherwise
stated, we omit the subscripts representing individual stocks, brokers and the sides of the order
book.
4.1
Anomaly Detection Framework
Let {Vid, i = 1, . . . , Nd}D
d=1 denote the available information set. We split the information set into
two subsets: the training dataset of legitimate trading activity X = {Vid : i = 1, . . . , Nd, d ∈I1},
where I1 ⊂{1, . . . , D}, and the testing dataset Y = {Vid : i = 1, . . . , Nd, d ∈I2}, where I2 = Ic
1
and min(I2) > max(I1). All activity in the training dataset with days indexed by I1 is designated
as legitimate trading activity because we have no cases of verifiable manipulation for those days.
Our detection framework is based on a comparison of Y to X. We define the anomaly scoring
function as f(X, Y, θ), where θ is a set of hyper-parameters. This function generates anomaly
scores for all intraday sequences in Y based on information about trading activity in X using the
NN DTW algorithm. The main idea is to use X to learn what trading behavior is considered
normal and then detect sequences in Y with trading patterns which do not reasonably conform to
the patterns in X. We achieve this in the following two step procedure.
9
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 11

First, the anomaly scoring function is applied to sequences of legitimate trading activity to
generate a set of training sample anomaly scores ϑ(X) = f(X, X, θ) = {ϑid, i = 1, . . . , Nd : d ∈I1}.
Let F denote the distribution of ϑ(X), which is a continuous distribution. We use a sample of
upper order statistics from ϑ(X) to estimate the parameters of a generalized Pareto extreme value
distribution which serves as an asymptotically valid approximation of the upper tail of F. An
anomaly score threshold is set as the conditional tail expectation τ (α) at confidence level α, using
this approximation.
Second, we apply the anomaly scoring function to the testing data. This generates a set of testing
sample anomaly scores ϑ(Y ) = f(X, Y, θ) = {ϑid, i = 1, . . . , Nd : d ∈I2} for each trading sequence
in Y. Using the anomaly score threshold τ (α), the class label vector is then ˆy = −sign(ϑ(Y ) −τ (α)).
A sequence is flagged as anomalous and thus representative of potential insider trading activity, if
the anomaly score exceeds the threshold (i.e. if ˆyid = −1).
4.2
Basics of Dynamic Time Warping
The ℓp-norm is a common measure of statistical distance. When applied to time series data the
ℓp-norm enforces a linear alignment between observations in two sequences. However, time-varying
market conditions, such as liquidity or volatility, and/or because of conscious attempts by traders
to conceal trading patterns by randomly shuffling the order of a small number of transactions may
cause regions of similar transactions for two sequences of trading activity to become misaligned.
To address this issue, we measure the statistical distance between sequences using DTW.
DTW is an elastic distance measure that finds the optimal alignment between two sequences by
constructing a non-linear mapping between observations (Sakoe and Chiba, 1978). The basic idea
is to warp, that is to stretch and shrink, various parts of a query sequence to find the best match
to a reference sequence. In doing so, one can define a distance measure that is invariant to any
misalignment in time between similar regions of the two sequences. The exceptional performance
of DTW for time series similarity search tasks is well established in the literature (Ding et al., 2008;
Bagnall et al., 2017; Dau et al., 2018).
The idea of non-linearly warping a sequence is easily seen in Figure 1, by comparing the align-
ment produced using DTW with the alignment produced using a standard ℓp-norm, such as the
Euclidean norm. As an illustration, the first panel of Figure 1 plots two starlight curves for the
same class of star which are misaligned in time9. Clearly, a Euclidean alignment does not account
for the misalignment between the two starlight curves. However, using DTW we observe that the
blue curve is warped so that similar regions of the two curves are aligned along the time axis.
9The starlight curve data is available at https://www.cs.ucr.edu/%7Eeamonn/time_series_data_2018/
10
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 12

The fourth panel of Figure 1 shows the two series after they have been synchronized using DTW.
The two starlight curves are then shown to belong to the same star. Figure 1 demonstrates that
measures which enforce lock-step one-to-one mappings, or even fixed linear mappings, between
observations can considerably overstate the distance between sequences which are unpredictably
misaligned in time.
Figure 1: Comparison of Euclidean and DTW alignment between two starlight curves for an identical star.
4.3
Multivariate DTW
When time series are multivariate (vector valued) DTW can be generalized in one of two ways
(see, e.g., Shokoohi-Yekta et al., 2017). First, one may construct feature-specific alignments by
applying DTW to the time series for each feature in the multivariate sequences. The distances
corresponding to each feature-specific alignment are then summed to compute the overall distance
between the multivariate sequences. This approach is known as independent DTW since it assumes
that the features carry no joint information so that characteristics of one feature do not affect the
warping path of another. The alternative is to warp all dimensions simultaneously based upon a
11
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 13

single optimal alignment path. This is known as dependent DTW. For problems where the feature
time series are “tightly coupled”, that is they change simultaneously as new observations arrive,
dependent DTW is preferred. In our setting, a new trade mechanistically affects the values of
all features simultaneously, giving rise to a high degree of dependence. We, therefore, implement
the dependent version of multivariate DTW. All references to DTW herein refer to the dependent
variant.
Broadly described, the DTW distance between two time series sequences is calculated in three
steps. First, a so-called cost matrix that contains the Euclidean distances between all possible
combinations of observations in the two time series is computed. Second, the optimal warping
path that defines the alignment between observations is found using dynamic programming. This
optimal warping path is found subject to constraints that ensure a realistic mapping between the
two time series. Finally, the DTW distance is calculated as the square-root of the sum of distances
along the optimal alignment path. Appendix A describes the DTW algorithm in more detail.
To visualize the mechanics of DTW, Figure 2 plots the cost matrix and cumulative cost matrix
together with the optimal warping path (solid white line) obtained under DTW for the two starlight
curves introduced in Figure 1. An example of the Warping Window Width constraint (See (10) in
Appendix A), is plotted as the dashed lines around the diagonal of the cumulative cost matrix in
panel (b). Intuitively, one can observe that the optimal warping path is the path of least resistance
through a hilly surface where the values of C(i, j) measure the hill heights.
4.4
The Nearest Neighbor Dynamic Time Warping Algorithm
The DTW distance is used as the statistical distance measure in a standard one-NN algorithm. We
believe the one-NN algorithm is an attractive solution to the broker market surveillance problem
for three reasons. First, a one-NN algorithm has no need for hyperparameter tuning, which can be
exceptionally difficult in one-class learning problems. Second, a NN algorithm is non-parametric.
Since no explicit definition of what constitutes insider trading activity is used to construct the
anomaly score, it is possible that multiple patterns of insider trading behavior can be identified
using this anomaly detection approach. This sets our detection model apart from other insider
trading detection approaches in the literature and addresses the limitations of the existing market
surveillance systems that rely upon conditional alert logic.
Third, the instance-based learning
property of NN algorithms can handle concept drift by allowing the training dataset and threshold
to be updated at a high frequency with negligible model retraining costs. This property ensures
regulatory compliance as the most recent trading information can be rapidly incorporated into the
surveillance model.
In its basic form, the complexity of the NN DTW algorithm is considerable, generally inhibiting
12
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 14

(a) DTW Cost matrix
(b) DTW Cumulative Cost matrix
Figure 2: DTW cost matrices, optimal warping path and warping window width constraint for the alignment
of the two starlight curves from Figure 1. The Euclidean distance is 8.645. The DTW distance is 3.665.
its application to large scale time series classification problems, such as financial market surveil-
lance10. However, several studies have proposed alternative procedures to reduce the complexity
of the NN DTW algorithm. Broadly speaking, these procedures use the constraints imposed upon
the optimal warping path to prune nearest neighbor candidates. We use three lower bounding
functions and two early abandoning techniques to prune nearest neighbor candidates. We describe
each technique in Appendix B and give the pseudo code for the NN DTW algorithm. In our ex-
periments these techniques reduce the number of required full DTW calculations by approximately
85%, resulting in a considerable reduction in computational complexity. Finally, we use the efficient
cost matrix construction procedure of Silva et al. (2018) to reduce the search space of the optimal
warping path by pruning regions of the DTW cost matrix.
5
Threshold Selection
We address the setting of a precise anomaly score threshold for one-class learning problems, using
only information about the negative class. This threshold defines the largest anomaly score for
10Since DTW distance does not satisfy the Triangle Inequality, well known indexing techniques for metric spaces
cannot be used to reduce complexity.
13
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 15

which a broker account sequence can be classified as normal. Typical non-parametric approaches to
select an anomaly score threshold involve using quantiles of the empirical anomaly score distribution
function, which is equivalent to selecting the anomaly score value that identifies the n largest
scores as outliers.
However, the estimation of high quantiles in finite samples can be subject
to large variance. Moreover, only previously observed values of anomaly scores can be used as
thresholds and estimation beyond the largest observed value is not possible when using the empirical
distribution function. Parametric approaches typically involve assuming the entire range of anomaly
scores follows a specific distribution, such as Gaussian (Ahmad et al., 2017). Strong parametric
assumptions are subject to model misspecification risk, particularly so if the underlying anomaly
scores are heavy tailed and this regularity is not reflected in the choice of distribution.
Instead, we rely on extreme value theory to construct an accurate representation of the upper
tail of the distribution of training sample anomaly scores.
Extreme value theory describes the
asymptotic behavior of a stochastic process at unusually large or small values. The theory can
be used to construct a model for the tails of an underlying distribution, without the need to
make potentially inappropriate parametric assumptions over the entire support of the underlying
distribution. We rely on the “Peaks-Over-Threshold” (POT) method11 which models the behavior
of observations above a high initial threshold value, denoted by u.
We are given a set of training sample anomaly scores ϑ(X) computed by the NN DTW algorithm
which are assumed to be i.i.d. The common but unknown distribution function of these scores is
denoted by F. We can define an anomaly score threshold as the value in the support of F such
that at most 1 −α probability mass is above this value, for some sufficiently large α, since we are
interested in identifying anomalous broker account sequences. Quantiles are natural here. To apply
the POT method we fit the generalized Pareto distribution to the exceedances of the anomaly scores
above the initial threshold value. We provide additional details regarding the foundations of POT
extreme value theory in Appendix C. Let ˆξ and ˆσ denote the estimated shape and scale parameters
of the generalized Pareto distribution respectively. The POT method derives the following estimator
of the tail α-quantile
ˆQ(α) = u + ˆσ
ˆξ
" N
Nu
(1 −α)
−ˆξ
−1
#
,
α > F(u)
(1)
where N denotes the number of anomaly scores in the training data and Nu is the number of
11An alternative is to use the “Block-Maxima” method, which segments observations that are measured over regular
intervals into non-overlapping blocks and uses the largest order statistic in each block to develop a model for the
tail distribution. However, there is no obvious choice of block size in our application. Moreover, the block-maxima
method uses available data inefficiently by sampling only the largest order statistic in each block.
14
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 16

anomaly scores that exceed u.
The quantity ˆQ(α) is akin to the so-called Value-at-Risk when the underlying data are negative
log returns of financial assets. However the use of ˆQ(α) as an anomaly score threshold leaves room
for improvement, since information beyond the quantile ˆQα is disregarded. One implication, that
sequences with anomaly scores which are marginally greater than ˆQ(α) will be flagged as anomalous
even though they are typically not much different from anomaly scores just below ˆQ(α).
A more robust anomaly score threshold would consider the average behavior of the training
sample anomaly scores exceeding ˆQ(α), that is the behavior of E[ϑid −ˆQ(α)|ϑid > ˆQ(α)]. In the
financial risk management literature this measure is typically referred to as the Expected Shortfall,
while more broadly it is known as the Conditional Tail Expectation (CTE) or Superquantile.
Subject to the assumption that ξ < 1, which ensures that the mean of the generalized Pareto
distribution is finite12, the CTE anomaly score threshold is
ˆτα =
ˆQ(α) + ˆσ + ˆξ( ˆQ(α) −u)
1 −ˆξ
,
α > F(u),
ˆξ < 1
(2)
The CTE anomaly score threshold can be understood as the average anomaly score of the
most unusual patterns of normal training activity. The level of confidence α defines where unusual
training sample anomaly scores begin in terms of the quantiles of F.
Hence, sequences in the
testing sample are flagged as anomalous only if they are exceptionally different from historical
normal trading activity. Unusual, but still legitimate trading activity, such as fund fire sales or
large scale portfolio re-balancing, could be associated with large training sample anomaly scores.
In these cases, F will likely have heavy tails if unusual but still legitimate trading events occurred
during the training sample. The extreme value based anomaly score threshold accounts for this
circumstance by accurately modeling the behavior of the tails of F when such tails are heavy.
Since the construction of the anomaly score threshold is reminiscent of financial risk management
practices we believe the choice of α is intuitive and would typically lie between 0.95 and 0.99. This
means that the anomaly score threshold is set based upon the average behavior of the largest 5%
(or less) of training sample anomaly scores.
The POT extreme value modeling approach described above relies on the assumption that
observations are stationary and i.i.d.
We use a sliding window of size m to define all possible
combinations of intraday trading sequences for each broker account. As such, anomaly scores for
accounts that execute a large share of daily trades may not be independent of one another. To
eliminate this source of potential dependency we reduce the set of training sample anomaly scores
12In most practical applications it is unlikely that ξ exceeds one. In cases where ξ > 1 the quantile based anomaly
score threshold ˆQ(α) can be used instead.
15
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 17

used to estimate the parameters of the generalized Pareto distribution by retaining only scores for
non-overlapping broker account sequences on any given day13. This reduced set of training sample
anomaly scores is denoted by ˜ϑ(X).
The use of a generalized Pareto distribution requires the selection of a value for the initial
threshold u, which yields a trade-off between bias and variance. To select the optimal u we take
advantage of the automated sequential testing procedure of Bader et al. (2018). Specifically, we
consider an ordered finite set of candidate thresholds ˜u1 < · · · < ˜uj < · · · < ˜un between the 70th and
94th quantile of the training sample anomaly scores in increments of one. Each candidate threshold
is associated with a sample of exceedances ˜Zj = {˜ϑid −˜uj|˜ϑid > ˜uj, i = 1 . . . Nd : d ∈I1}, j =
1, . . . , n. The jth null hypothesis, H(0)
j
, states that ˜Zj follows a generalized Pareto distribution. The
Anderson-Darling goodness-of-fit test is applied to each set of exceedances with the corresponding
threshold, starting with (˜u1, ˜Z1) and proceeding until a pair (˜uj, ˜Zj) results in an acceptance of the
null hypothesis. We utilize the interpolated table of p-values provided by Bader et al. (2018).
The rejection of any null hypothesis H(0)
j
implies that all prior null hypotheses for lower can-
didate thresholds have also been rejected. Since multiple hypotheses are effectively being tested
there is a need to control the false discovery rate. Bader et al. (2018) propose to apply the recently
developed ForwardStop rule of G’Sell et al. (2016), which was shown to control the false discovery
rate at a level β in settings which require ordered hypothesis testing. After computing the p-values
pj, from the Anderson-Darling test for all candidate thresholds the index of the optimal threshold
is
ˆk = max{k ∈{1, . . . , n} : −1
k
k
X
j=1
log(1 −pj) ≤β}
(3)
and the optimal threshold is u = ˜uˆk. We set β = 0.1.
Therefore, our anomaly score threshold estimation procedure can be applied without needing
to manually adjust parameters, as is traditionally the case when applying extreme value theory to
data. Moreover, the anomaly score threshold can be made time-varying by simply re-estimating u,
ξ and σ whenever the set of training sample anomaly scores is updated. Users are required to pre-
select only one parameter, namely the quantile level α, to estimate the anomaly score threshold.
6
Experiments & Evaluation
The described model is evaluated using data relating to 14 suspicious trading reports filed for
alleged insider trading by an investment firm who acts as a dealer-broker in a large number of
13The Ljung-Box tests of the null hypothesis that the reduced anomaly score sample is independently distributed
found no evidence against the null.
16
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 18

equity markets. The 14 suspected insider trading cases originated in various prominent Asian equity
markets. Each case involves suspected insider trading activity ahead of an unscheduled material
information release. These information releases are diverse and encompass financial announcements
as well as news reports of corporate scandals. In each case, a material price movement alert was
triggered on the information release date and a skilled human analyst identified the pattern of
insider trading by manually analyzing historical transaction data.
Semi-identified limit order book data for each case in the sample identifies all trades by the
suspected insider account in conjunction with all trades by the client accounts.
As such, our
experiments assess the ability of an insider trading detection model to distinguish transactions by
the suspected insider account from all other broker account transactions in the days preceding the
information release. We use a validation sample containing all broker account transactions over
a 21 trading day period (approximately one trading month) before the information release date
which triggered the search for insider trading in each case. Hence, we analyze a total validation
sample of 294 days of broker trading activity in our experiments. The training dataset is a rolling
six-month historical sample of broker account transaction activity for each case. To ensure that the
training dataset contains only normal legitimate transaction activity we remove any transactions
associated with historical alerts produced by the existing rule-based expert market surveillance
system, regardless of whether or not the alert was a false positive.
6.1
Summary Statistics
Table 1 provides an insight into the volume of trading activity for each suspected illegal insider
account in our sample. The typical alleged illegal insider begins trading approximately four days
before the information release date and executes a total of 421 trades based upon their private
information. This corresponds to an average of 188 trades per day the suspicious account was
active in the market. In aggregate, we study 5902 transactions associated with suspected insider
trading from the suspicious trading reports. To the best of our knowledge, this is the largest sample
of illegal insider trades studied to date within the literature14. The dollar value of trade volume per
case varies between US$0.5 million and US$90 million, with the typical suspected insider trading
US$10.66 million ahead of the information release date. The trading activity statistics presented
in Table 1 highlight the diversity of suspicious trading behavior.
Table 2 reports the cumulative abnormal returns over a 10-day pre-release period. This period
covers all suspicious transaction activity in our sample. The information release date abnormal
return is also reported. Our treatment of the pre-information release period cumulative abnormal
14For comparison, Kacperczyk and Pagnotta (2019) study 5,058 transactions associated with insider trading, of
which 3392 are executed in U.S equity markets.
17
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 19

return follows the methodology used by regulators to measure the so-called ”market cleanliness”
(Dubow and Monteiro, 2006; ASIC, 2019). We use the market index relevant to each alleged insider
trading case to compute daily abnormal stock returns. Table 2 therefore provides an insight into
the effectiveness of traditional low frequency information leakage based insider trading detection
methods that are used by regulators.
The information release day abnormal return AR(0) exceeds 5% in absolute value in all but
one case.
The mean abnormal return on the information release day is approximately 11% in
absolute value.
Hence, the cases we study involve suspicious trading ahead of material single
day price movements. In only two cases are the pre-release period cumulative abnormal returns
CAR(−10, −1) statistically significant and consistent with the direction of the inside information.
Moreover, in approximately one-third of cases, cumulative abnormal returns in the pre-information
release period are in the opposite direction to the information release day abnormal return. Hence,
traditional insider trading detection approaches based upon the analysis of cumulative abnormal
returns would have been ineffective in identifying the presence of suspected insider trading for 12
of the 14 cases.
Finally, Table 3 presents summary statistics for each feature used in the NN DTW detection
model. Statistics are computed separately for all transactions in the first six-month training dataset
and total 21-day validation sample. T-statistics are reported for differences in the mean of each
feature between the training and validation samples. Both raw trade volume and short sell volume
are higher in the validation sample compared to the training sample and the difference is statistically
significant at the 1% level. Moreover, both mean and median broker account participation rates
are higher in the validation sample. Since the suspicious cases in our sample all involve trading
ahead of unanticipated material information, these elevated trade volume and participation rates
are consistent with the presence of informed trading rather than uninformed speculation.
While the immediate price impact of transactions does not differ between the two samples,
the adverse selection spread component (permanent price impact) is significantly higher in the
validation sample. This suggests that some broker accounts can predict short term price movements
ahead of unanticipated information releases. Importantly, this contrasts with the mean value of
the adverse selection spread component in the six-month training sample, which demonstrates that
the typical broker account is generally uninformed during normal times.
6.2
NN DTW Parameter Settings
Our NN DTW model requires the selection of two parameters. First, the warping window width
parameter used in constraint (10) is set to φ = 0.2. This means that we allow DTW to search
for an optimal alignment within a region of 20 trades. In standard classification problems this
18
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 20

parameter can be learned via cross-validation (Dau et al., 2018). However, this is not possible in
one-class learning problems. We choose the value of φ = 0.2, based upon the results of Kurbalija
et al. (2014) who find that the nearest neighbor assignments using the DTW distance remain
approximately stable above 0.15 for univariate time series. We acknowledge that our choice of
φ = 0.2 is unlikely to be optimal for all cases but generally works well in our experiments. One
may therefore further improve the performance of NN DTW by judiciously setting the warping
window width parameter. The second parameter to be set is the confidence level α, which is used
to determine the anomaly score threshold. We choose a value of α = 0.95, which is likely to be the
lowest threshold a broker would consider using.
6.3
Validation Framework and Performance Criteria
We use the ARMA(1,1) model (Park and Lee, 2010) as our first benchmark because this method is
designed for time series data and does not require access to historically prosecuted cases of insider
trading when estimating model parameters. We implement each of the three detection algorithms
proposed by (Park and Lee, 2010).
As outlined in Section 2, brokers are required to monitor
the trading activity of all client/principle accounts on each day before progressing to the next.
Therefore, to emulate the structure of a real-world market surveillance system, we design a time
series cross validation procedure to evaluate the detection performance of the NN DTW model and
the ARMA(1,1) model of Park and Lee (2010). We provide details regarding the implementation
of the ARMA(1,1) model in the online supplementary materials file15. This validation procedure is
applied uniformly to each of the 14 suspicious trading cases. Figure 3 describes the time series cross
validation procedure. Further details regarding the exact implementation of the cross validation
procedure are given in Appendix D
Classification performance is evaluated using the concatenated validation sample which contains
anomaly scores and class labels for all broker account sequences in each of the one-day testing
periods from the time series cross-validation. The information retrieval performance of the NN
DTW model and the ARMA(1,1) model of Park and Lee (2010) is summarised using the precision,
recall and F1 scores.
High precision scores ensure that the surveillance costs of a broker are
minimized by reducing the volume of false positive alerts which must be investigated by surveillance
analysts.
High recall scores are of particular interest in market surveillance applications since
financial penalties are imposed upon brokers who fail to detect illegal trading activity by their
clients. A high F1 score indicates that both precision and recall scores are high. If a high recall
score is achieved at the expense of a low precision score, and vice versa, then the utility of any
15The supplementary materials file is available at https://papers.ssrn.com/sol3/papers.cfm?abstract_id=
3727753.
19
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 21

Detection Sample Days
d1
d2
d3
d4
. . .
. . .
dalert
Iteration
1
2
3
......
21
6-Month Training Data
Testing Data
Final Validation Sample
Figure 3: Time Series Cross Validation Procedure
insider trading detection model will be diminished and this will be reflected by a low F1 score.
We compute individual precision, recall and F1 scores for each of the 14 cases in addition to the
average precision, recall and F1 score across all 14 cases.
To examine threshold-independent classification performance we study the Area Under the Re-
ceiver Operating Characteristic (AUROC) curve and the Area Under the Precision Recall (AUPR)
curve scores. Together, these two metrics describe how well a particular algorithm separates nor-
mal and insider trading activity, irrespective of the threshold.
For each case of alleged insider
trading 100 equi-spaced hypothetical thresholds in the interval [min({ϑid|ˆyid = −1, i = 1, . . . , Nd :
d ∈I2}), ϑ(Y )+] are used to construct the ROC and PR curves. Vertically averaged ROC and PR
curves are also computed. The area under each curve is computed using the trapezoidal rule.
To establish the statistical significance of differences in each of the aforementioned performance
metrics we follow standard practice for the comparison of classifiers over multiple datasets (Demˇsar,
2006). Friedman tests are used to establish if each of the aforementioned performance metrics differs
significantly between the NN DTW model and the three detection algorithms from the ARMA(1,1)
model. Wilcoxon signed-rank tests are then used to assess the statistical significance of pairwise
differences in the averages of each performance metric over all 14 cases.
20
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 22

6.4
Classification Performance Results
Table 4 reports the AUROC curve and AUPR curve statistics for our NN DTW procedure and
the three ARMA(1,1) model detection algorithms. Figure 4 plots the vertically averaged Receiver
Operating Characteristic (ROC) and Precision Recall (PR) curves to complement the numerical
results in Table 4. The Friedman test statistics (p-values) are 27.0 (0.0) and 9.86 (0.02) for the
averaged AUROC curve and AUPR curve metrics, respectively. Hence, the null hypothesis of equal
classifier performance is strongly rejected.
First, our NN DTW model outperforms each of the ARMA(1,1) model detection algorithms for
the AUROC curve score across all 14 cases. On average, our model achieves an AUROC curve score
of 0.972, corresponding to an improvement of 0.329 on the highest performing detection algorithm
from the ARMA(1,1) model. The difference in the average AUROC curve scores between our NN
DTW model and each ARMA(1,1) detection algorithms is statistically significant at all conventional
levels. Hence, our model has a higher probability of assigning larger anomaly scores to suspected
insider transactions and therefore higher probability of correct classification.
Second, our NN DTW model also outperforms all three ARMA(1,1) detection algorithms for
the AUPR curve statistic. The largest margin of difference in the average AUPR curve statistic
is 0.191. The difference between the average AUPR curve scores for our model and each of the
three ARMA(1,1) model detection algorithms is statistically significant at the 5% level. Figure
4 demonstrates that the true positive alert rate and the precision score of our NN DTW model
are remarkably stable across all possible threshold choices. In summary, we demonstrate that the
threshold independent classification performance of our model is superior to that of the ARMA(1,1)
model.
Table 5 reports the precision, recall and F1 statistics for our NN DTW insider trading detection
model and each of the three ARMA(1,1) model detection algorithms. The Friedman test statistics
(p-values) for the precision, recall and F1 scores are 24.9 (0.00), 30.0 (0.00) and 34.27 (0.0) respec-
tively. Hence, the null hypothesis of equal classifier performance is rejected for all three information
retrieval statistics at all conventional levels of statistical significance. In all but three of the alleged
insider trading cases (case 7, case 8 and case 14), our NN DTW model, outperforms all three of the
ARMA(1,1) detection algorithms across all information retrieval statistics. Moreover, with respect
to the F1 score, which measures the balanced precision and recall performance of a classifier, our
model outperforms the ARMA(1,1) detection algorithms in all but one case (case 14).
We find that our NN DTW model identifies approximately 90% of all suspected illegal insider
trades in the typical case over the 21-day validation sample.
In contrast, the first and third
ARMA(1,1) model detection algorithms only identify around 60% of all suspected insider trading
21
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 23

(a) ROC Curves
(b) PR Curves
Figure 4: Vertically Averaged Receiver Operating Characteristic (ROC) and Precision Recall (PR) curves
for the NN DTW and ARMA(1,1) illegal insider trading detection models
transactions. The second detection algorithm identifies only 5.4% of suspected illegal transactions.
The differences in average recall between our NN DTW model and each of the three ARMA(1,1)
model detection algorithms are statistically significant at the 1% level. As discussed in Section 2,
brokers who fail to detect illegal trading activity may be subject to significant financial penalties.
Hence, the average recall scores presented in Table 5 highlight the utility of our market surveillance
for real-world market surveillance applications since this model minimizes regulatory risk at the
broker.
Precision scores demonstrate that, on average, approximately 67% of all transactions identified
by our NN DTW model belong to the suspected illegal insider account. This corresponds to a Type
1 error rate of 33%. None of the ARMA(1,1) detection algorithms achieve an average precision
score greater than 0.29. The Type 1 error rate of the ARMA(1,1) model exceeds 71%. As such, the
difference in average precision scores between our model and the ARMA(1,1) model is statistically
significant at the 1% level. The low precision and high Type 1 error rate of all three ARMA(1,1)
model detection algorithms suggests that in a real-world market surveillance system the volume of
false positive alerts generated by the model could be unmanageable.
We find that the average F1 score of our NN DTW model significantly exceeds the F1 scores
achieved by all three ARMA(1,1) detection algorithms and that these differences are statistically
significant at the 1% level. The information retrieval performance of the ARMA(1,1) model suggests
that the 10% significance threshold may not be optimal. Finally, we note that the total run time of
22
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 24

our model is approximately equal to that of the ARMA(1,1) model over the entire 21-day validation
period. However, if the time taken to construct the initial set of training sample anomaly scores in
the first iteration of the time series cross validation procedure is removed, our model is considerably
faster than the ARMA(1,1) model. Additional details regarding this comparison can be found in
the online supplementary materials file.
6.5
Point Anomaly Detection Model Benchmarks
An alternative to our time series modeling approach is to construct a model of normal broker account
trading behavior based upon individual transactions (feature vectors), rather than sequences of
transactions, thereby neglecting the temporal nature of the data. An advantage of this individual
transaction based modeling approach is that several well studied point anomaly detection models
can be readily applied. Point anomaly detection models refer to algorithms designed to identify
anomalous data points rather than sequences (Chandola et al., 2009). Since many point anomaly
detection models are implemented in open source machine learning software (Pedregosa et al.,
2011), one may regard the approach as an out-of-the-box solution to the insider trading detection
problem.
As a second benchmark for our NN DTW model we study how well point anomaly detection
models perform in the insider trading detection problem. Guided by the review of Emmott et al.
(2015) we select two state-of-the-art point anomaly detection models identified for general purpose
applications, namely the EGMM and iForest algorithm of Liu et al. (2012). These two anomaly de-
tection models are particularly powerful since they are ensemble learners. We also use a traditional
point anomaly detection algorithm, namely the OCSVM with Gaussian kernel (Sch¨olkopf et al.,
2001). All the models use exactly the same set of features described in Section 3. The performance
of each point anomaly detection benchmark model is evaluated using the time series cross-validation
procedure described in Figure 3. The parameters of each model are re-estimated for each day in
the validation sample as the rolling six-month training dataset is updated based upon the binary
class labels assigned to broker account transactions in the previous iteration. Details regarding the
implementation of the EGMM, iForest and OCSVM anomaly detection models can be found in the
online supplementary materials file.
Table 6 presents the AUROC curve and AUPR curve statistics for the EGMM, iForest, OCSVM
point anomaly detection models. For completeness, we re-tabulate the AUROC curve and AUPR
curve statistics for our NN DTW detection model. Figure 5 plots the vertically averaged ROC and
PR curves for our NN DTW detection model and the EGMM, iForest and OCSVM models. We
find that our model outperforms the EGMM, iForest and OCSVM models with respect to both the
mean AUROC curve and mean AUPR curve statistics. The difference in mean AUROC curve and
23
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 25

(a) ROC Curves
(b) PR Curves
Figure 5: Vertically Averaged Receiver Operating Characteristic (ROC) and Precision Recall (PR) curves
for NN DTW model and Ensemble Gaussian Mixture Model (EGMM), isolation Forest (iForest) and One-
Class Support Vector Machine (OCSVM) models.
AUPR curve statistics for NN DTW model are statistically significant at the 1% level. The mean
AUROC curve and AUPR curve scores for the EGMM and iForest point anomaly detection models
are similar and outperform the OCSVM, likely since both are ensemble learners. Interestingly, we
observe that the ARMA(1,1) detection algorithms 1 and 2 outperform the OCSVM, EGMM and
iForest models in terms of the average area under the precision recall curve.
Table 7 reports the information retrieval statistics for EGMM, iForest and OCSVM models.
Our NN DTW surveillance model continues to achieve substantially higher precision scores than
any benchmark algorithm by a statistically significant margin. The Type 1 error rate for all three
point anomaly detection models exceeds 57% in the typical case. Although this is an improvement
over the Type 1 error rate of the ARMA(1,1) model, it is still considerably larger than the Type
1 error rate of our NN DTW model. The average recall score achieved by our model exceeds the
mean recall scores of the EGMM and iForest models but is marginally below the mean recall score
of OCSVM. However, the mean F1 scores for EGMM, iForest and OCSVM are all statistically
significantly below the F1 score achieved by our NN DTW model. The F1 scores for the EGMM
and OCSVM models demonstrate that these models achieve a high recall score at the expense
of precision. This trade-off is generally unfavorable for practical market surveillance applications.
Hence, we demonstrate that our NN DTW insider trading detection model also outperforms three
point anomaly detection models, highlighting the utility of our time series detection approach.
24
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 26

6.6
Simulation Analysis
We simulate sequences of normal and anomalous trading activity to further study the detection
performance of our NN DTW model compared to the OCSVM, EGMM and iForest benchmark
detection models16. The procedure to simulate anomalous sequences that may be representative
of insider trading activity is as follows.
First, we randomly sample a broker account sequence
from the training dataset of normal trading activity associated with case 12 on validation day d1.
This randomly sampled broker account sequence is removed from the training dataset and the
NN DTW, OCSVM, EGMM and iForest models are retrained using the revised training dataset.
Let the variable n.modified controls the number of transactions that are selected to be modified
from the broker account sequence. Then, we replace the feature values for the set of features {trade
volume, residual volume, moving volume sum and participation rate} associated with these selected
transactions with random values between the 99th and 100th quantiles in the training dataset. For
example, simulations where n.modified = 100 represent cases where all transactions in the sequence
are anomalous while simulations where n.modified is less than 100 represent circumstances where
the illegal insider “hides” anomalous transactions among normal transactions.
Finally, we add a degree of warping, controlled by the variable warping, to the modified broker
account sequence using the algorithm in Dau et al. (2018).
Each transaction in the simulated
anomalous broker account sequence is assigned a true class label of −1. These anomalous sequences
simulate broker accounts that trade large volumes, since this is a common scenario observed in the
actual insider trading cases studied above.
To simulate sequences of normal trading activity, we repeat the sampling process described
above but modify a randomly chosen set of features for the sampled broker account sequence with
values drawn at random from the entire empirical distribution of the training data for a random
number of features.
A simulated normal trading sequence is therefore a randomly constructed
and warped permutation of the training dataset. Each transaction in the simulated normal broker
account sequence is assigned a true class label of +1.
We consider values of the variable n.modified ∈{50, 70, 90, 100}, values of the variable warping ∈
{30%, 50%}, and conduct 1000 replications of the simulation procedure to study classifier perfor-
mance. Table 8 reports the classification rates for each detection model. When every transaction
in a simulated broker account sequence is characterized by abnormally large volume features, all
detection models are able to perfectly identify the presence of anomalous trading activity. In sim-
ulations where 90% of transactions are anomalous, our NN DTW model yields the highest True
Negative classification Rate (TNR), that is 0.99 and 1 for the cases for warping values of 30% and
16The code for the simulation exercise is available at https://github.com/rjames6023/DTW-insider-detection
25
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 27

50%, respectively. This result indicates that the model is able to correctly identify more insider
trading activity than the benchmark detection algorithms. As the proportion of anomalous trans-
actions drops to 70% the TNR of our NN DTW model remains competitive with the TNR of the
benchmark algorithms. For the case where the proportion of anomalous transactions in the se-
quence drops to 50%, the OCSVM and the EGMM models have a marginally higher TNR than our
NN DTW model. This result is intuitive, since the NN DTW model is a sequence based anomaly
detection model while the OCSVM and EGMM models are point anomaly detection models. Our
NN DTW model always has a higher TNR than the iForest model.
The results of the True Positive classification Rate (TPR) and False Negative classification Rate
(FNR) highlight the superiority of the NN DTW model. Over all simulation scenarios, the FNR of
our NN DTW model is negligible, demonstrating that the model raises very few false alarms in our
simulations. This is an important result because the volume of false alerts generated by industry
market surveillance systems is typically high. The FNR of the OCSVM and the EGMM models are
high, suggesting that these models suffer from over-fitting and cannot identify randomly warped
permutations of the training data. While the FNR of the iForest model is much lower than that of
the OCSVM or EGMM models, it is still considerably larger than the rate associated with our NN
DTW model. Reassuringly, the classification rates for our NN DTW model are nearly identical for
both degrees of warping we consider.
7
Conclusion
Given the prevalence of asymmetric information in financial markets, the accurate and timely
detection of insider trading is of paramount importance. In this study, we develop a financial market
surveillance model for the early detection of insider trading. Our surveillance model addresses the
limitations of existing approaches proposed in the literature and the shortcomings of industry
standard market surveillance systems.
Our detection model relies on the application of the NN DTW algorithm to generate anomaly
scores for discrete sequences of broker account trading activity. Using DTW distance, we over-
come the difficulties associated with misalignment in transactions between two sequences of broker
account trading activity, ensuring that similarity is accurately measured. We then construct an
anomaly score threshold based upon the conditional tail expectation of anomaly scores in the
training data using statistically principled methods from the field of extreme value theory.
Our empirical study analyzes 14 suspected insider trading cases from suspicious trading reports.
This data pertains to a validation sample of 294 trading days of broker transaction data and over
5,000 suspected insider transactions. Our NN DTW model correctly identifies 90% of all suspected
26
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 28

illegal transactions in the validation sample and achieves a Type 1 error rate of 38% for the average
case. We demonstrate that our detection model outperforms the ARMA(1,1) model of Park and
Lee (2010) as well as three state-of-the-art anomaly detection techniques that could serve as out-
of-the-box solutions to detect insider trading. Simulations further demonstrate that our NN DTW
model raises considerably fewer false alarms than benchmark detection algorithms while still being
able to competitively identify sequences of potentially illegal trading activity.
The surveillance model we develop could be used by regulators, exchanges and brokers, and is
particularly suited to match the data constraints faced by individual brokers. The carefully designed
anomaly scoring algorithm allows our surveillance model to achieve substantial improvements in
detection performance over benchmark approaches, minimizing regulatory risk at the broker. We
believe that our one-class machine learning approach can be used in conjunction with existing expert
market surveillance systems to provide a holistic surveillance program at a broker. For example,
the alerts generated by our NN DTW anomaly detection model could be further analyzed using
the finely tuned rules from existing expert systems in order to identify the most pertinent alerts
that a surveillance analyst should review first. While we focus on insider trading, our framework
is sufficiently generic to allow the detection of other forms of illegal trading activities that are
performed on an intraday basis in limit order driven financial markets by modifying the multivariate
feature set used by the DTW algorithm.
Although we show that our model works particularly well for detecting suspected illegal insider
trading activity in the real world, our study has limitations. First, we only evaluated our model for
a sample of illegal insider trading cases in equity markets, since this is currently the most prevalent
task within the industry. Future research may wish to consider how the methodology could be
extended to detect cross-asset or cross-market illegal trading strategies. Second, we acknowledge
that the ARMA(1,1) model used as one of the benchmarks in our study is a relatively simplistic
statistical model. Third, we evaluated our model over a 21-day validation period for each of the 14
illegal insider trading cases that we study. Future work may wish to test our NN DTW model over a
longer horizon, such as an one-year validation period. Fourth, we use a set of features derived from
a review of the financial market microstructure literature that describe the trading behaviour of
individual broker accounts. Future research may wish to explore the performance of our approach
for different feature sets.
In addition, future research could extend our model in the following ways. First, the warping
window width parameter in the NN DTW algorithm could be set using a data driven approach.
One possibility here is to use transfer learning. Alternatively recent work has recast DTW as an
optimization problem which allows for a more general estimation procedure (see, e.g., Deriso and
Boyd, 2019). Second, an ensemble model could be created by using popular feature bagging and
27
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 29

subsampling techniques that explore subspaces of the data to further improve detection perfor-
mance. Finally, future research could consider how the contextual outlier detection approach of
Golmohammadi et al. (2014) and the EDM approach of Amiram et al. (2020) could be applied to
detect illegal trading activity based upon individual time series of broker transactions and if these
approaches could be combined with our NN DTW model to improve the identification of illegal
insider trading.
28
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 30

A
Mechanics of Multivariate DTW
For the exposition which follows, let A and B denote two multivariate sequences of p features with
m observations, that is A and B are m × p data matrices. We refer to the multivariate sequence
A as the query sequence which is drawn from the testing data and to the multivariate sequence B
as the candidate sequence which is drawn from the training data. We wish to define a mapping
between the observations in A with respect to the observations in B by warping A. It is assumed
that all features have been standardized to zero mean and unit variance so the solution is scale-
invariant. DTW begins by initializing an m × m cost matrix C containing the Euclidean distances
between all possible combinations of row vectors {ai, i = 1 . . . , m} and {bj, j = 1 . . . , m} from A
and B respectively,
Cij = ∥ai −bj∥2, i, j = 1, . . . , m,
(4)
where || · ||2 denotes the Euclidean norm. A contiguous warping path containing pairs of indices
ϕ = {ϕl : ϕl = (i, j)l, l = 1, . . . L}, is traced through the cost matrix to define the alignment
between observations. Each observation ai may be mapped to more than one bj, and vice versa.
The alignment cost associated with a warping path, and therefore the distance between the two
input sequences, is the sum of Euclidean distances along the warping path,
cp =
L
X
l=1
Cϕl
(5)
The optimal warping path produces the alignment of lowest cost, subject to a number of con-
straints. Formally, we can write the optimal warping path search problem as
min
ϕ
X
(i,j)∈ϕ
Cij
(6)
Subject to:
ϕ1 = (1, 1)
(7)
ϕL = (m, m)
(8)
ϕl −ϕl−1 ∈{(1, 1), (0, 1), (1, 0)}
(9)
ϕl =









(i + φ, i)
if i > j + φ
(j, j + φ)
if j > i + φ
(i, j)
otherwise
(10)
The first three constraints (7), (8) and (9) state that the warping path must consider all points in
both sequences, must be continuous with a step size of one and that no backward matching is allowed
29
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 31

(the slope of the warping path must be non-negative at all points). The fourth constraint (10),
referred to within the literature as the Warping Window Width constraint, effectively restricts the
cost matrix, and the credible region of the optimal warping path, to be a band matrix with identical
upper and lower bandwidths which are equal to the constant φ. Intuitively, this constraint limits
how far forward or backward in time an observation can be warped, to ensure the solution remains
realistic. Restricting the search space of the optimal warping path also reduces the complexity
of the DTW algorithm. For synchronous data, one obtains the Euclidean mapping between two
sequences as a special case of DTW where the warping path lies along the diagonal of the cost
matrix.
The optimal warping path is the solution to a dynamic programming problem. This solution is
obtained by constructing a cumulative cost matrix, denoted by C∗. The initial condition is
C∗
i,j =



∞,
if i = 1 or j = 1
0,
if i = j = 1
(11)
The recurrence relation used to obtain the solution is
C∗
i,j = Ci,j + min









C∗
i−1,j
C∗
i,j−1
C∗
i−1,j−1
for i, j = 2, . . . , m
(12)
Once the cumulative cost matrix C∗has been recursively filled the DTW distance between the
two input sequences is
DTW(A, B) =
q
C∗m,m
(13)
30
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 32

B
Complexity Reduction Techniques
At each iteration of the nearest neighbor search for a query broker account sequence, we store the
best-so-far (BSF) DTW distance in memory. The BSF distance is defined as the current smallest
DTW distance across all previously searched candidate broker account sequences in the training
dataset.
Lower bound functions rely on this BSF distance to prune candidate broker account
sequences before computing the full DTW distance. A lower bound function takes as input, the
query and candidate sequences and returns a scalar value that is guaranteed to be smaller than
the true DTW distance.
A pragmatic lower bound must be faster to compute than the true
DTW distance and must closely approximate the true DTW distance, a property referred to as the
”tightness” of the lower bound. The three lower bounds used in this study are implemented in a
cascading fashion in order of complexity to determine if the current candidate training sequence
can be pruned from the nearest neighbor search. We describe these bounds in ascending order of
complexity.
The first lower bound, referred to as the modified LB Kim lower bound (Rakthanmanon et al.,
2013), recognizes that the sum of the Euclidean distance between the first pair of observations and
the Euclidean distance between the last pair of observations is always a component of the total
DTW distance, as per constraint (7) and (8). The modified LB Kim lower bound is
LB Kim(A, B) = ∥a1 −b1∥2 + ∥am −bm∥2
(14)
If in any iteration of the nearest neighbor search, LB Kim exceeds the BSF distance then we may
abandon the current candidate sequence comparison and proceed to the next iteration since the
current candidate sequence cannot possibly be the nearest neighbor.
If LB Kim does not exceed the BSF distance we compute a second tighter but computationally
more expensive lower bound, known as LB Keogh (Keogh and Ratanamahatana, 2005).
The
LB Keogh lower bound builds an envelope around the query sequence based upon the size of the
Warping Window Width constraint parameter φ. The LB Keogh lower bound is
LB Keogh(B, U, L) =
v
u
u
u
u
u
u
t
m
X
q=1
p
X
k=1









(Bkq −Ukq)2
if Bkq > Ukq
(Bkq −Lkq)2
if Bkq < Lkq
0
otherwise
(15)
31
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 33

where
Ukq = Max(Ak−φ:k+φ,q)
(16)
Lkq = Min(Ak−φ:k+φ,q)
(17)
are the upper and lower envelope sequences with a width dependent on the size of φ. Since the
query sequence is fixed during the nearest neighbor search the upper and lower envelope sequences
only need to be computed once in the first iteration and can be re-used for all other iterations. If
the LB Keogh lower bound exceeds the BSF distance then we may abandon the current candidate
sequence comparison and proceed to the next iteration of the nearest neighbor search.
Finally, if both LB Kim and LB Keogh do not exceed the BSF distance a third lower bound
is computed, referred to as LB Improved (Lemire, 2009). The LB Improved lower bound uses
the information from the LB Keogh lower bound to compute B
′, the projection of the candidate
sequence B on the upper and lower envelopes
B
′
kq =









Ukq
if Bkq > Ukq
Bkq
if Lkq < Bkq < Ukq
Lkq
if Bkq < Lkq
Expression (16) and (17) are reused to compute U
′
kq and L
′
kq by replacing A with B
′. The
LB Improved lower bound is then,
LB Improved = LB Keogh(B, U, L) + LB Keogh(A, U
′, L
′)
If all three aforementioned lower bounds are smaller than the BSF distance we proceed by
implementing two early abandoning strategies during the computation of the DTW distance (Rak-
thanmanon et al., 2013). Early abandoning specifies conditions under which it is possible to stop
the DTW distance computation early if the current candidate sequence cannot be the nearest
neighbor. Both strategies make use of the recurrence relation (12), to access a partial value of the
full DTW distance in the ith iteration, which is min{C∗
i1, . . . , C∗
im}. The first early abandoning
strategy states that if the partial DTW distance exceeds the BSF distance the current candidate
sequence comparison can be abandoned and we may proceed to the next iteration of the nearest
neighbor search.
The second early abandoning strategy uses the sum of the partial DTW distance and the
32
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 34

remaining portion of the LB Keogh lower bound, which is
min {C∗
i1, . . . , C∗
im} + LB Keogh(Ai:m,1:m, Ui:m,1:m, Li:m,1:m)
If this quantity exceeds the BSF we can abandon the current candidate sequence comparison and
proceed to the next iteration of the nearest neighbor search.
Algorithm 1 presents pseudo code for the NN DTW anomaly scoring function. The nearest
neighbor search begins by initializing the best-so-far DTW distance (BSFdistance) to infinity.
We then search through all broker account sequences in the training dataset to find the nearest
neighbor. Lines 3 to 9 perform the lower bound function checks implemented in cascading order of
computational complexity. Lines 10 to 13 compute the true DTW distance and check if the DTW
distance calculation was early abandoned, in which case the distance score is set to the placeholder
value of infinity.
The BSF distance is updated if the DTW distance score is smaller than the
prevailing BSF distance in the current iteration.
Algorithm 1: NN DTW Anomaly Scoring Function
Input
: Training dataset X, Query Sequence A
Output : Scalar Anomaly Score for the Query Sequence
Initialize: BSFdistance = ∞
1 for i = 1, . . . , |X| do
2
B = Xi
3
if LB Kim(A, B) < BSFdistance then
4
if i = 1 then
5
Construct upper and lower envelope sequences U, L (See (16) and (17))
6
if LB Keogh(B, U, L) < BSFdistance = 0 then
7
Construct projection sequence B
′
8
Construct upper and lower envelope sequences U
′, L
′ around B
′
9
if LB Keogh(B, U, L) + LB Keogh(A, U
′, L
′) < BSFdistance then
10
if DTW(A, B) is early abandoned then
11
DTW distance score = ∞
12
else
13
DTW distance score = DTW(A, B)
14
else
15
DTW distance score = ∞
16
else
17
DTW distance score = ∞
18
else
19
DTW distance score = ∞
20
if DTW distance score < BSFdistance then
21
BSFdistance = DTW distance score
22 anomaly score = BSFdistance
33
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 35

C
Peaks-Over-Threshold Extreme Value Theory
Let F denote the common but unknown distribution of the anomaly scores. Exceedances of the
anomaly scores above a high initial threshold value are the set Z = {ϑid−u|ϑid > u, i = 1 . . . Nd : d ∈
I1}. The Pickands-Balkema-de Haan theorem (Pickands, 1975; Balkema and De Haan, 1974) states
that the distribution of the exceedances converges to the generalized Pareto family of distributions
for a suitably large threshold value,
lim
u→F +
sup
0<z<ϑ(X)+−u
|Pr(Z < z) −Gξ,σ(z)| = 0
(18)
where F + is the right endpoint of F, ϑ(X)+ is the largest training sample anomaly score and Gξ,σ
is the generalized Pareto distribution function with shape parameter ξ and scale parameter σ.
The generalized Pareto distribution function is
Gξ,σ(z) =







1 −

1 + ξz
σ
−1/ξ
,
for ξ ̸= 0, z > 0
1 −exp

−z
σ

,
for ξ = 0, z > 0
(19)
When ξ > 0, the generalized Pareto distribution is heavy tailed. The shape and scale parameters
are estimated via Maximum Likelihood Estimation where the log-likelihood function is given in
Coles (2001). Let ˆξ and ˆσ denote the parameter estimates.
Assuming that the tail of F, the distribution of training sample anomaly scores, begins at u,
then for some η > u, the following inequality holds for observations in the tail:
F(η) = 1 −(1 −F(u))(1 −Fu(η −u)),
η > u
(20)
where Fu is the distribution of the excess loss beyond u. The POT method constructs an estimate
for F(η). The term (1−F(u)) is approximated non-parametrically by the proportion of observations
in the tail region above u, which is Nu/N, where Nu = |Z| is the cardinality of Z and N = |ϑ(X)| is
the cardinality of ϑ(X). The distribution of the excess loss beyond Fu(η −u) is generalized Pareto
by the Pickands-Balkema-de Haan theorem. Hence, the POT tail estimator is
ˆF(η) = ˆFZ(z) = 1 −Nu
N

1 + ξz
σ
−1/ξ
,
η > u
(21)
An estimator of the extreme α-quantile can be obtained by inverting the POT tail estimator
34
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 36

ˆFZ as follows:
ˆQ(α) = ˆF −1
Z (α) ≡u + ˆσ
ˆξ
" N
Nu
(1 −α)
−ˆξ
−1
#
,
α > F(u)
(22)
To derive an estimator of the CTE we use the fact that E[ϑid −u|ϑid > u, i = 1 . . . Nd : d ∈
I1] = σ/(1 −ξ) (for ξ < 1) and that for some u′ > u the excedances {ϑid −u′|ϑid > u′} also
follow a generalized Pareto distribution with an identical shape parameter ξ but a transformed
scale parameter σ′ = σ + ξ(u′ −u) (Coles, 2001).
35
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 37

D
Time Series Cross Validation Details
In the first iteration the first set of training sample anomaly scores, denoted by ϑ(X)
1
, is constructed
by computing the NN DTW distance for each broker account sequence with respect to all other
broker account sequences in the first 6-month training dataset. The remaining steps in the first iter-
ation of the time series cross-validation process, and the steps required in all subsequent iterations
are summarized as follows. For d = 1, . . . , 21,
1. Compute the dth anomaly score threshold, denoted τ (α)
d
, by estimating the parameters of the
generalized Pareto distribution based upon ϑ(X)
d
, as outlined in Section 5.
2. Construct the dth set of testing sample anomaly scores, denoted ϑ(Y )
d
, by computing the
NN DTW distance for each broker account sequence in the dth one-day testing dataset with
respect to all broker account sequences in the dth six-month training dataset.
3. Construct the dth class label vector ˆy(d) = −sign(ϑ(Y )
d
−τ (α)
d
).
4. Construct the (d+1)th six-month training sample by appending sequences classified as normal
in the dth testing sample to the end of the dth six-month training sample. Remove all sequences
for the first day in (d + 1)th six-month training sample.
5. Construct the (d + 1)th set of training sample anomaly scores by appending anomaly scores
for sequences classified as normal in the dth testing sample to the end of the dth set of training
sample anomaly scores. Remove all sequences for the first day in (d + 1)th set of training
sample anomaly scores.
The set of training sample anomaly scores needs to be built from scratch only once in the
first iteration of the cross-validation procedure. In all subsequent iterations, the set of training
sample anomaly scores is updated based upon the class labels assigned in the previous iteration.
In practice, since the first step is computationally intensive, the construction of ϑ(X)
1
could be
performed offline, before the implementation of the detection model.
36
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 38

Table 1: Trading Activity Statistics for the Suspected Insider Account
The table reports descriptive statistics of trading activity for the suspected illegal insider account in each case. The
variable First Trade Date is the number of days prior to the information release date that the insider started trading.
The variable Insider Volume is expressed in millions of U.S. dollars.
First Trade date
No. Insider Trades
Average No. Insider trades per day active
Insider Volume
Case 1
4
254
127
2.70
Case 2
9
105
26
0.50
Case 3
1
13
13
1.53
Case 4
7
1070
178
7.70
Case 5
10
2230
278
90.00
Case 6
2
84
84
1.71
Case 7
2
583
583
10.66
Case 8
7
196
196
3.43
Case 9
2
264
132
1.70
Case 10
2
183
91.5
4.31
Case 11
1
134
134
2.46
Case 12
1
511
511
19.96
Case 13
2
37
37
1.52
Case 14
1
238
238
1.14
Mean
3.64
421.57
187.75
10.66
Total
5902
149.31
37
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 39

Table 2: Abnormal Returns Around Information Release Dates
The table reports Abnormal return information for each alleged illegal insider trading case in the sample. The variable
CAR(−10, −1) denotes the cumulative abnormal return over the 10-day pre information release period. The variable
AR(0) denotes the information release day abnormal return. Abnormal returns are expressed as a percentage. The
model used to compute abnormal returns and the bootstrap procedure used to establish statistical significance is
described in (Dubow and Monteiro, 2006). ***, ** and * represent statistical significance at the 1%, 5% and 10%
significance levels, respectively.
CAR(-10,-1)
AR(0)
Case 1
1.281
-10.184
Case 2
-4.82
-40.796
Case 3
-5.552
-7.455
Case 4
-7.318
-10.473
Case 5
38.336***
20.187
Case 6
55.682
-6.646
Case 7
10.775
-7.224
Case 8
-6.983
-10.582
Case 9
1.629
-8.899
Case 20
2.787
-6.519
Case 11
-1.048
-5.174
Case 12
4.357
4.379
Case 13
-6.609**
-5.063
Case 14
-0.578
-7.817
38
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 40

Table 3: Summary Statistics for Model Features
The table reports summary statistics for each of the features used in our illegal insider trading detection model, computed for the initial
six-month training dataset and 10-day validation dataset. Mathematical definitions of each feature are presented in the online supplementary
materials file. T-statistics are reported for differences in the mean of each feature between the training dataset and validation sample. With
the exception of the feature Participation rate, all trade volume statistics are reported in 000’s of shares. The features Immediate Price Impact,
Adverse Selection Spread Component and Realized Volatility have been multiplied by 100 for exposition. ***, ** and * represent statistical
significance at the 1%, 5% and 10% significance levels, respectively.
(i) Training Sample
(ii) Validation Sample
Mean
Median
Std
Min
Max
Mean
Median
Std
Min
Max
Difference
Panel A: Trade Volume Features
Volume
7.199
2.000
22.884
0.100
1127.000
7.894
2.000
20.602
0.100
700.000
3.914***
Short Sell Volume
3.380
0.000
17.186
0.000
1127.000
3.871
0.000
15.684
0.000
411.000
3.677***
Residual Trade Volume
0.126
-2.461
22.264
-94.827
1117.946
0.289
-2.600
19.822
-76.803
665.629
0.945
Moving Window Volume
329.624
52.800
1624.612
0.000
26184.000
216.472
65.400
359.969
0.100
3344.000
-9.551***
Participation Rate
0.052
0.020
0.087
0.000
1.000
0.072
0.027
0.116
0.000
1.000
26.878***
Panel B: Illiquidity Features
Immediate Price Impact
0.022
0.000
0.125
-4.577
3.611
0.022
0.000
0.127
-1.667
2.102
-0.331
Adverse Selection Spread Component
-0.004
0.014
1.086
-14.297
18.934
0.075
0.030
1.233
-11.128
10.526
8.955***
Adjusted Trade Duration
0.154
0.021
0.288
0.000
1.000
0.152
0.026
0.281
0.000
1.000
-0.884
Panel C: Volatility Feature
Realized Volatility
0.025
0.010
0.063
0.000
1.522
0.026
0.011
0.042
0.000
0.476
2.507**
39
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 41

Table 4: Area Under the Curve Statistics for the 1-NN DTW and ARMA(1,1) Illegal Insider Trading detection model.
The table reports Area Under the Receiver Operating Characteristic (AUROC) curve statistics and Area Under the Precision Recall (AUPR)
curve statistics for the NN DTW illegal insider trading detection model and the three detection algorithms from the ARMA(1,1) benchmark
model of (Park and Lee, 2010) for all 14 cases. Differences in mean area under the curve statistics between the NN DTW model and each of
the three ARMA(1,1) model detection algorithms are presented in the final row. Statistical significance of each difference is established using a
Wilcoxon Signed Ranks Test. ***, ** and * represent statistical significance at the 1%, 5% and 10% significance levels, respectively.
(i) Receiver Operating Characteristic Curve
(ii) Precision Recall Curve
NN DTW
ARMA(1,1) Algorithm 1
ARMA(1,1) Algorithm 2
ARMA(1,1) Algorithm 3
NN DTW
ARMA(1,1) Algorithm 1
ARMA(1,1) Algorithm 2
ARMA(1,1) Algorithm 3
Case 1
1.000
0.550
0.579
0.647
1.000
0.658
0.666
0.686
Case 2
1.000
0.500
0.833
0.762
1.000
0.850
0.938
0.907
Case 3
0.997
0.538
0.720
0.935
0.325
0.501
0.501
0.011
Case 4
0.855
0.536
0.573
0.772
0.537
0.578
0.559
0.587
Case 5
0.907
0.529
0.514
0.609
0.912
0.943
0.934
0.934
Case 6
1.000
0.515
0.535
0.180
1.000
0.501
0.501
0.001
Case 7
1.000
0.439
0.568
0.303
1.000
0.885
0.924
0.816
Case 8
0.944
0.528
0.590
0.383
0.736
0.608
0.586
0.134
Case 9
0.992
0.551
0.618
0.742
0.899
0.633
0.649
0.690
Case 10
0.992
0.545
0.496
0.355
0.848
0.513
0.443
0.132
Case 11
1.000
0.620
0.647
0.244
1.000
0.632
0.629
0.107
Case 12
0.984
0.545
0.619
0.535
0.756
0.511
0.491
0.199
Case 13
1.000
0.709
0.701
0.888
1.000
0.513
0.512
0.531
Case 14
0.935
0.581
0.876
0.250
0.982
0.979
0.995
0.936
Average
0.972
0.549***
0.634***
0.543***
0.857
0.665**
0.666**
0.477***
40
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 42

Table 5: Information Retrieval Statistics for the NN DTW and ARMA(1,1) Illegal Insider Trading Detection models.
The table reports Precision, Recall and F1 scores for the NN DTW illegal insider trading detection model and for the three detection algorithms
from the ARMA(1,1) benchmark model. Differences in mean information retrieval statistics between the NN DTW model and each of the three
ARMA(1,1) model detection algorithms are presented in the final row. Statistical significance of each difference is established using a Wilcoxon
Signed Ranks Test. ***, ** and * represent statistical significance at the 1%, 5% and 10% significance levels, respectively.
(i) NN DTW
(ii) ARMA(1,1) Algorithm 1
(iii) ARMA(1,1) Algorithm 2
(iv) ARMA(1,1) Algorithm 3
Precision
Recall
F1
Precision
Recall
F1
Precision
Recall
F1
Precision
Recall
F1
Case 1
1.000
1.000
1.000
0.000
0.000
0.000
0.000
0.000
0.000
0.000
0.000
0.000
Case 2
1.000
1.000
1.000
0.500
0.429
0.462
0.000
0.000
0.000
0.600
0.429
0.500
Case 3
0.022
1.000
0.042
0.002
1.000
0.003
0.000
0.000
0.000
0.001
1.000
0.003
Case 4
0.365
0.718
0.484
0.047
0.217
0.077
0.047
0.058
0.052
0.047
0.217
0.077
Case 5
0.910
0.581
0.709
0.834
0.513
0.635
0.852
0.124
0.217
0.834
0.514
0.636
Case 6
0.150
1.000
0.261
0.007
1.000
0.015
0.000
0.000
0.000
0.007
1.000
0.014
Case 7
0.739
1.000
0.850
0.942
0.539
0.686
0.067
0.002
0.004
0.931
0.531
0.676
Case 8
0.601
0.562
0.581
0.247
0.964
0.393
0.088
0.089
0.088
0.239
0.964
0.383
Case 9
0.974
1.000
0.987
0.010
0.013
0.011
0.000
0.000
0.000
0.009
0.013
0.010
Case 10
0.377
1.000
0.547
0.036
0.766
0.069
0.026
0.125
0.042
0.036
0.766
0.068
Case 11
0.717
1.000
0.835
0.307
1.000
0.470
0.023
0.029
0.026
0.282
1.000
0.440
Case 12
0.651
0.914
0.760
0.098
0.860
0.175
0.046
0.177
0.073
0.096
0.860
0.173
Case 13
1.000
1.000
1.000
0.000
0.000
0.000
0.000
0.000
0.000
0.000
0.000
0.000
Case 14
0.916
0.870
0.892
0.978
0.964
0.971
0.846
0.158
0.267
0.964
0.971
0.968
Average
0.673
0.903
0.711
0.286***
0.59**
0.283***
0.142***
0.054***
0.055***
0.289***
0.59**
0.282***
41
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 43

Table 6: Area Under the Curve Statistics for the NN DTW, EGMM, iForest and OCSVM Illegal Insider Trading Detection
models.
The table reports Area Under the Receiver Operating Characteristic (AUROC) curve statistics and Area Under the Precision Recall (AUPR)
curve statistics for the NN DTW illegal insider trading detection model and the Ensemble Gaussian Mixture (EGMM), isolation Forest (iForest)
and One-Class Support Vector Machine (OCSVM) detection models.
Differences in mean area under the curve statistics between the NN
DTW models and each of the EGMM, iForest and OCSVM models are presented in the final row. Statistical significance of each difference
is established using a Wilcoxon Signed Ranks Test. ***, ** and * represent statistical significance at the 1%, 5% and 10% significance levels,
respectively.
(i) Receiver Operating Characteristic Curve
(ii) Precision Recall Curve
NN DTW
EGMM
iForest
OCSVM
NN DTW
EGMM
iForest
OCSVM
Case 1
1.000
0.726
0.833
0.806
1.000
0.596
0.493
0.366
Case 2
1.000
1.000
0.580
1.000
1.000
1.000
0.639
1.000
Case 3
0.997
0.976
0.960
0.915
0.325
0.158
0.303
0.031
Case 4
0.855
0.842
0.763
0.619
0.537
0.579
0.365
0.154
Case 5
0.907
0.877
0.743
0.761
0.912
0.871
0.721
0.793
Case 6
1.000
0.654
0.774
0.759
1.000
0.068
0.303
0.082
Case 7
1.000
0.932
0.897
0.914
1.000
0.927
0.819
0.872
Case 8
0.944
0.676
0.754
0.708
0.736
0.333
0.361
0.239
Case 9
0.992
0.684
0.743
0.662
0.899
0.372
0.437
0.275
Case 10
0.992
0.787
0.868
0.879
0.848
0.090
0.201
0.361
Case 11
1.000
0.547
0.798
0.860
1.000
0.097
0.231
0.530
Case 12
0.984
0.943
0.910
0.871
0.756
0.463
0.316
0.174
Case 13
1.000
0.994
0.995
0.888
1.000
0.977
0.919
0.114
Case 14
0.935
0.859
0.564
0.629
0.982
0.910
0.744
0.758
Average
0.972
0.821***
0.799***
0.805***
0.857
0.532***
0.489***
0.41***
42
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 44

Table 7: Information Retrieval Statistics for the NN DTW, EGMM, iForest and OCSVM Illegal Insider Trading Detection
models.
The table reports precision, recall and F1 scores for the NN DTW illegal insider trading detection model and for the Ensemble Gaussian
Mixture (EGMM), isolation Forest (iForest) and One-Class Support Vector Machine (OCSVM) models.
Differences in mean information
retrieval statistics between the NN DTW model and each of the EGMM, iForest and OCSVM models are presented in the final row. Statistical
significance of each difference is established using a Wilcoxon Signed Ranks Test. ***, ** and * represent statistical significance at the 1%, 5%
and 10% significance levels, respectively.
(i) NN DTW
(ii) EGMM
(iii) iForest
(iv) OCSVM
Precision
Recall
F1
Precision
Recall
F1
Precision
Recall
F1
Precision
Recall
F1
Case 1
1.000
1.000
1.000
0.200
0.780
0.318
0.469
0.327
0.385
0.260
0.925
0.406
Case 2
1.000
1.000
1.000
0.856
1.000
0.922
0.595
0.143
0.230
0.606
1.000
0.755
Case 3
0.022
1.000
0.042
0.013
1.000
0.026
0.028
0.846
0.054
0.007
1.000
0.014
Case 4
0.365
0.718
0.484
0.252
0.950
0.399
0.299
0.641
0.408
0.167
0.883
0.282
Case 5
0.910
0.581
0.709
0.680
0.942
0.790
0.726
0.542
0.621
0.567
0.898
0.695
Case 6
0.150
1.000
0.261
0.053
1.000
0.100
0.186
0.452
0.264
0.061
0.964
0.114
Case 7
0.739
1.000
0.850
0.590
0.971
0.734
0.803
0.770
0.786
0.423
0.991
0.593
Case 8
0.601
0.562
0.581
0.343
0.613
0.440
0.413
0.341
0.374
0.225
0.931
0.363
Case 9
0.974
1.000
0.987
0.455
0.595
0.516
0.567
0.481
0.520
0.268
0.913
0.414
Case 10
0.377
1.000
0.547
0.100
0.978
0.181
0.196
0.596
0.295
0.090
0.940
0.164
Case 11
0.717
1.000
0.835
0.122
0.455
0.193
0.246
0.351
0.289
0.134
0.970
0.236
Case 12
0.651
0.914
0.760
0.192
0.928
0.318
0.310
0.753
0.439
0.103
0.982
0.186
Case 13
1.000
1.000
1.000
0.112
1.000
0.201
0.353
0.973
0.518
0.051
1.000
0.098
Case 14
0.916
0.870
0.892
0.922
0.996
0.958
0.750
0.025
0.049
0.769
0.882
0.822
Average
0.673
0.903
0.711
0.349***
0.872
0.435***
0.424***
0.517***
0.374***
0.267***
0.949
0.367***
43
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 45

Table 8: Simulation Results
The table reports the classification rates from the simulation exercise described in Section 6.6. The simulation
design parameter n.modified is the number of observations that are modified in the randomly chosen broker
account sequence. The simulation design parameter warping is the degree of warping that is added to the
randomly chosen broker account sequence.
TNR
FPR
TPR
FNR
TNR
FPR
TPR
FNR
n.modified = 100, warping = 30%
n.modified = 100, warping = 50%
NN DTW
1.000
0.000
0.999
0.001
1.000
0.000
1.000
0.000
OCSVM
1.000
0.000
0.127
0.873
1.000
0.000
0.119
0.881
EGMM
1.000
0.000
0.152
0.848
1.000
0.000
0.103
0.897
iForest
1.000
0.000
0.898
0.102
1.000
0.000
0.907
0.094
n.modified = 90, warping = 30%
n.modified = 90, warping = 50%
NN DTW
0.999
0.001
0.999
0.001
1.000
0.000
0.997
0.003
OCSVM
0.979
0.021
0.149
0.851
0.989
0.011
0.140
0.860
EGMM
0.976
0.024
0.171
0.830
0.988
0.012
0.117
0.883
iForest
0.934
0.066
0.904
0.096
0.931
0.069
0.903
0.097
n.modified = 70, warping = 30%
n.modified = 70, warping = 50%
NNN DTW
0.938
0.062
0.998
0.002
0.928
0.072
0.999
0.001
OCSVM
0.937
0.063
0.180
0.820
0.968
0.032
0.181
0.819
EGMM
0.928
0.072
0.200
0.800
0.965
0.035
0.141
0.859
iForest
0.797
0.203
0.906
0.094
0.788
0.212
0.907
0.093
n.modified = 50, warping = 30%
n.modified = 50, warping = 50%
NN DTW
0.828
0.172
0.999
0.001
0.843
0.157
1.000
0.000
OCSVM
0.893
0.107
0.231
0.769
0.941
0.059
0.223
0.777
EGMM
0.877
0.123
0.239
0.761
0.936
0.064
0.173
0.827
iForest
0.645
0.355
0.909
0.091
0.631
0.369
0.912
0.088
44
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 46

References
Ahmad, S., A. Lavin, S. Purdy, and Z. Agha (2017). Unsupervised real-time anomaly detection for
streaming data. Neurocomputing 262, 134–147.
Aitken, M., D. Cumming, and F. Zhan (2015). Exchange trading rules, surveillance and suspected
insider trading. Journal of Corporate Finance 34, 311–330.
Aitken, M. J., F. H. d. B. Harris, and S. Ji (2015). A worldwide examination of exchange market
quality: Greater integrity increases market efficiency. Journal of Business Ethics 132(1), 147–
170.
Amiram, D., E. Lyandres, and D. Rabetti (2020). Competition and product quality: Fake trading
on crypto exchanges. Available at SSRN 3745617.
ASIC (2019). Review of Australian Equity Market Cleanliness. Technical report, Australian Secu-
rities and Investments Commission.
Ausubel, L. M. (1990). Insider trading in a rational expectations economy. The American Economic
Review 80(5), 1022–1041.
Axelsson, S. (2000). The base-rate fallacy and the difficulty of intrusion detection. ACM Transac-
tions on Information and System Security (TISSEC) 3(3), 186–205.
Back, K. and S. Baruch (2004). Information in securities markets: Kyle meets glosten and milgrom.
Econometrica 72(2), 433–465.
Bader, B., J. Yan, and X. Zhang (2018). Automated threshold selection for extreme value analysis
via ordered goodness-of-fit tests with adjustment for false discovery rate. The Annals of Applied
Statistics 12(1), 310–329.
Bagnall, A., J. Lines, A. Bostrom, J. Large, and E. Keogh (2017). The great time series classification
bake off: a review and experimental evaluation of recent algorithmic advances. Data Mining and
Knowledge Discovery 31(3), 606–660.
Balkema, A. A. and L. De Haan (1974). Residual life time at great age. The Annals of Probabil-
ity 2(5), 792–804.
Bolton, R. J. and D. J. Hand (2002). Statistical fraud detection: A review. Statistical Science 17(3),
235–255.
45
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 47

Chandola, V., A. Banerjee, and V. Kumar (2009). Anomaly detection: A survey. ACM Computing
Surveys (CSUR) 41(3), 15.
Cline, B. N. and V. V. Posylnaya (2019). Illegal insider trading: Commission and sec detection.
Journal of Corporate Finance 58, 247–269.
Coles, S. (2001). An introduction to statistical modeling of extreme values, Volume 208. Springer.
Comerton-Forde, C. and T. J. Putni¸nˇs (2011). Measuring closing price manipulation. Journal of
Financial Intermediation 20(2), 135–158.
Cong, L. W., X. Li, K. Tang, and Y. Yang (2021).
Crypto wash trading.
arXiv preprint
arXiv:2108.10984.
Cumming, D., S. Johan, and D. Li (2011). Exchange trading rules and stock market liquidity.
Journal of Financial Economics 99(3), 651–671.
Dau, H. A., D. F. Silva, F. Petitjean, G. Forestier, A. Bagnall, A. Mueen, and E. Keogh (2018).
Optimizing dynamic time warping’s window width for time series data mining applications. Data
Mining and Knowledge Discovery 32(4), 1074–1120.
DeMarzo, P. M., M. J. Fishman, and K. M. Hagerty (1998). The optimal enforcement of insider
trading regulations. Journal of Political Economy 106(3), 602–632.
Demˇsar, J. (2006). Statistical comparisons of classifiers over multiple data sets. Journal of Machine
Learning Research 7(1), 1–30.
Deng, S., C. Wang, M. Wang, and Z. Sun (2019). A gradient boosting decision tree approach for
insider trading identification: An empirical model evaluation of china stock market. Applied Soft
Computing 83, 105652.
Deriso, D. and S. Boyd (2019). A general optimization framework for dynamic time warping. arXiv
preprint arXiv:1905.12893.
Derrig, R. A. (2002). Insurance fraud. Journal of Risk and Insurance 69(3), 271–287.
Diaz, D., B. Theodoulidis, and P. Sampaio (2011). Analysis of stock market manipulations using
knowledge discovery techniques applied to intraday trade prices. Expert Systems with Applica-
tions 38(10), 12757–12771.
46
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 48

Ding, H., G. Trajcevski, P. Scheuermann, X. Wang, and E. Keogh (2008). Querying and mining of
time series data: experimental comparison of representations and distance measures. Proceedings
of the VLDB Endowment 1(2), 1542–1552.
Dubow, B. and N. B. Monteiro (2006). Measuring market cleanliness. Available at SSRN 1019999.
Easley, D. and M. O’hara (1987). Price, trade size, and information in securities markets. Journal
of Financial Economics 19(1), 69–90.
Emmott, A., S. Das, T. Dietterich, A. Fern, and W.-K. Wong (2015). A meta-analysis of the
anomaly detection problem. arXiv preprint arXiv:1503.01158.
Fernandes, N. and M. A. Ferreira (2009). Insider trading laws and stock price informativeness. The
Review of Financial Studies 22(5), 1845–1887.
Glosten, L. R. and P. R. Milgrom (1985). Bid, ask and transaction prices in a specialist market
with heterogeneously informed traders. Journal of Financial Economics 14(1), 71–100.
Golmohammadi, K., O. R. Zaiane, and D. D´ıaz (2014). Detecting stock market manipulation using
supervised learning algorithms. In 2014 International Conference on Data Science and Advanced
Analytics (DSAA), pp. 435–441. IEEE.
G’Sell, M. G., S. Wager, A. Chouldechova, and R. Tibshirani (2016). Sequential selection procedures
and false discovery rate control. Journal of the Royal Statistical society: Series B (Statistical
Methodology) 78(2), 423–444.
Hasbrouck, J. (1991).
Measuring the information content of stock trades.
The Journal of Fi-
nance 46(1), 179–207.
Hautsch, N. and M. Podolskij (2013).
Preaveraging-based estimation of quadratic variation in
the presence of noise and jumps: Theory, implementation, and empirical evidence. Journal of
Business & Economic Statistics 31(2), 165–183.
He, H. and J. Wang (1995). Differential information and dynamic behavior of stock trading volume.
The Review of Financial Studies 8(4), 919–972.
Islam, S. R., S. K. Ghafoor, and W. Eberle (2018). Mining illegal insider trading of stocks: a
proactive approach. In 2018 IEEE International Conference on Big Data (Big Data), pp. 1397–
1406. IEEE.
47
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 49

Kacperczyk, M. and E. S. Pagnotta (2019). Chasing private information. The Review of Financial
Studies 32(12), 4997–5047.
Kaniel, R. and H. Liu (2006). So what orders do informed traders use?
The Journal of Busi-
ness 79(4), 1867–1913.
Keogh, E. and C. A. Ratanamahatana (2005). Exact indexing of dynamic time warping. Knowledge
and Information Systems 7(3), 358–386.
Kurbalija, V., M. Radovanovi´c, Z. Geler, and M. Ivanovi´c (2014). The influence of global constraints
on similarity measures for time-series databases. Knowledge-Based Systems 56, 49–67.
Lee, E. J., K. S. Eom, and K. S. Park (2013).
Microstructure-based manipulation: Strategic
behavior and performance of spoofing traders. Journal of Financial Markets 16(2), 227–252.
Leland, H. E. (1992).
Insider trading: Should it be prohibited?
Journal of Political Econ-
omy 100(4), 859–887.
Lemire, D. (2009). Faster retrieval with a two-pass dynamic-time-warping lower bound. Pattern
Recognition 42(9), 2169–2180.
Lim, M. and R. Coggins (2005). The immediate price impact of trades on the australian stock
exchange. Quantitative Finance 5(4), 365–377.
Liu, F. T., K. M. Ting, and Z.-H. Zhou (2012). Isolation-based anomaly detection. ACM Transac-
tions on Knowledge Discovery from Data (TKDD) 6(1), 1–39.
Manove, M. (1989).
The harm from insider trading and informed speculation.
The Quarterly
Journal of Economics 104(4), 823–845.
Meulbroek, L. K. (1992).
An empirical analysis of illegal insider trading.
The Journal of Fi-
nance 47(5), 1661–1699.
Ngai, E. W., Y. Hu, Y. H. Wong, Y. Chen, and X. Sun (2011). The application of data mining
techniques in financial fraud detection: A classification framework and an academic review of
literature. Decision Support Systems 50(3), 559–569.
Olmo, J., K. Pilbeam, and W. Pouliot (2011). Detecting the presence of insider trading via struc-
tural break tests. Journal of Banking & Finance 35(11), 2820–2828.
Park, Y. S. and J. Lee (2010).
Detecting insider trading: The theory and validation in korea
exchange. Journal of Banking & Finance 34(9), 2110–2120.
48
Electronic copy available at: https://ssrn.com/abstract=3722391


## Page 50

Patton, A. J. and K. Sheppard (2009).
Optimal combinations of realised volatility estimators.
International Journal of Forecasting 25(2), 218–238.
Pedregosa, F., G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Pret-
tenhofer, R. Weiss, V. Dubourg, et al. (2011). Scikit-learn: Machine learning in python. Journal
of Machine Learning Research 12(85), 2825–2830.
Pickands, J. (1975). Statistical inference using extreme order statistics. The Annals of Statis-
tics 3(1), 119–131.
Putni¸nˇs, T. J. (2012).
Market manipulation: A survey.
Journal of Economic Surveys 26(5),
952–967.
Rakthanmanon, T., B. Campana, A. Mueen, G. Batista, B. Westover, Q. Zhu, J. Zakaria, and
E. Keogh (2013). Addressing big data time series: Mining trillions of time series subsequences un-
der dynamic time warping. ACM Transactions on Knowledge Discovery from Data (TKDD) 7(3),
1–31.
Sakoe, H. and S. Chiba (1978). Dynamic programming algorithm optimization for spoken word
recognition. IEEE Transactions on Acoustics, Speech, and Signal Processing 26(1), 43–49.
Sch¨olkopf, B., J. C. Platt, J. Shawe-Taylor, A. J. Smola, and R. C. Williamson (2001). Estimating
the support of a high-dimensional distribution. Neural Computation 13(7), 1443–1471.
Shkilko, A. (2019). Insider trading under the microscope. Manuscript, Wilfrid Laurier University.
Shokoohi-Yekta, M., B. Hu, H. Jin, J. Wang, and E. Keogh (2017). Generalizing dtw to the multi-
dimensional case requires an adaptive approach. Data Mining and Knowledge Discovery 31(1),
1–31.
Silva, D. F., R. Giusti, E. Keogh, and G. E. Batista (2018). Speeding up similarity search un-
der dynamic time warping by pruning unpromising alignments. Data Mining and Knowledge
Discovery 32(4), 988–1016.
Spathis, C., M. Doumpos, and C. Zopounidis (2002). Detecting falsified financial statements: a
comparative study using multicriteria analysis and multivariate statistical techniques. European
Accounting Review 11(3), 509–535.
49
Electronic copy available at: https://ssrn.com/abstract=3722391


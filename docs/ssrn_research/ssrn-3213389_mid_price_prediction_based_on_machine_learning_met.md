# Mid-price Prediction Based on Machine Learning Methods with

- **Source File**: `ssrn-3213389.pdf`
- **Total Pages**: 40
- **SSRN ID**: `ssrn-3213389`

---

## Page 1

 Electronic copy available at: https://ssrn.com/abstract=3213389 
Mid-price Prediction Based on Machine Learning Methods with
Technical and Quantitative Indicators
Adamantios Ntakarisa,∗, Juho Kanniainenb, Moncef Gabbouja, Alexandros Iosiﬁdisc
aLaboratory of Signal Processing, Tampere University of Technology, Korkeakoulunkatu 1, FI-33720, Tampere, Finland
bLaboratory of Industrial and Information Management, Tampere University of Technology, Korkeakoulunkatu 8,
FI-33101, Tampere, Finland
cDepartment of Engineering, Electrical and Computer Engineering, Aarhus University, Finlandsgade 22, Hangøvej 2,
Denmark
Abstract
Stock price prediction is a challenging task, but machine learning methods have recently been used
successfully for this purpose. In this paper, we extract over 270 hand-crafted features (factors) inspired
by technical and quantitative analysis and tested their validity on short-term mid-price movement
prediction. We focus on a wrapper feature selection method using entropy, least-mean squares, and
linear discriminant analysis. We also build a quantitative feature based on adaptive logistic regression
for online learning, which is constantly selected ﬁrst among the majority of the proposed feature selection
methods. This study examines the best combination of features using high frequency limit order book
data from Nasdaq Nordic. Our results suggest that sorting methods and classiﬁers can be used in such a
way that one can reach the best performance with a combination of only very few informative features.
This paper opens avenues for developing more advanced features combined with more sophisticated
feature selection methods. It also provides helpful insight to market makers and traders in general by
providing useful results that can be used to gain an information edge in trading.
Keywords:
high-frequency trading, mid-price, machine learning, technical analysis, quantitative
analysis
1. Introduction
The problem under consideration in this paper is the prediction of a stock’s mid-price during high-
frequency ﬁnancial trading. At a given time instance, the mid-price of a stock is deﬁned as the average
of the best ask and bid prices. We consider the mid-price as vital information for market makers who
continuously balance inventories as well as for traders who need to be able to predict market movements
in the correct direction to make money. Moreover, the mid-price facilitates the process of monitoring
the markets’ stability (i.e. spooﬁng identiﬁcation).
Over the past few years, several methods, such as those described in Sirignano (2016), Gould et al.
(2013), Dash & Dash (2016) Tsantekidis et al. (2017b), Passalis et al. (2017), Thanh et al. (2017), and
Tsantekidis et al. (2017a), have been proposed for analyzing stock market data. All these methods follow
the standard classiﬁcation pipeline formed by two processing steps. Given a time instance during the
trading process, the state of the market is described based on a (usually short) time window preceding
the current instance. A set of hand-crafted features is selected to describe the dynamics of the market,
leading to a vector representation. Based on such a representation, a classiﬁer is then employed to
predict the state of the market at a time instance within a prediction horizon, as illustrated in Fig.1.
∗Corresponding author
Email address: adamantios.ntakaris@tut.fi (Adamantios Ntakaris)
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 2

 Electronic copy available at: https://ssrn.com/abstract=3213389 
Figure 1: The concept of mid-price prediction can be described as follows: at a given time instance t, the state of the stock
is encoded in a vector-based representation calculated using a multi-dimensional time series information from a short-term
time window of length T. Given this representation, the direction of the mid-price is predicted at a horizon of ∆t.
The current literature in this area mainly focuses on the selection of appropriate classiﬁcation
schemes, while less attention has been paid to the selection of a good set of features to describe the dy-
namics of the market. In fact, there is no generally agreed upon good set of features for high-frequency
stock data analysis. The use of diﬀerent hand-crafted features leads to encoding diﬀerent properties
of the ﬁnancial time-series, and excluding some of these features can result in failing to exploit the
relevant information. The deﬁnition of a good set of features is directly connected to the performance
of the subsequent analysis, since any discarded information at this stage cannot be recovered later by
the classiﬁer.
One of the most widely followed approaches used to address this problem is using feature selection
methods (Miao & Niu, 2016), (Chandrashekar & Sahin, 2014), which can be performed in a wrapper
fashion using various types of criteria for feature ranking. While the use of transformation-based dimen-
sionality reduction techniques such as principal component analysis or linear discriminant analysis can
lead to a similar processing pipeline, in this paper, we are interested in deﬁning the set of features that
convey most of the information in the data. The use of feature selection using unsupervised criteria,
and in particular, the maximum entropy criterion, has been used in Battiti (1994) and Liu et al. (2009).
The motivation behind this approach is the fact that as the entropy of a feature increases (when it
is calculated in a set of data), the data variance and, thus, the information it encodes, also increases.
However, the combination of many high-entropy features in a vector-based representation does not nec-
essarily lead to good classiﬁcation performance. This is because diﬀerent dimensions of the adopted
data representation need to encode diﬀerent information.
In this paper, we provide an extensive analysis of various hand-crafted features (273 in total) for
mid-price movement prediction. We base our analysis on a wrapped-based feature selection method
(Kohavi & John, 1997) that exploits unsupervised and supervised criteria for feature ranking. More
speciﬁcally, we use maximum entropy (Battiti, 1994), Liu et al. (2009), maximum class discrimination
based on linear discriminant analysis (LDA) (Song et al., 2010), and regression-based classiﬁcation
2
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 3

 Electronic copy available at: https://ssrn.com/abstract=3213389 
(Chen, 2011). These diﬀerent realizations of the feature selection method are applied to a wide pool
of hand-crafted features. The list of hand-crafted features used in our study is selected to cover both
basic and advanced features from the two main trading schools, which means those focusing on technical
and quantitative analyses. Technical analysis is based on the fact that price prediction can be achieved
by monitoring price and volume charts, while quantitative analysis focuses on statistical models and
parameter estimation.
For the technical indicators, we calculate basic and advanced features accompanied by digital ﬁlters,
while for the quantitative indicators, we primarily focus on time series analysis and online machine
learning. We provide the full feature list and description and use it as input in twelve feature selection
models (each corresponding to a diﬀerent criterion and classiﬁer combination) for our classiﬁcation task.
We not only present the best subset combination of these two types of features but also make a clear
comparison of the two trading styles of feature tanks in terms of F1 performance (i.e. F1 score is a
test to measure performance and is calculated as the harmonic mean of precision and recall). To the
best of our knowledge this is the ﬁrst study to deﬁne which types of information needs to be used for
high-frequency time series description and classiﬁcation.
The remainder of the paper is organized as follows. We provide a comprehensive literature review
in Section 2. The problem statement and data description are provided in Section 3. The list of hand-
crafted features follows in Section 4. In Section 5, we describe the various realizations of the wrapper
method adopted in our analysis, while Section 6 provides empirical results, and Section 7 concludes the
paper. A detailed description of all features used in our experiments, as well as all ranking lists for each
method, are provided in the Appendix section.
2. Related Literature
The rise of algorithmic trading, a type of trading requiring the use of computers under speciﬁc rules
that can rapidly perform accurate calculations, suggests signal and statistical analyses. Several tools
are based on these two types of analysis that a machine learning (ML) trader can utilize to select the
best trade. However, which indicator or indicators (i.e. features) should be considered for a ML trader
to secure a proﬁtable move?
Do historical and present prices contain all the relevant information?
Finding answers to these questions is challenging due to the use of technical and quantitative analysis.
The former category suggests that there is hidden information and patterns that can be extracted from
historical data, whereas the latter suggests that statistical models and probabilities can provide relevant
information to an ML trader.
Technical analysis (Murphy, 1999) has traditionally received less academic scrutiny than quantitative
analysis. Nevertheless, several studies employ technical indicators as the main mechanism for signal
analysis and price prediction. In the sphere of HFT, Scholtus & van Dijk (2012) utilize seven trading
rule families as a measure of the impact of trading speed, while Kablan & Ng (2010) use fuzzy momentum
analysis based on technical indicators for high speed trading. Grammatical evolution (Gabrielsson et al.,
2014) is used in the E- mini S&P 500 index futures market along with technical indicators for entry
and exit trading exploration. Lo et al. (2000) provide an extensive investigation of charting analysis of
nonparametric kernel regression for Nasdaq stocks via an automated strategy. Dash & Dash (2016) use
a decision support system based on artiﬁcial neural networks (ANN) where six basic technical indicators
are used as input features for signal generation. An adaptive neuro fuzzy inference system (ANFIS)
is used by Kablan (2009) for the FOREX market where technical indicators are utilized to benchmark
ANFIS performance. Technical indicators are the basis for works by Teixeira & de Oliveira (2010),
Kwon & Moon (2007), Brasileiro et al. (2013), and Rodriguez-Gonzalez et al. (2011) for passive trading
strategies (i.e. buy-and-hold) and stop-loss/stop-gain strategies. A list of ten technical indicators are
utilized in Patel et al. (2015) as input features for several ML algorithms (i.e. ANN, SVM, random
forest, and Naive Bayes) to predict stock trends. The interested reader can also ﬁnd the implementation
of ML methods with technical indicators in Wysocki & Lawrynczuk (2010), Wen et al. (2010), Wysocki
& Lawrynczuk (2010), Oriani & Coelho (2013), de Oliveira et al. (2013), Dempster et al. (2001), and
Khaidem et al. (2016).
Technical indicators are also used by Baetje & Menkhoﬀ(2016) for equity
3
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 4

 Electronic copy available at: https://ssrn.com/abstract=3213389 
premium prediction in the US market, where they have been proved to be eﬃcient in the out-of-sample
period (1966 - 2014). For the German bond market, Batchelor & Kwan (2007) extend the judgemental
bootstrapping domain for the technical analysts’ case. The authors prove that technical analysts can
be as proﬁtable as the statistical models of experts, by using only a subset of technical indicators.
However, there is also quantitative analysis, which involves ML traders using complex mathematics
and statistics as indicators when making trading decisions. Quantitative ﬁnance is a broad ﬁeld that
varies from topics like portfolio optimization (Markowitz, 1952), (Markowitz, 1968), (Chan et al., 1999),
(Perold, 1984), (Bank & Baum, 2004), (Inuiguchi & Tanino, 2000) and asset pricing (French, 2003),
(Sharpe, 1964), (Lintner, 1965), (Mossin, 1966), (Ross, 1977), (Jensen et al., 1972), (Fama, 1968) risk
management (Hampton, 1982), (Diebold et al., 1999), (Dolde, 1993), (Smith et al., 1989), and time
series analysis (Box et al., 2015), (Taylor, 2008), (Bollerslev, 1987). In this work, we focus on time
series analysis and use ideas from ﬁnancial quantitative time series analysis that have been adjusted
to ML. For example, Shen et al. (2012) use SVMs and decision trees via correlation analysis for stock
market prediction. Another aspect of quantitative analysis is building trading strategies such as mean-
reversion (Poterba & Summers, 1988). A simplistic example of this trading strategy is when a ML
trader calculates Bollinger bands to spot trading signals and test a hypothesis. Furthermore, a ﬁnancial
time series is used for entry and exit signal exploration generated by Bollinger bands as described in
Lubnau & Todorova (2015). A time series analysis should also be tested for cointegration as suggested
by Engle & Granger (1987a). An additional aspect of quantitative analysis is the calculation of order
book imbalance for order imbalance strategies. This idea is used as a feature in a deep neural network
by Sirignano (2016).
In the present work, we focus on extracted hand-crafted features based on technical and quantitative
analysis. We show that a combination of features derived from these groups is able to improve forecasting
ability. A combined method is employed by Fang & Xu (2003) for asset returns predicatibility based on
technical indicators and time series models. To the best of our knowledge this is the ﬁrst attempt at a
comparison between these trading schools using several feature selection methods in a wrapper fashion
in the HFT literature.
3. Problem Statement
HF-type trading requires the constant analysis of market dynamics. One way to formulate these dy-
namics is constructing a limit order book (LOB), as illustrated in Table 2. LOB is the cumulative order
ﬂow representing valid limit orders that are not executed nor cancelled, which are listed in the so-called
message list, as illustrated in Table 1.
LOBs are multi-dimensional signals described by stochastic
processes, and their dynamics are described as c`adl`ag functions (Gould et al., 2013). Functions are
formulated for a speciﬁc limit order (i.e. an order with speciﬁc characteristics in terms of price and
volume at a speciﬁc time t), as: order = (t, Pricet, V olumet) that becomes active at time t holds that:
order ∈L(t), order /∈limorder′↑orderxL(order′).
Timestamp
Id
Price
Quantity
Event
Side
1275377039033
1372349
341100
300
Submission
Bid
1275377039033
1372349
341100
300
Cancellation
Bid
1275377039037
1370659
343700
100
Submission
Ask
1275377039037
1370659
343700
100
Cancellation
Ask
1275377039037
1372352
341700
150
Submission
Bid
1275377039037
1372352
341700
150
Cancellation
Bid
Table 1: Message list example. A sample from Wartsila Oyj on 01 June 2010.
Depending on how the LOB is constructed, we treat the new information according to event arrivals.
The objective of our work is to predict the direction (i.e. up, down, and stationary condition) of the
mid-price (i.e. (pa + pb)/2, where pa is the ask price and pb is the bid price at the ﬁrst level of LOB).
The goal is to utilize informative features based on the order ﬂow (i.e. message list or message book
[MB]) and LOB, which will help an ML trader improve the accuracy of mid-price movement prediction.
4
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 5

 Electronic copy available at: https://ssrn.com/abstract=3213389 
Level 1
...
Ask
Bid
Timestamp
Price
Quantity
Price
Quantity
1127537703903
343600
100
342300
485
...
1275377039033
343600
100
342300
485
...
1275377039037
343600
200
342300
485
...
1275377039037
343600
200
342300
485
...
1275377039037
343600
200
342300
485
...
1275377039037
343600
200
342300
485
...
1275377039037
343600
200
342300
485
...
1275377039037
343600
200
342300
485
...
Table 2: Order book example. A sample from Wartsila Oyj on 01 June 2010.
4. Feature Pool
LOB and MB are the sources that we utilize for feature extraction. We provide the complete list of the
features that have been explored in the literature for technical and quantitative trading in Table 3. The
motivation for choosing the suggested list of features is based on an examination of all the basic and
advanced features from technical analysis and comparisons with advanced statistical models, such as
adaptive logistic regression for online learning. The present research has identiﬁed a gap in the existing
literature concerning the performance of technical indicators and comparisons with quantitative models.
The present work sets the groundwork for every future work in this direction since it provides insight
into the features that are likely to achieve a high rank on the ordering list in terms of predictability
power. To this end, we divide our feature set into three main groups. The ﬁrst group of features is
extracted according to Kercheval & Zhang (2015) and Ntakaris et al. (2017). This group of features
aims to capture the dynamics of LOB. This is possible if we consider the actual raw LOB data and
relative intensities of diﬀerent look-back periods of the trade types (i.e. order placement, execution, and
cancellation). The second group of features is based on technical analysis. The suggested list describes
most of the existing technical indicators (basic and advanced). Technical indicators might help traders
spot hidden trends and patterns in their time series. The third group is based on quantitative analysis,
which is mainly based on statistical models; it can provide statistics that are hidden in the data. This can
be veriﬁed by the ranking process, where the advanced online feature (i.e. adaptive logistic regression)
is placed ﬁrst in most of the feature selection lists (i.e. four out of ﬁve feature lists). The suggested
features are fully described in Appendix A.
5. Wrapper Method of Feature Selection
Feature selection is an area which focuses on applications with multidimensional datasets. An ML trader
performs feature selection for three primary reasons: to reduce computational complexity, to improve
performance, and to gain a better understanding of the underlying process. Feature selection, as a
pre-processing method, can enhance classiﬁcation power by adding features that contain information
relevant to the task at hand.
There are two metaheuristic feature selection methods: the wrapper
method and the ﬁlter (i.e. transformation-based) method. We choose to perform classiﬁcation based
on the wrapper method since it considers the relationship among the features while the ﬁlter methods
do not.
Our wrapper approach consists of ﬁve diﬀerent feature subset selection criteria, two linear classiﬁers,
and one non-linear classiﬁer for evaluation (see Algorithm 1 for a general description), including entropy,
least-mean-square (LMS) based on L2-norm and a statistical bias measure, and linear discriminant
analysis (LDA) based on the ratio of the within-class scatter matrix and between-class scatter matrix,
as well as a statistical bias measure. For non-linear classiﬁers, we use a multilayer perceptron based on
extreme learning machines (i.e. radial basis function network [RBFN]) as described in Ntakaris et al.
(2017). Then we measure classiﬁcation performance according to accuracy, precision, recall, and the F1
5
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 6

 Electronic copy available at: https://ssrn.com/abstract=3213389 
Feature Sets
Description
First group:
Basic
n levels of LOB Data
Time-Insensitive
Spread & Mid-Price
Price Diﬀerences
Price & Volume Means
Accumulated Diﬀerences
Time-Sensitive
Price & Volume Derivation
Average Intensity per Type
Relative Intensity Comparison
Limit Activity Acceleration
Second group:
Technical Analysis
Accumulation Distribution Line
Awesome Oscillator
Accelerator Oscillator
Average Directional Index
Average Directional Movement Index Rating
Displaced Moving Average based on Williams Alligator Indicator
Absolute Price Oscillator
Aroon Indicator
Aroon Oscillator
Average True Range
Bollinger Bands
Ichimoku Clouds
Chande Momentum Oscillator
Chaikin Oscillator
Chandelier Exit
Center of Gravity Oscillator
Donchian Channels
Double Exponential Moving Average
Detrended Price Oscillator
Heikin-Ashi
Highest High and Lowest Low
Hull MA
Internal Bar Strength
Keltner Channels
Moving Average Convergence/Divergence Oscillator
Median Price
Momentum
Variable Moving Average
Normalized Average True Range
Percentage Price Oscillator
Rate of Change
Relative Strength Index
Parabolic Stop and Reverse
Standard Deviation
Stochastic Relative Strength Index
T3-Triple Exponential Moving Average
Triple Exponential Moving Average
Triangular Moving Average
True Strength Index
Ultimate Oscillator
Weighted Close
Williams %R
Zero-Lag Exponential Moving Average
Fractals
Linear Regression Line
Digital Filtering: Rational Transfer Function
Digital Filtering: Savitzky-Golay Filter
Digital Filtering: Zero-Phase Filter
Remove Oﬀset and Detrend
Beta-like Calculation
Third group:
Quantitative Analysis
Autocorrelation
Partial Correlation
Cointegration based on Engle-Granger test
Order Book Imbalance
Logistic Regression for Online Learning
Table 3: Feature list for the three groups (description and calculations in Appendix A).
6
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 7

 Electronic copy available at: https://ssrn.com/abstract=3213389 
score for every possible combination of the hand-crafted features by utilizing LMS, LDA, and RBFN.
Our choice to apply these linear and non-linear classiﬁers is informed by the amount of data in our
dataset (details will be provided in the following section).
Algorithm 1 Wrapper-Based Feature Selection
1: procedure lopt = Feature Select(X, labels, criterion)
2:
l = [1 : D]
3:
lopt = [ ]
4:
Xopt = [ ], [D, N] = size(X)
5:
for d = 1 : D do
6:
crit list = [ ]
7:
for i = 1 : D −d + 1 do
8:
curr X = [Xopt; X(i; :)]
9:
crit list[i] = crit(curr X)
10:
end for
11:
[best d, best crit] = opt(crit list)
12:
lopt[d] = best d
13:
l[best d] = [ ]
14:
Xopt = [Xopt; X(best d; :)]
15:
X(best d, :) = [ ]
16:
end for
17: end procedure
5.1. Feature Sorting
We convert sample entropy, LMS, and LDA (for the latter two methods we use two diﬀerent criteria for
feature evaluation) into feature selection methods.
5.1.1. Feature Sorting with Entropy
We employ entropy (Richman & Moorman, 2000), a measure of signal complexity where the signal is
the time series of the multidimensional two-mode tensor with dimensions Rp×n, and where p is the
number of features and n number of samples, as a measure of feature relevance. We calculate the bits
of every feature in the feature set in an iterative manner and report the order. We measure the entropy
as follows: H(X) = −
pP
i=1
p(xi) log p(xi), where p(xi) is the probability of the frequency per feature for
the given data samples.
5.1.2. Feature Sorting with Least-Mean-Square
We perform feature selection based on the least-mean square classiﬁcation rate (LMS1) and L2-norm
(LMS2). LMS is a ﬁtting method which aims to produce an approximation that minimizes the sum
of squared diﬀerences between given data and predicted values. We use this approach to evaluate the
relevance of our hand-crafted features. A hand-crafted feature evaluation is performed sequentially via
LMS. More speciﬁcally, each of the features is evaluated based on the classiﬁcation rate, the L2-norm of
the predicted labels, and the ground truth. The evaluation process is performed as follows: HW = T,
where H ∈Rpi×n is the input data with feature dimension pi where it is calculated incrementally for
the number of training samples n, W ∈Rpi×#cl are the weighted coeﬃcients for the number of features
pi of the number(#) of classes (i.e. up, down, and stationary labelling), and T ∈R#cl×n represents the
target labels of the training set. The weight coeﬃcient matrix W is estimated via the following formula:
W = H†T, where H† is the Moore-Penrose pseudoinverse matrix.
7
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 8

 Electronic copy available at: https://ssrn.com/abstract=3213389 
5.1.3. Feature Sorting with Linear Discriminant Analysis
Linear discriminant analysis (LDA) can be used for classiﬁcation and dimensionality reduction. However,
instead of performing these two tasks, we convert LDA into a feature selection algorithm. We measure
feature selection performance based on two metrics.
One is the classiﬁcation rate (LDA1) and the
other is based on the error term (LDA2), which we deﬁne as the ratio of the within-class scatter
matrix and the between-class scatter matrix.
The main objective of LDA is ﬁnding the projection
matrix W ∈Rm×#cl−1, where m is the sample dimension, and #cl is the number of classes, such
that Y = W T X maximizes the class separation. For the given sample set X = X1 ∪X2 ∪... ∪X#cl,
where Xk = {xk
1, ..., xk
ℓk}k=1,...,#cl is the class-speciﬁc data subsample, we try to ﬁnd W that maximizes
Fisher’s ratio J(W) =
trace

WT SBW

trace

WT SW W
, where SB =
#cl
P
i=1
Ni(µi −µ)(µi −µ)T and SW =
CP
i=1
dP
x∈Xi
(x −
µi)(x−µi)T are the between-class and within-class scatter matrices, respectively, with µi =
1
ℓk
P
k∈#cl
Xk
and µ =
1
m
P
k∈#cl
ℓkXk. In a similar fashion, we perform calculations for the projected samples y with
eµi =
1
ℓk
P
k∈#cl
Yk and eµ =
1
m
P
k∈#cl
ℓkYk, while the scatter matrices (i.e. within and between scatter
matrices, respectively) are g
SW =
#cl
P
i=1
P
k∈#cl
(y −˜µi)(y −˜µi)T and f
SB =
#cl
P
i=1
ℓk( eµi −eµ)( eµi −eµ)T . The
above calculations constitute the basis for the two metrics that we use to evaluate the hand-crafted
features incrementally. The two evaluation metrics are based on the classiﬁcation rate and the ratio of
the within-class and between-class scatter matrices of the projected space Y .
5.2. Classiﬁcation for Feature Selection
We performed feature sorting based on entropy, LMS (using two metrics), and LDA (using two metrics).
This leads to ﬁve feature selection variants, each leading to a diﬀerent ranking of the various features.
These feature lists are the basis for evaluating the performance of time series representations of diﬀerent
feature dimensions.
6. Results
In this section, we provide details regarding the conducted experiments. The experiments are based
on the idea of a mid-price prediction state (i.e.
up, down, and stationary) for ITCH feed data in
millisecond resolution. For the experimental protocol, we followed the setup in Ntakaris et al. (2017),
which is based on the anchored cross-validation format. According to this format, we use the ﬁrst day
as training and second day as testing for the ﬁrst fold, whereas the second fold consists of the previous
training and testing periods as a training set, and the next day is always used as a test set. Each of the
training and testing sets contains the hand-crafted feature representations for all the ﬁve stocks from
the FI-2010 dataset. Hence, we obtain a mode-three tensor of dimensions 273 × 458, 125. The ﬁrst
dimension is the number of features, whereas the second one is the number of sample events. At this
point, we must specify that the process of hand-crafted feature extraction in Section 5 is conducted in
the full length of the given information based on MB with 4,581,250 events. The motivation for taking
separate blocks of messages of ten events is the time-invariant nature of the data. To keep the ML
trader fully informed regarding MB blocks, we use features that convey this information by calculating,
among others, averages, regression, risk, and online learning feedback.
The results we present here are the mid-price predictions for the next 10th, 20th, and 30th events
(i.e. translated into MB events) or else one, two, and three next events after the current state translated
into a feature representations setup. The prediction performance of these events is measured by the
accuracy, precision, recall and F1 score, whereas we emphasize the F1 score.
We focus on the F1
score because it can only be aﬀected in one direction by skewed distributions for unbalanced classes,
8
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 9

 Electronic copy available at: https://ssrn.com/abstract=3213389 
as observed in our data. Performance metrics are calculated against the mid-price labelling calculation
of ground truth extraction. More speciﬁcally, we extract labels based on the percentage change of the
smoothed mid-price with a span window of 9, for our supervised learning methods, by calculating it
as follows: L1 = MPnext −MPcurr
MPcurr
, where MPcurr is the current mid-price, and MPnext is the next
mid-price. We threshold the percentage change identiﬁcation by a ﬁxed number γ = 0.002 and perform
z-score normalization on our dataset.
We report our results in Table 4 - Table 8 of the best feature selection list for the ﬁve sorting
lists (i.e. based on entropy, LMS1, LMS2, LDA1, and LDA2) according to the supervised linear and
non-linear classiﬁers of LMS, LDA, and RBFN. For the last classiﬁer (i.e. RBFN), we use a multilayer
perceptron based on the extreme learning machine model with a twist in the initialization process of
weights calculation based on the k-means algorithm. The full description of this method can be found
in Ntakaris et al. (2017). We provide results based on the whole feature pool (see Table 4), the ﬁrst
feature pool according to Kercheval & Zhang (2015) and Ntakaris et al. (2017) (see Table 5), based only
on technical indicators (see Table 6) and quantitative indicators (see Table 7). More speciﬁcally, for the
ﬁrst feature pool, we have 135 features, while for the second pool we have 83 features, and for the last
pool we have 55 features; in total, we have 273 features. The number of best features that used in the
above methods is diﬀerent in every case and can be monitored in Fig.2 and Fig.3.
Sorting
Classiﬁer
T
Accuracy
Precision
Recall
F1
Entropy
LMS
10
0.529 ± 0.059
0.447 ± 0.007
0.477 ± 0.013
0.440 ± 0.018
LMS1
LMS
10
0.540 ± 0.059
0.437 ± 0.007
0.456 ± 0.013
0.430 ± 0.018
LMS2
LMS
10
0.538 ± 0.052
0.447 ± 0.005
0.478 ± 0.013
0.444 ± 0.011
LDA1
LDA
10
0.616 ± 0.048
0.408 ± 0.019
0.398 ± 0.011
0.397 ± 0.015
LDA2
LDA
10
0.543 ± 0.057
0.430 ± 0.010
0.455 ± 0.017
0.429 ± 0.018
LDA1
LMS
10
0.604 ± 0.068
0.468 ± 0.035
0.431 ± 0.042
0.408 ± 0.035
LDA2
LMS
10
0.522 ± 0.026
0.441 ± 0.020
0.473 ± 0.007
0.435 ± 0.007
Entropy
RBFN
10
0.474 ± 0.046
0.420 ± 0.031
0.445 ± 0.039
0.400 ± 0.039
LMS1
RBFN
10
0.600 ± 0.045
0.436 ± 0.019
0.425 ± 0.021
0.417 ± 0.019
LMS2
RBFN
10
0.537 ± 0.016
0.442 ± 0.011
0.470 ± 0.016
0.439 ± 0.012
LDA1
RBFN
10
0.585 ± 0.061
0.443 ± 0.018
0.438 ± 0.037
0.419 ± 0.026
LDA2
RBFN
10
0.528 ± 0.029
0.438 ± 0.020
0.467 ± 0.010
0.434 ± 0.017
Entropy
LMS
20
0.503 ± 0.049
0.469 ± 0.008
0.482 ± 0.014
0.462 ± 0.017
LMS1
LMS
20
0.503 ± 0.049
0.470 ± 0.008
0.482 ± 0.014
0.462 ± 0.017
LMS2
LMS
20
0.503 ± 0.049
0.469 ± 0.008
0.481 ± 0.014
0.462 ± 0.018
LDA1
LDA
20
0.478 ± 0.060
0.400 ± 0.038
0.404 ± 0.041
0.393 ± 0.018
LDA2
LDA
20
0.505 ± 0.046
0.452 ± 0.009
0.461 ± 0.012
0.450 ± 0.012
LDA1
LMS
20
0.530 ± 0.032
0.457 ± 0.024
0.426 ± 0.048
0.401 ± 0.048
LDA2
LMS
20
0.499 ± 0.019
0.462 ± 0.019
0.476 ± 0.007
0.457 ± 0.015
Entropy
RBFN
20
0.464 ± 0.038
0.436 ± 0.033
0.448 ± 0.035
0.425 ± 0.036
LMS1
RBFN
20
0.519 ± 0.023
0.430 ± 0.016
0.417 ± 0.022
0.412 ± 0.027
LMS2
RBFN
20
0.508 ± 0.010
0.456 ± 0.015
0.466 ± 0.018
0.454 ± 0.017
LDA1
RBFN
20
0.523 ± 0.025
0.441 ± 0.024
0.429 ± 0.041
0.416 ± 0.046
LDA2
RBFN
20
0.502 ± 0.018
0.454 ± 0.019
0.465 ± 0.009
0.452 ± 0.015
Entropy
LMS
30
0.503 ± 0.042
0.475 ± 0.013
0.484 ± 0.014
0.470 ± 0.019
LMS1
LMS
30
0.503 ± 0.042
0.475 ± 0.013
0.484 ± 0.014
0.470 ± 0.019
LMS2
LMS
30
0.503 ± 0.043
0.474 ± 0.012
0.482 ± 0.014
0.461 ± 0.019
LDA1
LDA
30
0.464 ± 0.048
0.414 ± 0.025
0.420 ± 0.027
0.403 ± 0.018
LDA2
LDA
30
0.500 ± 0.043
0.457 ± 0.012
0.464 ± 0.013
0.455 ± 0.014
LDA1
LMS
30
0.489± 0.018
0.451 ± 0.030
0.429 ± 0.051
0.405 ± 0.072
LDA2
LMS
30
0.496 ± 0.016
0.476 ± 0.018
0.479 ± 0.009
0.472 ± 0.015
Entropy
RBFN
30
0.464 ± 0.035
0.446 ± 0.035
0.449 ± 0.034
0.440 ± 0.037
LMS1
RBFN
30
0.471 ± 0.018
0.425 ± 0.018
0.414 ± 0.020
0.409 ± 0.026
LMS2
RBFN
30
0.494 ± 0.014
0.464 ± 0.021
0.466 ± 0.021
0.461 ± 0.024
LDA1
RBFN
30
0.481 ± 0.022
0.438 ± 0.034
0.428 ± 0.045
0.415 ± 0.057
LDA2
RBFN
30
0.493 ± 0.017
0.465 ± 0.018
0.467 ± 0.010
0.463 ± 0.016
Table 4: F1-macro (i.e. F1-macro =
1
C
P
k∈C F1k, with C as the number of classes for the 9-fold experimental protocol)
results, based on the total feature pool, for the ﬁve sorting lists classiﬁed per LMS, LDA, and RBFN for the next T =10th,
20th, and 30th events, respectively, as the predicted horizon. The number of best features used in the above methods is
diﬀerent in every case (as seen in Fig. 3).
9
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 10

 Electronic copy available at: https://ssrn.com/abstract=3213389 
Sorting
Classiﬁer
T
Accuracy
Precision
Recall
F1
Entropy
LMS
10
0.420 ± 0.025
0.379 ± 0.011
0.397 ± 0.011
0.355 ± 0.013
LMS1
LMS
10
0.574 ± 0.055
0.402 ± 0.013
0.396 ± 0.018
0.384 ± 0.020
LMS2
LMS
10
0.519 ± 0.015
0.400 ± 0.009
0.413 ± 0.009
0.396 ± 0.010
LDA1
LDA
10
0.561 ± 0.090
0.389 ± 0.018
0.382 ± 0.016
0.363 ± 0.030
LDA2
LDA
10
0.507 ± 0.041
0.373 ± 0.014
0.384 ± 0.017
0.362 ± 0.019
Entropy
LMS
20
0.386 ± 0.018
0.386 ± 0.015
0.397 ± 0.015
0.363 ± 0.016
LMS1
LMS
20
0.527 ± 0.027
0.411 ± 0.013
0.389 ± 0.015
0.375 ± 0.029
LMS2
LMS
20
0.462 ± 0.013
0.405 ± 0.013
0.410 ± 0.009
0.400 ± 0.012
LDA1
LDA
20
0.529 ± 0.031
0.406 ± 0.017
0.381 ± 0.011
0.360 ± 0.024
LDA2
LDA
20
0.461 ± 0.036
0.378 ± 0.016
0.380 ± 0.016
0.368 ± 0.021
Entropy
LMS
30
0.391 ± 0.016
0.395 ± 0.018
0.401 ± 0.015
0.380 ± 0.017
LMS1
LMS
30
0.459 ± 0.025
0.405 ± 0.017
0.388 ± 0.020
0.366 ± 0.040
LMS2
LMS
30
0.432 ± 0.009
0.407 ± 0.015
0.409 ± 0.013
0.401 ± 0.016
LDA1
LDA
30
0.447 ± 0.041
0.391 ± 0.018
0.377 ± 0.017
0.352 ± 0.037
LDA2
LDA
30
0.418 ± 0.028
0.373 ± 0.016
0.375 ± 0.015
0.361 ± 0.018
Table 5: F1-macro (i.e. F1-macro =
1
C
P
k∈C F1k, with C as the number of classes for the 9-fold experimental protocol)
results, based only on the hand-crafted features from Ntakaris et al. (2017), for the ﬁve sorting lists classiﬁed based on
LMS, LDA, and RBFN for the next T =10th, 20th, and 30th events, respectively, as the predicted horizon. The number
of best features used in the above methods is diﬀerent in every case (as seen in Fig. 3).
Sorting
Classiﬁer
T
Accuracy
Precision
Recall
F1
Entropy
LMS
10
0.456 ± 0.038
0.372 ± 0.021
0.380 ± 0.014
0.353 ± 0.020
LMS1
LMS
10
0.497 ± 0.066
0.371 ± 0.017
0.377 ± 0.021
0.354 ± 0.024
LMS2
LMS
10
0.460 ± 0.016
0.383 ± 0.012
0.394 ± 0.009
0.365 ± 0.010
LDA1
LDA
10
0.517 ± 0.064
0.367 ± 0.015
0.371 ± 0.020
0.344 ± 0.026
LDA2
LDA
10
0.475 ± 0.023
0.371 ± 0.010
0.382 ± 0.009
0.351 ± 0.015
Entropy
LMS
20
0.430 ± 0.029
0.384 ± 0.025
0.387 ± 0.017
0.371 ± 0.023
LMS1
LMS
20
0.480 ± 0.033
0.384 ± 0.023
0.381 ± 0.021
0.364 ± 0.037
LMS2
LMS
20
0.452 ± 0.011
0.400 ± 0.018
0.402 ± 0.011
0.391 ± 0.015
LDA1
LDA
20
0.483 ± 0.034
0.379 ± 0.022
0.377 ± 0.020
0.355 ± 0.038
LDA2
LDA
20
0.453 ± 0.014
0.382 ± 0.015
0.387 ± 0.009
0.369 ± 0.016
Entropy
LMS
30
0.423 ± 0.030
0.394 ± 0.028
0.394 ± 0.020
0.385 ± 0.027
LMS1
LMS
30
0.450 ± 0.018
0.395 ± 0.028
0.393 ± 0.027
0.379 ± 0.050
LMS2
LMS
30
0.446 ± 0.013
0.409 ± 0.020
0.408 ± 0.013
0.403 ± 0.019
LDA1
LDA
30
0.430 ± 0.041
0.384 ± 0.027
0.382 ± 0.027
0.353 ± 0.053
LDA2
LDA
30
0.433 ± 0.021
0.397 ± 0.017
0.396 ± 0.016
0.386 ± 0.026
Table 6: F1-macro (i.e. F1-macro =
1
C
P
k∈C F1k, with C as the number of classes for the 9-fold experimental protocol)
results, based only on technical features, for the ﬁve sorting lists classiﬁed based on LMS,LDA, and RBFN for the next
T =10th, 20th, and 30th events, respectively, as the predicted horizon. The number of best features used in the above
methods is diﬀerent in every case (as seen in Fig. 3).
Sorting
Classiﬁer
T
Accuracy
Precision
Recall
F1
Entropy
LMS
10
0.393 ± 0.109
0.399 ± 0.047
0.419 ± 0.047
0.340 ± 0.064
LMS1
LMS
10
0.665 ± 0.033
0.468 ± 0.043
0.388 ± 0.016
0.366 ± 0.016
LMS2
LMS
10
0.571 ± 0.071
0.470 ± 0.053
0.418 ± 0.032
0.384 ± 0.020
LDA1
LMS
10
0.611 ± 0.088
0.422 ± 0.039
0.390 ± 0.020
0.370 ± 0.024
LDA2
LMS
10
0.380 ± 0.101
0.401 ± 0.024
0.428 ± 0.027
0.339 ± 0.063
Entropy
LMS
20
0.400 ± 0.074
0.408 ± 0.048
0.422 ± 0.048
0.372 ± 0.061
LMS1
LMS
20
0.553 ± 0.029
0.429 ± 0.037
0.373 ± 0.016
0.335 ± 0.025
LMS2
LMS
20
0.483 ± 0.017
0.447 ± 0.022
0.457 ± 0.025
0.435 ± 0.029
LDA1
LMS
20
0.513 ± 0.072
0.402 ± 0.032
0.379 ± 0.026
0.347 ± 0.040
LDA2
LMS
20
0.424 ± 0.073
0.431 ± 0.026
0.444 ± 0.023
0.340 ± 0.053
Entropy
LMS
30
0.410 ± 0.062
0.416 ± 0.051
0.423 ± 0.048
0.391 ± 0.060
LMS1
LMS
30
0.478 ± 0.022
0.407 ± 0.038
0.370 ± 0.019
0.320 ± 0.036
LMS2
LMS
30
0.481 ± 0.012
0.457 ± 0.026
0.460 ± 0.024
0.449 ± 0.034
LDA1
LMS
30
0.464 ± 0.037
0.394 ± 0.030
0.378 ± 0.027
0.338 ± 0.049
LDA2
LMS
30
0.425 ± 0.063
0.437 ± 0.029
0.443 ± 0.022
0.406 ± 0.055
Table 7: F1-macro (i.e. F1-macro =
1
C
P
k∈C F1k, with C as the number of classes for the 9-fold experimental protocol)
results, based only on quantitative features, for the ﬁve sorting lists classiﬁed based on LMS,LDA, and RBFN for the next
T =10th, 20th, and 30th events, respectively, as the predicted horizon. The number of best features used in the above
methods is diﬀerent in every case (as seen in Fig. 3).
10
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 11

 Electronic copy available at: https://ssrn.com/abstract=3213389 
Sorting
Classiﬁer
5
50
100
200
273
Entropy
LMS
0.319 ± 0.008
0.363 ± 0.027
0.414 ± 0.020
0.425 ± 0.025
0.440 ± 0.018
LMS1
LMS
0.377 ± 0.008
0.374 ± 0.036
0.393 ± 0.047
0.419 ± 0.036
0.440 ± 0.018
LMS2
LMS
0.402 ± 0.015
0.443 ± 0.014
0.441 ± 0.018
0.440 ± 0.018
0.440 ± 0.018
LDA1
LMS
0.373 ± 0.013
0.380 ± 0.017
0.395 ± 0.016
0.315 ± 0.018
0.289 ± 0.025
LDA2
LMS
0.412 ± 0.011
0.420 ± 0.017
0.420 ± 0.019
0.289 ± 0.013
0.309 ± 0.027
LDA1
LMS
0.370 ± 0.011
0.372 ± 0.032
0.387 ± 0.041
0.440 ± 0.017
0.440 ± 0.018
LDA2
LMS
0.421 ± 0.010
0.435 ± 0.011
0.435 ± 0.014
0.440 ± 0.017
0.441 ± 0.018
Entropy
RBFN
0.316 ± 0.010
0.363 ± 0.020
0.413 ± 0.016
0.430 ± 0.016
0.441 ± 0.016
LMS1
RBFN
0.387 ± 0.018
0.402 ± 0.022
0.421 ± 0.017
0.429 ± 0.017
0.441 ± 0.016
LMS2
RBFN
0.403 ± 0.015
0.444 ± 0.012
0.439 ± 0.013
0.439 ± 0.019
0.442 ± 0.016
LDA1
RBFN
0.371 ± 0.011
0.387 ± 0.021
0.411 ± 0.013
0.440 ± 0.016
0.441 ± 0.016
LDA2
RBFN
0.416 ± 0.011
0.434 ± 0.015
0.436 ± 0.015
0.436 ± 0.016
0.442 ± 0.016
Table 8: F1 results based on diﬀerent numbers of best features for the ﬁve criteria of the wrapper-based feature selection
methods.
Figure 2: Bar plots with variance present the average (i.e. average F1 performance for the 9-fold protocol for all the
features) F1 score of the 12 diﬀerent models for the cases of 5, 50, 100, 200, and 273 number of best features. The order
of the models from the left to the right column is (1) feature list sorted based on entropy and classiﬁed based on LMS, (2)
feature list sorted based on LMS1 and classiﬁed based on LMS, (3) feature list sorted based on LMS2 and classiﬁed based
on LMS, (4) feature list sorted based on LDA1 and classiﬁed based on LDA, (5) feature list sorted based on LDA2 and
classiﬁed based on LDA, (6) feature list sorted based on LDA1 and classiﬁed based on LMS, (7) feature list sorted based
on LDA2 and classiﬁed based on LMS, (8) feature list sorted based on LDA2 and classiﬁed based on LMS, (9) feature list
sorted based on entropy and classiﬁed based on RBFN, (10) feature list sorted based on LMS2 and classiﬁed based on
RBFN, (11) feature list sorted based on LDA1 and classiﬁed based on RBFN, and (12) feature list sorted based on LDA2
and classiﬁed based on RBFN.
11
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 12

 Electronic copy available at: https://ssrn.com/abstract=3213389 
Figure 3: F1 performance per number of best features sequence for 10 events as the projected horizon, where lines represent the 5 diﬀerent sorting methods as classiﬁed
based on LMS, LDA, and RBFN.
12
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 13

 Electronic copy available at: https://ssrn.com/abstract=3213389 
There is a dual interpretation of the suggested feature lists and wrapper method results. Regarding
the feature lists, we have ﬁve diﬀerent feature sorting methods starting from entropy, to LMS1 and
LMS2 and continue to LDA1 and LDA2. More speciﬁcally, results based on the entropy sorting method
reveal that the ﬁrst 20 places are covered by features almost entirely from technical indicators (i.e. 19
out of 20 places and only one from the ﬁrst basic group), while the ﬁrst 100 best places are covered by
36 quant features, 48 technical features, and 16 from the ﬁrst basic group.
For the LMS case, we present two sorting lists where we use two diﬀerent criteria for the ﬁnal
feature selection. In the LMS1 case, the ﬁrst best 20 places covered by features are derived mainly from
quantitative analysis (11 out of 20), 7 from the ﬁrst basic group, and only 2 from the technical group.
The ﬁrst place is covered by a very advanced feature based on the logistic regression model for online
learning. For the same method, the ﬁrst 100 best places covered by 25 quant features, 18 features from
technical analysis, and the remaining 57 from the ﬁrst basic group. In the LMS2 case, the ﬁrst 20 best
places are covered by 7 features from the quant pool, 9 from the technical pool, and only 4 from the ﬁrst
basic group. LMS2 also selects the advanced feature based on the logistic regression model for online
learning ﬁrst.
The last method that we use as the basis for the feature selection process is based on LDA. In a
similar fashion, we use two diﬀerent criteria as a measure for the selection process. In the LDA1 case,
the ﬁrst 20 best places are covered by 10 quant features, 3 technical indicators, and 7 from the ﬁrst
basic group. The ﬁrst 100 best positions are covered by 19 quant features, 20 technical features, and
the remaining 61 places from the ﬁrst basic group. Again, the ﬁrst place is covered by the advanced
feature based on the logistic regression model for online learning. The last feature selection model,
LDA2, selects 6 features from the quant pool, 6 from the technical pool, and 8 from the ﬁrst basic
group. LDA2 selects for the ﬁrst best 100 places 24 quant features, 27 technical features, and 49 from
the ﬁrst basic group. To gain better insight into the feature list, we present the names of the best 10
features for each of the 5 sorting methods in Table 9.
The second interpretation of our ﬁndings is the performance of the 12 diﬀerent classiﬁers (based on
LMS, LDA, and RBFN) that we used to measure, in terms of F1 score, the predictability of the mid-
price movement. Fig.3 provides a quick overview of the F1 score performance in terms of best feature
numbers and classiﬁers. We can divide these twelve models (pairs based on the sorting and classiﬁcation
method) into three groups according to their response in terms of information ﬂow. The ﬁrst group,
where LMS2-LMS, LDA2-LMS, LMS2-RBFN, and LDA2-RBFN belong, reach their plateau very early
in the incremental process of adding less informative features. These models where able to reach their
maximum (or close to their maximum) F1 score performance with approximately 5 best features, which
means that the dimensionality of the input matrix to the classiﬁcation model is quite small. The second
group of models, Entropy-LMS, LMS1-LMS, LDA1-LMS, Entropy-RBFN, LMS1-RBFN, and LDA1-
RBFN, had a slower reaction in the process of reaching their best F1 score performance. The last group
of models, LDA1-LDA and LDA2-LDA, reached their best performance very early in the process (which
is not higher performance compared to the other models) with only ﬁve features. Interestingly, it is
right after this point that their predictability power starts to decrease.
The experiments conducted show that this quantitative analysis can provide signiﬁcant trading
information, but results are improved with respect to features also taken from the technical pool.
Features on the top of the lists come from the logistic regression model. This is the very ﬁrst time this
model is presented as a feature in the HFT sphere. This shows that more sophisticated features from
the pool of quantitative analysis will provide the ML trader with vital information regarding metrics
prediction. This area is of great interest since more advanced features and models can be applied.
7. Conclusion
In this paper, we extracted hand-crafted features inspired by technical and quantitative analysis and
tested their validity on mid-price movement prediction. We used entropy, least-mean-squares (LMS),
and linear discriminant analysis (LDA) criteria to guide feature selection methods combined with linear
and non-linear classiﬁers.
This work is the ﬁrst attempt of this extent to develop a framework in
13
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 14

 Electronic copy available at: https://ssrn.com/abstract=3213389 
Feature Sets
Description
Entropy
1
Autocorrelation
2
Donchian Channels
3
Highest High
4
Center of Gravity Oscillator
5
Heikin-Ashi
6
Linear Regr. - Regression Coeﬃc.
7
Linear Regr. - Correlation Coeﬃc.
8
T3
9
TEMA
10
TRIMA
LMS1
1
Logistic Regr. - Local Spatial Ratio
2
Best LOB Level - Bid Side Volume
3
Second Best LOB Level - Ask Volume
4
Price and Volume Derivation
5
Best LOB Level - Ask Side
6
Linear Regr. - Corr. Coeﬃc.
7
Logistic Regr. - Logistic Coeﬃc.
8
Logistic Regr. - Extended Spatial Ratio
9
Autocorrelation for Log Returns
10
Partial Autocorrelation
LMS2
1
Logistic Regression - Spatial Ratio
2
Cointegration - Boolean Vector
3
Cointegration - Test Statistics
4
Price and Volume Means
5
Average Type Intensity
6
Average Type Intensity
7
Spread & Mid-Price
8
Alligator Jaw
9
Directional Index
10
Fractals
LDA1
1
Logistic Regression - Spatial Ratio
2
Second Best LOB Level - Ask Volume
3
Price & Volume derivation
4
Spread & Mid-Price
5
Partial Autocorrelation for Log Returns
6
Linear Regression Line - Squared Corr. Coeﬃc.
7
Order Book Imbalance
8
Linear Regression - Corr. Coeﬃc.
9
Linear Regression - Regr. Coeﬃc.
10
Third Best LOB Level - Ask Volume
LDA2
1
Logistic Regression - Probability Estimation
2
Logistic Regression - Spatial Ratio
3
Bollinger Bands
4
Alligator Teeth
5
Cointegration - Test Statistics
6
Best LOB Level - Bid Side Volume
7
Cointegration - p Values
8
Price & Volume Means
9
Price & Volume derivation
10
Price diﬀerences
Table 9: List for the ﬁrst 10 best features for the 5 sorting methods
14
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 15

 Electronic copy available at: https://ssrn.com/abstract=3213389 
information edge discovery via informative features from the two main trading schools. Therefore, we
provided the description of the hand-crafted features adjusted to the HFT universe by considering each
10-message book block as a separate trading unit (i.e. trading days). We evaluated our theoretical
framework on ﬁve ITCH feed data stocks from the Nordic stock market. The dataset contained more
than 4.5 million events and was incorporated into the hand-crafted features. The results suggest that
sorting methods and classiﬁers can be combined in such a way that market makers and traders can
reach, with only very few informative features, the best performance of their algorithm. Furthermore,
the very advanced quantitative feature based on logistic regression for online learning is placed ﬁrst
among most the ﬁve sorting methods. This is a strong indication for future research on developing more
advanced features combined with more sophisticated feature selection methods.
Acknowledgment
The research leading to these results has received funding from the H2020 Project BigDataFinance
MSCA-ITN-ETN 675044 (http://bigdataﬁnance.eu), Training for Big Data in Financial Research and
Risk Management.
Appendix
A. Feature Pool
A.1. First Group of Features
This set of features is based on Kercheval & Zhang (2015) and Ntakaris et al. (2017) and is divided
into three groups: basic, time-insensitive, and time-sensitive. These are fundamental features since they
reﬂect the raw data directly without any statistical analysis or interpolation. We calculated them as
follows:
A.1.1. Basic
• u1 = {P ask
i
, V ask
i
, P bid
i
, V bid
i
}n
i=1
which represents the raw data of the 10 levels of our LOB.
A.1.2. Time-Insensitive
• u2 = {(P ask
i
−P bid
i
), (P ask
i
+ P bid
i
)/2}n
i=1
• u3 =
{P ask
n
−P ask
1
, P bid
1
−P bid
n , |P ask
i+1 −P ask
i
|, |P bid
i+1 −P bid
i
|}n
i+1
• u4 =
n
1
n
nP
i=1
P ask
i
, 1
n
nP
i=1
P bid
i
, 1
n
nP
i=1
V ask
i
, 1
n
nP
i=1
V bid
i
o
• u5 =
n
nP
i=1
(P ask
i
−P bid
i
),
nP
i=1
(V ask
i
−V bid
i
)
o
where u3 represents the spread and the mid-price, u4 the price diﬀerences, and u5 the price and the
volume means, respectively.
15
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 16

 Electronic copy available at: https://ssrn.com/abstract=3213389 
A.1.3. Time-Sensitive
• u6 =
n
dP ask
i
/dt, dP bid
i
/dt, dV ask
i
/dt, dV bid
i
/dt
on
i=1
• u7 =
n
λ1
∆t, λ2
∆t, λ3
∆t, λ4
∆t, λ5
∆t, λ6
∆t
o
• u8 =
n
1λ1
∆t>λ1
∆T , 1λ2
∆t>λ2
∆T , 1λ3
∆t>λ3
∆T , 1λ4
∆t>λ4
∆T ,
1λ5
∆t>λ5
∆T , 1λ6
∆t>λ6
∆T
o
• u9 = {dλ1/dt, dλ2/dt, dλ3/dt, dλ4/dt, dλ5/dt,
dλ6/dt}
where u6 represents the price and volume derivation, u7 the average type intensity, u8 the relative
comparison intensity, and u9 the limit activity acceleration, respectively.
A.2. Technical Analysis
Technical analysis is based mainly on the idea that historical data provides all the relevant information
for trading prediction. The prediction, based on technical analysis, takes place according to open-close-
high and low prices in day-to-day trading. We adjust this idea to the HFT ML problem for every
10-MB block of events. More speciﬁcally, we consider every 10-MB block as a ’trading’ day (i.e. with
t as the current 10-MB block and t-1 the previous 10-MB block), and we extract features according to
this formation as follows:
A.2.1. Accumulation Distribution Line
Accumulation Distribution Line (ADL) (Chua, 2006) is a volume-based indicator for measuring supply
and demand and is a three-step process:
• MoneyFlowMultiplier = [(Ct −Lt) −(Ht −Ct)]/(Ht −Lt)
• MoneyFlowV olumet = MoneyFlowMultiplier x BlockPeriodV olume
• ADL = ADLt−1 + MoneyFlowV olumet
with Ct, Lt, and Ht being the closing, lowest, and highest current 10-MB block prices, respectively,
and BlockPeriodV olume, ADLt−1, and MoneyFlowV olumet are the total amounts of 10-MB block
volume density, the previous ADL price, and the current MoneyFlowV olumet, respectively.
A.2.2. Awesome Oscillator
An awesome oscillator (AO) (Williams, 1) is used to capture market momentum. Here, we adjust the
trading rules according to the previous block horizon investigation to 5 and 34 previous 10-MB blocks
as follows:
• AO = SMA5((Ht + Lt)/2) −SMA34((Ht + Lt)/2)
where SMA5 and SMA34 are the simple moving averages of the previous 5 and 34 previous blocks,
respectively.
16
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 17

 Electronic copy available at: https://ssrn.com/abstract=3213389 
A.2.3. Accelerator Oscillator
An accelerator oscillator (Williams, 1) is another market momentum indicator derived from AO. It is
calculated as follows:
• AC = AO −SMA5(AO)
A.2.4. Average Directional Index
An average directional index (ADX) indicator (Wilder Jr, 1986) has been developed to identify the
strength of a current trend. The ADX is calculated as follows:
• TR = max(Ht −Lt, |Ht −CLt−1|, |Lt −CLt−1|)
• +DM = Ht −Ht−1
• −DM = Lt −Lt−1
• TR14 = TRt−1 −(TRt−1/14) + TR
• +DM14 = (+DLt−14) −((+DLt−14)/14) + (+DM)
• −DM14 = (−DLt−14) −((−DLt−14)/14) + (−DM)
• +DI14 = 100 × ((+D14)/(+TR14))
• −DI14 = 100 × ((−D14)/(−TR14))
• DIdiff14 = |(+D14) −(−D14)|
• DIsum14 = |(+D14) + (−D14)|
• DX = 100 × ((DIdiff14)/(DIsum14))
• ADX = (ADXt−1 × 13) + DX)/14
where TR = true range, Ht = the current 10-block’s highest MB price, Lt = the current 10-block’s lowest
MB price, CLt = the previous 10-block’s closing MB price, +DM = positive Directional Movement
(DM), −DM = negative DM, TR14 =TR based on the previous 14-blocks, TRt−1 = the previous TR
price, +DM14 = DM based on the previous 14 +DM blocks, −DM14 = DM based on the previous 14
−DM blocks, +DMt−14 = +DM of the previous 14 +DM blocks, DIdiff14 = is the directional indicator
(DI) of the diﬀerence between +DM14 and −DM14, DIsum14 = DI of the sum between +DM14 and
−DM14, DX = directional movement index and ADXt−1 = the previous average directional index.
A.2.5. Average Directional Movement Index Rating
An average directional movement index rating (ADXR) evaluates the momentum change of ADX, and
it is calculated as the average of the current and previous price of ADX:
• ADXR = (ADX + ADXt−1)/2
17
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 18

 Electronic copy available at: https://ssrn.com/abstract=3213389 
A.2.6. Displaced Moving Average Based on Williams Alligator Indicator
A displaced moving average (Gregory-Williams & Williams, 2012) is the basis for building a trading
signal named Alligator. In practice, this is a combination of three moving averages (MA). We adjust
this idea as follows:
• AlligatorJaw = SMA13((Ht + Lt)/2)
• AlligatorT eeth = SMA8((Ht + Lt)/2)
• AlligatorLips = SMA5((Ht + Lt)/2)
where SMA13((Ht + Lt)/2), SMA8((Ht + Lt)/2), and SMA5((Ht + Lt)/2) are the simple moving
averages based on the previous 13, 8, and 5 average highest and lowest block prices, respectively.
A.2.7. Absolute Price Oscillator
An absolute price oscillator (APO) belongs to the family of price oscillators. It is a comparison between
fast and slow exponential moving averages and is calculated as follows:
• Mt = (Ht + Lt)/2
• APO = EMA5(Mt) −EMA13(Mt)
where EMA5(Mt) and EMA13(Mt) are the exponential moving averages of range 5 and 13 periods,
respectively, for the average of high and low prices of the current 10-MB block.
A.2.8. Aroon Indicator
An Aroon indicator (Chande & Kroll, 1994) is used as a measure of trend identiﬁcation of an underlying
asset. More speciﬁcally, the indicator has two main bodies: the uptrend and downtrend calculation.
We calculate the Aroon indicator based on the previous twenty 10-MB blocks for the highest-high and
lowest-low prices, respectively, as follows:
• ArronUp = (20 - Hhigh20/20) × 100
• ArronDown = (20 - Llow20/20) × 100
where Hhigh20 and Llow20 are the highest-high and lowest-low 20 previous 10-MB block prices, respec-
tively.
A.2.9. Aroon Oscillator
An Aroon oscillator is the diﬀerence between AroonUp and AroonDown indicators, which makes their
comparison easier:
• Arron Oscillator = AroonUp - AroonDown
18
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 19

 Electronic copy available at: https://ssrn.com/abstract=3213389 
A.2.10. Average True Range
Average true range (ATR) (Wilder, 1978) is a technical indicator which measures the degree of variability
in the market and is calculated as follows:
• ATR = (ATRt−1 × (N −1) + TR)/N
Here we use N =14, where N is the number of the previous 10-TR values, and ATRt−1 is the previous
ATR 10-MB block price.
A.2.11. Bollinger Bands
Bollinger bands (Bollinger, 2001) are volatility bands which focus on the price edges of the created
envelope (middle, upper, and lower band) and can be calculated as follows:
• BBmiddle = SMA20(CL)
• BBupper = SMA20(CL) + BBstd20 × 2
• BBlower = SMA20(CL) −BBstd20 × 2
where BBmiddle, BBupper, and BBlower represent the middle, upper, and lower Bollinger bands, SMA20(CL)
represents the simple moving average of the previous twenty 10-block closing prices, and BBstd20 rep-
resents the standard deviation of the last twenty 10-MB blocks.
A.2.12. Ichimoku Clouds
Ichimoku clouds (Muranaka, 2000) are ’one glance equilibrium charts,’ which means that the trader
can easily identify a good trading signal and is possible since this type of indicator contains dense
information (i.e. momentum and trend direction). Five modules are used in an indicator’s calculation:
• Conversion Line (Tenkan −sen) = (H9 + L9)/2
• Base Line (Kijun −sen) = H26 + L26
• Leading Span A (Senkou Span A) = (Conversion Line + Base line)/2
• Leading Span B (Senkou Span B) = (H52 + L52)/2
• Lagging Span (Chikou Span) = CL26
where H, L, and CL denotes the highest, lowest, and closing prices of the 10-MB raw data where
subscripts 9, 26, and 52 denotes the historical horizon of our trading rules.
A.2.13. Chande Momentum Oscillator
A Chande momentum oscillator (CMO) (Chande & Kroll, 1994) belongs to the family of technical
momentum oscillators and can monitor overbought and oversold situations. There are two modules in
the calculation process:
• Su =
19
P
i=1
CLi × 1CLt>CLt−19
• Sd =
19
P
i=1
CLi × 1CLt<CLt−19
• CMO = 100 × (Su - Sd)/(Su + Sd)
where CLi is the 10-block’s closing price with i = 1, and CLt and CLt−19 are the current block’s closing
price and the 19 previous blocks closing prices, respectively.
19
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 20

 Electronic copy available at: https://ssrn.com/abstract=3213389 
A.2.14. Chaikin Oscillator
The main purpose of a Chaikin oscillator (Naiman, 2009) is to measure the momentum of the accumu-
lation distribution line as follows:
• MFM= (CLt −Lt) −(Ht −CLt)]/(Ht −Lt)
• MFV = MFM ×
10
P
j=1
Vj
• ADL =ADLt−1 + MFM
• Chaikin Oscillator = EMA3(ADL) - EMA10(ADL)
where MFM and MFV stand for Money Flow Multiplier and Money Flow Volume, respectively, V is
the volume of each of the trading events in the 10-block MB, and EMA3(ADL) and EMA10(ADL) are
the exponential moving average for the past 3 and 10 10-MB blocks, respectively.
A.2.15. Chandelier Exit
A Chandelier exit (Elder, 2002) is part of the trailing stop strategies based on the volatility measured
by the ATR indicator. It is separated based on the number of ATRs that are below the 22-period high
(long) or above the 22-period low (short) and is calculated as follows:
• ChandelierLong = H22 −ATR22 × 3
• ChandelierShort = L22 + ATR22 × 3
where H22 and L22 denote the highest and lowest prices for a period of 22 10-MB blocks, and ATR22
are the ATR values for the 22 previous 10-MB blocks.
A.2.16. Center of Gravity Oscillator
A center of gravity oscillator (COG) (Ehlers, 2001) is a comparison of current prices against older prices
within a speciﬁc time window and is calculated as follows:
• Mt = (Ht + Lt)/2
• COG = −(Mt + r × Mt−1)/(Mt + Mt−1)
where Mt is the current mid-price of the highest and lowest prices of each of the 10-MB blocks, and r
is a weight that increases according to the number of the previous Mt−1 prices.
A.2.17. Donchian Channels
A Donchian channel (DC) (Rayome et al., 2007) is an indicator which bands the signal and notiﬁes the
ML trader of a price breakout. There are three modules in the calculation process:
• DCupper = Hhigh20
• DClower = Llow20
• DCmiddle = (Hhigh20 + Llow20)/2
where Hhigh20 and Llow20 are the highest high and lowest low prices of the previous twenty 10-MB
blocks.
20
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 21

 Electronic copy available at: https://ssrn.com/abstract=3213389 
A.2.18. Double Exponential Moving Average
A double exponential moving average (DEMA) (Mulloy, 1994) provides a smoothed average and oﬀers
a diminished amount of delays as follows:
• Mt = (Ht + Lt)/2
• DEMA = 2 × EMA20(Mt) −EMA20(EMA20(Mt))
where EMA20 is the exponential moving average of span 20 of the closing prices under the 10-MB block
format.
A.2.19. Detrended Price Oscillator
A detrended price oscillator (DPO) is an indicator used for short-term and long-term signal identiﬁ-
cation. A DPO eliminates cycles which are longer than the MA horizon. On day-to-day trading, the
closing prices are considered for the calculation, but here, we use the highest 10-MB block price as
follows:
• DPO = (Hhigh10/(10 + 2)) −SMA10(CL).
A.2.20. Heikin-Ashi
Heikin-Ashi (Valcu, 2004) is a candlestick method and is described as a visual technique that eliminates
irregularities:
• HeikinClose = (Ot + Ht + Lt + CLt)/4
• HeikinOpen = (Ot−1 + CLt−1)/2
• HeikinHigh = max(Ht, Ot−1, CLt−1)
• HeikinLow = min(Lt, Ot−1, CLt−1)
where Ot−1 and CLt−1 are the open and close prices of the previous 10-MB block.
A.2.21. Highest High and Lowest Low
Highest high and lowest low creates an envelope of the trading signal for the last twenty 10-MB blocks:
• HighestHigh = Hhigh20
• LowestLow = Llow20
A.2.22. Hull MA
A Hull moving average is a weighted moving average that reduces the smoothing lag eﬀect by using the
square root of the block period. It is calculated as follows:
• HullMA = WMA√
10(AHL)(2 × WMA5(AHL) −WMA10(AHL))
where WMA5(AHL) and WMA10(AHL) denote the weighted moving average of the average high and
low 10-MB block for periods 5 and 10, respectively.
21
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 22

 Electronic copy available at: https://ssrn.com/abstract=3213389 
A.2.23. Internal Bar Strength
Internal bar strength (IBS) (Pagonidis, 2014) is based on the position of the days closing price in relation
to the days range where we adjust this idea to the 10-MB block setup as follows:
• IBS = (CLt −Lt)/(Ht −Lt).
A.2.24. Keltner Channels
Keltner channels (Keltner, 1960) are based on Bollinger bands. The main diﬀerence, for this volatility-
based indicator, is that it uses ATR instead of standard deviation, as follows:
• MiddleChannel = EMA20AHL
• UpperChannel = MiddleChannel + 2 × ATR10
• LowerChannel = MiddleChannel −2 × ATR10.
A.2.25. Moving Average Convergence/Divergence Oscillator (MACD)
A moving average convergence/divergence oscillator (Aspray, 1989) is a measure of the convergence and
divergence of two moving averages and is calculated as follows:
• MACD = EMA12(AHL) −EMA26(AHL)
where AHL is the average of high and low prices for 12 and 26 previous 10-MB blocks, respectively,
with EMA12(AHL) and EMA26(AHL) as the exponential moving average of AHL of span 12 and 26,
respectively.
A.2.26. Median Price
Median price is an indicator which simpliﬁes the price overview. We calculate this indicator based on
the 10-MB block highest and lowest average prices:
• Mediant = (Ht + Lt)/2
A.2.27. Momentum
A momentum (MOM) indicator measures the rate of change of the selected time series. In our case, we
calculate it based on closing prices:
• MOM = CLt −CLt−1.
22
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 23

 Electronic copy available at: https://ssrn.com/abstract=3213389 
A.2.28. Variable Moving Average
A variable moving average (VMA) (Chande, 1992) is a dynamic indicator which acts as a variable-length
moving average with volatility-adaptation capabilities. We calculate VMA based on the eﬃciency ratio
(ER) as follows:
• Direction = |CLt −CLt−3|
• V olatility = 3 ×
3P
ii=1
|CLii −CLii+1|
• ER = Direction/V olatility
• V MA =
3P
jj=1
α × ERjj × CLjj
where α = 2/(N + 1), for N = 3 previous 10-MB blocks, is the adaptive parameter.
A.2.29. Normalized Average True Range
A normalized average true range (NATR) normalizes the average true range as follows:
• NATR = (ATR/CLt) × 100.
A.2.30. Percentage Price Oscillator
A percentage price oscillator (PPO) displays the convergence and divergence of two moving averages
and focuses on the percentage change of the larger moving average, as follows:
• MACD = EMA12(AHL) −EMA26(AHL)
• PPO = (MACD/EMA26(AHL)) × 100.
A.2.31. Rate of Change
Rate of change (ROC) measures the ascent or descent speed of the time series change:
• ROC = (CLt −CLt−12/CLt−12) × 100.
A.2.32. Relative Strength Index
A relative strength index (RSI) (Wilder Jr, 1986) is a measure of the velocity and magnitude of direc-
tional time series movements and is calculated as follows:
• CLd = CLt −CLt−1
• AG14 =
14
P
l=1
CLdl1CLdt>CLdt−1
• AL14 =
14
P
l=1
CLdl1CLdt<CLdt−1
• RelativeStrength = AG14/AL14
• RSI = 100 −100/(1 + RelativeStrength)
where AG14 and AL14 denotes the average gain and loss of the last fourteen 10-MB blocks, respectively.
23
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 24

 Electronic copy available at: https://ssrn.com/abstract=3213389 
A.2.33. Parabolic Stop and Reverse
Parabolic SAR (PSAR) (Wilder, 1978) is a trend following indicator which protects proﬁts. There are
two main modules for its calculation, the Rising SAR and the Falling SAR, and they are calculated as
follows:
• Rising SAR
– AF = Incremental increase of a predefined step
– EP = HHigh5
– SAR = SARt−1 + AFt−1(EPt−1 −SARt−1)
• Falling SAR
– AF = Incremental increase of a predefined step
– EP = LLow5
– SAR = SARt−1 −AFt−1(EPt−1 −SARt−1)
where AF is the acceleration factor, and EP is the extreme point
A.2.34. Standard Deviation
Standard deviation is a measure of volatility. We calculate this indicator based on the closing prices of
every 10-MB block, as follows:
• Deviation = CLt −SMA10(CL)
• SASD =
p
SMA10(SV D)
where SMA10(CL) is the simple moving average of the last 10 closing 10-MB prices, SASD is the
squared deviation of the SMA of the standard deviation (SVD) of the last 10 closing values of our
10-MB blocks.
A.2.35. Stochastic Relative Strength Index
A stochastic relative strength index (Stoch RSI) (Chande & Kroll, 1994) is a range-bound momentum
oscillator which provides information for the RSI based on the closing prices in terms of high and low
stock prices:
• StochRSI = (RSIcurr −RSILLow10)/(RSIHHigh10 −RSILLow10)
where RSILLow10 and RSIHHigh10 are the lowest low and highest high of the last ten RSI values.
24
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 25

 Electronic copy available at: https://ssrn.com/abstract=3213389 
A.2.36. T3-Triple Exponential Moving Average
A triple exponential moving average (Tillson, 1998) is a moving average indicator where the main
motivation for its development is to reduce lag in the time series response. For this reason, we use the
closing prices for our calculation and perform a reversal explanation calculation as follows:
• T3 = c1 × EMA6 + c2 × EMA5 + c3 × EMA4 + c4 × EMA3
with:
• c1 = −α3
• c2 = 3 × α2 + 3 × α3
• c3 = 6 × α23 × α3 × α3
• c4 = 1 + 3 × α + α3 + 3 × α2
• EMA1 = EMA10(CL)
• EMA2 = EMA10(EMA1)
• EMA3 = EMA10(EMA2)
• EMA4 = EMA10(EMA3)
• EMA5 = EMA10(EMA4)
• EMA6 = EMA10(EMA5)
where α is the volume factor, and EMA10(CL) is the exponential moving average of the 10 previous
10-MB closing prices.
A.2.37. Triple Exponential Moving Average
A triple exponential moving average (TEMA) (Mulloy, 1994) is an attempt to reduce the lag associated
with MA by adding weight to the most recent prices:
• TEMA = (3 × EMA10(CL)) −(3 × EMA10(EMA10(CL)) + EMA10(EMA10(EMA10(CL)))
with EMA being, in every case, the exponential moving average of the previous 10 prices (i.e. previous
EMA and closing prices).
A.2.38. Triangular Moving Average
A triangular moving average (TRIMA) is the average of the time series with emphasis placed on the
middle region:
• TRIMA = SMA10(SMA10(SMA10(CL)))
Where, for its calculation, we use the closing prices of the last 10 10-MB blocks.
25
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 26

 Electronic copy available at: https://ssrn.com/abstract=3213389 
A.2.39. Triple Exponential Average
A triple exponential average (TRIX) is a momentum oscillator which measures the rate of change of
the triple smoothed moving average as follows:
• EMAF irst = EMA10(CL)
• EMADouble = EMA10(EMAF irst)
• EMAT riple = EMA10(EMADouble)
• TRIX = 1-period Rate of Change.
A.2.40. True Strength Index
A true strength index (TSI) (Blau, 1991) is an indicator which speciﬁes the overbought and oversold
levels with market return anticipation. We calculate TSI as follows:
• PC = CLk −CLk−1, where k = 2, ..., T
• APC = |CLk −CLk−1|, where k = 2, ..., T
• EMA1 = EMA25(PC)
• EMA2 = EMA13(EMA1)
• EMA3 = EMA25(APC)
• EMA4 = EMA13(EMA3)
• TSI = 100 × EMA2/EMA4
where PC represents the closing price diﬀerences for the whole time series lookback period.
A.2.41. Ultimate Oscillator
An ultimate oscillator (UO) (Williams, 1985) is a momentum oscillator indicator with a multiple time-
frame perspective. There are three main modules as presented in the following calculations:
• Average of seven 10-MB blocks
– BP = CLt −(CLt−11CLt−1<Lt + Lt1CLt−1>Lt)
– TR1 = CLt−11CLt−1>Ht + Hcurr1CLt−1<Ht
– TR2 = CLt−11CLt−1<Lt + Lt1CLt−1>Lt
– TR = TR1 + TR2
– Average7 =
7P
l=1
BPl/
7P
l=1
TRl
• Average of fourteen 10-MB blocks
– BP = CLt −(CLt−11CLt−1<Lt + Lt1CLt−1>Lt)
– TR3 = CLt−11CLt−1>Ht + Ht1CLt−1<Ht
– TR4 = CLt−11CLt−1<Lt + Lt1CLt−1>Lt
– TR = TR3 + TR4
26
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 27

 Electronic copy available at: https://ssrn.com/abstract=3213389 
– Average14 =
14
P
l=1
BPl/
14
P
l=1
TRl
• Average of twenty-eight 10-MB blocks
– BP = CLt −(CLt−11CLt−1<Lt + Lt1CLt−1>Lt)
– TR5 = CLt−11CLt−1>Ht + Ht1CLt−1<Ht
– TR6 = CLt−11CLt−1<Lt + Lt1CLt−1>Lt
– TR = TR5 + TR6
– Average28 =
28
P
l=1
BPl/
28
P
l=1
TRl
• UO = 100 ×

(4 × Average7) + (2 × Average14) + Average28

/(4 + 2 + 1)
where BP represents buying pressure.
A.2.42. Weighted Close
Weighted close (WCL) is the average of the four universal types of prices which are included in each of
our 10-MB blocks:
• WCL = (Ht + Lt + 2 × CLt)/4.
A.2.43. Williams %R
Williams %R (?) is a momentum technical indicator which informs the ML trader whether the market
is trading close to the high or low trading range. It is calculated as follows:
• %R = −100 × (HHigh14 −CLt)/(HHigh14 −LLow14)
where -100 corrects the inversion.
A.2.44. Zero-Lag Exponential Moving Average
Zero-lag exponential moving average (ZLEMA) belongs to the EMA family of indicators where the main
purpose is to reduce or remove the impulse lag by introducing an error term. It is calculated as follows:
• error = CL −CLlag
• Input = CL + error
• ZLEMA = EMA10(Input)
where lag = (N −1)/2 with N = 1 in our case.
27
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 28

 Electronic copy available at: https://ssrn.com/abstract=3213389 
A.2.45. Fractals
A fractal (Gregory-Williams & Williams, 2012) is an indicator used to detect top and bottom trends
by focusing on ﬁve consecutive blocks, which, in our case, are ﬁve 10-MB blocks used for two diﬀerent
scenarios:
• Buy Fractals
A buy fractal is a sequence of ﬁve consecutive 10-MB blocks where the highest high is preceded
by two lower highs and is followed by two lower highs.
• Sell Fractals
The opposite framework is a sell fractal. 10-MB blocks can overlap in the quest of these two types
of fractals.
Here, we calculate fractals separately for the open, close, lowest, and highest 10-MB block prices.
A.2.46. Linear Regression Line
Linear regression line (LRL) is a basic statistical method that provides information for a future projection
wherein trading is used to capture overextended price trends. We perform LRL for each 10-MB block
without any prior stationarity assumptions. The basic calculations are as follows:
• PV = c1 + c2 × MBprices
• c2 = r × (stdP V /stdMBprices)
• r =

10
P
i=1
(MBprices(i)−MBprices)(P V (i)−P V )

s
10
P
i=1
(MBprices(i)−MBprices)2(
10
P
i=1
(P V (i)−P V )2

• c1 = PV −c2 × MBprices
where PV are the predicted values, r is the correlation coeﬃcient, and MBprices and PV are the mean
of 10-MB block prices and predicted values, respectively.
A.2.47. Digital Filtering: Rational Transfer Function
A rational transfer function (Kumaresan, 1990) is a representation of a linear time-invariant (LTI) ﬁlter,
with the assumption that the input signal depends on the time-frequency domain, which describes the
input-output relationship of a signal. In the Z-tranform domain, we have the following rational transfer
function:
• O(z) = b(1)+b(2)z−1+...+b(nb+1)+z−nb
1+α(2)z−1+...+α(na+1)z−nα I(z),
where:
• I(z) and O(z) are the input (i.e. 10-MB block closing prices) and output respectively,
• b are the numerator coeﬃcients,
• α are the denominator coeﬃcients,
• na is the feedback order,
• nb is the feedforward order,
• z is the complex variable,
• the lookback period for the calculations is ten 10-MB blocks.
28
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 29

 Electronic copy available at: https://ssrn.com/abstract=3213389 
A.2.48. Digital Filtering: Savitzky-Golay Filter
A Savitzky-Golay (S-G) digital ﬁlter (Savitzky & Golay, 1964), Schafer (2011) is a discrete convolution
with a speciﬁc impulse response. We describe how the ML trader can obtain the S-G signal based on
higher degree polynomials:
• Least-Square Filter
– Objective: minimize error EN =
m
P
i=l
wi(yi −
nP
r=0
prxr
i )2
– Partial derivative of the polynomial coeﬃcients:
∂Q
∂pk = 0 ⇒
m
P
i=l
wi
nP
r=0
prxr+k
i
=
m
P
i=l
wiyixk
i
– Finite time series allow order summation change:
nP
r=0
pr
m
P
i=l
wixr+k
i
=
m
P
i=l
wiyixk
i
– As a result, the desired linear equations are the following:


m
P
i=l
wix0
i
m
P
i=l
wix1
i
. . .
m
P
i=l
wixn
i
m
P
i=l
wix1
i
m
P
i=l
wix2
i
. . .
m
P
i=l
wixn+1
i
...
...
...
...
m
P
i=l
wixn
i
m
P
i=l
wixn+1
i
. . .
m
P
i=l
wix2n
i




p0
p1
...
pn

=


m
P
i=l
wiyix0
i
m
P
i=l
wiyix1
i
...
m
P
i=l
wiyixn
i


equivalent to the notation AP = B where matrix A−1 ∈R(n+1)×(n+1) under the condi-
tion that the polynomial degree is n ⩽m −l.
• S-G Filter
– Local convolution coeﬃcients calculation


p0
p1
...
pn

=


m
P
i=l
wix0
i
. . .
m
P
i=l
wixn
i
m
P
i=l
wix1
i
. . .
m
P
i=l
wixn+1
i
...
...
...
m
P
i=l
wixn
i
. . .
m
P
i=l
wix2n
i


−1 

m
P
i=l
wiyix0
i
m
P
i=l
wiyix1
i
...
m
P
i=l
wiyixn
i


⇒
29
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 30

 Electronic copy available at: https://ssrn.com/abstract=3213389 


p0
p1
...
pn

=


c0,0
c0,1
. . .
c0,n
c1,0
c1,1
. . .
c1,n
...
...
...
...
cn,0
cn,1
. . .
cn,n




m
P
i=l
wiyix0
i
m
P
i=l
wiyix1
i
...
m
P
i=l
wiyixn
i


– Response at the local point of 0 degree is:
y[0] = c0,0 ∗
m
P
i=l
wiyix0
i + c0,1 ∗
m
P
i=l
wiyix1
i + ... + c0,n ∗
m
P
i=l
wiyixn
i
A.2.49. Digital Filtering: Zero-Phase Filter
A zero-phase ﬁlter (Smith, 1999) is a bidirectional ﬁltering technique. With zero phase slope and even
impulse response h(n), the ﬁlter provides an output signal, which is a zero phase recursive signal. This
method is suitable for our experimental protocol since we use training and testing sets rather than online
learning architecture as we will do in 4.2.4. The calculation process is as follows:
• Real Impulse response: h(n), n ∈Z
• Discrete-time Fourier Transformation:
HωT (h) =
∞
P
n=1
h(n)cos(ωnT) - j
∞
P
n=1
h(n)sin(ωnT)
• Based on Euler formula and h-even: H(ejωT ) =
∞
P
n=1
h(n)cos(ωnT)
A.2.50. Remove Oﬀset and Detrend
We present three detrend methods for short-term cycle isolation and calculate them as follows:
• Remove Oﬀset
– Offset = CLt −(
nP
l=1
CLl)/n
where n denotes the 10-MB lookback period
• Detrend - Least Squares Fitting Line
– R2 =
nP
i=1
[yi −g(xi)]2
–
∂(R2)
∂α
= 0
–
∂(R2)
∂b
= 0
–

α
b

=


n
nP
i=l
xi
nP
i=l
xi
nP
i=l
x2
i


−1 

nP
i=l
yi
nP
i=l
xiyi


where α and b are the regression coeﬃcients of g, and x represents the 10-MB closing prices.
30
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 31

 Electronic copy available at: https://ssrn.com/abstract=3213389 
A.2.51. Beta-like Calculation
Beta (French, 2003) is a volatility indicator which considers market risk. We adjust the notion of beta
calculation to our experimental protocol where we index based on the average of the closing prices
(AvCL) with Avt as the current MB block price and Avt−1 as the previous MB block’s closing price.
Our calculations are as follow:
• IndexCL = CLt/CLt−1
• IndexAvCL = Avt/Avt−1
• DevCL = IndexCL −SMA10(IndexCL)
• DevAvCL = IndexAvCL −SMA10(IndexAvCL)
• Beta = cov10(DevCL, DevAvCL)/var10(DevAvCL)
where cov10(DevCL, DevAvCL) represents the covariance between the current closing price and the av-
erage of the previous ten 10-MB closing prices, and var10(DevAvCL) is the variance of the sum of the
ten previous IndexAvCL.
A.3. Quantitative Analysis
Quantitative analysis captures trading activity mainly via statistical modelling. We focus on time series
analysis, and more speciﬁcally, we examine features such as autocorrelation and partial autocorrelation,
among others (e.g., statistical tests), while in the end of the section, we build an ML feature extraction
method based on an online learning setup and test the validity of our hypothesis.
A.3.1. Autocorrelation and Partial Correlation
Autocorrelation and partial correlation (Box et al., 2015), (Eshel, 2003) are key features in the devel-
opment of time series analysis. We treat our time series (i.e. stock prices and log returns per 10-MB
blocks) as stationary stochastic processes since we estimate their local behavior based on 10-MB blocks:
• Autocorrelation
– ack =
E[(zt−µ)(zt+k−µ)]
√
E[(zt−µ)2]E[(zt+k−µ)2]
where zt and zt+k are the time series of lag k, µ = E[zt] =
R ∞
−∞zp(z)dz and σ2
z = E[(zt −µ)2] =
R ∞
−∞(z −µ)2p(z)dz are the constant mean and constant variance respectively.
• Partial Correlation
– For the general case of an autoregressive model AR(p), we have:
xi+1 = φ1xi + φ2xi−1 + ... + φpxi−p+1 + ξi+1 of lag 1 up to p follows:
∗< xixi+1 > =
pP
j=1
(φj < xixi−j+1 >)
∗< xi−1xi+1 > =
pP
j=1
(φj < xi−1xi−j+1 >)
∗< xi−k+1xi+1 > =
pP
j=1
(φj < xi−k+1xi−j+1 >)
31
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 32

 Electronic copy available at: https://ssrn.com/abstract=3213389 
∗< xi−p+1xi+1 > =
pP
j=1
(φj < xi−p+1xi−j+1 >)
by diving with N −1 and autocovariance of zero separated periods (where the autoco-
variance function is even), all the lag periods above will be:
∗r1 =
pP
j=1
φjrj−1
∗r2 =
pP
j=1
φjrj−2
∗rk =
pP
j=1
φjrj−k
∗rp =
pP
j=1
φjrj−p
where 2.1.5, 2.1.6, 2.1.7 and 2.1.8 can be described by the matrix operations RΦ = r, R ∈
Rp×p, Φ ∈Rp×1 and r ∈Rp×1. The symmetric and full rank Φ are as follows: ˆΦ = R−1r.
– Yule-Walker Equations calculation:
∗Lag interval 1 ⩽i ⩽p
∗ˆΦ =

R(i)−1
r(i) =


ˆφ1
ˆφ2
...
ˆφi


A.3.2. Cointegration
We investigate time-series equilibrium (Hamilton, 1994), (Engle & Granger, 1987b) by testing the coin-
tegrated hypothesis. Utilizing the cointegration test will help ML traders avoid the problem of spurious
regression. We employ the Engle-Granger (EG) test for the multivariable case of LOB ask (At) and bid
(Bt) times series. We formulate the EG test for the ask and bid LOB prices as follows:
• At and Bt ∼I(d), where I(d) represents the order of integration
• Cointegration equation based on the error term: ut = At −αBt
• EG Hypothesis: u(t)∼I(d), d ̸= 0
• Perform ordinary leat squares (OLS) for the estimation of ˆα and unit root test for: ˆu = At −ˆαBt
A.3.3. Order Book Imbalance
We calculate the order book imbalance (Sirignano, 2016) based on the volume depth of our LOB as
follows:
• V I = V b
l −V α
l
V b
l +V α
l
where V α
l
and V b
l are the volume sizes for the ask and bid LOB sides at level l.
32
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 33

 Electronic copy available at: https://ssrn.com/abstract=3213389 
A.3.4. Logistic Regression for Online Learning
We build a logistic regression model that we use as a feature in our experimental protocol. Motivation
for this model is Sirignano (2016) and Ng (2000) where the focal point is the local behavior of LOB
levels. We extend this idea by doing online learning with an adaptive learning rate. More speciﬁcally,
we use the Hessian matrix as our adaptive rate. We also report the ratio of the logistic coeﬃcients
based on the relationship of the LOB levels close to the best LOB level and the ones which are deeper
in LOB. Since 0 ⩽hθ(V ) ⩽1 and V are the stock volumes for the ﬁrst best six levels of the LOB, we
formulate the model as follows:
hθ(V ) =
1
1 + e−θT V
(A.1)
be the logistic function (i.e. Hypothesis function) and θT V = θ0 +
nP
j=1
θjVj. Parameter estimation is
considered by calculating the parameters likelihood:
L(θ) =
m
Y
i=1
(hθ(V (i)))y(i)(1 −hθ(V (i)))1−y(i)
(A.2)
for m training samples and the cost function, based on this probabilistic approach, is as follows:
J(θ) = 1
m
m
X
i=1

−y(i)log(hθ(V (i))) −(1 −y(i))log(1 −hθ(V (i)))

.
(A.3)
The next step is the process of choosing θs for optimizing (i.e. minimizing) J(θ). To do so, we will use
Newton’s update method:
θ(s+1) = θ(s) −H−1∇θJ,
(A.4)
where the gradient is: ∇θJ = 1
m
m
P
1
(hθ(V (i))−y(i))V (i) and the Hessian matrix is: H = 1
m
m
P
i=1

hθ(V (i))
 1−
hθ(V (i))

V (i)(V (i))T 
with V (i)(V (i))T ∈R(n+1)×(n+1) and y(i) are the labels which are calculated as
the diﬀerences of the best level’s ask (and bid) prices. The suggested labels describe a binary classiﬁ-
cation problem since we consider two states, one for change in the best ask price and another on for no
change in the best ask price.
We perform the above calculation in an online manner. The online process considers the 9th element
of every 10 MB block multiplied by the θ coeﬃcient ﬁrst-order tensor to obtain the probabilistic behavior
(we ﬁlter the obtained ﬁrst-order tensor through the hypothesis function) of the 10th event of the 10
MB block. The output is the feature representation expressed as scalar (i.e. probability) of the bid and
ask price separately.
B. Feature Sorting Lists
A detailed feature name list is available upon request.
1. Features sorting list based on Entropy:
{217;157;165;154;164;207;209;190;191;192;193;174;182;183;146;161;171;172;173;156;155;
184;194;137;177;176;138;195;136;218;213;181;147;245;243;247;188;241;242;244;240;246;
255;248;249;189;210;265;211;226;236;225;235;221;231;223;233;222;232;214;169;220;
230;228;238;224;234;83;84;227;237;139;135;134;142;162;140;185;129;86;128;186;212;
141;250;261;16;20;262;153;14;81;12;208;260;4;18;10;259;24;196;2;163;150;187;82;28;
197;22;8;26;6;32;30;36;34;40;148;175;160;149;38;151;60;59;58;57;56;55;54;53;52;51;
198;215;216;158;167;159;168;152;166;100;102;21;25;29;13;17;9;5;33;1;23;19;15;27;11;31;
33
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 34

 Electronic copy available at: https://ssrn.com/abstract=3213389 
37;7;3;35;85;39;104;252;96;98;106;269;108;92;112;110;88;253;116;124;120;145;94;50;
90;180;256;114;49;170;118;123;122;48;126;268;119;115;80;47;111;143;144;46;107;70;45;
125;103;121;44;117;43;113;99;42;109;254;270;271;105;41;95;101;91;272;97;273;93;179;
69;178;87;68;79;89;127;67;78;201;199;66;133;77;65;76;205;203;61;200;202;71;75;62;
72;64;206;204;257;63;132;131;74;73;130;251;258;267;266;219;229;239;263;264}
2. Features sorting list based on LMS1:
{269;4;6;88;2;211;266;267;249;250;251;92;253;254;91;252;255;193;122;270;174;183;
268;108;103;32;18;147;216;100;118;263;264;111;41;90;112;20;273;24;127;116;120;109;
110;126;225;235;164;107;98;102;124;165;89;94;133;114;119;104;96;95;87;115;188;61;
93;125;101;97;105;113;208;209;99;180;121;117;246;106;123;189;248;228;238;8;210;
186;130;185;10;14;242;157;136;16;218;240;244;65;66;64;69;153;28;73;22;170;143;
142;184;178;30;154;76;79;67;75;63;74;78;256;247;245;146;219;229;239;68;187;62;
70;176;201;179;194;72;197;131;132;77;217;42;43;44;45;46;47;48;49;50;71;85;207;40;
258;226;236;80;260;262;134;135;36;204;144;145;38;26;12;84;199;195;182;215;156;
171;158;151;167;148;161;168;191;152;159;160;149;150;141;198;169;166;1;212;213;181;
3;5;7;9;11;13;15;17;19;21;23;25;27;29;31;33;35;37;39;51;52;53;54;55;56;57;58;59;60;
81;82;86;155;163;196;175;214;272;172;173;140;190;192;139;200;162;227;237;222;232;
220;230;241;243;224;234;271;206;34;83;177;205;203;221;223;231;233;202;138;137;
261;128;129;257;259;265}
3. Features sorting list based on LMS2:
{269;259;262;83;129;130;49;137;177;205;203;257;223;202;200;199;243;273;176;206;
256;204;265;132;10;2;14;84;170;78;240;226;182;157;61;80;242;217;41;70;50;207;165;
150;164;93;87;62;43;89;66;215;18;154;251;111;222;8;261;201;258;270;271;65;96;151;
216;272;210;186;124;120;153;94;187;92;211;117;109;101;162;166;29;213;184;185;198;
195;127;146;191;192;193;196;174;171;159;149;161;139;125;113;106;102;266;118;104;
218;36;38;156;190;250;63;85;133;12;121;90;34;40;175;91;248;241;227;245;152;128;
189;178;214;136;142;158;224;225;112;99;115;264;212;169;141;163;220;221;188;197;
194;209;208;168;22;105;114;110;268;16;23;181;140;119;123;100;126;122;260;244;
246;134;135;131;56;103;173;167;6;228;47;97;255;107;180;71;155;4;254;253;179;
82;138;32;28;143;252;116;30;144;147;88;108;73;95;98;249;20;51;160;247;55;59;
5;148;42;7;76;31;54;3;145;77;46;19;231;48;17;15;81;232;21;45;52;230;236;37;1;24;
58;69;13;53;35;67;172;33;183;79;86;26;267;75;219;25;234;9;44;39;11;229;237;57;
235;239;60;27;68;64;74;233;238;72;263}
4. Features sorting list based on LDA1:
{269;6;88;41;255;211;266;250;249;10;252;251;253;268;8;108;114;174;193;254;100;
263;264;110;186;273;216;90;99;122;185;92;183;267;16;225;235;14;103;119;112;107;
95;104;147;111;91;115;270;127;109;116;120;18;89;94;118;126;98;180;106;208;209;124;
96;188;113;125;121;153;123;105;117;93;97;101;248;242;61;133;189;87;102;210;145;66;
65;64;69;136;184;142;73;76;157;75;74;78;67;63;79;170;178;77;219;229;239;262;182;
130;245;70;22;194;244;24;12;265;84;247;167;173;146;60;207;59;17;33;196;158;165;
4;218;25;149;203;3;36;53;37;86;21;30;155;58;164;48;246;161;223;26;85;226;205;43;
144;80;47;15;135;179;152;27;160;39;38;81;241;50;236;40;220;7;204;260;83;143;258;
168;166;51;141;162;23;57;19;131;9;42;132;82;56;49;62;154;128;5;228;259;55;181;191;
163;156;187;272;213;224;52;46;35;1;54;234;169;150;240;227;45;238;31;201;192;190;
199;261;172;44;134;2;140;129;20;72;214;215;195;68;151;271;198;237;171;11;29;137;221;
222;32;13;217;148;230;232;231;233;197;28;159;206;139;212;256;176;177;243;71;200;
34
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 35

 Electronic copy available at: https://ssrn.com/abstract=3213389 
34;138;175;202;257}
5. Features sorting list based on LDA2:
{265;269;257;138;259;4;262;83;108;68;129;205;204;120;6;48;248;141;179;203;212;
139;184;43;144;118;79;177;18;52;8;193;132;110;70;191;100;103;146;241;143;206;252;
247;273;63;211;207;22;10;142;244;16;258;122;221;219;87;217;47;93;140;40;180;202;
34;256;2;115;96;218;134;102;99;270;111;253;66;189;88;90;94;36;199;12;75;254;243;
72;137;45;272;64;251;77;222;155;255;210;104;209;174;267;105;194;50;14;126;109;32;
170;200;125;98;127;89;227;44;201;119;28;245;61;65;268;192;216;112;20;186;42;250;
187;107;121;116;84;185;128;30;237;156;124;160;195;133;147;41;223;215;123;113;135;
173;148;271;214;169;131;232;39;149;35;178;71;190;31;198;106;157;188;38;260;168;
153;228;55;5;69;246;114;67;15;266;76;152;33;183;37;27;238;46;242;17;166;101;54;
23;117;58;56;11;167;261;9;91;162;29;7;97;163;151;233;57;78;24;95;86;225;164;220;
154;181;249;171;230;229;130;172;60;26;182;51;1;3;136;159;25;59;208;145;85;53;80;
224;92;240;13;81;231;175;264;197;150;74;158;234;213;196;176;235;19;21;263;165;82;
226;236;73;161;239;62;49}
Acknowledgment
The research leading to these results has received funding from the H2020 Project BigDataFinance
MSCA-ITN-ETN 675044 (http://bigdataﬁnance.eu), Training for Big Data in Financial Research and
Risk Management.
References
Aspray, T. (1989). Individual stocks and macd. Technical Analysis of Stocks & Commodities, 7(2):56–61.
Baetje, F. & Menkhoﬀ, L. (2016). Equity premium prediction: Are economic and technical indicators
unstable? International Journal of Forecasting, 32(4):1193–1207.
Bank, P. & Baum, D. (2004). Hedging and portfolio optimization in ﬁnancial markets with a large trader.
Mathematical Finance, 14(1):1–18. Available from: http://dx.doi.org/10.1111/j.0960-1627.
2004.00179.x.
Batchelor, R. & Kwan, T. Y. (2007).
Judgemental bootstrapping of technical traders in the bond
market. International Journal of Forecasting, 23(3):427–445.
Battiti, R. (1994). Using mutual information for selecting features in supervised neural net learning.
Trans. Neur. Netw., 5(4):537–550. Available from: http://dx.doi.org/10.1109/72.298224.
Blau, W. (1991). Double smoothed-stochastics. Technical Analysis of Stocks and Commodities, 9.
Bollerslev, T. (1987).
A conditionally heteroskedastic time series model for speculative prices and
rates of return. The Review of Economics and Statistics, 69(3):542–547. Available from: http:
//www.jstor.org/stable/1925546.
Bollinger, J. (2001). Bollinger on Bollinger bands. McGraw Hill Professional.
Box, G. E., Jenkins, G. M., Reinsel, G. C., & Ljung, G. M. (2015). Time series analysis: forecasting
and control. John Wiley & Sons.
Brasileiro, R. C., Souza, V. L. F., Fernandes, B. J. T., & Oliveira, A. L. I. (2013). Automatic method
for stock trading combining technical analysis and the artiﬁcial bee colony algorithm. In IEEE
Congress on Evolutionary Computation, pages 1810–1817.
35
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 36

 Electronic copy available at: https://ssrn.com/abstract=3213389 
Chan, L. K. C., Karceski, J., & Lakonishok, J. (1999). On portfolio optimization: Forecasting covariances
and choosing the risk model. The Review of Financial Studies, 12(5):937–974. Available from:
+http://dx.doi.org/10.1093/rfs/12.5.937.
Chande, T. S. (1992). Adapting moving averages to market volatility. Stock & Commodities, 10:3.
Chande, T. S. & Kroll, S. (1994). The new technical trader. New York.
Chandrashekar, G. & Sahin, F. (2014). A survey on feature selection methods. Comput. Electr. Eng.,
40(1):16–28. Available from: http://dx.doi.org/10.1016/j.compeleceng.2013.11.024.
Chen, C.-H. (2011).
Feature selectionfor unlabeled data.
In Tan, Y., Shi, Y., Chai, Y., & Wang,
G., editors, Advances in Swarm Intelligence, pages 269–274, Berlin, Heidelberg. Springer Berlin
Heidelberg.
Chua, S. (2006). Sammy Chua’s Day Trade Your Way to Financial Freedom. John Wiley & Sons.
Dash, R. & Dash, P. K. (2016). A hybrid stock trading framework integrating technical analysis with
machine learning techniques. The Journal of Finance and Data Science, 2(1):42 – 57. Available
from: http://www.sciencedirect.com/science/article/pii/S2405918815300179.
de Oliveira, F. A., Nobre, C. N., & Zrate, L. E. (2013).
Applying artiﬁcial neural networks to
prediction of stock price and improvement of the directional prediction index
case study of
petr4, petrobras, brazil. Expert Systems with Applications, 40(18):7596 – 7606. Available from:
http://www.sciencedirect.com/science/article/pii/S0957417413004703.
Dempster, M. A. H., Payne, T. W., Romahi, Y., & Thompson, G. W. P. (2001). Computational learning
techniques for intraday fx trading using popular technical indicators. IEEE Transactions on Neural
Networks, 12(4):744–754.
Diebold, F. X., Hahn, J., & Tay, A. S. (1999). Multivariate density forecast evaluation and calibration in
ﬁnancial risk management: High-frequency returns on foreign exchange. The Review of Economics
and Statistics, 81(4):661–673. Available from: https://doi.org/10.1162/003465399558526.
Dolde, W. (1993). The trajectory of corporate ﬁnancial risk management. Journal of Applied Corporate
Finance, 6(3):33–41. Available from: http://dx.doi.org/10.1111/j.1745-6622.1993.tb00232.
x.
Ehlers, J. F. (2001). Rocket science for traders: digital signal processing applications, volume 112, 2001.
John Wiley & Sons.
Elder, A. (2002). Come into my trading room: A complete guide to trading, volume 163, 2002. John
Wiley & Sons.
Engle, R. F. & Granger, C. W. (1987a). Co-integration and error correction: representation, estimation,
and testing. Econometrica: journal of the Econometric Society, pages 251–276.
Engle, R. F. & Granger, C. W. J. (1987b). Co-integration and error correction: Representation, estima-
tion, and testing. Econometrica, 55(2):251–276. Available from: http://www.jstor.org/stable/
1913236.
Eshel, G. (2003). The yule walker equations for the ar coeﬃcients. Internet resource, 2:68–73.
Fama, E. F. (1968). Risk, return and equilibrium: some clarifying comments. The Journal of Finance,
23(1):29–40.
Fang, Y. & Xu, D. (2003). The predictability of asset returns: an approach combining technical analysis
and time series forecasts. International Journal of Forecasting, 19(3):369–385.
36
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 37

 Electronic copy available at: https://ssrn.com/abstract=3213389 
French, C. W. (2003). The treynor capital asset pricing model. Journal of Investment Management,
1(2):60–72.
Gabrielsson, P., Johansson, U., & Konig, R. (2014). Co-evolving online high-frequency trading strategies
using grammatical evolution. In IEEE Conference on Computational Intelligence for Financial
Engineering Economics, pages 473–480.
Gould, M. D., Porter, M. A., Williams, S., McDonald, M., Fenn, D. J., & Howison, S. D. (2013). Limit
order books. Quantitative Finance, 13(11):1709–1742.
Gregory-Williams, J. & Williams, B. M. (2012). Trading chaos: maximize proﬁts with proven technical
techniques, volume 172, 2012. John Wiley & Sons.
Hamilton, J. D. (1994). Time series analysis, volume 2, 1994. Princeton university press Princeton.
Hampton, J. J. (1982). Modern Financial Theory: Perfect and Imperfect Markets. Reston Publishing
Company.
Inuiguchi, M. & Tanino, T. (2000). Portfolio selection under independent possibilistic information. Fuzzy
Sets and Systems, 115(1):83 – 92. Available from: http://www.sciencedirect.com/science/
article/pii/S0165011499000263.
Jensen, M. C., Black, F., & Scholes, M. S. (1972). The capital asset pricing model: Some empirical
tests. Available from: https://ssrn.com/abstract=908569.
Kablan, A. (2009). Adaptive neuro-fuzzy inference system for ﬁnancial trading using intraday seasonality
observation model. World Academy of Science, Engineering and Technology, 58:479–488.
Kablan, A. & Ng, W. (2010). High frequency trading using fuzzy momentum analysis. In Proceedings
of the World Congress on Engineering, volume 1.
Keltner, C. W. (1960). How to make money in commodities. Keltner Statistical Service.
Kercheval, A. N. & Zhang, Y. (2015). Modelling high-frequency limit order book dynamics with support
vector machines. Quantitative Finance, 15(8):1315–1329. Available from: http://dx.doi.org/
10.1080/14697688.2015.1032546.
Khaidem, L., Saha, S., & Dey, S. R. (2016).
Predicting the direction of stock market prices using
random forest. CoRR, abs/1605.00003. Available from: http://arxiv.org/abs/1605.00003.
Kohavi, R. & John, G. H. (1997).
Wrappers for feature subset selection.
Artiﬁcial Intelli-
gence, 97(1):273 – 324. Available from: http://www.sciencedirect.com/science/article/pii/
S000437029700043X.
Kumaresan, R. (1990).
Identiﬁcation of rational transfer function from frequency response sample.
IEEE Transactions on Aerospace and Electronic Systems, 26(6):925–934.
Kwon, Y. K. & Moon, B. R. (2007). A hybrid neurogenetic approach for stock forecasting. IEEE
Transactions on Neural Networks, 18(3):851–864.
Lintner, J. (1965). The valuation of risk assets and the selection of risky investments in stock portfolios
and capital budgets. The review of economics and statistics, pages 13–37.
Liu, H., Sun, J., Liu, L., & Zhang, H. (2009). Feature selection with dynamic mutual information. Pat-
tern Recognition, 42(7):1330 – 1339. Available from: http://www.sciencedirect.com/science/
article/pii/S0031320308004615.
37
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 38

 Electronic copy available at: https://ssrn.com/abstract=3213389 
Lo, A. W., Mamaysky, H., & Wang, J. (2000). Foundations of technical analysis: Computational algo-
rithms, statistical inference, and empirical implementation. The Journal of Finance, 55(4):1705–
1765. Available from: http:https://doi.org/10.1111/0022-1082.00265.
Lubnau, T. & Todorova, N. (2015). Trading on mean-reversion in energy futures markets. Energy Eco-
nomics, 51(Supplement C):312 – 319. Available from: http://www.sciencedirect.com/science/
article/pii/S014098831500208X.
Markowitz, H. (1952). Portfolio selection. The Journal of Finance, 7(1):77–91. Available from: http:
//www.jstor.org/stable/2975974.
Markowitz, H. M. (1968). Portfolio selection: eﬃcient diversiﬁcation of investments, volume 16. Yale
university press.
Miao, J. & Niu, L. (2016). A survey on feature selection. In 4th International Conference on Information
Technology and Quantitative Management, pages 919 – 926, 2016.
Mossin, J. (1966). Equilibrium in a capital asset market. Econometrica: Journal of the econometric
society, pages 768–783.
Mulloy, P. G. (1994). Smoothing data with faster moving averages. Stocks & Commodities, 12(1):11–19.
Muranaka,
K.
(2000).
Ichimoku
charts.
TECHNICAL
ANALYSIS
OF
STOCKS
AND
COMMODITIES-MAGAZINE EDITION-, 18(10):22–31.
Murphy, J. (1999). Technical Analysis of the Financial Markets: A Comprehensive Guide to Trading
Methods and Applications. New York Institute of Finance Series. New York Institute of Finance.
Available from: https://books.google.fi/books?id=5zhXEqdr_IcC.
Naiman, E. (2009). Small encyclopedia of trader. Moscow: Alpina Business Books, 456.
Ng, A. (2000). Cs229 lecture notes. CS229 Lecture notes, 1(1):1–3.
Ntakaris, A., Magris, M., Kanniainen, J., Gabbouj, M., & Iosiﬁdis, A. (2017). Benchmark dataset
for mid-price prediction of limit order book data. CoRR, abs/1705.03233. Available from: http:
//arxiv.org/abs/1705.03233.
Oriani, F. B. & Coelho, G. P. (2013). Evaluating the impact of technical indicators on stock forecasting.
In IEEE Symposium Series on Computational Intelligence, pages 1–8, 2016.
Pagonidis, A. S. (2014). The ibs eﬀect: Mean reversion in equity etfs. Accessed on 2017-03-17. Avail-
able from: http://www.naaim.org/wp-content/uploads/2014/04/00V_Alexander_Pagonidis_
The-IBS-Effect-Mean-Reversion-in-Equity-ETFs-1.pdf.
Passalis, N., Tsantekidis, A., Tefas, A., Kanniainen, J., Gabbouj, M., & Iosiﬁdis, A. (2017). Time-series
classiﬁcation using neural bag-of-features. In IEEE 25th European Conference of Signal Processing,
pages 301–305, 2017.
Patel, J., Shah, S., Thakkar, P., & Kotecha, K. (2015). Predicting stock and stock price index move-
ment using trend deterministic data preparation and machine learning techniques. Expert Systems
with Applications, 42(1):259 – 268. Available from: http://www.sciencedirect.com/science/
article/pii/S0957417414004473.
Perold, A. F. (1984). Large-scale portfolio optimization. Management Science, 30(10):1143–1160. Avail-
able from: https://doi.org/10.1287/mnsc.30.10.1143.
Poterba, J. M. & Summers, L. H. (1988). Mean reversion in stock prices: Evidence and implications.
Journal of ﬁnancial economics, 22(1):27–59.
38
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 39

 Electronic copy available at: https://ssrn.com/abstract=3213389 
Rayome, D. L., Jain, A., & Konku, D. (2007). Technical analysis: Donchian channels and the british
pound. In IABE-Annual Conference, pages 302, 2007.
Richman, J. S. & Moorman, J. R. (2000). Physiological time-series analysis using approximate en-
tropy and sample entropy.
American Journal of Physiology-Heart and Circulatory Physiology,
278(6):H2039–H2049.
Rodriguez-Gonzalez, A., Garca-Crespo, A., Colomo-Palacios, R., Iglesias, F. G., & Gomez-Berbs, J. M.
(2011). Cast: Using neural networks to improve trading systems based on technical analysis by
means of the rsi ﬁnancial indicator. Expert Systems with Applications, 38(9):11489 – 11500. Avail-
able from: http://www.sciencedirect.com/science/article/pii/S0957417411004313.
Ross, S. A. (1977). The capital asset pricing model (capm), short-sale restrictions and related issues.
The Journal of Finance, 32(1):177–183.
Savitzky, A. & Golay, M. J. (1964). Smoothing and diﬀerentiation of data by simpliﬁed least squares
procedures. Analytical chemistry, 36(8):1627–1639.
Schafer, R. W. (2011). What is a savitzky-golay ﬁlter? [lecture notes]. IEEE Signal Processing Magazine,
28(4):111–117.
Scholtus, M. & van Dijk, D. (2012).
High-frequency technical trading: The importance of speed.
Available from: http://hdl.handle.net/1765/31778.
Sharpe, W. F. (1964). Capital asset prices: A theory of market equilibrium under conditions of risk.
The journal of ﬁnance, 19(3):425–442.
Shen, S., Jiang, H., & Zhang, T. (2012). Stock market forecasting using machine learning algorithms.
Department of Electrical Engineering, Stanford University, Stanford, CA, pages 1–5.
Sirignano, J. (2016). Deep learning for limit order books. Available from: https://arxiv.org/abs/
1601.01987.
Smith, C. W., Smithson, C. W., & Wilford, D. S. (1989). Managing ﬁnancial risk. Journal of Ap-
plied Corporate Finance, 1(4):27–48. Available from: http://dx.doi.org/10.1111/j.1745-6622.
1989.tb00172.x.
Smith, S. W. (1999). The scientist and engineer’s guide to digital signal processing. California Technical
Pub.
Song, F., Mei, D., & Li, H. (2010). Feature selection based on linear discriminant analysis. In IEEE
Proceedings of the 2010 International Conference on Intelligent System Design and Engineering
Application - vol 01, pages 746–749. Available from: http://dx.doi.org/10.1109/ISDEA.2010.
311.
Taylor, S. J. (2008). Modelling ﬁnancial time series. world scientiﬁc.
Teixeira, L. A. & de Oliveira, A. L. I. (2010). A method for automatic stock trading combining technical
analysis and nearest neighbor classiﬁcation. Expert Systems with Applications, 37(10):6885 – 6890.
Available from: http://www.sciencedirect.com/science/article/pii/S0957417410002149.
Thanh, D. T., Kanniainen, J., Gabbouj, M., & Iosiﬁdis, A. (2017).
Tensor representation in high-
frequency ﬁnancial data for price change prediction. arXiv:1709.01268.
Tillson, T. (1998). Better moving averages. Available from: http://www.technicalindicators.net/
indicators-technical-analysis/150-t3-movingaverage,[ziureta20160218].
39
Electronic copy available at: https://ssrn.com/abstract=3213389


## Page 40

 Electronic copy available at: https://ssrn.com/abstract=3213389 
Tsantekidis, A., Passalis, N., Tefas, A., Kanniainen, J., Gabbouj, M., & Iosiﬁdis, A. (2017a). Forecasting
stock prices from the limit order book using convolutional neural networks. In IEEE 19th Conference
on Business Informatics, volume 1, pages 7–12, 2017.
Tsantekidis, A., Passalis, N., Tefas, A., Kanniainen, J., Gabbouj, M., & Iosiﬁdis, A. (2017b). Using deep
learning to detect price change indications in ﬁnancial markets. In IEEE 25th European Conference
of Signal Processing, pages 2511–2515, 2017.
Valcu, D. (2004).
Using the heikin-ashi technique.
TECHNICAL ANALYSIS OF STOCKS AND
COMMODITIES-MAGAZINE EDITION-, 22(2):16–29.
Wen, Q., Yang, Z., Song, Y., & Jia, P. (2010). Automatic stock decision support system based on box
theory and svm algorithm. Expert Systems with Applications, 37(2):1015 – 1022. Available from:
http://www.sciencedirect.com/science/article/pii/S0957417409005107.
Wilder, J. W. (1978). New concepts in technical trading systems. Trend Research.
Wilder Jr, J. W. (1986). The relative strength index ?
J. of Technical Analysis of Stocks and Com-
modities, 4:343–346.
Williams, B. (1). New trading dimensions: how to proﬁt from chaos in stocks, bonds, and commodities,
volume 72, 1998. John Wiley & Sons.
Williams, L. (1985). The ultimate oscillator. Technical Analysis of Stocks and Commodities, 3(4):140–
141.
Wysocki, A. & Lawrynczuk, M. (2010). An investment strategy for the stock exchange using neural
networks. In Federated Conference on Computer Science and Information Systems, pages 183–190,
2013.
40
Electronic copy available at: https://ssrn.com/abstract=3213389


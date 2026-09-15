# The relevance of features to limit order book learning

- **Source File**: `ssrn-4226309.pdf`
- **Total Pages**: 21
- **SSRN ID**: `ssrn-4226309`

---

## Page 1

The relevance of features to limit order book learning
Jie Yina, Hoi Ying Wonga,∗
aDepartment of Statistics, The Chinese University of Hong Kong, Hong Kong
Abstract
The promising predictive power of machine learning (ML) models is encouraging a wide range of
applications, but the weak interpretability of their black-box feature is a major obstacle to their
application to finance. The large scale of limit order book (LOB) data provides fertile ground for
ML implementation and exploration in finance. To examine the contribution of input elements
to ML models, we propose three novel statistical measures for ranking each feature set from the
LOB data and the combinations of feature sets: the p-value from hypothesis testing with a black-
box model, a newly defined out-of-sample R2 with respect to the objective function, and another
new R2 with respect to the classification score. Multiple measures are used to evaluate the level
of significance of the features and their consistency. We empirically test several distinct models
using LOB data from the Chinese A-share market. We find that feature relevance varies greatly
across models for LOB forecasting. Moreover, notable patterns of consistency and significance
offer important insights into the remarkable empirical performance of some black-box models.
The testing results motivate us to improve prediction with ensemble learning. An additional
sensitivity analysis clarifies that the feature rankings are robust to off-machine parameters under
the well-designed deep convolutional neutral network.
Keywords:
Machine learning; Explainable methods for black box; limit order book; deep
learning; Chinese A-share market
1. Introduction
Although data-driven models powered by machine learning (ML) techniques are shown to
be useful in a wide range of applications, the black-box features of these models mean that it is
usually unclear how they derive a certain decision, and therefore, explanations of their prediction
accuracy and stability are lacking.
Traditional statistical methods are inadequate to carry
out structural and technical analyses to understand the rationale underlying the predictions
from black-box models. Consequently, explainable artificial intelligence (XAI), which aims to
elucidate why and under what conditions a model arrives at a specific decision, is attracting a
great deal of attention. XAI enables human beings to understand data-driven ML algorithms
and detect erroneous reasoning (Lapuschkin et al., 2019; Lundberg et al., 2020). In the credit
risk area, this enables the predictions of default probability and loss given default by black-
box models to be explained in terms of their inputs (Bussmann et al., 2021; Bastos & Matos,
2022; Kellner et al., 2022), which is particularly important because transparency is required to
comply with the Basel II agreement. In this study, we propose a set of measures to explain the
performance differences between black- and white-box models, and we apply them to empirically
interpret the forecasts of limit order book (LOB) learners.
After years of ML development, numerous publications are dedicated to the application of
black-box models in stock markets, as the inherent noise and stochastic nature of these markets
limit the utilization of traditional white-box models.
For interday trading, Leippold et al.
∗Corresponding author.
Email addresses: jyin@link.cuhk.edu.hk (Jie Yin), hywong@cuhk.edu.hk (Hoi Ying Wong)
1
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 2

(2022) and Peng et al. (2021) predict stock returns based on a comprehensive set of factors
using various ML algorithms. In the case of intraday trading, the high-frequency financial data
make stock price patterns more sophisticated and volatile than interday patterns. To capture
the essentials, ML models, such as support vector machines (SVM) (Kercheval & Zhang, 2015),
multilayer perceptrons (MLP) (Nousi et al., 2019), and deep neural networks (Chong et al.,
2017; Zhang et al., 2019), are used to contribute to forecasting short-term price movements of
stocks and achieve greater out-of-sample precision than simple linear methods (Briola et al.,
2020). The LOB data and elicited features are well utilized in the literature, but proper in-depth
explanations of the use of these features is lacking. This may undermine confidence in a wide
range of applications and hinder future improvements.
Several methods or measures for uncovering black boxes are proposed in the literature.
Shapley values (Lundberg & Lee, 2017) are designed to measure the importance of variables,
but their calculation is computationally demanding for high dimensions. Another option is an
accumulated local effects plot (Apley & Zhu, 2020), which is a visual representation of how
a single predictor influences the model predictions; however, it is not workable for multiple
predictors. Model-based significance tests by Horel & Giesecke (2020) discern the impact of
individual variables but are restricted to a single-layer feed-forward neural network model.
In this paper, we propose a feature explanation framework with three complementary sta-
tistical measures for LOB learning models. The first measure is based on model-free hypothesis
testing with unknown limiting distributions of parameter estimates. Specifically, we adopt the
statistical significance test derived by Dai et al. (2022) as a simultaneous test of a collection
of features that does not require massive computing. That is, we attempt to explain the fea-
ture relevance for the intractable LOB forecasting algorithms using model-free p-values. The
novel p-values have the same statistical interpretation as classical p-values. Loosely speaking,
the p-value of an input feature reflects the likelihood that the contribution of this feature to
prediction is purely by chance under the null hypothesis. Thus, the lower (higher) the p-value,
the higher (lower) is the significance level of an input feature. The other two measures that
we propose for evaluating feature importance are novel out-of-sample R-square measures with
respect to the predictive error ( ˜R2
error) and the area-under-the-curve (AUC) score ( ˜R2
AUC). More
convincing and compelling results can be achieved by using multiple measures to explore the
facts than using one measure only (Huynh-Thu et al., 2012). These three measures not only
enable us to test feature significance under black-box models but also provide a method to com-
pare traditional and state-of-the-art models in terms of measure consistency. More precisely, a
stable and consistent learning framework is expected to produce a consistent ranking for feature
selection among the three measures. Our empirical study finds that a deep convolutional neural
network (DCNN) stands out in LOB learning in terms of these three measures. It also performs
best in terms of the conventional Sharpe ratio for profit performance.
To better understand the nonlinear mapping between the input features and output predic-
tions of LOB models, we test for a collection of hypothesized features. In Section 2, four major
feature sets are used: raw LOB data, order flow, a time-insensitive set, and a time-sensitive set.
These feature sets describe the market from different perspectives, serve as distinct functional
regions, and contribute insights into the short-term price trend to varying degrees. They are
fed into both white- and black-box models, including multinomial logistic regression, multi-
class SVM, random forest, and DCNN models, as we discuss in Section 3. The models extract
compressed and invisible knowledge from the features and then predict the nature of trading
signals as long, short, or none. Then, the obtained signals are put forward to generate invest-
ment strategies. Under the complete scheme, our objective is to investigate the roles of both
individual and integrated feature sets for LOB prediction.
We conduct an empirical study using Chinese A-share market data to test the marginal ef-
fect of each feature set and the joint importance of combined feature sets. The implementation
of the three explainable measures reveals the information on which the predicted signals are
2
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 3

based. First, the most important determinants of trading signals differ for all of the models
under investigation, implying that the importance of the variables is sensitive to the model
structure. Second, we determine and analyze the consistency between the three measures and
the significance of the features within the same model. For DCNN, the three measures present
consistent rankings for 14 features with a certain degree of significance. Conversely, for the
other three models, no consistency is found for the logistic regression, the significance levels are
generally very low for SVM, and the random forest method leads to performances exhibiting
great disparities. Furthermore, the patterns and behaviors of the feature rankings help explain
the performance of the original models. Both the measure consistency and the feature signif-
icance support the conclusion that the DCNN has a stronger ability than the other measures
to digest features and capture valuable internal connections because of its complex nonlinear
structure.
To the best of our knowledge, this paper is the first to articulate and explain the remarkable
performance of deep learning for LOB forecasting and trading. The inconsistency and insignifi-
cance of input features found when using the parametric linear models of logistic regression and
SVM show that a successful LOB prediction relies on a complex and nonlinear transformation
of the input features. Further, we empirically confirm that the nonlinear ML framework of the
random forest successfully identifies several significant input features, each of which consistently
improves prediction. However, the random forest does not fully utilize the nonlinear informa-
tion contained in the rest of the features. The DCNN gains predictive improvement from all of
the input features, as reflected in the prediction measures of ˜R2
error and ˜R2
AUC. In addition, the
significance levels based on the p-values are consistent with the prediction measures for almost
all of the input features. Ranking the significance of the features helps us to understand the
key decision variables of a black-box model if there is consistency between the three measures.
Although parametric models are easy to interpret, the conclusions developed from a parametric
model could be in doubt if the model is consistently inconsistent in terms of its significance and
prediction analysis.
The learned experience from black-box models is crucial and informative for improving
models.
We provide a preliminary demonstration.
Considering the results for feature rele-
vance tested on 30 stocks in the Chinese A-share market, we adopt ensemble learning with the
bagging algorithm to combine the DCNN and random forest. First, we train the two models
independently on the most significant feature sets and then use the weighted combined model
for predictions. We find that both prediction accuracy and actual profit are promoted when
the models are combined, indicating that input features are well-pruned and utilized. On the
one hand, a single simplified model with fewer features contains less disturbance and noise than
a combined model, and the feature selection procedure is beneficial. On the other hand, sub-
sequent ensemble modeling can incorporate refined intelligence that originates from different
feature sets altogether. It ensures that feature sets not selected by one model are processed in
another model and that no related information is overlooked.
Finally, we conduct an additional sensitivity analysis to show the robustness of our measures
under the DCNN. Consistent rankings of feature importance for each experiment indicate that
the time period, data split, and stock selection are not substantial off-machine parameters,
instead being trivial external settings that do not contribute greatly to the feature relevance
rankings. Therefore, our interpretations hold true for universal stocks in the market and are
not limited to short time periods. This sensitivity analysis strengthens our confidence in the
model-free significance test and supports the adoption of these measures in a wide range of
areas.
The rest of this paper is organized as follows.
In Section 2, we introduce the concepts
and definitions of the four major feature sets. Section 3 describes the four distinct models for
forecasting the trading signals in detail. We explain and conduct the significance tests of the
feature sets using the three proposed measures (p-value, ˜R2
error, and ˜R2
AUC) in Section 4. Then,
3
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 4

in Section 5, we empirically evaluate the performance of the feature testing and improve the
predictions for the Chinese A-share market. A sensitivity analysis is also included. Section 6
concludes the paper. The technical details are provided in the Appendix.
2. Input feature sets
As data-driven algorithms, ML frameworks for LOB require essential “ingredients” as their
foundation. These ingredients are different forms of data and features. In addition to raw LOB
data (Zhang et al., 2019; Yin & Wong, 2022), many features are proposed and tested in the liter-
ature. Tsantekidis et al. (2020) demonstrate that their proposed stationary features significantly
outperform the raw price features, and Kolm et al. (2021) show that models trained on order
flow significantly outperform those trained directly on order books. Many other handcrafted
features are designed and evaluated by Kercheval & Zhang (2015); Ntakaris et al. (2019); Nousi
et al. (2019). Our choice of the feature sets that follow is based on their practical implications,
tractable mathematical calculations, and experimental performance in the literature.
2.1. Raw limit order book data
We first introduce the direct and visible high-frequency data sent by the exchanges at every
tick time t. The basic features of the tick-by-tick LOB data are prices and volumes at each level
from both the ask and bid sides of the market. Let
x1t :=
h
p(i)
a (t), v(i)
a (t), p(i)
b (t), v(i)
b (t)
in
i=1 ∈R4n,
(2.1)
where p(i)
a (t) and v(i)
a (t) denote the ask price and ask volume, respectively, at level i at time t.
Similarly, p(i)
b (t) and v(i)
b (t) denote the price and volume, respectively, on the bid side.
The data describe the shape of markets and summarize the fundamental trading circum-
stances. Listed orders with prices and volumes contain a great deal of valuable content. How-
ever, inherent noise and randomness are inevitable and will distort predictive power. Therefore,
we derive additional feature sets from the raw LOB data with the aim of extracting more
granular and refined information.
2.2. Order flow
To capture the transformation of the LOB, we integrate information on volumes and prices.
Simply put, this feature set is derived by calculating changes of volumes conditioned on the
price changes at each level. We use the following definition of order flow at tick time t as the
vector:
x2t :=
h
bOF(i)(t), aOF(i)(t)
in
i=1 ∈R2n,
(2.2)
where the bid order flows (bOF) and ask order flows (aOF) proposed by Kolm et al. (2021) are
given, respectively, by
bOF(i)(t) :=





v(i)
b (t),
if p(i)
b (t) > p(i)
b (t −1),
v(i)
b (t) −v(i)
b (t −1),
if p(i)
b (t) = p(i)
b (t −1),
−v(i)
b (t),
if p(i)
b (t) < p(i)
b (t −1),
aOF(i)(t) :=





−v(i)
a (t),
if p(i)
a (t) > p(i)
a (t −1),
v(i)
a (t) −v(i)
a (t −1),
if p(i)
a (t) = p(i)
a (t −1),
v(i)
a (t),
if p(i)
a (t) < p(i)
a (t −1).
(2.3)
The result is a modest generalization of the order flow imbalance (OFI) proposed by Cont
et al. (2014). The superior explanatory power of the OFI for market impact shown in Cont
et al. (2021) provides evidence that order flow is highly correlated with future returns.
4
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 5

2.3. Time-insensitive set
Now, rather than combining volumes and prices, we formulate indicators separately from
prices and volumes. We design the time-insensitive features depending on the data at the same
tick time t (conversely, if we use data across time, we obtain a time-sensitive feature set, as we
discuss below). These handcrafted features are used in Kercheval & Zhang (2015); Nousi et al.
(2019).
The time-insensitive features describing the spread, mid-price, and price differences between
adjacent levels of both sides are extracted. We denote the bid–ask spread for every level i as
p(i)
a (t) −p(i)
b (t), and the mid-price as (p(i)
a (t) + p(i)
b (t))/2. They form the vector
A :=
h
p(i)
a (t) −p(i)
b (t), (p(i)
a (t) + p(i)
b (t))/2
in
i=1 .
Price differences between adjacent levels are given by
B :=
hp(i+1)
a
(t) −p(i)
a (t)
 ,
p(i+1)
b
(t) −p(i)
b (t)

in−1
i=1 ∈R2n−2.
All the features are combined to obtain the following time-insensitive set:
x3t := (A, B) ∈R4n−2.
(2.4)
This static feature set best characterizes the price relationship on the panel.
2.4. Time-sensitive set
The time-sensitive set mainly concerns price and volume derivatives for each level i, which
are defined as
h
dp(i)
a /dt, dp(i)
b /dt, dv(i)
a /dt, dv(i)
b /dt
i
.
The average time derivatives of price and volume can be computed numerically over several
contiguous time ticks. The number of ticks used depends on the time interval between two
ticks, which varies greatly between markets. For the Chinese A-share market, the subject of
our empirical study, the time interval is usually around 3 seconds, which is much longer than
the case in other more mature markets. Prices and volumes of most stocks tend to present a
few changes during a 3-second time interval. Therefore, using the two most recent ticks, at time
t and t −1, the time-sensitive set is numerically calculated by
x4t :=
h
p(i)
a (t) −p(i)
a (t −1), p(i)
b (t) −p(i)
b (t −1),
v(i)
a (t) −v(i)
a (t −1), v(i)
b (t) −v(i)
b (t −1)
in
i=1 ∈R4n.
(2.5)
2.5. Integration of features
We combine the four feature sets defined in (2.1)-(2.5) to create a much larger feature set
Xt that includes all of the features in x1t, x2t, x3t, and x4t. Our combination of different
feature sets is inspired by the brain’s structure and function. The brain is divided into several
functional sections, with cooperation and communication between the different regions enabling
various kinds of functions. The central nervous system integrates the received information and
sends the processed signals to all parts of the body. Our LOB trades are similar operations that
generate trading signals. Figure 1 shows the analogy between the brain system and the LOB
trading system.
The objective of LOB trading is to classify the trading signals as long, short, or none. long
means that we expect an upward trend of the stock price and buying before selling, whereas
short indicates the opposite, selling before buying. If the stock is too stable for a trend to be
captured, we denote it as the third type of trading signal, none. The signals are determined by
5
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 6

the approximate wealth changes during a fixed and limited holding period, during which we set
stop-loss and take-profit points to control risks. These labels closely reflect actual transactions
and earnings, with details given in Appendix A.
Although the regions of the brain work together as a network to process information for
determining actions, there should be different critical areas responsible for different specific
actions. Learning the relevance of the regions with functions can help us better understand
how the brain, and, analogously, the LOB trading system, works. We want to determine which
regions are the most important or the most irrelevant.
Therefore, we want to explore the
relevance of the four major features to the trading signal predictions instead of simply pursuing
the accuracy of forecasts. This kind of hidden information explains the logic of black boxes and
enables us to make better use of those features later.
Figure 1: Illustration of how forecasting trading signals using features is analogous to the brain structure and
functions. The invisible mechanism from input features to output signals needs to be explored and explained.
Another inspiration for feature testing comes from the image processing procedure under
convolutional neural networks. The input features are converted into image pixels, as in Figure
2. Usually, a full picture is not required to make a judgment, and a small region is enough to
make a decision. Different regions of the picture carry different levels of information, generating
a ranking of feature relevance. The images composed of the feature sets enable us to explore
the key points of those visualized inputs.
Input features X
t
Tick time t
−7.5
−5.0
−2.5
0.0
2.5
5.0
7.5
10.0
Figure 2: Heatmap of input features for 50 time ticks. The black dotted vertical lines segment the picture into
four regions representing, from left to right, the feature sets x1, x2, x3, and x4. The heatmap is plotted from
the normalized real data of stock SZ300052.
3. Models
Many models are designed to address multi-classification problems such as the issue that
we consider. In this section, we consider four such models, ranging from naive to sophisticated,
covering different levels of complexity, and including both white- and black-box models.
6
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 7

3.1. Multinomial logistic regression
Logistic regression is a classic statistical model that, in its basic form, uses a logistic function
to model a binary dependent variable for solving classification problems. It can be extended
to a multinomial type with M classes. The response Y containing M categorical variables is
defined as
Yt = (y1t, ..., yMt)T , where yit =
(
1,
if i is the true label,
0,
o.w.
(3.1)
The probability of being the i-th category for sample t, pit, is modeled by a linear predictor
βiXt in the following way:
logit (pit) = ln
 pit
pMt

= βiXt,
(3.2)
where pit = P(yit = 1, yjt = 0, j ̸= i). For samples with t ranging from to T, the likelihood L is
available and the negative log-likelihood is given by
Llog = −ln(L) = −
T
X
t=1
M
X
i=1
yit log ˆpit.
(3.3)
Because the number of parameters is very large, we add an L1-regularization to avoid over-
fitting and obtain sparse estimations by solving the following:
min
β Llog + λ
M
X
i=1
||βi||1,
(3.4)
where || · ||1 denotes L1-Norm. The penalty is the same as the one used in LASSO regression
(Tibshirani, 1996).
3.2. Multi-class support vector machine
The basic SVM (Cortes & Vapnik, 1995) is a common type of binary classifier. Given the
feature Xt and the label yt ∈{1, −1}, the problem is formed as
min
w,b,ξ
1
2wT w + C
T
X
t=1
ξt,
subject to
yt
 wT ϕ (Xt) + b

≥1 −ξt,
ξt ≥0,
t = 1, . . . , T,
(3.5)
where ϕ is the feature mapping function and C > 0 is the regularization parameter. ϕ (Xt)
maps the feature into a higher-dimensional space to allow the data to be linearly separable.
The regularization is to penalize data on the wrong side of the hyperplane. Because we have a
large number of features and training samples, the linear kernel function is much faster and less
prone to overfitting than a nonlinear kernel. Furthermore, SVM with a linear kernel function
is usually comparable with logistic regression.
For a multi-class classification model, the SVM is reduced to a set of binary classification
tasks by the one-over-the-rest method and each classifier is trained independently. In the case
of three classes, we need to construct three binary classifiers and make decisions based on all of
the outcomes.
7
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 8

3.3. Random forest
The random forest method proposed by Breiman (2001) is a combination of tree predictors
such that each tree depends on the values of a random vector sampled independently, and all
of the trees in the forest have the same distribution. In other words, this classifier consists of a
collection of tree-structured classifiers {h(X, Θk), k = 1, ...}, where the {Θk} are independent
and identically distributed random vectors and each tree casts a unit vote for the most popular
class at input X.
Thus, random forest is basically an ensemble learning method through majority voting based
on all of the outputs from a multitude of decision trees. Therefore, it avoids the overfitting
problem of an individual decision tree and is relatively stable. Generally, random forest is more
advanced and captures more of the nonlinear structure than logistic regression or SVM.
3.4. Deep convolutional neural network
Combining historical LOB data, e.g., 50 ticks, the two-dimensional input resembles Figure
2, with time indicated on one axis and features indicated on the other. It is reasonable to apply
convolutional layers with different shaped filters, which are designed to summarize information
from each level, from the bid and ask sides, or from the nearest several time steps. Zhang
et al. (2019) propose DCNN for raw LOB data that correspond to our feature set x1. Adopting
similar DCNN models under a novel integrated LOB trading system, the prediction accuracy
and actual profits are guaranteed, as shown in Yin & Wong (2022). We adapt this DCNN to
deal with other feature sets, which we denote as DCNN1–DCNN4, and concat or merge them
together to reach the final output. The model structure of this DCNN is summarized in Figure
3.
To reduce overfit, the dropout layer offers a very computationally cheap and remarkably
effective regularization method by randomly dropping out nodes during training (Srivastava
et al., 2014). Nonetheless, the number of parameters is much larger and the structure is much
more complex than those of the aforementioned methods, making it hard to explain why the
output is reached or which feature plays a key role. There are other interesting questions, such
as whether the nonlinearity is captured and whether the features are well utilized.
Figure 3: Model structure of the DCNN designed for learning all four feature sets.
As the architecture of
the individual DCNN submodels is similar, we provide details of the submodel DCNN1 only along with the
hyperparameters in Appendix B.
8
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 9

4. Significance test of the feature sets with measures
4.1. p-value
In response to the limitations of the model-free hypothesis testing proposed by Candes et al.
(2018) and Tansey et al. (2018), Dai et al. (2022) provide a valid p-value for any pre-specified
region (feature) based on a black-box model. Given its wide range of applications, we expect
that this will enable us to learn the relevance of the features of our DCNN model and compare
our model with other accessible models. Under the model-free hypothesis, it is possible to rank
the importance of features by p-values for all models; that is, the method is not limited to
classic statistical models, traditional ML models, or deep learning models. In addition, the
ability of the model to deal with different features is beneficial to further enhancing the model
performance.
First, we clarify the notations with definitions. We determine a model to predict the response
Y based on the features X, and the loss function l(f(X), Y ) calculates the discrepancy between
the true value and the prediction. To capture the subtle differences between models and subse-
quently carry out accurate AUC score calculations, we predict the probability of each category
and denote it as vector ˆP . The model expressed as a function f can be learned by traditional
statistical models or ML models, such as those introduced in Section 3. R(f) = E(l(f(X), Y ))
is the corresponding risk.
The objective is to test the relevance of a subset of features XS = {xj : j ∈S} to the
prediction of Y with an unknown form of the prediction function, where S is an index set of
hypothesized features and the remaining features are denoted as XSc = {xj : j /∈S}, with Sc
indicating the complement set of S. Then, we replace the values of XS with zero and obtain
the masked feature Z. This comparative model is given as the prediction function g, and the
risk is RS(g) = E(l(g(Z), Y )).
For any loss function, conditional independence between the response and tested features
implies risk invariance, which is expressed as
Y ⊥XS | XSc =⇒R (f∗) −RS (g∗) = 0,
(4.1)
where f∗= arg minf R(f) and g∗= arg ming RS(g). Then, the significance test for the feature
set S is constructed in the following way:
H0 : R (f∗) −RS (g∗) = 0,
versus
H1 : R (f∗) −RS (g∗) < 0.
(4.2)
Referring to the one-split test in Dai et al. (2022), we split the given dataset (Xt, Yt)T
t=1
into the training set (Xt, Yt)n
t=1 and the testing set (Xt, Yt)n+m
t=n+1, with m = T −n.
The
training set includes the validation set for early stopping to prevent the overfitting problem.
The trained models are expressed by the functions ( bf, bg) to approximate (f∗, g∗). Then, we plug
these estimators into the evaluation of the testing samples. We can obtain a good estimation of
R (f∗) −RS (g∗) by the empirical risk function, which is ˆR

ˆf

−ˆRS (ˆg). As an averaged loss,
the empirical risk is calculated as ˆR

ˆf

= 1
m
Pm
j=1 l

bf (Xn+j) , Yn+j

for the testing set, and
is similarly defined for the comparative model ˆg.
Therefore, the test statistic is given as
Λn =
Pm
j=1 ∆n,j
√mbσn
,
∆n,j = l

bf (Xn+j) , Yn+j

−l (bg (Zn+j) , Yn+j) + ρεj,
(4.3)
where bσn is the sample standard deviation based on the inference set {∆n,j}m
j=1, and ρ is a
level of perturbation to address the vanishing standard deviation. According to the asymptotic
distribution of Λn in Theorem 2 of Dai et al. (2022), under some conditions, Λn
d→N(0, 1), as
n →∞. The p-value is calculated by
P = Φ (Λn) ,
(4.4)
9
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 10

where Φ(·) is the cumulative distribution function of the standard normal distribution.
In statistical hypothesis testing, there is always a significance level α, which is the probability
of the study rejecting the null hypothesis. Usually, α is set to 5% or 10% to determine whether
the result is statistically significant. However, it is not applicable to our empirical study in
Section 5.1. The averaged p-values among large amounts of stocks are much larger than the
individual values. Instead of setting a rigorous threshold, we rank these features to determine
their relative significance levels. In other words, the p-value is regarded as a measure of feature
relevance, similar to other additional measures that we define in the following (Section 4.2).
As an interesting direction for future research, we can choose a threshold after examining the
overall p-value level and select relevant features from the ranking (Huynh-Thu et al., 2012).
In addition, the proposed risk-based testing is workable for any loss function, such as constant
loss, L2-loss, or cross-entropy loss. The exact values of Λ and P are related to the choice of loss
function l(·). However, consistently using the identical loss function gives comparable results
for ranking. In our case, the loss function is the same as the one used for training models. The
focal loss function originally proposed in Lin et al. (2017) is designed for imbalanced data, and
is written as
l( ˆYt, Yt) = −
M
X
i=1
bi(1 −ˆyit)γyit log ˆyit,
(4.5)
where bi and γ are additional hyperparameters used to adjust the class weights. The effect
of the modulating factor (1 −ˆyit)γ is increased with γ. On the contribution of the focal loss
function compared with the traditional categorical cross-entropy loss function, refer to Yin &
Wong (2022).
4.2. R-squares
We propose additional measures, apart from the p value, to evaluate the features’ relevance
in a comprehensive manner. The measures are derived from the coefficient of determination
and modified according to the most general definition, which is R2 = 1−
P(yi−ˆyi)2
P(yi−¯y)2 . This classic
statistical measure determines the proportion of variance in the dependent variable that can be
explained by the independent variable. In the spirit of its interpretation, we define the out-of-
sample ˜R2 to measure the explanatory power of the hypothesized feature S, and we generalize
it in terms of the loss function and AUC score. A similar self-defined out-of-sample R2 in Gu
et al. (2020) is used to assess predictive performance for individual excess stock return forecasts,
and is further applied in Leippold et al. (2022) to determine the most important predictors in
the Chinese and US markets.
Instead of using the most common mean squared error as in the definition of R2, we quantify
the model error by the loss functions. The negative consequences of error can be measured
by symmetric or asymmetric loss functions. Although the loss function is widely applied in
regression or classification problems, calculating the AUC score is a very popular means of
measuring the ability of a classifier to distinguish between classes (Hanley & McNeil, 1983).
Huang & Ling (2005) show theoretically and empirically that the AUC is preferable to total
accuracy as a classifier evaluation. The AUC score is desirable and useful because it is invariant
to scale and classification thresholds, and is coherent, especially for imbalanced data (Flach
et al., 2011; He & Garcia, 2009).
As we mention above, the binary classifier AUC stands for “the area under the curve,” where
the “curve” refers to the receiver operating characteristic (ROC) curve, which plots the true
positive rate against the false positive rate at various threshold settings. That means we need
to input the predicted probabilities instead of labels to obtain an accurate ROC curve. AUC
ranges in value from 0 to 1; the higher (lower) the AUC, the better (worse) is the performance of
the model in distinguishing positive and negative classes. We can easily extend it to multi-class
classification problems by using the one-over-the-rest technique and a micro-average that will
10
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 11

aggregate the contributions of all classes to compute the average metric. Considering that our
dataset is imbalanced, the micro-average is preferable because it assigns unequal weights to the
labels.
In the context of a predictive or inferential model, we evaluate the performance of each
subset of features S by using the out-of-sample ˜R2 for each testing period, defined as
˜R2
error :=
m
X
j=1
l (bg (Zn+j) , Yn+j) /
m
X
j=1
l

bf (Xn+j) , Yn+j

−1,
(4.6)
˜R2
AUC := 1 −s

[bg (Zn+j) , Yn+j]m
j=1

/s
h
bf (Xn+j) , Yn+j
im
i=1

,
(4.7)
where l(·) is the loss function and s(·) is the AUC score. Other notations are the same as in
Section 4.1 for calculating the p-value. Generally, the larger (smaller) the ˜R2
error/ ˜R2
AUC, the
more (less) significant is the feature set S. The values of ˜R2
error/ ˜R2
AUC might be negative in
some cases where the masked features Z are better than the original whole feature set X for
prediction. Tested features are not significant and not contributing, merely providing noise or
other misleading information.
One should be cautious about comparing these two measures between different models.
Because they are highly correlated with the original model performance and are calculated
based on the improvement or degradation brought about by the selected features, the values
are model-dependent. To some extent, the ranking of hypothesized features is usually restricted
to testing under an identical initial model.
Cross-model comparisons of absolute ˜R2 values
require consideration of additional scaling or regularization.
5. Results of the feature relevance
5.1. Empirical study on the Chinese A-share market
We study the marginal effect of the individual feature sets and the joint importance of the
combined feature sets. The index set of hypothesized features is denoted as
S ∈{1, 2, 3, 4, 12, 13, 14, 23, 24, 34, 123, 124, 134, 234},
where 1, 2, 3, 4 represent the raw LOB x1, the order flow x2, the time-insensitive set x3, and
the time-sensitive set x4, respectively.
Other numbers represent combinations of the speci-
fied feature sets; for example, 12 is the joint set {x1, x2} and 123 combines the feature sets
{x1, x2, x3}.
The 10-level LOB data used for the experiments are level-II tick data from two major Chinese
A-share markets, the Shanghai Stock Exchange (SHSE) and the Shenzhen Stock Exchange
(SZSE). The proprietary data are provided by the Fintech company TradeMaster1. Because of
the computational time and data availability, we empirically analyze the historical LOB data
covering 30 stocks and five periods. The total testing period for one stock lasts over two months
(50 weekdays). Models are trained at the individual stock level, and features are tested under a
total of 150 sets of data. We use the four models in Section 3 in the empirical study, denoted by
their abbreviations. We use box and bar plots to display summary statistics, as shown below,
and the results of the same model are represented in the same color in the figures.
First, Figure 4 shows the p-values of all of the hypothesized features S under two models, the
classic logistic regression (LR) model and the advanced DCNN model. The white hollow dots
represent the average of individual stock results, and the boxplot displays the distribution of
p-values in regard to stocks. We find that there are huge disparities in the magnitude of p-values
1https://www.trademastertech.com
11
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 12

between stocks. However, the rank of feature importance is much more stable and less sensitive
to stock selection, especially from a stock pool perspective, which is discussed in Section 5.3.
Moreover, estimated p-values for features tested by the DCNN model are much smaller than
those produced by the LR model. For such a high-dimensional intricate problem with noisy
and non-stationary characteristics, deep learning techniques are considered to provide stronger
support for feature engineering than other more preliminary models (Zhu et al., 2018; Long
et al., 2019).
1
2
3
4
12
13
14
23
24
34
234
134
124
123
0.0
0.2
0.4
0.6
0.8
1.0
p-value
LR
DCNN
Figure 4: Boxplot of p-value estimated for hypothesized features under the logistic regression and DCNN. The
white hollow dots refer to the mean and the black horizontal lines refer to the median.
From a stock pool perspective, we take the average of all stock results and use the obtained
values for the significance ranking of the hypothesized features S.
The estimated values of
three measures (p-value, ˜R2
error, and ˜R2
AUC) for the four models (LR, SVM, RF, and DCNN)
are presented in Figure 5-6. The order of the features for the last two measures ( ˜R2
error and
˜R2
AUC) are identical to the order when the features are sorted by p-value, where the significance
decreases from top to bottom in the subplots of the first column. This is for convenience and
consistency in comparing the measures. As for the magnitude of ˜R2
error and ˜R2
AUC, negative
values identify which features degrade the model’s performance over time, and positive values
monitor how much the features contribute.
We illustrate the findings from two aspects, namely the consistency between the three mea-
sures and the significance of the hypothesized features. For the LR, it is obvious that the three
measures do not agree with each other, as shown by the messy shapes of the bars in Figure
5. For SVM, the same feature set is indicated as most significant by all of the measures, but
most of the features are not significant, as revealed by a negative out-of-sample ˜R2 and the
p-values being larger than 0.5. For random forest, we discover a clear gap between outper-
forming and underperforming features, which is consistent for the three measures. There is a
great discrepancy between the good and the bad, further demonstrating that the random forest
has distinct preferences for features. For DCNN, both the consistency of measures and the
significance of features perform well to a certain extent. In line with the order obtained by the
p-values, the decreasing characteristics from top to bottom of the out-of-sample ˜R2 are evident.
We can identify several important feature sets through small p-values and large positive values
for ˜R2
error and ˜R2
AUC. The importance of three combined feature sets ({234, 134, 124}) is par-
ticularly prominent under DCNN, probably because this model has excellent processing ability
for high-dimensional data.
The aim of the above analysis is to explore the meaning of features relative to the same
original model and to rank them according to the measures. This comparative testing does not
strictly reveal the predictive performance of these models. Therefore, we examine the original
models and perform cross-model comparisons of the prediction error, AUC scores, and signal
profits after trading. The profits are obtained by taking the signals for investment with the
12
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 13

0.0
0.2
0.4
0.6
0.8
p-value
4
34
14
134
13
123
1
124
24
3
12
234
23
2
LR
−0.06 −0.05 −0.04 −0.03 −0.02 −0.01
0.00
̃R2
error
4
34
14
134
13
123
1
124
24
3
12
234
23
2
LR
0.00
0.01
0.02
0.03
̃R2
AUC
4
34
14
134
13
123
1
124
24
3
12
234
23
2
LR
0.0
0.1
0.2
0.3
0.4
0.5
p-value
234
134
124
34
24
14
23
1
3
13
12
123
4
2
DCNN
0.000
0.002
0.004
0.006
0.008
0.010
0.012
0.014
̃R2
error
234
134
124
34
24
14
23
1
3
13
12
123
4
2
DCNN
0.000
0.00̃
0.010
0.01̃
0.020
0.02̃
̃R2
AUC
234
134
124
34
24
14
23
1
3
13
12
123
4
2
DCNN
Figure 5: Barplot of the three measures estimated for the hypothesized features under the logistic regression and
DCNN. The reference ranks are based on the left panels, labeled “p-value.”
0.0
0.1
0.2
0.3
0.4
0.5
0.6
p-value
134
13
3
2
12
123
4
24
1
23
34
234
14
124
SVM
−0.06
−0.04
−0.02
0.00
0.02
̃R2
error
134
13
3
2
12
123
4
24
1
23
34
234
14
124
SVM
−0.02
−0.01
0.00
0.01
0.02
̃R2
AUC
134
13
3
2
12
123
4
24
1
23
34
234
14
124
SVM
0.0
0.1
0.2
0.3
0.4
0.5
p-value
14
124
1
12
3
23
34
234
13
2
134
123
24
4
RF
0.00
0.25
0.50
0.75
1.00
1.25
1.50
1.75
̃R2
error
14
124
1
12
3
23
34
234
13
2
134
123
24
4
RF
−0.100
−0.075
−0.050
−0.0250.000
0.025
0.050
̃R2
AUC
14
124
1
12
3
23
34
234
13
2
134
123
24
4
RF
Figure 6: Barplot of three measures estimated for the hypothesized features under traditional ML models (SVM
and random forest). The reference ranks are based on the left panels, labeled “p-value.”
13
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 14

same tick-by-tick trading strategy proposed in Yin & Wong (2022), with details provided in
Appendix C. The unit of profit is basis points (bps). In contrast to the four models that utilize
features, the benchmark here is to estimate the signal probability in the absence of feature
information and count the ratio of each class in the training set as the predicted probability.
All of the models are tested under the same stock pool, 30 stocks, using one-pool training, and
the comparison of models is shown in Table 1.
Benchmark
LR
SVM
RF
DCNN
Mean of error
0.9123
0.8863
0.5151
0.7084
0.4508
Mean of AUC score
0.5948
0.6632
0.6497
0.6738
0.7621
Average profit per signal (bps)
-
15.63
10.10
20.86
27.43
Std of profit
-
0.0055
0.0044
0.0049
0.0046
Table 1: Performance of original models in terms of prediction error, AUC score, and signal profit after trading.
Our DCNN outperforms the other models in almost every aspect. The random forest is
the second-best model, as it is more satisfactory than LR and SVM. It is not difficult to infer
that measures such as the Sharpe ratio support the preference for DCNN. Table 1 shows the
significant differences in the ability of the models to process features and extract information.
Part of our results can be supported by the experimental comparisons and conclusions in Brown
& Mues (2012); Shin & Balasingham (2017); Couronn´e et al. (2018), where similar algorithms
are applied to classify various real data sets. In addition, Table 1 provides evidence for taking
the consistency of the measures and the significance of the features as references for the original
model performance. Although the feature testing and importance results are model-dependent,
they indicate the cross-model preference based on the shapes of the barplots presented in Figure
5-6. By measuring the feature relevance, we identify hidden patterns, including consistency and
significance, that provide explanations and support for the choice of models.
5.2. Ensemble learning
From the above results, we find that the feature importance or relevance varies greatly in
different models and measures. Based on the p-value, ˜R2
error, and ˜R2
AUC, we determine the con-
sistently most significant feature sets. Therefore, we consider an ensemble DCNN with features
from {2, 3, 4} and the random forest model trained by feature set {1, 2, 4}. It is intended to han-
dle the specific feature sets separately. Originally, ensemble systems are developed to reduce the
variability in classifier decisions and thereby increase the generalization performance, including
data sampling/selection, training member classifiers, and combining classifiers (Dietterich, 2000;
Polikar, 2012). In particular, ensemble learning can be applied to handle imbalanced data and
its generative model turns out to be superior to the separate models (Sun et al., 2015; Yijing
et al., 2016). We adopt the idea of the ensemble to exploit the significant features of each model
as an additional means of improving the predictive power.
One of the earliest and simplest yet effective ensemble-based algorithms, the bagging mech-
anism, is applied to train the DCNN and the random forest classifiers independently. However,
instead of simple majority voting or averaging, the weights for the ensemble combination are
chosen by the model performance based on validation data (t = n0, ..., n) within the training
set (t = 1, ..., n). Admittedly, this random forest model is preliminary and without advanced
settings, and its predictive power is not very stable. Therefore, we choose a quite small weight,
ω, for the ensemble in this study. Although the contribution of the random forest seems mild
compared to the DCNN model, implementing these signals improves the prediction accuracy in
terms of AUC score as well as the actual profit, as shown in Table 2.
The trained models by RF and DCNN are expressed by the functions (ˆgRF and ˆgDCNN),
respectively, and the selected features from S are denoted as XS. Unlike the masked feature
14
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 15

Z, which replaces the values with zero, we drop these useless variables and reduce the model to
fit the selected feature dimension. Then, by a specific ensemble rule, the predicted probabilities
for the inference set are given as
ˆPn+j = ωn ∗ˆgRF(X124
n+j) + (1 −ωn) ∗ˆgDCNN(X234
n+j),
j = 1, 2, ..., m,
(5.1)
where ωn = arg maxω∈Ωs([ω ∗ˆgRF + (1 −ω) ∗ˆgDCNN, Yt]n
t=n0) depending on the validation data,
Ω= [0, 1], and s(·) is the AUC score function introduced before.
Original DCNN
Original RF
Original ensemble model
Mean of error
0.4508
0.7084
0.4826
Mean of AUC score
0.7621
0.6738
0.7539
Average profit per signal (bps)
27.43
20.86
29.01
Std of profit
0.0046
0.0049
0.0047
DCNN234
RF124
Ensemble selected model
Mean of error
0.4336
0.7240
0.4424
Mean of AUC score
0.7822
0.6876
0.7825
Average profit per signal (bps)
29.87
22.21
32.98
Std of profit
0.0039
0.0037
0.0040
Table 2: Performance in terms of prediction error, AUC score, and signal profit after trading for different models.
The original DCNN and RF models are those trained using all features. DCNN234 and RF124 are trained using
selected features.
To fit the selected features XS, the models are reduced to a simpler structure with fewer
parameters and lower dimensions than the original models. Such refinements enhance the model
performance compared with the original models trained using the full feature sets. Combining
them again afterward avoids the omission of information and seeks to improve payback. The
outcomes in Table 2 indicate the improvements yielded by proper feature selection and model
ensemble techniques.
The experiments in this section provide enlightening ideas on how to
leverage the feature testing results to improve performance, especially for black-box models.
5.3. Sensitivity analysis
In previous sections, we investigated the measure consistency and feature significance for four
models. However, some settings and operations in the empirical study may influence the results;
to distinguish them from model parameters and machine hyperparameters, we refer to them
as off-machine parameters. Specifically, as a sensitivity analysis, we conduct experiments for
three off-machine parameters: the time period, data split, and stock selection. The sensitivity
analysis for the three off-machine parameters tests the robustness of the rankings determined
by the measures and helps to confirm their applicability. Because of space limitations and our
focus on black-box models, we only test the DCNN model. Thus, the following results all relate
to the DCNN.
In Section 5.1 above, we test five periods for each stock and then take the average of the
results for all stocks and all periods without distinguishing the specific time period.
These
results are considered to represent the overall performance throughout the whole testing pe-
riod. In Figure 7, we examine the results calculated from each period separately to check the
consistency between neighboring time periods. The reference ranks are taken from the third
period, indicated by the orange bars in the middle panel of Figure 7. We maintain the feature
order of this reference group for other periods for clarity. After a horizontal comparison, we
conclude that with slight and acceptable performance differences in several features, the ranking
of feature importance exhibits sufficient stability and consistency over the nearby time periods.
15
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 16

0.0
0.1
0.2
0.3
0.4
0.5
p-value
234
134
13
34
23
124
24
123
12
3
1
2
14
4
Period 1
0.0
0.1
0.2
0.3
0.4
0.5
p-value
234
134
13
34
23
124
24
123
12
3
1
2
14
4
Period 2
0.0
0.1
0.2
0.3
0.4
p-value
234
134
13
34
23
124
24
123
12
3
1
2
14
4
Period 3
0.0
0.1
0.2
0.3
0.4
0.5
p-value
234
134
13
34
23
124
24
123
12
3
1
2
14
4
Period 4
0.0
0.1
0.2
0.3
0.4
0.5
p-value
234
134
13
34
23
124
24
123
12
3
1
2
14
4
Period 5
0.00
0.01
0.02
0.03
̃R2
error
2
4
12
3
1
14
24
123
23
13
124
34
134
234
0.000
0.005
0.010
0.015
0.020
̃R2
error
2
4
12
3
1
14
24
123
23
13
124
34
134
234
0.000 0.005 0.010 0.015 0.020 0.025
̃R2
error
2
4
12
3
1
14
24
123
23
13
124
34
134
234
0.000 0.002 0.004 0.00̃ 0.008 0.010
̃R2
error
2
4
12
3
1
14
24
123
23
13
124
34
134
234
0.000
0.005
0.010
0.015
0.020
̃R2
error
2
4
12
3
1
14
24
123
23
13
124
34
134
234
0.00
0.01
0.02
0.03
0.04
̃R2
AUC
12
2
14
4
1
24
124
3
23
123
13
34
134
234
0.00
0.01
0.02
0.03
0.04
̃R2
AUC
12
2
14
4
1
24
124
3
23
123
13
34
134
234
0.00
0.01
0.02
0.03
̃R2
AUC
12
2
14
4
1
24
124
3
23
123
13
34
134
234
0.000 0.005 0.010 0.015 0.020
̃R2
AUC
12
2
14
4
1
24
124
3
23
123
13
34
134
234
0.00
0.01
0.02
0.03
̃R2
AUC
12
2
14
4
1
24
124
3
23
123
13
34
134
234
Figure 7: Barplot of three measures estimated for hypothesized features under DCNN over five periods. The
reference ranks are from the middle orange panels, labeled “period 3.”
The second analysis is related to the data split. Instead of dividing the data into five periods
as in Section 5.1, what will happen if we simply test the entire long period? Will the ranking
be greatly affected? To answer these questions, we estimate the values of the three measures
over the whole period, shown by the gray bars in Figure 7, and compare them with the previous
results, indicated by the orange bars in Figure 5. The results, shown in Figure 8, suggest that
the significance test is not sensitive to the data splitting. Although the exact values of the two
methods differ from each other, they give similar rankings of features.
0.0
0.2
0.4
p-value
234
134
124
34
24
14
23
1
3
13
12
123
4
2
Split
0.0
0.2
0.4
0.6
p-value
234
134
124
34
24
14
23
1
3
13
12
123
4
2
No split
0.000
0.005
0.010
0.015
̃R2
error
4
2
3
13
12
123
1
23
34
24
14
134
124
234
Split
−0.01
0.00
0.01
0.02
0.03
̃R2
error
4
2
3
13
12
123
1
23
34
24
14
134
124
234
Nõsplit
0.00
0.01
0.02
̃R2
AUC
4
2
1
12
14
3
24
23
13
124
123
34
134
234
Split
0.00
0.02
̃R2
AUC
4
2
1
12
14
3
24
23
13
124
123
34
134
234
Nõsplit
Figure 8: Barplot of three measures estimated for hypothesized features under DCNN using two calculation
methods. “Split” indicates the average from testing five periods and “no split” indicates testing with the five
periods combined. The reference ranks are from the orange panels, labeled “split.”
We conduct another sensitivity analysis on the effect of stock selection on feature ranking.
We randomly select another 30 stocks as a pool to compare with the stock pool tested earlier in
Section 5.1. All of the other settings remain the same. The feature testing indicates robustness,
16
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 17

as shown in Figure 9, where the two colors denote the two stock pools and the reference order
is taken from the orange panels labeled “split.”
0.0
0.2
0.4
p-value
234
134
124
34
24
14
23
1
3
13
12
123
4
2
Stock pool 1
0.0
0.2
0.4
p-value
234
134
124
34
24
14
23
1
3
13
12
123
4
2
Stock pool 2
0.000
0.005
0.010
0.015
̃R2
error
4
2
3
13
12
123
1
23
34
24
14
134
124
234
Stock pool 1
0.00
0.01
0.02
0.03
̃R2
error
4
2
3
13
12
123
1
23
34
24
14
134
124
234
Stock pool 2
0.00
0.01
0.02
̃R2
AUC
4
2
1
12
14
3
24
23
13
124
123
34
134
234
Stock pool 1
0.00
0.01
0.02
0.03
0.04
̃R2
AUC
4
2
1
12
14
3
24
23
13
124
123
34
134
234
Stock pool 2
Figure 9: Barplot of three measures estimated for the hypothesized features under DCNN for two groups of
stocks. “Stock pool 1” contains 30 stocks, studied in Section 5.1, and “stock pool 2” contains 30 other random
stocks. The reference ranks are from the orange panels, labeled “stock pool 1.”
The experiments enhance our confidence in the results and provide support for the applica-
tion of these statistics to test a vast number of features under black-box models. Off-machine
parameters, including the time period, data split, and stock selection, do not greatly affect the
rankings. The robustness indicates the feasibility of using the approach in a wide range of areas
in practice and shows that it is reasonable to estimate these values for ranking features, espe-
cially for complex deep learning models. Moreover, the hidden black-box information revealed
by the results is convincing and worth exploiting for model improvement.
6. Conclusion
This paper provides three statistical measures to test feature relevance using black-box
models with an integral investigation of LOB trading. We conduct significance tests for four
representative feature sets and their combinations using a classic statistical model, traditional
ML models, and an advanced deep learning model, the DCNN. The empirical study of LOB
trading on the Chinese A-share market indicates that the consistency of the measures and the
significance of the features vary across the models and are correlated with algorithm perfor-
mance. In particular, under the DCNN, features have consistent rankings by measures, and
most are committed to forecasting accuracy. Extended experiments, including ensemble learn-
ing for model improvement and sensitivity analyses for off-machine parameters, emphasize the
benefits of explaining features and encourage the utilization of the proposed measures.
Appendix A. Details of the labeling
The labeling for the trading actions follows Yin & Wong (2022); see Section 2.3 therein. We
briefly illustrate the main idea here. The approximate wealth change for a short signal is given
as
cshort
t
≜





2 −β,
if t < min S < min{ ¯S, t + ∆},
2 −¯α,
if t < min ¯S < min{S, t + ∆},
2pb(t)−mins∈[t,t+∆] pa(s)
pb(t)
,
if S = ¯S = ∅,
(A.1)
where S := {s ∈[t, t + ∆] : pa(s) < βpb(t)}, ¯S := {s ∈[t, t + ∆] : pa(s) > ¯αpb(t)}, ¯α, and β
are hyperparameters for stopping early. ∆is the length of the limited holding time and can be
set at 1, 2, or more minutes by traders. Conversely, the approximate wealth change for a long
signal is given by
clong
t
≜





¯β,
if t < min S′ < min{ ¯S′, t + ∆},
α,
if t < min ¯S′ < min{S′, t + ∆},
maxs∈[t,t+∆] pb(s)
pa(t)
,
if S′ = ¯S′ = ∅,
(A.2)
17
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 18

where S′ := {s ∈[t, t + ∆] : pb(s) > ¯βpa(t)} and ¯S′ := {s ∈[t, t + ∆] : pb(s) < αpa(t)} with
hyperparameters α and ¯β.
Based on the approximate wealth returns for long and short signals, the labels of the three
corresponding trading actions are
lt =





+1,
if clong
t
> max{cshort
t
, ϵ},
−1,
if cshort
t
> max{clong
t
, ϵ},
0,
o.w. ,
(A.3)
where ϵ is the threshold for checking the strength of signals. In the above equation, +1 denotes
taking the long position, –1 denotes taking the short position, and 0 denotes doing nothing at
the current time t. Thus, a larger (smaller) ϵ denotes a more (less) stringent signal screening.
Yin & Wong (2022) provide an approach to determine the values of the hyperparameters, ¯α, α,
¯β, and β based on historical bid–ask spreads from the training and validation datasets.
Appendix B. Details of the submodel DCNN1
Module
Layer (options)
Output shape
Number of parameters
Input
[(None, 50, 40, 1)]
-
Convolutional
layers
Conv2D (1×2@16, stride=1×2)
(None, 50, 20, 16)
48
Conv2D (5×1@16)
(None, 50, 20, 16)
1296
Conv2D (1×2@16, stride=1×2)
(None, 50, 10, 16)
528
Conv2D (5×1@16)
(None, 50, 10, 16)
1296
Conv2D (1×10@16)
(None, 50, 1, 16)
2576
Conv2D (5×1@16)
(None, 50, 1, 16)
1296
Inception module
Conv2D (1×1@16)
Conv2D (1×1@16)
MaxPooling2D(3×1)
Conv2D (3×1@16)
Conv2D (5×1@16)
Conv2D (1×1@16)
Filter concatenation
(None, 50, 1, 48)
2896
-
Reshape and Dropout
(None, 50, 48)
0
Table B.3: Summary of the DCNN submodel (DCNN1) structure designed for learning the feature set x1, raw
limit order book.
Details on the hyperparameters: the optimizer is the adaptive moment estimation algorithm
(ADAM) with default parameters β1 = 0.9 and β2 = 0.999 from Kingma & Ba (2014); the batch
size is 128; the learning rate is 0.01; and the activation function for Conv2D is LeakyReLU with
a negative slope coefficient of α = 0.01.
Appendix C. Details of the trading strategy
Figure C.10 illustrates the procedure for converting the signal predictions into trading ac-
tions. The trading strategy involves practical concerns and risk control.
18
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 19

Figure C.10: The tick-by-tick trading strategy for exploiting signal predictions to update the account position.
References
Apley, D. W. & Zhu, J. (2020).
Visualizing the effects of predictor variables in black box
supervised learning models. Journal of the Royal Statistical Society: Series B (Statistical
Methodology), 82(4), 1059–1086.
Bastos, J. A. & Matos, S. M. (2022). Explainable models of credit losses. European Journal of
Operational Research, 301(1), 386–394.
Breiman, L. (2001). Random forests. Machine Learning, 45(1), 5–32.
Briola, A., Turiel, J., & Aste, T. (2020).
Deep learning modeling of limit order book: A
comparative perspective. arXiv preprint arXiv:2007.07319.
Brown, I. & Mues, C. (2012).
An experimental comparison of classification algorithms for
imbalanced credit scoring data sets. Expert Systems with Applications, 39(3), 3446–3453.
Bussmann, N., Giudici, P., Marinelli, D., & Papenbrock, J. (2021). Explainable machine learning
in credit risk management. Computational Economics, 57(1), 203–216.
Candes, E., Fan, Y., Janson, L., & Lv, J. (2018). Panning for gold: ‘model-x’ knockoffs for high
dimensional controlled variable selection. Journal of the Royal Statistical Society: Series B
(Statistical Methodology), 80(3), 551–577.
Chong, E., Han, C., & Park, F. C. (2017). Deep learning networks for stock market analysis
and prediction: Methodology, data representations, and case studies. Expert Systems with
Applications, 83, 187–205.
Cont, R., Cucuringu, M., & Zhang, C. (2021). Price impact of order flow imbalance: Multi-level,
cross-sectional and forecasting. Cross-sectional and Forecasting (December 25, 2021).
Cont, R., Kukanov, A., & Stoikov, S. (2014). The price impact of order book events. Journal
of Financial Econometrics, 12(1), 47–88.
Cortes, C. & Vapnik, V. (1995). Support-vector networks. Machine Learning, 20(3), 273–297.
Couronn´e, R., Probst, P., & Boulesteix, A.-L. (2018). Random forest versus logistic regression:
a large-scale benchmark experiment. BMC Bioinformatics, 19(1), 1–14.
Dai, B., Shen, X., & Pan, W. (2022). Significance tests of feature relevance for a black-box
learner. IEEE Transactions on Neural Networks and Learning Systems, 1–14.
19
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 20

Dietterich, T. G. (2000). Ensemble methods in machine learning. In International Workshop
on Multiple Classifier Systems, (pp. 1–15). Springer.
Flach, P. A., Hern´andez-Orallo, J., & Ramirez, C. F. (2011). A coherent interpretation of AUC
as a measure of aggregated classification performance. In Proceedings of the 28th International
Conference on Machine Learning (ICML-11).
Gu, S., Kelly, B., & Xiu, D. (2020). Empirical asset pricing via machine learning. The Review
of Financial Studies, 33(5), 2223–2273.
Hanley, J. A. & McNeil, B. J. (1983). A method of comparing the areas under receiver operating
characteristic curves derived from the same cases. Radiology, 148(3), 839–843.
He, H. & Garcia, E. A. (2009). Learning from imbalanced data. IEEE Transactions on Knowl-
edge and Data Engineering, 21(9), 1263–1284.
Horel, E. & Giesecke, K. (2020). Significance tests for neural networks. Journal of Machine
Learning Research, 21(227), 1–29.
Huang, J. & Ling, C. X. (2005). Using AUC and accuracy in evaluating learning algorithms.
IEEE Transactions on Knowledge and Data Engineering, 17(3), 299–310.
Huynh-Thu, V. A., Saeys, Y., Wehenkel, L., & Geurts, P. (2012). Statistical interpretation of
machine learning-based feature importance scores for biomarker discovery. Bioinformatics,
28(13), 1766–1774.
Kellner, R., Nagl, M., & R¨osch, D. (2022). Opening the black box – Quantile neural networks
for loss given default prediction. Journal of Banking & Finance, 134, 106334.
Kercheval, A. N. & Zhang, Y. (2015). Modelling high-frequency limit order book dynamics with
support vector machines. Quantitative Finance, 15(8), 1315–1329.
Kingma, D. P. & Ba, J. (2014). Adam: A method for stochastic optimization. arXiv preprint
arXiv:1412.6980.
Kolm, P. N., Turiel, J., & Westray, N. (2021). Deep order flow imbalance: Extracting alpha at
multiple horizons from the limit order book. Available at SSRN 3900141.
Lapuschkin, S., W¨aldchen, S., Binder, A., Montavon, G., Samek, W., & M¨uller, K.-R. (2019).
Unmasking Clever Hans predictors and assessing what machines really learn. Nature Com-
munications, 10(1), 1–8.
Leippold, M., Wang, Q., & Zhou, W. (2022). Machine learning in the Chinese stock market.
Journal of Financial Economics, 145(2), 64–82.
Lin, T.-Y., Goyal, P., Girshick, R., He, K., & Doll´ar, P. (2017). Focal loss for dense object
detection. In Proceedings of the IEEE International Conference on Computer Vision, (pp.
2980–2988).
Long, W., Lu, Z., & Cui, L. (2019). Deep learning-based feature engineering for stock price
movement prediction. Knowledge-Based Systems, 164, 163–173.
Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., Katz, R., Him-
melfarb, J., Bansal, N., & Lee, S.-I. (2020). From local explanations to global understanding
with explainable AI for trees. Nature Machine Intelligence, 2(1), 56–67.
Lundberg, S. M. & Lee, S.-I. (2017). A unified approach to interpreting model predictions.
Advances in Neural Information Processing Systems, 30.
20
Electronic copy available at: https://ssrn.com/abstract=4226309


## Page 21

Nousi, P., Tsantekidis, A., Passalis, N., Ntakaris, A., Kanniainen, J., Tefas, A., Gabbouj, M., &
Iosifidis, A. (2019). Machine learning for forecasting mid-price movements using limit order
book data. IEEE Access, 7, 64722–64736.
Ntakaris, A., Mirone, G., Kanniainen, J., Gabbouj, M., & Iosifidis, A. (2019). Feature engi-
neering for mid-price prediction with deep learning. IEEE Access, 7, 82390–82412.
Peng, Y., Albuquerque, P. H. M., Kimura, H., & Saavedra, C. A. P. B. (2021). Feature selec-
tion and deep neural networks for stock price direction forecasting using technical analysis
indicators. Machine Learning with Applications, 5, 100060.
Polikar, R. (2012). Ensemble learning. In Ensemble Machine Learning (pp. 1–34). Springer.
Shin, Y. & Balasingham, I. (2017). Comparison of hand-craft feature based SVM and CNN based
deep learning framework for automatic polyp classification. In 2017 39th Annual International
Conference of the IEEE Engineering in Medicine and Biology Society (EMBC), (pp. 3277–
3280).
Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., & Salakhutdinov, R. (2014). Dropout:
A simple way to prevent neural networks from overfitting.
Journal of Machine Learning
Research, 15(1), 1929–1958.
Sun, Z., Song, Q., Zhu, X., Sun, H., Xu, B., & Zhou, Y. (2015). A novel ensemble method for
classifying imbalanced data. Pattern Recognition, 48(5), 1623–1637.
Tansey, W., Veitch, V., Zhang, H., Rabadan, R., & Blei, D. M. (2018). The holdout random-
ization test: Principled and easy black box feature selection. arXiv e-prints, arXiv–1811.
Tibshirani, R. (1996). Regression shrinkage and selection via the lasso. Journal of the Royal
Statistical Society: Series B (Methodological), 58(1), 267–288.
Tsantekidis, A., Passalis, N., Tefas, A., Kanniainen, J., Gabbouj, M., & Iosifidis, A. (2020).
Using deep learning for price prediction by exploiting stationary limit order book features.
Applied Soft Computing, 93, 106401.
Yijing, L., Haixiang, G., Xiao, L., Yanan, L., & Jinling, L. (2016). Adapted ensemble clas-
sification algorithm based on multiple classifier system and feature selection for classifying
multi-class imbalanced data. Knowledge-Based Systems, 94, 88–104.
Yin, J. & Wong, H. Y. (2022). Deep LOB trading: Half a second please! Revision in Expert
Systems with Applications.
Zhang, Z., Zohren, S., & Roberts, S. (2019). Deeplob: Deep convolutional neural networks for
limit order books. IEEE Transactions on Signal Processing, 67(11), 3001–3012.
Zhu, B., Yang, W., Wang, H., & Yuan, Y. (2018). A hybrid deep learning model for consumer
credit scoring.
In 2018 International Conference on Artificial Intelligence and Big Data
(ICAIBD), (pp. 205–208).
21
Electronic copy available at: https://ssrn.com/abstract=4226309


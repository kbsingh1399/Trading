# Using Machines to Advance Better Models of the

- **Source File**: `ssrn-4986862.pdf`
- **Total Pages**: 48
- **SSRN ID**: `ssrn-4986862`

---


### Page 1

Using Machines to Advance Better Models of the
Crypto Return Cross-Section*
Gurdip Bakshi†
Xiaohui Gao‡
Zhaowei Zhang§
October 12, 2024
Abstract
Our analysis of the crypto market is centered around three questions: (i) What factors can ex-
plain the performance of different crypto portfolios? (ii) Which of these factors can be considered
as priced risk factors? (iii) Can these factors help explain the observed average returns? We
propose a cross-section approach that considers 33 portfolios and 13 factors based on multiple
characteristics. By utilizing machine-learning techniques, we test and develop new models, while
also addressing challenges such as the complex relationships between characteristics, the num-
ber of factors, the presence of similar characteristics, and the relevance of selecting factors with
economic signiﬁcance.
Keywords: Cryptos, machines, estimations, model selection, average crypto returns,
cross-sectional pricing errors
JEL classiﬁcation codes: G12, G13, G14, G24, G32.
*First draft: April 2024. All computer codes are available from the authors. We thank Connie Mao, Oleg
Rytchkov, and Sam Rosen for their feedback. Seminar participants at Temple University provided many useful
suggestions.
†Fox School of Business, Temple University, Philadelphia, PA 19122. Email: gurdip.bakshi@temple.edu
‡Fox School of Business, Temple University, Philadelphia, PA 19122. Email: xiaohui.gao.bakshi@temple.edu
§Fox School of Business, Temple University, Philadelphia, PA 19122. Email: zhaowei.zhang@temple.edu


### Page 2

1. Introduction
Our contribution is to introduce a reliable factor model for evaluating expected returns in
the crypto market. This version builds upon benchmarks for understanding the cross-section of
crypto returns. Our model, called the crypto-eight-factor model, captures the essence of the cross-
section of crypto returns. Not only does it provide a more accurate measure of expected crypto
returns, but it also offers a conceptual framework that explains a wide range of potential ﬁndings
in a cohesive manner. A challenge in asset pricing is to construct models that can explain the
cross-section of expected crypto asset returns.
Many studies in ﬁnancial economics focus on identifying factors that drive market ﬂuctuations
based on theories. However, we employ the commonly utilized portfolio approach to create a
practical factor model, which is advantageous due to its simplicity and the availability of returns
data. The proposed model’s strong performance, along with its intuitive economic interpretation,
makes it applicable to various practical uses such as assessing the performance of crypto-oriented
funds, measuring abnormal returns in event studies, determining expected returns for portfolio
selection, and estimating the cost of equity for capital budgeting, as well as possibly determining
risk premiums for options on crypto futures. Cryptos are still opaquely understood.
Positioning our contribution. Our inquiry on the crypto market focuses on understanding the
following aspects: (i) What are the contributing factors to the performance of different crypto
portfolios? (ii) Can any of these factors be considered as key risk factors? (iii) How do these
factors explain the average returns in the crypto market? To answer these questions, we analyze
33 portfolios (relying on 5,389 coins and tokens) and consider 13 factors based on various char-
acteristics. To overcome challenges, such as the interrelationship between characteristics, a large
number of factors, presence of similar characteristics, and relevance of selecting factors with eco-
nomic signiﬁcance, we utilize machine-learning techniques in our investigation and develop new
1


### Page 3

models. Our sample period is January 3, 2014, to January 26, 2024, with data on 525 weekly
cross-sections of 33 crypto portfolio returns.
We develop a reliable indicator of crypto returns by combining a diverse group of potential
predictors into a stochastic discount factor (SDF) representation. Our approach is able to predict
out-of-sample performance of crypto returns in a high-dimensional setting by using a method
that maximizes out-of-sample R2 using a machine-learning algorithm subject to sparsity con-
straints. While previous research has mostly focused on SDFs of the crypto market with a few
characteristics-based factors, our ﬁndings combine a large pool of potential factors to effectively
approximate the candidate SDF. We then estimate SDF loadings and factor risk premiums. Fur-
thermore, we propose test procedures for model comparisons and conduct alpha tests.
Our ﬁndings and value-added relative to the crypto literature. Based on a study conducted
by Liu, Tsyvinski, and Wu (2022), the three-factor model for characterizing crypto returns in-
cludes the overall crypto market, size, and momentum. These three factors are found to have
a signiﬁcant impact on the expected weekly returns of cryptos over January 2014 to July 2020
(339 weeks). Through their analysis, they identify ten long-short strategies based on crypto char-
acteristics. These featured strategies can be explained and understood through the lens of the
three-factor model. However, our analysis shows that an eight-factor model outperforms the
three-factor model in predicting average returns. Our empirical strategy is twofold. First, we em-
ploy a machine-learning approach that regularizes the sensitivity coefﬁcients in the excess return
regressions. Second, we employ a machine-learning approach that regularizes the SDF loadings.
Both approaches build crypto models that are shown to improving on the three-factor model.
The analysis of crypto assets in Cong, Karolyi, Tang, and Zhao (2022) focuses on value and
network adoption risk premiums in a factor-based framework. Furthermore, they present a cat-
egorization of major cryptocurrencies, allowing for an examination of token pricing both within
2


### Page 4

and across categories. Their ﬁndings reveal market segmentation in the crypto market, validat-
ing the economic functionality-based categorization, and providing insights in the pricing crypto
assets. Their empirical analysis is documented over January 2014 to January 2021 (366 weeks).
The work of Dobrynskaya and Dubrovskiy (2020) analyzes different factors that could po-
tentially inﬂuence the returns of cryptocurrencies and equities and determine which ones are re-
sponsible for driving returns and risk premiums. They ﬁnd that only downside equity market risk,
crypto size, and policy uncertainty factors consistently have signiﬁcant premiums. Their analysis
considers the sample period from January 2014 to November 2020 (356 weeks).1
Deviating from these studies, our investigation utilizes a distinct methodology. We employ
a three-stage process, starting with a minimizing criterion to determine the best set of beta co-
efﬁcients taking into account pricing errors and regularization. These optimal coefﬁcients are
then tested on a separate out-of-sample dataset to calculate the out-of-sample R2. This process is
automatized for cross-validation, where the coefﬁcients are obtained from four folds and tested
on the remaining fold, for a total of ﬁve cross-validation tests. The algorithm utilizes a range of
penalty ratios to determine the most effective pair, which maximizes the out-of-sample R2. Each
combination of factors is evaluated using this algorithm. In the second stage, we select the set of
factors that result in the highest R2. Finally, in the third stage, we compare various crypto pricing
models and estimate the SDF loadings, ultimately deducing support for an eight-factor model.
This paper highlights the importance of data characteristics in crypto asset pricing. The suc-
cess of crypto investing strategies and availability of test assets for these models relies on un-
derstanding these characteristics. Additionally, digital currencies are becoming ingrained in the
1Our research brings a unique perspective, and to better understand our contribution, it is important to consider
how we compare to previous studies. We recognize that previous research has also explored factor-based asset
pricing, but our ﬁndings highlight potential limitations in their approaches. For example, our dataset is more compre-
hensive and our consideration of multiple factors may offer a more complete view of the crypto market. Furthermore,
our model has shown better performance when compared to previous ones. By providing this context, we can explain
why studies may not have reached the same conclusion as ours, thereby emphasizing the signiﬁcance of our ﬁndings.
3


### Page 5

investing realm and increasingly more ﬁnancialized. However, the market environment post-
COVID-19 have exposed a problem of missing data in crypto markets. As a result, the ﬁndings
and techniques presented in this paper have implications beyond solely crypto pricing. The issue
of new data presents an opportunity to develop more effective models that adequately capture the
cross-section of returns in the dynamically expanding crypto market.2
Connection to recent methods in the asset pricing literature. Kozak, Nagel, and Santosh
(2020) develop an estimation approach that minimizes the Hansen and Jagannathan (1997) dis-
tance, using L1 and L2 regularization penalties. Their goal is to obtain a set of SDF loadings
that would increase out-of-sample R2
oos within a speciﬁc range of penalties. Our method, on the
other hand, focuses on obtaining a sparse representation of the SDF by eliminating redundant
traded factors in a sequential manner. Speciﬁcally, we discipline machine-learning algorithms
in conjunction with factor selection that combine minimizing the mean-squared error of many
(potentially large) factor models, cross-validation, and the R2 criterion.
To manage the abundance of factors, newly added factors are viewed with skepticism. In this
regard, Feng, Giglio, and Xiu (2020) present a model-selection technique that evaluates the im-
pact of an introduced factor on asset pricing, in comparison to a high-dimensional set of known
factors. Their work takes into consideration potential errors in model selection that can lead to
confounding results by omitting relevant variables. We supervise machine-learning alongside tra-
ditional estimation methods to highlight both statistical and economic relevance of factor models.
Research on empirical asset pricing has revealed a growing number of factors being used to
explain returns, and some of these generated factors may not accurately capture the underlying
risk sources. However, a solution has yet to be proposed that can address all of these issues, such
2For a partial list of the crypto market research, see, among others, Grifﬁn and Sham (2020), Liu and Tsyvinski
(2020), Bianchi and Babiak (2021), Zhang, Li, Xiong, and Wang (2021), John, O’Hara, and Saleh (2022), Fan, Feng,
Lu, and Tong (2023), Huang, Lin, Lu, and Sun (2023), and Cai and Zhao (2024).
4


### Page 6

as being able to handle tradable factors, the factor spectrum, misspeciﬁcation, the weak inference
problem, and providing a more valid measure of risk compared to established models. A Bayesian
method is proposed by Bryzgalova, Huang, and Julliard (2023) to understand these challenges.
Giglio and Xiu (2021) consider a three-pass approach for estimating the risk premium asso-
ciated with an observable asset factor. They use principal components of test asset returns and
additional cross-sectional and time-series regressions to identify the risk premium of the observ-
able factor. Their methodology also addresses potential measurement error in the observable
factor and can identify when a factor is spurious or otherwise irrelevant. Acknowledging the rele-
vance of many such concerns, our estimation approach accommodates the uncertainty associated
with estimating the means and covariances of the traded factors.
2. Crypto characteristics: January 3, 2014, to January 26, 2024
Since crypto assets are traded across numerous global exchanges, collecting this information
manually is impractical. We utilize coinmarketcap.com, a reputable source in the crypto market,
which compiles data from over 200 major exchanges. The dataset used in our study consists
of all actively traded cryptos listed on coinmarketcap.com as of January 26, 2024. See https:
//coinmarketcap.com/methodologyfor CoinMarketCap’s selection methodology. Our dataset
includes crypto coins and digital tokens, as both are considered tradable assets.
We begin in 2014 because it marks the start of signiﬁcant crypto trading activity. Our data
sample is composed of weekly aggregates (525 weeks), starting from Friday and ending on the
following Friday. This dataset includes the entire duration of the COVID-19 pandemic, allowing
for analysis of potential changes in crypto trading patterns before, during, and after the pandemic.
To be selected for our study, a crypto must have had complete data on its price, trading volume,
and market capitalization. No further criteria, such as a minimum market capitalization, are
5


### Page 7

imposed, as this information is already incorporated by coinmarketcap.com. We also make use of
winsorization to adjust for potential data-recording mistakes, setting the upper limit at the 99.5th
percentile for each crypto price, as well as its capitalization and volume.
Table 1 displays the changing characteristics of the crypto market. The initial sample consists
of 55 coins and three tokens in the ﬁrst weekly cycle, while the ﬁnal cycle includes 551 coins
and 4,838 tokens. There is a noticeable upward trend in the average market capitalizations of
cryptos, with coins increasing from an average of $138 million to $4.5 billion, and tokens rising
from $3.7 million to $43.6 billion. However, the average trading volume reaches its peak in 2021,
suggesting a possible shift in crypto behavior after the pandemic.
Mean circulation rates for cryptos are also shown in Table 1. The circulation rate is a measure
of the amount of crypto available for trading. A lower circulation rate indicates that a portion
of the crypto is being held back, often by the creators. The data reveals lower circulation rate
values between 2018 and 2020, with tokens consistently below those for coins. This difference
may be attributed to the nature of these assets: Coins function more like traditional currencies,
while tokens resemble non-currency assets in terms of investment characteristics.
Table 2 provides information on crypto returns by examining the excess return for each crypto.
This calculation is re,i
t+∆≡(1 + ri
t+∆) −Rrf
t+∆, where ri
t+∆=
Si
t+∆
Sit −1 and Si
t is the price of crypto
asset i at time t. Additionally, Rrf
t+∆is the gross risk-free return over Friday-to-Friday (known at
time t) and ∆= 1
52.
According to Table 2, the equal-weight excess return, which evenly averages crypto returns
across successive Friday closing values, is 3.5%. On the other hand, the value-weight excess
return, which takes into account each crypto’s market capitalization, is lower, at 1.9% per week.
The weekly volatility of the value-weight excess return is considerable, at 19.1%, implying the
high-risk nature of crypto investments.
6


### Page 8

Distinct patterns emerge when analyzing coins and tokens, each with their own unique risk
proﬁles. Value-weight tokens have an average of 3.1% excess return per week, while coins have
an average of 1.0% excess return. Additionally, tokens tend to have higher return volatility with
a weekly standard deviation of 27%, while coins have a standard deviation of 11%. The market
capitalization distribution is skewed toward the four prominent cryptos (Bitcoin, Ethereum, Rip-
ple, and Dogecoin), which make up an average of 46% of the total crypto market. Our objective
is to effectively price a variety of crypto assets by eliminating redundant factors and comparing
multiple promising models.
3. Machines and dissecting the cross-section of crypto returns
We provide a framework for analyzing asset pricing models. Through this analysis, we show
how to estimate factor risk premiums and SDF loadings, evaluate hypothesis tests, and create
conﬁdence intervals for model coefﬁcients and alphas. One aspect of our approach is that it
accounts for cases where there are multiple nonnested misspeciﬁed SDFs. In these situations, our
method can identify the dominant factor model that subsumes the effect of other models.
3.1. Estimation of crypto models and construction of factors and test assets
Asset pricing theories focus on explaining the expected returns of portfolios based on various
risk factors. In this framework, the vector of excess returns for each test portfolio, re
t+∆, comprises
the excess return of test portfolio i from t to t +∆. This depiction allows for an understanding of
the underlying drivers of portfolio returns and for the evaluation of the effectiveness of different
risk factors in explaining return cross-sections.
Consistent with established theory, we formulate the asset pricing relations, as follows:
E

mt+∆re
t+∆

= 0,
with
mt+∆= 1 −b′(ft+∆−µ).
(1)
7


### Page 9

In (1),
mt+∆represents the SDF, ft+∆a set of risk factors, and µ the factor means. The vector of
parameters, b, also appears in an SDF formulation of the pricing equation (1). These parameters
— the SDF loadings — are estimated via a generalized method of moments (GMM), as follows:
E


(1 −b′(ft+∆−µ))⊗re
t+∆
ft+∆−µ
vec((ft+∆−µ)(ft+∆−µ)′)−vec(Ωf)


= 0,
(2)
where Ωf is the variance-covariance matrix of ft+∆. We follow the methodology of studies such
as Jagannathan and Wang (2002) and Menkhoff, Sarno, Schmeling, and Schrimpf (2012). This
method allows us to incorporate the uncertainty associated with estimating the means and covari-
ances of ft+∆.
The speciﬁcation of the SDF in (1) implies that it can be represented using a beta model. In
this approach, the expected excess returns of each asset are determined by a factor risk premium
vector λ, and the asset-speciﬁc risk loadings represented by vector βi. In other words,
E

re,i
= λ′βi,
where
λ = Ωfb.
(3)
We examine results based on the one-step GMM (which uses the identity matrix as a weighting
matrix) and those based on the two-step GMM (which uses the optimal weighting matrix).
To implement the GMM estimation in (2), we analyze 13 factors, resulting in a pool of many
possible SDF models. Each factor construction is based on a long and short portfolio combina-
tion based on a characteristic. These characteristics include size, reversal, momentum, attention,
liquidity, lottery, circulation, skewness, coskewness, downside risk, upside potential, and golden
cross. See the method of the factor construction in Table 3 and the corresponding summary statis-
tics in Table 4. The long and short legs of these strategies are chosen to generate a positive average
8


### Page 10

return for each factor.
Our ﬁndings suggest that only a sparse set of these factors can be considered reliable indicators
of cross-section of crypto returns. Through our analysis, we show that there are deﬁnitive models
that stand out among all the potential combinations of factor investments. In fact, a seven- to nine-
factor model consisting of the most promising factors outperforms the three-factor benchmark due
to Liu, Tsyvinski, and Wu (2022). Speciﬁcally, their model favors market, size, and momentum.
We create a dataset of crypto portfolios for the purpose of testing crypto models and gener-
ating model representations. This dataset consists of 33 portfolios, each representing a different
segment of the crypto market based on speciﬁc characteristics. This provides a diverse and poten-
tially representative sample of the market for our analysis.3 These portfolios are based on Decile
1, Decile 5, and Decile 10 of various characteristics, encompassing size, reversal, momentum,
attention, liquidity, lottery, skewness, coskewness, downside risk, upside potential, and golden
cross. We allow for an analysis of various factors and their impact on crypto portfolios. By in-
cluding a range of portfolios, we aim to capture broad behaviors in order to draw meaningful
comparisons and inform investment strategies. The details of each test portfolio are in Table 5.
Table 4 (bottom panel) displays the correlations between the crypto factors. The results show
that there is generally low correlation among the factors, with 17 out of 78 absolute correlations
above 0.25 (indicated by bold font). This implies that the factors reﬂect distinct characteristics.
However, there are some notable correlations. The market factor (f market
t+∆) is strongly negatively
correlated with the size factor (f size
t+∆), with a coefﬁcient of −0.75, suggesting that crypto f market
t+∆is
closely linked to the size of the crypto assets being traded. Additionally, there is a strong positive
correlation of 0.75 between the attention factor (f attention
t+∆) and the liquidity factor (f
liquidity
t+∆). This
3The problem of inadequate test assets in empirical asset pricing has been examined, including recently by Bryz-
galova, Pelger, and Zhu (2024) and Giglio, Xiu, and Zhang (2024). It is crucial to select suitable test assets, as they
need to represent the underlying SDF. In line with this notion, we incorporate a wide variety of test assets, as the
appropriate selection of these assets is essential not only for assessing models but also for constructing factors.
9


### Page 11

feature indicates that attention — or interest in a particular crypto — is associated with higher
trading volume, alluding the possible impact of investor sentiment.
3.2. Nonsparse SDFs and disciplining model constructions
The concept of sparsity is frequently utilized in asset pricing, although it may not always
be explicitly acknowledged. In our scenario, we are required to estimate and assess 8,100 (=
∑13
r=3
13!
(13−r)!r!) factor models. From this perspective, sparsity refers to incorporating a limited
number of factors in an empirical model of SDF, its corresponding beta model, and underlying
time-series return representations.4
We adopt the elastic-net framework with cross-validation to initially guide the selection of the
best combinations of certain number of factors, for example, selecting eight from a list of 13 in a
model. The following problem is used to achieve sparsity in the asset pricing models:
min
β
1
2T ∥r
e,actual −fβ∥2 + ψ×w×∥β∥21 + ψ×(1 −w)
2
×∥β∥2,
(4)
where ∥· ∥indicates Frobenius norm, ∥β∥21 ≡∑13
k=1
q
∑33
i=1 β2
ki, and T is the number of time-
series observations (i.e., 525 weeks). Additionally, ψ and w align with penalty ratios. Notably,
the algorithm shrinks to LASSO (ridge) regressions when ψ = w = 1 (ψ = 1 and w = 0).
For our purposes, we employ a ﬁvefold cross-validation approach to estimate the parameters
β (along with ψ and w) subject to factor selection. Speciﬁcally, for a given set of f, ψ, and w,
the algorithm ﬁrst estimates β by solving (4). This cross-validation technique divides the dataset
into ﬁve equal-sized folds, training the model on four folds, and validating it on the remaining
fold. The accuracy of the ﬁt is assessed using the mean-squared-error on the validation fold. This
4Sparse models are often preferred because they offer a more amenable representation of expected returns and
tend to outperform more complex models in out-of-sample exercises. Additionally, sparse models are easier to
interpret and align with economic theories compared to factor models which use principal component aggregation. It
is beneﬁcial to prioritize sparsity in modeling since dense models may overﬁt and can be challenging to justify.
10


### Page 12

process is repeated ﬁve times, with each fold serving as the validation set in turn, and the average
mean-squared-error score is computed across all iterations.
Subsequently, the algorithm repeats this process over a grid of speciﬁed values for ψ and w to
identify the optimal combination that yields the highest ﬁtting accuracy. Once the optimal values
of ψ and w are determined, the algorithm resolves the minimization problem deﬁned by (4) using
the entire dataset to obtain the optimal β
optimal and the corresponding accuracy score for this given
set of factors f,
R2
elastic-net[f] ≡1 −
∥re,actual −fβ∥2
∥re,actual −¯re,actual∥2.
(5)
Next, to identify the optimal combination of factors, f, we apply the entire algorithm to every
possible combination of factors (e.g., selecting eight factors from a set of 13). We then select the
combination, fbest, that yields the highest R2
elastic-net[fbest].
We have chosen scikit-learn, a Python machine-learning library, to implement elastic net.
This particular library provides the option to generate a grid of ψ-values automatically. As such,
we need to deﬁne a list of only w-values for the calculations, such as [0.01, 0.05, 0.1, 0.2, 0.3, 0.5,
0.6, 0.7, 0.8, 0.9, 0.95, 0.99]. Various studies, including those by Freyberger, Neuhierl, and Weber
(2020), Gu, Kelly, and Xiu (2020), and Kelly and Xiu (2023), have utilized different approaches
to incorporate elastic net into their research on asset pricing.5
The resulting asset pricing models, featured in Table 6, are built upon selected nonzero β
and SDF loadings b, include ten versions of the encompassing model estimated. These models,
obtained using the elastic net (LASSO or ridge) lead to predetermined combinations of factors.
Our regularization procedures indicate that the circulation factor never passes model selection.
Additionally, the factor model most frequently comprises market (11 times), size (11 times),
5As opposed to our elastic net approach with cross-validation, Feng, Giglio, and Xiu (2020) propose a double-
selection LASSO method. Their aim is to address concerns over traditional factor selection techniques that potentially
lead to model selection errors and introduce bias through omitted variables.
11


### Page 13

lottery (11 times), momentum (nine times), reversal (nine times), downside risk (eight times),
and upside potential (eight times) factors. The essence of this selection procedure is to generate
sparsity for the returns model, while acknowledging the isomorphism between the beta model and
the corresponding SDF representation.
3.3. Cross-sectional variation in average excess returns and links to risk factors
Motivated by our evidence in Table 6, we next discipline model constructions by computing
performance statistics in Table 7 and conducting GMM estimations of SDF loadings, b, using (2).
Then we assess the effectiveness of SDF representations in explaining the variation of returns in
various crypto portfolios. By using this approach, we conduct a comparison between the various
three-factor crypto models and more complex models with up to 13 factors. Overall, our method-
ology addresses the suitability of factor models in explaining the return cross-section of crypto
portfolios. We investigate both in-sample and out-of-sample model performance.
3.3.1. A snapshot of performance across the 14 models
Table 7 summarizes the performance of different models, ranging from three factors to 13
factors. Our focus is on how adding more crypto factors affects the benchmark three-factor model
of Liu, Tsyvinski, and Wu (2022). Our results suggest a bowl-shaped pattern in the average
absolute alphas (A|α| ≡1
N ∑N
i=1|αi|), with portfolio α’s obtained from time-series regressions.
The highest A|α| is obtained by the three-factor model with market, size, and momentum, which
gradually decreases as more factors are added up to the eight-factor model. After that, we see an
increase in A|α| for the dense 13-factor model. The turning point of A|α| is 1.11%, reached by the
factor model supported by both the elastic net and ridge procedures.
The overall results show consistent evidence that the eight-factor model derived from elastic
net and ridge procedures — the crypto-eight — provides a more accurate representation of average
returns for different types of portfolios compared to alternative models. This can be seen through
12


### Page 14

various measures, such as the Hansen and Jagannathan (1997) distance measure, denoted HJ+
distance,
which shows a noticeable improvement with the eight-factor model. The “100×HJ+
distance distance”
column displays the measure, which indicates the normalized maximum pricing errors. When
considering the three-factor model, the 100×HJ+
distance is 9.92. On the other hand, the eight-factor
model has a 100×HJ+
distance of 8.88. This implies that the eight-factor model provides more precise
pricing in comparison to the three-factor model driven by market, size, and momentum.
The R2 values for the 33 excess return portfolios are calculated for each factor model spec-
iﬁcation, and the average, denoted AR2, is determined. Our results indicate that the eight-factor
model achieved a higher AR2 of 35.4% compared to the three-factor — based on market, size, and
momentum — model’s AR2 of 25.5%. This implies that the eight-factor model is more successful
in explaining the returns of various crypto portfolios. These ﬁndings highlight the effectiveness
of the sparsity approach in identifying a robust model for analyzing and predicting returns across
diverse portfolio types.
3.3.2. GMM estimation of models and economic and statistical relevance of crypto factors
Table 8 displays the estimated SDFs by ﬁrst utilizing 33 test portfolios. Return data is Friday-
to-Friday, and we obtain the b coefﬁcients through two-step GMM procedure. All models are
evaluated against the cross-section of crypto returns.
Allied to an estimated coefﬁcient are superscripts “**” (Newey and West (1987) HAC p-value
less than 0.05) and “*” (p-value between 0.05 and 0.1), which indicate the statistical signiﬁcance
of these factors in explaining the returns of the portfolios.
The analysis of results in Table 8 (Panel A) reveal that the SDF loading parameters associated
with the market, size, lottery, and downside risk factors are positive and statistically signiﬁcant,
indicating an explanatory power for these factors in the cross-section of crypto returns. The mar-
ket, size, lottery, and downside factors support positive risk premiums, suggesting that portfolios
13


### Page 15

with a higher covariance with these factors receive higher compensation.
Factors related to reversal, upside, and golden cross do not have a signiﬁcant effect on the ex-
pected returns of the portfolios in the eight-factor model. Additionally, the parameters associated
with the risk loading for these factors are also insigniﬁcant, possibly implying that these factors
do not explain a signiﬁcant amount of the variation in expected returns.
The ﬁndings of our study reveal that the three-factor model is weaker compared to alternative
multifactor models in predicting crypto returns. In particular, while the SDF loading for market
and size, and the associated factor risk premiums (λ), is signiﬁcant, the momentum factor has lost
signiﬁcance in our sample up to January 2024. Overall, our investigations show the importance
of market and size risk premiums, which suggests that market and size are signiﬁcant risk factors
that impact asset pricing.
Thus, our results show that the three-factor model, comprising market, size, and momentum
factors, cannot fully explain the cross-section of crypto returns. To explore the potential contri-
bution of other factors, we return to our two-step GMM estimation with an optimal weighting
matrix. By testing exclusion restrictions on the SDF with many factors versus various three-
factor models in Table 9, we address the issue of redundant factors. Our ﬁndings suggest that
the exclusion restrictions of (i) blottery = bskewness = bdownside = bupside = bgolden cross = 0, (ii) breversal = blottery =
bskewness = bdownside = bupside = 0, (iii) breversal = blottery = bskewness = bdownside = bupside = bgolden cross = 0, and (iv)
breversal = blottery = bdownside = bupside = 0 are statistically rejected. This indicates that additional factors,
such as lottery, skewness, downside, upside, and golden cross, have economically signiﬁcant load-
ings on the SDF and provide additional pricing ﬂexibility in explaining the cross-section of crypto
returns. The χ2 statistics for these exclusion restrictions are all 0.000, reinforcing the importance
of these additional factors in explaining crypto returns on top of these three-factor models.
We draw statistical inferences regarding models’ HJ+
distance in Table 8 (Panel C). We block-
14


### Page 16

bootstrap factors and assets jointly with replacement and compute HJ distance in each boot-
strap draw, for each model. We judge HJ+, B Model
distance
< HJ+, A model
distance
by testing against hypothesis H0 :
100 ×( HJ+, A model
distance
HJ+, B Model
distance
−1) ≥0 versus HA : 100 ×( HJ+, A model
distance
HJ+, B Model
distance
−1) < 0. We bootstrap the sample 10,000
times and compute the empirical p-value as the proportion that 100 × ( HJ+, A model
distance
HJ+, B Model
distance
−1) < 0. We
also compute the White’s heteroskedasticity-consistent one-sided p-value by running the series
of 10,000 differences on a constant. Comparing with the empirical p-value, the White’s p-value
takes into account the sizes of the differences. This investigation shows that the three-factor model
does not fare better in our comparisons than competing models.
Our conclusion of a seven- to nine-factor SDF is justiﬁed by various crypto data charac-
teristics, including extracted principal components. The test assets exhibit a sizable correlation
between the crypto market factor and the ﬁrst principal component, explaining 30.3% of the total
variation. The second principal component, which represents 9.3% of the variation, is heavily
inﬂuenced by factors such as size, momentum, reversal, lottery, and coskewness. This analysis
suggests that seven to nine factors are needed to capture a signiﬁcant portion (67.5%) of the vari-
ability observed in the 33 baseline portfolios, despite the potential for 33 principal components.
3.3.3. Average returns of crypto portfolios implied by models
Figure 1 illustrates expected return pricing error by showing the model’s pricing errors. The
errors are represented by the deviations from the 45-degree line, indicating discrepancies in the
predicted returns compared to the actual returns for some portfolios. Additionally, we calculate
the ﬁtted average returns using equation (3) and use the uncentered R2’s and mean absolute errors
(MAEOLS) measures as indicators of the model’s goodness-of-ﬁt. The MAEOLS is calculated as
(1/33)∑33
i=1|Realizedi −Fittedi|, in weekly percentage unit.
Table 10 reveals that the crypto portfolios with the smallest market capitalizations, as well as
the smallest and middle portfolios based on reversal, liquidity, and lottery are the most challenging
15


### Page 17

to accurately price using the models. Despite these difﬁculties, these portfolios hold signiﬁcant
interest from a model perspective.
Using a GLS cross-sectional uncentered R2 of 78.5% and an OLS uncentered R2 of 80.1%, it
can be concluded that the eight-factor model effectively captures a signiﬁcant portion of the cross-
sectional variation in cryptos. However, the χ2
NW tests (with N −K degrees of freedom (Cochrane
(2005, 12.2, page 237))), which show p-values of 0.00 with Newey and West’s method, indicates
that the asset pricing model is rejected for the featured 33 crypto portfolios.
3.3.4. Removing insigniﬁcant SDF loadings in crypto models worsens performance
The economic contribution of each crypto factor in explaining the cross-section of returns
can be quantiﬁed by considering the issue of potentially redundant factors from two perspectives.
First, in light of our ﬁndings from Table 8, we examine results from a restricted version of the
eight-factor model that jointly imposes zero SDF loadings on (i) size, (ii) lottery, and (iii) down-
side factors (the ones that are signiﬁcant). Our analysis shows that this restricted ﬁve-factor model
is rejected. This evidence relies on the p-values of 0.000 for the χ2(3) statistic, which indicates
that omitting these factors has a negative impact on the model’s performance. Furthermore, the
R2
GLS drops and the Hansen-Jagannathan distance increases, indicating that the eight-factor model
provides a better characterization of crypto returns compared to its nested counterparts. Therefore,
the eight-factor generalization is an appealing approach for explaining the return cross-section.
Second, Kozak, Nagel, and Santosh (2020) show that incorporating a signiﬁcant number of
factors based on equity market characteristics is essential for achieving consistent performance in
the SDF, even if the SDF loadings are not statistically signiﬁcant. Our approach ensures that only
economically relevant factors are included in the crypto SDF. The results in Table 11, notably
based on HJ+
distance, MAEOLS, and A|α|, support our contention that crypto models with a restriction
on the number of factors (eight or nine) perform worse compared to the original model with a
16


### Page 18

higher number of factors. This is done by excluding (i) reversal, (ii) skewness, (iii) upside, and
(iv) golden cross in the eight-factor model (see Panel A of Table 11), or excluding (i) upside in
the nine-factor model (see Panel B of Table 11).
In sum, this analysis highlights the value-added of incorporating a sufﬁcient number of fac-
tors in the SDF, even if their SDF loadings may not be statistically signiﬁcant. This part of our
investigation suggests that the identiﬁed factors are not spurious, but likely reﬂect true risk factors
driving crypto returns.
3.3.5. Downside risk factor and lottery factor are economically relevant
In their study, Lettau, Maggiori, and Weber (2014) demonstrate that incorporating a down-
side risk factor in addition to the market factor leads to improved pricing across traditional asset
classes. Our seven, eight, and nine factor speciﬁcations in Table 8 consistently show strong sig-
niﬁcance in both the estimated factor risk premiums and risk loadings of the SDF, indicating the
practical and statistical relevance of including a downside factor in crypto model.
The level of lottery preference in cryptos exerts an impact on model performance and behavior.
Cryptos with a higher lottery preference tend to be smaller in size and have less liquidity. They
also exhibit a stronger tendency for anomalies, such as crypto volatility. Compared to cryptos
with a lower lottery preference, those with a high preference show more pronounced returns.
This is substantiated by the signiﬁcant and positive coefﬁcients of both blottery and λlottery in Table 8,
indicating the economic relevance of the lottery factor. These ﬁndings suggest that including a
lottery factor in crypto pricing models can improve their explanatory power for these anomalies.
In summary, our study highlights the signiﬁcance of downside risk in understanding crypto
market behavior and underscores its relevance in pricing models. Our ﬁndings also suggest that
investors are drawn to lottery-style investments, prompting them to invest in highly volatile cryp-
tos, ultimately favoring their potential returns.
17


### Page 19

3.3.6. Alpha tests from the time-series regressions and spanning tests
We evaluate the performance of the models in capturing crypto returns by conducting regres-
sion analyses on the baseline test assets, i = 1,...,33. The regressions are of the form
r
e,i
t+∆= αi +
K
∑
k=1
βki × f k
t+∆+ εi
t+∆
for t = 1,...,T.
(6)
We investigate individual signiﬁcance on each αi. Additionally, we test the adequacy of the mod-
els by assessing the hypothesis that α = [α1,...,α33]′ = 0. This hypothesis of zero pricing errors
is examined using a GMM approach, where the statistic ˆα′var( ˆα)−1 ˆα follows an asymptotic
chi-square distribution with 33 degrees of freedom (Cochrane (2005, pages 233 and 234)).
The results, reported in Table 12, show that the eight-factor model can describe the returns
variation in the 33 test portfolios. In particular, 20 out of the 33 αi estimates have p-values that
exceed 0.1 and the largest (absolute) α has a value of 6.7% weekly, while the majority of α’s are
small, implying that the departures from the model are economically small. However, the p-value
of 0.00 indicates that the null hypothesis of α = 0 is rejected.
We draw the following additional conclusions. First, the βmarket coefﬁcients for crypto portfo-
lios are consistently positive and signiﬁcant, indicating that the returns of these crypto portfolios
are inﬂuenced by the general crypto market movements. Further analysis reveals that the crypto
portfolios exhibit a strong size effect, with the βsize coefﬁcients consistently positive and signiﬁ-
cant, establishing the link between crypto portfolio returns and their size. Third, while the reversal
factor does not signiﬁcantly inﬂuence the returns of portfolios sorted by size, it does explain the
returns of portfolios categorized by momentum, skewness, and upside.
This suggests that the size, reversal, and lottery factors are distinct and explain returns for
different portfolios in the time-series. This further emphasizes the usefulness of considering a
variety of distinct factors in constructing and analyzing crypto portfolios.
18


### Page 20

From a statistical perspective, the performance of the three-factor model is relatively unsatis-
factory. Although not tabulated for each crypto portfolio, the R2 values are lower (see the average
in Table 7). This is likely due to the model being incorrectly speciﬁed, as a considerable number
of αi are observed to be signiﬁcantly different from zero, indicating a lack of adequacy. Overall,
eight factors better capture the ﬂuctuations in crypto returns.
We conduct factor spanning tests by performing time-series regressions of each factor on the
baseline eight-factor model, following Fama and French (2015). The data in Table 13 imparts
key takeaways. For one, the intercepts in the regressions involving market, size, momentum,
coskewness, and downside, show p-values of 0.00. Thus, the intercepts — the returns explained
by eight factors other than itself, remain statistically signiﬁcant for ﬁve out of 13 factors, ranging
from 0.32% to 4.61% per week. For another, the intercepts for the reversal and lottery factors
manifest high p-values. However, our evidence on SDF loadings and HJ+
distance tests reveal an
economic role for both reversal and lottery. For example, the lottery factor is statistically relevant
in the presence of market and size factors in Table 8.
All in all, our analysis reveals that the eight-factor model consistently outperforms other mod-
els in explaining the crypto cross-section.6
3.3.7. Our results are favorable relative to methods that distill factors through aggregation
How does our approach with observable factors compare to an approach that distills the prin-
cipal components from the factors? In analogy to extant approaches, we decompose the SDF
speciﬁcation into two parts, as follows:
6We emphasize two comparisons. First, the models used in this study have relatively lower explanatory power
(the average R2 (AR2)) compared to equity studies such as those done by Fama and French (2015). Additionally,
the cross-sectional χ2 tests generate consistently low p-values of 0.000, indicating difﬁculties in accurately ﬁtting
the volatile returns of cryptos. This implies that certain crypto portfolio returns, particularly those related to size,
reversal, and momentum, are not adequately captured by the combination of models used in our analysis.
19


### Page 21

mt+∆=













1−b∗
market( f market
t+∆−µmarket) −
m⊥
t+∆,
| {z }
∑12
j=1 b∗
j×f
pc j
t+∆
1 −bmarket( f market
t+∆−µmarket) −bmve( mmve
t+∆−µmve).
(7)
Our ﬁndings support the effectiveness of our method versus the SDF that can be constructed
using the market and 12 orthogonalized factor components (f
pc j
t+∆for j = 1,...,12). Additionally,
here we do not identify sparsity, where a small number of portfolios and principal components
are sufﬁcient to represent the SDF, which aligns with characteristics of these portfolios. The
approach to construct
mmve
t+∆follows the ridge regularization procedure of Kozak, Nagel, and
Santosh (2020), who use principal components as factors to explain the returns of asset portfolios
in the space of equity anomalies, net of market exposure.
In essence, these developments result in SDFs that considers both the market returns and
nonmarket factors, whereby the principal components capture the majority of the variability in
the crypto returns. On the other hand,
mmve
t+∆incorporates the weighting of risk factors rank-
ordered by the estimated price of risk. To examine the dependability of our conclusions, we then
estimate both SDF speciﬁcations in equation (7) by GMM.
Table 14 allows for two conclusions. First, like other models, the p-values for the Hansen’s
J-statistics are 0.00 and the overidentifying restrictions of the models are rejected. Second, the
100×HJ+
distance obtained using the two-step (iterated) GMM are 14.90 (11.73), which, as noted from
Table 7, are higher than those from the three-factor model and the crypto-eight model. Thus, the
PC-based approaches manifest poor cross-sectional properties even though the in-sample ﬁtting
based on the R2
OLS and MAEOLS fare better, implying the possibility of overﬁtting.
In sum, our analysis survives robustness check with respect to principal components, to the
use of iterated GMM, and to the weighting of risk-factors with the highest price of risk. Our work
20


### Page 22

aligns with previous research that utilizes a broad sample of asset returns to analyze the risk-return
relationship through factor models. However, our particular emphasis is on investigating speciﬁc
aspects of these trade-offs in the crypto market.
3.3.8. Cross-sectional out-of-sample comparisons
Kozak, Nagel, and Santosh (2020) derive a Bayesian estimator of SDF loadings that entails
minimizing the Hansen-Jagannathan distance subject to L1 and L2 penalties on SDF loadings.
Our methodology does not depend on the Hansen-Jagannathan distance as a target, but rather
focuses on minimizing pricing deviations subject to the regularization of sensitivities in the re-
turn time-series regressions via elastic net, LASSO, or ridge, and cross-validation. Overall, the
two approaches share a goal of estimating the SDF but differ in their methods and underlying
regularization.
Our analysis in this section uses both cross-sectional and time-series methods to evaluate the
effectiveness of developed crypto asset pricing models through an out-of-sample approach. Our
focus is on addressing two questions: (1) Is the three-factor model less reliable in out-of-sample
exercises compared to models that regularize b or β? (2) Which type of regularization yields better
performance according to out-of-sample metrics? The performance of the eight-factor models of
the SDF in cross-sectional asset pricing is the focus of this analysis. Our aim is to determine
whether the crypto-eight model provides better performance.
Here, as advocated by Kozak, Nagel, and Santosh (2020), we utilize the same 13 factors as
test assets. In this case, the factors not only serve as the assets whose returns need to be explained
but also act as candidate factors that may become priced factors in the SDF formulation. In so
doing, we consider a statistical approach that can effectively handle a wide range of potential
crypto factors and assets, accurately determining their corresponding loadings in the SDF model.
Then we employ the models estimated in a baseline cross-section of 13 crypto portfolios to price
21


### Page 23

the larger cross-section of 33 crypto assets without the need for additional estimation of the SDF.
Table 15 shows the out-of-sample performance comparison for models. We display the 100×HJ+
distance,
while also showing MAEOLS and cross-sectional R2 values. In particular, we present results for an
eight-factor model that distill the potential factors examined with the highest seven risk loadings
along the lines of Kozak, Nagel, and Santosh (2020) — superscripted “kns” — as well as a cor-
responding two-factor characterization based on
mt+∆= 1 −bmarket( f market
t+∆−µmarket) −bmve( mmve
t+∆−
µmve), where
mmve
t+∆= b′ft+∆is constructed from the seven most pronounced risk factors.
At the center of our analysis are three conclusions. When ranking models based on their per-
formance in relation to the HJ+
distance criterion, the three-factor model consistently scores lower com-
pared to other eight-factor models. Speciﬁcally, the eight-factor model supported by elastic net
and ridge had the lowest HJ+
distance, followed by the eight-factor model based on regularizing the SDF
loadings (HJ
+,8 kns
distance). This is evidenced by the 100 ×(HJ+, 3 factor
distance
HJ+,8 factor
distance −1) and 100 ×(HJ+, 3 factor
distance
HJ+, 8 kns
distance −1) boot-
strap computed values of 8.84 and 8.85, respectively, with the White’s two-sided p-value of 0.00.
Additionally, the bootstrap p-value that tests the hypothesis that HJ+, 8 factor
distance > HJ+, 3 factor
distance has a p-value
of 0.14 implying that this eight-factor model does better than the three-factor model in 86% of
the 10,000 bootstrap draws. We further observe that the eight-factor model does slightly better
than the eight-factor model with regularized SDF loadings, as supported by 100 ×( HJ+, 8 kns
distance
HJ+, 8 factor
distance −1)
bootstrap obtained value of 0.1, with a White’s two-sided p-value of 0.08. The bootstrap p-value
for HJ+, 8 factor
distance > HJ+, 8 kns
distance is 0.54.
Our analysis also elicits the ﬁnding that the MAEOLS values are lower for the eight-factor mod-
els, contrasting higher values for the two-factor and the three-factor models (implying worsening
ﬁt). Furthermore, scoring with other metrics such as A|α| and AR2 is also better for the two eight-
factor models. Overall, our analysis is consistent with the pattern that incorporating more than
three factors into the model results in better crypto pricing.
22


### Page 24

4. Interpretation of the risk factors in the SDF speciﬁcations
The essence of the ensuing analysis is to investigate the relationship between innovation in
volatility variables, denoted ∆VOLℓ
t , and key crypto factors. Additionally, we utilize ∆VOLℓ
t to
evaluate the pricing of ten crypto characteristic-sorted portfolios that underlie the factor construc-
tion. The premise is that investors expect to be compensated for holding underperforming crypto
assets during periods of positive volatility innovation, as this indicates a high SDF.
For our analysis, the following innovations in volatility are constructed:
−∆VOLS&P 500
{t+∆}. Innovation in equity volatility. This volatility is constructed by analyzing the
ﬁve-minute returns of E-mini S&P 500 futures (Friday-to-Friday (390 observations)).
−∆VOLvix futures
{t+∆} . Innovation in VIX futures volatility. Weekly VIX volatility is constructed by
analyzing the ﬁve-minute returns of VIX futures.
−∆VOLbond
{t+∆}. Innovation in volatility of futures on 30-year Treasury bond. Weekly volatility
is constructed by analyzing the ﬁve-minute returns of Treasury bond futures.
−∆VOL
commodity
{t+∆} . Innovation in commodity index futures volatility. Weekly volatility is con-
structed by analyzing the underlying ﬁve-minute returns of commodity index futures.
−∆VOLdollar index
{t+∆} . Innovation in dollar index futures volatility. Weekly volatility is constructed
by analyzing the underlying ﬁve-minute returns of dollar index futures.
We use the method of weekly time-series regression to analyze the crypto factors, including
their long and short components, and their relationships with volatility innovations. We then
report the most pertinent results in Table 16. The regression model is as follows:
f
characteristic
t+∆
= constant + slope×∆VOLℓ
t+∆+ et+∆.
(8)
The variable ∆VOLℓ
t+∆represents the change in intraday measured volatility over t −∆and t +∆.
Overall, we interpret our ﬁndings as an indication that crypto investors require compensation
23


### Page 25

for strategies that perform poorly when the investing environment deteriorates and that positive
innovations in volatility are good proxies for such economic states. See, among others, Liew and
Vassalou (2000), Chen and Petkova (2012), and Bakshi, Gao, and Rossi (2019).
Our results reveal that the size factor is positively associated with ∆VOLbond
t+∆while the crypto
momentum factor has an inverse relation with ∆VOL
commodity
t+∆
. This pattern is also evident in the
regressions involving the short and long leg of size and momentum factor, respectively. In eco-
nomic terms, large-cap (winner) cryptos decline when bond (commodity) volatility innovation is
positive. However, the returns from going long (short) small-cap (losers) do not show a signiﬁcant
relationship with ∆VOLbond
t+∆(∆VOL
commodity
t+∆
). This ﬁnding is crucial because the size (momentum)
factor returns are tilted towards the short (long) leg. Additionally, the lottery (downside risk)
factor has a signiﬁcant positive (negative) relationship with ∆VOLdollar index
t+∆
(∆VOL
commodity
t+∆
).
Using the ﬁndings described above, we demonstrate that ﬂuctuations in commodity volatility
have a signiﬁcant impact on the SDF when using the ten-momentum portfolios as test assets.
Formalizing our analysis, we modify the speciﬁcation in (1) as follows:
mt+∆= 1 −bmarket( f
market
t+∆−µmarket) −bsize ( f
size
t+∆−µsize) −bvol (∆VOLℓ
t −µvol).
(9)
We ﬁnd that the SDF loading on ∆VOL
commodity
t+∆
is signiﬁcantly negative. Additionally, the risk
premium associated with ∆VOL
commodity
t+∆
is negative and statistically signiﬁcant, which indicates that
an increase in volatility is linked to a decrease in potential investment opportunities. These results
afﬁrm that ∆VOL
commodity
t+∆
is able to explain the variation in crypto portfolios formed on momentum.
In sum, we are able to identify a source of risk underlying crypto momentum returns.
Positive innovations in Treasury bond futures volatility, as indicated by a higher ∆VOLbond
t+∆,
are often associated with unfavorable economic states. This aspect is captured by the size factor,
which performs well when ∆VOLbond
t+∆increases. This is attributable to the returns of small cap
24


### Page 26

cryptos having a signiﬁcant negative coefﬁcient, which aligns with the positive SDF loading on
∆VOLbond
t+∆and the positive risk premiums associated with this factor. This analysis illustrates a
source of risk underlying crypto size returns.
We gather additional evidence to show that the positive innovations in commodity and bond
volatility are distinct indicators of worsening investment opportunities. We note that the ∆VOLbond
t+∆
variable has no signiﬁcant impact on the ten momentum portfolios, while ∆VOL
commodity
t+∆
is discon-
nected from the ten size portfolios.
We also investigate the impact of changes in alternative measures of return volatility, speciﬁ-
cally relating to ﬂuctuations in the dollar index volatility. While these ﬂuctuations result in a pos-
itive SDF loading based on our ten lottery and ten golden cross portfolios in GMM estimations,
there is no signiﬁcant evidence of factor risk premiums. Furthermore, when evaluating downside
risk portfolios, there is no statistically signiﬁcant factor risk premium associated with commodity
volatility innovation. Although there is a signiﬁcant SDF loading associated with ∆VOLbond
t+∆on
skewness, the risk premium linked to ∆VOLbond
t+∆is weaker compared to other volatility measures.
In essence, our analysis demonstrates that the Fama-MacBeth regressions support accurate
model pricing when incorporating dollar index volatility as a factor and the ten lottery portfolios,
as the χ2
NW p-value is 0.11. Correct pricing is also supported for the ten skewness, downside, and
golden cross portfolios when incorporating ∆VOLbond
t+∆, ∆VOL
commodity
t+∆
, and ∆VOLdollar index
t+∆
, respec-
tively. However, our analysis, including the χ2
NW test, shows that the model is unable to accurately
price the ten size and momentum portfolios, with a p-value less than 0.05.
One further observation from this analysis is that ∆VOLS&P 500
t+∆
and ∆VOLvix futures
t+∆
do not sig-
niﬁcantly inﬂuence the returns of any crypto factors. Innovations in equity volatility and VIX
volatility are likely driven by a host of developments (such as institutional investors, substitution
between stock and bond, and geopolitical risks), and may be an inadequate proxy for changes in
25


### Page 27

the investment opportunity set for crypto investors.
In summary, our novelty is to show the dimensions of risk that affect crypto factors and port-
folios. We offer an economic perspective on the crypto factors with our ﬁndings suggesting that
these factors, which are used to explain crypto cross-section, may reﬂect information about the
overall performance of the economy.
5. Conclusion
Two main aspects of our investigation are the selection of crypto test assets from various
portfolios and the development of a crypto pricing model for evaluation. The selected portfolios
consist of 33 diverse collections, while the pricing model consists of 13 crypto factors. This ap-
proach allows for efﬁcient testing and development of new nested and non-nested crypto models.
Creating cross-sections of portfolios for cryptos is an essential step in understanding their
underlying characteristics. However, the process of grouping cryptos based on their character-
istics presents a fundamental challenge. This is because it is crucial to select a diverse set of
cryptos that collectively represent the entire SDF conditioned on characteristics. The complex-
ity of dependencies among multiple characteristics, the numerous factors and portfolios that may
result, redundancy in characteristics, and the interpretability of chosen features are some of the
difﬁculties faced in this process.
To address these obstacles, our approach focuses on creating compact and informative cross-
sections of test assets based on multiple crypto characteristics. Our analysis provides support
for eight-factor models for cryptos, moving beyond the relevance of the three-factor model. Our
methods combine machine-learning algorithms in conjunction with traditional asset pricing ap-
proaches that estimate the SDF loading and assess cross-sectional pricing errors.
Asset pricing studies have made advancements in identifying characteristics that can explain
26


### Page 28

variations in expected returns. However, a limitation of this research is that it has only tested these
models on portfolios constructed from a limited number of known return predictors. As a result, it
is uncertain how well these models would perform when faced with a larger set of cross-sectional
return predictors, which is often a challenge due to the high number of variables involved. Our
study is part of a literature that uses machine learning techniques to overcome the challenges
posed by high dimensionality in asset pricing. We speciﬁcally focus on examining cross-sectional
pricing in the crypto market, both in and out-of-sample, allowing for the development of new
crypto models.
27


### Page 29

References
Bakshi, G., Gao, X., Rossi, A., 2019. Understanding the sources of risk underlying the cross
section of commodity returns. Management Science 65, 619–641.
Bali, T., Hirshleifer, D., Peng, L., Tang, Y., 2019. Attention, social interaction, and investor
attraction to lottery stocks. Working paper. Georgetown University.
Bianchi, D., Babiak, M., 2021. A factor model for cryptocurrency returns. Working paper. Lan-
caster University.
Bryzgalova, S., Huang, J., Julliard, C., 2023. Bayesian solutions for the factor zoo: We just ran
two quadrillion models. Journal of Finance 78, 487–557.
Bryzgalova, S., Pelger, M., Zhu, J., 2024. Forest through the trees: Building cross-sections of
stock returns. Journal of Finance 100, 2274–2325.
Cai, C., Zhao, R., 2024. Salience theory and cryptocurrency returns. Journal of Banking & Fi-
nance 159, 107052.
Chen, Z., Petkova, R., 2012. Does idiosyncratic volatility proxy for risk exposure?. Review of
Financial Studies 25, 2745–2787.
Cochrane, J., 2005. Asset Pricing. Princeton University Press, Princeton, NJ.
Cong, L., Karolyi, A., Tang, K., Zhao, W., 2022. Value premium, network adoption, and factor
pricing of crypto assets. Working paper. Cornell University.
Dobrynskaya, V., Dubrovskiy, M., 2020. Cryptocurrencies meet equities: Risk factors and asset
pricing relationships. Working paper. HSE School (Moscow).
Fama, E., French, K., 2015. A ﬁve-factor asset pricing model. Journal of Financial Economics
116, 1–22.
28


### Page 30

Fan, Z., Feng, J., Lu, L., Tong, X., 2023. The risk and return of cryptocurrency carry trade.
Working paper. University of Manitoba.
Feng, G., Giglio, S., Xiu, D., 2020. Taming the factor zoo. Journal of Finance 75, 1327–1370.
Freyberger, J., Neuhierl, A., Weber, M., 2020. Dissecting characteristics nonparametrically. Re-
view of Financial Studies 33, 2326–2377.
Giglio, S., Xiu, D., 2021. Asset pricing with omitted factors. Journal of Political Economy 129,
1947–1990.
Giglio, S., Xiu, D., Zhang, D., 2024. Test assets and weak factors. Journal of Finance (forthcom-
ing).
Grifﬁn, J., Sham, A., 2020. Is bitcoin really untethered?. Journal of Finance 75, 1913–1964.
Gu, S., Kelly, B., Xiu, D., 2020. Empirical asset pricing via machine learning. Review of Financial
Studies 33, 2223–2273.
Hansen, L., Jagannathan, R., 1997. Assessing speciﬁcation errors in stochastic discount factor
models. Journal of Finance 52, 557–590.
Harvey, C., Siddique, A., 2000. Conditional skewness in asset pricing tests. Journal of Finance
55, 1263–1295.
Huang, L., Lin, T.-C., Lu, F., Sun, J., 2023. The ﬁnancialization of cryptocurrencies. Working
paper. Singapore Management University.
Jagannathan, R., Wang, Z., 2002. Empirical evaluation of asset-pricing models: A comparison of
the SDF and beta methods. Journal of Finance 57, 2337–2367.
John, K., O’Hara, M., Saleh, F., 2022. Bitcoin and beyond. Annual Review of Financial Eco-
nomics 14, 95–115.
29


### Page 31

Kelly, B., Xiu, D., 2023. Financial machine learning. Working paper. Yale University and Univer-
sity of Chicago.
Kozak, S., Nagel, S., Santosh, S., 2020. Shrinking the cross section. Journal of Financial Eco-
nomics 135, 271–292.
Kumar, A., 2009. Who gambles in the stock market?. Journal of Finance 64, 1889–1933.
Lettau, M., Maggiori, M., Weber, M., 2014. Conditional risk premia in currency markets and
other asset classes. Journal of Financial Economics 1, 127–154.
Liew, J., Vassalou, M., 2000. Can book-to-market, size and momentum be risk factors that predict
economic growth?. Journal of Financial Economics 57, 221–245.
Liu, Y., Tsyvinski, A., 2020. Risks and returns of cryptocurrency. Review of Financial Studies
34, 2689–2727.
Liu, Y., Tsyvinski, A., Wu, X., 2022. Common risk factors in cryptocurrency. Journal of Finance
77, 1133–1177.
Menkhoff, L., Sarno, L., Schmeling, M., Schrimpf, A., 2012. Currency momentum strategies.
Journal of Financial Economics 106, 660–684.
Newey, W., West, K., 1987. A simple, positive semi-deﬁnite, heteroskedasticity and autocorrela-
tion consistent covariance matrix. Econometrica 55, 703–708.
Zhang, W., Li, Y., Xiong, X., Wang, P., 2021. Downside risk and the cross-section of cryptocur-
rency returns. Journal of Banking & Finance 133, 106246.
30


### Page 32

Table 1
Number, market capitalization, trading volume, and circulation rates of cryptos by year
This table describes the attributes of cryptocurrencies categorized by year. Panel A features all cryptos in our sample, whereas Panels B and C
solely comprise crypto coins and tokens, respectively. Statistics for market capitalization and trading volume are presented in U.S. dollars. The
circulation rate shows the percentage of cryptos actively circulating in the market. The data spans the time period from January 3, 2014, to January
26, 2024, constituting 525 weeks. This data is sourced from coinmarketcap.com.
Market
Trading
Circulation
cap. (million, $)
|
{z
}
volume (thousand, $)
|
{z
}
rate
|{z}
Year
Number
Mean
Mean
Mean
Panel A: Cryptos (coins and tokens), January 3, 2014, to January 26, 2024 (525 weeks)
2023
5389
39,625
16,836
0.88
2022
3494
63,626
46,796
0.82
2021
2201
8,883
126,384
0.73
2020
1274
732
96,848
0.69
2019
834
1,655
65,890
0.68
2018
624
602
28,89
0.69
2017
297
555
26,746
0.78
2016
121
89
1,079
0.94
2015
83
55
486
0.94
2014
58
131
701
0.93
Panel B: Crypto coins, January 3, 2014, to January 26, 2024 (525 weeks)
2023
551
4,532
68,061
0.87
2022
504
2,631
162,367
0.85
2021
453
3,641
307,435
0.83
2020
419
752
169,556
0.81
2019
336
940
104,634
0.81
2018
278
1,273
50,113
0.82
2017
175
829
39,740
0.88
2016
114
94
1,132
0.94
2015
78
59
516
0.94
2014
55
138
739
0.92
Panel C: Crypto tokens, January 3, 2014, to January 26, 2024 (525 weeks)
2023
4838
43,622
11,002
0.88
2022
2990
73,907
27,315
0.81
2021
1748
10,242
79,464
0.71
2020
855
722
61,217
0.64
2019
498
2,138
39,749
0.60
2018
346
63
11,848
0.58
2017
122
161
8,107
0.63
2016
7
11
217
0.95
2015
5
2
12
1.0
2014
3
4
4
1.0
31


### Page 33

Table 2
Properties of excess returns of cryptos (percentage per week)
This table includes data covering a period from January 3, 2014, to January 26, 2024, which comprises 525 weeks. The constructed data consists
of the weekly excess returns (%) for both value-weighted and equal-weighted portfolios of cryptocurrencies, as well as the excess returns of four
prominent cryptos: Bitcoin, Ethereum, Ripple, and Dogecoin. The mean, standard deviation (SD), bootstrap 90% lower and upper boundaries,
Newey and West (1987) p-values (shown as NW[p]), minimum, median, maximum, and ﬁrst-order autocorrelation coefﬁcient (shown as Acf) are
calculated. We also calculate the time-series fraction of returns that are positive, sample skewness, and sample excess kurtosis.
Mean
SD
Block
NW[p]
Min.
Median
Max.
Acf
1{r>0}
Skewness
Kurtosis
(%)
(%)
Bootstrap
(%)
(excess)
(weekly)
(weekly)
Panel A: Weekly excess returns (%) of value-weight and equal-weight portfolios
re,vwi
t+∆: Coins and tokens
1.9
19.1
⌊0.5
2.9⌋
(0.01)
-65
0.4
139
-0.27
54
1.66
10.6
re,vwi
t+∆: Coins
1.0
11.0
⌊0.2
2.0⌋
(0.06)
-68
0.5
51
0.07
54
-0.58
6.1
re,vwi
t+∆: Tokens
3.1
27.0
⌊1.0
4.7⌋
(0.01)
-70
0.0
198
-0.18
49
2.37
12.3
re,ewi
t+∆: Coins and tokens
3.5
11.6
⌊2.3
4.8⌋
(0.00)
-38
2.5
62
0.31
63
0.71
3.2
re,ewi
t+∆: Coins
3.7
11.3
⌊2.5
5.0⌋
(0.00)
-37
2.9
53
0.28
65
0.60
2.3
re,ewi
t+∆: Tokens
4.8
19.9
⌊3.1
6.6⌋
(0.00)
-70
2.5
180
0.10
58
2.81
17.7
Panel B: Weekly excess returns (%) of Bitcoin, Ethererum, Ripple, and Dogecoin
re,bitcoin
t+∆
1.2
9.8
⌊0.5
2.1⌋
(0.01)
-39
0.6
51
0.10
54
0.40
2.7
re,ethereum
t+∆
2.9
17.3
⌊1.3
4.7⌋
(0.00)
-45
0.3
142
0.08
43
2.69
16.1
re,ripple
t+∆
2.2
21.2
⌊0.4
4.4⌋
(0.06)
-52
-1.5
200
0.27
42
3.65
22.4
re,dogecoin
t+∆
3.0
25.8
⌊0.7
4.8⌋
(0.02)
-46
-0.7
252
0.06
46
5.73
49.3
32


### Page 34

Table 3
Construction of 13 factors in the crypto market
This table describes the underlying crypto-traded factors. In order to create a comprehensive view of cryptos, several features are taken into
consideration, including macroeconomic events, fundamental analysis, volatility, market sentiment, and technical indicators. First, the macroe-
conomic environment, such as economic conditions and government regulations, can impact the performance of cryptos. Second, fundamental
analysis, such as coskewness, market capitalization, momentum, and trading volume, are taken into account. Third, cryptos are known for their
high volatility and lottery features. Additionally, market sentiment, including investor speculation, can inﬂuence the direction of crypto markets.
We include the effects of speculation by using metrics like seven-day price momentum and volume. Finally, crypto markets are technical in nature,
with support and resistance levels playing a signiﬁcant role in price movements. We include technical indicators to capture market trends and
relative demand by implementing golden cross. Factors are constructed weekly over t to t +∆. The data sample spans January 3, 2014, to January
26, 2024 (total of 525 weeks). The data source is coinmarketcap.com.
Factor
Construction of the factors in the crypto market
f market
t+∆
Crypto market factor. Value-weight excess returns of all cryptos from t to t +∆.
f size
t+∆
Crypto size factor. Based on market capitalization. The size factor is calculated as the returns from a long (short)
position in the bottom (top) size group. The breakpoints are 30%, 40%, and 30%.
f reversal
t+∆
Crypto reversal factor. Cryptos are sorted based on previous four-week returns. This factor is the return of a long and
short position in losers and winners. The breakpoints are 30%, 40%, and 30%.
f momentum
t+∆
Crypto momentum factor. Cryptos are sorted based on previous seven-day returns. This factor is the return from a long
and short position in winners and losers. The breakpoints are 30%, 40%, and 30%.
f attention
t+∆
Crypto attention factor. Cryptos are sorted based on previous seven-day volume. The factor is the return of a long and
short position in low and high volume cryptos. The breakpoints are 30%, 40%, and 30%.
f liquidity
t+∆
Crypto liquidity factor. Cryptos are sorted based on previous four-week volume. The factor is the return of a long and
short position in low and high volume cryptos. The breakpoints are 30%, 40%, and 30%.
f lottery
t+∆
Crypto lottery factor. Cryptos are sorted based on the previous 30-day volatility. The factor is the return of a long and
short position in high and low volatility cryptos. The breakpoints are 30%, 40%, and 30%. For stock market evidence,
see Kumar (2009) and Bali, Hirshleifer, Peng, and Tang (2019).
f circulation
t+∆
Crypto circulation factor. Cryptos are sorted based on circulation rate. The factor is the return of a long and short
position in low and high circulation cryptos. The breakpoints are 50%, and 50%.
f skewness
t+∆
Crypto skewness factor. Cryptos are sorted based on realized skewness over the previous 30-days. The factor is the
return of a long and short position in low and high skewness cryptos. The breakpoints are 30%, 40%, and 30%.
f coskew
t+∆
Crypto coskewness factor. Cryptos are sorted based on realized coskewness (see Harvey and Siddique (2000) for equity
market evidence) over the previous 30-days. The factor is the return of a long and short position in high and low
coskewness cryptos. The breakpoints are 30%, 40%, and 30%.
f downside
t+∆
Crypto downside risk factor. Cryptos are sorted based on downside risk regression (see Lettau, Maggiori, and Weber
(2014) for equity market evidence) using previous 30-day threshold. The factor is the return of a long and short position
in low and high downside risk cryptos. The breakpoints are 30%, 40%, and 30%.
f upside
t+∆
Crypto upside potential factor. Cryptos are sorted based on upside potential regression using previous 30-day threshold.
The factor is the return of a long and short position in high and low upside potential cryptos. The breakpoints are 30%,
40%, and 30%.
f golden cross
t+∆
Crypto golden cross factor. Cryptos are sorted based on the differences between average returns in the past seven-days
with their average returns in the past 12 weeks. The factor is the return of a long and short position in low and high
categories. The breakpoints are 30%, 40%, and 30%.
33


### Page 35

Table 4
Summary statistics of the 13 crypto factors (percentage per week)
Tabulated are return summary statistics of factors created for the crypto market. The mean, standard deviation (SD), bootstrap 90% lower and
upper boundaries, Newey and West (1987) p-values, minimum, median, maximum, and ﬁrst-order autocorrelation coefﬁcient (shown as Acf) are
calculated. We also calculate the time-series fraction of returns that are positive, sample skewness, and sample excess kurtosis. Summarized also
are the pairwise correlations between factors. Absolute correlations higher than 0.25 are shown in bold. The data sample spans from January 3,
2014, to January 26, 2024 (525 weeks). The data source is coinmarketcap.com.
Factors
Mean
SD
Block
NW[p] Min. Max.
Acf
1{r>0} Skewness Kurtosis
(%)
(%)
Bootstrap
(%)
(excess)
(weekly) (weekly)
f market
t+∆
1.9
19.1
⌊0.5
2.9⌋
(0.01)
-65
139
-0.27
54
1.66
10.6
f size
t+∆: long (short) small (large) cap
2.3
20.3
⌊1.2
3.9⌋
(0.01)
-140
85
-0.18
59
-1.0
9.5
f reversal
t+∆
: long (short) four-week decliners (risers)
1.1
37.2
⌊-2.0 4.2⌋
(0.52)
-260
238
0.01
45
0.7
13.5
f momentum
t+∆
: long (short) seven-day winners (losers)
1.6
40.1
⌊-0.6 4.7⌋
(0.36)
-231
241
-0.08
54
-0.5
10.1
f attention
t+∆
: long (short) seven-day low (high) volume
3.3
36.1
⌊1.3
5.8⌋
(0.01)
-161
249
-0.12
48
2.2
12.8
f liquidity
t+∆
: long (short) four-week low (high) volume
2.8
32.2
⌊0.8
4.9⌋
(0.02)
-172
206
-0.11
50
1.1
8.1
f lottery
t+∆
: long (short) high (low) volatility
2.5
37.5
⌊-0.3 4.7⌋
(0.11)
-78
245
-0.15
41
2.2
8.8
f circulation
t+∆
: long (short) low (high) circulation
1.5
18.9
⌊0.1
2.5⌋
(0.04)
-73
139
-0.25
54
1.6
12.0
f skewness
t+∆
: long (short) low (high) skewness
1.1
28.3
⌊-1.7 3.0⌋
(0.47)
-115
224
0.07
48
2.1
13.6
f coskew
t+∆
: long (short) high (low) coskewness
3.5
29.8
⌊2.0
5.5⌋
(0.00)
-135
220
-0.07
54
1.4
10.9
f downside
t+∆
: long (short) low (high) downside
4.2
35.0
⌊1.9
6.6⌋
(0.00)
-105
195
-0.08
52
1.1
4.7
f upside
t+∆
: long (short) high (low) upside
0.7
37.6
⌊-1.3 3.8⌋
(0.66)
-233
211
-0.04
50
0.0
9.4
f golden cross
t+∆
: long (short) low (high) golden cross
1.6
38.3
⌊-1.1 3.7⌋
(0.28)
-240
214
-0.10
49
0.5
10.1
Correlation between the crypto factors
f size
t+∆
f reversal
t+∆
f momentum
t+∆
f attention
t+∆
f liquidity
t+∆
f lottery
t+∆
f circulation
t+∆
f skewness
t+∆
f coskew
t+∆
f downside
t+∆
f upside
t+∆
f golden cross
t+∆
f market
t+∆
-0.75
0.05
0.00
0.17
0.18
0.47
0.39
0.15
0.10
0.17
0.01
0.12
f size
t+∆
-0.09
0.08
-0.07
-0.06
-0.39
-0.25
-0.16
-0.12
-0.16
0.00
-0.17
f reversal
t+∆
-0.39
0.14
0.02
0.12
-0.04
0.53
0.20
-0.08
0.10
0.36
f momentum
t+∆
0.06
0.02
-0.10
0.04
-0.36
0.20
0.15
0.14
-0.72
f attention
t+∆
0.75
0.41
-0.27
0.12
0.01
0.12
-0.08
0.03
f liquidity
t+∆
0.36
-0.28
0.08
-0.10
0.11
-0.11
-0.02
f lottery
t+∆
0.12
0.23
0.12
0.07
0.05
0.16
f circulation
t+∆
0.09
0.08
0.00
-0.02
0.02
f skewness
t+∆
0.01
-0.07
-0.12
0.23
f coskew
t+∆
0.40
0.49
-0.03
f downside
t+∆
-0.08
-0.01
f upside
t+∆
-0.05


### Page 36

Table 5
Average returns of the 33 crypto test assets (percentage per week)
Tabulated are return summary statistics of test portfolios created for the crypto market. The mean, standard deviation (SD), bootstrap 90% lower
and upper boundaries, Newey and West (1987) p-values, minimum, median, maximum, and ﬁrst-order autocorrelation coefﬁcient (shown as Acf)
are calculated. We also calculate the time-series fraction of returns that are positive, sample skewness, and sample excess kurtosis. The data
sample spans from January 3, 2014, to January 26, 2024 (525 weeks).
Test
Mean
SD
Block
NW[p]
Min.
Median
Max.
Acf
1{r>0}
Skewness
Kurtosis
Assets
(%)
(%)
Bootstrap
(%)
(excess)
(weekly)
(weekly)
Size
Decile 1
9.78
21.8
⌊7.99
11.38⌋
(0.00)
-38
6.89
181
0.00
71
2.3
10.7
Decile 5
3.06
16.6
⌊1.53
4.45⌋
(0.00)
-40
0.95
141
0.23
56
2.5
15.6
Decile 10
1.92
19.2
⌊0.46
2.88⌋
(0.01)
-65
0.45
139
-0.27
54
1.7
10.6
Reversal
Decile 1
5.59
37.4
⌊2.21
8.75⌋
(0.00)
-69
-1.43
250
0.04
46
3.1
13.6
Decile 5
0.46
15.8
⌊-0.86
1.76⌋
(0.55)
-69
0.00
140
0.04
50
2.3
19.4
Decile 10
2.87
33.1
⌊0.61
5.46⌋
(0.06)
-70
-1.51
251
0.02
47
2.1
10.6
Momentum
Decile 1
3.66
35.0
⌊0.84
5.95⌋
(0.02)
-69
-1.58
251
-0.05
46
2.8
14.1
Decile 5
0.52
14.1
⌊-0.71
1.73⌋
(0.47)
-63
-0.23
78
0.15
49
0.9
6.5
Decile 10
1.44
34.9
⌊-0.98
3.86⌋
(0.34)
-70
-3.66
231
0.00
41
2.2
9.4
Attention
Decile 1
3.82
25.1
⌊1.81
5.76⌋
(0.00)
-67
0.20
173
0.03
53
2.2
9.7
Decile 5
1.10
19.4
⌊-0.61
2.74⌋
(0.27)
-65
-0.46
203
0.15
47
2.8
25.0
Decile 10
1.75
11.9
⌊0.70
2.94⌋
(0.01)
-40
0.67
101
0.28
56
2.2
15.0
Liquidity
Decile 1
4.84
24.0
⌊3.10
6.67⌋
(0.00)
-65
0.50
135
0.01
55
1.9
7.2
Decile 5
0.76
20.6
⌊-0.90
2.55⌋
(0.46)
-70
-0.64
153
0.09
46
1.7
13.4
Decile 10
2.01
14.4
⌊0.95
3.24⌋
(0.00)
-69
0.77
163
0.06
56
3.6
37.4
Lottery
Decile 1
0.70
8.9
⌊-0.04
1.48⌋
(0.11)
-37
0.15
38
0.14
52
0.2
2.6
Decile 5
1.35
18.8
⌊-0.23
3.21⌋
(0.18)
-54
-1.06
135
0.15
46
2.2
10.8
Decile 10
5.91
49.0
⌊2.28
8.86⌋
(0.00)
-70
-3.77
250
-0.16
44
2.3
7.5
Skewness
Decile 1
1.45
23.7
⌊-0.08
3.25⌋
(0.16)
-66
-0.16
238
-0.11
49
4.1
33.3
Decile 5
-0.02
17.9
⌊-1.31
1.46⌋
(0.98)
-67
-0.41
143
0.03
48
2.5
21.3
Decile 10
1.59
20.8
⌊-0.24
3.49⌋
(0.15)
-70
-0.34
120
0.17
48
1.4
7.1
Coskew
Decile 1
0.49
21.9
⌊-0.90
2.23⌋
(0.61)
-70
-0.69
185
0.06
46
2.5
19.1
Decile 5
2.26
20.3
⌊0.59
3.99⌋
(0.02)
-54
-0.34
152
0.01
49
2.6
12.8
Decile 10
3.03
25.3
⌊0.98
4.97⌋
(0.01)
-70
-0.96
220
0.03
46
2.8
16.2
Downside
Decile 1
5.20
38.0
⌊2.50
8.17⌋
(0.00)
-70
-2.46
248
-0.10
46
2.3
8.5
Decile 5
1.14
15.8
⌊0.00
2.57⌋
(0.14)
-43
-0.15
198
0.09
49
5.1
55.2
Decile 10
1.58
35.0
⌊-0.98
3.73⌋
(0.27)
-69
-1.59
237
-0.07
44
2.7
13.4
Upside
Decile 1
1.88
35.0
⌊-0.82
3.91⌋
(0.21)
-70
-2.46
211
-0.04
44
2.2
8.8
Decile 5
0.88
13.1
⌊-0.23
1.81⌋
(0.16)
-69
0.25
126
0.05
52
1.5
18.5
Decile 10
1.42
33.8
⌊-0.90
3.86⌋
(0.32)
-70
-2.69
248
-0.04
43
2.9
14.1
Golden Cross
Decile 1
4.06
34.7
⌊1.28
6.37⌋
(0.01)
-69
-0.74
247
-0.10
46
2.9
13.3
Decile 5
1.55
16.3
⌊0.12
3.05⌋
(0.07)
-53
0.03
133
0.14
50
2.5
16.8
Decile 10
0.26
31.5
⌊-1.83
2.97⌋
(0.86)
-70
-2.78
243
0.00
40
2.2
11.5
35


### Page 37

Table 6
Factors selected by the machine-learning algorithm and cross-validation
In this table, we present the results from the factor selection exercise. For a dense multifactor asset pricing model, we minimize the regularized
objective associated with (4), that is, LASSO, ridge, and elastic net. We adopt a ﬁvefold cross-validation approach to estimate the parameters of
the model. Then, we select the combination, fbest, that achieves the highest R2
elastic-net[fbest] in equation (5). The circulation factor is never selected
by the machine-learning algorithm. In the case of the three-factor model derived from elastic net, LASSO, and ridge, for example, only the β
coefﬁcients associated with market, size, and lottery are nonzero, while all other β coefﬁcients are equal to zero.
K
Factors
Method
f market
t+∆
f size
t+∆f reversal
t+∆
f momentum
t+∆
f attention
t+∆
f liquidity
t+∆
f lottery
t+∆
f skewness
t+∆
f coskew
t+∆
f downside
t+∆
f upside
t+∆
f golden cross
t+∆
12
Elastic net, LASSO, ridge
✓
✓
✓
✓
✓
✓
✓
✓
✓
✓
✓
✓
11
Elastic net, LASSO, ridge
✓
✓
✓
✓
✓
✓
✓
✓
✓
✓
✓
10
Elastic net, LASSO, ridge
✓
✓
✓
✓
✓
✓
✓
✓
✓
✓
9
Elastic net, LASSO, ridge
✓
✓
✓
✓
✓
✓
✓
✓
✓
8
Elastic net, ridge
✓
✓
✓
✓
✓
✓
✓
✓
8
LASSO
✓
✓
✓
✓
✓
✓
✓
✓
7
Elastic net, LASSO, ridge
✓
✓
✓
✓
✓
✓
✓
6
Elastic net, LASSO, ridge
✓
✓
✓
✓
✓
✓
5
Elastic net, LASSO, ridge
✓
✓
✓
✓
✓
✓
4
Elastic net, LASSO, ridge
✓
✓
✓
✓
3
Elastic net, LASSO, ridge
✓
✓
✓
How often?
11
11
9
9
1
2
11
6
3
8
8
5
36


### Page 38

Table 7
Performance of models selected by the machine-learning algorithm with ﬁvefold cross-
validation
This table assesses the effectiveness of factor models in explaining monthly excess returns on various crypro portfo-
lios. The 33 portfolios are classiﬁed by characteristics. We show (i) the average absolute intercept value, (ii) the ratio
of average absolute alpha to the average demeaned return on portfolio, and (iii) the GRS statistic determining if the
intercept estimates are signiﬁcantly different from zero. The two columns for “Alphas” are based on the correspond-
ing calculation in Fama and French (2015, Table 5). We show the average adjusted R2 from the 33 portfolios as AR2.
Additionally, we show the Hansen and Jagannathan (1997) distance with identity matrix (Cochrane (2005)).
Alphas
GRS
K factors
Supporting
A|α|
A|α|
A|r|
AR2
stat.
p-value
HJ+
distance
Method
(%)
(%)
(%)
×100
(weekly)
13 factors
Dense model
1.13
72.4
37.6
3.75
0.00
16.46
12 factors
Elastic net, LASSO, ridge
1.13
72.5
37.2
3.74
0.00
12.71
11 factors
Elastic net, LASSO, ridge
1.13
72.5
37.0
3.74
0.00
14.26
10 factors
Elastic net, LASSO, ridge
1.13
72.6
36.2
3.76
0.00
9.95
9 factors
Elastic net, LASSO, ridge
1.16
74.1
35.9
3.81
0.00
9.14
8 factors
Elastic net, ridge
1.11
70.9
35.4
3.87
0.00
8.88
8 factors
LASSO
1.21
77.7
35.3
3.95
0.00
9.24
7 factors
Elastic net, LASSO, ridge
1.22
78.1
34.5
3.95
0.00
9.22
6 factors
Elastic net, LASSO, ridge
1.37
87.6
32.8
4.20
0.00
9.53
5 factors
Elastic net, LASSO, ridge
1.37
87.6
31.1
4.14
0.00
9.53
4 factors
Elastic net, LASSO, ridge
1.35
86.7
29.2
4.13
0.00
9.52
3 factors
Elastic net, LASSO, ridge
1.33
85.4
26.1
4.12
0.00
9.85
3 factors
market, size, reversal
1.36
87.5
25.3
4.09
0.00
10.30
3 factors
market, size, momentum
1.40
89.8
25.5
4.10
0.00
9.92
37


### Page 39

Table 8
Cross-sectional pricing results of best models selected by the machine-learning algorithm
with ﬁvefold cross-validation
The following table displays the estimated factor risk premiums and SDF loadings using alternative models derived from the analysis in Table 7.
The results are based on an eight-factor model, and we also present results from an expanded nine-factor model and a restricted seven-factor
model. The estimations are conducted using a two-step GMM method on a dataset over the sample period of January 3, 2014, to January 26, 2024
(covering 525 weeks). The level of signiﬁcance is superscripted by ** if the p-value is lower than 0.05, and * if the p-value is between 0.05 and
0.10. χ2
NW represents the test of whether all pricing errors are zero (Cochrane (2005, 12.2, page 237)) and is distributed χ2
N−K, where K is the
number of factors. We determine the goodness-of-ﬁt using both the uncentered R2 and the MAEOLS as metrics.
Panel A: Model estimation results
Eight-factor models
Nine-factor model
Seven-factor model
Three-factor model
Method
Elastic net, ridge
|
{z
}
LASSO
| {z }
Elastic net, LASSO, ridge
|
{z
}
Elastic net, LASSO, ridge
|
{z
}
market, size, momentum
|
{z
}
SDF
Factor
SDF
Factor
SDF
Factor
SDF
Factor
SDF
Factor
Loading Premium Loading Premium
Loading
Premium
Loading
Premium
Loading
Premium
b
λ
b
λ
b
λ
b
λ
b
λ
×100
×100
×100
×100
×100
f market
t+∆
2.11**
6.96**
2.05**
7.22**
1.96**
6.93**
2.09**
6.71**
2.67**
6.49**
f size
t+∆
3.03**
6.46**
2.90**
6.29**
3.10**
6.46**
2.95**
6.28**
2.54**
5.39**
f reversal
t+∆
-0.40
-2.46
-0.16
-1.85
-0.52*
-2.47
0.07
0.03
f momentum
t+∆
0.02
-1.43
0.77**
0.20
-0.07
-1.55
-0.20
0.63
f lottery
t+∆
0.38**
4.11**
0.38**
3.72*
0.39**
4.13**
0.38**
3.98**
f skewness
t+∆
0.57
3.82*
0.48
3.28
0.81**
3.85*
f downside
t+∆
0.46**
3.44*
0.41**
3.51*
0.39**
3.44*
0.40**
3.44*
f upside
t+∆
-0.01
3.29
-0.10
3.21
-0.02
3.28
-0.14
3.01
f golden cross
t+∆
0.22
2.83
0.94**
2.90
Hansen’s J
131
(0.00)
129
(0.00)
125
(0.00)
132
(0.00)
140
(0.00)
{df}
{25}
{25}
{24}
{26}
{30}
Panel B: Cross-sectional pricing errors
R2
GLS (%)
78.5
78.4
78.2
78.1
75.6
R2
OLS (%)
80.1
79.6
80.1
78.8
75.6
MAEOLS (%)
0.970
0.984
0.969
0.982
1.13
χ2
NW
110.2
(0.00)
307.1
(0.00)
131.4
(0.00)
77.0
(0.00)
157.5
(0.00)
Panel C: Bootstrap evidence on model comparisons
100×(
HJ+, 3 factor
distance
HJ+, 8 factor
distance
−1) is 8.0 with White’s two-sided p-value of 0.00. The bootstrap p-value is 0.14 for HJ+, 8 factor
distance
> HJ+, 3 factor
distance .
100×(
HJ+, 3 factor
distance
HJ+, 9 factor
distance
−1) is 6.3 with White’s two-sided p-value of 0.00. The bootstrap p-value is 0.24 for HJ+, 9 factor
distance
> HJ+, 3 factor
distance .
100×(
HJ3 factor
distance
HJ+, 7 factor
distance
−1) is 5.8 with White’s two-sided p-value of 0.00. The bootstrap p-value is 0.22 for HJ7 +, factor
distance
> HJ+, 3 factor
distance .
38


### Page 40

Table 9
Exclusion tests: Restricting the SDF loadings on certain factors to be zero
The results presented here are obtained using a two-step GMM estimation procedure with an optimally weighted
matrix. We assess the validity of four exclusion restrictions on the SDF and reject those with p-values below 0.05,
indicating that the excluded factors have loadings on the SDF that are signiﬁcantly different from zero. Table 8
contains the GMM results for the eight-, nine-, and seven-factor models.
Original
Excluded factors in SDF
χ2
{df}
p-value
Model
1
Eight-factor
blottery = bskewness = bdownside = bupside = bgolden cross = 0
17.7
{5}
(0.000)
(Elastic net, ridge)
2
Eight-factor
breversal = blottery = bskewness = bdownside = bupside = 0
19.3
{5}
(0.000)
(LASSO)
3
Nine-factor
breversal = blottery = bskewness = bdownside = bupside = bgolden cross = 0
23.2
{6}
(0.000)
4
Seven-factor
breversal = blottery = bdownside = bupside = 0
17.5
{4}
(0.000)
39


### Page 41

Table 10
Expected return pricing errors across the 33 crypto portfolios
To calculate the model-based average returns of various crypto portfolios, we use equation (3) to obtain the ﬁtted average returns. The mean
absolute errors (denoted MAEOLS) are then computed as (1/33)∑33
i=1 |Realizedi −Fittedi| (using the identity matrix in the calculation of ﬁtted
returns). This is reﬂected as weekly percentage unit.
Eight-factors
Three-factors
Average
Fitted
Model
Fitted
Model
Test Asset
Return
Return
Error
Return
Error
(%)
(%)
(%)
(%)
(%)
(weekly)
(weekly)
(weekly)
(weekly)
(weekly)
(realized)
MAEthree-factor
OLS
−MAEeight-factor
OLS
= 0.16%
with a one-sided p-value = 0.058
1
Size: Decile 1
9.78
4.75
5.03
4.42
5.36
2
Size: Decile 5
3.06
3.51
-0.45
3.41
-0.36
3
Size: Decile 10
1.92
1.73
0.19
1.93
-0.01
4
Reversal: Decile 1
5.59
3.42
2.17
3.71
1.88
5
Reversal: Decile 5
0.46
2.71
-2.25
2.20
-1.74
6
Reversal: Decile 10
2.87
2.85
0.03
1.88
0.99
7
Momentum: Decile 1
3.66
3.36
0.30
3.06
0.60
8
Momentum: Decile 5
0.52
1.55
-1.03
1.60
-1.08
9
Momentum: Decile 10
1.44
1.28
0.17
1.04
0.41
10
Attention: Decile 1
3.82
4.19
-0.37
3.56
0.26
11
Attention: Decile 5
1.10
1.37
-0.27
1.37
-0.27
12
Attention: Decile 10
1.75
0.45
1.30
0.40
1.35
13
Liquidity: Decile 1
4.84
3.81
1.03
3.69
1.15
14
Liquidity: Decile 5
0.76
3.35
-2.59
3.36
-2.60
15
Liquidity: Decile 10
2.01
0.56
1.45
0.81
1.20
16
Lottery: Decile 1
0.70
-0.61
1.31
-0.43
1.13
17
Lottery: Decile 5
1.35
2.91
-1.56
2.64
-1.29
18
Lottery: Decile 10
5.91
5.30
0.61
5.51
0.39
19
Skewness: Decile 1
1.45
2.42
-0.96
1.98
-0.52
20
Skewness: Decile 5
-0.02
1.17
-1.20
1.59
-1.61
21
Skewness: Decile 10
1.59
1.33
0.25
1.93
-0.34
22
Coskew: Decile 1
0.49
1.04
-0.55
1.92
-1.43
23
Coskew: Decile 5
2.26
2.42
-0.17
2.17
0.08
24
Coskew: Decile 10
3.03
1.90
1.13
1.67
1.36
25
Downside: Decile 1
5.20
5.21
-0.01
3.59
1.62
26
Downside: Decile 5
1.14
0.86
0.29
1.01
0.14
27
Downside: Decile 10
1.58
1.31
0.27
3.15
-1.56
28
Upside: Decile 1
1.88
3.61
-1.73
5.16
-3.29
29
Upside: Decile 5
0.88
0.60
0.28
0.97
-0.10
30
Upside: Decile 10
1.42
3.41
-1.99
2.59
-1.17
31
Golden Cross: Decile 1
4.06
4.42
-0.36
3.67
0.39
32
Golden Cross: Decile 5
1.55
1.35
0.20
1.17
0.38
33
Golden Cross: Decile 10
0.26
0.77
-0.51
1.59
-1.33
Mean
2.49
2.39
2.34
Standard deviation
2.07
1.51
1.36
40


### Page 42

Table 11
Cross-sectional pricing results for the best models selected by the machine-learning algo-
rithm and removing the insigniﬁcant SDF loadings in Table 8
The table displays the estimated factor risk premiums and SDF loadings for alternative models. These models are based on the analysis in
Table 7 and include the restricted four- and eight-factor models. These results are based on a two-step GMM estimation procedure. The level of
signiﬁcance is superscripted by ** if the p-value is lower than 0.05, and * if the p-value is between 0.05 and 0.10. χ2
NW represents the test of
whether all pricing errors are zero (Cochrane (2005, 12.2, page 237)) and is distributed χ2
N−K, where K is the number of factors.
Panel A:
Panel B:
Eight-factor model
Nine-factor model
restricted to four factors
restricted to eight factors
SDF
Factor
SDF
Factor
Loading
Premium
Loading
Premium
b
λ
b
λ
×100
×100
f market
t+∆
2.11**
4.5**
1.99**
5.2**
f size
t+∆
2.93**
4.5**
3.13**
5.7**
f reversal
t+∆
≡0
≡0
-0.52*
-0.7
f momentum
t+∆
0.79**
0.8
f lottery
t+∆
0.38**
5.4**
0.34*
4.8**
f skewness
t+∆
≡0
≡0
0.84**
2.0
f downside
t+∆
0.42**
2.6
0.40**
3.2
f upside
t+∆
≡0
≡0
≡0
≡0
f golden cross
t+∆
≡0
≡0
1.00**
3.0
Hansen’s J-statistic
131
(0.00)
127
(0.00)
{df}
{29}
{25}
Cross-Sectional Pricing Errors
100×HJ+
distance
9.60
9.13
R2
GLS (%)
73.4
78.2
R2
OLS (%)
71.4
77.4
MAEOLS (%)
1.179
0.966
χ2
NW
119.6
(0.00)
141.0
(0.00)
A|α| (%)
1.24
1.16
A|α|
A|r| (%)
79.8
74.2
AR2 (%)
27.9
34.4
41


### Page 43

Table 12
Time-series regressions of the eight-factor (crypto-eight) model and alpha tests
The eight-factor model is supported by elastic net and ridge regression results and our diagnostics. We conduct a time-series regression using this
eight-factor model in (following equation (6)) and present the regression coefﬁcient estimates. The level of signiﬁcance is superscripted by **
if the p-value is lower than 0.05, and * if the p-value is between 0.05 and 0.10. The p-values are calculated using the Newey and West (1987)
method, with the number of lags automatically selected. To test the hypothesis that all intercepts are equal to zero, a GMM approach was adopted;
that is, E

(re
t+∆−α −βf′
t+∆)⊗[1 f′
t+∆]′
=
0
(297×1) (see Cochrane (2005, pages 233 and 234)). The Wald test has an asymptotically chi-square
distribution with 33 degrees of freedom.
Portfolio
α
βmarket
βsize
βreversal
βlottery
βskewness
βdownside
βupside
βgolden cross
R2
(%)
Joint test of α = 0 for eight-factor model:
χ2(33) = 183,
p-value=0.000, # of αi signiﬁcant: 13 out of 33
Joint test of α = 0 for three-factor model:
χ2(33) = 178,
p-value=0.000, # of αi signiﬁcant: 17 out of 33
Size
Decile 1
6.7**
0.77**
0.72**
0.004
0.02
-0.03
0.01
-0.01
-0.02
23
Decile 5
0.4
0.70**
0.61**
0.01
0.02
-0.03
-0.01
-0.01
-0.02
31
Decile 10
0.03**
0.995**
-0.01**
0.00
-0.001*
0.001
0.00
0.00
0.00
100
Reversal
Decile 1
2.2*
0.78**
0.33**
0.35**
0.28**
0.20**
-0.04
0.02
0.004
48
Decile 5
-2.0**
0.67**
0.48**
0.01
-0.04**
0.03
0.03
0.01
0.02
27
Decile 10
0.3
0.53**
0.31**
-0.35**
0.33**
-0.20**
0.12**
0.12**
0.02
46
Momentum
Decile 1
0.3
0.51**
0.30**
0.01
0.31**
0.14*
0.02
0.01
0.41**
49
Decile 5
-1.5**
0.63**
0.42**
0.03*
-0.04**
-0.04
-0.02
0.03*
-0.02
30
Decile 10
-0.6
0.63**
0.21
-0.13*
0.21**
-0.13
0.09
0.08
-0.23**
28
Attention
Decile 1
1.0
0.69**
0.62**
-0.01
0.03
0.09
-0.001
0.03
-0.01
14
Decile 5
-0.6
0.61**
0.39**
-0.05
-0.04*
0.09
-0.04*
-0.05
-0.08
20
Decile 10
0.2
0.58**
0.28**
-0.02
-0.06**
-0.04
0.01
0.04*
-0.02
42
Liquidity
Decile 1
1.9**
0.66**
0.68**
0.03
0.06
-0.01
0.001
-0.01
-0.02
16
Decile 5
-1.9**
0.73**
0.54**
0.03
0.03
-0.04
-0.01
0.02
0.01
21
Decile 10
0.5
0.66**
0.25**
0.02
-0.06**
-0.09**
-0.04
0.07**
0.01
42
Lottery
Decile 1
-0.5*
0.46**
0.24**
-0.001
-0.05**
0.01
-0.01
0.02*
-0.03*
41
Decile 5
-1.2*
0.73**
0.51**
0.02
-0.03
-0.10**
0.04
0.02
0.02
25
Decile 10
1.6
0.64**
0.30**
0.02
0.85**
0.08
0.04
0.06
0.01
58
Skewness
Decile 1
-1.2*
0.58**
0.41**
0.18*
0.09**
0.22**
-0.03
0.07
-0.001
41
Decile 5
-2.2**
0.62**
0.41**
0.13**
0.004
-0.10**
0.003
0.01
0.01
23
Decile 10
-0.5
0.68**
0.36**
-0.01
0.09*
-0.24**
0.01
0.01
-0.04
33
Coskew
Decile 1
-1.34*
0.53**
0.45**
0.04
0.11**
-0.06
-0.11**
-0.08*
0.01
17
Decile 5
-0.1
0.60**
0.50**
0.02
0.02
0.002
0.001
0.03
0.03
15
Decile 10
-0.1
0.67**
0.34**
0.12**
0.04
-0.24**
0.21**
0.10**
0.08*
33
Downside
Decile 1
-0.2
0.58**
0.45**
-0.01
0.37**
-0.01
0.56**
0.003
-0.002
50
Decile 5
-0.6
0.58**
0.34**
0.05
-0.04**
0.06
-0.03*
-0.01
-0.01
23
Decile 10
0.5
0.72**
0.32**
0.01
0.31**
-0.16**
-0.41**
0.05
-0.01
36
Upside
Decile 1
-1.7
0.85**
0.51**
0.17**
0.28**
-0.04
0.03
-0.39**
0.05
44
Decile 5
-0.9
0.53**
0.37**
0.02
0.02
-0.06**
-0.02
0.00
-0.03**
29
Decile 10
-1.6*
0.63**
0.29**
0.10*
0.31**
0.003
0.01
0.44**
-0.06
53
Golden Cross
Decile 1
0.5
0.73**
0.30**
0.02
0.23**
0.11*
0.02
-0.03
0.45**
57
Decile 5
-0.6
0.57**
0.41**
0.03
-0.04**
-0.05
0.04
0.05**
0.03
20
Decile 10
-1.5
0.63**
0.27**
-0.06
0.18*
-0.09
0.03
0.04
-0.34**
33
42


### Page 44

Table 13
Factor spanning tests: Time-series regressions with the eight-factor (crypto-eight) model
This table provides the intercept and slope coefﬁcients estimated from time-series regressions of each of the 13 crypto factors using the eight-factor
model as the covariate. The level of signiﬁcance is superscripted by ** if the p-value is lower than 0.05, and * if the p-value is between 0.05 and
0.10. The last column displays the adjusted R2 (R2).
Intercept
βmarket
βsize
βreversal
βlottery
βskewness
βdownside
βupside
βgolden cross
R2
(%)
(%)
f market
t+∆
2.95∗∗
≡0
-0.62∗∗
-0.02
0.11∗∗
0.02
0.03
0.01
-0.01
59
f size
t+∆
3.93∗∗
-0.75∗∗
≡0
-0.01
-0.02
-0.02
-0.02
0.00
-0.04∗∗
56
f reversal
t+∆
0.32
-0.11
-0.03
≡0
-0.02
0.66
-0.02
0.17
0.26
37
f momemtum
t+∆
1.80∗∗
0.22
0.05
-0.08
-0.01
-0.22∗
0.15
0.11
-0.70∗∗
60
f attention
t+∆
0.92
0.15
0.31∗∗
0.16
0.43∗∗
-0.06
0.11
-0.11
-0.07
21
f liquidity
t+∆
0.66
0.24
0.32∗∗
0.03
0.33∗∗
-0.02
0.08
-0.11
-0.06
17
f lottery
t+∆
0.89
0.76∗∗
-0.12
-0.03
≡0
0.23
0.01
0.07
0.08
25
f circulation
t+∆
0.76
0.47∗∗
0.06
-0.05
-0.04
0.06
-0.04
0.00
-0.001
16
f skewness
t+∆
0.68
0.06
-0.06
0.40∗∗
0.11∗
≡0
-0.06
-0.14∗∗
-0.004
34
f coskew
t+∆
1.80∗∗
-0.08
-0.09
0.17∗∗
0.04
0.01
0.38∗∗
0.40∗∗
-0.07
47
f downside
t+∆
4.31∗∗
0.21
-0.15
-0.03
0.02
-0.13
≡0
-0.09
-0.01
4
f upside
t+∆
1.06
0.05
0.00
0.26∗∗
0.09
-0.36∗∗
-0.10
≡0
-0.10
6
f golden cross
t+∆
1.84
-0.08
-0.26∗∗
0.36∗∗
0.09
-0.01
-0.01
-0.09
≡0
15
43


### Page 45

Table 14
Estimated SDF loadings and factor risk premiums with (i) market and 12 principal com-
ponents, (ii) dense factor model of 13 principal components, and (iii) market plus mean-
variance efﬁcient portfolio
This table presents the estimated SDF loadings and factor risk premiums using a dense factor model with 13 principal
components. These principal components are derived from either (i) 12 factors orthogonalized with respect to the
crypto market or (ii) all 13 factors, and the estimation is conducted using a two-step and iterated GMM method (see
equation (2)) with 33 test assets. The dataset covers a sample period from January 3, 2014, to January 26, 2024,
which includes 525 weeks. The signiﬁcance level is denoted with ** if the p-value is less than 0.05, and * if the
p-value falls between 0.05 and 0.10. χ2
NW represents the test of whether all pricing errors are zero (Cochrane (2005,
12.2, page 237)) and is distributed χ2
N−K, where K is the number of factors.
Panel A:
Panel B:
Panel C:
Crypto market and 12
13 crypto
Crypto market
principal components
principal components
plus MVE portfolio
(33 assets and 13 factors )
(33 assets and 13 factors)
(33 assets and two factors)
SDF
Factor
SDF
Factor
SDF
Loading
Premium
Loading
Premium
Loading
Two
Fama
Two
Iterated
Fama
Two
Step
McBeth
Step
GMM
McBeth
Step
f market
t+∆
0.12
0.06**
f
pc1
t+∆
0.02
0.04
0.09
f market
t+∆
0.87**
f
pc1
t+∆
0.03
-0.21**
f
pc2
t+∆
0.01
0.04
0.11
mmve
t+∆
3.37**
f
pc2
t+∆
0.06
-0.03
f
pc3
t+∆
-0.04
0.02
0.25*
f
pc3
t+∆
0.08
0.08
f
pc4
t+∆
0.13
0.11
0.10
f
pc4
t+∆
0.06
-0.40**
f
pc5
t+∆
0.20**
0.24**
-0.02
f
pc5
t+∆
0.06
0.23**
f
pc6
t+∆
0.004
0.04
0.07
f
pc6
t+∆
-0.31**
-0.57**
f
pc7
t+∆
0.14
0.28**
0.30**
f
pc7
t+∆
0.08
0.26**
f
pc8
t+∆
0.08
0.34**
0.21**
f
pc8
t+∆
-0.22
-0.47**
f
pc9
t+∆
-0.13
-0.06
0.01
f
pc9
t+∆
-0.15
-0.03
f
pc10
t+∆
-0.48
-0.57*
-0.03
f
pc10
t+∆
-0.69**
-0.20**
f
pc11
t+∆
0.27
0.02
-0.07
f
pc11
t+∆
0.14
-0.14**
f
pc12
t+∆
0.69**
1.27**
0.48**
f pc12
t+∆
0.06
-0.10
f pc13
t+∆
0.38
-0.04
0.08
Hansen’s J
53.8
(0.00)
53.8
(0.00)
82.9
(0.00)
{df}
{20}
{20}
{20}
100×HJ+
distance
14.84
14.90
11.73
9.72
R2
GLS (%)
82.3
82.3
68.5
R2
OLS (%)
83.7
83.7
68.7
MAEOLS (%)
0.848
0.848
1.19
χ2
NW
87.8
(0.00)
94.1
(0.00)
44


### Page 46

Table 15
Out-of-sample cross-sectional performance of models (model estimated on 13 assets same as
factors but applied to 33 test portfolios)
This table assesses the effectiveness of factor models in explaining monthly excess returns on various crypro portfolios not used in estimation.
The 33 portfolios considered are classiﬁed by characteristics as portfolios 1, 5, and 10. We show (i) the Hansen and Jagannathan (1997) distance
with identity matrix (Cochrane (2005)), (ii) the average absolute alpha value, (iii) the ratio of average absolute alpha to the average demeaned
return on portfolio, (iv) the average adjusted R2 from the 33 portfolios as AR2, and (v) the GRS statistic. The “kns” model refers to the method of
regularizing SDF loadings.
HJ+
distance
A|α|
A|α|
A|r|
AR2
R2
OLS
R2
GLS
MAEOLS
GRS
×100
(%)
(%)
(%)
(%)
(%)
Panel A: Models estimated using 13 assets same as 13 factors
and applied to 33 crypto portfolios
Eight factors: Elastic net and ridge
9.54
1.11
0.71
35.4
80.1
78.5
0.970
3.87
Eight factors: regularizing SDF loadings
9.57
1.12
0.72
30.6
79.7
77.0
0.962
3.70
Market plus MVE: regularizing SDF loadings
10.89
1.16
0.75
18.1
68.7
68.5
1.185
3.98
Three-factors: Market, size, momentum
10.70
1.40
0.90
26.1
75.6
75.6
1.133
4.10
100×(
HJ+, 3 factor
distance
HJ+, 8 factor
distance
−1) is 8.8 with White’s two-sided p-value of 0.00. The bootstrap p-value is 0.14 for HJ+, 8 factor
distance
> HJ+, 3 factor
distance .
100×(
HJ+, 3 factor
distance
HJ+, 8 kns
distance
−1) is 8.8 with White’s two-sided p-value of 0.00. The bootstrap p-value is 0.13 for HJ+, 8 kns
distance > HJ+, 3 factor
distance
100×(
HJ+, 3 factor
distance
HJ+, 2 kns
distance
−1) is 2.2 with White’s two-sided p-value of 0.00. The bootstrap p-value is 0.44 for HJ+, 2 kns
distance > HJ+, 3 factor
distance
100×(
HJ+, 8 kns
distance
HJ+, 8 factor
distance
−1) is 0.1 with White’s two-sided p-value of 0.08. The bootstrap p-value is 0.54 for HJ+, 8 factor
distance
> HJ+, 8 kns
distance
100×(
HJ+, 2 kns
distance
HJ+, 8 factor
distance
−1) is 8.3 with White’s two-sided p-value of 0.00. The bootstrap p-value is 0.31 for HJ+, 8 factor
distance
> HJ+, 2 kns
distance
Panel B: Insample model estimation results
Three
Eight
Eight
Two
Factor
Factor
Factor
Factor
(kns)
(kns)
f market
t+∆
2.30**
2.05**
1.81**
0.62**
f size
t+∆
2.04**
2.25**
2.17**
f coskew
t+∆
0.38**
f circulation
t+∆
0.37
f downside
t+∆
0.41**
0.23*
f golden cross
t+∆
0.10
0.20*
f attention
t+∆
0.13
f liquidity
t+∆
0.12
f reversal
t+∆
0.12
f momentum
t+∆
0.02
f lottery
t+∆
0.11
f skewness
t+∆
0.05
f upside
t+∆
0.07
mmve
t+∆
2.52**
R2
OLS (%)
83.2
97.1
99.2
94.9
R2
GLS (%)
81.1
96.8
98.8
92.1
MAEOLS (%)
0.82
0.30
0.17
0.45
Hansen’s J-statistic
21
(0.02)
8
(0.14)
2
(0.80)
24
(0.01)
{df}
{10}
{5}
{5}
{11}
100×HJ+
distance
6.72
2.64
1.55
3.06
A|α| (%)
1.48
0.46
0.20
1.20
AR2 (%)
33.9
73.8
73.7
26.1
45


### Page 47

Table 16
Interpretation of crypto factors and innovations in volatilities of S&P 500, VIX, bond, com-
modity, and dollar index
For each crypto factor, we perform a regression on six innovations in volatility constructed from (i) E-mini S&P 500 futures, (ii) VIX futures,
(iii) commodity index futures, (iv) futures on 30-year Treasury bond, and (v) futures on dollar index. The source of this intraday data sampled
at ﬁve-minute is Barchart. Innovations in equity futures volatility and innovations in VIX futures volatility are never signiﬁcant. For each crypto
factor, there are two panels. The ﬁrst panel presents the results of a univariate regression model that examines the relationship between the crpto
factor and a innovation in a volatility (constructed from ﬁve-minute intraday data), as follows:
f characteristic
t+∆
= constant + slope×∆VOLℓ
t+∆+et+∆
for
ℓ= {
futures underlier
z
}|
{
S&P 500,vix,commodity,bond,dollar index}.
The signiﬁcance is represented by the Newey and West p-value with a ** (p-value lower than 0.05) or * (p-value higher than 0.05 but less than
0.1). The long and short legs of carry are consistent with the construction in Table 4. In the adjacent panel, the Fama and MacBeth procedure is
utilized, with p-values calculated using the Newey and West procedure. The SDF loadings are estimated by GMM, as follows:
E


 1 −b′(ft+∆−µ)

|
{z
}
market plus size plus ∆VOL
⊗
re
t+∆
|{z}
ten crypto assets
ft+∆−µ
vec((ft+∆−µ)(ft+∆−µ)′)−vec(Ωf)

=
0
(19×1),
χ2
NW represents the test of whether all pricing errors are zero (Cochrane (2005, 12.2, page 237)) and is distributed χ2
N−K, where K is the number
of factors.
Univariate regression
GMM estimations and Fama-McBeth procedure
Dependent
constant
slope
R2
Test
SDF
Factor
SDF
Factor
SDF
Factor
variable
(%)
Assets
Loading
Premium
Loading
Premium
Loading
Premium
b
λ
b
λ
b
λ
×100
×100
×100
∆VOLbond
Crypto market
Crypto size
∆VOLbond
f size
t+∆
0.02**
3.83*
0.15
Ten size
0.346
-2.34**
≡0
≡0
413.5**
0.79**
Long small cap
0.04**
0.31
-0.19
• χ2
NW p-value=0.00
Short large cap
0.02**
-3.52
0.13
∆VOLcommodity
Crypto market
Crypto size
∆VOLcommodity
f momentum
t+∆
0.02
-1.89*
0.02
Ten momentum
0.552
6.59**
-0.165
-2.84
-131.7**
-1.02*
Long winners
0.04**
-1.41
0.05
• χ2
NW p-value=0.02
Short losers
0.02*
0.48
-0.17
∆VOLdollar index
Crypto market
Crypto size
∆VOLdollar index
f lottery
t+∆
0.03
15.34**
0.44
Ten lottery
0.897**
4.67**
0.595
-4.43*
342.5**
0.01
Long high variance
0.04**
12.61**
0.21
• χ2
NW p-value=0.11
Short low variance
0.01**
-2.73
0.11
∆VOLbond
Crypto market
Crypto size
∆VOLbond
f skewness
t+∆
0.01
-7.04*
0.40
Ten skewness
0.962*
-0.62
0.681
0.76
250.5**
0.08
Long low skewness
0.02**
-7.73**
0.77
• χ2
NW p-value=0.19
Short high skewness
0.01
-0.69
-0.18
∆VOLcommodity
Crypto market
Crypto size
∆VOLcommodity
f downside
t+∆
0.04**
-2.07**
0.14
Ten downside
0.864
4.96
-1.021
-9.21*
7.769
-0.62
Long low downside
0.04**
-1.89*
0.20
• χ2
NW p-value=0.43
Short high downside
0.00
0.18
-0.19
∆VOLdollar index
Crypto market
Crypto size
∆VOLdollar index
f golden cross
t+∆
0.02
16.26*
0.49
Ten golden cross
1.218**
4.24
1.179*
-0.09
273.4**
0.08
Long low golden cross
0.03**
11.54*
0.41
• χ2
NW p-value=0.07
Short high golden cross
0.02
-4.72
-0.06
46


### Page 48

−0.02
0.00
0.02
0.04
0.06
0.08
0.10
Realized  etu ns
−0.02
0.00
0.02
0.04
0.06
0.08
0.10
F
itted  etu ns
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
(13)
(14)
(15)
(16)
(17)
(18)
(19)
(20)
(21)
(22)
(23)
(24)
(25)
(26)
(27)
(28)
(29)
(30)
(31)
(32)
(33)
Th ee-facto  model
Eight-facto  model
Figure 1. Realized versus ﬁtted returns across the 33 crypto portfolios
Plotted are the realized returns (x-axis) and the ﬁtted returns (y-axis) corresponding to the crypto
portfolios indexed from 1 to 33. The ﬁtted average returns are based on equation (3).
• Three-factor model comprises market, size, and momentum;
• Eight-factor model comprises market, size, reversal, lottery, skewness, downside, upside,
and golden cross.
See the model estimates in Table 8. The crypto test portfolios and the corresponding model errors
are shown in Table 10.
47

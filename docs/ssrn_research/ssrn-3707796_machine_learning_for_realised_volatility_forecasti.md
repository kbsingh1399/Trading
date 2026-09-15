# Machine Learning for Realised Volatility Forecasting

- **Source File**: `ssrn-3707796.pdf`
- **Total Pages**: 91
- **SSRN ID**: `ssrn-3707796`

---

## Page 1

Machine Learning for Realised Volatility Forecasting
Eghbal Rahimikia and Ser-Huang Poon∗
First version: October 12, 2020 • This revision: January 22, 2026
Abstract
We assess the predictive power of machine learning (ML) models for forecasting realised
volatility using information from HAR model variables, limit order book (LOB) data, and
news sentiment. Training and robustness checks on nearly seven million ML models show
that high-dimensional ML models outperform HAR models in 90% of the out-of-sample
period, except during extreme volatility. Explainable AI analysis identifies mid prices, mean
bids, and mean asks as key predictors. Notably, incorporating ML into ensemble frameworks
enhances HAR model performance, though caution is needed when using ML models as direct
substitutes, since they may yield unreliable forecasts under certain market conditions.
Keywords: Realised Volatility Forecasting, Machine Learning, Big Data, Long Short-Term Mem-
ory, Heterogeneous Autoregressive Models, Explainable AI.
JEL: C22, C45, C51, C53, C55, C58
∗Eghbal Rahimikia (corresponding author) (eghbal.rahimikia@manchester.ac.uk) and Ser-Huang Poon (ser-
huang.poon@manchester.ac.uk) are at the University of Manchester, Alliance Manchester Business School, UK.
In particular, we would like to extend our thanks to Robert Engle, Francis X. Diebold, and Bill McDonald
for their helpful comments and suggestions.
We are also grateful to the participants and discussants of the
British Accounting and Finance Association (BAFA) Annual Conference, 37th International Conference of the
French Finance Association (AFFI), 8th Annual MMF PhD Conference, Durham University Business School, 7th
International Young Finance Scholar’s Conference, Data Fest, Russia, Finance Research Day, Alliance Manchester
Business School, 10th International Conference of the Financial Engineering and Banking Society (FEBS), and
the 2023 BAR Inaugural Annual Conference, Harvard University. All models were run on the Computational
Shared Facility of the University of Manchester. We must express our sincere appreciation to the IT Services
of the University of Manchester for their constant and continued support, and for providing the computational
infrastructure for this study. Last but not least, our sincere thanks are due to the Accounting and Finance Division
at Alliance Manchester Business School for their financial support.


## Page 2

1
Introduction
Volatility forecasting plays a critical role in financial modelling and decision-making. This study
investigates the effectiveness of machine learning (ML) models combined with a rich feature set
in forecasting volatility for 23 NASDAQ tickers over a sample period from 27 July 2007 to 27
January 2022. It is vital to consider ML for several reasons. First, classical econometric models,
without undergoing additional modifications, cannot handle a large number of input variables in
big datasets, such as limit order book (LOB) data and news stories, within a single model. Second,
ML models are usually more efficient in capturing nonlinear relationships in high dimensions, a
task that standard econometric models generally struggle to accomplish. In this study, we aim
to explore the impact of a wide array of variable groups originating from the well-known HAR-
family of models, high-frequency LOB data, and sentiment variables extracted from news stories
on the forecasting accuracy of realised volatility (RV) under different market conditions, achieved
through the utilisation of ML models, notably long short-term memory (LSTM) models.
ML models have been used in various areas of finance for several years. Gu et al. (2020)
showed the superior performance of ML models for empirical asset pricing, Gu et al. (2021)
introduced an autoencoder asset pricing model and produced smaller out-of-sample pricing errors
compared to classical leading factor models, Jiang et al. (2023) produced more accurate stock
return predictions based on ML image analyses, and Chen et al. (2024) employed ML in the
estimation of the stochastic discount factor. A subgroup of ML models has been developed for
sequential data such as video, music, text, and, in our case, financial time series. The recurrent
neural network (RNN) and its extension, LSTM (Hochreiter and Schmidhuber, 1997), are among
the most widely used pioneering ML models in both academia and industry for sequential data,
paving the way for more advanced ML models (see Vinyals et al. (2019) and Andrychowicz et al.
(2020) for recent recurrent use cases).
Through their recurrent structure and, in the case of
LSTM, gated memory mechanisms, these models can perform sequential processing and learn
long-term dependencies in time series.
The availability of high-frequency financial data makes RV a popular model-free proxy for ac-
tual volatility (Andersen et al., 2001; Barndorff-Nielsen and Shephard, 2001). With the popularity
of RV, the heterogeneous autoregressive (HAR) model (Corsi, 2009) and its variations are com-
monly used in forecasting RV. Well-known variants include HAR-J (HAR with jumps) and CHAR
2


## Page 3

(continuous HAR) (Andersen et al., 2007), Patton and Sheppard (2015) SHAR (semivariance-
HAR), which separates the impact of negative and positive returns on subsequent RV, and HARQ
(Bollerslev et al., 2016), which adjusts forecasts for measurement error based on realised quarticity
(RQ).
Within the realm of literature centred on ML models for RV forecasting, Hillebrand and
Medeiros (2010), Fernandes et al. (2014), Audrino and Knaus (2016), Branco et al. (2024), and
Audrino and Chassot (2025) demonstrated that ML models exhibit similar or lower forecasting
performance when compared to the HAR-family of models. On the other hand, Bucci (2020),
Christensen et al. (2023), Zhu et al. (2023), and Li and Tang (2025) reported improvements in
RV forecasting using ML models. Motivated by these contradictory findings, this study aims to
establish a more systematic comparison between the two classes of models, with the objective of
better identifying their respective strengths and weaknesses under different market conditions.
Also, apart from fitting ML models with a large, comprehensive dataset, it is very important
to fully explore the hyperparameters and tuning of ML models. In contrast to these previous
ML studies that utilised a relatively small number of variables, our study focuses on leveraging a
vast array of data features and testing near seven million ML models. This approach enables us
to explore thoroughly whether ML (with a wide and varied range of variables) outperforms the
HAR-family of models in RV forecasting.
The three variable sets, i.e., LOB, news sentiments and HAR, are commonly used in the liter-
ature for volatility forecasting, though rarely all three at the same time. The high dimensionality
of ML models allows us to test all these variables together in a single model. Using combina-
tions of 147 predictors (6 HAR, 9 news sentiments, and 132 LOB variables), this study provides
strong statistical evidence that ML models outperform the HAR-family of models in RV fore-
casting according to MSE, quasi-likelihood (QLIKE), and mean directional accuracy (MDA) loss
functions, as well as the reality check (RC). However, and more importantly, this considerable
and statistically significant enhancement applies to 90% of out-of-sample daily forecasts, except
when the actual RV reaches high levels.
On high volatility days, the HAR-family of models
generally outperform ML models. This finding is potentially concerning and highlights the need
for cautious evaluation before considering ML models as direct substitutes for the HAR-family
of models. Moreover, LOB data, in general, provides stronger volatility forecasting performance
when compared to news sentiment variables. A key discovery of our study is the importance of
3


## Page 4

incorporating a wide range of input variables in a single model to improve RV forecasting perfor-
mance. We noted that even a simple ML model with HAR variables can outperform HAR models
in forecasting RV. As emphasised by Christensen et al. (2023), this could be due to the ability
of ML models to capture nonlinear relationships in RV forecasting. However, the performance
improvement becomes particularly pronounced when a rich set of predictors is included in the
ML models.
Recently, there has been increased attention in the fields of accounting and finance towards
deploying explainable AI (XAI) techniques to evaluate ML models; see, for example, Erel et al.
(2021), Bali et al. (2023), and Chronopoulos et al. (2024). By applying XAI, we find that, among
the 147 input variables, mid prices at all LOB levels, mean bid, and mean ask are the most
informative variables for forecasting RV. We also find that the relative importance of different
groups of information sets changes over time, with 2018 emerging as a structural breakpoint. Prior
to 2018, news-based variables constitute the most informative group. However, in the post-2018
period, characterised by heightened market volatility, LOB variables become more prominent.
Additionally, HAR variables demonstrate greater importance during periods of high volatility.
This alternation in the importance of different predictors over time once again underscores the
critical relevance of the time-varying choice of optimal predictors for RV forecasting. The results
also demonstrate that HAR variables maintain their importance, particularly for forecasting RV
during high volatility days.
Extensive robustness checks also confirmed that, for normal volatility days in the out-of-
sample period, the superiority of ML over the HAR-family of models remained unchanged. We
also trained and tested LSTM models for individual tickers using different ML hyperparameters,
i.e., the number of units and the number of epochs. For 90% of the out-of-sample forecasting
period, when the actual RV level is less extreme, the optimal number of units and epochs varies,
but the overall ML structure is simpler. For the remaining 10% of the out-of-sample period,
when the actual RV level is extreme, a more complex ML structure with a larger number of
units and epochs is needed. The full out-of-sample is also influenced by high volatility days and
leans towards more complex models. We further reinforced our robustness checks by changing
the model type, altering the input data, employing alternative loss functions, and implementing
additional techniques to mitigate overfitting. Across all specifications, the results consistently
support our main conclusions. Our findings also suggest that a simple ensemble method, which
4


## Page 5

combines the outputs of the HAR-family of models and ML models, offers a practical and effective
way to leverage the strengths of both model classes simultaneously. This method achieved robust
RV forecasting performance across varying market conditions. Importantly, the results indicate
that exclusive reliance on ML models may be suboptimal in certain scenarios, particularly during
high volatility days, a limitation that can be mitigated through this simple method.
The literature offers conflicting evidence on whether ML models systematically outperform the
HAR-family of models in forecasting realised volatility. We show that these discrepancies largely
reflect fundamental differences in sample composition, market conditions, and modelling design
rather than the existence of a universally superior approach. Relative forecasting performance
is inherently sample- and regime-dependent: variations in the underlying asset universe and
sample timeframe directly affect the frequency, severity, and composition of high volatility days,
which can influence forecast evaluation and model rankings. ML models are flexible function
approximators with large hyperparameter spaces, and differences in model architecture, feature
construction, tuning strategies, and validation schemes can also generate variation in out-of-
sample performance across studies. By contrast, the HAR-type specifications are deliberately
parsimonious in structure and estimation, which tends to yield more stable and comparable
performance across samples.
Finally, a relatively small number of extreme realised volatility
observations, often associated with stock-specific jumps followed by periods of elevated market-
wide volatility, can disproportionately affect forecast comparisons, with ML models being more
sensitive to such tail events, while HAR-type specifications are relatively more robust.
The remainder of this study is organised as follows: Section 2 gives a brief review of RV and the
HAR-family of models. Section 3 describes the data and provides variable definitions. Section 4
provides the empirical framework: RNN, LSTM, and regularisation techniques in Subsection 4.1,
and the structure of our proposed ML models in Subsection 4.2. Section 5 presents the results
of the primary experiments, Section 6 evaluates the predictive power of input variables, and
Section 7 performs a series of robustness checks. Section 8 also introduces a simple ensemble
method for forecasting RV. Finally, Section 9 concludes with a discussion of the findings from
this study.
5


## Page 6

2
Realised Volatility and HAR-Family of Models
Suppose that Pt is the ticker price process with the following dynamics:
d log(Pt) = µtdt + σtdWt + JtdQt,
(1)
where µt is the drift (a continuous function), σt is the volatility process (a c`adl`ag function), Jt is
the jump size, Wt is the standard Brownian motion, and Qt is a Poisson process. For time t −1
to t, the integrated variance is defined as follows:
IVt =
Z t
t−1
σ2
sds.
(2)
This integrated variance is not observable; therefore, the realised variance is defined by the sum-
mation of squared high-frequency returns as follows:
RVt ≡
M
X
i=1
r2
t,i,
(3)
where M = 1/δ, and the δ-period intraday return is defined as rt,i ≡log (Pt−1+iδ)−log
 Pt−1+(i−1)δ

.
In the absence of jumps, it provides a consistent estimator as the number of intraday observations
increases, or equivalently, as δ →0 (Barndorff-Nielsen and Shephard, 2002). Building on existing
research, this study seeks to forecast realised variance.
2.1
HAR-Family of Models
Introduced by Corsi (2009), the HAR model, defined below, encompasses the most popular RV
forecasting model:
RVt+1 = β0 + β1RVt + β2RV
w
t + β3RV
m
t + ϵt+1,
(4)
where RVt is the daily RV at time t, RV
w
t is the daily average over the last week (last 5 days),
and RV
m
t is the daily average over the last month (last 21 days). Corsi (2009) showed that this
easy-to-estimate linear model with a simple set of historical RVs produced remarkable forecasting
performance. Since the work of Corsi (2009), research on improving RV forecasting performance
has gained momentum. Researchers expanded the basic HAR model with various information
sets and high-frequency data to enhance RV forecasting performance.
6


## Page 7

Andersen et al. (2007) and Corsi and Reno (2009) analysed the impact of adding a jump com-
ponent to the basic HAR model. The jump component at time t is defined as Jt = max[RVt −
BPVt, 0], with bipower variations:
BPVt = π
2
M−1
X
i=1
|rt,i||rt,i+1|,
(5)
where M denotes the number of intraday returns per day and rt,i is the i-th intraday return on
day t, for i = 1, . . . , M. The HAR-J model is specified as follows:
RVt+1 = β0 + β1RVt + β2RV
w
t + β3RV
m
t + βjJt + ϵt+1.
(6)
As an alternative specification, the CHAR replaces the predictive variables with BPVt as follows:
RVt+1 = β0 + β1BPVt + β2BPV
w
t + β3BPV
m
t + ϵt+1,
(7)
where BPVt, BPV
w
t , and BPV
m
t
are, respectively, the daily BPV, the daily average over the
past week, and the daily average over the past month at time t. Without the jump component,
BPV in Equation (7) is better at capturing volatility persistence and long memory than RV in
Equation (4).
Patton and Sheppard (2015) proposed the SHAR model, separating the impact of negative and
positive intraday returns on subsequent RV. In the SHAR model, the first lag of RV in the HAR
model (Equation (4)) is replaced by a positive return RV +
t
and a negative return RV −
t , where
RV +
t
≡PM
i=1 r2
t,iI(rt,i>0) and RV −
t
≡PM
i=1 r2
t,iI(rt,i<0). Here, I denotes an indicator function. The
authors found that RVt+1 is more strongly related to RV −
t
than to RV +
t
for the S&P 500 index
and 105 individual tickers.
Bollerslev et al. (2016) studied the impact of measurement error on volatility forecasting. First,
they defined the integrated quarticity, IQt =
R t
t−1 σ4
s ds, and its discrete-time equivalent, realised
quarticity RQt ≡
  M
3
 PM
i=1 r4
t,i. Next, they introduced the ARQ, HARQ, and HARQ-F models.
The HARQ model is defined as follows:
RVt+1 = β0 + β1RVt + β1QRQ1/2
t
RVt + β2RV
w
t + β3RV
m
t + ϵt+1,
(8)
7


## Page 8

where RQt
1/2 is demeaned for easier interpretation. For β1Q < 0, RVt has a lower impact when
the measurement error is larger, and a higher impact when the measurement error is smaller.
When the coefficients on the weekly and monthly components are set to zero (i.e., β2 = β3 = 0),
Equation (8) reduces to the ARQ model. Also, HARQ-F is defined by adding the daily average
of RQ over the past week and past month to the HARQ model specification. Bollerslev et al.
(2016) found the HARQ model to have better forecasting performance, producing more volatility
persistence in normal times and quicker volatility mean reversion in erratic times for the S&P 500
index and 27 Dow Jones constituent tickers. Finally, Rahimikia and Poon (2020) compared a range
of alternative variables aimed at enhancing the forecasting performance of HAR-family of models.
They showed that augmenting standard HAR specifications with only the previous day’s average
LOB depth and news count yields statistically and economically significant improvements in RV
forecasting performance, without requiring any modification to the underlying model structure.
3
Variables
In this study, 23 NASDAQ tickers continuously traded between 27 July 2007 and 27 January
2022 were chosen for analysis.1 RV is calculated according to Equation (3) using 5-minute ticker
returns.
Table 1 provides the RV descriptive statistics for these 23 tickers.
Subsection 3.1,
Subsection 3.2, and Subsection 3.3 describe the three variable sets from, respectively, HAR-family,
news stories, and LOB2. The LOB variables for these 23 tickers are compiled using information
extracted from LOBSTER3 (Huang and Polak, 2011). These are the three main variable sets
commonly used in the literature for volatility forecasting. The fourth variable set is simply the
amalgamation of all three variable sets above.
3.1
HAR-Family Variables
Table 2 lists the variables used in the HAR-family of models. The first column (‘Description’)
contains the names of the variables.
‘RV’, ‘BPV’, ‘BPV jump’, ‘negative RV’, ‘positive RV’,
1Nearly seven million ML models were trained and evaluated in this study. To ensure the analysis remained
computationally manageable, a limited number of tickers was selected, specifically those with the highest market
capitalisations over the sample period and complete data coverage across all trading days. Model training and
evaluation were carried out on high-performance computing servers. Despite the limited number of tickers, the
model development process was highly computationally intensive, requiring several months of continuous training
and evaluation.
2Throughout this study, we use the terms LOB and order book (OB) interchangeably.
3LOBSTER stands for ‘limit order book system – the efficient reconstructor.’
8


## Page 9

Table 1: Descriptive Statistics of Realised Volatility
Ticker
Min
Max
1st quantile
Median
3rd quantile
Mean
STD
Kurtosis
Skewness
AAPL
0.102
229.420
0.899
1.733
3.680
4.623
12.596
111.012
9.124
MSFT
0.067
216.181
0.829
1.449
2.814
3.237
8.125
194.004
11.275
INTC
0.030
318.697
1.103
1.873
3.577
4.299
11.628
294.963
13.982
CMCSA
0.004
237.387
0.910
1.632
3.320
3.821
9.697
192.169
11.462
QCOM
0.122
373.543
1.024
1.975
4.129
5.073
15.380
200.609
12.100
CSCO
0.047
343.946
0.886
1.561
3.028
4.115
13.160
212.453
12.258
EBAY
0.205
252.608
1.319
2.271
4.356
5.082
12.592
142.684
10.009
GILD
0.064
259.489
1.167
1.892
3.379
4.304
12.930
182.820
12.063
TXN
0.177
287.897
1.047
1.905
3.748
4.014
9.820
311.666
14.242
AMZN
0.065
547.030
1.305
2.336
4.808
6.200
19.359
242.205
12.735
SBUX
0.052
265.094
0.864
1.594
3.423
4.201
11.237
161.435
10.626
NVDA
0.159
1104.351
2.282
4.358
9.084
9.756
30.117
586.612
20.058
MU
0.292
484.388
3.570
6.246
11.912
12.818
25.734
89.141
7.960
AMAT
0.292
531.579
1.783
3.028
5.712
6.005
14.632
532.194
18.338
NTAP
0.119
462.821
1.503
2.587
5.154
6.289
18.008
201.510
11.934
ADBE
0.119
569.720
1.099
2.020
3.908
4.947
15.003
588.095
18.867
XLNX
0.229
265.374
1.296
2.363
4.787
5.005
11.941
194.718
11.764
AMGN
0.032
214.156
0.969
1.593
2.872
3.398
9.612
183.759
11.898
VOD
0.055
219.033
0.687
1.342
3.137
3.933
10.869
122.252
9.601
CTSH
0.189
485.894
0.984
1.764
4.161
5.288
15.757
325.214
14.287
KLAC
0.154
499.808
1.456
2.710
5.416
5.919
16.878
354.626
16.033
PCAR
0.039
389.930
1.157
2.162
4.633
5.125
12.108
313.338
13.010
ADSK
0.268
693.772
1.644
2.765
5.167
6.644
22.377
388.131
16.554
Table 2: HAR-Family Variables
Description
#
Characteristic
RV
1
RVt ≡PM
i=1 r2
t,i
BPV
1
BPVt = π
2
PM−1
i=1 |rt,i||rt,i+1|
BPV jump
1
Jt = max(RVt −BPVt, 0)
Positive; negative RV
2
RV +
t
≡PM
i=1 r2
t,iI(rt,i>0); RV −
t
≡PM
i=1 r2
t,iI(rt,i<0)
Realised quarticity
1
RQt ≡(M
3 ) PM
i=1 r4
t,i
Notes: The first column (‘Description’) contains the names of the variables. Section 2 de-
scribes ‘RV’, ‘BPV’ and ‘BPV jump’ (as defined in Barndorff-Nielsen and Shephard (2004)),
‘negative RV’ and ‘positive RV’ (as defined in Patton and Sheppard (2015)), and ‘realised
quarticity’ (as defined in Bollerslev et al. (2016)). The second column (‘#’) lists the number
of variables included. The formula used to compile each defined variable is shown in the last
column (‘Characteristic’). This group has six defined variables in total. The most commonly
used 5-minute sampling frequency is used for calculating these variables. I denotes an indica-
tor function.
9


## Page 10

and ‘realised quarticity’ are described in Section 2. The second column (‘#’) lists the number
of variables included. The formula used to compile each defined variable is shown in the last
column (‘Characteristic’). This group has six defined variables in total. The most commonly
used 5-minute sampling frequency is used for calculating these variables.
3.2
News Variables
The Dow Jones Newswires covers the Wall Street Journal, MarketWatch, Barron’s news, etc.
Every news story is tagged with ‘significant’, ‘about’, or ‘mention’. ‘Significant’ denotes a news
story that is important to a specific ticker; ‘about’ denotes a news story about a ticker but of
no particular significance, while ‘mention’ denotes cases where the ticker is referenced but is not
the main subject of the news story. As ‘significant’ is introduced much later and is not avail-
able for most of our sample period, the tag ‘about’ is used for extracting company-related news
for constructing the nine daily news variables listed in Table 3. Apart from ‘News count’, the
other sentiment variables, ‘Negative’, ‘Positive’, ‘Uncertainty’, ‘Litigious’, ‘Weak modal’, ‘Mod-
erate modal’, ‘Strong modal’, and ‘Constraining’, are compiled according to the LM dictionary
(Loughran and McDonald, 2011).4
The steps for preprocessing the news data and calculating the sentiment variables follow those
in Loughran and McDonald (2011). The sentiment measure for a particular company on day t is
equal to the weighted word counts summed over all relevant words and all related news stories pub-
lished about the company on day t. The averaging is done across sentiment measures of all news
stories for a company on a specific day. The proposed term-frequency-inverse-document-frequency
(tf-idf) weighting scheme in Loughran and McDonald (2011) and Loughran and McDonald (2016)
is applied when calculating the news sentiment variables to take into account that some words
appear more often than others.5
4The LM dictionary is downloaded from Software Repository for Accounting and Finance, University of Notre
Dame.
5A note of caution is due here, since the LM dictionary was explicitly developed in the context of 10-K
filings. Therefore, its direct usage in other types of financial textual datasets may not yield the desired results (see
Loughran and McDonald (2020) for more details). Bearing in mind this limitation, the LM dictionary is still one
of the most widely used for sentiment analysis in finance at the time of writing.
10


## Page 11

Table 3: News Variables
Description
#
Characteristic
News count
1
Number of news stories
Positive sentiment
1
Average of positive sentiments
Negative sentiment
1
Average of negative sentiments
Uncertainty sentiment
1
Average of uncertainty sentiments
Litigious sentiment
1
Average of litigious sentiments
Weak modal sentiment
1
Average of weak modal sentiments
Moderate modal sentiment
1
Average of moderate modal sentiments
Strong modal sentiment
1
Average of strong modal sentiments
Constraining sentiment
1
Average of constraining sentiments
Notes: The first column (‘Description’) contains the variable names. The second column
(‘#’) lists the number of variables. The formula used to compile each defined variable is
shown in the third column (‘Characteristic’). All sentiment measures in this table are cal-
culated based on the LM dictionary (Loughran and McDonald, 2011). ‘News count’ is the
number of stories on that day. The average value is the daily average of the specific senti-
ment measure in the first column for all news stories for a company on that day.
3.3
LOB Variables
The LOBSTER dataset contains LOB and message data for NASDAQ-listed tickers, the latter
including the execution, submission, cancellation, and deletion of orders. The data cleaning steps
are described in Appendix A, and the CRSP dataset is used to correct stock price and volume
for stock splits, stock dividends, spin-offs, stock distributions, and rights issues.6 7 Table 4 lists
the LOB variables inspired by Kercheval and Zhang (2015) for up to ten LOB levels, giving rise
to 132 variables in total and representing a comprehensive set of LOB features. The flexibility of
ML makes it possible to include such a large and comprehensive set of LOB variables in a single
model.
These variables are designed to describe the state and dynamics of the LOB at high-frequency.
Specifically, we include basic variables such as the best bid and ask prices and volumes, which
reflect the immediate available liquidity on both sides of the LOB. In addition, we incorporate
higher-order variables that measure depth beyond the best level, spreads between quotes, mid
6We performed supplementary analysis on the LOB data by omitting the cleaning procedures to evaluate
their effect on the calculation of RV. Detailed descriptive statistics and the correlation between RVs, computed
with and without the cleaning steps, are provided in Table A2. The results show that the uncleaned data yield
descriptive statistics that closely mirror those reported in Table 1. In all instances, we observed an exceptionally
high correlation, thereby confirming the robustness of the RV calculations.
7Table C1 further examines whether differences in high-frequency data sources may contribute to discrepancies
in empirical findings. This table reports the correlation between daily RV computed from LOBSTER data and RV
constructed from NYSE TAQ data over the common training period. For the TAQ-based RV, only cleaning steps
in Appendix A that do not rely on LOB information are applied, and the same sampling frequency and aggregation
methodology are used as in the main analysis. The table documents consistently high correlations across tickers,
indicating a close alignment between RV measures derived from the two data sources despite differences in market
microstructure content and timestamp resolution. Overall, this evidence suggests that the empirical results are
unlikely to be driven primarily by the choice of data source.
11


## Page 12

Table 4: Limit Order Book Variables
Description
#
Characteristica
Parameter
Bid-ask spreads
10
[(P ask
l
−P bid
l
)]N
l=1
-
Mid prices
10
[(P ask
l
+ P bid
l
)/2]N
l=1
-
Price differences
18
[P ask
l
−P ask
1
]N
l=2, [P bid
1
−P bid
l
]N
l=2
-
Absolute price differences
18
[|P ask
l+1 −P ask
l
|]N−1
l=1 , [|P bid
l+1 −P bid
l
|]N−1
l=1
-
Mean prices
2
[ 1
N
PN
l=1 P ask
l
,
1
N
PN
l=1 P bid
l
]
-
Mean volumes
2
[ 1
N
PN
l=1 V ask
l
,
1
N
PN
l=1 V bid
l
]
-
Price/volume
accumulated differences
2
[PN
l=1(P ask
l
−P bid
l
),
PN
l=1(V ask
l
−V bid
l
)]
-
Price/volume changes
40
[∆P ask
l
, ∆P bid
l
,
∆V ask
l
, ∆V bid
l
]N
l=1
∆t = 1 day
Event-type proportionsb
10
[π(EV )bid(ask), π(EH)bid(ask), π(S)bid(ask), π(C)bid(ask), π(D)bid(ask)]
∆t = 1 day
Relative proportionsc
10
[1{π(EV )bid(ask)
∆t
>π(EV )bid(ask)
∆T
}, 1{π(EH )bid(ask)
∆t
>π(EH )bid(ask)
∆T
},
1{π(S)bid(ask)
∆t
>π(S)bid(ask)
∆T
}, 1{π(C)bid(ask)
∆t
>π(C)bid(ask)
∆T
},
1{π(D)bid(ask)
∆t
>π(D)bid(ask)
∆T
}]
∆T = 1 day,
∆t = 15 minutes
Accelerationsd
10
[∆π(EV )bid(ask), ∆π(EH)bid(ask), ∆π(S)bid(ask), ∆π(C)bid(ask), ∆π(D)bid(ask)]
∆t = 1 day
Notes: This table contains LOB variables inspired by Kercheval and Zhang (2015). The first column (‘Description’) contains the variable names.
The second column (‘#’) lists the number of variables included from 10 LOB levels. The formula used to compile each defined variable is shown
in the third column (‘Characteristic’). The fourth column (‘Parameter’) specifies the time parameter. When there is no time parameter, the last
snapshot of the LOB for a particular day is used. N denotes the number of LOB levels used per side (bid and ask); throughout we set N = 10.
Depending on the construction, level-based variables contribute 2N components when defined separately for bid and ask, and N components
when bid and ask are combined into a single statistic per level. Variables defined as deviations from the best quote (level 1) are indexed by l =
2, . . . , N and thus contribute 2(N −1) components. Also, aggregates over levels yield a fixed number of components (e.g., two when computed
once per side).
a (EV ) and (EH) denote visible and hidden executions, while (S), (C), and (D) stand for submission, cancellation, and deletion
of orders, respectively. ‘P’ and ‘V’ stand for price and volume.
b Proportion of messages of each event type and side within the window, defined as the count of events of that type divided by the total number
of messages in the window.
c This value is a one-or-zero binary number.
d First difference of the event-type proportions from ‘Event-type
proportions’.
prices, and volume imbalances, providing a richer description of the cross-sectional configuration of
liquidity. By summarising both the best levels and deeper layers of the LOB, these features allow
us to capture variations in trading pressure and market tightness. This selection encompasses
variables capturing not only the instantaneous structure of the LOB, but also its recent dynamics,
such as changes in bid and ask prices and volumes over short time intervals. We also include
event-based proportions and their short-horizon changes to capture recent trading activity.
4
Empirical Framework
RNN is a type of artificial neural network designed to recognise patterns in data sequences that
have a temporal dimension, such as financial time series. Subsection 4.1 provides a brief review of
RNN, their extension, LSTM, and regularisation techniques. Subsection 4.2 presents the structure
of the proposed ML models used in this study.
12


## Page 13

Xt
X3
X2
X1
a1
a2
...
Yt
wy,by
wx,bx
wx,bx
wx,bx
a0 
wx,bx
wa,ba
wa,ba
wa,ba
wa,ba
Figure 1: Recurrent Neural Network Abstract Representation
Notes: This representation of the RNN has t input vectors through time (X1, X2, X3, . . . , Xt) and one output
(Y t). Wx and bx are the shared weights and biases between inputs and the neural network layers for time steps 1
to t, Wa and ba are the shared weights and biases between different layers, and Wy and by are the shared weights
and biases between the last layer of the neural network and the single output (Y t). For the ease of exposition, this
illustration portrays an RNN for a single input variable. Also, in this representation, every layer has an arbitrary
number of units, which are represented by the hatched circles. a1 to at are the transferred information from one
layer to the subsequent layer, and a0 is the input vector for the first layer.
4.1
RNN and LSTM
Figure 1 is a representation of the RNN with t input vectors (X1, X2, X3, . . . , Xt) and one
output (Y t). Wx and bx are the shared weights and biases between inputs and the neural network
layers for time steps 1 to t, Wa and ba are the shared weights and biases between layers, and
Wy and by are the shared weights and biases between the last layer of the neural network and
the single output (Y t). For the ease of exposition, Figure 1 portrays an RNN for a single input
variable. Also, in this representation, every layer has an arbitrary number of units8 which are
represented by the hatched circles, a1 to at are the transferred information from one layer to the
subsequent layer, and a0 is the input vector for the first layer. at is defined as follows:
at = tanh(wax[at−1, Xt] + bax),
(9)
where wax is the stacked matrix of wa and wx, bax is the stacked matrix of ba and bx, and tanh is
the hyperbolic tangent activation function. Also, the output (Y t) is defined as follows:
Y t = tanh(wyat + by),
(10)
8A unit (neuron) is a basic building block that takes in a set of inputs, performs mathematical operations on
them, and produces a single output. Generally, an ML model with more units can be considered more complex.
13


## Page 14

where wy and by are the output weights and biases, and tanh is the hyperbolic tangent activation
function. The weights and biases in Equation (9) and Equation (10) are estimated by minimising
MSE using gradient descent with backpropagation.
RNN suffers from the vanishing-gradient
problem: the influence of early inputs on later states can decay toward zero as sequences grow
longer, limiting the ability to capture long-range dependencies.
Hochreiter and Schmidhuber (1997) use gated cells with their own sets of weights to store,
read, or erase historical information. To tackle the vanishing gradient problem, a more constant
error rate is maintained in LSTM to allow the model to continue learning over many steps. First,
define the candidate memory cell (˜ct) as:
˜ct = tanh(wc[at−1, Xt] + bc),
(11)
where wc and bc are the weights and biases of the candidate memory cell, and tanh is the hyperbolic
tangent activation function. Then, the input, forget, and output gates are defined as:
Gi = σ(wi[at−1, Xt] + bi),
(12)
Gf = σ(wf[at−1, Xt] + bf),
(13)
Go = σ(wo[at−1, Xt] + bo),
(14)
where wi and bi are the weight and bias of the input gate, wf and bf are the weight and bias
of the forget gate, wo and bo are the weight and bias of the output gate, and σ is the sigmoid
activation function. Taken together, the updated memory cell (ct) is calculated as:
ct = Gi ⊙˜ct + Gf ⊙ct−1,
(15)
where ct−1 is the memory cell at time t −1, and ˜ct is the candidate memory cell at time t from
Equation (11). The input gate controls the flow of the input activation into the memory cell,
while the forget gate scales the internal state of the cell before adding it to the memory cell.
Finally, at, the control for information flowing into the next layer, is calculated as:
at = Go ⊙tanh(ct),
(16)
14


## Page 15

where Go is the output gate in Equation (14), ct is the memory cell in Equation (15), and tanh is
the hyperbolic tangent activation function. The role of the output gate is to control the output
flow of the cell activation into the rest of the neural network. All the weights and biases are to be
learned during training. Collectively, LSTM avoids the vanishing gradient by suitably memorising
and forgetting some past states, so theoretically, it can capture long dependencies in sequential
data. Appendix B demonstrates that, under fixed gate configurations, the LSTM architecture
collapses to standard models, illustrating its role as a unifying framework.
One typical issue with ML is overfitting, i.e., when the error rate in the training set is artificially
low, but the error rate in the test data is high. In this study, we implemented L2 regularisation
and dropout, two of the most widely used regularisation techniques. The L2 regularisation works
by adding a regularisation term, λ||w||2, to the loss function, L, as follows:
L′(w; X, Y ) = L(w; X, Y ) + λ||w||2,
(17)
where L and L′ are the initial and modified loss functions, and w, X, and Y are, respectively,
the weights, inputs, and output of the ML model; ||.||2 is the squared L2 norm; and λ is the reg-
ularisation factor. The regularisation term penalises a model with larger weights. The larger the
regularisation factor, λ, the more severe the penalty. Together, λ||w||2 helps mitigate overfitting.
Moving to another regularisation technique, dropout works by randomly removing some units
along with their incoming and outgoing connections during training. As a rule of thumb, the
optimal dropout rate typically ranges between 20% and 50% of the input and hidden units (Sri-
vastava et al., 2014). The purpose of dropout is to introduce noise into the optimisation process,
making training more challenging and thereby preventing the ML model from overfitting.9
4.2
ML Model Structure
In this study, we follow the classical framework to evaluate forecasting performance by producing
out-of-sample forecasts using only ex-ante information. This means repeatedly re-estimating the
ML model using only historical information available at the time and rolling forward one step at
a time over the out-of-sample period. Such a process is extremely laborious, even without the
9In Subsection 7.6, as part of the robustness checks, the regularisation techniques are extended to include early
stopping, and its impact on the performance of ML models in forecasting RV is examined.
15


## Page 16

complexity of testing different ML models using many combinations of hyperparameters and 147
input variables for each of the 23 tickers. Instead of testing several ML models, we have decided
here to focus on LSTM and concentrate on gaining a deeper understanding of its strengths and
weaknesses in volatility forecasting.10 Recent studies have found neural networks to be superior
among some popular ML models, and among neural networks, LSTM has a structure resembling
a time series model. We believe that a detailed investigation of LSTM is crucial at this juncture
for its importance in time series analysis. Furthermore, an even more essential objective revolves
around assessing the importance of the model’s ability to forecast RV using a rich and diverse set
of predictors in a single setting.
As explained in Section 1 and Subsection 4.1, the LSTM has many unique features making it
ideal for handling sequential data, including financial time series. This model is one of the top ML
choices for modelling time series data in academia and industry. Hence, our goal here is to focus
on the LSTM, testing a wide range of hyperparameters, in order to better understand the tuning
strategy for achieving the best possible performance. We also believe that testing many models
with limited variations in tuning parameters could lead to misleading conclusions. Furthermore,
we have chosen a single-layer LSTM instead of a more complex LSTM. A simple vanilla LSTM
is chosen as it is more tractable for follow-up analyses. A simpler LSTM model is easier to train;
substantially more time, computing capacity, and data are needed for training a more complex
LSTM model. Finally, complex ML models have many more combinations of hyperparameters to
test and choose from, making the analyses more complicated and less intuitive.11
Figure 2 presents the structure of the LSTM model used in this study. For every explanatory or
predictive variable X, the sequence (Xt, Xt−1, . . . , Xt−n) is included as input to the LSTM model.
The number of outputs from the LSTM (DO) is equal to the number of units in this model. A
FCNN is used for converting DO outputs into a single forecast (RV t+1).12 Two regularisation
techniques, L2 regularisation and dropout, as described in Subsection 4.1, are implemented to
10As a robustness check, Subsection 7.5 examines the performance of a FCNN model in forecasting RV, serving
as a replacement for the LSTM model.
11Although the theoretical benefit of a deeper sequential architecture is not clear, deeper models could lead to
better performance in some specific tasks (Goldberg, 2016). With our objectives in mind and all the constraints
at hand, a multi-layer (stacked) model is left for future research.
12As highlighted by Andersen et al. (2007), considering logarithmic RV could serve as a viable approach for
controlling RV’s extreme distributions. However, as emphasised in Patton and Sheppard (2015), this alternative
approach centres on predicting log-RV rather than volatility in levels, despite the latter typically being more
relevant for economic applications. In alignment with the approach taken by Bollerslev et al. (2016) and consistent
with the prevailing literature on the HAR-family of models, this study uses the raw RV formulation instead of
log-RV.
16


## Page 17

Fully connected 
neural network
LSTM
n lags
Input variables
DO
RVt+1
Xt
Xt-1
Xt-2
Xt-3
Xt-4
Xt-5
Xt-6
Xt-n
Figure 2: ML Model Structure
Notes: For every input variable (X), n lags of that variable (Xt, Xt−1, . . . , Xt−n) are included as input variables
to the LSTM model. The number of outputs of the LSTM (DO) is equal to the number of units in the LSTM
model. An FCNN converts the DO outputs of the LSTM to a single RV t+1.
avoid overfitting.
The ML technical specifications implemented here are as follows: the optimisation algorithm
is ADAM (Kingma and Ba, 2014). ADAM is an adaptive learning rate optimisation algorithm
based on stochastic gradient descent. The initial learning rate is set to 0.001, and a separate
learning-rate schedule with decay coefficient 10−5 is applied. For both the LSTM and FCNN,
kernel and bias L2 regularisation are applied with regularisation coefficient 10−4. The second
regularisation technique, dropout, is applied between the LSTM and FCNN with a rate of 0.5.
For the LSTM, the sigmoid activation function is used for the input, forget, and output gates,
while the hyperbolic tangent activation function is used for the candidate cell update and for
the cell-state output when computing the hidden state. Also, for FCNN, the rectifier activation
function13 is chosen.14 For the primary experiments in Section 5, MSE is used as the loss function,
and the number of epochs is set to 50. The LSTM is tested with 5, 10, 15, 20, and 25 units. The
FCNN consists of a single layer.
In the primary experiments presented in Section 5, 21 lags (corresponding to n = 20 in Figure 2)
are employed for all input variables, aligning with the structure of the HAR model. However, the
13A unit with the rectifier activation function is called a rectified linear unit (ReLU).
14The choice of hyperparameters adopted here is consistent with the default values used in the literature and
common practices. Certain hyperparameters, such as the learning-rate schedule coefficient and the L2 regulari-
sation coefficient, are chosen through trial and error. While the robustness checks in Section 7 provide valuable
insights into the sensitivity of the choice of loss function, and the number of units and epochs, there are other
hyperparameters that could impact model performance. Because of the extensive number of models trained in
this study and the computational intensity involved, investigating the simultaneous impact exerted by all hyper-
parameters is beyond the scope of this research. Therefore, a potential avenue for future research would be to
extend the robustness analysis to include a more comprehensive examination of model performance sensitivity to
the choice of hyperparameters.
17


## Page 18

Table 5: Number of Independent Variables and Parameters of Models
Group
HAR-Family of Models
Model
AR(1)
HAR
HAR-J
CHAR
SHAR
ARQ
HARQ
HARQ-F
Number of Variables
1
3
4
3
4
2
4
6
Number of Parameters
2
4
5
4
5
3
5
7
Group
ML Models
Model
HAR-ML
News-ML
OB-ML
News/OB-ML
Number of Variables
6 × NoLa
15 × NoL
138 × NoL
147 × NoL
Number of Parameters (5 Units)b
246c
426
2,886
3,066
Number of Parameters (10 Units)
691
1,051
5,971
6,331
Number of Parameters (15 Units)
1,336
1,876
9,256
9,796
Number of Parameters (20 Units)
2,181
2,901
12,741
13,461
Number of Parameters (25 Units)
3,226
4,126
16,426
17,326
Notes: HAR-ML contains only the HAR-family variables described in Subsection 3.1. News-ML augments the HAR-family vari-
ables with all news variables described in Subsection 3.2. OB-ML augments the HAR-family variables with all LOB variables
described in Subsection 3.3. Finally, News/OB-ML includes the HAR-family, news, and LOB variables simultaneously. Hence,
all ML models are built on the HAR-family baseline, and the additional blocks capture the incremental contribution of news
and LOB information.
a Number of lags (i.e., 21 for the primary experiments).
b Number of units in the LSTM model.
c In a single-layer LSTM, let p represent the number of input features and h the number of hidden units. The total number of
trainable parameters is given by 4h(p + h + 1) + (h + 1), because each of the four gates (input, forget, cell, and output) con-
tributes h(p + h + 1) parameters: comprising an input-weight matrix of size p × h, a recurrent-weight matrix of size h × h, and
a bias vector of length h. Additionally, the final dense (output) layer adds h weights and one bias. Consequently, for the HAR–
ML case where p = 6 inputs and h = 5 units, the total number of trainable parameters is 4 × 5(6 + 5 + 1) + 5 + 1 = 246.
number of variables included in the ML model is far greater than that included in HAR, even
with the restriction to 21 lags. All predictive variables are standardised by removing the mean
and scaling to unit variance. The standardisation is executed every day when the window is rolled
forward, using only the data in the relevant window.15
Table 5 shows the number of variables and parameters for the HAR-family of models (top
panel) and the ML model variants (bottom panel).
The ML models clearly use more input
variables than the HAR models.
Combining all datasets, the News/OB-ML model uses 147
features per time step and a sequence length of 21 lags, corresponding to 147× 21 input elements
per observation, whereas the AR(1) model relies on a single input variable. The ability to deal
with nonlinear relationships in a high-dimensional environment is a vital feature of ML models.
Note also that adding more lags to the ML models does not change the number of parameters in
the LSTM model; only the number of variables and the number of units determines the number
of parameters. For each of the 23 tickers, only the data for that ticker are used for training.
The same seed in the random number generator (RNG) is also used for all models to ensure
reproducible results.
15In accordance with the HAR model structure, the input sequence length for the primary experiment is set to
21. For the robustness checks in Subsection 7.1, we experimented with sequence lengths set to 5 and 1.
18


## Page 19

5
Out-of-Sample Forecasting Results
The entire sample period of 27 July 2007 to 27 January 2022 was separated into an in-sample train-
ing period from 27 July 2007 to 11 September 2015 (2,046 days) and an out-of-sample forecasting
period from 14 September 2015 to 27 January 2022 (1,604 days).16 Following Poon and Granger
(2003), the model’s forecasting power is judged only according to the out-of-sample forecasting
performance. To maintain consistency with the estimation and implementation procedures of the
HAR-family of models, all ML models in this study are retrained daily using a rolling window
approach. To better understand the forecasting performance on normal versus high volatility
days, we classify high volatility days whenever the RV is greater than Q3 + 1.5 × IQR, where Q1
and Q3 are the first and third quartiles, respectively, and IQR = Q3 −Q1. Normal volatility
days are defined as all trading days excluding those classified as high volatility. This classification
is applied separately for each ticker, using only data from the out-of-sample period. Based on
this definition and averaging across all tickers, about 10% (160 days) of the out-of-sample period
(1,604 days) are classified as high volatility days. We have purposefully avoided parametric jump
estimation as it is sensitive to the assumption of the stock price dynamics and the bandwidth
adopted for data frequency.17 We consistently noticed that the forecasting of normal and high
volatility requires different ML specifications and different information sets. Thus, as long as the
out-of-sample forecasts are separated into a main set of normal observations and a smaller set of
extreme observations (i.e., high volatility days), regardless of the method used to separate them,
our findings and conclusions should continue to hold.
To better understand the characteristics of high volatility days, Figure 3 illustrates the monthly
distribution of high volatility days over the out-of-sample period. High volatility days are identi-
fied at the individual-ticker level based on the RV distribution and aggregated to monthly counts
for each asset. The horizontal axis denotes calendar months, while the vertical axis reports the
number of high volatility days per month for a given ticker. Black markers correspond to in-
dividual assets, the solid line reports the cross-sectional monthly average, and the shaded band
represents one standard deviation around this average. Consistent with the empirical classifica-
16To ensure comparability, both the in-sample estimation and the out-of-sample forecasting should reflect similar
data characteristics. Hence, the selection of in-sample and out-of-sample periods is also driven by the desire to
include days with extreme volatility in both periods. In particular, the in-sample period encompasses the 2008
financial crisis, while the out-of-sample period includes the COVID-19 disruptions.
17The distinction between normal and high RVs is not known a priori; it is solely made ex post for the purpose
of comparing out-of-sample performance.
19


## Page 20

2015−11
2016−05
2016−11
2017−05
2017−11
2018−05
2018−11
2019−05
2019−11
2020−05
2020−11
2021−05
2021−11
Month
0
5
10
15
20
Number of High Volatility Days
Ticker
Monthly Average
Figure 3: Number of High Volatility Days per Month over the Out-of-Sample Period
Notes: The figure shows the monthly frequency of high volatility days for individual tickers over the out-of-sample
period. The horizontal axis corresponds to calendar months, and the vertical axis reports the number of days
within each month classified as high volatility for a given asset. Black-filled markers represent individual tickers,
illustrating cross-sectional dispersion in volatility dynamics. The solid line denotes the cross-sectional average
number of high volatility days per month, while the shaded band represents one standard deviation across tickers.
tion, high volatility days account for a relatively small fraction of the out-of-sample observations.
Nevertheless, the figure shows that these days are observed throughout the sample and across as-
sets, with pronounced variation during time and substantial cross-sectional heterogeneity. While
their frequency increases during periods of heightened market-wide RV like COVID-19 around
2020, high volatility days are not confined to a small number of isolated episodes. This pattern
suggests that elevated RV reflects both market-wide risk factors, such as shifts in aggregate uncer-
tainty or risk premia, while the majority of observations are attributable to asset-specific episodes
of heightened volatility driven by idiosyncratic events, for example firm-level information arrivals,
liquidity shocks, and flash crashes.
We use the reality check (RC) to test the forecasting performance of the ML model against
every model in the HAR-family.
In line with White (2000) and Bollerslev et al. (2016), the
stationary bootstrap of Politis and Romano (1994) with 999 re-samplings and an average block
length of 5 is used for this test.18 The hypotheses of the test are defined as follows:
H0 : Min
k=1,...,n E[Lk(RV, X) −L0(RV, X)] ≤0,
H1 : Min
k=1,...,n E[Lk(RV, X) −L0(RV, X)] > 0,
(18)
where Lk is the loss measure of the kth out of n benchmark HAR models, which include AR(1),
18Our analysis shows that the results are not sensitive to the choice of block length.
20


## Page 21

HAR, HAR-J, CHAR, SHAR, ARQ, HARQ, and HARQ-F, and L0 is the loss measure of the
target ML model. Rejection of the null hypothesis indicates that Lk > L0 for all k, meaning the
ML model outperforms the HAR-family of models jointly.
Following Patton (2011), the MSE and QLIKE loss functions are chosen for measuring the RV
forecasting performance, in addition to the mean directional accuracy (MDA) metric. According
to Patton (2011), the MSE and QLIKE loss functions are among the family of robust and ho-
mogeneous loss functions for volatility forecasting comparison.19 Rankings of volatility forecasts
based on these loss functions are robust to noise in the proxy, and the rankings are invariant to
the choice of units of measurement. On the other hand, MDA is a useful measure complementing
these two cardinal measures, especially for monitoring the overfitting of the models. The three
loss functions are defined as follows:
MSE(RVt, d
RV t) ≡1
N
N
X
t=1
(RVt −d
RV t)2,
(19)
QLIKE(RVt, d
RV t) ≡1
N
N
X
t=1
 RVt
d
RV t
−log( RVt
d
RV t
) −1

,
(20)
MDA(RVt, RVt−1, d
RV t) ≡1
N
N
X
t=1
1{sign(RVt −RVt−1) = sign(d
RV t −RVt−1)},
(21)
where RVt is the true RV at time t, d
RV t is the forecast RV at time t, N is the number of
days in the out-of-sample period, and sign(·) and 1{·} denote the sign and indicator functions,
respectively. Following Bollerslev et al. (2016), if the forecast RV is larger (smaller) than the
maximum (minimum) of the RV in the estimation series, it is replaced by the average of the RV
in the estimation series.
To select the best-performing model among the HAR-family of models, we assess both in-
sample and out-of-sample forecasting performance across all HAR-type specifications. Table C2
reports parameter estimates and in-sample evaluation metrics aggregated across 23 stocks, includ-
ing adjusted R2, MSE, QLIKE, and MDA. The results indicate that the CHAR model provides
the strongest and most stable in-sample performance, achieving the highest average and median
adjusted R2, as well as the lowest average and median MSE and the lowest average QLIKE
among competing HAR-family of models. While differences in MDA across models are generally
19See Poon and Granger (2003) for a review of the volatility performance metrics.
21


## Page 22

modest, CHAR remains competitive in terms of directional accuracy. The estimated coefficients
across models are broadly consistent with theoretical expectations and prior empirical findings.
Table C3 reports forecasting performance over the full out-of-sample period, as well as separately
for normal and high volatility days.
Consistent with the in-sample evidence, CHAR delivers
the lowest average and median MSE and QLIKE over the full out-of-sample period and domi-
nates alternative HAR specifications according to the RC across both volatility regimes, while
also exhibiting competitive MDA across subsamples. Although some models, such as HAR-J or
HARQ-F, perform well under specific metrics or market conditions, their performance gains are
not systematic. This evidence identifies CHAR as the best-performing model within the HAR-
family, and we therefore adopt it as the benchmark. We also observe a clear pattern in Table C3:
the out-of-sample performance of all HAR-family of models deteriorate substantially during high
volatility days. This is evidenced by elevated MSE and QLIKE values, indicating that these
models systematically fail to forecast high volatility days prior to their realisation.
We compare the out-of-sample forecasting performance of four groups of ML models, differing
by their information sets, against the benchmark CHAR model as the best-performing HAR
model. If we define, for ticker i, and for each ML model j,
ρMSE,i,j = MSEML
i
(Modelj)
MSEOLS
i
(CHAR),
(22)
ρQLIKE,i,j = QLIKEML
i
(Modelj)
QLIKEOLS
i
(CHAR),
(23)
ρMDA,i,j = MDAOLS
i
(CHAR)
MDAML
i
(Modelj) ,
(24)
where j = 1, 2, 3, 4 is one of the four groups of ML models in Table 5, and i = 1, . . . , 23
identifies each of the 23 tickers. For the ML models, j = 1 corresponds to HAR-ML, and the HAR
variables are described in Subsection 3.1; j = 2 is News-ML, and the news variables are described
in Subsection 3.2; j = 3 is OB-ML, and the LOB variables are described in Subsection 3.3; and
finally, j = 4 is News/OB-ML, i.e., the news and LOB variables combined. It is worth noting
that News-ML, OB-ML, and News/OB-ML also contain the HAR variables. In this context, a
value of one indicates no difference in performance relative to the benchmark. A value below one
reflects better performance compared to the benchmark, whereas a value above one represents
worse performance relative to the benchmark.20
20In Equation (24), the numerator and denominator for the MDA metric are inverted to ensure that lower
22


## Page 23

Next, the ML model j’s average ρMSE/QLIKE/MDA,j for the 23 tickers are:
Average ρMSE,j = 1
23
23
X
i=1
ρMSE,i,j,
(25)
Average ρQLIKE,j = 1
23
23
X
i=1
ρQLIKE,i,j,
(26)
Average ρMDA,j = 1
23
23
X
i=1
ρMDA,i,j,
(27)
while Median ρMSE,j, Median ρQLIKE,j, and Median ρMDA,j are the median equivalents of Equa-
tion (25), Equation (26), and Equation (27), respectively.
5.1
Full Out-of-Sample Period
Table 6 reports the average and median ρMSE/QLIKE/MDA for the four groups of ML models,
with 21 lags of every group of variables included and different numbers of units (5, 10, 15, 20,
and 25). The corresponding RC value is the percentage of tickers with better ML performance,
in terms of MSE, QLIKE, or MDA, at the 5% and 10% significance levels against every model
in the HAR-family of models (AR(1), HAR, HAR-J, CHAR, SHAR, ARQ, HARQ, and HARQ-
F). For cardinal forecasts evaluated using MSE and QLIKE, and considering the RC results,
improvement in forecasting performance is clear, especially for the HAR-ML and OB-ML groups.
However, the results in Table 6 are mixed. In all cases and for all groups of ML models, the
average and median values show degradation in performance compared to the CHAR model as
a benchmark. For directional forecasts evaluated using MDA, ML outperformed CHAR in most
specifications, delivering the largest improvement: about 4% overall and 100% for RC, primarily
within the OB-ML and News/OB-ML groups. Taken together, except for the MDA loss function,
consistent improvements are noticeable only from the RC results.21
However, by separating
values correspond to better forecasting performance.
21Table 6 indicates that, over the full out-of-sample period, ML underperformed in terms of average and median
MSE and QLIKE relative to the strongest benchmark, but outperformed in terms of RC when evaluated against
the full set of benchmark models. The ρ-metrics quantify the magnitude of the forecast-error gap between each ML
specification and the single strongest benchmark (CHAR). In contrast, the RC statistic assesses, for each ticker,
whether the ML model significantly outperforms all members of the entire HAR-family of models (AR, HAR, HAR-
J, CHAR, SHAR, ARQ, HARQ, HARQ-F), and reports the percentage of tickers for which the null hypothesis is
rejected. Hence, an ML specification may yield ρ-values slightly above one, indicating a marginal loss to CHAR,
yet still record a high RC if it dominates several other HAR variants across most tickers. The two statistics,
therefore, capture distinct but complementary dimensions of forecast performance.
When both metrics align,
the ranking is unambiguous; when they diverge, ρ quantifies the shortfall against the top-performing benchmark,
while RC reflects the extent of statistically significant gains across the broader benchmark set. Following standard
practice in forecast evaluation, we retain both metrics, as this dual perspective mitigates model-selection bias and
23


## Page 24

24
Table 6: Out-of-Sample Volatility Forecasting Performance
14 September 2015 to 27 January 2022 (1,604 days)
HAR-ML
News-ML
OB-ML
News/OB-ML
Units
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
Full Out-of-Sample Period
MSEa
Avg
1.225
1.199
1.182
1.161
1.146
1.229
1.204
1.182
1.166
1.150
1.209
1.179
1.156
1.144
1.174
1.216
1.178
1.157
1.151
1.138
Med
1.198
1.180
1.160
1.139
1.119
1.198
1.179
1.160
1.139
1.123
1.178
1.174
1.136
1.125
1.151
1.186
1.154
1.145
1.147
1.123
RCd
5%
13.04
34.78
39.13
56.52
73.91
17.39
26.09
39.13
52.17
73.91
26.09
39.13
56.52
73.91
78.26
17.39
39.13
47.83
69.57
78.26
10%
47.83
60.87
82.61
86.96
100
52.17
60.87
82.61
91.30
95.65
60.87
73.91
91.30
100
100
65.22
69.57
86.96
91.30
95.65
QLIKEb
Avg
8.081
3.881
2.517
1.742
1.391
7.787
4.258
2.600
2.004
1.526
4.816
2.335
1.656
1.525
2.082
6.174
2.210
1.678
1.636
1.455
Med
6.879
3.321
2.185
1.569
1.305
7.596
4.154
2.474
1.743
1.352
3.178
1.996
1.504
1.442
1.922
5.142
1.878
1.528
1.473
1.386
RC
5%
0.00
0.00
0.00
0.00
13.04
0.00
0.00
0.00
4.35
8.70
0.00
4.35
0.00
8.70
13.04
0.00
0.00
0.00
0.00
8.70
10%
0.00
4.35
17.39
34.78
60.87
0.00
0.00
4.35
8.70
43.48
4.35
8.70
13.04
17.39
21.74
0.00
8.70
13.04
21.74
17.39
MDAc
Avg
1.015
0.993
0.973
0.969
0.969
1.016
0.999
0.974
0.964
0.961
0.967
0.946
0.938
0.942
0.963
0.992
0.943
0.938
0.944
0.952
Med
1.001
0.988
0.969
0.968
0.972
0.999
0.990
0.970
0.964
0.963
0.952
0.945
0.941
0.947
0.964
0.969
0.937
0.928
0.945
0.953
RC
5%
65.22
91.30
95.65
100
100
65.22
82.61
95.65
95.65
100
78.26
91.30
100
100
100
69.57
91.30
100
100
100
10%
69.57
95.65
95.65
100
100
65.22
86.96
95.65
100
100
86.96
95.65
100
100
100
73.91
91.30
100
100
100
Notes: The best value in each row is marked in bold.
a The mean (or median) MSE ratio of ML to CHAR for 23 tickers. A ratio above one indicates degradation, while below one indicates improvement.
b The mean (or median) QLIKE ratio of ML to CHAR for 23 tickers. A ratio above one indicates degradation, while below one indicates improvement.
c The mean (or median) MDA ratio of CHAR to ML for 23 tickers.
A ratio above one indicates degradation, while below one indicates improvement.
d Percentage of tickers with the outstanding performance of ML against the HAR-family of models at the 5% and 10% significance levels.


## Page 25

the out-of-sample actual RVs into normal and high volatility days, a clearer picture emerged in
Subsection 5.2 below.22
5.2
Normal vs High Volatility Days
Table 7 reports the results for normal and high volatility days separately. First, consider the
top panel of Table 7, which corresponds to normal volatility days and, on average, accounts for
90% of the out-of-sample forecast period. The four groups of ML models outperform the CHAR
model, as the average and median MSE and QLIKE values are mostly below one. When using
the MSE measure, RC values are 100% in all but one case. When using QLIKE, RC is near
100% in many cases. This provides strong evidence supporting the superior forecasting power of
ML models compared to all HAR-family of models on normal volatility days. The substantial
improvement is also evident in the MDA loss function, with directional forecasting performance
increasing by around 11% in the best-performing model. Among the four ML model groups,
OB-ML and News/OB-ML perform the best. In general, a higher number of units corresponds
to better forecasting performance on normal volatility days.23
The results for high volatility days in the bottom panel of Table 7 present a completely different
picture. All four groups of ML models underperformed the CHAR model, as the average/median
MSE/QLIKE values are all above one. When the MSE measure is used, the RC values are low,
most of which are below 50%, and even worse when QLIKE is used. Likewise, the MDA loss
function results show deterioration in forecasting performance. These sharply contrasting results
strengthens the robustness of our inference.
22To better understand the impact of the rule governing the replacement of RV forecasts that fall outside the
estimation-sample range on the results in Section 5, Table C4 reports summary statistics for the HAR-family of
models across 23 tickers. The table shows that such forecast replacements occur very infrequently for all HAR
specifications, with zero or near-zero counts for most models. Table C5 reports the corresponding statistics for
the ML models across alternative model classes and sizes. While forecast replacements occur more frequently
for ML models, particularly for smaller models and richer information sets, their frequency declines markedly as
model complexity increases. Overall, these results indicate that extreme forecast replacements are more common
for ML models than for HAR-family of models, but remain limited relative to the total number of out-of-sample
observations (1,604 days) and vary systematically with model specification rather than occurring uniformly across
ML architectures.
23The finding that adding LOB variables to the ML models substantially improves forecasting performance,
particularly on normal volatility days, contradicts Rahimikia and Poon (2020), which found that news variables
had stronger predictive power than LOB variables. The contradictory finding could be due to the fact that the
ML model here has a large number of predictors, whereas in Rahimikia and Poon (2020), 10 LOB variables and
9 news sentiment measures were added, only one at a time, to the CHAR model. In contrast, News/OB-ML, the
largest ML model tested here, has 147 predictors, i.e., 132 LOB variables, 9 news variables, and 6 HAR variables,
all included and tested in a single ML model. Hence, apart from the ability to capture nonlinear relationships as
highlighted in Christensen et al. (2023), the ability of the ML model to fit a large number of predictors jointly
significantly amplifies its forecasting accuracy, particularly on normal volatility days.
25


## Page 26

26
Table 7: Out-of-Sample Volatility Forecasting Performance: Normal vs High Volatility Days
14 September 2015 to 27 January 2022 (1,604 days)
HAR-ML
News-ML
OB-ML
News/OB-ML
Units
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
Normal Volatility Days
MSEa
Avg
0.699
0.618
0.573
0.571
0.584
0.704
0.658
0.605
0.600
0.628
0.540
0.468
0.474
0.527
0.554
0.611
0.467
0.493
0.516
0.578
Med
0.669
0.591
0.578
0.587
0.562
0.640
0.635
0.597
0.591
0.655
0.478
0.386
0.433
0.471
0.576
0.492
0.436
0.429
0.488
0.543
RCd
5%
100
100
100
100
100
91.30
100
100
100
100
100
100
100
100
100
100
100
100
100
100
10%
100
100
100
100
100
91.30
100
100
100
100
100
100
100
100
100
100
100
100
100
100
QLIKEb
Avg
4.770
2.132
1.263
1.041
0.926
4.819
2.682
1.499
1.192
1.036
2.701
1.153
0.924
0.951
1.099
3.948
1.100
0.953
1.029
0.976
Med
3.721
1.484
1.001
0.985
0.928
4.098
2.018
1.362
1.090
1.010
1.524
0.871
0.892
0.950
1.010
2.331
0.913
0.906
0.921
0.977
RC
5%
4.35
30.44
65.22
78.26
100
0.00
4.35
39.13
65.22
73.91
39.13
65.22
86.96
82.61
82.61
21.74
65.22
78.26
86.96
82.61
10%
4.35
34.78
69.57
82.61
100
0.00
4.35
39.13
78.26
86.96
39.13
65.22
86.96
82.61
82.61
21.74
73.91
82.61
91.30
86.96
MDAc
Avg
0.954
0.941
0.925
0.928
0.936
0.956
0.944
0.925
0.920
0.923
0.904
0.888
0.890
0.900
0.918
0.928
0.885
0.890
0.898
0.916
Med
0.951
0.943
0.927
0.933
0.936
0.938
0.935
0.925
0.917
0.923
0.899
0.892
0.892
0.896
0.921
0.905
0.882
0.887
0.907
0.915
RC
5%
86.96
95.65
100
100
100
82.61
91.30
100
100
100
100
100
100
100
100
91.30
100
100
100
100
10%
86.96
95.65
100
100
100
86.96
91.30
100
100
100
100
100
100
100
100
95.65
100
100
100
100
High Volatility Days
MSE
Avg
1.245
1.220
1.204
1.182
1.166
1.249
1.224
1.203
1.186
1.169
1.233
1.205
1.181
1.167
1.196
1.238
1.205
1.181
1.174
1.159
Med
1.218
1.199
1.183
1.169
1.141
1.221
1.204
1.186
1.163
1.151
1.197
1.200
1.164
1.152
1.170
1.210
1.182
1.172
1.167
1.145
RC
5%
0.00
8.70
26.09
30.44
39.13
0.00
8.70
21.74
26.09
43.48
4.35
17.39
26.09
34.78
39.13
8.70
21.74
26.09
30.44
34.78
10%
30.44
39.13
47.83
56.52
69.57
26.09
39.13
39.13
47.83
73.91
30.44
43.48
52.17
56.52
69.57
26.09
43.48
52.17
60.87
65.22
QLIKE
Avg
11.425
5.613
3.759
2.428
1.844
11.027
5.907
3.728
2.819
2.007
6.963
3.512
2.383
2.108
3.040
8.513
3.307
2.406
2.228
1.948
Med
8.998
4.679
3.348
2.044
1.695
11.270
6.232
3.261
2.426
1.810
4.962
3.096
2.241
1.992
2.857
6.077
3.304
2.326
2.045
1.765
RC
5%
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
0.00
0.00
4.35
0.00
0.00
0.00
0.00
4.35
10%
0.00
4.35
4.35
0.00
13.04
0.00
0.00
0.00
4.35
17.39
4.35
4.35
0.00
4.35
4.35
4.35
0.00
0.00
4.35
4.35
MDA
Avg
1.070
1.066
1.063
1.059
1.062
1.070
1.064
1.062
1.059
1.057
1.069
1.065
1.063
1.059
1.059
1.069
1.064
1.060
1.056
1.050
Med
1.058
1.058
1.058
1.049
1.050
1.058
1.058
1.058
1.054
1.054
1.058
1.058
1.054
1.054
1.050
1.058
1.058
1.054
1.056
1.050
RC
5%
0.00
0.00
0.00
4.35
8.70
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
0.00
0.00
4.35
10%
0.00
0.00
0.00
4.35
13.04
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
0.00
0.00
4.35
Notes: The best value in each row is marked in bold.
a The mean (or median) MSE ratio of ML to CHAR for 23 tickers. A ratio above one indicates degradation, while below one indicates improvement.
b The mean (or median) QLIKE ratio of ML to CHAR for 23 tickers. A ratio above one indicates degradation, while below one indicates improvement.
c The mean (or median) MDA ratio of CHAR to ML for 23 tickers. A
ratio above one indicates degradation, while below one indicates improvement.
d Percentage of tickers with the outstanding performance of ML against the HAR-family of models at the 5% and 10% significance levels.


## Page 27

27
0
20
40
60
80
100
Full Out-of-Sample
1.00
1.05
1.10
1.15
1.20
Full Out-of-Sample
HAR
News
OB
News/OB
MSE (avg)
MSE (med)
0
20
40
60
80
100
Normal Volatility Days
CHARx
0.4
0.6
0.8
1.0
1.2
Normal Volatility Days
Negative
Positive
Uncertainty
Litigious
Modalweak
Modalmoderate
Modalstrong
Constraining
News count
T1slope10
T1slope(10bid)
T1slope(10ask)
T1slope5
T1slope(5bid)
T1slope(5ask)
T2slope10
T2slope5
Depth10
Depth5
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
0
20
40
60
80
100
High Volatility Days
1.00
1.05
1.10
1.15
1.20
1.25
High Volatility Days
Reality Check (%)
Diﬀerence
(a) Forecast Evaluation under MSE
0
20
40
60
80
100
Full Out-of-Sample
1
2
3
4
5
6
7
8
Full Out-of-Sample
HAR
News
OB
News/OB
QLIKE (avg)
QLIKE (med)
0
20
40
60
80
100
Normal Volatility Days
CHARx
1.0
1.5
2.0
2.5
3.0
3.5
4.0
4.5
5.0
Normal Volatility Days
Negative
Positive
Uncertainty
Litigious
Modalweak
Modalmoderate
Modalstrong
Constraining
News count
T1slope10
T1slope(10bid)
T1slope(10ask)
T1slope5
T1slope(5bid)
T1slope(5ask)
T2slope10
T2slope5
Depth10
Depth5
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
0
20
40
60
80
100
High Volatility Days
2
4
6
8
10
High Volatility Days
Reality Check (%)
Diﬀerence
(b) Forecast Evaluation under QLIKE
Notes: The bar chart shows the percentage of tickers with outstanding performance considering the MSE loss function in Figure 4a and the QLIKE loss function in Figure 4b
at the 5% significance level of the RC compared to the HAR-family of models as the benchmark for each specified CHARx model (grey bars) and the ML model (white bars).
The values for the bar chart can be read from the left-hand axis. The dashed (solid) line shows the average (median) out-of-sample MSEs and QLIKEs of the CHAR relative to
the CHARx models (left group) and ML models (right group) across 23 tickers. A value below one indicates improved performance of the ML model, while a value above one
indicates degradation. The values for the dashed and solid lines can be read from the right-hand axis. The horizontal dashed line represents no improvement.
Figure 4: Comparison of ML and CHARx Models


## Page 28

to normal volatility days suggest that the ML models fitted to the full in-sample period, dominated
by normal volatility days, are not appropriate for forecasting the infrequent high volatility days.
One possible explanation for these contrasting results could be due to RV’s persistence differing
on high versus normal volatility days. It is widely documented that volatility is highly persistent,
but not when volatility is extreme.
Volatility half-life is much shorter for extreme volatility
compared to the normal level of volatility.24
This is the first and most important clue that
separate modelling considerations are needed for normal versus high volatility regimes. Here, as
we did not separate the normal and high volatility days, the optimisation was driven by the 90%
of normal volatility days’ forecast evaluations. Nevertheless, although the high volatility days
constitute only 10% of the out-of-sample period, the poor performance of the ML models during
high volatility days strongly indicates that these models, particularly in their basic form without
additional adjustments to the RV definition and/or the model itself, might be economically less
useful. This is because precise forecasts of high volatility days hold greater importance in a risk
management scenario compared to days with low volatility. Our findings show that ML models
trained using the full in-sample period did not perform well on the 10% of (non-consecutive day)
daily volatility forecasts when the actual (non-consecutive day) daily RVs are very high. This is
different from the finding in Bucci (2020), which studied monthly S&P 500 volatility and found
good forecasting performance from ML models during the Great Recession high volatility period
from September 2007 to June 2009, which may include many days when the index volatility was
at a ‘normal’ level. Our sample of individual tickers will have more idiosyncratic volatility that
does not persist and is more challenging to forecast.25
We further extend our analysis by comparing ML models with the CHARx model proposed
by Rahimikia and Poon (2020), which augments the original CHAR model in Subsection 2.1 by
incorporating variables derived from news and LOB data from the previous day to forecast daily
RV. In Figure 4, the white (grey) bar reports the RC values for a specific ML model (CHARx)
24In the individual tickers analyses and the robustness checks later, we also find very different ML modelling
considerations for normal versus high volatility days.
25As discussed in Section 5, the results are based on a rolling window approach with a fixed in-sample training
period of 2,046 days. To further assess the robustness of our findings, we re-estimated all models using an increasing
window approach; the corresponding results are presented in Table C7. In a second experiment, we shortened
the in-sample training period from 2,046 days to 1,604 days, holding all other parameters constant; the results
of this robustness check are reported in Table C8. In both cases, the CHAR benchmark model was re-estimated
to match the respective training setup, using an increasing window in the first case and the shortened in-sample
period in the second. Both sets of results are consistent with our main conclusions. Forecasting performance
improves on normal volatility days, but deteriorates on high volatility days, which in turn negatively impacts the
full out-of-sample performance. Consistent with earlier findings, the OB-ML and News/OB-ML models continue
to exhibit the strongest performance among the four ML model groups.
28


## Page 29

against all HAR-family of models. The dashed (solid) line represents the out-of-sample average
(median) ρMSE in Figure 4a, and the average (median) ρQLIKE in Figure 4b. The news variables
in the CHARx model are defined in Subsection 3.2.
The LOB variables include the ‘type 1
modified slope’ (Næs and Skjeltorp, 2006), the ‘type 2 slope’ (Kalay et al., 2004), and the ‘LOB
depth’. A variable name, ‘T1slope(5bid)’, means ‘type 1 slope’ aggregated from the first five
levels on the bid side of the LOB. If a LOB variable name does not contain ‘ask’ or ‘bid’, it means
that it is calculated using both the bid and ask sides of the LOB. The results are reported for
the full out-of-sample period (top panel), for days with normal volatility (middle panel), and for
days with high volatility (bottom panel).
The most striking result in Figure 4 is the superior forecasting performance of the ML models
compared to CHARx for normal volatility days.
In contrast, all four groups of ML models
performed poorly on high volatility days. News count and LOB depth are the only variables
that, when added to the CHAR model, help to forecast RV on high volatility days.
In the
full out-of-sample period, the CHARx models demonstrate superior performance, particularly
in terms of RC metrics, with notable improvements observed when the news count variable is
incorporated into the CHAR model. The results for MDA presented in Figure C1 broadly support
these findings, viz., a significant improvement in RV forecasting performance on normal volatility
days when switching from CHARx to ML, but significant degradation in performance on high
volatility days. For the full out-of-sample evaluation, interestingly, the ML models substantially
improve performance in terms of both magnitude and RC metrics compared to the CHARx model.
These findings from the MDA provide evidence that the ML models are effectively capturing the
dynamics of RV, suggesting that the risk of overfitting is relatively low.
Combining all results, the findings suggest that no single model consistently outperforms others
in forecasting RV. While ML models demonstrate strong performance on days characterised by
normal volatility, their effectiveness diminishes during periods of high volatility, which becomes
evident over the full out-of-sample evaluation period. Moreover, the choice of performance metric
significantly influences model assessment. In particular, when using MDA, ML models emerge
as clear outperformers not only during normal volatility days but also across the entire out-of-
sample period. However, this advantage comes at the expense of reduced forecasting accuracy
during high volatility days. These results indicate that, in their current architectures, ML models
may not serve as direct substitutes for HAR-family of models. Instead, they can be viewed as
29


## Page 30

complementary models that enhance forecasting performance when used alongside HAR-family
of models. Moreover, following the characteristics of high volatility days documented in Sec-
tion 5, we find that excluding these rare high volatility episodes that are predominantly driven by
asset-specific shocks, while the remaining episodes are largely attributable to systematic factors,
leads to a significant improvement in RV forecasting performance when employing ML models.
Although numerous ML models have already been tested, further analysis is necessary to ensure
the generalisability of the results. This includes exploring variations in input variables, model
architectures, training parameters, and model types, among others, to confirm that the findings
are not specific to this particular evaluation framework.26
5.3
ML with Limited Feature Set
This subsection examines three distinct limited information sets. Beginning with the first two,
the first set comprises the past 21 lags of RV, while the second includes the previous day’s
RV, the average RV over the past week, and the average RV over the past month. The results
are presented in Figure 5, where Φt = {RVt, ..., RVt−20} for the LSTM model in Figure 5a,
and Φt = {RVt, RV
w
t−1, RV
m
t−1} for the simpler FCNN model in Figure 5b.27 The FCNN with
three input variables is equivalent to the HAR model structure but with a potentially nonlinear
relationship. The MSE is presented on the left and the QLIKE loss on the right. The full out-
of-sample period is shown at the top, followed by normal volatility days in the middle, and high
volatility days at the bottom.
In both Figure 5a and Figure 5b under MSE for normal volatility days, the ML model, generally
with a higher number of units, continues to outperform CHAR and the HAR-family of models.
The average and median ρMSE are below one in all cases. The RC values are also close to 100%
26Table C6 repeats the main out-of-sample comparison in Table 6 and Table 7, but replaces CHAR with the
standard HAR model as the benchmark. Relative to the CHAR-benchmarked ratios, HAR-benchmarked ratios are
uniformly closer to one, reflecting that HAR is a weaker baseline than CHAR and therefore easier to outperform.
Importantly, this change in benchmark does not alter the substantive conclusions drawn from the CHAR-based
analysis. First, the same regime dependence is preserved: ML models continue to deliver sizable improvements on
normal volatility days, while underperforming during high volatility days, with the latter capable of dominating
performance over the full out-of-sample period. Second, the relative ordering across model variants and sizes is
largely preserved.
27The FCNN has a simple structure, unlike the LSTM. It consists of only three layers, viz. input, hidden,
and output layers. The size of the input layer is the same as the number of input variables. The hidden layer
size varies from 5, 10, 15, 20, to 25. The size of the output layer is equal to the number of output(s), which
is one in this study. The dropout rate between the hidden layer and the output layer is set equal to 0.5. The
activation functions are sigmoid and rectifier, respectively, for the hidden and output layers. The other ML model
specifications remained unchanged.
30


## Page 31

0
10
20
30
40
50
Full Out-of-Sample
1.00
1.05
1.10
1.15
1.20
MSE (avg)
MSE (med)
0
20
40
60
80
100
Normal Volatility Days
0.65
0.70
0.75
0.80
0.85
0.90
0.95
1.00
5
10
15
20
25
0
5
10
15
20
25
30
35
High Volatility Days
1.00
1.05
1.10
1.15
1.20
1.25
0
1
2
3
4
1
2
3
4
5
6
7
8
9
Full Out-of-Sample
QLIKE (avg)
QLIKE (med)
0
10
20
30
40
50
19
1
2
3
4
5
6
Normal Volatility Days
5
10
15
20
25
−0.04
−0.02
0.00
0.02
0.04
32
2
4
6
8
10
12
High V olatility Days
Reality Check (%)
Diﬀerence
(a) LSTM with Φt = {RVt, ..., RVt−20}
0.0
2.5
5.0
7.5
10.0
12.5
15.0
17.5
Full Out-of-Sample
1.00
1.05
1.10
1.15
1.20
MSE (avg)
MSE (med)
0
20
40
60
80
Normal Volatility Days
0.80
0.85
0.90
0.95
1.00
5
10
15
20
25
0
2
4
6
8
10
12
High Volatility Days
1.00
1.05
1.10
1.15
1.20
−0.04
−0.02
0.00
0.02
0.04
1
2
3
4
5
6
7
8
Full Out-of-Sample
QLIKE (avg)
QLIKE (med)
−0.04
−0.02
0.00
0.02
0.04
19
1
2
3
4
5
6
Normal Volatility Days
5
10
15
20
25
−0.04
−0.02
0.00
0.02
0.04
32
2
4
6
8
10
High V olatility Days
Reality Check (%)
Diﬀerence
(b) FCNN with Φt = {RVt, RV
w
t−1, RV
m
t−1}
Figure 5: ML Models with Limited Information Sets
Notes: The bar chart shows the percentage of tickers with outstanding performance considering the MSE (left figures)
and QLIKE (right figures) loss functions at the 5% significance level of the RC compared to the HAR-family of models
as the benchmark for each specified number of units of the ML model. The values for the bar chart can be read from
the left-hand axis. The dashed (solid) line shows the average (median) out-of-sample MSEs and QLIKEs of the ML
model relative to the CHAR model across 23 tickers. A value below one indicates improved performance of the ML
model, while a value above one indicates degradation. The values for the dashed and solid lines can be read from the
right-hand axis. The horizontal dashed line represents no improvement.
31


## Page 32

in many cases. As before, the ML models perform poorly on high volatility days. However,
results under QLIKE are less marked compared to those under MSE, especially for FCNN (as
compared to LSTM). Furthermore, a comparison between Figure 5 and Figure 4 clearly indicates
that limiting the predictors to include only the history of RV and HAR variables significantly
degrades forecasting performance for normal volatility days. This deterioration is evident not
only in contrast to models with a greater number of predictors such as OB-ML and News/OB-
ML, but also when compared to the smaller scale HAR-ML model. Hence, consistent with the
outcomes presented in Subsection 5.2, aside from nonlinearity, a diverse range of data features
plays a crucial role in the ML model’s RV forecasting performance. When extending the analysis
to the full out-of-sample period, the results remain broadly consistent with previous findings.
However, since substantially less data are used as input, the performance deterioration is more
severe, both in terms of magnitude and the RC metric.
The MDA results in Figure C2 for
LSTM and in Figure C3 for FCNN produce findings consistent with the discussion here.28 These
findings again suggest that while ML models are effective under normal market conditions, their
performance weakens during periods of high volatility, ultimately limiting their performance over
the full out-of-sample period.
Turning to the third restricted information set, a key question is whether the superior per-
formance of the OB-ML group, as documented in Subsection 5.1 and Subsection 5.2, can be
attributed to the greater number of variables incorporated in the model. To examine this, we
constrain the set of LOB variables employed in the OB-ML model to correspond with the CHARx
specification, as detailed in Figure 4. Specifically, keeping all model specifications and parameters
consistent with those outlined in Subsection 4.2, we include only a subset of LOB variables: the
LOB depth on both bid and ask sides, type 1 slope from the bid side, ask side, and jointly, as
well as type 2 slope. These variables are computed using both 5 and 10 levels of the LOB, and
are also used in Figure 4 and Figure C1, where each variable is added individually to the base
CHAR model in separate specifications. As mentioned, we use all input variables collectively in
the LSTM model. Consequently, to construct the limited version of OB-ML, as before, we also
28ML provides a substantial MDA improvement over the HAR-family of models on normal volatility days. In
some cases, the improvement exceeds 6%, and the RC values approach 100%. Nevertheless, ML performance is
poor on high volatility days, and this is more marked when using only three variables in the FCNN compared
to the LSTM model with the past history of RV. Extending the analysis to the full out-of-sample period, the
improvement is clearly noticeable in Figure C2, but not in Figure C3, which uses only three input variables. We
also see that, compared to the MDA results for the primary experiment in Figure C1, this obtained improvement
in performance is weaker. These findings again highlight the critical role of using a diverse range of data features
in enabling ML models to achieve gains.
32


## Page 33

include the HAR-family variables, which decreases the total number of input variables from 138
in Table 5 to 16.
Figure 6 presents the results for the OB-ML, as defined in Subsection 3.3, alongside those for
a restricted version of the OB-ML that incorporates a reduced set of variables, as defined above.
The first five bars represent the results obtained using the LOB information set, while the second
five bars are those derived from the limited LOB information set. It is evident that across the full
out-of-sample period, as well as when normal and high volatility days are considered separately,
the OB-ML group of models with access to the full information set consistently demonstrates
superior forecasting performance. This finding is strongly supported by the RC results in nearly all
cases. Although the magnitude of improvement, as reflected in both average and median values,
exhibits some variation, the overall enhancement in forecasting performance remains evident
when transitioning from the limited to full LOB information set. Furthermore, the MDA results
presented in Figure C4 further support this conclusion. Overall, even when considering a limited
number of LOB variables, an improvement in forecasting performance is observed; however, the
gains are not as substantial as those achieved when a larger set of LOB variables is utilised.
5.4
Evaluation of Individual Tickers
To understand the changes in forecasting performance at the ticker and model levels, this sub-
section analyses the ρMSE,i and ρQLIKE,i between the ML model (OB-ML with 15 units as one
of the best-performing ML specifications in Table 7) and each of the HAR-family of models29
using radar plots in Figure 7. The MSE results are shown on the left and the QLIKE results on
the right. The top figure corresponds to full out-of-sample days, the middle figure to days with
normal volatility, and the bottom figure to high volatility days. A ρ below one indicates that the
ML model outperformed, while a ρ above one indicates that it underperformed. The bold inner
circle represents ρ = 1, i.e., no difference in performance.
For normal volatility days in Figure 7b, it is apparent that OB-ML outperformed every model
in the HAR-family of models, as ρMSE and ρQLIKE are mostly lower than one and lie inside the
bold circle for most of the tickers. For high volatility days, presented in Figure 7c at the bottom,
most ρMSE and ρQLIKE are above one and lie outside the bold circle, i.e., ML underperformed
29That is, AR(1), HAR, HAR-J, CHAR, SHAR, ARQ, HARQ, and HARQ-F.
33


## Page 34

34
0
10
20
30
40
50
60
70
80
Full Out-of-Sample
1.00
1.05
1.10
1.15
1.20
Full Out-of-Sample
OB
OB(Limited)
MSE (avg)
MSE (med)
0
20
40
60
80
100
Normal Volatility Days
0.4
0.5
0.6
0.7
0.8
0.9
1.0
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
0
5
10
15
20
25
30
35
40
High Volatility Days
1.00
1.05
1.10
1.15
1.20
High Volatility Days
Reality Check (%)
Diﬀerence
(a) Forecast Evaluation under MSE
0
2
4
6
8
10
12
Full Out-of-Sample
1
2
3
4
5
6
Full Out-of-Sample
OB
OB(Limited)
QLIKE (avg)
QLIKE (med)
0
20
40
60
80
Normal Volatility Days
1.0
1.5
2.0
2.5
3.0
3.5
4.0
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
0
1
2
3
4
High Volatility Days
1
2
3
4
5
6
7
8
9
High Volatility Days
Reality Check (%)
Diﬀerence
(b) Forecast Evaluation under QLIKE
Notes: The bar chart is the percentage of tickers with the outstanding performance considering the MSE loss function in Figure 6a and the QLIKE loss function in Figure 6b at
the 5% significance level of the RC compared to the HAR-family of models as the benchmark for every specified model. The first five bars represent the results obtained using the
LOB information set in Subsection 3.3, while the second five bars are those derived from the limited LOB information set. The dashed (solid) line shows the average (median)
out-of-sample MSEs and QLIKEs of the ML model relative to the CHAR model across 23 tickers. A value below one indicates improved performance of the ML model, while a
value above one indicates degradation. The values for the dashed and solid lines can be read from the right-hand axis. The horizontal dashed line represents no improvement.
Figure 6: Comparison of OB-ML and OB-ML (Limited) Models


## Page 35

all HAR-family of models. The ρMSE and ρQLIKE are also large for six tickers, viz. ‘NVDA’,
‘AMAT’, ‘ADSK’, ‘MU’, ‘NTAP’ and ‘KLAC’. From the descriptive statistics of RV in Table 1,
the RV of ‘MU’ has a very high standard deviation, while the RVs of ‘NVDA’, ‘AMAT’, ‘ADSK’,
‘NTAP’ and ‘KLAC’ exhibit very high skewness. When moving to the full out-of-sample period
in Figure 7a, a clear degradation in performance is observed for most tickers, as well as across
the various benchmark models. The MDA results presented in Figure C5 align with those from
MSE and QLIKE above. However, in line with the previous findings, for the full out-of-sample
period, the improvement is clear for many tickers.30
These results again confirm the previous findings that the ML model dominates the HAR-
family of models on normal volatility days but underperforms on high volatility days, especially for
tickers exhibiting extreme volatility distributions. Moreover, in line with the results in Section 5,
the red dotted line, representing CHAR, lies closest to the bold circle, suggesting that CHAR
has the best forecasting performance among the HAR-family of models, albeit not as good as
ML. Additionally, there are some substantial differences in the forecasting performance of HAR-
family of models on both normal and high volatility days, with some exhibiting much worse
performance than CHAR. Once again, the results reveal a consistent pattern: ML models perform
well under certain volatility conditions, while the HAR-family of models performs better under
others, indicating that each approach excels under distinct volatility dynamics. Also, the MDA
again clearly shows an improvement in performance for the full out-of-sample period, which is
not the case for the MSE and QLIKE loss functions.
Figure 8 uses a box plot to present the distribution of true RV and the forecast RVs from the
OB-ML model with 15 and 25 units, as well as from CHAR. For clarity, the RV values on the y-
axis are truncated at 100%. The points above each box plot indicate high volatility days. Several
important observations can be made here. CHAR produced some forecasts that are classified as
high volatility days, whereas the ML models rarely generated forecasts that fall into this category.
CHAR’s RV forecasts were more conservative compared to the actual RV, and the ML models
produced even more conservative forecasts, capped at around 20%. Consequently, both performed
30Consistent with the previous results, Figure C5 shows that for normal volatility days (middle figure), all the
ρMDA values lie inside the bold circle, indicating that ML substantially outperformed every model in the HAR-
family of models. In some cases, this improvement approaches 20%. In contrast, on high volatility days (right
figure), ML underperformed the HAR-family of models for many tickers. Over the full out-of-sample period (left
figure), all points fall within the circle, again demonstrating improved performance for the majority of tickers and
benchmark models.
35


## Page 36

poorly on high volatility days. Closer inspection of other HAR-family of models revealed a similar
pattern. In general, the HAR-family of models produced forecasts with higher means and standard
deviations during the out-of-sample period than those of the ML models.31 This is one of the
reasons for the poor forecasting performance of the ML models on high volatility days. Increasing
the number of units in the ML model raises both the mean and standard deviation of the RV
forecasts, resulting in better performance on such days.
This behaviour can be better understood through an analogy with large language models
(LLMs). For instance, image-generation models often produce clocks displaying 10:10, an adver-
tising convention common in training data due to its visual symmetry. Analogously, ML models
are trained on data dominated by normal volatility days, leading them to focus on forecasting
these typical conditions. As a result, they perform well during normal volatility days but struggle
on rarer high volatility days. This imbalance in the training data biases model learning and
contributes to the performance asymmetry observed. This issue is further exacerbated by the
high capacity of ML models to capture complex nonlinear patterns, which makes them more
sensitive to such imbalances. In contrast, linear models, while less flexible, are more robust on
high volatility days, at the cost of significantly reduced forecasting performance during normal
volatility days.
31The forecasts from AR(1), HAR, HAR-J, CHAR, SHAR, ARQ, HARQ, and HARQ-F exceed the true RV
in, respectively, 77.6%, 78.7%, 79.8%, 80.2%, 78.6%, 78.0%, 78.8%, and 77.6% of cases (average across 23 tickers),
while the OB-ML forecasts with 15 and 25 units exceed the true RV in 59.5% and 65.0% of cases, respectively. The
standard deviations of forecasts from the eight models under the HAR-family exceed that of OB-ML with 15 units
(25 units) in, respectively, 91.3%, 100%, 100%, 100%, 100%, 100%, 100%, and 100% (82.6%, 100%, 100%, 100%,
100%, 100%, 100%, and 100%) of the 23 tickers. This further underscores the fundamentally different behaviour
of these two types of models in RV forecasting.
36


## Page 37

AAPL
MSFT
INTC
CMCSA
QCOM
CSCO
EBAY
GILD
TXN
AMZN
SBUX
NVDA
MU
AMAT
NTAP
ADBE
XLNX
AMGN
VOD
CTSH
KLAC
PCAR
ADSK
MSE
0.2
0.4
0.6
0.8
1.0
1.2
1.4
AAPL
MSFT
INTC
CMCSA
QCOM
CSCO
EBAY
GILD
TXN
AMZN
SBUX
NVDA
MU
AMAT
NTAP
ADBE
XLNX
AMGN
VOD
CTSH
KLAC
PCAR
ADSK
QLIKE
0.25
0.50
0.75
1.00
1.25
1.50
1.75
(a) Full Out-of-Sample Period
AAPL
MSFT
INTC
CMCSA
QCOM
CSCO
EBAY
GILD
TXN
AMZN
SBUX
NVDA
MU
AMAT
NTAP
ADBE
XLNX
AMGN
VOD
CTSH
KLAC
PCAR
ADSK
MSE
0.2
0.4
0.6
0.8
1.0
AAPL
MSFT
INTC
CMCSA
QCOM
CSCO
EBAY
GILD
TXN
AMZN
SBUX
NVDA
MU
AMAT
NTAP
ADBE
XLNX
AMGN
VOD
CTSH
KLAC
PCAR
ADSK
QLIKE
0.2
0.4
0.6
0.8
1.0
1.2
(b) Normal Volatility Days
AAPL
MSFT
INTC
CMCSA
QCOM
CSCO
EBAY
GILD
TXN
AMZN
SBUX
NVDA
MU
AMAT
NTAP
ADBE
XLNX
AMGN
VOD
CTSH
KLAC
PCAR
ADSK
MSE
0.2
0.4
0.6
0.8
1.0
1.2
1.4
AAPL
MSFT
INTC
CMCSA
QCOM
CSCO
EBAY
GILD
TXN
AMZN
SBUX
NVDA
MU
AMAT
NTAP
ADBE
XLNX
AMGN
VOD
CTSH
KLAC
PCAR
ADSK
QLIKE
0.5
1.0
1.5
2.0
2.5
3.0
3.5
AR
HAR
HAR-J
CHAR
SHAR
ARQ
HARQ
HARQ-F
AR
HAR
HAR-J
CHAR
SHAR
ARQ
HARQ
HARQ-F
(c) High Volatility Days
Figure 7: ρMSE and ρQLIKE between OB-ML (15 units) and HAR-Family of Models
Notes: Each radar chart illustrates the performance of the OB-ML model with 15 units relative to the AR(1),
HAR, HAR-J, CHAR, SHAR, ARQ, HARQ, and HARQ-F models across the specified tickers. The evaluations
are conducted over the full out-of-sample period (Figure 7a), during normal volatility days (Figure 7b), and during
high volatility days (Figure 7c). The left and right radar charts present results based on the MSE and QLIKE loss
functions, respectively. A value below one indicates improved performance of the ML model, while a value above
one indicates degradation. The bold circle represents the baseline (no improvement, i.e., a value of one).
37


## Page 38

38
AAPL
ADBE
ADSK
AMAT
AMGN
AMZN
CMCSA
CSCO
CTSH
EBAY
GILD
INTC
KLAC
MSFT
MU
NTAP
NVDA
PCAR
QCOM
SBUX
TXN
VOD
XLNX
0
20
40
60
80
100
RV (%)
True RV
AAPL
ADBE
ADSK
AMAT
AMGN
AMZN
CMCSA
CSCO
CTSH
EBAY
GILD
INTC
KLAC
MSFT
MU
NTAP
NVDA
PCAR
QCOM
SBUX
TXN
VOD
XLNX
0
20
40
60
80
100
CHAR
AAPL
ADBE
ADSK
AMAT
AMGN
AMZN
CMCSA
CSCO
CTSH
EBAY
GILD
INTC
KLAC
MSFT
MU
NTAP
NVDA
PCAR
QCOM
SBUX
TXN
VOD
XLNX
0
20
40
60
80
100
OB-ML (15 Units)
AAPL
ADBE
ADSK
AMAT
AMGN
AMZN
CMCSA
CSCO
CTSH
EBAY
GILD
INTC
KLAC
MSFT
MU
NTAP
NVDA
PCAR
QCOM
SBUX
TXN
VOD
XLNX
0
20
40
60
80
100
Ticker
OB-ML (25 Units)
Figure 8: True and Forecast RVs from OB-ML and CHAR
Notes: From left to right, the box plots show the distribution of the true RVs, the forecast RVs from the OB-ML models with 15 and 25 units, and CHAR, respectively.
For clarity, the RV on the y-axis is truncated at 100%. The points above each box plot represent high volatility days.


## Page 39

6
XAI
ML models are often described as ‘black boxes’. In this section, an XAI technique is employed to
enhance our understanding of the relative importance of various features used in RV forecasting.
We calculate the SHAP (SHapley Additive exPlanations) values for the set of 147 (i.e., six HAR,
nine news, and 132 LOB) variables included in the News/OB-ML model with 15 units, represent-
ing the middle number of units we tested. Instead of using the best-performing ML model, we use
News/OB-ML because this model group includes all variables, and the goal here is to examine
the explanatory power of each variable in the set. Lundberg and Lee (2017) introduced SHAP as
a type of sensitivity analysis within the realm of XAI techniques. The Shapley value ϕi, defined
below, measures the importance of variable i:
ϕi =
1
|N|!
X
S⊆N\{i}
|S|! (|N| −|S| −1)! [f(S ∪{i}) −f(S)],
(28)
where N = 147 is the total number of variables included in the News/OB-ML model, S represents
all possible subsets from N \ {i} (i.e., the set of 146 variables after excluding the ith variable),
f(S ∪{i}) −f(S) is the change in RV forecast by adding variable i to the set S, and |N| is the
number of variables in N. |S|! and (|N| −|S| −1)! show the number of ways the chosen and the
remaining set of variables may be presented. The resulting value is the average contribution to RV
forecasts of the input variable ith. In this study, we utilise a high-speed approximation algorithm
called Deep SHAP, based on DeepLIFT (Deep Learning Important FeaTures; Shrikumar et al.
(2017)).32 For each of the 23 tickers, we calculate SHAP for every day in the out-of-sample period.
A variable is among the most important variables for each ticker when it is among the top 10%
(i.e., 15 out of 147 variables), and also appears in the list at least 50% of the time (i.e., 802 out
of 1,604 days) in the out-of-sample period.
The consolidated results across 23 tickers are reported in Table 8, displaying the number of
times each variable is chosen as an important variable. The findings clearly indicate that primary
financial variables, including ‘Mid prices’ (at various LOB levels from 1 to 10), ‘Mean bid’, and
32DeepLIFT attributes neural network outputs to input features by comparing activations to a reference state
and propagating resulting differences back through the network. Deep SHAP extends this approach by integrating
Shapley values from cooperative game theory, thereby combining the computation efficiency of DeepLIFT with the
theoretical rigour of SHAP. By leveraging DeepLIFT’s backpropagation mechanism and averaging over multiple
reference baselines, Deep SHAP provides an efficient approximation of SHAP values while preserving their desirable
properties.
39


## Page 40

Table 8: Variable Aggregate Importance
Mid price (L1)
13a
Relative proportion (S/bid)
3
Relative proportion (D/ask)
1
Mid price (L7)
11
News count
2
Relative proportion (C/ask)
1
Mean price (bid)
10
Relative proportionV (E/ask)
2
Relative proportionV (E/bid)
1
Mean price (ask)
9
Mean volume (bid)
2
Bid-ask spreads (L2)
1
Mid price (L4)
9
Mean volume (ask)
2
Event proportionV (E/ask)
1
Mid price (L6)
8
Bipower variation (BPV)
2
Price difference (L7/bid)
1
Mid price (L10)
8
Event proportion (S/ask)
2
AccelerationsV (E/bid)
1
Mid price (L3)
8
Event proportion (C/ask)
2
Price difference (L9/bid)
1
Mid price (L9)
7
Price difference (L4/ask)
2
Volume change (L4/bid)
1
Mid price (L8)
7
Price difference (L2/bid)
2
Volume change (L6/bid)
1
Price difference (L6/ask)
6
Price difference (L10/bid)
2
Price difference (L2/ask)
1
Mid price (L2)
6
Volume change (L10/bid)
2
Price difference (L6/bid)
1
Mid price (L5)
5
Price difference (L6/bid)
2
Event proportion (C/bid)
1
Event proportionH (E/bid)
4
Price difference (L3/ask)
2
Event proportion (D/bid)
1
Price difference (L2/ask)
4
Price difference (L5/ask)
1
AccelerationsH (E/ask)
1
Price difference (L3/bid)
3
Volume change (L3/ask)
1
Accelerations (S/bid)
1
Relative proportion (S/ask)
3
Price difference (L5/bid)
1
Event proportion (S/bid)
1
Relative proportion (C/bid)
3
Price difference (L1/bid)
1
AccelerationsH (E/bid)
1
Relative proportion (D/bid)
3
Relative proportionH (E/ask)
1
Uncertainty sentiment
1
Notes: ‘L’ stands for the level of the LOB. ‘E’, ‘S’, ‘C’, and ‘D’ stand for execution, submission, cancellation, and deletion
of orders, respectively. For execution, ‘V’ and ‘H’ denote visible and hidden execution, respectively.
a The number of times the indicated variable is chosen as an important variable among the 23 tickers.
‘Mean ask’, are among the most important variables. It is also dominated by LOB variables.
Only three non-LOB variables are included in Table 8, viz., BPV from the list of HAR variables,
and ‘News count’ and ‘Uncertainty’ from the set of news variables.33
Finally, many complex
LOB-derived variables are chosen as important variables but only for a few tickers, suggesting
idiosyncratic behaviour among individual tickers.34
Next, we made an information set comparison in terms of the groups’ forecasting performance
in the out-of-sample period. The top chart in Figure 9 shows the daily SHAP average importance
(across 23 tickers) of HAR, LOB, and news variable groups. The y-axis displays the normalised
importance of the three variable groups at the daily level, with values summing to one for each
day. The bottom chart shows the daily RVs of the NASDAQ-100 (with a 5-minute sampling
interval) downloaded from the Oxford-Man Institute of Quantitative Finance Realised Library.35
What stands out from Figure 9 is that the HAR variables exhibited the lowest overall importance,
except during sporadic episodes of heightened volatility. HAR’s dominating importance during
the COVID-19 disruption and the extremely high volatility period in early 2020 is very prominent.
The out-of-sample period can also be separated into a pre-2018 low-volatility period and a post-
33Similarly, Rahimikia and Poon (2020) found that, among all the news variables, ‘News count’ is the most
powerful for forecasting RV.
34Zhu et al. (2023) found that the key variables for RV forecasting within ML models are primarily sourced
from high-frequency returns. However, the findings of this study suggest that broadening the range of features
may alter this perspective. Specifically, it becomes evident that primary variables from various levels of the LOB
are informative for accurate RV forecasting.
35A note of caution is due here, since there are some missing daily RVs in this library.
40


## Page 41

2016
2017
2018
2019
2020
2021
2022
0.2
0.4
0.6
0.8
Average Importance
HAR
LOB
NEWS
2016
2017
2018
2019
2020
2021
2022
Date
0.000
0.001
0.002
0.003
0.004
0.005
0.006
RV
RV (NASDAQ −100)
Figure 9: Average Variable Importance vs Market RV (Out-of-Sample)
Notes: The top chart shows the daily SHAP average importance (across 23 tickers) of the HAR variable group
in Subsection 3.1, the news variable group in Subsection 3.2, and the LOB variable group in Subsection 3.3.
This analysis uses News/OB-ML (15 units) to cover all variables together. The y-axis displays the normalised
importance of the three variable groups at the daily level, with values summing to one for each day. The bottom
chart shows the daily RVs of the NASDAQ-100 (5-min) downloaded from the Oxford-Man Institute of Quantitative
Finance Realised Library.
2018 period populated by many episodes of fluctuating volatility.
Before 2018, the variable
importance across all three information sets remained largely stable. The variable importance of
news sentiment dominated LOB and HAR variables before 2018, when the market was calm. Post-
2018, the variable importance of news sentiment steadily declined and was dominated by LOB
variables. There were a few short time intervals when the importance of news sentiment variables
dominated, but these did not coincide with the timing of the most volatile periods. In summary,
it is clear that (i) the importance of the three information sets varied through time, (ii) some
predictors are more informative during extremely volatile periods, while other predictors are more
informative during normal volatility periods, and (iii) the elevated importance of HAR variables
is consistent with the findings reported in Subsection 5.4. Nevertheless, although the ML models
assign greater importance to HAR variables during periods of high volatility, its performance still
falls short of that achieved by the HAR-family of models under these conditions. The flexible
ML structure (where there is no fixed time chain, and past information is flexibly controlled by
the LSTM gates at every time step) can accommodate the complex patterns in (i), (ii), and
(iii). Moreover, the inherent flexibility of the ML model in integrating a wide array of predictive
variables plays a crucial role in driving these results.
41


## Page 42

7
Robustness Checks
Up to now, all results in Section 5 show that the ML model with LOB variables outperformed
the HAR-family of models for forecasting RV on normal volatility days, but not on high volatility
days. This is also reflected in the forecasting performance over the full out-of-sample period,
where the HAR-family of models generally outperform ML models. In this section, we perform
a series of robustness checks for this conclusion by using time-restricted input information in
Subsection 7.1, using QLIKE (instead of MSE) as the loss function in Subsection 7.2, testing a
large combination of hyperparameters in Subsection 7.3 and Subsection 7.4, changing the model
architecture from LSTM to FCNN in Subsection 7.5, and adding additional safeguards against
overfitting in Subsection 7.6. Apart from the experimented parameters in each subsection, all
other model specifications are the same as those adopted in Subsection 4.2.
7.1
Restricted Number of Lags
One could argue that the forecasting performance of ML is solely attributable to the extensive
historical information it utilises. Here, we restrict all input variables to have five lags (equivalent
to one week) and one lag (i.e., the previous day). An LSTM with one lag (one input and one
output) reduces to a standard neural network. Figure 10 presents the average (dashed line) and
median (solid line) of ρMSE and ρQLIKE, as well as the RC values (bar chart).
The results show that restricting the information set from 21 days in Figure 4 to 5 days and 1
day did not change the superior performance of the ML models for normal volatility days when
evaluated using MSE. Additionally, the QLIKE results are comparatively weaker for both the
5-day and 1-day cases relative to our primary experiment, particularly when a smaller amount
of information is utilised. The 1-day results are also weaker than the 5-day results. Consistent
with previous findings, the ML models continue to face challenges in forecasting RV on high
volatility days, resulting in weaker performance over the full out-of-sample period. Similar to
the results on normal and high volatility days, the achieved performance over the full out-of-
sample period is also weaker than that observed in the primary experiment. The MDA results
presented in Figure C6 are consistent with previous findings, further reinforcing earlier patterns
and highlighting the superior performance of the models in directional forecasting.36 Due to the
36For normal volatility days, the RC values of ML models are high, and many reach 100%. The improvement
in MDA by switching from CHAR to ML varies between 2% to 10% for ML with different numbers of units and
42


## Page 43

(a) Forecast Evaluation under MSE
(i) Five Lags
0
10
20
30
40
50
60
70
Full Out-of-Sample
1.00
1.05
1.10
1.15
1.20
Full Out-of-Sample
HAR
News
OB
News/OB
MSE (avg)
MSE (med)
0
20
40
60
80
100
Normal Volatility Days
0.5
0.6
0.7
0.8
0.9
1.0
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
0
5
10
15
20
25
30
35
40
High Volatility Days
1.00
1.05
1.10
1.15
1.20
1.25
High Volatility Days
Reality Check (%)
Diﬀerence
(ii) One Lag
0
5
10
15
20
25
30
35
Full Out-of-Sample
1.00
1.05
1.10
1.15
1.20
Full Out-of-Sample
HAR
News
OB
News/OB
MSE (avg)
MSE (med)
0
20
40
60
80
100
Normal Volatility Days
0.5
0.6
0.7
0.8
0.9
1.0
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
0
5
10
15
20
High Volatility Days
1.00
1.05
1.10
1.15
1.20
1.25
High Volatility Days
Reality Check (%)
Diﬀerence
(b) Forecast Evaluation under QLIKE
(i) Five Lags
0
1
2
3
4
Full Out-of-Sample
2
4
6
8
10
Full Out-of-Sample
HAR
News
OB
News/OB
QLIKE (avg)
QLIKE (med)
0
10
20
30
40
50
60
70
Normal Volatility Days
1
2
3
4
5
6
7
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
0
1
2
3
4
High Volatility Days
2
4
6
8
10
12
14
High Volatility Days
Reality Check (%)
Diﬀerence
(ii) One Lag
−0.04
−0.02
0.00
0.02
0.04
Full Out-of-Sample
2
4
6
8
10
12
14
Full Out-of-Sample
HAR
News
OB
News/OB
QLIKE (avg)
QLIKE (med)
0
5
10
15
20
Normal Volatility Days
2
4
6
8
10
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
−0.04
−0.02
0.00
0.02
0.04
High Volatility Days
2.5
5.0
7.5
10.0
12.5
15.0
17.5
High Volatility Days
Reality Check (%)
Diﬀerence
Figure 10: ML Models with Restricted Number of Lags
Notes: The left and right figures show the results considering five lags (last week) and one lag (last
day), respectively. The bar chart shows the percentage of tickers with outstanding performance,
considering the MSE/QLIKE loss function at the 5% significance level of the RC compared to the
HAR-family of models as the benchmark for each HAR-ML, News-ML, OB-ML, and News/OB-ML
group. The values for the bar chart can be read from the left-hand axis. The dashed (solid) line
shows the average (median) out-of-sample MSEs and QLIKEs of the ML model relative to the CHAR
model across 23 tickers. A value below one indicates improved performance of the ML model, while
a value above one indicates degradation. The values for the dashed and solid lines can be read from
the right-hand axis. The horizontal dashed line represents no improvement.
43


## Page 44

good performance of ML models even in the case of a restricted number of lags, we also conclude
that our findings of superior ML forecasting performance on normal volatility days are due not
only to the larger historical information set it has access to but also to its model structure.
(a) Normal Volatility
0.0
0.5
1.0
1.5
2.0
2.5
3.0
3.5
4.0
0
2
4
6
8
Loss
QLIKE
MSE
RV = 2
d
RV < RV
d
RV > RV
(b) High Volatility
0
20
40
60
80
100
120
0
500
1000
1500
2000
2500
3000
Loss
QLIKE
MSE
RV = 80
d
RV < RV
d
RV > RV
Figure 11: A Representation of MSE and QLIKE Loss Functions
Notes: This figure presents the shape of the MSE and QLIKE loss functions. The vertical dashed line denotes
the true RV, which equals 2 in panel (a) and 80 in panel (b). Forecast values located to the left of the true RV
correspond to underprediction, d
RV < RV , whereas values to the right correspond to overprediction, d
RV > RV .
7.2
MSE vs QLIKE as Loss Function
All the ML model results produced so far are based on minimising MSE as the loss function in
the training period while using MSE and QLIKE in forecast evaluation. Here, we test whether
changing the loss function to minimising QLIKE will change the results and conclusions. Accord-
ing to Patton (2011), MSE and QLIKE are members of a family of robust and homogeneous loss
functions, L (·), shown below:
L(RV , d
RV ; b) =


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


1
(b+1)(b+2)(RV b+2 −d
RV
b+2) −
1
b+1d
RV
b+1(RV −d
RV ),
for b ̸∈{−1, −2}
d
RV −RV + RV (log(RV
d
RV )),
for b = −1
RV
d
RV −log(RV
d
RV ) −1,
for b = −2,
(29)
where L is the loss function, RV is the true RV, d
RV is the fitted (forecasted) RV, and b is the scalar
parameter. For b = 0, L becomes MSE, and L becomes QLIKE if b = −2. Figure 11 presents
the shape of these two loss functions, setting the true RV (vertical dashed line) equal to 2 (in
different numbers of lagged variables. It is also evident that the results for the 1-day are weaker than those for
the 5-day, and that incorporating additional information as input improves the performance of the ML models.
In summary, these results show that ML outperforms the HAR-family of models in RV forecasting for normal
volatility days, even with only 1 and 5 lags instead of 21 lags. This is further reflected in the full out-of-sample
results, which exhibit RC values approaching 100% and up to a 4% improvement in MDA for both the 5-day and
1-day cases.
44


## Page 45

Figure 11a) and 80 (in Figure 11b). Forecast values located to the left of the true RV correspond to
underprediction, d
RV < RV , whereas values to the right correspond to overprediction, d
RV > RV .
Compared to MSE, QLIKE is asymmetric and penalises large under-forecasts more than large
over-forecasts. Patton and Sheppard (2015) found, in volatility forecasting, that the power of
DMW tests (Diebold and Mariano (1995) and West (1996)) is higher when the loss function
is QLIKE instead of MSE, suggesting that QLIKE might be a better loss function for ranking
competing volatility forecasting models.
As a robustness check, we compare MSE versus QLIKE as the loss function for training the
ML models, while all other model specifications remain unchanged. QLIKE (as in Equation (20)
and Equation (29)) is undefined when d
RV ≤0. To address this limitation and prevent the loss
function from becoming undefined during training, we append a Lambda layer after the FCNN.
This layer enforces a lower bound on the predicted RV, ensuring that d
RV ≥0.01 and thus remains
strictly positive.37 The results are presented in Figure 12. Figure 12a (Figure 12b) evaluates the
forecasts under MSE (QLIKE), while the left (right) figure within each subfigure shows the results
for the ML models trained using minimising MSE (QLIKE) as the loss function.
As before, there are substantial gains from ML models, improving forecasts on normal volatility
days but with a performance degradation on high volatility days. Figure 12a shows that changing
the MSE to the QLIKE loss function causes a substantial degradation in forecasting performance
for high volatility days.
Considering both RC and the average and median ρMSE values for
normal volatility days, the degradation is evident but not as severe as on high volatility days.
Further analysis of forecasts evaluated under the QLIKE loss function in Figure 12b shows a
similar but more severe degradation pattern in performance when switching to the QLIKE loss
function.
It can be seen that the degradation for normal volatility days is high; many RC
values are near zero, and all the average and median ρQLIKE values are above one, indicating
substantial degradation in forecasting performance. Moving to high volatility days, incorporating
the QLIKE loss function in the training process changes all RC values to zero with substantial
degradation in ρQLIKE values. The results for the full out-of-sample period are also consistent
with previous findings and indicate that using QLIKE instead of MSE leads to degradation in
performance under both MSE and QLIKE metrics, with the effect being more pronounced for
37Another way of ensuring d
RV > 0 is to change the scalar parameter, b, to very close to −2, such as −1.99 or
−2.01 in Equation (29). In order to maintain consistency with the other experiments, this method is not utilised
in this study.
45


## Page 46

(a) Forecast Evaluation under MSE
(i) MSE Loss Function
0
10
20
30
40
50
60
70
80
Full Out-of-Sample
1.00
1.05
1.10
1.15
1.20
Full Out-of-Sample
HAR
News
OB
News/OB
MSE (avg)
MSE (med)
0
20
40
60
80
100
Normal Volatility Days
0.4
0.5
0.6
0.7
0.8
0.9
1.0
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
0
10
20
30
40
High Volatility Days
1.00
1.05
1.10
1.15
1.20
1.25
High Volatility Days
Reality Check (%)
Diﬀerence
(ii) QLIKE Loss Function
0
5
10
15
20
25
Full Out-of-Sample
1.00
1.05
1.10
1.15
1.20
1.25
Full Out-of-Sample
HAR
News
OB
News/OB
MSE (avg)
MSE (med)
0
20
40
60
80
100
Normal Volatility Days
0.5
0.6
0.7
0.8
0.9
1.0
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
0
1
2
3
4
High Volatility Days
1.00
1.05
1.10
1.15
1.20
1.25
High Volatility Days
Reality Check (%)
Diﬀerence
(b) Forecast Evaluation under QLIKE
(i) MSE Loss Function
0
2
4
6
8
10
12
Full Out-of-Sample
1
2
3
4
5
6
7
8
Full Out-of-Sample
HAR
News
OB
News/OB
QLIKE (avg)
QLIKE (med)
0
20
40
60
80
100
Normal Volatility Days
1.0
1.5
2.0
2.5
3.0
3.5
4.0
4.5
5.0
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
0
1
2
3
4
High Volatility Days
2
4
6
8
10
High Volatility Days
Reality Check (%)
Diﬀerence
(ii) QLIKE Loss Function
−0.04
−0.02
0.00
0.02
0.04
Full Out-of-Sample
2
4
6
8
10
12
14
16
Full Out-of-Sample
HAR
News
OB
News/OB
QLIKE (avg)
QLIKE (med)
0
5
10
15
20
25
Normal Volatility Days
2
4
6
8
10
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
−0.04
−0.02
0.00
0.02
0.04
High Volatility Days
0
5
10
15
20
25
High Volatility Days
Reality Check (%)
Diﬀerence
Figure 12: Minimising MSE vs QLIKE as the Loss Function in Training
Notes: For each of the two subfigures, the left (right) figure presents the results for the four groups
of ML models (HAR-ML, News-ML, OB-ML, and News/OB-ML) trained using minimising MSE
(QLIKE) as the loss function. The other model specifications are the same as in Subsection 4.2.
The bar chart is the percentage of tickers with the outstanding performance at the 5% significance
level of the RC compared to the HAR-family of models as the benchmark for every specified ML
model. The values for the bar chart can be read from the left-hand axis. The dashed (solid) line
shows the average (median) out-of-sample MSEs and QLIKEs of the ML model relative to the CHAR
model across 23 tickers. A value below one indicates improved performance of the ML model, while
a value above one indicates degradation. The values for the dashed and solid lines can be read from
the right-hand axis. The horizontal dashed line represents no improvement.
46


## Page 47

QLIKE. Furthermore, for the full out-of-sample results, a general degradation in performance,
particularly in terms of magnitude, is evident. However, RC values still demonstrate moderate,
albeit reduced, improvements in performance compared to the primary experiment. The results
derived from the MDA loss function align with previous empirical findings.38
However, what remains unclear is why, when minimising QLIKE (instead of MSE) as the loss
function, the ML models severely underperform when QLIKE is designed to avoid large under-
forecasts. The clue lies in the QLIKE weighting function when true RV is very high. Returning
to Figure 11, where the MSE and QLIKE loss functions are presented for true RV = 2 on the
left and true RV = 80 on the right, it is clear that when the true RV is very high, the weights
of QLIKE become very flat on both sides of the true RV; only when d
RV ≪RV does the weight
begin to rise. This means that when true RV is very high, QLIKE becomes insensitive to the
size of the forecast errors (except for extremely large under-forecasts). Hence, the optimisation
algorithm loses the ability to learn to forecast accurately. This evidence suggests that QLIKE,
without further modification, is not appropriate as a loss function for training ML models, at
least as specified here. Therefore, only the minimisation of MSE is used in this study.39
7.3
No. of Units vs No. of Epochs
This subsection tests the sensitivity of the number of units (#units) and the number of epochs
(#epochs) in affecting the forecasting performance of ML models. We test the number of units
ranging from 5, 10, 15, 20, to 25, and for the number of epochs, from 25, 50, 75, 100, to 125. The
other ML model specifications are the same as those in Subsection 4.2. For 23 tickers, four ML
groups, and 1,604 days in the out-of-sample period, 3,689,200 (25 × 23 × 4 × 1604) ML models
are trained and tested, which is substantially higher than the 737,840 (5 × 23 × 4 × 1604) ML
models trained in Section 5.
The results are presented in Figure 13, Figure 13a for the MSE loss function, and Figure 13b
for the QLIKE loss function, across the four groups of ML models (from left to right: HAR-ML,
News-ML, OB-ML, and News/OB-ML). The results are shown in the following order from left to
38From Figure C7, changing the MSE loss function in Figure C7a to the QLIKE loss function in Figure C7b
results in a degradation in performance on both normal and high volatility days. This pattern is also evident
across the full out-of-sample period.
39The results here also weaken the case for using QLIKE as a measure for forecast evaluation when QLIKE is
used as the optimisation algorithm loss, especially on high volatility days.
47


## Page 48

0
20
40
60
80
Full Out-of-Sample
1.00
1.05
1.10
1.15
1.20
Full Out-of-Sample
MSE (avg)
MSE (med)
0
20
40
60
80
100
Normal Volatility Days
0.4
0.5
0.6
0.7
0.8
0.9
1.0
Normal Volatility Days
0
10
20
30
40
50
High Volatility Days
1.00
1.05
1.10
1.15
1.20
1.25
High Volatility Days
HAR
News
OB
News/OB
Reality Check (%)
Diﬀerence
(a) Forecast Evaluation under MSE
0
5
10
15
20
25
30
Full Out-of-Sample
1
2
3
4
5
6
7
8
9
Full Out-of-Sample
QLIKE (avg)
QLIKE (med)
0
20
40
60
80
100
Normal Volatility Days
1
2
3
4
5
Normal Volatility Days
0
2
4
6
8
High Volatility Days
2
4
6
8
10
12
High Volatility Days
HAR
News
OB
News/OB
Reality Check (%)
Diﬀerence
(b) Forecast Evaluation under QLIKE
Figure 13: No. of Units vs. No. of Epochs
Notes: From left to right, each figure consists of the HAR-ML, News-ML, OB-ML, and News/OB-ML groups. For
each group, the results are shown in the following order from left to right (#units-#epochs): 5-25, 5-50, 5-75, 5-100,
5-125, 10-25, 10-50, 10-75, 10-100, 10-125, 15-25, 15-50, 15-75, 15-100, 15-125, 20-25, 20-50, 20-75, 20-100, 20-125,
25-25, 25-50, 25-75, 25-100, and 25-125. For the sake of clarity, these values are not shown in the figures. The bar
chart shows the percentage of tickers with outstanding performance, considering the MSE loss function in the top
part (QLIKE in the bottom part) at the 5% significance level of the RC compared to the HAR-family of models as
the benchmark for each specified ML model. The dark grey bars represent the RC values of the primary experiments
in Section 5. The RC values can be read from the left-hand axis. The dashed (solid) line shows the average (median)
out-of-sample MSEs and QLIKEs of the ML model relative to the CHAR model across 23 tickers. A value below one
indicates improved performance of the ML model, while a value above one indicates degradation. The values for the
dashed and solid lines can be read from the right-hand axis. The horizontal dashed line represents no improvement.
48


## Page 49

right (#units-#epochs): 5-25, 5-50, 5-75, 5-100, 5-125, 10-25, 10-50, 10-75, 10-100, 10-125, 15-25,
15-50, 15-75, 15-100, 15-125, 20-25, 20-50, 20-75, 20-100, 20-125, 25-25, 25-50, 25-75, 25-100,
and 25-125. For the sake of clarity, these values are not shown in Figure 13. The light grey
bars represent the percentage of tickers with outstanding performance at the 5% significance level
based on the RC. The dark grey bars represent the RC values from the primary experiments
described in Section 5.
First, consider the case of MSE (QLIKE) as the loss function in Figure 13a (in Figure 13b).
As before, the results confirm that, for normal volatility days, generally, a higher number of units
produced the best performance in terms of average (median) ρMSE/QLIKE and the RC values.
Second, the number of units influences forecasting performance more than the number of epochs.
Third, ML outperformed CHAR and the HAR-family of models only on normal volatility days;
when switching to the high volatility days, ML models underperformed, with above one average
(median) ρMSE/QLIKE and RC values lower than 50%. Also, increasing the number of units and
epochs reduces the amount of underperformance on high volatility days. Fourth, the results for
QLIKE as the loss function show the same patterns. Fifth, of the four groups of ML models tested
here, OB-ML and News/OB-ML performances are the most outstanding.
Finally, consistent
with previous findings, the poor performance observed on high volatility days has a significant
impact on the full out-of-sample results, leading to a degradation in performance.
However,
the incorporation of more complex models and an expanded information set helps mitigate this
effect. As in earlier results, the degradation in performance is primarily in magnitude relative
to the CHAR benchmark. Notably, the RC results continue to show improvements, particularly
when more complex models are employed. The results for the MDA in Figure C8 corroborate the
findings here.40
These results further confirm that the ML models defined in this study exhibit strong volatility
forecasting performance during periods of normal market conditions but perform less effectively
on high volatility days. This suggests that greater attention is needed when forecasting during
episodes of heightened market turbulence. To improve forecasting performance under such con-
ditions, more complex ML models with an increased number of units and training epochs may
40Most RC values for normal volatility days are near 100% and ρMDA reaching around 12% improvement in
the OB-ML and News/OB groups. For high volatility days, poor performance is clear for all combinations of the
number of units and epochs. However, consistent with prior outcomes, improvements in forecasting performance
over the full out-of-sample period are evident, both in terms of mean and average values, as well as in the results
produced by the RC.
49


## Page 50

need to be developed and trained.41
7.4
Units vs Epochs: Individual Ticker Analysis
This subsection concerns the best combination of the number of units and epochs for each ticker’s
best volatility forecasting performance. The results are presented in Figure 14, Figure 14a, Fig-
ure 14b, and Figure 14c, corresponding to the full out-of-sample period, as well as performance
on normal and high volatility days, respectively. For each ticker, there are two sets of four bars
corresponding to the four groups of ML models, viz., from left to right, HAR-ML, News-ML,
OB-ML, and News/OB-ML. The first four black bars represent the optimal number of units for
the four groups of ML models, while the next four grey bars represent the optimal number of
epochs for the same groups. Within each subfigure, the top (bottom) graph reports the results
based on the MSE (QLIKE) loss function. The number of units (# of units) can be read from
the left axis, and the number of epochs (# of epochs) can be read from the right axis.
The optimal numbers of units and epochs are generally larger for high volatility days than for
normal volatility days. There are also some variations among the tickers, especially for normal
volatility days in Figure 14b for both MSE and QLIKE.42 For high volatility days in Figure 14c,
there are fewer variations across tickers, and the results are in favour of a more complex ML model
with about 25 units and 70 to 120 or more epochs. The results for the full out-of-sample period
in Figure 14a match this. The corresponding results for the MDA loss function are presented
in Figure C9.43 The individual ticker analysis provides important insight into the importance of
hyperparameter choice conditioned on the level of actual RV. A more complex ML model specifi-
cation (with a high number of units and epochs) works well for almost all tickers for forecasting
41We deliberately omit the early stopping mechanism in the training process because of three primary con-
siderations.
Firstly, allocating a segment of the time series for early stopping would lead to the exclusion of
the most recent data from the training process. This segment could potentially hold crucial insights for more
accurate RV forecasts. Secondly, as detailed earlier, we have tested 3,689,200 distinct models, each employing
different combinations of the number of units and epochs. The findings unanimously point towards poor perfor-
mance on high volatility days by all models tested. That is, our conclusion, in general, is not sensitive to the
choice of hyperparameters. Thirdly, by omitting early stopping, we can compare performance due entirely to the
choice of hyperparameters. Although early stopping is omitted here, in Subsection 7.6, we test its impact with a
smaller-scale experiment.
42Looking at Figure 14b, it is apparent that for some of the tickers like ‘NVDA’, ‘MU’, ‘AMAT’, and ‘ADSK’,
a more complex model with a higher number of units is required for better forecasting performance, consistent
with the findings in Subsection 5.4.
43Interestingly, although some differences are observed across individual tickers, a less complex model with
fewer units and fewer training epochs tends to be sufficient. Increasing model complexity or extending the number
of training epochs does not result in substantial performance gains when evaluated using the MDA loss function.
This further supports the premise that these ML models, many of which are fundamentally designed for directional
forecasting, perform effectively even in their most minimal configurations.
50


## Page 51

0
10
20
30
40
50
# of units
MSE
AAPL
MSFT
INTC
CMCSA
QCOM
CSCO
EBAY
GILD
TXN
AMZN
SBUX
NVDA
MU
AMAT
NTAP
ADBE
XLNX
AMGN
VOD
CTSH
KLAC
PCAR
ADSK
Ticker
0
10
20
30
40
50
# of units
QLIKE
0
20
40
60
80
100
120
# of epochs
# of units
# of epochs
0
20
40
60
80
100
120
# of epochs
(a) Full Out-of-Sample
0
10
20
30
40
50
# of units
MSE
AAPL
MSFT
INTC
CMCSA
QCOM
CSCO
EBAY
GILD
TXN
AMZN
SBUX
NVDA
MU
AMAT
NTAP
ADBE
XLNX
AMGN
VOD
CTSH
KLAC
PCAR
ADSK
Ticker
0
10
20
30
40
50
# of units
QLIKE
0
20
40
60
80
100
120
# of epochs
# of units
# of epochs
0
20
40
60
80
100
120
# of epochs
(b) Normal Volatility Days
0
10
20
30
40
50
# of units
MSE
AAPL
MSFT
INTC
CMCSA
QCOM
CSCO
EBAY
GILD
TXN
AMZN
SBUX
NVDA
MU
AMAT
NTAP
ADBE
XLNX
AMGN
VOD
CTSH
KLAC
PCAR
ADSK
Ticker
0
10
20
30
40
50
# of units
QLIKE
0
20
40
60
80
100
120
# of epochs
# of units
# of epochs
0
20
40
60
80
100
120
# of epochs
(c) High Volatility Days
Figure 14: The Best-Performing Hyperparameters (#Units & #Epochs)
Notes: There are two sets of four bars for each ticker that correspond to the four groups of ML models, viz.
HAR-ML, News-ML, OB-ML, and News/OB-ML. The first four black bars correspond to their optimal number of
units, while the next four grey bars correspond to their optimal number of epochs. The top, middle, and bottom
figures correspond to the full out-of-sample period, normal volatility days, and high volatility days, respectively.
Within each subfigure, the top (bottom) graph reports the results considering the MSE (QLIKE) loss function.
The number of units (# of units) can be read from the left axis, and the number of epochs (# of epochs) can be
read from the right axis.
51


## Page 52

RV on high volatility days. In contrast, for forecasting RV on normal volatility days, one would
expect more idiosyncratic variations, and careful tuning of hyperparameters for each ML group
and for each ticker can provide additional improvement to forecasting performance. Additionally,
the pronounced impact of high volatility days on full out-of-sample performance supports the
use of more complex ML models when evaluating the entire out-of-sample period. Altogether,
these variations raise concerns about using ML models as direct substitutes for the HAR-family
of models, due to the inherent complexities associated with hyperparameter optimisation.
7.5
Fully Connected Neural Network
FCNN is among the most commonly employed alternatives to conventional models in the lit-
erature. Accordingly, we investigate the impact of replacing the LSTM model with an FCNN
on out-of-sample forecasting performance.
To ensure a controlled comparison, we retain the
same hyperparameter settings as those used for the LSTM model, as detailed in Subsection 4.2.
Furthermore, we ensure that the input variables are consistent with those used in the LSTM
experiments. Specifically, in the LSTM model, each variable includes 21 lags, which are naturally
accommodated by the LSTM architecture due to its inherent capacity to model sequential depen-
dencies. In contrast, the FCNN architecture does not inherently accommodate sequential data.
To preserve the input structure, 21 lags of each variable must be explicitly specified as separate
input features for the FCNN. As a result, the number of input variables rises to 126, 315, 2,898,
and 3,087 for the HAR-ML, News-ML, OB-ML, and News/OB-ML groups, respectively.
We present the results for HAR-ML, News-ML, OB-ML, and News/OB-ML. Specifically, for
23 tickers, these four ML groups, and 1,604 days in the out-of-sample period, a total of 737,840
(5 × 23 × 4 × 1604) ML models, specifically FCNN, are trained and tested. Figure 15 presents a
comparison of the LSTM model from Subsection 5.1 and Subsection 5.2 with the results obtained
from FCNN. The first, second, third, and fourth sets of ten bars correspond to the HAR, News,
OB, and News/OB groups, respectively. Within each set, the first five hatched bars represent
results from the LSTM model, while the subsequent five bars represent results from the FCNN
model. Each bar within these subsets reflects performance associated with a specific number
of units. The values for the bar chart correspond to the left-hand axis. As before, the dashed
(solid) line represents the average (median) out-of-sample MSEs and QLIKEs of the ML model
relative to the CHAR model across 23 tickers, with values read from the right-hand side. Across
52


## Page 53

all information sets, the superior performance of the LSTM model relative to the FCNN model
is evident. As previously observed, model performance is generally superior on normal volatility
days, with the LSTM consistently achieving 100% RC, while the FCNN reaches this level of
RC primarily in its more complex forms. A similar pattern emerges in terms of magnitude of
performance, as even the simplest LSTM model matches or outperforms the most complex FCNN
model. The results under the QLIKE loss function further reinforce these findings. This can be
attributed to the sequential structure of LSTM, which provides greater predictive power for
RV forecasting compared to FCNN models. Additionally, the comparatively better performance
of FCNN on normal volatility days, rather than during high volatility days, further supports
our previous conclusions. A similar pattern is also observed over the full out-of-sample period.
Consistent with the LSTM, the FCNN exhibits a marked decline in performance, particularly
regarding the magnitude of its forecasting performance. The results for MDA in Figure C10 align
with the findings presented here, both demonstrating the superior performance of LSTM over
FCNN.
Table 9 reports the out-of-sample forecasting performance of the FCNN model and enables
a direct comparison with the LSTM results presented in Table 6 and Table 7, using identical
information sets and evaluation designs.
Overall, the LSTM models outperform their FCNN
counterparts. With respect to MSE, in the full out-of-sample period both architectures produce
loss ratios exceeding unity across all specifications, although in some cases the FCNN achieves val-
ues marginally closer to one for the best-performing configurations. In contrast, for QLIKE, the
LSTM models generally deliver more favourable outcomes in the corresponding optimal specifica-
tions. The comparison is most pronounced for MDA, where the LSTM consistently attains lower
loss ratios than the FCNN in the leading configurations. The RC statistics broadly corroborate
these findings, indicating stronger and more persistent dominance of the LSTM specifications.
Results for normal volatility days reinforce this pattern, with LSTM exhibiting substantially su-
perior performance. During high volatility days, the FCNN shows a modest advantage in a subset
of configurations; however, both architectures perform poorly in this regime, consistent with our
earlier evidence that ML models generally perform poorly during periods of elevated volatility.
Moreover, these results highlight that the choice of ML architecture, and potentially the asso-
ciated hyperparameter configurations used in model design, has an impact on RV forecasting
performance, particularly for high volatility days, which, as discussed in Section 5, remain diffi-
53


## Page 54

54
0
20
40
60
80
Full Out-of-Sample
1.00
1.05
1.10
1.15
1.20
Full Out-of-Sample
HAR
News
OB
News/OB
LSTM
FCNN
LSTM
FCNN
LSTM
FCNN
LSTM
FCNN
MSE (avg)
MSE (med)
0
20
40
60
80
100
Normal Volatility Days
0.4
0.6
0.8
1.0
1.2
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
0
10
20
30
40
50
60
70
80
High Volatility Days
1.00
1.05
1.10
1.15
1.20
1.25
High Volatility Days
Reality Check (%)
Diﬀerence
(a) Forecast Evaluation under MSE
0
2
4
6
8
10
12
Full Out-of-Sample
1
2
3
4
5
6
7
8
Full Out-of-Sample
HAR
News
OB
News/OB
LSTM
FCNN
LSTM
FCNN
LSTM
FCNN
LSTM
FCNN
QLIKE (avg)
QLIKE (med)
0
20
40
60
80
100
Normal Volatility Days
1
2
3
4
5
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
0
5
10
15
20
25
30
High Volatility Days
2
4
6
8
10
High Volatility Days
Reality Check (%)
Diﬀerence
(b) Forecast Evaluation under QLIKE
Notes: The bar chart is the percentage of tickers with the outstanding performance considering the MSE loss function in Figure 15a and the QLIKE loss function in Figure 15b
at the 5% significance level of the RC compared to the HAR-family of models as the benchmark for every specified model. The first, second, third, and fourth sets of ten bars
correspond to the HAR, News, OB, and News/OB groups, respectively. Within each set, the first five hatched bars represent results from the LSTM model, while the subsequent
five bars represent results from the FCNN model. Each bar within these subsets reflects performance associated with a specific number of units. The dashed (solid) line shows
the average (median) out-of-sample MSEs and QLIKEs of the ML model relative to the CHAR model across 23 tickers. A value below one indicates improved performance of the
ML model, while a value above one indicates degradation. The values for the dashed and solid lines can be read from the right-hand axis. The horizontal dashed line represents
no improvement.
Figure 15: Comparison of LSTM and FCNN Models


## Page 55

55
Table 9: Out-of-Sample Volatility Forecasting Performance of FCNN Models
14 September 2015 to 27 January 2022 (1,604 days)
HAR-ML
News-ML
OB-ML
News/OB-ML
Units
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
Full Out-of-Sample
MSEa
Avg
1.215
1.214
1.219
1.211
1.200
1.217
1.220
1.221
1.209
1.194
1.214
1.201
1.132
1.179
1.182
1.213
1.197
1.138
1.123
1.119
Med
1.191
1.188
1.197
1.177
1.165
1.187
1.193
1.193
1.174
1.160
1.182
1.176
1.116
1.150
1.151
1.195
1.164
1.108
1.102
1.103
RCd
5%
26.09
13.04
21.74
26.09
30.44
17.39
17.39
17.39
26.09
30.44
17.39
26.09
86.96
30.44
26.09
21.74
17.39
73.91
78.26
69.57
10%
60.87
60.87
56.52
60.87
65.22
60.87
60.87
52.17
60.87
73.91
56.52
69.57
95.65
86.96
82.61
56.52
78.26
95.65
95.65
100
QLIKEb
Avg
5.221
6.152
7.402
5.141
4.474
5.924
6.706
6.573
4.609
3.902
4.406
3.487
1.560
2.527
2.615
5.091
3.254
1.602
1.501
1.535
Med
5.017
5.352
6.554
4.320
4.433
5.438
6.119
5.841
4.407
4.049
3.773
2.946
1.487
2.431
2.534
4.414
3.358
1.503
1.419
1.495
RC
5%
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
0.00
0.00
0.00
0.00
0.00
4.35
0.00
4.35
10%
4.35
0.00
4.35
8.70
0.00
4.35
0.00
0.00
0.00
0.00
4.35
0.00
0.00
0.00
0.00
0.00
0.00
4.35
4.35
4.35
MDAc
Avg
1.016
1.009
1.017
0.999
0.992
1.022
1.021
1.035
1.003
0.988
1.014
0.985
0.970
0.974
0.974
1.018
0.987
0.966
0.976
0.979
Med
1.022
1.013
1.014
0.991
0.972
1.023
1.029
1.033
0.997
0.983
1.003
0.979
0.970
0.971
0.980
1.011
0.982
0.966
0.983
0.983
RC
5%
52.17
69.57
60.87
82.61
82.61
52.17
47.83
47.83
73.91
73.91
69.57
73.91
95.65
95.65
91.30
56.52
82.61
95.65
91.30
100
10%
65.22
73.91
65.22
86.96
82.61
60.87
56.52
52.17
73.91
78.26
78.26
73.91
95.65
95.65
91.30
56.52
82.61
100
95.65
100
Normal Volatility Days
MSE
Avg
0.972
0.853
0.824
0.783
0.689
0.990
0.928
0.930
0.847
0.726
0.979
0.816
0.944
0.764
0.810
0.993
0.907
0.906
1.159
1.308
Med
0.919
0.755
0.776
0.702
0.662
0.924
0.892
0.896
0.799
0.687
0.933
0.697
0.861
0.746
0.775
0.919
0.920
0.903
1.046
1.214
RC
5%
78.26
91.30
91.30
95.65
100
78.26
82.61
86.96
86.96
95.65
69.57
82.61
86.96
91.30
95.65
73.91
82.61
78.26
65.22
47.83
10%
78.26
91.30
95.65
95.65
100
82.61
86.96
86.96
91.30
95.65
69.57
82.61
86.96
95.65
95.65
73.91
82.61
78.26
65.22
52.17
QLIKE
Avg
3.255
4.271
5.184
3.091
2.873
3.677
4.876
5.018
3.165
2.608
2.796
2.076
1.248
1.630
1.678
3.175
2.130
1.228
1.316
1.378
Med
3.008
3.492
3.776
2.106
2.571
3.700
4.200
3.954
2.678
2.403
2.255
1.813
1.241
1.541
1.538
2.711
1.805
1.215
1.247
1.347
RC
5%
8.70
4.35
4.35
8.70
21.74
4.35
4.35
0.00
4.35
34.78
4.35
8.70
26.09
4.35
0.00
0.00
13.04
39.13
21.74
0.00
10%
8.70
4.35
4.35
8.70
21.74
4.35
4.35
0.00
4.35
34.78
4.35
8.70
30.44
4.35
4.35
0.00
13.04
43.48
21.74
0.00
MDA
Avg
0.965
0.955
0.962
0.944
0.938
0.970
0.967
0.981
0.948
0.934
0.959
0.930
0.940
0.925
0.926
0.964
0.936
0.935
0.952
0.957
Med
0.977
0.964
0.955
0.953
0.923
0.977
0.980
0.979
0.954
0.929
0.954
0.931
0.936
0.916
0.932
0.964
0.943
0.930
0.951
0.957
RC
5%
82.61
86.96
86.96
86.96
95.65
73.91
86.96
82.61
91.30
91.30
86.96
95.65
100
100
100
78.26
95.65
100
95.65
91.30
10%
86.96
86.96
91.30
91.30
95.65
82.61
86.96
86.96
95.65
100
86.96
95.65
100
100
100
78.26
95.65
100
95.65
100
High Volatility Days
MSE
Avg
1.224
1.228
1.233
1.226
1.219
1.226
1.231
1.231
1.222
1.211
1.221
1.215
1.140
1.194
1.195
1.221
1.206
1.146
1.122
1.114
Med
1.212
1.211
1.206
1.207
1.188
1.210
1.206
1.219
1.200
1.186
1.197
1.183
1.112
1.157
1.160
1.194
1.182
1.125
1.100
1.103
RC
5%
17.39
13.04
4.35
8.70
8.70
8.70
8.70
4.35
4.35
8.70
4.35
13.04
60.87
21.74
17.39
0.00
8.70
56.52
78.26
82.61
10%
52.17
43.48
34.78
34.78
39.13
56.52
43.48
34.78
34.78
34.78
39.13
39.13
78.26
43.48
47.83
39.13
47.83
78.26
86.96
86.96
QLIKE
Avg
7.376
8.302
9.870
7.225
6.146
8.404
8.752
8.374
6.213
5.228
6.051
5.040
1.906
3.517
3.612
6.988
4.368
2.002
1.703
1.726
Med
6.267
7.172
10.009
6.506
5.645
7.196
8.361
8.571
5.880
5.021
5.568
4.307
1.882
3.109
3.257
6.406
4.099
1.940
1.723
1.750
RC
5%
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
4.35
0.00
8.70
0.00
0.00
0.00
0.00
13.04
13.04
30.44
10%
8.70
0.00
4.35
4.35
0.00
8.70
0.00
0.00
0.00
0.00
8.70
0.00
13.04
4.35
4.35
4.35
0.00
13.04
30.44
47.83
MDA
Avg
1.067
1.068
1.067
1.067
1.066
1.067
1.068
1.068
1.066
1.065
1.066
1.066
1.044
1.067
1.065
1.064
1.064
1.047
1.025
1.016
Med
1.058
1.058
1.058
1.058
1.058
1.058
1.058
1.058
1.058
1.058
1.058
1.058
1.049
1.058
1.058
1.058
1.058
1.049
1.022
1.000
RC
5%
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
4.35
0.00
0.00
0.00
0.00
13.04
17.39
34.78
10%
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
4.35
0.00
0.00
0.00
0.00
13.04
17.39
39.13
Notes: The results present the out-of-sample volatility forecasting performance of FCNN models. The best value in each row is marked in bold.
a The mean (or median) MSE ratio of ML to CHAR for 23 tickers. A ratio above one indicates degradation, while below one indicates improvement.
b The mean (or median) QLIKE ratio of ML to CHAR for 23 tickers.
A ratio above one indicates degradation, while below one indicates improvement.
c The mean (or median) MDA ratio of CHAR to ML for 23 tickers. A ratio above one indicates degradation, while below one indicates
improvement.
d Percentage of tickers with the outstanding performance of FCNN against the HAR-family of models at the 5% and 10% significance levels.


## Page 56

cult to forecast even for HAR-family of models. This phenomenon may help explain part of the
mixed evidence in the literature regarding the relative outperformance of ML models over HAR-
family benchmarks, as our results show that changes in ML architecture can lead to improved
forecasting performance during high volatility days relative to the LSTM.
7.6
Overfitting
To further strengthen our conclusions regarding overfitting, we carry out additional tests beyond
those already presented. Overfitting and two approaches for addressing it are discussed in Sub-
section 4.1. Additionally, as outlined in Section 5, we incorporated MDA as a complementary
performance metric alongside MSE and QLIKE. This addition provides a more nuanced evalua-
tion of model performance, particularly in terms of capturing the directional dynamics of RV. Our
findings consistently indicate that although ML models may not outperform benchmark models
in terms of MSE and QLIKE, especially on days with high volatility, they exhibit notable im-
provements in MDA. This suggests that the ML models are effectively learning the underlying
structure of RV. Furthermore, in Subsection 7.3, we expanded the model’s hyperparameter space
by varying both the number of training epochs and units. Across these extended settings, we
observed consistent results, even for the simplest ML models and the smallest number of epochs.
Comparable outcomes were also obtained when the model architecture was entirely changed from
LSTM to FCNN, as shown in Subsection 7.5, further reinforcing the conclusion that overfitting
is unlikely to be a significant issue.
We now introduce an additional safeguard against overfitting, complementing the existing use
of L2 regularisation and dropout described in Subsection 4.1. Specifically, we reserve the last 20%
of the training data from previous experiments as validation data. Following common practice,
we apply early stopping with a patience of 7 epochs and restore the model weights from the epoch
with the best validation performance. The early stopping range is consistent with that used in
Subsection 7.3, spanning from 25 to 125 epochs. Accordingly, we re-train all models presented
in Section 5. Figure 16 presents the results across all ML groups, including HAR, News, OB,
and the combined News/OB. This figure is directly comparable to the ML section of Figure 4.
Overall, the findings are consistent with those discussed in Section 5 for models without early
stopping.
Specifically, all models exhibit a consistent pattern: improved performance during
periods of normal volatility, but deteriorated performance on high volatility days. As before, the
56


## Page 57

behaviour observed during the full out-of-sample period closely mirrors the pattern seen during
high volatility days. The MDA results shown in Figure C11 are also consistent with our earlier
findings, supporting the same conclusions as before.
To facilitate a more detailed comparison, Table 10 reports the differences between the results
presented in Table 6 and Table 7 and the models with early stopping.
Positive values indi-
cate superior performance of the models with early stopping and are highlighted in bold. The
primary finding is that the application of early stopping generally results in a decline in fore-
casting performance for both the OB-ML and News/OB-ML model groups across the majority of
tests. Although slight performance improvements are occasionally observed when early stopping
is applied to the HAR-ML and News-ML groups, these gains are limited in both frequency and
magnitude. Overall, the evidence further substantiates our earlier conclusion that overfitting is
not a primary factor underlying the observed results.
8
A Reflection on the Practical Usability of ML Models
All main tests in Section 5, as well as the robustness tests in Section 7, which consider different
ML model types, hyperparameters, and information groups, lead to the same conclusion. ML
models significantly improve RV forecasting performance on normal volatility days. However,
they tend to degrade forecasting performance during high volatility days, which can adversely
affect performance over the full out-of-sample period.
As highlighted in Subsection 5.2, the
stark contrast in model performance between normal and high volatility days suggests that ML
models trained on full in-sample periods, which are dominated by normal volatility observations,
are poorly suited for forecasting rare high volatility days. This distinction is further supported
by our analyses of individual tickers in Subsection 5.4, which indicate that different modelling
strategies are necessary for normal versus high volatility days. This raises the key question of
whether to use HAR-family of models or ML models, and more importantly, how to effectively
leverage the strengths of ML models for forecasting RV.
To address this, we propose a straightforward ensemble model that combines forecasts from
both the HAR-family of models and ML models by averaging their predicted values. This simple
ensemble method can help moderate model behaviour under varying market conditions, leveraging
ML models during periods of normal volatility and relying on linear models during episodes of high
57


## Page 58

58
0
10
20
30
40
50
60
70
Full Out-of-Sample
1.00
1.05
1.10
1.15
1.20
Full Out-of-Sample
HAR
News
OB
News/OB
MSE (avg)
MSE (med)
0
20
40
60
80
100
Normal Volatility Days
0.5
0.6
0.7
0.8
0.9
1.0
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
0
5
10
15
20
25
30
35
40
High Volatility Days
1.00
1.05
1.10
1.15
1.20
1.25
High Volatility Days
Reality Check (%)
Diﬀerence
(a) Forecast Evaluation under MSE
0
1
2
3
4
Full Out-of-Sample
1
2
3
4
5
6
7
8
9
Full Out-of-Sample
HAR
News
OB
News/OB
QLIKE (avg)
QLIKE (med)
0
20
40
60
80
Normal Volatility Days
1
2
3
4
5
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
−0.04
−0.02
0.00
0.02
0.04
High Volatility Days
2
4
6
8
10
12
High Volatility Days
Reality Check (%)
Diﬀerence
(b) Forecast Evaluation under QLIKE
Notes: The bar chart is the percentage of tickers with the outstanding performance considering the MSE loss function in Figure 16a and the QLIKE loss function in Figure 16b at
the 5% significance level of the RC compared to the HAR-family of models as the benchmark. The results are presented for each model group: HAR, News, OB, and News/OB,
across varying numbers of units, specifically 5, 10, 15, 20, and 25 units. The values for the bar chart can be read from the left-hand axis. The dashed (solid) line shows the
average (median) out-of-sample MSEs and QLIKEs of the ML model relative to the CHAR model across 23 tickers. A value below one indicates improved performance of the
ML model, while a value above one indicates degradation. The values for the dashed and solid lines can be read from the right-hand axis. The horizontal dashed line represents
no improvement.
Figure 16: ML Models Utilising Early Stopping


## Page 59

59
Table 10: Out-of-Sample Volatility Forecasting Performance of ML Models Utilising Early Stopping
14 September 2015 to 27 January 2022 (1,604 days)
HAR-ML
News-ML
OB-ML
News/OB-ML
Units
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
Full Out-of-Sample
MSE
Avg
0.002
0.001
0.002
-0.002
-0.003
0.006
-0.001
-0.003
-0.001
-0.004
-0.007
-0.027
-0.039
-0.044
-0.011
-0.001
-0.024
-0.039
-0.040
-0.049
Med
0.004
0.007
0.002
-0.003
-0.006
0.009
-0.001
0.000
-0.004
-0.011
-0.005
0.002
-0.033
-0.033
0.000
0.001
-0.019
-0.024
-0.017
-0.038
RC
5%
4.35
0.00
0.00
-4.35
-8.70
-4.35
4.35
-8.70
-4.35
0.00
-13.04
-13.04
-34.78
-47.83
-47.83
0.00
-13.04
-26.09
-43.48
-47.83
10%
0.00
0.00
-8.70
8.70
-4.35
0.00
0.00
-4.35
4.35
0.00
-4.35
-4.35
-21.74
-30.44
-21.74
-13.04
0.00
-21.74
-21.74
-26.09
QLIKE
Avg
-0.256
0.154
-0.133
-0.217
-0.147
-0.931
-0.339
-0.811
0.053
-0.262
-2.693
-2.884
-2.906
-2.399
-2.090
-1.310
-2.866
-2.993
-2.474
-2.930
Med
-0.562
-0.263
-0.112
-0.098
-0.093
0.125
-0.045
-0.822
-0.124
-0.301
-3.820
-3.001
-2.727
-2.415
-1.659
-2.406
-2.845
-3.238
-2.202
-2.397
RC
5%
0.00
0.00
0.00
0.00
-8.70
0.00
0.00
0.00
-4.35
-8.70
0.00
-4.35
0.00
-8.70
-13.04
0.00
0.00
0.00
0.00
-8.70
10%
0.00
0.00
4.35
-8.70
-26.09
0.00
0.00
-4.35
0.00
-26.09
-4.35
-8.70
-13.04
-17.39
-21.74
0.00
-8.70
-13.04
-21.74
-17.39
MDA
Avg
-0.016
0.011
0.005
0.005
0.005
-0.005
0.008
0.006
0.002
-0.001
-0.063
-0.058
-0.056
-0.047
-0.025
-0.036
-0.058
-0.058
-0.050
-0.043
Med
-0.009
0.017
0.007
0.002
0.004
-0.002
0.006
0.006
0.005
-0.005
-0.073
-0.064
-0.056
-0.041
-0.022
-0.061
-0.058
-0.069
-0.045
-0.040
RC
5%
-8.70
0.00
0.00
0.00
0.00
0.00
4.35
-4.35
4.35
0.00
-30.43
-21.74
-26.09
-8.70
-13.04
-17.39
-21.74
-21.74
-26.09
-26.09
10%
-4.35
-4.35
0.00
0.00
0.00
4.35
0.00
4.35
0.00
0.00
-30.43
-21.74
-21.74
-8.70
-13.04
-17.39
-21.74
-13.04
-13.04
-21.74
Normal Volatility Days
MSE
Avg
-0.011
0.021
0.026
0.024
0.019
-0.018
0.021
0.029
0.043
0.026
-0.245
-0.265
-0.233
-0.213
-0.235
-0.188
-0.260
-0.230
-0.234
-0.229
Med
-0.019
0.030
0.043
0.069
0.002
-0.032
0.040
0.045
0.077
0.052
-0.261
-0.338
-0.243
-0.185
-0.170
-0.305
-0.303
-0.247
-0.180
-0.210
RC
5%
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
-4.35
-4.35
0.00
0.00
-4.35
-8.70
-8.70
-4.35
-4.35
-4.35
10%
0.00
0.00
0.00
0.00
0.00
4.35
0.00
0.00
0.00
0.00
-4.35
-4.35
0.00
0.00
-4.35
-4.35
-4.35
0.00
0.00
-4.35
QLIKE
Avg
-0.799
-0.121
0.046
-0.005
-0.038
-0.547
-0.276
-0.113
0.061
-0.086
-2.636
-2.397
-2.136
-1.885
-1.932
-1.394
-2.448
-2.040
-1.927
-2.166
Med
-0.729
-0.161
0.026
0.046
-0.006
0.124
-0.754
0.061
0.034
-0.087
-3.540
-2.458
-1.744
-1.465
-1.601
-2.324
-1.929
-1.889
-1.581
-1.661
RC
5%
-4.35
4.35
8.70
4.35
-8.70
0.00
4.35
8.70
-4.35
-17.39
-39.13
-52.17
-73.91
-69.57
-69.57
-21.74
-60.87
-69.57
-73.91
-69.57
10%
-4.35
0.00
4.35
0.00
0.00
0.00
13.04
8.70
-13.04
-13.04
-39.13
-47.83
-73.91
-69.57
-69.57
-21.74
-65.22
-73.91
-78.26
-73.91
MDA
Avg
-0.015
0.012
0.007
0.008
0.010
-0.005
0.010
0.008
0.005
0.003
-0.068
-0.056
-0.049
-0.035
-0.022
-0.044
-0.057
-0.050
-0.044
-0.030
Med
-0.006
0.019
0.016
0.013
0.011
-0.005
0.001
0.010
0.006
-0.004
-0.075
-0.060
-0.041
-0.041
-0.023
-0.072
-0.057
-0.057
-0.034
-0.027
RC
5%
-8.70
4.35
0.00
0.00
0.00
0.00
4.35
0.00
0.00
0.00
-17.39
-4.35
-4.35
0.00
0.00
-8.70
-8.70
0.00
0.00
0.00
10%
-8.70
4.35
0.00
0.00
0.00
-4.35
4.35
0.00
0.00
0.00
-13.04
0.00
0.00
0.00
0.00
-8.70
0.00
0.00
0.00
0.00
High Volatility Days
MSE
Avg
0.003
0.001
0.001
-0.004
-0.004
0.007
-0.002
-0.004
-0.003
-0.005
0.001
-0.017
-0.031
-0.037
-0.004
0.007
-0.014
-0.031
-0.032
-0.042
Med
0.002
0.000
0.007
-0.003
-0.008
0.007
0.001
-0.005
-0.004
-0.012
-0.020
0.006
-0.018
-0.024
0.003
-0.001
-0.001
-0.011
-0.008
-0.038
RC
5%
17.39
13.04
4.35
8.70
8.70
8.70
8.70
4.35
4.35
8.70
4.35
13.04
60.87
21.74
17.39
0.00
8.70
56.52
78.26
82.61
10%
52.17
43.48
34.78
34.78
39.13
56.52
43.48
34.78
34.78
34.78
39.13
39.13
78.26
43.48
47.83
39.13
47.83
78.26
86.96
86.96
QLIKE
Avg
0.114
0.338
-0.328
-0.411
-0.235
-1.198
-0.490
-1.560
0.086
-0.413
-2.956
-3.456
-3.844
-2.971
-2.413
-1.325
-3.344
-4.105
-3.118
-3.855
Med
-2.164
-0.003
0.011
-0.329
-0.169
0.247
0.061
-1.678
-0.232
-0.397
-4.719
-3.348
-3.417
-3.227
-1.818
-2.987
-2.240
-3.173
-3.088
-2.867
RC
5%
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
0.00
0.00
-4.35
0.00
0.00
0.00
0.00
-4.35
10%
0.00
-4.35
0.00
4.35
0.00
0.00
0.00
0.00
-4.35
-13.04
-4.35
-4.35
0.00
-4.35
-4.35
-4.35
0.00
0.00
-4.35
-4.35
MDA
Avg
0.001
0.000
-0.004
-0.005
-0.003
0.001
-0.002
-0.002
-0.005
-0.009
0.000
-0.002
-0.002
-0.007
-0.006
0.001
-0.001
-0.005
-0.009
-0.016
Med
0.000
0.000
0.000
-0.005
-0.008
0.000
0.000
0.000
-0.002
-0.004
0.000
0.000
-0.004
-0.004
-0.008
0.000
0.000
-0.004
-0.002
-0.008
RC
5%
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
0.00
0.00
0.00
0.00
0.00
0.00
0.00
-4.35
10%
0.00
0.00
0.00
0.00
-4.35
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
0.00
0.00
-4.35
Notes: The results report the difference in out-of-sample RV forecasting performance between the primary trained models in Section 5 and those trained with early stopping. Positive values indicate superior performance of the models
with early stopping and are highlighted in bold. It should be noted that the presentation of values in this table differs from that in previous tables to facilitate interpretation and enhance the clarity of the comparison.


## Page 60

volatility. To further refine the ensemble, a weighted averaging scheme may be employed, allowing
for differential weighting across model groups. These weights can be optimised using training data
to enhance forecasting performance. However, for illustrative purposes, we adopt a conservative
weighting strategy. Specifically, we assign a weight of 0.75 to the best-performing HAR-family
model (CHAR) and 0.25 to the ML models, thereby favouring the more conventional model in
the ensemble. This approach also holds practical value: it allows practitioners to leverage the
predictive power of ML models without fully replacing conventional models, thereby benefiting
from both ML and HAR models.
Table 11 reports the results of the ensemble models. These findings are directly comparable to
those presented for the full out-of-sample period in Table 6, as well as for normal and high volatility
days in Table 7. A comparison of ensemble models with the ML models used in our primary
experiment clearly indicates that the ensemble models outperform individual ML approaches.
Focusing on the full out-of-sample period, we observe that for nearly all models, the RC reaches
or approaches 100%.
Additionally, several ML models demonstrate modest improvements in
MSE and QLIKE, with MDA improving by approximately 3%. On normal volatility days, as
expected, we observe substantial improvements not only in RC but also in MSE, QLIKE, and
MDA metrics. On average, MSE improves by around 30% and QLIKE by approximately 10%
compared to the CHAR benchmark model, while MDA shows a 4% improvement. During high
volatility days, improvements are more modest but still evident in several cases. Even in scenarios
where no improvement is observed, the degradation in average and median values is significantly
less pronounced compared to the results reported in Table 7. As in previous results, the OB-
ML and News/OB-ML groups emerge as the best-performing models over the full out-of-sample
period.
As outlined earlier, the approach employed here involves a simple ensemble model with pre-
defined weights. While more optimal results can be achieved by calibrating these weights using
training data on a rolling basis, even this basic implementation demonstrates that ML models
can enhance forecasting performance alongside HAR-family of models. However, the findings
also underscore an important caveat: exclusive reliance on ML models may be detrimental in
certain scenarios, particularly during periods of high volatility. Therefore, any proposed switch
between model classes should be supported by rigorous empirical evidence demonstrating con-
sistent performance across both stable and turbulent market conditions. In the absence of such
60


## Page 61

61
Table 11: Out-of-Sample Volatility Forecasting Performance of Ensemble Models
14 September 2015 to 27 January 2022 (1,604 days)
HAR-ML
News-ML
OB-ML
News/OB-ML
Units
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
Full Out-of-Sample
MSEa
Avg
0.995
0.993
0.991
0.990
0.988
0.995
0.993
0.991
0.989
0.988
0.993
0.991
0.989
0.987
0.987
0.993
0.990
0.989
0.988
0.987
Med
1.000
1.000
0.998
0.997
0.995
1.000
1.000
0.996
0.996
0.994
0.997
0.998
0.995
0.994
0.993
0.997
0.998
0.995
0.994
0.993
RCd
5%
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
10%
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
QLIKEb
Avg
1.054
1.032
1.023
1.013
1.008
1.054
1.030
1.012
1.004
0.996
1.026
1.011
1.001
0.994
0.992
1.028
1.009
1.002
0.994
0.991
Med
1.048
1.025
1.019
1.010
1.004
1.050
1.022
1.011
1.003
0.998
1.025
1.009
1.001
0.994
0.991
1.024
1.006
1.003
0.995
0.993
RC
5%
43.48
60.87
65.22
78.26
95.65
47.83
69.57
78.26
86.96
86.96
65.22
78.26
91.30
100
100
60.87
73.91
82.61
86.96
86.96
10%
60.87
69.57
73.91
82.61
95.65
56.52
73.91
82.61
86.96
86.96
78.26
86.96
100
100
100
69.57
78.26
82.61
86.96
86.96
MDAc
Avg
0.964
0.972
0.979
0.984
0.988
0.964
0.971
0.976
0.983
0.985
0.964
0.973
0.978
0.982
0.986
0.963
0.973
0.979
0.980
0.984
Med
0.961
0.974
0.979
0.983
0.988
0.966
0.971
0.976
0.984
0.987
0.967
0.975
0.978
0.981
0.988
0.964
0.974
0.979
0.980
0.983
RC
5%
100
100
100
95
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
10%
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
Normal Volatility Days
MSE
Avg
0.635
0.693
0.731
0.768
0.801
0.627
0.678
0.718
0.751
0.786
0.629
0.674
0.720
0.748
0.775
0.614
0.671
0.722
0.732
0.768
Med
0.644
0.697
0.726
0.763
0.816
0.635
0.677
0.715
0.741
0.783
0.620
0.669
0.733
0.752
0.775
0.615
0.662
0.714
0.741
0.765
RC
5%
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
10%
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
QLIKE
Avg
0.865
0.906
0.933
0.948
0.966
0.859
0.894
0.918
0.935
0.954
0.845
0.874
0.903
0.913
0.930
0.832
0.874
0.904
0.907
0.925
Med
0.874
0.911
0.933
0.950
0.971
0.864
0.892
0.916
0.931
0.952
0.840
0.875
0.905
0.913
0.923
0.820
0.865
0.903
0.907
0.918
RC
5%
100
100
100
100
95.65
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
10%
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
100
MDA
Avg
0.943
0.957
0.968
0.977
0.985
0.942
0.953
0.964
0.974
0.980
0.947
0.961
0.969
0.976
0.982
0.944
0.960
0.971
0.973
0.980
Med
0.943
0.960
0.970
0.978
0.985
0.945
0.955
0.965
0.975
0.982
0.950
0.961
0.971
0.976
0.983
0.945
0.958
0.971
0.974
0.981
RC
5%
100
100
95.65
95.65
73.91
100
100
100
100
91.30
100
100
95.65
95.65
86.96
100
100
100
100
95.65
10%
100
100
95.65
95.65
91.30
100
100
100
100
95.65
100
100
95.65
95.65
91.30
100
100
100
100
95.65
High Volatility Days
MSE
Avg
1.009
1.004
1.001
0.998
0.995
1.009
1.005
1.001
0.998
0.995
1.007
1.002
0.999
0.996
0.995
1.008
1.002
0.999
0.997
0.995
Med
1.017
1.012
1.007
1.004
1.002
1.016
1.011
1.006
1.004
1.002
1.014
1.010
1.006
1.004
1.002
1.014
1.010
1.006
1.004
1.002
RC
5%
56.52
60.87
65.22
82.61
91.30
56.52
60.87
73.91
86.96
86.96
56.52
65.22
65.22
82.61
86.96
56.52
60.87
69.57
78.26
82.61
10%
65.22
78.26
86.96
91.30
95.65
65.22
78.26
86.96
86.96
86.96
69.57
78.26
86.96
95.65
95.65
65.22
65.22
86.96
86.96
86.96
QLIKE
Avg
1.237
1.154
1.106
1.074
1.046
1.242
1.162
1.102
1.069
1.035
1.206
1.147
1.097
1.075
1.054
1.221
1.142
1.098
1.079
1.058
Med
1.237
1.155
1.100
1.064
1.043
1.235
1.152
1.095
1.067
1.030
1.208
1.154
1.099
1.069
1.055
1.224
1.153
1.105
1.068
1.054
RC
5%
0.00
0.00
0.00
0.00
17.39
0.00
0.00
0.00
13.04
39.13
0.00
0.00
4.35
21.74
43.48
0.00
0.00
4.35
21.74
30.44
10%
0.00
0.00
0.00
0.00
21.74
0.00
0.00
13.04
21.74
52.17
0.00
0.00
8.70
34.78
43.48
0.00
4.35
8.70
26.09
30.44
MDA
Avg
1.039
1.032
1.025
1.022
1.019
1.037
1.036
1.027
1.023
1.023
1.034
1.027
1.020
1.018
1.015
1.036
1.025
1.021
1.020
1.016
Med
1.037
1.027
1.022
1.013
1.022
1.034
1.034
1.034
1.024
1.019
1.034
1.022
1.013
1.013
1.013
1.037
1.022
1.022
1.013
1.014
RC
5%
8.70
13.04
26.09
30.44
60.87
13.04
13.04
21.74
21.74
39.13
17.39
13.04
34.78
52.17
65.22
13.04
13.04
30.44
39.13
52.17
10%
13.04
21.74
26.09
47.83
69.57
13.04
13.04
21.74
34.78
60.87
21.74
21.74
47.83
56.52
73.91
17.39
17.39
39.13
52.17
56.52
Notes: The results present the out-of-sample volatility forecasting performance of ensemble models. These ensemble models are constructed as weighted averages, combining the CHAR model, identified as the best-
performing model within the HAR-family of models, with each ML model evaluated in Section 5. The ensemble assigns weights of 0.75 to the CHAR model and 0.25 to the respective ML model.
a The mean (or median) MSE ratio of ensemble model to CHAR for 23 tickers. A ratio above one indicates degradation, while below one indicates improvement.
b The mean (or median) QLIKE ratio of ensemble
model to CHAR for 23 tickers. A ratio above one indicates degradation, while below one indicates improvement.
c The mean (or median) MDA ratio of CHAR to ensemble model for 23 tickers. A ratio above one
indicates degradation, while below one indicates improvement.
d Percentage of tickers with the outstanding performance of ensemble model against the HAR-family of models at the 5% and 10% significance levels.


## Page 62

robustness, ensemble models offer a promising alternative by combining the respective strengths
of each modelling approach.
9
Discussions and Conclusions
This study evaluates the performance of ML models, combined with a comprehensive set of
features, for RV forecasting from 27 July 2007 to 27 January 2022. Three types of daily data
are utilised: six HAR variables, 132 LOB variables, and nine news sentiment variables. The full
sample period is divided into an in-sample training period, from 27 July 2007 to 11 September
2015, and an out-of-sample forecasting period, from 14 September 2015 to 27 January 2022.
A diverse set of neural network-based ML models, incorporating different information sets and
architectural designs, is used to train and evaluate over seven million model variants.
Empirical results show that ML models outperformed all HAR-family of models, and that
LOB variables, relative to news sentiments and HAR variables, emerged as the most informative
predictors for forecasting RV. However, this statistically significant improvement applies only to
90% of out-of-sample daily forecasts when the actual RV is not extremely high. For a small
number of tickers, and for the remaining 10% of the out-of-sample forecasts when the actual
RV is extremely high, HAR-family of models outperformed ML models. The underperformance
of ML models during periods of high volatility affected their overall out-of-sample performance,
suggesting that ML models should not be viewed as direct substitutes for conventional HAR-
family of models. Our findings remain qualitatively the same when the forecasts are evaluated
using MSE, QLIKE, MDA, or RC. Also, our findings emphasise not only the importance of
capturing nonlinear relationships in the RV dynamics but also the importance of including a rich
collection of predictors in a forecasting ML model to achieve better performance when using ML
models.
The ML model is a black box, giving very little clue about which predictors contributed to
good forecasting performance. Here, we implemented SHAP, an XAI technique, to identify the
predictors that provided the greatest forecasting power. Results from SHAP suggest that, among
the 147 input variables, mid prices at all LOB levels, mean bid and mean ask from the LOB,
BPV from HAR, news count, and the ‘uncertainty’ sentiment are identified as the most important
predictive variables for forecasting RV. In general, LOB variables have stronger predictive power
62


## Page 63

than HAR and news sentiment variables.
There are also some performance variations across
time. Notably, HAR variables, while generally of low importance, became highly informative
during periods of extreme volatility, such as the COVID-19 crisis. Conversely, in more stable
market conditions (pre-2018), news sentiment played a dominant role, while LOB variables gained
importance post-2018 amid increased volatility. Once again, these changes over time highlight
the importance of incorporating a broad and diverse range of predictors in ML models for RV
forecasting. It also reinforces the important role of the HAR-family of models, and particularly
their variables, in achieving accurate RV forecasting, especially on high volatility days.
To further validate the reliability of our findings, we conducted extensive robustness checks,
including variations in model type, input variable selection, alternative loss functions, and mea-
sures to mitigate overfitting. These tests consistently confirmed the superiority of ML models
over the HAR-family of models during normal volatility days, while highlighting their relative
vulnerability during high volatility days. In response to this, we proposed a simple yet effective
ensemble approach that combines forecasts from both ML and HAR-family of models. This en-
semble method leverages the strengths of each model class, capturing nonlinear dynamics via ML
while maintaining robustness during turbulent market periods through HAR, resulting in more
stable and accurate forecasts across a wide range of market conditions. The success of the en-
semble underscores the value of integrating diverse modelling approaches in volatility forecasting
rather than relying exclusively on either traditional econometric methods or ML. Therefore, we
stress that replacing conventional HAR-family of models with ML models can be dangerous in
practice, and emphasise that this should be done with caution, where ensemble methods offer a
simple alternative.
To summarise, our findings indicate that neither ML models nor HAR-family specifications
exhibit uniform dominance in RV forecasting. Instead, relative performance depends critically
on sample composition, prevailing market conditions, modelling design, and the choice of ML
architecture.
ML models exploit their flexibility and richer information sets to deliver supe-
rior performance primarily during normal volatility days; however, these gains are sensitive to
model specification, hyperparameter tuning, and architectural choices. In contrast, HAR-family
of models provide more stable and robust forecasts, particularly during high volatility days that
are predominantly driven by firm-specific shocks and, to a lesser extent, by broader market-wide
stress. This distinction helps explain the divergent conclusions in the literature regarding whether
63


## Page 64

ML models can serve as direct replacements for HAR-type benchmarks when these are imple-
mented across different asset universes and sample timeframes. Overall, these results highlight the
importance of regime awareness and careful model integration when developing and evaluating
RV forecasting frameworks.
This study provides a new understanding of the complexities behind developing ML models
for volatility forecasting. The tuning of the ML hyperparameters, the choice of the loss function,
and the information content of a large volume of input variables can all affect the forecasting
performance conditioned on the level of actual RV. This study is among the first comprehensive
assessments to employ a rich feature set for RV forecasting and lays the foundation for future ML
research in this area. Future research could extend the forecast evaluation to include multi-step-
ahead RV predictions. Another promising direction is the implementation of switching methods
to adjust models in response to evolving market conditions. Additionally, tree-based models such
as XGBoost (Chen and Guestrin, 2016) and LGBM (Ke et al., 2017) offer valuable opportunities
for further investigation. The application of Transformer-based architectures, which have recently
gained significant attention (Vaswani et al., 2017), also merits further exploration. Finally, de-
veloping a universal model for RV forecasting by leveraging comprehensive market information
represents an exciting avenue for future research.
64


## Page 65

A
LOBSTER Dataset and Data Cleaning
The LOBSTER dataset is used to extract the HAR variables described in Subsection 3.1 and the
LOB variables described in Subsection 3.3. Prior to computing these variables, the LOBSTER
dataset is preprocessed using a set of modified cleaning steps based on Barndorff-Nielsen et al.
(2009). These steps are applied to both the LOB and message data in the following way (the step
names, such as P2, T4, ..., are consistent with the names in Barndorff-Nielsen et al. (2009)):
• P2: Delete entries with a bid, ask or transaction price equal to zero.
• T4: Delete entries with prices that are above the ‘ask’ plus the bid-ask spread, or below
the ‘bid’ minus the bid-ask spread.
• Q1: When multiple quotes share the same timestamp, they are replaced by a single entry
using the median bid price, median ask price, and the sum of all volumes from these mul-
tiple quotes. For messages with the same direction (buy or sell), the mentioned procedure
is applied to the message data, and the last snapshot of the LOB is selected as the LOB
associated with the merged message data. For messages with different directions, the mes-
sage data and the LOB with the same direction are grouped, and the mentioned procedure
is applied separately to the buy-side and sell-side.
• Q2: Delete entries for which the spread is negative.
• Q3: Delete entries for which the spread is more than 50 times the median spread on that
day.
• Q4: Delete entries for which the mid-quote deviated by more than 10 mean absolute devi-
ations from a rolling centred median (excluding the observation under consideration) of 50
observations (25 observations before and 25 after).
The summary statistics pertaining to the data cleaning steps are presented in Table A1.
65


## Page 66

Table A1: Data Cleaning Summary Statistics
Sample Period From 27 July 2007 to 27 January 2022
Name
Ticker
Sample Size
Removed (%)
P2 (%)
T4 (%)
Q1 (%)
Q2 (%)
Q3 (%)
Q4 (%)
Apple
AAPL
4,174,971,328
34.22
0.00
29.88
4.34
0.00
0.00
0.00
Microsoft
MSFT
3,827,824,574
35.88
0.01
30.18
5.69
0.00
0.00
0.00
Intel
INTC
2,807,965,330
38.59
0.01
31.79
6.78
0.01
0.00
0.01
Comcast
CMCSA
2,390,133,817
45.18
0.01
39.59
5.58
0.00
0.00
0.01
Qualcomm
QCOM
2,086,295,132
41.46
0.00
36.46
4.98
0.00
0.00
0.01
Cisco Systems
CSCO
2,296,179,428
40.46
0.01
33.50
6.94
0.00
0.00
0.01
eBay
EBAY
1,683,001,942
40.73
0.01
35.68
5.03
0.00
0.00
0.01
Gilead Sciences
GILD
1,404,574,567
41.68
0.00
38.41
3.25
0.00
0.00
0.01
Texas Instruments
TXN
1,485,049,597
39.45
0.00
35.14
4.29
0.00
0.00
0.01
Amazon.com
AMZN
1,201,210,867
23.06
0.00
19.89
3.15
0.00
0.00
0.02
Starbucks
SBUX
1,564,221,129
44.04
0.01
39.95
4.07
0.00
0.00
0.01
Nvidia
NVDA
1,548,447,223
35.47
0.01
30.40
5.05
0.00
0.00
0.01
Micron Technology
MU
2,110,482,619
35.99
0.00
31.11
4.86
0.00
0.00
0.01
Applied Materials
AMAT
1,616,466,522
39.70
0.01
34.41
5.27
0.00
0.00
0.01
NetApp
NTAP
1,015,914,054
44.99
0.01
41.14
3.82
0.00
0.00
0.02
Adobe
ADBE
1,083,392,595
37.76
0.01
34.35
3.39
0.00
0.00
0.02
Xilinx
XLNX
1,172,584,895
40.24
0.01
36.97
3.26
0.00
0.00
0.02
Amgen
AMGN
863,464,001
38.62
0.01
34.73
3.86
0.00
0.00
0.02
Vodafone Group
VOD
1,012,861,232
47.20
0.01
44.23
2.95
0.00
0.00
0.02
Cognizant
CTSH
928,987,253
46.22
0.01
43.28
2.91
0.00
0.00
0.02
KLA Corporation
KLAC
783,931,409
42.63
0.01
39.83
2.77
0.00
0.00
0.02
Paccar
PCAR
775,954,122
45.74
0.01
42.98
2.73
0.00
0.00
0.03
Autodesk
ADSK
803,552,017
41.73
0.01
38.96
2.74
0.00
0.00
0.02
Average
40.05
0.01
35.78
4.25
0.00
0.00
0.01
Notes: P2: Delete entries with a bid, ask or transaction price equal to zero, T4: Delete entries with prices that are above the ‘ask’ plus the
bid-ask spread, or below the ‘bid’ minus the bid-ask spread, Q1: When multiple quotes share the same timestamp, they are replaced by a single
entry using the median bid price, median ask price, the sum of all volumes, and the last snapshot of the LOB is selected as the LOB associated
with the merged message data. For messages with different directions (buy or sell), the message data and the LOB with the same direction
are grouped according to the buy side or sell side. The procedure mentioned above is then applied to the message data, and the last snapshot
of the LOB of the group, Q2: Delete entries for which the spread is negative, Q3: Delete entries for which the spread is more than 50 times
the median spread on that day, Q4: Delete entries for which the mid-quote deviated by more than 10 mean absolute deviations from a rolling
centred median (excluding the observation under consideration) of 50 observations (25 observations before and 25 after).
Table A2: RV Descriptive Statistics (Without Cleaning)
Sample Period From 27 July 2007 to 27 January 2022
Ticker
Min
Max
1st quantile
Median
3rd quantile
Mean
STD
Kurtosis
Skewness
Correlationa
AAPL
0.101
229.529
0.898
1.737
3.702
4.623
12.579
110.333
9.093
0.9999
MSFT
0.096
216.486
0.828
1.458
2.810
3.240
8.119
194.967
11.294
0.9997
INTC
0.030
318.118
1.099
1.876
3.592
4.300
11.615
295.828
14.000
0.9999
CMCSA
0.006
237.387
0.913
1.631
3.344
3.833
9.773
190.221
11.459
0.9994
QCOM
0.123
368.449
1.025
1.980
4.140
5.076
15.363
197.106
12.012
0.9999
CSCO
0.038
343.946
0.884
1.564
3.031
4.117
13.170
213.266
12.287
0.9999
EBAY
0.215
259.723
1.328
2.263
4.361
5.111
12.745
142.560
10.028
0.9974
GILD
0.063
261.664
1.170
1.895
3.375
4.312
12.933
184.066
12.094
0.9999
TXN
0.183
289.765
1.046
1.895
3.713
4.006
9.928
310.664
14.275
0.9986
AMZN
0.066
551.566
1.307
2.342
4.833
6.203
19.355
246.159
12.802
0.9998
SBUX
0.048
265.554
0.864
1.594
3.441
4.209
11.227
161.691
10.615
0.9997
NVDA
0.159
1104.483
2.280
4.342
9.098
9.760
30.112
586.751
20.055
1.0000
MU
0.288
484.388
3.575
6.281
11.964
12.821
25.726
89.478
7.966
0.9990
AMAT
0.312
529.508
1.773
3.031
5.730
6.014
14.615
526.901
18.237
0.9999
NTAP
0.114
463.545
1.508
2.606
5.180
6.301
18.020
201.869
11.942
0.9998
ADBE
0.120
575.498
1.096
2.001
3.874
4.810
14.784
661.002
20.309
0.9998
XLNX
0.231
265.372
1.300
2.374
4.791
5.022
11.950
193.951
11.739
0.9990
AMGN
0.039
212.485
0.962
1.580
2.860
3.311
9.225
202.622
12.391
0.9995
VOD
0.043
217.091
0.684
1.334
3.081
3.693
9.500
149.567
10.122
0.9998
CTSH
0.186
493.255
0.979
1.743
4.085
5.218
15.843
339.283
14.667
0.9997
KLAC
0.149
499.806
1.451
2.701
5.412
5.820
16.308
384.071
16.516
0.9933
PCAR
0.029
389.021
1.157
2.172
4.657
5.137
12.123
309.547
12.928
0.9998
ADSK
0.268
696.615
1.642
2.770
5.176
6.660
22.503
389.706
16.604
0.9999
Notes: The descriptive statistics of RV without applying the cleaning steps are presented in this table, while the statistics after applying
the cleaning steps are reported in Table 1.
a Correlation between two sets of calculated RVs, with and without the implementation of the
cleaning steps described in Appendix A.
66


## Page 67

B
LSTM as a Unifying Framework
The LSTM architecture can be interpreted as a unifying framework that embeds a wide range of
familiar models within a single, general formulation. By imposing simple restrictions on its gating
mechanisms and state evolution, the LSTM reduces to well-known specifications, demonstrating
that many standard models arise as special cases of its structure. In particular, fixing the gates
at constant values yields dynamics equivalent to familiar linear and nonlinear models. Assume
the forget gate is Gf = ϕ, the input gate is set to Gi = 1 −ϕ, and the output gate is fully open,
Go = 1. Additionally, linearise the cell activation function by replacing tanh(·) in Equation (16)
with the identity function. With a constant candidate value ˜ct = ¯c, Equation (15) simplifies to:
ct = ϕct−1 + (1 −ϕ)¯c,
(B1)
and, since at = ct by Equation (16), the hidden output satisfies:
at = ϕat−1 + (1 −ϕ)¯c.
(B2)
Equation (B2) represents an AR(1) model with autoregressive coefficient ϕ and intercept (1−ϕ)¯c.
In this formulation, the gates serve the role of the autoregressive lag coefficient, while the candidate
cell bias determines the long-run mean. As the next case, assume that Gf = 1, Gi = 0, Go = 1,
and, similar to the previous case, replace the tanh(·) with the identity function. Under these
assumptions, Equation (15) and Equation (16) reduce to:
ct = ct−1,
at = ct,
(B3)
which becomes the familiar random walk, yt = yt−1+εt, once an additive noise term εt is included.
We now consider a different case. A final limiting configuration shows that the LSTM cell
collapses to an ordinary FCNN when the memory pathway is disabled and all gates are fixed. As-
sume that Gf = 0, Gi = 1, and Go = 1. Also, for every t, replace the internal nonlinearity tanh(·)
by the identity, and eliminate the recurrent connection by zeroing the part of the candidate-state
weight that multiplies the previous hidden state, wc = [ 0, wx ]. Then, from Equation (11), this
67


## Page 68

yields:
˜ct = wxXt + bc.
(B4)
Because Gf = 0 and Gi = 1, Equation (15) also reduces to:
ct = ˜ct = wxXt + bc.
(B5)
With Go = 1 and a linear output activation, Equation (16) simplifies to:
at = ct = wxXt + bc.
(B6)
Equation (B6) is precisely the affine map produced by a single fully connected layer, and the
hidden state no longer depends on past time steps. Stacking several such modified LSTM cells
therefore reproduces a standard FCNN. These special cases highlight how LSTM nests a range
of models, including AR(1), random walk, and FCNN, through simple gate configurations. This
illustrates its flexibility in capturing both dynamic and static relationships within a unified frame-
work.
68


## Page 69

C
Complementary Results
Table C1: Correlation Between RV from LOBSTER and TAQ
Ticker
Correlation
Ticker
Correlation
AAPL
0.8441
MU
0.8402
MSFT
0.9856
AMAT
0.8855
INTC
0.8898
NTAP
0.9674
QCOM
0.9036
ADBE
0.9452
CSCO
0.9786
XLNX
0.9176
EBAY
0.8715
AMGN
0.8353
GILD
0.8310
VOD
0.7188
TXN
0.9785
CTSH
0.9702
AMZN
0.8248
KLAC
0.7689
SBUX
0.7870
PCAR
0.7441
NVDA
0.7870
ADSK
0.8736
Notes: This table reports the correlation between daily RV computed from LOBSTER and
RV obtained from TAQ data. The procedures used to construct RV from TAQ data are con-
sistent with the data-cleaning approach in Appendix A and the RV construction methodology
in Section 2. For TAQ data, only cleaning steps that do not rely on LOB information are ap-
plied. The TAQ data are obtained from WRDS using two products. For 2007–2013 we rely
on the trade and quote monthly product, in which trade timestamps are recorded at second
level resolution. For 2014–2015 we use the millisecond trade and quote daily product, which
provides millisecond timestamps. By contrast, LOBSTER data are recorded at up to nanosec-
ond resolution. These differences in timestamp granularity may affect the statistics reported
in this table. Due to limited access to TAQ data, the analysis is restricted to the training pe-
riod from 27 July 2007 to 11 September 2015. The only missing ticker is CMCSA, which is
excluded because it is not available in TAQ for the training period.
69


## Page 70

Table C2: Parameter Estimates of HAR-family of Models
AR(1)
HAR
HAR-J
CHAR
SHAR
ARQ
HARQ
HARQ-F
β0
3.6436a
1.8528
1.4401
1.2273
1.8444
2.8734
1.6127
0.6807
(1.6305)b
(0.9216)
(0.6446)
(0.6357)
(0.9213)
(1.3585)
(0.8758)
(0.8382)
(100, 0)c
(100, 0)
(99.9, 0.1)
(98.7, 1.3)
(99.9, 0.1)
(100, 0)
(99.9, 0.1)
(77.2, 22.8)
β1
0.1428
0.0394
0.6544
0.3653
0.2136
0.1695
(0.1090)
(0.0382)
(0.2743)
(0.2028)
(0.1093)
(0.1193)
(100, 0)
(93.8, 6.2)
(100, 0)
(100, 0)
(100, 0)
(99.3, 0.7)
β+
1
0.0625
(0.0942)
(92.8, 7.2)
β−
1
0.0346
(0.0390)
(88.4, 11.6)
βw
0.1471
0.0523
0.1449
0.1123
0.2076
(0.1805)
(0.1305)
(0.1774)
(0.1568)
(0.1731)
(77.2, 22.8)
(60.2, 39.8)
(77.0, 23.0)
(72.6, 27.4)
(89.6, 10.4)
βm
0.3566
0.2510
0.3527
0.3090
0.5367
(0.1754)
(0.1562)
(0.1767)
(0.1675)
(0.1956)
(100, 0)
(97.1, 2.9)
(98.7, 1.3)
(98.1, 1.9)
(100, 0)
βjump
-0.7353
(0.2840)
(0, 100)
βd
BP V
0.4136
(0.2526)
(98.3, 1.7)
βw
BP V
0.3434
(0.2926)
(91.2, 8.8)
βm
BP V
0.4336
(0.3329)
(92.5, 7.5)
β1Q
-0.0004
-0.0003
-0.0002
(0.0004)
(0.0003)
(0.0003)
(0.4, 99.6)
(0.6, 99.4)
(2.0, 98.0)
βw
Q
-0.0008
(0.0013)
(22.0, 78.0)
βm
Q
-0.0064
(0.0080)
(7.4, 92.6)
Adj. R2(avg)
0.0318
0.0721
0.0984
0.1000
0.0731
0.0583
0.0818
0.0871
Adj. R2(med)
0.0104
0.0404
0.0673
0.0692
0.0406
0.0406
0.0505
0.0552
MSE (avg)
173.3761
165.6939
161.0308
160.7043
165.4823
168.4723
163.9610
162.7886
MSE (med)
127.6872
124.0916
120.5695
119.9260
124.0427
125.2517
121.4500
120.8497
QLIKE (avg)
0.6139
0.5619
0.5177
0.5167
0.5615
0.5773
0.5481
0.5599
QLIKE (med)
0.6223
0.5670
0.5187
0.5236
0.5656
0.5813
0.5452
0.5737
MDA (avg)
59.7570
61.5238
60.4922
60.8509
61.4839
59.0413
60.9705
61.5254
MDA (med)
59.6088
61.4181
60.3423
61.0758
61.3203
59.0709
60.9291
61.2225
Notes: We summarise the results by reporting the mean[a], the standard deviation[b], and the fractions of pos-
itive and negative coefficients[c]. These statistics are computed from 36,892 daily coefficient estimates, corre-
sponding to 1,604 trading days across 23 stocks. These values are aggregated across all 23 stocks, using either
the overall average (or median). The HAR model follows Corsi (2009). HAR-J and CHAR are based on An-
dersen et al. (2007); Corsi and Reno (2009). SHAR follows Patton and Sheppard (2015). ARQ, HARQ, and
HARQ-F follow Bollerslev et al. (2016). RV is computed using 5-minute returns. For each stock, MSE, QLIKE,
and MDA are calculated as the average (or median) in-sample errors.
70


## Page 71

71
Table C3: HAR-family Out-of-Sample Forecasting Performance
AR(1)
HAR
HAR-J
CHAR
SHAR
ARQ
HARQ
HARQ-F
Full Out-of-Sample
MSEa
Avg
218.957
208.345
199.070
198.924
209.478
210.459
204.707
207.962
Med
144.744
137.001
130.463
129.495
138.829
142.448
136.673
147.108
RCd
5%
52.17
73.91
95.65
100
73.91
47.83
69.57
82.61
10%
86.96
95.65
100
100
95.65
69.57
86.96
95.65
QLIKEb
Avg
0.693
0.608
0.552
0.543
0.608
0.641
0.590
0.607
Med
0.687
0.612
0.560
0.537
0.606
0.650
0.591
0.601
RC
5%
0.00
0.00
86.96
100
0.00
0.00
8.70
13.04
10%
0.00
0.00
86.96
100
0.00
8.70
8.70
17.39
MDAc
Avg
59.961
61.230
60.276
60.639
61.146
59.269
60.701
60.954
Med
59.888
60.699
59.638
60.137
60.761
59.139
60.200
60.699
RC
5%
52.17
100
47.83
73.91
95.65
34.78
52.17
91.30
10%
69.57
100
69.57
82.61
100
39.13
73.91
95.65
Normal Volatility Days
MSE
Avg
11.745
11.228
9.030
7.730
12.230
10.115
10.364
10.808
Med
7.798
7.000
5.947
5.091
7.489
7.478
7.101
7.392
RC
5%
47.83
52.17
52.17
95.65
56.52
26.09
26.09
26.09
10%
56.52
60.87
69.57
95.65
78.26
30.44
47.83
30.44
QLIKE
Avg
0.399
0.340
0.313
0.298
0.339
0.364
0.327
0.318
Med
0.362
0.327
0.296
0.269
0.330
0.339
0.314
0.303
RC
5%
0.00
4.35
21.74
95.65
0.00
0.00
13.04
43.48
10%
0.00
4.35
34.78
95.65
0.00
0.00
17.39
56.52
MDA
Avg
57.370
58.363
56.429
56.768
58.276
55.891
57.334
57.735
Med
57.322
58.491
55.734
56.407
58.298
55.463
57.300
57.848
RC
5%
73.91
95.65
13.04
39.13
95.65
13.04
13.04
73.91
10%
78.26
100
13.04
43.48
100
17.39
34.78
82.61
High Volatility Days
MSE
Avg
2131.361
2028.059
1954.202
1964.630
2030.282
2060.872
1999.278
2027.084
Med
1293.253
1223.783
1171.940
1163.489
1236.025
1266.151
1218.390
1334.427
RC
5%
47.83
69.57
100
91.30
69.57
69.57
91.30
100
10%
91.30
91.30
100
100
95.65
91.30
91.30
100
QLIKE
Avg
3.329
3.008
2.690
2.739
3.015
3.126
2.946
3.184
Med
3.275
2.905
2.618
2.691
2.914
3.109
2.902
3.108
RC
5%
43.48
52.17
95.65
100
47.83
69.57
43.48
26.09
10%
73.91
56.52
95.65
100
56.52
82.61
52.17
52.17
MDA
Avg
51.243
52.609
54.261
54.508
52.561
51.423
52.598
52.835
Med
51.282
53.012
54.386
54.839
53.012
51.534
52.601
52.941
RC
5%
0.00
4.35
95.65
86.96
8.70
21.74
21.74
39.13
10%
0.00
21.74
100
95.65
13.04
26.09
30.43
39.13
Notes: The best value in each row is marked in bold.
a Averaging (or taking the median of) the MSE across 23 stocks; lower values indicate better performance.
b Averaging (or taking the median of) the
QLIKE across 23 stocks; lower values indicate better performance.
c Averaging (or taking the median of) the MDA across 23 stocks; higher values indicate better performance.
d Percentage of tickers with outstanding performance of the specified model against the HAR-family of models, excluding the model under assessment, at the 5% and 10% significance levels.


## Page 72

Table C4: Sanity Check Filter Counts Across HAR-family of Models
Statistic
AR(1)
HAR
HAR-J
CHAR
SHAR
ARQ
HARQ
HARQ-F
Mean
0
0
2
0
0
1
1
3
Median
0
0
1
0
0
1
1
1
Min
0
0
0
0
0
0
0
0
Max
0
0
8
0
0
4
3
10
STD
0
0
2
0
0
1
1
3
Notes: This table reports summary statistics for the number of times the sanity check filter is
applied for the HAR-family of models during the out-of-sample period. The statistics are com-
puted across 23 individual stocks. For each stock, the count is obtained by recording the number
of RV forecast occasions over the out-of-sample evaluation window in which the RV forecast falls
outside the range of RV observed in the corresponding rolling in-sample window. In such cases,
the forecasted RV is replaced by the in-sample mean RV. The maximum achievable value is 1,604,
corresponding to the total number of out-of-sample trading days.
Table C5: Sanity Check Filter Counts Across ML Models
HAR-ML
News-ML
OB-ML
News/OB-ML
Statistic
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
Mean
42
4
11
2
0
83
20
17
14
12
78
7
13
16
19
72
8
18
19
19
Median
25
0
0
0
0
70
10
4
8
6
11
3
6
5
7
23
4
4
3
7
Min
0
0
0
0
0
11
2
0
0
0
0
0
0
0
0
0
0
0
0
0
Max
269
48
207
31
0
199
104
55
66
88
811
45
65
95
89
396
53
137
144
135
STD
62
10
44
7
0
48
23
20
18
20
181
11
17
25
27
124
12
35
36
35
Notes: This table presents summary statistics on the frequency with which the sanity check filter is applied in the HAR-ML, News-
ML, OB-ML, and News/OB-ML models, for alternative model specifications using 5, 10, 15, 20, and 25 units, over the out-of-sample
period. The statistics are computed across 23 individual stocks. For each stock, the count is obtained by recording the number of
RV forecast occasions over the out-of-sample evaluation window in which the RV forecast falls outside the range of RV observed in
the corresponding rolling in-sample window. In such cases, the forecasted RV is replaced by the in-sample mean RV. The maximum
achievable value is 1,604, corresponding to the total number of out-of-sample trading days.
72


## Page 73

73
Table C6: Benchmark Robustness: Out-of-Sample Performance Relative to HAR
14 September 2015 to 27 January 2022 (1,604 days)
HAR-ML
News-ML
OB-ML
News/OB-ML
Units
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
Full Out-of-Sample
MSEa
Avg
1.168
1.143
1.127
1.107
1.093
1.173
1.148
1.128
1.112
1.097
1.153
1.124
1.103
1.091
1.084
1.160
1.124
1.103
1.097
1.086
Med
1.143
1.123
1.103
1.082
1.066
1.148
1.128
1.108
1.090
1.076
1.129
1.098
1.086
1.078
1.065
1.129
1.108
1.085
1.080
1.070
QLIKEb
Avg
7.239
3.462
2.250
1.555
1.245
6.968
3.809
2.329
1.786
1.365
4.334
2.081
1.483
1.365
1.256
5.533
1.984
1.504
1.467
1.302
Med
6.115
2.950
1.950
1.367
1.163
6.980
3.779
2.276
1.568
1.203
2.893
1.805
1.352
1.293
1.239
4.539
1.731
1.391
1.315
1.231
MDAc
Avg
1.025
1.003
0.982
0.978
0.979
1.026
1.009
0.984
0.974
0.971
0.976
0.955
0.948
0.952
0.965
1.002
0.952
0.947
0.954
0.961
Med
1.029
0.995
0.976
0.978
0.981
1.013
0.999
0.985
0.970
0.973
0.955
0.951
0.951
0.956
0.965
0.970
0.949
0.947
0.957
0.960
Normal Volatility Days
MSE
Avg
0.509
0.459
0.427
0.422
0.430
0.511
0.485
0.448
0.445
0.464
0.390
0.343
0.343
0.377
0.417
0.443
0.343
0.354
0.374
0.413
Med
0.458
0.430
0.450
0.467
0.439
0.438
0.447
0.454
0.451
0.497
0.367
0.296
0.330
0.376
0.419
0.380
0.302
0.319
0.374
0.415
QLIKE
Avg
4.183
1.857
1.110
0.912
0.814
4.219
2.342
1.316
1.045
0.910
2.338
1.008
0.811
0.834
0.845
3.416
0.969
0.835
0.901
0.855
Med
3.365
1.317
0.864
0.865
0.824
3.558
1.760
1.212
0.948
0.879
1.286
0.795
0.804
0.848
0.854
2.129
0.806
0.820
0.833
0.853
MDA
Avg
0.981
0.968
0.952
0.954
0.963
0.983
0.971
0.951
0.946
0.950
0.930
0.913
0.915
0.926
0.947
0.955
0.910
0.916
0.923
0.942
Med
0.979
0.970
0.947
0.954
0.964
0.974
0.965
0.945
0.942
0.940
0.919
0.912
0.925
0.933
0.948
0.925
0.912
0.924
0.931
0.937
High Volatility Days
MSE
Avg
1.203
1.179
1.163
1.143
1.127
1.207
1.183
1.163
1.146
1.130
1.192
1.165
1.142
1.128
1.118
1.197
1.164
1.142
1.135
1.120
Med
1.178
1.160
1.146
1.130
1.115
1.178
1.167
1.155
1.130
1.115
1.165
1.139
1.117
1.122
1.095
1.175
1.145
1.123
1.116
1.103
QLIKE
Avg
10.394
5.098
3.411
2.207
1.682
10.089
5.391
3.407
2.558
1.828
6.446
3.191
2.178
1.923
1.693
7.848
3.033
2.207
2.042
1.782
Med
8.386
4.030
3.078
1.877
1.557
9.862
5.502
2.903
2.074
1.631
4.668
2.968
2.105
1.804
1.621
5.898
3.030
2.112
1.832
1.611
MDA
Avg
1.031
1.027
1.025
1.021
1.024
1.031
1.026
1.024
1.021
1.019
1.031
1.027
1.025
1.021
1.016
1.031
1.026
1.022
1.018
1.012
Med
1.034
1.029
1.033
1.022
1.029
1.034
1.034
1.025
1.025
1.025
1.034
1.034
1.029
1.023
1.014
1.034
1.034
1.034
1.022
1.014
Notes: This table reports out-of-sample performance measures using the standard HAR model as the benchmark and complements the results in Table 6 and Table 7, which use CHAR as the benchmark.
a Averaging (or taking the median of) the MSE across 23 stocks; lower values indicate better performance.
b Averaging (or taking the median of) the QLIKE across 23 stocks; lower values indicate better performance.
c Averaging (or taking the median of) the MDA across 23 stocks; higher values indicate better performance.


## Page 74

74
Table C7: Out-of-Sample Volatility Forecasting Performance of ML Models (Increasing Window)
14 September 2015 to 27 January 2022 (1,604 days)
HAR-ML
News-ML
OB-ML
News/OB-ML
Units
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
Full Out-of-Sample
MSEa
Avg
1.253
1.238
1.079
1.067
1.141
1.259
1.241
1.215
1.183
1.070
1.139
1.105
1.157
1.192
1.105
1.204
1.137
1.098
1.187
1.172
Med
1.225
1.212
1.078
1.060
1.117
1.225
1.216
1.201
1.167
1.062
1.130
1.101
1.144
1.164
1.084
1.154
1.111
1.088
1.165
1.154
RCd
5%
17.39
30.44
100
100
86.96
17.39
34.78
47.83
69.57
100
91.30
100
73.91
65.22
82.61
52.17
86.96
95.65
60.87
73.91
10%
56.52
69.57
100
100
100
56.52
65.22
73.91
91.30
100
100
100
82.61
78.26
100
82.61
91.30
100
73.91
82.61
QLIKEb
Avg
8.654
4.350
1.038
1.031
1.276
8.853
5.055
3.100
1.730
1.190
1.368
1.296
1.854
2.509
1.702
4.487
2.234
1.598
1.912
1.766
Med
7.455
3.993
1.031
1.033
1.274
8.143
4.387
2.856
1.550
1.149
1.360
1.332
1.542
1.846
1.555
2.699
1.367
1.353
1.844
1.480
RC
5%
0.00
0.00
86.96
86.96
43.48
0.00
0.00
0.00
4.35
43.48
17.39
26.09
8.70
0.00
0.00
4.35
13.04
13.04
0.00
4.35
10%
0.00
0.00
100
95.65
60.87
0.00
0.00
4.35
26.09
56.52
21.74
34.78
17.39
17.39
0.00
13.04
21.74
13.04
4.35
13.04
MDAc
Avg
1.028
1.004
0.969
0.971
0.975
1.030
1.008
0.978
0.967
0.963
0.933
0.943
0.953
0.953
0.963
0.977
0.957
0.955
0.950
0.944
Med
1.021
0.994
0.970
0.971
0.977
1.039
0.986
0.972
0.969
0.959
0.933
0.951
0.951
0.948
0.967
0.972
0.949
0.949
0.950
0.940
RC
5%
47.83
69.57
100
100
95.65
52.17
69.57
95.65
100
100
100
100
95.65
91.30
95.65
73.91
91.30
100
100
100
10%
47.83
73.91
100
100
95.65
56.52
73.91
100
100
100
100
100
95.65
91.30
100
73.91
91.30
100
100
100
Normal Volatility Days
MSE
Avg
0.894
0.738
0.761
0.826
0.766
0.954
0.793
0.716
0.667
1.054
0.549
0.751
0.621
0.635
1.027
0.695
0.777
0.913
0.561
0.568
Med
0.757
0.684
0.741
0.801
0.761
0.941
0.799
0.696
0.645
1.022
0.536
0.729
0.622
0.600
0.928
0.538
0.748
0.846
0.529
0.580
RC
5%
82.61
100
95.65
91.30
91.30
78.26
95.65
95.65
100
69.57
100
91.30
100
91.30
69.57
91.30
91.30
78.26
100
100
10%
86.96
100
100
91.30
91.30
78.26
95.65
95.65
100
69.57
100
100
100
91.30
73.91
91.30
91.30
82.61
100
100
QLIKE
Avg
5.844
2.754
0.876
0.888
0.996
6.116
3.192
1.843
1.146
1.053
0.910
1.000
1.121
1.592
1.401
2.596
1.554
1.291
1.080
1.028
Med
4.594
2.116
0.873
0.881
0.972
4.950
2.290
1.578
1.041
1.076
0.889
1.013
1.086
1.017
1.354
1.157
1.090
1.298
0.996
1.039
RC
5%
0.00
8.70
91.30
91.30
69.57
0.00
0.00
8.70
47.83
56.52
86.96
78.26
60.87
60.87
21.74
52.17
56.52
30.44
60.87
69.57
10%
8.70
13.04
91.30
91.30
69.57
0.00
0.00
13.04
47.83
60.87
86.96
82.61
69.57
60.87
30.44
52.17
65.22
39.13
65.22
82.61
MDA
Avg
0.966
0.947
0.958
0.959
0.947
0.969
0.953
0.925
0.921
0.934
0.889
0.907
0.903
0.901
0.926
0.918
0.916
0.920
0.896
0.895
Med
0.953
0.938
0.959
0.959
0.953
0.962
0.937
0.925
0.927
0.926
0.890
0.908
0.912
0.907
0.931
0.915
0.902
0.907
0.894
0.900
RC
5%
78.26
95.65
95.65
91.30
86.96
82.61
86.96
100
100
100
100
100
100
95.65
95.65
86.96
91.30
100
95.65
100
10%
78.26
95.65
95.65
91.30
86.96
91.30
95.65
100
100
100
100
100
100
95.65
95.65
95.65
91.30
100
100
100
High Volatility Days
MSE
Avg
1.268
1.258
1.090
1.075
1.154
1.270
1.257
1.234
1.202
1.070
1.162
1.120
1.177
1.212
1.108
1.224
1.152
1.106
1.211
1.196
Med
1.231
1.225
1.082
1.068
1.136
1.227
1.223
1.213
1.180
1.050
1.142
1.113
1.157
1.180
1.076
1.192
1.120
1.089
1.180
1.168
RC
5%
13.04
17.39
100
100
73.91
13.04
17.39
39.13
47.83
95.65
60.87
86.96
65.22
30.44
69.57
30.44
73.91
86.96
39.13
56.52
10%
43.48
43.48
100
100
78.26
39.13
47.83
56.52
69.57
100
78.26
95.65
69.57
65.22
82.61
52.17
86.96
95.65
60.87
65.22
QLIKE
Avg
11.871
6.118
1.210
1.186
1.550
12.134
7.021
4.541
2.343
1.359
1.891
1.638
2.677
3.585
2.071
6.903
3.061
1.984
2.824
2.644
Med
10.680
5.756
1.207
1.173
1.428
12.421
6.624
3.911
2.235
1.328
1.792
1.677
1.923
3.011
1.831
4.353
1.841
1.752
2.750
2.259
RC
5%
0.00
0.00
56.52
56.52
39.13
0.00
0.00
0.00
4.35
52.17
0.00
13.04
4.35
0.00
13.04
0.00
13.04
26.09
4.35
0.00
10%
0.00
0.00
65.22
69.57
60.87
0.00
0.00
0.00
26.09
65.22
4.35
26.09
8.70
0.00
21.74
4.35
30.44
43.48
4.35
4.35
MDA
Avg
1.076
1.074
0.995
0.985
1.040
1.077
1.073
1.068
1.069
0.987
1.054
1.014
1.042
1.069
1.021
1.071
1.033
1.002
1.070
1.068
Med
1.067
1.071
1.000
0.978
1.035
1.067
1.067
1.058
1.069
0.988
1.054
1.000
1.044
1.058
1.012
1.058
1.018
0.987
1.058
1.058
RC
5%
0.00
0.00
95.65
95.65
43.48
0.00
0.00
0.00
4.35
52.17
0.00
21.74
4.35
0.00
21.74
0.00
17.39
26.09
4.35
4.35
10%
0.00
0.00
95.65
95.65
52.17
0.00
0.00
4.35
8.70
69.57
13.04
30.44
13.04
0.00
30.44
4.35
34.78
30.44
4.35
8.70
Notes: The best value in each row is marked in bold.
a The mean (or median) MSE ratio of ML to CHAR for 23 tickers. A ratio above one indicates degradation, while below one indicates improvement.
b The mean (or median) QLIKE ratio of ML to CHAR for 23 tickers. A ratio above one indicates degradation, while below one indicates improvement.
c The mean (or median) MDA ratio of CHAR to ML for 23 tickers. A ratio
above one indicates degradation, while below one indicates improvement.
d Percentage of tickers with the outstanding performance of ML against the HAR-family of models at the 5% and 10% significance levels.


## Page 75

75
Table C8: Out-of-Sample Volatility Forecasting Performance of ML Models (Reduced In-Sample Training Period)
14 September 2015 to 27 January 2022 (1,604 days)
HAR-ML
News-ML
OB-ML
News/OB-ML
Units
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
Full Out-of-Sample
MSEa
Avg
1.206
1.203
1.185
1.166
1.155
1.198
1.195
1.181
1.159
1.147
1.137
1.102
1.146
1.135
1.116
1.189
1.166
1.085
1.131
1.119
Med
1.194
1.187
1.164
1.143
1.143
1.181
1.175
1.163
1.146
1.137
1.131
1.100
1.135
1.128
1.111
1.174
1.149
1.083
1.131
1.107
RCd
5%
17.39
26.09
30.44
47.83
47.83
21.74
30.44
39.13
56.52
60.87
60.87
91.30
60.87
69.57
78.26
34.78
39.13
95.65
69.57
82.61
10%
47.83
47.83
69.57
78.26
82.61
56.52
60.87
65.22
82.61
86.96
82.61
100
82.61
86.96
91.30
56.52
73.91
100
91.30
91.30
QLIKEb
Avg
9.053
6.634
4.563
3.050
2.053
8.596
6.206
4.051
2.546
2.105
1.862
1.453
2.324
1.861
1.523
4.250
3.157
1.422
1.826
1.680
Med
8.704
6.357
4.480
2.310
2.090
8.464
5.956
3.843
2.230
1.749
1.679
1.422
1.837
1.735
1.467
3.963
2.445
1.436
1.597
1.486
RC
5%
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
4.35
0.00
0.00
13.04
0.00
0.00
0.00
0.00
8.70
10%
0.00
0.00
0.00
0.00
17.39
0.00
0.00
0.00
0.00
8.70
0.00
8.70
8.70
8.70
21.74
0.00
4.35
4.35
0.00
13.04
MDAc
Avg
1.036
1.019
1.005
0.984
0.971
1.024
1.009
0.988
0.972
0.966
0.944
0.939
0.947
0.950
0.950
0.979
0.960
0.948
0.944
0.950
Med
1.033
1.009
0.996
0.972
0.967
1.015
1.015
0.981
0.967
0.967
0.947
0.937
0.937
0.943
0.952
0.988
0.942
0.952
0.942
0.945
RC
5%
47.83
56.52
69.57
95.65
95.65
60.87
60.87
86.96
91.30
100
95.65
100
100
100
100
82.61
91.30
100
100
100
10%
47.83
60.87
73.91
95.65
100
65.22
69.57
86.96
100
100
100
100
100
100
100
91.30
91.30
100
100
100
Normal Volatility Days
MSE
Avg
0.765
0.721
0.632
0.544
0.527
0.715
0.678
0.579
0.559
0.545
0.421
0.496
0.468
0.480
0.520
0.543
0.486
0.587
0.470
0.511
Med
0.743
0.661
0.604
0.515
0.538
0.660
0.675
0.531
0.525
0.512
0.378
0.476
0.424
0.441
0.484
0.523
0.474
0.556
0.420
0.500
RC
5%
91.30
95.65
91.30
100
100
91.30
91.30
100
100
100
100
100
100
100
100
100
100
100
100
100
10%
91.30
95.65
95.65
100
100
95.65
91.30
100
100
100
100
100
100
100
100
100
100
100
100
100
QLIKE
Avg
6.281
4.347
3.005
1.726
1.188
6.096
4.366
2.549
1.566
1.317
1.126
1.017
1.498
1.169
1.014
2.632
2.201
1.140
1.204
1.219
Med
6.259
3.656
3.085
1.321
1.085
5.670
3.862
2.693
1.451
1.110
1.027
0.986
1.070
1.050
0.958
2.232
1.358
1.029
1.033
1.007
RC
5%
0.00
0.00
0.00
17.39
47.83
0.00
0.00
13.04
26.09
56.52
73.91
82.61
56.52
60.87
69.57
8.70
39.13
52.17
69.57
65.22
10%
0.00
0.00
0.00
26.09
52.17
0.00
0.00
13.04
39.13
56.52
73.91
82.61
69.57
69.57
73.91
13.04
39.13
60.87
73.91
73.91
MDA
Avg
0.981
0.963
0.953
0.934
0.927
0.968
0.955
0.935
0.924
0.921
0.891
0.904
0.898
0.906
0.914
0.916
0.904
0.919
0.901
0.914
Med
0.983
0.961
0.943
0.929
0.932
0.967
0.975
0.931
0.916
0.921
0.895
0.900
0.896
0.900
0.914
0.925
0.900
0.923
0.901
0.907
RC
5%
78.26
86.96
91.30
100
100
82.61
91.30
95.65
100
100
100
100
100
100
100
100
100
100
100
100
10%
86.96
91.30
91.30
100
100
82.61
100
100
100
100
100
100
100
100
100
100
100
100
100
100
High Volatility Days
MSE
Avg
1.223
1.221
1.206
1.190
1.179
1.216
1.214
1.204
1.183
1.170
1.164
1.125
1.172
1.160
1.139
1.213
1.191
1.104
1.157
1.142
Med
1.218
1.218
1.193
1.179
1.173
1.189
1.199
1.196
1.177
1.161
1.154
1.131
1.166
1.164
1.139
1.204
1.190
1.109
1.150
1.141
RC
5%
4.35
13.04
17.39
34.78
34.78
8.70
13.04
21.74
34.78
34.78
39.13
47.83
34.78
34.78
47.83
17.39
26.09
69.57
43.48
39.13
10%
39.13
43.48
43.48
52.17
52.17
34.78
39.13
43.48
52.17
60.87
52.17
73.91
56.52
52.17
69.57
39.13
47.83
86.96
56.52
69.57
QLIKE
Avg
11.643
8.924
6.007
4.234
2.888
11.079
8.000
5.509
3.448
2.813
2.538
1.870
3.081
2.494
2.002
5.833
4.092
1.684
2.401
2.108
Med
10.574
8.520
5.673
3.364
2.800
10.413
8.209
5.069
3.041
2.351
2.368
1.852
2.641
2.403
1.858
5.273
3.552
1.646
2.274
1.948
RC
5%
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
4.35
0.00
0.00
4.35
0.00
0.00
4.35
0.00
4.35
10%
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
13.04
0.00
4.35
8.70
0.00
8.70
0.00
8.70
8.70
0.00
17.39
MDA
Avg
1.070
1.070
1.070
1.069
1.069
1.070
1.070
1.069
1.067
1.067
1.069
1.051
1.066
1.063
1.058
1.070
1.070
1.032
1.064
1.060
Med
1.080
1.080
1.080
1.080
1.080
1.080
1.080
1.080
1.073
1.073
1.080
1.056
1.073
1.073
1.070
1.080
1.080
1.026
1.073
1.073
RC
5%
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
0.00
0.00
0.00
0.00
0.00
8.70
0.00
0.00
10%
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
8.70
0.00
4.35
4.35
0.00
0.00
13.04
4.35
8.70
Notes: The best value in each row is marked in bold.
a The mean (or median) MSE ratio of ML to CHAR for 23 tickers. A ratio above one indicates degradation, while below one indicates improvement.
b The mean (or median) QLIKE ratio of ML to CHAR for 23 tickers. A ratio above one indicates degradation, while below one indicates improvement.
c The mean (or median) MDA ratio of CHAR to ML for 23 tickers. A ratio
above one indicates degradation, while below one indicates improvement.
d Percentage of tickers with the outstanding performance of ML against the HAR-family of models at the 5% and 10% significance levels.


## Page 76

0
20
40
60
80
100
Full Out-of-Sample
0.94
0.96
0.98
1.00
1.02
Full Out-of-Sample
HAR
News
OB
News/OB
MDA (avg)
MDA (med)
0
20
40
60
80
100
Normal Volatility Days
CHARx
0.88
0.90
0.92
0.94
0.96
0.98
1.00
1.02
1.04
Normal Volatility Days
Negative
Positive
Uncertainty
Litigious
Modalweak
Modalmoderate
Modalstrong
Constraining
News count
T1slope10
T1slope(10bid)
T1slope(10ask)
T1slope5
T1slope(5bid)
T1slope(5ask)
T2slope10
T2slope5
Depth10
Depth5
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
0
20
40
60
80
100
High Volatility Days
0.96
0.98
1.00
1.02
1.04
1.06
High Volatility Days
Reality Check (%)
Diﬀerence
Figure C1: Comparison of ML and CHARx Models (MDA)
Notes: The bar chart shows the percentage of tickers with outstanding performance considering the MDA loss
function at the 5% significance level of the RC compared to the HAR-family of models as the benchmark for each
specified CHARx model (grey bars) and the ML model (white bars). The values for the bar chart can be read from
the left-hand axis. The dashed (solid) line shows the average (median) out-of-sample MDAs of the CHAR relative
to the CHARx models (left group) and ML models (right group) across 23 tickers. A value below one indicates
improved performance of the ML model, while a value above one indicates degradation. The values for the dashed
and solid lines can be read from the right-hand axis. The horizontal dashed line represents no improvement.
76


## Page 77

0
20
40
60
80
100
Full Out-of-Sample
0.98
0.99
1.00
1.01
1.02
1.03
1.04
Full Out-of-Sample
MDA (avg)
MDA (med)
0
20
40
60
80
100
Normal Volatility Days
0.93
0.94
0.95
0.96
0.97
0.98
0.99
1.00
Normal Volatility Days
5
10
15
20
25
0
2
4
6
8
High Volatility Days
1.00
1.01
1.02
1.03
1.04
1.05
1.06
1.07
High V olatility Days
Reality Check (%)
Diﬀerence
Figure C2: LSTM with Φt = {RVt, ..., RVt−20} (MDA)
Notes: The bar chart is the percentage of tickers with outstanding performance considering the MDA loss function
at the 5% significance level of the RC compared to the HAR-family of models as the benchmark for every specified
number of units of the ML model. The values for the bar chart can be read from the left-hand axis. The dashed
(solid) line shows the average (median) out-of-sample MDAs of the CHAR model relative to the ML model across
23 tickers. A value below one indicates improved performance of the ML model, while a value above one indicates
degradation. The values for the dashed and solid lines can be read from the right-hand axis. The horizontal dashed
line represents no improvement.
77


## Page 78

0
10
20
30
40
50
Full Out-of-Sample
1.000
1.005
1.010
1.015
1.020
1.025
1.030
Full Out-of-Sample
MDA (avg)
MDA (med)
0
20
40
60
80
Normal Volatility Days
0.970
0.975
0.980
0.985
0.990
0.995
1.000
Normal Volatility Days
5
10
15
20
25
−0.04
−0.02
0.00
0.02
0.04
High Volatility Days
1.00
1.01
1.02
1.03
1.04
1.05
1.06
1.07
High V olatility Days
Reality Check (%)
Diﬀerence
Figure C3: FCNN with Φt = {RVt, RV
w
t−1, RV
m
t−1} (MDA)
Notes: The bar chart is the percentage of tickers with outstanding performance considering the MDA loss function
at the 5% significance level of the RC compared to the HAR-family of models as the benchmark for every specified
number of units of the ML model. The values for the bar chart can be read from the left-hand axis. The dashed
(solid) line shows the average (median) out-of-sample MDAs of the CHAR model relative to the ML model across
23 tickers. A value below one indicates improved performance of the ML model, while a value above one indicates
degradation. The values for the dashed and solid lines can be read from the right-hand axis. The horizontal dashed
line represents no improvement.
78


## Page 79

0
20
40
60
80
100
Full Out-of-Sample
0.94
0.95
0.96
0.97
0.98
0.99
1.00
1.01
Full Out-of-Sample
OB
OB(Limited)
MDA (avg)
MDA (med)
0
20
40
60
80
100
Normal Volatility Days
0.90
0.92
0.94
0.96
0.98
1.00
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
−0.04
−0.02
0.00
0.02
0.04
High Volatility Days
1.00
1.01
1.02
1.03
1.04
1.05
1.06
1.07
High Volatility Days
Reality Check (%)
Diﬀerence
Figure C4: Comparison of OB-ML and OB-ML (Limited) Models (MDA)
Notes: The bar chart is the percentage of tickers with the outstanding performance considering the MDA loss function
at the 5% significance level of the RC compared to the HAR-family of models as the benchmark for every specified
model. The first five bars represent the results obtained using the LOB information set in Subsection 3.3, while the
second five bars are those derived from the limited LOB information set. The dashed (solid) line shows the average
(median) out-of-sample MDAs of the CHAR model relative to the ML model across 23 tickers. A value below one
indicates improved performance of the ML model, while a value above one indicates degradation. The values for the
dashed and solid lines can be read from the right-hand axis. The horizontal dashed line represents no improvement.
79


## Page 80

AAPL
MSFT
INTC
CMCSA
QCOM
CSCO
EBAY
GILD
TXN
AMZN
SBUX
NVDA
MU
AMAT
NTAP
ADBE
XLNX
AMGN
VOD
CTSH
KLAC
PCAR
ADSK
Full Out-of-Sample
0.2
0.4
0.6
0.8
1.0
AAPL
MSFT
INTC
CMCSA
QCOM
CSCO
EBAY
GILD
TXN
AMZN
SBUX
NVDA
MU
AMAT
NTAP
ADBE
XLNX
AMGN
VOD
CTSH
KLAC
PCAR
ADSK
Normal Volatility Days
0.2
0.4
0.6
0.8
AAPL
MSFT
INTC
CMCSA
QCOM
CSCO
EBAY
GILD
TXN
AMZN
SBUX
NVDA
MU
AMAT
NTAP
ADBE
XLNX
AMGN
VOD
CTSH
KLAC
PCAR
ADSK
High Volatility Days
0.2
0.4
0.6
0.8
1.0
AR
HAR
HAR-J
CHAR
SHAR
ARQ
HARQ
HARQ-F
Figure C5: ρMDA between OB-ML (15 Units) and HAR-Family of Models
Notes: Each radar chart illustrates the performance of the AR(1), HAR, HAR-J, CHAR, SHAR, ARQ, HARQ,
and HARQ-F models relative to the OB-ML model with 15 units across the specified tickers based on the MDA loss
function. The evaluations are conducted over the full out-of-sample period (left figure), during normal volatility
days (middle figure), and during high volatility days (right figure). A value below one indicates improved perfor-
mance of the ML model, while a value above one indicates degradation. The bold circle represents the baseline
(no improvement, i.e., a value of one).
80


## Page 81

0
20
40
60
80
100
Full Out-of-Sample
0.94
0.96
0.98
1.00
1.02
1.04
Full Out-of-Sample
HAR
News
OB
News/OB
MDA (avg)
MDA (med)
0
20
40
60
80
100
Normal Volatility Days
0.90
0.92
0.94
0.96
0.98
1.00
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
0
1
2
3
4
High Volatility Days
1.00
1.01
1.02
1.03
1.04
1.05
1.06
1.07
High Volatility Days
Reality Check (%)
Diﬀerence
(a) Five Lags
0
20
40
60
80
100
Full Out-of-Sample
0.96
0.98
1.00
1.02
1.04
1.06
1.08
Full Out-of-Sample
HAR
News
OB
News/OB
MDA (avg)
MDA (med)
0
20
40
60
80
100
Normal Volatility Days
0.90
0.92
0.94
0.96
0.98
1.00
1.02
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
−0.04
−0.02
0.00
0.02
0.04
High Volatility Days
1.00
1.01
1.02
1.03
1.04
1.05
1.06
1.07
High Volatility Days
Reality Check (%)
Diﬀerence
(b) One Lag
Figure C6: ML Models with Restricted Number of Lags (MDA)
Notes: Figure C6a and Figure C6b display the results considering five lags (last week) and one lag (last day). The
bar chart is the percentage of tickers with the outstanding performance considering the MDA loss function at the 5%
significance level of the RC compared to the HAR-family of models as the benchmark for every HAR-ML, News-ML,
OB-ML, and News/OB-ML group. The values for the bar chart can be read from the left-hand axis. The dashed
(solid) line shows the average (median) out-of-sample MDAs of the CHAR model relative to the ML model across
23 tickers. A value below one indicates improved performance of the ML model, while a value above one indicates
degradation. The values for the dashed and solid lines can be read from the right-hand axis. The horizontal dashed
line represents no improvement.
81


## Page 82

0
20
40
60
80
100
Full Out-of-Sample
0.94
0.96
0.98
1.00
1.02
Full Out-of-Sample
HAR
News
OB
News/OB
MDA (avg)
MDA (med)
0
20
40
60
80
100
Normal Volatility Days
0.88
0.90
0.92
0.94
0.96
0.98
1.00
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
0
2
4
6
8
High Volatility Days
1.00
1.01
1.02
1.03
1.04
1.05
1.06
1.07
High Volatility Days
Reality Check (%)
Diﬀerence
(a) MSE Loss Function
0
20
40
60
80
Full Out-of-Sample
0.98
1.00
1.02
1.04
1.06
Full Out-of-Sample
HAR
News
OB
News/OB
MDA (avg)
MDA (med)
0
20
40
60
80
100
Normal Volatility Days
0.92
0.94
0.96
0.98
1.00
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
−0.04
−0.02
0.00
0.02
0.04
High Volatility Days
1.00
1.01
1.02
1.03
1.04
1.05
1.06
1.07
High Volatility Days
Reality Check (%)
Diﬀerence
(b) QLIKE Loss Function
Figure C7: Minimising MSE vs QLIKE as the Loss Function in Training (MDA)
Notes: Figure C7a (Figure C7b) presents the results for the four groups of ML models (HAR-ML, News-ML, OB-ML,
and News/OB-ML) trained using minimising MSE (QLIKE) as the loss function. The other model specifications are
the same as in Subsection 4.2. The bar chart is the percentage of tickers with the outstanding performance at the 5%
significance level of the RC compared to the HAR-family of models as the benchmark for every specified ML model.
The values for the bar chart can be read from the left-hand axis. The dashed (solid) line shows the average (median)
out-of-sample MDAs of the CHAR model relative to the ML model across 23 tickers. A value below one indicates
improved performance of the ML model, while a value above one indicates degradation. The values for the dashed
and solid lines can be read from the right-hand axis. The horizontal dashed line represents no improvement.
82


## Page 83

0
20
40
60
80
100
Full Out-of-Sample
0.94
0.96
0.98
1.00
1.02
Full Out-of-Sample
MDA (avg)
MDA (med)
0
20
40
60
80
100
Normal Volatility Days
0.88
0.90
0.92
0.94
0.96
0.98
1.00
Normal Volatility Days
0
2
4
6
8
10
12
High Volatility Days
1.00
1.01
1.02
1.03
1.04
1.05
1.06
1.07
High Volatility Days
HAR
News
OB
News/OB
Reality Check (%)
Diﬀerence
Figure C8: No. of Units vs. No. of Epochs (MDA)
Notes: From left to right, this figure consists of the HAR-ML, News-ML, OB-ML, and News/OB-ML groups. For
every group, the results are shown in the following order from left to right (#units-#epochs): 5-25, 5-50, 5-75, 5-100,
5-125, 10-25, 10-50, 10-75, 10-100, 10-125, 15-25, 15-50, 15-75, 15-100, 15-125, 20-25, 20-50, 20-75, 20-100, 20-125,
25-25, 25-50, 25-75, 25-100, and 25-125. For the sake of clarity, these values are not shown in this figure. The bar
chart is the percentage of tickers with the outstanding performance considering the MDA loss function at the 5%
significance level of the RC compared to the HAR-family of models as the benchmark for every specified ML model.
The darker bar charts are the RC values of primary experiments in Section 5. The RC values can be read from the
left-hand axis. The dashed (solid) line shows the average (median) out-of-sample MDAs of the CHAR model relative
to the ML model across 23 tickers. A value below one indicates improved performance of the ML model, while a value
above one indicates degradation. The values for the dashed and solid lines can be read from the right-hand axis. The
horizontal dashed line represents no improvement.
83


## Page 84

0
20
40
# of units
Full Out-of-Sample Period
0
20
40
# of units
Normal Volatility Days
AAPL
MSFT
INTC
CMCSA
QCOM
CSCO
EBAY
GILD
TXN
AMZN
SBUX
NVDA
MU
AMAT
NTAP
ADBE
XLNX
AMGN
VOD
CTSH
KLAC
PCAR
ADSK
Ticker
0
20
40
# of units
High Volatility Days
0
50
100
# of epochs
# of units
# of epochs
0
50
100
# of epochs
0
50
100
# of epochs
Figure C9: The Best-Performing Hyperparameters (#Units & #Epochs) (MDA)
Notes: There are two sets of four bars for each ticker that correspond to the four groups of ML models, viz.
HAR-ML, News-ML, OB-ML, and News/OB-ML. The first four black bars correspond to their optimal number of
units, while the next four grey bars correspond to their optimal number of epochs. The top, middle, and bottom
figures correspond to the full out-of-sample period, normal volatility days, and high volatility days, respectively,
based on the MDA loss function. The number of units (# of units) can be read from the left axis, and the number
of epochs (# of epochs) can be read from the right axis.
84


## Page 85

0
20
40
60
80
100
Full Out-of-Sample
0.94
0.96
0.98
1.00
1.02
Full Out-of-Sample
HAR
News
OB
News/OB
LSTM
FCNN
LSTM
FCNN
LSTM
FCNN
LSTM
FCNN
MDA (avg)
MDA (med)
0
20
40
60
80
100
Normal Volatility Days
0.88
0.90
0.92
0.94
0.96
0.98
1.00
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
0
5
10
15
20
25
30
35
High Volatility Days
1.00
1.01
1.02
1.03
1.04
1.05
1.06
1.07
High Volatility Days
Reality Check (%)
Diﬀerence
Figure C10: Comparison of LSTM and FCNN Models (MDA)
Notes: The bar chart is the percentage of tickers with the outstanding performance considering the MDA loss function
at the 5% significance level of the RC compared to the HAR-family of models as the benchmark for every specified
model. The first, second, third, and fourth sets of ten bars correspond to the HAR, News, OB, and News/OB groups,
respectively. Within each set, the first five hatched bars represent results from the LSTM model, while the subsequent
five bars represent results from the FCNN model. Each bar within these subsets reflects performance associated with
a specific number of units. The values for the bar chart correspond to the left-hand axis. The dashed (solid) line
shows the average (median) out-of-sample MDAs of the CHAR model relative to the ML model across 23 tickers. A
value below one indicates improved performance of the ML model, while a value above one indicates degradation.
The values for the dashed and solid lines can be read from the right-hand axis. The horizontal dashed line represents
no improvement.
85


## Page 86

0
20
40
60
80
100
Full Out-of-Sample
0.96
0.97
0.98
0.99
1.00
1.01
1.02
1.03
Full Out-of-Sample
HAR
News
OB
News/OB
MDA (avg)
MDA (med)
0
20
40
60
80
100
Normal Volatility Days
0.92
0.94
0.96
0.98
1.00
Normal Volatility Days
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
5
10
15
20
25
0
2
4
6
8
High Volatility Days
1.00
1.01
1.02
1.03
1.04
1.05
1.06
1.07
High Volatility Days
Reality Check (%)
Diﬀerence
Figure C11: ML Models Utilising Early Stopping (MDA)
Notes: The bar chart is the percentage of tickers with the outstanding performance considering the MDA loss function
at the 5% significance level of the RC compared to the HAR-family of models as the benchmark. The results are
presented for each model group: HAR, News, OB, and News/OB, across varying numbers of units, specifically 5, 10,
15, 20, and 25 units. The values for the bar chart can be read from the left-hand axis. The dashed (solid) line shows
the average (median) out-of-sample MDAs of the CHAR model relative to the ML model across 23 tickers. A value
below one indicates improved performance of the ML model, while a value above one indicates degradation. The
values for the dashed and solid lines can be read from the right-hand axis. The horizontal dashed line represents no
improvement.
86


## Page 87

References
Andersen, T. G., T. Bollerslev, and F. X. Diebold (2007). Roughing It Up: Including Jump
Components in the Measurement, Modeling, and Forecasting of Return Volatility. The Review
of Economics and Statistics 89(4), 701–720.
Andersen, T. G., T. Bollerslev, F. X. Diebold, and P. Labys (2001). The Distribution of Realized
Exchange Rate Volatility. Journal of the American Statistical Association 96(453), 42–55.
Andrychowicz, O. M., B. Baker, M. Chociej, R. Jozefowicz, B. McGrew, J. Pachocki, A. Petron,
M. Plappert, G. Powell, A. Ray, et al. (2020). Learning Dexterous In-Hand Manipulation. The
International Journal of Robotics Research 39(1), 3–20.
Audrino, F. and J. Chassot (2025). HARd to Beat: The Overlooked Impact of Rolling Windows
in the Era of Machine Learning. International Journal of Forecasting.
Audrino, F. and S. D. Knaus (2016). Lassoing the HAR Model: A Model Selection Perspective
on Realized Volatility Dynamics. Econometric Reviews 35(8-10), 1485–1521.
Bali, T. G., H. Beckmeyer, M. Moerke, and F. Weigert (2023). Option Return Predictability with
Machine Learning and Big Data. The Review of Financial Studies 36(9), 3548–3602.
Barndorff-Nielsen, O. E., P. R. Hansen, A. Lunde, and N. Shephard (2009). Realized Kernels in
Practice: Trades and Quotes. The Econometrics Journal 12(3), C1–C32.
Barndorff-Nielsen, O. E. and N. Shephard (2001). Non-Gaussian Ornstein–Uhlenbeck-Based Mod-
els and Some of Their Uses in Financial Economics. Journal of the Royal Statistical Society:
Series B (Statistical Methodology) 63(2), 167–241.
Barndorff-Nielsen, O. E. and N. Shephard (2002). Estimating Quadratic Variation Using Realized
Variance. Journal of Applied Econometrics 17(5), 457–477.
Barndorff-Nielsen, O. E. and N. Shephard (2004). Power and Bipower Variation with Stochastic
Volatility and Jumps. Journal of Financial Econometrics 2(1), 1–37.
Bollerslev, T., A. J. Patton, and R. Quaedvlieg (2016). Exploiting the Errors: A Simple Approach
for Improved Volatility Forecasting. Journal of Econometrics 192(1), 1–18.
Branco, R. R., A. Rubesam, and M. Zevallos (2024).
Forecasting Realized Volatility: Does
Anything Beat Linear Models? Journal of Empirical Finance 78, 101524.
87


## Page 88

Bucci, A. (2020). Realized Volatility Forecasting with Neural Networks. Journal of Financial
Econometrics 18(3), 502–531.
Chen, L., M. Pelger, and J. Zhu (2024). Deep Learning in Asset Pricing. Management Sci-
ence 70(2), 714–750.
Chen, T. and C. Guestrin (2016). XGBoost: A Scalable Tree Boosting System. In Proceedings of
the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining,
pp. 785–794.
Christensen, K., M. Siggaard, and B. Veliyev (2023). A Machine Learning Approach to Volatility
Forecasting. Journal of Financial Econometrics 21(5), 1680–1727.
Chronopoulos, I., A. Raftapostolos, and G. Kapetanios (2024). Forecasting Value-at-Risk Using
Deep Neural Network Quantile Regression. Journal of Financial Econometrics 22(3), 636–669.
Corsi, F. (2009). A Simple Approximate Long-Memory Model of Realized Volatility. Journal of
Financial Econometrics 7(2), 174–196.
Corsi, F. and R. Reno (2009). HAR Volatility Modelling with Heterogeneous Leverage and Jumps.
Available at SSRN 1316953.
Diebold, F. and R. Mariano (1995). Comparing Predictive Accuracy. Journal of Business &
Economic Statistics 13(3), 253–263.
Erel, I., L. H. Stern, C. Tan, and M. S. Weisbach (2021). Selecting Directors Using Machine
Learning. The Review of Financial Studies 34(7), 3226–3264.
Fernandes, M., M. C. Medeiros, and M. Scharth (2014). Modeling and Predicting the CBOE
Market Volatility Index. Journal of Banking & Finance 40, 1–10.
Goldberg, Y. (2016). A Primer on Neural Network Models for Natural Language Processing.
Journal of Artificial Intelligence Research 57, 345–420.
Gu, S., B. Kelly, and D. Xiu (2020). Empirical Asset Pricing via Machine Learning. The Review
of Financial Studies 33(5), 2223–2273.
Gu, S., B. Kelly, and D. Xiu (2021). Autoencoder Asset Pricing Models. Journal of Economet-
rics 222(1), 429–450.
88


## Page 89

Hillebrand, E. and M. C. Medeiros (2010).
The Benefits of Bagging for Forecast Models of
Realized Volatility. Econometric Reviews 29(5-6), 571–593.
Hochreiter, S. and J. Schmidhuber (1997). Long Short-Term Memory. Neural Computation 9(8),
1735–1780.
Huang, R. and T. Polak (2011). LOBSTER: Limit Order Book Reconstruction System. Available
at SSRN 1977207.
Jiang, J., B. Kelly, and D. Xiu (2023).
(Re-)Imag(in)ing Price Trends.
The Journal of Fi-
nance 78(6), 3193–3249.
Kalay, A., O. Sade, and A. Wohl (2004). Measuring Stock Illiquidity: An Investigation of the
Demand and Supply Schedules at the TASE. Journal of Financial Economics 74(3), 461–486.
Ke, G., Q. Meng, T. Finley, T. Wang, W. Chen, W. Ma, Q. Ye, and T.-Y. Liu (2017). LightGBM:
A Highly Efficient Gradient Boosting Decision Tree. Advances in Neural Information Processing
Systems 30.
Kercheval, A. N. and Y. Zhang (2015). Modelling High-Frequency Limit Order Book Dynamics
with Support Vector Machines. Quantitative Finance 15(8), 1315–1329.
Kingma, D. P. and J. Ba (2014). Adam: A Method for Stochastic Optimization. arXiv preprint
arXiv:1412.6980.
Li, S. Z. and Y. Tang (2025). Automated Volatility Forecasting. Management Science 71(7),
6248–6274.
Loughran, T. and B. McDonald (2011). When Is a Liability Not a Liability? Textual Analysis,
Dictionaries, and 10-Ks. The Journal of Finance 66(1), 35–65.
Loughran, T. and B. McDonald (2016). Textual Analysis in Accounting and Finance: A Survey.
Journal of Accounting Research 54(4), 1187–1230.
Loughran, T. and B. McDonald (2020). Textual Analysis in Finance. Annual Review of Financial
Economics 12, 357–375.
Lundberg, S. M. and S.-I. Lee (2017). A Unified Approach to Interpreting Model Predictions.
Advances in Neural Information Processing Systems 30.
89


## Page 90

Næs, R. and J. A. Skjeltorp (2006).
Order Book Characteristics and the Volume–Volatility
Relation: Empirical Evidence from a Limit Order Market. Journal of Financial Markets 9(4),
408–432.
Patton, A. J. (2011). Volatility Forecast Comparison Using Imperfect Volatility Proxies. Journal
of Econometrics 160(1), 246–256.
Patton, A. J. and K. Sheppard (2015). Good Volatility, Bad Volatility: Signed Jumps and The
Persistence of Volatility. The Review of Economics and Statistics 97(3), 683–697.
Politis, D. N. and J. P. Romano (1994). The Stationary Bootstrap. Journal of the American
Statistical Association 89(428), 1303–1313.
Poon, S.-H. and C. W. Granger (2003). Forecasting Volatility in Financial Markets: A Review.
Journal of Economic Literature 41(2), 478–539.
Rahimikia, E. and S.-H. Poon (2020). Alternative Data for Realised Volatility Forecasting: Limit
Order Book and News Stories. Available at SSRN 3684040.
Shrikumar, A., P. Greenside, and A. Kundaje (2017). Learning Important Features Through
Propagating Activation Differences. In International Conference on Machine Learning, pp.
3145–3153. PMLR.
Srivastava, N., G. Hinton, A. Krizhevsky, I. Sutskever, and R. Salakhutdinov (2014). Dropout: A
Simple Way to Prevent Neural Networks from Overfitting. The Journal of Machine Learning
Research 15(1), 1929–1958.
Vaswani, A., N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez,  L. Kaiser, and I. Polo-
sukhin (2017). Attention is All You Need. Advances in Neural Information Processing Sys-
tems 30.
Vinyals, O., I. Babuschkin, W. M. Czarnecki, M. Mathieu, A. Dudzik, J. Chung, D. H. Choi,
R. Powell, T. Ewalds, P. Georgiev, et al. (2019). Grandmaster Level in StarCraft II Using
Multi-Agent Reinforcement Learning. Nature 575(7782), 350–354.
West, K. D. (1996). Asymptotic Inference About Predictive Ability. Econometrica, 1067–1084.
White, H. (2000). A Reality Check for Data Snooping. Econometrica 68(5), 1097–1126.
90


## Page 91

Zhu, H., L. Bai, L. He, and Z. Liu (2023). Forecasting Realized Volatility with Machine Learning:
Panel Data Perspective. Journal of Empirical Finance 73, 251–271.
91


Contents
I Introduction 1
1 Introduction To Advanced Algorithmic Trading . . . . . . . . . . . . . . . . . 3
1.1 Why Time Series Analysis, Bayesian Statistics and Machine Learning? . . . . . . 3
1.1.1 Bayesian Statistics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.1.2 Time Series Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.1.3 Machine Learning . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1.2 How Is The Book Laid Out?. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
1.3 Required Technical Background . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
1.3.1 Mathematics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
1.3.2 Programming . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
1.4 How Does This Di(cid:27)er From "Successful Algorithmic Trading"? . . . . . . . . . . 6
1.5 Software Installation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
1.5.1 Installing Python . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
1.5.2 Installing R . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
1.6 Backtesting Software Options . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
1.6.1 Alternatives . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
1.7 What Do You Get In The Rough Cut Version? . . . . . . . . . . . . . . . . . . . 8
II Bayesian Statistics 9
2 Introduction to Bayesian Statistics . . . . . . . . . . . . . . . . . . . . . . . . . 11
2.1 What is Bayesian Statistics? . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
2.1.1 Frequentist vs Bayesian Examples . . . . . . . . . . . . . . . . . . . . . . 12
2.2 Applying Bayes’ Rule for Bayesian Inference . . . . . . . . . . . . . . . . . . . . . 14
2.3 Coin-Flipping Example. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
3 Bayesian Inference of a Binomial Proportion . . . . . . . . . . . . . . . . . . . 19
3.1 The Bayesian Approach . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
3.2 Assumptions of the Approach . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
3.3 Recalling Bayes’ Rule . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
3.4 The Likelihood Function . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
3.4.1 Bernoulli Distribution . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
3.4.2 Bernoulli Likelihood Function . . . . . . . . . . . . . . . . . . . . . . . . . 22
3.4.3 Multiple Flips of the Coin . . . . . . . . . . . . . . . . . . . . . . . . . . . 22
3.5 Quantifying our Prior Beliefs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22
3.5.1 Beta Distribution . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23
3.5.2 Why Is A Beta Prior Conjugate to the Bernoulli Likelihood? . . . . . . . 25
3.5.3 Multiple Ways to Specify a Beta Prior . . . . . . . . . . . . . . . . . . . . 25
3.6 Using Bayes’ Rule to Calculate a Posterior. . . . . . . . . . . . . . . . . . . . . . 26
4 Markov Chain Monte Carlo . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
4.1 Bayesian Inference Goals . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
4.2 Why Markov Chain Monte Carlo? . . . . . . . . . . . . . . . . . . . . . . . . . . 29
4.2.1 Markov Chain Monte Carlo Algorithms . . . . . . . . . . . . . . . . . . . 30
4.3 The Metropolis Algorithm . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 30
1

2
4.4 Introducing PyMC3 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31
4.5 Inferring a Binomial Proportion with Markov Chain Monte Carlo . . . . . . . . . 32
4.5.1 Inferring a Binonial Proportion with Conjugate Priors Recap . . . . . . . 32
4.5.2 Inferring a Binonial Proportion with PyMC3 . . . . . . . . . . . . . . . . 32
4.6 Next Steps . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 37
4.7 Bibliographic Note . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 38
5 Bayesian Linear Regression . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39
5.1 Frequentist Linear Regression . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39
5.2 Bayesian Linear Regression . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 40
5.3 Bayesian Linear Regression with PyMC3 . . . . . . . . . . . . . . . . . . . . . . . 41
5.3.1 What are Generalised Linear Models? . . . . . . . . . . . . . . . . . . . . 41
5.3.2 Simulating Data and Fitting the Model with PyMC3 . . . . . . . . . . . . 41
5.4 Next Steps . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 45
5.5 Bibliographic Note . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 46
5.6 Full Code . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 46
III Time Series Analysis 49
6 Introduction to Time Series Analysis . . . . . . . . . . . . . . . . . . . . . . . . 51
6.1 What is Time Series Analysis? . . . . . . . . . . . . . . . . . . . . . . . . . . . . 51
6.2 How Can We Apply Time Series Analysis in Quantitative Finance? . . . . . . . . 52
6.3 Time Series Analysis Software . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 52
6.4 Time Series Analysis Roadmap . . . . . . . . . . . . . . . . . . . . . . . . . . . . 52
6.5 How Does This Relate to Other Statistical Tools? . . . . . . . . . . . . . . . . . . 53
7 Serial Correlation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 55
7.1 Expectation, Variance and Covariance . . . . . . . . . . . . . . . . . . . . . . . . 55
7.1.1 Example: Sample Covariance in R . . . . . . . . . . . . . . . . . . . . . . 56
7.2 Correlation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 57
7.2.1 Example: Sample Correlation in R . . . . . . . . . . . . . . . . . . . . . . 58
7.3 Stationarity in Time Series . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 58
7.4 Serial Correlation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 59
7.5 The Correlogram . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 60
7.5.1 Example 1 - Fixed Linear Trend . . . . . . . . . . . . . . . . . . . . . . . 61
7.5.2 Example 2 - Repeated Sequence . . . . . . . . . . . . . . . . . . . . . . . 61
7.6 Next Steps . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 61
8 Random Walks and White Noise Models . . . . . . . . . . . . . . . . . . . . . . 65
8.1 Time Series Modelling Process . . . . . . . . . . . . . . . . . . . . . . . . . . . . 65
8.2 Backward Shift and Di(cid:27)erence Operators . . . . . . . . . . . . . . . . . . . . . . 66
8.3 White Noise . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 66
8.3.1 Second-Order Properties . . . . . . . . . . . . . . . . . . . . . . . . . . . . 67
8.3.2 Correlogram . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 67
8.4 Random Walk. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 68
8.4.1 Second-Order Properties . . . . . . . . . . . . . . . . . . . . . . . . . . . . 68
8.4.2 Correlogram . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 69
8.4.3 Fitting Random Walk Models to Financial Data . . . . . . . . . . . . . . 69
9 Autoregressive Moving Average Models . . . . . . . . . . . . . . . . . . . . . . 75
9.1 How Will We Proceed?. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 75
9.2 Strictly Stationary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 76
9.3 Akaike Information Criterion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 76
9.4 Autoregressive (AR) Models of order p . . . . . . . . . . . . . . . . . . . . . . . . 77
9.4.1 Rationale . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 77
9.4.2 Stationarity for Autoregressive Processes . . . . . . . . . . . . . . . . . . 78

3
9.4.3 Second Order Properties . . . . . . . . . . . . . . . . . . . . . . . . . . . . 78
9.4.4 Simulations and Correlograms. . . . . . . . . . . . . . . . . . . . . . . . . 79
9.4.5 Financial Data . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 82
9.5 Moving Average (MA) Models of order q . . . . . . . . . . . . . . . . . . . . . . . 87
9.5.1 Rationale . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 88
9.5.2 De(cid:28)nition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 88
9.5.3 Second Order Properties . . . . . . . . . . . . . . . . . . . . . . . . . . . . 88
9.5.4 Simulations and Correlograms. . . . . . . . . . . . . . . . . . . . . . . . . 89
9.5.5 Financial Data . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 93
9.5.6 Next Steps . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 98
9.6 Autogressive Moving Average (ARMA) Models of order p, q . . . . . . . . . . . . 99
9.6.1 Bayesian Information Criterion . . . . . . . . . . . . . . . . . . . . . . . . 99
9.6.2 Ljung-Box Test . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 99
9.6.3 Rationale . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 100
9.6.4 De(cid:28)nition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 100
9.6.5 Simulations and Correlograms. . . . . . . . . . . . . . . . . . . . . . . . . 100
9.6.6 Choosing the Best ARMA(p,q) Model . . . . . . . . . . . . . . . . . . . . 104
9.6.7 Financial Data . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 106
9.7 Next Steps . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 107
10 AutoregressiveIntegratedMovingAverageandConditionalHeteroskedastic
Models . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .109
10.1 Quick Recap . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 109
10.2 Autoregressive Integrated Moving Average (ARIMA) Models of order p, d, q . . 110
10.2.1 Rationale . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 110
10.2.2 De(cid:28)nitions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 110
10.2.3 Simulation, Correlogram and Model Fitting . . . . . . . . . . . . . . . . . 111
10.2.4 Financial Data and Prediction . . . . . . . . . . . . . . . . . . . . . . . . 113
10.2.5 Next Steps . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 117
10.3 Volatility . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 117
10.4 Conditional Heteroskedasticity . . . . . . . . . . . . . . . . . . . . . . . . . . . . 117
10.5 Autoregressive Conditional Heteroskedastic Models . . . . . . . . . . . . . . . . . 118
10.5.1 ARCH De(cid:28)nition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 118
10.5.2 Why Does This Model Volatility?. . . . . . . . . . . . . . . . . . . . . . . 118
10.5.3 When Is It Appropriate To Apply ARCH(1)? . . . . . . . . . . . . . . . . 119
10.5.4 ARCH(p) Models . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 119
10.6 Generalised Autoregressive Conditional Heteroskedastic Models . . . . . . . . . . 119
10.6.1 GARCH De(cid:28)nition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 119
10.6.2 Simulations, Correlograms and Model Fittings . . . . . . . . . . . . . . . 120
10.6.3 Financial Data . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 122
10.7 Next Steps . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 124
11 State Space Models and the Kalman Filter . . . . . . . . . . . . . . . . . . . .127
11.1 Linear State-Space Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 128
11.2 The Kalman Filter . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 129
11.2.1 A Bayesian Approach . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 129
11.2.2 Prediction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 130
IV Statistical Machine Learning 133
12 Model Selection and Cross-Validation . . . . . . . . . . . . . . . . . . . . . . .135
12.1 Bias-Variance Trade-O(cid:27) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 135
12.1.1 Machine Learning Models . . . . . . . . . . . . . . . . . . . . . . . . . . . 135
12.1.2 Model Selection . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 136
12.1.3 The Bias-Variance Tradeo(cid:27) . . . . . . . . . . . . . . . . . . . . . . . . . . 137

4
12.2 Cross-Validation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 140
12.2.1 Overview of Cross-Validation . . . . . . . . . . . . . . . . . . . . . . . . . 140
12.2.2 Forecasting Example . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 141
12.2.3 Validation Set Approach . . . . . . . . . . . . . . . . . . . . . . . . . . . . 142
12.2.4 k-Fold Cross Validation . . . . . . . . . . . . . . . . . . . . . . . . . . . . 142
12.2.5 Python Implementation . . . . . . . . . . . . . . . . . . . . . . . . . . . . 143
12.2.6 k-Fold Cross Validation . . . . . . . . . . . . . . . . . . . . . . . . . . . . 147
12.2.7 Full Python Code . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 149
13 Kernel Methods and SVMs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .157
13.1 Support Vector Machines . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 157
13.1.1 Motivation for Support Vector Machines . . . . . . . . . . . . . . . . . . . 157
13.1.2 Advantages and Disadvantages of SVMs . . . . . . . . . . . . . . . . . . . 158
13.1.3 Linear Separating Hyperplanes . . . . . . . . . . . . . . . . . . . . . . . . 159
13.1.4 Classi(cid:28)cation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 160
13.1.5 Deriving the Classi(cid:28)er . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 161
13.1.6 Constructing the Maximal Margin Classi(cid:28)er . . . . . . . . . . . . . . . . . 162
13.1.7 Support Vector Classi(cid:28)ers . . . . . . . . . . . . . . . . . . . . . . . . . . . 163
13.1.8 Support Vector Machines . . . . . . . . . . . . . . . . . . . . . . . . . . . 165
13.2 Document Classi(cid:28)cation using Support Vector Machines . . . . . . . . . . . . . . 168
13.2.1 Overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 168
13.2.2 Supervised Document Classi(cid:28)cation . . . . . . . . . . . . . . . . . . . . . 169
13.3 Preparing a Dataset for Classi(cid:28)cation . . . . . . . . . . . . . . . . . . . . . . . . 169
13.3.1 Vectorisation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 178
13.3.2 Term-Frequency Inverse Document-Frequency . . . . . . . . . . . . . . . . 179
13.4 Training the Support Vector Machine . . . . . . . . . . . . . . . . . . . . . . . . 180
13.4.1 Performance Metrics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 181
13.5 Full Code Implementation in Python 3.4.x . . . . . . . . . . . . . . . . . . . . . . 183
13.5.1 Biblographic Notes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 187
V Quantitative Trading Strategies 189
14 Introduction to QSTrader . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .191
14.1 Backtesting vs Live Trading . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 191
14.2 Design Considerations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 192
14.2.1 Quantitative Trading Considerations . . . . . . . . . . . . . . . . . . . . . 192
14.3 Installation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 193
15 ARIMA+GARCH Trading Strategy on Stock Market Indexes Using R . . .195
15.1 Strategy Overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 195
15.2 Strategy Implementation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 195
15.3 Strategy Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 198
15.4 Full Code . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 201

Limit of Liability/Disclaimer of
Warranty
Whiletheauthorhasusedtheirbeste(cid:27)ortsinpreparingthisbook,theymakenorepresentations
or warranties with the respect to the accuracy or completeness of the contents of this book and
speci(cid:28)callydisclaimanyimpliedwarrantiesofmerchantabilityor(cid:28)tnessforaparticularpurpose.
It is sold on the understanding that the author is not engaged in rendering professional services
and the author shall not be liable for damages arising herefrom. If professional advice or other
expert assistance is required, the services of a competent professional should be sought.
i

ii

Part I
Introduction
1

| Chapter      | 1   |     |             |     |     |     |
| ------------ | --- | --- | ----------- | --- | --- | --- |
| Introduction |     |     | To Advanced |     |     |     |
| Algorithmic  |     |     | Trading     |     |     |     |
Inthisintroductorychapterwewillconsiderwhywewanttoadoptafullystatisticalapproachto
quantitativetradinganddiscussBayesianStatistics,TimeSeriesAnalysisandMachineLearning.
In addition we will look at what the book contains, the technical background you will need
to get the most out of the book, why it di(cid:27)ers from the previous book Successful Algorithmic
Trading and choices of backtesting software for the strategies we will discuss at the end of the
book.
| 1.1 Why | Time      | Series | Analysis, | Bayesian | Statistics | and Ma- |
| ------- | --------- | ------ | --------- | -------- | ---------- | ------- |
| chine   | Learning? |        |           |          |            |         |
In the last few years there has been a signi(cid:28)cant increase in the availability of software for
carrying out statistical analysis at large scales, the so called "big data" era.
Much of this software is completely free, open source, extremely well tested and straightfor-
ward to use. This coupled to the availability of (cid:28)nancial data, as provided by services such as
YahooFinance,GoogleFinance,QuandlandIQFeed,hasleadtoasharpincreaseinindividuals
| learning | how to become | a quantitative | trader. |     |     |     |
| -------- | ------------- | -------------- | ------- | --- | --- | --- |
However, many of these individuals never get past learning basic "technical analysis" and so
avoid important topics such as risk management, portfolio construction and algorithmic execu-
tion. In addition they often neglect more e(cid:27)ective means of generating alpha, such as can be
| provided | via detailed statistical |     | analysis. |     |     |     |
| -------- | ------------------------ | --- | --------- | --- | --- | --- |
InthisbookIwanttoprovidea"nextstep"forthosewhohavealreadybeguntheiralgorithmic
trading career, or are looking to try more advanced methods. In particular, we will be making
use of techniques that are currently in deployment at some of the large quantitative hedge funds
| and asset | management | (cid:28)rms. |     |     |     |     |
| --------- | ---------- | ------------ | --- | --- | --- | --- |
Ourmainareaofstudywillbethatofrigourous statistical analysis. Thismaysoundlike
a dry topic, but I can assure you that not only is it extremely interesting when applied to real
world data, but it will provide you with a solid "mental framework" for how to think about all
| of your future | trading | methods | and approaches. |     |     |     |
| -------------- | ------- | ------- | --------------- | --- | --- | --- |
Obviously, statistical analysis is a huge (cid:28)eld of academic interest. Trying to distill the topics
important for quantitative trading is di(cid:30)cult. However, there are three main areas that we will
| concentrate | on in this | book: |     |     |     |     |
| ----------- | ---------- | ----- | --- | --- | --- | --- |
(cid:136)
| Bayesian          | Statistics      |           |                           |                |     |     |
| ----------------- | --------------- | --------- | ------------------------- | -------------- | --- | --- |
| (cid:136) Time    | Series Analysis |           |                           |                |     |     |
| (cid:136) Machine | Learning        |           |                           |                |     |     |
| Each              | of these three  | areas has | its place in quantitative | (cid:28)nance. |     |     |
3

4
1.1.1 Bayesian Statistics
Bayesian Statistics is an alternative way of thinking about probability. The more traditional
"frequentist" approach considers probabilities as the end result of many trials, for instance, the
fairness of a coin being (cid:29)ipped many times. Bayesian Statistics takes a di(cid:27)erent approach and
instead considers probability as a measure of belief. That is, our own opinions are used to create
probability distributions from which the fairness of the coin might be based on.
Whilethismaysoundhighlysubjective, itisoftenanextremelye(cid:27)ectivemethodinpractice.
AsnewdataarriveswecanupdateourbeliefsinarationalmannerusingthefamousBayes’Rule.
Bayesian Statistics has found uses in many (cid:28)elds, including engineering reliability, searching for
lost nuclear submarines and controlling spacecraft orientation. However, it is also extremely
applicable to quantitative trading problems.
Bayesian Inference is the application of Bayesian Statistics to making inference and predic-
tionsaboutdata. Inourcase,wewillbestudying(cid:28)nancialassetpricesinordertopredictfuture
values or understand why they change. The Bayesian framework provides us with a modern,
sophisticated toolkit with which to carry this out.
Time Series Analysis and Machine Learning make heavy use of Bayesian Inference for the
design of some of their algorithms. Hence it is essential that we understand the basics of how
Bayesian Statistics is carried out, particularly in relation to the Markov Chain Monte Carlo
method, which will we discuss at length in the book section on Bayesian Statistics.
To carry out Bayesian Inference in this book we will use a "probabilistic programming" tool,
written in Python, called PyMC.
1.1.2 Time Series Analysis
Time Series Analysis provides a set of workhorse techniques for analysing (cid:28)nancial time series.
Most professional quants will begin their analysis of (cid:28)nancial data using basic time series meth-
ods. Bystudyingthetoolsintimeseriesanalysiswecanmakeelementaryassessmentsof(cid:28)nancial
asset behaviour and use this to consider more advanced methods, in a structured way.
The main idea in Time Series Analysis is that of serial correlation. Brie(cid:29)y, in terms of
daily trading prices, serial correlation describes to us how much of today’s asset prices are
correlated to previous days’ prices. Understanding the structure of this correlation helps us to
build sophisticated models that can help us interpret the data and predict future values.
Time Series Analysis can be thought of as a much more rigourous approach to understand-
ing the behaviour of (cid:28)nancial asset prices than "technical analysis". While technical analysis
has basic "indicators" for trends, mean reverting behaviour and volatility determination, time
series analysis brings with it the full power of statistical inference, including hypothesis testing,
goodness-of-(cid:28)ttestsandmodelselection,allofwhichservetohelpusrigourouslydetermineasset
behaviour and thus eventually increase our pro(cid:28)tability of our strategies. We can understand
trends, seasonality, long-memory e(cid:27)ects and volatility clustering in much more detail.
To carry out Time Series Analysis in this book we will use the R statistical programming
environment, along with its many external libraries.
1.1.3 Machine Learning
MachineLearningisanothersubsetofstatisticallearningthatappliesmodernstatisticalmodels,
across huge data sets, whether they have a temporal component or not. Machine Learning is
part of the broader "data science" and quant ecosystem.
Machine Learning is generally subdivided into two separate categories, namely supervised
learning and unsupervised learning. The former uses "training data" to train an algorithm to
detect patterns in data. The latter has no concept of training (hence the "unsupervised") and
algorithms solely act on the data without being penalised or rewarded for correct answers.
WewillbeusingmachinelearningtechniquessuchasSupportVectorMachinesandRandom
Forests to (cid:28)nd more complicated relationships between di(cid:27)ering sets of (cid:28)nancial data. If these
patterns can be successfully validated then we can use them to infer structure in the data and
make predictions about future data points. Such tools are highly useful in alpha generation and
risk management.

5
To carry out Machine Learning in this book we will use the Python scikit-learn library, as
well as pandas, for data analysis.
1.2 How Is The Book Laid Out?
The book is broadly laid out in four sections. The (cid:28)rst three are theoretical and teach you the
basics through to intermediate usage of Bayesian Statistics, Time Series Analysis and Machine
Learning. The fourth section applies all of the previous theory to real trading strategies.
The book begins with a discussion on the Bayesian philosophy of statistics and uses the
binomial model as a simple example with which to apply Bayesian concepts such as conjugate
priors and posterior sampling via Markov Chain Monte Carlo.
ItthenexploresBayesianstatisticsasrelatedtoquantitative(cid:28)nance,discussingkeyexamples
suchasswitch-pointanalysis(forregimedetection)andstochasticvolatility. Finally,weconclude
by discussing the burgeoning area of Bayesian Econometrics.
In Time Series Analysis we begin by discussing the concept of Serial Correlation, before
applyingittosimplemodelssuchasWhiteNoiseandtheRandomWalk. Fromthesetwomodels
we can build up more sophisticated approaches to explaining Serial Correlation, culminating in
the Autoregressive Integrated Moving Average (ARIMA) family of models.
We then move on to consider volatility clustering, or conditional heteroskedasticity, and de-
(cid:28)ne and utilise the Generalised Autoregressive Conditional Heteroskedastic (GARCH) family of
models.
Subsequent to ARIMA and GARCH we will consider long-memory e(cid:27)ects in (cid:28)nancial time
series, take a deeper look at cointegration (for statistical arbitrage) and consider approaches to
state space models including Hidden Markov Models and Kalman Filters.
All the while we will be applying these time series models to current (cid:28)nancial data and
assessing how they perform in terms of inference and prediction.
In the Machine Learning section we will begin with a more rigourous de(cid:28)nition of supervised
andunsupervisedlearning,andthendiscussthenotationandmethodologyofstatisticalmachine
learning. We will use the humble linear regression as our (cid:28)rst model, swiftly moving on to linear
classi(cid:28)cationwithlogisticregression,lineardiscriminantanalysisandtheNaiveBayesClassi(cid:28)er.
Wewillthenbereadytoconsiderthemoreadvancednon-linearmethodssuchasSupportVec-
tor Machines and Random Forests. We will consider unsupervised techniques such as Principal
Components Analysis, k-Means Clustering and Non-Negative Matrix Factorisation.
We will apply these techniques to asset price prediction, natural language processing and
subsequently sentiment analysis.
Finallywewilldiscusswheretogofromhere. Thereareplentyofacademictopicsofinterestto
review,includingNon-LinearTimeSeriesMethods,BayesianNonparametricsandDeepLearning
using Neural Networks. However, these topics will have to wait for later books!
1.3 Required Technical Background
Advanced Algorithmic Trading is a de(cid:28)nite step up in complexity from Successful Algorithmic
Trading. Unfortunately it is di(cid:30)cult to carry out any statistical inference without utilising
mathematics and programming.
1.3.1 Mathematics
To get the most out of this book it will be necessary to have taken introductory undergrad-
uate classes in Mathematical Foundations, Calculus, Linear Algebra and Probability,
which are often taught in university degrees of Mathematics, Physics, Engineering, Economics,
Computer Science or similar.
Thankfully, you do not have to had a university education in order to use this book. There
are plenty of fantastic resources for learning these topics on the internet. I prefer:
(cid:136)
Khan Academy - https://www.khanacademy.org

6
(cid:136)
| MIT                | Open Courseware            |     | - http://ocw.mit.edu/index.htm |     |     |     |
| ------------------ | -------------------------- | --- | ------------------------------ | --- | --- | --- |
| (cid:136) Coursera | - https://www.coursera.org |     |                                |     |     |     |
| (cid:136) Udemy    | - https://www.udemy.com    |     |                                |     |     |     |
However, Bayesian Statistics, Time Series Analysis and Machine Learning are quantitative
subjects. There is no avoiding the fact that we will be using some intermediate mathematics to
| quantify | our ideas. |     |     |     |     |     |
| -------- | ---------- | --- | --- | --- | --- | --- |
I recommend the following courses for helping you get up to scratch with your mathematics:
(cid:136) Linear Algebra by Gilbert Strang - http://ocw.mit.edu/courses/mathematics/18-06sc-
linear-algebra-fall-2011/index.htm
(cid:136)
SingleVariableCalculusbyDavidJerison-http://ocw.mit.edu/courses/mathematics/18-
01-single-variable-calculus-fall-2006
(cid:136)
MultivariableCalculusbyDenisAuroux-http://ocw.mit.edu/courses/mathematics/18-
02-multivariable-calculus-fall-2007
(cid:136) Probability by Santosh Venkatesh - https://www.coursera.org/course/probability
| 1.3.2 | Programming |     |     |     |     |     |
| ----- | ----------- | --- | --- | --- | --- | --- |
Since this book is fundamentally about programming quantitative trading strategies, it will be
| necessary | to have some | exposure | to programming | languages. |     |     |
| --------- | ------------ | -------- | -------------- | ---------- | --- | --- |
While it is not necessary to be an expert programmer or software developer, it is helpful to
| have used | a language | similar | to C++, C#, | Java, Python, | R or MatLab. |     |
| --------- | ---------- | ------- | ----------- | ------------- | ------------ | --- |
Many of you will likely have programmed in VB Script or VB.NET, through Excel. I would
strongly recommend taking some introductory Python and R programming courses if this is the
case as it will teach you about deeper programming topics that will be utilised in this book.
| Here | are some useful | courses: |     |     |     |     |
| ---- | --------------- | -------- | --- | --- | --- | --- |
(cid:136)
Programming for Everybody - https://www.coursera.org/learn/python
(cid:136)
| R   | Programming | - https://www.coursera.org/course/rprog |              |      |             |             |
| --- | ----------- | --------------------------------------- | ------------ | ---- | ----------- | ----------- |
| 1.4 | How Does    | This                                    | Di(cid:27)er | From | "Successful | Algorithmic |
Trading"?
SuccessfulAlgorithmicTrading waswrittenprimarilytohelpreadersthinkinrigourousquantita-
tive terms about their trading. In introduces the concepts of hypothesis testing and backtesting
trading strategies. It also outlined the available software that can be used to build backtesting
systems.
Itdiscussesthemeansofstoring(cid:28)nancialdata,measuringquantitativestrategyperformance,
howtoassessriskinquantitativestrategiesandhowtooptimisestrategyperformance. Finally,it
providesatemplateevent-drivenbacktestingengineonwhichtobasefurther,moresophisticated,
trading systems.
It is not a book that provides many trading strategies. The emphasis is primarily on how to
| think in | a quantitative | fashion | and how | to get started. |     |     |
| -------- | -------------- | ------- | ------- | --------------- | --- | --- |
Advanced Algorithmic Trading has a di(cid:27)erent focus. In this book the main topics are time
series,machinelearningandBayesianstats,asappliedtorigourousquantitativetradingstrategies
| across multiple | asset | classes. |     |     |     |     |
| --------------- | ----- | -------- | --- | --- | --- | --- |
Hence this book is largely theoretical for the (cid:28)rst three sections and then highly practical for
the fourth, where we discuss the implementation of actual trading strategies.
Ihaveaddedfarmorestrategiestothisbookthaninthepreviousversionandthisshouldgive
you a solid idea in how to continue researching and improving your own strategies and trading
ideas.

7
Thisbookisnot abookthatcoversextensionsoftheevent-drivenbacktester,nordoesitdwell
on software-speci(cid:28)c testing methodology or how to build an institutional-grade infrastructure
system. It is primarily about quantitative trading strategies and how to carry out research into
their pro(cid:28)tability.
| 1.5 | Software |     | Installation |     |     |     |
| --- | -------- | --- | ------------ | --- | --- | --- |
Overthelastfewyearsithasbecomesigni(cid:28)cantlyeasiertogetbothPythonandRenvironments
installed on Windows, Mac OS X and Linux. In this section I’ll describe how to easily install
| Python | and R.     |     |        |     |     |     |
| ------ | ---------- | --- | ------ | --- | --- | --- |
| 1.5.1  | Installing |     | Python |     |     |     |
In order to follow the code for the Bayesian Statistics and Machine Learning chapters you will
| need to | install | a Python | environment. |     |     |     |
| ------- | ------- | -------- | ------------ | --- | --- | --- |
Possibly the easiest way to achieve this is to download and install the free Anaconda distri-
bution from Continuum Analytics at: https://www.continuum.io/downloads
Theinstallationinstructionsareprovidedatthelinkaboveandcomewithallofthenecessary
| libraries | you need | to  | get going | with | the code in | this book. |
| --------- | -------- | --- | --------- | ---- | ----------- | ---------- |
OnceinstalledyouwillhaveaccesstotheSpyderIntegratedDevelopmentEnvironment(IDE),
which provides a Python syntax-highlighting text editor, an IPython console for interactive
work(cid:29)ow and visualisation, and an object/variable explorer for helpful debugging.
All of the code in the Python sections of this book has been designed to be run using Ana-
conda/Spyder for both Python 2.7.x and 3.4.x+, but will also happily work in "vanilla" Python
| virtual environments, |     |     | once the | necessary | libraries | have been installed. |
| --------------------- | --- | --- | -------- | --------- | --------- | -------------------- |
IfyouhaveanyquestionsaboutPythoninstallation,pleaseemailmeatmike@quantstart.com.
| 1.5.2 | Installing |     | R   |     |     |     |
| ----- | ---------- | --- | --- | --- | --- | --- |
R is a little bit tricker to install than Anaconda, but not massively so. I make use of an IDE
for R, known as R Studio. This provides a similar interface to Anaconda, in that you get an R
syntax-highlighting console and visualisation tools all in the same document interface.
R Studio requires R itself, so you must (cid:28)rst download R before using R Studio. This can be
done for Windows, Mac OS X or Linux from the following link: https://cran.rstudio.com/
You’llwanttoselectthepre-compiledbinaryfromthetopofthepagethat(cid:28)tsyourparticular
| operating | system. |     |     |     |     |     |
| --------- | ------- | --- | --- | --- | --- | --- |
Once you have successfully installed R, the next step (if desired!) is to download R Studio:
https://www.rstudio.com/products/rstudio/download/
Onceagain,you’llneedtopicktheversionforyourparticularplatformandoperatingsystem
type(32/64-bit). Youneedtoselectoneofthelinksunder"InstallersforSupportedPlatforms".
All of the code in the R sections of this book has been designed to be run using "vanilla" R
| and/or R | Studio. |     |     |     |     |     |
| -------- | ------- | --- | --- | --- | --- | --- |
If you have any questions about R installation, please email me at mike@quantstart.com.
| 1.6 | Backtesting |     |     | Software | Options |     |
| --- | ----------- | --- | --- | -------- | ------- | --- |
These days, there are a myriad of options for carrying out backtests and new software (both
| open source | and | proprietary) |     | appears | every month. |     |
| ----------- | --- | ------------ | --- | ------- | ------------ | --- |
Ihavedecidedtoexplainthestrategiesinsimpletermsandtoconcentratepredominantlyon
themathematicaltechniques. Wewillmakeuseofvectorised (thatis, nonevent-driven)systems
| purely for | reasons | of  | speed | and ease | of implementation. |     |
| ---------- | ------- | --- | ----- | -------- | ------------------ | --- |
Python, via the pandas library, and R, both allow straightforward vectorised backtesting,
which can give us a good (cid:28)rst-order approximation to how well a strategy is likely to do in
production.

8
Hence all performance (cid:28)gures will be derived on the basis of these vectorised backtests and
we will discuss how much of an impact transaction costs are likely to have on performance.
| 1.6.1 | Alternatives |     |     |     |     |     |     |
| ----- | ------------ | --- | --- | --- | --- | --- | --- |
There are many alternative backtesting environments available and I strongly encourage you
to code up these strategies in more realistic environments if you wish to trade them in a live
| environment. |     | In particular, | you | could consider: |     |     |     |
| ------------ | --- | -------------- | --- | --------------- | --- | --- | --- |
(cid:136) QSForex-Myownopen-sourcehigh-frequencyevent-drivenbacktesterfortheForexmarket
| using | the | OANDA | brokerage: | https://www.quantstart.com/qsforex |     |     |     |
| ----- | --- | ----- | ---------- | ---------------------------------- | --- | --- | --- |
(cid:136)
Quantopian - A well-regarded web-based backtesting and trading engine for equities mar-
| kets: | https://www.quantopian.com |     |     |     |     |     |     |
| ----- | -------------------------- | --- | --- | --- | --- | --- | --- |
(cid:136)
Zipline - An open source backtesting library that powers the Quantopian web-based back-
| tester: | https://github.com/quantopian/zipline |     |     |     |        |       |              |
| ------- | ------------------------------------- | --- | --- | --- | ------ | ----- | ------------ |
| 1.7     | What                                  | Do  | You | Get | In The | Rough | Cut Version? |
Firstly, I’d like to thank you for pre-ordering the book in its ’rough cut’ state. It is immensely
valuable to me - and subsequently current and future readers - to have a continual process of
feedback while the book is being (cid:28)nished. For C++ For Quantitative Finance and Successful
Algorithmic Trading Iwasabletoincorporatemanysuggestionsthatcamedirectlyfromreaders
| of the site | and | the books. |     |     |     |     |     |
| ----------- | --- | ---------- | --- | --- | --- | --- | --- |
Since this is a pre-order ’rough cut’ release of Advanced Algorithmic Trading, not all of the
topics mentioned in the website ebook page will be available at this point in time. However,
the book is continually being written and so as new content is produced it will be added to the
| ’rough cut’, | prior | to its | full release | early | in 2016. |     |     |
| ------------ | ----- | ------ | ------------ | ----- | -------- | --- | --- |
I have endeavoured to make sure that the Time Series Analysis section is nearly complete.
It currently covers White Noise, Random Walks, ARMA, ARIMA, GARCH and State-Space
Models. It is currently not covering Multivariate Models, Cointegration, Long-Memory E(cid:27)ects
or Market Microstructure. However, the material covered up to the GARCH model already
provides a very useful introduction to Time Series Analysis for those who have not considered it
| before. | The remaining |     | sections | will be | added | in later releases. |     |
| ------- | ------------- | --- | -------- | ------- | ----- | ------------------ | --- |
The Bayesian Statistics section currently contains discussion on the basics of Bayesian Infer-
enceandtheanalyticalapproachtoinferenceonbinomialproportions. Thisissu(cid:30)cientmaterial
necessary to understand the later material on time series. It is currently not covering Markov
Chain Monte Carlo techniques, Switch-Point Analysis, Stochastic Volatility or further Bayesian
| Econometric | tools. | These | will be | added | in later | releases. |     |
| ----------- | ------ | ----- | ------- | ----- | -------- | --------- | --- |
The Machine Learning section currently discusses two of the major issues in Supervised
Learning, namely the Bias-Variance Tradeo(cid:27) and k-Fold Cross-Validation. It also discusses
our(cid:28)rstadvancedmachinelearningtechnique,namelytheSupportVectorMachine. Itcurrently
doesnotcoverabroadintroductiontoSupervisedandUnsupervisedLearning,LinearRegression,
Linear Classi(cid:28)cation, Kernel Density Estimation, Tree-Based Methods, Unsupervised Learning
| and Natural | Language |     | Processing. | These | will | be added in | later releases. |
| ----------- | -------- | --- | ----------- | ----- | ---- | ----------- | --------------- |
TheQuantitativeTradingStrategiessectioncurrentlyonlyhasastrategybasedprimarilyon
the material from the Time Series section, namely the combined ARIMA+GARCH predictive
model. It currently does not cover High Frequency Bid-Ask Spread Prediction, Asset Returns
Forecasting using Machine Learning techniques, Kalman Filters for Pairs Trading, Volatility
Forecasting or Sentiment Analysis. These strategies, and more, will be added in later releases.
Ifthereareanytopicsthatyouthinkwouldbeparticularlysuitableforthebook,thenplease
email me at mike@quantstart.com and I’ll do my best to try and incorporate them prior to the
(cid:28)nal release.

Part II
Bayesian Statistics
9

Chapter 2
Introduction to Bayesian Statistics
The (cid:28)rst part of Advanced Algorithmic Trading is concerned with a detailed look at Bayesian
Statistics. As I mentioned in the introduction, Bayesian methods underpin many of the tech-
niques in Time Series Analysis and Machine Learning, so it is essential that we gain an un-
derstanding of the "philosophy" of the Bayesian approach and how to apply it to real world
quantitative (cid:28)nance problems.
This chapter has been written to help you understand the basic ideas of Bayesian Statistics,
andinparticular,Bayes’Theorem(alsoknownasBayes’Rule). WewillseehowtheBayesian
approach compares to the more traditional Classical, or Frequentist, approach to statistics
and the potential applications in both quantitative trading and risk management.
In the chapter we will:
(cid:136)
De(cid:28)ne Bayesian statistics and Bayesian inference
(cid:136)
Compare Classical/Frequentist statistics and Bayesian statistics
(cid:136)
Derive the famous Bayes’ Rule, an essential tool for Bayesian inference
(cid:136)
Interpret and apply Bayes’ Rule for carrying out Bayesian inference
(cid:136)
Carry out a concrete probability coin-(cid:29)ip example of Bayesian inference
2.1 What is Bayesian Statistics?
Bayesian statistics is a particular approach to applying probability to statistical prob-
lems. It provides us with mathematical tools to update our beliefs about random events in light
of seeing new data or evidence about those events.
In particular Bayesian inference interprets probability as a measure of believability or con(cid:28)-
dence that an individual may possess about the occurance of a particular event.
Wemayhaveaprior beliefaboutanevent,butourbeliefsarelikelytochangewhennewevi-
denceisbroughttolight. Bayesianstatisticsgivesusasolidmathematicalmeansofincorporating
our prior beliefs, and evidence, to produce new posterior beliefs.
Bayesian statistics provides us with mathematical tools to rationally update our sub-
jective beliefs in light of new data or evidence.
This is in contrast to another form of statistical inference, known as Classical or Frequentist,
statistics,whichassumesthatprobabilitiesarethefrequency ofparticularrandomeventsoccuring
in a long run of repeated trials.
For example, as we roll a fair unweighted six-sided die repeatedly, we would see that each
number on the die tends to come up 1/6th of the time.
Frequentist statistics assumes that probabilities are the long-run frequency of random
events in repeated trials.
11

12
When carrying out statistical inference, that is, inferring statistical information from proba-
bilisticsystems,thetwoapproaches-FrequentistandBayesian-haveverydi(cid:27)erentphilosophies.
Frequentiststatisticstriestoeliminate uncertaintybyprovidingestimates. Bayesianstatistics
tries to preserve and re(cid:28)ne uncertainty by adjusting individual beliefs in light of new evidence.
2.1.1 Frequentist vs Bayesian Examples
In order to make clear the distinction between the two di(cid:27)ering statistical philosophies, we will
consider two examples of probabilistic systems:
(cid:136)
Coin (cid:29)ips - What is the probability of an unfair coin coming up heads?
(cid:136) Election of a particular candidate for UKPrime Minister-Whatistheprobability
of seeing an individual candidate winning, who has not stood before?
The following table describes the alternative philosophies of the frequentist and Bayesian
approaches:
Table 2.1: Comparison of Frequentist and Bayesian probability
Example Frequentist Interpretation Bayesian Interpretation
Unfair Coin Flip The probability of seeing a head Prior to any (cid:29)ips of the coin an
when the unfair coin is (cid:29)ipped individual may believe that the
is the long-run relative frequency coin is fair. After a few (cid:29)ips the
of seeing a head when repeated coincontinuallycomesupheads.
(cid:29)ips of the coin are carried out. Thus the prior belief about fair-
That is, as we carry out more ness of the coin is modi(cid:28)ed to
coin (cid:29)ips the number of heads account for the fact that three
obtained as a proportion of the headshavecomeupinarowand
total (cid:29)ips tends to the "true" or thus the coin might not be fair.
"physical"probabilityofthecoin After 500 (cid:29)ips, with 400 heads,
coming up as heads. In partic- the individual believes that the
ular the individual running the coin is very unlikely to be fair.
experiment does not incorporate The posterior belief is heavily
their own beliefs about the fair- modi(cid:28)ed from the prior belief of
ness of other coins. a fair coin.
Election of Candidate The candidate only ever stands An individual has a prior belief
once for this particular election of a candidate’s chances of win-
and so we cannot perform "re- ning an election and their con-
peated trials". In a frequen- (cid:28)dence can be quanti(cid:28)ed as a
tist setting we construct "vir- probability. However another in-
tual" trials of the election pro- dividual could also have a sepa-
cess. The probability of the can- rate di(cid:27)ering prior belief about
didate winning is de(cid:28)ned as the the same candidate’s chances.
relative frequency of the candi- Asnewdataarrives, bothbeliefs
datewinninginthe"virtual"tri- are (rationally) updated by the
als as a fraction of all trials. Bayesian procedure.
Thus in the Bayesian interpretation probability is a summary of an individual’s opinion.
A key point is that di(cid:27)erent (rational, intelligent) individuals can have di(cid:27)erent opinions (and
thus di(cid:27)erent prior beliefs), since they have di(cid:27)ering access to data and ways of interpreting
it. However, as both of these individuals come across new data that they both have access to,
their (potentially di(cid:27)ering) prior beliefs will lead to posterior beliefs that will begin converging
towards each other, under the rational updating procedure of Bayesian inference.

13
In the Bayesian framework an individual would apply a probability of 0 when they have
no con(cid:28)dence in an event occuring, while they would apply a probability of 1 when they are
absolutelycertainofaneventoccuring. Assigningaprobabilitybetween0and1allowsweighted
con(cid:28)dence in other potential outcomes.
In order to carry out Bayesian inference, we need to utilise a famous theorem in probability
known as Bayes’ rule and interpret it in the correct fashion. In the following box, we derive
Bayes’ruleusingthede(cid:28)nitionofconditional probability. However,itisn’tessentialtofollowthe
derivationinordertouseBayesianmethods, sofeel free to skip the following sectionifyou
wish to jump straight into learning how to use Bayes’ rule.
Deriving Bayes’ Rule
We begin by considering the de(cid:28)nition of conditional probability, which gives us a rule for
determining the probability of an event A, given the occurance of another event B. An example
questioninthisveinmightbe"Whatistheprobabilityofrainoccuring giventhatthereareclouds
in the sky?"
The mathematical de(cid:28)nition of conditional probability is as follows:
P(A∩B)
P(A|B)= (2.1)
P(B)
This simply states that the probability of A occuring given that B has occured is equal to
the probability that they have both occured, relative to the probability that B has occured.
Or in the language of the example above: The probability of rain given that we have seen
clouds isequaltotheprobabilityofrainand cloudsoccuringtogether,relativetotheprobability
of seeing clouds at all.
If we multiply both sides of this equation by P(B) we get:
P(B)P(A|B)=P(A∩B) (2.2)
But, we can simply make the same statement about P(B|A), which is akin to asking "What
is the probability of seeing clouds, given that it is raining?":
P(B∩A)
P(B|A)= (2.3)
P(A)
Note that P(A∩B)=P(B∩A) and so by substituting the above and multiplying by P(A),
we get:
P(A)P(B|A)=P(A∩B) (2.4)
We are now able to set the two expressions for P(A∩B) equal to each other:
P(B)P(A|B)=P(A)P(B|A) (2.5)
If we now divide both sides by P(B) we arrive at the celebrated Bayes’ rule:
P(B|A)P(A)
P(A|B)= (2.6)
P(B)
However, it will be helpful for later usage of Bayes’ rule to modify the denominator, P(B)
on the right hand side of the above relation to be written in terms of P(B|A). We can actually
write:

14
(cid:88)
|     |     |     |     | P(B)= | P(B∩A) |     |     | (2.7) |
| --- | --- | --- | --- | ----- | ------ | --- | --- | ----- |
a∈A
This is possible because the events A are an exhaustive partition of the sample space.
| So that | by substituting |       | the de(cid:28)ntion |          | of conditional | probability | we get: |       |
| ------- | --------------- | ----- | ------------------- | -------- | -------------- | ----------- | ------- | ----- |
|         |                 |       |                     | (cid:88) |                | (cid:88)    |         |       |
|         |                 | P(B)= |                     | P(B∩A)=  |                | P(B|A)P(A)  |         | (2.8) |
|         |                 |       |                     | a∈A      |                | a∈A         |         |       |
Finally, wecansubstitutethisintoBayes’rulefromabovetoobtainanalternativeversionof
| Bayes’ rule, | which is | used | heavily | in Bayesian | inference: |     |     |     |
| ------------ | -------- | ---- | ------- | ----------- | ---------- | --- | --- | --- |
P(B|A)P(A)
|     |     |     | P(A|B)= |     |                     |     |     | (2.9) |
| --- | --- | --- | ------- | --- | ------------------- | --- | --- | ----- |
|     |     |     |         |     | (cid:80) P(B|A)P(A) |     |     |       |
a∈A
Now that we have derived Bayes’ rule we are able to apply it to statistical inference.
| 2.2 | Applying | Bayes’ |     | Rule | for | Bayesian | Inference |     |
| --- | -------- | ------ | --- | ---- | --- | -------- | --------- | --- |
As we stated at the start of this chapter the basic idea of Bayesian inference is to continually
update our prior beliefs about events as new evidence is presented. This is a very natural way
to think about probabilistic events. As more and more evidence is accumulated our prior beliefs
| are steadily | "washed | out" | by any | new data. |     |     |     |     |
| ------------ | ------- | ---- | ------ | --------- | --- | --- | --- | --- |
Consider a (rather nonsensical) prior belief that the Moon is going to collide with the Earth.
For every night that passes, the application of Bayesian inference will tend to correct our prior
belief to a posterior belief that the Moon is less and less likely to collide with the Earth, since it
| remains | in orbit. |     |     |     |     |     |     |     |
| ------- | --------- | --- | --- | --- | --- | --- | --- | --- |
In order to demonstrate a concrete numerical example of Bayesian inference it is necessary
| to introduce | some new | notation. |     |     |     |     |     |     |
| ------------ | -------- | --------- | --- | --- | --- | --- | --- | --- |
Firstly, we need to consider the concept of parameters and models. A parameter could be
the weighting of an unfair coin, which we could label as θ. Thus θ = P(H) would describe the
probability distribution of our beliefs that the coin will come up as heads when (cid:29)ipped. The
model is the actual means of encoding this (cid:29)ip mathematically. In this instance, the coin (cid:29)ip
| can be modelled | as    | a Bernoulli | trial. |     |     |     |     |     |
| --------------- | ----- | ----------- | ------ | --- | --- | --- | --- | --- |
| Bernoulli       | Trial |             |        |     |     |     |     |     |
A Bernoulli trial is a random experiment with only two outcomes, usually labelled as "success"
or "failure", in which the probability of the success is exactly the same every time the trial is
carried out. The probability of the success is given by θ, which is a number between 0 and 1.
Thus θ ∈[0,1].
Over thecourse ofcarryingout somecoin (cid:29)ipexperiments(repeated Bernoulli trials)wewill
| generate | some data, | D, about | heads | or  | tails. |     |     |     |
| -------- | ---------- | -------- | ----- | --- | ------ | --- | --- | --- |
A natural example question to ask is "What is the probability of seeing 3 heads in 8 (cid:29)ips (8
| Bernoulli | trials), given | a fair | coin | (θ =0.5)?". |     |     |     |     |
| --------- | -------------- | ------ | ---- | ----------- | --- | --- | --- | --- |
A model helps us to ascertain the probability of seeing this data, D, given a value of the
parameter θ. The probability of seeing data D under a particular value of θ is given by the
| following | notation: | P(D|θ). |     |     |     |     |     |     |
| --------- | --------- | ------- | --- | --- | --- | --- | --- | --- |
However,ifyouconsideritforamoment,weareactually interestedinthealternativequestion
- "What is the probability that the coin is fair (or unfair), given that I have seen a particular
| sequence | of heads and | tails?". |     |     |     |     |     |     |
| -------- | ------------ | -------- | --- | --- | --- | --- | --- | --- |
Thus we are interested in the probability distribution which re(cid:29)ects our belief about di(cid:27)erent
possible values of θ, given that we have observed some data D. This is denoted by P(θ|D).
Notice that this is the converse of P(D|θ). So how do we get between these two probabilities?
It turns out that Bayes’ rule is the link that allows us to go between the two situations.

15
| Bayes’ | Rule | for Bayesian |     | Inference              |     |     |     |     |        |
| ------ | ---- | ------------ | --- | ---------------------- | --- | --- | --- | --- | ------ |
|        |      |              |     | P(θ|D)=P(D|θ)P(θ)/P(D) |     |     |     |     | (2.10) |
Where:
| (cid:136) P(θ) |     |     |     |     |     |     | θ   |     |     |
| -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
is the prior. This is the strength in our belief of without considering the evidence
| D.  | Our | prior view | on  | the probability |     | of how fair | the coin is. |     |     |
| --- | --- | ---------- | --- | --------------- | --- | ----------- | ------------ | --- | --- |
(cid:136) P(θ|D) is the posterior. This is the (re(cid:28)ned) strength of our belief of θ once the evidence
D
has been taken into account. After seeing 4 heads out of 8 (cid:29)ips, say, this is our updated
| view | on  | the fairness | of  | the | coin. |     |     |     |     |
| ---- | --- | ------------ | --- | --- | ----- | --- | --- | --- | --- |
(cid:136) P(D|θ) is the likelihood. This is the probability of seeing the data D as generated by a
modelwithparameterθ.
|     |        |          |     | If           | we knew | the coin was    | fair, this tells | us the probability | of seeing |
| --- | ------ | -------- | --- | ------------ | ------- | --------------- | ---------------- | ------------------ | --------- |
| a   | number | of heads | in  | a particular | number  | of (cid:29)ips. |                  |                    |           |
(cid:136) P(D) is the evidence. This is the probability of the data as determined by summing (or
θ,
integrating) across all possible values of weighted by how strongly we believe in those
particular values of θ. If we had multiple views of what the fairness of the coin is (but
didn’t know for sure), then this tells us the probability of seeing a certain sequence of (cid:29)ips
| for | all possibilities |     | of  | our belief | in the | coin’s fairness. |     |     |     |
| --- | ----------------- | --- | --- | ---------- | ------ | ---------------- | --- | --- | --- |
The entire goal of Bayesian inference is to provide us with a rational and mathematically
sound procedure for incorporating our prior beliefs, with any evidence at hand, in order to
produce an updated posterior belief. What makes it such a valuable technique is that posterior
beliefscanthemselvesbeusedaspriorbeliefsunderthegenerationofnew data. HenceBayesian
inferenceallowsustocontinually adjustourbeliefsundernewdatabyrepeatedlyapplyingBayes’
rule.
There was a lot of theory to take in within the previous two sections, so I’m now going to
provide a concrete example using the age-old tool of statisticians: the coin-(cid:29)ip.
| 2.3 | Coin-Flipping |     |     | Example |     |     |     |     |     |
| --- | ------------- | --- | --- | ------- | --- | --- | --- | --- | --- |
In this example we are going to consider multiple coin-(cid:29)ips of a coin with unknown fairness. We
will use Bayesian inference to update our beliefs on the fairness of the coin as more data (i.e.
more coin (cid:29)ips) becomes available. The coin will actually be fair, but we won’t learn this until
the trials are carried out. At the start we have no prior belief on the fairness of the coin, that
| is, we can | say | that any | level | of fairness | is  | equally likely. |     |     |         |
| ---------- | --- | -------- | ----- | ----------- | --- | --------------- | --- | --- | ------- |
|            |     |          |       |             |     | N               |     |     | θ =0.5. |
In statistical language we are going to perform repeated Bernoulli trials with We
will use a uniform distribution as a means of characterising our prior belief that we are unsure
about the fairness. This states that we consider each level of fairness (or each value of θ) to be
equally likely.
We are going to use a Bayesian updating procedure to go from our prior beliefs to posterior
beliefs as we observe new coin (cid:29)ips. This is carried out using a particularly mathematically
succinctprocedureviatheconceptofconjugate priors. Wewon’tgointoanydetailonconjugate
priors within this chapter, as it will form the basis of the next chapter on Bayesian inference. It
will however provide us with the means of explaining how the coin (cid:29)ip example is carried out in
practice.
The uniform distribution is actually a more speci(cid:28)c case of another probability distribution,
known as a Beta distribution. Conveniently, under the binomial model, if we use a Beta distri-
bution for our prior beliefs it leads to a Beta distribution for our posterior beliefs. This is an
extremelyusefulmathematicalresult,asBetadistributionsarequite(cid:29)exibleinmodellingbeliefs.
However, I don’t want to dwell on the details of this too much here, since we will discuss it in
the next chapter. At this stage, it just allows us to easily create some visualisations below that
| emphasises | the | Bayesian | procedure! |     |     |     |     |     |     |
| ---------- | --- | -------- | ---------- | --- | --- | --- | --- | --- | --- |

16
In the following (cid:28)gure we can see 6 particular points at which we have carried out a number
of Bernoulli trials (coin (cid:29)ips). In the (cid:28)rst sub-plot we have carried out no trials and hence our
probability density function (in this case our prior density) is the uniform distribution. It states
that we have equal belief in all values of θ representing the fairness of the coin.
The next panel shows 2 trials carried out and they both come up heads. Our Bayesian
procedureusingtheconjugateBetadistributionsnowallowsustoupdatetoaposterior density.
Notice how the weight of the density is now shifted to the right hand side of the chart. This
indicates that our prior belief of equal likelihood of fairness of the coin, coupled with 2 new data
points, leads us to believe that the coin is more likely to be unfair (biased towards heads) than
it is tails.
The following two panels show 10 and 20 trials respectively. Notice that even though we
have seen 2 tails in 10 trials we are still of the belief that the coin is likely to be unfair and
biased towards heads. After 20 trials, we have seen a few more tails appear. The density of the
probability has now shifted closer to θ =P(H)=0.5. Hence we are now starting to believe that
the coin is possibly fair.
After 50 and 500 trials respectively, we are now beginning to believe that the fairness of
the coin is very likely to be around θ = 0.5. This is indicated by the shrinking width of the
probabilitydensity,whichisnowclusteredtightlyaroundθ =0.46inthe(cid:28)nalpanel. Wereweto
carry out another 500 trials (since the coin is actually fair) we would see this probability density
become even tighter and centred closer to θ =0.5.
Figure 2.1: Bayesian update procedure using the Beta-Binomial Model
Thus it can be seen that Bayesian inference gives us a rational procedure to go from an
uncertainsituationwithlimitedinformationtoamorecertainsituationwithsigni(cid:28)cantamounts
of data. In the next chapter we will discuss the notion of conjugate priors in more depth, which
heavily simplify the mathematics of carrying out Bayesian inference in this example.
For completeness, I’ve provided the Python code (heavily commented) for producing this
plot. It makes use of SciPy’s statistics model, in particular, the Beta distribution:

17
# beta_binomial.py
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
if __name__ == "__main__":
# Create a list of the number of coin tosses ("Bernoulli trials")
number_of_trials = [0, 2, 10, 20, 50, 500]
# Conduct 500 coin tosses and output into a list of 0s and 1s
# where 0 represents a tail and 1 represents a head
data = stats.bernoulli.rvs(0.5, size=number_of_trials[-1])
# Discretise the x-axis into 100 separate plotting points
x = np.linspace(0, 1, 100)
# Loops over the number_of_trials list to continually add
# more coin toss data. For each new set of data, we update
# our (current) prior belief to be a new posterior. This is
# carried out using what is known as the Beta-Binomial model.
# For the time being, we won’t worry about this too much.
for i, N in enumerate(number_of_trials):
# Accumulate the total number of heads for this
# particular Bayesian update
heads = data[:N].sum()
# Create an axes subplot for each update
ax = plt.subplot(len(number_of_trials) / 2, 2, i + 1)
ax.set_title("%s trials, %s heads" % (N, heads))
# Add labels to both axes and hide labels on y-axis
plt.xlabel("$P(H)$, Probability of Heads")
plt.ylabel("Density")
if i == 0:
plt.ylim([0.0, 2.0])
plt.setp(ax.get_yticklabels(), visible=False)
# Create and plot a Beta distribution to represent the
# posterior belief in fairness of the coin.
y = stats.beta.pdf(x, 1 + heads, 1 + N - heads)
plt.plot(x, y, label="observe %d tosses,\n %d heads" % (N, heads))
plt.fill_between(x, 0, y, color="#aaaadd", alpha=0.5)
# Expand plot to cover full width/height and show it
plt.tight_layout()
plt.show()

18

| Chapter  | 3         |     |      |          |
| -------- | --------- | --- | ---- | -------- |
| Bayesian | Inference |     | of a | Binomial |
Proportion
In the previous chapter we examined Bayes’ rule and considered how it allowed us to rationally
update beliefs about uncertainty as new evidence came to light. We mentioned brie(cid:29)y that
such techniques are becoming extremely important in the (cid:28)elds of data science and quantitative
(cid:28)nance.
Inthischapterwearegoingtoexpandonthecoin-(cid:29)ipexamplethatwestudiedintheprevious
chapter by discussing the notion of Bernoulli trials, the beta distribution and conjugate priors.
Ourgoalinthischapteristoallowustocarryoutwhatisknownas"inferenceonabinomial
proportion". That is, we will be studying probabilistic situations with two outcomes (e.g. a
coin-(cid:29)ip) and trying to estimate the proportion of a repeated set of events that come up heads
or tails.
Our goal is to estimate how fair a coin is. We will use that estimate to make
predictions abouthowmanytimesitwillcomeupheadswhenwe(cid:29)ipitinthefuture.
While this may sound like a rather academic example, it is actually substantially more ap-
plicable to real-world applications than may (cid:28)rst appear. Consider the following scenarios:
(cid:136)
Engineering: Estimating the proportion of aircraft turbine blades that possess a struc-
| tural | defect after fabrication |     |     |     |
| ----- | ------------------------ | --- | --- | --- |
(cid:136) Social Science: Estimating the proportion of individuals who would respond "yes" on a
| census | question |     |     |     |
| ------ | -------- | --- | --- | --- |
(cid:136)
Medical Science: Estimating the proportion of patients who make a full recovery after
| taking | an experimental | drug to cure | a disease |     |
| ------ | --------------- | ------------ | --------- | --- |
(cid:136) Corporate Finance: Estimating the proportion of transactions in error when carrying
| out (cid:28)nancial | audits |     |     |     |
| ------------------- | ------ | --- | --- | --- |
(cid:136)
Data Science: Estimating the proportion of individuals who click on an ad when visiting
a website
As can be seen, inference on a binomial proportion is an extremely important statistical
technique and will form the basis of many of the chapters on Bayesian statistics that follow.
| 3.1 The | Bayesian | Approach |     |     |
| ------- | -------- | -------- | --- | --- |
While we motivated the concept of Bayesian statistics in the previous chapter, I want to outline
(cid:28)rst how our analysis will proceed. This will motivate the following sections and give you a
| "bird’s eye | view" of what | the Bayesian | approach is all about. |     |
| ----------- | ------------- | ------------ | ---------------------- | --- |
19

20
As we stated above, our goal is estimate the fairness of a coin. Once we have an estimate for
the fairness, we can use this to predict the number of future coin (cid:29)ips that will come up heads.
We will learn about the speci(cid:28)c techniques as we go while we cover the following steps:
1. Assumptions - We will assume that the coin has two outcomes (i.e. it won’t land on its
side),the(cid:29)ipswillappearrandomlyandwillbecompletelyindependentofeachother. The
fairness of the coin will also be stationary, that is it won’t alter over time. We will denote
the fairness by the parameter θ. We will be considering stationary processes in depth in
| the section | on  | Time Series | Analysis |     | later in the | book. |     |
| ----------- | --- | ----------- | -------- | --- | ------------ | ----- | --- |
2. Prior Beliefs-TocarryoutaBayesiananalysis,wemustquantifyourprior beliefs about
the fairness of the coin. This comes down to specifying a probability distribution on our
beliefs of this fairness. We will use a relatively (cid:29)exible probability distribution called the
| beta distribution |     | to  | model | our beliefs. |     |     |     |
| ----------------- | --- | --- | ----- | ------------ | --- | --- | --- |
3. Experimental Data-Wewillcarryoutsome(virtual)coin-(cid:29)ipsinordertogiveussome
harddata. Wewillcountthenumberofheadsz thatappearinN (cid:29)ipsofthecoin. Wewill
alsoneedawayofdeterminingtheprobabilityofsuchresultsappearing,givenaparticular
fairness, θ, of the coin. For this we will need to discuss likelihood functions, and in
| particular | the | Bernoulli | likelihood |     | function. |     |     |
| ---------- | --- | --------- | ---------- | --- | --------- | --- | --- |
4. Posterior Beliefs - Once we have a prior belief and a likelihood function, we can use
Bayes’ruleinordertocalculateaposterior belief aboutthefairnessofthecoin. Wecouple
ourpriorbeliefswiththedatawehaveobservedandupdateourbeliefsaccordingly. Luckily
for us, if we use a beta distribution as our prior and a Bernoulli likelihood we also get a
| beta distribution |     | as a | posterior. | These | are known | as conjugate | priors. |
| ----------------- | --- | ---- | ---------- | ----- | --------- | ------------ | ------- |
5. Inference - Once we have a posterior belief we can estimate the coin’s fairness θ, predict
the probability of heads on the next (cid:29)ip or even see how the results depend upon di(cid:27)erent
| choices | of prior | beliefs. | The | latter is | known as | model comparison. |     |
| ------- | -------- | -------- | --- | --------- | -------- | ----------------- | --- |
At each step of the way we will be making visualisations of each of these functions and
distributions using the relatively recent Seaborn plotting package for Python. Seaborn sits "on
| top" of Matplotlib, |     | but has | far better | defaults | for statistical | plotting. |     |
| ------------------- | --- | ------- | ---------- | -------- | --------------- | --------- | --- |
| 3.2 Assumptions     |     |         | of the     | Approach |                 |           |     |
As with all models we need to make some assumptions about our situation.
(cid:136) We are going to assume that our coin can only have two outcomes, that is it can only land
| on its head | or  | tail and | never | on its side |     |     |     |
| ----------- | --- | -------- | ----- | ----------- | --- | --- | --- |
(cid:136)
Each(cid:29)ipofthecoiniscompletelyindependentoftheothers, i.e. wehaveindependentand
| identically | distributed |     | (i.i.d.) | coin (cid:29)ips |     |     |     |
| ----------- | ----------- | --- | -------- | ---------------- | --- | --- | --- |
(cid:136)
| The fairness | of  | the coin | does | not change | in time, | that is it | is stationary |
| ------------ | --- | -------- | ---- | ---------- | -------- | ---------- | ------------- |
With these assumptions in mind, we can now begin discussing the Bayesian procedure.
| 3.3 Recalling |     | Bayes’ |     | Rule |     |     |     |
| ------------- | --- | ------ | --- | ---- | --- | --- | --- |
In the the previous chapter we outlined Bayes’ rule. I’ve repeated it here for completeness:
P(θ|D)=P(D|θ)P(θ)/P(D) (3.1)
Where:

21
| (cid:136) P(θ) |     |     |     |     |     |     | θ   |
| -------------- | --- | --- | --- | --- | --- | --- | --- |
is the prior. This is the strength in our belief of without considering the evidence
| D.  | Our prior | view | on  | the probability |     | of how fair | the coin is. |
| --- | --------- | ---- | --- | --------------- | --- | ----------- | ------------ |
(cid:136) P(θ|D) θ
is the posterior. This is the (re(cid:28)ned) strength of our belief of once the evidence
D has been taken into account. After seeing 4 heads out of 8 (cid:29)ips, say, this is our updated
| view | on the | fairness | of  | the coin. |     |     |     |
| ---- | ------ | -------- | --- | --------- | --- | --- | --- |
(cid:136)
P(D|θ) is the likelihood. This is the probability of seeing the data D as generated by a
modelwithparameterθ. If we knew the coin was fair, this tells us the probability of seeing
| a number |     | of heads | in  | a particular | number | of (cid:29)ips. |     |
| -------- | --- | -------- | --- | ------------ | ------ | --------------- | --- |
(cid:136) P(D) is the evidence. This is the probability of the data as determined by summing (or
integrating) across all possible values of θ, weighted by how strongly we believe in those
particular values of θ. If we had multiple views of what the fairness of the coin is (but
didn’t know for sure), then this tells us the probability of seeing a certain sequence of (cid:29)ips
| for | all possibilities |     | of our | belief | in the | coin’s fairness. |     |
| --- | ----------------- | --- | ------ | ------ | ------ | ---------------- | --- |
Note that we have three separate components to specify, in order to calcute the posterior.
They are the likelihood, the prior and the evidence. In the following sections we are going to
discuss exactly how to specify each of these components for our particular case of inference on a
| binomial | proportion. |            |     |     |          |     |     |
| -------- | ----------- | ---------- | --- | --- | -------- | --- | --- |
| 3.4 The  |             | Likelihood |     |     | Function |     |     |
We have just outlined Bayes’ rule and have seen that we must specify a likelihood function,
a prior belief and the evidence (i.e. a normalising constant). In this section we are going to
| consider | the (cid:28)rst | of these | components,  |     | namely | the likelihood. |     |
| -------- | --------------- | -------- | ------------ | --- | ------ | --------------- | --- |
| 3.4.1    | Bernoulli       |          | Distribution |     |        |                 |     |
Our example is that of a sequence of coin (cid:29)ips. We are interested in the probability of the coin
coming up heads. In particular, we are interested in the probability of the coin coming up heads
| as a function | of  | the underlying |     | fairness | parameter | θ.  |     |
| ------------- | --- | -------------- | --- | -------- | --------- | --- | --- |
This will take a functional form, f. If we denote by k the random variable that describes the
result of the coin toss, which is drawn from the set {1,0}, where k = 1 represents a head and
k = 0 represents a tail, then the probability of seeing a head, with a particular fairness of the
| coin, is given | by: |     |     |     |     |     |     |
| -------------- | --- | --- | --- | --- | --- | --- | --- |
P(k =1|θ)=f(θ) (3.2)
We can choose a particularly succint form for f(θ) by simply stating the probability is given
by θ itself, i.e. f(θ)=θ. This leads to the probability of a coin coming up heads to be given by:
|     |                 |     |           |     | P(k      | =1|θ)=θ | (3.3) |
| --- | --------------- | --- | --------- | --- | -------- | ------- | ----- |
| And | the probability |     | of coming |     | up tails | as:     |       |
P(k =0|θ)=1−θ (3.4)
| This | can also | be written |     | as: |     |     |     |
| ---- | -------- | ---------- | --- | --- | --- | --- | --- |
P(k|θ)=θk(1−θ)1−k
(3.5)
| Where | k ∈{1,0} | and | θ ∈[0,1]. |     |     |     |     |
| ----- | -------- | --- | --------- | --- | --- | --- | --- |
This is known as the Bernoulli distribution. It gives the probability over two separate,
| discrete | values of | k for | a (cid:28)xed | fairness | parameter | θ.  |     |
| -------- | --------- | ----- | ------------- | -------- | --------- | --- | --- |
In essence it tells us the probability of a coin coming up heads or tails depending on how fair
the coin is.

22
| 3.4.2 | Bernoulli |     | Likelihood |     | Function |     |     |     |     |
| ----- | --------- | --- | ---------- | --- | -------- | --- | --- | --- | --- |
We can also consider another way of looking at the above function. If we consider a (cid:28)xed
k, θ
observation, i.e. a known coin (cid:29)ip outcome, and the fairness parameter as a continuous
variable then:
P(k|θ)=θk(1−θ)1−k
(3.6)
tells us the probability of a (cid:28)xed outcome k given some particular value of θ. As we adjust θ
(e.g. change the fairness of the coin), we will start to see di(cid:27)erent probabilities for k.
This is known as the likelihood function of θ. It is a function of a continuous θ and di(cid:27)ers
from the Bernoulli distribution because the latter is actually a discrete probability distribution
| over two | potential | outcomes |     | of the | coin-(cid:29)ip | k.  |     |     |     |
| -------- | --------- | -------- | --- | ------ | --------------- | --- | --- | --- | --- |
Note that the likelihood function is not actually a probability distribution in the true sense
θ
since integrating it across all values of the fairness parameter does not actually equal 1, as is
| required | for a | probability | distribution. |     |     |     |     |     |     |
| -------- | ----- | ----------- | ------------- | --- | --- | --- | --- | --- | --- |
We say that P(k|θ)=θk(1−θ)1−k is the Bernoulli likelihood function for θ.
| 3.4.3 | Multiple |     | Flips | of the | Coin |     |     |     |     |
| ----- | -------- | --- | ----- | ------ | ---- | --- | --- | --- | --- |
Now that we have the Bernoulli likelihood function we can use it to determine the probability of
| seeing a | particular | sequence |     | of N | (cid:29)ips, given | by  | the set | {k ,...,k }. |     |
| -------- | ---------- | -------- | --- | ---- | ------------------ | --- | ------- | ------------ | --- |
|          |            |          |     |      |                    |     |         | 1 N          |     |
Since each of these (cid:29)ips is independent of any other, the probability of the sequence occuring
| is simply | the product |     | of the | probability |     | of each | (cid:29)ip occuring. |     |     |
| --------- | ----------- | --- | ------ | ----------- | --- | ------- | -------------------- | --- | --- |
If we have a particular fairness parameter θ, then the probability of seeing this particular
| stream | of (cid:29)ips, | given | θ, is given | by: |     |     |     |     |     |
| ------ | --------------- | ----- | ----------- | --- | --- | --- | --- | --- | --- |
(cid:89)
|     |     |     | P({k | ,...,k |     | }|θ) = | P(k | |θ) | (3.7) |
| --- | --- | --- | ---- | ------ | --- | ------ | --- | --- | ----- |
|     |     |     |      | 1      | N   |        |     | i   |       |
i
(cid:89)
θki(1−θ)1−ki
|     |     |     |     |     |     | =   |     |     | (3.8) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
i
What if we are interested in the number of heads, say, in N (cid:29)ips? If we denote by z the
| number | of heads | appearing, |     | then the            | formula | above | becomes: |     |       |
| ------ | -------- | ---------- | --- | ------------------- | ------- | ----- | -------- | --- | ----- |
|        |          |            |     | P(z,N|θ)=θz(1−θ)N−z |         |       |          |     | (3.9) |
|        |          |            |     |                     | z       |       | N        |     | θ.    |
That is, the probability of seeing heads, in (cid:29)ips, assuming a fairness parameter We
will use this formula when we come to determine our posterior belief distribution later in the
chapter.
| 3.5 | Quantifying |     |     | our | Prior | Beliefs |     |     |     |
| --- | ----------- | --- | --- | --- | ----- | ------- | --- | --- | --- |
AnextremelyimportantstepintheBayesianapproachistodetermineourpriorbeliefsandthen
| (cid:28)nd a means | of  | quantifying |     | them. |     |     |     |     |     |
| ------------------ | --- | ----------- | --- | ----- | --- | --- | --- | --- | --- |
In the Bayesian approach we need to determine our prior beliefs on parameters and
| then | (cid:28)nd | a probability |     | distribution |     | that quanti(cid:28)es |     | these beliefs. |     |
| ---- | ---------- | ------------- | --- | ------------ | --- | --------------------- | --- | -------------- | --- |
In this instance we are interested in our prior beliefs on the fairness of the coin. That is, we
| wish to | quantify | our uncertainty |     | in  | how | biased | the coin | is. |     |
| ------- | -------- | --------------- | --- | --- | --- | ------ | -------- | --- | --- |
Todothisweneedtounderstandtherangeofvaluesthatθ
cantakeandhowlikelywethink
| each of | those values | are | to occur. |     |     |     |     |     |     |
| ------- | ------------ | --- | --------- | --- | --- | --- | --- | --- | --- |
θ = 0 indicates a coin that always comes up tails, while θ = 1 implies a coin that always
comes up heads. A fair coin is denoted by θ = 0.5. Hence θ ∈ [0,1]. This implies that our
| probability | distribution |     | must | also | exist | on the interval |     | [0,1]. |     |
| ----------- | ------------ | --- | ---- | ---- | ----- | --------------- | --- | ------ | --- |
The question then becomes - which probability distribution do we use to quantify our beliefs
| about the | coin? |     |     |     |     |     |     |     |     |
| --------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |

23
| 3.5.1 | Beta Distribution |     |     |
| ----- | ----------------- | --- | --- |
Inthisinstancewearegoingtochoosethebeta distribution. Theprobabilitydensityfunction
| (PDF) of | the beta distribution | is given | by the following: |
| -------- | --------------------- | -------- | ----------------- |
P(θ|α,β)=θα−1(1−θ)β−1/B(α,β) (3.10)
B(α,β)
Where the term in the denominator, is present to act as a normalising constant so
| that the area | under the PDF | actually sums | to 1. |
| ------------- | ------------- | ------------- | ----- |
I’ve plotted a few separate realisations of the beta distribution for various parameters α and
| β in Figure | 3.1. |     |     |
| ----------- | ---- | --- | --- |
Figure 3.1: Di(cid:27)erent realisations of the beta distribution for various parameters α and β.
| To plot     | the image yourself, | you will | need to install seaborn: |
| ----------- | ------------------- | -------- | ------------------------ |
| pip install | seaborn             |          |                          |
| The Python  | code to produce     | the plot | is given below:          |
# beta_plot.py
| import numpy             | as np          |        |     |
| ------------------------ | -------------- | ------ | --- |
| from scipy.stats         | import         | beta   |     |
| import matplotlib.pyplot |                | as plt |     |
| import seaborn           | as sns         |        |     |
| if __name__              | == "__main__": |        |     |
sns.set_palette("deep",
desat=.6)
| sns.set_context(rc={"figure.figsize": |                |         | (8, 4)}) |
| ------------------------------------- | -------------- | ------- | -------- |
| x =                                   | np.linspace(0, | 1, 100) |          |
| params                                | = [            |         |          |

24
(0.5, 0.5),
(1, 1),
(4, 3),
(2, 5),
(6, 6)
]
| for                    | p in            | params: |                         |       |              |      |
| ---------------------- | --------------- | ------- | ----------------------- | ----- | ------------ | ---- |
|                        | y = beta.pdf(x, |         | p[0],                   | p[1]) |              |      |
|                        | plt.plot(x,     |         | y, label="$\\alpha=%s$, |       | $\\beta=%s$" | % p) |
| plt.xlabel("$\\theta$, |                 |         | Fairness")              |       |              |      |
plt.ylabel("Density")
plt.legend(title="Parameters")
plt.show()
α
Essentially, as becomes larger the bulk of the probability distribution moves towards the
right(acoinbiasedtocomeupheadsmoreoften),whereasanincreaseinβmovesthedistribution
| towards | the left | (a coin | biased to come | up tails more | often). |     |
| ------- | -------- | ------- | -------------- | ------------- | ------- | --- |
However,ifbothαandβ increasethenthedistributionbeginstonarrow. Ifαandβ increase
equally, then the distribution will peak over θ =0.5, i.e. when the coin is far.
Why have we chosen the beta function as our prior? There are a couple of reasons:
(cid:136) Support - It’s de(cid:28)ned on the interval [0,1], which is the same interval that θ exists over.
(cid:136) Flexibility-Itpossessestwoshapeparametersknownasαandβ,whichgiveitsigni(cid:28)cant
(cid:29)exibility. This (cid:29)exibility provides us with a lot of choice in how we model our beliefs.
However, perhaps the most important reason for choosing a beta distribution is because it is
| a conjugate | prior  | for | the Bernoulli | distribution. |     |     |
| ----------- | ------ | --- | ------------- | ------------- | --- | --- |
| Conjugate   | Priors |     |               |               |     |     |
In Bayes’ rule above we can see that the posterior distribution is proportional to the product of
| the prior | distribution | and | the likelihood | function: |     |     |
| --------- | ------------ | --- | -------------- | --------- | --- | --- |
P(θ|D)∝P(D|θ)P(θ) (3.11)
A conjugate prior is a choice of prior distribution, that when coupled with a speci(cid:28)c type
of likelihood function, provides a posterior distribution that is of the same family as the prior
distribution.
Thepriorandposteriorbothhavethesameprobabilitydistributionfamily,butwithdi(cid:27)ering
parameters.
Conjugate priors are extremely convenient from a calculation point of view as they provide
closed-form expressions for the posterior, thus negating any complex numerical integration.
In our case, if we use a Bernoulli likelihood function AND a beta distribution as the choice
of our prior, we immediately know that the posterior will also be a beta distribution.
Using a beta distribution for the prior in this manner means that we can carry out more
experimental coin (cid:29)ips and straightforwardly re(cid:28)ne our beliefs. The posterior will become the
new prior and we can use Bayes’ rule successively as new coin (cid:29)ips are generated.
If our prior belief is speci(cid:28)ed by a beta distribution and we have a Bernoulli likelihood
|     | function, then | our | posterior will | also be a beta | distribution. |     |
| --- | -------------- | --- | -------------- | -------------- | ------------- | --- |
Note however that a prior is only conjugate with respect to a particular likelihood function.

25
3.5.2 Why Is A Beta Prior Conjugate to the Bernoulli Likelihood?
We can actually use a simple calculation to prove why the choice of the beta distribution for the
prior, with a Bernoulli likelihood, gives a beta distribution for the posterior.
Asmentionedabove,theprobabilitydensityfunctionofabetadistribution,forourparticular
| parameter | θ, is | given | by: |                              |     |     |     |        |
| --------- | ----- | ----- | --- | ---------------------------- | --- | --- | --- | ------ |
|           |       |       |     | P(θ|α,β)=θα−1(1−θ)β−1/B(α,β) |     |     |     | (3.12) |
You can see that the form of the beta distribution is similar to the form of a Bernoulli
likelihood. In fact, if you multiply the two together (as in Bayes’ rule), you get:
|     |     | θα−1(1−θ)β−1/B(α,β)×θk(1−θ)1−k |     |     |     | ∝θα+k−1(1−θ)β+k |     | (3.13) |
| --- | --- | ------------------------------ | --- | --- | --- | --------------- | --- | ------ |
Notice that the term on the right hand side of the proportionality sign has the same form as
| our prior | (up to   | a normalising |      | constant). |        |       |     |     |
| --------- | -------- | ------------- | ---- | ---------- | ------ | ----- | --- | --- |
| 3.5.3     | Multiple |               | Ways | to Specify | a Beta | Prior |     |     |
At this stage we’ve discussed the fact that we want to use a beta distribution in order to specify
our prior beliefs about the fairness of the coin. However, we only have two parameters to play
| with, namely | α   | and | β.  |     |     |     |     |     |
| ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
How do these two parameters correspond to our more intuitive sense of "likely fairness" and
| "uncertainty | in  | fairness"? |     |     |     |     |     |     |
| ------------ | --- | ---------- | --- | --- | --- | --- | --- | --- |
Well,thesetwoconceptsneatlycorrespondtothemean andthevariance ofthebetadistribu-
α β
tion. Hence, if we can (cid:28)nd a relationship between these two values and the and parameters,
| we can more | easily | specify |          | our beliefs.   |     |     |     |     |
| ----------- | ------ | ------- | -------- | -------------- | --- | --- | --- | --- |
| It turns    | out    | that    | the mean | µ is given by: |     |     |     |     |
α
|     |     |     |     | µ=  |     |     |     | (3.14) |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ |
α+β
| While | the standard |     | deviation | σ is given | by: |     |     |     |
| ----- | ------------ | --- | --------- | ---------- | --- | --- | --- | --- |
(cid:115)
αβ
|     |     |     |     | σ = |     |     |     | (3.15) |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ |
(α+β)2(α+β+1)
Hence, all we need to do is re-arrange these formulae to provide α and β in terms of µ and
| σ. α is given | by: |     |     |          |     |          |     |     |
| ------------- | --- | --- | --- | -------- | --- | -------- | --- | --- |
|               |     |     |     | (cid:18) |     | (cid:19) |     |     |
1−µ 1
|     |     |     |     | α=  | −   | µ2  |     | (3.16) |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ |
σ2 µ
| While | β is | given | by: |     |     |     |     |     |
| ----- | ---- | ----- | --- | --- | --- | --- | --- | --- |
(cid:18) 1 (cid:19)
|     |     |     |     | β =α | −1  |     |     | (3.17) |
| --- | --- | --- | --- | ---- | --- | --- | --- | ------ |
µ
Note that we have to be careful here, as we should not specify a σ >0.289, since this is the
standard deviation of a uniform density (which itself implies no prior belief on any particular
| fairness | of the | coin). |     |     |     |     |     |     |
| -------- | ------ | ------ | --- | --- | --- | --- | --- | --- |
Let’s carry out an example now. Suppose I think the fairness of the coin is around 0.5, but
I’m not particularly certain (hence I have a wider standard deviation). I may specify a standard
| deviation | of around |     | 0.1. What | beta distribution | is  | produced | as a result? |     |
| --------- | --------- | --- | --------- | ----------------- | --- | -------- | ------------ | --- |
Plugging the numbers into the above formulae gives us α = 12 and β = 12 and the beta
| distribution | in  | this instance |     | is given in Figure | 3.2. |     |     |     |
| ------------ | --- | ------------- | --- | ------------------ | ---- | --- | --- | --- |
Notice how the peak is centred around 0.5 but that there is signi(cid:28)cant uncertainty in this
| belief, represented |     | by  | the width | of the curve. |     |     |     |     |
| ------------------- | --- | --- | --------- | ------------- | --- | --- | --- | --- |

26
|     |       | Figure |     | 3.2: A | beta distribution | with | α=12        | and β =12. |
| --- | ----- | ------ | --- | ------ | ----------------- | ---- | ----------- | ---------- |
| 3.6 | Using | Bayes’ |     | Rule   | to Calculate      |      | a Posterior |            |
We are (cid:28)nally in a position to be able to calculate our posterior beliefs using Bayes’ rule.
| Bayes’ | rule | in this | instance | is  | given by: |     |     |     |
| ------ | ---- | ------- | -------- | --- | --------- | --- | --- | --- |
P(θ|z,N)=P(z,N|θ)P(θ)/P(z,N) (3.18)
This says that the posterior belief in the fairness θ, given z heads in N (cid:29)ips, is equal to the
likelihood of seeing z heads in N (cid:29)ips, given a fairness θ, multiplied by our prior belief in θ,
| normalised | by  | the evidence. |     |     |     |     |     |     |
| ---------- | --- | ------------- | --- | --- | --- | --- | --- | --- |
Ifwesubstituteinthevaluesforthelikelihoodfunctioncalculatedabove, aswellasourprior
| belief beta | distribution, |          | we  | get:                  |     |     |     |     |
| ----------- | ------------- | -------- | --- | --------------------- | --- | --- | --- | --- |
|             |               | P(θ|z,N) |     | = P(z,N|θ)P(θ)/P(z,N) |     |     |     |     |
(3.19)
= θz(1−θ)N−zθα−1(1−θ)β−1/[B(α,β)P(z,N)]
(3.20)
|     |     |     |     | = θz+α−1(1−θ)N−z+β−1/B(z+α,N |     |     |     | −z+β) |
| --- | --- | --- | --- | ---------------------------- | --- | --- | --- | ----- |
(3.21)
The denominator function B(.,.) is known as the Beta function, which is the correct nor-
| malising | function | for | a beta | distribution, | as discussed | above. |     |     |
| -------- | -------- | --- | ------ | ------------- | ------------ | ------ | --- | --- |
|          |          |     |        | beta(θ|α,β)   |              |        | z   | N   |
If our prior is given by and we observe heads in (cid:29)ips subsequently,
| then | the | posterior | is  | given by | beta(θ|z+α,N | −z+β). |     |     |
| ---- | --- | --------- | --- | -------- | ------------ | ------ | --- | --- |
This is an incredibly straightforward (and useful!) updating rule. All we need do is specify
the mean µ and standard deviation σ of our prior beliefs, carry out N (cid:29)ips and observe the
z
number of heads and we automatically have a rule for how our beliefs should be updated.
As an example, suppose we consider the same prior beliefs as above for θ with µ = 0.5 and
| σ =0.1. | This | gave us | the prior | belief | distribution | of beta(θ|12,12). |     |     |
| ------- | ---- | ------- | --------- | ------ | ------------ | ----------------- | --- | --- |
Now suppose we observe N = 50 (cid:29)ips and z = 10 of them come up heads. How does this
| change | our belief | on    | the fairness | of   | the coin?     |      |              |         |
| ------ | ---------- | ----- | ------------ | ---- | ------------- | ---- | ------------ | ------- |
| We     | can plug   | these | numbers      | into | our posterior | beta | distribution | to get: |

27
|     | beta(θ|z+α,N | −z+β) | = beta(θ|10+12,50−10+12) | (3.22) |
| --- | ------------ | ----- | ------------------------ | ------ |
|     |              |       | = beta(θ|22,52)          | (3.23) |
The plots of the prior and posterior belief distributions are given in Figure 4.1. I have used
a blue dotted line for the prior belief and a green solid line for the posterior.
Figure 3.3: The prior and posterior belief distributions about the fairness θ.
Notice how the peak shifts dramatically to the left since we have only observed 10 heads in
50(cid:29)ips. Inaddition, noticehowthewidthofthepeakhasshrunk, whichisindicativeofthefact
that our belief in the certainty of the particular fairness value has also increased.
At this stage we can compute the mean and standard deviation of the posterior in order to
produce estimates for the fairness of the coin. In particular, the value of µ is given by:
post
α
|     |     | µ    | =   | (3.24) |
| --- | --- | ---- | --- | ------ |
|     |     | post | α+β |        |
22
|     |     |     | =   | (3.25) |
| --- | --- | --- | --- | ------ |
22+52
|     |     |     | = 0.297 | (3.26) |
| --- | --- | --- | ------- | ------ |
(3.27)
σ
| While the | standard deviation | post is given | by: |     |
| --------- | ------------------ | ------------- | --- | --- |
(cid:115)
αβ
|     | σ   | =   |     | (3.28) |
| --- | --- | --- | --- | ------ |
post (α+β)2(α+β+1)
(cid:115)
22×52
|     |     | =   |     | (3.29) |
| --- | --- | --- | --- | ------ |
(22+52)2(22+52+1)
= 0.053
(3.30)
In particular the mean has sifted to approximately 0.3, while the standard deviation (s.d.)
hashalvedtoapproximately0.05. Ameanofθ =0.3statesthatapproximately30%ofthetime,
the coin will come up heads, while 70% of the time it will come up tails. The s.d. of 0.05 means

28
that while we are more certain in this estimate than before, we are still somewhat uncertain
about this 30% value.
If we were to carry out more coin (cid:29)ips, the s.d. would reduce even further as α and β
continued to increase, representing our continued increase in certainty as more trials are carried
out.
Note in particular that we can use a posterior beta distribution as a prior distribution in a
new Bayesian updating procedure. This is another extremely useful bene(cid:28)t of using conjugate
priors to model our beliefs.

| Chapter |     | 4     |     |       |     |       |     |
| ------- | --- | ----- | --- | ----- | --- | ----- | --- |
| Markov  |     | Chain |     | Monte |     | Carlo |     |
In previous chapters we introduced Bayesian Statistics and considered how to infer a binomial
proportion using the concept of conjugate priors. We discussed the fact that not all models can
make use of conjugate priors and thus calculation of the posterior distribution would need to be
| approximated | numerically. |     |     |     |     |     |     |
| ------------ | ------------ | --- | --- | --- | --- | --- | --- |
In this chapter we introduce the main family of algorithms, known collectively as Markov
Chain Monte Carlo (MCMC), that allow us to approximate the posterior distribution as calcu-
lated by Bayes’ Theorem. In particular, we consider the Metropolis Algorithm, which is easily
stated and relatively straightforward to understand. It serves as a useful starting point when
learning about MCMC before delving into more sophisticated algorithms such as Metropolis-
| Hastings, | Gibbs | Samplers | and Hamiltonian | Monte | Carlo. |     |     |
| --------- | ----- | -------- | --------------- | ----- | ------ | --- | --- |
OncewehavedescribedhowMCMCworks,wewillcarryitoutusingtheopen-sourcePython-
basedPyMC3library, whichtakescareofmanyoftheunderlyingimplementationdetails, allow-
ing us to concentrate speci(cid:28)cally on modelling, rather than implementation details.
| 4.1 | Bayesian | Inference |     | Goals |     |     |     |
| --- | -------- | --------- | --- | ----- | --- | --- | --- |
OurgoalincarryingoutBayesianStatisticsistoproduce quantitative trading strategies based on
Bayesian models. However, in order to reach that goal we need to consider a reasonable amount
| of Bayesian | Statistics | theory. | So far | we have: |     |     |     |
| ----------- | ---------- | ------- | ------ | -------- | --- | --- | --- |
(cid:136)
IntroducedthephilosophyofBayesianStatistics, makinguseofBayes’Theoremtoupdate
| our | prior | beliefs on | probabilities | of outcomes | based | on new | data |
| --- | ----- | ---------- | ------------- | ----------- | ----- | ------ | ---- |
(cid:136)
Used conjugate priors as a means of simplifying computation of the posterior distribution
| in  | the case | of inference | on a | binomial proportion |     |     |     |
| --- | -------- | ------------ | ---- | ------------------- | --- | --- | --- |
In this chapter speci(cid:28)cally we are going to discuss MCMC as a means of computing the
| posterior | distribution | when | conjugate | priors are | not applicable. |     |     |
| --------- | ------------ | ---- | --------- | ---------- | --------------- | --- | --- |
SubsequenttoadiscussionontheMetropolisalgorithm,usingPyMC3,wewillconsidermore
sophisticated samplers and then apply them to more complex models. Ultimately, we will arrive
at the point where our models are useful enough to provide insight into asset returns prediction.
At that stage we will be able to begin building a trading model from our Bayesian analysis.
| 4.2 | Why | Markov | Chain | Monte | Carlo? |     |     |
| --- | --- | ------ | ----- | ----- | ------ | --- | --- |
In the previous chapter we saw that conjugate priors gave us a signi(cid:28)cant mathematical "short-
cut" to calculating the posterior distribution in Bayes’ Rule. A perfectly legitimate question at
this point would be to ask why we need MCMC at all if we can simply use conjugate priors.
The answer lies in the fact that not all models can be succinctly stated in terms of conjugate
priors. In particular, many more complicated modelling situations, particularly those related to
29

30
hierarchical models with hundreds of parameters, which we will consider in later chapters, are
| completely | intractable   | using | analytical | methods. |     |     |
| ---------- | ------------- | ----- | ---------- | -------- | --- | --- |
| If we      | recall Bayes’ | Rule: |            |          |     |     |
P(D|θ)P(θ)
|     |     |     | P(θ|D)= |     |     | (4.1) |
| --- | --- | --- | ------- | --- | --- | ----- |
P(D)
We can see that we need to calculate the evidence P(D). In order to achieve this we need to
evaluate the following integral, which integrates over all possible values of θ, the parameters:
(cid:90)
|     |     |     | P(D)= |     | P(D,θ)dθ | (4.2) |
| --- | --- | --- | ----- | --- | -------- | ----- |
Θ
The fundamental problem is that we are often unable to evaluate this integral analytically
| and so | we must | turn to a numerical |     | approximation | method instead. |     |
| ------ | ------- | ------------------- | --- | ------------- | --------------- | --- |
An additional problem is that our models might require a large number of parameters. This
means that our prior distributions could potentially have a large number of dimensions. This
in turn means that our posterior distributions will also be high dimensional. Hence, we are
in a situation where we have to numerically evaluate an integral in a potentially very large
| dimensional | space. |     |     |     |     |     |
| ----------- | ------ | --- | --- | --- | --- | --- |
This means we are in a situation often described as the Curse of Dimensionality. Informally,
this means that the volume of a high-dimensional space is so vast that any available data be-
comes extremely sparse within that space and hence leads to problems of statistical signi(cid:28)cance.
Practically, in order to gain any statistical signi(cid:28)cance, the volume of data needed must grow
| exponentially | with | the number | of dimensions. |     |     |     |
| ------------- | ---- | ---------- | -------------- | --- | --- | --- |
Such problems are often extremely di(cid:30)cult to tackle unless they are approached in an in-
telligent manner. The motivation behind Markov Chain Monte Carlo methods is that they
perform an intelligent search within a high dimensional space and thus Bayesian Models in high
| dimensions | become | tractable. |     |     |     |     |
| ---------- | ------ | ---------- | --- | --- | --- | --- |
The basic idea is to sample from the posterior distribution by combining a "random search"
(theMonteCarloaspect)withamechanismforintelligently"jumping"around,butinamanner
that ultimately doesn’t depend on where we started from (the Markov Chain aspect). Hence
Markov Chain Monte Carlo methods are memoryless searches performed with intelligent jumps.
As an aside, MCMC is not just for carrying out Bayesian Statistics. It is also widely used
in computational physics and computational biology as it can be applied generally to the approx-
| imation | of any high | dimensional | integral. |       |            |     |
| ------- | ----------- | ----------- | --------- | ----- | ---------- | --- |
| 4.2.1   | Markov      | Chain       | Monte     | Carlo | Algorithms |     |
Markov Chain Monte Carlo is a family of algorithms, rather than one particular method. In
this section we are going to concentrate on a particular method known as the Metropolis Algo-
rithm. In later sections we will consider Metropolis-Hastings, the Gibbs Sampler, Hamiltonian
MCMC and the No-U-Turn Sampler (NUTS). The latter is actually incorporated into PyMC3,
the software we’ll be using to numerically infer our binomial propoertion in this chapter.
| 4.3 | The Metropolis |     | Algorithm |     |     |     |
| --- | -------------- | --- | --------- | --- | --- | --- |
The (cid:28)rst MCMC algorithm considered in this chapter is due to Metropolis[36], which was devel-
oped in 1953. Hence it is not a recent method! While there have been substantial improvements
onMCMCsamplingalgorithmssince, itwillsu(cid:30)ceforthissection. Theintuitiongainedonthis
simpler method will help us understand more complex samplers in later sections and chapters.
The basic recipes for most MCMC algorithms tend to follow this pattern (see Davidson-
| Pilon[19] | for more | details): |     |     |     |     |
| --------- | -------- | --------- | --- | --- | --- | --- |
1. Begin the algorithm at the current position in parameter space (θ )
current

31
(θ
| 2. Propose |     | a "jump" | to a | new position | in parameter |     | space | new | )   |     |
| ---------- | --- | -------- | ---- | ------------ | ------------ | --- | ----- | --- | --- | --- |
3. Accept or reject the jump probabilistically using the prior information and available data
| 4. If | the jump | is accepted, |     | move to    | the new | position | and    | return  | to step 1 |     |
| ----- | -------- | ------------ | --- | ---------- | ------- | -------- | ------ | ------- | --------- | --- |
| 5. If | the jump | is rejected, |     | stay where | you are | and      | return | to step | 1         |     |
6. After a set number of jumps have occurred, return all of the accepted positions
The main di(cid:27)erence between MCMC algorithms occurs in how you jump as well as how you
| decide whether |     | to jump. |     |     |     |     |     |     |     |     |
| -------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
The Metropolis algorithm uses a normal distribution to propose a jump. This normal distri-
bution has a mean value µ which is equal to the current position and takes a "proposal width"
| for its standard |     | deviation | σ.  |     |     |     |     |     |     |     |
| ---------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
This proposal width is a parameter of the Metropolis algorithm and has a signi(cid:28)cant impact
onconvergence. Alargerproposalwidthwilljumpfurtherandcovermorespaceintheposterior
distribution, but might miss a region of higher probability initially. However, a smaller proposal
width won’t cover as much of the space as quickly and thus could take longer to converge.
A normal distribution is a good choice for such a proposal distribution (for continuous pa-
rameters) as, by de(cid:28)nition, it is more likely to select points nearer to the current position than
further away. However, it will occassionally choose points further away, allowing the space to be
explored.
Once the jump has been proposed, we need to decide (in a probabilistic manner) whether it
is a good move to jump to the new position. How do we do this? We calculate the ratio of the
proposal distribution of the new position and the proposal distribution at the current position
p:
| to determine |     | the probability |     | of moving, |       |         |     |     |     |       |
| ------------ | --- | --------------- | --- | ---------- | ----- | ------- | --- | --- | --- | ----- |
|              |     |                 |     | p=P(θ      | )/P(θ |         | )   |     |     | (4.3) |
|              |     |                 |     |            | new   | current |     |     |     |       |
Wethengenerateauniformrandomnumberontheinterval[0,1]. Ifthisnumberiscontained
| within the | interval | [0,p] | then | we accept | the move, | otherwise |     | we reject | it. |     |
| ---------- | -------- | ----- | ---- | --------- | --------- | --------- | --- | --------- | --- | --- |
While this is a relatively simple algorithm it isn’t immediately clear why this makes sense
and how it helps us avoid the intractable problem of calculating a high dimensional integral of
| the evidence, |     | P(D). |     |     |     |     |     |     |     |     |
| ------------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
As Thomas Wiecki[50] points out in his article on MCMC sampling, we’re actually dividing
the posterior of the proposed parameter by the posterior of the current parameter. Utilising
| Bayes’ Rule | this | eliminates | the | evidence, | P(D) | from | the ratio: |     |     |     |
| ----------- | ---- | ---------- | --- | --------- | ---- | ---- | ---------- | --- | --- | --- |
P(D|θnew)P(θnew)
|     |     | P(θ |D) |     |     | P(D) |     | P(D|θ |     | )P(θ ) |       |
| --- | --- | ------- | --- | --- | ---- | --- | ----- | --- | ------ | ----- |
|     |     | new     | =   |     |      | =   |       | new | new    | (4.4) |
P(D|θcurrent)P(θcurrent)
|     |     | P(θ current | |D) |     |     |     | P(D|θ | current | )P(θ current ) |     |
| --- | --- | ----------- | --- | --- | --- | --- | ----- | ------- | -------------- | --- |
P(D)
Therighthandsideofthelatterequalitycontainsonlythelikelihoodsandthepriors,bothof
whichwecancalculateeasily. Hencebydividingtheposterioratonepositionbytheposteriorat
another,we’resamplingregionsofhigherposteriorprobabilitymoreoftenthannot, inamanner
| which fully | re(cid:29)ects | the | probability | of  | the data. |     |     |     |     |     |
| ----------- | -------------- | --- | ----------- | --- | --------- | --- | --- | --- | --- | --- |
| 4.4         | Introducing    |     | PyMC3       |     |           |     |     |     |     |     |
PyMC3[] is a Python library (currently in beta) that carries out "Probabilistic Programming".
Thatis,wecande(cid:28)neaprobabilisticmodelandthencarryoutBayesianinferenceonthemodel,
usingvarious(cid:29)avoursofMarkovChainMonteCarlo. InthissenseitissimilartotheJAGS[]and
Stan[]packages. PyMC3hasalonglistofcontributorsandiscurrentlyunderactivedevelopment.
PyMC3 has been designed with a clean syntax that allows extremely straightforward model
speci(cid:28)cation, with minimal "boilerplate" code. There are classes for all major probability distri-
butions and it is easy to add more specialist distributions. It has a diverse and powerful suite

32
of MCMC sampling algorithms, including the Metropolis algorithm that we discussed above, as
well as the No-U-Turn Sampler (NUTS). This allows us to de(cid:28)ne complex models with many
| thousands | of parameters. |     |     |     |     |     |     |
| --------- | -------------- | --- | --- | --- | --- | --- | --- |
It also makes use of the Python Theano[] library, often used for highly CPU/GPU-intensive
Deep Learning applications, in order to maximise e(cid:30)ciency in execution speed.
In this chapter we will use PyMC3 to carry out a simple example of inferring a binomial
proportion,whichissu(cid:30)cienttoexpressthemainideas,withoutgettingboggeddowninMCMC
implementationspeci(cid:28)cs. InlaterchapterswewillexploremorefeaturesofPyMC3oncewecome
| to carry | out inference | on more | sophisticated | models.    |     |             |       |
| -------- | ------------- | ------- | ------------- | ---------- | --- | ----------- | ----- |
| 4.5      | Inferring     | a       | Binomial      | Proportion |     | with Markov | Chain |
|          | Monte         | Carlo   |               |            |     |             |       |
If you recall from the previous chapter on inferring a binomial proportion using conjugate priors
our goal was to estimate the fairness of a coin, by carrying out a sequence of coin (cid:29)ips.
The fairness of the coin is given by a parameter θ ∈[0,1] where θ =0.5 means a coin equally
| likely to | come up | heads or tails. |     |     |     |     |     |
| --------- | ------- | --------------- | --- | --- | --- | --- | --- |
Wediscussedthefactthatwecouldusearelatively(cid:29)exibleprobabilitydistribution,thebeta
distribution, to model our prior belief on the fairness of the coin. We also learnt that by using
a Bernoulli likelihood function to simulate virtual coin (cid:29)ips with a particular fairness, that our
posteriorbeliefwouldalsohavetheformofabetadistribution. Thisisanexampleofaconjugate
prior.
To be clear, this means we do not need to use MCMC to estimate the posterior in this
particular case as there is already an analytic closed-form solution. However, the majority of
Bayesian inference models do not admit a closed-form solution for the posterior, and hence it is
| necessary | to use MCMC | in  | these cases. |     |     |     |     |
| --------- | ----------- | --- | ------------ | --- | --- | --- | --- |
WearegoingtoapplyMCMCtoacasewherewealready"knowtheanswer", sothatwecan
comparetheresultsfromaclosed-formsolutionandonecalculatedbynumericalapproximation.
4.5.1 Inferring a Binonial Proportion with Conjugate Priors Recap
In the previous chapter we took a particular prior belief that the coin was likely to be fair, but
that we weren’t particularly certain. This translated as giving θ a mean µ=0.5 and a standard
| deviation | σ =0.1. |     |     |     |     |     |     |
| --------- | ------- | --- | --- | --- | --- | --- | --- |
Abetadistributionhastwoparameters,αandβ,thatcharacterisethe"shape"ofourbeliefs.
A mean µ=0.5 and s.d. σ =0.1 translate into α=12 and β =12 (see the previous chapter for
| details | on this transformation). |     |     |     |     |     |     |
| ------- | ------------------------ | --- | --- | --- | --- | --- | --- |
We then carried out 50 (cid:29)ips and observed 10 heads. When we plugged this into our closed-
formsolutionfortheposteriorbetadistribution,wereceivedaposteriorwithα=22andβ =52.
| Figure | 4.1, reproduced | from | the previous | chapter, | plots the | distributions: |     |
| ------ | --------------- | ---- | ------------ | -------- | --------- | -------------- | --- |
We can see that this intuitively makes sense, as the mass of probability has dramatically
shifted to nearer 0.2, which is the sample fairness from our (cid:29)ips. Notice also that the peak has
become narrower as we’re quite con(cid:28)dent in our results now, having carried out 50 (cid:29)ips.
| 4.5.2 | Inferring | a Binonial | Proportion |     | with | PyMC3 |     |
| ----- | --------- | ---------- | ---------- | --- | ---- | ----- | --- |
We’re now going to carry out the same analysis using the numerical Markov Chain Monte Carlo
method instead.
| Firstly, | we need | to install | PyMC3: |     |     |     |     |
| -------- | ------- | ---------- | ------ | --- | --- | --- | --- |
pip install --process-dependency-links git+https://github.com/pymc-devs/pymc3
Once installed, the next task is to import the necessary libraries, which include Matplotlib,
Numpy, Scipy and PyMC3 itself. We also set the graphical style of the Matplotlib output to be
| similar | to the ggplot2 | graphing | library | from the | R statistical | language: |     |
| ------- | -------------- | -------- | ------- | -------- | ------------- | --------- | --- |

33
Figure 4.1: The prior and posterior belief distributions about the fairness θ
| import | matplotlib.pyplot |     | as plt |     |
| ------ | ----------------- | --- | ------ | --- |
| import | numpy as          | np  |        |     |
import pymc3
| import | scipy.stats | as  | stats |     |
| ------ | ----------- | --- | ----- | --- |
plt.style.use("ggplot")
The next step is to set our prior parameters, as well as the number of coin (cid:29)ip trials carried
out and heads returned. We also specify, for completeness, the parameters of the analytically-
calculated posterior beta distribution, which we will use for comparison with our MCMC ap-
proach. In addition we specify that we want to carry out 100,000 iterations of the Metropolis
algorithm:
| # Parameter | values | for | prior and | analytic posterior |
| ----------- | ------ | --- | --------- | ------------------ |
n = 50
z = 10
| alpha | = 12 |     |     |     |
| ----- | ---- | --- | --- | --- |
beta = 12
| alpha_post | = 22 |     |     |     |
| ---------- | ---- | --- | --- | --- |
beta_post
= 52
| # How       | many iterations |     | of the Metropolis |     |
| ----------- | --------------- | --- | ----------------- | --- |
| # algorithm | to carry        | out | for MCMC          |     |
| iterations  | = 100000        |     |                   |     |
Now we actually de(cid:28)ne our beta distribution prior and Bernoulli likelihood model. PyMC3
has a very clean API for carrying this out. It uses a Python with context to assign all of
the parameters, step sizes and starting values to a pymc3.Model instance (which I have called
| basic_model, | as per | the PyMC3 | tutorial). |     |
| ------------ | ------ | --------- | ---------- | --- |
Firstly, we specify the parameter as a beta distribution, taking the prior and
theta alpha
beta values as parameters. Remember that our particular values of α=12 and β =12 imply a
| prior mean | µ=0.5 | and a prior | s.d. | σ =0.1. |
| ---------- | ----- | ----------- | ---- | ------- |
We then de(cid:28)ne the Bernoulli likelihood function, specifying the fairness parameter p=theta,
the number of trials n=n and the observed heads observed=z, all taken from the parameters
| speci(cid:28)ed | above. |     |     |     |
| --------------- | ------ | --- | --- | --- |
At this stage we can (cid:28)nd an optimal starting value for the Metropolis algorithm using the

34
PyMC3 Maximum A Posteriori (MAP) optimisation (we will go into detail about this in later
chapters). FinallywespecifytheMetropolissamplertobeusedandthenactuallysample(..)
| the         | results. | These | results       | are | stored  | in the  | trace | variable: |     |     |
| ----------- | -------- | ----- | ------------- | --- | ------- | ------- | ----- | --------- | --- | --- |
| # Use       | PyMC3    | to    | construct     |     | a model | context |       |           |     |     |
| basic_model |          | =     | pymc3.Model() |     |         |         |       |           |     |     |
basic_model:
with
|     | # Define |                       | our prior     |       | belief     | about         | the fairness |             |           |     |
| --- | -------- | --------------------- | ------------- | ----- | ---------- | ------------- | ------------ | ----------- | --------- | --- |
|     | # of     | the                   | coin          | using | a Beta     | distribution  |              |             |           |     |
|     | theta    | = pymc3.Beta("theta", |               |       |            | alpha=alpha,  |              | beta=beta)  |           |     |
|     | # Define |                       | the Bernoulli |       | likelihood |               | function     |             |           |     |
|     | y =      | pymc3.Binomial("y",   |               |       |            | n=n, p=theta, |              | observed=z) |           |     |
|     | # Carry  | out                   | the           | MCMC  | analysis   | using         | the          | Metropolis  | algorithm |     |
# Use Maximum A Posteriori (MAP) optimisation as initial value for MCMC
pymc3.find_MAP()
|     | start | =   |     |     |     |     |     |     |     |     |
| --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
# Use the Metropolis algorithm (as opposed to NUTS or HMC, etc.)
|     | step        | = pymc3.Metropolis() |     |       |        |                |     |                  |     |     |
| --- | ----------- | -------------------- | --- | ----- | ------ | -------------- | --- | ---------------- | --- | --- |
|     | # Calculate |                      | the | trace |        |                |     |                  |     |     |
|     | trace       | = pymc3.sample(      |     |       |        |                |     |                  |     |     |
|     | iterations, |                      |     | step, | start, | random_seed=1, |     | progressbar=True |     |     |
)
Notice how the speci(cid:28)cation of the model via the PyMC3 API is almost akin to the actual
mathematical speci(cid:28)cation of the model, with minimal "boilerplate" code. We will demonstrate
the power of this API in later chapters when we come to specify some more complex models.
Now that the model has been speci(cid:28)ed and sampled, we wish to plot the results. We cre-
ate a histogram from the trace (the list of all accepted samples) of the MCMC sampling us-
ing 50 bins. We then plot the analytic prior and posterior beta distributions using the SciPy
|     |     |     |     | method. | Finally, | we  | add some | labelling | to the graph | and display it: |
| --- | --- | --- | --- | ------- | -------- | --- | -------- | --------- | ------------ | --------------- |
stats.beta.pdf(..)
| # Plot | the | posterior |     | histogram |     | from | MCMC | analysis |     |     |
| ------ | --- | --------- | --- | --------- | --- | ---- | ---- | -------- | --- | --- |
bins=50
plt.hist(
|     | trace["theta"],  |     |     | bins,        |     |             |     |     |     |     |
| --- | ---------------- | --- | --- | ------------ | --- | ----------- | --- | --- | --- | --- |
|     | histtype="step", |     |     | normed=True, |     |             |     |     |     |     |
|     | label="Posterior |     |     | (MCMC)",     |     | color="red" |     |     |     |     |
)
| # Plot | the            | analytic |     | prior   | and | posterior | beta | distributions |     |     |
| ------ | -------------- | -------- | --- | ------- | --- | --------- | ---- | ------------- | --- | --- |
| x =    | np.linspace(0, |          |     | 1, 100) |     |           |      |               |     |     |
plt.plot(
|     | x, stats.beta.pdf(x, |                |     |     | alpha,       | beta), |     |     |     |     |
| --- | -------------------- | -------------- | --- | --- | ------------ | ------ | --- | --- | --- | --- |
|     | "--",                | label="Prior", |     |     | color="blue" |        |     |     |     |     |
)
plt.plot(
|     |     |     |     |     | alpha_post, |     | beta_post), |     |     |     |
| --- | --- | --- | --- | --- | ----------- | --- | ----------- | --- | --- | --- |
x, stats.beta.pdf(x,
|     | label=’Posterior |     |     | (Analytic)’, |     | color="green" |     |     |     |     |
| --- | ---------------- | --- | --- | ------------ | --- | ------------- | --- | --- | --- | --- |
)
| # Update                       |     | the | graph | labels |            |             |     |     |     |     |
| ------------------------------ | --- | --- | ----- | ------ | ---------- | ----------- | --- | --- | --- | --- |
| plt.legend(title="Parameters", |     |     |       |        |            | loc="best") |     |     |     |     |
| plt.xlabel("$\\theta$,         |     |     |       |        | Fairness") |             |     |     |     |     |
plt.ylabel("Density")
plt.show()

35
| When    | the code          | is executed | the following | output is given:  |               |     |
| ------- | ----------------- | ----------- | ------------- | ----------------- | ------------- | --- |
|         |                   |             |               | and               | theta_logodds |     |
| Applied | logodds-transform |             | to theta      | added transformed |               | to  |
model.
| [-----            |     | 14% |     | ] 14288 | of 100000 complete | in 0.5 sec |
| ----------------- | --- | --- | --- | ------- | ------------------ | ---------- |
| [----------       |     | 28% |     | ] 28857 | of 100000 complete | in 1.0 sec |
| [---------------- |     | 43% |     | ] 43444 | of 100000 complete | in 1.5 sec |
[-----------------58%-- ] 58052 of 100000 complete in 2.0 sec
[-----------------72%------- ] 72651 of 100000 complete in 2.5 sec
[-----------------87%------------- ] 87226 of 100000 complete in 3.0 sec
[-----------------100%-----------------] 100000 of 100000 complete in 3.4 sec
Clearly, the sampling time will depend upon the speed of your computer. The graphical
| output of | the analysis | is given | in Figure | 4.2: |     |     |
| --------- | ------------ | -------- | --------- | ---- | --- | --- |
Figure 4.2: Comparison of the analytic and MCMC-sampled posterior belief distributions about
| the fairness | θ, overlaid | with | the prior belief |     |     |     |
| ------------ | ----------- | ---- | ---------------- | --- | --- | --- |
In this particular case of a single-parameter model, with 100,000 samples, the convergence
of the Metropolis algorithm is extremely good. The histogram closely follows the analytically
calculated posterior distribution, as we’d expect. In a relatively simple model such as this we do
not need to compute 100,000 samples and far fewer would do. However, it does emphasise the
| convergence | of the | Metropolis | algorithm. |     |     |     |
| ----------- | ------ | ---------- | ---------- | --- | --- | --- |
We can also consider a concept known as the trace, which is the vector of samples produced
by the MCMC sampling procedure. We can use the helpful traceplot method to plot both a
kernel density estimate (KDE) of the histogram displayed above, as well as the trace.
The trace plot is extremely useful for assessing convergence of an MCMC algorithm and
whether we need to exclude a period of initial samples (known as the burn in). We will discuss
thetrace,burninandotherconvergenceissuesinlatersectionswhenwestudymoresophisticated
samplers. To output the trace we simply call traceplot with the trace variable:
| # Show | the trace | plot |     |     |     |     |
| ------ | --------- | ---- | --- | --- | --- | --- |
pymc3.traceplot(trace)
plt.show()
| The | full trace | plot is given | in Figure | 4.3: |     |     |
| --- | ---------- | ------------- | --------- | ---- | --- | --- |
Asyoucansee,theKDEestimateoftheposteriorbeliefinthefairnessre(cid:29)ectsbothourprior
belief of θ =0.5 and our data with a sample fairness of θ =0.2. In addition we can see that the

36
Figure 4.3: Trace plot of the MCMC sampling procedure for the fairness parameter θ
MCMC sampling procedure has "converged to the distribution" since the sampling series looks
stationary.
In more complicated cases, which we will examine in later sections, we will see that we need
to consider a "burn in" period as well as "thin" the results to remove autocorrelation, both of
| which will               | improve | convergence. |        |               |     |     |
| ------------------------ | ------- | ------------ | ------ | ------------- | --- | --- |
| For completeness,        |         | here         | is the | full listing: |     |     |
| import matplotlib.pyplot |         |              | as     | plt           |     |     |
| import numpy             | as      | np           |        |               |     |     |
import pymc3
| import scipy.stats |     |     | as stats |     |     |     |
| ------------------ | --- | --- | -------- | --- | --- | --- |
plt.style.use("ggplot")
| # Parameter | values |     | for prior | and analytic |     | posterior |
| ----------- | ------ | --- | --------- | ------------ | --- | --------- |
n = 50
z = 10
| alpha = | 12  |     |     |     |     |     |
| ------- | --- | --- | --- | --- | --- | --- |
beta = 12
| alpha_post | = 22 |     |     |     |     |     |
| ---------- | ---- | --- | --- | --- | --- | --- |
beta_post
= 52
| # How many  | iterations |               | of the  | Metropolis    |     |     |
| ----------- | ---------- | ------------- | ------- | ------------- | --- | --- |
| # algorithm | to         | carry         | out for | MCMC          |     |     |
| iterations  | = 100000   |               |         |               |     |     |
| # Use PyMC3 | to         | construct     | a       | model context |     |     |
| basic_model | =          | pymc3.Model() |         |               |     |     |
basic_model:
with
| # Define | our                   | prior | belief | about the    | fairness |            |
| -------- | --------------------- | ----- | ------ | ------------ | -------- | ---------- |
| # of     | the coin              | using | a Beta | distribution |          |            |
| theta    | = pymc3.Beta("theta", |       |        | alpha=alpha, |          | beta=beta) |

37
# Define the Bernoulli likelihood function
y = pymc3.Binomial("y", n=n, p=theta, observed=z)
# Carry out the MCMC analysis using the Metropolis algorithm
# Use Maximum A Posteriori (MAP) optimisation as initial value for MCMC
start = pymc3.find_MAP()
# Use the Metropolis algorithm (as opposed to NUTS or HMC, etc.)
step = pymc3.Metropolis()
# Calculate the trace
trace = pymc3.sample(
iterations, step, start, random_seed=1, progressbar=True
)
# Plot the posterior histogram from MCMC analysis
bins=50
plt.hist(
trace["theta"], bins,
histtype="step", normed=True,
label="Posterior (MCMC)", color="red"
)
# Plot the analytic prior and posterior beta distributions
x = np.linspace(0, 1, 100)
plt.plot(
x, stats.beta.pdf(x, alpha, beta),
"--", label="Prior", color="blue"
)
plt.plot(
x, stats.beta.pdf(x, alpha_post, beta_post),
label=’Posterior (Analytic)’, color="green"
)
# Update the graph labels
plt.legend(title="Parameters", loc="best")
plt.xlabel("$\\theta$, Fairness")
plt.ylabel("Density")
plt.show()
# Show the trace plot
pymc3.traceplot(trace)
plt.show()
4.6 Next Steps
At this stage we have a good understanding of the basics behind MCMC, as well as a speci(cid:28)c
method known as the Metropolis algorithm, as applied to inferring a binomial proportion.
However, as we discussed above, PyMC3 uses a much more sophisticated MCMC sampler
known as the No-U-Turn Sampler (NUTS). In order to gain an understanding of this sampler
we eventually need to consider further sampling techniques such as Metropolis-Hastings, Gibbs
Sampling and Hamiltonian Monte Carlo (on which NUTS is based).
WealsowanttostartapplyingProbabilisticProgrammingtechniquestomorecomplexmod-
els, such as hierarchical models. This in turn will help us produce sophisticated quantitative

38
trading strategies.
4.7 Bibliographic Note
ThealgorithmdescribedinthischapterisduetoMetropolis[36]. AnimprovementbyHastings[28]
led to the Metropolis-Hastings algorithm. The Gibbs sampler is due to Geman and Geman[24].
Gelfand and Smith[22] wrote a paper that was considered a major starting point for extensive
use of MCMC methods in the statistical community.
TheHamiltonianMonteCarloapproachisduetoDuaneetal[20]andtheNo-U-TurnSampler
(NUTS) is due to Ho(cid:27)man and Gelman[29]. Gelman et al[23] has an extensive discussion of
computional sampling mechanisms for Bayesian Statistics, including a detailed discussion on
MCMC. A gentle, mathematically intuitive, introduction to the Metropolis Algorithm is given
by Kruschke[34].
A very popular on-line introduction to Bayesian Statistics is by Cam Davidson-Pilon and
others[19], which has a fantastic chapter on MCMC (and PyMC3). Thomas Wiecki has also
written a great blog post[50] explaining the rationale for MCMC.
The PyMC3 project[2] also has some extremely useful documentation and some examples.

| Chapter  | 5   |        |            |     |     |
| -------- | --- | ------ | ---------- | --- | --- |
| Bayesian |     | Linear | Regression |     |     |
At this stage in our journey of Bayesian statistics we inferred a binomial proportion analytically
with conjugate priors and have described the basics of Markov Chain Monte Carlo via the
Metropolis algorithm. In this chapter we are going to introduce the basics of linear regression
modelling in the Bayesian framework and carry out inference using the PyMC3 MCMC library.
Wewillbeginbyrecappingtheclassical,orfrequentist,approachtomultiplelinearregression
(which will be discussed at length in the book part on Statistical Machine Learning in later
chapters). Then we will discuss how a Bayesian thinks of linear regression. We will brie(cid:29)y
describe the concept of a Generalised Linear Model (GLM), as this is necessary to understand
| the clean syntax | of model | descriptions | in PyMC3. |     |     |
| ---------------- | -------- | ------------ | --------- | --- | --- |
Subsequent to the description of these models we will simulate some linear data with noise
and then use PyMC3 to produce posterior distributions for the parameters of the model. This
is the same procedure that we will carry out when discussing time series models such as ARMA
and GARCH later on in the book. This "simulate and (cid:28)t" process not only helps us understand
the model, but also checks that we are (cid:28)tting it correctly when we know the "true" parameter
values.
Let’s now turn our attention to the frequentist approach to linear regression.
| 5.1 Frequentist |     | Linear | Regression |     |     |
| --------------- | --- | ------ | ---------- | --- | --- |
The frequentist, or classical, approach to multiple linear regression assumes a model of the
form[27]:
p
|     |     |        | (cid:88) +(cid:15)=βTX+(cid:15) |     |       |
| --- | --- | ------ | ------------------------------- | --- | ----- |
|     |     | f(X)=β | 0 + X j β j                     |     | (5.1) |
j=1
|     | βT  |     |     | N(0,σ2) |     |
| --- | --- | --- | --- | ------- | --- |
Where, is the transpose of the coe(cid:30)cient vector β and (cid:15) ∼ is the measurement
| error, normally | distributed | with mean | zero and standard | deviation σ. |     |
| --------------- | ----------- | --------- | ----------------- | ------------ | --- |
That is, our model f(X) is linear in the predictors, X, with some associated measurement
error.
If we have a set of training data (x ,y ),...,(x ,y ) then the goal is to estimate the β
|     |     |     | 1 1 N | N   |     |
| --- | --- | --- | ----- | --- | --- |
coe(cid:30)cients, which provide the best linear (cid:28)t to the data. Geometrically, this means we need to
(cid:28)nd the orientation of the hyperplane that best linearly characterises the data.
"Best"inthiscasemeansminimisingsomeformoferrorfunction. Themostpopularmethod
to do this is via ordinary least squares (OLS). If we de(cid:28)ne the residual sum of squares (RSS),
which is the sum of the squared di(cid:27)erences between the outputs and the linear regression esti-
mates:
39

40
N
|     |     |     |     |        |     | (cid:88) | ))2      |     |       |
| --- | --- | --- | --- | ------ | --- | -------- | -------- | --- | ----- |
|     |     |     |     | RSS(β) | =   | (y       | i −f(x i |     | (5.2) |
i=1
N
|     |     |     |     |     |     | (cid:88) | −βTx | )2  |       |
| --- | --- | --- | --- | --- | --- | -------- | ---- | --- | ----- |
|     |     |     |     |     | =   | (y       | i i  |     | (5.3) |
i=1
Then the goal of OLS is to minimise the RSS, via adjustment of the β coe(cid:30)cients. Although
we won’t derive it here (see Hastie et al[27] for details) the Maximum Likelihood Estimate of β,
| which minimises |     | the RSS, | is  | given | by: |     |     |     |     |
| --------------- | --- | -------- | --- | ----- | --- | --- | --- | --- | --- |
βˆ=(XTX)−1XTy
(5.4)
|     |     |     |     |     | y   |     |     | x   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
To make a subsequent prediction N+1 , given some new data N+1 , we simply multiply the
| components | of  | x by | the | associated | β coe(cid:30)cients |     | and obtain | y . |     |
| ---------- | --- | ---- | --- | ---------- | ------------------- | --- | ---------- | --- | --- |
|            |     | N+1  |     |            |                     |     |            | N+1 |     |
βˆ
The important point here is that is a point estimate. This means that it is a single value
Rp+1.
in In the Bayesian formulation we will see that the interpretation di(cid:27)ers substantially.
| 5.2 | Bayesian |     | Linear |     | Regression |     |     |     |     |
| --- | -------- | --- | ------ | --- | ---------- | --- | --- | --- | --- |
In a Bayesian framework, linear regression is stated in a probabilistic manner. That is, we
reformulate the above linear regression model to use probability distributions. The syntax for a
| linear regression |     | in a Bayesian |     | framework | looks   | like    | this:   |     |       |
| ----------------- | --- | ------------- | --- | --------- | ------- | ------- | ------- | --- | ----- |
|                   |     |               |     |           | (cid:0) |         | (cid:1) |     |       |
|                   |     |               |     |           | y∼N     | βTX,σ2I |         |     | (5.5) |
Inwords,ourresponsedatapointsyaresampledfromamultivariatenormaldistributionthat
coe(cid:30)cientsandthepredictors,X,andavarianceofσ2.
hasameanequaltotheproductoftheβ
Here, I refers to the identity matrix, which is necessary because the distribution is multivariate.
This is a very di(cid:27)erent formulation to the frequentist approach. In the frequentist setting
there is no mention of probability distributions for anything other than the measurement error.
IntheBayesianformulationtheentireproblemisrecastsuchthatthey
i valuesaresamplesfrom
| a normal | distribution. |     |     |     |     |     |     |     |     |
| -------- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
A common question at this stage is "What is the bene(cid:28)t of doing this?". What do we get
| out of this | reformulation? |     | There | are | two main | reasons | for doing | so[?]: |     |
| ----------- | -------------- | --- | ----- | --- | -------- | ------- | --------- | ------ | --- |
(cid:136)
Prior Distributions: If we have any prior knowledge about the parameters β, then we
can choose prior distributions that re(cid:29)ect this. If we don’t, then we can still choose non-
| informative |     | priors. |     |     |     |     |     |     |     |
| ----------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
(cid:136)
Posterior Distributions: I mentioned above that the frequentist MLE value for our
βˆ
regression coe(cid:30)cients, , was only a single point estimate. In the Bayesian formulation we
receiveanentireprobabilitydistributionthatcharacterisesouruncertaintyonthedi(cid:27)erent
β coe(cid:30)cients. The immediate bene(cid:28)t of this is that after taking into account any data
we can quantify our uncertainty in the β parameters via the variance of this posterior
| distribution. |     | A larger | variance |     | indicates | more | uncertainty. |     |     |
| ------------- | --- | -------- | -------- | --- | --------- | ---- | ------------ | --- | --- |
While the above formula for the Bayesian approach may appear succinct, it doesn’t really
give us much clue as to how to specify a model and sample from it using Markov Chain Monte
Carlo. In the next few sections we will use PyMC3 to formulate and utilise a Bayesian linear
| regression | model. |     |     |     |     |     |     |     |     |
| ---------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |

41
| 5.3 | Bayesian | Linear |     | Regression | with | PyMC3 |     |
| --- | -------- | ------ | --- | ---------- | ---- | ----- | --- |
In this section we are going to carry out a time-honoured approach to statistical examples,
namely to simulate some data with properties that we know, and then (cid:28)t a model to recover
these original properties. I have used this technique many times in the past on QuantStart.com
| and in later | chapters | on time | series | analysis. |     |     |     |
| ------------ | -------- | ------- | ------ | --------- | --- | --- | --- |
While it may seem contrived to go through such a procedure, there are in fact two major
bene(cid:28)ts. The (cid:28)rst is that it helps us understand exactly how to (cid:28)t the model. In order to do so,
we have to understand it (cid:28)rst. Thus it helps us gain intuition into how the model works. The
second reason is that it allows us to see how the model performs (i.e. the values and uncertainty
it returns) in a situation where we actually know the true values trying to be estimated.
Our approach will make use of numpy and pandas to simulate the data, use seaborn to plot
it, and ultimately use the Generalised Linear Models (GLM) module of PyMC3 to formulate a
| Bayesian | linear regression |             | and sample | from   | it, on our simulated | data | set. |
| -------- | ----------------- | ----------- | ---------- | ------ | -------------------- | ---- | ---- |
| 5.3.1    | What are          | Generalised |            | Linear | Models?              |      |      |
Before we begin discussing Bayesian linear regression, I want to brie(cid:29)y outline the concept of a
Generalised Linear Model (GLM), as we’ll be using these to formulate our model in PyMC3.
A Generalised Linear Model is a (cid:29)exible mechanism for extending ordinary linear regression
to more general forms of regression, including logistic regression (classi(cid:28)cation) and Poisson
| regression | (used for | count | data), as | well as linear | regression | itself. |     |
| ---------- | --------- | ----- | --------- | -------------- | ---------- | ------- | --- |
<P>GLMs allow for response variables that have error distributions other than the nor-
mal distribution (see (cid:15) above, in the frequentist section). The linear model is related to the
response/outcome, y, via a "link function", and is assumed to be generated from a statistical
distribution from the exponential distribution family. This family of distributions encompasses
many common distributions including the normal, gamma, beta, chi-squared, Bernoulli, Poisson
and others.
| The | mean of this | distribution, |     | µ depends | on X via the following |     | relation: |
| --- | ------------ | ------------- | --- | --------- | ---------------------- | --- | --------- |
E(y)=µ=g−1(Xβ) (5.6)
Where g is the link function. The variance is often some function, V, of the mean:
Var(y)=V(E(y))=V(g−1(Xβ))
(5.7)
Inthefrequentistsetting,aswithordinarylinearregressionabove,theunknownβ coe(cid:30)cients
| are estimated | via a | maximum | likelihood | approach. |     |     |     |
| ------------- | ----- | ------- | ---------- | --------- | --- | --- | --- |
I’m not going to discuss GLMs in depth here as they are not the focus of the chapter (or
the book). We are interested in them because we will be using the glm module from PyMC3,
which was written by Thomas Wiecki[50] and others, in order to easily specify our Bayesian
linear regression.
| 5.3.2 | Simulating | Data | and | Fitting | the Model | with | PyMC3 |
| ----- | ---------- | ---- | --- | ------- | --------- | ---- | ----- |
Before we utilise PyMC3 to specify and sample a Bayesian model, we need to simulate some
noisy linear data. The following snippet carries this out (this is modi(cid:28)ed and extended from
| Jonathan                  | Sedar’s post[?]): |     |                  |     |     |     |     |
| ------------------------- | ----------------- | --- | ---------------- | --- | --- | --- | --- |
| import                    | numpy as          | np  |                  |     |     |     |     |
| import                    | pandas as         | pd  |                  |     |     |     |     |
| import                    | seaborn as        | sns |                  |     |     |     |     |
| sns.set(style="darkgrid", |                   |     | palette="muted") |     |     |     |     |

42
| def simulate_linear_data(N, |     |     |     |     | beta_0, | beta_1, | eps_sigma_sq): |     |     |
| --------------------------- | --- | --- | --- | --- | ------- | ------- | -------------- | --- | --- |
"""
| Simulate |        | a         | random | dataset | using       | a noisy |     |     |     |
| -------- | ------ | --------- | ------ | ------- | ----------- | ------- | --- | --- | --- |
| linear   |        | process.  |        |         |             |         |     |     |     |
| N:       | Number | of        | data   | points  | to simulate |         |     |     |     |
| beta_0:  |        | Intercept |        |         |             |         |     |     |     |
beta_1:
|     |     | Slope | of  | univariate | predictor, |     | X   |     |     |
| --- | --- | ----- | --- | ---------- | ---------- | --- | --- | --- | --- |
"""
| #   | Create      | a             | pandas  | DataFrame | with           | column | ’x’ | containing |     |
| --- | ----------- | ------------- | ------- | --------- | -------------- | ------ | --- | ---------- | --- |
| #   | N uniformly |               | sampled |           | values between |        | 0.0 | and 1.0    |     |
| df  | =           | pd.DataFrame( |         |           |                |        |     |            |     |
{"x":
np.random.RandomState(42).choice(
map(
|     |     |     |     | lambda | x: float(x)/100.0, |     |     |     |     |
| --- | --- | --- | --- | ------ | ------------------ | --- | --- | --- | --- |
np.arange(100)
|     |     |     | ), N, | replace=False |     |     |     |     |     |
| --- | --- | --- | ----- | ------------- | --- | --- | --- | --- | --- |
)
}
)
|          |           |          |               |                | beta_0       | beta_1*x |                                   |            |     |
| -------- | --------- | -------- | ------------- | -------------- | ------------ | -------- | --------------------------------- | ---------- | --- |
| #        | Use       | a linear | model         | (y             | ~            | +        |                                   | + epsilon) | to  |
| #        | generate  |          | a column      | ’y’            | of responses |          | based                             | on ’x’     |     |
| eps_mean |           | =        | 0.0           |                |              |          |                                   |            |     |
|          |           | beta_0   |               | beta_1*df["x"] |              |          |                                   |            |     |
| df["y"]  |           | =        |               | +              |              | +        | np.random.RandomState(42).normal( |            |     |
|          | eps_mean, |          | eps_sigma_sq, |                | N            |          |                                   |            |     |
)
| return      |     | df  |             |     |     |     |     |     |     |
| ----------- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- |
| if __name__ |     |     | "__main__": |     |     |     |     |     |     |
==
| #      | These | are   | our | "true"    | parameters |     |     |     |     |
| ------ | ----- | ----- | --- | --------- | ---------- | --- | --- | --- | --- |
| beta_0 |       | = 1.0 | #   | Intercept |            |     |     |     |     |
beta_1
|                   |          | = 2.0                   | #            | Slope   |             |            |         |               |     |
| ----------------- | -------- | ----------------------- | ------------ | ------- | ----------- | ---------- | ------- | ------------- | --- |
| #                 | Simulate |                         | 100 data     | points, | with        | a variance |         | of 0.5        |     |
| N                 | = 100    |                         |              |         |             |            |         |               |     |
| eps_sigma_sq      |          |                         | = 0.5        |         |             |            |         |               |     |
| #                 | Simulate |                         | the "linear" |         | data using  | the        | above   | parameters    |     |
| df                | =        | simulate_linear_data(N, |              |         | beta_0,     |            | beta_1, | eps_sigma_sq) |     |
| #                 | Plot     | the                     | data,        | and a   | frequentist | linear     |         | regression    | fit |
| #                 | using    | the                     | seaborn      | package |             |            |         |               |     |
| sns.lmplot(x="x", |          |                         |              | y="y",  | data=df,    | size=10)   |         |               |     |
| plt.xlim(0.0,     |          |                         | 1.0)         |         |             |            |         |               |     |
| The               | output   | is                      | given in     | Figure  | 5.1:        |            |         |               |     |
We’ve simulated 100 datapoints, with an intercept β =1 and a slope of β =2. The epsilon
|     |     |     |     |     |     |     |     | 0   | 1   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
values are normally distributed with a mean of zero and variance σ2 = 1. The data has been
2
plottedusingthesns.lmplotmethod. Inaddition,themethodusesafrequentistMLEapproach
| to (cid:28)t | a linear | regression |     | line to | the data. |     |     |     |     |
| ------------ | -------- | ---------- | --- | ------- | --------- | --- | --- | --- | --- |
Now that we have carried out the simulation we want to (cid:28)t a Bayesian linear regression to
the data. This is where the glm module comes in. It uses a model speci(cid:28)cation syntax that is

43
Figure 5.1: Simulation of noisy linear data via Numpy, pandas and seaborn
similar to how R speci(cid:28)es models. To achieve this we make implicit use of the Patsy library.
InthefollowingsnippetwearegoingtoimportPyMC3,utilisethewithcontextmanager,as
described in the previous chapter on MCMC and then specify the model using the glm module.
Wearethengoingto(cid:28)ndthemaximum a posteriori (MAP)estimatefortheMCMCsampler
to begin from. Finally, we are going to use the No-U-Turn Sampler[29] to carry out the actual
inference and then plot the trace of the model, discarding the (cid:28)rst 500 samples as "burn in":
glm_mcmc_inference(df,
| def |     |     | iterations=5000): |     |     |     |
| --- | --- | --- | ----------------- | --- | --- | --- |
"""
| Calculates    | the      | Markov     | Chain         | Monte    | Carlo    | trace of     |
| ------------- | -------- | ---------- | ------------- | -------- | -------- | ------------ |
| a Generalised |          | Linear     | Model         | Bayesian | linear   | regression   |
| model on      | supplied | data.      |               |          |          |              |
| df: DataFrame |          | containing |               | the data |          |              |
| iterations:   | Number   |            | of iterations |          | to carry | out MCMC for |
"""
| # Use PyMC3 | to  | construct |     | a model | context |     |
| ----------- | --- | --------- | --- | ------- | ------- | --- |
basic_model
= pm.Model()
with basic_model:
| # Create | the   | glm    | using        | the | Patsy model | syntax     |
| -------- | ----- | ------ | ------------ | --- | ----------- | ---------- |
| # We     | use a | Normal | distribution |     | for the     | likelihood |

44
|     | pm.glm.glm("y |             |               | ~ x",        | df,     | family=pm.glm.families.Normal()) |     |     |     |
| --- | ------------- | ----------- | ------------- | ------------ | ------- | -------------------------------- | --- | --- | --- |
|     | #             | Use Maximum |               | A Posteriori |         | (MAP) optimisation               |     |     |     |
|     | #             | as initial  |               | value        | for     | MCMC                             |     |     |     |
|     | start         | =           | pm.find_MAP() |              |         |                                  |     |     |     |
|     | #             | Use the     | No-U-Turn     |              | Sampler |                                  |     |     |     |
step = pm.NUTS()
|     | #     | Calculate       |            | the trace |                  |     |     |     |     |
| --- | ----- | --------------- | ---------- | --------- | ---------------- | --- | --- | --- | --- |
|     | trace | =               | pm.sample( |           |                  |     |     |     |     |
|     |       | iterations,     |            | step,     | start,           |     |     |     |     |
|     |       | random_seed=42, |            |           | progressbar=True |     |     |     |     |
)
| return |     | trace |     |     |     |     |     |     |     |
| ------ | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
...
...
| if __name__ |     | ==  | "__main__": |     |     |     |     |     |     |
| ----------- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- |
...
...
glm_mcmc_inference(df,
| trace |     | =   |     |     |     | iterations=5000) |     |     |     |
| ----- | --- | --- | --- | --- | --- | ---------------- | --- | --- | --- |
pm.traceplot(trace[500:])
plt.show()
| The | output | of  | the script | is  | as follows: |     |     |     |     |
| --- | ------ | --- | ---------- | --- | ----------- | --- | --- | --- | --- |
Applied log-transform to sd and added transformed sd_log to model.
| [----      |     |     | 11% |     |     | ] 563  | of 5000 | complete | in 0.5 sec |
| ---------- | --- | --- | --- | --- | --- | ------ | ------- | -------- | ---------- |
| [--------- |     |     | 24% |     |     | ] 1207 | of 5000 | complete | in 1.0 sec |
in
| [--------------           |     |     | 37% |     |     | ] 1875 | of 5000 | complete | 1.5 sec    |
| ------------------------- | --- | --- | --- | --- | --- | ------ | ------- | -------- | ---------- |
| [-----------------51%     |     |     |     |     |     | ] 2561 | of 5000 | complete | in 2.0 sec |
| [-----------------64%---- |     |     |     |     |     | ] 3228 | of 5000 | complete | in 2.5 sec |
[-----------------78%--------- ] 3920 of 5000 complete in 3.0 sec
[-----------------91%-------------- ] 4595 of 5000 complete in 3.5 sec
[-----------------100%-----------------] 5000 of 5000 complete in 3.8 sec
| The | traceplot |     | is given | in Figure | 5.2: |     |     |     |     |
| --- | --------- | --- | -------- | --------- | ---- | --- | --- | --- | --- |
We covered the basics of traceplots in the previous chapter. Recall that Bayesian models
provide a full posterior probability distribution for each of the model parameters, as opposed to
| a frequentist |     | point | estimate. |     |     |     |     |     |     |
| ------------- | --- | ----- | --------- | --- | --- | --- | --- | --- | --- |
On the left side of the panel we can see marginal distributions for each parameter of interest.
Notice that the intercept β 0 distribution has its mode/maximum posterior estimate almost ex-
actly at 1, close to the true parameter of β =1. The estimate for the slope β parameter has a
|     |     |     |     |     |     | 0   |     |     | 1   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
mode at approximately 1.98, close to the true parameter value of β =2. The (cid:15) error parameter
1
associated with the model measurement noise has a mode of approximately 0.465, which is a
| little | o(cid:27) compared |     | to the | true | value of | (cid:15)=0.5. |     |     |     |
| ------ | ------------------ | --- | ------ | ---- | -------- | ------------- | --- | --- | --- |
In all cases there is a reasonable variance associated with each marginal posterior, telling us
that there is some degree of uncertainty in each of the values. Were we to simulate more data,
| and carry | out | more | samples, | this | variance | would likely | decrease. |     |     |
| --------- | --- | ---- | -------- | ---- | -------- | ------------ | --------- | --- | --- |
The key point here is that we do not receive a single point estimate for a regression line, i.e.
"alineofbest(cid:28)t",asinthefrequentistcase. Insteadwereceiveadistribution oflikelyregression
lines.
Wecanplottheselinesusingamethodoftheglmlibrarycalledplot_posterior_predictive.
The method takes a trace object and the number of lines to plot (samples).

45
Figure 5.2: Using PyMC3 to (cid:28)t a Bayesian GLM linear regression model to simulated data
fit_reg
Firstly we use the seaborn lmplot method, this time with the parameter set to
False to stop the frequentist regression line being drawn. Then we plot 100 sampled posterior
predictive regression lines. Finally, we plot the "true" regression line using the original β = 1
0
| and β 1 | =2 parameters. | The code snippet | below produces |     | such a plot: |
| ------- | -------------- | ---------------- | -------------- | --- | ------------ |
..
..
| __name__ | "__main__": |     |     |     |     |
| -------- | ----------- | --- | --- | --- | --- |
| if       | ==          |     |     |     |     |
..
..
| #   | Plot a sample | of posterior | regression | lines |     |
| --- | ------------- | ------------ | ---------- | ----- | --- |
fit_reg=False)
| sns.lmplot(x="x", |     | y="y", data=df, | size=10, |     |     |
| ----------------- | --- | --------------- | -------- | --- | --- |
| plt.xlim(0.0,     |     | 1.0)            |          |     |     |
| plt.ylim(0.0,     |     | 4.0)            |          |     |     |
pm.glm.plot_posterior_predictive(trace,
samples=100)
| x   | = np.linspace(0, | 1, N)    |     |     |     |
| --- | ---------------- | -------- | --- | --- | --- |
|     | beta_0           | beta_1*x |     |     |     |
| y   | = +              |          |     |     |     |
plt.plot(x, y, label="True Regression Line", lw=3., c="green")
plt.legend(loc=0)
plt.show()
| We  | can see the sampled | range of | posterior regression | lines | in Figure 5.3: |
| --- | ------------------- | -------- | -------------------- | ----- | -------------- |
The main takeaway here is that there is uncertainty in the location of the regression line as
sampled by the Bayesian model. However, it can be seen that the range is relatively narrow and
that the set of samples is not too dissimilar to the "true" regression line itself.
| 5.4 | Next Steps |     |     |     |     |
| --- | ---------- | --- | --- | --- | --- |
Thenextstepistobegindiscussionofrobustregression andhierarchicallinearmodels,apowerful
modelling technique made tractable by rapid MCMC implementations. From a quantitative

46
Figure 5.3: Using PyMC3 GLM module to show a set of sampled posterior regression lines
(cid:28)nance point of view we will also take a look at a stochastic volatility model using PyMC3 and
| see how | we can use    | this model to form | trading algorithms. |     |
| ------- | ------------- | ------------------ | ------------------- | --- |
| 5.5     | Bibliographic | Note               |                     |     |
AnintroductiontofrequentistlinearregressioncanbefoundinJamesetal[32]. Amoretechnical
overview, including subset selection methods, can be found in Hastie et al[27]. Gelman et al[23]
| discuss | Bayesian linear | models in depth | at a reasonably | technical level. |
| ------- | --------------- | --------------- | --------------- | ---------------- |
This chapter is in(cid:29)uenced from previous blog posts by Thomas Wiecki[50] including his
discussion of Bayesian GLMs[48, 49] as well as Jonathan Sedar with his posts on Bayesian
| Inference | with PyMC3[44].   |        |     |     |
| --------- | ----------------- | ------ | --- | --- |
| 5.6       | Full Code         |        |     |     |
| import    | matplotlib.pyplot | as plt |     |     |
| import    | numpy as np       |        |     |     |
| import    | pandas as         | pd     |     |     |
| import    | pymc3 as pm       |        |     |     |
| import    | seaborn as        | sns    |     |     |

47
| sns.set(style="darkgrid", |     |     | palette="muted") |         |         |                |     |     |
| ------------------------- | --- | --- | ---------------- | ------- | ------- | -------------- | --- | --- |
| simulate_linear_data(N,   |     |     |                  | beta_0, | beta_1, | eps_sigma_sq): |     |     |
def
"""
| Simulate | a random | dataset |     | using | a noisy |     |     |     |
| -------- | -------- | ------- | --- | ----- | ------- | --- | --- | --- |
linear process.
| N: Number | of  | data points |     | to simulate |     |     |     |     |
| --------- | --- | ----------- | --- | ----------- | --- | --- | --- | --- |
beta_0:
Intercept
| beta_1: | Slope | of univariate |     | predictor, |     | X   |     |     |
| ------- | ----- | ------------- | --- | ---------- | --- | --- | --- | --- |
"""
| # Create      | a pandas | DataFrame |        | with    | column | ’x’ | containing |     |
| ------------- | -------- | --------- | ------ | ------- | ------ | --- | ---------- | --- |
| # N uniformly |          | sampled   | values | between |        | 0.0 | and 1.0    |     |
df = pd.DataFrame(
{"x":
np.random.RandomState(42).choice(
map(
|     |     | lambda | x:  | float(x)/100.0, |     |     |     |     |
| --- | --- | ------ | --- | --------------- | --- | --- | --- | --- |
np.arange(N)
|     |     | ), N, replace=False |     |     |     |     |     |     |
| --- | --- | ------------------- | --- | --- | --- | --- | --- | --- |
)
}
)
| # Use a    | linear | model  | (y  | ~ beta_0     | + beta_1*x |       | + epsilon) | to  |
| ---------- | ------ | ------ | --- | ------------ | ---------- | ----- | ---------- | --- |
| # generate | a      | column | ’y’ | of responses |            | based | on ’x’     |     |
| eps_mean   | = 0.0  |        |     |              |            |       |            |     |
df["y"] = beta_0 + beta_1*df["x"] + np.random.RandomState(42).normal(
| eps_mean, |     | eps_sigma_sq, |     |     |     |     |     |     |
| --------- | --- | ------------- | --- | --- | --- | --- | --- | --- |
N
)
return df
| def glm_mcmc_inference(df, |     |     | iterations=5000): |     |     |     |     |     |
| -------------------------- | --- | --- | ----------------- | --- | --- | --- | --- | --- |
"""
| Calculates    | the      | Markov     | Chain         | Monte    | Carlo | trace  | of           |     |
| ------------- | -------- | ---------- | ------------- | -------- | ----- | ------ | ------------ | --- |
| a Generalised |          | Linear     | Model         | Bayesian |       | linear | regression   |     |
| model on      | supplied | data.      |               |          |       |        |              |     |
| df: DataFrame |          | containing |               | the data |       |        |              |     |
| iterations:   |          | Number     | of iterations |          | to    | carry  | out MCMC for |     |
"""
| # Use PyMC3 |     | to construct |     | a model | context |     |     |     |
| ----------- | --- | ------------ | --- | ------- | ------- | --- | --- | --- |
| basic_model |     | = pm.Model() |     |         |         |     |     |     |
with basic_model:
| # Create      |         | the glm       | using        | the                                  | Patsy | model        | syntax     |     |
| ------------- | ------- | ------------- | ------------ | ------------------------------------ | ----- | ------------ | ---------- | --- |
| # We          | use     | a Normal      | distribution |                                      | for   | the          | likelihood |     |
| pm.glm.glm("y |         | ~             | x",          | df, family=pm.glm.families.Normal()) |       |              |            |     |
| # Use         | Maximum | A             | Posteriori   |                                      | (MAP) | optimisation |            |     |
| # as          | initial | value         | for          | MCMC                                 |       |              |            |     |
| start         | =       | pm.find_MAP() |              |                                      |       |              |            |     |

48
# Use the No-U-Turn Sampler
step = pm.NUTS()
# Calculate the trace
trace = pm.sample(
iterations, step, start,
random_seed=42, progressbar=True
)
return trace
if __name__ == "__main__":
# These are our "true" parameters
beta_0 = 1.0 # Intercept
beta_1 = 2.0 # Slope
# Simulate 100 data points, with a variance of 0.5
N = 200
eps_sigma_sq = 0.5
# Simulate the "linear" data using the above parameters
df = simulate_linear_data(N, beta_0, beta_1, eps_sigma_sq)
# Plot the data, and a frequentist linear regression fit
# using the seaborn package
sns.lmplot(x="x", y="y", data=df, size=10)
plt.xlim(0.0, 1.0)
trace = glm_mcmc_inference(df, iterations=5000)
pm.traceplot(trace[500:])
plt.show()
# Plot a sample of posterior regression lines
sns.lmplot(x="x", y="y", data=df, size=10, fit_reg=False)
plt.xlim(0.0, 1.0)
plt.ylim(0.0, 4.0)
pm.glm.plot_posterior_predictive(trace, samples=100)
x = np.linspace(0, 1, N)
y = beta_0 + beta_1*x
plt.plot(x, y, label="True Regression Line", lw=3., c="green")
plt.legend(loc=0)
plt.show()

|      | Part   | III      |
| ---- | ------ | -------- |
| Time | Series | Analysis |
49

| Chapter      | 6   |     |     |      |     |        |          |
| ------------ | --- | --- | --- | ---- | --- | ------ | -------- |
| Introduction |     |     | to  | Time |     | Series | Analysis |
Inthischapterwearegoingtointroducemethodsfromthe(cid:28)eldoftime series analysis. These
techniquesareextremelyimportantinquantitative(cid:28)nanceasthevastmajorityofassetmodelling
in the (cid:28)nancial industry still makes extensive use of these statistical models.
We will now examine what time series analysis is, outline its scope and learn how we can
apply the techniques to various frequencies of (cid:28)nancial data in order to predict future values or
infer relationships, ultimately allowing us to develop quantitative trading strategies.
| 6.1 What | is  | Time | Series | Analysis? |     |     |     |
| -------- | --- | ---- | ------ | --------- | --- | --- | --- |
Firstly, a time series is de(cid:28)ned as some quantity that is measured sequentially in time over
some interval.
In its broadest form, time series analysis is about inferring what has happened to a series of
data points in the past and attempting to predict what will happen to it in the future.
However, we are going to take a quantitative statistical approach to time series, by assuming
that our time series are realisations of sequences of random variables. That is, we are going to
assumethatthereissomeunderlyinggeneratingprocessforourtimeseriesbasedononeormore
| statistical distributions |     | from which | these | variables | are | drawn. |     |
| ------------------------- | --- | ---------- | ----- | --------- | --- | ------ | --- |
Time series analysis attempts to understand the past and predict the future.
Such a sequence of random variables is known as a discrete-time stochastic process
(DTSP). In quantitative trading we are concerned with attempting to (cid:28)t statistical models to
these DTSPs to infer underlying relationships between series or predict future values in order to
| generate trading | signals. |     |     |     |     |     |     |
| ---------------- | -------- | --- | --- | --- | --- | --- | --- |
Time series in general, including those outside of the (cid:28)nancial world, often contain the fol-
lowing features:
(cid:136)
Trends - A trend is a consistent directional movement in a time series. These trends
will either be deterministic or stochastic. The former allows us to provide an underlying
rationale for the trend, while the latter is a random feature of a series that we will be
unlikelytoexplain. Trendsoftenappearin(cid:28)nancialseries,particularlycommoditiesprices,
and many Commodity Trading Advisor (CTA) funds use sophisticated trend identi(cid:28)cation
| models in | their trading | algorithms. |     |     |     |     |     |
| --------- | ------------- | ----------- | --- | --- | --- | --- | --- |
(cid:136) Seasonal Variation - Many time series contain seasonal variation. This is particularly
true in series representing business sales or climate levels. In quantitative (cid:28)nance we often
see seasonal variation in commodities, particularly those related to growing seasons or
| annual temperature |     | variation | (such | as natural |     | gas). |     |
| ------------------ | --- | --------- | ----- | ---------- | --- | ----- | --- |
(cid:136) SerialDependence-Oneofthemostimportantcharacteristicsoftimeseries,particularly
(cid:28)nancialseries,isthatofserial correlation. Thisoccurswhentimeseriesobservationsthat
are close together in time tend to be correlated. Volatility clustering is one aspect of serial
| correlation | that | is particularly | important |     | in quantitative | trading. |     |
| ----------- | ---- | --------------- | --------- | --- | --------------- | -------- | --- |
51

52
| 6.2 How | Can      | We  | Apply | Time |     | Series | Analysis |     | in Quantita- |
| ------- | -------- | --- | ----- | ---- | --- | ------ | -------- | --- | ------------ |
| tive    | Finance? |     |       |      |     |        |          |     |              |
Our goal as quantitative researchers is to identify trends, seasonal variations and correlation
using statistical time series methods, and ultimately generate trading signals or (cid:28)lters based on
| inference or | predictions. |         |     |     |     |     |     |     |     |
| ------------ | ------------ | ------- | --- | --- | --- | --- | --- | --- | --- |
| Our approach |              | will be | to: |     |     |     |     |     |     |
(cid:136)
Forecast and Predict Future Values - In order to trade successfully we will need to
| accurately | forecast |     | future asset | prices, | at least | in  | a statistical | sense. |     |
| ---------- | -------- | --- | ------------ | ------- | -------- | --- | ------------- | ------ | --- |
(cid:136)
SimulateSeries-Onceweidentifystatisticalpropertiesof(cid:28)nancialtimeserieswecanuse
them to generate simulations of future scenarios. This allows us to estimate the number of
trades, the expected trading costs, the expected returns pro(cid:28)le, the technical and (cid:28)nancial
investment required in infrastructure, and thus ultimately the risk pro(cid:28)le and pro(cid:28)tability
| of a particular |     | strategy | or portfolio. |     |     |     |     |     |     |
| --------------- | --- | -------- | ------------- | --- | --- | --- | --- | --- | --- |
(cid:136)
Infer Relationships - Identi(cid:28)cation of relationships between time series and other quan-
titative values allows us to enhance our trading signals through (cid:28)ltration mechanisms. For
example, if we can infer how the spread in a foreign exchange pair varies with bid/ask
volume, then we can (cid:28)lter any prospective trades that may occur in a period where we
| forecast | a wide | spread | in order | to reduce | transaction |     | costs. |     |     |
| -------- | ------ | ------ | -------- | --------- | ----------- | --- | ------ | --- | --- |
In addition we can apply standard (classical/frequentist or Bayesian) statistical tests to our
timeseriesmodelsinordertojustifycertainbehaviours,suchasregimechangeinequitymarkets.
| 6.3 Time |     | Series | Analysis |     | Software |     |     |     |     |
| -------- | --- | ------ | -------- | --- | -------- | --- | --- | --- | --- |
In my two previous books we made exclusive use of C++ and Python for our trading strategy
implementationandsimulation. Bothoftheselanguagesare"(cid:28)rstclassenvironments"forwriting
an entire trading stack. They contain many libraries and allow an end-to-end construction of a
| trading system | solely | within | that | language. |     |     |     |     |     |
| -------------- | ------ | ------ | ---- | --------- | --- | --- | --- | --- | --- |
Unfortunately, C++ and Python do not possess extensive statistical libraries. This is one of
theirshortcomings. ForthisreasonwewillbeusingtheR statistical environmentasameans
of carrying out time series research. R is well-suited for the job due to the availability of time
series libraries, statistical methods and straightforward plotting capabilities.
We will learn R in a problem-solving fashion, whereby new commands and syntax will be
introduced as needed. Fortunately, there are plenty of extremely useful tutorials for R availabile
on the internet and I will point them out as we go through the sequence of time series analysis
chapters.
| 6.4 Time |     | Series | Analysis |     | Roadmap |     |     |     |     |
| -------- | --- | ------ | -------- | --- | ------- | --- | --- | --- | --- |
We have previously discussed Bayesian statistics and that it will form the basis of many of our
time series and machine learning models. Eventually we will utilise Bayesian tools and machine
learning techniques in conjunction with the following time series methods in order to forecast
price level and direction, act as (cid:28)lters and determine "regime change", that is, determine when
| our time series | have | changed | their | underlying | statistical |     | behaviour. |     |     |
| --------------- | ---- | ------- | ----- | ---------- | ----------- | --- | ---------- | --- | --- |
Our time series roadmap is as follows. Each of the topics below will form its own chapter.
Oncewe’veexaminedthesemethodsindepth,wewillbeinapositiontocreatesomesophisticated
modern models for examining high-frequency data across di(cid:27)erent markets.
(cid:136) Time Series Introduction - This chapter outlines the area of time series analysis, its
| scope | and how | it can | be applied | to (cid:28)nancial |     | data. |     |     |     |
| ----- | ------- | ------ | ---------- | ------------------ | --- | ----- | --- | --- | --- |

53
(cid:136)
Serial Correlation - An absolutely fundamental aspect of modeling time series is the
concept of serial correlation. We will de(cid:28)ne it, visualise it and outline how it can be used
to (cid:28)t time series models.
(cid:136)
Random Walks and White Noise - In this chapter we will look at two basic time
series models that will form the basis of the more complicated linear and conditional het-
eroskedastic models of later chapters.
(cid:136)
ARMA Models - We will consider linear autoregressive, moving average and combined
autoregressive moving average models as our (cid:28)rst attempt at predicting asset price move-
ments.
(cid:136)
ARIMA and GARCH Models - We will extend the ARMA model to use di(cid:27)erencing
and thus allowing them to be "integrated", leading to the ARIMA model. We will also
discuss non-stationary conditional heteroskedastic (volatility clustering) models.
(cid:136)
Multivariate Modeling-WehaveconsideredmultivariatemodelsinSuccessful Algorith-
mic Trading, namely when we considered mean-reverting pairs of equities. In this chapter
we will more rigourously de(cid:28)ne cointegration and look at further tests for it. We will also
consider vector autoregressive (VAR) models [not to be confused with Value-at-Risk!].
(cid:136)
State-Space Models - State Space Modelling borrows a long history of modern control
theory used in engineering in order to allow us to model time series with rapidly varying
parameters(suchastheβ slopevariablebetweentwocointegratedassetsinalinearregres-
sion). In particular, we will consider the famous Kalman Filter and the Hidden Markov
Model. This will be one of the major uses of Bayesian analysis in time series.
(cid:136)
Market Microstructure - We will consider high frequency trading and examine market
microstructuree(cid:27)ectsindetail, laterapplyingourknowledgetohigh-frequencyforexdata.
6.5 How Does This Relate to Other Statistical Tools?
My goal with QuantStart has always been to try and outline the mathematical and statistical
framework for quantitative analysis and quantitative trading, from the basics through to the
more advanced modern techniques.
In previous books we have spent the majority of the time on introductory and intermediate
techniques. However,wearenowgoingtoturnourattentiontowardsrecentadvancedtechniques
used in quantitative (cid:28)rms.
Thiswillnotonlyhelpthosewhowishtogainacareerintheindustry,butitwillalsogivethe
quantitative retail traders among you a much broader toolkit of methods, as well as a unifying
approach to trading.
Having worked full-time in the industry previously, and now as a consultant to funds, I
can state with certainty that a substantial fraction of quantitative fund professionals use very
sophisticated techniques to "hunt for alpha".
However, many of these (cid:28)rms are so large that they are not interested in "capacity con-
strained" strategies, i.e. those that aren’t scalable above 1-2million USD. As retailers, if we
can apply a sophisticated trading framework to these areas, coupled with a robust portfolio
management system and brokerage link, we can achieve pro(cid:28)tability over the long term.
We will eventually combine our chapters on time series analysis with the Bayesian approach
to hypothesis testing and model selection, along with optimised R and Python code, to produce
non-linear, non-stationary time series models that can trade at high-frequency.
The next chapter will discuss serial correlation and why it is one of the most fundamental
aspects of time series analysis.

54

| Chapter |     | 7           |     |     |     |     |
| ------- | --- | ----------- | --- | --- | --- | --- |
| Serial  |     | Correlation |     |     |     |     |
Inthepreviouschapterweconsideredhowtimeseriesanalysismodelscouldbeusedtoeventually
allow us create trading strategies. In this chapter we are going to look at one of the most
important aspects of time series, namely serial correlation (also known as autocorrelation).
Before we dive into the de(cid:28)nition of serial correlation we will discuss the broad purpose of
| time series | modelling | and | why we’re | interested |     | in serial correlation. |
| ----------- | --------- | --- | --------- | ---------- | --- | ---------------------- |
Whenwearegivenoneormore(cid:28)nancialtimeseriesweareprimarilyinterestedinforecasting
or simulating data. It is relatively straightforward to identify deterministic trends as well as
seasonal variation and decompose a series into these components. However, once such a time
| series has | been decomposed |     | we are | left with | a   | random component. |
| ---------- | --------------- | --- | ------ | --------- | --- | ----------------- |
Sometimes such a time series can be well modelled by independent random variables. How-
ever,therearemanysituations,particularlyin(cid:28)nance,whereconsecutiveelementsofthisrandom
componenttimeserieswillpossesscorrelation. Thatis,thebehaviourofsequentialpointsinthe
remaining series a(cid:27)ect each other in a dependent manner. One major example occurs in mean-
reverting pairs trading. Mean-reversion shows up as correlation between sequential variables in
time series.
Our task as quantitative modellers is to try and identify the structure of these correlations,
as they will allow us to markedly improve our forecasts and thus the potential pro(cid:28)tability
of a strategy. In addition identifying the correlation structure will improve the realism of any
simulated timeseriesbasedonthemodel. Thisisextremelyusefulforimprovingthee(cid:27)ectiveness
| of risk management |     | components |     | of the strategy |     | implementation. |
| ------------------ | --- | ---------- | --- | --------------- | --- | --------------- |
When sequential observations of a time series are correlated in the manner described above
we say that serial correlation (or autocorrelation) exists in the time series.
Now that we have outlined the usefulness of studying serial correlation we need to de(cid:28)ne it
in a rigourous mathematical manner. Before we can do that we must build on simpler concepts,
| including        | expectation |     | and variance. |     |     |            |
| ---------------- | ----------- | --- | ------------- | --- | --- | ---------- |
| 7.1 Expectation, |             |     | Variance      |     | and | Covariance |
Many of these de(cid:28)nitions will be familiar if you have a background in statistics or probability,
but they will be outlined here speci(cid:28)cally for purposes of consistent notation.
| The (cid:28)rst | de(cid:28)nition | is  | that of | the expected |     | value or expectation: |
| --------------- | ---------------- | --- | ------- | ------------ | --- | --------------------- |
De(cid:28)nition 7.1.1. Expectation. The expected value or expectation, E(x), of a random variable
x is its mean average value in the population. We denote the expectation of x by µ, such that
E(x)=µ.
Now that we have the de(cid:28)nition of expectation we can de(cid:28)ne the variance, which charac-
| terises the | "spread" | of a | random | variable: |     |     |
| ----------- | -------- | ---- | ------ | --------- | --- | --- |
De(cid:28)nition7.1.2. Variance. Thevariance ofarandomvariableistheexpectationofthesquared
| deviations | of the | variable | from the | mean, | denoted | by σ2(x)=E[(x−µ)2]. |
| ---------- | ------ | -------- | -------- | ----- | ------- | ------------------- |
55

56
Notice that the variance is always non-negative. This allows us to de(cid:28)ne the standard devia-
tion:
De(cid:28)nition 7.1.3. Standard Deviation. The standard deviation of a random variable x, σ(x), is
x.
| the square | root of the | variance |     | of  |     |     |     |
| ---------- | ----------- | -------- | --- | --- | --- | --- | --- |
Nowthatwe’veoutlinedtheseelementarystatisticalde(cid:28)nitionswecangeneralisethevariance
to the concept of covariance between two random variables. Covariance tells us how linearly
| related | these two variables |     | are: |     |     |     |     |
| ------- | ------------------- | --- | ---- | --- | --- | --- | --- |
De(cid:28)nition 7.1.4. Covariance. The covariance of two random variables x and y, each having
respective expectations µ and µ , is given by σ(x,y)=E[(x−µ )(y−µ )].
|            |       |     | x       | y         |      | x y       |     |
| ---------- | ----- | --- | ------- | --------- | ---- | --------- | --- |
| Covariance | tells | us  | how two | variables | move | together. |     |
Howeversinceweareinastatisticalsituationwedonothaveaccesstothepopulationmeans
µ andµ . Insteadwemustestimate thecovariancefromasample. Forthisweusetherespective
x y
| sample | means x¯ and | y¯. |     |     |     |     |     |
| ------ | ------------ | --- | --- | --- | --- | --- | --- |
Ifweconsiderasetofnpairsofelementsofrandomvariablesfromxandy, givenby(x ,y ),
i i
the sample covariance, Cov(x,y) (also sometimes denoted by q(x,y)) is given by:
|     |     |     |     |     | 1   | n   |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
(cid:88)
|     |     |     | Cov(x,y)= |     |     | (x i −x¯)(y i −y¯) | (7.1) |
| --- | --- | --- | --------- | --- | --- | ------------------ | ----- |
n−1
i=1
Note: You may be wondering why we divide by n−1 in the denominator, rather than n. This
is a valid question! The reason we choose n−1 is that it makes Cov(x,y) an unbiased estimator.
| 7.1.1 | Example: | Sample |     | Covariance |     | in R |     |
| ----- | -------- | ------ | --- | ---------- | --- | ---- | --- |
This is actually our (cid:28)rst usage of R in the book. We have previously discussed the installation
procedure, so you can refer back to the introductory chapter if you need to install R. Assuming
| you have | R installed | you | can open | up the | R terminal. |     |     |
| -------- | ----------- | --- | -------- | ------ | ----------- | --- | --- |
In the following commands we are going to simulate two vectors of length 100, each with a
linearly increasing sequence of integers with some normally distributed noise added. Thus we
| are constructing | linearly |     | associated | variables |     | by design. |     |
| ---------------- | -------- | --- | ---------- | --------- | --- | ---------- | --- |
We will (cid:28)rstly construct a scatter plot and then calculate the sample covariance using the
cor function. In order to ensure you see exactly the same data as I do, we will set a random
| seed of | 1 and 2 respectively |     | for | each variable: |     |     |     |
| ------- | -------------------- | --- | --- | -------------- | --- | --- | --- |
> set.seed(1)
| > x <- | seq(1,100) | +   | 20.0*rnorm(1:100) |     |     |     |     |
| ------ | ---------- | --- | ----------------- | --- | --- | --- | --- |
> set.seed(2)
| > y <- | seq(1,100) | +   | 20.0*rnorm(1:100) |     |     |     |     |
| ------ | ---------- | --- | ----------------- | --- | --- | --- | --- |
> plot(x,y)
| The | plot is given | in Figure | 7.1. |     |     |     |     |
| --- | ------------- | --------- | ---- | --- | --- | --- | --- |
There is a relatively clear association between the two variables. We can now calculate the
sample covariance:
> cov(x,y)
[1] 681.6859
| The | sample covariance |     | is given | as 681.6859. |     |     |     |
| --- | ----------------- | --- | -------- | ------------ | --- | --- | --- |
One drawback of using the covariance to estimate linear association between two random
variables is that it is a dimensional measure. That is, it isn’t normalised by the spread of the
data and thus it is hard to draw comparisons between datasets with large di(cid:27)erences in spread.
| This motivates | another | concept, |     | namely | correlation. |     |     |
| -------------- | ------- | -------- | --- | ------ | ------------ | --- | --- |

57
Figure 7.1: Scatter plot of two linearly increasing variables with normally distributed noise.
7.2 Correlation
Correlation is a dimensionless measure of how two variables vary together, or "co-vary". In
essence, itisthecovarianceoftworandomvariablesnormalisedbytheirrespectivespreads. The
| (population) | correlation |     | between | two    | variables | is often denoted | by ρ(x,y): |
| ------------ | ----------- | --- | ------- | ------ | --------- | ---------------- | ---------- |
|              |             |     |         | E[(x−µ | )(y−µ     | )] σ(x,y)        |            |
|              |             |     | ρ(x,y)= |        | x         | y =              |            |
(7.2)
|     |     |     |     |     | σ σ |     | σ σ |
| --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     | x   | y   | x y |
The denominator product of the two spreads will constrain the correlation to lie within the
interval [−1,1]:
| (cid:136)               |     |             | ρ(x,y)=+1 |                  |            |              |                    |
| ----------------------- | --- | ----------- | --------- | ---------------- | ---------- | ------------ | ------------------ |
| A correlation           |     | of          |           | indicates        | exact      | positive     | linear association |
| (cid:136)               |     |             | ρ(x,y)=0  |                  |            |              |                    |
| A correlation           |     | of          |           | indicates        | no linear  | association  | at all             |
| (cid:136) A correlation |     | of          | ρ(x,y)=−1 | indicates        | exact      | negative     | linear association |
| As with                 | the | covariance, | we        | can de(cid:28)ne | the sample | correlation, | Cor(x,y):          |
Cov(x,y)
Cor(x,y)= (7.3)
sd(x)sd(y)

58
|     | Cov(x,y) |     |     |     |     | x   | y,  | sd(x) |
| --- | -------- | --- | --- | --- | --- | --- | --- | ----- |
Where is the sample covariance of and while is the sample standard
| deviation | of x.    |     |        |             |     |     |      |     |
| --------- | -------- | --- | ------ | ----------- | --- | --- | ---- | --- |
| 7.2.1     | Example: |     | Sample | Correlation |     |     | in R |     |
Wewillusethesamexandyvectorsofthepreviousexample. ThefollowingRcodewillcalculate
| the sample | correlation: |     |     |     |     |     |     |     |
| ---------- | ------------ | --- | --- | --- | --- | --- | --- | --- |
> cor(x,y)
[1] 0.5796604
The sample correlation is given as 0.5796604 showing a reasonably strong positive linear
| association | between      |     | the two vectors, | as   | expected. |     |     |     |
| ----------- | ------------ | --- | ---------------- | ---- | --------- | --- | --- | --- |
| 7.3         | Stationarity |     | in               | Time | Series    |     |     |     |
Nowthatwehaveoutlinedthede(cid:28)nitionsofexpectation,variance,standarddeviation,covariance
and correlation we are in a position to discuss how they apply to time series data.
Firstly, we will discuss a concept known as stationarity. This is an extremely important
aspect of time series and much of the analysis carried out on (cid:28)nancial time series data will
concern stationarity. Once we have discussed stationarity we are in a position to talk about
| serial | correlation |     | and construct | some | correlogram |     | plots. |     |
| ------ | ----------- | --- | ------------- | ---- | ----------- | --- | ------ | --- |
We will begin by trying to apply the above de(cid:28)nitions to time series data, starting with the
mean/expectation:
De(cid:28)nition 7.3.1. Mean of a Time Series. The mean of a time series x , µ(t), is given as the
t
| expectation | E(x | )=µ(t). |     |     |     |     |     |     |
| ----------- | --- | ------- | --- | --- | --- | --- | --- | --- |
t
| There | are | two important | points | to  | note about |     | this de(cid:28)nition: |     |
| ----- | --- | ------------- | ------ | --- | ---------- | --- | ---------------------- | --- |
(cid:136) µ=µ(t),
|     |     | i.e. the | mean (in | general) | is a | function | of time. |     |
| --- | --- | -------- | -------- | -------- | ---- | -------- | -------- | --- |
(cid:136) This expectation is taken across the ensemble population of all the possible time series
that could have been generated under the time series model. In particular, it is NOT the
| expression |     | (x  | +x +...+x | )/k | (more | on this | below). |     |
| ---------- | --- | --- | --------- | --- | ----- | ------- | ------- | --- |
|            |     | 1   | 2         | k   |       |         |         |     |
Thisde(cid:28)nitionisusefulwhenweareabletogeneratemanyrealisationsofatimeseriesmodel.
However in real life this is usually not the case! We are "stuck" with only one past history and
as such we will often only have access to a single historical time series for a particular asset or
situation.
So how do we proceed if we wish to estimate the mean, given that we don’t have access to
these hypothetical realisations from the ensemble? Well, there are two options:
(cid:136)
| Simply | estimate |     | the mean | at each | point | using | the observed | value. |
| ------ | -------- | --- | -------- | ------- | ----- | ----- | ------------ | ------ |
(cid:136)
Decomposethetimeseriestoremoveanydeterministictrendsorseasonalitye(cid:27)ects, giving
a residual series. Once we have this series we can make the assumption that the residual
seriesisstationary in the mean,i.e. thatµ(t)=µ,a(cid:28)xedvalueindependentoftime. It
then becomes possible to estimate this constant population mean using the sample mean
(cid:80)n
| x¯= |     | xt. |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
t=1 n
µ(t)=µ,
De(cid:28)nition 7.3.2. Stationary in the Mean. A time series is stationary in the mean if
a constant.
Now that we’ve seen how we can discuss expectation values we can use this to (cid:29)esh out the
de(cid:28)nitionofvariance. Onceagainwemakethesimplifyingassumptionthatthetimeseriesunder
consideration is stationary in the mean. With that assumption we can de(cid:28)ne the variance:
De(cid:28)nition 7.3.3. Variance of a Time Series. The variance σ2(t) of a time series model that is
| stationary | in the | mean | is given | by σ2(t)=E[(x |     | −µ)2]. |     |     |
| ---------- | ------ | ---- | -------- | ------------- | --- | ------ | --- | --- |
t

59
Thisisastraightforwardextensionofthevariancede(cid:28)nedaboveforrandomvariables,except
that σ2(t) is a function of time. Importantly, you can see how the de(cid:28)nition strongly relies on
the fact that the time series is stationary in the mean (i.e. that µ is not time-dependent).
You might notice that this de(cid:28)nition leads to a tricky situation. If the variance itself varies
with time how are we supposed to estimate it from a single time series? As before, the presence
of the expectation operator E(..) requires an ensemble of time series and yet we will often only
have one!
Once again, we simplify the situation by making an assumption. In particular, and as with
the mean, we assume a constant population variance, denoted σ2, which is not a function of
time. Once we have made this assumption we are in a position to estimate its value using the
sample variance de(cid:28)nition above:
(cid:80) (x −x¯)2
Var(x)= t (7.4)
n−1
Noteforthistoworkweneedtobeabletoestimatethesamplemean,x¯. Inaddition,aswith
thesamplecovariancede(cid:28)nedabove, wemustusen−1inthedenominatorinordertomakethe
sample variance an unbiased estimator.
De(cid:28)nition 7.3.4. Stationary in the Variance. A time series is stationary in the variance if
σ2(t)=σ2, a constant.
This is where we need to be careful! With time series we are in a situation where sequential
observations may be correlated. This will have the e(cid:27)ect of biasing the estimator, i.e. over- or
under-estimating the true population variance.
Thiswillbeparticularlyproblematicintimeserieswhereweareshortondataandthusonly
have a small number of observations. In a high correlation series, such observations will be close
to each other and thus will lead to bias.
Inpractice,andparticularlyinhigh-frequency(cid:28)nance,weareofteninasituationofhavinga
substantialnumberofobservations. Thedrawbackisthatweoftencannotassumethat(cid:28)nancial
series are truly stationary in the mean or stationary in the variance.
As we make progress with the section in the book on time series, and develop more sophisti-
cated models, we will address these issues in order to improve our forecasts and simulations.
We are now in a position to apply our time series de(cid:28)nitions of mean and variance to that of
serial correlation.
7.4 Serial Correlation
The essence of serial correlation is that we wish to see how sequential observations in a time
series a(cid:27)ect each other. If we can (cid:28)nd structure in these observations then it will likely help
us improve our forecasts and simulation accuracy. This will lead to greater pro(cid:28)tability in our
trading strategies or better risk management approaches.
Firstly,anotherde(cid:28)nition. Ifweassume,asabove,thatwehaveatimeseriesthatisstationary
in the mean andstationary in the variance thenwecantalkaboutsecond order stationarity:
De(cid:28)nition 7.4.1. Second Order Stationary. A time series is second order stationary if the
correlation between sequential observations is only a function of the lag, that is, the number of
time steps separating each sequential observation.
Finally, we are in a position to de(cid:28)ne serial covariance and serial correlation!
De(cid:28)nition 7.4.2. Autocovariance of a Time Series. If a time series model is second order
stationary then the (population) serial covariance or autocovariance, of lag k, C = E[(x −
k t
µ)(x −µ)].
t+k
The autocovariance C is not a function of time. This is because it involves an expectation
k
E(..),which,asbefore,istakenacrossthepopulationensembleofpossibletimeseriesrealisations.
This means it is the same for all times t.

60
As before this motivates the de(cid:28)nition of serial correlation or autocorrelation, simply by
dividing through by the square of the spread of the series. This is possible because the time
| series is | stationary | in the | variance | and | thus | σ2(t)=σ2: |     |     |     |
| --------- | ---------- | ------ | -------- | --- | ---- | --------- | --- | --- | --- |
De(cid:28)nition 7.4.3. AutocorrelationofaTimeSeries. Theserialcorrelationor autocorrelation
of lag k, ρ , of a second order stationary time series is given by the autocovariance of the series
k
C
| normalised | by  | the product | of  | the spread. | That | is, ρ | k = k. |     |     |
| ---------- | --- | ----------- | --- | ----------- | ---- | ----- | ------ | --- | --- |
σ2
µ)2]
Note that ρ = C 0 = E[(x t− = σ 2 = 1. That is, the (cid:28)rst lag of k = 0 will always give a
|     |     | 0 σ2 | σ   | 2   | σ 2 |     |     |     |     |
| --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
value of unity.
As with the above de(cid:28)nitions of covariance and correlation, we can de(cid:28)ne the sample auto-
covariance and sample autocorrelation. In particular, we denote the sample autocovariance with
a lower-case c to di(cid:27)erentiate between the population value given by an upper-case C.
| The | sample | autocovariance |     | function |     | c is given | by: |     |     |
| --- | ------ | -------------- | --- | -------- | --- | ---------- | --- | --- | --- |
k
n−k
1 (cid:88)
|     |     |     |     | c = | (x  | −x¯)(x | −x¯) |     | (7.5) |
| --- | --- | --- | --- | --- | --- | ------ | ---- | --- | ----- |
|     |     |     |     | k   | n   | t      | t+k  |     |       |
t=1
| The | sample | autocorrelation |     | function |     | r is given | by: |     |     |
| --- | ------ | --------------- | --- | -------- | --- | ---------- | --- | --- | --- |
k
c
|     |     |     |     |     | r   | = k |     |     | (7.6) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
k
c 0
Now that we have de(cid:28)ned the sample autocorrelation function we are in a position to de(cid:28)ne
| and plot | the correlogram, |             | an  | essential | tool | in time | series analysis. |     |     |
| -------- | ---------------- | ----------- | --- | --------- | ---- | ------- | ---------------- | --- | --- |
| 7.5      | The              | Correlogram |     |           |      |         |                  |     |     |
A correlogram is simply a plot of the autocorrelation function for sequential values of lag
| k =0,1,...,n. | It  | allows | us to | see the | correlation | structure | in  | each lag. |     |
| ------------- | --- | ------ | ----- | ------- | ----------- | --------- | --- | --------- | --- |
The main usage of correlograms is to detect any autocorrelation subsequent to the removal
| of any deterministic |     | trends | or  | seasonality | e(cid:27)ects. |     |     |     |     |
| -------------------- | --- | ------ | --- | ----------- | -------------- | --- | --- | --- | --- |
If we have (cid:28)tted a time series model then the correlogram helps us justify that this model is
well (cid:28)tted or whether we need to further re(cid:28)ne it to remove any additional autocorrelation.
Here is an example correlogram, plotted in R using the acf function, for a sequence of
normallydistributedrandomvariables. ThefullRcodeisasfollowsandisplottedinFigure7.2.
> set.seed(1)
> w <- rnorm(100)
> acf(w)
| There | are a | few notable | features |     | of the correlogram |     | plot | in R: |     |
| ----- | ----- | ----------- | -------- | --- | ------------------ | --- | ---- | ----- | --- |
(cid:136)
Firstly, since the sample correlation of lag k = 0 is given by r = c 0 = 1 we will always
0 c
have a line of height equal to unity at lag k =0 on the plot. In fact, 0 this provides us with
a reference point upon which to judge the remaining autocorrelations at subsequent lags.
Note also that the y-axis ACF is dimensionless, since correlation is itself dimensionless.
(cid:136)
The dotted blue lines represent boundaries upon which if values fall outside of these, we
have evidence against the null hypothesis that our correlation at lag k, r , is equal to zero
k
at the 5% level. However we must take care because we should expect 5% of these lags to
exceedthesevaluesanyway! Furtherwearedisplayingcorrelated valuesandhenceifonelag
fallsoutsideoftheseboundariesthenproximatesequentialvaluesaremorelikelytodosoas
well. Inpracticewearelookingforlagsthatmayhavesomeunderlyingreasonforexceeding
the 5% level. For instance, in a commodity time series we may be seeing unanticipated
seasonality e(cid:27)ects at certain lags (possibly monthly, quarterly or yearly intervals).
| Here | are a couple | of  | examples | of  | correlograms | for | sequences | of data. |     |
| ---- | ------------ | --- | -------- | --- | ------------ | --- | --------- | -------- | --- |

61
Figure 7.2: Correlogram plotted in R of a sequence of normally distributed random variables.
| 7.5.1 | Example | 1 - Fixed | Linear | Trend |
| ----- | ------- | --------- | ------ | ----- |
The following R code generates a sequence of integers from 1 to 100 and then plots the autocor-
relation:
| > w <- | seq(1, 100) |     |     |     |
| ------ | ----------- | --- | --- | --- |
> acf(w)
| The | plot is displayed | in Figure | 7.3. |     |
| --- | ----------------- | --------- | ---- | --- |
Notice that the ACF plot decreases in an almost linear fashion as the lags increase. Hence a
| correlogram | of this | type is clear | indication | of a trend. |
| ----------- | ------- | ------------- | ---------- | ----------- |
| 7.5.2       | Example | 2 - Repeated  |            | Sequence    |
The following R code generates a repeated sequence of numbers with period p = 10 and then
| plots the | autocorrelation: |     |     |     |
| --------- | ---------------- | --- | --- | --- |
| > w <-    | rep(1:10,        | 10) |     |     |
> acf(w)
| The | plot is displayed | in Figure | 7.4. |     |
| --- | ----------------- | --------- | ---- | --- |
We can see that at lag 10 and 20 there are signi(cid:28)cant peaks. This makes sense, since the
sequencesarerepeatingwithaperiodof10. Interestingly,notethatthereisanegativecorrelation
at lags 5 and 15 of exactly -0.5. This is very characteristic of seasonal time series and behaviour
of this sort in a correlogram is usually indicative that seasonality/periodic e(cid:27)ects have not fully
| been accounted | for        | in a model. |     |     |
| -------------- | ---------- | ----------- | --- | --- |
| 7.6            | Next Steps |             |     |     |
Nowthatwe’vediscussedautocorrelationandcorrelogramsinsomedepth,insubsequentchapters
we will be moving on to linear models and begin the process of forecasting.

62
Figure 7.3: Correlogram plotted in R of a sequence of integers from 1 to 100
Figure 7.4: Correlogram plotted in R of a sequence of integers from 1 to 10, repeated 10 times
Whilelinearmodelsarefarfromthestateoftheartintimeseriesanalysis,weneedtodevelop
thetheoryonsimplercasesbeforewecanapplyittothemoreinterestingnon-linearmodelsthat

63
are in use today.

64

| Chapter |     | 8     |     |     |     |       |     |       |
| ------- | --- | ----- | --- | --- | --- | ----- | --- | ----- |
| Random  |     | Walks |     |     | and | White |     | Noise |
Models
In the previous chapter we discussed the importance of serial correlation and why it is ex-
| tremely | useful in | the context | of  | quantitative | trading. |     |     |     |
| ------- | --------- | ----------- | --- | ------------ | -------- | --- | --- | --- |
In this chapter we will make full use of serial correlation by discussing our (cid:28)rst time series
models,includingsomeelementarylinearstochasticmodels. Inparticularwearegoingtodiscuss
| the White | Noise | and Random |           | Walk | models. |     |     |     |
| --------- | ----- | ---------- | --------- | ---- | ------- | --- | --- | --- |
| 8.1       | Time  | Series     | Modelling |      | Process |     |     |     |
What is a time series model? Essentially, it is a mathematical model that attempts to "explain"
| the serial | correlation | present | in  | a time | series. |     |     |     |
| ---------- | ----------- | ------- | --- | ------ | ------- | --- | --- | --- |
Whenwesay"explain"whatwereallymeanisoncewehave"(cid:28)tted"amodeltoatimeseries
it should account for some or all of the serial correlation present in the correlogram. That is,
by (cid:28)tting the model to a historical time series, we are reducing the serial correlation and thus
| "explaining | it away". |     |     |     |     |     |     |     |
| ----------- | --------- | --- | --- | --- | --- | --- | --- | --- |
Our process, as quantitative researchers, is to consider a wide variety of models including
their assumptions and their complexity, and then choose a model such that it is the "simplest"
that will explain the serial correlation. Once we have such a model we can use it to predict
future values, or future behaviour in general. This prediction is obviously extremely useful in
| quantitative | trading. |     |     |     |     |     |     |     |
| ------------ | -------- | --- | --- | --- | --- | --- | --- | --- |
If we can predict the direction of an asset movement then we have the basis of a trading
strategy (allowing for transaction costs, of course!). Also, if we can predict volatility of an asset
then we have the basis of another trading strategy or a risk-management approach. This is why
we are interested in second order properties, since they give us the means to help us make
forecasts.
How do we know when we have a good (cid:28)t for a model? What criteria do we use to judge
which model is best? We will be considering these questions in this part of the book.
Let’s summarise the general process we will be following throughout the time series section:
(cid:136)
| Outline | a hypotheis |     | about | a particular | time | series | and its behaviour |     |
| ------- | ----------- | --- | ----- | ------------ | ---- | ------ | ----------------- | --- |
(cid:136) Obtain the correlogram of the time series using R and assess its serial correlation
(cid:136)
Use our knowledge of time series to (cid:28)t an appropriate model that reduces the serial corre-
| lation | in the | residuals |     |     |     |     |     |     |
| ------ | ------ | --------- | --- | --- | --- | --- | --- | --- |
(cid:136) Re(cid:28)ne the (cid:28)t until no correlation is present and then subsequently make use of statistical
| goodness-of-(cid:28)t |     | tests | to assess | the | model (cid:28)t |     |     |     |
| --------------------- | --- | ----- | --------- | --- | --------------- | --- | --- | --- |
(cid:136)
Use the model and its second-order properties to make forecasts about future values
65

66
(cid:136)
Iterate through this process until the forecast accuracy is optimised
(cid:136)
Utilise such forecasts to create trading strategies
Thatisourbasicprocess. Thecomplexitywillarisewhenweconsidermoreadvancedmodels
that account for additional serial correlation in our time series.
In this chapter we are going to consider two of the most basic time series models, namely
White NoiseandRandom Walks. Thesemodelswillformthebasisofmoreadvancedmodels
later so it is essential we understand them well.
However, before we introduce either of these models, we are going to discuss some more
abstract concepts that will help us unify our approach to time series models. In particular, we
are going to de(cid:28)ne the Backward Shift Operator and the Di(cid:27)erence Operator.
8.2 Backward Shift and Di(cid:27)erence Operators
The Backward Shift Operator (BSO) and the Di(cid:27)erence Operator will allow us to write
many di(cid:27)erent time series models in a particularly succinct way that more easily allows us to
draw comparisons between them.
Since we will be using the notation of each so frequently, it makes sense to de(cid:28)ne them now.
De(cid:28)nition 8.2.1. Backward Shift Operator. The backward shift operator or lag operator, B,
takes a time series element as an argument and returns the element one time unit previously:
Bx =x .
t t−1
Repeated application of the operator allows us to step back n times: Bnx =x .
t t−n
We will use the BSO to de(cid:28)ne many of our time series models going forward.
Inaddition, whenwecometostudytimeseriesmodelsthatarenon-stationary(thatis, their
mean and variance can alter with time), we can use a di(cid:27)erencing procedure in order to take a
non-stationary series and produce a stationary series from it.
De(cid:28)nition8.2.2. Di(cid:27)erenceOperator. Thedi(cid:27)erenceoperator,∇,takesatimeserieselementas
anargumentandreturnsthedi(cid:27)erencebetweentheelementandthatofonetimeunitpreviously:
∇x =x −x , or ∇x =(1−B)x .
t t t−1 t t
As with the BSO, we can repeatedly apply the di(cid:27)erence operator: ∇n =(1−B)n.
Now that we’ve discussed these abstract operators, let us consider some concrete time series
models.
8.3 White Noise
Let’s begin by trying to motivate the concept of White Noise.
Above, we mentioned that our basic approach was to try (cid:28)tting models to a time series until
the remaining series lacked any serial correlation. This motivates the de(cid:28)nition of the residual
error series:
De(cid:28)nition 8.3.1. Residual Error Series. The residual error series or residuals, x , is a time
t
seriesofthedi(cid:27)erencebetweenanobservedvalueandapredictedvalue,fromatimeseriesmodel,
at a particular time t.
Ify istheobservedvalueandyˆ isthepredictedvalue,wesay: x =y −yˆ aretheresiduals.
t t t t t
The key point is that if our chosen time series model is able to "explain" the serial corre-
lation in the observations, then the residuals themselves are serially uncorrelated. This means
that each element of the serially uncorrelated residual series is an independent realisation from
some probability distribution. That is, the residuals themselves are independent and identically
distributed (i.i.d.).
Hence,ifwearetobegincreatingtimeseriesmodelsthatexplainawayanyserialcorrelation,
it seems natural to begin with a process that produces independent random variables from some
distribution. This directly leads on to the concept of (discrete) white noise:

67
|                        |                     |     |     | Consideratimeseries{w |     | :t=1,...n}. |               |
| ---------------------- | ------------------- | --- | --- | --------------------- | --- | ----------- | ------------- |
| De(cid:28)nition8.3.2. | DiscreteWhiteNoise. |     |     |                       |     | t           | Iftheelements |
oftheseries,w ,areindependentandidenticallydistributed(i.i.d.),withameanofzero,variance
i
σ2 and no serial correlation (i.e. Cor(w ,w ) = 0,∀i (cid:54)= j) then we say that the time series is
i j
| discrete white | noise (DWN). |     |     |     |     |     |     |
| -------------- | ------------ | --- | --- | --- | --- | --- | --- |
In particular, if the values w are drawn from a standard normal distribution (i.e. w ∼
i t
| N(0,σ2)), | then the series | is known | as Gaussian | White | Noise. |     |     |
| --------- | --------------- | -------- | ----------- | ----- | ------ | --- | --- |
White Noise is useful in many contexts. In particular, it can be used to simulate a synthetic
series.
As we’ve mentioned before, a historical time series is only one observed instance. If we can
simulate multiple realisations then we can create "many histories" and thus generate statistics
for some of the parameters of particular models. This will help us re(cid:28)ne our models and thus
| increase accuracy | in our | forecasting. |     |     |     |     |     |
| ----------------- | ------ | ------------ | --- | --- | --- | --- | --- |
Nowthatwe’vede(cid:28)nedDiscreteWhiteNoise,wearegoingtoexaminesomeoftheattributes
| of it, including   | its second | order      | properties | and its | correlogram. |     |     |
| ------------------ | ---------- | ---------- | ---------- | ------- | ------------ | --- | --- |
| 8.3.1 Second-Order |            | Properties |            |         |              |     |     |
The second-order properties of DWN are straightforward and follow easily from the actual de(cid:28)-
nition. In particular, the mean of the series is zero and there is no autocorrelation by de(cid:28)nition:
|     |     |     | µ   | =E(w )=0 |     |     |       |
| --- | --- | --- | --- | -------- | --- | --- | ----- |
|     |     |     | w   | t        |     |     | (8.1) |
(cid:40)
1 k =0
if
|                   |     | ρ   | =Cor(w | ,w )= |        |            |     |
| ----------------- | --- | --- | ------ | ----- | ------ | ---------- | --- |
|                   |     | k   |        | t t+k | 0 if k | (cid:54)=0 |     |
| 8.3.2 Correlogram |     |     |        |       |        |            |     |
WecanalsoplotthecorrelogramofaDWNusingR,seeFigure8.1. Firstlywe’llsettherandom
seed to be 1, so that your random draws will be identical to mine. Then we will sample 1000
| elements from | a normal | distribution | and | plot the autocorrelation: |     |     |     |
| ------------- | -------- | ------------ | --- | ------------------------- | --- | --- | --- |
> set.seed(1)
> acf(rnorm(1000))
Notice that at k =6, k =15 and k =18, we have three peaks that di(cid:27)er from zero at the 5%
level. However, this is to be expected simply due to the variation in sampling from the normal
distribution.
Once again, we must be extremely careful in our interpretation of results. In this instance,
|     |     |     |     |     |     | k =6, | k =15 k =18? |
| --- | --- | --- | --- | --- | --- | ----- | ------------ |
do we really expect anything physically meaningful to be happening at or
NoticethattheDWNmodelonlyhasasingleparameter,namelythevarianceσ2. Thankfully,
it is straightforward to estimate the variance with R. We can simply use the var function:
> set.seed(1)
| > var(rnorm(1000, | mean=0, | sd=1)) |     |     |     |     |     |
| ----------------- | ------- | ------ | --- | --- | --- | --- | --- |
[1] 1.071051
We’ve speci(cid:28)cally highlighted that the normal distribution above has a mean of zero and a
standarddeviationof1(andthusavarianceof1). Rcalculatesthesamplevarianceas1.071051,
| which is close | to the population |     | value of | 1.  |     |     |     |
| -------------- | ----------------- | --- | -------- | --- | --- | --- | --- |
The key takeaway with Discrete White Noise is that we use it as a model for the residuals.
Wearelookingto(cid:28)tothertimeseriesmodelstoourobservedseries,atwhichpointweuseDWN
as a con(cid:28)rmation that we have eliminated any remaining serial correlation from the residuals
| and thus have | a good model | (cid:28)t. |     |     |     |     |     |
| ------------- | ------------ | ---------- | --- | --- | --- | --- | --- |
Now that we have examined DWN we are going to move on to a famous model for (some)
| (cid:28)nancial time | series, namely | the | Random | Walk. |     |     |     |
| -------------------- | -------------- | --- | ------ | ----- | --- | --- | --- |

68
|     |        |     | Figure | 8.1: Correlogram |     | of  | Discrete White | Noise. |     |
| --- | ------ | --- | ------ | ---------------- | --- | --- | -------------- | ------ | --- |
| 8.4 | Random |     | Walk.  |                  |     |     |                |        |     |
A random walk is another time series model where the current observation is equal to the
previous observation with a random step up or down. It is formally de(cid:28)ned below:
De(cid:28)nition 8.4.1. Random Walk A random walk is a time series model x such that x =
t t
| x +w | , where | w is | a discrete | white | noise | series. |     |     |     |
| ---- | ------- | ---- | ---------- | ----- | ----- | ------- | --- | --- | --- |
| t−1  | t       | t    |            |       |       |         |     |     |     |
Recall above that we de(cid:28)ned the backward shift operator B. We can apply the BSO to the
random walk:
|       |          |                  |          | x =Bx | +w     | =x       | +w         |         | (8.2) |
| ----- | -------- | ---------------- | -------- | ----- | ------ | -------- | ---------- | ------- | ----- |
|       |          |                  |          | t     | t      | t        | t−1 t      |         |       |
| And   | stepping | back             | further: |       |        |          |            |         |       |
|       |          |                  | x t−1    | =Bx   | t−1 +w | t−1 =x   | t−2 +w t−1 |         | (8.3) |
| If we | repeat   | this process     | until    | the   | end of | the time | series we  | get:    |       |
|       |          | x =(1+B+B2+...)w |          |       |        | =⇒ x     | =w +w      | +w +... | (8.4) |
|       |          | t                |          |       | t      | t        | t t−1      | t−2     |       |
Henceitiscleartoseehowtherandomwalkissimplythesumoftheelementsfromadiscrete
| white noise | series.      |     |     |            |     |     |     |     |     |
| ----------- | ------------ | --- | --- | ---------- | --- | --- | --- | --- | --- |
| 8.4.1       | Second-Order |     |     | Properties |     |     |     |     |     |
The second-order properties of a random walk are a little more interesting than that of discrete
white noise. While the mean of a random walk is still zero, the covariance is actually time-
| dependent. | Hence | a random |     | walk is | non-stationary: |     |     |     |     |
| ---------- | ----- | -------- | --- | ------- | --------------- | --- | --- | --- | --- |

69
|     |     |     |     | µ   | x = | 0   |     |     | (8.5) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
)=tσ2
|     |     |     |     | γ k (t) | =   | Cov(x t ,x t+k |     |     | (8.6) |
| --- | --- | --- | --- | ------- | --- | -------------- | --- | --- | ----- |
In particular, the covariance is equal to the variance multiplied by the time. Hence, as time
| increases, | so does | the | variance. |     |     |     |     |     |     |
| ---------- | ------- | --- | --------- | --- | --- | --- | --- | --- | --- |
What does this mean for random walks? Put simply, it means there is very little point in
extrapolating "trends" in them over the long term, as they are literally random walks.
| 8.4.2 | Correlogram |     |     |     |     |     |     |     |     |
| ----- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
The autocorrelation of a random walk (which is also time-dependent) can be derived as follows:
|     |     |        | Cov(x     | ,x     | )   | tσ2          |     | 1         |       |
| --- | --- | ------ | --------- | ------ | --- | ------------ | --- | --------- | ----- |
|     |     | ρ (t)= |           | t      | t+k | =            | =   |           |       |
|     |     | k      | (cid:112) |        |     | (cid:112)    |     | (cid:112) | (8.7) |
|     |     |        | Var(x     | )Var(x |     | ) tσ2(t+k)σ2 |     | 1+k/t     |       |
|     |     |        |           | t      | t+k |              |     |           |       |
Notice that this implies if we are considering a long time series, with short term lags, then
we get an autocorrelation that is almost unity. That is, we have extremely high autocorrelation
that does not decrease very rapidly as the lag increases. We can simulate such a series using R.
Firstly, we set the seed so that you can replicate my results exactly. Then we create two
sequencesofrandomdraws(xandw),eachofwhichhasthesamevalue(asde(cid:28)nedbytheseed).
We then loop through every element of x and assign it the value of the previous value of
x plus the current value of w. This gives us the random walk. We then plot the results using
type="l" to give us a line plot, rather than a plot of circular points, see Figure 8.2.
> set.seed(4)
| > x <-    | w <- rnorm(1000) |        |         |           |             |                 |      |     |     |
| --------- | ---------------- | ------ | ------- | --------- | ----------- | --------------- | ---- | --- | --- |
| > for (t  | in 2:1000)       |        | x[t]    | <- x[t-1] |             | + w[t]          |      |     |     |
| > plot(x, | type="l")        |        |         |           |             |                 |      |     |     |
| It is     | simple           | enough | to draw | the       | correlogram | too, see Figure | 8.3. |     |     |
> acf(x)
| 8.4.3 | Fitting | Random |     | Walk | Models | to Financial |     | Data |     |
| ----- | ------- | ------ | --- | ---- | ------ | ------------ | --- | ---- | --- |
Wementionedabovethatwewouldtryand(cid:28)t modelstodata whichwehavealreadysimulated.
Clearly this is somewhat contrived, as we’ve simulated the random walk in the (cid:28)rst place!
However, we’re trying to demonstrate the (cid:28)tting process. In real situations we won’t know
the underlying generating model for our data, we will only be able to (cid:28)t models and then
| assess the | correlogram. |     |     |     |     |     |     |     |     |
| ---------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
We stated that this process was useful because it helps us check that we’ve correctly imple-
mented the model by trying to ensure that parameter estimates are close to those used in the
simulations.
| Fitting | to Simulated |     | Data |     |     |     |     |     |     |
| ------- | ------------ | --- | ---- | --- | --- | --- | --- | --- | --- |
Since we are going to be spending a lot of time (cid:28)tting models to (cid:28)nancial time series, we should
getsomepracticeonsimulateddata(cid:28)rst,suchthatwe’rewell-versedintheprocessoncewestart
| using real | data. |     |     |     |     |     |     |     |     |
| ---------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
Wehavealreadysimulatedarandomwalksowemayaswellusethatrealisationtoseeifour
| proposed | model | (of a | random | walk) | is accurate. |     |     |     |     |
| -------- | ----- | ----- | ------ | ----- | ------------ | --- | --- | --- | --- |
How can we tell if our proposed random walk model is a good (cid:28)t for our simulated data?
Well,wemakeuseofthede(cid:28)nitionofarandomwalk,whichissimplythatthedi(cid:27)erencebetween
two neighbouring values is equal to a realisation from a discrete white noise process.
Hence,ifwecreateaseriesofthedi(cid:27)erences ofelementsfromoursimulatedseries,weshould
| have a series | that | resembles |     | discrete | white | noise! |     |     |     |
| ------------- | ---- | --------- | --- | -------- | ----- | ------ | --- | --- | --- |

70
| Figure | 8.2: Realisation | of a Random | Walk with   | 1000 timesteps. |
| ------ | ---------------- | ----------- | ----------- | --------------- |
|        | Figure 8.3:      | Correlogram | of a Random | Walk.           |
InRthiscanbeaccomplishedverystraightforwardlyusingthedifffunction. Oncewehave
created the di(cid:27)erence series, we wish to plot the correlogram and then assess how close this is to

71
discrete white noise, see Figure 8.4.
> acf(diff(x))
Figure 8.4: Correlogram of the Di(cid:27)erence Series from a Simulated Random Walk.
Whatcanwenoticefromthisplot? Thereisastatisticallysigni(cid:28)cantpeakatk =10,butonly
marginally. Remember, thatweexpect toseeatleast5%ofthepeaksbestatisticallysigni(cid:28)cant,
simply due to sampling variation.
Hencewecanreasonablystatethatthethecorrelogramlookslikethatofdiscretewhitenoise.
It implies that the random walk model is a good (cid:28)t for our simulated data. This is exactly what
we should expect, since we simulated a random walk in the (cid:28)rst place!
Fitting to Financial Data
Let’s now apply our random walk model to some actual (cid:28)nancial data. As with the Python
library pandas we can use the R package quantmod to easily extract (cid:28)nancial data from
Yahoo Finance.
Wearegoingtoseeifarandomwalkmodelisagood(cid:28)tforsomeequitiesdata. Inparticular,
I am going to choose Microsoft (MSFT), but you can experiment with your favourite ticker
symbol.
Before we’re able to download any of the data, we must install quantmod as it isn’t part of
the default R installation. Run the following command and select the R package mirror server
that is closest to your location:
> install.packages(’quantmod’)
Once quantmod is installed we can use it to obtain the historical price of MSFT stock:
> require(’quantmod’)
> getSymbols(’MSFT’, src=’yahoo’)
> MSFT
..
..

72
| 2015-07-15 | 45.68 | 45.89 | 45.43 |     | 45.76 | 26482000 | 45.76000 |
| ---------- | ----- | ----- | ----- | --- | ----- | -------- | -------- |
| 2015-07-16 | 46.01 | 46.69 | 45.97 |     | 46.66 | 25894400 | 46.66000 |
| 2015-07-17 | 46.55 | 46.78 | 46.26 |     | 46.62 | 29262900 | 46.62000 |
ThiswillcreateanobjectcalledMSFT(casesensitive!) intotheRnamespace,whichcontains
thepricingandvolumehistoryofMSFT.We’reinterestedinthecorporate-actionadjustedclosing
price. We can use the following commands to (respectively) obtain the Open, High, Low, Close,
Volume and Adjusted Close prices for the Microsoft stock: Op(MSFT), Hi(MSFT), Lo(MSFT),
| Cl(MSFT), | Vo(MSFT), | Ad(MSFT). |     |     |     |     |     |
| --------- | --------- | --------- | --- | --- | --- | --- | --- |
Our process will be to take the di(cid:27)erence of the Adjusted Close values, omit any missing
values, and then run them through the autocorrelation function. When we plot the correlogram
we are looking for evidence of discrete white noise, that is, a residuals series that is serially
| uncorrelated.         | To carry | this out in R, | we run     | the following | command: |     |     |
| --------------------- | -------- | -------------- | ---------- | ------------- | -------- | --- | --- |
| > acf(diff(Ad(MSFT)), |          | na.action      | = na.omit) |               |          |     |     |
The latter part (na.action = na.omit) tells the acf function to ignore missing values by
| omitting | them. The output | of the acf | function | is given | in Figure | 8.5. |     |
| -------- | ---------------- | ---------- | -------- | -------- | --------- | ---- | --- |
Figure 8.5: Correlogram of the Di(cid:27)erence Series from MSFT Adjusted Close.
Wenoticethatthemajorityofthelagpeaksdonotdi(cid:27)erfromzeroatthe5%level. However
thereareafewthataremarginallyabove. Giventhatthelagsk i wherepeaksexistaresomeway
from k =0, we could be inclined to think that these are due to stochastic variation and do not
| represent | any physical | serial correlation | in the | series. |     |     |     |
| --------- | ------------ | ------------------ | ------ | ------- | --- | --- | --- |
Hencewecanconclude,withareasonabledegreeofcertainty,thattheadjustedclosingprices
| of MSFT | are well approximated | by  | a random | walk. |     |     |     |
| ------- | --------------------- | --- | -------- | ----- | --- | --- | --- |
Let’s now try the same approach on the S&P500 itself. The Yahoo Finance symbol for the
S&P500 index is ^GSPC. Hence, if we enter the following commands into R, we can plot the
| correlogram           | of the di(cid:27)erence | series       | of the S&P500: |     |     |     |     |
| --------------------- | ----------------------- | ------------ | -------------- | --- | --- | --- | --- |
| > getSymbols(’^GSPC’, |                         | src=’yahoo’) |                |     |     |     |     |
| > acf(diff(Ad(GSPC)), |                         | na.action    | = na.omit)     |     |     |     |     |

73
Figure 8.6: Correlogram of the Di(cid:27)erence Series from the S&P500 Adjusted Close.
| The | correlogram is given | in Figure | 8.6. |     |     |
| --- | -------------------- | --------- | ---- | --- | --- |
Thecorrelogramhereiscertainlymoreinteresting. Noticethatthereisanegativecorrelation
| at k =1. | This is unlikely | to be due | to random | sampling variation. |     |
| -------- | ---------------- | --------- | --------- | ------------------- | --- |
Notice also that there are peaks at k = 15, k = 16 and k = 18. Although it is harder to
justify their existence beyond that of random variation, they may be indicative of a longer-lag
process.
Hence it is much harder to justify that a random walk is a good model for the S&P500
Adjusted Close data. This motivates more sophisticated models, namely the Autoregressive
| Models | of Order p, which | will be | the subject | of the following | chapter. |
| ------ | ----------------- | ------- | ----------- | ---------------- | -------- |

74

| Chapter        |     | 9   |     |        |     |     |         |
| -------------- | --- | --- | --- | ------ | --- | --- | ------- |
| Autoregressive |     |     |     | Moving |     |     | Average |
Models
In the last chapter we looked at random walks and white noise as basic time series models for
certain (cid:28)nancial instruments, such as daily equity and equity index prices. We found that in
some cases a random walk model was insu(cid:30)cient to capture the full autocorrelation behaviour
| of the instrument, |     | which | motivates | more | sophisticated | models. |     |
| ------------------ | --- | ----- | --------- | ---- | ------------- | ------- | --- |
In this chapter we are going to discuss three types of model, namely the Autoregressive
p, q
(AR) model of order the Moving Average (MA) model of order and the mixed Auto-
gressive Moving Average (ARMA) model of order p,q. These models will help us attempt
to capture or "explain" more of the serial correlation present within an instrument. Ultimately
| they will | provide | us with | a means | of forecasting | the | future | prices. |
| --------- | ------- | ------- | ------- | -------------- | --- | ------ | ------- |
However, it is well known that (cid:28)nancial time series possess a property known as volatility
clustering. That is, the volatility of the instrument is not constant in time. The technical term
for this behaviour is conditional heteroskedasticity. Since the AR, MA and ARMA models
are not conditionally heteroskedastic, that is, they don’t take into account volatility clustering,
| we will ultimately |     | need | a more | sophisticated | model | for our | predictions. |
| ------------------ | --- | ---- | ------ | ------------- | ----- | ------- | ------------ |
Such models include the Autogressive Conditional Heteroskedastic (ARCH) model
and Generalised Autogressive Conditional Heteroskedastic (GARCH) model, and the
manyvariantsthereof. GARCHisparticularlywellknowninquant(cid:28)nanceandisprimarilyused
| for (cid:28)nancial | time | series | simulations | as a means | of estimating |     | risk. |
| ------------------- | ---- | ------ | ----------- | ---------- | ------------- | --- | ----- |
However, we will be building up to these models from simpler versions in order to see how
each new variant changes our predictive ability. Despite the fact that AR, MA and ARMA are
relatively simple time series models, they are the basis of more complicated models such as the
Autoregressive Integrated Moving Average (ARIMA) and the GARCH family. Hence it
| is important | that | we study | them. |     |     |     |     |
| ------------ | ---- | -------- | ----- | --- | --- | --- | --- |
One of our trading strategies later in the book will be to combine ARIMA and GARCH in
ordertopredictpricesnperiodsinadvance. However, wewillhavetowaituntilwe’vediscussed
both ARIMA and GARCH separately before we apply them to this strategy.
| 9.1 | How | Will | We  | Proceed? |     |     |     |
| --- | --- | ---- | --- | -------- | --- | --- | --- |
In this chapter we are going to outline some new time series concepts that we’ll need for the re-
mainingmethods,namelystrict stationarityandtheAkaike information criterion (AIC).
Subsequenttothesenewconceptswewillfollowthetraditionalpatternforstudyingnewtime
series models:
(cid:136)
Rationale-The(cid:28)rsttaskistoprovideareasonwhywe’reinterestedinaparticularmodel,
as quants. Why are we introducing the time series model? What e(cid:27)ects can it capture?
| What | do  | we gain | (or lose) | by adding | in extra | complexity? |     |
| ---- | --- | ------- | --------- | --------- | -------- | ----------- | --- |
75

76
(cid:136)
De(cid:28)nition-Weneedtoprovidethefullmathematicalde(cid:28)nition(andassociatednotation)
of the time series model in order to minimise any ambiguity.
(cid:136)
Second Order Properties - We will discuss (and in some cases derive) the second order
properties of the time series model, which includes its mean, its variance and its autocor-
relation function.
(cid:136)
Correlogram - We will use the second order properties to plot a correlogram of a realisa-
tion of the time series model in order to visualise its behaviour.
(cid:136)
Simulation-Wewillsimulaterealisationsofthetimeseriesmodelandthen(cid:28)tthemodel
tothesesimulationstoensurewehaveaccurateimplementationsandunderstandthe(cid:28)tting
process.
(cid:136)
RealFinancialData-Wewill(cid:28)tthetimeseriesmodeltoreal(cid:28)nancialdataandconsider
thecorrelogramoftheresidualsinordertoseehowthemodelaccountsforserialcorrelation
in the original series.
(cid:136) Prediction - We will create n-step ahead forecasts of the time series model for particular
realisations in order to ultimately produce trading signals.
Nearlyallofthechapterswritteninthisbookontimeseriesmodelswillfallintothispattern
and it will allow us to easily compare the di(cid:27)erences between each model as we add further
complexity.
We’re going to start by looking at strict stationarity and the AIC.
9.2 Strictly Stationary
We provided the de(cid:28)nition of stationarity in the chapter on serial correlation. However, because
we are going to be entering the realm of many (cid:28)nancial series, with various frequencies, we need
to make sure that our (eventual) models take into account the time-varying volatility of these
series. In particular, we need to consider their heteroskedasticity.
Wewillcomeacrossthisissuewhenwetryto(cid:28)tcertainmodelstohistoricalseries. Generally,
not all of the serial correlation in the residuals of (cid:28)tted models can be accounted for without
taking heteroskedasticity into account. This brings us back to stationarity. A series is not
stationary in the variance if it has time-varying volatility, by de(cid:28)nition.
This motivates a more rigourous de(cid:28)nition of stationarity, namely strict stationarity:
De(cid:28)nition 9.2.1. Strictly Stationary Series. A time series model, {x }, is strictly stationary if
t
thejointstatisticaldistributionoftheelementsx ,...,x isthesameasthatofx ,...,x ,
t1 tn t1+m tn+m
∀t ,m.
i
Onecanthinkofthisde(cid:28)nitionassimplythatthedistributionofthetimeseriesisunchanged
for any abritrary shift in time.
In particular, the mean and the variance are constant in time for a strictly stationary series
andtheautocovariancebetweenx andx (say)dependsonlyontheabsolutedi(cid:27)erenceoftand
t s
s, |t−s|.
We will be revisiting strictly stationary series in future chapters.
9.3 Akaike Information Criterion
Imentionedinpreviouschaptersthatwewouldeventuallyneedtoconsiderhowtochoosebetween
separate"best"models. Thisistruenotonlyoftimeseriesanalysis,butalsoofmachinelearning
and, more broadly, statistics in general.
The two main methods we will use, for the time being, are the Akaike Information Criterion
(AIC) and the Bayesian Information Criterion (BIC).
We’ll brie(cid:29)y consider the AIC, as it will be used in the next section when we come to discuss
the ARMA model.

77
AICisessentiallyatooltoaidinmodelselection. Thatis,ifwehaveaselectionofstatistical
models (including time series), then the AIC estimates the "quality" of each model, relative to
| the others | that | we have | available. |     |     |     |     |     |     |     |
| ---------- | ---- | ------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
Itisbasedoninformation theory,whichisahighlyinteresting,deeptopicthatunfortunately
we can’t go into too much detail about in this book. It attempts to balance the complexity of
the model, which in this case means the number of parameters, with how well it (cid:28)ts the data.
| Let’s | provide a | de(cid:28)nition: |     |     |     |     |     |     |     |     |
| ----- | --------- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- |
De(cid:28)nition 9.3.1. AkaikeInformationCriterion. Ifwetakethelikelihoodfunctionforastatisti-
calmodel,whichhask parameters,andLmaximisesthelikelihood,thentheAkaike Information
| Criterion | is given | by: |     |     |     |              |     |     |     |       |
| --------- | -------- | --- | --- | --- | --- | ------------ | --- | --- | --- | ----- |
|           |          |     |     |     | AIC | =−2log(L)+2k |     |     |     | (9.1) |
The preferred model, from a selection of models, has the minimum AIC of the group. You
can see that the AIC grows as the number of parameters, k, increases, but is reduced if the
negative log-likelihood increases. Essentially it penalises models that are over(cid:28)t.
We are going to be creating AR, MA and ARMA models of varying orders and one way to
| choose | the "best"     | model | (cid:28)t | for a | particular | dataset | is to | use the | AIC. |     |
| ------ | -------------- | ----- | --------- | ----- | ---------- | ------- | ----- | ------- | ---- | --- |
| 9.4    | Autoregressive |       |           | (AR)  |            | Models  | of    | order   | p    |     |
The (cid:28)rst model we’re going to consider, which forms the basis of Part 1, is the Autoregressive
| model | of order  | p, often | shortened |     | to AR(p). |     |     |     |     |     |
| ----- | --------- | -------- | --------- | --- | --------- | --- | --- | --- | --- | --- |
| 9.4.1 | Rationale |          |           |     |           |     |     |     |     |     |
In the previous chapter we considered the random walk, where each term, x is dependent
t
|        |          |          |       | x   |     |              |       |       | w         |       |
| ------ | -------- | -------- | ----- | --- | --- | ------------ | ----- | ----- | --------- | ----- |
| solely | upon the | previous | term, | t−1 | and | a stochastic | white | noise | term, t : |       |
|        |          |          |       |     | x   | =x +w        |       |       |           | (9.2) |
|        |          |          |       |     | t   | t−1          | t     |       |           |       |
The autoregressive model is simply an extension of the random walk that includes terms
further back in time. The structure of the model is linear, that is the model depends linearly on
the previous terms, with coe(cid:30)cients for each term. This is where the "regressive" comes from in
"autoregressive". Itisessentiallyaregressionmodelwheretheprevioustermsarethepredictors.
{x },
De(cid:28)nition 9.4.1. AutoregressiveModeloforderp. Atimeseriesmodel, t isanautoregres-
| sive model | of  | order p, | AR(p), | if: |     |          |     |      |     |       |
| ---------- | --- | -------- | ------ | --- | --- | -------- | --- | ---- | --- | ----- |
|            |     |          |        | x   | = α | x +...+α |     | x +w |     | (9.3) |
|            |     |          |        | t   |     | 1 t−1    | p   | t−p  | t   |       |
p
(cid:88)
|     |     |     |     |     | =   | α x   | +w  |     |     | (9.4) |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | ----- |
|     |     |     |     |     |     | i t−i | t   |     |     |       |
i=1
Where {w } is white noise and α ∈R, with α (cid:54)=0 for a p-order autoregressive process.
|     | t   |     |     | i   |     | p   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
If we consider the Backward Shift Operator, B, then we can rewrite the above as a function
θ of B:
|     |     |     | θ (B)x | =(1−α | B−α | B2−...−α |     | B)x | =w  | (9.5) |
| --- | --- | --- | ------ | ----- | --- | -------- | --- | --- | --- | ----- |
|     |     |     | p      | t     | 1   | 2        |     | p t | t   |       |
Perhaps the (cid:28)rst thing to notice about the AR(p) model is that a random walk is simply
AR(1) with α 1 equal to unity. As we stated above, the autogressive model is an extension of the
| random | walk, | so this | makes | sense! |     |     |     |     |     |     |
| ------ | ----- | ------- | ----- | ------ | --- | --- | --- | --- | --- | --- |
It is straightforward to make predictions with the AR(p) model, for any time t, as once we
| have the | α coe(cid:30)cients |     | determined, |     | our | estimate | simply | becomes: |     |     |
| -------- | ------------------- | --- | ----------- | --- | --- | -------- | ------ | -------- | --- | --- |
i

78
|     |     |     | xˆ =α | x +...+α |     | x     |     |       |
| --- | --- | --- | ----- | -------- | --- | ----- | --- | ----- |
|     |     |     | t     | 1 t−1    |     | p t−p |     | (9.6) |
Hencewecanmaken-stepaheadforecastsbyproducingxˆ ,xˆ ,xˆ ,...uptoxˆ
|     |     |     |     |     |     | t   | t+1 t+2 t+n | . Infact, |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --------- |
once we consider the ARMA models later in the chapter, we will use the R predict function to
create forecasts (along with standard error con(cid:28)dence interval bands) that will help us produce
trading signals.
| 9.4.2 | Stationarity | for | Autoregressive |     | Processes |     |     |     |
| ----- | ------------ | --- | -------------- | --- | --------- | --- | --- | --- |
OneofthemostimportantaspectsoftheAR(p)modelisthatitisnotalwaysstationary. Indeed
the stationarity of a particular model depends upon the parameters. I’ve touched on this before
| in my other | book, Successful |     | Algorithmic | Trading. |     |     |     |     |
| ----------- | ---------------- | --- | ----------- | -------- | --- | --- | --- | --- |
In order to determine whether an AR(p) process is stationary or not we need to solve the
characteristic equation. The characteristic equation is simply the autoregressive model, written
| in backward | shift form, | set to | zero: |         |     |     |     |       |
| ----------- | ----------- | ------ | ----- | ------- | --- | --- | --- | ----- |
|             |             |        |       | θ (B)=0 |     |     |     | (9.7) |
p
We solve this equation for B. In order for the particular autoregressive process to be sta-
tionary we need all of the absolute values of the roots of this equation to exceed unity. This
is an extremely useful property and allows us to quickly calculate whether an AR(p) process is
| stationary | or not.        |          |         |      |                |     |     |     |
| ---------- | -------------- | -------- | ------- | ---- | -------------- | --- | --- | --- |
| Let’s      | consider a few | examples | to make | this | idea concrete: |     |     |     |
(cid:136)
RandomWalk-TheAR(1)processwithα =1hasthecharacteristicequationθ =1−B.
1
| Clearly | this has | root B=1 | and | as such | is not | stationary. |     |     |
| ------- | -------- | -------- | --- | ------- | ------ | ----------- | --- | --- |
(cid:136) AR(1) - If we choose α = 1 we get x = 1x +w . This gives us a characteristic
|     |     |       | 1 4 |     | t 4   | t−1 | t   |     |
| --- | --- | ----- | --- | --- | ----- | --- | --- | --- |
|     | 1−  | 1B=0, |     |     | B=4>1 |     |     |     |
equation of which has a root and so this particular AR(1) process
4
is stationary.
| (cid:136) |     |     | 1   |     |     | 1x  | 1x  |     |
| --------- | --- | --- | --- | --- | --- | --- | --- | --- |
AR(2) - If we set α = α = then we get x = + +w . Its characteristic
|     |     | 1   | 2 2 |     |     | t 2 t−1 | 2 t−2 t |     |
| --- | --- | --- | --- | --- | --- | ------- | ------- | --- |
equation becomes −1(B−1)(B+2) = 0, which gives two roots of B = 1,−2. Since this
2
hasaunitrootitisanon-stationaryseries. However,otherAR(2)seriescanbestationary.
| 9.4.3 | Second Order |     | Properties |     |     |     |     |     |
| ----- | ------------ | --- | ---------- | --- | --- | --- | --- | --- |
The mean of an AR(p) process is zero. However, the autocovariances and autocorrelations are
given by recursive functions, known as the Yule-Walker equations. The full properties are given
below:
|     |     |     |     | µ =E(x | )=0 |     |     | (9.8) |
| --- | --- | --- | --- | ------ | --- | --- | --- | ----- |
|     |     |     |     | x      | t   |     |     |       |
p
(cid:88)
|     |     |     | γ = | α   | γ , k | >0  |     | (9.9) |
| --- | --- | --- | --- | --- | ----- | --- | --- | ----- |
|     |     |     | k   | i   | k−i   |     |     |       |
i=1
p
(cid:88)
|     |     |     | ρ = | α   | ρ , k | >0  |     | (9.10) |
| --- | --- | --- | --- | --- | ----- | --- | --- | ------ |
|     |     |     | k   | i   | k−i   |     |     |        |
i=1
Note that it is necessary to know the α i parameter values prior to calculating the autocorre-
lations.
Now that we’ve stated the second order properties we can simulate various orders of AR(p)
| and plot | the corresponding | correlograms. |     |     |     |     |     |     |
| -------- | ----------------- | ------------- | --- | --- | --- | --- | --- | --- |

79
| 9.4.4 Simulations |     | and Correlograms |     |
| ----------------- | --- | ---------------- | --- |
AR(1)
Let’s begin with an AR(1) process. This is similar to a random walk, except that α does not
1
havetoequalunity. Ourmodelisgoingtohaveα =0.6. TheRcodeforcreatingthissimulation
1
| is given as | follows: |     |     |
| ----------- | -------- | --- | --- |
> set.seed(1)
| > x <- w | <- rnorm(100)  |               |        |
| -------- | -------------- | ------------- | ------ |
| > for (t | in 2:100) x[t] | <- 0.6*x[t-1] | + w[t] |
Notice that our for loop is carried out from 2 to 100, not 1 to 100, as x[t-1] when t=0 is
not indexable. Similarly for higher order AR(p) processes, t must range from p to 100 in this
loop.
We can plot the realisation of this model and its associated correlogram using the layout
| function, given | in Figure | 9.1. |     |
| --------------- | --------- | ---- | --- |
> layout(1:2)
type="l")
> plot(x,
> acf(x)
Figure 9.1: Realisation of AR(1) Model, with α =0.6 and Associated Correlogram.
1
Let’snowtry(cid:28)ttinganAR(p)processtothesimulateddatawe’vejustgenerated,toseeifwe
can recover the underlying parameters. You may recall that we carried out a similar procedure
| in the previous | chapter on | white noise and | random walks. |
| --------------- | ---------- | --------------- | ------------- |
As it turns out R provides a useful command ar to (cid:28)t autoregressive models. We can use
this method to (cid:28)rstly tell us the best order p of the model (as determined by the AIC above)
and provide us with parameter estimates for the α , which we can then use to form con(cid:28)dence
i
intervals.
| For completeness | let’s | recreate the x series: |     |
| ---------------- | ----- | ---------------------- | --- |
> set.seed(1)

80
| > x <-   | w <- | rnorm(100) |         |            |     |      |     |
| -------- | ---- | ---------- | ------- | ---------- | --- | ---- | --- |
| > for (t | in   | 2:100)     | x[t] <- | 0.6*x[t-1] | +   | w[t] |     |
Now we use the ar command to (cid:28)t an autoregressive model to our simulated AR(1) process,
| using maximum |               | likelihood | estimation | (MLE)         | as     | the (cid:28)tting procedure. |     |
| ------------- | ------------- | ---------- | ---------- | ------------- | ------ | ---------------------------- | --- |
| We will       | (cid:28)rstly | extract    | the        | best obtained | order: |                              |     |
| > x.ar        | <- ar(x,      | method     | =          | "mle")        |        |                              |     |
> x.ar$order
[1] 1
The command has successfully determined that our underlying time series model is an
ar
AR(1) process.
| We can | then | obtain | the α | parameter(s) | estimates: |     |     |
| ------ | ---- | ------ | ----- | ------------ | ---------- | --- | --- |
i
> x.ar$ar
[1] 0.5231187
|     |     |     |     |     |     | αˆ = 0.523, |     |
| --- | --- | --- | --- | --- | --- | ----------- | --- |
The MLE procedure has produced an estimate, 1 which is slightly lower than the
| true value | of α | =0.6. |     |     |     |     |     |
| ---------- | ---- | ----- | --- | --- | --- | --- | --- |
1
Finally, we can use the standard error, with the asymptotic variance, to construct 95%
con(cid:28)dence intervals around the underlying parameter. To achieve this we simply create a vector
| c(-1.96,      | 1.96)      | and       | then multiply            | it by | the standard | error: |     |
| ------------- | ---------- | --------- | ------------------------ | ----- | ------------ | ------ | --- |
| x.ar$ar       | + c(-1.96, |           | 1.96)*sqrt(x.ar$asy.var) |       |              |        |     |
| [1] 0.3556050 |            | 0.6906324 |                          |       |              |        |     |
Thetrueparameterdoesfallwithinthe95%con(cid:28)denceinterval,aswe’dexpectfromthefact
| we’ve generated |       | the realisation |     | from the | model | speci(cid:28)cally.     |      |
| --------------- | ----- | --------------- | --- | -------- | ----- | ----------------------- | ---- |
| How             | about | if we change    | the | α =−0.6? | The   | plot is given in Figure | 9.2. |
1
> set.seed(1)
| > x <-   | w <- | rnorm(100) |         |             |     |        |     |
| -------- | ---- | ---------- | ------- | ----------- | --- | ------ | --- |
| > for (t | in   | 2:100)     | x[t] <- | -0.6*x[t-1] |     | + w[t] |     |
> layout(1:2)
| > plot(x, | type="l") |     |     |     |     |     |     |
| --------- | --------- | --- | --- | --- | --- | --- | --- |
> acf(x)
| As before |     | we can (cid:28)t | an AR(p) | model | using ar: |     |     |
| --------- | --- | ---------------- | -------- | ----- | --------- | --- | --- |
> set.seed(1)
| > x <-   | w <-     | rnorm(100) |         |             |     |        |     |
| -------- | -------- | ---------- | ------- | ----------- | --- | ------ | --- |
| > for (t | in       | 2:100)     | x[t] <- | -0.6*x[t-1] |     | + w[t] |     |
| > x.ar   | <- ar(x, | method     | =       | "mle")      |     |        |     |
> x.ar$order
[1] 1
> x.ar$ar
[1] -0.5973473
| > x.ar$ar      | +   | c(-1.96,   | 1.96)*sqrt(x.ar$asy.var) |     |     |     |     |
| -------------- | --- | ---------- | ------------------------ | --- | --- | --- | --- |
| [1] -0.7538593 |     | -0.4408353 |                          |     |     |     |     |
Onceagainwerecoverthecorrectorderofthemodel,withaverygoodestimateαˆ =−0.597
1
of α =−0.6. We also see that the true parameter falls within the 95% con(cid:28)dence interval once
1
again.
AR(2)
Let’saddsomemorecomplexitytoourautoregressiveprocessesbysimulatingamodeloforder2.
In particular, we will set α =0.666, but also set α =−0.333. Here’s the full code to simulate
|     |     |     | 1   |     |     | 2   |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
and plot the realisation, as well as the correlogram for such a series, given in Figure 9.3.

81
Figure 9.2: Realisation of AR(1) Model, with α =−0.6 and Associated Correlogram.
1
> set.seed(1)
| > x <- | w <- rnorm(100) |     |     |     |     |
| ------ | --------------- | --- | --- | --- | --- |
> for (t in 3:100) x[t] <- 0.666*x[t-1] - 0.333*x[t-2] + w[t]
> layout(1:2)
type="l")
> plot(x,
> acf(x)
As before we can see that the correlogram di(cid:27)ers signi(cid:28)cantly from that of white noise, as
we’d expect. There are statistically signi(cid:28)cant peaks at k =1, k =3 and k =4.
Once again, we’re going to use the ar command to (cid:28)t an AR(p) model to our underlying
| AR(2) realisation. | The procedure | is similar | as for the AR(1) | (cid:28)t: |     |
| ------------------ | ------------- | ---------- | ---------------- | ---------- | --- |
> set.seed(1)
| > x <- | w <- rnorm(100) |     |     |     |     |
| ------ | --------------- | --- | --- | --- | --- |
> for (t in 3:100) x[t] <- 0.666*x[t-1] - 0.333*x[t-2] + w[t]
| > x.ar       | <- ar(x, method | = "mle")       |              |           |     |
| ------------ | --------------- | -------------- | ------------ | --------- | --- |
| Warning      | message:        |                |              |           |     |
| In arima0(x, | order =         | c(i, 0L, 0L),  | include.mean | = demean) | :   |
| possible     | convergence     | problem: optim | gave code    | = 1       |     |
> x.ar$order
[1] 2
> x.ar$ar
| [1] 0.6961005 | -0.3946280 |     |     |     |     |
| ------------- | ---------- | --- | --- | --- | --- |
The correct order has been recovered and the parameter estimates αˆ 1 = 0.696 and αˆ 2 =
−0.395 are not too far o(cid:27) the true parameter values of α =0.666 and α =−0.333.
|     |     |     |     | 1   | 2   |
| --- | --- | --- | --- | --- | --- |
Notice that we receive a convergence warning message. Notice also that R actually uses the
arima0functiontocalculatetheARmodel. Aswe’lllearninsubsequentchapters,AR(p)models
are simply ARIMA(p, 0, 0) models, and thus an AR model is a special case of ARIMA with no
| Moving | Average (MA) or | Integrated (I) component. |     |     |     |
| ------ | --------------- | ------------------------- | --- | --- | --- |

82
Figure 9.3: Realisation of AR(2) Model, with α =0.666, α =−0.333 and Associated Correlo-
|     |     |     | 1   | 2   |     |     |
| --- | --- | --- | --- | --- | --- | --- |
gram.
We’ll also be using the arima command to create con(cid:28)dence intervals around multiple pa-
| rameters, | which is why we’ve | neglected | to do it here. |     |     |     |
| --------- | ------------------ | --------- | -------------- | --- | --- | --- |
Nowthatwe’vecreatedsomesimulateddataitistimetoapplytheAR(p)modelsto(cid:28)nancial
| asset time      | series. |     |     |     |     |     |
| --------------- | ------- | --- | --- | --- | --- | --- |
| 9.4.5 Financial | Data    |     |     |     |     |     |
| Amazon          | Inc.    |     |     |     |     |     |
Let’sbeginbyobtainingthestockpriceforAmazon(AMZN)usingquantmodasintheprevious
chapter:
> require(quantmod)
> getSymbols("AMZN")
> AMZN
..
..
| 2015-08-12 | 523.75 | 527.50 | 513.06 | 525.91 | 3962300 | 525.91 |
| ---------- | ------ | ------ | ------ | ------ | ------- | ------ |
| 2015-08-13 | 527.37 | 534.66 | 525.49 | 529.66 | 2887800 | 529.66 |
| 2015-08-14 | 528.25 | 534.11 | 528.25 | 531.52 | 1983200 | 531.52 |
The (cid:28)rst task is to always plot the price for a brief visual inspection. In this case we’ll be
| using the | daily closing prices. | The plot | is given in | Figure 9.4. |     |     |
| --------- | --------------------- | -------- | ----------- | ----------- | --- | --- |
> plot(Cl(AMZN))
You’ll notice that quantmod adds some formatting for us, namely the date, and a slightly
| prettier chart | than the usual | R charts. |     |     |     |     |
| -------------- | -------------- | --------- | --- | --- | --- | --- |
We are now going to take the logarithmic returns of AMZN and then the (cid:28)rst-order di(cid:27)er-
ence of the series in order to convert the original price series from a non-stationary series to a
| (potentially) | stationary one. |     |     |     |     |     |
| ------------- | --------------- | --- | --- | --- | --- | --- |

83
|     |     | Figure | 9.4: | Daily Closing | Price | of AMZN. |
| --- | --- | ------ | ---- | ------------- | ----- | -------- |
This allows us to compare "apples to apples" between equities, indexes or any other asset,
for use in later multivariate statistics, such as when calculating a covariance matrix.
| Let’s    | create a new          | series,  | amznrt, | to hold our | di(cid:27)erenced | log returns: |
| -------- | --------------------- | -------- | ------- | ----------- | ----------------- | ------------ |
| > amznrt | = diff(log(Cl(AMZN))) |          |         |             |                   |              |
| Once     | again, we can         | plot the | series, | as given in | Figure            | 9.5.         |
> plot(amznrt)
At this stage we want to plot the correlogram. We’re looking to see if the di(cid:27)erenced series
looks like white noise. If it does not then there is unexplained serial correlation, which might be
| "explained"   | by an autoregressive |     | model. | See Figure | 9.6. |     |
| ------------- | -------------------- | --- | ------ | ---------- | ---- | --- |
| > acf(amznrt, | na.action=na.omit)   |     |        |            |      |     |
We notice a statististically signi(cid:28)cant peak at k =2. Hence there is a reasonable possibility
of unexplained serial correlation. Be aware though, that this may be due to sampling bias. As
such, we can try (cid:28)tting an AR(p) model to the series and produce con(cid:28)dence intervals for the
parameters:
| > amznrt.ar | <- ar(amznrt, |     | na.action=na.omit) |     |     |     |
| ----------- | ------------- | --- | ------------------ | --- | --- | --- |
> amznrt.ar$order
[1] 2
> amznrt.ar$ar
| [1] -0.02779869 | -0.06873949 |     |     |     |     |     |
| --------------- | ----------- | --- | --- | --- | --- | --- |
> amznrt.ar$asy.var
|                  | [,1]        |     | [,2] |     |     |     |
| ---------------- | ----------- | --- | ---- | --- | --- | --- |
| [1,] 4.59499e-04 | 1.19519e-05 |     |      |     |     |     |
| [2,] 1.19519e-05 | 4.59499e-04 |     |      |     |     |     |
Fitting the autoregressive model to the (cid:28)rst order di(cid:27)erenced series of log prices produces
ar
anAR(2)model,withαˆ =−0.0278andαˆ =−0.0687. I’vealsooutputtheaysmptoticvariance
|     |     | 1   |     | 2   |     |     |
| --- | --- | --- | --- | --- | --- | --- |

84
Figure 9.5: First Order Di(cid:27)erenced Daily Logarithmic Returns of AMZN Closing Prices.
Figure9.6: CorrelogramofFirstOrderDi(cid:27)erencedDailyLogarithmicReturnsofAMZNClosing
Prices.
so that we can calculate standard errors for the parameters and produce con(cid:28)dence intervals.

85
We want to see whether zero is part of the 95% con(cid:28)dence interval, as if it is, it reduces our
con(cid:28)dence that we have a true underlying AR(2) process for the AMZN series.
Tocalculatethecon(cid:28)denceintervalsatthe95%levelforeachparameter,weusethefollowing
commands. We take the square root of the (cid:28)rst element of the asymptotic variance matrix to
produce a standard error, then create con(cid:28)dence intervals by multiplying it by -1.96 and 1.96
| respectively,  | for        | the 95%    | level:              |     |     |     |     |     |
| -------------- | ---------- | ---------- | ------------------- | --- | --- | --- | --- | --- |
| > -0.0278      | + c(-1.96, |            | 1.96)*sqrt(4.59e-4) |     |     |     |     |     |
| [1] -0.0697916 |            | 0.0141916  |                     |     |     |     |     |     |
| > -0.0687      | + c(-1.96, |            | 1.96)*sqrt(4.59e-4) |     |     |     |     |     |
| [1] -0.1106916 |            | -0.0267084 |                     |     |     |     |     |     |
Note that this becomes more straightforward when using the arima function, but we’ll wait
| until the | next chapter |     | before | introducing | it properly. |     |     |     |
| --------- | ------------ | --- | ------ | ----------- | ------------ | --- | --- | --- |
Thuswecanseethatforα 1 zeroiscontainedwithinthecon(cid:28)denceinterval,whileforα 2 zero
is not contained in the con(cid:28)dence interval. Hence we should be very careful in thinking that we
| really have | an underlying |     | generative |     | AR(2) | model for | AMZN. |     |
| ----------- | ------------- | --- | ---------- | --- | ----- | --------- | ----- | --- |
In particular we note that the autoregressive model does not take into account volatility
clustering, which leads to clustering of serial correlation in (cid:28)nancial time series. When we
consider the ARCH and GARCH models in later chapters, we will account for this.
When we come to use the full arima function in the trading strategy section of the book, we
will make predictions of the daily log price series in order to allow us to create trading signals.
| S&P500 | US Equity |     | Index |     |     |     |     |     |
| ------ | --------- | --- | ----- | --- | --- | --- | --- | --- |
AlongwithindividualstockswecanalsoconsidertheUSEquityindex,theS&P500. Let’sapply
all of the previous commands to this series and produce the plots as before:
> getSymbols("^GSPC")
> GSPC
..
..
2015-08-12 2081.10 2089.06 2052.09 2086.05 4269130000 2086.05
2015-08-13 2086.19 2092.93 2078.26 2083.39 3221300000 2083.39
2015-08-14 2083.15 2092.45 2080.61 2091.54 2795590000 2091.54
| We  | can plot | the prices, | as  | given in | Figure | 9.7. |     |     |
| --- | -------- | ----------- | --- | -------- | ------ | ---- | --- | --- |
> plot(Cl(GSPC))
| As before, | we’ll                 | create | the  | (cid:28)rst order | di(cid:27)erence | of        | the log closing | prices: |
| ---------- | --------------------- | ------ | ---- | ----------------- | ---------------- | --------- | --------------- | ------- |
| > gspcrt   | = diff(log(Cl(GSPC))) |        |      |                   |                  |           |                 |         |
| Once       | again,                | we can | plot | the series,       | as given         | in Figure | 9.8.            |         |
> plot(gspcrt)
It is clear from this chart that the volatility is not stationary in time. This is also re(cid:29)ected
in the plot of the correlogram, given in Figure 9.9. There are many peaks, including k =1 and
| k =2, which | are | statistically |     | signi(cid:28)cant | beyond | a white | noise model. |     |
| ----------- | --- | ------------- | --- | ----------------- | ------ | ------- | ------------ | --- |
In addition, we see evidence of long-memory processes as there are some statistically signi(cid:28)-
| cant peaks    | at k | =16,               | k =18 | and k =21: |     |     |     |     |
| ------------- | ---- | ------------------ | ----- | ---------- | --- | --- | --- | --- |
| > acf(gspcrt, |      | na.action=na.omit) |       |            |     |     |     |     |
Ultimately we will need a more sophisticated model than an autoregressive model of order p.
However, at this stage we can still try (cid:28)tting such a model. Let’s see what we get if we do so:
| > gspcrt.ar | <-  | ar(gspcrt, |     | na.action=na.omit) |     |     |     |     |
| ----------- | --- | ---------- | --- | ------------------ | --- | --- | --- | --- |
> gspcrt.ar$order
[1] 22
> gspcrt.ar$ar

86
| Figure | 9.7: Daily Closing | Price of S&500. |
| ------ | ------------------ | --------------- |
Figure 9.8: First Order Di(cid:27)erenced Daily Logarithmic Returns of S&500 Closing Prices.
[1] -0.111821507 -0.060150504 0.018791594 -0.025619932 -0.046391435
[6] 0.002266741 -0.030089046 0.030430265 -0.007623949 0.044260402

87
Figure9.9: CorrelogramofFirstOrderDi(cid:27)erencedDailyLogarithmicReturnsofS&500Closing
Prices.
[11] -0.018924358 0.032752930 -0.001074949 -0.042891664 -0.039712505
[16] 0.052339497 0.016554471 -0.067496381 0.007070516 0.035721299
| [21] -0.035419555 |     | 0.031325869 |     |     |     |     |
| ----------------- | --- | ----------- | --- | --- | --- | --- |
Using ar produces an AR(22) model, i.e. a model with 22 non-zero parameters! What does
this tell us? It is indicative that there is likely a lot more complexity in the serial correlation
| than a simple | linear | model of past | prices can | really account | for. |     |
| ------------- | ------ | ------------- | ---------- | -------------- | ---- | --- |
However, we already knew this because we can see that there is signi(cid:28)cant serial correlation
in the volatility. For instance, consider the highly volatile period around 2008.
This motivates the next set of models, namely the Moving Average MA(q) and the Autore-
gressive Moving Average ARMA(p, q). We’ll learn about both of these in the next couple of
sections of this chapter. As we repeatedly mention, these will ultimately lead us to the ARIMA
and GARCH family of models, both of which will provide a much better (cid:28)t to the serial corre-
| lation complexity |     | of the S&P500. |     |     |     |     |
| ----------------- | --- | -------------- | --- | --- | --- | --- |
This will allows us to improve our forecasts signi(cid:28)cantly and ultimately produce more prof-
itable strategies.
| 9.5 | Moving | Average | (MA) | Models | of order | q   |
| --- | ------ | ------- | ---- | ------ | -------- | --- |
In the previous section we considered the Autoregressive model of order p, also known as the
AR(p) model. We introduced it as an extension of the random walk model in an attempt to
| explain additional |     | serial correlation | in (cid:28)nancial | time series. |     |     |
| ------------------ | --- | ------------------ | ------------------ | ------------ | --- | --- |
Ultimately we realised that it was not su(cid:30)ciently (cid:29)exible to truly capture all of the autocor-
relation in the closing prices of Amazon Inc. (AMZN) and the S&P500 US Equity Index. The
primaryreasonforthisisthatbothoftheseassetsareconditionallyheteroskedastic,whichmeans
thattheyarenon-stationaryandhaveperiodsof"varyingvariance"orvolatilityclustering,which
| is not taken | into | account by the | AR(p) model. |     |     |     |
| ------------ | ---- | -------------- | ------------ | --- | --- | --- |

88
InthenextchapterwewillconsidertheAutoregressiveIntegratedMovingAverage(ARIMA)
model, as well as the conditional heteroskedastic models of the ARCH and GARCH families.
These models will provide us with our (cid:28)rst realistic attempts at forecasting asset prices.
Inthissection, however, wearegoingtointroducetheMoving Average of order qmodel,
known as MA(q). This is a component of the more general ARMA model and as such we need
| to understand   | it  | before | moving | further. |     |     |     |     |     |
| --------------- | --- | ------ | ------ | -------- | --- | --- | --- | --- | --- |
| 9.5.1 Rationale |     |        |        |          |     |     |     |     |     |
A Moving Average model is similar to an Autoregressive model, except that instead of being a
linear combination of past time series values, it is a linear combination of the past white noise
terms.
Intuitively, this means that theMA model sees suchrandom white noise"shocks" directlyat
each current value of the model. This is in contrast to an AR(p) model, where the white noise
"shocks" are only seen indirectly, via regression onto previous terms of the series.
A key di(cid:27)erence is that the MA model will only ever see the last q shocks for any particular
MA(q) model, whereas the AR(p) model will take all prior shocks into account, albeit in a
| decreasingly           | weak | manner. |     |     |     |     |     |     |     |
| ---------------------- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- |
| 9.5.2 De(cid:28)nition |      |         |     |     |     |     |     |     |     |
Mathematically, the MA(q) is a linear regression model and is similarly structured to AR(p):
{x },
De(cid:28)nition 9.5.1. Moving Average Model of order q. A time series model, t is a moving
| average model | of   | order    | q, MA(q), | if:      |             |          |       |     |        |
| ------------- | ---- | -------- | --------- | -------- | ----------- | -------- | ----- | --- | ------ |
|               |      |          | x         | =w       | +β w +...+β |          | w     |     | (9.11) |
|               |      |          |           | t t      | 1 t−1       |          | q t−q |     |        |
| Where         | {w } | is white | noise     | with E(w | )=0 and     | variance |       | σ2. |        |
|               | t    |          |           |          | t           |          |       |     |        |
If we consider the Backward Shift Operator, B then we can rewrite the above as a function φ
of B:
|              |      | x =(1+β |            | B+β      | B2+...+β      | Bq)w      | =φ  | (B)w | (9.12) |
| ------------ | ---- | ------- | ---------- | -------- | ------------- | --------- | --- | ---- | ------ |
|              |      | t       |            | 1        | 2             | q         | t   | q t  |        |
| We will      | make | use of  | the φ      | function | in subsequent | chapters. |     |      |        |
| 9.5.3 Second |      | Order   | Properties |          |               |           |     |      |        |
As with AR(p) the mean of a MA(q) process is zero. This is easy to see as the mean is simply a
| sum of means | of  | white | noise terms, | which | are all | themselves |     | zero. |     |
| ------------ | --- | ----- | ------------ | ----- | ------- | ---------- | --- | ----- | --- |
q
(cid:88)
|     |     |     | Mean: | µ   | =E(x )= | E(w | )=0 |     | (9.13) |
| --- | --- | --- | ----- | --- | ------- | --- | --- | --- | ------ |
|     |     |     |       | x   | t       |     | i   |     |        |
i=0
σ2(1+β2+...+β2)
|     |     |     |     | Var: |     |     |     |      | (9.14) |
| --- | --- | --- | --- | ---- | --- | --- | --- | ---- | ------ |
|     |     |     |     |      | w 1 |     | q   |      |        |
|     |     |     |     | 1   |     |     |     | k =0 |        |
if

|     |     |      |     |       | q −k     | q        |     |            |     |
| --- | --- | ---- | --- | ----- | -------- | -------- | --- | ---------- | --- |
|     |     |      |     |       | (cid:88) | (cid:88) | 2   |            |     |
|     |     | ACF: |     | ρ k = | β β      | / β      | if  | k =1,...,q |     |
|     |     |      |     |       | i i+k    |          | i   |            |     |

|       |       |     |     |     | i=0 | i=0 |     |      |     |
| ----- | ----- | --- | --- | --- | --- | --- | --- | ---- | --- |
|       |       |     |     |     | 0   |     | if  | k >q |     |
| Where | β =1. |     |     |     |     |     |     |      |     |
0
We’re now going to generate some simulated data and use it to create correlograms. This
| will make | the above | formula | for | ρ somewhat | more | concrete. |     |     |     |
| --------- | --------- | ------- | --- | ---------- | ---- | --------- | --- | --- | --- |
k

89
| 9.5.4 | Simulations | and | Correlograms |     |     |
| ----- | ----------- | --- | ------------ | --- | --- |
MA(1)
Let’s start with a MA(1) process. If we set β =0.6 we obtain the following model:
1
|     |     |     | x t =w t +0.6w | t−1 | (9.15) |
| --- | --- | --- | -------------- | --- | ------ |
AswiththeAR(p)modelwecanuseRtosimulatesuchaseriesandthenplotthecorrelogram.
Since we’ve had a lot of practice in the previous sections of carrying out plots, I will write the R
| code in full, | rather than | splitting | it up: |     |     |
| ------------- | ----------- | --------- | ------ | --- | --- |
> set.seed(1)
| > x <-   | w <- rnorm(100) |         |                   |     |     |
| -------- | --------------- | ------- | ----------------- | --- | --- |
| > for (t | in 2:100)       | x[t] <- | w[t] + 0.6*w[t-1] |     |     |
> layout(1:2)
| > plot(x, | type="l") |     |     |     |     |
| --------- | --------- | --- | --- | --- | --- |
> acf(x)
| The | output is given | in Figure | 9.10. |     |     |
| --- | --------------- | --------- | ----- | --- | --- |
Figure 9.10: Realisation of MA(1) Model, with β =0.6 and Associated Correlogram
1
As we saw above in the formula for ρ , for k > q, all autocorrelations should be zero. Since
k
q =1, we should see a signi(cid:28)cant peak at k =1 and then insigni(cid:28)cant peaks subsequent to that.
However, due to sampling bias we should expect to see 5% (marginally) signi(cid:28)cant peaks on a
| sample autocorrelation |     | plot. |     |     |     |
| ---------------------- | --- | ----- | --- | --- | --- |
This is precisely what the correlogram shows us in this case. We have a signi(cid:28)cant peak
at k = 1 and then insigni(cid:28)cant peaks for k > 1, except at k = 4 where we have a marginally
| signi(cid:28)cant | peak. |     |     |     |     |
| ----------------- | ----- | --- | --- | --- | --- |
In fact, this is a useful way of seeing whether an MA(q) model is appropriate. By taking a
lookatthecorrelogramofaparticularserieswecanseehowmanysequentialnon-zerolagsexist.
If q such lags exist then we can legitimately attempt to (cid:28)t a MA(q) model to a particular series.

90
Since we have evidence from our simulated data of a MA(1) process, we’re now going to
try and (cid:28)t a MA(1) model to our simulated data. Unfortunately, there isn’t an equivalent ma
| command | to  | the autoregressive |     | model | ar command | in  | R.  |     |
| ------- | --- | ------------------ | --- | ----- | ---------- | --- | --- | --- |
Instead, we must use the more general arima command and set the autoregressive and inte-
gratedcomponentstozero. Wedothisbycreatinga3-vectorandsettingthe(cid:28)rsttwocomponents
| (the autogressive |             | and | integrated | parameters, | respectively) |     | to  | zero: |
| ----------------- | ----------- | --- | ---------- | ----------- | ------------- | --- | --- | ----- |
| > x.ma            | <- arima(x, |     | order=c(0, |             | 0, 1))        |     |     |       |
> x.ma
Call:
| arima(x | = x, | order | = c(0, | 0, 1)) |     |     |     |     |
| ------- | ---- | ----- | ------ | ------ | --- | --- | --- | --- |
Coefficients:
ma1 intercept
|      | 0.6023 | 0.1681 |     |     |     |     |     |     |
| ---- | ------ | ------ | --- | --- | --- | --- | --- | --- |
| s.e. | 0.0827 | 0.1424 |     |     |     |     |     |     |
sigma^2 estimated as 0.7958: log likelihood = -130.7, aic = 267.39
We receive some useful output from the arima command. Firstly, we can see that the
parameter has been estimated as βˆ = 0.602, which is very close to the true value of β =
1 1
0.6. Secondly, the standard errors are already calculated for us, making it straightforward to
calculate con(cid:28)dence intervals. Thirdly, we receive an estimated variance, log-likelihood and
| Akaike | Information | Criterion |     | (necessary | for model | comparison). |     |     |
| ------ | ----------- | --------- | --- | ---------- | --------- | ------------ | --- | --- |
Themajordi(cid:27)erencebetweenarimaandaristhatarimaestimatesanintercepttermbecause
itdoesnotsubtractthemeanvalueoftheseries. Henceweneedtobecarefulwhencarryingout
| predictions | using | the | arima | command. | We’ll return | to  | this point | later. |
| ----------- | ----- | --- | ----- | -------- | ------------ | --- | ---------- | ------ |
βˆ
| As a | quick | check we’re | going | to calculate | con(cid:28)dence |     | intervals | for : |
| ---- | ----- | ----------- | ----- | ------------ | ---------------- | --- | --------- | ----- |
1
| > 0.6023     | +   | c(-1.96, | 1.96)*0.0827 |     |     |     |     |     |
| ------------ | --- | -------- | ------------ | --- | --- | --- | --- | --- |
| [1] 0.440208 |     | 0.764392 |              |     |     |     |     |     |
We can see that the 95% con(cid:28)dence interval contains the true parameter value of β = 0.6
1
and so we can judge the model a good (cid:28)t. Obviously this should be expected since we simulated
| the data | in the | (cid:28)rst place! |     |     |     |     |     |     |
| -------- | ------ | ------------------ | --- | --- | --- | --- | --- | --- |
β
How do things change if we modify the sign of 1 to -0.6? Let’s perform the same analysis:
> set.seed(1)
| > x <- | w <-  | rnorm(100) |      |         |              |     |     |     |
| ------ | ----- | ---------- | ---- | ------- | ------------ | --- | --- | --- |
| > for  | (t in | 2:100)     | x[t] | <- w[t] | - 0.6*w[t-1] |     |     |     |
> layout(1:2)
| > plot(x, | type="l") |     |     |     |     |     |     |     |
| --------- | --------- | --- | --- | --- | --- | --- | --- | --- |
> acf(x)
| The | output | is given | in Figure | 9.11. |     |     |     |     |
| --- | ------ | -------- | --------- | ----- | --- | --- | --- | --- |
We can see that at k = 1 we have a signi(cid:28)cant peak in the correlogram, except that it
shows negative correlation, as we’d expect from a MA(1) model with negative (cid:28)rst coe(cid:30)cient.
Once again all peaks beyond k = 1 are insigni(cid:28)cant. Let’s (cid:28)t a MA(1) model and estimate the
parameter:
| > x.ma | <- arima(x, |     | order=c(0, |     | 0, 1)) |     |     |     |
| ------ | ----------- | --- | ---------- | --- | ------ | --- | --- | --- |
> x.ma
Call:
| arima(x | = x, | order | = c(0, | 0, 1)) |     |     |     |     |
| ------- | ---- | ----- | ------ | ------ | --- | --- | --- | --- |
Coefficients:
ma1 intercept
|     | -0.7298 |     | 0.0486 |     |     |     |     |     |
| --- | ------- | --- | ------ | --- | --- | --- | --- | --- |

91
Figure 9.11: Realisation of MA(1) Model, with β =−0.6 and Associated Correlogram
1
| s.e. | 0.1008 |     | 0.0246 |     |     |     |
| ---- | ------ | --- | ------ | --- | --- | --- |
sigma^2 estimated as 0.7841: log likelihood = -130.11, aic = 266.23
βˆ = −0.730, which is a small underestimate of β = −0.6. Finally, let’s calculate the
| 1                |            |           |              |     |     | 1   |
| ---------------- | ---------- | --------- | ------------ | --- | --- | --- |
| con(cid:28)dence | interval:  |           |              |     |     |     |
| > -0.730         | + c(-1.96, |           | 1.96)*0.1008 |     |     |     |
| [1] -0.927568    |            | -0.532432 |              |     |     |     |
Wecanseethatthetrueparametervalueofβ =−0.6iscontainedwithinthe95%con(cid:28)dence
1
| interval, | providing | us  | with evidence |     | of a good model | (cid:28)t. |
| --------- | --------- | --- | ------------- | --- | --------------- | ---------- |
MA(3)
Let’srunthroughthesameprocedureforaMA(3)process. Thistimeweshouldexpectsigni(cid:28)cant
| peaks at | k ∈{1,2,3}, |     | and insigni(cid:28)cant |     | peaks for | k >3. |
| -------- | ----------- | --- | ----------------------- | --- | --------- | ----- |
Wearegoingtousethefollowingcoe(cid:30)cients: β 1 =0.6,β 2 =0.4andβ 3 =0.3. Let’ssimulate
a MA(3) process from this model. I’ve increased the number of random samples to 1000 in this
simulation, which makes it easier to see the true autocorrelation structure, at the expense of
| making | the original | series | harder | to  | interpret: |     |
| ------ | ------------ | ------ | ------ | --- | ---------- | --- |
> set.seed(3)
| > x <- | w <- | rnorm(1000) |     |     |     |     |
| ------ | ---- | ----------- | --- | --- | --- | --- |
> for (t in 4:1000) x[t] <- w[t] + 0.6*w[t-1] + 0.4*w[t-2] + 0.3*w[t-3]
> layout(1:2)
| > plot(x, | type="l") |     |     |     |     |     |
| --------- | --------- | --- | --- | --- | --- | --- |
> acf(x)
| The | output | is given | in Figure | 9.12. |     |     |
| --- | ------ | -------- | --------- | ----- | --- | --- |

92
|     |     | Figure 9.12: | Realisation |     | of MA(3) | Model | and Associated | Correlogram |
| --- | --- | ------------ | ----------- | --- | -------- | ----- | -------------- | ----------- |
As expected the (cid:28)rst three peaks are signi(cid:28)cant. However, so is the fourth. But we can
legitimately suggest that this may be due to sampling bias as we expect to see 5% of the peaks
| being  | signi(cid:28)cant | beyond            | k =q.      |     |          |        |              |             |
| ------ | ----------------- | ----------------- | ---------- | --- | -------- | ------ | ------------ | ----------- |
|        | Let’s now         | (cid:28)t a MA(3) | model      | to  | the data | to try | and estimate | parameters: |
| > x.ma | <-                | arima(x,          | order=c(0, |     | 0, 3))   |        |              |             |
> x.ma
Call:
| arima(x | =   | x, order | = c(0, | 0,  | 3)) |     |     |     |
| ------- | --- | -------- | ------ | --- | --- | --- | --- | --- |
Coefficients:
|      | ma1    | ma2    |        | ma3 | intercept |     |     |     |
| ---- | ------ | ------ | ------ | --- | --------- | --- | --- | --- |
|      | 0.5439 | 0.3450 | 0.2975 |     | -0.0948   |     |     |     |
| s.e. | 0.0309 | 0.0349 | 0.0311 |     | 0.0704    |     |     |     |
sigma^2 estimated as 1.039: log likelihood = -1438.47, aic = 2886.95
|     |     | βˆ  |     | βˆ  |     | βˆ  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
The estimates 1 =0.544, 2 =0.345 and 3 =0.298 are close to the true values of β 1 =0.6,
β =0.4andβ =0.3,respectively. Wecanalsoproducecon(cid:28)denceintervalsusingtherespective
| 2        |          | 3        |              |     |     |     |     |     |
| -------- | -------- | -------- | ------------ | --- | --- | --- | --- | --- |
| standard | errors:  |          |              |     |     |     |     |     |
| > 0.544  | +        | c(-1.96, | 1.96)*0.0309 |     |     |     |     |     |
| [1]      | 0.483436 | 0.604564 |              |     |     |     |     |     |
| > 0.345  | +        | c(-1.96, | 1.96)*0.0349 |     |     |     |     |     |
| [1]      | 0.276596 | 0.413404 |              |     |     |     |     |     |
| > 0.298  | +        | c(-1.96, | 1.96)*0.0311 |     |     |     |     |     |
| [1]      | 0.237044 | 0.358956 |              |     |     |     |     |     |
In each case the 95% con(cid:28)dence intervals do contain the true parameter value and we can
conclude that we have a good (cid:28)t with our MA(3) model, as should be expected.

93
| 9.5.5 | Financial | Data |     |     |     |     |
| ----- | --------- | ---- | --- | --- | --- | --- |
In the previous section we considered Amazon Inc. (AMZN) and the S&P500 US Equity Index.
We (cid:28)tted the AR(p) model to both and found that the model was unable to e(cid:27)ectively capture
the complexity of the serial correlation, especially in the case of the S&P500, where conditional
| heteroskedastic |      | and long-memory |     | e(cid:27)ects | seem | to be present. |
| --------------- | ---- | --------------- | --- | ------------- | ---- | -------------- |
| Amazon          | Inc. | (AMZN)          |     |               |      |                |
Let’s begin by trying to (cid:28)t a selection of MA(q) models to AMZN, namely with q ∈{1,2,3}. As
in the previous section, we’ll use quantmod to download the daily prices for AMZN and then
| convert | them into | a log | returns | stream | of closing | prices: |
| ------- | --------- | ----- | ------- | ------ | ---------- | ------- |
> require(quantmod)
> getSymbols("AMZN")
| > amznrt | = diff(log(Cl(AMZN))) |     |     |     |     |     |
| -------- | --------------------- | --- | --- | --- | --- | --- |
Nowthatwehavethelogreturnsstreamwecanusethearimacommandto(cid:28)tMA(1),MA(2)
and MA(3) models and then estimate the parameters of each. For MA(1) we have:
| > amznrt.ma | <-  | arima(amznrt, |     | order=c(0, |     | 0, 1)) |
| ----------- | --- | ------------- | --- | ---------- | --- | ------ |
> amznrt.ma
Call:
| arima(x | = amznrt, | order |     | = c(0, | 0, 1)) |     |
| ------- | --------- | ----- | --- | ------ | ------ | --- |
Coefficients:
ma1 intercept
| -0.030 |       | 0.0012 |     |     |     |     |
| ------ | ----- | ------ | --- | --- | --- | --- |
| s.e.   | 0.023 | 0.0006 |     |     |     |     |
sigma^2 estimated as 0.0007044: log likelihood = 4796.01, aic = -9586.02
We can plot the residuals of the daily log returns and the (cid:28)tted model, given in Figure 9.13.
> acf(amznrt.ma$res[-1])
Notice that we have a few signi(cid:28)cant peaks at lags k = 2, k = 11, k = 16 and k = 18,
indicating that the MA(1) model is unlikely to be a good (cid:28)t for the behaviour of the AMZN log
| returns,    | since this  | does          | not look | like a     | realisation | of white noise. |
| ----------- | ----------- | ------------- | -------- | ---------- | ----------- | --------------- |
| Let’s       | try a MA(2) | model:        |          |            |             |                 |
| > amznrt.ma | <-          | arima(amznrt, |          | order=c(0, |             | 0, 2))          |
> amznrt.ma
Call:
| arima(x | = amznrt, | order |     | = c(0, | 0, 2)) |     |
| ------- | --------- | ----- | --- | ------ | ------ | --- |
Coefficients:
|         | ma1    |         | ma2 | intercept |     |     |
| ------- | ------ | ------- | --- | --------- | --- | --- |
| -0.0254 |        | -0.0689 |     | 0.0012    |     |     |
| s.e.    | 0.0215 | 0.0217  |     | 0.0005    |     |     |
sigma^2 estimated as 0.0007011: log likelihood = 4801.02, aic = -9594.05
Both of the estimates for the β coe(cid:30)cients are negative. Let’s plot the residuals once again,
| given in | Figure | 9.14. |     |     |     |     |
| -------- | ------ | ----- | --- | --- | --- | --- |
> acf(amznrt.ma$res[-1])
We can see that there is almost zero autocorrelation in the (cid:28)rst few lags. However, we have
(cid:28)ve marginally signi(cid:28)cant peaks at lags k = 12, k = 16, k = 19, k = 25 and k = 27. This is

94
|     | Figure 9.13: | Residuals | of MA(1) Model | Fitted to AMZN | Daily Log Prices |
| --- | ------------ | --------- | -------------- | -------------- | ---------------- |
|     | Figure 9.14: | Residuals | of MA(2) Model | Fitted to AMZN | Daily Log Prices |
suggestive that the MA(2) model is capturing a lot of the autocorrelation, but not all of the
| long-memory | e(cid:27)ects. | How about | a MA(3) model? |     |     |
| ----------- | -------------- | --------- | -------------- | --- | --- |

95
> amznrt.ma <- arima(amznrt, order=c(0, 0, 3))
> amznrt.ma
Call:
arima(x = amznrt, order = c(0, 0, 3))
Coefficients:
ma1 ma2 ma3 intercept
-0.0262 -0.0690 0.0177 0.0012
s.e. 0.0214 0.0217 0.0212 0.0005
sigma^2 estimated as 0.0007009: log likelihood = 4801.37, aic = -9592.75
Once again, we can plot the residuals, as given in Figure 9.15.
> acf(amznrt.ma$res[-1])
Figure 9.15: Residuals of MA(3) Model Fitted to AMZN Daily Log Prices
The MA(3) residuals plot looks almost identical to that of the MA(2) model. This is not
surprising,aswe’readdinganewparametertoamodelthathasseeminglyexplainedawaymuch
ofthecorrelationsatshorterlags, butthatwon’thavemuchofane(cid:27)ectonthelongertermlags.
All of this evidence is suggestive of the fact that an MA(q) model is unlikely to be useful in
explaining all of the serial correlation in isolation, at least for AMZN.
S&P500
If you recall in the previous section we saw that the (cid:28)rst order di(cid:27)erenced daily log returns
structure of the S&P500 possessed many signi(cid:28)cant peaks at various lags, both short and long.
Thisprovidedevidenceofbothconditional heteroskedasticity (i.e. volatilityclustering)andlong-
memory e(cid:27)ects. It lead us to conclude that the AR(p) model was insu(cid:30)cient to capture all of
the autocorrelation present.

96
Aswe’veseenabovetheMA(q)modelwasinsu(cid:30)cienttocaptureadditionalserialcorrelation
in the residuals of the (cid:28)tted model to the (cid:28)rst order di(cid:27)erenced daily log price series. We will
| now attempt | to  | (cid:28)t the | MA(q) | model | to the S&P500. |     |     |     |
| ----------- | --- | ------------- | ----- | ----- | -------------- | --- | --- | --- |
One might ask why we are doing this is if we know that it is unlikely to be a good (cid:28)t. This
is a good question. The answer is that we need to see exactly how it isn’t a good (cid:28)t, because
this is the ultimate process we will be following when we come across much more sophisticated
| models, | that are | potentially | harder | to  | interpret. |     |     |     |
| ------- | -------- | ----------- | ------ | --- | ---------- | --- | --- | --- |
Let’s begin by obtaining the data and converting it to a (cid:28)rst order di(cid:27)erenced series of
| logarithmically |     | transformed | daily | closing | prices | as in the | previous | section: |
| --------------- | --- | ----------- | ----- | ------- | ------ | --------- | -------- | -------- |
> getSymbols("^GSPC")
| > gspcrt | = diff(log(Cl(GSPC))) |     |     |     |     |     |     |     |
| -------- | --------------------- | --- | --- | --- | --- | --- | --- | --- |
We are now going to (cid:28)t a MA(1), MA(2) and MA(3) model to the series, as we did above for
| AMZN.       | Let’s start | with          | MA(1): |            |     |        |     |     |
| ----------- | ----------- | ------------- | ------ | ---------- | --- | ------ | --- | --- |
| > gspcrt.ma | <-          | arima(gspcrt, |        | order=c(0, |     | 0, 1)) |     |     |
> gspcrt.ma
Call:
| arima(x | = gspcrt, | order | =   | c(0, | 0, 1)) |     |     |     |
| ------- | --------- | ----- | --- | ---- | ------ | --- | --- | --- |
Coefficients:
ma1 intercept
| -0.1284 |        |     | 2e-04 |     |     |     |     |     |
| ------- | ------ | --- | ----- | --- | --- | --- | --- | --- |
| s.e.    | 0.0223 |     | 3e-04 |     |     |     |     |     |
sigma^2 estimated as 0.0001844: log likelihood = 6250.23, aic = -12494.46
Let’s make a plot of the residuals of this (cid:28)tted model, as given in Figure 9.16.
> acf(gspcrt.ma$res[-1])
The(cid:28)rstsigni(cid:28)cantpeakoccursatk =2,buttherearemanymoreatk ∈{5,10,14,15,16,18,20,21}.
This is clearly not a realisation of white noise and so we must reject the MA(1) model as a po-
| tential good | (cid:28)t     | for the       | S&P500. |             |     |        |     |     |
| ------------ | ------------- | ------------- | ------- | ----------- | --- | ------ | --- | --- |
| Does         | the situation |               | improve | with MA(2)? |     |        |     |     |
| > gspcrt.ma  | <-            | arima(gspcrt, |         | order=c(0,  |     | 0, 2)) |     |     |
> gspcrt.ma
Call:
| arima(x | = gspcrt, | order | =   | c(0, | 0, 2)) |     |     |     |
| ------- | --------- | ----- | --- | ---- | ------ | --- | --- | --- |
Coefficients:
|         | ma1    |         | ma2 intercept |       |     |     |     |     |
| ------- | ------ | ------- | ------------- | ----- | --- | --- | --- | --- |
| -0.1189 |        | -0.0524 |               | 2e-04 |     |     |     |     |
| s.e.    | 0.0216 | 0.0223  |               | 2e-04 |     |     |     |     |
sigma^2 estimated as 0.0001839: log likelihood = 6252.96, aic = -12497.92
Once again, let’s make a plot of the residuals of this (cid:28)tted MA(2) model, as given in Figure
9.17.
> acf(gspcrt.ma$res[-1])
Whilethepeakatk =2hasdisappeared(aswe’dexpect),wearestillleftwiththesigni(cid:28)cant
peaks at many longer lags in the residuals. Once again, we (cid:28)nd the MA(2) model is not a good
(cid:28)t.
We should expect, for the MA(3) model, to see less serial correlation at k = 3 than for the
| MA(2), | but once | again | we should | also | expect | no reduction | in  | further lags. |
| ------ | -------- | ----- | --------- | ---- | ------ | ------------ | --- | ------------- |

97
Figure 9.16: Residuals of MA(1) Model Fitted to S&P500 Daily Log Prices
Figure 9.17: Residuals of MA(2) Model Fitted to S&P500 Daily Log Prices
| > gspcrt.ma | <- arima(gspcrt, | order=c(0, | 0, 3)) |
| ----------- | ---------------- | ---------- | ------ |
> gspcrt.ma

98
Call:
| arima(x | = gspcrt, | order | = c(0, | 0, 3)) |
| ------- | --------- | ----- | ------ | ------ |
Coefficients:
|      | ma1     | ma2     | ma3    | intercept |
| ---- | ------- | ------- | ------ | --------- |
|      | -0.1189 | -0.0529 | 0.0289 | 2e-04     |
| s.e. | 0.0214  | 0.0222  | 0.0211 | 3e-04     |
sigma^2 estimated as 0.0001838: log likelihood = 6253.9, aic = -12497.81
Finally, let’s make a plot of the residuals of this (cid:28)tted MA(3) model, as given in Figure 9.18.
> acf(gspcrt.ma$res[-1])
Figure 9.18: Residuals of MA(3) Model Fitted to S&P500 Daily Log Prices
This is precisely what we see in the correlogram of the residuals. Hence the MA(3), as with
| the   | other models | above, is | not a good | (cid:28)t for the S&P500. |
| ----- | ------------ | --------- | ---------- | ------------------------- |
| 9.5.6 | Next         | Steps     |            |                           |
We’ve now examined two major time series models in detail, namely the Autogressive model
of order p, AR(p) and then Moving Average of order q, MA(q). We’ve seen that they’re both
capable of explaining away some of the autocorrelation in the residuals of (cid:28)rst order di(cid:27)erenced
daily log prices of equities and indices, but volatility clustering and long-memory e(cid:27)ects persist.
It is (cid:28)nally time to turn our attention to the combination of these two models, namely the
Autoregressive Moving Average of order p,q, ARMA(p,q) to see if it will improve the situation
any further.

99
| 9.6 | Autogressive |     |     | Moving |     | Average |     | (ARMA) | Models | of order |
| --- | ------------ | --- | --- | ------ | --- | ------- | --- | ------ | ------ | -------- |
|     | p, q         |     |     |        |     |         |     |        |        |          |
We’veintroducedAutoregressivemodelsandMovingAveragemodelsinthetwoprevioussections.
| Now it is | time | to combine | them | to  | produce | a more | sophisticated |     | model. |     |
| --------- | ---- | ---------- | ---- | --- | ------- | ------ | ------------- | --- | ------ | --- |
Ultimately this will lead us to the ARIMA and GARCH models that will allow us to predict
asset returns and forecast volatility. These models will form the basis for trading signals and
| risk management |     | techniques. |     |     |     |     |     |     |     |     |
| --------------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
If you’ve read the previous sections in this chapter you will have seen that we tend to follow
| a pattern                  | for our | analysis | of           | a time        | series           | model.  | I’ll repeat | it         | brie(cid:29)y here: |     |
| -------------------------- | ------- | -------- | ------------ | ------------- | ---------------- | ------- | ----------- | ---------- | ------------------- | --- |
| (cid:136) Rationale        |         | - Why    | are          | we interested |                  | in this | particular  | model?     |                     |     |
| (cid:136) De(cid:28)nition |         | - A      | mathematical |               | de(cid:28)nition | to      | reduce      | ambiguity. |                     |     |
(cid:136) Correlogram - Plotting a sample correlogram to visualise a models behaviour.
(cid:136) Simulation and Fitting - Fitting the model to simulations, in order to ensure we’ve
| understood |     | the | model | correctly. |     |     |     |     |     |     |
| ---------- | --- | --- | ----- | ---------- | --- | --- | --- | --- | --- | --- |
(cid:136)
| Real | Financial |     | Data | - Apply | the | model | to real | historical | asset prices. |     |
| ---- | --------- | --- | ---- | ------- | --- | ----- | ------- | ---------- | ------------- | --- |
However, before delving into the ARMA model we need to discuss the Bayesian Information
Criterion and the Ljung-Box test, two essential tools for helping us to choose the correct model
| and ensuring | that     | any | chosen      | model | is a      | good (cid:28)t. |     |     |     |     |
| ------------ | -------- | --- | ----------- | ----- | --------- | --------------- | --- | --- | --- | --- |
| 9.6.1        | Bayesian |     | Information |       | Criterion |                 |     |     |     |     |
IntheprevioussectionwelookedattheAkaikeInformationCriterion(AIC)asameansofhelping
| us choose | between | separate |     | "best" | time | series models. |     |     |     |     |
| --------- | ------- | -------- | --- | ------ | ---- | -------------- | --- | --- | --- | --- |
A closely related tool is the Bayesian Information Criterion (BIC). Essentially it has
similar behaviour to the AIC in that it penalises models for having too many parameters. This
mayleadtoover(cid:28)tting. Thedi(cid:27)erencebetweentheBICandAICisthattheBICismorestringent
| with its | penalisation |     | of additional |     | parameters. |     |     |     |     |     |
| -------- | ------------ | --- | ------------- | --- | ----------- | --- | --- | --- | --- | --- |
De(cid:28)nition 9.6.1. Bayesian Information Criterion. If we take the likelihood function for a
statistical model, which has k parameters, and L maximises the likelihood, then the Bayesian
| Information | Criterion |            | is given | by:     |                   |        |              |     |     |        |
| ----------- | --------- | ---------- | -------- | ------- | ----------------- | ------ | ------------ | --- | --- | ------ |
|             |           |            |          | BIC     | =−2log(L)+klog(n) |        |              |     |     | (9.16) |
| Where       | n is      | the number |          | of data | points            | in the | time series. |     |     |        |
We will be using the AIC and BIC below when choosing appropriate ARMA(p,q) models.
| 9.6.2 | Ljung-Box |     | Test |     |     |     |     |     |     |     |
| ----- | --------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
TheLjung-Box testisaclassical(inastatisticalsense)hypothesistestthatisdesignedtotest
whether a set of autocorrelations of a (cid:28)tted time series model di(cid:27)er signi(cid:28)cantly from zero. The
test does not test each individual lag for randomness, but rather tests the randomness over a
| group of | lags. | Formally: |     |     |     |     |     |     |     |     |
| -------- | ----- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
De(cid:28)nition 9.6.2. Ljung-Box Test. We de(cid:28)ne the null hypothesis H as: The time series data
0
at each lag are independent and identically distributed (i.i.d.), that is, the correlations between
| the population |     | series | values | are zero. |     |     |     |     |     |     |
| -------------- | --- | ------ | ------ | --------- | --- | --- | --- | --- | --- | --- |
We de(cid:28)ne the alternate hypothesis H as: The time series data are not i.i.d. and possess
a
serial correlation.
| We calculate |     | the | following | test | statistic, | Q:  |     |     |     |     |
| ------------ | --- | --- | --------- | ---- | ---------- | --- | --- | --- | --- | --- |

100
h ρˆ2
(cid:88)
|     |     |     |     | Q=n(n+2) |     | k   |     | (9.17) |
| --- | --- | --- | --- | -------- | --- | --- | --- | ------ |
n−k
k=1
Wherenisthelengthofthetimeseriessample,ρˆ isthesampleautocorrelationatlagk and
k
| h is the | number of | lags under | the | test. |     |     |     |     |
| -------- | --------- | ---------- | --- | ----- | --- | --- | --- | --- |
istocheckwhetherQ>χ2
| ThedecisionruleastowhethertorejectthenullhypothesisH |     |     |     |     |     |     | 0   | ,   |
| ---------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
α,h
for a chi-squared distribution with h degrees of freedom at the 100(1−α)th percentile.
Whilethedetailsofthetestmayseemslightlycomplex, wecaninfactuseRtocalculatethe
| test for | us, simplifying | the | procedure | somewhat. |     |     |     |     |
| -------- | --------------- | --- | --------- | --------- | --- | --- | --- | --- |
Now that we’ve discussed the BIC and the Ljung-Box test, we’re ready to discuss our (cid:28)rst
mixed model, namely the Autoregressive Moving Average of order p, q, or ARMA(p,q).
| 9.6.3 | Rationale |     |     |     |     |     |     |     |
| ----- | --------- | --- | --- | --- | --- | --- | --- | --- |
To date we have considered autoregressive processes and moving average processes.
The former model considers its own past behaviour as inputs for the model and as such
attempts to capture market participant e(cid:27)ects, such as momentum and mean-reversion in stock
trading. The latter model is used to characterise "shock" information to a series, such as a
surprise earnings announcement or other unexpected event. A good example of "shock" news
| would be | the BP Deepwater |     | Horizon | oil spill. |     |     |     |     |
| -------- | ---------------- | --- | ------- | ---------- | --- | --- | --- | --- |
Hence, an ARMA model attempts to capture both of these aspects when modelling (cid:28)nancial
timeseries. Notehoweverthatitdoes not takeintoaccountvolatilityclustering, akeyempirical
phenomenaofmany(cid:28)nancialtimeseries. Itisnotaconditionalheteroskedasticmodel. Forthat
| we will | need to wait     | for the | ARCH | and GARCH | models. |     |     |     |
| ------- | ---------------- | ------- | ---- | --------- | ------- | --- | --- | --- |
| 9.6.4   | De(cid:28)nition |         |      |           |         |     |     |     |
TheARMA(p,q)modelisalinearcombinationoftwolinearmodelsandthusisitselfstilllinear:
De(cid:28)nition 9.6.3. Autoregressive Moving Average Model of order p, q. A time series model,
{x }, is an autoregressive moving average model of order p,q, ARMA(p,q), if:
t
x t =α 1 x t−1 +α 2 x t−2 +...+w t +β 1 w t−1 +β 2 w t−2 ...+β q w t−q (9.18)
σ2.
| Where | {w t } is white | noise | with | E(w t )=0 | and | variance |     |     |
| ----- | --------------- | ----- | ---- | --------- | --- | -------- | --- | --- |
If we consider the Backward Shift Operator, B then we can rewrite the above as a function θ
φ B:
and of
|     |     |     |     | θ (B)x | =φ (B)w |     |     | (9.19) |
| --- | --- | --- | --- | ------ | ------- | --- | --- | ------ |
|     |     |     |     | p      | t q     | t   |     |        |
We can straightforwardly see that by setting p (cid:54)= 0 and q = 0 we recover the AR(p) model.
|           |           | p=0 | q (cid:54)=0 |            |     |              |     |     |
| --------- | --------- | --- | ------------ | ---------- | --- | ------------ | --- | --- |
| Similarly | if we set | and |              | we recover | the | MA(q) model. |     |     |
One of the key features of the ARMA model is that it is parsimonious and redundant in its
parameters. That is, an ARMA model will often require fewer parameters than an AR(p) or
MA(q) model alone. In addition if we rewrite the equation in terms of the BSO, then the θ and
φ polynomials can sometimes share a common factor, thus leading to a simpler model.
| 9.6.5 | Simulations |     | and Correlograms |     |     |     |     |     |
| ----- | ----------- | --- | ---------------- | --- | --- | --- | --- | --- |
As with the autoregressive and moving average models we will now simulate various ARMA
seriesandthenattemptto(cid:28)tARMAmodelstotheserealisations. Wecarrythisoutbecausewe
want to ensure that we understand the (cid:28)tting procedure, including how to calculate con(cid:28)dence
intervals for the models, as well as ensure that the procedure does actually recover reasonable
| estimates | for the original |     | ARMA | parameters. |     |     |     |     |
| --------- | ---------------- | --- | ---- | ----------- | --- | --- | --- | --- |

101
N
In the previous sections we manually constructed the AR and MA series by drawing
samples from a normal distribution and then crafting the speci(cid:28)c time series model using lags of
these samples.
However,thereisamorestraightforwardwaytosimulateAR,MA,ARMAandevenARIMA
| data, | simply | by using | the arima.sim |     | method | in  | R.  |     |     |
| ----- | ------ | -------- | ------------- | --- | ------ | --- | --- | --- | --- |
Let’s start with the simplest possible non-trivial ARMA model, namely the ARMA(1,1)
model. That is, an autoregressive model of order one combined with a moving average model of
order one. Such a model has only two coe(cid:30)cients, α and β, which represent the (cid:28)rst lags of the
time series itself and the "shock" white noise terms. Such a model is given by:
|     |     |     |     | x   | =αx | +w  | +βw   |     | (9.20) |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | ------ |
|     |     |     |     |     | t   | t−1 | t t−1 |     |        |
We need to specify the coe(cid:30)cients prior to simulation. Let’s take α=0.5 and β =−0.5:
> set.seed(1)
| > x | <- arima.sim(n=1000, |     |     | model=list(ar=0.5, |     |     | ma=-0.5)) |     |     |
| --- | -------------------- | --- | --- | ------------------ | --- | --- | --------- | --- | --- |
> plot(x)
| The | output | is  | given in | Figure | 9.19. |     |     |     |     |
| --- | ------ | --- | -------- | ------ | ----- | --- | --- | --- | --- |
α=0.5 β =−0.5
|       | Figure | 9.19: | Realisation      |     | of an ARMA(1,1) |           | Model, with | and |     |
| ----- | ------ | ----- | ---------------- | --- | --------------- | --------- | ----------- | --- | --- |
| Let’s | also   | plot  | the correlogram, |     | as given        | in Figure | 9.20.       |     |     |
> acf(x)
We can see that there is no signi(cid:28)cant autocorrelation, which is to be expected from an
| ARMA(1,1) |     | model. |     |     |     |     |     |     |     |
| --------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
Finally, let’s try and determine the coe(cid:30)cients and their standard errors using the arima
function:
| > arima(x, |     | order=c(1, |     | 0, 1)) |     |     |     |     |     |
| ---------- | --- | ---------- | --- | ------ | --- | --- | --- | --- | --- |
Call:

102
Figure 9.20: Correlogram of an ARMA(1,1) Model, with α=0.5 and β =−0.5
| arima(x | = x, | order | = c(1, | 0, 1)) |     |     |     |
| ------- | ---- | ----- | ------ | ------ | --- | --- | --- |
Coefficients:
|         | ar1    |        | ma1 | intercept |     |     |     |
| ------- | ------ | ------ | --- | --------- | --- | --- | --- |
| -0.3957 |        | 0.4503 |     | 0.0538    |     |     |     |
| s.e.    | 0.3727 | 0.3617 |     | 0.0337    |     |     |     |
sigma^2 estimated as 1.053: log likelihood = -1444.79, aic = 2897.58
We can calculate the con(cid:28)dence intervals for each parameter using the standard errors:
| > -0.396     | + c(-1.96, |         | 1.96)*0.373 |     |     |     |     |
| ------------ | ---------- | ------- | ----------- | --- | --- | --- | --- |
| [1] -1.12708 |            | 0.33508 |             |     |     |     |     |
| > 0.450      | + c(-1.96, |         | 1.96)*0.362 |     |     |     |     |
| [1] -0.25952 |            | 1.15952 |             |     |     |     |     |
The con(cid:28)dence intervals do contain the true parameter values for both cases, however we
should note that the 95% con(cid:28)dence intervals are very wide (a consequence of the reasonably
| large standard |     | errors). |     |     |     |     |     |
| -------------- | --- | -------- | --- | --- | --- | --- | --- |
Let’s now try an ARMA(2,2) model. That is, an AR(2) model combined with a MA(2)
model. We need to specify four parameters for this model: α , α , β and β . Let’s take
1 2 1 2
| α 1 =0.5, | α 2 =−0.25 |     | β 1 =0.5 | and β 2 | =−0.3: |     |     |
| --------- | ---------- | --- | -------- | ------- | ------ | --- | --- |
> set.seed(1)
> x <- arima.sim(n=1000, model=list(ar=c(0.5, -0.25), ma=c(0.5, -0.3)))
> plot(x)
| The | output            | of our | ARMA(2,2)       | model | is given | in       | Figure 9.21. |
| --- | ----------------- | ------ | --------------- | ----- | -------- | -------- | ------------ |
| And | the corresponding |        | autocorelation, |       | as       | given in | Figure 9.22. |
> acf(x)
| We can | now | try (cid:28)tting | an  | ARMA(2,2) | model | to  | the data: |
| ------ | --- | ----------------- | --- | --------- | ----- | --- | --------- |

103
Figure 9.21: Realisation of an ARMA(2,2) Model, with α = 0.5, α = −0.25, β = 0.5 and
1 2 1
β =−0.3
2
Figure 9.22: Correlogram of an ARMA(2,2) Model, with α = 0.5, α = −0.25, β = 0.5 and
1 2 1
β =−0.3
2

104
> arima(x, order=c(2, 0, 2))
Call:
arima(x = x, order = c(2, 0, 2))
Coefficients:
ar1 ar2 ma1 ma2 intercept
0.6529 -0.2291 0.3191 -0.5522 -0.0290
s.e. 0.0802 0.0346 0.0792 0.0771 0.0434
sigma^2 estimated as 1.06: log likelihood = -1449.16, aic = 2910.32
We can also calculate the con(cid:28)dence intervals for each parameter:
> 0.653 + c(-1.96, 1.96)*0.0802
[1] 0.495808 0.810192
> -0.229 + c(-1.96, 1.96)*0.0346
[1] -0.296816 -0.161184
> 0.319 + c(-1.96, 1.96)*0.0792
[1] 0.163768 0.474232
> -0.552 + c(-1.96, 1.96)*0.0771
[1] -0.703116 -0.400884
Notice that the con(cid:28)dence intervals for the coe(cid:30)cients for the moving average component
(β and β ) do not actually contain the original parameter value. This outlines the danger of
1 2
attempting to (cid:28)t models to data, even when we know the true parameter values!
However, for trading purposes we just need to have a predictive power that exceeds chance
and produces enough pro(cid:28)t above transaction costs, in order to be pro(cid:28)table in the long run.
Now that we’ve seen some examples of simulated ARMA models we need a mechanism for
choosing the values of p and q when (cid:28)tting to the models to real (cid:28)nancial data.
9.6.6 Choosing the Best ARMA(p,q) Model
In order to determine which order p,q of the ARMA model is appropriate for a series, we need
to use the AIC (or BIC) across a subset of values for p,q, and then apply the Ljung-Box test to
determine if a good (cid:28)t has been achieved, for particular values of p,q.
To show this method we are going to (cid:28)rstly simulate a particular ARMA(p,q) process. We
will then loop over all pairwise values of p ∈ {0,1,2,3,4} and q ∈ {0,1,2,3,4} and calculate
the AIC. We will select the model with the lowest AIC and then run a Ljung-Box test on the
residuals to determine if we have achieved a good (cid:28)t.
Let’s begin by simulating an ARMA(3,2) series:
> set.seed(3)
> x <- arima.sim(n=1000, model=list(ar=c(0.5, -0.25, 0.4), ma=c(0.5, -0.3)))
Wewillnowcreateanobjectfinaltostorethebestmodel(cid:28)tandlowestAICvalue. Weloop
over the various p,q combinations and use the current object to store the (cid:28)t of an ARMA(i,j)
model, for the looping variables i and j.
If the current AIC is less than any previously calculated AIC we set the (cid:28)nal AIC to this
current value and select that order. Upon termination of the loop we have the order of the
ARMA model stored in final.order and the ARIMA(p,d,q) (cid:28)t itself (with the "Integrated" d
component set to 0) stored as final.arma:
> final.aic <- Inf
> final.order <- c(0,0,0)
> for (i in 0:4) for (j in 0:4) {
> current.aic <- AIC(arima(x, order=c(i, 0, j)))
> if (current.aic < final.aic) {
> final.aic <- current.aic

105
| >   | final.order |     | <- c(i,  | 0,  | j)                 |     |     |     |
| --- | ----------- | --- | -------- | --- | ------------------ | --- | --- | --- |
| >   | final.arma  | <-  | arima(x, |     | order=final.order) |     |     |     |
> }
> }
|     | Let’s output | the AIC, | order | and | ARIMA | coe(cid:30)cients: |     |     |
| --- | ------------ | -------- | ----- | --- | ----- | ------------------ | --- | --- |
> final.aic
[1] 2863.365
> final.order
| [1] | 3 0 2 |     |     |     |     |     |     |     |
| --- | ----- | --- | --- | --- | --- | --- | --- | --- |
> final.arma
Call:
| arima(x | =   | x, order | = final.order) |     |     |     |     |     |
| ------- | --- | -------- | -------------- | --- | --- | --- | --- | --- |
Coefficients:
|      | ar1    |         | ar2 | ar3    |        | ma1     | ma2    | intercept |
| ---- | ------ | ------- | --- | ------ | ------ | ------- | ------ | --------- |
|      | 0.4470 | -0.2822 |     | 0.4079 | 0.5519 | -0.2367 |        | 0.0274    |
| s.e. | 0.0867 | 0.0345  |     | 0.0309 | 0.0954 |         | 0.0905 | 0.0975    |
sigma^2 estimated as 1.009: log likelihood = -1424.68, aic = 2863.36
WecanseethattheoriginalorderofthesimulatedARMAmodelwasrecovered,namelywith
p = 3 and q = 2. We can plot the corelogram of the residuals of the model to see if they look
| like | a realisation | of discrete |     | white | noise (DWN), |     | as given in | Figure 9.23. |
| ---- | ------------- | ----------- | --- | ----- | ------------ | --- | ----------- | ------------ |
> acf(resid(final.arma))
Figure9.23: Correlogramoftheresidualsofthebest(cid:28)ttingARMA(p,q)Model, p=3andq =2

106
ThecorelogramdoesindeedlooklikearealisationofDWN.Finally,weperformtheLjung-Box
| test for                      | 20 lags | to con(cid:28)rm | this: |     |         |                   |     |     |
| ----------------------------- | ------- | ---------------- | ----- | --- | ------- | ----------------- | --- | --- |
| > Box.test(resid(final.arma), |         |                  |       |     | lag=20, | type="Ljung-Box") |     |     |
| Box-Ljung                     |         | test             |       |     |         |                   |     |     |
data: resid(final.arma)
| X-squared | =   | 13.1927, | df  | = 20, | p-value | = 0.869 |     |     |
| --------- | --- | -------- | --- | ----- | ------- | ------- | --- | --- |
Notice that the p-value is greater than 0.05, which states that the residuals are independent
| at the 95% | level | and | thus an | ARMA(3,2) |     | model provides | a good model | (cid:28)t. |
| ---------- | ----- | --- | ------- | --------- | --- | -------------- | ------------ | ---------- |
Clearly this should be the case since we’ve simulated the data ourselves! However, this is
preciselytheprocedurewewillusewhenwecometo(cid:28)tARMA(p,q)modelstotheS&P500index
| in the following |           | section. |      |     |     |     |     |     |
| ---------------- | --------- | -------- | ---- | --- | --- | --- | --- | --- |
| 9.6.7            | Financial |          | Data |     |     |     |     |     |
Nowthatwe’veoutlinedtheprocedureforchoosingtheoptimaltimeseriesmodelforasimulated
series, it is rather straightforward to apply it to (cid:28)nancial data. For this example we are going to
| once again | choose | the | S&P500 | US  | Equity | Index. |     |     |
| ---------- | ------ | --- | ------ | --- | ------ | ------ | --- | --- |
Let’s download the daily closing prices using quantmod and then create the log returns
stream:
> require(quantmod)
> getSymbols("^GSPC")
> sp = diff(log(Cl(GSPC)))
Let’sperformthesame(cid:28)ttingprocedureasforthesimulatedARMA(3,2)seriesaboveonthe
| log returns     | series         | of   | the S&P500       | using          | the                  | AIC:       |         |     |
| --------------- | -------------- | ---- | ---------------- | -------------- | -------------------- | ---------- | ------- | --- |
| > spfinal.aic   |                | <-   | Inf              |                |                      |            |         |     |
| > spfinal.order |                | <-   | c(0,0,0)         |                |                      |            |         |     |
| > for           | (i in          | 0:4) | for (j           | in 0:4)        | {                    |            |         |     |
| > spcurrent.aic |                |      | <- AIC(arima(sp, |                |                      | order=c(i, | 0, j))) |     |
| > if            | (spcurrent.aic |      |                  | < spfinal.aic) |                      | {          |         |     |
| >               | spfinal.aic    |      | <- spcurrent.aic |                |                      |            |         |     |
| >               | spfinal.order  |      | <-               | c(i,           | 0, j)                |            |         |     |
| >               | spfinal.arma   |      | <-               | arima(sp,      | order=spfinal.order) |            |         |     |
> }
> }
| The | best (cid:28)tting | model | has | order | ARMA(3,3): |     |     |     |
| --- | ------------------ | ----- | --- | ----- | ---------- | --- | --- | --- |
> spfinal.order
| [1] 3 | 0 3 |     |     |     |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- |
Let’s plot the residuals of the (cid:28)tted model to the S&P500 log daily returns stream, as given
| in Figure                  | 9.24: |     |     |                    |     |     |     |     |
| -------------------------- | ----- | --- | --- | ------------------ | --- | --- | --- | --- |
| > acf(resid(spfinal.arma), |       |     |     | na.action=na.omit) |     |     |     |     |
Notice that there are some signi(cid:28)cant peaks, especially at higher lags. This is indicative of a
poor (cid:28)t. Let’s perform a Ljung-Box test to see if we have statistical evidence for this:
| > Box.test(resid(spfinal.arma), |     |      |     |     | lag=20, | type="Ljung-Box") |     |     |
| ------------------------------- | --- | ---- | --- | --- | ------- | ----------------- | --- | --- |
| Box-Ljung                       |     | test |     |     |         |                   |     |     |
data: resid(spfinal.arma)
| X-squared | =   | 37.1912, | df  | = 20, | p-value | = 0.0111 |     |     |
| --------- | --- | -------- | --- | ----- | ------- | -------- | --- | --- |

107
Figure9.24: Correlogramoftheresidualsofthebest(cid:28)ttingARMA(p,q)Model,p=3andq =3,
| to the S&P500 | daily | log returns | stream |     |     |
| ------------- | ----- | ----------- | ------ | --- | --- |
Aswesuspected,thep-valueisless that0.05andassuchwecannotsaythattheresidualsare
a realisation of discrete white noise. Hence there is additional autocorrelation in the residuals
| that is not | explained | by the | (cid:28)tted ARMA(3,3) | model. |     |
| ----------- | --------- | ------ | ---------------------- | ------ | --- |
| 9.7         | Next      | Steps  |                        |        |     |
As we’ve discussed all along in this part of the book we have seen evidence of conditional het-
eroskedasticity(volatilityclustering)intheS&P500series,especiallyintheperiodsaround2007-
2008. When we use a GARCH model in the next chapter we will see how to eliminate these
autocorrelations.
In practice, ARMA models are never generally good (cid:28)ts for log equities returns. We need
to take into account the conditional heteroskedasticity and use a combination of ARIMA and
GARCH. The next chapter will consider ARIMA and show how the "Integrated" component
| di(cid:27)ers from | the ARMA | model | we have been | considering | in this chapter. |
| ------------------ | -------- | ----- | ------------ | ----------- | ---------------- |

108

| Chapter         |     | 10  |     |             |            |     |        |
| --------------- | --- | --- | --- | ----------- | ---------- | --- | ------ |
| Autoregressive  |     |     |     |             | Integrated |     | Moving |
| Average         |     |     | and | Conditional |            |     |        |
| Heteroskedastic |     |     |     |             | Models     |     |        |
Inthepreviouschapterwewentintosigni(cid:28)cantdetailabouttheAR(p),MA(q)andARMA(p,q)
linear time series models. We used these models to generate simulated data sets, (cid:28)tted models
to recover parameters and then applied these models to (cid:28)nancial equities data.
In this chapter we are going to discuss an extension of the ARMA model, namely the Au-
toregressive Integrated Moving Average model, or ARIMA(p,d,q) model as well as models that
| incorporate | conditional |     | heteroskedasticity, |     | such as | ARCH and GARCH. |     |
| ----------- | ----------- | --- | ------------------- | --- | ------- | --------------- | --- |
We will see that it is necessary to consider the ARIMA model when we have non-stationary
| series. | Such series | occur | in the | presence | of stochastic | trends. |     |
| ------- | ----------- | ----- | ------ | -------- | ------------- | ------- | --- |
| 10.1    | Quick       |       | Recap  |          |               |         |     |
We have steadily built up our understanding of time series with concepts such as serial corre-
lation, stationarity, linearity, residuals, correlograms, simulating, (cid:28)tting, seasonality, conditional
| heteroscedasticity |     | and | hypothesis | testing. |     |     |     |
| ------------------ | --- | --- | ---------- | -------- | --- | --- | --- |
As of yet we have not carried out any prediction or forecasting from our models and so have
| not had | any mechanism |     | for producing |     | a trading system | or equity | curve. |
| ------- | ------------- | --- | ------------- | --- | ---------------- | --------- | ------ |
Once we have studied ARIMA we will be in a position to build a basic long-term trading
| strategy | based | on prediction |     | of stock | market index | returns. |     |
| -------- | ----- | ------------- | --- | -------- | ------------ | -------- | --- |
Despite the fact that I have gone into a lot of detail about models which we know will
ultimatelynothavegreatperformance(AR,MA,ARMA),wearenowwell-versedintheprocess
| of time | series | modeling. |     |     |     |     |     |
| ------- | ------ | --------- | --- | --- | --- | --- | --- |
This means that when we come to study more recent models (and even those currently in
the research literature), we will have a signi(cid:28)cant knowledge base on which to draw, in order to
e(cid:27)ectivelyevaluatethesemodels, insteadoftreatingthemasa"turnkey"prescriptionor"black
box".
More importantly, it will provide us with the con(cid:28)dence to extend and modify them on our
| own and | understand |     | what we | are doing | when we | do it! |     |
| ------- | ---------- | --- | ------- | --------- | ------- | ------ | --- |
I’d like to thank you for being patient so far, as it might seem that these chapters on time
series analysis theory are far away from the "real action" of actual trading. However, true
quantitative trading research is careful, measured and takes signi(cid:28)cant time to get right. There
| is no quick | (cid:28)x | or "get | rich scheme" |     | in quant trading. |     |     |
| ----------- | --------- | ------- | ------------ | --- | ----------------- | --- | --- |
We’reverynearlyreadytoconsiderour(cid:28)rsttradingmodel,whichwillbeamixtureofARIMA
andGARCH,soitisimperativethatwespendsometimeunderstandingtheARIMAmodelwell!
Once we have built our (cid:28)rst trading model, we are going to consider more advanced models
in subsequent chapters including long-memory processes, state-space models (i.e. the Kalman
109

110
Filter)andVectorAutoregressive(VAR)models,whichwillleadustoother,moresophisticated,
trading strategies.
| 10.2   | Autoregressive |     |     |       | Integrated |     | Moving | Average | (ARIMA) |     |
| ------ | -------------- | --- | --- | ----- | ---------- | --- | ------ | ------- | ------- | --- |
|        | Models         |     | of  | order | p, d,      | q   |        |         |         |     |
| 10.2.1 | Rationale      |     |     |       |            |     |        |         |         |     |
ARIMA models are used because they can reduce a non-stationary series to a stationary series
| using | a sequence | of  | di(cid:27)erencing |     | steps. |     |     |     |     |     |
| ----- | ---------- | --- | ------------------ | --- | ------ | --- | --- | --- | --- | --- |
We can recall from the previous chapter on white noise and random walks that if we apply
the di(cid:27)erence operator to a random walk series {x } (a non-stationary series) we are left with
t
| white | noise | {w } (a | stationary |     | series): |     |     |     |     |     |
| ----- | ----- | ------- | ---------- | --- | -------- | --- | --- | --- | --- | --- |
t
|     |     |     |     |     | ∇x =x | −x    | =w  |     |     | (10.1) |
| --- | --- | --- | --- | --- | ----- | ----- | --- | --- | --- | ------ |
|     |     |     |     |     | t     | t t−1 | t   |     |     |        |
ARIMA essentially performs this function but does so repeatedly d times in order to reduce
a non-stationary series to a stationary one. In order to handle other forms of non-stationarity
| beyond | stochastic |     | trends | additional | models | can be | used. |     |     |     |
| ------ | ---------- | --- | ------ | ---------- | ------ | ------ | ----- | --- | --- | --- |
Seasonality e(cid:27)ects such as those that occur in commodity prices can be tackled with the
Seasonal ARIMA model (SARIMA), however we won’t be discussing SARIMA much in this
book. Conditional heteroskedastic e(cid:27)ects, such as volatility clustering in equities indexes, can
be tackled with ARCH and GARCH, which we discuss later in this chapter.
In this chapter we will (cid:28)rst be considering non-stationary series with stochastic trends and
(cid:28)t ARIMA models to these series. We will also (cid:28)nally produce forecasts for our (cid:28)nancial series.
| 10.2.2 | De(cid:28)nitions |     |     |     |     |     |     |     |     |     |
| ------ | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Prior to de(cid:28)ning ARIMA processes we need to discuss the concept of an integrated series:
|                  |     |         | IntegratedSeriesoforderd. |     |     | Atimeseries{x |     | }isintegrated |          | d,I(d), |
| ---------------- | --- | ------- | ------------------------- | --- | --- | ------------- | --- | ------------- | -------- | ------- |
| De(cid:28)nition |     | 10.2.1. |                           |     |     |               |     | t             | of order |         |
if:
∇dx
|     |     |     |     |     |     | t =w t |     |     |     | (10.2) |
| --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | ------ |
That is, if we di(cid:27)erence the series d times we receive a discrete white noise series.
Alternatively, using the Backward Shift Operator B an equivalent condition is:
|     |     |     |     |     | (1−Bd)x | =w  |     |     |     |        |
| --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | ------ |
|     |     |     |     |     |         | t   | t   |     |     | (10.3) |
Now that we have de(cid:28)ned an integrated series we can de(cid:28)ne the ARIMA process itself:
De(cid:28)nition 10.2.2. Autoregressive Integrated Moving Average Model of order p, d, q. A time
series{x }isanautoregressiveintegratedmovingaveragemodeloforderp,d,q,ARIMA(p,d,q),
t
if ∇dx is an autoregressive moving average model of order p,q, ARMA(p,q).
t
That is, if the series {x } is di(cid:27)erenced d times, and it then follows an ARMA(p,q) process,
t
| then it | is an | ARIMA(p,d,q) |     | series. |     |     |     |     |     |     |
| ------- | ----- | ------------ | --- | ------- | --- | --- | --- | --- | --- | --- |
IfweusethepolynomialnotationfromthepreviouschapteronARMAthenanARIMA(p,d,q)
B:
| process | can | be written | in       | terms | of the Backward | Shift | Operator, |     |     |        |
| ------- | --- | ---------- | -------- | ----- | --------------- | ----- | --------- | --- | --- | ------ |
|         |     |            |          |       | θ (B)(1−B)dx    | =φ    | (B)w      |     |     | (10.4) |
|         |     |            |          |       | p               | t     | q t       |     |     |        |
| Where   | w   | is a       | discrete | white | noise series.   |       |           |     |     |        |
t

111
There are some points to note about these de(cid:28)nitions.
Since the random walk is given by x = x + w it can be seen that I(1) is another
t t−1 t
representation, since ∇1x =w .
t t
Ifwesuspectanon-lineartrendthenwemightbeabletouserepeateddi(cid:27)erencing(i.e. d>1)
to reduce a series to stationary white noise. In R we can use the diff command with additional
parameters, e.g. diff(x, d=3) to carry out repeated di(cid:27)erences.
10.2.3 Simulation, Correlogram and Model Fitting
Sincewehavealreadymadeuseofthearima.simcommandtosimulateanARMA(p,q)process,
the following procedure will be similar to that carried out in the previous chapter.
The major di(cid:27)erence is that we will now set d=1, that is, we will produce a non-stationary
time series with a stochastic trending component.
As before we will (cid:28)t an ARIMA model to our simulated data, attempt to recover the param-
eters, create con(cid:28)dence intervals for these parameters, produce a correlogram of the residuals of
the (cid:28)tted model and (cid:28)nally carry out a Ljung-Box test to establish whether we have a good (cid:28)t.
WearegoingtosimulateanARIMA(1,1,1)model,withtheautoregressivecoe(cid:30)cientα=0.6
and the moving average coe(cid:30)cient β = −0.5. Here is the R code to simulate and plot such a
series, see Figure 10.1.
> set.seed(2)
> x <- arima.sim(list(order = c(1,1,1), ar = 0.6, ma=-0.5), n = 1000)
> plot(x)
Figure 10.1: Plot of simulated ARIMA(1,1,1) model with α=0.6 and β =−0.5
Now that we have our simulated series we are going to try and (cid:28)t an ARIMA(1,1,1) model
to it. Since we know the order we will simply specify it in the (cid:28)t:
> x.arima <- arima(x, order=c(1, 1, 1))
Call:

112
| arima(x | = x, order | = c(1, 1, 1)) |     |     |
| ------- | ---------- | ------------- | --- | --- |
Coefficients:
|             | ar1     | ma1 |     |     |
| ----------- | ------- | --- | --- | --- |
| 0.6470      | -0.5165 |     |     |     |
| s.e. 0.1065 | 0.1189  |     |     |     |
sigma^2 estimated as 1.027: log likelihood = -1432.09, aic = 2870.18
| The           | con(cid:28)dence intervals | are calculated | as: |     |
| ------------- | -------------------------- | -------------- | --- | --- |
| > 0.6470      | + c(-1.96,                 | 1.96)*0.1065   |     |     |
| [1] 0.43826   | 0.85574                    |                |     |     |
| > -0.5165     | + c(-1.96,                 | 1.96)*0.1189   |     |     |
| [1] -0.749544 | -0.283456                  |                |     |     |
Bothparameterestimatesfallwithinthecon(cid:28)denceintervalsandareclosetothetrueparam-
etervaluesofthesimulatedARIMAseries. Hence,weshouldn’tbesurprisedtoseetheresiduals
| looking | like a realisation | of discrete white | noise, see Figure | 10.2. |
| ------- | ------------------ | ----------------- | ----------------- | ----- |
> acf(resid(x.arima))
Figure 10.2: Correlogram of the residuals of the (cid:28)tted ARIMA(1,1,1) model
Finally, we can run a Ljung-Box test to provide statistical evidence of a good (cid:28)t:
| > Box.test(resid(x.arima), |      | lag=20, | type="Ljung-Box") |     |
| -------------------------- | ---- | ------- | ----------------- | --- |
| Box-Ljung                  | test |         |                   |     |
data: resid(x.arima)
| X-squared | = 19.0413, | df = 20, p-value | = 0.5191 |     |
| --------- | ---------- | ---------------- | -------- | --- |

113
We can see that the p-value is signi(cid:28)cantly larger than 0.05 and as such we can state that
there is strong evidence for discrete white noise being a good (cid:28)t to the residuals. Hence, the
| ARIMA(1,1,1) |           | model | is a good | (cid:28)t, | as expected. |     |     |
| ------------ | --------- | ----- | --------- | ---------- | ------------ | --- | --- |
| 10.2.4       | Financial |       | Data      | and        | Prediction   |     |     |
In this section we are going to (cid:28)t ARIMA models to Amazon, Inc. (AMZN) and the S&P500
US Equity Index (^GPSC, in Yahoo Finance). We will make use of the forecast library, written
| by Rob | J Hyndman[30]. |     |         |     |         |       |     |
| ------ | -------------- | --- | ------- | --- | ------- | ----- | --- |
| Let’s  | go ahead       | and | install | the | library | in R: |     |
> install.packages("forecast")
> library(forecast)
Now we can use quantmod to download the daily price series of Amazon from the start of
2013. Since we will have already taken the (cid:28)rst order di(cid:27)erences of the series, the ARIMA (cid:28)t
| carried | out shortly | will | not | require | d>0 | for the integrated | component: |
| ------- | ----------- | ---- | --- | ------- | --- | ------------------ | ---------- |
> require(quantmod)
| > getSymbols("AMZN", |                       |     | from="2013-01-01") |     |     |     |     |
| -------------------- | --------------------- | --- | ------------------ | --- | --- | --- | --- |
| > amzn               | = diff(log(Cl(AMZN))) |     |                    |     |     |     |     |
p, d
As in the previous chapter we are now going to loop through the combinations of and
q, to (cid:28)nd the optimal ARIMA(p,d,q) model. By "optimal" we mean the order combination that
| minimises       | the   | Akaike | Information        |     | Criterion | (AIC):     |         |
| --------------- | ----- | ------ | ------------------ | --- | --------- | ---------- | ------- |
| > azfinal.aic   |       | <-     | Inf                |     |           |            |         |
| > azfinal.order |       | <-     | c(0,0,0)           |     |           |            |         |
| > for           | (p in | 1:4)   | for (d             | in  | 0:1) for  | (q in 1:4) | {       |
| > azcurrent.aic |       |        | <- AIC(arima(amzn, |     |           | order=c(p, | d, q))) |
if
| >   | (azcurrent.aic |     | <                | azfinal.aic) |       | {                    |     |
| --- | -------------- | --- | ---------------- | ------------ | ----- | -------------------- | --- |
| >   | azfinal.aic    |     | <- azcurrent.aic |              |       |                      |     |
| >   | azfinal.order  |     | <-               | c(p,         | d, q) |                      |     |
| >   | azfinal.arima  |     | <-               | arima(amzn,  |       | order=azfinal.order) |     |
> }
> }
We can see that an order of p = 4, d = 0, q = 4 was selected. Notably d = 0, as we have
| already | taken | (cid:28)rst order | di(cid:27)erences |     | above: |     |     |
| ------- | ----- | ----------------- | ----------------- | --- | ------ | --- | --- |
> azfinal.order
| [1] 4 | 0 4 |     |     |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- |
If we plot the correlogram of the residuals we can see if we have evidence for a discrete white
| noise series,               | see | Figure | 10.3. |     |                    |     |     |
| --------------------------- | --- | ------ | ----- | --- | ------------------ | --- | --- |
| > acf(resid(azfinal.arima), |     |        |       |     | na.action=na.omit) |     |     |
There are two signi(cid:28)cant peaks, namely at k =15 and k =21, although we should expect to
seestatisticallysigni(cid:28)cantpeakssimplyduetosamplingvariation5%ofthetime. Let’sperform
| a Ljung-Box                      | test | and  | see if | we have | evidence | for a good                | (cid:28)t: |
| -------------------------------- | ---- | ---- | ------ | ------- | -------- | ------------------------- | ---------- |
| > Box.test(resid(azfinal.arima), |      |      |        |         |          | lag=20, type="Ljung-Box") |            |
| Box-Ljung                        |      | test |        |         |          |                           |            |
data: resid(azfinal.arima)
| X-squared | =   | 12.6337, | df  | = 20, | p-value | = 0.8925 |     |
| --------- | --- | -------- | --- | ----- | ------- | -------- | --- |
As we can see the p-value is greater than 0.05 and so we have evidence for a good (cid:28)t at the
95% level.
We can now use the command from the forecast library in order to predict 25
forecast
| days ahead | for | the returns | series |     | of Amazon, | see Figure | 10.4. |
| ---------- | --- | ----------- | ------ | --- | ---------- | ---------- | ----- |

114
Figure 10.3: Correlogram of residuals of ARIMA(4,0,4) model (cid:28)tted to AMZN daily log returns
> plot(forecast(azfinal.arima, h=25))
| Figure 10.4: | 25-day forecast | of AMZN daily | log returns |
| ------------ | --------------- | ------------- | ----------- |

115
We can see the point forecasts for the next 25 days with 95% (dark blue) and 99% (light
blue) error bands. We will be using these forecasts in our (cid:28)rst time series trading strategy when
| we come | to combine | ARIMA |     | and GARCH |     | later | in the book. |     |
| ------- | ---------- | ----- | --- | --------- | --- | ----- | ------------ | --- |
Let’scarryoutthesameprocedurefortheS&P500. Firstlyweobtainthedatafromquantmod
| and convert           | it to | a daily | log                | returns | stream: |     |     |     |
| --------------------- | ----- | ------- | ------------------ | ------- | ------- | --- | --- | --- |
| > getSymbols("^GSPC", |       |         | from="2013-01-01") |         |         |     |     |     |
> sp = diff(log(Cl(GSPC)))
| We (cid:28)t    | an ARIMA       | model  |               | by looping   | over                 | the        | values of p, d | and q: |
| --------------- | -------------- | ------ | ------------- | ------------ | -------------------- | ---------- | -------------- | ------ |
| > spfinal.aic   |                | <- Inf |               |              |                      |            |                |        |
| > spfinal.order |                | <-     | c(0,0,0)      |              |                      |            |                |        |
| for             | in             | for    |               | in           | for                  |            | in             |        |
| > (p            | 1:4)           |        | (d            | 0:1)         |                      | (q         | 1:4) {         |        |
| > spcurrent.aic |                | <-     | AIC(arima(sp, |              |                      | order=c(p, | d, q)))        |        |
| > if            | (spcurrent.aic |        | <             | spfinal.aic) |                      | {          |                |        |
| > spfinal.aic   |                | <-     | spcurrent.aic |              |                      |            |                |        |
| > spfinal.order |                |        | <- c(p,       | d,           | q)                   |            |                |        |
| > spfinal.arima |                |        | <- arima(sp,  |              | order=spfinal.order) |            |                |        |
> }
> }
The AIC tells us that the "best" model is the ARIMA(2,0,1) model. Notice once again that
| d=0, as | we have | already | taken | (cid:28)rst | order | di(cid:27)erences | of the series: |     |
| ------- | ------- | ------- | ----- | ----------- | ----- | ----------------- | -------------- | --- |
> spfinal.order
| [1] 2 0 | 1   |     |     |     |     |     |     |     |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- |
We can plot the residuals of the (cid:28)tted model to see if we have evidence of discrete white
| noise, see                  | Figure | 10.5. |     |                    |     |     |     |     |
| --------------------------- | ------ | ----- | --- | ------------------ | --- | --- | --- | --- |
| > acf(resid(spfinal.arima), |        |       |     | na.action=na.omit) |     |     |     |     |
Figure10.5: CorrelogramofresidualsofARIMA(2,0,1)model(cid:28)ttedtoS&P500dailylogreturns

116
The correlogram looks promising, so the next step is to run the Ljung-Box test and con(cid:28)rm
| that we                          | have a | good model |     | (cid:28)t: |         |                   |     |
| -------------------------------- | ------ | ---------- | --- | ---------- | ------- | ----------------- | --- |
| > Box.test(resid(spfinal.arima), |        |            |     |            | lag=20, | type="Ljung-Box") |     |
| Box-Ljung                        |        | test       |     |            |         |                   |     |
data: resid(spfinal.arima)
| X-squared | = 13.6037, |     | df  | = 20, | p-value | = 0.85 |     |
| --------- | ---------- | --- | --- | ----- | ------- | ------ | --- |
Since the p-value is greater than 0.05 we have evidence of a good model (cid:28)t.
Why is it that in the previous chapter our Ljung-Box test for the S&P500 showed that the
| ARMA(3,3) | was | a poor | (cid:28)t for | the daily | log | returns? |     |
| --------- | --- | ------ | ------------- | --------- | --- | -------- | --- |
NoticethatIdeliberatelytruncatedtheS&P500datatostartfrom2013onwardshere,which
conveniently excludes the volatile periods around 2007-2008. Hence we have excluded a large
portion of the S&P500 where we had excessive volatility clustering. This impacts the serial
correlation of the series and hence has the e(cid:27)ect of making the series seem "more stationary"
| than it | has been | in the | past. |     |     |     |     |
| ------- | -------- | ------ | ----- | --- | --- | --- | --- |
This is a very important point. When analysing time series we need to be extremely careful
of conditionally heteroscedastic series, such as stock market indexes. In quantitative (cid:28)nance,
trying to determine periods of di(cid:27)ering volatility is often known as "regime detection". It is one
| of the harder | tasks | to  | achieve! |     |     |     |     |
| ------------- | ----- | --- | -------- | --- | --- | --- | --- |
Let’s now plot a forecast for the next 25 days of the S&P500 daily log returns, see Figure
10.6.
| > plot(forecast(spfinal.arima, |     |        |       |        | h=25))   |                 |             |
| ------------------------------ | --- | ------ | ----- | ------ | -------- | --------------- | ----------- |
|                                |     | Figure | 10.6: | 25-day | forecast | of S&P500 daily | log returns |
Now that we have the ability to (cid:28)t and forecast models such as ARIMA, we’re very close to
| being able | to create | strategy |     | indicators | for | trading. |     |
| ---------- | --------- | -------- | --- | ---------- | --- | -------- | --- |

117
| 10.2.5 | Next | Steps |     |     |     |     |     |     |
| ------ | ---- | ----- | --- | --- | --- | --- | --- | --- |
In the next section we are going to take a look at the Generalised Autoregressive Conditional
Heteroscedasticity(GARCH)modelanduseittoexplainmoreoftheserialcorrelationincertain
| equities | and equity | index | series. |     |     |     |     |     |
| -------- | ---------- | ----- | ------- | --- | --- | --- | --- | --- |
Once we have discussed GARCH we will be in a position to combine it with the ARIMA
model and create signal indicators and thus a basic quantitative trading strategy.
| 10.3 | Volatility |     |     |     |     |     |     |     |
| ---- | ---------- | --- | --- | --- | --- | --- | --- | --- |
The main motivation for studying conditional heteroskedasticity in (cid:28)nance is that of volatility
of asset returns. Volatility is an incredibly important concept in (cid:28)nance because it is highly
| synonymous | with | risk.  |       |                 |     |                |     |     |
| ---------- | ---- | ------ | ----- | --------------- | --- | -------------- | --- | --- |
| Volatility | has  | a wide | range | of applications | in  | (cid:28)nance: |     |     |
(cid:136)
Options Pricing - The Black-Scholes model for options prices is dependent upon the
| volatility |     | of the | underlying | instrument |     |     |     |     |
| ---------- | --- | ------ | ---------- | ---------- | --- | --- | --- | --- |
(cid:136) Risk Management - Volatility plays a role in calculating the VaR of a portfolio, the
| Sharpe | Ratio | for | a trading | strategy | and in | determination | of  | leverage |
| ------ | ----- | --- | --------- | -------- | ------ | ------------- | --- | -------- |
(cid:136)
Tradeable Securities - Volatility can now be traded directly by the introduction of the
| CBOE | Volatility |     | Index | (VIX), and | subsequent | futures | contracts | and ETFs |
| ---- | ---------- | --- | ----- | ---------- | ---------- | ------- | --------- | -------- |
Hence, if we can e(cid:27)ectively forecast volatility then we will be able to price options more
accurately,createmoresophisticatedriskmanagementtoolsforouralgorithmictradingportfolios
| and even | come | up with | new | strategies | that trade | volatility | directly. |     |
| -------- | ---- | ------- | --- | ---------- | ---------- | ---------- | --------- | --- |
We’re now going to turn our attention to conditional heteroskedasticity and discuss what it
means.
| 10.4 | Conditional |     |     | Heteroskedasticity |     |     |     |     |
| ---- | ----------- | --- | --- | ------------------ | --- | --- | --- | --- |
Let’s (cid:28)rst discuss the concept of heteroskedasticity and then examine the "conditional" part.
If we have a collection of random variables, such as elements in a time series model, we say
that the collection is heteroskedastic if there are certain groups, or subsets, of variables within
| the larger | set that | have | a di(cid:27)erent | variance | from | the remaining | variables. |     |
| ---------- | -------- | ---- | ----------------- | -------- | ---- | ------------- | ---------- | --- |
For instance, in a non-stationary time series that exhibits seasonality or trending e(cid:27)ects, we
may (cid:28)nd that the variance of the series increases with the seasonality or the trend. This form of
| regular variability |     | is known | as  | heteroskedasticity. |     |     |     |     |
| ------------------- | --- | -------- | --- | ------------------- | --- | --- | --- | --- |
However, in (cid:28)nance there are many reasons why an increase in variance is correlated to a
| further increase |     | in variance. |     |     |     |     |     |     |
| ---------------- | --- | ------------ | --- | --- | --- | --- | --- | --- |
For instance, consider the prevalence of downside portfolio protection insurance employed
by long-only fund managers. If the equities markets were to have a particularly challenging
day (i.e. a substantial drop!) it could trigger automated risk management sell orders, which
would further depress the price of equities within these portfolios. Since the larger portfolios are
generally highly correlated anyway, this could trigger signi(cid:28)cant downward volatility.
These "sell-o(cid:27)" periods, as well as many other forms of volatility that occur in (cid:28)nance, lead
to heteroskedasticity that is serially correlated and hence conditional on periods of increased
| variance. | Thus | we say | that such | series | are conditional |     | heteroskedastic. |     |
| --------- | ---- | ------ | --------- | ------ | --------------- | --- | ---------------- | --- |
One of the challenging aspects of conditional heteroskedastic series is that if we were to plot
the correlogram of a series with volatility we might still see what appears to be a realisation
of stationary discrete white noise. That is, the volatility itself is hard to detect purely from
the correlogram. This is despite the fact that the series is most de(cid:28)nitely non-stationary as its
| variance | is not | constant | in time. |     |     |     |     |     |
| -------- | ------ | -------- | -------- | --- | --- | --- | --- | --- |
We are going to describe a mechanism for detecting conditional heteroskedastic series in this
chapter and then use the ARCH and GARCH models to account for it, ultimately leading to
more realistic forecasting performance, and thus more pro(cid:28)table trading strategies.

118
| 10.5 | Autoregressive |     | Conditional |     |     | Heteroskedastic | Models |     |
| ---- | -------------- | --- | ----------- | --- | --- | --------------- | ------ | --- |
We’ve now discussed conditional heteroskedasticity (CH) and its importance within (cid:28)nancial
series. We want a class of models that can incorporate CH in a natural way. We know that the
| ARIMA model | does not | account | for | CH, so | how can | we proceed? |     |     |
| ----------- | -------- | ------- | --- | ------ | ------- | ----------- | --- | --- |
Well, how about a model that utilises an autoregressive process for the variance itself? That
is, a model that actually accounts for the changes in the variance over time using past values of
the variance.
This is the basis of the Autoregressive Conditional Heteroskedastic (ARCH) model. We’ll
beginwiththesimplestpossiblecase,namelyanARCHmodelthatdependssolelyontheprevious
| variance value | in the series.        |     |     |     |     |     |     |     |
| -------------- | --------------------- | --- | --- | --- | --- | --- | --- | --- |
| 10.5.1         | ARCH De(cid:28)nition |     |     |     |     |     |     |     |
De(cid:28)nition 10.5.1. Autoregressive Conditional Heteroskedastic Model of Order Unity.
| A time | series {(cid:15) t } is | given | at each | instance | by:  |     |     |        |
| ------ | ----------------------- | ----- | ------- | -------- | ---- | --- | --- | ------ |
|        |                         |       |         | (cid:15) | =σ w |     |     | (10.5) |
|        |                         |       |         | t        | t t  |     |     |        |
Where {w } is discrete white noise, with zero mean and unit variance, and σ2 is given by:
|       | t           |            |     |        |        |           | t   |        |
| ----- | ----------- | ---------- | --- | ------ | ------ | --------- | --- | ------ |
|       |             |            |     | σ2     |        | (cid:15)2 |     |        |
|       |             |            |     | =α     | 0 +α 1 |           |     | (10.6) |
|       |             |            |     | t      |        | t−1       |     |        |
| Where | α and α are | parameters |     | of the | model. |           |     |        |
0 1
Wesaythat{(cid:15) }isanautoregressiveconditionalheteroskedasticmodeloforderunity,denoted
t
σ2,
| by ARCH(1). | Substituting | for | we  | receive: |     |     |     |     |
| ----------- | ------------ | --- | --- | -------- | --- | --- | --- | --- |
t
(cid:113)
|        |          |      | (cid:15) | =w  | α +α        | (cid:15)2 |     | (10.7) |
| ------ | -------- | ---- | -------- | --- | ----------- | --------- | --- | ------ |
|        |          |      |          | t t | 0           | 1 t−1     |     |        |
| 10.5.2 | Why Does | This | Model    |     | Volatility? |           |     |        |
I personally (cid:28)nd the above "formal" de(cid:28)nition lacking in motivation as to how it introduces
volatility. However, you can see how it is introduced by squaring both sides of the previous
equation:
|     |     |     | Var((cid:15) | ) = | E[(cid:15)2]−(E[(cid:15) | ])2 |     | (10.8) |
| --- | --- | --- | ------------ | --- | ------------------------ | --- | --- | ------ |
|     |     |     |              | t   | t                        | t   |     |        |
|     |     |     |              | =   | E[(cid:15)2]             |     |     | (10.9) |
t
|     |     |     |     | =   | E[w2]E[α | +α (cid:15)2 ] |     | (10.10) |
| --- | --- | --- | --- | --- | -------- | -------------- | --- | ------- |
|     |     |     |     |     | t        | 0 1 t−1        |     |         |
|     |     |     |     | =   | E[α +α   | (cid:15)2 ]    |     | (10.11) |
|     |     |     |     |     | 0        | 1 t−1          |     |         |
|     |     |     |     | =   | α +α     | Var((cid:15) ) |     | (10.12) |
|     |     |     |     |     | 0        | 1 t−1          |     |         |
Where I have used the de(cid:28)nitions of the variance Var(x)=E[x2]−(E[x])2 and the linearity
of the expectation operator E, along with the fact that {w t } has zero mean and unit variance.
Thus we can see that the variance of the series is simply a linear combination of the variance
of the prior element of the series. Simply put, the variance of an ARCH(1) process follows an
AR(1) process.
ItisinterestingtocomparetheARCH(1)modelwithanAR(1)model. Recallthatthelatter
is given by:
|     |     |     | x   | =α +α | x     | +w  |     | (10.13) |
| --- | --- | --- | --- | ----- | ----- | --- | --- | ------- |
|     |     |     | t   | 0     | 1 t−1 | t   |     |         |
Youcanseethatthemodelsaresimilarinform(withtheexceptionofthewhitenoiseterm).

119
| 10.5.3 | When | Is  | It Appropriate |     | To  | Apply ARCH(1)? |     |     |
| ------ | ---- | --- | -------------- | --- | --- | -------------- | --- | --- |
So what approach can we take in order to determine whether an ARCH(1) model is appropriate
| to apply | to a | series? |     |     |     |     |     |     |
| -------- | ---- | ------- | --- | --- | --- | --- | --- | --- |
Consider that when we were attempting to (cid:28)t an AR(1) model we were concerned with the
decay of the (cid:28)rst lag on a correlogram of the series. However, if we apply the same logic to the
square of the residuals, and see whether we can apply an AR(1) to these squared residuals then
| we have | an indication | that | an ARCH(1) |     | process | may be appropriate. |     |     |
| ------- | ------------- | ---- | ---------- | --- | ------- | ------------------- | --- | --- |
NotethatARCH(1)shouldonlyeverbeappliedtoaseriesthathasalreadyhadanappropriate
model(cid:28)ttedsu(cid:30)cienttoleavetheresidualslookinglikediscretewhitenoise. Sincewecanonlytell
whether ARCH is appropriate or not by squaring the residuals and examining the correlogram,
| we also | need to | ensure | that the mean | of  | the residuals | is zero. |     |     |
| ------- | ------- | ------ | ------------- | --- | ------------- | -------- | --- | --- |
Crucially,ARCHshouldonlyeverbeappliedtoseriesthatdonothaveanytrendsorseasonal
e(cid:27)ects, i.e. that has no (evident) serial correlation. ARIMA is often applied to such a series (or
| even Seasonal |         | ARIMA), | at which | point | ARCH may | be a good (cid:28)t. |     |     |
| ------------- | ------- | ------- | -------- | ----- | -------- | -------------------- | --- | --- |
| 10.5.4        | ARCH(p) |         | Models   |       |          |                      |     |     |
It is straightforward to extend ARCH to higher order lags. An ARCH(p) process is given by:
(cid:118)
(cid:117)
p
|     |     |     |     |                           | (cid:117) | (cid:88) (cid:15)2 |     |         |
| --- | --- | --- | --- | ------------------------- | --------- | ------------------ | --- | ------- |
|     |     |     |     | (cid:15) t =w t(cid:116)α | 0 +       | α p                |     | (10.14) |
t−i
i=1
You can think of ARCH(p) as applying an AR(p) model to the variance of the series.
An obvious question to ask at this stage is if we are going to apply an AR(p) process to
the variance, why not a Moving Average MA(q) model as well? Or a mixed model such as
ARMA(p,q)?
This is actually the motivation for the Generalised ARCH model, known as GARCH, which
| we will | now de(cid:28)ne | and | discuss.       |     |     |             |               |     |
| ------- | ---------------- | --- | -------------- | --- | --- | ----------- | ------------- | --- |
| 10.6    | Generalised      |     | Autoregressive |     |     | Conditional | Heteroskedas- |     |
tic Models
| 10.6.1 | GARCH |     | De(cid:28)nition |     |     |     |     |     |
| ------ | ----- | --- | ---------------- | --- | --- | --- | --- | --- |
De(cid:28)nition 10.6.1. Generalised Autoregressive Conditional Heteroskedastic Model of Order p,
q.
| A time | series | {(cid:15) } is | given at | each instance | by: |     |     |     |
| ------ | ------ | -------------- | -------- | ------------- | --- | --- | --- | --- |
t
|     |     |     |     |     | (cid:15) =σ w |     |     | (10.15) |
| --- | --- | --- | --- | --- | ------------- | --- | --- | ------- |
|     |     |     |     |     | t t           | t   |     |         |
Where {w } is discrete white noise, with zero mean and unit variance, and σ2 is given by:
|       | t   |           |            |          |           |             | t   |         |
| ----- | --- | --------- | ---------- | -------- | --------- | ----------- | --- | ------- |
|       |     |           |            |          | q         | p           |     |         |
|       |     |           | σ2         | (cid:88) | (cid:15)2 | (cid:88) σ2 |     |         |
|       |     |           | =α         | +        | α         | + β         |     | (10.16) |
|       |     |           | t          | 0        | i t−i     | j t−j       |     |         |
|       |     |           |            | i=1      |           | j=1         |     |         |
| Where | α   | and β are | parameters | of the   | model.    |             |     |         |
i j
{(cid:15) }
We say that t is a generalised autoregressive conditional heteroskedastic model of order
| p,q, denoted | by  | GARCH(p,q). |     |     |     |     |     |     |
| ------------ | --- | ----------- | --- | --- | --- | --- | --- | --- |
Hence this de(cid:28)nition is similar to that of ARCH(p), with the exception that we are adding
moving average terms, that is the value of σ2 at t, σ2, is dependent upon previous σ2 values.
|     |     |     |     |     |     | t   |     | t−j |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Thus GARCH is the "ARMA equivalent" of ARCH, which only has an autoregressive com-
ponent.

120
| 10.6.2 | Simulations, | Correlograms | and Model | Fittings |     |     |
| ------ | ------------ | ------------ | --------- | -------- | --- | --- |
Asalwayswe’regoingtobeginwiththesimplestpossiblecaseofthemodel,namelyGARCH(1,1).
This means we are going to consider a single autoregressive lag and a single "moving average"
| lag. The | model is given | by the following: |               |     |     |         |
| -------- | -------------- | ----------------- | ------------- | --- | --- | ------- |
|          |                | (cid:15) t =      | σ t w t       |     |     | (10.17) |
|          |                | σ2                | (cid:15)2     | σ2  |     |         |
|          |                | =                 | α 0 +α 1 +β 1 |     |     | (10.18) |
|          |                | t                 | t−1           | t−1 |     |         |
Note that it is necessary for α +β <1 otherwise the series will become unstable.
|     |     | 1 1 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
We can see that the model has three parameters, namely α , α and β . Let’s set α =0.2,
|          |               |     |     | 0 1 | 1   | 0   |
| -------- | ------------- | --- | --- | --- | --- | --- |
| α 1 =0.5 | and β 1 =0.3. |     |     |     |     |     |
To create the GARCH(1,1) model in R we need to perform a similar procedure as for our
original random walk simulations. That is, we need to create a vector w to store our random
whitenoisevalues, thenaseparatevector epstostoreourtimeseriesvaluesand(cid:28)nallyavector
| sigsq to | store the ARMA | variances. |     |     |     |     |
| -------- | -------------- | ---------- | --- | --- | --- | --- |
We can use the R rep command to create a vector of zeros that we will populate with our
| GARCH | values: |     |     |     |     |     |
| ----- | ------- | --- | --- | --- | --- | --- |
> set.seed(2)
| > a0 <- | 0.2 |     |     |     |     |     |
| ------- | --- | --- | --- | --- | --- | --- |
| > a1 <- | 0.5 |     |     |     |     |     |
| > b1 <- | 0.3 |     |     |     |     |     |
> w <- rnorm(10000)
| > eps <-   | rep(0, 10000)          |                     |                   |     |     |     |
| ---------- | ---------------------- | ------------------- | ----------------- | --- | --- | --- |
| > sigsq    | <- rep(0, 10000)       |                     |                   |     |     |     |
| > for (i   | in 2:10000)            | {                   |                   |     |     |     |
| > sigsq[i] | <- a0                  | + a1 * (eps[i-1]^2) | + b1 * sigsq[i-1] |     |     |     |
| > eps[i]   | <- w[i]*sqrt(sigsq[i]) |                     |                   |     |     |     |
> }
At this stage we have generated our GARCH model using the aforementioned parameters
over 10,000 samples. We are now in a position to plot the correlogram, which is given in Figure
10.7.
> acf(eps)
Notice that the series looks like a realisation of a discrete white noise process.
However, if we plot correlogram of the square of the series, as given in Figure 10.8,
> acf(eps^2)
we see substantial evidence of a conditionally heteroskedastic process via the decay of suc-
cessive lags.
As in the previous chapter we now want to try and (cid:28)t a GARCH model to this simulated
series to see if we can recover the parameters. Thankfully, a helpful library called tseries
| provides | the garch command | to carry | this procedure out: |     |     |     |
| -------- | ----------------- | -------- | ------------------- | --- | --- | --- |
> require(tseries)
We can then use the confint command to produce con(cid:28)dence intervals at the 97.5% level
for the parameters:
| > eps.garch | <- garch(eps, | trace=FALSE) |     |     |     |     |
| ----------- | ------------- | ------------ | --- | --- | --- | --- |
> confint(eps.garch)
|              | 2.5 % 97.5 | %   |     |     |     |     |
| ------------ | ---------- | --- | --- | --- | --- | --- |
| a0 0.1786255 | 0.2172683  |     |     |     |     |     |
| a1 0.4271900 | 0.5044903  |     |     |     |     |     |
| b1 0.2861566 | 0.3602687  |     |     |     |     |     |
We can see that the true parameters all fall within the respective con(cid:28)dence intervals.

121
Figure 10.7: Correlogram of a simulated GARCH(1,1) model with α = 0.2, α = 0.5 and
0 1
β =0.3
1
Figure 10.8: Correlogram of a simulated GARCH(1,1) models squared values with α = 0.2,
0
α =0.5 and β =0.3
1 1

122
| 10.6.3 | Financial |     | Data |     |     |     |
| ------ | --------- | --- | ---- | --- | --- | --- |
Now that we know how to simulate and (cid:28)t a GARCH model, we want to apply the procedure to
some(cid:28)nancialseries. Inparticular,let’stry(cid:28)ttingARIMAandGARCHtotheFTSE100index
of the largest UK companies by market capitalisation. Yahoo Finance uses the symbol ^FTSE
| for the index. | We  | can use | quantmod | to  | obtain | the data: |
| -------------- | --- | ------- | -------- | --- | ------ | --------- |
> require(quantmod)
> getSymbols("^FTSE")
We can then calculate the di(cid:27)erences of the log returns of the closing price:
| > ftrt =   | diff(log(Cl(FTSE))) |         |             |        |       |     |
| ---------- | ------------------- | ------- | ----------- | ------ | ----- | --- |
| Let’s plot | the                 | values, | as given in | Figure | 10.9. |     |
> plot(ftrt)
It is very clear that there are periods of increased volatility, particularly around 2008-2009,
| late 2011 | and more | recently | in mid | 2015: |     |     |
| --------- | -------- | -------- | ------ | ----- | --- | --- |
Figure 10.9: Di(cid:27)erenced log returns of the daily closing price of the FTSE 100 UK stock index
We also need to remove the NA value generated by the di(cid:27)erencing procedure:
| > ft <- | as.numeric(ftrt) |     |     |     |     |     |
| ------- | ---------------- | --- | --- | --- | --- | --- |
ft[!is.na(ft)]
> ft <-
Thenexttaskisto(cid:28)tasuitableARIMA(p,d,q)model. Wesawhowtodothatintheprevious
chapter, so I won’t repeat the procedure here, I will simply provide the code:
| > ftfinal.aic       | <-      | Inf         |                |     |            |           |
| ------------------- | ------- | ----------- | -------------- | --- | ---------- | --------- |
| > ftfinal.order     |         | <- c(0,0,0) |                |     |            |           |
| > for (p            | in 1:4) | for         | (d in 0:1)     | for | (q         | in 1:4) { |
| > ftcurrent.aic     |         | <-          | AIC(arima(ft,  |     | order=c(p, | d, q)))   |
| > if (ftcurrent.aic |         |             | < ftfinal.aic) |     | {          |           |
| > ftfinal.aic       |         | <-          | ftcurrent.aic  |     |            |           |

123
| >   | ftfinal.order |     | <- c(p,      | d, q)                |     |
| --- | ------------- | --- | ------------ | -------------------- | --- |
| >   | ftfinal.arima |     | <- arima(ft, | order=ftfinal.order) |     |
> }
> }
Since we’ve already di(cid:27)erenced the FTSE returns once, we should expect our integrated
| component | d to | equal zero, | which | it does: |     |
| --------- | ---- | ----------- | ----- | -------- | --- |
> ftfinal.order
| [1] 4 | 0 4 |     |     |     |     |
| ----- | --- | --- | --- | --- | --- |
Thus we receive an ARIMA(4,0,4) model, that is four autoregressive parameters and four
| moving | average | parameters. |     |     |     |
| ------ | ------- | ----------- | --- | --- | --- |
We are now in a position to decide whether the residuals of this model (cid:28)t possess evidence
of conditional heteroskedastic behaviour. To test this we need to plot the correlogram of the
| residuals, | as given | in Figure | 10.10. |     |     |
| ---------- | -------- | --------- | ------ | --- | --- |
> acf(resid(ftfinal.arima))
Figure 10.10: Residuals of an ARIMA(4,0,4) (cid:28)t to the FTSE100 di(cid:27) log returns
Thislookslikearealisationofadiscretewhitenoiseprocessindicatingthatwehaveachieved
| a good | (cid:28)t with | the ARIMA(4,0,4) |     | model. |     |
| ------ | -------------- | ---------------- | --- | ------ | --- |
To test for conditional heteroskedastic behaviour we need to square the residuals and plot
| the corresponding |     | correlogram, |     | as given in Figure | 10.11. |
| ----------------- | --- | ------------ | --- | ------------------ | ------ |
> acf(resid(ftfinal.arima)^2)
We can see clear evidence of serial correlation in the squared residuals, leading us to the
conclusion that conditional heteroskedastic behaviour is present in the di(cid:27) log return series of
the FTSE100.
We are now in a position to (cid:28)t a GARCH model using the tseries library.
The(cid:28)rstcommandactually(cid:28)tsanappropriateGARCHmodel,withthetrace=Fparameter
| telling R | to suppress | excessive |     | output. |     |
| --------- | ----------- | --------- | --- | ------- | --- |
The second command removes the (cid:28)rst element of the residuals, since it is NA:

124
Figure 10.11: Squared residuals of an ARIMA(4,0,4) (cid:28)t to the FTSE100 di(cid:27) log returns
| > ft.garch | <- garch(ft,        | trace=F) |     |
| ---------- | ------------------- | -------- | --- |
| > ft.res   | <- ft.garch$res[-1] |          |     |
Finally, to test for a good (cid:28)t we can plot the correlogram of the GARCH residuals and the
| square GARCH | residuals, | as given | in Figure 10.12. |
| ------------ | ---------- | -------- | ---------------- |
> acf(ft.res)
The correlogram looks like a realisation of a discrete white noise process, indicating a good
| (cid:28)t. Let’s | now try the squared | residuals, | given in Figure 10.13. |
| ---------------- | ------------------- | ---------- | ---------------------- |
> acf(ft.res^2)
Once again, we have what looks like a realisation of a discrete white noise process, indi-
cating that we have "explained" the serial correlation present in the squared residuals with an
| appropriate | mixture of | ARIMA(p,d,q) | and GARCH(p,q). |
| ----------- | ---------- | ------------ | --------------- |
| 10.7        | Next Steps |              |                 |
WearenowatthepointinourtimeserieseducationwherewehavestudiedARIMAandGARCH,
allowing us to (cid:28)t a combination of these models to a stock market index, and to determine if we
| have achieved | a good (cid:28)t | or not. |     |
| ------------- | ---------------- | ------- | --- |
The next step is to actually produce forecasts of future daily returns values from this com-
bination and use it to create a basic trading strategy. We will discuss this in the Quantitative
| Trading | Strategies part | of the book. |     |
| ------- | --------------- | ------------ | --- |

125
Figure 10.12: Residuals of a GARCH(p,q) (cid:28)t to the ARIMA(4,0,4) (cid:28)t of the FTSE100 di(cid:27) log
returns
Figure 10.13: Squared residuals of a GARCH(p,q) (cid:28)t to the ARIMA(4,0,4) (cid:28)t of the FTSE100
di(cid:27) log returns

126

| Chapter | 11    |     |        |     |     |            |
| ------- | ----- | --- | ------ | --- | --- | ---------- |
| State   | Space |     | Models |     | and | the Kalman |
Filter
Thus far in our analysis of time series we have considered linear time series models including
ARMA,ARIMAaswellastheGARCHmodelforconditionalheteroskedasticity. Inthischapter
we are going to consider a more general class of models known as state space models, the
primarybene(cid:28)tofwhichisthatunliketheARIMAfamily,theirparameters can adapt over time.
State space models are very general and it is possible to put the models we have considered
to date into a state space formulation. However, in order to keep the analysis straightforward,
| it is often | better to use | the simpler | representation. |     |     |     |
| ----------- | ------------- | ----------- | --------------- | --- | --- | --- |
The general premise of a state space model is that we have a set of states that evolve in
time (such as the hedge ratio between two cointegrated pairs of equities), but our observations
of these states contain statistical noise (such as market microstructure noise), and hence we are
| unable to | ever directly observe | the | "true" | states. |     |     |
| --------- | --------------------- | --- | ------ | ------- | --- | --- |
The goal of the state space model is to infer information about the states, given the obser-
vations, as new information arrives. A famous algorithm for carrying out this procedure is the
| Kalman | Filter, which | we will | also discuss | in this | article. |     |
| ------ | ------------- | ------- | ------------ | ------- | -------- | --- |
The Kalman Filter is ubiquitous in engineering control problems, including guidance & navi-
gation,spacecrafttrajectoryanalysisandmanufacturing,butitisalsowidelyusedinquantitative
(cid:28)nance.
In engineering, for instance, a Kalman Filter will be used to estimate values of the state,
which are then used to control the system under study. This introduces a feedback loop, often
in real-time.
Perhaps the most common usage of a Kalman Filter in quantitative trading is to update
hedging ratios between assets in a statistical arbitrage pairs trade, but the algorithm is much
| more general | than this | and we will | look | at other | use cases. |     |
| ------------ | --------- | ----------- | ---- | -------- | ---------- | --- |
Generally, there are three types of inference that we are interested in when considering state
space models:
(cid:136)
| Prediction | - Forecasting |     | subsequent | values | of the state |     |
| ---------- | ------------- | --- | ---------- | ------ | ------------ | --- |
(cid:136)
Filtering - Estimating the current values of the state from past and current observations
(cid:136)
Smoothing - Estimating the past values of the state given the observations
Filtering and smoothing are similar, but not the same. Perhaps the best way to think of the
di(cid:27)erence is that with smoothing we are really wanting to understand what has happened to
states in the past given our current knowledge, whereas with (cid:28)ltering we really want to know
| what is happening | with | the state | right | now. |     |     |
| ----------------- | ---- | --------- | ----- | ---- | --- | --- |
In this chapter we are going to discuss the theory of the state space model and how we can
use the Kalman Filter to carry out the various types of inference described above. We will then
apply the Kalman Filter to trading situations, such as cointegrated pairs, as well as asset price
| prediction, | later in the | book. |     |     |     |     |
| ----------- | ------------ | ----- | --- | --- | --- | --- |
127

128
WewillbemakinguseofaBayesianapproachtotheproblem,asthisisanaturalstatistical
framework for allowing us to readily update our beliefs in light of new information, which is
| precisely | the desired | behaviour |     | of the | Kalman | Filter. |     |     |     |     |
| --------- | ----------- | --------- | --- | ------ | ------ | ------- | --- | --- | --- | --- |
I want to warn you that state-space models and Kalman Filters su(cid:27)er from an abundance of
mathematical notation, even if the conceptual ideas behind them are relatively straightforward.
I will try and explain all of this notation in depth, as it can be confusing for those new to
engineering control problems or state-space models in general. Fortunately we will be letting R
do the heavy lifting of solving the model for us, so the verbose notation will not be a problem in
practice.
| 11.1 | Linear | State-Space |     |     | Model |     |     |     |     |     |
| ---- | ------ | ----------- | --- | --- | ----- | --- | --- | --- | --- | --- |
Let’s begin by discussing all of the elements of the linear state-space model.
t.
Since the states of the system are time-dependent, we need to subscript them with We
| will use | θ to represent |     | a column | vector | of  | the states. |     |     |     |     |
| -------- | -------------- | --- | -------- | ------ | --- | ----------- | --- | --- | --- | --- |
t
In a linear state-space model we say that these states are a linear combination of the prior
state at time t−1 as well as system noise (random variation). In order to simplify the analysis
we are going to suggest that this noise is drawn from a multivariate normal distribution, but of
| course, | other distributions |     | can | be used. |     |     |     |     |     |     |
| ------- | ------------------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
The linear dependence of θ on the previous state θ is given by the matrix G , which can
|     |     |     |     | t   |     |     | t−1 |     | t   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
also be time-varying (hence the subscript t). The multivariate time-dependent noise is given by
w t . The relationship is summarised below in what is often called the state equation:
|     |     |     |     |     | θ t =G | t θ t−1 | +w t |     |     | (11.1) |
| --- | --- | --- | --- | --- | ------ | ------- | ---- | --- | --- | ------ |
However,thisisonlyhalfofthestory. Wealsoneedtodiscusstheobservations,thatis,what
| we actually | see, | since the | states | are | hidden | to us | by system | noise. |     |     |
| ----------- | ---- | --------- | ------ | --- | ------ | ----- | --------- | ------ | --- | --- |
Wecandenotethe(time-dependent)observationsbyy . Theobservationsarealinearcombi-
t
nation of the current state and some additional random variation known as measurement noise,
| also drawn | from | a multivariate |     | normal | distribution. |     |     |     |     |     |
| ---------- | ---- | -------------- | --- | ------ | ------------- | --- | --- | --- | --- | --- |
If we denote the linear dependence matrix of θ on y by F (also time-dependent), and the
|             |       |     |             |     |             |     | t         | t t |     |     |
| ----------- | ----- | --- | ----------- | --- | ----------- | --- | --------- | --- | --- | --- |
| measurement | noise | by  | v t we have | the | observation |     | equation: |     |     |     |
=FTθ
|     |     |     |     |     | y t | t   | +v t |     |     | (11.2) |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | ------ |
t
| Where | FT is | the transpose |     | of F. |     |     |     |     |     |     |
| ----- | ----- | ------------- | --- | ----- | --- | --- | --- | --- | --- | --- |
Inordertofullyspecifythemodelweneedtoprovidethe(cid:28)rststateθ 0 ,aswellasthevariance-
covariance matrices for the system noise and measurement noise. These terms are distributed
as:
|     |     |     |     |     | θ   | ∼ N(m   | ,C  | )   |     | (11.3) |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | ------ |
|     |     |     |     |     | 0   |         | 0   | 0   |     |        |
|     |     |     |     |     | v   | ∼ N(0,V | )   |     |     | (11.4) |
|     |     |     |     |     | t   |         | t   |     |     |        |
|     |     |     |     |     | w   | ∼ N(0,W | )   |     |     | (11.5) |
|     |     |     |     |     | t   |         | t   |     |     |        |
Clearly that is a lot of notation to specify the model. For completeness, I’ll summarise all of
| the terms | here to | help | you get | to grips | with | the | model: |     |     |     |
| --------- | ------- | ---- | ------- | -------- | ---- | --- | ------ | --- | --- | --- |
(cid:136)
| θ   | - The state | of  | the model | at  | time t |     |     |     |     |     |
| --- | ----------- | --- | --------- | --- | ------ | --- | --- | --- | --- | --- |
t
| (cid:136) y | - The observation |     | of  | the model | at  | time | t   |     |     |     |
| ----------- | ----------------- | --- | --- | --------- | --- | ---- | --- | --- | --- | --- |
t
(cid:136) G - The state-transition matrix between current and prior states at time t and t−1
t
respectively

129
(cid:136) F
t - The observation matrix between the current observation and current state at time
t
(cid:136)
|     | w t - The | system | noise | drawn | from | a multivariate | normal | distribution |     |
| --- | --------- | ------ | ----- | ----- | ---- | -------------- | ------ | ------------ | --- |
(cid:136)
v t - The measurement noise drawn from a multivariate normal distribution
(cid:136) m - The mean value of the multivariate normal distribution of the initial state, θ
|     | 0   |     |     |     |     |     |     |     | 0   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:136) C - The variance-covariance matrix of the multivariate normal distribution of the initial
0
|     | state, | θ 0 |     |     |     |     |     |     |     |
| --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:136)
W t - The variance-covariance matrix for the multivariate normal distribution from which
|     | the system | noise | is drawn |     |     |     |     |     |     |
| --- | ---------- | ----- | -------- | --- | --- | --- | --- | --- | --- |
(cid:136)
V - The variance-covariance matrix for the multivariate normal distribution from from
t
|     | which | the measurement |     | noise | is drawn |     |     |     |     |
| --- | ----- | --------------- | --- | ----- | -------- | --- | --- | --- | --- |
Nowthatwe’vespeci(cid:28)edthelinearstate-spacemodel,weneedanalgorithmtoactuallysolve
it. This is where the Kalman Filter comes in. We can use Bayes’ Rule and conjugate priors, as
| discussed | in  | the previous | part | of     | the book, | to help us | derive | the algorithm. |     |
| --------- | --- | ------------ | ---- | ------ | --------- | ---------- | ------ | -------------- | --- |
| 11.2      | The | Kalman       |      | Filter |           |            |        |                |     |
This section follows very closely the notation and analysis carried out in Pole et al[40]. I decided
it wasn’t particularly helpful to invent my own notation for the Kalman Filter, as I want you to
| be able | to relate | it to    | other | research | papers | or texts. |     |     |     |
| ------- | --------- | -------- | ----- | -------- | ------ | --------- | --- | --- | --- |
| 11.2.1  | A         | Bayesian |       | Approach |        |           |     |     |     |
If we recall from the prior chapters on Bayesian inference, Bayes’ Rule is given by:
P(θ|D)=P(D|θ)P(θ)/P(D)
(11.6)
|     | θ   |     |     |     | D   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Where refers to our parameters and refers to our data or observations.
Wewanttoapplytheruletotheideaofupdatingtheprobabilityofseeingastategivenallof
the previous data we have and our current observation. Once again, we need to introduce more
notation!
If we are at time t, then we can represent all of the data known about the system by the
|     | D   |     |     |     |     |     |     | y   | D = |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
quantity t . However, our current observations are given by t . Thus we can say that t
(D ,y ). That is, our current knowledge is a mixture of our previous knowledge plus our most
t−1 t
recent observation.
| Applying |     | Bayes’ | Rule to | this   | situation | gives the following: |     |     |        |
| -------- | --- | ------ | ------- | ------ | --------- | -------------------- | --- | --- | ------ |
|          |     |        |         |        |           | P(y |θ )P(θ          | |D  | )   |        |
|          |     |        |         |        |           | t t                  | t   | t−1 |        |
|          |     |        |         | P(θ |D | ,y )=     |                      |     |     | (11.7) |
|          |     |        |         | t      | t−1 t     | P(y                  | )   |     |        |
t
What does this mean? It says that the posterior or updated probability of obtaining a state
θ , given our current observation y and previous data D , is equal to the likelihood of seeing
| t   |     |     |     |     | t   |     | t−1 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
an observation y t , given the current state θ t multiplied by the prior or previous belief of the
current state, given only the previous data D , normalised by the probability of seeing the
t−1
y
| observation |     | t regardless. |     |     |     |     |     |     |     |
| ----------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
While the notation may be somewhat verbose, it is a very natural statement. It says that
we can update our view on the state, θ , in a rational manner given the fact that we have new
t
| information |     | in the form | of  | the current | observation, | y   | t . |     |     |
| ----------- | --- | ----------- | --- | ----------- | ------------ | --- | --- | --- | --- |
OneoftheextremelyusefulaspectsofBayesianinferenceisthatifourpriorandlikelihoodare
bothnormallydistributed, wecanusetheconceptofconjugatepriorstostatethatourposterior
| (i.e. | updated | view of | θ ) will | also | be normally | distributed. |     |     |     |
| ----- | ------- | ------- | -------- | ---- | ----------- | ------------ | --- | --- | --- |
t

130
We utilised the same concept, albeit with di(cid:27)erent distributional forms, in our previous
| discussion | on   | the inference | of      | binomial | proportions. |         |     |     |     |
| ---------- | ---- | ------------- | ------- | -------- | ------------ | ------- | --- | --- | --- |
| So how     | does | this          | help us | produce  | a Kalman     | Filter? |     |     |     |
Well, let’s specify the terms that we’ll be using, from Bayes’ Rule above. Firstly, we specify
| the distributional |     | form | of the | prior: |       |      |      |     |        |
| ------------------ | --- | ---- | ------ | ------ | ----- | ---- | ---- | --- | ------ |
|                    |     |      |        |        | θ |D  | ∼N(a | ,R ) |     | (11.8) |
|                    |     |      |        |        | t t−1 |      | t t  |     |        |
That is, the prior view of θ at time t, given our knowledge at time t−1 is distributed as
a multivariate normal distribution, with mean a and variance-covariance R . The latter two
t t
| parameters | will           | be de(cid:28)ned | below.          |     |             |     |      |     |        |
| ---------- | -------------- | ---------------- | --------------- | --- | ----------- | --- | ---- | --- | ------ |
| Now        | let’s consider |                  | the likelihood: |     |             |     |      |     |        |
|            |                |                  |                 |     | y |θ ∼N(FTθ |     | ,V ) |     | (11.9) |
|            |                |                  |                 |     | t t         | t   | t t  |     |        |
That is, the likelihood function of the current observation y at time t is distributed as a
FTθ
multivariate normal distribution, with mean t and variance-covariance V t . We’ve already
t
| outlined | these | terms    | in our list | above. |     |     |     |     |     |
| -------- | ----- | -------- | ----------- | ------ | --- | --- | --- | --- | --- |
| Finally  | we    | have the | posterior   | of     | θ : |     |     |     |     |
t
|     |     |     |     |     | θ t |D t ∼N(m |     | t ,C t ) |     | (11.10) |
| --- | --- | --- | --- | --- | ------------- | --- | -------- | --- | ------- |
|     |     |     |     |     |               |     | θ        | t,  |         |
That is, our posterior view of the current state at time given our current knowledge at
timetisdistributedasamultivariatenormaldistributionwithmeanm andvariance-covariance
t
C .
t
The Kalman Filter is what links all of these terms together for t=1,...,n. We won’t derive
where these values actually come from, but we will simply state them. Thankfully we can use
| library | implementations |     | in R | to carry | out   | the "heavy | lifting" | for us: |         |
| ------- | --------------- | --- | ---- | -------- | ----- | ---------- | -------- | ------- | ------- |
|         |                 |     |      |          | a t = | G t m t−1  |          |         | (11.11) |
GT
|     |     |     |     |     | R t = | G t C t−1 | +W  | t   | (11.12) |
| --- | --- | --- | --- | --- | ----- | --------- | --- | --- | ------- |
t
|     |     |     |     |     | e t = | y t −f | t     |     | (11.13) |
| --- | --- | --- | --- | --- | ----- | ------ | ----- | --- | ------- |
|     |     |     |     |     | m t = | a t +A | t e t |     | (11.14) |
FTa
|     |     |     |     |     | f t = | t t |     |     | (11.15) |
| --- | --- | --- | --- | --- | ----- | --- | --- | --- | ------- |
FTR
|     |     |     |     |     | Q t = | t t     | F t +V | t   | (11.16) |
| --- | --- | --- | --- | --- | ----- | ------- | ------ | --- | ------- |
|     |     |     |     |     | A =   | R F Q−1 |        |     |         |
|     |     |     |     |     | t     | t t     | t      |     | (11.17) |
|     |     |     |     |     | C =   | R −A    | Q AT   |     |         |
|     |     |     |     |     | t     | t       | t t    | t   | (11.18) |
Clearly that is a lot of notation! As I said above, we need not worry about the excessive
verboseness of the Kalman Filter, as we can simply use libraries in R to calculate the algorithm
for us.
|     |     |     |     |     | f   |     |     |     | t,  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
So how does it all (cid:28)t together? Well, t is the predicated value of the observation at time
where we make this prediction at time t−1. Since e =y −f , we can see easily that e is the
|                  |     |      |              |      |                  |         | t   | t t       | t   |
| ---------------- | --- | ---- | ------------ | ---- | ---------------- | ------- | --- | --------- | --- |
| error associated |     | with | the forecast | (the | di(cid:27)erence | between |     | f and y). |     |
Importantly, theposteriormeanisaweighting of the prior mean and the forecast error, since
m =a +A e =G m +A e , where G and A are our weighting matrices.
| t t | t   | t t | t−1 | t t |     | t   | t   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Now that we have an algorithmic procedure for updating our views on the observations and
| states, we | can        | use it | to make | predictions, | as  | well as | smooth | the data. |     |
| ---------- | ---------- | ------ | ------- | ------------ | --- | ------- | ------ | --------- | --- |
| 11.2.2     | Prediction |        |         |              |     |         |        |           |     |
The Bayesian approach to the Kalman Filter leads naturally to a mechanism for prediction.
Since we have our posterior estimate for the state θ , we can predict the next day’s values by
t
| considering | the | mean | value of | the observation. |     |     |     |     |     |
| ----------- | --- | ---- | -------- | ---------------- | --- | --- | --- | --- | --- |

131
Let’s take the expected value of the observation tomorrow, given our knowledge of the data
today:
E[FT
|     |     |     |     | E[y t+1 | |D t ] | =   | θ t +v | t+1 |D t ] | (11.19) |
| --- | --- | --- | --- | ------- | ------ | --- | ------ | ---------- | ------- |
t+1
FT
|     |     |     |     |     |     | =    | E[θ | |D ] | (11.20) |
| --- | --- | --- | --- | --- | --- | ---- | --- | ---- | ------- |
|     |     |     |     |     |     | t+1  | t+1 | t    |         |
|     |     |     |     |     |     | = FT | a   |      | (11.21) |
|     |     |     |     |     |     | t+1  | t+1 |      |         |
|     |     |     |     |     |     | = f  |     |      | (11.22) |
t+1
| Where | does | this come | from? | Let’s | try | and follow | through | the analysis: |     |
| ----- | ---- | --------- | ----- | ----- | --- | ---------- | ------- | ------------- | --- |
Since the likelihood function for today’s observation y , given today’s state θ , is normally
|     |     |     |     |     |     |     |     | t t |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
distributedwithmeanFTθ andvariance-covarianceV (seeabove),wehavethattheexpectation
|     |     |     | t t |     |     |     | t   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
of tomorrow’s observation y t+1 , given our data today, D t , is precisely the expectation of the
multivariatenormalforthelikelihood,namelyE[FT θ +v |D ]. Oncewemakethisconnection
|     |     |     |     |     |     | t+1 | t   | t+1 t |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- |
it simply reduces to applying rules about the expectation operator to the remaining matrices
| and vectors, | ultimately |     | leading | us to | f . |     |     |     |     |
| ------------ | ---------- | --- | ------- | ----- | --- | --- | --- | --- | --- |
t+1
However it is not su(cid:30)cient to simply calculate the mean, we must also know the variance of
tomorrow’s observation given today’s data, otherwise we cannot truly characterise the distribu-
| tion on which | to  | draw tomorrow’s |     | prediction. |     |     |     |     |     |
| ------------- | --- | --------------- | --- | ----------- | --- | --- | --- | --- | --- |
Var[FT
|     |     |     | Var[y | t+1 |D t | ] = |     | θ t +v t+1 | |D t ] | (11.23) |
| --- | --- | --- | ----- | -------- | --- | --- | ---------- | ------ | ------- |
t+1
|     |     |     |     |     | =   | FT Var[θ | |D   | ]F +V     | (11.24) |
| --- | --- | --- | --- | --- | --- | -------- | ---- | --------- | ------- |
|     |     |     |     |     |     | t+1      | t+1  | t t+1 t+1 |         |
|     |     |     |     |     | =   | FT R     | F +V |           | (11.25) |
|     |     |     |     |     |     | t+1 t+1  | t+1  | t+1       |         |
|     |     |     |     |     | =   | Q        |      |           | (11.26) |
t+1
Now that we have the expectation and variance of tomorrow’s observation, given today’s
data, we are able to provide the general forecast for k steps ahead, by fully characterising the
| distribution | on  | which these | predictions |     | are     | drawn: |       |     |         |
| ------------ | --- | ----------- | ----------- | --- | ------- | ------ | ----- | --- | ------- |
|              |     |             |             | y   | |D ∼N(f |        | ,Q    | )   | (11.27) |
|              |     |             |             | t+k | t       | t+k|t  | t+k|t |     |         |
Note that I have used some odd notation here - what does it mean to have a subscript of
t+k|t? Actually, it allows us to write a convenient shorthand for the following:
FT Gk−1a
|     |     | f t+k|t | =   |     |     | t+1 |     |     | (11.28) |
| --- | --- | ------- | --- | --- | --- | --- | --- | --- | ------- |
t+k
|     |     | Q     | =   | FT  | R F | +V  |     |     | (11.29) |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | ------- |
|     |     | t+k|t |     | t+k | t+k | t+k | t+k |     |         |
k
(cid:88)
|     |     | R     | =   | Gk−1R |     | (Gk−1)T | + Gk−jW | (Gk−j)T | (11.30) |
| --- | --- | ----- | --- | ----- | --- | ------- | ------- | ------- | ------- |
|     |     | t+k|t |     |       | t+1 |         |         | t+j     |         |
j=2
AsI’vementionedrepeatedlyinthischapter, weshouldnotconcernourselvestoomuchwith
the verboseness of the Kalman Filter and its notation, rather we should think about the overall
| procedure | and | its Bayesian | underpinnings. |     |     |     |     |     |     |
| --------- | --- | ------------ | -------------- | --- | --- | --- | --- | --- | --- |
Thus we now have the means of predicting new values of the series. This is an alternative
tothepredictionsproducedbycombiningARIMAandGARCH.Insubsequentchapterslaterin
the book we will actually carry this out for some real (cid:28)nancial data and apply it to a predictive
trading model.
We will also be able to use the "(cid:28)lter" aspect to provide us with continually updated views
on a linear hedge ratio between two cointegrated pairs of assets, such as might be found in a
| stastical | arbitrage | strategy. |     |     |     |     |     |     |     |
| --------- | --------- | --------- | --- | --- | --- | --- | --- | --- | --- |

132

Part IV
| Statistical | Machine | Learning |
| ----------- | ------- | -------- |
133

| Chapter |     | 12        |     |     |     |     |
| ------- | --- | --------- | --- | --- | --- | --- |
| Model   |     | Selection |     |     | and |     |
Cross-Validation
InthischapterIwanttodiscussoneofthemostimportantandtrickyissuesinmachinelearning,
thatofmodel selection andthebias-variance tradeo(cid:27). Thelatterisoneofthemostcrucialissues
in helping us achieve pro(cid:28)table trading strategies based on machine learning techniques.
Model selection refers to our ability to assess performance of di(cid:27)ering machine learning
| models | in order | to choose | the | best one. |     |     |
| ------ | -------- | --------- | --- | --------- | --- | --- |
The bias-variance tradeo(cid:27) is a particular property of all (supervised) machine learning
models, that enforces a tradeo(cid:27) between how "(cid:29)exible" the model is and how well it performs
on unseen data. The latter is known as a models generalisation performance.
| 12.1 | Bias-Variance |     |     | Trade-O(cid:27) |     |     |
| ---- | ------------- | --- | --- | --------------- | --- | --- |
We will begin by understanding why model selection is important and then discuss the bias-
variancetradeo(cid:27)qualitatively. Wewillwrapupthechapterbyderivingthebias-variancetradeo(cid:27)
mathematically and discuss measures to minimise the problems it introduces.
In this chapter we are considering supervised regression models. That is, models which are
trained on a set of labelled training data and produce a quantitative response. An example of
thiswouldbeattemptingtopredictfuturestockpricesbasedonotherfactorssuchaspastprices,
| interest | rates or | foreign | exchange | rates. |     |     |
| -------- | -------- | ------- | -------- | ------ | --- | --- |
This is in contrast to a categorical or binary response model as in the case of supervised
classi(cid:28)cation. An example of a classi(cid:28)cation setting would be attempting to assign a topic to a
text document, from a (cid:28)nite set of topics. The bias-variance and model selection situations for
classi(cid:28)cation are extremely similar to the regression setting and simply require modi(cid:28)cation to
| handle | the di(cid:27)ering | ways     | in which | errors | and performance | are measured. |
| ------ | ------------------- | -------- | -------- | ------ | --------------- | ------------- |
| 12.1.1 | Machine             | Learning |          | Models |                 |               |
As with most of our discussions in machine learning the basic model is given by the following:
Y =f(X)+(cid:15) (12.1)
This states that the response vector, Y, is given as a (potentially non-linear) function, f, of
X,
the predictor vector, with a set of normally distributed error terms that have mean zero and
| a standard | deviation | of        | one.         |     |     |     |
| ---------- | --------- | --------- | ------------ | --- | --- | --- |
| What       | does      | this mean | in practice? |     |     |     |
As an example, our vector X could represent a set of lagged (cid:28)nancial prices, similar to the
time series autoregressive models we considered earlier in the book. It could also represent
interest rates, derivatives prices, real-estate prices, word-frequencies in a document or any other
| factor that | we  | consider | useful | in making | a prediction. |     |
| ----------- | --- | -------- | ------ | --------- | ------------- | --- |
135

136
Y
The vector could be single or multi-valued. In the former case it might simply represent
tomorrow’s stock price, in the latter case it might represent the next week’s daily predicted
prices.
f representsourviewontheunderlyingrelationshipbetweenY andX. Thiscouldbelinear,
in which case we may estimate f via a linear regression model. It may be non-linear, in which
case we may estimate f with a Support Vector Machine or a spline-based method, for instance.
Theerrorterms(cid:15)representallofthefactorsthata(cid:27)ectY thatwehaven’ttakenintoaccount
with our function f. They are essentially the "unknown" components of our prediction model.
It is commmon to assume that these are normally distributed with mean zero and a standard
| deviation | of one. |     |     |     |     |     |     |
| --------- | ------- | --- | --- | --- | --- | --- | --- |
In this section we are going to describe how to measure the performance of an estimate
for the (unknown) function f. As with the time series models discussed previously, such an
| estimate | uses "hat" | notation. | Hence, | fˆ can be read | as "the estimate | of f". |     |
| -------- | ---------- | --------- | ------ | -------------- | ---------------- | ------ | --- |
In addition we will describe the e(cid:27)ect on the performance of the model as we make it more
(cid:29)exible. Flexibilitydescribestheabilitytoincreasethedegrees of freedom availabletothemodel
to"(cid:28)t"tothetrainingdata. Wewillseethattherelationshipbetween(cid:29)exibilityandperformance
error is non-linear and thus we need to be extremely careful when choosing the "best" model.
Notethatthereisnevera"best"modelacrosstheentiretyofstatistics,timeseriesormachine
learning. Di(cid:27)erentmodelshavevaryingstrengthsandweaknesses. Onemodelmaywork
verywellononedataset,butmayperformbadlyonanother. Thechallengeinstatisticalmachine
learning is to pick the "best" model for the problem at hand with the data available.
| 12.1.2 | Model | Selection |     |     |     |     |     |
| ------ | ----- | --------- | --- | --- | --- | --- | --- |
Whentryingtoascertainwhichstatisticalmachinelearningmethodisbestweneedsomemeansof
characterisingtherelativeperformancebetweenmodels. Inthetimeseriessectionweconsidered
theAkaikeInformationCriterionandtheBayesianInformationCriterion. Inthissectionwewill
| consider | other methods. |     |     |     |     |     |     |
| -------- | -------------- | --- | --- | --- | --- | --- | --- |
To determine model suitability we need to compare the known values of the underlying rela-
| tionship | with those | that | are predicted | by an estimated | model. |     |     |
| -------- | ---------- | ---- | ------------- | --------------- | ------ | --- | --- |
Forinstance,ifweareattemptingtopredicttomorrow’sstockprices,thenwewishtoevaluate
how close our models predictions are to the true value on that particular day.
This motivates the concept of a loss function, which quantitatively compares the di(cid:27)erence
| between | the true | values | with the predicted | values. |     |     |     |
| ------- | -------- | ------ | ------------------ | ------- | --- | --- | --- |
|         |          |        |                    |         | fˆ  |     | fˆ  |
Let’s assume that we have created an estimate of the underlying relationship f. might
be a linear regression or a Random Forest model, for instance. fˆ will have been trained on a
particular data set, τ, which contains predictor-response pairs. If there are N such pairs then τ
is given by:
|     |     |     | τ ={(X | ,Y ),...,(X | ,Y )} |     | (12.2) |
| --- | --- | --- | ------ | ----------- | ----- | --- | ------ |
|     |     |     |        | 1 1         | N N   |     |        |
The X represent the prediction factors, which could be prior lagged prices for a series or
i
some other factors, as mentioned above. The Y i could be the predictions for our stock prices in
the following period. In this instance, N represents the number of days of data that we have
available.
|     |     |     | L(Y,fˆ(X)). |     |     |     | fˆ  |
| --- | --- | --- | ----------- | --- | --- | --- | --- |
The loss function is denoted by Its job is to compare the predictions made by
at particular values of X to their true values given by Y. A common choice for L is the absolute
error:
|     |     |     | L(Y,fˆ(X))=|Y | −fˆ(X)| |     |     |     |
| --- | --- | --- | ------------- | ------- | --- | --- | --- |
(12.3)
| Another | popular | choice | is the squared | error:   |     |     |     |
| ------- | ------- | ------ | -------------- | -------- | --- | --- | --- |
|         |         |        | L(Y,fˆ(X))=(Y  | −fˆ(X))2 |     |     |     |
(12.4)

137
Note that both choices of loss function are non-negative. Hence the "best" loss for a model
is zero, that is, there is no di(cid:27)erence between the prediction and the true value.
| Training | Error versus | Test Error |     |     |     |     |
| -------- | ------------ | ---------- | --- | --- | --- | --- |
Nowthatwehavealossfunctionweneedsomewayofaggregatingthevariousdi(cid:27)erencesbetween
the true values and the predicted values. One way to do this is to de(cid:28)ne the Mean Squared
Error (MSE), which is simply the average, or expectation value, of the squared loss:
1 (cid:88) N
|     |     |     |     | −fˆ(X | ))2 |        |
| --- | --- | --- | --- | ----- | --- | ------ |
|     |     | MSE | :=  | (Y i  | i   | (12.5) |
N
i=1
The de(cid:28)nition simply states that the Mean Squared Error is the average of all of the squared
fˆ(X
di(cid:27)erences between the true values Y and the predicted values ). A smaller MSE means
i i
| that the estimate | is more | accurate. |     |     |     |     |
| ----------------- | ------- | --------- | --- | --- | --- | --- |
ItisimportanttorealisethatthisMSEvalueiscomputedusingonlythetraining data. That
is, it is computed using only the data that the model was (cid:28)tted on. Hence, it is actually known
| as the training | MSE. |     |     |     |     |     |
| --------------- | ---- | --- | --- | --- | --- | --- |
In practice this value is of little interest to us. What we are really concerned about is how
| well the model | can predict | values | on new | unseen data. |     |     |
| -------------- | ----------- | ------ | ------ | ------------ | --- | --- |
For instance, we are not really interested in how well the model can predict past stock prices
of the following day, we are only concerned with how it can predict the following days stock
prices going forward. This quanti(cid:28)cation of a models performance is known as its generalisation
| performance. | It is what | we are really | interested | in. |     |     |
| ------------ | ---------- | ------------- | ---------- | --- | --- | --- |
Mathematically, if we have a new prediction value X and a true response Y , then we wish
0 0
to take the expectation across all such new values to come up with the test MSE:
|     |     |      |        | (cid:104) | (cid:105) |        |
| --- | --- | ---- | ------ | --------- | --------- | ------ |
|     |     |      | MSE:=E | (Y −fˆ(X  | ))2       |        |
|     |     | Test |        | 0         | 0         | (12.6) |
Where the expectation is taken across all new unseen predictor-response pairs (X ,Y ).
0 0
Our goal is to select the model where the test MSE is lowest across choices of other models.
Unfortunately it is di(cid:30)cult to calculate the test MSE! This is because we are often in a
| situation | where we do not | have any | test data | available. |     |     |
| --------- | --------------- | -------- | --------- | ---------- | --- | --- |
In general machine learning domains this can be quite common. In quantitative trading we
are (usually) in a "data rich" environment and thus we can retain some of our data for training
and some for testing. In the next section we will discuss cross-validation, which is one means of
| utilising subsets | of the | training data | in order | to estimate | the test MSE. |     |
| ----------------- | ------ | ------------- | -------- | ----------- | ------------- | --- |
A pertinent question to ask at this stage is "Why can we not simply use the model with
the lowest training MSE?". The simple answer is that there is no guarantee that the model
with the lowest training MSE will also be the model with the lowest test MSE. Why is this so?
The answer lies in a particular property of statistical machine learning methods known as the
| bias-variance | tradeo(cid:27).   |     |                |     |     |     |
| ------------- | ----------------- | --- | -------------- | --- | --- | --- |
| 12.1.3        | The Bias-Variance |     | Tradeo(cid:27) |     |     |     |
Let’s consider a slightly contrived situation where we know the underlying "true" relationship
between Y and X, which I will state is given by a sinusoidal function, f = sin, such that
Y =f(X)=sin(X). Note that in reality we will not ever know the underlying f, which is why
| we are estimating | it in | the (cid:28)rst place! |     |     |     |     |
| ----------------- | ----- | ---------------------- | --- | --- | --- | --- |
ForthiscontrivedsituationIhavecreatedasetoftrainingpoints,τ,givenbyY =sin(X )+(cid:15) ,
i i i
where (cid:15) are draws from a standard normal distribution (mean of zero, standard deviation equal
i
to one). This can be seen in Figure 12.1. The black curve is the "true" function f, restricted to
the interval [0,2π], while the circled points represent the Y simulated data values.
i
We can now try to (cid:28)t a few di(cid:27)erent models to this training data. The (cid:28)rst model, given by
the green line, is a linear regression (cid:28)tted with ordinary least squares estimation. The second

138
Figure 12.1: Various estimates of the underlying sinusoidal model, f =sin
model, given by the blue line, is a polynomial model with degree m=3. The third model, given
by the red curve is a higher degree polynomial with degree m=20. Between each of the models
I have varied the (cid:29)exibility, that is, the degrees of freedom (DoF). The linear model is the least
(cid:29)exible withonlytwoDoF.Themost(cid:29)exiblemodelisthepolynomialoforderm=20. Itcanbe
seen that the polynomial of order m=3 is the apparent closest (cid:28)t to the underlying sinusoidal
relationship.
For each of these models we can calculate the training MSE. It can be seen in Figure 12.2
thatthetrainingMSE(givenbythegreencurve)decreasesmonotonicallyasthe(cid:29)exibilityofthe
model increases. This makes sense, since the polynomial (cid:28)t can become as (cid:29)exible as we need it
to in order to minimise the di(cid:27)erence between its values and those of the sinusoidal data.
However, if we plot the test MSE (given by the blue curve) the situation is vastly di(cid:27)erent.
The test MSE initially decreases as we increase the (cid:29)exibility of the model but eventually starts
to increase again after we introduce a lot of (cid:29)exibility. Why is this? By allowing the model to
be extremely (cid:29)exible we are letting it (cid:28)t to "patterns" in the training data.
However, as soon as we introduce new unseen data points in the test set the model cannot
generalise well because these "patterns" are only random artifacts of the training data and are
not an underlying property of the true sinusoidal form. We are in a situation of over(cid:28)tting.
Infact,thispropertyofa"u-shaped"testMSEasafunctionofmodel(cid:29)exibilityisanintrinsic
property of statistical machine learning models, known as the bias-variance tradeo(cid:27).
Itcanbeshown(seebelowintheMathematicalExplanation section)thattheexpected test
MSE, where the expectation is taken across many training sets, is given by:
(cid:104) (cid:105)2
E(Y −fˆ(X ))2 =Var(fˆ(X ))+ Biasfˆ(X ) +Var((cid:15)) (12.7)
0 0 0 0
The (cid:28)rst term on the right hand side is the variance of the estimate across many training
sets. It determines how much the average model estimation deviates as di(cid:27)erent training data
are tried. In particular, a model with high variance is suggestive that it is over(cid:28)t to the training
data.

139
Figure 12.2: Training MSE and Test MSE as a function of model (cid:29)exibility.
The middle term is the squared bias, which characterises the di(cid:27)erence between the averages
of the estimate and the true values. A model with high bias is not capturing the underlying be-
haviourofthetruefunctionalformwell. Onecanimaginethesituationwherealinearregression
is used to model a sine curve (as above). No matter how well "(cid:28)t" to the data the model is, it
| will never | capture | the non-linearity |     | inherant | in a sine | curve. |
| ---------- | ------- | ----------------- | --- | -------- | --------- | ------ |
The (cid:28)nal term is known as the irreducible error. It is the minimum lower bound for the
test MSE. Since we only ever have access to the training data points (including the randomness
associated with the (cid:15) values) we can’t ever hope to get a "more accurate" (cid:28)t than what the
| variance | of the | residuals | o(cid:27)er. |     |     |     |
| -------- | ------ | --------- | ------------ | --- | --- | --- |
Generally, as (cid:29)exibility increases we see an increase in variance and a decrease in bias. How-
ever it is the relative rate of change between these two factors that determines whether the
| expected | test MSE | increases | or decreases. |     |     |     |
| -------- | -------- | --------- | ------------- | --- | --- | --- |
As (cid:29)exibility is increased the bias will tend to drop quickly (faster than the variance can
increase) and so we see a drop in test MSE. However, as (cid:29)exibility increases further, there is
less reduction in bias (because the (cid:29)exibility of the model can (cid:28)t the training data easily) and
| instead | the variance | rapidly | increases, |     | due to the model | being over(cid:28)t. |
| ------- | ------------ | ------- | ---------- | --- | ---------------- | -------------------- |
Our ultimate goal in machine learning is to try and minimise the expected test
MSE, that is we must choose a statistical machine learning model that simultane-
| ously has | low | variance | and | low bias. |     |     |
| --------- | --- | -------- | --- | --------- | --- | --- |
Ifyouwishtogainamoremathematicallyprecisede(cid:28)nitionofthebias-variancetradeo(cid:27)then
| you can | read the     | next section. |             |     |     |     |
| ------- | ------------ | ------------- | ----------- | --- | --- | --- |
| A More  | Mathematical |               | Explanation |     |     |     |
We’ve now qualitatively outlined the issues surrounding model (cid:29)exibility, bias and variance.
In the following box we are going to carry out a mathematical decomposition of the expected
prediction error for a particular model estimate, fˆ(X) with prediction vector X =x using the
0
| latter of | our loss | functions, | the | squared-error | loss: |     |
| --------- | -------- | ---------- | --- | ------------- | ----- | --- |

140
X
The de(cid:28)nition of the squared error loss, at the prediction point 0 , is given by:
|     |     |     |     | (cid:20)(cid:16) |     |     | (cid:21) |     |     |
| --- | --- | --- | --- | ---------------- | --- | --- | -------- | --- | --- |
(cid:17)2
|     |     | Err(X | )=E | Y   | −fˆ(X | ) |X | =X  |     | (12.8) |
| --- | --- | ----- | --- | --- | ----- | ---- | --- | --- | ------ |
|     |     |       | 0   |     | 0     |      | 0   |     |        |
However, we can expand the expectation on the right hand side into three terms:
|     |       |       | (cid:104) |         | (cid:105)2 | (cid:104) |              | (cid:105)2 |        |
| --- | ----- | ----- | --------- | ------- | ---------- | --------- | ------------ | ---------- | ------ |
|     |       | )=σ2+ | Efˆ(X     |         |            | +E        | fˆ(X )−Efˆ(X |            |        |
|     | Err(X | 0     |           | 0 )−f(X | 0 )        |           | 0            | 0 )        | (12.9) |
(cid:15)
The (cid:28)rst term on the RHS is known as the irreducible error. It is the lower bound on the
| possible expected |     | prediction | error. |     |     |     |     |     |     |
| ----------------- | --- | ---------- | ------ | --- | --- | --- | --- | --- | --- |
The middle term is the squared bias and represents the di(cid:27)erence in the average value of all
predictions at X , across all possible training sets, and the true mean value of the underlying
0
X
| function | at 0 . |     |     |     |     |     |     |     |     |
| -------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
Thiscanbethoughtofastheerrorintroducedbythemodelinnotrepresentingtheunderlying
behaviour of the true function. For example, using a linear model when the phenomena is
| inherently | non-linear. |     |     |     |     |     |     |     |     |
| ---------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
The third term is known as the variance. It characterises the error that is introduced as the
model becomes more (cid:29)exible, and thus more sensitive to variation across di(cid:27)ering training sets,
τ.
|     |     | Err(X | ) = | σ2+Bias2+Var(fˆ(X |                      |     | ))  |     | (12.10) |
| --- | --- | ----- | --- | ----------------- | -------------------- | --- | --- | --- | ------- |
|     |     |       | 0   | (cid:15)          |                      |     | 0   |     |         |
|     |     |       | =   | Irreducible       | Error+Bias2+Variance |     |     |     | (12.11) |
It is important to remember that σ2 represents an absolute lower bound on the expected
(cid:15)
predictionerror. Whiletheexpectedtrainingerrorcanbereducedmonotonicallytozero(justby
increasing model (cid:29)exibility), the expected prediction error will always be at least the irreducible
| error, even | if the squared   | bias | and | variance | are both | zero. |     |     |     |
| ----------- | ---------------- | ---- | --- | -------- | -------- | ----- | --- | --- | --- |
| 12.2        | Cross-Validation |      |     |          |          |       |     |     |     |
In this section we will attempt to (cid:28)nd a partial remedy to the problem of an over(cid:28)t machine
| learning model | using | a technique | known | as  | cross-validation. |     |     |     |     |
| -------------- | ----- | ----------- | ----- | --- | ----------------- | --- | --- | --- | --- |
Firstly we will de(cid:28)ne cross-validation and then describe how it works. Secondly, we will
constructaforecastingmodelusinganequityindexandthenapplytwocross-validationmethods
to this example: the validation set approach and k-fold cross-validation. Finally we will
discuss the code for the simulations using Python, Pandas, Matplotlib and Scikit-Learn.
Ourgoalistoeventuallycreateasetofstatisticaltoolsthatcanbeusedwithinabacktesting
framework to help us minimise the problem of over(cid:28)tting a model and thus constrain future
| losses due | to a poorly | performing |                  | strategy | based on | such | a model. |     |     |
| ---------- | ----------- | ---------- | ---------------- | -------- | -------- | ---- | -------- | --- | --- |
| 12.2.1     | Overview    | of         | Cross-Validation |          |          |      |          |     |     |
Recall from the section above the de(cid:28)nitions of test error and (cid:29)exibility:
(cid:136)
Test Error-Theaverageerror,wheretheaverageisacrossmanyobservations,associated
with the predictive performance of a particular statistical model when assessed on new
| observations |     | that were | not used | to train | the model. |     |     |     |     |
| ------------ | --- | --------- | -------- | -------- | ---------- | --- | --- | --- | --- |
(cid:136)
Flexibility-Thedegreesoffreedomavailabletothemodelto"(cid:28)t"tothetrainingdata. A
linearregressionisveryin(cid:29)exible(itonlyhastwodegreesoffreedom)whereasahigh-degree
polynomial is very (cid:29)exible (and as such can have many degrees of freedom).

141
| With | these | concepts | in mind | we  | can now | de(cid:28)ne | cross-validation: |
| ---- | ----- | -------- | ------- | --- | ------- | ------------ | ----------------- |
Thegoalofcross-validationistoestimatethetesterrorassociatedwithastatisticalmodel
or select the appropriate level of (cid:29)exibility for a particular statistical method.
Again, we can recall from the section above that the training error associated with a model
can vastly underestimate the test error of the model. Cross-validation provides us with the
capability to more accurately estimate the test error, which we will never know in practice.
Cross-validation works by holding out particular subsets of the training set in order to use
them as test observations. In this section we will discuss the various ways in which such subsets
are held out as well as implement the methods using Python on an example forecasting model
| based on | prior       | historical | data.   |     |     |     |     |
| -------- | ----------- | ---------- | ------- | --- | --- | --- | --- |
| 12.2.2   | Forecasting |            | Example |     |     |     |     |
In order to make the following theoretical discussion concrete we will consider the development
of a new trading strategy based on the prediction of price levels of an equity index. Let’s
choose the FTSE100, which contains a weighted grouping of the one hundred largest (by market
capitalisation) publicly traded (cid:28)rms on the London Stock Exchange (LSE). Equally we could
| pick the | S&P500, | as in | the time | series | sections, | or  | the DAX. |
| -------- | ------- | ----- | -------- | ------ | --------- | --- | -------- |
For this strategy we will simply consider the closing price of the historical daily Open-High-
Low-Close(OHLC)barsaspredictors andthefollowingday’sclosingpriceastheresponse. Hence
we are attempting to predict tomorrow’s price using daily historic prices. This is similar to an
autoregressivemodelfromthetimeseriessectionexceptthatwewillusebothalinearregression
| and a non-linear |     | polynomial |     | regression | as our | machine | learning models. |
| ---------------- | --- | ---------- | --- | ---------- | ------ | ------- | ---------------- |
|                  |     |            |     |            |        |         | X y,             |
An observation will consist of a pair of vectors, and which contain the predictor values
and the response value respectively. If we consider a daily lag of p days, then X has p compo-
nents. Each of these components represents the closing price from one day further behind. X
p
representstoday’sclosingprice(known),whileX p−1 representstheclosingpriceyesterday,while
| X represents |     | the price | p−1 | days ago. |     |     |     |
| ------------ | --- | --------- | --- | --------- | --- | --- | --- |
1
Y
contains only a single value, namely tomorrow’s closing price, and is thus a scalar. Hence
each observation is a tuple (X,y). We will consider a set of n observations corresponding to n
days worth of historical pricing information about the FTSE100 (see Fig 12.3).
|     |     | Figure | 12.3: | The FTSE100 |     | Index | - Image Credit: Wikipedia |
| --- | --- | ------ | ----- | ----------- | --- | ----- | ------------------------- |
Ourgoalisto(cid:28)ndastatisticalmodelthatattemptstopredictthepriceleveloftheFTSE100
based on the previous days prices. If we were to achieve an accurate prediction, we could use it
| to generate | basic | trading | signals. |     |     |     |     |
| ----------- | ----- | ------- | -------- | --- | --- | --- | --- |

142
We will use cross-validation in two ways: Firstly to estimate the test error of particular
statistical learning methods (i.e. their separate predictive performance), and secondly to select
the optimal (cid:29)exibility of the chosen method in order to minimise the errors associated with bias
and variance.
We will now outline the di(cid:27)ering ways of carrying out cross-validation, starting with the
validation set approach and then (cid:28)nally k-fold cross validation. In each case we will use Pandas
| and Scikit-Learn | to implement |              | these methods. |     |     |     |
| ---------------- | ------------ | ------------ | -------------- | --- | --- | --- |
| 12.2.3           | Validation   | Set Approach |                |     |     |     |
The validation set approach to cross-validation is very simple to carry out. Essentially we take
the set of observations (n days of data) and randomly divide them into two equal halves. One
halfisknownasthetraining set whilethesecondhalfisknownasthevalidation set. Themodel
is (cid:28)t using only the data in the training set, while its test error is estimated using only the
| validation | set. |     |     |     |     |     |
| ---------- | ---- | --- | --- | --- | --- | --- |
This is easily recognisable as a technique often used in quantitative trading as a mechanism
for assessing predictive performance. However, it is more common to (cid:28)nd two-thirds of the data
used for the training set, while the remaining third is used for validation. In addition it is more
common to retain the ordering of the time series such that the (cid:28)rst two-thirds chronologically
| represents | the (cid:28)rst two-thirds | of  | the historical | data. |     |     |
| ---------- | -------------------------- | --- | -------------- | ----- | --- | --- |
What is less common when applying this method is randomising the observations into each
of thetwo separatesets. Evenless common isa discussion as towhat subtle problems canarises
| when this | is carried out. |     |     |     |     |     |
| --------- | --------------- | --- | --- | --- | --- | --- |
Firstly, and especially in situations with limited data, the procedure can lead to a high
variance for the estimate of the test error due to the randomisation of the samples. This is a
typical "gotcha" when carrying out the validation set approach to cross-validation. It is all too
possibletoachievealowtesterrorsimplythroughblindluckonreceivinganappropriaterandom
samplesplit. Hencethetruetesterror(i.e. predictivepower)canbesigni(cid:28)cantlyunderestimated.
Secondly, note that in the 50-50 split of testing/training data we are leaving out half of all
observations. Hence we are reducing information that would otherwise be used to train the
model. Thus it is likely to perform worse than if we had used all of the observations, including
those in the validation set. This leads to a situation where we may actually overestimate the
| test error | for the full | data set. |     |     |     |     |
| ---------- | ------------ | --------- | --- | --- | --- | --- |
In order to reduce the impact of these issues we will consider a more sophisticated splitting
| of the data | known as     | k-fold cross | validation. |     |     |     |
| ----------- | ------------ | ------------ | ----------- | --- | --- | --- |
| 12.2.4      | k-Fold Cross | Validation   |             |     |     |     |
K-foldcross-validationimprovesuponthevalidationsetapproachbydividingthenobservations
into k mutually exclusive, and approximately equally sized, subsets known as "folds".
The (cid:28)rst fold becomes a validation set, while the remaining k−1 folds (aggregated together)
become the training set. The model is (cid:28)t on the training set and its test error is estimated on
the validation set. This procedure isrepeated k times, with eachrepetition holdingout a foldas
| the validation | set, while | the remaining | k−1 | are used | for training. |     |
| -------------- | ---------- | ------------- | --- | -------- | ------------- | --- |
This allows an overall test estimate, CV , to be calculated that is an average of all the
k
| individual | mean-squared | errors, | MSE , for | each fold: |     |     |
| ---------- | ------------ | ------- | --------- | ---------- | --- | --- |
i
k
|     |     |     |     | 1 (cid:88) |     |         |
| --- | --- | --- | --- | ---------- | --- | ------- |
|     |     |     | CV  | = MSE      |     | (12.12) |
|     |     |     | k   |            | i   |         |
k
i=1
The obvious question that arises at this stage is what value do we choose for k? The short
answer (based on empirical studies) is to choose k = 5 or k = 10. The longer answer to this
question relates to both computational expense and, once again, the bias-variance tradeo(cid:27).

143
| Leave-One-Out |     | Cross | Validation |     |     |     |
| ------------- | --- | ----- | ---------- | --- | --- | --- |
We can actually choose k = n, which means that we (cid:28)t the model n times, with only a sin-
gle observation left out for each (cid:28)tting. This is known as leave-one-out cross-validation
(LOOCV).Itcanbeverycomputationallyexpensive,particularlyifnislargeandthemodelhas
| an expensive | (cid:28)tting |     | procedure. |     |     |     |
| ------------ | ------------- | --- | ---------- | --- | --- | --- |
While LOOCV is bene(cid:28)cial from the point of reducing bias, due to the fact that nearly all
of the samples are used for (cid:28)tting in each case, it actually su(cid:27)ers from the problem of high
variance. Thisisbecausewearecalculatingthetesterroronasingle response eachtimeforeach
| observation | in  | the data | set. |     |     |     |
| ----------- | --- | -------- | ---- | --- | --- | --- |
k-fold cross-validation reduces the variance at the expense of introducing some more bias,
due to the fact that some of the observations are not used for training. With k = 5 or k = 10
| the bias-variance |        | tradeo(cid:27) | is generally   | optimised. |     |     |
| ----------------- | ------ | -------------- | -------------- | ---------- | --- | --- |
| 12.2.5            | Python |                | Implementation |            |     |     |
We are quite lucky when working with Python and its library ecosystem as much of the "heavy
lifting" is done for us. Using Pandas, Scikit-Learn and Matplotlib, we can rapidly create some
| examples  | to show | the  | usage and | issues surrounding |     | cross-validation. |
| --------- | ------- | ---- | --------- | ------------------ | --- | ----------------- |
| Obtaining | the     | Data |           |                    |     |                   |
The(cid:28)rsttaskistoobtainthedataandputitinaformatwecanuse. I’veactuallycarriedoutthis
procedure in my previous book Successful Algorithmic Trading but I’d like to have this section
asself-containedaspossible,soyoucanusethefollowingcodetoobtainhistoricaldatafromany
(cid:28)nancial time series available on Yahoo Finance, as well as their associated daily predictor lag
values:
| from __future__ |     | import | print_function |     |     |     |
| --------------- | --- | ------ | -------------- | --- | --- | --- |
import datetime
| import | numpy  | as np |     |     |     |     |
| ------ | ------ | ----- | --- | --- | --- | --- |
| import | pandas | as    | pd  |     |     |     |
import sklearn
| from pandas.io.data |     |     | import | DataReader |     |     |
| ------------------- | --- | --- | ------ | ---------- | --- | --- |
def create_lagged_series(symbol, start_date, end_date, lags=5):
"""
| This    | creates    |         | a pandas   | DataFrame      | that      | stores      |
| ------- | ---------- | ------- | ---------- | -------------- | --------- | ----------- |
| the     | percentage |         | returns    | of the         | adjusted  | closing     |
| value   | of         | a stock | obtained   | from           | Yahoo     | Finance,    |
| along   | with       | a       | number     | of lagged      | returns   | from the    |
| prior   | trading    |         | days (lags | defaults       |           | to 5 days). |
| Trading |            | volume, | as well    | as the         | Direction | from        |
| the     | previous   |         | day, are   | also included. |           |             |
"""
| # Obtain |               | stock | information | from | Yahoo | Finance |
| -------- | ------------- | ----- | ----------- | ---- | ----- | ------- |
| ts       | = DataReader( |       |             |      |       |         |
symbol,
"yahoo",
start_date
- datetime.timedelta(days=365),
end_date
)

144
# Create the new lagged DataFrame
tslag = pd.DataFrame(index=ts.index)
tslag["Today"] = ts["Adj Close"]
tslag["Volume"] = ts["Volume"]
# Create the shifted lag series of
# prior trading period close values
for i in xrange(0,lags):
tslag["Lag%s" % str(i+1)] = ts["Adj Close"].shift(i+1)
# Create the returns DataFrame
tsret = pd.DataFrame(index=tslag.index)
tsret["Volume"] = tslag["Volume"]
tsret["Today"] = tslag["Today"].pct_change()*100.0
# If any of the values of percentage
# returns equal zero, set them to
# a small number (stops issues with
# QDA model in scikit-learn)
for i,x in enumerate(tsret["Today"]):
if (abs(x) < 0.0001):
tsret["Today"][i] = 0.0001
# Create the lagged percentage returns columns
for i in xrange(0,lags):
tsret["Lag%s" % str(i+1)] = tslag[
"Lag%s" % str(i+1)
].pct_change()*100.0
# Create the "Direction" column
# (+1 or -1) indicating an up/down day
tsret["Direction"] = np.sign(tsret["Today"])
tsret = tsret[tsret.index >= start_date]
return tsret
Note that we are not storing the direct close price values in the "Today" or "Lag" columns.
Instead we are storing the close-to-close percentage return from the previous day.
We need to obtain the data for the FTSE100 daily prices along some suitable time frame. I
have chosen Jan 1st 2004 to Dec 31st 2004. However this is an arbitrary choice. You can adjust
the time frame as you see (cid:28)t. To obtain the data and place it into a Pandas DataFrame called
ftse_lags we can use the following code:
if __name__ == "__main__":
symbol = "^FTSE"
start_date = datetime.datetime(2004, 1, 1)
end_date = datetime.datetime(2004, 12, 31)
ftse_lags = create_lagged_series(
symbol, start_date, end_date, lags=5
)
Atthisstagewehavethenecessarydatatobegincreatingasetofstatisticalmachinelearning
models.
Validation Set Approach
Now that we have the (cid:28)nancial data we need to create a set of predictive regression models we
can use the above cross-validation methods to obtain estimates for the test error.

145
The (cid:28)rst task is to import the models from Scikit-Learn. We will choose a Linear Regression
model with polynomial features. This provides us with the ability to choose varying degrees
of (cid:29)exibility simply by increasing the degree of the features’ polynomial order. Initially we are
| going | to consider | the | validation | set | approach | to cross | validation. |     |     |
| ----- | ----------- | --- | ---------- | --- | -------- | -------- | ----------- | --- | --- |
Scikit-Learn provides a validation set approach via the train_test_split method found
in the cross_validation module. We will also need to import the method for k-fold
KFold
cross validation later, as well as the linear regression model itself. We need to import the MSE
calculation as well as Pipeline and PolynomialFeatures. The latter two allow us to easily
create a set of polynomial feature linear regression models with minimal additional coding:
..
|      | sklearn.cross_validation |     |        |        |                    | train_test_split,  |     |     |       |
| ---- | ------------------------ | --- | ------ | ------ | ------------------ | ------------------ | --- | --- | ----- |
| from |                          |     |        |        | import             |                    |     |     | KFold |
| from | sklearn.linear_model     |     |        | import | LinearRegression   |                    |     |     |       |
| from | sklearn.metrics          |     | import |        | mean_squared_error |                    |     |     |       |
| from | sklearn.pipeline         |     |        | import | Pipeline           |                    |     |     |       |
| from | sklearn.preprocessing    |     |        |        | import             | PolynomialFeatures |     |     |       |
..
Once the modules are imported we can create a FTSE DataFrame that uses (cid:28)ve of the prior
lagging days returns as predictors. We can then create ten separate random splittings of the
| data into | a training |     | and validation |     | set. |     |     |     |     |
| --------- | ---------- | --- | -------------- | --- | ---- | --- | --- | --- | --- |
Finally, for multiple degrees of the polynomial features of the linear regression, we can cal-
culate the test error. This provides us with ten separate test error curves, each value of which
| shows | the test | MSE | for a di(cid:27)ering |     | degree | of polynomial | kernel: |     |     |
| ----- | -------- | --- | --------------------- | --- | ------ | ------------- | ------- | --- | --- |
..
..
validation_set_poly(random_seeds,
| def |     |     |     |     |     | degrees, | X,  | y): |     |
| --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- |
"""
| Use      | the            | train_test_split |       |            | method     | to create        | a        |      |     |
| -------- | -------------- | ---------------- | ----- | ---------- | ---------- | ---------------- | -------- | ---- | --- |
| training |                | set              | and a | validation |            | set (50%         | in each) |      |     |
| using    | "random_seeds" |                  |       | separate   |            | random samplings |          | over |     |
| linear   |                | regression       |       | models     | of varying | flexibility      |          |      |     |
"""
| sample_dict |             | =   | dict( |       |       |             |                  |     |     |
| ----------- | ----------- | --- | ----- | ----- | ----- | ----------- | ---------------- | --- | --- |
|             | [("seed_%s" |     |       |       |       |             | random_seeds+1)] |     |     |
|             |             |     | %     | i,[]) | for i | in range(1, |                  |     |     |
)
| #   | Loop           | over each           | random   |                  | splitting | into                | a train-test |     | split |
| --- | -------------- | ------------------- | -------- | ---------------- | --------- | ------------------- | ------------ | --- | ----- |
| for | i in           | range(1,            |          | random_seeds+1): |           |                     |              |     |       |
|     | print("Random: |                     |          | %s"              | % i)      |                     |              |     |       |
|     | # Increase     |                     | degree   | of               | linear    | regression          | polynomial   |     | order |
|     | for            | d in                | range(1, | degrees+1):      |           |                     |              |     |       |
|     |                | print("Degree:      |          |                  | %s" % d)  |                     |              |     |       |
|     |                | # Create            | the      | model,           | split     | the sets            | and          | fit | it    |
|     |                | polynomial_features |          |                  | =         | PolynomialFeatures( |              |     |       |
include_bias=False
degree=d,
)
linear_regression
= LinearRegression()
|     |     | model                   | = Pipeline([ |     |     |                       |     |     |     |
| --- | --- | ----------------------- | ------------ | --- | --- | --------------------- | --- | --- | --- |
|     |     | ("polynomial_features", |              |     |     | polynomial_features), |     |     |     |
|     |     | ("linear_regression",   |              |     |     | linear_regression)    |     |     |     |
])
|     |     | X_train, | X_test, |     | y_train, | y_test | train_test_split( |     |     |
| --- | --- | -------- | ------- | --- | -------- | ------ | ----------------- | --- | --- |
=
|     |     | X,  | y,  | test_size=0.5, |     | random_state=i |     |     |     |
| --- | --- | --- | --- | -------------- | --- | -------------- | --- | --- | --- |

146
)
|     | model.fit(X_train, |            |                       | y_train) |        |        |        |     |
| --- | ------------------ | ---------- | --------------------- | -------- | ------ | ------ | ------ | --- |
|     | #                  | Calculate  | the                   | test MSE | and    | append | to the |     |
|     | #                  | dictionary | of                    | all test | curves |        |        |     |
|     | y_pred             |            | model.predict(X_test) |          |        |        |        |     |
=
|     | test_mse              |       | = mean_squared_error(y_test, |           |                       |     | y_pred) |     |
| --- | --------------------- | ----- | ---------------------------- | --------- | --------------------- | --- | ------- | --- |
|     | sample_dict["seed_%s" |       |                              |           | % i].append(test_mse) |     |         |     |
| #   | Convert               | these | lists                        | into      | numpy                 |     |         |     |
| #   | arrays                | to    | perform                      | averaging |                       |     |         |     |
sample_dict["seed_%s"
|     |                       |     |     | % i] | = np.array( |     |     |     |
| --- | --------------------- | --- | --- | ---- | ----------- | --- | --- | --- |
|     | sample_dict["seed_%s" |     |     |      | % i]        |     |     |     |
)
| # Create | the | "average | test    | MSE" | series     | by  | averaging  | the    |
| -------- | --- | -------- | ------- | ---- | ---------- | --- | ---------- | ------ |
| # test   | MSE | for each | degree  | of   | the linear |     | regression | model, |
| # across | all | random   | samples |      |            |     |            |        |
sample_dict["avg"]
|                    |             |     | = np.zeros(degrees) |                          |     |     |     |     |
| ------------------ | ----------- | --- | ------------------- | ------------------------ | --- | --- | --- | --- |
| for i              | in range(1, |     | random_seeds+1):    |                          |     |     |     |     |
| sample_dict["avg"] |             |     |                     | += sample_dict["seed_%s" |     |     | %   | i]  |
| sample_dict["avg"] |             |     | float(random_seeds) |                          |     |     |     |     |
/=
return sample_dict
..
..
WecanuseMatplotlibtoplotthisdata. Weneedtoimportpylabandthencreateafunction
| to plot the | test error | curves: |     |     |     |     |     |     |
| ----------- | ---------- | ------- | --- | --- | --- | --- | --- | --- |
..
| import pylab | as  | plt |     |     |     |     |     |     |
| ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
..
..
def plot_test_error_curves_vs(sample_dict, random_seeds, degrees):
| fig, | ax =     | plt.subplots() |     |     |     |     |     |     |
| ---- | -------- | -------------- | --- | --- | --- | --- | --- | --- |
| ds = | range(1, | degrees+1)     |     |     |     |     |     |     |
random_seeds+1):
| for i | in range(1, |     |     |     |     |     |     |     |
| ----- | ----------- | --- | --- | --- | --- | --- | --- | --- |
ax.plot(
ds,
sample_dict["seed_%s"
% i],
lw=2,
|     | label=’Test |     | MSE | - Sample | %s’ | % i |     |     |
| --- | ----------- | --- | --- | -------- | --- | --- | --- | --- |
)
ax.plot(
ds,
sample_dict["avg"],
linestyle=’--’,
color="black",
lw=3,
| label=’Avg |     | Test | MSE’ |     |     |     |     |     |
| ---------- | --- | ---- | ---- | --- | --- | --- | --- | --- |
)
ax.legend(loc=0)
| ax.set_xlabel(’Degree |     |     | of  | Polynomial |     | Fit’) |     |     |
| --------------------- | --- | --- | --- | ---------- | --- | ----- | --- | --- |
ax.set_ylabel(’Mean
|                   |     |     | Squared | Error’) |     |     |     |     |
| ----------------- | --- | --- | ------- | ------- | --- | --- | --- | --- |
| ax.set_ylim([0.0, |     |     | 4.0])   |         |     |     |     |     |

147
fig.set_facecolor(’white’)
plt.show()
..
..
We have selected the degree of our polynomial features to vary between d=1 to d=3, thus
providinguswithuptocubicorderinourfeatures. Figure12.4displaysthetendi(cid:27)erentrandom
splittings of the training and testing data along with the average test MSE (the black dashed
line).
Figure12.4: TestMSEcurvesformultipletraining-validationsplitsforaLinearRegressionwith
polynomial features of increasing degree
It is immediately apparent how much variation there is across di(cid:27)erent random splits into a
training and validation set. Since there is not a great deal of predictive signal in using previous
days historical close prices of the FTSE100, we see that as the degree of the polynomial features
increases the test MSE actually increases.
In addition it is clear that the validation set su(cid:27)ers from high variance. The average test
MSE for the validation set approach on the degree d=3 model is approximately 1.9.
In order to minimise this issue we will now implement k-fold cross-validation on the same
FTSE100 dataset.
12.2.6 k-Fold Cross Validation
Since we have already taken care of the imports above, I will simply outline the new functions
for carrying out k-fold cross-validation. They are almost identical to the functions used for the
training-test split. However, we need to use the KFold object to iterate over k "folds".
In particular the KFold object provides an iterator that allows us to correctly index the
samples in the data set and create separate training/test folds. I have chosen k = 10 for this
example.
Aswiththevalidationsetapproach,wecreateapipelineofpolynomialfeaturetransformation
andthenapplyalinearregressionmodel. WethencalculatethetestMSEandconstructseparate

148
test MSE curves for each fold. Finally, we create an average MSE curve across folds:
..
..
k_fold_cross_val_poly(folds,
| def |     |     |     |     |     | degrees, | X,  | y): |     |
| --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- |
"""
| Use        | the      | k-fold   | cross | validation |        | method      |        | to create |     |
| ---------- | -------- | -------- | ----- | ---------- | ------ | ----------- | ------ | --------- | --- |
| k          | separate | training |       | test       | splits | over        | linear |           |     |
| regression |          | models   |       | of varying |        | flexibility |        |           |     |
"""
| #   | Create     | the     | KFold          | object | and     |     |     |     |     |
| --- | ---------- | ------- | -------------- | ------ | ------- | --- | --- | --- | --- |
| #   | set the    | initial |                | fold   | to zero |     |     |     |     |
| n   | = len(X)   |         |                |        |         |     |     |     |     |
| kf  | = KFold(n, |         | n_folds=folds) |        |         |     |     |     |     |
kf_dict
= dict(
|     | [("fold_%s" |     | %   | i,[]) | for | i in range(1, |     | folds+1)] |     |
| --- | ----------- | --- | --- | ----- | --- | ------------- | --- | --------- | --- |
)
| fold | =            | 0                   |             |            |                    |                       |     |                  |       |
| ---- | ------------ | ------------------- | ----------- | ---------- | ------------------ | --------------------- | --- | ---------------- | ----- |
| #    | Loop         | over                | the k-folds |            |                    |                       |     |                  |       |
|      | train_index, |                     |             | test_index |                    |                       |     |                  |       |
| for  |              |                     |             |            |                    | in kf:                |     |                  |       |
|      | fold         | +=                  | 1           |            |                    |                       |     |                  |       |
|      | print("Fold: |                     |             | %s" %      | fold)              |                       |     |                  |       |
|      | X_train,     |                     | X_test      | =          | X.ix[train_index], |                       |     | X.ix[test_index] |       |
|      | y_train,     |                     | y_test      | =          | y.ix[train_index], |                       |     | y.ix[test_index] |       |
|      | # Increase   |                     | degree      |            | of linear          | regression            |     | polynomial       | order |
|      | for          | d in                | range(1,    |            | degrees+1):        |                       |     |                  |       |
|      |              | print("Degree:      |             |            | %s" %              | d)                    |     |                  |       |
|      |              | # Create            |             | the model  | and                | fit                   | it  |                  |       |
|      |              | polynomial_features |             |            |                    | = PolynomialFeatures( |     |                  |       |
include_bias=False
degree=d,
)
|     |     | linear_regression |                         |     | =   | LinearRegression() |                       |     |     |
| --- | --- | ----------------- | ----------------------- | --- | --- | ------------------ | --------------------- | --- | --- |
|     |     | model             | = Pipeline([            |     |     |                    |                       |     |     |
|     |     |                   | ("polynomial_features", |     |     |                    | polynomial_features), |     |     |
|     |     |                   | ("linear_regression",   |     |     |                    | linear_regression)    |     |     |
])
|     |     | model.fit(X_train, |     |                       | y_train) |             |        |        |     |
| --- | --- | ------------------ | --- | --------------------- | -------- | ----------- | ------ | ------ | --- |
|     |     | # Calculate        |     | the                   | test     | MSE and     | append | to the |     |
|     |     | # dictionary       |     | of                    | all      | test curves |        |        |     |
|     |     | y_pred             |     | model.predict(X_test) |          |             |        |        |     |
=
|     |     | test_mse          |     | = mean_squared_error(y_test, |     |                        |     | y_pred) |     |
| --- | --- | ----------------- | --- | ---------------------------- | --- | ---------------------- | --- | ------- | --- |
|     |     | kf_dict["fold_%s" |     |                              |     | fold].append(test_mse) |     |         |     |
%
|     | # Convert         |     | these      | lists | into      | numpy       |     |     |     |
| --- | ----------------- | --- | ---------- | ----- | --------- | ----------- | --- | --- | --- |
|     | # arrays          |     | to perform |       | averaging |             |     |     |     |
|     | kf_dict["fold_%s" |     |            |       | % fold]   | = np.array( |     |     |     |
kf_dict["fold_%s"
|     |     |     |     |     | %   | fold] |     |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
)
| #              | Create | the     | "average |                   | test MSE" | series |        | by averaging | the    |
| -------------- | ------ | ------- | -------- | ----------------- | --------- | ------ | ------ | ------------ | ------ |
| #              | test   | MSE for | each     | degree            | of        | the    | linear | regression   | model, |
| #              | across | each    | of       | the k             | folds.    |        |        |              |        |
| kf_dict["avg"] |        |         | =        | np.zeros(degrees) |           |        |        |              |        |

149
| for            | i              | in range(1, | folds+1):            |     |      |
| -------------- | -------------- | ----------- | -------------------- | --- | ---- |
|                | kf_dict["avg"] |             | += kf_dict["fold_%s" |     | % i] |
| kf_dict["avg"] |                | /=          | float(folds)         |     |      |
kf_dict
return
..
..
| We  | can plot | these curves | with the following |     | function: |
| --- | -------- | ------------ | ------------------ | --- | --------- |
..
..
plot_test_error_curves_kf(kf_dict,
| def  |            |                  |           |     | folds, degrees): |
| ---- | ---------- | ---------------- | --------- | --- | ---------------- |
| fig, | ax         | = plt.subplots() |           |     |                  |
| ds   | = range(1, | degrees+1)       |           |     |                  |
| for  | i          | in range(1,      | folds+1): |     |                  |
ax.plot(
ds,
|     |     | kf_dict["fold_%s" | %   | i], |     |
| --- | --- | ----------------- | --- | --- | --- |
lw=2,
|     |     | label=’Test | MSE - Fold | %s’ | % i |
| --- | --- | ----------- | ---------- | --- | --- |
)
ax.plot(
ds,
kf_dict["avg"],
linestyle=’--’,
color="black",
lw=3,
|     | label=’Avg | Test | MSE’ |     |     |
| --- | ---------- | ---- | ---- | --- | --- |
)
ax.legend(loc=0)
ax.set_xlabel(’Degree
|                     |     |     | of Polynomial |         | Fit’) |
| ------------------- | --- | --- | ------------- | ------- | ----- |
| ax.set_ylabel(’Mean |     |     | Squared       | Error’) |       |
| ax.set_ylim([0.0,   |     |     | 4.0])         |         |       |
fig.set_facecolor(’white’)
plt.show()
..
..
| The | output | is given | in Figure 12.5. |     |     |
| --- | ------ | -------- | --------------- | --- | --- |
Notice that the variation among the error curves is much lower than for the validation set
d = 3
approach. This is the desired e(cid:27)ect of carrying out cross-validation. In particular, at we
| have a | reduced | average | test error of around | 0.8. |     |
| ------ | ------- | ------- | -------------------- | ---- | --- |
Cross-validation generally provides a much better estimate of the true test MSE, at the ex-
penseofsomeslightbias. Thisisusuallyanacceptabletrade-o(cid:27)inmachinelearningapplications.
| 12.2.7   | Full   | Python   | Code                |     |                 |
| -------- | ------ | -------- | ------------------- | --- | --------------- |
| The full | Python | code for | cross_validation.py |     | is given below: |
# cross_validation.py
| from | __future__ | import | print_function |     |     |
| ---- | ---------- | ------ | -------------- | --- | --- |
import datetime
import pprint
| import | numpy | as np |     |     |     |
| ------ | ----- | ----- | --- | --- | --- |

150
Figure 12.5: Test MSE curves for multiple k-fold cross-validation folds for a Linear Regression
| with polynomial     | features | of increasing |            | degree |     |     |
| ------------------- | -------- | ------------- | ---------- | ------ | --- | --- |
| import pandas       | as       | pd            |            |        |     |     |
| from pandas.io.data |          | import        | DataReader |        |     |     |
| import pylab        | as       | plt           |            |        |     |     |
import sklearn
| from sklearn.cross_validation |     |     |        | import train_test_split, |     | KFold |
| ----------------------------- | --- | --- | ------ | ------------------------ | --- | ----- |
| from sklearn.linear_model     |     |     | import | LinearRegression         |     |       |
mean_squared_error
| from sklearn.metrics         |     | import |          |                    |           |          |
| ---------------------------- | --- | ------ | -------- | ------------------ | --------- | -------- |
| from sklearn.pipeline        |     | import | Pipeline |                    |           |          |
| from sklearn.preprocessing   |     |        | import   | PolynomialFeatures |           |          |
| create_lagged_series(symbol, |     |        |          | start_date,        | end_date, |          |
| def                          |     |        |          |                    |           | lags=5): |
"""
| This creates   |         | a pandas   | DataFrame | that          | stores      |     |
| -------------- | ------- | ---------- | --------- | ------------- | ----------- | --- |
| the percentage |         | returns    | of        | the adjusted  | closing     |     |
| value of       | a stock | obtained   |           | from Yahoo    | Finance,    |     |
| along with     | a       | number     | of lagged | returns       | from the    |     |
| prior trading  |         | days (lags | defaults  |               | to 5 days). |     |
| Trading        | volume, | as well    | as        | the Direction | from        |     |
| the previous   |         | day, are   | also      | included.     |             |     |
"""
| # Obtain         | stock | information |     | from Yahoo | Finance |     |
| ---------------- | ----- | ----------- | --- | ---------- | ------- | --- |
| ts = DataReader( |       |             |     |            |         |     |
symbol,
"yahoo",
start_date
- datetime.timedelta(days=365),
end_date

151
)
| #               | Create | the                          | new lagged | DataFrame    |         |     |     |     |     |
| --------------- | ------ | ---------------------------- | ---------- | ------------ | ------- | --- | --- | --- | --- |
| tslag           | =      | pd.DataFrame(index=ts.index) |            |              |         |     |     |     |     |
| tslag["Today"]  |        |                              | = ts["Adj  |              | Close"] |     |     |     |     |
| tslag["Volume"] |        |                              | =          | ts["Volume"] |         |     |     |     |     |
| #               | Create | the                          | shifted    | lag          | series  | of  |     |     |     |
| #               | prior  | trading                      | period     | close        | values  |     |     |     |     |
| for             | i in   | xrange(0,lags):              |            |              |         |     |     |     |     |
str(i+1)]
|                 | tslag["Lag%s" |                                 |                                     | %               | =          | ts["Adj | Close"].shift(i+1) |     |     |
| --------------- | ------------- | ------------------------------- | ----------------------------------- | --------------- | ---------- | ------- | ------------------ | --- | --- |
| #               | Create        | the                             | returns                             | DataFrame       |            |         |                    |     |     |
| tsret           | =             | pd.DataFrame(index=tslag.index) |                                     |                 |            |         |                    |     |     |
| tsret["Volume"] |               |                                 | =                                   | tslag["Volume"] |            |         |                    |     |     |
| tsret["Today"]  |               |                                 | = tslag["Today"].pct_change()*100.0 |                 |            |         |                    |     |     |
| #               | If any        | of                              | the values                          | of              | percentage |         |                    |     |     |
| #               | returns       | equal                           | zero,                               | set             | them       | to      |                    |     |     |
| #               | a small       | number                          | (stops                              | issues          |            | with    |                    |     |     |
| #               | QDA model     |                                 | in scikit-learn)                    |                 |            |         |                    |     |     |
| for             | i,x           | in enumerate(tsret["Today"]):   |                                     |                 |            |         |                    |     |     |
|                 | if            | (abs(x)                         | < 0.0001):                          |                 |            |         |                    |     |     |
|                 |               | tsret["Today"][i]               |                                     |                 | = 0.0001   |         |                    |     |     |
| #               | Create        | the                             | lagged                              | percentage      |            | returns | columns            |     |     |
| for             | i in          | xrange(0,lags):                 |                                     |                 |            |         |                    |     |     |
|                 | tsret["Lag%s" |                                 |                                     | % str(i+1)]     | =          | tslag[  |                    |     |     |
|                 |               | "Lag%s"                         | %                                   | str(i+1)        |            |         |                    |     |     |
].pct_change()*100.0
| #                  | Create | the | "Direction" |                           | column  |     |     |     |     |
| ------------------ | ------ | --- | ----------- | ------------------------- | ------- | --- | --- | --- | --- |
| #                  | (+1 or | -1) | indicating  | an                        | up/down | day |     |     |     |
| tsret["Direction"] |        |     |             | = np.sign(tsret["Today"]) |         |     |     |     |     |
start_date]
| tsret                                 | =   | tsret[tsret.index |     |     | >=  |          |     |        |     |
| ------------------------------------- | --- | ----------------- | --- | --- | --- | -------- | --- | ------ | --- |
| return                                |     | tsret             |     |     |     |          |     |        |     |
| def validation_set_poly(random_seeds, |     |                   |     |     |     | degrees, |     | X, y): |     |
"""
| Use      | the            | train_test_split |       |            | method     | to create   | a         |      |     |
| -------- | -------------- | ---------------- | ----- | ---------- | ---------- | ----------- | --------- | ---- | --- |
| training |                | set              | and a | validation | set        | (50%        | in each)  |      |     |
| using    | "random_seeds" |                  |       | separate   | random     |             | samplings | over |     |
| linear   |                | regression       |       | models     | of varying | flexibility |           |      |     |
"""
| sample_dict |             |     | = dict( |           |      |          |                  |     |     |
| ----------- | ----------- | --- | ------- | --------- | ---- | -------- | ---------------- | --- | --- |
|             | [("seed_%s" |     |         |           |      |          | random_seeds+1)] |     |     |
|             |             |     | %       | i,[]) for | i in | range(1, |                  |     |     |
)
| #   | Loop           | over     | each random | splitting        |        | into | a train-test |     | split |
| --- | -------------- | -------- | ----------- | ---------------- | ------ | ---- | ------------ | --- | ----- |
| for | i in           | range(1, |             | random_seeds+1): |        |      |              |     |       |
|     | print("Random: |          |             | %s" %            | i)     |      |              |     |       |
|     | # Increase     |          | degree      | of               | linear |      |              |     |       |
|     | # regression   |          | polynomial  |                  | order  |      |              |     |       |
|     | for            | d in     | range(1,    | degrees+1):      |        |      |              |     |       |

152
print("Degree: %s" % d)
# Create the model, split the sets and fit it
polynomial_features = PolynomialFeatures(
degree=d, include_bias=False
)
linear_regression = LinearRegression()
model = Pipeline([
("polynomial_features", polynomial_features),
("linear_regression", linear_regression)
])
X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.5, random_state=i
)
model.fit(X_train, y_train)
# Calculate the test MSE and append to the
# dictionary of all test curves
y_pred = model.predict(X_test)
test_mse = mean_squared_error(y_test, y_pred)
sample_dict["seed_%s" % i].append(test_mse)
# Convert these lists into numpy
# arrays to perform averaging
sample_dict["seed_%s" % i] = np.array(
sample_dict["seed_%s" % i]
)
# Create the "average test MSE" series by averaging the
# test MSE for each degree of the linear regression model,
# across all random samples
sample_dict["avg"] = np.zeros(degrees)
for i in range(1, random_seeds+1):
sample_dict["avg"] += sample_dict["seed_%s" % i]
sample_dict["avg"] /= float(random_seeds)
return sample_dict
def k_fold_cross_val_poly(folds, degrees, X, y):
"""
Use the k-fold cross validation method to create
k separate training test splits over linear
regression models of varying flexibility
"""
# Create the KFold object and
# set the initial fold to zero
n = len(X)
kf = KFold(n, n_folds=folds)
kf_dict = dict(
[("fold_%s" % i,[]) for i in range(1, folds+1)]
)
fold = 0
# Loop over the k-folds
for train_index, test_index in kf:
fold += 1

153
| print("Fold: |                     |             | %s" %     | fold)              |                       |     |                  |       |
| ------------ | ------------------- | ----------- | --------- | ------------------ | --------------------- | --- | ---------------- | ----- |
| X_train,     |                     | X_test      | =         | X.ix[train_index], |                       |     | X.ix[test_index] |       |
| y_train,     |                     | y_test      | =         | y.ix[train_index], |                       |     | y.ix[test_index] |       |
| #            | Increase            | degree      |           | of linear          | regression            |     | polynomial       | order |
| for          | d                   | in range(1, |           | degrees+1):        |                       |     |                  |       |
|              | print("Degree:      |             |           | %s" %              | d)                    |     |                  |       |
|              | #                   | Create      | the model | and                | fit it                |     |                  |       |
|              | polynomial_features |             |           |                    | = PolynomialFeatures( |     |                  |       |
include_bias=False
degree=d,
)
|     | linear_regression |                         |            | =   | LinearRegression() |                       |     |     |
| --- | ----------------- | ----------------------- | ---------- | --- | ------------------ | --------------------- | --- | --- |
|     | model             | =                       | Pipeline([ |     |                    |                       |     |     |
|     |                   | ("polynomial_features", |            |     |                    | polynomial_features), |     |     |
|     |                   | ("linear_regression",   |            |     | linear_regression) |                       |     |     |
])
|     | model.fit(X_train, |            |                       | y_train) |             |        |        |     |
| --- | ------------------ | ---------- | --------------------- | -------- | ----------- | ------ | ------ | --- |
|     | #                  | Calculate  | the                   | test     | MSE and     | append | to the |     |
|     | #                  | dictionary | of                    | all      | test curves |        |        |     |
|     | y_pred             |            | model.predict(X_test) |          |             |        |        |     |
=
|     | test_mse          |     | = mean_squared_error(y_test, |     |                        |     | y_pred) |     |
| --- | ----------------- | --- | ---------------------------- | --- | ---------------------- | --- | ------- | --- |
|     | kf_dict["fold_%s" |     |                              |     | fold].append(test_mse) |     |         |     |
%
| #                 | Convert | these | lists   | into      | numpy       |     |     |     |
| ----------------- | ------- | ----- | ------- | --------- | ----------- | --- | --- | --- |
| #                 | arrays  | to    | perform | averaging |             |     |     |     |
| kf_dict["fold_%s" |         |       |         | % fold]   | = np.array( |     |     |     |
kf_dict["fold_%s"
|     |     |     |     | %   | fold] |     |     |     |
| --- | --- | --- | --- | --- | ----- | --- | --- | --- |
)
| # Create | the  | "average |        | test MSE" | series     | by  | averaging  | the    |
| -------- | ---- | -------- | ------ | --------- | ---------- | --- | ---------- | ------ |
| # test   | MSE  | for each | degree | of        | the linear |     | regression | model, |
| # across | each | of       | the k  | folds.    |            |     |            |        |
kf_dict["avg"]
|                |             | =   | np.zeros(degrees) |                   |     |     |     |     |
| -------------- | ----------- | --- | ----------------- | ----------------- | --- | --- | --- | --- |
| for i          | in range(1, |     | folds+1):         |                   |     |     |     |     |
| kf_dict["avg"] |             |     |                   | kf_dict["fold_%s" |     |     |     |     |
|                |             |     | +=                |                   |     | %   | i]  |     |
| kf_dict["avg"] |             | /=  | float(folds)      |                   |     |     |     |     |
return kf_dict
| plot_test_error_curves_vs(sample_dict, |          |                |     |     |     | random_seeds, |     |           |
| -------------------------------------- | -------- | -------------- | --- | --- | --- | ------------- | --- | --------- |
| def                                    |          |                |     |     |     |               |     | degrees): |
| fig,                                   | ax =     | plt.subplots() |     |     |     |               |     |           |
| ds =                                   | range(1, | degrees+1)     |     |     |     |               |     |           |
random_seeds+1):
| for i | in range(1, |     |     |     |     |     |     |     |
| ----- | ----------- | --- | --- | --- | --- | --- | --- | --- |
ax.plot(
ds,
|     | sample_dict["seed_%s" |     |     |     | % i], |     |     |     |
| --- | --------------------- | --- | --- | --- | ----- | --- | --- | --- |
lw=2,
|     | label=’Test |     | MSE | - Sample | %s’ | % i |     |     |
| --- | ----------- | --- | --- | -------- | --- | --- | --- | --- |
)
ax.plot(
ds,
sample_dict["avg"],
linestyle=’--’,

154
color="black",
lw=3,
| label=’Avg |     | Test | MSE’ |     |     |
| ---------- | --- | ---- | ---- | --- | --- |
)
ax.legend(loc=0)
ax.set_xlabel(’Degree
|                     |     |     | of Polynomial |         | Fit’) |
| ------------------- | --- | --- | ------------- | ------- | ----- |
| ax.set_ylabel(’Mean |     |     | Squared       | Error’) |       |
| ax.set_ylim([0.0,   |     |     | 4.0])         |         |       |
fig.set_facecolor(’white’)
plt.show()
| def plot_test_error_curves_kf(kf_dict, |                     |            |           |     | folds, degrees): |
| -------------------------------------- | ------------------- | ---------- | --------- | --- | ---------------- |
| fig,                                   | ax = plt.subplots() |            |           |     |                  |
| ds =                                   | range(1,            | degrees+1) |           |     |                  |
| for i                                  | in range(1,         |            | folds+1): |     |                  |
ax.plot(
ds,
kf_dict["fold_%s"
|     |     |     |     | % i], |     |
| --- | --- | --- | --- | ----- | --- |
lw=2,
|     | label=’Test |     | MSE - | Fold %s’ | % i |
| --- | ----------- | --- | ----- | -------- | --- |
)
ax.plot(
ds,
kf_dict["avg"],
linestyle=’--’,
color="black",
lw=3,
| label=’Avg |     | Test | MSE’ |     |     |
| ---------- | --- | ---- | ---- | --- | --- |
)
ax.legend(loc=0)
| ax.set_xlabel(’Degree |     |     | of Polynomial |     | Fit’) |
| --------------------- | --- | --- | ------------- | --- | ----- |
ax.set_ylabel(’Mean
|     |     |     | Squared | Error’) |     |
| --- | --- | --- | ------- | ------- | --- |
ax.set_ylim([0.0,
4.0])
fig.set_facecolor(’white’)
plt.show()
| __name__ |           | "__main__": |     |     |     |
| -------- | --------- | ----------- | --- | --- | --- |
| if       | ==        |             |     |     |     |
| symbol   | = "^FTSE" |             |     |     |     |
start_date
|           |     | = datetime.datetime(2004, |           |     | 1, 1)   |
| --------- | --- | ------------------------- | --------- | --- | ------- |
| end_date  | =   | datetime.datetime(2004,   |           |     | 12, 31) |
| ftse_lags | =   | create_lagged_series(     |           |     |         |
|           |     | start_date,               | end_date, |     |         |
| symbol,   |     |                           |           |     | lags=5  |
)
| # Use         | five | prior    | days of returns |              | as predictor |
| ------------- | ---- | -------- | --------------- | ------------ | ------------ |
| # values,     | with | "Today"  | as              | the response |              |
| # (Further    |      | days are | commented,      | but          | can be       |
| # uncommented |      | to       | allow extra     | predictors)  |              |
ftse_lags[[
X =
| "Lag1",   |     | "Lag2",  | "Lag3",  | "Lag4", | "Lag5",           |
| --------- | --- | -------- | -------- | ------- | ----------------- |
| #"Lag6",  |     | "Lag7",  | "Lag8",  | "Lag9", | "Lag10",          |
| #"Lag11", |     | "Lag12", | "Lag13", |         | "Lag14", "Lag15", |
| #"Lag16", |     | "Lag17", | "Lag18", |         | "Lag19", "Lag20"  |

155
]]
y = ftse_lags["Today"]
| degrees    | = 3        |        |                |     |
| ---------- | ---------- | ------ | -------------- | --- |
| # Plot the | test error | curves | for validation | set |
random_seeds
= 10
| sample_dict_val | = validation_set_poly( |     |      |     |
| --------------- | ---------------------- | --- | ---- | --- |
| random_seeds,   | degrees,               |     | X, y |     |
)
plot_test_error_curves_vs(
| sample_dict_val, |     | random_seeds, |     |     |
| ---------------- | --- | ------------- | --- | --- |
degrees
)
| # Plot the | test error               | curves | for k-fold | CV set |
| ---------- | ------------------------ | ------ | ---------- | ------ |
| folds =    | 10                       |        |            |        |
| kf_dict    | = k_fold_cross_val_poly( |        |            |        |
| folds,     | degrees,                 | X, y   |            |        |
)
plot_test_error_curves_kf(
| kf_dict, | folds, | degrees |     |     |
| -------- | ------ | ------- | --- | --- |
)

156

Chapter 13
Kernel Methods and SVMs
13.1 Support Vector Machines
In this section we are going to discuss an extremely powerful machine learning technique known
as the Support Vector Machine (SVM). It is one of the best "out of the box" supervised
classi(cid:28)cationtechniques. Itisanimportanttoolforboththequantitativetradingresearcherand
data scientist.
This section will cover the theory of maximal margin classi(cid:28)ers, support vector clas-
si(cid:28)ers and support vector machines. We will be making use of Scikit-Learn to demonstrate
some examples of the aforementioned theoretical techniques on actual data.
13.1.1 Motivation for Support Vector Machines
The problem to be solved in this section is one of supervised binary classi(cid:28)cation. That
is, we wish to categorise new unseen objects into two separate groups based on their properties
and a set of known examples that are already categorised. A good example of such a system
is classifying a set of new documents into positive or negative sentiment groups, based on other
documentswhichhavealreadybeenclassi(cid:28)edaspositiveornegative. Similarly,wecouldclassify
newemailsintospamornon-spam,basedonalargecorpusofdocumentsthathavealreadybeen
marked as spam or non-spam by humans. SVMs are highly applicable to such situations.
ASupportVectorMachinemodelsthesituationbycreatingafeature space, whichisa(cid:28)nite-
dimensional vector space, each dimension of which represents a "feature" of a particular object.
Inthecontextofspamordocumentclassi(cid:28)cation,each"feature"istheprevalenceorimportance
of a particular word.
The goal of the SVM is to train a model that assigns new unseen objects into a particular
category. It achieves this by creating a linear partition of the feature space into two subspaces.
Based on the features in the new unseen objects (e.g. documents/emails), it places an object
"above" or "below" the separation plane, leading to a categorisation (e.g. spam or non-spam).
This makes it an example of a non-probabilistic linear classi(cid:28)er. It is non-probabilistic because
the features in the new objects fully determine its location in feature space and there is no
stochastic element involved.
However, much of the bene(cid:28)t of SVMs comes from the fact that they are not restricted to
being linear classi(cid:28)ers. Utilising a technique known as the kernel trick they can become much
more (cid:29)exible by introducing various types of non-linear decision boundaries.
Formally, in mathematical language, SVMs construct linear separating hyperplanes in large
(cid:28)nite-dimensional vector spaces. Data points are viewed as ((cid:126)x,y) tuples, (cid:126)x=(x ,...,x ) where
1 p
the x are the feature values and y is the classi(cid:28)cation (usually given as +1 or −1). Optimal
j
classi(cid:28)cation occurs when such hyperplanes provide maximal distance to the nearest training
data points. Intuitively, this makes sense, as if the points are well separated, the classi(cid:28)cation
between two groups is much clearer.
However, if in a feature space some of the sets are not linearly separable (i.e. they over-
lap!), then it is necessary to perform a transformation of the original feature space to a higher-
157

158
dimensional space, in which the separation between the groups is clear, or at least clearer.
However, this has the consequence of making the separation boundary in the original space
potentially non-linear.
In this section we will proceed by considering the advantages and disadvantages of SVMs as
a classi(cid:28)cation technique. We will then de(cid:28)ne the concept of an optimal linear separating
hyperplane, whichmotivatesasimpletypeoflinearclassi(cid:28)erknownasamaximal margin clas-
si(cid:28)er (MMC).Subsequentlywewillshowthatmaximalmarginclassi(cid:28)ersarenotoftenapplicable
to many "real world" situations and need modi(cid:28)cation in the form of a support vector classi(cid:28)er
(SVC). We will then relax the restriction of linearity and consider non-linear classi(cid:28)ers, namely
support vector machines, which use kernel functions to improve computational e(cid:30)ciency.
13.1.2 Advantages and Disadvantages of SVMs
As a classi(cid:28)cation technique the SVM has many advantages, some of which are due to its com-
putational e(cid:30)ciency on large datasets. The Scikit-Learn team have summarised the main ad-
vantages and disadvantages[4] but I have repeated and elaborated on them for completeness:
Advantages
(cid:136)
High-Dimensionality - The SVM is an e(cid:27)ective tool in high-dimensional spaces, which
is particularly applicable to document classi(cid:28)cation and sentiment analysis where the di-
mensionality can be extremely large (≥106).
(cid:136)
Memory E(cid:30)ciency - Since only a subset of the training points are used in the actual
decision process of assigning new members, only these points need to be stored in memory
(and calculated upon) when making decisions.
(cid:136)
Versatility - Class separation is often highly non-linear. The ability to apply new kernels
allows substantial (cid:29)exibility for the decision boundaries, leading to greater classi(cid:28)cation
performance.
Disadvantages
(cid:136) p>n-Insituationswherethenumberoffeaturesforeachobject(p)exceedsthenumberof
trainingdatasamples(n),SVMscanperformpoorly. Thiscanbeseenintuitively,asifthe
high-dimensional feature space is much larger than the number of samples, then there are
less e(cid:27)ective support vectors on which to support the optimal linear hyperplanes, leading
to poorer classi(cid:28)cation performance as new unseen samples are added.
(cid:136)
Non-Probabilistic - Since the classi(cid:28)er works by placing objects above and below a
classifyinghyperplane,thereisnodirectprobabilisticinterpretationforgroupmembership.
However, one potential metric to determine "e(cid:27)ectiveness" of the classi(cid:28)cation is how far
from the decision boundary the new point is.
Now that we’ve outlined the advantages and disadvantages we’re going to discuss the geo-
metric objects and mathematical entities that will ultimately allow us to de(cid:28)ne the SVMs and
how they work.
Therearesomefantasticreferences(bothlinksandtextbooks)thatderivemuchofthemath-
ematical detail of how SVMs function. In the following derivation I didn’t want to "reinvent the
wheel"toomuch,especiallywithregardsnotationandpedagogy,soI’veformulatedthefollowing
treatmentbasedonthereferencesprovided,makingstronguseofJamesetal[32],Hastieetal[27]
and the Wikibooks article on SVMs[5]. As this is a textbook on trading strategies, I have made
changes to the notation where appropriate and have adjusted the narrative to suit individuals
interested in quantitative trading.

159
| 13.1.3 | Linear | Separating | Hyperplanes |     |     |     |     |
| ------ | ------ | ---------- | ----------- | --- | --- | --- | --- |
The linear separating hyperplane is the key geometric entity that is at the heart of the SVM.
Informally, if we have a high-dimensional feature space, then the linear hyperplane is an object
one dimension lower than this space that divides the feature space into two regions.
Thislinearseparatingplaneneednotpassthroughtheoriginofourfeaturespace,i.e. itdoes
not need to include the zero vector as an entity within the plane. Such hyperplanes are known
as a(cid:30)ne.
|     |     |     | p-dimensional |     |     |     | Rp, |
| --- | --- | --- | ------------- | --- | --- | --- | --- |
If we consider a real-valued feature space, known mathematically as then
our linear separating hyperplane is an a(cid:30)ne p−1 dimensional space embedded within it.
For the case of p = 2 this hyperplane is simply a one-dimensional straight line, which lives
in the larger two-dimensional plane, whereas for p=3 the hyerplane is a two-dimensional plane
| that lives | in the | larger three-dimensional |            | feature             | space (see | Figure 13.1): |     |
| ---------- | ------ | ------------------------ | ---------- | ------------------- | ---------- | ------------- | --- |
|            |        | Figure                   | 13.1: One- | and two-dimensional |            | hyperplanes   |     |
)∈Rp,
If we consider an element of our p-dimensional feature space, i.e. (cid:126)x=(x ,...,x then
1 p
we can mathematically de(cid:28)ne an a(cid:30)ne hyperplane by the following equation:
|     |     |     | b 0 +b | 1 x 1 +...+b | p x p =0 |     | (13.1) |
| --- | --- | --- | ------ | ------------ | -------- | --- | ------ |
b 0 (cid:54)=0 gives us an a(cid:30)ne plane (i.e. it does not pass through the origin). We can use a more
| succinct | notation | for this equation | by  | introducing | the summation | sign: |     |
| -------- | -------- | ----------------- | --- | ----------- | ------------- | ----- | --- |
p
(cid:88)
|     |     |     |     | b + b | x =0 |     | (13.2) |
| --- | --- | --- | --- | ----- | ---- | --- | ------ |
|     |     |     |     | 0     | j j  |     |        |
j=1
Notice however that this is nothing more than a multi-dimensional dot product (or, more
generally, an inner product), and as such can be written even more succinctly as:
(cid:126)b·(cid:126)x+b
|     |     |     |     |     | =0  |     | (13.3) |
| --- | --- | --- | --- | --- | --- | --- | ------ |
0
If an element (cid:126)x∈Rp satis(cid:28)es this relation then it lives on the p−1-dimensional hyperplane.
p-dimensional
This hyperplane splits the feature space into two classi(cid:28)cation regions (see Figure
13.2):
| Elements | (cid:126)x above | the plane | satisfy: |     |     |     |     |
| -------- | ---------------- | --------- | -------- | --- | --- | --- | --- |
(cid:126)b·(cid:126)x+b
|       |       |                   |     |     | 0 >0 |     | (13.4) |
| ----- | ----- | ----------------- | --- | --- | ---- | --- | ------ |
| While | those | below it satisfy: |     |     |      |     |        |

160
|     |     | Figure | 13.2: | Separation | of p-dimensional        |     | space by a | hyperplane |        |
| --- | --- | ------ | ----- | ---------- | ----------------------- | --- | ---------- | ---------- | ------ |
|     |     |        |       |            | (cid:126)b·(cid:126)x+b | <0  |            |            | (13.5) |
0
Thekeypointhereisthatitispossibleforustodeterminewhichsideoftheplaneanyelement
(cid:126)x will fall on by calculating the sign (i.e. whether it is positive or negative) of the expression
(cid:126)b·(cid:126)x+b
|     | . This | concept | will form | the | basis of | a supervised | classi(cid:28)cation | technique. |     |
| --- | ------ | ------- | --------- | --- | -------- | ------------ | -------------------- | ---------- | --- |
0
| 13.1.4 | Classi(cid:28)cation |     |     |     |     |     |     |     |     |
| ------ | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Continuing with our example of email spam (cid:28)ltering, we can think of our classi(cid:28)cation problem
(say) as being provided with a thousand emails (n=1000), each of which is marked spam (+1)
ornon-spam(−1). Inaddition, eachemailhasanassociatedsetofkeywords(i.e. separatingthe
words on spacing) that provide features. Hence if we take the set of all possible keywords from
p
all of the emails (and remove duplicates), we will be left with keywords in total.
Ifwetranslatethisintoamathematicalproblem,thestandardsetupforasupervisedclassi(cid:28)-
cationprocedureistoconsiderasetofntrainingobservations,(cid:126)x ,eachofwhichisap-dimensional
i
vector of features. Each training observation has an associated class label, y i ∈ {−1,1}. Hence
we can think of n pairs of training observations ((cid:126)x ,y ) representing the features and class labels
i i
(keywordlistsandspam/non-spam). Inadditiontothetrainingobservationswecanprovidetest
observations, (cid:126)x∗ = (x∗,...,x∗) that are later used to test the performance of the classi(cid:28)ers. In
|     |     |     | 1 p |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
our spam example, these test observations would be new emails that have not yet been seen.
Our goal is to develop a classi(cid:28)er based on provided training observations that will correctly
classify subsequent test observations using only their feature values. This translates into being
able to classify an email as spam or non-spam solely based on the keywords contained within it.
We will initially suppose that it is possible, via a means yet to be determined, to construct
a hyperplane that separates training data perfectly according to their class labels (see Figure
13.3). This would mean cleanly separating spam emails from non-spam emails solely by using
speci(cid:28)c keywords. The following diagram is only showing p=2, while for keyword lists we may
p>106.
| have |            | Hence | Figures        | 13.3 are              | only representative |          | of the problem. |     |        |
| ---- | ---------- | ----- | -------------- | --------------------- | ------------------- | -------- | --------------- | --- | ------ |
| This | translates | into  | a mathematical |                       | separating          | property | of:             |     |        |
|      |            |       |                | (cid:126)b·(cid:126)x | +b >0,              | if y     | =1              |     | (13.6) |
|      |            |       |                |                       | i 0                 | i        |                 |     |        |
and

161
Figure 13.3: Multiple separating hyperplanes; Perfect separation of class data
(cid:126)b·(cid:126)x +b <0, if y =−1 (13.7)
i 0 i
This basically states that if each training observation is above or below the separating hy-
perplane, according to the geometric equation which de(cid:28)nes the plane, then its associated class
label will be +1 or −1. Thus we have developed a simple classi(cid:28)cation process. We assign a test
observation to a class depending upon which side of the hyperplane it is located on.
This can be formalised by considering the following function f((cid:126)x), with a test observation
(cid:126)x∗ =(x∗,...,x∗):
1 p
f((cid:126)x∗)=(cid:126)b·(cid:126)x∗+b
(13.8)
0
If f((cid:126)x∗)>0 then y∗ =+1, whereas if f((cid:126)x∗)<0 then y∗ =−1.
However, this tells us nothing about how we go about (cid:28)nding the b components of (cid:126)b, as well
j
as b , which are crucial in helping us determine the equation of the hyperplane separating the
0
two regions. The next section discusses an approach for carrying this out, as well as introducing
the concept of the maximal margin hyperplane and a classi(cid:28)er built on it, known as the
maximal margin classi(cid:28)er.
13.1.5 Deriving the Classi(cid:28)er
At this stage it is worth pointing out that separating hyperplanes are not unique since it is
possible to slightly translate or rotate such a plane without touching any training observations
(see Figures 13.3).
So,notonlydoweneedtoknowhow toconstructsuchaplane,butwealsoneedtodetermine
the most optimal plane. This motivates the concept of the maximal margin hyperplane
(MMH), which is the separating hyperplane that is farthest from any training observations and
is thus "optimal".
How do we (cid:28)nd the maximal margin hyperplane? Firstly, we compute the perpendicular
distance from each training observation (cid:126)x for a given separating hyperplane. The smallest
i
perpendicular distance to a training observation from the hyperplane is known as the margin.
The MMH is the separating hyperplane where the margin is the largest. This guarantees that it
is the farthest minimum distance to a training observation.
The classi(cid:28)cation procedure is then just simply a case of determining which side a test ob-
servation falls on. This can be carried out using the above formula for f((cid:126)x∗). Such a classi(cid:28)er is
known as a maximimal margin classi(cid:28)er (MMC). Note however that (cid:28)nding the particular
values that lead to the MMH is purely based on the training observations. That is, we still need
to be aware of how the MMC performs on the test observations. We are implicitly making the

162
assumption that a large margin in the training observations will provide a large margin on the
test observations, but this may not be the case.
As always, we must be careful to avoid over(cid:28)tting when the number of feature dimensions
is large (e.g. in Natural Language Processing applications such as email spam classi(cid:28)cation).
Over(cid:28)tting here means that the MMH is a very good (cid:28)t for the training data but can perform
quitepoorlywhenexposedtotestingdata. Idiscussedthisissueindepthinthepreviouschapter,
under the Bias-Variance Tradeo(cid:27) section.
To reiterate, our goal now becomes (cid:28)nding an algorithm that can produce the b values,
j
which will (cid:28)x the geometry of the hyperplane and hence allow determination of f((cid:126)x∗) for any
test observation.
If we consider Figure 13.4, we can see that the MMH is the mid-line of the widest "block"
that we can insert between the two classes such that they are perfectly separated.
Figure 13.4: Maximal margin hyperplane with support vectors (A, B and C)
One of the key features of the MMC (and subsequently SVC and SVM) is that the location
of the MMH only depends on the support vectors, which are the training observations that
lie directly on the margin (but not hyperplane) boundary (see points A, B and C in Figure
13.4). This means that the location of the MMH is NOT dependent upon any other training
observations.
ThusitcanbeimmediatelyseenthatapotentialdrawbackoftheMMCisthatitsMMH(and
thus its classi(cid:28)cation performance) can be extremely sensitive to the support vector locations.
However, it is also partially this feature that makes the SVM an attractive computational tool,
as we only need to store the support vectors in memory once it has been "trained" (i.e. the b
j
values are (cid:28)xed).
13.1.6 Constructing the Maximal Margin Classi(cid:28)er
I feel it is instructive to fully outline the optimisation problem that needs to be solved in order
to create the MMH (and thus the MMC itself). While I will outline the constraints of the
optimisation problem, the algorithmic solution to this problem is beyond the scope of the book.
Thankfullytheseoptimisationroutinesareimplementedinscikit-learn(actually,viatheLIBSVM
library[16]). If you wish to read more about the solution to these algorithmic problems, take a
look at Hastie et al (2009)[27] and the Scikit-Learn page on Support Vector Machines[4].
Theprocedurefordeterminingamaximalmarginhyperplaneforamaximalmarginclassi(cid:28)er
isasfollows. Givenntrainingobservations(cid:126)x ,...,(cid:126)x ∈Rp andnclasslabelsy ,...,y ∈{−1,1},
1 n 1 n
the MMH is the solution to the following optimisation procedure:
Maximise M ∈R, by varying b ,...,b such that:
1 p

163
p
(cid:88) b2
|     |     |     | =1  |     | (13.9) |
| --- | --- | --- | --- | --- | ------ |
j
j=1
and
|     |     | (cid:16)                  | (cid:17)       |     |         |
| --- | --- | ------------------------- | -------------- | --- | ------- |
|     |     | y (cid:126)b·(cid:126)x+b | ≥M, ∀i=1,...,n |     | (13.10) |
|     |     | i                         | 0              |     |         |
Despite the complex looking constraints, they actually state that each observation must be
on the correct side of the hyperplane and at least a distance M from it. Since the goal of the
procedure is to maximise M, this is precisely the condition we need to create the MMC!
Clearly, the case of perfect separability is an ideal one. Most "real world" datasets will not
have such perfect separability via a linear hyperplane (see Figure 13.5). However, if there is no
separability then we are unable to construct a MMC by the optimisation procedure above. So,
| how do we | create a form | of separating | hyperplane?                      |            |     |
| --------- | ------------- | ------------- | -------------------------------- | ---------- | --- |
|           | Figure        | 13.5: No      | possibility of a true separating | hyperplane |     |
Essentially we have to relax the requirement that a separating hyperplane will perfectly
separate every training observation on the correct side of the line (i.e. guarantee that it is
associated with its true class label), using what is called a soft margin. This motivates the
| concept | of a support vector | classi(cid:28)er         | (SVC). |     |     |
| ------- | ------------------- | ------------------------ | ------ | --- | --- |
| 13.1.7  | Support             | Vector Classi(cid:28)ers |        |     |     |
As we alluded to above, one of the problems with MMC is that they can be extremely sensitive
to the addition of new training observations. Consider Figure 13.6. In the left panel it can be
seen that there exists a MMH perfectly separating the two classes. However, in the right panel
if we add one point to the +1 class we see that the location of the MMH changes substantially.
| Hence in | this situation | the MMH has | clearly been over-(cid:28)t: |     |     |
| -------- | -------------- | ----------- | ---------------------------- | --- | --- |
As we mentioned above also, we could consider a classi(cid:28)er based on a separating hyperplane
thatdoesn’tperfectlyseparatethetwoclasses,butdoeshaveagreaterrobustnesstotheaddition
ofnew invididualobservationsandhasabetterclassi(cid:28)cationonmost ofthetrainingobservations.
This comes at the expense of some misclassi(cid:28)cation of a few training observations.
This is how a support vector classi(cid:28)er or soft margin classi(cid:28)er works. A SVC allows some
observationstobeontheincorrectsideofthemargin(orhyperplane), henceitprovidesa"soft"
separation. Figure13.7demonstrateobservationsbeingonthewrongsideofthemarginandthe
| wrong side | of the hyperplane | respectively: |     |     |     |
| ---------- | ----------------- | ------------- | --- | --- | --- |

164
Figure 13.6: Addition of a single point dramatically changes the MMH line
Figure 13.7: Observations on the wrong side of the margin and hyperplane, respectively
Asbefore,anobservationisclassi(cid:28)eddependinguponwhichsideoftheseparatinghyperplane
| it lies on, | but some points | may be | misclassi(cid:28)ed. |     |     |
| ----------- | --------------- | ------ | -------------------- | --- | --- |
It is instructive to see how the optimisation procedure di(cid:27)ers from that described above for
theMMC.Weneedtointroducenewparameters,namelyn(cid:15)
|     |     |     |     | i values(knownastheslack | values) |
| --- | --- | --- | --- | ------------------------ | ------- |
andaparameterC, knownasthebudget. WewishtomaximiseM, acrossb ,...,b ,(cid:15) ,..,(cid:15) such
1 p 1 n
that:
p
(cid:88)
b2
|     |     |     | j =1 |     | (13.11) |
| --- | --- | --- | ---- | --- | ------- |
j=1
and
|     |     | (cid:16)                  | (cid:17)      |               |         |
| --- | --- | ------------------------- | ------------- | ------------- | ------- |
|     |     | y (cid:126)b·(cid:126)x+b | ≥M(1−(cid:15) | ), ∀i=1,...,n | (13.12) |
|     |     | i                         | 0 i           |               |         |
and
(cid:88) n
|     |     |     | (cid:15) i ≥0, (cid:15) i | ≤C  | (13.13) |
| --- | --- | --- | ------------------------- | --- | ------- |
i=1
Where C, the budget, is a non-negative "tuning" parameter. M still represents the margin
andtheslackvariables(cid:15) allowtheindividualobservationstobeonthewrongsideofthemargin
i
or hyperplane.

165
|     | (cid:15) | ith |     |     |     |
| --- | -------- | --- | --- | --- | --- |
In essence the i tell us where the observation is located relative to the margin and
hyperplane. For (cid:15) = 0 it states that the x training observation is on the correct side of the
|     | i   | i   |     |     |     |
| --- | --- | --- | --- | --- | --- |
margin. For (cid:15) >0 we have that x is on the wrong side of the margin, while for (cid:15) >1 we have
|             | i            | i                       |     |     | i   |
| ----------- | ------------ | ----------------------- | --- | --- | --- |
| that x i is | on the wrong | side of the hyperplane. |     |     |     |
C collectively controls how much the individual (cid:15) can be modi(cid:28)ed to violate the margin.
i
| C = 0 | (cid:15) = | 0,∀i |     |     |     |
| ----- | ---------- | ---- | --- | --- | --- |
implies that i and thus no violation of the margin is possible, in which case (for
| separable | classes) we have | the MMC situation. |     |     |     |
| --------- | ---------------- | ------------------ | --- | --- | --- |
For C > 0 it means that no more than C observations can violate the hyperplane. As C
increases the margin will widen. See Figure 13.8 for two di(cid:27)ering values of C:
|     | Figure | 13.8: Di(cid:27)erent values | of the tuning | parameter C |     |
| --- | ------ | ---------------------------- | ------------- | ----------- | --- |
How do we choose C in practice? Generally this is done via cross-validation. In essence C is
the parameter that governs the bias-variance trade-o(cid:27) for the SVC. A small value of C means a
low bias, high variance situation. A large value of C means a high bias, low variance situation.
As before, to classify a new test observation x∗ we simply calculate the sign of f((cid:126)x∗) =
(cid:126)b·(cid:126)x∗+b
.
0
This is all well and good for classes that are linearly (or nearly linearly) separated. However,
what about separation boundaries that are non-linear? How do we deal with those situations?
Thisiswherewecanextendtheconceptofsupportvectorclassi(cid:28)erstosupportvectormachines.
| 13.1.8 | Support Vector | Machines |     |     |     |
| ------ | -------------- | -------- | --- | --- | --- |
ThemotivationbehindtheextensionofaSVCistoallownon-lineardecisionboundaries. Thisis
the domain of the Support Vector Machine (SVM). Consider the following Figure 13.9. In such
a situation a purely linear SVC will have extremely poor performance, simply because the data
| has no clear | linear separation:  |                      |                |           |     |
| ------------ | ------------------- | -------------------- | -------------- | --------- | --- |
| Hence        | SVCs can be useless | in highly non-linear | class boundary | problems. |     |
In order to motivate how an SVM works, we can consider a standard "trick" in linear re-
gression, when considering non-linear situations. In particular a set of p features x ,...,x can
1 p
,x2,...,x ,x2.
be transformed, say, into a set of 2p features x 1 p This allows us to apply a linear
|           |                        |           | 1   | p   |     |
| --------- | ---------------------- | --------- | --- | --- | --- |
| technique | to a set of non-linear | features. |     |     |     |
Whilethedecisionboundaryislinearinthenew2p-dimensionalfeaturespaceitisnon-linear
intheoriginalp-dimensionalspace. Weendupwithadecisionboundarygivenbyq((cid:126)x)=0where
q is a quadratic polynomial function of the original features and hence is a non-linear solution.
This is clearly not restricted to quadratic polynomials. Higher dimensional polynomials,
interaction terms and other functional forms, could all be considered. Although the drawback is
thatitdramaticallyincreasesthedimensionofthefeaturespacetothepointthatsomealgorithms
| can become | untractable. |     |     |     |     |
| ---------- | ------------ | --- | --- | --- | --- |
ThemajoradvantageofSVMsisthattheyallowanon-linearenlargeningofthefeaturespace,
while still retaining a signi(cid:28)cant computational e(cid:30)ciency, using a process known as the "kernel

166
Figure 13.9: No clear linear separation between classes and thus poor SVC performance
| trick", which |     | will be outlined |     | below | shortly. |     |     |     |
| ------------- | --- | ---------------- | --- | ----- | -------- | --- | --- | --- |
So what are SVMs? In essence they are an extension of SVCs that results from enlargening
thefeaturespacethroughtheuseoffunctionsknownaskernels. Inordertounderstandkernels,
weneedtobrie(cid:29)ydiscusssomeaspectsofthesolutiontotheSVCoptimisationproblemoutlined
above.
While calculating the solution to the SVC optimisation problem, the algorithm only needs
to make use of inner products between the observations and not the observations themselves.
Recall that an inner product is de(cid:28)ned for two p-dimensional vectors u,v as:
p
(cid:88)
|     |     |     |     |     | (cid:104)(cid:126)u,(cid:126)v(cid:105)= | u   | v   | (13.14) |
| --- | --- | --- | --- | --- | ---------------------------------------- | --- | --- | ------- |
j j
j=1
| Hence | for | two observations |     | an inner | product | is de(cid:28)ned | as: |     |
| ----- | --- | ---------------- | --- | -------- | ------- | ---------------- | --- | --- |
p
(cid:88)
|     |     |     |     |     | (cid:104)(cid:126)x i ,(cid:126)x k (cid:105)= | x ij | x kj | (13.15) |
| --- | --- | --- | --- | --- | ---------------------------------------------- | ---- | ---- | ------- |
j=1
While we won’t dwell on the details (since they are beyond the scope of this book), it is
possible to show that a linear support vector classi(cid:28)er for a particular observation (cid:126)x can be
| represented | as  | a linear | combination |     | of inner | products: |     |     |
| ----------- | --- | -------- | ----------- | --- | -------- | --------- | --- | --- |
n
(cid:88)
|     |     |     |     | f((cid:126)x)=b | +   | α   | (cid:104)(cid:126)x,(cid:126)x (cid:105) |         |
| --- | --- | --- | --- | --------------- | --- | --- | ---------------------------------------- | ------- |
|     |     |     |     |                 | 0   | i   | i                                        | (13.16) |
i=1
| With | n a | coe(cid:30)cients, | one | for each | of the | training | observations. |     |
| ---- | --- | ------------------ | --- | -------- | ------ | -------- | ------------- | --- |
i
(cid:0)n(cid:1)
To estimate the b 0 and a i coe(cid:30)cients we only need to calculate = n(n − 1)/2 inner
2
products between all pairs of training observations. In fact, we ONLY need to calculate the
inner products for the subset of training observations that represent the support vectors. I will
S.
| call this | subset | This        | means | that:          |      |                  |     |         |
| --------- | ------ | ----------- | ----- | -------------- | ---- | ---------------- | --- | ------- |
|           |        |             |       |                | a =0 | if (cid:126)x ∈/ | S   | (13.17) |
|           |        |             |       |                | i    | i                |     |         |
| Hence     | we     | can rewrite | the   | representation |      | formula          | as: |         |
(cid:88)
|     |     |     |     | f(x)=b | +   | a   | (cid:104)(cid:126)x,(cid:126)x (cid:105) | (13.18) |
| --- | --- | --- | --- | ------ | --- | --- | ---------------------------------------- | ------- |
|     |     |     |     |        | 0   | i   | i                                        |         |
i∈S

167
| This | turns | out to | be a | major advantage |     | for computational |     | e(cid:30)ciency. |     |     |
| ---- | ----- | ------ | ---- | --------------- | --- | ----------------- | --- | ---------------- | --- | --- |
This now motivates the extension to SVMs. If we consider the inner product (cid:104)(cid:126)x ,(cid:126)x (cid:105) and
i k
|     |     |     |     |     |     |     |     | K   | = K((cid:126)x ,(cid:126)x ), |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------------------------- | --- |
replace it with a more general inner product "kernel" function i k we can modify
the SVC representation to use non-linear kernel functions and thus modify how we calculate
"similarity" betweentwoobservations. For instance, torecoverthe SVCwejust take K to be as
follows:
p
(cid:88)
|     |     |     |     |     | K((cid:126)x ,(cid:126)x | )= x | x     |     |     | (13.19) |
| --- | --- | --- | --- | --- | ------------------------ | ---- | ----- | --- | --- | ------- |
|     |     |     |     |     | i k                      |      | ij kj |     |     |         |
j=1
Since this kernel is linear in its features the SVC is known as the linear SVC. We can also
| consider | polynomial |     | kernels, | of degree | d:  |     |     |     |     |     |
| -------- | ---------- | --- | -------- | --------- | --- | --- | --- | --- | --- | --- |
p
(cid:88)
|     |     |     |     | K((cid:126)x | ,(cid:126)x )=(1+ |     | x x   | )d  |     | (13.20) |
| --- | --- | --- | --- | ------------ | ----------------- | --- | ----- | --- | --- | ------- |
|     |     |     |     |              | i k               |     | ij kj |     |     |         |
j=1
Thisprovidesasigni(cid:28)cantlymore(cid:29)exibledecisionboundaryandessentiallyamountsto(cid:28)tting
a SVC in a higher-dimensional feature space involving d-degree polynomials of the features (see
Figure 13.10).
|     |     | Figure | 13.10: | A   | d-degree | polynomial | kernel; | A radial | kernel |     |
| --- | --- | ------ | ------ | --- | -------- | ---------- | ------- | -------- | ------ | --- |
Hence, the de(cid:28)nition of a support vector machine is a support vector classi(cid:28)er with a non-
| linear kernel | function. |          |     |         |        |             |        |         |     |     |
| ------------- | --------- | -------- | --- | ------- | ------ | ----------- | ------ | ------- | --- | --- |
| We            | can also  | consider | the | popular | radial | kernel (see | Figure | 13.10): |     |     |
|               |           |          |     |         |       |             |        |        |     |     |
p
(cid:88)
|     |     |     | K((cid:126)x | ,(cid:126)x )=exp−γ |     | (x  | −x )2 | , γ >0 |     | (13.21) |
| --- | --- | --- | ------------ | -------------------- | --- | --- | ----- | ------- | --- | ------- |
|     |     |     | i            | k                    |     | ij  | kj    |         |     |         |
j=1
Sohowdoradialkernelswork? Theyclearlydi(cid:27)erfrompolynomialkernels. Essentiallyifour
observation(cid:126)x∗
test is far from a training observation(cid:126)x i in standard Euclidean distance then the
(cid:80)p
sum (x∗−x )2 will be large and thus K((cid:126)x∗,(cid:126)x ) will be very small. Hence this particular
|     | j=1 j | ij  |     |     |     |     | i   |     |     |     |
| --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
training observation (cid:126)x will have almost no e(cid:27)ect on where the test observation (cid:126)x∗ is placed, via
i
f((cid:126)x∗).
Thus the radial kernel has extremely localised behaviour and only nearby training observa-
| tions to | (cid:126)x∗ will | have | an impact | on  | its class | label. |     |     |     |     |
| -------- | ---------------- | ---- | --------- | --- | --------- | ------ | --- | --- | --- | --- |

168
13.2 Document Classi(cid:28)cation using Support Vector Machines
InthissectionwewillapplySupportVectorMachinestothedomainofnaturallanguageprocess-
ing (NLP) for the purposes of sentiment analysis and ultimately automated trade (cid:28)lter or signal
generation. Our approach will be to use Support Vector Machines to classify text documents
into mutually exclusive groups. Note that this is a supervised learning technique. Later in the
| book we | will look | at unsupervised |     | techniques | for | similar | tasks. |
| ------- | --------- | --------------- | --- | ---------- | --- | ------- | ------ |
| 13.2.1  | Overview  |                 |     |            |     |         |        |
There are a signi(cid:28)cant number of steps to carry out between viewing a text document on a web
site, say, and using its content as an input to an automated trading strategy to generate trade
| (cid:28)lters or | signals. | In particular, |     | the following | steps | must | be carried out: |
| ---------------- | -------- | -------------- | --- | ------------- | ----- | ---- | --------------- |
(cid:136)
Automate the download of multiple, continually generated articles from external sources
| at a | potentially | high | throughput |     |     |     |     |
| ---- | ----------- | ---- | ---------- | --- | --- | --- | --- |
(cid:136)
Parse these documents for the relevant sections of text/information that require analysis,
| even | if the | format di(cid:27)ers |     | between documents |     |     |     |
| ---- | ------ | -------------------- | --- | ----------------- | --- | --- | --- |
(cid:136)
Convert arbitrarily long passages of text (over many possible languages) into a consistent
| data | structure | that | can be | understood | by  | a classi(cid:28)cation | system |
| ---- | --------- | ---- | ------ | ---------- | --- | ---------------------- | ------ |
(cid:136) Determine a set of groups (or labels) that each document will be a member of. Examples
| include | "positive" | and | "negative" | or  | "bullish" | and | "bearish" |
| ------- | ---------- | --- | ---------- | --- | --------- | --- | --------- |
(cid:136)
Createa"trainingcorpus"ofdocumentsthathaveknown labelsassociatedwiththem. For
instance, a thousand (cid:28)nancial articles may need tagging with the "bullish" or "bearish"
labels
(cid:136) Traintheclassi(cid:28)er(s)onthiscorpusbymeansofasoftwarelibrarysuchasPython’sscikit-
| learn | (which | we will | be using | below) |     |     |     |
| ----- | ------ | ------- | -------- | ------ | --- | --- | --- |
(cid:136) Use the classi(cid:28)er to label new documents, in an automated, ongoing manner.
(cid:136) Assess the "classi(cid:28)cation rate" and other associated performance metrics of the classi(cid:28)er
(cid:136)
Integrate the classi(cid:28)er into an automated trading system (such as QSTrader), either by
| means | of (cid:28)ltering | other | trade | signals | or generating |     | new ones. |
| ----- | ------------------ | ----- | ----- | ------- | ------------- | --- | --------- |
(cid:136) Continually monitor the system and adjust it as necessary, its performance begins to de-
grade
In this particular section we will avoid discussion of how to download multiple articles from
externalsourcesandmakeuseofagivendatasetthatalreadycomeswithitsownprovidedlabels.
This will allow us to concentrate on the implementation of the "classi(cid:28)cation pipeline", rather
than spend a substantial amount of time obtaining and tagging documents.
While beyond the scope of this section, it is possible to make use of Python libraries, such
as ScraPy and BeautifulSoup, to automatically obtain many web-based articles and e(cid:27)ectively
| extract their | text-based | data | from | the HTML | making | up  | the page data. |
| ------------- | ---------- | ---- | ---- | -------- | ------ | --- | -------------- |
Inlaterchaptersofthebookwewilldiscusshowtointegratesuchaclassi(cid:28)erintoaproduction-
| ready algorithmic |     | trading | system. |     |     |     |     |
| ----------------- | --- | ------- | ------- | --- | --- | --- | --- |
Hence,undertheassumptionthatwehaveadocumentcorpusthatispre-labelled(theprocess
ofwhichwillbeoutlinedbelow),wewillbeginbytakingthetrainingcorpusandincorporatingit
intoaPythondatastructurethatissuitableforpre-processing andconsumptionviatheclassi(cid:28)er.

169
| 13.2.2 | Supervised |     | Document |     | Classi(cid:28)cation |     |     |     |
| ------ | ---------- | --- | -------- | --- | -------------------- | --- | --- | --- |
Consider a set of text documents. Each document has an associated set of words, which we will
call "features". Each of these documents might be associated with a class label that describes
| what the | article | is about. |     |     |     |     |     |     |
| -------- | ------- | --------- | --- | --- | --- | --- | --- | --- |
For instance, a set of articles from a website discussing pets might have articles that are
primarily about dogs, cats or hamsters (say). Certain words, such as "cage" (hamster), "leash"
(dog) or "milk" (cat) might be more representative of certain pets than others. Supervised
classi(cid:28)ers are able to isolate certain words which are representative of certain labels (animals)
by "learning" from a set of "training" articles, which are already pre-labelled, often in a manual
| fashion, | by a | human. |     |     |     |     |     |     |
| -------- | ---- | ------ | --- | --- | --- | --- | --- | --- |
Mathematically, each of the j articles about pets within a training corpus have an associated
feature vector X , with components of this vector representing "strength" of words (we will
j
de(cid:28)ne "strength" below). Each article also has an associated class label, y , which in this case
j
| would be | the | name of | the pet | most associated |     | with | the article. |     |
| -------- | --- | ------- | ------- | --------------- | --- | ---- | ------------ | --- |
The "supervision" of the training procedure occurs when a model is trained or (cid:28)t to this
particular data. This means that the classi(cid:28)er is fed feature vector-class label pairs and it
"learns" how representative features are for particular class labels. In the following example we
will use the SVM as our model and "train" it on a corpus (a collection of documents) which we
| will have | previously | generated. |     |         |     |     |                      |     |
| --------- | ---------- | ---------- | --- | ------- | --- | --- | -------------------- | --- |
| 13.3      | Preparing  |            | a   | Dataset |     | for | Classi(cid:28)cation |     |
Afamousdatasetthatisusedinmachinelearningclassi(cid:28)cationdesignistheReuters21578set,
thedetailsofwhichcanbefoundhere: http://www.daviddlewis.com/resources/testcollections/reuters21578/.
| It is one | of the | most widely | used | testing | datasets |     | for text | classi(cid:28)cation. |
| --------- | ------ | ----------- | ---- | ------- | -------- | --- | -------- | --------------------- |
Thesetconsistsofacollectionofnewsarticles-a"corpus"-thataretaggedwithaselection
oftopicsandgeographiclocations. Thusitcomes"readymade"tobeusedinclassi(cid:28)cationtests,
| since it | is already | pre-labelled. |     |     |     |     |     |     |
| -------- | ---------- | ------------- | --- | --- | --- | --- | --- | --- |
We will now download, extract and prepare the dataset. The following instructions assume
you have access to a command line interface, such as the Terminal that ships with Linux or Mac
OS X. If you are using Windows then you will need to download a Tar/GZIP extraction tool to
| get hold | of the | data, such | as  | 7-Zip (http://www.7-zip.org/). |     |     |     |     |
| -------- | ------ | ---------- | --- | ------------------------------ | --- | --- | --- | --- |
TheReuters21578datasetcanbefoundathttp://kdd.ics.uci.edu/databases/reuters21578/reuters21578.tar.gz
as a compressed tar GZIP (cid:28)le. The (cid:28)rst task is to create a new working directory and download
| the (cid:28)le | into it. | Please | modify | the directory |     | name | below as | you see (cid:28)t: |
| -------------- | -------- | ------ | ------ | ------------- | --- | ---- | -------- | ------------------ |
cd ~
| mkdir | -p quantstart/classification/data |     |     |     |     |     |     |     |
| ----- | --------------------------------- | --- | --- | --- | --- | --- | --- | --- |
cd quantstart/classification/data
wget http://kdd.ics.uci.edu/databases/reuters21578/reuters21578.tar.gz
OnWindowsyouwillneedtousetherespectivecommandlinesyntaxtocreatethedirectories,
| or use    | Windows             | Explorer, | and       | use a     | web browser |            | to download | the data. |
| --------- | ------------------- | --------- | --------- | --------- | ----------- | ---------- | ----------- | --------- |
| We        | can then            | unzip     | and untar | the       | (cid:28)le: |            |             |           |
| tar -zxvf | reuters21578.tar.gz |           |           |           |             |            |             |           |
| On        | Windows             | you can   | use       | 7-Zip for | this        | procedure. |             |           |
If we list the contents of the directory (ls -l) we can see the following (the permissions and
| ownership | details | have  | been omitted |                              | for brevity): |     |     |     |
| --------- | ------- | ----- | ------------ | ---------------------------- | ------------- | --- | --- | --- |
| ...       | 186     | Dec 4 | 1996         | all-exchanges-strings.lc.txt |               |     |     |     |
| ...       | 316     | Dec 4 | 1996         | all-orgs-strings.lc.txt      |               |     |     |     |
| ...       | 2474    | Dec 4 | 1996         | all-people-strings.lc.txt    |               |     |     |     |
| ...       | 1721    | Dec 4 | 1996         | all-places-strings.lc.txt    |               |     |     |     |
| ...       | 1005    | Dec 4 | 1996         | all-topics-strings.lc.txt    |               |     |     |     |
cat-descriptions_120396.txt
| ...        | 28194 | Dec 4  | 1996 |                                    |     |     |     |     |
| ---------- | ----- | ------ | ---- | ---------------------------------- | --- | --- | --- | --- |
| ... 273802 |       | Dec 10 | 1996 | feldman-cia-worldfactbook-data.txt |     |     |     |     |

170
| ...         | 1485 | Jan 23 | 1997 lewis.dtd           |     |     |     |     |
| ----------- | ---- | ------ | ------------------------ | --- | --- | --- | --- |
| ... 36388   |      | Sep 26 | 1997 README.txt          |     |     |     |     |
| ... 1324350 |      | Dec 4  | 1996 reut2-000.sgm       |     |     |     |     |
| ... 1254440 |      | Dec 4  | 1996 reut2-001.sgm       |     |     |     |     |
| ... 1217495 |      | Dec 4  | 1996 reut2-002.sgm       |     |     |     |     |
| ... 1298721 |      | Dec 4  | 1996 reut2-003.sgm       |     |     |     |     |
| ... 1321623 |      | Dec 4  | 1996 reut2-004.sgm       |     |     |     |     |
| ... 1388644 |      | Dec 4  | 1996 reut2-005.sgm       |     |     |     |     |
| ... 1254765 |      | Dec 4  | 1996 reut2-006.sgm       |     |     |     |     |
| ... 1256772 |      | Dec 4  | 1996 reut2-007.sgm       |     |     |     |     |
| ... 1410117 |      | Dec 4  | 1996 reut2-008.sgm       |     |     |     |     |
| ... 1338903 |      | Dec 4  | 1996 reut2-009.sgm       |     |     |     |     |
| ... 1371071 |      | Dec 4  | 1996 reut2-010.sgm       |     |     |     |     |
| ... 1304117 |      | Dec 4  | 1996 reut2-011.sgm       |     |     |     |     |
| ... 1323584 |      | Dec 4  | 1996 reut2-012.sgm       |     |     |     |     |
| ... 1129687 |      | Dec 4  | 1996 reut2-013.sgm       |     |     |     |     |
| ... 1128671 |      | Dec 4  | 1996 reut2-014.sgm       |     |     |     |     |
| ... 1258665 |      | Dec 4  | 1996 reut2-015.sgm       |     |     |     |     |
| ... 1316417 |      | Dec 4  | 1996 reut2-016.sgm       |     |     |     |     |
| ... 1546911 |      | Dec 4  | 1996 reut2-017.sgm       |     |     |     |     |
| ... 1258819 |      | Dec 4  | 1996 reut2-018.sgm       |     |     |     |     |
| ... 1261780 |      | Dec 4  | 1996 reut2-019.sgm       |     |     |     |     |
| ... 1049566 |      | Dec 4  | 1996 reut2-020.sgm       |     |     |     |     |
| ... 621648  |      | Dec 4  | 1996 reut2-021.sgm       |     |     |     |     |
| ... 8150596 |      | Mar 12 | 1999 reuters21578.tar.gz |     |     |     |     |
You will see that all the (cid:28)les beginning with reut2- are .sgm, which means that they are
Standard Generalized Markup Language (SGML)[1] (cid:28)les. Unfortunately, Python deprecated
sgmllib from Python in 2.6 and fully removed it for Python 3. However, all is not lost because
we can create our own SGML Parser class that overrides Python’s built in HTMLParser[3].
| Here | is a single | news | item from | one | of the (cid:28)les: |     |     |
| ---- | ----------- | ---- | --------- | --- | ------------------- | --- | --- |
..
..
| <REUTERS                | TOPICS="YES" |                    | LEWISSPLIT="TRAIN" |     |            |     |     |
| ----------------------- | ------------ | ------------------ | ------------------ | --- | ---------- | --- | --- |
| CGISPLIT="TRAINING-SET" |              |                    | OLDID="5544"       |     | NEWID="1"> |     |     |
| <DATE>26-FEB-1987       |              | 15:01:01.79</DATE> |                    |     |            |     |     |
<TOPICS><D>cocoa</D></TOPICS>
<PLACES><D>el-salvador</D><D>usa</D><D>uruguay</D></PLACES>
<PEOPLE></PEOPLE>
<ORGS></ORGS>
<EXCHANGES></EXCHANGES>
<COMPANIES></COMPANIES>
<UNKNOWN>
| &#5;&#5;&#5;C |     | T   |     |     |     |     |     |
| ------------- | --- | --- | --- | --- | --- | --- | --- |
&#22;&#22;&#1;f0704&#31;reute
| u f BC-BAHIA-COCOA-REVIEW |     |     |     | 02-26 | 0105</UNKNOWN> |     |     |
| ------------------------- | --- | --- | --- | ----- | -------------- | --- | --- |
<TEXT>&#2;
| <TITLE>BAHIA |           | COCOA      | REVIEW</TITLE> |          |                     |                  |       |
| ------------ | --------- | ---------- | -------------- | -------- | ------------------- | ---------------- | ----- |
| <DATELINE>   |           | SALVADOR,  | Feb            | 26       | - </DATELINE><BODY> |                  |       |
| Showers      | continued | throughout |                | the      | week in             |                  |       |
| the Bahia    | cocoa     | zone,      | alleviating    |          | the drought         | since early      |       |
| January      | and       | improving  | prospects      |          | for the             | coming temporao, |       |
| although     | normal    | humidity   | levels         |          | have not            | been restored,   |       |
| Comissaria   | Smith     | said       | in its         | weekly   | review.             |                  |       |
| The          | dry       | period     | means the      | temporao | will                | be late this     | year. |
| Arrivals     |           | for the    | week           | ended    | February            | 22 were 155,221  | bags  |

171
of 60 kilos making a cumulative total for the season of 5.93
mln against 5.81 at the same stage last year. Again it seems
that cocoa delivered earlier on consignment was included in the
arrivals figures.
Comissaria Smith said there is still some doubt as to how
much old crop cocoa is still available as harvesting has
practically come to an end. With total Bahia crop estimates
around 6.4 mln bags and sales standing at almost 6.2 mln there
are a few hundred thousand bags still in the hands of farmers,
middlemen, exporters and processors.
There are doubts as to how much of this cocoa would be fit
for export as shippers are now experiencing dificulties in
obtaining +Bahia superior+ certificates.
In view of the lower quality over recent weeks farmers have
sold a good part of their cocoa held on consignment.
Comissaria Smith said spot bean prices rose to 340 to 350
cruzados per arroba of 15 kilos.
Bean shippers were reluctant to offer nearby shipment and
only limited sales were booked for March shipment at 1,750 to
1,780 dlrs per tonne to ports to be named.
New crop sales were also light and all to open ports with
June/July going at 1,850 and 1,880 dlrs and at 35 and 45 dlrs
under New York july, Aug/Sept at 1,870, 1,875 and 1,880 dlrs
per tonne FOB.
Routine sales of butter were made. March/April sold at
4,340, 4,345 and 4,350 dlrs.
April/May butter went at 2.27 times New York May, June/July
at 4,400 and 4,415 dlrs, Aug/Sept at 4,351 to 4,450 dlrs and at
2.27 and 2.28 times New York Sept and Oct/Dec at 4,480 dlrs and
2.27 times New York Dec, Comissaria Smith said.
Destinations were the U.S., Covertible currency areas,
Uruguay and open ports.
Cake sales were registered at 785 to 995 dlrs for
March/April, 785 dlrs for May, 753 dlrs for Aug and 0.39 times
New York Dec for Oct/Dec.
Buyers were the U.S., Argentina, Uruguay and convertible
currency areas.
Liquor sales were limited with March/April selling at 2,325
and 2,380 dlrs, June/July at 2,375 dlrs and at 1.25 times New
York July, Aug/Sept at 2,400 dlrs and at 1.25 times New York
Sept and Oct/Dec at 1.25 times New York Dec, Comissaria Smith
said.
Total Bahia sales are currently estimated at 6.13 mln bags
against the 1986/87 crop and 1.06 mln bags against the 1987/88
crop.
Final figures for the period to February 28 are expected to
be published by the Brazilian Cocoa Trade Commission after
carnival which ends midday on February 27.
Reuter
&#3;</BODY></TEXT>
</REUTERS>
..
..
Whileitmaybesomewhatlaborioustoparsedatainthismanner,especiallywhencompared
to the actual machine learning, I can fully reassure you that a large part of a data scientist’s
or quant researcher’s day is in actually getting the data into a format usable by the analysis

172
software! This particular activity is often jokingly referred to as "data wrangling". Hence I feel
it is worth it for you to get some practice at it!
If we take a look at the topics (cid:28)le, all-topics-strings.lc.txt, by typing
less all-topics-strings.lc.tx
we can see the following (I’ve removed most of it for brevity):
acq
alum
austdlr
austral
barley
bfr
bop
can
carcass
castor-meal
castor-oil
castorseed
citruspulp
cocoa
coconut
coconut-oil
coffee
copper
copra-cake
corn
...
...
silver
singdlr
skr
sorghum
soy-meal
soy-oil
soybean
stg
strategic-metal
sugar
sun-meal
sun-oil
sunseed
tapioca
tea
tin
trade
tung
tung-oil
veg-oil
wheat
wool
wpi
yen
zinc
By calling:
cat all-topics-strings.lc.txt | wc -l

173
we can see that there are 135 separate topics among the articles. This will make for quite a
| classi(cid:28)cation |     | challenge! |     |     |     |     |     |
| -------------------- | --- | ---------- | --- | --- | --- | --- | --- |
At this stage we need to create what is known as a list of predictor-response pairs. This is a
list of two-tuples that contain the most appropriate class label and the raw document text, as
two separate components. For instance, we wish to end up with a data structure, after parsing,
| which | is similar | to  | the following: |     |     |     |     |
| ----- | ---------- | --- | -------------- | --- | --- | --- | --- |
[
|     | ("cat", | "It | is best | not to | give them | too | much milk"), |
| --- | ------- | --- | ------- | ------ | --------- | --- | ------------ |
(
|     | "dog", | "Last  | night  | we took | him for | a      | walk, |
| --- | ------ | ------ | ------ | ------- | ------- | ------ | ----- |
|     |        | but he | had to | remain  | on the  | leash" |       |
),
..
..
("hamster", "Today we cleaned out the cage and prepared the sawdust"),
("cat", "Kittens require a lot of attention in the first few months")
]
To create this structure we will need to parse all of the Reuters (cid:28)les individually and add
them to a grand corpus list. Since the (cid:28)le size of the corpus is rather low, it will easily (cid:28)t into
| available | RAM | on most | modern | laptops/desktops. |     |     |     |
| --------- | --- | ------- | ------ | ----------------- | --- | --- | --- |
However, in production applications it is usually necessary to stream training data into a
machine learning system and carry out "partial (cid:28)tting" on each batch, in an iterative manner.
Inlaterchapterswewillconsiderthiswhenwestudyextremelylargedatasets(particularlytick
data).
As stated above, our (cid:28)rst goal is to actually create the SGML Parser that will achieve this.
TodothiswewillsubclassPython’sHTMLParserclasstohandlethespeci(cid:28)ctagsintheReuters
dataset.
UponsubclassingHTMLParserweoverridethreemethods,handle_starttag,handle_endtag
handle_data,
and which tell the parser what to do at the beginning of SGML tags, what to do
| at the | closing | of SGML | tags | and how | to handle | the data | in between. |
| ------ | ------- | ------- | ---- | ------- | --------- | -------- | ----------- |
We also create two additional methods, _reset and parse, which are used to take care of
internal state of the class and to parse the actual data in a chunked fashion, so as not to use up
| too | much | memory. |     |     |     |     |     |
| --- | ---- | ------- | --- | --- | --- | --- | --- |
__main__
Finally, I have created a basic function to test the parser on the (cid:28)rst set of data
| within | the        | Reuters | corpus: |                |     |     |     |
| ------ | ---------- | ------- | ------- | -------------- | --- | --- | --- |
|        | __future__ |         |         | print_function |     |     |     |
| from   |            |         | import  |                |     |     |     |
import pprint
import re
try:
|     | from |             | import |            |     |     |     |
| --- | ---- | ----------- | ------ | ---------- | --- | --- | --- |
|     |      | html.parser |        | HTMLParser |     |     |     |
except ImportError:
|     | from | HTMLParser | import | HTMLParser |     |     |     |
| --- | ---- | ---------- | ------ | ---------- | --- | --- | --- |
class ReutersParser(HTMLParser):
"""
ReutersParser subclasses HTMLParser and is used to open the SGML
files associated with the Reuters-21578 categorised test collection.
The parser is a generator and will yield a single document at a time.
Since the data will be chunked on parsing, it is necessary to keep
some internal state of when tags have been "entered" and "exited".
|     |       | in_body, |     | in_topics | in_topic_d |     |                  |
| --- | ----- | -------- | --- | --------- | ---------- | --- | ---------------- |
|     | Hence | the      |     |           | and        |     | boolean members. |
"""

174
__init__(self,
| def |     | encoding=’latin-1’): |     |     |     |     |     |     |
| --- | --- | -------------------- | --- | --- | --- | --- | --- | --- |
"""
| Initialise | the      | superclass | (HTMLParser) |       |     | and reset |     | the parser. |
| ---------- | -------- | ---------- | ------------ | ----- | --- | --------- | --- | ----------- |
| Sets the   | encoding | of         | the SGML     | files | by  | default   | to  | latin-1.    |
"""
HTMLParser.__init__(self)
self._reset()
| self.encoding | =   | encoding |     |     |     |     |     |     |
| ------------- | --- | -------- | --- | --- | --- | --- | --- | --- |
def _reset(self):
"""
| This is  | called | only       | on initialisation |     | of   | the        | parser | class |
| -------- | ------ | ---------- | ----------------- | --- | ---- | ---------- | ------ | ----- |
| and when | a new  | topic-body | tuple             | has | been | generated. |        | It    |
resets all off the state so that a new tuple can be subsequently
generated.
"""
self.in_body
= False
| self.in_topics |     | = False |     |     |     |     |     |     |
| -------------- | --- | ------- | --- | --- | --- | --- | --- | --- |
self.in_topic_d
= False
| self.body   | = "" |     |     |     |     |     |     |     |
| ----------- | ---- | --- | --- | --- | --- | --- | --- | --- |
| self.topics | = [] |     |     |     |     |     |     |     |
self.topic_d
= ""
| def parse(self, | fd): |     |     |     |     |     |     |     |
| --------------- | ---- | --- | --- | --- | --- | --- | --- | --- |
"""
| parse accepts | a   | file | descriptor | and | loads | the | data | in chunks |
| ------------- | --- | ---- | ---------- | --- | ----- | --- | ---- | --------- |
in order to minimise memory usage. It then yields new documents
| as they | are parsed. |     |     |     |     |     |     |     |
| ------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
"""
| self.docs | = []   |     |     |     |     |     |     |     |
| --------- | ------ | --- | --- | --- | --- | --- | --- | --- |
| for chunk | in fd: |     |     |     |     |     |     |     |
self.feed(chunk.decode(self.encoding))
| for | doc in | self.docs: |     |     |     |     |     |     |
| --- | ------ | ---------- | --- | --- | --- | --- | --- | --- |
yield doc
| self.docs | =   | []  |     |     |     |     |     |     |
| --------- | --- | --- | --- | --- | --- | --- | --- | --- |
self.close()
| def handle_starttag(self, |     |     | tag, | attrs): |     |     |     |     |
| ------------------------- | --- | --- | ---- | ------- | --- | --- | --- | --- |
"""
| This method | is  | used | to determine |     | what to | do  | when | the parser |
| ----------- | --- | ---- | ------------ | --- | ------- | --- | ---- | ---------- |
comes across a particular tag of type "tag". In this instance
we simply set the internal state booleans to True if that particular
| tag has | been found. |     |     |     |     |     |     |     |
| ------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
"""
| if tag == | "reuters": |     |     |     |     |     |     |     |
| --------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
pass
| elif tag     | == "body":   |        |     |     |     |     |     |     |
| ------------ | ------------ | ------ | --- | --- | --- | --- | --- | --- |
| self.in_body |              | = True |     |     |     |     |     |     |
| elif tag     | == "topics": |        |     |     |     |     |     |     |
self.in_topics
= True
| elif tag | == "d": |     |     |     |     |     |     |     |
| -------- | ------- | --- | --- | --- | --- | --- | --- | --- |
self.in_topic_d
= True
| def handle_endtag(self, |     |     | tag): |     |     |     |     |     |
| ----------------------- | --- | --- | ----- | --- | --- | --- | --- | --- |
"""
| This method | is  | used | to determine |     | what to | do  | when | the parser |
| ----------- | --- | ---- | ------------ | --- | ------- | --- | ---- | ---------- |

175
| finishes    |         | with a particular |           | tag         | of   | type | "tag".   |           |     |
| ----------- | ------- | ----------------- | --------- | ----------- | ---- | ---- | -------- | --------- | --- |
| If          | the tag | is a <REUTERS>    |           | tag,        | then | we   | remove   | all       |     |
| white-space |         | with              | a regular | expression  |      |      | and then | append    | the |
| topic-body  |         | tuple.            |           |             |      |      |          |           |     |
| If          | the tag | is a <BODY>       |           | or <TOPICS> |      | tag  | then     | we simply | set |
the internal state to False for these booleans, respectively.
If the tag is a <D> tag (found within a <TOPICS> tag), then we
| append  | the | particular | topic |     | to the | "topics" |     | list and |     |
| ------- | --- | ---------- | ----- | --- | ------ | -------- | --- | -------- | --- |
| finally |     | reset it.  |       |     |        |          |     |          |     |
"""
| if  | tag ==            | "reuters":       |               |     |     |               |     |     |     |
| --- | ----------------- | ---------------- | ------------- | --- | --- | ------------- | --- | --- | --- |
|     | self.body         | = re.sub(r’\s+’, |               |     | r’  | ’, self.body) |     |     |     |
|     | self.docs.append( |                  | (self.topics, |     |     | self.body)    |     | )   |     |
self._reset()
| elif | tag | == "body": |     |     |     |     |     |     |     |
| ---- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
self.in_body
|      |                 |              | = False |     |     |     |     |     |     |
| ---- | --------------- | ------------ | ------- | --- | --- | --- | --- | --- | --- |
| elif | tag             | == "topics": |         |     |     |     |     |     |     |
|      | self.in_topics  |              | = False |     |     |     |     |     |     |
| elif | tag             | == "d":      |         |     |     |     |     |     |     |
|      | self.in_topic_d |              | = False |     |     |     |     |     |     |
self.topics.append(self.topic_d)
|     | self.topic_d |     | = "" |     |     |     |     |     |     |
| --- | ------------ | --- | ---- | --- | --- | --- | --- | --- | --- |
handle_data(self,
| def |     |     | data): |     |     |     |     |     |     |
| --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
"""
| The | data | is simply | appended |     | to the | appropriate |     | member | state |
| --- | ---- | --------- | -------- | --- | ------ | ----------- | --- | ------ | ----- |
for that particular tag, up until the end closing tag appears.
"""
self.in_body:
if
|      | self.body        | +=  | data |     |     |     |     |     |     |
| ---- | ---------------- | --- | ---- | --- | --- | --- | --- | --- | --- |
| elif | self.in_topic_d: |     |      |     |     |     |     |     |     |
self.topic_d
|             |                             |             | += data   |         |           |        |             |        |     |
| ----------- | --------------------------- | ----------- | --------- | ------- | --------- | ------ | ----------- | ------ | --- |
| if __name__ | == "__main__":              |             |           |         |           |        |             |        |     |
| # Open      | the first                   | Reuters     | data      | set     | and       | create | the         | parser |     |
| filename    | = "data/reut2-000.sgm"      |             |           |         |           |        |             |        |     |
| parser      | = ReutersParser()           |             |           |         |           |        |             |        |     |
| # Parse     | the                         | document    | and force | all     | generated |        | docs        | into   |     |
| # a list    | so                          | that it can | be        | printed | out       | to     | the console |        |     |
| doc =       | parser.parse(open(filename, |             |           |         | ’rb’))    |        |             |        |     |
pprint.pprint(list(doc))
At this stage we will see a signi(cid:28)cant amount of output that looks like this:
..
..
| ([’grain’, | ’rice’, | ’thailand’], |     |     |     |     |     |     |     |
| ---------- | ------- | ------------ | --- | --- | --- | --- | --- | --- | --- |
’Thailand exported 84,960 tonnes of rice in the week ended February 24, ’
’up from 80,498 the previous week, the Commerce Ministry said. It said ’
’government and private exporters shipped 27,510 and 57,450 tonnes ’
’respectively. Private exporters concluded advance weekly sales for ’
’79,448 tonnes against 79,014 the previous week. Thailand exported ’

176
’689,038 tonnes of rice between the beginning of January and February 24, ’
’up from 556,874 tonnes during the same period last year. It has ’
’commitments to export another 658,999 tonnes this year. REUTER ’),
([’soybean’, ’red-bean’, ’oilseed’, ’japan’],
’The Tokyo Grain Exchange said it will raise the margin requirement on ’
’the spot and nearby month for U.S. And Chinese soybeans and red beans, ’
’effective March 2. Spot April U.S. Soybean contracts will increase to ’
’90,000 yen per 15 tonne lot from 70,000 now. Other months will stay ’
’unchanged at 70,000, except the new distant February requirement, which ’
’will be set at 70,000 from March 2. Chinese spot March will be set at ’
’110,000 yen per 15 tonne lot from 90,000. The exchange said it raised ’
’spot March requirement to 130,000 yen on contracts outstanding at March ’
’13. Chinese nearby April rises to 90,000 yen from 70,000. Other months ’
’will remain unchanged at 70,000 yen except new distant August, which ’
’will be set at 70,000 from March 2. The new margin for red bean spot ’
’March rises to 150,000 yen per 2.4 tonne lot from 120,000 and to 190,000 ’
’for outstanding contracts as of March 13. The nearby April requirement ’
’for red beans will rise to 100,000 yen from 60,000, effective March 2. ’
’The margin money for other red bean months will remain unchanged at ’
’60,000 yen, except new distant August, for which the requirement will ’
’also be set at 60,000 from March 2. REUTER ’),
..
..
In particular, note that instead of having a single topic label associated with a document,
we have multiple topics. In order to increase the e(cid:27)ectiveness of the classi(cid:28)er, it is necessary
to assign only a single class label to each document. However, you’ll also note that some of
the labels are actually geographic location tags, such as "japan" or "thailand". Since we are
concerned solely with topics and not countries we want to remove these before we select our
topic.
The particular method that we will use to carry this out is rather simple. We will strip out
thecountrynamesandthenselectthe(cid:28)rstremainingtopiconthelist. Iftherearenoassociated
topics we will eliminate the article from our corpus. In the above output, this will reduce to a
data structure that looks like:
..
..
(’grain’,
’Thailand exported 84,960 tonnes of rice in the week ended February 24, ’
’up from 80,498 the previous week, the Commerce Ministry said. It said ’
’government and private exporters shipped 27,510 and 57,450 tonnes ’
’respectively. Private exporters concluded advance weekly sales for ’
’79,448 tonnes against 79,014 the previous week. Thailand exported ’
’689,038 tonnes of rice between the beginning of January and February 24, ’
’up from 556,874 tonnes during the same period last year. It has ’
’commitments to export another 658,999 tonnes this year. REUTER ’),
(’soybean’,
’The Tokyo Grain Exchange said it will raise the margin requirement on ’
’the spot and nearby month for U.S. And Chinese soybeans and red beans, ’
’effective March 2. Spot April U.S. Soybean contracts will increase to ’
’90,000 yen per 15 tonne lot from 70,000 now. Other months will stay ’
’unchanged at 70,000, except the new distant February requirement, which ’
’will be set at 70,000 from March 2. Chinese spot March will be set at ’
’110,000 yen per 15 tonne lot from 90,000. The exchange said it raised ’
’spot March requirement to 130,000 yen on contracts outstanding at March ’
’13. Chinese nearby April rises to 90,000 yen from 70,000. Other months ’
’will remain unchanged at 70,000 yen except new distant August, which ’

177
’will be set at 70,000 from March 2. The new margin for red bean spot ’
’March rises to 150,000 yen per 2.4 tonne lot from 120,000 and to 190,000 ’
’for outstanding contracts as of March 13. The nearby April requirement ’
’for red beans will rise to 100,000 yen from 60,000, effective March 2. ’
’The margin money for other red bean months will remain unchanged at ’
’60,000 yen, except new distant August, for which the requirement will ’
| ’also | be set | at 60,000 | from | March | 2.  | REUTER | ’), |
| ----- | ------ | --------- | ---- | ----- | --- | ------ | --- |
..
..
To remove the geographic tags and select the primary topic tag we can add the following
code:
..
..
def obtain_topic_tags():
"""
| Open   | the  | topic list | file | and      | import | all of | the topic names |
| ------ | ---- | ---------- | ---- | -------- | ------ | ------ | --------------- |
| taking | care | to strip   | the  | trailing | "\n"   | from   | each word.      |
"""
| topics | =                                 | open( |     |     |     |     |     |
| ------ | --------------------------------- | ----- | --- | --- | --- | --- | --- |
|        | "data/all-topics-strings.lc.txt", |       |     |     |     | "r" |     |
).readlines()
| topics | =      | [t.strip() | for | t in | topics] |     |     |
| ------ | ------ | ---------- | --- | ---- | ------- | --- | --- |
| return | topics |            |     |      |         |     |     |
filter_doc_list_through_topics(topics,
| def |     |     |     |     |     | docs): |     |
| --- | --- | --- | --- | --- | --- | ------ | --- |
"""
Reads all of the documents and creates a new list of two-tuples
that contain a single feature entry and the body text, instead of
a list of topics. It removes all geographic features and only
retains those documents which have at least one non-geographic
topic.
"""
ref_docs
= []
| for | d in    | docs: |         |     |     |     |     |
| --- | ------- | ----- | ------- | --- | --- | --- | --- |
|     | if d[0] | == [] | or d[0] | ==  | "": |     |     |
continue
|     | for | t in d[0]:      |       |       |     |     |     |
| --- | --- | --------------- | ----- | ----- | --- | --- | --- |
|     |     | if t in topics: |       |       |     |     |     |
|     |     | d_tup           | = (t, | d[1]) |     |     |     |
ref_docs.append(d_tup)
break
| return      | ref_docs                           |                        |      |            |         |              |             |
| ----------- | ---------------------------------- | ---------------------- | ---- | ---------- | ------- | ------------ | ----------- |
| if __name__ |                                    | == "__main__":         |      |            |         |              |             |
| #           | Open the                           | first Reuters          |      | data       | set and | create       | the parser  |
| filename    |                                    | = "data/reut2-000.sgm" |      |            |         |              |             |
| parser      | =                                  | ReutersParser()        |      |            |         |              |             |
| #           | Parse                              | the document           | and  | force      | all     | generated    | docs into   |
| #           | a list                             | so that it             | can  | be printed |         | out to       | the console |
| docs        | = list(parser.parse(open(filename, |                        |      |            |         | ’rb’)))      |             |
| #           | Obtain                             | the topic              | tags | and filter |         | docs through | it          |

178
topics = obtain_topic_tags()
ref_docs = filter_doc_list_through_topics(topics, docs)
pprint.pprint(ref_docs)
The output from this is as follows:
..
..
(’acq’,
’Security Pacific Corp said it completed its planned merger with Diablo ’
’Bank following the approval of the comptroller of the currency. Security ’
’Pacific announced its intention to merge with Diablo Bank, headquartered ’
’in Danville, Calif., in September 1986 as part of its plan to expand its ’
’retail network in Northern California. Diablo has a bank offices in ’
’Danville, San Ramon and Alamo, Calif., Security Pacific also said. ’
’Reuter ’),
(’earn’,
’Shr six cts vs five cts Net 188,000 vs 130,000 Revs 12.2 mln vs 10.1 mln ’
’Avg shrs 3,029,930 vs 2,764,544 12 mths Shr 81 cts vs 1.45 dlrs Net ’
’2,463,000 vs 3,718,000 Revs 52.4 mln vs 47.5 mln Avg shrs 3,029,930 vs ’
’2,566,680 NOTE: net for 1985 includes 500,000, or 20 cts per share, for ’
’proceeds of a life insurance policy. includes tax benefit for prior qtr ’
’of approximately 150,000 of which 140,000 relates to a lower effective ’
’tax rate based on operating results for the year as a whole. Reuter ’),
..
..
We are now in a position to pre-process the data for input into the classi(cid:28)er.
13.3.1 Vectorisation
Atthisstagewehavealargecollectionoftwo-tuples, eachcontainingaclasslabelandrawbody
text from the articles. The obvious question to ask now is how do we convert the raw body text
into a data representation that can be used by a (numerical) classi(cid:28)er?
The answer lies in a process known as vectorisation. Vectorisation allows widely-varying
lengthsofrawtexttobeconvertedintoanumericalformatthatcanbeprocessedbytheclassi(cid:28)er.
It achieves this by creating tokens from a string. A token is an individual word (or group of
words) extracted from a document, using whitespace or punctuation as separators. This can, of
course, include numbers from within the string as additional "words". Once this list of tokens
has been created they can be assigned an integer identi(cid:28)er, which allows them to be listed.
Once the list of tokens have been generated, the number of tokens within a document are
counted. Finally, these tokens are normalised to de-emphasise tokens that appear frequently
within a document (such as "a", "the"). This process is known as the Bag Of Words.
The Bag Of Words representation allows a vector to be associated with each document,
each component of which is real-valued (i.e. ∈ R) and represents the importance of tokens (i.e.
"words") appearing within that document.
Furthermore it means that once an entire corpus of documents has been iterated over (and
thusallpossibletokenshavebeenassessed)thetotalnumberofseparatetokensisknown. Hence
the length of the token vector for any document of any length is also (cid:28)xed and identical.
This means that the classi(cid:28)er now has a set of features via the frequency of token occurance.
In addition the document token-vector represents a sample for the classi(cid:28)er.
Inessence,theentirecorpuscanberepresentedasalargematrix,eachrowofwhichrepresents
one of the documents and each column represents token occurance within that document. This
is the process of vectorisation.
Note that vectorisation does not take into account the relative positioning of the words within
the document, just the frequency of occurance. More sophisticated machine learning techniques
will, however, use this information to enhance the classi(cid:28)cation process.

179
13.3.2 Term-Frequency Inverse Document-Frequency
One of the major issues with vectorisation, via the Bag Of Words representation, is that
there is a lot of "noise" in the form of stop words, such as "a", "the", "he", "she" etc. These
words provide little context to the document but their relatively high frequency will mean that
they can mask words that do provide document context.
Thismotivatesatransformationprocess,knownasTerm-Frequency Inverse Document-
Frequency (TF-IDF). The TF-IDF value for a token increases proportionally to the frequency
of the word in the document but is normalised by the frequency of the word in the corpus. This
essentially reduces importance for words that appear a lot generally, as opposed to appearing a
lot within a particular document.
Thisispreciselywhatweneedaswordssuchas"a","the"willhaveextremelyhighoccurances
within the entire corpus, but the word "cat" may only appear often in a particular document.
This would mean that we are giving "cat" a relatively higher strength than "a" or "the", for
that document.
It isn’t necessary dwell on the calculation of TF-IDF, but if you are interested then you can
read the Wikipedia article[6] on the subject, which goes into more detail.
Hence we wish to combine the process of vectorisation with that of TF-IDF to produce a
normalised matrix of document-token occurances. This will then be used to provide a list of
features to the classi(cid:28)er upon which to train.
Thankfully, the developers of the Python Scikit-Learn library realised that it would be an
extremelycommonoperationtovectoriseandtransformtext(cid:28)lesinthismannerandsoincluded
the TfidfVectorizer class.
Wecanusethisclasstotakeourlistoftwo-tuplesrepresentingclasslabelsandrawdocument
text, to produce both a vector of class labels and a sparse matrix, which represents the TF-IDF
and Vectorisation procedure applied to the raw text data.
Since Scikit-Learn classi(cid:28)ers take two separate data structures for training, namely, y, the
vector of class labels or "responses" associated with an ordered set of documents, and, X, the
sparse TF-IDF matrix of raw document text, we modify our two-tuple list to create y and X.
The code to create these objects is given below:
..
from sklearn.feature_extraction.text import TfidfVectorizer
..
..
def create_tfidf_training_data(docs):
"""
Creates a document corpus list (by stripping out the
class labels), then applies the TF-IDF transform to this
list.
The function returns both the class label vector (y) and
the corpus token/feature matrix (X).
"""
# Create the training data class labels
y = [d[0] for d in docs]
# Create the document corpus list
corpus = [d[1] for d in docs]
# Create the TF-IDF vectoriser and transform the corpus
vectorizer = TfidfVectorizer(min_df=1)
X = vectorizer.fit_transform(corpus)
return X, y

180
if __name__ == "__main__":
# Open the first Reuters data set and create the parser
filename = "data/reut2-000.sgm"
parser = ReutersParser()
# Parse the document and force all generated docs into
# a list so that it can be printed out to the console
docs = list(parser.parse(open(filename, ’rb’)))
# Obtain the topic tags and filter docs through it
topics = obtain_topic_tags()
ref_docs = filter_doc_list_through_topics(topics, docs)
# Vectorise and TF-IDF transform the corpus
X, y = create_tfidf_training_data(ref_docs)
At this stage we now have two components to our training data. The (cid:28)rst, X, is a matrix
of document-token occurances. The second, y, is a vector (which matches the ordering of the
matrix) that contains the correct class labels for each of the documents. This is all we need to
begin training and testing the Support Vector Machine.
13.4 Training the Support Vector Machine
In order to train the Support Vector Machine it is necessary to provide it with both a set of
features (the X matrix) and a set of "supervised" training labels, in this case the y classes.
However,wealsoneedameansofevaluatingthetrainedperformanceoftheclassi(cid:28)ersubsequent
toitstrainingphase. Wediscussedapproachesforthisinthepreviouschapteroncross-validation.
One question that arises here is what percentage to retain for training and what to use for
testing. Clearly the more that is retained for training, the "better" the classi(cid:28)er will be because
it will have seen more data. More training data means less testing data and as such will lead to
apoorerestimateofitstrueclassi(cid:28)cationcapability. Inthissectionwewillretainapproximately
about 70-80% of the data for training and use the remainder for testing. A more sophisticated
approach would be to use k-fold cross-validation.
Since the training-test split is such a common operation in machine learning, the developers
of Scikit-Learn provided the train_test_split method to automatically create the split from
a dataset provided (which we have already discussed in the previous chapter). Here is the code
that provides the split:
from sklearn.cross_validation import train_test_split
..
..
X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.2, random_state=42
)
The test_size keyword argument controls the size of the testing set, in this case 20%. The
random_statekeywordargumentcontrolstherandomseedforselectingthepartitionrandomly.
The next step is to actually create the Support Vector Machine and train it. In this instance
we are going to use the SVC (Support Vector Classi(cid:28)er) class from Scikit-Learn. We give it the
parameters C = 1000000.0, γ = 0.0 and choose a radial kernel. To understand where these
parameters come from, please take a look at the previous section on Support Vector Machines
The following code imports the SVC class and then (cid:28)ts it on the training data:
from sklearn.svm import SVC
..
..
def train_svm(X, y):
"""

181
| Create | and | train | the | Support | Vector | Machine. |     |
| ------ | --- | ----- | --- | ------- | ------ | -------- | --- |
"""
| svm         | = SVC(C=1000000.0,                 |                                        |         | gamma=0.0, | kernel=’rbf’) |              |             |
| ----------- | ---------------------------------- | -------------------------------------- | ------- | ---------- | ------------- | ------------ | ----------- |
| svm.fit(X,  |                                    | y)                                     |         |            |               |              |             |
| return      | svm                                |                                        |         |            |               |              |             |
| if __name__ | ==                                 | "__main__":                            |         |            |               |              |             |
| # Open      | the                                | first                                  | Reuters | data       | set and       | create       | the parser  |
| filename    | =                                  | "data/reut2-000.sgm"                   |         |            |               |              |             |
| parser      | = ReutersParser()                  |                                        |         |            |               |              |             |
| # Parse     | the                                | document                               |         | and force  | all           | generated    | docs into   |
| # a         | list so                            | that                                   | it can  | be printed |               | out to       | the console |
| docs        | = list(parser.parse(open(filename, |                                        |         |            |               | ’rb’)))      |             |
| # Obtain    | the                                | topic                                  | tags    | and filter |               | docs through | it          |
| topics      | = obtain_topic_tags()              |                                        |         |            |               |              |             |
| ref_docs    |                                    | filter_doc_list_through_topics(topics, |         |            |               |              |             |
|             | =                                  |                                        |         |            |               |              | docs)       |
| # Vectorise |                                    | and                                    | TF-IDF  | transform  | the           | corpus       |             |
create_tfidf_training_data(ref_docs)
| X, y     | =       |                |          |                 |     |                   |     |
| -------- | ------- | -------------- | -------- | --------------- | --- | ----------------- | --- |
| # Create | the     | training-test  |          | split           | of  | the data          |     |
| X_train, | X_test, |                | y_train, | y_test          | =   | train_test_split( |     |
|          | X, y,   | test_size=0.2, |          | random_state=42 |     |                   |     |
)
| # Create | and                  | train | the | Support  | Vector | Machine |     |
| -------- | -------------------- | ----- | --- | -------- | ------ | ------- | --- |
| svm      | = train_svm(X_train, |       |     | y_train) |        |         |     |
Now that the SVM has been trained we need to assess its performance on the testing data.
| 13.4.1 | Performance |     | Metrics |     |     |     |     |
| ------ | ----------- | --- | ------- | --- | --- | --- | --- |
The two main performance metrics that we will consider for this supervised classifer are the
hit-rate and the confusion matrix. The former is simply the ratio of correct assignments to
| total assignments |     | and is | usually | quoted as | a percentage. |     |     |
| ----------------- | --- | ------ | ------- | --------- | ------------- | --- | --- |
The confusion matrix goes into more detail and provides output on true-positives, true-
negatives, false-positives and false-negatives. In a binary classi(cid:28)cation system, with a "true"
or "false" class labelling, these characterise the rate at which the classi(cid:28)er correctly classi(cid:28)es
an entity as true or false when it is, respectively, true or false, and also incorrectly classi(cid:28)es an
| entity as true | or  | false when | it  | is, respectively, | false | or true. |     |
| -------------- | --- | ---------- | --- | ----------------- | ----- | -------- | --- |
A confusion matrix need not be restricted to a binary classi(cid:28)cation situation. For multiple
class groups (as in our situation with the Reuters dataset) we will have an N×N matrix, where
| N is the number |     | of class | labels | (or document | topics). |     |     |
| --------------- | --- | -------- | ------ | ------------ | -------- | --- | --- |
Scikit-Learn has functions for calculating both the hit-rate and the confusion matrix of a
supervised classi(cid:28)er. The former is a method on the classi(cid:28)er itself called score. The latter
| must be imported |     | from | the metrics | library. |     |     |     |
| ---------------- | --- | ---- | ----------- | -------- | --- | --- | --- |
The (cid:28)rst task is to create a predictions array from the X_test test-set. This will simply
contain the predicted class labels from the SVM via the retained 20% test set. This prediction
array is used to create the confusion matrix. Notice that the confusion_matrix function takes
both the pred predictions array and the y_test correct class labels to produce the matrix. In
additionwecreatethehit-ratebyprovidingscorewithboththeX_testandy_testsubsetsof
the dataset:
..

182
..
| from sklearn.metrics |     |     | import | confusion_matrix |     |     |     |     |
| -------------------- | --- | --- | ------ | ---------------- | --- | --- | --- | --- |
..
..
| if __name__ | ==  | "__main__": |     |     |     |     |     |     |
| ----------- | --- | ----------- | --- | --- | --- | --- | --- | --- |
..
..
| # Create | and                   | train | the            | Support  | Vector | Machine |     |     |
| -------- | --------------------- | ----- | -------------- | -------- | ------ | ------- | --- | --- |
| svm =    | train_svm(X_train,    |       |                | y_train) |        |         |     |     |
| # Make   | an                    | array | of predictions |          | on the | test    | set |     |
| pred     | = svm.predict(X_test) |       |                |          |        |         |     |     |
# Output the hit-rate and the confusion matrix for each model
| print(svm.score(X_test,      |     |          |     | y_test))    |          |     |     |     |
| ---------------------------- | --- | -------- | --- | ----------- | -------- | --- | --- | --- |
| print(confusion_matrix(pred, |     |          |     |             | y_test)) |     |     |     |
| The output                   | of  | the code | is  | as follows: |          |     |     |     |
0.660194174757
| [[21 0 | 0 0 | 2 3  | 0   | 0 0 | 1 0 0 | 0 0 | 1 1 1 | 0 0]  |
| ------ | --- | ---- | --- | --- | ----- | --- | ----- | ----- |
| [ 0 0  | 0 0 | 0 0  | 0   | 0 0 | 0 0 0 | 0 0 | 0 0 0 | 0 0]  |
| [ 0 0  | 1 0 | 0 0  | 0   | 0 0 | 0 0 0 | 0 0 | 0 0 0 | 0 0]  |
| [ 0 0  | 0 1 | 0 0  | 0   | 0 0 | 0 0 0 | 0 0 | 0 0 0 | 0 0]  |
| [ 0 0  | 0 0 | 4 0  | 0   | 0 0 | 0 0 0 | 0 0 | 0 0 0 | 0 0]  |
| [ 0 1  | 0 0 | 1 26 | 0   | 0 0 | 1 0 1 | 0 1 | 0 0 0 | 0 0]  |
| [ 0 0  | 0 0 | 0 0  | 2   | 0 0 | 0 0 0 | 0 0 | 0 0 0 | 0 1]  |
| [ 0 0  | 0 0 | 0 0  | 0   | 1 0 | 0 0 0 | 0 0 | 0 0 0 | 0 0]  |
| [ 0 0  | 0 0 | 0 0  | 0   | 0 0 | 0 0 0 | 0 0 | 0 0 0 | 0 0]  |
| [ 0 0  | 0 0 | 1 0  | 0   | 0 0 | 3 0 0 | 0 0 | 0 0 0 | 0 0]  |
| [ 3 0  | 0 1 | 2 2  | 3   | 0 1 | 1 6 0 | 1 0 | 0 0 2 | 3 0]  |
| [ 0 0  | 0 0 | 0 0  | 0   | 0 0 | 0 0 0 | 0 0 | 0 0 0 | 0 0]  |
| [ 0 0  | 0 0 | 0 0  | 0   | 0 0 | 0 0 0 | 0 0 | 0 0 0 | 0 0]  |
| [ 0 0  | 0 0 | 0 0  | 0   | 0 0 | 0 0 0 | 0 1 | 0 0 0 | 0 0]  |
| [ 0 0  | 0 0 | 0 0  | 0   | 0 0 | 0 0 0 | 0 0 | 1 0 0 | 0 0]  |
| [ 0 0  | 0 0 | 0 0  | 0   | 0 0 | 0 0 0 | 0 0 | 0 1 0 | 0 0]  |
| [ 0 0  | 0 0 | 0 0  | 0   | 0 0 | 0 0 0 | 0 0 | 0 0 0 | 0 0]  |
| [ 0 0  | 0 0 | 0 0  | 0   | 0 0 | 0 0 0 | 0 0 | 0 0 0 | 0 0]  |
| [ 0 0  | 0 0 | 0 0  | 0   | 0 0 | 0 0 0 | 0 0 | 0 0 0 | 0 0]] |
Thus we have a 66% classi(cid:28)cation hit rate, with a confusion matrix that has entries mainly
on the diagonal (i.e. the correct assignment of class label). Notice that since we are only using a
single (cid:28)le from the Reuters set (number 000), we aren’t going to see the entire set of class labels
and hence our confusion matrix is smaller in dimension than if we had used the full dataset.
In order to make use of the full dataset we can modify the __main__ function to load all 21
Reuters(cid:28)lesandtraintheSVMonthefulldataset. Wecanoutputthefullhit-rateperformance.
I’ve neglected to include the confusion matrix output as it becomes large for the total number
of class labels within all documents. Note that this will take some time! On my system it takes
| about 30-45 | seconds                  | to          | run. |         |          |        |             |      |
| ----------- | ------------------------ | ----------- | ---- | ------- | -------- | ------ | ----------- | ---- |
| __name__    |                          | "__main__": |      |         |          |        |             |      |
| if          | ==                       |             |      |         |          |        |             |      |
| # Create    | the                      | list        | of   | Reuters | data and | create | the parser  |      |
| files       | = ["data/reut2-%03d.sgm" |             |      |         | % r      | for r  | in range(0, | 22)] |
| parser      | = ReutersParser()        |             |      |         |          |        |             |      |

183
# Parse the document and force all generated docs into
# a list so that it can be printed out to the console
docs = []
for fn in files:
for d in parser.parse(open(fn, ’rb’)):
docs.append(d)
..
..
print(svm.score(X_test, y_test))
For the full corpus, the hit rate provided is 83.6%:
0.835971855761
There are plenty of ways to improve on this (cid:28)gure. In particular we can perform a Grid
Search Cross-Validation, which is a means of determining the optimal parameters for the
classi(cid:28)er that will achieve the best hit-rate (or other metric of choice).
In later chapters we will discuss such optimisation procedures and explain how a classi(cid:28)er
suchasthiscanbeaddedtoaproductionsysteminadatascienceorquantitative(cid:28)nancecontext.
13.5 Full Code Implementation in Python 3.4.x
Here is the full code for reuters_svm.py written in Python 3.4.x:
from __future__ import print_function
import pprint
import re
try:
from html.parser import HTMLParser
except ImportError:
from HTMLParser import HTMLParser
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
class ReutersParser(HTMLParser):
"""
ReutersParser subclasses HTMLParser and is used to open the SGML
files associated with the Reuters-21578 categorised test collection.
The parser is a generator and will yield a single document at a time.
Since the data will be chunked on parsing, it is necessary to keep
some internal state of when tags have been "entered" and "exited".
Hence the in_body, in_topics and in_topic_d boolean members.
"""
def __init__(self, encoding=’latin-1’):
"""
Initialise the superclass (HTMLParser) and reset the parser.
Sets the encoding of the SGML files by default to latin-1.
"""
HTMLParser.__init__(self)

184
self._reset()
| self.encoding | = encoding |     |     |     |     |     |
| ------------- | ---------- | --- | --- | --- | --- | --- |
_reset(self):
def
"""
| This is  | called only      | on initialisation |     | of   | the parser | class |
| -------- | ---------------- | ----------------- | --- | ---- | ---------- | ----- |
| and when | a new topic-body | tuple             | has | been | generated. | It    |
resets all off the state so that a new tuple can be subsequently
generated.
"""
self.in_body
= False
self.in_topics
= False
| self.in_topic_d | = False |     |     |     |     |     |
| --------------- | ------- | --- | --- | --- | --- | --- |
| self.body       | = ""    |     |     |     |     |     |
| self.topics     | = []    |     |     |     |     |     |
| self.topic_d    | = ""    |     |     |     |     |     |
| def parse(self, | fd):    |     |     |     |     |     |
"""
| parse accepts | a file | descriptor | and | loads | the data | in chunks |
| ------------- | ------ | ---------- | --- | ----- | -------- | --------- |
in order to minimise memory usage. It then yields new documents
| as they | are parsed. |     |     |     |     |     |
| ------- | ----------- | --- | --- | --- | --- | --- |
"""
| self.docs | = []   |     |     |     |     |     |
| --------- | ------ | --- | --- | --- | --- | --- |
| for chunk | in fd: |     |     |     |     |     |
self.feed(chunk.decode(self.encoding))
| for | doc in self.docs: |     |     |     |     |     |
| --- | ----------------- | --- | --- | --- | --- | --- |
yield doc
| self.docs | = [] |     |     |     |     |     |
| --------- | ---- | --- | --- | --- | --- | --- |
self.close()
handle_starttag(self,
| def |     | tag, attrs): |     |     |     |     |
| --- | --- | ------------ | --- | --- | --- | --- |
"""
| This method | is used | to determine | what | to  | do when | the parser |
| ----------- | ------- | ------------ | ---- | --- | ------- | ---------- |
comes across a particular tag of type "tag". In this instance
we simply set the internal state booleans to True if that particular
| tag has | been found. |     |     |     |     |     |
| ------- | ----------- | --- | --- | --- | --- | --- |
"""
| if tag == | "reuters": |     |     |     |     |     |
| --------- | ---------- | --- | --- | --- | --- | --- |
pass
| elif tag | == "body": |     |     |     |     |     |
| -------- | ---------- | --- | --- | --- | --- | --- |
self.in_body
|                         | = True       |        |     |     |     |     |
| ----------------------- | ------------ | ------ | --- | --- | --- | --- |
| elif tag                | == "topics": |        |     |     |     |     |
| self.in_topics          | =            | True   |     |     |     |     |
| elif tag                | == "d":      |        |     |     |     |     |
| self.in_topic_d         |              | = True |     |     |     |     |
| def handle_endtag(self, |              | tag):  |     |     |     |     |
"""
| This method | is used           | to determine | what    | to        | do when     | the parser |
| ----------- | ----------------- | ------------ | ------- | --------- | ----------- | ---------- |
| finishes    | with a particular | tag          | of type | "tag".    |             |            |
| If the tag  | is a <REUTERS>    | tag,         | then    | we remove | all         |            |
| white-space | with a regular    | expression   |         | and       | then append | the        |
| topic-body  | tuple.            |              |         |           |             |            |

185
| If  | the tag | is a <BODY> | or  | <TOPICS> | tag then | we  | simply set |
| --- | ------- | ----------- | --- | -------- | -------- | --- | ---------- |
the internal state to False for these booleans, respectively.
If the tag is a <D> tag (found within a <TOPICS> tag), then we
| append  | the | particular | topic | to the | "topics" | list | and |
| ------- | --- | ---------- | ----- | ------ | -------- | ---- | --- |
| finally |     | reset it.  |       |        |          |      |     |
"""
| if  | tag ==            | "reuters":       |               |     |               |     |     |
| --- | ----------------- | ---------------- | ------------- | --- | ------------- | --- | --- |
|     | self.body         | = re.sub(r’\s+’, |               | r’  | ’, self.body) |     |     |
|     | self.docs.append( |                  | (self.topics, |     | self.body)    |     | )   |
self._reset()
| elif | tag            | == "body":   |         |     |     |     |     |
| ---- | -------------- | ------------ | ------- | --- | --- | --- | --- |
|      | self.in_body   | =            | False   |     |     |     |     |
| elif | tag            | == "topics": |         |     |     |     |     |
|      | self.in_topics |              | = False |     |     |     |     |
| elif | tag            | == "d":      |         |     |     |     |     |
self.in_topic_d
= False
self.topics.append(self.topic_d)
self.topic_d
|                       |     | =   | ""     |     |     |     |     |
| --------------------- | --- | --- | ------ | --- | --- | --- | --- |
| def handle_data(self, |     |     | data): |     |     |     |     |
"""
| The | data | is simply | appended | to the | appropriate |     | member state |
| --- | ---- | --------- | -------- | ------ | ----------- | --- | ------------ |
for that particular tag, up until the end closing tag appears.
"""
if self.in_body:
|      | self.body        | += data |     |     |     |     |     |
| ---- | ---------------- | ------- | --- | --- | --- | --- | --- |
| elif | self.in_topic_d: |         |     |     |     |     |     |
self.topic_d
|     |     | +=  | data |     |     |     |     |
| --- | --- | --- | ---- | --- | --- | --- | --- |
obtain_topic_tags():
def
"""
| Open   | the topic | list file    | and      | import | all of the | topic      | names |
| ------ | --------- | ------------ | -------- | ------ | ---------- | ---------- | ----- |
| taking | care      | to strip the | trailing | "\n"   | from       | each word. |       |
"""
| topics                            | = open( |     |     |     |     |     |     |
| --------------------------------- | ------- | --- | --- | --- | --- | --- | --- |
| "data/all-topics-strings.lc.txt", |         |     |     |     | "r" |     |     |
).readlines()
| topics | = [t.strip() | for | t in | topics] |     |     |     |
| ------ | ------------ | --- | ---- | ------- | --- | --- | --- |
return topics
| def filter_doc_list_through_topics(topics, |     |     |     |     | docs): |     |     |
| ------------------------------------------ | --- | --- | --- | --- | ------ | --- | --- |
"""
Reads all of the documents and creates a new list of two-tuples
that contain a single feature entry and the body text, instead of
a list of topics. It removes all geographic features and only
retains those documents which have at least one non-geographic
topic.
"""
| ref_docs | = []     |               |     |     |     |     |     |
| -------- | -------- | ------------- | --- | --- | --- | --- | --- |
| for d    | in docs: |               |     |     |     |     |     |
| if       | d[0]     | == [] or d[0] | ==  | "": |     |     |     |
continue
| for | t in | d[0]:      |     |     |     |     |     |
| --- | ---- | ---------- | --- | --- | --- | --- | --- |
|     | if t | in topics: |     |     |     |     |     |

186
d_tup = (t, d[1])
ref_docs.append(d_tup)
break
return ref_docs
def create_tfidf_training_data(docs):
"""
Creates a document corpus list (by stripping out the
class labels), then applies the TF-IDF transform to this
list.
The function returns both the class label vector (y) and
the corpus token/feature matrix (X).
"""
# Create the training data class labels
y = [d[0] for d in docs]
# Create the document corpus list
corpus = [d[1] for d in docs]
# Create the TF-IDF vectoriser and transform the corpus
vectorizer = TfidfVectorizer(min_df=1)
X = vectorizer.fit_transform(corpus)
return X, y
def train_svm(X, y):
"""
Create and train the Support Vector Machine.
"""
svm = SVC(C=1000000.0, gamma=0.0, kernel=’rbf’)
svm.fit(X, y)
return svm
if __name__ == "__main__":
# Create the list of Reuters data and create the parser
files = ["data/reut2-%03d.sgm" % r for r in range(0, 22)]
parser = ReutersParser()
# Parse the document and force all generated docs into
# a list so that it can be printed out to the console
docs = []
for fn in files:
for d in parser.parse(open(fn, ’rb’)):
docs.append(d)
# Obtain the topic tags and filter docs through it
topics = obtain_topic_tags()
ref_docs = filter_doc_list_through_topics(topics, docs)
# Vectorise and TF-IDF transform the corpus
X, y = create_tfidf_training_data(ref_docs)
# Create the training-test split of the data
X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.2, random_state=42

187
)
| # Create           | and train the | Support Vector | Machine |
| ------------------ | ------------- | -------------- | ------- |
| train_svm(X_train, |               | y_train)       |         |
svm =
| # Make | an array of predictions | on the | test set |
| ------ | ----------------------- | ------ | -------- |
pred = svm.predict(X_test)
# Output the hit-rate and the confusion matrix for each model
| print(svm.score(X_test,      |     | y_test)) |     |
| ---------------------------- | --- | -------- | --- |
| print(confusion_matrix(pred, |     | y_test)) |     |
| 13.5.1 Biblographic          |     | Notes    |     |
Originally,SVMswereinventedbyVapnik[47],whilethecurrentstandard"softmargin"approach
is due to Cortes[17]. My treatment of the material follows, and is strongly in(cid:29)uenced by, the
excellent statistical machine learning texts of James et al[32] and Hastie et al[27].

188

Part V
| Quantitative | Trading | Strategies |
| ------------ | ------- | ---------- |
189

| Chapter      |     | 14  |     |     |          |
| ------------ | --- | --- | --- | --- | -------- |
| Introduction |     |     |     | to  | QSTrader |
In this chapter I want to brie(cid:29)y introduce the QSTrader library, which will eventually be used
| for all of | the trading | strategies | outlined |      | in this book. |
| ---------- | ----------- | ---------- | -------- | ---- | ------------- |
| 14.1       | Backtesting |            | vs       | Live | Trading       |
Oneofthemostimportantmomentsinthedevelopmentofaquantitativetradingstrategyoccurs
| when a backtested |     | strategy | is (cid:28)nally | set | to trade live. |
| ----------------- | --- | -------- | ---------------- | --- | -------------- |
Unfortunately, the performance of a deployed strategy is often signi(cid:28)cantly worse than that
| of a backtested |     | system. There | are | many | reasons for this: |
| --------------- | --- | ------------- | --- | ---- | ----------------- |
(cid:136)
Transaction costs - These includes spread, fees, slippage and market impact.
(cid:136) Latency to liquidity provider - This is the time taken between issuing an order to a
| brokerage |     | and the brokerage |     | executing | it. |
| --------- | --- | ----------------- | --- | --------- | --- |
(cid:136) Market regime change - A strategy or portfolio might have behaved well in previous
market conditions, but fundamental changes to the market (such as a new regulatory
| environment) |     | reduce | the performance |     | of the strategy. |
| ------------ | --- | ------ | --------------- | --- | ---------------- |
(cid:136) Alpha decay - This describes the concept of the strategy being replicated by multiple
| users | over | time, thus | "arbitraging |     | away" the edge. |
| ----- | ---- | ---------- | ------------ | --- | --------------- |
The most common reason for signi(cid:28)cant underperformance when compared to a backtest is
due to incomplete transaction cost modelling in the backtest. Spread, slippage, fees and market
impact all contribute to reduced pro(cid:28)tability when a strategy is traded live.
In this book I want the historical backtested performance of trading strategies presented to
be as realistic as possible, in order to allow you, the reader (and potential trader), to make the
most informed decision possible as to what trading these strategies will be like.
For this reason I decided back in November 2015 to begin writing a new backtesting and
live trading engine, called QSTrader, that would attempt to mitigate these issues. I wanted
to make QSTrader freely available under a permissive open source license so that anyone could
contributetothecodebaseoruseitforwhateverpurposetheywished. Aswithmostsoftwareon
QuantStart, QSTrader is written primarily in Python, which makes it straightforwardly cross-
| platform | compatible. |     |     |     |     |
| -------- | ----------- | --- | --- | --- | --- |
QSTraderisstronglyin(cid:29)uencedbythepreviouslydevelopedQSForexsoftware,alsoavailable
under a permissive open-source license, with the exception that it will not only support the
OANDA RESTful API, but also the Interactive Brokers API via swigpy. The eventual goal is to
allow trading with Equities, ETFs and Forex all under the same portfolio framework.
The project page of QSTrader will always be available on Github at https://github.com/
mhallsmoore/qstrader. Please head there in order to study the installation instructions and
documentation.
191

192
Ultimately, QSTrader will be used for all of the trading strategies within this book. At this
stage however it is under active development both by myself and the community. As new modules
| are released, | the    | book (and      | strategies) |     | will be | updated. |
| ------------- | ------ | -------------- | ----------- | --- | ------- | -------- |
| 14.2          | Design | Considerations |             |     |         |          |
The design of QSTrader is equivalent to the type of customised algorithmic trading stack that
might be found in a small quantitative hedge fund manager. Thus, I consider the end goal of
this project to be a fully open-source, but institutional grade, production-ready portfolio and
order management system, with risk management layers across positions, portfolios and the
| infrastructure | as  | a whole. |     |     |     |     |
| -------------- | --- | -------- | --- | --- | --- | --- |
QSTrader will be end-to-end automated, meaning that minimal human intervention is neces-
sary for the system to trade once it is set "live". It is impossible to completely eliminate human
intervention, especially when it comes to input data quality, such as with erroneous ticks, but it
is certainly possible to have the system running in an automated fashion most of the time.
| 14.2.1 | Quantitative |     | Trading |     | Considerations |     |
| ------ | ------------ | --- | ------- | --- | -------------- | --- |
Thedesigncallsfortheinfrastructuretomirrorthatwhichmightbefoundinasmallquantfund
orfamilyo(cid:30)cequantarm. Itwillbehighlymodularandlooselycoupled. Themaincomponents
arethedatastore(securitiesmaster),signalgenerator,portfolio/ordermanagementsystem,risk
| layer and | brokerage | interface. |     |     |     |     |
| --------- | --------- | ---------- | --- | --- | --- | --- |
The following is a list of "institutional grade" components that the system will contain:
(cid:136)
Data Provider Integration - The (cid:28)rst major component involves interacting with a set
ofdataproviders, usuallyviasomeformofAPI.TypicalprovidersofdataincludeQuandl,
| DTN | IQFeed | and | Interactive | Brokers. |     |     |
| --- | ------ | --- | ----------- | -------- | --- | --- |
(cid:136) Data Ingestion and Cleaning-Inbetweendatastorageanddownloaditisnecessaryto
incorporate a (cid:28)ltration and cleansing layer that will only store data once it passes certain
| checks. | It  | will (cid:29)ag | "bad" | data | and note | if data is unavailable. |
| ------- | --- | --------------- | ----- | ---- | -------- | ----------------------- |
(cid:136) Pricing Data Storage - There will be a need for an intraday securities master database,
storing symbols as well as price values obtained from a brokerage or data provider.
(cid:136) Trading Data Storage - Orders, trades and portfolio states will need to be stored over
time. Object serialisation and persistence can be used for this, such as with Python’s
| pickle | library. |     |     |     |     |     |
| ------ | -------- | --- | --- | --- | --- | --- |
(cid:136)
Con(cid:28)guration Data Storage - Time-dependent con(cid:28)guration information will need to
be stored for historical reference in a database, either in tabular format or, once again, in
| pickled | format. |     |     |     |     |     |
| ------- | ------- | --- | --- | --- | --- | --- |
(cid:136)
Research/Backtesting Environment-Theresearchandbacktestingenvironmentswill
need to hook into the securities master and ultimately use the same trading logic as live
| trading | in  | order to | generate | realistic | backtests. |     |
| ------- | --- | -------- | -------- | --------- | ---------- | --- |
(cid:136)
Signal Generation - The techniques of Bayesian statistics, time series analysis and ma-
chinelearningwillbeusedwithina"signalgenerator"classtoproducetradingrecommen-
| dations | to  | our portfolio |     | engine. |     |     |
| ------- | --- | ------------- | --- | ------- | --- | --- |
(cid:136) Portfolio/Order Management - The "heart" of the system will be the portfolio and
order management system (OMS) which will receive signals from the signal generator and
use them as "recommendations" for constructing orders. The OMS will communicate
directly with the risk management component in order to determine how these orders
| should | be  | constructed. |     |     |     |     |
| ------ | --- | ------------ | --- | --- | --- | --- |

193
(cid:136)
Risk Management - The risk manager will provide a "veto" or modi(cid:28)cation mechanism
fortheOMS,suchthatsector-speci(cid:28)cweightings,leverageconstraints,brokermarginavail-
ability and average daily volume limits are kept in place. The risk layer will also provide
"umbrella hedge" situations, providing market- or sector-wide hedging capability to the
portfolio.
(cid:136)
Brokerage Interface - The brokerage interface will consist of the raw interface code
to the the broker API (in this case the C++ API of Interactive Brokers) as well as the
implementation of multiple order types such as market, limit, stop etc.
(cid:136)
Algorithmic Execution -Automated execution algorithms will eventually be developed
in order to mitigate market impact e(cid:27)ects for strategies that trade larger amounts or on
small-cap stocks.
(cid:136)
Accounting and P&L - Accounting is a tricky concept in quantitative trading. A lot of
time will be spent considering how to correctly account for PnL in a professional trading
system.
14.3 Installation
AtthisstageQSTraderisstillbeingactivelydevelopedandtheinstallationinstructionscontinue
to evolve. However, you can (cid:28)nd the latest installation process at the following URL: https:
//github.com/mhallsmoore/qstrader.

194

| Chapter     |       | 15  |        |     |         |       |          |     |
| ----------- | ----- | --- | ------ | --- | ------- | ----- | -------- | --- |
| ARIMA+GARCH |       |     |        |     | Trading |       | Strategy |     |
| on          | Stock |     | Market |     | Indexes | Using |          | R   |
In this chapter we will apply the knowledge gained in the chapters on linear time series models,
namely our understanding of ARIMA and GARCH, to a predictive trading strategy applied to
| the S&P500 | US  | Stock Market | Index. |     |     |     |     |     |
| ---------- | --- | ------------ | ------ | --- | --- | --- | --- | --- |
We will see that by combining the ARIMA and GARCH models we can signi(cid:28)cantly outper-
| form a "Buy-and-Hold" |          |     | approach | over the | long term. |     |     |     |
| --------------------- | -------- | --- | -------- | -------- | ---------- | --- | --- | --- |
| 15.1                  | Strategy |     | Overview |          |            |     |     |     |
If you’ve skipped ahead directly to the strategy section, then great, you can dive in! However,
despite the fact that the idea of the strategy is relatively simple, if you want to experiment and
improve on it I highly suggest reading the part of the book related to Time Series Analysis in
| order to | understand | what       | you would | be modifying. |        |     |     |     |
| -------- | ---------- | ---------- | --------- | ------------- | ------ | --- | --- | --- |
| The      | strategy   | is carried | out on    | a "rolling"   | basis: |     |     |     |
1. Foreachday,n,thepreviouskdaysofthedi(cid:27)erencedlogarithmicreturnsofastockmarket
index are used as a window for (cid:28)tting an optimal ARIMA and GARCH model.
2. The combined model is used to make a prediction for the next day returns.
3. If the prediction is negative the stock is shorted at the previous close, while if it is positive
| it  | is longed. |     |     |     |     |     |     |     |
| --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
4. If the prediction is the same direction as the previous day then nothing is changed.
ForthisstrategyIhaveusedthemaximumavailabledatafromYahooFinancefortheS&P500.
I have taken k = 500 but this is a parameter that can be optimised in order to improve perfor-
| mance or | reduce | drawdown. |     |     |     |     |     |     |
| -------- | ------ | --------- | --- | --- | --- | --- | --- | --- |
The backtest is carried out in a straightforward vectorised fashion using R. It has not been
implemented in an event-driven backtester, as I provided in the previous book, Successful Al-
gorithmic Trading. Hence the performance achieved in a real trading system would likely be
| slightly | less than | you might | achieve        | here, | due to commission | and slippage. |     |     |
| -------- | --------- | --------- | -------------- | ----- | ----------------- | ------------- | --- | --- |
| 15.2     | Strategy  |           | Implementation |       |                   |               |     |     |
To implement the strategy we are going to use some of the code we have previously created in
the time series analysis section as well as some new libraries including rugarch.
Iwillgothroughthesyntaxinastep-by-stepfashionandthenpresentthefullimplementation
at the end. If you have also purchased the full source version I’ve included the dataset for the
195

196
ARIMA+GARCHindicatorsoyoudon’thavetospendtimecalculatingityourself. I’veincluded
the latter because it took me a couple of days on my dekstop PC to generate the signals!
You should be able to replicate my results in entirety as the code itself is not too complex,
| although | it does          | take  | some    | time to | simulate | if you carry  | it out in full. |
| -------- | ---------------- | ----- | ------- | ------- | -------- | ------------- | --------------- |
| The      | (cid:28)rst task | is to | install | and     | import   | the necessary | libraries in R: |
> install.packages("quantmod")
> install.packages("lattice")
> install.packages("timeSeries")
> install.packages("rugarch")
| If you | already | have | the libraries |     | installed | you can | simply import them: |
| ------ | ------- | ---- | ------------- | --- | --------- | ------- | ------------------- |
> library(quantmod)
> library(lattice)
> library(timeSeries)
> library(rugarch)
With that done are going to apply the strategy to the S&P500. We can use quantmod to
obtain data going back to 1950 for the index. Yahoo Finance uses the symbol "^GPSC".
We can then create the di(cid:27)erenced logarithmic returns of the "Closing Price" of the S&P500
| and strip                                          | out | the initial           | NA                 | value: |     |     |     |
| -------------------------------------------------- | --- | --------------------- | ------------------ | ------ | --- | --- | --- |
| > getSymbols("^GSPC",                              |     |                       | from="1950-01-01") |        |     |     |     |
| > spReturns                                        |     | = diff(log(Cl(GSPC))) |                    |        |     |     |     |
| > spReturns[as.character(head(index(Cl(GSPC)),1))] |     |                       |                    |        |     |     | = 0 |
We need to create a vector, forecasts to store our forecast values on particular dates. We
setthelengthforeLengthtobeequaltothelengthoftradingdatawehaveminusk,thewindow
length:
| > windowLength |     | =                           | 500 |     |     |                    |     |
| -------------- | --- | --------------------------- | --- | --- | --- | ------------------ | --- |
| > foreLength   |     | = length(spReturns)         |     |     |     | - windowLength     |     |
| > forecasts    |     | <- vector(mode="character", |     |     |     | length=foreLength) |     |
At this stage we need to loop through every day in the trading data and (cid:28)t an appropriate
ARIMA and GARCH model to the rolling window of length k. Given that we try 24 separate
ARIMA(cid:28)tsand(cid:28)taGARCHmodel,foreachday,theindicatorcantakealongtimetogenerate.
k
We use the index d as a looping variable and loop from to the length of the trading data:
| > for | (d in | 0:foreLength) |     | {   |     |     |     |
| ----- | ----- | ------------- | --- | --- | --- | --- | --- |
We then create the rolling window by taking the S&P500 returns and selecting the values
| between | 1+d             | and k+d, | where | k                                 | =500 | for this strategy: |     |
| ------- | --------------- | -------- | ----- | --------------------------------- | ---- | ------------------ | --- |
| >       | spReturnsOffset |          | =     | spReturns[(1+d):(windowLength+d)] |      |                    |     |
We use the same procedure as in the ARIMA chapter to search through all ARMA models
| with p∈{0,...,5} |     | and | q ∈{0,...,5}, |     | with | the exception | of p,q =0. |
| ---------------- | --- | --- | ------------- | --- | ---- | ------------- | ---------- |
We wrap the arimaFit call in an R tryCatch exception handling block to ensure that if we
don’tgeta(cid:28)tforaparticularvalueofpandq,weignoreitandmoveontothenextcombination
of p and q.
Note that we set the "integrated" value of d = 0 (this is a di(cid:27)erent d to our indexing
parameter!) and as such we are really (cid:28)tting an ARMA model, rather than an ARIMA.
The looping procedure will provide us with the "best" (cid:28)tting ARMA model, in terms of the
Akaike Information Criterion, which we can then use to feed in to our GARCH model:
| >   | final.aic   | <-      | Inf         |      |         |     |     |
| --- | ----------- | ------- | ----------- | ---- | ------- | --- | --- |
| >   | final.order |         | <- c(0,0,0) |      |         |     |     |
| >   | for (p      | in 0:5) | for         | (q   | in 0:5) | {   |     |
| >   | if          | ( p     | == 0 &&     | q == | 0)      | {   |     |
| >   |             | next    |             |      |         |     |     |
| >   | }           |         |             |      |         |     |     |

197
>
> arimaFit = tryCatch( arima(spReturnsOffset, order=c(p, 0, q)),
> error=function( err ) FALSE,
> warning=function( err ) FALSE )
>
> if( !is.logical( arimaFit ) ) {
> current.aic <- AIC(arimaFit)
> if (current.aic < final.aic) {
> final.aic <- current.aic
> final.order <- c(p, 0, q)
> final.arima <- arima(spReturnsOffset, order=final.order)
> }
> } else {
> next
> }
> }
Inthenextcodeblockwearegoingtousetherugarchlibrary,withtheGARCH(1,1)model.
Thesyntaxforthisrequiresustosetupaugarchspecspeci(cid:28)cationobjectthattakesamodelfor
the variance and the mean. The variance receives the GARCH(1,1) model while the mean takes
an ARMA(p,q) model, where p and q are chosen above. We also choose the sged distribution
for the errors.
Once we have chosen the speci(cid:28)cation we carry out the actual (cid:28)tting of ARMA+GARCH
usingtheugarchfitcommand,whichtakesthespeci(cid:28)cationobject,thekreturnsoftheS&P500
andanumericaloptimisationsolver. Wehavechosentousehybrid,whichtriesdi(cid:27)erentsolvers
in order to increase the likelihood of convergence:
> spec = ugarchspec(
> variance.model=list(garchOrder=c(1,1)),
> mean.model=list(
armaOrder=c(
final.order[1],
final.order[3]
), include.mean=T
),
> distribution.model="sged")
>
> fit = tryCatch(
> ugarchfit(
> spec, spReturnsOffset, solver = ’hybrid’
> ), error=function(e) e, warning=function(w) w
> )
If the GARCH model does not converge then we simply set the day to produce a "long"
prediction, which is clearly a guess. However, if the model does converge then we output the
date and tomorrow’s prediction direction (+1 or -1) as a string at which point the loop is closed
o(cid:27).
In order to prepare the output for the CSV (cid:28)le I have created a string that contains the data
separated by a comma with the forecast direction for the subsequent day:
> if(is(fit, "warning")) {
> forecasts[d+1] = paste(
index(spReturnsOffset[windowLength]), 1, sep=","
)
> print(
paste(
index(spReturnsOffset[windowLength]), 1, sep=","
)

198
)
| >   | } else         | {                         |                     |               |     |            |        |             |     |
| --- | -------------- | ------------------------- | ------------------- | ------------- | --- | ---------- | ------ | ----------- | --- |
| >   | fore           | =                         | ugarchforecast(fit, |               |     | n.ahead=1) |        |             |     |
| >   | ind            | = fore@forecast$seriesFor |                     |               |     |            |        |             |     |
| >   | forecasts[d+1] |                           |                     | = paste(      |     |            |        |             |     |
|     |                | colnames(ind),            |                     | ifelse(ind[1] |     | <          | 0, -1, | 1), sep="," |     |
)
| >   | print( |                      |     |     |               |     |     |            |          |
| --- | ------ | -------------------- | --- | --- | ------------- | --- | --- | ---------- | -------- |
|     |        | paste(colnames(ind), |     |     | ifelse(ind[1] |     | <   | 0, -1, 1), | sep=",") |
)
> }
> }
The penultimate step is to output the CSV (cid:28)le to disk. This allows us to take the indicator
and use it in alternative backtesting software for further analysis, if so desired:
> write.csv(forecasts, file="forecasts.csv", row.names=FALSE)
However, there is a small problem with the CSV (cid:28)le as it stands right now. The (cid:28)le contains
alistofdatesandapredictionfortomorrow’s direction. Ifweweretoloadthisintothebacktest
codebelowasitstands,wewouldactuallybeintroducingalook-aheadbiasbecausetheprediction
| value | would | represent | data | not known |     | at the time | of the | prediction. |     |
| ----- | ----- | --------- | ---- | --------- | --- | ----------- | ------ | ----------- | --- |
In order to account for this we simply need to move the predicted value one day ahead. I
have found this to be more straightforward using Python. To keep things simple, I’ve kept it to
| pure Python, |     | by not | using | any special |     | libraries. |     |     |     |
| ------------ | --- | ------ | ----- | ----------- | --- | ---------- | --- | --- | --- |
Here is the short script that carries this procedure out. Make sure to run it in the same
| directory   | as        | the forecasts.csv |                              |      | (cid:28)le: |                  |            |           |     |
| ----------- | --------- | ----------------- | ---------------------------- | ---- | ----------- | ---------------- | ---------- | --------- | --- |
| if __name__ |           | ==                | "__main__":                  |      |             |                  |            |           |     |
| #           | Open      | the               | forecasts                    | CSV  | file        | and read         | in         | the lines |     |
| forecasts   |           | =                 | open("forecasts.csv",        |      |             | "r").readlines() |            |           |     |
| #           | Run       | through           | the                          | list | and lag     | the forecasts    |            | by one    |     |
| old_value   |           | =                 | 1                            |      |             |                  |            |           |     |
| new_list    |           | =                 | []                           |      |             |                  |            |           |     |
| for         | f         | in forecasts[1:]: |                              |      |             |                  |            |           |     |
|             | strpf     | =                 | f.replace(’"’,’’).strip()    |      |             |                  |            |           |     |
|             | new_str   |                   |                              |      |             | old_value)       |            |           |     |
|             |           |                   | = "%s,%s\n"                  |      | % (strpf,   |                  |            |           |     |
|             | newspl    |                   | = new_str.strip().split(",") |      |             |                  |            |           |     |
|             | final_str |                   | = "%s,%s\n"                  |      | %           | (newspl[0],      | newspl[2]) |           |     |
|             | final_str |                   | final_str.replace(’"’,’’)    |      |             |                  |            |           |     |
=
|     | old_value |     | = f.strip().split(’,’)[1] |     |     |     |     |     |     |
| --- | --------- | --- | ------------------------- | --- | --- | --- | --- | --- | --- |
new_list.append(final_str)
| #   | Output | the | updated | forecasts |     | CSV file |     |     |     |
| --- | ------ | --- | ------- | --------- | --- | -------- | --- | --- | --- |
open("forecasts_new.csv",
| out | =   |              |     |     |     | "w") |     |     |     |
| --- | --- | ------------ | --- | --- | --- | ---- | --- | --- | --- |
| for | n   | in new_list: |     |     |     |      |     |     |     |
out.write(n)
At this point we now have the corrected indicator (cid:28)le stored in forecasts_new.csv. If you
purchased the book+source option you will (cid:28)nd the (cid:28)le in the appropriate directory in the zip
package.
| 15.3 | Strategy |     | Results |     |     |     |     |     |     |
| ---- | -------- | --- | ------- | --- | --- | --- | --- | --- | --- |
NowthatwehavegeneratedourindicatorCSV(cid:28)leweneedtocompareitsperformanceto"Buy
& Hold".
We (cid:28)rstly read in the indicator from the CSV (cid:28)le and store it as spArimaGarch:

199
| > spArimaGarch |     | =   | as.xts( |     |     |     |     |
| -------------- | --- | --- | ------- | --- | --- | --- | --- |
> read.zoo(
> file="forecasts_new.csv", format="%Y-%m-%d", header=F, sep=","
> )
> )
WethencreateanintersectionofthedatesfortheARIMA+GARCHforecastsandtheoriginal
set of returns from the S&P500. We can then calculate the returns for the ARIMA+GARCH
| strategy              | by multiplying |          | the forecast      |                 | sign (+ or | -) with the return | itself: |
| --------------------- | -------------- | -------- | ----------------- | --------------- | ---------- | ------------------ | ------- |
| > spIntersect         |                | = merge( | spArimaGarch[,1], |                 |            | spReturns,         | all=F ) |
| > spArimaGarchReturns |                |          | =                 | spIntersect[,1] |            | spIntersect[,2]    |         |
*
Once we have the returns from the ARIMA+GARCH strategy we can create equity curves
forboththeARIMA+GARCHmodeland"Buy&Hold". Finally,wecombinethemintoasingle
data structure:
> spArimaGarchCurve = log( cumprod( 1 + spArimaGarchReturns ) )
| > spBuyHoldCurve |     |     | = log( | cumprod( | 1 + | spIntersect[,2] | ) ) |
| ---------------- | --- | --- | ------ | -------- | --- | --------------- | --- |
> spCombinedCurve = merge( spArimaGarchCurve, spBuyHoldCurve, all=F )
Finally, we can use the xyplot command to plot both equity curves on the same plot:
> xyplot(
> spCombinedCurve,
> superpose=T,
| > col=c("darkred", |     |     | "darkblue"), |     |     |     |     |
| ------------------ | --- | --- | ------------ | --- | --- | --- | --- |
> lwd=2,
> key=list(
> text=list(
| >   | c("ARIMA+GARCH", |     |     | "Buy | & Hold") |     |     |
| --- | ---------------- | --- | --- | ---- | -------- | --- | --- |
> ),
> lines=list(
| >   | lwd=2, | col=c("darkred", |     |     | "darkblue") |     |     |
| --- | ------ | ---------------- | --- | --- | ----------- | --- | --- |
> )
> )
> )
| The | equity | curve | up to 6th | October | 2015 | is given in Figure | 15.1: |
| --- | ------ | ----- | --------- | ------- | ---- | ------------------ | ----- |
Asyoucansee,overa65yearperiod,theARIMA+GARCHstrategyhassigni(cid:28)cantlyoutper-
formed "Buy & Hold". However, you can also see that the majority of the gain occured between
1970 and 1980. Notice that the volatility of the curve is quite minimal until the early 80s, at
which point the volatility increases signi(cid:28)cantly and the average returns are less impressive.
Clearly the equity curve promises great performance over the whole period. However, would
| this strategy | really | have | been | tradeable? |     |     |     |
| ------------- | ------ | ---- | ---- | ---------- | --- | --- | --- |
First of all, let’s consider the fact that the ARMA model was only published in 1951. It
wasn’t really widely utilised until the 1970’s when Box & Jenkins[12] discussed it in their book.
Secondly, the ARCH model wasn’t discovered (publicly!) until the early 80s, by Engle[21],
| and GARCH | itself | was | published | by  | Bollerslev[11] | in 1986. |     |
| --------- | ------ | --- | --------- | --- | -------------- | -------- | --- |
Thirdly, this "backtest" has actually been carried out on a stock market index and not a
physically tradeable instrument. In order to gain access to an index such as this it would have
been necessary to trade S&P500 futures or a replica Exchange Traded Fund (ETF) such as
SPDR.
Hence is it really that appropriate to apply such models to a historical series prior to their
invention? An alternative is to begin applying the models to more recent data. In fact, we can
consider the performance in the last ten years, from Jan 1st 2005 to today in Figure 15.2.
AsyoucanseetheequitycurveremainsbelowaBuy&Holdstrategyforalmostthreeyears,
but during the stock market crash of 2008/2009 it does exceedingly well. This makes sense

200
Figure 15.1: Equity curve of ARIMA+GARCH strategy vs "Buy & Hold" for the S&P500 from
1952
Figure 15.2: Equity curve of ARIMA+GARCH strategy vs "Buy & Hold" for the S&P500 from
2005 until today
because there is likely to be a signi(cid:28)cant serial correlation in this period and it will be well-
captured by the ARIMA and GARCH models. Once the market recovered post-2009 and enters
what looks to be more a stochastic trend, the model performance begins to su(cid:27)er once again.

201
Note that this strategy can be easily applied to di(cid:27)erent stock market indices, equities or
other asset classes. I strongly encourage you to try researching other instruments, as you may
obtain substantial improvements on the results presented here.
15.4 Full Code
Here is the full listing for the indicator generation, backtesting and plotting:
# Import the necessary libraries
library(quantmod)
library(lattice)
library(timeSeries)
library(rugarch)
# Obtain the S&P500 returns and truncate the NA value
getSymbols("^GSPC", from="1950-01-01")
spReturns = diff(log(Cl(GSPC)))
spReturns[as.character(head(index(Cl(GSPC)),1))] = 0
# Create the forecasts vector to store the predictions
windowLength = 500
foreLength = length(spReturns) - windowLength
forecasts <- vector(mode="character", length=foreLength)
for (d in 0:foreLength) {
# Obtain the S&P500 rolling window for this day
spReturnsOffset = spReturns[(1+d):(windowLength+d)]
# Fit the ARIMA model
final.aic <- Inf
final.order <- c(0,0,0)
for (p in 0:5) for (q in 0:5) {
if ( p == 0 && q == 0) {
next
}
arimaFit = tryCatch( arima(spReturnsOffset, order=c(p, 0, q)),
error=function( err ) FALSE,
warning=function( err ) FALSE )
if( !is.logical( arimaFit ) ) {
current.aic <- AIC(arimaFit)
if (current.aic < final.aic) {
final.aic <- current.aic
final.order <- c(p, 0, q)
final.arima <- arima(spReturnsOffset, order=final.order)
}
} else {
next
}
}
# Specify and fit the GARCH model
spec = ugarchspec(
variance.model=list(garchOrder=c(1,1)),
mean.model=list(armaOrder=c(

202
|     |     | final.order[1], |     |     | final.order[3] |     |     |     |     |
| --- | --- | --------------- | --- | --- | -------------- | --- | --- | --- | --- |
), include.mean=T),
distribution.model="sged"
)
|     | fit = | tryCatch( |     |     |     |     |     |     |     |
| --- | ----- | --------- | --- | --- | --- | --- | --- | --- | --- |
ugarchfit(
|     | spec, |                   | spReturnsOffset, |     | solver                 | =   | ’hybrid’ |     |     |
| --- | ----- | ----------------- | ---------------- | --- | ---------------------- | --- | -------- | --- | --- |
|     | ),    | error=function(e) |                  |     | e, warning=function(w) |     |          | w   |     |
)
# If the GARCH model does not converge, set the direction to "long" else
# choose the correct forecast direction based on the returns prediction
|     | # Output                              | the | results     |          | to the screen |     | and the | forecasts  | vector |
| --- | ------------------------------------- | --- | ----------- | -------- | ------------- | --- | ------- | ---------- | ------ |
|     | if(is(fit,                            |     | "warning")) |          | {             |     |         |            |        |
|     | forecasts[d+1]                        |     |             | = paste( |               |     |         |            |        |
|     | index(spReturnsOffset[windowLength]), |     |             |          |               |     |         | 1, sep="," |        |
)
print(
paste(
|     |     | index(spReturnsOffset[windowLength]), |     |     |     |     |     | 1, sep="," |     |
| --- | --- | ------------------------------------- | --- | --- | --- | --- | --- | ---------- | --- |
)
)
|     | } else         | {                         |     |               |            |     |        |             |     |
| --- | -------------- | ------------------------- | --- | ------------- | ---------- | --- | ------ | ----------- | --- |
|     | fore           | = ugarchforecast(fit,     |     |               | n.ahead=1) |     |        |             |     |
|     | ind            | = fore@forecast$seriesFor |     |               |            |     |        |             |     |
|     | forecasts[d+1] |                           |     | = paste(      |            |     |        |             |     |
|     | colnames(ind), |                           |     | ifelse(ind[1] |            | <   | 0, -1, | 1), sep="," |     |
)
print(paste(colnames(ind), ifelse(ind[1] < 0, -1, 1), sep=","))
}
}
| # Output |     | the CSV | file | to  | "forecasts.csv" |     |     |     |     |
| -------- | --- | ------- | ---- | --- | --------------- | --- | --- | --- | --- |
file="forecasts.csv",
| write.csv(forecasts, |     |                |         |     |          |       | row.names=FALSE) |     |     |
| -------------------- | --- | -------------- | ------- | --- | -------- | ----- | ---------------- | --- | --- |
| # Input              | the | Python-refined |         |     | CSV file | AFTER | CONVERSION       |     |     |
| spArimaGarch         |     | =              | as.xts( |     |          |       |                  |     |     |
read.zoo(
file="forecasts_new.csv", format="%Y-%m-%d", header=F, sep=","
)
)
| # Create            |     | the ARIMA+GARCH |        |                   | returns     |     |                 |        |     |
| ------------------- | --- | --------------- | ------ | ----------------- | ----------- | --- | --------------- | ------ | --- |
| spIntersect         |     | =               | merge( | spArimaGarch[,1], |             |     | spReturns,      | all=F  | )   |
| spArimaGarchReturns |     |                 |        | = spIntersect[,1] |             | *   | spIntersect[,2] |        |     |
| # Create            |     | the backtests   |        | for               | ARIMA+GARCH |     | and Buy         | & Hold |     |
spArimaGarchCurve = log( cumprod( 1 + spArimaGarchReturns ) )
| spBuyHoldCurve |     |     | = log( | cumprod( | 1 + | spIntersect[,2] |     | ) ) |     |
| -------------- | --- | --- | ------ | -------- | --- | --------------- | --- | --- | --- |
spCombinedCurve = merge( spArimaGarchCurve, spBuyHoldCurve, all=F )
| # Plot | the | equity | curves |     |     |     |     |     |     |
| ------ | --- | ------ | ------ | --- | --- | --- | --- | --- | --- |
xyplot(
spCombinedCurve,
superpose=T,
| col=c("darkred", |     |     | "darkblue"), |     |     |     |     |     |     |
| ---------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- |

203
lwd=2,
key=list(
text=list(
| c("ARIMA+GARCH", |     | "Buy | & Hold") |     |     |     |
| ---------------- | --- | ---- | -------- | --- | --- | --- |
),
lines=list(
| lwd=2, | col=c("darkred", |     | "darkblue") |     |     |     |
| ------ | ---------------- | --- | ----------- | --- | --- | --- |
)
)
)
| And the Python | code to                 | apply | to forecasts.csv |                  | before | reimporting: |
| -------------- | ----------------------- | ----- | ---------------- | ---------------- | ------ | ------------ |
| if __name__    | == "__main__":          |       |                  |                  |        |              |
| # Open         | the forecasts           | CSV   | file             | and read         | in     | the lines    |
| forecasts      | = open("forecasts.csv", |       |                  | "r").readlines() |        |              |
| # Run through  | the                     | list  | and lag          | the forecasts    |        | by one       |
| old_value      | = 1                     |       |                  |                  |        |              |
new_list
= []
| for f in | forecasts[1:]:               |     |           |            |     |     |
| -------- | ---------------------------- | --- | --------- | ---------- | --- | --- |
| strpf    | = f.replace(’"’,’’).strip()  |     |           |            |     |     |
| new_str  |                              |     |           | old_value) |     |     |
|          | = "%s,%s\n"                  |     | % (strpf, |            |     |     |
| newspl   | = new_str.strip().split(",") |     |           |            |     |     |
final_str
|           | = "%s,%s\n"                 |     | %   | (newspl[0], | newspl[2]) |     |
| --------- | --------------------------- | --- | --- | ----------- | ---------- | --- |
| final_str | = final_str.replace(’"’,’’) |     |     |             |            |     |
| old_value | = f.strip().split(’,’)[1]   |     |     |             |            |     |
new_list.append(final_str)
| # Output                        | the updated | forecasts |     | CSV file |     |     |
| ------------------------------- | ----------- | --------- | --- | -------- | --- | --- |
| out = open("forecasts_new.csv", |             |           |     | "w")     |     |     |
| for n in                        | new_list:   |           |     |          |     |     |
out.write(n)

204

Bibliography
[1] Wikipedia: Standard generalized markup language. http://en.wikipedia.org/wiki/
Standard_Generalized_Markup_Language, 2015.
[2] Pymc3: Probabilistic programming in python. https://github.com/pymc-devs/pymc3,
2016.
[3] Python htmlparser. https://docs.python.org/2/library/htmlparser.html, 2016.
[4] Scikit-learn: Support vector machines. http://scikit-learn.org/stable/modules/
svm.html, 2016.
[5] Wikibooks: Support vector machines. https://en.wikibooks.org/wiki/Support_
Vector_Machines, 2016.
[6] Wikipedia: Term frequency-inverse document frequency. http://en.wikipedia.org/
wiki/Tf%E2%80%93idf, 2016.
[7] Arnold, G. Financial Times Guide to the Financial Markets. Financial Times/Prentice
Hall, 2011.
[8] Barber, D. Bayesian Reasoning and Machine Learning. Cambridge University Press, 2012.
[9] Bird,S.,Klein,E.,andLoper,E. NaturalLanguageProcessingwithPython. O’ReillyMedia,
2009.
[10] Bollen, J., Mao, H., and Zeng, X. Twitter mood predicts the stock market. CoRR,
abs/1010.3003, 2010.
[11] Bollerslev, T. Generalized autoregressive conditional heteroskedasticity. Journal of Econo-
metrics, 31(3):307(cid:21)327, 1986.
[12] Box, G., Jenkins, G., Reinsel, G., and Ljung, G. Time Series Analysis: Forecasting and
Control, 5th Ed. Wiley-Blackwell, 2015.
[13] Brockwell, P. and Davis, R. Time Series: Theory and Methods. Springer, 2009.
[14] Chan, E. P. Quantitative Trading: How to Build Your Own Algorithmic Trading Business.
John Wiley & Sons, 2009.
[15] Chan, E. P. Algorithmic Trading: Winning Strategies And Their Rationale. John Wiley &
Sons, 2013.
[16] Chang, C. and Lin, C. Libsvm: A library for support vector machines. http://www.csie.
ntu.edu.tw/~cjlin/papers/libsvm.pdf, 2013.
[17] Cortes, C. and Vapnik, V. Support vector networks. Machine Learning, 20(3):273, 1995.
[18] Cowpertwait, P. and Metcalfe, A. Introductory Time Series with R. Springer, 2009.
[19] Davidson-Pilon, C. Probabilistic Programming & Bayesian Methods for Hackers, 2016.
[20] Duane, S. and et al. Hybrid monte carlo. Physics Letters B, 195(2):216(cid:21)222, 1987.
205

206
[21] Engle, R. F. Autoregressive conditional heteroscedasticity with estimates of the variance of
| united | kingdom | in(cid:29)ation. | Econometrica, |     | 50(4):987(cid:21)1007, |     | 1982. |
| ------ | ------- | ---------------- | ------------- | --- | ---------------------- | --- | ----- |
[22] Gelfand, A. E. and Smith, A. F. M. Sampling-based approaches to calculating marginal
| densities. | J. Amer. |     | Statist. Assoc., |     | 85(140):398(cid:21)409, |     | 1990. |
| ---------- | -------- | --- | ---------------- | --- | ----------------------- | --- | ----- |
[23] Gelman, A., Carlin, J., Stern, H., Dunson, D., Vehtari, A., and Rubin, D. Bayesian Data
| Analysis, | 3rd | Ed. Chapman | and | Hall/CRC, | 2013. |     |     |
| --------- | --- | ----------- | --- | --------- | ----- | --- | --- |
[24] Geman, S. and Geman, D. Stochastic relaxation, gibbs distributions and the bayesian
restoration of images. IEEE Trans. Pattern Anal. Mach. Intell., 6:721(cid:21)741, 1984.
[25] Hamada, M., Wilson, A., Reese, C. S., and Martz, H. Bayesian Reliability. Springer, 2008.
[26] Harris, L. Trading and Exchanges: Market Microstructure for Practitioners. Oxford Uni-
| versity | Press, | 2002. |     |     |     |     |     |
| ------- | ------ | ----- | --- | --- | --- | --- | --- |
[27] Hastie, T., Tibshirani, R., and Friedman, J. The Elements of Statistical Learning: Data
| Mining, | Inference | and | Prediction, | 2nd | Ed. Springer, |     | 2011. |
| ------- | --------- | --- | ----------- | --- | ------------- | --- | ----- |
[28] Hastings, W. Monte carlo sampling methods using markov chains and their applications.
| Biometrika, | 57:97(cid:21)109, |     | 1970. |     |     |     |     |
| ----------- | ----------------- | --- | ----- | --- | --- | --- | --- |
[29] Ho(cid:27)man, M. D. and Gelman, A. The no-u-turn sampler: Adaptively setting path lengths
| in hamiltonian |     | monte | carlo. |     |     |     |     |
| -------------- | --- | ----- | ------ | --- | --- | --- | --- |
[30] Hyndman,R.J.andKhandakar,Y. Automatictimeseriesforecasting: theforecastpackage
| for R. Journal |     | of Statistical | Software, |     | 26(3):1(cid:21)22, | 2008. |     |
| -------------- | --- | -------------- | --------- | --- | ------------------ | ----- | --- |
[31] Hyndman, R. J. forecast: Forecasting functions for time series and linear models, 2015. R
| package | version | 6.2. |     |     |     |     |     |
| ------- | ------- | ---- | --- | --- | --- | --- | --- |
[32] James,G.,Witten,D.,Hastie,T.,andTibshirani,R.AnIntroductiontoStatisticalLearning:
| with applications |     | in  | R. Springer, | 2013. |     |     |     |
| ----------------- | --- | --- | ------------ | ----- | --- | --- | --- |
[33] Johnson,B.AlgorithmicTrading&DMA:Anintroductiontodirectaccesstradingstrategies.
| 4Myeloma | Press, | 2010. |     |     |     |     |     |
| -------- | ------ | ----- | --- | --- | --- | --- | --- |
[34] Kruschke, J. Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan, 2nd Ed.
| Academic       | Press, | 2015.  |          |           |          |        |       |
| -------------- | ------ | ------ | -------- | --------- | -------- | ------ | ----- |
| [35] McKinney, | W.     | Python | for Data | Analysis. | O’Reilly | Media, | 2012. |
[36] Metropolis, N. and et al. Equations of state calculations by fast computing machines. J.
| Chem. | Phys., | 21:1087(cid:21)1092, | 1953. |     |     |     |     |
| ----- | ------ | -------------------- | ----- | --- | --- | --- | --- |
[37] Narang, R. K. Inside The Black Box: The Simple Truth About Quantitative and High-
| Frequency | Trading, |     | 2nd Ed. John | Wiley | & Sons, | 2013. |     |
| --------- | -------- | --- | ------------ | ----- | ------- | ----- | --- |
[38] Pardo, R. The Evaluation and Optimization of Trading Strategies, 2nd Ed. John Wiley &
| Sons, 2008. |     |     |     |     |     |     |     |
| ----------- | --- | --- | --- | --- | --- | --- | --- |
[39] Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel,
M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D.,
Brucher, M., Perrot, M., and Duchesnay, E. Scikit-learn: Machine learning in Python.
| Journal | of Machine |     | Learning | Research, | 12:2825(cid:21)2830, |     | 2011. |
| ------- | ---------- | --- | -------- | --------- | -------------------- | --- | ----- |
[40] Pole,A.,West,M.,andHarrison,J.AppliedBayesianForecastingandTimeSeriesAnalysis,
| 2nd Ed. | Chapman |     | and Hall/CRC, | 2011. |     |     |     |
| ------- | ------- | --- | ------------- | ----- | --- | --- | --- |
[41] Robert, C. and Casella, G. A short history of markov chain monte carlo: Subjective recol-
| lections | from | incomplete | data. | Statistical | Science, | 0(00):1(cid:21)14, | 2011. |
| -------- | ---- | ---------- | ----- | ----------- | -------- | ------------------ | ----- |

207
| [42] Russell, | M. A. 21     | Recipes for Mining | Twitter. O’Reilly | Media, 2011.          |
| ------------- | ------------ | ------------------ | ----------------- | --------------------- |
| [43] Russell, | M. A. Mining | the Social         | Web, 2nd Ed.      | O’Reilly Media, 2013. |
| [44] Sedar,   | J. Bayesian  | inference          | with pymc3        | - part 1.             |
http://blog.applied.ai/
| bayesian-inference-with-pymc3-part-1/, |               |          |                    | 2016.         |
| -------------------------------------- | ------------- | -------- | ------------------ | ------------- |
| [45] Sinclair,                         | E. Volatility | Trading, | 2nd Ed. John Wiley | & Sons, 2013. |
[46] Tsay, R. Analysis of Financial Time Series, 3rd Ed. Wiley-Blackwell, 2010.
[47] Vapnik, V. The Nature of Statistical Learning Theory. Springer, 1996.
[48] Wiecki,T. Theinferencebutton: Bayesianglmsmadeeasywithpymc3. http://twiecki.
| github.io/blog/2013/08/12/bayesian-glms-1/, |     |     |     | 2013. |
| ------------------------------------------- | --- | --- | --- | ----- |
[49] Wiecki, T. This world is far from normal(ly distributed): Bayesian robust regression in
pymc3. http://twiecki.github.io/blog/2013/08/27/bayesian-glms-2/, 2013.
[50] Wiecki, T. Mcmc sampling for dummies. http://twiecki.github.io/blog/2015/11/
| 10/mcmc-sampling/, |     | 2015. |     |     |
| ------------------ | --- | ----- | --- | --- |
[51] Wilmott, P. Paul Wilmott Introduces Quantitative Finance, 2nd Ed. John Wiley & Sons,
2007.
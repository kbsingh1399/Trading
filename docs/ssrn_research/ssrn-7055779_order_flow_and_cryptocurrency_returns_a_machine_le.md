# Order Flow and Cryptocurrency Returns: A Machine Learning

- **Source File**: `ssrn-7055779 (1).pdf`
- **Total Pages**: 27
- **SSRN ID**: `ssrn-7055779`

---

## Page 1

   Order Flow and Cryptocurrency Returns: A Machine Learning 
Approach with Out-of-Sample Validation 
 Abstract 
The results indicate that overall order flow plays a significant role in explaining variations in 
cryptocurrency returns. Using machine learning for out-of-sample predictions, we demonstrate 
that order flow is an effective predictor of daily cryptocurrency returns. Portfolio strategies that 
rely on machine-learning forecasts based on daily order flow achieve an alpha of up to 0.86% 
per day and a Sharpe ratio of 3.97 annually. Order flow outperforms economic fundamentals 
in predicting returns, especially when nonlinear machine learning models conditioned on order 
flow are used, demonstrating strong out-of-sample predictive power beyond arbitrage limits. 
In addition to statistical analysis, we assess the economic value of conditioning on order flow 
through portfolio sorting. Overall, our findings suggest that order flow consistently influences 
cryptocurrency returns.  
 
Keyboards: Order flows, cryptocurrency returns, machine learning techniques, and out-of-
sample.  
1. Introduction 
The cryptocurrency market has experienced rapid expansion over the past decade, with market 
capitalisation rising from $428.60 billion in 2018 to $ 3,257.43 trillion in 2025, and daily 
trading volume increasing from $160 million to $415 billion USD in 2025. Unlike traditional 
foreign exchange markets, which are dominated by a few major dealers [22], the crypto market 
features independently operated, non-integrated exchanges that operate across various 
countries and currencies [21]. Despite its growth, the market remains illiquid and faces 
considerable information asymmetry compared to conventional financial markets [3]. These 
unique qualities position crypto markets as a fresh domain for studying how order flow 
influences price formation.  
Order flow indicates the total buy and sell volumes and greatly influences price, liquidity, and 
volatility. [6] highlight order flow as the immediate factor affecting price in almost all 
microstructure analyses, underscoring its importance for understanding short-term market 
behaviour. It measures the net load of a cryptocurrency by calculating the natural-log difference 
between buyer- and seller-initiated transaction volumes, denominated in the relevant fiat 
currency over a specified period. The link between order flow and cryptocurrency returns is 
driven primarily by economic indicators rather than by order flow itself, supporting the “no-
predictability view” and the null hypothesis we examine. Since order flow is believed to have 
only a temporary effect on crypto returns, it is seen as a transitory phenomenon, a view known 
as the “transitory view” [12, 22]. In contrast, order flow also reflects the integration of future 
economic information into cryptocurrency returns through price discovery, often referred to as 
the "permanent view" [6, 7, 22].   
The analysis of order flow also examines how various events in the order book influence future 
price changes. Modelling order flow and its market impact is crucial in finance for 
understanding how private information is reflected in prices and for creating profitable trading 
strategies. In cryptocurrency markets, order flow has a temporary effect on returns, but this 
influence doesn't last long. Microstructure research examines how these short-term effects 


## Page 2

relate to shifts in liquidity, inflationary trends, and short-term shocks to preferences. In-sample 
data show that global order flows are the strongest predictor of cross-sectional crypto returns, 
with a positive correlation. These flows, along with control variables, explain about 15-22% of 
the variation in returns. The regression emphasises the importance of distinguishing between 
short-lived, transient order-flow components and longer-term, persistent ones. Following [3], 
lagged returns are used as proxies for short-term reversals. Analyses with lagged order flow 
and past crypto returns reveal that a significant portion of lagged flow, even when uncorrelated 
with past returns, still strongly predicts future returns. The positive relationship between global 
order flow and daily or weekly crypto returns supports the idea that order-flow effects are 
persistent. Panel regressions show that the most influential coefficient among all global order 
flows is from these flows. When global order flow is included in regressions, U.S. order flow 
remains highly significant, though its effect diminishes. Overall, these results suggest that 
global order flows are more active and are better predictors than individual flow components. 
Out-of-sample forecasting of typical cryptocurrency returns using order flow employs machine 
learning (ML) techniques for variable selection and dimensionality reduction, accommodating 
a large number of indicators and many usable forms. Machine learning-based forecasting 
allows us to incorporate global order flows and other economic indicators to predict the next 
day's cryptocurrency returns.  
The estimation of the linear and the nonlinear ML techniques, including ridge regression (RR), 
Lasso (AS), elastic net (EN), principal component regression (PCR), and random forest (RF), 
stochastic gradient boosted regression trees (SGB), as well as the neural networks comprising 
1-4 hidden layers (NN1-NN4) along with the varied forest combinations spanning several 
linear models (L-Avg) and also the non-linear models (NL-Avg), as the out-of-sample ML 
forecasting is only carried out for the regular returns. Regarding out-of-sample performance, 
the non-linear ML forecasts, conditioned on all order flows, consistently surpass the linear 
models conditioned on all order flows, as well as the linear and non-linear models based on the 
economic indicators and the zero-forecast benchmark. From amongst these, the standard 
gradient boosted regression model (SGB) that conditions on almost all the order flows with 
𝑅2 of 0.41%. The non-linear ML techniques that condition on order flow display significant 
out-of-sample predictive ability. 
2. Research Literature 
This study advances the growing cryptocurrency literature by analysing the information 
entropy of order flow to assess and predict cryptocurrency returns. We examine three main 
questions: whether order flow can explain cross-sectional cryptocurrency returns, if it provides 
predictive insights, and whether key information in international order flows is missing from 
US order flow data. Addressing these questions is essential to understanding market 
microstructure and supports broader research into the economic factors that shape order flow 
and price discovery in cryptocurrency markets. While these questions have been answered in 
traditional financial markets, they remain open in the cryptocurrency context. By replicating 
the information contained in order flow within the cryptocurrency market, this paper fills a gap 
in existing research. Several studies have shown empirical evidence of order flow's impact on 
physical currency exchange rates. We primarily focus on the out-of-sample test, which 
provides the most in-depth evidence about the asset return predictability [27, 29]. Very few 
studies analyse out-of-sample cryptocurrency return prediction; for example, [7,6,15] use 
various technical indicators to predict daily and weekly Bitcoin returns, whereas others predict 


## Page 3

daily Bitcoin returns using several predictors. We also extend the existing cryptocurrency 
returns literature by exploring the out-of-sample predictability of daily cryptocurrency returns, 
applying a broad range of predictors and a wide variety of machine learning techniques. The 
daily cryptocurrency return forecasts are generated using various machine-learning methods, 
including elastic net [32] and linear model estimation that includes almost all indicators 
(Linear-ENet forecast). Conventional Ordinary Least Squares (C-OLS) estimates a large-scale 
linear model using correlated economic indicators, leading to in-sample overfitting. The ENet 
refers to an extension of the seminal least absolute shrinkage and selection operator [29], 
helping to mitigate overfitting by using penalised (Lasso) regression to shrink coefficient 
estimates to near zero. [6, 7] develop a theoretical model of order flow, confirming that it 
significantly influences the Deutschmark/dollar market, where order flow explains at least 50% 
of exchange-rate variation and yields residuals that outperform the random-walk benchmark. 
[2] Use high-frequency intraday data to find a strong positive relationship between order flows 
and crypto returns across time horizons ranging from 1 minute to 1 day. [22] prioritise fiat 
currencies and evaluate the breakdown of foreign exchange customer segments by order flow, 
suggesting that order flow contains important forecast information, though the degree of 
uniformity varies across end-user foreign exchange markets. The literature on market 
microstructure links transitory market effects to variations in liquidity, price impact, and 
temporary preference shocks [12, 22]. Several studies based on market microstructure correlate 
permanent effects with asymmetric information among market participants, such that 
transactions convey information and have a consistent effect on security prices [13, 18, 15, & 
16]. Crypto trades convey information about future economic indicators that is unknown to all 
market participants, and order flow then serves as the primary vehicle for spreading this 
information about cryptocurrency returns through the price discovery process [6, 7, 22]. 
Several papers assess the out-of-sample predictive power of order flow for daily crypto returns 
using machine learning (ML) techniques [14, 6,10, 13]. [2] Analyse the profitability of machine 
learning models under economic constraints, such as short-selling limitations, transaction 
costs, and limits on speculators' risk-taking capacity.  
 
Hypothesis  
The hypotheses analysed in the study are  
1. The order flow 𝑂𝑟𝐹𝑙𝑜𝑤𝑘 positively affects the linear relationship with simultaneous 
mid-level price change ∆𝑀𝑖𝑑𝑃𝑟𝑘 , i.e., the price change in the coefficient 𝛽𝑂𝑟𝐹𝑙𝑜𝑤𝑘 is 
not equal to zero and is statistically significant at 1% significance level, i.e., 𝑝 ≤0.01. 
𝐻0: 𝛽𝑂𝑟𝐹𝑙𝑜𝑤= 0;  
𝐻1: 𝛽𝑂𝑟𝐹𝑙𝑜𝑤≠0; 
2. The international trade flows balance 𝐼𝑇𝐹𝑘 positively affects the linear correlation with 
the simultaneous mid-level price change ∆𝑀𝑖𝑑𝑃𝑟𝑘 i.e., the price change in the 
coefficient 𝛽𝐼𝑇𝐹𝑘 is not equal to zero and is statistically significant at 1% significance 
level, 𝑝 ≤0.01. 
𝐻0: 𝛽𝐼𝑇𝐹= 0;  
       𝐻1: 𝛽𝐼𝑇𝐹≠0; 


## Page 4

3. The order flow 𝑂𝑟𝐹𝑙𝑜𝑤𝑘 firmly explained the international trade flow imbalances 𝐼𝑇𝐹𝑘 
on the mid-level price variation ∆𝑀𝑖𝑑𝑃𝑟𝑘, similarly as computed by the coefficient of 
determination- R-squared (𝑅2) 
 
3. Data and Methodology 
We use cross-sectional data on 128 cryptocurrencies for the sample period from February 14th, 
2020, to June 30th, 2025. For each cryptocurrency or coin, the daily price data is sourced from 
coinmarketcap.com (CMC) at 00:00 am GMT. The data collected from CMC comes from over 
700 exchanges and is therefore considered a reliable source, frequently used in the crypto 
literature, such as [24] and [25], which exclude weekends and holidays from the daily sample. 
CMC contains data on thousands of coins with low market capitalisation and limited or 
historical data; hence, to obtain the final cross-sectional data for 128 coins, we apply two 
criteria to ensure liquidity across the entire dataset. The first criterion is that the coins must 
have a market capitalisation greater than 1 million USD on the first day of the sample period. 
The second is that the coins must be traded continuously at non-zero prices and volumes in 
each period of the sample. As a result, our dataset comprises a balanced panel of 128 coins 
listed in Appendix Table 1. We use the daily prices to compute their respective returns. 
𝑟𝑒𝑖,𝑡= 𝑃𝑟𝑖,𝑡
𝑃𝑟𝑖,𝑡−1
−1                        (1) 
where, 𝑃𝑟𝑖,𝑡refers to the price of coin i at time t, and the weekly crypto returns are calculated 
over the period from Saturday at 00:00 GMT to the following Friday at 23:59 GMT, covering 
seven days including the weekend.  at 11.59 pm GMT, spanning seven days, including the 
weekend.  
The volatility is assessed, like the five-minute annualised log return volatility.  
𝜎= √𝑉𝑎𝑟(𝑁𝑙𝑜𝑔 ( 𝑃𝑟𝑡
𝑃𝑟𝑡−1
)) ∗288 ∗365               (1.1) 
 3.1Methodology 
Machine learning method 
We index coins as I = 1, …, N and days t = 1, …, T, and describe the returns of the coins I at 
time t + 1 as 
𝑟𝑒𝑖,𝑡+1 = 𝐸𝑡(𝑟𝑒𝑖,𝑡+1) + 𝜖𝑖,𝑡+1,               (2) 
where, 𝐸𝑡(𝑟𝑒𝑖,𝑡+1) = 𝑔(𝑧𝑖,𝑡) refers to the conditional expected return, and 𝑔(∙) displays as the 
flexible function of the coin i’s P-dimensional vector of characteristics 𝑧𝑖,𝑡, aided by Gu et al. 
(2020), we estimate  𝑔(∙) making use of a variety of models with increasing complexity to 
maximise the out-of-sample predictive power for the realised 𝑟𝑒𝑖,𝑡+1. In asset return prediction 
using machine learning techniques, such as those of [15] and [19], among others, the pooled 
approach is used to forecast individual stock returns. [12] Also, use the above approach to 
forecast exchange rate changes. The excess return forecast is given by: 
𝑟𝑒
̂𝑖,𝑡+1 = 𝑓̂ (𝑥𝑖,𝑡; 𝜂̂)           (3) 


## Page 5

where, 𝑓̂ (∙; 𝜂̂) refers to the fitted predictive model based on data through day t, ensuring no 
forward-looking bias in the forecast.  
For each Monte Carlo sample, we divide the full time series into 3 sequential subsamples of 
equal length for training, validation, and analysis.  Especially, we evaluate each of the two 
models included in the training model by applying PLS, PCR, Ridge, Lasso, Elastic Net (ENet), 
a generalised linear model with the Lasso group (GLM), random forest (RF), gradient boosted 
regression trees (GBRT), and the five similar architecture frameworks of the neural networks 
(NN1,…, NN5) we approve the empirical analysis, respectively.   
Linear-ENet 
A linear specification for the prediction model is considered, and we fit it using ENet [35]. The 
linear ENet excess return forecast is summarised from the intercept term for minimalism, which 
is expressed as: 
 
𝑟𝑒
̂𝑖,𝑡+1
𝐿𝐸𝑛𝑒𝑡= 𝑥𝑖,𝑡
′ 𝜂̂,       (4) 
where, 𝜂̂ refers to the vector of coefficients for the linear model estimated via ENet using data 
up to time t.  Conventional OLS estimation of the linear model maximises the fit of the model 
over the training model. The ENet is often regarded as an extension of the original LASSO 
[32], in which, like LASSO, it uses penalised regularised regression to shrink parameter 
estimates towards zero, thereby guarding against overfitting. The ENet objective function 
applied to the linear model is expressed as:  
arg 𝑚𝑖𝑛
𝜂
1
2(𝑡−1)𝑛[∑∑(𝑟𝑒𝑖,𝑠+1 −𝑥𝑖,𝑠
′ 𝜂)
2
𝑡−1
𝑠=1
𝑛
𝑖=1
] +  𝜆𝑃𝛿(𝜂),                (5)   
Where, 𝑃𝛿(𝜂) = 0.5(1 −𝛿) ‖𝜂‖2
2 + 𝛿 ‖𝜂‖1; and 𝜆≥0 refers to the hyperparameter that 
directs the degree of shrinkage; ‖∙‖1 𝑎𝑛𝑑  ‖∙‖2 stands for the 𝑙𝑜𝑠𝑠1 𝑎𝑛𝑑 𝑙𝑜𝑠𝑠2 standards, 
respectively; 0 ≤ 𝛿 ≤1 refers to the hyperparameter for mixing the 𝑙𝑜𝑠𝑠1 𝑎𝑛𝑑 𝑙𝑜𝑠𝑠2 
elements of the penalty term;  and 𝑛 is the number of cryptocurrencies. For the ease of the 
individual, the equation above uses a balanced panel. For the analysis in our paper, as it is very 
simple to change the notation for the unbalanced panel. The ENet objective function shown in 
the above equation reduces the values for the OLS parameter when 𝜆= 0  and if the value is 
𝛿= 1, the resultant value equals the LASSO objective function, whereas the 𝛿= 0  presents 
the ridge regression [22]. It also encompasses an 𝐿𝑜𝑠𝑠1, Components like the lasso objective 
function, as it permits shrinkage to precisely zero, and ENet also performs variable selection.  
 
Order Flow 
Order flow measures the log difference between customer-initiated and seller-initiated 
transaction volumes in a specific fiat currency over time. We compute order flow using signed 
volume data (buy and sell volumes) from cryptocompare.com (CC), a reliable source of 
cryptocurrency volume data [4]. CC compiles data from over 300 exchanges and provides 
signed volume information that coinmarketcap.com (CMC) does not offer. In our study, we 
use crypto data from CMC, except for signed volume or order flow, which is available only 
from cryptocompare.com. The advantage of CC data is that it supplies signed volume figures 
in multiple fiat currencies. We examine order flow across the G10 currencies, as well as in 
South Korea, an important trading hub outside the G10. This group is called the G11 currencies, 


## Page 6

including the US dollar (USD), Euro (EUR), British pound (GBP), Japanese yen (JPY), Swiss 
franc (CHF), Canadian dollar (CAD), Australian dollar (AUD), New Zealand dollar (NZD), 
Norwegian krone (NOK), Swedish krona (SEK), and Korean won (KRW). We present a 
measure of order flow comparable across cryptocurrencies. Following [28], we standardise 
each series as follows: 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡= 
𝑜𝑓𝑖,𝑡
𝜎(𝑜𝑓𝑖,𝑡−29:𝑡)                       (5) 
where 𝑂𝐹𝑖,𝑡 shows the standardised order flow of coin i at time t, 𝑜𝑓𝑖,𝑡 refers to the original 
order flow, and 𝜎(𝑜𝑓𝑖,𝑡−29:𝑡) shows order-flow volatility over the last 30 days. Due to 
standardisation, the first day of our sample is February 14th, 2018, as the standardised order 
flow is shortened to address potential large volatility spikes; hence, the regression results did 
not change significantly when using truncated vs. non-truncated order flow. Additionally, to 
the 11 international order flows, we also determine the cumulative measure known as the world 
order flow (𝑂𝑟𝐹𝑙𝑜𝑤𝑊𝐹), whereby, it is calculated by aggregating the 11 buy and sell volumes, 
taking the log difference, and applying the same standardisation as for the disaggregated order 
flows.  To verify the contribution of each cryptocurrency to the world order flow, we conduct 
a variance decomposition as follows: 
𝑉𝑎𝑟𝐶𝑜𝑛𝑖
𝑊𝐹= 
𝛽𝑖
2𝑉𝑎𝑟(𝑂𝑟𝐹𝑙𝑜𝑤𝑖)
∑
𝛽𝑖
2𝑉𝑎𝑟(𝑂𝑟𝐹𝑙𝑜𝑤𝑗)
11
𝑗=1
             (6) 
where 𝑉𝑎𝑟𝐶𝑜𝑛𝑖
𝑊𝐹 is the variance contribution of coin I to the world order flow, 𝛽𝑖 displays the 
estimated coefficient of each order flow when regressing the world order flow on its 11 
components, and 𝑉𝑎𝑟(𝑂𝑟𝐹𝑙𝑜𝑤𝑖) refers to the variance of each order flow.  
Linear Regression 
The benchmark model in our paper does not include nonlinearities or interactions among 
predictors. It assumes that the conditional expectation of return g(.) can be approximated by a 
linear function of the predictors and the parameter vector 𝜃.  
𝑔(𝑧𝑖,𝑡;  𝜃) = 𝑧𝑖,𝑡
′ 𝜃            (7) 
The pooled ordinary least squares (OLS) are obtained by minimising the 𝑙2 objective function: 
ℒ(𝜃) = 
1
𝑁𝑜. 𝑜𝑓𝑂𝑏𝑠. 𝑇 ∑∑(𝑟𝑒𝑖,𝑡+1
𝑜𝑏𝑠𝑇
𝑡=1
𝑁
𝑖=1
−𝑔(𝑧𝑖,𝑡;  𝜃))2              (8) 
In our paper, the OLS estimator remains unbiased and fairly efficient when the number of 
predictors, P, is small relative to the number of observations, T. However, as P approaches T, 
the estimator becomes inefficient and prone to overfitting. To mitigate this problem, we utilise 
several Machine Learning (ML) models that have recently been applied in the asset pricing 
literature.  
Birched Linear Regression: Elastic, Lasso, and Ridge Net 
The Accelerated Proximal Algorithm (APG) of [32] and [34], which allows for the efficient 
implementation of the elastic net, Lasso, ridge regression and Group Lasso for both 𝑙𝑜𝑠𝑠2 and 


## Page 7

Huber losses.  This method reduces overfitting in OLS by shrinking the least-squares estimates 
toward zero by adding a penalty term to the objective function. This standard procedure 
intentionally deteriorates the model’s in-sample fit to enhance its out-of-sample stability. Birch 
linear models estimate 𝜃 by reducing: 
ℒ (𝜃; ∙) =  ℒ(𝜃) +  ∅ (𝜃; ∙)                       (9) 
Where, ℒ(𝜃) refers to the loss function and the ∅ (𝜃; ∙) shows the penalty ad and also omits 
the dependency on the tuning parameters. Specifically, we calculate 
𝑅𝑖𝑑𝑔𝑒= 1
2 𝜆∑𝜃𝑗
2,
𝑃𝑟
𝑗=1
𝐿𝑎𝑠𝑠𝑜= 𝜆∑|𝜃𝑗|
𝑃𝑟
𝑗=1
             (10) 
𝐸𝑙𝑎𝑠𝑡𝑖𝑐 𝑁𝑒𝑡= 𝜆(1 −𝑝) ∑|𝜃𝑗| +
𝑃𝑟
𝑗=1
1
2 𝜆𝑝∑𝜃𝑗
2,
𝑃𝑟
𝑗=1
 𝐺𝑟𝑜𝑢𝑝 𝐿𝑎𝑠𝑠𝑜= ∑‖𝜃𝑗‖         (11)
𝑃𝑟
𝑗=1
 
Where, in the Lasso Group case, 𝜃= (𝜃1, 𝜃2, … . . 𝜃𝑃) 𝑖𝑠 𝑡ℎ𝑒 𝐾 × 𝑃 𝑚𝑎𝑡𝑟𝑖𝑥 𝑎𝑛𝑑 where ∅ (𝜃; ) 
is the commonly used elastic net (EN) penalty on 𝜃 defined as: 
∅(𝜃;  𝜆, 𝜌) =  𝜆(1 −𝜌) ∑|𝜃𝑗|
𝑃
𝑗=1
+ 1
2 𝜆𝑝∑𝜃𝑗
2                   (12)
𝑃
𝑗=1
 
where λ refers to the positive tuning parameter controlling the degree of the shrinkage, so that 
the enhanced values of λ lead to further shrinkage of the estimated parameters. When λ=0, the 
model reduces to OLS, and when λ > 0, the EN incorporates two famous standard procedures 
as special cases, controlled by the positive hyperparameter 𝜌. When 𝜌= 0, equation (1) equals 
the Lasso (LAS), which enforces an 𝑙1 parameter penalisation. LAS may specify a subset of 𝜃 
to exactly zero, imposing rarity on the model and thus performing variable selection. When 
𝜌= 1, equation (2) equals the ridge regression (RR), which enforces an 𝑙2 parameter 
penalization. Ridge regression decreases the coefficient estimates toward zero while keeping 
all predictors in the model. For all the values of 𝜌 between 0 and 1, the elastic net blends the 
benefits of RR and LASSO by performing both shrinkage and variable selection. We enhance 
the hyperparameters, 𝜆 𝑎𝑛𝑑 𝜌, by using the validation sample. 
  
Proximal Algorithms 
Proximal algorithms are used to solve convex hyperbolic optimisation problems, where the 
underlying operation is to evaluate the function's recursive operator, such as solving the 
optimisation problem, and, in most cases, the smaller problem has a closed-form solution. The 
optimisation problem requires the proximal operators of  𝜙(𝜃;∙)s which have a closed form 
 
𝑃𝑟𝑜𝑥𝑖𝑚𝐴𝑙𝑔𝑜𝛾𝜙(𝜃) = { 𝑅𝑖𝑑𝑔𝑒=
𝜃
1 + 𝜆𝛾 
                                                                                          {𝐿𝑎𝑠𝑠𝑜=  𝜆𝑆(𝜃, 𝜆𝛾) 
                                                                                       {𝐸𝑙𝑎𝑠𝑡𝑖𝑐 𝑁𝑒𝑡=
𝜃
1 + 𝜆𝛾𝑝𝑆(𝜃, (1 −𝑝)𝜆𝛾), 
                                                                       { 𝐺𝑟𝑜𝑢𝑝 𝑙𝑎𝑠𝑠𝑜
= (𝑆̃(𝜃1, 𝜆𝛾)𝑇, 𝑆̃(𝜃2, 𝜆𝛾)𝑇, … . 𝑆̃(𝜃𝑃, 𝜆𝛾)𝑇)𝑇              (13) 


## Page 8

 
where, 𝑆(𝑥, 𝜇) 𝑎𝑛𝑑 𝑆̃(𝑥, 𝜇) are the multivariate functions where the 𝑖𝑡ℎ Components are 
defined by 
(𝑆(𝑥, 𝜇))𝑖=  {
𝑥𝑖−𝜇       𝑤ℎ𝑒𝑟𝑒 𝑖𝑓 𝑥𝑖> 0 𝑎𝑛𝑑 𝜇< |𝑥𝑖|;
𝑥𝑖+ 𝜇     𝑤ℎ𝑒𝑟𝑒 𝑓 𝑥𝑖 < 0 𝑎𝑛𝑑 𝜇< |𝑥𝑖|;
0, 𝑖𝑓 𝜇 ≥ |𝑥𝑖|; 
}     (14) 
(𝑆̃(𝑥, 𝜇))𝑖= {𝑥𝑖−𝜇
𝑥𝑖
‖𝑥𝑖‖ ,         𝑖𝑓  ‖𝑥𝑖‖ >  𝜇;   
0,                     𝑖𝑓 ‖𝑥𝑖‖ ≤    𝜇.
}        (15) 
 
Here, the 𝑆(𝑥, 𝜇) refers to the binarisation function so that the proximal algorithm is equal to 
the coordinate descent algorithm in the case of loss 𝑙2 like [8], [16].  
 
  Principal Component Analysis Regression (PCAR) 
The PCAR technique is a dimension-reduction method that uses a two-step procedure. In the 
first stage, principal component analysis (PCA) compresses the P predictors into K linear 
combinations that best capture their common variation. In particular, PCA linearly transforms 
the set of predictors into orthogonal principal components, with the initial component having 
the highest variance, and the second component having the second highest variance, and so on, 
up to where the condition K < P principal components. The 𝑗𝑡ℎ principal component 𝑍𝑤𝑗 is 
used to solve the optimisation problem: 
 
𝑤𝑗= 𝑎𝑟𝑔
𝑉𝑎𝑟
𝑤
𝑚𝑎𝑥
(𝑍𝑤),   𝑠. 𝑡. 𝑤′𝑤= 1,
𝐶𝑜𝑣(𝑍𝑤, 𝑍𝑤𝑡) = 0,    𝑙= 1,2, … . , 𝑗−1       (16) 
 
where Z stands for NT X P matrix of the basic standardised predictors,  𝑧𝑖,𝑡 𝑎𝑛𝑑 𝑤𝑗 is the 
eigenvector corresponding to the jth eigenvalue of Var(Z). In the second step, PCAR uses the 
first K leading components as regressors in the OLS regression. Hence, PCAR acts as a 
regularisation technique by isolating coefficients with very low variance components. The 
equation above shows that the first K principal components are selected to explain the variation 
in the P predictors. Though forecasting the future, there is no guarantee that these principal 
components are effective since 𝑟𝑒𝑖,𝑡+1 is not considered in the above equation. Therefore, the 
potential drawback of PCAR is that the initial K principal components, while displaying high 
variance, may have little relation   with 𝑟𝑒𝑖,𝑡+1.  
 
Random Forest and gradient boosted regression trees 
 
Regression trees are fully non-parametric and use a different logic from linear models. A tree 
is built through a sequence of actions, where at each step a new “branch” splits the remaining 
data from the preceding action based on a single predictor. This sequential process divides the 
predictor area into rectangular regions, and the final result is the average values of 𝑟𝑒𝑖,𝑡+1 
within each region. In particular, the prediction of a tree with K regions and depth L, is 
calculated as: 


## Page 9

𝑔(𝑧𝑖,𝑡;  𝜃, 𝐾, 𝐿) = ∑𝜃𝑘
𝐾
𝑘=1
1(𝑧𝑖,𝑡 𝜖𝐶𝑘(𝐿))               (17) 
where, 𝐶𝑘(𝐿) refers to the K regions into which the data is partitioned, 1(.) is the indicator 
function depicting whether 𝑧𝑖,𝑡 falls into the region where 𝐶𝑘(𝐿) and 𝜃𝑘 are a constant. We use 
the algorithm of [5] for the estimation of 𝜃. For each new level, the predictor is selected, and 
the trigger value that minimises the prediction error is used to create the resulting two branches. 
This technique, known as recursive binary splitting, is considered a greedy algorithm because 
at each step of the tree-building process, the best split is selected based solely on that step, 
without considering future splits. The prediction error for each branch C is calculated as:  
𝐻(𝜃, 𝐶) = 1
|𝐶| ∑(
𝑧𝑖,𝑡𝜖𝐶
𝑟𝑒𝑖,𝑡+1 − 𝜃)2                (18) 
here |𝐶|shows the number of observations within the particular branch C, where the loss 
function naturally leads to the optimal choice of 𝜃 as the test average of return within each 
branch, i.e., 𝜃= 
1
|𝐶| ∑
(
𝑧𝑖,𝑡𝜖𝐶𝑟𝑒𝑖,𝑡+1)     𝑇he branching continues until the maximum specified 
depth L is attained or the number of observations in each region is below the specified count. 
The trees capture complex non-linearities and adaptable interactions among the predictors, yet 
this flexibility also introduces a limitation that often leads to trees overfitting the training 
sample. To tackle overfitting, we employ two types of ensemble models that improve stability 
by averaging across multiple trees. The initial model is the random forest (RF), a special case 
of the general technique known as bagging. The partitions are generated by a sequence of 
splitting rules, generally based on the classification and regression tree (CART) algorithm. In 
regression, the predicted value is the mean of the target observations in the terminal nodes. The 
forecasts related to the regression tree with 𝑈 terminal nodes is expressed as: 
𝑟𝑒
̂𝑖,𝑡+1
𝑅𝑔𝑟𝑒𝑠𝑠𝑇𝑟𝑒𝑒= ∑𝑟𝑒
̅̅̅𝑢1𝑢
𝑈
𝑢=1
(𝑥𝑖,𝑡; 𝜂̂𝑢),            (19)  
where the characteristic function 1𝑢(𝑥𝑖,𝑡; 𝜂̂𝑢) = 1 𝑖𝑓 𝑥𝑖,𝑡 ∈ 𝑅𝑢 (𝜂̂𝑢) for the uth region denoted 
by 𝑅𝑢 Correlated with vector 𝜂̂𝑢 based on the splits characterising the tree, or else zero and 𝑟𝑒
̅̅̅𝑢 
shows the mean value of the target sample data observations where 𝑅𝑒𝑢 stands for the training 
sample.  
 
 
Forecast combinations 
Linear and non-linear machine learning techniques help form forecast combinations by 
aggregating predictive ability across multiple models [39]. Following [37], we can compute 
the weighted average of all forecasts across the set of models at each time point, known as the 
mean combination. Conventionally, if the forecast of a given model 𝑗(𝑗= 1, … … 𝐽) is denoted 
by 𝑟𝑒
̂𝑖,𝑡+1
(𝑗) , then the forecast combination at t + 1 is:  
𝑟𝑒
̂𝑖,𝑡+1
𝑀𝑒𝑎𝑛=  1
𝐽∑𝑟𝑒
̂𝑖,𝑡+1
(𝑗)
𝐽
𝑗=1
              (20) 


## Page 10

In this context, J denotes the set of combined models. We examine and compare forecast 
combinations in two scenarios: (1) linear models (L-mean) and (2) non-linear models (NL-
mean). This comparison allows us to evaluate the improvement in predictive accuracy achieved 
by integrating non-linear components and interactions among predictors.  
 
Robust Huber Objective Function  
Cryptocurrency returns follow a heavy-tailed distribution due to asymmetry and high kurtosis. 
The 𝑙2 objective function shown in equation… reveals significant outliers that can destabilise 
the models. To mitigate the influence of this fat-tailed data and enhance model stability, we 
employed the robust Huber objective function, as supported by [21], which is illustrated as:    
ℒ𝐻(𝜃) = 
1
𝑁𝑜. 𝑜𝑓𝑂𝑏𝑠. 𝑇 ∑∑𝐻 (𝑟𝑒𝑖,𝑡+1
𝑜𝑏𝑠𝑇
𝑡=1
𝑁
𝑖=1
−𝑔(𝑧𝑖,𝑡;  𝜃), 𝜉),            (21) 
Here, 𝐻 (𝑥; 𝜉) = {
𝑥2
𝑖𝑓 ⌈𝑥⌉≤ 𝜉;
2𝜉⌈𝑥⌉−𝜉2,
𝑖𝑓 ⌈𝑥⌉> 𝜉} 
The Huber Loss H(.) integrates the 𝐿2 loss reflecting the small errors and the 𝑙1 loss, depicting 
the large errors. The threshold parameter 𝜉 regulates the mix of 𝑙1 𝑎𝑛𝑑 𝑙2. By setting the 
threshold at the 99.9th percentile of returns across the joint training and validation data, we can 
efficiently handle extreme values. We train all our models, excluding Random Forest, using 
the Huber objective function, which is inherently robust to outliers, by following [21], and 
thereby use the default 𝑙2 loss function. Estimation models that use the Huber objective 
function generally outperform those estimated with the mean squared error (MSE) objective 
function on cryptocurrency data.  
 
Deep Neural Network- Feed-Forward (FF) Neural Networks 
 
Neural networks are highly adaptable and can approximate any continuous function, similar to 
the human brain [25]. We utilise feed-forward neural networks with three layers: the input 
layer, which accepts raw predictors; one or more hidden layers that process and transform these 
predictors; and the output layer, which combines the hidden layers' outputs to produce the final 
projection. Each layer takes the signals from the neurons in the previous layer to generate the 
new signal: 
𝑆ℎ𝑚
(𝑙) = 𝑔(𝑤𝑡𝑚,0
(𝑙) + ∑𝑤𝑡𝑚,𝑗
(𝑙)
𝑃𝑡−1
𝑗=1
ℎ𝑗
(𝑙−1))    𝑓𝑜𝑟 𝑚= 1, … , 𝑃𝑡; 𝑙= 1, … 𝐿          (22) 
Here, 𝑆ℎ𝑚
(𝑙) refer to the signal related to the mth neuron in the lth hidden layer; 
𝑤𝑡𝑚,0
(𝑙) , 𝑤𝑡𝑚,1
(𝑙) ,….., 𝑤𝑡𝑚,𝑃𝑡−1
(𝑙)
 are the corresponding weights; and 𝑔 (∙) shows the nonlinear 
activation function. The final layer known as the output layer that derives the signal form the 
last hidden layer and finally transforming them into the prediction: 
 
𝑟𝑒
̂𝑖,𝑡+1
𝑁𝑒𝑡= 𝑤𝑡0
(𝐿+1) +  ∑
𝑤𝑡𝑗
(𝐿+1`)
𝑃𝐿
𝑗=1
ℎ𝑗
(𝐿).       (23) 
The FF neural network is estimated by applying the following formula: 


## Page 11

𝑥(𝑘)
(𝑙) = 𝑓(𝑥(𝑙−1)′𝜃𝑘
(𝑙−1))                        (24) 
where, 𝐾𝑙 refers to the number of concealed units in every layer 𝑙= 1, … . 𝐿, The output of the 
unit k in the layer l is symbolized by 𝑥(𝑘)
(𝑙) , 𝑤ℎ𝑒𝑟𝑒 𝑥𝑙= (1, 𝑥(1)
(𝑙),… . . 𝑥(𝑘)
(𝑙) )′ as the vector of 
outputs for the layer l, along with a constant term. The vector 𝑥(0) shows the input layer of the 
raw predictors. Every unit in the hidden layer follows the condition of 0 < 𝑙< 𝐿 and is also 
frequently expressed in the above equation, and 𝑥(𝑙−1)′ shows the modified output vector from 
the preceding layer 𝑙−1, and 𝜃𝑘
(𝑙−1) refers to the weight coefficients connecting the output of 
unit k to the layer L. The function f indicates the irregular activation of the function that 
modifies the weighted sum of the inputs. We apply the Rectified Linear Unit (ReLU) for the 
neural networks used in our paper: 
 
𝑓(𝑢) = {0 𝑤ℎ𝑒𝑛 𝑢< 0
𝑢 𝑤ℎ𝑒𝑛 𝑢< 0}               (25) 
 
The neural network's final result is computed using the equation below, which is similar to the 
linear output of the last secret layer. 
𝑔(𝑧; 𝜃) = 𝑥(𝑙−1)′𝜃𝑘
(𝑙−1)
                     (26) 
 
Following [21], we determine the turnover of the long-short portfolio at time t as follows: 
𝑇𝑂𝑡= 1
2 ∑|𝑤𝑖,𝑡−
𝑤𝑖,𝑡−1(1 + 𝑟𝑒𝑖,𝑡)
∑
𝑤𝑘,𝑡−1(1 + 𝑟𝑒𝑘,𝑡)
𝑘∈𝐿
|
𝑖∈𝐿
+ 1
2 ∑|𝑤𝑗,𝑡−
𝑤𝑗,𝑡−1(1 + 𝑟𝑒𝑗,𝑡)
∑
𝑤𝑛,𝑡−1(1 + 𝑟𝑒𝑛,𝑡)
𝑛∈𝑆
|
𝑗∈𝑆
    (27)  
Where 𝑖∈𝐿 (𝑗∈𝑆) displays that the coin i (j) takes the long (short) portfolio position, 
𝑤𝑖,𝑡 (𝑤𝑗,𝑡) shows the weight of coin i(j) at time t, 𝑟𝑒𝑖,𝑡(𝑟𝑒𝑗,𝑡)  
 
Out-of-sample model estimation and assessment procedure 
 
We modify the out-of-sample data set for each model's diurnal forecasts by partitioning the 
data into three mutually exclusive sets: the training, reference, and observational sets. First, we 
assess the control variable of the training sample 𝑇𝑟𝑆1 across one year (February 14th, 2020, to 
February 14th, 2022), along with comprehensive hyperparameter maximisation of the 1-year 
reference sample 𝑇𝑟𝑆2 (February 15th, 2022 to February 14th, 2023). Lastly, we perform an out-
of-sample assessment of each model by applying the first 1-month t-test sample results to the 
extended data for the last lap (February 15th, 2024, to June 30th, 025). In our analysis, the 
control variable is held fixed for one month, and the process is replicated by advancing the 
reference and observational sets by one month, while simultaneously extending the training 
sample dataset by one month in each recurrent loop. We carry out the process at the end of the 
sample data so that the complete dataset 𝑇𝑟𝑆3 covers the period from February 14th, 2022, to 
June 30th, 2025. Our out-of-sample dataset analysis focuses on diurnal forecasts, as the short-
rate sample period precludes weekly machine-learning estimation. The key performance 
indicator metric is the modified [42] of the sample R-squared (𝑅𝑜𝑜𝑠
2  ) numerator exercised by 
[21]:  
𝑅𝑜𝑜𝑠
2
= 1 −
∑
(𝑟𝑟𝑒𝑖,𝑡+1 −𝑟𝑟𝑒𝑖,𝑡+1)
2
(𝑖,𝑡)𝜖𝑇𝑟𝑆3
∑
(𝑟𝑟𝑒𝑖,𝑡+1)
2
(𝑖,𝑡)𝜖𝑇𝑟𝑆3
                (28) 


## Page 12

where, 𝑟𝑟𝑒𝑖,𝑡+1 𝑎𝑛𝑑 𝑟𝑟𝑒𝑖,𝑡+1 depicts the realised returns at 𝑡+ 1 and also for the succeeding 
day ahead 𝑡+ 1 forecast for the crypto coin i, respectively, and 𝑇𝑟𝑆3 states the metric function 
is evaluated only on the test sample.  
The anomalies in cryptocurrency returns are evident in the very high kurtosis coefficient. The 
R-squared (𝑅𝑜𝑜𝑠
2  ) fact is based on the MSE, which assigns high weight to large errors; the 
anomalies can be significant. The out-of-sample MSE for the existing mean benchmark in 
relation to the competing forecast via the out-of-sample 𝑅2 statistic [12], [7]  
𝑅,𝑖,𝑜𝑜𝑠
2
= 1 −
∑
(𝑟𝑒𝑖,𝑡𝑠𝑖𝑛𝑖+𝑠− 𝑟𝑒
̂𝑖,𝑡𝑠𝑖𝑛𝑖+𝑠
𝐶𝑜𝑚𝑝𝑒𝐹𝑜𝑟𝑒)
2
𝑇𝑆−𝑡𝑖𝑛𝑖
𝑠=1
∑
(𝑟𝑒𝑖,𝑡𝑠𝑖𝑛𝑖+𝑠− 𝑟𝑒
̂𝑖,𝑡𝑠𝑖𝑛𝑖+𝑠
𝐵𝑒𝑛𝑐ℎ𝑚𝑎𝑟𝑘)
2
𝑇𝑆−𝑡𝑖𝑛𝑖
𝑠=1
,        (29) 
Where,  𝑟𝑒
̂𝑖,𝑡
𝐶𝑜𝑚𝑝𝑒𝐹𝑜𝑟𝑒 depicts a competing forecast, and 𝑡𝑖𝑛𝑖𝑠 (T) refers to the end of the initial 
sample period (i.e., the total sample). The proportional decrease in the out-of-sample MSE of 
the competing forecasts relative to the prevailing average benchmark. The [11] statistic, also 
known as the DMW statistic, is used to test whether a competing forecast yields a statistically 
significant decrease in MSE relative to the prevailing benchmark. The DMW statistics are 
calculated as the t-statistic, similar to the intercept 𝑎𝑖 of the time-series regression as calculated 
below: 
(𝑟𝑒𝑖,𝑡−𝑟𝑒
̂𝑖,𝑡
𝐵𝑒𝑛𝑐ℎ𝑚𝑎𝑟𝑘 )2 −(𝑟𝑒𝑖,𝑡−𝑟𝑒
̂𝑖,𝑡
𝐶𝑜𝑚𝑝𝑒𝐹𝑜𝑟𝑒 )2 
⏟                                
𝐷−𝑇𝑙𝑜𝑠𝑠𝑑𝑖𝑓𝑓𝑖,𝑡
      = 𝑎𝑖+ 𝜀𝑖,𝑡   𝑓𝑜𝑟 𝑡= 𝑡𝑖𝑛𝑠+
1, … … , 𝑇  (30) 
where, 𝐷−𝑇𝑙𝑜𝑠𝑠𝑑𝑖𝑓𝑓𝑖,𝑡 stands for the day-t loss differential, which covers the difference 
between the squared errors of the benchmark and the competing forecasts. The null hypothesis 
𝐻0: 𝑎𝑖 ≤0  
 
Vector Autoregression (VAR) technique 
Financial asset prices and order flows are closely linked and evolve together over time [16]. 
The positive correlation between them likely results from two factors: first, positive price 
insights encourage more buying activity, as order flow contains predictive information. 
Additionally, increased order flow exerts upward pressure on prices, creating a feedback loop 
that pushes prices higher. Alternatively, lower prices can attract more buy orders, which in turn 
draw in sell orders, thereby reducing overall trading velocity. The momentum of this cost push 
is quantitatively assessed as follows: 
𝑟𝑒𝑡=  𝑎0 + ∑𝑎1𝑟𝑒𝑡−1
5
𝑖=1
+ ∑𝑏1
5
𝑖=0
𝑂𝑟𝐹𝑙𝑜𝑤𝑡−𝑖
𝐺𝑙𝑜𝑏𝑎𝑙+ ∑𝑚𝑖
𝑁
𝑖=1
𝐸𝑓𝑖,𝑡−1 + 𝜀1,𝑡                (31) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑡
𝐺𝑙𝑜𝑏𝑎𝑙=  𝑐𝑜+ ∑𝑐1𝑟𝑒𝑡−1
5
𝑖=1
+  ∑𝑑1
5
𝑖=0
𝑂𝑟𝐹𝑙𝑜𝑤𝑡−𝑖
𝐺𝑙𝑜𝑏𝑎𝑙+ ∑𝑛𝑖
𝑁
𝑖=1
𝐸𝑓𝑖,𝑡−1 + 𝜀2,𝑡    (32) 
here, 𝐸𝑓𝑖,𝑡−1 is the 𝑖 ≤𝑁  refers to the economic variables applied as the control variables. For 
the selective unique constant and the cumulative factors at 5 lags, we compute the t-statistics 
using time- and coin-grouped standard errors. The sample period is February 14th, 2020, to 
June 30th, 2025.  
 


## Page 13

ANALSYIS 
Table 1-Analysis of the Predictive 𝑹𝟐𝒔 for the  average in-sample (AIS) and out-of-
sample) 
Model 
(1) 
(2) 
 
𝑷𝑷𝒄𝒕= 𝟓𝟎 
𝑷𝑷𝒄𝒕= 𝟓𝟎 
𝑷𝑷𝒄𝒕= 𝟓𝟎 
𝑷𝑷𝒄𝒕= 𝟓𝟎 
Particular 
AIS 
OOS 
AIS 
OOS 
AIS 
OOS 
AIS 
OOS 
OLS 
7.60 
1.24 
8.29 
-1.45 
3.54 
-4.82 
4.49 
-7.85 
OLS+HL 
7.58 
1.35 
8.26 
-1.25 
3.53 
-4.70 
4.46 
-7.64 
PCR 
2.79 
0.99 
1.80 
0.44 
0.75 
0.05 
0.51 
-0.05 
PLS 
6.34 
3.58 
6.29 
2.83 
1.12 
-0.09 
0.99 
-0.27 
LASSO 
6.14 
4.36 
6.18 
4.35 
1.46 
0.68 
1.46 
0.71 
Lasso+HL 
6.10 
4.36 
6.14 
4.35 
1.42 
0.69 
1.41 
0.71 
RIDGE 
6.56 
3.99 
6.76 
3.49 
1.76 
0.44 
1.86 
0.33 
RIDGE+HL 
6.52 
3.99 
6.71 
3.44 
1.73 
0.45 
1.83 
0.35 
ENET 
6.14 
4.36 
6.18 
4.35 
1.45 
0.68 
1.45 
0.71 
ENET+HL 
6.10 
4.36 
6.14 
4.35 
1.42 
0.69 
1.41 
0.71 
GLM 
5.99 
4.21 
5.95 
4.18 
3.48 
1.32 
3.41 
1.27 
GLM+HL 
5.95 
4.22 
5.98 
4.19 
3.42 
1.34 
3.34 
1.30 
RF 
8.44 
3.45 
8.33 
3.40 
8.15 
3.17 
8.23 
3.12 
GBRT 
7.18 
3.45 
7.12 
3.44 
6.61 
2.86 
6.52 
2.94 
GBRT+HL 
7.26 
3.55 
7.21 
3.47 
6.57 
3.22 
6.47 
3.33 
NN1 
6.63 
4.47 
6.82 
4.38 
5.71 
2.88 
5.90 
2.69 
NN2 
6.66 
4.52 
6.82 
4.36 
6.32 
3.23 
6.43 
2.99 
NN3 
6.57 
4.44 
6.76 
4.37 
6.13 
2.99 
6.19 
2.78 
NN4 
6.57 
4.41 
6.76 
4.34 
5.99 
2.91 
6.14 
2.61 
NN5 
6.51 
4.37 
6.66 
4.24 
5.91 
2.82 
5.80 
2.30 
ORACLE 
6.33 
5.62 
6.33 
5.62 
5.96 
5.50 
5.96 
5.50 
Source: Author's Own Creation 
Note- The above table displays the average in-sample (AIS) and out-of-sample (OOS) 𝑅2 models (1) and (2) by 
applying the Ridge, Lasso, Elastic Net (ENet), summarised linear model with lasso group (GLM), random forest 
(RF), gradient boosted regression trees (GBRT), and five configurations of the neural networks (NN1, …., NN5), 
respectively. “+HL” refers to the Huber loss instead of the 𝑙2 loss, Oracle refers to the current covariates used in 
the pooled OLS regression. We set the no. of the sample at 200, where N=2, T=180, and 𝑃𝑃𝑐𝑡= 2 in comparison 
to the 𝑃𝑃𝑐𝑡= 10 𝑤𝑖𝑡ℎ 𝑃𝑃𝑐𝑡= 50And also the number of Monte Carlo repetitions is 100.  
 
The average in-sample (AIS) and out-of-sample (OOS) 𝑅2  models relate to estimators based 
on the AIS average. For model (1), Lasso, ENet, and NNs show superior and nearly equal OOS 
𝑅2  results, though high-performing models are rare and vary with the study's inlet covariates. 
Advanced tree methods like RF and GBRT tend to overfit, so they perform slightly worse. In 
contrast, in model (2), these methods clearly outperform Lasso and ENet, as the latter fail to 
capture the models' nonlinearities. The GLM performs similarly well, although it is driven by 
NNs, RF, and GBRT. OLS results are the worst across all conditions, while PLS outperforms 
PCR in linear model (1) and exceeds it in nonlinear models. As the 𝑃𝑃𝑐𝑡 increases, AIS 𝑅2rises, 
but OSS 𝑅2 declines, indicating a deterioration in performance as selection bias increases. 
Applying the Huber Loss improves OOS performance for nearly all methods, with RF, GBRT, 
and HL considered optimal for nonlinear models. The NNs show a notable trade-off between 
flexibility and complexity; the ENet's Accelerated Proximal Gradient (APG) algorithms are 
unsuitable for all NNs due to non-linear loss functions. The table notes that lower NNs 
outperform higher ones.  
 
Table 2 Analysis of the Predictive 𝑹𝟐𝒔 for the average in-sample (AIS) and out-of-sample) 
for different prediction time periods in Simulations  


## Page 14

Model 
(1) 
(2) 
Range 
Qtr. 
 
HYrly 
 
Yearly 
 
Qtr. 
 
H.Yr. 
 
Yearly 
 
𝑹𝟐   (%) 
AIS 
OOS 
AIS 
OOS 
AIS 
OOS 
AIS 
OOS 
AIS 
OOS 
AIS 
OOS 
OLS 
18.94 
-0.95 
27.77 
0.29 
35.50 
-0.25 
10.13 
-16.57 
15.22 
-23.58 
20.29 
-30.83 
OLS+HL 
18.92 
-0.86 
27.76 
0.41 
35.48 
-0.19 
10.10 
16.37 
14.95 
-23.42 
20.25 
-30.76 
PCR 
3.96 
0.95 
5.60 
1.42 
7.68 
1.49 
0.99 
-0.14 
1.40 
-0.14 
1.81 
-0.34 
PLS 
15.22 
6.66 
21.62 
8.50 
26.56 
8.24 
1.95 
-0.52 
1.83 
-0.43 
2.88 
-0.90 
LASSO 
14.20 
10.43 
20.52 
14.78 
25.16 
16.76 
3.20 
1.27 
4.13 
1.22 
4.97 
0.50 
Lasso+HL 
14.21 
10.42 
20.40 
14.77 
24.95 
16.84 
3.13 
1.29 
3.95 
1.25 
4.76 
0.58 
RIDGE 
15.86 
7.91 
23.36 
10.77 
29.37 
11.75 
4.17 
0.53 
5.76 
0.54 
6.82 
0.00 
RIDGE+HL 
15.78 
7.94 
23.25 
10.79 
29.23 
11.75 
4.10 
0.55 
5.66 
0.56 
6.66 
0.14 
ENET 
14.18 
10.43 
20.59 
14.79 
25.16 
16.79 
3.20 
1.25 
4.17 
1.24 
4.90 
0.51 
ENET+HL 
13.95 
10.42 
20.47 
14.78 
24.95 
16.76 
3.12 
1.27 
3.95 
1.28 
4.70 
0.58 
GLM 
13.99 
9.50 
21.12 
13.63 
27.25 
15.46 
7.71 
2.56 
10.89 
2.99 
13.17 
1.73 
GLM+HL 
13.89 
9.52 
20.98 
13.66 
26.95 
15.50 
7.58 
2.61 
10.69 
2.99 
12.88 
1.81 
RF 
17.66 
8.21 
25.34 
11.96 
31.14 
14.42 
15.62 
5.95 
20.63 
7.21 
22.58 
6.15 
GBRT 
15.99 
8.95 
22.78 
13.37 
28.78 
15.16 
12.49 
5.97 
15.95 
6.99 
18.18 
5.95 
GBRT+HL 
15.80 
8.88 
22.94 
13.55 
29.17 
15.39 
12.22 
5.97 
16.10 
7.23 
18.30 
6.27 
NN1 
15.78 
9.99 
23.14 
14.17 
29.72 
15.68 
13.32 
5.46 
17.99 
6.39 
20.78 
5.42 
NN2 
15.66 
9.96 
22.82 
14.10 
28.99 
16.11 
13.39 
5.86 
17.99 
6.87 
20.20 
5.53 
NN3 
15.55 
9.89 
22.77 
13.95 
28.69 
16.20 
13.21 
5.67 
17.60 
6.73 
20.41 
5.37 
NN4 
15.59 
9.95 
22.42 
14.16 
28.69 
15.99 
13.30 
5.66 
17.90 
6.62 
19.77 
5.30 
NN5 
15.29 
9.92 
22.24 
13.95 
28.32 
15.95 
13.10 
5.34 
17.25 
6.29 
18.96 
5.18 
ORACLE 
14.47 
12.82 
20.83 
18.25 
25.52 
21.66 
10.99 
10.38 
13.71 
12.85 
13.14 
11.62 
Source: Author's Own Creation 
Note- The above table displays the average in-sample (AIS) and out-of-sample (OOS) 𝑅2 models (1) and (2) by 
applying the Ridge, Lasso, Elastic Net (ENet), summarised linear model with lasso group (GLM), random forest 
(RF), gradient boosted regression trees (GBRT), and five configurations of the neural networks (NN1, …., NN5), 
respectively. “+HL” refers to the Huber loss instead of the 𝑙2 loss, Oracle refers to the current covariates used in 
the pooled OLS regression. We set the no. of the sample at 200, where N=2, T=180, and 𝑃𝑃𝑐𝑡= 2 in comparison 
to the 𝑃𝑃𝑐𝑡= 10 𝑤𝑖𝑡ℎ 𝑃𝑃𝑐𝑡= 50And also the number of Monte Carlo repetitions is 100.  
 
The usual ever-increasing hump-shaped pattern of the 𝑅2𝑠 Against varied investment horizons, 
it is specifically driven by the covariate's persistence, with comparable performance across the 
models.  
 
Table 3 Comparison of the Mean Variable Selection Frequencies in Simulation 
Model (1) 
Parameter 
Technique 
𝒄𝒗𝒊,𝟏,𝒕 
𝒄𝒗𝒊,𝟐,𝒕 
𝒄𝒗𝒊,𝟑,𝒕 
𝒄𝒗𝒊,𝟏,𝒕× 𝒙𝒕 
𝒄𝒗𝒊,𝟐,𝒕 × 𝒙𝒕 
𝒄𝒗𝒊,𝟑,𝒕× 𝒙𝒕 
Dissonance 
𝑃𝑃𝑐𝑡= 5𝑜 
Lasso 
0.96 
0.95 
0.66 
0.54 
0.52 
0.86 
0.10 
 
Lasso +HL 
0.96 
0.95 
0.64 
0.54 
0.51 
0.87 
0.09 
 
ENet 
0.96 
0.95 
0.66 
0.55 
0.52 
0.87 
0.10 
 
ENet+HL 
0.96 
0.95 
0.65 
0.54 
0.51 
0.87 
0.10 
 
GLM 
0.96 
0.95 
0.73 
0.62 
0.64 
0.91 
0.14 
 
GLM+ HL 
0.96 
0.95 
0.71 
0.62 
0.63 
0.91 
0.13 
𝑃𝑃𝑐𝑡= 100 
Lasso 
0.96 
0.95 
0.66 
0.53 
0.50 
0.86 
0.07 
 
Lasso +HL 
0.96 
0.95 
0.64 
0.54 
0.50 
0.87 
0.07 
 
ENet 
0.96 
0.95 
0.66 
0.54 
0.50 
0.87 
0.07 
 
ENet+HL 
0.96 
0.95 
0.65 
0.54 
0.50 
0.87 
0.07 
 
GLM 
0.96 
0.95 
0.73 
0.59 
0.62 
0.91 
0.10 


## Page 15

 
GLM+ HL 
0.96 
0.95 
0.70 
0.56 
0.61 
0.91 
0.10 
Model (2) 
Parameter 
Technique 
𝒄𝒗𝒊,𝟏,𝒕 
𝒄𝒗𝒊,𝟐,𝒕 
𝒄𝒗𝒊,𝟑,𝒕 
𝒄𝒗𝒊,𝟏,𝒕× 𝒙𝒕 
𝒄𝒗𝒊,𝟐,𝒕 × 𝒙𝒕 
𝒄𝒗𝒊,𝟑,𝒕× 𝒙𝒕 
Dissonance 
𝑃𝑃𝑐𝑡= 5𝑜 
Lasso 
0.27 
0.27 
0.40 
0.28 
0.32 
0.76 
0.05 
 
Lasso +HL 
0.26 
0.26 
0.39 
0.29 
0.32 
0.75 
0.05 
 
ENet 
0.27 
0.26 
0.40 
0.28 
0.32 
0.7 
0.05 
 
ENet+HL 
0.26 
0.25 
0.40 
0.29 
0.32 
0.76 
0.05 
 
GLM 
0.81 
0.55 
0.69 
0.69 
0.65 
0.83 
0.22 
 
GLM+ HL 
0.80 
0.55 
0.71 
0.69 
0.63 
0.83 
0.21 
𝑃𝑃𝑐𝑡= 100 
Lasso 
0.26 
0.26 
0.38 
0.26 
0.32 
0.76 
0.03 
 
Lasso +HL 
0.25 
0.25 
037 
0.27 
0.32 
0.76 
0.03 
 
ENet 
0.26 
0.26 
038 
0.26 
0.32 
0.77 
0.03 
 
ENet+HL 
0.25 
0.25 
0.38 
0.27 
0.32 
0.76 
0.03 
 
GLM 
0.81 
0.53 
0.68 
0.66 
0.58 
0.82 
0.15 
 
GLM+ HL 
0.80 
0.49 
0.68 
0.67 
0.57 
0.82 
0.14 
Source: Author's Own Creation 
Note- The above table reports the mean variable selection for the frequencies of the 6 particulate variables for the 
2 models (1) and (2) covering the monthly horizon by applying the Lasso, Elastic Net (ENet) and the generalised 
linear model with the group lasso (GLM), respectively. “+HL” refers to the Huber loss instead of the 𝑙2 loss. 
“Dissonance” sates the mean selection frequency of the remaining P-6 covariates.  We set the no. of the sample 
at 200, where N=2, T=180, and 𝑃𝑃𝑐𝑡= 2 in comparison to the 𝑃𝑃𝑐𝑡= 10 𝑤𝑖𝑡ℎ 𝑃𝑃𝑐𝑡= 50 and also the number of 
Monte Carlo repetitions is 100.  
We use the Lasso, Elastic Net and Lasso Group along with their most powerful versions, as 
they all enforce the 𝑙𝑜𝑠𝑠1 penalty and thereby select the variable selection. The true covariates 
(𝑐𝑣𝑖,1,𝑡, 𝑐𝑣𝑖,2,𝑡, 𝑐𝑣𝑖,3,𝑡× 𝑥𝑡) are selected in over 85% of the sample size, unlike the superfluous 
covariates (𝑐𝑣𝑖,3,𝑡, 𝑐𝑣𝑖,1,𝑡×  𝑐, 𝑐𝑣𝑖,2,𝑡, 𝑥𝑡) are selected in around 60% of the samples. The last 
covariate is occasionally chosen. The pressure on variable selection and prediction, or on finite-
sample issues, is that the true covariates are included in the selected models with very high 
probability. There are zero covariates for the second model; the covariates included are far 
more useful and therefore are selected substantially more often than the rest of the covariates 
𝑃−6 covariates.  
 
Table 4 Comparison of the Mean Variable Selection Frequencies in Simulation 
Model (1) 
Parameter 
Technique 
𝒄𝒗𝒊,𝟏,𝒕 
𝒄𝒗𝒊,𝟐,𝒕 
𝒄𝒗𝒊,𝟑,𝒕 
𝒄𝒗𝒊,𝟏,𝒕× 𝒙𝒕 
𝒄𝒗𝒊,𝟐,𝒕 × 𝒙𝒕 
𝒄𝒗𝒊,𝟑,𝒕× 𝒙𝒕 
Dissonance 
𝑃𝑃𝑐𝑡= 5𝑜 
RF 
22.55 
23.30 
5.99 
6.55 
6.45 
19.55 
0.20 
 
GBRT 
24.68 
27.88 
5.74 
6.46 
6.13 
25.77 
0.06 
 
GNRT+HL 
24.03 
24.63 
5.53 
6.50 
6.88 
25.99 
0.06 
 
NN1 
26.60 
29.99 
5.61 
2.88 
3.76 
25.28 
0.08 
 
NN2 
26.45 
28.96 
5.24 
3.23 
3.96 
25.84 
0.08 
 
NN3 
26.15 
28.67 
5.23 
3.19 
3.89 
25.67 
0.09 
 
NN4 
26.29 
28.92 
5.28 
3.47 
3.86 
25.69 
0.09 
 
NN5 
25.96 
28.60 
5.32 
3.36 
3.76 
25.46 
0.10 
𝑃𝑃𝑐𝑡= 100 
RF 
21.60 
23.18 
5.94 
5.63 
5.89 
19.28 
0.11 
 
GBRT 
24.87 
28.92 
5.52 
6.23 
5.89 
25.53 
0.04 
 
GNRT+HL 
23.85 
27.22 
5.40 
6.14 
6.36 
26.10 
0.04 
 
NN1 
25.88 
28.56 
5.23 
2.88 
3.63 
24.67 
0.06 
 
NN2 
25.60 
27.99 
4.95 
2.96 
3.55 
24.68 
0.07 
 
NN3 
25.82 
28.33 
4.83 
2.99 
3.56 
24.63 
0.07 


## Page 16

 
NN4 
25.22 
27.73 
4.88 
2.93 
3.48 
24.44 
0.07 
 
NN5 
24.89 
27.93 
4.86 
3.17 
3.53 
24.29 
0.07 
Model (2) 
Parameter 
Technique 
𝒄𝒗𝒊,𝟏,𝒕 
𝒄𝒗𝒊,𝟐,𝒕 
𝒄𝒗𝒊,𝟑,𝒕 
𝒄𝒗𝒊,𝟏,𝒕× 𝒙𝒕 
𝒄𝒗𝒊,𝟐,𝒕 × 𝒙𝒕 
𝒄𝒗𝒊,𝟑,𝒕× 𝒙𝒕 
Dissonance 
𝑃𝑃𝑐𝑡= 5𝑜 
RF 
27.80 
6.49 
5.06 
8.12 
5.10 
32.23 
0.19 
 
GBRT 
31.25 
7.38 
5.92 
8.82 
6.53 
36.51 
0.14 
 
GNRT+HL 
32.15 
7.47 
5.93 
8.88 
6.72 
35.67 
0.14 
 
NN1 
55.66 
14.50 
4.56 
3.56 
2.98 
12.21 
0.17 
 
NN2 
51.94 
13.77 
4.25 
2.97 
2.82 
18.33 
0.17 
 
NN3 
52.10 
13.74 
4.46 
2.95 
2.99 
16.73 
0.18 
 
NN4 
51.09 
13.71 
4.55 
3.36 
2.89 
16.29 
0.19 
 
NN5 
49.76 
13.78 
4.58 
3.38 
2.96 
15.99 
0.21 
𝑃𝑃𝑐𝑡= 100 
RF 
26.43 
5.84 
4.60 
7.78 
4.79 
31.96 
0.11 
 
GBRT 
31.50 
7.40 
5.48 
8.67 
6.27 
36.80 
0.05 
 
GNRT+HL 
32.23 
7.58 
5.81 
8.77 
6.40 
35.89 
0.05 
 
NN1 
53.11 
13.63 
4.89 
3.55 
2.88 
12.12 
0.06 
 
NN2 
50.26 
12.96 
4.36 
2.88 
2.55 
17.41 
0.06 
 
NN3 
50.46 
13.10 
4.40 
2.91 
2.64 
15.46 
0.07 
 
NN4 
48.38 
13.15 
4.60 
3.23 
2.73 
15.15 
0.08 
 
NN5 
43.44 
12.51 
4.81 
3.63 
2.69 
16.19 
0.10 
Source: Author's Own Creation 
Note- The above table reports the mean variable selection for the frequencies of the 6 particulate variables for the 
2 models (1) and (2) covering the monthly horizon by applying Random Forest (RF), gradient boosted regression 
trees (GBRT), and five architectures of neural networks (NN1,….NN), respectively. “+HL” refers to the Huber 
loss instead of the 𝑙2 loss. “Dissonance” sates the mean selection frequency of the remaining P-6 covariates.  We 
set the no. of the sample at 200, where N=2, T=180, and 𝑃𝑃𝑐𝑡= 2 in comparison to the 𝑃𝑃𝑐𝑡= 10 𝑤𝑖𝑡ℎ 𝑃𝑃𝑐𝑡= 50 
and also the number of Monte Carlo repetitions is 100. The above table reports the mean VIPs of the 
specific covariates and the mean of the remaining 𝑃−6 
 
Table 5 Variance segregation of the global order flows 
 
Diurnal% 
Per Week% 
𝑂𝑟𝐹𝑙𝑜𝑤𝑈𝑆𝐷 
38.07 
38.13 
𝑂𝑟𝐹𝑙𝑜𝑤𝐾𝑅𝑊 
23.43 
30.49 
𝑂𝑟𝐹𝑙𝑜𝑤𝐸𝑈𝑅 
10.47 
10.08 
𝑂𝑟𝐹𝑙𝑜𝑤𝐺𝐵𝑃 
5.99 
4.89 
𝑂𝑟𝐹𝑙𝑜𝑤𝑁𝑍𝐷 
3.88 
3.23 
𝑂𝑟𝐹𝑙𝑜𝑤𝐶𝐻𝐹 
3.75 
2.49 
𝑂𝑟𝐹𝑙𝑜𝑤𝐴𝑈𝐷 
3.67 
2.66 
𝑂𝑟𝐹𝑙𝑜𝑤𝐶𝐴𝐷 
3.54 
2.88 
𝑂𝑟𝐹𝑙𝑜𝑤𝑁𝑂𝐾 
2.84 
1.88 
𝑂𝑟𝐹𝑙𝑜𝑤𝑆𝐸𝐾 
2.76 
1.61 
𝑂𝑟𝐹𝑙𝑜𝑤𝐽𝑃𝑌 
1.60 
1.66 
𝑂𝑟𝐹𝑙𝑜𝑤𝑊𝑜𝑟𝑙𝑑 
100 
100 
Source: Author's Own Creation 
Table 2 presents the variance decomposition of world order flows across 11 countries where cryptocurrencies are 
primarily traded. The daily data show the highest variance contribution at 38%; South Korea ranks second at 23%, 
making it one of the elite players in the crypto market. The Euro ranked third at 11%, followed by the British 
Pound at about 6%. Broadly, the world order flow is dominated by a few countries: the top 2 countries account 
for almost 61% of the total variance, and the top 3 account for approximately 72%. The weekly variance 
contributions are similar to the daily ones, regardless of the order flow of the top three countries, which together 
account for 79% of global order flow. The values represent the percentage contribution to the variance of each 


## Page 17

country's world order flows at daily and weekly frequencies. The out-of-sample testing period runs from February 
14th, 2020, to June 30th, 2025. 
  
Table 6 Concurrent panel regressions with the Global Order Flows 
 
Diurnal 
Per Week 
 
(1|) 
(2) 
(3) 
(4) 
Constant term 
0.003 
0.002 
0.013 
0.060 
 
(1.20) 
(1.17) 
(1.51) 
(1.18) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝑊 
0.033*** 
0.033*** 
0.055*** 
0.050*** 
 
(15.78) 
(15.70) 
(8.20) 
(8.39) 
𝑀𝑘𝑡𝐶𝑎𝑝𝑖𝑖,𝑡 
 
-0.002 
 
0.020*** 
 
 
(-0.60) 
 
(3.18) 
𝑇𝑜𝑡𝑎𝑙𝑉𝑜𝑙𝑖,𝑡 
 
0.008*** 
 
0.008*** 
 
 
(6.96) 
 
(2.58) 
𝑁𝑙𝑜𝑔𝑉𝑜𝑙𝑖,𝑡 
 
0.269** 
 
0.266*** 
 
 
(3.64) 
 
(3.42) 
𝐶𝐵𝑂𝐸𝑉𝐼𝑋𝑡 
 
-0.050 
 
-0.095 
 
 
(-1.62) 
 
(-1.18) 
𝐹𝑅𝐸𝐷𝑇 
 
0.000 
 
0.001 
 
 
(0.89) 
 
(0.88) 
𝑆&𝑃 500 𝑉𝐼𝑋𝑡 
 
-0.677 
 
-4.066 
 
 
(-2.06) 
 
(-2.30) 
𝑀𝑆𝐶𝐼𝑡
𝑊𝑜𝑟𝑙𝑑 
 
0.784 
 
5.892*** 
 
 
(1.44) 
 
(2.86) 
𝑆ℎ𝑅𝑎𝑡𝑒𝑡 
 
-0.003 
 
-0.018 
 
 
(-0.86) 
 
(-1.46) 
𝑌𝑖𝑒𝑙𝑑 𝑆𝑝𝑟𝑒𝑎𝑑𝑡 
 
-0.008 
 
-0.066** 
 
 
(-1.51) 
 
(-1.99) 
𝑍(𝑑𝑒𝑓𝑎𝑢𝑙𝑡)𝑆𝑝𝑟𝑒𝑎𝑑𝑡 
 
0.011 
 
0.014 
 
 
(1.37) 
 
(0.30) 
R-Squared (%) 
7.1 
11.36 
6.7 
21.4 
No. of Obs.  
101139 
101139 
18723 
18723 
Source: Author's Own Creation 
The table above presents the results of the concurrent panel regression, which includes global order flow and 
various control variables. The study uses the log version of order flow, with market capitalisation and total 
volatility also expressed in logarithmic form. “Volatility” indicates the difference between a cryptocurrency’s 
high and low prices. Log returns are used for the CBOEVIX, S&P 500 VIX, and MSCI World indices. FRED 
presents the difference between the 3-month Treasury bill rate and LIBOR, with the short rate denoting the former. 
The yield spread measures the difference between the 10-year and 3-month Treasury bill rates. The Z-default 
spread is the difference between AAA and BAA bonds. The total panel regression is based on a balanced panel 
that includes fixed effects for each cryptocurrency. Columns (1) and (2) show daily returns, while columns (3) 
and (4) show weekly returns. Statistics are in parentheses and are calculated using standard errors, grouped by 
time and coins. The out-of-sample testing period runs from February 14th, 2020, to June 30th, 2025.  
 
The table shows that global order flow has a marked impact on cryptocurrency returns, a pattern 
observed across all cases. This indicates that global order flows effectively account for 
variations in returns. For instance, a 1% increase in the standard deviation of control variables, 
such as global order flows, is associated with a 3.3% increase in daily returns and a 5.0% 
increase in weekly returns. These results are supported by high t-statistics of 15.70 for daily 
data and 8.39 for weekly data, confirming their robustness. Our findings are consistent with 
[21], who also documented a positive relationship. The analysis establishes a contemporaneous 
link between global order flow and Bitcoin returns in daily regressions, with this positive 
association extending to other cryptocurrencies and to weekly models. The weekly regressions 
show higher coefficients than the daily ones, with R-squared values of 11.36% for daily and 


## Page 18

21.4% for weekly data. The stronger weekly results likely stem from order-flow data that filter 
out high-frequency noise and uninformed trades. Summing order flow over a week reduces this 
noise, which may explain its greater explanatory power for weekly price changes. Besides order 
flow, other control variables are also significant: for daily data, total volume and volatility; for 
weekly data, total market cap, volume, volatility, S&P 500 VIX returns, MSCI Global index 
returns, and yield spreads. Overall, these results demonstrate that order flows have substantial 
explanatory power for cross-sectional cryptocurrency returns, even after controlling for crypto-
specific factors and basic economic indicators. 
 
Table 7 Predictive longitudinal data analysis with the global order flows 
 
Diurnal 
Per Week 
 
(1|) 
(2) 
(3) 
(4) 
(5) 
(6) 
Constant term 
0.003 
0.003 
0.014 
0.014 
0.014 
0.056 
 
(1.03) 
(1.09) 
(1.09) 
(1.52) 
(1.54) 
(0.78) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−1
𝑊
 
0.002 
0.002*** 
0.002*** 
0.009** 
0.009*** 
0.009*** 
 
(0.72) 
(2.68) 
(3.12) 
(2.40) 
(3.33) 
(3.50) 
𝑟𝑒𝑖,𝑡−1 
 
-0.064*** 
-0.067 
 
-0.029 
-0.038 
 
 
(-3.35) 
(-3.83) 
 
(-0.52) 
(-1.02) 
𝑀𝑘𝑡𝐶𝑎𝑝𝑖𝑖,𝑡−1 
 
 
-0.008*** 
 
 
-0.031*** 
 
 
 
(-3.85) 
 
 
(-6.00) 
𝑇𝑜𝑡𝑎𝑙𝑉𝑜𝑙𝑖,𝑡−1 
 
 
0.002 
 
 
0.005** 
 
 
 
(1.49) 
 
 
(1.09) 
𝑁𝑙𝑜𝑔𝑉𝑜𝑙𝑖,𝑡−1 
 
 
0.058*** 
 
 
0.077* 
 
 
 
(2.74) 
 
 
(3.08) 
𝐶𝐵𝑂𝐸𝑉𝐼𝑋𝑡−1 
 
 
-0.014 
 
 
-0.106 
 
 
 
(-0.40) 
 
 
(-1.29) 
𝐹𝑅𝐸𝐷𝑡−1 
 
 
-0.000 
 
 
-0.001 
 
 
 
(0.02) 
 
 
(-0.40) 
𝑆&𝑃 500 𝑉𝐼𝑋𝑡−1 
 
 
-0.150 
 
 
1.575 
 
 
 
(-0.30) 
 
 
(1.60) 
𝑀𝑆𝐶𝐼𝑡−1
𝑊𝑜𝑟𝑙𝑑 
 
 
0.498 
 
 
-1.988 
 
 
 
(0.88) 
 
 
(-1.88) 
𝑆ℎ𝑅𝑎𝑡𝑒𝑡−1 
 
 
-0.007* 
 
 
-0.025 
 
 
 
(-1.82) 
 
 
(-1.62) 
𝑌𝑖𝑒𝑙𝑑 𝑆𝑝𝑟𝑒𝑎𝑑𝑡−1 
 
 
-0.005 
 
 
-0.007 
 
 
 
(-0.51) 
 
 
(-0.18) 
𝑍(𝑑𝑒𝑓𝑎𝑢𝑙𝑡)𝑆𝑝𝑟𝑒𝑎𝑑𝑡−
 
 
-0.006 
 
 
-0.007 
 
 
 
(-0.48) 
 
 
(-0.12) 
R-Squared (%) 
0.1 
0.3 
1.3 
0.2 
0.2 
3.6 
No. of Obs.  
101047 
101047 
101047 
18631 
18631 
18631 
Source: Author's Own Creation 
The table above presents the predictive longitudinal data analysis of cryptocurrency returns, along with lagged 
global order flow and lagged control factors. The table shows the same information as concurrent panel 
regressions, but all the factor variables are lagged and 𝑟𝑒𝑖,𝑡−1 refers to the lagged return of each cryptocurrency 
under study.  Statistics are in parentheses and are calculated using standard errors, grouped by time and coins. The 
out-of-sample testing period runs from February 14th, 2020, to June 30th, 2025.  
The table's results show that global order flows are a highly significant predictor of 
cryptocurrency returns both 1 day and 1 week ahead. The Diurnal predictive regression shows 
an unusual pattern: lagged global order flows are not significant on their own (t-stat = 0.72), 
but when controlling for other factors, their logged returns become highly significant (t-stat = 
2.68). Conversely, the effect of the logged returns is negative and highly significant (t-stat = -
3.35). This suggests that lagged order flows have two opposing influences: a short-term 


## Page 19

reversal associated with lagged returns and a long-term factor that, while uncorrelated with 
lagged returns, is positively linked to future crypto returns. Other variables, including total 
market capitalisation, volatility, and the short rate, are important for the daily regressions. For 
weekly regressions, market capitalisation, MSCI global uncertainty, and volatility are key 
factors. The R-squared values are 1.3% for the daily regression and 3.6% for the weekly 
regression.   
 
Table 8 Concurrent Panel regression with all multinational order flows 
 
Diurnal 
Per Week 
 
(1|) 
(2) 
(3) 
(4) 
Constant term 
0.003 
0.002 
0.063 
0.060 
 
(0.20) 
(0.009) 
(1.29) 
(1.26) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝑊 
 
0.021*** 
 
0.031*** 
 
 
(13.03) 
 
(6.96) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝑈𝑆𝐷 
0.014*** 
0.007*** 
0.028*** 
0.016*** 
 
(8.88) 
(4.50) 
(6.66) 
(4.28) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝐸𝑈𝑅 
0.013*** 
0.008*** 
0.020*** 
0.009*** 
 
(7.76) 
(6.33) 
(5.88) 
(3.82) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝐾𝑅𝑊 
0.005*** 
0.001 
0.0011** 
0.004* 
 
(5.25) 
(0.76) 
(3.99) 
(1.84) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝐺𝐵𝑃 
0.003*** 
-0.001** 
0.006*** 
-0.002 
 
(4.19) 
(-2.40) 
(2.79) 
(-0.50) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝐽𝑃𝑌 
0.001* 
-0.001 
0.002 
-0.002 
 
(1.85) 
(-0.63) 
(0.85) 
(-0.40) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝐶𝐴𝐷 
0.001*** 
-0.001*** 
0.006*** 
0.003 
 
(2.71) 
(-2.73) 
(4.26) 
(1.29) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝐴𝑈𝐷 
0.001 
-0.002*** 
0.002* 
-0.002 
 
(1.55) 
(-3.19) 
(1.88) 
(-0.56) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝐶𝐻𝐹 
0.001 
-0.002*** 
0.002 
-0.002* 
 
(0.82) 
(-6.73) 
(0.36) 
(-1.84) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝑁𝑍𝐷 
0.002 
-0.002*** 
-0.002 
-0.003* 
 
(1.69) 
(-5.73) 
(-0.46) 
(-3.40) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝑁𝑂𝐾 
0.001 
-0.002*** 
0.002 
-0.002 
 
(0.56) 
(-5.11) 
(1.07) 
(-0.36) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝑆𝐸𝐾 
0.001 
-0.002*** 
0.002 
-0.002 
 
(0.84) 
(-5.26) 
(0.83) 
(-0.92) 
R-Squared (%) 
9.8 
12.5 
20.8 
22.2 
No. of Obs.  
101139 
101139 
18723 
18723 
Source: Author's Own Creation 
The table shows a concurrent panel regression of cryptocurrency returns on global order flows, multinational order 
flows, and control factors. It also presents the combined analysis for all multinationals alongside global order 
flows. Statistics are shown in parentheses, calculated with standard errors grouped by time and coins. The out-of-
sample testing covers the period from February 14th, 2020, to June 30th, 2025.  
 
Table 9Exponential Smoothing of Panel Regression—Nonlinear factors test sample period 
Single Predictive Panel Regression  
 
Linear 
Square 
Cubic 
Interrelation with 𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝑊 
Constant 
0.0293 
 
 
 
 
(1.27) 
 
 
 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−1
𝑊
 
0.0044** 
-0.0009* 
-0.0003* 
 
 
(3.50) 
(-1.96) 
(-1.85) 
 


## Page 20

𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−1
𝑈𝑆𝐷 
-0.0001 
0.0002 
0.0001 
0.0005 
 
(-0.10) 
(0.78) 
(1.09) 
(1.00) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−1
𝐸𝑈𝑅 
-0.0007 
-0.0002 
0.0001 
-0.0001 
 
(-1.18) 
(-0.64) 
(0.46) 
(-0.27) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−1
𝐾𝑅𝑊 
0.0016** 
0.0003 
0.0001 
0.0015*** 
 
(2.20) 
(1.06) 
(1.40) 
(2.79) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−1
𝐺𝐵𝑃 
-0.0007 
-0.0001 
0.0001 
0.0000 
 
(-1.17) 
(-0.44) 
(0.77) 
(0.10) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−1
𝐽𝑃𝑌 
0.0002 
-0.001 
-0.0001* 
-0.0000 
 
(0.49) 
(-0.34) 
(-1.93) 
(0.04) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−1
𝐶𝐴𝐷 
-0.0005 
0.0003 
-0.0002 
-0.0002 
 
(-0.83) 
(0.77) 
(-1.25) 
(-0.55) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−1
𝐴𝑈𝐷 
-0.0008 
0.0006** 
0.0000 
-0.0006 
 
(-1.59) 
(1.99) 
(0.42) 
(-1.07) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−1
𝐶𝐻𝐹 
-0.0004 
-0.0009*** 
0.0001 
0.0005 
 
(-0.60) 
(-2.93) 
(1.55) 
(1.27) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−1
𝑁𝑍𝐷 
-0.0003 
0.0005 
0.0000 
-0.0002 
 
(-0.56) 
(1.13) 
(0.60) 
(-0.30) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−1
𝑁𝑂𝐾 
-0.0002 
0.0008** 
-0.0000 
-0.0004 
 
(-0.33) 
(2.44) 
(-0.20) 
(-0.78) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−1
𝑆𝐸𝐾 
-0.0001 
0.0004 
-0.0002 
-0.0009 
 
(-0.21) 
(0.98) 
(-1.08) 
(-1.58) 
𝑟𝑒𝑖,𝑡−1 
-0.0852*** 
0.0450 
-0.0097 
0.0010 
 
(-3.03) 
(0.88) 
(-0.64) 
(1.43) 
F-test (non-linear) 
 
0.068 
0.000 
0.096 
F-test (All non-linear) 
 
0.000 
 
 
𝑅2   (%) 
(Discrete regression) 
1.99 
2.14 
2.21 
2.29 
No. of observations 
101139 
101139 
18723 
18723 
Source: Author's Own Creation 
The table shows the results of a specific predictive regression of cryptocurrency returns on the linear, squared, 
cubic, and cross-product terms of the lagged world order flow and international order flows. The exponential 
smoothing of the panel regressions also accounts for the control variables estimated in the previous tables, but 
these results are not reported to save space. The t-statistics in parentheses are calculated using the standard errors 
grouped by time and coins. The adjusted 𝑅̅2 values are reported at the bottom, along with the four individual 
regressions: the first conditioned only on the linear terms, the second also including squared terms, the third adding 
cubic terms, and the last incorporating all terms. The out-of-sample testing period runs from February 14th, 2020, 
to June 30th, 2025.  
Table 10 Vector Autoregression Result: BTC and XRP 
 
BTC 
XRP 
 
Returns 
Order Flow 
Returns 
Order Flow 
 
Parameter 
(t-stat) 
Parameter 
(t-stat) 
Parameter 
(t-stat) 
Parameter 
(t-stat) 
Constant 
0.013 
0.99 
0.264 
0.99 
-0.010 
(-0.72) 
0.534* 
(2.09) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝑊 
0.025*** 
(13.05) 
 
 
0.047*** 
(12.97) 
 
 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−1
𝑊
 
0.002 
(1.16) 
0.060 
(1.52) 
0.007** 
(2.57) 
0.017 
(0.27) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−2
𝑊
 
-0.001 
(-0.84) 
0.093** 
(3.04) 
0.007* 
(1.99) 
-0.039 
(-0.89) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−3
𝑊
 
-0.001 
(-0.66) 
0.017 
(0.45) 
0.005* 
(1.99) 
0.055 
(1.10) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−4
𝑊
 
0.000 
(0.06) 
0.059 
(1.49) 
-0.005 
(-1.58) 
-0.009 
(-0.19) 


## Page 21

𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−5
𝑊
 
0.005* 
(1.96) 
0.033 
(0.97) 
0.001 
(0.46) 
0.026 
(0.76) 
𝑟𝑒𝑖,𝑡−1 
-0.037 
(-2.27) 
-3.330*** 
(-3.83) 
-0.028 
(-0.83) 
-1.188* 
(-1.78) 
𝑟𝑒𝑖,𝑡−2 
0.043 
(1.29) 
0.395 
(0.39) 
-0.097** 
(-3.44) 
1.376** 
(3.31) 
𝑟𝑒𝑖,𝑡−3 
0.025 
(0.80) 
1.749** 
(2.05) 
-0.042 
(-1.00) 
-0.040 
(-0.09) 
𝑟𝑒𝑖,𝑡−4 
-0.013 
(0.34) 
0.206 
(0.35) 
0.073* 
(1.84) 
0.994* 
(1.85) 
𝑟𝑒𝑖,𝑡−5 
-0.088* 
(-1.94) 
-1.068 
(-1.27) 
-0.009 
(17) 
-0.085 
(-0.26) 
𝑀𝐶𝐴𝑃𝑖,𝑡−1 
-0.005 
(-0.63) 
-0.067 
(-0.58) 
-0.019** 
(-2.50) 
-0.365*** 
(-3.70) 
𝑉𝑜𝑙𝑢𝑚𝑒𝑖,𝑡−1 
-0.006 
(-0.88) 
-0.008 
(-0.08) 
0.006 
(0.60) 
-0.068 
(-0.98) 
𝑉𝑜𝑙𝑎𝑡𝑖𝑙𝑖𝑡𝑦𝑖,𝑡−1 
0.086** 
(2.22) 
0.497 
(0.56) 
0.050 
(0.98) 
1.534*** 
(3.95) 
𝑉𝐼𝑋𝑡−1 
0.037 
(1.57) 
-0.590 
(-0.99) 
-0.050 
(-1.37) 
-0.554 
(-0.96) 
𝑇𝐸𝐷 𝑆𝑝𝑟𝑒𝑎𝑑𝑡−1 
0.000 
(0.10) 
-0.001 
(0.75) 
0.00 
(-0.96) 
-0.001 
(-0.76) 
𝑆&𝑃500𝑡−1 
0.412 
(0.86) 
-11.7000 
(-2.48) 
-0.795* 
(-1.93) 
3.925 
(0.52) 
𝑀𝑆𝐶𝐼𝑡−1
𝐺𝑙𝑜𝑏𝑎𝑙 
-0.080 
(-0.25) 
10.956 
(1.34) 
0.970** 
(2.24) 
-2.506 
(-0.25) 
𝑆ℎ𝑜𝑟𝑡 𝑟𝑎𝑡𝑒𝑡−1 
-0.008* 
(-2.55) 
-0.082 
(-0.93) 
0.006 
(0.86) 
-0.092 
(-1.00) 
𝑇𝑒𝑟𝑚 𝑆𝑝𝑟𝑒𝑎𝑑 𝑡−1 
-0.008 
(-2.10) 
-0.019 
(-0.16) 
0.019* 
(1.88) 
0.030 
(0.30) 
𝐷𝑒𝑓𝑎𝑢𝑙𝑡 𝑆𝑝𝑟𝑒𝑎𝑑 𝑡−1 
0.000 
(0.05) 
-0.142 
(-0.69) 
-0.006 
(-0.64) 
-0.552*** 
(-3.82) 
𝑅2   (%) 
30.88 
 
1.81 
 
47.81 
 
2.24 
 
Source: Author's Own Creation 
The table above presents vector autoregressions (VARs) of cryptocurrency returns and order flow for two coins: 
Bitcoin (BTC) and XRP (Ripple). The VAR stipulations follow [25].  T-statistics shown in parentheses are 
computed using the standard errors that are clustered both by time and coin. The out-of-sample testing period runs 
from February 18, 2020, to June 30, 2025.  
Table 11 Portfolios sorted based on the U.S. order flow 
Part A: Daily Portfolios Sorted based on US order Flow 
 
𝑃𝑟1 
𝑃𝑟2 
𝑃𝑟3 
𝑃𝑟4 
𝑃𝑟5 
𝑃𝑟5 −𝑃𝑟1 
 
Mean Returns (% Daily) 
Mean 
Alpha 
SR 
𝑂𝑟𝐹𝑙𝑜𝑤𝑈𝑆𝐷 
0.51 
(2.15) 
0.48 
(1.90) 
0.43 
(1.70) 
0.46 
(1.85) 
0.43 
(1.721) 
-0.09 
(-0.81) 
-0.09 
(-0.75) 
-0.49 
Ortho- 
𝑂𝑟𝐹𝑙𝑜𝑤𝑈𝑆𝐷 
0.49 
(2.00) 
0.47 
(1.90) 
0.33 
(1.34) 
0.50 
(2.05) 
0.50 
(2.03) 
0.01 
(0.10) 
0.03 
(0.27) 
0.07 
Part B: Daily Portfolios Sorted based on US order Flow 
 
𝑃𝑟1 
𝑃𝑟2 
𝑃𝑟3 
𝑃𝑟4 
𝑃𝑟5 
𝑃𝑟5 −𝑃𝑟1 
 
Mean Returns (% Daily) 
Mean 
Alpha 
SR 
𝑂𝑟𝐹𝑙𝑜𝑤𝑈𝑆𝐷 
1.18 
(0.91) 
2.56 
(1.84) 
2.00 
(1.55) 
2.50 
(1.85) 
3.02 
(2.29) 
1.85 
(3.16) 
1.78 
(2.84) 
1.95 
Ortho- 
𝑂𝑟𝐹𝑙𝑜𝑤𝑈𝑆𝐷 
1.05 
(0.78) 
2.26 
(1.75) 
2.51 
(1.79) 
2.61 
(1.98) 
2.85 
(2.16) 
1.80 
(3.12) 
1.61 
(2.72) 
1.98 
Source: Author's Own Creation 
The table above shows the performance of the cryptocurrency portfolios classified by the U.S. order flow 
𝑂𝑟𝐹𝑙𝑜𝑤𝑈𝑆𝐷, 𝑂𝑟𝑡ℎ𝑜−𝑂𝑟𝐹𝑙𝑜𝑤𝑈𝑆𝐷 refers to the US order flow that is orthogonal to the same-period returns. 𝑃𝑟1 
refers to the portfolio with the lowest lagged order flow, and 𝑃𝑟5 shows the portfolio encompassing the highest 
lagged order flow. The portfolios are equally weighted and recalculated daily (Part A) or weekly (Part B). The 
alpha is explained by a three-factor model comprising the cryptocurrency market, size, and momentum factors 
[30]. The returns and the alphas are converted into daily/weekly percentages. SR refers to the annual Sharpe Ratio. 
The Newey and West (1987) t-statistics are shown in parentheses. The out-of-sample testing period runs from 
February 18, 2020, to June 30, 2025.  
Table 12 Daily portfolios classified on ML forecasts 


## Page 22

 
OF Model 
EF Model 
OF + EF model 
 
𝑷𝟓− 𝑷𝟏 
𝑷𝟓− 𝑷𝟏 
𝑷𝟓− 𝑷𝟏 
 
Mean  
Alpha (α) 
ASR 
Mean  
Alpha (α) 
ASR 
Mean  
Alpha (α) 
ASR 
OLS 
(t-stat) 
-0.18 
(-1.04) 
-0.17 
(-0.98) 
-0.68 
-0.04 
(-0.13) 
0.04 
(0.11) 
-0.09 
-0.11 
(-0.56) 
-0.08 
(-0.41) 
-0.36 
RR 
(t-stat) 
-0.15 
(-0.87) 
-0.15 
(-0.83) 
-0.57 
-0.09 
(-0.44) 
-0.06 
(-0.22) 
-0.28 
-0.13 
(-0.72) 
-0.10 
(-0.58) 
-0.46 
LAS 
(t-stat) 
-0.20 
(-1.29) 
-0.20 
(-1.25) 
-0.83 
0.13 
(0.98) 
0.13 
(0.95) 
0.62 
0.14 
(1.10) 
0.15 
(1.07) 
0.69 
EN 
(t-stat) 
-0.15 
(-0.88) 
-0.13 
(-0.72) 
-0.56 
-0.03 
(-0.06) 
0.04 
(0.14) 
-0.04 
0.00 
(-0.10) 
0.02 
(0.16) 
-0.01 
PCR 
(t-stat) 
-0.07 
(-0.34) 
-0.06 
(-0.30) 
-0.22 
0.00 
(0.02) 
-0.06 
(-0.25) 
0.03 
-0.04 
(-0.17) 
-0.09 
(-0.45) 
-0.11 
RF 
(t-stat) 
0.42 
(2.59) 
0.44 
(2.82) 
1.74 
-0.23 
(-1.46) 
-0.21 
(-1.31) 
-0.93 
-0.12 
(-0.70) 
-0.13 
(-0.74) 
-0.45 
SGB 
(t-stat) 
0.55 
(3.27) 
0.58 
(3.50) 
2.16 
0.24 
(1.92) 
0.23 
(1.91) 
1.22 
0.20 
(1.61) 
0.21 
(1.63) 
1.03 
NN1 
(t-stat) 
0.13 
(0.71) 
0.17 
(0.95) 
0.45 
-0.29 
(-1.69) 
-0.25 
(-1.39) 
-1.03 
-0.15 
(-0.84) 
-0.12 
(-0.60) 
-0.53 
NN2 
(t-stat) 
-0.07 
(-0.31) 
0.00 
(0.02) 
-0.20 
-0.02 
(-0.11) 
0.02 
(0.10) 
-0.07 
-0.10 
(-0.59) 
-0.06 
(-0.28) 
-0.39 
NN3 
(t-stat) 
-0.05 
(-0.24) 
-0.04 
(-0.12) 
-0.16 
-0.12 
(-0.70) 
-0.10 
(-0.63) 
-0.47 
-0.19 
(-1.05) 
-0.15 
(-0.82) 
-0.67 
NN4 
(t-stat) 
-0.08 
(-0.44) 
-0.07 
(-0.30) 
-0.27 
-0.14 
(-0.90) 
-0.09 
(-0.51) 
-0.53 
-0.09 
(-0.53) 
-0.04 
(-0.21) 
-0.35 
L-Mean 
(t-stat) 
0.00 
(0.00) 
0.00 
(0.03) 
0.00 
-0.09 
(-0.49) 
-0.05 
(-0.22) 
-0.30 
-0.09 
(-0.47) 
 
-0.06 
(-0.28) 
-0.29 
NL-Mean 
(t-stat) 
0.44 
(2.80) 
0.48 
(2.96) 
1.79 
-0.38 
(-2.21) 
-0.34 
(-1.83) 
-1.36 
-0.19 
(-1.11) 
-0.15 
(-0.82) 
-0.71 
Source: Author's Own Creation 
The table above presents the performance of a cryptocurrency portfolio, segmented by Machine 
Learning forecasts, using the top 20 cryptocurrencies by market cap as of February 15, 2020. 
ML techniques are applied to a full cross-sectional sample of 128 coins. The top portfolio 
(𝑃𝑜𝑟𝑡3) includes the five coins with the highest ML forecasts, while the bottom portfolio 
(𝑃𝑜𝑟𝑡3) contains the coins with the lowest forecasts. Both portfolios are equally weighted and 
rebalanced daily. The study analyses three ML models: one where order flow depends only on 
itself; another where EF depends on economic indicators; and a third where OF+EF jointly 
constrain both. All models depend on lagged returns. The alpha is computed using a three-
factor model including the crypto market, size, and momentum (Liu, Tsyvinski, and Wu, 2022). 
Returns and alpha are presented daily in percentage terms. SR denotes the annualised Sharpe 
Ratio, with Newey-West (1987) t-statistics in parentheses. Bold figures indicate the highest 
Sharpe ratio for each ML model across the three datasets (OF, EF, OF+EF). The out-of-sample 
test periods range from February 18, 2020, to June 30, 2025. sets (O  F, EF, OF+EF). The out-
of-sample test sample periods are from February 18, 2020, to June 30, 2025.  
Table 13: Momentum Factor Betas 
𝜷𝒎𝒐𝒎𝒇𝒂𝒄𝒕𝒐𝒓 
 
OF 
EF 
OF+EF 
OLS 
(t-stat) 
12.97 
(-2.26) 
-13.78 
(-2.36) 
-8.92 
(1.56) 
RidRegre 
11.86 
-14.80 
-11.38 


## Page 23

(t-stat) 
(-2.08) 
(-2.53) 
(-2.00) 
LASso 
(t-stat) 
-3.82 
(-0.76) 
-7.34 
(-1.63) 
-7.70 
(-1.71) 
EN 
(t-stat) 
-5.56 
(-1.07) 
-11.18 
(-2.29) 
-11.48 
(-2.35) 
PCR 
(t-stat) 
15.21 
(-2.75) 
8.44 
(-1.57) 
3.35 
(-0.65) 
RForest 
(t-stat) 
-11.30 
(-2.20) 
6.17 
(-1.13) 
-1.70 
(-0.31) 
SGBD 
(t-stat) 
-5.72 
(-1.11) 
-1.44 
(-0.32) 
-1.44 
(-0.32) 
NN1 
(t-stat) 
-3.76 
(-0.70) 
-9.25 
(-1.56) 
-14.91 
(-2.84) 
NN2 
(t-stat) 
-7.92 
(-1.45) 
1.65 
(-0.28) 
-0.49 
(-0.09) 
NN3 
(t-stat) 
-4.69 
(-0.87) 
-19.07 
(-3.53) 
-6.21 
(-1.11) 
NN4 
(t-stat) 
-16.08 
(-3.04) 
-11.98 
(-2.39) 
-17.45 
(-3.35) 
L-Mean 
(t-stat) 
16.17 
(-2.79) 
-14.50 
(-2.45) 
-10.13 
(-1.78) 
NL-Mean 
(t-stat) 
-9.10 
(-1.69) 
-8.50 
(-1.54) 
-7.55 
(-1.36) 
Source: Author's Own Creation 
Note: The table above presents the momentum factor betas for long-short portfolio returns, sorted by ML forecasts, 
relative to the three-factor model (Liu et al., 2022). The portfolios are equally weighted and recalculated daily. 
The daily results are provided for three information sets: OF, based solely on order flows; EF, based on economic 
fundamentals; and OF+EF, incorporating both. All models rely on lagged returns. The out-of-sample testing 
period runs from February 18, 2020, to June 30, 2025.  
Table 14 Vector Autoregression Results 
 
BTC 
ETH 
USDT 
BNB 
XRP 
USDC 
SOL  
TRX 
DOGE 
BCH 
Top 10 
All 128 
Rate of Return Parity 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝑊 
0.025*** 
0.035*** 
0.048*** 
0.032*** 
0.025*** 
0.050*** 
0.045*** 
0.026*** 
0.048*** 
0.048*** 
0.038*** 
0.023*** 
 
(13.05) 
(12.90) 
(12.71) 
(9.03) 
(8.40) 
(20.66) 
(10.73) 
(8.03) 
(15.44) 
(15.44) 
(30.28) 
(28.73) 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−1
𝑊
 
0.004 
0.000 
0.008** 
0.000 
0.007** 
0.008* 
0.008* 
-0.003 
0.004 
0.010*** 
0.005*** 
0.005*** 
 
(1.26) 
(0.27) 
(20.22) 
(0.14) 
(2.32) 
(2.20) 
(1.82) 
(-0.63) 
(1.06) 
(3.20) 
(3.51) 
(5.41) 
∑
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−𝑗
𝑊
𝑗=5
𝑗=1
 
 
0.005 
0.004 
0.016** 
0.012* 
0.016*** 
0.018*** 
0.012 
0.004 
0.019*** 
0.019*** 
0.009*** 
0.006*** 
 
(0.90) 
(0.61) 
(2.15) 
(1.95) 
(3.83) 
(2.96) 
(1.41) 
(0.48) 
(2.14)) 
(3.41) 
(4.56) 
(3.06) 
𝑟𝑒𝑖,𝑡−1 
-0.037 
-0.018 
-0.030 
0.012 
-0.068** 
-0.048 
0.046 
0.003 
-0.021 
-0.060* 
-0.018 
0.000 
 
(-1.29) 
(-0.63) 
(-0.75) 
(0.24) 
(-2.49) 
(-1.31) 
(0.79) 
(0.06) 
(-0.72) 
(-1.83) 
(-1.17) 
(-0.19) 
∑
𝑟𝑒𝑖,𝑡−𝑗
𝑗=5
𝑗=1
 
-0.59 
0.014 
-0.099 
0.031 
-0.136** 
-0.164* 
-0.026 
0.026 
-0.052 
-0.131 
-0.043* 
-0.057* 
 
(-0.83) 
(0.18) 
(-0.97) 
(0.41) 
(-1.99) 
(-1.74) 
(-0.39) 
(0.36) 
(-0.76) 
(-1.31) 
(-1.70) 
(-1.77) 
R-squared (%) 
28.5 
35.3 
44.0 
21.3 
16.2 
47.6 
39.3 
13.5 
43.3 
37.0 
31.5 
7.8 
Order Flow Parity 
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡
𝑊 
0.062 
-0.057 
0.018 
-0.153** 
-0.027 
-0.090* 
0.041 
-0.014 
-0.026 
-0.096 
-0.035** 
-0.013 
 
(1.54) 
(-1.13) 
(0.27) 
(-2.56) 
(-0.75) 
(-1.81) 
(0.65) 
(-0.28) 
(-0.59) 
(-2.05) 
(-2.05) 
(-1.72) 
∑
𝑂𝑟𝐹𝑙𝑜𝑤𝑖,𝑡−𝑗
𝑊
𝑗=5
𝑗=1
 
 
0.239*** 
 
0.008 
 
0.061 
 
-
0.295*** 
 
-0.053 
 
0.030 
0.020 
0.088 
-0.040 
-0.066 
0.030 
0.033*** 
 
(3.05) 
(0.09) 
(0.45) 
(-2.68) 
(-0.76) 
(0.25) 
(0.25) 
(1.11) 
(-0.46) 
(-0.69) 
(0.69) 
(2.45) 
𝑟𝑒𝑖,𝑡−1 
-
2.333*** 
-0.005 
-1.195* 
0.444 
-0.396 
-0.605 
-
2.127*** 
-0.996 
-1.315** 
-0.889 
-
0.949*** 
0436*** 
 
(-2.85) 
(0.00) 
(-1.85) 
(0.72) 
(-0.63) 
(-0.85) 
(-3.45) 
(-1.84) 
(-2.09) 
(-1.39) 
(-4.66) 
(-5.95) 
∑
𝑟𝑒𝑖,𝑡−𝑗
𝑗=5
𝑗=1
 
 
-1.163 
 
0.631 
 
0.856 
 
2.658* 
 
0.236 
 
0.015 
 
-1.325 
 
-0.396 
0.299 
0.005 
-0.151 
-0.335** 
 
(-0.67) 
(0.49) 
(0.65) 
(1.90) 
(0.17) 
(0.02) 
(-1.13) 
(-0.35) 
(0.26) 
(0.02) 
(-0.37) 
(-2.09) 
R-squared (%) 
1.9 
1.8 
2.4 
2.9 
0.6 
2.5 
1.4 
0.0 
0.5 
2.6 
1.9 
0.6 


## Page 24

 
Table 15: Duple-types or double-sorted portfolios—economic fundamentals 
Linear ML Forest Combination (L-mean) 
 
𝑷𝒓𝟏 
𝑷𝒓𝟐 
𝑷𝒓𝟑 
𝑷𝒓𝟑−𝑷𝒓𝟏 
 
 
Mean 
Returns 
(% Daily) 
Mean 
Alpha 
SR 
𝑹𝒆𝒐𝒐𝒔
𝟐 
Arbitrage    1 
0.59 
0.59 
0.46 
-0.13 
-0.10 
-0.64 
-4.59 
Index 
(2.39) 
(2.44) 
(1.49) 
(-0.97) 
(-0.79) 
 
 
2 
0.40 
0.86 
0.51 
0.11 
0.22 
0.37 
-2.32 
 
(1.50) 
(3.28) 
(1.94) 
(0.56) 
(1.18) 
 
 
3 
0.23 
0.62 
1.03 
0.79 
0.92 
2.53 
-1.93 
 
(0.86) 
(2.38) 
(3.78) 
(0.09) 
(4.53) 
 
 
Source: Author's Own Creation. 
Note: The table presents the performance of the dual-sorted cryptocurrency portfolios for models subject to 
economic fundamentals (EF). The data is first sorted by the arbitrage index, using quantiles of size, idiosyncratic 
volatility, and illiquidity.  The second sort is carried out by the linear ML forest combination (L-mean), which is 
based on EF, and the non-linear ML forecast combination (NL-Mean) for the EF model. The portfolios sorted are 
equally weighted and reconciled daily. The alpha, based on the three-factor model, includes the crypto market, 
size, and momentum factors [25]. The average returns and alphas are expressed in daily percentages. SR refers to 
the Sharpe Ratio. The Newey and West, t-statistics are shown in parentheses. The table also shows the 𝑅𝑒𝑜𝑜𝑠
2  in 
percentage form for both the ML models for each level of the arbitrage index. The out-of-sample test period is 
from February 18, 2020, to June 30, 2025.  
 
Conclusion 
The rapid rise of cryptocurrencies is creating a new branch of financial econometrics, focusing 
on out-of-sample predictions of crypto returns and the analysis of consistently profitable 
trading strategies. Our research enhances understanding of how economic indicators of order 
flow can forecast crypto returns and extends beyond these indicators. We provide empirical 
evidence of a non-linear relationship between order flows and crypto returns, explaining why 
non-linear machine learning models outperform linear ones based on order flows. Additionally, 
the study shows that this relationship varies across coins, indicating that not all are equally 
affected by the magnitude of the price push. When comparing the top crypto coins to the other 
128, this relationship becomes stronger. The effectiveness of non-linear order flow methods 
remains robust despite economic constraints such as short-selling limits, transaction costs, and 
arbitrage restrictions, supporting the consistent impact of order flow on crypto returns. Our 
multivariate portfolio analysis demonstrates that non-linear order flow models generate 
profitable results not only for minute, illiquid, and highly volatile coins, but also for the top 20 
coins by market cap, as further validated by objective economic measures.  
This paper provides a comprehensive analysis of out-of-sample predictability in 
cryptocurrencies, using a large cross-sectional dataset of daily excess returns. It includes a wide 
Non-Linear ML Forest Combination (NL-mean) 
 
𝑷𝒓𝟏 
𝑷𝒓𝟐 
𝑷𝒓𝟑 
𝑷𝒓𝟑−𝑷𝒓𝟏 
 
 
Mean 
Returns 
(% Daily) 
Mean 
Alpha 
SR 
𝑹𝒆𝒐𝒐𝒔
𝟐 
Arbitrage    1 
0.50 
0.61 
0.54 
0.03 
0.07 
0.20 
0.31 
Index 
(2.12) 
(2.53) 
(2.15) 
(0.31) 
(0.48) 
 
 
2 
0.36 
0.63 
0.79 
0.43 
0.49 
1.62 
0.32 
 
(1.41) 
(2.46) 
(2.86) 
(2.55) 
(2.78) 
 
 
3 
0.19 
0.79 
0.91 
0.72 
0.82 
2.34 
0.12 
 
(0.75) 
(2.69) 
(3.44) 
(3.45) 
(4.04) 
 
 


## Page 25

range of economic indicators across categories and employs recent machine learning 
techniques to forecast crypto returns. Combining these predictors with machine learning 
enhances the accuracy of out-of-sample forecasts for daily cross-sectional cryptocurrency 
returns, as measured by the out-of-sample mean squared deviation (MSD). These forecasts are 
then used to optimise portfolios, which offer significant utility to investors. Such investors 
allocate assets among individual cryptocurrencies, T-bills, and long-short portfolios (LSE) that 
include cryptocurrencies with the highest or lowest return forecasts. This strategy yields high 
Sharpe, Calmar, and Sortino ratios and generates notable alphas, consistent with the [25] 
cryptocurrency three-factor model. Order flow plays a key role in explaining and predicting 
cross-sectional cryptocurrency returns. In in-sample regression analysis, world order flow 
shows persistent correlation and a causal link with crypto returns. Using nonlinear machine 
learning techniques to analyse data from all global order flows suggests high out-of-sample 
forecasting accuracy. This is supported by the very high economic value, with a forecast Sharpe 
ratio of 0.86 for the long portfolio and 3.97 for the long-short portfolios. Overall, our results 
remain robust even when accounting for factors such as short-selling constraints, transaction 
costs, and arbitrage limits, providing strong empirical support for the influence of order flow 
on crypto returns.  
In conclusion, the evidence indicates that order flow information is significantly relevant for 
understanding cryptocurrency returns. The economic value of ML models that do not condition 
on order flow is clearly explained by arbitrage limits evident in the stock, options, and crypto 
markets. Ultimately, observational evidence strongly indicates that order-flow information is 
important for predicting cryptocurrency returns and is robust to economic restrictions. 
References 
1. Anastasopoulos, 
A. 
(2025). Three 
Essays 
on 
Order 
Flow 
and 
Cryptocurrency 
Returns (Doctoral dissertation, University of Guelph). 
2. Avramov, D., Cheng, S., & Metzker, L. (2023). Machine learning vs. economic restrictions: 
Evidence from stock return predictability. Management Science, 69(5), 2587-2619. 
3. Berger, D. W., Chaboud, A. P., Chernenko, S. V., Howorka, E., & Wright, J. H. (2008). Order 
flow and exchange rate dynamics in electronic brokerage system data. Journal of international 
Economics, 75(1), 93-109. 
4. Bianchi, D., Babiak, M., & Dickerson, A. (2022). Trading volume and liquidity provision in 
cryptocurrency markets. Journal of Banking & Finance, 142, 106547. 
5. Breiman, L., Friedman, J., Olshen, R. A., & Stone, C. J. (1984). Classification and regression 
trees, Chapman and Hall/CRC. Chapman Hall/CRC. 
6. Breiman, L., Friedman, J., Olshen, R. A., & Stone, C. J. (2017). Classification and regression 
trees. Chapman and Hall/CRC. 
7. Campbell, J. Y., & Thompson, S. B. (2008). Predicting excess stock returns out of sample: Can 
anything beat the historical average?. The Review of Financial Studies, 21(4), 1509-1531. 
8. Cakici, N., Shahzad, S. J. H., Będowska-Sójka, B., & Zaremba, A. (2024). Machine learning 
and the cross-section of cryptocurrency returns. International Review of Financial Analysis, 94, 
103244. 
9. Daubechies, I., Defrise, M., & De Mol, C. (2004). An iterative thresholding algorithm for linear 
inverse problems with a sparsity constraint. Communications on Pure and Applied 
Mathematics: A Journal Issued by the Courant Institute of Mathematical Sciences, 57(11), 
1413-1457. 
10. Detzel, A., Liu, H., Strauss, J., Zhou, G., & Zhu, Y. (2021). Learning and predictability via 
technical analysis: Evidence from bitcoin and stocks with hard‐to‐value fundamentals. Financial 
management, 50(1), 107-137. 


## Page 26

11. Diebold, F. X., & Mariano, R. S. (2002). Comparing predictive accuracy. Journal of Business & 
economic statistics, 20(1), 134-144. 
12. Evans, M. D., & Lyons, R. K. (2002). Order flow and exchange rate dynamics. Journal of 
political economy, 110(1), 170-180. 
13. Evans, M. D., & Lyons, R. K. (2005). Do currency markets absorb news quickly?. Journal of 
International Money and Finance, 24(2), 197-217. 
14. Fama, E. F. and K. R. French (1989). Business conditions and the expected returns on 
stocks and bonds. Journal of Financial Economics 25 (1), 23–49 
15. Filippou, I., Rapach, D., Taylor, M. P., & Zhou, G. (2025). Economic fundamentals and short-
run exchange rate prediction: A machine-learning perspective. Available at SSRN 3455713. 
16. Foucault, T., Pagano, M., & Röell, A. (2023). Market liquidity: theory, evidence, and policy. 
Oxford University Press. 
17. Fieberg, C., Liedtke, G., Poddig, T., Walker, T., & Zaremba, A. (2025). A Trend Factor for the 
Cross Section of Cryptocurrency Returns. Journal of Financial and Quantitative Analysis, 60(7), 
3116-3153. 
18. Friedman, J., Hastie, T., Höfling, H., & Tibshirani, R. (2007). Pathwise coordinate optimization. 
19. Freyberger, 
J., 
Neuhierl, 
A., 
& 
Weber, 
M. 
(2020). 
Dissecting 
characteristics 
nonparametrically. The Review of Financial Studies, 33(5), 2326-2377. 
20. Froot, K. A., & Ramadorai, T. (2005). Currency returns, intrinsic value, and institutional‐investor 
flows. The Journal of Finance, 60(3), 1535-1566. 
21. Glosten, L. R., & Milgrom, P. R. (1985). Bid, ask and transaction prices in a specialist market 
with heterogeneously informed traders. Journal of financial economics, 14(1), 71-100. 
22. Gradojevic, N., Kukolj, D., Adcock, R., & Djakovic, V. (2023). Forecasting Bitcoin with technical 
analysis: A not-so-random forest?. International Journal of Forecasting, 39(1), 1-17. 
23. Gu, S., Kelly, B., & Xiu, D. (2020). Empirical asset pricing via machine learning. The Review of 
Financial Studies, 33(5), 2223-2273. 
24. Hasbrouck, J. (1988). Trades, quotes, inventories, and information. Journal of financial 
economics, 22(2), 229-252. 
25. Hasbrouck, J. (1991). Measuring the information content of stock trades. The Journal of 
Finance, 46(1), 179-207. 
26. Hoerl, A. E., & Kennard, R. W. (1970). Ridge regression: applications to nonorthogonal 
problems. Technometrics, 12(1), 69-82. 
27. Hornik, K., Stinchcombe, M., & White, H. (1989). Multilayer feedforward networks are universal 
approximators. Neural networks, 2(5), 359-366. 
28. Kyle, A. S. (1985). Continuous auctions and insider trading. Econometrica: Journal of the 
Econometric Society, 1315-1335. 
29. Liu, Y., & Tsyvinski, A. (2021). Risks and returns of cryptocurrency. The Review of Financial 
Studies, 34(6), 2689-2727. 
30. Liu, Y., Tsyvinski, A., & Wu, X. (2022). Common risk factors in cryptocurrency. The Journal of 
Finance, 77(2), 1133-1177. 
31. Makarov, I., & Schoar, A. (2020). Trading and arbitrage in cryptocurrency markets. Journal of 
Financial Economics, 135(2), 293-319. 
32. Martin, I. W., & Nagel, S. (2022). Market efficiency in the age of big data. Journal of financial 
economics, 145(1), 154-177 
33. Menkhoff, L., Sarno, L., Schmeling, M., & Schrimpf, A. (2016). Information flows in foreign 
exchange markets: Dissecting customer currency trades. The Journal of Finance, 71(2), 601-
634. 
34. Most 
Challenging 
Machine 
Learning 
Problems 
https://www.cudocompute.com/blog/what-are-the-most-challenging-machine-
learning-problems 
35. Nagel, S. (2021). Machine learning in asset pricing. 
36. Neal, P., Eric, C., Borja, P., & Jonathan, E. (2011). Distributed optimization and statistical 
learning via the alternating direction method of multipliers. Foundations and Trends® in 
Machine learning, 3(1), 1-122. 


## Page 27

37. Parikh, N., & Boyd, S. (2014). Proximal algorithms. Foundations and Trends in 
optimization, 1(3), 127-239. 
38. Parikh, N., & Boyd, S. (2014). Block splitting for distributed optimization. Mathematical 
Programming Computation, 6(1), 77-102. 
39. Polson, N. G., Scott, J. G., & Willard, B. T. (2015). Proximal algorithms in statistics and machine 
learning. Statistical Science, 559-581. 
40. Rapach, D. E., Strauss, J. K., & Zhou, G. (2010). Out-of-sample equity premium prediction: 
Combination forecasts and links to the real economy. The Review of Financial Studies, 23(2), 
821-862. 
41. Tibshirani, R. (1996). Regression shrinkage and selection via the lasso. Journal of the Royal 
Statistical Society Series B: Statistical Methodology, 58(1), 267-288. 
42. Timmermann, A. (2006). Forecast combinations. Handbook of economic forecasting, 1, 135-
196. 
43. Welch, I., & Goyal, A. (2008). A comprehensive look at the empirical performance of equity 
premium prediction. The Review of Financial Studies, 21(4), 1455-1508. 
44. Zou, H., & Hastie, T. (2005). Regularization and variable selection via the elastic net. Journal 
of the Royal Statistical Society Series B: Statistical Methodology, 67(2), 301-320. 
 


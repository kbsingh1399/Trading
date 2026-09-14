# Forecasting Volatility with Machine Learning and Rough

- **Source File**: `ssrn-4626835.pdf`
- **Total Pages**: 25
- **SSRN ID**: `ssrn-4626835`

---


### Page 1

Forecasting Volatility with Machine Learning and Rough
Volatility: Example from the Crypto-Winter
Siu Hin Tang∗, Mathieu Rosenbaum†, and Chao Zhou‡
November 2, 2023
Abstract. We extend the application and test the performance of a recently
introduced volatility prediction framework encompassing LSTM and rough volatil-
ity. Our asset class of interest is cryptocurrencies, at the beginning of the “crypto-
winter” in 2022. We ﬁrst show that to forecast volatility, a universal LSTM approach
trained on a pool of assets outperforms traditional models. We then consider a par-
simonious parametric model based on rough volatility and Zumbach e↵ect.
We
obtain similar prediction performances with only ﬁve parameters whose values are
non-asset-dependent. Our ﬁndings provide further evidence on the universality of
the mechanisms underlying the volatility formation process.
Keywords – Machine learning, LSTM, rough volatility, quadratic rough Heston,
Zumbach e↵ect, cryptocurrencies, Bitcoin
∗Department of Mathematics, National University of Singapore; email: s.h.tang@u.nus.edu
†CMAP, Ecole Polytechnique email: mathieu.rosenbaum@polytechnique.edu
‡Department of Mathematics and Risk Management Institute, National University of Singapore;
email: matzc@nus.edu.sg
1


### Page 2

1
Introduction
In [31], classical parametric models, non-parametric Long Short-Term Memory
(LSTM), as well as a novel parsimonious rough volatility-based predictor are used
to predict stocks’ volatility. The authors are successful in establishing some uni-
versal mechanism in the volatility formation process, and the rough volatility-based
framework of [31] is able to forecast volatility better than traditional methods. In
this paper, we are thus interested in testing the applicability and robustness of this
approach by adapting the volatility forecasting framework to a di↵erent class of as-
set. Here we choose cryptocurrencies which is a much newer and younger market.
Serving as a companion paper to [31], we aim at answering two questions in this
work:
• Whether the devices used in the original paper predict volatility well for cryp-
tocurrencies at the beginning of the so-called “crypto-winter”.
• Whether the volatilities have the same properties as observed for stocks, such
as the universality of their formation process across coins during this period.
Bitcoin, proposed in [28], is a decentralized payment system where transactions
are stored with blockchain technology, leveraging cryptographic algorithms. Many
similar systems were introduced and formed a completely new asset class known
as cryptocurrencies. Such electronic currencies o↵er many unique advantages over
traditional ﬁat money. Since conception, cryptocurrencies have been a popular re-
search topic in the academic community and have also received a lot of interest from
ﬁnancial institutions and the general public alike [2, 6, 10, 15, 19, 26]. The recent
work [32] provided evidence that Bitcoin’s volatility is rough, further justifying the
inclusion of the rough volatility model in our work. The rapid increase in the num-
2


### Page 3

ber of listed coins on major cryptocurrency exchanges in recent years makes it more
feasible to apply machine learning models such as the LSTM, and to demonstrate
universality features.
The year 2022 corresponds to a signiﬁcant price and volume drop in cryptocur-
rencies compared to the peak in late 2021, or the beginning of a “crypto-winter”
1 2 3 4. For example, we display in Figure 1 the prices and volumes from the two
largest coins Bitcoin (BTC) and Ethereum (ETH).
Figure 1: Price and weekly USDT trading volume of BTC and ETH, with the period
Jan to Jun 2022 shaded.
There have been a few studies focusing on using machine learning to predict cryp-
tocurrency volatility. In [11], deep neural networks are used to model the volatilities
of the three most popular cryptocurrencies. The papers [24] and [1] consider a hybrid
1Mccrank, J. (2022, February 14). Wall St Week Ahead Crypto investors face more uncertainty
after rocky start to 2022. Reuters. https://www.reuters.com/business/ﬁnance/wall-st-week-ahead-
crypto-investors-face-more-uncertainty-after-rocky-start-2022-2022-02-11/
2Harrison,
E.
(2022,
May
10).
The
crypto
winter
is
here.
Bloomberg.com.
https://www.bloomberg.com/news/newsletters/2022-05-10/the-crypto-winter-is-here
3Howcroft, E. (2022, June 13).
Cryptocurrency market value slumps under $1 trillion.
Reuters.
https://www.reuters.com/business/ﬁnance/cryptocurrency-market-value-slumps-under-
1-trillion-2022-06-13/
4Coingecko.
(2023).
2022
Annual
Crypto
Industry
Report.
CoinGecko.
https://www.coingecko.com/research/publications/2022-annual-crypto-report
3


### Page 4

approach combining neural networks and GARCH models to model cryptocurrency
volatility, with the former using only Bitcoin and the latter using 27 coins. Com-
pared with existing literature, we use a much larger set of 213 cryptocurrencies
which enables us to show the universality of the volatility formation process across
the asset class.
The rough volatility paradigm allows us to generate stylized facts of realized
volatility [5, 16]. It is also e↵ective in pricing and hedging derivatives [4, 12, 13, 14].
With the simplest version of this approach, namely the rough fractional stochastic
volatility (RFSV) model, volatility forecasts can be made with a simple formula
that requires essentially one parameter, namely the Hurst parameter. The Hurst
parameter is systematically around 0.1 for all di↵erent asset classes [5, 16, 33], giv-
ing a quasi-universal volatility model and suggesting universality in the volatility
formation process across assets. In this paper, we also estimate the Hurst parameter
for many cryptocurrencies and demonstrate the same observation.
In [31], the authors presume that the universal volatility formation mechanism
involves past returns. They extend the RFSV approach incorporating strong Zum-
bach e↵ect [34] which corresponds to the feedback e↵ect of price trends on volatility.
To do so they incorporate a quadratic rough Heston (QRH) component to the RFSV.
We recall the QRH model is particularly popular as it is able to reproduce market
observations of SPX and VIX options [17, 30] thanks to its rough nature and the
Zumbach e↵ect.
We focus on the problem of forecasting the daily volatility of cryptocurrencies
one day ahead. In particular, one of our goals is to understand the universal aspects
4


### Page 5

of the volatility formation process. One element towards this will be to investigate
whether non-asset-dependent, generic, forecasting devices can lead to optimal pre-
dictions of future volatilities. First, we show that the LSTM approach performs
better than classical autoregressive models, one of which is the heterogeneous au-
toregressive (HAR) model [8]. Then we use a combination of the RFSV and QRH
for the parsimonious model candidate. We also conduct comparison tests to show
that for this model, the universal version of the model performs very similarly to the
one calibrated on each coin. This further conﬁrms the universality of the volatility
formation process from a parametric perspective.
We will follow the same structure as our companion paper [31]. In Section 2,
we describe our data and model evaluation metrics. In Section 3, we describe both
the parametric and non-parametric forecasting devices. We compare in Section 4
the performances of di↵erent forecasting models to provide evidence of a universal
volatility formation mechanism for cryptocurrencies. Our approach also enables us
to uncover asymmetry properties in the cryptocurrencies’ volatilities in contrast to
the stocks’ volatilities. In Section 5, we aim to describe a universal mechanism for
the volatility formation process with a parsimonious parametric model relating fu-
ture volatility with past volatilities and returns. We conclude in Section 6.
2
Data and evaluation metrics
Our dataset contains 5-minute intraday prices of cryptocurrencies traded on the
Binance exchange, with USDT, a popularly used stablecoin, as the base currency.
Stablecoins are cryptocurrencies with price stabilization mechanisms, often in the
form of pegging to some other assets such as traditional ﬁat money or other cryp-
5


### Page 6

tocurrencies [27]. In the case of USDT, it is pegged 1-to-1 with US dollars and can
be considered a cryptocurrency version of USD5. The Binance exchange is one of
the largest cryptocurrency exchanges by trading volume and o↵ers easily obtainable
market data, including price, volume, and number of trades in intervals as granular
as 5 minutes. The data is directly obtained from Binance.com.
We select 213 coins after ﬁltering out coins that are stablecoins, leveraged, or
have low liquidity or insuﬃcient data. The training set is chosen to be the two-year
period from 2020-01-01 to 2021-12-31, and the test set is a six-month period from
2022-01-01 to 2022-06-30.
Due to the rapid increase in the number of cryptocurrencies in recent years and
the issue of past data availability, we choose not to use training data from before
2020. The distribution of the number of available data points in the entire 2.5-year
period for selected coins is given in Figure 2.
Figure 2: Distribution of the number of available data points for selected coins.
The daily realized volatility for day t, σt, the variable of interest, is computed
5More about USDT can be found at https://tether.to/en/how-it-works.
6


### Page 7

as
σt =
sX
i
r2
t,i,
where r2
t,i is the ith 5-minute returns of the day. The return of day t is deﬁned as
rt = Pt −Pt−1
Pt−1
,
where Pt is the closing price of day t. Since cryptocurrencies trade 24 hours per
day every day, daily volatilities and returns are for 24-hour periods. The volatilities
and returns are scaled and normalized respectively by the individual coin’s statistics
calculated on the training set.
For model evaluation, we choose to use the mean-squared-error or MSE, calcu-
lated as
MSE(σ, ˆσ) = 1
T
T
X
t=1
(ˆσt −σt)2,
where T is the number of trading days in the test set. According to [29], it is a
robust and homogeneous metric for evaluating and comparing volatility models.
3
Forecasting devices
Here we introduce the parametric and non-parametric forecasting devices in this
study.
3.1
Parametric models
First, we consider two auto-regressive type models. One is a classical autoregres-
sive (AR) model, the other is a heterogeneous autoregressive (HAR) model [8]. Due
7


### Page 8

to the fact that cryptocurrencies are traded every day, for the HAR, the windows are
chosen to be 7 and 30 instead of 5 and 22 in the literature on traditional markets.
More precisely we deﬁne:
• ARp
ˆσt = ↵0 +
p
X
j=1
βjσt−j
p is chosen to be 7 or 30.
• HAR
ˆσt = ↵0 + β1σt−1 + β2
7
X
j=1
σt−j + β3
30
X
j=1
σt−j
These two models are ﬁtted on individual coin data.
For the RFSV, the log-volatility is modeled as a fractional Brownian motion
W H
t :
d log σt = ⌫dW H
t , ⌫> 0
The Hurst parameter H and ⌫can be estimated using the method in [16].
As in [16, 31], the predictor for H < 1
2 is given by:
\
log σt = cos(H⇡)
⇡
Z t−1
−1
log σs
(t −s + 1)(t −s)H+ 1
2
ds,
ˆσt = c exp(\
log σt),
where c = exp(
Γ( 3
2 −H)
2Γ(H+ 1
2 )Γ(2−2H)⌫2). We will see in Section 5 that c is empirically
very close to 1, and the impact of ⌫2 on the forecast is marginal. H is calibrated
using the pooled data set with all the coins.
8


### Page 9

3.2
Non-parametric forecasting with LSTM
The recurrent neural network (RNN) is suitable for sequential learning tasks.
Among types of RNNs, the Long Short-Term Memory (LSTM) neural network, in-
troduced in [21], is one of the most popular choices for predicting ﬁnancial time
series.
For each timestep t, the following computations are performed:
il
t = s(W l
iixl
t + bl
ii + W l
hihl
t−1 + bl
hi),
fl
t = s(W l
ifxl
t + bl
if + W l
hfhl
t−1 + bl
hf),
gl
t = tanh(W l
igxl
t + bl
ig + W l
hghl
t−1 + bl
hg),
ol
t = s(W l
ioxl
t + bl
io + W l
hohl
t−1 + bl
ho),
cl
t = fl
t ⇤cl
t−1 + il
t ⇤gl
t,
hl
t = ol
t ⇤tanh(cl
t)
where the superscript indexes the layer, cl
t, hl
t are the cell and hidden states, xl
t
equals the t-th element of the input sequence (σt) or (σt, rt) when l = 1 or hl−1
t
for l > 1, s(·) is the sigmoid function, ⇤is the Hadamard product, W l
. and bl
. are
parameters to learn from data. LSTMs use gates i, f, and o to capture long-range
dependence in the sequential data and to avoid the vanishing gradient problem of
classical RNNs [18, 21].
We use LSTMs with input length p, which are also chosen to be 7 or 30. The
inputs can be volatilities or both volatilities and returns.
We denote them by
LSTMp,var and LSTMp,ret respectively.
The LSTM consists of one LSTM layer
and one dense output layer. The dimensions of h1
t for LSTMp,var and LSTMp,ret are
9


### Page 10

chosen to be 2 and 4 respectively. This number is tuned using a cross-validation
split within the training data. We use the SiLU, introduced in [20], as the activation
function.
Neural network ﬁtting uses stochastic gradient descent and the results are noisy.
Therefore we train 10 identically structured models, initialized with 10 di↵erent
seeds. Lastly, we use the average of all their predictions as the ﬁnal prediction. The
optimizer we use is Adam, introduced in [23], with a learning rate of 1e-3. The
LSTMs are trained using the pooled data set.
4
Towards universality in the volatility formation pro-
cess
In this section, we compare di↵erent forecasting devices and show that we can
achieve optimal performance with the universal ones. We also analyze the local
sensitivities of the LSTMs and relate them to asymmetric volatility.
4.1
Parametric vs LSTM
In Figure 3, we have each model’s MSE relative to HAR, grouped by coins. We can
see that:
• AR7 underperforms HAR.
• AR30 is on par with HAR.
• LSTMs outperform HAR in general.
10


### Page 11

• LSTMs with a longer window show signiﬁcantly better than those with a
shorter window.
• LSTMs with return inputs show signiﬁcantly better performances than those
without.
• RFSV outperforms HAR, is slightly better than LSTM7,var and close to LSTM30,var,
but underperforms LSTM7,ret and LSTM30,ret.
These are largely consistent with the relative performances in [31].
Figure 3: Distribution of out-of-sample MSE of each model relative to the HAR
model.
4.2
Local sensitivities and asymmetric volatility
We deﬁne local sensitivities by:
↵t(⌧) :=
@ˆσt
@σ2
t−⌧
, βt(⌧) :=
@ˆσt
@rt−⌧
for ⌧= 1, 2, ..., 30.
Here we obtain the gradients of the predictions with respect to each of the inputs of
LSTM30,ret. For each coin, ↵(⌧) is given by the average of ↵t(⌧), β(⌧) the average
11


### Page 12

of βt(⌧). We then plot the average of these values across coins with a band of one
standard deviation in Figure 4. The plot of ↵(⌧) looks very similar to the one for
stocks in [31]. We observe that the values are signiﬁcantly positive, have a similar
magnitude, and decay with increasing ⌧.
For β(⌧), the values are one order smaller than ↵(⌧), also decay in ⌧, and are
positive for cryptocurrencies. In [31], β(⌧) are observed to be negative for stocks. In
both cases, the LSTMs captured a signiﬁcant e↵ect of returns on next-day volatili-
ties, but the di↵erent signs of β for the two asset classes are a curious observation.
If we use volatility as an indicator of trading activity or even the popularity of an
asset, we might hypothesize that cryptocurrency traders react to positive returns
more than to negative returns, while stock traders do the opposite. By extension, we
can also speculate that the typologies of market participants are di↵erent between
the two asset classes.
It has been previously observed that for cryptocurrencies, positive price shocks
increase the volatility more than negative shocks do [3, 7, 22]. This phenomenon is
known as inverted asymmetric volatility. In traditional markets, such as the stock
market, the observed asymmetry is reversed, i.e.
negative price shocks increase
volatility more than positive shocks. Such an observation has often been attributed
to the “fear of missing out” (FOMO) of uninformed cryptocurrency traders [9], and
the existence of “pump and dump” schemes [25]. A common conclusion in these
previous works is that the observation comes from the di↵erence in behaviour and
trading activity by uninformed and informed traders dominating the cryptocurrency
and stock market respectively.
12


### Page 13

Figure 4: Average ↵t(⌧) and βt(⌧) across coins and a one standard deviation band.
A nice byproduct of our methodology is a novel way to capture this inverted
asymmetry in cryptocurrencies with the LSTM. We have also provided supportive
evidence of this phenomenon across a much wider selection of cryptocurrencies than
in previous studies of asymmetric volatility, conﬁrming this observation on a large
scale. Additionally, in tandem with [31], in which an asymmetry is also observed
using a similar method, we have strong evidence from large baskets of assets from
both asset classes that the asymmetry in cryptocurrencies is opposite from that in
the stock market.
Figure 5 plots the model prediction ˆσ and gradients ↵t(⌧), βt(⌧) against σ2
t−1
and rt−1 for all datapoints, without grouping by coin.
4.3
Comparing universal and non-universal LSTMs
4.3.1
Universality across di↵erent market capitalisation levels
A new LSTM30,ret is trained on the top 50 coins by market capitalization (on
2021-12-31, the last day of the training period) only and compared with the univer-
sal one on the test period. The relative performance is shown in Figure 6. There
is no degradation of performance by the much smaller set of coins used in training,
13


### Page 14

Figure 5: Top left: ˆσ against σ2
t−1, top right: ˆσ against rt−1, bottom left: ↵t(1)
against σ2
t−1, bottom right: βt(1) against rt−1.
which suggests some universality of volatility formation across coins at di↵erent lev-
els of market capitalization.
4.3.2
No asset dependent mechanisms
Next, the universal LSTM30,ret is ﬁne-tuned to each individual coin’s data to
study whether this would improve its performance on individual coins. Fine-tuning
of neural networks is done by initiating a neural network’s parameters with a trained
one, then further training it with an often smaller dataset. In our case, for each
available coin, we initialize neural networks with the universal LSTM30,ret, then
train it further with only that coin’s training data.
14


### Page 15

Figure 6: Distribution of out-of-sample MSE of LSTM30,ret trained with the top 50
coins by market capitalization relative to the universal one.
If there were any asset-speciﬁc mechanisms that could be captured by the LSTM,
we should see the ﬁne-tuned LSTMs performing better. Here we allow all parameters
to be changed during ﬁne-tuning. The relative performance is shown in Figure 7.
The ﬁne-tuned models do not perform better.
This supports that there are no
asset-dependent mechanisms in volatility formation for the coins.
Figure 7: Distribution of out-of-sample MSE of LSTM30,ret ﬁne-tuned to each coin
relative to the universal one.
15


### Page 16

5
Uncovering universal mechanisms in the volatility for-
mation process
In this section, we calibrate the RFSV to each coin to conﬁrm the universality
of the volatility formation process. Then we incorporate the strong Zumbach e↵ect
into the rough-volatility based model by adding a quadratic rough Heston compo-
nent. By comparing the combined model to the LSTM and RFSV, we obtain a
promising candidate for the description of a universal volatility formation process.
5.1
RFSV
For RFSV, we ﬁrst estimate H and c for each coin, and the distributions are
shown in Figures 8 and 9. H and c tend to be higher than the ones for stocks as
found in [31]. The median of H and c are 0.103 and 1.06 respectively.
Figure 8: Distribution of H.
16


### Page 17

Figure 9: Distribution of c.
To once again check for universality from a parametric perspective, RFSVs are
calibrated to each coin and compared with the universal RFSV that is calibrated to
all coins. The relative performance is shown in Figure 10. The asset-speciﬁc RFSVs
perform very similarly to the universal RFSV. Similar to ﬁne-tuned LSTMs, we
would expect improvements from the asset-speciﬁc RFSVs if there were any coin-
speciﬁc mechanisms that could be captured by RFSV. Once again we obtain further
evidence of a lack of asset-speciﬁc mechanisms from a parametric perspective.
Figure 10: Distribution of out-of-sample MSE of RFSV calibrated to each coin
relative to the universal one.
17


### Page 18

5.2
RFSV enhanced with QRH
Here we use the forecasting device based on the Zumbach e↵ect from [30, 31]
via a quadratic rough Heston component. The forecasting formula from the QRH
model is given by
ˆσ2
t = a(Zt−1 −b)2 + c,
Zt =
n
X
i=1
cd
i Zi,t,
Zi,t = e−γdiZi,t−1 + rt,
Zi,0 = zi,0,
i = 1, . . . , n,
where a, b, c > 0, and (cdi, γdi)i=1,...,n are given by the same multi-factor approx-
imation of the rough kernel function K(t) :=
tH−1/2
Γ(H+1/2) [30].
Given H and n,
(cd
i , γd
i )i=1,2,...,n are not free parameters.
The predictions are essentially moving
averages of past realized volatilities and are not sensitive to the earliest inputs due
to the exponential decay in weights. In practice after computing Zi,t, one needs to
discard the earliest samples without suﬃcient histories. By including the QRH, we
have three more parameters a, b, c to calibrate which can be done by regressing σ2
t
on (Zt−1, Z2
t−1).
We will combine the predictions from RFSV and QRH linearly. The ﬁnal pre-
diction is given by (1 −λ)ˆσRFSV + λˆσQRH. The relative performances for di↵erent
values for λ to RFSV only are shown in Figure 11, the relative performances to
LSTM30,ret are shown in Figure 12.
Incorporating past returns in the RFSV through the QRH component is a
clear improvement.
At λ = 0.15, the model performs best and is very similar
18


### Page 19

to LSTM30,ret. This gives us a parsimonious parametric model candidate for a uni-
versal volatility mechanism.
We also note the larger optimal value for λ than that in [31] for stocks. Past re-
turns play a larger part in the volatility formation in cryptocurrencies than in stocks.
Figure 11: Distribution of out-of-sample MSE of (1 −λ)ˆσRFSV + λˆσQRH relative to
RFSV only (or λ = 0).
Figure 12: Distribution of out-of-sample MSE of (1 −λ)ˆσRFSV + λˆσQRH relative to
LSTM30,ret.
19


### Page 20

6
Conclusion
In this work, we adapt the volatility forecasting framework of [31] and extend it
to a di↵erent asset class. The framework and forecasting devices used in the origi-
nal paper are applied to the daily volatilities of cryptocurrencies at the start of the
“crypto-winter” crisis where prices and trading volume dropped. This is also the
ﬁrst study of cryptocurrency volatility in which a wide selection of coins is used.
In general, we ﬁnd the framework to work very well in producing relevant universal
volatility forecasting devices, as well as evidence of universal mechanisms in the
volatility formation process, as was found in stocks. The ﬁndings of the applied
methods, regarding predicting volatility, are thus remarkably largely similar in the
very di↵erent datasets and contexts.
Using classical auto-regressive models, LSTM and RFSV, we show that the
volatility during this period can be modeled and predicted well with the latter two.
The non-parametric LSTM and parsimonious RFSV, like for US stocks, outperform
all other traditional models used in industry and past literature. While constructing
the RFSV forecaster, we estimate the Hurst parameters of the log volatilities for all
the coins and showed that their volatilities are indeed “rough”. While comparing the
ﬁne-tuned LSTM and RFSV to their universal counterparts, we observe a universal-
ity of this process across the wide selection of coins, which is also observed in stocks.
Next, we use the combination of RFSV and QRH to obtain a parsimonious
model. We then ﬁnd that the RFSV+QRH model can perform as well as the LSTM
with both volatility and returns as input. This suggests that the main features in
the volatility formation for cryptocurrencies can be described by rough volatility
boosted with a strong Zumbach e↵ect. This model has also once again conﬁrmed
20


### Page 21

the universality of the volatility formation process across coins. The obtained mod-
els and volatility characteristics can further our understanding of this young and
evolving market. Remarkably, this device is found to also perform very well for
stock volatility, suggesting a higher level of universality across asset classes.
In addition, the use of LSTM o↵ers a new way to capture the e↵ect known as
asymmetric volatility. By analyzing the gradients of the volatility forecast with re-
spect to past returns, we can capture and conﬁrm the asymmetrical e↵ect of past
returns on volatility, and compare this e↵ect with other asset classes. This e↵ect
can be further used to infer the behavior and informedness of the traders in these
markets. Based on existing results, we can hypothesize cryptocurrency traders tend
to react to positive shocks more and might be less informed compared to traditional
market participants.
Acknowledgements
Siu Hin Tang is supported by the SINGA award by A*Star Singapore. Math-
ieu Rosenbaum is supported by the ´Ecole Polytechnique’s chairs Deep ﬁnance and
statistics and Machine learning and systematic methods. Chao Zhou is supported
by the Ministry of Education in Singapore under the MOE AcRF grants A-0004255-
00-00, A-0004273-00-00, A-0004589-00-00 and by Iotex Foundation Ltd under the
grant A-8001180-00-00.
21


### Page 22

References
[1] Amirshahi, B. and Lahmiri, S. (2023).
Hybrid deep learning and GARCH-
family models for forecasting volatility of cryptocurrencies. Machine Learning
with Applications, 12:100465.
[2] Arnosti, N. and Weinberg, S. M. (2022). Bitcoin: A natural oligopoly. Manage-
ment Science, 68(7):4755–4771.
[3] Baur, D. G. and Dimpﬂ, T. (2018). Asymmetric volatility in cryptocurrencies.
Economics Letters, 173:148–151.
[4] Bayer, C., Friz, P., and Gatheral, J. (2016).
Pricing under rough volatility.
Quantitative Finance, 16(6):887–904.
[5] Bennedsen, M., Lunde, A., Pakkanen, and S, M. (2022). Decoupling the short-
and long-term behavior of stochastic volatility. Journal of Financial Economet-
rics, 20(5):961–1006.
[6] Bianchi, D. and Babiak, M. (2022). On the performance of cryptocurrency funds.
Journal of Banking & Finance, 138:106467.
[7] Cheikh, N. B., Zaied, Y. B., and Chevallier, J. (2020). Asymmetric volatility in
cryptocurrency markets: New evidence from smooth transition GARCH models.
Finance Research Letters, 35:101293.
[8] Corsi, F. (2009). A simple approximate long-memory model of realized volatility.
Journal of Financial Econometrics, 7(2):174–196.
[9] Delfabbro, P., King, D. L., and Williams, J. (2021). The psychology of cryp-
tocurrency trading: Risk and protective factors. Journal of behavioral addictions,
10(2):201–207.
22


### Page 23

[10] Donier, J. and Bonart, J. (2015). A million metaorder analysis of market impact
on the Bitcoin. Market Microstructure and Liquidity, 1(02):1550008.
[11] D’Amato, V., Levantesi, S., and Piscopo, G. (2022). Deep learning in predicting
cryptocurrency volatility. Physica A: Statistical Mechanics and its Applications,
596:127158.
[12] El Euch, O., Gatheral, J., and Rosenbaum, M. (2019). Roughening Heston.
Risk, pages 84–89.
[13] El Euch, O. and Rosenbaum, M. (2018).
Perfect hedging in rough Heston
models. The Annals of Applied Probability, 28(6):3813–3856.
[14] El Euch, O. and Rosenbaum, M. (2019). The characteristic function of rough
Heston models. Mathematical Finance, 29(1):3–38.
[15] Fang, F., Ventre, C., Basios, M., Kanthan, L., Martinez-Rego, D., Wu, F.,
and Li, L. (2022). Cryptocurrency trading: a comprehensive survey. Financial
Innovation, 8(1):1–59.
[16] Gatheral, J., Jaisson, T., and Rosenbaum, M. (2018). Volatility is rough. Quan-
titative Finance, 18(6):933-949.
[17] Gatheral, J., Jusselin, P., and Rosenbaum, M. (2020). The quadratic rough
Heston model and the joint S&P 500/VIX smile calibration problem. Risk, May
2020.
[18] Goodfellow, I., Bengio, Y., and Courville, A. (2016). Deep learning. MIT press.
[19] Griﬃn, J. M. and Shams, A. (2020). Is Bitcoin really untethered? The Journal
of Finance, 75(4):1913–1964.
23


### Page 24

[20] Hendrycks, D. and Gimpel, K. (2020). Gaussian error linear units (gelus). arXiv
preprint, arXiv:1606.08415v4.
[21] Hochreiter, S. and Schmidhuber, J. (1997). Long short-term memory. Neural
Computation, 9(8):1735-1780.
[22] Kakinaka, S. and Umeno, K. (2022). Asymmetric volatility dynamics in cryp-
tocurrency markets on multi-time scales. Research in International Business and
Finance, 62:101754.
[23] Kingma, D. P. and Ba, J. (2015). Adam: a method for stochastic optimization.
Proceedings of the International Conference on Learning Representations (ICLR).
[24] Kristjanpoller, W. and Minutolo, M. C. (2018). A hybrid volatility forecasting
framework integrating GARCH, artiﬁcial neural network, technical analysis and
principal components analysis. Expert Systems with Applications, 109:1–11.
[25] Li, T., Shin, D., and Wang, B. (2021).
Cryptocurrency pump-and-dump
schemes. Available at SSRN 3267041.
[26] Malik, N., Aseri, M., Singh, P. V., and Srinivasan, K. (2022). Why Bitcoin will
fail to scale? Management Science, 68(10):7323–7349.
[27] Mita, M., Ito, K., Ohsawa, S., and Tanaka, H. (2019). What is stablecoin?: A
survey on price stabilization mechanisms for decentralized payment systems. In
2019 8th International Congress on Advanced Applied Informatics (IIAI-AAI),
pages 60–66. IEEE.
[28] Nakamoto, S. (2008). Bitcoin: A peer-to-peer electronic cash system. Available
online: http://bitcoin.org/bitcoin.pdf.
24


### Page 25

[29] Patton, A. J. (2011). Volatility forecast comparison using imperfect volatility
proxies. Journal of Econometrics, 160(1):246–256.
[30] Rosenbaum, M. and Zhang, J. (2022a). Deep calibration of the quadratic rough
Heston model. Risk, Oct 2022.
[31] Rosenbaum, M. and Zhang, J. (2022b). On the universality of the volatility
formation process: when machine learning and rough volatility agree. To appear
in Frontiers in Financial Mathematics.
[32] Takaishi, T. (2020). Rough volatility of Bitcoin. Finance Research Letters,
32:101379.
[33] Wu, P., Muzy, J.-F., and Bacry, E. (2022). From rough to multifractal volatility:
The log S-fBM model.
Physica A: Statistical Mechanics and its Applications,
604:127919.
[34] Zumbach, G. (2010). Volatility conditional on price trends. Quantitative Fi-
nance, 10(4):431–442.
25

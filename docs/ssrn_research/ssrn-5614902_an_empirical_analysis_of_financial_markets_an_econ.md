# An Empirical Analysis of Financial Markets: An Econophysics Approach

- **Source File**: `ssrn-5614902.pdf`
- **Total Pages**: 56
- **SSRN ID**: `ssrn-5614902`

---

## Page 1

An Empirical Analysis of Financial Markets: An Econophysics Approach
Haochen Li1, Yi Cao2, Maria Polukarov3, Carmine Ventre4,*
*Corresponding author
1King’s College London, haochen_li@kcl.ac.uk
2Xi’an Jiaotong-Liverpool University, yi.cao@xjtlu.edu.cn
3King’s College London, maria.polukarov@kcl.ac.uk
4King’s College London, carmine.ventre@kcl.ac.uk
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 2

An Empirical Analysis of Financial Markets: An
1
Econophysics Approach
2
Abstract
3
We develop a physics-inspired microstructure model for digital asset mar-
4
kets that processes Level-3 limit-order-book (LOB) events in real time. Treat-
5
ing orders as particles and order activity as system dynamics, we derive in-
6
terpretable measures, kinetic energy and momentum, in order to forecast
7
short-horizon volatility and direction.
To scale beyond top-of-book snap-
8
shots, we introduce Active Depth, a data-driven procedure that selects the
9
most informative LOB layers from event-time flows. Across cryptocurrency
10
datasets, the proposed measures outperform VPIN and Order Flow Imbal-
11
ance in both volatility and directional forecasting, and serve as high-value
12
features that improve DeepLOB, LSTM, and Transformer baselines. The
13
approach is training-free, latency-aware, and deployable at depth, offering
14
transparent signals for trading, market surveillance, and risk management.
15
We discuss implications for digital asset and provide studies validating Active
16
Depth and the incremental value of physics-informed features. Our results
17
highlight how econophysics can complement machine learning to deliver in-
18
terpretable, computationally efficient prediction in financial markets.
19
Keywords:
Econophysics, Market Microstructure, Limit Order Book,
20
Machine Learning, Cryptocurrency
21
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 3

1. Introduction
22
We study digital asset markets through a physics-inspired microstruc-
23
ture model that ingests Level-3 limit-order-book (LOB) events in real time.
24
Our objective is to forecast short-horizon volatility and direction while pro-
25
viding interpretable signals that can be operationalized in trading, market-
26
surveillance, and risk-management systems. The paper makes three contri-
27
butions.
28
Implication on asset pricing for digital asset markets. First, this
29
work sits squarely within Digital Finance. It addresses data-intensive mar-
30
kets (crypto), develops AI-compatible features (physics-informed signals that
31
lift deep models), and targets operational needs in risk management, market
32
surveillance, and digital governance (transparent real-time indicators, depth-
33
aware scaling). By linking econophysics with deployable analytics on Level-3
34
data, the paper speaks to the special issue’s focus on big data, ML/AI, dig-
35
ital currencies/blockchain, and the economic-regulatory challenges of digital
36
markets.
37
We establish novel benchmarks for the predictive accuracy of cryptocur-
38
rency asset price volatility and expected return utilising Level 3 order book
39
data. The accuracy of our model is justified by high predictive R-squared
40
values and prediction accuracy compared to previous literature, illustrating
41
its robustness across different market conditions. Our model bypasses the
42
need for training samples or parameter fitting since it takes full advantage
43
of the market microstructure information inherently enclosed in the Level
44
3 order book data.
Challet and Stinchcombe (2003), Eisler et al. (2012)
45
and Cont et al. (2014) studied the price impact of market order submis-
46
sions, and limit order submissions and cancellations that contained in the
47
Level 3 order book data, and discussed how these actions affect the limit or-
48
der book (LOB). This information is adequate for estimating the impact of
49
both current and forthcoming orders on the order book dynamics and, subse-
50
quently, price dynamics. We underline significant economic implications for
51
investors leveraging these predictive measures, which display a considerable
52
edge over conventional techniques such as the Volume-Synchronized Prob-
53
ability of Informed Trading (VPIN) and the Order Flow Imbalance (OFI)
54
when predicting volatility and expected asset returns.
55
Volatility and return prediction carry tangible economic significance. The
56
principal objective of asset pricing revolves around comprehending the pat-
57
terns of expected return and its accompanying volatility, as presented by
58
2
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 4

French et al. (1987).
Even if expected returns were observed completely,
59
the requirement for theories explaining their behaviour still persists and the
60
same for the empirical analysis validating them. However, the tasks of mea-
61
suring volatility and return are well-known intricate: at a lower frequency
62
time scale (like hourly or daily), return variations are primarily influenced by
63
unpredictable news events that impact prices. Upon examination of identi-
64
cal datasets, distinct volatility estimators can manifest disparate characteris-
65
tics. Notably, according to Cont et al. (2014), these estimators exhibit varied
66
intra-day patterns in different underlying assets. On the other hand, at high-
67
frequency trading scales, they are shadowed by the market microstructure
68
noise generated by market participants, including market makers, informed
69
traders, and noise traders.
70
Cont et al. (2014) proved that the order book depth deeper than best bid
71
and best ask contain information relevant to the price dynamics. Based on
72
this empirical finding, a recent strand of literature attempted machine learn-
73
ing methods to capture the volatility and expected return of assets. Doering
74
et al. (2017) developed convolutional neural networks (CNN) to predict price
75
and its volatility. Kercheval and Zhang (2015) employed Support Vector Ma-
76
chine (SVM) on the order book data. Sirignano (2019) and Sirignano and
77
Cont (2019) developed a deep Long Short-Term Memory (LSTM) model to
78
study the snapshot data of the order book. However, due to the restriction
79
of computing power and model complexity of machine learning models, they
80
are not feasible to study the information in deeper depths of the order book.
81
Our proposed physics-based model defines the concept of Active Depth to
82
distinguish the order book depths relevant with a simplicity in model com-
83
plexity. The model interpretability is another shortcoming of the machine
84
learning methods labeled as ‘black boxes’ because of the difficulty to un-
85
derstand the precise reasoning behind them, while the physics-based model
86
provides a straightforward intuition to explain the order book dynamics by
87
modelling it as a physical system.
88
Market microstructure noise is another important topic to consider as it
89
captures various of frictions intrinsic to the trading process. As argued by
90
Ait-Sahalia and Yu (2008), these noises include the bid-ask bounces, dis-
91
creteness of price fluctuations, differences in trade sizes, the informational
92
content of price changes, strategies of the order flow, and inventory manage-
93
ment effects. Eliminating the impact of these noises during investigating the
94
asset price is meaningful for the asset pricing practices, particularly in the
95
high-frequency trading markets.
96
3
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 5

We provide a novel technique to model the order book dynamics that
97
is possible to bypass hence eliminate the impact of both market news and
98
market microstructure noises as they arise from the time series of asset price,
99
volume, bid-ask spread or any other explanatory variables generated by or-
100
der book dynamics.
As a result, our research acts as a foundation upon
101
which future studies can be built, moving the field towards a more compre-
102
hensive understanding of the mechanisms that dominate asset pricing and,
103
by extension, the broader financial market dynamics.
104
Furthermore, we conduct an extensive benchmarking exercise comparing
105
our Physical Model to state-of-the-art deep learning architectures, including
106
Deep LSTM, DeepLOB, and a custom LOB-Transformer. The results show
107
that our model achieves competitive accuracy with no need for training, while
108
also significantly enhancing the performance of these models when used in
109
conjunction. This highlights the robustness and utility of physics-inspired
110
measures in high-frequency market prediction tasks.
111
A physics-informed microstructure model for digital asset mar-
112
kets. Second, we integrate microstructure-based asset pricing with a physics-
113
informed representation of LOB event flows, yielding interpretable, deployment-
114
ready signals for digital markets. While asset pricing traditionally focuses
115
on determining the intrinsic value of assets, an understanding of the market
116
microstructure – the system through which the trading of assets takes place –
117
is crucial to comprehend how the supply and demand for assets are matched
118
and how prices are ultimately discovered.
119
Bouchaud et al. (2002) along with Potters and Bouchaud (2003) eluci-
120
dated the statistical intricacies inherent to the order book. These empirical
121
investigations served as the foundation of ’zero-intelligence’ models. Such
122
models posited that the ‘stylised facts’ are an emergent outcome of order
123
flow properties and the intrinsic structure of the order book, without the
124
need for the ‘rationality’ assumptions. In their studies on limit order book,
125
Bouchaud et al. (2002) and Potters and Bouchaud (2003) offered a systematic
126
exploration of empirical properties, and developed models based on econo-
127
physics that linked the financial markets with physical systems.
128
The increasing interest in applying physical models to finance, both in
129
academia and in the industry, has yielded empirical studies in the field of asset
130
pricing and the field of Econophysics. Bouchaud et al. (2003) examined the
131
complex interplay between order flow and price fluctuations, drawing analo-
132
gies with the external stimuli in physical systems. Their insights unveiled
133
the market ‘randomness’. Farmer and Lillo (2004) through rigorous analy-
134
4
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 6

sis, highlighted a connection between power-law tails in price changes and
135
order flow dynamics, aligning with phenomena observed in physics. Farmer
136
et al. (2006) explored the effects of supply-demand on price movements, con-
137
trasting with the Efficient Market Hypothesis. Their findings drew parallels
138
with long-range correlations in physical systems. Borland (2012) looked into
139
the statistical pattern during market panics, by harnessing the concept of
140
self-organizing systems from physics. Inspired from these studies in Econo-
141
physics, our analysis aim to provide a detailed investigation of the utility of
142
a physical model applied to the challenging problems of modelling the LOB.
143
Bak et al. (1997) offered a distinctive perspective on price dynamics
144
within a multifaceted agent stock market. Drawing parallels with physical
145
systems, orders were conceptualised as particles on a price trajectory, where
146
intersections resulted in transactions. Yura et al. (2014) conceptualised or-
147
ders as fluid particles, using an interaction range defined by order activity to
148
segment the order book into layers. Yura et al. (2015) expanded this model,
149
linking price movement velocity to changes in the inner layer’s time-averaged
150
limit orders, and introduced a financial Knudsen number.
151
Approaching the complex structure of the limit order book from a econo-
152
physics perspective allows us to view the orders as interactive elements, and
153
the price fluctuation of an asset as a macroscopic property of this complex
154
system.
The historical price data merely encapsulates past alterations in
155
this macroscopic property, analogous to the temperature in a fluid system.
156
Nonetheless, examining the evolution of a fluid system necessitates knowledge
157
of inherent physical parameters such as density, mass, and velocity. These
158
parameters cannot be seized from historical temperature data alone; they re-
159
quire an understanding of the complex system. The key of the argument lies
160
in the fact that the limit order book system is vastly more information-rich
161
compared to historical price data.
162
The current literature of asset pricing does not address to this point but
163
merely studies the time series of asset price, while econophysics provides
164
the framework and techniques to build such models. By treating the limit
165
order book as a physical system, we can tap into a deeper, more macro-
166
scopic level of information. This approach, akin to the methods employed
167
in econophysics, allows us to better understand the underlying mechanisms
168
that drive the dynamics of asset prices. By recognizing that price movements
169
are a macroscopic feature of a more complex system of interacting orders, we
170
can gain new insights into the asset pricing process. This perspective opens
171
up novel avenues for research and presents opportunities for the development
172
5
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 7

of more robust models for understanding the price discovery and predicting
173
asset prices.
174
We employ the term ‘physical model’ to refer to a novel method that
175
mimics the dynamics of the order activities. We introduce a econophysics
176
perspective to model the limit order book, drawing an analogy between fi-
177
nancial markets and physics. It constructs a microscopic model of the orders,
178
conceptualising them as particles within the complex system of the limit or-
179
der book. Order submissions are interpreted as particles entering the system,
180
order cancellations as particles exiting the system, and each order transac-
181
tion as a particle annihilation. This allows us to calculate the change in
182
‘kinetic energy’ and ‘momentum’ within the system and estimate the im-
183
pact of each activity on the LOB. Our method considers the different quoted
184
prices of each single order upon submission and cancellation, estimates the
185
impact of each order activity on the order book, and utilises the microscopic
186
dynamics of order book activities to construct a systemic description of mar-
187
ket behaviour. We evaluate their efficacy in predicting price changes in the
188
Bitcoin and LUNA markets. Our findings suggest that these new measures
189
offer enhanced predictive power and capacity to accurately assess the market
190
behaviour, price volatility and return of the cryptocurrencies, outperforming
191
existing models such as the VPIN and OFI measure. This approach also
192
enables us to visually highlight events occurring within the high-frequency
193
trading market. Based on the current literature, few analytical tools har-
194
ness the vast amount of data in this domain to effectively illustrate financial
195
market phenomena.
196
In our analysis, we find that the predictive power of these measures, when
197
analyzed through the lens of our physical model, surpasses that of the bench-
198
mark techniques. Our findings show an improvement in the ability to forecast
199
price volatility and return in the asset. Moreover, the physical model’s suc-
200
cess in addressing the inefficiencies of traditional prediction models leads us
201
to our next empirical fact: the use of physical models to analyse market mi-
202
crostructure is viable when complemented with accurate description of the
203
order book complex system measured by the physical models. This empirical
204
research serves to justify the role of such models in the broader architecture
205
of the financial markets, which offers a significant advantage in capturing the
206
complexity of the order book dynamics that the traditional methods often
207
fail to accomplish.
208
However, it’s important to note that while our physical model signifi-
209
cantly enhances our understanding of asset returns, it is fundamentally a
210
6
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 8

measurement tool. It merely explains the process that the limit and market
211
orders discover the price and impact its dynamics, while it does not provide
212
insights into the economic mechanisms that drive these activities. As such,
213
while the physical model can significantly describe market behaviour and
214
enhance prediction, it must be complemented with economic theories that
215
investigate the underlying mechanisms driving asset returns. This remains an
216
exciting direction for future research, as there is an emerging literature that
217
combines these advanced analytical tools with economic theories to provide
218
a more comprehensive understanding of asset returns.
219
Active Depth: data-driven depth selection for scalable real-time
220
systems.
While top-of-book dynamics drive immediate price formation,
221
deeper levels encode broader market sentiment, hidden liquidity, and strate-
222
gic placement. Active Depth endogenously selects the LOB region where the
223
reacted order volume is able to predict price and volatility, enabling depth-
224
aware modeling with efficient computation
225
Bouchaud et al. (2002) emphasised the importance of understanding the
226
full depth of order books and not just the top layers. Their models, which
227
built on econophysics, revealed the intricate patterns and correlations across
228
different layers, underscoring the significance of considering deeper levels
229
when analysing price dynamics. Zovko and Farmer (2001) highlighted the
230
nuanced ‘patience’ traders demonstrate, suggesting that order placement is
231
not just concentrated near the best bid and ask, instead, many traders placed
232
orders at deeper levels and the distribution decayed as a power law. Through
233
simulation analysis, Smith et al. (2003) provided a statistical framework to
234
describe the continuous double auction mechanism. Their theory encapsu-
235
lated the significance of interactions at varying depths in the order book. By
236
illustrating how orders at different layers influence price determination, they
237
accentuated the importance of understanding the full spectrum of the order
238
book for accurate price prediction. Chiarella and Iori (2002) brought forth
239
insights into the microstructure dynamics of double auction markets. Their
240
agent-based model, with traders influenced by factors like chartists, funda-
241
mentalists, and noise, underscored that the depth of the order book was not
242
static but evolved based on these influences. They advocate for an in-depth
243
examination of the order book, suggesting that the deeper levels can provide
244
substantial insights into forthcoming market movements.
245
However, due to the restriction of computing power and model complex-
246
ity, it is impossible to study the information in all the depths of the order
247
book. Market makers, informed traders, noise traders and other market par-
248
7
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 9

ticipants participate in the market by submitting and cancelling the orders.
249
The order book dynamics is impacted by these order activities. As a result,
250
it is possible to find the depths that are encountering such activities. Based
251
on this inspiration, we proposed a method to define and calculate the concept
252
of active depth, which distinguish the depths that are active and contains
253
the relevant information to impact the order book.
254
In conclusion, the physical model, with its purely empirical approach
255
based on limit order book data, provides a fresh perspective that tran-
256
scends the traditional assumptions of empirical and behavioral finance. This
257
methodology offers a more nuanced and comprehensive analysis of market
258
dynamics, heralding a new direction in financial market research. However,
259
it is important to acknowledge that while this approach provides valuable
260
insights, it does not entirely replace the need for understanding the underly-
261
ing economic mechanisms or equilibrium. Complementary use of empirical,
262
behavioral, and the physical model may provide a more holistic perspective
263
of financial markets and asset pricing.
264
Beyond theoretical elegance, the model’s practicality is validated through
265
systematic experiments showing strong generalisation across prediction hori-
266
zons, minimal latency, and high interpretability. These qualities make the
267
Physical Model suitable not only as a standalone predictor but also as a
268
complementary module in modern machine learning pipelines for trading
269
systems.
270
The structure of this article is as follows. The review on the current re-
271
lated literature is given in Section 2. In Section 3, we overview the source and
272
format of the cryptocurrency order book data we used for our experiments.
273
A physical model to describe the limit order book and the order activity is
274
presented in Section 4, as well as the definition and calculation of the pre-
275
requisite concept called active depth. In Section 6 the kinetic energy measure
276
from the physical model is compared to the VPIN method on predicting the
277
volatility. In Section 7 another measure of momentum is discussed in a com-
278
parative analysis to the Order Flow Imbalance method. In Section 8, we
279
benchmark the Physical Model against deep learning models and show how
280
it improves predictive performance when integrated with them.
281
2. Literature Review
282
We here give an overview of existing financial models and methodologies,
283
focusing on those relevant to model the financial market with physics and
284
8
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 10

those predicting price volatility and impact.
285
Zero-intelligence econophysics models. A key theoretical founda-
286
tion for our work comes from zero-intelligence models, which assume that
287
market participants submit orders randomly rather than strictly optimizing
288
utility functions.
These models have proven surprisingly effective in cap-
289
turing a range of empirically observed market phenomena. Notably, Smith
290
et al. (2003) developed a statistical theory of the continuous double auction,
291
demonstrating that many stylised facts about prices and order flows emerge
292
even under zero-intelligence conditions. Farmer et al. (2005) further showed
293
that zero-intelligence models can exhibit nontrivial predictive power, high-
294
lighting that certain regularities of limit order markets do not necessarily
295
require strong assumptions about rationality or strategic behavior.
They
296
refined the modelling of order arrival, price movement, and implied supply-
297
demand relationships in a continuous double auction context. They estab-
298
lished functional relationships between order-arrival rates and market statis-
299
tical characteristics, as well as price movements and order flow. Upon testing
300
this model with trading data from different stocks, they found a shared price-
301
impact curve, suggesting a universal statistical law. Lillo and Doyne Farmer
302
(2005) demonstrated that the multidimensional stochastic process of bid-ask
303
spread exhibits specific statistical attributes, and that fluctuations in the
304
state of the limit order book drive price movements.
305
Lillo et al. (2003) conducted data analysis on the determinants of the
306
price impact of individual transactions, accounting for factors such as vol-
307
ume and underlying stock characteristics.
To standardise across different
308
liquidity levels, they re-scaled the mean price change and volume, result-
309
ing in a uniform price-impact curve across various stocks. Their findings
310
suggested a universal statistical law governing fluctuations from supply-and-
311
demand equilibrium across different financial assets. They postulated the
312
efficacy of modelling human activity as stochastic in certain contexts over
313
rational models. Building on these insights, Daniels et al. (2003) modeled
314
the price formation process, assuming random order placement and cancel-
315
lation, which allowed them to predict price movements successfully.
316
The aforementioned studies provide evidence that the state of the limit
317
order book and movement of limit orders follow stochastic processes, reveal-
318
ing certain statistical laws governing the limit order book. Consequently,
319
it becomes viable to study the rules governing order activities using econo-
320
physics. Beyond zero-intelligence approaches, our paper also draws on the
321
larger econophysics literature, which connects statistical physics methods to
322
9
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 11

financial market dynamics. Bouchaud et al. (2009) provided a foundational
323
survey on how markets absorb order flow imbalances over time, emphasiz-
324
ing that imbalances in supply and demand can persist and exhibit long-range
325
correlations. Their work underscores the idea that market price dynamics of-
326
ten arise from local interactions among heterogeneous agents, an insight that
327
aligns with our analogy of treating orders as interacting ‘particles’ within an
328
order book.
329
Yura et al. (2014) studied the LOB by drawing a parallel between financial
330
market dynamics and Brownian motion. They segmented the order book into
331
layers based on an ‘interaction range’ defined by order activity. Consequently,
332
they modeled the bid-ask spread and the nearest depths with the highest
333
temporary volume as a colloidal financial Brownian particle.
Their work
334
provided valuable insights on investigating how order book structures drove
335
price dynamics with econophysics. Li et al. (2023) modelled the orders as
336
particles and calculated the LOB system’s momentum in the defined passive
337
area, which they use to recognise the anomalous patterns and detect market
338
manipulation activities. They showcased the potential of physical models on
339
Level 3 order book data which may not be discernible using conventional
340
financial econometrics tools. Although this work did not study the volatility
341
and expected return, Li et al. (2023) offered an innovative way of viewing
342
the LOB and analysing the behaviours of market participants.
343
Order flow and microstructure metrics. Easley et al. (2011) pro-
344
vided an in-depth analysis of the events of May 6, 2010, known as the ‘flash
345
crash’. The authors argued that the crash was precipitated by automated
346
execution of a large sell order in the E-mini contract, leading to two liquid-
347
ity crises. They presented evidence that the liquidity problem was slowly
348
developing in the hours and days before the collapse, with high and unbal-
349
anced volume but low liquidity. The authors also discussed the role of high-
350
frequency trading (HFT) firms in this event, noting that these firms, which
351
account for over 73% of all U.S. equity trading volume, often act as mar-
352
ket makers. The paper introduced a measure of order flow toxicity, VPIN,
353
and demonstrated its predictive power for absolute returns and its poten-
354
tial use as a warning measure for the risk of a liquidity crash. The authors
355
concluded that in markets dominated by high-frequency liquidity providers,
356
unusually high levels of flow toxicity could lead to liquidity providers turning
357
into liquidity consumers, potentially destabilising the market.
358
In the paper by Andersen and Bondarenko (2014), the authors further
359
critically examined the Volume-Synchronised Probability of Informed Trad-
360
10
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 12

ing (VPIN) and its variants. They argued against the significance of any
361
specific metric unless it retained significance in formal tests that incorporate
362
readily observable real-time market activity measures, such as trading inten-
363
sity and implied volatility measures. The authors also discussed the volume
364
clock, the Order Imbalance (OI) measure, and the Trade Classification (TR-
365
VPIN) metric. They highlighted the complex interplay of parameters such
366
as the volume bucket, the time bar, the trade classification indicator, and the
367
length of the moving average in determining both the level and the dynamic
368
behaviour of the metric. The authors concluded that these parameters were
369
necessary to gauge the incremental information content of any new metric.
370
Easley et al. (2021) further demonstrated the application of machine
371
learning algorithms to predict and explain modern market microstructure
372
phenomena. They investigated the efficacy of various microstructure mea-
373
sures, showing that they continued to provide insights into price dynamics in
374
current complex markets. Interestingly, some microstructure features with
375
high explanatory power exhibited low predictive power, and vice versa. The
376
authors also found that some microstructure-based measures were useful for
377
out-of-sample prediction of various market statistics, leading to questions
378
about market efficiency.
Their results were derived using 87 of the most
379
liquid futures contracts across all asset classes. The authors suggested that
380
as markets become faster and data more copious, the market microstructure
381
played a critical role in predicting market behavior. They argued that despite
382
the increased complexity of trading strategies and the empirical measures of
383
microstructure, machine learning techniques can play an important role in
384
the evolution of microstructure research.
385
Regarding to the market microstructure analysis based on the order flow,
386
Cont et al. (2014) empirically investigated the influence of order book events
387
on equity prices using NYSE TAQ data. It proposed a simplified model using
388
a single variable, the Order Flow Imbalance (OFI), to linearly explain mid-
389
price changes, demonstrating robustness across various stocks and timescales.
390
Based on this work, Shen (2015) presented a compelling exploration of the
391
Volume Order Imbalance (VOI), which provided a robust framework for un-
392
derstanding market dynamics and offers valuable insights into the supply
393
and demand analysis on market microstructure level. Cartea et al. (2018)
394
provided an in-depth exploration of how trading strategies can be improved
395
by incorporating signals from the order book. Their research offered valuable
396
insights into the application of high-frequency order book data in strategy
397
optimization, thereby broadening the understanding of market microstruc-
398
11
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 13

ture and its implications for trading strategies. Their rigorous mathematical
399
approach and insightful findings underscored the importance of incorporating
400
granular market data to enhance trading efficacy.
401
Machine learning methods for financial markets. In recent years,
402
applying machine learning approaches on finance is an emerging topic while
403
there are relatively few that using such approaches to study the LOB. Nevmy-
404
vaka et al. (2006) introduced machine learning to the LOB by applying rein-
405
forcement learning on optimal order execution. Kercheval and Zhang (2015)
406
applied support vector machines (SVM) to predict the direction move of the
407
mid-price for stocks. Sirignano (2019) argued that neural networks outper-
408
forms SVM as well as other machine learning methods for LOB as they are
409
more capable of dealing with high-dimensional data and capturing nonlinear
410
relationships, while SVM can only provide binary classification instead of
411
indicate probabilities. Sirignano and Cont (2019) further developed a deep
412
neural network (DNN) model with Long Short-Term Memory (LSTM) units.
413
They trained an universal model with the LOB data of about 500 NAS-
414
DAQ stocks to predict the direction move of price. Yin and Wong (2023)
415
engineered deep convolutional neural network model to seize the information
416
from the LOB data at tick frequency of 0.5 second. After exploiting such in-
417
formation, the performance of their trading algorithm proved that the LOB
418
data contained rich information for liquidity, price prediction and trading
419
signal generation. Shavandi and Khedmati (2022) and Huang et al. (2024)
420
developed deep reinforcement learning model and proved them efficient on
421
optimizing algorithmic trading strategies.
422
While our research emphasises an interpretable physics-based approach,
423
the growing literature on deep learning methods for limit order books of-
424
fers a different angle on capturing microstructure dynamics. For instance,
425
Tsantekidis et al. (2017) investigated how deep learning architectures, includ-
426
ing recurrent and convolutional networks, can detect price-change signals or
427
volatility patterns embedded in high-frequency LOB data. Similarly, Zhang
428
et al. (2019) explored deep convolutional neural networks trained on order
429
book snapshots (known as DeepLOB). Their framework automatically learns
430
predictive features from multi-level bid and ask data, achieving strong fore-
431
casting performance on short-term price moves. Both works illustrate that
432
well-designed neural networks can uncover complex, nonlinear relationships
433
in trading data—albeit often at the cost of substantial computational re-
434
sources and reduced interpretability.
435
In contrast, our physics-based method does not require large-scale GPU
436
12
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 14

training or extensive hyperparameter tuning. By focusing on kinetic energy
437
and momentum constructs, adapted from zero-intelligence and econophysics
438
principles, we obtain interpretable metrics that directly connect to the under-
439
lying order flow. This approach provides a practical alternative or comple-
440
ment to deep neural networks, particularly in high-frequency contexts where
441
computational overhead and model explainability are crucial considerations.
442
Moreover, the model is straightforward and does not rely on extensive pa-
443
rameter fitting or large-scale training.
This interpretability is a practical
444
advantage compared to typical ‘black box’ machine learning models.
445
3. Data
446
This section details the data sets used in the study. It describes the source
447
of the data, which includes transaction data for Bitcoin and LUNA, and the
448
time frame covered. It also outlines the steps taken to clean and prepare the
449
data for analysis.
450
Financial markets are typically organised around a central record, the
451
limit order book (LOB), which logs all orders placed by traders. Our study
452
aims to process Level 3 order book data and summarise the complete infor-
453
mation about order activity and order book dynamics. Rather than relying
454
on time-based snapshot data of the order book, we propose a more compre-
455
hensive approach that processes every detail and message of the order book
456
data, thereby preserving all temporal information.
457
These data are considered to be high-frequency trading data (in microsec-
458
onds) sourced from the Coinbase exchange, accessed via Websocket feeds.
459
Due to the nature of the comprehensive physical modelling , this study re-
460
quires large-scale event data to model them with physical particle dynamics.
461
As a result, we study the BTC/USD pair as it has the largest trading volume
462
among existing cryptocurrencies. We also investigated the LUNA/USD pair
463
about its well-known flash crash in May 2022.
464
There are only limited exchanges that provide the Level-3 order book
465
event data, and Coinbase is the most popular exchange hence offers the
466
largest amount of available data demanded by this study. Our Level-3 order
467
book data were procured from the Coinbase exchange via a websocket feed,
468
encompassing Level-3 trading data for the BTC/USD and LUNA/USD cryp-
469
tocurrency pairs. As the most granular form of the order book data, Level-3
470
data includes records of order submissions, cancellations, and matches. In
471
13
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 15

contrast, Level-1 data comprises the Open/High/Low/Close price and vol-
472
ume data for a given period, while Level-2 data incorporates additional in-
473
formation regarding bid and ask order depths.
474
Orders received at a price equal to or worse than an existing order (typ-
475
ically, the best bid/ask) are executed immediately, generating a ‘match’
476
record. Unexecuted or partially executed orders become limit orders in the
477
LOB, creating an ‘open’ record. These limit orders, if not excuted, will re-
478
main on the LOB until they are cancelled, leaving a ‘cancelled’ record. In
479
our dataset, approximately 98.6% of open orders are eventually cancelled.
480
The minimum price precision is 0.01 USD for both BTC/USD and LUNA/USD
481
pairs, and the minimum trading volume unit (order size) is 0.00001 BTC for
482
BTC/USD pair and 0.001 LUNA for LUNA/USD pair. The minimum pre-
483
cision of the recorded timestamp is 0.000001 second (one microsecond). A
484
timestamp is counted when an order activity (or, event) occurs, hence the
485
timestamps of the event-driven records are discrete and not consecutive. For
486
both BTC/USD and LUNA/USD datasets, we grouped the event records
487
by ∆t = 0.1 second basis and aggregated all the events occurred in each
488
∆t = 0.1 time period. We also recorded the best bid and best ask prices
489
when the last event of each ∆t = 0.1 time period occurs as the best bid/ask
490
prices of the consecutive ∆t = 0.1 time period.
491
The granularity of Level-3 order book data presents a rich tapestry of
492
information, demanding opportune computational strategies. We opted to
493
aggregate events into 0.1-second intervals, representing a careful balance be-
494
tween retaining market activity resolution and optimising computational ef-
495
ficiency. The empirical assessments confirmed that this aggregation granu-
496
larity preserved the integrity of significant market patterns and trends.
497
Section 5 analysed cryptocurrency market behaviour by investigating
498
Level-3 trading data for the BTC/USD pair between 20/04/2022 23:00-00:00
499
and the LUNA/USD pair between 11/05/2022 16:00-20:00, when the LUNA
500
crash occurred. In the LUNA/USD dataset from 11/05/2022 16:00-17:00, a
501
total of 248,796 order submission and cancellation records were identified,
502
with 233,134 occurring within the active area, 8,302 within the passive area,
503
and 7,360 outside. Consequently, about 97% of order submissions and can-
504
cellations transpired within the active area, and 3% within the passive area.
505
In Section 4.2, 6 and 7, we investigated the Level-3 order book data for the
506
BTC/USD pair during 02:00-03:00 20/04/2022, 15:00-16:00 on 28/11/2022,
507
and for the LUNA/USD pair during 16:00-20:00 on 11/05/2022, 02:00-03:00
508
on 12/05/2022, while the LUNA was facing the significant fall. The original
509
14
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 16

datasets are composed of two datasets - full channel data and ticker channel
510
data. The full channel encompasses all of the Level-3 order book data dis-
511
cussed previously, and is event-driven, with every order activity (submission,
512
cancellation, and matches) leaving a record. On the other hand, the ticker
513
channel contains snapshot information of the order book, including the best
514
bid price and best ask price, with a new record in this channel created each
515
time a match occurs. However, the aggregated quoted volume of the best
516
bid and best ask price was available for the BTC/USD data, but not for the
517
LUNA/USD data. There were more than 2,700,000 lines of records in the full
518
channel data and 47,000 in the ticker channel for each one-hour BTC/USD
519
dataset, while the numbers were about 480,000 and 35,000 for LUNA/USD.
520
We also used both the Level-3 order book data and LOB snapshot data
521
for the BTC/USD pair during the 12-hour span between 16/09/2023 02:00 -
522
16/09/2023 14:00 to train the Deep LSTM model, the DeepLOB model, and
523
an LOB-Transformer model to analyse the capability of the physics-based
524
model in Section 8. This data set contained 9,839,922 samples of Level-3
525
order book data and 2,018,900 samples of LOB snapshots.
526
The high-frequency nature of the dataset resulted in a significantly large
527
amount of data points, even for a relatively short timeframe. The usage,
528
time span, and nature of the data we have used in this study are listed in
529
Table 1.
530
Table 1: Summary of datasets used throughout the study
Dataset
Section and Usage
Time Span
Event Data
Snapshot Data
BTC/USD (I)
Section 5 - empirical market behaviour
20/04/2022 23:00-00:00
✓
✗
LUNA/USD (I)
Section 5 - empirical market behaviour
11/05/2022 16:00-20:00
✓
✗
BTC/USD (II)
Section 4.2 - calculation on Active Depth
28/11/2022 15:00-16:00
✓
✗
Section 6 - comparison with VPIN on volatility
Section 7 - comparison with OFI on price prediction
LUNA/USD (II)
Section 4.2 - calculation on Active Depth
12/05/2022 02:00-03:00
✓
✗
Section 6 - comparison with VPIN on volatility
Section 7 - comparison with OFI on price prediction
BTC/USD (III)
Section 8 - Benchmarking with deep models
16/09/2023 02:00-12:00
✓
✓
Why Level-3 data?
531
Throughout the empirical chapters we rely on Level-3 (order-event) feeds
532
rather than the coarser Level-1 (best quote) or Level-2 (depth snapshot)
533
alternatives. Two considerations motivate this choice.
534
Requirement for event granularity: The Physical Model treats every order
535
as a particle whose displacement, velocity and momentum must be observed
536
15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 17

at the moment of submission or cancellation. These quantities are not recov-
537
erable from aggregated depth messages; once orders are bucketed by price
538
level, the exact path that each quote has travelled through the book is irre-
539
trievably lost.
540
Ability to diagnose manipulation at source: Rule-based surveillance works
541
reasonably well when abuse manifests only in executed trades, but it strug-
542
gles whenever abusive strategies exploit the order-submission process itself
543
(for example, spoofers layering quotes far from the touch but cancelling mil-
544
liseconds before execution). Level-3 order book data feeds are the only public
545
record that preserves those additions and withdrawals before they influence
546
the best bid or ask. Without this detail a spoofing episode may be indis-
547
tinguishable from innocuous quote flickering driven by market making algo-
548
rithms.
549
Level-3 order book data feeds therefore supply the minimum informa-
550
tion set required to compute physical variables reliably and to attribute any
551
detected anomaly to an identifiable sequence of messages. Lower-resolution
552
data may still be useful for descriptive statistics, but they cannot support
553
the particle-based mechanics that underpins this work.
554
4. Methodology
555
The Physical Model, with its purely empirical approach based on limit
556
order book data, provides a fresh perspective that transcends the traditional
557
assumptions of empirical and behavioural finance. This methodology offers
558
a more nuanced and comprehensive analysis of market dynamics, heralding
559
a new direction in financial market research.
560
4.1. The Physical Model
561
In this section, we will propose a model for the LOB inspired by concepts
562
from physics, which models the LOB as a physical system where the conserva-
563
tion of momentum and energy can be applied. We will extend these concepts
564
to introduce and define the novel measures such as the Active Depth, total
565
volume of reacted order, and kinetic energy of the LOB.
566
In the LOB, the best bid and best ask prices are represented by bM
567
and aM, and the market midprice is subsequently denoted by zmid = bM+aM
2
.
568
Additionally, the market match price pM is noted whenever a trade execution
569
occurs. For a given time t, the market midprice and match price are denoted
570
by zmid(t) and pM(t) respectively. The quantity of limit orders at a specific
571
16
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 18

quoted price x is denoted by N(x, t) which is invariably non-negative. Over
572
the interval [t −∆t, t], the velocity of the match price, vM(t), is calculated
573
by the rate of change in the match price with vM(t) = pM(t)−pM(t−∆t)
∆t
.
574
It was observed that order activities predominantly cluster around the
575
market midprice. A so-called active area is identified as an extended range
576
at a particular depth within the LOB, oriented around the bid-ask spread as
577
illustrated in Figure 1. The dynamics of the active area closely mirror those
578
of the market midprice; within this range, order submissions and cancella-
579
tions exhibit elevated activity, while beyond this range, limit orders generally
580
remain stationary. Consequently, the active bid price and active ask price
581
are derived as the best bid and best ask prices adjusted by the Active Depth
582
defined in Section 4.2.
583
Figure 1: Active and passive areas of the order book
In this study, orders are conceptualised as physical particles moving on
584
a one-dimensional axis.
The order size corresponds to the particle mass,
585
while its displacement is akin to the distance of particle movement. Over a
586
sampling period ∆t, the velocity v(t) of an order is computed as the quotient
587
of its displacement ∆p and the elapsed time ∆t. The order velocity is only
588
defined within the active area, bounded by [bM −α, aM + α] where α is the
589
Active Depth which will be defined in Section 4.2.
590
17
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 19

Figure 2: Motion of a limit buy order
During each sampling interval (T −∆t, T], we define the velocity of a
591
limit buy order as the rate of change in its quoted price relative to the active
592
bid price bM −α. Specifically, the velocity of a limit buy order quoted at
593
price p∗(t) at time t reflects its movement from price depth bM −α to p∗(t)
594
within this period, encapsulating the intensity and direction of order activity
595
in the LOB. In other words, for a specific limit buy order of size s submitted
596
to its quoted price p∗(t) at time t during the sampling period (T −∆t, T],
597
t ∈(T −∆t, T], the order’s velocity can be computed with
598
v(t) = p∗(t) −(bM(T −∆t) −α)
∆t
.
(1)
It is noteworthy that for limit buy orders exceeding the best ask price aM,
599
the effective quoted price becomes p∗(t) = aM at time T −∆t.
600
In contrast, a canceled buy order is considered to move from its initial
601
quoted price p∗(t) to the active bid price, bM −α at time T −∆t. Its velocity
602
is thus calculated as:
603
v(t) = (bM(T −∆t) −α) −p∗(t)
∆t
.
(2)
18
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 20

Similarly, for a newly submitted limit sell order, the velocity is
604
v(t) = p∗(t) −(aM(T −∆t) + α)
∆t
.
(3)
Here, if the quoted price is below the best bid price bM, the effective quoted
605
price becomes p∗(t) = bM at time T −∆t.
For canceled sell orders, the
606
velocity is computed as:
607
v(t) = (aM(T −∆t) + α) −p∗(t)
∆t
.
(4)
The depth of the order book will be raised to specify the location of limit
608
orders with regard to the inside of the order book (best bid price for buy
609
orders and best ask price for sell orders) at the same side. At time t, the
610
depth of a specific limit order quoted at price p∗is denoted by γ(p∗, t) and
611
defined by
612
γ(p∗, t) = [bM(T −∆t) −p∗]
(5)
for the bid side, where the buy orders are normally quoted at price lower
613
than the best bid price. And
614
γ(p∗, t) = [p∗−aM(T −∆t)]
(6)
for the ask side, where the sell orders are normally quoted at price higher
615
than the best ask price.
Note that the depth for a limit order could be
616
negative value in the case that it is quoted between the bid-ask spread.
617
Let Nγ(t) denote the total number of limit orders submitted at depth γ
618
of the LOB during time t, and N c
γ(t) for the total number of limit orders
619
cancelled at depth γ at time t. We define the Reacted Orders Volume (either
620
cancelled or submitted) inside depth γ during T −∆t to T as
621
∆V (γ)(T−∆t,T] =
X
t∈(T−∆t,T]
aM+γ
X
γ∗=bM−γ
(
Nγ∗(t)
X
i=1
si +
Nc
γ∗(t)
X
j=1
sc
j)
(7)
where si is the order size of the ith submitted limit order quoted at this
622
depth, while sc
j is the order size of the jth cancelled limit order quoted at
623
this depth. Note that this equation takes discrete values, over the discretised
624
event-based order book data timeframe t ∈(T −∆t, T], on the order book
625
depth γ∗ranging from the depth bM −γ at best bid price minus the given
626
19
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 21

value γ, to the depth aM + γ at best ask price plus the given value γ, and it
627
is similar in Equations 8 and 9.
628
Now, we can define the kinetic energy and momentum of an order akin
629
the physical kinetic energy and momentum of an object. That is, the product
630
of half its size and squared velocity 1
2s·v2 for kinetic energy, and the product
631
of its size and velocity s · v for momentum. Thus, to calculate the kinetic
632
energy and momentum of submitted market and limit orders we shall use
633
equations (1) and (3) for velocity, and for cancelled limit orders – equations
634
(2) and (4).
635
Recall the denotation of Nγ(t) for the total number of limit orders at
636
depth γ of the LOB at time t. We then calculate the cumulative sum of
637
kinetic energy and momentum respectively at time t by aggregating the ki-
638
netic energy and momentum resulting from all order activities occurred in
639
the order book depths γ ranging from the lower bound to the upper bound
640
of the active area. Specifically, the kinetic energy of the order book at time
641
T is
642
KE(T) =
X
t∈(0,T]
aM+α
X
γ∗=bM−α
(
Nγ∗(t)
X
i=1
1
2si · vi
2 +
Nc
γ∗(t)
X
j=1
1
2sc
j · vc
j
2)
(8)
and the momentum of the order book at time T is
643
P(T) =
X
t∈(0,T]
aM+α
X
γ∗=bM−α
(
Nγ∗(t)
X
i=1
si · vi +
Nc
γ∗(t)
X
j=1
sc
j · vc
j)
(9)
where si and vi are the order size and velocity of the ith submitted limit order
644
quoted at this depth, while sc
j and vc
j are the order size and velocity of the
645
jth cancelled limit order quoted at this depth.
646
Importantly, our approach models the order book as a complex system,
647
and emphasises the vicinity surrounding the bid-ask spread, where order
648
activities exhibit the highest degree of activity, and assigns greater weight to
649
orders quoted in closer proximity to the bid-ask spread as they exert a more
650
substantial influence on the bid-ask spread.
651
4.2. Calculation of Active Depth
652
This section explains the methodology used to calculate the Active Depth,
653
a crucial component in the proposed Physical Model. We will present the
654
details how to establish the definition and calculation on the upper and lower
655
20
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 22

boundaries of the Active Depth. In Section 4, we introduced the concept of
656
the active area, defined by the order book depth α, wherein the majority
657
of order activity takes place. This section will focus on the computational
658
methodology for deriving this pivotal depth and elaborate on the empirical
659
analysis supporting its efficacy.
660
To extract this depth empirically and determine the active area α, we
661
investigate the interconnection between the order activities around to the
662
bid-ask spread and their response subjected to movements in the match price,
663
in terms of the order cancellation or submission. Our approach employs a
664
moving window to compute the change in the Reacted Orders Volume ∆V (γ)
665
within different order book depth γ based on equation 7. Concurrently, we
666
assess the corresponding distance traversed by the match price vM(t) within
667
this identical time frame.
668
Our analysis further extends to study the cross-correlation function Corr[vM(t), ∆V (γ)]
669
to investigate the relationship between changes in the match price and al-
670
terations in the total volume of orders reacted at depth γ. The graphical
671
representation of this relationship is presented in Figure 3, where the time
672
range of the data investigated were 15:00-16:00 28/11/2022 for BTC/USD
673
pair, and 02:00-03:00 12/05/2022 for LUNA/USD pair.
674
Specifically, to compute the cross-correlation coefficient Corr[vM(t), ∆V (γ)]
675
across order book depths, we proceed by applying a subtle methodology for
676
each depth γ∗. First, we establish a moving window with a fixed step size.
677
Within each window, we aggregate the total size of orders submitted and can-
678
celled (Reacted Order Volume), resulting in an order size count that captures
679
the volume of the responsive order activities at that depth. Simultaneously,
680
we calculate the price velocity over each step, defined as the difference in
681
the match price between the end of the previous window and the end of the
682
current window. By constructing a series of Reacted Order Volume and cor-
683
responding price velocities, we then calculate the correlation between these
684
two series, yielding the cross-correlation coefficient Corr[vM(t), ∆V (γ∗)] for
685
each depth γ∗. This approach allows us to quantify the relationship between
686
match price velocity and the order activities corresponded to the price change
687
across varying depths in the order book.
688
A close examination of Figure 3a reveals the correlation coefficient peak-
689
ing at depth $50 for the BTC/USD market. In contrast, for the LUNA/USD
690
market, the maximum correlation is observed at a considerably shallower
691
depth of $0.2, as illustrated in Figure 3b. This is due to the different pro-
692
portions of tick size (minimum price increment unit) to the price of the
693
21
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 23

(a) BTC/USD market
(b) LUNA/USD market
Figure 3: Correlation analysis of the match price and the change in Reacted Orders Volume
across order book depth (X-axis: order book depth, Y-axis: correlation coefficient)
respective underlying asset. For Bitcoin, this ratio is approximately $0.01 to
694
about $16,000, whereas for LUNA, it is significantly larger, at $0.01 to about
695
$2. These graphical illustrations portray a quantifiable correlation between
696
fluctuations in the match price and corresponding changes in the Reacted
697
Orders Volume, as a function of the order book depth.
698
This characteristic pattern demonstrates a collective trend following be-
699
haviour of orders, thereby substantiating our active area concept. In partic-
700
ular, according to the experiments based on different windows sizes ranging
701
from 1 second to 360 seconds, at an order book depth of $50 for Bitcoin and
702
$0.2 for LUNA, the high-frequency traders exhibit a pronounced tendency
703
to modify the largest volume of order in response to the movement of the
704
match price.
705
Now we can define the Active Depth α by:
706
α = arg max
γ
Corr[vM(t), ∆V (γ)]
(10)
This empirical evidence amplifies the pivotal role of the active area in the
707
financial market dynamics and underscores its utility in assessing the market
708
microstructure. It offers a valuable lens through which to understand and
709
anticipate the behaviour of high-frequency traders. The findings contribute
710
to the broader understanding of market liquidity and depth, and could have
711
important implications for market participants and regulators alike.
712
22
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 24

5. Empirical Findings
713
In this section we present the results of applying the Physical Model to
714
the datasets of Bitcoin and LUNA. We report the outcomes of their analysis
715
and interpret these findings, highlighting the ability of the Physical Model
716
to describe the order book dynamics and market behaviour.
717
In the realm of physical systems, examining the motion of a single particle
718
is infeasible. However, when considering a vast number of particles within a
719
complex system, statistical rules governing their collective behaviour and mo-
720
tion may be discerned. A parallel can be drawn with an order book dynam-
721
ics, where individual traders place orders based on their supply and demand
722
needs, resulting in irregular market oscillations and noise. Nevertheless, when
723
aggregating all order records and information, emergent collective behaviours
724
become evident. By observing these collective behaviours, insights into mar-
725
ket behaviour can be gleaned, potentially unveiling the underlying factors
726
driving the order book and price dynamics.
727
(a) Limit order and market order unseparated
(b) Limit order and market order separated
Figure 4:
Measures in the active area (depth = $100) for BTC/USD pair during
20/04/2022 23:00-00:00, with limit order and market order unseparated or separated
Thus, for the BTC/USD pair during the interval of 20/04/2022 23:00-
728
00:00 and with an active area set to $100, the cumulative sum of net momen-
729
tum for all orders closely mirrors the midprice movement, as demonstrated
730
in Figure 4a.
731
23
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 25

Examining the cumulative sum of net momentum separately for limit
732
orders and market orders yields Figure 4b, where the first row represents
733
the cumulative sum of net momentum for limit orders and the second row
734
for market orders. We see a noticeable jump in the cumulative sum of net
735
momentum for market orders, which is attributable to the placement of a
736
substantial market buy order that does not adhere to the midprice trend.
737
Similar experiments on the LUNA/USD pair during 11/05/2022 16:00-
738
17:00, 18:00-19:00 and 19:00-20:00 with active area set to $0.5 are illustrated
739
in Figures 5a, 5b and 5c.
740
(a) 11/05/2022 16:00-17:00
(b) 11/05/2022 18:00-19:00
(c) 11/05/2022 19:00-20:00
Figure 5: Measures for LUNA/USD during different periods
The midprice trend is followed albeit somehow more loosely than in the
741
case of BTC/USD (e.g., the midprice downtrends in the middle of Figure 5a
742
not reflected by the cumulative sum of net momentum). However, upon eval-
743
uating the cumulative sum of net momentum separately for limit orders and
744
market orders in Figures 6a, 6b, and 6c, an intriguing market microstructure
745
phenomenon emerges. Market orders consistently exhibit greater momen-
746
tum than limit orders across all three time periods. Moreover, market orders
747
24
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 26

persistently attempt to drive the price upward (unsuccessfully), while limit
748
orders continuously sell.
749
(a) 11/05/2022 16:00-17:00
(b) 11/05/2022 18:00-19:00
(c) 11/05/2022 19:00-20:00
Figure 6: Measures in the active area (depth = $0.5) for LUNA/USD pair during different
periods, with limit order and market order separated
6. Volatility Forecasting: A Comparative Analysis of Kinetic En-
750
ergy and VPIN
751
In the realm of financial market analysis, predicting volatility is an ongo-
752
ing challenge and a critical component for both risk management and trad-
753
ing strategies. Traditional volatility prediction models have often relied on
754
measures like historical volatility, implied volatility, GARCH models, and
755
more recently, VPIN (Volume-Synchronised Probability of Informed Trad-
756
ing). However, we proposed a novel approach to predict short-term volatility
757
by employing the concept of Energy Change, inspired by physical systems.
758
The VPIN model discussed by Easley et al. (2012); Abad and Yag¨ue
759
(2012), is designed to measure the imbalanced volume of trades. It is based
760
on the idea that informed traders will trade more aggressively, leading to an
761
imbalance in the trade volume and hence, increased volatility. The model
762
has been popularly used for its ability to capture the arrival rate of informed
763
25
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 27

traders and its subsequent impact on volatility. However, the VPIN model
764
primarily focuses on transaction data, and as a result, might not fully capture
765
the dynamics of the limit order book.
766
In contrast, the kinetic energy measure proposed offers a fresh perspective
767
by drawing an analogy between physical systems and financial markets. The
768
Energy measure is calculated as half the sum of the squared order velocity
769
in the defined Active Depth of the order book. This measure is expected
770
to capture the degree of demand to produce a change for different order
771
activities, thus evaluating a macroscopic view of the order book dynamics.
772
6.1. Introduction on the VPIN Method
773
The Volume-Synchronised Probability of Informed Trading (VPIN) rep-
774
resents a cutting-edge analytical tool, garnering increasing interest within
775
the realm of market microstructure studies. This tool serves as a metric for
776
the disequilibrium between informed and uninformed market trades. The
777
cornerstone of VPIN lies in the hypothesis that informed traders leverage
778
private information, thus provoking an imbalance in trading volumes.
779
To derive VPIN, one divides the trade volume into discrete segments, or
780
’buckets’, and subsequently juxtaposes the volume of buyer-oriented trades to
781
that of seller-initiated trades within each segment. Normalising the disparity
782
between these two volumes by the total volume yields the VPIN. A high
783
VPIN value signals a heightened likelihood of informed trading, indicative of
784
a substantial disequilibrium between purchase and sale orders. In contrast,
785
a low VPIN suggests a harmonious market characterised by equivalent levels
786
of purchasing and selling.
787
In the sphere of financial markets, VPIN serves as an instantaneous indi-
788
cator of market states, offering crucial insights into the degree of information
789
asymmetry in the market. This asymmetry could presage periods of intense
790
volatility. Hence, the VPIN may serve as an instrument for forecasting short-
791
term market fluctuations, proving particularly beneficial for high-frequency
792
traders and market makers.
793
Abrupt VPIN fluctuations, particularly sharp escalations, may serve as an
794
early warning system for impending market volatility. Some empirical studies
795
suggest that elevated VPIN values can anticipate price volatility driven by
796
liquidity and market imbalances. Consequently, traders and financial institu-
797
tions frequently employ VPIN as a risk management instrument. However, it
798
is crucial to bear in mind that while VPIN is a valuable metric, it does carry
799
its set of limitations. The VPIN model presumes that all informed trades will
800
26
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 28

instigate price variations, an assumption that may not always hold. More-
801
over, the selection of volume bucket size can significantly influence the VPIN
802
output and there lacks a universal method choosing the optimal bucket size.
803
6.2. Historical Volatility
804
In the context of time series analysis, the Granger causality test proposed
805
by Granger (1969) is a statistical hypothesis test for determining whether one
806
time series is useful in forecasting another and provide evidence of predictive
807
power.
808
The results of P-values in the Granger causality test on the 5-minuite
809
volatility against the VPIN time series lagging from 1 to 300 seconds for
810
Bitcoin and LUNA are shown in Figure 7. The similar results on the 5-
811
minuite volatility against the kinetic energy are shown in Figure 8.
812
(a) BTC/USD market
(b) LUNA/USD market
Figure 7: Granger causality test on the 5-minuite volatility against the VPIN
(a) BTC/USD market
(b) LUNA/USD market
Figure 8: Granger causality test on the 5-minuite volatility against the kinetic energy
A small p-value indicates strong evidence against the null hypothesis and
813
suggests that the latter time series Granger-cause the former time series. The
814
VPIN data performs the best in predicting the 5-minute volatility that is
815
27
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 29

about 0-50 seconds behinds for Bitcoin and about 55-150 seconds for LUNA.
816
And the kinetic energy performs the best predicting the 5-minute volatility
817
about 0-100 seconds behinds for Bitcoin while it acts terribly in predicing
818
the 5-minute volatility for LUNA.
819
In general, we can conclude that the VPIN of LUNA performs better
820
than its kinetic energy in predicting the 5-minute volatility. while the kinetic
821
energy of Bitcoin outperform its VPIN.
822
6.3. Local Volatility
823
As we are studying the high-frequency trading data, we adopt a different
824
method to calculate the instantaneous volatility. This new method seeks to
825
address a potential shortcoming of the traditional standard deviation calcu-
826
lation in the context of financial asset price data, particularly when the asset
827
price exhibits a trending behaviour.
828
The traditional calculation of volatility involves computing the standard
829
deviation of returns, which is based on the mean return. However, when the
830
asset price exhibits a trending behaviour, the mean return could be signifi-
831
cantly different from zero, and changing the length of the time window used
832
for the calculation could result in artificially high volatility values. This is
833
because more returns would be further away from the mean, leading to a
834
larger sum of squared deviations.
835
To address this issue, our Local Volatility measure computes the standard
836
deviation of the differences between consecutive asset prices, rather than their
837
returns. This provides a measure of how much the price changes from one
838
tick to the next, irrespective of the overall trend.
839
The Local Volatility for an asset with time series of match price P M
t
is
840
defined as:
841
σLV =
sPT
t=1(pM
t −pM
t−1)2
T
(11)
where pM
t
represents the price at time t, and T is the total number of price
842
observations, the symbol σLV represents the Local Volatility.
843
This equation calculates the square of the differences between consecutive
844
prices (pM
t −pM
t−1)2, sums them up, divides by the total number of observations
845
to calculate the mean squared difference, and finally takes the square root
846
to obtain the standard deviation of price changes.
This Local Volatility
847
measure provides a more meaningful estimate of the instantaneous volatility
848
28
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 30

of an underlying asset, particularly when the asset price exhibits a trending
849
behaviour.
850
Regarding to the calculated 30-second Local Volatility, we carried out
851
the Granger causality test again, and the results of 30-second Local Volatility
852
against the VPIN are shown in Figure 9 while that against the kinetic energy
853
in Figure 10.
854
(a) BTC/USD market
(b) LUNA/USD market
Figure 9: Granger causality test on the 30-second Local Volatility against the VPIN
(a) BTC/USD market
(b) LUNA/USD market
Figure 10: Granger causality test on the 30-second Local Volatility against the kinetic
energy
It is apparent that the VPIN method has a worse performance in the in-
855
stantaneous volatility data with higher sampling frequency. And these results
856
prove that the kinetic energy owns significantly advantage compared to the
857
VPIN method in predicting the instantaneous volatility in a high-frequency
858
trading market. Hence, while VPIN is a powerful real-time measure of order
859
flow toxicity, it does not fully capture limit-order dynamics at deeper levels
860
of the LOB.
861
29
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 31

6.4. Comparative Analysis
862
The empirical analysis reveals that the kinetic energy measure outper-
863
forms the VPIN model in predicting short-term volatility for both Bitcoin
864
and LUNA. This superior performance to the kinetic energy measure’s ability
865
to capture not only the effects of individual order activity but also the overall
866
order book dynamics. Our model includes the LOB depth by computing the
867
kinetic energy measure of each order activity according to the LOB depth of
868
their quoted price so that their different impact on the order book can be
869
analysed quantitatively, which are often overlooked by models focusing solely
870
on transaction data.
871
The findings suggest that while the VPIN model has its merits, the kinetic
872
energy measure provides a more encompassing view of order book dynamics
873
and is thus a more effective tool for predicting short-term volatility. This
874
highlights the potential benefits of integrating concepts from econophysics
875
into financial markets.
876
These results underscore the importance of considering multiple facets of
877
market data when predicting volatility. The kinetic energy measure’s suc-
878
cess points to the potential value of developing hybrid models that combine
879
transaction data with other elements of the LOB. Such an approach could
880
provide a more accurate and comprehensive understanding of the complex
881
and rapidly changing dynamics that characterise financial markets.
882
In conclusion, the comparative analysis of the kinetic energy measure
883
and the VPIN model represents a significant contribution to the literature
884
on volatility prediction. It not only provides a novel perspective on volatility
885
prediction but also sparks a potential shift in the methodological paradigm
886
from purely econometric models to an interdisciplinary approach combining
887
financial economics and econophysics.
Further research exploring this in-
888
terdisciplinary approach could open up new vistas for improving volatility
889
prediction in financial markets.
890
7. Price Prediction: Momentum Versus Order Flow Imbalance
891
Forecasting price changes in financial markets forms the foundation of
892
trading strategies and risk management paradigms. Conventional method-
893
ologies frequently depend on the Order Flow Imbalance (OFI), a metric that
894
characterises shifts in supply and demand. We introduced a novel measure -
895
the physical momentum, conceptually rooted in physical systems - for antic-
896
ipating near-term price fluctuations.
897
30
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 32

The OFI has been widely recognised and utilised in microstructure stud-
898
ies, primarily to encapsulate the fundamental alterations in supply and de-
899
mand dynamics within financial markets. The premise of the OFI model
900
is underpinned by the belief that an augmentation in the best bid or size
901
at the best bid is indicative of an escalation in demand, while a diminution
902
signifies a contraction in demand. Inversely, a decrease in the best ask or
903
an expansion in the size at the best ask points to a surge in supply, while
904
an increment in the best ask or a contraction in size at the best ask signals
905
a decrease in supply. Consequently, this metric measures the change in the
906
supply or demand, even at a high-frequency level.
907
In contrast, the Momentum Change metric, as proposed in this study,
908
takes its conceptual basis from physical systems, and seeks to encapsulate
909
the ’momentum’ of the order book system. It is calculated as the aggregated
910
product of the velocity and the corresponding volume of each order.
By
911
incorporating the impact of each order on the price movement based on their
912
LOB depth and quoted volume, this measure provides a more holistic view
913
of the order book dynamics.
914
7.1. Introduction on the OFI
915
The OFI measure introduced by Cont et al. (2014) is a pivotal instru-
916
ment in the domain of market microstructure, playing an instrumental role
917
in assessing the swings in supply and demand dynamics. Conceived as an
918
answer to the demand for a sophisticated understanding of these oscillations,
919
the OFI measure is firmly rooted in empirical finance research and has been
920
extensively employed as a tool for market examination.
921
In theoretical terms, the OFI measure is founded on the premise that
922
the oscillations in the best bid and ask levels, in conjunction with the cor-
923
responding sizes, can act as an effective surrogate for the latent supply and
924
demand changes in the market. In specific terms, an augmentation in the
925
best bid or an augmentation in the size at the best bid is construed as a
926
surge in demand, signaling an influx of purchasing interest in the market.
927
Inversely, a diminution in these variables signifies a contraction in demand,
928
indicating a shrinkage in buying interest.
929
On the supply facet, the OFI measure operates under an analogous ratio-
930
nale. A diminution in the best ask or an augmentation in the size at the best
931
ask is perceived as a swell in supply, suggesting an increasing willingness of
932
market participants to vend. In contrast, an augmentation in the best ask
933
31
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 33

or a diminution in size at the best ask indicates a contraction in supply,
934
signifying a retrenchment in selling interest.
935
The OFI measure, therefore, acts as a vital metric that encapsulates high-
936
frequency changes in market dynamics. By providing real-time insights into
937
the state of supply and demand in the market, the OFI measure aids the
938
creation of reactive and adaptive trading strategies. It enables market par-
939
ticipants to forecast price movements and adapt their positions accordingly,
940
thus mitigating risk and optimising returns.
941
7.2. The Prediction Power on Price Change
942
(a) BTC/USD market, 1-second change
(b) BTC/USD market, 10-second change
Figure 11: Regression analysis on the match price change against the OFI
(a) BTC/USD market, 1-second change
(b) BTC/USD market, 10-second change
Figure 12: Regression analysis on the match price change against the momentum
This section provides a comprehensive empirical analysis of the predictive
943
power of two different measures, namely the Order Flow Imbalance (OFI) and
944
Momentum Change, in forecasting the price change of Bitcoin and LUNA
945
32
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 34

(a) LUNA/USD market, 1-second change
(b) LUNA/USD market, 10-second change
Figure 13: Regression analysis on the match price change against the momentum
over two distinct time horizons: one and ten seconds. For LUNA, due to
946
unavailability of certain data points, the OFI measure could not be computed,
947
and thus we only report the results for physical momentum change.
948
In order to evaluate the respective predictive abilities of trade imbalances
949
and Order Flow Imbalances with regards to price fluctuations, we conduct a
950
series of the following regressions:
951
∆Pk = αi + βiOFIk + ϵk
(12)
for the OFI measure and
952
∆Pk = αi + βiMk + ϵk
(13)
for the momentum measure.
953
These regressions are computed independently for each data subset (in-
954
dexed by i). Each subset represents an one-hour order book data sampled
955
by 1-second frequency, which typically comprises approximately 3600 data
956
points (indexed by k), collected at a frequency of one second. The details for
957
these regression analysis are listed in Table 2.
958
The OFI measure was regressed against price changes of Bitcoin over one-
959
second and ten-second horizons according to Figure 11. The R-squared values
960
were 0.094 and 0.019 for the one-second and ten-second horizons, respectively.
961
These relatively low R-squared values suggest that the predictive power of
962
the OFI measure is modest, but not negligible. The F-statistic results (373.0
963
and 70.87) and their corresponding p-values (3.83e-79 and 5.45e-17) indicate
964
that the OFI measure is statistically significant in predicting Bitcoin price
965
changes. Meanwhile, the performance of the OFI on Bitcoin data is relatively
966
33
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 35

Table 2: The regression analysis
Dataset
R2
F-statistic
Prob(F-statistic)
Omnibus
Prob(Omnibus)
Skew
Kurtosis
Durbin-Watson
Jarque-Bera (JB)
Prob(JB)
BTC/USD OFI vs ∆P 1s
0.094
373.0
3.83e-79
255.040
0.000
-0.139
5.829
2.472
1208.261
4.26e-263
BTC/USD OFI vs ∆P 10s
0.019
70.87
5.45e-17
655.211
0.000
-0.403
11.230
0.337
10204.282
0.00
BTC/USD ∆M vs ∆P 1s
0.168
723.6
2.33e-145
110.277
0.000
-0.128
4.296
2.653
261.177
1.93e-57
BTC/USD ∆M vs ∆P 10s
0.816
1.589e+04
0.00
747.131
0.000
0.737
9.455
0.970
6560.394
0.00
LUNA/USD ∆M vs ∆P 1s
0.036
137.0
4.26e-31
202.154
0.000
0.012
5.316
2.793
816.435
5.17e-178
LUNA/USD ∆M vs ∆P 10s
0.274
1375
1.43e-255
165.117
0.000
0.236
4.593
0.840
419.270
9.05e-92
weaker than the result presented by Cont et al. (2014) where the R-squared
967
value is about 0.65 for NYSE TAQ stock data, which indicates that on the
968
Bitcoin data the OFI is not as efficient as on the equities data.
969
The Momentum Change measure was regressed against price changes of
970
Bitcoin and LUNA over one-second and ten-second horizons in Figure 12.
971
For Bitcoin, the R-squared values were 0.168 and 0.816 for the one-second
972
and ten-second horizons, respectively, suggesting a stronger predictive power
973
than the OFI measure. The F-statistics (723.6 and 1.589e+04) and their cor-
974
responding p-values (2.33e-145 and 0.00) further support the significant role
975
of Momentum Change in predicting Bitcoin price changes. The coefficients
976
of the Momentum Change measure were positive and significant, suggesting
977
that an increase in momentum would lead to a price increase in Bitcoin. On
978
the other hand, this feature is not significant enough for the LUNA data in
979
Figure 13.
980
Overall, our empirical analysis reveals that the Momentum Change mea-
981
sure has a stronger predictive ability for the price change of Bitcoin compared
982
to the OFI measure. This suggests that the Momentum Change measure
983
could be a more robust tool for short-term price prediction in the cryptocur-
984
rency market.
985
7.3. Comparative Analysis
986
The empirical study offers a comparative evaluation of these two metrics.
987
For Bitcoin, it was discovered that the Momentum Change metric demon-
988
strated superior performance than the OFI in forecasting price fluctuations
989
over one-second and ten-second intervals. The R-squared values associated
990
with the Momentum Change metric were significantly larger than those af-
991
filiated with the OFI metric, suggesting a more potent predictive capacity.
992
The statistical significance of the Momentum Change metric, as evidenced
993
by the F-statistics and their corresponding p-values, further accentuates its
994
efficacy in forecasting Bitcoin price fluctuations.
995
34
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 36

Table 3: The fitted model
The fitted model
Coefficient
Standard error
t
P ≥|t|
[2.5%,
97.5%]
α1
-0.0215
0.027
-0.787
0.431
-0.075
0.032
β1
0.7208
0.037
19.313
0.000
0.648
0.794
α2
-0.2008
0.072
-2.803
0.005
-0.341
-0.060
β2
0.8237
0.098
8.418
0.000
0.632
1.016
α3
-0.0070
0.026
-0.269
0.788
-0.058
0.044
β3
0.0025
9.28e-05
26.900
0.000
0.002
0.003
α4
0.0005
0.039
0.013
0.989
-0.076
0.077
β4
0.0041
3.26e-05
126.061
0.000
0.004
0.004
α5
0.0002
0.000
0.729
0.466
-0.000
0.001
β5
4.441e-06
3.79e-07
11.706
0.000
3.7e-06
5.18e-06
α6
0.0034
0.000
7.305
0.000
0.003
0.004
β6
6.637e-06
1.79e-07
37.075
0.000
6.29e-06
6.99e-06
In the case of LUNA, due to data limitations, only the Momentum Change
996
metric could be computed. However, the results indicated a substantial pre-
997
dictive capability of the Momentum Change metric for LUNA prices, espe-
998
cially over a ten-second interval.
999
The results imply that while the OFI metric provides critical insights
1000
into the dynamics of supply and demand, the Momentum Change metric, by
1001
amalgamating price and volume fluctuations, offers a more comprehensive
1002
understanding of market dynamics. This underscores the potential advan-
1003
tages of integrating concepts from the physical sciences into financial market
1004
analysis. The superior performance of the momentum measure over the OFI
1005
implies potential limitations of the OFI in forecasting price fluctuations in
1006
cryptocurrency data, particularly when compared with stock data.
This
1007
underscores the distinct characteristics of cryptocurrency markets and the
1008
necessity for further experiments of the Physical Model on the other asset
1009
classes.
1010
The comparative empirical study between the Momentum Change met-
1011
ric and the OFI model constitutes a notable addition to the literature on
1012
price change prediction. It not only introduces a fresh perspective but also
1013
indicates a paradigm shift from traditional econometric models to an inter-
1014
disciplinary approach that merges financial economics and physical sciences.
1015
Further investigation into this interdisciplinary approach could potentially
1016
facilitate advancements in price change prediction within financial markets.
1017
35
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 37

8. Benchmarking the Physical Model: Insights Into Predictive Per-
1018
formance
1019
Based on the work in Sirignano (2019), the Deep Long Short Term Mem-
1020
ory (LSTM) model designed by Sirignano and Cont (2019) was constituted
1021
by three layers of LSTM units, succeeded by a fully-connected layer of recti-
1022
fied linear units (ReLUs). The subsequent application of a softmax activation
1023
function facilitated the generation of a probability distribution for the future
1024
price movement. Sirignano and Cont (2019) compared the performance of
1025
the Deep LSTM model against the other linear models, especially Vector
1026
Autoregressive (VAR) model. The empirical results revealed that the Deep
1027
LSTM model transcended these counterparts, demonstrating its capability to
1028
capture non-linear relationships in the LOB data which other models might
1029
miss.
1030
The DeepLOB model, further proposed in Zhang et al. (2019), introduces
1031
a deep learning framework for predicting short-term price movements using
1032
limit order book (LOB) data.
It combines convolutional neural networks
1033
(CNNs) to extract spatial features from LOB snapshots with long short-
1034
term memory (LSTM) networks to capture temporal dependencies.
This
1035
hybrid architecture enables effective learning from high-dimensional, noisy
1036
market data. DeepLOB demonstrates strong predictive performance across
1037
multiple instruments and maintains generalisability to unseen stocks, making
1038
it a robust tool for financial forecasting.
1039
We replicated the aforementioned two models as baseline to test the ca-
1040
pability of our Physical Model. Our dataset comprises snapshots of the LOB,
1041
encapsulating price and volume data for the 10 highest bid and 10 lowest ask
1042
orders. The snapshots data was reconstructed from the Coinbase exchange
1043
for Bitcoin/USD pair during 2023/09/16 02:00 - 2023/09/16 14:00. Note
1044
that we did not test the Deep LSTM model on LUNA/USD pair during flash
1045
crash due to the lack of corresponding snapshots data.
1046
Each observation or timestamp in the raw data thus constitutes 40 fea-
1047
tures: 10 bid prices, 10 bid volumes, 10 ask prices, and 10 ask volumes.
1048
We computed the physical measure with the Physical Model and synchro-
1049
nised them to the original snapshot data. The snapshot dataset contained
1050
2,018,900 LOB snapshots in the span of 12 hours, and the 80% of them are
1051
used as training set while the left for the test set. The physical measures are
1052
computed from the Level-3 order book data with length 9,839,922 during the
1053
same time span. We also carried out further experiments by incorporating
1054
36
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 38

the physical measures including Market Momentum and Market Energy as
1055
the training data. The classification of training set and test set is depicted
1056
in Figure 14, where the data labelled with blue dotted line is the training set
1057
and red for the test set.
1058
Figure 14: Training/Test partition on the dataset
Before feeding the data into the LSTM, we subjected it to rigorous prepro-
1059
cessing. We standardised the dataset ensuring zero mean and unit variance
1060
for each feature. This scaling is imperative for neural networks to ensure
1061
all input features are treated with equal importance and to aid in model
1062
convergence.
1063
8.1. Benchmark Models
1064
The Deep LSTM model. Sirignano and Cont (2019) utilised a deep
1065
feedforward neural network, where the input was several layers of the limit
1066
order book (i.e., levels of bids and asks, quantities at each level, etc.), and the
1067
output was the future price change after a certain fixed time horizon. They
1068
used a large dataset to train the neural network, optimising the model’s
1069
weights using backpropagation.
The model was trained to minimise the
1070
difference between its predicted price changes and the actual price changes
1071
observed in the data.
1072
Instead of handcrafting features as in traditional finance models, the Deep
1073
LSTM model was trained to directly learn from the order book data. This
1074
37
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 39

automatic feature extraction capability is crucial for understanding complex
1075
structures and patterns in financial data.
1076
Sirignano and Cont (2019) compared the performance of the Deep LSTM
1077
model with other benchmark models. The Deep LSTM outperformed these
1078
models, demonstrating its capability to capture non-linear relationships in
1079
the LOB data which other models might miss. Apart from its predictive
1080
power, the model’s importance lies in its ability to shed light on the mi-
1081
crostructure of financial markets. The patterns and features automatically
1082
learned by the Deep LSTM model can be interpreted to gain insights into
1083
the underlying mechanisms of price formation in financial markets.
1084
In essence, their study showcases the power of deep learning in capturing
1085
and understanding the complex dynamics of financial markets, particularly
1086
when it comes to the microstructure of how prices are formed. It also em-
1087
phasises the potential of deep learning to unveil universal features of price
1088
formation.
1089
The model is designed to accommodate sequences of fixed length T = 10,
1090
each embedding 40 features, reflective of the bid-ask dynamics in our dataset.
1091
The network consists of a stack of three LSTM layers, each with 32 hidden
1092
units. These layers use the hyperbolic tangent (tanh) activation for hidden
1093
states and the hard-sigmoid function for recurrent activations. Dropout with
1094
a rate of 0.2 follows each LSTM layer to prevent overfitting. The LSTM
1095
layers are configured with return sequences=True for the first two layers
1096
and return sequences=False for the third, effectively summarising the se-
1097
quence into a final hidden representation. The kernel and recurrent weight
1098
initialisers follow the Glorot Uniform and Orthogonal schemes, respectively,
1099
ensuring stable training. This deep configuration enables the model to cap-
1100
ture hierarchical temporal patterns across the order book dynamics. The
1101
structure of the Deep LSTM layers is demonstrated as follows:
1102
• Window length: Each training example comprises a sequence of the
1103
last T = 10 snapshots.
1104
• Feature dimension: F = 40 raw depth-of-book features per snapshot,
1105
giving an input tensor of shape (T, F) = (10, 40).
1106
• Target: The continuous mid-price change ∆pt+0.5s observed half a sec-
1107
ond after the final snapshot in each window.
1108
• Input layer: Input(10, 40).
1109
38
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 40

• Recurrent layers: A stack of three LSTM(32) layers. The first two lay-
1110
ers use return sequences=True, while the final uses return sequences=False.
1111
• Regularisation: Dropout(0.2) applied after each LSTM layer.
1112
• Dense layer: Dense(32, ReLU) adds a non-linear transformation before
1113
output.
1114
• Output layer: Dense(1, linear) predicts the continuous price change.
1115
The model employs a fully connected dense layer with a linear activation
1116
function for regression output.
The chosen optimiser for the model was
1117
Adam with a learning rate of 10−4, known for its efficient handling of sparse
1118
gradients and adaptability. The primary metric for model evaluation was the
1119
mean squared error (MSE), alongside directional accuracy for classification
1120
insight.
1121
The model was trained over 30 epochs with early stopping patience set to
1122
10. The batch size, a crucial hyperparameter, was set at 256, indicating the
1123
model processes 256 sequences simultaneously in each iteration to balance
1124
convergence stability and memory efficiency.
This configuration supports
1125
effective learning of short-term price movements driven by order book dy-
1126
namics.
1127
The DeepLOB model. This subsection provides an academically rig-
1128
orous exposition of the DeepLOB model, a convolutional - recurrent neural
1129
network expressly designed for limit order book (LOB) data.
1130
The original formulation by Zhang et al. (2019) couples spatial convo-
1131
lutions with temporal recurrent layers to capture local depth-of-book pat-
1132
terns and their evolution across time. In contrast with earlier LSTM-only
1133
approaches, DeepLOB first learns hierarchical representations of the spa-
1134
tial structure of the LOB (e.g. bid-ask levels, volume imbalances) and then
1135
models their temporal dynamics, thereby extracting richer features for price-
1136
movement prediction.
1137
Similar to the Deep LSTM examined previously, DeepLOB eschews hand-
1138
crafted features in favour of end-to-end learning. However, by incorporating
1139
convolutional kernels of varying receptive fields together with an Inception-
1140
style module, it is able to detect short-, medium- and long-range level interac-
1141
tions that a pure recurrent model might overlook. Empirical results in Zhang
1142
et al. (2019) demonstrate that this hybrid architecture outperforms both tra-
1143
ditional statistical models and purely recurrent deep networks, highlighting
1144
39
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 41

the explanatory power of convolutional feature maps for market microstruc-
1145
ture. The architecture of our implemented DeepLOB model is as follows:
1146
• Input layer: A tensor of shape (T, NF, 1) where T = 10 time steps
1147
and NF = 40 depth-wise features (yielding 10 × 40 = 400 raw LOB
1148
features).
1149
• Convolutional block 1:
1150
– Conv2D(16, (1, 2), stride = (1, 2)) with LeakyReLU;
1151
– two Conv2D(16, (4, 1)) layers with same padding and LeakyReLU
1152
activations.
1153
Reduces the feature-axis width from 40 to 20 while extracting local
1154
level interactions.
1155
• Convolutional block 2: Repeats the above pattern, compressing the
1156
width from 20 to 10 and refining spatial features (Conv2D(16, (1, 2))
1157
then two Conv2D(16, (4, 1))).
1158
• Feature-collapse block:
1159
– Conv2D(16, (1, 10)) to collapse width 10 →1, followed by two
1160
Conv2D(16, (4, 1)) layers (all with LeakyReLU).
1161
Produces a (T, 1, 16) representation.
1162
• Inception-style module: Three parallel branches:
1163
– 1 × 1 then 3 × 1 convolutions with 32 filters,
1164
– 1 × 1 then 5 × 1 convolutions with 32 filters,
1165
– 3 × 1 max-pool followed by a 1 × 1 convolution with 32 filters,
1166
each using LeakyReLU and concatenated to yield (T, 1, 96).
1167
• Reshape & Dropout: The tensor is reshaped to (T, 96) and a dropout
1168
layer (p = 0.2) is applied to mitigate overfitting.
1169
• Temporal layer: A single LSTM(16) processes the ten time steps, sum-
1170
marising temporal dependencies.
1171
• Output layer: A fully connected Dense(1) with linear activation outputs
1172
the predicted mid-price change ∆p.
1173
40
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 42

Model parameters and training details.. The implementation adopts the Adam
1174
optimiser with a learning rate of 10−4 and a mean-squared-error loss, reflect-
1175
ing the continuous nature of the prediction target. Training is performed for
1176
30 epochs with early stopping patience set to 10, using a batch size of 256 on
1177
80% of the chronologically ordered data (with 10% of that subset reserved
1178
for validation). Empirical tuning confirmed that using 16 convolutional fil-
1179
ters and 16 LSTM units strikes a good balance between model capacity and
1180
overfitting risk.
1181
In summary, DeepLOB extends pure recurrent frameworks by embedding
1182
convolutional inductive biases that account for the hierarchical structure of
1183
order books, delivering state-of-the-art predictive performance and offering
1184
interpretable insights into level interactions within high-frequency markets.
1185
The LOB-Transformer model. This subsection presents the Limit
1186
Order Book (LOB) Transformer model - a hybrid patch-based Vision Trans-
1187
former (ViT) augmented with an LSTM read-out layer - tailored for high-
1188
frequency market data. Inspired by the patch-embedding strategy of the orig-
1189
inal Transformer architecture Vaswani et al. (2017), the model first tokenises
1190
the two-dimensional LOB snapshot into non-overlapping patches, projects
1191
them into an embedding space, and then applies stacked self-attention blocks
1192
to learn contextual interactions before a recurrent layer captures longer-
1193
horizon temporal dependencies.
1194
Unlike convolutional approaches such as DeepLOB, the Transformer re-
1195
lies on global self-attention, permitting each patch token to attend to every
1196
other, thereby modelling higher-order cross-level relationships without induc-
1197
tive biases about locality. The subsequent LSTM summarises the sequence
1198
of attended patch embeddings, furnishing an expressive representation for
1199
mid-price change regression. We implemented an LOB-Transformer model
1200
with the following architecture:
1201
• Input tensor: (20, 20, 1), obtained by reshaping each (10, 40) LOB
1202
window into a “pseudo-image” of height 20 and width 20 (so that 20 ×
1203
20 = 400 raw features).
1204
• Patch extraction: A Patches layer splits the (20×20) image into 4×4 =
1205
16 non-overlapping patches of size (5 × 5), flattening each patch into a
1206
vector of length 5 · 5 · 1 = 25.
1207
• Patch encoder: Each patch vector is linearly projected to a d = 32-
1208
41
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 43

dimensional embedding and augmented with learned positional em-
1209
beddings, producing a sequence of length 16 and dimension 32.
1210
• Transformer encoder (repeated twice):
1211
– Layer normalisation;
1212
– multi-head self-attention with 2 heads (key dim=32) and dropout
1213
rate 0.1;
1214
– residual addition;
1215
– MLP block with hidden dimensions [64, 32], ReLU activations,
1216
and dropout 0.1;
1217
– second residual addition.
1218
These operations yield contextualised patch embeddings of shape (16, 32).
1219
• Representation layer: Layer normalisation followed by dropout p = 0.5
1220
for regularisation.
1221
• Temporal aggregation: A single LSTM(64) (returning sequences) pro-
1222
cesses the 16 patch embeddings; its final hidden state is passed through
1223
batch normalisation.
1224
• Dense head: A Dense(64, ReLU) layer with batch normalisation and
1225
dropout 0.2 adds a non-linear transformation before the output.
1226
• Output layer: A Dense(1) with linear activation outputs the predicted
1227
mid-price change ∆p.
1228
Model parameters and training details.. The model is instantiated with projection dim=
1229
32, two Transformer layers, two attention heads, and an LSTM of 64 units,
1230
followed by a dense layer of 64 units. The Adam optimiser with learning
1231
rate 3 × 10−6 minimises the mean-squared-error loss. Training proceeds for
1232
up to 50 epochs with early stopping patience set to 10, using a batch size of
1233
1024 on the earliest 80% of samples, reserving 10% of that subset for valida-
1234
tion and 20% for out-of-sample evaluation. Dropout rates of 0.1 within the
1235
Transformer, 0.5 after the Transformer, and 0.2 in the dense head mitigate
1236
overfitting given the limited number of epochs.
1237
42
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 44

In essence, the LOB-Transformer model integrates global self-attention
1238
with recurrent temporal modelling, providing a flexible framework for cap-
1239
turing both spatial depth-of-book interactions and their evolution across time
1240
in high-frequency trading environments.
1241
8.1.1. The Prediction Accuracy
1242
Exploratory Analysis of the Experimental Set-up
1243
This study assesses whether physically-motivated order book features can
1244
enhance short-horizon price-direction forecasting. Multiple experiments were
1245
carried out:
1246
• Physics-based baseline: The Physical Model converts full Level-3 order
1247
book data into the cumulation of four measures - kinetic energy of order
1248
submission, kinetic energy of order cancellation, upward momentum,
1249
and downward momentum computed from the methods in Section 4 -
1250
without any parameter training. When evaluated on an event-driven
1251
test set the model achieved a directional accuracy of 64.44 % at a 0.5 s
1252
horizon and 61.88 % at a 1 s horizon.
1253
• Deep-learning baselines: Three architectures commonly used for LOB
1254
forecasting were implemented: Deep LSTM by Sirignano and Cont
1255
(2019), DeepLOB by Zhang et al. (2019), and a proprietary LOB-
1256
Transformer. Each network was trained (i) on Level-2 snapshot data
1257
only, (ii) on the physical measures only, and (iii) on an augmented input
1258
consisting of snapshots plus the four physical measures.
1259
Data alignment: Level-3 data arrive at a much higher frequency than
1260
the snapshots supplied. For each ticker, the cumulative physical measures
1261
were therefore merged into the snapshot stream that selects the most recent
1262
physical observation at or before each snapshot time stamp. The resulting
1263
dataframe provides a single, temporally aligned input row for every snapshot.
1264
Accuracy metrics: The model performance were estimated using the di-
1265
rectional predicting accuracy function given by Sirignano and Cont (2019) in
1266
equation 14, as the models were trained to forecast the direction of the next
1267
price change. Note that the number of correct prediction is calculated from
1268
the total correct forecasts of the model on the direction of price changes every
1269
time an event of price change occurs, where the datapoints are not sampled
1270
equally but are event-driven.
1271
43
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 45

DirectionalAccuracy = Number of correct predictions
Total number of price changes × 100%. (14)
In our study, two notions of different accuracies are reported:
1272
• Sklearn Accuracy is the standard sklearn score: the proportion of
1273
samples for which the predicted sign of the price change matches the
1274
true sign, counting every sample, including those in which either value
1275
is exactly zero.
1276
• Directional Accuracy is better for evaluating high-frequency predictions
1277
decreasing the impact of market microstructure noise: it ignores any
1278
observation where the true or predicted price change is zero and then
1279
measures the fraction of sign agreements among the remaining, strictly
1280
non-zero cases. Consequently this figure can diverge from the conven-
1281
tional accuracy, especially when the test set contains many negligible
1282
price moves.
1283
In general, during training and testing the following statistics were recorded:
1284
directional accuracy, sklearn accuracy, precision, recall, F1, and ROC AUC.
1285
Experimental Analysis
1286
All deep models were optimised with cross-entropy loss on binarised di-
1287
rection labels. Test-set results for every architecture and input variant are
1288
listed in Table 4 for all models.
1289
In addition to the machine-learning experiments, we also evaluated a
1290
simple physical momentum predictor that uses only the recent change in cu-
1291
mulative net momentum to forecast the sign of the mid-price change, without
1292
any trainable parameters. Specifically, for each timestamp t, we compute
1293
∆Ppast = P(t) −P
 t −0.1 s

,
where P(·) denotes the cumulative sum of net momentum. We then compare
1294
∆Ppast with the actual mid-price change over the next horizon ∆pricefuture =
1295
price
 t + h

−price(t) (with h = 0.5 s or 1 s). A correct directional pre-
1296
diction is counted whenever ∆Ppast and ∆pfuture share the same sign (both
1297
positive or both negative).
Because this heuristic involves no fitted pa-
1298
rameters, standard metrics that require model-based probability estimates
1299
44
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 46

(such as sklearn accuracy, precision, recall, F1, or ROC AUC) are not de-
1300
fined. Instead, we report only the resulting directional accuracy-termed di-
1301
rectional accuracy - which is simply the fraction of timestamps for which
1302
sign(∆Ppast) = sign(∆pricefuture). Consequently, metrics such as accuracy,
1303
precision, recall, F1, and ROC AUC pertain only to models that involve
1304
learned parameters; they are omitted for the physical-momentum baseline.
1305
Although the neural networks attain the highest headline scores, it is
1306
noteworthy that the Physical Model, which requires no training, still achieves
1307
accuracies of 65.7% (0.5 s horizon) and 64.0% (1 s horizon). In other words,
1308
a purely mechanistic description of order book dynamics already delivers a
1309
small but statistically significant forecasting edge without the computational
1310
overhead of deep learning. These results establish the Physical Model as a
1311
robust baseline.
1312
The experimental results from all settings are listed in Table 4, while
1313
the comparisons on the directional accuracy metric are demonstrated in Fig-
1314
ure 15.
1315
The experiments with predicting time horizon of 0.5 s are shown in Fig-
1316
ure 15a, where physics-derived features (orange) consistently outperform
1317
snapshot - only baselines (grey), while deep networks fed solely with physi-
1318
cal measures (green) recover most of the benefit without any depth-of-book
1319
images. The untrained Physical Model (blue) remains a strong lightweight
1320
benchmark.
1321
As for predicting time horizon of 1 s compared in Figure 15b, the perfor-
1322
mance patterns mirror the 0.5 s horizon: combining physics-derived features
1323
with LOB snapshots yields the best results, whereas physics-only deep mod-
1324
els still close much of the gap, confirming the predictive power embedded in
1325
the four physical measures alone.
1326
45
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 47

(a) Directional accuracy at a 0.5 s prediction horizon
(b) Directional accuracy at a 1 s prediction horizon
Figure 15: Comparisons on the directional accuracy across different models, experimental
settings and datasets
46
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 48

Table 4: Comparison of evaluation metrics across models and prediction horizons
Model & Horizon
Directional Accuracy
Sklearn Accuracy
Precision
Recall
F1
ROC AUC
Physical Momentum - resampled to snapshot time (0.5 s)
0.657301
-
-
-
-
-
Physical Momentum - resampled to snapshot time (1 s)
0.640118
-
-
-
-
-
Deep LSTM - physical measures only (0.5 s)
0.684597
0.643175
0.590833
0.674087
0.629720
0.692204
Deep LSTM - physical measures only (1 s)
0.685300
0.649411
0.610430
0.702113
0.653069
0.700474
DeepLOB - physical measures only (0.5 s)
0.682560
0.651162
0.608853
0.629281
0.618898
0.684500
DeepLOB - physical measures only (1 s)
0.679050
0.651779
0.625133
0.647130
0.635941
0.691433
LOB-Transformer - physical measures only (0.5 s)
0.676852
0.640404
0.590698
0.654895
0.621142
0.677958
LOB-Transformer - physical measures only (1 s)
0.673885
0.646862
0.619856
0.642864
0.631150
0.688431
Deep LSTM - snapshot only (0.5 s)
0.676897
0.636452
0.583362
0.672958
0.624965
0.681198
Deep LSTM - snapshot data only (1 s)
0.671923
0.640401
0.604406
0.679807
0.639893
0.683927
DeepLOB - snapshot only (0.5 s)
0.690460
0.646329
0.592194
0.688178
0.636588
0.693916
DeepLOB - snapshot only (1 s)
0.688503
0.651998
0.614595
0.695975
0.652758
0.700247
LOB-Transformer - snapshot only (0.5 s)
0.612476
0.580863
0.528183
0.645002
0.580776
0.616468
LOB-Transformer - snapshot only (1 s)
0.619193
0.579604
0.537200
0.761754
0.630067
0.621915
Deep LSTM - snapshot & physical measures (0.5 s)
0.693153
0.653711
0.601555
0.683185
0.639777
0.692689
Deep LSTM - snapshot & physical measures (1 s)
0.693166
0.660953
0.622677
0.707029
0.662177
0.704316
DeepLOB - snapshot & physical measures (0.5 s)
0.690947
0.648535
0.596498
0.677407
0.634383
0.695138
DeepLOB - snapshot & physical measures (1 s)
0.693882
0.661360
0.630580
0.674759
0.651922
0.709587
LOB-Transformer - snapshot & physical measures (0.5 s)
0.661615
0.596492
0.532882
0.839080
0.651812
0.676322
LOB-Transformer - snapshot & physical measures (1 s)
0.663810
0.635582
0.601237
0.666958
0.632395
0.679886
Several patterns emerge from Table 4. First, the baseline of physical mo-
1327
mentum directly computed from Level-3 order flow without any optimisation
1328
has a performance only a few percentage lower than the best-performing deep
1329
learning architecture, despite requiring neither GPU training time nor hyper-
1330
parameter search. It demonstrates that much of the short-term predictive
1331
signal in a limit order book is contained in mechanically interpretable quan-
1332
tities such as net momentum and energy, rather than in opaque non-linear
1333
transformations of raw depth snapshots.
1334
Another observation is that deep learning on the physical measures alone
1335
surpasses the performance obtained from the raw depth snapshots in two
1336
cases.
For example, the Deep LSTM fed only the four physics variables
1337
reaches 0.684 (0.5 s) and 0.685 (1 s) directional accuracy, beating its snapshot-
1338
only counterpart by roughly two percentage points. The LOB-Transformer
1339
benefits even more: physical-only training lifts its 1-second accuracy from
1340
0.619 to 0.673, a gain of more than five percentage points. These results
1341
confirm that the physics features capture a large share of the short-horizon
1342
signal that is usually sought with much higher-dimensional inputs.
1343
Second, augmenting snapshot tensors with four physical measures (energy
1344
of new order submissions, energy of cancellations, upward momentum and
1345
downward momentum) always improves the neural networks’ out-of-sample
1346
scores. For the Deep LSTM model, sklearn accuracy rises from 0.636 to 0.654
1347
(0.5 s horizon) and ROC AUC from 0.681 to 0.693, while directional accuracy
1348
increases by roughly 2 percentage points for every architecture tested. The
1349
47
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 49

gain is largest for the LOB-Transformer, whose global self-attention evidently
1350
benefits from an explicit, physics-derived summary of recent order-flow stress.
1351
This synergy shows that the Physical Model is not merely a light-weight
1352
alternative to deep learning; it is a complementary feature generator that
1353
can be dropped into existing pipelines to boost performance with negligible
1354
additional latency.
1355
Third, the table highlights a trade-off between raw headline accuracy and
1356
computational cost. All deep networks require tens of epochs of GPU train-
1357
ing and non-trivial feature engineering (windowing, normalisation and label
1358
alignment). The Physical Model, by contrast, is trained on no data, while
1359
it merely requires the calculation of Active Depth in Section 4.2 which can
1360
be computed real-time with little computing power and time. The Physical
1361
Model is able to be executed in linear time with respect to the data stream,
1362
and produces interpretable alarms suitable for real-time surveillance systems.
1363
For practitioners concerned with computing power consumption, deployment
1364
complexity or model interpretability, the physical features offer a principled
1365
middle ground: they deliver much of the accuracy advantage of deep learning
1366
while preserving the transparency of the signal.
1367
Finally, as the momentum baseline is computed in an event-driven man-
1368
ner and then resynchronised to an arbitrary snapshot clock - it is not tied
1369
to a particular sampling frequency. This is in stark contrast to supervised
1370
networks, whose weights are horizon-specific and must be re-trained if the
1371
prediction latency is required to be changed. Hence the Physical Model gen-
1372
eralises across both temporal resolutions and market venues with minimal
1373
re-calibration.
1374
These findings reinforce two findings of this study: (i) Purely statistical
1375
or deep learning baselines under-utilise microstructural information that is
1376
readily available in the message stream; the Physical Model captures that
1377
information explicitly. (ii) When the physical measures are supplied to the
1378
networks, their marginal benefit exceeds that of adding yet another layer
1379
or attention head, implying that future work should focus on richer feature
1380
engineering rather than ever-deeper architectures. Any comparative analy-
1381
sis that follows should therefore emphasise complementarity rather than a
1382
winner-takes-all narrative: the best practice is to couple lightweight, mech-
1383
anistically grounded signals with data-hungry models when latency budgets
1384
permit.
1385
Comparative Analysis
1386
Efficiency and deployability: Deep architectures demand GPU hardware,
1387
48
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 50

extensive hyper-parameter tuning and hours of training. By contrast, the
1388
Physical Model runs in real time on a standard CPU because its computa-
1389
tions reduce to algebraic operations on incoming LOB updates. In latency-
1390
sensitive trading systems every millisecond counts; therefore, a model that
1391
incurs zero training time and minimal inference latency represents a substan-
1392
tial engineering advantage.
1393
Data parsimony and robustness: Large-scale neural networks perform
1394
best when vast, stationary data sets are available. In volatile crypto markets,
1395
distributional shifts are frequent and can quickly erode learnt representations.
1396
The Physical Model sidesteps this fragility: its parameters are derived from
1397
first principles (trade-arrival rates, volume imbalance, queue dynamics) and
1398
update organically with the latest order-book state, maintaining relevance
1399
without re-training.
1400
Interpretability and risk management:
Regulatory and fiduciary con-
1401
straints increasingly require transparent decision rules. The Physical Model’s
1402
components (e.g. best-bid queue depletion, depth-weighted imbalance) map
1403
directly to observable microstructural phenomena, enabling traders and risk
1404
managers to trace a forecast back to concrete market mechanisms. In con-
1405
trast, attention maps or LSTM cell activations rarely translate into action-
1406
able narratives.
1407
Scalability across depths and assets: Neural networks typically truncate
1408
the order book to the top 10-20 levels for tractability. The Physical Model can
1409
ingest arbitrarily deep queues because its computational cost grows linearly
1410
with depth, not quadratically with parameter count. This flexibility is vital
1411
when quoting on venues where meaningful liquidity may reside dozens of ticks
1412
away. Moreover, because the model is data-agnostic, it transfers effortlessly
1413
from highly liquid BTC/USD to thinner alt-coin pairs without re-estimation.
1414
Complementarity rather than competition: Finally, nothing precludes in-
1415
tegrating approaches: the outputs of physical model can be appended as
1416
features to Transformer or LSTM inputs, supplying inductive bias that may
1417
accelerate convergence and improve stability. Our empirical results already
1418
hint at this synergy: augmenting snapshot data with physical measures raises
1419
the LSTM’s one-second directional accuracy by 2.12% and boosts LOB-
1420
Transformer by 4.47%.
1421
Order Book Depth and Price Dynamics: The study of Cont et al. (2014)
1422
discovered that while the first level has the strongest impact on price dy-
1423
namics, deeper depths still contain information relevant for forecasting. The
1424
experimental findings from Sirignano and Cont (2019) and Zhang et al. (2019)
1425
49
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 51

further underscored and proved the predictive significance of the deeper
1426
depths in the LOB on price dynamics. They defined and calculated sen-
1427
sitivity of a given depth in the LOB, which was 1.7% for the best bid/best
1428
ask, 0.4% for depth 2, 0.2% for both depth 3 and 4, and the total sensitiv-
1429
ity of depth 5-10 was 0.4%. The truth is the depth beyond contain even
1430
more significant information, however, the restriction on computing power
1431
and model complexity of deep learning models make it difficult to train with
1432
the data for deeper depth. Contrarily, the Physical Model decides the depths
1433
relevant to the price dynamics by calculating the defined Active Depth in or-
1434
der to take full advantage. As a result, the Physical Model would be more
1435
efficient to capture the price dynamics compared to deep learning models.
1436
In summary, while deep neural networks currently post the highest raw
1437
accuracies, the Physical Model offers a compelling blend of real-time oper-
1438
ability, interpretability and cross-asset robustness. Its favourable cost-benefit
1439
profile makes it an indispensable component of any practical high-frequency
1440
forecasting toolkit.
1441
9. Conclusion
1442
This paper presents a novel framework for analyzing limit order book
1443
dynamics through a physics-inspired lens. By modelling individual orders
1444
as physical particles and conceptualising the order book as a physical sys-
1445
tem, we introduce two interpretable microstructural measures, kinetic energy
1446
and momentum, to characterise and forecast short-term price volatility and
1447
directional changes. Crucially, we define the concept of Active Depth to iso-
1448
late the region of the order book where the most influential order activity
1449
occurs, allowing for efficient, high-resolution modelling without relying on
1450
time-based snapshots.
1451
Our approach makes full use of Level-3 order book data, preserving
1452
temporal granularity and enabling a microscopic view of market dynamics.
1453
Through a case study of the LUNA cryptocurrency flash crash, we reveal
1454
contrasting behaviours between limit and market orders and offer empiri-
1455
cal evidence that further supports the physical interpretation of market mi-
1456
crostructure. The empirical analysis demonstrates that our physical model
1457
consistently outperforms established measures such as VPIN and Order Flow
1458
Imbalance (OFI), and rivals state-of-the-art deep learning architectures in-
1459
cluding Deep LSTM, DeepLOB, and Transformer-based models.
1460
50
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 52

Beyond predictive performance, the Physical Model is computationally
1461
efficient, real-time deployable, scalable to deep levels of the LOB, and easily
1462
interpretable. Furthermore, we show that these physics-based measures en-
1463
hance the accuracy of deep learning models when integrated as input features,
1464
underscoring their value not only as standalone tools but also as complemen-
1465
tary signal generators.
1466
This work highlights the potential of econophysics in the financial analysis
1467
of digital asset, and encourages a synthesis of physical intuition with modern
1468
machine learning. Future work could extend this framework to other asset
1469
classes such as equities, foreign exchanges and futures, or develop hybrid
1470
models that fuse physical and data-driven components for even more robust
1471
forecasting and interpretability. Together, these directions offer a compelling
1472
path toward a deeper, more structured understanding of financial market
1473
dynamics..
1474
References
1475
Abad, D., Yag¨ue, J., 2012. From pin to vpin: An introduction to order flow
1476
toxicity. The Spanish Review of Financial Economics 10, 74–83.
1477
Ait-Sahalia, Y., Yu, J., 2008. High frequency market microstructure noise
1478
estimates and liquidity measures. Technical Report. National Bureau of
1479
Economic Research.
1480
Andersen, T.G., Bondarenko, O., 2014. Vpin and the flash crash. Journal of
1481
Financial Markets 17, 1–46.
1482
Bak, P., Paczuski, M., Shubik, M., 1997. Price variations in a stock market
1483
with many agents. Physica A: Statistical Mechanics and its Applications
1484
246, 430–453.
1485
Borland, L., 2012.
Statistical signatures in times of panic: markets as a
1486
self-organizing system. Quantitative Finance 12, 1367–1379.
1487
Bouchaud, J.P., Farmer, J.D., Lillo, F., 2009. How markets slowly digest
1488
changes in supply and demand, in: Handbook of financial markets: dy-
1489
namics and evolution. Elsevier, pp. 57–160.
1490
Bouchaud, J.P., Gefen, Y., Potters, M., Wyart, M., 2003. Fluctuations and
1491
response in financial markets: the subtle nature ofrandom’price changes.
1492
Quantitative finance 4, 176.
1493
51
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 53

Bouchaud, J.P., M´ezard, M., Potters, M., 2002. Statistical properties of stock
1494
order books: empirical results and models. Quantitative finance 2, 251.
1495
Cartea, A., Donnelly, R., Jaimungal, S., 2018. Enhancing trading strategies
1496
with order book signals. Applied Mathematical Finance 25, 1–35.
1497
Challet, D., Stinchcombe, R., 2003. Non-constant rates and over-diffusive
1498
prices in a simple model of limit order markets. Quantitative finance 3,
1499
155.
1500
Chiarella, C., Iori, G., 2002. A simulation analysis of the microstructure of
1501
double auction markets. Quantitative finance 2, 346.
1502
Cont, R., Kukanov, A., Stoikov, S., 2014. The price impact of order book
1503
events. Journal of financial econometrics 12, 47–88.
1504
Daniels, M.G., Farmer, J.D., Gillemot, L., Iori, G., Smith, E., 2003. Quan-
1505
titative model of price diffusion and market friction based on trading as a
1506
mechanistic random process. Physical review letters 90, 108102.
1507
Doering, J., Fairbank, M., Markose, S., 2017. Convolutional neural networks
1508
applied to high-frequency market microstructure forecasting, in: 2017 9th
1509
computer science and electronic engineering (ceec), IEEE. pp. 31–36.
1510
Easley, D., De Prado, M.M.L., O’Hara, M., 2011. The microstructure of
1511
the “flash crash”: flow toxicity, liquidity crashes, and the probability of
1512
informed trading. The Journal of Portfolio Management 37, 118–128.
1513
Easley, D., L´opez de Prado, M., O’Hara, M., Zhang, Z., 2021. Microstructure
1514
in the machine age. The Review of Financial Studies 34, 3316–3363.
1515
Easley, D., L´opez de Prado, M.M., O’Hara, M., 2012. Flow toxicity and
1516
liquidity in a high-frequency world. The Review of Financial Studies 25,
1517
1457–1493.
1518
Eisler, Z., Bouchaud, J.P., Kockelkoren, J., 2012. The price impact of order
1519
book events: market orders, limit orders and cancellations. Quantitative
1520
Finance 12, 1395–1419.
1521
Farmer, J.D., Gerig, A., Lillo, F., Mike, S., 2006.
Market efficiency and
1522
the long-memory of supply and demand: Is price impact variable and
1523
permanent or fixed and temporary? Quantitative finance 6, 107–112.
1524
52
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 54

Farmer, J.D., Lillo, F., 2004. On the origin of power-law tails in price fluc-
1525
tuations. Quantitative Finance 4, C7.
1526
Farmer, J.D., Patelli, P., Zovko, I.I., 2005. The predictive power of zero
1527
intelligence in financial markets. Proceedings of the National Academy of
1528
Sciences 102, 2254–2259.
1529
French, K.R., Schwert, G.W., Stambaugh, R.F., 1987. Expected stock re-
1530
turns and volatility. Journal of financial Economics 19, 3–29.
1531
Granger, C.W., 1969. Investigating causal relations by econometric models
1532
and cross-spectral methods. Econometrica: journal of the Econometric
1533
Society , 424–438.
1534
Huang, Y., Zhou, C., Cui, K., Lu, X., 2024. A multi-agent reinforcement
1535
learning framework for optimizing financial trading strategies based on
1536
timesnet. Expert Systems with Applications 237, 121502.
1537
Kercheval, A.N., Zhang, Y., 2015. Modelling high-frequency limit order book
1538
dynamics with support vector machines. Quantitative Finance 15, 1315–
1539
1329.
1540
Li, H., Polukarov, M., Ventre, C., 2023. Detecting financial market manip-
1541
ulation with statistical physics tools, in: Proceedings of the Fourth ACM
1542
International Conference on AI in Finance, pp. 1–1.
1543
Lillo, F., Doyne Farmer, J., 2005. The key role of liquidity fluctuations in
1544
determining large price changes. Fluctuation and Noise Letters 5, L209–
1545
L216.
1546
Lillo, F., Farmer, J.D., Mantegna, R.N., 2003. Master curve for price-impact
1547
function. Nature 421, 129–130.
1548
Nevmyvaka, Y., Feng, Y., Kearns, M., 2006. Reinforcement learning for opti-
1549
mized trade execution, in: Proceedings of the 23rd international conference
1550
on Machine learning, pp. 673–680.
1551
Potters, M., Bouchaud, J.P., 2003. More statistical properties of order books
1552
and price impact. Physica A: Statistical Mechanics and its Applications
1553
324, 133–140.
1554
53
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 55

Shavandi, A., Khedmati, M., 2022. A multi-agent deep reinforcement learn-
1555
ing framework for algorithmic trading in financial markets. Expert Systems
1556
with Applications 208, 118124.
1557
Shen, D., 2015. Order imbalance based strategy in high frequency trading.
1558
Ph.D. thesis. oxford university.
1559
Sirignano, J., Cont, R., 2019. Universal features of price formation in finan-
1560
cial markets: perspectives from deep learning. Quantitative Finance 19,
1561
1449–1459.
1562
Sirignano, J.A., 2019. Deep learning for limit order books. Quantitative
1563
Finance 19, 549–570.
1564
Smith, E., Farmer, J.D., Gillemot, L., Krishnamurthy, S., 2003. Statistical
1565
theory of the continuous double auction. Quantitative finance 3, 481.
1566
Tsantekidis, A., Passalis, N., Tefas, A., Kanniainen, J., Gabbouj, M., Iosi-
1567
fidis, A., 2017. Forecasting stock prices from the limit order book using
1568
convolutional neural networks, in: 2017 IEEE 19th conference on business
1569
informatics (CBI), IEEE. pp. 7–12.
1570
Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N.,
1571
Kaiser,  L., Polosukhin, I., 2017. Attention is all you need. Advances in
1572
neural information processing systems 30.
1573
Yin, J., Wong, H.Y., 2023. Deep lob trading: Half a second please! Expert
1574
Systems with Applications 213, 118899.
1575
Yura, Y., Takayasu, H., Sornette, D., Takayasu, M., 2014. Financial brow-
1576
nian particle in the layered order-book fluid and fluctuation-dissipation
1577
relations. Physical review letters 112, 098703.
1578
Yura, Y., Takayasu, H., Sornette, D., Takayasu, M., 2015. Financial knudsen
1579
number: Breakdown of continuous price dynamics and asymmetric buy-
1580
and-sell structures confirmed by high-precision order-book information.
1581
Physical Review E 92, 042811.
1582
Zhang, Z., Zohren, S., Roberts, S., 2019. Deeplob: Deep convolutional neural
1583
networks for limit order books. IEEE Transactions on Signal Processing
1584
67, 3001–3012.
1585
54
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


## Page 56

Zovko, I., Farmer, J.D., 2001. The power of patience: A behavioral regularity
1586
in limit order placement. Quantitative Finance , 1–6.
1587
55
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5614902
Preprint not peer reviewed


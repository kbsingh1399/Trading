# (Re-)Imag(in)ing LOB in Jiangsu Province Electricity Market

- **Source File**: `ssrn-6189791.pdf`
- **Total Pages**: 17
- **SSRN ID**: `ssrn-6189791`

---

## Page 1

Title: 
(Re-)Imag(in)ing LOB in Jiangsu Province Electricity Market
Abstract:
The scholars argue image of price trend (open-high-low-close) is useful for daily-
level return prediction. In market microeconomic structure, both academic and 
industry hold consensus that limit order book (LOB) has strong impact on second-
level return prediction, but no one provides a theoretical and practical framework to 
use its information. We firstly transform the LOB data into pixel graphics and further 
use CNN technique to predict the trend of future return, as opposed to traditional 
variables extracted from LOB like order imbalance. We rely on second-level LOB 
charts from electricity market to perform whole analysis. Such LOB-chart based 
forecasting differs significantly from traditional trend strategies, yields more accurate 
return predictions, and enables more profitable investment strategies.
Authors: 
Jingtao Xua, Mei Zhonga*
Jingtao Xu Email: virgil123mry@gmail.com
Mei Zhong Email: zhongm@swfu.edu.cn
Affiliation:
a College of Economics and Management, Southwest Forestry University,
No. 300 Bailong Temple, Panlong District, Kunming 650224, Yunnan, China
*Corresponding Author:
Mei Zhong
Email: zhongm@swfu.edu.cn
CRediT authorship contribution statement:
Jingtao Xu: Conceptualization, Methodology, Formal analysis, Data curation, Writing 
– original draft, Writing – review & editing.
Mei Zhong: Supervision, Writing – review & editing.
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


## Page 2

Declaration of competing interest:
The authors declare that they have no known competing financial interests or personal 
relationships that could have appeared to influence the work reported in this paper.
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


## Page 3

(Re-)Imag(in)ing LOB in Jiangsu Province Electricity Market
A R T I C L E I N F O
Keywords:
Limit order books
Machine learning
Forecasting
A B S T R A C T
The scholars argue image of price trend (open-high-low-close) is useful for daily-level return
prediction. In market microeconomic structure, both academic and industry hold consensus that
limit order book (LOB) has strong impact on second-level return prediction, but no one provides
a theoretical and practical framework to use its information. We firstly transform the LOB data
into pixel graphics and further use CNN technique to predict the trend of future return, as opposed
to traditional variables extracted from LOB like order imbalance. We rely on second-level LOB
charts from electricity market to perform whole analysis. Such LOB-chart based forecasting
differs significantly from traditional trend strategies, yields more accurate return predictions,
and enables more profitable investment strategies.
1. Introduction
Since the 1990s, financial markets have experienced a fundamental transformation in their trading mechanisms.
Earlier decades were dominated by floor-based open outcry systems and later by quote-driven structures, both of which
have now largely been replaced by electronic, order-driven limit order books (LOBs). This evolution reflects the broader
shift in market microstructure toward greater transparency, efficiency, and automation. The LOB functions through
two fundamental types of orders: limit orders and market orders (Hollifield, Miller and Sandås, 2004). A limit order
represents a trader’s commitment, at a given moment, to buy or sell a specific quantity of a security at a predetermined
price. By contrast, a market order is executed instantly at the most favorable price available. Limit orders that remain
unfilled are retained in the book until they are either executed or withdrawn. Within this microstructure, liquidity is
provided by limit orders, while market orders serve to consume that liquidity (Bloomfield, O’hara and Saar, 2005).
LOBs have become central to modern financial markets owing to their distinct advantages. They reduce trading
costs by narrowing spreads and lowering fees, while their electronic design allows remote access to a wide pool of
participants. By providing both pre-trade and post-trade transparency, LOBs enhance information flow and support
efficient price discovery through the aggregation of diverse trading signals. Moreover, they reduce information
asymmetry and foster competition, thereby strengthening overall market quality and efficiency.
Recently, financial markets have experienced profound technological transformations, marked by the rapid rise
of algorithmic and data-driven trading. Alongside these developments, the growing availability of high-frequency
and high-dimensional market data, coupled with advances in computational power, has created fertile ground for the
application of deep learning models (Chen, Chen, Huang, Huang and Chen, 2016; Hu, Hu, Yang, Yu, Sung, Zhang, Xie,
Liu, Robertson and Hospedales, 2018; Tsantekidis, Passalis, Tefas, Kanniainen, Gabbouj and Iosifidis, 2017; Chen,
Pelger and Zhu, 2024).
Despite the considerable progress in high-frequency trading research and deep learning applications, existing
literature remains heavily concentrated on liquid financial assets such as equities or foreign exchange, where depth,
liquidity, and trading frequency naturally suit data-driven modeling (Harris, 2013; Carrion, 2013). By contrast, elec-
tricity markets, particularly the hybrid intra-month trading mechanism employed in China have received comparatively
little scholarly attention. While a few studies leverage LOB information for volatility forecasting or jump prediction
(Mäkinen, Kanniainen, Gabbouj and Iosifidis, 2019), they are typically limited to static or low-frequency data, thus
failing to capture the subtle, second-level dynamics inherent to electricity markets.
Moreover, although deep learning models such as Convolutional Neural Networks (CNNs) have demonstrated
success in stock return prediction using image-transformed price data, these applications are largely limited to
benchmark financial markets with regular trading hours, dense order flows, and minimal exogenous intervention. In
the case of electricity, however, the non-storability of the asset, sparse order books, and administrative price controls
introduce market frictions and information asymmetries that render traditional financial models inadequate. Few, if
∗Corresponding author
( ); ( )
ORCID(s):
: Preprint submitted to Elsevier
Page 1 of 15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


## Page 4

any, studies rigorously examine whether deep learning can extract actionable signals from such structurally illiquid,
policy-constrained environments.
Lastly, while sentiment-augmented and order-imbalance-based strategies have been explored (Biais, Foucault and
Moinas, 2015; Zhang, Zhang, Wang, Yao, Fang and Yu, 2018), these approaches often neglect the microstructural
complexities unique to electricity LOBs, such as non-persistent depth, fragmented trading interest, and volatile demand
shocks. This absence points to an urgent methodological and empirical gap: a need to develop specialized, high-
resolution prediction frameworks tailored to the distinctive attributes of electricity trading.
Our empirical analysis focuses on short-term return prediction in the Jiangsu Province electricity market from
February to May 2025. We train a CNN to classify the direction (up or down) of future short-term returns. Specifically,
we estimate a single CNN model with a fixed architecture and shared parameters across all training samples, which
generates directional forecasts based on LOB images. The input images are constructed from the top five bid and ask
prices levels, together with their corresponding volumes, over a fixed 5-second historical window. Based on these
images, the model is trained to predict the directional movement of the mid-price at multiple forecast horizons (5, 10,
15, 30 and 60 seconds).
This study contributes to the literature in several important respects. First, while existing studies acknowledge
the predictive relevance of the LOB for high-frequency price dynamics, no prior work has proposed a systematic
framework that applies CNNs to exploit LOB information for second-level return prediction. Second, rather than
relying on traditional handcrafted features, such as order imbalance or aggregated liquidity measures, we introduce
a novel image-based representation of the LOB, which allows CNNs to directly capture the geometric and relational
patterns embedded in order flow. Third, our empirical results demonstrate that this approach delivers superior predictive
accuracy and enhanced trading profitability relative to conventional strategies, underscoring the methodological and
practical advantages of treating the LOB as a visual structure rather than a set of pre-defined variables.
Our main empirical finding is that image-based CNN predictions provide powerful forecasts of second-level
returns, generating economically meaningful trading profits in a high-frequency market setting. The model exhibits its
strongest performance at short horizons, particularly around 10 seconds, where it achieves both high profitability and
favorable risk-adjusted outcomes. More broadly, across horizons of 5 to 30 seconds, CNN-based strategies consistently
outperform classical technical rules, underscoring their ability to exploit transient and non-linear patterns in limit
order book dynamics. To evaluate the economic value of our model, we simulate trading based on predicted class
probabilities and benchmark the CNN’s performance against three widely used rule-based strategies: momentum,
reversal, and trend-following. Of these, momentum strategies remain largely ineffective at short horizons, reversal
strategies display intermittent but inconsistent success, and trend-following strategies perform poorly across nearly
all settings. Robustness tests further confirm that the CNN model retains strong predictive power in volatile periods,
though its advantage diminishes at longer horizons. This pattern supports the view that the model captures genuine
patterns in LOB dynamics rather than overfitting to past noise. Taken together, these findings underscore the potential of
deep learning methods to extract high-frequency trading signals from market images, offering a powerful complement
to conventional rule-based approaches in short-term prediction and execution.
The remainder of the paper is organized as follows. Section 2 reviews the prior literature on high-frequency trading,
limit order book and price discovery, and CNNs. Section 3 presents the intuition and detailed mechanics of our CNN
framework. We describe the process of converting LOB data into images in Section 4. In Section 5, we report our main
empirical analysis. Section 6, we report robustness tests of our main empirical analysis. Section 7 concludes.
2. Literature Review
2.1. High-frequency Trading
High-frequency trading (HFT) influences financial markets in many ways. For example, HFT reduces the bid-ask
spread (Harris, 2013), increases price efficiency (Carrion, 2013) and displayed depth in the LOB, and decreases short-
term volatility (Hasbrouck and Saar, 2013). In general, HFT plays a dominant part in providing liquidity (Hagströmer
and Nordén, 2013; Conrad, Wahal and Xiang, 2015), but probably also withdraw this liquidity during a period of large
and temporary selling pressure (Kirilenko, Kyle, Samadi and Tuzun, 2017; Korajczyk and Murphy, 2019). Meanwhile,
other papers show that HFT can predict future order flow from other traders and future price movements (Biais et al.,
2015; Hoffmann, 2014; Foucault, Hombert and Roşu, 2016; Hirschey, 2021).
HFT does not represent a single trading style but rather a method characterized by extremely short holding periods,
rapid order submission, and algorithmic execution. Within this method, HFT strategies are commonly divided into
: Preprint submitted to Elsevier
Page 2 of 15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


## Page 5

two broad categories: market-making HFTs, which continuously post limit orders to capture the bid-ask spread while
managing inventory risk, and directional HFTs, which seek to forecast short-term price movements and typically rely on
aggressive orders. In the case of directional HFTs, order placement strategies based on order book imbalances have been
shown to be particularly effective in volatile markets (Brogaard, Hendershott and Riordan, 2019). Aggressive orders
in this context exhibit several important properties. First, they are strongly predictive of very short-term price changes
and contribute substantially to overall trading volume, accounting for 25%-42% depending on market capitalization
(Brogaard, Hendershott and Riordan, 2014). Second, they are closely linked to information flows, responding to market-
wide returns, quote updates, macroeconomic announcements, E-mini price changes, and even real-time newswire
items (Hirschey, 2021; Kelley and Tetlock, 2013). These findings suggest that directional HFTs frequently trade in
anticipation of upcoming information releases.
Aggressive orders, however, come with a significant premium for immediacy. While passive orders tend to have
a negative price impact, aggressive orders display strong persistence once executed (Griffiths, Smith, Turnbull and
White, 2000). They are usually submitted when spreads and depths are relatively low, and their impact induces a
persistent widening of bid-ask spreads and changes in depth. Although market conditions gradually revert, this process
may take up to 20 best limit updates following the initial shock (Degryse, Jong and Ravenswaaij, 2005).
Beyond order-level dynamics, a growing body of research emphasizes the role of human behavior and sentiment
in shaping price movements (Barberis, 2018). For example, Zhang et al. (2018) propose a predictive model integrating
events, sentiment indicators, and quantitative features extracted from diverse sources such as news articles, social
media and market data feeds. Earlier studies, however, suggest that while aggregate sentiment measures exhibit strong
contemporaneous linkages with market returns, they provide little evidence of short-term predictive power (Brown and
Cliff, 2004). This contrast highlights the need for more refined sentiment measures and advanced modeling techniques.
Nowadays, the question is no longer whether investor sentiment affects stock prices, but how to measure investor
sentiment and quantify its effects. Baker and Wurgler (2007) take the origin of investor sentiment as exogenous and
instead focus on its empirical effects.
2.2. Limit Order Book and Price Discovery
Academic evidence suggests that the importance of market design and trading protocols in the determination of
agents’ decisions to provide liquidity such as price efficiency, volatility, and trading costs (Madhavan, 2000). For
example, Large (2009) finds that a LOB induces in expectation equal numbers of market orders and uncanceled limit
orders over time in a minimal stationarity property of microstructure dynamics.
The important parameters indicating the shape of order book include the depth, height, slope, resilience and order
imbalance (Cao, Hansch and Wang, 2009; Næs and Skjeltorp, 2006). The current state of a LOB substantially affects
the price formation and short-term price volatility (Ahn, Bae and Chan, 2001; Pascual and Veredas, 2010). For instance,
a greater depth around the best quotes reflects a consensus on the true price (Goettler, Parlour and Rajan, 2005). In
contrast, a high preponderance of limit orders away from the best quotes. This mispricing may lead to increasing
short-term price volatility and may improve the execution probability of limit orders. Therefore, the shape of order
book has significant implications for market efficiency. The resilience of the order book to order flow shocks is one of
the important criteria to measure market efficiency, which remains less explored (Degryse et al., 2005; Large, 2007).
We infer that this is because the computation of this measure is data intensive and requires intraday high-frequency
order book (e.g., order book snapshots at 1-second, 5-second frequencies).
LOB is a channel for volatility information (Foucault, Moinas and Theissen, 2007). The use of LOB data is found
to improve the performance of the proposed model in jump prediction (Mäkinen et al., 2019). Sandås (2001) find that
break-even conditions for marginal orders in the LOB define the slope of the price schedule offered at a given point
in time. After trading halts, A large proportion of the LOB at the reopen is composed of orders submitted during the
halt, and that the market-clearing price at the reopen is a good predictor of future prices (Corwin and Lipson, 2000).
Informed traders use limit orders when volatility is low (Goettler, Parlour and Rajan, 2009) and realized signals are
close to their expected value.
2.3. CNNs
Financial data has to be taken into machine learning methods in asset pricing because of its time dimension (Chen
et al., 2024). Gu, Kelly and Xiu (2020) also demonstrate the potential of machine learning in finance through empirical
analysis of asset pricing. Deep neural networks (DNNs), especially CNNs, can learn or extract technical indicators
(e.g., Bollinger bands, MACD). As a method to predict price movements of financial markets, technical indicators and
: Preprint submitted to Elsevier
Page 3 of 15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


## Page 6

technical analysis has been extensively used by market practitioners. Although the theoretical sensibility and empirical
reliability of technical analysis have long been a subject of debate, some studies provide evidence of its forecast
ability (Lo and MacKinlay, 1988; Timmermann and Granger, 2004). Some scholars combine textual information with
historical market data for stock prediction, showing that such approaches outperform models relying on a single input
type. For instance, Vargas, De Lima and Vargas, De Lima and Evsukoff (2017) employ a deep learning framework that
combines financial news with technical indicators to predict intraday movements of the Standard & Poor’s 500 index,
while Akita, Yoshihara, Matsubara and Uehara (2016) use recurrent neural networks to integrate news headlines with
numerical stock data. An emerging literature in the field of computer vision about image recognition, which using
price plots and CNN-based models to forecast stock returns. Existing studies typically offer methodological overviews
accompanied by limited-scale empirical validations. For example, Chen et al. (2016) use not only CNNs but also data
visualization methods, for the purpose of transforming stock price data into image data to eliminate noise. Hu et al.
(2018) use price plot CNNs to cluster individual stocks.
The standard way of approaching LOB modeling has primarily utilized parametric models to concisely capture
order book dynamics or simulation-based flexible agent models (Large, 2009; Goettler et al., 2005). More recently,
the econometric techniques from other areas (e.g., computer science and information technology) have been adopted
to model LOB (Cont, Stoikov and Talreja, 2010; Toth, Palit, Lillo and Farmer, 2015). For example, machine learning
models are widely acknowledged to improve the forecast ability in LOB modeling. Tsantekidis et al. (2017) train a
CNN on high frequency LOB data and compare with other methods (e.g., multilayer neural networks and support
vector machines), showing that CNNs are better than suited for stock price movements.
3. The CNN Model
This section outlines the CNN model architecture and training process, and discusses the rationale for using image-
based representations of time-series market data instead of conventional time-series models.
3.1. A Brief Description of the CNN Architecture
To capture intricate spatial patterns embedded in the LOB dynamics, our model adopts a convolutional neural
networks (CNN) architecture trained on image-based representations of historical market snapshots. Each image is
a pixel graphic derived from LOB features over a lookback window of five consecutive observations, with pixel
intensities normalized to the [0, 1] range. While it is theoretically possible to flatten these images and pass them
into a conventional feed-forward neural network, such an approach would be both computationally inefficient and
structurally myopic. Fully connected architectures, lacking spatial inductive biases, are highly sensitive to variations in
position and scale, and typically suffer from overfitting due to their immense parameter count, particularly problematic
in data-limited financial contexts.
CNNs overcome these limitations through localized receptive fields, shared weights, and hierarchical abstraction,
enabling efficient learning even with modest datasets. Furthermore, their inherent translation invariance allows them
to generalize well to subtle structural shifts in the LOB visual patterns.
The architecture of CNN model is shown in Fig. 1. Our proposed CNN architecture consists of two convolutional
blocks, each comprising a 2D convolutional layer (with 32 and 64 filters, respectively), batch normalization, ReLU
nonlinearity, and a 2 × 2 max-pooling operation. These blocks progressively extract increasingly abstract and robust
local features from the LOB images, while simultaneously reducing spatial resolution to mitigate overfitting. The output
of the final convolutional block is flattened and passed through a fully connected network with 64 hidden units, followed
by dropout regularization and a final linear layer producing two logits. During inference, a softmax transformation is
applied to these logits to yield class probabilities corresponding to the binary classification task—whether the mid-price
will rise or fall over a specified forecast horizon. The probability assigned to class 1 reflects the model’s confidence in
an upward price movement.
3.2. A Brief Description of the CNN Architecture
Our modeling framework begins by transforming the raw limit order book (LOB) time-series data into structured
pixel graphics, effectively re-encoding the multidimensional temporal and depth-wise market information into a two-
dimensional matrix format. This transformation enables CNNs to leverage their spatial inductive biases, particularly
suited to capturing localized, nonlinear dependencies across both price levels and time steps. These nuances are
frequently obscured in traditional time-series models.
: Preprint submitted to Elsevier
Page 4 of 15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


## Page 7

Figure 1: Diagram of the CNN model
By juxtaposing temporal evolution and market depth within a unified image representation, the CNN can
discern subtle structural signatures indicative of underlying market regimes. For example, the model becomes
capable of distinguishing between stable liquidity configurations, transitory depth distortions, and pronounced bid-ask
imbalances. Unlike 1D convolutional approaches that operate over flattened sequences and are limited to capturing
sequential dependencies, 2D convolutional filters (e.g., 3 × 3 kernels) operate over localized spatial patches, allowing
the model to detect intricate joint patterns that span both axes such as diagonal spreads of depth shifts or vertically
stacked liquidity voids.
Each image encodes multiple key dimensions of the LOB state, including the mid-price, the top five levels of bid
and ask quotes, and their corresponding order volumes. These elements are embedded as pixel intensities, forming
a visual surface where spatial configurations implicitly reflect directional price pressure, instantaneous liquidity, and
market microstructure dynamics. In classical econometric frameworks, modeling such effects would typically require
extensive manual feature engineering such as extracting volume-weighted average price (VWAP), order imbalance
ratios, or engaging nonlinear modeling paradigms like GARCH or stochastic volatility models. Our approach bypasses
these manual steps entirely: through end-to-end training on raw image inputs, the CNN autonomously learns which
features are most predictive of short-term price trends.
Fundamentally, encoding LOB states as images allows the model to tap into the same visual pattern-recognition
capabilities that underpin much of modern computer vision. Just as a human observer can more readily detect patterns
from a heatmap than from a raw numeric table, a CNN can exploit this structured visual representation to discover
predictive motifs, which are otherwise difficult to express analytically. This image-based paradigm thus serves not
only as a dimensionality-reduction mechanism but as a domain-aware encoding scheme that aligns with the CNN’s
architectural strengths.
: Preprint submitted to Elsevier
Page 5 of 15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


## Page 8

3.3. Training the CNN
Our workflow for model training, validation, and evaluation follows a time-ordered, out-of-sample design.
Specifically, we design three sequential training configurations using high-frequency electricity market data from
Jiangsu Province, spanning February to May 2025.
In the first configuration, data from February serves as the in-sample set. This dataset is randomly partitioned into
training (70%) and validation (30%) subsets. The trained model is then evaluated on March data, representing a genuine
out-of-sample environment. The second configuration expands the in-sample window to include both February and
March. A stratified 70/30 split is again applied to this combined dataset, and performance is assessed on unseen April
data. The third configuration extends this design further: data from February through April is used for model fitting
and validation, with May data held out entirely as the final test set. This progressive expansion mirrors a real-world
deployment setting, where the model is updated as more historical data becomes available.
We formulate return direction prediction as a classification task. Labels are generated by comparing the mid-price
at the current time with the mid-price after a fixed forecast horizon, which we set to one of 5, 10, 15, 30, or 60 seconds
depending on the experimental configuration. If the mid-price at the future timestamp exceeds its current value, the
label is assigned as 𝑦= 1 (indicating an upward movement); otherwise, the sample is labeled as 𝑦= 0. While this
binary labeling implicitly includes the "no-change" cases in the negative class, we explicitly address the issue of class
imbalance by downsampling the unchanged instances. Specifically, we randomly retain a number of unchanged samples
equal to 20% of the total count of directional samples (ups and downs combined), ensuring that the resulting training
set is both informative and balanced.
Following this preprocessing, the labeled image samples are divided into training and validation sets using stratified
sampling. This methodology reduces bias from prevailing market regimes (e.g., prolonged bullish or bearish trends)
and enhances the robustness of the classifier under varying market conditions.
The CNN produces a two-dimensional output vector 𝑧= [𝑧0, 𝑧1], referred to as logits, which correspond to the
model’s unnormalized confidence scores for the two classes. Model training minimizes the standard cross-entropy loss
function:
𝐿(𝑦, 𝑧) = −log
(
exp(𝑧𝑦)
∑1
𝑖=0 exp(𝑧𝑖)
)
(1)
Here, 𝑦∈{0, 1} is the ground truth label, and the softmax operation is applied internally to transform logits into
valid class probabilities. This objective encourages the model to allocate high confidence to the correct class while
penalizing erroneous predictions proportionally.
We optimize this loss using the Adam optimizer, with an initial learning rate of 1 × 10−5, a batch size of 128, and
an 𝐿2 weight decay of 1 × 10−4 (Srivastava, Hinton, Krizhevsky, Sutskever and Salakhutdinov, 2014). To prevent
overfitting and promote generalization, we implement an early stopping mechanism: training is halted when the
validation loss fails to improve for two consecutive epochs.
In the fully connected layers, we apply dropout with a probability of 0.5 to mitigate the co-adaptation of neurons
and encourage the learning of robust features. 𝐿2 regularization further constrains model complexity by penalizing
excessively large weight magnitudes.
The convolutional backbone of the network incorporates ReLU activations, batch normalization, and 2 × 2 max-
pooling operations. These elements jointly introduce nonlinearity, promote numerical stability during training, and
impart spatial invariance to the learned features. Importantly, dropout is not applied within the convolutional layers to
preserve the spatial integrity of local feature representations. This architectural design, combined with early stopping
and regularization, ensures stable, efficient, and generalizable training performance across diverse market conditions.
4. LOB Data
In this section, we outline the process used to transform historical electricity market data into image-based inputs
for the CNN forecasting model. The dataset employed in this study was obtained from trading information by the
Jiangsu Power Exchange Center. Specifically, the data were collected through a custom-developed Python web crawler
from the Jiangsu Power Exchange Center, encompassing per-second market transaction volumes, prices, and related
information.
In Jiangsu Province of China, at each month, Government will open the electricity exchange for several days. At
each electricity trading day, the trading hour is fixed between 10:00 am and 11:00 am. So, based on 1-second frequency
: Preprint submitted to Elsevier
Page 6 of 15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


## Page 9

Figure 2: BTC/USDT Limit Order Book and Market Depth Chart from Binance
observation, we generally will have about 3600 second-level LOB and transaction result. Our dataset covers all trading
days from February to May 2025, amounting to 49 trading days in total, and includes approximately 160,000 second-
level LOB and transaction result. Each snapshot captures the full state of the LOB at that second, including prices,
volumes, and executed trades, providing a rich basis for modeling market microstructure dynamics and predicting
short-term returns.
Fig. 2 illustrates a 1-second snapshot of the Bitcoin (BTC/USDT) depth chart as displayed on a cryptocurrency
trading platform. The right panel displays a market depth chart, where the green and red areas respectively represent
cumulative buy-side and sell-side liquidity. This visual representation provides insight into short-term market sentiment
and order flow, serving as the basis for constructing LOB images used in our model.
Fig. 3 illustrates a black-and-white visual representation of the LOB over a rolling five-second window. Each image
is constructed on a fixed canvas of 125 pixels in height and 52 pixels in width. The horizontal axis encodes price levels:
the left half is reserved for the top five bid prices, the right half for the top five ask prices, while the vertical line is
dynamically positioned between the best bid and the best ask. The vertical axis, in turn, translates the cumulative
order volumes into pixel coordinates through a logarithmic transformation and normalization, ensuring that both small
and large volumes can be visualized within the same frame. The temporal dimension unfolds from bottom to top: the
lowest 25-pixel band corresponds to the first second within the window, while each subsequent band above represents
the next second, culminating in the most recent snapshot at the top. Within each band, the bid and ask prices are mapped
horizontally according to their relative distance from the mid-price, while the corresponding cumulative volumes are
plotted vertically. These coordinates are then connected in a step-line fashion, producing ladder-like curves for both
bids and asks. Finally, a vertical line is drawn at the mid-price for each second, visually anchoring the bid-ask dynamics
around the evolving price center. In this way, the sequence of images provides an intuitive yet rigorous visualization
of order book fluctuations.
This design intricately emphasizes the structural aspects of the order book over time, showcasing the distribution of
liquidity across varying price levels and highlighting the symmetry between the buy and sell sides. The visualization
captures the dynamic movement of the order book, making it possible to discern subtle trends and patterns in the
market depth as it evolves.
: Preprint submitted to Elsevier
Page 7 of 15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


## Page 10

Figure 3: Generated 5-second LOB Image
The decision to focus on the top 5 bid-ask prices and their corresponding volumes, in conjunction with the mid-
price, is firmly rooted in both practical considerations and the foundational principles of market microstructure theory.
From a market microstructure standpoint, the top levels of the limit order book (typically the first 5 – 10 levels) represent
the most immediately executable liquidity, encapsulating the most up-to-date supply and demand conditions. Empirical
research (Conrad et al., 2015; Hautsch and Huang, 2012) consistently demonstrates that price movements in high-
frequency trading environments are frequently initiated by shifts in these near-best quotes, as they directly mirror the
trading intentions of the market’s most active participants.
By limiting the model’s input to the top 5 levels, we strike an optimal balance between information richness and
computational efficiency. Including an excessive number of levels could introduce noise, as the deeper layers of the
book tend to become stale, offering less relevant data for short-term predictions. On the other hand, focusing on too
few levels risks overlooking critical liquidity shifts and failing to capture the imbalances just beyond the best bid and
ask.
Moreover, we incorporate the average of the best bid and best ask prices, which serves as a robust, widely accepted
proxy for the true market price. Including this mid-price in each snapshot ensures that the model can effectively
normalize price movements, fostering consistency across varying volatility regimes. This compact, yet rich visual
representation empowers the CNN to discern both spatial and temporal regularities in the LOB, thereby enhancing the
model’s ability to forecast short-term returns with greater accuracy.
5. Empirical Result
In this study, we adopt a single input design that encodes LOB data from the past 5 seconds into images. Each
image is labeled with a "1" if the mid-price increases over a specified forecast horizon (5, 10, 15, 30, or 60 seconds),
and "0" otherwise. For each distinct forecast horizon, we independently train the CNN model five times to account for
the inherent stochasticity in the optimization process, such as weight initialization and data shuffling. The resulting
predictions are then averaged to enhance stability, following the methodology outlined by Gu et al. (2020).
To optimize computational efficiency, we refrain from utilizing a rolling retraining approach. Instead, each model is
trained and validated once using in-sample data from February to April 2025. For model training, 70% of the samples
are randomly selected, while the remaining 30% are reserved for validation. Once trained, the model is employed to
generate predictions on out-of-sample data from May 2025.
5.1. Short-horizon Model Performance
To assess the overall performance of the proposed model, we report both in-sample and out-of-sample (OOS)
McFadden 𝑅2, which is suitable only for regression tasks involving continuous outcomes, McFadden 𝑅2 provides a
more appropriate measure of goodness-of-fit for classification models such as logistic regression and neural networks.
The implementation follows three steps. First, we calculate the log-likelihood of the estimated model (𝐿𝐿model) by
: Preprint submitted to Elsevier
Page 8 of 15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


## Page 11

applying the softmax output to the true class labels. For each observation, the predicted probability of its actual class is
extracted, the logarithm is taken, and the results are summed across all samples. Second, we compute the log-likelihood
of the null model (𝐿𝐿model), which assumes equal probability for each class. In the binary setting, this reduces to
𝐿𝐿null = 𝑁⋅ln(0.5), where 𝑁denotes the number of samples. Finally, McFadden 𝑅2 is obtained as:
𝑅2
McFadden = 1 −𝐿𝐿model
𝐿𝐿null
(2)
Table 1 summarizes the model’s predictive performance across five forecast horizons using LOB image inputs and
illustrates how the effectiveness of short-horizon return direction prediction varies as the prediction window lengthens.
In addition, the table includes out-of-sample classification accuracy on May data, offering an evaluation of the model’s
generalization ability to unseen market conditions.
Table 1
Model performance across different prediction horizons
Horizon
5s
10s
15s
30s
60s
Training set McFadden 𝑅2
0.24
0.39
0.48
0.59
0.70
Validation set McFadden 𝑅2
0.12
0.29
0.38
0.52
0.65
Test set McFadden 𝑅2
0.16
0.15
0.22
0.12
0.02
OOS accuracy
0.71
0.69
0.72
0.69
0.71
A clear upward trend is observed in the training set’s McFadden 𝑅2, rising steadily from 0.2377 at the 5-second
horizon to 0.7048 at 60 seconds. This progression indicates that the model captures increasingly rich predictive
structure as the forecast horizon extends. Intuitively, shorter-term price movements are often more erratic and driven
by noise, rendering them harder to predict. In contrast, longer horizons tend to reveal more pronounced patterns, such
as autocorrelation and trend persistence, which the model is able to learn more effectively.
On the validation set, a similar improvement is observed: McFadden 𝑅2 increases from 0.1225 to 0.6453 as the
horizon lengthens. This consistent performance across unseen in-sample data suggests strong generalization capacity.
Furthermore, the narrowing gap between training and validation 𝑅2 at extended horizons implies reduced overfitting
and greater model robustness in those settings. However, the test set (out-of-sample) McFadden 𝑅2 follows a different
trajectory. It peaks at the 15-second horizon with a value of 0.2191 but declines sharply thereafter, reaching just
0.022 at 60 seconds. This reversal suggests either overfitting to in-sample patterns that do not persist into the OOS
period, or a shift in the underlying price dynamics during May, which undermines the model’s predictive accuracy.
Such non-monotonic behavior underscores the fundamental challenge of temporal non-stationarity in high-frequency
financial markets—patterns that hold over one time span may degrade or vanish in another, especially as longer horizons
introduce additional layers of macroeconomic or structural noise.
Despite this decline in 𝑅2 on the test set, the out-of-sample classification accuracy remains relatively stable across
horizons, fluctuating within a narrow range from 0.6924 to 0.7173. This stability suggests that, although the model’s
confidence in its predictions may weaken, the classification boundary it learns remains reasonably robust for directional
inference across varying timeframes.
Table 2 presents the normalized out-of-sample (OOS) confusion matrix for the CNN model’s directional forecasts
across multiple short-term return horizons. Each cell of the matrix represents the proportion of test set samples that
fall into one of four prediction-outcome categories: True Positive (TP), False Negative (FN), False Positive (FP), and
True Negative (TN). This matrix serves not only to evaluate the overall classification accuracy but also to assess the
model’s directional bias. Specifically, it helps identify whether the model exhibits a tendency to overpredict upward
trends or, conversely, demonstrates a more conservative approach in predicting downturns.
A clear and striking pattern emerges in the matrix: there is a strong asymmetry between "True Up" and "True Down"
samples. Across all horizons, the proportion of "True Down" cases (i.e., mid-price decreases after the prediction point)
dominates the test set. For example, "True Down" cases account for 96.6% of all samples at the 5-second horizon.
Even at the 60-second horizon, upward trends account for less than 17% of the total test set. This imbalance reflects the
inherent dynamics of high-frequency market microstructure, where price movements are typically small, short-lived,
and more frequently downward due to factors such as bid-ask bounce, short-term liquidity pressures, or quote revisions
: Preprint submitted to Elsevier
Page 9 of 15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


## Page 12

Table 2
OOS Win Rate Confusion Matrix
Horizon
TP
FN
FP
TN
5s
0.01357
0.02028
0.26215
0.70399
10s
0.02193
0.03070
0.27868
0.66869
15s
0.02728
0.04161
0.23266
0.69845
30s
0.04424
0.06538
0.23813
0.65226
60s
0.04391
0.12413
0.16174
0.67023
(Foucault, Kadan and Kandel, 2005). This inherent skew presents a challenge for classifiers: if the model were to predict
only the majority class, its accuracy would artificially increase.
The OOS confusion matrix also reveals a consistent directional bias in the model’s predictions, particularly a
conservative tendency to favor downward forecasts across all return horizons. This is evident in the high proportions
of "True Down – Forecast Down" cases, such as 70.4% at 5 seconds and 67.0% at 60 seconds, paired with relatively low
TP rates for upward movements, which stand at only 1.36% at 5 seconds. From a calibration standpoint, this pattern
suggests that the model is more confident in predicting trend continuation or short-term reversals toward the downside,
and it is less likely to assign high probabilities to upward trends unless there are strong distinguishing features. This
asymmetry may arise from the label imbalance in the training set, as well as the limited visual variation among upward
patterns in the LOB image data, which hampers the model’s ability to generalize upward signals effectively.
As the prediction horizon increases, the model’s predictive confidence shows signs of degradation. This is likely
due to the increasing noise in future returns and the non-stationary nature of high-frequency market microstructure,
both of which reduce the correlation between current order book features and future price movements. Empirically,
this is reflected in a rising FN rate, which increases from 2.0% at 5 seconds to 12.4% at 60 seconds. In contrast, the
FP rate decreases over the same horizon range, indicating growing conservatism and possibly reflecting lower softmax
confidence thresholds as the horizon extends.
Overall, the CNN-based model exhibits consistent performance in forecasting short-term return directions,
particularly within the 5 to 15-second window. McFadden 𝑅2 values demonstrate a robust in-sample fit and a moderate
degree of generalization. Simultaneously, the out-of-sample classification accuracy remains stable across the various
horizons, while the confusion matrix analysis highlights a directional conservatism that mirrors the class imbalance
inherent in the LOB data.
To ascertain whether these results are consistent across different periods and not limited to the May dataset, we
conduct a series of robustness tests utilizing alternative OOS periods. The additional findings from these tests are
presented in Section 6.
5.2. Trading
We implement trading strategies by converting both model forecasts and benchmark signals into discrete positions
through a rolling quantile procedure. For each valid decision point, the CNN model produces an upward probability,
which is mapped into a long or short signal (+1∕−1) if the value lies in the upper or lower quantile of its rolling
distribution. Analogous rules are applied to the momentum, short-term reversal, and trend-following indicators derived
from mid-price dynamics. Importantly, all strategies are executed on the same set of decision points, ensuring that
performance differences are attributable to the forecasting methods rather than timing advantages.
For each trade initiated at time 𝑡, the realized return is defined as
𝑟𝑡= investment × 𝑃𝑡+𝐻−𝑃𝑡
𝑃𝑡
.
(3)
where the investment takes values of ±1. Here, 𝑃𝑡denotes the mid-price at time 𝑡and 𝑃𝑡+𝐻the mid-price after horizon
𝐻. Daily returns are then aggregated to compute annualized performance statistics, including return, volatility, Sharpe
ratio and the total number of trades.
Table 3 presents the results of applying the CNN-based trend prediction model to out-of-sample data across various
short-term return horizons. At very short horizons (5s, 10s, and 15s), the strategy achieves strong and economically
meaningful results. For instance, the annualized return reaches 59.5% at the 5-second horizon and 62.82% at 15 seconds,
: Preprint submitted to Elsevier
Page 10 of 15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


## Page 13

Table 3
OOS Trading
Horizon
5s
10s
15s
30s
60s
Total trades
7880
6442
6653
4332
3991
Annualized returns
0.5950
0.3605
0.6282
0.6185
-2.2348
Annualized volatility
0.0694
0.0307
0.0911
0.2116
0.2556
Sharpe ratio
8.57
11.74
6.89
2.92
-8.74
while the corresponding Sharpe ratios remain high at 8.57 and 6.89. The 10-second horizon delivers the most favorable
risk-adjusted performance, with a Sharpe ratio of 11.74 and relatively low volatility of 3.07%.
At longer horizons, however, the profitability deteriorates. Although the 30-second horizon still yields a positive
annualized return of 61.85%, the Sharpe ratio drops to 2.92, reflecting the higher volatility of 21.16%. The degradation
becomes even more pronounced at the 60-second horizon, where the strategy generates a large negative annualized
return of –223.48% and a Sharpe ratio of –8.74. This pattern suggests that the CNN model is particularly effective in
capturing short-term predictive signals from limit order book images, but its forecasts lose reliability as the horizon
extends, where noise and mean-reverting microstructure effects dominate price dynamics.
The CNN-based trend prediction model demonstrates notable profitability and exceptional risk-adjusted returns,
particularly within high-frequency horizons (5s, 10s, and 15s). These results validate the potential of deep learning
models for real time execution in algorithmic trading, especially when complemented by conservative position sizing
and stringent transaction cost management. However, as the prediction horizon extends (30s and 60s), both the model’s
predictive calibration and its economic performance decline, suggesting that CNN models trained on short-term LOB
images are less adept at capturing longer-term price movements.
6. Robust Test
While Section 5 demonstrates the model’s effectiveness on May OOS data, robust financial modeling requires evi-
dence that its performance is not limited to a single market condition. To address this, we conduct two complementary
robustness tests. First, we evaluate the model’s predictive power under different volatility regimes to assess its stability
across different market environments. Second, we benchmark the CNN model against several classic technical trading
strategies to determine whether its superior performance stems from capturing genuine market signals rather than
overfitting or data specific patterns.
6.1. Performance Across Market Volatility Periods
To examine whether the CNN model retains its predictive accuracy and trading profitability across different market
environments, we conduct a robustness analysis stratified by local realized volatility. Specifically, we compute rolling
volatility based on intraday mid-price returns. For each test sample at time index 𝑡, the back-looking realized volatility
is calculated over a 60-second window as:
𝜎𝑡= std
{ 𝑃𝑖+1 −𝑃𝑖
𝑃𝑖
||||
𝑖∈[𝑡−𝜔, … , 𝑡−1]
}
,
(4)
where 𝑃𝑡denotes the mid-price at time 𝑡, and 𝜔= 60 seconds is the estimation window. This measure captures the
intensity of recent return fluctuations. After computing volatility for all valid test samples, we split them into High-
volatility and Low-volatility groups using the median volatility as the threshold, ensuring balanced subsample sizes.
Table 4 and 5 present the model’s performance when the out-of-sample test set is stratified by volatility. Several
important patterns emerge. In high-volatility periods, the CNN model translates turbulent market conditions into
profitable short-term strategies. At horizons of 5 to 30 seconds, annualized returns remain positive, ranging from
23.42% to 34.30%, while Sharpe ratios are consistently above 3. Notably, the 5-second horizon achieves the highest
Sharpe ratio of 9.43, indicating that the model is particularly effective in extracting predictive signals from order
flow when market activity is intense. However, performance deteriorates substantially at the 60-second horizon, with
negative McFadden 𝑅2, a Sharpe ratio of –6.95, and an annualized return of –158.19%. This suggests that as the
forecast horizon lengthens, noise and mean reversion dominate price dynamics, limiting profitability. In contrast,
: Preprint submitted to Elsevier
Page 11 of 15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


## Page 14

during low-volatility periods, model maintains robust classification accuracy, with McFadden 𝑅2 values as high as
0.4451 at the 15-second horizon. Trading performance is also favorable at short to medium horizons. For example, at
5 and 15 seconds, Sharpe ratios reach 12.56 and 7.98, respectively, while annualized returns are 18.05% and 28.52%.
Interestingly, the 30-second horizon yields the strongest profitability in quiet markets, with an annualized return of
95.13% and a Sharpe ratio of 7.96. Yet, as in the high-volatility case, performance collapses at the 60-second horizon,
where both Sharpe ratios and returns turn sharply negative.
Table 4
High-volatility Trading
Horizon
McFadden 𝑅2
Sharpe Ratio
Annualized Returns
5s
0.08
9.43
0.3317
10s
0.02
5.51
0.2342
15s
0.26
3.67
0.3430
30s
0.15
3.22
0.2889
60s
-0.02
-6.95
-1.5819
Table 5
Low-volatility Trading
Horizon
McFadden 𝑅2
Sharpe Ratio
Annualized Returns
5s
0.19
12.56
0.1805
10s
0.23
5.63
0.1263
15s
0.45
7.98
0.2852
30s
0.35
7.96
0.9513
60s
0.20
-3.90
-0.6529
These results reveal a clear asymmetry in the CNN model’s performance across volatility regimes. In high-volatility
environments, the model excels at extracting predictive signals from order flow, yielding consistently high Sharpe
ratios and positive returns at short horizons, though profitability deteriorates once the forecast horizon extends to
60 seconds. In contrast, in low-volatility periods the model continues to exhibit strong classification accuracy and
generates attractive returns at shorter and medium horizons, yet its profitability collapses at longer horizons due to the
absence of strong directional movements and the dominance of noise. These findings confirm that the CNN framework
is particularly well suited for high-frequency trading under volatile market conditions, while its effectiveness diminishes
in calmer environments, especially when the prediction horizon is lengthened.
6.2. Comparison with Traditional Strategies
Having established the CNN model’s differential performance across volatility periods, We benchmark it against
three standard rule-based technical strategies: (i) a short-term reversal strategy, which buys after negative returns
over the past 10 seconds and sells after positive returns, thereby exploiting potential price reversals; (ii) a momentum
strategy, which evaluates cumulative returns from 60 to 10 seconds prior, going long if the cumulative return is positive
and short otherwise; (iii) a trend-following strategy, which compares the current price with its moving average over a
window equal to the prediction horizon, going long when the price exceeds the moving average and short otherwise.
These strategies are standard approaches commonly employed in quantitative finance.
For each strategy, we evaluate both the annualized return and annualized volatility across five prediction horizons:
5s, 10s, 15s, 30s, and 60s. The comparative results are presented in Fig. 4.
Our findings demonstrate that the CNN model achieves consistently superior performance relative to the benchmark
strategies, particularly at shorter horizons. The model performs best at the 10-second horizon, where it records an
annualized return of 36.05% with a volatility of only 3.07%, resulting in the highest Sharpe ratio among all strategies
and horizons. Similar robustness is observed at the 5-second and 15-second horizons, with annualized returns of 59.5%
and 62.8%, respectively, accompanied by Sharpe ratios above 6. In contrast, the performance deteriorates sharply at
longer horizons, most notably at 60 seconds, where the CNN model produces large negative returns (-223.5%) and a
strongly negative Sharpe ratio (-8.74), highlighting its limitation in capturing more persistent dynamics.
: Preprint submitted to Elsevier
Page 12 of 15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


## Page 15

Figure 4: Trading by Traditional Technical Strategies
The momentum strategy exhibits weak and generally negative performance at shorter horizons, with Sharpe ratios
ranging from -8.75 at 5 seconds to -2.50 at 10 seconds. It only becomes profitable at longer horizons, delivering its
strongest outcome at 60 seconds with an annualized return of 70.3% and a Sharpe ratio of 4.74. The reversal strategy
yields relatively strong returns at 5, 10, and 15 seconds (30.5%, 25.7%, and 44.7%, respectively), with corresponding
Sharpe ratios ranging from 4 to 6. However, its performance is inconsistent, collapsing at the 60-second horizon with
negative returns (-36.6%) and high volatility (30.6%). Finally, the trend-following strategy performs poorly across
most horizons, producing negative returns at 10, 15, and 60 seconds, with only marginally positive results at 5 and 30
seconds, confirming its limited applicability in high-frequency environments.
The trend-following strategy assumes that prices move in prolonged directional patterns relative to moving aver-
ages. However, in high-frequency markets, such trends are rare. Short-term price movements are typically fragmented
and shaped more by limit order placement, cancellation, and matching mechanics rather than by macroeconomic or
behavioral drivers. Furthermore, in our test set, we observed that the majority of price movements were stagnant. Due
to the binary labeling scheme employed in this study, observations with no price change over the prediction horizon
were assigned to the “down” class. This situation causes the trend-following strategy, which depends on identifying
momentum above a moving average, to frequently generate false-positive long signals in a market that is either flat or
declining. As these conditions do not align with sustained trends, the strategy struggles to establish effective directional
momentum and incurs consistent losses.
In summary, these rule-based strategies are ill-suited to the dynamics of high-frequency markets, where non-linear,
rapidly shifting, and low-signal-to-noise patterns dominate. Their rigid signal structures lack the adaptability needed
to interpret the subtle variations in limit order book states. In contrast, the CNN model can learn these complex,
context-dependent patterns directly from LOB image inputs, making it far more effective for short-term prediction and
trading.
7. Conclusion
This paper contributes to the growing body of literature at the intersection of computer vision and financial
modeling by applying a Convolutional Neural Network (CNN) to predict second-level returns using Limit Order Book
(LOB) image data. By transforming raw market microstructure information into visual representations, the CNN is
able to detect complex and non-linear patterns that traditional rule-based methods often fail to capture. Across multiple
short-term forecast horizons, our empirical findings demonstrate that the image-based model delivers superior return
predictability and trading performance, particularly within the 5–30 second range.
We further validate the model’s robustness through tests across different volatility regimes and through systematic
comparisons with classical technical strategies such as momentum, reversal, and trend-following. While rule-based
approaches exhibit horizon-dependent weaknesses—momentum strategies performing poorly at short horizons but
gaining strength at longer horizons, reversal strategies showing intermittent success yet lacking consistency, and trend-
following strategies remaining largely ineffective—the CNN model consistently dominates in the short-run. However,
at longer horizons such as 60 seconds, its performance deteriorates sharply, highlighting the temporal limits of its
predictive power.
One of the most important implications of our findings is the model’s ability to capture subtle, high-frequency
patterns embedded in LOB structures—patterns that may reflect transient liquidity imbalances, order flow pressure, or
: Preprint submitted to Elsevier
Page 13 of 15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


## Page 16

fleeting arbitrage opportunities. Unlike conventional time-series methods, the CNN learns from spatial configurations
of market data, offering a fundamentally different lens through which to interpret market dynamics. In doing so, it not
only serves as a predictive tool but also points toward a richer modeling paradigm: one that aligns more closely with
how human traders visually interpret order books and respond to their structure in real time.
The study represents a modest but promising step toward bridging the gap between machine perception and
high-frequency financial decision-making. Future research could explore extending this framework to portfolio-
level applications, incorporating multi-asset visual inputs, or integrating attention-based architectures to enhance
interpretability. As markets continue to evolve in complexity and speed, image-based approaches provide a novel and
powerful methodology for decoding the rapidly shifting signals embedded within market microstructure.
CRediT authorship contribution statement
: . : .
References
Ahn, H.J., Bae, K.H., Chan, K., 2001. Limit orders, depth, and volatility: Evidence from the stock exchange of hong kong. J. Finance 56, 767–788.
Akita, R., Yoshihara, A., Matsubara, T., Uehara, K., 2016. Deep learning for stock prediction using numerical and textual information, in: Proc.
2016 IEEE/ACIS 15th Int. Conf. Comput. Inf. Sci. (ICIS), pp. 1–6.
Baker, M., Wurgler, J., 2007. Investor sentiment in the stock market. J. Econ. Perspect. 21, 129–151.
Barberis, N., 2018.
Psychology-based models of asset prices and trading volume, in: Handbook of Behavioral Economics: Applications and
Foundations 1. Elsevier, Amsterdam. volume 1, pp. 79–175.
Biais, B., Foucault, T., Moinas, S., 2015. Equilibrium fast trading. J. Financ. Econ. 116, 292–313.
Bloomfield, R., O’hara, M., Saar, G., 2005. The “make or take” decision in an electronic market: Evidence on the evolution of liquidity. J. Financ.
Econ. 75, 165–199.
Brogaard, J., Hendershott, T., Riordan, R., 2014. High-frequency trading and price discovery. Rev. Financ. Stud. 27, 2267–2306.
Brogaard, J., Hendershott, T., Riordan, R., 2019. Price discovery without trading: Evidence from limit orders. J. Finance 74, 1621–1658.
Brown, G.W., Cliff, M.T., 2004. Investor sentiment and the near-term stock market. J. Empir. Finance 11, 1–27.
Cao, C., Hansch, O., Wang, X., 2009. The information content of an open limit-order book. J. Futures Mark. 29, 16–41.
Carrion, A., 2013. Very fast money: High-frequency trading on the nasdaq. J. Financ. Mark. 16, 680–711.
Chen, J.F., Chen, W.L., Huang, C.P., Huang, S.H., Chen, A.P., 2016. Financial time-series data analysis using deep convolutional neural networks,
in: Proc. 2016 7th Int. Conf. Cloud Comput. Big Data (CCBD), pp. 87–92.
Chen, L., Pelger, M., Zhu, J., 2024. Deep learning in asset pricing. Manag. Sci. 70, 714–750.
Conrad, J., Wahal, S., Xiang, J., 2015. High-frequency quoting, trading, and the efficiency of prices. J. Financ. Econ. 116, 271–291.
Cont, R., Stoikov, S., Talreja, R., 2010. A stochastic model for order book dynamics. Oper. Res. 58, 549–563.
Corwin, S.A., Lipson, M.L., 2000. Order flow and liquidity around nyse trading halts. J. Finance 55, 1771–1801.
Degryse, H., Jong, F.D., Ravenswaaij, M.V., 2005. Aggressive orders and the resiliency of a limit order market. Rev. Finance 9, 201–242.
Foucault, T., Hombert, J., Roşu, I., 2016. News trading and speed. J. Finance 71, 335–382.
Foucault, T., Kadan, O., Kandel, E., 2005. Limit order book as a market for liquidity. Rev. Financ. Stud. 18, 1171–1217.
Foucault, T., Moinas, S., Theissen, E., 2007. Does anonymity matter in electronic limit order markets? Rev. Financ. Stud. 20, 1707–1747.
Goettler, R.L., Parlour, C.A., Rajan, U., 2005. Equilibrium in a dynamic limit order market. J. Finance 60, 2149–2192.
Goettler, R.L., Parlour, C.A., Rajan, U., 2009. Informed traders and limit order markets. J. Financ. Econ. 93, 67–87.
Griffiths, M.D., Smith, B.F., Turnbull, D.A.S., White, R.W., 2000. The costs and determinants of order aggressiveness. J. Financ. Econ. 56, 65–88.
Gu, S., Kelly, B., Xiu, D., 2020. Empirical asset pricing via machine learning. Rev. Financ. Stud. 33, 2223–2273.
Hagströmer, B., Nordén, L., 2013. The diversity of high-frequency traders. J. Financ. Mark. 16, 741–770.
Harris, L., 2013. What to do about high-frequency trading. Financ. Anal. J. 69, 6–9.
Hasbrouck, J., Saar, G., 2013. Low-latency trading. J. Financ. Mark. 16, 646–679.
Hautsch, N., Huang, R., 2012. The market impact of a limit order. J. Econ. Dyn. Control 36, 501–522.
Hirschey, N., 2021. Do high-frequency traders anticipate buying and selling pressure? Manag. Sci. 67, 3321–3345.
Hoffmann, P., 2014. A dynamic limit order market with fast and slow traders. J. Financ. Econ. 113, 156–169.
Hollifield, B., Miller, R.A., Sandås, P., 2004. Empirical analysis of limit order markets. Rev. Econ. Stud. 71, 1027–1063.
Hu, G., Hu, Y., Yang, K., Yu, Z., Sung, F., Zhang, Z., Xie, F., Liu, J., Robertson, N., Hospedales, T., e.a., 2018. Deep stock representation learning:
From candlestick charts to investment decisions, in: Proc. 2018 IEEE Int. Conf. Acoust. Speech Signal Process. (ICASSP), pp. 2706–2710.
Kelley, E.K., Tetlock, P.C., 2013. How wise are crowds? insights from retail orders and stock returns. J. Finance 68, 1229–1265.
Kirilenko, A., Kyle, A.S., Samadi, M., Tuzun, T., 2017. The flash crash: High-frequency trading in an electronic market. J. Finance 72, 967–998.
Korajczyk, R.A., Murphy, D., 2019. High-frequency market making to large institutional trades. Rev. Financ. Stud. 32, 1034–1067.
Large, J., 2007. Measuring the resiliency of an electronic limit order book. J. Financ. Mark. 10, 1–25.
Large, J., 2009. A market-clearing role for inefficiency on a limit order book. J. Financ. Econ. 91, 102–117.
Lo, A.W., MacKinlay, A.C., 1988. Stock market prices do not follow random walks: Evidence from a simple specification test. Rev. Financ. Stud.
1, 41–66.
Madhavan, A., 2000. Market microstructure: A survey. J. Financ. Mark. 3, 205–258.
: Preprint submitted to Elsevier
Page 14 of 15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


## Page 17

Mäkinen, Y., Kanniainen, J., Gabbouj, M., Iosifidis, A., 2019. Forecasting jump arrivals in stock prices: new attention-based network architecture
using limit order book data. Quant. Finance 19, 2033–2050.
Næs, R., Skjeltorp, J.A., 2006. Order book characteristics and the volume–volatility relation: Empirical evidence from a limit order market. J.
Financ. Mark. 9, 408–432.
Pascual, R., Veredas, D., 2010. Does the open limit order book matter in explaining informational volatility? J. Financ. Econometr. 8, 57–87.
Sandås, P., 2001. Adverse selection and competitive market making: Empirical evidence from a limit order market. Rev. Financ. Stud. 14, 705–734.
Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., Salakhutdinov, R., 2014. Dropout: A simple way to prevent neural networks from overfitting.
J. Mach. Learn. Res. 15, 1929–1958.
Timmermann, A., Granger, C.W.J., 2004. Efficient market hypothesis and forecasting. Int. J. Forecast. 20, 15–27.
Toth, B., Palit, I., Lillo, F., Farmer, J.D., 2015. Why is equity order flow so persistent? J. Econ. Dyn. Control 51, 218–239.
Tsantekidis, A., Passalis, N., Tefas, A., Kanniainen, J., Gabbouj, M., Iosifidis, A., 2017. Forecasting stock prices from the limit order book using
convolutional neural networks, in: Proc. 2017 IEEE 19th Conf. Business Informatics (CBI), Vol.1, pp. 7–12.
Vargas, M.R., De Lima, B.S.L.P., Evsukoff, A.G., 2017. Deep learning for stock market prediction from financial news articles, in: Proc. 2017 IEEE
Int. Conf. Comput. Intell. Virtual Environ. Meas. Syst. Appl. (CIVEMSA), pp. 60–65.
Zhang, X., Zhang, Y., Wang, S., Yao, Y., Fang, B., Yu, P.S., 2018. Improving stock market prediction via heterogeneous information fusion.
Knowl.-Based Syst. 143, 236–247.
: Preprint submitted to Elsevier
Page 15 of 15
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=6189791
Preprint not peer reviewed


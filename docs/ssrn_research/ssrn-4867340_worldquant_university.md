# WorldQuant University

- **Source File**: `ssrn-4867340.pdf`
- **Total Pages**: 28
- **SSRN ID**: `ssrn-4867340`

---


### Page 1

WorldQuant University
2024
Copyright ⓒ
Optimizing Cryptocurrency Trading with
Machine Learning: Predictive Analytics with
Limit Order Book and Sentiment Data
Author
Diana Gorsh
diana.gorsh@gmail.com
“This paper was created as part of a WorldQuant University degree program
towards an MSc in Financial Engineering. This paper is reproduced with the
consent and permission of WorldQuant University.
All rights reserved.”


### Page 2

WorldQuant University
2024
2
Abstract
This capstone project, prepared by Diana Gorsh, tackles the challenge of optimizing
cryptocurrency trading through the development of a predictive analytics model that
leverages machine learning to facilitate generating trading signals by utilizing limit order
book and the sentiment scores along with price movements. The project is set against the
backdrop of the cryptocurrency market's extreme volatility and the limitations of traditional
financial analysis tools in this unique domain. It aims to bridge the gap between
conventional market analysis techniques and the specific needs of cryptocurrency trading
by refining machine learning methodologies for more effective decision-making processes.
The core of the project is the construction of a sophisticated predictive model designed
to make informed trading decisions by analyzing a wide array of market variables, such as
historical trade data, sentiment, volume metrics, and the depth of the limit order book, with
a focus on highly liquid cryptocurrencies. The model employs data from the top ten levels
of the limit order book, utilizing stationary transformations of this data—specifically, order
flow and order flow imbalance—to capture the nuances of market dynamics more
accurately than traditional approaches.
To enhance prediction accuracy, the project explores ensemble and hybrid models that
integrate various deep learning architectures, such as Long Short-Term Memory (LSTM)
networks and Variational Autoencoders (VAEs), addressing challenges like data overfitting
and model complexity. Moreover, it incorporates sentiment analysis through FinBERT, a
transformer-based model pre-trained on financial texts, to assess market sentiment as a
critical input feature.
The methodology extends beyond theoretical research, aiming to create a practical tool
for cryptocurrency trading that combines market movement predictions, risk assessment,
and sentiment analysis. This integrated machine learning framework endeavors to provide
a comprehensive toolset for traders, allowing for more informed decisions and strategic
trade execution. The project is supported by a GitHub repository and includes
acknowledgments and references to foundational and recent works in the field, positioning
itself as a significant contribution to both academic research and professional practice in
cryptocurrency trading optimization.
.
The extreme volatility in the cryptocurrency markets, coupled with the complexity
of trading execution, portfolio construction and strategy optimization, contribute to
challenges in making strategic investments. Traditional financial market analysis tools and
techniques struggle to adapt into the cryptocurrency domain due to its unique
characteristics, adding the necessity for innovative approaches in trading strategy
development and portfolio management.
This capstone project aims to bridge the gap between traditional financial market
analysis and the unique challenges of the cryptocurrency domain by adapting and refining
machine learning methodologies to enhance decision-making processes for predicting
market movements, assessing risks, and analyzing sentiment.
The central challenge addressed by this project is the development of a nuanced
predictive model designed to support informed trading decisions. Such a model must
interpret and analyze an extensive array of market variables including historical trade data,
volume metrics, sentiment, and depth of the limit order book, focusing primarily on highly
liquid cryptocurrencies such as Bitcoin (BTC), Ethereum (ETH), and Solana (SOL) against


### Page 3

WorldQuant University
2024
3
the U.S. dollar. As we can see from the correlation matrix below (Figure 1), those 3 pairs
are highly correlated.
Figure 1. Correlation Matrix for BTC, SOL and ETH
Trading in securities today frequently utilizes a limit order book, which aggregates
all buy and sell orders. This book serves to match incoming orders for execution or to be
listed in the book based on their price and time of submission. The bid price represents the
maximum price buyers are willing to pay, while the ask price is the minimum sellers are
willing to accept. The model we are developing aims to forecast the movement of the mid-
price, which is calculated as the average between the bid and ask prices.
An order's characteristics include its type (buy or sell), the quantity desired, the
price at which the trade is intended, and the time it was submitted. Upon entry into the
system, the exchange's matching engine attempts to pair the new order with existing ones
in the book. Orders that find a match are executed as market orders, while those that don't
match or only partially match become limit orders and are added to the book.
Our predictive model uses data from the top ten levels of the order book as input.
Each level is specified by its price and the volume being bid or asked. On the bid side,
prices decrease with each subsequent level, whereas on the ask side, prices increase. Our
dataset consists of 40-variable vectors, capturing the price and volume of the top ten levels
for both bids and asks, effectively providing a snapshot of the limit order book's state at
each moment in time.


### Page 4

WorldQuant University
2024
4
Figure 2. Ask-Bid Spread
Building on the work of Zhang et al. and others, the model is trained on stationary
transformations of limit order book data - specifically order flow and order flow imbalance
- to better capture the nuances of market dynamics. This approach contrasts with previous
works that have typically relied on non-stationary order book states (Zhang, Zohren, and
Roberts, 2020).
Stationary transformations of limit order book (LOB) data, specifically focusing on
order flow and order flow imbalance, offer a refined lens through which to view and predict
market dynamics. These transformations help in mitigating the challenges posed by the
non-stationary nature of raw LOB data, enabling more stable and predictive modeling.
Non-stationary data, which is typical of raw LOB states, poses significant
challenges for predictive modeling due to its changing mean and variance over time. This
can lead to models that are less generalizable and potentially overfit to specific time periods.
Stationary data, on the other hand, with its constant mean and variance, is more amenable
to traditional time series analysis and forecasting techniques, leading to models that are
potentially more stable and predictive over different market conditions.
The model takes as inputs representations of the first ten levels of the order book.
A level is denoted by its price and volume that is bid or asked. So, as we progress down
levels on the bid side of the order book, the price decreases, and as we progress down levels
of the ask side, the price increases. Each observation in our dataset will be a 40-variable
vector displaying the price and volume for each of the top ten bid and ask levels, giving us
a truncated screenshot of the state of the limit order book at each timestep.


### Page 5

WorldQuant University
2024
5
Table 1. Limit Order Book (BTC-USD)
We define the bid order flows (bOF) and ask order flows (aOF) at a timestamp to
be 10-variable vectors computed using two consecutive order book states, where each
element is given by:
(1)
Order Flow (OF) represents the net volume of orders entering the market. It’s
calculated as the difference between the volume of buy orders and sell orders within a
specific timeframe and can be defined as:
(2)


### Page 6

WorldQuant University
2024
6
Table 2. Bid-Ask Order Flow (BTC-USD)
Order Flow Imbalance (OFI) reflects the difference in the order flow between the
buy and sell sides of the market, providing an indicator of which side is exerting more
pressure and potentially where the price might move, and is calculated as:
(3)
where Vbuy,i and Vsell,i represent the volume of buy and sell orders at time i,
respectively.
Table 3. Bid-Ask Order Flow Imbalance (BTC-USD)


### Page 7

WorldQuant University
2024
7
Data Gathering:
From Coinbase Exchange, using API, we fetched LOB data for all 3 trading pairs
and 10000 observations for each, which took substantial computational resources. For
example, to fetch 100 limit order book observations just for one pair “BTC-USD” took
approximately 3 minutes. Therefore, it would take 5*3 hours to fetch all necessary data
unless we would run it on cloud in parallel.
We also extracted Open, Close, High, Low, Volume (OCLHV) data, for the same
timestamps as LOB data to integrate this with order flow and imbalance. The granularity
for OCLHV data for each trading pair was chosen equal to 60, which is 1 minutes and
approximately 2240 observations in 1 trading day. For LOB data we fetched about 10,000
observations for each trading pair over the course of a day as well. This approach provides
a robust dataset incorporating both traditional market indicators and advanced metrics
capturing market dynamics. The addition of OF and OFI aims to enhance the model's ability
to discern underlying market pressures and trends that may not be evident from price data
alone. The time series graphs with candles for each cryptocurrency pair for a chosen day
can be found in Appendix 2.
By integrating these stationary transformations into the predictive models, we
could assess their impact on forecasting performance through backtesting. The expectation
is that these metrics will offer predictive insights into market directionality, improving the
accuracy and reliability of trading strategy. This methodological shift towards stationary
transformations of LOB data signifies a more nuanced understanding of market mechanics,
potentially leading to superior forecasting models that can adapt to and capitalize on the
fluid dynamics of the cryptocurrency markets.
The model:
The exploration of ensemble and hybrid models has emerged as a promising
direction for improving prediction accuracy. By combining the strengths of multiple
predictive models, ensemble approaches can offer more robust and accurate forecasts. For
example, the use of ensemble models incorporating LSTM, GRU, and other DL
architectures has been shown to marginally improve prediction performance (Murray et al.,
2023).
Table 4. Ensemble and Hybrid models Comparison
Despite the promising outcomes associated with these models, challenges such as
data overfitting, model complexity, and the dynamic nature of financial markets persist.


### Page 8

WorldQuant University
2024
8
These issues not only complicate model training and validation but also highlight the
importance of continuous model adaptation and the exploration of diverse data sources,
including social media for a more comprehensive sentiment analysis (Zeng & Jiang, 2023;
Koker & Koutmos, 2020). Moreover, the inherent volatility and unpredictability of the
market, coupled with the influence of external factors such as regulatory changes and
market sentiment, complicate the forecasting task. Furthermore, the computational
complexity and data requirements of advanced DL models pose practical limitations.
Therefore, we are proposing a long short-term memory (LSTM) network to predict
the future direction of an order book at high frequency. Using Coinbase order book data for
Bitcoin, Ethereum and Solana our goal is to forecast whether the mid-price will rise, fall,
or remain constant in the subsequent time series observation.
The universal approximation theorem suggests that a feedforward neural network
with just one hidden layer has the capacity to approximate any continuous function within
a defined compact subset. However, specialized neural network designs can tap into the
unique patterns present in data—a feature especially beneficial for analyzing complex
financial time series. Long Short-Term Memory networks (LSTMs) architecture has the
ability to process and adapt to data over time in ways that enhance their performance in
challenging modeling tasks. In contrast, simpler feedforward networks may face difficulties
with instability and a lack of clarity when trying to decipher intricate data relationships.
The exact number of layers will be determined through hyperparameter
optimization – to effectively capture the temporal sequences within the market data. These
networks will be trained using advanced optimizer Adam to refine learning rates and
mitigate the vanishing gradient problem inherent in deep network training.
Figure 3. LSTM model architecture
LSTMs, a subset of recurrent neural networks, are adept at managing sequences
and their inherent temporal correlations, countering the vanishing gradient dilemma that
plagues standard RNNs. An LSTM unit, equipped with a memory cell and three regulatory
gates, meticulously manages information flow, deciding what data is stored, updated, or
forgotten, thus allowing for efficient processing of temporal sequences in data.


### Page 9

WorldQuant University
2024
9
(4)
where
m
is
the
number
of
LSTM
units
in
the
module,
σ(x)=(1+e−x)−1=(1+(1+ex)−1) is the sigmoid activation function, ft∈Rm×f is the forget
gate's activation vector, it∈Rm×i is the input gate's activation vector, ot∈Rm×o is the output
gate's activation vector, ct∈Rm×c is the LSTM unit's hidden state vector, and ht∈Rm×h is
the unit's output vector. U∈Rm×n, W∈Rm×m, and b∈Rm×b are learned during training and
represent the weight matrices in connection to the input vector, the weight matrices in
connection to the previous output state, and the bias vectors, respectively (Kolm, Turiel, &
Westray, 2021).
Below are the architecture and the results of our first constructed LSTM model,
that is incorporating Batch Normalization and training with class weights. We normalized
the output of a previous activation layer by subtracting the batch mean and dividing by the
batch standard deviation, then scaling and shifting using learned parameters. This helps to
stabilize and accelerate the training process by reducing internal covariate shift. It also acts
as a regularizer, potentially improving the model's ability to generalize to new data. By
applying class weights, we improved the balance and performance of the model on the
"Down" and "Up" classes. These improvements contributing to training stability and
potentially better performance on underrepresented classes.
We also explored Vector autoregression (VAR) model to fit order flow (OF) and
order flow imbalance (OFI) data. It’s important to determine the correct number of past
observations, or "lags," to include in the model. This helps ensure that LSTM model can
adequately capture the dynamics of the data.


### Page 10

WorldQuant University
2024
10
Figure 4. LSTM_1 model architecture for OF/OFI classification
Figure 5. LSTM_1 model results and confusion matrix
From Figure 5 we can see the classification metrics - the precision, recall, F1-score,
and support for each class in both OF and OFI classification tasks. These metrics provide a
detailed picture of the model's performance across different classes. Precision, which
measures the accuracy of the positive predictions, shows variability across classes. For
instance, in the OF classification, the 'Stationary' class achieves higher precision compared
to the 'Down' and 'Up' classes. This indicates that the model is more confident and accurate
when predicting the 'Stationary' state, but less so for 'Down' and 'Up' states. Recall, on the
other hand, measures the model's ability to identify all positive instances of a class. Here,
again, the 'Stationary' class shows better recall, meaning the model is more successful in
identifying instances of 'Stationary' compared to the other states.


### Page 11

WorldQuant University
2024
11
The F1-score, which is the harmonic mean of precision and recall, balances these
two metrics and provides a single measure of performance. For both OF and OFI
classifications, the F1-scores indicate that while the model performs reasonably well for the
'Stationary' class, it struggles more with the 'Down' and 'Up' classes. This might be due to
the inherent imbalance in the data, as indicated by the support values, which show that
'Stationary' has a significantly higher number of instances compared to 'Down' and 'Up'.
The support values highlight the number of true instances for each class, and the imbalance
can skew the model's performance, favoring the more frequent 'Stationary' class.
Analyzing the confusion matrices showing the distribution of predictions across the
actual classes, we can see that the majority of misclassifications occur between 'Stationary'
and the other states. This, again, suggests that the model often predicts 'Stationary' when
the true class is 'Down' or 'Up', which aligns with the higher precision and recall for
'Stationary'. Addressing this misclassification could involve further tuning the model or
incorporating additional features that help better distinguish between these states.
Figure 6. LSTM_1 model Training and Validation Losses


### Page 12

WorldQuant University
2024
12
From the graphs in Figure 6, we can see the learning process of the LSTM model
which indicates a successful training process where both training and validation losses
decrease over time. The validation loss follows the training loss closely, suggesting that the
model is generalizing well to unseen data without significant overfitting. The first graph
depicts the model's loss over epochs for both the training set and the validation set. Ideally,
we want to see both lines trending downwards, with the validation loss following closely
behind the training loss, which seems to be the case here after the initial epochs.
The training and validation loss both show some volatility, which is normal in the
beginning as the model starts to learn, but since the volatility continues, it might suggest
that the learning rate is too high or that the model's capacity (its complexity) is not
adequately tuned to capture the underlying patterns in the data.
The reasonable performance of the model might be due to the fact that it’s too
simplistic to do justice to the underlying complexity of the data. We will consider more
LSTM layers or increasing the number of units in the LSTM layers, as well as adjusting the
model's hyperparameters, such as the learning rate, batch size, or epoch. We are going to
optimize the model using the GridSearch.
Alongside the LSTM model, we propose Variational Autoencoder (VAE
Variational Autoencoder (VAE) for risk estimation. This approach is particularly suited for
capturing the latent representation of high-dimensional financial data and subsequently
estimating the covariance matrix. The VAE processes high-dimensional order flow (OF)
and order flow imbalance (OFI) data, reducing noise and highlighting critical features
within the data.
The VAE addresses the limitations of traditional linear factor models by leveraging
neural networks to model complex, non-linear relationships within the data. This allows for
a more accurate estimation of risk in financial portfolios. Once the VAE compresses the
data into its latent representation, we use this representation to estimate the covariance
matrix, which is crucial for portfolio risk management. This covariance matrix is then used
in the construction of a minimum variance portfolio, demonstrating the practical application
of the VAE in financial scenarios.
Following the transformation and risk estimation, the encoded data from the VAE
is fed into a Long Short-Term Memory (LSTM) network for trading purposes. The LSTM
utilizes the refined features from the VAE to make predictions about future time steps,
enhancing its sequential modeling capabilities. This two-step process leverages the
strengths of both the VAE and LSTM: the VAE excels at feature extraction and noise
reduction, while the LSTM is adept at recognizing temporal patterns.
The process involves first training the VAE on the OF and OFI datasets to create
the latent representation. This representation is then used to estimate the covariance matrix.
The estimated covariance matrix is crucial for constructing a minimum variance portfolio,
which is a key application in risk management. Those graphs can be found in Appendix 4
to 7.


### Page 13

WorldQuant University
2024
13
For optimization, we performed a grid search to identify the most effective model
parameters. The best-performing parameters for the Variational Autoencoder (VAE) used
with the Order Flow Imbalance (OFI) data were as follows: a hidden dimension of 128, a
latent dimension of 10, a learning rate of 0.0001, a batch size of 32, and 100 epochs. These
parameters were determined through extensive experimentation, ensuring the robustness
and effectiveness of the model in handling high-dimensional financial data. A hidden
dimension of 128 was chosen to capture the complex relationships in the data, while a latent
dimension of 10 suggests that the model's latent space, where it encodes the input data,
consists of 10 features. This helps in capturing the essence of the input data while
maintaining computational efficiency.
By adjusting the batch size and epochs, we experimented with the learning process
to find an optimal balance between training time and model performance. Our model's loss
function, which includes both reconstruction loss and KL divergence, is finely tuned to
balance the model's focus between data fidelity and latent space regularization.
In our Variational Autoencoder (VAE) model, the Kullback-Leibler (KL)
divergence is a crucial component. It's part of the loss function and helps the model learn a
well-formed latent space that approximates the prior distribution. The KL divergence acts
as a regularizer in the loss function of a VAE. It measures how much one probability
distribution diverges from a second, expected probability distribution. In the context of
VAEs, it's used to compare the distribution of the latent variables encoded by the encoder
network to the prior distribution.
The loss function of a VAE defines as follows and is composed of two parts:
(5)
where 𝐿𝐿𝐿𝐿𝐿𝐿𝐿𝐿𝐿𝐿𝐿𝐿 is a Reconstruction Loss that measures how well the decoded
samples match the original inputs. In the case of an LSTM-VAE this would be the Mean
Squared Error (MSE) between the predicted sequence and the true sequence:
(6)
KL Divergence part of the loss function measures how the learned latent variable
distribution (encoded by the LSTM encoder) diverges from the prior distribution. It
encourages the encoder to produce latent variables that follow the prior distribution, which
helps in generating more consistent and coherent data points from the latent space during
the decoding process. The KL divergence part of the loss ensures that the latent variables 𝑧𝑧
follow the prior distribution 𝑝𝑝(𝑧𝑧), which is often chosen to be the standard normal
distribution 𝑁𝑁(0,𝐼𝐼). The encoder of the VAE models the posterior distribution 𝑞𝑞(𝑧𝑧∣𝑥𝑥) as a
normal distribution 𝑁𝑁(𝜇𝜇,𝜎𝜎2𝐼𝐼) with a mean 𝜇𝜇 and standard deviation 𝜎𝜎 that are functions of
the input 𝑥𝑥. The KL divergence between 𝑞𝑞(𝑧𝑧∣𝑥𝑥) and 𝑝𝑝(𝑧𝑧) is computed as follows:


### Page 14

WorldQuant University
2024
14
(7)
where 𝐽𝐽 is the dimensionality of the latent space.
The KL divergence is integrated into the training of the VAE by adding it to the
reconstruction loss to form the final loss that is minimized during training. This integration
is necessary for the VAE to not only fit the data but also ensure that the latent space has
good properties, enabling generative processes. By utilizing MSE for the reconstruction
loss and combining it with KL divergence, we aim to maintain a balance between the
model's ability to reconstruct input data and its generalization capability. By using these
optimized parameters and carefully tuning the loss function, we ensured that our VAE
models for both OFI and price/sentiment data were robust and effective in capturing the
essential features of high-dimensional financial data.
The second part of the project is to integrate sentiment analysis by employing
FinBERT, a transformer-based model pre-trained on financial texts. It will be fine-tuned on
domain-specific datasets to accurately capture market sentiment, which will serve as a
pivotal input feature for the predictive models.
"Financial Sentiment Analysis using FinBERT with Application in Prediction
Stock Movement" by Qingyun Zeng and Tingsong Jiang paper explores the innovative
Application of FinBERT, a variant of BERT trained specifically on financial data, which is
adept at capturing the nuances of financial sentiment. This specialization could potentially
offer superior sentiment analysis in the financial context compared to generic language
models. Using the Cryptopanic API key, we are able to feftch financial news for each
Crypto Pair. For text summarization, we used models that are trained specifically for that
task, such as BART (Bidirectional and Auto-Regressive Transformers).
Figure 7. Example of DataFrame with Sentiment output


### Page 15

WorldQuant University
2024
15
Alongside with fetched previously OCLHV data we now constructed dataframe for
BTC_USD prices with sentiment score from FinBERT and merged by timestamps. The
next step was to add a NSI index as well, as discussed in Zeng & Jiang paper - “we proposed
a numerical sentiment index based on the price movement, which is defined as NSI = 1 if
return > s and NSI = 0 if −s < return < s and NSI = −1 if return < −s” (Zeng & Jiang, 2023).
The formula for calculating returns is given by the ratio of the closing price minus the
opening price to the opening price. This formula can be extended to calculate the return
over any number of days k by using the closing price on the k-th day after the current one.
(8)
The Normalized Sentiment Indicator (NSI) plays a role in refining the predictions
of closing prices using models like FinBERT, which assess the interplay between textual
sentiment and market dynamics. To forecast closing prices while mitigating issues like
long-term inflation and stock diversity, we apply a MinMax scaler to the data before
modeling. Our data is split into a 90% training set and a 10% testing set. Predicting long-
term market trends is challenging due to unpredictable events.
Table 5. DataFrame with NSI and Sentiment scores
The dynamic nature of market sentiment, especially in response to real-time events,
poses a challenge for any model relying on historical data for prediction. The lag between
news publication and market reaction may limit the model's effectiveness in fast-moving
markets (Zeng & Jiang, 2023).
Below is the distribution of the return for BTC close price, which shows a
pronounced peak at zero. This distribution suggests that small percentage changes in BTC's
close price are most common, reflecting frequent minor fluctuations in price. The sharp
peak at zero indicates a high frequency with short time frames. The fat tails indicate that
while extreme changes in percentage are less frequent, they are still significant enough to
affect the distribution, highlighting the inherent volatility of BTC prices. The symmetry of
the distribution also suggests that upward and downward movements are equally probable,
reflecting the dynamic and unpredictable nature of cryptocurrency markets.


### Page 16

WorldQuant University
2024
16
Figure 8. Distribution of Returns for BTC time series
We trained LSTM models using historical BTC price data combined with sentiment
scores and NSI values, which lead to potentially more informed trading decisions,
predicting future price movements based on these features. Similarly, to include a
comprehensive risk analysis, we trained a VAE model for the price/sentiment data with the
same best-performing parameters: a hidden dimension of 128, a latent dimension of 10, a
learning rate of 0.0001, a batch size of 32, and 100 epochs. These parameters were
determined through grid search and extensive experimentation, ensuring that the model
effectively encodes the input data into a lower-dimensional space with 10 features. The
learning rate of 0.0001 ensures a smooth convergence during the optimization process.
Figure 9. Buy/Sell Decisions on BTC Train Data


### Page 17

WorldQuant University
2024
17
The "Buy/Sell Decisions" graph in Figure 9 illustrates the actual BTC price
movements over a period of days, with buy and sell signals generated by our LSTM model.
The black line represents the actual price, while green and red markers indicate buy and sell
signals, respectively, showing 303 buy signals and 51 sell signals.
Now we have two tuned and trained separate LSTM models: one on historical BTC
price data with sentiment scores and NSI values, and the other on OFI data. We then
combined the predictions from both models to enhance the robustness of the trading signals.
Additionally, we employed two VAE models, one trained on the OFI dataset and the other
on the price/sentiment dataset, to estimate the risk associated with each trading decision.
The combined predictions and risk metrics were used to generate buy, sell, and hold signals,
which were then backtested on the test data to evaluate the performance. This integrated
approach, leveraging both price/sentiment and OFI data along with risk management from
the VAEs, enabled us to create a more comprehensive and effective trading strategy.
Through integrating the predictability of prices and the dynamics of the limit order
book, reinforcement learning surpasses numerous established methods, including those
based on price prediction through supervised learning. For reinforcement learning, two
strategies exist for training agents with market data: employing offline data and utilizing
online data. Offline data use involves processing historical market data for training, which
is more time-efficient than the use of online data, which relies on real-time market data.
Since the supervised learning component necessitates historical data storage, offline data is
accessible for simulating market conditions for learning purposes. The implementation
includes developing the backtesting procedure, utilizing the following algorithm (Jaddu and
Bilokon, 2023):
Figure 10. Backtesting Algorithm (Jaddu and Biloko, 2023)
We conducted backtesting to offer the agent subsequent state and reward based on
the current state and action while incorporating transaction costs into each trade's profit or


### Page 18

WorldQuant University
2024
18
loss. Evaluating trading strategies or automated trading bots in a risk-free yet realistic
setting is crucial before their live trading deployment with real capital. Backtesting
simulates market conditions using historical data to assess the outcomes of buy/sell signals
as if they were actual trades. These results help gauge the agent's performance post-
simulation. Since Coinbase does not offer historical limit order book (LOB) data,
backtesting required independent coding. The backtesting routine alternates the agent
between maintaining active buy or sell positions, with all trade signals and outcomes
recorded for performance evaluation. Although we did not use OpenAI’s Gym Environment
or incorporate retail-level commissions into each trade's profit or loss, we accounted for
transaction costs in the assessment.
Figure 11. Backtesting Results
The graph above "Buy/Sell Decisions for BTC" illustrates the results of our
backtesting. It shows BTC price movements over time with buy signals (green triangles)
and sell signals (red triangles) overlaid. The model's signals are based on a combination of
LSTM predictions and risk assessments from VAEs trained on OFI and price/sentiment
data. The initial balance was set at 5000 units, and the final balance post-backtesting was
6933.93 units, indicating a profitable strategy. However, the highly precise signals might
indicate potential data leakage, which warrants further investigation and validation.
Additionally, since Solana (SOL) and Ethereum (ETH) are highly correlated with Bitcoin
(BTC), we applied the same strategies and models in parallel to these assets. The detailed
results of these applications can be found in Appendix 7.
Future developments will involve forward testing, which considers the viability of
a trading strategy based on its backtesting performance. This involves connecting the agent
to a platform like Coinbase for live, unseen data processing and real order submissions.
Forward testing, essential for accurate simulation, will utilize the Coinbase API through a
Flask-based web application, enabling model-based signal transmission to the platform via
POST requests. It supports both real and simulated (paper trading) money, providing a more
authentic experience as the platform updates the agent on order executions, including any
discrepancies from expected entry prices (slippage) and variable spreads. Forward testing's


### Page 19

WorldQuant University
2024
19
outcomes offer a more precise reflection of a strategy's effectiveness compared to
backtesting. Despite the higher accuracy, forward testing is more resource-intensive,
relying on live data rather than historical data iterations, explaining why backtesting
remains a valuable preliminary step (Jaddu and Biloko, 2023).
Figure 12. Forward Testing Algorithm (Jaddu and Biloko, 2023)
Furthermore, in future developments, we can consider combining these assets as a
portfolio for a more holistic strategy, although their actual correlation and combined
performance need to be thoroughly analyzed. Optimizing hyperparameters can be
approached in various ways, yet given sufficient time for tuning, we employed a
straightforward and effective method grid search. This method methodically explores all
possible combinations of hyperparameters, selecting the one with the highest validation
performance.
Collectively, combining sentiment analysis and VAEs for risk estimation with
LSTM for predicting future direction of prices is a robust methodological approach. It
blends the strengths of deep learning in processing sequential data with the nuanced
understanding of market sentiment, offering a comprehensive tool for market analysis.
These goals are directed towards creating an integrated machine learning framework that
not only predicts market movements but also assesses risks and considers market sentiment
to inform cryptocurrency trading decisions. This capstone project transcends theoretical
academic research and ventures into the creation of a practical, professional tool designed
to fortify the synergy between state-of-the-art computational methodologies and the elusive
nature of cryptocurrency trading.


### Page 20

WorldQuant University
2024
20
Appendix 1
The project GitHub Repository with Python Notebook is here


### Page 21

WorldQuant University
2024
21
Appendix
2


### Page 22

WorldQuant University
2024
22
Appendix
3


### Page 23

WorldQuant University
2024
23
Appendix 4


### Page 24

WorldQuant University
2024
24
Appendix 5


### Page 25

WorldQuant University
2024
25
Appendix 6


### Page 26

WorldQuant University
2024
26
Appendix 7


### Page 27

WorldQuant University
2024
27
References
1. McNally, Sean, Jason Roche, and Simon Caton. "Predicting the Price of
Bitcoin Using Machine Learning." 26th Euromicro International Conference
on Parallel, Distributed and Network-based Processing (PDP), March 2018,
pp. 339-343. IEEE, doi:10.1109/PDP2018.2018.00060.
2. Dixon, Matthew, Diego Klabjan, and Jin Hoon Bang. "Classification-based
Financial Markets Prediction using Deep Neural Networks." Algorithmic
Finance, vol. 6, no. 3-4, December 2017, pp. 67-77. IOS Press,
doi:10.3233/AF-170176.
3. Nsarang. "Stock Price Prediction Using Historical Patterns." GitHub,
https://github.com/nsarang/big-data-stock-price-forecast.git.
4. Koker, Thomas E., and Dimitrios Koutmos. "Cryptocurrency Trading Using
Machine Learning." Journal of Risk and Financial Management, vol. 13, no.
178, 2020, www.mdpi.com/journal/jrfm. DOI:10.3390/jrfm13080178.
5. Jiang, Tingsong, Andy Zeng. “Financial Sentiment Analysis using FinBERT
with
Application
in
Prediction
Stock
Movement.”
arXiv,
2023,
https://arxiv.org/abs/2306.02136
6. Zeng, Qingyun, and Tingsong Jiang. "Financial Sentiment Analysis using
FinBERT with Application in Prediction Stock Movement." arXiv (2023):
https://arxiv.org/abs/2306.02136.
7. Murray, Kate, et al. "On Forecasting Cryptocurrency Prices: A Comparison
of Machine Learning, Deep Learning, and Ensembles." Forecasting (2023):
https://doi.org/10.3390/forecast5010010.
8. Zhang, Zihao, Stefan Zohren, and Stephen Roberts. "DeepLOB: Deep
Convolutional Neural Networks for Limit Order Books." Journal of Latex
Class Files, vol. XX, no. XX, Jan. 2020, pp. 1-11.
9. Kolm, Petter N., Jeremy Turiel, and Nicholas Westray. "Deep Order Flow
Imbalance: Extracting Alpha at Multiple Horizons from the Limit Order
Book."
SSRN
Electronic
Journal,
2021,
SSRN:
3900141.
https://ssrn.com/abstract=3900141.
10. Jaddu, Koti S., and Paul A. Bilokon. "Combining Deep Learning on Order
Books with Reinforcement Learning for Profitable Trading." Preprint,
Department of Computing, Imperial College London, 13 September 2023.


### Page 28

WorldQuant University
2024
28
Author
Diana Gorsh,
https://www.linkedin.com/in/diana-gorsh/

# Prediction-based limit order trading

- **Source File**: `ssrn-4320775.pdf`
- **Total Pages**: 9
- **SSRN ID**: `ssrn-4320775`

---

## Page 1

Prediction-based limit order trading
Christopher Felder
University of Tübingen
Tübingen, Germany
christopher.felder@uni-tuebingen.de
Abstract—Managing the trade-off between volume and margin is
among the most fundamental challenges for dealers in a securities
market. We attempt to overcome this trade-off by incorporating
predictions for buyer- and seller-initiated trades when submitting
limit orders. Using the Avellaneda–Stoikov model as an exam-
ple, we show how dealers can adjust quotes to predictions and
thereby capture larger spreads at constant volume. Simulations
on historical limit order book data illustrate that our model allows
dealers to both increase market making revenues through trade
flow-optimized positioning in the order book and reduce adverse
selection cost through preempted adverse price movements.
Keywords—Sequence learning, Limit order trading, Avellaneda–
Stoikov model, Adverse price selection, Cryptocurrency.
JEL classification—C45, C53, C55, C63, D49, G17.
1 Introduction
Intuitively, dealers aim to repeatedly earn the ‘spread’ between
buy and sell prices by simultaneously buying and selling an asset
without accumulating a large net position. As a result, dealers face
a trade-off between trade volume and margin: Wide spreads lead
to high margins but less volume, while dealers with tight spreads
trade frequently but at unfavorable prices [31]. Additionally [34],
dealers face inventory risk arising from the stochastic behavior of
the net position [5], execution risk arising from limit orders not
being executed or only partially executed [36, 40], and adverse se-
lection risk arising from trading with informed traders [23]. Thus,
much of the literature has been concerned with the question of
whether there is an optimal strategy for posting limit orders [2].
Avellaneda and Stoikov [5] propose a stochastic optimal con-
trol model in which the dealer’s reservation price is a function
of the net position: When the dealer is long (short), the reserva-
tion price is below (above) the mid-price to incentivize execution
of sell (buy) orders and return to a neutral inventory, thereby al-
lowing the dealer to manage inventory risk. Numerous studies
[2, 6, 7, 9, 10, 12, 22, 31, 32, 34] discuss extensions of the model.
Like [5], most of these studies assume that market orders follow a
stochastic process. In contrast, [8, 17, 18, 39, 62, 63, 66, 67] present
evidence of mid-price predictability from the limit order book
(LOB). Moreover, [37] finds that high-frequency traders anticipate
specific order flow trends, while [22] shows that high-frequency
traders can improve their P&L with directional bets.
Motivated by these discussions, we introduce an approach to in-
tegrate trade flow forecasting into limit order trading. We model
buyer- and seller-initiated trades using a Recurrent Neural Net-
work (RNN) – a powerful sequence learner well-suited for model-
ing the high-frequency dynamics of an LOB [19] – that processes
LOB and trade data to predict average 24-hour percentile ranks of
buyer- and seller-initiated trade sizes during the next five seconds.
For example, a 90% prediction for buyer-initiated trades means
that the average buy trade size over the next five seconds is greater
than 90% of all buyer-initiated trades over the last 24 hours.
Using the Avellaneda–Stoikov model as an example, we ad-
just limit order prices to these predictions in two ways: First, if
our model predicts large (small) trades, we increase (decrease) the
depth of orders in the LOB, i.e., post orders deeper (closer) in the
LOB. For example, when predicting large buy orders and small sell
orders, we increase both the ask and bid price to maximize the po-
tentially captured spread on the ask side and increase the chance
of being consumed on the bid side. Second, we shift the reser-
vation price to protect against the anticipated price movement,
which we derive from the imbalance between the predictions for
buy and sell trade sizes. Hence, when anticipating a price increase
(decline), we shift the reservation price up (down) to protect from
being adversely selected by informed buyers (sellers) and partici-
pate in the price increase (decline) through long (short) exposure.
We test our model on historical LOBs of the BTC-USD and ETH-
USD pairs and arrive at the following findings: The RNN improves
prediction quality by about 40% over a standard feedforward neu-
ral network and performs best when previous trade flow is bal-
anced. Moreover, there is an empirical optimum of sensitivity to
predictions, which states that we should be twice as sensitive to
predictions when adjusting order depth to trade sizes than when
adjusting reservation price to adverse price movements. Our limit
order model significantly improves P&L over a wide range of test
periods compared to the Avellaneda–Stoikov model, e.g., by up to
7% for one-hour periods, but this improvement also comes with
higher risk and depends on market dynamics. As two main con-
tributors to the P&L, we identify higher market making revenues
due to larger spreads earned especially when the order book is
less liquid, and reduced adverse selection costs by preempting ad-
verse price movements, with the cost reduction being proportional
to the magnitude of the adverse price movement. Accordingly,
our model provides an effective approach to both overcoming the
trade-off between volume and margin and reducing adverse selec-
tion cost by taking trade flow forecasts into account when decid-
ing whether we can afford a wider spread to increase profitability.
2 High-frequency trading in a limit order book
A limit order is an order to buy or sell a specified amount of an as-
set at a specified price. If execution is not possible at the time of ar-
rival, the order queues in the LOB at the respective price level. The
LOB typically follows a price-time priority, with orders queued ac-
cording to their price level and arrival time. For more information
on LOBs, we refer to [1, 29]. A market order, in contrast, has no
price limit and serves impatient traders by instantaneous execu-
tion against open orders in the LOB, starting with the best price
level and, if necessary, continuing with subsequent price levels
until the total order volume has been matched. The objective of
dealers is to provide liquidity to the market by continuously of-
fering buy and sell prices through the LOB without accumulating
large net positions [47]. The prices offered therefore should take
into account a dealer’s net position: Symmetrically placing orders,
e.g., at the top of the order book, risks adverse selection, as down-
ward or upward trends could lead to a disproportionate number
of filled buy or sell orders, respectively, resulting in a large net po-
sition that the dealer would have to offset at unfavorable prices.
A common approach in the literature for determining a dealer’s
optimal buy and sell price is to treat market making as a stochas-
tic optimal control problem introduced by [38], who analyzes the
optimal price of a single stock for a monopolistic dealer. Avel-
laneda and Stoikov [5] extend this approach and formulate the
1
Electronic copy available at: https://ssrn.com/abstract=4320775


## Page 2

problem mathematically for a dealer who optimizes the expected
utility of the terminal profit. Consistent with empirical indications
[24, 28, 46, 50, 64], the authors assume that market order flow fol-
lows a Poisson process with rate 𝐴𝑒−𝜅𝛿, where 𝛿is the distance
between order price and mid-price, and 𝐴and 𝜅represent order
book liquidity. The authors derive the indifference or reservation
price 𝑟𝐴𝑆and the optimal bid-ask spread 𝛿𝑎+ 𝛿𝑏as
𝑟𝐴𝑆= 𝑠−𝑞𝛾𝜎2 (𝑇−𝑡)
(1)
𝛿𝑎+ 𝛿𝑏= 𝛾𝜎2 (𝑇−𝑡) + 2
𝛾ln

1 + 𝛾
𝜅

(2)
where 𝑠denotes the mid-price, 𝑞depicts the inventory net posi-
tion, 𝜎is the standard deviation of the mid-price, 𝛾is an inven-
tory risk aversion parameter, and ‘𝐴𝑆’ indicates the Avellaneda–
Stoikov model. The optimal ask price is𝑟𝑎
𝐴𝑆= 𝑟𝐴𝑆+(𝛿𝑎+𝛿𝑏)/2 and
the optimal bid price is 𝑟𝑏
𝐴𝑆= 𝑟𝐴𝑆−(𝛿𝑎+𝛿𝑏)/2. Close to terminal,
𝛿𝑎+ 𝛿𝑏converges towards 2/𝛾ln(1 +𝛾/𝜅) and becomes symmet-
rical to the mid-price, increasing the dealer’s chance of finishing
with a zero net position. The ask and bid order’s depth in the order
book is 𝛿𝑎
𝐴𝑆= 𝑟𝑎
𝐴𝑆−𝑠and 𝛿𝑏
𝐴𝑆= 𝑠−𝑟𝑏
𝐴𝑆, respectively.
A large literature discusses extensions of the Avellaneda–
Stoikov model [2, 6, 7, 9, 10, 12, 22, 31, 32, 34]. Studies focus-
ing on re-modeling the market order flow include [2, 22], both
of which, inline with [13], replace the Brownian process with a
mean-reverting process, and [7], who considers the liquidation
problem and models order arrivals as a function of the liquida-
tion price. More recently, reinforcement learning has led to im-
provements over stochastic optimal control formulations – see
[25, 26, 33, 43, 56, 60]. On the question of whether market order
flow is stochastic, numerous studies examine the relationship be-
tween LOBs and price discovery. Yet, [18] acknowledges that there
is “no consensus on the extent to which LOBs convey predictive
information”. While [27] and [58] argue that limit orders are not
informative, [8, 17, 18, 39, 62, 63, 66, 67] state that LOBs contain
predictive information. For more studies, we refer to the survey of
[65]. [42] uses sentiment predictions from LOBs and market news
for limit order trading, whereas [35] implements price predictions
into a reinforcement learning-based limit order model.
3 Data
[56] outlines that cryptocurrency exchanges “represent a well-
suited test environment” for limit order trading models, as – in
contrast to global stock exchanges – data are easily and free
to access and “major cryptocurrency exchanges operate like es-
tablished limit order exchanges and exhibit very similar stylized
facts” [45, 57]. As one of the most liquid centralized cryptocur-
rency exchanges with more than 100 million traders [16], Coin-
base is therefore a suitable example to test our limit order model.
Accordingly, we focus on the two most liquid pairs, ‘BTC-USD’
and ‘ETH-USD’.
Since tick-level data from Coinbase is not downloadable, we
record LOB and trade messages between 2022-08-16 05:37:27 UTC
and 2022-10-05 16:07:40 UTC via WebSocket using cbpro [49], the
Python client for the Coinbase Pro API. We receive batches of
level-2 messages every 50 milliseconds through the level2_batch
channel and price updates on each match through the ticker
channel. After recording, we replay the messages to reconstruct
LOBs and trade flows, aggregate both data sets into one-second
intervals and cut the LOBs behind the top 50 price levels on each
side of the book. To obtain comparable results between the two
pairs, we index all prices at 100 with the first recorded price.
For the split into training, validation and test periods, we fol-
low the reasoning of [21] and use 𝑛-fold cross validation that di-
vides the entire period into 𝑛equal-sized sub-intervals, for each
of which we train independent models. We choose an overlap-
ping split of five days in length, of which the first three days are
for training (60%), the fourth day is for validation (20%), and the
last day is for test (20%). The overlap is four days, i.e., we shift
the sub-intervals by one day, yielding a total of 45 sub-intervals,
allowing us to test each day once with an independent model.
4 High-frequency trade flow prediction
4.1 24-hour trade size percentile ranks
We model buyer- and seller-initiated trade flows using the per-
centile ranks of trade sizes in the frequency distribution of all trade
sizes over the past 24 hours. We calculate the 24-hour percentile
rank 𝑅of a trade size as the share of trade sizes that are less than
that trade size, indicating whether the trade tends to be large or
small relative to other trades from the previous 24 hours. Thus, 𝑅
is defined in the range [0, 1], with 𝑅> 0.5 (𝑅< 0.5) indicating a
relatively large (small) trade. Considering the differences between
bid and ask market order flow, we calculate percentile ranks sep-
arately for buyer-initiated trades (𝑅𝑏) and seller-initiated trades
(𝑅𝑎). For example, if a buyer-initiated trade about 1.5 BTC has a
percentile rank of 𝑅𝑏= 0.90, this means that 90% of all buyer-
initiated trades over the past 24 hours are smaller than 1.5 BTC.
To obtain comparable results across all sub-intervals, we calculate
percentile ranks prior to separating training, validation and test
periods. Figure 5 illustrates that, although we calculate percentiles
based on sequences along the time axis, the percentile ranks are
evenly distributed across test periods.
Together, 𝑅𝑏and 𝑅𝑎convey two pieces of information: First, 𝑅𝑏
and 𝑅𝑎indicate whether trades are more likely to consume one or
multiple price levels. Figure 14 in the Appendix illustrates that
trades with a low (high) trade size percentile rank consume one
(multiple) price level(s), e.g., trade sizes with 𝑅= 90% consume
five price levels on average. Second, the difference between 𝑅𝑏and
𝑅𝑎indicates the imbalance between the buyer- and seller-initiated
trade flow. For example, a small 𝑅𝑏combined with a large 𝑅𝑎may
represent a sell surplus. In contrast to the widely used definition
[3, 59], we follow [54] and define the trade flow imbalance 𝑇𝐹𝐼in
the range [−1, 1] by (𝑅𝑏−𝑅𝑎)/(𝑅𝑏+𝑅𝑎), where𝑇𝐹𝐼< 0 (𝑇𝐹𝐼> 0)
indicates a sell (buy) surplus. Consistent with [15, 59], we consider
𝑇𝐹𝐼as an approximation of the price movement, with 𝑇𝐹𝐼> 0
(𝑇𝐹𝐼< 0) indicating a price increase (decline).
4.2 Sequence learning for limit order trading
We present a limit order trading model that adjusts buy and sell
prices according to the predicted 24-hour percentile rank of future
seller- and buyer-initiated trade sizes. The prediction task is a re-
gression task with 𝑅𝑏and 𝑅𝑎as target variables. As [59] shows
that trade flow imbalance is auto-correlated and [18] states that
high-frequency price “increments are neither independent nor sta-
tionary and depend on the state of the order book”, we assume that
the observations of 𝑅𝑏and 𝑅𝑎, respectively, are auto-correlated
and not i.i.d. Hence, we define our prediction task as a sequence
prediction model that uses lagged values of 𝑅𝑏and 𝑅𝑎sequences
to predict subsequent values of that sequences. A sequence learner
proven successful in modeling high-frequency dynamics is the
RNN [19]. While some researchers [63, 66] prefer Long Short-
term Memories (LSTM) over RNNs, [19] outlines that for high-
frequency LOB modeling, “short-term memory is adequate”, i.e.,
the auto-correlation lowers for larger lags and the vanishing gra-
dient problem of RNNs [53] is not an issue, and hypothesizes that
“there is little to no benefit in using an LSTM”.
Introduced by [52], the RNN is an artificial neural network
architecture capable to extract temporally encoded information
from time-series data by using feedback connections between neu-
rons. A hidden state transfers information contained in cell out-
2
Electronic copy available at: https://ssrn.com/abstract=4320775


## Page 3

puts across time steps and facilitates connection of information
between time steps, thereby allowing past information to persist.
The output of an RNN cell at time 𝑡is the vector of hidden states
ℎ𝑡. At each time step 𝑡, the cell processes both ℎ𝑡−1 and the vector
of current elements of the input sequence, 𝑥𝑡, to generate the new
hidden state ℎ𝑡= 𝑡𝑎𝑛ℎ(𝑤𝑥𝑥𝑡+ 𝑤ℎℎ𝑡−1 + 𝑏ℎ) through a 𝑡𝑎𝑛ℎacti-
vation function, where 𝑤𝑥(𝑤ℎ) is a vector of weights determining
which elements of 𝑥𝑡(ℎ𝑡−1) to keep and which to remove. This
procedure ensures that the network considers important knowl-
edge acquired in previous time steps when processing new infor-
mation. The model output at time 𝑡is 𝑦𝑡= 𝑤𝑦ℎ𝑡+𝑏𝑦. In our case,
𝑦𝑡is a vector containing ˆ𝑅𝑏
𝑡and ˆ𝑅𝑎
𝑡.
4.3 Predictors of trade flow
Besides the sequences of 𝑅𝑏
𝑡and 𝑅𝑎
𝑡, we additionally include se-
quences of predictors proposed by the price prediction literature:
First, we include the price level distance, which is the distance of
each of the 10 best price levels on both sides of the order book
from the mid-price, expressed as a percentage of the mid-price
[63]. Second, we include the cumulative depth size, which reports
the cumulative sum of open limit order sizes at each of the 10 best
price levels [63]. Both variables yield a vector of 20 unique val-
ues for each time step. Third, we include the order flow imbalance
𝑂𝐹𝐼[17, 48], which we calculate as the difference between the cu-
mulative bid and ask size at the tenth price levels on each side,
divided by their sum [11]. For example, if the cumulative size at
the 10th price level on the bid side is 5 ETH and on the ask side
4 ETH, it is 𝑂𝐹𝐼= (5 −4)/(5 + 4) = 0.11. Finally, we include
the percentage change in the mid-price [63, 65] and the distance
between the highest and lowest trade price of all matches within
each one-second interval [65].
In total, given that we process 𝑛observations per batch, each
time step includes five predictors with shape 𝑛×1 and two predic-
tors with shape 𝑛× 20, i.e., we process 45 predictors per time step.
Motivated by [18] who chooses a sequence length of 10 for tick-
level data, we use a sequence length of 10 seconds, i.e., we provide
ten lags to our model in order to deliver a prediction. The final
vector of input variables thus has shape 𝑛×45×10. Prior to train-
ing, we standardize the input data by subtracting the mean and
dividing by the standard deviation across all sub-intervals [41].
4.4 Network configuration
We use a three-layer network architecture with two visible lay-
ers and one hidden layer. The number of units in the first and
last layer equals the dimension of the vector of input and output
variables, respectively. The activation function for the two output
units is the sigmoid function, which squashes predictions into the
range [0, 1], corresponding to the range for which 𝑅𝑏and 𝑅𝑎are
defined. Determining the number of units in the hidden layer is
not as straightforward. Out of architectures with 16, 32, 64, 128,
and 256 hidden units, we choose 64 hidden units, resulting in the
lowest mean squared prediction error for the validation sets. As
activation function we select 𝑡𝑎𝑛ℎ, scaling values between [−1, 1]
and thereby avoiding dropping information by scaling towards 0.
Each training step, we minimize the mean squared prediction
error, a loss function suited for regression problems in modeling
high-frequency dynamics [20], across batches of 8 random sam-
ples using the stochastic gradient descent [30, 51] with an initial
learning rate of 0.01. We regularize training in multiple ways:
First, we consider a stateless RNN, i.e., memory does not transfer
between sequences of different batches and persist for one batch.
Second, we shuffle samples within batches. Third, we apply 20%
dropout [61] to the input layer and, as proposed by [30], the non-
recurrent connections in the hidden layer. Finally, we use early
stopping and halt training when there has been no improvement
for the validation set for two epochs.
5 Prediction-based limit order trading
5.1 Prediction-based order depth
We propose order depth as a function of the predicted trade size
percentile ranks, ˆ𝑅𝑏and ˆ𝑅𝑎. Assumed that we make predictions
one period ahead and use these predictions to adjust 𝑟𝑎
𝐴𝑆and 𝑟𝑏
𝐴𝑆,
respectively, the function should fulfill two requirements: First,
if ˆ𝑅𝑏< 0.5 ( ˆ𝑅𝑎< 0.5), i.e., predicting small buy (sell) orders,
we should post sell (buy) orders closer to the top of the book
to increase the hit probability, whereas if 𝑅𝑏> 0.5 (𝑅𝑎> 0.5),
we should post sell (buy) orders deeper in the book to maxi-
mize the captured spread. Second, the spread adjustment should
be proportional to the percentile rank, i.e., the adjustment for
ˆ𝑅𝑏= 0.9 should be larger than that for ˆ𝑅𝑏= 0.6. Based on the
the Avellaneda–Stoikov model, we define the spread-adjusted ask
price 𝑟𝑎
𝑆𝑃and the spread-adjusted bid price 𝑟𝑏
𝑆𝑃by
𝑟𝑎
𝑆𝑃= 𝑟𝐴𝑆+ 1
2

1 + 1
𝛼1

2 ˆ𝑅𝑏−1
 
𝛿𝑎+ 𝛿𝑏
(3)
𝑟𝑏
𝑆𝑃= 𝑟𝐴𝑆−1
2

1 + 1
𝛼1

2 ˆ𝑅𝑎−1
 
𝛿𝑎+ 𝛿𝑏
(4)
where 𝛼1 ≥0 is a scaling parameter that determines how sensitive
order depth is to predicted percentile ranks, i.e., by how much we
widen or tighten the spread in response to a prediction. As equa-
tion (3) can be rewritten as 𝑟𝑎
𝑆𝑃= 𝑟𝑎
𝐴𝑆+ (𝛿𝑎+ 𝛿𝑏)(2 ˆ𝑅𝑏−1)/(2𝛼1),
we simply add a weighted version of 𝛿𝑎+ 𝛿𝑏to 𝑟𝑎
𝐴𝑆. The terms
(2 ˆ𝑅𝑏−1)/𝛼1 and (2 ˆ𝑅𝑎−1)/𝛼1 are positive for ˆ𝑅𝑏> 0.5 and
ˆ𝑅𝑎> 0.5 as we wish to post orders deeper in the LOB, zero for
ˆ𝑅𝑏= 0.5 and ˆ𝑅𝑎= 0.5 as predicted orders are neither large
nor small and we are indifferent between widening or tighten-
ing spreads, and negative for ˆ𝑅𝑏< 0.5 and ˆ𝑅𝑎< 0.5 as we
wish to narrow the spread. For 𝛼1 = 1, the terms are defined in
the range [−1, 1], implying that the maximum spread adjustment
( ˆ𝑅𝑏, ˆ𝑅𝑎= 1) is 𝑟𝑎
𝑆𝑃−𝑟𝑎
𝐴𝑆= (𝛿𝑎+𝛿𝑏)/2 and 𝑟𝑏
𝐴𝑆−𝑟𝑏
𝑆𝑃= (𝛿𝑎+𝛿𝑏)/2,
i.e., the order’s depth in the order book is twice the depth given by
the Avellaneda–Stoikov model, and the minimum spread adjust-
ment ( ˆ𝑅𝑏, ˆ𝑅𝑎= 0) is 𝑟𝑎
𝑆𝑃−𝑟𝑎
𝐴𝑆= −(𝛿𝑎+ 𝛿𝑏)/2 and 𝑟𝑏
𝐴𝑆−𝑟𝑏
𝑆𝑃=
−(𝛿𝑎+𝛿𝑏)/2, i.e., 𝑟𝑎
𝑆𝑃,𝑟𝑏
𝑆𝑃= 𝑟𝐴𝑆. Smaller (larger) values for 𝛼1 are
associated with more (less) impact of predictions on the depth.
Figure 1 illustrates 𝑟𝑎
𝑆𝑃−𝑟𝑎
𝐴𝑆(left) and 𝑟𝑏
𝑆𝑃−𝑟𝑏
𝐴𝑆(right) as func-
tions of 𝛼1 and ˆ𝑅𝑏and ˆ𝑅𝑎, respectively. For illustration purposes,
we set 𝑠= 100, 𝛾= 0.25, 𝜎= 0.3, 𝑇= 1, 𝑡= 0.3, 𝜅= 2, 𝑞= 0.
Both charts emphasize that small (large) values for 𝛼1 are associ-
ated with strong (little) changes to the quotes as order depth reacts
more (less) strongly to predictions. If ˆ𝑅𝑏> 0.5, we increase the
ask price to exploit a larger spread from arriving large buy orders,
and lower the ask price if ˆ𝑅𝑏< 0.5 to increase the chance of being
consumed by small buy orders. Correspondingly, we decrease the
bid price if ˆ𝑅𝑎> 0.5 and increase it if ˆ𝑅𝑎< 0.5. One may interpret
our extension as a way to reduce adverse selection cost: Informed
trades typically are larger than uninformed trades [14, 44]. By
increasing spreads when predicting large orders, we potentially
protect against adverse selection by informed traders [55].
5.2 Prediction-based reservation price
Adverse price selection occurs when better informed traders pick
off our limit orders on one side of the order book [9], resulting in
an adverse price movement for our limit orders on the other side,
which now queue away from the inside market. Following [18],
one approach “potentially reducing the likelihood of adverse price
movement” between the fill of a sell and a buy order is predicting
price movements, thereby preempting unfavorable execution of
orders. For example, [9] simulates an informed dealer using a hid-
den Markov model and reports reduced adverse selection costs.
We propose the reservation price as a function of the predicted
trade flow imbalance, d
𝑇𝐹𝐼, given by d
𝑇𝐹𝐼= ( ˆ𝑅𝑏−ˆ𝑅𝑎)/( ˆ𝑅𝑏+ ˆ𝑅𝑎).
3
Electronic copy available at: https://ssrn.com/abstract=4320775


## Page 4

α1
0.40.60.81.01.2 1.4
ˆRb
0.0 0.2 0.4 0.6 0.8 1.0
ra
SP −ra
AS
−1
0
1
α1
0.4
0.6
0.8
1.0
1.2
1.4
ˆRa
0.0
0.2
0.4
0.6
0.8
1.0
rb
SP −rb
AS
−1
0
1
−1
0
1
Figure 1: Prediction-based spread adjustments
This function should fulfill two requirements: First, if d
𝑇𝐹𝐼> 0,
we should increase the reservation price in order to avoid adverse
filling of sell orders and incentivize long exposure for participating
in the price increase, whereas if d
𝑇𝐹𝐼< 0, we should decrease the
reservation price for avoiding adverse filling of buy orders and
incentivize short exposure. Second, considering our net position,
these directional adjustments should be allowed to contradict with
the Avellaneda–Stoikov model, i.e., if we predict a price increase
(decline), we should be able to use a reservation price greater (less)
than 𝑟𝐴𝑆even if we are long (short). We define the directional
forecast-adjusted reservation price 𝑟𝐷𝐹by
𝑟𝐷𝐹= 𝑠+

𝑠𝑔𝑛(𝑞) 1
𝛼2
d
𝑇𝐹𝐼−1

𝑞𝛾𝜎2 (𝑇−𝑡)
(5)
where𝑠𝑔𝑛(𝑞) is the signum function of𝑞and𝛼2 ≥0 measures how
sensitive the reservation price is to a prediction. Rewriting equa-
tion (5) as 𝑟𝐷𝐹= 𝑟𝐴𝑆+𝑠𝑔𝑛(𝑞)(d
𝑇𝐹𝐼/𝛼2)𝑞𝛾𝜎2(𝑇−𝑡) illustrates that
we simply add or subtract a weighted version of the Avellaneda–
Stoikov correction term 𝑞𝛾𝜎2(𝑇−𝑡). For 𝛼2 = 1 and 𝑞> 0, the
maximum adjustment (d
𝑇𝐹𝐼= 1) is 𝑟𝐷𝐹−𝑠= 0, i.e., we neutralize
the Avellaneda–Stoikov correction, and the minimum adjustment
(d
𝑇𝐹𝐼= −1) is 𝑟𝐷𝐹−𝑠= 2 (𝑟𝐴𝑆−𝑠), i.e., we double the distance to
the mid-price. Smaller (larger) values for 𝛼2 imply a higher (lower)
price sensitivity to d
𝑇𝐹𝐼. For instance, if d
𝑇𝐹𝐼= 0.25, the price ad-
justment is 2𝑞𝛾𝜎2(𝑇−𝑡) for 𝛼2 = 0.5 and 0.5𝑞𝛾𝜎2(𝑇−𝑡) for 𝛼2 = 2.
Figure 2 illustrates the difference between 𝑟𝐷𝐹and 𝑟𝐴𝑆for val-
ues in the range𝑞= [−2, 2] and d
𝑇𝐹𝐼= [−1, 1] with 𝛼2 = 1, 𝑠= 100,
𝛾= 0.25, 𝜎= 0.3, 𝑇= 1, 𝑡= 0.3, 𝜅= 2. If predicting a sell surplus,
it is 𝑟𝐷𝐹< 𝑟𝐴𝑆, either contradicting (𝑞< 0) or reinforcing (𝑞> 0)
the Avellaneda–Stoikov correction. Analogous, if predicting a buy
surplus, it is 𝑟𝐷𝐹> 𝑟𝐴𝑆, either contradicting (𝑞> 0) or reinforc-
ing (𝑞< 0) the Avellaneda–Stoikov correction. The directional
forecast-adjusted ask and bid quote is 𝑟𝑎
𝐷𝐹= 𝑟𝐷𝐹+ (𝛿𝑎+𝛿𝑏)/2 and
𝑟𝑏
𝐷𝐹= 𝑟𝐷𝐹−(𝛿𝑎+ 𝛿𝑏)/2, respectively.
5.3 Consolidated prediction-based limit order model
Finally, we combine both 𝐷𝐹and 𝑆𝑃models to one consolidated
limit order model that considers 𝑟𝐷𝐹as reservation price and de-
termines bid and ask quotes based on equations (3) and (4) with
q
−2
−1
0
1
2
d
TFI
−1.0 −0.5 0.0 0.5 1.0
rDF −rAS
−0.03
−0.02
−0.01
0.00
0.01
0.02
0.03
−0.02
−0.01
0.00
0.01
0.02
Figure 2: Prediction-based reservation price adjustments
replacing 𝑟𝐴𝑆by 𝑟𝐷𝐹. As a result, the consolidated ask price is
𝑟𝑎
𝑆𝑃𝐷𝐹= 𝑟𝐷𝐹+ (1 + (2b𝑅𝑏−1)/𝛼1)(𝛿𝑎+𝛿𝑏)/2 and the consolidated
bid price is 𝑟𝑏
𝑆𝑃𝐷𝐹= 𝑟𝐷𝐹−(1 + (2b𝑅𝑎−1)/𝛼1)(𝛿𝑎+ 𝛿𝑏)/2.
One might wonder how 𝐷𝐹and 𝑆𝑃relate to each other and
whether 𝐷𝐹and 𝑆𝑃adjustments to 𝐴𝑆quotes would offset each
other in the consolidated model. To understand their relationship,
we compare the absolute difference between 𝑆𝑃𝐷𝐹quotes and 𝐴𝑆
quotes (e.g., |𝑟𝑎
𝑆𝑃𝐷𝐹−𝑟𝑎
𝐴𝑆|) with the absolute difference between
𝑆𝑃or 𝐷𝐹quotes and 𝐴𝑆quotes (e.g., |𝑟𝑎
𝐷𝐹−𝑟𝑎
𝐴𝑆| or |𝑟𝑎
𝑆𝑃−𝑟𝑎
𝐴𝑆|). By
using absolute differences, we take into account that 𝑆𝑃or 𝐷𝐹cor-
rections occur in both directions, either increasing or decreasing
𝐴𝑆quotes, which allows us to summarize the comparison in four
cases represented by inequations (6)–(9). For instance, if inequa-
tion (6) is true, this means that 𝑆𝑃𝐷𝐹does not offset or reinforces
the 𝐷𝐹adjustment, whereas if it is false, this means that the 𝑆𝑃𝐷𝐹
adjustment to 𝐴𝑆is less than the 𝐷𝐹adjustment, i.e., 𝑆𝑃𝐷𝐹con-
tradicts 𝐷𝐹and neutralizes (parts of) the 𝐷𝐹adjustment.
|𝑟𝑎
𝑆𝑃𝐷𝐹−𝑟𝑎
𝐴𝑆| ≥|𝑟𝑎
𝐷𝐹−𝑟𝑎
𝐴𝑆|
(6)
|𝑟𝑏
𝑆𝑃𝐷𝐹−𝑟𝑏
𝐴𝑆| ≥|𝑟𝑏
𝐷𝐹−𝑟𝑏
𝐴𝑆|
(7)
|𝑟𝑎
𝑆𝑃𝐷𝐹−𝑟𝑎
𝐴𝑆| ≥|𝑟𝑎
𝑆𝑃−𝑟𝑎
𝐴𝑆|
(8)
|𝑟𝑏
𝑆𝑃𝐷𝐹−𝑟𝑏
𝐴𝑆| ≥|𝑟𝑏
𝑆𝑃−𝑟𝑏
𝐴𝑆|
(9)
With regard to 𝐷𝐹strategy, we find that inequation (6) is true if
ˆ𝑅𝑏≥ˆ𝑅𝑎and ˆ𝑅𝑏≥0.5 or if ˆ𝑅𝑏≤ˆ𝑅𝑎and ˆ𝑅𝑏≤0.5, and inequation
(7) is true if ˆ𝑅𝑏≥ˆ𝑅𝑎and ˆ𝑅𝑎≤0.5 or if ˆ𝑅𝑏≤ˆ𝑅𝑎and ˆ𝑅𝑎≥
0.5. For instance, when 𝐷𝐹shifts the reservation price upward
( ˆ𝑅𝑏≥ˆ𝑅𝑎), 𝑆𝑃does so as well if buy orders are relatively large
( ˆ𝑅𝑏≥0.5) or sell orders are relatively small ( ˆ𝑅𝑎≤0.5). Thus,
if predicting a buy surplus, we increase the reservation price to
protect from being adversely selected by informed buyers, thereby
implicitly increasing (decreasing) the depth of buy (sell) orders in
the LOB. This does not hold if the predicted buy surplus is based
on a relatively small buy volume, as in that case, we choose a closer
spread to increase the chance of being consumed by small orders.
With regard to 𝑆𝑃strategy, we find that, analogous to 𝐷𝐹strat-
egy, inequation (8) is true if ˆ𝑅𝑏≥ˆ𝑅𝑎and ˆ𝑅𝑏≥0.5 or if ˆ𝑅𝑏≤ˆ𝑅𝑎
and ˆ𝑅𝑏≤0.5, and, inequation (9) is true if ˆ𝑅𝑏≥ˆ𝑅𝑎and ˆ𝑅𝑎< 0.5 or
if ˆ𝑅𝑏≤ˆ𝑅𝑎and ˆ𝑅𝑎≥0.5. If predicting large sell orders ( ˆ𝑅𝑎≥0.5)
and a sell surplus ( ˆ𝑅𝑏≤ˆ𝑅𝑎), we post buy orders deeper in the book
to maximize the captured spread, thereby implicitly lowering the
mid-point between ask and price, which is consistent with lower-
ing the reservation in response to the sell surplus. If predicting a
buy surplus instead, the 𝐷𝐹adjustment would contradict the 𝑆𝑃
adjustment in response to ˆ𝑅𝑎≥0.5.
5.4 Trading model
We propose a limit order trading model in which we predict the
five-second averages of 𝑅𝑎and 𝑅𝑏, use these predictions to de-
termine bid and ask price, and then simultaneously place a cor-
responding buy order and a corresponding sell order. After five
4
Electronic copy available at: https://ssrn.com/abstract=4320775


## Page 5

seconds, the orders have either been filled by incoming market
orders or we cancel them and submit new orders. Even if both or-
ders get filled in less than five seconds, we still wait five seconds
before submitting new orders. As target variables we consider the
equal-weighted averages of all five values in the five-second in-
tervals of 𝑅𝑏and 𝑅𝑎, respectively, while keeping the predictors in
one-second granularity.
We follow [31] and base our trading model on several assump-
tions: First, the money market pays no interest and we can cancel
and submit orders for free [5]. Second, there is no latency [34],
which is a rather minor condition since we consider five-second
intervals. Finally, our limit orders have no effect on the market
[5, 12, 22, 60]. This is a realistic assumption as we model highly
liquid currency pairs [66] and order sizes that are small compared
to the total amount traded in the market [60]. Besides, we assume
constant risk aversion 𝛾= 0.5 and order book density 𝜅= 2, and
compute 𝜎over 24-hour windows, corresponding to 𝑅𝑏and 𝑅𝑎.
The size per order is 0.1 BTC and 0.1 ETH and the maximum net
position is ±0.5 BTC and ±0.5 ETH, respectively. Once reached
the inventory limit, we stop posting on the respective side until
the net position is less than 0.5. We trade BTC and ETH simulta-
neously, with hedging of positions between BTC and ETH being
not allowed, and calculate P&L following [5] separately for each
currency pair. In the following sections, we report P&L as equally
weighted average of both currency pairs. Since we use indexed
prices, P&L does not represent currency units.
Due to the LOB’s aggregate form, we have no access the time
queue at a particular price level. While we can separate new from
waiting orders based on trade history, if the size at a price level
decreases without a trade at that time, we cannot identify which
orders were cancelled. We follow [60] and assume that the prob-
ability that the canceled order is ahead our order is proportional
to the volume ahead compared to the volume behind our order.
Any increase (resp. decrease) in volume at a particular price level
that is not related to a trade will queue behind our order (resp. be
evenly distributed among the orders before and after our order).
5.5 Empirical calibration of 𝛼1 and 𝛼2
As we have historical data, we can empirically determine which
values of 𝛼1 and 𝛼2 would have been P&L-optimal. For this cali-
bration, we assume to have full knowledge of the future and de-
termine quotes according to the realized 𝑅𝑏and 𝑅𝑎. Figure 3 illus-
trates the average one-hour P&L (solid lines with markers), i.e.,
the average P&L at the end of each hour, and the execution rate
ExR (dashed lines), i.e., the share of executions in all submissions,
achieved by 𝑆𝑃as a function of 𝛼1 (red) and achieved by 𝐷𝐹as a
function of 𝛼2 (green). The blue lines represent the 𝐴𝑆benchmark.
0.2
0.4
0.6
0.8
1.0
1.2
1.4
α1, α2
7.5
8.0
8.5
9.0
9.5
10.0
10.5
P&L
P&LAS
P&LSP
P&LDF
0.54
0.56
0.58
0.60
0.62
Execution rate (ExR)
ExRAS
ExRSP
ExRDF
Figure 3: One-hour P&L and ExR as functions of 𝛼1 and 𝛼2
α1
0.3 0.6 0.9 1.2 1.5 1.8
α2
0.6 0.9 1.2 1.5 1.8
P&LSPDF
9.5
10.0
10.5
11.0
9.5
10.0
10.5
11.0
Figure 4: 𝑆𝑃𝐷𝐹one-hour P&L as a function of 𝛼1 and 𝛼2
We find that P&L𝑆𝑃and P&L𝐷𝐹have their optima for 𝛼1 < 1
and 𝛼2 < 1, respectively, indicating relatively high sensitivity to
predictions. For very small 𝛼1 and 𝛼2, 𝑆𝑃and 𝐷𝐹are little prof-
itable as orders get filled rarely. For 𝛼1, 𝛼2 < 1, 𝑆𝑃and 𝐷𝐹outper-
form 𝐴𝑆despite less order executions, suggesting larger spreads
earned or reduced adverse selection cost. The optimal calibration
for 𝑆𝑃is 𝛼1 = 0.5, resulting in 35% P&L improvement over 𝐴𝑆, and
for 𝐷𝐹it is 𝛼2 = 0.9, resulting in 10% P&L improvement.
Figure 4 illustrates the average one-hour P&L achieved by𝑆𝑃𝐷𝐹
as a function of 𝛼1 and 𝛼2. Similar to Figure 3, P&L is the lowest
for large and very small values of 𝛼1 and 𝛼2, and has its maximum
for the combination of 𝛼1 = 0.55 and 𝛼2 = 1.00, improving P&L
by more than 40%. This calibration is similar to the stand-alone
strategies 𝑆𝑃and 𝐷𝐹, requiring us to be about twice as sensitive
to predictions when adjusting order depth to trade flow than when
adjusting the reservation price to adverse price movements.
6 Trading simulation with order predictions
6.1 Prediction quality
We analyze prediction quality benchmarked against a single-layer
feedforward neural network (SFN), which directly maps the inputs
to 𝑅𝑏and 𝑅𝑎. Figure 5 illustrates the frequency distribution of
ˆ𝑅𝑏(dashed) and ˆ𝑅𝑎(solid) over all test periods. The gray lines
focus on 𝑅𝑏and 𝑅𝑎. Regarding the distribution of 𝑅𝑏and 𝑅𝑎, RNN
apparently captures the true case better than SFN by achieving
a stretched and rather flat predictions distribution. Both models
predict very large and small values poorly, with substantially less
(RNN) or hardly any (SFN) predictions in the upper and lower 10%.
Table 1 reports average prediction errors across all test periods
aggregated by prediction error sign (‘Sign’). Sign group ‘−’ (‘+’)
includes all negative (positive) prediction errors. We calculate pre-
diction errors by ˆ𝑅𝑏−𝑅𝑏and ˆ𝑅𝑎−𝑅𝑎, respectively. Throughout
all groups, RNN shows smaller prediction errors than SFN. For
instance, if overpredicting percentile ranks, SFN ranks buy trades
on average 23 percentile ranks too high, whereas RNN ranks them
on average 14 ranks too high, suggesting an improvement by 40%.
The mean squared error of RNN is less than half of the SFN model.
Next, we investigate whether prediction quality depends on
0.2
0.4
0.6
0.8
ˆRb, ˆRa, Rb, Ra
0
200
400
600
800
Frequency
ˆRb (RNN)
ˆRa (RNN)
ˆRb (SFN)
ˆRa (SFN)
Rb
Ra
Figure 5: Frequency distribution of true and predicted values
5
Electronic copy available at: https://ssrn.com/abstract=4320775


## Page 6

Side
b𝑅𝑏
b𝑅𝑎
Sign
−
+
All
−
+
All
Average prediction error
RNN
−0.14
0.14
−0.00
−0.14
0.14
−0.00
SFN
−0.22
0.23
0.01
−0.22
0.22
0.00
Mean squared error (%)
RNN
3.78
3.78
3.78
3.83
3.80
3.82
SFN
6.96
7.21
7.09
7.14
7.04
7.09
Table 1: Prediction error metrics
market sentiment. Analogous to the sequence length, we group
the last ten seconds before a prediction into two equal-sized in-
tervals, where the first (second) interval 𝑇𝐹𝐼1−5 (𝑇𝐹𝐼6−10) repre-
sents the aggregated 𝑇𝐹𝐼of the first (last) five seconds. Figure 6
shows the mean squared error as a function of𝑇𝐹𝐼1−5 and𝑇𝐹𝐼6−10
for RNN and SFN predictions. Prediction models perform well
when the preceding flow of buy and sell market orders is rela-
tively balanced, and poorly when there is an excess of buyer- or
seller-initiated trades. This behavior is less pronounced for RNN
model than for SFN predictions, indicating that RNN outperforms
SFN when making predictions based on imbalanced trade flows.
6.2 Trading performance
We conduct trading simulations separately for 𝑆𝑃, 𝐷𝐹and 𝑆𝑃𝐷𝐹,
once based on RNN and once based on SFN predictions. Table 2
presents the equal-weighted average of cumulative P&Ls achieved
within non-overlapping periods of 1 minute (min) to 12 hours (h).
In the majority of periods, prediction-based strategies lead to an
improvement over 𝐴𝑆, e.g., we improve one-hour P&L by up to
7%. We also perform t-tests between the P&L distributions of
prediction-based strategies and that of 𝐴𝑆strategy and find that
increases in P&L are statistically significant in most cases. RNN-
based strategies produce, on average, a higher P&L than SFN-
based strategies. Moreover, the standard deviation of P&Ls illus-
trate that higher profit chances come at the cost of higher risk.
Only 𝐷𝐹actually achieves a meaningful increase in profits while
keeping standard deviation constant.
In order to quantify the P&L improvement, we define the P&L
surplus as the difference between the P&L of a prediction-based
strategy and the P&L of 𝐴𝑆(P&L𝐴𝑆). The left chart in Figure 7 il-
ˆ𝑅𝑏(RNN)
−1
0
1
TFI1−5
−1
0
1
TFI6−10
ˆ𝑅𝑎(RNN)
−1
0
1
TFI1−5
−1
0
1
TFI6−10
3.5
4.0
4.5
Mean squared error (%)
ˆ𝑅𝑏(SFN)
−1
0
1
TFI1−5
−1
0
1
TFI6−10
ˆ𝑅𝑎(SFN)
−1
0
1
TFI1−5
−1
0
1
TFI6−10
6
7
8
Mean squared error (%)
Figure 6: Mean squared prediction error by market sentiment
Strategy
1 min
5 min
1 h
12 h
𝐴𝑆
0.13
(0.25)
0.66
(0.79)
7.89
(5.71)
81.37
(32.95)
𝑆𝑃
RNN
0.14∗∗∗
(0.28)
0.70∗∗∗
(0.95)
8.06∗∗
(7.48)
101.93∗∗∗
(44.71)
SFN
0.14∗∗∗
(0.27)
0.68∗
(0.92)
8.01∗
(7.29)
91.86∗∗
(42.27)
𝐷𝐹
RNN
0.13∗∗
(0.25)
0.69∗∗
(0.80)
8.34∗∗∗
(5.74)
88.10∗∗
(32.56)
SFN
0.13
(0.25)
0.66
(0.80)
7.88
(5.76)
81.00
(32.91)
𝑆𝑃𝐷𝐹
RNN
0.14∗∗∗
(0.28)
0.75∗∗∗
(0.93)
8.45∗∗∗
(7.29)
104.13∗∗∗
(43.61)
SFN
0.14∗∗
(0.26)
0.67
(0.90)
7.92
(7.08)
92.01∗∗
(41.06)
Note: Numbers in brackets report the P&Ls’ standard deviation; ∗∗∗, ∗∗
and ∗indicate significant difference from 𝐴𝑆at the 1%, 5% and 10% level.
Table 2: Cumulative P&L by trading duration
lustrates the average one-minute P&L surplus as a function of one-
minute P&L𝐴𝑆percentile groups, where percentile group 1 (100)
contains the worst (best) 1% of all one-minute P&L𝐴𝑆. In both
RNN- and SFN-based strategies, we benefit from prediction-based
strategies when 𝐴𝑆performs poorly. The better 𝐴𝑆performs, the
less beneficial or more detrimental prediction-based strategies are.
The right chart plots the P&L surplus over one-minute predic-
tion error percentile groups, where percentile group 1 (100) con-
tains the 1% smallest (largest) one-minute sums of absolute predic-
tion errors for both buy and sell forecasts. The graph illustrates
that P&L surplus is large (small) when prediction errors are small
(large), suggesting that prediction quality is an indicator of P&L
performance. Besides, the charts show that 𝐷𝐹is less dependent
on prediction quality and P&L𝐴𝑆than 𝑆𝑃or 𝑆𝑃𝐷𝐹strategy.
Figure 8 illustrates each strategy’s average one-minute P&L
as a function of one-minute 𝑇𝐹𝐼and one-minute 𝑂𝐹𝐼. We cal-
culate one-minute 𝑇𝐹𝐼based on minute-by-minute aggregated
buy and sell trades, whereas for one-minute 𝑂𝐹𝐼, we consider
equal-weighted averages of all one-second LOB records within
a minute. Trading is least profitable during a seller overhang in
the LOB (𝑂𝐹𝐼< −0.5) in combination with a buyer surplus in
trade flow (𝑇𝐹𝐼> 0.5), potentially representing high competition
among waiting sellers such that we can catch only a small share
of impatient buyers. P&L is the highest in the opposite scenario,
𝑂𝐹𝐼> 0.5 with 𝑇𝐹𝐼< −0.5, indicating that we are more success-
ful in competing with buyers than with sellers (see Section 6.3).
Overall, 𝐴𝑆and 𝐷𝐹(𝑆𝑃and 𝑆𝑃𝐷𝐹) are less (more) dependent on
market dynamics and therefore provide a less (more) volatile P&L
profile. 𝑆𝑃and 𝑆𝑃𝐷𝐹are superior to 𝐴𝑆and 𝐷𝐹only if 𝑂𝐹𝐼> 0
20
40
60
80
P&L𝐴𝑆percentile group
−0.02
0.00
0.02
0.04
0.06
Mean P&L surplus
20
40
60
80
Prediction error percentile group
−0.02
0.00
0.02
0.04
0.06
Mean P&L surplus
𝑆𝑃(RNN)
𝐷𝐹(RNN)
𝑆𝑃𝐷𝐹(RNN)
𝑆𝑃(SFN)
𝐷𝐹(SFN)
𝑆𝑃𝐷𝐹(SFN)
Figure 7: One-minute P&L surplus over percentile groups
6
Electronic copy available at: https://ssrn.com/abstract=4320775


## Page 7

𝐴𝑆
TFI
−0.9−0.3 0.3
0.9
OFI
−0.9
−0.3
0.3
0.9
One-minute P&L
0.0
0.1
0.2
𝑆𝑃
TFI
−0.9−0.3 0.3
0.9
OFI
−0.9
−0.3
0.3
0.9
One-minute P&L
0.0
0.1
0.2
0.0
0.1
0.2
𝐷𝐹
TFI
−0.9−0.3 0.3
0.9
OFI
−0.9
−0.3
0.3
0.9
One-minute P&L
0.0
0.1
0.2
𝑆𝑃𝐷𝐹
TFI
−0.9−0.3 0.3
0.9
OFI
−0.9
−0.3
0.3
0.9
One-minute P&L
0.0
0.1
0.2
0.0
0.1
0.2
Figure 8: One-minute P&L as a function of 𝑇𝐹𝐼and 𝑂𝐹𝐼
and 𝑇𝐹𝐼< 0, whereas in all other situations 𝐴𝑆and 𝐷𝐹are su-
perior. Hence, dealers could switch between trading strategies in
response to changes in trade and order flow. e.g., switch to 𝐴𝑆or
𝐷𝐹(𝑆𝑃or 𝑆𝑃𝐷𝐹) when the buyer share (seller share) in trade flow
is large while the buyer share (seller share) in the LOB is small.
Since P&L includes both market making revenues and unre-
alized directional changes of the net position [60], we next aim
to understand each component’s contribution to P&L. We calcu-
late P&L generated from directional movements, P&L𝐷𝑅, as the
change in value of the net position caused by the mid-price change
[4], i.e., if the mid-price increases by 0.1 while we are long 2 assets,
it is P&L𝐷𝑅= 0.2. The left plot in Figure 9 reports RNN-based
P&L𝐷𝑅surplus as a function of one-minute mid-price change
decile groups, i.e., decile group 1 (10) contains the 10% minutes
with the most negative (positive) mid-price changes. In case of
𝐷𝐹, P&L𝐷𝑅surplus is the highest (smallest) when the mid-price
sharply (slightly) increases or decreases. As P&L𝐷𝑅can be viewed
as an approximation of adverse selection cost, this result suggests
that 𝐷𝐹’s reduction in adverse selection cost is proportional to the
magnitude of price movement: The larger the positive or negative
price movement, the larger the reduction in adverse selection cost.
As second P&L component, we calculate P&L from market mak-
ing activities, P&L𝑀𝑀, by subtracting P&L𝐷𝑅from P&L [60].
Thus, we implicitly subsume realized directional revenues [4] un-
der market making revenues. The right plot in Figure 9 shows
average P&L𝑀𝑀surplus as a function of average one-minute bid-
ask spread decile groups. Both𝑆𝑃and𝑆𝑃𝐷𝐹achieve the largest in-
crease in market making revenues when bid-ask spreads are large,
suggesting that the strategies are most successful at adjusting their
LOB position to trade flow when the order book is less liquid. From
1
2
3
4
5
6
7
8
9
10
Mid-price change decile group
−0.002
0.000
0.002
0.004
0.006
0.008
Mean P&LDR surplus
SP
DF
SPDF
1
2
3
4
5
6
7
8
9
10
Bid-ask spread decile group
−0.05
0.00
0.05
0.10
0.15
Mean P&LMM surplus
SP
DF
SPDF
Figure 9: One-minute P&L𝐷𝑅surplus and P&L𝑀𝑀surplus
both charts in Figure 9, we infer that P&L surplus of 𝐷𝐹is mainly
driven by reduced adverse selection cost, while P&L surplus of 𝑆𝑃
and 𝑆𝑃𝐷𝐹is mainly due to increased market making revenues.
6.3 Limit order book dynamics
Finally, we analyze how our strategies affect our position in
the LOB. Figure 10 illustrates the average 𝛿𝑎(solid lines) and
the average 𝛿𝑏(dotted lines) as functions of bid-ask spread per-
centile groups (top left), the net position (top right), the predicted
trade flow imbalance (below left), and one-second P&L percentile
groups (below right).
The top left graph shows that 𝑆𝑃and 𝑆𝑃𝐷𝐹place orders deeper
in the book than 𝐴𝑆and 𝐷𝐹, suggesting that 𝑆𝑃and 𝑆𝑃𝐷𝐹seek in-
creasing the margin through wider spreads rather than increasing
trade volume through tighter spreads. 𝐴𝑆and 𝐷𝐹quotes are less
sensitive to bid-ask spreads, i.e., when bid-ask spreads increase, 𝐴𝑆
and 𝐷𝐹follow this trend slower than 𝑆𝑃and 𝑆𝑃𝐷𝐹. It is 𝛿𝑎> 𝛿𝑏
in most cases, indicating that our average net position is short (see
Figure 15 in the Appendix). Thus, despite prediction-based correc-
tions, the dominant parameter determining 𝛿𝑎and 𝛿𝑏remains 𝑞.
Correspondingly, the top right graph shows that 𝛿𝑎is large (small)
when we are short (long) and 𝛿𝑏is small (large) when we are short
(long) to return to a neutral net position.
The chart below left illustrates 𝐷𝐹’s and 𝑆𝑃𝐷𝐹’s protection
against adverse price selection: 𝛿𝑎increases for d
𝑇𝐹𝐼> 0 to protect
against informed buyers, and decreases for d
𝑇𝐹𝐼< 0 to incentivize
short exposure for positively participating in the price decline. Ac-
cordingly, buy prices are lower represented by increasing 𝛿𝑏when
predicting a sell surplus, although the effect is less pronounced
than for sell orders, which could be due to the fact that we are
short on average and thus generally place buy orders deeper in
the book. The chart below right illustrates that submitting sell or-
ders deep in the book is risky: The highest and lowest P&L are
associated with the deepest sell orders, while sell orders close to
the top of the order book are associated with average P&L. Again,
this relationship is less clear for buy orders.
Next, we compare the price level priority of orders between
prediction-based strategies and the 𝐴𝑆strategy. We start counting
10
30
50
70
90
Bid-ask spread percentile group
1.00
1.25
1.50
1.75
2.00
2.25
2.50
2.75
3.00
δa, δb
−0.4 −0.2
0.0
0.2
0.4
Net position
−0.5
0.0
0.5
1.0
1.5
2.0
2.5
3.0
δa, δb
−1
−0.5
0
0.5
1
d
TFI
1.0
1.5
2.0
2.5
3.0
3.5
δa, δb
0
25
50
75
One-second P&L percentile group
0.0
0.5
1.0
1.5
2.0
2.5
3.0
δa, δb
δa
AS
δa
SP
δa
DF
δa
SPDF
δb
AS
δb
SP
δb
DF
δb
SPDF
Note: 𝑆𝑃, 𝐷𝐹and 𝑆𝑃𝐷𝐹use RNN predictions. 𝛿𝑎, 𝛿𝑏denote in basis points.
Figure 10: Depth of orders in the order book
7
Electronic copy available at: https://ssrn.com/abstract=4320775


## Page 8

−1.0
−0.5
0.0
0.5
1.0
d
TFI
−1.0
−0.5
0.0
0.5
1.0
Price level diﬀerence to AS
SP
DF
SPDF
−1.0
−0.5
0.0
0.5
1.0
OFI
0.0
0.1
0.2
0.3
0.4
0.5
Price level diﬀerence to AS
SP
DF
SPDF
Note: Solid (dashed) lines represent ask (bid) orders.
Figure 11: Price level difference to 𝐴𝑆
price levels at the top of the book as position 1, continuing with
the second-best price level as position 2, and so on. Thus, a posi-
tion difference of 1 (−1) means that the prediction-based strategy
is one price level behind (ahead of) 𝐴𝑆, i.e., it has a one price level
lower (higher) priority. Figure 11 shows the average price level
difference for RNN-based strategies as a function of d
𝑇𝐹𝐼(left) and
𝑂𝐹𝐼(right). The left chart shows that all three strategies post sell
(buy) orders deeper in the book when predicting a price increase
(decline) to protect against informed buyers (sellers). This effect
is most pronounced for 𝐷𝐹and 𝑆𝑃𝐷𝐹, since 𝑆𝑃initially does not
consider directional forecasts. The right chart illustrates that 𝑆𝑃
and 𝑆𝑃𝐷𝐹orders have a lower (equal) priority when there is ei-
ther (neither) a large buy or (nor) a large sell overhang in the order
book. In contrast, 𝐷𝐹posts sell orders closer to the top of (deeper
in) the book when 𝑂𝐹𝐼> 0 (𝑂𝐹𝐼< 0), thus acts contrary to d
𝑇𝐹𝐼.
To understand how our positioning in the LOB contributes to
P&L, the bar chart in Figure 12 illustrates the execution rate (left y-
axis) by price level. An execution rate of 30% at price level 3 means
that 30% of our orders queuing at price level 3 are filled within five
seconds. The circle markers indicate the average margin earned
(right y-axis), measured by 𝛿𝑎+ 𝛿𝑏. A margin of 5 basis points at
price level 2 means that we earn 5 basis points on average if one
buy and one sell order, each waiting at the second best price level,
get simultaneously filled by market orders.
While at the top of the order book all strategies achieve similar
execution rates and margins, 𝑆𝑃and 𝑆𝑃𝐷𝐹exceed 𝐴𝑆and 𝐷𝐹for
higher price levels. The margin advantage suggests that 𝑆𝑃and
𝑆𝑃𝐷𝐹can execute deeper orders even when the bid-ask spread is
large, whereas 𝐴𝑆and 𝐷𝐹execute on these levels only when the
bid-ask spread is small anyway and, accordingly, earn less margin.
Thus, 𝑆𝑃and 𝑆𝑃𝐷𝐹maximize the margin earned by increasing the
depth of orders while keeping the execution share at a high level.
Figure 13 shows each strategy’s share of executed orders by price
level, illustrating that 𝑆𝑃and 𝑆𝑃𝐷𝐹execute more orders at price
levels 2 to 5 than 𝐴𝑆and 𝐷𝐹. We infer that the higher market
making revenue of 𝑆𝑃and 𝑆𝑃𝐷𝐹largely comes from a higher ex-
ecution share of orders with more profitable spreads.
1
2
3
4
5
Price level
0
10
20
30
40
50
60
70
Execution rate (%)
AS
SP
DF
SPDF
2
3
4
5
6
7
8
Margin (bp)
Figure 12: Trade executions by price level
0
20
40
60
80
100
Share of executed orders (%)
AS
SP
DF
SPDF
Price level
1
2
3
4
≥5
Figure 13: Share of order executions by price level
7 Conclusion
In this paper, we present a data-driven attempt to overcome deal-
ers’ trade-off between volume and margin. To this end, we develop
a sequence prediction model for buyer- and seller-initiated trades
that predicts how the trade sizes of the next five seconds relate
to the trade sizes of the previous 24 hours. Using the Avellaneda-
Stoikov model as an example, we show how to adjust reservation
price and order depth in response to predictions based on empir-
ically calibrated sensitivity parameters. In a trading simulation,
we find both higher market making revenues through trade flow-
optimized positioning in the order book and lower adverse selec-
tion costs through anticipated price movements.
For future work, we see two possible approaches to improv-
ing our method. Given the recent development of reinforcement
learning in high-frequency trading, one approach would be to in-
corporate our predictions into the training of an agent, thus pro-
viding predictive information to the agent. Second, instead of ap-
proximating price changes using trade flow imbalance, predicting
price changes directly could improve our protection against ad-
verse selection as negative (positive) trade flow imbalance need
not always be associated with a price decrease (increase).
8 Appendix
Figure 14 presents the average number of price levels consumed
by 𝑅𝑏and 𝑅𝑎. The minimum price level consumed is 1, i.e., the
order has been fully matched with open limit orders at the top
price level. The figure indicates that larger trades are associated
with larger spreads earned by dealers on average.
Figure 15 shows the percentiles of net positions held as an
equal-weighted average for both ETH-USD and BTC-USD pairs.
The inventory limit is ±0.5 BTC or ±0.5 ETH, respectively. In more
than 50% (less than 20%) of all seconds, the dealer is net short (net
long), whereas in about 30% of all seconds the position is neutral.
0.0
0.2
0.4
0.6
0.8
1.0
Rb, Ra
2
4
6
8
10
Average number of price
levels consumed
Bid side
Ask side
Figure 14: Price level
consumption by 𝑅𝑏and 𝑅𝑎
0
20
40
60
80
100
Percentile
−0.4
−0.2
0.0
0.2
0.4
Net position
AS
SP
DF
SPDF
Figure 15: Percentiles
of net positions
8
Electronic copy available at: https://ssrn.com/abstract=4320775


## Page 9

References
[1] Abergel, F., Anane, M., Chakraborti, A., Jedidi, A. and Toke, I. M. [2016], Limit
order books, Cambridge University Press.
[2] Ahuja, S., Papanicolaou, G., Ren, W. and Yang, T.-W. [2017], ‘Limit order trading
with a mean reverting reference price’, Risk and Decision Analysis 6(2), 121–136.
[3] Albers, J., Cucuringu, M., Howison, S. and Shestopaloff, A. Y. [2021], ‘Fragmen-
tation, price formation and cross-impact in bitcoin markets’, Applied Mathe-
matical Finance 28(5), 395–448.
[4] Anolli, M. and Petrella, G. [2007], ‘Internalization in European Equity Mar-
kets Following the Adoption of the EU MiFID Directive’, The Journal of Trading
2(2), 77–88.
[5] Avellaneda, M. and Stoikov, S. [2008], ‘High-frequency trading in a limit order
book’, Quantitative Finance 8(3), 217–224.
[6] Aydoğan, B., Uğur, Ö. and Aksoy, Ü. [2022], ‘Optimal limit order book trad-
ing strategies with stochastic volatility in the underlying asset’, Computational
Economics pp. 1–36.
[7] Bayraktar, E. and Ludkovski, M. [2014], ‘Liquidation in limit order books with
controlled intensity’, Mathematical Finance 24(4), 627–650.
[8] Cao, C., Hansch, O. and Wang, X. [2009], ‘The information content of an
open limit-order book’, Journal of Futures Markets: Futures, Options, and Other
Derivative Products 29(1), 16–41.
[9] Cartea, Á. and Jaimungal, S. [2013], ‘Modelling asset prices for algorithmic and
high-frequency trading’, Applied Mathematical Finance 20(6), 512–547.
[10] Cartea, Á. and Jaimungal, S. [2015], ‘Risk metrics and fine tuning of high-
frequency trading strategies’, Mathematical Finance 25(3), 576–611.
[11] Cartea, Á., Jaimungal, S. and Penalva, J. [2015], Algorithmic and high-frequency
trading, Cambridge University Press.
[12] Cartea, Á., Jaimungal, S. and Ricci, J. [2014], ‘Buy low, sell high: A high fre-
quency trading perspective’, SIAM Journal on Financial Mathematics 5(1), 415–
444.
[13] Chakraborty, T. and Kearns, M. [2011], Market making and mean reversion, in
‘Proceedings of the 12th ACM Conference on Electronic Commerce’, EC ’11,
Association for Computing Machinery, New York, NY, USA, p. 307–314.
[14] Chakravarty, S. [2001], ‘Stealth-trading: Which traders’ trades move stock
prices?’, Journal of Financial Economics 61(2), 289–307.
[15] Chan, E. [2017], Machine Trading: Deploying Computer Algorithms to Conquer
the Markets, Wiley trading series, Wiley.
[16] Coinbase [2022], ‘Coinbase Homepage: About’, https://www.coinbase.com/
about.
[17] Cont, R., Kukanov, A. and Stoikov, S. [2014], ‘The price impact of order book
events’, Journal of Financial Econometrics 12(1), 47–88.
[18] Dixon, M. [2018a], ‘A high-frequency trade execution model for supervised
learning’, High Frequency 1(1), 32–52.
[19] Dixon, M. [2018b], ‘Sequence classification of the limit order book using recur-
rent neural networks’, Journal of Computational Science 24, 277–286.
[20] Dixon, M. F., Polson, N. G. and Sokolov, V. O. [2019], ‘Deep learning for spatio-
temporal modeling: dynamic traffic flows and high frequency trading’, Applied
Stochastic Models in Business and Industry 35(3), 788–807.
[21] Felder, C. and Seemüller, J. [2022], Intelligent Inventory Management for Cryp-
tocurrency Brokers, in ‘Proceedings of the Third ACM International Confer-
ence on AI in Finance’, ICAIF ’22, Association for Computing Machinery, New
York, NY, USA, p. 1–8.
[22] Fodra, P. and Labadie, M. [2012], ‘High-frequency market-making with in-
ventory constraints and directional bets’, unpublished, available at https:
//arxiv.org/abs/1206.4810.
[23] Frey, S. and Grammig, J. [2008], Liquidity supply and adverse selection in a pure
limit order book market, in ‘High Frequency Financial Econometrics’, Springer,
pp. 83–109.
[24] Gabaix, X., Gopikrishnan, P., Plerou, V. and Stanley, H. E. [2006], ‘Institu-
tional investors and stock market volatility’, The Quarterly Journal of Economics
121(2), 461–504.
[25] Ganesh, S., Vadori, N., Xu, M., Zheng, H., Reddy, P. and Veloso, M. [2019],
‘Reinforcement learning for market making in a multi-agent dealer market’,
unpublished, available at https://arxiv.org/abs/1911.05892.
[26] Gašperov, B. and Kostanjčar, Z. [2021], ‘Market making with signals through
deep reinforcement learning’, IEEE Access 9, 61611–61622.
[27] Glosten, L. R. [1994], ‘Is the electronic open limit order book inevitable?’, The
Journal of Finance 49(4), 1127–1161.
[28] Gopikrishnan, P., Plerou, V., Gabaix, X. and Stanley, H. E. [2000], ‘Statisti-
cal properties of share volume traded in financial markets’, Physical review e
62(4), R4493.
[29] Gould, M. D., Porter, M. A., Williams, S., McDonald, M., Fenn, D. J. and Howi-
son, S. D. [2013], ‘Limit order books’, Quantitative Finance 13(11), 1709–1742.
[30] Graves, A. [2013], ‘Generating sequences with recurrent neural networks.’,
CoRR abs/1308.0850. http://arxiv.org/abs/1308.0850.
[31] Guéant, O. [2017], ‘Optimal market making’, Applied Mathematical Finance
24(2), 112–154.
[32] Guéant, O., Lehalle, C.-A. and Fernandez-Tapia, J. [2013], ‘Dealing with the
inventory risk: a solution to the market making problem’, Mathematics and
financial economics 7(4), 477–507.
[33] Guéant, O. and Manziuk, I. [2019], ‘Deep reinforcement learning for market
making in corporate bonds: beating the curse of dimensionality’, Applied Math-
ematical Finance 26(5), 387–452.
[34] Guilbaud, F. and Pham, H. [2013], ‘Optimal high-frequency trading with limit
and market orders’, Quantitative Finance 13(1), 79–94.
[35] Haider, A., Wang, H., Scotney, B. and Hawe, G. [2022], ‘Predictive Market Mak-
ing via Machine Learning’, Operations Research Forum 3(1), 1–21.
[36] Handa, P. and Schwartz, R. A. [1996], ‘Limit order trading’, The Journal of Fi-
nance 51(5), 1835–1861.
[37] Hirschey, N. [2021], ‘Do high-frequency traders anticipate buying and selling
pressure?’, Management Science 67(6), 3321–3345.
[38] Ho, T. and Stoll, H. R. [1981], ‘Optimal dealer pricing under transactions and
return uncertainty’, Journal of Financial Economics 9(1), 47–73.
[39] Kercheval, A. N. and Zhang, Y. [2015], ‘Modelling high-frequency limit
order book dynamics with support vector machines’, Quantitative Finance
15(8), 1315–1329.
[40] Kühn, C. and Stroh, M. [2010], ‘Optimal portfolios of a small investor in a limit
order market: a shadow price approach’, Mathematics and Financial Economics
3(2), 45–72.
[41] LeCun, Y. A., Bottou, L., Orr, G. B. and Müller, K.-R. [2012], Efficient backprop,
in ‘Neural networks: Tricks of the trade’, Springer, pp. 9–48.
[42] Li, X., Deng, X., Zhu, S., Wang, F. and Xie, H. [2014], ‘An intelligent market
making strategy in algorithmic trading’, Frontiers of Computer Science 8(4), 596–
608.
[43] Lim, Y.-S. and Gorse, D. [2018], Reinforcement learning for high-frequency
market making, in ‘ESANN 2018-Proceedings, European Symposium on Ar-
tificial Neural Networks, Computational Intelligence and Machine Learning’,
ESANN, pp. 521–526.
[44] Linnainmaa, J. [2003], ‘Who makes the limit order book? Implications for con-
trarian strategies, attention-grabbing hypothesis, and the disposition effect’,
Available at SSRN 474222 .
[45] Makarov, I. and Schoar, A. [2020], ‘Trading and arbitrage in cryptocurrency
markets’, Journal of Financial Economics 135(2), 293–319.
[46] Maslov, S. and Mills, M. [2001], ‘Price fluctuations from the order book per-
spective—empirical facts and a simple model’, Physica A: Statistical Mechanics
and its Applications 299(1-2), 234–246.
[47] Menkveld, A. J. [2013], ‘High frequency trading and the new market makers’,
Journal of Financial Markets 16(4), 712–740.
[48] Palguna, D. and Pollak, I. [2013], Non-parametric prediction in a limit order
book, in ‘2013 IEEE Global Conference on Signal and Information Processing’,
IEEE, pp. 1139–1139.
[49] Paquin, D. [2020], ‘Coinbase Pro API’, https://github.com/danpaquin/
coinbasepro-python.
[50] Potters, M. and Bouchaud, J.-P. [2003], ‘More statistical properties of order
books and price impact’, Physica A: Statistical Mechanics and its Applications
324(1-2), 133–140.
[51] Rojas, R. [2013], Neural networks: a systematic introduction, Springer Science &
Business Media.
[52] Rumelhart, D. E., Hinton, G. E. and Williams, R. J. [1985], Learning internal rep-
resentations by error propagation, Technical report, California Univ San Diego
La Jolla Inst for Cognitive Science.
[53] Rumelhart, D. E., Hinton, G. E. and Williams, R. J. [1986], ‘Learning represen-
tations by back-propagating errors’, Nature 323(6088), 533–536.
[54] Sadighian, J. [2019], ‘Deep reinforcement learning in cryptocurrency market
making’, unpublished, available at https://arxiv.org/abs/1911.08647.
[55] Sandås, P. [2001], ‘Adverse selection and competitive market making: Empirical
evidence from a limit order market’, The Review of Financial Studies 14(3), 705–
734.
[56] Schnaubelt, M. [2022], ‘Deep reinforcement learning for the optimal place-
ment of cryptocurrency limit orders’, European Journal of Operational Research
296(3), 993–1006.
[57] Schnaubelt, M., Rende, J. and Krauss, C. [2019], ‘Testing stylized facts of bitcoin
limit order books’, Journal of Risk and Financial Management 12(1), 25.
[58] Seppi, D. J. [1997], ‘Liquidity provision with limit orders and a strategic spe-
cialist’, The Review of Financial Studies 10(1), 103–150.
[59] Silantyev, E. [2019], ‘Order flow analysis of cryptocurrency markets’, Digital
Finance 1(1), 191–218.
[60] Spooner, T., Fearnley, J., Savani, R. and Koukorinis, A. [2018], Market making
via reinforcement learning, in ‘Proceedings of the 17th International Confer-
ence on Autonomous Agents and MultiAgent Systems’, AAMAS ’18, Interna-
tional Foundation for Autonomous Agents and Multiagent Systems, Richland,
SC, p. 434–442.
[61] Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I. and Salakhutdinov, R.
[2014], ‘Dropout: A Simple Way to Prevent Neural Networks from Overfitting’,
Journal of Machine Learning Research 15(56), 1929–1958.
[62] Tsantekidis, A., Passalis, N., Tefas, A., Kanniainen, J., Gabbouj, M. and Iosifidis,
A. [2017], Forecasting stock prices from the limit order book using convolu-
tional neural networks, in ‘2017 IEEE 19th conference on business informatics
(CBI)’, Vol. 1, IEEE, pp. 7–12.
[63] Tsantekidis, A., Passalis, N., Tefas, A., Kanniainen, J., Gabbouj, M. and Iosifidis,
A. [2020], ‘Using deep learning for price prediction by exploiting stationary
limit order book features’, Applied Soft Computing 93, 106401.
[64] Weber, P. and Rosenow, B. [2005], ‘Order book approach to price impact’, Quan-
titative Finance 5(4), 357–364.
[65] Zaznov, I., Kunkel, J., Dufour, A. and Badii, A. [2022], ‘Predicting stock price
changes based on the limit order book: A survey’, Mathematics 10(8).
[66] Zhang, Z., Zohren, S. and Roberts, S. [2019], ‘DeepLOB: Deep convolutional
neural networks for limit order books’, IEEE Transactions on Signal Processing
67(11), 3001–3012.
[67] Zheng, B., Moulines, E. and Abergel, F. [2013], ‘Price jump prediction in limit
order book’, Journal of Mathematical Finance 3(2), 242–255.
9
Electronic copy available at: https://ssrn.com/abstract=4320775


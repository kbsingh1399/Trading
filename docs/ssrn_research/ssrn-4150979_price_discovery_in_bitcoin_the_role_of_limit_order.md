# Price Discovery in Bitcoin: The Role of Limit Orders

- **Source File**: `ssrn-4150979.pdf`
- **Total Pages**: 39
- **SSRN ID**: `ssrn-4150979`

---

## Page 1

Price Discovery in Bitcoin: The Role of Limit Orders
Carol Alexander∗, Daniel F. Heck† , Andreas Kaeck‡
June 29, 2022
Abstract
We analyse the price discovery process in bitcoin-dollar trading on Coinbase, the most
established cryptocurrency spot exchange. Using a modiﬁed reinforcement learning frame-
work, we ﬁnd that market orders individually carry more information than limit orders,
but due to their abundance, limit orders are the main driver of price discovery. Moreover,
we observe a signiﬁcant asymmetry in permanent price impact, with sell market orders
carrying more information than buy market orders. We relate this asymmetry to unidirec-
tional retail order ﬂows. Owing to a negligible relative tick size, most of the price discovery
contribution of limit orders originates from orders undercutting the best quotes. Consistent
with theoretical predictions, the state of the order book has a signiﬁcant impact on price
discovery, with orders submitted along the order book imbalance showing an increased con-
tribution and the importance of market orders being more pronounced in case of a binding
bid-ask spread. Finally, the price discovery process on Coinbase is strongly inﬂuenced by
information ﬂows from other exchanges.
Keywords: Price Impact; Limit Order Book; Liquidity Provision; Price Discovery; Information Content; Rein-
forcement Learning.
JEL classiﬁcation: C22, C5, E42, F31, G1, G2
∗University of Sussex Business School. Email: c.alexander@sussex.ac.uk
†Corresponding author: University of Sussex Business School. Email: d.heck@sussex.ac.uk
‡University of Sussex Business School. Email: a.kaeck@sussex.ac.uk
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 2

1
Introduction
Traditional microstructure models assume that informed agents incorporate their private information
into prices by seeking immediacy and removing liquidity, whereas market makers are uninformed and
their quotes reﬂect only public information (Kyle, 1985). While such a classiﬁcation was reasonable
in traditional markets where liquidity was provided through a designated market maker, it is overly
simplistic nowadays. With most exchanges operating electronic limit order books where any participant
is able to act as liquidity provider, the process of price discovery has fundamentally changed. Investors
with an informational advantage have to choose between market and limit orders, where the decision
might depend on the current state of the market, the expected behaviour of other market participants
or even the time of day. In addition, the advent of algorithmic trading has tremendously increased
both the number of messages sent to exchanges and the speed at which information is impounded into
prices (O’Hara, 2015).
Despite their comparatively short history, cryptocurrencies have not been spared from this trans-
formation in market microstructure. On the contrary, even the earliest crypto exchanges have been
fully electronic, with trading occurring through a publicly visible limit order book. Modern cryptocur-
rency trading venues operate application programming interfaces (APIs) which allow users to connect
their trading algorithms to the exchange without any intermediary and retrieve market data as well
as manage their orders. Even less experienced retail traders can easily engage in algorithmic trading
by using one of the countless available out-of-the-box trading bots.
In this study, we use an extensive tick-by-tick data set on transactions and order book messages
on Coinbase, the most established and only listed cryptocurrency spot exchange, to analyse the price
discovery process in bitcoin-dollar trading at its most granular level. In total, our data set covers
the four-month period from February to May 2022 which, due to crypto exchanges operating 24/7,
corresponds to 120 trading days. The data contain every message sent to the exchange, which allows
us to identify each order submission and cancellation uniquely and eliminates the need to construct
limit order ﬂow variables as in Chaboud et al. (2021) for example.
To be consistent with related
studies such as Fleming et al. (2018), we ﬁrst consider only market orders (trades) and examine how
their permanent price impact is related to their size.1 Then, to analyse the importance of limit order
activity, we study all order ﬂow components – market orders, limit order submissions, and limit order
cancellations – jointly. In this context, we ﬁrst quantify the price discovery contribution of limit order
actions depending on their aggressiveness, before more closely examining the relationship between
permanent price impact and order size. Several empirical studies have shown that in modern ﬁnancial
markets, the shape of the order book aﬀects the behaviour of market participants and consequently,
the price discovery process (Cao et al., 2009; Brogaard et al., 2014). Therefore, we then integrate
the order book in our study and analyse how the price discovery contribution of the diﬀerent order
ﬂow components changes depending on the prevailing order book imbalance and the quoted bid-ask
spread. Finally, having closely analysed price discovery on Coinbase, we broaden our perspective and
1We use the term market order for all marketable orders, i.e. orders that are immediately executed when submitted.
Therefore, market orders also include buy (sell) limit orders where the limit price is greater (smaller) than the best ask
(bid) quote.
2
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 3

take into account information ﬂows from other exchanges. The crypto market is highly fragmented
with hundreds of electronic exchanges, where the trading volume on some of them exceeds that on
Coinbase by far.
Therefore, it is likely that information from these exchanges inﬂuence the price
discovery process on Coinbase. To analyse this, we study the permanent price impact of the diﬀerent
order ﬂow components on Coinbase depending on the preceding return on other crypto derivatives and
spot exchanges.
To analyse the permanent price impacts of diﬀerent order ﬂow components as well as their interac-
tion, we rely on a modiﬁed reinforcement learning (RL) framework recently proposed by Philip (2020).
Compared to the standard empirical tool for evaluating price discovery – the Vector Autoregression
(VAR) model (Hasbrouck, 1991) – the RL framework oﬀers two major advantages. First, unlike the
VAR, the RL framework is able to capture nonlinear relationships.
For example, many empirical
studies report a concave relationship between price impact and trade size (Donier and Bonart, 2015).
The traditional basic VAR model is not able to capture this relationship correctly and might lead to
erroneous conclusions. In contrast, as shown by Philip (2020) and Kwan et al. (2021), the modiﬁed
RL model is able to identify such nonlinear relationships. Second, the RL framework consistently out-
performs the VAR in terms of computation time. By expanding the space of variables, the basic VAR
model can be modiﬁed to capture nonlinearities. However, the estimation time increases exponentially
in the number of coeﬃcients. In contrast, the computational time required to estimate the modiﬁed
RL model increases only linearly in the number of variables. Therefore, the RL framework is better
suited to study permanent price impact, especially if multiple market variables are considered jointly.
Our analysis shows that market orders individually exhibit a much larger permanent price impact,
and thus carry more information, than limit order actions. In particular, the individual information
content of market orders is two to three times greater than that of undercutting limit order submis-
sions. However, if the abundance of limit order actions is taken into account, limit order submissions are
signiﬁcantly more important than market orders and contribute about 50% to price discovery. More-
over, we ﬁnd a signiﬁcant asymmetry in the permanent price impact of market orders that persists
throughout the entire sample period and has not been observed in traditional asset classes. Speciﬁcally,
sell-initiated market orders contain 60% more information than orders originating from the buy side.
We suppose that this asymmetry is caused by unidirectional retail order ﬂows on Coinbase, where retail
investors are mainly on the buy side of transactions. Since these investors are typically less informed
than institutions, the large proportion of buy transactions initiated by retail traders reduces the in-
formation content, and consequently the permanent price impact, of buy-inititiated market orders,
causing an asymmetry.
For limit orders, the negligible relative tick size of less than one-third basis point makes submissions
inside the spread highly attractive and thus, the bulk of the price discovery contribution of limit order
submissions originates from undercutting orders. Cancellations of limit orders also contribute a signif-
icant amount to price discovery (34%) where, similar to submissions, most of this contribution comes
from price-changing cancellations. However, for these cancellations, a large part of the permanent price
impact is of mechanical nature. The extremely low tick size causes many empty price levels behind
the best quotes, which in turn cause price-changing cancellations to trigger a rather large immediate
3
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 4

changes in the mid price.
Moreover, our results show that the state of the order book has a signiﬁcant impact on the price
discovery process. Trading actions whose direction coincides with the imbalance prevailing in the order
book contribute considerably more to price discovery than actions opposite to the imbalance. Similarly,
the quoted bid-ask spread aﬀects the order choice of informed agents. If the spread is more than one
tick, price discovery predominantly occurs through undercutting limit orders – their contribution is
57%. However, in case of a binding spread, market orders become the main driver of price discovery,
contributing about 38%.
Finally, we ﬁnd that the price discovery process on Coinbase is heavily
inﬂuenced by information ﬂows from other exchanges. In particular, the price evolution of the three
most actively traded bitcoin derivatives products and the largest bitcoin spot pair, within the second
before a trading action on Coinbase determines the direction and magnitude of the permanent price
impact of the trading action. In fact, the preceding price evolution on the three derivatives products
and the largest spot pair is even more relevant for the price discovery process on Coinbase than the
preceding price movement on Coinbase itself.
This study contributes to the existing literature in several ways. First, our results conﬁrm the
central assumption of modern microstructure models, such as Rosu (2020), that, in order to impound
their information into prices, informed agents not only use market orders (informed liquidity taking)
but also rely heavily on limit orders (informed liquidity making). Similarly, the results also support
recent models of limit order book markets such as Bhattacharya and Saar (2020) and Ricc´o et al. (2022)
in their empirical predictions that order book variables contain signiﬁcant amounts of information and
inﬂuence the price discovery process. Second, our study contributes to the empirical literature on price
formation in modern ﬁnancial markets where trading occurs through central limit order books. While
the theoretical market microstructure literature has recognized the fundamental shift from informed
liquidity taking to informed liquidity provision and has started to incorporate it into models, the
number of detailed empirical studies is still limited, mainly due to the lack of available data. Existing
works focus on US Treasury securities (Fleming et al., 2018), Canadian equities (Brogaard et al., 2019)
and FX markets (Chaboud et al., 2021). We expand this spectrum to include the relatively new asset
class of cryptocurrencies. Even though the crypto market has experienced an increasing institutional
adoption and has recently moved once more into the focus of regulators, its microstructure is still little
researched and not yet completely understood.2 While there are several works such as Alexander and
Heck (2020) that quantify inter-exchange price discovery, mostly relying exclusively on transaction
data, we are the ﬁrst to provide insights into the most fundamental aspects of the intra-exchange price
discovery process, by considering not only transaction data, but all messages sent to the exchange. In
particular, we show that even within the still young and comparatively small cryptocurrency market,
liquidity providers are well informed and their actions are highly relevant in terms of price discovery.
The remainder of this paper is organized as follows: Section 2 explains the methodology of the mod-
iﬁed reinforcement learning framework used to measure permanent price impact. Section 3 describes
the cryptocurrency trading landscape as well as the data set used in this study. Section 4 presents
our results on permanent price impacts and price discovery contribution of market orders, limit order
2See Financial Times on 24 June 2022.
4
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 5

submissions and cancellations. Sections 5 and 6 explore how the price discovery process on Coinbase
is inﬂuenced by the state of the order book and the price evolution on other crypto trading venues,
respectively. Section 7 summarises and concludes.
2
Methodology
In this section, we introduce the main idea and the most important features of the modiﬁed reinforce-
ment learning (RL) framework used to quantify permanent price impact. For more details on RL itself
and the augmentation of the original RL setting as well as for very illustrative examples, we refer
to Philip (2020). In terms of assumptions, the RL approach is minimal and only assumes that the
data are stationary and Markov. Compared to the traditional VAR model, which assumes linearity,
these conditions are quite unrestrictive. Within the bitcoin market, Ghysels and Nguyen (2019) ﬁnd
no evidence for non-Markovian learning, suggesting that the Markovian learning assumption typically
adopted in limit order book models is reasonable.
In the RL framework proposed by Philip (2020), traders interact with the market in discrete time
steps. Formally, at each time step, the market can be in a certain state si ∈S where S is called
the state space. This space is very general and can be deﬁned depending on the research question.
In the most simple case, there is only one state (i.e. open), while more sophisticated states could
for example capture the current order book imbalance or the available liquidity. At each time step,
market participants are allowed to perform certain actions aj ∈A with A denoting the action space.
As for the market states, this set of available actions can be modiﬁed depending on the object of the
analysis. Practical examples are the submissions of market orders or the cancellations of limit orders.
In the following, we denote the state of the market at time t by s(t) and the action that is performed
at time t by a(t). The model can operate either in event time or in calendar time. We choose to use
the former since this reduces the bias arising from irregularly spaced observations (O’Hara, 2015).
The actions represent interactions of agents with the market that might change its state and trigger
reactive actions by other agents in the next time step. Speciﬁcally, if at time t, an agent performs
action a(t), the market might transit from its current state s(t) to some state s(t + 1) at time t + 1.
At this next time step, where the market is in the new state s(t + 1), other agents – or even the same
agent that initiated action a(t) previously – might then take some action a(t + 1). For example, if
the bid-ask spread is at its minimum value, the submission of a very large buy market order could
absorb all liquidity available at the ﬁrst few ask levels and consequently widen the spread. Due to this
widening, market makers might then submit sell limit orders to restore the removed liquidity.
Due to this interaction between agents and the market, each state-action pair (si, aj) ∈S × A can
be assigned a probability to trigger a transition to the state-action pair (sk, al). Formally, this is the
probability that if the market is in state si at time t (i.e. s(t) = si) and an agent performs action aj
(i.e. a(t) = aj), the market will be in state sk at the next time step t + 1 (i.e. s(t + 1) = sk) where
then action al is performed (i.e. a(t + 1) = al).3 Following Philip (2020), these transition probabilities
3The state-action pair (si, aj) can also trigger a ”transition” to itself. In fact, ﬁnancial markets typically exhibit a
diagonal eﬀect, where the probability to observe a given action is increased after this action has just occurred (Biais
et al., 1995).
5
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 6

can be empirically estimated by maximum likelihood estimation, as
P(i,j),(k,l) : = P (s(t + 1) = sk, a(t + 1) = al | s(t) = si, a(t) = aj)
=
N(sk, al | si, aj)
P
sk∈S
P
al∈A N(sk, al | si, aj)
(1)
where N(sk, al | si, aj) denotes the number of times the state-action pair (si, aj) is followed by state-
action pair (sk, al). Intuitively, the probability in (1) is simply the number of times (si, aj) is followed
by (sk, al), relative to the number of times (si, aj) occurs in the data set.
Besides the ability to change the market state, actions might also cause an immediate change in the
mid price where the magnitude of this change might further depend on the current market state. For
instance, a very large buy market order leads to a larger immediate change in the mid price if the depth
at the ﬁrst ask levels is low. Therefore, each state-action pair (si, aj) exhibits an immediate impact on
the mid price, denoted by R(si, aj). Note that this immediate impact is of purely mechanical nature
and for some actions, such as limit order submissions behind the best quotes, it will always be zero.
Once more following Philip (2020), we estimate R(si, aj) as the average demeaned log change in the
mid price observed for the state-action pair (si, aj).
The permanent price impact of (si, aj) is the long-run change in the mid price caused by the state-
action pair, i.e. by an agent taking action aj when the market is in state si. As explained above, there
are two consequences to the occurrence of a state-action pair. It causes an immediate change in the
mid price and triggers a transition to some other (or possibly the same) state-action pair in the next
time step. Therefore, both of these consequences have to be taken into account when calculating the
permanent price impact. Philip (2020) does this by measuring the permanent price impact Q(si, aj)
of (si, aj) recursively as its immediate impact R(si, aj) plus the discounted expected permanent price
impacts of all subsequent state-action pairs (sk, al) triggered by the initial state-action pair (si, aj).
Put in mathematical terms, this yields the value iteration rule
Q(si, aj) = R(si, aj) + γ
n(S)
X
k=1
n(A)
X
l=1
P(i,j),(k,l) Q(sk, al)
(2)
where n(S) and n(A) denote the cardinality of S and A respectively, and γ represents a discount
factor that in a high-frequency analysis is typically set very close to 1. Such a value iteration update
is commonly known as Q-learning in the RL literature. Watkins and Dayan (1992) show that the
iteration of Equation (2) will converge to the optimum with probability one so long as all actions are
repeatedly sampled in all states and the action-values are represented discretely. Given that these
requirements are met and both the immediate impacts and the transition probabilities are calculated
as explained above, we can estimate the permanent price impact Q(si, aj) of (si, aj) by initializing it
as some constant (usually zero) and then iterating Equation (2) until convergence.
The transition probabilities and the immediate impacts are empirically estimated input parameters
and thus, they exhibit a certain ﬁnite-sample error, which can cause estimation errors in the permanent
price impact estimates. Therefore, to quantify these estimation errors, we follow the block bootstrap-
6
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 7

ping procedure in Philip (2020). Speciﬁcally, a sinlge bootstrap iteration involves the following steps.
First, we decompose the original data sample of size n into blocks of l consecutive observations. Then,
we sample n/l blocks with replacement from this set of blocks and concatenate the sampled blocks,
so that we again obtain a sample of the same size as the original data. For this bootstrapped sample,
we can then compute the permanent price impacts. We repeat this procedure 100 times and calculate
conﬁdence intervals over the 100 bootstrapped estimates of permanent price impact. Following White
and White (2010), the block length l is chosen as n1/3.
Finally, in a similar spirit to Hasbrouck (1991), Philip (2020) also introduces a simple metric which
assigns to each state-action pair its relative contribution to the total price variation in the model. The
metric is calculated as
RC(si, aj) =
|Q(si, aj)| × N(si, aj)
Pn(S)
k=1
Pn(A)
l=1 |Q(sk, al)| × N(sk, al)
(3)
where N(si, aj) denotes the number of times the state-action pair (si, aj) occurs in the data set. This
metric is highly ﬂexible and can easily be modiﬁed to obtain the contribution of an action to the total
amount of price variation within a certain market state or even the contribution of a state to the total
price variation.
3
Data
Our analysis is based on an extensive tick-by-tick data set obtained from Tardis.dev. In particular,
we obtain data on all transactions and order book messages on Coinbase during the period from 1
February to 31 May 2022. Since crypto markets operate 24/7, this sample period corresponds to 120
trading days. The transaction records specify the transaction price, the amount that was traded, as
well as the order sign, i.e. a ﬂag indicating the taker side of the transaction. If a marketable order
executes against multiple resting limit orders, the transaction records contain a separate entry for each
of the limit orders. However, according to Upson et al. (2018), interpreting these entries as separate
transactions introduces signiﬁcant bias into empirical studies. Therefore, we combine consecutive trade
records with the same order sign and the exact same timestamp into a single transaction.
The order book data set is split so that we obtain a separate ﬁle for each trading day in our sample.
Each of these 120 ﬁles starts with an initial snapshot of the entire order book, containing all active
price levels and the respective available volumes. After this snapshot, all updates to any of the price
levels are recorded.4 Speciﬁcally, for each change in the order book, we obtain a record specifying the
price level that was changed, the order book side of the change, whether the volume at this level was
increased or reduced, as well as the volume available at this price level after the change.
Both types of data are double timestamped with microsecond precision, once by the exchange and
a second time when the message arrives at the Tardis servers. Importantly, for the transaction records,
4Due to latency issues, the initial snapshot is usually not taken exactly at midnight but a few milliseconds after.
Therefore, it happens that on some days, the ﬁle contains a few order book update messages before the initial snapshot.
Since we cannot accurately determine the top-of-book quotes for these updates without going back to data from the
previous day, we ignore these few messages.
7
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 8

Table 1 Summary Statistics: Market and Limit Order Activity
The table reports averages on market and limit order activity in BTCUSD on Coinbase during the period from 1 February
to 31 May 2022. The ratio of average to standard deviation is shown in parentheses. Count represents the daily number
of observations for each action. Size denotes the order size, either in USD or in BTC. Duration denotes the average time
between two actions of the same type (in milliseconds).
Daily Count
Size (in BTC)
Size (in USD)
Duration
Trades
Buy
202,862 (3.24)
0.0448 (0.16)
1,680.07 (0.16)
425.91 (0.70)
Sell
117,386 (2.46)
0.0725 (0.17)
2,728.05 (0.17)
736.03 (0.57)
Limit Order Submissions
Buy
6,312,348 (3.72)
0.2474 (0.00)
7,865.76 (0.27)
13.69 (0.04)
Sell
6,023,769 (3.58)
0.2144 (0.21)
8,702.35 (0.01)
14.34 (0.04)
Limit Order Cancellations
Buy
6,140,126 (3.81)
0.2489 (0.00)
8,034.19 (0.27)
14.07 (0.04)
Sell
5,845,214 (3.67)
0.2194 (0.22)
8,913.68 (0.01)
14.78 (0.04)
the exchange-provided timestamp indicates the exact time at which the market order causing the trade
hit the order book. This eliminates time delay issues as in Hautsch and Huang (2012) and allows us
to match transactions and order book updates on this exchange-provided timestamp so that we can
uniquely identify the volume reductions in the order book that are caused by market orders, rather
than cancellations of limit orders.
Trading on major cryptocurrency exchanges is very active and fast-paced. Over our 120-day sample
period, there were more than 2.9 billion order book changes and almost 39 million transactions. For
comparison, Fleming et al. (2018) report 2.4 billion order book messages for US Treasury securities
over 500 trading days in 2010 and 2011, where – similar to crypto exchanges – trading takes place
almost 24 hours per day. Table 1 reports summary statistics on the market and limit order activity over
our sample period from 1 February to 31 May 2022. We see that limit order actions occur much more
frequently than market orders. With a daily average of about 24 million limit order messages and only
320,000 transactions, limit order activity is responsible for almost 99% of all messages sent to the ex-
change. Highlighting the fast paced nature of cryptocurrency exchanges, submissions and cancellations
of limit orders occur on average every 14 milliseconds. The number of submissions and cancellations is
almost equal, with about 97% of all limit orders being cancelled. Such high cancellation rates are not
unique to cryptocurrencies but they are a common characteristic of modern ﬁnancial markets (O’Hara,
2015). Moreover, transactions exhibit two statistically signiﬁcant asymmetries. While trades are more
often initiated from the bid side than from the ask side, the average size of sell transactions is about
60% greater than that of buy-initiated trades. Finally, we note that the size of limit order submissions
and cancellations is about four times that of transactions.
Table 2 provides summary statistics on the quoted bid-ask spread and the absolute price distances
among the top ﬁve levels in the order book, based on one-second snapshots. We see that the bid-ask
spread is binding for about 37% of the time. However, with a standard deviation of more than two
dollars, it is highly volatile and sometimes reaches even values above 150 USD, which highlights the
high volatility of bitcoin (Scaillet et al., 2020). Despite these extreme values, the bid-ask spread is in
relative terms still very small, with its average value of 1.73 USD consistently corresponding to less
than a basis point of the BTCUSD price during our sample period. The statistics on the distances
between adjacent price levels behind the best quotes indicate a large number of empty price levels
8
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 9

Table 2 Summary Statistics: Spread and Price Distance
The table reports summary statistics on the bid-ask spread and the absolute price distances among the top ﬁve levels in
the order book. Binding represents the proportion of observations (in %) where the variables are at their minimum value
of 0.01 USD. All statistics are calculated based on one-second order book snapshots during the period from 1 February
31 May 2022. Except Binding, all quantities are in USD.
Spread
Bid 1-2
Bid 2-3
Bid 3-4
Bid 4-5
Ask 1-2
Ask 2-3
Ask 3-4
Ask 4-5
Average
1.73
0.86
0.71
0.62
0.59
0.80
0.66
0.59
0.55
St. Dev.
2.13
1.38
1.12
0.97
0.88
1.28
1.03
0.91
0.83
Min.
0.01
0.01
0.01
0.01
0.01
0.01
0.01
0.01
0.01
Median
1.04
0.15
0.19
0.20
0.22
0.18
0.21
0.21
0.22
Max.
196.02
186.95
95.53
107.28
107.28
126.24
91.34
126.17
77.25
Binding
37.39
36.45
29.68
27.09
23.53
34.17
27.61
25.93
23.15
in the order book. For instance, the absolute distance between the best and second best quote is on
average 0.80 USD on the ask side and 0.86 USD on the bid side. These empty price levels are caused by
the tick size of 0.01 USD, which in relative terms, corresponds to only about 0.0025 bps of the bitcoin
price. This negligible relative tick size makes bitcoin similar to (very) small-tick stocks for which the
limit order book is usually sparse and exhibits many empty price levels.
4
Permanent Price Impact
In this section, we study in detail permanent price impacts and price discovery contributions of all
order ﬂow components – market orders, limit order submissions and limit order cancellations. However,
for now, we ignore the state of the order book that prevails when the respective action occurs. That is,
we do not take into account, for example, whether the order book is imbalanced or whether the bid-ask
spread is narrow. Therefore, throughout this section, we assume in the RL model that there is only
one possible market state (i.e. open). This way, we obtain price impact estimates that are averaged
over all possible states of the order book. In Section 5, we will then take into account diﬀerent market
states and analyse their inﬂuence on price impact.
Due to the sheer size of our order book data, it is computationally not feasible for us to train
the RL model and compute block-bootstrapped conﬁdence intervals based on the entire sample period
from 1 February to 31 May 2022. Therefore, we randomly choose the week from 18 to 24 April as a
representative interval in our sample period for which results are presented in this section. Limiting
the timeframe to this seven-day period allows us to train the model in a reasonable amount of time,
while still leading to very tight conﬁdence intervals and reducing the impact of possible day-of-the-week
eﬀects. To justify our procedure, Figure 1 depicts the evolution of permanent price impact over our
sample period, that is, we train the RL model and estimate price impact separately for each of the 120
days in our sample period. We see that the price impact of all trading actions is signiﬁcantly elevated
during the high-volatility regimes from mid-February to mid-March and the beginning of May. Overall
however, the permanent price impact estimates are quite consistent and the ranking of individual
actions by the magnitude of their impacts varies very little, substantiating our procedure of focussing
on a representative week.
Figure 2 depicts the evolution of the BTCUSD mid price on Coinbase between 18 and 24 April
9
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 10

Figure 1 Permanent Price Impact Over Time
The ﬁgure displays the permanent price impacts (in basis points), estimated separately for each day in our sample period
from 1 February to 31 May 2022. To increase visibility, we only show the impacts of market orders (MO), price-improving
limit order submissions (LO Sub), and price-worsening limit order cancellations (LO Canc).
2022. After a temporary initial drop in the morning of 18 April from almost 40,000 USD to below
39,000 USD, the price steadily increased and peaked at slightly below 43,000 USD in the afternoon
of 21 April. After that, it dropped again to about 39,500 USD during the afternoon of 22 April and
remained at this level until the end of the week.
The earliest microstructure models such as Kyle (1985) suggest that only trades carry information.
Therefore, we start our analysis by quantifying the permanent price impact of market orders in Section
4.1. Initially, we consider only the order sign of trades in our model. In a second analysis, we then
diﬀerentiate market orders based on their size to examine the relationship between permanent price
impact and trade size. In Section 4.2, we then incorporate limit order acitivity and train the model
on all order ﬂow components – market orders, limit order submissions, and limit order cancellations –
jointly. Since limit orders are more nuanced than market orders, we ﬁrst train a model including order
sign and aggressiveness. Then, we additionally diﬀerentiate all orders based on their size. Finally,
in Section 4.3, we analyse the intraday pattern of permanent price impact and price discovery on
Coinbase.5
4.1
Market Orders
We start by analysing the price impact of market orders (trades). To this end, we train the RL model
with the most simple action space – submitting a buy market order and submitting a sell market order.
In contrast to the traditional basic VAR used for example in Chaboud et al. (2021), the RL approach
is able to distinguish between buy and sell market orders and therefore, it yields diﬀerent estimates for
5Due to the very large sample size, the conﬁdence intervals of all estimates are very tight and therefore, to increase
visibility, we do not show them in the ﬁgures of this paper.
10
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 11

Figure 2 BTCUSD Mid Price
The ﬁgure displays the second-by-second mid price of BTCUSD on Coinbase from 18 to 24 April 2022.
the two types of orders.6 Table 3 reports the permanent price impact estimates for buy and sell market
orders (in basis points) together with block-bootstrapped conﬁdence intervals and standard errors, as
well as the number of observations for each action. We observe a statistically signiﬁcant asymmetry,
with sell market orders having a higher price impact (in absolute terms), and consequently carrying
more information, than buy market orders. While sell-initiated orders reduce the mid price by about
0.14 basis points, orders originating from the buy side lead to an increase of only 0.09 bps in the mid
price. Figure 1 shows that this asymmetry is not unique to the representative week from 18 to 24
April, but it persists throughout the entire sample period.
Such an asymmetry is not reported in other price discovery studies. In fact, Fleming et al. (2018)
even show that for US Treasury securities, permanent price impact is not signiﬁcantly diﬀerent for buy
and sell trades. We suppose that the asymmetry in Table 3 is related to the investor structure in the
cryptocurrency space. In most asset classes, retail investors play a minor role. For example, in US
equity markets, retail trading is reponsible for less than 20% of the total trading volume.7 In crypto
markets however, retail investors take on a signiﬁcant role, with their trading accounting for one third of
the total trading volume on Coinbase.8 Moreover, in contrast to traditional asset classes, smaller retail
investors have repeatedly triggered strong bubble-like price increases in the cryptocurrency space.9
Therefore, we suppose that the observed asymmetry in price impact is caused by highly unidirectional
retail order ﬂow on Coinbase. Retail investors have a rather positive view on the future of bitcoin
– or are possibly even driven by the fear of missing out on large proﬁts – and thus, they prefer to
buy, rather than sell, bitcoin. Since this type of investors is usually less informed than institutions,
6The VAR model can be expanded to distinguish between buy and sell market orders as in (Fleming et al., 2018) but
this increases the number of coeﬃcients, and thus the estimation time, exponentially (Philip, 2020).
7See Bloomberg on 17 November 2021.
8See Financial Times on 13 May 2022. Since Coinbase is the most established cryptocurrency exchange and thus quite
attractive for institutions, the retail trading volume is likely to be higher on other unregulated exchanges.
9See Financial Times on 28 June 2022.
11
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 12

Table 3 Permanent Price Impact: Market Orders – Trade Sign
The table reports the permenant price impact estimates (in basis points) for market orders, together with bootstrapped
conﬁdence intervals and standard errors, as well as the number of observations for each action. The conﬁdence intervals
and standard errors are computed from 100 simulations following the block bootstrapping procedure described in Philip
(2020).
Action
Count
Price Impact
Lower 2.5%
Upper 2.5%
St. Err.
Sell
792,735
−0.1419
−0.1434
−0.1407
0.0007
Buy
1,295,979
0.0868
0.0859
0.0879
0.0005
the large proportion of buy transactions initiated by retail traders reduces the information content,
and consequently the permanent price impact, of buy-inititiated market orders, causing the asymmetry
documented in Table 3. Such a hypothesis is very diﬃcult to conﬁrm empirically since only proprietary
exchange data would allow us to conduct appropriate tests. However, the summary statistics on trade
sizes in Table 1 lend some credence to our hypothesis. While there are signiﬁcantly more market orders
originating from the bid side than from the ask side, the average size of sell-initiated market orders is
more than 60% larger than that of buy-initiated orders.10 Since small trades are usually considered a
proxy for retail trading (Han and Kumar, 2013), this signiﬁcant diﬀerence in trade size supports our
hypothesis that the asymmetry in permanent price impact of buy and sell market orders is caused by
retail traders being mainly on the buy side of the transaction.
Compared to Brogaard et al. (2019) and Philip (2020) who study price impact on Canadian and
Australian equity markets, respectively, and document impacts between −3.06 bps and 3.25 bps, the
order of magnitude of the permanent price impacts in Table 3 is very small. The reasons for this
diﬀerence are trading frequency and tick size. As documented by Hautsch and Huang (2012), the
strength of market responses is negatively correlated to trading frequency and positively inﬂuenced
by relative tick size. Comparing the trading frequency of Australian and Canadian equities to that of
BTCUSD on Coinbase, we ﬁnd a massive diﬀerence. The most traded stock in Philip (2020) exhibits
about 280,000 trades during a two-month period, while the average daily number of transactions for
Canadian stocks included in Brogaard et al. (2019) is less than 5,000. In contrast, our dataset on
BTCUSD includes more than two million transactions within the representative week from 18 to 24
April. Moreover, Coinbase has a tick size of 0.01 USD which in relative terms corresponds to only
about 0.002 to 0.003 bps of the BTCUSD price. In contrast, Australian and Canadian equities included
in Brogaard et al. (2019) and Philip (2020) typically exhibit a relative tick size of more than one basis
point. Following Hautsch and Huang (2012), both of these features – the high number of transactions
and the negligible relative tick size – contribute to the small magnitude of permanent price impacts in
BTCUSD. In fact, the price impact estimates in Table 3 are of a similar magnitude as those in Chaboud
et al. (2021) who document an average impact of about 0.1 bps for market orders in euro-dollar trading
on Electronic Broking Services (EBS) during the period from 2008 to 2017.
It is well documented that the price impact of a trade is positively correlated with its size, with many
studies reporting a concave functional relationship between trade size and price impact (Cont et al.,
2014; Philip, 2020). However, within the crypto market, little to no research has been conducted to
10Note that this size diﬀerence between buy and sell transactions does not explain the asymmetry in Table 3. The next
analysis shows that a sell trade has a signiﬁcantly larger impact than a buy trade of the same size.
12
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 13

investigate this issue. The only notable study dealing with price impact within crypto markets is Donier
and Bonart (2015) who analyse the price impact of meta orders on the now-defunct cryptocurrency
exchange Mt. Gox, conﬁrming the well-documented square-root relationship between price impact and
trade size for meta orders. It is worth mentioning however that (i) this study focusses on the impact
of meta orders and (ii) at the time of the study, the crypto market was still in its infancy and has
transformed signiﬁcantly since then. Therefore, we examine the relationship between permanent price
impact and trade size within today’s crypto market more closely.
To incorporate trade sizes, we expand the action space of the previous RL model by quantizing the
size of market orders. Speciﬁcally, we divide orders into six quantile groups depending on their size
and deﬁne submissions of orders in each group as a separate action. This additional diﬀferentiation
expands the action space of the RL model from two to twelve actions (six quantile groups for buy
orders and six quantile groups for sell orders).11 Table 4 reports the resulting price impact estimates,
conﬁdence intervals, standard errors as well as the number of observations for each action. We see that
permanent price impact is generally increasing in signed trade size. For example, a very small buy
trade (Q1) exhibits a price impact of 0.05 bps, whereas a very large buy transaction (Q6) moves the
mid price by 0.30 bps. Similarly, the smallest sell trades (Q1) lead to a decrease of 0.09 bps in the mid
price, while large sell-initiated trades (Q6) exhibit an impact of 0.32 bps. Moreover, we see that the
asymmetry in permanent price impact between buy and sell transactions that we already documented
in Table 3 persists across all order size groups. That is, sell-initiated market orders have a higher
absolute price impact, and thus contain more information, than buy market orders of the same size.
As explained above, we suppose that this asymmetry is related to retail investors being mainly on the
buy side of transactions. Further supporting this hypothesis, Table 4 shows that in the ﬁrst ﬁve order
size groups, there are signiﬁcantly more buy-initiated transactions, while in the top quantile group, sell
trades predominate. Finally, it is worth mentioning that permanent price impact is not monotonically
increasing in signed order size. Rather small market orders (Q2) exhibit a lower absolute impact than
very small trades in the ﬁrst quantile size group. This artefact seems however to be related to the
interaction between trades and limit orders, since it disappears (or is at least greatly reduced) once we
incorporate limit order activity in the RL model in Section 4.2.
Figure 3 displays the permanent price impact of buy and sell trades as a function of their signed
size, i.e. sell-initiated market orders are depicted by negative trade sizes. It is clearly visible that the
relationship between permanent price impact and trade size is not linear, but rather concave. That is,
price impact is overall increasing with trade size, but the rate of increase reduces as trade size grows,
which implies that small trades exhibit in relative terms a lower impact than large transactions. This
ﬁnding is consistent with Philip (2020) and conﬁrms their conclusion that the basic linear VAR with
trade size as measure for market order ﬂow might lead to erroneous conclusions about permanent price
impact.
11For consistency and comparability, the quantile groups are computed across all trades, instead of separately for buy
and sell transactions.
13
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 14

Table 4 Permanent Price Impact: Market Orders – Trade Size
The table reports the permanent price impact estimates (in basis points) for market orders, depending on their size.
Orders are divided into quantile groups (Q1 to Q6) depending on their size. The conﬁdence intervals and standard errors
are computed from 100 simulations following the block bootstrapping procedure described in Philip (2020).
Action
Size
Count
Price Impact
Lower 2.5%
Upper 2.5%
St. Err.
Sell
Q1
115,554
−0.0921
−0.0937
−0.0902
0.0009
Q2
103,422
−0.0664
−0.0678
−0.0649
0.0008
Q3
135,293
−0.1249
−0.1271
−0.1227
0.0011
Q4
111,772
−0.1005
−0.1023
−0.0989
0.0009
Q5
148,347
−0.1469
−0.1490
−0.1449
0.0011
Q6
178,347
−0.3169
−0.3212
−0.3127
0.0023
Buy
Q1
232,565
0.0469
0.0460
0.0481
0.0005
Q2
244,697
0.0423
0.0413
0.0435
0.0006
Q3
212,826
0.0710
0.0695
0.0725
0.0008
Q4
236,347
0.0590
0.0580
0.0601
0.0006
Q5
199,772
0.1138
0.1122
0.1152
0.0008
Q6
169,772
0.2997
0.2953
0.3042
0.0024
4.2
Limit Order Activity
The earliest microstructure models such as Kyle (1985) assume that only trades contain and trans-
mit information. However, since most modern markets operate a limit order book where all market
participants can provide liquidity, this assumption is not reasonable anymore. Therefore, more recent
models such as Rosu (2020) also allow limit orders to carry information. Recent studies empirically
support this new approach to information transmission within ﬁnancial markets (Brogaard et al., 2019;
Chaboud et al., 2021). However, nothing is yet known about the role of limit orders within the crypto
market. We ﬁll this gap by providing detailed insights on the importance of limit order activity in
terms of information transmission.
In contrast to the previous section, we now include all order ﬂow components (market orders, limit
order submissions, limit order cancellations) jointly. However, compared to market orders, limit order
activity is more nuanced. Due the additional dimension of the limit price, a classiﬁcation of limit
orders solely by their sign would be far too general to assess their information content accurately.
Therefore, we additionally diﬀerentiate both submissions and cancellations based on their aggressive-
ness, measured as the signed distance to the best quote on the same side of the order book. More
speciﬁcally, we apply the following classiﬁcation to limit order activity. Submissions are divided into
ten predeﬁned bins depending on their distance to the best same-side quote.12 The exact deﬁnitions
of the bins can be seen in Table 5. Here, the ﬁrst bin captures submissions with a negative distance
to the best quote, which corresponds to price-improving submissions. Limit order cancellations are
divided into the same predeﬁned bins, but since they can by deﬁnition not occur at a price better than
the best quote, the ﬁrst distance-to-best bin is redundant and can be removed, reducing the number of
bins to nine. Nevertheless, a cancellation can still lead to an immediate change in the mid price, given
12Previously, we divided trade sizes into quantile groups. While this classiﬁcation is still possible for the distance to
the best same-side quote, we prefer to divide limit order submissions in predeﬁned bins rather than quantile groups, since
the vast majority of limit order activity takes place around the best quotes and therefore the distribution of the distance
to the best same-side quote is heavily right-skewed.
14
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 15

Figure 3 Permanent Price Impact of Market Orders
The ﬁgure displays the permanent price impact estimates (in basis points) for market orders as a function of signed order
size. Note that sell market orders are reported with negative trade sizes.
that it occurs at the best quote and there is no other limit order resting at this price. According to
Brogaard et al. (2019), such price-worsening cancellations exhibit signiﬁcantly diﬀerent price impacts.
Therefore, to capture this diﬀerence, we split cancellations occurring at the best quotes further, de-
pending on whether they are price-worsening (i.e. their immediate impact is not zero) or immediately
leave the best quote unchanged (i.e. zero immediate impact).13 As in the previous section, market
orders are classiﬁed solely based on their sign.14 Table 5 illustrates the 42 actions resulting from this
diﬀerentiation of market and limit order activity.
Having deﬁned the action space properly, we can now train the RL model. The resulting estimates
of permanent price impact are reported in Table 6. In addition, it displays the relative contribution
of each action to the total amount of price variation, as deﬁned in Equation (3). We see that market
orders individually carry much more information than limit order submissions, even in case the latter
improve on the best quotes. Speciﬁcally, buy (sell) market orders move the mid price by 0.06 bps
(−0.11 bps) and thus carry two to three times as much information as submissions of limit orders
inside the spread. Compared to limit order cancellations however, the dominance of market orders is
not that pronounced. The impact of a price-worsening buy limit order cancellation is about −0.1 bps
and therefore, more than 90% of the impact of a sell-initiated market order.15 On the ask side, the
13Note that for submissions, such a diﬀerentiation by immediate impact is already contained in the distance-to-best
classiﬁcation since submissions with a negative distance to the best same-side quote are price-improving and will by
deﬁnition immediately impact the mid price.
Also, limit order actions behind the best quotes will not immediately
change the best quote and thus, they always exhibit a zero immediate impact.
14As in Brogaard et al. (2019), it would also be possible to diﬀerentiate market orders further based on whether they
consume all liquidity available on the best quote. However, in order to stay consistent with Chaboud et al. (2021) and
to not distort results too much by liquidity eﬀects, we decided to include only the order sign as diﬀerentiating factor. As
robustness check, we also trained the RL model where market orders are diﬀerentiated based on whether they consume
all available liquidity, but the results – especially the price discovery contributions – are qualitatively very similar to those
presented here.
15We compare buy (sell) limit order cancellations to sell-initiated (buy-initiated) market orders since their trading
15
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 16

Table 5 RL Model – Action Space
The table illustrates the classiﬁcation of market and limit order activity. Market orders (MO) are diﬀerentiated based
on order sign, limit order submissions (LO Sub) and limit order cancellations (LO Canc) are classiﬁed by order sign and
signed distance to the best same-side quote (DTB; in USD). In addition, cancellations at the best quotes are diﬀerentiated
based on whether they lead to an immediate change in the mid price (Worsening) or leave it unchanged (Matching). Note
that the submission of a limit order with negative distance to the best quote improves the mid price by deﬁnition.
Criterion
Possible Values
MO
LO Sub
LO Canc
Order Sign
Buy
✓
✓
✓
Sell
✓
✓
✓
DTB
< 0
Improving
✓
0
Worsening
✓
0
Matching
✓
✓
0.01
✓
✓
0.02−0.05
✓
✓
0.05−0.10
✓
✓
0.10−0.25
✓
✓
0.25−0.50
✓
✓
0.50−1.00
✓
✓
1.00−2.00
✓
✓
2.00−3.00
✓
✓
≥2
✓
✓
price impact of 0.09 bps is even larger than that of buy market orders. However, this large impact of
cancellations seems to be of rather mechanical nature. The extremely small relative tick size of less than
0.003 bps on Coinbase leads to a very high granularity of the order book, which in turn leads to many
empty price levels and thus, to often quite large price gaps behind the best quotes. According to Table
2, there are on average 80 empty price levels between the best and second best quote. These gaps then
cause price-worsening cancellations at the best quotes to have a comparatively large immediate price
impact. Speciﬁcally, during the representative week from 18 to 24 April, price-worsening cancellations
exhibit an immediate impact of 0.086 bps for sell orders and −0.095 bps for buy orders, which is more
than 96% of the the permanent price impact reported in Table 6. Therefore, a large portion of the
high permanent price impact of cancellations can be attributed to a high immediate impact caused by
the extremely small relative tick size.16
The most important takeaway from Table 6 is however that since limit order actions are far more
numerous, the contribution of market orders to the total price variation is only about 16% and therefore
much lower than that of limit order submissions (50%) and cancellations (34%). In total, limit order
actions changing the best quotes (price-increasing submissions and price-worsening cancellations) con-
tribute more than 71% to the total price variation and therefore, they are clearly the most important
order ﬂow instrument with regards to price discovery. More speciﬁcally, of that 50% contributed by
limit order submissions, 87% comes from orders undercutting the best quotes, while price-worsening
cancellations are responsible for 82% of the contribution caused by limit order cancellations (34%). In
directions coincide.
16Since we do not diﬀerentiate market orders based on whether they consume all liquidity available at the opposite-side
best quote, the inﬂuence of this mechanical feature is reduced. For limit order submissions on the other hand, price gaps
behind the best quotes are not relevant and the majority of undercutting limit orders are placed just one tick above the
best bid or below the best ask, leading to an immediate impact of 0.01 USD.
16
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 17

general, this ﬁnding is in line with recent empirical studies including Collin-Dufresne and Fos (2015),
Fleming et al. (2018), Brogaard et al. (2019), and Chaboud et al. (2021).
There are two cost-related reasons for the pronounced importance of (price-improving) limit order
submissions with regards to information transmission. The ﬁrst one is trading costs. Fees on Coinbase
follow a tiered maker-taker model. Depending on the market participant’s 30-day trading volume,
liquidity-taking orders face fees ranging from 60 bps to 5 bps, while orders that add liquidity to the
book are charged at most only 40 bps and for highest-volume traders, they are even free of charge.17
This fee structure naturally makes submitting limit orders more attractive compared to market orders:
in order to overcome transaction costs, the trader’s informational advantage needs to be signiﬁcantly
greater for market orders than for limit orders. The second reason for informed investors to use price-
improving limit orders is the tick size. As already mentioned above, Coinbase has a tick size of 0.01
USD which in relative terms corresponds to only about 0.0025 bps, leading to an extreme granularity of
the order book. This granularity allows market participants to undercut limit orders of other traders,
and consequently gain price priority, at very low costs, which reduces the importance of submissions at
the best quotes and makes price-improving limit order submissions highly attractive (Dyhrberg et al.,
ming). In this context, Chaboud et al. (2021) conduct event studies on EBS and document that the
tick size has a signiﬁcant impact on the importance of limit order activity. The decimalization – i.e.
the reduction of tick size by a factor of ten – in the euro-dollar pair in 2011 strongly reduced (increased)
the importance of limit order ﬂow at the best quotes (inside the spread). The ”half-pip” rule that
was implemented in 2012 and partially reversed the decimalization policy lead to an increase in the
information content of limit orders submitted at the best quotes. Hence, on Coinbase, price-improving
limit order submissions are attractive for informed investors not only due to lower transaction fees but
also due to the very low costs of gaining priority over other market participants.
Another factor for the pronounced importance of limit order activity is the structure of the crypto
market. With more than 300 spot trading venues and about 40 derivatives exchanges, the crypto
market is extremely fragmented.18 In addition, unlike traditional equity markets, where for example
the National Best Bid and Oﬀer (NBBO) regulation of the Securities and Exchange Commission (SEC)
ensures that market participants receive the best price when executing trades, the still-unregulated
crypto market does not oﬀer a mechanism connecting multiple exchanges. Due to the absence of such a
uniﬁed framework, there is great potential (and need) for cross-exchange market making and arbitrage
activities within the crypto market (Makarov and Schoar, 2020). Typically, such strategies involve a
large number of limit order submissions and cancellations – especially in light of the larger fees for
market orders – in order to incorporate information learned from other (faster) exchanges (Van Kervel,
2015; Shkilko and Sokolov, 2020), leading to the large information content of limit order activity.
A more fundamental possible factor for the importance of limit order activity is related to the
works of Bloomﬁeld et al. (2005) and Rosu (2020). They argue that the informed traders’ order choice
depends on the value of their information. If their privately observed mispricing, deﬁned as the diﬀer-
ence between the privately observed fundamental value of the asset and the public expectation of the
17The exact fee structure can be found on Coinbase.
18According to coinmarketcap.com.
17
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 18

fundamental value, is large enough, they demand liquidity, otherwise they provide liquidity. However,
for cryptocurrencies, there is far no public consensus on their fundamental value. Most recently, Biais
et al. (2022) determine the fundamental value of cryptocurrencies as their stream of net transactional
beneﬁts, which depend on their future prices. From this, they conclude that cryptocurrencies exhibit
multiple equilibria and extrinsic volatility, i.e. prices ﬂuctuate even when fundamentals are constant.
On the basis of this, it is far from trivial for informed agents to determine the mispricing and con-
sequently, speculation plays a greater role. However, as shown by Goettler et al. (2009), speculators
prefer providing liquidity over demanding it, leading to the high information content of limit order
activity.
For limit order submissions, Table 6 shows that price-improving actions are clearly most important.
With impacts of ±0.03 bps, submissions inside the spread contribute about ten times as much as
submissions at the best quotes. Behind the best quotes, submissions consistently have absolute price
impacts of less than 0.004 bps and in total contribute only about 4% to price discovery. These results
are in line with Brogaard et al. (2019) who for Canadian equities, identify orders improving on the
NBBO as the most important ones and ﬁnd limit order activity behind the best quotes contributing very
little to price discovery. In comparison to the results by Chaboud et al. (2021) however, the permanent
price impact estimates of limit order submissions in Table 6 are of small magnitude. For example,
during the last year of their sample, Chaboud et al. (2021) ﬁnd price-improving limit orders to exhibit
price impacts of around 0.075 bps. The reason for this discrepancy is again the tick size. According
to Hautsch and Huang (2012), the impact of price-improving limit order submissions increases with
relative tick size. Since euro-dollar trading on EBS exhibits a relative tick size of close to one basis point
– which is signiﬁcantly larger than the relative tick size for BTCUSD on Coinbase – an undercutting
limit order has a larger price impact for EURUSD on EBS than for BTCUSD on Coinbase.
Interestingly, limit orders submitted more than two dollars away from the best quote have price
impacts opposite their order sign. As argued by Brogaard et al. (2019) who also observe this behaviour,
this does not imply that an order placed very deep in the book causes the mid price to move, but
the order rather predicts the movement. That is, orders are placed deep in the book (to gain priority
over other market participants) when the mid price is about to move in the appropriate direction. For
example, when the mid price is about to increase, or already has started to increase, traders might
place a sell limit order at a rather high price in order to gain order book priority, which would cause
the sell limit order to exhibit a positive price impact. Interestingly, if we partition aggressiveness of
limit order submissions more granularly, the results (not presented here) indicate a certain asymmetry
in the distance from the best quote at which such ”predicting” orders are placed. On the ask side, we
observe a positive price impact for orders submitted two to ten dollars above the best ask quote. On
the bid side however, the price impact is negative for all orders submitted more than two dollars below
the best bid price. We think that this asymmetry might be related to the leverage eﬀect of volatility
that has also been identiﬁed for cryptocurrency markets (Alexander et al., 2021). When the bitcoin
price starts to decrease, market participants expect higher volatility, and consequently place their limit
orders further away from the best quote, compared to when the price starts to increase.
Finally, we note that apart from very deep in the book, the impact of cancellations behind the best
18
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 19

quotes coincides with their sign, i.e. the cancellation of a buy (sell) limit order is associated with an
increase (decrease) in the mid price. When training the RL model containing only cancellations (results
not presented here), we do not observe this behaviour. Instead, we ﬁnd small but signiﬁcant price
impacts opposite to the order sign, that is, cancelling a buy (sell) limit order behind the best quotes
leads to an increase (decrease) in the mid price. This indicates that the change in sign of permanent
price impacts is caused by the interaction between trades, limit order submissions and cancellations.
Due to the recursive architecture of the RL model, the impact of market and limit orders that follow a
cancellation are partially attributed to the cancellation, which oﬀsets and overcomes the small impacts
of cancellations behind the best quotes. However, similar to submissions, limit order cancellations
behind the best quotes exhibit very small absolute price impacts of less than 0.004 bps and despite
their abundance, contribute only about 6% to price discovery.
Similar to the previous section, we now investigate how order size aﬀects permanent price impact
when all order ﬂow components are considered jointly. To this end, we once more divide all orders
into six quantile groups depending on their size.19 However, in light of the results in Table 6, we only
include limit order submissions and cancellations occurring within the spread or at the best quotes.
Since activities behind the ﬁrst level contribute only very little to price discovery, this does not change
our results signiﬁcantly. Nevertheless, we still keep the diﬀerentiation of limit order activity from the
previous analysis. That is, limit order submissions are stratiﬁed based on whether they occur inside
the spread (i.e.
improve the best quote) or at the best quote (i.e.
match the best quote), while
cancellations at the best quotes are classiﬁed by whether they lead to an immediate change in the mid
price (i.e. worsen the best quote) or leave it unchanged (i.e. match the best quote). Consequently,
the action space of the RL model includes 60 elements – two order signs and six order size groups
for market orders and two order signs, two diﬀerent immediate mid price reactions, and six order size
groups for both limit order submissions and cancellations.
The results of the RL model are reported in Table 7. Overall, they conﬁrm and expand our previous
ﬁnding on the pronounced importance of limit order activity with regards to information transmission.
The permanent price impact of market orders is still signiﬁcantly larger than that of limit order
submissions, regardless of whether the latter improve the best quote. Speciﬁcally, depending on the
order size, the impact of sell market orders is 2.2 to 3.6 times the impact of a price-improving sell
limit order of similar size and even 3.9 to 8.8 times the impact of a price-matching limit order. On
the bid side, the discrepancy shows a higher variation, with buy-initiated market orders exhibiting
impacts of 1.1 to 3.7 (2.2 to 10.6) times the impact of price-improving (price-matching) limit orders
of similar size. However, if we take into account the number of limit order submissions in each order
size group, roles are reversed. Across all groups, submissions of price-improving limit orders contribute
signiﬁcantly more to price discovery than market orders. For instance, submissions of very small price-
improving buy limit orders (Q1) contribute about 2.9%, whereas buy-initiated market orders of similar
size exhibit price discovery contributions of only 1.4%. In some cases, even price-matching submissions
at the best quotes contribute more than market orders.
Due to the large price impact of limit order cancellations, that is mostly of mechanical nature,
19For the sake of consistency, we determine the quantile groups across all components rather than for each one separately.
19
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 20

Table 6 Permanent Price Impact: Market and Limit Orders
The table reports the permanent price impact estimates (in basis points) for market orders (MO), limit order submissions
(LO Sub) and limit order cancellations (LO Canc), together with bootstrapped conﬁdence intervals and standard errors,
as well as the number of observations for each action. Market orders are diﬀerentiated solely on their sign, limit order
submissions are distinguished by both their sign and their aggressiveness, and cancellations of limit orders are classiﬁed
by their sign, their aggressiveness and whether they lead to an immediate change in the mid price (Worsening) or leave
it unchanged (Matching). Note that a negative distance to the best same-side quote for limit order submissions indicates
that the order improves upon the best same-side quote (Improving). The conﬁdence intervals and standard errors are
computed from 100 simulations following the block bootstrapping procedure described in Philip (2020). RC represents
the relative contribution of each action to the total amount of price variation (in %), computed as in Equation (3).
Action
DTB
Mid Price
Count
Impact
Lower 2.5%
Upper 2.5%
St. Err.
RC
Sell
MO
0
792,735
−0.1084
−0.1091
−0.1078
0.0004
8.26
LO Sub
< 0
Improving
6,414,655
−0.0346
−0.0348
−0.0344
0.0001
21.33
0
Matching
3,141,497
−0.0034
−0.0034
−0.0034
< 10−4
1.03
0.01
425,090
−0.0030
−0.0031
−0.0030
< 10−4
0.12
0.02−0.05
343,424
−0.0028
−0.0029
−0.0027
< 10−4
0.09
0.05−0.10
319,928
−0.0035
−0.0036
−0.0034
< 10−4
0.11
0.10−0.25
693,542
−0.0035
−0.0035
−0.0034
< 10−4
0.23
0.25−0.50
1,042,044
−0.0029
−0.0029
−0.0028
< 10−4
0.29
0.50−1.00
1,685,528
−0.0020
−0.0021
−0.0020
< 10−4
0.33
1.00−2.00
2,825,264
−0.0010
−0.0010
−0.0010
< 10−4
0.28
≥2
21,055,363
0.0002
0.0002
0.0002
< 10−4
0.44
LO Canc
0
Worsening
1,573,868
0.0893
0.0889
0.0897
0.0002
13.51
0
Matching
1,135,575
< 10−4
−0.0001
< 10−4
< 10−4
0.00
0.01
1,118,259
−0.0014
−0.0014
−0.0013
< 10−4
0.15
0.02−0.05
1,527,963
−0.0033
−0.0033
−0.0032
< 10−4
0.48
0.05−0.10
755,359
−0.0032
−0.0033
−0.0032
< 10−4
0.23
0.10−0.25
1,129,161
−0.0030
−0.0030
−0.0029
< 10−4
0.33
0.25−0.50
1,447,087
−0.0021
−0.0022
−0.0021
< 10−4
0.30
0.50−1.00
2,259,387
−0.0015
−0.0015
−0.0015
< 10−4
0.33
1.00−2.00
3,659,924
−0.0008
−0.0008
−0.0008
< 10−4
0.29
≥2
22,324,451
0.0001
0.0001
0.0001
< 10−4
0.19
Buy
MO
0
1,295,979
0.0630
0.0626
0.0635
0.0002
7.86
LO Sub
< 0
Improving
7,634,526
0.0305
0.0304
0.0307
0.0001
22.40
0
Matching
4,193,746
0.0032
0.0031
0.0032
< 10−4
1.28
0.01
584,536
0.0028
0.0028
0.0028
< 10−4
0.16
0.02−0.05
469,613
0.0022
0.0021
0.0023
< 10−4
0.10
0.05−0.10
446,759
0.0030
0.0029
0.0031
< 10−4
0.13
0.10−0.25
848,514
0.0030
0.0030
0.0031
< 10−4
0.25
0.25−0.50
1,146,475
0.0024
0.0024
0.0024
< 10−4
0.26
0.50−1.00
1,729,113
0.0015
0.0015
0.0016
< 10−4
0.26
1.00−2.00
2,619,198
0.0007
0.0007
0.0008
< 10−4
0.18
≥2
21,798,480
−0.0004
−0.0004
−0.0004
< 10−4
0.81
LO Canc
0
Worsening
1,488,842
−0.0988
−0.0991
−0.0984
0.0002
14.15
0
Matching
1,316,697
0.0001
0.0001
0.0002
< 10−4
0.02
0.01
1,452,636
0.0019
0.0019
0.0019
< 10−4
0.27
0.02−0.05
2,365,114
0.0038
0.0038
0.0038
< 10−4
0.86
0.05−0.10
1,117,042
0.0035
0.0034
0.0035
< 10−4
0.37
0.10−0.25
1,561,111
0.0033
0.0032
0.0033
< 10−4
0.49
0.25−0.50
1,745,226
0.0022
0.0022
0.0023
< 10−4
0.38
0.50−1.00
2,516,970
0.0015
0.0014
0.0015
< 10−4
0.35
1.00−2.00
3,651,241
0.0007
0.0007
0.0007
< 10−4
0.24
≥2
23,303,142
−0.0004
−0.0004
−0.0004
< 10−4
0.88
20
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 21

market orders exhibit a smaller impact than price-worsening cancellations across the ﬁrst three order
size groups (Q1−Q3).
However, for larger order sizes (Q4−Q6), market orders cause a mid price
movement that is 1.2 to 2.5 times larger than that associated with price-worsening cancellations. For
example, a very large buy-initiated market order increases the mid price by 0.24 bps, whereas the
price-worsening cancellation of a similarly-large sell limit order exhibits a price impact of only 0.1 bps.
However, analogous to submissions, price-worsening limit order cancellations are much more frequent,
and therefore, apart from the largest order size group (Q6), they contribute signiﬁcantly more to price
discovery than market orders.
Finally, we note that price-matching cancellations of moderate to large size (Q3−Q6) exhibit a
permanent price impact whose direction coincides with their order sign, i.e. buy (sell) cancellations
are associated with an increase (decrease) in mid price. A close examination of the data shows that
these cancellations are remarkably often followed by submissions of price-matching (and to a lesser
extent, also price-improving) limit orders on the same order book side and in the same order size
group. Due to the recursive architecture of the RL model, this causes the permanent price impact of
cancellations to change its sign. Such sequences of cancellations and resubmissions are either driven by
queue positioning (traders learn that their order is too far down the queue, decide to cancel the order
and submit a new order undercutting the best quote) or order modiﬁcations (Coinbase does not allow
limit orders to be modiﬁed and thus, if traders want to modify the volume of an already submitted
limit order, they have to cancel this existing order and submit a new one).
Figure 4 depicts the permanent price impacts of all three order ﬂow components as a function of
signed order size and highlights the large diﬀerences in price impact between the individual components.
The price impact of market orders is still an increasing and concave function of trade size, but compared
to Figure 3, the curve appears much smoother now that limit order actions are included in the RL
model. For limit order submissions, the functional shape of permanent price impact resembles a sigmoid
function, with an apparent limit to which the price impact of limit orders converges. For submissions
improving on the best quotes, this limit is around ±0.07 bps, whereas the impact of submissions at the
best quotes seems to converge to roughly ±0.02 bps. Besides from disproportionately large values for
very small order sizes, permanent price impact of price-worsening cancellations, as a function of order
size, resembles to some extent a reversed S-shape, similar to a sigmoid function mirrored at the y-axis.
Therefore, apart from the reversed direction and the larger magnitude – which is of rather mechanical
nature – the price impact of price-worsening limit order cancellations is overall similar to that of limit
order submissions undercutting the best quotes.
4.3
Intraday Pattern
In ﬁnancial markets, information are usually not incorporated into prices at a constant rate and
thus, many information-related market variables exhibit a certain intraday variation. Recent studies
of equity markets report an S-shaped intraday pattern in bid-ask spreads where the spread is highest
after opening and then declines throughout the trading day (Upson and Van Ness, 2017). This intraday
shape is usually attributed to index-tracking investors and algorithmic and high-frequency traders who
trade extensively at the end of the trading day to rebalance portfolios and to achieve a close-to-zero
21
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 22

Table 7 Permanent Price Impact: Market and Limit Orders – Order Size
The table reports the permanent price impact estimates (in basis points) for market orders (MO), limit order submissions
(LO Sub) and limit order cancellations (LO Canc) at the best quotes, depending on their order size. Market orders
are diﬀerentiated solely on their sign, limit order submissions and cancellations are distinguished by both their sign and
whether they lead to an immediate change in the mid price (Improving, Worsening) or not (Matching). The components
are additionally divided into quantile groups (Q1 to Q6) depending on their size. The conﬁdence intervals are computed
from 100 simulations following the block bootstrapping procedure described in Philip (2020). RC represents the relative
contribution of each action to the total amount of price variation (in %), computed as in Equation (3).
Sell
Buy
Action
Mid Price
Size
Impact
Lower 2.5%
Upper 2.5%
RC
Impact
Lower 2.5%
Upper 2.5%
RC
MO
Q1
−0.0858
−0.0867
−0.0848
1.60
0.0377
0.0373
0.0381
1.43
Q2
−0.0862
−0.0877
−0.0850
0.61
0.0430
0.0424
0.0437
0.57
Q3
−0.0995
−0.1006
−0.0982
1.03
0.0545
0.0539
0.0550
1.14
Q4
−0.1281
−0.1296
−0.1267
0.93
0.0890
0.0878
0.0899
0.81
Q5
−0.1645
−0.1670
−0.1623
0.71
0.1270
0.1250
0.1289
0.69
Q6
−0.2592
−0.2619
−0.2564
3.33
0.2429
0.2398
0.2457
2.99
LO Sub
Improving
Q1
−0.0305
−0.0308
−0.0303
2.99
0.0331
0.0328
0.0335
2.86
Q2
−0.0251
−0.0253
−0.0249
1.91
0.0213
0.0212
0.0216
2.84
Q3
−0.0336
−0.0339
−0.0334
2.36
0.0287
0.0285
0.0290
2.81
Q4
−0.0481
−0.0484
−0.0477
3.82
0.0425
0.0422
0.0428
3.84
Q5
−0.0737
−0.0742
−0.0733
6.29
0.0658
0.0653
0.0662
6.45
Q6
−0.0722
−0.0728
−0.0715
5.81
0.0667
0.0660
0.0672
5.13
Matching
Q1
−0.0177
−0.0179
−0.0176
0.74
0.0161
0.0159
0.0163
0.67
Q2
−0.0220
−0.0222
−0.0218
0.81
0.0196
0.0194
0.0198
1.23
Q3
−0.0234
−0.0237
−0.0232
0.97
0.0205
0.0203
0.0207
1.40
Q4
−0.0236
−0.0238
−0.0234
0.94
0.0198
0.0196
0.0200
1.01
Q5
−0.0274
−0.0276
−0.0272
1.01
0.0227
0.0224
0.0229
1.02
Q6
−0.0295
−0.0298
−0.0293
1.27
0.0230
0.0228
0.0232
1.16
LO Canc
Worsening
Q1
0.1402
0.1394
0.1411
2.17
−0.1790
−0.1800
−0.1781
2.29
Q2
0.1113
0.1100
0.1124
1.01
−0.1223
−0.1232
−0.1214
1.69
Q3
0.0743
0.0734
0.0750
1.07
−0.0901
−0.0909
−0.0893
1.23
Q4
0.0727
0.0721
0.0733
1.75
−0.0828
−0.0833
−0.0822
1.92
Q5
0.0820
0.0811
0.0829
2.18
−0.0888
−0.0897
−0.0879
2.26
Q6
0.0972
0.0964
0.0979
2.95
−0.1032
−0.1042
−0.1021
2.54
Matching
Q1
0.0065
0.0060
0.0068
0.05
−0.0080
−0.0084
−0.0076
0.07
Q2
0.0030
0.0026
0.0034
0.02
−0.0061
−0.0064
−0.0057
0.06
Q3
−0.0020
−0.0023
−0.0016
0.03
0.0020
0.0018
0.0022
0.03
Q4
−0.0083
−0.0086
−0.0081
0.17
0.0071
0.0069
0.0074
0.17
Q5
−0.0163
−0.0165
−0.0160
0.32
0.0125
0.0123
0.0127
0.28
Q6
−0.0164
−0.0167
−0.0161
0.31
0.0129
0.0126
0.0132
0.25
22
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 23

Figure 4 Permanent Price Impact of Market and Limit Orders
The ﬁgure displays the permanent price impact estimates (in basis points) for market orders (left-hand graph),
limit order submissions inside the spread and at the best quotes (middle graph), and limit order cancellations
at the best quotes (right-hand graph), as a function of signed order size. Note that sell orders are reported with
negative order sizes.
inventory position. In FX markets, which in terms of trading times most closely resemble the crypto
market, Bollerslev and Domowitz (1993) document a slightly elevated bid-ask spread during Asian
trading hours and a rather low spread in European and US trading. Within the crypto market, Dimpﬂ
and Maeckle (2021) and Ghysels and Nguyen (2019) ﬁnd a U-shaped intraday pattern in the bid-ask
spread for BTCEUR and BTCUSD on Kraken and BTC-e, respectively. More recently, Jahanshahloo
et al. (2022) document that trading sessions of the New York Stock Exchange (NYSE) lead bitcoin
trading activity, both on the blockchain and centralised exchanges.
To identify a possible intraday pattern in price discovery, we divide the UTC day into 30-minute
periods and train the RL model from Table 7 for each intraday period separately. Figure 5 depicts the
resulting relative permanent price impacts. That is, for each action, the price impact estimates are
ﬁrst normalised, by dividing by the estimate for the ﬁrst intraday period, and then averaged across
buy and sell. We also include the relative contribution of each 30-minute intraday period to the total
price variation. To increase visibility, we only show the price impact estimates for moderately-sized
orders of the third quantile size group, but the remaining groups exhibit a very similar pattern. In
addition, for limit order activity, only price-changing actions are depicted.20 We see that the intraday
pattern is very similar for all three order ﬂow components. During Asian trading in the early UTC
morning, price impact is generally rather low. When the London Stock Exchange (LSE) then opens
at 07:00 UTC, it jumps up by 20% to 30% and continues to ﬂuctuate around this higher level. At
13:30 UTC, the NYSE opens and we observe a massive jump in price impact during the subsequent
30-minute period. While limit order submissions and cancellations show an increase of 75% and 43%,
20While submissions of price-matching limit orders show a very similar intraday pattern as the actions presented here,
price-matching cancellations do not seem to exhibit signiﬁcant intraday variation.
23
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 24

respectively, the impact of market orders increases by more than 90%. After this peak, price impact
shows a few smaller spikes between 16:30 and 18:30 UTC, but overall exhibits a declining trend and
reaches its minimum around 22:00, i.e. shortly after closing at the NYSE. The intraday pattern of the
relative price discovery contribution coincides with that of permanent price impact. In particular, we
see that the NYSE trading periods are clearly most relevant in terms of price discovery. Especially the
30-minute opening period is highly important and contributes by far the most (5%). This intraday
pattern conﬁrms the ﬁnding of Jahanshahloo et al. (2022) that trading sessions of the NYSE are most
relevant in terms of bitcoin trading activity. Moreover, it resembles the M-shaped intraday pattern of
volatility that is typically observed for FX pairs (Andersen and Bollerslev, 1998). This similarity is
not entirely surprising since the structures of FX and cryptocurrency markets are similar in that both
operate continuously from Monday to Friday and trading is not interrupted overnight.
During the early UTC morning, there is one notable exception to the otherwise quite low price
impact. In the 30-minute period from 04:00 to 04:30 UTC, the price impact strongly increases for all
three order ﬂow components, with trades showing the largest relative jump of almost 60% compared
to the preceding 30-minute interval. This spike is caused by an extremely large trading volume of
almost 700 BTC within a ten-minute interval in the early UTC morning of 18 April 2022. During
this period, the bitcoin price dropped from almost 40,000 USD to below 38,700 USD (see Figure 2).
Following Hautsch and Huang (2012), this extremely large trading volume, paired with the otherwise
comparatively low activity in the market in the early UTC morning, leads to the very high price impact
in Figure 5 between 04:00 and 04:30 UTC.
5
The Inﬂuence of the Order Book
Throughout the previous section, we have ignored the state of the order book that prevails when the
respective action occurs, by assuming that there is only one possible market state (open) in the RL
model. This way, we obtained a permanent price impact estimate for each action that is averaged over
all possible states of the order book. However, it is well documented that in modern ﬁnancial markets,
the shape of the order book carries a signiﬁcant amount of information and inﬂuences the behaviour of
market participants. For example, Cao et al. (2009) document that order imbalances between demand
and supply schedules have signiﬁcant power in predicting short-term returns, even after controlling
for autocorrelations in returns and the bid-ask spread. Similarly, Brogaard et al. (2014) ﬁnd that
high-frequency traders use order book information to demand liquidity. Therefore, in this section, we
investigate how the permanent price impact of individual actions changes depending on the prevailing
order book state.
Formally, we incorporate the state of the order book into the RL model by expanding its state
space appropriately. In particular, we no longer assume that there is only one market state (open)
but we include diﬀerent variables into the state space that characterise the shape of the order book.
The action space is chosen as in Table 7 and is left unchanged throughout this section. That is, all
RL models presented here include all order ﬂow components (market orders, limit order submissions,
limit order cancellations) jointly, where for limit order activity, only those orders that aﬀect the best
24
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 25

Figure 5 Intraday Pattern of Price Impact and Price Discovery
The ﬁgure displays the intraday pattern of permanent price impact and price discovery during the representative week
from 18 to 24 April 2022. The upper graph shows the permanent price impact estimates for moderately-large market
orders, price-moving limit order submissions, and price-worsening cancellations. All estimates are normalised, by dividing
by the estimate for the ﬁrst intraday period, and then averaged across buy and sell. The lower graph depicts the relative
contribution of each 30-minute intraday period to the total price variation, computed similar to Equation (3).
quotes are included. All order ﬂow components are classiﬁed based on their sign and divided into six
quantile groups depending on their size.21 In addition, limit order submissions are stratiﬁed based on
whether they occur inside the spread (i.e. improve the best quote) or at the best quote (i.e. match
the best quote), while cancellations are classiﬁed by whether they lead to an immediate change in the
mid price (i.e. worsen the best quote) or leave it unchanged (i.e. match the best quote). Overall, this
amounts to 60 diﬀerent actions in the RL model. Note that all results presented in this section are
still based on data for the representative week from 18 to 24 April 2022.
21As before, the quantile groups are computed across market orders, limit order submissions, and limit order cancella-
tions jointly, instead of separately for each order type.
25
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 26

5.1
Order Book Imbalance
Many recent theoretical works such as Bhattacharya and Saar (2020) assume order book imbalance to
be informative, with several empirical studies supporting this assumption (Cao et al., 2009; Gould and
Bonart, 2015; Kwan et al., 2021). Within the bitcoin market, Scaillet et al. (2020) document that the
aggressive part of the order ﬂow imbalance predicts price jumps. Therefore, it is most likely that the
price impact of orders depends signiﬁcantly on the prevailing order book imbalance. To analyse this,
we compute the order book imbalance each time an order is submitted as the normalised diﬀerence in
cumulative depth between the ﬁrst ﬁve bid and ask price levels, i.e.
OBI =
P5
i=1 VolB
i −P5
i=1 VolA
i
P5
i=1 VolB
i + P5
i=1 VolA
i
(4)
where VolB
i (VolA
i ) denotes the volume available at the i-th price level on the bid (ask) side of the order
book. Due to the normalisation, OBI is between −1 and 1, where a negative (positive) value implies
that the volume on the ask (bid) side outweighs that on the bid (ask) side of the book. Finally, we
modify the state space of the RL model by dividing the order book imbalance in ﬁve quantile groups
(QOBI
1
−QOBI
5
) and assign each action to one of the groups depending on the imbalance that prevailed
at the time the action occurred. Combined with the action space containing 60 elements, the RL model
includes 300 state-action pairs.22
The resulting permanent price impact estimates and relative price discovery contributions within
each state are reported in Table 8.23 For reasons of clarity, we only include the results on the most
negative imbalance group (QOBI
1
) and the most positive one (QOBI
5
) but the results for the three
remaining groups are consistent with those presented here. We observe a strong positive relationship
between order book imbalance and permanent price impact, with orders submitted or cancelled in the
same direction as the order book imbalance leading to much more extreme price impacts than actions in
the direction opposite to the imbalance. This relationship is highly robust and holds for all 30 actions.
For example, a very large buy market order (Q6) has an impact of only 0.16 bps when the imbalance
is most negative (QOBI
1
) compared to 0.34 bps in the case of a high positive book imbalance (QOBI
5
).
Similarly, the submission of a rather small price-improving sell limit order (Q2) exhibits an impact
of −0.04 bps if the imbalance is most negative, whereas in the case of a highly positive imbalance,
it reduces the mid price by only 0.002 bps. For limit order actions that do not induce an immediate
change in the mid price, the eﬀect of the imbalance in some cases even oﬀsets and overcomes that
of the action, so that the price impact is opposite to the direction of the action. For instance, if the
order book is negatively imbalanced, sell limit order cancellations that do not lead to an immediate
worsening of the best ask quote exhibit negative price impacts across all order size groups, ranging
from −0.04 bps to −0.01 bps.
In general, the relative price discovery contribution of the individual actions within each state is
22Estimating a VAR of equivalent dimensionality would basically be impossible, since the estimation time of the VAR
increases exponentially with the dimensionality of the state space (Philip, 2020).
23To prevent clutter, we do not report conﬁdence intervals for the analyses in this section. However, due to the very
large sample size, conﬁdence intervals are still quite tight.
26
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 27

also positively related to order book imbalance. Trading actions whose direction coincides with the
prevailing imbalance in the order book contribute signiﬁcantly more to price discovery than orders
submitted or cancelled against the order book imbalance. For example, submissions of price-improving
buy limit orders overall account for about 33% of price discovery if the order book imbalance is
highly positive, whereas they are responsible for only 12% of the total price variation in case of a
highly negative imbalance. Within the two most extreme order book imbalance groups (QOBI
1
and
QOBI
5
), actions whose direction coincides with the imbalance jointly account for about 70% of price
discovery. However, within the less extreme groups (QOBI
2
and QOBI
4
), this dominance is signiﬁcantly
less pronounced and imbalance-conforming actions contribute only slightly more than 50%.
The order book imbalance seems to have no impact on the overall importance of the individual order
ﬂow components. The contribution of the components, aggregated over order signs, to the amount of
price variation within each state does not change signiﬁcantly across the diﬀerent imbalance groups.
It is rather the distribution of the price discovery contribution across order signs that changes. For
example, the relative contribution of price-improving limit order submissions, aggregated over buy and
sell, only varies between 45% and 46% across all ﬁve diﬀerent imbalance groups. If the order book
imbalance is highly negative, most of this contribution originates from sell limit orders (34%), while
in the case of a high positive imbalance, submissions of buy limit orders are most relevant (33%).
Market orders and cancellations of limit orders exhibit a similar pattern. This implies that the order
book imbalance does have a signiﬁcant inﬂuence on the permanent price impact of individual actions,
however it does not change the order type that informed agents choose to incorporate their information.
Figure 6 depicts the permanent price impact of market orders, limit order submissions and limit
order cancellations as a function of their signed order size, for the two most extreme order book im-
balance groups (QOBI
1
and QOBI
5
). To increase visibility, we only include price-changing actions for
limit order submissions and cancellations. Comparing the graphs to Figure 4, we see that the perma-
nent price impact of market orders is still nonlinear, even after accounting for order book imbalance.
However, the imbalance seems to change the functional shape of price impact. The impact of orders
that are submitted against the order book imbalance does not increase as strongly in order size as the
impact of orders that are submitted with the order book imbalance. That is, the imbalance of the
order book appears to dampen the eﬀect of order size for those orders that are submitted against the
imbalance. For example, for the most negative order book imbalance group, the impact of buy market
orders increases from about 0.01 bps for very small orders to 0.16 bps for the largest orders, which
corresponds to an increase of 0.15 bps. However, if the imbalance is most positive, the impact of buy
market orders exhibits an increase of 0.28 bps over the same order size range. For limit order submis-
sions and cancellations, including the order book imbalance does not seem to change the functional
shape of permanent price impact signiﬁcantly, but it rather leads to an upward (downward) shift of
the curve for positive (negative) imbalances.
5.2
Bid-Ask Spread
Next, we analyse how permanent price impact changes with the bid-ask spread. In an early study of
cryptocurrency markets, Dimpﬂ(2017) ﬁnds that the largest part of the spread can be attributed to
27
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 28

Table 8 Permanent Price Impact: Market and Limit Orders – Order Book Imbalance
The table reports the permanent price impact estimates (in basis points) for market orders (MO), limit order submissions
(LO Sub) and limit order cancellations (LO Canc) at the best quotes, depending on the order size and the prevailing
order book imbalance. Market orders are diﬀerentiated solely on their sign, limit order submissions and cancellations are
distinguished by both their sign and whether they lead to an immediate change in the mid price (Improving, Worsening)
or leave it unchanged (Matching). The components are additionally divided into quantile groups (Q1 to Q6) depending
on their size. The order book imbalance is calculated according to Equation (4) and then divided into ﬁve quantile
groups (QOBI
1
−QOBI
5
). RCS represents the relative contribution of each action to the amount of price variation within
the speciﬁc state (in %), computed similar to Equation (3).
Most Negative Imbalance (QOBI
1
)
Most Positive Imbalance (QOBI
5
)
Sell
Buy
Sell
Buy
Action
Mid Price
Size
Impact
RCS
Impact
RCS
Impact
RCS
Impact
RCS
MO
Q1
−0.1110
2.35
0.0079
0.29
−0.0506
0.82
0.0634
2.48
Q2
−0.0959
0.93
0.0149
0.18
−0.0617
0.31
0.0658
0.96
Q3
−0.1098
1.47
0.0240
0.48
−0.0691
0.58
0.0789
1.74
Q4
−0.1493
1.35
0.0490
0.41
−0.0897
0.54
0.1223
1.22
Q5
−0.1860
0.86
0.0881
0.39
−0.1274
0.45
0.1575
0.90
Q6
−0.3657
2.85
0.1554
2.14
−0.1733
2.56
0.3398
2.82
LO Sub
Improving
Q1
−0.0491
4.70
0.0157
1.28
−0.0075
0.76
0.0460
4.73
Q2
−0.0439
2.30
−0.0003
0.05
−0.0020
0.22
0.0396
3.89
Q3
−0.0486
3.30
0.0073
0.87
−0.0122
1.00
0.0452
3.66
Q4
−0.0642
5.22
0.0186
2.11
−0.0262
2.24
0.0628
4.67
Q5
−0.0874
7.63
0.0404
4.62
−0.0513
4.41
0.0853
6.87
Q6
−0.0801
10.95
0.0433
2.93
−0.0584
3.28
0.0829
9.30
Matching
Q1
−0.0368
1.25
−0.0007
0.03
0.0013
0.06
0.0338
1.49
Q2
−0.0403
0.94
0.0009
0.07
−0.0017
0.08
0.0369
1.75
Q3
−0.0411
1.16
0.0022
0.18
−0.0037
0.20
0.0376
1.84
Q4
−0.0443
1.61
0.0012
0.06
−0.0023
0.09
0.0394
1.79
Q5
−0.0478
1.56
0.0047
0.22
−0.0064
0.23
0.0422
1.66
Q6
−0.0485
2.46
0.0096
0.49
−0.0126
0.46
0.0427
2.24
LO Canc
Worsening
Q1
0.1190
1.56
−0.1820
3.09
0.1488
2.84
−0.1542
1.79
Q2
0.1031
0.60
−0.1116
2.87
0.1149
1.83
−0.1396
1.10
Q3
0.0543
0.70
−0.0945
2.17
0.0904
1.73
−0.0804
0.81
Q4
0.0582
1.30
−0.0845
3.09
0.0840
2.44
−0.0780
1.33
Q5
0.0592
1.48
−0.0948
3.40
0.1004
3.06
−0.0741
1.43
Q6
0.0788
4.53
−0.0970
1.39
0.1046
1.42
−0.0887
3.64
Matching
Q1
−0.0146
0.09
−0.0319
0.22
0.0293
0.26
0.0145
0.13
Q2
−0.0162
0.06
−0.0296
0.37
0.0272
0.26
0.0158
0.12
Q3
−0.0193
0.19
−0.0220
0.40
0.0205
0.34
0.0233
0.33
Q4
−0.0295
0.49
−0.0181
0.39
0.0174
0.37
0.0289
0.58
Q5
−0.0397
0.70
−0.0149
0.26
0.0141
0.24
0.0359
0.74
Q6
−0.0321
0.83
−0.0123
0.11
0.0108
0.10
0.0297
0.80
28
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 29

Figure 6 Permanent Price Impact Depending on Order Book Imbalance
The ﬁgure displays the permanent price impact estimates (in basis points) of market orders (left-hand graph), price-
improving limit order submissions (middle graph) and price-worsening limit order cancellations (left-hand graph) for the
two most extreme order book imbalance groups (QOBI
1
and QOBI
5
), as a function of signed order size.
adverse selection. Similarly, Scaillet et al. (2020) report that a widening of the bid-ask spread predicts
jumps in the bitcoin price. Therefore, it seems likely that the spread on Coinbase contains a signiﬁcant
amount of information and has a non-trivial inﬂuence on permanent price impact.
Similar to order book imbalance, we compute the bid-ask spread each time an action occurs and
modify the state space of the RL model by partitioning the spread. However, according to Table 2, the
spread is at its minimum value for 37% of the time and its distribution is quite heavily right-skewed.
Therefore, we refrain from using quantile groups for partitioning and instead, following Kwan et al.
(2021), simply divide the spread into two states: binding (0.01 USD) and wide (>0.01 USD). Each
action is then assigned to one of the two states depending on the bid-ask spread that prevailed at the
time the action occurred. Since price-improving limit order submissions cannot occur if the spread is
binding, this partitioning leads to only 168 state-action pairs in the RL model.
Table 9 reports the resulting permanent price impact estimates and relative price discovery con-
tributions within each state. We see that for both buy and sell, market orders generally exhibit a
signiﬁcantly higher price impact, and thus carry more information, if the bid-ask spread is binding.
For instance, a very small buy market order increases the mid price by 0.06 bps in case of a binding
spread, compared to only 0.03 bps if the spread is wide. Moreover, the overall contribution of mar-
ket orders to price discovery is signiﬁcantly higher in the case of a binding spread (38%) than if the
spread is wide (11%). This ﬁnding is in line with the prediction of Bhattacharya and Saar (2020) that
informed agents submit market orders when the spread is narrow.
The only exception to this are very large market orders in the top quantile size group, which
contain more information in case of a wide spread. Since a widening of the spread is typically an
indicator for an imminent increase in volatility (Scaillet et al., 2020), we suppose that these large
orders are submitted by agents that anticipate such an increase in volatility and consume the liquidity
29
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 30

available on the opposite side of the book before it vanishes. To conﬁrm this hypothesis, we re-train
the RL model with an additional state in which the spread is larger than two dollars, corresponding
approximately to its 60%-quantile. If the high price impact of very large orders was due to agents taking
liquidity in the anticipation of elevated volatility, the impact should even be more extreme in the newly-
introduced widest-spread state. Indeed, the results conﬁrm this hypothesis. While the impact of small
to moderately-large market orders (Q1 to Q5) reduces as the spread increases, very large orders in the
top quantile group (Q6) exhibit price impacts that consistently increase across all three spread states.
This ﬁnding is in contrast to Kwan et al. (2021) who document that market orders have a larger price
impact across all order size groups in case of a binding spread. The discrepancy is probably related to
the high volatility of cryptocurrencies compared to equities. Since large price swings occur much more
frequently for bitcoin than for equity, we observe such large volatility-anticipating trades signiﬁcantly
more often, which leads to the larger price impacts in case of a wide spread. However, these large
trades at a wide bid-ask spread still tend to occur comparatively rarely and therefore, despite the
larger individual price impact in case of a wide spread, their relative contribution to price discovery
is still higher when the spread is binding (6.68% for sell trades and 6.24% for buy transactions) than
when it is wide (2.54% and 2.25%).
For limit order submissions, results are more nuanced. In case of a wide spread, price-improving
submissions are highly important and in total account for more than 57% of price discovery, which
conﬁrms the prediction of Bhattacharya and Saar (2020) that informed traders rely on limit orders
when the bid-ask spread is wide. If the spread is binding, price-improving limit orders cannot be
submitted and consequently, submissions at the best quotes become more relevant. However, the large
infomation content of price-improving orders in the case of a binding spread is not entirely transferred
to submissions at the best quotes, but it is split and transferred to both market orders and submissions
at the best quotes, with the contribution of the latter increasing from below 10% in case of a wide
spread to more than 28% for a binding spread.
These results imply that if the bid-ask spread becomes binding, informed agents partially change
the type of order they use to incorporate information. While some agents continue to provide liquidity
(at the best quotes), others switch to taking it which makes market orders the main driver of price
discovery if the bid-ask spread is binding. An obvious explanation for this behaviour are execution
costs.
In case of a binding spread which in relative terms corresponds to only about 0.0025 bps,
market orders (and the associated immediacy) are relatively inexpensive and the value of the agents’
information does not need to be as high in order for the proﬁt to exceed execution costs. Another
possible explanation is competition among informed market participants in the spirit of Baruch et al.
(2017). Informed agents might interpret a binding bid-ask spread as a signal for the presence of other
informed traders and therefore, prefer to act quickly on their information by submitting market orders
(and paying higher execution costs) rather than facing execution risk (and reducing transaction costs)
through limit orders.
Finally, as in previous analyses, price-worsening limit order cancellations have a very high perma-
nent price impact and contribute a signiﬁcant amount to price discovery. However, a close examination
of the data shows that in both cases – binding spread and wide spread – most of this high impact is
30
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 31

of mechanical nature due to large price gaps behind the best quotes that are caused by the extremely
small relative tick size. For example, the price-worsening cancellation of a very small sell limit order
(Q1) causes an immediate increase of 0.2 bps in the mid price, which is already more than 90% of the
entire permanent price impact of 0.22 bps documented in Table 9.
Table 9 Permanent Price Impact: Market and Limit Orders – Bid-Ask Spread
The table reports the permanent price impact estimates (in basis points) for market orders (MO), limit order submissions
(LO Sub) and limit order cancellations (LO Canc) at the best quotes, depending on the order size and the prevailing
bid-ask spread.
Market orders are diﬀerentiated solely on their sign, limit order submissions and cancellations are
distinguished by both their sign and whether they lead to an immediate change in the mid price (Improving, Worsening)
or leave it unchanged (Matching). The components are additionally divided into quantile groups (Q1 to Q6) depending
on their size. The bid-ask spread is divided in two states: binding (0.01 USD) and wide (>0.01 USD). RCS represents
the relative contribution of each action to the amount of price variation within the speciﬁc state (in %), computed similar
to Equation (3).
Binding Spread
Wide Spread
Sell
Buy
Sell
Buy
Action
Mid Price
Size
Impact
RCS
Impact
RCS
Impact
RCS
Impact
RCS
MO
Q1
−0.1225
4.94
0.0552
4.31
−0.0614
0.84
0.0271
0.78
Q2
−0.1080
1.55
0.0547
1.44
−0.0741
0.40
0.0362
0.37
Q3
−0.1200
2.57
0.0652
2.69
−0.0869
0.68
0.0482
0.78
Q4
−0.1427
2.21
0.1021
1.93
−0.1184
0.63
0.0811
0.56
Q5
−0.1701
1.52
0.1310
1.61
−0.1606
0.53
0.1249
0.48
Q6
−0.2302
6.68
0.2212
6.24
−0.2791
2.54
0.2596
2.25
LO Sub
Improving
Q1
−0.0300
3.56
0.0336
3.52
Q2
−0.0241
2.22
0.0214
3.46
Q3
−0.0329
2.80
0.0290
3.45
Q4
−0.0475
4.59
0.0427
4.69
Q5
−0.0739
7.65
0.0663
7.89
Q6
−0.0721
7.05
0.0674
6.29
Matching
Q1
−0.0233
1.47
0.0124
0.73
−0.0176
0.64
0.0180
0.68
Q2
−0.0299
1.72
0.0185
1.50
−0.0212
0.68
0.0207
1.21
Q3
−0.0318
2.54
0.0210
2.11
−0.0225
0.73
0.0213
1.30
Q4
−0.0326
3.35
0.0208
2.38
−0.0222
0.57
0.0209
0.77
Q5
−0.0361
3.31
0.0245
2.47
−0.0265
0.65
0.0234
0.75
Q6
−0.0404
3.93
0.0260
2.67
−0.0274
0.83
0.0230
0.89
LO Canc
Worsening
Q1
0.2236
5.02
−0.2587
5.54
0.1073
1.47
−0.1388
1.49
Q2
0.1916
1.67
−0.2087
2.66
0.0928
0.85
−0.1021
1.42
Q3
0.1509
1.16
−0.1805
1.45
0.0650
1.02
−0.0769
1.14
Q4
0.1423
1.58
−0.1563
1.66
0.0657
1.76
−0.0741
1.91
Q5
0.2089
2.05
−0.2065
1.78
0.0720
2.17
−0.0790
2.29
Q6
0.2074
2.58
−0.2280
2.40
0.0880
3.01
−0.0910
2.51
Matching
Q1
0.0057
0.14
−0.0126
0.33
0.0079
0.03
−0.0080
0.03
Q2
0.0000
0.00
−0.0099
0.27
0.0061
0.02
−0.0064
0.04
Q3
−0.0081
0.33
0.0018
0.09
0.0032
0.02
0.0003
0.00
Q4
−0.0106
0.63
0.0028
0.18
−0.0080
0.09
0.0095
0.13
Q5
−0.0150
0.79
0.0054
0.31
−0.0204
0.24
0.0178
0.25
Q6
−0.0195
1.07
0.0085
0.44
−0.0178
0.19
0.0169
0.20
6
Inter-Exchange Information Flows
Due to the high fragmentation of cryptocurrency markets, it is likely that trading on Coinbase is
inﬂuenced by information from other exchanges. In fact, empirical studies such as Alexander and
31
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 32

Heck (2020) report that spot exchanges, including Coinbase, do not contribute much to price discovery
and it is the highly-leveraged derivatives products oﬀered by many unregulated crypto exchanges that
dominate the price discovery process. Therefore, in this section, we study how exactly information
from other exchanges inﬂuences the price discovery process on Coinbase. As before, we consider only
actions aﬀecting the best quotes, which according to Table 6, should not change results signiﬁcantly.
Therefore, in the following, the term event refers to all messages on Coinbase aﬀecting the best quotes.
To analyse how the permanent price impact on Coinbase is inﬂuenced by other exchanges, we
obtain tick data on major derivatives instruments and spot pairs from Tardis.dev. More speciﬁcally,
we retrieve tick data on the top-of-book quotes of the three most actively traded bitcoin derivatives
(USDT-perpetual contracts traded on Binance and Bybit and the USD-perpetual oﬀered by FTX)
and the spot pair with the highest trading volume (BTCUSDT on Binance). As a sort of control
variable, we also obtain quotes data for bitcoin-dollar trading on Bitstamp, a well-established but
rather small spot exchange that is likely to have little to no inﬂuence on Coinbase. It is important to
note that Tardis operates a synchronized clock to timestamp messages upon arrival on their servers.
This mitigates the issue of small time diﬀerences in the timestamps provided by the exchanges and
allows us to replay the market from the perspective of a trader.
For each of these ﬁve products (called transmitting products in the following), we now train an
RL model where the state space captures the past return on both Coinbase and the product. More
speciﬁcally, we apply the following procedure for each product. First, for each event t on Coinbase,
we determine the as-of mid price of the transmitting product, i.e. the most recent mid price at the
time of the Coinbase event. Then, we use these as-of mid prices to calculate the log return of the
product over the previous 50 Coinbase events (i.e. t −50, . . . , t −1), which on average corresponds to
a time period of about one second.24 Next, we quantize these mid returns and divide them into ﬁve
quantile groups (QP
1 −QP
5 ). In the same way, we calculate the 50-message log returns of the mid price
on Coinbase and quantize them, yielding the groups QCB
1
−QCB
5
. This way, we obtain for each event
t on Coinbase, the quantile group of the preceding return on the transmitting product as well as the
quantile group of the preceding return on Coinbase. The state space of the RL model is now deﬁned
as the set of all 25 possible combinations of the returns on Coinbase and the transmitting product, i.e.
S = {(QCB
i
, QP
j ) | i, j = 1, . . . , 5}. The action space is chosen similar to Table 7 but to not overload
the model, we do not diﬀerentiate orders based on their size. Therefore, the action space includes
only ten actions – buy and sell market order, price-improving and price-matching submissions of buy
and sell limit orders, price-worsening and price-matching cancellations of buy and sell limit orders.
Consequently, this speciﬁcation of the RL model includes 250 state-action pairs.
Table 10 provides the permanent price impact estimates from these RL models.25 For reasons of
brevity, we only report the results on sell actions for two of the ﬁve transmitting products (Binance
24Due to their fully electronic nature, we expect information to be transmitted rather quickly between cryptocurrency
exchanges. Even retail traders can easily apply optimised out-of-the-box trading bots that allow them to monitor several
exchanges and execute trading strategies based on inter-exchange price diﬀerences (see for example the open-source
Hummingbot). As a robustness check, we have repeated the procedure with returns calculated over both shorter and
longer intervals. However, the results are qualitatively similar to those for 50-event returns.
25As before, we do not report conﬁdence intervals to prevent clutter. However, due to the large sample size, the intervals
are still quite tight.
32
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 33

USDT-perpetual and BTCUSD on Bitstamp). However, the results for buy actions and the remaining
three products are very similar to those presented here. Moreover, the relative price discovery contri-
butions, calculated using Equation (3), do not yield any further insights and are consistent with the
permanent price impacts (i.e. the higher the absolute price impact of an action, the higher its price
discovery contribution). Therefore, we refrain from reporting the contributions here.
We see that the past return on the Binance perpetual signiﬁcantly inﬂuences permanent price
impacts on Coinbase.
If the price on the Binance perpetual has declined over the last 50 events,
Coinbase follows and the permanent price impacts of all actions are shifted downwards. On the other
hand, if the Binance perpetual has shown a price increase, the impact of all actions on Coinbase
increases as well. For instance, a sell market order that is submitted on Coinbase after a negative
return on the Binance perpetual (QP
2 ) reduces the mid price by 0.25 bps to 0.37 bps. If the same
order is submitted after a moderate price increase on Binance (QP
4 ), the mid price on Coinbase is only
reduced at most 0.05 bps. Interestingly, in the case of a highly positive price movement on the Binance
perpetual (QP
5 ) the permanent price impact of all actions on Coinbase is positive. For example, the
submission of a sell market order on Coinbase after a highly positive return on Binance leads to an
increase in the Coinbase mid price of 0.34 bps to 0.75 bps. This implies that the inﬂuence of the
Binance USDT-perpetual is strong enough to oﬀset and overcome the negative immediate impact of
sell actions on Coinbase.
The inﬂuence of the Binance perpetual contract on Coinbase is so strong that its returns even
aﬀect the permanent price impact of all actions more than the returns on Coinbase itself. If we hold
the quantile return group of Coinbase constant, the inﬂuence of past Binance returns, measured as the
diﬀerence in permanent price impact between the most negative and the most positive return group
(QP
1 and QP
5 ), is between 1.38 bps and 1.66 bps. On the other hand, if we hold the quantile return
group of Binance constant, the inﬂuence of past Coinbase returns ranges only from 0.12 bps to 0.41
bps. This massive diﬀerence highlights the dominance of the Binance USDT-perpetual over Coinbase
in terms of price discovery and implies that even at such short time frames, the price discovery process
on Coinbase is largely dictated by the Binance perpetual.
For Bitstamp, Table 10 shows a diﬀerent picture. The permanent price impacts on Coinbase are
aﬀected very little by the preceding return on Bitstamp. In fact, they are even slightly reduced if
there has been a positive return on Bitstamp.26 For instance, a sell market order on Coinbase reduces
the mid price by at most 0.33 bps if the preceding return on Bitstamp has been most negative (QP
1 )
while the same order causes the mid price to decrease by at most 0.42 bps in case of a a positive
price movement on Bitstamp. In contrast to Binance, the inﬂuence of Bitstamp on Coinbase is not
strong enough to oﬀset and overcome the negative immediate impact of sell actions, so that in case of
a highly positive return on Bitstamp (QP
5 ), all sell actions generally still have a negative permanent
price impact.27
26Such a reduction could for example arise from a counter-cyclical behaviour of Bitstamp and Coinbase.
That is,
if Bitstamp follows Coinbase with a time lag, it might be that just after a positive return has been transmitted from
Coinbase to Bitstamp, the price on the latter starts to increase, while the price on Coinbase has already lost its momentum
and starts falling again.
27In some cases, submissions of sell orders exhibit a positive permanent impact for a highly positive Bitstamp return.
However, this behaviour occurs only after a positive return on Coinbase (QCB
4
and QCB
4
) and should therefore not be
33
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 34

Table 10 Permanent Price Impact: Market and Limit Orders – Inter-Exchange Information Flows
The table reports the permanent price impact estimates (in basis points) for market orders (MO), limit order submissions (LO Sub) and limit order cancellations
(LO Canc) at the best quotes, depending on the preceding return on both Coinbase and the Binance USDT-perpetual (Bitstamp BTCUSD). Market orders are
diﬀerentiated solely on their sign, limit order submissions and cancellations are distinguished by both their sign and whether they lead to an immediate change in the
mid price (Improving, Worsening) or leave it unchanged (Matching). The preceding returns are calculated as the log change in the mid price over the last 50 events
on Coinbase. Then, they are divided into ﬁve quantile groups, giving the Coinbaser return groups (QCB
1
toQCB
5
) and the return groups (QP
1 −QP
5 ) of the Binance
USDT-perpetual (Bitstamp BTCUSD). For reasons of brevity, we only report results for sell actions. QP
5 −QP
1 reports the diﬀerence in permanent price impact
between the most negative and the most positive return group of the Binance USDT-perpetual (Bitstamp BTCUSD). QCB
5
−QCB
1
reports the diﬀerence in permanent
price impact between the most negative and the most positive return group of Coinbase.
Binance USDT-Perpetual
Bitstamp BTCUSD
Action
Mid Price
Coinbase
QP
1
QP
2
QP
3
QP
4
QP
5
QP
5 −QP
1
QP
1
QP
2
QP
3
QP
4
QP
5
QP
5 −QP
1
MO
QCB
1
−1.1150
−0.3718
−0.1652
−0.0459
0.3408
1.4558
−0.3280
−0.3372
−0.3573
−0.4004
−0.4190
−0.0909
QCB
2
−0.9996
−0.3143
−0.1179
0.0331
0.4887
1.4883
−0.1856
−0.1833
−0.2036
−0.2061
−0.2809
−0.0953
QCB
3
−0.8914
−0.2634
−0.0567
0.0981
0.5924
1.4838
−0.0839
−0.0951
−0.0861
−0.0894
−0.1698
−0.0859
QCB
4
−0.8755
−0.2382
−0.0297
0.1267
0.6578
1.5333
−0.0250
−0.0485
−0.0298
−0.0387
−0.1160
−0.0910
QCB
5
−0.9168
−0.2506
−0.0155
0.1481
0.7471
1.6638
0.0205
0.0070
0.0613
0.0477
−0.0259
−0.0464
QCB
5
−QCB
1
0.1982
0.1212
0.1497
0.1940
0.4063
0.3485
0.3442
0.4185
0.4481
0.3931
LO Sub
Improving
QCB
1
−0.9697
−0.2948
−0.1064
0.0195
0.4876
1.4573
−0.2018
−0.1961
−0.2410
−0.2701
−0.2787
−0.0769
QCB
2
−0.8488
−0.2331
−0.0545
0.0929
0.5686
1.4174
−0.0681
−0.0693
−0.1044
−0.1123
−0.1658
−0.0978
QCB
3
−0.7676
−0.1908
−0.0110
0.1412
0.6377
1.4053
0.0068
−0.0095
−0.0236
−0.0315
−0.0937
−0.1005
QCB
4
−0.7296
−0.1693
0.0118
0.1701
0.7072
1.4369
0.0559
0.0273
0.0287
0.0164
−0.0388
−0.0947
QCB
5
−0.7437
−0.1522
0.0396
0.2127
0.8061
1.5498
0.1134
0.0940
0.1190
0.1134
0.0565
−0.0569
QCB
5
−QCB
1
0.2260
0.1425
0.1460
0.1932
0.3186
0.3152
0.2901
0.3600
0.3835
0.3352
Matching
QCB
1
−0.9232
−0.2784
−0.0909
0.0329
0.5192
1.4424
−0.1643
−0.1629
−0.2065
−0.2404
−0.2428
−0.0784
QCB
2
−0.8190
−0.2235
−0.0448
0.1011
0.5786
1.3976
−0.0478
−0.0542
−0.0881
−0.0974
−0.1456
−0.0978
QCB
3
−0.7343
−0.1817
−0.0028
0.1475
0.6484
1.3826
0.0240
0.0024
−0.0108
−0.0218
−0.0738
−0.0978
QCB
4
−0.6889
−0.1504
0.0316
0.1869
0.7303
1.4192
0.0827
0.0495
0.0526
0.0357
−0.0123
−0.0950
QCB
5
−0.6703
−0.1174
0.0738
0.2480
0.8558
1.5261
0.1668
0.1424
0.1654
0.1596
0.1042
−0.0626
QCB
5
−QCB
1
0.2529
0.1609
0.1646
0.2151
0.3366
0.3311
0.3052
0.3719
0.4000
0.3470
LO Canc
Worsening
QCB
1
−0.7559
−0.1485
0.0341
0.1719
0.7567
1.5125
−0.0048
−0.0149
−0.0594
−0.0848
−0.0760
−0.0712
QCB
2
−0.6807
−0.1270
0.0551
0.1989
0.7638
1.4445
0.0811
0.0457
0.0279
0.0070
−0.0199
−0.1011
QCB
3
−0.6256
−0.1054
0.0713
0.2233
0.8240
1.4495
0.1403
0.0834
0.0757
0.0573
0.0387
−0.1016
QCB
4
−0.5689
−0.0591
0.1224
0.2801
0.9192
1.4881
0.2113
0.1587
0.1711
0.1435
0.1210
−0.0903
QCB
5
−0.4916
−0.0106
0.1753
0.3580
1.0384
1.5300
0.3252
0.2890
0.3133
0.3024
0.2609
−0.0643
QCB
5
−QCB
1
0.2642
0.1379
0.1412
0.1861
0.2817
0.3300
0.3039
0.3727
0.3872
0.3369
Matching
QCB
1
−0.8986
−0.2607
−0.0776
0.0490
0.5660
1.4646
−0.1439
−0.1449
−0.1886
−0.2199
−0.2211
−0.0772
QCB
2
−0.7941
−0.2114
−0.0330
0.1151
0.6105
1.4046
−0.0308
−0.0413
−0.0739
−0.0812
−0.1286
−0.0978
QCB
3
−0.7140
−0.1731
0.0059
0.1588
0.6694
1.3834
0.0361
0.0114
−0.0010
−0.0100
−0.0594
−0.0955
QCB
4
−0.6656
−0.1351
0.0455
0.2052
0.7601
1.4257
0.1021
0.0652
0.0688
0.0547
0.0070
−0.0951
QCB
5
−0.6380
−0.0958
0.0932
0.2724
0.8923
1.5303
0.1938
0.1673
0.1902
0.1878
0.1308
−0.0630
QCB
5
−QCB
1
0.2606
0.1648
0.1708
0.2235
0.3263
0.3377
0.3122
0.3788
0.4077
0.3519
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 35

Overall, the inﬂuence of Bitstamp on Coinbase is at best rather weak. If we hold the quantile return
group of Coinbase ﬁxed, the inﬂuence of past Bitstamp returns, again measured as the diﬀerence in
permanent price impact between the most negative and the most positive return group, is very small
and even negative, ranging from −0.1 bps to −0.05 bps. In contrast, the inﬂuence of past Coinbase
returns is between 0.31 bps and 0.41 bps. This discrepancy implies that Bitstamp is rather irrelevant
with regards to price discovery on Coinbase.
Figure 7 depicts the permanent price impacts of market orders on Coinbase, depending on the
preceding return on both Coinbase and the ﬁve transmitting products.
Note that the respective
ﬁgures look very similar for submissions and cancellations of limit orders and they are therefore not
shown here. The price impact estimates are depicted as heatmaps, i.e. the darker the colour of a
cell, the lower the permanent price impact for the respective combination of quantile return groups.
For the three perpetual contracts and the BTCUSDT spot pair on Binance, cells in the same column
are of very similar colour and most variation is between, rather than within, columns. This implies
that the estimates of permanent price impact do not vary much across the diﬀerent return groups of
Coinbase (QCB
1
−QCB
5
), but they change signiﬁcantly depending on the quantile return group of the
three perpetuals and the Binance spot pair (QP
1 −QP
5 ). Therefore, we conclude that even at short
time frames of about one second, permanent price impacts, and thus the price discovery process, on
Coinbase strongly depend on the preceding price movements on other, leading products and exchanges.
In contrast, the heatmap for Bitstamp shows a large degree of variation within, rather than across,
columns, which indicates that past returns on Coinbase itself are more relevant for the price discovery
process on Coinbase than returns on Bitstamp. That is, Coinbase does not follow the price movements
on Bitstamp, but it is rather the other way around.
7
Conclusion
Similar to traditional stock exchanges, cryptocurrency exchanges operate a central limit order book
and thus, the traditional assumption that only trades carry information is not reasonable any more.
Therefore, using an extensive four-month tick-by-tick data set on transactions and order book messages
on Coinbase, the most established cryptocurrency spot exchange, we are the ﬁrst to study the price
discovery process of bitcoin-dollar trading at its most granular level. To do so, we apply a recently
proposed modiﬁed reinforcement learning framework that is able to capture nonlinear relationships
and can be trained within a reasonable amount of time, even if tens of millions of observations are
included and the variables space is high-dimensional. We estimate the permanent price impacts and
the relative price discovery contributions of diﬀerent order ﬂow components (market orders, limit
order submissions, limit order cancellations) and analyse how the state of the order book aﬀects the
contribution of individual components. Finally, we examine how other cryptocurrency (derivatives)
exchanges inﬂuence the price discovery process on Coinbase.
We show that market orders individually exhibit a much larger permanent price impact than
limit order submissions, even in case the latter undercut the best quote. However, if the number of
attributed to the positive Bitstamp return.
35
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 36

Figure 7 Permanent Price Impact Depending on Inter-Exchange Flows
The ﬁgure displays the permanent price impact estimates for market orders on Coinbase, depending on the preceding
returns on both Coinbase and one of the ﬁve transmitting products (Binance USDT-perpetual, FTX USD-perpetual,
Bybit USD-perpetual, BTCUSDT on Binance, BTCUSD on Bitstamp). The upper row of graphs represents sell-initiated
market orders, the lower row is for buy-initiated market orders.
occurrences is taken into account, limit order submissions are signiﬁcantly more important than market
orders and contribute about 50% to the price discovery process. The bulk of this large contribution
originates from limit order submissions that undercut the best quotes. These ﬁndings are consistent
with recent studies on FX and equity markets (Brogaard et al., 2019; Chaboud et al., 2021). In contrast
to traditional asset classes, we observe a certain asymmetry in the permanent price impact of market
orders, with sell-initiated market orders carrying signiﬁcantly more information than buy orders. We
suppose that this discrepancy is caused by unidirectional retail order ﬂows on Coinbase, where retail
investors mainly position themselves on the buy side of transactions.
Moreover, we show that the order book has a signiﬁcant impact on the price discovery process.
Orders that are submitted with the order book imbalance contribute considerably more to price dis-
covery than orders whose direction is opposite to the prevailing imbalance. The bid-ask spread has
a non-trivial eﬀect on the order choice of informed agents. In case of a non-binding spread, price
discovery mainly occurs through undercutting limit orders, whereas if the spread is binding, market
orders are most important. Finally, we show that the three most actively traded bitcoin derivatives
products and the largest spot pair heavily inﬂuence the price discovery process on Coinbase. Trading
actions whose direction coincides with the preceding price evolution on the four leading products are
the main driver of price discovery. Compared to the returns on the three derivatives products and the
largest spot pair, the preceding price evolution on Coinbase itself is rather irrelevant.
With several hundred spot exchanges and a few dozen derivatives trading venues, the cryptocur-
rency is highly fragmented.
However, fragmented markets are still interconnected.
As shown by
Van Kervel (2015), transactions on one exchange trigger reactive submissions and cancellations of
limit orders on other exchanges.
Such reactions are eﬃcient and in a price impact analysis, they
36
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 37

should be attributed to the initial transaction. Therefore, in terms of futures research, it would be
of great interest (i) to analyse the price discovery process on exchanges other than Coinbase – most
importantly the derivatives venues – and (ii) to expand the RL framework used in this study to include
several exchanges so that it yields a market-wide permanent price impact estimate, where, for exam-
ple, cancellations on one exchange that are caused by a transaction on another exchange are correctly
assigned to the transaction.
References
Alexander, C. and D. F. Heck (2020). Price discovery in bitcoin: The impact of unregulated markets.
Journal of Financial Stability 50.
Alexander, C., D. F. Heck, and A. Kaeck (2021). The role of binance in bitcoin volatility transmission.
Working Paper.
Andersen, T. G. and T. Bollerslev (1998). Deutsche mark-dollar volatility: Intraday activity patterns,
macroeconomic announcements, and longer run dependencies. Journal of Finance 53(1), 219–265.
Baruch, S., M. Panayides, and K. Venkataraman (2017). Informed trading and price discovery before
corporate events. Journal of Financial Economics 125(3), 561–588.
Bhattacharya, A. and G. Saar (2020). Limit order markets under asymmetric information. working
paper.
Biais, B., C. Bisi`ere, M. Bouvard, C. Casamatta, and A. J. Menkveld (2022). Equilibrium bitcoin
pricing. Journal of Finance forthcoming.
Biais, B., P. Hillion, and C. Spatt (1995). An empirical analysis of the limit order book and the order
ﬂow in the paris bourse. Journal of Finance 50(5), 1655–1689.
Bloomﬁeld, R., M. O’Hara, and G. Saar (2005). The “make or take” decision in an electronic market:
Evidence on the evolution of liquidity. Journal of Financial Economics 75(1), 165–199.
Bollerslev, T. and I. Domowitz (1993). Trading patterns and prices in the interbank foreign exchange
market. Journal of Finance 48(4), 1421–1443.
Brogaard, J., T. Hendershott, and R. Riordan (2014). High-frequency trading and price discovery.
Review of Financial Studies 27(8), 2267–2306.
Brogaard, J., T. Hendershott, and R. Riordan (2019). Price discovery without trading: Evidence from
limit orders. Journal of Finance 74(4), 1621–1658.
Cao, C., O. Hansch, and X. Wang (2009).
The information content of an open limit-order book.
Journal of Futures Markets 29(1), 16–41.
Chaboud, A., E. Hjalmarsson, and F. Zikes (2021). The evolution of price discovery in an electronic
market. Journal of Banking and Finance 130.
Collin-Dufresne, P. and V. Fos (2015). Do prices reveal the presence of informed trading? Journal of
Finance 70(4), 1555–1582.
Cont, R., A. Kukanov, and S. Stoikov (2014). The price impact of order book events. Journal of
Financial Econometrics 12(1), 47–88.
37
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 38

Dimpﬂ, T. (2017). Market microstructure. Working Paper.
Dimpﬂ, T. and K. Maeckle (2021). Dry as the desert? on the liquidity of a bitcoin exchange. Working
Paper.
Donier, J. and J. Bonart (2015). A million metaorder analysis of market impact on the bitcoin. Market
Microstructure and Liquidity 1(2).
Dyhrberg, A. H., S. Foley, and J. Svec (forthcoming). When bigger is better: The impact of a tiny
tick size on undercutting behavior. Journal of Financial and Quantitative Analysis.
Fleming, M. J., B. Mizrach, and G. Nguyen (2018). The microstructure of a U.S. Treasury ECN: The
BrokerTec platform. Journal of Financial Markets 40, 2–22.
Ghysels, E. and G. Nguyen (2019). Price discovery of a speculative asset: Evidence from a bitcoin
exchange. Journal of Risk and Financial Management 12(4), 164–189.
Goettler, R. L., C. A. Parlour, and U. Rajan (2009). Informed traders and limit order markets. Journal
of Financial Economics 93(1), 67–87.
Gould, M. D. and J. Bonart (2015). Queue imbalance as a one-tick-ahead price predictor in a limit
order book. working paper.
Han, B. and A. Kumar (2013). Speculative retail trading and asset prices. Journal of Financial and
Quantitative Analysis 48(2), 377–404.
Hasbrouck, J. (1991). The summary informativeness of stock trades: An econometric analysis. Review
of Financial Studies 4(3), 571–595.
Hautsch, N. and R. Huang (2012). The market impact of a limit order. Journal of Economic Dynamics
and Control 36(4), 501–522.
Jahanshahloo, H., S. Corbet, and L. Oxley (2022). Seeking sigma: Time-of-the-day eﬀects on the
bitcoin network. Working Paper.
Kwan, A., R. Philip, and A. Shkilko (2021). The conduits of price discovery: A machine learning
approach. Working Paper.
Kyle, A. S. (1985). Continuous auctions and insider trading. Econometrica 53(6), 1315–1335.
Makarov, I. and A. Schoar (2020).
Trading and arbitrage in cryptocurrency markets.
Journal of
Financial Economics 135(2), 293–319.
O’Hara, M. (2015). High frequency market microstructure. Journal of Financial Economics 116(2),
257–270.
Philip, R. (2020). Estimating permanent price impact via machine learning. Journal of Economet-
rics 215, 414–449.
Ricc´o, R., B. Rindi, and D. J. Seppi (2022). Information, liquidity, and dynamic limit order markets.
Working Paper.
Rosu, I. (2020). Liquidity and information in limit order markets. Journal of Financial and Quantitative
Analysis 55(6), 1792–1839.
38
Electronic copy available at: https://ssrn.com/abstract=4150979


## Page 39

Scaillet, O., Z. Treccani, and C. Trevisan (2020). High-frequency jump analysis of the bitcoin market.
Journal of Financial Econometrics 18(2), 209–232.
Shkilko, A. and K. Sokolov (2020). Every cloud has a silver lining: Fast trading,microwave connectivity,
and trading costs. Journal of Finance 75(6), 2899–2927.
Upson, J., T. H. McInish, and H. Johnson (2018). Orders versus trades on the consolidated tape.
Working Paper.
Upson, J. and R. A. Van Ness (2017). Multiple markets, algorithmic trading, and market liquidity.
Journal of Financial Markets 32, 49–68.
Van Kervel, V. (2015). Competition for order ﬂow with fast and slow traders. Review of Financial
Studies 28(7), 2094–2127.
Watkins, C. J. C. H. and P. Dayan (1992). Q-learning. Machine Language 8(3-4), 279–292.
White, M. and A. White (2010).
Interval estimation for reinforcement-learning algorithms in
continuous-state domains. Advances in Neural Information Processing Systems 23, 2433–2441.
39
Electronic copy available at: https://ssrn.com/abstract=4150979


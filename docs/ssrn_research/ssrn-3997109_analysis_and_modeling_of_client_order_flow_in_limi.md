# Analysis and modeling of client order flow in limit order markets

- **Source File**: `ssrn-3997109.pdf`
- **Total Pages**: 32
- **SSRN ID**: `ssrn-3997109`

---

## Page 1

Analysis and modeling of client order ﬂow in limit order markets
Rama Cont1, Mihai Cucuringu1,2,3, Vacslav Glukhov4, and Felix Prenzel∗1,4
1Mathematical Institute, University of Oxford
2Department of Statistics, University of Oxford
3The Alan Turing Institute
4JP Morgan†
December 30, 2021
Abstract
Orders in major electronic stock markets are executed through centralised limit order books (LOBs).
The availability of historical data have led to extensive research modelling LOBs. Better understanding the
dynamics of LOBs and building simulators as a framework for controlled experiments, when testing trading
algorithms or execution strategies are among the aims in this area. Most work in the literature models the
aggregate view of the limit order book, which focuses on the volume of orders at a given price level using
a point process. In addition to this aggregate view, brokers and exchanges also have information on the
identity of the agents submitting the order to them. This leads to a more complicated representation of
limit order book dynamics, which we attempt to model using a heterogeneous model of order ﬂow.
We present a granular representation of the limit order book, that allows to account for the origins of
diﬀerent orders. Using client order ﬂow from a large broker, we analyze the properties of variables in this
representation. The heterogeneity of the order ﬂow is modeled by segmenting clients into diﬀerent clusters,
for which we identify representative prototypes. This segmentation appears to be stable both over time, as
well as over diﬀerent stocks. Our ﬁndings can be leveraged to build more realistic order ﬂow models that
account for the diversity of market participants.
1
Introduction
Limit order books (LOBs) are the data structures that record the outstanding limit orders on an exchange,
where diﬀerent agents interact buying and selling a certain asset. This continuous buy and sell procedure leads
to the asset’s price formation. The diﬀerent agents participating in the market follow diﬀerent investment
objectives and strategies when making trading decisions, which eventually end up as orders of diﬀerent types
sent to a LOB. Orders are sent to the exchange either through execution services or directly by the agents
themselves. In particular, high-frequency traders (HFTs) and market makers (MMs) tend to have proprietary
access to exchanges. Intuitively, this brings up the question about the heterogeneity of the order ﬂow in LOBs.
Yet, most LOB models based on stochastic processes like [23, 10, 2] assume homogeneous order ﬂow and do
not account for the potential diﬀerences between diﬀerent agents with regard to their behaviour in LOBs.
The reason for this widely employed homogeneous modelling lies in the limited access to private data. In most
settings, public data is being used, which, in the best case scenarios, shows orders on a tick level (i.e. order by
order), such as the LOBSTER database1. This does not allow to account for the origin of a particular order,
e.g. which agent (or what type of agent) submitted the order, and whether a limit order is part of a larger
parent order which is being executed throughout a speciﬁed time horizon.
Figure 1 presents a view of this heterogeneous market ecology, which cannot be observed in public data. In ﬁrst
instance, one might separate traders into two groups – those trading with a proprietary access to exchanges, and
those trading through execution services/brokers. The ﬁrst group primarily contains high frequency traders and
∗Corresponding author: prenzel@maths.ox.ac.uk
†Opinions expressed in this paper are those of the authors, and do not necessarily reﬂect the view of JP Morgan.
1https://lobsterdata.com/
1
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 2

market makers, generally trading with proprietary access to the exchange. The remainder are traders which
generally trade through execution services and are not in full control of the actual placement of limit orders.
In contrast, they send parent orders (also called meta orders) to a broker. The broker then uses diﬀerent
algorithms to slice the parent order into diﬀerent child orders, which are then sent as limit or market orders to
the exchange. Studies using public LOB data only see what is being sent to exchanges at the end of the order
process (right hand side of Figure 1).
A
B
C
D
...
Traders/Clients
HT
LT
...
Desks
VWAP
POV
ALGO X
...
Algos
SOR
Routing
HFT
MM
HFT/MM
CBOE
LSE
XETRA
...
Venues
Figure 1: Flow chart depicting the process of an order from a client sent to a broker. Clients submit “parent
orders” to execution services and diﬀerent trading desks. For example, these could be high tough (HT) and
low touch (LT) desks. At steps “Desks” and “Algos”, the parent orders are sliced into child orders, and sent
to diﬀerent venues for cost-eﬃcient execution. Usually, a routing system (SOR) determines to which venue a
child order is sent.
This work contributes along two dimensions to the literature. Firstly, it introduces a new notation for LOBs
which accounts for diﬀerent agents submitting orders to LOBs. This notation allows for more detailed views
on LOBs; in addition, common views such as the public view (queue size) can be derived from it. Second, one
particular view on the LOB, the broker view, is analyzed in detail. We use trade execution data to segment
traders into representative groups with similar attributes. These are then analyzed for stability in both the
cross-sectional (i.e, cross-asset) and temporal dimensions. Following, the heterogeneity of the aggregated order
ﬂow which is induced by diﬀerent trader types is investigated.
We ﬁnd traders can be segmented into four diﬀerent components, namely the quant, VWAP, signal and residual
order ﬂows. The diﬀerent groups are stable both over time as well as over diﬀerent instruments. This also
holds for the traders themselves. Heterogeneity in both the agents’ structure and the order ﬂow they generate
in LOBs allow the development of heterogeneous order ﬂow models. In particular, we suggest a model for each
agent types, based on the insights derived from the segmentation analysis which capture the most important
characteristics of each component despite their simplicity.
This section concludes with a review of related work in the area. In Section 2, an alternative, more detailed
notation for LOBs accounting for diﬀerent origins of orders is introduced. The notation allows for diﬀerent
views on the LOB. Section 3 presents the data and pre-processing. Afterwards, the set of traders is segmented
the representative agent types explained in detail and the segmentations’ stability is shown. Section 4 presents
results on the properties of the accumulated order ﬂows for each agent type. A simple model for parent order
ﬂow capturing the main heterogeneity between the diﬀerent agent types is presented in Section 5. Section 6
summarizes the results and present future research directions.
1.1
Related work
The existing literature covering LOBs is vast. This is particularly true for publicly available data. Compre-
hensive introductions to LOBs are given in [1, 11]. and among others [9, 5] analyse properties of the LOBs in
general data.
Modelling, simulation and prediction have been the subject of a broad variety of studies in the literature. Most
commonly known in literature, [23, 10] model the LOB via homogeneous Poisson processes. Hawkes processes –
another type of point process – have been studied, for example, in [2], analyzing long-term properties of LOBs
2
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 3

driven by such self-exciting point processes. [22, 26] use deep learning to predict the mid price moves over some
time interval. Several studies exist that aim to model LOBs with agent based models, e.g. [8, 25], but usually
these models struggle with calibration since it is not clear how to calibrate the single agents.
The literature on market ecology is more scarce. The reason is partially data privacy and general access to
non-public data. Few studies are available where researchers had access to non-public order book data, which
were mainly used to analyse the eﬀect of the newly arisen HFTs and MMs.
Two of the studies with non-public data have been presented by Brogaard et al. in [6, 7]. They study LOB data
in which orders from HFTs and MMs are ﬂagged, in order to analyse the impact of HFT and MM accounts on
market quality and price discovery. The studies ﬁnd evidence that HFTs increase market quality by potentially
dampening intraday volatility among other properties. Furthermore, they argue that the trade directions of
HFTs are based on public information such as “macro news announcements, market-wide price movements,
and limit order book imbalances” [7]. [12] analyse LOB data with information about orders from HFTs and
MMs, speciﬁcally outlining the diﬀerences between these two types of market participants in the way they tend
to trade. They ﬁnd MMs to take the majority of limit order traﬃc and to hold lower inventories compared
to HFTs. [13] attempt to extract HFT trades by identifying the so-called “strategy runs”, i.e., periods with
similar inter-arrival times and order sizes, which is unique for HFTs, as the authors argue. Their suggested
measure of low latency indicates that with increasing low latency trading, spreads decrease and the depth at
the ﬁrst level increases.
The richest analysis in the literature is [15]. The authors analyse audit trail data on transaction level from the
S&P 500 eMini Future during 4 days, including the ﬂash crash from May 2010. In particular, they separate the
market into high frequency traders, market makers, fundamental buyers, fundamental sellers and opportunistic
traders, as previously derived in [17]. The classiﬁcation is done both based on transaction volume and scaled net
positions. Despite having access to a very granular data set, the analysis is focused on high-frequency traders
and market makers during the ﬂash crash, and less on the properties of the remaining market participants.
Our present work aims to ﬁll in the above gaps, by focusing on the remainder of the market participants,
namely traders relying on execution services for their execution. In particular, we seek to analyse such traders
which do not have direct market access (DMA), but rather trade through brokers/execution services.
2
Limit Order Book as a queuing system with diﬀerent agents
To account for the origin of any order, we consider a ﬁnite set of agents A, representing diﬀerent traders or
agent types acting together in a limit order book. An agent is denoted as α. Each agent α ∈A generates a
ﬂow of orders which aﬀect the state of the LOB.
Deﬁnition 2.1 (Limit Order (LO)). A limit order x = (t, p, q, α) is characterized by
• an arrival time t ∈R+,
• a price p ∈δN which is a multiple of the price tick δ > 0,
• a quantity q ∈Z \ {0} with q > 0 denoting buy orders and q < 0 denoting sell orders,
• the identity α ∈A of the agent submitting the order.
A limit order is considered “outstanding” as long as it has neither been cancelled nor fully executed.
Furthermore, we denote the unit point mass at x by ϵx and by
M+(R+ × δN × A),
the space of positive measures on R+ × δN × A, and by
M(R+ × δN × A),
the (vector) space of signed measures on R+ × δN × A. With this in mind, we may represent the collection of
outstanding orders as a signed measure
µ : R+ × δN × A →Z,
([0, T], {p}, {α}) 7→µ([0, T], {p}, {α}),
(1)
3
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 4

where µ([0, T] × {p} × {α}) represents the (net) volume of orders submitted by agent α at price p, between
time 0 and T. The measure µ is an element of M(R+ × δN × A), the (vector) space of signed measures on
R+ × δN × A, and its Jordan decomposition
µ = µ+ −µ−,
corresponds to the distribution of outstanding sell and buy orders. The signed measure deﬁned in Equation (1)
allows to describe diﬀerent views on the limit order book. The omniscient view and public view form extreme
cases, while the third one, the broker view, builds a mixture between the ﬁrst two.
2.1
Public View
The public view (i.e.
anonymized view) on the limit order book corresponds to the information available
to market participants who observe the volume of orders at each price.
However, it does not contain any
information regarding the origin nor the submission times of the single orders. Hence, most market participants
only observe the queue size Qp at each price level p
Deﬁnition 2.2 (Queue Size). The queue size for any price p ∈δN is denoted by
Qp =
X
α∈A
µ([0, t], {p}, α).
(2)
We call Q : δN →Z the anonymized limit order book, Q ∈M(δN) and belongs to the state space ZδN.
The public view is visualised in Figure 2a and corresponds to the sum of all orders’ quantity at a particular
level. The agent neither observes the number of orders nor the color (i.e. the agent id).
2.2
Omniscient View
The omniscient view of the limit order book is the collection of all outstanding limit orders, including the
information about their time of submission and the identity of the submitter. This information is represented
by the measure µ. E.g. in Figure 2c, the omniscient view not only contains the single orders with prices and
quantities, but also the color (i.e. the agent id).
For example, the measure of the outstanding orders from agent α ∈A is given by
µ(·, ·, {α}) ∈M+(R+ × δN).
(3)
While the omniscient view exists usually no one has access to it. The closest to the omniscient view is the
view, which the corresponding exchange has on the order book because it has some origin about all the ﬂow in
the LOB. However, in many cases the exchange is not able to distinguish between the ﬂow of diﬀerent clients
from a broker. Thus, the exchange sees all orders of a particular broker as one aggregated ﬂow.
2.3
Broker View
The omniscient view and the anonymized limit order book represent two extreme cases of information on
the limit order book. However, there are intermediate situations corresponding to partial information on the
limit order book. An important case is the case of a broker who can observe the order submissions times and
identities for a subset B ⊂A of agents. This broker will have a less detailed view of the limit order book, which
corresponds to aggregating over all agents not in B. Denote by B∗= B ∪{∆} the set obtained by adding one
element to B; this element will represent all other agents not included in the broker’s set of clients. The broker
view of the limit order book may then be described by a measure µB ∈M(R+ × δN × B∗) deﬁned by
µB(·, ·, {α})
=
µ(·, ·, {α})
α ∈B,
(4)
µB(·, ·, {∆})
=
X
α/∈B
µ(·, ·, {α}).
(5)
4
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 5

p
Qa/b
i
(t)
-20
-10
0
10
20
(a) Public view
p
Qa/b
i
(t)
-20
-10
0
10
20
(b) Broker view
p
Qa/b
i
(t)
-20
-10
0
10
20
(c) Omniscient view
Figure 2: Diﬀerent views of the same LOB snapshot. Note, only the omniscient view has complete information
about the queue priority of each order.
An exemplary broker view snapshot is visualised in Figure 2b. Yellow and light blue correspond to agents
α ∈B, thus are from the broker’s clients. These orders are observed with their particular ID and viewed via
µB(., ., {α}), while green and red orders would correspond to “all other agents” (∆) which are not in B, the
broker’s set of clients. These orders are seen as µB(., ., {∆}). Furthermore, the broker does not observe the
speciﬁc time as (5) suggests, but rather the relative time since the broker knows its queue position. Hence, the
broker can (only) know that an order has been submitted between two orders of its own clients.
Most literature aims to model the public view of the LOB. These models have been shown to be useful for
describing certain dynamics of limit order books. These dynamics include general price moves or distribution
of queue sizes. The detailed queue and a speciﬁc order’s queue position, however, is generally not available in
both public data and the majority of the models in the literature. This has led to research aiming to estimate
the queue position of an order such as [19]. It turns out, “queueing eﬀects can be very signiﬁcant”[19] and
accounting for the queue position should not be ignored when designing trading algorithms. In accordance to
this, keeping track of the queue size rather than the entire collection of orders does not allow cancellations to refer
to particular orders. This makes keeping track of how orders ﬂow through the queue impossible. Furthermore,
models in the literature do not distinguish between diﬀerent agents submitting these orders. However, diﬀerent
agents generally trade with diﬀerent expectations and intentions. This is likely to be reﬂected in the way they
place orders (close to the best prices or deeper in the book), as well as how they tend to cancel their orders.
Instead, a LOB model which accounts for this heterogeneity allows to do this. We remark that the topic of
identifying determinants of limit orders cancellation has been extensively studied recently, and would be an
interesting research direction to explore, in itself.
As Figure 1 visualizes, limit orders sent through a broker part of a larger parent order. Since these parent
orders are central in the sequel of the paper, we formally introduce the structure of a parent order.
Deﬁnition 2.3 (Parent order). A parent order P is deﬁned by a number of variables some of which are
determined by the submitting trader, others are only known at the end of the execution.
• a submission or arrival time t ∈R+,
• a target quantity qtarget ∈Z \ {0}, the total quantity which shall be executed in the market,
• an executed quantity qexec ∈Z which corresponds to the total sum of executed child orders.
The parent order’s target quantity qtarget can be decomposed in its
1. absolute quantity ˜q = |qtarget| ∈N,
2. sign (buy or sell order)
sign(qtarget) =
(
−1,
if qtarget < 0
1,
if qtarget > 0.
(6)
Each order, depending on its size and preferences, has an order placement schedule, which we denote by
X = {x1, . . . , xN},
xi = (ti, pi, qi, αi) ∀xi ∈X,
(7)
5
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 6

where each element has the form of a LO as deﬁned in Deﬁnition 2.1. The schedule contains all LOs placed
in the LOB during to the parent order execution. Hence, αi = α since all limit orders are posted by the same
agent. Note, X may contain eﬀective market orders as executable limit orders. In other words, a buy limit
order (qi < 0 with price pi = ∞) would correspond to a buy market order (qi > 0 and pi = 0 to a sell market
order respectively).
Additionally, there is an execution schedule
X exec = {x1, . . . , xN},
xi = (ti, pi, qi, αi) ∀xi ∈X exec,
(8)
which is comprised of the record of all executed limit orders for parent order P. This may be
1. a market order x with p ∈{0, ∞} sent within the order schedule eq. (7); in this case, x ∈X.
2. a market order x sent by any other agent which executes an outstanding order from X; in this case,
x ∈X exec but x ̸∈X.
Any x ∈Xexec may not be the complete market order but only the fraction which aﬀected a limit order in X.
For instance, if an incoming market order executes two limit orders from X currently in the limit order book,
there are two entries in the data set. In contrast to X, the execution schedule X exec may contain orders from
diﬀerent agents. Note, (7) and (8) are generally determined during the execution of the parent order.
A full description of the market, the omniscient view, is not always available. The broker view, however, oﬀers
a partially more detailed view on the market, in particular of the broker’s set of agents B. Thus, we want to
shed some light into what B consists of to better understand the limit order market ecosystem. In case, the
ecosystem can be separated into several groups of order ﬂows, modelling the order ﬂow of each group is a much
more feasible and tractable task in comparison to modelling every single agent α ∈B. Thus, the remainder of
this paper analyses the order ﬂow of a broker, and separates a typical set of agents using execution services into
diﬀerent representative groups. These show homogeneous behaviour within their group but diﬀer substantially
across diﬀerent groups.
3
Segmentation of agent types
This section considers the task of segmenting the population of traders that send orders to the brokers. Traders
sending orders builds the very left hand side of Figure 1. Our analysis of this process stands in contrast to
known works in the literature, since most studies only use anonymized order ﬂow data, as outlined in Section 1.1.
Few studies use non-public LOB data, and mainly [15] has access to the trading accounts. To the best of our
knowledge, our study is the ﬁrst one to provide an analysis of parent orders arriving at the broker. Consequently,
the available data structure not only allows us to observe what arrives in the LOB and who sends it, but also
whether several limit orders come from the same parent order. Uncovering latent similarities across traders
and identifying diﬀerent trader typologies can potentially facilitate better modelling of the parent order ﬂow
in LOBs. The main implication of our ﬁndings is that one can move beyond modeling each agent or trader
independently, and pave the way for modelling each homogeneous group or cluster of agents.
3.1
Data set and Features
For the analysis, we use anonymized trade execution data from a large broker. This data builds a detailed
view on a subset of the entire LOB as explained in Section 2. The universe is set to stocks from STOXX 600
and buckets of 1-month duration will be employed in the segmentation. In other words, for each asset i and
time period t, the set of traders that execute their trades via the broker is denoted as Bi,t where each agent
α ∈Bi,t has sent at least one order to the broker which led to an execution. Clearly, Bi,t ⊆Ai,t, the whole set
of agents active in a LOB of the given ticker. Instruments are primarily analysed separately; joint analysis is
used primarily for matters of comparison and stability, in particular in Section 3.4.
Generally speaking, the broker manages the execution and the child orders which are sent to the LOB. For the
analysis, we thus rely on the parent order structure and the corresponding statistics for each agent. Features
regarding the single child orders are not included. This means: when do agents send orders, how large are
6
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 7

they, and how aggressive shall they be executed? The corresponding data ﬁelds are primarily side (buy/sell),
number of orders, time of submission and size. The resulting features/statistics of this information include, for
example, the average direction of an agent’s trades, the number of orders an agent has submitted, distributional
properties of the day time an agent submits orders, or an agent’s order sizes’ standard deviation. Information
regarding external information or market conditions such as momentum, volatility, etc.
are also used.
A
detailed description of each feature can be found in Table 14.
Altogether, this amounts to a data set of n = |Bi,t| agents with p features
X ∈Rn×p with xα = (xα,1, . . . , xα,p) ∈Rp ∀α ∈Bi,t
describing Bi,t. Each vector xα describes the parent order structure of agent α in instrument i during period t.
(a) Marginal distribution
(b) Pearson correlation matrix
Figure 3: Features of data.
Figure 3 shows the distribution and correlation of computed features for one exemplary Bi,t from the STOXX
600. Many features, such as the ratio to which a particular agent speciﬁes a maximum price for execution
(minimum price for sell orders respectively) – market order ratio – tend to be rather 0 or 1. I.e., most agents
either always or never indicate a limit for executions of child orders. Other features are very skewed, for example
n days, the number of days an agent sends an order. This is because most agents only send very few orders
during one month for a given ticker.
To visualize agents in a lower-dimensional space, methods such as principal component analysis (PCA) [14] or
spectral embedding [4] may be applied to obtain further insights into the structure of the agents interacting
with ﬁnancial brokers. To this end, Figure 4 shows two exemplary features in the embedding space. The mean
creation time of a client’s orders in Figure 4a and the ratio indicating the fraction of orders of a particular trader
which contains a maximum price for the execution (minimum price for sell orders respectively) in Figure 4b. For
both features in Figure 4 there are areas of the embedding where traders with similar values of the corresponding
features are clustered. For example, there exists an area of traders which have much higher mean creation time
compared to that of other clusters. In Figure 4b, a group of traders can be encountered which tends to specify
a limit price when sending orders for executions. Additionally, the fact that the point cloud in the embedding
is not just a sphere indicates some structure in the underlying data which can be further exploited.
3.2
Spectral Clustering
As outlined in Section 2, a broker has a detailed view on a subset of the market, i.e. knows the trader identity
and the speciﬁc time of an order, for all agents α ∈Bi,t. For ease of notation, we will refer to Bi,t as B
in the sequel. To better understand the structure of a typical set of traders which use a broker, this section
segments B into a partition C = {C1, . . . , CK}, in order to obtain representative agent types that best describe
the structure of a broker’s clients.
Clustering algorithms are designed to do exactly what we want to do. They separate the observations into
diﬀerent, typically unknown, classes or clusters such that observations within the same cluster are more similar
7
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 8

(a) Mean creation time
(b) Ratio of speciﬁed limit price
Figure 4: Exemplary embedding using ﬁrst three eigenvectors of the normalized Laplacian matrix using the
spectral embedding method from [4]. The color of the nodes indicates the values of the associated feature. The
brighter the points, the higher the value of the corresponding feature.
to each other, while observations that end up in diﬀerent clusters are rather diﬀerent or dissimilar to each other.
A partition C = {C1, . . . , CK} is sought after, such that
1. Ck ⊆B,
2. Ck ̸= ∅∀k ∈{1, . . . , K},
3. Ck ∩C′
k = ∅∀k ̸= k′,
and furthermore is optimal with respect to some objective. In our case, this means every trader would belong
to a certain type. These types should be heterogeneous, but traders of the same type should rather form a
homogeneous population with similar characteristics. Referring to Figure 1, we would like to shrink down
the number of nodes of many individual traders submitting parent orders on the left hand side to just a
few nodes representing each trader type. K indicates the number of types the agents shall be separated into.
¯x1, . . . , ¯xK ∈Rp are the corresponding cluster centers indicating the average features (i.e. coordinates) of the of
the data points (i.e. agents) aﬃliated with the corresponding cluster, so ¯xk,j =
1
|Ck|
P
α∈Ck xα,j ∀j ∈{1, . . . , p}.
Essential to each clustering algorithm is a distance matrix W ∈Rn×n which contains the distance Wα,α′ between
observation xα and xα′, for some distance measure d. This distance is often the Euclidean distance.
The spectral clustering technique used in this study combines two methods, spectral embedding and the K-
means clustering algorithm [21, 20, 18]. In other words, it creates the partition via an iterative ascent algorithm
on a p′-dimensional, non-linear embedding of the data set, describing the agents’ trading behaviour.
1. Construction of the adjacency graph
The adjacency graph indicates for each pair of observations whether these are connected or not.
In
particular,
A ∈Rn×n where Ai,j =
(
1 if ∥xi −xj∥2 < ϵ
0 else,
∀i, j ∈{1, . . . , n}.
(9)
Two vertices are connected by an edge if their Euclidean distance in the actual space Rp is below a certain
threshold ϵ. Alternatively, one may connect a vertex i to its l nearest neighbors where l ≤n, l ∈N.
2. Weighting the similarities
8
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 9

This step weighs the connections between observation i (row) and j (column). The common choice is the
heat/rbf kernel. In this case, the matrix W ∈Rn×n is computed with
Wi,j =
(
e−
∥xi−xj ∥2
σ
if Ai,j = 1
0 else
∀i, j ∈{1, . . . , n},
(10)
for some user-tuned bandwidth parameter σ ∈R+. The closer (i.e. more similar) the observations xi
and xj are in Euclidean distance, the higher the value Wij. Alternatively, whenever the input matrix is
binary, with Ai,j = 1 for connected vertices, we set Wi,j = 1 if Ai,j = 1.
3. Compute eigenmaps via ﬁrst p′ eigenvectors
Next, the generalised eigenvector problem
Lf = λDf,
(11)
is solved. D ∈Rn×n is a diagonal matrix containing the row-sums of W, i.e. Di,i = P
j Wi,j. We deﬁne
L = D −W to be the unnormalized Laplacian matrix (also referred to as the Combinatorial Laplacian).
The solution of eq. (11) is a set of (sorted) eigenvalues λ = (λ0, . . . , λn−1) for which λ0 ≤λ1 ≤· · · ≤λn−1
holds. For the corresponding eigenvectors f = (f0, . . . , fn−1) from eq. (11) λ0 = 0 and f0 = (1, . . . , 1) ∈
Rn holds [24]. The multiplicity of the λ0 = 0 indicates the number of connected components in the
graph.
Finally, the eigenvectors f1, . . . fp′ are then used for the p′-dimensional embedding and yi =
(f1(i), . . . , fp′(i)) ∈Rp′.
4. Clustering the low-dimensional embedding
Finally, the agents are clustered in this low-dimensional embedding via the K-means algorithm [16]. The
objective function optimized by the algorithm is given by
min
C,{¯yk}k
K
X
k=1
|Ck|
X
α∈Ck
∥yα −¯yk∥2,
(12)
where yα, ¯yk ∈Rp′, the space of the embedding. The objective function (12) corresponds to the mini-
mization of the variance within the clusters with respect to partition C. Optimization is done via iterative
descent, alternating between recomputing cluster centers ¯yk and reassigning the observations yα to the
nearest cluster center2.
In contrast to K-Means, spectral clustering is a non-linear clustering method. This enables the algorithm to
potentially uncover clusters which are not convex [24] since the clustering is not performed in the original
feature space Rp, but rather in the embedding space Rp′. This capability of uncovering non-linear relationships
makes spectral clustering more ﬂexible in comparison to K-Means.
The features prepared in Section 3.1 are now used to cluster the agents. Several clustering algorithms, such as
K-means and spectral clustering, are used to gain insights into a potential segmentation of the agents’ structure.
For this, the representative agent types, or centroids, are analyzed.
Extracting centroids when using spectral clustering is not as straight forward as for K-Means. This is because
the embedding procedure described above is not invertible for any arbitrary point. Hence, a point y ∈Rk cannot
be mapped into the actual feature space Rp. To overcome this, one can use the center of a cluster’s observations
in the actual space from the data X ∈Rn×p, i.e. ¯xk =
1
|Ck|
P
i∈Ck xi ∀k ∈{1, . . . , K}. Alternatively, the
prototype for cluster k can be deﬁned as xi ∈Rp with i = arg min
i∈Ck
∥yi −¯yk∥2. In other words, the observation
xi is the one whose embedding yi is the closest to the cluster center ¯yk in the embedding space. In this study,
the ﬁrst method is used to obtain cluster centers, as it is less prone to outliers for some feature of the prototype
xi. The cluster centers are then used to give details about properties and provide a comparison of the diﬀerent
agent types.
Several algorithms were used to cluster Bi,t and ﬁnd an optimal partition C. In the following, we particularly
outline observations and statistics when comparing the partitions between K-means and spectral clustering in
more detail for one exemplary Bi,t. The number of clusters K ranges from 2 to 5. The number of agents for
the ticker is ∼80. Some observations may be made:
2See [14] for the detailed algorithm.
9
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 10

1. Cluster sizes: Generally, the number of observations in the clusters is neither very large nor very small.
There is no cluster with only very few observations.
2. Consistency: The partitions using K-means and spectral clustering are very similar. This can quantiﬁed
by the adjusted rand index (ARI) which indicates the consistency across two partitions.
Let C(1) =
{C(1)
1 , . . . C(1)
K } and C(2) = {C(2)
1 , . . . C(2)
K } be two partitions. The ARI reads
ARI =
P
k,k′
 nk,k′
2

−
hP
k
 ak
2
 P
k′
 bk′
2
i
/
 n
2

1
2
hP
k
 ak
2

+ P
k′
 bk′
2
i
−
hP
k
 ak
2
 P
k′
 bk′
2
i
/
 n
2
,
(13)
where nk,k′ = |C(1)
k
∩C(2)
k′ | denotes the number of observations inside C(1)
k
and C(2)
k′ and ak = P
j nk,k′ =
|C(1)
k | (bk′ = P
k nk,k′ = |C(2)
k′ |). The index takes a maximum value of 1 if C(1) = C(2).
Table 1 shows the ARI for diﬀerent values of K. A particularly high consistency is indicated for 2 and 4
clusters. Noteworthy is the high consistency taking into account that K-means is performed on the actual
feature space (Rp), while the spectral clustering is based on the non-linear embedding in Rp′, p′ ≪p. In
other words, regardless of the feature space employed, the recovered partitions are very similar.
# Clusters
2
3
4
5
ARI
0.7979
0.5107
0.7968
0.6153
Table 1: Table indicating the ARI between K-means and spectral clustering. The higher the number, the higher
the consistency between to partitions; the maximum value ARI can attain is 1, indicating a perfect matching
of the clusters.
3. Stability of clusters: Increasing K leads to a sequential splitting of the data cloud into clusters. E.g.
one cluster gets further split when increasing K by one unit. The other clusters and their aﬃliated traders
remain stable.
4. Number of clusters: Setting K = 2 or K = 4 leads to the best scores. First of all, the consistency is
better than for 3 and 5 clusters indicated by higher ARIs in Table 1. Lastly, Table 2 shows the variance
between agents and their corresponding cluster center. In particular, the more the variance decreases, the
more justiﬁed is the addition of another cluster. The second diﬀerences of the variance within the clusters
can indicate how the variance reduction of an additional new cluster changes. This helps to identify a
K, for which an increase leads to a much lower variance reduction. In particular, values for K would be
either 2 or 4, which goes in line with the other metrics.
# Clusters
1
2
3
4
5
6
7
8
9
Variances
3.914
3.507
3.210
2.981
2.871
2.738
2.640
2.596
2.536
2nd Diﬀs.
-
0.108
0.069
0.118
-0.021
0.034
0.053
-0.016
-
Table 2: The variance between an observation and its corresponding cluster. The stronger the decrease when
K is increased by one cluster, the larger is the marginal eﬀect of the new cluster to separate the data.
3.3
Representative agent types
Despite the ﬁnal goal being the heterogeneity of the aggregated order ﬂow caused by diﬀerent clusters, the
cluster centers ¯xk =
1
|Ck|
P
i∈Ck xi are computed to interpret the agent types. Such resulting cluster centers for
a subset of the features used are shown in Table 3, for one exemplary Bi,t.
In fact, as shown in Table 4, the four agent types may be summarised as follows:
1. Quantitative agents (C-Quant): The most distinguishable agent type is cluster 1, which contains
those agents that submit many trades within the period, with a smaller trade size. Despite trading rather
small amounts, the total volume traded is by far the highest in this cluster. Also, the number of days
during which the cluster’s agents trade is 12 days, which is several times higher than the second highest
10
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 11

1: C-Quant
2: C-Day VWAP
3: C-Signal
4: C-Res
Buy ratio
0.63
0.55
0.63
0.65
Cancellation ratio
0.26
0
0.15
0.07
# Trades per month
219.7
1.72
4.08
5.03
Maximum order creation time
16:10:47
08:32:04
15:02:03
14:34:05
Mean order creation time
12:03:50
08:25:34
14:20:00
11:31:56
Mean order size (in ADV)
0.01
0.03
0.06
0.06
Mean momentum (bps)
2.285
-17.87
29.94
38.26
Mean volatility
22.2
23.03
22.42
22
Minimum order creation time
07:58:08
08:19:10
13:34:31
08:40:12
# Active days per month
13.47
2.1
3.71
4.95
St. dev. of order creation time
02:24:49
00:07:12
00:42:16
02:40:46
Table 3: Exemplary centroids setting K = 4 for one of the 25 most liquid STOXX 600 instruments during
December 2019. Liquidity in this case refers to the total number of trades in the data base. The highest (lowest)
value of the corresponding features are highlighted in blue (red).
Cluster Name
Cluster Description
C-Quant
Mainly quantitative traders, many trades, small volumes, or-
ders sent throughout the day, execution with few child orders
leading to a large POV, net inventory closer to 0
C-Day VWAP
Mostly VWAP as execution, few orders, only sent in the
morning, almost no cancellation
C-Signal
Typically trading in the afternoon (especially US market
opening), large trades, large amount traded in dark venues,
large POV in general
C-Res
Large orders, medium frequency, sent throughout the day
Table 4: Summary of representative agents.
value. Cluster 1 exhibits the highest average cancellation rate, indicating that this agent type perhaps
tracks the execution of its trades more actively than other types. Also, the day time of the trades is
uniformly distributed across the whole day, with a mean creation time around noon. This type of agent
may be summarised as a “quantitative agent”, called C-Quant in the following sections.
2. Day VWAP agents (C-Day VWAP): The most distinct cluster from C-Quant is cluster 2 as its
features exhibit the largest anti-correlation to features of C-Quant. The number of trades per agent is
the lowest, and all trades are submitted very early in the morning. The average trade size is larger than
for C-Quant, yet not the largest across the agents for this partition. Most noticeable apart from the
few number of trades with larger size is the creation time of the order, which typically only occurs before
market open. This indicates that these orders are large orders typically sent before market opening, and
with an execution target over the entire day. Looking at the execution algorithm, one can primarily ﬁnd
rather passive algorithms such as VWAP, which further supports the previous statement. This trading
behaviour is further reﬂected in the cancellation rate, which is the lowest across all clusters, while having
most child orders during the execution. This type of agent is summarised as a “Day VWAP agent”, called
C-Day VWAP in the following sections.
3. Signal agents (C-Signal): Cluster number 3 is most distinguishable due to its creation time, which
shows a minimum of ∼13:30 and a maximum of ∼15:00 for the corresponding data slice. Hence, this
is an agent type which is typically active in the afternoon (which corresponds to the opening of the US
market since it is a STOXX 600 instrument). Similar to C-Day VWAP, the cancellation rate is quite
small, only ∼5%, when compared to C-Quant which is around ∼14%. This agent type tends to execute
large order sizes (5% of the average daily volume of the last 20 days). Additionally, the cluster in this
example has a high percentage of volume, and signiﬁcant fractions are executed via dark venues which
leads us to assume the agent type is less concerned about execution costs, but has a high urgency – hence
also executes a lot in dark venues to mitigate traces in the market. The reason may be that this agent
type wants to act on trading signals and is thus referred to as a “Signal agent”, called C-Signal in the
following sections.
4. Residual agents (C-Res): Cluster 4 indicates agents with the largest average trade size, and only about
11
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 12

ﬁve trades per month. The trades are submitted during the entire day, which is also indicated by the high
standard deviation of the creation time. Furthermore, the standard deviation of the sizes, as measured in
the logarithm of the average daily volume percentage, is the highest. This is the “least distinguishable”
agent type, and seems to be in-between the other three clusters. One possible reason may be that some
agents trade diﬀerent strategies, and thus do not act very homogeneously. Hence, these agents may be
referred to as “residual agent”, denoted as C-Res in the following sections.
3.4
Stability of clusters
Section 3.3 shows that the set of agents Bi,t, trading asset i during period t through a broker, can be segmented
into diﬀerent clusters. Setting K = 4 gives an appropriate number of agent types which can be interpreted,
and are also very distinct in their representative features. Moreover, the partitions do not change signiﬁcantly
when changing the clustering algorithm or the feature standardisation.
What is unknown is how the cluster aﬃliations and the representative agent types change over time or diﬀerent
instruments. Are the results in Section 3.3 random or is the partition rather stable? This section addresses
the stability of the agents and clusters, both across diﬀerent instruments as well as diﬀerent time slices. One
problem arising when comparing two partitions in the present case is that most often Bi,t ̸= Bj,t′. In other
words, traders which are active in asset i during period t do not necessarily trade asset j during period t′.
This is expected to hold in particular for traders which tend to trade at lower frequency or rather long-term
strategies. Nonetheless, the following two questions are of particular interest:
1. How stable is the aﬃliation of an agent to a particular cluster? Do agents change their behaviour and
act diﬀerently across time or diﬀerent tickers?
2. How stable are the representative agent types and their features presented in Section 3.3? How do they
vary across time and diﬀerent tickers?
Two approaches are pursued to answer these questions:
1. Joint clustering of several data slices:
As before Bi,t is the set of agents α with at least one trade in asset i during period t. For example,
¯xi,α =
1
|Ti,α|
P
t∈Ti,α xi,t,α, where Ti,α = {t|α ∈Bi,t} denotes the average of a trader’s features across all
time periods in which they have traded at least once.
If T periods of one asset i, i.e. Bi,t ∀i ∈{1, . . . , T} are clustered together, a high concentration of
observations from one agent, e.g. xi,t,α, Ti,α in one cluster Ck indicates consistency of the agent across
diﬀerent time spans, and similar for diﬀerent assets in the same period. Denoting Pα(α ∈Ck) as the
empirical probability for an observation of agent α to be in cluster Ck, the entropy
Hα = −
X
k∈{1,...,K}
Pα(α ∈Ck) log(Pα(α ∈Ck))
(14)
is used to measure a client’s concentration in one cluster. Additionally, the maximum aﬃliation proba-
bility, deﬁned as
max
k
Pα(α ∈Ck),
(15)
indicates a more interpretable degree of concentration.
For evaluation, we compute the log-weighted
average of both (14) and (15) across diﬀerent traders. This assigns a higher weight to agents active in
many tickers, and none to agents which are only active in one ticker.
2. Meta clustering:
For stability of the representative agent types, their representative features should coincide over diﬀerent
tickers (or time spans). Matching the clusters of two tickers/time frames is diﬃcult for two reasons.
Firstly, an agent does not necessarily behave equally in diﬀerent tickers (or time) which makes a mapping
based on trader aﬃliation not necessarily correct.
Secondly and more importantly, many agents are
potentially active only every couple of months and not in every ticker Bi,t ̸= Bj,t′. Hence, the intersection
of Bi,t and Bi,t′ (or Bj,t) may not contain enough samples to correctly match the clusters from two
diﬀerent partitions.
12
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 13

To circumvent this problem, meta clustering can be applied. In particular, every Bi,t is clustered as
before. The result are several diﬀerent cluster partitions, T diﬀerent cluster partitions for each month
clustered of one particular instrument.
Ci,t with Ci,t = {Ci,t
0 , . . . , Ci,t
K } ∀i ∈{1, . . . , N}, t ∈{1, . . . , T}
where each partition Ci,t
k
has its cluster center ¯xi,t
k
=
1
|Ci,t
k |
P
α∈Ci,t
k xi,t,α. The K · |T| or (K · |N| for
instrument dimension respectively) cluster centers obtained in the ﬁrst step are then clustered in the
second step. A high concentration of the ﬁrst stage cluster centers indicates a rather high stability of the
agent types and their representative features. In other words, a very clear partition with low variance
within the cluster, as well as a high variance between values from diﬀerent cluster centers, are expected.
In our computations, the number of clusters is set to K = 4 as outlined in Section 3.3. The analysis is performed
for the 25 most liquid instruments in the STOXX 600 index, in terms of the numbers of parent orders submitted
in the period. Two years of data corresponds to 24 partitions per ticker. Figure 5 shows the distribution of
both entropy and the maximum aﬃliation probability across the agents. Table 5 shows log-weighted values for
entropy and maximum aﬃliation, in both ticker and time dimension. Log-weights with respect to the number
of tickers (respectively, time periods) a trader has been active in are used to give higher weights to such traders
that span across several distinct sets.
The log-weighted average of the entropy of ∼0.4, which is relatively low compared to the maximum value
of entropy for 4 clusters of 1.4. The log weighted maximum aﬃliation probability is ∼0.8 = 80%. In other
words, for the cluster Ck which contains most of some agent’s observations, the average probability of that
agent’s observation to be in this cluster is 80%. This indicates a fairly strong stability of the agent’s aﬃliation
to a cluster, across diﬀerent tickers. This indicates, the agents have similar behaviour throughout time and
instruments.
Dimension
Entropy
Maximum Aﬃliation
Ticker
0.4
0.8
Time
0.5
0.76
Table 5: Log-weighted average of agents’ entropy and maximum aﬃliation probability. The ﬁrst row indicates
both values for the consistency of the 10 diﬀerent tickers, for an exemplary time slice. The second row indicates
the values for 24 time slices, of one exemplary ticker.
(a) Entropy.
(b) Maximum aﬃliation percentage.
Figure 5: Entropy and maximum aﬃliation probability for diﬀerent agents. The orange vertical lines indicate
the log-weighted averages. Log-weights are based on how many tickers an agent has been active in. Hence,
agents with only one observation are given a weight of equal to zero.
Figure 6 shows traders for several diﬀerent tickers in their embedding space. In particular, the observations of
two traders, one with low (orange) and and one with high (green) entropy are accentuated. The observations
of the low entropy trader can be observed to be very concentrated in the embedding space as expected. The
observations of the high entropy trader are more spread out than for the low entropy trader. However, the
observations of they do not spread across the entire embedding space but are rather clustered as well. This
indicates that even those agents with a higher entropy do have some consistency in their trading.
13
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 14

Figure 6: Observations of two agents visualised in embedding space. Despite one agent exhibiting one of the
largest entropy values, the points are still concentrated in one area of the embedding supporting the evidence
that agents act similarly across diﬀerent tickers.
For the temporal comparison, 24 months of one ticker are clustered together. In particular, for the project’s
aim to use the clustered trader types in order to simulate markets, a certain degree of stability of the clusters
would be beneﬁcial to design a model which represents and captures the heterogeneity which can consistently
be found in LOBs. While an individual agent may change its behaviour, it would be desirable if the cluster
centers and the clusters’ aggregated properties are rather stable.
As outlined above, an agent may have several observations (one for each month, which is used for the analysis).
These can be clustered together, and the entropy along with the maximum aﬃliation probability can be com-
puted. The second row in table Table 5 shows a slightly higher entropy and a slightly lower maximum aﬃliation
probability. This indicates that agents tend to have a slightly higher consistency across diﬀerent tickers at the
same time, than for the same ticker but across diﬀerent time slices. Potentially, many agents may not act every
month, for instance, due to the typical holding period of the purchased instrument (e.g. trading frequency in
general). Thus, despite similar trading behaviour, they do not occur quite as often in a data.
Concerning the stability of the representative features of agent types, meta clustering is applied. In this setting,
cluster centers obtained (1) for diﬀerent tickers at the same time slice, and (2) the same ticker and diﬀerent
time slices, are now considered as single observations. If the clusters are consistent, the meta-clusters (the
clusters of the representative agent types) should be very clear and distinguishable, and each cluster centre
should belong to the corresponding meta cluster. Figure 7 shows the cluster centers in their embedding in R2,
with the colour indicating the cluster from the ﬁrst stage. Cluster centres of the same type are very much
concentrated – e.g. all C-Quant cluster centers are located closely together in the embedding.Just few points
are close to the cluster centers of other types. For some partitions some clusters are closer to the C-Res point
cloud.
This is also conﬁrmed by the meta clustering using K = 4 meta clusters. Both Table 6 and Table 7 show very
small confusion where cluster centres are not correctly grouped in their meta clusters. The most prominent
confusion is occurs in table 6. In particular, for three instruments, the C-Quant cluster is allocated to the
Meta Residual cluster.
Meta Quant
Meta Day VWAP
Meta Signal
Meta Res
C-Quant
22
0
0
3
C-Day VWAP
0
25
0
0
C-Signal
0
0
24
1
C-Res
1
0
0
24
Table 6: Aﬃliation of clusters to meta clusters for diﬀerent tickers.
To further support the evidence for the agent types’ stability, one may look at certain representative features
14
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 15

(a) Diﬀerent tickers, same time period.
(b) Same ticker, diﬀerent time periods.
Figure 7: Embedding of ﬁrst stage cluster centers from the single time slice clustering process. Colours indicate
the ﬁrst stage clustering result. As discovered in Table 3, C-Res is positioned in-between the other three
clusters.
Meta Quant
Meta Day VWAP
Meta Signal
Meta Res
C-Quants
23
0
0
1
C-Day VWAP
0
23
0
1
C-Signal
0
0
24
0
C-Res
0
0
0
24
Table 7: Aﬃliation of clusters to meta clusters diﬀerent time periods.
from the clusters across diﬀerent months or tickers. Figure 8 visualises three of the clusters’ representative
features for 24 diﬀerent months:
• The average number of orders (Figure 8a) was one of the most relevant features in the clustering. Also
the centroid values over time show strong discriminative behaviour here. C-Quant is trading by far the
most in all months, but one where C-Res trades similarly often. C-Day VWAP and C-Signal show
a similar number of trades on the lowest level. This further supports our interpretation above and the
embedding in Figure 7 that C-Res lies in-between all clusters, and sometimes much closer to C-Quant
in terms of the number of trades.
• The mean creation time depicted in Figure 8b shows a both a discriminative and stable behaviour, similar
to the number of trades in Figure 8a. C-Quant and C-Res have a mean creation creation time around
noon both types typically trade throughout the entire day. In contrast, C-Day VWAP trades very early
in the morning and thus shows a mean submission time much earlier than the remaining agent types. For
C-Signal, the mean submission time for diﬀerent months ﬂuctuates to a certain degree around the US
market open. In general, the feature values from C-Day VWAP and C-Signal are well separated from
C-Quant and C-Res.
• For mean percentage of volume, the situation diﬀers slightly.
In general, the centroids’ mean value
ﬂuctuates less and the time series of the values throughout diﬀerent months are more overlapping. The
dashed lines indicating the mean values of the diﬀerent partitions still indicate the same order, where in
particular C-Quant tends to have a high POV since the parent orders often lead to just one child order
execution leading to a large POV. Second highest is C-Res, which in several periods contains traders
which tend to behave like C-Quant agents increasing the average percentage of volume. C-Day VWAP,
apart from one large outlier, has the lowest average POV of all clusters. In general, mean POV illustrates
that not all of the features used in the clustering process are stable or have the same ranking throughout
diﬀerent partitions.
This section’s results indicate a high stability of the agent types presented in Section 3.3. This leads us to
assume that the observations are not random, but rather follow a consistent pattern that exhibits diﬀerent
types of traders acting in the limit order market ecosystem.
15
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 16

(a) Number of orders (log scale)
(b) Mean submission time
(c) Cancellation rate
Figure 8: Exemplary centroid features of one ticker for several months. The solid lines indicate the actual
values over the months, the dashed horizontal lines indicate the average over all months.
4
Decomposition of order ﬂow components
This section reviews properties of the order ﬂow components which were segmented by clustering the agents
in Section 3, both on parent and child order level. This shall answer the question whether the components
which are found to have strong heterogeneity in their features, also lead to diﬀerent dynamics in the LOB.
This section builds a change of perspective as we do not look at diﬀerent traders anymore but aggregate over
a particular cluster as one component. First, we look at the sizes and activities of the components’ ﬂow over
diﬀerent data slices. Following this, child order properties, proﬁtability and the correlation of inventory with
the market’s price move are analyzed to outline notable diﬀerences between the components.
Figure 9a illustrates the distribution of the number of orders for each of the order ﬂow components, throughout
25 diﬀerent instruments of the STOXX 600 in two years. The distributions diﬀer substantially. While C-Day
VWAP and C-Signal show a similar distribution in terms of numbers of trades per month, C-Quant exhibits
the largest numbers of orders. C-Res is once more located in-between the C-Quant and C-Day VWAP/C-
Signal. This matches and further intensiﬁes our previous interpretation that C-Res is some mixture of the
ﬁrst three agent types. Table 8 also indicates that the majority of the trades are done by C-Quant, and only
a small fraction by C-Day VWAP and C-Signal.
The fraction of the total executed quantity from each of the single data slices is indicated in Figure 9b. The
distributions of the fractions from C-Quant and C-Res show a similar shape. The same holds for C-Day
VWAP and C-Signal. In fact, the sum of the executed quantity from C-Quant and C-Res does not vary
much due to their strong negative correlation. The fraction of C-Res tends to increase when a trader from
C-Res behaves rather like a C-Quant trader or potentially as a mixture of C-Quant, C-Day VWAP and
C-Signal.
In comparison to the very small number of orders submitted by C-Day VWAP and C-Signal, the actual
executed quantity is much higher. In other words, while C-Day VWAP and C-Signal tend to account for
only a small fraction of the number of orders, their contribution to the overall executed quantity is much larger
since the orders are generally larger and/or lead to higher execution size (for example, due to fewer cancellations
and longer execution). The mean fractions are displayed in the “Executed qty” row of Table 8.
(a) Number of submitted orders
(b) Fraction of executed quantity
Figure 9: Distribution of the number of trades and the executed quantity.
16
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 17

C-Quant
C-Day VWAP
C-Signal
C-Res
Number of orders
0.69
0.06
0.06
0.20
Executed qty
0.41
0.15
0.11
0.34
Table 8: Average values of the distributions of clients, trades and executed quantities across diﬀerent clusters
4.1
Heterogeneity of child orders
So far, we primarily focused on the structure of the parent orders which were also used for the segmentation
of the traders. This section reviews the diﬀerences of the four diﬀerent components regarding the child orders
which are sent to diﬀerent venues.
This may give further insights to the degree to which the order ﬂow
components diﬀer not only at parent order, but also at the child order level. Table 9 shows a summary of the
orders submitted to exchanges for one exemplary Bi,t. These sample results are for BATS.L for the month of
December 2019. The numbers are normalized either by the mean of the corresponding statistic or by their sum.
In line with the observations regarding the number of orders and executed quantity from Figure 9a and Figure 9b,
the number of child orders submitted by C-Quant is by far the largest. Furthermore, the quantitative agents
have the highest direct market access (DMA) ratio. This means these child orders come from parent orders
that skip the processing of the broker’s execution algorithms, hence primarily using the broker as a platform
to send their orders to a venue. The DMA ratio is also high for the C-Signal component. In this particular
segmentation, C-Signal contains one agent which heavily and exclusively trades with DMA orders leading to
both an unusually high DMA and cancellation rate. This may be an agent which rather belongs to the C-
Quant cluster and impacts the statistics of the C-Signal order ﬂow component. For the C-Res and C-Day
VWAP clusters, the DMA ratio is almost zero, and only around 75% of the child orders get cancelled.
Regarding the order and execution sizes of child orders, the orders of C-Quant have the lowest mean and
standard deviation, as indicated in Table 9.
C-Signal has by far the highest mean order and execution
quantity. A signiﬁcantly higher mean compared to median indicates the presence of outliers for all clusters,
which is potentially due to larger orders in dark venues. In particular, component C-Signal exhibits many
executions in dark venues for this month as mentioned in Section 3.3, hence rendering a large mean order
quantity more plausible. As for the median, the execution quantities are signiﬁcantly lower than the order
sizes. One reason for this may be partially ﬁlled orders – in particular, in dark venues. Note that we exclude
child orders without any partial ﬁlls for the present statistics.
Lastly, Median Distance to Best Price indicates the relative price level at which the child orders of the particular
component tend to be placed (i.e., this can be construed as a proxy for aggressiveness or urgency). Again, the
median is displayed due to its robustness. C-Quant child orders are placed closest to the best price. The
median distance from the best price for C-Res and C-Signal is roughly similar, while the orders from C-Day
VWAP are placed deeper in the book, when compared to child orders from the other clusters.
C-Quant
C-Day VWAP
C-Signal
C-Res
# Child Orders
0.88
0.02
0.03
0.06
Mean Order Qty.
0.23
0.42
2.74
0.61
Median Order Qty.
0.29
0.28
3.11
0.33
Std Order Qty.
0.52
0.61
2.02
0.85
Mean Exec Qty.
0.12
0.18
3.53
0.17
Median Exec Qty.
0.70
0.75
1.76
0.79
Std Exec Qty.
0.33
0.40
2.95
0.31
DMA Ratio
2.27
0.03
1.63
0.07
Cancellation Ratio
1.07
0.90
1.09
0.94
Median Distance to Best Price
0.52
1.81
0.90
0.77
Table 9: Aggregated statistics of child orders by clusters. This table shows the total number of submitted
child orders, the ratio of orders which where sent due to direct market access, the ratio of child orders which
were cancelled, the mean, median and standard deviation for both order quantity and the executed quantity
of orders. The last row shows the median distance of a limit order from the best opposite price. The number
of child orders is normalized by the sum of all clusters; the remainder of the statistics are normalized by the
mean of the four clusters.
17
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 18

Lastly, we look at daily net inventory of the diﬀerent components’ child orders, the sum of the signed traded
sizes (positive for buy, negative for sell) submitted by a cluster during one day. Table 10 indicates the mean
cumulative inventory for one exemplary month. In particular, C-Quant appears to have been a net seller,
while the remaining clusters were net buyers in that particular month during which the corresponding stock
showed a positive return.
C-Quant
C-Day VWAP
C-Signal
C-Res
Average inventory
-0.62
0.12
0.11
0.16
Table 10: Table indicating the mean cumulative inventory of the clusters. Values are normalized with the
absolute inventory of the clusters.
Table 11b indicates the correlation between the components over the whole duration and all instruments
for both the net inventory as well as the order ﬂow imbalance3. Clusters C-Signal and C-Res show the
strongest dependency with a negative correlation of −0.09.
However, the correlations obtained are mostly
statistically insigniﬁcant. Regressing the net inventory or the order ﬂow imbalance of one cluster on any of
the three other components, the coeﬃcients rarely show any signiﬁcant deviations from zero on instrument
basis. For only very few instruments, weak signiﬁcant correlations can be found, but the average p-value over
all instruments considered here is around 0.25. We furthermore ﬁt regressions over several instruments but a
smaller time horizon, under the assumption that the correlations may change over time. Again, few variables
show a persistent signiﬁcance throughout time and the resulting R2 are very small. This indicates that, despite
signiﬁcance for few variable combinations, the explanatory power is small.
C-Quant
C-Day VWAP
C-Signal
C-Res
C-Quant
1.00
-0.05
-0.02
-0.04
C-Day VWAP
-0.05
1.00
0.00
-0.03
C-Signal
-0.02
0.00
1.00
-0.09
C-Res
-0.04
-0.03
-0.09
1.00
(a) Net inventory.
C-Quant
C-Day VWAP
C-Signal
C-Res
C-Quant
1.00
-0.07
0.00
-0.11
C-Day VWAP
-0.07
1.00
-0.02
-0.04
C-Signal
0.00
-0.02
1.00
-0.03
C-Res
-0.11
-0.04
-0.03
1.00
(b) Order ﬂow imbalance.
Table 11: Tables indicating the correlation of the order ﬂow between diﬀerent components.
The resulting both inconclusive as well as insigniﬁcant correlation between the net inventories (OFIs respec-
tively) indicates that not only the behaviour between the cluster diﬀers quite substantially but they are also
independent from each other in the way the accumulate inventory. One possible reason for this may be that
diﬀerent trader types trade diﬀerent strategies which are either not correlated at all (leading to insigniﬁcant
correlations). Another explanation would be that changes depend on the market environment as some strate-
gies may only correlate during certain market conditions. In particular the ﬁrst makes sense since the trading
types seem to act on diﬀerent time scales in the market. The most persistent observation is a slight negative
correlation between C-Quant and the remainder of the order ﬂow components which, however, is relatively
weak.
4.2
Proﬁtability
In Section 3, we showed that traders using execution services may be summarised into diﬀerent clusters. These
trader types have diﬀerent properties when it comes to the type of orders they send. This leads to the assumption
that the objectives of the segmented agent types may diﬀer as well, for example, with respect to their horizon
of investment. To this end, we analyze the hypothetical proﬁt and loss (PnL) for each order ﬂow component,
in order to investigate structural diﬀerences in the returns of the components’ trades. We remark that this
PnL is hypothetical as it does not refer to the actual inventory of the trader. For example, it may be that
a trader is not holding a position for the respective future horizon of time, or that it is actually unwinding a
short position instead of building a long position, or the holding period is diﬀerent. It much rather represents
the average PnL of the respective component, at a certain ﬁxed time horizon.
To investigate the hypothetical proﬁtability of each component, we compute the PnL of each trade via
PnLl
t = −sign(qtarget) log
 pt+l
pexec

,
(16)
3The order ﬂow imbalance is computed with the net inventory divided by the total trade volume of the component. A more
detailed explanation can be found in Section 4.3.
18
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 19

where pexec is the volume-weighted execution price of the corresponding parent order. qtarget is the target
quantity of the parent order, as speciﬁed in Deﬁnition 2.3, and −sign(qtarget) the negative sign of the return.
If, for example, qtarget > 0 the order is a sell order, thus we multiply the log-return with −1. For some timestep
t + l, pt+l denotes the closing price at t + l, where we consider trading days as increments. For l = 0, pt
corresponds to the close price of the day when the corresponding trade happens.
The volume weighted execution price pexec of one parent order is computed via
pexec =
1
qexec
X
x∈X exec
qx · px,
(17)
where qx and px indicate the quantity and the price of each execution in X exec of the corresponding parent order.
Finally, we compute the expected PnL for each component k ∈{1, . . . , K} of trades at day t, as E(PnLl
t,k) by
averaging over all returns for a given l, t, k. The result is a daily time series for diﬀerent lags l ∈{0, 1, 10, 20}
and diﬀerent components k ∈{1, . . . , K}, where each element is the average PnL of the trades occurred on
that particular day. The same computation is done using market excess return, where we subtract the future
market return from the instrument’s future return, for the PnL computation in Equation (16).
Table 12 indicates the average expected PnL in basis points for 2018 and 2019 for 25 instruments. From trade to
close, C-Quant appears to be the only order ﬂow component generating a slight proﬁt over the period covered
here. This indicates, C-Quant is potentially pursuing more intraday like strategies. For C-Signal, the 20-day
return (both raw return and market excess return) are the largest. Even though this is not a realized return,
it gives reason to assume this agent type has some information medium-frequency comparison to the other
components. This is supported by the observation that C-Signal shows the smallest PnL on the same trading
day (l = 0), which further supports our interpretation of C-Signal given in Section 3 that this component is
not aiming for a proﬁt realizing the same day. It may well be C-Signal trades mean reversion signals which
realize only after around a month. Apart from that, C-Day VWAP shows a slight outperformance on the
l = 1 horizon.
l = 0
l = 1
l = 10
l = 20
l = 1, excess
l = 10, excess
l = 20, excess
C-Quant
0.38
0.72
3.39
3.76
0.78
3.78
2.83
C-Day VWAP
-0.25
1.54
-2.04
-3.95
1.42
0.15
1.44
C-Signal
-0.47
-0.43
3.09
13.17
0.32
2.65
10.63
C-Res
0.08
0.37
-1.36
-1.51
0.52
-2.24
-2.19
Table 12: Table indicating the average E(PnLl
k) for agent types in basis points (bps).
The suﬃx
excess
indicates market excess returns over the STOXX 600 baseline.
Additionally, Figure 10 shows the cumulative hypothetical PnL for each component. In line with the observa-
tions from Table 12, C-Signal is clearly outperforming the other agent types on a 20-day horizon (lower right
plot) while having the worst performance from trade to close and to t + 1 (upper plots).
4.3
Order ﬂow imbalances during volatile periods
While some components show diﬀerences in their expected returns with respect to the trading horizon, it stands
to question to which degree the components’ order ﬂow on a particular day is correlated with the return of the
day. In particular, how does the order ﬂow of diﬀerent agent types behaves when markets move substantially.
To this end, we compute the order ﬂow imbalance (OFI) for each instrument via the following measures
OFICk =
P
p∈X k qexec
P
p∈X k |qexec|,
(18)
and
OFIADV =
P
p∈X k qexec
ADV
,
(19)
where X k is the set of parent orders from cluster k on a given day. We compute the imbalance of the order ﬂow
in two ways. The ﬁrst imbalance shown in Equation (18) is normalized by the total executed quantity of the
19
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 20

(a) l = 0
(b) l = 1
(c) l = 10
(d) l = 20
Figure 10: Cumulative PnL E(PnLl
t,k) of agent types over diﬀerent time horizons, l = {0, 1, 10, 20}.
cluster, hence called OFICk. The second imbalance shown in Equation (19) is normalized by the average daily
volume (ADV) from the last 20 days and denoted as OFIADV . This is to take into account that a large OFI,
as deﬁned in Equation (18), does not necessarily mean a large impact to the market during the particular day.
That is because the total traded volume of the cluster might only be a small fraction of the daily volume. In
contrast, Equation (19) makes diﬀerent values of the same day more comparable across diﬀerent clusters, and
is large only if a component’s net inventory is large in relation to the historical ADV. E.g. one cluster might
have a large OFI in terms of own orders but still a very small OFI measured on the ADV due to small traded
volume.
Figure 11 shows a histogram of the OFI as in Equation (18) to simplify comparison. C-Quant stands in
contrast to the other three components. The net order ﬂow peaks around zero, while the other order ﬂow
components have two peaks at zero and one. In particular, the aggregated order ﬂow from C-Quant tends
to be rather neutral in terms of order ﬂow imbalance, which can be due to two reasons. First, C-Quant
trades much more often (albeit smaller sizes) and thus facilitates order ﬂow imbalances closer to zero. Second,
C-Quant pursues more intraday/medium frequency strategies without accumulating larger positions.
Figure 11: Order ﬂow imbalance by cluster, during days of returns with large magnitude.
Table 13 shows the correlation of the OFI computed via Equation (18) in Table 13a and Equation (19) in
Table 13b with the log return from open to close (logOC). C-Day VWAP and C-Res show the clearest picture.
20
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 21

For both the case of days of large returns of the particular instrument (left columns), as well as days of large
returns of the index (right columns), C-Day VWAP and C-Res exhibit a fairly strong positive correlation.
This holds for the net inventory scaled by the traded volume of the particular component (Table 13a), as
well as the net inventory scaled by the market volume (Table 13b). In fact, the correlation of OFIADV with
both the instrument and the index return are larger than the correlation of OFICk with the return. In other
words, when these clusters accumulate net inventory which is also large in terms of the average daily volume,
the instrument is likely to also exhibit a larger return. A possible reason for this may be that the order ﬂow
becomes a driving factor in the market.
cluster
logOC
logOC index
C-Quant
-0.0301
0.0113
C-Day VWAP
0.1590
0.0229
C-Signal
-0.1506
0.0499
C-Res
0.1102
0.1616
(a) OFICk as in Equation (18).
cluster
logOC
logOC index
C-Quant
0.1368
0.0833
C-Day VWAP
0.2044
0.1416
C-Signal
-0.0441
-0.0794
C-Res
0.2189
0.2390
(b) OFIADV as in Equation (19).
Table 13: Correlation between OFI and returns of stocks (column logOC) and return of the index (column
logOC index), for two diﬀerent types of normalized OFI.
C-Signal is the only cluster exhibiting a fairly large negative correlation with negative returns of the instru-
ments. This correlation seems to be less strong when the net inventory is large as deﬁned in Equation (19).
A reason for this may be that due to the high participation rate, C-Signal becomes a driving factor of the
market, similar to C-Day VWAP and C-Res above. The correlation with the index is less clear and varies
between OFICk and OFIADV . However, it seems that the index is more likely to decrease if the net inventory
is large, also based on the average daily volume of the corresponding stock.
C-Quant shows the lowest correlation of net inventory scaled with total trade size, with both the daily return
as well as the index (-0.03 and 0.01, respectively). This is to be expected, taking into account Figure 11 that
shows the tendency of C-Quant to keep a net inventory closer to zero. For net inventories which are large
measured on the total market volume following Equation (19), however, the correlation also seems to turn
stronger. Similar as for C-Day VWAP and C-Res, if the net inventory is large measured on the ADV, the
cluster becomes more of a market driver and a higher correlation with the daily return can be observed.
5
Heterogeneous parent order model
As illustrated in the order process in Figure 1, limit orders sent through execution services are usually part of
a larger parent order. This section proposes a simple model which captures the most important heterogeneous
properties for each of the components extracted in Section 3. Once these parent orders can be modeled, their
scheduling and execution in the LOB may be simulated.
This can be done by replicating the ﬂow of the
parent orders orders into the LOB as depicted in Figure 1 via known execution and order routing algorithms,
some of which are well studied in the literature. Modelling the ﬂow of these components itself without the
direct scheduling and execution can additionally be of high interest to brokers, as this can possibly improve the
broker’s knowledge and service to clients. Rather than aiming to replicate and ﬁt the data to the full extent,
the following model is designed to outline a starting point which has good ﬁts from a marginal perspective
for several stocks, despite being very simple. It also further underpins the structural diﬀerences between the
diﬀerent clusters which have been outlined in the previous sections. Furthermore, we assume independence
between the ﬂows presented in the following, due to the absence of a signiﬁcant correlation structure between
the components, as detailed in Table 11.
5.1
C-Quant
As outlined in Section 3, the C-Quant order ﬂow component is submitting orders throughout the day. Fig-
ure 12c suggests the U-shaped intra-day pattern commonly observed in trading behaviour of limit order books
[9]. In the morning and towards closing time of the market, the intensity of the orders increases. C-Quant
order sizes are of mostly small size and typically executed in just a few child orders. This, however, does not
imply that only one order is sent to the exchange.
21
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 22

As per modelling the C-Quant order ﬂow component, we suggest a non-homogeneous Poisson process. In
particular, {N Quant(t), t > 0} denotes the counting process of the parent order submissions indicating the
number of submitted parent orders up to time t. The arrival time of the n-th parent order is denoted as tQuant
n
.
New orders arrive proportionally to the conditional intensity rate λQuant(t), t ∈[0, T] similar to the shape in
Figure 12c. This is to properly reﬂect the intraday pattern of the C-Quant order arrivals. It must hold that
Z T
0
λQuant(s)ds = 1,
so that the expected number of orders within [0, T] equals one. The conditional intensity function λQuant(t) is
then scaled by the number of expected order submissions for the corresponding day
λQuant(t) · nQuant.
Each of the arriving parent orders additional “marks” or properties as speciﬁed in Deﬁnition 2.3, in particular
a sign and a target quantity. For the C-Quant parent orders, the following considerations are in place
• the logarithm of the expected number of parent orders, parameter N follows a skewed normal distribution,
log(nQuant) ∼sN(a, µ, σ2) with skewness a, mean µ and variance σ2 (Figure 12a),
• the target quantities are ﬁtted with a Laplacian distribution, i.e. qtarget ∼Laplace(µ, b), as illustrated in
Figure 12b,
• the signs of the order is Bernoulli distributed signi ∼B(1, p),
• the probability of an order being a buy order, p, diﬀers across days and is modelled by a Beta(a, b)
distribution; Figure 12d indicates the ﬁt.
The execution of the C-Quant orders is done with the Almgren-Chriss optimal execution framework, ﬁrst
presented in [3]. The execution generally consists of only very few if not just one child order and the execution
time is very short.
(a) Order counts: QUANT order ﬂow.
(b) Order size distribution: QUANT order ﬂow.
(c) Submission times
(d) Fraction of buy orders
Figure 12: Aggregated parent order ﬂow distributions for one stock, over two years, for C-Quant.
22
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 23

5.2
C-Day VWAP
As outlined in Table 3, C-Day VWAP mainly sends parent orders in the early morning around the market
opening. The total number of parent orders is quite small, while execution generally takes places throughout the
entire day. A model for these orders is thus quite simple and can be done without any time dependence, since
we assume all orders to be submitted at market open (i.e. t = 0). The orders are then executed throughout
the day proportional to some estimated volume proﬁle.
For C-Day VWAP, it suﬃces to know how the sum of all buy (respectively, sell) orders is distributed, which
is then executed as one large buy order (respectively, sell order). Denoting XDayV W AP as the set of all parent
orders from the C-Day VWAP component for a given day, the quantities of interest are
X
p∈XDayV W AP
(qtarget)−
and
X
p∈XDayV W AP
(qtarget)+,
where the ﬁrst term builds the cumulative size of all C-Day VWAP buy orders, and the second term all C-Day
VWAP sell orders. The C-Day VWAP component hence consists of two (aggregated) parent orders with
• submission time t = 0,
• target quantities for both orders, where the logarithm of the absolute value, log(qtarget) ∼sN(a, µ, σ2)
where sN(a, µ, σ) follow a skewed normal distribution with skew a, mean µ and variance σ2 (as shown in
Figure 13),
• the sign of the order, which is −1 for the aggregated buy order and 1 for the aggregated sell order.
The aggregated buy and sell C-Day VWAP orders are executed following to the volume proﬁle of the previous
day.
Figure 13: The aggregated parent order sizes (on a log scale) for one stock over two years for C-Day VWAP.
5.3
C-Signal
The C-Signal cluster as outlined in Table 3 sends quite large orders and executes them in a relatively short
horizon. This lets assume C-Signal is a more aggressive player in the LOB, moving the LOB in a certain time
horizon.
As per modelling the C-Signal component, we suggest a non-homogeneous Poisson process similar to C-
Quant. As before, {N Signal(t), t > 0} denotes the counting process of the parent order submissions indicating
the number of submitted parent orders up to time t.
New orders arrive proportionally to the conditional
intensity rate λSignal(t), t ∈[0, T], similar to the shape in Figure 14c. The conditional intensity function
λSignal(t) is then scaled by the number of expected order submissions for the corresponding day
λSignal(t) · nSignal.
The C-Signal parent orders come with the following “marks” or properties
23
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 24

• the expected number of arriving parent orders at a day, nSignal, follows a geometric distribution, i.e.
nSignal ∼Geo(p) (Figure 14a),
• the logarithm of the target quantities C-Signal parent orders log(qtarget) is skewed normal distributed,
log(qtarget) ∼sN(a, µ, σ2) with skew a, mean µ and variance σ2 similarly to C-Day VWAP (Figure 14b).
• the sign of the orders signi ∼B(1, p), where p denoted the probability of a buy orders.
A large proportion of the C-Signal component consists of close related orders. These orders are removed
because they do not form part of the continuous trading session. We suggest the execution of the C-Signal
orders is done similarly to the C-Quant orders using the Almgren-Chriss framework [3]. The detailed execution,
however, is not part of this work. Note, orders from C-Signal are substantially larger than those from C-
Quant, which – together with the frequency of orders and the intraday pattern – constitutes the main diﬀerence
between the two clusters.
(a) Order counts
(b) Order sizes
(c) Submission times
Figure 14: Aggregated parent order ﬂow distributions for one stock over two years for C-Signal.
5.4
C-Res
Both the representative features in Table 3 as well as the embedding of the ﬁrst stage clustering in Figure 7
indicate that C-Res lies in between the remainder of the other clusters. In addition, the confusion matrices
in Table 6 and Table 7 conﬁrm that whenever there exists instability in the market segmentation, one of the
remaining clusters is mistaken with C-Res. To this end, we model C-Res as a random mixture of C-Quant,
C-Day VWAP and C-Res. We suggest random attribution of the mixture following a dirichlet distribution
f(x) =
1
B(α)Π3
i=1xαi−1
i
where
B(α) = ΠK
i=1Γ(αi)
Γ(PK
i=1)
(20)
and x = (x1, x2, x3), α = (α1, α2, α3) are the weights between the three clusters. The random allocation is then
proportionally added to the ﬁrst three components.
6
Conclusion
Many diﬀerent agents act together in limit order books with diﬀerent intentions, trading horizons and infor-
mation sets. This gives reason to assume that order ﬂow in limit order books is not homogeneous but rather
of diﬀerent types. To account for diﬀerent agents submitting orders an alternative notation for limit order
books was given in Section 2. This notation allows to derive diﬀerent views on the order book with diﬀerent
granularity ranging from an anonymised public view to the fully detailed omniscient view.
To investigate the heterogeneity of those agents which make use of brokers, trade execution data was analysed.
Results show these agents may be summarised in four representative clusters which diﬀer substantially in both
their trading behaviour as well as the order ﬂow induced in the limit order book by the parent orders. In
particular, trading frequency, trade size but also order submission time and execution strategies show notable
diﬀerences between these agent types which gives evidence that some heterogeneity may be assumed. The
insights were used to propose a simple model for parent order ﬂow of each cluster in order to capture some of
the heterogeneous dynamics of the diﬀerent trader types in Section 5.
24
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 25

In relation to [15], the results may be seen as additive rather than comparative. In particular, the results
presented in this work refers more to the “fundamental buyers/sellers” and “opportunistic traders” classes
from [15] as the data in this study excludes HFT and market maker agents which have their own execution
platforms. Kirilenko et al. [15] mainly focus on HFTs and MMs in their study. Looking at the entire market
one thus would have to aggregate both studies to get the full picture of the heterogeneity in limit order markets.
In contrast to [15], this study is able to distinguish agents on their actual parent orders for several tickers and
a longer time horizon. This enables to show that the agent types presented in Section 3.3 are consistent over
longer time periods and also exists in diﬀerent stocks. The only noteworthy confusion factor is between C-Res
and some of the other clusters which seem to move towards C-Res under certain conditions.
The results of this study and [15] provide evidence that order ﬂow in limit order books show strong heterogeneity
indicating that modelling LOBs under the assumption of homogeneity is not very valid. In contrast to most
order ﬂow models in literature, such models should hence include some degree of heterogeneity.
This study builds a ﬁrst step towards better understanding limit order markets and their heterogeneity. We
focus on the parent order process, the very left hand side of the order process depicted in Figure 1. Our results
provide a foundation for many future research directions.
The interplay between traders with proprietary
access to the exchange (HFTs and MMs) and traders acting through brokers is yet to be analyzed in detail.
The authors of [15] remark, for instance, that HFTs keep their trading patterns stable also in times of increased
market volatility. More detailed studies are yet missing. It is also to be investigated how exactly orders are
processed and arrive in the LOB. This would correspond to the center part of Figure 1. While this study
provides indications in which fashion each agent type tends to execute orders, it is not exactly clear how much
liquidity from each venue tends to go to the lit or dark venues etc. Lastly, the combination of parent order
ﬂow and HFTs and MMs may be used to create heterogeneous models for entire LOBs. Under the assumption
of similarity of the trader structure between diﬀerent brokers, these order ﬂows may be scaled up to the entire
volume of all brokers. It remains to be investigated whether realistic LOB models can be developed, which
intend to incorporate the entire process shown in Figure 1.
25
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 26

References
[1] F. Abergel, M. Anane, A. Chakraborti, A. Jedidi, and I. M. Toke. Limit order books. Cambridge University
Press, 2016.
[2] F. Abergel and A. Jedidi. Long-time behavior of a hawkes process–based limit order book. SIAM Journal
on Financial Mathematics, 6(1):1026–1043, 2015.
[3] R. Almgren and N. Chriss. Optimal execution of portfolio transactions. Journal of Risk, 3:5–40, 2001.
[4] M. Belkin and P. Niyogi. Laplacian eigenmaps and spectral techniques for embedding and clustering. In
Advances in neural information processing systems, pages 585–591, 2002.
[5] J.-P. Bouchaud, M. M´ezard, M. Potters, et al. Statistical properties of stock order books: empirical results
and models. Quantitative ﬁnance, 2(4):251–256, 2002.
[6] J. Brogaard et al. High frequency trading and its impact on market quality. Northwestern University
Kellogg School of Management Working Paper, 66, 2010.
[7] J. Brogaard, T. Hendershott, and R. Riordan. High-frequency trading and price discovery. The Review of
Financial Studies, 27(8):2267–2306, 2014.
[8] D. Byrd, M. Hybinette, and T. H. Balch. Abides: Towards high-ﬁdelity market simulation for ai research.
arXiv preprint arXiv:1904.12066, 2019.
[9] R. Cont. Statistical modeling of high-frequency ﬁnancial data. IEEE Signal Processing Magazine, 28(5):16–
25, 2011.
[10] R. Cont, S. Stoikov, and R. Talreja. A stochastic model for order book dynamics. Operations research,
58(3):549–563, 2010.
[11] M. D. Gould, M. A. Porter, S. Williams, M. McDonald, D. J. Fenn, and S. D. Howison. Limit order books.
Quantitative Finance, 13(11):1709–1742, 2013.
[12] B. Hagstr¨omer and L. Nord´en. The diversity of high-frequency traders. Journal of Financial Markets,
16(4):741–770, 2013.
[13] J. Hasbrouck and G. Saar. Low-latency trading. Journal of Financial Markets, 16(4):646–679, 2013.
[14] T. Hastie, R. Tibshirani, and J. Friedman. The elements of statistical learning: data mining, inference,
and prediction. Springer Science & Business Media, 2009.
[15] A. Kirilenko, A. S. Kyle, M. Samadi, and T. Tuzun.
The ﬂash crash: High-frequency trading in an
electronic market. The Journal of Finance, 72(3):967–998, 2017.
[16] J. MacQueen et al. Some methods for classiﬁcation and analysis of multivariate observations. In Proceed-
ings of the ﬁfth Berkeley symposium on mathematical statistics and probability, volume 1, pages 281–297.
Oakland, CA, USA, 1967.
[17] S. Mankad, G. Michailidis, and A. Kirilenko. Discovering the ecosystem of an electronic ﬁnancial market
with a dynamic machine-learning method. Algorithmic Finance, 2(2):151–165, 2013.
[18] M. Meila and J. Shi. A random walks view of spectral segmentation. 2001.
[19] C. C. Moallemi and K. Yuan. A model for queue position valuation in a limit order book. Columbia
Business School Research Paper No. 17-70, 2016.
[20] A. Y. Ng, M. I. Jordan, and Y. Weiss. On spectral clustering: Analysis and an algorithm. In Advances in
neural information processing systems, pages 849–856, 2002.
[21] J. Shi and J. Malik. Normalized cuts and image segmentation. IEEE Transactions on pattern analysis and
machine intelligence, 22(8):888–905, 2000.
[22] J. Sirignano and R. Cont. Universal features of price formation in ﬁnancial markets: perspectives from
deep learning. Quantitative Finance, 19(9):1449–1459, 2019.
[23] E. Smith, J. D. Farmer, L. s. Gillemot, S. Krishnamurthy, et al. Statistical theory of the continuous double
auction. Quantitative ﬁnance, 3(6):481–514, 2003.
26
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 27

[24] U. Von Luxburg. A tutorial on spectral clustering. Statistics and computing, 17(4):395–416, 2007.
[25] S. Vyetrenko, D. Byrd, N. Petosa, M. Mahfouz, D. Dervovic, M. Veloso, and T. H. Balch. Get real: Realism
metrics for robust limit order book market simulations. arXiv preprint arXiv:1912.04941, 2019.
[26] Z. Zhang, S. Zohren, and S. Roberts. Deeplob: Deep convolutional neural networks for limit order books.
IEEE Transactions on Signal Processing, 67(11):3001–3012, 2019.
27
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 28

A
Feature table
Feature Name
Explanation
Buy ratio
Pct. of client orders which is a buy order
Cancellation ratio
Pct. of client orders which are cancelled before full execution
# Trades per month
Number of trades per month.
Inventory
Mean inventory accumulation of a client on a given day
NO Limit price ratio
Percentage of the client’s orders for which no limit price has been speci-
ﬁed (maximum/minimum price for execution of child orders)
Maximum
order
creation
time
Latest time at which a client submits an order
Mean order creation time
Average time at which a client submits an order
Mean order size (ratio of
ADV)
Mean order size measured on the average daily volume of the last 20
days, execution may be less.
Mean momentum (bps)
Mean momentum of entire trading day measured in basis points (bps)
Mean percentage of volume
Mean percentage of traded volume during trade horizon (visible ﬁlls +
dark ﬁlls) / (visible market volume), exceeding 100 is indicator for larger
placements in dark venues
Mean volatility
Mean volatility during which a client trades measured on the last 20 days
Minimum
order
creation
time
Earliest time a client creates an order
# Active days per month
Number of days a client trades per month
Mean # orders per active
day
Number of orders a client trades if it trades during a day
Standard deviation # or-
ders per active day
Standard deviation of the number of orders of days during which a client
places at least one order
Standard deviation of order
creation time
Standard deviation of a client’s creation time
Standard
deviation
order
size
Standard deviation of a clients order size
Total order size
Cumulative trade size measured on the average daily volume of the last
20 days. Indication of how much a client in average trades at all
Table 14: Feature list used for the clustering. All features are computed on the base of a one month data set.
For instance, #Trades indicates the number of trades for a particular client per month. The creation time,
measured from the time passed since midnight is set to a minimum of 7 as some clients, sending their orders
on the evening before disrupt the feature distribution. 7am in this case involves all orders sent before market
opening.
28
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 29

B
Plots – Parent order model
Additional ﬁts for suggested distributions for a high market cap stock (left), high volume stock (middle) and
low volume stock (right).
B.1
C-Day VWAP
(a) Order quantities
(b) Order quantities
(c) Order quantities
Figure 15: Order quantities of the C-Day VWAP trader type for a high market cap stock (left), high volume
stock (middle) and low volume stock (right).
29
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 30

B.2
C-Quant
(a) Order counts
(b) Order counts
(c) Order counts
(d) Order quantities
(e) Order quantities
(f) Order quantities
(g) Submission times
(h) Submission times
(i) Submission times
(j) Fraction of buy orders
(k) Fraction of buy orders
(l) Fraction of buy orders
Figure 16: Order counts, order quantities, submission time and fraction buy orders distribution of the C-Quant
trader type for a high market cap stock (left), high volume stock (middle) and low volume stock (right).
30
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 31

B.3
C-Signal
(a) Order counts
(b) Order counts
(c) Order counts
(d) Order quantities
(e) Order quantities
(f) Order quantities
(g) Submission times
(h) Submission times
(i) Submission times
Figure 17: Order counts, order quantities, submission time and buy ratio distribution of the C-Signal trader
type for a high market cap stock (left), high volume stock (middle) and low volume stock (right).
31
Electronic copy available at: https://ssrn.com/abstract=3997109


## Page 32

C
Disclaimer
Opinions and estimates constitute our judgement as of the date of this Material, are for informational purposes
only and are subject to change without notice. This Material is not the product of J.P. Morgan’s Research
Department and therefore, has not been prepared in accordance with legal requirements to promote the inde-
pendence of research, including but not limited to, the prohibition on the dealing ahead of the dissemination of
investment research. This Material is not intended as research, a recommendation, advice, oﬀer or solicitation
for the purchase or sale of any ﬁnancial product or service, or to be used in any way for evaluating the merits
of participating in any transaction. It is not a research report and is not intended as such. Past performance
is not indicative of future results. Please consult your own advisors regarding legal, tax, accounting or any
other aspects including suitability implications for your particular circumstances. J.P. Morgan disclaims any
responsibility or liability whatsoever for the quality, accuracy or completeness of the information herein, and
for any reliance on, or use of this material in any way.
32
Electronic copy available at: https://ssrn.com/abstract=3997109


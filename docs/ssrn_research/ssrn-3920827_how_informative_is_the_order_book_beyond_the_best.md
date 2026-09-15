# How informative is the Order Book Beyond the Best

- **Source File**: `ssrn-3920827.pdf`
- **Total Pages**: 33
- **SSRN ID**: `ssrn-3920827`

---

## Page 1

How informative is the Order Book Beyond the Best
Levels? Machine Learning Perspective
Dat Thanh Tran1∗, Juho Kanniainen1, Alexandros Iosiﬁdis2
1Department of Computing Sciences, Tampere University, Finland
2Department of Electrical and Computer Engineering, Aarhus University, Denmark
Abstract
Research on limit order book markets has been rapidly growing and nowa-
days high-frequency full order book data is widely available for researcher
and practitioners. However, it is common that research papers use the best
level data only, which motivates us to ask is if the exclusion of the quotes
deeper in the book over multiple price levels cause performance degradation.
In this paper, we address this question by using modern Machine Learn-
ing (ML) techniques to predict mid-price movements without assuming that
limit order book markets represent a linear system. We provide a number of
results that are robust across ML prediction models, feature selection algo-
rithms, data sets, and prediction horizons. We ﬁnd that the best bid and ask
levels are systematically identiﬁed not only to be the most informative levels
in the order books, but to carry most of the information needed for good pre-
diction performance. On the other hand, even if the top-of-the-book levels
contain most of the relevant information, to maximize models’ performance
one should use all data across all the levels. Additionally, the informativeness
of the order book levels clearly decreases from the ﬁrst to the fourth level
while the rest of the levels are approximately equally important.
Keywords:
Limit Order Book, Machine Learning, Feature Selection,
Mid-price Movement Prediction
∗Corresponding author: Tel.: +358 401592373
Email address: thanh.tran@tuni.fi (Dat Thanh Tran1)
Preprint
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 2

1. Introduction
The modern stock markets are mainly operated by the electronic limit
order book (LOB) mechanism, which allows traders and algorithms to im-
mediately use order-book data beyond the best levels for their trading deci-
sions. Intuitively, the contents of a LOB can be informative and useful for
trading purposes for many reasons. The order-book asymmetry may reﬂect
trader sentiment or the presence of well informed traders, for which reason
one might want to trade in front of its heavy side [1]. Moreover, data beyond
the best levels reﬂects the order-book liquidity, i.e. the quantity immediately
available for trading and therefore the price of immediacy. Available liquidity
beyond the best levels matters especially when investors’ impatience gener-
ates a sudden liquidity demand across multiple price levels, leading to large
movements in stock prices [2, 3].
Even if the data beyond the best levels were informative, there can be
many reasons to use the best-level data only, often referred to as Level-I data,
to answer certain research questions. First, parsimonious and tractable mod-
els that accomplishes a desired level of explanation or prediction with as few
predictor variables as possible can be preferred for the sake interpretabil-
ity. If models are large and complex, the parameter estimates can be shaky
(having large standard errors), leading to statistical insigniﬁcance and thus
uncertain conclusions. The other reasons to use Level-I data is that data
are more easily obtainable than Level-II data that include quotes deeper in
the book over multiple price levels. Particularly, Level-I data are easier to
pre-process and analyse, and they are well available for academic research.
However, when it comes to the maximization of model’s predictive power,
the current literature lacks to answer the question how informative the top
quotes are compared the quotes beyond them. Moreover, it is unclear if one
should use multi-level order book data, even at the cost of complexity of the
model.
Seeking answers to the research questions above is important in many
ways. First, the major portion of the extant ﬁnancial and econometric lit-
erature rely on Level-I data and for diﬀerent research questions, and it is
important to understand how large impact the exclusion of the data beyond
the best level can have on the results. The literature uses Level-I data, for
example, to analyse micro-structure noise [4, 5], price impact [6, 7, 8, 9],
optimal trading strategies [10], and algorithmic trading [11, 12], model and
predict the price or order-book dynamics [13, 14]. Even if this paper focuses
2
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 3

on the last topic, i.e. the modelling and prediction of the stock prices with
order book data, we believe that our results shed light on other topics, too.
In particular, we are eﬃciently using and assessing on informativeness of the
empirical LOB data in terms of the price formation, which is related to trad-
ing strategies as well as the use of algorithmic trading. If the inclusion of
multi-level order book data did not signiﬁcantly improve the empirical per-
formance of a prediction model, then it would be suﬃcient to rely on Level-I
data only, which would validate the methodological and data choices of these
papers relying on Level-I data.
Second, there is a branch of literature that uses multi-level order-book
data to analyze the use of the limit versus market orders [15, 16], order
book liquidity [17, 2, 3], market impact [18, 19], and price formation [20].
Recently, the use of complete order-book data has become popular in pre-
dicting order-book dynamics or price movements with the advanced machine
learning techniques, particularly in the quantitative ﬁnance and machine
learning literature (see, for example [21, 22, 23, 24, 25, 26, 27, 28] and refer-
ences therein). Moreover, recently Deep Reinforecement Learning has used
for high-frequency trading with LOB data [29]. Even if modern deep-learning
techniques allow a huge number of input variables (as long as the size of the
data is large), the use of irrelevant input variables is not only unnecessary
but can reduce the robustness of the models. Irrelevant data, which poten-
tially acts as a source of noise, can adversely aﬀect the accuracy of the model
that captures the underlying relationship between the variables. Moreover,
the extra computational burden introduced by additional information can
be signiﬁcant, which renders the analysis impractical for high thoughput ap-
plications. For these reason, it is important to know if the use of complete
Level-II order book data does maximize the predictive power of machine
learning models. If this is the case, then one could argue that it is better to
use data-driven machine learning techniques with all the available data than
parsimonious and tractable models that rely on the top level quotes only.
The question about the importance of the order book data beyond the
best level has been barely addressed in the literature, indeed. While there
are existing papers that have considered the question about informational
contents of LOBs, such as [30, 31], they rely on such simple linear mod-
els. In reality, the way how investors and algorithms use order-book data
for their trading decisions can be very complicated and vary over diﬀerent
circumstances. If one estimates a speciﬁc model assuming pre-speciﬁed (lin-
ear) relations between the explanatory and dependent variables, the drawn
3
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 4

conclusions can be misleading because of the possibility of model misspeciﬁ-
cation. More generally, in variable selection (feature selection), it is crucial
not to restrict the model to be linear, and in fact, to have any restriction that
can incorrectly to falsify the importance of a variable. For that reason, the
assumption of linearity is not acceptable when it comes to truly non-linear
systems, what stock markets deﬁnitely represent [32].
In this paper, instead of relying on the linear model paradigm, we aim
to address the question about the informativeness of the order book data
beyond the best levels by allowing the involved variables to interact in a
complex, nonlinear manner. To our best knowledge, this is the ﬁrst paper
that addresses the research question about how informative the order-book
is beyond the best levels by a data-driven approach in which the necessity
of each explanatory variable and their complex, nonlinear interaction (which
also encapsulates the linear case) are jointly estimated.
Particularly, we
employ state-of-the-arts modeling tools from the machine learning commu-
nity in our method, namely deep neural networks. It has been shown that
feed-forward neural networks with bounded activation functions or rectiﬁed
linear units are universal function approximators [33]. Simply put, a univer-
sal function approximator is guaranteed to have the capacity to approximate
arbitrarily well any function that generates the observed data. Thus, from
the theoretical perspective, deep neural networks are suitable tools to model
the underlying complex relationship between the limit order information and
any dependent targets since the only assumption required is the existence of
such a relationship. Besides, the most prominent empirical successes over the
last few years in ﬁnancial applications such as stock prediction [34, 35, 36, 37],
portfolio selection and optimization [38, 39], factor and risk analysis [40, 41],
derivatives hedging [42, 43] and so on, are mainly driven by deep neural
network solutions.
In order to discover the importance of diﬀerent explanatory variables
with respect to the dependent variables of interest, our work adapts and
integrates well-studied automatic feature selection methods into the training
procedure of deep neural networks. By doing so, we are able to gauge the
the contribution of explanatory variables to the ﬁnal forecasting decision
in a complete data-driven manner. As the name implied, feature selection
[44] aims to select the most relevant subset of the explanatory variables to
achieve similar or even better learning performance than using all explanatory
variables. By developing feature selection methods, not only are we able to
identify the most relevant information from the LOB but also to reduce
4
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 5

the computational inference cost when deploying the estimated models in
production.
There are three main categories of feature selection methods: ﬁlter-based
methods, embedded methods, and wrapper methods. Filter-based methods
perform selection based on certain criteria measured on the observed data,
prior to the estimation of the learning model. Popular criteria used in ﬁlter-
based methods include reliefF, F-statistic, mRMR or information gain [44].
Because the selection step is decoupled from the model estimation step, the
result obtained from a ﬁlter-based method is independent of the learning
model being used. On the contrary, the feature selection scheme in wrapper-
based and embedded methods is intertwined with the learning model, leading
to results that are dependent on the models being used. In other words,
we might obtain two diﬀerent subsets of features when applying the same
selection scheme to two diﬀerent learning models.
The machine learning literature mainly concerns about learning models
and the ﬁnal performances. At the same time, we are not aware of any prior
work that investigates the consistency among the solutions obtained from a
feature selection method applied to diﬀerent backbone estimation models or
even across the solutions obtained from diﬀerent feature selection methods.
Because our main focus is on the informational content of the LOB, inter-
pretations of the outcome are only valid when there is a consensus among
diﬀerent feature selection methods using diﬀerent backbone estimation mod-
els, estimated with observed data from diﬀerent markets. For this reason,
in our work, we adapt and integrate two popular feature selection meth-
ods, namely Backward Elimination (BE) [45, 46] and Binary Particle Swarm
Optimization (BPSO) [47], into two state-of-the-arts neural network models
that are speciﬁcally designed for LOBs, namely Deep Convolutional Neural
Network for LOB
(DeepLOB) [25] and Temporal Attention Bilinear Layer
Network (TABL) [22].
The idea of BE is that it gradually identiﬁes and removes the most ir-
relevant features, which, in the context of this paper, are the LOB levels.
Particularly, we implemented the algorithm in a way that a given LOB level
is removed from the both side of the book.1 This elimination process contin-
ues until there was only one level remaining. By that way, we can analyze
how likely a given LOB level remains ’alive’ once the algorithm has elimi-
1In our notation, Level n denotes the nth level on the both sides of the book.
5
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 6

nated the others. Because the algorithm removes LOB levels in a way that
the performance degradation is minimal, the remaining LOB level can be
thought to be the most informative one. On the other hand, with BPSO,
an optimal set of input variables is selected such that the ﬁtness function
of the neural network model is maximized. This allows us to analyze the
appearance of each LOB level in the selected subsets. One can argue that
the more often a given LOB level appears in the optimal set of the levels, the
more informative the level is. Therefore, both of the approaches show the
importance of diﬀerent LOB levels in the price movement prediction, but in
diﬀerent ways: BE by elimination of the least important levels and BPSO by
optimal selection of the sets of the most important levels.
Our empirical analysis was conducted using data coming from two diﬀer-
ent markets (US and Nordic), which diﬀer in terms the number of order book
messages in a given time interval (and thus order book liquidity). Moreover,
we vary the length of the prediction horizon from 10 to 30 LOB events. With
extensive experimentation, the we ﬁnd out that there is indeed a consensus
between diﬀerent combinations of (i) neural network models, (ii) feature dis-
covery methods, and (iii) markets: the top level of the LOBs provides the
most important source of information in predicting the future movements of
the mid-price. In addition, there is also a consensus in the ranking between
the top three levels of the order-book in terms of importance: the top three
levels are also ranked in the same order as their execution priority in the
order-book. Our analysis also points out that orders beyond the best level
indeed provide complementary information in the prediction of mid-price
movements, accounting for 2 to 3 percents of performance improvements
compared to the cases where only the most important quotes are used.
To summarize, our paper is organized as follows: Section 2 describes
the design and optimization of two state-of-the-arts neural networks that
have been proposed for LOBs. In Section 3, we describe our methodology for
analyzing the informational content of the LOB. Section 4 provides empirical
results and our discussion on the ﬁndings. Finally, concluding remarks are
drawn in Section 5.
2. Neural Networks for Limit Order Book
Neural networks are a parametric family of mathematical functions that
are composed in a hierarchical manner. The abstraction in neural networks is
often expressed via layers of processing units. As a high level view, a neural
6
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 7

network consists of the input layer, one or multiple intermediate layers, also
referred to as hidden layers, and the output layer. The input layer receives the
input data, which can be in the form of a vector or a tensor. The intermediate
layers sequentially transform the input data and give the results in the output
layer. Each layer in a neural network (except the input layer) represents a
mathematical function, which is often parameterized by a set of parameters,
also referred to as weights. In a simple feed-forward construction, the k-th
layer processes the output of the previous layer, i.e., the (k −1)-th layer. Let
us denote the mathematical function expressed by the k-th layer as Gk and
its parameters as Θk. The transformation of the k-th layer is described by
xk = Gk(Θk, xk−1),
(1)
where xk denotes the output of the k-th layer. Depending on the types of
neurons forming the neural network, Θk can be a matrix as in fully-connected
layers or Θk can be a tensor as in convolutional layers. While the form of Gk
is often determined by human experts via domain knowledge and experimen-
tation, most common layer designs such as the fully-connected layer and the
convolution layer typically involve some linear transformations of the input
via matrix multiplication followed by element-wise nonlinear activation. In
addition, a single choice of nonlinear activation function, such as the Recti-
ﬁed Linear Unit (ReLU), is often applied to all layers to narrow down the
possible choices when designing a neural network solution, except for the out-
put layer, which has an activation function depending on the given task. For
example, the soft-max function, which transforms an un-normalized vector
to a vector having positive elements summing up to one, thus, representing
the class probability prediction, is a de-facto choice for classiﬁcation tasks.
Here we should note that in many state-of-the-arts neural network for-
mulations, the connectivity patterns can be more complicated than the one
described in Eq. (1) for a simple feed-forward construction. That is, a layer
can not only take the output of its immediate preceding layer, but also the
output of other preceding layers. After deﬁning the architecture of a neural
network model, i.e., the types of the input data, the number of layers, the
type of transformation of each layer and their connectivity pattern, its pa-
rameters are estimated by optimizing a learning objective (measured by a loss
function) using the set of (training) data. That is, the network’s parameters
7
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 8

(Θ = {Θ1, . . . , ΘK}) are determined by solving
argmin
Θ
N
X
i=1
L(yi, ˜yi),
(2)
where L denotes the loss function, yi denotes the true label of the i-th sample
and ˜yi denotes the corresponding prediction by the neural network.
Since the objective in Eq. (2) is highly nonlinear for neural networks with
multiple layers, a variant of the gradient descent algorithm is often used to
ﬁnd Θ.
As the name implies, gradient descent is an iterative algorithm
that updates the parameters of a function by repeatedly moving the current
parameters’ values along the steepest slope (the gradient). In its simplistic
form, a gradient descent algorithm has the following update rule:
Θ(t + 1) = Θ(t) −α ∂L
∂Θ(t),
(3)
where Θ(t) denotes the value of Θ at step t, and α is a scalar for controlling
the amount of the update. The value of α can be sensitive to the conver-
gence of the gradient descent algorithm since a large value can easily lead to
divergence while a small value makes it slow to converge. There have been
many extensions to the basic gradient descent algorithm described in Eq.
(3). Among those, SGD with momentum [48] and ADAM [49] are the most
popular ones in the neural network community.
In the following, we will describe two state-of-the-arts neural network
formulations for the mid-price movement prediction task, namely TABL and
DeepLOB. Both networks take as input the most recent states of the order-
book, which include the top ten quotes (price and volume) from the bid
and the ask sides.
For a given stock at time t, let us denote the top-k
bid and ask prices as pb
k(t) and pa
k(t), and volumes as vb
k(t) and va
k(t). The
information of the top ten levels at each time instance is thus represented
by a 40-dimensional vector. Since TABL and DeepLOB take advantage of both
the current and past order-book information, the input data is a multivariate
time-series having dimension of 40 × T with T being a hyperparameter that
determines the length of past information.
2.1. Temporal Attention Augmented Bilinear Layer Networks
Temporal Attention augmented Bilinear Layer network (TABL) was for-
mulated by [22] to speciﬁcally work with ﬁnancial multivariate time-series.
8
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 9

There are two main ideas in the design of TABL networks: (i) the utilization
of bilinear layers to capture linear dependency along the feature and tempo-
ral dimension of the input and intermediate series, and (ii) the incorporation
of an attention mechanism to automatically identify and focus on important
temporal instances within a series.
A bilinear layer (BL) takes as input a matrix X ∈RD×T and produces a
matrix Y ∈RD′×T ′ via transformation
Y = φ(W1XW2 + B),
(4)
where W1 ∈RD′×D, W2 ∈RT×T ′, and B ∈RD′×T ′ denote the the parame-
ters associated with the bilinear layer. φ denotes an element-wise activation
function such as ReLU or sigmoid. In short, a BL layer linearly transforms
the input time-series X along the ﬁrst (the feature) and second (the tempo-
ral) dimension separately by using W1 and W2, then shifts the intermediate
result with the bias term B before the nonlinear thresholding operation.
The beneﬁt of using a bilinear transformation for multivariate time-series
is two-fold. The ﬁrst advantage is the reduction of parameters that need to
be estimated, compared to a linear transformation. This is because a linear
mapping, which transforms a vector from D·T to D′·T ′ dimensions, requires
the estimation of a transformation matrix having D·T ·D′·T ′ elements while
the bilinear transformation in Eq. (4) using W1 and W2 only requires the es-
timation of D·D′+T ·T ′ elements. The second advantage is the preservation
of semantic structure within input time-series. In Eq. (4) since W1 linearly
combines the rows of X and W2 linearly combines the columns of X, a BL
layer eﬀectively captures the linear dependency between diﬀerent univariate
series within X via W1, and the linear dependency between diﬀerent tem-
poral observations via W2 (note that the second dimension of X represents
the temporal dimension). On the hand, using a linear mapping requires the
vectorization of X, thus breaking the structural information inherent in the
input series.
TABL architecture follows a simple feed-forward connectivity pattern in
which one or a few BL layers are stacked one after another in a sequential
manner to form the hidden layers. The output layer of a TABL network is
TABL layer, which extends the standard BL layer with an attention mecha-
nism on the temporal dimension. Given the same input and output notation
as in a BL layer, the transformation performed by a TABL layer consists of
ﬁve steps:
9
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 10

(i) The input series X is ﬁrst linearly transformed along the ﬁrst dimen-
sion, i.e., the feature dimension, using W1:
¯X = W1X.
(5)
(ii) The relative importance between diﬀerent temporal instances (columns)
in the intermediate feature matrix ¯X is computed via a specially de-
signed matrix W,
E = ¯XW,
(6)
where W ∈RT×T is a parameter matrix that has constant values (1/T)
on its diagonal. Other elements of W are estimated during optimization
to determine the pair-wise relevance scores between columns of ¯X.
(iii) The relevance score at each position [i, j] of E is then normalized over
the second dimension (the temporal dimension) using the soft-max
function to produce an attention mask A ∈RD′×T, with the element
at position [i, j] computed as
A[i, j] =
exp(E[i, j])
PT
k=1 exp(E[i, k]))
.
(7)
Since E is normalized along the second dimension, elements within each
row of the attention mask A sums up to one. In this way, the attention
mask encodes the relative importance of a temporal slice (a column)
with respect to others.
(iv) The attention matrix A is then used to mask out irrelevant elements
in the intermediate feature ¯X. This is done via a soft attention mech-
anism, which performs convex combination of ¯X and its masked-out
version:
˜X = λ( ¯X ⊙A) + (1 −λ) ¯X.
(8)
Here λ is a scalar, which is constrained to have a value between [0, 1]
and is also estimated during the optimization procedure.
(v) In the ﬁnal computation step, the attended feature matrix ˜X is linearly
transformed in the second dimension with W2, and shifted by the bias
term B, before going through the activation function φ to produce the
output of the layer:
Y = φ

˜XW2 + B

(9)
10
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 11

Compared with the standard BL layer, the TABL layer requires an ad-
ditional estimation of W and λ for the computation of the attention mech-
anism. Since both BL and TABL layers are diﬀerentiable, gradient descent
updates can be easily computed. In the original paper, the authors used
ADAM [49], a stochastic gradient descent optimizer that performs adaptive
estimate of the update size using lower-order moments. In this work, we also
use ADAM with the same conﬁguration as in [22] to optimize TABL networks.
Regarding the architecture, [22] evaluated three diﬀerent TABL networks with
the number of hidden layers ranging from zero to two. Despite being shal-
lower and having far fewer parameters, a TABL network with two hidden layers
produces superior prediction performance compared to existing neural net-
work solutions, both shallow and deep nets. For this reason, we use the same
two-hidden-layer network topology proposed by [22]: this network takes an
input series of size 40 × 10, containing the quote data of the ten most recent
order-book states; two hidden layers are BL layers, which have the output
dimensions of 60 × 10 and 120 × 5, respectively; the output layer is a TABL
layer, which has the output dimension of 3 × 1, encoding the probability of
three types of future mid-price movements.
2.2. Deep Convolutional Neural Networks for Limit Order Books
Beside the TABL network from [22], the deep neural network design called
DeepLOB proposed by [25] has also demonstrated excellent performances in
predicting mid-price movements using LOB information.
Diﬀerent from
TABL, DeepLOB is a deep network with several convolution layers.
In ad-
dition, DeepLOB also stacks a recurrent layer after the convolution layers and
before the output layer, which is a fully-connected layer that performs linear
mapping and soft-max activation to produce a probability prediction vector.
As the name implies, a convolution layer applies convolutional transfor-
mations of the input via a set of convolution ﬁlters. Given an input matrix
I ∈RH×W, a convolution ﬁlter w ∈Rh×w, and a stride length of s1 × s2, the
result of convolving X with w using the given stride length is a matrix Y,
with the element at position [p, q] computed as
Y[p, q] =
h
X
i=1
w
X
j=1
w[i, j] · I[i + (p −1) · s1, j + (q −1) · s2],
(10)
where Y has dimensions of H′ × W ′, with H′ = ⌊(H −h)/s1 + 1⌋and W ′ =
⌊(W −w)/s2 + 1⌋.
11
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 12

Figure 1: DeepLOB architecture from [25]
In order to extract low level features from the input time-series, DeepLOB
utilizes a series of nine convolution layers with diﬀerent conﬁgurations, which
are depicted in Figure 1. The output of the last convolution layer is fed to
a computation module called Inception. The design of the Inception mod-
ule in DeepLOB was inspired from the work of [50], in which the authors
proposed a very eﬃcient neural network architecture, called Inception, for
solving computer vision problems. The key idea behind the Inception design
is the utilization of convolution layers with diﬀerent ﬁlter sizes in parallel
to extract multi-scale features. That is, instead of applying one convolution
layer after the output of another, the Inception module contains three par-
allel branches of convolution layers that are applied to the same input, and
concatenates the output of all branches to form the output of the module.
The Inception design is illustrated in Figure 1.
After extracting multi-scale features using the Inception module, DeepLOB
further processes multi-scale features using a Long-Short-Term-Memory (LSTM)
layer [51]. LSTM is a type of recurrent layer, which was designed speciﬁcally
to extract ﬁxed-length representation from variable-length sequences such as
those encountered in natural language processing problems. The ability to
12
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 13

transform variable-length sequences to ﬁxed-length sequences comes from the
fact that a recurrent layer applies recursive computation to each temporal
slice of the input sequence using both the current temporal slice and the out-
puts of the previous computation as inputs. Mathematically, let us denote
the input sequence as X ∈RD×T with the second dimension representing
the temporal dimension. In addition, xt ∈RD denotes the t-th temporal
slice (column) of X. The recursive computation of a recurrent layer can be
described by
ht, ot = F(ht−1, xt), ∀t = 1, . . . , T,
(11)
where F denotes some function that takes two vectors, namely ht−1 and xt
as inputs, and also returns two vectors ht and ot as outputs.
In recurrent network terminology, ht ∈RDh is referred to as the hidden
state at time t and ot ∈RDo is known as the cell state or intermediate output
at time t. The last cell state, i.e., oT is also the output of the recurrent layer.
Here Dh and Do are the dimensions of the hidden states and the outputs,
which are typically set similar, and often referred to as the number of units in
a recurrent layer. The speciﬁc transformations in F depend on the design of
the recurrent layer. There are many diﬀerent recurrent layer designs, among
which LSTM and GRU [52] are the most widely used. The output layer of
DeepLOB performs a linear transformation on the output of the LSTM layer,
then soft-max activation to generate a probability prediction vector.
3. Informational Content Discovery via Feature Selection
As we have mentioned in Introduction, our objective is to study the in-
formational content of the quote data across multiple levels by analyzing
the predictive power of each level of quotes. For this purpose, we adopted
two feature selection methods to incorporate into the TABL and DeepLOB net-
works. The general idea of feature selection is to identify a subset of input
variables that can eﬀectively capture the most relevant information from the
observed data for a given learning task. Since the number of input variables
is ﬁnite, this is essential a search problem in a discrete space. Depending
on the nature of the data and the main purpose behind having such a sub-
set of features, the criterion for the search problem might be constructed in
diﬀerent ways. For example, one might be interested in ﬁnding the smallest
subset of features to reduce future computational complexity when working
with the given problem. Others might be merely interested in the relevance
of each feature and their relative ranking in terms of relevance.
13
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 14

Typically, feature selection is formulated as ﬁnding the subset of input
features from which the estimated learning model achieves the best perfor-
mance. A global solution for this criterion requires estimating at least 2D
models, corresponding to all 2D subsets of features, with D denoting the
number of input variables. For the class of models that are estimated with
some degree of stochasticity, one would need to estimate far more than 2D
models to ensure statistical signiﬁcance of the conclusion. Even for a model
with closed-form solution such as linear models, a greedy solution becomes
exponentially slow as the number of input variables increases. For this rea-
son, the feature selection criteria might be formulated diﬀerently [44], such as
ﬁnding the subset of a given size to achieve the best performance or ﬁnding
a subset of features that achieve similar or better performance compared to
the baseline model that is estimated using the full set of features.
In order to discover the predictive power of diﬀerent levels in the order-
book, we selected two feature selection methods, namely Backward Elim-
ination (BE) [45, 46] and Binary Particle Swam Optimization (BPSO) [47]
with diﬀerent search trajectories. While BE produces a candidate subset of
a given size that may achieve the best performance, the search trajectory of
BPSO can travel the entire search space and converges at a subset of any size,
which is not predeﬁned. Since our selected classiﬁers (TABL and DeepLOB)
are estimated using stochastic gradient descent, it is possible that diﬀerent
runs of either BE or BPSO can generate diﬀerent subsets. Thus, to analyse
the informational content of our inputs, we look for any consensus among
the solutions provided by both methods applied to the selected classiﬁers,
using two diﬀerent markets’ data. Our approach to look for such consensus
is elaborated in Section 4.
The idea of BE is very simple: the algorithm starts with the set of all
input features, then gradually identiﬁes and removes the most irrelevant fea-
ture, one at a time, until there is only a single level left or the learning
performance falls below a pre-deﬁned threshold. The majority of existing lit-
erature that uses BE employed simple linear models, thus F-test or t-test are
popular criteria to identify the irrelevant feature at each elimination step.
For the approach that utilizes a linear regressor, we only need to perform
one estimation of the model’s parameters and use them to identify which
feature to remove. In our case where highly nonlinear neural networks are
employed, there is no straight-forward method to quantify the importance of
a given input variable based on the optimized weights. For this reason, in
order to determine data from which order-book level should be discarded in
14
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 15

an elimination round having K remaining levels, we train K diﬀerent neural
network instances, each of which corresponds to leaving out the quotes of a
potentially irrelevant level. The irrelevant level is then identiﬁed with the
network instance that achieves the lowest prediction performance. In our
experiments, we performed the elimination routine until there was only one
level left. Here we should point out that since these K neural network in-
stances are independent of each other, they can be optimized in parallel in
practice.
One might be concerned with our selection of the BE algorithm since
in some prior research employing BE to study the explanatory or predictive
power of input variables in modeling tasks, the algorithm exhibited certain
degrees of instability with respect to small pertubation of data or noise, which
was considered as having no eﬀect on the dependent variable [53, 54, 55].
Here we should note that the nature of our problem and data is diﬀerent
from those scenarios for two reasons: (i) the data coming from electronic
LOBs can be considered as rather clean in the sense that it is expected
to contain very little to no noise such as those coming from an imperfect
measurement/collection process in other application areas. This is especially
true from a technical point of view for modern, completely electronic systems
in big exchanges, which are thoroughly designed, tested and equipped with
backups. Thus, the simulation of noise by introducing small pertubation to
the data does not represent a real scenario. (ii) Small pertubation of the
quote price cannot be considered as insigniﬁcant or having no eﬀect to the
dependent variables.
While BE resembles more of a series of heuristic tests to identify important
features, BPSO is a generic, well-studied meta-heuristic optimizer for binary
variables, rather than a dedicated feature selection method. That is, BPSO
optimizes a binary vector such that a ﬁtness function computed on it is
maximized. In order to use BPSO to perform feature selection, one would
deﬁne a binary mask vector having the same dimension as the number of
features, which represents the selection of a particular subset of features.
The values of this binary mask vector are randomly initialized and iteratively
updated until convergence. BPSO applied in such manner considers each input
variable independently while in our case, we want to form subset of the
quote values that correspond to speciﬁc order-book levels. This necessitates
modiﬁcations as how BPSO is formulated for LOBs.
Let us recall from Section 2 that our input variables are the most recent
order-book events, which include the top ten bid prices (pb
1(t), . . . , pb
10(t))
15
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 16

and volumes (vb
1(t), . . . , vb
10(t)), and top ten ask prices (pa
1(t), . . . , pa
10(t)) and
volumes (va
1(t), . . . , va
10(t)), with t indicating the time index. These variables
are organized in the following matrix to reﬂect a multivariate time-series
nature of the order-book events:
Xt =


pa
1(t −T −1)
. . .
pa
1(t)
va
1(t −T −1)
. . .
va
1(t)
pb
1(t −T −1)
. . .
pb
1(t)
vb
1(t −T −1)
. . .
vb
1(t)
...
. . .
...
pa
10(t −T −1)
. . .
pa
10(t)
va
10(t −T −1)
. . .
va
10(t)
pb
10(t −T −1)
. . .
pb
10(t)
vb
10(t −T −1)
. . .
vb
10(t)


∈R40×T,
(12)
where T denotes the number of the most recent order-book events that a
neural network predictor uses as inputs. In our experiments, we used ten
most recent order events, i.e., T = 10. In addition, each sample Xt comes
with a label yt that indicates the future mid-price movement.
Let us denote by s ∈R10 the binary vector that indicates a particular
subset of ten levels, with s[i] = 1 indicating the inclusion of level i and
s[i] = 0 otherwise. In addition, we also denote by M(s) ∈R40×T a binary
matrix that is formed from s as
M(s)[i, j] = s[k],
∀j = 1, . . . , T
(13)
k = ⌊(i −1)/4⌋+ 1,
∀i = 1, . . . , 40.
(14)
That is, M(s) denotes the binary matrix that can be used to mask out all the
values in Xt that belongs to unchosen levels expressed in s. Here we should
note that M(s) can also be deﬁned via a matrix multiplication operation as
M(s) = I1sI2 with I1 ∈R40×10 and I2 ∈R1×T being two constant matrices
with appropriate ones and zeros. Now the optimization objective of BPSO
can be stated as
argmax
s
F1
 {yt, N(Xt ⊙M(s))|t = 1, . . . }

,
(15)
where N denotes the function representing the neural network giving pre-
dictions and Θ is its parameters. F1 denotes the function that computes
average F1 measure in a classiﬁcation problem given the set of true labels
16
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 17

and predicted labels. The element-wise multiplication operation at the end
of Eq. (15) is denoted as ⊙.
Here we should note that the F1 measure is used in our analysis because
it reﬂects the trade-oﬀbetween precision and recall, which is especially im-
portant for problems with skewed distributions as observed in our data.
The idea in BPSO is that we may discover an optimal solution faster by
using a list of candidate solutions, which are also called particles. Let us
denote the k-th particle in the swarm as sk and the size of the swarm as K.
The swarm of particles moves together in the search space to ﬁnd the optimal
solution, thus, each of them has a velocity, which is denoted as vk ∈R10. At
each movement, a particle moves to a new position with its velocity, which
is computed based on its past experience and also the experiences of other
particles. Let us denote the best position that the k-th particle has visited
as s∗
k, and the best position that the entire swarm has visited as s∗. The k-th
particle adjusts its velocity with the following rule:
v(i+1)
k
= w ⊙v(i)
k + c1 · r1 · (s∗
k −s(i)
k ) + c2 · r2 · (s∗−s(i)
k ),
(16)
where i represents the iteration index in the optimization routine. w is the
inertia term, which is a hyperparameter of the method to control the impact
of the old velocity on the new one. The value of w is often reduced gradually
as the swarm progresses. c1 ∈R and c2 ∈R are acceleration constants and
r1 and r2 are randomly sampled scalars from the uniform distribution [0, 1].
To control the maximum velocity of a particle at each iteration, the velocity
is limited within a range [−vmax, vmax].
Since a particle can only move in a discrete space of 0 and 1, the velocity
is used to determine the probability that a particle will move to position 0 or
1. With the new velocity v(i+1)
k
, the k-th particle updates its position using
the following rule:
s(i+1)
k
[j] =



1
if r3 < sigmoid

v(i+1)
k
[j]

0
else,
(17)
where s(i+1)
k
[j] and v(i+1)
k
[j] denote the j-th element in s(i+1)
k
and v(i+1)
k
, re-
spectively. r3 is a randomly sampled scalars from the uniform distribution
[0, 1].
Given the new positions of the swarm, BPSO evaluates the ﬁtness of each
particle by optimizing the neural network’s parameters, i.e., for the k-th
17
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 18

particle, we need to solve the following optimization problem with stochastic
gradient descent:
Θ∗= argmin
Θ
X
t
L

yt, N

Xt ⊙M

s(i)
k

,
(18)
where Θ is the parameters of the neural network N, and Θ∗denotes its
optimal values obtained from stochastic gradient descent.
L denotes the
cross-entropy loss function.
The ﬁtness for the k-th particle at the i-t iteration is deﬁned as the F1
score obtained at Θ∗. Based on new ﬁtness values for all particles, BPSO
checks and updates s∗
k and s∗if new best solutions emerge. The algorithm
repeats the aforementioned procedure for a pre-deﬁned number of iterations.
4. Empirical Results
4.1. Data Collection and Processing
We analysed the informational content of the LOB data coming from two
diﬀerent markets: the Nordic market and the US market. For the Nordic mar-
ket, we collected orders from ﬁve companies that are listed on Helsinki Stock
Exchange, namely Kesko, Outokumpu, Rautaruukki, Sampo and Wartsila,
and for the US market, we used orders coming from Amazon and Google. All
of our data is procured from TotalView-ITCH feed with the resolution in mil-
liseconds, covering a period of ten working days from the 22nd of September
2015 to the 5th of October 2015. Data from the message books was processed
to form the LOBs of depth ten for both bid and ask sides.
For the Helsinki Stock Exchange, the trading period goes from 10:00 to
18:25 (local time, UTC/GMT+2) while for the Nasdaq US Stock Market,
the trading hour spans from 09:30 to 16:00 (EST). For Nordic stocks, we
excluded the auction period and only considered data between 10:30 and
18:00 following the previous convention used for this data [2, 3]. For the
US stocks, we considered all trading hours. This resulted in approximately
13 millions events for the US dataset and 4 millions events for the Nordic
dataset, with the duration between consecutive events unevenly distributed,
ranging from milliseconds to minutes.
The data of the ﬁrst seven days was used to to train and validate the
models and the data covering the last three days was used as the held-out
test set. For each market, we aggregated the data from all stocks and used
18
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 19

them to train stock-agnostic models to predict the future movement of the
mid-price after H = {10, 20, 50} order events. The future movements of the
mid-price belongs to one of the three categories: up, down, and stationary.
Since ﬁnancial data often exhibits stochasticity, simply deriving labels for
mid-price movements by comparing the current mid-price with the one in
the future will lead to a very noisy label set. To reduce this eﬀect, previous
practices have employed price smoothing for the labeling process [56, 25],
and we followed the same procedure that smoothes the mid-price using both
future and past values as follows:
yt ≡





up,
lt > α
stationary,
−α ≤lt ≤α
down,
lt < −α,
(19)
where α = 0.00001 is a constant to deﬁne the smallest margin change to be
considered as a movement. The quantity lt is deﬁned as
lt = m+(t) −m−(t)
m−(t)
(20)
m−(t) = 1
H
H
X
i=0
p(t −i)
(21)
m+(t) = 1
H
H
X
i=1
p(t + i).
(22)
For machine learning models in general and for neural networks in par-
ticular, data normalization can heavily aﬀect the ﬁnal performance.
For
high-frequency trading data, prior works [28, 57] have shown that a suitable
data normalization method can signiﬁcantly boost the performance of the
same model. In our case, since we aimed to train stock-agnostic model using
their order information, the price range and the volume can be signiﬁcantly
diﬀerent for diﬀerent stocks, thus, requiring attention on data normalization
scheme. Z-score normalization, i.e., subtracting the mean from the data and
dividing the values with standard deviation, is the most common scheme.
For a large amount of time-series data spanning several days, it is also a
common practice to perform Z-score normalization with statistics coming
from the previous day, rather than from the whole training set spanning sev-
eral days [25]. There are also other advanced data normalization methods
19
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 20

that estimate the normalization parameters in conjuction with a learning
model’s parameters [58, 59, 28, 57]. Based on the results of our preliminary
experiments with Z-score normalization and two adaptive methods [28, 57],
we adopted the bilinear normalization technique proposed in [57] for our
experiments since this method exhibits strong performance over the others.
As a ﬁnal note on data normalization procedure, depending on the data
normalization methods, the normalized data might inherently contain infor-
mation of all features, thus, can interfere with the judgement of relevant
subset of features because the chosen subset of normalized features already
contains some information, which is obtained from the discarded features.
For this reason, instead of normalizing the whole data once and proceed with
feature selection algorithms, we only performed data normalization after the
subset selection step . For example, in BE when evaluating K diﬀerent neural
networks using K diﬀerent subsets of the remaining levels in an elimination
round, the train sets corresponding to K subsets are normalized indepen-
dently, using only statistics of the corresponding subset.
4.2. Hyperparameters and Optimization Details
Regarding the optimization of TABL and DeepLOB, we used ADAM op-
timizer [49] with β1 = 0.9 and β2 = 0.999 for both networks in all experi-
ments. To optimize a neural network instance, we randomly initialized the
parameters with the initialization technique proposed in [60] and updated
the parameters for 50 epochs with the initial learning rate of 0.001, which
was reduced by a factor of 10 at epoch 6 and 46. The batch size for all ex-
periments was set to 128 and weight decay regularization coeﬃcient was set
to 0.00005. To counter the eﬀect of imbalanced class observed in the mid-
price movement labels, when training the networks, we adopted the same
weighted cross-entropy loss function proposed in [22], which basically multi-
plies a weight scalar, which is inversely proportional with the size of a class,
to the loss terms associated with that class.
Regarding BPSO, we used a swarm of 15 particles for all experiments. The
inertia term w in Eq. (16) was computed using an annealing schedule, with
the value of w at the i-th iteration computed as w = 2 −2 · (i/I)1/π2 with
I = 20 being the maximum number of iterations. In Eq. (16), c1 = c2 = 1.5,
and the velocity was limited within the range [−6, 6]. The selected values for
hyperparameters of BPSO are conventional choices adopted in literature.
Given two types of prediction networks (TABL and DeepLOB), two feature
selection methods (BE and BPSO), two datasets (US and Nordic), and three
20
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 21

prediction horizons (H = {10, 20, 50} events), our total experiment set con-
sists of 24 diﬀerent conﬁgurations. For each conﬁguration, we repeated the
experiment 20 times and reported the mean and standard deviation values
for F1 score measured on the held-out test set.
4.3. Are the top quotes the most important predictors?
Based on the experiment results collected, the ﬁrst question that we
sought an answer is whether the assumption about the top quotes being
the most informative information of the LOBs still holds even when using
highly nonlinear models for the modeling task. Let us recall from Section 3
that as the elimination goes in BE, we sequentially obtain the most impor-
tant subsets of LOB levels of decreasing sizes, and also the associated test
performance that can be achieved from the selected subset. This process was
conducted until there was only one level remaining. If we look into the per-
centage that a given level appeared as the only remaining level after running
BE, out of 20 experiment repetitions for each conﬁguration, we obtained the
following statistics for ten levels in Table 1.
Table 1: The percentage that a given level (on the both sides of the book) appeared as
the only remaining level when using BE. The results are provided for US and Nordic data
sets and for three diﬀerent prediction horizons, H = 10, 20, 50. Moreover, two models for
the price prediction with the LOB data are used, DeepLOB [25] and DeepLOB [22].
US Data
Nordic Data
DeepLOB
TABL
DeepLOB
TABL
H
10
20
50
10
20
50
10
20
50
10
20
50
Level 1
100%
100%
100%
100%
100%
100%
95%
90%
95%
65%
95%
100%
Level 2
0%
0%
0%
0%
0%
0%
0%
5%
0%
25%
5%
0%
Level 3
0%
0%
0%
0%
0%
0%
0%
0%
0%
5%
0%
0%
Level 4
0%
0%
0%
0%
0%
0%
0%
5%
5%
5%
0%
0%
Level 5
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
Level 6
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
Level 7
0%
0%
0%
0%
0%
0%
5%
0%
0%
0%
0%
0%
Level 8
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
Level 9
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
Level 10
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
As it is obvious from Table 1, the ﬁrst LOB level consistently appeared
with high percentages as the last level remaining during the elimination in
BE across diﬀerent conﬁgurations. Most notably, for the US data, the results
21
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 22

of all conﬁgurations unanimously selected level 1 as the most predictive level.
The results for Nordic data also indicated the same phenomenon with level
1 being selected at least 18 out of 20 times (90%) for all conﬁgurations, with
the only exception when using TABL to predict at H = 10.
We will now look into the results obtained from BPSO from the same
aspect. Let us recall from Section 3 that the subset of levels selected by
BPSO can be of any cardinality. The solution given by BPSO at the end of
the optimization process is the best solution among all the positions that
the swarm visited during its course. To seek for potential consensus between
BPSO and BE, we computed the percentage that a given level appeared in the
ﬁnal solution given by BPSO, out of 20 experiment runs for each conﬁguration.
The statistics are shown in Table 2.
Table 2: The percentage that a given level (on the both sides of the book) appeared in
the ﬁnal solution of BPSO. The results are provided for US and Nordic data sets and for
three diﬀerent prediction horizons, H = 10, 20, 50. Moreover, two models for the price
prediction with the LOB data are used, DeepLOB [25] and DeepLOB [22].
US Data
Nordic Data
DeepLOB
TABL
DeepLOB
TABL
H
10
20
50
10
20
50
10
20
50
10
20
50
Level 1
100%
100%
60%
100%
100%
80%
60%
50%
50%
50%
90%
70%
Level 2
20%
10%
30%
0%
10%
10%
30%
20%
20%
20%
10%
20%
Level 3
0%
10%
10%
10%
0%
20%
10%
30%
10%
30%
0%
0%
Level 4
0%
0%
0%
0%
10%
0%
0%
0%
10%
0%
0%
0%
Level 5
0%
0%
0%
10%
10%
0%
0%
10%
10%
0%
10%
0%
Level 6
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
0%
10%
Level 7
0%
0%
0%
10%
0%
0%
0%
0%
0%
0%
0%
0%
Level 8
0%
0%
10%
0%
0%
0%
0%
0%
0%
0%
0%
0%
Level 9
0%
10%
0%
20%
0%
0%
0%
0%
0%
0%
0%
0%
Level 10
10%
0%
10%
0%
0%
0%
0%
0%
0%
0%
0%
0%
Compared to the statistics obtained from BE, we observed more variation
in the results when running BPSO, with the majority of variations associated
with the Nordic data. This phenomenon resembles what appeared for the BE
experiments in Table 1. Despite the results being less unanimous, we can still
observed the fact that level 1 was repeatedly selected by the swarm-based
solver with percentages exceeding other levels by large margins. In addition,
Table 2 also shows that there is a consensus between the two feature selection
methods about level 1 being the most important predictor.
22
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 23

Table 3: The percentage that a given level appeared in the subset containing two levels
selected by BE algorithm. The results are provided for US and Nordic data sets and for
three diﬀerent prediction horizons, H = 10, 20, 50. Moreover, two models for the price
prediction with the LOB data are used, DeepLOB [25] and DeepLOB [22].
US Data
Nordic Data
DeepLOB
TABL
DeepLOB
TABL
H
10
20
50
10
20
50
10
20
50
10
20
50
Level 1
100%
100%
100%
100%
100%
100%
100%
100%
100%
80%
100%
100%
Level 2
10%
20%
15%
15%
35%
25%
5%
10%
30%
35%
55%
50%
Level 3
0%
20%
25%
20%
20%
15%
5%
5%
10%
10%
5%
20%
Level 4
10%
0%
5%
5%
20%
25%
15%
10%
5%
20%
5%
10%
Level 5
10%
5%
10%
0%
0%
0%
10%
5%
20%
10%
0%
5%
Level 6
5%
15%
5%
20%
10%
15%
5%
15%
5%
10%
5%
10%
Level 7
15%
10%
20%
15%
5%
5%
25%
20%
5%
15%
5%
0%
Level 8
20%
15%
5%
5%
5%
0%
15%
10%
20%
10%
15%
0%
Level 9
25%
15%
0%
15%
0%
0%
10%
20%
0%
5%
5%
0%
Level 10
5%
0%
15%
5%
5%
15%
10%
5%
5%
5%
5%
5%
Table 4: The average percentage of appearance in a 2-element subset selected by BE
algorithm over all prediction horizons, neural network models and datasets, i.e., average
over all columns in Table 3.
Level 1
Level 2
Level 3
Level 4
Level 5
Level 6
Level 7
Level 8
Level 9
Level 10
98.33%
25.42%
12.92%
10.83%
6.25%
10.00%
11.67%
10.00%
7.92%
6.67%
4.4. What is the second most important predictor?
Given that the quote data from level 1 are the most important source of
information in the order-book, which level comes second? In order to seek
an answer for this question, we need to look at another statistic from the
results. Particularly, from the set of results obtained from BE method, we
looked at the percentage that a given level appeared in the subsets selected
by BE having a cardinality of 2. Due to the sequential removal nature of BE,
we know for certain that the numbers for level 1 are similar or higher than
those appear in Table 1. But can we observe a similar phenomenon for any
other level when BE is allowed to form a subset of two levels?
The statistics for this inquiry are shown in Table 3. The numbers in this
table indicate that there is no level that seems to consistently appear by
more than 50% with the top quote data in 2-element subsets chosen by BE.
In fact, for each level, we computed the average percentage of appearance in
23
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 24

a 2-element subset selected by BE over all prediction horizons, neural network
models and datasets, i.e., the average number for every row in Table 3, we
observed that the second highest record comes from level 2, however, at only
25.42%. The records for all levels are shown in Table 4. By following the same
procedure and computing the average percentage of each level appearing in
the 1-element, 2-element and 3-element subsets yielded by BE algorithm, we
obtained Figure 2, which gives us an overall insights into the importance of
each level assessed by BE algorithm.
Level 1
Level 2
Level 3
Level 4
Level 5
Level 6
Level 7
Level 8
Level 9 Level 10
0
20
40
60
80
100
Percentage
1-element subset
2-element subset
3-element subset
Figure 2: The average percentage of appearance of each level in the 1-element, 2-element
and 3-element subsets selected by BE algorithm.
Table 5: The average percentage of appearance in the ﬁnal solution outputed by BPSO
algorithm over all prediction horizons, neural network models and datasets, i.e., average
over all columns in Table 2
Level 1
Level 2
Level 3
Level 4
Level 5
Level 6
Level 7
Level 8
Level 9
Level 10
75.83%
16.67%
10.83%
1.67%
4.17%
0.83%
0.83%
0.83%
2.50%
1.67%
From Figure 2, we can see that the top three quote levels of the LOB are
also ranked in the same order according to the frequency of being selected
by BE. To ﬁnd potential consensus between BE and BPSO, we also computed
the average percentage of appearance in the ﬁnal solution of BPSO for each
level, which is shown in Table 5. From Figure 2 and Table 5, we can see that
there is indeed a consensus between BE and BPSO about the ranking between
the top three levels while there is no consistent ranking for levels beyond the
top three.
24
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 25

Level 1
Level 2
Level 3
Level 4
Level 5
Level 6
Level 7
Level 8
Level 9 Level 10
0
20
40
60
80
Percentage
best solution discovered
second best solution discovered
third best solution discovered
Figure 3: The average percentage of appearance of each level in the best, second best
and third best solution discovered by BPSO algorithm during optimization process. The
statistics are aggregated from both US and Nordic data for all prediction horizons
For BPSO, we cannot specify the size of the selected subset, thus, we cannot
analyse the appearance of a given level with a ﬁxed subset cardinality as in BE.
However, for BPSO, we can also look at the average percentage of appearance
of each level in the second and third best solutions discovered by the swarm
during the course of optimization. The statistics, aggregated from both US
and Nordic data in all prediction horizons, are shown in Figure 3, which also
conﬁrms the ranking between the top three levels of the LOB suggested by
BE.
4.5. Are quotes beyond the best levels needed for good performance?
In the previous analysis, we have identiﬁed that the top quotes carry the
most important information that is relevant for the prediction of mid-price
movements. However, we have not looked at the prediction performances
achieved by using the subsets of information selected by the feature selection
algorithms. In this section, we analyze this question.
Table 6 shows F1 scores measured on the test set (out-of-sample) of the
US and Nordic datasets on Panels A and B, respectively.
In particular,
the mean F1 and the lowest and highest F1 across the diﬀerent seed values
are provided. The ﬁrst line of each panel shows the performances of the
corresponding neural network models that were trained using data of all ten
LOB levels, denoted as baseline. The second line of each panel shows the
performance with the most important level, sequentially identiﬁed with BE.
25
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 26

Table 6: Model performance reported as the mean F1 score in % with the lowest and
highest F1 across the diﬀerent seed values. The results are provided for US (Panel A)
and Nordic (Panel B) data sets and for three diﬀerent prediction horizons, H = 10, 20, 50.
Moreover, two models for the price prediction with the LOB data are used, DeepLOB
[25] and DeepLOB [22]. The ﬁrst line shows the performances of the models that were
trained using data of all ten LOB levels, denoted as Baseline. The second line shows the
results on the most important level, sequentially identiﬁed with BE. The third level shows
performance of the models based on the use of the set of levels, optimized by BPSO.
DeepLOB
TABL
H
10
20
50
10
20
50
Panel A: US Data
Baseline
65.01 ± 00.36
66.27 ± 00.12
65.73 ± 00.21
64.31 ± 00.28
65.26 ± 00.16
65.38 ± 00.07
BE
63.66 ± 02.57
60.85 ± 04.43
64.98 ± 00.12
60.57 ± 00.84
63.13 ± 00.57
64.02 ± 00.16
BPSO
64.35 ± 00.22
65.74 ± 00.09
62.26 ± 03.69
62.77 ± 00.87
64.38 ± 00.44
62.94 ± 03.17
Panel B: Nordic Data
Baseline
69.92 ± 01.86
71.53 ± 02.22
71.83 ± 00.49
70.10 ± 01.23
71.32 ± 00.89
71.89 ± 00.74
BE
63.77 ± 08.12
68.24 ± 06.78
71.87 ± 00.08
66.84 ± 02.02
69.44 ± 01.35
71.29 ± 00.72
BPSO
68.53 ± 01.89
68.18 ± 03.36
69.07 ± 03.27
67.06 ± 02.43
70.38 ± 01.12
70.15 ± 03.00
The third level shows the performance with the set of levels, optimized by
BPSO.
It is clear from the both panels that there are performance degradations
with both BE and BPSO almost under all conﬁgurations (the only exception
is BPSO with H = 1 with DeepLOB on Nordic data). In particular, when
using the subsets of data, i.e. the most informative LOB levels, selected by
BE, we observed on average 3.76% decline in performance for US stocks, and
3.58% for Nordic stocks. Two conclusions can be drawn: On the ﬁrst hand,
the use of the most informative LOB level data, which, according to Table
1, most often come from the top of the book, provides surprisingly good
performance. On the second hand, using quote data across the order-book
provides extra performance gains. For the levels that maximize the ﬁtness
function within the training procedure with BPSO, the average reductions are
2.43% and 3.10% for US and Nordic stocks, respectively. This means that
the the optimal selection of the set of LOB levels in the training phase does
not lead to the superior out-of-sample performance.
Are these a few percents diﬀerences are substantial or marginal? To an-
swer this question, one needs to judge whether improvements can outweigh
the extra computational cost, which depend on a speciﬁc targets and appli-
cation settings in practice. Nevertheless, based on our analysis, one can be
assured that there is indeed useful information contained in levels beyond
26
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 27

the top quotes in the LOB.
5. Conclusion
The major part of the existing literature uses the top-quotes of the limit
order book data only, which makes us to ask how informative the top quotes
are compared the quotes beyond them. Moreover, one can ask if multi-level
order book data should be used instead of best-level data only, even at the
cost of complexity of the model. In this paper, we answered these questions
in the context of stock price prediction. Because the ﬁnancial market mech-
anisms can be highly non-linear, in contrast to existing papers, we employed
a non-linear approach. For a robustness of the results, we used two well-
performing machine learning models [25, 22]. Moreover, two data sets from
diﬀerent kind of markets, namely from US and Nordic markets, are used. The
questions are addressed by two (variable) feature selection algorithms: one
which removes the most irrelevant methods and another one which identiﬁes
the optimal set of order book levels for the prediction task: Backward Elim-
ination (BE) [45, 46] and Binary Particle Swarm Optimization (BPSO) [47].
Furthermore, for additional robustness checks, diﬀerent prediction horizons
are used.
We provide a number of results that are robust across several the dimen-
sions (ML prediction models, feature selection algorithms, data sets, predic-
tion horizons). The best bid and ask levels are systematically identiﬁed not
only to be the most informative levels in the order books, but to carry most
of the information needed for good prediction performance. More speciﬁ-
cally, in terms of the models’ predictive power (performance), the inclusion
of multiple levels from the limit order books improves models’ performance
by around 3.5%. Thus, even if the top-of-the-book levels contain most of the
relevant information, to maximize models’ performance one should use all
data across all the levels. Moreover, the informativeness of the levels clearly
decreases from the ﬁrst to the fourth level while the rest of the levels are
approximately equally important.
6. Acknowledgements
The authors wish to acknowledge CSC – IT Center for Science, Fin-
land, for computational resources. A. Iosiﬁdis acknowledges funding from
the Independent Research Fund Denmark project DISPA (Project Number:
9041-00004).
27
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 28

References
[1] L. E. Harris, V. Panchapagesan, The information content of the limit
order book: evidence from nyse specialist trading decisions, Journal of
Financial Markets 8 (1) (2005) 25–67.
[2] M. Siikanen, J. Kanniainen, J. Valli, Limit order books and liquidity
around scheduled and non-scheduled announcements: Empirical evi-
dence from nasdaq nordic, Finance Research Letters 21 (2017) 264–271.
[3] M. Siikanen, J. Kanniainen, A. Luoma, What drives the sensitivity of
limit order books to company announcement arrivals?, Economics Let-
ters 159 (2017) 65–68.
[4] Y. A¨ıt-Sahalia, P. A. Mykland, L. Zhang, Ultra high frequency volatility
estimation with dependent microstructure noise, Journal of Economet-
rics 160 (1) (2011) 160–175.
[5] F. M. Bandi, J. R. Russell, Separating microstructure noise from volatil-
ity, Journal of Financial Economics 79 (3) (2006) 655–692.
[6] A. Dufour, R. F. Engle, Time and the price impact of a trade, The
Journal of Finance 55 (6) (2000) 2467–2498.
[7] R. F. Engle, A. J. Patton, Impacts of trades in an error-correction model
of quote prices, Journal of Financial Markets 7 (1) (2004) 1–25.
[8] J.-P. Bouchaud, Y. Gefen, M. Potters, M. Wyart, Fluctuations and re-
sponse in ﬁnancial markets: the subtle nature of ‘random’price changes,
Quantitative ﬁnance 4 (2) (2004) 176–190.
[9] Z. Eisler, J.-P. Bouchaud, J. Kockelkoren, The price impact of order
book events: market orders, limit orders and cancellations, Quantitative
Finance 12 (9) (2012) 1395–1419.
[10] F. Guilbaud, H. Pham, Optimal high-frequency trading with limit and
market orders, Quantitative Finance 13 (1) (2013) 79–94.
[11] T. Hendershott, C. M. Jones, A. J. Menkveld, Does algorithmic trading
improve liquidity?, The Journal of ﬁnance 66 (1) (2011) 1–33.
28
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 29

[12] A. P. Chaboud, B. Chiquoine, E. Hjalmarsson, C. Vega, Rise of the ma-
chines: Algorithmic trading in the foreign exchange market, The Journal
of Finance 69 (5) (2014) 2045–2084.
[13] R. Cont, S. Stoikov, R. Talreja, A stochastic model for order book dy-
namics, Operations research 58 (3) (2010) 549–563.
[14] R. Cont, A. De Larrard, Price dynamics in a markovian limit order
market, SIAM Journal on Financial Mathematics 4 (1) (2013) 1–25.
[15] A. Anand, S. Chakravarty, T. Martell, Empirical evidence on the evolu-
tion of liquidity: Choice of market versus limit orders by informed and
uninformed traders, Journal of Financial Markets 8 (3) (2005) 288–308.
[16] J. T. Linnainmaa, Do limit orders alter inferences about investor perfor-
mance and behavior?, The Journal of Finance 65 (4) (2010) 1473–1506.
[17] A. Pardo, R. Pascual, On the hidden side of liquidity, The European
Journal of Finance 18 (10) (2012) 949–967.
[18] J. D. Farmer, P. Patelli, I. I. Zovko, The predictive power of zero in-
telligence in ﬁnancial markets, Proceedings of the National Academy of
Sciences 102 (6) (2005) 2254–2259.
[19] N. Hautsch, R. Huang, The market impact of a limit order, Journal of
Economic Dynamics and Control 36 (4) (2012) 501–522.
[20] F. Abergel, A. Jedidi, A mathematical approach to order book modeling,
International Journal of Theoretical and Applied Finance 16 (05) (2013)
1350025.
[21] M. Dixon, D. Klabjan, J. H. Bang, Classiﬁcation-based ﬁnancial mar-
kets prediction using deep neural networks, Algorithmic Finance 6 (3-4)
(2017) 67–77.
[22] D. T. Tran, A. Iosiﬁdis, J. Kanniainen, M. Gabbouj, Temporal attention-
augmented bilinear network for ﬁnancial time-series data analysis, IEEE
transactions on neural networks and learning systems 30 (5) (2018)
1407–1418.
29
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 30

[23] J. Sirignano, R. Cont, Universal features of price formation in ﬁnancial
markets: perspectives from deep learning, Quantitative Finance 19 (9)
(2019) 1449–1459.
[24] J. A. Sirignano, Deep learning for limit order books, Quantitative Fi-
nance 19 (4) (2019) 549–570.
[25] Z. Zhang, S. Zohren, S. Roberts, Deeplob: Deep convolutional neural
networks for limit order books, IEEE Transactions on Signal Processing
67 (11) (2019) 3001–3012.
[26] Y. M¨akinen, J. Kanniainen, M. Gabbouj, A. Iosiﬁdis, Forecasting jump
arrivals in stock prices: new attention-based network architecture using
limit order book data, Quantitative Finance 19 (12) (2019) 2033–2050.
[27] P. Nousi, A. Tsantekidis, N. Passalis, A. Ntakaris, J. Kanniainen,
A. Tefas, M. Gabbouj, A. Iosiﬁdis, Machine learning for forecasting
mid-price movements using limit order book data, IEEE Access 7 (2019)
64722–64736.
[28] N. Passalis, A. Tefas, J. Kanniainen, M. Gabbouj, A. Iosiﬁdis, Deep
adaptive input normalization for time series forecasting, IEEE Trans-
actions on Neural Networks and Learning Systems Forthcoming (2019).
doi:10.1109/TNNLS.2019.2944933.
[29] A. Briola, J. Turiel, R. Marcaccioli, T. Aste, Deep reinforcement learn-
ing for active high frequency trading, arXiv preprint arXiv:2101.07107
(2021).
[30] C. Cao, O. Hansch, X. Wang, The information content of an open limit-
order book, Journal of Futures Markets: Futures, Options, and Other
Derivative Products 29 (1) (2009) 16–41.
[31] R. Pascual, D. Veredas, What pieces of limit order book information
do are informative? an empirical analysis of a pure order-driven market
(2003).
[32] D. A. Hsieh, Chaos and nonlinear dynamics: application to ﬁnancial
markets, Journal of Finance 46 (5) (1991) 1839–1877.
30
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 31

[33] C. P. Chen, Z. Liu, S. Feng, Universal approximation capability of broad
learning system and its structural variations, IEEE transactions on neu-
ral networks and learning systems 30 (4) (2018) 1191–1204.
[34] W. Long, Z. Lu, L. Cui, Deep learning-based feature engineering for
stock price movement prediction, Knowledge-Based Systems 164 (2019)
163–173.
[35] Z. Fu, W. Xu, R. Hu, G. Long, J. Jiang, Mhier-encoder: Modelling
the high-frequency changes across stocks, Knowledge-Based Systems 224
(2021) 107092.
[36] H. Gunduz, Y. Yaslan, Z. Cataltepe, Intraday prediction of borsa is-
tanbul using convolutional neural networks and feature correlations,
Knowledge-Based Systems 137 (2017) 138–148.
[37] T. Zhou, S. Gao, J. Wang, C. Chu, Y. Todo, Z. Tang, Financial time
series prediction using a dendritic neuron model, Knowledge-Based Sys-
tems 105 (2016) 214–224.
[38] H. K. Cao, H. K. Cao, B. T. Nguyen, Delafo: An eﬃcient portfolio
optimization using deep neural networks, in: Paciﬁc-Asia Conference on
Knowledge Discovery and Data Mining, Springer, 2020, pp. 623–635.
[39] Z. Zhang, S. Zohren, S. Roberts, Deep learning for portfolio optimiza-
tion, The Journal of Financial Data Science 2 (4) (2020) 8–20.
[40] P. M. Addo, D. Guegan, B. Hassani, Credit risk analysis using machine
and deep learning models, Risks 6 (2) (2018) 38.
[41] M. Leo, S. Sharma, K. Maddulety, Machine learning in banking risk
management: A literature review, Risks 7 (1) (2019) 29.
[42] J. Cao, J. Chen, J. C. Hull, Z. Poulos, Deep hedging of derivatives using
reinforcement learning, Available at SSRN 3514586 (2019).
[43] J. Du, M. Jin, P. N. Kolm, G. Ritter, Y. Wang, B. Zhang, Deep rein-
forcement learning for option replication and hedging, The Journal of
Financial Data Science 2 (4) (2020) 44–57.
[44] G. Chandrashekar, F. Sahin, A survey on feature selection methods,
Computers & Electrical Engineering 40 (1) (2014) 16–28.
31
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 32

[45] M. Efroymson, Multiple regression analysis, Mathematical methods for
digital computers (1960) 191–203.
[46] R. R. Hocking, A biometrics invited paper. the analysis and selection of
variables in linear regression, Biometrics (1976) 1–49.
[47] J. Kennedy, R. C. Eberhart, A discrete binary version of the parti-
cle swarm algorithm, in: 1997 IEEE International conference on sys-
tems, man, and cybernetics. Computational cybernetics and simulation,
Vol. 5, IEEE, 1997, pp. 4104–4108.
[48] D. E. Rumelhart, G. E. Hinton, R. J. Williams, Learning representations
by back-propagating errors, nature 323 (6088) (1986) 533–536.
[49] D. P. Kingma, J. Ba, Adam: A method for stochastic optimization,
arXiv preprint arXiv:1412.6980 (2014).
[50] C. Szegedy, W. Liu, Y. Jia, P. Sermanet, S. Reed, D. Anguelov, D. Er-
han, V. Vanhoucke, A. Rabinovich, Going deeper with convolutions, in:
Proceedings of the IEEE conference on computer vision and pattern
recognition, 2015, pp. 1–9.
[51] S. Hochreiter, J. Schmidhuber, Long short-term memory, Neural com-
putation 9 (8) (1997) 1735–1780.
[52] K. Cho, B. Van Merri¨enboer, C. Gulcehre, D. Bahdanau, F. Bougares,
H. Schwenk, Y. Bengio, Learning phrase representations using rnn
encoder-decoder for statistical machine translation, arXiv preprint
arXiv:1406.1078 (2014).
[53] V. F. Flack, P. C. Chang, Frequency of selecting noise variables in subset
regression analysis: a simulation study, The American Statistician 41 (1)
(1987) 84–86.
[54] S. Derksen, H. J. Keselman, Backward, forward and stepwise automated
subset selection algorithms: Frequency of obtaining authentic and noise
variables, British Journal of Mathematical and Statistical Psychology
45 (2) (1992) 265–282.
32
Electronic copy available at: https://ssrn.com/abstract=3920827


## Page 33

[55] P. C. Austin, J. V. Tu, Automated variable selection methods for lo-
gistic regression produced unstable models for predicting acute myocar-
dial infarction mortality, Journal of clinical epidemiology 57 (11) (2004)
1138–1146.
[56] A. Ntakaris, M. Magris, J. Kanniainen, M. Gabbouj, A. Iosiﬁdis, Bench-
mark dataset for mid-price forecasting of limit order book data with ma-
chine learning methods, Journal of Forecasting 37 (8) (2018) 852–866.
[57] D. T. Tran, J. Kanniainen, M. Gabbouj, A. Iosiﬁdis, Data normaliza-
tion for bilinear structures in high-frequency ﬁnancial time-series, in:
International Conference on Pattern Recognition (ICPR), 2020.
[58] S. Ioﬀe, C. Szegedy, Batch normalization: Accelerating deep network
training by reducing internal covariate shift, in: International conference
on machine learning, PMLR, 2015, pp. 448–456.
[59] D. Ulyanov, A. Vedaldi, V. Lempitsky, Instance normalization: The
missing ingredient for fast stylization, arXiv preprint arXiv:1607.08022
(2016).
[60] K. He, X. Zhang, S. Ren, J. Sun, Delving deep into rectiﬁers: Surpassing
human-level performance on imagenet classiﬁcation, in: Proceedings of
the IEEE international conference on computer vision, 2015, pp. 1026–
1034.
33
Electronic copy available at: https://ssrn.com/abstract=3920827


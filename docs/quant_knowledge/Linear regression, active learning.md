6.867 Machine learning, lecture 5 (Jaakkola) 1
Linear regression, active learning
We arrived at the logistic regression model when trying to explicitly model the uncertainty
about the labels in a linear classifier. The same general modeling approach permits us to
use linear predictions in various other contexts as well. The simplest of them is regression
where the goal is to predict a continuous response y ∈ R to each example vector. Here
t
too focusing on linear predictions won’t be inherently limiting as linear predictions can be
easily extended (next lecture).
So, how should we model continuous responses? The linear function of the input already
produces a “mean prediction” or θT x + θ . By treating this as a mean prediction more
0
formally, we are stating that the expected value of the response variable, conditioned on
x, is θT x + θ . More succinctly, we say that E{y|x} = θT x + θ . It remains to associate
0 0
a distribution over the responses around such mean prediction. The simplest symmetric
distribution is the normal (Gaussian) distribution. In other words, we say that the responses
y follow the normal pdf
� �
1 1
N(y; µ,σ2) = √ exp − (y − µ)2 (1)
2πσ2 2σ2
where µ = θT x + θ . Our response model is therefore defined as
0
P (y|x,θ,θ ) = N(y; θT x + θ , σ2) (2)
0 0
So, when the input is 1-dimensional, we predict a mean response that is a line in (x,y)
space, and assume that noise in y is normally distributed with zero mean and variance σ2 .
Note that the noise variance σ2 in the model does not depend on the input x. Moreover, we
only model variation in the y-direction while expecting to know x with perfect precision.
Taking into account the effect of potential noise in x on the responses y would tie parameters
θ and θ to the noise variance σ2, potentially in an input dependent manner. The specifics
0
of this coupling depend on the form of noise added to x. We will discuss this in a bit more
detail later on.
We can also write the linear regression model in another way to explicate how exactly the
additive noise appears in the responses:
y = θT x + θ + � (3)
0
where � ∼ N(0,σ2) (meaning that noise � is distributed normally with mean zero and
variance σ2). Clearly for this model E{y|x} = θT x + θ since � has zero mean. Moreover,
0
adding Gaussian noise to a deterministic prediction θT x + θ makes y normally distributed
0
Cite as: Tommi Jaakkola, course materials for 6.867 Machine Learning, Fall 2006. MIT OpenCourseWare
(http://ocw.mit.edu/), Massachusetts Institute of Technology. Downloaded on [DD Month YYYY].(cid:13)(cid:10)

| 6.867 Machine learning, lecture 5 (Jaakkola)  |     |     |                              |     |     |     |     |     |     |     |     |     | 2   |
| --------------------------------------------- | --- | --- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| with mean θT x + θ                            |     |     | and variance σ2, as before.  |     |     |     |     |     |     |     |     |     |     |
So, in particular, for the training inputs
0
| x ,..., x | and outputs y |     |     | ,...,y | , the model relating them is  |     |     |     |     |     |     |     |     |
| --------- | ------------- | --- | --- | ------ | ----------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1         | n             |     |     | 1      | n                             |     |     |     |     |     |     |     |     |
= θT x
|         |                 |     |     | y                   | + θ | + � | , t = | 1,...,n      |     |     |     |     | (4)  |
| ------- | --------------- | --- | --- | ------------------- | --- | --- | ----- | ------------ | --- | --- | --- | --- | ---- |
|         |                 |     |     | t                   | t   | 0   | t     |              |     |     |     |     |      |
| where e | ∼ N(0,σ2) and e |     |     | is independent of e |     |     |       | for any i =� |     | i.  |     |     |      |
|         | t               |     |     | i                   |     |     | j     |              |     |     |     |     |      |
Regardless of how we choose the write the model (both forms are useful) we can find the
parameter estimates by maximizing the conditional likelihood.  Similarly to the logistic
regression case, the conditional likelihood is written as
|     |     |     |     |     | n   1 |     | �   | 1   |     |     | �   |     |     |
| --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
�
|     |     | L(θ,θ | ,σ2) | =   | √   | exp  | −   | (y   | − θT x | − θ | )2  |     | (5)  |
| --- | --- | ----- | ---- | --- | --- | ---- | --- | ---- | ------ | --- | --- | --- | ---- |
|     |     |       | 0    |     |     |      |     | 2σ2  | t      | t   | 0   |     |      |
2πσ2
t=1
Note that σ2 is also a parameter we have to estimate. It accounts for errors not captured
by the linear model. In terms of the log-likelihood, we try to maximize
|     |        |        |     |     |        |       |      |      |           |     |         |     |      |
| --- | ------ | ------ | --- | --- | ------ | ----- | ---- | ---- | --------- | --- | ------- | --- | ---- |
|     |        |        |     | n   |   �    |       | �    |      |           |     |         | ��  |      |
|     |        |        |     | �   |        | 1     |      | 1    |           |     |         |     |      |
|     | l(θ, θ | , σ2)  |     | =   | log  √ |       | exp  | −    | (y − θT x |     | − θ )2  |     | (6)  |
|     |        | 0      |     |     |        |       |      |      | t         | t   | 0       |     |      |
|     |        |        |     |     |        | 2πσ2  |      | 2σ2  |           |     |         |     |      |
t=1
|     |     |     |     |     |       |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     | n   |  � 1  |     | 1   |     | 1   |     |     | �   |     |
�
|     |     |     |     | =   | −  log(2π) −  |     |     | log σ2 −  |      | (y − θT x |     | − θ )2  | (7)  |
| --- | --- | --- | --- | --- | ------------- | --- | --- | --------- | ---- | --------- | --- | ------- | ---- |
|     |     |     |     |     |               |     |     |           |      | t         | t   | 0       |      |
|     |     |     |     |     | 2             |     | 2   |           | 2σ2  |           |     |         |      |
t=1
|     |     |     |     |              |     |           |      | n   |        |     |     |     |      |
| --- | --- | --- | --- | ------------ | --- | --------- | ---- | --- | ------ | --- | --- | --- | ---- |
|     |     |     |     |              | n   |           | 1    | �   |        |     |     |     |      |
|     |     |     |     |              |     | log σ2 −  |      |     | − θT x |     | )2  |     |      |
|     |     |     |     | =  const. −  |     |           |      |     | (y     |     | − θ |     | (8)  |
|     |     |     |     |              | 2   |           | 2σ2  |     | t      | t   | 0   |     |      |
t=1
where ’const.’ absorbs terms that do not depend on the parameters. Now, the problem of
estimating the parameters θ and θ is nicely decoupled from estimating σ2 . In other words,
0
|     |     |     |     | ˆ   | ˆ   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
we can find the maximizing θ and θ by simply minimizing the mean squared error
0
n
�
|     |     |     |     |     |     | − θT x |     | )2  |     |     |     |     |      |
| --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | ---- |
|     |     |     |     |     | (y  |        | − θ |     |     |     |     |     | (9)  |
|     |     |     |     |     |     | t      | t   | 0   |     |     |     |     |      |
t=1
It is perhaps easiest to write the solution based on a bit of matrix calculation.  Let X be
a matrix whose rows, indexed by training examples, are given by [xT , 1] (x turned into a
|     |     |     |     |     |     |     |     |     |     |     | t   | t   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
row vector and 1 added at the end).  In terms of this matrix, the minimization problem
Cite as: Tommi Jaakkola, course materials for 6.867 Machine Learning, Fall 2006. MIT OpenCourseWare
(http://ocw.mit.edu/), Massachusetts Institute of Technology. Downloaded on [DD Month YYYY].(cid:13)(cid:10)

6.867 Machine learning, lecture 5 (Jaakkola) 3
becomes
�
n
�
y −
�
θ
�T �
x t
�
�2
= �
n �
y − � xT , 1 �
�
θ
��2
(10)
t θ 1 t t θ
0 0
t=1 t=1
� � � ⎡ y 1 ⎤ ⎡ x 1 T , 1 ⎤ � θ � � � � 2
= �⎣ ··· ⎦ − ⎣ ··· ⎦ � (11)
�
� y xT , 1
θ
0
�
�
n n
� � ��2
� θ �
= �
�
y − X
θ
�
�
(12)
0
� �T � �T � �
θ θ θ
= y T y − 2 XT y + XT X (13)
θ θ θ
0 0 0
where y = [y ,...,y ]T is a vector of training responses. Solving it yields
1 n
�
θ
ˆ �
= (XT X)−1XT y (14)
ˆ
θ
0
Note that the optimal parameter values are linear functions of the observed responses y. We
will make use of this property later on. The dependence on the training inputs x ,..., x
1 n
(or the matrix X) is non-linear, however.
The noise variance can be subsequently set to account for the remaining prediction errors.
Indeed, the the maximizing value of σ2 is given by
1 �
n
σˆ2 = (y − θ ˆT x − θ ˆ )2 (15)
t t 0
n
t=1
which is the average squared prediction error. Note that we cannot compute σˆ2 before
knowing how well the linear model explains the responses.
Bias and variance of the parameter estimates
We can make use of the closed form parameter estimates in Eq.(14) to analyze how good
these estimates are. For this purpose let’s make the strong assumption that the actual
relation between x and y follows a linear model of the same type that we are estimating
(we just don’t know the correct parameter values θ∗, θ∗, and σ∗2). We can therefore describe
0
the observed responses y as
t
y = θ∗T x + θ∗ + � , t = 1,...,n (16)
t t 0 t
Cite as: Tommi Jaakkola, course materials for 6.867 Machine Learning, Fall 2006. MIT OpenCourseWare
(http://ocw.mit.edu/), Massachusetts Institute of Technology. Downloaded on [DD Month YYYY].(cid:13)(cid:10)

6.867 Machine learning, lecture 5 (Jaakkola)  4
∼ N(0,σ∗2). In a matrix form
where �
t
|     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
� θ∗  �
|     |     |     |     | y = X  |     |     | + e  |     |     |     |     | (17)  |
| --- | --- | --- | --- | ------ | --- | --- | ---- | --- | --- | --- | --- | ----- |
θ∗
0
where e = [� ,...,� ]T , E{e} = 0 and E{eeT } = σ∗2 I. The noise vector e is also indepen­
|     | 1   | n   |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
dent of the inputs or X. Plugging this form of responses into Eq.(14) we get
|     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | � ˆ | �   |     |     |     | �   | �   |     |     |     |     |
|     |     | θ   |     |     |     |     | θ∗  |     |     |     |     |     |
(XT X)−1XT (X
|     |     |     | =   |     |     |     |     | + e)  |     |     |     | (18)  |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | ----- |
|     |     | θ ˆ |     |     |     |     | θ∗  |       |     |     |     |       |
|     |     |     | 0   |     |     |     |     | 0     |     |     |     |       |
|     |     |     |     |     |     |     |     |       |     |     |     |       |
|     |     |     |     |     |     |     | �   | �     |     |     |     |       |
θ∗
|     |     |     | =   | (XT X)−1XT X  |     |     |     | +(XT X)−1XT e  |     |     |     | (19)  |
| --- | --- | --- | --- | ------------- | --- | --- | --- | -------------- | --- | --- | --- | ----- |
θ∗
0
|     |     |     |     |       |                |     |     |     |     |     |     |       |
| --- | --- | --- | --- | ----- | -------------- | --- | --- | --- | --- | --- | --- | ----- |
|     |     |     |     | � θ∗  | �              |     |     |     |     |     |     |       |
|     |     |     | =   |       | +(XT X)−1XT e  |     |     |     |     |     |     | (20)  |
θ∗
0
In other words, our parameter estimates can be decomposed into the sum of correct under­
lying parameters and estimates based on noise alone (i.e., based on e).  Thus, on average
with fixed inputs
|     |     | �   � |        | �   | �                     |     |     |     | �   |   �   |     |       |
| --- | --- | ----- | ------ | --- | --------------------- | --- | --- | --- | --- | ----- | --- | ----- |
|     |     | θ ˆ   |        | θ∗  |                       |     |     |     |     | θ∗    |     |       |
|     | E{  |       | |X} =  |     | +(XT X)−1XT E{e|X} =  |     |     |     |     |       |     | (21)  |
|     |     | ˆ     |        | θ∗  |                       |     |     |     |     | θ∗    |     |       |
θ
|     |     | 0   |     |     | 0   |     |     |     |     | 0   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Our parameter estimates are therefore unbiased or correct on average when averaging is
over possible training sets we could generate.  The averaging here is conditioned on the
specific training inputs.
Using Eq.(20) and Eq.(21) we can also evaluate the conditional co-variance of the parameter
estimates where the expectation is again over the noise in the outputs:

|       |     |      |     | �   |      |     |     |        |     |        | �   |       |
| ----- | --- | ---- | --- | --- | ---- | --- | --- | ------ | --- | ------ | --- | ----- |
|       | �   | ˆ �  |     |     | �� ˆ | �   | �   | ���� ˆ | �   | � ��T  |     |       |
|       |     | θ    |     |     | θ    |     | θ∗  | θ      |     | θ∗     |     |       |
| Cov{  |     | |X}  | =   | E   |      | −   |     |        | −   |        | |X  | (22)  |
|       |     | ˆ    |     |     | ˆ    |     |     | ˆ      |     |        |     |       |
|       |     | θ    |     |     | θ    |     | θ∗  | θ      |     | θ∗     |     |       |
|       |     | 0    |     |     |      | 0   | 0   |        | 0   | 0      |     |       |

|     |     |     |     | �                                |               |     |     |               |     | �   |     |       |
| --- | --- | --- | --- | -------------------------------- | ------------- | --- | --- | ------------- | --- | --- | --- | ----- |
|     |     |     |     |                                  | �             |     | ��  |               |     | �T  |     |       |
|     |     |     | =   | E                                | (XT X)−1XT e  |     |     | (XT X)−1XT e  |     | |X  |     | (23)  |
|     |     |     |     |                                  |               |     |     |               |     |     |     |       |
|     |     |     |     | �                                |               |     |     |               | �   |     |     |       |
|     |     |     | =   | E  (XT X)−1XT ee T X(XT X)−1|X   |               |     |     |               |     |     |     | (24)  |
|     |     |     | =   | (XT X)−1XT E{ee T |X} X(XT X)−1  |               |     |     |               |     |     |     | (25)  |
(XT X)−1XT (σ∗2 I) X(XT X)−1
|     |     |     | =   |                          |     |     |     |     |     |     |     | (26)  |
| --- | --- | --- | --- | ------------------------ | --- | --- | --- | --- | --- | --- | --- | ----- |
|     |     |     | =   | σ∗2(XT X)−1XT X(XT X)−1  |     |     |     |     |     |     |     | (27)  |
σ∗2(XT X)−1
|     |     |     | =   |     |     |     |     |     |     |     |     | (28)  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
Cite as: Tommi Jaakkola, course materials for 6.867 Machine Learning, Fall 2006. MIT OpenCourseWare
(http://ocw.mit.edu/), Massachusetts Institute of Technology. Downloaded on [DD Month YYYY].(cid:13)(cid:10)

| 6.867 Machine learning, lecture 5 (Jaakkola)  |     |     |     |     |     |     |     |     |     | 5   |
| --------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
So the way in which the parameters vary in response to noise in the outputs is a function
of the inputs or X. We will use this property in the next section to select inputs so as to
improve the quality of the parameter estimates or to reduce the variance of predictions.
Based on the bias and variance calculations we can evaluate the mean squared error of
the parameter estimates. To this end, we use the fact that the expectation of the squared
norm of any vector valued random variable can be decomposed into a bias and variance
components as follows:
|            |     |     |                         |     |     |     |     |     |     |       |
| ---------- | --- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | ----- |
| �          | �   |     | �                       |     |     |     | �   |     |     |       |
| �z − z∗�2  |     |     | �z − E{z} + E{z}− z∗�2  |     |     |     |     |     |     |       |
| E          |     | =   | E                       |     |     |     |     |     |     | (29)  |
|            |     |     |                         |     |     |     |     |     |     |       |
|            |     |     | �                       |     |     |     |     |     |     | �     |
=  E  �z − E{z}�2 + 2(z − E{z})T (E{z}− z∗)+ �E{z}− z∗�2  (30)
|     |     |     |              |     |      |              |     |                          |     |     |
| --- | --- | --- | ------------ | --- | ---- | ------------ | --- | ------------------------ | --- | --- |
|     |     |     | �            |     | �    | �            |     | �                        |     |     |
|     |     |     | �z − E{z}�2  |     |      | (z − E{z})T  |     | (E{z}− z∗)+ �E{z}− z∗�2  |     |     |
|     |     | =   | E            |     | +2E  |              |     |                          |     |     |
variance
|     |     |     |                 |     |                | bias2  |     |     |     |       |
| --- | --- | --- | --------------- | --- | -------------- | ------ | --- | --- | --- | ----- |
|     |     |     | �               | ��  | �              |        |     |     |     |       |
|     |     |     | �               |     | � �            | ��     | �   |     |     |       |
|     |     | =   | E  �z − E{z}�2  |     | + �E{z}− z∗�2  |        |     |     |     | (31)  |
where we have assumed that z∗ is fixed. Make sure you understand how this decomposition
is derived. We will further elaborate the variance part to better use the result in our context:
|     |     |                 |     |     |       |                         |     |     |     |       |
| --- | --- | --------------- | --- | --- | ----- | ----------------------- | --- | --- | --- | ----- |
|     |     | �               |     | �   | �     |                         |     |     | �   |       |
|     |     | E  �z − E{z}�2  |     |     | =  E  | (z − E{z})T (z − E{z})  |     |     |     | (32)  |
|     |     |                 |     |     |       |                         |     |     |     |       |
|     |     |                 |     |     | �     |                         |     |     |  �  |       |

|     |     |     |     |     |       | � (z − E{z})T (z − E{z})   |     |     | �   |       |
| --- | --- | --- | --- | --- | ----- | -------------------------- | --- | --- | --- | ----- |
|     |     |     |     |     | =  E  | Tr                         |     |     |     | (33)  |
|     |     |     |     |     |       |                            |     |     |     |       |
|     |     |     |     |     | �     |                            |     |     |  �  |       |
|     |     |     |     |     |       | �                          |     |     | �   |       |
|     |     |     |     |     | =  E  | Tr  (z − E{z})(z − E{z})T  |     |     |     | (34)  |
|     |     |     |     |     |       |                            |     |     |     |       |
|     |     |     |     |     | �     | �                          |     |     | ��  |       |
(z − E{z})(z − E{z})T
|     |     |     |     |     | =  Tr           | E   |     |     |     | (35)  |
| --- | --- | --- | --- | --- | --------------- | --- | --- | --- | --- | ----- |
|     |     |     |     |     | =  Tr [Cov{z}]  |     |     |     |     | (36)  |
where Tr[·] is the matrix trace, the sum of its diagonal components, and therefore a linear
operation (exchangeable with the expectation). We have also used the fact that Tr[aT b]
=
Tr[abT ] for any vectors a and b.
Cite as: Tommi Jaakkola, course materials for 6.867 Machine Learning, Fall 2006. MIT OpenCourseWare

(http://ocw.mit.edu/), Massachusetts Institute of Technology. Downloaded on [DD Month YYYY].(cid:13)(cid:10)

| 6.867 Machine learning, lecture 5 (Jaakkola)  |     |     |     |     |     |     |     |     |     |     |     | 6   |
| --------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Now, adapting the result to our setting, we get
bias2
|     |       |     |        |     | variance            |     |     |      |     | =0     |     |        |
| --- | ----- | --- | ------ | --- | ------------------- | --- | --- | ---- | --- | ------ | --- | ------ |
|     |       |     |        |     |                     |     |     |      |     |        |     |        |
|     |       |     |        |     | �                   | ��  |     | � �  |     | ��     |     | �      |
| �   | � �   | � � | �� 2   | �   | �                   | ��  | �   | �� � | ��  | � �    | �   | �� 2   |
|     | θ ˆ   | θ∗  |        |     |                     |     | θ ˆ |      | θ ˆ |        | θ∗  |        |
|     | �     |     | �      |     |                     |     |     | �    |     |        |     | �      |
| E   | �     | −   | �      | |X  | =  Tr  Cov          |     | |X  | + �E |     | |X  −  |     | �      |
|     | � θ ˆ | θ∗  | �      |     |                     | θ ˆ |     | �    | θ ˆ |        | θ∗  | �      |
|     |       | 0   | 0      |     |                     |     | 0   |      |     | 0      | 0   |        |
|     |       |     |        |     |                     |     |     |      |     |        |     |        |
|     |       |     |        |     | σ∗2 Tr  � (XT X)−1  |     | �   |      |     |        |     |        |
|     |       |     |        |     | =                   |     |     |      |     |        |     | (37)   |
Let’s understand this result a bit further. How does it depend on n, the number of training
examples? In other words, how quickly does the mean squared error decrease as the number
of training examples increases, assuming the input examples x are sampled independently
from some underlying distribution P (x)?  To answer this let’s start by analyzing what
happens to the matrix XT X:

|     |     |     |       |     | n  � | �    |       |     |     |     |     |       |
| --- | --- | --- | ----- | --- | ---- | ---- | ----- | --- | --- | --- | --- | ----- |
|     |     |     |       |     | � x  |      |       |     |     |     |     |       |
|     |     |     | XT X  |     | t    | [xT  |       |     |     |     |     |       |
|     |     |     |       | =   |      |      | , 1]  |     |     |     |     | (38)  |
|     |     |     |       |     | 1    | t    |       |     |     |     |     |       |
t=1

|     |     |     |     |     | n  � |     | �         |     |     |     |     |       |
| --- | --- | --- | --- | --- | ---- | --- | --------- | --- | --- | --- | --- | ----- |
|     |     |     |     |     | 1 �  | x   |           |     |     |     |     |       |
|     |     |     |     | =   | n ·  | t   | [xT , 1]  |     |     |     |     | (39)  |
|     |     |     |     |     | n    | 1   | t         |     |     |     |     |       |
|     |     |     |     |     | t=1  |     |           |     |     |     |     |       |
|     |     |     |     |     |      | ��  | �         | �   |     |     |     |       |
x
[xT  , 1]
|     |     |     |     | ≈   | n · E |     |     | = n · C  |     |     |     | (40)  |
| --- | --- | --- | --- | --- | ----- | --- | --- | -------- | --- | --- | --- | ----- |
|     |     |     |     |     | x∼P   | 1   |     |          |     |     |     |       |
where for large n the average will be close to the corresponding expected value. For large
n the mean squared error of the parameter estimates will therefore be close to
σ∗2
|     |     |     |     |     | · Tr[C−1]  |     |     |     |     |     |     | (41)  |
| --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | ----- |
n
The variance of simply averaging the (noise in the) outputs would behave as σ∗2/n. Since
we are estimating d + 1 parameters where d is the input dimension, this dependence would
have to be in Tr[C−1]. Indeed it is. This term, a trace of a (d + 1) × (d + 1) matrix C−1 ,
is directly proportional to d + 1.
Penalized log-likelihood and Ridge regression
When the number of training examples is small, i.e., not too much larger than the number
of parameters (dimension of the inputs), it is often beneficial to regularize the parameter
estimates. We will derive the form of regularization here by assigning a prior distribution
over the parameters P (θ,θ ). The purpose of the prior is to prefer small parameter values
0
Cite as: Tommi Jaakkola, course materials for 6.867 Machine Learning, Fall 2006. MIT OpenCourseWare
(http://ocw.mit.edu/), Massachusetts Institute of Technology. Downloaded on [DD Month YYYY].(cid:13)(cid:10)

6.867 Machine learning, lecture 5 (Jaakkola) 7
(predict values close to zero) in the absence of data. Specifically, we will look at simple
zero mean Gaussian distributions
� � � � d
θ 0 �
P (θ,θ ; σ�2) = N( ; ,σ�2I) = N(θ ;0,σ�2) N(θ ;0,σ�2) (42)
0 θ 0 0 j
0
j=1
where the variance parameter σ�2 in the prior distribution specifies how strongly we wish
to bias the parameters towards zero.
By combining the log-likelihood criterion with the prior we obtain a penalized log-likelihood
function (penalized by the prior):
�
n �
1
�
1
��
l�(θ,θ ,σ2) = log √ exp − (y − θT x − θ )2 + log P (θ,θ ; σ�2) (43)
0 2πσ2 2σ2 t t 0 0
t=1
n 1 �
n
= const. − log σ2 − (y − θT x − θ )2
2 2σ2 t t 0
t=1
1 �
d
d +1
− (θ2 + θ2) − log σ�2 (44)
2σ�2 0 j 2
j=1
It is convenient to tie the prior variance σ�2 to the noise variance σ2 according to σ�2 = σ2/λ.
This has the effect that if the noise variance σ2 is large, we penalize the parameters very
little (permit large deviations from zero by assuming a large σ�2). On the other hand, if
the noise variance is small, we could be over-fitting the linear model. This happens, for
example, when the number of training examples is small. In this case most of the responses
can be explained directly by the linear model making the noise variance very small. In such
cases our penalty for the parameters will be larger as well (prior variance is smaller).
Incorporating this parameter tie into the penalized log-likelihood function gives
n 1 �
n
l�(θ,θ ,σ2) = const. − log σ2 − (y − θT x − θ )2
0 2 2σ2 t t 0
t=1
λ �
d
d +1
− (θ2 + θ2) − log(σ2/λ) (45)
2σ2 0 j 2
j=1
n + d +1 d +1
= const. − log σ2 + log λ (46)
2 2
� �
1 �
n
�
d
− (y − θT x − θ )2 + λ(θ2 + θ2) (47)
2σ2 t t 0 0 j
t=1 j=1
Cite as: Tommi Jaakkola, course materials for 6.867 Machine Learning, Fall 2006. MIT OpenCourseWare
(http://ocw.mit.edu/), Massachusetts Institute of Technology. Downloaded on [DD Month YYYY].(cid:13)(cid:10)

6.867 Machine learning, lecture 5 (Jaakkola)  8
separates from setting the noise variance σ2 . Note
where again the estimation of θ and θ
0
that this separation is achieved because we tied the prior and noise variance parameters.
The above regularized problem of finding the parameter estimates θ ˆ and θ ˆ is known as
0
Ridge regression.
As before, we can get closed form estimates for the parameters (we omit the analogous
derivation):

|     |     |     | � ˆ | �   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
θ
|     |     |     |     | = (λI + XT X)−1XT y  |     |     | (48)  |
| --- | --- | --- | --- | -------------------- | --- | --- | ----- |
ˆ
θ
0
It is now useful to understand how the properties of these parameter estimates depend on
λ. For example, are the parameter estimates unbiased? No, they are not:
|     |     |       |     |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- |
|     | ��  | �     | �   |     | � � |     |     |
|     |     | θ ˆ   |     |     | θ∗  |     |     |
(λI + XT X)−1XT X
|     | E   |     | |X  =  |     |     |     | (49)  |
| --- | --- | --- | ------ | --- | --- | --- | ----- |
|     |     | θ ˆ |        |     | θ∗  |     |       |
|     |     | 0   |        |     | 0   |     |       |

� �
θ∗
(λI + XT X)−1(XT X + λI − λI)
|     |     |     | =   |     |     |     | (50)  |
| --- | --- | --- | --- | --- | --- | --- | ----- |
θ∗
0
bias
|     |     |     |     |                  |      |       |       |
| --- | --- | --- | --- | ---------------- | ---- | ----- | ----- |
|     |     |     |     |    �             | ��   | �     |       |
|     |     |     |     | � θ∗  �          | �    | θ∗  � |       |
|     |     |     | =   | −λ(λI + XT X)−1  |      |       | (51)  |
|     |     |     |     | ˆ∗               |      | θ∗    |       |
θ
|     |     |     |     | 0                     |     | 0     |       |
| --- | --- | --- | --- | --------------------- | --- | ----- | ----- |
|     |     |     |     |                       |  �  | �     |       |
|     |     |     |     |                       | θ∗  |       |       |
|     |     |     |     | � I − λ(λI + XT X)−1  | �   |       |       |
|     |     |     | =   |                       |     |       | (52)  |
θ∗
0
|     |     |     |     |                       |     |     |     |
| --- | --- | --- | --- | --------------------- | --- | --- | --- |
|     |     |     |     | � I − λ(λI + XT X)−1  | �   |     |     |
It is straightforward to check that  is a positive definite matrix with
eigenvalues all less than one.  The parameter estimates are therefore shrunk towards zero
and more so the larger the value of λ.  This is what we would expect since we explicitly
favored small parameter values with the prior penalty. What do we gain from such biased
parameter estimates? Let’s evaluate the mean squared error, starting with the covariance:
|     |      |     |     |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- | --- |
|     | �� ˆ | � � |     |     |     |     |     |
θ
| Cov  |     | |X  | =  σ∗2(λI + XT X)−1XT X(λI + XT X)−1  |     |     |     | (53)  |
| ---- | --- | --- | ------------------------------------- | --- | --- | --- | ----- |
ˆ
θ
0
|     |     |     | =  σ∗2(λI + XT X)−1(λI + XT X − λI)(λI + XT X)−1  |     |     |     | (54)  |
| --- | --- | --- | ------------------------------------------------- | --- | --- | --- | ----- |
|     |     |     | =  σ∗2(λI + XT X)−1 − λσ∗2(λI + XT X)−2           |     |     |     | (55)  |
The mean squared error in the parameters is therefore given by (we again omit the deriva-
Cite as: Tommi Jaakkola, course materials for 6.867 Machine Learning, Fall 2006. MIT OpenCourseWare
(http://ocw.mit.edu/), Massachusetts Institute of Technology. Downloaded on [DD Month YYYY].(cid:13)(cid:10)

6.867 Machine learning, lecture 5 (Jaakkola) 9
tion that can be obtained similarly to previous expressions):
� �
E � � �
�
�
θ ˆ
θ ˆ � − � θ
θ
∗
∗
�� � �
�
2 |X = σ∗2 · Tr � ( λI + XT X)−1 − λ(λI + XT X)−2 �
0 0
�
θ∗
�T �
θ ∗
�
+λ2 (λI + XT X)−2 (56)
θ∗ θ∗
0 0
Can this be smaller than the mean squared error corresponding to the unregularized esti­
� �
mates σ∗2 · Tr (XT X)−1 ? Yes, it can. This is indeed the benefit from regularization: we
can reduce large variance at the cost of introducing a bit of bias. We will get back to this
trade-off in the context of model selection.
Let’s exemplify the effect of λ on the mean squared error in a context of a very simple
1-dimensional example. Suppose, we have observed responses for only two points, x = −1
and x = 1. In this case,
� � � � � �
−1 1 2 0 1/(2 + λ) 0
X = , XT X = , (λI + XT X)−1 = (57)
1 1 0 2 0 1/(2 + λ)
The expression for the mean squared error therefore becomes
� �
� � � θ ˆ � � θ∗ �� � 2 � 2 2λ � λ2
E �
� θ ˆ
−
θ∗
�
�
|X = σ∗2
(2 + λ)
−
(2 + λ)2
+
(2 + λ)2
(θ∗2 + θ
0
∗ 2)
0 0
4σ∗2 λ2
= + (θ∗2 + θ∗2) (58)
(2 + λ)2 (2 + λ)2 0
� �
We should compare this to σ∗2Tr (XT X)−1 = σ∗2 obtained without regularization (cor­
responds to setting λ = 0). In the noisy case σ∗2 > θ∗2 + θ∗2 we can set λ = 2 and
0
obtain
� �
� � � θ ˆ � � θ∗ �� � 2 4σ∗2 4 8σ∗2 1
E �
� θ ˆ
−
θ∗
�
�
|X =
16
+
16
(θ∗2 + θ
0
∗ 2) <
16
=
2
σ∗2 (59)
0 0
The mean squared error of the parameters is therefore clearly smaller than without regu­
larization.
Active learning
We can use the expressions for the mean squared error to actively select input points
x ,..., x , when possible, so as to reduce the resulting estimation error. This is an active
1 n
Cite as: Tommi Jaakkola, course materials for 6.867 Machine Learning, Fall 2006. MIT OpenCourseWare
(http://ocw.mit.edu/), Massachusetts Institute of Technology. Downloaded on [DD Month YYYY].(cid:13)(cid:10)

6.867 Machine learning, lecture 5 (Jaakkola)  10
learning  (experiment design) problem.  The goal is to get by with as few responses as
possible without sacrificing the estimation accuracy.  For example, in training a classifier
we would like to minimize the number of training images we would have to label in order
obtain a certain classification accuracy.  In the regression context, we may be selecting
among possible experiments to carry out (e.g., choosing different operating points for a
factory or gauging market/customer responses to different strategies available to us).  By
letting the method guide the selection of the training examples (inputs), we will generally
need far fewer examples in comparison to selecting them at random from some underlying
distribution, database, or trying available experiments at random. Fewer responses means
less human effort, less cost, or both.
To develop this further let’s go back to the unregularized case where
|
      |       |
          |            |     |       |
| ------ | ----- | ---------- | ---------- | --- | ----- |
| � �
  |

   | ��
 2 �   |            |     |       |
| � θ ˆ
 | � � θ | ∗          |            |     |       |
| �      |       | � = σ∗2Tr
 | �          | �   |       |
| E
 �   | −
    | � |X

    | ( XT X)−1  |     | (60)
 |
|
 ˆ    | θ     | ∗
      |            |     |       |
| � θ    |       | �          |            |     |       |
0  0
We do not know the noise variance σ∗2
for the correct model but it only appears as a
multiplicative constant in the above expression and therefore won’t affect how we should
choose the inputs. When the choice of inputs is indeed up to us (e.g., which experiments to

� �
carry out) we can select them so as to minimize Tr  (XT X)−1  . One caveat of this approach
is that it relies on the underlying relationship between the inputs and the responses to be
linear. When this is no longer the case we may end up with clearly suboptimal selections.
We will discuss next time how we can find say n input examples x ,..., x that minimize
1 n
the criterion.
Cite as: Tommi Jaakkola, course materials for 6.867 Machine Learning, Fall 2006. MIT OpenCourseWare
(http://ocw.mit.edu/), Massachusetts Institute of Technology. Downloaded on [DD Month YYYY].(cid:13)(cid:10)
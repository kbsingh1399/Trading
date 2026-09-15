# # To whom correspondence should be addressed

- **Source File**: `ssrn-4180768.pdf`
- **Total Pages**: 20
- **SSRN ID**: `ssrn-4180768`

---

## Page 1

# To whom correspondence should be addressed
EnLFADE: Ensemble Learning Based Fake Account Detection on Ethereum Blockchain
Lavina Pahuja
Department of Mathematics
Jamia Millia Islamia (A Central University)
New Delhi-110025, India
Email: lavinapahuja95@gmail.com
Ahmad Kamal#
Department of Mathematics
Jamia Millia Islamia (A Central University)
New Delhi-110025, India
Email: akamal1@jmi.ac.in
Abstract:
Cryptocurrencies continue to captivate businesses and investors despite market fluctuations. The 
number of crypto users have risen rapidly in the last few years, and alarmingly, many appear to be 
unaware of the risks involved. These risks aren't confined to market hazards but include very 
sophisticated cybercrimes related to cryptocurrencies. As cryptocurrencies have become a breeding 
ground for a variety of cybercrimes, resulting in enormous financial losses, it hinders user adoption 
limiting the utility of the blockchain technology. It has become crucial to spot such scams and devise 
intelligent techniques to make this technology a safer place for investors. This study proposes a 
classification model to handle fake account problem over Ethereum blockchain, and its contribution is 
multi-faceted; firstly, available imbalanced Ethereum dataset has been balanced to enhance the 
accuracy of the classification model. Secondly, correlation-based feature selection technique has been 
applied to retain best discriminating features. Thirdly, an effective machine learning based model has 
been presented for the identification of fake accounts over the Ethereum system. A comparative study 
of ten machine learning techniques has been presented consisting of both individual and ensemble 
classifiers. Experimental results showed that ensemble classifiers appear to yield better performance 
measures over individual classifiers and among all, LightGbm-based classification model 
outperformed with 99.2 % accuracy.
Keywords: Ethereum Blockchain, Ensemble Learning, Machine Learning, Data Imbalance, Fake 
Account Detection
1.
Introduction
Cryptocurrencies have seen a massive growth due to the evolution of blockchain technology and its 
economic ecosystem. Latest innovations in digital currencies have given rise to a whole new means of 
exchanging values that has the potential to eventually replace traditional notary services or payment 
processing organisations [1, 2]. Hundreds of cryptocurrency exchanges have emerged as essential 
trading platforms for the ecosystem, facilitating the trading of digital assets. As of the end of 2018, 
there were over 2,000 distinct cryptocurrencies, including Bitcoin, Ethereum, and Litecoin 
[1]. However, the current technical advancement of cryptocurrencies and its associated advantages 
have been tainted by a several unlawful affairs taking place on the network, including illicit accounts, 
money laundering, bribery and phishing etc. [3], resulting in massive financial losses [4].
1.1 Cryptocurrency and blockchain: 
A cryptocurrency or a virtual currency is a digital asset designed to function as a medium of exchange 
that encrypts transactions. A cryptocurrency’s transactions are given substance by a blockchain that 
accumulates and archives all trades between the two parties permanently. Each record is referred as a 
block that includes a digital hash pointer to the earlier block, a timestamp, and trade records [5]. A 
blockchain usually implements a cryptocurrency which can be swapped for other cryptocurrencies or 
fiat money through exchanges. For years, the data and information of people have long been held and 
performed by a centralised and trusted arbitrator, such as governments or businesses. Due to 
organisational changes, people have to confront issues like excessive fees, data silos, and instability. 
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 2

However, after the induction of blockchain technology, one doesn’t need to rely on these old-
fashioned third parties as the data can be effortlessly distributed around the world. The technology 
both makes the system reliable and reduces the charges levied by middlemen [6]. Thus, 
cryptocurrency is comparable to traditional currency, with the exception that it does not have a 
physical form and operates through encryption [46]. A quick rundown of the two most prominent 
cryptocurrencies are as follows:
Bitcoin: Created in 2009, Bitcoin is the first digital money to run in a multi user architecture, with no 
central authority to monitor transactions. It is the first cryptographic commodity that can be traded 
like cash. It has risen to become the world's most popular cryptocurrency in recent years, with an 
increasing number of businesses accepting it as payment, fostering a crypto-driven society [2, 7].
Ethereum: Introduced in 2014 by Vitalik Buterin, Ethereum is a publicly available blockchain 
platform that supports smart contracts. It facilitates multi user transactions by utilising Ether, a 
dedicated cryptocurrency [6]. Like Bitcoin, Ethereum is based on blockchain technology, but it goes 
one step further by allowing developers to execute programmes, such as smart contracts, that may 
host any type of decentralised application, often known as "dApps" [47]. Thus, Ethereum provided 
solution to the challenges faced in Bitcoin. In line with [49], buying ether money is significantly faster 
than buying bitcoin, around 14-15 seconds compared to bitcoin's near-uniform 10 minutes.
1.2 Frauds in cryptocurrencies 
The invention of digital currency, specifically Bitcoin and Ethererum, was initially hailed as a game-
changer; nevertheless, the popularity of these currencies has grown in tandem with a bad spirit of 
speculation, fraud, and hype throughout the past decade. Bitcoin investors were duped by a Ponzi 
scheme known as the Bitcoin Savings & Trust. In this scheme, early investors were given money by 
taking money from later investors. It became one of the most infamous fraud cases using a fictitious 
Initial Coin Offering (ICO) [7, 48]. Similar as Bitcoin, Ethereum has also been the victim of multiple 
cyberattacks in tandem with its growing popularity. It has also been subjected to several entities 
engaging in illicit behaviour on the network, including phishing, money laundering, fraud, and other 
criminal activities [3]. Despite the fact that the bitcoin technology is continually changing and trying 
to provide an error-free system for its users, the reputation of cryptocurrency has been tarnished as a 
result of the aforementioned behaviours. As mentioned in [3], an anomalous behaviour over the 
network was discovered after an account paid $450,000, divided in 3 trades, to transfer almost 0.1 
ETH in 2019. Such transactions raised questions about their legitimacy, further highlighting if they 
were genuine errors in which the account owner mistaken the transaction fee for transfer of Ether, or 
if they are part of any conspiracy in regard to money laundering [3]. The proliferation of the 
aforementioned Ethereum scams will not only stifle user adoption, but will also limit block chain 
technology's utility. As a result, it is critical to identify such scams and develop effective strategies to 
make technology a safer environment for investors. 
Recent enhancement in Machine Learning (ML) has attracted researchers worldwide to use data and 
algorithm and train machines to learn in the same way that humans do, with the goal of constantly 
improving accuracy. With the rise in Ethereum transactions, ML has become a major tool for handling 
classification difficulties. Such algorithms adaptively improve their performance as the number of 
transactions available for learning increases. ML techniques consists of both individual and ensemble 
learning based classification. The ensemble learning strategy combines multiple base models to create 
a single optimal predictive model. When compared to individual models, ensemble learning strategies 
have been shown to perform better and have higher predictive accuracy. Current study has 
demonstrated the applicability of ML techniques focusing on five different individual classifiers 
including Naïve Bayes [9], Decision Trees [10], Support Vector Machine (SVM) [11], K Nearest 
Neighbour (KNN) [12], Logistic Regression [13] and five different bagging and boosting Ensemble 
Classifiers including Catboost [14], Adaboost [15], Xgboost [16], LightGbm [17] and Random Forest 
[18]. However, for an ensemble ML classifier to function effectively, experimental dataset needs to be 
balanced as in many cases class label attribute is not equally distributed which further contributes to 
the creation of biased models. In this work, a popular technique known as Synthetic Minority 
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 3

Oversampling Technique (SMOTE) [8, 32] has been used for handling imbalanced dataset to improve 
accuracy. As per our knowledge, this study is the first systematic work of the application of ensemble 
techniques for the detection of fake accounts over Ethereum blockchain. The work can be utilised to 
detect fake accounts by investigative and enforcement authorities, developers, researchers, news 
organisations, and private companies, and remains very helpful in performing filtered activities like 
combating terror financing and money laundering [4]. Major contributions of this paper includes:

To design an ensemble ML based classification model for classifying fake accounts over the 
Ethereum network. 

Comparative analysis of various ensemble classifiers’ performance over individual classifiers.

To perform exploratory data analysis and handling imbalanced dataset using SMOTE.

Feature selection using Pearson Correlation Coefficient for enhancing accuracy.
The remaining paper has been laid out as follows: Section 2 gives an assessment of the related works. 
Section 3 highlights ML ensemble approaches followed by section 4 which introduces the proposed 
ML based classification model and depiction of the dataset used in the reported study, pre-processing 
steps and feature engineering. Section 5 highlights the experimental and evaluated outcomes. Finally, 
Section 6 discusses the conclusion with future directions of work.
2.
Related Works
This section shows some relevant study in which researchers proposed models for detecting 
cryptocurrency fraud. Researchers have been attempting to create computationally intelligent methods 
to detect frauds in the crypto space. Such frauds are growing rapidly with many crypto investors being 
duped either by a Ponzi scheme or the money invested in crypto is illegally transferred to a fraudulent 
account by online criminals. Pengcheng Xia et al. [1] were the first to identify and classify 
cryptocurrency exchange scams in 2019. They gathered existing reports and used typosquatting 
creation tools to identify approximately 1,500 and 300 scam domains and bogus apps, respectively. 
They then looked into their connections and discovered 94 fraudulent domain groups and 30 false app 
groups. Authors revealed that such scams resulted in a financial loss of $520K and also discovered 
183 blockchain addresses linked to the attackers. Their findings are critical for blockchain 
stakeholders, and they illustrate the urgency of identifying and preventing blockchain scams. In [19], 
Hao Hua Sun Yin et al. developed and validated a unique method for deanonymizing the Bitcoin 
network and recognized numerous unlawful activities using supervised learning during 2019. In this 
study, the dataset used includes nearly 395 million transactions among 12 categories. It also includes 
957 unique cluster-created classifiers that distinguish between illegal activities, including scam stolen 
bitcoins, darknet market among others. The authors used seven Machine Learning algorithms viz. 
Decision Tree, Random Forest, Adaboost, Extra Trees, KNN, Bagging, and Gradient Boosting with 
Gradient Boosting algorithm outperforming the others with a mean cross validation accuracy and      
F1 score of 80.42 percent and 79.64 percent, respectively.
Further, T phan et al. [20] emphasized on anomaly detection over bitcoin network. The most suspect 
users and transactions were identified by the researchers in this investigation. Their dataset included 
over 6 million unidentified individuals, over 37 million transactions, and nearly 30 identified bitcoin 
criminals. They have created network of two graphs based on Bitcoin transaction, and employed 
various algorithms to discover anomalies namely - K-means clustering, Mahalanobis distance, and 
unsupervised Support Vector Machine (SVM). Despite their low agreement metrics, they were able to 
detect two known occurrences of burglary and one known case of loss out of a total of 30. Likewise, 
Sayadi et al. [21] proposed a study that employed two ML methods to identify bitcoin transaction 
fraud. To begin with, a one class SVM was identified to discover numerous irregularities in bitcoin 
electronic transactions and the accuracy was reported as 90%. Later, the authors utilised the k-means 
algorithm to find similar abnormalities.
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 4

It has been observed that Ethereum network is growing up nowadays leading to frauds similar as 
Bitcoin. Rahmez Fawaz Ibrahim et al. [22] in 2021, suggested a fraud detection model based on 
Decision Tree (J48), Random Forest, and K Nearest Neighbours (KNN) approaches for detecting 
bogus accounts over the Ethereum blockchain. The authors used a supervised dataset that included 
7651 regular transactions and 159 fraudulent transactions with 42 attributes. They were able to 
enhance time measurements and F measure using Random Forest. In [3], Steven Farrugia et al. used 
datasets obtained from two sources: Etherscamb and a local Geth client, totalling 4681 accounts, with 
2179 fraudulent and 2502 normal accounts. They proposed a gradient boosting based classifier 
Xgboost for the identification of bogus accounts. Authors claimed to attain an average accuracy of 
96.4% and Area Under Curve (AUC) as 0.994, after applying 10-fold cross validation. Authors 
revealed that three features namely time difference between first and last minutes, total Ether balance 
and min value received outperform other features used in this study. 
In Ethereum space, phishing scams are rapidly appearing that include creation of a fraudulent certified 
website and tracking accounts while logging, so as to steal sensitive data including passwords. In [23], 
authors proposed a systematic approach for detecting phishing accounts using Ethereum blockchain 
transactions. Transactions on the Ethereum network and the designated phishing addresses were 
collected by utilising the parity client and crawling etherscan.io. Authors developed a transaction 
graph utilising extracted data and suggested an attribute extraction technique. Then, they proposed a 
LightGbm-based Dual-sampling Ensemble model to detect phishing suspects based on the retrieved 
features. Yuan Huang et al. [4] developed a 3-phase framework by mining transaction records to 
detect Ethereum phishing frauds during 2020. Firstly, they built the Ethereum transaction network 
after obtaining the labelled phishing accounts and their transaction logs. Then, latent properties of 
accounts were extracted using node2vec for phishing classification. Finally, authors employed the one 
class SVM to determine whether the account is phishing. Their model attained an F score of 0.846. In 
[24], Alam Sarma et al. designed a framework to identify phishing scams using Random Forest (RF) 
and Decision Tree (DT). Their model was fed with standard datasets of phishing assaults obtained 
from kaggle.com. Further PCA was used to examine the features, and finally, they reported accuravy 
of 97% and 91% using RF and DT respectively. 
Apart from phishing, various fraudulent behaviour has also been detected on Ethereum network. In 
[25], a study published during 2019 looked at etherscamdb.info and etherscan.io databases and 
reported nearly 420 and 53 fraudulent wallets. Authors built a transaction network based on 
transactional data, evaluated it using graph traversal technique, and clustered them by applying ML 
techniques viz. K-means clustering, Support Vector Machine, and Random Forest. The Random 
Forest class model was reported as the most effective in their experiments. 
From the above literature survey, it has been observed that most researchers have applied their 
learning on imbalanced datasets, resulting in bias model formation. In imbalanced dataset, standard 
classifiers are generally skewed by huge classes and the small ones are ignored. Further, it has been 
found that majority of the research work uses individual classifiers [20, 21, 22] to handle this 
problem. However, very few research efforts are based on ensemble techniques [3, 19]. The aim of 
the current work is to balance the dataset and exploit the benefits of ensemble learning techniques for 
achieving high precision and accuracy.
3.
Methodology
Ensemble Machine Learning is a broad meta method that tries to improve predictive performance by 
merging the projections from various diverse models. For a number of classification and regression 
issues, ensemble approaches have proven to be effective. By combining several weak classifiers, the 
errors of a single base classifier will be remunerated by other strong base learners, leading to 
ensemble's overall prediction performance superior than that of a single base learner [27]. Such 
classifiers provide superior accuracy with lower errors, greater consistency by dodging overfitting, 
and decreases bias and variance errors. Bagging and boosting are the most popular ensemble ML 
techniques as they exhibit powerful experimental results and theoretical performance guarantees [28]. 
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 5

Bagging: A bootstrap aggregation technique developed by Breiman in 1996 initiates by voting 
various classifiers generated by different bootstrap samples. As shown in Figure 1, it learns several 
homogeneous weak classifiers with high variance (independently from each other) and combines their 
predicted result using averaging process in regression and majority voting in classification. The 
number of classifiers used in the ensemble has a direct relationship with the drop in this variance 
aspect [28]. Thus making it suitable for classification problems. The major advantages of bagging are 
as follows:

To increase stability and accuracy of the bagged result.

To reduce variance of the ensemble classifier. 
Given: Training data ‘D’
Base 
classifier
𝑪𝟏
Base 
classifier
𝑪𝟐
Base 
classifier
𝑪𝒏
𝑫𝟏
𝑫𝟐
Ensemble Classifier    𝑪∗
Classification: Maximum voting
Regression: Average=  𝒇(𝒙) =
𝟏
𝒃∑𝒏
𝒋= 𝟏𝝋𝒋(𝒙)
     Bootstrap
    Resampling
     Generation of
       base classifiers  
 Aggregation into
 strong 
classifier  
𝐶∗
𝑫
                                      Figure 1: Bagging
Boosting: Boosting creates an ensemble of classifiers through adapting the training set's distribution 
based on the accuracy of previously constructed classifiers. The probability distribution is adjusted for 
samples that were mistakenly forecasted by prior classifiers can be chosen more often than those that 
were correctly forecasted. Working steps of Boosting can be visualized using Figure 2. Boosting aims 
to create new classifiers that can better categorise rigid samples for earlier ensemble members [28]. It 
has two main advantages: 

It has significant relevance for small sample sizes and high-dimensional samples, compared to 
other classification techniques. 

It can choose features while categorising and is quick, easy to programme, highly adaptable, and 
accurate [30].
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 6

                            
Given: Training data ‘D’
         Ensemble Classifier    𝑪∗
𝒇(𝒙) = ∑𝒏
𝒋
𝟏𝜽𝒋𝝋𝒋(𝒙)
Weighting
Weighting
Base 
classifier
𝑪𝟏
Base 
classifier
𝑪𝒏
Base 
classifier
𝑪𝟐
     Combination of all
     classifiers using
   weighted avg. strategy
          
                               Figure 2: Boosting
Following sub-sections highlight the working details of some Bagging and Boosting algorithms used 
in this study. 
3.1 Random Forest: 
Random Forest [18], a most significant and robust Bagging method that can be seen as ensemble of 
classifiers made up of decision trees built from two different randomization sources. Each decision 
tree is proficient on a random sample of data, with replacement from original data of the equivalent 
size as the training set. Attribute sampling is a second source of randomization used in random forest 
[34]. Thus, bagging in conjunction with random attribute selection can be used to create random 
forests. It improves classification accuracy by using maximum voting and regulates the model to 
avoid overfitting [ 24]. In line with [33], the main steps of the algorithm are as follows:
1.
Suppose D = {
} denotes training data. A bootstrapping collection 
 of 
 (𝑥1,𝑦1),.....(𝑥𝑁,𝑦𝑁)
𝐷𝑗
dimension N from D (with replacement) has been picked where j = 1 to J. With 
 as the training 
𝐷𝑗
data, binary recursive partitioning has been used to adjust a tree. 
       a. Start by assembling all the data in a particular distinct node. 
       b. Till the terminating condition is achieved, repeat the following steps for each    
            undivided node:
            i. m predictors were randomly selected from the available p predictors. 
            ii. The efficient binary split has been chosen from all the m predictors
            iii. Using the best suited split (from step ii) the node has been divided into two daughter nodes 
2.
At new point x, a prediction has been made for:

Regression :  
                                                                                         (1)
𝑓(𝑥) =
1
𝐽∑𝐽
𝑗= 1ℎ𝑗(𝑥)

Classification : 
                                                          (2)
𝑓(𝑥) = 𝑎𝑟𝑔 𝑚𝑎𝑥𝑦∑𝐽
𝑗= 1𝐼(ℎ𝑗(𝑥) = 𝑦)
             where 
  implies the prediction of x (response variable) using the 
 tree.
ℎ𝑗(𝑥)
𝑗𝑡ℎ
3.2 Adaboost
Freund and Schapire invented a boosting method known as Adaboost in 1996 [15], which creates a 
powerful learning model by combining multiple weak learning models. In each iteration, misclassified 
data points are identified and their weights are increased, while the weights of correct data points are 
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 7

decreased, so that the following classifier can focus more on getting them correctly. The instruction 
continues in such a way that the weak learner's exit becomes the other learner's entry. The results are 
then merged, and the final decision limits are established [32, 50].  In this method, instances are 
pulled into successive data sets from an iteratively updated training data sample distribution, and the 
classifiers are integrated using weighted majority voting [31]. In line with [26], the major steps of the 
Adaboost algorithm are as follows :-
1.
Suppose  X= {
} be the sample set, where 
 (domain space) and 
 
 Y 
1
1
(
,
),.....(
,
)
m
m
x y
x
y
𝑥𝑖 ∈𝑋
𝑦𝑖∈
where Y={-1, +1}. Initialize, 
                   
, for t = 1,..,T                                             
  (3)
                                             𝐷𝑡(𝑖) =
1
𝑚
       Where 
 is a distribution that represents each instance's weights and train the weak classifier 
 𝐷𝑡(𝑖)
       using it.
2.
Training of weak classifier returns a weak hypothesis,
: X → {−1, +1} and the value of 
  
 ℎ𝑡
ℎ𝑡
should be set to minimise the weighted error: 
                                                           
  (4)
:
(
)
( )
t
i
i
t
t
i h
x
y
D i



3.
Adaboost selects a parameter, 
, to measure the relevance of the weak hypothesis and is defined 
𝛼𝑡 
as:                                       
                                   
  (5)
                           𝛼𝑡=
1
2ln(
1 ‒ 𝜀𝑡
𝜀𝑡)
4.
Well-classified examples are given lower weights than those that are misclassified. Adaboost 
apprises the distribution for each 
with label 
, by taking into account 
 and 
. 
= 1 since 
  
𝑥𝑖 
𝑦𝑖
𝛼𝑡
ℎ𝑡𝐷𝑡 
𝑍𝑡
is the chosen normalising factor.
  = 
  (6)
                                      𝐷𝑡+ 1(𝑖) =
𝐷𝑡(𝑖)
𝑍𝑡×{
𝑒‒ 𝛼𝑡  𝑖𝑓 ℎ𝑡(𝑥𝑖) = 𝑦𝑖
𝑒𝛼𝑡  𝑖𝑓 ℎ𝑡(𝑥𝑖) ≠𝑦𝑖
𝐷𝑡(𝑖)(𝑒
‒ 𝛼𝑡𝑦𝑖ℎ𝑡(𝑥𝑖))
𝑍𝑡
5.
Adaboost returns a final hypothesis when all T iterations have been completed: 
                                                            
  (7)
1
( )
(
( ))
T
t
t
t
H x
sign
h x




3.3 Xgboost
Xgboost [16] is an efficient, versatile, and portable parallel decision tree-based ensemble ML 
approach [27, 32]. It applies gradient descent on decision trees in order to develop a number of 
models, that are sequentially integrated while the earlier models are rectified to obtain the ultimate 
suitable model [31]. Xgboost overcomes one of the most important shortcomings of gradient boosting 
i.e. the potential losses that can be encountered when branching the tree. It examines how features are 
distributed among all the data points in a leaf and uses this knowledge to branch out the data. Based 
on the strengthening method of the Xgboost algorithm, the basic idea is to build a weak model, make 
inferences regarding various feature importance and parameters, and then use these results to create a 
new, stronger model, attempting to reduce the existing error by exploiting the previous model's 
misclassification error [35, 43]. In order to prevent data over-fitting, Xgboost uses a more 
systematised model formalisation, which improves efficiency when compared to previous gradient 
boosting methods. To do so, there is a need to study  functions, each of which contains tree structure 
ℎ𝑖
and leaf scores. In line with [22, 36], following are the major steps of the Xgboost algorithm :-
1.
Given a dataset S having m-samples and n-features, S = {( 
, 
 )}(|S| = m, 
 ∈ 
, 
 ∈ 
), a 
𝑋𝑗𝑦𝑗
𝑋𝑗
ℝ𝑛𝑦𝑗
ℝ
tree ensemble model employs L additive functions to forecast the result as presented in the 
equation (8).
                                                 
          
  (8)
𝑦'𝑗= 𝜑(𝑋𝑗) = ∑𝐿
𝑙= 1ℎ𝑙(𝑋𝐽) , ℎ𝑙 ∈𝐻  
where  
 is the space of regression trees, q signifies each 
𝐻= {ℎ(𝑋) = 𝑤𝑞(𝑋)} (𝑞:ℝ𝑛→𝑇,𝑤𝜖ℝ𝑛)
tree’s structure that maps a sample to its corresponding leaf index, and T represents total leaves in 
the tree. Each  relates to independent structure of tree q and leaf weights w. 
ℎ𝑙
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 8

2.
To understand the collection of functions used in the model, the regularised objective is 
minimised as follows in the equation (9).
                         (9)                                  
 𝐿(𝜑) = ∑𝑗𝑙 (𝑦'𝑗,𝑦𝑗) + ∑𝑙Ω(ℎ𝑙) , Ω(ℎ) = 𝛾𝑇+
1
2 𝜆 ||𝑤||2
where  denotes differentiable convex loss function which calculates difference between the target 
𝑙
and predicted 
, Ω penalizes complexity of the model in order to elude over-fitting.
𝑦𝑗 
𝑦'𝑗
3.
Xgboost also employs a 2nd order Taylor series goal function. If the loss or error function 
is the mean square error, then the objective function is stated using equation (10). 
                (10)
 𝐿(𝜑) = ∑𝑛
𝑗= 1[𝑝𝑗𝑤𝑞(𝑥𝑗) +
1
2(𝑞𝑗𝑤2
𝑞(𝑥𝑗))] +  𝛾𝑇+
1
2 𝜆 ∑𝐿
𝑙= 1𝑤𝑙
2
where, 
 and 
describes the 1st and 2nd derivatives of loss or error function, respectively,  while 
𝑝𝑗
𝑞𝑗  
 is a function which maps data points to the associated leaves.
𝑞(𝑥𝑗)
4.
Because the DT instances correspond to leaf nodes, the final loss value is the addition of loss 
values. Hence, objective function can be shown as: 
          
(11)
𝐿(𝜑) = ∑𝑇
𝑡= 1[𝑃𝑡𝑤𝑡+
1
2(𝑄𝑡 + 𝜆  )𝑤2
𝑡)] +  𝛾𝑇
where 
 and  indicates all samples in leaf node t. 
𝑃𝑡= ∑𝑗𝜖𝐼𝑡𝑝𝑗,𝑄𝑡= ∑𝑗𝜖𝐼𝑡𝑞𝑗, 
𝐼𝑡
5.
To summarise, objective function optimization is reduced to challenge of obtaining the optimum 
value of a quadratic function. Due to the addition of the regularisation term, Xgboost is more 
resistant to overfitting.
3.4 LightGbm 
Microsoft's LightGbm [17] is an open source gradient boosting decision tree method that implements 
a boosting technique in an efficient and scalable manner. Modern network connectivity is combined 
with the parallel voting decision tree method to maximise parallel learning. This method uses a 
histogram-based technique to speed up training and consume less memory. To locate the highest 
splitter gain of the leaf, LightGbm employs a leaf-by-leaf approach [37]. It employs two unique 
techniques: Gradient-based One-Side Sampling (GOSS) and Exclusive Feature Bundling (EFB) to 
handle vast data samples and features respectively. GOSS preserves all instances having higher 
gradients and random samples with lesser gradients. The EFB method aims at combining numerous 
selective features into a smaller number of dense characteristics, reducing the amount of time spent 
calculating zero feature values [34]. Large volumes of data can be processed quickly with the 
LightGbm algorithm. In line with [17, 42], the major steps of the algorithm are given as follows :-
1.
Suppose training data S = {
 }, 
 ,
 
 Y={-1,+1}, loss function be  L(y, 
 (𝑥1,𝑦1),.....(𝑥𝑁,𝑦𝑁)
𝑥𝑖 ⊆ℝ 𝑦𝑖∈
x) and number of iterations be M. Let the sampling ratio of large gradient data and sampling ratio 
of small gradient data be a and b respectively.
2.
Merge mutually exclusive features by using EFB method. For m=1 to M, calculate absolute values 
of gradients   
  , i ={1, …,N}                                                        (12)           
𝑟𝑖= |
∂𝐿(𝑦𝑖,𝜃(𝑥𝑖 )
∂𝜃(𝑥𝑖 ) |
∂𝜃(𝑥) = 𝜃𝑚‒ 1(𝑥)
3.
Resampling dataset by using GOSS method:
        top
 = a
 and rand
= b
,
 𝑁
 × 𝑙𝑒𝑛( 𝑆 )
 𝑁 
 × 𝑙𝑒𝑛( 𝑆 )
        sorted = GetSortedIndices(abs(r)),
        E = sorted [ 1 : top
], F = RandomPick(sorted[ top
 : 
] , rand
)
 𝑁
 𝑁𝑙𝑒𝑛( 𝑆 )
 𝑁
        S_ = E + F
4.
Compute information gains: -
                                     
(𝑑)=
                 (13)    
𝑉𝑗
1
𝑛(
(∑𝑥𝑖𝜖𝐴𝑙𝑟𝑖+
1 ‒ 𝑎
𝑏∑𝑥𝑖𝜖𝐵𝑙𝑟𝑖)
2
𝑁𝑗𝑙(𝑑)
+
(∑𝑥𝑖𝜖𝐴𝑟𝑟𝑖+
1 ‒ 𝑎
𝑏∑𝑥𝑖𝜖𝐵𝑟𝑟𝑖)
2
𝑁𝑗𝑟(𝑑)
)
𝑛𝑡
5.
Obtain another decision tree 
′(𝑋)  on set S ′. Then update 
(𝑋) = 
(𝑋) + 
′(𝑋), for m=1 
𝜃𝑚
𝜃𝑚
𝜃𝑚‒ 1
𝜃𝑚
to M. Hence, 
′(𝑋)  =
(𝑋)
𝜃𝑀
 𝜃𝑀
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 9

3.5 Catboost
It has been observed that, CatBoost [14] may be more efficient when applied to dataset that comprises 
a huge number of categorical values having large cardinality in addition to numerical attributes. The 
name, CatBoost, is a mixture of the terms "Category" and "Boosting", which is a Yandex-developed 
open source ML technique that effectively manages categorical attributes and outdoes previous 
publicly available gradient boosting methods in terms of performance [50]. As given in [39] learning 
and scoring methods are implemented on the GPU and CPU respectively, making the library 
significantly faster than previous gradient boosting libraries. The ability to operate with both 
numerical, category, and text data, as well as GPU support and visualisation choices, distinguishes 
this approach from others It has numerous benefits:

A novel approach is built in to treat category attributes as numerical characteristics automatically.

It employs a blend of category attributes that capitalise on feature linkages, considerably 
enhancing feature dimensions.

To prevent overfitting and increase the algorithm's accuracy and generalizability, a balanced tree 
model has been used [38].
4.
Proposed Model
This paper proposed an ensemble learning based classification method known as EnLFADE for the 
detection of fraudulent transactions over the Ethereum blockchain. The various components of the 
model have been presented in Figure 3. It consists of four different functional components – data 
collection, data pre-processing, model building & training and model validation & evaluation. These 
components have been presented in detail in the following subsections.
Figure 3: EnLFADE- Proposed Ethereum fake account detection model.
4.1. Dataset
The supervised Ethereum dataset has been collected from [3, 22, 44], containing 9841 transactions: 
7662 normal transactions (77.9%) and 2179 fraudulent ones (22.1%). It consists of 51 attributes and is 
a two-class problem with class label ‘genuine account’ and ‘fake account’ respectively. The genuine 
account class describes an account with legal and normal transactions, whereas, illicit account class 
specifies an account with fraudulent and fake transactions. The dataset displays rows of recognised 
illegal and legal transactions built over Ethereum network. Table 1 gives the details of the dataset 
used in this work.
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 10

Table 1: Details of Ethereum dataset
Dataset
No. of 
samples
Output 
classes
Input 
attribute
Output 
attribute
Least 
important 
attributes
Total no. 
of 
attributes
Ethereum 
dataset
9841
2
50
1
17
33
Extracted dataset contains some duplicate features and a few having variance 0. Hence, 17 out of 51 
unwanted attributes have been dropped as they will not contribute significantly in the performance of 
the model. Remaining 34 attributes are retained for further analysis. Details of the same has been 
discussed in the section 4.3.  
       
4.2 Data pre-processing
On performing Exploratory Data Analysis (EDA), it is observed that data requires cleaning, balancing 
and scaling. After dropping null and duplicate values, 8739 data instances were left for further 
experimentation. As shown in Figure 4, the target class label is not equally distributed leading to 
imbalanced dataset. In case of imbalanced dataset, the model is trained mainly on the majority class 
and it becomes biased towards the majority class prediction. In this study, SMOTE [8, 32] has been 
used for managing the problem of class imbalance. This method produces new data samples of the 
illicit account class by emulating prevailing minority samples (i.e. illicit account) and making minor 
changes internally. The usage of SMOTE found that the number of samples for both the classes were 
same. Moving forward, in order to handle highly varying magnitudes, it is important to perform 
feature scaling on the data. Without scaling features, the algorithm may be biased towards the features 
which have higher magnitudes. In this study, standard scaler method has been used. It's a technique 
for regulating the data's autonomous features within a given range.   
87%
13%
genuine 
accounts
illicit 
accounts
Figure 4: Imbalanced Ethereum dataset
4.3 Feature selection
Feature selection not only removes the unwanted features but also helps in finding the most effective 
discriminator in the classification problem. It further helps in improving performances, achieving 
higher accuracies and decreasing models’ logical errors. In this paper, Pearson Correlation Coefficient 
[35] has been applied to choose the most crucial features. It is a statistical number that highlights the 
dependency between two features and is measured using the following formula: 
                          
                                                             (14)
𝜌𝑥,𝑦=
cov(𝑥,𝑦)
𝜎𝑥.𝜎𝑦=
𝐸(𝑥𝑦) ‒ 𝐸(𝑥)𝐸(𝑦)
𝐸(𝑥2) ‒ 𝐸2(𝑥). 𝐸(𝑦2) ‒ 𝐸2(𝑦)
where, cov (x, y) implies covariance. Further, 
 depicts the product of vector standard deviation 
.
x
y

and 
. Stronger positive correlation and stronger negative correlation is shown by 
𝜌𝑥,𝑦∈{ ‒ 1, + 1}
value close to +1 and -1 respectively. Figure 5 displays the heatmap of the correlation matrix of 33 
features used in this study. 
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 11

Figure 5:   Correlation heat map of 33 features
As observed from Figure 5, few features were highly correlated, resulting in exclusion of 13 features 
using heuristic correlation threshold value of 0.65. Hence, the feature set consisting 33 features has 
been reduced to 20 independent features. The feature selection step proceeds further by computing the 
ranking of retained features using Mutual Information (MI). The MI between X (feature) and Y 
(target) lies between 0 and 1, which measures the dependency between the variables. Its mathematical 
equation is as follows:
                                                   Info (X; Y) = V(X) – V (X | Y)                                                        (15)
where Info (X; Y) implies MI for X and Y, V(X) is the entropy for X and V (X | Y) depicts 
conditional entropy for X given Y. Features having higher MI value are considered as the most 
discriminating ones.
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 12

0.452665
0.43248
0.356885
0.311079
0.273819
0.270527
0.225904
0.224311
0.208749
0.181997
0.170346
0.168413
0.160561
0.136216
0.129529
0.12472
0.112813
0.059499
0.027314
0
0
0.1
0.2
0.3
0.4
0.5
 Total ERC20 tnxs                     
 ERC20 uniq rec contract addr       
Received Tnx                         
Time Diff between first and...
Sent tnx                             
 ERC20 min val rec                
 ERC20 total Ether received            
min value received                   
Avg min between received tnx         
avg val received                      
max val sent                         
total Ether sent                      
max value received                   
avg val sent                          
min val sent                         
total ether balance                   
Avg min between sent tnx             
Number of Created Contracts          
 ERC20 total ether sent                
 ERC20 total Ether sent contract        
FEATURE IMPORTANCE
                           Figure 6: The ranking of top 20 features based on Mutual Information
4.4 Model learning and classification
In the initial phase of the experiment, classification of data has been achieved using five individual 
classifiers. Further, to achieve better classification accuracy, five different bagging and boosting 
ensemble classifiers are applied. List of the same are shown in the Figure 7.
                    
Decision Trees
KNN
Logistic Regression
SVM
Naive Bayes
Individual 
Classifiers
Catboost
Xgboost
Light Gbm
Adaboost
Random Forest
Ensemble 
Classifiers
Figure 7: Individual and ensemble classifiers
4.5 Hyper parameter tuning
Top-level parameters useful for configuring a Machine Learning based model are known as hyper 
parameters. An efficient strategy for selecting the set of optimal hyper parameter values for a learning 
algorithm in order to have the best modelling output is known as optimization or hyper parameter 
tuning. In line with [40, 41, 34], description of various hyper parameters that have been tuned in the 
proposed work are given as follows:

base_estimator: It is the base learner from which the boosted ensemble is built.

n_estimator: The maximum number of trees to train sequentially 

random_state: It is the integral value which controls the random seed given at each base 
estimator at each iteration.

max_depth: It is defined as maximum depth of the tree. It limits the complexity and depth of the 
trees.

criterion: It checks the quality of the split, e.g. Gini, entropy etc.

min_sample_split: The minimum number of samples required to split an internal node

max_features: The number of features required for the best split

min_child_samples: Minimum samples required in the child leaf.
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 13


learning_rate: It is considered as crucial parameter that controls the rate or speed at which model 
learns and is also defined as the weight applied to each classifier at each boosting iteration. Also 
known as shrinkage. 

num_leaves: It is the maximum number of leaves per tree. 

subsample: The subsampling rate for the size of the random samples.
4.6 Performance evaluation
This study contains several evaluation metrics including confusion matrix, accuracy, recall, 
specificity, precision, F1 score and log loss. These precise criteria are compared to reveal the most 
effective classifier used in this work. 

Confusion matrix: A 2 x 2 matrix used to determine the link between the model's expected and 
actual value. 
                                       

Accuracy: It is defined as occurrence of correct predictions w.r.t. all the available examples being 
tested. The accuracy metric calculates the percentage of cases that are successfully classified. 
                                                   Accuracy = 
                                                                
𝑇𝑃+ 𝑇𝑁
𝑇𝑃+ 𝐹𝑃+ 𝑇𝑁+ 𝐹𝑁
(16) 

Sensitivity (Recall): It is described as the proportion of genuine positives (fake accounts) to all 
actual positives.                            
                                                   Sensitivity 
= 
                           
𝑇𝑃
𝑇𝑃+ 𝐹𝑁
(17)

Specificity: It is the fraction of negative class (i.e. genuine accounts) got correctly classified. 
                                                    Specificity = 
                                                                         
 
𝑇𝑁
𝑇𝑁+ 𝐹𝑃
(18)                                 

Precision: It determines positive class measurement (i.e. illicit accounts) that are being truly 
acknowledged by definite classifier besides demonstrating the definite propriety.
                                                    Precision = 
                                                                            
𝑇𝑃
𝑇𝑃+ 𝐹𝑃
(19)

F1 score: The 
 coefficient helps in assessing the predictive effectiveness of the model based 
F
on the outcomes from both Recall and Precision. It is defined as:
                                          
 , where x is precision, and y is recall.                               (20)
𝐹𝛽=
(1 + 𝛽2) 𝑥𝑦
(𝛽2𝑥) + 𝑦
                                       ∴ 
                                                                     (21)
𝐹1 =
2.𝑝𝑟𝑒𝑐𝑖𝑠𝑖𝑜𝑛.𝑟𝑒𝑐𝑎𝑙𝑙
𝑝𝑟𝑒𝑐𝑖𝑠𝑖𝑜𝑛+ 𝑟𝑒𝑐𝑎𝑙𝑙=  
2𝑥𝑦
𝑥+ 𝑦
      

Log Loss:
Log-loss, or logarithmic loss, tells about the minute information of ML classifier. As stated in 
[45], “Log-loss is a ‘soft’ measurement of accuracy that incorporates this idea of probabilistic 
confidence”. Hence, the binary classifier’s Log-loss is:
                                    Log-loss = 
                             (22)
‒
1
𝑁∑𝑁
𝑖= 1𝑦𝑖log  𝑏𝑖+ (1 ‒ 𝑙𝑖)log(1 ‒ 𝑏𝑖)
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 14

where
 depicts the probability that the ith instance belongs to class 1, as judged by the classifier. 
 𝑏𝑖
 which depicts the true label. Log-loss is the cross entropy between the distribution of the 
𝑙𝑖𝜖{0,1}
true labels and the predictions. Thus, lesser the value of Log loss or cross entropy, more accurate 
the classifier is.
5.
Experimental and Evaluation Results
The findings of the proposed machine learning-based methodology in effectively detecting 
illegitimate accounts are summarised in this section. During the experimental phase, total six major 
observations have been evaluated as shown in the following subsections:
Observation 1: As previously stated, the dataset was initially imbalanced, and SMOTE has been used 
to balance it in order to improve accuracy and reduce model bias. Table 2 compares different ML 
classifiers trained on a balanced dataset versus an imbalanced dataset, both having 33 features. The 
accuracy metric is ineffective in the imbalanced data situation since the classifier can still achieve 
higher accuracy if it predicts all instances as negative. As a result, F1 score has been computed instead 
of accuracy in this table because it provides a more comprehensive picture of the classifiers’ 
performance.
                       Table 2: Comparison of F1scores on imbalanced and balanced dataset
Classifiers
Class 
label 
0(normal) 
1(fraud)
Imbalanced 
dataset 
(33 features) 
Balanced 
dataset
(33 
features)
Classifiers
Class 
label 
0(normal) 
1(fraud)
Imbalanced 
dataset (33 
features) 
Balanced 
dataset
(33 
features)
0
.99
.99
0
.99
.97
1
Catboost
1
.95
.99
6
Decision 
trees
1
.88
.97
0
.99
.99
0
.94
.96
2
Xgboost
1
.94
.99
7
KNN
1
.57
.96
0
.99
.99
0
.94
.68
3
Light Gbm
1
.96
.99
8
Logistic 
Regression
1
.03
.78
0
.99
.99
0
.94
.83
4
Adaboost
1
.94
.99
9
Svm
1
0
.87
0
.99
.99
0
.94
.31
5
Random 
forest
1
.94
.99
10
Naïve 
bayes
1
0
.71
From Table 2, it can be concluded that the balanced dataset provides better and unbiased results. So 
the balanced data was randomly divided into two parts, 80% being used for model training and 20% 
for model testing. 
Observation 2: Table 3 and Figure 8 and 9 illustrate the comparison of performances for all 
classification algorithms applied on the balanced Ethereum dataset with 20 selective features 
containing 12211 samples from the perspective of Accuracy, Precision, Recall, F1 score, Specificity 
and Log loss.
Table 3: Performance comparison of various classifiers on Ethereum dataset
Classifiers
Accuracy
( in % )
Precision
Recall
(senstivity)
F1
score
Specificity
Log 
loss
1
Catboost
99.12
.99
.99
.99
.99
.31
2
Xgboost
99.18
.99
.99
.99
.99
.28
3
LightGbm
99.2
.99
.99
.99
.98
.25
4
Adaboost
98.8
.98
.99
.99
.98
.41
5
Ensemble
Classifiers
Random Forest
98.9
.98
.99 
.99
.98
.4
6
Decision Trees
97.1
.97
.97
.97
.97
.9
7
Knn
95.1
.93
.97
.95
.93
1.6
8
Individual 
Classifiers
Logistic 
Regression
73.6
.69
.88
.77
.57
9.1
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 15

9
Svm
82.2
.77
.92
.84
.71
6.1
10
Naïve Bayes
59.8
.56
.9
.71
.19
13.8
                 
CATBOOST
XGBOOST
LIGHT GBM
ADABOOST
RANDOM FOREST
DECISION TREES
KNN
LOGISTIC REGRESSION
SVM
NAÏVE BAYES
60
70
80
90
100
ACCURACY ( in %)
    
  Figure 8: Accuracy (in %) of different 
classifiers
CATBOOST
XGBOOST
LIGHT GBM
ADABOOST
RANDOM FOREST
DECISION TREES
KNN
LOGISTIC REGRESSION
SVM
NAÏVE BAYES
0.88
0.90
0.92
0.94
0.96
0.98
1.00
 SENSITIVITY
 SPECIFICITY
 F1 SCORE
0.2
0.4
0.6
0.8
1.0
0.70
0.75
0.80
0.85
0.90
0.95
1.00
 Figure 9: Sensitivity, Specificity, F1 score of 
different classifiers 
From Table 3, Figure 8 and 9, it can be observed that ensemble classifiers - Catboost, Adaboost, 
Xgboost, LightGbm and Random Forest are performing better than the individual classifiers. The 
parameter setting of ensemble classifiers is illustrated in Table 4.                
Table 4: Parameter setting of Ensemble Classifiers
Adaboost
Parameters
Default Values
Optimal Values
Algorithm
‘SAMME.R’
‘SAMME.R’
Base 
Estimator
none
Random 
Forest 
Classifier
Learning Rate
1
0.01
N Estimators
50
100
Random State
none
96
LightGbm
Parameters 
Default 
Values
Optimal 
Values
Boosting type
‘gbdt’
‘gbdt’
Number of leaves
31
31
Max depth
-1
-1
Learning rate
0.1
0.2
N estimators
100
100
Min child samples
30
20
                               Catboost
Parameters
Default Values
Optimal 
Values
Learning rate
0.03
0.2
Max depth
6
8
Leaf estimation 
iterations
none
10
N estimators
500
300
                         Random Forest
Parameters
Default 
Values
Optimal
Values
Criterion
‘gini’
‘gini’
Min samples split
2
3
Max features
‘auto’
‘auto’
Random state
None
10
                              Xgboost
Parameters
Default Values
Optimal 
Values
Learning rate
0.1
0.1
Max features
‘auto’
‘auto’
Max depth
3
8
N estimators
100
300
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 16

Observation 3: Figure 10 illustrates confusion matrices of different 10 ML classifiers.
Figure 10(a) LightGbm
         Figure 10(b) Catboost
        Figure 10(c) Adaboost
Figure 10(d) Random Forest
      Figure 10(e) Xgboost
           Figure 10(f) KNN
      Figure10 (g) Decision Trees                        Figure 10(h) Naïve Bayes
              Figure 10(i) SVM
Figure 10(j) Logistic Regression
Figure 10: Confusion matrices for (a) LightGbm (b) Catboost (c) Adaboost (d) Random Forest
(e) Xgboost (f) KNN (g) Decision Trees (h) Naïve Bayes (i) SVM (j) Logistic Regression
Observation 4: Table 5 and Figure 11 show the FN, FP, TP and TN score of different classifiers 
obtained from confusion matrices shown in Figure 10. The aim of an efficient model is to maximize 
TP, TN and minimize FN, FP. Also, in case of illicit account detection problem, if a fraudulent 
transaction goes undetected then it will incur a huge loss. Thus, focus should be to minimize FN.
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 17

  
CATBOOST
XGBOOST
LIGHT GBM
ADABOOST
RANDOM FOREST
DECISION TREES
KNN
LOGISTIC REGRESSION
SVM
NAÏVE BAYES
0
200
400
600
800
1000
1200
1400
1600
 FN
 FP
 TP
 TN
  
  Figure 11: FN, FP, TP and TN score of different classifiers.
     Table 5: FN, FP, TP and TN score of 
     different classifiers
FN
FP
TP
TN
Catboost
10
17
1573
1453
Xgboost
6
19
1577
1451
LightGbm
5
17
1578
1453
Adaboost
11
25
1572
1445
Random 
Forest
9
26
1574
1444
Decision 
Trees
35
51
1548
1419
Knn
47
102
1536
1368
Logistic 
Regression
183
622
1400
848
Svm
121
422
1462
1048
Naïve 
Bayes
36
1192
1547
278
5.5 Observation 5: Figure 12 showcases the ROC curve and AUC score for different classification 
algorithms used in this study. 
Figure 12: ROC curves for the different algorithms
The aforementioned results reveal that individual classifiers do not provide satisfactory results, but 
ensemble techniques perform remarkably on Ethereum illegal account detection with 99 % accuracy, 
which is the highest so far among other research works as per our best knowledge.
                        
Observation 6: Further comparative analysis of ensemble classifiers has been presented in Table 6, 
Figure 13, 14 and 15, to rank the best ensemble classifier.
Table 6: Performance comparison of developed ensemble techniques
Parameters 
& Rank
Ensemble Techniques 
Catboost
Xgboost
LightGbm
Adaboost
Random
Forest
Accuracy
Rank
99.12
3
99.18
2
99.2
1
98.8
5
98.9
4
FN Count
Rank
10
4
6
2
5
1
11
5
9
3
Log Loss 
Value
Rank
.31
  3
.28
  2
.25
  1
.41
  5
.4
 4
Observed
Overall 
Rank
3
2
1
5
4
   
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 18

5
6
9
10
11
LIGHT 
GBM
XGBOOST
RANDOM 
FOREST
CATBOOST
ADABOOST
0
10
FALSE NEGATIVE (FN)
99.2
99.18
99.12
98.9
98.8
LIGHT 
GBM
XGBOOST
CATBOOST
RANDOM 
FOREST
ADABOOST
98.5
99.5
ACCURACY ( in % )
0.25
0.28
0.31
0.4
0.41
LIGHT 
GBM
XGBOOST
CATBOOS...
RANDOM 
FOREST
ADABOOS...
0
0.4
LOG LOSS
Figure 13
Figure 14
Figure 15
Thus, it can be observed from the aforementioned Table 6 that LightGbm (with accuracy=99.2%) 
outperforms other ensemble classifiers followed by Xgboost (99.18%), Catboost (99.12%), Random 
Forests (98.9%) and Adaboost (98.8%).
6.
Conclusion and Future Work
In this paper, classification model for detection of illicit accounts over Ethereum networks named as 
EnLFADE has been presented using ensemble learning advances like Catboost, Xgboost, Adaboost, 
LightGbm, Random forest and some individual classifiers like Naïve Bayes, SVM, KNN, Decision 
Trees and Logistic Regression. Extracted Kaggle-based Ethereum dataset was initially imbalanced 
and further it has been balanced using SMOTE in order to achieve an unbiased model. Feature 
selection played an important role and 20 crucial independent features have been retained out of 33 
using correlation analysis. The performances of trained classifiers are evaluated using various 
evaluation metrics. Results indicate that the ensemble techniques with accuracy approximately 99% 
provide better outcomes in comparison to individual classifiers. Also, it has been concluded that 
among the ten aforementioned ML approaches, LightGbm based model with 99.2% accuracy is the 
best suited for precise detection of the illicit accounts. Extending the outcome of this learning to 
identify phishing scams over Ethereum network could be an interesting study in this field of research.
References
[1] Xia, P., Wang, H., Zhang, B., Ji, R., Gao, B., Wu, L., ... & Xu, G. (2020). Characterizing 
cryptocurrency exchange scams. Computers & Security, 98, 101993.
[2] Ostapowicz, M., & Żbikowski, K. (2020, January). Detecting fraudulent accounts on blockchain: a 
supervised approach. In International Conference on Web Information Systems Engineering (pp. 18-
31). Springer, Cham.
[3] Farrugia, S., Ellul, J., & Azzopardi, G. (2020). Detection of illicit accounts over the Ethereum 
blockchain. Expert Systems with Applications, 150, 113318.
[4] Yuan, Q., Huang, B., Zhang, J., Wu, J., Zhang, H., & Zhang, X. (2020, October). Detecting 
phishing scams on ethereum based on transaction records. In 2020 IEEE International Symposium on 
Circuits and Systems (ISCAS) (pp. 1-5). IEEE.
[5] Bian, S., Deng, Z., Li, F., Monroe, W., Shi, P., Sun, Z., ... & Li, J. (2018). Icorating: A deep-
learning system for scam ico identification. arXiv preprint arXiv:1803.03670.
[6] Chen, L., Peng, J., Liu, Y., Li, J., Xie, F., & Zheng, Z. (2020). Phishing scams detection in 
ethereum transaction network. ACM Transactions on Internet Technology (TOIT), 21(1), 1-16.
[7] Issac, A. C., & Baral, R. (2020). A trustworthy network or a technologically disguised scam: A 
biblio-morphological analysis of bitcoin and blockchain literature. Global Knowledge, Memory and 
Communication. 
[8] Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). SMOTE: synthetic 
minority over-sampling technique. Journal of artificial intelligence research, 16, 321-357.
[9] Friedman, N., Geiger, D., & Goldszmidt, M. (1997). Bayesian network classifiers. Machine 
learning, 29(2), 131-163.
[10] Quinlan, J. R. (1986). Induction of decision trees. Machine learning, 1(1), 81-106.
[11] Cortes, C., & Vapnik, V. (1995). Support-vector networks. Machine learning, 20(3), 273-297
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 19

[12] Cover, T., & Hart, P. (1967). Nearest neighbor pattern classification. IEEE transactions on 
information theory, 13(1), 21-27.
[13] Hosmer Jr, D. W., Lemeshow, S., & Sturdivant, R. X. (2013). Applied logistic regression (Vol. 
398). John Wiley & Sons.
[14] Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A. (2018). CatBoost: 
unbiased boosting with categorical features. Advances in neural information processing systems, 31.
[15] Freund, Y., & Schapire, R. E. (1997). A decision-theoretic generalization of on-line learning and 
an application to boosting. Journal of computer and system sciences, 55(1), 119-139.
[16] Chen, T., & Guestrin, C. (2016, August). Xgboost: A scalable tree boosting system. 
In Proceedings of the 22nd acm sigkdd international conference on knowledge discovery and data 
mining (pp. 785-794).
[17] Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., ... & Liu, T. Y. (2017). Lightgbm: A 
highly efficient gradient boosting decision tree. Advances in neural information processing 
systems, 30.
[18] Breiman, L. (2001). Random forests. Machine learning, 45 (1), 5-32.
[19] Sun Yin, H. H., Langenheldt, K., Harlev, M., Mukkamala, R. R., & Vatrapu, R. (2019). 
Regulating cryptocurrencies: a supervised machine learning approach to de-anonymizing the bitcoin 
blockchain. Journal of Management Information Systems, 36 (1), 37-73.
[20] Pham, T., & Lee, S. (2016). Anomaly detection in bitcoin network using unsupervised learning 
methods. arXiv preprint arXiv:1611.03941.
[21] Sayadi, S., Rejeb, S. B., & Choukair, Z. (2019, June). Anomaly detection model over blockchain 
electronic transactions. In 2019 15th International Wireless Communications & Mobile Computing 
Conference (IWCMC) (pp. 895-900). IEEE.
[22] Ibrahim, R. F., Elian, A. M., & Ababneh, M. (2021, July). Illicit Account Detection in the 
Ethereum Blockchain Using Machine Learning. In 2021 International Conference on Information 
Technology (ICIT) (pp. 488-493). IEEE.
[23] Chen, W., Guo, X., Chen, Z., Zheng, Z., & Lu, Y. (2020, July). Phishing Scam Detection on 
Ethereum: Towards Financial Security for Blockchain Ecosystem. In IJCAI (pp. 4506-4512).
[24] Alam, M. N., Sarma, D., Lima, F. F., Saha, I., & Hossain, S. (2020, August). Phishing attacks 
detection using machine learning approach. In 2020 third international conference on smart systems 
and inventive technology (ICSSIT) (pp. 1173-1179). IEEE.
[25] Lašas, K., Kasputytė, G., Užupytė, R., & Krilavičius, T. (2020). Fraudulent behaviour 
identification in ethereum blockchain. In CEUR Workshop Proceedings [Electronic Resource]: IVUS 
2020, Information Society and University Studies, Kaunas, Lithuania, 23 April, 2020: Proceedings. 
Aachen: CEUR-WS (Vol. 2698).
[26] Sun, J., Jia, M. Y., & Li, H. (2011). AdaBoost ensemble for financial distress prediction: An 
empirical 
comparison 
with 
data 
from 
Chinese 
listed 
companies. Expert 
systems 
with 
applications, 38(8), 9305-9312
[27] Dev, V. A., & Eden, M. R. (2019). Formation lithology classification using scalable gradient 
boosted decision trees. Computers & chemical engineering, 128, 392-404.
[28] Kotsiantis, S. B. (2014). Bagging and boosting variants for handling classifications problems: a 
survey. The Knowledge Engineering Review, 29(1), 78-100.
[29] Mayr, A., Binder, H., Gefeller, O., & Schmid, M. (2014). The evolution of boosting 
algorithms. Methods of information in medicine, 53(06), 419-427.
[30]  Gu, W. (2014). Application of Boosting Algorithm in Spam Filtration. TELKOMNIKA 
Indonesian Journal of Electrical Engineering, 12(7), 5685-5692.
[31] Jhaveri, S., Khedkar, I., Kantharia, Y., & Jaswal, S. (2019, March). Success prediction using 
random forest, catboost, xgboost and adaboost for kickstarter campaigns. In 2019 3rd International 
Conference on Computing Methodologies and Communication (ICCMC) (pp. 1170-1173). IEEE.
[32] Khan, N. I., Mahmud, T., Islam, M. N., & Mustafina, S. N. (2020, November). Prediction of 
cesarean childbirth using ensemble machine learning methods. In Proceedings of the 22nd 
international conference on information integration and web-based applications & services (pp. 331-
339).
[33] Cutler, A., Cutler, D. R., & Stevens, J. R. (2012). Random forests. In Ensemble machine 
learning (pp. 157-175). Springer, Boston, MA.
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


## Page 20

[34] Bentéjac, C., Csörgő, A., & Martínez-Muñoz, G. (2021). A comparative analysis of gradient 
boosting algorithms. Artificial Intelligence Review, 54(3), 1937-1967.
[35] Mo, H., Sun, H., Liu, J., & Wei, S. (2019). Developing window behavior models for residential 
buildings using XGBoost algorithm. Energy and Buildings, 205, 109564.
[36] Liang, W., Luo, S., Zhao, G., & Wu, H. (2020). Predicting hard rock pillar stability using GBDT, 
XGBoost, and LightGBM algorithms. Mathematics, 8(5), 765.
[37] Wang, D., Zhang, Y., & Zhao, Y. (2017, October). LightGBM: an effective miRNA 
classification method in breast cancer patients. In Proceedings of the 2017 International Conference 
on Computational Biology and Bioinformatics (pp. 7-11).
[38] Luo, M., Wang, Y., Xie, Y., Zhou, L., Qiao, J., Qiu, S., & Sun, Y. (2021). Combination of 
feature selection and catboost for prediction: The first application to the estimation of aboveground 
biomass. Forests, 12(2), 216.
[39] Dorogush, A. V., Ershov, V., & Gulin, A. (2018). CatBoost: gradient boosting with categorical 
features support. arXiv preprint arXiv:1810.11363.
[40] Isabona, J., Imoize, A. L., & Kim, Y. (2022). Machine Learning-Based Boosted Regression 
Ensemble Combined with Hyperparameter Tuning for Optimal Adaptive Learning. Sensors, 22(10), 
3776.
[41] Yang, L., & Shami, A. (2020). On hyperparameter optimization of machine learning algorithms: 
Theory and practice. Neurocomputing, 415, 295-316.
[42] Mohammed, Mohammed A., Suhad M. Kadhem, and A. Ali Maisa'a. "Insider Attacker Detection 
Based On Body Language and Technical Behavior Using Light Gradient Boosting Machine 
(LightGBM)." Tech-Knowledge 1.1 (2021): 48-66.
[43] Asselman, A., Khaldi, M., & Aammou, S. (2021). Enhancing the prediction of student 
performance based on the machine learning XGBoost algorithm. Interactive Learning Environments, 
1-20.
[44] https://www.kaggle.com/vagifa/ethereum-frauddetection-dataset.
[45] https://www.oreilly.com/data/free/files/evaluating-machine-learning-models.pdf
[46] https://www.simplilearn.com/tutorials/blockchain-tutorial/what-is-cryptocurrency
[47] https://www.businessinsider.com/personal-finance/what-is-ethereum?IR=T
[48]https://tech.hindustantimes.com/how-to/beware-of-cryptocurrency-frauds-bitcoin-ethereum-
scams-hit-delhi-maha-know-how-to-avoid-71641194570992.html
[49] https://money.com/what-is-ethereum/
[50]https://www.researchgate.net/project/TURKISH-FAKE-NEWS-DETECTION-WITH-
BOOSTING-ALGORITHMS
       
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=4180768
Preprint not peer reviewed


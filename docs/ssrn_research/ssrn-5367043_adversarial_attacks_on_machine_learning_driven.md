# Adversarial Attacks on Machine Learning-Driven

- **Source File**: `ssrn-5367043.pdf`
- **Total Pages**: 17
- **SSRN ID**: `ssrn-5367043`

---

## Page 1

1
Adversarial Attacks on Machine Learning-Driven 
High-Frequency Trading Models
Hajime Shimaoa, Kanis Saengchoteb,*, Kamabir Chakrabortya, 
Chengfei Wanga, Warut Khern-am-nuaic
ABSTRACT
Machine learning (ML) has become central to high-frequency trading 
(HFT), yet the vulnerability of these complex models to adversarial manipulation 
presents a significant, under-explored risk to market integrity. This paper examines 
how small, strategically crafted perturbations to limit order book (LOB) data can 
compromise the performance of widely used ML models. Using standardized 
white-box attack methods (FGSM, PGD) on the public FI-2010 dataset, we 
benchmark the adversarial robustness of LSTM, CNN, and the hybrid DeepLOB 
architecture. We find that imperceptibly small input perturbations significantly 
reduce predictive accuracy and signal quality, leading to erroneous trades and 
missed alpha, especially in CNN and DeepLOB. Our results reveal an accuracy-
robustness trade-off, where the model most accurate in benign conditions is the 
most fragile under attack. These findings underscore robustness as a pillar of 
trustworthy AI in finance, expose a significant security gap in automated financial 
systems, and highlight the need for security-aware model design in modern trading 
infrastructure.
Keywords: high-frequency trading, adversarial machine learning, limit order book, 
market stability, financial cybersecurity, trustworthy AI
a Engineering Division, Penn State Great Valley
b Chulalongkorn Business School, Chulalongkorn University
c Desautels Faculty of Management, McGill University
* Please send correspondences to Kanis Saengchote (email: kanis@cbs.chula.ac.th). 
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


## Page 2

1
Adversarial Attacks on Machine Learning-Driven 
High-Frequency Trading Models
ABSTRACT
Machine learning (ML) has become central to high-frequency trading 
(HFT), yet the vulnerability of these complex models to adversarial manipulation 
presents a significant, under-explored risk to market integrity. This paper examines 
how small, strategically crafted perturbations to limit order book (LOB) data can 
compromise the performance of widely used ML models. Using standardized 
white-box attack methods (FGSM, PGD) on the public FI-2010 dataset, we 
benchmark the adversarial robustness of LSTM, CNN, and the hybrid DeepLOB 
architecture. We find that imperceptibly small input perturbations significantly 
reduce predictive accuracy and signal quality, leading to erroneous trades and 
missed alpha, especially in CNN and DeepLOB. Our results reveal an accuracy-
robustness trade-off, where the model most accurate in benign conditions is the 
most fragile under attack. These findings underscore robustness as a pillar of 
trustworthy AI in finance, expose a significant security gap in automated financial 
systems, and highlight the need for security-aware model design in modern trading 
infrastructure.
Keywords: high-frequency trading, adversarial machine learning, limit order book, 
market stability, financial cybersecurity, trustworthy AI
 
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


## Page 3

2
1.
Introduction
Over the past decade, financial markets have undergone significant transformation with 
the integration of high-frequency trading (HFT) and machine learning (ML). Modern algorithmic 
systems are now capable of processing vast streams of market data and execute millions of trades 
per second, contributing to increased market liquidity and price discovery (Brogaard, 
Hendershott, and Riordan, 2014; Korajczyk and Murphy, 2019). However, this growing reliance 
on automation also introduces novel cybersecurity risks. The ML models at the heart of these 
HFT systems, while powerful, are susceptible to adversarial manipulation—a vulnerability that 
has been well-documented in domains such as computer vision (Goodfellow et al., 2015; 
Kurakin et al., 2018) but remains underexplored in finance, where errors can propagate rapidly 
and distort market signals (e.g., the Flash Crash, Kirilenko et al., 2017).
Adversarial attacks involve making small, often imperceptible, perturbations to a model’s 
input to cause misclassification or erroneous prediction (Szegedy et al., 2014; Goodfellow et al., 
2015; Kurakin et al., 2018). When applied to HFT, this technique constitutes a new and 
sophisticated form of market manipulation. By strategically placing or canceling small orders, a 
malicious actor could subtly alter the state of the limit order book (LOB)—a primary input for 
many HFT models—and trick a model into executing suboptimal trades, potentially triggering 
significant losses or market instability.
This paper examines the susceptibility of HFT models to such adversarial threats. While 
prior work has explored adversarial attacks in trading using custom simulations (Goldblum et al., 
2021), our study is the first to evaluate the robustness of widely used deep learning architectures, 
including LSTM, CNN, and the hybrid DeepLOB, against standardized adversarial attacks 
methods such as FGSM and PGD. We demonstrate that even generic, non-domain-specific 
attacks can cause severe performance degradation in terms of predictive accuracy, precision 
(signal quality), and recall (opportunity capture). Our findings highlight a critical gap in the 
security practices surrounding financial ML and provide a replicable framework for stress-testing 
the models that increasingly drive modern market operations. By exposing how adversarial 
vulnerabilities undermine reliability in financial ML systems, our work contributes to the broader 
goal of trustworthy AI—ensuring that AI systems are transparent, robust, secure, and ethical in 
high-stakes applications (Li et al., 2023). Enhancing adversarial resilience is a key step toward 
building AI systems that can be trusted for real-world financial decision-making.
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


## Page 4

3
2.
Machine Learning Models and Limit Order Book Data
ML has transformed HFT by enabling trading firms to analyze large volumes of market 
data, recognize patterns, and execute trades with minimal latency. Among the most used ML 
models in HFT are deep learning architectures that process limit order book (LOB) data to 
predict short-term price movements and optimize trade execution. The LOB data is the supply 
and demand for securities observable to market participants, displaying bid and ask prices along 
with order volumes. ML models such as Long Short-Term Memory (LSTM) networks (Dixon, 
2018), Convolutional Neural Networks (CNNs) (Tsantekidis et al., 2017), and DeepLOB (Zhang 
et al., 2019) leverage LOB data to generate trading signals (neutral, up, or down). These models 
analyze historical and real-time order book changes, identifying trends and liquidity dynamics to 
inform trade execution strategies. While ML models mostly operate as black boxes, the three 
models’ trading strategies can be motivated as follows. LSTM has “memory,” so it looks for 
sustained order flow imbalances and detects momentum shifts based on short- and long-term 
dependencies. CNN emphasizes “spatial patterns,” such as the shape of the order book, for 
example, liquidity walls, slopes, contours, and spread tightness. Finally, DeepLOB combines the 
architectures of LSTM and CNN, making it the most complex.
The most widely used dataset among academics is the FI-2010 dataset (Ntakaris et al., 
2018), which provides normalized LOB data from the ITCH feed of the NASDAQ OMX Nordic 
Helsinki exchange for five stocks over ten consecutive trading days (June 1-14, 2010).1 The data 
consists of time-ordered sequences of messages that track and record all the events occurring in 
the market. The first 40 columns represent the top 10 levels of ask and bid prices and volumes, 
while the last 5 columns are the labels for different prediction horizons.
The reliance on LOB data makes ML-driven HFT models susceptible to adversarial 
attacks. Small, strategically placed manipulations of LOB data can mislead trading models, 
resulting in erroneous predictions and suboptimal trades. Empirical studies (e.g., Goldblum et al., 
2021) demonstrate that adversarial perturbations, such as minor alterations in bid-ask volumes in 
this context, can significantly degrade the performance of ML models, reducing their predictive 
1 While the FI-2010 dataset reflects Nordic equity markets in 2010, it remains the most comprehensive and widely 
used publicly available dataset for limit order book research.
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


## Page 5

4
accuracy and increasing trading risks. These vulnerabilities underscore the need for robust model 
defenses against adversarial threats.
Adversarial attacks in the paper are trained using the Fast Gradient Sign Method (FGSM) 
(Goodfellow et al., 2015) and Projected Gradient Descent (PGD) (Madry et al., 2018), which are 
common techniques for generating adversarial examples in machine learning models. FGSM is a 
single-step attack that adds a small perturbation to the input in the direction of the loss function’s 
gradient. It is computationally efficient and represents a rapid, opportunistic attack. PGD is a 
powerful iterative attack that applies smaller perturbations over multiple steps, ensuring the total 
manipulation remains within a predefined budget. It represents a more sophisticated, optimized 
attack. It is important to emphasize that both adversarial attacks require knowledge of the 
model’s specification. This type of attack is often known as a white-box attack (Xu et al., 2020).2 
Details of the ML models and the perturbation methods are in the Appendix.
We apply these attacks to perturb the LOB input data and then evaluate the performance 
of the trained models on this adversarial data without retraining. This experiment simulates a 
real-world scenario where a deployed model encounters unexpected, manipulated market data. 
The framework is visualized in Figure 1.
The steps are as follows: First, the attacker monitors the LOB and observes trading 
patterns. The attacker then identifies key levels where placing small perturbations can maximize 
disruption. Second, the attacker posts a sequence of small limit orders designed to manipulate the 
observed order book. The strategic perturbations influence the ML model’s input data, making it 
misinterpret market conditions. The adversarially perturbed LOB is re-entered into the original 
model, and the model performance from the perturbed LOB is compared to the original LOB. 
We compare (1) prediction accuracy, (2) precision,3 and (3) recall4 across LSTM, CNN, and 
DeepLOB models and various magnitudes of perturbations. 
We also report the average perturbation volume, calculated as the average magnitude of 
changes made to the input data during an adversarial attack. If a model’s performance drops 
2 The technical details are provided in the Appendix. For a survey of deep learning in finance, see, for example, 
Ozbayoglu et al. (2020).
3 Model precision measures how many of the predictions labeled as positive (e.g., a price increase or a trade signal) 
were correct. A drop in precision means the model begins making incorrect trades, increasing financial risk.
4 Model recall measures how well the model identifies actual positive instances from all available positive cases. A 
drop in recall means the model is missing critical trading opportunities.
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


## Page 6

5
significantly with a small perturbation, it indicates a high vulnerability to adversarial 
manipulation.
Figure 1: Research Workflow
The framework consists of three steps. In Step 1, machine learning models (LSTM, CNN, DeepLOB) are trained on 
clean order book data (FI-2010) to forecast short-term price direction as a three-class classification problem (neutral, 
up, or down). Model performance is evaluated using standard metrics: accuracy, precision, and recall. In Step 2, 
adversarial perturbations are generated using gradient-based attack methods (FGSM, PGD) by introducing small but 
deliberate modifications to the original input data. In Step 3, the same trained model is reused without retraining and 
evaluated on the perturbed inputs to assess changes in predictive performance. The difference in evaluation metrics 
between clean and perturbed scenarios quantifies the model’s robustness to adversarial attacks.
3.
Results
Our experiments reveal that all tested HFT models are vulnerable to adversarial attacks, 
though the degree and nature of the vulnerability differ significantly across architectures. 
3.1 Performance Degradation under Attack
First, we note that the baseline performance ranking of our models is consistent with 
prior literature. Tsantekidis et al. (2020), who analyze FOREX order book data, find that CNN 
slightly outperforms LSTM, and a combination of CNN and LSTM (like our DeepLOB) can 
further improve performance. Our results in Table 1 confirm this hierarchy, with DeepLOB and 
CNN achieving the highest baseline accuracies.
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


## Page 7

6
However, this performance hierarchy is fragile. As shown in Table 1 and Figure 2, both 
FGSM and PGD attacks successfully degrade model performance. PGD, the stronger iterative 
attack, causes a more pronounced drop in accuracy even at minuscule perturbation magnitudes (𝜖
). For instance, at 𝜖 = 0.000001, PGD reduces the accuracy of the CNN and DeepLOB models 
from over 76% to just 48%, while FGSM has a negligible impact. Sophisticated, multi-step 
manipulations are far more threatening than simple, one-shot attacks.
An interesting finding relates to the perturbation volume. Under PGD, the average 
volume remains remarkably constant at approximately 2.26 across all 𝜖 levels (Panel D, Table 1). 
The similar volume suggests the attack finds a consistent vulnerability threshold even when 
allowed a much larger budget. In contrast, FGSM (Panel C) exhibits a non-monotonic 
relationship. The required perturbation volume is very small at 𝜖 = 0.001 (0.004) but much larger 
at the smallest 𝜖 = 0.000001 (4.471). The result suggests that the single FGSM step is inefficient 
at extremely small magnitudes, requiring a large but ineffective perturbation, whereas a slightly 
larger 𝜖 allows it to find a much more efficient attack path.
Table 1: Model Accuracy and Average Perturbation Volume Under FGSM and PGD Attacks
This table reports the classification accuracy (%) of three ML models (LSTM, CNN, and DeepLOB) under 
increasing levels of adversarial perturbation with magnitude ε. Panel A shows the model accuracy for the 
Fast Gradient Sign Method (FGSM), and Panel B shows the model accuracies for Projected Gradient 
Descent (PGD). Accuracy is measured on the test set using adversarially perturbed inputs. Baseline refers 
to accuracy on clean, unperturbed data. Panel C and D show the average magnitude of perturbations added 
to input features during FGSM (Panel C) and PGD (Panel D) attacks. Average perturbation volume is 
calculated as the mean absolute change across all perturbed LOB input values per instance, reflecting the 
typical size of input modifications required to degrade model performance.
Panel A: Model Accuracy Under Fast Gradient Sign Method (FGSM)
Model
Baseline
Accuracy
0.000001
0.00001
0.0001
0.001
0.01
0.1
1
10
LSTM
48.62
48.20
48.10
48.15
47.77
44.07
26.80
3.83
3.86
CNN
76.06
74.67
74.62
74.17
69.87
45.38
44.37
41.84
41.84
DeepLOB
77.19
74.33
74.27
73.77
69.76
50.68
40.28
32.34
32.33
Panel B: Model Accuracy Under Projected Gradient Descent (PGD)
Model
Baseline
Accuracy
0.000001
0.00001
0.0001
0.001
0.01
0.1
1
10
LSTM
48.62
39.85
39.85
39.85
39.84
39.84
39.67
36.84
31.00
CNN
76.06
48.02
48.02
48.02
48.02
48.02
47.13
37.65
22.15
DeepLOB
77.19
47.80
47.80
47.80
47.80
47.70
46.00
38.30
22.46
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


## Page 8

7
Panel C: Average Perturbation Volume Under Fast Gradient Sign Method (FGSM)
Model
0.000001
0.00001
0.0001
0.001
0.01
0.1
1
10
LSTM
4.4710
4.4720
0.0004
0.0044
0.0400
0.3282
3.0890
3.0890
CNN
4.4710
4.4710
0.0004
0.0040
0.0400
0.3300
3.0900
3.0900
DeepLOB
4.4710
4.4720
0.0004
0.0044
0.0400
0.3248
3.0520
3.0520
Panel D: Average Perturbation Volume Under Projected Gradient Descent (PGD)
Model
0.000001
0.00001
0.0001
0.001
0.01
0.1
1
10
LSTM
2.2640
2.2640
2.2640
2.2640
2.2640
2.2640
2.2600
2.2700
CNN
2.2640
2.2640
2.2640
2.2640
2.2640
2.2640
2.2600
2.2700
DeepLOB
2.2640
2.2640
2.2640
2.2640
2.2640
2.2640
2.2650
2.2690
Figure 2: Model Accuracy
This figure visualizes the accuracy drop of the three ML models across different perturbation magnitudes. 
Panel A plots performance under FGSM, while Panel B does so for PGD. The x-axis represents the 
perturbation magnitude (ε), and the y-axis shows classification accuracy. 
3A: Fast Gradient Sign Method (FGSM)
3B: Projected Gradient Descent (PGD)
3.2 Degradation of Signal Quality
Beyond simple accuracy, we assess the impact on precision and recall, which measure 
signal quality and opportunity capture, respectively. Table 3 shows that adversarial attacks erode 
both. Lower precision implies a higher rate of false positives (executing bad trades), while lower 
recall implies more false negatives (missing profitable opportunities). Consistent with Table 2, 
LSTM is the least accurate both in low precision and recall, and PGD attacks again cause a more 
severe degradation. For the DeepLOB model, precision falls from a baseline of 78% to 49% 
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


## Page 9

8
under the smallest PGD perturbation, resulting in more than half of its trade signals becoming 
incorrect. The significant decline in precision demonstrates that attacks not only cause models to 
be wrong more often but they degrade the quality of the trading signals they generate.
Compared to prior work that relies on custom-built simulation environments and 
explicitly specified trading constraints (e.g., Goldblum et al., 2021), our use of standard 
FGSM/PGD attacks demonstrates that small, algorithmically generated perturbations are 
sufficient to impair decision quality even without detailed domain-specific constraints.
Table 3: Precision and Recall Under FGSM and PGD Attacks
This table shows the model precision (%) under FGSM (Panel A) and PGD (Panel B), as well as recall 
under FGSM (Panel C) and PGD (Panel D), across increasing ε values. Precision measures the proportion 
of predicted positive classes (e.g., signals to buy or sell) that are correct. In high-frequency trading, lower 
precision translates to a higher rate of false positives, meaning the model is more likely to trigger erroneous 
trades. Recall captures the proportion of actual positive cases (i.e., genuine profitable opportunities) that 
the model correctly identifies as such. A drop in recall indicates that the model is missing signals that should 
have triggered trades, resulting in missed opportunities.
Panel A: Precision Under Fast Gradient Sign Method (FGSM)
Model
Baseline
0.000001
0.00001
0.0001
0.001
0.01
0.1
1
10
LSTM
0.4933
0.4848
0.4848
0.4844
0.4808
0.4561
0.2928
0.1100
0.1100
CNN
0.8233
0.7400
0.7400
0.7400
0.6985
0.4626
0.4200
0.4300
0.4300
DeepLOB
0.7766
0.7422
0.7417
0.7360
0.6963
0.5384
0.5165
0.4156
0.4065
Panel B: Precision Under Projected Gradient Descent (PGD)
Model
Baseline
0.000001
0.00001
0.0001
0.001
0.01
0.1
1
10
LSTM
0.4933
0.4030
0.4030
0.4030
0.4030
0.4030
0.4030
0.3700
0.3244
CNN
0.8233
0.4800
0.4800
0.4800
0.4800
0.4800
0.4700
0.3819
0.1600
DeepLOB
0.7766
0.4866
0.4866
0.4866
0.4866
0.4850
0.4700
0.3900
0.2030
Panel C: Recall Under Fast Gradient Sign Method (FGSM)
Model
Baseline
0.000001
0.00001
0.0001
0.001
0.01
0.1
1
10
LSTM
0.4900
0.4838
0.4838
0.4833
0.4795
0.4440
0.2679
0.0377
0.0380
CNN
0.8100
0.7460
0.7450
0.7410
0.6983
0.4588
0.4400
0.4200
0.4200
DeepLOB
0.7733
0.7424
0.7419
0.7360
0.6969
0.5113
0.4087
0.3308
0.3307
Panel D: Recall Under Projected Gradient Descent (PGD)
Model
Baseline
0.000001
0.00001
0.0001
0.001
0.01
0.1
1
10
LSTM
0.4900
0.4000
0.4000
0.4000
0.4000
0.4000
0.4000
0.3690
0.3110
CNN
0.8100
0.4800
0.4800
0.4800
0.4800
0.4800
0.4700
0.3769
0.2200
DeepLOB
0.7733
0.4790
0.4790
0.4790
0.4790
0.4780
0.4600
0.3800
0.2260
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


## Page 10

9
3.3 The Accuracy-Robustness Trade-Off
Our results show that ML models used in HFT are highly sensitive to even small input 
perturbations, consistent with the broader adversarial ML literature, which often identifies a 
trade-off between a model’s accuracy on clean data and its robustness to attack (Tsipras et al., 
2018). Our best-performing models on clean data, CNN and DeepLOB (with baseline accuracies 
of 76% and 77%), were the most vulnerable to PGD attacks, suggesting that models optimized 
for high performance may learn highly complex and brittle decision boundaries that are easily 
exploited. While Tsantekidis et al. (2020) find that hybrid models can improve predictive 
performance, our contribution is to show that this performance gain may come at the cost of 
increased vulnerability.
The use of precision and recall losses, in addition to accuracy, helps highlight the specific 
types of mistakes that can lead to real-world financial damage. Our approach offers a replicable 
framework for adversarial stress testing, utilizing publicly available data and broadly applicable 
attack algorithms.
4.
Conclusion
This paper examines the vulnerability of common high-frequency trading (HFT) models 
to adversarial attacks, showing that these systems are highly susceptible to small, gradient-based 
input perturbations. This vulnerability manifests as a significant degradation in predictive 
accuracy, precision, and recall, resulting in direct financial risk through erroneous trades and 
missed opportunities. Our work highlights a critical trade-off between accuracy and robustness 
(Tsipras et al., 2018), where the most accurate models in benign conditions are often the most 
fragile under attack. This vulnerability poses a significant challenge for financial institutions, 
suggesting that optimizing for accuracy alone, without considering adversarial robustness, is a 
risky strategy in the competitive environment of modern financial markets.
These findings have practical implications for traders, risk managers, and regulators, who 
must now consider adversarial manipulation as a new category of operational risk. Model 
validation must be augmented with adversarial stress testing, as current regulatory frameworks 
are ill-equipped to handle such high-speed, algorithmic threats. While our analysis assumes 
white-box access—a scenario of growing concern as models can be reverse-engineered or 
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


## Page 11

10
leaked—further work is needed to explore attack feasibility under more constrained, black-box 
settings. To mitigate these risks, future research should focus on defense mechanisms 
specifically tailored to HFT, such as adversarial training and order book anomaly detection (Xu 
et al., 2020). As machine learning (ML) continues to reshape market infrastructure, ensuring 
model security is an integral component of maintaining market stability and integrity.
Declaration of generative AI and AI-assisted technologies in the writing process
During the preparation of this work the authors used ChatGPT, Gemini and Grammarly in order 
to help review the flow of the writing. After using this tool/service, the author(s) reviewed and 
edited the content as needed and take full responsibility for the content of the published article.
REFERENCES
Brogaard, J., Carrion, A., Moyaert, T., Riordan, R., Shkilko, A., & Sokolov, K. (2018). High 
frequency trading and extreme price movements. Journal of Financial Economics, 
128(2), 253-265.
Brogaard, J., Hendershott, T., & Riordan, R. (2014). High-frequency trading and price discovery. 
The Review of Financial Studies, 27(8), 2267-2306.
Dixon, M. (2018). Sequence classification of the limit order book using recurrent neural 
networks. Journal of Computational Science, 24, 277-286.
Goldblum, M., Schwarzschild, A., Patel, A., & Goldstein, T. (2021). Adversarial attacks on 
machine learning systems for high-frequency trading. In Proceedings of the Second ACM 
International Conference on AI in Finance (pp. 1-9).
Goodfellow, I. J., Shlens, J., & Szegedy, C. (2015). Explaining and harnessing adversarial 
examples. In International Conference on Learning Representations, 2015.
Hochreiter, S., & Schmidhuber, J. (1997). Long short-term memory. Neural Computation, 9(8), 
1735-1780.
Ke, Y., & Zhang, Y. (2020). Does high-frequency trading reduce market underreaction to 
earnings news?. Finance Research Letters, 34, 101239.
Kirilenko, A., Kyle, A. S., Samadi, M., & Tuzun, T. (2017). The flash crash: High‐frequency 
trading in an electronic market. The Journal of Finance, 72(3), 967-998.
Korajczyk, R. A., & Murphy, D. (2019). High-frequency market making to large institutional 
trades. The Review of Financial Studies, 32(3), 1034-1067.
Kurakin, A., Goodfellow, I. J., & Bengio, S. (2018). Adversarial examples in the physical world. 
In Artificial intelligence safety and security (pp. 99-112). Chapman and Hall/CRC.
LeCun, Y., & Bengio, Y. (1995). Convolutional networks for images, speech, and time series. 
The handbook of brain theory and neural networks, 3361(10), 1995.
Li, B., Qi, P., Liu, B., Di, S., Liu, J., Pei, J., ... & Zhou, B. (2023). Trustworthy AI: From 
principles to practices. ACM Computing Surveys, 55(9), 1-46. 
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


## Page 12

11
Madry, A., Makelov, A., Schmidt, L., Tsipras, D., & Vladu, A. (2018). Towards deep learning 
models resistant to adversarial attacks. arXiv preprint arXiv:1706.06083.
Ntakaris, A., Magris, M., Kanniainen, J., Gabbouj, M., & Iosifidis, A. (2018). Benchmark dataset 
for mid-price forecasting of limit order book data with machine learning methods. 
Journal of Forecasting, 37(8), 852-866.
Ozbayoglu, A. M., Gudelek, M. U., & Sezer, O. B. (2020). Deep learning for financial 
applications: A survey. Applied Soft Computing, 93, 106384.
Szegedy, C., Zaremba, W., Sutskever, I., Bruna, J., Erhan, D., Goodfellow, I., & Fergus, R. 
(2014). Intriguing properties of neural networks. arXiv preprint arXiv:1312.6199.
Szegedy, C., Vanhoucke, V., Ioffe, S., Shlens, J., & Wojna, Z. (2016). Rethinking the inception 
architecture for computer vision. In Proceedings of the IEEE conference on computer 
vision and pattern recognition (pp. 2818-2826). 
Tsantekidis, A., Passalis, N., Tefas, A., Kanniainen, J., Gabbouj, M. and Iosifidis, A. (2017). 
Forecasting stock prices from the limit order book using convolutional neural networks. 
In 2017, IEEE 19th Conference on Business Informatics (CBI) (Vol. 1, pp. 7-12). IEEE.
Tsantekidis, A., Passalis, N., Tefas, A., Kanniainen, J., Gabbouj, M., & Iosifidis, A. (2020). 
Using deep learning for price prediction by exploiting stationary limit order book 
features. Applied Soft Computing, 93, 106401.
Tsipras, D., Santurkar, S., Engstrom, L., Turner, A., & Madry, A. (2018). Robustness may be at 
odds with accuracy. arXiv preprint arXiv:1805.12152.
Xu, H., Ma, Y., Liu, H. C., Deb, D., Liu, H., Tang, J. L., & Jain, A. K. (2020). Adversarial 
attacks and defenses in images, graphs and text: A review. International Journal of 
Automation and Computing, 17, 151-178.
Yamada, M. (2022). Profitability and liquidity provision of HFTs during large price shocks: 
Does relative tick size matter?. Finance Research Letters, 46, 102308.
Zhang, Z., Zohren, S., & Roberts, S. (2019). Deeplob: Deep convolutional neural networks for 
limit order books. IEEE Transactions on Signal Processing, 67(11), 3001-3012.
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


## Page 13

12
APPENDIX
A. Technical Comparison of Order Book Perturbation Methods
This Appendix provides a technical overview of the two white-box adversarial attack 
methods used in this study: the Fast Gradient Sign Method (FGSM) introduced by Goodfellow et 
al. (2015) and the Projected Gradient Descent (PGD) by Madry et al. (2018). Both methods 
generate perturbations by leveraging the gradient of the model’s loss function, but they differ 
significantly in their mechanism, computational intensity, and effectiveness. 
A1. Fast Gradient Sign Method (FGSM)
FGSM Method is a foundational, single-step adversarial attack designed for efficiency. It 
operates by making a linear assumption about the model’s loss function and perturbing the input 
data in the direction that maximizes this loss. The perturbation is calculated by taking the sign of 
the gradient of the loss function with respect to the input features. This direction represents the 
path of the steepest ascent for the loss, and by moving the input along this path, the attack aims 
to induce a misclassification with minimal computational effort.
The adversarial example, 𝑥′, is generated from the original input 𝑥 using the following 
formula:
𝑥′ = 𝑥+ 𝜖∙𝑠𝑖𝑔𝑛(∇𝑥𝐽(𝜃,𝑥,𝑦))
Where:

𝑥′ is the perturbed, adversarial input.

𝑥 is the original input data (i.e., the LOB snapshot).

𝜖 is a small scalar value that controls the magnitude (volume) of the perturbation.

𝑠𝑖𝑔𝑛( ⋅) is the sign function, which returns -1, 0, or 1.

∇𝑥𝐽(𝜃,𝑥,𝑦) is the gradient of the model’s loss function 𝐽 with respect to the input 𝑥, for a 
given set of model parameters 𝜃 and true label 𝑦.
In essence, FGSM identifies the direction that will most effectively increase the model’s 
error and applies a uniform perturbation of size 𝜖 in that direction across all features. Its primary 
advantages are its speed and simplicity, making it a common baseline for assessing adversarial 
vulnerability.
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


## Page 14

13
A2. Projected Gradient Descent (PGD)
PGD is a more powerful, iterative extension of FGSM. Rather than taking a single large 
step, PGD applies the perturbation in multiple, smaller steps, refining the adversarial example at 
each iteration. Crucially, after each step, it “projects” the perturbed input back into an 𝜖-ball 
around the original input. This projection ensures that the total perturbation does not exceed the 
maximum magnitude 𝜖, preventing the attack from becoming too obvious or unrealistic. This 
iterative refinement makes PGD a much stronger attack, as it is more likely to find the optimal 
perturbation within the given constraints to fool the model.
The PGD attack is an iterative process. Starting with the original input 𝑥(0) = 𝑥, the 
adversarial example at the next step, 𝑡+ 1, is calculated as:
𝑥(𝑡+1) =
𝑥,𝜖(𝑥(𝑡) + 𝛼∙𝑠𝑖𝑔𝑛(∇𝑥(𝑡)𝐽(𝜃,𝑥(𝑡),𝑦)))
Where:

𝑥(𝑡) is the adversarial example at iteration 𝑡. The process is initialized with the original, 
unperturbed data, 𝑥(0) = 𝑥.

𝛼 is the step size for each iteration, which is typically smaller than the total perturbation 
budget 𝜖.

∇𝑥(𝑡)𝐽(𝜃,𝑥(𝑡),𝑦) is the gradient of the model’s loss function 𝐽 with respect to the current 
adversarial example 𝑥(𝑡).

𝛱𝑥,𝜖( ∙) is the projection operator, which ensures that the updated example 𝑥(𝑡+1) remains 
within the 𝜖-ball around the original input 𝑥(0) = 𝑥. 
PGD can be seen as a more patient and strategic adversary. It methodically searches for 
the best possible attack within the allowed perturbation space, making it the gold standard for 
evaluating the robustness of machine learning models.
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


## Page 15

14
B. Technical Comparison of High-Frequency Trading Model Architectures
We provide a technical comparison of three machine learning models employed for 
predicting price movements from limit order book (LOB) data: LSTM, CNN, and DeepLOB. 
Each model utilizes distinct neural network architectures to capture the higher-order patterns 
inherent in high-frequency trading environments. All models use the same input, which consists 
of the top 10 levels of ask and bid prices and volumes (20 features each) over 100 timesteps. 
Therefore, each input tensor has a shape of 100 x 40 (time x features).
1. Long Short-Term Memory (LSTM)
Long Short-Term Memory (LSTM) networks are a specialized form of recurrent neural 
network designed to model temporal dependencies in sequential data by maintaining a memory 
cell that is updated and gated at each time step (Hochreiter and Schmidhuber, 1997). When 
applied to limit order book (LOB) data, an LSTM ingests a sequence of consecutive snapshots, 
each containing features such as bid and ask prices and volumes, and learns to retain or forget 
temporal information about past order flow dynamics based on the evolving market context. The 
input, forget, and output gates within each LSTM unit control the flow of information into and 
out of the cell state, allowing the network to capture both short-term bursts of trading activity 
(e.g., rapid sequences of buy orders) and longer-term trends (e.g., persistent accumulation or 
distribution phases). 
We use two stacked LSTM layers (each with 64 memory units), followed by a dropout 
layer (rate = 0.2) to mitigate overfitting, and a final softmax classifier over three classes (price 
up, down, or neutral). By preserving salient patterns over variable time lags, LSTMs can 
effectively predict near-term price movements driven by momentum or mean. An LSTM trader 
is akin to an experienced tape reader, constantly monitoring every incoming quote and trade on 
the ticker tape and recalling patterns of order flow over time (e.g., sustained buying or selling).
2. Convolutional Neutral Network (CNN)
CNN architecture is often used for computer vision (LeCun and Bengio, 1995). It 
processes limit order book (LOB) data by applying learnable filters that slide across the 
multidimensional input (the “image” of price and volume levels over time) to extract salient 
spatial patterns automatically. In the context of LOB prediction, a CNN first transforms the input 
through a series of convolutional layers, where small kernels identify local motifs, such as 
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


## Page 16

15
clustered liquidity at adjacent price levels or recurring depth imbalances (Tsantekidis et al., 
2017). Deeper layers aggregate these local features into more abstract representations (e.g., 
multi-tick “walls” of resting orders or systematic spread compressions), enabling the network to 
discern which structural configurations have historically preceded price upticks or downticks. By 
incorporating inception modules (parallel convolutions with different kernel sizes), advanced 
CNN variants can simultaneously capture patterns across multiple scales, thereby enhancing 
robustness and predictive accuracy (Szegedy et al., 2015).
A CNN trader is similar to a chartist who examines price and volume bars at various time 
scales (ticks, minutes, hours) to identify patterns (e.g., head-and-shoulders). CNN applies filters 
of different lengths to detect short- and medium-term patterns in the LOB (spatial), but it has no 
explicit mechanism for memory (temporal) like LSTM.
3. DeepLOB
DeepLOB is a hybrid convolutional-recurrent architecture specifically designed to 
forecast short-term mid-price movements from raw limit order book (LOB) data by combining 
multiscale spatial feature extraction with temporal modeling (Zhang et al. (2019). First, a series 
of 2D CNN layers and inception modules apply parallel filters of varying widths to a 100 × 40 
LOB input window, automatically identifying liquidity walls, spread compressions, and other 
structural motifs at multiple scales. The resulting feature maps are then flattened and fed into an 
LSTM layer, which integrates these spatial representations over the most recent 100 timesteps of 
market activity to capture evolving order-flow dynamics. A final softmax layer produces 
probabilities for downward, stationary, or upward price movements, enabling the model to 
leverage both static depth patterns and their temporal evolution for robust high-frequency trading 
signals.
A DeepLOB trader integrates both order book depth and evolving order flow over time to 
build predictive signals. DeepLOB first “maps” the depth structure (spatial), then “remembers” 
how it evolves (temporal).
Table A1 summarizes the key architectural components and parameter counts for each 
model, while Table A2 presents the model accuracies for both the training data and the test data.
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


## Page 17

16
Table A1: Model Architectures and Parameters
This table summarizes the key architectural components and the approximate number of trainable 
parameters for the three deep learning models used in the study: LSTM, CNN, and DeepLOB. Each model 
is designed to predict price movements from limit order book data.
Model
Architecture Components
Parameters
LSTM
- Input Layer
- LSTM Layers (2 layers with 64 units each)
- Dropout Layer
- Output Layer
~80,000
CNN
- Input Layer
- Convolutional Blocks (multiple 2D convolutions)
- Inception Modules
- Output Layer
~150,000
DeepLOB
- Input Layer
- Convolutional Blocks (multiple 2D convolutions)
- Inception Modules
- LSTM Layer (64 units)
- Output Layer
~142,000 + 64,000
Table A2: Baseline Model Accuracy
This table presents the baseline model accuracy on both the training and test datasets for the LSTM, CNN, 
and DeepLOB models before any adversarial attacks. Gap is the difference between training and test 
accuracy, a measure of model overfitting.
Model
Baseline
Accuracy:
Training
Baseline
Accuracy:
Test
Gap
LSTM
67.27
48.62
18.65
CNN
82.90
76.06
6.84
DeepLOB
84.30
77.19
7.11
This preprint research paper has not been peer reviewed. Electronic copy available at: https://ssrn.com/abstract=5367043
Preprint not peer reviewed


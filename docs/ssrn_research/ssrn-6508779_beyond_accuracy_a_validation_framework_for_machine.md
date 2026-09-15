# Beyond Accuracy: A Validation Framework for Machine Learning

- **Source File**: `ssrn-6508779.pdf`
- **Total Pages**: 37
- **SSRN ID**: `ssrn-6508779`

---

## Page 1

Highlights
1
Beyond Accuracy: A Validation Framework for Machine Learning
2
in Cryptocurrency Trading
3
Jaewook Kim
4
• VALID: to our knowledge the first checklist-style protocol pairing binary
5
statistical and economic gates for financial ML
6
• Bull bias: tree-based crypto ML models predict 90–97% long without
7
class balancing
8
• Statistical significance does not guarantee economic profitability: nine
9
Bonferroni survivors all carry PBO=1.0
10
• Net Sharpe falls monotonically with trading frequency; every 15-minute
11
variant loses money after costs
12
• Monte Carlo (n=200): 27% AUC false positive rate, eliminated by
13
CPCV with PBO
14


## Page 2

Beyond Accuracy: A Validation Framework for
15
Machine Learning in Cryptocurrency Trading
16
Jaewook Kim
17
Independent Researcher, Goyang-si, Republic of Korea; B.S. Industrial Engineering,
18
UNIST; Professional Engineer (Engineers Australia)
19
Abstract
20
Machine learning strategies for cryptocurrency trading routinely report excep-
21
tional backtest results, yet practitioners consistently fail to replicate them. We
22
identify three systematic failure modes—directional prediction bias, statistical-
23
economic disconnect, and transaction cost omission—through 340 strategy
24
variants across four timeframes and three cryptocurrency assets. To address
25
these failures, we propose VALID (Validation Architecture for Learning-based
26
Investment Decisions), a 12-item reporting and validation framework for
27
financial ML research—to our knowledge the first checklist-style protocol for
28
financial ML to pair binary statistical and economic gates in a fixed reporting
29
order.
30
We demonstrate that gradient-boosted models predict long 90–97% of
31
the time without class balancing; that a run passing the permutation test
32
(p = 0) can still fail combinatorial purged cross-validation and be economically
33
irrelevant; and that net Sharpe falls monotonically with trading frequency.
34
Monte Carlo analysis (200 iterations × 4 asset-timeframe settings) shows
35
27–30% false positive rates for AUC-based validation alone, reduced to 0%
36
by CPCV with PBO. Applying five multiple-testing corrections to the corpus,
37
nine variants survive Bonferroni—all with PBO = 1.0—and none survives
38
the Deflated Sharpe Ratio. We report null-distribution analysis of Var(SRIS)
39
providing evidence consistent with Witzany’s (2021) PBO critique. A system-
40
atic audit of 80 papers reveals that the median study satisfies only 2.5 of 12
41
VALID items. We release an open-source implementation for reproducibility.
42
Keywords:
financial machine learning, cryptocurrency trading, validation
43
framework, backtest overfitting, reporting standard
44
JEL: G11, G14, G17, C45, C52
45


## Page 3

Revision note (v3.2, August 2026). This version corrects the previous
draft: a cost table built on a synthetic placeholder signal has been replaced with
corpus statistics; a case study that combined metrics from two pipeline runs
has been rewritten from a single run’s artifacts; the parameter-flatness claim
has been narrowed; the self-assessment was revised from 10/12 to 9/12. All
corrections were identified by applying the VALID audit process to our own pa-
per. Full changelog: https://github.com/orcajae/valid-framework/blob/
main/CHANGELOG_CR.md
46
1. Introduction
47
The application of machine learning to cryptocurrency trading has grown
48
rapidly, producing a literature characterized by strikingly positive results.
49
Cross-sectional factor models report weekly long-short returns of 3.87%
50
(Fieberg et al., 2025). LSTM ensembles achieve annualized Sharpe ratios
51
exceeding 3.0 (Xu et al., 2022). Tree-based models demonstrate AUC scores
52
above 0.80 on directional prediction tasks (Li et al., 2024). Taken at face value,
53
these findings suggest ML-driven crypto trading offers among the highest
54
risk-adjusted returns in any asset class.
55
Yet the gap between published results and practitioner experience is vast.
56
In traditional finance, this disconnect is well documented: Ioannidis (2005)
57
demonstrated that most published research findings are false under conditions
58
of low pre-study odds and high researcher flexibility. Harvey et al. (2016)
59
showed that the majority of 316 published equity factors are likely false
60
discoveries, proposing a t-ratio threshold of 3.0 rather than the conventional
61
2.0. McLean and Pontiff (2016) documented 26% out-of-sample decay and
62
58% post-publication decay in equity anomalies. Hou et al. (2020) replicated
63
452 anomalies and found 65% fail—82% after multiple testing correction. The
64
cryptocurrency ML literature has not yet undergone equivalent scrutiny.
65
Kapoor and Narayanan (2023) identified data leakage affecting 294 studies
66
across 17 scientific fields, proposing a taxonomy of eight leakage types and
67
a “model info sheet” reporting template. Their work, published in Patterns
68
and subsequently extended to the REFORMS framework in Science Advances
69
(Kapoor et al., 2024), demonstrated that domain-specific validation standards
70
can substantially reduce false positive rates. However, no analogous standard
71
exists for financial ML. TRIPOD+AI (Collins et al., 2024) covers clinical
72
2


## Page 4

prediction models. REFORMS addresses general ML-based science. MI-
73
CLAIM (Norgeot et al., 2020) targets clinical AI. Not one published checklist
74
addresses the unique challenges of ML-based trading strategy development:
75
temporal data dependencies, transaction cost modeling, class imbalance in
76
directional prediction, or the distinction between statistical and economic
77
significance.
78
This gap has consequences. Without standardized validation, published
79
crypto ML results vary wildly in methodological rigor. Some studies omit
80
transaction costs entirely; others use unrealistically low cost assumptions.
81
Few test for directional prediction bias. Even fewer apply advanced over-
82
fitting diagnostics such as Combinatorial Purged Cross-Validation (CPCV)
83
or Probability of Backtest Overfitting (PBO), despite their demonstrated
84
superiority over traditional walk-forward methods (Arian et al., 2024).
85
1.1. Contributions
86
This paper makes five contributions:
87
1. The VALID framework.
We propose a 12-item validation and
88
reporting checklist for financial ML research—to our knowledge the
89
first checklist-style protocol for this field to pair binary statistical and
90
economic gates in a fixed reporting order, complementing rather than
91
superseding prior backtesting guidance.
92
2. Systematic literature audit. We survey 80 published cryptocurrency
93
ML trading papers (2018–2026), coding each for validation methodol-
94
ogy, cost assumptions, class balancing, baseline comparison, and code
95
availability.
96
3. Three empirical failure modes at scale. Using 340 strategy variants
97
across four timeframes and three cryptocurrency assets (BTC, ETH,
98
SOL), we document: (a) bull bias, (b) statistical-economic disconnect,
99
and (c) cost illusion.
100
4. Monte Carlo false positive quantification. We generate 200 syn-
101
thetic price series per setting across four asset-timeframe configurations,
102
demonstrating that AUC-based evaluation produces 27–30% false posi-
103
tives while CPCV + PBO reduces this to 0% [0%, 1.9%] in every setting.
104
Ablation analysis identifies CPCV/PBO (Item V4) as the single most
105
impactful validation component.
106
5. Multiple-testing evidence. Applying five correction methods to the
107
corpus, nine variants survive Bonferroni—every one with PBO = 1.0—
108
while the Deflated Sharpe Ratio rejects all 340. We also derive a Monte
109
3


## Page 5

Carlo null distribution of Var(SRIS) (real 0.012, null 95th percentile
110
0.328) and show that the absolute and null-relative flatness criteria
111
disagree, evidence consistent with Witzany’s (2021) PBO critique.
112
1.2. Notation and Abbreviations
113
Table 1 defines the key terms used throughout this paper.
114
Table 1: Key abbreviations and definitions.
Term
Definition
AUC
Area Under the ROC Curve; classification performance metric
CPCV
Combinatorial Purged Cross-Validation; generates
 N
k

tem-
poral train-test splits
CUSUM
Cumulative Sum filter; event sampling method for non-
uniform time series
FPR
False Positive Rate; proportion of null (signal-free) datasets
incorrectly classified as positive
PBO
Probability of Backtest Overfitting; fraction of CPCV paths
where in-sample-best underperforms out-of-sample
SR
Sharpe Ratio; annualized risk-adjusted return
TB
Triple Barrier labeling; assigns {−1, 0, +1} labels based on
profit/stop-loss/time barriers
Var(SRIS)
Variance of in-sample Sharpe ratios across configurations;
measures parameter-landscape diversity
VALID
Validation Architecture for Learning-based Investment Deci-
sions
1.3. Paper Organization
115
Section 2 reviews related work. Section 3 presents the systematic literature
116
audit. Section 4 introduces the VALID framework. Sections 5 and 6 provide
117
empirical validation. Section 7 discusses implications. Section 8 concludes.
118
2. Related Work
119
2.1. Machine Learning for Cryptocurrency Trading
120
The premise that ML can profitably trade cryptocurrency rests on market
121
inefficiency; Urquhart (2016) provided early evidence that Bitcoin prices do
122
4


## Page 6

not follow a random walk, though subsequent work suggests efficiency has
123
increased over time. The crypto ML literature has grown rapidly since 2019.
124
Fang et al. (2022) surveyed 146 papers and identified technical analysis, funda-
125
mental analysis, and ML-based approaches as the three dominant paradigms,
126
noting that approximately half of surveyed studies omit transaction costs.
127
Early work focused on price direction prediction: McNally et al. (2018) applied
128
LSTM and Bayesian-optimized RNNs to Bitcoin, while Alessandretti et al.
129
(2018) tested gradient-boosted methods across multiple cryptocurrencies. Sun
130
et al. (2020) proposed a LightGBM-based forecasting model, and Vo and
131
Yuen (2020) explored multi-step prediction with deep learning. Sebastião
132
and Godinho (2021) examined how changing market conditions affect ML
133
trading performance. More recent work has expanded to cross-sectional factor
134
models: Fieberg et al. (2025) developed the CTREND factor across 3,244
135
coins, while Cakici et al. (2024) applied 12 ML models to 37 cryptocurrency-
136
specific factors. Leung and Zhao (2021) provide a comprehensive overview of
137
cryptocurrency trading and exchange mechanics.
138
The methods adopted in crypto trading mirror those validated in tradi-
139
tional equities. Gu et al. (2020) demonstrated that gradient-boosted trees and
140
neural networks dominate equity return prediction, and these same architec-
141
tures now constitute the majority of crypto ML studies. Krauss et al. (2017)
142
showed that ensemble methods achieve statistical arbitrage on the S&P 500
143
but noted the critical role of transaction costs in eroding gross alpha—a
144
finding we extend to crypto in Section 5. Deep learning surveys (Olorunnimbe
145
and Viktor, 2023; Siami-Namini et al., 2019; Jiang et al., 2024) document
146
rapid LSTM adoption, yet neither addresses the class imbalance problem
147
we identify. Beyond supervised learning, Borrageiro et al. (2022) applied
148
reinforcement learning to FX trading, and Zhang et al. (2025) review neural
149
algorithmic trading systems; both paradigms face the same validation gaps
150
that VALID addresses. Schnaubelt (2022) applied DRL to cryptocurrency
151
limit order placement, reporting profitable results but without CPCV or PBO
152
validation.
153
However, several concerns have emerged. Jaquart et al. (2021) explicitly
154
warned that imbalanced training sets may cause classifiers to predict the
155
majority class regardless of input features. Lahmiri and Bekiros (2019) found
156
that naive models consistently outperform ML and deep learning in univariate
157
crypto forecasting. Grądzki et al. (2025) demonstrated that information-driven
158
bars with triple barrier labeling improve upon standard approaches, but their
159
cost assumptions (10 basis points) may understate realistic execution costs.
160
5


## Page 7

More broadly, Zhu et al. (2023) documented common pitfalls in ML-based
161
science—including data leakage, overfitting, and inadequate baselines—that
162
map directly onto the failure modes we quantify.
163
2.2. Backtest Overfitting and Validation Methodology
164
White (2000) proposed the Reality Check for data snooping, later refined
165
by Hansen’s (2005) Superior Predictive Ability test. Bailey and López de
166
Prado (2014); Bailey et al. (2017) introduced PBO and DSR as tools for
167
detecting backtest overfitting. Arian et al. (2024), published in Knowledge-
168
Based Systems, compared CPCV against walk-forward methods, introducing
169
Bagged CPCV and Adaptive CPCV variants.
170
Witzany (2021) provided the only formal critique of PBO, demonstrating
171
that CSCV/PBO exhibits negative bias when strategies have similar returns:
172
“the best IS model tends to the worst OOS not because of the models but due to
173
the design of the method itself.” Bailey et al. (2017) themselves acknowledged
174
that low PBO does not guarantee positive out-of-sample performance. The
175
Sharpe ratio itself requires careful statistical treatment (Lo, 2002), particularly
176
when comparing strategies across different holding periods.
177
2.3. Statistical Versus Economic Significance
178
Harvey et al. (2016) argued that extensive data mining requires t-ratios
179
above 3.0. Novy-Marx and Velikov (2016) demonstrated that most equity
180
anomalies with monthly turnover above 50% become unprofitable after costs.
181
Blitz et al. (2023) showed that even short-term alpha signals in equities are
182
substantially eroded by transaction costs. Patton and Weller (2020) found
183
momentum implementation costs of 7.2–7.6% annually eliminate most profits.
184
Chen and Velikov (2023) showed that post-publication decay combined with
185
trading costs destroys 93% of anomaly returns.
186
In cryptocurrency markets, Makarov and Schoar (2020) documented signif-
187
icant cross-exchange price differences. Kim et al. (2021) developed a volatility
188
index for cryptocurrencies, highlighting the extreme volatility regime that
189
amplifies transaction cost impact. Almeida and Gonçalves (2024) system-
190
atically reviewed crypto market microstructure, identifying bid-ask spreads
191
of 2–50+ basis points. No published study has systematically quantified
192
the gross-to-net alpha gap across multiple timeframes for ML-based crypto
193
strategies.
194
6


## Page 8

2.4. Reporting Standards for ML-Based Research
195
TRIPOD (Collins et al., 2015) provides 22 items for clinical prediction
196
model reporting and has accumulated over 4,000 citations. TRIPOD+AI
197
(Collins et al., 2024) extends this with 27 items. REFORMS (Kapoor et al.,
198
2024) proposes 32 items for general ML-based science. MI-CLAIM (Norgeot
199
et al., 2020) provides a 6-step checklist for clinical AI. Model Cards (Mitchell
200
et al., 2019) propose documentation standards for trained ML models.
201
Critically, no published reporting standard addresses financial
202
ML or algorithmic trading. This gap motivates the VALID framework
203
proposed in Section 4.
204
2.5. Cryptocurrency Momentum and Simple Benchmarks
205
Time-series momentum in Bitcoin was established by Liu and Tsyvinski
206
(2021). Yang (2025) applied risk-managed momentum to crypto, reporting
207
Sharpe improvements from 1.12 to 1.42. Grobys et al. (2025) documented that
208
crypto momentum is subject to severe crashes mitigable through volatility
209
management.
210
3. Systematic Literature Audit
211
3.1. Search Strategy and Paper Selection
212
We searched Google Scholar, Scopus, and Web of Science for papers
213
published between 2018 and 2026 using the query terms “cryptocurrency” AND
214
(“machine learning” OR “deep learning”) AND (“trading” OR “prediction”).
215
After screening, we retained 80 papers for full-text analysis, of which 74
216
are empirical crypto ML studies.
We classify a paper as empirical if it
217
applies a machine learning method to real cryptocurrency market data for
218
a trading or prediction task; surveys, synthetic-only methodological studies,
219
and non-crypto or non-ML studies are excluded (six papers).
220
3.2. Coding Methodology
221
Each paper was coded on seven dimensions corresponding to the VALID
222
framework’s core items (Table 2).
223
7


## Page 9

Table 2: Literature audit coding dimensions.
Dimension
Coding Question
D1: Cost modeling
Are transaction costs included?
D2: Class balance
Is directional prediction bias addressed?
D3: Temporal split
Is train/test splitting temporal or random?
D4: Validation
Walk-forward, CPCV, k-fold, or holdout?
D5: Baselines
Compared against buy-and-hold? Simple rules?
D6: Net performance
Is cost-adjusted performance reported?
D7: Reproducibility
Is code or data publicly available?
Table 3: Literature audit results (n = 74 empirical papers).
Dimension
Failing
Rate
95% CI
VALID Item
D1: Costs omitted
40/74
54%
[43%, 65%]
V7
D2: No class balance
54/74
73%
[62%, 82%]
V1, V2
D3: Random split
5/74
7%
[3%, 15%]
V3
D4: Weak validation
15/74
20%
[13%, 31%]
V4
D4: CPCV used
0/74
0%
[0%, 5%]
V4
D5: BnH only baseline
26/74
35%
[25%, 46%]
V9
D6: No net performance
40/74
54%
[43%, 65%]
V7, V8
D7: No code available
63/74
85%
[75%, 91%]
V12
8


## Page 10

3.3. Audit Results
224
Table 3 summarizes the findings across 74 empirical papers, with 95%
225
Wilson confidence intervals.
226
Class imbalance is the most neglected dimension: 73% [62%, 82%] of
227
papers do not address class balance. Cost omission remains widespread at
228
54% [43%, 65%]. CPCV adoption is negligible: no empirical paper in our
229
sample uses it. Reproducibility is poor: 85% [75%, 91%] provide neither
230
code nor data. The median paper satisfies only 2.5 of 12 VALID items (see
231
Figure 1).
232
4. The VALID Framework
233
4.1. Design Principles
234
The VALID (Validation Architecture for Learning-based Investment De-
235
cisions) framework follows three principles: (1) finance-specific, addressing
236
pitfalls beyond REFORMS/TRIPOD; (2) evidence-based, motivated by quan-
237
tified failure modes; (3) actionable, specifying what to report and how to
238
test.
239
4.2. The 12 VALID Items
240
Table 4 presents the 12 items.
241
4.2.1. Item Descriptions
242
V1: Report prediction class distribution. Authors must report the
243
proportion of long, short, and neutral labels in both training and test sets.
244
In trending cryptocurrency markets, base rates of 60–80% long are common,
245
making majority-class memorization a viable strategy for any classifier. With-
246
out this disclosure, reviewers cannot distinguish genuine predictive power
247
from base-rate exploitation.
248
V2: Test with and without class balancing. Results should be
249
reported under both balanced and unbalanced conditions. As demonstrated
250
in Section 5 (Failure Mode 1), class balancing eliminates directional bias but
251
typically does not improve AUC, revealing whether the model has learned
252
signal or structure. Acceptable balancing methods include sample weights,
253
SMOTE, and undersampling; the chosen method should be stated explicitly.
254
V3: Use temporal splitting only. All train-test splits must respect
255
chronological order, with purge and embargo periods to prevent information
256
leakage from overlapping feature lookback windows. Random or stratified
257
9


## Page 11

V1: Class distribution
V2: Class balancing
V3: Temporal split
V4: CPCV with PBO
V5: Var(SR_IS)
V6: Permutation tests
V7: Net performance
V8: Cost sensitivity
V9: Simple baselines
V10: Bear markets
V11: Trade frequency
V12: Code available
Jiang Liang (2017)
Nakano et al. (2018)
McNally et al. (2018)
Alessandretti et al. (2018)
Abraham et al. (2018)
Huang et al. (2019)
Valencia et al. (2019)
Ferdiansyah et al. (2019)
Patel et al. (2020)
Jay et al. (2020)
Livieris et al. (2020)
Mudassir et al. (2020)
Saad et al. (2020)
Sun et al. (2020)
Aboussalah Lee (2020)
Vo Yuen (2020)
Lucarelli Borrotti (2020)
Chowdhury et al. (2020)
Dutta et al. (2020)
Bustos Pomares-Quimbaya (2020)
Jaquart Dann Weinhardt (2021)
Akyildirim et al. (2021)
Chen He Tao (2021)
Khedr et al. (2021)
Sebastiao Godinho (2021)
Carta et al. (2021)
Liu Tsyvinski (2021)
Xu et al. (2022)
Borrageiro et al. (2022)
Schnaubelt (2022)
Ortu et al. (2022)
Liew Hewlett (2022)
Huang Rojas Cahill (2022)
Parekh et al. (2022)
Otero Caicedo (2022)
Mahmoodi et al. (2023)
Michankow et al. (2023)
Koutsouri et al. (2023)
Slepaczuk Zenkova (2023)
Bu Cho (2023)
Ji et al. (2023)
Zhang et al. (2023)
Sadorsky (2023)
Kim et al. (2023)
Sattarov et al. (2023)
Zheng et al. (2023)
Kwon et al. (2023)
Hachicha et al. (2023)
Maleki et al. (2023)
Cohen (2023)
Sun et al. (2023)
Li et al. (2024)
Lahmiri Bekiros (2024)
Kim et al. (2024)
Yin Liu (2024)
Cakici et al. (2024)
Helder et al. (2024)
Weng et al. (2024)
Banerjee et al. (2024)
Alonso et al. (2024)
Tzouvanas et al. (2024)
Huang et al. (2024)
Hachicha Prigent (2024)
Hassan et al. (2024)
Lee Kim (2024)
Chen et al. (2024)
Mohapatra et al. (2024)
Gradzki et al. (2025)
Fieberg et al. (2025)
Yang et al. (2025)
Grobys et al. (2025)
Zhang Wei (2025)
MDPI Info 2025 (2025)
Kose (2025)
0
3
6
9
12
VALID score (of 12)
dashed: median = 2.5
V1
V2
V3
V4
V5
V6
V7
V8
V9
V10 V11 V12
0
50
100
Fail (%)
95%
98%
7%
23%
100% 100%
54%
54%
32%
n/a
n/a
85%
Pass
Partial
Fail
Not applicable
Figure 1: VALID compliance across 74 empirical cryptocurrency ML papers (2017–2025).
Each row represents one paper (chronologically ordered); columns represent VALID items
V1–V12. The median paper satisfies 2.5 of 12 items. Per-paper states are derived from
the coding sheet (Table 2) under the dimension-to-item mapping printed in Table 3. The
failure rates in the lower panel use applicable-only denominators and so differ from Table 3,
which divides by all 74: V1 and V2 fail in 95% and 98% of the 58 papers where a directional
class balance applies, and in 73% of all 74. V5 and V6 were not coded per paper and
are recorded as universal non-compliance; V10 and V11 were not directly assessable from
published text and are coded as N/A.
10


## Page 12

Table 4: The 12 VALID items.
#
Item
Rationale
Failure Mode
V1
Report prediction
class distribution
Base-rate learning on trending assets
Bull bias
V2
Test with/without
class balancing
Structural class imbalance in crypto
Bull bias
V3
Use temporal splitting
only
Information leakage across time,
including feature lookback windows
Temporal
leakage
V4
Apply CPCV with
PBO
Holdout insufficient for large search
Overfitting
V5
Report Var(SRIS)
PBO = 0 from flat landscape
(Witzany, 2021)
PBO misinter-
pretation
V6
Include permutation
tests (≥100)
Confirm signal existence
Spurious
patterns
V7
Report net
performance with
costs
Cost omission inflates alpha
Cost illusion
V8
Cost sensitivity
analysis
Cost assumptions can flip alpha sign
Cost illusion
V9
Compare against
simple baselines
Weak baselines inflate relative
performance
Weak baselines
V10 Evaluate in bear
markets and regime
transitions
Bull-market trend-following not
informative
Regime overfit
V11 Report trade
frequency
High-frequency cost headwinds
Hidden
turnover
V12 Provide code for
reproducibility
<10% of papers provide code
Irrepro-
ducibility
11


## Page 13

k-fold splitting violates the temporal dependence structure of financial data
258
and produces upward-biased performance estimates. Our audit finds 7% of
259
papers still use random splitting (Table 3).
260
V4: Apply CPCV with PBO. Combinatorial Purged Cross-Validation
261
generates
 N
k

train-test combinations from N chronological groups, producing
262
multiple non-overlapping backtest paths (see Equation 4). PBO quantifies
263
the probability that the in-sample-best configuration underperforms out-of-
264
sample. Our ablation analysis (Table 12) shows that removing V4 alone
265
increases the false positive rate from 0% to 27%, making it the single most
266
impactful validation component.
267
V5: Report parameter-space variance Var(SRIS). A low PBO can
268
be misleading when all strategy configurations perform similarly in-sample,
269
so that the search cannot distinguish between them (Equation 5). Authors
270
should compute Var(SRIS) across all tested configurations and compare it
271
against a null distribution derived from synthetic data.
If the observed
272
variance falls below the 5th percentile of the null, PBO should be flagged as
273
uninformative rather than reassuring (Table 9).
274
V6: Include permutation tests (≥100 iterations). Permutation
275
testing establishes whether a model’s performance exceeds what would be
276
expected from random label assignment. We recommend a minimum of 100
277
permutation iterations and reporting the resulting p-value alongside standard
278
metrics. This provides a complementary check to CPCV/PBO by testing for
279
signal existence rather than overfitting.
280
V7: Report net performance with realistic transaction costs.
281
Gross Sharpe ratios are meaningless for deployment decisions. Authors must
282
report net performance after round-trip transaction costs including exchange
283
fees, estimated slippage, and funding rates where applicable. Our analysis
284
shows net Sharpe falling monotonically with trading frequency (Table 10)
285
and, in the one run where gross and net are both recorded, 82% of the gross
286
Sharpe consumed at 18 bp.
287
V8: Conduct cost sensitivity analysis. Because true execution costs
288
vary by venue, time, and order size, authors should report performance across
289
at least three cost levels (e.g., 0, 18, and 50 basis points round-trip). A strategy
290
whose alpha flips sign within realistic cost bounds has limited practical value.
291
This analysis also reveals the cost breakeven point—the maximum tolerable
292
transaction cost for positive net returns.
293
V9: Compare against simple baselines beyond buy-and-hold. Buy-
294
and-hold is a necessary but insufficient baseline. Authors should include at
295
12


## Page 14

least one rule-based alternative with comparable trading frequency (Table 11).
296
In our experiments, RSI and MACD crossover—strategies implementable in
297
under 10 lines of code—outperform the best ML variant at matched frequency.
298
V10: Evaluate in bear markets and regime transitions. Strategies
299
trained predominantly on bull-market data may perform well on average but
300
fail catastrophically during drawdowns. Authors should report performance
301
conditional on market regime (e.g., calm vs. stressed, as in Figure 5). A
302
strategy that underperforms buy-and-hold during bear markets offers no
303
hedging value despite positive aggregate statistics.
304
V11: Report trade frequency and turnover. High-frequency strate-
305
gies incur proportionally higher transaction costs, creating a hidden drag that
306
aggregate Sharpe ratios obscure. Reporting annualized trade count enables
307
reviewers to assess whether reported returns survive realistic execution. In
308
our sample, every 15-minute variant shows SR ≤−1.33 after costs.
309
V12: Provide code and data for reproducibility. Our audit finds 85%
310
of papers provide neither code nor data (Table 3). Without reproducibility
311
artifacts, claimed results cannot be independently verified. We recommend
312
releasing, at minimum, the training pipeline, evaluation code, and a sample
313
dataset or synthetic data generator sufficient to reproduce the main results.
314
4.3. Relationship to Existing Standards
315
VALID supplements REFORMS with finance-specific items (V7, V8,
316
V11 for cost modeling; V1, V2 for class balance) absent from all existing
317
frameworks. Table 5 highlights the coverage gap.
318
Table 5: VALID versus existing ML reporting standards.
Standard
Domain
Items
Cost Model
Class Bal.
TRIPOD+AI
Clinical ML
27
N/A
No
REFORMS
General ML
32
No
Partial
MI-CLAIM
Clinical AI
6
N/A
No
NeurIPS Checklist
ML research
15
No
No
VALID
Financial ML
12
Yes
Yes
4.4. Application Protocol
319
We recommend two stages: Stage 1 (Reporting): V1–V6, V9, V12;
320
Stage 2 (Deployment): V7, V8, V10, V11. A strategy passing Stage 1 but
321
13


## Page 15

failing Stage 2 has scientific value but limited practical value—a distinction we
322
term the statistical-economic disconnect. Figure 2 provides an overview
323
of the VALID framework architecture and its relationship to the three failure
324
modes documented in Section 5.
325
ML trading
strategy
VALID-
compliant
Stage 1: Reporting
scientific validity
V1-V2
Class balance
V3
Temporal split
V4
CPCV with PBO
V5
Var(SRIS)
V6
Permutation tests
V9
Baseline comparison
V12
Code released
Stage 2: Deployment
economic viability
V7-V8
Net SR after costs
V10
Bear market eval
V11
Trade frequency
all pass
all pass
all pass
Failure modes and the items that detect them
Bull bias
Detected by V1, V2
Statistical-economic disconnect
Detected by V4, V5, V6
Cost illusion
Detected by V7, V8, V11
Figure 2: VALID framework overview. Stage 1 (Reporting) items V1–V6, V9, V12 address
scientific validity; Stage 2 (Deployment) items V7, V8, V10, V11 address economic viability.
Three empirical failure modes are detected by specific item subsets: bull bias (V1, V2),
statistical-economic disconnect (V4–V6), and cost illusion (V7, V8, V11). A strategy
passing Stage 1 but failing Stage 2 exhibits the statistical-economic disconnect.
5. Empirical Validation: Three Failure Modes
326
5.1. Methodology and Notation
327
We deliberately employ standard, well-documented model architectures
328
rather than novel ones, as our objective is to evaluate validation methodology,
329
not to propose new prediction algorithms. This subsection defines the key
330
methods used throughout our experiments.
331
14


## Page 16

5.1.1. Triple Barrier Labeling
332
Following López de Prado (2018), each observation is assigned a label
333
yi ∈{−1, 0, +1} based on the first barrier touched by the price path after
334
event time ti. Let pt denote the price at time t. Three barriers are defined:
335
Upper:
pti+τ ≥pti(1 + θu)
(1)
Lower:
pti+τ ≤pti(1 −θl)
(2)
Vertical:
τ = Tmax
(3)
where τ > 0 is the elapsed time since the event, so that pti+τ is the price
336
τ periods after ti and the label is set by whichever of the three conditions
337
holds at the smallest τ; θu, θl > 0 are profit-taking and stop-loss thresholds
338
scaled to ˆσ, the exponentially weighted estimate of local return volatility at ti
339
(θu = 2.0ˆσ, θl = 2.5ˆσ in our daily configuration; Equations 1–3); and Tmax is
340
the maximum holding period. Events are sampled via CUSUM filtering on
341
cumulative log-returns with threshold h.
342
5.1.2. Combinatorial Purged Cross-Validation (CPCV)
343
Given N chronologically ordered groups and a test size of k groups,
344
CPCV generates
 N
k

unique train-test combinations, each respecting temporal
345
ordering with purge and embargo periods to prevent information leakage.
346
In our configuration (N = 6, k = 2), this yields
 6
2

= 15 combinations,
347
producing ϕ = (k/N)
 N
k

= 5 non-overlapping backtest paths. For each
348
combination j, a model is trained on the N −k training groups and evaluated
349
on the k test groups, producing an out-of-sample Sharpe ratio SR(j)
OOS.
350
5.1.3. Probability of Backtest Overfitting (PBO)
351
Let M denote the number of candidate configurations evaluated in the
352
search. For each CPCV path, the in-sample-best configuration is identified
353
and its out-of-sample rank ω(j) ∈{1, . . . , M} is recorded. The relative rank is
354
normalized as ¯ω(j) = ω(j)/(M + 1) to avoid boundary values. PBO is defined
355
as:
356
PBO =
1
 N
k

(N
k)
X
j=1
1

logit(¯ω(j)) ≤0

(4)
where logit(x) = ln(x/(1 −x)). PBO ≈0 indicates that in-sample-best config-
357
urations tend to rank in the top half out-of-sample; PBO ≈1 indicates severe
358
overfitting (Equation 4; Bailey et al. 2017).
359
15


## Page 17

5.1.4. Parameter-Space Variance
360
To diagnose how much configurations differ in-sample (Witzany, 2021),
361
we compute the variance of in-sample Sharpe ratios across all tested configu-
362
rations:
363
Var(SRIS) =
1
M −1
M
X
m=1

SR(m)
IS −SRIS
2
(5)
where SR(m)
IS
is the in-sample Sharpe ratio of configuration m and SRIS their
364
mean over the M configurations. Low Var(SRIS) relative to a null distribution
365
(Equation 5) indicates that all configurations perform similarly, rendering
366
PBO = 0 uninformative rather than reassuring.
367
5.2. Strategy Universe
368
Our 340 strategy variants1 are constructed as shown in Table 6:
369
Table 6: Composition of the 340-variant strategy universe.
Component
Description
Count
(a)
SHAP-derived rule combinations (applied to momentum benchmark)
64
(b)
Order flow features (individual + multi-asset)
55
(c)
External/on-chain/macro feature sets
45
(d)
ML pipeline: 3 assets × 4 TF × 3 tree families
36
(e)
Triple Barrier parameter sensitivity
36
(f)
Cross-section momentum configurations
24
(g)
Cost sensitivity & traditional baselines
24
(h)
Deep learning: 3 assets × 2 TF × 5 arch. (Transformer, LSTM, TCN, MLP×2)
30
(i)
VALID ablation configurations
12
(j)
Volatility prediction overlays
8
(k)
Bull bias analysis (tree + DL)
6
Total unique configurations
340
Component (a) uses SHAP feature attributions (Lundberg and Lee, 2017)
370
to derive interpretable trading rules from gradient-boosted models. Com-
371
ponents (a)–(k) span three cryptocurrency assets (BTC, ETH, SOL), four
372
timeframes (15-minute to daily), and eight model families (CatBoost, Light-
373
GBM, Random Forest, Transformer, bidirectional LSTM, TCN, MLP 2-layer,
374
1The corpus includes 18 cost-level entries (a rule-based benchmark and two signal proxies
evaluated at six cost levels each). Excluding them, 55.0% of the remaining 322 variants are
negative net of costs and 11 exceed the benchmark, one of which is the benchmark’s own
entry in the baseline block; all corpus-level conclusions are unchanged.
16


## Page 18

MLP 3-layer). Bull bias analysis (component k) additionally includes unidi-
375
rectional LSTM and SimpleRNN. Each was evaluated with 18 bp round-trip
376
costs. Apart from the 18 cost-level entries described in footnote 1, all variants
377
were executed through the full ML pipeline.
378
5.3. Failure Mode 1: Bull Bias
379
5.3.1. Experimental Setup
380
We train gradient-boosted tree models (CatBoost (Prokhorenkova et al.,
381
2018), LightGBM (Ke et al., 2017), Random Forest) and deep learning models
382
(2-layer LSTM, SimpleRNN) on hourly OHLCV data for BTC, ETH, and
383
SOL with Triple Barrier labeling and CUSUM filtering (López de Prado,
384
2018). All tree-based methods follow the gradient boosting framework of
385
Friedman (2001), with CatBoost’s ordered boosting (Dorogush et al., 2018)
386
and XGBoost’s regularized objective (Chen and Guestrin, 2016) representing
387
the two dominant implementations in recent crypto ML studies.
388
5.3.2. Results
389
Table 7 presents the results.
390
Table 7: Bull bias across assets and model families.
Asset (Model)
Unbal. Long%
Bal. Long%
AUC (u)
AUC (b)
Net SR
BTC (CatBoost)
97.2%
42.3%
0.502
0.501
−0.877
BTC (LSTM)
57.7%
52.3%
0.518
0.519
−1.149
BTC (SimpleRNN)
63.3%
—
—
0.520
—
ETH (CatBoost)
90.5%
45.2%
0.501
0.493
−1.283
SOL (CatBoost)
97.0%
32.2%
0.533
0.511
−0.206
Tree-based models exhibit extreme long bias (90–97%) while deep learning
391
shows moderate-to-strong bias (58–86% across seven architectures including
392
Transformer, bidirectional LSTM, and TCN). AUC is indistinguishable from
393
random (0.50–0.52) across all model families. Bull bias extends the observation
394
of Jaquart et al. (2021) to a systematic, multi-asset, multi-model phenomenon
395
(see Figure 3).
396
5.3.3. Extended Multi-Asset Analysis
397
To confirm that bull bias is not an artifact of a single asset, timeframe,
398
or model family, we extend the evaluation to 18 asset-timeframe-model
399
17


## Page 19

BTC
CatBoost
ETH
CatBoost
SOL
CatBoost
BTC
LSTM
0
25
50
75
100
Predicted "long" (%)
(a) Directional prediction share
BTC
CatBoost
ETH
CatBoost
SOL
CatBoost
BTC
LSTM
0.44
0.46
0.48
0.50
0.52
0.54
AUC after balancing
(b) Discriminative power after balancing
0.501
0.493
0.511
0.519
Unbalanced
Balanced
No-skill reference (50% share, 0.50 AUC)
Figure 3: Bull bias, computed from the 340-variant corpus (the same rows as Table 7).
(a) Share of test observations predicted “long” without and with class balancing: tree
models fall from 90–97% to 32–45%, the LSTM from 57.7% to 52.3%. (b) AUC after
balancing sits at chance level (0.493–0.519) for every model.
Table 8: Extended multi-asset bull bias (18 combinations).
Asset
Mean Unbal. Long%
Mean Bal. Long%
Mean AUC (bal)
Mean Net SR
BTC
85%
47%
0.484
−0.174
ETH
83%
52%
0.563
+0.023
SOL
80%
45%
0.542
+0.441
18


## Page 20

combinations: 3 assets × 2 timeframes (1-hour, daily) × 3 model families
400
(CatBoost, LightGBM, Random Forest). Table 8 summarizes the results.
401
All assets exhibit unbalanced long ratios of 80–97% across all models and
402
timeframes. Critically, class balancing eliminates directional bias but does
403
not improve predictive power: balanced AUC remains indistinguishable from
404
random (0.48–0.56) across all 18 asset-model combinations, and mean net SR
405
is negative for BTC (−0.174). All 1-hour models receive PBO = 1.000. The
406
phenomenon is timeframe-invariant and asset-invariant.
407
5.4. Failure Mode 2: Statistical-Economic Disconnect
408
5.4.1. The Disconnect
409
The order-flow 1h CatBoost run illustrates why Stage 1 requires more
410
than significance testing. The model passes the permutation test decisively
411
(p = 0.000; AUC 0.570 vs. a shuffled 95th percentile of 0.516): genuine
412
signal exists. Its net SR of +0.135 against a benchmark of 0.917 already
413
signals economic irrelevance—but a reviewer applying only significance tests
414
would not see this coming.
CPCV does: the same run’s PBO is 0.267,
415
failing V4’s threshold. Selection on in-sample performance is not merely
416
uninformative here but actively misleading: across CPCV configurations, the
417
Spearman correlation between IS and OOS Sharpe is ρ = −0.83 (p = 0.005,
418
n = 9 configurations), corroborated by the walk-forward analysis (ρ = −0.73,
419
n = 26). Both statistics are configuration-level; we do not report a fold-level
420
correlation. This aligns with Harvey et al. (2016) and Novy-Marx and Velikov
421
(2016) on statistical-economic gaps (see Figure 4).
422
5.4.2. Parameter-Space Variance: Evidence Consistent with Witzany (2021)
423
Witzany (2021) demonstrated theoretically that CSCV/PBO exhibits neg-
424
ative bias when strategies have similar returns. Arian et al. (2024) compared
425
CPCV variants but did not measure Var(SRIS) under null conditions.
426
We address this gap using 200-iteration Monte Carlo simulation (Section 6).
427
Table 9 compares the real and null distributions:
428
The real data’s parameter-space variance falls below the Monte Carlo null
429
distribution, but it exceeds the absolute flatness threshold of 0.01 that the
430
same computation applies. Here the two flatness criteria disagree (absolute
431
threshold 0.01 vs. MC null 95th percentile 0.328), illustrating why V5 requires
432
the null to be pre-specified rather than derived after the fact. This provides
433
empirical evidence consistent with Witzany’s analysis of PBO under similar
434
19


## Page 21

0.45
0.50
0.55
0.60
0.65
AUC (balanced)
0.0
0.2
0.4
0.6
0.8
1.0
PBO
V4 accepts below 0.20
AUC 0.55
all 209 variants
at PBO = 1.000
(a) PBO against the V4 threshold
0.0
0.2
0.4
0.6
Var(SRIS)
0
5
10
15
20
25
30
Monte Carlo iterations
(b) Real value against the null
Real data: 0.012
Absolute flatness: 0.01
Null 95th pct: 0.328
Figure 4: The PBO paradox. (a) PBO against AUC for the 209 corpus variants for which
PBO was computed. Every one receives PBO of exactly 1.000—the ceiling, and five times
the 0.20 below which V4 accepts—while AUC clusters at chance. (b) Parameter-space
variance: the real data’s Var(SRIS) of 0.012 falls below the Monte Carlo null distribution
(n = 200, 95th percentile 0.328) while remaining above the absolute flatness threshold of
0.01—the two criteria disagree (Section 5.4.2).
Table 9: Parameter-space variance: real vs. null across four settings. †The real-data figure
is computed on the 1-hour balanced pipeline (the base configuration without order-flow
features), as the mean within-fold variance of in-sample Sharpe across model configurations.
Setting
Real Data
Null Mean
Null 95th pctl
BTC 1h†
0.012
0.176
0.328
ETH 1h
—
0.262
0.534
SOL 1h
—
0.296
0.617
BTC daily
—
0.176
0.328
20


## Page 22

strategy returns; it is not a verdict that our own parameter landscape is flat.
435
An analytically derived acceptance threshold remains open.
436
5.4.3. Monte Carlo Confirmation
437
Monte Carlo analysis (Section 6) confirms these findings on synthetic
438
data: AUC-based validation alone produces 27% false positives, while PBO
439
eliminates all false positives (0% FPR, upper bound 1.9%). Full results are
440
reported in Table 13.2
441
5.5. Failure Mode 3: Cost Illusion
442
5.5.1. Cross-Timeframe Cost Analysis
443
Table 10 reports net Sharpe ratios at 18 bp for the model variants of the
444
corpus, grouped by trading frequency.
445
Table 10: Net Sharpe ratio (18 bp round-trip) of model variants in the 340-variant corpus,
by trading frequency. Benchmark (DM): 0.917.
Frequency
n
Median
Best
Share < 0
15-minute
9
−1.80
−1.33
100%
1-hour
133
−1.32
+0.32
96%
4-hour
9
+0.28
+0.57
44%
Daily
77
+0.54
+1.98
22%
Model variants only; cost-level and rule-baseline rows of
the corpus are excluded (Table 11).
Net performance degrades monotonically with trading frequency. The
446
median 15-minute variant returns SR = −1.80 and all nine lose money after
447
costs, whereas the median daily variant returns +0.54. Only daily-frequency
448
variants exceed the DM benchmark at all (best 1.98); the best hourly variant
449
reaches 0.32. In the one run where gross and net Sharpe are directly com-
450
parable, transaction costs consume 82% of the gross Sharpe ratio (0.750 →
451
0.135) at 101 trades per year.
452
Our 18 bp fixed round-trip cost is conservative for hourly and daily
453
frequencies (Binance taker fee: 10 bp + estimated slippage of 5–10 bp;
454
2Permutation test results are based on the first 100 iterations (n = 100); all other criteria
are evaluated across all 200 iterations.
21


## Page 23

Almeida and Gonçalves 2024). For sub-hourly frequencies, volume-dependent
455
slippage models (Almgren and Chriss, 2001) would further erode returns,
456
strengthening rather than weakening our conclusions.
457
5.5.2. Comparison with Traditional Baselines
458
To ensure fair comparison across different trading frequencies, we group
459
baselines by rebalancing frequency (Table 11) and compare each ML variant
460
against a frequency-matched alternative.
461
Table 11: Strategy comparison by frequency band (18 bp round-trip costs).
Frequency
Strategy
CAGR
MDD
SR (net)
Trades/yr
Low (monthly)
Dual momentum†
42.8%
−51.3%
0.917
9.7
SMA 200 crossover
33.1%
−64.6%
0.723
7.6
Medium (daily)
RSI(14) > 50
38.4%
−54.1%
0.804
44.0
MACD crossover
25.2%
−55.0%
0.613
26.2
Passive
Buy & Hold
30.6%
−76.6%
0.618
0.1
†Upper-bound reference following Antonacci (2014); monthly rebalancing not directly comparable to intraday ML.
Every rule-based baseline in Table 11 outperforms the median model
462
variant at its own frequency band (Table 10): RSI(14) reaches SR = 0.804 at
463
44 trades per year and MACD 0.613 at 26, while the median hourly model
464
variant returns −1.32. The dual momentum benchmark serves as an upper-
465
bound reference; its superior SR reflects lower turnover (9.7 trades/year)
466
rather than superior signal quality. Cross-section momentum strategies (24
467
configurations across 7 lookback periods and 3 portfolio sizes) similarly fail,
468
with only 4 of 24 achieving SR > 0 (see Figures 5 and 6).
469
5.6. Ablation Analysis: Which VALID Items Matter Most?
470
Table 12 presents the ablation results.
471
V4 (CPCV/PBO) is the single most important item. Its removal causes
472
FPR to increase from 0% to 27%.
473
6. Monte Carlo False Positive Analysis
474
6.1. Motivation and Definitions
475
The empirical results in Section 5 demonstrate failure modes on real data,
476
but a natural question arises: how often would standard validation tools
477
22


## Page 24

Calm (65% of days)
Stressed (35% of days)
0.0
0.2
0.4
0.6
0.8
1.0
1.2
1.4
1.6
Net Sharpe ratio
0.69
0.51
+0.18
1.40
0.79
+0.61
DM benchmark
Buy-and-hold
Figure 5: Regime-conditional performance under a two-state Gaussian HMM on 21-day
rolling volatility. The momentum benchmark earns SR = 1.40 in stressed regimes (35% of
evaluation days) versus 0.79 for buy-and-hold, and 0.69 versus 0.51 in calm periods: the
spread widens from +0.18 to +0.61 under stress. No regime-conditional Sharpe ratio was
computed for the model variants, so none is shown.
−3
−2
−1
0
1
2
Net Sharpe ratio (18 bp round-trip)
0
5
10
15
20
25
30
35
Number of strategy variants
52% negative
4.4% above
benchmark
Negative net SR
Positive net SR
DM benchmark (SR = 0.917)
Break-even (SR = 0)
Figure 6: Distribution of net Sharpe ratios across the 340 strategy variants at 18 bp
round-trip costs. Gray bars: negative net Sharpe (52%). Blue line: the DM benchmark
(SR = 0.917), which 4.4% of variants exceed.
23


## Page 25

Table 12: Ablation: false positive rates by VALID item removal.
Configuration
Items Removed
FPR
95% Wilson CI
Full VALID
None
0.0%
[0.0%, 1.9%]
No CPCV/PBO
−V4
27.0%
[21.3%, 33.5%]
No balancing
−V2
0.0%
[0.0%, 5.8%]
No cost adj.
−V7
0.0%
[0.0%, 1.9%]
No permutation
−V6
0.0%
[0.0%, 1.9%]
produce false positives on data with no embedded signal? We address this
478
through Monte Carlo simulation.
479
We define a false positive as a null (signal-free) dataset on which a given
480
validation criterion incorrectly indicates the presence of a tradable signal.
481
Specifically, for each criterion C and null dataset i, let FPi = 1[Ci passes].
482
The false positive rate is:
483
FPR(C) = 1
n
n
X
i=1
FPi
(6)
with 95% Wilson confidence intervals (Wilson, 1927).
We evaluate five
484
criteria: AUC > 0.55, permutation test p < 0.05, PBO < 0.20, net SR > 0, and
485
the conjunction of all VALID items.
486
6.2. Synthetic Data Generation
487
We generate n = 200 synthetic BTC price series by bootstrapping (Efron
488
and Tibshirani, 1993) daily log-returns (2017–2026, 3,132 observations per
489
series). The bootstrap preserves the marginal distribution of returns (mean,
490
variance, skewness, kurtosis) while destroying temporal dependence, ensuring
491
that any predictive signal detected by the ML pipeline is spurious by con-
492
struction. We use simple i.i.d. resampling rather than block or stationary
493
bootstrap (Politis and Romano, 1994), as our goal is to eliminate all temporal
494
structure. The choice of n = 200 yields Wilson CI half-widths of ±6% at
495
FPR = 27%, providing sufficient precision to distinguish informative from
496
uninformative validation criteria.
497
6.3. Pipeline Application
498
Each synthetic series passes through the identical pipeline used for real
499
data: (a) compute 17 price-derived technical features (returns, volatility,
500
24


## Page 26

momentum indicators); (b) generate Triple Barrier labels with CUSUM
501
filtering; (c) train CatBoost with class-balanced sample weights; (d) evaluate
502
via CPCV (N = 6, k = 2, yielding 15 train-test combinations); (e) record AUC,
503
PBO, Var(SRIS), permutation p-value, and net SR (18 bp round-trip cost).
504
The pipeline is deterministic given the input data; no hyperparameter tuning
505
is performed within the Monte Carlo loop.
506
6.4. Results
507
Mean AUC across 200 null iterations is 0.506 ± 0.070, confirming that
508
the pipeline produces near-chance classification on signal-free data. However,
509
individual criteria show dramatically different false positive rates (Table 13;
510
Equation 6). The 27% AUC-based FPR, combined with the audit finding
511
that no empirical paper in our sample uses CPCV, suggests a substantial
512
fraction of published positive results may reflect statistical artifacts. Critically,
513
PBO < 0.20 alone achieves 0% FPR [0%, 1.9%], confirming its value as the
514
primary overfitting diagnostic and justifying its central role in VALID (Item
515
V4).
516
To confirm generalizability, we replicate the Monte Carlo analysis across
517
three additional settings: ETH 1h, SOL 1h, and BTC daily (Table 13).
518
AUC-based FPR ranges from 26.5% to 30.0% across all four settings, while
519
PBO-based FPR remains 0.0% in every case. The consistency of these results
520
across assets (BTC, ETH, SOL) and timeframes (hourly, daily) confirms that
521
the findings are asset-invariant and timeframe-invariant: standard validation
522
criteria produce false positives at similar rates regardless of the underlying
523
data, and CPCV with PBO eliminates them universally.
524
Table 13: False positive rates on null data (n = 200 per setting). BTC 1h is the primary
setting; three additional settings confirm generalizability. Column labels follow the original
run names: all four settings were generated from daily-bar bootstrap series (838–919 events
per series), a label mismatch recorded in the repository’s REPRODUCE.md. The conclusion
is unaffected—every setting yields 0% under CPCV with PBO.
Criterion
BTC 1h
ETH 1h
SOL 1h
BTC daily
AUC > 0.55 alone
27.0%
30.0%
26.5%
27.0%
Permutation passed
22.0%
19.0%
18.0%
20.0%
PBO < 0.20 alone
0.0%
0.0%
0.0%
0.0%
Net SR > 0 alone
49.5%
52.0%
52.5%
49.5%
Full VALID
0.0%
0.0%
0.0%
0.0%
25


## Page 27

6.5. Multiple Testing Correction
525
The Monte Carlo analysis quantifies false positives on signal-free data. A
526
complementary question is what survives on the real corpus once the number
527
of trials is taken into account. Of the 340 variants, 15 (4.4%) exceed the
528
benchmark before correction, of which 10 are model variants; the remaining
529
five are benchmark entries of the cost-level and baseline blocks. We convert
530
each variant’s excess Sharpe to a t-statistic following Lo (2002) and apply
531
five corrections: Bonferroni (N = 340, α = 0.05) leaves 9 survivors, Holm-
532
Bonferroni 9, Benjamini-Hochberg FDR 10, the Harvey et al. (2016) t > 3.0
533
threshold 10, and the Deflated Sharpe Ratio (Bailey and López de Prado,
534
2014) 0.
535
Cross-referencing the nine Bonferroni survivors against CPCV gives the
536
central result: every one exhibits PBO = 1.0, with t-statistics from 4.07 to
537
21.70 and AUC values between 0.47 and 0.64. All nine operate at the daily
538
timeframe. The Deflated Sharpe Ratio, which accounts for the expected
539
maximum Sharpe under N trials (E[max] = 2.93), rejects all 340: the best
540
observed Sharpe of 1.98 falls below the noise threshold. Classical corrections
541
control familywise or false-discovery error under independence, but they can-
542
not detect backtest overfitting—a strategy can satisfy t > 21 and PBO = 1.0
543
simultaneously. This is the corpus-level form of the disconnect documented
544
in Section 5.4.2, and it is why VALID places CPCV with PBO (Item V4) in
545
Stage 1 rather than treating multiple-testing correction as sufficient.
546
7. Discussion
547
7.1. Implications for the Field
548
Our findings have four implications. First, the crypto ML literature likely
549
contains a substantial false positive rate—across our 340 strategy variants,
550
52% produce negative net Sharpe ratios after realistic transaction costs, and
551
15 variants (4.4%) exceed the simple momentum benchmark (SR = 0.917),
552
of which 10 are model variants; the remaining five are benchmark entries
553
of the cost-level and baseline blocks. Second, our Monte Carlo analysis of
554
the Var(SRIS) null distribution provides evidence consistent with Witzany’s
555
(2021) theoretical critique of PBO. Third, the statistical-economic disconnect
556
is not a failure of existing tools but a gap in how they are applied. Fourth, the
557
VALID framework addresses a genuine gap—no existing reporting standard
558
covers financial-ML-specific pitfalls.
559
26


## Page 28

7.1.1. Adoption Barriers
560
The VALID framework imposes computational and reporting overhead
561
that may deter adoption, particularly for research groups without access to
562
high-performance computing. CPCV with
 6
2

= 15 combinations requires 15
563
full model training runs per configuration, and Monte Carlo analysis with
564
200 iterations multiplies this further. We view this cost as appropriate: if a
565
validation procedure is too expensive to run, the strategy search itself may be
566
too expansive to be trustworthy. Nonetheless, we acknowledge that pragmatic
567
compromises—such as reducing N or using fewer Monte Carlo iterations—may
568
be necessary for large-scale strategy searches, provided authors disclose the
569
reduced scope.
570
7.1.2. Relationship to Publication Incentives
571
The failure modes documented in this paper are not primarily technical
572
failures but incentive failures. Journals and conferences reward novelty and
573
positive results; negative results—such as our finding that 52% of strategy
574
variants produce negative net returns—are difficult to publish. The VALID
575
framework cannot resolve this structural problem, but by mandating disclosure
576
of class distributions, cost-adjusted performance, and baseline comparisons,
577
it raises the evidentiary bar for claiming positive results.
We note that
578
analogous reporting standards in clinical research (CONSORT; Moher et al.,
579
2010; Collins et al., 2015) have measurably improved methodological quality
580
over time, though compliance remains imperfect.
581
7.1.3. Generalizability Beyond Cryptocurrency
582
While our empirical validation focuses on cryptocurrency markets, the
583
three failure modes—directional prediction bias, statistical-economic discon-
584
nect, and cost illusion—are not crypto-specific. Bull bias arises whenever
585
training labels are imbalanced, which occurs in any trending asset class. The
586
statistical-economic disconnect exists wherever statistical validation tools
587
lack economic grounding. Cost illusion affects any strategy with non-trivial
588
turnover. We expect VALID to be applicable, with minor parameter ad-
589
justments, to equity factor models, FX strategies, and commodity trading
590
algorithms.
591
7.2. Limitations
592
Our analysis is subject to several limitations. First, we evaluate three
593
cryptocurrency assets (BTC, ETH, SOL); extending to a broader universe
594
27


## Page 29

including equities, foreign exchange, or fixed income would strengthen gen-
595
eralizability claims. Second, the VALID framework has not been validated
596
through a formal expert consensus process such as a Delphi study, which
597
is standard for clinical reporting guidelines (TRIPOD, CONSORT). Third,
598
the momentum benchmark operates at monthly rebalancing frequency while
599
ML strategies trade hourly to daily; although we provide frequency-matched
600
comparisons using RSI and MACD (Table 11), the cross-frequency comparison
601
warrants caution. Fourth, our deep learning evaluation covers five architec-
602
tures but omits Temporal Fusion Transformers (Lim et al., 2021) and graph
603
neural networks, which may exploit cross-asset dependencies not captured
604
here. Fifth, the literature audit was conducted by a single coder without
605
independent inter-rater reliability assessment, introducing potential coding
606
bias. Sixth, the audit covers only published and indexed papers, creating
607
survivorship bias—unpublished negative results are absent by construction.
608
Seventh, our 18 bp fixed cost model, while conservative for hourly and daily fre-
609
quencies, does not capture the volume-dependent slippage dynamics relevant
610
to sub-minute execution.
611
7.3. Future Work
612
Three extensions merit investigation. First, applying VALID retroactively
613
to highly cited papers would quantify how many published results survive rig-
614
orous validation. Second, extending the framework to reinforcement learning
615
strategies—which face additional challenges in reward shaping and environ-
616
ment non-stationarity—would broaden applicability. Third, developing an
617
automated VALID compliance tool, analogous to existing TRIPOD adherence
618
checkers, would lower adoption barriers.
619
8. Conclusion
620
We propose VALID which, to our knowledge, is the first checklist-style
621
protocol for financial ML that pairs binary statistical and economic gates
622
in a fixed reporting order. Through a systematic audit of 80 papers, 340
623
strategy variants across three assets and four timeframes, 800-iteration Monte
624
Carlo analysis across four asset-timeframe settings, and ablation testing,
625
we demonstrate three systematic failure modes: bull bias (90–97% for tree
626
models, 58–86% across seven deep learning architectures), statistical-economic
627
disconnect, and cost illusion (net Sharpe falling monotonically with trading
628
frequency), with 52% of all tested variants producing negative returns after
629
28


## Page 30

costs and 15 (4.4%) exceeding a simple momentum benchmark, of which 10
630
are model variants. Nine variants survive Bonferroni correction—all with
631
PBO = 1.0—and none survives the Deflated Sharpe Ratio. Our Var(SRIS) null-
632
distribution analysis (real 0.012, null 95th percentile 0.328) provides evidence
633
consistent with Witzany’s (2021) PBO critique. The VALID framework’s 12
634
items would establish minimum reporting standards for a field that currently
635
lacks them.
636
In a field where positive results are rewarded and negative results are
637
invisible, the most important validation is the discipline to accept that a
638
statistically detectable signal is not the same as a tradable edge.
639
CRediT Authorship Contribution Statement
640
Jaewook Kim: Conceptualization, Methodology, Software, Validation,
641
Formal analysis, Investigation, Data curation, Writing – original draft, Writing
642
– review & editing, Visualization.
643
Declaration of Competing Interest
644
The author declares that there is no known competing financial interest or
645
personal relationship that could have appeared to influence the work reported
646
in this paper.
647
Acknowledgments
648
The author thanks the anonymous reviewers for their constructive feed-
649
back.
650
Funding
651
This research did not receive any specific grant from funding agencies in
652
the public, commercial, or not-for-profit sectors.
653
Data Availability
654
Bitcoin, Ethereum, and Solana OHLCV data were obtained from
655
Binance and Bybit public APIs via the CCXT library.
Macro in-
656
dicators were obtained from Yahoo Finance.
The literature audit
657
coding sheet (audit/literature_audit_80.csv), the 340-variant corpus
658
29


## Page 31

(results/reference/variants_340.csv) and the scripts that recompute
659
every published corpus figure (scripts/) are in the public repository; Monte
660
Carlo per-iteration results are provided in supplementary materials. Source
661
code is available at https://github.com/orcajae/valid-framework.
662
Appendix A: VALID Self-Assessment
663
To demonstrate the framework’s application, Table 14 applies VALID to
664
the present study. This self-assessment serves as a worked example for future
665
adopters.
666
V5 is partial because the absolute and null-relative flatness criteria disagree
667
for our own pipeline (Section 5.4.2); V8 is partial because all corpus variants
668
are evaluated at a single 18 bp cost level, so we report a frequency ladder
669
rather than a cost sweep of our own strategies; V10 remains partial: the
670
regime analysis covers two volatility states on three cryptocurrency assets.
671
This self-assessment was revised downward after auditing our own submission
672
against VALID.
673
Table 14: VALID self-assessment applied to this study.
#
Item
Status
Evidence
V1
Class distribution reported
✓
Table 7: 90–97% long
V2
Balanced/unbalanced comparison
✓
Tables 7, 8
V3
Temporal splitting only
✓
CPCV with purge & embargo
V4
CPCV with PBO
✓
N = 6, k = 2, 15 combinations
V5
Var(SRIS) reported
∼
Table 9: criteria disagree
V6
Permutation tests
✓
p = 0.000; n = 100 (meets the
≥100 floor; 200 in three of four
settings)
V7
Net performance with costs
✓
18 bp RT; Table 10
V8
Cost sensitivity analysis
∼
Single 18 bp level; Section 5.5
V9
Simple baselines
✓
RSI, MACD, SMA in Table 11
V10
Bear market evaluation
△
Figure 5: two regimes only
V11
Trade frequency reported
✓
Trades/yr in Table 11
V12
Code available
✓
GitHub repository linked
Total
9/12
3 partial
30


## Page 32

Appendix B: Supplementary Materials
674
Supplementary materials include:
(A) complete 340-variant perfor-
675
mance results; (B) VALID framework implementation code; (C) the
676
complete 80-paper coding sheet,
available in the public repository
677
(audit/literature_audit_80.csv); (D) Monte Carlo simulation details
678
and per-iteration results (200 iterations).
679
References
680
Alessandretti, L., ElBahrawy, A., Aiello, L.M., Baronchelli, A., 2018. Antic-
681
ipating cryptocurrency prices using machine learning. Complexity 2018,
682
8983590.
683
Almeida, J., Gonçalves, T.C., 2024. Cryptocurrency market microstructure:
684
A systematic literature review. Annals of Operations Research .
685
Almgren, R., Chriss, N., 2001. Optimal execution of portfolio transactions.
686
Journal of Risk 3, 5–39. doi:10.21314/JOR.2001.041.
687
Antonacci, G., 2014. Dual Momentum Investing. McGraw-Hill.
688
Arian, H.R., Mobarekeh, D.N., Seco, L., 2024. Backtest overfitting in the
689
machine learning era: A comparison of out-of-sample testing methods in a
690
synthetic controlled environment. Knowledge-Based Systems 305, 112477.
691
Bailey, D.H., Borwein, J.M., López de Prado, M., Zhu, Q.J., 2017. The
692
probability of backtest overfitting. Journal of Computational Finance 20,
693
39–69.
694
Bailey, D.H., López de Prado, M., 2014. The deflated Sharpe ratio. Journal
695
of Portfolio Management 40, 94–107.
696
Blitz, D., Hanauer, M.X., Honarvar, I., Huisman, R., van Vliet, P., 2023.
697
Beyond Fama-French factors: Alpha from short-term signals. Financial
698
Analysts Journal 79, 96–117.
699
Borrageiro, G., Firoozye, N., Barucca, P., 2022. Reinforcement learning for
700
systematic FX trading. Expert Systems with Applications 195, 116522.
701
31


## Page 33

Cakici, N., Shahzad, S.J.H., Będowska-Sójka, B., Zaremba, A., 2024. Machine
702
learning and the cross-section of cryptocurrency returns. International
703
Review of Financial Analysis 94, 103244.
704
Chen, A.Y., Velikov, M., 2023. Zeroing in on the expected returns of anomalies.
705
Journal of Financial and Quantitative Analysis 58, 968–1004.
706
Chen, T., Guestrin, C., 2016. XGBoost: A scalable tree boosting system, in:
707
Proceedings of KDD, pp. 785–794.
708
Collins, G.S., Moons, K.G.M., Dhiman, P., Riley, R.D., Beam, A.L., Van Cal-
709
ster, B., Ghassemi, M., Liu, X., Reitsma, J.B., van Smeden, M., Boulesteix,
710
A.L., Camaradou, J.C., Celi, L.A., Denaxas, S., Denniston, A.K., Glocker,
711
B., Golber, R., Harvey, H., Heinze, G., Hoffman, M.M., Kengne, A.P.,
712
Lam, E., Lee, N., Loder, E.K., Maier-Hein, L., Manniesing, B., McCradden,
713
M.D., Msosa, L., Navarro, J.L.D., Reyes, M., Roßnagel, K., Singh, A.,
714
Wynants, L., Logullo, P., 2024. TRIPOD+AI statement: updated guidance
715
for reporting clinical prediction models that use regression or machine
716
learning methods. BMJ 385, e078378. doi:10.1136/bmj-2023-078378.
717
Collins, G.S., Reitsma, J.B., Altman, D.G., Moons, K.G.M., 2015. Transpar-
718
ent reporting of a multivariable prediction model for individual prognosis
719
or diagnosis (TRIPOD). Annals of Internal Medicine 162, 55–63.
720
Dorogush, A.V., Ershov, V., Gulin, A., 2018. CatBoost: Gradient boosting
721
with categorical features support. arXiv preprint arXiv:1810.11363 .
722
Efron, B., Tibshirani, R.J., 1993. An Introduction to the Bootstrap. Chapman
723
& Hall. doi:10.1007/978-1-4899-4541-9.
724
Fang, F., Ventre, C., Basios, M., Kanthan, L., Martinez-Rego, D., Wu, F.,
725
Li, L., 2022. Cryptocurrency trading: A comprehensive survey. Financial
726
Innovation 8, 13.
727
Fieberg, C., Hornuf, L., Merkle, M., Treitz, T., 2025. Cryptocurrency factor
728
momentum. Journal of Financial and Quantitative Analysis 60, 3116–3153.
729
doi:10.1017/S0022109024000516.
730
Friedman, J.H., 2001. Greedy function approximation: A gradient boosting
731
machine. Annals of Statistics 29, 1189–1232.
732
32


## Page 34

Grądzki, R., Korzeniewski, J., Szymczyk, M., 2025. Algorithmic crypto
733
trading using information-driven bars. Financial Innovation 11, 136. doi:10.
734
1186/s40854-025-00866-w.
735
Grobys, K., Junttila, J., Kolari, J.W., Sapkota, N., 2025. Cryptocurrency
736
momentum has (not) its moments. Financial Markets and Portfolio Man-
737
agement Forthcoming.
738
Gu, S., Kelly, B., Xiu, D., 2020. Empirical asset pricing via machine learning.
739
Review of Financial Studies 33, 2223–2273.
740
Hansen, P.R., 2005. A test for superior predictive ability. Journal of Business
741
& Economic Statistics 23, 365–380.
742
Harvey, C.R., Liu, Y., Zhu, H., 2016. . . . and the cross-section of expected
743
returns. Review of Financial Studies 29, 5–68.
744
Hou, K., Xue, C., Zhang, L., 2020. Replicating anomalies. Review of Financial
745
Studies 33, 2019–2133.
746
Ioannidis, J.P.A., 2005. Why most published research findings are false. PLoS
747
Medicine 2, e124.
748
Jaquart, P., Dann, D., Weinhardt, C., 2021. Short-term bitcoin market
749
prediction via machine learning. Journal of Finance and Data Science 7,
750
45–66. doi:10.1016/j.jfds.2021.03.001.
751
Jiang, J., Ye, B., Liu, J., 2024. A survey of deep learning applications in
752
cryptocurrency. Intelligent Systems with Applications 21, 200349. doi:10.
753
1016/j.iswa.2024.200349.
754
Kapoor, S., Cantrell, E., Peng, K., Pham, T.H., Bail, C.A., Gundersen, O.E.,
755
Hofman, J.M., Hullman, J., Lones, M.A., Malik, M.M., Nanayakkara, P.,
756
Poldrack, R.A., Raji, I.D., Roberts, M., Saez-Rodriguez, J., Schmidt-Hieber,
757
J., Schwartz, R., Singh, A., Szollosi, A., Valen-Sendstad, K., Narayanan,
758
A., 2024. REFORMS: Consensus-based recommendations for machine-
759
learning-based science.
Science Advances 10, eadk3452.
doi:10.1126/
760
sciadv.adk3452.
761
Kapoor, S., Narayanan, A., 2023. Leakage and the reproducibility crisis in
762
machine-learning-based science. Patterns 4, 100804.
763
33


## Page 35

Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., Liu,
764
T.Y., 2017. LightGBM: A highly efficient gradient boosting decision tree,
765
in: Advances in Neural Information Processing Systems.
766
Kim, A., Trimborn, S., Härdle, W.K., 2021. VCRIX — a volatility index for
767
crypto-currencies. International Review of Financial Analysis 78, 101915.
768
Krauss, C., Do, X.A., Huck, N., 2017. Deep neural networks, gradient-boosted
769
trees, random forests: Statistical arbitrage on the S&P 500. European
770
Journal of Operational Research 259, 689–702.
771
Lahmiri, S., Bekiros, S., 2019. Cryptocurrency forecasting with deep learning
772
chaotic neural networks. Chaos, Solitons & Fractals 118, 35–40. doi:10.
773
1016/j.chaos.2018.11.014.
774
Leung, T., Zhao, B., 2021. Cryptocurrency trading and exchanges, in: Springer
775
Handbook of Blockchain, pp. 245–275.
776
Li, Y., Urquhart, A., Wang, P., Zhang, W., 2024. Cryptocurrency factors
777
and machine learning. SSRN Working Paper .
778
Lim, B., Arík, S.Ö., Loeff, N., Pfister, T., 2021. Temporal fusion transformers
779
for interpretable multi-horizon time series forecasting. International Journal
780
of Forecasting 37, 1748–1764. doi:10.1016/j.ijforecast.2021.03.012.
781
Liu, Y., Tsyvinski, A., 2021. Risks and returns of cryptocurrency. Review of
782
Financial Studies 34, 2689–2727.
783
Lo, A.W., 2002. The statistics of Sharpe ratios. Financial Analysts Journal
784
58, 36–52.
785
Lundberg, S.M., Lee, S.I., 2017. A unified approach to interpreting model
786
predictions, in: Advances in Neural Information Processing Systems, pp.
787
4765–4774.
788
Makarov, I., Schoar, A., 2020. Trading and arbitrage in cryptocurrency
789
markets. Journal of Financial Economics 135, 293–319.
790
McLean, R.D., Pontiff, J., 2016. Does academic research destroy stock return
791
predictability? Journal of Finance 71, 5–32.
792
34


## Page 36

McNally, S., Roche, J., Caton, S., 2018. Predicting the price of Bitcoin using
793
machine learning, in: 26th Euromicro Conference on PDP, pp. 339–343.
794
Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson,
795
B., Spitzer, E., Raji, I.D., Gebru, T., 2019. Model cards for model report-
796
ing, in: Proceedings of the Conference on Fairness, Accountability, and
797
Transparency, pp. 220–229. doi:10.1145/3287560.3287596.
798
Moher, D., Hopewell, S., Schulz, K.F., Montori, V., Gøtzsche, P.C., Devereaux,
799
P.J., Elbourne, D., Egger, M., Altman, D.G., 2010. CONSORT 2010
800
explanation and elaboration. BMJ 340, c869. doi:10.1136/bmj.c869.
801
Norgeot, B., Quer, G., Beaulieu-Jones, B.K., Torkamani, A., Dias, R., Lber,
802
M., Arnaout, R., Kohane, I.S., Saria, S., Topol, E., 2020. Minimum informa-
803
tion about clinical artificial intelligence modeling: The MI-CLAIM checklist.
804
Nature Medicine 26, 1320–1324. doi:10.1038/s41591-020-1041-y.
805
Novy-Marx, R., Velikov, M., 2016. A taxonomy of anomalies and their trading
806
costs. Review of Financial Studies 29, 104–147.
807
Olorunnimbe, K., Viktor, H., 2023. Deep learning in the stock market — a
808
systematic survey of practice and research. Artificial Intelligence Review
809
56, 5427–5501.
810
Patton, A.J., Weller, B.M., 2020. What you see is not what you get. Journal
811
of Financial Economics 137, 515–549.
812
Politis, D.N., Romano, J.P., 1994. The stationary bootstrap. Journal of the
813
American Statistical Association 89, 1303–1313. doi:10.1080/01621459.
814
1994.10476870.
815
López de Prado, M., 2018. Advances in Financial Machine Learning. Wiley.
816
Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A.V., Gulin, A., 2018.
817
CatBoost: Unbiased boosting with categorical features, in: NeurIPS.
818
Schnaubelt, M., 2022. Deep reinforcement learning for the optimal placement
819
of cryptocurrency limit orders. European Journal of Operational Research
820
296, 993–1006. doi:10.1016/j.ejor.2021.04.050.
821
35


## Page 37

Sebastião, H., Godinho, P., 2021. Forecasting and trading cryptocurren-
822
cies with machine learning under changing market conditions. Financial
823
Innovation 7, 3.
824
Siami-Namini, S., Tavakoli, N., Namin, A.S., 2019. The performance of LSTM
825
and BiLSTM in forecasting time series, in: IEEE International Conference
826
on Big Data.
827
Sun, X., Liu, M., Sima, Z., 2020. A novel cryptocurrency price trend forecast-
828
ing model based on LightGBM. Finance Research Letters 32, 101084.
829
Urquhart, A., 2016. The inefficiency of Bitcoin. Economics Letters 148, 80–82.
830
doi:10.1016/j.econlet.2016.09.019.
831
Vo, A., Yuen, C., 2020. Towards multi-step cryptocurrency price prediction
832
with deep learning. Expert Systems with Applications 146, 113200.
833
White, H., 2000. A reality check for data snooping. Econometrica 68, 1097–
834
1126.
835
Wilson, E.B., 1927. Probable inference, the law of succession, and statistical
836
inference. Journal of the American Statistical Association 22, 209–212.
837
doi:10.1080/01621459.1927.10502953.
838
Witzany, J., 2021. A Bayesian approach to measurement of backtest overfitting.
839
Risks 9, 18.
840
Xu, W., Rao, J., Ren, Y., Luo, Z., Zu, Y., 2022. A machine learning approach
841
for cryptocurrency trading. Journal of King Saud University – Computer
842
and Information Sciences 34, 3322–3330. doi:10.1016/j.jksuci.2022.04.
843
006.
844
Yang, A., 2025. Cryptocurrency market risk-managed momentum strategies.
845
Finance Research Letters 71, 106402. doi:10.1016/j.frl.2024.106402.
846
Zhang, W., Li, P., Sha, D., Wang, Y., Huang, S.H., 2025. Neural network-
847
based algorithmic trading systems. arXiv preprint arXiv:2508.02356 .
848
Zhu, Y., Yang, Y., Ren, Q., 2023. Machine learning in environmental research:
849
Common pitfalls and best practices. Environmental Science & Technology
850
57, 17671–17689.
851
36


# Detecting Crypto Wash Trades via Machine Learning

- **Source File**: `ssrn-4649565.pdf`
- **Total Pages**: 52
- **SSRN ID**: `ssrn-4649565`

---


### Page 1

Detecting Crypto Wash Trades via Machine Learning
Brett Hemenway Falk, Gerry Tsoukalas, Niuniu Zhang∗
September 19, 2025
Research Policy, Forthcoming.
Abstract
Existing studies of crypto wash trading often rely on indirect statistical methods or leaked
private data.
We develop a machine learning framework that achieves trade-level detection
using public on-chain data alone. In three major NFT marketplaces, on-chain filters flag 38%
of trades and 60% of traded value as wash trades, with substantial variation across platforms.
We engineer a set of trade-level features and train tree-based and deep learning models on these
labels, achieving accurate transaction-level classification. The framework accommodates prior
aggregate estimators as features, including the trade-size roundedness regression of Cong et al.
(2023b). The methodology also applies to fungible-token trade data, as demonstrated on the
Mt. Gox Bitcoin dataset. Together, these results provide a scalable basis for on-chain market
surveillance.
Keywords:
AI, Cryptocurrency, Decision Trees, Deep Learning, Non-Fungible Tokens
(NFTs), Machine Learning, Market Manipulation, Wash Trading, Web3.
∗Hemenway Falk:
University of Pennsylvania (fbrett@cis.upenn.edu), Tsoukalas:
Boston University (ger-
ryt@bu.edu), Zhang: University of California, Los Angeles (niuniu.zhang.phd@anderson.ucla.edu)
1


### Page 2

1
Introduction
Web3 innovations hold the promise of decentralization, enhanced security, and greater transparency,
fundamentally transforming various sectors.
In particular, financial applications have arguably
been at the forefront of this transformation since their inception. While these innovations have
the potential to revolutionize the financial landscape, features such as account anonymization also
introduce challenges, including novel methods of market manipulation. At the same time, they
offer new opportunities for detecting and preventing such manipulations. For example, the on-
chain nature of transactions produces transparent data that can be analyzed using statistical and
machine learning tools. This paper explores the tension between the increased transparency offered
by these technologies and the evolving strategies for market manipulation they enable.
In traditional stock and commodity markets, wash trading has been deemed illegal since 1936.
This malpractice involves either a single actor or a coalition of actors engaging in self-directed
trades to artificially manipulate market activity, aiming to exploit these distortions for profit. The
SEC rigorously polices such activities in conventional financial markets; however, cryptocurrencies
remain less stringently regulated. The anonymization of accounts mentioned above allows crypto
traders to manipulate the appearance of market demand by easily creating and trading between
multiple anonymous accounts. Accordingly, this subject is of considerable interest and debate to
regulators, practitioners, and academics (Cong, Li, Tang and Yang 2023, Decrypt 2023, Bonifazi
et al. 2023, Morgia et al. 2023, von Wachter et al. 2022).
Addressing wash trading in cryptocurrencies presents a complex challenge.
Approximately
83.3% of crypto trades occur on private, centralized exchanges—such as Binance—that typically
conduct off-chain transactions, thereby limiting transparency (Shimron 2022). These platforms
usually provide only rudimentary details (e.g., trading pair and size) while withholding trader
identities, which complicates wash trading detection. Moreover, these exchanges may have little
incentive to curb wash trading since inflated trading volumes can be beneficial. To overcome these
2


### Page 3

challenges, current research leverages leaked insider data from hacks (Aloosh and Li 2024) and
advanced statistical methods for pattern recognition (Cong, Li, Tang and Yang 2023). The latter
study estimates that up to 70% of the traded value on certain exchanges may be attributed to wash
trading—an alarming finding. While these approaches have advanced our understanding meaning-
fully, the lack of systematic access to timely public data continues to constrain their accuracy and
their ability to capture live, ongoing market activity.
This paper seeks to bridge this gap by focusing on a specific segment of crypto markets: Non-
Fungible Tokens (NFTs). These tokens are unique for their on-chain trading nature and inherent
transaction transparency. NFTs are usually traded on decentralized exchanges, where every trans-
action is recorded on a public ledger, revealing comprehensive details including the identities (wallet
addresses) of buyers and sellers. Such transparency facilitates a more direct analysis of trading pat-
terns, better enabling the identification of practices like wash trading. Consequently, NFTs provide
a distinct advantage in data transparency and pattern identification compared to traditional cen-
tralized exchanges. In particular, NFT data can help answer several interrelated questions:
Research Questions
First, can we leverage increased NFT transparency to establish a more direct estimation method for
wash trading levels? Second, and perhaps more crucially, how do more direct estimation methods
compare to indirect statistical approaches used in studies like Cong, Li, Tang and Yang (2023)?
Do the two methodologies align, and if discrepancies exist, is there a way to reconcile them?
Data
We concentrated our data collection on three of the top NFT marketplaces: LooksRare, Blur, and
OpenSea. From these platforms, we manually amassed a comprehensive dataset encompassing all
recorded transactions. Each transaction in our dataset is represented by a single row, detailing
critical information such as the transaction hash, block number, NFT seller and buyer, the NFT
3


### Page 4

collection, tokenId, price, and date of the transaction. Additionally, we scraped one degree upstream
Ether transfers for all buyers and sellers from the sales dataset to identify possible collusion. This
rich dataset offers an insightful view into the NFT trading landscape, encapsulating a diverse range
of transactions across numerous collections. The depth of this data, covering thousands of NFT
collections and a vast number of transactions with significant total value in ETH for both platforms,
offers a comprehensive basis for our analysis of wash trading practices, allowing us to observe and
decipher patterns and anomalies indicative of such activities. The details are discussed in Section 3.
Direct Estimation
Using this dataset, we apply four distinct filters to directly estimate wash trading in NFT markets.
Filter 1 flags the simplest case, where the buyer and seller use the same wallet, indicating a direct
self-sale. Filter 2 detects back-and-forth trades—instances where buyer and seller identities are
inverted in sequential transactions—suggesting coordinated trading between two accounts. Filter
3 identifies cases where the same buyer purchases the same NFT three or more times, capturing
cyclical patterns unlikely to arise naturally. Filter 4 flags trades where both buyer and seller are
funded by the same upstream account, signaling potential control by a single entity. Figure 2 shows
these filters graphically. To reduce false positives in Filter 4, we exclude known addresses associated
with smart contracts and exchanges. See Section 4.
Indirect Estimation and Machine Learning
Leveraging our on-chain data and direct estimation results, we assess the effectiveness of indirect
estimation methods, i.e., methods that aim to classify the prevelance of wash trading, without iden-
tifying individual trades as wash trading. Building on Cong, Li, Tang and Yang (2023), we adopt
their approach and distributional tests—examining deviations in trade-size roundedness, confor-
mity to Benford’s Law, clustering around round numbers, and tail behavior—to detect potential
market manipulation. We extend these methods in two key ways. First, we enhance their regression
4


### Page 5

framework through hyperparameter optimization (see Section 5). Second, we embed the refined
regression into a broader AI-driven filter that integrates machine learning techniques, including
boosting and deep learning, with additional engineered features—such as trade price, round level,
trading frequency, and inter-trade time intervals—to predict wash trading more accurately and at
scale (see Section 6).
Results
Our results are presented as 11 key insights (I1–I11), detailed throughout the paper and summarized
in Table 1 in the literature review (Section 2). These findings highlight both the scale of NFT wash
trading and the strengths and limitations of different detection methods.
First, in Section 4, we apply our dataset and direct filters to estimate that approximately 38%
(30–40%) of trades likely involve manipulation, with results remaining remarkably consistent across
exchanges. However, these trades account for approximately 60% (25–95%) of traded value, reflect-
ing substantial variation across marketplaces (I1). Variations aside, the overall average aligns with
Cong, Li, Tang and Yang (2023), which estimates ∼70% for fungible tokens. Notably, collections
implicated in wash trading tend to exhibit inflated prices (I2), though higher wash-trade activity
does not systematically translate to greater profits for participants (I3).
Although NFTs differ structurally from cryptocurrencies, many of the incentives for wash trad-
ing remain similar. NFT marketplaces, like crypto exchanges, compete aggressively for liquidity
and trader engagement, as higher reported trading volumes enhance platform rankings and at-
tract investors. This dynamic is exemplified by Blur’s rapid rise past OpenSea through aggressive
incentives.
Additionally, NFTs introduce unique motivations for wash trading, including earn-
ing royalties per trade, benefiting from zero-fee trading models, and exploiting price opacity. On
some platforms, we find wash trading volumes even exceed those observed in crypto exchanges,
underscoring how these incentives can intensify market manipulation.
In Section 5, we adapt the roundedness regression method from Cong, Li, Tang and Yang (2023),
5


### Page 6

to NFT markets. While this approach, which we term 1-regression, is effective in certain cases, it
does not generalize seamlessly across all exchanges, leading to estimation discrepancies (I4). To
address this, we refine the method by optimizing the roundedness threshold, calibrating it to each
platform’s characteristics. This enhanced τ-regression meaningfully reduces estimation errors on
some exchanges (I5).
However, residual discrepancies persist, motivating the introduction of our AI-based approach
in Section 6, which systematically reduces error rates below 1.29%, across all exchanges. The best
models achieve AUC scores over 0.9 on NFT data (I6, I7). Notably, they perform even better
outside NFT markets (I8), particularly on the Mt. Gox dataset from Aloosh and Li (2024),1 where
the AUC score exceeds 0.97, suggesting that our approach not only generalizes but may also be
more effective in traditional fungible token markets.
Finally, in Section 7, we evaluate distributional tests—Benford’s Law, trade-size clustering, and
power-tail distributions—which serve as coarse detectors of anomalous trading rather than precise
estimators of wash trading volume. We find that both wash and legitimate NFT trades deviate
from Benford’s Law, limiting its effectiveness (I9). Similarly, while trade-size clustering—based
on the concentration of trades around round numbers—has been proposed as a wash-trading in-
dicator, its effect appears muted in NFT markets (I10). Moreover, NFT trade-size distributions
diverge significantly from the classical power-law behavior observed in other asset markets (I11).
While these techniques provide useful benchmarks for flagging potential manipulation, their direct
applicability to NFTs is limited.
Taken together, our contributions (I1–I11) establish a scalable framework for detecting and
measuring wash trading at the individual trade level using public data. This framework not only
benchmarks existing indirect methods but also introduces enhanced techniques—through optimized
regression and machine learning—that bridge the gap between direct and indirect approaches,
advancing our understanding of market manipulation in digital asset markets.
1We are thankful to the authors for facilitating access to the dataset.
6


### Page 7

2
Literature Review
Illicit market behaviors like wash trading on cryptocurrency exchanges and NFT marketplaces
have drawn considerable academic attention. Early studies in traditional finance Mao et al. (2015),
Cao et al. (2014), Zitzewitz (2012), O’Hara et al. (2014) laid the foundation for detecting mar-
ket manipulation, from identifying fraudulent transactions to analyzing odd-lot trades in equities.
These works provide key insights into market scheming and detection methods, shaping the broader
understanding of financial misconduct.
Among the most relevant studies to our work are Cong, Li, Tang and Yang (2023) and Aloosh
and Li (2024), which examine wash trading in cryptocurrency markets.
Cong, Li, Tang and Yang (2023) introduce indirect statistical tests to detect fake transactions
on cryptocurrency exchanges, estimating that over 70% of traded value in unregulated markets
stems from wash trading. Their approach provides valuable insights into the scale of manipulation
but relies on statistical inference rather than direct observation and is not designed for trade-level
detection.
Complementing this, Aloosh and Li (2024) analyze Bitcoin wash trading using hacked Mt. Gox
transaction logs, offering a rare opportunity for direct estimation on a centralized exchange based
on leaked trader identities.
They define wash trades as self-to-self transactions2 to establish a
lower bound and evaluate several other direct and indirect estimation methods, including those
from Cong, Li, Tang and Yang (2023), but find limited applicability in their dataset. For example,
their direct filters, before augmentation with insider reports, estimate around 1.4% of wash trading
activity on Bitcoin, compared to an average of 70% in Cong, Li, Tang and Yang (2023).
Our study builds on these seminal contributions while addressing some inherent limitations.
2Their self-to-self trades align with our filter f1. But the rest of our filters are specific to the on-chain nature of
our data. For fungible tokens, filters f2 and f3 are likely to generate false positives. For example, for filter f2, a
legitimate user is unlikely to sell a NFT to a buyer, then immediately buy the exact same NFT back from the same
buyer, but a legitimate market maker might sell BTC, then buy BTC back moments later. Our filter f3, has similar
issues when applied to fungible tokens. Finally, Filter f4 cannot be applied to their dataset because it only includes
Mt. Gox trading data, which does not have information on how to link wallets to their original funding source the
way we can using on-chain data.
7


### Page 8

The methods in Cong, Li, Tang and Yang (2023) are designed for aggregate-level estimation,
whereas we focus on trade-level predictions. Similarly, Aloosh and Li (2024) rely on leaked data
and insider reports, providing a static snapshot of a single exchange.
In contrast, we leverage
public NFT data and apply a broader set of direct filters, allowing for a scalable and adaptable
approach across multiple marketplaces and collections.
This direct estimation framework then
enables us to introduce both an optimized log-log regression method and a machine-learning-based
estimator, reducing estimation errors between direct and indirect methods by more than an order
of magnitude.
In addition to these key differences, our work also diverges from Cong, Li, Tang and Yang
(2023) and Aloosh and Li (2024) in several other dimensions, summarized in Table 1.
Our Paper
Aloosh & Li (2024)
Cong et al. (2023)
Dataset
Assets
NFTs
Bitcoin
Crypto
Multiple tokens/currencies?
✓
×
✓
Multiple exchanges?
✓
×
✓
Public On-Chain Data?
✓
×
×
Transaction-level estimators?
✓
✓
×
All methods apply without leaked info?
✓
×
✓
Efficacy of Distributional Filters
Benford (Section 7.1)
×
✓
✓
Trade Size Clustering (Section 7.2)
✓
×
✓
Power Tail (Section 7.3)
×
×
✓
Avg. Wash Value % - Direct
Our ∪fi filters (Section 4)
60.08%
×
×
Aloosh & Li filters
×
34.39%
×
Avg. Wash Value Estimation % - Indirect
1-Regression (Section 5.1)
46.98%
3.30%
70.85%
τ-Regression (Section 5.2)
52.75%
×
×
Machine/Deep Learning (Section 6)
60.19%
×
×
Avg. Wash Value Estimation % Error
1-Regression (Section 5.1)
13.10%
31.09%
×
τ-Regression (Section 5.2)
7.33%
×
×
Machine/Deep Learning (Section 6)
0.11%
×
×
Table 1: Comparison to seminal papers. A more detailed comparison Table with per-filter break-
downs is provided in Appendix A.
Beyond these foundational papers, several other studies explore wash trading and market ma-
8


### Page 9

nipulation from different angles.
Bonifazi et al. (2023) analyze the profitability of NFT wash trading, while Morgia et al. (2023)
examine how traders exploit token reward systems on NFT platforms. von Wachter et al. (2022)
apply a graph-theoretic approach to quantify cyclic and non-cyclic wash trades in decentralized
Ethereum NFT markets. Amiram et al. (2025) show that on centralized cryptocurrency exchanges,
increased competition can exacerbate information manipulation through inflated trading volumes.
Motivated by their findings, we conduct a preliminary exploration of whether greater competition,
measured by the entry of newly minted NFTs, is associated with higher levels of wash trading.
As reported in Appendix C, we find mixed evidence: a positive correlation on two exchanges, but
no statistically significant relationship on the third. Given competition is multifaceted and can be
measured in many ways, these results are only suggestive and point to a fruitful direction for future
research.
Other studies focus on specific market segments. Chen et al. (2024) analyze wash trading within
OpenSea’s popular NFT collections but on a more limited dataset than our multi-platform study.
Oh (2024) explore the economic motivations behind wash and insider trading in Ethereum NFTs but
do not benchmark detection methods. Cong, Landsman, Maydew and Rabetti (2023) examine tax-
loss harvesting in cryptocurrencies, highlighting investor-driven incentives distinct from exchange-
driven manipulation. These studies use different methodologies, and their wash-trading estimates
often diverge significantly from those in Cong, Li, Tang and Yang (2023), whereas ours remain
consistent.
Broader NFT market research also provides relevant context. Huang and Goetzmann (2023)
examine how behavioral biases, such as selection neglect, influence NFT markets during speculative
bubbles, while Fridgen et al. (2025) analyze herding behavior in “blue-chip” NFTs, shedding light
on price formation and liquidity patterns.
While these studies offer valuable insights, none systematically compare direct and indirect
detection methods across different markets. Our work fills this gap by evaluating the strengths
9


### Page 10

and limitations of each approach, enabling more precise wash-trading detection and laying the
foundation for new methodologies tailored to diverse market structures.3
3
Data
Our study focuses on the NFT marketplaces OpenSea, LooksRare and Blur, selected due to their
significant and different roles in the NFT market.
As of May 2024, OpenSea held the number one position by all-time volume with $36.9 billion,
followed by Blur with $10.54 billion, and LooksRare in third place with $4.86 billion.4 This selection
is particularly relevant for analyzing different aspects of NFT wash trading: LooksRare is known
for its problematic token reward system, which has been criticized for paving the way to severe
wash trading, whereas a reward system is absent in OpenSea (Morgia et al. 2023). Blur’s program,
more focused on user loyalty and platform engagement, offers a contrasting perspective (Barter
2023).
We obtained transaction data of LooksRare, Blur, and OpenSea through the Alchemy getN-
FTSales API. For LooksRare, our data covers all transactions from 11:04, December 29th, 2021 to
07:56, April 13th, 2023. For Blur, our data covers all transactions from 04:49, October 19th, 2022
to 17:14, March 7th, 2024. For OpenSea, our data covers all transactions from 19:57, February
18th, 2022 to 13:46, March 20th, 2024. In these datasets, each transaction is represented by a single
row, with the schema detailed as follows:
• Transaction hash: A unique identifier for the transaction on the blockchain.
• Block number: The specific block on the blockchain where the transaction is recorded.
• NFT seller: The address of the individual or entity selling the NFT.
• NFT buyer: The address of the individual or entity purchasing the NFT.
3Beyond academic research, practitioners also see value in using direct filters to estimate wash trading, e.g., this
blog post by Dune (2022). This said, we are not aware of any practitioner publication that systematically analyzes
the relationship between filter-based estimation and indirect statistical methods, as we do.
4https://dappradar.com/rankings/nft/marketplaces?range=all
10


### Page 11

• NFT collection: The specific collection to which the NFT belongs.
• NFT tokenId: A unique identifier for the specific NFT within its collection.
• Price: The sale price of the NFT, denominated in ETH.
• Date: The date and time when the transaction occurred.
The datasets from LooksRare, Blur, and OpenSea exchanges are substantial. The Blur exchange
dataset occupies 1.4 GB and comprises 3503420 transactions, the LooksRare dataset is 194.2 MB
with 401636 transactions, and the OpenSea dataset is 10.6 GB with 21514100 transactions. For
data cleaning, the direct outputs from Alchemy for Blur and LooksRare are ready as is. However,
for OpenSea, we combined transactions from both the Seaport and Wyvern protocols and excluded
the 0.39% of transactions not conducted in ETH-type currencies (e.g., ETH, wETH) to ensure
consistency in our analysis.
To identify potential collusions between NFT traders (buyer and seller), we collected one degree
upstream transfers of all NFT traders per platform using Alchemy’s getAssetTransfers API. For
each marketplace, we specified the to address as this marketplace’s unique trader, set fromBlock
to be well before the marketplace’s contract deployment date, and toBlock to be well after the last
transaction in the marketplace’s sales data. To err on the conservative side, we limited the transfers
to be of “external” type, i.e., Ether transfers from Externally Owned Accounts (EOAs).5
The resulting upstream dataset per marketplace includes schemas that contain “to” (unique
buyers and sellers from the marketplace sales dataset) and all the “from” EOAs who sent Ether, and
Ether only, to these traders. The upstream data sizes are 1.6 GB for Blur, 2.3 GB for LooksRare,
and 14 GB for OpenSea, with a total of 6,961,436 Ether transfers for Blur, 10,100,725 Ether
transfers for LooksRare, and 56,845,125 Ether transfers for OpenSea.
In total, we identified 9474 NFT collections on LooksRare, 7495 NFT collections on Blur, and
42442 NFT collections on OpenSea. Figure 1a shows a histogram of total sale value per collection
on LooksRare, Figure 1b shows a histogram of total sales value per collection on Blur, and Figure 1c
5https://docs.alchemy.com/reference/transfers-api-quickstart#types-of-transfers
11


### Page 12

shows a histogram of total sales value per collection on OpenSea. The figures exclude any outlier
collections that amassed total sale value above the 99th percentile - 741.78 ETH on LooksRare,
3319.01 ETH on Blur, and 1759.13 ETH on OpenSea respectively. Each bin of histograms represents
an even 1/100 intervals from 0 to 99th percentile of total sale value.
Data Visualization and Summary Statistics
0
100
200
300
400
500
600
700
Total sales (ETH)
100
101
102
103
104
105
(a) LooksRare
0
500
1000
1500
2000
2500
3000
Total sales (ETH)
100
101
102
103
104
105
(b) Blur
0
250
500
750
1000 1250 1500 1750
Total sales (ETH)
100
101
102
103
104
105
(c) OpenSea
Figure 1: Distribution of total value traded.
Figure 1 illustrates the distribution of trade volumes per NFT collection on each platform. We
exclude the top 1% of collections to prevent scale distortion from exceptionally high transaction
prices, thus offering a clearer comparison across the broader range of collections.
The histograms for all three platforms display a distribution that is heavily skewed to the left,
indicating that a majority of NFT collections fall into the lower sales value category. This suggests
that while there are a large number of NFT collections available on both platforms, the bulk of
these collections are what might be termed “small fish,” with only a few reaching higher sales
value. LooksRare and Blur show sparser distributions towards the right, while OpenSea appears
“smoother” due to its significantly higher trade count of 21514100 compared to 3503420 for Blur
and 401636 for LooksRare. This concentration in the lower end of the sales spectrum illustrates
the long-tail nature of NFT collections in these marketplaces.
A technical note: transactions on LooksRare involve trading NFT for Ether. OpenSea includes
12


### Page 13

sales done in Ether, Wrapped Ether, and other ERC20 tokens. Blur involves a mixture of Ether,
Wrapped Ether (wETH), as well as their own Blur Pool token.6 Like wrapped Ether, Blur pool
tokens can be minted by depositing ETH, and redeemed for ETH in the pool. Since all three tokens
(ETH, wETH, and Blur Pool Tokens) trade at the same valuation, we can treat all payments as
being in Ether. Our LooksRare data set has 401636 transactions that amounts to a total value of
10026162.88 ETH. As for the Blur data set, it has 3503420 transactions that amounts to a total
value of 3507602.25 ETH. Our OpenSea dataset, after filtering to include only sales done in Ether,
wETH, and Blur Pool Tokens, resulted in 21514100 transactions (99.61% of the raw OpenSea sales
data) amounting to 5910280.56 ETH.
Data Availability.
A replication package, including the data and code used in this study, are
available at Falk et al. (2025).
4
Direct Estimation
In developing our direct estimator for wash trading, we introduce four filters specifically tailored
to accommodate observables from on-chain NFT data. We discuss each filter in detail next.
4.1
Wash Trading Filters
Figure 2 provides a visual representation of the four filters.
6Blur implements its own token to reduce gas costs when interacting with the Blur exchange contract.
13


### Page 14

Filter f1: Self trades
Filter f2: Back-and-forth trades
Filter f3: 3 times around
ETH
ETH
NFT
Filter f4: Common funder
Figure 2: The four direct wash-trading filters.
Filter f1 flags trades where the buyer and seller account is one and the same – this is the most
na¨ıve form of wash-trading – literally selling the NFT to oneself.
Filter f2 detects back and forth trades, meaning, if buyer and seller are inverted for the same
exact NFT, then f2 will be triggered. This is intended to flag slightly more sophisticated wash
trading activity, where the wash trader has created two accounts and sells the same NFT back and
forth between these two accounts. It gets triggered even when there is just one instance of inversion
between buyer and seller identities for the exact same NFT. This means if an NFT is sold from
Address A to Address B, and then subsequently sold back from Address B to Address A, f2 would
identify this as a potential wash trade.
Filter f3 flags trades where the same buyer purchased the same NFT, three or more times.
Imagine a slightly more sophisticated wash trader, who generates multiple (more than two) ac-
counts, and trades a single NFT between these accounts in a cycle. Unlike f2, which flags direct
back-and-forth trades between two accounts, f3 identifies circular trading patterns involving three
or more accounts. Filter f3 will flag this activity as wash trading, if the NFT passes around the
cycle at least three times. For example, if an NFT is first sold to Buyer A, who then sells it to
Buyer B, and Buyer B subsequently sells it to Buyer C, who then completes the loop by selling it
back to Buyer A, f3 would flag the activity when Buyer A acquires the NFT for the third time.
14


### Page 15

This cycle could involve numerous parties and is designed to detect more complex wash trading
schemes where a single entity might be operating multiple accounts to simulate a closed loop of
trades.
Finally, Filter f4 detects transactions with a common upstream wallet that has funded both
the buyer and seller, indicating potential control over both sides of the trade. In our dataset, we
analyze the transfer history up to one degree upstream for both buyers and sellers. This means,
for example, if Wallet A sells an NFT to Wallet B, the Filter checks if there is a Wallet C that
previously transferred funds (Ether only) to both Wallet A and Wallet B. The presence of such a
common upstream wallet suggests a single entity may be orchestrating the trade from behind the
scenes, using different wallets to create the illusion of a genuine transaction.
4.2
Mitigating False Positives
We believe our Filters 1-3 are extremely conservative, and unlikely to classify organic behavior as
wash trading. By focusing only on NFT sales, rather than NFT transfers, we immediately exclude
all activity where a single user simply transfers an NFT between different wallets, e.g. to increase
anonymity, or reduce risk. Second, Filters 1-3, only catch behavior where a user engages with the
NFT marketplace (and pays trading fees to the marketplace on top of the Ethereum gas costs),
and the same NFT ends up in exactly the same wallet.
When implementing these filters, we have to make a decision about granularity. For example,
in f2, when we say “the same” NFT was traded back and forth between, does “the same” NFT
mean the same NFT contract (e.g. Bored Apes) or the same exact NFT (e.g. Bored Ape #3401).
We can ask a similar question for f3 as well. For f2, we consider a typical wash trader would buy
and sell from the same NFT collections (e.g. Bored Apes) back and forth, but not necessarily the
same token. Thus, we set f2 at the collection level. For f3, since it is reasonable for a legitimate
trader to buy multiple tokens from the same collection, we apply f3 at the individual token level,
(e.g. Bored Ape #3401), rather than at the collection level. This ensures that frequent purchases
15


### Page 16

within a collection are not automatically classified as wash trading, while repeated trades of the
same token remain a strong indicator of wash activity.
To mitigate potential false positives in f4, which identifies common upstream wallets, we exclude
all smart contract addresses and EOAs of centralized exchanges (CEXs). Legitimate traders often
interact with the same smart contracts. For instance, if both buyer and seller minted Wrapped
Ether (wETH), they would have received a “payment” from the wETH smart contract. Similarly,
if both parties sold NFTs on OpenSea before transacting on LooksRare, they could mistakenly be
flagged due to payments from OpenSea’s contract.
Furthermore, since some CEXs also use EOAs, such as Binance deposit addresses, we also
exclude transactions where the upstream EOA is tagged as belonging to a CEX. While this method
yields a conservative estimate by excluding other type of transfers, e.g., ERC20 tokens transfers, it
reflects common wash trading practices where Ether is typically used to cover gas and transaction
costs. Applying these measures, we ensure that only direct, user-controlled funding sources are
considered.
4.3
Direct Estimation Results
Table 2 shows our direct estimation results after applying each filter individually, and then com-
bining them (∪fi).
Wash trades, as a percentage of total trades, appear quite stable across exchanges – we estimate
between 30-40% across. On the other hand, there is significant heterogeneity (26% - 95%) in terms
of wash trade values (often referred to as traded volume in the literature), that is, when taking into
account not just the number of trades categorized as wash, but also their size and price.
On LooksRare, Filter 1 only flagged 57 trades, whereas Filter 4 flagged 147006 trades as wash
trades. In total, filters 1 through 4 collectively identified 163320 wash trades, which is not simply
the sum of the individual filters’ results. This is because a single transaction may meet the criteria
of multiple filters, and the last line in the table represents any transaction flagged by at least one
16


### Page 17

Wash Trades
Wash Value
Filter
Marketplace
(% of transactions)
(% of value traded)
Count
f1
LooksRare
0.01%
0.05%
57
Blur
0.15%
0.36%
5239
OpenSea
0.01%
0.0%
2379
f2
LooksRare
7.51%
92.6%
30171
Blur
7.2%
27.2%
252204
OpenSea
0.56%
0.71%
120910
f3
LooksRare
8.91%
88.46%
35770
Blur
5.17%
23.56%
181240
OpenSea
6.89%
5.1%
1483348
f4
LooksRare
36.6%
80.19%
147006
Blur
35.52%
38.47%
1244360
OpenSea
25.91%
22.43%
5574336
∪fi
LooksRare
40.66%
95.68%
163320
Blur
40.86%
58.16%
1431537
OpenSea
31.22%
26.39%
6717283
Average
37.58%
60.08%
2770713
Table 2: Direct estimation of wash trades by filter and marketplace.
of these filters (logical OR). Overall, we found 40.66% of wash trades on LooksRare corresponding
to an astouding 95.68% of the trade value in ETH (in other words, trades identified as wash, were
larger in size on average ).
On Blur, Filter 1 flagged the least, 5239 trades, while Filter 4 flagged the most, 1244360 trades.
Here, the combination of filters 1 through 4 caught 1431537 trades, with 40.86% of transactions
accounting for 58.16% of the value.
Finally, on OpenSea, Filter 1 identified 2379 trades as wash trades, while Filter 4 flagged 5574336
trades. Collectively, filters 1 through 4 flagged 6717283 trades, where 31.22% of the flagged wash
trades contributed 26.39% of the total value.
The discrepancy in wash trade value between LooksRare (95.68%), Blur (58.16%), and OpenSea
(26.39%), despite their similar fraction of wash trades (40.66%, 40.86%, and 31.22%, respectively),
can be partly attributed to findings from Morgia et al. (2023). Their study suggests that LooksRare,
while processing fewer transactions, focuses on higher-value NFTs, which likely contributes to the
17


### Page 18

observed difference in wash trade value
4.4
Impact of Wash Trading on NFT Prices and Trader Profits
We can leverage our direct estimator to investigate two additional questions that may be of in-
terest: does wash trading influence NFT prices and trader profits? Although our analysis reveals
correlations, we do not assert causation. Given that our primary focus is on comparing direct and
indirect estimation methods, these findings are presented as ancillary observations to inform future
research.
Wash trading correlates with higher NFT prices
To examine the impact of wash trading on NFT prices, we categorized NFT collections into two
groups: those involved in wash trading and those that were not. We then calculated the median
transaction price for each collection, excluding the top 1% of sales to reduce the influence of outliers.
Figure 3 presents the resulting histograms on a logarithmic scale, where purple bars represent wash-
traded collections, yellow bars indicate legitimate trading, and overlapping areas appear as a darker
yellow.
Our analysis reveals significant differences across exchanges. The median transaction price is
19.13 ETH on LooksRare, 7.37 ETH on Blur, and 2.74 ETH on OpenSea, with the highest-priced
collections reaching 11307.24 ETH, 187.0 ETH, and 2000.0 ETH, respectively.
Wash-traded collections exhibit higher median sale prices on Blur and OpenSea, but the opposite
is observed on LooksRare. Specifically, the median sale prices for wash-traded collections are 0.0333
ETH on LooksRare, 0.0189 ETH on Blur, and 0.0192 ETH on OpenSea, compared to 0.0395 ETH,
0.0131 ETH, and 0.018 ETH for collections without wash trading. These findings suggest that
while wash trading may artificially inflate the perceived value for some NFT collections, it is not
universal.
18


### Page 19

0.0
2.5
5.0
7.5
10.0 12.5 15.0 17.5 20.0
Median Price (ETH)
100
101
102
103
104
105
Wash Trading
Legitimate Trading
(a) LooksRare
0
1
2
3
4
5
6
7
Median Price (ETH)
100
101
102
103
104
105
Wash Trading
Legitimate Trading
(b) Blur
0.0
0.5
1.0
1.5
2.0
2.5
Median Price (ETH)
100
101
102
103
104
105
Wash Trading
Legitimate Trading
(c) OpenSea
Figure 3: Distribution of median transaction prices.
Wash trading does not correlate with increased wash trader profits
Given wash trading seems to lead to increased median prices, it naturally follows to ask whether
this activity actually increases short-term wash trader profits. To help answer this question, we
grouped wash trading accounts based on their connectivity through trades. In particular, as wash
trading usually involves more than one wallet, we group buyer and seller as one entity if their
transaction is flagged as a wash trade. To illustrate, consider the following toy example involving 3
traders and 2 transactions. Suppose there are traders A, B, and C, in which the transaction from
A to B is flagged as wash trade and the one from B to C is not.
A
B
A, B
∼=
C
C
Wash trade
Legitimate trade
Legitimate trade
In this case, trader A and B are both considered to be wash traders and thus we classify them as a
single wash-trading group that either makes a profit or takes a loss through their transaction with
legitimate trader C. To calculate the profit, we gather the revenue and expense of each trader and
wash group.
Filtering through every transaction, we obtained a complete list of disjoint wash trading groups.
We collapsed 64465 wash traders on LooksRare into 6643 disjoint wash trading groups. As for Blur,
19


### Page 20

115174 wash traders were categorized into 2007 wash groups. Similarly, on OpenSea, 942034 wash
traders were grouped into 13194 disjoint wash trading groups. Excluding the traders who took a
loss and those with profits over the 99th percentile to avoid extreme values, Figure 4 compares the
wash trading group to legitimate trader profits:
0
10
20
30
40
Profit (ETH)
100
101
102
103
104
105
106
Wash Trading
Legitimate Trading
(a) LooksRare
0
5
10
15
20
25
30
35
Profit (ETH)
100
101
102
103
104
105
106
Wash Trading
Legitimate Trading
(b) Blur
0
5
10
15
20
Profit (ETH)
100
101
102
103
104
105
106
Wash Trading
Legitimate Trading
(c) OpenSea
Figure 4: Distributin of trader profits.
These histograms visualize the profits earned by traders involved in wash trading versus those
engaging in legitimate trading across both platforms. In each histogram, the x-axis represents the
profit range in ETH, while the y-axis shows the number of traders or wash trading groups on a
logarithmic scale, enabling a clear comparison of the frequency of profit amounts.
The histograms reveal that, across various profit brackets, wash traders do not consistently
secure higher profits when compared to their legitimate counterparts.
This visual evidence is
corroborated by the following numbers:
On LooksRare, the median profit for wash trading groups is approximately zero ETH, with a
maximum profit reaching 69398.18 ETH. In contrast, legitimate traders attain a higher median
profit of 0.01672 ETH and achieve up to 9861.77 ETH at the higher end.
On Blur, wash trading groups achieve a median profit close to zero ETH, with their most
profitable outcomes peaking at 107.55 ETH. This is lower than the median profit for legitimate
traders, which stands at 0.014515 ETH, and legitimate traders also reach much more substantial
maximum profits of 5647.13 ETH.
20


### Page 21

On OpenSea, both wash trading groups and legitimate traders achieve a median profit close
to zero ETH. However, legitimate traders can achieve significantly higher maximum profits, reach-
ing up to 124374.95 ETH, compared to wash trading groups with a maximum profit of 2891.45
ETH. These findings suggest that while wash trading may influence market dynamics, it does not
necessarily result in greater profitability for those who engage in it.
Summary of Direct Estimation Results
(I1) Wash trading is identified as a percentage of total trades 40.66% on LooksRare, 40.86% on
Blur, and 31.22% on OpenSea; yet these trades contribute disproportionately to the total
value, accounting for 95.68%, 58.16%, and 26.39% of the value in ETH, respectively.
(I2) NFT collections implicated in wash trading typically show higher median transaction prices
when compared to legitimate trading collections, with a more noticeable discrepancy observed
on Blur. This indicates a potential influence of wash trading on inflating NFT collection
values.
(I3) Wash trading activities do not guarantee higher profits. Data reveals that wash traders do
not consistently outperform legitimate traders in terms of profit margins.
5
Indirect Estimation #1: Exchange-level Regressions
Among the indirect statistical methods analyzed in Cong, Li, Tang and Yang (2023), Trade-Size
Roundedness stands out for its ability to quantify aggregate wash trading percentages by combining
roundness metrics with a regression-based approach.
Leveraging our direct estimation methods from Section 4, we make two meaningful extensions
to their method: In Section 5.1, we slightly modify their regression to apply it to the NFT setting
where the benchmark for ground truth is given by the direct filters. As both approaches use a
1% roundedness threshold (discussed below), we refer to them as “1-Regression” going forward. In
21


### Page 22

section 5.2, we further extend this method via hyper-parameter optimization, and show how this
can reduce estimation errors between direct and indirect methods. We refer to this approach as
“τ-Regression” where the threshold τ is the outcome of an optimization.
5.1
1-Regression
Cong, Li, Tang and Yang (2023) categorize a trade price as “round” if its last nonzero digit exceeds
1% of the total price.7 The authors use this to quantify the amount of unrounded trades that are
typical on a hypothetical exchange with exactly zero wash trades. As a proxy, they assume that
highly regulated exchanges likely have very low wash trading activity, and could thus serve in lieu of
this ideal benchmark. The amount of unrounded volume obtained from these regulated exchanges
is referred to as the Benchmark Unrounded Volume (BUV). Deviations from the BUV indicate
wash trading activity, and this is captured via the regression Equation 1. One important difference
in our setting is that since our dataset allows for direct trade-level estimation, we can leverage our
results from Section 4 to provide a bespoke BUV for each platform, improving regression accuracy.
In particular, for each complete week of data in our dataset, indexed by t, we aggregate the
weekly rounded and unrounded traded volumes of legitimate non-wash trades (those not tagged by
∪fi), denoted by V legit
Roundedt and V legit
Unroundedt. We then perform a log-log linear regression for each
exchange:
ln

V legit
Unroundedt

= c + β · ln

V legit
Roundedt

+ ϵt
(1)
where c is the constant term, β is the regression coefficient, and ϵt is the error term.
Once we obtain the estimated parameters ˆc and ˆβ, they are used to predict the aforementioned
BUV, which is the total predicted legitimate unrounded trade volume ˆV legit
Unrounded, using the legiti-
mate rounded non-wash trade volume V legit
Rounded as input. The deviation of the predicted unrounded
7For instance, 2.1 is “round” because .1 is more than 1% of 2.1. On the other hand, 1.135 is not round because
the last nonzero digit, .005, is less than 1% of 1.135.
22


### Page 23

volume from the actual unrounded volume (which includes both legit and wash trades) captures
wash trading activity:
WashVolume = max
n
VUnrounded −ˆV legit
Unrounded, 0
o
,
(2)
with
ˆV legit
Unrounded = exp

ˆc + ˆβ · ln

V legit
Rounded

,
(3)
where WashVolume represents the non-negative excess of total unrounded trade volume over the
predicted legitimate unrounded volume, capturing potential wash trading activity. Then, the esti-
mated wash % can be computed by dividing by total volume traded.
1-Regression Results
Table 3 compares the estimated percentage of wash trading value obtained using the 1-Regression
method with the results from the direct estimation method from Section 4. The error column
represents the absolute difference between the 1-Regression estimates and the direct wash value
estimates.
1-Regression
1-Regression
1-Regression
Direct ∪fi
Abs.
Platform
R2
p-value
Wash Value %
Wash Value %
Error
Blur
0.905
2.5e-31
12.64%
58.16%
45.52%
LooksRare
0.804
5.9e-24
76.39%
95.68%
19.29%
OpenSea
0.909
4.9e-35
51.92%
26.39%
25.53%
Averages
46.98%
60.08%
30.11%
Table 3: Comparison of 1-Regression and direct wash value estimates across platforms. Avg. 1-
regression aggregate error: 60.08% −46.98% = 13.10%. Avg. 1-regression absolute error: 30.11%.
As the table suggests, the errors between the two methods, direct and indirect, can be significant.
The 1-regression underestimates wash trading on Blur (-45.2%). Less so on LooksRare (-19.3%).
On the other hand, it overestimates wash trading on OpenSea (by 25.5%). Next, we explore whether
23


### Page 24

these errors can be reduced by leveraging on-chain trade-level data.
5.2
τ-Regression
The 1% roundedness threshold chosen in Cong, Li, Tang and Yang (2023) is not the result of
an optimization process, and it’s possible, even likely, that a different threshold may be optimal.
Fortunately, the availability of on-chain data and our direct estimation results allow us to vary the
1% roundedness threshold used in Cong, Li, Tang and Yang (2023) and evaluate its impact on the
errors between the two methods.
We denote the roundedness threshold τ and to optimize it, we conduct a line-search through 100
evenly spaced values from 0.01%(0.0001) to 10%(0.1), applying the regression method to each one.
Figure 5 illustrates the impact of varying thresholds on errors. Each point on the figure represents
an independent log-log regression. Thus, we run hundreds of such regressions to populate these
figures.
0.00
0.02
0.04
0.06
0.08
0.10
Threshold
0
10
20
30
40
50
Blur Error
LooksRare Error
OpenSea Error
Figure 5: Estimation Error Abs(Direct −Indirect wash %), versus thresholds τ.
Table 4 summarizes the results.
24


### Page 25

Optimal
τ-Regression
Direct ∪fi
τ-Regression
1-Regresion
Platform
Threshold (τ)
Wash Value %
Wash Value %
Abs. Error
Abs. Error
Blur
9.09%
27.17%
58.16%
30.99%
45.52%
LooksRare
8.18%
94.65%
95.68%
1.03%
19.29%
OpenSea
0.21%
36.42%
26.39%
10.03%
25.53%
Averages
5.83%
52.75%
60.08%
14.02%
30.11%
Table 4: Comparison of 1-Regression and direct wash value estimates across platforms. Avg. τ-
regression aggregate error: 60.08% −52.75% = 7.33%. Avg. τ-regression absolute error: 14.02%.
The optimal threshold is defined as the one yielding the smallest absolute difference, i.e., min-
imum error, between regression-based and direct wash value percentage estimates. Notably, this
optimal threshold does not align with the fixed 1% threshold across platforms. The optimal thresh-
olds are 9.09% for Blur, 8.18% for LooksRare, and 0.21% for OpenSea. These optimal thresholds
lead to a significant reduction in error between predicted and direct wash value estimates, in
some cases by an order of magnitude. For instance, LooksRare’s error drops from 19.29% to just
1.03%. These observations validate the potential usefulness of the Cong, Li, Tang and Yang (2023)
log-log regression approach for some exchanges, while emphasizing the need for platform-specific
fine-tuning.
Summary of Indirect Estimation Method #1 - Regressions
(I4) The standard 1% threshold regression “1-regression” from Cong, Li, Tang and Yang (2023)
shows promise when applied to NFT data, but unoptimized, it can lead to significant estima-
tion errors compared to the direct estimation method.
(I5) The optimized τ-regression meaningfully reduces these errors (down to 1.03% for LooksRare!)
but a significant gap still remains for the Blur marketplace.
25


### Page 26

6
Indirect Estimation #2: Machine Learning
While the τ-Regression approach from Section 5.2 shows promise in narrowing the gap between
direct and indirect estimation methods, notable discrepancies remain—particularly on the Blur
platform, where a 7.33% residual aggregate error (and 30.11% absolute average error) persists even
after fine-tuning the threshold. To address these issues, we propose herein a comprehensive artificial
intelligence / machine learning framework. We optimize three models: two tree-based algorithms
(random forests and XGBoost (Chen and Guestrin 2016)) and a deep learning neural network based
on the TabNet architecture (Arik and Pfister 2021).
As the first two models are more commonly discussed in the literature, we focus our attention
on the latter here.8 The attention mechanism in TabNet is conceptually similar to the multi-head
self-attention used in large language models; while LLMs capture inter-token dependencies, here the
mechanism dynamically weights features on an instance-by-instance basis. This capability allows
the model to focus on specific combinations of trade volume, timing, and account activity that are
indicative of wash trading, even if individual features may not appear anomalous.
Designed with tabular data in mind, the network employs a sequential process in which each
decision step selectively attends to a subset of features. An attentive transformer first generates a
sparse mask that highlights the most relevant inputs; these selected features are then processed by
a feature transformer module—comprising fully connected layers with non-linear activations—to
capture complex interactions and conditional dependencies among trading metrics. This approach
preserves some degree of interpretability by revealing which features most influenced each predic-
tion.
The primary parameters of this network are nsteps (the number of sequential decision steps),
na (the dimension of the attention layer, influencing feature interaction complexity), and nd (the
dimension of the decision layer, shaping the output features at each step). Given the size of our
8Complete hyperparameter and training settings are available in the github accompaniment to the paper, available
in Falk et al. (2025). A summary is provided in Appendix B.
26


### Page 27

dataset and feature list (see Section 6.1), we aim for a moderate number of parameters to balance
expressiveness and avoid overfitting. We explored na and nd within the range [8, 32], and nsteps
in [3, 7], but ultimately fixed nsteps = 1 and na = nd ∈{128, 256} based on early performance.
This approach results in a model with tens of thousands, or at most, low hundreds of thousands
of weights. The relaxation parameter (γ) and sparsity regularization (λsparse) are also tuned. The
hyperparameter search employs a combination of grid and random search.
Although fine-tuning is essential, a pivotal aspect is the initial feature engineering. To this end,
given the promising results from Section 5, we start by adapting the τ-regression method to operate
at the individual trade level.9 This adapted τ-regression is combined with 15 additional features
that capture key characteristics of wash trading behavior.
6.1
Input Features
Each sales record in our dataset includes detailed information such as buyer and seller identities,
trade value, the NFT collection and token Id, and the timestamp of the transaction. These rich
attributes enabled the construction of the following features for each trade:
• Price: Value of the trade in its native token (e.g., 0.8 ETH); price.
• Round Level: Round level of the trade value;
round level.
• Collection Cumulative Wash Percentage (τ-regression): Fraction of estimated wash
value relative to the total trading value of the NFT collection, computed up to the given
trade timestamp, estimated using Cong, Li, Tang and Yang (2023)-style log-log regression
with optimal threshold from Section 5;
cumu wash percent opt.
• Trader Trade Count: Total number of trades by the trader (buyer or seller) in the preceding
9To achieve this, we estimate the τ-regression parameters using the entire dataset, then for each trade, compute
its NFT collection’s cumulative rounded and unrounded value up to that point in time, and apply Equation 3 from
Section 5 to derive the cumulative wash value percentage.
27


### Page 28

24 hours and preceding 7 days10;
buyer 24h trade count, buyer 7d trade count, seller 24h trade count,
seller 7d trade count.
• Trader NFT Trade Count: Total number of trades by the trader involving the specific
NFT collection in the preceding 24 hours and preceding 7 days11;
buyer 24h nfttrade count, buyer 7d nfttrade count, seller 24h nfttrade count,
seller 7d nfttrade count.
• NFT Trade Count: Total number of times the NFT collection was traded (by any trader)
up to this point in time; buyer nft all trade count, seller nft all trade count.
• Price Deviation: Difference between the current trade price and the last recorded trade
price for this specific NFT token; price deviation.
• Time Since Last Trade: Elapsed time since the last trade of this specific NFT token;
time since last trade.
• Time of Day: Hour of the day when the trade occurred; hours.
To ensure data integrity, we excluded samples with missing feature values. After cleaning, Blur
retains 3,450,059 samples (99.66% of total), LooksRare retains 401,105 samples (100.00%), and
OpenSea retains 21,309,625 samples (99.69%). The cleaned data was then split into 4 stratified
folds to preserve the distribution of the target label across training and test sets, and subsequently
used for model training and evaluation via 4-fold cross-validation.
Note, we must deliberately exclude all direct filters from Section 4 from our feature set for
two reasons. First, and most obviously, these filters are meant to detect direct evidence of wash
trading and thus serve as ground truth labels—their inclusion in the feature set would compromise
model integrity.12 Second, we aim to design this ML-based framework in a generalizable way, for
10Each interval (24 hours and 7 days) is calculated separately for both buyers and sellers, resulting in 4 distinct
features.
11Similar to Trader Trade Count, this generates 4 distinct features due to the inclusion of both buyers and
sellers over two time intervals.
12If an alternative ground truth—such as court orders or leaked private data (e.g., Aloosh and Li (2024))—were
available, these filters could be incorporated in the feature set to further improve performance.
28


### Page 29

applicability beyond NFT markets; the feature set is thus constructed to handle both fungible
and non-fungible assets with minimal modifications. The performance of the AI-based estimation
approach on NFTs is discussed in 6.2, while its performance on fungible tokens is discussed in
Section 6.3.
Finally, our target variable in this section is the joint filter ∪fi, which aggregates all identified
wash trades at the exchange level. An alternative would be to treat each filter separately, reporting
per-filter accuracies or even conducting distinct training runs for each filter. These would provide
a more granular view of not only whether a trade is classified as a wash trade, but also the specific
“type” of wash trade. However, because some wash types are relatively rare on some exchanges, this
approach faces data limitations that make it difficult to draw statistically meaningful conclusions
and train reliable models.
A more granular breakdown would therefore likely require a larger
dataset, in which case our methodology could be applied directly by simply redefining the target
variable to represent each individual filter, rather than their union.
6.2
ML Results
We evaluate model predictive performance out-of-sample at two levels: the individual trade level
and the aggregate wash trading volume level. We use 4-fold cross-validation, and report average
metrics over the four randomized train-test splits. Trade-level performance is measured using ROC-
AUC scores, while aggregate performance assesses how well each ML algorithm predicts the “true”
percentage of total wash trading volume (from Section 4). The aggregate error is quantified as:
aggr pred error = true wash trading volume % - predicted wash trading volume %
At the trade level, ML models predict the probability of each trade being a wash trade. A
binary classification (wash or non-wash) is assigned based on a probability threshold (set at 50% by
default). To evaluate trade-level performance, we use out-of-sample ROC-AUC scores because they
are threshold-independent, allowing for an objective comparison across models without requiring a
fixed probability-to-label conversion threshold.
29


### Page 30

In contrast, evaluating aggr pred error requires selecting a conversion threshold, and this is
typically optimized against a specific objective. The choice of objective is inherently subjective
and application-dependent, with possible criteria including minimizing wash number or wash value
percentage errors, maximizing F1 or MCC scores, etc. Some contexts may require more elaborate
objectives, such as cost-benefit matrices. For our analysis, to keep things simple, we optimize for
the threshold that minimizes aggr pred error.
Table 5 summarizes the average out-of-sample
performance across folds for each ML model in terms of AUC scores and absolute aggr pred error
(denoted “Error” in the table).
XGB
RF
DL
XGB
RF
DL
Platform
ROC-AUC
ROC-AUC
ROC-AUC
Abs. Error
Abs. Error
Abs. Error
Blur
0.904
0.721
0.842
0.07%
0.24%
0.07%
LooksRare
0.844
0.747
0.789
0.01%
0.04%
0.03%
OpenSea
0.771
0.647
0.678
0.14%
1.29%
0.57%
Table 5: Out-of-sample machine learning results. Average ML error across all exchanges, models,
and folds is 0.27%.
Legend: XGB = XGBoost, RF = Random Forest, DL = Deep Learning
(TabNet).
The results in Table 5 demonstrate that all three models achieve exceptional performance in
reducing aggregate out-of-sample estimation errors. These range from just 0.01% (XGB) to 1.29%
(RF). Thus the ML approach substantially outperforms previous regression-based methods. Yet,
these regressions remain highly relevant!
As a reminder, they now form a critical part of the
input feature-set, helping achieve these remarkably low error rates, well beyond their standalone
capabilities.
For clarity, we summarize how the error rates drop significantly from 1-Regression to τ-Reg-
ression to the average rates for the three machine learning models, in Table 6.
30


### Page 31

1-Regression
τ-Regression
avg. ML
Platform
Abs. Error
Abs. Error
Abs. Error
Blur
45.6%
31.0%
0.13%
LooksRare
19.3%
1.0%
0.03%
OpenSea
25.5%
10.0%
0.67%
Table 6: Absolute Estimation Errors Across Platforms and Methods.
Regarding trade-level AUC scores, however, the results reveal greater complexity, reinforcing our
earlier observation about dispersion between NFT exchanges (as discussed in the direct estimation
section 4).
While all models demonstrate discriminative ability beyond random chance, XGB
exhibits a marked advantage, achieving average AUC scores of 0.84 across platforms and exceeding
0.9 for Blur specifically. The deep learning model comes in second, though our experiments indicate
the training can be further improved if additional compute is available, e.g., by leveraging higher-
end GPU clusters and longer sessions (we trained the model using individual mid-tier NVIDIA
L40s, A100, and RTX 4090 GPU cards, limited to overnight runs).
Factors Driving Wash Trading
While the algorithms we use are not as interpretable as other ML techniques, we can nonetheless ex-
tract importance scores to tag the features that seem to consistently rank high in terms of predictive
power. Table 7 summarizes these, ranked by average importance score across all platforms, models,
and folds. Each individual cell reports the average score across 4 folds, except the final column.
The top 4 features are time since last trade, seller 7d trade count, buyer 7d trade count,
and price.
31


### Page 32

Blur
LooksRare
OpenSea
Rank
Feature
RF
XGB
DL
RF
XGB
DL
RF
XGB
DL
Average
1
time since last trade
0.081
0.092
0.062
0.121
0.053
0.081
0.501
0.265
0.087
0.149
2
seller 7d trade count
0.093
0.206
0.067
0.018
0.046
0.052
0.039
0.226
0.060
0.090
3
buyer 7d trade count
0.252
0.096
0.103
0.146
0.031
0.071
0.007
0.033
0.059
0.089
4
price
0.032
0.081
0.066
0.129
0.214
0.062
0.020
0.076
0.061
0.082
5
buyer 7d nfttrade count
0.104
0.048
0.065
0.140
0.039
0.127
0.003
0.029
0.063
0.069
6
seller nft all trade count
0.037
0.058
0.047
0.037
0.137
0.046
0.105
0.054
0.063
0.065
7
buyer nft all trade count
0.149
0.050
0.055
0.110
0.052
0.051
0.002
0.017
0.053
0.060
8
buyer 24h trade count
0.119
0.063
0.062
0.086
0.037
0.058
0.001
0.031
0.058
0.057
9
seller 7d nfttrade count
0.026
0.037
0.071
0.039
0.050
0.072
0.083
0.057
0.066
0.056
10
price deviation
0.002
0.046
0.053
0.042
0.050
0.075
0.142
0.006
0.080
0.055
11
buyer 24h nfttrade count
0.076
0.076
0.061
0.090
0.032
0.056
0.003
0.031
0.059
0.054
12
seller 24h nfttrade count
0.006
0.043
0.065
0.018
0.057
0.064
0.044
0.040
0.060
0.044
13
seller 24h trade count
0.018
0.040
0.060
0.009
0.075
0.051
0.022
0.049
0.058
0.042
14
cumu wash percent opt
0.004
0.004
0.059
0.011
0.048
0.047
0.026
0.049
0.062
0.034
15
round level
0.001
0.050
0.051
0.005
0.065
0.046
0.003
0.029
0.056
0.034
16
hours
0.001
0.010
0.053
0.000
0.013
0.040
0.000
0.006
0.055
0.020
Table 7: Feature scores by model and exchange, sorted by average score
Across all three NFT platforms, our models reveal a unifying theme: wash trading detection
hinges on identifying abnormal deviations in trading behavior—whether these manifest as sustained,
inflated trading volumes or as sudden shifts in trade recency and price dynamics. In every case, the
predictive models highlight anomalies in key features that depart from normal market behavior.
Notably, 7-day trade activity, trade recency (as measured by time since the last trade) and price
emerge as critical indicators, albeit with differing absolute values across platforms.
Delving into the specifics, on Blur, buyer-side activity remains the dominant signal, with buyer
7-day trade count emerging as the top-ranked feature (importance scores of 0.252 for RF and 0.103
for XGBoost). This is followed closely by seller 7-day trade count and buyer NFT all trade count.
Other short-horizon buyer metrics such as buyer 24-hour trade count also score highly, while time
since last trade and trade prices contribute moderately. The broader pattern on Blur suggests that
wash trading is most strongly associated with frequent buyer engagement and short-term trade
bursts.
For LooksRare, the trade price emerges as the most important feature (0.214 for TabNet),
suggesting that pricing patterns themselves help flag manipulative activity. Still, buyer activity
remains crucial: buyer 7-day NFT trade count and buyer 7-day trade count rank among the top
32


### Page 33

features across models. Short-term buyer features (e.g., buyer 24-hour trade count and buyer NFT
all trade count) also show consistent signal. This blend of buyer behavior and pricing reinforces the
interpretation that both sustained buyer-side manipulation and anomalous price levels drive wash
trading on LooksRare.
In contrast, on OpenSea the dynamics differ markedly. The models assign the highest impor-
tance to time since the last trade (0.501 for RF and 0.087 for XGBoost) and to price deviation
(0.142 and 0.080, respectively). Buyer metrics such as the buyer 7-day trade count are nearly neg-
ligible, while seller-related features (e.g., seller NFT all trade count and seller 7-day trade count)
assume greater prominence. This pattern indicates that on OpenSea, wash trading is characterized
by rapid bursts of trading activity and aggressive price shifts—suggesting that coordinated seller
actions, along with abrupt trade recency signals, are key markers of manipulation.
6.3
Robustness of ML Estimation Beyond NFTs
To gauge robustness to crypto assets outside of NFTs, we deploy the machine learning approach
from Section 6 to the Bitcoin dataset from Aloosh and Li (2024). Each transaction is represented
by a single row with the following schema:
• Trade ID: A unique identifier for the trade on the platform.
• Buyer: The anonymized ID of the entity purchasing Bitcoin.
• Seller: The anonymized ID of the entity selling Bitcoin.
• Time: The timestamp of the transaction.
• Bitcoins: The amount of Bitcoin traded in the transaction.
• Price (USD): The price per Bitcoin in USD.
In line with their approach, we focus on a subsample of Mt. Gox trades between June 26,
2011, and May 20, 2013, capturing the platform’s active trading period. This subsample contains
5,539,244 transactions. The full dataset, including later records, totals 480MB.
We rely on the same 16 features as before with minor tweaks to tailor to Bitcoin data:
33


### Page 34

• Price: Value of the trade in its native token (e.g., 0.8 BTC).
• Round Level: Round level of the trade value.
• Market Cumulative Wash Percentage: fraction of estimated wash trades relative to total
BTC traded in the market up to that point.
• Trader Trade Count: Total number of trades by the trader (buyer or seller) in the preceding
24 hours and preceding 7 days. (4 features; time frame x buyer/seller)
• Trader BTC Trade Count: Total number of BTC traded by the trader in the preceding
24 hours and preceding 7 days. (4 features; time frame x buyer/seller)
• BTC Trade Count: Total number of BTC was traded (by any trader). (2 features)
• Price Deviation: Difference between the current trade price and the last recorded trade
price in USD per BTC.
• Time Since Last Trade: Elapsed time since the last trade.
• Time of Day: Hour of the day when the trade occurred.
As before, to preserve model integrity, we do not include the direct filters used by Aloosh and Li
(2024) in the feature list, because the authors utilized them to build their “ground truth” wash
data.
The results are presented in Table 8.
XGB
RF
DL
XGB
RF
DL
Platform
AUC
AUC
AUC
Abs. Error
Abs. Error
Abs. Error
Mt. Gox
0.972
0.859
0.939
0.10%
0.51%
0.06%
Table 8: Out-of-sample machine learning results on Mt. Gox dataset. Legend: XGB=xgboost,
RF=random forest, DL=Deep Learning.
As before, the results demonstrate very low error rates across all three models, while AUC scores
are also higher, reaching a remarkable 0.972 and 0.939 with the XGB and deep learning models,
respectively. This suggests that our ML method not only transfers beyond NFTs but performs
even more effectively in this context. A likely explanation is that we’re applying it to a single asset
34


### Page 35

(Bitcoin) rather than diverse NFT collections all traded on the same exchange. This implies two
potential improvements for future work: enhancing our NFT feature set with collection-specific
characteristics, or implementing an unsupervised clustering algorithm before supervised learning.
We leave this for future work.
Below, we print out the importance scores for the XGB method, given it has the highest AUC.
Feature
Score
1
buyer 7d trade count
0.2082
2
seller 7d trade count
0.1362
3
buyer all btc sum
0.1098
4
seller all btc sum
0.1041
5
cumu wash percent opt (τ-regression)
0.0618
6
seller 7d btc sum
0.0474
7
seller 24h trade count
0.0470
8
buyer 24h trade count
0.0458
9
buyer 7d btc sum
0.0434
10
seller 24h btc sum
0.0405
11
buyer 24h btc sum
0.0388
12
bitcoins
0.0289
13
hours
0.0273
14
round level
0.0262
15
time since last trade
0.0179
16
price deviation
0.0166
Table 9: Importance scores for XGB features on Mt. Gox dataset.
Interestingly, the optimized Cong, Li, Tang and Yang (2023) regressions we developed in Section
5.2 appear 5th out of 16 in the list, labeled cumu wash percent opt. This relatively high ranking
demonstrates the effectiveness of this specialized method for detecting wash trading patterns in
fungible tokens, even when compared to more general trading behavior features.
Summary of Indirect Estimation Method #2 - Machine Learning
(I6) All three predictive algorithms we test substantially reduce aggregate estimation errors (in-
cluding for the Blur marketplace). XGBoost and Deep Learning perform better than Random
Forest in terms of ROC-AUC scores.
35


### Page 36

(I7) The main features that drive wash trading predictability relate to unusual short-term trading
activity, time since last trade, and price deviations. The τ-regression feature also plays an
important role for some ML methods.
(I8) The machine learning framework extends beyond NFTs, achieving remarkable performance
on the Bitcoin dataset from Aloosh and Li (2024), (<1% errors and 0.97 AUC).
7
Indirect Estimation #3: Distributional Methods
In this section, we turn our attention to the distributional statistical tests from Cong, Li, Tang and
Yang (2023) that assess market manipulation presence in aggregate, rather than predicting specific
wash trading quantities.
7.1
Benford’s Law
Benford’s Law predicts that in many natural datasets, smaller leading digits appear more frequently
than larger ones (e.g., 1 appears ∼30% of the time, while 9 appears ∼5%). Significant deviation
from this expected distribution may indicate manipulation, such as price fixing or wash trading.
For this test, we extract the first nonzero digit from each NFT transaction price (e.g., 1 for
0.125 ETH) and compare it to Benford’s expected distribution for wash trades and legitimate trades.
We test the null hypothesis that the observed distribution follows Benford’s law at a significance
level of α = 0.05. Results are shown in Figures 6, 7, and 8.
36


### Page 37

1.0
2.0
3.0
4.0
5.0
6.0
7.0
8.0
9.0
Digits
0
5
10
15
20
25
30
Frequency (%)
31.2
16.9
11.3
9.6
6.5
5.9
4.8
4.9
9.0
Benfords distribution
Empirical distribution
(a) LooksRare Wash Trades.
Anomaly detected, p < 0.001, Tstats = 8231.39
1.0
2.0
3.0
4.0
5.0
6.0
7.0
8.0
9.0
Digits
0
5
10
15
20
25
30
Frequency (%)
31.2
17.2
11.1
9.3
6.1
5.8
5.1
4.9
9.4
Benfords distribution
Empirical distribution
(b) LooksRare Legitimate Trades.
Anomaly detected, p < 0.001, Tstats = 14385.7
Figure 6: Distribution of first significant price digits for LooksRare wash and legitimate trades.
1.0
2.0
3.0
4.0
5.0
6.0
7.0
8.0
9.0
Digits
0
5
10
15
20
25
30
Frequency (%)
33.0
15.3
11.0
9.2
7.5
6.7
5.4
4.7
7.1
Benfords distribution
Empirical distribution
(a) Blur Wash Trades.
Anomaly detected, p < 0.001, Tstats = 32744.8
1.0
2.0
3.0
4.0
5.0
6.0
7.0
8.0
9.0
Digits
0
5
10
15
20
25
30
Frequency (%)
31.6
16.2
11.6
9.3
7.5
6.4
5.2
4.5
7.7
Benfords distribution
Empirical distribution
(b) Blur Legitimate Trades.
Anomaly detected, p < 0.001, Tstats = 53124.6
Figure 7: Distribution of first significant price digits for Blur wash and legitimate trades.
1.0
2.0
3.0
4.0
5.0
6.0
7.0
8.0
9.0
Digits
0
5
10
15
20
25
30
Frequency (%)
28.9
16.4
11.7
10.3
6.6
6.6
6.0
6.7
6.7
Benfords distribution
Empirical distribution
(a) OpenSea Wash Trades.
Anomaly detected, p < 0.001, Tstats = 127535
1.0
2.0
3.0
4.0
5.0
6.0
7.0
8.0
9.0
Digits
0
5
10
15
20
25
30
Frequency (%)
29.6
16.5
11.8
9.8
6.7
6.8
6.1
6.5
6.4
Benfords distribution
Empirical distribution
(b) OpenSea Legitimate Trades.
Anomaly detected, p < 0.001, Tstats = 211007
Figure 8: Distribution of first significant price digits for OpenSea wash and legitimate trades.
In these figures, the black bars represent the empirical first-digit distribution, while red dots
denote the Benford expected values. Deviations indicate non-conformity, quantified by the p-value
(probability of observing such deviation under the null) and the t-statistic (magnitude of deviation
in standard error units).
37


### Page 38

Across LooksRare, Blur, and OpenSea, both wash and legitimate trades yield near zero p-values,
confirming statistically significant departures from Benford’s Law. Surprisingly, legitimate trades
show higher t-statistics than wash trades, indicating even greater divergence. These findings suggest
that Benford’s Law may not be applicable to NFT data, as both wash and non-wash samples display
anomalies.
This contrasts with Cong, Li, Tang and Yang (2023), where regulated exchanges followed Ben-
ford’s Law while unregulated Tier-2 exchanges deviated.
7.2
Trade-Size Clustering
Trade-size clustering stems from the tendency of legitimate traders to prefer round numbers, simpli-
fying decision-making and reducing transaction costs. Following Cong, Li, Tang and Yang (2023),
we analyze NFT trade prices (in ETH) using a base unit of 0.001 ETH to capture meaningful round
sizes. We then assess clustering at multiples of 100 base units to distinguish genuine trades from
algorithm-driven wash trading. Results are shown in Figures 9, 10, and 11.
0
200
400
600
800
1000
Trade Size in base unit
100
101
102
103
104
105
Count (Log Scale)
(a) LooksRare Wash Trades
0
200
400
600
800
1000
Trade Size in base unit
100
101
102
103
104
105
Count (Log Scale)
(b) LooksRare Legitimate Trades
Figure 9: Trade-size clustering analysis for LooksRare wash and legitimate trades.
38


### Page 39

0
200
400
600
800
1000
Trade Size in base unit
100
101
102
103
104
105
106
Count (Log Scale)
(a) Blur Wash Trades
0
200
400
600
800
1000
Trade Size in base unit
100
101
102
103
104
105
106
Count (Log Scale)
(b) Blur Legitimate Trades
Figure 10: Trade-size clustering analysis for Blur wash and legitimate trades.
0
200
400
600
800
1000
Trade Size in base unit
100
101
102
103
104
105
106
107
Count (Log Scale)
(a) OpenSea Wash Trades
0
200
400
600
800
1000
Trade Size in base unit
100
101
102
103
104
105
106
107
Count (Log Scale)
(b) OpenSea Legitimate Trades
Figure 11: Trade-size clustering analysis for OpenSea wash and legitimate trades.
These histograms show trade-size distributions on a logarithmic scale. Blue bars represent trade
counts per size interval, while red bars mark multiples of 100, highlighting potential clustering.
Regular peaks at these intervals could indicate manual or algorithmic trading tendencies, with
differences between wash and legitimate trades potentially revealing manipulation.
Across LooksRare, Blur, and OpenSea, we apply a uniform 1000 base-unit cutoff and bin trades
in increments of 10.
No strong clustering effect is observed in the figures, for either wash or
legitimate trades on any platform.
39


### Page 40

To quantify trade-size clustering more formally, we apply the Student’s t-test:
t = ¯x −µ0
s/√n ,
where ¯x is the difference between the mean frequency of rounded and unrounded trade sizes, s is
the sample standard deviation, and n is the sample size.
Following Cong, Li, Tang and Yang (2023), we compute trade frequencies using two sets of
observation windows: 100-unit windows ([100X - 50, 100X +50]) and 500-unit windows ([500X -
100, 500X + 100]). A trade is “rounded” if its size is an exact multiple of 100 (or 500, depending
on the window); otherwise, it is “unrounded.” The null hypothesis states no difference between the
frequencies of rounded and unrounded trades. Table 10 presents the t-statistics for each sub-sample.
Windows in 100s
Windows in 500s
LooksRare wash
-16.46
-24.00
LooksRare legitimate
-8.53
-11.06
Blur wash
-143.56
-27.51
Blur legitimate
-351.77
-16.16
OpenSea wash
-246.86
-114.11
OpenSea legitimate
-4.04
-1.56
Table 10: t-statistics for trade size clustering in 100 and 500 unit windows.
All t-statistics are negative, indicating that rounded trade sizes occur less frequently than
unrounded ones. The absolute value of the t-statistic reflects the strength of this effect—larger
values indicate stronger avoidance of round numbers.
On LooksRare, both wash and legitimate trades show moderate negative t-values (wash: −16.46
and −24.00; legitimate: −8.53 and −11.06), suggesting a limited clustering effect. On Blur, the
t-statistics indicate a strong avoidance of round numbers, especially in the 100-unit window (wash:
−143.56; legitimate: −351.77), while the effect is weaker in the 500-unit window (wash: −27.51;
legitimate: −16.16). On OpenSea, wash trades exhibit a strong avoidance (−246.86 and −114.11),
whereas legitimate trades show only a slight difference (−4.04 and −1.56).
40


### Page 41

This method effectively differentiates NFT wash and non-wash trades, though in a subtle way.
Unlike Cong, Li, Tang and Yang (2023), where regulated exchanges exhibited clear clustering
around round numbers, our results indicate a general avoidance of round numbers across all NFT
trades. However, legitimate trades still display weaker avoidance than wash trades—except on Blur
(100-unit window), where the effect is slightly reversed.
7.3
Tail Distribution
Financial and cryptocurrency markets often exhibit fat-tailed distributions, well-approximated by
power laws:
P(X > x) ∼x−α,
where α is the power-law exponent, reflecting the probability of extreme trade sizes.
Large α
(steeper slope) indicates thinner tails, while small α (shallower slope) suggests fatter tails.
For NFTs, we analyze the top 10% of trade sizes (trades above the 90th percentile) and es-
timate α using Ordinary Least Squares (OLS) and Maximum Likelihood Estimation (MLE) (Hill
estimator). In unmanipulated markets, α typically falls in the Pareto-L´evy regime, α ∈(1, 2), with
deviations suggesting anomalies.
Figures 12, 13, and 14 compare the tail distributions of wash and legitimate trades across
marketplaces. Trade sizes are plotted against probability densities on a log-log scale. Blue dots
represent the empirical data, while the red and black lines show the OLS and MLE fits, respectively:
41


### Page 42

12
13
14
15
16
Trade Size in base unit (Log Scale)
25.0
22.5
20.0
17.5
15.0
12.5
10.0
Probability Density (Log Scale)
Empirical Data (Top 10%)
OLS Fit
MLE Fit
(a) LooksRare Wash Trades
8
9
10
11
12
13
14
15
16
Trade Size in base unit (Log Scale)
25.0
22.5
20.0
17.5
15.0
12.5
10.0
Probability Density (Log Scale)
Empirical Data (Top 10%)
OLS Fit
MLE Fit
(b) LooksRare Legitimate Trades
Figure 12: Trade-size tail distributions for LooksRare wash and legitimate trades
8
9
10
11
12
13
Trade Size in base unit (Log Scale)
22
20
18
16
14
12
10
8
6
Probability Density (Log Scale)
Empirical Data (Top 10%)
OLS Fit
MLE Fit
(a) Blur Wash Trades
7
8
9
10
11
12
Trade Size in base unit (Log Scale)
22
20
18
16
14
12
10
8
6
Probability Density (Log Scale)
Empirical Data (Top 10%)
OLS Fit
MLE Fit
(b) Blur Legitimate Trades
Figure 13: Trade-size tail distributions for Blur wash and legitimate trades
6
7
8
9
10
11
12
13
14
Trade Size in base unit (Log Scale)
30
25
20
15
10
5
Probability Density (Log Scale)
Empirical Data (Top 10%)
OLS Fit
MLE Fit
(a) OpenSea Wash Trades
6
8
10
12
14
16
18
Trade Size in base unit (Log Scale)
30
25
20
15
10
5
Probability Density (Log Scale)
Empirical Data (Top 10%)
OLS Fit
MLE Fit
(b) OpenSea Legitimate Trades
Figure 14: Trade-size tail distributions for OpenSea wash and legitimate trades
42


### Page 43

Table 11 summarizes the estimated exponents. In general, the OLS and MLE lines intersect,
except for the LooksRare wash trades where they run parallel—suggesting unique tail behavior,
possibly due to outliers or idiosyncrasies in the distribution.
ˆαOLS
ˆαHill
LooksRare wash
2.2957
1.9357
LooksRare legitimate
2.3559
1.9319
Blur wash
2.8993
1.8675
Blur legitimate
2.8925
2.1322
OpenSea wash
2.5178
2.0780
OpenSea legitimate
2.6357
2.0164
Table 11: Estimated power-law exponents (ˆα) from OLS and Hill Estimator (MLE) for trade-size
tails
Cong, Li, Tang and Yang (2023) found a clear distinction between regulated and unregulated
exchanges: regulated platforms adhered to the Pareto–L´evy regime with tail exponents, α ∈(1, 2),
while unregulated exchanges exhibited deviations, α ̸∈(1, 2). However, our results show that this
method does not apply to NFT markets, as none of the platforms, whether wash trade sub-sample
or not, exhibit exponents within the expected range. This suggests that power-law tail analysis
may not be a reliable diagnostic for manipulation in NFT markets.
7.4
Summary of Indirect Estimation Method #3 - Distributional Methods
As a summary, the distributional methods yield the following key insights:
(I9) Benford’s Law: Both wash and legitimate trades deviate from Benford’s Law, with legiti-
mate trades showing greater deviations.
(I10) Trade-Size Clustering: Legitimate trades exhibit slightly more clustering around round
numbers compared to wash trades.
(I11) Tail Distribution: NFT trade-size tails differ from those in traditional financial markets.
43


### Page 44

8
Discussion
In this paper, we introduced a novel framework for detecting and quantifying wash trading in
NFT markets by leveraging public on-chain data from three major exchanges. Our analysis reveals
that nearly 38% of trades—and a disproportionately higher 60% of traded value—likely involve
manipulation.
These findings augment those of prior studies that relied on indirect statistical
proxies or leaked private data, demonstrating the importance of granular on-chain evidence.
A central contribution of our work lies in its critical evaluation of existing indirect detection
methods. We revisited roundedness-based regressions, as popularized in earlier studies, and showed
that while such methods have promise, they are inherently error-prone when applied to NFTs. To
overcome these challenges, we developed an enhanced approach: an optimized τ-regression method
integrated within an AI-driven estimation framework. This hybrid methodology markedly reduces
estimation errors—down to below 1.30%—across various platforms and even generalizes to fungible
token markets (Bitcoin). Thus, our study bridges the gap between traditional statistical models
and modern machine learning techniques, setting a new benchmark for precision in wash trading
detection.
Our findings also shed light on the unique dynamics shaping NFT manipulation. Although
NFTs share many of the same wash trading incentives found in cryptocurrency markets, key struc-
tural differences—such as on-chain transaction fees, zero-fee trading models, royalty earnings, and
price opacity—create distinct economic incentives. These factors, coupled with the unprecedented
transparency of blockchain technology, have paradoxically contributed to a market environment
where manipulative practices can sometimes thrive. As Web3 innovations continue to redefine the
financial landscape, the tension between enhanced transparency and the evolution of sophisticated
market manipulation becomes ever more pronounced.
Perhaps most importantly, our work carries significant regulatory implications. The high accu-
racy of our machine learning models—boasting AUC scores exceeding 0.9 on platforms like Blur
44


### Page 45

and Mt. Gox—indicates that regulators could feasibly implement automated, real-time surveillance
systems to flag suspicious trading patterns. Yet, the marked variation in wash trading behavior
across exchanges cautions against a uniform, one-size-fits-all regulatory approach. Instead, our re-
sults advocate for exchange-specific frameworks to ensure effective detection across diverse market
settings.
Moreover, while our enhanced detection systems provide powerful tools for uncovering manip-
ulative behavior, they are intended to complement, not replace, the judicial process. Some trading
behaviors—such as asset transfers conducted for privacy, tax optimization, or risk management
purposes—may superficially resemble wash trading, leading to potential misclassification. This in-
herent ambiguity underscores a broader challenge in wash trading enforcement, which often relies
on inferring intent from circumstantial evidence. U.S. regulators, for example, define wash trading
based on its outcome—specifically, the absence of genuine ownership or risk change—rather than on
explicit intent, making judicial deliberation essential. By following outcome-based best practices
and identifying transactions that most strongly exhibit the characteristics associated with wash
trading, our approach reinforces its role as a critical complement to, rather than a substitute for,
due process and nuanced legal adjudication.
In sum, this paper advances the literature by offering a rigorous, multi-layered analysis that
not only challenges existing methodologies but also provides innovative solutions for accurately
detecting wash trading in NFT markets and beyond. By critically evaluating traditional approaches
and integrating state-of-the-art machine learning techniques, we deliver a scalable framework that
enhances our understanding of digital asset manipulation and informs both academic inquiry and
practical regulatory policymaking. As the Web3 ecosystem continues to evolve, future research
should extend these methodologies to broader asset classes, ensuring that regulatory measures keep
pace with the rapid innovations reshaping financial markets.
45


### Page 46

References
Aloosh, A. and Li, J. (2024), ‘Direct evidence of bitcoin wash trading’, Management Science 70(12), 8875–
8921.
URL: https://doi.org/10.1287/mnsc.2021.01448
Amiram, D., Lyandres, E. and Rabetti, D. (2025), ‘Trading volume manipulation and competition among
centralized crypto exchanges’, Management science .
URL: https://doi.org/10.1287/mnsc.2021.02903
Arik, S. O. and Pfister, T. (2021), ‘Tabnet: Attentive interpretable tabular learning’, Proceedings of the
AAAI Conference on Artificial Intelligence 35(8), 6679–6687.
URL: https://ojs.aaai.org/index.php/AAAI/article/view/16826
Barter, J. (2023), ‘Blur continues momentum with incentive program’, Meta Digest . Accessed: 2023-11-23.
URL: https://metadigest.io/blur-continues-momentum-with-incentive-program/
Bonifazi, G., Cauteruccio, F., Corradini, E., Marchetti, M., Montella, D., Scarponi, S., Ursino, D. and
Virgili, L. (2023), ‘Performing wash trading on NFTs: Is the game worth the candle?’, Big Data and
Cognitive Computing 7(1).
URL: https: // www. mdpi. com/ 2504-2289/ 7/ 1/ 38
Cao, Y., Li, Y., Coleman, S., Belatreche, A. and McGinnity, T. M. (2014), Detecting wash trade in the
financial market, in ‘2014 IEEE Conference on Computational Intelligence for Financial Engineering
& Economics (CIFEr)’, pp. 85–91.
Chen, S., Chen, J., Yu, J., Luo, X. and Wang, Y. (2024), The dark side of nfts: A large-scale empirical study
of wash trading, in ‘Proceedings of the 15th Asia-Pacific Symposium on Internetware’, Internetware
’24, Association for Computing Machinery, New York, NY, USA, p. 447–456.
URL: https://doi.org/10.1145/3671016.3674808
Chen, T. and Guestrin, C. (2016), Xgboost: A scalable tree boosting system, in ‘Proceedings of the 22nd
ACM SIGKDD International Conference on Knowledge Discovery and Data Mining’, KDD ’16, ACM,
p. 785–794.
URL: http://dx.doi.org/10.1145/2939672.2939785
Cong, L. W., Landsman, W., Maydew, E. and Rabetti, D. (2023), ‘Tax-loss harvesting with cryptocurrencies’,
46


### Page 47

Journal of Accounting and Economics 76(2), 101607.
URL: https://www.sciencedirect.com/science/article/pii/S0165410123000319
Cong, L. W., Li, X., Tang, K. and Yang, Y. (2023), ‘Crypto wash trading’, Management Science 69(11), 6427–
6454.
URL: https://doi.org/10.1287/mnsc.2021.02709
Decrypt (2023), ‘How much wash trading is really happening on blur?’.
URL: https://decrypt.co/122369/wash-trading-blur-ethereum-nfts
Dune (2022), ‘NFT wash trading on Ethereum’.
URL: https://community.dune.com/blog/nft-wash-trading-on-ethereum
Falk, B., Tsoukalas, G. and Zhang, N. (2025), ‘Can AI detect wash trading? evidence from NFTs’. Dataset
and replication code.
URL: https://doi.org/10.17632/4hyxfwzpgg.1
Fridgen, G., Kr¨aussl, R., Papageorgiou, O. and Tugnetti, A. (2025), ‘Pricing dynamics and herding behaviour
of nfts’, European Financial Management 31(2), 670–710.
URL: https://onlinelibrary.wiley.com/doi/abs/10.1111/eufm.12506
Huang, D. and Goetzmann, W. N. (2023), Selection-neglect in the NFT bubble, Working Paper 31498,
National Bureau of Economic Research.
URL: http: // www. nber. org/ papers/ w31498
Mao, R., Li, Z. and Fu, J. (2015), Fraud transaction recognition: A money flow network approach, in ‘Pro-
ceedings of the 24th ACM International on Conference on Information and Knowledge Management’,
CIKM ’15, Association for Computing Machinery, New York, NY, USA, p. 1871–1874.
URL: https://doi.org/10.1145/2806416.2806647
Morgia, M. L., Mei, A., Mongardini, A. M. and Nemmi, E. N. (2023), A Game of NFTs: Characterizing
NFT Wash Trading in the Ethereum Blockchain , in ‘2023 IEEE 43rd International Conference on
Distributed Computing Systems (ICDCS)’, IEEE Computer Society, Los Alamitos, CA, USA, pp. 13–
24.
URL: https://doi.ieeecomputersociety.org/10.1109/ICDCS57875.2023.00018
Oh, S. (2024), ‘Market manipulation in non-fungible token markets’. Available at SSRN: https://ssrn.
47


### Page 48

com/abstract=4397409 or http://dx.doi.org/10.2139/ssrn.4397409.
O’Hara, M., Yao, C. and Ye, M. (2014), ‘What’s not there: Odd lots and market data’, The Journal of
Finance 69(5), 2199–2236.
URL: http://www.jstor.org/stable/43612955
Shimron, L. (2022), ‘DEXs gain market share as faith in centralized crypto players erodes’, Forbes . Avail-
able at:
https://www.forbes.com/sites/leeorshimron/2022/11/23/dexs-gain-market-share-as-faith-in-
centralized-crypto-players-erodes.
von Wachter, V., Jensen, J. R., Regner, F. and Ross, O. (2022), Nft wash trading: Quantifying suspicious
behaviour in nft markets, in ‘Financial Cryptography and Data Security. FC 2022 International Work-
shops: CoDecFin, DeFi, Voting, WTSC, Grenada, May 6, 2022, Revised Selected Papers’, Springer-
Verlag, Berlin, Heidelberg, p. 299–311.
URL: https://doi.org/10.1007/978-3-031-32415-4 20
Zitzewitz, E. (2012), ‘Forensic economics’, Journal of Economic Literature 50(3), 731–69.
URL: https://www.aeaweb.org/articles?id=10.1257/jel.50.3.731
48


### Page 49

A
More Detailed Table
Our Paper
Aloosh & Li (2024)
Cong et al. (2023)
Dataset
Assets
NFTs
Bitcoin
Crypto
Multiple tokens/currencies?
✓
×
✓
Multiple exchanges?
✓
×
✓
Public On-Chain Data?
✓
×
×
Transaction-level estimators?
✓
✓
×
All methods apply without leaked info?
✓
×
✓
Efficacy of Distributional Filters
Benford (Section 7.1)
×
✓
✓
Trade Size Clustering (Section 7.2)
✓
×
✓
Power Tail (Section 7.3)
×
×
✓
Avg. Wash Value % - Direct
Our ∪fi filters (Section 4)
60.08%
×
×
f1 (Self trades)
0.14%
×
×
f2 (Back-and-forth trades)
40.17%
×
×
f3 (3 times around)
39.04%
×
×
f4 (Common funder)
47.03%
×
×
∪ifi
60.08%
×
×
Aloosh & Li filters
×
34.39%
×
G0 (Self trades)
×
1.39%
×
G1 (G0∪known insiders)
×
1.62%
×
G2 (G1∪double users)
×
2.04%
×
G3 (G2∪hijackers)
×
2.06%
×
G4 (G3∪zero-fee traders)
×
2.21%
×
G5 (G4∪all wash traders)
×
34.39%
×
Avg. Wash Value Estimation % - Indirect
1-Regression (Section 5.1)
46.98%
3.30%
70.85%
τ-Regression (Section 5.2)
52.75%
×
×
Machine/Deep Learning (Section 6)
60.19%
×
×
Avg. Wash Value Estimation % Error
1-Regression (Section 5.1)
13.10%
31.09%
×
τ-Regression (Section 5.2)
7.33%
×
×
Machine/Deep Learning (Section 6)
0.11%
×
×
Table 12: A more detailed comparison to seminal papers.
49


### Page 50

B
ML Hyperparameters used for training
Parameter
Mt. Gox
Blur
LooksRare
OpenSea
n d
256
256
256
128
n a
256
256
256
128
n steps
1
1
1
1
gamma
1.4
1.4
1.4
1.4
lambda sparse
1e-4
1e-4
1e-4
1e-4
optimizer
Adam
Adam
Adam
Adam
learning rate
2e-2
2e-2
2e-2
2e-2
scheduler
StepLR
StepLR
StepLR
StepLR
step size
10
10
10
10
scheduler gamma
0.92
0.92
0.92
0.92
mask type
sparsemax
sparsemax
sparsemax
sparsemax
momentum
0.2
0.2
0.2
0.2
batch size
215
215
215
215
virtual batch size
8000
8000
8000
8000
num workers
24
24
24
24
max epochs
500
500
500
500
patience
500
500
500
500
device
cuda
cuda
cuda
cuda
avg. runtime (per fold)
2:58:11
2:03:13
0:42:03
1:33:17
Table 13: Final hyperparameters used for DL. For OpenSea, only the first 5% of data was used to
keep runtime comparable with other platforms, given its much larger scale.
Parameter
Mt. Gox
Blur
LooksRare
OpenSea
tree method
hist
hist
hist
hist
device
cuda
cuda
cuda
cuda
n jobs
-1
-1
-1
-1
n estimators
110
5000
5000
5000
max depth
15
15
15
15
learning rate
0.09
0.1
0.1
0.1
subsample
0.9
0.8
0.8
0.8
colsample bytree
0.9
0.8
0.8
0.8
min child weight
2
1
1
1
alpha
0.1
0
0
0
reg lambda
1.5
1
1
1
random state
42
42
42
42
scale pos weight
Computed
Computed
Computed
Computed
early stopping rounds
50
5000
5000
5000
eval metric
auc
auc
auc
auc
avg. runtime (per fold)
0:00:16
0:03:50
0:01:18
0:15:25
Table 14: Final hyperparameters used for XGB
50


### Page 51

Parameter
Mt. Gox
Blur
LooksRare
OpenSea
n estimators
100
100
100
100
max depth
5
5
5
5
max features
sqrt
sqrt
sqrt
sqrt
n jobs
-1
-1
-1
-1
random state
42
42
42
42
class weight
balanced
balanced
balanced
balanced
avg. runtime (per fold)
0:00:39
0:00:20
0:00:01
0:02:42
Table 15: Final hyperparameters used for RF
C
Competition and Wash Trading in NFT Markets
This section explores whether increased competition, measured by the entry of new NFT collections,
is associated with increased wash trading among top collections.
We run a simple linear regression separately for each platform (Blur, LooksRare, OpenSea),
using weekly data. For each platform, we define the top 10 collections by cumulative volume as
focal collections. Competition is proxied by the number of new NFT collections that appear on
the platform in a given week, excluding focal collections. A new entrant is any contract address
observed for the first time during that week. The outcome variable is weekly wash trading volume
for each focal collection, identified using the direction filter (∪fi) described in Section 4.
We use transaction-level data from Blur, LooksRare, and OpenSea (see Section 3), spanning
October 2022 to March 2024 (Blur), December 2021 to April 2023 (LooksRare), and February
2022 to March 2024 (OpenSea). Transactions are aggregated into weekly wash volume per focal
collection. To focus on periods of relevant activity, we retain only weeks where at least one focal
collection records nonzero wash trading.
The resulting panel data enable a pooled regression
specification with collection fixed effects.
We estimate the following model per platform:
WashVoli,t = α + β · NewEntrantst + γi + εi,t,
(4)
51


### Page 52

where i indexes focal collections and t indexes weeks. The term γi denotes collection fixed effects,
implemented as a set of dummy variables for each focal collection to control for time-invariant
differences across them.
Table 16 summarizes the regression results.
Platform
Weeks Retained
Obs.
Coefficient (ˆβ)
p-value
R2
Blur
40
352
5.46 × 1018
0.0078
0.227
LooksRare
65
295
1.94 × 1020
0.0000
0.210
OpenSea
68
522
1.87 × 1017
0.3717
0.059
Table 16: Weekly wash volume on top 10 collections regressed on number of new collections.
We find a positive and statistically significant relationship on Blur and LooksRare, but no effect
on OpenSea. These results suggest that competition may be associated with short-term volume
inflation in some marketplaces. However, the effect is not consistent across platforms and does not
amount to a systematic pattern. As such, this could be an interesting direction for future work.
52

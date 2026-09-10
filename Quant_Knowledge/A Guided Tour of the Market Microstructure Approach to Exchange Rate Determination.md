| A Guided | Tour of     | the | Market | Microstructure |
| -------- | ----------- | --- | ------ | -------------- |
| Approach | to Exchange |     | Rate   | Determination∗ |
Paolo Vitale
University†
|     | D’Annunzio |         | and  | CEPR |
| --- | ---------- | ------- | ---- | ---- |
|     |            | January | 2006 |      |
Abstract
We propose a critical review of recent developments in exchange rate economics which have
offered a novel approach to exchange rate determination. This new strand of research, the
market microstructure approach to exchange rates, is motivated by some very stark empirical
evidence, relating exchange rate dynamics to the imbalance in the sequence of purchases and
sales of foreign currencies in the markets for foreign exchange. Through our review we outline
the results this new strand of research has achieved alongside its open questions and future
challenges.
| JEL Nos.: D82, G14 | and G15. |     |     |     |
| ------------------ | -------- | --- | --- | --- |
Keywords: Order Flow, Foreign Exchange Microstructure, Exchange Rate Dynamics.
∗Discussions with Kathryn Dominguez, Ryan Love and Richard Lyons were extremely stimulating. Several help-
ful comments from the editor and three anonymous referees are gratefully acknowledged. Any errors remain my
responsibility.
†Department
of Economics and Land History, Gabriele D’Annunzio University, Viale Pindaro 42, 65127 Pescara
(Italy), phone: ++39-085-453-7647; fax: ++39-085-453-7565; e-mail: p.vitale@unich.it.

Introduction
In the 1980s an extensive body of empirical research on the models of exchange rate determination
developedinthe1970sindicatedhowthesewerenotabletoexplainexchangeratemovementsinthe
short-run. Typically, the coefficients of the regressors employed to explain exchange rate dynamics
would present the wrong sign or would not be significantly different from zero, while the coefficient
of multiple correlation would take extremely low values.1 On the other hand, more recent empirical
studies based on cointegration analysis suggest that the equilibrium relations provided by these
models hold in the long-run.2
A popular explanation for the difficulty of these traditional models in explaining short-run
exchange rate dynamics lies with the particular forward looking nature of currency values and with
the impact that the arrivals of news on macro variables have on exchange rates. Indeed, when
news reaches financial markets, conditioning market expectations of future values of exchange rate
fundamentals, currencyvaluesimmediatelyreactanticipatingtheeffectofthesefundamentalshifts.
Since news is hard to observe, it is difficult to control for news effects on exchange rate dynamics
and hence it is hard to conduct any meaningful analysis of traditional models of exchange rate
determination.
With this background, a new strand of research has proposed a novel approach to exchange rate
determination. Very recently researchers have gained access to detailed data on the transactions
of individual traders in foreign exchange (FX) markets and have hence turned their attention to
the study of such trading activity. Indeed, it has been suggested that moving from a macro to
a micro perspective allows to bypass the analysis of the relation between fundamental variables
and exchange rates. According to this approach the imbalance between buyer-initiated and seller-
initiated trades in FX markets represents the transmission link between fundamental information
and exchange rates, in that it conveys information on deeper determinants of exchange rates, which
FX markets need to aggregate and impound in currency values.
In this survey we do not attempt to offer a comprehensive overview of what is generally referred
as the market microstructure approach to exchange rates, we rather prefer to conduct a guided
tour of the most interesting and promising contributions of this very recent strand of research.3
Moreover, we limit the boundaries of our survey as we concentrate on exchange rate determination.
This means that we do not discuss contributions which apply the market microstructure approach
tootherinternationalfinancequestions, suchastheanalysisofmarketperformance, marketdesign,
1See inter alia Meese and Rogoff (1983), Backus (1984), Frankel (1993) and Frankel and Rose (1994).
2See Mark (1995) and McDonald and Taylor (1995).
3An extremely useful website containing up-to-date information on the market microstructure approach to ex-
change rates can be found at the following URL: http://faculty.haas.berkeley.edu/lyons/wpothers.html.
1

monetary union and alternative exchange rate regimes.
The survey is structured as follows. In Section 1 we briefly present the trading structure of FX
markets. In the following Section, it is discussed some stark evidence showing a strong contem-
poraneous correlation between order flow and exchange rate variations. In Section 3, we discuss
estimates of VAR models of order flow and exchange rate returns. In this way proper impulse
response functions can be derived and short- and long-term effects of shocks can be studied, so as
to outline possibly portfolio-balance and information effects of currency trades. In Section 4, the
VAR approach is extended to consider the short- and long-term inter-relations between order flow,
exchangeratereturnsandfundamentals. InthesameSectionwealsoexaminethepredictingpower
of order flow with respect to future fundamentals and exchange rates.
In Section 5, a simple structural model of exchange rate determination offers a theoretical
underpinningfortheempiricalevidencepertainingtotherelationbetweenspotrates,fundamentals
and order flow. Since order flow is often assigned an information content, in Section 6 empirical
studies of the inter-relation between order flow, news arrivals and spot rates are examined. In
Section 7 we discuss the role of central bank intervention in FX markets, since it corresponds to a
very important component of order flow. A final Section concludes with some general remarks on
the achievements and future challenges of this strand of research.
1 The Microstructure of Foreign Exchange Markets
Market microstructure theory is devoted to the study of the trading process in securities markets
underexplicittradingrules.4 Accordingtothistheorytheorganizationandregulationoftradingin
securitiesmarketshaveimportantimplicationsfortheprocessofpriceformationandmoregenerally
for all characteristics of these markets. However, this theory has been developed having in mind
equity markets and therefore it is mainly oriented toward micro questions, such as institution
design, regulation, and market performance.
The market microstructure approach to exchange rates is instead concerned with macro issues
andisparticularlyinterestedinsheddingsomelightonexchangeratedetermination. Thus,whereas
the market microstructure approach to exchange rates borrows the economic concepts and the
techniques of investigation developed within the traditional equity market microstructure theory,
it applies them to different questions and employs different sets of data and variables.
Before we can examine the market microstructure approach to exchange rate determination, let
4See O’Hara (1995) for an introduction to market microstructure theory and Madhavan (2000) for an exposition
of more recent developments.
2

us see in some detail the structure of FX markets. We should concentrate on four central aspects
of this structure. Firstly, one should note that since these markets by their nature are dislocated in
several financial centers, practically no rules can be imposed on their functioning and the activity
of their participants. This means that their organization is not the result of the decisions of some
authorities but the consequence of their natural evolution.
Secondly, one can easily classify the population of foreign exchange traders according to three
different types of agents: FX dealers, brokers and customers. FX dealers, generally from the
financial division of major commercial banks, trade among each others and with customers. These
maybelargecorporationsorfinancialinstitutions. Brokersareagentswhodonottradeontheirown
account. Instead, they help customers and/or FX dealers to complete their desired transactions.
Thirdly, transactions among these market participants can be either direct or can be mediated
by a broker. Several estimations suggest that the inter-dealer market accounts for about 50 to 60
percent of the total volume of trading and that almost 50% of these transactions are carried out
through a broker (BIS (2001,2004)).
Fourthly, in FX markets two different mechanisms of trading coexist: the direct (bilateral)
market is quote-driven and decentralized, while the indirect (brokered) market is order-driven and
quasi-centralized. As transactions can be completed at any time, markets for foreign exchange are
also continuous. We will now try to explain briefly what we mean with this terminology, whilst for
a more extensive analysis we refer to Lyons (2001) and Rime (2003).
The direct market operates like other dealership markets, such as the Nasdaq or the London
Stock Exchange (LSE), where transactions are the result of private bilateral “meetings” between
traders. In the past these meetings have generally been conducted on the phone. Nowadays,
though, FX dealers employ electronic communication systems, such as the Reuters Dealing 3000
spot matching system.
In the direct market transactions are quote-driven because prices are fixed before quantities. In
fact, clients contact single dealers, which “make the market” quoting bid and ask prices for any
specific foreign currency they trade. These quotes specify at which prices dealers (market makers)
will be ready to buy (bid) and to sell (ask) it. Then, clients can place orders to buy or sell the
currency. Since quotes are valid for orders not exceeding some prefixed amount, the size of these
transactions is limited, even though most market makers will accept very large orders.
The direct market is decentralized or fragmented in that transactions are completed through
private bilateral deals among traders and cannot be observed by other market participants. On the
contrary, in other securities markets, such as the NYSE, all transactions are centralized, because
3

tradingisorganizedaroundasinglemarketmakeroraccordingtoanopenoutcry system. Moreover,
there are other decentralized markets, notably the LSE, in which dealers are forced by institutional
rules to communicate almost immediately information on their sequence of transactions to all other
traders. Thesemechanismsofconsolidation areabsentinthedirectFXmarket, thathenceremains
fragmented and opaque.
The indirect market is order-driven. Here prices and quantities are set altogether. Moreover,
transactions are not the result of simple bilateral deals, but are mediated by brokers, that is agents
who do not deal on their own but operate on account of clients charging a small transaction fee.
Anybrokerkeeps abook of limit orders placed by his/her clients. Limit orders placed with a broker
are matched against other market and limit orders from other traders. A limit order specifies the
amount of a particular currency a trader is willing to sell (buy) and the minimum (maximum)
price he/she will accept. A market order indicates the intention to buy (sell) immediately a given
quantity of the foreign currency at the existing best price.
In the past, the indirect market was operated on the phone. Traders would call a broker and ask
for his inside spread on his/her limit order book. This means that the broker would quote the best
buy and sell limit orders contained in his/her book and that the trader would then have the faculty
to “hit” them, taking the other side of the outstanding orders. Nowadays the indirect market is
dominated by electronic brokerage systems, such as EBS and Reuters Dealing 2000-2.
The trading platforms of these electronic brokerage systems share some common features with
those of some centralized equity markets, such as the Paris Bourse or the SETS system in London.
The platform’s subscribers are attached to a screen reporting the best outstanding buy and sell
limit orders for a set of foreign currencies on an electronic limit order book. All other limit orders
remain in the background and are used to up-date the information available to the subscribers
when a transaction is completed or one of the best orders is withdrawn. At any time subscribers
can hit the limit orders posted on the screen or add their owns.
Sincethesearecentralizedmechanismsof trading, theindirect marketisquasi-centralized. How-
ever, given that the identities of traders which complete a transaction are kept anonymous, in that
they are not published on the platform screen, the indirect market remains partially opaque.
4

| 2 The | Explanatory |     | Power |     | of Order | Flow |     |     |     |
| ----- | ----------- | --- | ----- | --- | -------- | ---- | --- | --- | --- |
Traditional models of exchange rate determination are based on two fundamental principles: i)
exchange rate determination is basically a macro phenomenon, in that exchange rate movements
are uniquely determined by shifts in macro aggregates; and ii) exchange rates immediately react
to shifts in macro aggregates. In other words, after a variation in the inflation rate or in the GDP
growth a new equilibrium exchange rate is reached without any change in investors’ portfolios.
The meagre explanatory power of these traditional models alongside the empirical evidence
showing the importance of micro-structural aspects of the functioning of equity markets in explain-
ing short-term movements in equity prices have induced many researchers to turn their attention
toward the trading activity of market participants and order flow in FX markets.
Order flow is defined as the net of the buyer-initiated and seller-initiated orders in a securities
market. It is the simplest measure of buying pressure and it is calculated from: i) the sequence of
market orders reaching market makers in dealership markets; and ii) the sequence of market and
limit orders which reach electronic trading platforms and cross with existing posted limit orders.5
Order flow may convey information on exchange rate fundamentals, which FX markets need to
| aggregate | and impound | in currency |     | values. |     |     |     |     |     |
| --------- | ----------- | ----------- | --- | ------- | --- | --- | --- | --- | --- |
Evans and Lyons (2002) consider a very simple model of exchange rate determination which
makes use of the information contained in order flow. According to this model daily exchange rate
variations are determined by changes in the interest rate differential, as suggested by traditional
| models, | and signed order | flow. | Thus, |     |          |     |       |     |     |
| ------- | ---------------- | ----- | ----- | --- | -------- | --- | ----- | --- | --- |
|         |                  |       | ∆s    | =   | β ∆(i∗−i | ) + | β z , |     | (1) |
|         |                  |       |       | t+1 | i        | t t | z t   |     |     |
where ∆s is the first difference in the log of the foreign exchange price within day t, s −s ,
|     | t+1 |     |     |     |     |     |     |     | t+1 t |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
∆(i∗−i ) is the first difference in the interest rate differential, (i∗−i )−(i∗ −i ), and z is the
| t   | t   |     |     |     |     |     | t t t−1 | t−1 | t   |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- |
t.6
difference between the number of buyer-initiated and seller-initiated trades in day
To interpret this simple linear specification consider that a positive value for z implies that
t
within day t the number of buy orders exceed that of sell ones. This means that a majority
of traders has purchased the foreign currency during the day, indicating that they consider the
5Two distinct groups of traders operate on electronic trading platforms: “patient” or “passive” traders, which
are willing to offer liquidity at given prices; and “impatient” or “active” traders which, in search of immediacy, hit
outstandinglimitordersandconsumetheliquidityofferedbytheformergroup. Impatienttradersareinterpretedas
the initiators of transactions as their orders move prices and alter market conditions.
6Evans
and Lyons write equation (1) differently, as the dependent variable in their model is the price of the
| domestic | currency in terms | of the | foreign one. | We  | follow | the usual convention. |     |     |     |
| -------- | ----------------- | ------ | ------------ | --- | ------ | --------------------- | --- | --- | --- |
5

foreign currency undervalued. This imbalance might reflect all that news, in the form of macro
announcements, data releases, etc., which reaches FX markets and induces traders to modify their
evaluations of exchange rate returns and their portfolios of assets.
This interpretation is borrowed from equity market microstructure theory. Thus, Glosten and
Milgrom (1985) and Kyle (1985) have developed market micro structure models in which trade
innovations in equity markets contain information on future dividend announcements, which condi-
tion the fundamental values of equities and hence their equilibrium prices.7 Clearly, in the context
of the market microstructure approach to exchange rates information on dividends is replaced by
information on exchange rate fundamentals, such as interest rates, unemployment levels, GDP
growth rates, and so on.
EvansandLyonsemploydatapertainingtoall bilateraltransactionscompletedamongFXdeal-
ers via the Reuters Dealing 2000-1 electronic trading system in the spot USD/DEM and USD/JPY
markets between May 1st and August 31st 1996.8 Their data-set indicates for any transaction the
exchange rate, which of the two counter-parties bought and sold and, more importantly, which
initiated the transaction, allowing thus to define the corresponding direction (i.e. if a buy or a sell
order) of trade. The data-set does not report either the transaction size or the counter-parties’
identity.
EvansandLyonsconsolidatetheirtransactiondataatthedailylevelandthenestimateequation
(1). TheyfindthatbothfortheUSD/DEMandUSD/JPYregressionsapositivevaluefortheorder
flow z induces an increase in the spot rate. Thus, in the case of the USD/DEM regression, Evans
t
and Lyons estimate that in a day where DEM buy orders exceed DEM sell orders by 1000 the
German currency appreciates by 2.1%. Given that the average trade size in the sample for the spot
USD/DEM market is $3.9 million, $1 billion net purchases of the German currency increases its
value by 0.54%. Assuming that the USD/DEM rate is 1.5, the value of the DEM augments by 0.8
pfenning (i.e. 0.08 DEM).
BothfortheUSD/DEMandUSD/JPYregressionsthecoefficientoftheinterestratedifferential
is either not significant or does not contribute to the empirical fit of the regression. In particular,
in the USD/DEM regression the coefficient of multiple correlation, R2, takes a value larger than
0.6 when the order flow variable is included and falls dramatically when it is excluded. A similar
conclusion is drawn in the USD/JPY regression.9
7This thesis that trade innovations in equity markets may possess an information content was actually first put
forward by Bagehot (1971).
8TheReutersDealing2000-1systemistheelectronicplatformforbilateraltradingwhichpre-existedtherecently
introduced Reuters Dealing 3000 spot matching system.
9Otherstudies,notablyLyons(1995),BiønnesandRime(2001,2005),Danielsson et al. (2002),Hauet al (2002),
Carpenter and Wang (2003), Berger et al. (2005) and Killen et al. (2005) have reported very similar results to
6

A legitimate criticism against the linear regression proposed by Evans and Lyons refers to the
issue of simultaneity bias, which emerges if exchange rate movements cause order flow. In fact, in
the case in which the exchange rate presents a feedback effect on order flow the OLS estimate of
the coefficient β is biased. Suppose, in particular, that z = z +z , where
|           | z                  |     |       |     |         |     | t     | 1,t  | 2,t |             |
| --------- | ------------------ | --- | ----- | --- | ------- | --- | ----- | ---- | --- | ----------- |
|           |                    | z   | = γ∆s |     | , while |     | ∆s    | = αz | +   | (cid:178) . |
|           |                    | 2,t |       | t+1 |         |     | t+1   |      | 1,t | t           |
| If we     | run the regression |     |       |     |         |     |       |      |     |             |
|           |                    |     |       |     | ∆s      | = β | z + η | ,    |     |             |
|           |                    |     |       |     | t+1     | z   | t     | t    |     |             |
| the value | of β is equal      | to  |       |     |         |     |       |      |     |             |
z
|     |     |     | α(1 | +   | γα) + | γφ  |     |     |     | σ2  |
| --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
(cid:178)
|     |     | β z | =   |        |     | ,   | where | φ   | =   | .   |
| --- | --- | --- | --- | ------ | --- | --- | ----- | --- | --- | --- |
|     |     |     | (1  | + γα)2 | +   | γ2φ |       |     | σ2  |     |
z,1
Since z is not directly observable, it is not possible to establish whether a positive value for
2t,
the estimate of β corresponds to either α > 0 (with γ ≥ 0), so that order flow causes exchange
z
rates to move (with or without a feedback effect on order flow), or α = 0 and γ > 0, so that the
estimated β assumes a positive value only because of a positive feedback effect of the exchange
z
rate on order flow. Thus, in the presence of positive feedback trading rules (γ > 0) the results
| reported | by Evans | and Lyons | are      | spurious | and | hence | misleading. |     |     |     |
| -------- | -------- | --------- | -------- | -------- | --- | ----- | ----------- | --- | --- | --- |
| 3 Order  | Flow     | and       | Exchange |          |     | Rate  | Returns     |     |     |     |
To take into account the possible feedback effects of exchange rate movements on order flow an
alternative methodology can be employed. This is based on the study of a simple linear VAR
model for trades and quote revisions originally proposed by Hasbrouck (1991) for the analysis of
the NYSE.
Payne (2003) applies Hasbrouck’s methodology to a transaction data-set which refers to the
brokered section of the spot FX market. His study can then be considered a complement to
that of Evans and Lyons, which instead analyzes the direct market. He considers all inter-dealer
trades completed via the Reuters Dealing 2000-2 system in the spot USD/DEM market over the
week between October 6th and October 10th 1997. While this period is rather short, his data-set
those of Evans and Lyons for other markets and periods. In particular, Biønnes and Rime and Killen et al. show
that cumulative order flow and exchange rates are cointegrated. This suggests that the microstructure approach to
exchangeratedeterminationshouldnotnecessarilybeconfinedtotheanalysisofshort-runexchangeratedynamics.
In Table 1 we present a synthesis of these and other empirical studies of FX market microstructure.
7

containsinformationoverroughly30,000transactions, withatotalvolumeofmorethan$60billion.
DifferentlyfromEvansandLyons,Paynehasaccesstoinformationonthesizeofalltransactions.
This extra bit of information allows to measure more precisely the information content of order
flow, as in the presence of asymmetric information rational expectations models of asset pricing
information.10
show a clear dependence of trade size on Payne’s empirical methodology is based
| on the following | VAR | model for exchange | rate returns | and trades |               |
| ---------------- | --- | ------------------ | ------------ | ---------- | ------------- |
|                  |     |                    | (cid:88)p    | (cid:88)p  |               |
|                  |     | r =                | α r +        | β z        | + (cid:178) , |
|                  |     | t                  | i t−i        | zi t−i     | 1,t           |
|                  |     |                    | i=1          | i=0        |               |
|                  |     |                    | (cid:88)p    | (cid:88)p  |               |
|                  |     | z =                | γ r +        | δ z        | + (cid:178) . |
|                  |     | t                  | i t−i        | zi t−i     | 2,t           |
|                  |     |                    | i=1          | i=1        |               |
In his study Payne does not consolidate transactions and hence the interval (t,t+1] does not
refer to a given period of time, such as the day considered by Evans and Lyons. Indeed, Payne
does not use calendar time, but an event time, where an event is any instance in which either the
exchangeratebestquotes(i.e.thebestbidandaskprices)arerevisedoratransactioniscompleted
on the Reuters Dealing 2000-2 system. In this way the interval (t,t+1] refers to the spell of time
| between two | subsequent | events. |     |     |     |
| ----------- | ---------- | ------- | --- | --- | --- |
In this simple VAR model z t is now a vector containing trades information. This comprises: a
signedtradeindicator,whichtakesvalue1(-1)ifanordertobuy(sell)theUSdollariscompletedat
timetand0ifaquoterevisiontakesplaceattimettriggeredbytheintroductionorthecancellation
of a limit order; a signed trade size variable, to analyze the effect of volume on exchange rates;
a squared trade size variable, which is introduced to account for possible non linearities in the
| relation between | price | revisions and | order flow. |     |     |
| ---------------- | ----- | ------------- | ----------- | --- | --- |
Notethatthereturnontheforeigncurrency,r ,differsfromtheexchangeratevariation,s −s ,
t t t−1
i∗
by the interest rate differential − i t−1 . The difference is inconsequential at these very high
t−1
frequencies, because over such short spells of time the period-by-period interest rate differential,
i∗ − i , is negligible. This component of the exchange rate return is hence ignored in the
t−1 t−1
| calculation | of r . |     |     |     |     |
| ----------- | ------ | --- | --- | --- | --- |
t
In the VAR specification the contemporaneous realization of z enters into the regression for
t
the exchange rate return. The opposite is not true, in that in the regression for z only lag values
t
of the exchange rate return, r , are considered. Payne claims that at these very high frequencies
t
transactions logically anticipate quote revisions and hence he does not allow the opposite causality.
10In this respect, within market microstructure theory see the seminal contribution by Kyle (1985).
8

This assumption, alongside with that that the innovation terms, (cid:178) and (cid:178) , are uncorrelated,
1,t 2,t
permits identifying the VAR model.11
According to Payne’s interpretation of the VAR model the innovation term (cid:178) corresponds to
1,t
quote revisions induced by the arrival of public information, associated with macro announcements
and the like. The innovation term (cid:178) refers instead to unpredictable trading activity, possibly
2,t
associated with private information. From the vector moving-average (VMA) representation of the
VAR model Payne is able to derive the impulse-response functions associated with news releases
and trade innovations respectively. Payne suggests that the long-run response of exchange rates to
trade innovations can be considered a measure of the information content of order flow.
The long-run response of exchange rates to trade innovations allows to measure the information
content of order flow, but does not permit assessing its contribution to the total volatility of
exchangerates. However,underthehypothesisthatexchangeratescanbedecomposedinarandom
walk and a stationary process, Payne is able to separate the component of the total volatility of the
exchange rate which pertains to public information from that which is due to trade innovations.
Then, the importance of private information-based trades in determining exchange rate movements
can be measured via the ratio between these two components.
Employingonlythesignedtradeindicator amongthetransactioncharacteristics,z , Paynefinds
t
that in the exchange rate equation the coefficient of multiple correlation, R2, is equal to 0.25 and
that the sum of the coefficients β is positive and significantly different from zero, suggesting that
zi
order flow has a positive impact on exchange rates. From the VMA representation he finds that
the total impact of a US dollar buy order on the USD/DEM rate is equal to 0.005%, i.e. that a
purchase of the American currency brings about roughly a 1 basis point increase in its value, while
from the variance decomposition Payne finds that more than 40% of the exchange rate variability
must be attributed to unpredictable trading activity.
One should also notice that signed trade size and squared trade size when introduced among
the transaction characteristics are not significant. A possible explanation of this finding rests with
the very small variability observed in the trade size variable. However, it is rather worrying for an
information-based argument to find no relation between trade size and price impact. Possibly, this
is due to the strategic behavior of sophisticated informed traders, who may decide to split their
large trades, so that the link between information content and trade size is broken.12
11In a recent paper Danielsson and Love (2004) allow for contemporaneous feedback trading. In fact, differently
from Payne’s study, in their VAR specification order flow also depends on the current exchange rate return. Using
instrumental variables to estimate their VAR specification on EUR/USD data, Danielsson and Love derive impulse
responsefunctionsofspotratestotradeinnovationswhichtakeaccountofcontemporaneousfeedbacktrading. Their
analysis indicates an even stronger price impact of order flow than that outlined by Payne.
12An extensive literature on the strategic behavior of sophisticated informed traders exists within market mi-
9

In synthesis, Payne concludes that even when we take into account the possibility of feedback
trading signed order flow is still a key determinant of short-term exchange rate dynamics.
| 4 Fundamentals, |     |     | Order | Flow | and | Exchange | Rates |
| --------------- | --- | --- | ----- | ---- | --- | -------- | ----- |
Froot and Ramadorai (2005) examine the relation which exists between order flow, exchange rate
returnsandfundamentals. WithrespecttothestudiesofEvansandLyons(2002)andPayne(2003)
| there are | two major | differences | in  | their approach. |     |     |     |
| --------- | --------- | ----------- | --- | --------------- | --- | --- | --- |
Firstly, they employ a data-set of more than 6 million FX transactions obtained from State
Street Corporation, a very large global asset custodian. This data-set contains records of end-user
trades,consistingofallforeignexchangetransactionsfor111currenciesbymorethan10,000mutual
funds over the period between January 1st 1994 and February 9th 2001. Clearly, this is different
from previous studies where inter-dealer trades are considered. Secondly, they try to examine the
long-run effects of international flows on exchange rates and their relation to fundamentals.
As a starting point Froot and Ramadorai repeat the analysis of Evans and Lyons considering
| the following | regression |     |       |       |        |       |                |
| ------------- | ---------- | --- | ----- | ----- | ------ | ----- | -------------- |
|               |            |     | r     | (h) = | α + βh | z (h) | + (cid:178)h , |
|               |            |     | t+1,j |       | z,j    | t,j   | t,j            |
where r (h) is the h-period cumulative return on currency j over the interval (t−h+1,t+1],
t+1,j
(cid:80)
r (h) = h−1r , and z (h) is the corresponding cumulate for the signed order flow size,
| t+1,j |     | t+1−i,j | t,j |     |     |     |     |
| ----- | --- | ------- | --- | --- | --- | --- | --- |
(cid:80) i=0
h−1z
| z t,j (h) | =   | t−i,j . |     |     |     |     |     |
| --------- | --- | ------- | --- | --- | --- | --- | --- |
i=0
Becauseofthelackofenoughobservations,FrootandRamadoraidonotconsidersimplebilateral
rates. Rather, r (h) represents the return on currency j against a basket of major currencies,
t+1,j
while z t,j (h) is the corresponding value in US dollars of all currency j (net) inflows from the
countries in the basket during the interval (t−h+1,t+1]. This hides a weakness of Froot and
Ramadorai’smethodology. Indeed,whiletheirdata-setisverybroadcross-sectionally,itisalsovery
shallow in the major currencies, given that the observed trades account for less than 5 percent of
all transactions in these bigger markets. In other words, their study relies too much on information
obtainedfromsmallerandlessimportantmarkets, whileatthesametimeinformationderivedfrom
| bigger | markets | is also quite | inaccurate. |     |     |     |     |
| ------ | ------- | ------------- | ----------- | --- | --- | --- | --- |
βh
The coefficients ’s estimated by Froot and Ramadorai indicate that even over very long
zj
time horizons international inflows and exchange rate returns are positively correlated. For most
currencies the values of these coefficients are significantly larger than zero and relatively stable
| crostructure | theory. | See in particular | Easley | and | O’Hara (1987). |     |     |
| ------------ | ------- | ----------------- | ------ | --- | -------------- | --- | --- |
10

across various time horizons. On average the values of the βh ’s indicate that a $100 million dollar
zj
inflow results in a appreciation of 11.5 basis points (i.e. 0.115%) of the corresponding currency.
Thecorrelationcoefficientsbetweensignedorderflowsizeandexchangeratereturns,ρ(r (h),z (h)),
t+1,j t,j
reported by Froot and Ramadorai also present some very interesting regularities. These coefficients
take positive values with maxima reaching values ranging from 0.3 to 0.6. In addition, they tend
first to increase with the time horizon, h, between the 1-day and the 20 day horizon and then to
| decrease | as horizons | pass | beyond | 20-60 | days. |     |     |     |
| -------- | ----------- | ---- | ------ | ----- | ----- | --- | --- | --- |
Froot and Ramadorai suggest that these results do not show a stable causal relation from
international flows to exchange rates, as the impact of signed order flow size on exchange rate
returns is transitory. They conjecture that the positive correlation observed over short horizons
between order flow and exchange rate returns is not related to fundamentals but is the consequence
| of trend | chasing | activity | on the | part | of some | investors. |     |     |
| -------- | ------- | -------- | ------ | ---- | ------- | ---------- | --- | --- |
To verify their conjecture Froot and Ramadorai examine a VAR model of exchange rate returns,
fundamentals and order flow. Their VAR specification is de facto an extension of the formulation
proposedbyPayne,asitincludesinterestratedifferentialsandinflationdifferentialsalongsideorder
| flow and | exchange | rate | returns, |     |                 |        |         |               |
| -------- | -------- | ---- | -------- | --- | --------------- | ------ | ------- | ------------- |
|          |          |      |          |     |                 |        | −i∗,π   | −π∗)(cid:48). |
|          |          | x    | = Γx     | +   | (cid:178) where | x = (r | ,z ,i   |               |
|          |          | t    | t−1      |     | t               | t t+1  | t t t t | t             |
Because of the limited number of observations a unique VAR specification is estimated for all
currencies. This means that all observations are stacked together in a single series. Then, to take
account of the differences in the volume of trading across FX markets, a standardization of the
signed order flow size, z t , is employed. In fact, single currency j trades, z t,j , are normalized by
dividing all purchases/sales of assets denominated in currency j by their standard deviation for the
entire period. However, one should notice an important limitation of such a procedure, since this
normalization does not allow to capture possible differences in liquidity and information conditions
| among different |     | currencies. |     |     |     |     |     |     |
| --------------- | --- | ----------- | --- | --- | --- | --- | --- | --- |
Since Froot and Ramadorai concentrate on the short- and long-run interaction between order
flow, fundamentals and returns, the impulse-response functions associated with this VAR specifi-
cation play a paramount role in their analysis. Indeed, from these impulse-response functions it
is possible to calculate the short- and long-run covariances between order flow and returns. This
| exercise | proposes | very | interesting | results. |     |     |     |     |
| -------- | -------- | ---- | ----------- | -------- | --- | --- | --- | --- |
FrootandRamadoraifindthatthecontemporaneous covariancebetweenorderflowandexchange
rate returns is as expected larger than zero. In addition, the covariance between current order
11

flow and short-term future exchange rate returns is also positive. This indicates that order flow
positively anticipates short-term (1-month ahead) movements in exchange rates. Anyhow, over
longer horizons this anticipation effect changes sign, as the co-movement between current order
flow and long-term future exchange rate returns (more than 1-month ahead) is negative.
Froot and Ramadorai’s results also show that the covariance between short-term future cumu-
lative innovations in order flow and current exchange rate returns is positive. This indicates that
some investors employ positive feedback trading rules over short horizons. On the contrary, the
covariance between long-term future cumulative innovations in order flow and current exchange
rate returns is strongly negative. In brief, these results seem to indicate that some investors employ
positive feedback trading rules over short-term horizons, accumulating speculative positions which
they eventually unwind in the long-run. Consequently they appear to follow negative feedback
trading rules over long horizons.
Froot and Ramadorai find insignificant values for the covariance between overall exchange rate
returns (i.e. the sum of contemporaneous, short-term and long-term future exchange rate returns)
and: i) contemporaneous order flow; ii) short-term future innovations in order flow; and iii) long-
term future innovations in order flow. In synthesis, Froot and Ramadorai conclude that: i) there is
no permanent link between order flow and exchange rates; and ii) the positive impact of order flow
on exchange rate is a transitory phenomenon not necessarily related to fundamental information.
Froot and Ramadorai also analyze the short-run and long-run covariances between: i) exchange
rate returns and interest rate differentials; and ii) order flow and interest rate differentials. Their
results partially vindicates order flow. In fact, they suggest that current exchange rate returns
are positively correlated with short-term future changes in interest rates, while current order flow
is positively correlated with short-term future changes in interest rates. Thus, we can differ from
the conclusions of Froot and Ramadorai and suggest that order flow is at least related to some
short-term fundamental information.
Furthermore, it could be argued that the sort of FX transactions Froot and Ramadorai employ
refers to a specific subset of end-user transactions in FX markets and hence does not capture all
the information content of order flow. In this respect it is worth noticing that several studies,
notably Carpenter and Wang (2003), Marsh and O’Rourke (2004) and Evans and Lyons (2005a),
have explored the information content of disaggregated order flow in FX markets.
Evans and Lyons, employing daily data on the transactions of Citibank with its customers
between January 1993 and June 1999, claim that different classes of end-user transaction flows
possessadifferentexplanatorypowerforshort-termexchangeratedynamics. MarshandO’Rourke,
investigating daily data on the customer transactions of Royal Bank of Scotland between August
12

2002 and June 2004, find that the probability of informed trading is larger for financial customers.
Carpenter and Wang, using tick-by-tick data on the customer transactions of a large Austrialian
FX dealer between Mayand July 2002, conclude that financial end-user order flowpresents a larger
impact on spot rates.
These studies appear to contradict the conclusions of Froot and Ramadorai, as they indicate
that end-user order flow actually presents an information content. Though, such information con-
tent may not necessarily be linked to interest rate shifts, but rather to other macro and financial
variables, such as GDP, money supply and dividends.13
Thus, Evans and Lyons find that end-user order flow Granger causes macro variables, such as
moneygrowth,outputgrowthandinflation, atthemonthly(formoneyandinflation)andquarterly
(for output) horizon both in the US and Germany. Linear regressions of the innovation in these
macro variables over lags of the disaggregated end-user transaction flows indicate that: i) order
flow explains a substantial part of future movements in these macro variables over horizons ranging
between 1 month and two quarters; and ii) such forecasting power is stronger over the longer
horizons. Specifically, over the two-quarter horizon the coefficient of multiple correlation in these
regressions takes values in the 0.20-0.50 range.
In brief, these results suggest that order flow might anticipate future exchange rate movements.
Evans and Lyons (2005b) present compelling evidence of such forecasting power. This is based
on the comparison of short-term exchange rate forecasts obtained from several alternative linear
models against those derived from a random walk.
EvansandLyonsemploytheirCitibanktransactiondatatoderivefromseveralalternativelinear
models proper ex-ante exchange rate forecasts over horizons ranging from 1 day to 1 month. To
obtain these forecasts Evans and Lyons split their data in two sub-samples of roughly the same
length. The former, from January 1993 to February 1996, allows to estimate the parameters of the
various alternative forecasting models they consider. The latter, from March 1996 to June 1999, is
instead employed to derive the corresponding ex-ante forecasts.
Incomparing the forecasts obtained from alternativemodels, beside the traditional mean square
error(MSE)statistic,EvansandLyonsemployatestbasedontheprojection statistic. Thisstatistic
13HauandRey(2004,2005)andDunneet al. (2005)considermodelsinwhichexchangeratedynamicsislinkedto
equityreturnsandportfolioflows. Inparticular,inHauandRey’smodeldividendinnovationsconditiontheportfolio
holdingsofinternationalinvestorsandhenceaffectcapitalflowsandexchangereturns. Accordingtotheirportfoliore-
balancingeffectequityreturnsandexchangeratereturnsshouldbenegativelycorrelated,whileinternationalportfolio
flows and exchange rate returns should be positively correlated. In fact, risk-averse investors prefer to reduce their
exposure to foreign exchange risk in the face of an appreciation of a foreign equity market. Their outflow of funds
from the foreign equity market then leads to a depreciation of the corresponding foreign currency.
13

is calculated as the estimated coefficient, β , in the following linear regression
h
∆(cid:100)s = β + β (s − s ) + (cid:178) , with h = 1 day, 2 days, ..., 1 month,
t+h|t 0,h h t+h t t+h
where∆s(cid:100) indicatestheforecastoftheexchangeratevariationovertheinterval(t,t+h]obtained
t+h|t
from a specific forecasting model with data available at time t. A test of significance for the
projection statistic, β , represents a check of the forecasting power of the model, as in the case of
h
no forecastability this coefficient would not be significantly different from zero. In addition, the
magnitude of the coefficient β can be taken as a measure of the forecasting performance of the
h
model, as it estimates the contribution of the model forecasts to the variance of future exchange
rate variations.
The MSE statistic indicates that the exchange rate forecasts based on end-user order flow are
more precise than those derived from a random walk. However, the increase in the accuracy of
these forecasts appears to be significant only over the longer horizons. In contrast, the projection
statistic suggests that order flow possesses a significant forecasting power over all horizons and
that the corresponding forecasts can explain up to 16% of the variance of future exchange rate
variations. These are quite dramatic results, particularly in view of the negative conclusions drawn
from analogous studies conducted for more traditional macro-based forecasting models.
5 Heterogeneous Information, Order Flow and Exchange Rates
Bacchetta and van Wincoop (2005) have offered a possible rationale for the empirical evidence
outlined by Evans and Lyons, Payne, Froot and Ramadorai and others. Their basic idea is that in
FX markets if risk averse traders i) possess heterogeneous beliefs over exchange rate fundamentals
andii)observeimperfectlycorrelatedsignalsonfundamentals, portfolioshiftswillhaveapersistent
and large impact on exchange rates. This is due to: i) a portfolio-balance effect, when investors
need to be compensated for any extra risk they are forced to bear as a consequence of a purchase
or a sale of foreign currencies, and; ii) an information-based effect, when, in the face of the opaque
structure of FX markets, investors confuse an appreciation (depreciation) of the exchange rate due
to portfolio shifts with that induced by fundamental information.
When such confusion concerns fundamental information that becomes public in the distant
future, the impact of order flow on exchange rates is magnified by the infinite regress of investors’
individual beliefs. In fact, if investors receive private signals on fundamental variables, such as
interest rates or monetary aggregates, whose realizations are not imminent but distant in the
future, they will try to learn from prices and quantities they observe (i.e. exchange rates and order
14

flow) not only the fundamental value of foreign currencies, but also other investors’ forecasts. This
attempt to learn other investors’ forecasts exacerbates the confusion between portfolio shifts and
fundamental shocks, amplifying the impact of order flow on exchange rates.
The magnification effect is absent if private signals concern imminent shifts in fundamentals.
Thisisbecausewhenprivateinformationisshort-livedtheknowledgeofotherinvestors’forecastsis
redundantandhencetheconfusionbetweenportfolioshiftsandfundamentalshockssubdues. More
precisely, when private signals concern next period realizations of fundamental variables investors
know that very soon they will all share the same fundamental information. If they are aware that
changes to the fundamental variables to which their private signals pertain will become of public
domain in the near future, investors realize that they will not be able to exploit any information
they can extract from other investors’ forecasts and hence will not seek to learn these forecasts.
We now briefly discuss Bacchetta and van Wincoop’s market microstructure model of exchange
rate determination. First we present a simplified analytical framework which represents their basic
argument. We then discuss the properties of their model, analyzing the confusion between funda-
mental shocks and portfolio shifts and the magnification effect. Finally we present the empirical
implications of this model in the face of the empirical evidence discussed in the previous Sections.14
5.1 A Simple Structural Model
According to this simplified framework presented by Breedon and Vitale (2004) in the market for
foreign exchange a single foreign currency is traded for the currency of a large domestic economy.
TradinginthismarketisorganizedaccordingtoasequenceofWalrasianauctions. Whenanauction
is called agents simultaneously submit either market or limit orders for the foreign currency and
then a clearing price (exchange rate) is established.15
14BacchettaandvanWincoop’sisnottheuniqueattempttoformulateamarketmicrostructuremodelofexchange
rate determination. Recently, Evans and Lyons (2004) have proposed a very rich micro-founded model, which,
combines a market microstructure component, based on the analytical framework originally proposed by Lyons
(1997), with a general equilibrium set-up. However, whereas their model is more complex than the one we describe
here,itcontainssimilarfeatures,suchasheterogeneousbeliefsandinformativeorderflow,andproducesfairlysimilar
empirical implications.
15This Walrasian auction mechanism is typical of several rational expectations models of asset pricing, notably
Grossman and Stiglitz (1980) and Hellwig (1980). The mechanism we propose differs from the very popular batch
mechanism put forward by Kyle in his seminal contribution to market microstructure theory (Kyle (1985)). The
formermechanismisbettersuitedforthestructureofFXmarkets. Infact,inKyle’sformulationrisk-neutralmarket
makers enforce a semi-strong form efficiency condition for the equilibrium price. This is problematic as it is well
knownthatinFXmarketsinvestorsarerisk-averse. Inaddition, consideringrisk-neutralinvestorswouldwashaway
any portfolio-balance effects of order flow on currency values. The Walrasian auction mechanism is also consistent
with the growing share of FX transactions which is now conducted through centralized electronic limit order books,
suchastheReutersDealing2002andEBSsystems,andcapturesthelackoftransparencyofFXmarkets,inthatall
transactions are anonymous.
15

In the market for foreign exchange two classes of traders coexist: rational investors and unso-
phisticated customers. Rational investors, such as FX dealers, managers of currency funds, hedge
funds and other actively traded funds, are risk-averse agents who select optimal portfolios of do-
mestic and foreign assets. They are supposed to be short-sighted in that their investment horizon
is just one period long. This assumption is introduced for tractability but also captures a quite well
known feature of the behavior of many professional traders in FX markets, which usually attempt
day.16
to unwind their foreign exchange exposure by the end of any trading
All rational investors share the same CARA utility function of their end-of-period wealth. At
time t they can invest in three different assets: a domestic production technology, which depends
on the amount of real balances possessed, domestic bonds that pay period-by-period interest rate
i and foreign bonds that pay period-by-period interest rate i∗. Their optimal demand for foreign
| t   |     |     |     | t   |     |
| --- | --- | --- | --- | --- | --- |
bonds (foreign currency) on the part of the population of rational investors is
|     |     |     | (cid:195) |     | (cid:33) |
| --- | --- | --- | --------- | --- | -------- |
1
|     |     | d = | E¯ (s | ) − s + (i∗ | − i ) , |
| --- | --- | --- | ----- | ----------- | ------- |
|     |     | t   | t t+1 | t t         | t       |
γσ2
where s t is the log of the spot rate (i.e. the number of units of the domestic currency for one unit
E¯
of the foreign one), (s ) is the average of the conditional expectations for next period spot
t t+1
rate, s , on the part of all rational investors given the information they possess in t, σ2 is the
t+1
corresponding conditional variance and γ is their coefficient of absolute risk-aversion.
The unsophisticated customers provide all the supply of foreign currency. Thus, at time t the
total demand for foreign currency on the part all rational investors is in equilibrium equal to the
| total amount | of foreign | currency supplied | by their | clients, x , |     |
| ------------ | ---------- | ----------------- | -------- | ------------ | --- |
t
|     |     |     | d = | x . |     |
| --- | --- | --- | --- | --- | --- |
|     |     |     | t   | t   |     |
These customers comprise a population of noise and informed traders. The amount of foreign
currency these customers supply changes over time in order to meet their liquidity needs and/or
exploittheirprivateinformation. Ifo representstheamountofforeigncurrencynoiseandinformed
t
traders collectively desire to sell at time t, the total supply of foreign currency changes according
| to the following | expression |     |       |       |     |
| ---------------- | ---------- | --- | ----- | ----- | --- |
|                  |            |     | x = x | + o . |     |
|                  |            |     | t t−1 | t     |     |
Signed order flow, o t , can be decomposed in the number of units of foreign currency traded
| 16Such behavior | is documented | by Lyons (1995) | and Biønnes | and Rime | (2005). |
| --------------- | ------------- | --------------- | ----------- | -------- | ------- |
16

| respectively | by  | the | noise, | b , and | the | informed | customers, |     | I ,17 |     |     |     |     |
| ------------ | --- | --- | ------ | ------- | --- | -------- | ---------- | --- | ----- | --- | --- | --- | --- |
|              |     |     |        | t       |     |          |            |     | t     |     |     |     |     |
|              |     |     |        |         |     | o        | =          | b + | I .   |     |     |     |     |
|              |     |     |        |         |     | t        |            | t   | t     |     |     |     |     |
The population of noise customers may be interpreted as formed by the financial arms of indus-
trial corporations and by other unsophisticated financial traders, whose portfolios of foreign assets
are subject to persistent shifts. Such shifts may be associated with current account transactions or
with capital movements, such as foreign direct and portfolio investment, which are not motivated
| by current | movements |     | in  | exchange | rates. |     |     |     |     |     |     |     |     |
| ---------- | --------- | --- | --- | -------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
At time t the amount of foreign currency offered for sale by the informed traders, I , is instead
t
correlated with the innovation in a macro variable, f , which depends linearly on the interest rate
t
differential, i∗−i , and which determines the equilibrium value of the foreign currency. Whilst this
t t
fundamental variable is observable, at time t all informed traders possess some private information
(cid:178)f
on its next period innovation, . This assumption indicates that the informed traders collect
t+1
information on future shifts in interest rates before these shifts become of public domain. In order
to gain speculative profits they collectively place a market order equal to
|     |     |     |     |     |     | I   | ≡   | −θ(cid:178)f | ,   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | t   |     |              | t+1 |     |     |     |     |
where θ is a positive constant that measures the intensity of their trading activity.
Imposing equilibrium conditions for the domestic and foreign money markets and assuming that
the purchasing power condition holds, it can be established that the following “present value”
| equilibrium | condition |     | applies | to  | the       | spot rate |           |           |     |         |           |     |     |
| ----------- | --------- | --- | ------- | --- | --------- | --------- | --------- | --------- | --- | ------- | --------- | --- | --- |
|             |           |     |         |     |           | (cid:181) | (cid:182) |           |     |         |           |     |     |
|             |           |     |         |     | (cid:88)∞ |           | k         | (cid:179) |     |         | (cid:180) |     |     |
|             |           |     |         | 1   |           | α         |           | E¯k(f     |     | σ2E¯k(x |           |     |     |
|             |           | s   | =       |     |           |           |           |           | ) − | αγ      | ) ,       |     | (2) |
|             |           | t   |         |     |           |           |           | t         | t+k | t       | t+k       |     |     |
|             |           |     |         | 1+α |           | 1+α       |           |           |     |         |           |     |     |
k=0
E¯k(f
where t+k ) is the order k average rational expectation across all rational investors of period
t
|                 |     |     |           |     |        | E¯k(f |     | E¯ E¯ | ...E¯     |       |            | E¯k(x |      |
| --------------- | --- | --- | --------- | --- | ------ | ----- | --- | ----- | --------- | ----- | ---------- | ----- | ---- |
| t+k fundamental |     |     | variable, | f   | , i.e. |       | )   | =     |           | (f ). | Similarly, |       | ) is |
|                 |     |     |           | t+k |        | t     | t+k | t     | t+1 t+k−1 | t+k   |            | t     | t+k  |
theorderk averagerationalexpectationacrossallrationalinvestorsofperiodt+k supplyofforeign
| currency, | x   | .   |     |     |     |     |     |     |     |     |     |     |     |
| --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
t+k
In their simplified version of Bacchetta and van Wincoop’s model, Breedon and Vitale assume
thatallrationalinvestors: i)possesssymmetricinformation;andii)attimetcanonlyreceivesignals
over next period fundamental innovation, (cid:178)f . These two assumptions allow to circumnavigate the
t+1
17Differentlyfromtheusualconventionapositiveo indicatesanetsaleofforeigncurrency. Ifinsteado isnegative,
|     |     |     |     |     |     |     | t   |     |     |     |     | t   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
rational investors’ clients collectively place an order to purchase the foreign currency.
17

infinite regress problem Bacchetta and van Wincoop study and hence obtain simple closed form
solutionsfortheexchangerateequation(2). Inpractice,thisamountstoimposetheconditionsthat
| E¯k(f |     |     | )andE¯k(x |     |     |     |     |     |     |     |     |     |     |
| ----- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
) = E(f | Ω ) = E(x | Ω ), whereΩ correspondstotheinformationset
| t t+k |     | t+k | t   | t   | t+k | t+k | t   |     | t   |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
rational investors possess at time t. Thus, the order k average rational expectations of period t+k
fundamental variable, f , and supply of foreign currency, x , are simply equal to all rational
|            |             |     | t+k          |     |          |            |     |     | t+k |     |     |     |     |
| ---------- | ----------- | --- | ------------ | --- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
| investors’ | conditional |     | expectations |     | of these | variables. |     |     |     |     |     |     |     |
As rational investors can readily obtain from various official sources and publicly available data,
such as newswire services, newsletters, monetary authorities’ watchers and so on, information on
macro variables which condition currency values, Breedon and Vitale also assume that at time t all
rational investors observe the following common signal on the fundamental innovation
|     |     |     |     |     |     | (cid:178)f |     | (cid:178)v. |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ---------- | --- | ----------- | --- | --- | --- | --- | --- |
|     |     |     |     |     | v   | t =        | +   |             |     |     |     |     |     |
|     |     |     |     |     |     |            | t+1 | t           |     |     |     |     |     |
Alongsidethissignalallrationalinvestorscanobservetheflowoftransactionsthatarecompleted
in the market for foreign exchange. This is possible because in centralized platforms such as EBS
and Reuters Dealing 2000-2, all transactions are immediately published on the system’s computer
screens. This means that in any period t all rational investors observe the signed order flow, o t .
Then, under the assumption that the fundamental variable and the noise trading component
of order flow follows independent AR(1) processes, Breedon and Vitale (2004) show that in a
stationary equilibrium the variation in the exchange rate respects the following expression
| s     | − s              | =              | λ (s       |     | − s )  | + λ (f     | − f   | ) +        | λ    | (f    | − f ) +  | λ o | +   |
| ----- | ---------------- | -------------- | ---------- | --- | ------ | ---------- | ----- | ---------- | ---- | ----- | -------- | --- | --- |
| t     | t−1              |                | s,−1       | t−1 | t−2    | f          | t t−1 |            | f,−1 | t−1   | t−2      | x t |     |
|       |                  |                | λ o        | +   | λ (o   | − o )      | + λ   | (o         | −    | o ) + | λ (v − v | ),  | (3) |
|       |                  |                | x,−1       | t−1 | o t    | t−1        |       | o,−1       | t−1  | t−2   | v t      | t−1 |     |
| where | the coefficients |                | λ’s depend |     | on the | parameters | of    | the model. |      |       |          |     |     |
| 5.2   | Model            | Interpretation |            |     |        |            |       |            |      |       |          |     |     |
Whereas explicit formulae for the coefficients λ’s are reported in Breedon and Vitale (2004), here
we offer an economic interpretation of equation (3). We start from the coefficient λ whose sign
f
turns out to be positive. This is because an increase in the fundamental variable,f , corresponds to
t
a rise in the interest rate differential i∗−i and hence in the excess return on the foreign currency.
|     |     |     |     |     | t   | t   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
A similar result holds for the public signal, whose coefficient, λ v , is also positive.
The coefficient λ is instead negative because an increase in the supply of foreign currency
x
depresses its value via a portfolio-balance effect. Rational investors will be willing to hold a larger
18

quantity of the foreign currency only if they are compensated for the increased risk they bear.
Thus, a larger x forces a depreciation of the foreign currency, as this corresponds to a larger excess
t
return rational investors expect from holding foreign bonds.
Thecoefficientλ isnegative,becauseoftheaforementionedportfolio-balanceeffectandbecause
o
order flow possesses an information content. When some customer orders are informative (i.e. for
θ > 0)anexcessofsellordersmightindicateanimpendingnegativefundamentalinnovation((cid:178)f <
t+1
0) which induces rational investors to expect a future exchange rate depreciation. Consequently,
they will be willing to hold the same amount of the foreign currency only if a reduction in s
t
re-establishes the expected excess return foreign bonds are required to yield.
Breedon and Vitale show that |λ | > |λ |, so that the effect of order flow on exchange rates is
o o,−1
persistent. Importantly, this result holds even when customer trades do not carry any information,
i.e. when θ = 0, suggesting that the impact of portfolio shifts on exchange rates is not transitory.
Such conclusion contrasts with the generally held view that any transitory imbalance between buy
and sell orders possesses only a short-lived effect on exchange rates if order flow does not carry any
information.
5.3 Extensions and Empirical Implications
When,differentlyfromtheformulationwehavepresentedhere,rationalinvestorsobservecorrelated
but different signals of the fundamental process, the impact of order flow on exchange rates is
amplified. If any rational investor, i, observes a private signal on the fundamental innovation,
v = (cid:178)f + (cid:178)v , other things being equal, the coefficient λ in the equilibrium equation (3) is
t,i t+1 t,i x
larger, indicating that the impact of non-fundamental shocks, b , is magnified.
t
Bacchetta and van Wincoop show that the impact of these non fundamental shocks is very
large if traders possess long-lived private information. This is the case if at time t either informed
customers observe period t+T fundamental innovation, (cid:178)f (with T > 1), or rational investors
t+T
observe private signals on the same shock, v = (cid:178)f +(cid:178)v . In both cases it is not possible to
t,i t+T t,i
impose the simplifying assumption that E¯k(f ) = E (f ) and E¯k(x ) = E (x ) and as a
t t+k t t+k t t+k t t+k
consequence the impact of non fundamental shocks, b , on exchange rates is greatly magnified.
t
The empirical implications of Bacchetta and van Wincoop’s model are very interesting. In
particular, the fundamental shock, (cid:178)f , presents a persistent effect on the value of the foreign
t+T
currency. However, its initial impact is smaller than its total effect. In fact, when a positive
innovation hits the fundamental variable, (cid:178)f > 0, because of the rational confusion between noise
t+T
trading and fundamental shifts, rational investors need several observations of the exchange rate
19

to realize the extension of this innovation.
BacchettaandvanWincoopshowthatunderheterogeneousinformation: i)orderflowvariability
accounts for a large share of exchange rate volatility over the short-run; ii) the amount of exchange
rate volatility explained by fundamental variables augments over time; and iii) the exchange rate
is a good predictor of future changes in fundamentals over short horizons.18
6 News, Order Flow and Exchange Rates
In the previous Sections we have seen that at least over the short-run order flow and exchange rates
are strongly correlated. Via Bacchetta and van Wincoop’s analytical framework we have seen that
order flow can affect exchange rates through either a portfolio-balance effect, as investors need to
be compensated for the risk they bear when they hold foreign currencies, or an information effect,
if order flow conveys information on fundamental shifts which affect the value of currencies. In the
second scenario order flow is related to news arrivals, i.e. to information on macro variables which
FX traders obtain from various sources.
The analysis of the effects of news arrivals on spot rates dates back to the debate over the
exchange rate disconnect puzzle stimulated in the early 1980s by Meese and Rogoff’s influential
work. Since then researchers have tried to verify whether macro variables influence exchange rates,
studying the effects of macro announcements on exchange rates. Earlier contributions (Hardouvelis
(1985), Ito and Roley (1987)), that concentrated on the analysis of daily data, have reaffirmed the
role of fundamentals, showing that news arrivals on variables such as output, price levels, etc., do
affect exchange rates. Recently researchers (Goodhart (1992), Andersen et al. (2003)) have studied
the effects of news arrivals at high frequencies, also trying to explore the relation between news and
order flow (Evans and Lyons (2003), Love and Payne (2003)).
Data on macro variables are continuously released by official and unofficial sources. According
totheefficientmarketsparadigmpricesreflectall availableinformation,sothatonlytheunexpected
component of these macro announcements should affect exchange rates. Thus, let A represent a
k,t
macro announcement variable. This is equal to the announced value of a macro indicatork, such as
US GDP or German unemployment level, in the interval (t,t+1] in which a public announcement
is released and zero in any other interval. Let E indicate the corresponding value expected by
k,t
market participants at time t. According to the efficient markets paradigm only the unexpected
component, A −E , of the announcement variable should influence exchange rates.
k,t k,t
18As already mentioned, Evans and Lyons (2002,2005a,2005b), Payne (2003) and others offer some evidence in
favor of the first two empirical implications. Engel and West (2005) provides some empirical support in favor of the
predicting power of exchange rates with respect to future changes in fundamentals.
20

Andersenetal.(2003)havestudiedtheeffectsonsixmajorexchangerates(USD/CHF,USD/DEM,
EUR/USD, GBP/USD and USD/JPY) of the unexpected components of announcements on 41
macro variables for the United States and Germany over the period between January 1992 and De-
cember1998,employingReutersdataonexchangeratereturns,r ,observedat5-minute intervals
t+1
and MMS data on money managers’ expectations of the 41 macro variables, E .
k,t
For any indicator, k, a standardized news variable is defined as follows
|     |     |     |     | A k,t − E | k,t |     |     |
| --- | --- | --- | --- | --------- | --- | --- | --- |
|     |     |     | N   | ≡         | ,   |     |     |
k,t
|     |     |     |     | σ k |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
where σ is the sample standard deviation of the news variable N . The effect of these news
| k   |     |     |     |     | k,t |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
variables on exchange rates is evaluated estimating a linear regression of the 5-minute return, r ,
t+1
on its own lags and on the contemporaneous and lagged values of the news variables N ’s,
k,t
|     |     |     | (cid:88)p | (cid:88)K |           |               |     |
| --- | --- | --- | --------- | --------- | --------- | ------------- | --- |
|     |     | r = | α +       | α r +     | θ N       | + (cid:178) . | (4) |
|     |     | t+1 | 0         | i t+1−i   | k,j k,t−j | t             |     |
|     |     |     | i=1       | k=1       |           |               |     |
Andersen et al. find that both for US and German indicators the unexpected components of the
macro announcements significantly affect exchange rates. Moreover, exchange rates react quickly
to news shocks, with an immediate jump and very little movement thereafter. For example, a
one standard deviation US payroll employment shock, N e,t = 1, appreciates the US dollar against
the German currency by 0.16%. Adding the announcement indicators, A ’s, to the linear model
k,t
(4) Andersen et al. find that the expected components of the macro announcements do not affect
| exchange | rates. |     |     |     |     |     |     |
| -------- | ------ | --- | --- | --- | --- | --- | --- |
Most of the econometric fit in equation (4) comes from the lagged values of the dependent
variable and the contemporaneous news variables, N ’s. This suggests that most of the effect of
k,t
the news variables N on the spot rate is felt within a 5-minute interval. Indeed, considering only
k,t
the intervals of time for which some news is released (this amounts to a sub-sample of less than
0.2% of all observations), Anderson et al. find that the news variables present a strong explanatory
| power. This | is documented | by  | the following | linear regression |               |     |     |
| ----------- | ------------- | --- | ------------- | ----------------- | ------------- | --- | --- |
|             |               | r   | = θ N         | + (cid:178) , for | k = 1,...,41, |     | (5) |
|             |               | t+1 | k             | k,t t             |               |     |     |
where the sample is restricted to the intervals, (t,t+1], in which an announcement on the macro
variable k is observed. While the coefficients of multiple correlations are very small for all currency
pairsinthecaseofequation(4),inthe41estimationsofequation(5),whereonlytheeventwindows
thecoefficientofmultiplecorrelation,R2,oftentakesvaluesaround0.3andattimes
areconsidered,
21

approaches 0.6.
Love and Payne (2003) extend the analysis of the effects of news arrivals on exchange rates by
studying the interplay between order flow, spot rates and macro news. More precisely, they study:
i) the effect of news arrivals on exchange rates and order flow separately; ii) the impact of order
flow on exchange rates around announcement dates; and iii) the effect of news arrivals and order
flow on exchange rates simultaneously.
They employ transaction data which consist of all spot inter-dealer trades completed via the
Reuters Dealing 2000-2 system in the EUR/USD, EUR/GBP and GBP/USD markets over several
months in 1999 and 2000. Exchange rate returns are sampled at the 1-minute frequency, so that
severalthousandsobservationsareavailableforthethreespotrates. Onlythedirection ofindividual
trades is available, whilst no information on their size is accessible. We have already seen that this
lack of information is inconsequential for the study of the effects of order flow on spot rates.
Their news data consist of announcements on several macro indicators for the three listed eco-
nomic areas, alongside the corresponding market expectations collected by Standard and Poors.
Sinceveryfewannouncementsperanymacroindicatorareavailable,foranyeconomicareaaunique
macro news variable is obtained consolidating the data for the individual indicators. This is done
in two stages: firstly, in the economic area C the news variable for the individual indicator k is
standardized via the familiar formulation, NC ≡ (AC −EC )/σ ; secondly, this standardized
k,t k,t k,t k,C
news variable is signed according to its effect on the value of the currency of the area.
To give a sign to the news variable NC a simple linear regression of the return for currency
k,t
C, rC , on the news variable NC is estimated via OLS over the entire sample period. If the
t+1 k,t
coefficientofthislinearregressionispositive(negative), positiveunexpectedshocksintheindicator
k appreciate (depreciate) currency C. The news variable NC is then signed by pre-multiplying
k,t
its value by the sign of this linear coefficient. Hence, for any economic area C a single news
variable is obtained by aggregating (i.e. summing together) thesigned standardized news variables,
(cid:80)
NC = K sign(NC )NC .
t k=1 k,t k,t
As a preliminary analysis, Payne and Love study the impact of news arrivals on exchange rates
and order flow separately. Returns and order flow are regressed on leads and lags of macro news
variables. Conclusions of this exercise are that: i) even at this very high frequency (1-minute) news
arrivals affect exchange rates; and ii) surprisingly, news arrivals also affect order flow, with both
immediate and delayed effects.
Love and Payne also examine the possibility that news arrivals alter the impact of order flow on
exchange rates. Thus, their analysis shows that around periods of news arrivals exchange rates are
22

more sensitive to order flow than during calmer times. Contemporaneously to the release of US
(UK) news, order flow presents a significantly larger impact on the value of the US dollar (British
pound). Finally, in order to test whether exchange rate response to news arrivals is mediated by
order flow, the two authors estimate a simple bivariate VAR model for each spot rate,
|     | (cid:34) | (cid:35) | (cid:34) | (cid:35) | (cid:34) | (cid:35) |           | (cid:34) |       | (cid:35)  |       |                   |
| --- | -------- | -------- | -------- | -------- | -------- | -------- | --------- | -------- | ----- | --------- | ----- | ----------------- |
|     | rC       |          |          |          |          |          | (cid:88)p |          | rC    | (cid:88)q |       |                   |
|     |          |          |          | α r      | β        |          |           |          |       |           |       |                   |
|     |          | t+1      | =        |          | +        | zC       | +         | Γ        | t+1−i | +         | Θ N   | + (cid:178) , (6) |
|     |          | zC       |          |          |          | t        |           | i        | zC    |           | j t−j | t                 |
|     |          |          |          | α        | 0        |          |           |          |       |           |       |                   |
|     |          | t        |          | z        |          |          | i=1       |          | t−i   | j=1       |       |                   |
where zC indicates order flow moving funds into currency C in the interval (t,t + 1], i.e. the
t
difference between the number of buy and sell orders for currency C, while N is the vector of the
t
news variables in the three economic areas, N ≡ (NEU,NUK,NUS)(cid:48).
|     |     |     |     |     |     |     | t   | t   | t   | t   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
As in Payne (2003) this specification is identified assuming that while the contemporaneous
value of the order flow variable, zC, enters into the return equation the opposite is not true.
t
This identification restriction is justified by the 1-minute frequency at which the variables are
observed. As already mentioned, over such short periods of time a causal link from returns to flows
is improbable.
Results from the estimation of this VAR specification indicate that, as seen elsewhere, the order
zC’s,
flow variables, possess a large and highly significant positive impact on exchange rates. A net
t
purchase of euros in the EUR/USD and EUR/GBP markets brings about a rise in the value of the
euro. Similarly, a net purchase of US dollars in the EUR/USD and GBP/USD markets produces a
| rise | in the | value of | the American |     | currency. |     |     |     |     |     |     |     |
| ---- | ------ | -------- | ------------ | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
News arrivals also have a significant impact on exchange rates and order flow. A positive
news shock in the euro area (NEU > 0) appreciates the euro against the US dollar and generates
t
positive order flow from the United States and the United Kingdom. Likewise, a positive value
NUS
for appreciates the US dollar against the euro and the British pound and generates positive
t
order flow from Euro-land and the United Kingdom. Interestingly, news arrivals in one area also
condition the performance of the market between the other two currencies. A positive news shock
(NUS
in the US > 0) brings about an outflow from Euro-land toward the United Kingdom and a
t
| corresponding |     | depreciation |     | of  | the euro | against | the | British | pound. |     |     |     |
| ------------- | --- | ------------ | --- | --- | -------- | ------- | --- | ------- | ------ | --- | --- | --- |
Since news arrivals provoke order flow and this on its turn moves exchange rates, news shocks
condition the values of currencies both via a direct channel, as exchange rates immediately adjust
after an informative shock, and via an indirect channel, as exchange rates react to imbalances
| between | buy | and | sell orders. |     |     |     |     |     |     |     |     |     |
| ------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Studying the impulse response functions of the VAR model Love and Payne are able to separate
23

these two components of the impact of news shocks on exchange rates. Calculating the cumulative
return generated by a positive news shock in area C under the restriction that order flow is not
affected by news, i.e. by introducing zeros in the second row of all the matrices of coefficients Θ
j
in equation (6), Love and Payne isolate the direct component. Subtracting the direct component
from the cumulative return generated by a positive news shock in area C under no restriction they
pin down the indirect component.
Results of this decomposition show that, according to the currency pairs examined, between 30
and 60 percent of the simultaneous impact of news shocks on exchange rates is mediated by order
flow. Love and Payne conclude that nearly 50% of public information simultaneously released to
all market participants is impounded into exchange rates via order flow. This implies that efficient
markets paradigm, according to which public information should be immediately transferred into
prices with no role for trading, is violated.
AdifficultywiththeanalysisofLoveandPayneisthattheirmethodologyispronetoacircularity
issue. In fact, the direction of news is defined on the basis of the effect of macro announcements on
exchangerates. NC ispositively(negatively)signedifanunexpectedpositivemacroannouncement
k,t
(AC > 0) augments (reduces) the value of currency C. The effect of news arrivals on the first
k,t
moment of order flow and exchange rates is then investigated. Since Love and Payne use the same
sample of observations to sign the variables NC and to study their effects on exchange rates, their
k,t
results are biased in favor of a positive effect of news arrivals on returns.
The contradictory results of the empirical analysis of traditional models of exchange rate de-
termination make it hard to sign news. For example, an unexpected rise in the growth rate of
monetary aggregates in one country can lead either to a depreciation of the domestic currency, if
this process brings about inflation and devaluation expectations, or to its appreciation, if, in the
presence of a central bank reaction function, nominal interest rates are set to rise. In other words,
any empirical study of the effects of news on exchange rates and order flow is plagued by the issue
of the indeterminacy of the direction of news.
In the face of these difficulties one could just concentrate on the effects of news arrivals on the
second moments of exchange rates and order flow. That is the route followed by Evans and Lyons
(2003). In their study they employ data on all bilateral transactions between FX dealers via the
Reuters Dealing 2000-1 system in the spot USD/DEM and USD/JPY markets between May 1st
and August 31st 1996 and data on macro announcements for US and German indicators derived
from Reuters’ newswire services. From these sources they construct daily observations for signed
order flow, z , the exchange rate variation, ∆s , and the number of news releases, A .
t t+1 t
Evans and Lyons study the effects of news arrivals on the volatility of exchange rates and of
24

order flow, considering the following simple linear model of exchange rate determination
|       | ∆s         | = αz +  | N + (cid:178) , | where   |       |
| ----- | ---------- | ------- | --------------- | ------- | ----- |
|       | t+1        | 1,t     | C,t t           |         |       |
| z = z | + z , with | z = γ∆s | , and           | z = N   | + η . |
| t     | 1,t 2,t    | 2,t     | t+1             | 1,t P,t | t     |
Here order flow can be both informative, z , and induced by exchange rate movements, z , as
1,t 2,t
consequence of feedback trading. Moreover, exchange rate movements can be the consequence of
public information, N C,t , or of private information contained in order flow, N P,t .
NoticethatEvansandLyonsproposeadifferentroleforpublicinformationfromthatadvocated
by Love and Payne, in that they suggest that public information does not affect order flow and it
is immediately incorporated in currency values. Only the private component of information alters
exchange rates via order flow. Their notion of private information is also different from the usual
one, as FX traders do not share a common model of exchange rate determination and give different
interpretations to macro announcements. Hence, a general consensus on the implications of an
unexpected shock to a macro variable can be obtained only via trading. Thus, N C,t refers to the
common knowledge component of news while N subsumes all the rest.
P,t
Evans and Lyons do not attempt to identify N and N . Rather, they simply assume that
C,t P,t
|     | σ2  | σ2  |     |     |     |
| --- | --- | --- | --- | --- | --- |
the corresponding variances, and , are increasing in the pace of news arrivals,
|     | C,t | P,t          |          |     |     |
| --- | --- | ------------ | -------- | --- | --- |
|     | σ2  |              | σ2       |     |     |
|     |     | = σ C ·A t , | = σ P ·A | t . |     |
|     | C   |              | P        |     |     |
UsingGMMestimatorstheyfindthatnewsarrivalssignificantlyincreasethevolumeoftrading. The
arrival of news also augments the volatility of exchange rates via both a (direct) public information
channel and an (indirect) order flow one. In line with the results of Love and Payne, Evans and
Lyons calculate that roughly 70% of daily exchange rate variance due to news arrivals is via order
flow and 30% is via the direct effect. In addition, they find that exchange rate movements have a
negative feedback effect on order flow. Note that this clearly contradicts the thesis of Froot and
Ramadorai on the short-term trend chasing activity of some FX traders.
We now turn to the intervention activity of central banks in FX markets, as this is an important
component of order flow.
25

7 Central Bank Intervention in Foreign Exchange Markets
Central banks routinely buy and sell currencies in spot FX markets with the intention of condi-
tioning currency values. We denote this trading activity as foreign exchange (FX) intervention.19
However, notice that we intend sterilized FX intervention, in that when central banks buy and
sell currencies, the consequent change in the money supply is usually offset through an immediate
open market operation. In effect, FX intervention represents an independent instrument of policy-
making as long as it does not change the money supply, since otherwise it would be a different and
less convenient way of implementing the monetary policy.
FX intervention may alter currency values via the portfolio-balance effect, for it modifies the
ratio between domestic and foreign assets held by the private sector. A purchase (sale) of foreign
currencies by the central bank, which reduces (augments) the ratio between domestic and foreign
assets held by the private sector, induces a depreciation (appreciation) of the national currency, in
that investors require a greater risk-premium to hold a larger quantity of this currency.
Early studies, such as Frankel (1982), Frankel and Engle (1984), Jurgensen (1983), Loopesko
(1984), Neumann(1984)andRogoff(1984), indicatedthatFXinterventionhadaverysmall, ifany,
effect on exchange rates, suggesting that either domestic and foreign assets are perfect substitutes
or that the effect of FX intervention on risk-premia is minuscule. Other studies based on more
recent and accurate data, notably Dominguez and Frankel (1993a) and Gosh (1992), concluded
that FX intervention presents a significant short-term impact on exchange rates and influences
risk-premia.
An alternative channel through which FX intervention may alter exchange rates has been pop-
ularized by Mussa (1981). According to his signalling hypothesis, operations in FX markets by
a central bank may signal changes in future monetary policy. As a consequence, FX intervention
affects market expectations on currency fundamentals and hence exchange rates. In other words,
order flow in FX markets “carries” fundamental information and condition exchange rates. This is
because some informed agents, central banks, trade on their superior information and consequently
alter currency values.
Several studies, such as Dominguez and Frankel (1993b,1993c), Klein and Rosengren (1991),
Dominguez (1992), Watanabe (1992), Lewis (1993), Kaminsky and Lewis (1996) and Catte et al.
(1994), have attempted to assess the signalling role of FX intervention. Their conclusions support
Mussa’s hypothesis, as they conclude that FX intervention is related to the monetary policy and
19Here we present the bulk of the empirical research on FX intervention. For a more detailed coverage of this
strand of research see the the surveys of Edison (1993) and Sarno and Taylor (2001).
26

that it conditions investors’ expectations.
All cited authors in their studies have considered either daily or monthly observations of FX in-
tervention. PayneandVitale(2003)insteademploytransactiondataontheinterventionoperations
of the Swiss National Bank (SNB) and conduct an event study of the effects of FX intervention
on exchange rates at high frequency.20 Their data-set consists of all customer and intervention
operations, time-stamped to the minute, conducted by the SNB in the USD/CHF market and are
recorded for the period covering 1986 to 1995.21 The data-set also contains tick-by-tick indicative
exchange rate quotes on the USD/CHF rate over the same period.
Payne and Vitale consider simple linear regressions of the 15 minute percentage return, r , on
t+1
the USD/CHF rate on leads and lags of a signed intervention operation indicator, I , and a signed
t
customer operation indicator, C ,
t
(cid:88)−8
r = α + β I + γ r + γ r + (cid:178) ,
t+1 j t+j 1 t 2 t−1 t
j=8
(cid:88)−8
r = α + β C + γ r + γ r + (cid:178) .
t+1 j t+j 1 t 2 t−1 t
j=8
HereI (C )is+1inany15minuteintervalwheretheSNBpurchaseddollars,withinanintervention
t t
(customer) operation, -1 in intervals when the SNB sold dollars and zero otherwise.
PayneandVitale’sresultsindicatethatinterventionshaveasignificant impactonexchangerate
levels. Onthecontrary,customertradesdonotalterexchangerates,asatnopointisthecumulative
effect of a customer trade on the USD/CHF rate significantly different from zero. These results
suggest that the exchange rate reaction to the SNB intervention activity is not the consequence of
the portfolio-balance effect. Rather, it is evidence that intervention operations carry information.
As a further check of the signalling hypothesis, Payne and Vitale assess the relevance of the size
of intervention in the relationship between intervention size and the USD/CHF return, inserting
among the regressors of the percentage return, r , leads and lags of the signed intervention
t+1
quantity, z .
t
Results for this regression show that the size of the intervention operation is important. In
fact, the coefficient on contemporaneous intervention is significantly positive, so that the larger the
magnitude of intervention, the larger its immediate impact on the exchange rate. More precisely,
20Dominguez(2003) hasalsoofferedahighfrequencystudyofFXintervention. However,shedoesnothaveaccess
to actual transaction data and makes use of newswire reports of central bank activity in FX markets.
21The distinction between customer and intervention operations is crucial: whilst the former are triggered by the
need of the Swiss government for foreign currency, the latter are aimed at influencing the value of the Swiss franc.
27

the estimated impact on the exchange rate of an intervention purchase of $50 million by the SNB
(nearly 30 basis points) is very large. This impact is an order of magnitude larger than the lower
bound estimated by Evans and Lyons (2000) for the impact of central bank intervention in the
USD/DEM market (5 basis points for operations of $100 million).
To investigate the persistence of these effects Payne and Vitale also examine the results from
regressions of temporally aggregated exchange rate return data on aggregated intervention activity.
These regressions indicate that the effect of SNB intervention operations is significant, even though
the quantitative impact of these operations falls with the time horizon. In brief, at least over
the short-run, the signalling hypothesis seems confirmed. Intervention operations in FX markets
represent an expensive instrument of policymaking. Because of their potential cost, they can be
employed by monetary authorities to credibly convey information to market participants and hence
condition market sentiment and currency values. Moreover, since large operations are potentially
more expensive they have a bigger impact on exchange rate returns than small ones.
Concluding Remarks
Like a guide presenting a collection of paintings in a gallery we have offered a tour of the recent
market microstructure approach to exchange rate determination. Thus, in lieu of a complete
overview of a large and growing body of research, we have tried to isolate its most important and
innovative contributions, focusing our attention on some key studies.
Market microstructure studies of exchange rate determination report widespread evidence that
signed order flow is strongly positively correlated with short-term exchange rate movements. Even
when taking into account possible feedback effects from exchange rates to trade innovations, order
flow presents a significant explanatory power for short-term exchange rate dynamics.
This explanatory power can be associated with two different channels of transmission, due
respectively to portfolio-balance and information effects. How important these two channels of
transmission are remains an open question. Some researchers suggest that the contemporaneous
correlation observed between order flow and exchange rate variations is not the consequence of a
stable causal link from order flow to exchange rates, but rather the effect of the transitory impact
of portfolio shifts. Others instead claim that order flow presents an information content, as it
anticipates innovations in some fundamental variables and future movements in exchange rates.
In our opinion, a pressing challenge for this strand of research is represented by the estimation
of a proper market microstructure model of exchange rate determination. This model should deal
28

with the issue of simultaneity in the determination of exchange rates and order flow, while disen-
tangling the portfolio-balance and information effects of the latter on the former. The estimation
of such a model would shed further light on the dispute over the portfolio-balance and information
effects of order flow on exchange rates and help dissipating the general skepticism that the mar-
ket microstructure approach to exchange rate determination has met among several international
finance scholars.
An even more important challenge pertains to the forecasting power of order flow. In fact, the
existing evidence put forward in its favor mostly concerns end-user transaction flows and is limited
to few studies based on one or two data-sets. It can be argued that the forecasting power of order
flow should be corroborated by more complementary studies. In addition, it is worth noticing
that end-user transactions amount to proprietary order flow, which cannot be widely observed and
whose potential forecasting power would in any case be of minimal practical use. In the end, more
work is required before it can be legitimately argued that an answer to the elusive quest for valid
exchange rate forecasts has been found.
References
Andersen,T.,T.Bollerslev,F.Diebold,andC.Vega,2003,MicroEffectsofMacroAnnouncements:
Real-Time Price Discovery in Foreign Exchange, American Economic Review, 93, 38–62.
Bacchetta, P., and E. van Wincoop, 2005, Can Information Heterogeneity Explain the Exchange
Rate Determination Puzzle?, American Economic Review, forthcoming.
Backus, D., 1984, Empirical Models of the Exchange Rate: Separating the Wheat from the Chaff,
Canadian Journal of Economics, pp. 824–846.
Bagehot, W., 1971, The Only Game in Town, Financial Analyst Journal, 27, 29–34.
Berger, D. W., A. P. Chaboud, S. V. Chernenko, E. Howorka, R. S. Krishnasami Iyer, D. Liu, and
J. H. Wright, 2005, Order Flow and Exchange Rate Dynamics in Electronic Brokerage System
Data, mimeo, Federal Reserve Board.
Biønnes, G. H., and D. Rime, 2001, Customer Trading and Information in Foreign Exchange
Markets, mimeo, Norwegian School of Management.
, 2005, Dealer Behavior and Trading Systems in Foreign Exchange Markets, Journal of
Financial Economics, 75, 571–605.
BIS, 2001, Triennal Central Bank Survey: Foreign Exchange and Derivatives Market Activity in
2001. Bank of International Settlement, Basel.
29

, 2004, Triennal Central Bank Survey: Foreign Exchange and Derivatives Market Activity
| in 2004. | Bank of | International |     | Settlement, |     | Basel. |     |     |
| -------- | ------- | ------------- | --- | ----------- | --- | ------ | --- | --- |
Breedon, F., andP.Vitale, 2004, AnEmpiricalStudyofLiquidityandInformationEffectsofOrder
| Flow on | Exchange | Rates, |     | CEPR | Discussion | Paper | 4586, | London. |
| ------- | -------- | ------ | --- | ---- | ---------- | ----- | ----- | ------- |
Carpenter,A.,andJ.Wang,2003,SourcesofPrivateInformationinFXTrading,mimeo,University
| of New South | Wales. |     |     |     |     |     |     |     |
| ------------ | ------ | --- | --- | --- | --- | --- | --- | --- |
Catte, P., G. Galli, and S. Rebecchini, 1994, “Concerted Interventions and the Dollar: An Analysis
of Daily Data”. In P.B. Kenen, F. Papadia and F. Saccomanni: The International Monetary
| System, | CUP, Cambridge. |     |     |     |     |     |     |     |
| ------- | --------------- | --- | --- | --- | --- | --- | --- | --- |
Danielsson, J., and R. Love, 2004, Feedback Trading, mimeo, London School of Economics.
Danielsson, J., R. Payne, and J. Luo, 2002, Exchange Rate Determination and InterMarket Order
| Flow Effects, | mimeo, |     | London | School | of  | Economics. |     |     |
| ------------- | ------ | --- | ------ | ------ | --- | ---------- | --- | --- |
Dominguez, K. M., 1992, Exchange Rate Efficiency and the Behavior of International Asset Mar-
| kets. Garland, | New | York, |     | NY. |     |     |     |     |
| -------------- | --- | ----- | --- | --- | --- | --- | --- | --- |
, 2003, The Market Microstructure of Central Bank Intervention, Journal of International
| Economics, | 59, | 25–45. |     |     |     |     |     |     |
| ---------- | --- | ------ | --- | --- | --- | --- | --- | --- |
Dominguez, K. M., and J. A. Frankel, 1993a, Does Foreign Exchange Intervention Matter? The
| Portfolio | Effect, | American |     | Economic | Review, |     | 83, 1356–1369. |     |
| --------- | ------- | -------- | --- | -------- | ------- | --- | -------------- | --- |
, 1993b, Does Foreign Exchange Intervention Work? Institute for International Economics,
| Washington, | DC. |     |     |     |     |     |     |     |
| ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
, 1993c, “Foreign Exchange Intervention: An Empirical Assessment”. In J.A. Frankel: On
| Exchange | Rates, | Mit | Press, | Cambridge, |     | MA. |     |     |
| -------- | ------ | --- | ------ | ---------- | --- | --- | --- | --- |
Dunne, P., H. Hau, and M. Moore, 2005, International Order Flow: Explaining Equity and Ex-
| change Rate | Returns, |     | mimeo. |     |     |     |     |     |
| ----------- | -------- | --- | ------ | --- | --- | --- | --- | --- |
Easley, D., and M. O’Hara, 1987, Price, Trade Size, and Information in Securities Markets, Journal
| of Financial | Economics, |     | 19, | 69–90. |     |     |     |     |
| ------------ | ---------- | --- | --- | ------ | --- | --- | --- | --- |
Edison, H. J., 1993, The Effectiveness of Central-Bank Intervention: A Survey of the Literature
| After 1982, | Special | paper |     | 18, Princeton |     | University. |     |     |
| ----------- | ------- | ----- | --- | ------------- | --- | ----------- | --- | --- |
Engel, C., and K. D. West, 2005, ExchangeRates and Fundamentals, Journal of PoliticalEconomy,
113, 485–517.
30

Evans, M. D., and R. K. Lyons, 2000, The Price Impact of Currency Trades: Implications for
| Intervention, | Mimeo, | University |     | of California | at  | Berkeley. |
| ------------- | ------ | ---------- | --- | ------------- | --- | --------- |
, 2002, Order Flow and Exchange Rates Dynamics, Journal of Political Economy, 110,
170–180.
, 2003, How Is Macro News Transmitted to Exchange Rates?, NBER Working Paper 9433.
, 2004, A New Micro Model of Exchange Rate Dynamics, NBER Working Paper 10379.
, 2005a, Exchange Rate Fundamentals and Order Flow, NBER Working Paper 11042.
,2005b,Meese-RogoffRedux: Micro-BasedExchangeRateForecasting,AmericanEconomic
| Review, Papers | and | Proceedings, |     | forthcoming. |     |     |
| -------------- | --- | ------------ | --- | ------------ | --- | --- |
Frankel,J.A.,1982,InSearchoftheExchangeRateRiskPremium: ASixCurrencyTestAssuming
Mean-Variance Optimization, Journal of International Money and Finance, 1, 255–276.
| , 1993, | On Exchange |     | Rates. | The | MIT Press, | Boston. |
| ------- | ----------- | --- | ------ | --- | ---------- | ------- |
Frankel, J. A., and C. M. Engel, 1984, Do Asset Demand Functions Optimize Over the Mean
and Variance of Real Returns? A Six Currency Test, Journal of International Economics, 17,
209–223.
Frankel, J. A., and A. K. Rose, 1994, A Survey of Empirical Research on Nominal Exchange Rates,
| NBER Working | Paper |     | 4865. |     |     |     |
| ------------ | ----- | --- | ----- | --- | --- | --- |
Froot, K., and T. Ramadorai, 2005, Currency Returns, Intrinsic Value, and Institutional Investor
| Flows, Journal | of  | Finance, | 60, | 1535–1566. |     |     |
| -------------- | --- | -------- | --- | ---------- | --- | --- |
Glosten, L., and P. Milgrom, 1985, Bid, Ask and Transaction Prices in a Specialist Market with
Heterogeneously Informed Traders, Journal of Financial Economics, 13, 71–100.
Goodhart, C.A.E., 1992, NewsEffectsinaHigh-FrequencyModeloftheSterling-DollarExchange
| Rate, Journal | of  | Applied | Econometrics, |     | 7.  |     |
| ------------- | --- | ------- | ------------- | --- | --- | --- |
Gosh,A.,1992,IsitSignaling? ExchangeInterventionandtheDollar-DeutscheMarkRate,Journal
| of International | Economics, |     | 32, | 201–220. |     |     |
| ---------------- | ---------- | --- | --- | -------- | --- | --- |
Grossman, S., and J. Stiglitz, 1980, On the Impossibility of Informationally Efficient Markets,
| American | Economic | Review, |     | 70, 393–408. |     |     |
| -------- | -------- | ------- | --- | ------------ | --- | --- |
Hardouvelis, G. A., 1985, Exchange Rates, Interest Rates, and Money-Stock Announcements: A
Theoretical Exposition, Journal of International Money and Finance, 4, 443–454.
31

Hasbrouck, J., 1991, Measuring the Information Content of Stock Trades, Journal of Finance, 46,
178–208.
Hau, H., W. Killen, and M. Moore, 2002, How Has the Euro Changed the Foreign Exchange
| Market?, | Economic | Policy, |     | 17, 149–192. |     |     |
| -------- | -------- | ------- | --- | ------------ | --- | --- |
Hau, H., and H. Rey, 2004, Can Portfolio Rebalancing Explain the Dynamics of Equity Returns,
Equity Flows and Exchange Rates?, American Economic Review, Papers and Proceedings, 93,
126–133.
, 2005, Exchange Rates, Equity Prices and Capital Flows, Review of Financial Studies,
forthcoming.
Hellwig,M.,1980,OntheAggregationofInformationinCompetitiveMarkets,JournalofEconomic
| Theory, 22, | 477–498. |     |     |     |     |     |
| ----------- | -------- | --- | --- | --- | --- | --- |
Ito, T., and V. V. Roley, 1987, News from the U.S. and Japan: Which Moves the Yen/Dollar
| Exchange | Rate?, | Journal | of  | Monetary | Economics, | 19, 255–277. |
| -------- | ------ | ------- | --- | -------- | ---------- | ------------ |
Jurgensen, P., 1983, Report of the Working Group on Exchange Market Intervention. Department
| of Treasury, | Washington |     | D.C. |     |     |     |
| ------------ | ---------- | --- | ---- | --- | --- | --- |
Killen, W., R. Lyons, and M. Moore, 2005, Fixed Versus Floating: Lessons From the EMS Order
| Flow, Journal | of  | International |     | Money and | Finance, | forthcoming. |
| ------------- | --- | ------------- | --- | --------- | -------- | ------------ |
Klein, M., and E. Rosengren, 1991, Foreign Exchange Intervention as a Signal of Monetary Policy,
| New England | Economic |     | Review, | May/June, | 39–50. |     |
| ----------- | -------- | --- | ------- | --------- | ------ | --- |
Kyle, A. S., 1985, Continuous Auction and Insider Trading, Econometrica, 53(6), 1315–1335.
Lewis, K. K., 1993, Are Foreign Exchange Intervention and Monetary Policy Related and Does it
| Really Matter?, |     | NBER | Working | Paper | 4377. |     |
| --------------- | --- | ---- | ------- | ----- | ----- | --- |
Loopesko, B., 1984, Relationships Among Exchange Rates, Interventions, and Interest Rates: An
Empirical Investigation, Journal of International Money and Finance, 3, 257–277.
Love, R., and R. Payne, 2003, Macroeconomic News, Order Flow and Exchange Rates, mimeo,
| London School | of  | Economics. |     |     |     |     |
| ------------- | --- | ---------- | --- | --- | --- | --- |
Lyons, R. K., 1995, Tests of Microstructural Hypotheses in the Foreign Exchange Market, Journal
| of Financial | Economics, |     | 39, | 321–351. |     |     |
| ------------ | ---------- | --- | --- | -------- | --- | --- |
, 1997, A Simultaneous Trade Model of the Foreign Exchange Hot Potato, Journal of
| International | Economics, |     | pp. | 275–298. |     |     |
| ------------- | ---------- | --- | --- | -------- | --- | --- |
32

, 2001, The Microstructure Approach to Exchange Rates. The MIT Press, Boston.
Madhavan, A., 2000, Market Microstructure: A Survey, Journal of Financial Markets, 3, 205–258.
Mark, N. C., 1995, Exchange Rates and Fundamentals: Evidence on Long-Horizon Predictability,
| American | Economic | Economic, | 85, | 201–218. |     |     |     |
| -------- | -------- | --------- | --- | -------- | --- | --- | --- |
Marsh, I. W., and C. O’Rourke, 2004, Customer Order Flow and Exchange Rate Movements: Is
| There Really | Information |     | Content”, | Cass | Business | School | mimeo. |
| ------------ | ----------- | --- | --------- | ---- | -------- | ------ | ------ |
McDonald,R.R.,andM.P.Taylor,1993,TheMonetaryApproachtotheExchangeRate: Rational
Expectations,Long-RunEquilibriumandForecasting,InternationalMonetaryFundStaffPapers,
40, 89–107.
Meese, R., and K. Rogoff, 1983, Empirical Exchange Rate Models of the Seventies: Do They Fit
| Out of | the Sample?, | Journal | of International |     | Economics, |     | 13, 3–24. |
| ------ | ------------ | ------- | ---------------- | --- | ---------- | --- | --------- |
Mussa, M., 1981, The Role of Official Intervention. Group of Thirty, New York, NY.
Neumann, M., 1984, Intervention in the Mark/Dollar Market: The Authorities’ Reaction, Journal
| of International | Money | and | Finance, | 3, 223–239. |     |     |     |
| ---------------- | ----- | --- | -------- | ----------- | --- | --- | --- |
O’Hara, M., 1995, Market Microstructure Theory. Blackwell, Oxford.
Payne, R., 2003, Informed Trade in Spot Foreign Exchange Markets: An Empirical Investigation,
| Journal | of International |     | Economics, | 61, 307–329. |     |     |     |
| ------- | ---------------- | --- | ---------- | ------------ | --- | --- | --- |
Payne, R., and P. Vitale, 2003, A Transaction Level Study of the Effects of Central Bank Interven-
tion on Exchange Rates, Journal of International Economics, 61, 331–352.
Rime,D.,2003,“NewElectronicTradingSystemsinForeignExchangeMarkets”.In: NewEconomy
| Handbook, | Elsevier | Science, | USA. |     |     |     |     |
| --------- | -------- | -------- | ---- | --- | --- | --- | --- |
Rogoff, K., 1984, On the Effect of Sterilized Intervention: An Analysis of Weekly Data, Journal of
| Monetary | Economics, | 14, | 133–150. |     |     |     |     |
| -------- | ---------- | --- | -------- | --- | --- | --- | --- |
Sarno, L., and M. P. Taylor, 2001, Official Intervention in the Foreign Exchange Market: Is It
Effective and, If So, How Does It Work?, Journal of Economic Literature, 39, 839–868.
Watanabe, T., 1992, The Signaling Effect of Foreign Exchange Intervention: The Case of Japan,
| Bank of | Japan, mimeo. |     |     |     |     |     |     |
| ------- | ------------- | --- | --- | --- | --- | --- | --- |
33

Table 1: Synthesis of empirical studies of FX market microstructure.
| Study | Data | Spot Rates | Main Results |     |     |
| ----- | ---- | ---------- | ------------ | --- | --- |
Andersen et al. (2003) Reuters FXFX EUR/USD, USD/DEM News announcements have a large
03/01/92 - 30/12/98 USD/JPY, GBP/USD and immediate impact on spot rates.
|     | 5-minute obs. | USD/CHF | News releases | generates | R2 5-40% on |
| --- | ------------- | ------- | ------------- | --------- | ----------- |
|     |               |         | announcement  | periods’  | returns.    |
Berger et al. (2005) Reuters D2000-2 EUR/USD, USD/JPY Order flow generates R2 30-50%
|     | 01/01/99 - 29/02/04 |     | for intra-daily | and daily      | returns. |
| --- | ------------------- | --- | --------------- | -------------- | -------- |
|     | 1-minute obs.       |     | Order flow      | Granger causes | returns  |
|     |                     |     | at 1-minute     | frequency.     |          |
Biønnes and Rime (2005) Four Scandinavian USD/DEM, DEM/CHF Order flow and spot rates are
dealers’ trades USD/NOK, DEM/NOK cointegrated. 50/80% of spreads
02/03/98- 06/03/98 DEM/SEK, DEM/DKK explained by private information.
|     | tick-by-tick | obs. | Half-lives    | of dealers’ inventories |          |
| --- | ------------ | ---- | ------------- | ----------------------- | -------- |
|     |              |      | range between | 1 and 15                | minutes. |
Carpenter and Wang (2003) Australian dealer’s EUR/USD, USD/AUS Order flow generates R2 10-24%
|     | trades              |      | on tick-by-tick | rates. Financial    |     |
| --- | ------------------- | ---- | --------------- | ------------------- | --- |
|     | 01/05/02 - 03/07/02 |      | end-user        | order flow presents | a   |
|     | tick-by-tick        | obs. | significantly   | larger impact       | on  |
returns.
Danielsson and Love (2004) Reuters D2000-2 EUR/USD, GBP/USD Contemporaneous feedback trading
01/12/99 - 24/07/00 EUR/GBP is significant at high frequencies.
|     | 1- and 5-minute | obs. | IRF of trade | imbalance       | more than |
| --- | --------------- | ---- | ------------ | --------------- | --------- |
|     |                 |      | twice with   | contemporaneous |           |
feedback trading.
Danielsson et al. (2002) Reuters D2000-2 EUR/USD, USD/JPY Order flow generates R2 10-50%
28/09/99 - 24/07/00 GBP/USD, EUR/GBP on intra-daily rates. In-sample
|     | 5-minute obs. |     | forecasts  | of spot rates | based on     |
| --- | ------------- | --- | ---------- | ------------- | ------------ |
|     |               |     | order flow | outperform    | those of the |
random walk.
R2
Evans and Lyons (2002) Reuters D2000-1 USD/DEM, USD/JPY Order flow generates 40-60%
|     | 01/05/96 - 31/08/96 |     | on daily  | rates. $1 billion | trade |
| --- | ------------------- | --- | --------- | ----------------- | ----- |
|     | daily obs.          |     | imbalance | increases USD/DEM |       |
by 0.5%.
Evans and Lyons (2003) Reuters D2000-1 USD/DEM News releases increase order flow
|     | 01/05/96 - 31/08/96 |     | and exchange    | rate volatility  | at daily      |
| --- | ------------------- | --- | --------------- | ---------------- | ------------- |
|     | 5-minute obs.       |     | and intra-daily | frequency.       | The           |
|     |                     |     | impact          | of news releases | on spot rates |
|     |                     |     | via order       | flow is 2/3 of   | the total.    |
Evans and Lyons (2005a) Citibank dealer’s EUR/USD Customer order flow forecasts future
|     | customer trades     |     | macro variables | over horizons      | ranging    |
| --- | ------------------- | --- | --------------- | ------------------ | ---------- |
|     | 01/01/93 - 30/06/99 |     | from 1 month    | to 2 quarters.     | Different  |
|     | daily obs.          |     | explanatory     | power of different | end-       |
|     |                     |     | user order      | flows for daily    | to monthly |
returns.
Evans and Lyons (2005b) Citibank dealer’s EUR/USD Micro-based out-of-sample forecasting
|     | customer trades     |     | models          | out-perform traditional | macro        |
| --- | ------------------- | --- | --------------- | ----------------------- | ------------ |
|     | 01/01/93 - 30/06/99 |     | models          | and the random          | walk. Micro- |
|     | daily obs.          |     | based forecasts | explain                 | 16% of       |
|     |                     |     | monthly         | exchange rate           | volatility.  |

Table 1: Synthesis of empirical studies of FX market microstructure. (cont.ed)
| Study |     | Data | Spot Rates |     | Main Results |     |     |
| ----- | --- | ---- | ---------- | --- | ------------ | --- | --- |
Froot and Ramadorai (2005) State Street Co 111 rates from 19 International portfolio flows are
int. portfolio flows countries strongly positively correlated with
|     |     | 01/01/94   | - 09/02/99 |     | contemporaneous | returns. | No long- |
| --- | --- | ---------- | ---------- | --- | --------------- | -------- | -------- |
|     |     | daily obs. |            |     | run co-movement | between  | flows    |
and spot rates.
R2
Hau et al. (2002) EBS USD/DEM, EUR/USD Pooled order flow generates
|     |     | 01/01/98 | - 31/12/99 USD/JPY, | USD/CHF | 36% on | pooled monthly | rates. |
| --- | --- | -------- | ------------------- | ------- | ------ | -------------- | ------ |
monthly obs. JPY/DEM, EUR/JPY Impact of order flow on spot rates
|     |     |     | DEM/CHF, | EUR/CHF | is larger | in the post-euro | period. |
| --- | --- | --- | -------- | ------- | --------- | ---------------- | ------- |
Killen et al. (2005) EBS DEM/FF Cumulate order flow and spot rate
|     |     | 01/01/98   | - 31/12/98 |     | cointegraed | over flexible      | regime |
| --- | --- | ---------- | ---------- | --- | ----------- | ------------------ | ------ |
|     |     | daily obs. |            |     | period.     | DEM1 billion trade |        |
|     |     |            |            |     | imbalance   | increases DEM/FF   | by     |
3 pips.
Love and Payne (2003) Reuters D2000-2 EUR/USD, GBP/USD Impact of order flow on spot rates
|     |     | 28/09/99 | - 24/07/00 EUR/GBP |     | doubles   | around news releases. |           |
| --- | --- | -------- | ------------------ | --- | --------- | --------------------- | --------- |
|     |     | 1-minute | obs.               |     | Over half | of the impact         | on spot   |
|     |     |          |                    |     | rates of  | news releases is      | via order |
flow.
Lyons (1995) NY bank dealer’s USD/DEM Trade innovations have strong
|     |     | and broker’s | trades     |     | information     | and inventory-control |           |
| --- | --- | ------------ | ---------- | --- | --------------- | --------------------- | --------- |
|     |     | 03/08/92     | - 07/08/92 |     | effects.        | $10 million trade     | imba-     |
|     |     | tick-by-tick | obs.       |     | lance increases | USD/DEM               | by 1 pip. |
Marsh and O’Rourke (2004) RBS customer trades EUR/USD, USD/JPY Customer order flow generates
R2
|     |     | 01/08/02   | - 29/06/04 GBP/USD, | EUR/JPY | 5-27%     | on daily rates.     |     |
| --- | --- | ---------- | ------------------- | ------- | --------- | ------------------- | --- |
|     |     | daily obs. | EUR/GBP,            | GBP/JPY | Financial | order flow presents |     |
larger PINs.
Payne (2003) Reuters D2000-2 USD/DEM 60% of spreads explained by
|     |     | 06/10/97     | - 10/10/97 |     | private information. | 40%       | of spot |
| --- | --- | ------------ | ---------- | --- | -------------------- | --------- | ------- |
|     |     | tick-by-tick | obs.       |     | rate variability     | is due to | trade   |
imbalance.
Notes: 1 pip corresponds to the fourth digit employed to quote exchange rates. IRF stands for impulse-response function.
| PIN stands | for probability | of information | trading. |     |     |     |     |
| ---------- | --------------- | -------------- | -------- | --- | --- | --- | --- |
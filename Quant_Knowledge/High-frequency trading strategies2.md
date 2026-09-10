High-frequency trading strategies
Michael Goldstein, Babson College
Amy Kwan, University of Sydney
Richard Philip, University of Sydney
THE UNIVERSITY OF SYDNEY
BUSINESS SCHOOL
7th Emerging Markets Conference
15th December 2016

Is HFT beneficial to market quality?
“The U.S. stock market was now a class system, rooted in
speed, of haves and have-nots. The haves paid for
nanoseconds; the have-nots had no idea that nanoseconds
had value. The haves enjoyed a perfect view of the market;
the have-nots never saw the market at all.”
(Michael Lewis, Flash Boys)
› “there are also HFT firms who believe that 350 microseconds is critical to what
they do, as they look to pick up trading signals so that they can race ahead and
pick off trades from regular investors.” (Brad Katsuyama, CEO of IEX)
› The Senate Banking Committee has “expressed concerns about increased market
speed, complexity, and potential market fragility as a result of increased automated
trading.” (Congressional Research Service Report, 2016)
2

Is HFT beneficial to market quality?
› Earlier academic evidence is almost always supportive:
- “AT improves liquidity and enhances the informativeness of quotes.”
(Hendershott, Jones and Menkveld, 2011)
- “greater AT intensity improves liquidity and informational efficiency” (Boehmer,
Fong and Wu, 2012)
- “increased low-latency activity improves traditional market quality measures—
decreasing spreads, increasing displayed depth in the limit order book, and
lowering short-term volatility” (Hasbrouck and Saar, 2013)
- “Overall HFTs facilitate price efficiency” (Brogaard, Hendershott and Riordan,
2014)
- “Increasing the speed of market-making participants benefits market liquidity”
(Brogaard, Hagstromer, Norden and Riordan, 2015)
3

Is HFT beneficial to market quality?
› But then…
- “I find evidence consistent with HFTs being able to anticipate order flow from
other investors.” (Hirschey, 2013)
- “Because speed is a source of market power, it enables fast traders to extract
rents from other market participants and triggers a costly arms race that reduces
social welfare” (Hoffmann, 2014)
- “trades are followed by limit order cancellations on competing venues” (van
Kervel, 2015)
- “Reductions in latency exacerbate quote-fade and latency arbitrage” (Malinova
and Park, 2016)
- Van Kervel and Menkveld (2016) and Korajczyk and Murphy (2016) find that
HFTs initially trade ‘against the wind’ but eventually trade ‘with the wind’ as the
large trade progresses.
4

Objectives and motivations
› Much is known about the effects of HFT, the literature is unclear on how
HFTs trade to influence financial markets.
- i.e., what are the information channels that drive HFT behavior?
› Most of the existing evidence is based on executed trades. The order
submission behaviour and strategies of HFTs is not well understood.
› We examine HFT trading strategies directly by reconstructing the shape of
the limit order book at the time of order submissions, cancellations and
amendments.
› Related studies:
- Malinova and Park (2016): Study HFT order submission behaviour in a multi-
market setting
- Subrahmanyam and Zheng (2016): examine HFT limit order placements on
Nasdaq and find that HFT have a stabilizing influence on markets.
5

Main findings
1. All traders trade with the order book imbalance but HFT do it better.
2. HFT supply liquidity to the thick side of the order book (where it is not
required) and demand liquidity from the thin side of the order book
(where it is most needed).
- Consistent with order anticipation strategies
3. HFT cancel limit orders that are at high risk of being picked off.
4. After the introduction of ITCH (a faster data feed) on the ASX, HFT
become even more strategic.
5. By competing with non-HFT, HFT crowd out non-HFT limit orders from
the order book.
6

Data and sample
› Full order book and trade data for stocks in the S&P/ASX 100 index from
AusEquities (provided by SIRCA)
- Data contains stock symbol, date and time of order entry, order size and price,
identifier for submitting broker (proprietary HFT firms, institutions, retail)
- Each order has a unique identifier such that subsequent
amendments/executions/cancellation can be traced to the original submitted
order
› We examine the period January 1, 2012 to December 31, 2012
- ITCH introduced on April 2, 2012 (more later)
7

Data and sample
8

Strategic trading
9

Depth Imbalance and volume imbalance
› We capture the shape of the order book using depth imbalance (DI) at the
time of each order book event (i.e., submission, trade, amendment or
cancelation):
| ∑(cid:3041) (cid:1848)(cid:1867)(cid:1864)(cid:1828)(cid:1861)(cid:1856) | (cid:3398) ∑(cid:3041)                               | (cid:1848)(cid:1867)(cid:1864)(cid:1827)(cid:1871)(cid:1863) |                       |
| ------------------------------------------------------------------------ | ---------------------------------------------------- | ------------------------------------------------------------ | --------------------- |
| (cid:3036)(cid:2880)(cid:2869)                                           | (cid:3036),(cid:3047) (cid:3036)(cid:2880)(cid:2869) |                                                              | (cid:3036),(cid:3047) |
(cid:1830)(cid:1835) (cid:3404)
| (cid:3047) ∑(cid:3041)                                       | ∑(cid:3041)                                          |                                                              |                       |
| ------------------------------------------------------------ | ---------------------------------------------------- | ------------------------------------------------------------ | --------------------- |
| (cid:1848)(cid:1867)(cid:1864)(cid:1828)(cid:1861)(cid:1856) | (cid:3397)                                           | (cid:1848)(cid:1867)(cid:1864)(cid:1827)(cid:1871)(cid:1863) |                       |
| (cid:3036)(cid:2880)(cid:2869)                               | (cid:3036),(cid:3047) (cid:3036)(cid:2880)(cid:2869) |                                                              | (cid:3036),(cid:3047) |
› We expect:
1. A positive relationship between DI and future stock returns.
2. A strategic trader to buy when DI is high and sell when DI is low.
10

Depth imbalance, returns and trading volumes
|     | Panel A: Returns |     |     | Panel B: Volumes |     |     |     |
| --- | ---------------- | --- | --- | ---------------- | --- | --- | --- |
2
6.
1
55.
)pb( snruteR
)%( emuloV
0
5.
1-
54.
2-
4.
3-
| 0 1 2                              | 3 4 5               | 6 7 8 | 9   | 0 1 2                        | 3 4 5               | 6 7 8 | 9   |
| ---------------------------------- | ------------------- | ----- | --- | ---------------------------- | ------------------- | ----- | --- |
| Directional depth imbalance decile |                     |       |     | Directional imbalance decile |                     |       |     |
|                                    | (9 = most positive) |       |     |                              | (9 = most positive) |       |     |
11

Depth imbalance and trading volumes by broker
|     | Panel A: HFT |     |     | Panel B: Institutions |     |     |     |
| --- | ------------ | --- | --- | --------------------- | --- | --- | --- |
41
54
21
| )%( emuloV |     |     | )%( emuloV |     |     |     |     |
| ---------- | --- | --- | ---------- | --- | --- | --- | --- |
| 01         |     |     |            | 04  |     |     |     |
8
53
6
4
03
| 0 1 2                              | 3 4 5               | 6 7 8 | 9   | 0 1                                | 2 3 4 5             | 6 7 8 | 9   |
| ---------------------------------- | ------------------- | ----- | --- | ---------------------------------- | ------------------- | ----- | --- |
| Directional depth imbalance decile |                     |       |     | Directional depth imbalance decile |                     |       |     |
|                                    | (9 = most positive) |       |     |                                    | (9 = most positive) |       |     |
|                                    | Panel C: Retail     |       |     | Panel D: Volume imbalance          |                     |       |     |
)%( ecnalabmi emuloV
5
05
)%( emuloV
5.4
0
| 4   |     |     |     | 05- |         |       |     |
| --- | --- | --- | --- | --- | ------- | ----- | --- |
| 5.3 |     |     |     | 0 1 | 2 3 4 5 | 6 7 8 | 9   |
Directional depth imbalance decile
| 0 1 2 | 3 4 5 | 6 7 8 | 9   |     | (9 = most positive) |     |     |
| ----- | ----- | ----- | --- | --- | ------------------- | --- | --- |
Directional depth imbalance decile
|     |     |     |     | HFT | Institutions | Retail |     |
| --- | --- | --- | --- | --- | ------------ | ------ | --- |
(9 = most positive)
12

Depth imbalance and volume imbalances
(cid:1828)(cid:1873)(cid:1877) (cid:1874)(cid:1867)(cid:1864)(cid:1873)(cid:1865)(cid:1857) (cid:3398) (cid:1845)(cid:1857)(cid:1864)(cid:1864) (cid:1874)(cid:1867)(cid:1864)(cid:1873)(cid:1865)(cid:1857)
(cid:3038) (cid:3038)
(cid:1848)(cid:1867)(cid:1864)(cid:1873)(cid:1865)(cid:1857) (cid:1861)(cid:1865)(cid:1854)(cid:1853)(cid:1864)(cid:1853)(cid:1866)(cid:1855)(cid:1857) % (cid:3404)
(cid:3038)
(cid:1828)(cid:1873)(cid:1877) (cid:1874)(cid:1867)(cid:1864)(cid:1873)(cid:1865)(cid:1857) (cid:3397) (cid:1845)(cid:1857)(cid:1864)(cid:1864) (cid:1874)(cid:1867)(cid:1864)(cid:1873)(cid:1865)(cid:1857)
(cid:3038) (cid:3038)
13

Depth imbalance and volume imbalances
14

Depth imbalance and volume imbalances
(cid:3003)(cid:3048)(cid:3052) (cid:3049)(cid:3042)(cid:3039)(cid:3048)(cid:3040)(cid:3032) (cid:2879)(cid:3020)(cid:3032)(cid:3039)(cid:3039) (cid:3049)(cid:3042)(cid:3039)(cid:3048)(cid:3040)(cid:3032)
Dependent variable: (cid:1848)(cid:1867)(cid:1864)(cid:1873)(cid:1865)(cid:1857) (cid:1861)(cid:1865)(cid:1854)(cid:1853)(cid:1864)(cid:1853)(cid:1866)(cid:1855)(cid:1857) % (cid:3404) (cid:3286) (cid:3286)
(cid:3038)
(cid:3003)(cid:3048)(cid:3052) (cid:3049)(cid:3042)(cid:3039)(cid:3048)(cid:3040)(cid:3032) (cid:2878)(cid:3020)(cid:3032)(cid:3039)(cid:3039) (cid:3049)(cid:3042)(cid:3039)(cid:3048)(cid:3040)(cid:3032)
(cid:3286) (cid:3286)
15

Order placement strategies
| ∑(cid:3041)                                                  | ∑(cid:3041)                               |                                                              |            |
| ------------------------------------------------------------ | ----------------------------------------- | ------------------------------------------------------------ | ---------- |
| (cid:1848)(cid:1867)(cid:1864)(cid:1828)(cid:1861)(cid:1856) | (cid:3398)                                | (cid:1848)(cid:1867)(cid:1864)(cid:1827)(cid:1871)(cid:1863) |            |
| (cid:3036)(cid:2880)(cid:2869)                               | (cid:3047) (cid:3036)(cid:2880)(cid:2869) |                                                              | (cid:3047) |
(cid:1827)(cid:1856)(cid:1862)(cid:1873)(cid:1871)(cid:1872)(cid:1857)(cid:1856)	(cid:1830)(cid:1835) (cid:3404) (cid:1869)	 (cid:3400)
| ∑(cid:3041) (cid:1848)(cid:1867)(cid:1864)(cid:1828)(cid:1861)(cid:1856) | (cid:3397) ∑(cid:3041)                    | (cid:1848)(cid:1867)(cid:1864)(cid:1827)(cid:1871)(cid:1863) |            |
| ------------------------------------------------------------------------ | ----------------------------------------- | ------------------------------------------------------------ | ---------- |
| (cid:3036)(cid:2880)(cid:2869)                                           | (cid:3047) (cid:3036)(cid:2880)(cid:2869) |                                                              | (cid:3047) |
16

Order placement strategies
17

Volatility and trading volumes by broker
|     | Panel A: HFT |     |     | Panel B: Institutions |     |     |     |
| --- | ------------ | --- | --- | --------------------- | --- | --- | --- |
09
41
21
| )%(emuloV |     |     | )%(emuloV | 58  |     |     |     |
| --------- | --- | --- | --------- | --- | --- | --- | --- |
01
08
8
| 6                                     |       |       |     | 57                                    |       |       |     |
| ------------------------------------- | ----- | ----- | --- | ------------------------------------- | ----- | ----- | --- |
| 0 1 2                                 | 3 4 5 | 6 7 8 | 9   | 0 1 2                                 | 3 4 5 | 6 7 8 | 9   |
| Volatility decile (9 = most volatile) |       |       |     | Volatility decile (9 = most volatile) |       |       |     |
Panel C: Retail
11
01
)%(emuloV
9
8
7
6
| 0 1 2 | 3 4 5 | 6 7 8 | 9   |     |     |     |     |
| ----- | ----- | ----- | --- | --- | --- | --- | --- |
Volatility decile (9 = most volatile)
18

Volatility and trading volumes by broker
19

Volatility and depth imbalance by broker
| Panel A: Aggressive trades |     |     |     | Panel B: Passive trades |     |     |     |
| -------------------------- | --- | --- | --- | ----------------------- | --- | --- | --- |
51.
2.
| 51.                        |     |     |                            | 1.  |     |     |     |
| -------------------------- | --- | --- | -------------------------- | --- | --- | --- | --- |
| )slevel 5( ecnalabmi htpeD |     |     | )slevel 5( ecnalabmi htpeD |     |     |     |     |
50.
1.
50.
0
50.-
0
| 0 1 2                                 | 3 4 5        | 6 7 8  | 9   | 0 1 2                                 | 3 4 5        | 6 7 8  | 9   |
| ------------------------------------- | ------------ | ------ | --- | ------------------------------------- | ------------ | ------ | --- |
| Volatility decile (9 = most volatile) |              |        |     | Volatility decile (9 = most volatile) |              |        |     |
| HFT                                   | Institutions | Retail |     | HFT                                   | Institutions | Retail |     |
20

Volatility and depth imbalance
Dependent variable: Adjusted depth imbalance
21

What happens when trading speeds increase?
› ASX ITCH: designed to meet the requirements of speed sensitive traders
and increased market information access speeds by up to 7 times existing
connections.
- Implemented on April 2, 2012
- Pre period: March 2, 2012 to April 1, 2012
- Post-period: April 9, 2012 to May 9, 2012
- This event creates benefits for HFT participants, who are the most speed
sensitive.
22

HFT strategies and trading speeds
23

Do HFT crowd out the limit order book?
› As HFTs become faster, we expect the probability of fill for non-HFT limit
orders to decrease.
- i.e., it becomes more difficult for non-HFT traders to receive executions for their
limit orders.
› Examine only limit orders submitted to the best bid or ask:
∑(cid:1846)(cid:1870)(cid:1853)(cid:1856)(cid:1857)(cid:1848)(cid:1867)(cid:1864)(cid:1873)(cid:1865)(cid:1857)
(cid:1842)(cid:4666)(cid:1858)(cid:1861)(cid:1864)(cid:1864)(cid:4667) (cid:3404)
∑(cid:1845)(cid:1873)(cid:1854)(cid:1865)(cid:1861)(cid:1872)(cid:1848)(cid:1867)(cid:1864)(cid:1873)(cid:1865)(cid:1857)
24

Probability of fill and trading speeds
25

Conclusion
› HFT trade on information contained in the limit order book. Our findings
provide an explanation for how HFT:
i. Predict future order flow
ii. Increases stock volatility
› HFT supply liquidity to the thick side of the order book (where it is not
required) and demand liquidity from the thin side of the order book (where
it is most needed). This trading behaviour exacerbates future order book
imbalances.
› HFT become more strategic with faster trading speeds. However, HFT
strategies come at the cost of crowding out non-HFT limit orders from the
order book.
26
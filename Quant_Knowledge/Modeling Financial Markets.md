Team-LRN

7700++ DDVVDD’’ss FFOORR SSAALLEE && EEXXCCHHAANNGGEE
wwwwww..ttrraaddeerrss--ssooffttwwaarree..ccoomm
wwwwww..ffoorreexx--wwaarreezz..ccoomm
wwwwww..ttrraaddiinngg--ssooffttwwaarree--ccoolllleeccttiioonn..ccoomm
wwwwww..ttrraaddeessttaattiioonn--ddoowwnnllooaadd--ffrreeee..ccoomm
CCoonnttaaccttss
aannddrreeyybbbbrrvv@@ggmmaaiill..ccoomm
aannddrreeyybbbbrrvv@@yyaannddeexx..rruu
SSkkyyppee:: aannddrreeyybbbbrrvv

������������
Want to learn more?
We hope you enjoy this
McGraw-Hill eBook! If
you’d like more information about this book,
its author, or related books and websites,
please click here.
Team-LRN

| MODELING  |     | FINANCIAL |     |     |
| --------- | --- | --------- | --- | --- |
MARKETS
| Using  Visual     | Basic.NET  |           |     | and  Databases |
| ----------------- | ---------- | --------- | --- | -------------- |
| to  Create        | Pricing,   | Trading,  |     | and            |
| Risk  Management  |            | Models    |     |                |
| BENJAMIN          | VAN VLIET  |           |     |                |
ROBERTHENDRY
McGraw-Hill
| NewYork          | Chicago SanFrancisco |     | Lisbon |     |
| ---------------- | -------------------- | --- | ------ | --- |
| London Madrid    | MexicoCity           |     | Milan  |     |
| NewDelhi         | SanJuan Seoul        |     |        |     |
| Singapore Sydney | Toronto              |     |        |     |
Team-LRN

Copyright © 2004 by The McGraw-Hill Companies, Inc. All rights reserved. Manufactured in
the United States of America. Except as permitted under the United States Copyright Act
of 1976, no part of this publication may be reproduced or distributed in any form or by
any means, or stored in a database or retrieval system, without the prior written
permission of the publisher.
0-07-144288-X
The material in this eBook also appears in the print version of this title: 0-07-141772-9
All trademarks are trademarks of their respective owners. Rather than put a trademark
symbol after every occurrence of a trademarked name, we use names in an editorial
fashion only, and to the benefit of the trademark owner, with no intention of
infringement of the trademark. Where such designations appear in this book, they have
been printed with initial caps.
McGraw-Hill eBooks are available at special quantity discounts to use as premiums and
sales promotions, or for use in corporate training programs. For more information, please
contact George Hoare, Special Sales, at george_hoare@mcgraw-hill.com or (212) 904-
4069.
TERMS OF USE
This is a copyrighted work and The McGraw-Hill Companies, Inc. (“McGraw-Hill”) and
its licensors reserve all rights in and to the work. Use of this work is subject to these
terms. Except as permitted under the Copyright Act of 1976 and the right to store and
retrieve one copy of the work, you may not decompile, disassemble, reverse engineer,
reproduce, modify, create derivative works based upon, transmit, distribute, disseminate,
sell, publish or sublicense the work or any part of it without McGraw-Hill’s prior
consent. You may use the work for your own noncommercial and personal use; any other
use of the work is strictly prohibited. Your right to use the work may be terminated if
you fail to comply with these terms.
THE WORK IS PROVIDED “AS IS.” McGRAW-HILL AND ITS LICENSORS
MAKE NO GUARANTEES OR WARRANTIES AS TO THE ACCURACY,
ADEQUACY OR COMPLETENESS OF OR RESULTS TO BE OBTAINED FROM
USING THE WORK, INCLUDING ANY INFORMATION THAT CAN BE
ACCESSED THROUGH THE WORK VIA HYPERLINK OR OTHERWISE, AND
EXPRESSLY DISCLAIM ANY WARRANTY, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES OF
MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. McGraw-Hill
and its licensors do not warrant or guarantee that the functions contained in the work will
meet your requirements or that its operation will be uninterrupted or error free. Neither
McGraw-Hill nor its licensors shall be liable to you or anyone else for any inaccuracy,
error or omission, regardless of cause, in the work or for any damages resulting
therefrom. McGraw-Hill has no responsibility for the content of any information
accessed through the work. Under no circumstances shall McGraw-Hill and/or its
licensors be liable for any indirect, incidental, special, punitive, consequential or similar
damages that result from the use of or inability to use the work, even if any of them has
been advised of the possibility of such damages. This limitation of liability shall apply to
any claim or cause whatsoever whether such claim or cause arises in contract, tort or
otherwise.
DOI: 10.1036/007144288X
Team-LRN

For more information about this title, click here.
| C O N           | T   | E N T S |     |     |     |     |
| --------------- | --- | ------- | --- | --- | --- | --- |
| Acknowledgments |     | v       |     |     |     |     |
SECTIONONE
| Trading        | System | Development |     | 1   |     |     |
| -------------- | ------ | ----------- | --- | --- | --- | --- |
| 1 Introduction |        | 3           |     |     |     |     |
| 2 Development  |        | Methodology |     |     | 11  |     |
SECTIONTWO
| Introduction |       | to VB.NET:   | Algorithm |     | Development | 31  |
| ------------ | ----- | ------------ | --------- | --- | ----------- | --- |
| 3 Getting    |       | Started with | VB.NET    |     | 33          |     |
| 4 Value      | Types | and          | Operators | 47  |             |     |
| 5 Control    |       | Structures   | 65        |     |             |     |
| 6 Procedures |       | 81           |           |     |             |     |
| 7 Objects    |       | 109          |           |     |             |     |
| 8 Arrays     |       | 133          |           |     |             |     |
| 9 Problem    |       | Solving      | 151       |     |             |     |
| 10 .NET      | Type  | System       | 171       |     |             |     |
SECTIONTHREE
| Database        | Programming: |                 | Back       | Testing | 185 |     |
| --------------- | ------------ | --------------- | ---------- | ------- | --- | --- |
| 11 Relational   |              | Databases       | 187        |         |     |     |
| 12 ADO.NET      |              | 201             |            |         |     |     |
| 13 Structured   |              | Query           | Language   |         | 219 |     |
| 14 Introduction |              | to Data         | Structures |         | 243 |     |
| 15 Advanced     |              | Data Structures |            | 257     |     |     |
iii
Team-LRN

iv Contents
SECTIONFOUR
| Advanced      | VB.NET:   |              | Implementation   |                  | 269 |     |     |
| ------------- | --------- | ------------ | ---------------- | ---------------- | --- | --- | --- |
| 16 Software   |           | Connectivity | and              | Interoperability |     |     | 271 |
| 17 Connecting |           | to           | Trading Software |                  | 281 |     |     |
| 18 XML        | 301       |              |                  |                  |     |     |     |
| 19 XML        | Protocols |              | in Financial     | Markets          |     | 323 |     |
SECTIONFIVE
| Object-Oriented |     | Programming: |           | Risk | Management |     | 341 |
| --------------- | --- | ------------ | --------- | ---- | ---------- | --- | --- |
| 20 Unified      |     | Modeling     | Lanaguage |      | 343        |     |     |
| References      |     | 379          |           |      |            |     |     |
| Acronyms        |     | 383          |           |      |            |     |     |
| Index           | 385 |              |           |      |            |     |     |
Team-LRN

| A C K  | N O      | W L        | E D G | M E       | N T S |            |     |       |
| ------ | -------- | ---------- | ----- | --------- | ----- | ---------- | --- | ----- |
| Andrew | Kumiega, | Nithiphong |       | Vikitset, | Anton | Karadakov, |     | David |
Norman,KeithBlack,PamelaReardon,AlexDeitz,MelanieWinter,
| Siriporn         | Treetanasawat, |                                          | Mulianto |      | The,      | Debbie   | Cernauskas, |         |
| ---------------- | -------------- | ---------------------------------------- | -------- | ---- | --------- | -------- | ----------- | ------- |
| Michael          | Modica,        | Jerold                                   | Lavin,   |      | Duana     | Wooters, | Thomas      | E.      |
| “Burma”Shea,     |                | SagyMintz,KennethM.Horjus,MarkMcCracken, |          |      |           |          |             |         |
| Julia Spaulding, |                | Dave                                     | Kuipers, | Rich | Pombonyo, |          | Paresh      | Akbari, |
Cliff Ensing, Brain Huyser, Mark Groenenboom, Bruce Rawlings,
Gary Lahey, Hank Perrit, Jack Wing, Varsha Pitre, Michael Ubis,
| Jason Malkin, |     | and Irma | Baines. |     |     |     |     |     |
| ------------- | --- | -------- | ------- | --- | --- | --- | --- | --- |
v
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

This page intentionally left blank.
Team-LRN

| S E C   | T I O | N O    | N E |     |     |
| ------- | ----- | ------ | --- | --- | --- |
| Trading |       | System |     |     |     |
Development
| I projectthat,[inthe |     | next | ten years], | themajority | ofmoney |
| -------------------- | --- | ---- | ----------- | ----------- | ------- |
managers will completelyautomate their trade entry decisions....
| So, in thevery | near         | future,if | you havea | mousein | yourhand, |
| -------------- | ------------ | --------- | --------- | ------- | --------- |
| you will       | be too late. |           |           |         |           |
Blair Hull
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

This page intentionally left blank.
Team-LRN

| C   | H A | P T E | R   | 1   |     |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
Introduction
A
lthoughthisbookfollowsthelayoutofaprogrammingbook,the
underlying theme is financial modeling and quantitative trading
system development. In a sense, this book really marries four
disciplines—computer science, quantitative finance, trading strat-
egy,andqualitydevelopment—intoone,financialengineering.The
| following | chapter, |     | Chapter | 2,  | outlines | the | Kumiega–Van |     | Vliet |
| --------- | -------- | --- | ------- | --- | -------- | --- | ----------- | --- | ----- |
Trading System Development Methodology, which as you will see
provides the underlying structure for the rest of the book. As the
chapters progress, we present gradually more complex program-
ming ideas along with mathematics and trading applications to
illustratethestepsalongtheKumiega–VanVlietparadigm.Sothis
bookisnotjustaboutVisualBasic.NET(VB.NET)anddatabases.It
is about modeling financial instruments in code and putting the
pieces, or models, together to create an automated trading or risk
managementsystemusingaprogramminglanguage,whichinthis
| case is   | VB.NET. | Let’s   | get | started. |          |       |               |     |      |
| --------- | ------- | ------- | --- | -------- | -------- | ----- | ------------- | --- | ---- |
| Financial |         | markets | are | in a     | constant | state | of evolution, |     | from |
buttonwood trees to trading floors to computer screens. Over the
| last 40 | years, | owing | to  | the | invention | of  | computers | and | the |
| ------- | ------ | ----- | --- | --- | --------- | --- | --------- | --- | --- |
development of quantitative tools for market analysis, the pace of
| this change |     | has increased |     | dramatically. |     |     | The revolution |     | in  |
| ----------- | --- | ------------- | --- | ------------- | --- | --- | -------------- | --- | --- |
derivatives market analysis really got into full swing in the early
| 1970s  | when, | soon    | after   | the Chicago |     | Board     | Options | Exchange    |     |
| ------ | ----- | ------- | ------- | ----------- | --- | --------- | ------- | ----------- | --- |
| (CBOE) | began | listing | options |             | on  | equities, | Texas   | Instruments |     |
developed a calculator to price options using the Black-Scholes
formula (Berstein, 1996, pp. 310–316). Over the coming years, one
| major | outcome | of this | revolution |     | may | very | well be | a complete |     |
| ----- | ------- | ------- | ---------- | --- | --- | ---- | ------- | ---------- | --- |
3
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

4 TradingSystemDevelopment
automation of the trading process (Norman, 2001, p. 236). In the
future, computerized investment models and trading algorithms
and instantaneous trade execution could render human traders
completely obsolete (Van Vliet and Kumiega, 2000).
Humantraders,usingstrategiesbasedontechnicalindicators,
fundamentalfactors,orevenplainoldmarketsavvy,arebecoming
increasingly scarce. More and more each day financial engineers
are quantifying trading systems that can watch hundreds of
securities and derivatives in real time and execute hundreds of
strategies instantaneously and simultaneously. The trend that
started decades ago with Moore’s law (a doubling of speed in
computerprocessingpoweraboutevery18months),coupledwith
thedecreasedcostoftechnologyandmarketdata,meansthatinthe
future all profitable trading strategies may be, through mathema-
tics and statistics, quantifiable and programmable.
Theequitiestradingindustrycaughtonseveralyearsagowith
programtradingandindexarbitrage,usingcomputerstogenerate
hundreds of orders simultaneously. The options exchanges,
however, have in the past prohibited automated order entry in an
efforttoprotectmarketmakers.Butitappearsnowthatsuchrules
may very well be abolished in the near future, if they have not
already been by the time this book is published. The Boston
Options Exchange (BOX), which will be opening for business in
mid-2003, currently has no bylaw prohibiting automated order
entry, which will likely have the effect of forcing the other options
exchanges to amend their rules.
Whatever the future holds, however, make no mistake—the
trading game will be as it always has been: The first person, or
computer,torecognizeaprofitableopportunityandexecuteatrade
wins. It’s just that being first is no longer measured in the split
seconds it takes to click your mouse button, but rather the
milliseconds it takes a computer to react. The financial engineer
who can program a computer to recognize profitable trading
opportunities and execute trades is really the trader of the future
(Van Vliet and Kumiega, 2000).
In the trading industry, a key job performed by financial
engineers, among other things, is to formalize trading strategies
based upon quantitative research, back-test algorithms against
Team-LRN

| Introduction |     |     |     |     |     |     |     | 5   |
| ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
historical data, construct or supervise construction of necessary
software for automation of order execution, and, after implemen-
tation, manage the risk of the trading system. Of course, not all
these duties are always performed by just one person, but rather,
| usually, | by a       | team of | financial | engineers |     | and        | programmers.     |     |
| -------- | ---------- | ------- | --------- | --------- | --- | ---------- | ---------------- | --- |
| If       | you intend | to      | have      | a career  |     | in trading | in the financial |     |
markets, you will likely work on such a team, which will require
that at some point you will be required to either write computer
| code yourself, |     | manage | programmers, |     |     | or work | and interact | with |
| -------------- | --- | ------ | ------------ | --- | --- | ------- | ------------ | ---- |
programmers on projects. This will necessitate an understanding
of,attheleast,MicrosoftExcelspreadsheetandtheVisualBasicfor
Applications (VBA) environment, but likely also Visual Basic.NET
| orahigher-levellanguagesuchasC/Cþþ |     |            |     |     |           | orJava.Inadditionyou |                 |     |
| ---------------------------------- | --- | ---------- | --- | --- | --------- | -------------------- | --------------- | --- |
| will need                          | to  | understand |     | how | databases |                      | are constructed | and |
accessedusingcomputercodetodofinancialresearchanddevelop
| trading | and risk | management |     | algorithms |     | and | systems. |     |
| ------- | -------- | ---------- | --- | ---------- | --- | --- | -------- | --- |
All financial research requires data, and the efficient manage-
ment and storage of data is crucial to the profitable operation of a
trading system. “Data is the lifeblood of electronic markets,” as
|              |     |        |     |          | Professional |     | Electronic | Trading |
| ------------ | --- | ------ | --- | -------- | ------------ | --- | ---------- | ------- |
| David Norman |     | states | in  | his book |              |     |            |         |
(2002). Industrial-strength relational database management sys-
tems,suchasOracleorMSSQLServer,canstoregigabytesofsuch
things as historical market data and firmwide trade and position
information (Norman, 2001). Often, historical market data is sim-
ply the opening, high, low, and closing prices or other time-
incremented data such as implied volatilities, but it could also be
more qualitative, economic, or fundamental data such as earnings
reportdata,stocksplits,orFedactions.Whateverthecase,analysis
of data requires not only the knowledge of quantitative methods,
butalsotheprogrammingtoolstoimplementthatanalysisinareal-
life environment. This book addresses topics that are critical to
| these aspects |           | of trading | system | development. |     |      |                 |     |
| ------------- | --------- | ---------- | ------ | ------------ | --- | ---- | --------------- | --- |
| Top           | financial | engineers  |        | estimate     |     | that | only a fraction | of  |
financial engineering actually deals with mathematics. The lion’s
share of time applies to the actual construction and analysis of
| models | and forecasts |     | and technology |           |            | development. |              |     |
| ------ | ------------- | --- | -------------- | --------- | ---------- | ------------ | ------------ | --- |
| This   | majority      |     | of a           | financial | engineer’s |              | time engaged | in  |
construction,though,isnotsimplyspentcoding.Rather,theentire
Team-LRN

6 TradingSystemDevelopment
development process requires this amount of effort; actual time
spent coding should be just a part of it. As you grow in your
understanding of programming and trading and/or risk manage-
ment system development, you will become increasingly aware
that comprehensive blueprints, or plans, or development method-
ologies,ofaprojectmustbelaidoutbeforeanynailsarehammered
or computer keys pressed. The value of a development paradigm
cannot be underestimated.
A good methodology, though, does not mean that an
engineered trading system is infallible. Not every trade and not
every system makes money. There are certainly dozens, if not
thousands, of examples or anecdotes trotted out by “nonquant”
market participants that attempt to disprove the ability of
automated systems to outperform human traders over the long
run. To be sure, the markets are “replete with examples of ‘fat
tails’—unusual and extreme price swings that, based on a reading
of previous prices, would have seemed implausible” according to
Roger Lowenstein in his book When Genius Failed (2000, p. 229). In
the past, quantitative systems, like that of Long Term Capital
Management, which were built on historical data have blown up
quite spectacularly during financial meltdowns, or tenth standard
deviation events, when all correlations go to 1, as they say. But we
don’t stop engineering bridges just because one in London fell
down.Nomatterwhatanybodysays,usingabridgetocrossariver
is still an improvement on taking a boat across. Over time, with
more experience and better engineering, financial models and
forecasting will improve and become more able to weather those
once-a-millennium floods that seem to come around every couple
ofyears.Acomputercan’tbeatKasparovatchessyet.Butgiveita
few more years. Our money is with Deep Blue, or Deep Junior as
the case may be, over the long haul.
The real strategy for quantitative trading systems is to know
aheadof time, through research, the probabilityof the success of a
particular trade or series of trades, and assuming the odds are in
yourfavor,toplayasoftenaspossible,allthewhilekeepingaclose
eyeonriskandthechangingtradewinds(Lowenstein,2000,p.134).
Developing a profitable trading system is no small task,
however. One options trader we talked to estimates that it takes a
Team-LRN

Introduction 7
$10 million investment just to get in the game. That $10 million
pays for building a network infrastructure, hiring high-level
quantitative analysts and programmers, and conducting at least a
yearofresearchanddevelopmentbeforeyouevenmakeyourfirst
trade. Much of this expense, though, may be dedicated to creating
and installing proprietary software and hardware that connects to
| exchanges | through | their | application |     | programming |     | interfaces |
| --------- | ------- | ----- | ----------- | --- | ----------- | --- | ---------- |
(APIs). APIs can be thought of as “pipelines” to the market over
which third parties, such as exchange member trading firms, can
access exchange data and place orders electronically. Installing
| and maintaining |     | a communications |     |     | network | for | data and |
| --------------- | --- | ---------------- | --- | --- | ------- | --- | -------- |
order execution, however, involves a terrible tangle of inter-
connectinghubs,routers,switches,andfiberoptics,nottomention
constantsoftwareredevelopmentasexchangesupgradetheirAPIs
| (Norman, | 2001). |           |     |          |         |     |                |
| -------- | ------ | --------- | --- | -------- | ------- | --- | -------------- |
| Rather   | than   | incurring | the | time and | expense | it  | takes to build |
from scratch, it is also possible and much less capital-intensive to
license third-party trading software and take advantage of the
exchange connections and built-in functionality for data feeds,
order entry, and risk management. Then proprietary analytics and
trading algorithms can be added on top of this software via their
own APIs. Many of these third-party vendors have over 10 years’
experience building front-end systems for futures and options
tradersandare,intermsofdevelopment,wellaheadofevensome
| major       | U.S. trading | houses       | (Norman, |          | 2001).      |        |           |
| ----------- | ------------ | ------------ | -------- | -------- | ----------- | ------ | --------- |
| In          | this book,   | we will      | show     | you      | how to use  | Visual | Basic.NET |
| and several |              | quantitative | tools    | to begin | development |        | of some   |
trading strategies and to analyze data, and we will share some
| ideas | about how | to connect |     | to industry | software |     | via APIs to |
| ----- | --------- | ---------- | --- | ----------- | -------- | --- | ----------- |
monitor financial markets and execute trades. Figure 1.1 shows
graphicallyhowtoimplementatradingsysteminthisway.Inthis
| figure | the arrows | represent | APIs. |               |          |     |            |
| ------ | ---------- | --------- | ----- | ------------- | -------- | --- | ---------- |
| One    | limitation | to        | this  | architecture, | however, |     | is that no |
singlefront-endtradingsystemconnectstoallmarketsaroundthe
world. So it may necessary to create proprietary software that
connects to a multiplicity of front-end trading system APIs to
provide access to all the different markets and products (Norman,
| 2001, p. | 175). |     |     |     |     |     |     |
| -------- | ----- | --- | --- | --- | --- | --- | --- |
Team-LRN

| 8         |           |         | TradingSystemDevelopment |                |     |
| --------- | --------- | ------- | ------------------------ | -------------- | --- |
| F I G U R | E 1.1     |         |                          |                |     |
| The term  | front-end | trading | system refers            | to the “client |     |
workstation [and software], or order entry point, on the exchange
memberlocalareanetwork(LAN)thatatradingfirmusestoaccess
electronicexchangeservices”(Norman,2001,p.242).Anexchange
“back end” is the point where an electronic order reaches the
exchange and passes through to the exchange’s matching engine
(Norman, 2001, p. 242). Electronically routed orders pass from a
| firm’sfront endtotheexchangebackendandthen,oncethetrade |     |     |     |     |     |
| ------------------------------------------------------- | --- | --- | --- | --- | --- |
hasbeenexecuted,againtothefrontendasatrade-fillconfirmation
| (Norman, 2001, | p. 243). |         |          |                  |     |
| -------------- | -------- | ------- | -------- | ---------------- | --- |
| In derivatives | markets, | related | products | are often traded | on  |
different markets. For example, Dow futures trade on the Chicago
Board of Trade, S&P 500 futures trade on the Chicago Mercantile
Exchange, and S&P 500 cash options trade on the Chicago Board
| Options Exchange. | Shares | of IBM | stock trade | on the NYSE | and |
| ----------------- | ------ | ------ | ----------- | ----------- | --- |
Team-LRN

Introduction 9
| other stock | exchanges, | while | IBM     | stock  | futures | trade on One   |
| ----------- | ---------- | ----- | ------- | ------ | ------- | -------------- |
| Chicago     | and NQLX   | and   | options | on IBM | trade   | on the various |
options exchanges. Given the disparate technological infrastruc-
turesandtradingrulesforthedifferentexchanges,connectingtoall
ofthemforautomatedtradingofrelatedproductscanbesomewhat
of a nightmare.
SoasyoumaybeabletoseefromFigure1.1,itispossible,for
example,tobuildanautomatichedgingdevicethroughthetypeof
framework we described. MicroHedge is a popular institutional
software package with connections to the options markets. And
Trading Technologies’ X_Trader software is a popular front-end
softwaresystemforfuturestradingonelectronicmarkets.Thus,we
couldcreateasystemtotradetheCBOE’sS&P500cashoptions,via
a market connection through MicroHedge’s API, that could also
provide real-time delta hedging with the E-Mini S&P contract on
| the Chicago   | Mercantile |          | Exchange | via connection |     | to Trading |
| ------------- | ---------- | -------- | -------- | -------------- | --- | ---------- |
| Technologies’ | API        | (Norman, | 2001).   |                |     |            |
Aswementionedearlier,therearefourdisciplinesthatgointo
| automated | trading | strategy | development: |     | computer | science, |
| --------- | ------- | -------- | ------------ | --- | -------- | -------- |
quantitative finance, trading strategy, and quality development.
Thisisalottolearn.Wedonotattemptteachyouallofit.Ratherwe
bringtogethersomeimportantideasfrommath,technology,project
management,andthefinancialmarketsthatarerequiredtobuilda
| real-world | automated | trading | system. |     |     |     |
| ---------- | --------- | ------- | ------- | --- | --- | --- |
Team-LRN

This page intentionally left blank.
Team-LRN

| C           | H A | P T E | R 2 |     |             |     |     |     |
| ----------- | --- | ----- | --- | --- | ----------- | --- | --- | --- |
| Development |     |       |     |     | Methodology |     |     |     |
S
owhatisanautomatedtradingorriskmanagementsystem,and
| what process |     | do we go | through | to  | create | one? |     |     |
| ------------ | --- | -------- | ------- | --- | ------ | ---- | --- | --- |
Atradingorriskmanagementsystem,aswedefineit,consists
of the rules for automated entry into and exit from a position or
| positions | and | the technology |     | used | to make | them | happen. | These |
| --------- | --- | -------------- | --- | ---- | ------- | ---- | ------- | ----- |
rules are a set of logical or mathematical operations that can be
based upon qualitative, technical, or quantitative research. Many
books and papers currently available outline stock and futures
| trading | system | development |     | from | a   | purely technical |     | analysis |
| ------- | ------ | ----------- | --- | ---- | --- | ---------------- | --- | -------- |
standpoint, often using a retail software package to optimize a set
of trading rules based upon moving averages and oscillators. In
this book, however, we will focus on quantitative analysis of
| equities, | equity | indexes, |     | and | options | on equities |     | and the |
| --------- | ------ | -------- | --- | --- | ------- | ----------- | --- | ------- |
programming of professional, proprietary software using Visual
Basic.NET.
Several steps are involved in creating a quantitatively based
trading system, and while clearly not exhaustive since there are
literally an infinite number of potential quantifiable trading
strategies, this book presents some of the necessary steps to create
an automated system, with lots of code examples along the way.
Beforewebegin,however,weshoulddefinethestepstogothrough
| or the            | process | of creating | an      | automated |         | system. |        |           |
| ----------------- | ------- | ----------- | ------- | --------- | ------- | ------- | ------ | --------- |
| In                | their   | paper       | “An     | Automated |         | Trading | System | Develop-  |
| ment Methodology” |         |             | (2003), | Andrew    | Kumiega | and     | Ben    | Van Vliet |
propose a process for trading system development that consists of
four phases: research and documentation of calculations, back
| testing, | implementation, |     | and | portfolio | and | risk management. |     |     |
| -------- | --------------- | --- | --- | --------- | --- | ---------------- | --- | --- |
11
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

| 12          |         |     |             |         |                 | TradingSystemDevelopment |     |           |     |
| ----------- | ------- | --- | ----------- | ------- | --------------- | ------------------------ | --- | --------- | --- |
| KUMIEGA–VAN |         |     | VLIET       | TRADING |                 | SYSTEM                   |     |           |     |
| DEVELOPMENT |         |     | METHODOLOGY |         |                 |                          |     |           |     |
| By their    | nature, | all | implemented |         | and functioning |                          |     | automated |     |
tradingorriskmanagementsystemsmustmanagetwoconcurrent
processes: (1) trade selection and (2) portfolio and risk manage-
ment. However, prior to implementation the process of develop-
mentshouldfollowawell-defined,well-documentedflowofsteps
alongadevelopmentmethodology.In2001,KumiegaandVanVliet
| first proposed |     | a software | development |     | methodology |     |     | for finan- |     |
| -------------- | --- | ---------- | ----------- | --- | ----------- | --- | --- | ---------- | --- |
cial markets that laid out the steps to codify trading and risk
managementalgorithms.Thisearliermodelisencompassedwithin
thisbroadermethodology,whichoutlinesanentiretradingsystem
| development | paradigm. |     |     |     |     |     |     |     |     |
| ----------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
KumiegaandVanVlietproposeastandardizedmodelforthe
| development |     | of automated |     | trading | systems |     | that will | ensure |     |
| ----------- | --- | ------------ | --- | ------- | ------- | --- | --------- | ------ | --- |
rapidity, desired by senior management, and consistent quality
standards,desiredbyfinancialengineers.Whiletheidiosyncrasies
ofthesecuritiesandderivativestradingindustriesrequireaunique
| system development |     |     | paradigm, | this | methodology |     | owes | a   | large |
| ------------------ | --- | --- | --------- | ---- | ----------- | --- | ---- | --- | ----- |
portionofitsstructuretoacombinationofthetraditionalwaterfall
model (Royce, 1970) and the evolutionary spiral models (Boehm,
1988). The combination of these two models seeks to gain from
their respective strengths as well as to overcome their respective
weaknesses.
|                 |             | Waterfall |       | Methodology |        |          |        |          |     |
| --------------- | ----------- | --------- | ----- | ----------- | ------ | -------- | ------ | -------- | --- |
| The traditional |             | waterfall | model | is          | a very | powerful |        | software |     |
| development     | methodology |           | and   | consists    | of     | four     | phases | that,    | in  |
general,maptothefourphasesoftheKumiega–VanVlietmodel—
analysis, design, implementation, and ongoing system testing. At
| the completion |     | of each | phase, | the | waterfall | model |     | requires | a   |
| -------------- | --- | ------- | ------ | --- | --------- | ----- | --- | -------- | --- |
decisionbymanagementpriortoadvancingtothenextphase.This
decision is whether or not to continue development of the system
| based upon | the | potential | for profitable |     | implementation. |     |     |     |     |
| ---------- | --- | --------- | -------------- | --- | --------------- | --- | --- | --- | --- |
Inanutshell,thewaterfallmodelforcesfinancialengineersto
think about the system to be built and to come up with a plan for
buildingit,beforetheybeginconstruction.Byfollowingthismodel,
Team-LRN

| DevelopmentMethodology |     |     |     |     |     |     |     | 13  |
| ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
wecanforceourselvestouseadisciplinedapproachtotheprocess
of development and to avoid the pitfalls of creating a system and
writingcomputercodebeforetheblueprintsoftheprojectarewell
| defined | and precisely |     | laid        | out.     |      |           |       |           |
| ------- | ------------- | --- | ----------- | -------- | ---- | --------- | ----- | --------- |
| The     | waterfall     |     | methodology |          | does | have a    | major | drawback  |
| though: | It puts       | too | much        | emphasis | on   | planning. | The   | waterfall |
modelnecessitatesthatalldetailsandallplansbedefinedupfront
beforedesignandimplementationbegin.Thatistosay,thereisno
room for error and no process for handling feedback or problems
that occur down the road. In the fast-moving financial markets,
where trading opportunities come and go quickly, the waterfall
| model may | not         | be able | to      | react | quickly | enough.           |     |       |
| --------- | ----------- | ------- | ------- | ----- | ------- | ----------------- | --- | ----- |
| As        | an example, |         | suppose | we    | find in | an implementation |     | phase |
thatacoherenttradingideawillbeimpossiblycomplexintermsof
the technology needed to make it happen. As a result the project
fails. Had the financial engineers been aware of this fact in the
| analysis | phase, | they | may | have | been able | to modify | the | system |
| -------- | ------ | ---- | --- | ---- | --------- | --------- | --- | ------ |
designsoastoenablesuccessfulconstruction.Thewaterfallmodel
has no way of handling these types of situations. Furthermore,
technology these days is changing just about as fast as the market
itself. The danger with the waterfall methodology is that by the
time a trading system is ready for implementation, the technology
it was built on may be obsolete and there may be a better, faster,
| easier technology |          | already    |              | on the      | market. |               |        |     |
| ----------------- | -------- | ---------- | ------------ | ----------- | ------- | ------------- | ------ | --- |
| To                | overcome | the        | shortcomings |             | of      | the waterfall | model, | the |
| spiral model      | was      | developed. |              |             |         |               |        |     |
|                   |          | Spiral     |              | Methodology |         |               |        |     |
In the spiral methodology a small amount of time is initially
devoted to each of four phases: research, planning, implemen-
tation, and testing, followed by several repetitive iterations or
| cycles over | each | of them. |     |     |     |     |     |     |
| ----------- | ---- | -------- | --- | --- | --- | --- | --- | --- |
As the cycles progress and the spiral gets larger, more detail
and refinement are gained in each phase. At some final point, it is
| hoped, | each phase | will | be  | complete. |     |     |     |     |
| ------ | ---------- | ---- | --- | --------- | --- | --- | --- | --- |
Inthisway,thespiralmethodallowsforfeedbackasproblems
in the system are detected. A problem can be dealt with either by
Team-LRN

14 TradingSystemDevelopment
correcting it or, if the problem is fatal, by scrapping the entire
trading idea. Of course, the truly fatal problem is the prospect of
losses. If the system cannot or will not be profitable, for whatever
reason, it will be discarded. So intermittent or prototype
implementations can provide feedback about the viability and
profitability of the trading system. Also, as new discoveries in
quantitative methods and system design are made, the system’s
blueprints can incorporate them as they arise.
Aswiththewaterfallmethod,thespiralmethodisnotwithout
its drawbacks. The primary problem with the spiral methodology
is that the number of cycles can grow without end, using up
resources. There are no inherent constraints or deadlines. This can
lead to loss of project focus, messy logic, and extraneous or
unnecessary digressions. This is often called scope creep, when the
scope of the projects gets continuously larger.
As a result, the blueprints may never present a clear and
concise architecture of the trading system. So in the spiral model,
the cycling process must have a clear condition for termination.
ThislackofterminationiscommoninExcel-basedtradingsystems.
To overcome the problems with each of these methodologies,
Kumiega and Van Vliet have combined them into a single
paradigm for trading system development. As Figure 2.1
illustrates, the four phases progress in a traditional waterfall, but
within each phase, four elements are connected into a spiral
structure. At the completion of each phase, management must
make a decision before proceeding to the next phase. After
completing the fourth and final phase, the methology calls for
financial engineers to repeat the entire waterfall process for
continuous improvement. The phases are as follows:
Phase I. Research and Document Calculations
1. Describe trading idea.
2. Research quantitative methods.
3. Prototype in Excel.
4. Check profitability.
Phase II. Back-Test
1. Gather data.
2. Clean data.
3. Perform in-sample/out-of-sample test.
Team-LRN

DevelopmentMethodology 15
|       | 4. Check       | profitability.   |           |     |
| ----- | -------------- | ---------------- | --------- | --- |
| Phase | III. Implement |                  |           |     |
|       | 1. Build       | vision and scope | document. |     |
2.
|       | Build          | objects and   | program           | document.         |
| ----- | -------------- | ------------- | ----------------- | ----------------- |
|       | 3. Program     | and document  | the               | system.           |
|       | 4. Paper-trade | and check     | profitability.    |                   |
| Phase | IV. Manage     | Portfolio     | and Risk          |                   |
|       | 1. Monitor     | portfolio     | statistics.       |                   |
|       | 2. Perform     | value-at-risk | calculations.     |                   |
|       | 3. Document    | profit and    | loss attribution. |                   |
|       | 4. Determine   | causes        | of variation      | in profitability. |
Repeat the entire waterfall process for continuous improvement.
Here is some brief discussion on the 16 elements listed in the
| Kumiega–Van | Vliet   | methodology. |     |     |
| ----------- | ------- | ------------ | --- | --- |
| F I G U     | R E 2.1 |              |     |     |
Team-LRN

| 16    |     |          |     |     |          | TradingSystemDevelopment |     |
| ----- | --- | -------- | --- | --- | -------- | ------------------------ | --- |
| PHASE | I.  | RESEARCH |     | AND | DOCUMENT |                          |     |
CALCULATIONS
The first of the four phases consists of researching quantitative
| algorithms | for | a trading | system. |         |      |     |     |
| ---------- | --- | --------- | ------- | ------- | ---- | --- | --- |
|            |     | Describe  |         | Trading | Idea |     |     |
There is an old saying in the trading business, “Got a hunch, bet a
bunch.” As with most old sayings, this one is based more on fact
thanfiction. In most humanendeavors it is more fun to do thanto
plan. This trait is very human and is only driven out of people by
years of schooling and life. There are two problems with planning
infinance.Oneproblemisthatmosttraderswanttotrade,notplan.
And the second problem is that most planners never get to trade
since management in financial firms mainly rise from the trading
ranks, which means they strive to optimize for the short term.
| Therefore, |     | in financial |     | markets | we have | a large | number of |
| ---------- | --- | ------------ | --- | ------- | ------- | ------- | --------- |
simple systems being built again and again and again. However,
these simple systems do not result in maintainable excess returns.
We have a few firms that do actually implement their long-term
plans,andtheseplansdoresultinmaintainableexcessreturns.The
small-sized firms that become mid-sized firms eventually end up
beingsoldtolargefirms.Thefewlargefirmsthatcontinuetobuild
their proprietary systems end up dominating markets. The most
interesting feature of the business is that the best trading and
money management firms seem to understand this, given the size
| of their | budgets | for proprietary |     | trading | system | development. |     |
| -------- | ------- | --------------- | --- | ------- | ------ | ------------ | --- |
Complextradingsystemsarebuiltonestepatatime,evolving
along the way. The first step toward building a trading system is
normallythehardestone.Itmayseemelementary,butbeingableto
clearly articulate a trading idea is extremely important. Being
forcedtodescribeanideahastheeffectofclarifyingyourthoughts,
| as well | as communicating |     |     | plans and | defining | goals | and the |
| ------- | ---------------- | --- | --- | --------- | -------- | ----- | ------- |
meaning of success. The more complex the trading idea, the more
| time it | takes to | define | and communicate |     | it clearly. |     |     |
| ------- | -------- | ------ | --------------- | --- | ----------- | --- | --- |
Thedescriptionofthetradingideashouldcontaintheanswers
| to several | basic | questions: |     |     |     |     |     |
| ---------- | ----- | ---------- | --- | --- | --- | --- | --- |
Team-LRN

DevelopmentMethodology 17
1. What market or markets will be traded?
2. What capital will be traded?
a. Short term
b. Long term
c. Midterm
3. Whose capital is it? Proprietary or investor capital?
4. Howwillsuccessbedefined?Isthereabenchmarkagainst
which to compare the results? Are there competitors
against which to compare results?
a. Best/worst/average returns for a group
b. Sharpe ratio
5. What is the strategic advantage over the competition?
a. Data
b. Calculations
c. Speed
d. Capital cost
6. Whatistheexpectedtimehorizonforlaunchoftheinitial
paper trading?
7. What is the expected time horizon for full-scale trading?
Thegoalofthisstageoftheprojectistofocusattentiononthe
long-term features of the trading system. As with most business
ideas,afocused,well-definedplanisessential,especiallyinastart-
upphase.Duetothelowbarrierstoentry,onecommonsituationin
thetradingindustryistheexistenceofmultipletradingfirmswith
little or no focus and, to make matters worse, meager start-up
capital.
Research Quantitative Methods
Research into quantitative methods may be in the form of the
derivation of proprietary algorithms or the application of publicly
availableresearchorwhitepapers.Furthermore,thisresearchmay
also include gaining an understanding of the methodologies of
other successful systems.
Tobe successfulat quantitative research, you shouldtakefull
advantage of the available resources such as the Internet and
librariesofacademicpublications.Buildingaproprietarylibraryof
quantitative methods is key to long-term system and firm success.
Team-LRN

| 18  |     |     |     |     | TradingSystemDevelopment |     |     |
| --- | --- | --- | --- | --- | ------------------------ | --- | --- |
Booksandpapersinthislibraryshouldbecatalogedbytheauthor,
the firm, and the nature of the quantitative method discussed.
|          |          | Prototype |             | in Excel    |     |     |         |
| -------- | -------- | --------- | ----------- | ----------- | --- | --- | ------- |
| Excel is | the most | rapid     | development | environment |     | for | testing |
trading ideas. However, large spreadsheets, especially those that
contain historical data, can become increasingly difficult to
| document | and manage. |     |     |     |     |     |     |
| -------- | ----------- | --- | --- | --- | --- | --- | --- |
Check Profitability
At any point in this or any other of the four stages, profitability
testing may show system failure. That is, the trading system may
not be profitable. This will necessitate a looping back to previous
stages.Thegoalistoquicklystopdevelopmentontradingsystems
| that have | a low probability |     | of success. |     |     |     |     |
| --------- | ----------------- | --- | ----------- | --- | --- | --- | --- |
| PHASE     | II. BACK-TEST     |     |             |     |     |     |     |
Abacktestisasimulationofanautomatedtradingsystemagainst
historical data. A back test determines what buys and sells would
| have been | made | according | to  | a prescribed | set | of algorithms. |     |
| --------- | ---- | --------- | --- | ------------ | --- | -------------- | --- |
Successful system analysis and design necessitates research into
| past market | movement | as  | a way | to analyze | and | validate | the |
| ----------- | -------- | --- | ----- | ---------- | --- | -------- | --- |
system. But not only should back testing confirm the validity and
accuracy of a system’s algorithms; it must also confirm risks and
| rewards | of competing | alternative |     | algorithms. |     |     |     |
| ------- | ------------ | ----------- | --- | ----------- | --- | --- | --- |
|         |              | Gather      |     | Data        |     |     |     |
Itmayseemobvious,butbeingabletogatherthenecessarymarket
data is very important. Oftentimes data required may not exist at
| all or may | be too expensive. |     |     |     |     |     |     |
| ---------- | ----------------- | --- | --- | --- | --- | --- | --- |
Team-LRN

DevelopmentMethodology 19
|     |     |     | Clean | Data |     |     |     |
| --- | --- | --- | ----- | ---- | --- | --- | --- |
Oneofthemajorobstaclestobuildingaprofitabletradingsystemis
the unavailability of clean and timely data. Many systems that are
dependent upon the analyses of historical data are never fully
implementedbecausedataiseithertooexpensiveornotobtainable
altogether.Therefore,priorto startingaproject,thedatafeedsand
| their prices | should |                         | be determined. |     |     |     |      |
| ------------ | ------ | ----------------------- | -------------- | --- | --- | --- | ---- |
| Perform      |        | In-Sample/Out-of-Sample |                |     |     |     | Test |
Financial engineers are keenly aware of the extent to which in-
sampleresultsofmodelfittingdifferfromresultsobtainedonout-
of-sample data. Trading algorithms and quantitative models must
be examined against out-of-sample data prior to moving to the
| implementation |     | stage. | A well-developed |     |     | system | will perform |
| -------------- | --- | ------ | ---------------- | --- | --- | ------ | ------------ |
similarly out-of-sample as it does in-sample. It is of course
important to save some of your historical data for out-of-sample
testing.
|        |          |     | Check             | Profitability |        |        |              |
| ------ | -------- | --- | ----------------- | ------------- | ------ | ------ | ------------ |
| Again, | checking |     | the profitability |               | of the | system | will prevent |
additional time and resources from being spent on unprofitable
projects.Wemayneedtoloopbacktotheinitialresearchphaseand
| reassess       | the quantitative |           | methods      | and | algorithms. |        |              |
| -------------- | ---------------- | --------- | ------------ | --- | ----------- | ------ | ------------ |
| PHASE          | III.             | IMPLEMENT |              |     |             |        |              |
| Implementation |                  | of        | an automated |     | trading     | system | will require |
connectivity between and interoperability with disparate software
| systems | for | trade | execution | and | other | processes | such as |
| ------- | --- | ----- | --------- | --- | ----- | --------- | ------- |
optimization.Thiswillrequirethecreationofplansandblueprints
| before programming |     |     | in a language |     | like VB.NET | begins. |     |
| ------------------ | --- | --- | ------------- | --- | ----------- | ------- | --- |
Team-LRN

20 TradingSystemDevelopment
Build Vision and Scope Documents
The purpose of the vision and scope documents is to ensure that
management fully understands the end goal along with the
expected costs of the project before construction starts. The vision
document provides both the financial engineers assigned to the
project and management a brief overview of the current project.
Theinformation listed onthe visiondocument should beat avery
high level so that the entire form can be completed in a couple of
hours.
The scope document should clearly define the steps for the
project along with the documentation of all the detailed
information about a calculation. After management has approved
theinitialproject concept andthevision document,thenthe scope
document can be completed. A full-blown scope document can
rangefrom2or3pagestoover20pagesdependingonthelevelof
detail provided. Its design should allow for multiple revisions
along the way. This is important in finance since many of the key
itemsofaprojectgetrevisedregularlyasthedetailsgetflushedout
with prototypes.
The following samples of vision and scope documents
provide some basic information about the project in a consistent
manner from project to project.
Team-LRN

| DevelopmentMethodology |     |     |     |     |     | 21  |
| ---------------------- | --- | --- | --- | --- | --- | --- |
Project 1
|                     | Vision | Document |         |       |          |     |
| ------------------- | ------ | -------- | ------- | ----- | -------- | --- |
| Project Leader:     | Andrew |          | Kumiega | Date: | 03/01/03 |     |
| Project Originator: | Ben    | Van      | Vliet   |       |          |     |
| Sponsor:            | Bob    | Hendry   |         |       |          |     |
Project Definition:
| This section | should | include | a one-paragraph |     | definition | of  |
| ------------ | ------ | ------- | --------------- | --- | ---------- | --- |
| the project. |        |         |                 |     |            |     |
Major Objectives:
This section should list the major objectives of the project.
Impact:
| This section | should | define | and forecast | the | success | of the |
| ------------ | ------ | ------ | ------------ | --- | ------- | ------ |
project.
| Priority/Deadline | Issues: |     |     |     |     |     |
| ----------------- | ------- | --- | --- | --- | --- | --- |
Thissectionshouldlistalldeadlines,knownpriorities,and
| other issues | relevant | to the | project. |     |     |     |
| ------------ | -------- | ------ | -------- | --- | --- | --- |
Constraints:
| This section | should | list | any known | constraints |     | for this |
| ------------ | ------ | ---- | --------- | ----------- | --- | -------- |
project.
| Analysis of  | Product:         |     |           |           |               |     |
| ------------ | ---------------- | --- | --------- | --------- | ------------- | --- |
| This section | defines          | how | we intend | to test   | the implemen- |     |
| tation       | of the completed |     | product,  | including | white-        | and |
| black-box    | testing.         |     |           |           |               |     |
Resources:
| This section | should      | list the | financial    | engineers  | involved | in        |
| ------------ | ----------- | -------- | ------------ | ---------- | -------- | --------- |
| the project  | as well     | as other | support      | personnel, |          | including |
| additional   | programmers |          | and hardware | support.   |          |           |
Team-LRN

22 TradingSystemDevelopment
| Project  | Type: _____Formal | _____Ad Hoc            |
| -------- | ----------------- | ---------------------- |
| Initial  | Priority: A       | B C D E                |
| Approved | By:               | ______________________ |
| Approved | Date:             | ______________________ |
Team-LRN

| DevelopmentMethodology |             |     |        |           |     |       |          |     | 23  |
| ---------------------- | ----------- | --- | ------ | --------- | --- | ----- | -------- | --- | --- |
|                        |             |     |        | Project   | 1   |       |          |     |     |
|                        |             |     | Scope  | Document  |     |       |          |     |     |
| Project                | Leader:     |     | Andrew | Kumiega   |     | Date: | 03/01/03 |     |     |
| Project                | Originator: |     | Ben    | Van Vliet |     |       |          |     |     |
| Sponsor:               |             |     | Bob    | Hendry    |     |       |          |     |     |
Project Definition:
|     | This section | should |     | include | a one-paragraph |     | definition |     | of  |
| --- | ------------ | ------ | --- | ------- | --------------- | --- | ---------- | --- | --- |
theproject.Also,theprojectdefinitionshouldbeupdatedas
|     | additional | specifications |     | arise | or  | changes | to the | specifica- |     |
| --- | ---------- | -------------- | --- | ----- | --- | ------- | ------ | ---------- | --- |
|     | tions are  | made.          |     |       |     |         |        |            |     |
Functionalities:
|     | The entire     | list         | of functionalities |      |          | of the | application   | should |     |
| --- | -------------- | ------------ | ------------------ | ---- | -------- | ------ | ------------- | ------ | --- |
|     | befully        | documentedin |                    | this | section. | Beyond | whatever      |        | may |
|     | be the obvious |              | functionalities,   |      | here     | a      | few important | things |     |
to remember:
|     | V Management     |              | will   | likely   | still want | printed    | reports.        |           |     |
| --- | ---------------- | ------------ | ------ | -------- | ---------- | ---------- | --------------- | --------- | --- |
|     | V Bulletproof    |              | error  | handling |            | must       | be incorporated |           | to  |
|     | prevent          | trading      | errors |          | due        | to bad     | data or         | erroneous |     |
|     | human            | interaction. |        |          |            |            |                 |           |     |
|     | V The algorithms |              | should |          | be clearly | explained. |                 |           |     |
V Thegraphicaluserinterface,assimpleasitmayturnout
|     | to be, | should | be fully | laid | out. |     |     |     |     |
| --- | ------ | ------ | -------- | ---- | ---- | --- | --- | --- | --- |
V Acompletedatadictionaryshouldtobebuiltalongwith
|     | a data  | flow         | map. |             |     |          |               |     |     |
| --- | ------- | ------------ | ---- | ----------- | --- | -------- | ------------- | --- | --- |
|     | V Speed | of execution |      | is critical |     | for many | applications, |     | and |
socompetingmethodsofimplementationmayneedtobe
analyzed.
| Steps | and Milestones: |     |           |     |                |     |         |       |      |
| ----- | --------------- | --- | --------- | --- | -------------- | --- | ------- | ----- | ---- |
|       | The purpose     | of  | the Steps |     | and Milestones |     | section | is to | keep |
theprojectontrack.Thegoalistodocumentatahighlevel
|     | all the           | major       | steps | and     | milestones |                 | that are | required | to   |
| --- | ----------------- | ----------- | ----- | ------- | ---------- | --------------- | -------- | -------- | ---- |
|     | complete          | the trading |       | system. | A          | simple,         | but key, | element  | of   |
|     | the documentation |             |       | of the  | steps      | is color-coding |          | of       | work |
Team-LRN

24 TradingSystemDevelopment
items. These steps should be updated at least weekly as
progress is made on the project.
V Standard black text is used to list steps and milestones
that are progressing as planned.
V Blue text is used to show steps and milestones that have
been completed.
V Red text is used to show steps and milestones that have
stopped and are currently placing the project at risk.
V Green is used to show scope creep.
As we have discussed, scope creep can be the most
dangerous portion of a project as stakeholders request
additionstotheproject.Unnecessarydigressionscandoom
a project, and so it is important to focus on specific and
relevant functionalities. However, as is typically the case,
rejected additions will be used as an excuse if the trading
system loses money.
Future Features:
This section should describe any additional features that
should be started after the initial project is completed. The
goal of this section is to contain scope creep.
Schedule:
A schedule should be presented in this section done in
project management software such as Microsoft Project.
Detailed Documentation of Key Functionalities:
Key functionalities of the trading systems should be fully
documented—for example, data, I/O, GUIs, calculations,
error handling, and reports.
Team-LRN

DevelopmentMethodology 25
Build Objects and Program Document
Building a trading system in code is a bit like building a building.
The bigger and more complex the building, the more important
blueprints are to the success of the project. Likewise, the more
complex a trading system becomes, the more important it is to
create detailed architectural plans before construction in code
begins. But how do we create these blueprints? The answer is the
Uniform Modeling Language (UML). UML is the software
industry’s graphical language that enables project designers and
programmers to communicate the details of software design.
Through the use of UML, programming problems can be
solved in an object-oriented way before programming begins. As
you can imagine then, financial engineers who want to use UML
must be familiar with object-oriented programming and the
process of abstraction and application modeling. (Don’t worry. If
you are not familiar with these concepts, we will show you them
overthecourseofthisbook.)ModelswrittenusingUMLwillhelp
us visualize and document the structure of a software application.
Program and Document the System
Having proved the trading system to be successful through in-
sample and out-of-sample testing, we proceed with the crossover
stage of the system development process. In this stage we cross
overfromExcel’scell-basedenvironmenttoVB.NETbyconverting
the system’s functionalities into programming code.
Paper-Trade and Check Profitability
Thistimewhenwecheckprofitability,wewillhavesomereal-time,
live data to go on. The last step prior to opening an account and
turning on a trading system is paper trading. Placing simulated
trades against real-time market data will give us a true and final
test of the potential of a trading system.
Team-LRN

| 26    |     |            |     |     |           |     | TradingSystemDevelopment |      |
| ----- | --- | ---------- | --- | --- | --------- | --- | ------------------------ | ---- |
| PHASE |     | IV. MANAGE |     |     | PORTFOLIO |     | AND                      | RISK |
Apartfromthesimplesttradingsystems,noindividualtradeexists
inavacuum.Rather,allthetradesandsubsequentpositionswillbe
| viewed | as  | a portfolio |     | of positions. |     |            |     |     |
| ------ | --- | ----------- | --- | ------------- | --- | ---------- | --- | --- |
|        |     | Monitor     |     | Portfolio     |     | Statistics |     |     |
Portfolios of securities and derivatives require constant monitor-
ing. No system, no matter how well planned or well built, should
be left unattended. A system for monitoring trade limits, risk
| factors | such    | as          | portfolio     | delta | and      | gammas,      | and | drawdowns |
| ------- | ------- | ----------- | ------------- | ----- | -------- | ------------ | --- | --------- |
| should  | be      | implemented |               | and   | followed | strictly.    |     |           |
|         | Perform |             | Value-at-Risk |       |          | Calculations |     |           |
Value-at-risk calculations will give management a snapshot of the
potential losses given a portfolio. However, while methods for
dealingwithextraordinaryoccurrencesmaybebuiltintoatrading
| system, | overnight |          | volatility |        | in the | form | of opening  | gaps may |
| ------- | --------- | -------- | ---------- | ------ | ------ | ---- | ----------- | -------- |
| render  | them      | useless. |            |        |        |      |             |          |
|         | Document  |          |            | Profit | and    | Loss | Attribution |          |
A good way to monitor the success of a system is to keep track of
individual trades and their respective payoffs. These will be
valuablewhenreevaluatingtheunderlyingpremiseforthesystem.
| Determine |     |     | Causes | of  | Variation |     | in Profitability |     |
| --------- | --- | --- | ------ | --- | --------- | --- | ---------------- | --- |
Profitable trading systems will not be so forever. Eventually, the
marketwillclosethedooronourtrade.Sosystemswillneedtobe
continuouslytweaked,andintheendscrapped.Thegoalhereisto
quicklystoptradingsystemsthatlosetheiredgebeforetheycause
losses.Asuccessfullyimplementedtradingsystemalwaysrequires
| ongoing | profitability |     | assessment. |     |     |     |     |     |
| ------- | ------------- | --- | ----------- | --- | --- | --- | --- | --- |
Team-LRN

DevelopmentMethodology 27
Repeat the Entire Waterfall Process for
Continuous Improvement
Continuous improvement consists of an ongoing effort toward
bettering our trading systems. When applied to a trading
environment, a continuous-improvement strategy involves both
management and financial engineers working together in trading
teams to make small improvements continuously. It is top-level
management’s responsibility to cultivate a professional environ-
mentthatengendersconstantimprovement.Acultureofsustained
ongoingimprovementwillfocuseffortsoneliminatingwasteinall
tradingsystemsandprocessesofatradingorganization.Intelligent
companyleadershipshouldguideandencouragetradingteamsto
continuously improve profitability, increase efficiency, and reduce
costs.
Throughsmallinnovationsfromresearchandentrepreneurial
activity,tradingfirmscandiscoverbreakthroughideas.Theseideas
include, among other things, the creation of new trade selection
algorithms,theapplicationofexistingsystemstonewmarkets,and
the implementation of new technologies for more efficient trade
execution.
SUMMARY
TheadvantageoftheKumiega–VanVlietapproachisthatitallows
financial engineers to quickly deliver a prototype for evaluation
and specifications prototyped in Excel that are scalable into
VB.NET or some other implementation language. If the trading
system is deemed to have a high probability of long-term
profitability, financial engineers can proceed down the waterfall.
There are four distinct advantages to using this methodology
for trading system development:
1. The research and documentation stage along with its
Excel prototyping approach provides a mechanism for
documenting the system requirements and for gaining
buy-in from senior management. Financial engineers
Team-LRN

28 TradingSystemDevelopment
should be able to explicitly state and demonstrate the
algorithms and profitability of a trading system prior to
implementation.
2. The iterative framework of documentation, prototyping,
and testing of intermediate-level working versions of the
system allows for feedback and reduces risks before they
become problematic.
3. Thismethodologyallowsforstep-by-steptestingofcoded
algorithms against Excel’s built-in functions.
4. Time to market is greatly reduced since the Excel
prototype demonstrates the profitability of a system in a
short amount of time.
The process of doing quantitative research in financial
markets requires the completion of these four phases of
development resulting in four models: the algorithms model,
data model, implementation model, and risk management model.
Over the remainder of this book, each of these phases, and their
subphases,willbeaddressed.Alongtheway,wewilllearnagreat
deal about quantitative finance, Visual Basic.NET, ADO.NET,
databasesandSQL,object-orientedprogramming,XML,andUML.
Team-LRN

DevelopmentMethodology 29
PROBLEMS
| 1. When | developing | financial | models in Visual Basic.NET, |
| ------- | ---------- | --------- | --------------------------- |
howdowetestwhetherornotouralgorithmsarecorrect?
| 2. What | is a trading | system?       |              |
| ------- | ------------ | ------------- | ------------ |
| 3. What | is meant     | by continuous | improvement? |
| 4. What | are vision   | and scope     | documents?   |
| 5. What | is UML used  | for?          |              |
Team-LRN

This page intentionally left blank.
Team-LRN

| S E C                      | T I O N        | T W O                |           |
| -------------------------- | -------------- | -------------------- | --------- |
| Introduction               |                | to VB.NET            |           |
| Algorithm                  | Development    |                      |           |
| The ability                | to learnfaster | than yourcompetitors | may bethe |
| onlysustainablecompetitive |                | advantage.           |           |
Peter Senge
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

This page intentionally left blank.
Team-LRN

| C H A   | P T | E R 3   |     |      |     |     |     |
| ------- | --- | ------- | --- | ---- | --- | --- | --- |
| Getting |     | Started |     | with |     |     |     |
VB.NET
I
n this chapter you will learn how to maneuveraround the Visual
| Basic.NETintegrated |     | development |     | environment | (IDE) | and | how to |
| ------------------- | --- | ----------- | --- | ----------- | ----- | --- | ------ |
customizeittoyourlikingforefficientdevelopment.Whilewewill
| only be writing      | a                | smidgen | of  | code, we | will  | be creating | a     |
| -------------------- | ---------------- | ------- | --- | -------- | ----- | ----------- | ----- |
| professional-looking |                  | program | and | learning | a few | simple      | tech- |
| niques that are      | big time-savers. |         |     |          |       |             |       |
| DIFFERENT            | VERSIONS         |         | OF  | VISUAL   | BASIC |             |       |
TherearedifferentversionsofVisualBasic.Thisbookpresentsthe
latest version, Visual Basic.NET. If you are using Visual Basic 6.0,
we suggest you upgrade your software to take full advantage of
the .NET environment. Since many readers are probably already
familiar with VBA (Visual Basic for Applications), which is very
similar to VB 6.0, this book will be particularly valuable in
converting spreadsheets and VBA macros into professional stand-
| alone software. | While | VB.NET |     | does support | some | backward |     |
| --------------- | ----- | ------ | --- | ------------ | ---- | -------- | --- |
compatibility, we have in all cases used .NETconstructs and have
| left COM to the | scrap      | bin. |     |             |     |     |     |
| --------------- | ---------- | ---- | --- | ----------- | --- | --- | --- |
| THE VB.NET      | INTEGRATED |      |     | DEVELOPMENT |     |     |     |
ENVIRONMENT
Visual Studio.NETenables you to program visually, dragging and
dropping controls, like buttons and text boxes, into place rather
33
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

| 34            |     |      |          |         |      | IntroductiontoVB.NET |             |     |
| ------------- | --- | ---- | -------- | ------- | ---- | -------------------- | ----------- | --- |
| than creating |     | them | in code. | In this | way, | visual               | programming |     |
greatlyincreasesprogrammerproductivity.VisualStudio.NETalso
includes several advanced tools for writing and debugging your
| program code. |          | Let’s | jump     | right in. |            |     |      |         |
| ------------- | -------- | ----- | -------- | --------- | ---------- | --- | ---- | ------- |
| Step          | 1 Before |       | you open | Visual    | Basic.NET, | you | will | need to |
createaseparatefolderonyourharddrivetoholdall
|      | the    | files  | for all | the projects     | in     | this book,  |          | so create a |
| ---- | ------ | ------ | ------- | ---------------- | ------ | ----------- | -------- | ----------- |
|      | folder | called |         | “C:\ModelingFM.” |        |             |          |             |
| Step | 2 Now  | go     | ahead   | and open         | Visual | Studio.NET. |          |             |
| Step | 3 When | the    | Start   | Page opens,      | click  | New         | Project. |             |
| Step | 4 Give | the    | project | the name         | “Test” | and         | the      | location of |
theModelingFMfolder.Also,wewillbeusingVisual
|     | Basic.NET |     | for     | the projects         | in   | this book, | and       | so leave  |
| --- | --------- | --- | ------- | -------------------- | ---- | ---------- | --------- | --------- |
|     | Visual    |     | Basic   | Projects highlighted |      | (see       | Figure    | 3.1), as  |
|     | well      | as  | Windows | Application          |      | as the     | template. | Later     |
|     | in        | the | book    | we will              | look | at some    | of        | the other |
templates.
| F I G U | R E | 3.1 |     |     |     |     |     |     |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- |
Team-LRN

| GettingStartedwithVB.NET |     |             |     |          |                     |     |     |        | 35  |
| ------------------------ | --- | ----------- | --- | -------- | ------------------- | --- | --- | ------ | --- |
| When                     | a   | new project | is  | created, | VB.NETautomatically |     |     | places |     |
all the filesassociated withyour new project within a folderof the
| same name. |     | So the | path | to  | your | new project |     | should | be  |
| ---------- | --- | ------ | ---- | --- | ---- | ----------- | --- | ------ | --- |
C:\ModelingFM\Test\. If you take a look at the contents of this
folder via Window Explorer, you will notice that several files and
subfolders have been created to contain all the elements of our
project. Visual Basic.NET applications that we build consist of
several files. We will learn more about some of these files in later
chapters. For right now, just be aware that programs consist of
several files in a folder. To later reopen the project for further
| development, |     | click on | the | file with | the | .sln extension. |     |     |     |
| ------------ | --- | -------- | --- | --------- | --- | --------------- | --- | --- | --- |
Let’stakealookattheVB.NETIDEthatshouldnowbevisible
| on your | screen | (see | Figure | 3.2). | Notice | that the | development |     |     |
| ------- | ------ | ---- | ------ | ----- | ------ | -------- | ----------- | --- | --- |
environment consists of several windows, which are all either
| dockable    | or  | free-floating, |         | allowing |      | you to | customize |         | the |
| ----------- | --- | -------------- | ------- | -------- | ---- | ------ | --------- | ------- | --- |
| environment |     | to your        | liking. | The      | form | in the | center,   | labeled |     |
Form1,iswherewewillactuallybuildthegraphicaluserinterface
| (GUI) for | our | program. |     |      |     |     |     |     |     |
| --------- | --- | -------- | --- | ---- | --- | --- | --- | --- | --- |
|           |     |          |     | Menu | Bar |     |     |     |     |
Across the top of the screen is the menu bar. Take some time to
| peruse | the menu | bar | and | become | familiar | with | the | types | of  |
| ------ | -------- | --- | --- | ------ | -------- | ---- | --- | ----- | --- |
commandsthatperformvariousactions.Manyofthesecommands
also have corresponding shortcuts, through either keystrokes or
menubariconsorboth.Asyouwillnodoubtdiscoverasyougain
experienceinprogramminginthe.NETIDE,thereareoftenseveral
| ways to | accomplish |     | the same | task. |     |     |     |     |     |
| ------- | ---------- | --- | -------- | ----- | --- | --- | --- | --- | --- |
Toolbox
Written vertically down the left side of the screen should be the
Toolboxbutton.Ifyoudonotseeit,clickontheToolboxiconinthe
upperright-handcorner.It’stheonewithahammerandwrenchin
an X-shaped design. When you open the Toolbox, you will see the
listsoftools,calledcontrols,thatyouseeinFigure3.2.Wewilloften
Team-LRN

36 IntroductiontoVB.NET
| F I G U | R E 3.2 |     |     |
| ------- | ------- | --- | --- |
beaddingcontrols,bydragginganddroppingthemintoourforms,
torapidlybuildprogramsandGUIs.Youmaywanttospendalittle
| time investigating | each     | of the tools before | you proceed. |
| ------------------ | -------- | ------------------- | ------------ |
|                    | Solution | Explorer            | Window       |
The Solution Explorer window, shown in the upper right corner,
enables you to access the different parts of your project. If the
Team-LRN

| GettingStartedwithVB.NET |     |     |     |     |     |     | 37  |
| ------------------------ | --- | --- | --- | --- | --- | --- | --- |
Solution Explorer window is not visible, click on the Solution
Explorericon;oronthemenubar,clickViewandSolutionExplorer.
| In our  | applications, | we  | almost   | always       | have several | forms | and |
| ------- | ------------- | --- | -------- | ------------ | ------------ | ----- | --- |
| classes | and program   |     | modules. | The Solution | Explorer     | gives | us  |
instant access to any part of our project at any time. To close the
SolutionExplorer,clicktheXbuttonintheupperright-handcorner.
|     |     | Properties |     | Window |     |     |     |
| --- | --- | ---------- | --- | ------ | --- | --- | --- |
InthelowerrightcorneristhePropertieswindow.Again,ifitisnot
visible,clickonthePropertieswindowicononthetoolbar,orselect
| View and | Properties | Window |     | from the | menu bar. |     |     |
| -------- | ---------- | ------ | --- | -------- | --------- | --- | --- |
Properties are attributes, like size and color, of the objects we
useinprograms.Sinceeachcontrol,ortool,fromourtoolboxisan
| object | and has its | own | set | of properties, | we can | see all | the |
| ------ | ----------- | --- | --- | -------------- | ------ | ------- | --- |
propertiesassociatedwitheachoftheminthiswindow.Youshould
familiarize yourself with the different properties associated with
thedifferentcontrolsasweusethemthroughoutthisbook.Theleft-
hand side of the Properties window column lists the individual
properties, and the right-hand column lists the value of each
property. You will need the Properties window to set the initial
| valuesof               | thesepropertiesat |     | designtime,andasyouwill |     |             | latersee, |     |
| ---------------------- | ----------------- | --- | ----------------------- | --- | ----------- | --------- | --- |
| we canchangeproperties |                   |     | at runtimeusing         |     | VB.NETcode. | Aswith    |     |
SolutionExplorer,wecanclosethePropertieswindowandreopen
| it from | either the | View | menu | or the menu | bar icon. |     |     |
| ------- | ---------- | ---- | ---- | ----------- | --------- | --- | --- |
AswewillseeinChapter7,other,nonvisibleobjectswecreate
in our programs will also have properties associated with them.
When we cannot see the objects, it gets slightly more difficult to
understandproperties.Forexample,infinance,acalloptioncould
beanobject.Anoptionobjectinourprogramwouldcertainlyhave
properties,likeanoptionsymbol,strikeprice,expirationdate,and
| implied | volatility. |     |     |     |     |     |     |
| ------- | ----------- | --- | --- | --- | --- | --- | --- |
Events
Besidesproperties,controlsalsohaveeventsassociatedwiththem.
An event is triggered when something happens to a control. The
Team-LRN

| 38  |     |     |     |     |     | IntroductiontoVB.NET |     |     |
| --- | --- | --- | --- | --- | --- | -------------------- | --- | --- |
button “click” event is probably the most easily understandable
exampleofanevent.Laterwewilllearnhowtoprogramthingsto
| happen | when | events | are | fired. |     |     |     |     |
| ------ | ---- | ------ | --- | ------ | --- | --- | --- | --- |
Methods
Objects,likecontrols,alsohavetoperformfunctionsoftheirown.It
isn’t usually enough that an object simply exists. After all, the
whole point of creating a control is that the object does something
useful.TheseadditionalfunctionsareknownasmethodsinVisual
| Basic.NET | terms. | Whereas |     | properties | are | thought | of as | nouns, |
| --------- | ------ | ------- | --- | ---------- | --- | ------- | ----- | ------ |
methods are often thought of as verbs. Later, we will learn how to
| create our | own | objects | and | add methods | to  | them. |     |     |
| ---------- | --- | ------- | --- | ----------- | --- | ----- | --- | --- |
|            |     | Visual  |     | Studio.NET  |     | Help  |     |     |
Thereisnowaythatanybookcanhopetocoverallthefeaturesof
VisualBasic.NETorallthepotentialinstancesyoumayuncoverfor
using them. Finding and solving new problems quickly is one of
thejoysofprogramming.Fortunately,VisualStudio.NETprovides
a vast array of help features. Knowing how to find what you need
in the Help files is one of the most valuable skills you can gain to
improve your expertise. Again, you should investigate the Help
| files on | your | own | and | become comfortable |     | accessing | the | Help |
| -------- | ---- | --- | --- | ------------------ | --- | --------- | --- | ---- |
indexandDynamicHelp.Mostoften,programmingquestionsthat
arise are covered extensively in the Help files, almost always with
code examples.
| CREATING |     | AN  | EXECUTABLE |     | PROGRAM |     |     |     |
| -------- | --- | --- | ---------- | --- | ------- | --- | --- | --- |
You will write many different applications as you go through this
| book. | Creating | an  | executable | program | allows | you | to run | your |
| ----- | -------- | --- | ---------- | ------- | ------ | --- | ------ | ---- |
application as a single .exe file from the Windows environment
without having to be in the VB.NET IDE. In order to create an
executable file, VB.NET programs must be compiled into machine
language.
| CompilingaVB.NETapplicationisatwo-stage |     |             |     |                |     |              | process.First, |     |
| --------------------------------------- | --- | ----------- | --- | -------------- | --- | ------------ | -------------- | --- |
| the program                             |     | is compiled |     | into Microsoft |     | Intermediate | Language       |     |
Team-LRN

GettingStartedwithVB.NET 39
(MSIL). Then second, another compiler translates this MSIL code
into a single, executable file in machine language. In this way,
Microsoft’s .NET framework provides language interoperability.
Programs that are written in different languages, such as C#, Perl,
orPython,canallbefirstcompiledintoMSIL.Sodifferentpartsofa
program,writtenindifferentlanguages,canbecombinedtocreate
a single program. In fact, any .NET-compliant language can be
compiled into MSIL in this way, and thus .NET is said to be
language-independent.
Step 5 Make sure your form, known by the default name
“Form1” in your project, is active by clicking on it.
Youcanchangethesizeoftheformbypullingonthe
highlighted corners or sides. This will automatically
cause the Size property of the form to change. Now,
in the Properties window, change the value of the
“Text”propertytoread“MyFirstVB.NETProgram”
without the quotation marks. When you press Enter,
you will see the title on the form change to the new
text.
Step 6 In the Toolbox, click on Label and “paint” a label on
your form by holding down the left mouse button
and dragging over the form.
Step 7 This new label is now known by the default name
Label1, as you can see in the Properties window.
Make surethe labelis selected,and in theProperties
window, change the Font property to Garamond,
Bold, size 36. Also, change the Text property to Buy
Low, Sell High. Change the TextAlign property to
MiddleCenter.
Your form should now look like the one shown in Figure 3.3.
Step 8 Now to run your program, click the Start button on
themenubar,orundertheDebugtab,clickStart.The
Start button is the one that looks like a blue arrow,
nexttothewordDebug.Yourprogramshouldtakea
fewsecondstocompile,andthenitwillrun.Youcan
close the program by clicking on the X.
Team-LRN

40 IntroductiontoVB.NET
F I G U R E 3.3
Step 9 In Windows Explorer you can find the executable
program Test.exe in the Test folder, subfolder bin.
The path to the file in its entirety should be
C:\ModelingFM\Test\bin\Test.exe. If you close
down the Visual Basic.NET IDE, you can run this
executable program by double-clicking it. Fur-
thermore, you can drag the Test.exe icon onto your
Windows desktop. You can even email it to your
friendssothattheyneverforgethowtomakemoney
in the markets.
Now let’s take a little deeper look at the VB.NET IDE.
Step 10 If you have not already done so, close the program,
so that you are back in the VB.NET IDE. In the
Solution Explorer window, click on the View Code
icon as shown in Figure 3.4.
Step 11 The Form1 code window will appear (see Figure
3.5). This is where we write VB.NET code that is
associated with the controls we place on Form1,
including code that runs when events happen, as
previously discussed.
Team-LRN

GettingStartedwithVB.NET 41
F I G U R E 3.4
F I G U R E 3.5
Team-LRN

42 IntroductiontoVB.NET
Inthecomboboxesacrossthetopofthecodewindow,clickon
Label1 in the left-hand combo box and open the list in the right-
handcombo box.Thisis a list of allthe eventsassociatedwith our
label,Label1.AllthecontrolsintheToolboxhaveeventsassociated
with them. When an event happens, we can add code to make
something happen.
Step 12 For example, select DoubleClick from the list of
eventsforLabel1.NoticethatVB.NETwritesastub
of the event code for us. In the event code routine,
type Label1.Text¼ “Sell High, Buy Low.” The
underscores you see below allow us to wrap long
lines of code onto the next line.
Private Sub Label1_DoubleClick(ByVal sender As Object, _
ByVal e As System.EventArgs) _
Handles Label1.DoubleClick
Label1.Text = "Sell High, Buy Low."
End Sub
Step 13 Run the program again. Notice that the program
runsthesameaspreviously.Butifyoudouble-click
on the label in the form, an entirely new way to
profit in the markets appears (see Figure 3.6).
F I G U R E 3.6
Team-LRN

GettingStartedwithVB.NET 43
SUMMARY
Visual Basic.NET makes every effort to provide us with the tools
| that simplify |     | and | speed | the | process | of creating | our own |
| ------------- | --- | --- | ----- | --- | ------- | ----------- | ------- |
applications, or solutions as they are known in VB.NET. If you
already program in a previous version of Visual Basic, you will
notice several similarities in the new.NET IDE. If you are new to
programming, you will be able to turn out professional-looking
| applications | even | while | you      | are learning |     | VB.NET.     |             |
| ------------ | ---- | ----- | -------- | ------------ | --- | ----------- | ----------- |
| Make         | sure | you   | practice | using        | the | Help files. | Practically |
everythingyouneedtoknowisincludedintheresomewhere.You
| might have | to  | dig for | it, but | it is in | there. |     |     |
| ---------- | --- | ------- | ------- | -------- | ------ | --- | --- |
Intheexampleprograminthischapter,welookedatthelabel
control and the properties and events associated with it. We even
| wrote a      | brief | statement | to     | change | the | text property | when the |
| ------------ | ----- | --------- | ------ | ------ | --- | ------------- | -------- |
| double-click | event | is        | fired. |        |     |               |          |
Team-LRN

| 44  |     |     | IntroductiontoVB.NET |     |
| --- | --- | --- | -------------------- | --- |
PROBLEMS
| 1. Where | does VB.NETstore | the | various files associated | with |
| -------- | ---------------- | --- | ------------------------ | ---- |
your program?
| 2. Where | willyoufindthecontrolsusedtocreate |     | agraphical |     |
| -------- | ---------------------------------- | --- | ---------- | --- |
user interface?
3. IfthePropertieswindowisclosed,howcanyoureopenit?
| 4. How  | do you create   | an executable | program? |     |
| ------- | --------------- | ------------- | -------- | --- |
| 5. What | are properties, | events, and   | methods? |     |
Team-LRN

| GettingStartedwithVB.NET |     |     |     |     | 45  |
| ------------------------ | --- | --- | --- | --- | --- |
| PROJECT                  | 3.1 |     |     |     |     |
CreateagraphicaluserinterfaceliketheonepicturedinFigure3.7.
UseatabcontrolwiththreetabpagesnamedStocks,Options,and
Futures.OntheOptionstabpage,place4comboboxeswithsorted
items, including 10 stock tickers, Put/Call, 12 expirations, and 10
strikes. Also, place labels on your tab forms with Fixed3D border
| style and | custom background | colors. | Name | the colored | labels |
| --------- | ----------------- | ------- | ---- | ----------- | ------ |
lblBidQty, lb1BidPrice, lb1AskPrice, lblAskQty, and lblLast. Try
| adding | some controls | and changing | the | fonts to | enhance the |
| ------ | ------------- | ------------ | --- | -------- | ----------- |
appearance and user-friendliness of your GUI. Also, on the Stocks
and Futures tab pages, add similar content for financial instru-
ments of these types. For right now, to keep things simple do not
| add any  | code to handle | any of the | events | associated | with the |
| -------- | -------------- | ---------- | ------ | ---------- | -------- |
| controls | on your form.  |            |        |            |          |
| PROJECT  | 3.2            |            |        |            |          |
Use buttons, group boxes, and radio buttons to create the GUI
pictured in Figure 3.8. The default checked property for each of
| F I G | U R E 3.7 |     |     |     |     |
| ----- | --------- | --- | --- | --- | --- |
Team-LRN

46 IntroductiontoVB.NET
| F I G | U R E 3.8 |     |
| ----- | --------- | --- |
yourOnbuttonsshouldbesettoTrue.Whenyouruntheprogram
andchecktheFalseradiobuttons,theTruebuttonsshouldturnoff
automaticallybecausetheyaregroupedtogether.Forrightnow,to
keepthingssimpledonotaddanycodetohandleanyoftheevents
| associated | with the controls | on your form. |
| ---------- | ----------------- | ------------- |
Team-LRN

| C     | H A | P T   | E R 4 |     |           |     |     |     |
| ----- | --- | ----- | ----- | --- | --------- | --- | --- | --- |
| Value |     | Types |       | and | Operators |     |     |     |
M
| ost | financial | programming |     | involves | making | mathematical |     |     |
| --- | --------- | ----------- | --- | -------- | ------ | ------------ | --- | --- |
calculations. As in algebra, we often use variables in computer
programs to hold different values we need for calculation. In this
| chapter,     | you | will learn | how | to declare | variables | and | perform |     |
| ------------ | --- | ---------- | --- | ---------- | --------- | --- | ------- | --- |
| calculations | in  | VB.NET.    |     |            |           |     |         |     |
| DECLARING    |     | VARIABLES  |     |            |           |     |         |     |
Toacomputer,primitiveorsimplevaluetypes,calledvariables,are
actual, physical spaces in memory that store data for use by our
program.Beforewecanuseavariable,weneedtodeclareitusing
theDimstatement.Thatis,wehavetotellthecomputertosetupa
| space in | memory |     | with a | specific name. | In  | programming, |     | the |
| -------- | ------ | --- | ------ | -------------- | --- | ------------ | --- | --- |
variable names we use are usually descriptive of the contents they
| hold. For | example,        |      | a program     | to analyze    |       | stock returns   |        | might |
| --------- | --------------- | ---- | ------------- | ------------- | ----- | --------------- | ------ | ----- |
| contain   | variables       | like | this:         |               |       |                 |        |       |
| Dim       | sglMondayClose, |      | sglStockPrice |               | As    | Single          |        |       |
| Dim       | dblCallDelta    |      | As Double     |               |       |                 |        |       |
| Dim       | strTicker       |      | As String     |               |       |                 |        |       |
| These     | lines           | of   | code set      | up variables, |       | physical        | places | in    |
| memory,   | that            | will | be known      | by the        | names | sglMondayClose, |        |       |
sglStockPrice, dblCallDelta, and strTicker. Furthermore, the types
of data that will go into each of these containers will be things
calledasingle,adouble,andastring.Single,double,andstringare
value types, which tell us what kind of data the variable can hold.
Here is a list of the different value types supported by VB.NET,
with descriptions:
47
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

| epyTeulaVdnanoitnevnoC |     |     | trohSsAstcartnoCmuNthsmiD |
| ---------------------- | --- | --- | ------------------------- |
gnimaNgnisUelpmaxE regetnIsAserahSmuNtnimiD elgniSsAecirPkcotSlgsmiD
| naelooBsAlleSyuBnlbmiD | elbuoDsAatleDllaClbdmiD | gnoLsAsedarTmuNgnlmiD             |                      |
| ---------------------- | ----------------------- | --------------------------------- | -------------------- |
| rahCsAhtnoMpxErhcmiD   | lamiceDsAravoCcedmiD    |                                   |                      |
|                        | etaDsAetaDpxEtdmiD      |                                   | gnirtSsArekciTrtsmiD |
| refiitnedI             |                         | %serahSmuNtnimiD &sedarTmuNgnlmiD |                      |
!ecirPkcotSlgsmiD
#atleDllaClbdmiD
@ravoCcedmiD
$rekciTrtsmiD
|     | ro  | ro ro ro                      | ro ro                       |
| --- | --- | ----------------------------- | --------------------------- |
|     |     | onllitstub,sregetnigiB.stib46 | oN.ylnosregetnillamS.stib61 |
semitdnasetadsdloH.stib46
sayllanretniderotS.stib61
|     | srebmunegraL.stib821 noisicerp-elbuoD.stib46 | oN.ylnosregetnI.stib23        | noisicerp-elgniS.stib23 |
| --- | -------------------------------------------- | ----------------------------- | ----------------------- |
|     |                                              | elbairavtniop-gnitaofl        | elbairavtniop-gnitaofl  |
|     |                                              | srebmunlamiced srebmunlamiced | srebmunlamiced          |
etoN
sedocretcarahC
| 1ro0rehtie 535,56ot0    |                      |                               | atadretcarahC              |
| ----------------------- | -------------------- | ----------------------------- | -------------------------- |
|                         |                      | 746,384,741,2ot846,384,741,22 | 83þE4.32/þot542E5.1        |
|                         |                      | 708,577,458,630,273,322,9ot   | forebmunehtnopudesabseiraV |
| dna9999/13/21ot1000/1/1 | E7.12/þot4232E0.52/þ | 808,577,458,630,273,322,92    |                            |
82þE9.7ot822E0.1
| egnaR retcarahcedocinUynA | 95:95:32ot00:00:0 |     |     |
| ------------------------- | ----------------- | --- | --- |
767,23ot867,232
| eslafroeurT |     |     | sretcarahc |
| ----------- | --- | --- | ---------- |
803þ
2/þ
refiitnedIhtiw
epyTeulaV
@lamiceD
|         | #elbuoD | %regetnI |                 |
| ------- | ------- | -------- | --------------- |
| naelooB |         |          | !elgniS $gnirtS |
&gnoL
| rahC |     |     | trohS |
| ---- | --- | --- | ----- |
etaD
48
Team-LRN

ValueTypesandOperators 49
Whenavariableofanytypeiscreated,itsdefaultvalueis0.We
can define or change the values of our variables this way:
sglMondayClose = 10.12
strTicker = "MMZR"
Alternatively, we could declare and define a variable in the same
line:
Dim sglStockPrice As Single = 4.92
InVisualBasic.NETallvariablesmustbedeclaredbeforethey
can be used. Later in the book, we will show you that this helps
avoid common programming errors.
CONSTANTS
If the value of a variable is not going to change over the life of our
program,weshoulddeclareitasaconstant,ratherthanavariable,
like this:
Const DIVISOR = 1.8
Declaring a value as a constant protects it against accidentally
being changed down the road.
VARIABLE SCOPE
Variables and constants can also be declared using an access
modifier. Access modifiers serve to specify the scope and
accessibility of the variable. The access modifiers are Friend,
Private, Protected, Protected Friend, and Public. Here is an
example:
Public strExchange As String
In later chapters, we will discuss access and scope in more
detail. For now, be aware that the scope of a variable refers to the
parts of a program that can access a variable. Not all variables are
accessible everywhere. Variables in Visual Basic.NETcan have the
following scope:
Team-LRN

| 50    |     |                                                   |                             |     | IntroductiontoVB.NET |     |
| ----- | --- | ------------------------------------------------- | --------------------------- | --- | -------------------- | --- |
| Scope |     |                                                   | Accessibilityor“Visibility” |     |                      |     |
| Class |     | Accessibleinwhatisknownasthedeclarationspaceofthe |                             |     |                      |     |
class
| Module |     | Accessibletoallfunctionsandproceduresdefinedinthe |     |     |     |     |
| ------ | --- | ------------------------------------------------- | --- | --- | --- | --- |
module
| GlobalorNamespace |     | Accessibleanywhereinaproject                     |     |     |     |     |
| ----------------- | --- | ------------------------------------------------ | --- | --- | --- | --- |
| Block             |     | Accessibleonlywithintheblockofcodeinwhichtheyare |     |     |     |     |
declared
Variablesshouldalwaysbedefinedwiththesmallestpossible
| scope. Variables | with | global | scope | can make | the | logic of an |
| ---------------- | ---- | ------ | ----- | -------- | --- | ----------- |
application extremely difficult to understand and make the reuse
andmaintenanceofyourcodemoredifficult.InaVisualBasic.NET
application, globalvariables should beused only when there is no
otherconvenientwaytosharedatabetweenpartsofyourprogram.
When global variables must be used, it is good practice to declare
them all in a single module, grouped by function. For now, just be
aware that not all variables are accessible from everywhere in our
applications. The access modifiers will limit the visibility of
variables.
| REPRESENTING |           | DATES         | AND | TIMES   |       |         |
| ------------ | --------- | ------------- | --- | ------- | ----- | ------- |
| When making  | financial | calculations, |     | we also | often | need to |
represent dates and times in our programs for things like interest
| accrual and | trade time   | stamps. |     |     |     |     |
| ----------- | ------------ | ------- | --- | --- | --- | --- |
| Dim         | dtMyDate     | As Date |     |     |     |     |
| dtMyDate    | = #01/02/03# |         |     |     |     |     |
VisualBasic.NETissensitivetotheculturaldifferencesindate
representation. For example, if you are working in the United
Kingdom and rerun the above example, the first four numbers are
interpreted as, the first of February rather than the American
| second of | January. |              |        |        |        |        |
| --------- | -------- | ------------ | ------ | ------ | ------ | ------ |
| OPTION    | STRICT   |              |        |        |        |        |
| An Option | Strict   | On statement | should | always | appear | in the |
declarations section of a module. Option Strict On prevents Visual
Basic.NETfrommakingimplicittypeconversionsthatmayinvolve
Team-LRN

| ValueTypesandOperators |     |     |     | 51  |
| ---------------------- | --- | --- | --- | --- |
loss of data. For purposes of demonstration in this book, however,
we will leave the default Option Strict Off. Just remember, in the
realworldyoushouldalwayshavetheOptionStrictOnstatement
| at the top | in your programs. |     |     |     |
| ---------- | ----------------- | --- | --- | --- |
STRUCTURES
Generally,whenagroupofdatafittogether,butconsistofdifferent
valuetypes,wemayprefertocreateourownvariabletype,calleda
structure. Visual Basic.NET allows us to create our own user-
defined value types using the Structure statement. Our structures
will generally contain more than one element, and each element
must be declared with an access modifier. Here is an example of a
| user-defined | data type called | QuoteData:             |           |        |
| ------------ | ---------------- | ---------------------- | --------- | ------ |
| Structure    | QuoteData        |                        |           |        |
|              | Public dtDate    | As Date                |           |        |
|              | Public dblOpen   | As Double              |           |        |
|              | Public dblHigh   | As Double              |           |        |
|              | Public dblLow    | As Double              |           |        |
|              | Public dblClose  | As Double              |           |        |
|              | Public lngVolume | As Long                |           |        |
| End          | Structure        |                        |           |        |
| We can       | then declare     | a variable of the type | QuoteData | in the |
| following    | way:             |                        |           |        |
| Dim          | qdStockPrice As  | QuoteData              |           |        |
Muchinthesamewaywereferencepropertiesofobjects,such
ascontrols,wecanreferencetheindividualelementsofastructure
| value type | like this:             |     |     |     |
| ---------- | ---------------------- | --- | --- | --- |
| Text1.Text | = qdStockPrice.dtDate  |     |     |     |
| Text2.Text | = qdStockPrice.dblOpen |     |     |     |
ENUMERATIONS
Enumerations are integer value types that have a limited set of
acceptable values. VB.NETallows us to create enumerations using
Team-LRN

| 52  |     |     |     |     |     | IntroductiontoVB.NET |     |     |
| --- | --- | --- | --- | --- | --- | -------------------- | --- | --- |
the Enum statement, the integer value type—byte, short, integer,
| long—and | the         | acceptable | values.  |     |     |     |     |     |
| -------- | ----------- | ---------- | -------- | --- | --- | --- | --- | --- |
| Enum     | TradeStatus |            | As Short |     |     |     |     |     |
Filled
Open
Partial
Canceled
Rejected
| End          | Enum    |                  |           |                   |     |        |            |     |
| ------------ | ------- | ---------------- | --------- | ----------------- | --- | ------ | ---------- | --- |
| We           | can use | this enumeration |           | by calling        | on  | one of | its member |     |
| names        | in code | as follows:      |           |                   |     |        |            |     |
| Dim          | myTrade | As TradeStatus   |           | = myTrade.Partial |     |        |            |     |
| Enumerations |         | make             | it easier | to understand     |     | the    | purpose    | of  |
variableswithalimitednumberofallowablevaluesasopposedto
| the integer | values. |     |     |     |     |     |     |     |
| ----------- | ------- | --- | --- | --- | --- | --- | --- | --- |
OPERATORS
VisualBasic.NEThasawealthofoperatorstohandlemathematical
calculations and other logical operations. As we go through the
book, we will be making extensive use of operators as we write
programs.Mostofthemareself-explanatory,butsomemaynotbe.
You can use this section as a reference as they come up over the
| course     | of the book. |           |     |     |     |     |     |     |
| ---------- | ------------ | --------- | --- | --- | --- | --- | --- | --- |
| Arithmetic |              | Operators |     |     |     |     |     |     |
Math
| Operator |                | Name | Example   |                                 |     | Description |     |     |
| -------- | -------------- | ---- | --------- | ------------------------------- | --- | ----------- | --- | --- |
| ^        | Exponentiation |      | x^y       | Raisesxtothepowerofy            |     |             |     |     |
| -        | Negation       |      | -y        | Negatesy                        |     |             |     |     |
| (cid:1)  | Multiplication |      | x(cid:1)y | Multipliesxandy                 |     |             |     |     |
| /        | Division       |      | x/y       | Dividesxbyyandreturnsafloating- |     |             |     |     |
pointresult
| \   | Integerdivision |     | x\y | Dividesxbyyandreturnsaninteger |     |     |     |     |
| --- | --------------- | --- | --- | ------------------------------ | --- | --- | --- | --- |
result
| Mod | Modulos |     | xMody | Dividesxbyyandreturnsthe |     |     |     |     |
| --- | ------- | --- | ----- | ------------------------ | --- | --- | --- | --- |
remainder
| þ   | Addition    |     | xþy | Addsxandy         |     |     |     |     |
| --- | ----------- | --- | --- | ----------------- | --- | --- | --- | --- |
| 2   | Subtraction |     | x2  | y Subtractsyfromx |     |     |     |     |
Team-LRN

ValueTypesandOperators 53
| Comparison |     | Operators |     |     |     |     |
| ---------- | --- | --------- | --- | --- | --- | --- |
Comparison
| Operator   |     | Description        |     |                    |     | Example          |
| ---------- | --- | ------------------ | --- | ------------------ | --- | ---------------- |
| ¼          |     | Equal              |     | sglStockPrice¼5.67 |     |                  |
| ,.         |     | Notequal           |     | intNumShares,.     |     | 500              |
| .          |     | Greaterthan        |     | dblCallDelta.      |     | .5               |
| ,          |     | Lessthan           |     | intVolume,         |     | 10000            |
| .¼         |     | Greaterthanorequal |     | sglClosePrice.¼    |     | 52.50            |
| ,¼         |     | Lessthanorequal    |     | sglHighPrice,¼     |     | sglPreviousClose |
| Assignment |     | Operators          |     |                    |     |                  |
Assignment
| Operator |     | Example | Explanation |     |     | NewValue |
| -------- | --- | ------- | ----------- | --- | --- | -------- |
AssumethatsglPrice510.00andstrTicker5“PKR”
| þ¼  | sglPriceþ¼3    |     | sglPrice¼sglPriceþ3    |     |     | sglPrice¼13.00 |
| --- | -------------- | --- | ---------------------- | --- | --- | -------------- |
| -¼  | sglPrice2¼2.00 |     | sglPrice¼sglPrice22.00 |     |     | sglPrice¼8.00  |
(cid:1)¼ sglPrice(cid:1)¼1.15 sglPrice¼sglPrice(cid:1) 1.15 sglPrice¼11.5
| /¼      | sglPrice/¼2    |     | sglPrice¼sglPrice/2     |           |      | sglPrice¼5       |
| ------- | -------------- | --- | ----------------------- | --------- | ---- | ---------------- |
| \¼      | sglPrice\¼3    |     | sglPrice¼sglPrice\3     |           |      | sglPrice¼3       |
| ^¼      | sglPrice^¼.2   |     | sglPrice                | ¼sglPrice | ^ .2 | sglPrice¼1.5849  |
| &¼      | strTicker&¼“Q” |     | strTicker¼strTicker&“Q” |           |      | strTicker¼“PKRQ” |
| Logical | Operators      |     |                         |           |      |                  |
Logical
| Operator |                               | Description |     |     |           | Example       |
| -------- | ----------------------------- | ----------- | --- | --- | --------- | ------------- |
| And      | EvaluatestoTrueonlyifboth     |             |     |     | dblPrice. | 55AnddblPrice |
|          | conditionsaretrue             |             |     |     | ,         | 56            |
| AndAlso  | EvaluatestoTrueonlyifboth     |             |     |     | dblPrice. | 55AndAlso     |
|          | conditionsaretrue             |             |     |     | dblPrice, | 56            |
| Not      | Reversesornegatesthemeaningof |             |     |     |           |               |
anoperand
| Or     | EvaluatestoTrueifoneorboth       |     |     |     | dblPrice.55OrdblPrice, |               |
| ------ | -------------------------------- | --- | --- | --- | ---------------------- | ------------- |
|        | conditionsaretrue                |     |     |     | 40                     |               |
| OrElse | EvaluatestoTrueifoneorboth       |     |     |     | dblPrice.              | 55OrElse      |
|        | conditionsaretrue                |     |     |     | dblPrice,              | 40            |
| Xor    | Ifbotharetrueorfalse,evaluatesto |     |     |     | dblPrice.              | 55XordblPrice |
|        | False                            |     |     |     | ,                      | 60            |
Team-LRN

| 54            |           |     |     | IntroductiontoVB.NET |
| ------------- | --------- | --- | --- | -------------------- |
| Concatenation | Operators |     |     |                      |
Concatenation
| Operator |                              | Description |     | Example       |
| -------- | ---------------------------- | ----------- | --- | ------------- |
| &        | Concatenatesorbindsanumberof |             |     | strTick¼      |
|          | stringstogether.(Preferred)  |             |     | strSymbol&“Q” |
| þ        | Concatenatesorbindsanumberof |             |     | strTick¼      |
|          | stringstogether              |             |     | strSymbolþ“Q” |
| STOCK    | INDEX FUTURES                |             |     |               |
ThemostwidelytradedequityindexfuturescontractintheUnited
States is the S&P 500. The futures contracts on the S&P 500 index
aretradedattheChicagoMercantileExchange(CME).Thevalueof
the contract is $250 times the futures price. The CME’s “e-Mini”
contract is a smaller, electronically traded version of the original
pit-tradedcontractandhasavalueof$50timesthefuturesprice.So
ifthefuturescontractwerevaluedat1000,itwouldhaveanotional
value of $250,000 and the e-Mini a notional value of $50,000. The
CME also trades options on these futures contracts. The Chicago
BoardOptionsExchangetradesoptionsonthecashS&P500index.
The S&P 500 index consists of 500 stocks, each selected for its
market size, liquidity, and industry group. Also, the S&P 500 is a
| market | value–weighted | index | where the market | value of an |
| ------ | -------------- | ----- | ---------------- | ----------- |
individual stock is the stock price times the number of shares
outstanding.Eachstock’sweightintheindexthenisproportionate
toitsmarketvalue.Theweightsfortheindividualstockschangeas
their respective prices rise and fall relative to other stocks in the
index (Kolb, 1997, p. 334). Alternatively, an index could be price-
weighted, where the index weights are proportional to the stock
prices.TheDowJonesIndustrialAverageisanexampleofaprice-
| weighted | index. |     |     |     |
| -------- | ------ | --- | --- | --- |
Hereisanexampleofaformulaforthecalculationofthecash
| value of | a market value–weighted |     | index: |     |
| -------- | ----------------------- | --- | ------ | --- |
|          |                         |     | !      |     |
P500NP
|     | S&P | 500 ¼ | i¼1 i i (cid:2)10 |     |
| --- | --- | ----- | ----------------- | --- |
O:V:
Team-LRN

ValueTypesandOperators 55
where:
O.V.¼original valuation
N ¼number of shares outstanding for the ith firm
i
P ¼price per share of the ith firm
i
Let’s build a simple program that will calculate the price of a
market value–weighted stock index. In this example, we will
demonstratethesimplesttypeofcomputerprogram,onethatuses
procedural programming techniques. Procedural programs are
thosewrittenaslistsofinstructionsdividedintosectionsorunitsof
code called the main block, plus subroutines and functions, which
we will look at in Chapter 6. Procedural programming works well
for small projects because it is very intuitive. Moreover, machine
code is procedural, and so compiling procedural code is very
efficient.
Step 1 Open the Visual Basic.Net IDE. For this exercise we
aregoingtocreateanewconsoleapplication,soclick
ontheiconnamedConsoleApplicationandnamethe
project “IndexFutures.” A console application is the
simplest type of VB.NET program and contains only
text input and output, as you will see. The interface
will be a command, or console, window.
Step 2 When the project IDE opens up, you will be
presented only with a window in which to write
code. Within the Sub main() procedure, we need to
create the necessary variables and algorithms to
make our calculations.
Forsimplicity,wewillassumethattherearetwostocksinthis
index,knownasstockAandstockB,andthatitisamarketvalue–
weighted index like the S&P 500. Also, to keep things simple, we
will not add Option Strict to our code.
Step3 Now,let’saddsomecodetocalculatetheindexvalue.
To do this, we will need to declare and define some
variables and use some mathematical operators
according to the formula.
Team-LRN

56 IntroductiontoVB.NET
Module Module1
Sub Main()
Const ORIGINALVALUE = 2000 ’ Index original value
Dim dblIndexValue As Double
Dim intSharesA% = 1000 ’ 1000 shares of A outstanding
Dim intSharesB% = 2000 ’ 2000 shares of B outstanding
Console.WriteLine("Please enter the price of stock A:")
Dim dblPriceA# = Console.ReadLine
Console.WriteLine("Please enter the price of stock B:")
Dim dblPriceB# = Console.ReadLine
’ Calculate the value of the index and print it to the screen.
dblIndexValue = (((dblPriceA * intSharesA) + (dblPriceB * _
intSharesB)) / ORIGINALVALUE) * 10
Console.WriteLine(‘The value of the index is’ & dblIndexValue)
End Sub
End Module
You will notice in the code above, we have included some
sample values for the Original Value and the number of shares
outstanding. We will allow the user to enter the prices of stocks A
andBwhentheConsole.ReadLinestatementsareexecuted.Notice
that we have used the double value type for our variables using
both the type name and the identifier for illustration purposes.
Also,wehavedeclaredtheoriginalvalueoftheindexasaconstant.
Step 4 Once your code is finished, run the program by
selecting from the menu bar Debug . Start Without
Debugging. This will cause the program to pause
before it closes the console window so we can
examine the results of our program (see Figure 4.1).
Let’s augment this program to calculate the fair value of a
futurescontractonthisindex.Wecancalculatethefairvalueusing
the cost-of-carry model (Kolb, 1997, p. 340):
(cid:1) T (cid:2) X n (cid:1) t i (cid:2)
F ¼ S 1þR (cid:3) D 1þR
0,t 0 i
360 360
i¼1
where:
F ¼indexfuturespriceattime0andexpirestdays
0,t
in the future
S ¼value of the market value–weighted cash
0
index at time 0
R¼interest rate
T¼number of days till futures expiration
Team-LRN

ValueTypesandOperators 57
F I G U R E 4.1
D ¼amount of the ith dividend
i
t ¼number of days the ith dividend will be
i
invested from receipt until futures expiration
Step 5 Change the code so as to calculate the fair value of a
futures contract.
Module Module1
Sub Main()
Const ORIGINALVALUE = 2000 ’ Index original value
Dim dblFairValue, dblIndexValue As Double
Dim dblDaysTillExp As Double = 90 ’ 90 days till expiration
Dim dblRate As Double = 0.10 ’ 10% interest rate
Dim intSharesA% = 1000 ’ 1000 shares of A outstanding
Dim intSharesB% = 2000 ’ 2000 shares of B outstanding
Dim dblDivA# = 2.00 ’ 2.00 dividend 40 days from now on A
Dim dblDivB# = 1.00 ’ 1.00 dividend 50 days from now on B
Dim intDaysDivAInvested% = 50
’ ( 90 - 40 ) = 50 days to invest dividend
Dim intDaysDivBInvested% = 40
’ ( 90 - 50 ) = 40 days to invest dividend
Console.WriteLine("Please enter the price of stock A:")
Dim dblPriceA# = Console.ReadLine
Console.WriteLine("Please enter the price of stock B:")
Dim dblPriceB# = Console.ReadLine
’ Calculate the fair value and print it to the screen.
dblIndexValue = (((dblPriceA * intSharesA) + (dblPriceB * _
intSharesB)) / ORIGINALVALUE) * 10
dblFairValue = (dblIndexValue) * (1 + dblRate * dblDaysTillExp _
/ 360) - (dblDivA * (1 + dblRate * _
Team-LRN

| 58  |                        |                     |                       |     | IntroductiontoVB.NET |      |     |
| --- | ---------------------- | ------------------- | --------------------- | --- | -------------------- | ---- | --- |
|     |                        | intDaysDivAInvested |                       | /   | 360) + dblDivB       | * (1 | + _ |
|     |                        | dblRate             | * intDaysDivBInvested |     | / 360))              |      |     |
|     | Console.WriteLine("The |                     | fair value            | is" | & dblFairValue)      |      |     |
End Sub
| Step     | 6      |             |             |           |         |          |       |
| -------- | ------ | ----------- | ----------- | --------- | ------- | -------- | ----- |
|          | Run    | the program | by          | selecting | from    | the menu | bar   |
|          | Debug  | . Start     | Without     | Debugging | (see    | Figure   | 4.2). |
| Although | we are | finished    | programming |           | for the | chapter, | let’s |
takealittlemorein-depthlookatthefairvalueofafuturescontract
| on a stock | index. |     |     |     |     |     |     |
| ---------- | ------ | --- | --- | --- | --- | --- | --- |
No-arbitrageconditionspreventthevalueoftheindexfutures
contract from moving too far away from the fair value. Cash-and-
carry strategies prevent the futures price from getting too high
relative to the cash stocks, and reverse cash-and-carry arbitrage
strategiespreventitfromgettingtoolow.Identifyingopportunities
for cash-and-carry arbitrage, however, necessitates the technologi-
calinfrastructuretomonitorthe500stocksinrealtimeandexecute
trades simultaneously. These types of trading strategies are often
| referred | to as “program |     | trading” | since | they | are computer- |     |
| -------- | -------------- | --- | -------- | ----- | ---- | ------------- | --- |
generated.
Inthefollowingtwoexamplesillustratingindexarbitrage,we
assume that the prices of the underlying stocks A and B do not
change over the 90 days, although the profit or loss does not in
either case depend on the stock prices at expiration. Rather, the
| F I | G U R E 4.2 |     |     |     |     |     |     |
| --- | ----------- | --- | --- | --- | --- | --- | --- |
Team-LRN

| ValueTypesandOperators |     |     |     |     |     |     |     | 59  |
| ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
profit arises from a discrepancy between the futures price and its
| fair value | on      | day | 0 (Kolb, | 1997, p. 342). |        |      |             |      |
| ---------- | ------- | --- | -------- | -------------- | ------ | ---- | ----------- | ---- |
| The        | futures |     | price    | must be equal  | to the | cash | index price | plus |
the charges to carry the cash index forward to expiration (Kolb,
1997, p. 71). The carrying charge is the interest lost by being long
theunderlyingstocks.Ifthepricesdonotfallinlinewiththecostof
carry, a trader may attempt a cash-and-carry or reverse cash-and-
carry arbitrage.
|     |     | Cash-and-Carry |     |     | Arbitrage |     |     |     |
| --- | --- | -------------- | --- | --- | --------- | --- | --- | --- |
A cash-and-carry arbitrage strategy involves buying the stock and
selling the futurescontract in a similarbut oppositefashion (Kolb,
| 1997, | p. 343). | Here | we  | replicate the | index |     | by weighting | our |
| ----- | -------- | ---- | --- | ------------- | ----- | --- | ------------ | --- |
portfoliowiththreepartsstockB,$750,andtwopartsstockA,$500,
| Time  |                           |     | CashMarket |     |     |                        | FuturesMarket |     |
| ----- | ------------------------- | --- | ---------- | --- | --- | ---------------------- | ------------- | --- |
| 0days | Borrow$1250for90daysat10% |     |            |     |     | Sell1futurescontractat |               |     |
|       | Interestowedwillbe$31.25  |     |            |     |     |                        | 1285.00       |     |
Buy5sharesofstockAat$100
Buy10sharesofstockBat$75
| 40days | Receive$2.00dividendoneachshareof |     |     |     |     |     |     |     |
| ------ | --------------------------------- | --- | --- | --- | --- | --- | --- | --- |
stockA,totaling$10
Investproceedsfor50daysat10%
| 50days | Receive$1.00dividendoneachshareof |     |     |     |     |     |     |     |
| ------ | --------------------------------- | --- | --- | --- | --- | --- | --- | --- |
stockB,totaling$10
Investproceedsfor40daysat10%
| 90days | Sell5sharesofstockAat$100        |                            |     |     |     | Buy1futurescontractat |                         |     |
| ------ | -------------------------------- | -------------------------- | --- | --- | --- | --------------------- | ----------------------- | --- |
|        | Sell10sharesofstockBat$75        |                            |     |     |     |                       | fairvalueatexpirationof |     |
|        | Receivetotalproceedsfrominvested |                            |     |     |     |                       | 1250,whichisthespot     |     |
|        |                                  | dividendsof$10.14and$10.11 |     |     |     |                       | indexvalue              |     |
Totalproceedsare$1270.25
Repaydebtplusinterestof$1281.25
| P&L | Loss:$11.00 |     |     |     |     | Profit:$35.00 |     |     |
| --- | ----------- | --- | --- | --- | --- | ------------- | --- | --- |
Totalprofitof$35.002$11.00¼$24.00
|     | Reverse |     | Cash-and-Carry |     |     | Arbitrage |     |     |
| --- | ------- | --- | -------------- | --- | --- | --------- | --- | --- |
Areversecash-and-carryarbitrageopportunityinvolvessellingthe
underlying stock and buying the futures contract in a similar but
| opposite | fashion |     | (Kolb, | 1997, p. 343). |     |     |     |     |
| -------- | ------- | --- | ------ | -------------- | --- | --- | --- | --- |
Team-LRN

| 60    |                           |            |     |     | IntroductiontoVB.NET  |     |     |
| ----- | ------------------------- | ---------- | --- | --- | --------------------- | --- | --- |
| Time  |                           | CashMarket |     |     | FuturesMarket         |     |     |
| 0days | Sell5sharesofstockAat$100 |            |     |     | Buy1futurescontractat |     |     |
|       | Sell10sharesofstockBat$75 |            |     |     | 1255.00               |     |     |
Investproceedsof$1250for90daysat
10%
Interestearnedwillbe$31.25
| 40days | Borrow$10.00for50daysat10% |     |     |     |     |     |     |
| ------ | -------------------------- | --- | --- | --- | --- | --- | --- |
PaydividendonstockA
Interestowedwillbe$0.14
| 50days | Borrow$10.00for40daysat10% |     |     |     |     |     |     |
| ------ | -------------------------- | --- | --- | --- | --- | --- | --- |
PaydividendonstockB
Interestowedwillbe$0.11
90days Buyback5sharesofstockAat$100 Sell1futurescontractatfair
|     | Buyback10sharesofstockBat$75  |     |     |     | valueatexpirationof1250, |     |     |
| --- | ----------------------------- | --- | --- | --- | ------------------------ | --- | --- |
|     | Repaydebtplusinterestof$20.25 |     |     |     | whichisthespotindex      |     |     |
|     | Receiveinterestof$31.25       |     |     |     | value                    |     |     |
| P&L | Profit:$11.00                 |     |     |     | Loss:$5.00.              |     |     |
TotalProfitof$11.002$5.005$6.00
SUMMARY
In this chapter you have been exposed to all the different variable
| types      | available | in  | Visual Basic.NET. | Also, | you | should        | now |
| ---------- | --------- | --- | ----------------- | ----- | --- | ------------- | --- |
| understand | how       | to  | declare variables | using | the | Dim statement |     |
and the various identifiers and access modifiers as well as how
| to define | them. | Good | programmers | will | also | understand | the |
| --------- | ----- | ---- | ----------- | ---- | ---- | ---------- | --- |
importance of the Option Strict On, though for simplicity’s sake
we will neglect it in this book. Also, our variable naming con-
vention requires that we add prefixes to our variable names that
indicate the data type of the variable. Variable names should
also describe something about the nature of the value, such as
dblStockPrice.
Further, we investigated the different operators available to
programmersinVB.NETandlookedathowsomeofthemcouldbe
usedinthefinancialmarkets.Ourexampleconsistedofcalculating
the cash value of a stock index and the fair value of a futures
| contract | on that | index. |     |     |     |     |     |
| -------- | ------- | ------ | --- | --- | --- | --- | --- |
Team-LRN

| ValueTypesandOperators |     |     |     |     |     |     | 61  |
| ---------------------- | --- | --- | --- | --- | --- | --- | --- |
PROBLEMS
| 1. What | is a   | variable, | and | what   | is a constant? |     |     |
| ------- | ------ | --------- | --- | ------ | -------------- | --- | --- |
| 2. When | should | you       | use | Option | Strict?        |     |     |
3. Write a line of code that would declare a variable to hold
| the value | of  | the | gamma | of an | option. |     |     |
| --------- | --- | --- | ----- | ----- | ------- | --- | --- |
4. Writealineofcodethatwouldcalculatetheaverageoffive
| daily                  | returns  | known         |                 | as dblMonReturn, |                    | dblTuesReturn, |      |
| ---------------------- | -------- | ------------- | --------------- | ---------------- | ------------------ | -------------- | ---- |
| dblWedReturn,          |          |               | dblThursReturn, |                  | and dblFriReturn.  |                |      |
| 5. What                | is a     | concatenation |                 | operator?        | What               | is the value   | of a |
| string                 | variable |               | known           |                  | as strOptionSymbol |                | if   |
| strOptionSymbol¼“INTC” |          |               |                 |                  | & “ ” & “Sep”      | & “ ” & “50”?  |      |
Team-LRN

| 62      |     |     |     |     |     | IntroductiontoVB.NET |     |     |
| ------- | --- | --- | --- | --- | --- | -------------------- | --- | --- |
| PROJECT | 4.1 |     |     |     |     |                      |     |     |
CreateaVB.NETconsoleapplicationthatacceptsfivedailyclosing
stock prices from the user and calculates the mean and standard
deviationofthestock’slogreturns(seeFigure4.3).Theformulafor
| the | log return is |     |     |         |         |     |     |     |
| --- | ------------- | --- | --- | ------- | ------- | --- | --- | --- |
|     |               |     |     | (cid:1) | (cid:2) |     |     |     |
S i
|     |     |     | r   | ¼ ln |     |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- |
i
S i(cid:3)1
| Of  | course, the equations |     | for | mean and | standard | deviation |     | are |
| --- | --------------------- | --- | --- | -------- | -------- | --------- | --- | --- |
sffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffi
|     |       | n   |     |       |           |     | n                     |     |
| --- | ----- | --- | --- | ----- | --------- | --- | --------------------- | --- |
|     | 1X    |     |     |       |           | 1 X |                       |     |
|     | m ¼   | r   |     | s     | ¼         |     | (r (cid:3)rr(cid:1))2 |     |
|     | r;t,T | i   | and | r;t,T |           |     | i                     |     |
|     | n     |     |     |       | n(cid:3)1 |     |                       |     |
|     |       | i¼1 |     |       |           | i¼1 |                       |     |
Sincewewon’tcoverfunctionsuntillaterinthebook,here’sahint.
| We  | can calculate | the | natural | log | using VB.NET’s |     | built-in | log |
| --- | ------------- | --- | ------- | --- | -------------- | --- | -------- | --- |
function.
|     | dblTuesReturn | =   | Math.log( | dblTuesPrice |     | /   | dblMonPrice | )   |
| --- | ------------- | --- | --------- | ------------ | --- | --- | ----------- | --- |
Also, the square root can be found by raising the value to the 0.5
^
| power | using the | operator. |     |     |     |     |     |     |
| ----- | --------- | --------- | --- | --- | --- | --- | --- | --- |
Besuretonameyourvariablesusingthenamingconventions.
| F   | I G U R E | 4.3 |     |     |     |     |     |     |
| --- | --------- | --- | --- | --- | --- | --- | --- | --- |
Team-LRN

ValueTypesandOperators 63
| PROJECT | 4.2 |     |
| ------- | --- | --- |
TocalculatethevalueoftheDowJonesIndustrialAverage,aprice-
| weighted index, | the equation | is  |
| --------------- | ------------ | --- |
P30
P i
DJIA ¼ i¼1
divisor
FuturescontractsontheDJIAtradeattheChicagoBoardofTrade.
Create a console application that calculates the fair value of a
two-stock,price-weightedindexaccordingtothisformula.Assume
thatthetwostocks,AandB,arepricedat100and75,respectively,
andpaydividendsintheamountsandtimesshowninthechapter
| (Kolb, 1997, p. | 330). |     |
| --------------- | ----- | --- |
Team-LRN

This page intentionally left blank.
Team-LRN

|     | C H     | A P T E | R 5        |     |     |     |     |
| --- | ------- | ------- | ---------- | --- | --- | --- | --- |
|     | Control |         | Structures |     |     |     |     |
T
he code we wrote in Chapter 4 was all linear, or sequential, in
nature. That is, lines of code were executed in order, one after the
other, till the end of the program. Although this is fine for very
short tasks, to tackle more complex situations, we will need to
employ control structures, which involve the use of program flow
statements.Programflowstatementsfallintooneoftwocategories:
^ Selection structures. Conditional, or decision statements, in
whichcodeisexecutedbasedonwhetherornotacondition
|     | is  | met |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
^ Repetition structures. Looping statements, in which code is
|           | executed  | repeatedly | either        | a number  | of  | times | or until a |
| --------- | --------- | ---------- | ------------- | --------- | --- | ----- | ---------- |
|           | condition | is         | met           |           |     |       |            |
| SELECTION |           | STRUCTURES |               |           |     |       |            |
|           |           | If ...     | Then ... Else | Statement |     |       |            |
TheIf...Then...Elsestatementletsussay,ineffect,“Ifthisistrue,
then do this; otherwise, do that.” The logic couldn’t be more
| intuitive.       |                  | The following | example     | illustrates   |     | the use | of the |
| ---------------- | ---------------- | ------------- | ----------- | ------------- | --- | ------- | ------ |
| If...Then...Else |                  | structure.    |             |               |     |         |        |
|                  | If dblStockPrice |               | > 55 OrElse | dblStockPrice |     | < 40    | Then   |
Console.WriteLine("SELL!!!")
Else
Console.WriteLine("HOLD")
|     | End | If  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
65
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

| 66  |     |     |     |     |     | IntroductiontoVB.NET |
| --- | --- | --- | --- | --- | --- | -------------------- |
Intheexample,thestatementsfollowingtheIfareexecutedonlyif
theexpressionevaluates toTrue,that isifthe stockpriceisgreater
than 55 or less than 40. The Else block of code executes if the
expression evaluates to False. So in this case, if the stock price is
between40and55,wewillhold.TheexpressionusedinIf...Then
isaBooleanexpression,trueorfalse.TheuseoftheElseblockinan
| If statement | is  | optional.  |     |      |           |     |
| ------------ | --- | ---------- | --- | ---- | --------- | --- |
|              |     | The Select |     | Case | Statement |     |
If...Then...Else
| The Select | Case | structure | is  | very similar | to the |     |
| ---------- | ---- | --------- | --- | ------------ | ------ | --- |
structure, but it is much more efficient and makes our code much
| more readable |     | if there | are | several | branches | to the decision |
| ------------- | --- | -------- | --- | ------- | -------- | --------------- |
structure.IntheSelectCasestructurewecanincludeanunlimited
numberofclauses.Let’slookatanexamplethatnotonlyillustrates
the logic statements within a Select Case framework, but also
| demonstrates |     | how to build |     | a histogram | of log | returns: |
| ------------ | --- | ------------ | --- | ----------- | ------ | -------- |
Dim intBin1, intBin2, intBin3, intBin4, intBin5, intBin6 As Integer
| Dim    | dblDailyReturn | As              | Double | = Math.Log( | 51 / 50 | )   |
| ------ | -------------- | --------------- | ------ | ----------- | ------- | --- |
| Select | Case           | dblDailyReturns |        |             |         |     |
|        | Case           | Is < -.02       |        |             |         |     |
|        |                | intBin1         | += 1   |             |         |     |
|        | Case           | -.02 To         | -.01   |             |         |     |
|        |                | intBin2         | += 1   |             |         |     |
|        | Case           | -.01 To         | 0      |             |         |     |
|        |                | intBin3         | += 1   |             |         |     |
Case 0 To.01
|     |     | intBin4 | += 1 |     |     |     |
| --- | --- | ------- | ---- | --- | --- | --- |
Case .01 To.02
|     |      | intBin5  | += 1 |     |     |     |
| --- | ---- | -------- | ---- | --- | --- | --- |
|     | Case | Is > .02 |      |     |     |     |
|     |      | intBin6  | += 1 |     |     |     |
Case Else
|     |        | MsgBox | "Error." |     |     |     |
| --- | ------ | ------ | -------- | --- | --- | --- |
| End | Select |        |          |     |     |     |
Sincethenaturallogof(51/50)is0.0198,thevalueofintBin5
will be incremented by 1. The Case Else clause at the end of the
structure is optional. Also, multiple conditions are evaluated
separately with a logical OR as opposed to an AND, so it’s best to
Team-LRN

| ControlStructures |     |     |     |     |     | 67  |
| ----------------- | --- | --- | --- | --- | --- | --- |
keep Select Case logic as simple as possible. Let’s look at another
| example | evaluating | strings.   |         |     |                  |           |
| ------- | ---------- | ---------- | ------- | --- | ---------------- | --------- |
| Call    | and        | put option | symbols |     | include a strike | price and |
expiration month. The second-to-last letter in the symbol denotes
themonthofexpiration,andthelasttermdenotestheprice.So,for
| example, | GEKD | would | be the | symbol | for the General | Electric |
| -------- | ---- | ----- | ------ | ------ | --------------- | -------- |
November20.00calls.GERTwouldbetheJune17.50puts.Wewill
have more examples using option symbols later in the book, but
hereisaSelectCasestructureusingthechardatatypetodetermine
| the month | of expiration: |           |               |     |     |     |
| --------- | -------------- | --------- | ------------- | --- | --- | --- |
| Dim       | chrMonth       | As Char   | =             | "D" |     |     |
| Dim       | strMonth       | As String |               |     |     |     |
| Select    | Case           | chrMonth  |               |     |     |     |
|           | Case           | "A", "a", | "M",          | "m" |     |     |
|           |                | strMonth  | = "January"   |     |     |     |
|           | Case           | "B", "b", | "N",          | "n" |     |     |
|           |                | strMonth  | = "February"  |     |     |     |
|           | Case           | "C", "c", | "O",          | "o" |     |     |
|           |                | strMonth  | = "March"     |     |     |     |
|           | Case           | "D", "d", | "P",          | "p" |     |     |
|           |                | strMonth  | = "April"     |     |     |     |
|           | Case           | "E", "e", | "Q",          | "q" |     |     |
|           |                | strMonth  | = "May"       |     |     |     |
|           | Case           | "F", "f", | "R",          | "r" |     |     |
|           |                | strMonth  | = "June"      |     |     |     |
|           | Case           | "G", "g", | "S",          | "s" |     |     |
|           |                | strMonth  | = "July"      |     |     |     |
|           | Case           | "H", "h", | "T",          | "t" |     |     |
|           |                | strMonth  | = "August"    |     |     |     |
|           | Case           | "I", "i", | "U",          | "u" |     |     |
|           |                | strMonth  | = "September" |     |     |     |
|           | Case           | "J", "j", | "V",          | "v" |     |     |
|           |                | strMonth  | = "October"   |     |     |     |
|           | Case           | "K", "k", | "W",          | "w" |     |     |
|           |                | strMonth  | = "November"  |     |     |     |
|           | Case           | "L", "l", | "X",          | "x" |     |     |
|           |                | strMonth  | = "December"  |     |     |     |
| End       | Select         |           |               |     |     |     |
Since the value of chrMonth is “D,” the value of strMonth will be
set to “April.”
Team-LRN

| 68         |     |     |            |     |     |     |     | IntroductiontoVB.NET |     |
| ---------- | --- | --- | ---------- | --- | --- | --- | --- | -------------------- | --- |
| REPETITION |     |     | STRUCTURES |     |     |     |     |                      |     |
VisualBasic.NETprovidesanumberofdifferenttypesofloopsthat
| you can | use | to implement |     | repetitive |      | operations. |      |     |     |
| ------- | --- | ------------ | --- | ---------- | ---- | ----------- | ---- | --- | --- |
|         |     |              | The | For ...    | Next |             | Loop |     |     |
The For...Next loop executes a series of statements a specific
| number | of times.               |             | The basic | syntax | is:   |         |       |                  |        |
| ------ | ----------------------- | ----------- | --------- | ------ | ----- | ------- | ----- | ---------------- | ------ |
| For    | x =                     | 0 to        | 10 Step   | 2      |       |         |       |                  |        |
|        | Console.Writeline("Your |             |           |        | stock | is      | down" | & x & "points.") |        |
| Next   | x                       |             |           |        |       |         |       |                  |        |
| Here,  |                         | the program |           | will   | loop  | through | this  | code five        | times, |
starting with x¼0. Each time it loops, x will be incremented by 2
until the maximum value of x, in this case 10, is reached. In the
example above, the printout will show our stock fall by 2 points
| with each | successive |     | loop. |     |     |     |     |     |     |
| --------- | ---------- | --- | ----- | --- | --- | --- | --- | --- | --- |
If the Step phrase is leftout, your programwill automatically
incrementtheloopcountervariablebyþ1.Let’stakealookatthis
code:
| For   | x   | = 1 to     | 5   |           |     |     |       |           |     |
| ----- | --- | ---------- | --- | --------- | --- | --- | ----- | --------- | --- |
|       |     | intSum     | +=  | x         |     |     |       |           |     |
| Next  | x   |            |     |           |     |     |       |           |     |
|       |     |            |     |           |     |     |       |           | ¼ þ |
| After |     | completing |     | the loop, |     | the | value | of intSum | 1   |
2þ3þ4þ5¼15.
|     |     | The | For | Each |     | Next | Loop |     |     |
| --- | --- | --- | --- | ---- | --- | ---- | ---- | --- | --- |
...
Each...Next
| The For |     |     | loop | is a | special | type | of loop | designed | to be |
| ------- | --- | --- | ---- | ---- | ------- | ---- | ------- | -------- | ----- |
used with data structures, such as an array. We will not discuss
arrays until later in the book, so for right now, just note the
| structure | of     | this type  | of  | loop. Here   |     | is an  | example: |     |     |
| --------- | ------ | ---------- | --- | ------------ | --- | ------ | -------- | --- | --- |
| Sub       | Main() |            |     |              |     |        |          |     |     |
|           | Dim    | dblReturn, |     | dblLowReturn | As  | Double |          |     |     |
Dim dblIBM As Double() = New Double() f.01,.005, -.05, 0,.02g
|     | For | Each | dblReturn    | In dblIBM      |             |      |     |     |     |
| --- | --- | ---- | ------------ | -------------- | ----------- | ---- | --- | --- | --- |
|     |     | If   | dblReturn    | < dblLowReturn |             | Then |     |     |     |
|     |     |      | dblLowReturn |                | = dblReturn |      |     |     |     |
Team-LRN

| ControlStructures |     |     |     |     |     |     |     |     | 69  |
| ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|                   |     | End | If  |     |     |     |     |     |     |
Next dblReturn
|     | Console.WriteLine("The |     |     | lowest      | return | is"     | & dblLowReturn) |     |       |
| --- | ---------------------- | --- | --- | ----------- | ------ | ------- | --------------- | --- | ----- |
| End | Sub                    |     |     |             |        |         |                 |     |       |
| The | For Each...Next        |     |     | loop cycles |        | through | each element    |     | in an |
array, or collection, without requiring specification of each
element’s index. Each timethrough the loop,the variable element,
in this case dblReturn, is assigned the contents of the next item in
the array.
| For | two-dimensional |     |     | arrays, | the | For Each...Next |     | structure |     |
| --- | --------------- | --- | --- | ------- | --- | --------------- | --- | --------- | --- |
will iterate through all the elements by row. That is, it will
increment the second index until it reaches the upper bound, then
increment the first index, and then restart iterating through the
second again.
| As      | we will     | see            | later,          | For Each...Next |       |             | loops | are also | very |
| ------- | ----------- | -------------- | --------------- | --------------- | ----- | ----------- | ----- | -------- | ---- |
| useful  | for looping |                | through         | collections     |       | of objects. |       |          |      |
|         |             | The            | Do...While      |                 |       | Loop        |       |          |      |
| Here is | an example  |                | of a Do...While |                 | loop: |             |       |          |      |
| Sub     | Main()      |                |                 |                 |       |             |       |          |      |
|         | Dim         | dblStockPrice# |                 | = 35            |       |             |       |          |      |
|         | Do          | While          | dblStockPrice   |                 | < 100 |             |       |          |      |
|         |             | dblStockPrice  |                 | +=              | 1     |             |       |          |      |
Loop
|     | Console.WriteLine("The |     |     |     | stock | price is" | & dblStockPrice) |     |     |
| --- | ---------------------- | --- | --- | --- | ----- | --------- | ---------------- | --- | --- |
| End | Sub                    |     |     |     |       |           |                  |     |     |
When this loop is finished, it prints out the price as 100. This
| routineevaluatesdblStockPrice |                   |     |     | ,        | 100eachtimethroughtheloop. |     |               |     |     |
| ----------------------------- | ----------------- | --- | --- | -------- | -------------------------- | --- | ------------- | --- | --- |
| When                          | dblStockPrice¼99, |     |     | the loop | increments                 |     | dblStockPrice |     | to  |
dblStockPrice¼100
| 100. The | next | evaluation |     | of  |     |     | is  | False, and | so  |
| -------- | ---- | ---------- | --- | --- | --- | --- | --- | ---------- | --- |
program execution exits the loop and continues with the line after
| the Loop | statement,         |               | printing        | dblStockPrice   |       | as   | 100. |     |     |
| -------- | ------------------ | ------------- | --------------- | --------------- | ----- | ---- | ---- | --- | --- |
|          |                    | The           | Do              | ...             | Until | Loop |      |     |     |
| Here is  | an example         |               | of a Do...Until |                 | loop: |      |      |     |     |
| Sub      | Main()             |               |                 |                 |       |      |      |     |     |
|          | Dim dblSellPrice#  |               | =               | 95              |       |      |      |     |     |
|          | Dim dblStockPrice# |               | =               | 45              |       |      |      |     |     |
|          | Do Until           | dblStockPrice |                 | >= dblSellPrice |       |      |      |     |     |
Team-LRN

| 70  |     |                       |     |                  |           | IntroductiontoVB.NET |
| --- | --- | --------------------- | --- | ---------------- | --------- | -------------------- |
|     |     | dblStockPrice         |     | *= Math.Exp(0.1) |           |                      |
|     |     | Console.WriteLine("We |     |                  | are still | holding the stock.") |
Loop
Console.WriteLine("We have sold the stock at" & dblStockPrice)
| End | Sub |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
As with the Do...While loop, the Do...Until is not necessarily
executedatallsincetheprogramevaluatestheexitconditionbefore
entering the loop. In this example, we sold the stock at 100.149.
|     |     | The | Do ... | Loop | While | Loop |
| --- | --- | --- | ------ | ---- | ----- | ---- |
To make sure that a loop executes at least once, place the exit
conditionattheLoopstatement,ratherthanattheDostatement,as
in the following:
| Sub | Main() |                |     |     |     |     |
| --- | ------ | -------------- | --- | --- | --- | --- |
|     | Dim    | dblStockPrice# |     | =   | 35  |     |
Do
|     |                         | Console.WriteLine("Incrementing |               |       |                | the stock price.")   |
| --- | ----------------------- | ------------------------------- | ------------- | ----- | -------------- | -------------------- |
|     |                         | dblStockPrice                   |               |       | -= 1           |                      |
|     | Loop                    | While                           | dblStockPrice |       | > 30           |                      |
|     | Console.WriteLine("Sold |                                 |               |       | the stock      | at" & dblStockPrice) |
| End | Sub                     |                                 |               |       |                |                      |
| In  | this                    | program                         | the           | stock | is sold at 30. |                      |
|     |                         | The                             | Do            | Loop  | Until          | Loop                 |
...
YoucansimilarlyputtheUntilconditionattheendofaloop.Inthe
previousexampleyouknewyouwantedtogothroughtheloopat
leastonce.ByputtingtheUntilstatementattheend,youdon’tneed
| to worry | about  | the            | initial | value | of the variable. |     |
| -------- | ------ | -------------- | ------- | ----- | ---------------- | --- |
| Sub      | Main() |                |         |       |                  |     |
|          | Dim    | dblStockPrice# |         | =     | 35               |     |
Do
|         |                       | dblStockPrice |               |         | -= 1     |                            |
| ------- | --------------------- | ------------- | ------------- | ------- | -------- | -------------------------- |
|         | Loop                  | Until         | dblStockPrice |         | = 25     |                            |
|         | Console.WriteLine("We |               |               |         | sold the | stock at" & dblStockPrice) |
| End     | Sub                   |               |               |         |          |                            |
| In this | program,              | the           | stock         | is sold | at 25.   |                            |
Team-LRN

| ControlStructures |           |     |       |          |     |         |                 | 71   |
| ----------------- | --------- | --- | ----- | -------- | --- | ------- | --------------- | ---- |
|                   |           | The | While | ...      | End | While   | Loop            |      |
| Visual            | Basic.NET |     | also  | provides |     | another | general-purpose | Loop |
While...End While...End
| statement |      | called             | the                        |     |         | While | loop. The    |     |
| --------- | ---- | ------------------ | -------------------------- | --- | ------- | ----- | ------------ | --- |
| While     | loop | has                | the following              |     | syntax: |       |              |     |
|           | Sub  | Main()             |                            |     |         |       |              |     |
|           |      | Dim dblStockPrice# |                            |     | = 35    |       |              |     |
|           |      | While              | dblStockPrice              |     | <= 50   |       |              |     |
|           |      |                    | dblStockPrice              |     | += 1    |       |              |     |
|           |      |                    | Console.WriteLine("Holding |     |         |       | the stock.") |     |
End While
|         | Console.WriteLine("We |          |           |         | sold the | stock | at" & dblStockPrice) |     |
| ------- | --------------------- | -------- | --------- | ------- | -------- | ----- | -------------------- | --- |
|         | End                   | Sub      |           |         |          |       |                      |     |
| In this | program               |          | the stock | is sold | at       | 51.   |                      |     |
| THE     | EXIT                  | COMMANDS |           |         |          |       |                      |     |
Thereareoccasionswhereyouneedtobreakoutofaloop.Insucha
case we can insert an Exit command. Depending on which type of
loopstructureyouareusing,youwillusetheExitForcommandor
| the | Exit | Do command. |     | We  | might | generally | do this inside | an  |
| --- | ---- | ----------- | --- | --- | ----- | --------- | -------------- | --- |
If...Thenstatementinsidealoop.Hereisanexampleofaninfinite
loop.TheDoWhile1statementwillneverevaluatetoFalse,andso
thisprogramwillloopforeveruntilsomeeventcausesanexitfrom
the loop. As you can imagine, it’s best to be very careful with
infinite loops.
|     | Sub | Main()             |                  |         |      |     |      |     |
| --- | --- | ------------------ | ---------------- | ------- | ---- | --- | ---- | --- |
|     |     | Dim dblStockPrice# |                  |         | = 35 |     |      |     |
|     |     | Do While           | 1                |         |      |     |      |     |
|     |     |                    | dblStockPrice    |         | += 1 |     |      |     |
|     |     |                    | If dblStockPrice |         | >    | 100 | Then |     |
|     |     |                    |                  | Exit Do |      |     |      |     |
|     |     |                    | End If           |         |      |     |      |     |
Loop
|         |          | Console.WriteLine("We |         |     | sold  | the     | stock at" & dblStockPrice) |     |
| ------- | -------- | --------------------- | ------- | --- | ----- | ------- | -------------------------- | --- |
|         | End      | Sub                   |         |     |       |         |                            |     |
| In this | program, |                       | we sold | the | stock | at 101. |                            |     |
| NESTED  |          | LOOPS                 |         |     |       |         |                            |     |
You can put a For...Next loop inside another For...Next loop.
ConsiderthefollowingexampleshowingnestedFor...Nextloops
Team-LRN

| 72  |     |     |     |     |     | IntroductiontoVB.NET |     |
| --- | --- | --- | --- | --- | --- | -------------------- | --- |
to transpose a matrix. Again, we haven’t looked at arrays yet, so
don’t worry about the variable references. For now, just note the
| structure | of embedded |            | loops.      |     |              |     |     |
| --------- | ----------- | ---------- | ----------- | --- | ------------ | --- | --- |
| For       | x = 0       | To intRows |             |     |              |     |     |
|           | For         | y = 0      | To intCols  |     |              |     |     |
|           |             |            | outArray(y, | x)  | = inArray(x, |     | y)  |
Next y
| Next | x   |     |     |     |     |     |     |
| ---- | --- | --- | --- | --- | --- | --- | --- |
For...Next
| Although |     |     | loops are | useful when | we  | know | in advance |
| -------- | --- | --- | --------- | ----------- | --- | ---- | ---------- |
how many times we want to execute the loop, there are occasions
| when we    | do not | have | this information | in  | advance. |            |     |
| ---------- | ------ | ---- | ---------------- | --- | -------- | ---------- | --- |
| ESTIMATING |        | AND  | FORECASTING      |     |          | VOLATILITY |     |
When analyzing financial data, we often estimate volatility over a
period of time in the past. This is easily done if we have a time
series of price data, as was the case in Project 4.1 where we used
fourlogreturnstocalculatethestandarddeviationofreturns.Ifwe
have several years of historical data, we can estimate the daily
volatility bysimply calculating the standard deviation of daily log
returns.
| How | though | do  | we estimate | volatility | given | only | 1 day of |
| --- | ------ | --- | ----------- | ---------- | ----- | ---- | -------- |
data? Usually, we would use the same method. We estimate 1 day
| standard | deviation | using | close-to-close | data | as follows: |     |     |
| -------- | --------- | ----- | -------------- | ---- | ----------- | --- | --- |
sffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffi
|     |     |     | (cid:4) | (cid:2) C (cid:3)(cid:5)2 |     |     |     |
| --- | --- | --- | ------- | ------------------------- | --- | --- | --- |
i
|     |     |     | s ¼ | ln  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | CC  | C   |     |     |     |
i(cid:1)1
| However, |     | this method | certainly | does | not | capture | all the |
| -------- | --- | ----------- | --------- | ---- | --- | ------- | ------- |
informationofintradayvolatility.Astockcouldcloseat50oneday,
gapopento53thefollowingday,tradedownto44,andcloseback
at50.Inthiscase,usingthisclose-to-closecalculationwouldnotbe
| a very      | good    | indicator | of volatility | since | “0” | is not | a good |
| ----------- | ------- | --------- | ------------- | ----- | --- | ------ | ------ |
| description | of what | happened. |               |       |     |        |        |
Tobetteraccountforone-periodvolatility,severalother,more
efficient methods have been proposed that use intraperiod highs
and lows to estimate volatility. These methods are often grouped
underthetermextremevalueestimators.Sinceseveralmodelsthatwe
Team-LRN

ControlStructures 73
useinfinancialmarketsarebasedontheassumptionofcontinuous
time, it is more intuitive to examine the entire time period rather
than simply the ends. The most well known of the extreme value
estimators have been proposed by Parkinson (1980) and Garman
and Klass (1980) (cited in Nelken, 1997, Chap. 1). The Parkinson’s
equation uses the intraperiod high and low thusly:
sffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffi
(cid:2)
H
(cid:3)2
i
s ¼ 0:601 ln
P L
i
The Garman-Klass estimator, which uses the intraperiod high and
low as well as the open and close data, has the form
vffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffi
u
u
"
1
(cid:2)
H i
(cid:3)2 (cid:2)
C i
(cid:3)2 #
s ¼ t ln (cid:1) ½2ln(2)(cid:1)1(cid:2) ln
GK 2 L O
i i
Noticethattheseequationsrepresentanestimateoftheone-period
historical volatility of the underlying symbol. You may notice,
however, that neither of these models takes into account gaps,
either up or down, from the previous day’s close. Volatility that
happens overnight will not be accounted for in either of these
models. For this and other reasons there are dozens of derivatives
ofthesetwoextremevalueestimatorscurrentlyinuse.Wewillnot
examine any of them beyond the two standard models presented.
These Parkinson and Garman-Klass models estimate past
volatility. They do not forecast future volatility. Forecasting
volatility is its own subject and is the topic of literally hundreds
of research papers and books. The most popular models for
forecasting volatility are the GARCH (generalized autoregressive
conditional heteroscedasticity) family.
Dozens of variations of GARCH models have been proposed
for forecasting volatility based on the assumption that returns are
generated by a random process with time-varying and mean-
reverting volatility (Alexander, 2001, p. 65). That is, in financial
markets,periodsoflowvolatilitytendtobefollowedbyperiodsof
low volatility, but are interspersed with periods of high volatility.
The most commonly referenced GARCH model for forecasting
Team-LRN

74 IntroductiontoVB.NET
variance is GARCH(1,1):
ss^2 ¼ (1(cid:1)a(cid:1)b)(cid:3)V þar2þbss^2 (5:1)
tþ1 t t
and
ss^2 ¼ V þ(aþb) j(cid:1)1(cid:3)(ss^2 (cid:1)V) (5:2)
tþj tþ1
whereaandbareoptimizedcoefficients,risthelogreturn,andV
is the sample variance over the entire data set. Determining the
valuesofthesecoefficients,aandb,isinitselfanartandascience
called optimization. In a later chapter we will discuss how to
employ an optimization engine to calculate the values of these
coefficientsusingmaximum-likelihoodmethods.Fornow,let’sget
familiarwithforecastingvariance,andthereforethevolatility,ofan
underlying stock for use in option pricing.
Since the variance forecasts are additive, we can estimate the
volatilitybetweennow,timet,andexpirationhdaysinthefuturein
the following way:
h
X
ss^2 ¼ ss^2 (5:3)
t,tþh tþj
j¼1
So if10 daysremainto expiration,wefirst calculatethe forecastof
variance for tþ1, or tomorrow, using Equation (5.1). Then we can
calculate the individual forecasts for the remaining 9 days using
Equation (5.2). Summing them up, we get a forecast of variance
from today until expiration 10 days from now. From there, we can
easily calculate an annualized volatility, which may or may not
differ from a market-implied volatility in an option.
Let’s create a Windows application that uses a For...Next
looptoforecastvolatilityforauser-definednumberofdaysahead.
Step 1 Open VB.NET and select New Project. In the New
Project window, select Windows Application, and
giveyourprojectthenameGARCHandalocationof
C:\ModelingFM.
Step 2 Now that the GUI designer is on your screen, from
the Toolbox add to your form a button, named
Button1, a text box, named TextBox1, and a label,
Team-LRN

| ControlStructures |     |     |     |     |     |     |     |     | 75  |
| ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
namedLabel1.InthePropertieswindowforButton1,
|     |     | change     | the text | property | to       | “Calculate.” |              | You | should |
| --- | --- | ---------- | -------- | -------- | -------- | ------------ | ------------ | --- | ------ |
|     |     | also clear | the      | text     | property | for          | the TextBox1 |     | and    |
Label1.
| Step | 3   | In the    | Solution | Explorer | window,   |      | click   | on the | View |
| ---- | --- | --------- | -------- | -------- | --------- | ---- | ------- | ------ | ---- |
|      |     | Code icon | to       | view     | the Form1 | code | window. |        |      |
In this project, we will demonstrate the use of a user-defined
valuetype,calledQuoteData,aswellasotherdatatypes.Youmay
| remember | the | discussion |     | of a | QuoteData | type | in the | previous |     |
| -------- | --- | ---------- | --- | ---- | --------- | ---- | ------ | -------- | --- |
chapter.Inanycase,weneedaconstructtoholdpricedata,andthe
| QuoteData | type | works | nicely. | Before | we  | can use | the | QuoteData |     |
| --------- | ---- | ----- | ------- | ------ | --- | ------- | --- | --------- | --- |
type, we need to define it for the compiler. Then we can declare
| some variables, |     | known |     | as qdMonday |     | and | qdTuesday, |     | as  |
| --------------- | --- | ----- | --- | ----------- | --- | --- | ---------- | --- | --- |
QuoteDatas.
| Step4   |           | Inthecodewindow,changethecodetothefollowing: |                           |           |           |      |     |     |     |
| ------- | --------- | -------------------------------------------- | ------------------------- | --------- | --------- | ---- | --- | --- | --- |
| Public  |           | Class Form1                                  |                           |           |           |      |     |     |     |
|         | Inherits  |                                              | System.Windows.Forms.Form |           |           |      |     |     |     |
| Windows |           | Form Designer                                |                           | generated |           | code |     |     |     |
|         | Structure |                                              | QuoteData                 |           |           |      |     |     |     |
|         |           | Public                                       | dblOpen                   | As        | Double    |      |     |     |     |
|         |           | Public                                       | dblHigh                   | As        | Double    |      |     |     |     |
|         |           | Public                                       | dblLow                    | As        | Double    |      |     |     |     |
|         |           | Public                                       | dblClose                  |           | As Double |      |     |     |     |
End Structure
|          | Dim               | qdMonday             |                | As QuoteData |               |            |             |              |      |
| -------- | ----------------- | -------------------- | -------------- | ------------ | ------------- | ---------- | ----------- | ------------ | ---- |
|          | Dim               | qdTuesday            |                | As QuoteData |               |            |             |              |      |
| End      | Class             |                      |                |              |               |            |             |              |      |
| Step     | 5                 | In the               | Class          | Name         | combo         | box at the | top         | left of      | your |
| code     | window,           | select               |                | Form1.       | In the        | Method     | Name        | combo        | box  |
| at       | the top           | right                | of your        | code         | window,       | select     | Form1_Load. |              | A    |
| code     | stub              | for                  | the Form1_Load |              | event         | handler    |             | will appear. |      |
| Within   |                   | this subroutine      |                | add          | the following |            | code to     | define       | the  |
| contents |                   | of qdMonday          |                | and          | qdTuesday:    |            |             |              |      |
| Private  |                   | Sub Form1_Load(ByVal |                |              | sender...)    | Handles    | MyBase.Load |              |      |
|          | qdMonday.dblOpen  |                      |                | = 50         |               |            |             |              |      |
|          | qdMonday.dblHigh  |                      |                | = 51.25      |               |            |             |              |      |
|          | qdMonday.dblLow   |                      |                | = 49.75      |               |            |             |              |      |
|          | qdMonday.dblClose |                      |                | = 50.5       |               |            |             |              |      |
Team-LRN

76 IntroductiontoVB.NET
qdTuesday.dblOpen = 50.5
qdTuesday.dblHigh = 51.0
qdTuesday.dblLow = 48.5
qdTuesday.dblClose = 49.5
End Sub
Wehavenowdefinedtwodailybarsforastock.Fromherewe
can add code to forecast volatility.
Step 6 InthesamewayasinStep5,selecttheButton1_Click
event.Withinthissubroutineaddthefollowingcode
to declare and define some variables and calculate
the volatility forecast according to the GARCH(1,1)
formula:
Private Sub Button1_Click(ByVal sender...) Handles Button1.Click
Dim dblSampleVariance# = 0.0002441 ’ V is the equation
Dim dblAlpha# = 0.0607 ’ Optimized coefficient
Dim dblBeta# = 0.899 ’ Optimized coefficient
Dim dblPrevForecast# = 0.0004152
Dim dblTotalForecast, x As Double
Dim dblOneDayAheadForecast# = (1 - dblAlpha - dblBeta) * _
dblSampleVariance + dblAlpha * Math.Log(qdTuesday.dblClose _
/ qdMonday.dblClose) ^ 2 + dblBeta (cid:4) dblPrevForecast
For x = 1 To TextBox1.Text
dblTotalForecast += (dblSampleVariance + (dblAlpha + _
dblBeta) ^ (x - 1) * (dblOneDayAheadForecast - _
dblSampleVariance))
Next x
’ Calculate the annualized volatility forecast.
Label1.Text = dblTotalForecast ^ 0.5 * (256/10) ^ 0.5
End Sub
TheGARCH(1,1)equationforecastsvariance.Thesquareroot
of this 10-day variance forecast will give us a 10-day volatility
forecast. Multiplying this by the square root of 256 trading days
divided by 10 gives us an annualized volatility number.
Step 7 Runtheprogram.Theresultwillappearasshownin
Figure 5.1.
Team-LRN

ControlStructures 77
F I G U R E 5.1
SUMMARY
InthischapterwelearnedhowtouseIf...Then...Elsestatements,
Select Case statements, and many different kinds of loops to con-
trol program flow. Loops will become more important in future
chaptersaboutarraysanddatastructures.Wealsolookedathowto
use a loop to forecast volatility using the GARCH(1,1) equation.
Team-LRN

| 78  |     |     |     |     | IntroductiontoVB.NET |     |     |
| --- | --- | --- | --- | --- | -------------------- | --- | --- |
PROBLEMS
| 1. What | are the two | types | of structures |     | discussed |     | in this |
| ------- | ----------- | ----- | ------------- | --- | --------- | --- | ------- |
chapter?
| 2. Assume | you bought | stock | in  | MMZR | at  | 50. | Write an |
| --------- | ---------- | ----- | --- | ---- | --- | --- | -------- |
If...Then...Elsestructuretosellthestockifitgoesupby
| 10 percent | or down           | by 5    | percent. |               |     |     |        |
| ---------- | ----------------- | ------- | -------- | ------------- | --- | --- | ------ |
| 3. What    | is the difference | between |          | the following |     | two | loops: |
|            | Do While x <      | 10      |          |               |     |     |        |
|            | x += 1            |         |          |               |     |     |        |
Loop
and
Do
|         | x += 1            |      |            |            |     |           |     |
| ------- | ----------------- | ---- | ---------- | ---------- | --- | --------- | --- |
|         | Loop While x      | < 10 |            |            |     |           |     |
| 4. What | are the different |      | repetition | structures |     | available | in  |
VB.NET?
| 5. Take | a look at the following |     | piece | of  | code: |     |     |
| ------- | ----------------------- | --- | ----- | --- | ----- | --- | --- |
| For     | x = 0 To 2              |     |       |     |       |     |     |
|         | For y = 0 To            | 3   |       |     |       |     |     |
|         | Console.WriteLine(x     |     |       | *   | y)    |     |     |
Next y
| Next    | x                |     |     |             |     |     |     |
| ------- | ---------------- | --- | --- | ----------- | --- | --- | --- |
| 6. What | would be printed | out | to  | the screen? |     |     |     |
Team-LRN

ControlStructures 79
PROJECT 5.1
TheGARCH(1,1)equationforecastsvolatilityusingtwooptimized
coefficients, alpha and beta, and three values—an estimate of the
previous day’s variance, r2; the long-run variance, V; and the
previous day’s forecast, s2. The estimate of the previous day’s
t
variance uses the log of the close-to-close method discussed in the
chapter. However, as we saw, close-to-close may not be a good
representation of intraperiod volatility.
Create a VB.NET Windows application that calculates three
forecasts for volatility for a user-defined number of days ahead.
This time make the GARCH(1,1) forecast using the close-to-close,
the Parkinson, and the Garman-Klass estimators of one-period
volatility. Print out the three forecasts in three labels.
PROJECT 5.2: MONTE CARLO SIMULATION
Visual Basic.NET has a built-in random number generator, rnd(),
which draws uniformly distributed deviates (random numbers)
between 0 and 1. In finance, we often wish to use a normal
distribution for Monte Carlo simulation. Here is the code to
generate a random number drawn from the standard normal
distribution using the rnd() function:
Dim dblNormRand As Double
Randomize()
dblNormRand = rnd() + rnd() + rnd() + rnd() + rnd() + rnd() +
rnd() + rnd() + rnd() + rnd() + rnd() + rnd() - 6
Create a VB.NET Windows application that will use a
For...Next loop and a Select Case structure to generate a user-
defined number of normally distributed random deviates and put
thedeviatesinto10binsasshownintheSelectCaseexplanationin
the chapter. Your result should look similar to Figure 5.2.
To initialize the VB’s random number generator, place
Randomize() in the Form1_Load event before calling rnd().
Team-LRN

80 IntroductiontoVB.NET
F I G U R E 5.2
Team-LRN

| C   | H A P | T E | R 6 |     |     |     |     |     |     |
| --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
Procedures
A
| procedure            | is  | a generic |     | term       | that refers | to  | the | two types    | of  |
| -------------------- | --- | --------- | --- | ---------- | ----------- | --- | --- | ------------ | --- |
| routines—subroutines |     |           | and | functions. | Procedures  |     |     | are packaged |     |
pieces of code that perform specific operations. Visual Basic.NET
has hundreds of procedures that we can use in our programs to
| perform | common | tasks |     | such | as string | manipulation, |     |     | error |
| ------- | ------ | ----- | --- | ---- | --------- | ------------- | --- | --- | ----- |
checking, and even a few mathematical and financial calculations.
What’s more, we can create our own, user-defined procedures to
| accomplish | specific     | tasks | in        | our programs. |          |            |            |      |         |
| ---------- | ------------ | ----- | --------- | ------------- | -------- | ---------- | ---------- | ---- | ------- |
| When       | we call      | a     | procedure |               | in our   | program,   | we         | are  | telling |
| Visual     | Basic.NET    | to    | execute   |               | the code | associated |            | with | that    |
| procedure. | Furthermore, |       | we        | may           | specify  | input      | arguments, |      | or      |
parameters, that we want to pass into the procedure—that is, the
valueorvalueswewanttheroutinetoworkon.Whenwedefinea
procedure,wemustspecifyfourthings:anamefortheprocedure;a
comma-separated list of parameters the procedure accepts, if any;
| the data | type of | the | return | value, | if  | any; | and the | procedure |     |
| -------- | ------- | --- | ------ | ------ | --- | ---- | ------- | --------- | --- |
definition, which is the code that executes when the routine is
called.
| The | only difference |     | between |     | a subroutine |     | and | a function | is  |
| --- | --------------- | --- | ------- | --- | ------------ | --- | --- | ---------- | --- |
that a function returns a value, aptly named the return value or
returnargument,whereasasubroutinedoesnot.Areturnvaluegets
sent back from the function to the code that called it. In general,
functions are preferred to subroutines, and they will be used
| whenever    | possible.   |        | The   | distinction |     | between  | functions |     | and     |
| ----------- | ----------- | ------ | ----- | ----------- | --- | -------- | --------- | --- | ------- |
| subroutines | will        | become | clear | when        | we  | use them | later.    |     |         |
| We          | programmers |        | use   | procedures  | to  | better   | organize  |     | code by |
breaking it up into smaller tasks. This makes the program code
81
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

| 82  |     |     |     |     |     |     | IntroductiontoVB.NET |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------- | --- | --- |
easier to read and debug. Also, procedures that perform common
tasks can be called over and over from different sections of the
| program, | reducing | duplication |     | of  | code and | making |     | the program |     |
| -------- | -------- | ----------- | --- | --- | -------- | ------ | --- | ----------- | --- |
easiertomaintain.Forexample,ifwewantedtocalculatethemean
returnsfor100stocks,wecouldwriteonefunctioncalledAverage()
anduseitahundredtimesover,ratherthanmakingthecalculation
in code for each of the 100 stocks. Let’s look at the code for an
| Average() | function: |                        |          |          |            |      |           |      |        |
| --------- | --------- | ---------------------- | -------- | -------- | ---------- | ---- | --------- | ---- | ------ |
| Public    |           | Function Average(ByVal |          |          | dblReturn1 | As   | Double,   | _    |        |
|           |           |                        |          | ByVal    | dblReturn2 | As   | Double    | ) As | Double |
|           |           | Return ( dblReturn1    |          | +        | dblReturn2 | )/2  |           |      |        |
| End       | Function  |                        |          |          |            |      |           |      |        |
| Now       | let’s     | review                 | the four | elements |            | of a | function. | One, | the    |
name of this function is Average(). Two, this function accepts two
input arguments, both of type Double, that will have the names
dblReturn1 and dblReturn2 within the function definition. Three,
thisfunctionreturnsavalueoftypeDouble.And,four,thefunction
definition is the code between the function header, the Public
Function Average line, and the function footer, End Function. We
could call this function from somewhere else in our program this
way:
| Sub | Main() |                       |     |     |                  |                      |     |     |     |
| --- | ------ | --------------------- | --- | --- | ---------------- | -------------------- | --- | --- | --- |
|     |        | Dim dblAverageReturn# |     |     |                  | = Average(.015,.005) |     |     |     |
|     |        | Console.WriteLine(    |     |     | dblAverageReturn |                      |     | )   |     |
| End | Sub    |                       |     |     |                  |                      |     |     |     |
HerethevalueofdblAverageReturnissetequaltothereturnvalue
of the function Average(). Of course, this program prints out .01.
| One | way | to describe | a   | function | is to | think | about | a black | box |
| --- | --- | ----------- | --- | -------- | ----- | ----- | ----- | ------- | --- |
thatprocessesinput,muchlikeamathematicalfunction.Inalgebra
| we may | use | an expression | like | this: |         |     |     |     |     |
| ------ | --- | ------------- | ---- | ----- | ------- | --- | --- | --- | --- |
|        |     |               | y ¼  | f(x , | x , x ) |     |     |     |     |
|        |     |               |      | 1     | 2 3     |     |     |     |     |
f(x) is, of course, a function. This function has a name, f. The
| function | accepts | input | arguments, |     | namely |     | x , | x , and | x . |
| -------- | ------- | ----- | ---------- | --- | ------ | --- | --- | ------- | --- |
|          |         |       |            |     |        |     | 1   | 2       | 3   |
The function named f has a return value to which y is then set
|           |              |                 | fexists |           |             |         |     | say,f(x       | ,x    |
| --------- | ------------ | --------------- | ------- | --------- | ----------- | ------- | --- | ------------- | ----- |
| equal.The | definitionof |                 |         | somewhere |             | elseand | is, |               | 1 2 , |
| x )¼2x    | þ3x          | þ4x . Functions |         | in        | programming |         | are | no different. |       |
| 3         | 1            | 2 3             |         |           |             |         |     |               |       |
Team-LRN

| Procedures     |           |     |             |     |      |       |            | 83  |
| -------------- | --------- | --- | ----------- | --- | ---- | ----- | ---------- | --- |
| INPUT          | ARGUMENTS |     |             |     |      |       |            |     |
| Both functions |           | and | subroutines | can | take | input | arguments. | The |
inputargumentlist,oftencalledtheparameters,hasitsownsyntax
| that requires |     | separate | consideration. |     |     |     |     |     |
| ------------- | --- | -------- | -------------- | --- | --- | --- | --- | --- |
Wecandeclareasmanyinputargumentswiththeirrespective
data types as are needed, provided we separate each parameter
with a comma. The basic syntax is to specify a local name for the
valueandadatatype.Forexample,hereisasimplesubroutinethat
| prints     | out two            | numbers               | in the       | console   | window:     |     |            |     |
| ---------- | ------------------ | --------------------- | ------------ | --------- | ----------- | --- | ---------- | --- |
| Private    |                    | Sub PrintPrices(ByVal |              |           | dblPrice1   |     | As Double, | _   |
|            |                    |                       |              | ByVal     | dblPrice2   |     | As Double) |     |
|            | Console.WriteLine( |                       |              | dblPrice1 |             | )   |            |     |
|            | Console.WriteLine( |                       |              | dblPrice2 |             | )   |            |     |
| End        | Sub                |                       |              |           |             |     |            |     |
| We         | then               | call the              | PrintNumbers |           | subroutine. |     | We specify | the |
| parameters | after              | the                   | name as      | follows:  |             |     |            |     |
| Sub        | Main()             |                       |              |           |             |     |            |     |
|            | PrintPrices(       |                       | 45.23,       | 65.54     |             | )   |            |     |
| End        | Sub                |                       |              |           |             |     |            |     |
In this example, the values 45.23 and 65.54 are passed to the
variablesdblPrice1anddblPrice2.Withinthesubroutinedefinition,
the values passed in will be known by the local names dblPrice1
anddblPrice2.Sincethisisasubroutine,thereisnoreturnvalueas
was the case in the Average() function. The output of this simple
| program | will | be: |     |     |     |     |     |     |
| ------- | ---- | --- | --- | --- | --- | --- | --- | --- |
45.23
65.54
| There | are | times | when we | may | not | be required | to pass | all the |
| ----- | --- | ----- | ------- | --- | --- | ----------- | ------- | ------- |
arguments in a parameter list to a procedure. This is typically the
case when parameters later in the list are dependent on specific
values of variables earlier in the list. To declare a parameter as
| optional,    | we  | include | the Optional |     | keyword     |     | in the parameter |     |
| ------------ | --- | ------- | ------------ | --- | ----------- | --- | ---------------- | --- |
| declaration. |     | When    | we declare   |     | a parameter |     | as optional,     | all |
subsequent parameters in the list must also be optional. Here is
an example:
Team-LRN

84 IntroductiontoVB.NET
Public Function PV( ByVal Rate As Double, _
ByVal NPer As Double, _
ByVal Pmt As Double, _
Optional ByVal FV As Double, _
Optional ByVal Due As Date) _
As Double
Here values for FV and Due are not required by the function
definition to perform the calculation and return the PV, present
value.
ByRef and ByVal
Let’s take a look at the important distinction between ByRef and
ByVal, the two methods for passing input arguments to functions.
Passing an input argument ByVal means that the original
variable, which is being passed as an input argument, will not be
changed by the function definition. That is to say, the procedure
makes a copy of the value and performs the operations within the
procedure definition on the copy, as opposed to the original
variable. This is demonstrated by the following example:
Sub Main()
Dim dblStockPrice# = 52.78
Increment(dblStockPrice)
Console.WriteLine("Stock price after increment is: " _
& dblStockPrice)
End Sub
Private Sub Increment(ByVal dblNum As Double)
Console.WriteLine("Increment subroutine was passed: " & dblNum)
dblNum += 1
Console.WriteLine("New value is: " & dblNum)
End Sub
This program outputs:
Increment function was passed: 52.78
New value is: 53.78
Stock price after increment is: 52.78
The dblStockPrice variable is unaffected by the addition
within the Increment subroutine. This is because only the value of
dblStockPricehasbeenpassedtodblNum.dblNumisacompletely
separate variable. ByVal is the default method for passing values
Team-LRN

Procedures 85
into functions. Now try this example again, but change ByVal in
| Increment() |       | to ByRef            | as follows: |       |        |       |         |     |
| ----------- | ----- | ------------------- | ----------- | ----- | ------ | ----- | ------- | --- |
| Private     |       | Sub Increment(ByRef |             |       | dblNum | As    | Double) |     |
| This time   | the   | output              | is:         |       |        |       |         |     |
| Increment   |       | was                 | passed:     | 52.78 |        |       |         |     |
| New         | value | is:                 | 53.78       |       |        |       |         |     |
| Stock       | price | after               | increment   |       | is:    | 53.78 |         |     |
Here a reference to the location of dblStockPrice in memory is
passedtodblNum,notthevalueofdblStockPrice.Therefore,asfar
| asthecomputerisconcerned,bothdblNumand |     |     |     |     |     |     | dblStockPriceare |     |
| -------------------------------------- | --- | --- | --- | --- | --- | --- | ---------------- | --- |
referringtothesamephysicalspace,orlocation,inmemory.Hence,
when dblNum is incremented, the value of dblStockPrice changes
| since | they are | both | the same | variable. |     |     |     |     |
| ----- | -------- | ---- | -------- | --------- | --- | --- | --- | --- |
ParamArray
| There                    | is one | additional |     | keyword    | we  | can     | use | in procedure |
| ------------------------ | ------ | ---------- | --- | ---------- | --- | ------- | --- | ------------ |
| declarations—ParamArray. |        |            |     | ParamArray |     | enables | us  | to pass an   |
arbitrary numberof arguments into function. That is, ParamArray
| allows | an indeterminate |     |     | number | of input | arguments |     | passed as |
| ------ | ---------------- | --- | --- | ------ | -------- | --------- | --- | --------- |
either a one-dimensional list or an array of the type specified.
Withinthefunctiondefinition,theparameterarrayistreatedasan
arrayofitsdeclaredtype.TouseaParamArray,justspecifythelast
| parameter | in     | a parameter |     | list as | a ParamArray: |     |     |     |
| --------- | ------ | ----------- | --- | ------- | ------------- | --- | --- | --- |
| Sub       | Main() |             |     |         |               |     |     |     |
Dim dblPrices As Double() = New Double() f52.34, 35.34, 0.15g
|     | PrintPrices(dblPrices) |     |        |        |        | ’ Pass | as  | an array |
| --- | ---------------------- | --- | ------ | ------ | ------ | ------ | --- | -------- |
|     | PrintPrices(10.5,      |     | 95.34, | 31.22, | 74.23) | ’ Pass | as  | a list   |
| End | Sub                    |     |        |        |        |        |     |          |
Private Sub PrintPrices(ByVal ParamArray dblStockPrices As Double())
|     | Dim                          | i As Double         |                   |                       |           |          |           |     |
| --- | ---------------------------- | ------------------- | ----------------- | --------------------- | --------- | -------- | --------- | --- |
|     | Console.WriteLine("Portfolio |                     |                   |                       | of stocks | contains | "         | & _ |
|     |                              |                     |                   | dblStockPrices.Length |           | &        | " stocks. | _   |
|     |                              |                     |                   | The prices            | are:      | ")       |           |     |
|     | For                          | Each i              | In dblStockPrices |                       |           |          |           |     |
|     |                              | Console.WriteLine(" |                   | "                     | & i)      |          |           |     |
Next i
| End | Sub |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Team-LRN

86 IntroductiontoVB.NET
This program calls the function twice: The first time the array,
dblPrices,ispassedwiththreeprices;thesecondtimealistoffour
prices is passed. In Chapter 8, we will take an in-depth look at
arrays.Also,noticetheuseoftheForEach...Nextloopstructure,
which we discussed in the previous chapter.
RETURN VALUES
Aswesaid,functionshavereturnvalues,whichdonotnecessarily
have to be numbers; they can return any data type. We can set the
return value of a function by using the Return keyword. Here is a
function that returns a Boolean, expressing whether or not our
stock has hit a support level:
Public Function SupportLevel( dblStockPrice As Double, _
dblStrongSupport As Double ) As Boolean
If dblStockPrice > dblStrongSupport
Return True
Else
Return False
End If
End Function
Functions can return any value type, such as doubles, integers,
Booleans, or strings. As we will learn in later chapters, functions
can also return reference types like arrays and objects.
BLACK-SCHOLES OPTION PRICING FORMULA
In programming VB.NET, and all other languages for that matter,
theprocessof creatingourownuser-definedproceduresis exactly
thesameasinalgebra.However,asyoumayhavenoticed,welike
togiveourproceduresandinputvariablesmoredescriptivenames
than just f and x’s and y’s. Programmers prefer to use names like
Command1_Click() or BlackScholesCall() that describe the nature
of the operations performed within the procedure definition.
TheBlack-Scholespriceofacalloptionisafunctionofseveral
input values, namely S, the price of the underlying stock; X, the
strike price; t, the time to expiration; r, the interest rate; ands, the
volatility; so that
y5BlackScholesCall( S, X, t, r, s )
Team-LRN

| Procedures |     |     |     |     |     |     | 87  |
| ---------- | --- | --- | --- | --- | --- | --- | --- |
The mathematical definition of the Black-Scholes equation for the
| price | of a call | option | is  |     |     |     |     |
| ----- | --------- | ------ | --- | --- | --- | --- | --- |
)(cid:1)Xe(cid:1)rtN(d
|     |     | BlackScholesCall |     | ¼ SN(d |     | )   |     |
| --- | --- | ---------------- | --- | ------ | --- | --- | --- |
|     |     |                  |     |        | 1   | 2   |     |
where
ln(S=X)þ(rþ(s2=2))T
|     |     | d   | ¼   | p   |              |     |     |
| --- | --- | --- | --- | --- | ------------ | --- | --- |
|     |     | 1   |     |     | ffiffiffiffi |     |     |
s T
and
p
ffiffiffiffi
|     |     |     |     | d ¼ d (cid:1)s | T   |     |     |
| --- | --- | --- | --- | -------------- | --- | --- | --- |
2 1
To make a VB.NET function that calculates the price of a call
optionaccordingtotheBlack-Scholesformula,weneedfourthings:
afunctionname,alistofinputargumentswiththeirrespectivedata
| types, | a return | type,                  | and | a function | definition.     |            |           |
| ------ | -------- | ---------------------- | --- | ---------- | --------------- | ---------- | --------- |
| Public | Function | BlackScholesCall(ByVal |     |            | dblStock        | As Double, | _         |
|        |          |                        |     | ByVal      | dblStrike       | As Double, | _         |
|        |          |                        |     | ByVal      | dblTime         | As Double, | _         |
|        |          |                        |     | ByVal      | dblInterestRate | As         | Double, _ |
|        |          |                        |     | ByVal      | dblSigma        | As Double) | _         |
As Double
|     | Dim                   | d1, d2, Nd1, | Nd2                   | As Double          |                    |     |     |
| --- | --------------------- | ------------ | --------------------- | ------------------ | ------------------ | --- | --- |
|     | ’ Calculate           | d1           | and                   | d2                 |                    |     |     |
|     | d15(Math.Log(dblStock |              |                       | / dblStrike)       | + (dblInterestRate |     | + _ |
|     |                       | (dblSigma    | ^ 2)                  | / 2) * dblTime)    | / _                |     |     |
|     |                       | (dblSigma    | * Math.Sqrt(dblTime)) |                    |                    |     |     |
|     | d25d12dblSigma        |              | *                     | Math.Sqrt(dblTime) |                    |     |     |
|     | ’ Calculate           | N(d1)        | and                   | N(d2)              |                    |     |     |
Nd15NormCDF(d1)
Nd25NormCDF(d2)
|     | ’ Calculate | the | price | of the call |     |     |     |
| --- | ----------- | --- | ----- | ----------- | --- | --- | --- |
Return dblStock * Nd1 - dblStrike * Math.Exp(-dblInterestRate _
|     |          | * dblTime) | *     | Nd2                    |     |          |      |
| --- | -------- | ---------- | ----- | ---------------------- | --- | -------- | ---- |
| End | Function |            |       |                        |     |          |      |
| The | code     | that       | calls | the BlackScholesCall() |     | function | then |
doesn’tneedtoknowhowthefunctioncalculatestheresult.Itjust
takestheoutputitneedsandgoesonitsmerryway.Thisdefinition
of the function will be somewhere else. We could call the function
in this fashion:
Team-LRN

88 IntroductiontoVB.NET
Sub Main()
Dim dblOptionPrice As Double
dblOptionPrice = BlackScholesCall( 42, 40, .5, .1, .2 )
Console.WriteLine(dblOptionPrice)
End Sub
The variable dblOptionPrice then will be set equal to the
return value of the function called BlackScholesCall(), which of
course calculates the price of a call option according to the
parameters, or input arguments, it receives.
The Black-Scholes formula is just one of several methods to
calculatethepriceofanoption.Wewillnot,however,coveroption
pricingtheoryindepthinthisbook,althoughwewillbrieflycover
binomial trees in Chapter 8. We refer you to one of several other
books on the topic, especially The Complete Guide to Option Pricing
Formulas byEspenGaarder Haug(New York:McGraw-Hill, 1998),
which contains particularly complete coverage of option pricing
methods.
Let’s create a short Windows application that calculates the
price of a call option using the BlackScholesCall() function.
Step 1 Open a new Windows application in Visual
Basic.NETand name it BlackScholes.
Step 2 Once the IDE for your new program is ready, in the
Project menu, click on Add Module to add a code
module.
Step 3 In the module, type in the BlackScholesCall()
function code as shown previously, or copy it from
thefilenamedBlackScholesCall.txtfromtheCDand
paste it in. Your module should look like this:
Module BlackScholes
Public Function BlackScholesCall(ByVal dblStock ...) As Double
’ Function definition in here.
End Function
End Module
Step 4 Since the BlackScholesCall() function itself calls
another function named NormCDF(), we will have
to add this function, which is an approximation of
thecumulativenormaldistributionfunction.Again,
in the Project menu, click on Add Module. Add the
following code to the new module:
Team-LRN

Procedures 89
Module NormalCDF
Public Function NormCDF(ByVal X As Double) As Double
’ Calculate the cumulative probability distribution
’ function for standard normal at X
Dim a, b, c, d, prob As Double
a = 0.4361836
b = -0.1201676
c = 0.937298
d = 1 / (1 + 0.33267 * Math.Abs(X))
prob = 1 - 1 / Math.Sqrt(2 * 3.1415926) * Math.Exp(-0.5 *
X * _ X) * (a * d + b * d * d 1 c * d * d * d)
If X < 0 Then prob = 1 - prob
Return prob
End Function
End Module
Step 5 At the top of your code window, click on the
Form1.vb [Design] tab to return to the GUI
development window. From the Toolbox, add a
label,namedLabel1,andacommandbutton,named
Button1, to your form.
Step 6 Double-clickonthecommandbuttontobringupthe
code stub for the Button1_Click event. To this event
subroutine, add the following code:
Private Sub Button1_Click(ByVal sender ...) Handles Button1.Click
Dim dblCallPrice As Double
dblCallPrice = BlackScholesCall(42, 40, 0.5, 0.1, 0.2)
Label1.Text = Str(dblCallPrice)
End Sub
Step 7 Run the program (see Figure 6.1).
The program you have just created illustrates the use of two
functions: the BlackScholesCall() and the NormCDF(). It also
illustrates the use of a subroutine, Button1_Click(). Again, notice
that the two functions accept input arguments and have a return
value, whereas the subroutine does not have a return value.
To review, the BlackScholesCall() function header shows that
the values passed into the function will be known as dblStock,
dblStrike, dblTime, dblInterestRate, and dblSigma within the
functiondefinition.Also,thereturnvalueofthefunctionwillbeof
type double as indicated at the tail end of the function header:
Team-LRN

| 90     |          |                        |     |       |                 | IntroductiontoVB.NET |           |
| ------ | -------- | ---------------------- | --- | ----- | --------------- | -------------------- | --------- |
| F I G  | U R      | E 6.1                  |     |       |                 |                      |           |
| Public | Function | BlackScholesCall(ByVal |     |       | dblStock        | As Double,           | _         |
|        |          |                        |     | ByVal | dblStrike       | As Double,           | _         |
|        |          |                        |     | ByVal | dblTime         | As Double,           | _         |
|        |          |                        |     | ByVal | dblInterestRate | As                   | Double, _ |
|        |          |                        |     | ByVal | dblSigma        | As Double)           | _         |
As Double
| The | function | definition |     | exists | between | the header | and the |
| --- | -------- | ---------- | --- | ------ | ------- | ---------- | ------- |
footer, End Function. The return value is set using the Return
| keyword.  | Notice | that       | within | both       | the       | BlackScholesCall() | and      |
| --------- | ------ | ---------- | ------ | ---------- | --------- | ------------------ | -------- |
| NormCDF() |        | functions, | we     | call other | functions | from               | the Math |
library, including Math.Exp(), Math.Log(), and Math.Sqrt(). These
are prebuilt functions in VB.NET that we can call in our programs
| without | having    | to provide |     | function | definitions | for them. |     |
| ------- | --------- | ---------- | --- | -------- | ----------- | --------- | --- |
| MATH    | FUNCTIONS |            |     |          |             |           |     |
If you program in Excel, you should be well versed in prebuilt
mathematicalfunctions.VisualBasic.NETtoohasnumerousbuilt-
in mathematical functions that we can call in our programs. The
following table summarizes the available functions found in the
Mathnamespacethatmaybeimportantinquantitativefinance.To
callthesefunctions,weneedtoprecedethefunctionnamewiththe
class name Math and a dot (.). That is, the fully qualified function
| name for | the | Max() function, |     | for example, |     | is Math.Max(). |     |
| -------- | --- | --------------- | --- | ------------ | --- | -------------- | --- |
Team-LRN

Procedures 91
Math
| Functions | Description                | Example           |     |
| --------- | -------------------------- | ----------------- | --- |
| Abs()     | Returnstheabsolutevalueofx | dblError¼Math.abs |     |
(dblForecast-dblActual)
| Ceiling() | Returnstheintegergreaterthan | dblSell¼Math.ceiling |     |
| --------- | ---------------------------- | -------------------- | --- |
|           | orequaltotheinputargument    | (dblStockPrice)      |     |
Exp() Returnse(thebaseofnatural dblFV¼dblPV(cid:2)Math.exp(dblR
|     | logarithms)raisedtothe | (cid:2) dblTime) |     |
| --- | ---------------------- | ---------------- | --- |
powerofx
| Floor() | Returnstheintegerlessthanor   | dblBuy¼Math.floor |     |
| ------- | ----------------------------- | ----------------- | --- |
|         | equaltotheinputargument       | (dblStockPrice)   |     |
| Log()   | Returnsthenaturallogarithmofx | dblRate¼Math.log  |     |
(dblTuesday/dblMonday)
| Max() | Returnsthemaximumoftwo | DblPrice¼Math.max(0,x) |     |
| ----- | ---------------------- | ---------------------- | --- |
inputarguments
| Min() | Returnstheminimumoftwo | DblPrice¼Math.min(0,x) |     |
| ----- | ---------------------- | ---------------------- | --- |
inputarguments
| Sign() | Returns:1ifxisgreaterthan0;0 | blnBUYSELL¼    | Math.sign |
| ------ | ---------------------------- | -------------- | --------- |
|        | ifxequals0;21ifxisless       | (dblMoonphase) |           |
than0
| Sqrt() | Returnsthesquareroot | dblStDev¼             |     |
| ------ | -------------------- | --------------------- | --- |
|        | ofx                  | Math.sqrt(myVariance) |     |
| STRING | FUNCTIONS            |                       |     |
Astringisoftentimesjustathingthatweprintoutorpassfromone
part of our program to another without regard for its contents.
Other times, however, we need to know what’s inside. We might
need to verify its contents, modify it in some way, or extract a
specific piece of information from it. When dealing with options
quotes, for example, we sometimes need to parse out the stock
symbol, the expiration month, and the strike price, which are all
strungtogetherinonelongoptionsymbol.Thestringfunctionswe
will need to know, but certainly not all that are available, are
summarizedbelow.Asyouwillsee,someofthefunctionsareinthe
Microsoft.VisualBasic.Strings class.
String
| Functions | Description         | Example        |     |
| --------- | ------------------- | -------------- | --- |
| Chr()     | Returnsthecharacter | myChar¼Chr(65) |     |
associatedwithaspecific
charactercode
(continues)
Team-LRN

| 92  |     |     | IntroductiontoVB.NET |     |
| --- | --- | --- | -------------------- | --- |
String
Functions Description Example
| GetChar() | Returnsacharvaluetype    |     | myChar¼            |     |
| --------- | ------------------------ | --- | ------------------ | --- |
|           | representingthecharacter |     | GetChar("IBMDP",4) |     |
fromaspecificindexina
string
| Join() | Concatenatesanarrayofstrings |     | myString¼             |     |
| ------ | ---------------------------- | --- | --------------------- | --- |
|        | intoadelimitedstring         |     | Join(myArray,Optional |     |
delimiter)
| Len() | Returnstheintegerlengthof |     | myInt¼Len(string) |     |
| ----- | ------------------------- | --- | ----------------- | --- |
String
| InStr() | Returnsanintegerspecifying    |     | myInt¼InStr(1,string, |     |
| ------- | ----------------------------- | --- | --------------------- | --- |
|         | thestartingpositionofthefirst |     | "D")                  |     |
occurrenceofastringwithin
anotherstring
| Left() | Returnstheleftmostlengthof |     | strTicker¼             |     |
| ------ | -------------------------- | --- | ---------------------- | --- |
|        | charactersofastring        |     | Microsoft.VisualBasic. |     |
Left(strOptionsSymbol,3)
| Right() | Returnstherightmostlengthof |     | strStrike¼                  |     |
| ------- | --------------------------- | --- | --------------------------- | --- |
|         | charactersofastring         |     | Microsoft.VisualBasic.Right |     |
(strOptionsSymbol,1)
| Mid() | Returnslengthcharactersfrom |     | myString¼Mid(string, |     |
| ----- | --------------------------- | --- | -------------------- | --- |
|       | String,startingatposition   |     | start,length)        |     |
Start
| Split() | Returnsanarrayofstrings  |     | myString¼“IBMApril80Call” |     |
| ------- | ------------------------ | --- | ------------------------- | --- |
|         | consistingofthedelimited |     | myArray¼ Split(myString)  |     |
strings(orwords)ofaninput
argumentstring
StrComp() Returns21,0,or1,depending myInt¼ StrComp(myStringA,
|     | upontheresultofastring |     | myStringB) |     |
| --- | ---------------------- | --- | ---------- | --- |
comparison
Manyofthesefunctionsarehelpfulinparsingstrings.Parsing
is the process of extracting smaller pieces or substrings from a
string.Herearesomeexamplesshowinghowtoparsestringsusing
| the string | functions in the | table. |     |     |
| ---------- | ---------------- | ------ | --- | --- |
The Split Function
| The Split | function accepts | a string | as an input argument | and |
| --------- | ---------------- | -------- | -------------------- | --- |
returns an array consisting of the parsed values of the array.
| Sub | Main()             |             |     |     |
| --- | ------------------ | ----------- | --- | --- |
|     | Dim strMyString    | As String   |     |     |
|     | Dim strReturnArray | As String() |     |     |
Team-LRN

| Procedures |     |             |         |     |          |     |     | 93  |
| ---------- | --- | ----------- | ------- | --- | -------- | --- | --- | --- |
|            |     | strMyString | = "INTC | Jun | 25 Call" |     |     |     |
strReturnArray5Split(strMyString)
Console.WriteLine(strReturnArray(0))
|     | End Sub |     |     |     |     |     |     |     |
| --- | ------- | --- | --- | --- | --- | --- | --- | --- |
Afterrunningthiscode,thevaluesinthestrReturnArraywill
| look | like this:        |       |        |     |     |           |     |     |
| ---- | ----------------- | ----- | ------ | --- | --- | --------- | --- | --- |
|      | strReturnArray(0) |       | = INTC |     |     |           |     |     |
|      | strReturnArray(1) |       | = Jun  |     |     |           |     |     |
|      | strReturnArray(2) |       | = 25   |     |     |           |     |     |
|      | strReturnArray(3) |       | = Call |     |     |           |     |     |
|      | The               | Left, | Right, | and | Mid | Functions |     |     |
TheLeftandRightfunctionsareverysimilartoeachother.TheLeft
and Right functions accept two input arguments—a string and a
length. The Left function returns a string containing the leftmost
“length” number of characters in the string. The Right function
returns the rightmost “length” number of characters. Here is an
example:
|     | Sub Main()       |            |                                                 |     |           |           |     |     |
| --- | ---------------- | ---------- | ----------------------------------------------- | --- | --------- | --------- | --- | --- |
|     | Dim              | strTicker, | strOptionsSymbol,                               |     | strStrike | As String |     |     |
|     | strOptionsSymbol |            | = "IBMDP"                                       |     |           |           |     |     |
|     | strTicker        |            | = Microsoft.VisualBasic.Left(strOptionsSymbol,  |     |           |           | 3)  |     |
|     | strStrike        |            | = Microsoft.VisualBasic.Right(strOptionsSymbol, |     |           |           | 1)  |     |
Console.WriteLine(strTicker)
Console.WriteLine(strStrike)
|     | End Sub |     |     |     |     |     |     |     |
| --- | ------- | --- | --- | --- | --- | --- | --- | --- |
The variable strTicker then will be equal to just IBM. strStrike will
equal P.
|     | The Mid | function | accepts | a string, | a   | starting number, | and | a   |
| --- | ------- | -------- | ------- | --------- | --- | ---------------- | --- | --- |
length. It returns a string of length with a given string. So
|            | Dim strMonth$ |          | = Mid(strOptionsSymbol, |     |         | 4, 1)     |         |     |
| ---------- | ------------- | -------- | ----------------------- | --- | ------- | --------- | ------- | --- |
| strMonth   | will          | equal    | D.                      |     |         |           |         |     |
| FORMATTING |               |          | NUMBERS                 |     | FOR     | OUTPUT    |         |     |
| The        | Format()      | function | converts                | and | formats | dates and | numbers |     |
intostrings.Format()givesusamuchgreaterdegreeofcontrolover
Team-LRN

| 94  |     |     |     |     | IntroductiontoVB.NET |     |
| --- | --- | --- | --- | --- | -------------------- | --- |
how our data is presented for either screen or printer output. In
VB.NET, we can choose from predefined named formats or create
| our own | user-defined |     | format | for finer control. | Numeric | data, |
| ------- | ------------ | --- | ------ | ------------------ | ------- | ----- |
regardless of type, can be formatted using the Format() function.
The following table explains some of the predefined formats and
| some user-defined |     | formats |     | with their associated | outputs: |     |
| ----------------- | --- | ------- | --- | --------------------- | -------- | --- |
Predefined
FormatFunction
| Names                   |     |     |           | Example |     | Output |
| ----------------------- | --- | --- | --------- | ------- | --- | ------ |
| AssumethatdblVolatility |     | ¼   | 0.1234567 |         |     |        |
GeneralNumber Format(dblVolatility,“GeneralNumber”) 0.1234567
| Currency   |     | Format(dblVolatility,“Currency”)   |     |     |     | $0.12    |
| ---------- | --- | ---------------------------------- | --- | --- | --- | -------- |
| Fixed      |     | Format(dblVolatility,“Fixed”)      |     |     |     | 0.12     |
| Standard   |     | Format(dblVolatility,“Standard”)   |     |     |     | 0.12     |
| Percent    |     | Format(dblVolatility,“Percent”)    |     |     |     | 12.34%   |
| Scientific |     | Format(dblVolatility,“Scientific”) |     |     |     | 1.23E-01 |
User-Defined
Format
| Function |     |                                          |     | Example |     | Output    |
| -------- | --- | ---------------------------------------- | --- | ------- | --- | --------- |
|          |     | Format(dblVolatility,“#.####”)           |     |         |     | .12345    |
|          |     | Format(dblVolatility,“0.####”)           |     |         |     | 0.12345   |
|          |     | Format(dblVolatility,“00000”)            |     |         |     | 00000     |
|          |     | Format(dblVolatility,“#####”)            |     |         |     | [nothing] |
|          |     | Format(dblVolatility,“###%”)             |     |         |     | 12%       |
|          |     | Format(dblVolatility,“###,###,##0.000”)  |     |         |     | 0.123     |
|          |     | Format(dblVolatility,“\$###,###,##0.00”) |     |         |     | $0.12     |
Notethe use of thebackslashin the finalline of code. It allowsthe
computer to interpret the next character literally instead of as a
format character. Here is a quick code example that will print out
| the value  | of dblVolatility                        |                | as        | 0.1235:     |     |            |
| ---------- | --------------------------------------- | -------------- | --------- | ----------- | --- | ---------- |
| Sub        | Main()                                  |                |           |             |     |            |
|            | Dim                                     | dblVolatility# |           | = 0.1234567 |     |            |
|            | Console.WriteLine(Format(dblVolatility, |                |           |             |     | "0.####")) |
| End        | Sub                                     |                |           |             |     |            |
| CONVERSION |                                         |                | FUNCTIONS |             |     |            |
As mentioned in Chapter 4, Option Strict On requires explicit
conversionofdatatypesincaseswheredatalosscouldoccur.This
Team-LRN

Procedures 95
includes any conversion between numeric types and string types.
| For example, | data | loss | may | occur | when | a string | variable is |
| ------------ | ---- | ---- | --- | ----- | ---- | -------- | ----------- |
convertedtoadoubleoranyotherdatatypewithlessprecisionor
smaller capacity. If Option Strict is set to On, an error will occur if
an implicit conversion exists in our program. VB.NET provides
several functions for explicit conversion. Also, as we mentioned
earlier, in order to clarify and simplify the algorithms and logic in
ourexampleprograms,wehavealmostalwaysleftOptionStrictby
default set to Off. However, production applications you create
should include Option Strict On and explicit type conversions
| through | the use | of these | conversion |     | functions. |     |     |
| ------- | ------- | -------- | ---------- | --- | ---------- | --- | --- |
Conversion
| Functions |                           | Description |     |     |                     | Example            |               |
| --------- | ------------------------- | ----------- | --- | --- | ------------------- | ------------------ | ------------- |
| Str()     | Convertsanumbertoastring  |             |     |     | strPrice¼           | str(dblStockPrice) |               |
| Val()     | Convertsastringtoanumber  |             |     |     | dblStockPrice¼      |                    | val(strPrice) |
| CBool()   | ConvertsavaluetoaBoolean  |             |     |     | myBool¼CBool(myVal) |                    |               |
| CChar()   | Convertsavaluetoachar     |             |     |     | myChar¼CChar(myVal) |                    |               |
| CDate()   | Convertsavaluetoadate     |             |     |     | myDate¼CDate(myVal) |                    |               |
| CDbl()    | Convertsavaluetoadouble   |             |     |     | myDbl¼CDbl(myVal)   |                    |               |
| CDec()    | Convertsavaluetoadecimal  |             |     |     | myDec¼CDec(myVal)   |                    |               |
| CInt()    | Convertsavaluetoaninteger |             |     |     | myInt¼CInt(myVal)   |                    |               |
| CLng()    | Convertsavaluetoalong     |             |     |     | myLng¼CLng(myVal)   |                    |               |
| CShort()  | Convertsavaluetoashort    |             |     |     | myShort¼            | CShort(myVal)      |               |
| CSng()    | Convertsavaluetoasingle   |             |     |     | mySng¼CSng(myVal)   |                    |               |
| CStr()    | Convertsavaluetoastring   |             |     |     | myStr¼CStr(myVal)   |                    |               |
CType() Convertsavalueintoaspecifiedtype myDbl¼CType(myValue,Double)
Asyoucanprobablyimagine,notallconversionsarepossible.
We clearly cannot convert IBMDP into a double. Here is a short
| program | illustrating | the | use | of a conversion |     | function: |     |
| ------- | ------------ | --- | --- | --------------- | --- | --------- | --- |
| Option  | Strict       | On  |     |                 |     |           |     |
| Module  | Module1      |     |     |                 |     |           |     |
Sub Main()
|     |     | Dim           | dblVolatility# |     | =                   | 0.1234567 |     |
| --- | --- | ------------- | -------------- | --- | ------------------- | --------- | --- |
|     |     | Dim           | sglVolatility  |     | As                  | Single    |     |
|     |     | sglVolatility |                | =   | CSng(dblVolatility) |           |     |
Console.WriteLine(sglVolatility)
End Sub
| End | Module |     |     |     |     |     |     |
| --- | ------ | --- | --- | --- | --- | --- | --- |
Team-LRN

| 96                             |         |           |             |     |                              | IntroductiontoVB.NET |     |
| ------------------------------ | ------- | --------- | ----------- | --- | ---------------------------- | -------------------- | --- |
| Thisprogramprintsoutthevalueof |         |           |             |     | sglVolatilityas.1234567since |                      |     |
| no data                        | is lost | in the    | conversion. |     |                              |                      |     |
| VALIDATION                     |         | FUNCTIONS |             |     |                              |                      |     |
As shown in the table below, VB.NET’s validation functions allow
ustocheckthedatatypeofavaluebeforeweperformanoperation.
Youmayhavenoticedinpreviousprogramsthaterrorsoccurifthe
userenters a bad value. If, forexample, instead of entering 1000, a
| number | to be | used | in a calculation, |     | the user | enters | XYZ, the |
| ------ | ----- | ---- | ----------------- | --- | -------- | ------ | -------- |
program will end with an error since the calculation requires a
number,notastring.Validationfunctionsallowustocheckfirstto
seethattheuser-inputtedvaluesarecorrect.Ifnot,wecanprompt
| the user | with a | message | box | to reenter | the values | properly. |     |
| -------- | ------ | ------- | --- | ---------- | ---------- | --------- | --- |
Validation
| Function |     | Description |     |     |     | Example |     |
| -------- | --- | ----------- | --- | --- | --- | ------- | --- |
IsArray() ReturnsTrueorFalseindicating myBool¼ IsArray(myArray)
whetheravalueisareference
toanarray
IsConstant() ReturnsTrueorFalseindicating myBool¼IsConstant(myConstant)
whetheravalueisaconstant
| IsDate() | ReturnsTrueorFalseindicating |     |     |     | myBool¼IsDate(myDate) |     |     |
| -------- | ---------------------------- | --- | --- | --- | --------------------- | --- | --- |
whetheravalueisadate
IsNumeric() ReturnsTrueorFalseindicating myBool¼IsNumeric(myNumber)
whetheravalueisanumber
IsReference() ReturnsTrueorFalseindicating myBool¼IsReference(myRef)
whetheravalueisareference
| Here    | is a short    | program                          |       | that will | keep prompting        |           | the user to |
| ------- | ------------- | -------------------------------- | ----- | --------- | --------------------- | --------- | ----------- |
| enter a | valid numeric |                                  | value | until it  | gets the value.       |           |             |
| Sub     | Main()        |                                  |       |           |                       |           |             |
|         | Do While      | 1                                |       |           |                       |           |             |
|         |               | Console.WriteLine("Please        |       |           | enter a volatility:") |           |             |
|         |               | If IsNumeric(Console.ReadLine()) |       |           | Then                  |           |             |
|         |               | Console.WriteLine("Thank         |       |           | you for               | the valid | input.")    |
Exit Do
Else
|     |     | MsgBox("Please |     | enter | a valid value.") |     |     |
| --- | --- | -------------- | --- | ----- | ---------------- | --- | --- |
|     |     | End If         |     |       |                  |     |     |
Loop
| End | Sub |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
Team-LRN

Procedures 97
| DATE FUNCTIONS |     |     |     |     |
| -------------- | --- | --- | --- | --- |
Visual Basic.NET provides a wealth of date functions that can be
used to manipulate dates, which, as you can probably imagine,
becomeveryvaluableinmodelingfixed-incomesecurities,futures,
| and options. | Here are several | of the date | functions: |     |
| ------------ | ---------------- | ----------- | ---------- | --- |
Date
| Function  | Description          |     |                       | Example |
| --------- | -------------------- | --- | --------------------- | ------- |
| DateAdd() | Returnsadatetowhicha |     | dtMyDate¼(“d”,Now,30) |         |
specifictimeintervalhasbeen
added
| DateDiff()   | Returnsthenumberoftime       |     | lngMyDays¼                 | DateDiff(“d”, |
| ------------ | ---------------------------- | --- | -------------------------- | ------------- |
|              | intervalsbetweentwodates     |     | Now,dtMyExpiration)        |               |
| DateSerial() | Returnsadatefromayear,       |     | dtMyDate¼                  |               |
|              | month,andday                 |     | DateSerial(1,1,2003)       |               |
| DateValue()  | Returnsadatefromastring      |     | dtMyDate¼                  |               |
|              | representationofadate        |     | DateValue(“January1,2003”) |               |
| Day()        | Returnsanintegerrepresenting |     | intMyDay¼                  | Day(Now)      |
thedayofthemonthfrom1to
31
| Hour() | Returnsanintegerrepresenting |     | intMyHour¼ | Hour(Now) |
| ------ | ---------------------------- | --- | ---------- | --------- |
thehourofthedayfrom0to
23
Minute() Returnsanintegerrepresenting intMyMinute¼ Minute(Now)
theminuteofthehourfrom0
to59
| Month() | Returnsanintegerrepresenting |     | intMyMonth¼ | Month(Now) |
| ------- | ---------------------------- | --- | ----------- | ---------- |
themonthoftheyearfrom1
to12
| Now | Returnsthecurrentdateand |     | dtMyNow¼Now |     |
| --- | ------------------------ | --- | ----------- | --- |
timefromthecomputer’s
built-inclock
intMySecond¼
| Second() | Returnsanintegerrepresenting |     |     | Second(Now) |
| -------- | ---------------------------- | --- | --- | ----------- |
theminuteofthehourfrom0
to59
dtMyTime¼TimeOfDay
| TimeOfDay | Readsorsetsthetimefromyour |     |     |     |
| --------- | -------------------------- | --- | --- | --- |
computer’sclock
dtMyDate¼Today
| Today | Readsorsetsthedatefromyour |     |     |     |
| ----- | -------------------------- | --- | --- | --- |
computer’sclock
Weekday()
intMyDay¼
|     | Returnsanintegerrepresenting |     |     | Weekday(Now) |
| --- | ---------------------------- | --- | --- | ------------ |
thedayoftheweekfrom1to
7startingonSunday
intMyYear¼
| Year() | Returnsanintegerrepresenting |     |     | Year(Now) |
| ------ | ---------------------------- | --- | --- | --------- |
theyearfrom1to9999
Team-LRN

| 98  |     |     |     |     | IntroductiontoVB.NET |
| --- | --- | --- | --- | --- | -------------------- |
Here is a short program illustrating the use of the DateDiff()
function.
| Sub | Main()    |           |                 |             |              |
| --- | --------- | --------- | --------------- | ----------- | ------------ |
|     | Dim       | intMyDays | As Integer      |             |              |
|     | intMyDays |           | = DateDiff("d", | #1/7/2003#, | #4/23/2003#) |
Console.WriteLine(intMyDays)
| End          | Sub        |     |            |                 |           |
| ------------ | ---------- | --- | ---------- | --------------- | --------- |
| This program | calculates |     | the number | of days between | these two |
dates,106.Wecanconvertcalendardaystotradingdaysusingthe
formula:
| Trading   | days | = Calendar | days | - 2(Int(Calendar | days / 7)) |
| --------- | ---- | ---------- | ---- | ---------------- | ---------- |
| FINANCIAL |      | FUNCTIONS  |      |                  |            |
VB.NETalsohasseveralbuilt-infinancialfunctions,whichwewill
rarely, if ever, use in this book. They are, however, worth noting,
andsomearelistedinthetablebelow.InChapter10wewilllookat
how to create our own library of financial classes and functions.
Financial
| Function |     |     |     | Description |     |
| -------- | --- | --- | --- | ----------- | --- |
FV() Returnsthefuturevalueofanannuitygiventheinterestrate,numberof
payments,payment,optionalpresentvalue,andoptionalflag
specifyingwhenpaymentsaredue
Ipmt() Returnstheinterestpaymentforagivenperiodofanannuitygiventhe
interestrate,paymentperiod,numberofpayments,presentvalue,
optionalfuturevalue,andoptionalflagspecifyingwhenpaymentsare
due
IRR() Returnstheinternalrateofreturnforaseriesofcashflowsasanarray
MIRR() Returnsthemodifiedinternalrateofreturnforaseriesofcashflows
giventheinterestratepaidandinterestratereceived
NPer() Returnsthenumberofperiodsforanannuitygiventheinterestrate,
payment,presentvalue,optionalfuturevalueatmaturity,andoptional
flagspecifyingwhenpaymentsaredue
NPV() Returnsthenetpresentvalueofaninvestmentgiventheinterestrate
andcashflowvalues
Pmt() Returnsthepaymentforanannuitygiventheinterestrate,numberof
payments,presentvalue,optionalfuturevalue,andoptionalflag
specifyingwhenpaymentsaredue
Team-LRN

| Procedures |     |     |     |     |     |     | 99  |
| ---------- | --- | --- | --- | --- | --- | --- | --- |
Financial
| Function |     |     |     | Description |     |     |     |
| -------- | --- | --- | --- | ----------- | --- | --- | --- |
PPmt() Returnstheprincipalpaymentforagivenperiodofanannuitygiventhe
interestrate,paymentperiod,numberofpayments,presentvalue,
optionalfuturevalue,andoptionalflagspecifyingwhenpaymentsare
due
PV() Returnsthepresentvalueofanannuitygiventheinterestrate,numberof
payments,payment,optionalfuturevalue,andoptionalflagspecifying
whenpaymentsaredue
Rate() Returnstheinterestrateperperiodforanannuitygiventhenumberof
payments,payment,presentvalue,optionalfuturevalue,andoptional
flagspecifyingwhenpaymentsaredue
FV() Returnsthefuturevalueofanannuitygiventheinterestrate,numberof
payments,payment,optionalpresentvalue,andoptionalflag
specifyingwhenpaymentsaredue
| MsgBox | FUNCTION |     |     |     |     |     |     |
| ------ | -------- | --- | --- | --- | --- | --- | --- |
The MsgBox procedure displays a dialog box with a message, an
OKbutton,anoptionalicon,andatitle.MsgBoxcanalsoreturnthe
| value of | the button | pressed | by  | the user. |     |     |     |
| -------- | ---------- | ------- | --- | --------- | --- | --- | --- |
The title parameter is simply the text that appears across the
title bar of the message box. This defaults to your application’s
name. The MsgBox function can have one, two, or three buttons.
The function returns the value of the button your user pressed.
Beforewetalkaboutthesevalues,however,weneedtotakeaquick
| detour | and talk       | about VB.NET’s  |         | predefined | constants. |     |     |
| ------ | -------------- | --------------- | ------- | ---------- | ---------- | --- | --- |
| The    | following      | is an           | example | call       | to MsgBox: |     |     |
| Sub    | Main()         |                 |         |            |            |     |     |
|        | Dim myResponse | As MsgBoxResult |         |            |            |     |     |
myResponse = MsgBox("Continue?", vbYesNo + vbQuestion, "Continue")
| End            | Sub          |           |           |          |                 |              |     |
| -------------- | ------------ | --------- | --------- | -------- | --------------- | ------------ | --- |
| Or more        | simply,      |           |           |          |                 |              |     |
| MsgBox("Please |              | enter     | valid     | data.",, | "Option         | Calculator") |     |
| RANDOM         | NUMBER       |           | FUNCTIONS |          |                 |              |     |
| The Rnd()      | function     | in VB.NET |           | returns  | a random        | number from  | a   |
| uniform        | distribution | between   |           | 0 and    | 1. For example, |              |     |
Team-LRN

100 IntroductiontoVB.NET
Sub Main()
Randomize()
Dim myRnd As Double = Rnd()
Console.WriteLine(myRnd)
End Sub
Make sure to call the Randomize() function to initialize, or
“seed,” the random number generator. You only need to call
Randomize()once,andsoifyourprogramneedsrandomnumbers,
just include the call in the form load event.
Several mathematical methods have been developed for
accomplishing the task of generating standard normal deviates,
including the well-known rejection method with the Box-Muller
transformation, which can be converted into program code.
However, we prefer a much simpler method, as shown here:
Function StdNormRnd() As Double
Return Rnd() + Rnd() + Rnd() + Rnd() + Rnd() + Rnd() + Rnd() + Rnd() + _
Rnd() + Rnd() + Rnd() + Rnd() - 6
End Function
In all cases, this method will suffice, and the StdNormRand()
function above will be used in this book. Here are two other
functions for random numbers from distributions other than the
standard normal. First, normal distribution with mean and
standard deviation:
Function NormRnd(dblMean As Double, dblStdDev As Double) As Double
Return StdNormRnd() * dblStdDev + dblMean
End Function
And second, the lognormal:
Function LogNormalRnd(dblMean As Double, dblStdDev As Double) As Double
Return Exp(dblMean + dblStdDev * StdNormRnd())
End Function
IMPLIED VOLATILITY
Mostofteninfinancialmarkets,weareinterestedincalculatingthe
volatilityimpliedbyanoption’spriceasopposedtothepriceitself,
since the price can be observed in the market. Rather than passing
the stock price, strike, time, interest rate, and volatility into a
Team-LRN

Procedures 101
function to get the price, we would rather pass the option price,
stockprice,strike,time,andinterestrateintoafunctionandgetthe
volatility.
Analyzing and forecasting volatility is an important facet of
automated derivatives trading. In Chapter 5 we looked at some
ways of forecasting volatility based upon estimates of past, or
historical, volatility. If the implied volatility of an option, as
observed from its market price, deviates substantially from our
forecast of volatility between now and expiration, there may be a
tradingopportunity.Thatis,iftheimpliedvolatilityissubstantially
higher than our forecast, we may consider selling the option.
Alternatively, if the implied volatility is substantially lower than
our forecast, we may consider buying the option.
Let’saugmenttheprogramwestartedearlierinthischapterto
calculate the implied volatility of a call option given an options
symbol, a price for the underlying stock, and the price of the call
option. We will use some of the string manipulation functions to
determine the month of expiration and the strike price from an
option symbol according to the following tables:
ExpirationMonthCodes
Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
Calls A B C D E F G H I J K L
Puts M N O P Q R S T U V W X
StrikePriceCodes(Abbr.)
A B C D E F G H I J K L M
5 10 15 20 25 30 35 40 45 50 55 60 65
N O P Q R S T U V W X Y Z
70 75 80 85 90 95 100 7.5 12.5 17.5 22.5 27.5 32.5
Step 8 Add three more modules to your program to
hold the TimeTillExp(), ImpliedVolatilityCall(),
and StrikePrice() functions. Type in the function
Team-LRN

102 IntroductiontoVB.NET
definitions for the three functions as follows.
Alternatively you can copy and paste in the code
from the CD. Here is the code for the TimeTillExp()
function:
Module ExpirationTime
Public Function TimeTillExp(ByVal strOptionSym As String) As Double
’ Find the second to last character in the string.
Dim strMonthStrike As String5Right(strOptionSym, 2)
Dim chrMonth As Char5Left(strMonthStrike, 1)
Dim strMonth As String
Dim dtExpDate As Date
Select Case chrMonth
Case "A", "a", "M", "m" ’Use a Select...Case structure to
strMonth = "January" ’ transform the month character
Case "B", "b", "N", "n" ’ into the appropriate string.
strMonth = "February"
Case "C", "c", "O", "o"
strMonth = "March"
Case "D", "d", "P", "p"
strMonth = "April"
Case "E", "e", "Q", "q"
strMonth = "May"
Case "F", "f", "R", "r"
strMonth = "June"
Case "G", "g", "S", "s"
strMonth = "July"
Case "H", "h", "T", "t"
strMonth = "August"
Case "I", "i", "U", "u"
strMonth = "September"
Case "J", "j", "V", "v"
strMonth = "October"
Case "K", "k", "W", "w" ’ Assume all options expire on
strMonth = "November" ’ the 15th of the month. If the
Case "L", "l", "X", "x" ’ date has passed for the
strMonth = "December" ’ current year, find the date
End Select ’ for the following year.
dtExpDate = DateValue(strMonth & "15," & Year(Today()))
If Today() > dtExpDate Then _
dtExpDate = DateValue(strMonth & "15," & (Year(Today()) + 1))
Return (DateDiff(DateInterval.Day, Today(), dtExpDate)) / 365
End Function
End Module
Notice that the TimeTillExp() function makes use of several
functions we have looked at in this chapter, including Right() and
Left() to find the second-to-last character in the option symbol
string,DateValue() toconvert astringrepresentation ofa dateinto
a variable of data type Date, Year() to determine the year
corresponding to the date returned by Today(), and DateDiff() to
Team-LRN

| Procedures |     |     |     |     | 103 |
| ---------- | --- | --- | --- | --- | --- |
calculate the number of days between Today() and the expiration
date,assumingoptionsalwaysexpireonthefifteenthofthemonth,
| which                   | simplifies | this example. | Here is the | code for | the |
| ----------------------- | ---------- | ------------- | ----------- | -------- | --- |
| ImpliedVolatilityCall() |            | function:     |             |          |     |
Module ImpliedVol
Public Function ImpliedVolatilityCall(ByVal dblMarketPrice As Double,
|     |     |     | ByVal dblStock As  | Double, _ |     |
| --- | --- | --- | ------------------ | --------- | --- |
|     |     |     | ByVal dblStrike As | Double, _ |     |
|     |     |     | ByVal dblTime As   | Double, _ |     |
ByVal dblInterestRateAsDouble)_
AsDouble
DimImpliedVol,LowVol,HighVol,epsilon,mu,_
TheoreticalPrice,PreviousPriceAsDouble
HighVol=10
ImpliedVol=HighVol
TheoreticalPrice=BlackScholesCall(dblStock,dblStrike,_
dblTime,dblInterestRate,HighVol)
epsilon=TheoreticalPrice-dblMarketPrice
mu=TheoreticalPrice-PreviousPrice
DoWhile(Math.Abs(epsilon)>0.0000001)
IfMath.Abs(mu)<0.0000001ThenExitDo
Ifepsilon>0Then
ImpliedVol=HighVol
HighVol=HighVol-(HighVol-LowVol)/2
Else
LowVol=HighVol
HighVol=LowVol+(ImpliedVol-LowVol)/2
EndIf
PreviousPrice=TheoreticalPrice
TheoreticalPrice=BlackScholesCall(dblStock,dblStrike,_
dblTime,dblInterestRate,HighVol)
epsilon=TheoreticalPrice-dblMarketPrice
mu=TheoreticalPrice-PreviousPrice
Loop
ReturnHighVol
EndFunction
EndModule
And finally, here is the code for the StrikePrice() function:
| Module | Strike |     |     |     |     |
| ------ | ------ | --- | --- | --- | --- |
Public Function StrikePrice(ByVal strOptionSym As String) As Double
|     | Dim chrStrike | = Right(strOptionSym, | 1)  |     |     |
| --- | ------------- | --------------------- | --- | --- | --- |
|     | Select Case   | chrStrike             |     |     |     |
|     | Case "A",     | "a"                   |     |     |     |
|     | Return        | 5                     |     |     |     |
|     | Case "B",     | "b"                   |     |     |     |
|     | Return        | 10                    |     |     |     |
|     | Case "C",     | "c"                   |     |     |     |
|     | Return        | 15                    |     |     |     |
|     | Case "D",     | "d"                   |     |     |     |
|     | Return        | 20                    |     |     |     |
|     | Case "E",     | "e"                   |     |     |     |
Team-LRN

104 IntroductiontoVB.NET
Return 25
Case "F", "f"
Return 30
Case "G", "g"
Return 35
Case "H", "h"
Return 40
Case "I", "i"
Return 45
Case "J", "j"
Return 50
Case "K", "k"
Return 55
Case "L", "l"
Return 60
Case "M", "m"
Return 65
Case "N", "n"
Return 70
Case "O", "o"
Return 75
Case "P", "p"
Return 80
Case "Q", "q"
Return 85
Case "R", "r"
Return 90
Case "S", "s"
Return 95
Case "T", "t"
Return 100
Case "U", "u"
Return 7.5
Case "V", "v"
Return 12.5
Case "W", "w"
Return 17.5
Case "X", "x"
Return 22.5
Case "Y", "y"
Return 27.5
Case "Z", "z"
Return 32.5
End Select
End Function
End Module
Step 9 On your form, place four text boxes named
txtStockPrice, txtOptionSymbol, txtOptionPrice, and
txtImpliedVol. In the Button1_Click event, change
the code to the following:
Team-LRN

| Procedures |     |     |     |     |     |     |     | 105 |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
Private Sub Button1_Click(ByVal sender ...) Handles Button1.Click
|              | Dim                | dblImpVol        | As Double                             |                                |          |                 |               |          |
| ------------ | ------------------ | ---------------- | ------------------------------------- | ------------------------------ | -------- | --------------- | ------------- | -------- |
|              | Dim                | strOptionSymbol$ |                                       | = txtOptionSymbol.Text         |          |                 |               |          |
|              | Dim                | dblStockPrice#   | =                                     | txtStockPrice.Text             |          |                 |               |          |
|              | Dim                | dblOptionPrice#  |                                       | = txtOptionPrice.Text          |          |                 |               |          |
|              | Dim                | dblTimeTillExp#  |                                       | = TimeTillExp(strOptionSymbol) |          |                 |               |          |
|              | Dim                | dblStrike#       | = StrikePrice(strOptionSymbol)        |                                |          |                 |               |          |
|              | Dim                | dblRate#         | = 0.1                                 |                                |          |                 |               |          |
|              | dblImpVol          | =                | ImpliedVolatilityCall(dblOptionPrice, |                                |          |                 | _             |          |
|              |                    | dblStockPrice,   |                                       | dblStrike,                     |          | dblTimeTillExp, |               | dblRate) |
|              | txtImpliedVol.Text |                  | =                                     | Format(dblImpVol,              |          | 0.#####")       |               |          |
| End          | Sub                |                  |                                       |                                |          |                 |               |          |
| Notice       | that               | our code         | employs                               |                                | several  | function        | calls         | to our   |
| user-defined | functions          |                  | as well                               | as to the                      | Format() | function.       |               |          |
| Step         | 10                 | Run the          | program                               | (see                           | Figure   | 6.2).           | The results   | you      |
|              |                    | obtain           | will be                               | different                      | from     | the             | one shown     | in       |
|              |                    | Figure           | 6.2 since                             | the time                       | to       | expiration      | is            | always   |
|              |                    | changing.        | However,                              |                                | if you   | pick            | an expiration |          |
|              |                    | around           | 6 months                              | in the                         | future,  | a strike        | price         | of 40,   |
astockpriceof42,andanoptionpriceof4.76,your
|       |     | implied | volatility | should | be  | around | 20 percent. |     |
| ----- | --- | ------- | ---------- | ------ | --- | ------ | ----------- | --- |
| F I G | U R | E 6.2   |            |        |     |        |             |     |
Team-LRN

| 106 |     |     |     | IntroductiontoVB.NET |
| --- | --- | --- | --- | -------------------- |
SUMMARY
A procedure is a piece of code that performs a specific task.
Functions return a value to the calling statement. Subroutines are
exactlythesameasfunctionsexceptthattheydonotreturnavalue.
| In general, | functions | are preferred. |        |                     |
| ----------- | --------- | -------------- | ------ | ------------------- |
| Procedures  | are       | the building   | blocks | of VB.NET programs. |
Modularizingourcodeintoseparateprocedures,orblocksofcode,
enables reusability and cuts down on errors and debugging time.
Team-LRN

Procedures 107
PROBLEMS
1. What is a subroutine? What is a function? What is the
difference between a subroutine and a function?
2. Write a line of code that calculates the number of days
between January 7, 2003, and November 9, 2002, and
assigns the value to a variable named intNumDays.
3. Whatfunction wouldwe use to findthedate37days from
today?
4. Writealineofcodethatassignsthevalueofthelogof1.05
to a variable named dblReturn.
5. What function could we use to make sure that a user-
entered value is actually a number?
6. How could we print out a randomly drawn number from
the standard normal distribution to five decimal places?
Team-LRN

| 108     |     |     |     |     |     |     | IntroductiontoVB.NET |     |
| ------- | --- | --- | --- | --- | --- | --- | -------------------- | --- |
| PROJECT | 6.1 |     |     |     |     |     |                      |     |
CreateaVisualBasic.NETWindowsapplicationthatcalculatesthe
price and Greeks of a call option using the BlackScholesCall()
functionandthefunctionsfortheGreeksfoundontheCDincluded
withthisbook.Allowtheusertoinputanoptionsymbolandparse
| it as in the | chapter | example. |     |     |     |     |     |     |
| ------------ | ------- | -------- | --- | --- | --- | --- | --- | --- |
Theprojectshouldallowtheusertoinputthestockpriceand
the volatility. You can simply set the value of the interest rate in
| your code. | Your       | program   |     | should    | calculate    | the | other      | two input |
| ---------- | ---------- | --------- | --- | --------- | ------------ | --- | ---------- | --------- |
| arguments  | necessary  |           | to  | calculate | the prices   |     | and Greeks | of an     |
| option—the | expiration |           | and | the       | strike—from  |     | the option | symbol    |
| using the  | functions  | discussed |     | in        | the chapter. |     |            |           |
| PROJECT    | 6.2        |           |     |           |              |     |            |           |
The lognormal distribution assumes that the natural logarithm of
| the price-relative |     | from | time | t to | tþh is | drawn | from | a normal |
| ------------------ | --- | ---- | ---- | ---- | ------ | ----- | ---- | -------- |
distribution with meanmand standard deviations. The volatility
of a stock then is the sample standard deviation of the logs of the
price-relatives.
To simulate the price path of a stock, we need to first draw a
random number, Z, from the standard normal distribution. Using
thefollowingequation,wecanthenderivearandomstockpriceat
time tþh.
pffiffi
|     |     |     |     |     | e½m(h)þsZ h(cid:3) |     |     |     |
| --- | --- | --- | --- | --- | ------------------ | --- | --- | --- |
|     |     |     | S   | ¼ S |                    |     |     |     |
|     |     |     | tþh |     | t                  |     |     |     |
CreateaVBprogramthatwillallowtheusertoentertheinitial
stock price, the mean and standard deviation, and the change in
time,h,andwillgeneratearandomseriesof10successivepricesso
that each new price depends on the previous one. Remember that
volatility is anannualized numberbased on256 trading days, and
so a change in time of 1 day would be 1/256¼0.0039. Be sure to
includethisinyourcalculations.Also,usetheFormat()functionso
that your random prices print out in a readable fashion. Try using
the MsgBox and the IsNumeric() function to validate user inputs.
Team-LRN

C H A P T E R 7
Objects
T
husfar,wehavelookedatproceduralprogramminginChapter4
and event-driven programming in Chapters 5 and 6 using control
structures and procedures. Event-driven programming focuses on
the use of events, such as—among others—button clicks and form
loads, to control the execution of code. In event-driven program-
ming, different procedures run when different events happen. For
the remainder of the book, we will use things called objects and
object-oriented programming (OOP), although we will still use
events to illustrate code execution. OOP focuses on the use of
objectstocontrolprogramflow.Asyouwillsee,OOPenablesusto
performverylargeandcomplextaskswithjustafewlinesofcode.
OBJECTS AND CLASSES
Inpreviouschapters,wehavelookedatseveralclassesandobjects
inourprograms.Thebuttonsthatweputonourformsareobjects.
The button objects, known by default names like Button1, are
actuallyinstancesofthebuttonclass.Sowesaythatanobjectisan
instanceofaclass.Microsoft’s.NETFrameworkgivesushundreds
of premade classes, like buttons and text boxes as well as other
nonvisibleclasses,thatwecaninstantiateanduseinourprograms.
VB.NET is an object-oriented programming language and as
such uses reference types to encapsulate things. These things,
calledclasses,havebothdataandfunctionalitytiedtogetherwithin
their definitions. Classes have “member variables” that store data
and functionalities, or behaviors, held in procedures known as
methods or member functions. Classes may also have events associ-
atedwiththeminthewayabuttonhasaclick event.In aworking
program, different objects, which again are instances of classes,
109
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for terms of use.
Team-LRN

| 110 |     |     |     |     |     |     | IntroductiontoVB.NET |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------- | --- |
worktogether,ortalktoeachother,throughtheirrespectivepublic
interfaces.Thatistosay,privatedatawithinanobject,whichisnot
accessible from the outside world, is available to the outside
programmingenvironmentthroughtheobject’spublicinterface.
| For | example, | your | name | is  | a private | piece | of data about | you. |
| --- | -------- | ---- | ---- | --- | --------- | ----- | ------------- | ---- |
Noindividualscanknowyournameunlesstheyinteractwithyour
publicinterface,yourearsandyourvoice.Theycangetthevalueof
yournamebyaskingyouwhatyournameis,andthenyouwilltell
them the value of your private name data using your public voice
interface.Toextendtheanalogy,whenyouwereborn,yourparents
setthevalueofyournamemuchlikewecansetthetextpropertyof
abuttonatdesigntime.Ifyouwantedtochange,orset,yourname
| during           | your    | lifetime, |         | that is | at run  | time,        | you would | say |
| ---------------- | ------- | --------- | ------- | ------- | ------- | ------------ | --------- | --- |
| You.Name¼“Gordon |         |           | Gekko.” |         |         |              |           |     |
| In               | VB.NET, | we        | can     | create  | our own | user-defined | classes   | and |
create objects based on them. For example, we could create a class
calledStockOption.Inaprogram,anIBMApril80callwouldbean
| object, that | is,          | an instance |     | of the  | StockOption | class.       |             |     |
| ------------ | ------------ | ----------- | --- | ------- | ----------- | ------------ | ----------- | --- |
| The          | organization |             | of  | a class | can         | be difficult | to envision | to  |
programmers not used to thinking in terms of classes and objects.
| Here are | the elements |     | that | make | up a | class: |     |     |
| -------- | ------------ | --- | ---- | ---- | ---- | ------ | --- | --- |
Member
| Variables |     |     |                                             |     |     | Description |     |     |
| --------- | --- | --- | ------------------------------------------- | --- | --- | ----------- | --- | --- |
| Variable  |     |     | Simpledata                                  |     |     |             |     |     |
| Constant  |     |     | Read-onlyvaluessharedbyallobjectsintheclass |     |     |             |     |     |
Nestedtypes Othertypes––classes,structures,interfaces,enums,etc.
| Properties |     |     |                                               |     |     | Description |     |     |
| ---------- | --- | --- | --------------------------------------------- | --- | --- | ----------- | --- | --- |
| Property   |     |     | Valuesofmembervariablesaredefinedandretrieved |     |     |             |     |     |
throughpublicGetandSetmethodsofaproperty
| MemberFunctions |     |     |                                                 |     |     | Description |     |     |
| --------------- | --- | --- | ----------------------------------------------- | --- | --- | ----------- | --- | --- |
| Methods         |     |     | Procedurethatprovidestheobjectwithfunctionality |     |     |             |     |     |
| Constructor     |     |     | New()methodrunswhenanobjectisinstantiated       |     |     |             |     |     |
| Finalization    |     |     | Methodthatrunsjustbeforeanobjectisdestroyed     |     |     |             |     |     |
| Events          |     |     |                                                 |     |     | Description |     |     |
| Event           |     |     | Messagesentfromaneventsourcetolistenerobjects,  |     |     |             |     |     |
calledaneventreceiver
| In  | order | to use | OOP | in VB.NET, |     | we need to | understand | four |
| --- | ----- | ------ | --- | ---------- | --- | ---------- | ---------- | ---- |
main concepts of object-oriented programming: abstraction, en-
| capsulation, | inheritance, |     |     | and polymorphism. |     |     |     |     |
| ------------ | ------------ | --- | --- | ----------------- | --- | --- | --- | --- |
Team-LRN

Objects 111
ABSTRACTION
Abstraction is the process of creating an abstract model of a real-
world objector thing. Theprocessconsists oftakingtheattributes,
or properties, and functionalities, or methods, of an object and
| turning them | into logical | pieces of  | data and functionality. |                |
| ------------ | ------------ | ---------- | ----------------------- | -------------- |
| Again,       | let’s look   | at a stock | option. To turn         | a stock option |
into a class in VB.NET, we need to think about the properties of a
| stock option—that | is, | what nouns | are associated | with a stock |
| ----------------- | --- | ---------- | -------------- | ------------ |
option, like the option symbol, the strike price, and the expiration
date,aswellastheverbs,orfunctionalities,orbehaviors,ofastock
option, like calculating implied volatility or calculating and
returning the price. When we come up with a list of nouns, the
“whatitis”ofanobject,andverbs,the“whatitdoes,”wesaythat
theobjecthasbeenabstracted.Solet’sassumeforaminutewehave
fully abstracted a StockOption class into the following nouns and
verbs:
| Nouns        |     |                                        | Description |     |
| ------------ | --- | -------------------------------------- | ----------- | --- |
| Optionsymbol |     | Theoptionsymbolconsistsofasymbolforthe |             |     |
underlyingsymbol,asymbolforthemonth,anda
symbolforthestrikeprice
| Expirationmonth       |     | Derivedfromtheoptionsymbol                  |     |     |
| --------------------- | --- | ------------------------------------------- | --- | --- |
| Strikeprice           |     | Derivedfromtheoptionsymbol                  |     |     |
| Underlyingsymbol      |     | Derivedfromtheoptionsymbol                  |     |     |
| Priceoftheoption      |     | WewillusetheBlack-Scholesmodeltosettheprice |     |     |
| Marketprice           |     | Theoption’spriceobservedinthemarketplace    |     |     |
| Volatilityoftheoption |     | Wewillneedtosetthevolatility                |     |     |
| Interestrate          |     | Wewillneedtosettheinterestrate              |     |     |
| Greeks                |     | WewillneedtocalculatetheGreeks              |     |     |
| Timetillexpiration    |     | Calculatedfromtheexpirationmonth            |     |     |
| Daystillexpiration    |     | Calculatedfromtheexpirationmonth            |     |     |
Calculatedfromthemarketprice
|                       | Verbs |                                        | Description |     |
| --------------------- | ----- | -------------------------------------- | ----------- | --- |
| Deriveexpirationmonth |       | Symbolformonthisfoundintheoptionsymbol |             |     |
Derivestrikeprice Symbolforstrikepriceisfoundintheoptionsymbol
Deriveunderlyingsymbol Symbolfortheunderlyingsymbolisfoundintheoption
symbol
| Calculateprice  |     | NeedaproceduretocalculateBlack-Scholesprice |     |     |
| --------------- | --- | ------------------------------------------- | --- | --- |
| CalculateGreeks |     | NeedprocedurestocalculatetheGreeks          |     |     |
Calculatetradingdaysand Needaproceduretocalculatethedaysandtimetill
| timetillexpiration |     | expirationusingtradingdays |     |     |
| ------------------ | --- | -------------------------- | --- | --- |
Calculatetheimpliedvolatility Needaproceduretocalculatetheimpliedvolatility
Team-LRN

112 IntroductiontoVB.NET
ENCAPSULATION
Encapsulation refers to the process of containing the abstracted
propertiesandmethodsintoaclass,exposingtotheoutsideworld
only those methods that absolutely must be exposed, which are
then known collectively as the class’s public interface. So classes
hide the implementation of their properties and methods and
communicate with the external programming environment
through the public interface. In this way encapsulation protects
the object from being tampered with and frees the programmer
from having to know the details of the object’s implementation.
In our StockOption example the outside programming
environment does not need to be exposed to the method of
calculating the price, and so this functionality is encapsulated and
made unavailable to the outside world. This idea will become
clearer as we go along. For right now let’s look at the code to
encapsulate just the private variable named strOptionSym to hold
the option symbol in the StockOption class, along with a public
property called Symbol to get the value of the strOptionSym.
Let’s create a StockOption class.
Step 1 Open a new Windows application named
OptionObject and add a single label, named Label1,
to Form1.
Step 2 Under the Project menu item, select Add Class. A
new class code window will appear.
Step 3 Add the following code to the StockOption class:
Public Class StockOption
Private strOptionSym As String
Public Sub New (ByVal strSymbol As String)
strOptionSym = strSymbol
End Sub
Public ReadOnly Property Symbol()
Get
Return strOptionSym
End Get
End Property
End Class
Notice that the class name is StockOption. Be careful.
StockOptionisaclass,notanobject.Inthisexample,strOptionSym
Team-LRN

| Objects |     |     |     |     |     |     |     |     | 113 |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
isprivate,andsowewillnotbeabletogetorsetthevalueofitfrom
| outside      | the object |         | itself. We | can,        | however, |        | set   | the value | of     |
| ------------ | ---------- | ------- | ---------- | ----------- | -------- | ------ | ----- | --------- | ------ |
| strOptionSym |            | through | the        | constructor |          | method | known |           | as the |
New() subroutine.
SoNew()iscalledtheconstructormethod.Anytimeanobject
is instantiated, or born, using the New keyword, the object’s
constructor method executes. In this case the public subroutine
New() accepts a string and sets the value of strOptionSym, our
private member variable, equal to it. By requiring that an option
symbolbepassedtotheconstructormethod,wepreventourselves,
or any other programmer using this class, from creating a new
| option object | without |     | a symbol. |     |     |     |     |     |     |
| ------------- | ------- | --- | --------- | --- | --- | --- | --- | --- | --- |
AlsonoticethatwecangetthevalueofstrOptionSymthrough
the public property Symbol, which has a Get method within it.
| Public properties |          | provide   |              | us with      | access   | to      | private  | member  |         |
| ----------------- | -------- | --------- | ------------ | ------------ | -------- | ------- | -------- | ------- | ------- |
| variables         | through  | Get       | and          | Set methods. |          | Notice, | however, |         | that    |
| our Symbol        | property |           | is ReadOnly, |              | implying |         | that     | once    | the     |
| strOptionSym      | member   |           | variable     | is           | set via  | the     | New()    | method, | it      |
| cannot be         | changed. |           |              |              |          |         |          |         |         |
| Creating          | a        | reference | type,        | such         | as an    | object, | out      | of      | a class |
is a two-stage process. First, we declare the name of the object,
which will actually then be a variable that holds a reference to
thelocationoftheobjectinmemory.Second,wecreateaninstance
of a class using the New keyword. This is when the constructor
| method | will run. | Here | is an | example | of  | showing |     | the two-stage |     |
| ------ | --------- | ---- | ----- | ------- | --- | ------- | --- | ------------- | --- |
process:
| Dim      | myOption | As  | StockOption          |     |     |     |     |     |     |
| -------- | -------- | --- | -------------------- | --- | --- | --- | --- | --- | --- |
| myOption | =        | New | StockOption("IBMDP") |     |     |     |     |     |     |
Alternatively,wecanaccomplishtheprocessusingonelineof
code:
| Dim | myOption | As  | New StockOption("IBMDP") |     |     |     |     |     |     |
| --- | -------- | --- | ------------------------ | --- | --- | --- | --- | --- | --- |
Indifferentsituationsitwillbeadvantageoustouseoneorthe
other of these two methods. We will use both methods over the
course of the book. As with variables, it is important to pay close
attentiontothescopeofyourreferencetypes,whichwilldictatein
| many cases | the | method | of instantiation. |     |     |     |     |     |     |
| ---------- | --- | ------ | ----------------- | --- | --- | --- | --- | --- | --- |
Team-LRN

| 114  |                                              |     |        |     | IntroductiontoVB.NET |
| ---- | -------------------------------------------- | --- | ------ | --- | -------------------- |
| Step | 4 IntheForm1codewindow,addthefollowingcodeto |     |        |     |                      |
|      | the Form1_Load                               |     | event: |     |                      |
Private Sub Form1_Load(ByVal sender As...) Handles MyBase.Load
|     | Dim         | myOption | As New StockOption("IBMDP") |     |     |
| --- | ----------- | -------- | --------------------------- | --- | --- |
|     | Label1.Text |          | = myOption.Symbol           |     |     |
End Sub
| Now when | the program | is  | running, | myOption | is the object, |
| -------- | ----------- | --- | -------- | -------- | -------------- |
whereas StockOption is the class. We set the value of strOption-
Symbol by passing a string into the constructor, New(), as shown.
| Step | 5       |         |             |       |     |
| ---- | ------- | ------- | ----------- | ----- | --- |
|      | Run the | program | (see Figure | 7.1). |     |
The content of this program is not earth-shattering of course,
but congratulate yourself nonetheless; you have just created your
firstclass, yourfirstobject, and yourfirstobject-orientedprogram.
| Of course, | a stock | option | consists | of a lot | more data and |
| ---------- | ------- | ------ | -------- | -------- | ------------- |
functionalitythanjustasymbol.Also,aswesawinourabstraction
ofastockoption,someofthisotherdatamightnotbesetfromthe
outside, but rather calculated internally. For example, we would
obviously prefer to have the option object derive the strike price
internallyfromtheoptionsymbolratherthanrequirethatwesetit
explicitlyfromtheoutside.Let’stakealookatthefullydeveloped
| StockOption | class found                                       | on the | CD. |     |     |
| ----------- | ------------------------------------------------- | ------ | --- | --- | --- |
| Step        | 6 CleartheStockOptionclassofthepreviousdefinition |        |     |     |     |
andpasteinthefullStockOptionclasscodefromthe
|       | StockOption.txt |     | file found | on the CD. |     |
| ----- | --------------- | --- | ---------- | ---------- | --- |
| F I G | U R E 7.1       |     |            |            |     |
Team-LRN

| Objects |     |           |       |            |         |      |     |        | 115 |
| ------- | --- | --------- | ----- | ---------- | ------- | ---- | --- | ------ | --- |
| Step    | 7   | Add       | three | labels     | to your | form | and | change | the |
|         |     | Form_Load |       | event code | to:     |      |     |        |     |
Private Sub Form1_Load(ByVal sender As ...) Handles MyBase.Load
|       | Dim         | MyOption | As                    | StockOption5New |        | StockOption("IBMDP") |      |          |     |
| ----- | ----------- | -------- | --------------------- | --------------- | ------ | -------------------- | ---- | -------- | --- |
|       | Label1.Text |          | = MyOption.Underlying |                 |        |                      |      |          |     |
|       | Label2.Text |          | = MyOption.ExpMonth   |                 |        |                      |      |          |     |
|       | Label3.Text |          | = MyOption.Strike     |                 |        |                      |      |          |     |
|       | Label4.Text |          | = MyOption.BSPrice    |                 |        |                      |      |          |     |
| End   | Sub         |          |                       |                 |        |                      |      |          |     |
| Step  | 8           | Run the  | program               | (see            | Figure | 7.2).                |      |          |     |
| F I G | U R         | E 7.2    |                       |                 |        |                      |      |          |     |
| Once  | we          | have     | completely            | turned          |        | our model            | into | computer |     |
code, we say that the class has been encapsulated. A major benefit
| of OOP  | is that | because |      | the data  | and | methods | encapsulated |     | in   |
| ------- | ------- | ------- | ---- | --------- | --- | ------- | ------------ | --- | ---- |
| classes | are so  | closely | tied | together, |     | we do   | not need     | to  | pass |
argumentsbackandforthasinputstoprocedures.Rather,member
| functions | can | access | member |     | variables | directly |     | within | their |
| --------- | --- | ------ | ------ | --- | --------- | -------- | --- | ------ | ----- |
definitions. In the StockOption class code, notice that the member
methods, such as SetStrikePrice, are able to access the member
variablesdirectly.AlsonoticethattheBlackScholesPrice()method,
| which | contains | a   | method | definition |     | setting | the | price | of all |
| ----- | -------- | --- | ------ | ---------- | --- | ------- | --- | ----- | ------ |
StockOptionobjectsto1.11,isoverridable.Thismeansthatmethod
definitions in classes that inherit from the StockOption class may
override the definition in the base, or parent, StockOption class.
Team-LRN

| 116 |     |     |     | IntroductiontoVB.NET |     |     |
| --- | --- | --- | --- | -------------------- | --- | --- |
INHERITANCE
| The best | way to understand |     | inheritance | is to | continue | the |
| -------- | ----------------- | --- | ----------- | ----- | -------- | --- |
StockOption object example. A stock option, through abstraction
and encapsulation into a class and then instantiation, can be an
| object | in VB.NET. This | object | built | on the StockOption |     | class |
| ------ | --------------- | ------ | ----- | ------------------ | --- | ----- |
containsonlythosepropertiesandmethodsthatarecommontoall
stock options. Certainly the method of calculating the price is not
common to all stock options. We calculate the price of a call
| differently | than we calculate | the | price | of a put. |     |     |
| ----------- | ----------------- | --- | ----- | --------- | --- | --- |
Acalloptionisastockoption.Assuch,ithasmethodsthatare
notcommontoallstockoptions,suchascalculationofitsprice.So
rather than create a whole new CallOption class, we can create a
derived, or child, class, called CallOption, that inherits all the
| properties | and methods | from | the base, | or parent, | StockOption |     |
| ---------- | ----------- | ---- | --------- | ---------- | ----------- | --- |
class. The CallOption class then may have some added properties
orfunctionalities,suchaspricingalgorithmsthatareuniquetocall
optionsonstocks.Likewise,wecouldcreateaPutOptionclassthat
inherits from the base StockOption class and has its own specific
| functionalities | added | on. |     |     |     |     |
| --------------- | ----- | --- | --- | --- | --- | --- |
Continuing on then, an American call option is a call option.
So we could create a derived class called AmerCallOption that
inherits all the properties and methods from the base CallOption
class and so on. For the purposes of this book, however, we will
| stop with | the CallOption | class. |     |     |     |     |
| --------- | -------------- | ------ | --- | --- | --- | --- |
A derived class can add functionality beyond that of the base
class, and it can also override methods of its base class. That is, a
derivedclassmayreplaceamemberfunctiondefinitionofthebase
class with its own new definition. In such cases, the base class
definitionshouldindicatewhichifanymethodsmaybeoverridden
inderivedclassesusingtheOverridableinheritancemodifier.Here
| is a table | of the inheritance | modifiers: |     |     |     |     |
| ---------- | ------------------ | ---------- | --- | --- | --- | --- |
Inheritance
| Modifier |     |     | Description |     |     |     |
| -------- | --- | --- | ----------- | --- | --- | --- |
MustInherit Indicatesanabstractclassthatcannotbeinstantiated,onlyinherited
MustOverride Mustbeoverriddeninthederivedclass.NecessitatesaMustInherit
class
| Overridable    | Maybeoverriddeninthederivedclass        |     |     |     |     |     |
| -------------- | --------------------------------------- | --- | --- | --- | --- | --- |
| NotOverridable | Preventsoverridinginderivedclasses      |     |     |     |     |     |
| Overrides      | Indicatesoverridingabaseclassdefinition |     |     |     |     |     |
| Shadows        | Hasthesamenameasamethodinthebaseclass   |     |     |     |     |     |
Team-LRN

Objects 117
In our program, let’s create a derived class CallOption that
will inherit all the member variables and methods from the base,
StockOption class.
Step 9 In your program,add anotherclassmodule andto it
add the following code:
Public Class CallOption
Inherits StockOption
Public Sub New(ByVal strSymbol As String)
MyBase.New(strSymbol)
End Sub
Protected Overrides Sub BlackScholesPrice()
Dim d1 As Double, d2 As Double, Nd1 As Double, Nd2 As Double
d1 = (Math.Log(dblStock / dblStrike) + (dblInterestRate + _
(dblSigma ^ 2) / 2) * dblTimeTillExp) / _
(dblSigma * Math.Sqrt(dblTimeTillExp))
d2 = d1 - dblSigma * Math.Sqrt(dblTimeTillExp)
Nd1 = NormCDF(d1)
Nd2 = NormCDF(d2)
dblBSPrice = dblStock * Nd1 - dblStrike * _
Math.Exp(-dblInterestRate * dblTimeTillExp) * Nd2
End Sub
End Class
In the derived class CallOption, the BlackScholesCall()
methoddefinitionoverridesthedefinitioninthebaseStockOption
class. Again, notice that the procedure in the CallOption class
calledBlackScholesPrice()isamemberfunctionand,therefore,has
direct access to the member variables.
Also, because constructor methods are not inherited, we
neededtoaddaNew()methodtoourderivedCallOptionclassthat
explicitly calls the constructor of the base class using the MyBase
keyword. The MyBase keyword always references the base class
within any derived class.
Step 10 Change the Form_Load event code to:
Private Sub Form1_Load(ByVal sender As ...) Handles MyBase.Load
Dim MyCallOption As CallOption = New CallOption("IBMDP")
Label1.Text = MyCallOption.Underlying
Label2.Text = MyCallOption.ExpMonth
Label3.Text = MyCallOption.Strike
MyCallOption.IntRate50.1 ’ default IntRate = .1
Team-LRN

| 118   |                         |     |                                |      |         | IntroductiontoVB.NET |           |           |
| ----- | ----------------------- | --- | ------------------------------ | ---- | ------- | -------------------- | --------- | --------- |
| F I G | U R E                   | 7.3 |                                |      |         |                      |           |           |
|       | MyCallOption.StockPrice |     |                                | =    | 80      |                      |           |           |
|       | MyCallOption.Volatility |     |                                | =    | 0.25    |                      |           |           |
|       | Label4.Text             |     | = Format(MyCallOption.BSPrice, |      |         |                      | "#.0000") |           |
| End   | Sub                     |     |                                |      |         |                      |           |           |
| Step  | 11 Run                  | the | program                        | (see | Figure  | 7.3).                |           |           |
| As    | we mentioned            |     | before,                        | your | program | will                 | have a    | different |
pricefromtheoneshowninFigure7.3sincethetimetillexpiration
changes as time moves forward. Also, the StockOption class sets
the IntRate¼.1 by default, and so in future programs we will not
| need to | set it explicitly. |     |     |     |     |     |     |     |
| ------- | ------------------ | --- | --- | --- | --- | --- | --- | --- |
POLYMORPHISM
| Polymorphism |     | allows | us to | have one | method | name, | or  | function |
| ------------ | --- | ------ | ----- | -------- | ------ | ----- | --- | -------- |
name, used in different derived classes, but yet have different
implementations, or functionalities, associated with that name
depending on the class. In our CallOption class above, and the
| PutOption | class | also | found | on the | CD, | for example, | we  | have |
| --------- | ----- | ---- | ----- | ------ | --- | ------------ | --- | ---- |
inherited a BlackScholesPrice() method from the parent Stock-
Optionclass,butyeteachofthederivedclasseshasitsownmethod
for calculation since the equations for Black-Scholes call and put
| pricing | are different. |     |     |     |     |     |     |     |
| ------- | -------------- | --- | --- | --- | --- | --- | --- | --- |
EVENTS
Events allow an object, called the publisher or source, to notify
other objects, called the subscribers or receivers, when something
Team-LRN

| Objects |     |     |     |     |     |     |     |     | 119 |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
happens. The most intuitive event is the button Click event. When
| theuserclicksa |     | button,theClickeventfires,andaswehaveseen, |     |     |     |     |     |     |     |
| -------------- | --- | ------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
we can write code that will execute when this happens. Creating
events in VB.NET is really quite easy. Here are the four steps to
| create | an event: |           |            |                |        |           |                |     |        |
| ------ | --------- | --------- | ---------- | -------------- | ------ | --------- | -------------- | --- | ------ |
|        | 1. Create | an        | event      | member         | in the | publisher | class.         |     |        |
|        | 2. Within | the       | subscriber |                | class, | create    | an instance    |     | of the |
|        | publisher |           | using      | the WithEvents |        | keyword.  |                |     |        |
|        | 3. Fire   | the event | in         | the publisher  |        | using     | the RaiseEvent |     | key-   |
word.
|     | 4. Create | a method |       | in the | subscriber |          | that will run | when | the |
| --- | --------- | -------- | ----- | ------ | ---------- | -------- | ------------- | ---- | --- |
|     | event     | is fired | using | the    | Handles    | keyword. |               |      |     |
We will not review events further. So for more information on
| events, | we refer | you       | to the | VB.NET |     | help files. |     |     |     |
| ------- | -------- | --------- | ------ | ------ | --- | ----------- | --- | --- | --- |
| ACCESS  |          | MODIFIERS |        |        |     |             |     |     |     |
InthecompleteStockOptionclass,wehavechangedallthePrivate
access modifiers to Protected, because Private member variables
and Private methods are not accessible in derived classes. Take a
| look | at the    | BlackScholesPrice() |     |           | method:             |         |     |            |     |
| ---- | --------- | ------------------- | --- | --------- | ------------------- | ------- | --- | ---------- | --- |
|      | Protected | Overridable         |     | Sub       | BlackScholesPrice() |         |     |            |     |
|      | Protected | member              |     | variables | and                 | methods | are | accessible | in  |
derived classes. So since we intended to create a derived class,
CallOption,fromourbaseclassStockOption,weneededtousethe
Protectedaccessmodifier.Herearetheaccessmodifiersforclasses:
Access
| Modifier |     |                    |     |     |     | Scope |     |     |     |
| -------- | --- | ------------------ | --- | --- | --- | ----- | --- | --- | --- |
| Public   |     | Accessibleanywhere |     |     |     |       |     |     |     |
Private Accessibleonlybymethodsoftheclass.Derivedclassmethodscannot
accessPrivatepropertiesormethods
| Protected |     | Accessiblebybaseclassandderivedclassmethods |     |     |     |     |     |     |     |
| --------- | --- | ------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
Friend Accessiblebybaseclassmethods,derivedclassmethods,andcertain
otherclasses
Shared Sharedmembersarecallabledirectlyfromtheclasswithoutrequiringan
instanceoftheclass
Team-LRN

120 IntroductiontoVB.NET
OVERLOADING
ThecompleteStockOptionclassalsocontainstwoNew()methods.
This is an example of method overloading. We can create as many
methodswiththesamenameinasingleclassasareneededaslong
asthelistsofinputargumentsaredifferentfromoneanother,either
in number of arguments or in the data types of the arguments.
Methods other than New() that are overloaded must include
the Overloads keyword. Although not illustrated in the code for
StockOption, an example would be:
Public Overloads Function NormCDF(ByVal x As Integer) As Double
where this function overloads the original NormCDF() function
because it differs in its parameter list.
Public Overloads Function NormCDF(ByVal x As Double) As Double
NOTHING
Because the name of an object is really a variable holding a
reference to the location of the object in memory, we can assign a
value of Nothing to the object, which allows the .NET garbage
collector to dispose of the unused memory. This method disposes
of the instance of the object, but not the name of the object.
MyOption = Nothing
CALCULATING AT-THE-MONEY VOLATILITY
Very rarely, if ever, in financial markets can we look at an
at-the-money (ATM) option and calculate its implied volatility.
Yet in our discussions about markets, we often talk in terms of
ATM volatility. Quantitative research papers frequently use time
series of ATM volatility, and what’s more, many mathematical
models assume the reader understands that volatility means
at-the-money volatility. But what is ATM volatility if it cannot
beobservedinthemarketplace?TheansweristhatATMvolatility
is a value we must calculate from the implied volatilities of the
puts and calls with the strikes surrounding the ATM value—those
Team-LRN

| Objects |     |     |     |     |     |     |     | 121 |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- |
nearest, above and below, the price of the underlying symbol.
Furthermore,sincetimeisalwaysmovingforwardandexpirations
are continuously drawing nearer, we have to include volatilities
| for the | nearby and | second | nearby |     | expirations |     | to come | up with |
| ------- | ---------- | ------ | ------ | --- | ----------- | --- | ------- | ------- |
a constant-maturity ATM volatility. That is, if we wish to refer
| to an | ATM volatility |     | that | is, for | example, |     | 30 calendar | days |
| ----- | -------------- | --- | ---- | ------- | -------- | --- | ----------- | ---- |
out (which is somewhat difficult to envision since only on 1 day
a month will an expiration be exactly 30 days away), we need a
| mathematical | construct    |             | to interpolate |           |       | between | options     | in the    |
| ------------ | ------------ | ----------- | -------------- | --------- | ----- | ------- | ----------- | --------- |
| nearby       | and second   | nearby      | expirations.   |           |       |         |             |           |
| In           | this section |             | we will        | use       | the   | Chicago | Board       | Options   |
| Exchange’s   | market       |             | volatility     | index     | (VIX) |         | methodology | for       |
| calculating  | ATM          | volatility. | As             | described |       | by      | Robert      | Whaley in |
his paper “The Investor Fear Gauge” (2000), the VIX represents
| the ATM  | volatility | for | the    | S&P      | 100 (OEX) |        | index. The | CBOE       |
| -------- | ---------- | --- | ------ | -------- | --------- | ------ | ---------- | ---------- |
| computes | the value  |     | of the | VIX from | the       | prices | of         | eight puts |
and calls with the strikes nearest, above and below, the price
| of the | underlying | security |     | for the | nearby | and | second | nearby |
| ------ | ---------- | -------- | --- | ------- | ------ | --- | ------ | ------ |
expirations (Whaley, 2000, p. 1). The implied volatilities derived
from these eight options are then weighted to form a 30-calendar-
day, 22-trading-day, constant-maturity, ATM implied volatility for
the OEX index. The prices used for these eight options will be the
| midpoints | between | the | respective | bids | and | offers. |     |     |
| --------- | ------- | --- | ---------- | ---- | --- | ------- | --- | --- |
While the implied volatilities for these eight options should
| be calculated | using | a         | cash dividend–adjusted |       |       |           | binomial | method   |
| ------------- | ----- | --------- | ---------------------- | ----- | ----- | --------- | -------- | -------- |
| to account    | for   | the facts | that                   | OEX   | index | options   | are      | American |
| style and     | that  | the       | underlying             | index |       | portfolio | pays     | discrete |
cash dividends, we will use the traditional Black-Scholes model
for European options to derive all required implied volatilities.
Forecasting dividends for the 100 stocks that make up the index
is beyond the scope of this book. As you can imagine, this will,
of course, lead to small deviations from the value of the actual
VIX.
| If      | it happens     | that | the   | implied  | volatilities |       | for these | eight |
| ------- | -------------- | ---- | ----- | -------- | ------------ | ----- | --------- | ----- |
| options | are calculated |      | using | calendar |              | days, | then each | must  |
be converted to a trading-day implied volatility. If the number
| of calendar | days | to  | expiration | is  | Days | C and | the number | of  |
| ----------- | ---- | --- | ---------- | --- | ---- | ----- | ---------- | --- |
trading days till expiration is Days , then Days is calculated as
|     |     |     |     |     | T   |     | T   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Team-LRN

| 122 |     |     |     |     |     | IntroductiontoVB.NET |
| --- | --- | --- | --- | --- | --- | -------------------- |
follows:
|     |     | Days | ¼ Days | (cid:1)2(cid:2)int(Days | =7) |     |
| --- | --- | ---- | ------ | ----------------------- | --- | --- |
|     |     |      | T      | C                       | C   |     |
Toconvertcalendar-dayvolatilitiestotrading-dayvolatilities,
wemultiplytheeightbythesquarerootoftheratioofthenumber
| of calendar | days | to the | number | of trading days | thusly: |     |
| ----------- | ---- | ------ | ------ | --------------- | ------- | --- |
 rffiffiffiffiffiffiffi!
N
|     |     |     | s ¼s | C   |     |     |
| --- | --- | --- | ---- | --- | --- | --- |
|     |     |     | T    | C   |     |     |
N
T
Fortunately, the StockOption class already assumes trading days
| for time | to expiration, |     | and | so we will not | need | to make this |
| -------- | -------------- | --- | --- | -------------- | ---- | ------------ |
adjustment.
In practice, the risk-free interest rate we should use in the
calculation is the continuous yield of the T-bill with the maturity
most closely matching the option’s expiration. If the time till
expirationisshorterthan30days,however,the30dayT-billrateis
used. The StockOption class sets the default interest rate to .1, and
| we will | just use | that. |     |     |     |     |
| ------- | -------- | ----- | --- | --- | --- | --- |
Thecalculationswillbeclearerifwelookatanexample.Let’s
assume today is February 3 and the OEX index is at 435.70. The
optionswiththeneareststrikesaboveandbelowwouldbethe435s
and 440s.If we takethe midpoints of thebids and asksof theputs
and calls for the next two expirations, February 16 and March 16,
for both these strikes, we will have eight option prices and eight
| trading-day | volatilities, |     | as shown | in Figure | 7.4. |     |
| ----------- | ------------- | --- | -------- | --------- | ---- | --- |
Nowweneedtoaveragetheeightimpliedvolatilitiestoarrive
at a single ATM volatility 22 days hence, denoted by the gray X in
Figure 7.5. First we average the call and put volatilities in each of
the quadrants, respectively, to reduce the number of volatilities to
four.
N
| In Figure | 7.5, | the | subscript | refers to | the nearby | expiration |
| --------- | ---- | --- | --------- | --------- | ---------- | ---------- |
andStothesecondnearby,andsubscriptAandBmeanaboveand
| below the | current | price | of  | the underlying. | In  | the upcoming |
| --------- | ------- | ----- | --- | --------------- | --- | ------------ |
formulas,Pstandsforthepriceoftheunderlying,andXmeansthe
strike price, so that X refers to the strike price above the price of
A
X
the underlying security and B to the strike price below. Also in
upcomingformulas,Nreferstothenumberoftradingdays,sothat
Team-LRN

Objects 123
| F I G U | R E 7.4 |     |     |
| ------- | ------- | --- | --- |
N and N refer to the numberof trading days till the nearby and
| N S           |              |               |     |
| ------------- | ------------ | ------------- | --- |
| second nearby | expirations, | respectively. |     |
Second we average the two volatilities across each of the two
expirations. The average of the two nearby volatilities to arrive at
| the ATM volatility | for the | nearby expiration | is found using  |
| ------------------ | ------- | ----------------- | --------------- |
|                    |         | (cid:2) (cid:3)   | (cid:2) (cid:3) |
|                    |         | X A (cid:1)P      | P (cid:1)X B    |
|                    | s ¼s    | þs                |                 |
|                    | N N,B   | N,A               |                 |
|                    |         | X A (cid:1)X B    | X A (cid:1)X B  |
| F I G U            | R E 7.5 |                   |                 |
Team-LRN

| 124 |     |     |     |     | IntroductiontoVB.NET |     |     |
| --- | --- | --- | --- | --- | -------------------- | --- | --- |
and the ATM volatility for the second nearby expiration is found
using
|           |                     | (cid:2)     | (cid:3)    | (cid:2)       | (cid:3)  |              |     |
| --------- | ------------------- | ----------- | ---------- | ------------- | -------- | ------------ | --- |
|           |                     | X (cid:1)P  |            | P             | (cid:1)X |              |     |
|           | s ¼s                | A           | þs         |               | B        |              |     |
|           | S S,B               |             |            | S,A           |          |              |     |
|           |                     | X (cid:1)X  |            | X             | (cid:1)X |              |     |
|           |                     | A           | B          |               | A B      |              |     |
| as shown  | in Figure 7.6.      |             |            |               |          |              |     |
| Third     | and last, we        | average     | the        | two remaining |          | volatilities | to  |
| arrive at | a constant-maturity |             | 22 trading | hence,        | using    |              |     |
|           |                     | (cid:2)     | (cid:3)    | (cid:2)       | (cid:3)  |              |     |
|           |                     | N (cid:1)22 |            | 22(cid:1)N    |          |              |     |
|           |                     | S           |            |               | N        |              |     |
|           | VIX ¼s N            |             | þs         | S             |          |              |     |
|           |                     | N (cid:1)N  |            | N             | (cid:1)N |              |     |
|           |                     | S           | N          | S             | N        |              |     |
as shown in Figure 7.7. (These calculations are all taken from
| Whaley, | 2000, p. 12ff.) |        |         |     |             |      |      |
| ------- | --------------- | ------ | ------- | --- | ----------- | ---- | ---- |
| Now     | let’s create a  | VB.NET | Windows |     | application | that | uses |
optionobjectstocalculatetheconstant-maturityATMvolatilityfor
| IBM using | the VIX methodology, |        | again | assuming | no          | dividends. |        |
| --------- | -------------------- | ------ | ----- | -------- | ----------- | ---------- | ------ |
| Step      | 1                    |        |       |          |             |            |        |
|           | Open a new           | VB.NET |       | Windows  | application |            | called |
ATMExample.
| F I G | U R E 7.6 |     |     |     |     |     |     |
| ----- | --------- | --- | --- | --- | --- | --- | --- |
Team-LRN

Objects 125
F I G U R E 7.7
Step 2 On the menu bar, select Project, Add Class three
times and paste in the code for the StockOption,
CallOption, and PutOption classes.
Step 3 Now we will need eight put and call objects and
eight corresponding prices. This will require 16
text boxes laid out in a pattern similar to that shown
in Figure 7.4 for the two expirations. Name the text
boxes with the following scheme: The name of
the textbox forthe nearbycall option withthestrike
below the underlying price should be txtCallNB
for Call, Nearby, Below. The text box for the second
nearbyputwiththestrikepriceabovetheunderlying
price should be txtPutSA for Put, Second, Above.
Figure7.8showstherespectivenamesforthetextbox
controls.
Step 4 AddthefollowingcodetotheButton1_Clickeventto
read in the price of the underlying IBM stock and
create eight put and call objects and set their
MarketPrices and StockPrices.
Dim UnderlyingPrice As Double = txtUnderlyingPrice.Text
Dim CallNB As New CallOption(txtCallNB.Text)
CallNB.MarketPrice = txtCallNBprice.Text
CallNB.StockPrice = UnderlyingPrice
Team-LRN

126 IntroductiontoVB.NET
F I G U R E 7.8
Dim PutNB As New PutOption(txtPutNB.Text)
PutNB.MarketPrice = txtPutNBprice.Text
PutNB.StockPrice = UnderlyingPrice
Dim CallNA As New CallOption(txtCallNA.Text)
CallNA.MarketPrice = txtCallNAprice.Text
CallNA.StockPrice = UnderlyingPrice
Dim PutNA As New PutOption(txtPutNA.Text)
PutNA.MarketPrice = txtPutNAprice.Text
PutNA.StockPrice = UnderlyingPrice
Team-LRN

Objects 127
Dim CallSB As New CallOption(txtCallSB.Text)
CallSB.MarketPrice = txtCallSBprice.Text
CallSB.StockPrice = UnderlyingPrice
Dim PutSB As New PutOption(txtPutSB.Text)
PutSB.MarketPrice = txtPutSBprice.Text
PutSB.StockPrice = UnderlyingPrice
Dim CallSA As New CallOption(txtCallSA.Text)
CallSA.MarketPrice = txtCallSAprice.Text
CallSA.StockPrice = UnderlyingPrice
Dim PutSA As New PutOption(txtPutSA.Text)
PutSA.MarketPrice = txtPutSAprice.Text
PutSA.StockPrice = UnderlyingPrice
Asmentionedearlier,theStockOptionclassalreadycalculates
the time till expiration using trading days as opposed to calendar
days, and so no conversion of the volatilities will be necessary.
Step 5 Once these eight option objects are created, we need
to average the call and put volatilities in each of the
quadrants, respectively, to reduce the number of
volatilities to four. For this we will need four new
variables of type double. Add the following code to
the Button1_Click event:
Dim dblVolNB, dblVolNA, dblVolSB, dblVolSA As Double
dblVolNB = (CallNB.ImpliedVol + PutNB.ImpliedVol) / 2
dblVolNA = (CallNA.ImpliedVol + PutNA.ImpliedVol) / 2
dblVolSB = (CallSB.ImpliedVol + PutSB.ImpliedVol) / 2
dblVolSA = (CallSA.ImpliedVol + PutSA.ImpliedVol) / 2
Step6 Now we will need to weight the above and below
volatilitiestoarriveatanaveragevolatilityforeachof
the two expirations, nearby and second nearby.
Dim dblNearbyVol, dblSecondVol As Double
dblNearbyVol = dblVolNB *((CallNA.Strike - UnderlyingPrice) / _
(CallNA.Strike - CallNB.Strike)) + dblVolNA * ((UnderlyingPrice- _
CallNB.Strike) / (CallNA.Strike - CallNB.Strike))
dblSecondVol = dblVolSB * ((CallSA.Strike - UnderlyingPrice) / _
(CallSA.Strike - CallSB.Strike)) + dblVolSA * ((UnderlyingPrice - _
CallSB.Strike) / (CallSA.Strike - CallSB.Strike))
Step 7 And, finally, we can calculate the ATM constant
maturity volatility:
Team-LRN

| 128 |     |     | IntroductiontoVB.NET |
| --- | --- | --- | -------------------- |
Dim ATMVol As Double = dblNearbyVol * ((CallSA.DaysTillExp - 22) / _
CallSA.DaysTillExp - CallNA.DaysTillExp)) + dblSecondVol * ((22 - _
CallNA.DaysTillExp) / (CallSA.DaysTillExp - CallNA.DaysTillExp))
| lblATMvol.Text | = Format(ATMVol, | "0.#####")  |       |
| -------------- | ---------------- | ----------- | ----- |
| Step           | 8                |             |       |
|                | Run the program  | (see Figure | 7.9). |
Theresultsyougetwillbedifferentfromtheresultsshownin
Figure 7.9 since the time-to-expiration calculations are continu-
ously changing. Thus on the CD we have included a spreadsheet
| called ATMs.xls, | against which | you can | check your answers. |
| ---------------- | ------------- | ------- | ------------------- |
| F I G U          | R E 7.9       |         |                     |
Team-LRN

Objects 129
Asyoucansee,creatingandmanagingmultipleobjectscanbe
quite a difficult task codewise. Suppose, for example, we had a
portfolio of 100 options. How much coding would we have to do
then? Obviously we will need a superior method for dealing with
this situation. In the following chapter we will discuss arrays,
which are a convenient way to hold multiple value types, that is,
variables. In later chapters we will look at data structures, which
provide convenient methods for dealing with groups of objects
such as portfolios of options.
SUMMARY
In this chapter we introduced the concepts of classes and objects.
Object-oriented programming necessitates that we understand the
ideas of abstraction, encapsulation, polymorphism, and inheri-
tance. Further we used the StockOption and CallOption classes to
illustrate these concepts as well as access modifiers and method
overloading. Lastly we built a complex model using eight put and
call objects to calculate the ATM volatility for IBM. This was a
complex program!
Team-LRN

| 130 |     |     | IntroductiontoVB.NET |
| --- | --- | --- | -------------------- |
PROBLEMS
| 1. In OOP, | what is meant       | by the term | abstraction?         |
| ---------- | ------------------- | ----------- | -------------------- |
| 2. What    | is encapsulation?   |             |                      |
| 3. What    | is polymorphism?    |             |                      |
| 4. What    | is inheritance?     |             |                      |
| 5. What    | are the differences | between     | the access modifiers |
| Public,    | Private, and        | Protected?  |                      |
Team-LRN

| Objects |            |     |               |     |          |     |         |     | 131     |
| ------- | ---------- | --- | ------------- | --- | -------- | --- | ------- | --- | ------- |
| PROJECT |            | 7.1 |               |     |          |     |         |     |         |
| To the  | CallOption |     | and PutOption |     | classes, | add | methods |     | for the |
Greeks. Build a Windows application that accepts user inputs for
anoptionssymbol,astockprice,andavolatility,andcalculatesthe
Black-Scholes price and Greeks for either a call or a put. Your
program should print out in labels all the necessary information
| including | the | price and | all | the Greeks. |     |     |     |     |     |
| --------- | --- | --------- | --- | ----------- | --- | --- | --- | --- | --- |
| PROJECT   |     | 7.2       |     |             |     |     |     |     |     |
Create a Stock class. Although this class will be comparatively
simple, you should add Private member variables for, at least, the
ticker, price, dividend, and dividend date, along with Public
properties for each of them. You should set the ticker in the
| constructor | function |     | New(). | Then | create | a   | VB.NET | Windows |     |
| ----------- | -------- | --- | ------ | ---- | ------ | --- | ------ | ------- | --- |
application that creates an object based upon the Stock class using
user-entered values. Override the ToString() method to print out
| the ticker | and     | the price | in a        | label. |            |        |     |           |     |
| ---------- | ------- | --------- | ----------- | ------ | ---------- | ------ | --- | --------- | --- |
| In         | VB.NET, | the       | overridable |        | ToString() | method | is  | inherited | by  |
every class by default. ToString() allows us to simply print out a
stringrepresentationofanobject.WithinyourStockclass,youcan
| implement | this      | method    | in       | the following |                        | way: |           |     |     |
| --------- | --------- | --------- | -------- | ------------- | ---------------------- | ---- | --------- | --- | --- |
| Public    | Overrides |           | Function |               | ToString()             |      | As String |     |     |
|           | Return    | strTicker |          | & "           | " & str(dblStockPrice) |      |           |     |     |
| End       | Function  |           |          |               |                        |      |           |     |     |
Team-LRN

This page intentionally left blank.
Team-LRN

| C   | H A | P T | E R | 8   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Arrays
I
nVB.NET,arraysareobjectsthatessentiallygroupidenticalvalue
| types             | together |          | contiguously | in           | memory |        | in one | or  | more |
| ----------------- | -------- | -------- | ------------ | ------------ | ------ | ------ | ------ | --- | ---- |
| dimensions—hence, |          |          | the          | Dim keyword. |        | We can | access | any | one  |
| element           | in       | an array | by           | referencing  | the    | array  | name   | and | the  |
element’s index, or position or address, within the array. When
doing financial modeling, we use arrays frequently, and so a good
| understanding |     | of  | them | and how they | work |     | is very | important. |     |
| ------------- | --- | --- | ---- | ------------ | ---- | --- | ------- | ---------- | --- |
Arrays come in particularly handy when dealing with data, doing
| matrix          | algebra, | and | creating | binomial | and     | trinomial |     | trees.    |     |
| --------------- | -------- | --- | -------- | -------- | ------- | --------- | --- | --------- | --- |
| ONE-DIMENSIONAL |          |     |          | ARRAYS   |         |           |     |           |     |
| Although        | arrays   |     | occupy   | space in | memory, | simply    |     | declaring | an  |
array does not create the space. Rather, because an array is a
reference type, an array declaration creates a variable that stores a
referencetothespaceinmemoryoccupiedbyanarray.Socreating
an array object is again a two-stage process. Here is a sample
| declaration |                  | for an | array of | doubles:     |     |           |     |        |       |
| ----------- | ---------------- | ------ | -------- | ------------ | --- | --------- | --- | ------ | ----- |
| Dim         | dblClosingPrices |        |          | As Double()  |     |           |     |        |       |
| Then        | the              | New    | keyword  | is necessary |     | to create | an  | actual | array |
object. The value in parentheses defines the upper bound for the
| array. The       | lower | bound | is  | always 0.     |     |     |     |     |     |
| ---------------- | ----- | ----- | --- | ------------- | --- | --- | --- | --- | --- |
| dblClosingPrices |       |       | =   | New Double(2) |     | {}  |     |     |     |
Asimplewaytopopulateanarrayistousetheinitializerlist,
like this:
| dblClosingPrices |     |     | =   | New Double(2) |     | {52.5, | 51.4, | 45.24} |     |
| ---------------- | --- | --- | --- | ------------- | --- | ------ | ----- | ------ | --- |
133
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

| 134            |                  |     |                |          |       | IntroductiontoVB.NET |     |     |
| -------------- | ---------------- | --- | -------------- | -------- | ----- | -------------------- | --- | --- |
| Alternatively, |                  | the | two statements |          | could | be combined:         |     |     |
| Dim            | dblClosingPrices |     | As             | Double() | =     | New Double(2)        |     | {}  |
| or using       | the initializer: |     |                |          |       |                      |     |     |
Dim dblClosingPrices As Double() = New Double(2) {52.5, 51.4, 45.24}
| Since | the | index | of the | first element | is  | always | 0,  | the upper |
| ----- | --- | ----- | ------ | ------------- | --- | ------ | --- | --------- |
bound, in this case 2, will always be 1 less than the number of
elementsinthearray,inthiscase3.Wecanaccessanyelementina
one-dimensional array by referencing its index, or address, within
the array.
| dblClosingPrices(0) |         |     | =      | 52.5     |         |         |     |           |
| ------------------- | ------- | --- | ------ | -------- | ------- | ------- | --- | --------- |
| dblClosingPrices(1) |         |     | =      | 51.4     |         |         |     |           |
| dblClosingPrices(2) |         |     | =      | 45.24    |         |         |     |           |
| If we               | attempt | to  | access | an array | element | outside |     | the upper |
bound, say dblClosingPrices(53), we will get an error message
saying that the index was outside the bounds of the array. Should
the situation arise, we could also declare an array of the user-
| defined data | type        | QuoteData. |                |     |       |               |     |     |
| ------------ | ----------- | ---------- | -------------- | --- | ----- | ------------- | --- | --- |
| Dim          | qdPriceData |            | As QuoteData() |     | = New | QuoteData(10) |     | {}  |
And we could reference the individual elements of a QuoteData
| array in the            | following |     | way: |         |     |     |     |     |
| ----------------------- | --------- | --- | ---- | ------- | --- | --- | --- | --- |
| qdPriceData(3).dblClose |           |     |      | = 43.45 |     |     |     |     |
| TWO-DIMENSIONAL         |           |     |      | ARRAYS  |     |     |     |     |
A two-dimensional array object could be instantiated in one line
this way:
| Dim | dblCovariance |     | As Double(,) |     | = New | Double(1,1) |     | {}  |
| --- | ------------- | --- | ------------ | --- | ----- | ----------- | --- | --- |
Wecoulddeclareandpopulateatwo-dimensionalarrayusing
| the two-line  | method        |       | and the      | initializer | in this | way:  |        |        |
| ------------- | ------------- | ----- | ------------ | ----------- | ------- | ----- | ------ | ------ |
| Dim           | dblCovariance |       | As Double(,) |             |         |       |        |        |
| dblCovariance |               | = New | Double(1,1)  |             | {{.057, | .83}, | {.192, | -.12}} |
Team-LRN

| Arrays      |                                    |               |             |              |                      |         |       | 135 |
| ----------- | ---------------------------------- | ------------- | ----------- | ------------ | -------------------- | ------- | ----- | --- |
| We          | can                                | access        | any element |              | in a two-dimensional |         | array | by  |
| referencing | its                                | index,        | or address, |              | in the array.        |         |       |     |
| Sub         | Main()                             |               |             |              |                      |         |       |     |
|             | Dim                                | dblCovariance |             | As Double(,) |                      |         |       |     |
|             | dblCovariance                      |               | = New       | Double(1,    | 1) {{0.057,          | 0.83},  | _     |     |
|             |                                    |               |             |              | {0.192,              | -0.12}} |       |     |
|             | Console.WriteLine(dblCovariance(0, |               |             |              | 0))                  |         |       |     |
|             | Console.WriteLine(dblCovariance(1, |               |             |              | 0))                  |         |       |     |
|             | Console.WriteLine(dblCovariance(0, |               |             |              | 1))                  |         |       |     |
|             | Console.WriteLine(dblCovariance(1, |               |             |              | 1))                  |         |       |     |
| End         | Sub                                |               |             |              |                      |         |       |     |
ThisprogramprintsouttheelementsofthedblCovariancearrayas:
.057 .192
.083 -0.12
| As  | discussed | in  | Chapter | 5,  | we can access | each | element | in a |
| --- | --------- | --- | ------- | --- | ------------- | ---- | ------- | ---- |
two-dimensionalarrayinVB.NETbywritinganestedFor...Next
| loop structure, |      | such   | as:       |     |                          |     |       |     |
| --------------- | ---- | ------ | --------- | --- | ------------------------ | --- | ----- | --- |
| For             | Rows | = 0 To | 1         |     |                          |     |       |     |
|                 | For  | Cols   | = 0 To    | 1   |                          |     |       |     |
|                 |      | ’ Do   | something |     | with dblCovariance(Rows, |     | Cols) |     |
Next Cols
| Next   | Rows |        |     |     |     |     |     |     |
| ------ | ---- | ------ | --- | --- | --- | --- | --- | --- |
| JAGGED |      | ARRAYS |     |     |     |     |     |     |
On occasion, the structure of the data in a program may be two-
dimensional,butnotrectangular.Thatis,noteveryrowwillbethe
samelength.Insuchcasesitmaybeadvantageousfromamemory
savingsstandpointtouseajaggedarray.Ajaggedarrayisanarray
that has rows of different lengths. In memory a jagged array is
really stored as an array of arrays. Here is how to declare a jagged
| array in | one          | line: |     |            |                   |     |     |     |
| -------- | ------------ | ----- | --- | ---------- | ----------------- | --- | --- | --- |
| Dim      | dblBinomTree |       | As  | Double()() | = New Double(2)() |     | {}  |     |
Binomial trees are valuable tools in derivatives pricing, and
thereareseveralmethodsforbuildingbinomialtreesincodeusing
Team-LRN

| 136 |     |     |     |     |     | IntroductiontoVB.NET |     |
| --- | --- | --- | --- | --- | --- | -------------------- | --- |
arrays. Some methods only require a single-dimensional array.
However, in cases where the entire tree must be maintained in
memory, jagged arrays work quite well. In fact, binomial trees fit
rather elegantly into jagged arrays and waste no memory space.
| Figure | 8.1 shows | different | potential | price      | paths | of a       | stock.    |
| ------ | --------- | --------- | --------- | ---------- | ----- | ---------- | --------- |
| The    | initial   | value     | in the    | tree, 100, | is    | calculated | using the |
formula
(cid:1)D0(cid:1)U0
|     |     |     | 100 ¼ | S   |     |     |     |
| --- | --- | --- | ----- | --- | --- | --- | --- |
0
The two prices after one step forward, 107.43 and 93.09, are found
using
|     |     |     | 107:48 ¼ | S (cid:1)D0(cid:1)U1 |     |     |     |
| --- | --- | --- | -------- | -------------------- | --- | --- | --- |
0
|     |     |     | 93:04 ¼ | S (cid:1)D1(cid:1)U0 |     |     |     |
| --- | --- | --- | ------- | -------------------- | --- | --- | --- |
0
| As           | you can | see, we       | calculate | individual |     | nodes  | on the tree by |
| ------------ | ------- | ------------- | --------- | ---------- | --- | ------ | -------------- |
|              |         |               |           | U          | D.  |        |                |
| incrementing |         | the exponents | of        | and        |     | We can | make these     |
calculations and populate a jagged array very easily since the
exponents map to the indexes of the array elements. Figure 8.2
| shows | the array | elements | with | their values | and | indexes. |     |
| ----- | --------- | -------- | ---- | ------------ | --- | -------- | --- |
| F I G | U R       | E 8.1    |      |              |     |          |     |
Team-LRN

| Arrays |       |         |     |     |     |     | 137 |
| ------ | ----- | ------- | --- | --- | --- | --- | --- |
| F      | I G U | R E 8.2 |     |     |     |     |     |
We can initialize the elements of a binomial tree into a jagged
| array | as per     | Figure                | 8.2 in this   | fashion:     |               |             |             |
| ----- | ---------- | --------------------- | ------------- | ------------ | ------------- | ----------- | ----------- |
|       | Sub Main() |                       |               |              |               |             |             |
|       | Dim        | x, y As               | Integer       |              |               |             |             |
|       | Dim        | dblStockPrice         | As            | Double       | = 100         |             |             |
|       | Dim        | U As Double           | = 1.074837    |              |               |             |             |
|       | Dim        | D As Double           | = 0.930374    |              |               |             |             |
|       | Dim        | dblBinomTree          | As Double()() |              | = New         | Double(3)() | {}          |
|       | For        | x = 0 To              | 3             |              |               |             |             |
|       |            | dblBinomTree(x)       | =             | New Double(3 | -             | x) {}       |             |
|       |            | For y =               | 0 To 3 - x    |              |               |             |             |
|       |            | dblBinomTree(x)(y)    |               | =            | dblStockPrice | * D         | ^ x * U ^ y |
|       |            | Console.WriteLine("(" |               |              | & x & ",      | " & y &     | " ) = " & _ |
dblBinomTree(x)(y))
Next y
|     | Next    | x   |     |     |     |     |     |
| --- | ------- | --- | --- | --- | --- | --- | --- |
|     | End Sub |     |     |     |     |     |     |
Jaggedarraysareheldinmemoryandrequirethatwedeclare
theupperboundofthefirstdimensionfirst.Thatis,wefirstdeclare
the number of rows, and then we can go through row by row and
declare the upper bound of each particular row as in the line of
code above.
|       | dblBinomTree(x) |         | = New | Double(3 | - x) | {}  |     |
| ----- | --------------- | ------- | ----- | -------- | ---- | --- | --- |
| ARRAY |                 | METHODS |       |          |      |     |     |
Because arrays in VB.NET are instances of the Array class, and
| thereforeare |     | objects,theyhaveproperties |     |     |     | andmethodsassociated |     |
| ------------ | --- | -------------------------- | --- | --- | --- | -------------------- | --- |
Team-LRN

| 138 |     |     |     |     | IntroductiontoVB.NET |
| --- | --- | --- | --- | --- | -------------------- |
withthem.Herearesomeofthepropertiesandmethodsaswellas
several functions found in the System.Array namespace. To use
| these     | functions | we should     | include | an Imports | System.Array |
| --------- | --------- | ------------- | ------- | ---------- | ------------ |
| statement | above     | all the other | code in | a module.  |              |
Array
| Properties |     | Description             |     |                     | Example |
| ---------- | --- | ----------------------- | --- | ------------------- | ------- |
| Length     |     | Returnsthetotalnumberof |     | intA¼myArray.Length |         |
elementsinthearray
| Rank |     | Returnsthenumberof |     | intA¼myArray.Rank |     |
| ---- | --- | ------------------ | --- | ----------------- | --- |
dimensionsinthearray
| ArrayMethods |     | Description |     |     | Example |
| ------------ | --- | ----------- | --- | --- | ------- |
GetLength Returnsthenumberofelements intA¼myArray.GetLength(0)
inagivendimension
| GetUpperBound |     | Returnstheupperboundofa |     | intA¼myArray.    |     |
| ------------- | --- | ----------------------- | --- | ---------------- | --- |
|               |     | givendimension          |     | GetUpperBound(0) |     |
System.Array
| Functions |     | Description                |     |                        | Example |
| --------- | --- | -------------------------- | --- | ---------------------- | ------- |
| Clear     |     | Setsarangeofelementswithin |     | Clear(SourceArray,0,3) |         |
thearrayequalto0
| Copy    |     | Makesacopyofallorpartofan |     | Copy(SourceArray,TargetArray, |     |
| ------- | --- | ------------------------- | --- | ----------------------------- | --- |
|         |     | arraygivenalength         |     | 5)                            |     |
| IndexOf |     | Findstheindexnumber       |     | intA¼                         |     |
|         |     | associatedwiththefirst    |     | IndexOf(SourceArray,“IBM”)    |     |
occurrenceofavalue
| Reverse |     | Reversessomeorallofthe |     | Reverse(SourceArray,1,10) |     |
| ------- | --- | ---------------------- | --- | ------------------------- | --- |
elementsinanarraygivena
startingandendingindex
| Sort |     | Sortssomeorallofaone- |     | Sort(SourceArray) |     |
| ---- | --- | --------------------- | --- | ----------------- | --- |
dimensionalarrayin
ascendingorder
Here is a short console application illustrating some of these
methods:
| Imports | System.Array |     |     |     |     |
| ------- | ------------ | --- | --- | --- | --- |
| Module  | Module1      |     |     |     |     |
Sub Main()
|     | Dim | x As Integer |     |     |     |
| --- | --- | ------------ | --- | --- | --- |
Dim dblReturns As Double() = New Double(4) {0.0176, 0.0083, _
|     |     |     |     | 0.0232, | -0.0241, 0.0077} |
| --- | --- | --- | --- | ------- | ---------------- |
Sort(dblReturns)
|     | For | x = 0 To dblReturns.GetUpperBound(0) |     |     |     |
| --- | --- | ------------------------------------ | --- | --- | --- |
Console.WriteLine(dblReturns(x))
Next x
End Sub
| End | Module |     |     |     |     |
| --- | ------ | --- | --- | --- | --- |
Team-LRN

Arrays 139
This program declares and populates a one-dimensional array
named dblReturns. The Sort() function puts the elements in the
order from lowest to highest. The GetUpperBound() member
function returns the upper bound, 4, so that the For...Next loop
will run five times. Also notice the inclusion of the Imports
statement at the top. The function definition for Sort() is found in
the System.Array namespace. We will discuss namespaces in
greater detail in Chapter 10. This program prints out:
-.0241
.0077 .0083
.0176 .0232
DYNAMIC ARRAY SIZING
In situations where the number of elements in an array either is
unknownorwillnotbefixed,weusetheDimstatementalongwith
the ReDim() procedure.
Dim dblCovariance As Double(,)
Before we can use this array, we must dimension bounds
using the ReDim statement. For example:
ReDim dblCovariance(4, 4)
All arrays in VB.NETare dynamic, and the ReDim() function
canbecalledasmanytimesasisnecessary.Beaware,though,that
VB.NETdoesnotallowyoutochangethenumberofdimensionsin
an array.
Also be careful because each time you ReDim an array, the
contents of the array are destroyed unless you use the Preserve
keyword. Preserve will keep the existing data intact and grow the
size of the array.
ReDim Preserve dblCovariance(5, 5)
As another example, say we want to read some historical
price data from a file, but we do not know how many items of
Team-LRN

| 140 |     |     |     |     |     | IntroductiontoVB.NET |     |     |
| --- | --- | --- | --- | --- | --- | -------------------- | --- | --- |
information are in the file. We could read through the file, count
| howmanyitemsthere |     |       | are,          | and thenuse |        | a singleReDim | statement |      |
| ----------------- | --- | ----- | ------------- | ----------- | ------ | ------------- | --------- | ---- |
| to allocate       | an  | array | of sufficient | size.       |        |               |           |      |
| What              | if  | the   | information   | was         | coming | from          | a live    | data |
connection? In that situation we would not have the opportunity
to determinethe numberof items aheadof time.The solution isto
| use the | Preserve | keyword |     | in conjunction |     | with ReDim, | as  | shown |
| ------- | -------- | ------- | --- | -------------- | --- | ----------- | --- | ----- |
below:
|     |     | Dim dblPriceData   |                | As Double()                  |         |     |     |     |
| --- | --- | ------------------ | -------------- | ---------------------------- | ------- | --- | --- | --- |
|     |     | Dim intNumElements |                | As                           | Integer |     |     |     |
|     |     | Dim blnMoreData    |                | As Boolean                   |         |     |     |     |
|     |     | Do While           | blnMoreData    |                              |         |     |     |     |
|     |     |                    | intNumElements | +=                           | 1       |     |     |     |
|     |     |                    | ReDim Preserve | dblPriceData(intNumElements) |         |     |     |     |
‘ Read data feed and set blnMoreData to True if more data was read.
End While
| PASSING |     | ARRAYS |     | TO FUNCTIONS |     |     |     |     |
| ------- | --- | ------ | --- | ------------ | --- | --- | --- | --- |
Visual Basic.NET allows us to pass arrays to functions as input
| arguments  | and         | also   | return    | them     | from       | functions  | as     | output |
| ---------- | ----------- | ------ | --------- | -------- | ---------- | ---------- | ------ | ------ |
| arguments, | or          | return | values.   | Here     | is         | an example | of the | basic  |
| syntax     | for passing |        | arrays to | and from | functions: |            |        |        |
| Sub        | Main()      |        |           |          |            |            |        |        |
Dim dblReturns As Double() = New Double(9) {0.0203, -0.0136, 0.0012, _
|     |     |     |     |     |     | 0.0266, -0.0063, | -0.0601, | _   |
| --- | --- | --- | --- | --- | --- | ---------------- | -------- | --- |
|     |     |     |     |     |     | 0.0307, 0.0123,  | 0.0055,  | _   |
0.0441}
Console.WriteLine(Average(dblReturns))
| End | Sub |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Here,wehavecreatedanarrayofdoublesandpopulatedthearray,
usingtheinitializer,with10valuesrepresentingdailyreturns.Then
wehavepassedthearraytoafunctioncalledAverage()thataccepts
an array of doubles as an input argument and returns a double,
| which  | is the average |                | of the        | elements        | in      | the array:   |     |        |
| ------ | -------------- | -------------- | ------------- | --------------- | ------- | ------------ | --- | ------ |
| Public | Function       |                | Average(ByRef |                 | InArray | As Double()) | As  | Double |
|        | Dim            | dblTotalReturn |               | As Double       |         |              |     |        |
|        | Dim            | x As           | Integer       |                 |         |              |     |        |
|        | Dim            | dblLength#     | =             | UBound(InArray, |         | 1)           |     |        |
|        | For            | x = 0          | To dblLength  |                 |         |              |     |        |
Team-LRN

Arrays 141
|     | dblTotalReturn |     | += InArray(x) |     |
| --- | -------------- | --- | ------------- | --- |
Next x
|     | Return dblTotalReturn |     | / (dblLength | + 1) |
| --- | --------------------- | --- | ------------ | ---- |
| End | Function              |     |              |      |
Becausearraysarealwayspassedtofunctionsbyreference,it
is important to remember that certain operations performed on
those arrays, such as matrix transposition and inversion, will
actually destroy the original matrix. To avoid this situation, it may
be necessary to first make a copy of the array within the function
definition and then proceed by making calculations on the new
| copy of | the original    | array. |     |     |
| ------- | --------------- | ------ | --- | --- |
| THE     | ERASE STATEMENT |        |     |     |
TheErasestatementclearsanarrayandreleasesthememoryused
by the array object. To reuse the array after Erase, we can use the
ReDim statement.
| Erase  | dblReturns |     |     |     |
| ------ | ---------- | --- | --- | --- |
| UBOUND | FUNCTION   |     |     |     |
TheUbound()functionreturnstheupperboundofadimensionof
the array. It works the same as the array class member function
GetUpperBound()exceptthatthearraydimensionsare1and2for
| a two-dimensional | array.        | For                      | example: |              |
| ----------------- | ------------- | ------------------------ | -------- | ------------ |
| Dim               | dblPriceData  | As Double(,)             | = New    | Double(10,5) |
| Dim               | intUpperBound | As Integer               |          |              |
| intUpperBound     |               | = UBound(dblPriceData,1) |          |              |
| intUpperBound     | will          | equal 10.                |          |              |
| USING             | ARRAYS        | FOR                      | DATA     |              |
Whenmodelingreturns,weoftendetermineaverageratesofreturn
and volatilities. In this case, we need to use continuous rates of
Team-LRN

| 142          |      |     |     |         |         | IntroductiontoVB.NET |     |     |
| ------------ | ---- | --- | --- | ------- | ------- | -------------------- | --- | --- |
| return, such | that |     |     |         |         |                      |     |     |
|              |      |     |     | (cid:1) | (cid:2) |                      |     |     |
S
|     |     |     | R   | ¼ ln | i   |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- |
i
S
i(cid:2)1
Given historical returns, we can calculate the average return:
1X n
|     |     |     | m     | ¼   | R i |     |     |     |
| --- | --- | --- | ----- | --- | --- | --- | --- | --- |
|     |     |     | R;t,T |     | n   |     |     |     |
i¼1
| We can calculate |     | the variance |     | of returns: |     |     |     |     |
| ---------------- | --- | ------------ | --- | ----------- | --- | --- | --- | --- |
1X n
|     |     |     | 2     |     | (cid:2)RR(cid:1) )2 |     |     |     |
| --- | --- | --- | ----- | --- | ------------------- | --- | --- | --- |
|     |     |     | s t,T | ¼   | (R i                |     |     |     |
n
i¼1
| We can calculate |     | the skew: |                        |     |           |                          |     |     |
| ---------------- | --- | --------- | ---------------------- | --- | --------- | ------------------------ | --- | --- |
|                  |     |           |                        |     | n (cid:1) | (cid:2)RR(cid:1)(cid:2)3 |     |     |
|                  |     |           |                        | n   | X R i     |                          |     |     |
|                  |     | Skew ¼    |                        |     |           |                          |     |     |
|                  |     |           | (n(cid:2)1)(n(cid:2)2) |     |           | s                        |     |     |
i¼1
| The skewness |        | of a | distribution |          | characterizes |     | the degree | of  |
| ------------ | ------ | ---- | ------------ | -------- | ------------- | --- | ---------- | --- |
| asymmetry    | around |      | its mean.    | Positive | skewness      |     | indicates  | an  |
asymmetric tail extending toward more positive values. Negative
skewness indicates an asymmetric tail extending toward negative
values.
| We  | can calculate |        | the kurtosis: |     |                                  |     |               |     |
| --- | ------------- | ------ | ------------- | --- | -------------------------------- | --- | ------------- | --- |
|     | (             |        |               |     | (cid:1) (cid:2)RR(cid:1)(cid:2)4 | )   |               |     |
|     |               | n(nþ1) |               |     | X n R                            |     | 3(n(cid:2)1)2 |     |
i
| Kurtosis¼ |                                   |     |     |     |     |     | (cid:2)                |     |
| --------- | --------------------------------- | --- | --- | --- | --- | --- | ---------------------- | --- |
|           | (n(cid:2)1)(n(cid:2)2)(n(cid:2)3) |     |     |     | s   |     | (n(cid:2)2)(n(cid:2)3) |     |
i¼1
This returns the kurtosis of a data set. Kurtosis characterizes the
relativepeakednessorflatnessofadistributioncomparedwiththe
normaldistribution.Positivekurtosisindicatesarelativelypeaked
distribution. Negative kurtosis indicates a relatively flat distri-
bution.
| Step | 1 In | VB.NET, | open | a new | Windows | application |     | called |
| ---- | ---- | ------- | ---- | ----- | ------- | ----------- | --- | ------ |
DataArray.
| Step | 2 Add | five | labels | to the | form. |     |     |     |
| ---- | ----- | ---- | ------ | ------ | ----- | --- | --- | --- |
Team-LRN

| Arrays |       |            |         |         |         |       |               | 143 |
| ------ | ----- | ---------- | ------- | ------- | ------- | ----- | ------------- | --- |
| Step   | 3 Add | five       | modules | and in  | them,   | place | the functions |     |
|        | for   | Average(), | Var(),  | VarP(), | Skew(), | and   | Kurtosis()    |     |
|        | from  | the        | CD.     |         |         |       |               |     |
Step 4
Intheformloadevent,addthefollowingcodetopass
|     | an  | array | of return | data into | each | of the | functions: |     |
| --- | --- | ----- | --------- | --------- | ---- | ------ | ---------- | --- |
Private Sub Form1_Load(ByVal sender As ...) Handles MyBase.Load
Dim dblReturns As Double() = New Double(9) {0.0203, -0.0136, 0.0012, _
|     |     |     |     |     | 0.0266, | -0.0063, | -0.0601, | _   |
| --- | --- | --- | --- | --- | ------- | -------- | -------- | --- |
|     |     |     |     |     | 0.0307, | 0.0123,  | 0.0055,  | _   |
0.0441g
|     | Label1.Text |     | = Format(Average(dblReturns),  |     |            | "#.#####") |     |     |
| --- | ----------- | --- | ------------------------------ | --- | ---------- | ---------- | --- | --- |
|     | Label2.Text |     | = Format(Var(dblReturns),      |     | "#.#####") |            |     |     |
|     | Label3.Text |     | = Format(VarP(dblReturns),     |     |            | "#.#####") |     |     |
|     | Label4.Text |     | = Format(Skew(dblReturns),     |     |            | "#.#####") |     |     |
|     | Label5.Text |     | = Format(Kurtosis(dblReturns), |     |            | "#.#####") |     |     |
End Sub
| Step | 5 Run | the | program | (see | Figure | 8.3). | As with | any |
| ---- | ----- | --- | ------- | ---- | ------ | ----- | ------- | --- |
calculationsyoumakeincode,besuretoverifythem
|       | against |     | Excel’s | built-in functions—Average(), |     |     |     | Var(), |
| ----- | ------- | --- | ------- | ----------------------------- | --- | --- | --- | ------ |
|       | VarP(), |     | Skew(), | and Kurt().                   |     |     |     |        |
| F I G | U R E   | 8.3 |         |                               |     |     |     |        |
Team-LRN

| 144   |        |     |     |     |        |         | IntroductiontoVB.NET |     |
| ----- | ------ | --- | --- | --- | ------ | ------- | -------------------- | --- |
| USING | ARRAYS |     |     | FOR | MATRIX | ALGEBRA |                      |     |
We often use matrix algebra when doing financial research. For
| example, | modern |     | portfolio |     | management | techniques |     | frequently |
| -------- | ------ | --- | --------- | --- | ---------- | ---------- | --- | ---------- |
make use of covariance matrices. Using matrix notation, we can
calculate the variance of a portfolio in the following manner:
|     |     |     |     | s   | 2 ¼v0Vv |     |     |     |
| --- | --- | --- | --- | --- | ------- | --- | --- | --- |
P
where V is the covariance matrix and vis the vector of portfolio
weights. A covariance matrix, of course, exists in two dimensions,
where:
1X
|     | V ¼ | Cov(r | , r | ) ¼ | [r (cid:2)E(r | )][r | (cid:2)E(r | )]  |
| --- | --- | ----- | --- | --- | ------------- | ---- | ---------- | --- |
|     |     |       | A B | n   | A,i           | A    | B,i        | B   |
Sothat,forexample,acovariancematrixforathree-assetportfolio
is
|     |     |     | 2   |        |               |              | 3   |     |
| --- | --- | --- | --- | ------ | ------------- | ------------ | --- | --- |
|     |     |     |     | 0:0025 | (cid:2)0:0011 | (cid:2)0:001 |     |     |
¼ 4(cid:2)0:0011
|     |     | V   |              |     | 0:0058 | 0:00035 |     |     |
| --- | --- | --- | ------------ | --- | ------ | ------- | --- | --- |
|     |     |     | (cid:2)0:001 |     | 0:0003 | 0:0048  |     |     |
and
|     |     |     |     |     | 2 3 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
0:3
|     |     |     |     | v¼  | 40:55 |     |     |     |
| --- | --- | --- | --- | --- | ----- | --- | --- | --- |
0:2
s 2,
| To  | calculate |     | the portfolio |     | variance, | P   | we need | to employ |
| --- | --------- | --- | ------------- | --- | --------- | --- | ------- | --------- |
somespecializedmatrixmathfunctionsthathandlethealgorithms
usingtwo-dimensionalarrays.FortunatelytheCDcontainsseveral
| math | functions | that       | manipulate |      | two-dimensional |     | arrays.     |        |
| ---- | --------- | ---------- | ---------- | ---- | --------------- | --- | ----------- | ------ |
| Step | 1         | In VB.NET, |            | open | a new Windows   |     | application | called |
MatrixArray.
| Step | 2   | Add         | at least      | one     | label to    | the form. |            |              |
| ---- | --- | ----------- | ------------- | ------- | ----------- | --------- | ---------- | ------------ |
| Step | 3   | Add         | two           | modules | and         | paste     | in the     | code for the |
|      |     | MMult2by1() |               | and     | MMult1by1() |           | functions. |              |
| Step | 4   | Add         | the following |         | code to     | the       | Form1_Load | event:       |
Private Sub Form1_Load(ByVal sender As ...) Handles MyBase.Load
|     | Dim | dblCovar | As  | Double(,) | = New Double(2, |          | 2) { _   |     |
| --- | --- | -------- | --- | --------- | --------------- | -------- | -------- | --- |
|     |     |          |     |           | {0.0025,        | -0.0011, | -0.001}, | _   |
|     |     |          |     |           | {20.0011,       | 0.0058,  | 0.0003}, | _   |
Team-LRN

Arrays 145
|     |     |            |     |              | {20.001, | 0.0003,         | 0.0048}} |      |
| --- | --- | ---------- | --- | ------------ | -------- | --------------- | -------- | ---- |
|     | Dim | dblWeights | As  | Double()5New |          | Double(2) f0.3, | 0.5,     | 0.2g |
|     | Dim | dblPortVar | As  | Double       |          |                 |          |      |
dblPortVar = MMult1by1(MMult2by1(dblCovar, dblWeights), dblWeights)
|       | Label1.Text |          | = Val(dblPortVar) |              |       |              |          |          |
| ----- | ----------- | -------- | ----------------- | ------------ | ----- | ------------ | -------- | -------- |
|       | End Sub     |          |                   |              |       |              |          |          |
|       | Step        | 5 Run    | yourprogram       |              | (see  | Figure 8.4). | Again,be | sure to  |
|       |             | verify   | your              | calculations |       | against      | Excel’s  | built-in |
|       |             | function | MMult().          |              |       |              |          |          |
| F     | I G U       | R E 8.4  |                   |              |       |              |          |          |
| USING |             | ARRAYS   |                   | FOR          | TREES |              |          |          |
Here we will show a simple example using a jagged array to price
an American call option using a binomial tree. The call option has
thefollowingattributes:stockprice,S,is100,strikeprice,X,is100,
I,
time till expiration is 3 months, interest rate, is 0.1, and the
annualized volatility, sigma, is 0.25. The binomial tree will consist
ofthreesteps,asintheexampleusingajaggedarraypreviouslyin
thechapter.Eachstepinthetreethenwillbe3calendarmonthsor
21 trading days, 0.25 of a year, divided by 3, so that the change in
t¼0.25/3¼0.083333.
| time | for each | step | is  |     |     | This | option | will expire |
| ---- | -------- | ---- | --- | --- | --- | ---- | ------ | ----------- |
inatotalofthreesteps,oneforeachofthe3months.SoN¼3.We
| calculate | U   | and D | thusly: |           |                              |            |     |     |
| --------- | --- | ----- | ------- | --------- | ---------------------------- | ---------- | --- | --- |
|           |     |       | pffiffi |           | pffiffiffiffiffiffiffiffiffi |            |     |     |
|           |     | U     | ¼ es    | t ¼ e0:25 | 08333                        | ¼ 1:074837 |     |     |
pffiffiffiffiffiffiffiffiffi
pffiffi
|     |     | D   | ¼ e(cid:2)s | t ¼ e(cid:2)0:25 | 08333 | ¼ 0:930374 |     |     |
| --- | --- | --- | ----------- | ---------------- | ----- | ---------- | --- | --- |
Team-LRN

146 IntroductiontoVB.NET
We will add a variable A to shorten the calculations:
A ¼ e(cid:2)I(cid:1)t ¼ e(cid:2)0:1(cid:1)0:083333 ¼ 0:991701
Also, the probability of an up move is found, such that
(eI(cid:1)t (cid:2)D) e0:1(cid:1)0:083333(cid:2)0:930374
P ¼ ¼ ¼ 0:5399892
U (cid:2)D 1:074837(cid:2)0:930374
Once we have declared and defined the necessary variables,
we can calculate the terminal payoffs for the option for each
outcome by calculating the intrinsic value in this way:
Tree ¼ max(S (cid:1)Dx(cid:1)UN(cid:2)x(cid:2)X, 0)
x,N(cid:2)x 0
American-style options require that a decision be made at
each node about whether to exercise the option. So we must
compare the intrinsic value of the option with the risk-neutral
valuation at each node:
Tree ¼ max[S (cid:1)Dx(cid:1)Uy(cid:2)x(cid:2)X, A(cid:1)(P (cid:1)Tree þ(1(cid:2)P)
x,y(cid:2)x 0 x,y(cid:2)xþ1
(cid:1)Tree ]
xþ1,y(cid:2)x
where y¼N21.
The value of the call option will then be Tree(0)(0).
Step 1 In VB.NETopen a new console application.
Step 2 Add the following code:
Imports System.Math
Module Module1
Sub Main()
Dim x, y As Integer
Dim N As Integer = 3
Dim dblStockPrice As Double = 100
Dim dblStrike As Double = 100
Dim dblTimeStep As Double = .25 / N
Dim dblIntRate = 0.1
Dim dblSigma = 0.25
Dim U As Double = Exp(dblSigma * dblTimeStep ^ 0.5)
Dim D As Double = Exp(-dblSigma * dblTimeStep ^ 0.5)
Dim A As Double = Exp(-dblIntRate * dblTimeStep)
Dim P As Double = (Exp(dblIntRate * dblTimeStep) - D) / (U - D)
Team-LRN

Arrays 147
Dim dblBinomTree As Double()() = New Double(N)() {}
For x = 0 To N
dblBinomTree(x) = New Double(N - x) {}
dblBinomTree(x)(N - x) = Max((dblStockPrice * D ^ x * _
U ^ (N - x)) - dblStrike, 0)
Next x
For y = N - 1 To 0 Step -1
For x = 0 To y
dblBinomTree(x)(y - x) = Max((dblStockPrice * D ^ (x) * _
U ^ (y - x)) - dblStrike, A * (P * _
dblBinomTree(x)(y - x + 1) + (1 - P) * _
dblBinomTree(x + 1)(y - x)))
Next x
Next y
Console.WriteLine("The price of the call option is: " & _
dblBinomTree(0)(0))
End Sub
End Module
Step 3 Run the program by selecting Start Without
Debugging from the Debug menu item.
Thevalueofthecalloptionusingthismethodis6.6468,which
rounds to 6.65. Figure 8.5 shows a map of the values of
dblBinomTree()(). We can increase the accuracy of our pricing
model by increasing the number of steps, N. For example, if we
change N to 20, so that t ¼ 0.25/20¼0.0125, the value of the call
option is 6.19.
F I G U R E 8.5
Team-LRN

148 IntroductiontoVB.NET
SUMMARY
In this chapter, we have looked at how to create and manipulate
arraysof variables. We use arrays often in finance to hold data, do
matrix math, and build trees for pricing derivatives. Important
thingstotakenoteofarehowtoemploydynamicarraysizingand
how to pass and return arrays to and from functions.
Team-LRN

Arrays 149
PROBLEMS
| 1. What | is a jagged  | array?      |                    |
| ------- | ------------ | ----------- | ------------------ |
| 2. How  | do we pass   | an array to | a function?        |
| 3. Why  | is declaring | an array a  | two-stage process? |
4. Becausearraysarereferencetypes,whatisthedangerwith
| passing | arrays to | functions? |     |
| ------- | --------- | ---------- | --- |
5. Whatisdynamicarraysizing,andhowisitaccomplished?
Team-LRN

| 150     |           |             |              | IntroductiontoVB.NET |     |
| ------- | --------- | ----------- | ------------ | -------------------- | --- |
| PROJECT | 8.1       |             |              |                      |     |
| Create  | a Windows | application | that creates | a two-dimensional    |     |
covariance matrix given three one-dimensional arrays of returns
| for three | stocks. | The covariance | matrix | should look like | the |
| --------- | ------- | -------------- | ------ | ---------------- | --- |
following:
|     |     | 2     | 3           |     |     |
| --- | --- | ----- | ----------- | --- | --- |
|     |     | s a,a | s a,b s a,c |     |     |
|     |     | 4s    | s s         |     |     |
|     |     | b,a   | b,b b,c5    |     |     |
|     |     | s     | s s         |     |     |
|     |     | c,a   | c,b c,c     |     |     |
Hard-code the three arrays of returns and use the Covariance()
functionontheCDtomakethecalculations.Printoutthematrixin
| labels on | the form. |     |     |     |     |
| --------- | --------- | --- | --- | --- | --- |
| PROJECT   | 8.2       |     |     |     |     |
Create a Windows application that sorts an array of 20 returns.
Then print out the fifth lowest return in a text box. Hard-code the
| returns | in a one-dimensional |     | array. |     |     |
| ------- | -------------------- | --- | ------ | --- | --- |
Team-LRN

9
| C       | H A | P T E | R       |     |     |     |     |     |     |
| ------- | --- | ----- | ------- | --- | --- | --- | --- | --- | --- |
| Problem |     |       | Solving |     |     |     |     |     |     |
U
| p to | this point | wehave | ignoredprogram |     |     | errors | and | debugging, |     |
| ---- | ---------- | ------ | -------------- | --- | --- | ------ | --- | ---------- | --- |
and we will do so again after this chapter. The reason for this is
simple: Intermingling program logic with error-handling logic
makes computer code very difficult to read and understand. This
book is primarily concerned with teaching the logic of modeling
derivative instruments and building automated trading systems.
| However,       | problem |            | solving    | is an        | extremely |     | important | topic   | to     |
| -------------- | ------- | ---------- | ---------- | ------------ | --------- | --- | --------- | ------- | ------ |
| consider       | when    | creating   | production |              | software, |     | and       | so we   | will   |
| address        | it on   | its own    | in this    | chapter.     |           |     |           |         |        |
| Unfortunately, |         | exceptions |            | or problems, |           | in  | the       | form of | syntax |
errors and logic errors, inevitably creep into our programs. Very
rarely, if ever, do our programs run correctly the first time. More
often, several mistakes are present in the syntax or logic of our
| programs | that | we  | must correct |     | before | the | program | will | run |
| -------- | ---- | --- | ------------ | --- | ------ | --- | ------- | ---- | --- |
smoothly. If you haven’t already noticed, the longer and more
complexourprogramsbecome,thelongerittakestodebugthem—
in fact, exponentially longer. For these reasons, programming is
really a series of problems to be solved. We call the process of
findingandfixingerrorsinourapplicationsdebugging,andlearning
todebugquicklyisoneofthemostimportantskillsyoucangainas
a financial engineer. Fear not, however—the more experience and
| knowledge | you | gain, | the | faster | you | will | become | at  | solving |
| --------- | --- | ----- | --- | ------ | --- | ---- | ------ | --- | ------- |
problems.
| In  | this chapter |     | we will | look | at syntax, |     | logic, | and run-time |     |
| --- | ------------ | --- | ------- | ---- | ---------- | --- | ------ | ------------ | --- |
errors in a program, and we will explore some helpful techniques
for finding and correcting them. Furthermore, we will show you
151
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

| 152 |     |     |     |     |     |     | IntroductiontoVB.NET |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------- | --- |
how to write blocks of code called exception handlers that will
properly react to error conditions that occur while a program is
| running | and will | prevent | the | program | from | crashing. |     |     |
| ------- | -------- | ------- | --- | ------- | ---- | --------- | --- | --- |
| SYNTAX  | ERRORS   |         |     |         |      |           |     |     |
Syntax errors occur when our program code violates the rules of
| Visual | Basic.NET, | and | they | will be | caught | when | we attempt | to  |
| ------ | ---------- | --- | ---- | ------- | ------ | ---- | ---------- | --- |
compile the program. Often syntax errors are misspelled variables
| or keywords, |     | improper | use | of VB.NET |     | language | elements, | or  |
| ------------ | --- | -------- | --- | --------- | --- | -------- | --------- | --- |
simple things like unmatched parentheses. Since VB.NETrequires
variable declaration by default, misspelled variables are caught
| immediately | and | can | be fixed. | This | is  | because | VB.NET | IDE |
| ----------- | --- | --- | --------- | ---- | --- | ------- | ------ | --- |
recognizes syntax errors prior to compilation and puts squiggly
blue lines underneath them even while we are writing our code.
We’re guessing you’ve probably had significant experience with
syntax errors over the course of the previous chapters. If we
happento miss a few syntax errors before compiling the program,
thecompilerwillcatchandlistthemintheTaskListwindowalong
| with a | full description |     | of the | error. |     |     |     |     |
| ------ | ---------------- | --- | ------ | ------ | --- | --- | --- | --- |
| LOGIC  | ERRORS           |     |        |        |     |     |     |     |
Logic errors are those that arise from incorrect results. In financial
| engineering, | our | programs     |     | frequently    |     | make  | dozens or | even  |
| ------------ | --- | ------------ | --- | ------------- | --- | ----- | --------- | ----- |
| hundreds     | of  | mathematical |     | calculations. |     | Quite | often our | first |
attemptatamathematicalalgorithmwillproduceincorrectresults,
for example, when a Black-Scholes calculator gives an incorrect
optionprice.Theonlywaytoavoidthesetypesoflogicerrorsisto
plan our programs carefully before writing code and to prototype
ouralgorithmsinExcelsothatwehavesomethingagainstwhichto
| verifyourresults. |     | Again,asyou |     | nodoubt |     | havefound,logicerrors |     |     |
| ----------------- | --- | ----------- | --- | ------- | --- | --------------------- | --- | --- |
arethehardesttypetofindandfixsinceitmaynotalwaysbeclear
exactly where they originate. In the worst-case scenario, a logic
| error can | turn | into a run-time |     | error | and crash | our | program. |     |
| --------- | ---- | --------------- | --- | ----- | --------- | --- | -------- | --- |
Team-LRN

ProblemSolving 153
RUN-TIME ERRORS
Run-time errors are those that often cause our programs to
terminate. Examples of logic errors that can turn into run-time
errors are divide-by-zero exceptions and array index out-of-range
exceptions. Other run-time errors may arise when we attempt to
connecttoadatabase,openafile,orsendanXMLmessage,where
errors beyond our control disrupt the flow of our program.
Whatcanbeespeciallyannoyingaboutrun-timeerrorsisthat
theymaynotshowupthefirsttime,oreventhefirsttentimes,we
executeaprogram—butonlyontheeleventhtime.Thatistosay,a
specific run-time error may occuronly when a certain sequence of
events takes place.
To deal with some potentially unavoidable run-time errors,
we can create exception handlers (blocks of code) to resolve or
handle errors in our programs and allow it to continue.
Inordertodemonstratethesedifferenttypesoferrors,wewill
need an example program.
FORECASTING COVARIANCE
Covariances between assets play an important part of many
automated trading and risk management systems. As shown in
Chapter 8, correlations and covariances are calculated using
historical price data. But covariances can also be updated and
forecast using GARCHmethodologiessince covariancerates often
exhibit mean reversion. One GARCH approach forecasts covari-
ances thusly:
ss^ ¼ (1(cid:1)a(cid:1)b)(cid:2)Cþar r þbss^
tþ1,i,j t,i t,j t,i,j
and
ss^ ¼ Cþ(aþb) j(cid:1)1(cid:2)(ss^ (cid:1)C)
tþn,i,j tþ1,i,j
where C is the long-run covariance.
Now let’s create a short program to forecast the covariance
between two stocks over the next 20 days.
Step 1 In VB.NETstart a new Windows application named
CovarForecast.
Team-LRN

154 IntroductiontoVB.NET
Step 2 On Form1, add a single text box with the multiline
property changed to True.
Step 3 In the Project menu bar item, select Add Class. You
can leave the file name as the default Class1.vb.
Step 4 IntheClass1codewindow,changetheclassnameto
CovarForecast and add the following code:
Public Class CovarForecast
Private dblForecasts As Double()
Private dblAlpha As Double
Private dblBeta As Double
Private dblPrevForecast As Double
Private dblCovariance As Double
Public Sub New()
dblForecasts = New Double(20) { }
dblPrevForecast = 0.00022627
dblCovariance = 0.000205927 0 Long Run Covariance
dblAlpha = 0.1943 0 Optimized coefficient
dblBeta = 0.5274 0 Optimized coefficient
CalcForecasts()
End Sub
Private Sub CalcForecasts()
Dim j As Integer
Dim newIBMreturn# = 0.0232
Dim newMSFTreturn# = 0.0352
dblForecasts(1) = (1 - dblAlpha - dblBeta) * dblCovariance + _
dblAlpha * newIBMreturn * newMSFTreturn + _
dblBeta * dblPrevForecast
For j = 2 To 20
dblForecasts(j) = dblCovariance + dblAlpha + dblBeta ^ _
(j - 1) * (dblForecasts(1) - dblCovariance)
Next j
End Sub
Public Function GetForecasts() As Double()
Return dblForecasts
End Function
End Class
End Sub
As with most classes, our CovarForecast class has several
Private member variables and a constructor function. Also the
CovarForecastclasshasaPrivatesubroutine CalcForecasts()and a
Public method GetForecasts().
Intheconstructormethod,wesetthevaluesoftheappropriate
variables including the long run covariance, the optimized values
of alpha and beta, and the previous 1-day-ahead forecast. Within
theCalcForecasts()subroutine,wereceivenewdataaboutourtwo
stocks, IBM and MSFT. Namely, a big up day in the market has
Team-LRN

| ProblemSolving |     |     |     |     |     |     |     |     | 155 |
| -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
raised both boats significantly, and consequently the historical
correlation will increase. However, over the long term, we expect
thecorrelationtoreverttothemean,aswewillseeinourforecasts.
| Step | 5 Back | in  | the | Form1      | code | window, | add | the following |     |
| ---- | ------ | --- | --- | ---------- | ---- | ------- | --- | ------------- | --- |
|      | code   | in  | the | Form1_Load |      | event:  |     |               |     |
Private Sub Form1_Load(ByVal sender As...) Handles MyBase.Load
Dim x As Integer
|     | Dim         | myForecasts   |                                 | As Double()   |       |              |           |           |     |
| --- | ----------- | ------------- | ------------------------------- | ------------- | ----- | ------------ | --------- | --------- | --- |
|     | Dim         | myCovars      | As                              | CovarForecast |       |              |           |           |     |
|     | myCovars    | =             | New CovarForecast()             |               |       |              |           |           |     |
|     | myForecasts |               | = myCovars.GetForecasts()       |               |       |              |           |           |     |
|     | For         | x = 1         | To myForecasts.GetUpperBound(0) |               |       |              |           |           |     |
|     |             | TextBox1.Text |                                 | &= x &        | " day | ahead        | forecast: | " & vbTab | & _ |
|     |             |               | Format(myForecasts(x),          |               |       | "0.0000000") |           | & vbCrLf  |     |
Next x
| End    | Sub        |     |     |        |         |         |     |                 |     |
| ------ | ---------- | --- | --- | ------ | ------- | ------- | --- | --------------- | --- |
| In the | Form1_Load |     |     | event, | we have | created |     | a CovarForecast |     |
objectnamedmyCovars.Onceweinstantiateanobjectbasedupon
the CovarForecast class, the constructor method performs all the
calculations and placesthe forecasted valuesinto anarray.We call
theGetForecastsmethodtoretrievethisarrayandloopthroughthe
| elements | to print | the | values   | in the     | text   | box. |         |      |      |
| -------- | -------- | --- | -------- | ---------- | ------ | ---- | ------- | ---- | ---- |
| Step     | 6 Run    | the | program  | (see       | Figure |      | 9.1).   |      |      |
| If you   | copied   |     | the code | correctly, |        | your | program | will | run. |
However,theresultsyougotwerenotthesameasshowninFigure
9.1. We have devilishly hidden a logic error in the code. But first
| let’s examine  |          | the syntax. |            | The program     |                | code | above | contains         | no  |
| -------------- | -------- | ----------- | ---------- | --------------- | -------------- | ---- | ----- | ---------------- | --- |
| syntax errors. | So       | we          | will       | create          | one and        | see  | what  | happens.         |     |
| Step           | 7 In     | the         | first line | of              | the Form1_Load |      |       | event, purposely |     |
|                | misspell |             | myCovars   |                 | as myCobars.   |      |       |                  |     |
| Dim            | myCobars | As          | New        | CovarForecast() |                |      |       |                  |     |
Notice that in your code the reference to the correctly spelled
| object myCovars |              | is  | now | underlined |       | in blue. |       | If we attempt | to      |
| --------------- | ------------ | --- | --- | ---------- | ----- | -------- | ----- | ------------- | ------- |
| compile         | the program, |     | a   | build      | error | will     | occur | which         | will be |
described in the Task List window. Double-clicking on this error
message in the Task List window will take you right to the line of
Team-LRN

| 156   |       |     |     |     |     | IntroductiontoVB.NET |     |
| ----- | ----- | --- | --- | --- | --- | -------------------- | --- |
| F I G | U R E | 9.1 |     |     |     |                      |     |
code containing the error, as shown in Figure 9.2. Syntax errors
such as this are common and easily fixed. Logic errors are much
| more difficult | to  | root out. |     |     |     |     |     |
| -------------- | --- | --------- | --- | --- | --- | --- | --- |
If we had not provided a picture showing the correct results,
| how would  | we            | know        | there is a problem |            | in the | program?     | With no |
| ---------- | ------------- | ----------- | ------------------ | ---------- | ------ | ------------ | ------- |
| method     | for verifying | our         | calculations,      | we         | are    | lost.        |         |
| As         | discussed     | in the      | methodology        | presented  |        | in Chapter   | 2, all  |
| complex    | calculations  |             | should first       | be modeled |        | in Excel     | before  |
| conversion | to            | programming | code.              | Figure     | 9.3    | demonstrates | the     |
prototyping of this model in spreadsheet format. If we know that
thespreadsheetcalculationsweredoneproperly,itisclearthatour
coded formulas are incorrect. Focusing on the lines containing the
Team-LRN

ProblemSolving 157
F I G U R E 9.2
F I G U R E 9.3
Team-LRN

| 158 |     |     |     |     |     | IntroductiontoVB.NET |     |     |
| --- | --- | --- | --- | --- | --- | -------------------- | --- | --- |
math,wecanusebreakpointsandtheLocalswindowtowatchthe
| values | of variables. |     |     |     |     |     |     |     |
| ------ | ------------- | --- | --- | --- | --- | --- | --- | --- |
BREAKPOINTS
| We can | set breakpoints |     | at  | different | lines | of code | to suspend |     |
| ------ | --------------- | --- | --- | --------- | ----- | ------- | ---------- | --- |
program execution. Then we can examine the value of variables
| currently    | in scope. |      | To enable | the | debugging | features | such | as    |
| ------------ | --------- | ---- | --------- | --- | --------- | -------- | ---- | ----- |
| breakpoints, | we        | must | compile   | the | program   | using    | the  | debug |
configuration.
Tosetabreakpoint,weclickthegrayareatotheleftoftheline
of code where we want to pause execution. Alternatively, we can
right-click over a line of code and select Insert Breakpoint.
| Step | 8 Set  | a       | breakpoint     | on  | the forecast | calculation |     | line    |
| ---- | ------ | ------- | -------------- | --- | ------------ | ----------- | --- | ------- |
|      | within |         | the For...Next |     | loop.        |             |     |         |
| Step | 9 Now  | run     | the program    |     | (see Figure  | 9.4).       |     |         |
| When | the    | program | reaches        | our | breakpoint,  | execution   |     | will be |
suspended. In this suspended state, we can explore the current
| values | of our variables. |       |     |     |     |     |     |     |
| ------ | ----------------- | ----- | --- | --- | --- | --- | --- | --- |
| F I    | G U R             | E 9.4 |     |     |     |     |     |     |
Team-LRN

ProblemSolving 159
F I G U R E 9.5
Step 10 On the Debug menu bar, open the Locals window.
The Locals window shows the current value of
0.0003353174341, which is consistent with our
spreadsheet model, so clearly the bug is not in the
line that defines the value of dblForecasts(1) (see
Figure 9.5).
Step 11 Press the F5 key to restart execution. The program
willproceedthroughthelooponetimeandrepause
when it again hits our breakpoint. This time the
Locals window shows the value of dblForecasts(2)
to be 0.19457416751494433. This is not right.
Step 12 Stop execution of the program altogether.
A quick inspection of the calculations line within the
For...NextloopshowsthatapairofparenthesesarounddblAlpha
plus dblBeta was left out. Add them in so that the corrected line
reads as follows:
Team-LRN

| 160             |     |     |               |                       |             |     | IntroductiontoVB.NET |     |
| --------------- | --- | --- | ------------- | --------------------- | ----------- | --- | -------------------- | --- |
| dblForecasts(j) |     | =   | dblCovariance |                       | + (dblAlpha |     | + dblBeta)           | ^ _ |
|                 |     |     | (j            | - 1)*(dblForecasts(1) |             |     | - dblCovariance)     |     |
Now run the program again and verify your answers against the
| Excel model. | This      | time     | the numbers |         | should | be          | correct.    |       |
| ------------ | --------- | -------- | ----------- | ------- | ------ | ----------- | ----------- | ----- |
| In           | addition  | to the   | Locals      | window, |        | there       | are several | other |
| windows      | and       | commands | that        | we will | look   | at briefly. |             |       |
| OTHER        | DEBUGGING |          |             | WINDOWS |        | AND         |             |       |
COMMANDS
The Autos, Watch, and Me windows all enable us to examine the
current value of variables or objects currently within scope. In the
Watch window, we can examine current variable values by typing
the variable name into the Name field and pressing Enter. We can
also change the value of variables listed in the Watch window for
testing and debugging purposes. To alter a variable’s value, enter
| the new  | value     | in the Value | field.  |        |        |       |         |          |
| -------- | --------- | ------------ | ------- | ------ | ------ | ----- | ------- | -------- |
| Clicking |           | the Continue |         | button | on the | Debug | menu    | bar will |
| resume   | execution | of a         | program | that   | we     | have  | paused. | The Stop |
Debuggingbuttonwillstoptheprogram.TheStepOverbutton,as
itsnameimplies,willcauseexecutionofthenextlineofcode.Ifthe
next line of code is a function or subroutine call, the function will
executeinitsentiretyinthatonestep.TheStepIntobutton,onthe
other hand, executes only the next line. If the line contains a
functioncall,controlwilltransfertothefunctiondefinitionforline-
by-linedebugging.Andfinally,theStepOutwillcauseaprocedure
to finish and then will return control to the calling line of code.
Uptothispoint,wehavebrieflyexaminedwaystoquicklyfix
syntaxandlogicerrorsinourprograms.Often,however,otherrun-
time errors beyond our control may arise that cause our programs
to crash. We can actually write code that will handle run-time
| errors on | the fly | and allow | our | program |     | to continue. |     |     |
| --------- | ------- | --------- | --- | ------- | --- | ------------ | --- | --- |
| EXCEPTION |         | HANDLING  |     |         |     |              |     |     |
Exception handling is the process of catching and dealing with
run-time errors as they occur, according to a prescribed set of
instructions. Although we often use the terms exception and error
Team-LRN

| ProblemSolving |     |     |     |     |     |     |     |     | 161 |
| -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
interchangeably, an exception is actually an object, which can
subsequentlybecomeanerrorandbreakourprogramifitdoesnot
| handle    | the exception       |     | properly. |     | VB.NETsupports |               | two  | methods | of  |
| --------- | ------------------- | --- | --------- | --- | -------------- | ------------- | ---- | ------- | --- |
| exception | handling—structured |     |           |     | and            | unstructured. | Both | methods |     |
allow us to plan for exceptions and thereby prevent them from
disruptingtheflowofourprogramsandpotentiallycrashingthem.
If you intend to create production software, you should consider
usingexceptionhandlersinanymethodthatmayitselfgeneratean
| error or | that | calls | procedures |     | that may | generate | them. |     |     |
| -------- | ---- | ----- | ---------- | --- | -------- | -------- | ----- | --- | --- |
Exceptionsthatoccurinproceduresthatarenotabletohandle
them are transmitted back to the calling procedure. If that calling
method is unable to handle it, it is then again transmitted back to
themethodcallingitandsoon.Inthisway,thecommonlanguage
run-time(CLR)searchesforanexceptionhandlerandwillcontinue
uptheseriesofprocedurecallstillitfindsone.Ifnohandlerisever
found, the CLR displays an error message and shuts the program
down. Wecan build into our programs structured or unstructured
exception handlers to catch exceptions before they become errors.
| Of  | course, | implementing |     |     | an exception-handling |     |     | strategy | into |
| --- | ------- | ------------ | --- | --- | --------------------- | --- | --- | -------- | ---- |
our software projects requires a fair amount of effort. As with
everything else in software development, planning pays off. Be
suretobuildyourstrategyintothedesignprocessfromtheget-go.
Itisverydifficulttoaddexception-handlingsystemslaterondown
the road. You can be assured, though, that once a software system
| has been | designed   |     | and    | implemented  |     | properly, | the | exception |     |
| -------- | ---------- | --- | ------ | ------------ | --- | --------- | --- | --------- | --- |
| handling | should     | not | hinder | performance. |     |           |     |           |     |
|          | Structured |     |        | Exception    |     | Handlers  |     |           |     |
Structured exception handlers consist of Try...Catch ...Final-
ly...End Try blocks of code that detect and respond to errors
during run time. (In the future, we will refer to these as simply
Try...Catchblocks.)Thepointinaprogramatwhichanexception
occurs is called the throw point. When something is “tried” and
createsanexception,theCLRthrowstheexception.Ifnoexception
| occurs, | however, |     | the | program | continues |     | execution | with | the |
| ------- | -------- | --- | --- | ------- | --------- | --- | --------- | ---- | --- |
statement following the End Try. In this way, structured exception
handlers help us create robust applications that rarely crash.
Team-LRN

162 IntroductiontoVB.NET
Try
[Some code in here that may generate an error.]
Catch exp as Exception
[Code to execute when a problem occurs.]
Finally
[Code that will always run.]
End Try
WithinaTry...Catchblock,theTryblockwillusuallycontain
somecodewearewaryof,thatis,somecodethatmaygeneratean
error.Forexample,ifwearetryingtoconnecttoadatabaseorsend
a message over the Internet, a problem beyond our control may
occurandcreateanerror.Whenanexceptionoccurs,theTryblock
terminates immediately, and the CLR searches the available Catch
statements and executes the first one that is able to handle an
exceptionofthattype.WithinaTry...Catchblock,thereareoneor
more Catch statements, each specifying an optional exception
parameter, which represents a unique exception type. A
parameterless Catch will catch all exception types. In fact,
exceptions of any kind are actually Exception objects that inherit
from the System.Exception class. The Try...Catch mechanism
allowsExceptionobjectsandderivedclassobjectstobethrownand
caught. Once caught, the Catch handler interacts with the
Exception object in a way that we can control.
The optional Finally block can contain code that will always
execute, regardless of whether an exception is thrown. Because it
will always run immediately before the Try...Catch block loses
scope,theFinallyblockisusuallyanexcellentlocationinwhichto
place deallocation code, for example, close files or connections or
release objects.
Let’s add a Try...Catch block to our program.
Step 13 In the Form1_Load event, change the code to
instantiate a CovarForecast object to include the
following:
Dim myCovars As CovarForecast
Try
myCovars = New CovarForecast()
Catch exp As Exception
MsgBox(exp.Message)
Exit Sub
End Try
Team-LRN

| ProblemSolving |             |     |       |      |       |     |            | 163    |
| -------------- | ----------- | --- | ----- | ---- | ----- | --- | ---------- | ------ |
| This           | Try...Catch |     | block | will | catch | any | exceptions | thrown |
during the execution of the constructor method of the myCovars
object, which will propagate back up to our calling function. As it
standsnow,allexceptionswillbecaughtbytheoneandonlyCatch
| statement, | which   | will      | show | a   | MessageBox        | with | the | Exception |
| ---------- | ------- | --------- | ---- | --- | ----------------- | ---- | --- | --------- |
| object’s   | message | property. |      | The | Exception.Message |      |     | property  |
contains a default message associated with the specific Exception
object.Thismessagecanbecustomizedbypassingamessagetothe
| Exception    | object’s    | constructor   |             | function.   |             |           |                   |          |
| ------------ | ----------- | ------------- | ----------- | ----------- | ----------- | --------- | ----------------- | -------- |
| At           | this point, | however,      |             | no          | exceptions  | will      | be thrown         | by our   |
| program.     | So let’s    | create        | one.        |             |             |           |                   |          |
| Step         | 14          | In the        | constructor |             | method      | of        | the CovarForecast |          |
|              |             | class,        | lower       | the         | number      | of        | elements          | in the   |
|              |             | dblForecasts  |             | array       | to 10,      | which     | will cause        | an array |
|              |             | out-of-bounds |             | exception.  |             |           |                   |          |
| dblForecasts |             | =             | New         | Double(10)  | f           | g         |                   |          |
| Step         | 15          | Run the       | program     |             | (see Figure | 9.6).     |                   |          |
| Again,       | our         | Catch         | handler,    |             | which       | specifies | Exception,        | will     |
| catch all    | exceptions  |               | types.      |             |             |           |                   |          |
| Step         | 16          | Change        | the         | Try...Catch | block       | to        | the following:    |          |
Try
|       | myCovars | =                           | New | CovarForecast() |     |     |     |     |
| ----- | -------- | --------------------------- | --- | --------------- | --- | --- | --- | --- |
| Catch | exp      | As IndexOutOfRangeException |     |                 |     |     |     |     |
MsgBox(exp.Message)
Exit Sub
| Catch | exp | As InvalidCastException |     |     |     |     |     |     |
| ----- | --- | ----------------------- | --- | --- | --- | --- | --- | --- |
MsgBox(exp.Message)
| F I G | U R | E 9.6 |     |     |     |     |     |     |
| ----- | --- | ----- | --- | --- | --- | --- | --- | --- |
Team-LRN

| 164 |     |     |     |     |     |     | IntroductiontoVB.NET |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------- | --- |
Exit Sub
Finally
|                          | MsgBox(“Finally |     |      | block   | exectuing.”)          |          |           |          |
| ------------------------ | --------------- | --- | ---- | ------- | --------------------- | -------- | --------- | -------- |
| End                      | Try             |     |      |         |                       |          |           |          |
| This                     | time,           | we  | have | defined | two                   | specific | exception | types—   |
| IndexOutOfRangeException |                 |     |      | and     | InvalidCastException. |          |           | Further, |
we have added a Finally block, which will execute whether or not
| we encounter |     | an error. |     |     |     |     |     |     |
| ------------ | --- | --------- | --- | --- | --- | --- | --- | --- |
| Step         | 17  |           |     |     |     |     |     |     |
IntheconstructormethodoftheCovarForecastclass,
|                 |     | change  | the     | dblPrevForecast |        | to  | some string | value. |
| --------------- | --- | ------- | ------- | --------------- | ------ | --- | ----------- | ------ |
| dblPrevForecast |     |         | = "IBM" |                 |        |     |             |        |
| Step            | 18  | Run the | program | (see            | Figure |     | 9.7).       |        |
In this case, the exception will first be thrown by the invalid
castfrom“IBM”toadouble.Oncetheexceptionhasbeenhandled,
theFinallyblockwillrunandalsoshowamessagebox.Noticealso
that in the current set of Catch handlers, exceptions other than the
IndexOutOfRangeExceptionortheInvalidCastExceptionclasswill
| not be   | handled | and         | will cause | the          | program |          | to terminate. |            |
| -------- | ------- | ----------- | ---------- | ------------ | ------- | -------- | ------------- | ---------- |
| Speaking |         | of specific |            | error types, |         | be aware | that          | .NET’s CLR |
allows division by zero. Division by zero will produce a special
| value | “not | a number,” | written |     | in string |     | form as | “NaN.” Our |
| ----- | ---- | ---------- | ------- | --- | --------- | --- | ------- | ---------- |
programs can be made to test for NaN results by using constants
| for positive |              | or negative | infinity. |           |     |          |     |     |
| ------------ | ------------ | ----------- | --------- | --------- | --- | -------- | --- | --- |
|              | Unstructured |             |           | Exception |     | Handling |     |     |
In unstructured exception handling, we place an On Error GoTo
statement at the beginning of a block of code. The On Error GoTo
will then handle any and all exceptions occurring within that
| F I | G U R | E 9.7 |     |     |     |     |     |     |
| --- | ----- | ----- | --- | --- | --- | --- | --- | --- |
Team-LRN

| ProblemSolving |     |     |     |     |     |     |     |     | 165 |
| -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
particular block regardless of class. When an exception is raised
aftertheOnErrorGoTostatement,theprogramexecutionwillgoto
the line specified in the On Error statement. As with structured
error handling, if a call is made to another function, and an
exceptionoccurswithinthatfunction,itwillpropagatebacktothe
calling method if it is not handled within the function. Here is the
| basic layout | of the  | On   | Error        | GoTo | error | handler:     |     |     |         |
| ------------ | ------- | ---- | ------------ | ---- | ----- | ------------ | --- | --- | ------- |
| Sub          | mySub() |      |              |      |       |              |     |     |         |
| On           | Error   | GoTo | ErrorHandler |      |       |              |     |     |         |
|              | [Some   | code | in           | here | that  | may generate |     | an  | error.] |
Exit Sub
ErrorHandler:
|     | [Code | to  | execute | when | a   | problem | occurs.] |     |     |
| --- | ----- | --- | ------- | ---- | --- | ------- | -------- | --- | --- |
Resume
| End   | Sub   |        |        |          |     |         |     |           |      |
| ----- | ----- | ------ | ------ | -------- | --- | ------- | --- | --------- | ---- |
| If an | error | occurs | within | mySub(), |     | program |     | execution | will |
automatically jump to the ErrorHandler label. The Resume state-
| ment included |     | in the | ErrorHandler |     | will | then | resume | execution |     |
| ------------- | --- | ------ | ------------ | --- | ---- | ---- | ------ | --------- | --- |
back at the line where the error occurred. Of course, the Exit Sub
statement is mandatory, or else program execution will run into
ErrorHandler when it comes to the end of the subroutine code.
| Let’s look | at an     | example: |     |            |     |       |     |      |        |
| ---------- | --------- | -------- | --- | ---------- | --- | ----- | --- | ---- | ------ |
| Step       | 19 Change |          | the | Form1_Load |     | event |     | code | to the |
following:
Private Sub Form1_Load(ByVal sender As...) Handles MyBase.Load
|     | On Error | GoTo | ErrorHandler |     |     |     |     |     |     |
| --- | -------- | ---- | ------------ | --- | --- | --- | --- | --- | --- |
Dim x As Integer
|     | Dim myForecasts |                        | As                           | Double() |           |              |     |           |     |
| --- | --------------- | ---------------------- | ---------------------------- | -------- | --------- | ------------ | --- | --------- | --- |
|     | Dim myCovars    |                        | As CovarForecast             |          |           |              |     |           |     |
|     | myCovars        | = New                  | CovarForecast()              |          |           |              |     |           |     |
|     | myForecasts     |                        | = myCovars.GetForecasts()    |          |           |              |     |           |     |
|     | For x           | = 1 To                 | myForecasts.GetUpperBound(0) |          |           |              |     |           |     |
|     | TextBox1.Text   |                        | &=                           | x & "    | day ahead | forecast:    |     | " & vbTab | & _ |
|     |                 | Format(myForecasts(x), |                              |          |           | "0.0000000") |     | & vbCrLf  |     |
Next x
Exit Sub
ErrorHandler:
MsgBox(Err.Description)
| End Sub |        |     |         |      |        |       |     |     |     |
| ------- | ------ | --- | ------- | ---- | ------ | ----- | --- | --- | --- |
| Step    | 20 Run | the | program | (see | Figure | 9.8). |     |     |     |
Team-LRN

| 166   |             |       |     |         |      | IntroductiontoVB.NET |          |      |
| ----- | ----------- | ----- | --- | ------- | ---- | -------------------- | -------- | ---- |
| F I G | U R E       | 9.8   |     |         |      |                      |          |      |
| The   | Err object, | which |     | is used | only | with the             | On Error | GoTo |
statement, contains properties that are set by the most recent
exception. The Number property holds a value corresponding to
the cause of the error. The Description property holds a text
message that describes the nature of the error. Unstructured error-
handling routines rely on the Err.Number property to determine
the error’s cause. If exceptions of multiple types may occur, our
error-handling routine should test the Number value for proper
handling.
| An     | alternative | to  | the        | On Error | GoTo    | structure | is  | On Error |
| ------ | ----------- | --- | ---------- | -------- | ------- | --------- | --- | -------- |
| Resume | Next, which |     | will cause |          | program | execution | to  | continue |
withthelineofcodeimmediatelyfollowingtheonethatgenerated
| the exception. | In  | this | way, | On Error |     | Resume Next | allows | our |
| -------------- | --- | ---- | ---- | -------- | --- | ----------- | ------ | --- |
program to continue despite an exception. In fact, the On Error
ResumeNextstructuremayinsomecasesbepreferabletoOnError
GoTo, especially when accessing objects. On Error Resume Next
allows us to place error-handling code specifically where errors
will occur, as opposed to shifting to another line in the procedure.
| While | we have | touched |     | only | briefly | on unstructured |     | error |
| ----- | ------- | ------- | --- | ---- | ------- | --------------- | --- | ----- |
handling, be aware that, in general, use of the On Error GoTo
structure will degrade performance. Furthermore, unstructured
error handling is often difficult to debug. So in most cases,
| structured | error-handling |           | techniques |     | are | preferable. |     |     |
| ---------- | -------------- | --------- | ---------- | --- | --- | ----------- | --- | --- |
| THE THROW  |                | STATEMENT |            |     |     |             |     |     |
InVB.NETwecanusetheThrowstatementtopurposelythrowan
| exception. | Throw | creates |            | an exception |     | object       | that       | we can |
| ---------- | ----- | ------- | ---------- | ------------ | --- | ------------ | ---------- | ------ |
| manipulate | with  | either  | structured |              | or  | unstructured | exception- |        |
Team-LRN

| ProblemSolving |     |       |     |     |     |     |     | 167 |
| -------------- | --- | ----- | --- | --- | --- | --- | --- | --- |
| F I G          | U R | E 9.9 |     |     |     |     |     |     |
handlingcode.WeoftenuseThrowtotraperrorswithinourcode,
because as we have seen, VB.NET will move up the hierarchy of
procedures till it encounters an appropriate exception handler.
| Wheneveran |         | exceptionis                                    |           | thrown | witha | Throw statement,the |          | Err |
| ---------- | ------- | ---------------------------------------------- | --------- | ------ | ----- | ------------------- | -------- | --- |
| object is  | set and | a new                                          | Exception | object |       | is instantiated.    |          |     |
| Step       | 21      | IntheCovarForecastclasscode,correcttheprevious |           |        |       |                     |          |     |
|            |         | errors                                         | and       | add a  | Throw | statement           | to raise | a   |
DllNotFoundException.
| dblForecasts    |     |                              | = New        | Double(20) | {      | }      |          |     |
| --------------- | --- | ---------------------------- | ------------ | ---------- | ------ | ------ | -------- | --- |
| dblPrevForecast |     |                              | = 0.00022627 |            |        |        |          |     |
| Throw           | New | DllNotFoundException("Error, |              |            |        | error, | error.") |     |
| Step            | 22  | Run                          | the program  | (see       | Figure | 9.9).  |          |     |
In the next chapter we will look at how to create .dll files.
SUMMARY
| In this | chapter | we  | have | addressed | solving | problems |     | in our |
| ------- | ------- | --- | ---- | --------- | ------- | -------- | --- | ------ |
program that occur during design time and run time. Further, we
showed some techniques for finding logic errors in our programs.
VB.NEThasawealthoftoolsforhelpingfinancialengineersdebug
production programs before implementation. Although for read-
ability’s sake, we will often skip error-handling routines in this
book, real software development necessitates that we include run-
time error-handling routines in the designs of our programs. In
general, it is preferable to take advantage of VB.NET’s structured
error-handling model and its inherent efficiency as opposed to the
| unstructured |     | On Error | GoTo | model. |     |     |     |     |
| ------------ | --- | -------- | ---- | ------ | --- | --- | --- | --- |
Team-LRN

| 168 |     |     |     |     | IntroductiontoVB.NET |     |
| --- | --- | --- | --- | --- | -------------------- | --- |
PROBLEMS
1. What do the terms syntax, logic, and run-time errors mean?
| 2. What | do breakpoints |                  | allow     | us to do? |                    |     |
| ------- | -------------- | ---------------- | --------- | --------- | ------------------ | --- |
| 3. What | window         | in               | the Debug | menu      | bar lets us change | the |
| value   | of a variable  |                  | during    | run time? |                    |     |
| 4. What | is structured  |                  | exception | handling? | What is unstruc-   |     |
| tured   | exception      | handling?        |           |           |                    |     |
| 5. What | is the         | System.Exception |           | class?    |                    |     |
Team-LRN

| ProblemSolving |     |     |     |     | 169 |
| -------------- | --- | --- | --- | --- | --- |
| PROJECT        | 9.1 |     |     |     |     |
Several errors may occur when a user enters a value to be used in
calculations.Forexample,ausermayenter“IBM”forastockprice
or some invalid symbol in the txtTicker text box. Create a simple
VB.NETWindowsapplicationthatwillacceptastockticker,astock
price, and a number of shares to calculate a market capitalization.
Use a structured error-handling mechanism with multiple Catch
statements to prompt the user to reenter correct data based upon
| the specific | exception | type.       |              |             |        |
| ------------ | --------- | ----------- | ------------ | ----------- | ------ |
| PROJECT      | 9.2       |             |              |             |        |
| Create a     | Windows   | application | that accepts | user inputs | for an |
options symbol, a stock price, and a volatility and that calculates
theBlack-ScholespriceandGreeksforeitheracalloraput.Adda
structured error-handling mechanism to ensure the program will
neverbreak,regardlessofwhattheuserenters.Also,yourprogram
should recognize specific exception types and prompt the user to
reentervalidvalues.Printoutthecalculatedvaluesintextboxeson
the screen.
Team-LRN

This page intentionally left blank.
Team-LRN

| C H  | A P T E | R 10 |        |     |     |     |     |     |
| ---- | ------- | ---- | ------ | --- | --- | --- | --- | --- |
| .NET | Type    |      | System |     |     |     |     |     |
I
n Chapter 7 we looked at classes and objects. Yet in fact, classes
| are only | one of many | mechanisms |     | we  | can use | to  | describe | the |
| -------- | ----------- | ---------- | --- | --- | ------- | --- | -------- | --- |
functionality of objects in our programs. What we really create in
| VB.NET | code are types. | The | term | type | represents |     | a broader |     |
| ------ | --------------- | --- | ---- | ---- | ---------- | --- | --------- | --- |
description of any combination of data storage and functionality.
| Classes are | but one | example | of  | a type, | as  | are variables |     | and |
| ----------- | ------- | ------- | --- | ------- | --- | ------------- | --- | --- |
functions.
Instances of types allocate space fordata storage and provide
us with the behaviors we require. Deciding what types to use—
classes, modules, subroutines, functions, structures, etc.—in our
programsfordatamanipulationwillbethefocusoftheremainder
| of the technology | portions | of  | the book. |     |     |     |     |     |
| ----------------- | -------- | --- | --------- | --- | --- | --- | --- | --- |
TYPES
A type is a generic term used to describe a representation of a
value.Instancesoftypes,intheirvariousforms,encapsulateallthe
| logic in | our programs, | and | so  | fully | understanding |     | types | is  |
| -------- | ------------- | --- | --- | ----- | ------------- | --- | ----- | --- |
fundamental to higher-level .NET programming, not just VB.NET.
| Through    | the .NET Framework’s |     |       | common | language |         | specification |     |
| ---------- | -------------------- | --- | ----- | ------ | -------- | ------- | ------------- | --- |
| and common | type system,         |     | it is | easy   | to use   | several | different     |     |
languagestocreateasingleapplication,althoughthisbookisonly
concernedwithVisualBasic.NET.Thiscommontypesystemlooks
like this:
171
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

| 172 |     |     |     |     |     |     | IntroductiontoVB.NET |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------- | --- | --- |
VB.NETCommon
| TypeSystem |     |     |     |     |     |     | Example |     |     |
| ---------- | --- | --- | --- | --- | --- | --- | ------- | --- | --- |
Interfaces
| Valuetypes     |     |     |     |     | Variables,constants,structures,etal. |     |     |     |     |
| -------------- | --- | --- | --- | --- | ------------------------------------ | --- | --- | --- | --- |
| Referencetypes |     |     |     |     | Classes,arrays,etc.                  |     |     |     |     |
Interfaces
| An interface |     | specifies  | a group |             | of methods    |      | that      | can only | be   |
| ------------ | --- | ---------- | ------- | ----------- | ------------- | ---- | --------- | -------- | ---- |
| implemented  |     | by another |         | class       | or structure. |      | We        | cannot   | then |
| instantiate  |     | interfaces | by      | themselves. |               | As a | practical | matter,  |      |
predefined .NETinterfaces start with the letter I, as in ICollection,
IList,andIComparable.IntheVB.NEThelpfiles,wecansurveythe
different interfaces and their respective members. In addition, we
can declare our own, user-defined interfaces. Here is an example:
| Interface  |           | ITradable |            |           |      |             |     |              |      |
| ---------- | --------- | --------- | ---------- | --------- | ---- | ----------- | --- | ------------ | ---- |
|            | Function  |           | Buy(ByVal  | Price     | As   | String)     | As  | Double       |      |
|            | Function  |           | Sell(ByVal | Price     | As   | String)     | As  | Double       |      |
| End        | Interface |           |            |           |      |             |     |              |      |
| The        | ITradable |           | interface  | indicates | that | we          | can | buy or       | sell |
| something, |           | but does  | not define |           | how  | it happens. |     | So different |      |
financial instruments have the ability to be traded electronically,
and therefore, as objects, they should implement the ITradable
interface. We have not though specified exactly how they will
| be traded, |     | since the | implementation |     |     | of a | trade | for different |     |
| ---------- | --- | --------- | -------------- | --- | --- | ---- | ----- | ------------- | --- |
instruments may be very different. For example, routing a buy
ordertotheISEmayrequireamuchdifferentimplementationthan,
| say, routing |     | a buy order | to the | CME. |     |     |     |     |     |
| ------------ | --- | ----------- | ------ | ---- | --- | --- | --- | --- | --- |
Sowehavedeferredtheimplementationoftheinterfacetothe
definition of the class, which implements the interface. None-
| theless, | the “stub” |         | is there. |                |     |     |           |      |       |
| -------- | ---------- | ------- | --------- | -------------- | --- | --- | --------- | ---- | ----- |
| We       | may        | at some | point     | then implement |     | an  | interface | like | this: |
| Class    | InstrObj   |         |           |                |     |     |           |      |       |
|          | Implements |         | ITradable |                |     |     |           |      |       |
...
|     | Public | Function   | Buy(ByVal     |     | Price | As String) |     | As Double | _   |
| --- | ------ | ---------- | ------------- | --- | ----- | ---------- | --- | --------- | --- |
|     |        | Implements | ITradable.Buy |     |       |            |     |           |     |
...
End Function
| End | Class |     |     |     |     |     |     |     |     |
| --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
Team-LRN

.NETTypeSystem 173
Classes may implement multiple interfaces although inter-
faces do not support multiple inheritance in derived classes. If a
class definition includes that of ITradable (the buy and sell
interfaces)andanobjectisinstantiated,wecancallthesellmethod:
Dim myInstr As New InstrObj()
myInstr.Sell("Market")
ASSEMBLIES
Assemblies are the fundamental building blocks of VB.NET
applicationsandareheldinexecutablefiles(EXEs)ordynamiclink
libraryfiles(DLLs).Anassemblyisacollectionoftypes,whichcan
be modules, interfaces, classes, delegates, enumerations, struc-
tures, and other units of functionality. When we create a VB.NET
application, the most common assemblies are already referenced
for us. However, if we need to use an assembly that is not already
referenced, we need to add a reference to the corresponding DLL
file and use the Imports statement for the appropriate namespace.
Oncewehaveaddedareferencetotheassemblyandimportedthe
namespace,alltheclasses,properties,methods,andothertypesin
thenamespaceareavailabletoourapplicationasiftheassembly’s
codewerepartofit.Beawarethatasingleassemblymightcontain
multiplenamespaces,andeachnamespacemightcontainmultiple
types.
NAMESPACES
The VB.NET Framework class library is made up of namespaces,
which contain and organize types, which are defined in an
assembly.Iftwoclasseshavethesamename,wecanstillusethem
bothaslongastheyareindifferentnamespacesandwequalifythe
class names using the namespace. “Fully qualified” object names
are prefixed with the name of the namespace where the object is
defined. So, for example, System.Windows.Forms.ListBox is the
fullyqualifiednameoftheListboxclasssincewehaveincludedthe
namespace.AllnamespacesinVB.NETbeginwitheitherSystemor
Microsoft.
Team-LRN

174 IntroductiontoVB.NET
IMPORTS STATEMENT
TheImportsstatementdoesnotitselfprovideaccesstoassemblies,
butrathersimplifiesaccesstothembyeliminatingtheneedtofully
qualifynamedreferences.Thatis,wecanusetypesdefinedwithin
the imported namespace of the assembly without qualification. A
module may contain any number of references and Imports
statements, as long as the Imports statements appear after any
Option statements and before any other code. For example,
Imports System.Data.OleDb
BUILDING AN OPTIONS LIBRARY
Creating an assembly with namespaces and types in VB.NET is
very simple. We simply need to create a new class library, build it,
and add a reference to the .dll file in future programs.
Step 1 In VB.NET, create a new project.
Step 2 In the New Project window, select Class Library and
name your project Options.
Step 3 Within the class definition add the code for the
StockOption class from the CD, the same one
discussed in Chapter 7.
Step 4 Addanewclassmodule,nametheclassCallOption,
and paste in the code for the CallOption class from
the CD. Also add a class module for the PutOption
class, the same one discussed in Chapter 7.
Step 5 On the menu bar, select Build and Build Options.
Close VB.NET.
Now a DLL filehas been created, and we can add a reference
to it in subsequent programs that we write and use these classes
withouthavingtocopyandpasteoverandoveragain.Let’stakea
look.
Step 1 Create a new Windows application named
LibraryExample.
Team-LRN

.NETTypeSystem 175
Step 2 In the Project menu, click on Add Reference. When
the Add Reference window shows up, click on
Browse. In the Browse window, find the Options
project folder, and within the bin subfolder double-
click on the FinMath.dll file. Click OK.
Step 3 Add four labels to your form.
Step 4 In the Form1_Load event add the following code:
Imports Options
Public Class Form1
Inherits System.Windows.Forms.Form
Private Sub Form1_Load(ByVal sender As...) Handles MyBase.Load
Dim myOption As New CallOption("IBMDP")
myOption.StockPrice = 80
myOption.IntRate = 0.1
myOption.Volatility = 0.25
Label1.Text = myOption.Underlying
Label2.Text = myOption.ExpMonth
Label3.Text = myOption.Strike
Label4.Text = Format(myOption.BSPrice, "#.####")
End Sub
End Class
Notice the use of the Imports Options syntax at the
top of the coding. This informs the compiler that we
will be using classes located in the Options name-
space.
Step 5 Run the program (see Figure 10.1).
F I G U R E 10.1
Team-LRN

176 IntroductiontoVB.NET
VOLATILITY SMILES
On an options exchange, dozens of option contracts trade on each
stock.Alltheoptionswithagivenexpirationmonthcreateastrike
structure of implied volatility, which usually has the shape of a
smile. All the options with a given strike form a term structure of
impliedvolatility.Togetherthestrikeandtermstructurescreatean
implied volatility surface. That is, any given stock has several
implied volatilities—though, as we saw in a previous chapter, we
can use four sets of near-the-money (nearby and second nearby)
puts and calls to calculate a single at-the-money volatility.
As a matter of practice, options with nearby expirations have
prices determined more by supply and demand as opposed to
volatilityforecasts,whereaslongerdatedoptionshavepricesmore
greatly influenced by historical volatility. That is to say, near-term
options tend to have implied volatilities greater than historical
volatilities would imply, and longer-term options tend to have
volatilities more in line with past movements of the underlying
security. The graph in Figure 10.2 illustrates a volatility surface
where across any given expiration there is a volatility smile.
F I G U R E 10.2
Team-LRN

.NETTypeSystem 177
Models of the volatility smile, or skew, enable us to examine
how the out-of-the-money volatilities are related to at-the-money
volatility and how this relationship behaves as price, time, and
volatility itself change. There are a wide range of methods for
modeling this relationship between option strikes and volatility,
includinglinearandnonlinearregressionmodelsandinterpolation
and cubic spline models. Many of these models require the use of
| matrix   | algebra | and regression. |         |      |      |     |                |
| -------- | ------- | --------------- | ------- | ---- | ---- | --- | -------------- |
| Included |         | on the          | CD with | this | book | is  | the MatrixMath |
assembly.Savethis.dllfiletoyourharddrivebeforeyoubeginthe
next project. The MatrixMath.dll contains the following shared
functions:
Matrix
| Function |     | Description |     |     |     | Example |     |
| -------- | --- | ----------- | --- | --- | --- | ------- | --- |
MMult() Matrixmultiplicationfor dblArray¼Matrix.MMult(Aarray,Barray)
two2-dimensional
matrices
| MInverse() | Matrixinversion |     |     | dblArray¼Matrix.Minverse(myArray) |     |     |     |
| ---------- | --------------- | --- | --- | --------------------------------- | --- | --- | --- |
MTranspose() Matrixtransposition dblArray¼Matrix.MTranspose(myArray)
MDeterm() Matrixdeterminant dblDouble¼Matrix.MDeterm(myArray)
MMult2by1() Matrixmultiplicationfora dblVector¼Matrix.MMult2by1
|     |     | 2-dimensionalmatrixby |     |     | (AArray,BVector) |     |     |
| --- | --- | --------------------- | --- | --- | ---------------- | --- | --- |
avector
| MultRegression() | Multiplelinearregression |     |     | dblArray¼ |     |     |     |
| ---------------- | ------------------------ | --- | --- | --------- | --- | --- | --- |
Matrix.MultRegression
(Aarray,Bvector)
In the case of the MatrixMath.dll, we will not instantiate any
objects based upon the class in this namespace. Rather we will
simplyusethePublicSharedclassfunctionsasyouwillsee.Hereis
an abbreviated code snippet from the MatrixMath.dll to illustrate
| the use | of Public | Shared   | class     | functions:           |     |       |              |
| ------- | --------- | -------- | --------- | -------------------- | --- | ----- | ------------ |
| Public  | Class     | Matrix   |           |                      |     |       |              |
|         | Public    | Shared   | Function  | MTranspose(ByRef...) |     |       | As Double(,) |
|         |           | 0 Matrix | transpose | code                 | in  | here. |              |
End Function
| End | Class |     |     |     |     |     |     |
| --- | ----- | --- | --- | --- | --- | --- | --- |
In allotherways,creatinga.dllwithclassfunctionsisthesameas
| previously | discussed |     | for class | libraries. |     |     |     |
| ---------- | --------- | --- | --------- | ---------- | --- | --- | --- |
Inthenextprojectwewillparameterizeonearm,orhalf,ofthe
front-month volatility smile using a linear structure with level (L),
Team-LRN

| 178 |     |     |     |     |     |     | IntroductiontoVB.NET |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------- | --- |
slope (S), and curvature (C) parameters. This model is closely
related to the yield curve models proposed by Nelson and Siegel
| (1987) and | Wilmer | (1996). |             |            |     |            |     |     |
| ---------- | ------ | ------- | ----------- | ---------- | --- | ---------- | --- | --- |
|            |        | ss^     | ¼ L(cid:1)x | þS(cid:1)x |     | þC(cid:1)x |     |     |
|            |        |         | i           | 1          | 2   |            | 3   |     |
where:
|     |     |     |     | (cid:3) | (cid:1) |          | (cid:2)(cid:4) |     |
| --- | --- | --- | --- | ------- | ------- | -------- | -------------- | --- |
|     |     |     |     |         | X       | (cid:2)P |                |     |
|     |     | x ¼ | x   | ¼       |         | i        |                |     |
|     |     | 1 1 |     | 2       | exp     |          |                |     |
t
|     |     | (cid:3) | (cid:2)PÞ2 |            | (cid:1)   |           | (cid:2)(cid:4) |     |
| --- | --- | ------- | ---------- | ---------- | --------- | --------- | -------------- | --- |
|     |     |         | ðX         |            | (cid:2)ðX | (cid:2)PÞ |                |     |
|     |     | x ¼     | i          | (cid:1)exp |           | i         |                |     |
3
|     |     |     | t   |     |     | t   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
and:
L¼the
|     |     | level | of         | the smile, | denoting |     | the at-the- |     |
| --- | --- | ----- | ---------- | ---------- | -------- | --- | ----------- | --- |
|     |     | money | volatility |            |          |     |             |     |
S¼the
|     |        | slope     | of    | the smile |       |     |     |     |
| --- | ------ | --------- | ----- | --------- | ----- | --- | --- | --- |
|     | C¼the  | curvature |       | of the    | smile |     |     |     |
|     | X ¼the | strike    | price | i         |       |     |     |     |
i
P¼the
|         |        | price     | of         | the underlying |     | stock     |             |         |
| ------- | ------ | --------- | ---------- | -------------- | --- | --------- | ----------- | ------- |
|         | t¼the  | optimized |            | location       |     | parameter |             |         |
| In this | model, | the       | parameters |                | L,  | S, and    | C are found | using a |
multiple-regressionalgorithmalongwithasimpleiterativeprocess
to find the optimal location parameter t. So the method is to
increase t by 1 and repeat the regression until the sum of the
squared errors is minimized. Let’s start by getting the multiple
regression set up properly. As always, we should first model the
algorithm using Excel before we code to ensure the correctness of
our algorithms. The Excel spreadsheet file LSCforVol.xls, which
| models this | method,                                       |     | is included    |     | on the | CD. |            |           |
| ----------- | --------------------------------------------- | --- | -------------- | --- | ------ | --- | ---------- | --------- |
| Step        | 1 OpenanewWindowsapplicationnamedLSCforVol.   |     |                |     |        |     |            |           |
| Step        | 2 AddasingletextboxtoForm1,andleavethedefault |     |                |     |        |     |            |           |
|             | name,                                         |     | Textbox1.Text. |     | Also,  |     | change the | Multiline |
propertyofTextbox1toTrue.Youshouldnowbeable
|     | to  | increase | the | size | of Textbox1 |     | on your form. |     |
| --- | --- | -------- | --- | ---- | ----------- | --- | ------------- | --- |
Team-LRN

.NETTypeSystem 179
Step 3 On the menu bar, select Project and Add Reference.
Browse to find the MatrixMath.dll file on your hard
drive and click OK.
Step 4 In the Form1 code window, add the following code:
Imports MatrixMath
Public Class Form1
Inherits System.Windows.Forms.Form
Private Sub Form1_Load(ByVal sender As...) Handles MyBase.Load
Dim x As Integer
Dim Tau As Integer = 10
Dim AMatrix As Double(,) = New Double(7, 2) { }
Dim dblStrikes As Double() = New Double() _
f0, 5, 10, 15, 20, 25, 30, 35g
Dim dblVolatilities As Double() = New Double() _
f25, 26, 29, 35, 37, 43, 50, 65g
Dim LSCparams As Double() = New Double(2) f g
For x50 To 7
AMatrix(x, 0) = 1
AMatrix(x, 1) = Math.Exp(dblStrikes(x) / Tau) * _
dblStrikes(x)
AMatrix(x, 2) = (dblStrikes(x) / Tau) * _
Math.Exp(-dblStrikes(x) / Tau) * dblStrikes(x)
Next x
LSCparams = Matrix.MultRegression(AMatrix, dblVolatilities)
TextBox1.Text = "Level: " & Format(LSCparams(0), "##.0000") & _
vbCrLf & "Slope: " & Format(LSCparams(1), "##.0000") & _
vbCrLf & "Curvature: " & Format(LSCparams(2), "##.0000") & _
vbCrLf & "Tau: " & Str(Tau)
End Sub
End Class
Step 5 Run the program (see Figure 10.3).
This model runs the LSC model for one arm of the volatility
skew with a hard-coded value of t¼10. However, this is not the
value of t that minimizes the sum of the squared errors. The
Windows application LSCforVol included on the CD contains the
full code for calculating the optimized parameters for the above
model.Intheoptimizedversionthecorrectvaluefortis12,giving
new values to the parameters L, S, and C as shown in Figure 10.4.
Another method for modeling volatility smiles is to use a
fourth-order polynomial such that
ss^ ¼b þbmþbm2þbm3þbm4
i 1 2 3 4 5
wherem¼thestrikepriceminusthepriceoftheunderlyingstock.
Let’s create a VB.NET program to model a volatility smile using
Team-LRN

| 180     |     |      |     |     | IntroductiontoVB.NET |     |
| ------- | --- | ---- | --- | --- | -------------------- | --- |
| F I G U | R E | 10.3 |     |     |                      |     |
thisalgorithm.WehavealreadycreatedthismodelinExcel,which
can be found in the spreadsheet PolynomialForVol.xls on the CD.
| Step | 1 Open | a new | Windows | application | and name | it  |
| ---- | ------ | ----- | ------- | ----------- | -------- | --- |
PolynomialForVol.
| Step | 2 Add                                         | a reference    | to  | the MatrixMath.dll | file.         |     |
| ---- | --------------------------------------------- | -------------- | --- | ------------------ | ------------- | --- |
| Step | 3 AddasingletextboxtoForm1,andleavethedefault |                |     |                    |               |     |
|      | name,                                         | Textbox1.Text. |     | Also, change       | the Multiline |     |
propertyofTextbox1toTrue.Youshouldnowbeable
|         | to increase | the  | size | of Textbox1 | on your form. |     |
| ------- | ----------- | ---- | ---- | ----------- | ------------- | --- |
| F I G U | R E         | 10.4 |      |             |               |     |
Team-LRN

.NETTypeSystem 181
Step 4 Add the following code:
Imports MatrixMath
Public Class Form1
Inherits System.Windows.Forms.Form
Private Sub Form1_Load(ByVal sender As...) Handles MyBase.Load
Dim x As Integer
Dim AMatrix As Double(,) = New Double(6, 4) { }
Dim dblStrikes As Double() = New Double() _
{-15, -10, -5, 0, 5, 10, 15}
Dim dblVolatilities As Double() = New Double() _
{47, 35, 20, 17, 19, 21, 28}
Dim PolyParams As Double() = New Double(4) f g
For x = 0 To 6
AMatrix(x, 0) = 1
AMatrix(x, 1) = dblStrikes(x)
AMatrix(x, 2) = dblStrikes(x) ^ 2
AMatrix(x, 3) = dblStrikes(x) ^ 3
AMatrix(x, 4) = dblStrikes(x) ^ 4
Next x
PolyParams = Matrix.MultRegression(AMatrix, dblVolatilities)
TextBox1.Text = "Beta1: " & Format(PolyParams(0), "##.00000") _
& vbCrLf & "Beta2: " & Format(PolyParams(1), "##.00000") _
& vbCrLf & "Beta3: " & Format(PolyParams(2), "##.00000") _
& vbCrLf & "Beta4: " & Format(PolyParams(3), "##.00000") _
& vbCrLf & "Beta5: " & Format(PolyParams(4), "##.00000")
End Sub
End Class
Step 5 Run the program (see Figure 10.5).
F I G U R E 10.5
Team-LRN

| 182 |     |     |     | IntroductiontoVB.NET |     |
| --- | --- | --- | --- | -------------------- | --- |
SUMMARY
| In this | chapter we | examined in | some depth | the VB.NET | Type |
| ------- | ---------- | ----------- | ---------- | ---------- | ---- |
System to gain a greater understanding about types, assemblies,
namespaces,andinterfaces.Further,welookedathowtocreateour
own namespaces using the .NET Class Library template to create
Options.dll.Wedeterminedthatwecanadda.dllfiletoaprogram
| we create | by adding | a reference | to it and | using | an Imports |
| --------- | --------- | ----------- | --------- | ----- | ---------- |
statement.Wethenlookedatvolatilitysmilesandexploredhowto
| model them | using the | MatrixMath.dll | file. |     |     |
| ---------- | --------- | -------------- | ----- | --- | --- |
Team-LRN

.NETTypeSystem 183
PROBLEMS
| 1. What | are types?      |           |                           |
| ------- | --------------- | --------- | ------------------------- |
| 2. What | is a namespace? |           |                           |
| 3. What | is an assembly? |           |                           |
| 4. How  | do we add a     | reference | to a .dll file in VB.NET? |
| 5. What | is this Imports | statement | all about?                |
Team-LRN

184 IntroductiontoVB.NET
PROJECT 10.1
Createa.dllfileusingtheStockOption,PutOption,andCallOption
classesaddinginmethodstotheappropriateclassesfortheoption
Greeks. Also, create a simple Windows application to test out
your.dll.
PROJECT 10.2
Create a .dll file called Statistics.dll. Include in the class library
Public Shared methods for the four moments of a distribution—
mean,variance,skew,andkurtosis—aswellasanyotherstatistical
functionsyoumightwanttouseinthefuture.Again,makesureto
buildasimpleWindowsapplicationtotestthefunctionsinthe.dll
file.
Team-LRN

| S E C       | T I O       | N T         | H R E E        |                  |
| ----------- | ----------- | ----------- | -------------- | ---------------- |
| Database    |             | Programming |                |                  |
| Back        | Testing     |             |                |                  |
| In          | times of    | change,it   | isthe learners | who willinherit  |
| the         | earth while | the learned | willfind       | themselves       |
| beautifully |             | equippedfor | a world that   | no longerexists. |
EricHoffer
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

This page intentionally left blank.
Team-LRN

| C          | H A P | T E | R 11 |           |     |     |     |     |
| ---------- | ----- | --- | ---- | --------- | --- | --- | --- | --- |
| Relational |       |     |      | Databases |     |     |     |     |
F
| inancial | analysis |     | requires | data. | Furthermore, |     | when | doing |
| -------- | -------- | --- | -------- | ----- | ------------ | --- | ---- | ----- |
quantitative financial analysis, we often find that the data, such
as historical price or fundamental data, comes in a very simple
database structure such as a flat file, or worse, a spreadsheet. Flat
files are a primitive database design and often contain redundant
andinconsistentdata.Thosewhounderstandtheelementsofgood
databasedesigncertainlyavoidtheflat-filestructureforallbutthe
| simplest  | data, such | as  | historical | price | data.    |             |             |           |
| --------- | ---------- | --- | ---------- | ----- | -------- | ----------- | ----------- | --------- |
| Financial | analysts   |     | are almost |       | always   | experienced |             | in Excel. |
| And they  | should     | be. | Excel      | is    | the most | rapid       | development |           |
environment for building and testing financial models. But Excel
isnotarelationaldatabase,anditshouldnotbeusedassuch.Data
inExceliseasilycorrupted,andtoomuchdatainaspreadsheethas
| been knownto | overflowmemoryand |     |     |     | cause | crashes. | Furthermore, |     |
| ------------ | ----------------- | --- | --- | --- | ----- | -------- | ------------ | --- |
productionsystemsruninExcelalmostalwayssufferfromquality
problems. If you are collecting and/or analyzing data on financial
markets,wesuggestyouusetherighttoolforthejob—arelational
database.
| It is | difficult, | however, |     | to break | away | from | Mother | Excel. |
| ----- | ---------- | -------- | --- | -------- | ---- | ---- | ------ | ------ |
Using Excel, it’s easy to paint a range of returns, for example, and
passittothecovariancefunction.Beingabletoseethedataandthe
functioncallsisverycomforting.Ifweuseadatabase,however,we
cannot see it, and this can be somewhat scary. But fear not. In the
longrun,wearemuchbetteroff.Therearefarmoreadvantagesto
usingadatabasethandisadvantages.UsingdatabasesandVB.NET
| programsgivesusmuchmorecontroland |          |     |     |     |     | securitywhenbuilding |     |     |
| --------------------------------- | -------- | --- | --- | --- | --- | -------------------- | --- | --- |
| production                        | systems. |     |     |     |     |                      |     |     |
187
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

| 188               |     |                                         |     |     | DatabaseProgramming |     |     |
| ----------------- | --- | --------------------------------------- | --- | --- | ------------------- | --- | --- |
| VisualBasic.NETis |     | anefficientplatformforcreatingfinancial |     |     |                     |     |     |
applications that interact with data and databases. The front-end
applications insulate the user from the back-end complexities and
innerworkingsoftherelationaldatabasemanagementsystemand
| protect     | the data  | from accidental | alteration |        | or deletion. |          |           |
| ----------- | --------- | --------------- | ---------- | ------ | ------------ | -------- | --------- |
| Just        | remember, | in very         | general    | terms, | a            | database | stores    |
| information | and       | provides        | methods    | for    | managing     |          | the data, |
including methods to retrieve existing data, add new data, and
edit data. As in the case of a flat file, a database may be a very
simple construct, consisting of a single file. But as we grow in our
understandingofdatabases,wewillseethattheycanbecomevery
powerful, full-scale client-server relational database management
systems. So it is important that we learn how relational databases
workinordertoaccomplishmoreadvancedanalysis.Aswithother
topicsdiscussedinthisbook,wecannothopetocoverallthetopics
relatingtorelationaldatabases.Therearehundredsofbooksonthe
marketthatdealwiththistopicalone.Butwewillbeabletodiscuss
several relatively advanced topics and build three or four models
that demonstrate relational database design and connectivity as
| used in | quantitative | research. |     |     |     |     |     |
| ------- | ------------ | --------- | --- | --- | --- | --- | --- |
Let’s consider a financial markets example using a relational
database in the front office. On a trading desk, we may want to
attribute trading profits and losses to different factors so as to
assess the success of an automated trading system. But profit and
loss analysis and risk management require combining data in a
relationalwaywithhistoricaltradeandpricedataalongwithprofit
and loss information. This scenario requires the use of a relational
| database | management | system. |     |     |     |     |     |
| -------- | ---------- | ------- | --- | --- | --- | --- | --- |
In general there are two types of databases used in financial
markets: operational databases and analytical databases. Oper-
ationaldatabasesstoredynamicdatasuchasportfolioandposition
information.Analyticaldatabasesholdstaticdatasuchashistorical
price or trade history data, often in a flat file. Regardless of the
brand of database software, both these types of databases will be
managed using the relational database model (RDM) (Hernandez,
| 1997, p. | 3).      |         |                 |     |       |          |       |
| -------- | -------- | ------- | --------------- | --- | ----- | -------- | ----- |
| In       | the RDM, | data is | held in tables, |     | which | are made | up of |
columns, called fields, and rows, called records. Connections
Team-LRN

RelationalDatabases 189
between different tables are defined in relationships. These
relationshipsbetweentablesareestablishedthroughsharedfields.
The RDM has the advantage that, through its use of tables and
relationships between them, data integrity is ensured and
consistency and accuracy of data is guaranteed. Furthermore,
changes in the design of the database will not adversely affect the
VB.NETapplications that we build to access it (Hernandez, 1997,
p. 16).
Programs that we create in VB.NET can interact with
databases through a set of objects known as MS ActiveX Data
Objects(ADO)andaspecializedlanguagecalledStructuredQuery
Language (SQL). SQL enables us to talk to a database from a
VB.NET application. SQL is the industrywide standard for
interacting with databases for everything from simple data
retrieval, called queries, to modification and updating of data,
and even to database creation. Regardless of which relational
database management system you are using, SQL will be the
languageyouwillusetocarryonaconversationincode.Relational
database management systems (RDBMSs) are software appli-
cations for building, managing, and modifying relational data-
bases. The most popular large-scale RDBMSs are from Microsoft,
Oracle,andSybase.Thismaybealotofnewinformationifyouare
not familiar with databases, but don’t worry—in Chapters 12 and
13 we will look at ADO and SQL in greater depth.
In order to fully understand the RDM and the following
chaptersinthisbook,itisimperativethatyoubecomefamiliarwith
“database-speak,” the terms and phrases used in the database
industry. We have used some of the terms already—tables, columns,
rows, relationships. Over the next few pages, we will define and
briefly discuss some of the more important terms. Afterward, we
will look at the three databases included on the CD that will
illustrate most of these terms.
TABLES
A tableis theprimarystructurein arelational database.Itconsists
of columns and rows, often called fields and records. Tables
representitems,suchashistoricaldataforIBM,andevents,suchas
Team-LRN

| 190 |     |     |     | DatabaseProgramming |     |
| --- | --- | --- | --- | ------------------- | --- |
trades. Tables should then have names that describe the data they
hold, like IBMData, or just IBM, or OptionTrades. Further, tables
| can be either | data tables, | which | supply | information | such as |
| ------------- | ------------ | ----- | ------ | ----------- | ------- |
historical prices, or validation tables, which implement data
integrity. For example, we may have a table that contains a list of
| options’ expiration | dates. |     |     |     |     |
| ------------------- | ------ | --- | --- | --- | --- |
FIELDS
A field, or column, represents a characteristic of a record. For
| example, our | IBMData | table would | probably | have a | ClosePrice |
| ------------ | ------- | ----------- | -------- | ------ | ---------- |
field. Fields then have names, data types, and lengths. Data in
databasescanbealphanumeric,numeric,ordate/time.Also,fields
can contain distinct or multipart values and may have values that
are calculated.
RECORDS
Arecord,orrow,holdstheactualdatainatable.Asinglerecordin
atableismadeupofonerowcontainingallthecolumnsinthetable
including a primary key that uniquely identifies a record. So
January 21, 2003, identifies a unique record, or data point, of
IBMData. The full record contains the date, open, high, low, and
| closing prices | and the | volume. |     |     |     |
| -------------- | ------- | ------- | --- | --- | --- |
| PRIMARY        | KEYS    |         |     |     |     |
Primary keys are special fields that uniquely identify a record in a
table. So, as in the previous example, the Date field represents a
unique record in a table of historical prices. Every table in a
database must have a primary key, and no two tables should have
the same primary key. Primary keys ensure that each record in a
table is uniquely identifiable. Therefore, each element of the
| primary key     | field must | be unique  | and    | cannot be | null. So no |
| --------------- | ---------- | ---------- | ------ | --------- | ----------- |
| duplicate dates | would      | be allowed | in our | example.  |             |
Team-LRN

| RelationalDatabases |      |     |     |     |     | 191 |
| ------------------- | ---- | --- | --- | --- | --- | --- |
| FOREIGN             | KEYS |     |     |     |     |     |
Foreign keys establish relationships between pairs of tables.
| Relationships | between | two tables | arise | when | the primary | key |
| ------------- | ------- | ---------- | ----- | ---- | ----------- | --- |
column in one table is identical to the foreign key column in the
other. In a later example, we will see a graphic depiction of a
| relational | database showing | the | primary | and | foreign | keys for |
| ---------- | ---------------- | --- | ------- | --- | ------- | -------- |
different tables along with arrows representing the relationships
| between | them. |     |     |     |     |     |
| ------- | ----- | --- | --- | --- | --- | --- |
RELATIONSHIPS
As we have seen, relationships are connections between pairs of
tables,throughtheuseofprimaryandforeignkeys.Therearethree
differenttypesofrelationships:onetoone,onetomany,andmany
to many.
|     | One-to-One |     | Relationships |     |     |     |
| --- | ---------- | --- | ------------- | --- | --- | --- |
A relationship is said to be one to one if a single record in the first
tableisrelatedtoasinglerecordinthesecondtable,andviceversa.
|     | One-to-Many |     | Relationships |     |     |     |
| --- | ----------- | --- | ------------- | --- | --- | --- |
Arelationshipissaidtobeonetomanyifasinglerecordinthefirst
tablecanberelatedtoseveralrecordsinthesecondtable,butatthe
sametimeasinglerecordinthesecondtablecanonlyberelatedto
asinglerecordinthefirsttable.Itmayseemalittleconfusingright
| now, but | a later example | will make | this          | idea quite | clear. |     |
| -------- | --------------- | --------- | ------------- | ---------- | ------ | --- |
|          | Many-to-Many    |           | Relationships |            |        |     |
A relationship is said to be many to many if a single record in the
first table is related to many records in the second table, and vice
versa.Inthecaseofamany-to-manyrelationship,weneedtocreate
alinkingtablebycopyingtheprimarykeyfromeachtableintothe
new table. We suggest you find a good book on database design
beforeyouattempttobuildcomplexdatabasesthatincludemany-
| to-many | relationships. |     |     |     |     |     |
| ------- | -------------- | --- | --- | --- | --- | --- |
Team-LRN

| 192 |     |     |     | DatabaseProgramming |     |
| --- | --- | --- | --- | ------------------- | --- |
QUERIES
A query is an SQL statement used to retrieve rows of information
from one or more tables. Queries will often also contain search
criteria to limit the amount of data returned from the tables. For
example, we may create a query that retrieves the trade data only
| for the month | of March | 2001. |     |     |     |
| ------------- | -------- | ----- | --- | --- | --- |
SQLqueriesalsoallowustojointables.Joiningtablesenables
use of data from several tables in a relational database for a single
purpose.Forexample, we could display a single column from one
table or several columns from multiple tables in a single query.
| From this, | you may    | begin to see | the flexibility | and | power of |
| ---------- | ---------- | ------------ | --------------- | --- | -------- |
| relational | databases. |              |                 |     |          |
NORMALIZATION
Often you will hear database professionals talk about normal-
ization or normal forms. Normalization is the process of breaking
downalargetableortablesintosmallertablesinordertoeliminate
duplicationofdataandtopreventcertainproblemsthatcommonly
arisewithdatabaseinteraction.Anormalformisasetofrulesthat
test a table structure to ensure it is sound and free of errors. There
are at least five normal forms—first through fifth—used to test for
specific sets of problems. Tables we will use are in at least third
| normal     | form since   | each one has | a primary | key that | uniquely |
| ---------- | ------------ | ------------ | --------- | -------- | -------- |
| identifies | each record. |              |           |          |          |
| DATABASE   | DESIGN       |              |           |          |          |
Creating proprietary databases from scratch is no small task. It
necessitatesexaminationsofthebusinesspurposesofthedatabase
| as well | as the technical | means | to implement | them. | In short, |
| ------- | ---------------- | ----- | ------------ | ----- | --------- |
designing relational databases requires a process or methodology.
Doing so without one can lead to disaster. Again, several good
booksonrelationaldatabasedesignhavealreadybeenwritten,and
so we will quickly review the process. Michael Hernandez in his
bookDatabaseDesignforMereMortals(1997)outlinesaseven-phase
| process | for database | design: |     |     |     |
| ------- | ------------ | ------- | --- | --- | --- |
Team-LRN

RelationalDatabases 193
1. Definethepurposeofthedatabaseandthetasksthatusers
will perform against it.
2. Analyze current database solutions.
3. Createtables,fields,andprimarykeysthatcharacterizethe
subjects the database will track.
4. Determine the relationships that exist between tables.
5. Define the constraints or business rules for the data.
6. Develop ways to look at or view the data.
7. Review the integrity of the data, including checking the
fieldspecifications,testingthevalidityofrelationships,and
reviewing the business rules.
A well-designed database is easy to modify structurally,
allows for efficient retrieval of data, and makes it easy for devel-
operstobuildapplicationstoconnecttoit(Hernandez,1997,p.28).
ACCESS DATABASES
MS Access databases are relational databases supported by all
Microsoft Windows environments. You do not need to have MS
Access software installed on your computer to interface with
Access databases through VB.NET. In an Access database, all the
variouspartsofthedatabasearestoredinasinglefile,whichhasan
.mdb extension. The CD contains three Access databases—
Finance.mdb, DirtyFinance.mdb, and Options.mdb—that we will
use over the course of the remainder of the book. If you have MS
Accesssoftwareonyourcomputer,feelfreetoopenthesedatabases
in Accessand examine theirstructures.Let’s takea look at eachof
them.
The Finance.mdb Database
Finance.mdb is an MS Access database included on the CD with
thisbookthatusesflatfilestoholddailyhistoricalpricedatafor13
stocksandtheS&P500.TheindividualdatatablesinFinance.mdb
are named AXP, GE, GM, IBM, INTC, JNJ, KO, MCD, MO, MRK,
MSFT, SUNW, WMT, and SPX. In addition, there is a validation
table named Tickers, which contains the 13 stock ticker symbols
shown.
Team-LRN

194 DatabaseProgramming
The 14 data tables consist of the primarykey column, labeled
Date, and five other columns named OpenPrice, HighPrice,
LowPrice, ClosePrice, and Volume. Each table holds 12 years of
daily price data from January 2, 1990, to December 31, 2002. Table
11.1 is a sample of the IBM table showing the structure.
T A B L E 11.1
Date OpenPrice HighPrice LowPrice ClosePrice Volume
2-Jan-90 23.54 24.38 23.48 24.35 1760600
3-Jan-90 24.53 24.72 24.44 24.56 2369400
4-Jan-90 24.62 24.94 24.56 24.84 2423600
5-Jan-90 24.81 25.25 24.72 24.78 1893900
8-Jan-90 24.66 25.06 24.66 24.94 1159800
2-Jan-90 23.54 24.38 23.48 24.35 1760600
TheTickersvalidationtableconsistsofasinglecolumnnamed
Symbols, which holds the ticker symbols for each of the 13 stocks.
Table 11.2 is a sample of the Tickers table.
T A B L E 11.2
Symbols
AXP
GE
GM
IBM
We have made every attempt to ensure that the data in the
Finance.mdbdatabaseiscleanandfreefromerrors.Thisisnotthe
case with the DirtyFinance.mdb database.
The DirtyFinance.mdb Database
The DirtyFinance.mdb Access database included on the CD
purposely contains dirty data. It is identical in every way
Team-LRN

| RelationalDatabases |     |     |     |     |     |     |     |     | 195 |
| ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
structurallytotheFinance.mdbdata.Theonlydifferenceisthatwe
have gone through and corrupted the data using all kinds of sly
| and malicious |     | techniques. |     | But the | errors | we  | have | created | are |
| ------------- | --- | ----------- | --- | ------- | ------ | --- | ---- | ------- | --- |
typicalofthoseyouwillencounterinrealdatapurchasedfromdata
| vendors.        | In Chapter |             | 14 it | will be  | your     | job     | to build   | a VB.NET |     |
| --------------- | ---------- | ----------- | ----- | -------- | -------- | ------- | ---------- | -------- | --- |
| program         | that finds | the         | dirty | data     | and to   | cleanse | it.        |          |     |
|                 | The        | Options.mdb |       |          | Database |         |            |          |     |
| The Options.mdb |            | Access      |       | database | uses     | a       | relational | database |     |
structure to hold information about stocks and options as well as
stock trades and option trades. In fact, there are four tables in the
Options.mdb database representing each of these things—Stocks,
| OptionContracts, |     | StockTrades, |     | and | OptionTrades. |     |     | As we | saw |
| ---------------- | --- | ------------ | --- | --- | ------------- | --- | --- | ----- | --- |
earlier,therelationshipsbetweentwotablesinarelationaldatabase
| are made | possible |     | by common |     | primary | and | foreign | keys. | In  |
| -------- | -------- | --- | --------- | --- | ------- | --- | ------- | ----- | --- |
Options.mdb, for example, the Stock and StockTrades tables are
related through a StockSymbol primary key in the Stock table and
| the foreign | key        | StockSymbol |           | column |           | in the | StockTrades        |     | table. |
| ----------- | ---------- | ----------- | --------- | ------ | --------- | ------ | ------------------ | --- | ------ |
| Figure      | 11.1 shows | the         | structure |        | or schema |        | of the Options.mdb |     |        |
database. In this diagram, the relationships are represented by
arrows.
| All | the relationships |     | in  | the Options.mdb |     |     | database | are | one to |
| --- | ----------------- | --- | --- | --------------- | --- | --- | -------- | --- | ------ |
many. As you may be able to gather from the diagram, a one-to-
many relationship exists between the Stock and OptionContracts
tables.Clearly,asinglestockcanhavemanyoptionscontractsonit.
But in the opposite direction, it is not the same. A single option
contract can have only one underlying stock associated with it.
| Earlier | in  | the chapter, |     | we briefly | described |     | a many-to-many |     |     |
| ------- | --- | ------------ | --- | ---------- | --------- | --- | -------------- | --- | --- |
relationship between two tables. Although not represented in the
Options.mdb diagram, let’s consider a quick example. A single
optioncontractmaybeinvolvedinmanytrades,butanindividual
tradecouldhavemorethanoneoptioncontractassociatedwithitif
we assume spreads are included in a SpreadTrades table. In this
way, a single option contract could be related to several spread
trades,andasinglespreadtradecouldberelatedtoseveraloption
contracts.
Team-LRN

| 196   |            |     | DatabaseProgramming |
| ----- | ---------- | --- | ------------------- |
| F I G | U R E 11.1 |     |                     |
SUMMARY
| When doing | financial   | modeling and certainly | when building       |
| ---------- | ----------- | ---------------------- | ------------------- |
| production | trading and | risk management        | systems, relational |
databasesaresuperiortoExcelasawaytostoreandmanagedata.
Team-LRN

| RelationalDatabases |     |     |     | 197 |
| ------------------- | --- | --- | --- | --- |
The databasefield has its own language that we must learn before
we canbegin creatingdatabasesand interacting withthem.In this
| chapter, we | looked | at and defined | several database | terms. |
| ----------- | ------ | -------------- | ---------------- | ------ |
Furthermore, creating new relational databases necessitates the
use of a design methodology. We very briefly reviewed the seven
| steps of a | well-known | methodology. |     |     |
| ---------- | ---------- | ------------ | --- | --- |
TherearethreeAccessdatabasesincludedontheCDwiththis
book—Finance.mdb,DirtyFinance.mdb,andOptions.mdb.Wewill
be building VB.NET Windows applications in later chapters that
access them.
Team-LRN

| 198 |     |     | DatabaseProgramming |     |
| --- | --- | --- | ------------------- | --- |
PROBLEMS
| 1. What     | are operational | and analytical | databases? |     |
| ----------- | --------------- | -------------- | ---------- | --- |
| 2. What     | is SQL?         |                |            |     |
| 3. Describe | tables, rows,   | and columns.   |            |     |
4. Whatarerelationshipsandhowaretheycreated?Describe
| the three | types of       | relationships. |           |              |
| --------- | -------------- | -------------- | --------- | ------------ |
| 5. What   | is the process | to go through  | to design | a relational |
database?
Team-LRN

| RelationalDatabases |      |     |     |     |     |     | 199 |
| ------------------- | ---- | --- | --- | --- | --- | --- | --- |
| PROJECT             | 11.1 |     |     |     |     |     |     |
AssumingyouhaveMSAccess,createasimplerelationaldatabase
called Futures.mdb in MS Access. This database should consist of
two tables named Futures and FuturesTrades. The Futures table
should have columns named FuturesSymbol, Expiration, Bid, and
| Ask. The | FuturesTrades |            | table | should         | have | columns   | named |
| -------- | ------------- | ---------- | ----- | -------------- | ---- | --------- | ----- |
| TradeID, | TradeDate,    | TradeTime, |       | FuturesSymbol, |      | Quantity, | and   |
Price.
| In  | Access,opena | blankAccessdatabase. |     |     | Next,under |     | Objects |
| --- | ------------ | -------------------- | --- | --- | ---------- | --- | ------- |
clickonTablesandthenonNew.InDesignView,enterthecolumn
namesfortheFuturestable.OntheFuturesSymbolfield,right-click
| and selectPrimary |          | Key. | Close the | DesignView | windowand |     | name |
| ----------------- | -------- | ---- | --------- | ---------- | --------- | --- | ---- |
| this table        | Futures. |      |           |            |           |     |      |
| F I G             | U R E    | 11.2 |           |            |           |     |      |
Team-LRN

| 200  |       |        |        |           | DatabaseProgramming |     |        |
| ---- | ----- | ------ | ------ | --------- | ------------------- | --- | ------ |
| Next | click | on New | again. | In Design | View, enter         | the | column |
namesfortheFuturesTradestable.SetTradeIDastheprimarykey.
ClosetheDesignViewwindowandnamethistableFuturesTrades.
| Under    | the     | Tools | menu          | bar item, | select Relationships. |     | Add |
| -------- | ------- | ----- | ------------- | --------- | --------------------- | --- | --- |
| both the | Futures | and   | FuturesTrades |           | tables.               |     |     |
Onthemenubar,selectRelationshipsandEditRelationships.
| In the Edit | Relationships |     | window, |     | click on Create | New. | Add a |
| ----------- | ------------- | --- | ------- | --- | --------------- | ---- | ----- |
relationship between the FuturesSymbol field in the Futures table
andtheFuturesSymbolfieldintheFuturesTradestableasshownin
Figure 11.2.
| Back | in the | Edit | Relationships |     | window, click | on  | Enforce |
| ---- | ------ | ---- | ------------- | --- | ------------- | --- | ------- |
Referential Integrity and Create. You should now see the one-to-
| many relationship |            | shown  |      | graphically  | in the  | Relationships |     |
| ----------------- | ---------- | ------ | ---- | ------------ | ------- | ------------- | --- |
| window—see        | Figure     | 11.3.  |      |              |         |               |     |
| Now               | try        | adding | some | hypothetical | data to | the tables    | by  |
| opening           | the table. |        |      |              |         |               |     |
| F I G             | U R E      | 11.3   |      |              |         |               |     |
| PROJECT           | 11.2       |        |      |              |         |               |     |
Designarelationaldatabasetoholdbondtradingdataandcreateit
in MS Access. Your database should contain at least two tables
| related to | each | other in | a one-to-many |     | way. |     |     |
| ---------- | ---- | -------- | ------------- | --- | ---- | --- | --- |
Team-LRN

| C H | A P T E | R 12 |     |     |     |     |     |
| --- | ------- | ---- | --- | --- | --- | --- | --- |
ADO.NET
A
| DO.NET   | is an application |     | programming |             |     | interface used | to    |
| -------- | ----------------- | --- | ----------- | ----------- | --- | -------------- | ----- |
| interact | with databases    | in  | VB.NET      | programming |     | code           | using |
ActiveXDataObjects(ADO).ADOisaproprietarysetofMicrosoft
objectsthatallowsdeveloperstoaccessrelationalandnonrelational
databases,includingMSAccess,Sybase,MSSQLServer,Informix,
and Oracle among others. So if we need to write a program that
providesaconnectiontoadatabase,wecanuseADOobjectsinour
application to perform database transactions. These objects are
| found in           | the data and | XML namespaces,                         |     |             | as for | example: |     |
| ------------------ | ------------ | --------------------------------------- | --- | ----------- | ------ | -------- | --- |
| Namespace          |              |                                         |     | Description |        |          |     |
| System.Data        |              | ADO.NETclasses,includingtheDataSetclass |     |             |        |          |     |
| System.Data.Common |              | Classesfordatabaseaccess                |     |             |        |          |     |
System.Data.OleDb ClassesforconnectiontoOleDb-compatibledatabases
System.Data.SqlClient ClassesforconnectiontoSQLServer7.0databases
| System.Data.SqlTypes |         | ClassesforSQLServer7.0datatypes        |     |         |      |        |          |
| -------------------- | ------- | -------------------------------------- | --- | ------- | ---- | ------ | -------- |
| System.XML           |         | ClassesforXMLmessagecreationandparsing |     |         |      |        |          |
| ADO.NET              | is part | of Microsoft’s                         |     | overall | data | access | strategy |
foruniversaldataaccess,whichattemptstopermitconnectivityto
the vast array of existing and future data sources. In order for
universal data access to work, Microsoft and several database
| companies | provide | interfaces | between |     | their | databases | and |
| --------- | ------- | ---------- | ------- | --- | ----- | --------- | --- |
Microsoft’s OleDb objects. OleDb (Object Linking and Embedding
Databases)objectsenableconnectiontojustaboutanydatasource,
whereas SqlClient objects enable optimized interaction with MS
SQLServerdatabases.Furthermore,ADOsupportstheuseofdata-
aware components, such as DataGrids in Visual Basic.NET, which
201
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

202 DatabaseProgramming
allow us to see the data from the database. So we can, if need be,
look at the data in a running Windows application.
ADO is a complex technology, and mastering it can take a
tremendousamountofeffort.Infact,severalgoodbookshavebeen
writtenaboutthissubjectalone.Theremainderofthischapterwill
focusonadiscussionoftheADO.NETclassesandtheiruses,which
enable us to open a connection to a data source, get data from it,
and put the data into an in-memory cache of records called a
DataSet. Then we can close the connection to the database. In a
nutshell, ADO allows us to connect to and disconnect from a
database,getdatafromadatabase,andviewandmanipulatedata,
including making changes to the data itself.
The model just mentioned is the one we will use in all
examples in this chapter. But there is another model. The
alternativeistoperformoperationsorcalculationsonthedatabase
directly using a data command object, OleDbCommand, with an
SQLstatement.Directdatabaseinteractioninthismannerusesless
overhead since it bypasses storage of data in a data set, which of
course requires memory. We will examine briefly this alternative
model in the following chapter.
The main advantage of the DataSet model, though, is that
DataSetallowsustoworkwithmultipletables,frommultipledata
sources such as databases, Excel spreadsheets, or XML files, and
use them in multiple applications. The long and the short of it is
that the advantages of the DataSet methodology outweigh the
disadvantage of increased memory usage.
The following sections will introduce you to some ADO
objects that have evolved since previous versions of Visual Basic
and some that are new.
CONNECTIONS
To interact with a database, we first need to establish a persistent
connection to it. A persistent connection is one that will stay open
until it is explicitly closed. VB.NETsupports many different types
of connection classes in the OleDb and SqlClient namespaces. We
will use the OleDbConnection class.
Team-LRN

| ADO.NET |     |     |     |     |     |     | 203 |
| ------- | --- | --- | --- | --- | --- | --- | --- |
DATAADAPTER
A DataAdapter is the object that communicates with the database
via an SQL statement to get data and put it in something called a
DataSet. Then, if need be, the DataAdaptercan send updateddata
| back to | the database | to make | changes | in  | the data, | based | on  |
| ------- | ------------ | ------- | ------- | --- | --------- | ----- | --- |
operations performed while the DataSet held the data. In an effort
to make multitiered applications more efficient, data processing is
turningtoamessage-basedapproachthatrevolvesaroundchunks
of information. At the center of this approach is the DataAdapter,
whichactsasaconduittogetandsenddatabetweenaDataSetand
| a database.       | It accomplishes                   | this     | by means    |           | of SQL  | queries    | and     |
| ----------------- | --------------------------------- | -------- | ----------- | --------- | ------- | ---------- | ------- |
| commands          | made against                      | the      | database.   | In        | Chapter | 13         | we will |
| discuss           | SQL in depth.                     | Here are | the         | important |         | properties | and     |
| methods           | of the OleDbDataAdapter           |          | class,      | which     | we      | will use:  |         |
| PublicConstructor |                                   |          | Description |           |         |            |         |
| New()             | Initializesanewinstanceoftheclass |          |             |           |         |            |         |
| PublicProperties  |                                   |          | Description |           |         |            |         |
DeleteCommand GetsorsetsanSQLstatementfordeletingrecordsfromthe
database
InsertCommand GetsorsetsanSQLstatementusedtoinsertnewrecordsinto
thedatabase
SelectCommand GetsorsetsanSQLstatementusedtoselectrecordsinthe
database
UpdateCommand GetsorsetsanSQLstatementusedtoupdaterecordsinthe
database
| PublicMethods |                                                |     | Description |     |     |     |     |
| ------------- | ---------------------------------------------- | --- | ----------- | --- | --- | --- | --- |
| Fill          | AddsrowsfromadatasourcetoaspecifiedDataSet     |     |             |     |     |     |     |
| FillSchema    | AddsaDataTabletoaDataSetsothattheschemamatches |     |             |     |     |     |     |
schemaofthedatasource
| Update | CallstheINSERT,UPDATE,orDELETEstatementsforeachrow |     |     |     |     |     |     |
| ------ | -------------------------------------------------- | --- | --- | --- | --- | --- | --- |
intheDataSet
DATASET
| A DataSet | can be thought | of  | as in-memory |     | representation |     | of a |
| --------- | -------------- | --- | ------------ | --- | -------------- | --- | ---- |
relational database, complete with tables, columns, rows, and
relations. DataSets can be used then for storing, remoting, and
Team-LRN

| 204 |     |     |     |     | DatabaseProgramming |     |
| --- | --- | --- | --- | --- | ------------------- | --- |
programmingagainstflat,XML,andrelationaldata.Theimportant
distinction between this evolved stage of ADO.NETand previous
Microsoft data architectures is that a DataSet is separate and
distinct from any data sources. For this reason, DataSet functions
are stand-alone entities that know nothing about the source or
destination of the data within it. The DataSet does not interact
| directly | with | the database | and is only | a cache | of data, | with |
| -------- | ---- | ------------ | ----------- | ------- | -------- | ---- |
database-like structures such as tables, columns, and relationships
withinit.Thisallowsustoworkwithaprogrammingmodelthatis
alwaysconsistent,regardlessofwherethesourcedataresides.Data
comingfromadatabase,anXMLfile,code,oruserinputcanallbe
placed into a DataSet object. Then as changes are made to the
DataSet, they can be tracked and verified before updating the
sourcedata.ThisDataSetisthenusedbyaDataAdaptertoupdate
| the original | data    | source. |             |         |            |     |
| ------------ | ------- | ------- | ----------- | ------- | ---------- | --- |
| The          | DataSet | class,  | the related | Columns | collection | of  |
DataColumns, the Rows collection of DataRows, and Constraints
| classes           | are all | defined in                                         | the System.Data   | namespace.  |         |        |
| ----------------- | ------- | -------------------------------------------------- | ----------------- | ----------- | ------- | ------ |
| Here              | are     | the important                                      | public properties | and         | methods | of the |
| DataSet           | class:  |                                                    |                   |             |         |        |
| PublicConstructor |         |                                                    |                   | Description |         |        |
| New               |         | Initializesaninstanceoftheclass                    |                   |             |         |        |
| PublicProperties  |         |                                                    |                   | Description |         |        |
| HasErrors         |         | Indicateswhetherthereareerrorsinanyoftherecords,or |                   |             |         |        |
rows,oftheDataSet
| Tables         |     | GetsthecollectionoftableswithintheDataSet    |     |             |     |     |
| -------------- | --- | -------------------------------------------- | --- | ----------- | --- | --- |
| PublicMethods  |     |                                              |     | Description |     |     |
| Clear          |     | ClearsalldatafromtheDataSet                  |     |             |     |     |
| Clone          |     | CopiesthestructureoftheDataSet,butnotthedata |     |             |     |     |
| Copy           |     | CopiesthestructureandthedataoftheDataSet     |     |             |     |     |
| GetChanges     |     | CreatesasecondDataSetthatcontainsthechanges  |     |             |     |     |
| GetXML         |     | GetsanXMLrepresentationoftheDataSet          |     |             |     |     |
| Merge          |     | MergestheDataSetwithanotherDataSet           |     |             |     |     |
| ReadXML        |     | ReadsdataandschemafromXMLintotheDataSet      |     |             |     |     |
| ReadXMLSchema  |     | ReadsanXMLschemaintheDataSet                 |     |             |     |     |
| Reset          |     | ResetstheDataSettoitsoriginalstate           |     |             |     |     |
| WriteXML       |     | WritesXMLdatafromtheDataSet                  |     |             |     |     |
| WriteXMLschema |     | WritestheXMLschemafromtheDataSet             |     |             |     |     |
Team-LRN

| ADO.NET  |          |     |           |     |              |     | 205        |
| -------- | -------- | --- | --------- | --- | ------------ | --- | ---------- |
| DataSets | are made | up  | primarily | of  | a collection | of  | DataTables |
andDataRelations.DataTablesareinturnmadeupofcollectionsof
columns,rows,andconstraints.Actualdataisthencontainedinthe
Rows collection of DataRow objects. As in a relational database,
constraints maintainthe data,entity,and relationalintegrity of the
data through the ForeignKeyConstraints, the UniqueConstraints,
| and the | PrimaryKey. | The | DataRelation |     | collection |     | acts as an |
| ------- | ----------- | --- | ------------ | --- | ---------- | --- | ---------- |
interface between related rows in different tables, as shown here:
DataSetObject
9
DataTablecollection
>>>>>>>>=
|     | Co lu m n s ( D         | at a ColumnCollection) |     |     |                        |     |     |
| --- | ----------------------- | ---------------------- | --- | --- | ---------------------- | --- | --- |
|     | D a ta C o l um         | n s                    |     |     |                        |     |     |
|     | Rows(DataRowCollection) |                        |     |     | DataRelationcollection |     |     |
>>>>>>>>;
D a t a R o w s
Co n s t ra in t s
Constraint
As we describe the pieces of the DataSet puzzle, we will also
showyouthecodesnippetstobuildaDataSetwithaDataTable.In
more situations than not, the DataAdapter will do these things
| automatically, | but | an  | understanding |     | of how | a   | DataSet is |
| -------------- | --- | --- | ------------- | --- | ------ | --- | ---------- |
constructed is absolutely necessary to higher-level programming.
| Step | 1 Create        | a          | new Windows |        | application |       | named      |
| ---- | --------------- | ---------- | ----------- | ------ | ----------- | ----- | ---------- |
|      | DataSetExample. |            | On          | the    | form, place | a     | label. All |
|      | the code        |            | we add      | to the | program     | will  | be in the  |
|      | Form1_Load      |            | event.      | Add    | the code    | shown | here to    |
|      | create          | a DataSet: |             |        |             |       |            |
Private Sub Form1_Load(ByVal sender As ...)Handles MyBase.Load
|         | Dim   | myDataSet | As New  | DataSet()   |     |     |     |
| ------- | ----- | --------- | ------- | ----------- | --- | --- | --- |
|         | ‘ Add | new       | code in | here later. |     |     |     |
| End Sub |       |           |         |             |     |     |     |
DATATABLE
BecauseDataTablesactuallyholdthedatainaDataSet,DataTables
| are the main | topic | in any | discussion | of  | ADO.NET. | A   | DataTable |
| ------------ | ----- | ------ | ---------- | --- | -------- | --- | --------- |
holds a Columns collection, which defines the table’s schema; a
Rows collection, which contains the records in DataRow objects;
Team-LRN

| 206 |     |     | DatabaseProgramming |     |
| --- | --- | --- | ------------------- | --- |
and Constraints, which ensure the integrity of the data along with
| the PrimaryKey | of the DataTable. | We  | can add a | DataTable to a |
| -------------- | ----------------- | --- | --------- | -------------- |
DataSet’s collection of tables using the overloaded Add method:
| PublicMethods           |               |                                        | Description  |             |
| ----------------------- | ------------- | -------------------------------------- | ------------ | ----------- |
| Tables.Add              |               | CreatesaDataTableintheDataSet          |              |             |
| Tables.Add(myName)      |               | CreatesaDataTableintheDataSetwithaname |              |             |
| Tables.Add(myDataTable) |               | AddsaDataTabletotheDataSet             |              |             |
| Here are                | the important | properties,                            | methods, and | events of a |
DataTable:
| PublicConstructor |                              |     | Description |     |
| ----------------- | ---------------------------- | --- | ----------- | --- |
| New               | CreatesaDataTable            |     |             |     |
| New(TableName)    | CreatesaDataTablewiththename |     |             |     |
| PublicProperties  |                              |     | Description |     |
Columns ReturnsareferencetotheDataColumnCollection,acollectionof
DataColumnobjects
| Constraints | TheConstraintscollection             |     |     |     |
| ----------- | ------------------------------------ | --- | --- | --- |
| DataSet     | TheDataSettowhichtheDataTablebelongs |     |     |     |
HasErrors IndicateswhetherthereareerrorsinanyoftheDataTable’s
DataRows
| PrimaryKey | TheprimarykeyoftheDataTable                           |     |     |     |
| ---------- | ----------------------------------------------------- | --- | --- | --- |
| Rows       | ReturnsareferencetotheDataRowCollection,acollectionof |     |     |     |
DataRowobjects
| TableName     | ThenameoftheDataTablewithintheDataSet                |     |             |     |
| ------------- | ---------------------------------------------------- | --- | ----------- | --- |
| PublicMethods |                                                      |     | Description |     |
| AcceptChanges | ChangesalltheDataRows                                |     |             |     |
| Clear         | DeletesallDataRowobjectsfromtheDataTable             |     |             |     |
| Clone         | CopiestheschemaoftheDataTable,butnotthedata          |     |             |     |
| Compute       | PerformsanoperationontheDataTable                    |     |             |     |
| Copy          | CopiestheschemaandthedataoftheDataTable              |     |             |     |
| ImportRow     | CopiesaDataRowintoaDataTable                         |     |             |     |
| NewRow        | CreatesarowwiththeschemaoftheDataTableasdefinedbythe |     |             |     |
DataColumnCollection
| Select | ReturnsanarrayofDataRowobjectsthatmatchaspecified |     |     |     |
| ------ | ------------------------------------------------- | --- | --- | --- |
criterion
| PublicEvents  |                                     |     | Description |     |
| ------------- | ----------------------------------- | --- | ----------- | --- |
| ColumnChanged | FiresafteraDataColumnhasbeenchanged |     |             |     |
| RowChanged    | FiresafteraDataRowhasbeenchanged    |     |             |     |
| RowDeleted    | FiresafteraDataRowhasbeendeleted    |     |             |     |
Team-LRN

| ADO.NET |         |        |             |     |                          |               |          | 207 |
| ------- | ------- | ------ | ----------- | --- | ------------------------ | ------------- | -------- | --- |
| Step    | 2 Let’s | create | a DataTable |     | and                      | add it to the | DataSet. |     |
|         |         | Dim    | dtIBMdata   | As  | New DataTable("IBMdata") |               |          |     |
myDataSet.Tables.Add(dtIBMdata)
| COLUMNS, |     | DATACOLUMNCOLLECTIONS, |     |     |     |     |     |     |
| -------- | --- | ---------------------- | --- | --- | --- | --- | --- | --- |
AND DATACOLUMNS
| The DataTable’s       |     | Columns |     | property | returns | a reference |            | to a |
| --------------------- | --- | ------- | --- | -------- | ------- | ----------- | ---------- | ---- |
| DataColumnCollection, |     |         | an  | object   | that    | holds a     | collection | of   |
DataColumn objects and defines the schema of the table. Usually
the DataColumnCollection is defined automatically by a DataA-
| dapter’s | Fillmethod,and |     | we  | can thenaccessthe |     | DataColumnCol- |     |     |
| -------- | -------------- | --- | --- | ----------------- | --- | -------------- | --- | --- |
lection through the DataTable’s Columns property. Because the
DataColumnCollection inherits from the CollectionBase class, it
uses the Add, Remove, Item, and Count methods to (respectively)
insert, delete, get a specified DataColumn from, and count the
number of DataColumn objects within it. As we will see, in some
| cases we    | may     | want       | to define  | the | schema       | ourselves | using        | the |
| ----------- | ------- | ---------- | ---------- | --- | ------------ | --------- | ------------ | --- |
| DataTable’s | Columns |            | properties |     | and methods. | We        | will discuss |     |
| Collection  | objects | in greater | detail     |     | in Chapter   | 14.       |              |     |
WecanaddDataColumnstotheDataColumnCollectionusing
| the Columns.Add         |     | method                                  | as         | follows: |                             |              |     |     |
| ----------------------- | --- | --------------------------------------- | ---------- | -------- | --------------------------- | ------------ | --- | --- |
| PublicMethod            |     |                                         |            |          | Description                 |              |     |     |
| Columns.Add(DataColumn) |     |                                         |            |          | AddsaDataColumntoaDataTable |              |     |     |
| Here                    | are | the important                           | properties |          | of                          | DataColumns: |     |     |
| PublicProperties        |     |                                         |            |          | Description                 |              |     |     |
| New                     |     | CreatesaDataColumn                      |            |          |                             |              |     |     |
| New(ColumnName)         |     | CreatesaDataColumnwithaname             |            |          |                             |              |     |     |
| New(ColumnName,         |     | CreatesaDataColumnwithanameandadatatype |            |          |                             |              |     |     |
DataType)
| PublicProperties |     |                                   |     |     | Description |     |     |     |
| ---------------- | --- | --------------------------------- | --- | --- | ----------- | --- | --- | --- |
| AllowDbNull      |     | Specifieswhetheracolumncanbeempty |     |     |             |     |     |     |
AutoIncrement Specifieswhetherthesystemwillincrementthevalueofthe
columnautomatically
Team-LRN

| 208              |     |                                              |             | DatabaseProgramming |     |
| ---------------- | --- | -------------------------------------------- | ----------- | ------------------- | --- |
| PublicProperties |     |                                              | Description |                     |     |
| Caption          |     | ThenameofthecolumnifdifferentfromColumnName  |             |                     |     |
| ColumnName       |     | Thenameofthecolumn                           |             |                     |     |
| DataType         |     | ThetypeofdatatheDataColumncanhold            |             |                     |     |
| DefaultValue     |     | ThedefaultvalueofelementsintheDataColumn     |             |                     |     |
| ReadOnly         |     | SpecifieswhetherelementsintheDataColumncanbe |             |                     |     |
changed
| Unique |     | SpecifieswhethereachelementintheDataColumnmustbe |     |     |     |
| ------ | --- | ------------------------------------------------ | --- | --- | --- |
unique
| Step | 3 Let’s | create a DataColumn | and | add it | to the |
| ---- | ------- | ------------------- | --- | ------ | ------ |
DataTable.
|     |     | Dim colClose = New | DataColumn("ClosePrice") |     |     |
| --- | --- | ------------------ | ------------------------ | --- | --- |
dtIBMdata.Columns.Add(colClose)
| ROWS, | DATAROWCOLLECTIONS, |     |     |     |     |
| ----- | ------------------- | --- | --- | --- | --- |
AND DATAROWS
| The Rows | property | of a DataTable | returns | a reference | to a |
| -------- | -------- | -------------- | ------- | ----------- | ---- |
DataRowCollection,acollectionthatcontainsthedatainDataRow
objects. Because the DataRowCollection inherits from the Collec-
tion class, it uses the Add, Remove, Item, and Count methods to
(respectively) insert, delete, get a specified DataRow from, and
count the numberof DataColumn objects within it. So we can add
DataRows to the DataTable through the Rows property using the
| Rows.Add          | methods | as follows:              |             |     |     |
| ----------------- | ------- | ------------------------ | ----------- | --- | --- |
| PublicMethods     |         |                          | Description |     |     |
| Rows.Add(DataRow) |         | AddsaDataRowtoaDataTable |             |     |     |
Rows.Add(datavalues()) AddsaDataRowtoaDataTableandsetstherespective
DataColumnvaluesaccordingtothedatavaluesarray
HerearetheimportantpropertiesandmethodsofaDataRow
object:
| PublicProperties |     |                                                   | Description |     |     |
| ---------------- | --- | ------------------------------------------------- | ----------- | --- | --- |
| HasErrors        |     | IndicateswhetherthereareerrorsintheDataRow        |             |     |     |
| Item             |     | SpecifiesaDataColumnwithintheDataRow              |             |     |     |
| ItemArray        |     | AnarrayofallthevaluesoftheDataColumnsintheDataRow |             |     |     |
| Table            |     | TheDataTabletowhichtheDataRowbelongs              |             |     |     |
Team-LRN

| ADO.NET       |                                                |             |     | 209 |
| ------------- | ---------------------------------------------- | ----------- | --- | --- |
| PublicMethods |                                                | Description |     |     |
| AcceptChanges | MakesallchangestoaDataRow                      |             |     |     |
| BeginEdit     | Startsaneditingoperation                       |             |     |     |
| CancelEdit    | Stopsaneditingoperation                        |             |     |     |
| Delete        | DeletesaDataRow                                |             |     |     |
| EndEdit       | Finishesaneditingoperation                     |             |     |     |
| IsNull        | SpecifieswhetheraDataColumnwithintheDataRowhas |             |     |     |
anullvalue
| Step 4 | Now let’s create | a DataRow | and add | it to the |
| ------ | ---------------- | --------- | ------- | --------- |
DataTable.
|     | Dim rowData | As DataRow | = dtIBMdata.NewRow() |     |
| --- | ----------- | ---------- | -------------------- | --- |
dtIBMdata.Rows.Add(rowData)
Wecandefinethevalueofthis“cell”oranyother“cell”inthe
| table this way:                      |     |     |         |     |
| ------------------------------------ | --- | --- | ------- | --- |
| dtIBMdata.Rows(0).Item("ClosePrice") |     |     | = 65.34 |     |
InthecasewheretheDataTableiscreatedbytheDataAdapter,
| we can reference | a specific | cell this way: |     |     |
| ---------------- | ---------- | -------------- | --- | --- |
Label1.Text = myDataSet.Tables("IBMdata").Rows(0).Item("ClosePrice")
| See Figure 12.1. |        |     |     |     |
| ---------------- | ------ | --- | --- | --- |
| F I G U R        | E 12.1 |     |     |     |
Team-LRN

210 DatabaseProgramming
CONNECTING TO A DATABASE
Asmentionedearlier,forthepurposesofthisbook,wewillusean
OleDbConnection to interface with databases. The System.Data.
OleDb namespace contains several classes we can use to access
OleDb-compatible data sources, such as MS Access databases.
To connect to a database, we will use an OleDbConnection
object, which represents a unique connection to a data source. An
instance of this class specifies the connection provider and the
name and path of the database to which our application will
connect.
We will use the OleDbDataAdapter class to hold an SQL
statementandtheconnectionuponwhichitwillbeexecuted.After
we have declared an OleDbDataAdapter object, we can create a
DataSet object in which to place the data the DataAdapter returns
to us. Unlike the DataSet example shown previously, we will not
have to construct the DataSet’s DataTable ourselves. Rather, the
DataAdapter will create the DataSet’s schema for us.
Step 1 The database to which we will connect will be the
Finance.mdb MS Access database, which can be
found on the CD. Create a copy of the Finance.mdb
databaseintheModelingFMfolderonyourC:\drive
so that the absolute path to the database is
C:\ModelingFM\Finance.mdb.
Step 2 In VB.NET, open a new Windows application called
ADOExample.
Step 3 On your Form1, add a Button, a Label, and a
DataGrid. You can leave the names to their defaults.
Step 4 In the Form1 code window, all the way at the top,
abovethelineofcodethatreadsPublicClassForm1,
type the statement:
Imports System.Data.OleDb
Step 5 In the Button1_Click event, add the following code:
Private Sub Button1_Click(ByVal sender As ...) Handles Button1.Click
Dim myConnect As New OleDbConnection("Provider=Microsoft.Jet _
.OLEDB.4.0;Data Source=C:\ModelingFM\Finance.mdb")
Dim myAdapter As New OleDbDataAdapter("select * from AXP", myConnect)
Dim myDataSet As New DataSet()
myConnect.Open()
Team-LRN

| ADO.NET                   |     |     |            |     |     |     | 211 |
| ------------------------- | --- | --- | ---------- | --- | --- | --- | --- |
| myAdapter.Fill(myDataSet, |     |     | "AXPdata") |     |     |     |     |
myConnect.Close()
| DataGrid1.DataSource |     | = myDataSet |     |     |     |     |     |
| -------------------- | --- | ----------- | --- | --- | --- | --- | --- |
| DataGrid1.DataMember |     | = "AXPdata" |     |     |     |     |     |
Label1.Text = myDataSet.Tables("AXPdata").Rows(0).Item("ClosePrice")
End Sub
| Step            | 6     |              |          |           |        |                    |     |
| --------------- | ----- | ------------ | -------- | --------- | ------ | ------------------ | --- |
|                 | Run   | your program |          | (see      | Figure | 12.2).             |     |
| In the          | above | code         | example, |           | the    | first line creates | an  |
| OleDbConnection |       | object       | called   | myConnect |        | and supplies       | the |
connection string. In this case the Microsoft JET driver is specified
as well as the local path for the MS Access database known as
Finance.mdb. With the connection string specified, a new instance
of the OleDbConnection is created. Notice that the connection
string is passed in the constructor, the New() method, of the
OleDbConnectionobject.Afewlinesdown,themyConnect.Open()
method is called. At that point, assuming no errors and that the
| database actually |     | exists,      | the database |     | connection          | is made. |         |
| ----------------- | --- | ------------ | ------------ | --- | ------------------- | -------- | ------- |
| The second        |     | line of code | creates      |     | an OleDbDataAdapter |          | object. |
Twoargumentsarepassedtoitsconstructor:astringcontainingan
| F I G U | R E | 12.2 |     |     |     |     |     |
| ------- | --- | ---- | --- | --- | --- | --- | --- |
Team-LRN

| 212 |     |     |     |     |     | DatabaseProgramming |     |     |
| --- | --- | --- | --- | --- | --- | ------------------- | --- | --- |
SQL statement that indicates that we are selecting (cid:1), which means
| all the    | columns, | from  | the table | named | AXP,      | and the | database  |     |
| ---------- | -------- | ----- | --------- | ----- | --------- | ------- | --------- | --- |
| connection | against  | which | the       | SQL   | statement | will be | executed, |     |
namely myConnect.
The third line of code in the example creates a DataSet object
called myDataSet.
Onceourthreeobjectsarecreatedandtheconnectionisopen,
we can execute the SQL statement by calling the myAdapter.Fill()
| method | of our | OleDbDataAdapter |     |     | object. This | method | takes | two |
| ------ | ------ | ---------------- | --- | --- | ------------ | ------ | ----- | --- |
arguments. The first argument is the DataSet that will hold all the
data returned by the SQL query. The second is a string value that
represents the name of the resulting DataTable. This name is an
arbitrarystringthatwesupply.OncethedataisintheDataSet,we
close the connection to the database using myConnect.Close().
Atthispointintheprogram,allthedatafromthetablenamed
| AXP in | the database |     | now exists | in  | memory | in myDataSet. |     | We  |
| ------ | ------------ | --- | ---------- | --- | ------ | ------------- | --- | --- |
display the data by telling DataGrid1 which DataSet, myDataSet,
andwhichDataMember,whichistheDataTablethatwearbitrarily
named AXPdata.
AsintheDataSetexamplewelookedatearlierinthechapter,
| we can | retrieve | any | specific | element |     | in the DataTable |     | by  |
| ------ | -------- | --- | -------- | ------- | --- | ---------------- | --- | --- |
referencing its DataSet, its DataTable, its row, and its column. As
you can see, the DataAdapter constructed the DataSet with the
same schema that we manually created in the previous program.
Nowthatthedataisinmemory,wecanperformmathematical
operations on it. In its current form, the data set consists of a date
columnandopen,high,low,close,andvolumecolumns.Primarily
when doing quantitative research, we are interested in log returns
as opposed to actual prices. So the log returns must be calculated.
| We can   | choose | to pass       | a   | reference | to the | DataRowCollection |     |      |
| -------- | ------ | ------------- | --- | --------- | ------ | ----------------- | --- | ---- |
| directly | to a   | new function, |     | or we     | may    | wish to create    | a   | one- |
dimensionalarrayoflogreturnsfirst,whichthencanbeusedwith
the functions discussed in Chapter 8. Let’s look at both methods.
| Step | 7   | First let’s   | pass     | a reference | to               | the DataRowCollection |        |     |
| ---- | --- | ------------- | -------- | ----------- | ---------------- | --------------------- | ------ | --- |
|      |     | to a new      | function | called      | ColumnAverage(). |                       | Change |     |
|      |     | the last line | of       | code to     | the following:   |                       |        |     |
Label1.Text = ColumnAverage(myDataSet.Tables("AXPdata").Rows, 5)
Team-LRN

| ADO.NET |       |         |            |        |                 | 213 |
| ------- | ----- | ------- | ---------- | ------ | --------------- | --- |
| Step    | 8 Now | add the | definition | of the | ColumnAverage() |     |
function:
Function ColumnAverage(ByRef myDataPoints As DataRowCollection, _
|     |               | ByVal     | intCol As | Integer) | As Double |     |
| --- | ------------- | --------- | --------- | -------- | --------- | --- |
|     | Dim dblTotRet | As Double |           |          |           |     |
Dim x As Integer
|     | For x     | = 0 To myDataPoints.Count-1     |     |     |     |     |
| --- | --------- | ------------------------------- | --- | --- | --- | --- |
|     | dblTotRet | += myDataPoints(x).Item(intCol) |     |     |     |     |
Next x
|              | Return | dblTotRet / | (x + 1) |     |     |     |
| ------------ | ------ | ----------- | ------- | --- | --- | --- |
| End Function |        |             |         |     |     |     |
NoticethattheColumnAverage()functionacceptsareference
toaDataRowCollectionandanintegerspecifyingthecolumntobe
averaged. In this case, we are averaging column 5, the volume
column, and so our program will print into the label the average
| volume. The | calling | statement | uses | the Rows | property, | which |
| ----------- | ------- | --------- | ---- | -------- | --------- | ----- |
returns a reference to a DataRowCollection, as mentioned earlier.
| Step    | 9   |             |             |        |     |     |
| ------- | --- | ----------- | ----------- | ------ | --- | --- |
|         | Run | the program | (see Figure | 12.3). |     |     |
| F I G U | R E | 12.3        |             |        |     |     |
Team-LRN

214 DatabaseProgramming
The alternative method is to create an array of log returns,
which can then be used with the statistical functions we looked at
previously.
Step 10 Add the following code to your Button1_Click
event:
Dim intLength As Integer = myDataSet.Tables("AXPdata").Rows.Count
Dim x%
Dim dblAXPreturns As Double() = New Double(intLength - 2) {}
For x = 1 To intLength - 1
dblAXPreturns(x - 1) = _
Math.Log(myDataSet.Tables("AXPdata").Rows(x).Item("ClosePrice") / _
myDataSet.Tables("AXPdata").Rows(x - 1).Item("ClosePrice"))
Next x
Label1.Text = Average(dblAXPreturns)
Step11 NowaddthecodefortheAverage()functionthatwe
lookedatinChapter8.Youcaneithertypeitorpaste
it in from the file on the CD.
Public Function Average(ByRef Returns As Double()) As Double
Dim dblTotRet As Double
Dim x As Integer
F I G U R E 12.4
Team-LRN

| ADO.NET |     |            |              |                   |     |     | 215 |
| ------- | --- | ---------- | ------------ | ----------------- | --- | --- | --- |
|         | Dim | dblLength# |              | = UBound(Returns, | 1)  |     |     |
|         | For | x = 0      | To dblLength |                   |     |     |     |
|         |     | dblTotRet  | +=           | Returns(x)        |     |     |     |
Next x
|      | Return   | dblTotRet |             | / (dblLength | + 1)   |        |     |
| ---- | -------- | --------- | ----------- | ------------ | ------ | ------ | --- |
| End  | Function |           |             |              |        |        |     |
| Step | 12       | Run       | the program | (see         | Figure | 12.4). |     |
Inthefollowingchapter,wewilllearnhowtoaddcolumnsto
tables to allow us to add this calculated data back to a database
itself.
SUMMARY
InthischapterwebrieflydiscussedtheADO.NETarchitectureand
someoftheOleDbobjectsforconnectingtodatabases.Specifically,
welookedatamodelfordatabaseinteractionthatincludestheuse
| of OleDbConnection |     |     | objects, | OleDbDataAdapters, |     | and DataSets. |     |
| ------------------ | --- | --- | -------- | ------------------ | --- | ------------- | --- |
DataSets contain DataTables, which in turn contain collections of
| DataColumns |        | and | DataRows. | Understanding |        | the structure | of a |
| ----------- | ------ | --- | --------- | ------------- | ------ | ------------- | ---- |
| DataSet     | allows | us  | to access | the data      | within | the DataSet.  |      |
Team-LRN

| 216 |     |     |     |     | DatabaseProgramming |     |
| --- | --- | --- | --- | --- | ------------------- | --- |
PROBLEMS
| 1. What | is an OleDbConnection |     | object? | What | is  | an OleDb- |
| ------- | --------------------- | --- | ------- | ---- | --- | --------- |
DataAdapter?
| 2. Describe | the model     | we use         | to interact | with       | a database. |         |
| ----------- | ------------- | -------------- | ----------- | ---------- | ----------- | ------- |
| 3. Describe | the structure | of a           | DataSet     | object.    |             |         |
| 4. What     | code can      | we use to      | access      | a specific | item        | of data |
| within      | a DataSet?    |                |             |            |             |         |
| 5. Write    | the lines of  | code necessary |             | to add     | a DataRow   | to a    |
| DataTable   | named         | myDataTable.   |             |            |             |         |
Team-LRN

| ADO.NET         |             |      |          |              |         |         |          | 217 |
| --------------- | ----------- | ---- | -------- | ------------ | ------- | ------- | -------- | --- |
| PROJECT         |             | 12.1 |          |              |         |         |          |     |
| The Finance.mdb |             |      | database | contains     | several | tables. | Create   | a   |
| Windows         | application |      | that     | gets all the | columns |         | from the | IBM |
| table and       | displays    | them | in       | a DataGrid.  |         |         |          |     |
Further,yourprogramshouldallowtheusertoenteranindex
numbercorrespondingtoaspecificrowintheDataTable.Inlabels,
print out the date, open, high, low, and closing prices and the
| volume  | associated | with | this | index. |     |     |     |     |
| ------- | ---------- | ---- | ---- | ------ | --- | --- | --- | --- |
| PROJECT |            | 12.2 |      |        |     |     |     |     |
CreateaWindowsapplicationthatconnectstotheSPYtableinthe
| Finance.mdb |     | database | and | downloads | all | the columns |     | into a |
| ----------- | --- | -------- | --- | --------- | --- | ----------- | --- | ------ |
DataSet. Create a one-dimensional array and populate it with the
dailylogreturnsfromtheDataSet.Addthefunctiondefinitionsfor
the four moments of a distribution: Average(), Variance(), Skew(),
| and Kurtosis(). |         | Print  | out these | values           | in two           | labels.    |     |         |
| --------------- | ------- | ------ | --------- | ---------------- | ---------------- | ---------- | --- | ------- |
| What            | can     | we say | about     | the distribution |                  | of returns | on  | the SPY |
| over the        | DataSet | from   | the       | values you       | have calculated? |            |     |         |
Team-LRN

This page intentionally left blank.
Team-LRN

| C          | H A | P T | E R | 13  |       |     |     |     |     |
| ---------- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
| Structured |     |     |     |     | Query |     |     |     |     |
Language
S
| tructured |     | Query | Language |     | is  | a computer |     | language | for |
| --------- | --- | ----- | -------- | --- | --- | ---------- | --- | -------- | --- |
communication and interaction with databases. SQL was created
tobeasinglesyntaxtoextractandmanipulatedatafromdisparate
databasesystems.SointheorythesameSQLquerieswrittenforan
| Oracle    | database | will | work         | on  | a Sybase |      | database | or an        | Access |
| --------- | -------- | ---- | ------------ | --- | -------- | ---- | -------- | ------------ | ------ |
| database  | and      | so   | on. However, |     | database |      | vendors  | have         | also   |
| developed | their    | own  | versions     |     | of SQL   | such | as       | Transact-SQL | and    |
Oracle’sPL/SQL.ThischapterwillfocusonwritingstandardSQL
| and will | not | use any | vendor-specific |     |     | SQL | code. |     |     |
| -------- | --- | ------- | --------------- | --- | --- | --- | ----- | --- | --- |
SQListheengineforcommunicatingwiththedatabasesfrom
| programming |     | code.       | The | communicating |     |     | parties | are typically | a   |
| ----------- | --- | ----------- | --- | ------------- | --- | --- | ------- | ------------- | --- |
| “front-end” |     | application |     | or program,   |     | in  | our     | case a VB.NET |     |
application that sends an SQL statement across a connection via
anOleDbDataAdapter,anda“back-end”datasourcethatholdsthe
data.Thatstatement,theSQLcode,containsinstructionstoreador
changethedatawithinthedatabaseortomanipulatethedatabase
itself in some other way. The universal rules of SQL have been
established by ANSI, the American National Standards Institute,
| and therefore |          | are | open,  | meaning  |           | that | SQL        | is not owned | or  |
| ------------- | -------- | --- | ------ | -------- | --------- | ---- | ---------- | ------------ | --- |
| controlled    | by       | any | single | company. |           |      |            |              |     |
| The           | strength |     | of SQL | is its   | universal |      | acceptance | by database  |     |
vendors,andwhiletherehasbeenalotoftalkandmarketingabout
219
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

| 220    |       |               |     |                       |     |     | DatabaseProgramming |             |     |
| ------ | ----- | ------------- | --- | --------------------- | --- | --- | ------------------- | ----------- | --- |
| “write | once, | run anywhere” |     | languages,fordatabase |     |     |                     | programmers |     |
it is really true. Understanding SQL is the ticket to “learn once,
profit anywhere.”
| SQL | is  | not a programming |     |     | language | in  | the way | that VB.NET |     |
| --- | --- | ----------------- | --- | --- | -------- | --- | ------- | ----------- | --- |
is.Itisapurelanguage.Thereisnodevelopmentenvironmentbuilt
into SQL. It does not have user forms like Windows applications.
SQL is a nonprocedural programming language consisting of only
about 100 specialized words that we can combine into statements.
WecanembedthesestatementsintoVB.NETprogramstoperform
everything from simple data retrieval to high-level operations on
databases.
| The       | SQL | statements |              | that we | may     | most | often   | be concerned |     |
| --------- | --- | ---------- | ------------ | ------- | ------- | ---- | ------- | ------------ | --- |
| with when |     | developing | quantitative |         | trading |      | or risk | management   |     |
systems are those that retrieve data, called queries. However, we
will at times also need to write data to a database or delete data
from a database. Forexample,since historical datais almost never
| perfectly | clean, | we  | may | need to | remove | or  | change | bad | quotes, |
| --------- | ------ | --- | --- | ------- | ------ | --- | ------ | --- | ------- |
whichrequireschangingdatainthedatabase.Alsowemayneedto
calculate values, such as log returns, that are not included in the
| raw data | and | that | then | must | be saved | back | to  | a database. | So  |
| -------- | --- | ---- | ---- | ---- | -------- | ---- | --- | ----------- | --- |
although SQL has many capabilities, we will need to at least learn
| how to     | read    | data, | create  | new      | fields | and      | records | to hold | new  |
| ---------- | ------- | ----- | ------- | -------- | ------ | -------- | ------- | ------- | ---- |
| calculated | values, | and   | change  | or       | delete | existing | data.   |         |      |
| By         | the     | end   | of this | chapter, | you    | should   |         | have a  | good |
understanding of the syntax of SQL. In addition, you should be
| ableto | writeSQLcode |     | to  | performbasic |     | queries. | Ourexperienceis |     |     |
| ------ | ------------ | --- | --- | ------------ | --- | -------- | --------------- | --- | --- |
thatunderstandingthebasicsofSQLismucheasierthanmastering
all the intricacies of it. In other words, it is relatively easy to get
| good at | SQL, | but very  | difficult | to  | get great     | at  | it. |           |     |
| ------- | ---- | --------- | --------- | --- | ------------- | --- | --- | --------- | --- |
| We      | are  | confident | that      | SQL | is a language |     | in  | which you | can |
becomefairlyproficientinarelativelyshortamountoftime.Aswe
mentioned, SQL consists of only about 100 or so words, and SQL
statements are simply groups of those words logically arranged to
pullspecificdatafromthedatasourceormanipulatethedatainthe
data source. These types of SQL statements are referred to as data
manipulationlanguage(DML).Also,however,SQLcanbeusedto
actually manipulate the database itself. These SQL statements are
calleddatadefinitionlanguage(DDL).Inthischapter,wewillgeta
| chance | to look | at both | DML | and | DDL. |     |     |     |     |
| ------ | ------- | ------- | --- | --- | ---- | --- | --- | --- | --- |
Team-LRN

StructuredQueryLanguage 221
DATA MANIPULATION LANGUAGE
We use DML to work with the actual data held within databases.
The SELECT Statement
Readingdataisthemostcommontaskwewanttoperformagainst
adatabase.ASELECTstatementqueriesthedatabaseandretrieves
selecteddatathatmatchesthecriteriathatwespecify.TheSELECT
statement has five main clauses, although a FROM clause is the
only required one. Each of the clauses has a wide array of options
and parameters. Here we will show the general structure of a
SELECT statement with clauses. However, each of them will be
covered in more detail later in the chapter.
SELECT [ALL | DISTINCT] column1,column2
FROM table1,table2
[WHERE "conditions"]
[GROUP BY "column-list"]
[HAVING "conditions"]
[ORDER BY "column-list" [ASC | DESC] ]
Again, in the SELECT syntax, only SELECT and the FROM
clausearerequired.InEnglish,aSELECTstatementmeansthatwe
want to select columns from a table. When selecting multiple
columns, a comma must delimit each of them except for the last
column. Also be aware that as with VB.NET, SQL is not case-
sensitive.Uppercaseorlowercaseletterswilldojustfine.Beaware
toothatmost,butnotall,databasesrequiretheSQLstatementtobe
terminated by a semicolon.
Before we get too in-depth, let’s create a VB.NET program to
test out the SQL statements we look at as we go along.
Step 1 Create a new Windows application named
SQLexample.
Step 2 To Form1 add a text box, a button, and a data grid.
Step 3 In the Form1 code window add the following code.
Mostofthiscodeshouldlookveryfamiliar.Itfollows
closely the example presented in the previous
chapter. This time, however, we will use the
Options.mdb database.
Team-LRN

| 222     |                   |       |     |     |     | DatabaseProgramming |     |
| ------- | ----------------- | ----- | --- | --- | --- | ------------------- | --- |
| Imports | System.Data.OleDb |       |     |     |     |                     |     |
| Public  | Class             | Form1 |     |     |     |                     |     |
Inherits System.Windows.Forms.Form
| Windows | Form | Designer | generated | code |     |     |     |
| ------- | ---- | -------- | --------- | ---- | --- | --- | --- |
Dim myConnect As New OleDbConnection("Provider=Microsoft.Jet.OLEDB. _
4.0;DataSource=C:\ModelingFM\Options.mdb")
| Dim | myAdapter | As  | OleDbDataAdapter |     |     |     |     |
| --- | --------- | --- | ---------------- | --- | --- | --- | --- |
| Dim | myDataSet | As  | DataSet          |     |     |     |     |
Private Sub Button1_Click(ByVal sender As ...) Handles Button1.Click
Try
|     |     | myAdapter | = New | OleDbDataAdapter(TextBox1.Text, |     |     | myConnect) |
| --- | --- | --------- | ----- | ------------------------------- | --- | --- | ---------- |
myConnect.Open()
|     |     | myDataSet                 | = New | DataSet()   |           |     |     |
| --- | --- | ------------------------- | ----- | ----------- | --------- | --- | --- |
|     |     | myAdapter.Fill(myDataSet, |       |             | "myData") |     |     |
|     |     | DataGrid1.DataSource      |       | = myDataSet |           |     |     |
|     |     | DataGrid1.DataMember      |       | = "myData"  |           |     |     |
Catch
|     |     | MsgBox("Please | enter | a valid | SQL | statement.") |     |
| --- | --- | -------------- | ----- | ------- | --- | ------------ | --- |
Finally
myConnect.Close()
End Try
| End | Sub   |     |     |     |     |     |     |
| --- | ----- | --- | --- | --- | --- | --- | --- |
| End | Class |     |     |     |     |     |     |
ThisprogramwillallowtheusertoprovideanSQLstatement
during run time. Furthermore, we will be able to test out several
| SQL statements |     | without | having | to  | rerun the | program. | Also we |
| -------------- | --- | ------- | ------ | --- | --------- | -------- | ------- |
have included a Try...Catch block so the program won’t crash if
| you make | a   | mistake | in the SQL    | statement. |       |            |              |
| -------- | --- | ------- | ------------- | ---------- | ----- | ---------- | ------------ |
| Step     | 4   |         |               |            |       |            |              |
|          |     | Run the | program       | and        | enter | into the   | text box the |
|          |     | simple  | SQL statement |            | shown | below. See | also Figure  |
13.1.
SELECT OptionSymbol,StockSymbol,Year,Month,Strike,Bid,Ask,OpenInt
FROM OptionContracts;
| This | SQL | statement | will | work in | any programming |     | language |
| ---- | --- | --------- | ---- | ------- | --------------- | --- | -------- |
or development environment, including, as you can see, VB.NET.
NoteinFigure13.1thatthecolumnsaredisplayedintheorderthat
they appear in the SELECTstatement. If all columns from a table
are neededto bepart of the result set, we do not need to explicitly
specify them. Rather, in the case where all columns are to be
selected, we can use the (cid:1) symbol. As we saw in the previous
chapter’s example, the resulting SQL statement would look like
this:
| SELECT |     | * FROM | OptionContracts; |     |     |     |     |
| ------ | --- | ------ | ---------------- | --- | --- | --- | --- |
Team-LRN

StructuredQueryLanguage 223
| F I G U | R E 13.1        |            |         |             |
| ------- | --------------- | ---------- | ------- | ----------- |
| For     | now, leave your | SQLexample | Windows | application |
running. You can test out the SQL statements as you read through
| the rest of | the chapter. |       |        |     |
| ----------- | ------------ | ----- | ------ | --- |
|             | The          | WHERE | Clause |     |
The previous example retrieved a result set that included all the
rows in the table from the specified columns. Usually, however,
some rows need to be filtered out. Most queries we will write will
notretrievealltherowsfromatable,butonlyasubsetofthem.This
| is where | the WHERE clause | comes | in. The WHERE | clause filters |
| -------- | ---------------- | ----- | ------------- | -------------- |
outrowsfromatableaccordingtosomecondition.Forexample,as
in the Finance.mdb database example, if we want to look at the
price data foronly the year 1994, we could achieve this by using a
comparisonoperatorintheWHEREstatement.HereisalistofSQL
| comparison         | operators:                                        |     |             |     |
| ------------------ | ------------------------------------------------- | --- | ----------- | --- |
| ComparisonOperator |                                                   |     | Description |     |
| ,                  | Contentsofthefieldarelessthanthevalue             |     |             |     |
| ,¼                 | Contentsofthefieldarelessthanorequaltothevalue    |     |             |     |
| .                  | Contentsofthefieldaregreaterthanthevalue          |     |             |     |
| .¼                 | Contentsofthefieldaregreaterthanorequaltothevalue |     |             |     |
| ¼                  | Contentsofthefieldareequaltothevalue              |     |             |     |
| ,.                 | Contentsofthefieldarenotequaltothevalue           |     |             |     |
| BETWEEN            | Contentsofthefieldfallbetweenarangeofvalues       |     |             |     |
| LIKE               | Contentsofthefieldmatchacertainpattern            |     |             |     |
| IN                 | Contentsofthefieldmatchoneofanumberofcriteria     |     |             |     |
Team-LRN

224 DatabaseProgramming
If we are interested in only the option contracts with open
interest greater than 1000, our SQL would look like this:
SELECT * FROM OptionContracts WHERE OpenInt > 1000;
Try this out in your SQLexample application. The WHERE
clause can also have multiple conditions using AND or OR. If we
want to see all contracts where open interest is over 1000 and the
bid is greater than 0, it would look like this:
SELECT * FROM OptionContracts WHERE OpenInt > 1000 AND Bid > 0;
The Options.mdb database does not have any string-type
fields. If we need to build a WHERE clause for such a field, MS
Accessrequiresthatweusesinglequotesforstringcomparisonlike
this:
SELECT * FROM OptionContracts WHERE StockSymbol = ’IBM’;
Date comparison requires the use of the pound sign, #. For
example, if we want to see all the options trades done in February
2003, we would use this SQL statement:
SELECT * FROM OptionTrades
WHERE TradeDateTime >= #2/01/2003# AND TradeDateTime <= #2/28/2003#;
The ORDER BY Clause
WecansortourresultsetwiththeORDERBYclause.ORDERBYis
anoptionalclausethatallowsustodisplaytheresultsofourquery
in a sorted order, either ascending or descending, based on the
columns we specify to order by. Here is an example:
SELECT * FROM OptionContracts
WHERE StockSymbol = ’MSFT’ ORDER BY OpenInt;
ThisstatementselectsalltheMSFToptioncontractsandordersthe
data from the lowest open interest to the highest.
Toviewthedataindescendingorder,wesimplyaddDESCto
the end, as shown here:
SELECT * FROM OptionContracts
WHERE StockSymbol = ’MSFT’ ORDER BY OpenInt DESC;
Team-LRN

StructuredQueryLanguage 225
If we need to order based on multiple columns, we must
separate the columns with commas:
SELECT * FROM OptionContracts
WHERE StockSymbol = ’MSFT’ ORDER BY OpenInt DESC, Strike;
Notice that the contracts that have the same open interest are now
listed in order of strike price. Also the DESC applies only to the
OpenInt. Strike is sorted with the default ASC order.
The LIKE Clause
We have looked at the comparison operators that can be used in a
WHERE clause, and most of them are self-explanatory and do not
warrant further discussion. The exception to this is the LIKE
operator.
So far we have learned how to find exact matches with SQL.
However,theremaybetimesyouneedtosearchforpartialstrings.
SQL provides a LIKE operator for just this type of query.
TheLIKEoperatorcanonlybeusedonfieldsthathaveoneof
thestringtypessetastheirdatatype.LIKEcannotbeusedondates
or numbers.
String comparison employs a wildcard sign, %, which can be
used to match any possible character that might appear before or
afterthecharactersspecified.Forthesakeofexamples,wewilluse
the standard SQL % wildcard symbol. If you want to view all the
IBM option contracts with an 80 strike, you would write this
statement:
SELECT * FROM OptionContracts
WHERE StockSymbol = ’IBM’ AND OptionSymbol LIKE ’%P’;
The LIKE operator proves to be very useful as we write more
complexSQLstatementssinceitenablesustofindpartialmatches
withoutperforminganycomplicatedstringmanipulation.Keepin
mind,however,thattheLIKEoperatorisnotthemostefficientSQL
command,anditwilldegradeoverallperformance.Ifweknowthe
exactstringwearelookingforinafield,thenweshouldusethe ¼
operator instead of LIKE. Adding an index on a field that is often
searched using the LIKE operator may increase system
performance.
Team-LRN

| 226 |          |     |                 |     |           |     | DatabaseProgramming |     |
| --- | -------- | --- | --------------- | --- | --------- | --- | ------------------- | --- |
| In  | addition | to  | the % wildcard, |     | there are | two | other important     |     |
wildcardsusedwiththeLIKEoperator:theunderscore(_)andthe
squarebrackets([]).Whereasthe%wildcardisusedtofindastring
with any number of characters before and/or after the specified
characters, the underscore is used to limit the search to a single
leading or trailing character. A search of ‘%D%’ would return
MCDREandIBMDP.Say,forexample,wewanttofindalltheApril
| calls for | all | the stocks. | Omitting   |     | the IBM | WHERE | class     | and    |
| --------- | --- | ----------- | ---------- | --- | ------- | ----- | --------- | ------ |
| changing  | the | LIKE        | expression | to  | ‘%D_’   | would | limit the | return |
values to just those calls with April expiration since we are now
lookingforanyoptioncontractwithaDasthesecond-to-lastletter
in its symbol.
| SELECT        | *   | FROM OptionContracts |         |     | WHERE OptionSymbol |      | LIKE       | ’%D_’; |
| ------------- | --- | -------------------- | ------- | --- | ------------------ | ---- | ---------- | ------ |
| Additionally, |     | we                   | can use | the | brackets           | ([]) | to further | limit  |
ranges of characters. With the brackets, we can specify particular
charactersthatmustappearinaparticularposition.Forinstance,if
we were looking for April and May calls, then we need to modify
ourcriteria.Welimitoursearchtooptioncontractsthathaveeither
D or E in the second-to-last position, and so we specify this by
putting these characters within brackets, in the appropriate place:
SELECT * FROM OptionContracts WHERE OptionSymbol LIKE ’%[DE]_’;
| Keep | in  | mind | that the | brackets | may | only | contain | single |
| ---- | --- | ---- | -------- | -------- | --- | ---- | ------- | ------ |
characters,andsowecannotusethemforlistsofstrings.Thisisthe
biggestlimitationtothebracketwildcard,buttherearestillalarge
| number    | of possibilities |     | for expression |     | searching |     | in strings. |     |
| --------- | ---------------- | --- | -------------- | --- | --------- | --- | ----------- | --- |
| AGGREGATE |                  | SQL | FUNCTIONS      |     |           |     |             |     |
SofartheSQLthatwehavebeenusingretrievesrowsofdatafrom
thedatabase.ButSQLcandoalotmore.Amongotherthings,SQL
hasafewbuilt-infunctionsthatcantellusthingsaboutthedataas
a whole. For example, what if we wanted to know what contract
hasthelargestopeninterest?Howaboutthetotalnumberoftrades
foragivenmonth?Asyoucansee,thesenumbersarenotcontained
within the columns of a table. Rather, they must be computed.
Team-LRN

StructuredQueryLanguage 227
ANSI SQL contains aggregate functions that can compute
simple information from the data in a database. The aggregate
functionsinthetablebelowaretheofficialonesthataresupported
by SQL-compliant databases. Specific RDBMSs may support
additional aggregate functions that are proprietary and also very
useful.WereferyoutothedocumentationofyourRDBMSforalist
of nonstandard aggregate methods.
Aggregate
Function Description
AVG Returnstheaverageofthevaluesinacolumn
COUNT Returnsthetotalnumberofvaluesinacolumn
COUNT((cid:1)) Returnsthenumberofrowsinatable
MAX Returnsthelargestvalueinacolumn
MIN Returnsthesmallestvalueinacolumn
SUM Returnsthesumofthenumericvaluesinacolumn
The SUM Function
Let’sbeginbytakingalookattheSUMfunction.Itisusedwithina
SELECT statement and, predictably, returns the summation of a
seriesofvalues.Inthisexamplewewillcomputethetotalnumber
of shares traded in the month of January 2003.
SELECT SUM(Quantity) FROM StockTrades
WHERE TradeDateTime >= #1/1/2003# AND TradeDateTime <= #1/31/2003#;
Notice in Figure13.2that theresult setonlycontains onerow
ofdata.ThisistobeexpectedwhenusinganyoftheSQLaggregate
functions.Alsonoticethenameofthecolumn.SinceweaskedSQL
toreturnanaggregatevalue,SQLnamedthecolumnforus.When
this occurs, we say that an SQL-computed column is being used.
Ofcourse,thecolumnnameExpr1000isnotdescriptiveofthe
data it contains. Fortunately SQL column naming is simple. To
rename computed columns, use the AS modifier. The AS modifier
allows us to give meaningful names to any computed columns. If
we wanted to give a meaningful name—say, TotalShares—to the
computed column shown in Figure 13.2, we could write it as:
SELECT SUM(Quantity) AS TotalShares FROM StockTrades
WHERE TradeDateTime = #1/1/2003# AND TradeDateTime <= #1/31/2003#;
Team-LRN

| 228   |                   |     |           | DatabaseProgramming |     |
| ----- | ----------------- | --- | --------- | ------------------- | --- |
| F I G | U R E 13.2        |     |           |                     |     |
| The   | AVG/COUNT/MIN/MAX |     | Functions |                     |     |
Predictably,theseaggregatefunctionswillreturntheaverageofthe
data in a column, the lowest and highest values in a column, and
thecountornumberofelementsinacolumn.Ifwewanttoobtain
| the respective | values        | for the month    | of January | 2003, our | SQL |
| -------------- | ------------- | ---------------- | ---------- | --------- | --- |
| statements     | would look    | as follows:      |            |           |     |
| SELECT         | MIN(Quantity) | FROM StockTrades |            |           |     |
WHERE TradeDateTime >= #01/01/2003# AND TradeDateTime <= #1/31/2003#;
| SELECT | MAX(Quantity) | FROM StockTrades |     |     |     |
| ------ | ------------- | ---------------- | --- | --- | --- |
WHERE TradeDateTime >= #01/01/2003# AND TradeDateTime <= #1/31/2003#;
| SELECT | AVG(Quantity) | FROM StockTrades |     |     |     |
| ------ | ------------- | ---------------- | --- | --- | --- |
WHERE TradeDateTime >= #01/01/2003# AND TradeDateTime <= #1/31/2003#;
| SELECT | COUNT(*) FROM | StockTrades |     |     |     |
| ------ | ------------- | ----------- | --- | --- | --- |
WHERE TradeDateTime >= #01/01/2003# AND TradeDateTime <= #1/31/2003#;
|         | The      | DISTINCT | Function       |          |       |
| ------- | -------- | -------- | -------------- | -------- | ----- |
| The SQL | DISTINCT | function | is useful when | only the | first |
occurrence of a desired series of data is needed. For example, if
we are interested in seeing a list of all the stocks that have been
traded, we would not care to see duplicates. That is, we may have
traded MSFTseveral times, and we don’t care to see it listed more
thanonce.WecanfilteroutduplicateswiththeDISTINCTfunction.
Team-LRN

StructuredQueryLanguage 229
| SELECT | DISTINCT(StockSymbol) |                 | FROM StockTrades |     |
| ------ | --------------------- | --------------- | ---------------- | --- |
|        | ORDER                 | BY StockSymbol; |                  |     |
|        | The                   | GROUP           | BY Clause        |     |
As we have just seen, using aggregate functions such as SUM and
MIN will get us theappropriate value for all records or a group of
records.Whatif,however,wewanttowriteanSQLstatementthat
would show the SUMs of the quantities traded of each individual
optionsymbol?TheGROUPBYwillreturntheresultsofaggregate
| functions | for a group | of values. |     |     |
| --------- | ----------- | ---------- | --- | --- |
SELECT OptionSymbol,SUM(Quantity) FROM OptionTrades GROUP BY OptionSymbol;
| Notice | in Figure | 13.3 that | option symbols | are only displayed |
| ------ | --------- | --------- | -------------- | ------------------ |
when they have a value greater than zero. If, for example, the
summation of the quantity for AXPDZ were zero, it would not be
included in the result set. The GROUP BY clause can only be used
whenselectingmultiplecolumnsfromatableortablesandatleast
| one aggregate | function | appears      | in the SELECTstatement. |               |
| ------------- | -------- | ------------ | ----------------------- | ------------- |
| When          | there    | are multiple | columns beyond          | the one being |
aggregated, we can GROUP BYall the other selected columns. For
example, if we want the total quantity for all option symbols by
| BuySell, | the SQL would | look | like the following: |     |
| -------- | ------------- | ---- | ------------------- | --- |
| F I G    | U R E 13.3    |      |                     |     |
Team-LRN

230 DatabaseProgramming
SELECT OptionSymbol,BuySell,SUM(Quantity) FROM OptionTrades
GROUP BY OptionSymbol,BuySell;
NotethattheaboveSQLhastwocolumnsintheGROUPBYclause.
Remember, if the column appears in the SELECTand the SELECT
has aggregate functions, the column must appear in a GROUP BY
clause.
The HAVING Clause
The HAVING clause is like a WHERE clause for groups. By
definition an SQL statement that uses a GROUP BY clause cannot
use a WHERE clause. We must use a HAVING clause instead. For
example, if we want to see only those option contracts that have
totalquantitiestradedthataregreaterthanorequalto50,theSQL
statement would look like this:
SELECT OptionSymbol,SUM(Quantity) FROM OptionTrades
GROUP BY OptionSymbol HAVING SUM(Quantity) >= 50;
Figure 13.4 shows how the results would look on your screen.
TheHAVINGclauseisreservedforaggregatefunctionsandis
usually placed at the end of an SQL statement. Also, an SQL
statement with a HAVING clause may or may not necessarily
F I G U R E 13.4
Team-LRN

| StructuredQueryLanguage |       |     |         |               |     |           | 231 |
| ----------------------- | ----- | --- | ------- | ------------- | --- | --------- | --- |
| include the             | GROUP | BY  | clause. | The following | SQL | statement | is  |
valid:
| SELECT | COUNT(OptionSymbol) |               |     | FROM OptionTrades |     |     |     |
| ------ | ------------------- | ------------- | --- | ----------------- | --- | --- | --- |
|        | HAVING              | SUM(Quantity) |     | >= 50;            |     |     |     |
Aliasing
Anytimeanaggregatefunctionorcomputedcolumnappearsinan
| SQL statement, |     | SQL | will rename | it. As | we ran | the | previous |
| -------------- | --- | --- | ----------- | ------ | ------ | --- | -------- |
examples, we noticed that the column headings looked something
like Expr1000. And we saw that with the AS modifier, the column
canbealiasedwithanamewesupply.Usingacolumnaliasgreatly
| makes the | output | much | more | readable. | We  | can also | make |
| --------- | ------ | ---- | ---- | --------- | --- | -------- | ---- |
mathematical calculations in our SQL statements. The following
SQLusesacolumnaliastodescribethe(quantity(cid:1)price)ofatrade:
SELECT OptionSymbol,Price,Quantity,(Price * Quantity * 100) AS TradeCost
| FROM | OptionTrades; |     |     |     |     |     |     |
| ---- | ------------- | --- | --- | --- | --- | --- | --- |
IfyouruntheaboveSQL,youwillnoticethatthecolumntitle
is changed. The column holding the cost of each trade has been
aliased.TablescanalsobealiasedinaFROMclause.Thefollowing
example creates an alias named OT for the OptionTrades table:
| SELECT | * FROM | OptionTrades |     | OT; |     |     |     |
| ------ | ------ | ------------ | --- | --- | --- | --- | --- |
This is convenient when you want to retrieve information from
two or more separate tables, an operation known as joining. The
advantageofusingatablealiaswhenjoiningwillbecomeapparent
| over the | course of | the rest | of the  | chapter. |     |     |     |
| -------- | --------- | -------- | ------- | -------- | --- | --- | --- |
|          |           |          | Joining | Tables   |     |     |     |
Sofarinourexamples,wehaveretrieveddatafromonlyonetable.
Inmanyinstances,however,wemayneedtoretrievedatafromtwo
ormoretables.Anytimemorethanonetableisbeingqueried,they
must be joined. The Stock table and the OptionContracts table
above contain information about individual stocks and options
contracts on those stocks. In a real-world application, we may be
interested in returning data from both tables in a single SQL
Team-LRN

| 232 |     |     |     |     |     | DatabaseProgramming |     |     |
| --- | --- | --- | --- | --- | --- | ------------------- | --- | --- |
statement.Tojoin thesetwo tables wemustfirst identifya column
in each table that contains the same data. In this example the
| OptionContracts |                 | table | contains  | a   | StockSymbol       |        | column | that     |
| --------------- | --------------- | ----- | --------- | --- | ----------------- | ------ | ------ | -------- |
| matches         | the StockSymbol |       | column    | in  | the Stock         | table. |        |          |
| The             | two tables      | can   | be joined | on  | these StockSymbol |        |        | columns, |
althoughitisjustacoincidencethatboththesetablesarenamedthe
| same.       | In order | to join | tables, | the  | data must |     | match, | but not |
| ----------- | -------- | ------- | ------- | ---- | --------- | --- | ------ | ------- |
| necessarily | the      | column  | names.  | When | creating  | an  | SQL    | SELECT  |
statement containing more than one column, we first specify the
join. Here is an example using table aliasing for readability:
| SELECT | *     | FROM Stock    | S,  | OptionContracts |                 | OC  |     |     |
| ------ | ----- | ------------- | --- | --------------- | --------------- | --- | --- | --- |
|        | WHERE | S.StockSymbol |     | =               | OC.StockSymbol; |     |     |     |
In this example the join is performed within the WHERE clause.
| TheaboveSQLwill |     | returnallcolumnsforeachtablejoined |     |     |     |     |     | bythe |
| --------------- | --- | ---------------------------------- | --- | --- | --- | --- | --- | ----- |
stock symbol.
| With   | the     | two tables   | joined, | the      | SELECT | and | the | WHERE |
| ------ | ------- | ------------ | ------- | -------- | ------ | --- | --- | ----- |
| clause | can now | be modified. | For     | example: |        |     |     |       |
SELECT OC.OptionSymbol,OC.StockSymbol,OC.Bid,OC.Ask,S.DividendAmount
|     | FROM Stock | S,  | OptionContracts |     | OC  |     |     |     |
| --- | ---------- | --- | --------------- | --- | --- | --- | --- | --- |
WHERE S.StockSymbol = OC.StockSymbol AND S.StockSymbol = ’IBM’;
| Figure | 13.5 shows | a screen | shot | of the | results. |     |     |     |
| ------ | ---------- | -------- | ---- | ------ | -------- | --- | --- | --- |
| F I    | G U R E    | 13.5     |      |        |          |     |     |     |
Team-LRN

StructuredQueryLanguage 233
|     |     | The UNION | Keyword |     |
| --- | --- | --------- | ------- | --- |
A UNION is useful if you want to get data from two tables within
the same result set. Forexample, if we want to see the bid and ask
forINTCaswellasthebidsandasksforalltheINTCoptionsinone
| result | set, the SQL        | statement would | read as follows: |     |
| ------ | ------------------- | --------------- | ---------------- | --- |
| Select | StockSymbol,Bid,Ask |                 | FROM Stock       |     |
|        | WHERE               | StockSymbol =   | ’IBM’            |     |
UNION
| Select     | OptionSymbol,Bid,Ask |               | FROM OptionContracts |     |
| ---------- | -------------------- | ------------- | -------------------- | --- |
|            | WHERE                | StockSymbol = | ’IBM’;               |     |
| See Figure | 13.6.                |               |                      |     |
ThedatatypeforthecolumnsineachSELECTstatementmust
| match | for a UNION | to work. This | is not an issue | in the above |
| ----- | ----------- | ------------- | --------------- | ------------ |
example because each of the tables has identical column sets.
|     | The | INSERT | Statement |     |
| --- | --- | ------ | --------- | --- |
Up to this point we have only queried the Options.mdb database
and looked at the results. We may, however, also be interested in
changingthedata.Inordertoadd,delete,ormodifythedatainthe
| F I | G U R E 13.6 |     |     |     |
| --- | ------------ | --- | --- | --- |
Team-LRN

| 234 |     |     |     |     |     | DatabaseProgramming |     |     |
| --- | --- | --- | --- | --- | --- | ------------------- | --- | --- |
Options.mdb database, we will first need to add some elements to
| our SQLexample |       | program. |           |     |         |                   |     |        |
| -------------- | ----- | -------- | --------- | --- | ------- | ----------------- | --- | ------ |
| Step           | 5 Add | another  | button    |     | to your | form.             |     |        |
| Step           | 6 Add | the      | following |     | code to | the Button2_Click |     | event: |
Private Sub Button2_Click(ByVal sender As ...) Handles Button2.Click
Try
myConnect.Open()
|     |     | Dim command | As  | New OleDbCommand(TextBox1.Text, |     |     |     | myConnect) |
| --- | --- | ----------- | --- | ------------------------------- | --- | --- | --- | ---------- |
command.ExecuteNonQuery()
Catch
|     |     | MsgBox("Please |     | enter | a valid | SQL statement.") |     |     |
| --- | --- | -------------- | --- | ----- | ------- | ---------------- | --- | --- |
Finally
myConnect.Close()
End Try
| End Sub        |              |              |        |         |       |               |      |         |
| -------------- | ------------ | ------------ | ------ | ------- | ----- | ------------- | ---- | ------- |
| An             | OleDbCommand |              | object |         | is an | SQL statement | that | we can  |
| use to perform |              | transactions |        | against |       | a database.   | We   | use the |
ExecuteNonQuery()membermethodtoexecuteUPDATE,INSERT,
| and DELETE | statements.   |     |        |          |     |                  |     |        |
| ---------- | ------------- | --- | ------ | -------- | --- | ---------------- | --- | ------ |
| For        | the remainder |     | of the | chapter, |     | SELECTstatements |     | should |
beexecutedusingthefirstbutton,andallothertransactionsshould
| be executed | using | this | new, | second | button. |     |     |     |
| ----------- | ----- | ---- | ---- | ------ | ------- | --- | --- | --- |
TheSQLINSERTstatementenablesustoadddatatoatablein
a database. Here is an example showing the syntax for adding a
| record to | the OptionTrades  |     |     | table: |     |     |     |     |
| --------- | ----------------- | --- | --- | ------ | --- | --- | --- | --- |
| INSERT    | INTO OptionTrades |     |     |        |     |     |     |     |
(TradeDateTime, OptionSymbol, BuySell, Price, Quantity, TradeStatus)
| VALUES | (#02/27/2003#,’IBMDP’,’B’,2.60,10,’F’); |     |     |     |     |     |     |     |
| ------ | --------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
Youcanverifythatthisdatahasbeenaddedtothetablebywriting
| a simple | SELECTstatement. |     |     |     |     |     |     |     |
| -------- | ---------------- | --- | --- | --- | --- | --- | --- | --- |
Noticethatallvaluesforallcolumnshavebeensuppliedsave
for the TradeID column, which is generated automatically. If a
valueforacolumnistobeleftblank,thekeywordNULLcouldbe
used to represent a blank column value. In regard to data types,
notice that strings are delimited by single quotes, numerical data
does not need single quotes, and dates are defined with pound
signs.Aswehavementionedpreviously,eachRDBMSisdifferent,
and so you should look into the documentation of your system to
| see how | to define |     | the data | types. | Whatever | your | RDBMS, | the |
| ------- | --------- | --- | -------- | ------ | -------- | ---- | ------ | --- |
Team-LRN

| StructuredQueryLanguage |     |     |     |     |     |     |     | 235 |
| ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
comma-delimited list of values must match the table structure
exactly in the number of attributes and the data type of each
attribute.
|     |     | The | UPDATE | Statement |     |     |     |     |
| --- | --- | --- | ------ | --------- | --- | --- | --- | --- |
TheSQLUPDATEclauseisusedtomodifydatainadatabasetable
existinginoneorseveralrows.ThefollowingSQLupdatesonerow
| in the       | stock | table, the   | dividend       | amount      | for    | IBM:     |             |            |
| ------------ | ----- | ------------ | -------------- | ----------- | ------ | -------- | ----------- | ---------- |
| UPDATE       |       | Stock SET    | DividendAmount |             | =      | .55      |             |            |
|              | WHERE | StockSymbol  |                | = ’IBM’;    |        |          |             |            |
| SQL          | does  | not limit    | us             | to updating |        | only     | one column. | The        |
| following    | SQL   | statement    | updates        | both        | the    | dividend |             | amount and |
| the dividend |       | date columns | in             | the stock   | table: |          |             |            |
UPDATE Stock SET DividendAmount = .50,DividendDate = #03/18/2003#
|     | WHERE | StockSymbol | = ’IBM’; |     |     |     |     |     |
| --- | ----- | ----------- | -------- | --- | --- | --- | --- | --- |
Theupdateexpressioncanbeaconstant,anycomputedvalue,
or even the result of a SELECTstatement that returns a single row
and a single column. If the WHERE clause is omitted, then the
specifiedattributeissettothesamevalueineveryrowofthetable.
We can also set multiple attribute values at the same time with a
| comma-delimited |     | list | of attribute-equals-expression |           |     |     | pairs. |     |
| --------------- | --- | ---- | ------------------------------ | --------- | --- | --- | ------ | --- |
|                 |     | The  | DELETE                         | Statement |     |     |        |     |
As its name implies, we use an SQL DELETE statement to remove
datafromatableinadatabase.LiketheUPDATEstatement,either
single rows or multiple rows can be deleted. The following SQL
statement deletes one row of data from the StockTrades table:
| DELETE |           | FROM StockTrades |           |      |        |     |         |          |
| ------ | --------- | ---------------- | --------- | ---- | ------ | --- | ------- | -------- |
|        | WHERE     | TradeID          | =         | 40;  |        |     |         |          |
| The    | following | SQL              | statement | will | delete | all | records | from the |
StockTrades table that represent trades before January 4, 2003:
| DELETE |       | FROM StockTrades |     |     |               |     |     |     |
| ------ | ----- | ---------------- | --- | --- | ------------- | --- | --- | --- |
|        | WHERE | TradeDateTime    |     | <   | #01/04/2003#; |     |     |     |
Team-LRN

236 DatabaseProgramming
If the WHERE clause is omitted, then every row of the table is
deleted, which of course should be done with great caution.
BEGIN, COMMIT, and ROLLBACK
Transaction commands such as INSERT, UPDATE, and DELETE
may also contain keywords such as BEGIN, COMMIT, and
ROLLBACK, depending upon the RDBMS you are using. For
example,tomakeyourDMLchangesvisibletotherestoftheusers
of the database, you may need to include a COMMIT. If you have
made an error in updating data and wish to restore your private
copyofthedatabasetothewayitwasbeforeyoustarted,youmay
be able to use the ROLLBACK keyword.
In particular, the COMMIT and ROLLBACK statements are
part of a very important and versatile Oracle capability to control
sequences of changes to a database. You should consult the
documentationofyourparticularRDMBSwithregardtotheuseof
these keywords.
DATA DEFINITION LANGUAGE
We use DDL to create or modify the structure of tables in a
database. When we execute a DDL statement, it takes effect
immediately. Again, for all transactions, you should click Button2
toexecutethesenonqueries.Youwillbeabletoverifytheresultsof
the SQL statements by creating simple SELECT statements and
executing a query with Button1 in your program.
Creating Views
Aviewis a saved,read-only SQLstatement.Viewsareveryuseful
when you find yourself writing the same SQL statement over and
overagain.Here is asample SELECTstatement to findalltheIBM
option contracts with an 80 strike:
SELECT * FROM OptionContracts
WHERE StockSymbol = ’IBM’ AND OptionSymbol LIKE ’%P’;
Team-LRN

| StructuredQueryLanguage |     |            |              |     |     |       |     | 237       |
| ----------------------- | --- | ---------- | ------------ | --- | --- | ----- | --- | --------- |
| Although                |     | not overly | complicated, |     | the | above | SQL | statement |
is not overly simplistic either. Rather than typing it again and
again, we can create a VIEW. The syntax for creating a VIEWis as
follows:
| CREATE |       | VIEW IBM80s | as SELECT | * FROM | OptionContracts  |     |      |       |
| ------ | ----- | ----------- | --------- | ------ | ---------------- | --- | ---- | ----- |
|        | WHERE | StockSymbol | =         | ’IBM’  | AND OptionSymbol |     | LIKE | ’%P’; |
TheabovecodecreatesaVIEWnamedIBM80s.Nowtorunit,
| simply | type | in the following | SQL      | statement: |     |      |          |     |
| ------ | ---- | ---------------- | -------- | ---------- | --- | ---- | -------- | --- |
| SELECT |      | * FROM IBM80s;   |          |            |     |      |          |     |
| Views  | can  | be deleted       | as       | well using | the | DROP | keyword. |     |
| DROP   | VIEW | IBM80s;          |          |            |     |      |          |     |
|        |      |                  | Creating | Tables     |     |      |          |     |
As you know by now, database tables are the basic structure in
whichdataisstored.Intheexampleswehaveusedsofar,thetables
have been preexisting. Oftentimes, however, we need to build a
| table     | ourselves. | While         | we         | are certainly |         | able     | to build | tables    |
| --------- | ---------- | ------------- | ---------- | ------------- | ------- | -------- | -------- | --------- |
| ourselves | with       | an RDBMS      | such       | as MS         | Access, |          | we will  | cover the |
| SQL code  | to         | create tables | in VB.NET. |               |         |          |          |           |
| As        | a review,  | tables        | contain    | rows          | and     | columns. | Each     | row       |
represents one piece of data, called a record, and each column,
calledafield,representsacomponentofthatdata.Whenwecreate
a table, we need to specify the column names as well as their data
types. Data types are usually database-specific but often can be
brokenintointegers,numericalvalues,strings,andDate/Time.The
| following    | SQL    | statement | builds | a simple | table | named | Trades: |     |
| ------------ | ------ | --------- | ------ | -------- | ----- | ----- | ------- | --- |
| CREATE TABLE | Trades |           |        |          |       |       |         |     |
(myInstr Char(4) NOT NULL,myPrice Numeric(8,2) NOT NULL,myTime Date _
| NOT | NULL);  |        |         |        |     |       |           |       |
| --- | ------- | ------ | ------- | ------ | --- | ----- | --------- | ----- |
| The | general | syntax | for the | CREATE |     | TABLE | statement | is as |
follows:
CREATE TABLE TableName (Column1 DataType1 Null/Not Null, ...);
Team-LRN

| 238 |      |            |     |      |     | DatabaseProgramming |     |         |
| --- | ---- | ---------- | --- | ---- | --- | ------------------- | --- | ------- |
| The | data | types that | you | will | use | most frequently     |     | are the |
VARCHAR2(n), a variable-length character field where n is its
maximumwidth;CHAR(n),afixed-lengthcharacterfieldofwidth
n; NUMERIC(w.d), wherew is the total width of the field and d is
the numberof places after the decimal point (omitting it produces
aninteger);andDATE,whichstoresbothdateandtimeinaunique
internalformat.NULLandNOTNULLindicatewhetheraspecific
| field may | be left | blank. |     |     |     |     |     |     |
| --------- | ------- | ------ | --- | --- | --- | --- | --- | --- |
Tablescanbedroppedaswell.Whenatableisdropped,allthe
| data it | contains | is lost.  |          |     |        |     |     |     |
| ------- | -------- | --------- | -------- | --- | ------ | --- | --- | --- |
| DROP    | TABLE    | myTrades; |          |     |        |     |     |     |
|         |          |           | Altering |     | Tables |     |     |     |
WehavealreadyseenthattheINSERTstatementcanbeusedtoadd
rows. Columns as well can be added to or removed from a table.
For example, if we want to add a column named Exchange to the
| StockTrades | table, | we  | can use | the | ALTER | TABLE | statement. | The |
| ----------- | ------ | --- | ------- | --- | ----- | ----- | ---------- | --- |
syntax is:
| ALTER | TABLE | StockTrades |     | ADD | Exchange | char(4); |     |     |
| ----- | ----- | ----------- | --- | --- | -------- | -------- | --- | --- |
Aswehaveseeninthepreviouschapter,alltablesmusthavea
| primary | key. We | can use | the     | ALTER      | TABLE | statement     |       | to specify |
| ------- | ------- | ------- | ------- | ---------- | ----- | ------------- | ----- | ---------- |
| TradeID | in the  | Trades  | table   | we created |       | previously.   |       |            |
| ALTER   | TABLE   | Trades  | ADD     | PRIMARY    |       | KEY(TradeID); |       |            |
| Columns |         | can be  | removed | as         | well  | using the     | ALTER | TABLE      |
statement.
| ALTER | TABLE | StockTrades |     | DROP | Exchange; |     |     |     |
| ----- | ----- | ----------- | --- | ---- | --------- | --- | --- | --- |
SUMMARY
| Over the     | course | of this  | chapter, |      | we         | have looked | at  | SQL data |
| ------------ | ------ | -------- | -------- | ---- | ---------- | ----------- | --- | -------- |
| manipulation |        | language | and      | data | definition | language.   |     | While we |
have certainly not covered all of SQL, you should now be fairly
Team-LRN

| StructuredQueryLanguage |     |     |     |     |     | 239 |
| ----------------------- | --- | --- | --- | --- | --- | --- |
proficientatextractingandmodifyingdatainadatabaseaswellas
| changing | the structure |     | of tables | within a | database.         |     |
| -------- | ------------- | --- | --------- | -------- | ----------------- | --- |
| SQL      | consists      | of  | a limited | number   | of SQL statements | and |
keywords,whichcanbearrangedlogicallytoperformtransactions
against a database. While it is easy to get good at SQL, it is very
| difficult | to become | an  | expert. |     |     |     |
| --------- | --------- | --- | ------- | --- | --- | --- |
Team-LRN

| 240 |     |     |     |     |     | DatabaseProgramming |
| --- | --- | --- | --- | --- | --- | ------------------- |
PROBLEMS
| 1. What | is SQL? | What | are | DDL | and DML? |     |
| ------- | ------- | ---- | --- | --- | -------- | --- |
2. Whatdocumentshouldyouconsulttofindoutthespecifics
| of SQL            | transactions |              | against   | your    | RDBMS?      |                 |
| ----------------- | ------------ | ------------ | --------- | ------- | ----------- | --------------- |
| 3. What           | is an        | OleDbCommand |           |         | object,     | and what is the |
| ExecuteNonQuery() |              |              | method?   |         |             |                 |
| 4. If we          | found        | corrupt      | data      | in      | a database, | what statements |
| might             | we           | use to       | either    | correct | it or get   | rid of it?      |
| 5. What           | is the       | syntax       | of CREATE |         | TABLE?      |                 |
Team-LRN

StructuredQueryLanguage 241
| PROJECT | 13.1 |     |
| ------- | ---- | --- |
The Finance.mdb database contains price data. However, we very
often will be interested in a time series of log returns. Create a
VB.NET application that will modify the AXP table to include a
Returnscolumn.Thenmakethecalculationsforthelogreturnsand
| populate | the column. |     |
| -------- | ----------- | --- |
| PROJECT  | 13.2        |     |
Create a VB.NETapplication that will connect to the Finance.mdb
database and return the average volume for a user-defined stock
| between any | two user-defined | dates. |
| ----------- | ---------------- | ------ |
Team-LRN

This page intentionally left blank.
Team-LRN

| C            | H A P T    | E R 14 |     |     |     |
| ------------ | ---------- | ------ | --- | --- | --- |
| Introduction |            |        | to  |     |     |
| Data         | Structures |        |     |     |     |
I
| n Chapter | 8 we | looked at arrays, | which | are the simplest | data |
| --------- | ---- | ----------------- | ----- | ---------------- | ---- |
structures and have fixed sizes, although they can be redimen-
sioned. Visual Basic.NET offers several other more dynamic data
structures known as collection objects, which are convenient for
holding groups of objects such as, for example, a portfolio of
options. These data structures include the Collection object itself
and the objects found in the System.Collections namespace, the
| mostnotable | ofwhich | forrightnoware | arraylists,queues,stacks, |     |     |
| ----------- | ------- | -------------- | ------------------------- | --- | --- |
hash tables, and sorted lists. Oddly enough, the Collection class
| itself is  | not located | in the System.Collections |     | namespace. |     |
| ---------- | ----------- | ------------------------- | --- | ---------- | --- |
| COLLECTION |             | OBJECT                    |     |            |     |
TheCollectionclassallowsustostoregroupsofobjectsofdifferent
datatypesandtoeasilycount,lookup,andaddorremoveobjects
within the collection using the Count and Item properties and the
AddandRemovemethodsoftheCollectionclass.Furthermorewe
| can iterate | through | the elements | in a | collection using | a For |
| ----------- | ------- | ------------ | ---- | ---------------- | ----- |
Each...Nextloop.Collectionsdonothavefixedsizes,andmemory
allocationiscompletelydynamic,andsoinmanycasestheywillbe
| a superior | way of | handling data | compared | with arrays. |     |
| ---------- | ------ | ------------- | -------- | ------------ | --- |
As with arrays, it will be important to note the index of the
first element. Most often, the Collection objects we will use will be
1-based. That is, the index of the first element will be by default 1
and not zero as with arrays. Also Collection objects allow us to
243
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

244 DatabaseProgramming
access elements of the collection by either index or an optional
string key. As we will see later, other collection types allow only
numeric index references and may not have a key. Here are the
properties and methods associated with Collection objects:
Collection
Properties Description Example
Count Returnsthenumberofobjectsin dblNum¼myColl.Count
thecollection
Item Returnsaspecificelementofthe dblObj¼myColl.Item(1)or
collection dblObj¼myColl.Item(strKey)
Collection
Methods Description Example
Add Addsanobjecttothecollection myColl.Add(myObj)
Remove Removesanobjectfromthe myColl.Remove(2)or
collection myColl.Remove(strKey)
We have in fact already had some experience with Collection
objects. As you may recall, several of the ADO.NET objects we
looked at in Chapter 12, like DataRowCollections and DataCo-
lumnCollections,areCollectionobjectsandassuchinheritfromthe
CollectionBase class.
Here is an example using a Collection object.
Step 1 Create a new Windows application named Portfolio.
Step 2 In theProject menuitem,selectAddClasstwiceand
add two new classes. Into these class code modules,
pasteinthecodefortheStockOptionandCallOption
classes.
Step 3 Go back to the Form1 code window, and in the
Form1_Load event, add the code to create a
Collection object named MyPortfolio.
Dim MyPortfolio As New Collection()
Step4 NextaddthecodetocreateaCallOptionobjectcalled
myOption.
Dim myOption As New CallOption("IBMDP")
Team-LRN

IntroductiontoDataStructures 245
Step 5 Add myOption to MyPortfolio.
MyPortfolio.Add(myOption)
Step 6 Now we can actually destroy myOption using the
Nothing keyword.
WhenweassignNothingtoanobject,theobjectreferencenolonger
refers to that object instance.
myOption = Nothing
Step 7 Still within the Form1_Load event, let’s create
another option and add it to MyPortfolio.
myOption = New CallOption("SUQEX")
MyPortfolio.Add(myOption)
myOption = Nothing
MyPortfolio now consists of two CallOption objects,
neitherknownbythenamemyOption,butratherby
their respective indexes within the MyPortfolio
collection.
Step 8 We could find the Strike price of the Sun
MicroSystemsoption(SUQEX)inthefollowingway:
Label1.Text = MyPortfolio.Item(2).Strike
Or simply:
Label1.Text = MyPortfolio(2).Strike
as shown in Figure 14.1.
F I G U R E 14.1
Team-LRN

| 246      |              |            | DatabaseProgramming |     |
| -------- | ------------ | ---------- | ------------------- | --- |
| CREATING | A CUSTOMIZED | COLLECTION |                     |     |
CLASS
Inthissimpleexample,wewillcreateourowncollectionclassthat
willholdaportfolioofoptions.ThisnewCollectionclasswillallow
us only to add option objects. As in the previous example, any
objecttype,notjustCallOptions,canbeaddedtoaninstanceofthe
generic Collection class since it is not strongly typed. There is an
inherent advantage and a disadvantage with using this approach.
Theadvantageisthatanyobjectrepresentingatradableinstrument
canbeaddedtoourMyPortfolioobject.However,thedisadvantage
isthatifwetrytouseaForEachCallOptionInMyPortfolio...Next
loopto processaportfolio of options,anerror willoccur sinceone
element in MyPortfolio may be, for example, a GovtBond object.
| In cases | where we require | a more robust | collection, | we can, |
| -------- | ---------------- | ------------- | ----------- | ------- |
through inheritance from the CollectionBase class, create our own
Collectionclassandaddourownfunctionality.TheCollectionBase
class, found in the System.Collections.namespace, includes the
publicClearmethod,theCountproperty,andaprotectedproperty
called List that implements the IList interface. The methods and
| properties—Add, | Remove, and | Item—require | that we | codify the |
| --------------- | ----------- | ------------ | ------- | ---------- |
implementation,asyouwillsee.Herearetheimportantproperties
| and methods | of the MustInherit | CollectionBase | class: |     |
| ----------- | ------------------ | -------------- | ------ | --- |
IList
| Implementations |                                                     | Description |     |     |
| --------------- | --------------------------------------------------- | ----------- | --- | --- |
| Count           | ReturnsthenumberofelementsintheCollectionBaseobject |             |     |     |
| PublicMethods   |                                                     | Description |     |     |
| Clear           | DeletesallelementsfromtheCollectionBaseobject       |             |     |     |
| Equals          | DetermineswhethertwoobjectsintheCollectionBaseare   |             |     |     |
equal
GetEnumerator Returnsanenumeratorthatcaniteratethroughtheelements
ofaCollectionBase
| RemoveAt | DeletesanelementfromtheCollectionBaseobjectata |     |     |     |
| -------- | ---------------------------------------------- | --- | --- | --- |
specifiedindex
IList
| Implementations |                                                      | Description |     |     |
| --------------- | ---------------------------------------------------- | ----------- | --- | --- |
| CopyTo          | CopiestheelementsofaCollectionBasetoaone-dimensional |             |     |     |
array
| Add      | AddsanelementattheendoftheCollectionBase         |     |     |     |
| -------- | ------------------------------------------------ | --- | --- | --- |
| Contains | Determineswhetheraspecifiedelementiscontainedina |     |     |     |
CollectionBase
Team-LRN

| IntroductiontoDataStructures |     |     |     |     |             |     |     | 247 |
| ---------------------------- | --- | --- | --- | --- | ----------- | --- | --- | --- |
| IList                        |     |     |     |     | Description |     |     |     |
Implementations
| IndexOf |     | Returnstheindexofthefirstoccurrenceofaspecified |     |     |     |     |     |     |
| ------- | --- | ----------------------------------------------- | --- | --- | --- | --- | --- | --- |
elementinaCollectionBase
| Insert |     | InsertsanelementintotheCollectionBaseatthespecified |     |     |     |     |     |     |
| ------ | --- | --------------------------------------------------- | --- | --- | --- | --- | --- | --- |
index
| Remove |     | Removesthefirstoccurrenceofaspecifiedelementfromthe |     |     |     |     |     |     |
| ------ | --- | --------------------------------------------------- | --- | --- | --- | --- | --- | --- |
CollectionBase
In this example, we will create an OptionCollection that only
accepts CallOptions as opposed to any object. Then we will add
methods to buy, implementing IList.Add(), and sell, IList.Remo-
| veAt(), CallOptions. |     |     | Also | we will | need | to implement |     | the Item |
| -------------------- | --- | --- | ---- | ------- | ---- | ------------ | --- | -------- |
property that returns the CallOption at a specified index. This
| customized | OptionCollection |     |     | class   | will be     | zero-based. |     |         |
| ---------- | ---------------- | --- | --- | ------- | ----------- | ----------- | --- | ------- |
| Step       | 1 Start          | a   | new | Windows | application |             | and | name it |
OptionCollection.
| Step   | 2 In             | thesamewayasin   |                 |        | thepreviousexample,add |            |             | the    |
| ------ | ---------------- | ---------------- | --------------- | ------ | ---------------------- | ---------- | ----------- | ------ |
|        | code             | for              | the StockOption |        | and                    | CallOption | classes.    |        |
| Step   | 3 Now            | add              | a code          | module |                        | for a      | third class | called |
|        | OptionCollection |                  |                 | with   | the following          |            | code:       |        |
| Public | Class            | OptionCollection |                 |        |                        |            |             |        |
Inherits System.Collections.CollectionBase
| Public | Sub Buy(ByVal |     | myOption | As CallOption) |     |     |     |     |
| ------ | ------------- | --- | -------- | -------------- | --- | --- | --- | --- |
List.Add(myOption)
| End    | Sub            |     |         |             |     |     |     |     |
| ------ | -------------- | --- | ------- | ----------- | --- | --- | --- | --- |
| Public | Sub Sell(ByVal |     | myIndex | As Integer) |     |     |     |     |
List.RemoveAt(myIndex)
| End | Sub |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Public ReadOnly Property Item(ByVal myIndex As Integer) As CallOption
Get
|     | Return | List.Item(myIndex) |     |     |     |     |     |     |
| --- | ------ | ------------------ | --- | --- | --- | --- | --- | --- |
End Get
| End    | Property |            |     |         |      |         |           |     |
| ------ | -------- | ---------- | --- | ------- | ---- | ------- | --------- | --- |
| End    | Class    |            |     |         |      |         |           |     |
| Notice | that     | the public |     | Buy and | Sell | methods | implement | the |
Add()andRemoveAt()methodsandtheItempropertyimplements
the Itempropertyof theList propertyof theparent CollectionBase
class.
| Step | 4 In             | the Form1_Load    |     | event,     | create  | an                    | instance | of the |
| ---- | ---------------- | ----------------- | --- | ---------- | ------- | --------------------- | -------- | ------ |
|      | OptionCollection |                   |     | class      | called  | MyOptionPortfolio.    |          |        |
|      | Also             | create            | two | CallOption | objects |                       |          |        |
|      | Dim              | myOptionPortfolio |     |            | As      | NewOptionCollection() |          |        |
|      | Dim              | myFirstOption     |     | As         | New     | CallOption("IBMDP")   |          |        |
|      | Dim              | mySecondOption    |     |            | As New  | CallOption("SUQEX")   |          |        |
Team-LRN

| 248        |         |             | DatabaseProgramming  |     |
| ---------- | ------- | ----------- | -------------------- | --- |
| F I G U R  | E 14.2  |             |                      |     |
| Step 5 Add | the two | CallOptions | to MyOptionPortfolio | by  |
“buying” them.
myOptionPortfolio.Buy(myFirstOption)
myOptionPortfolio.Buy(mySecondOption)
| Step 6 Sell | the IBMDP | option. |     |     |
| ----------- | --------- | ------- | --- | --- |
myOptionPortfolio.Sell(0)
| Step 7 The | SUQEX       | option is left                     | in the portfolio | as you can |
| ---------- | ----------- | ---------------------------------- | ---------------- | ---------- |
| see        | in Figure   | 14.2.                              |                  |            |
|            | Label1.Text | = myOptionPortfolio.Item(0).Strike |                  |            |
| CLEANING   | DATA        |                                    |                  |            |
Financial modeling and forecasting requires clean data for testing
and simulation. But almost no data is perfectly clean. In fact, we
shouldassumethatalldataisdirty.Asaresult,financialengineers
oftenspendlargeamountsoftimecleaningdata.Itisveryeasyand
very common to underestimate the amount of time it will take to
cleandata.Literallyhalfthetimerequiredforhigh-qualityanalysis
can typically be spent cleaning data, and every analyst can recall
wasting countless hours of time testing and coding only to draw
bad conclusions due to dirty data. Failing to adequately consider
the impact of bad datacan lead to the creation of bad models and,
worse, losses. Clean data can be profitable, but bad data will be
ruinous.Asyoumightimagine,thequalityofdatapurchasedfrom
different data vendors can range from very clean to terribly dirty.
Team-LRN

| IntroductiontoDataStructures |     |     |     |     |     |     | 249 |
| ---------------------------- | --- | --- | --- | --- | --- | --- | --- |
Using high-quality data almost always pays off even though it’s
moreexpensive.Inanycase,though,timespentfindinggooddata
and giving it a good once-over is worth the effort and expense.
| All | data should | be  | cleaned | before | use. | But serious | data |
| --- | ----------- | --- | ------- | ------ | ---- | ----------- | ---- |
cleaning involves more than just visually scanning data in Excel
and updating bad records with good data. Rather, it requires that
| we decompose | and | reassemble |     | data. | This takes | time. |     |
| ------------ | --- | ---------- | --- | ----- | ---------- | ----- | --- |
Data cleaning is a process that consists of first detection and
thencorrectionofdataerrorsandofupdatingthedirtydatasource
withcleandataorpreferablycreatinganewdatasourcetoholdthe
entire cleaned data set. Maintaining the original dirty data source
initsoriginalformallowsustogobackifwemakeamistakeinour
cleaning algorithms and consequently further corrupt the data.
| Another   | problem |      | requiring | data  | cleaning | occurs  | when,   |
| --------- | ------- | ---- | --------- | ----- | -------- | ------- | ------- |
| depending | on the  | time | interval  | we’re | looking  | at, the | data we |
have is not in the individual ticks or bars we desire (bars being
fixedunitsoftimewithadate/time,anopen,ahigh,alow,aclose,
| and maybe | even | a volume | and/or |     | open interest). | We  | may, for |
| --------- | ---- | -------- | ------ | --- | --------------- | --- | -------- |
example, possess tick data and want to analyze bars of several
different durations—a minute in length, 5 minutes, a day, a week,
or a month. It is, of course, possibleto convert raw tick data into a
seriesofbarsbywritingasimpleVB.NETprogramtogeneratethe
| bar data  | and save     | it to a  | new database. |     |       |             |          |
| --------- | ------------ | -------- | ------------- | --- | ----- | ----------- | -------- |
| Let’s     | look at some | of       | the common    |     | types | of bad data | we often |
| encounter | in financial | markets: |               |     |       |             |          |
Typeof
| BadData            |     |                                          |     |     | Example |     |     |
| ------------------ | --- | ---------------------------------------- | --- | --- | ------- | --- | --- |
| Badquotes          |     | Tickof23.54shouldbe83.54                 |     |     |         |     |     |
| Missingdata        |     | Blankfieldordatacodedas“9999,”“NA,”or“0” |     |     |         |     |     |
| Baddates           |     | 2/14/12997                               |     |     |         |     |     |
| Column-shifteddata |     | Valueprintedinanadjacentcolumn           |     |     |         |     |     |
| Filecorruption     |     | CDorfloppydiskerrors                     |     |     |         |     |     |
Differentdataformats Datafromdifferentvendorsmaycomeindifferentformats
ortableschemas
| Asweknow,theuseof |     |     | alargeamount |     | ofin-sampledatawill |     |     |
| ----------------- | --- | --- | ------------ | --- | ------------------- | --- | --- |
produce more stable models and have less curve-fitting danger,
thereby increasing the probability of success out-of-sample and
consequently during implementation. Sophisticated models, such
as GARCH(1,1), are often more affected by bad data as compared
| with simpler | models. |     |     |     |     |     |     |
| ------------ | ------- | --- | --- | --- | --- | --- | --- |
Team-LRN

| 250   |      |             |         |     |             |     | DatabaseProgramming |     |
| ----- | ---- | ----------- | ------- | --- | ----------- | --- | ------------------- | --- |
| Since | many | forecasting | models, |     | like GARCH, |     | are extremely       |     |
sensitivetoevenafewbaddatapoints,weshouldbesuretolookat
| means, medians, |     | standard | deviations, |     | histograms, |     | and minimum |     |
| --------------- | --- | -------- | ----------- | --- | ----------- | --- | ----------- | --- |
and maximum values of ourdata. A good way to do this is to sort
through the data set to examine values outside an expected range.
Or we can run scans to highlight suspicious, missing, extraneous,
or illogical data points. Here are a few, but certainly not all,
| methods often | used | to scan | data: |     |     |     |     |     |
| ------------- | ---- | ------- | ----- | --- | --- | --- | --- | --- |
ScanningforBadData
Intraperiodhighticklessthanclosingprice
Intraperiodlowtickgreaterthanopeningprice
Volumelessthanzero
Barswithwidehigh-lowrangesrelativetosomeprevioustimeperiod
Closingdeviance.Dividetheabsolutevalueofthedifferencebetweeneachclosingprice
andthepreviousclosingpricebytheaverageofthepreceding20absolutevalues
Datafallingonweekendsorholidays
Datawithout-of-orderdatesorwithduplicatebars
| As mentioned, |     | data | cleaning | has | three | components: |     | auditing |
| ------------- | --- | ---- | -------- | --- | ----- | ----------- | --- | -------- |
data to find bad data or to highlight suspicious data, fixing bad
data, and applying the fix to the data set or preferably saving the
data to a new data source. The methods we choose to accomplish
these three tasks constitute a data transformation management
| system (DTMS). |     | The hope | is  | that our | DTMS | will | improve | the |
| -------------- | --- | -------- | --- | -------- | ---- | ---- | ------- | --- |
qualityofthedataaswellasthesuccessofourmodels.Toreview,a
DTMS should capture data from your data source, clean it, and
then save it back or create a new data source with the clean data.
| As with | any | process, | it pays | to  | plan ahead |     | when building | a   |
| ------- | --- | -------- | ------- | --- | ---------- | --- | ------------- | --- |
DTMS. Before you begin, identify and categorize all the types of
errors you expect to encounter in your data, survey the available
techniquestoaddressthosedifferenttypesoferrors,anddevelopa
| system to  | identify | and resolve   |     | the errors. |        |          |      |      |
| ---------- | -------- | ------------- | --- | ----------- | ------ | -------- | ---- | ---- |
| Of course, | as       | we mentioned, |     | you         | should | purchase | data | only |
fromreputablevendorswhotakedataintegrityseriously.Evenso,
you should always scan and clean your data. It’s just that dealing
| with quality | vendors | will | nonetheless |     | save | time | and | improve |
| ------------ | ------- | ---- | ----------- | --- | ---- | ---- | --- | ------- |
results.
Team-LRN

| IntroductiontoDataStructures |     |        |                |     |     |     |     |     | 251 |
| ---------------------------- | --- | ------ | -------------- | --- | --- | --- | --- | --- | --- |
| CREATING                     |     | A DATA | TRANSFORMATION |     |     |     |     |     |     |
| MANAGEMENT                   |     | SYSTEM |                |     |     |     |     |     |     |
Let’slookatanexampleofhowtouseacollectiontobuildasimple
DTMS.
| Step | 1 Create                                    | a new                | Windows |     | application |      | called   | DTMS.      |         |
| ---- | ------------------------------------------- | -------------------- | ------- | --- | ----------- | ---- | -------- | ---------- | ------- |
| Step | 2 IntheForm1_LoadeventmakeanOleDbConnection |                      |         |     |             |      |          |            |         |
|      | to                                          | the DirtyFinance.mdb |         |     | database,   |      | retrieve |            | all the |
|      | columns                                     |                      | in the  | AXP | table       | with | an       | OleDbData- |         |
|      | Adapter                                     |                      | and an  | SQL | statement,  | and  | place    | the        | data    |
intomyDataSetwiththename“AXPdata.”Besureto
|                           | declare                   | myDataSet     |      | in      | the declarations |     | section |     | of the |
| ------------------------- | ------------------------- | ------------- | ---- | ------- | ---------------- | --- | ------- | --- | ------ |
|                           | Form1                     | class         | code | window. |                  |     |         |     |        |
| Imports System.Data.OleDb |                           |               |      |         |                  |     |         |     |        |
| Public Class              | Form1                     |               |      |         |                  |     |         |     |        |
| Inherits                  | System.Windows.Forms.Form |               |      |         |                  |     |         |     |        |
| Dim myDataSet             | As                        | New DataSet() |      |         |                  |     |         |     |        |
Private Sub Form1_Load(ByVal sender As ...) Handles MyBase.Load
Dim myConnect As New OleDbConnection("Provider=... ...\DirtyFinance.mdb")
Dim myAdapter As New OleDbDataAdapter("select * from AXP", myConnect)
myConnect.Open()
| myAdapter.Fill(myDataSet, |     |     | "AXPdata") |     |     |     |     |     |     |
| ------------------------- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- |
myConnect.Close()
End Sub
| At this | point, | you | may | notice | a particularly |     | advantageous |     |     |
| ------- | ------ | --- | --- | ------ | -------------- | --- | ------------ | --- | --- |
situation. The AXP price data is now already held in a collection,
namely a DataRowCollection. So we can, without any additional
machinations, loop through the collection’s elements, which are
DataRow objects, and search for bad data. We prefer, of course, to
containindividualdata-cleaningalgorithmsinseparateprocedures
orobjects.Thenwecansimplypassareferencetothecollectionas
aninputargumenttotheprocedureandcommencecleaning.Inthe
AXPdata DataTable, let’s search for intraday high prices that are
| less than the | closing                                         | price.  |     |          |          |     |             |     |      |
| ------------- | ----------------------------------------------- | ------- | --- | -------- | -------- | --- | ----------- | --- | ---- |
| Step          | 3 CreateasubroutinecalledCleanHighLessThanLow() |         |     |          |          |     |             |     |      |
|               | that                                            | accepts | as  | an input | argument |     | a reference |     | to a |
Team-LRN

252 DatabaseProgramming
DataRowCollection object. This subroutine should
loop through the element of a collection and find
instances where the intraday high is less than the
close.
As we discussed in Chapter 11, the DirtyFinance.mdb Access
database contains dirty data. For simplicity, your subroutine
should, upon finding a dirty data point, show a message box
alerting the user to the bad data as well as its index.
Private Sub CleanHighLessThanClose(ByRef myDataPoints As _
DataRowCollection)
Dim x As Integer
For x = 0 To myDataPoints.Count - 1
IfmyDataPoints(x).Item("HighPrice")< myDataPoints(x).Item("ClosePrice")
Then
MsgBox("Bad Data Point: High of " & _
myDataPoints(x).Item("HighPrice") & _
" and Close of " & myDataPoints(x).Item("Close") & _
" at " & Str(x))
End If
Next x
End Sub
Step 4 Add a button to Form1, and in the Button1_Click
event, call the subroutine to clean the table passing
a reference to the DataRowCollection. The Rows
property of the DataTable returns a reference to the
DataRowCollection.
Private Sub Button1_Click(ByVal sender As ...) Handles Button1.Click
CleanHighLessThanClose(myDataSet.Tables("AXPdata").Rows)
End Sub
Step 5 Run the program. Figure 14.3 shows the result.
F I G U R E 14.3
Team-LRN

| IntroductiontoDataStructures |              |                    |           | 253     |
| ---------------------------- | ------------ | ------------------ | --------- | ------- |
| In the AXP                   | table, there | are three instance | of a high | that is |
greaterthanthelow.Yourprogramshouldfindthematindexesof
| 177, 1200, and | 2342. |     |     |     |
| -------------- | ----- | --- | --- | --- |
SUMMARY
In this chapter we learned how to use the Collection object as well
as how to create our own Collection class by inheriting from the
CollectionBase class for adding Option objects to a strongly typed
Portfolioobject.Furtherwelookedattheimportanceofusingclean
data when making financial calculations and forecasts. Since data
stored in a DataSet is already in a DataRowCollection, we can
immediately scan data for errors by passing a reference to the
| DataRowCollection | to procedures | containing | data-cleaning |     |
| ----------------- | ------------- | ---------- | ------------- | --- |
algorithms.
Team-LRN

| 254 |     |     | DatabaseProgramming |
| --- | --- | --- | ------------------- |
PROBLEMS
| 1. What | is a collection?      |               |                          |
| ------- | --------------------- | ------------- | ------------------------ |
| 2. How  | does a collection     | differ from   | an array?                |
| 3. What | are common            | types of data | corruption?              |
| 4. What | are some techniques   | for           | scanning for dirty data? |
| 5. What | is the CollectionBase | class?        |                          |
Team-LRN

| IntroductiontoDataStructures |     |      |     |     |     |     |     | 255 |
| ---------------------------- | --- | ---- | --- | --- | --- | --- | --- | --- |
| PROJECT                      |     | 14.1 |     |     |     |     |     |     |
In the DirtyFinance.mdb database, the IBM table contains missing
data. Create a VB.NET Windows application that finds the three
| bad entries | and      | deletes | them    | from | the database. |        |                |     |
| ----------- | -------- | ------- | ------- | ---- | ------------- | ------ | -------------- | --- |
| To          | complete | this    | project | you  | will need     | to use | the IsDBNull() |     |
function. The IsDBNull() function returns True or False indicating
whetheragivenobjectisoftypeSystem.DBNull.ASystem.DBNull
object represents missing data in a data set. As may be intuitively
deduced,missingdataisnotheldasaNothingvalue,norisitheld
| as a string | with | no value | such | as  | “”. |     |     |     |
| ----------- | ---- | -------- | ---- | --- | --- | --- | --- | --- |
| PROJECT     |      | 14.2     |      |     |     |     |     |     |
The MRK table in the DirtyFinance.mdb database is rife with bad
| data, including |     | bad | and | missing | data | points, bad | dates, | and |
| --------------- | --- | --- | --- | ------- | ---- | ----------- | ------ | --- |
column-shifted data. Create a DTMS to find the bad data. Also,
allowtheusertoviewthebaddataandeitherupdateitordeleteit.
Team-LRN

This page intentionally left blank.
Team-LRN

| C H      | A P T E | R 15 |            |     |
| -------- | ------- | ---- | ---------- | --- |
| Advanced |         | Data | Structures |     |
T
| he System.Collections |     | namespace | contains several | classes for |
| --------------------- | --- | --------- | ---------------- | ----------- |
collections of objects. These Collection classes differ from the
Collection class we discussed in Chapter 14. Notice, however, the
inclusioninthisnamespaceoftheCollectionBase,whichwelooked
at briefly in the previous chapter. Here is a list of the Collection
| classes in | the System.Collections | namespace: |     |     |
| ---------- | ---------------------- | ---------- | --- | --- |
System.Collections
| NamespaceClasses |     |                                       | Description |     |
| ---------------- | --- | ------------------------------------- | ----------- | --- |
| ArrayList        |     | Anarraywhosesizeisdynamic             |             |     |
| BitArray         |     | Acompactarrayofbitvaluesrepresentedas |             |     |
Booleans
CaseInsensitiveComparer Comparestwononstringobjectsforequivalence
CaseInsensitiveHashCodeProvider Suppliesahashcodeforanonstringobject
| CollectionBase |     | Theabstractbaseclassforacollection  |     |     |
| -------------- | --- | ----------------------------------- | --- | --- |
| Comparer       |     | Comparestwoobjectsforcase-sensitive |     |     |
equivalence
| DictionaryBase |     | Thebaseclassforacollectionofkey-and-value |     |     |
| -------------- | --- | ----------------------------------------- | --- | --- |
pairs
| Hashtable |     | Acollectionofkey-and-valuepairsorganizedby |     |     |
| --------- | --- | ------------------------------------------ | --- | --- |
hashcode
| Queue |     | Afirst-in,first-outcollectionofobjects |     |     |
| ----- | --- | -------------------------------------- | --- | --- |
ReadOnlyCollectionBase Theabstractbaseclassforaread-onlycollection
| SortedList |     | Acollectionofkey-and-valuepairsthataresorted |     |     |
| ---------- | --- | -------------------------------------------- | --- | --- |
bykeyandareaccessiblebybothkeyand
index
| Stack           |             | Alast-in,first-outcollectionofobjects |                   |             |
| --------------- | ----------- | ------------------------------------- | ----------------- | ----------- |
| Structure       |             |                                       | Description       |             |
| DictionaryEntry |             | Definesadictionarykey-and-valuepair   |                   |             |
| We will         | not discuss | fully each                            | of these classes. | However, we |
will illustrate a hash table and leave it to the reader to investigate
257
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

| 258 |     |     |     | DatabaseProgramming |
| --- | --- | --- | --- | ------------------- |
the various members of each of the classes should the need for
themarise.Fornow,beawarethattheyexist,andunderstandtheir
| differing | descriptions. |     |     |     |
| --------- | ------------- | --- | --- | --- |
| HASH      | TABLES        |     |     |     |
A hash table is a collection of key-and-value pairs based upon the
hash code of the element’s key. Each element is then stored in a
DictionaryEntry object. Because of the way they are constructed,
hashtablesallowforspeedyretrievalofelementsinthehashtable.
Whenanapplicationneedstostoreelements,itcreatesaschemeto
converttheelement’skeyvaluetoasubscript,whichthenbecomes
the location of that object in the collection. To retrieve the object
then,theprogramconvertsthekeyvalueusingthesameschemeto
find and return the object from its location. This process is called
hashing.
| When | we convert | a key | to an index value, | we are scrambling |
| ---- | ---------- | ----- | ------------------ | ----------------- |
thebits.Problemscanarise,however,whentwodifferentkeyshash
into the same element in an array. Since we certainly cannot store
two different records in the same location, we need to find an
alternativelocationviasomemethod.TheVB.NETHashtableclass
solves this problem by having each cell of the hash table be a
bucket, which is a collection of all the key-value pairs that hash to
thatcell. Thisentireprocess isinvisibleto ussincethehashtable’s
hashingfunctioncalculateswheretoputthevalueinthehashtable.
This function is applied to the key of the key-value pair of objects.
By using this process, any object can be added to a hash table.
| The | VB.NET | Hashtable | class implements | the IDictionary, |
| --- | ------ | --------- | ---------------- | ---------------- |
ICollection, IEnumerable, ISerialization, IDeserializationCallback,
and ICloneable interfaces. As a result, there are several member
| variables, | properties, | and | methods associated | with Hashtable |
| ---------- | ----------- | --- | ------------------ | -------------- |
objects. Some of the more important members to be aware of are:
Public
| Constructor |                       |     | Description |     |
| ----------- | --------------------- | --- | ----------- | --- |
| Constructor | Initializesahashtable |     |             |     |
Public
| Properties |                                                |     | Description |     |
| ---------- | ---------------------------------------------- | --- | ----------- | --- |
| Count      | Returnsthenumberofelementsinthehashtable       |     |             |     |
| Item       | Returnsorsetsthevalueofanelementinthehashtable |     |             |     |
Team-LRN

| AdvancedDataStructures |     |     |     |     |     |     | 259 |
| ---------------------- | --- | --- | --- | --- | --- | --- | --- |
Public
| Properties |                                                     |     |     | Description |     |     |     |
| ---------- | --------------------------------------------------- | --- | --- | ----------- | --- | --- | --- |
| Keys       | Returnsacollectioncontainingthekeysinthehashtable   |     |     |             |     |     |     |
| Values     | Returnsacollectioncontainingthevaluesinthehashtable |     |     |             |     |     |     |
Public
| Methods |                                    |     |     | Description |     |     |     |
| ------- | ---------------------------------- | --- | --- | ----------- | --- | --- | --- |
| Add     | Addsanelementtothehashtable        |     |     |             |     |     |     |
| Clear   | Deletesallelementsfromthehashtable |     |     |             |     |     |     |
ContainsKey Determineswhetherthehashtablecontainsaspecifickey
ContainsValue Determineswhetherthehashtablecontainsaspecificvalue
CopyTo Copiestheelementsofthehashtablestoaone-dimensionalarray
| Equals | Determineswhethertwoobjectsareequal |     |     |     |     |     |     |
| ------ | ----------------------------------- | --- | --- | --- | --- | --- | --- |
GetEnumerator ReturnsanIDictionaryEnumeratorthatcaniteratethroughthehash
table
| Remove | Deletesasingleelementfromthehashtable |     |     |     |     |     |     |
| ------ | ------------------------------------- | --- | --- | --- | --- | --- | --- |
Protected
| Methods   |                                                |     |     | Description |     |     |     |
| --------- | ---------------------------------------------- | --- | --- | ----------- | --- | --- | --- |
| GetHash   | Returnsthehashcodeforaspecifiedkey             |     |     |             |     |     |     |
| KeyEquals | Comparesanobjectwithaspecifickeyinthehashtable |     |     |             |     |     |     |
Sincetheelementsofahashtablemaybeofdifferenttypes,we
| can loop               | through  | the | elements | in         | a hash | table using | an      |
| ---------------------- | -------- | --- | -------- | ---------- | ------ | ----------- | ------- |
| IDictionaryEnumerator. |          |     | Here is  | an example |        | from the    | program |
| presented              | later in | the | chapter: |            |        |             |         |
Dim enumerator As IDictionaryEnumerator = myPortfolio.GetEnumerator()
| txtPortfolio.Text |                       | =   | "PORTFOLIO                   | ELEMENTS:" | & vbCrLf |              |      |
| ----------------- | --------------------- | --- | ---------------------------- | ---------- | -------- | ------------ | ---- |
| While             | enumerator.MoveNext() |     |                              |            |          |              |      |
|                   | txtPortfolio.Text     |     | += enumerator.Value.ToString |            |          | & vbCrLf     |      |
| End               | While                 |     |                              |            |          |              |      |
| An                | IDictionaryEnumerator |     |                              | itemizes   |          | the elements | of a |
DictionaryEntryobject.Whenanenumeratoriscreated,itsposition
isbeforethefirstelementinthedictionary.Asaresult,wemustcall
theMoveNext()methodinordertoadvancetothefirstelement.We
can then use the Current() property or the Value() property to
retrieve the element at which the enumerator is positioned. And
thenwecancallMoveNext()anditeratethroughalltheelementsin
thehashtable.Iftheenumeratorrunsofftheendofthehashtable,
theMoveNext()methodwillsimplyreturnafalsevalue.Sowecan
loopwhileMoveNext()isTrue,asintheexampleshownabove.An
enumerator will be invalidated if changes are made to the hash
Team-LRN

260 DatabaseProgramming
table while it is being used. Here are the key properties and
methods of an IDictionaryEnumerator:
Public
Properties Description
Current Retrievesthecurrentelementinthedictionary
Entry Returnsboththekeyandthevalueofthecurrentdictionaryentry
Key Returnsthekeyofthecurrentdictionaryentry
Value Retrievesthecurrentelementinthedictionary
Public
Methods Description
MoveNext Movestheenumeratortothenextelementinthedictionary
Reset Movestheenumeratortothepositionbeforethefirstelement
Now let’s use a hash table to create a robust portfolio object
with a great deal more functionality than the one using the
Collection class that we looked at in the previous chapter.
Step 1 Open a new Windows application named Portfolio.
Step 2 Create the GUI shown in Figure 15.1.
Step 3 On your GUI, there should be seven text boxes. In
the Properties windows, rename these controls
txtSymbol, txtQuantity, txtStockPrice, txtVolatility,
txtDelta, txtPortfolio, and txtPortStatus. The large
text box in the middle, txtPortfolio, should have
the multiline property set to True and the scroll
bar property set to Vertical. Also on your GUI,
there should be a combo box. Rename this combo
box cboCallPut. There should be eight buttons
on your form. Rename these controls cmdBuy,
cmdSell, cmdGetMeOut, cmdContains, cmdIs-
Empty, cmdRetrieve, cmdCompute Delta, and
cmdListKeys, respectively.
Step 4 Now to add some code. Add a reference to
Options.dll and Import Options as well as
System.Collections at the top of your Form1 code
window.
Imports System.Collections
Imports Options
Team-LRN

| AdvancedDataStructures |                                                 |        |       |           |     |        | 261   |
| ---------------------- | ----------------------------------------------- | ------ | ----- | --------- | --- | ------ | ----- |
| F I G U                | R E                                             | 15.1   |       |           |     |        |       |
| Step                   | 5 InthegeneraldeclarationssectionoftheForm1code |        |       |           |     |        |       |
|                        | window,                                         | create | a new | Hashtable |     | object | named |
myPortfolio.
|      |       | Dim myPortfolio |      | As New | Hashtable()      |     |       |
| ---- | ----- | --------------- | ---- | ------ | ---------------- | --- | ----- |
| Step | 6 Add | the following   | code | to     | the cmdBuy_Click |     | event |
subroutine:
Private Sub cmdBuy_Click(ByVal sender As ...) Handles cmdBuy.Click
|     | Dim intOptionQuantity |                                       | As Integer       | = txtQuantity.Text         |     |         |      |
| --- | --------------------- | ------------------------------------- | ---------------- | -------------------------- | --- | ------- | ---- |
|     | Dim strSymbol         | As String                             | = txtSymbol.Text |                            |     |         |      |
|     | If cboCallPut.Text    |                                       | = "CALL" Then    |                            |     |         |      |
|     |                       | If myPortfolio.ContainsKey(strSymbol) |                  |                            |     | = False | Then |
|     |                       | Dim myOption                          | As New           | CallOption(txtSymbol.Text, |     |         | _    |
intOptionQuantity)
|     |     | myPortfolio.Add(strSymbol, |     |     | myOption) |     |     |
| --- | --- | -------------------------- | --- | --- | --------- | --- | --- |
Else
|     |     | myPortfolio(strSymbol).Quantity    |     |     | +=  | intOptionQuantity |     |
| --- | --- | ---------------------------------- | --- | --- | --- | ----------------- | --- |
|     |     | If myPortfolio(strSymbol).Quantity |     |     |     | = 0 Then          | _   |
myPortfolio.Remove(strSymbol)
End If
Else
|     |     | If myPortfolio.ContainsKey(strSymbol) |        |                           |     | = False | Then |
| --- | --- | ------------------------------------- | ------ | ------------------------- | --- | ------- | ---- |
|     |     | Dim myOption                          | As New | PutOption(txtSymbol.Text, |     |         | _    |
intOptionQuantity)
Team-LRN

| 262 |                            |     |     | DatabaseProgramming |     |     |
| --- | -------------------------- | --- | --- | ------------------- | --- | --- |
|     | myPortfolio.Add(strSymbol, |     |     | myOption)           |     |     |
Else
|     | myPortfolio(strSymbol).Quantity() |                                 |     | +=  | intOptionQuantity |     |
| --- | --------------------------------- | ------------------------------- | --- | --- | ----------------- | --- |
|     | If                                | myPortfolio(strSymbol).Quantity |     | =   | 0 Then            | _   |
myPortfolio.Remove(strSymbol)
End If
|     | End If |     |     |     |     |     |
| --- | ------ | --- | --- | --- | --- | --- |
ListPortfolioElements()
End Sub
Several things are going on in this routine. First of all, the
symbol and quantity are read into variables. Second, the code
distinguishesbetweencallandput.IfCallisselectedinthecombo
box, a CallOption is added to myPortfolio. Likewise, if Put is
selected, a PutOption object is added. Before either one is added,
however,theprogramcheckstoseeifthatparticularoptionalready
exists in myPortfolio using the myPortfolio.ContainsKey(strSym-
bol)memberfunction.IfmyPortfolioalreadycontainsapositionin
thatoption,itsimplyincrementsthequantityofthecurrentposition.
If there is no current position in that option in myPortfolio, then it
creates the new CallOption or PutOption object and adds it to
myPortfolio. Third and last, the procedure calls the ListPortfolio-
Elements()subroutine,whichwewilllookatshortly.
| Step | 7 Add the    | following  | code for      | the cmdSell_Click |         | event     |
| ---- | ------------ | ---------- | ------------- | ----------------- | ------- | --------- |
|      | subroutine.  | The        | cmdSell_Click | event             | routine | is the    |
|      | same as      | the cmdBuy | routine       | except            | that it | subtracts |
|      | the quantity | rather     | than adds     | it.               |         |           |
Private Sub cmdSell_Click(ByVal sender As ...) Handles cmdSell.Click
| Dim intOptionQuantity |                                       | As Integer       | = txtQuantity.Text         |         |      |     |
| --------------------- | ------------------------------------- | ---------------- | -------------------------- | ------- | ---- | --- |
| Dim strSymbol         | As String                             | = txtSymbol.Text |                            |         |      |     |
| If cboCallPut.Text    |                                       | = "CALL"         | Then                       |         |      |     |
|                       | If myPortfolio.ContainsKey(strSymbol) |                  |                            | = False | Then |     |
|                       | Dim myOption                          | As New           | CallOption(txtSymbol.Text, |         | _    |     |
-intOptionQuantity)
|     | myPortfolio.Add(strSymbol, |     | myOption) |     |     |     |
| --- | -------------------------- | --- | --------- | --- | --- | --- |
Else
|     | myPortfolio(strSymbol).Quantity    |     |     | -= intOptionQuantity |     |     |
| --- | ---------------------------------- | --- | --- | -------------------- | --- | --- |
|     | If myPortfolio(strSymbol).Quantity |     |     | = 0 Then             | _   |     |
myPortfolio.Remove(strSymbol)
|     | End If |     |     |     |     |     |
| --- | ------ | --- | --- | --- | --- | --- |
Else
|     | If myPortfolio.ContainsKey(strSymbol) |        |                           | = False | Then |     |
| --- | ------------------------------------- | ------ | ------------------------- | ------- | ---- | --- |
|     | Dim myOption                          | As New | PutOption(txtSymbol.Text, |         | _    |     |
-intOptionQuantity)
|     | myPortfolio.Add(strSymbol, |     | myOption) |     |     |     |
| --- | -------------------------- | --- | --------- | --- | --- | --- |
Team-LRN

AdvancedDataStructures 263
Else
myPortfolio(strSymbol).Quantity()-=intOptionQuantity
|     | If  | myPortfolio(strSymbol).Quantity |     |     |     | = 0 Then _ |
| --- | --- | ------------------------------- | --- | --- | --- | ---------- |
myPortfolio.Remove(strSymbol)
End If
|     | End If |     |     |     |     |     |
| --- | ------ | --- | --- | --- | --- | --- |
ListPortfolioElements()
End Sub
|     | Step 8 Add | the | following |     | code to | the cmdRetrieve_Click |
| --- | ---------- | --- | --------- | --- | ------- | --------------------- |
event:
Private Sub cmdRetrieve_Click(ByVal sender As ...) Handles cmdRetrieve.Click
|     | Dim strSymbol       | As String | =          | txtSymbol.Text           |                             |     |
| --- | ------------------- | --------- | ---------- | ------------------------ | --------------------------- | --- |
|     | Dim resultOption    | As        | Object     | = myPortfolio(strSymbol) |                             |     |
|     | If Not resultOption |           | Is Nothing | Then                     |                             |     |
|     | txtPortStatus.Text  |           | =          | "Retrieved:              | " & resultOption.ToString() |     |
Else
txtPortStatus.Text = txtSymbol.Text & " not in the Portfolio."
|     | End If |     |     |     |     |     |
| --- | ------ | --- | --- | --- | --- | --- |
ListPortfolioElements()
End Sub
ThecmdRetrieve_Clickeventfindsthespecificelementwithin
myPortfolio,ifitexists.Inthisexample,wearejustprintingoutina
textboxthefactthatitwasfound.Inmoresophisticatedproduction
| programs | and systems, |     | we would |     | probably | want to do something |
| -------- | ------------ | --- | -------- | --- | -------- | -------------------- |
more important.
|     | Step 9 Add | the | following |     | code to | the cmdIsEmpty_Click |
| --- | ---------- | --- | --------- | --- | ------- | -------------------- |
event:
Private Sub cmdIsEmpty_Click(ByVal sender As ...) Handles cmdIsEmpty.Click
|     | If myPortfolio.Count |     | = 0 | Then       |            |     |
| --- | -------------------- | --- | --- | ---------- | ---------- | --- |
|     | txtPortStatus.Text   |     | =   | "Portfolio | is empty." |     |
Else
|     | txtPortStatus.Text |     | =   | "Portfolio | is not | empty." |
| --- | ------------------ | --- | --- | ---------- | ------ | ------- |
|     | End If             |     |     |            |        |         |
ListPortfolioElements()
End Sub
This event simply uses the myPortfolio.Count method, as you can
see. The simplicity of using System.Collections classes is what
| makes | them so     | powerful. |           |     |         |                       |
| ----- | ----------- | --------- | --------- | --- | ------- | --------------------- |
|       | Step 10 Add | the       | following |     | code to | the cmdContains_Click |
event:
Private Sub cmdContains_Click(ByVal sender As ...) Handles cmdContains.Click
|     | Dim strSymbol | = txtSymbol.Text |     |     |     |     |
| --- | ------------- | ---------------- | --- | --- | --- | --- |
txtPortStatus.Text="Contains:"&myPortfolio.ContainsKey(strSymbol)
End Sub
Team-LRN

264 DatabaseProgramming
This subroutine simply calls the ContainsKey() method of
myPortfolioto checkand seewhethera specificelementis present
in the library. The ContainsKey() method returns a Boolean.
Step 11 AddthefollowingcodetothecmdGetMeOut_Click
event:
Private Sub cmdGetMeOut_Click(ByVal sender As ...) Handles cmdGetMeOut.Click
myPortfolio.Clear()
txtPortStatus.Text = "You are out. Portfolio is now empty."
ListPortfolioElements()
End Sub
The cmdGetMeOut_Click event calls the Clear() method of the
HashtableobjectmyPortfolio,whichremovesalltheelementsfrom
the library.
Step 12 Add the following code to the cmdListKeys_Click
event:
Private Sub cmdListKeys_Click(ByVal sender As ...) Handles cmdListKeys.Click
Dim enumerator As IDictionaryEnumerator = myPortfolio.GetEnumerator()
txtPortfolio.Text = "PORTFOLIO KEYS:" & vbCrLf
While enumerator.MoveNext()
txtPortfolio.Text += enumerator.Key & vbCrLf
End While
End Sub
HereweseetheIDictionaryEnumeratoratwork,aswediscussedin
the example.
Step 13 Add the following code for the ListPortfolio-
Elements() subroutine:
Private Sub ListPortfolioElements()
Dim enumerator As IDictionaryEnumerator = myPortfolio.GetEnumerator()
txtPortfolio.Text = "PORTFOLIO ELEMENTS:" & vbCrLf
While enumerator.MoveNext()
txtPortfolio.Text += enumerator.Value.ToString & vbCrLf
End While
End Sub
Here again we see the IDictionaryEnumerator at work calling the
ToString() method of each successive enumerator.Value.
Step 14 AddthefollowingcodefortheComputeDelta_Click
event:
Private Sub ComputeDelta_Click(ByVal sender As ...) Handles _
ComputeDelta.Click
Dim enumerator As IDictionaryEnumerator = myPortfolio.GetEnumerator()
Team-LRN

AdvancedDataStructures 265
| Dim myDelta                   | As Double | = 0                       |     |
| ----------------------------- | --------- | ------------------------- | --- |
| While enumerator.MoveNext()   |           |                           |     |
| enumerator.Value.StockPrice() |           | = Val(txtStockPrice.Text) |     |
| enumerator.Value.Volatility() |           | = Val(txtVolatility.Text) |     |
myDelta += (enumerator.Value.Quantity * enumerator.Value.Delta)
| End While     |                  |                |     |
| ------------- | ---------------- | -------------- | --- |
| txtDelta.Text | = Format(myDelta | * 100, "#.00") |     |
End Sub
The portfolio delta calculation takes the individual option deltas
times the number of contracts times 100 shares per contract to
| arrive at a portfolio | delta.          |             |        |
| --------------------- | --------------- | ----------- | ------ |
| Step 15               | Run the program | (see Figure | 15.2). |
| F I G U R             | E 15.2          |             |        |
SUMMARY
In this brief chapter we have illustrated the use of a Hashtable
object. Several classes, including hash tables, are defined in the
| System.Collections | namespace. | As you | have seen, implementing |
| ------------------ | ---------- | ------ | ----------------------- |
Team-LRN

| 266 |     |     | DatabaseProgramming |     |
| --- | --- | --- | ------------------- | --- |
collection objects greatly reduces the complexity of dealing with
multipleobjectsofsimilarorevendifferenttypes.Inalaterchapter
we will create VB.NETapplications that simulate placing buy and
sell orders on real derivatives markets. As trades are “executed,”
| you should | think about | how you can | manage your | portfolio of |
| ---------- | ----------- | ----------- | ----------- | ------------ |
positions as a collection of objects. This will make the jump to
| calculating | portfolio hedge | ratios rather | simple. |     |
| ----------- | --------------- | ------------- | ------- | --- |
Team-LRN

AdvancedDataStructures 267
PROBLEMS
| 1. What | is a  | hash table?            |         |     |     |     |     |
| ------- | ----- | ---------------------- | ------- | --- | --- | --- | --- |
| 2. What | are   | Queues and             | Stacks? |     |     |     |     |
| 3. What | is an | IDictionaryEnumerator? |         |     |     |     |     |
4. ThepropertiesofaCallOptiondifferfromthefieldsin
| the OptionTrades |     |           | and OptionContracts |            |      | tables     | in the |
| ---------------- | --- | --------- | ------------------- | ---------- | ---- | ---------- | ------ |
| Options.mdb      |     | database. | The                 | process    | of   | converting | the    |
| information      |     | in an     | object              | to another | data | structure  | is     |
calledmapping.HowcouldwemapanOptionTrades
recordinthedatabaseintoaCallOptionorPutOption
object?
| 5. If our  | portfolio |             | consisted | of  | options | on    | several |
| ---------- | --------- | ----------- | --------- | --- | ------- | ----- | ------- |
| different  |           | stocks, how | could     | we  | keep    | track | of the  |
| respective |           | deltas?     |           |     |         |       |         |
Team-LRN

| 268          |     |     | DatabaseProgramming |
| ------------ | --- | --- | ------------------- |
| PROJECT 15.1 |     |     |                     |
The Windows application presented in the chapter example uses
user inputs for stock price and volatility. Create a new VB.NET
program that provides the same functionality, but connects to the
Options.mdb database to retrieve the current bid as the stockprice
andconnectstotheFinance.mdbdatabasetocalculatethehistorical
volatility. You may use whatever time period you like to calculate
volatility.
| PROJECT 15.2    |           |                      |               |
| --------------- | --------- | -------------------- | ------------- |
| The Options.mdb | databased | contains information | about several |
OptionTrades.Usethistabletopopulateaportfolioobjectasinthe
chapter example.
Team-LRN

| S E C    | T I O N | F O U R |     |
| -------- | ------- | ------- | --- |
| Advanced |         | VB.NET  |     |
Implementation
| The | world hates | change,yet it istheonlything | that has |
| --- | ----------- | ---------------------------- | -------- |
broughtprogress.
CharlesF.Kettering
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

This page intentionally left blank.
Team-LRN

| C        | H A P T | E R | 16           |     |     |     |     |
| -------- | ------- | --- | ------------ | --- | --- | --- | --- |
| Software |         |     | Connectivity |     |     | and |     |
Interoperability
A
srecentlyas1990,theideaofautomatedtradeexecutionwasfor
| the most   | part inconceivable. |      | But        | today automated |     | systems       | and |
| ---------- | ------------------- | ---- | ---------- | --------------- | --- | ------------- | --- |
| electronic | exchanges           | have | completely | redefined       |     | the industry. |     |
Withoutsophisticatedtechnology,modernfinancialmarketswould
ceasetoexist.Todayglobalmarketsandglobaltradingneverstop.
Opportunities come and go quickly, and trades must be sent in
milliseconds. Securities and derivatives transactions have become
| instantaneous | and | inexpensive. | As  | technology | has | evolved | and |
| ------------- | --- | ------------ | --- | ---------- | --- | ------- | --- |
will continue to evolve, it will completely redefine the tasks of
traders.Theonlywayfortradersandfirmstosurvivetradinginthe
financial markets is through ever-better understanding of market
processesandtheuseofever-fastertechnology.Yesterday’strading
ideas and technologies fade quickly. In the twenty-first century,
real-time data is simply a raw material. Successful traders and
trading firms will be the ones that develop the technological and
analytic infrastructure to transform data into knowledge and then
| into action | and then       | into | continuously | improving     | processes. |      |     |
| ----------- | -------------- | ---- | ------------ | ------------- | ---------- | ---- | --- |
| The         | rapid increase |      | in the use   | of technology | has        | made | the |
trading of securities and derivatives more pervasive. It has freed
| markets | and exchanges |     | from their | geographic | boundaries |     | and |
| ------- | ------------- | --- | ---------- | ---------- | ---------- | --- | --- |
stimulated globalization. As more companies and instruments are
listed for trading on electronic markets around the world, traders
and trading firms will increasingly be seeking to get connected
usinglegacysoftwareandhardwareill-suitedforthejob,giventhe
| number | and complexity |     | of connections | that will | be needed. |     |     |
| ------ | -------------- | --- | -------------- | --------- | ---------- | --- | --- |
271
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

| 272 |     |     |     |     |     | AdvancedVB.NET |     |     |
| --- | --- | --- | --- | --- | --- | -------------- | --- | --- |
Whateverthefutureholds,onethingisforsure:Theabilityof
exchanges and trading firms to survive depends on the quality of
their technology. The proliferation of live market feeds and the
resulting tidal wave of data are increasing the complexity of the
| trading | selection | process |     | and the | architecture |     | of trading |     |
| ------- | --------- | ------- | --- | ------- | ------------ | --- | ---------- | --- |
technology. The new paradigm will necessitate open systems and
application programming interfaces for connectivity and inter-
| operation. | In other   | words, | the       | future lies | in middleware. |              |         |     |
| ---------- | ---------- | ------ | --------- | ----------- | -------------- | ------------ | ------- | --- |
| Middleware |            | is a   | computing | model       | that offers    | institutions |         | a   |
| means      | to embrace | the    | future    | of trading  | technology     |              | without |     |
destroying the foundation of systems created in the past. Large
trading institutions often incorporate several disparate legacy
systems for their front, middle, and back office, and as we will be
able to see, the goals of straight-through processing (STP) and
firmwide risk management are and will be severely hindered by
| the use | of multiple | systems. | Middleware |     | provides | a solution. |     |     |
| ------- | ----------- | -------- | ---------- | --- | -------- | ----------- | --- | --- |
Throughtheuseofmiddleware,ourtradingsystemscanhave
the ability to back-test trading systems against historical data,
assimilate real-time market information from a multiplicity of
| sources, | perform | complex |     | quantitative | calculations, |     | scan | the |
| -------- | ------- | ------- | --- | ------------ | ------------- | --- | ---- | --- |
markets for profitable opportunities, place buy and sell orders
automatically,andmanageaportfolioofpositionandmonitorrisk.
| Through                                 | network  | connectivity |               | and | interoperation     | of  | software |     |
| --------------------------------------- | -------- | ------------ | ------------- | --- | ------------------ | --- | -------- | --- |
| applications,automatedtradingsystemscan |          |              |               |     | tradeanyinstrument |     |          |     |
| at anytime                              | anywhere |              | in the world. |     |                    |     |          |     |
Whetherwerealizeitornot,virtuallyallsoftwareapplications
make requests to other programs to perform some tasks on their
behalf. To accomplish the goals of market connectivity, of data
transmission between disparate technologies, and of other higher-
level quantitative processes, such as optimization, it will be
necessary for our VB.NET applications to make requests to other
softwaresystemsaswell.Thiswilllargelybedonethroughtheuse
of application programming interfaces and, in the case of data
transmission, XML. Some software applications, including some
electronicexchanges,allowforconnectivityandinteroperationvia
both methods, APIs and XML. We will look at both over the next
fourchapters.EvenwithintheMicrosoftfamilyofvisuallanguages
and even within Visual Basic itself, we will often confront issues
Team-LRN

| SoftwareConnectivityandInteroperability |     |     |     |     |     |     |     |     | 273 |
| --------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
relating to interoperability of systems, particularly in legacy
| systems using |     | Component |             | Object | Model | (COM) | objects.   |     |     |
| ------------- | --- | --------- | ----------- | ------ | ----- | ----- | ---------- | --- | --- |
| APPLICATION   |     |           | PROGRAMMING |        |       |       | INTERFACES |     |     |
In short, a software application’s API defines the proper way for
other applications to interact with and request services from it. In
the trading industry, APIs facilitate the exchange of data between
differentsoftwareapplicationsandwillprovideforinteroperability
| between | financial | industry |     | software |     | packages | and | our | own |
| ------- | --------- | -------- | --- | -------- | --- | -------- | --- | --- | --- |
software built in VB.NET. Through APIs we are able to integrate
multiple commercial off-the-shelf (COTS) software products with
ourownproprietarysoftwaretocreatecustomizedtradingandrisk
managementsystems—andatafractionofthecostofdevelopinga
completesystemfromthegroundup.APIsallowustocreateakind
of middleware that shares data across different trading platforms
and networks. Most, if not all, software packages that you will
encounter as a financial engineer will have APIs that either are a
free bundled part of their software package itself or are separately
| licensed packages |     | available |        | for   | a fee. |         |          |       |     |
| ----------------- | --- | --------- | ------ | ----- | ------ | ------- | -------- | ----- | --- |
| An                | API | is a      | set of | rules | for    | writing | function | calls | or  |
instantiating objects that access function definitions or classes in a
library,usuallyintheformofa.dllfile.Programswecreatethatuse
| these functions |     | or  | classes | can | communicate |     | with | the | COTS |
| --------------- | --- | --- | ------- | --- | ----------- | --- | ---- | --- | ---- |
software to, for example, run an optimization routine, exchange
| information | such | as  | market |     | data | feeds, | process buy | and | sell |
| ----------- | ---- | --- | ------ | --- | ---- | ------ | ----------- | --- | ---- |
transactions,andposttradefillinformationtoadatabase.Oncewe
have created objects based upon the classes in the library, the API
classesdoalltheworkforus,totallytransparenttoourapplication.
In addition to performing data-sharing tasks, APIs usually check
network parameters and error conditions for us so as to deliver
| robust interoperation |     |     | between |      | the programs. |       |       |         |     |
| --------------------- | --- | --- | ------- | ---- | ------------- | ----- | ----- | ------- | --- |
| As opposed            |     | to  | fully   | open | source        | code, | which | exposes | the |
software maker’s proprietary methods, APIs represent a stream-
lined way to grant access to an application without giving away
intellectual property. APIs grant less access than open source code
| but certainly | more | than | entirely |     | closed | software. |     |     |     |
| ------------- | ---- | ---- | -------- | --- | ------ | --------- | --- | --- | --- |
Team-LRN

274 AdvancedVB.NET
Among financial markets COTS software, APIs exist in many
different forms. You should fully understand the implementation
oftheAPI,containedinthesoftwarevendor’sAPIdocumentation,
before you proceed.
EXCHANGE APPLICATION PROGRAMMING
INTERFACES
The major exchanges all have APIs to which developers can write
to create market data feed and order routing applications. Writing
to an exchange API, or alternatively to the FIX interface, and
building proprietary software from the ground up requires a
healthyamountofresearch,time,andmoney.Aswasdiscussedin
Chapter 1, for most small firms this is not a feasible option for
building automated trading systems. However, we can gain a
somewhat greater understanding of market connectively and
electronic exchange order routing if we briefly look at three
exchange APIs.
The Chicago Board Options Exchange offers an API through
which developers can access the CBOE’s Electronic Trading
System. The CBOE also supports the FIX messages for the
purposes of order routing. This FIX interface is available as an
alternative to connection through the API.
The all-electronic International Securities Exchange (ISE)
offers an API to which member firms can program to access
market data, send trades, and receive trade fill confirmations and
information.ThroughthisAPI,theISE’selectronicaccessmembers
andmarketmakerscandevelopapplicationsforautomatedtrading
purposes or for back-office systems.
The Chicago Mercantile Exchange has the Globex system,
whichcontainsopenAPIsformarketdataandorderroutingsothat
trading firms can write applications to receive real-time market
data from and place automated orders on the CME’s electronic
markets.
As we have seen previously, firms involved in trading on
multiple markets will need to connect to multiple APIs for market
data and order entry. And every exchange API is different.
Furthermore, to add to the complexity, in most cases applications
Team-LRN

SoftwareConnectivityandInteroperability 275
developedtointeractwithanexchange’sAPImustbeapprovedby
the exchange itself. Fortunately several third-party developers
have written customized applications to the respective exchange
APIs for market data and execution of securities, futures, and
optionstrades.WewilllookathowtoconnecttotwooftheseCOTS
software applications in Chapter 17.
COM INTEROPERATION
AswehaveseeninChapter10,inordertocreateVB.NETcodethat
requestsservicesfrom anexternalcomponent,wemustfirstadd a
reference to it. The components can be of the following types:
^ .NETclass libraries
^ COM components
^ XML web services
We have, up till now, looked only at .NET class libraries.
Although the new.NET libraries and assemblies are now a much-
improvedmodelfordevelopment,attimesweneedtomakeuseof
COM objects. .NETapplications may someday replace COM ones,
but until then, if we need to use a COM object in a VB.NET
application, we will need to understand something about COM
itself and how it differs from the .NET Framework.
COM is a Microsoft specification used prior to .NET that
controls library usage and compatibility and communication.
Through COM, objects are exposed and their functionality is
availabletootherapplications.ViaCOM,librariesareensuredtobe
highly organized and reusable. Microsoft defined COM so that
developers could create compatible libraries of classes and
components.VirtuallyallWindowslibrariesthatwereconstructed
prior to the advent of the .NET Framework adhere to the COM
specification, and most software today includes COM objects. But
COM is difficult to program and deploy because developers must
guarantee that new COM components are compatible. If a COM
library is placed on a system without being properly registered,
applications will be unable to find or use the library.
AnunderstandingofCOMinvolvesanunderstandingofhow
COM objects exist in memory. Whereas .NET objects are held in
Team-LRN

276 AdvancedVB.NET
managed memory, which is controlled by CLR (the common
languageruntime),COMobjectsareheldinunmanagedmemory.
The CLR in .NET manages certain tasks such as dynamic memory
allocation and type checking. VB.NETuses managed code, but we
can access the unmanaged COM code using interoperability
assemblies.Manycompanieshaveinvestedsignificantamountsof
time and effort into creating COM components but now find
themselves eager for a migration to .NET. Fortunately Microsoft
createdtoolsforintegratinglegacysystemsandCOMcomponents
into .NET Framework implementations.
The .NET Framework provides fordirect interaction between
objects in managed and unmanaged memory. These tools enable
interoperabilitywithCOMsothatwecanuseexistingCOMobjects
in our VB.NET programs. This process is known within the .NET
Framework as COM interop.
VB.NET uses an interoperability assembly to find COM
methodsandtranslatedatabetweenthe.NETandCOMtypes.This
translation is performed by the run-time callable wrapper (RCW),
whichiscreatedby.NETbasedupontheinformationinanobject’s
interop assembly. As we discussed in Chapter 10, assemblies are
collectionsoffunctionalityusuallyintheformofclassescontained
in one or several files with their assembly manifest. Assembly
manifestsperformthesamefunctionin.NETastypelibrariesdoin
COM components. They include information about version
numbering, constituent files, types and resources, compile-time
dependencies, and permissions.
The RCW controls the COM object and carries out
communication between .NET and COM code. When we create
an instance of a COM object in VB.NET, we are really creating a
new instance of the RCW of the object. Fortunately for VB.NET
developers, the communication between an RCW and its COM
objectiscompletelytransparenttous.Sowecancreateandinteract
with COM objects as if they were .NETobjects. Adding references
to COM objects is the same as in previous incarnations of Visual
Basicexceptthat.NETaddsthecreationofthisinteropassemblyto
theprocess.ReferencestotheCOMobjectpropertiesandmethods
inVB.NETareroutedtotheinteropassemblypriortoproceedingto
theactualCOMobjectcode.Onthewayback,responsesarerouted
Team-LRN

SoftwareConnectivityandInteroperability 277
first to the interop assembly and before being forwarded back to
calling code in .NET.
Should the need arise, we can create new COM objects in
VB.NET by using the .NET Framework’s COM class template,
which can create a new class and configures the project so as to
generate the COM class and register it with the operating system.
COMobjectsreferencedviainteropassembliesmustberegistered,
which we accomplish by using the Regsvr32 utility included with
allWindowsoperatingsystems.IfyouarefamiliarwithVB6.0,you
are aware that ActiveX controls are commonly used COM
components.Throughtheinteropassembly,wecanimportActiveX
controls into our .NET IDE toolbox using the Customize Toolbox
option, whichwill list alltheCOM componentsthat areregistered
with the operating system. We are then free to use the ActiveX
control in our VB.NETapplication. .NET Framework components
donotneedtoberegisteredsince.NETcomponentsmaintainallof
their type identification information internally.
In Visual Basic .NET, adding references to COM objects that
have type libraries is similar to doing so in previous versions of
Visual Basic. However, Visual Basic .NETadds the creation of an
interop assembly to the procedure. References to the members of
the COM object are routed to the interop assembly and then
forwarded to the actual COM object. Responses from the COM
object are routed to the interop assembly and forwarded to your
.NET application. If, for example, the input argument and return
valuesofaCOMobject’spropertiesandmethodsusedifferentdata
typesthan.NETdoes,aprocesscalledinteropmarshalingconverts
equivalent data types as they flow back and forth between COM
objects.Infactall.NETprogramsshareasetofcommontypesthat
permit interoperability of objects, regardless of the programming
language.
While COM objects have been the foundation of Visual Basic
applications for many years, .NETapplications designed for CLR
offermanyadvantages.Inthe.NETframework,COMcomponents
are no longer necessary. Through the use of assembly manifests,
.NET components hold on to the benefits of COM while solving
many of its inherent problems.
Team-LRN

| 278 |     |     |     | AdvancedVB.NET |     |
| --- | --- | --- | --- | -------------- | --- |
SUMMARY
| The financial |     | markets          | of the twenty-first | century  | require |
| ------------- | --- | ---------------- | ------------------- | -------- | ------- |
| connectivity  | and | interoperability | of disparate        | hardware | and     |
software systems. The use of APIs and XML will enable software
| we create | in VB.NET | to connect | and exchange | information | with |
| --------- | --------- | ---------- | ------------ | ----------- | ---- |
other systems. Furthermore, even within Visual Basic itself there
areinteroperabilityissuestoconfront,particularlythosepertaining
| to legacy | systems | making | use of COM components. |     |     |
| --------- | ------- | ------ | ---------------------- | --- | --- |
Team-LRN

SoftwareConnectivityandInteroperability 279
PROBLEMS
| 1. What is middleware? |      |     |     |
| ---------------------- | ---- | --- | --- |
| 2. What is an          | API? |     |     |
3. RatherthanconnectingtoexchangeAPIsourselves,whatis
| our alternative | for creating | automated | trading systems? |
| --------------- | ------------ | --------- | ---------------- |
| 4. What is COM? |              |           |                  |
| 5. What is an   | RCW?         |           |                  |
Team-LRN

This page intentionally left blank.
Team-LRN

| C H        | A P T | E R      | 17  |     |     |     |     |
| ---------- | ----- | -------- | --- | --- | --- | --- | --- |
| Connecting |       |          |     | to  |     |     |     |
| Trading    |       | Software |     |     |     |     |     |
A
| n important | problem |            | to solve | when | developing |     | automated     |
| ----------- | ------- | ---------- | -------- | ---- | ---------- | --- | ------------- |
| trading     | or risk | management | systems  |      | is market  |     | connectivity. |
Connecting to live electronic markets is no small task. Millions of
dollars and literally years of time can be spent building such a
systemfromthegroundup.However,wecansubstantiallyreduce
the amount of up-front time and expense needed to establish a
connection to a market by licensing third-party software that
already provides the required functionality. What’s more, most of
| thesesoftwarepackagesalreadyconnectto |     |     |     |     | more | thanonemarket, |     |
| ------------------------------------- | --- | --- | --- | --- | ---- | -------------- | --- |
sometimes dozens of them, around the world enabling traders, or
| financial | engineers, | to be | active | in  | multiple | markets | simul- |
| --------- | ---------- | ----- | ------ | --- | -------- | ------- | ------ |
taneously. More often than not, this kind of third-party software
| will include | an API | that we | can write | to  | in VB.NET. |     |     |
| ------------ | ------ | ------- | --------- | --- | ---------- | --- | --- |
These APIs usually exist in a single .dll library file or a set of
.dllfiles.Theselibrariescontainclassesthatenableustoconnectto
the licensed COTS software. When we create objects based upon
the classes in such a library, wecan use the functionality provided
bytheseobjectstointeractwiththesoftwareandsubsequentlypass
data back and forth. Such functionality might include getting live,
real-time market quotes, placing buy and sell orders, or receiving
| trade fill | confirmations. |      |     |         |      |         |            |
| ---------- | -------------- | ---- | --- | ------- | ---- | ------- | ---------- |
| Rather     | than require   | that | you | license | some | of this | commercial |
softwareyourself,wehaveprovidedtwolibrariesontheCD,called
| Trader API.dll | and | OptionsAPI.dll. |     |     |     |     |     |
| -------------- | --- | --------------- | --- | --- | --- | --- | --- |
281
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

| 282        |     |     |           |     |        | AdvancedVB.NET |     |     |
| ---------- | --- | --- | --------- | --- | ------ | -------------- | --- | --- |
| CONNECTING |     | TO  | A FUTURES |     | MARKET |                |     |     |
The classes in the TraderAPI.dll library allow us to simulate a
connection to a popular industry software package from Trading
Technologies,Inc.,calledX_Trader.TradingTechnologies,Inc.(TT)
developshigh-performancederivativestradingsoftwareincluding
theX_TRADERproduct,whichprovidesprofessionaltraderswith
connectivity to electronic derivatives markets around the world.
Furthermore, the X_TRADER application contains an API consist-
ing of 10 classes that financial engineers can instantiate for the
purposes of developing, among other things, automated analytics,
| order         | entry, and | trade    | fill     | information | processing |     | systems. |     |
| ------------- | ---------- | -------- | -------- | ----------- | ---------- | --- | -------- | --- |
| However,      | you        | do not   | need     | to license  | X_Trader   |     | to use   | the |
| TraderAPI.dll | library    | included |          | on the CD.  |            |     |          |     |
| As            | we said,   | by       | creating | objects     | from       | the | classes  | in  |
TraderAPI.dll, we achieve the goal of market connectivity, albeit
simulated.As a result, a VB.NETprogram that adds a referenceto
TraderAPI.dll and instantiates the objects in it can see the “real-
| time” market | price | movements |     | of the | S&P | 500 eMini | futures |     |
| ------------ | ----- | --------- | --- | ------ | --- | --------- | ------- | --- |
market,canplacemarketbuyandsellorders,andcanreceivetrade
fill confirmations.
TraderAPI.dll can be used to create applications to customize
order entry screens, monitor live fill feeds, perform live profit and
loss calculations, and automatically execute trades based upon
outside conditions and customized algorithms. While providing
only a subset of all the possible functionalities, TraderAPI.dll will
give our programs the look and feel of connecting to real markets
through TT’s X_Trader API. While APIs are always changing and
beingupgraded,wehave,ineverywaypossible,triedtomakethe
| architecture | of TraderAPI.dll |     |     | mimic the | API | that | comes | with |
| ------------ | ---------------- | --- | --- | --------- | --- | ---- | ----- | ---- |
X_TRADER.
| The | TraderAPI.dll |     | file included | with | this | book uses | the | same |
| --- | ------------- | --- | ------------- | ---- | ---- | --------- | --- | ---- |
classes, method calls, and methodology, albeit somewhat abbre-
viated in functionality, as if you were in a real-life environment
using the X_TRADER API. TraderAPI.dll contains five classes that
simulate a portion of the X_TRADER API’s functionality. The five
classes are:
Team-LRN

| ConnectingtoTradingSoftware |     |     |     | 283 |
| --------------------------- | --- | --- | --- | --- |
TraderAPI
| Classes  |                 | Description |     |     |
| -------- | --------------- | ----------- | --- | --- |
| InstrObj | Atradableobject |             |     |     |
InstrNotify MustbeattachedtoanInstrObjsowhentheinstrumentchanges,
messagescanbesent
| OrderProfile | Containsallorderinformationforsubmission |     |     |     |
| ------------ | ---------------------------------------- | --- | --- | --- |
| OrderSet     | Representsasubsetofordersonthismachine   |     |     |     |
| FillObj      | Storesallinformationabouteachfill        |     |     |     |
InstrObj Class
| An InstrObj | object represents | a tradable | object, that | is, an |
| ----------- | ----------------- | ---------- | ------------ | ------ |
instrument. If we want to receive prices or submit orders, we
mustcreateanInstrObjobject.AttachinganInstrNotifyobjecttoan
InstrObjobjectwillallowustoreceivepriceupdatesastheyoccur.
To create an active InstrObj object, we must supply values for the
Exchange, ProdType, Product, and Contract properties. Here are
the public properties and methods associated with the InstrObj
class.
Public
| Properties    |                            | Description |     |     |
| ------------- | -------------------------- | ----------- | --- | --- |
| Contract      | Contractidentifier         |             |     |     |
| Exchange      | Gatewayusedbytheinstrument |             |     |     |
| ProdType      | Producttypeoftheinstrument |             |     |     |
| Product       | Productnameoftheinstrument |             |     |     |
| PublicMethods |                            | Description |     |     |
CreateNotifyObject() Createsanotificationobjectfortheinstrument
| GetData() | Returnsthecurrentvaluesofpropertiesidentifiedby |     |     |     |
| --------- | ----------------------------------------------- | --- | --- | --- |
parameterstring
| Open() | Establishesaconnectiontotheinstrument |       |     |     |
| ------ | ------------------------------------- | ----- | --- | --- |
|        | InstrNotify                           | Class |     |     |
AnInstrNotifyobject,whichisattachedtoanInstrObjobject,alerts
ourapplicationwhensomeaspect,namelytheprice,ofanInstrObj
changes. If we want to monitor a price feed for an instrument,
we must create an InstrNotify object. To create an InstrNotify
object, we must use the InstrObj object’s CreateNotifyObject()
method.
Team-LRN

284 AdvancedVB.NET
| Dim         | myInstrument     | as New InstrObj()                       |             |
| ----------- | ---------------- | --------------------------------------- | ----------- |
| Dim         | myInstrNotifyObj | = New myInstrument.CreateNotifyObject() |             |
| PublicEvent |                  |                                         | Description |
OnNotifyFound() Fireswhenaconnectiontotheinstrumentisestablished
|     | OrderProfile |     | Class |
| --- | ------------ | --- | ----- |
An OrderProfile object contains the information needed for order
submission. An OrderProfile uses an OrderSet object to actually
send an order. The public properties and methods are listed here:
| PublicProperties |                                     |     | Description |
| ---------------- | ----------------------------------- | --- | ----------- |
| BuySell          | Buysorsells                         |     |             |
| GetPrice         | Returnsthepriceofaninstrument       |     |             |
| GetProduct       | Returnstheproductnameofaninstrument |     |             |
| Instrument       | Instrumenttobetraded                |     |             |
| Price            | Orderprice                          |     |             |
| Quantity         | Orderquantity                       |     |             |
| PublicMethods    |                                     |     | Description |
SetTradeParams() Marketordersonly;TraderAPI.dlldoesnotsupportlimitorders
| SetTradeType() | Setsthetradetype |          |       |
| -------------- | ---------------- | -------- | ----- |
|                |                  | OrderSet | Class |
An OrderSet object is used to submit orders. An OrderSet receives
the order information from an OrderProfile object and then sends
| the order.            | Characteristics | include | the following:                    |
| --------------------- | --------------- | ------- | --------------------------------- |
| PublicProperties      |                 |         | Description                       |
| EnableOrderAutoDelete |                 |         | DeletesallordersintheOrderSet     |
| EnableOrderFillData   |                 |         | Returnsallthefillinformation      |
| EnableOrderSend       |                 |         | Orderssendstatus                  |
| PublicMethods         |                 |         | Description                       |
| Open()                |                 |         | Openstheorderset.Defaultisnotopen |
| SendOrder()           |                 |         | Submitsanordertotheexchange       |
| SetLimits()           |                 |         | SetsOrderSetlimits                |
| PublicEvent           |                 |         | Description                       |
| OnOrderFillData()     |                 |         | Fireswhenafillhasbeenreceived     |
Team-LRN

ConnectingtoTradingSoftware 285
FillObj Class
TraderAPIcreatesanewFillObjwhenitisnotifiedofanewfill.The
OrderSet’s OnOrderFillData event will receive a fill object as an
input argument. It’s characterized by this public method:
PublicMethod Description
GetFillInfo() Returnsthecurrentvaluesofthefillobject
In our VB.NET applications, we can add a reference to the
TraderAPI.dllfile,importit,andinstantiateobjectsbaseduponthe
classesinthelibrary.Inthisway,wecan“connecttothemarket”to
get a simulated data feed, place buy and sell orders, and receive
trade fill information. Again, TraderAPI.dll is a stripped-down
versionofTT’sX_TraderAPIandprovidesonlybasicfunctionality,
but it will give you the look and feel of creating real automated
trading software.
Let’screateaprogramthatconnectstothemarketintheeMini
S&P 500 futures contracts traded on the Chicago Mercantile
Exchange.
Step 1 Start a new Windows application named PriceFeed.
Step 2 To your Form1, add five labels in a row.
Step 3 IntheProjectsmenutab,selectAddReference.Select
Browse and find the TraderAPI.dll file. In the code
window, above the class definition for Form1, add:
Imports TraderAPI
Step 4 To get a price feed, we need to set up an InstrObj
object and an InstNotify object. In the general
declarations section of the Form1 code window,
add the following code:
Private WithEvents InstNoti As InstrNotify
Dim Inst1 As InstrObj
Step 5 Also we will need an array of strings to receive the
quote information. Add the code to declare and
instantiate an array of strings in the general
declarations section:
Dim MyData As String() = New String() {}
Team-LRN

286 AdvancedVB.NET
Step 6 In the form load event, add the code to create the
objects and open the connection with the Chicago
Mercantile Exchange for the eMini S&P 500 contract
for December 2003. This will require setting the four
properties of the InstrObj object.
Private Sub Form1_Load(ByVal sender As ...) Handles MyBase.Load
Inst1 = New InstrObj()
InstNoti = Inst1.CreateNotifyObj()
Inst1.Exchange = "CME-S" ’ Setup gateway name
Inst1.Product = "ES" ’ Setup Product name
Inst1.ProdType = "FUTURE" ’ Setup Product type
Inst1.Contract = "Dec03" ’ Setup Expiry information
Inst1.Open() ’ Open/access the instrument
End Sub
Step 7 The InstrNotify object has an event, OnNotify-
Found(), that fires when the price of the instrument
object changes. When this happens, we want to
retrieve the new bid and ask prices, the bid and ask
quantities, and the last price. Add the following
event handler for the OnNotifyFound() event in the
Form1 code window:
Private Sub InstNoti_OnNotifyFound(ByRef pInstr As InstrObj) _
Handles InstNoti.OnNotifyFound
MyData = pInstr.GetData("BidQty,Bid,Ask,AskQty,Last")
Label1.Text = MyData(0)
Label2.Text = MyData(1)
Label3.Text = MyData(2)
Label4.Text = MyData(3)
Label5.Text = MyData(4)
End Sub
Step 8 Run the program. You should see the form window
populated with a simulated moving market—with a
moving bid and offer, moving quantities, and last
prices hitting the bid and offer. See Figure 17.1.
Now let’s add the ability to place some orders and get back
trade fill confirmations.
Step 9 Toplaceorders,wewillneedanOrderSetobjectand
an OrderProfile object. In the general declarations
section of the Form1 code window, add:
Dim WithEvents LiveOrderSet As OrderSet
Dim CurOrdProf As OrderProfile
Team-LRN

| ConnectingtoTradingSoftware |                                            |      |          |     |            |        |        | 287   |
| --------------------------- | ------------------------------------------ | ---- | -------- | --- | ---------- | ------ | ------ | ----- |
| F I G U                     | R E                                        | 17.1 |          |     |            |        |        |       |
| Step 10                     | TotheForm1_Loadevent,addthefollowingcodeto |      |          |     |            |        |        |       |
|                             | create                                     | the  | OrderSet |     | object and | enable | orders | to be |
sent:
|     |     | LiveOrderSet                        |     | = New | OrderSet() |     |        |        |
| --- | --- | ----------------------------------- | --- | ----- | ---------- | --- | ------ | ------ |
|     |     | LiveOrderSet.EnableOrderFillData    |     |       |            |     | = True |        |
|     |     | LiveOrderSet.EnableOrderAutoDelete  |     |       |            |     | =      | False  |
|     |     | LiveOrderSet.SetLimits("NetLimits", |     |       |            |     |        | False) |
|     |     | LiveOrderSet.EnableOrderSend        |     |       |            |     | = True |        |
LiveOrderSet.Open()
| Step 11 | Add        | two    | buttons | to      | your | form. Change  | the           | text |
| ------- | ---------- | ------ | ------- | ------- | ---- | ------------- | ------------- | ---- |
|         | properties |        | to say  | “Buy”   | and  | “Sell,”       | respectively. | In   |
|         | the        | Button | Click   | events, | add  | the following | code:         |      |
Private Sub Button1_Click(ByVal sender As ...) Handles Button1.Click
SendOrder("Buy")
End Sub
Private Sub Button2_Click(ByVal sender As ...) Handles Button2.Click
SendOrder("Sell")
End Sub
| Step 12 | In                                 | the             | form                               | code           | window, | add     | the following |     |
| ------- | ---------------------------------- | --------------- | ---------------------------------- | -------------- | ------- | ------- | ------------- | --- |
|         | subroutine                         |                 | called                             | SendOrder():   |         |         |               |     |
| Private | Sub                                | SendOrder(ByVal |                                    | BuySell        | As      | String) |               |     |
|         | CurOrdProf                         |                 | = New                              | OrderProfile() |         |         |               |     |
|         | Dim                                | intSent         | As Integer                         |                |         |         |               |     |
|         | CurOrdProf.Instrument              |                 |                                    | =              | Inst1   |         |               |     |
|         | CurOrdProf.SetTradeType("M2",      |                 |                                    |                |         | "L")    |               |     |
|         | CurOrdProf.SetTradeParams(BuySell, |                 |                                    |                |         | 1,      | "Market")     |     |
|         | intSent                            | =               | LiveOrderSet.SendOrder(CurOrdProf) |                |         |         |               |     |
|         | CurOrdProf                         |                 | = Nothing                          |                |         |         |               |     |
End Sub
Team-LRN

288 AdvancedVB.NET
The SendOrder() subroutine creates an order profile, sets the
Instrument property, and calls the SetTradeType() and SetTrade-
Params()methods.Inthecodeabove,wearesendingaquantityof
onecontract.Later,whenyoubecomeamoreaccomplishedtrader,
we will allow you to trade larger amounts. Finally, we send the
order by calling the SendOrder() method of the OrderSet object.
Ourmethodofhandlingthetradefillconfirmationsthatcome
back to us from the market will be to simply print them out in a
message box.
Step 13 Add the following subroutine to handle the
OnOrderFillData() event associated with the
OrderSet object:
Private Sub LiveOrderSet_OnOrderFillData(ByRef my FillObj As FillObj) _
Handles LiveOrderSet.OnOrderFillData
Dim strFillData As String()
strFillData = myFillObj.GetFillInfo("Contract,BuySell,NetQty,Price")
MsgBox(strFillData(0) & " " & strFillData(1) & " " & _
strFillData(2) & " @ " & strFillData(3), , "TradeFilled")
End Sub
Step 14 Run the program. The results are shown in Figure
17.2.
On the CD you will find a program named TotalAPI, which
shows the full functionality of the TraderAPI.dll together with a
DataSet and a DataGrid to list trade fill confirmations. In addition
to taking a look at the code, you can feel free to test your trading
acumen using this program.
F I G U R E 17.2
Team-LRN

ConnectingtoTradingSoftware 289
CONNECTING TO AN OPTIONS MARKET
The classes in the OptionsAPI.dll library allow us to simulate a
connection to a popular options industry software package from
MicroHedge, Inc. (MH). MH develops high-end equity options
trading and analytics software that provides professional market
makers and traders with a wealth of high-level option portfolio
analytics and risk management tools. MH’s flexible design, which
includes a robust COM wrapper, enables efficient interoperation
withthird-partysoftwaresystemsliketheonewewillbuildinthis
chapter.Asaresult,tradinginstitutionsoftenuseMicroHedgeasa
foundation on which they create proprietary systems.
With MH’s Screen Based Trading (SBT) software suite,
automated market analysis and order selection are greatly
simplified through the use of its API, which consists of dozens of
classes.Furthermore,SBTuserscansendorderstoanyofthemajor
U.S. options exchanges, the NYSE, and AMEX, as well as several
ECNs. Through the MH software developer’s kit (SDK) and SBT,
market makers create a single software application to autoquote
markets, manage risk, and employ custom models. As another
exampleofSBTflexibility,optionstraderscansetimpliedvolatility
curves with one of twenty different calculations, analyze their
portfolio risk under a multiplicity of “what-if” scenarios, and
monitor the national best bids and offers.
As we discussed in Chapter 1, it is extremely important to
realize that most, if not all, of the options exchanges prohibit
automated order entry in their bylaws. There must be human
intervention and trade approval at some point along the way to
entering an order. We will demonstrate this functionality in the
exampleprogram.Aswiththefuturesexample,youdonotneedto
license MicroHedge software in order to use the OptionsAPI.dll
library included on the CD.
BycreatingobjectsfromtheclassesinOptionsAPI.dll,wecan
achieve the goal of options market connectivity, albeit simulated
andverystrippeddown.Optionsanalyticsrequiresahugepieceof
software, which MicroHedge is, and we will be able to only
demonstrate the simplest functionality. In any case, a VB.NET
program that adds a reference to OptionsAPI.dll and instantiates
the objects in it can monitor “real-time” price movements of the
Team-LRN

| 290 |     |     |     |     |     |     | AdvancedVB.NET |     |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- |
S&P500optionsmarket,canplacemarketbuyandsellorders,and
| can receive    | trade | fill | confirmations. |      |     |      |          |          |
| -------------- | ----- | ---- | -------------- | ---- | --- | ---- | -------- | -------- |
| OptionsAPI.dll |       |      | can be         | used | to  | gain | practice | creating |
applications to customize order entry screens, monitor live fill
feeds, perform live profit and loss calculations, and execute trades
based upon outside conditions and customized algorithms. While
providing only a very small subset of all the possible functional-
ities, OptionsAPI.dll will give our programs the look and feel of
connectingtorealoptionsmarketsthroughMicroHedge’sAPI.The
architecture of OptionsAPI.dll attempts to mimic the SBTAPI that
| you can license |     | from | MicroHedge. |     |     |     |     |     |
| --------------- | --- | ---- | ----------- | --- | --- | --- | --- | --- |
TheOptionsAPI.dllfileincludedwiththisbookusesthesame
classes, method calls, and methodology (although again they are
| abbreviated | in      | functionality) |          | as   | if you    | were     | in             | a real-life |
| ----------- | ------- | -------------- | -------- | ---- | --------- | -------- | -------------- | ----------- |
| environment | using   | the            | MH SBT   | API. | As        | we said, | OptionsAPI.dll |             |
| contains    | classes | that           | simulate |      | a portion |          | of the         | SBT API’s   |
functionality. Here are the classes included in the OptionsAPI.dll
file:
| OptionsAPIClasses |        |     |               |     |                                 |     | Description |        |
| ----------------- | ------ | --- | ------------- | --- | ------------------------------- | --- | ----------- | ------ |
| MicroHedge        |        |     |               |     | AninstanceofMicroHedge          |     |             |        |
| MHSBT             |        |     |               |     | AninstanceofScreen-BasedTrading |     |             |        |
| CBOEorder         |        |     |               |     | ACBOEoptionorder                |     |             |        |
| IndexOp           |        |     |               |     | Anindexoptioninstrument         |     |             |        |
| MHposition        |        |     |               |     | ApositioninMicroHedge           |     |             |        |
| In our            | VB.NET |     | applications, |     | we can                          | add | a reference | to the |
OptionsAPI.dll file, import it, and instantiate objects based upon
theclassesinthelibrary.Inthiswaywecan“connecttothemarket”
to monitor market quotes, place buy and sell orders, and receive
trade fill information. Again, OptionsAPI.dll is a stripped-down
versionofMH’sSBTAPIandprovidesonlybasicfunctionality,but
it will give you the look and feel of creating real trading software.
Let’s create a program that connects to the market in the S&P
| 500 options | contracts |     | traded | on  | the Chicago |     | Board | Options |
| ----------- | --------- | --- | ------ | --- | ----------- | --- | ----- | ------- |
Exchange.
| Step | 1 Start | a   | new VB.NET |     | Windows |     | application | named |
| ---- | ------- | --- | ---------- | --- | ------- | --- | ----------- | ----- |
OptionOrders.
Team-LRN

ConnectingtoTradingSoftware 291
Step 2 To your Form1, add a single text box and a button.
ChangetheMultilinepropertyofthetextboxtoTrue.
Step 3 IntheProjectsmenutab,selectAddReference.Select
browse and find the OptionsAPI.dll file. In the code
window, above the class definition for Form1, add:
Imports OptionsAPI
Step 4 Togetmarketprices,weneedtosetupobjectsforthe
MicroHedge,MHSBT,andMHPositionclasses.Inthe
general declarations section of the Form1 code win-
dow, add the following code:
Public WithEvents mhApp As MicroHedge
Public WithEvents myMHSBT As MHSBT
Dim Pos As MHPosition
Step 5 In the form load event, add the code to create
instances of the objects
Private S.ub Form1_Load(ByVal sender As ...) Handles MyBase.Load
myMHSBT = New MHSBT()
mhApp = New MicroHedge()
Pos = mhApp.GetSymbol("SPY.TEST", True, False)
End Sub
Because MicroHedge is actually a COM object, we would in
therealworldusetheCreateObject()functiontocreateaninstance
of “MicroHedge.Application” in the following way:
mhApp = CreateObject("MicroHedge.Application")
However, in our simulated environment where we may not have
MicroHedge licensed software, we will use the method for
instantiation as shown. COM objects use something called
unmanaged code, which lacks the benefits of VB.NET’s common
language run time. But it should not prevent you from creating
efficient applications in VB.NET. Since a certain amount of
complexity is involved in mixing the VB.NET code with COM
objects, we suggest you contact MicroHedgeif you intend to use a
.NET platform for development.
Step 6 To the Button1_Click event, add the following code:
Private Sub Button1_Click(ByVal sender As ...) Handles Button1.Click
GetQuotes()
End Sub
Team-LRN

292 AdvancedVB.NET
The method for accessing options data is significantly
different from what we looked at for futures data. In the previous
example using TT and futures, we connected to the market for a
single instrument and were able to see the market in real time. In
this options example, however, we want to monitor several or
maybe hundreds of option contracts at the same time. This will
necessitateloopingthroughthecontractsandrefreshingthedataat
specified intervals. In this case the data will refresh, GetQuotes(),
when the user clicks the button.
Step 7 AddthefollowingcodefortheGetQuotes()function.
For simplicity’s sake, the OptionsAPI program will
only show data for 20 call options on the SPY. The
priceoftheunderlyingindexisapproximately841.00
and will not move.
Private Sub GetQuotes()
Dim i As Integer
Dim cBid, cAsk, cThv, cSym, Days, Strike As Object
cBid = Pos.OptionPairs.FieldArray("cBid")
cAsk = Pos.OptionPairs.FieldArray("cAsk")
cThv = Pos.OptionPairs.FieldArray("cThv")
cSym = Pos.OptionPairs.FieldArray("cSym")
Days = Pos.OptionPairs.FieldArray("Days")
Strike = Pos.OptionPairs.FieldArray("Strike")
TextBox1.Text = "SYMBOL" & vbTab & " BID" & vbTab & _
" ASK" & vbTab & "THEO" & vbCrLf & vbCrLf
For i = 0 To 19
TextBox1.Text &= cSym(i) & vbTab & Format(cBid(i), "##.00") & _
vbTab & Format(cAsk(i), "##.00") & vbTab & _
Format(cThv(i), "##.00") & vbCrLf
Next i
End Sub
Here the GetQuotes() function retrieves the bid, ask, theoretical
value,symbol,daystillexpiration,andstrikeeverytimeitiscalled.
Furthermore it prints the information into TextBox1.
Step 8 Run the program. You should see the form window,
similar to Figure 17.3, populated with simulated
market data when you click the button. The data is
not live, however, and will not change. Click the
button again and you will see that the markets do
change slightly with each refresh.
Team-LRN

ConnectingtoTradingSoftware 293
F I G U R E 17.3
Now let’s add the ability to place some orders and get back trade
fill confirmations.
Step 9 To place orders, we will need to specify a quantity.
InthegeneraldeclarationssectionoftheForm1code
window, add:
Const QUANT As Integer = 10
Step 10 In the GetQuotes() functions, add the following
code. This code will loop through the market bids
andoffersandplaceorders,usingtheEnterOrder()
subroutine, to buy orders when the ask price is 10
cents below the theoretical value and to sell orders
whenthebidis10centsabovethetheoreticalvalue:
For i = 0 To 19
TextBox1.Text &= cSym(i) & vbTab & Format(cBid(i), "##.00") & _
vbTab & Format(cAsk(i), "##.00") & vbTab & _
Format(cThv(i), "##.00") & vbCrLf
If cAsk(i) + 0.1 < cThv(i) Then
EnterOrder(Month(DateAdd("d", Days(i), #3/1/2003#)), _
Team-LRN

294 AdvancedVB.NET
Year(DateAdd("d", Days(i), #3/1/2003#)), cSym(i), _
Strike(i), cAsk(i), QUANT)
ElseIf cBid(i) - 0.1 > cThv(i) Then
EnterOrder(Month(DateAdd("d", Days(i), #3/1/2003#)), _
Year(DateAdd("d", Days(i), #3/1/2003#)), cSym(i), _
Strike(i), cBid(i), -QUANT)
End If
Next i
Step 11 Now add the function code for the EnterOrder()
subroutine:
Private Sub EnterOrder( ByVal ExMonth As Integer, _
ByVal ExYear As Integer, _
ByVal OPRA As String, _
ByVal Strike As Double, _
ByVal Price As Double, _
ByVal Quant As Long)
Dim Inst As New IndexOp()
Dim CBOEOrd As New CBOEorder()
Inst.ExpyMonth = ExMonth
Inst.ExpyYear = ExYear
Inst.OpenClose = 1 ’Open
Inst.CoverNaked = 2 ’Naked
Inst.Root = Microsoft.VisualBasic.Left(OPRA, 3)
Inst.Strike = Strike
Inst.Underlier = Pos.SYMBOL
Inst.CallPut = 1 ’Call
CBOEOrd.OrdPrice = Price
CBOEOrd.OrdQty = Math.Abs(Quant)
CBOEOrd.Account = Pos.Account
CBOEOrd.Duration = 1 ’Day
CBOEOrd.Instrument = Inst
CBOEOrd.PriceType = 2 ’Limit
If Quant > 0 Then
CBOEOrd.Side = 1
Else
CBOEOrd.Side = 2
End If
myMHSBT.PlaceOrder(CBOEOrd)
End Sub
The EnterOrder() subroutine creates an index option object,
IndexOp,andaCBOEorderobjectandsetsthevaluesnecessaryto
send an order. In this example, we are sending a quantity of 10
contracts. As you will be able to see, though, an order of 10
contracts can grow into a position of 50 or 100 contracts quickly if
the market price does not come back into line with the theoretical
value. Applications that you build will need to devise a way to
handle these situations from a portfolio perspective.
Team-LRN

| ConnectingtoTradingSoftware |     |     |     |     |     | 295 |
| --------------------------- | --- | --- | --- | --- | --- | --- |
Step 12 In order to receive trade fill confirmations, add the
|         | following                    | event               | handler: |               |                    |     |
| ------- | ---------------------------- | ------------------- | -------- | ------------- | ------------------ | --- |
| Private | Sub myMHSBT_OrderEvent(ByVal |                     | Order    | As CBOEorder) | _                  |     |
|         |                              |                     |          | Handles       | myMHSBT.OrderEvent |     |
|         | MsgBox("Filled:              | " & Order.ToString) |          |               |                    |     |
End Sub
Ourmethodofhandlingthetradefillconfirmationsthatcome
back to us from the market will be to simply print them out in a
message box.
| Step 13 | Run the program. |     | Figure | 17.4 shows | the results. |     |
| ------- | ---------------- | --- | ------ | ---------- | ------------ | --- |
Nowlet’saddatimer,sothatthedatarefreshesautomatically
| without a button | click. |     |     |     |     |     |
| ---------------- | ------ | --- | --- | --- | --- | --- |
Step 14
|         | Remove       | Button1 | and           | the Button1_Click |        | event   |
| ------- | ------------ | ------- | ------------- | ----------------- | ------ | ------- |
|         | routine.     | In the  | toolbox       | you will          | find   | a Timer |
|         | control. Add | a       | timer control | to your           | Form1. | In the  |
| F I G U | R E 17.4     |         |               |                   |        |         |
Team-LRN

| 296 |       |            |               |          |      |          |             | AdvancedVB.NET |       |
| --- | ----- | ---------- | ------------- | -------- | ---- | -------- | ----------- | -------------- | ----- |
| F I | G U R | E 17.5     |               |          |      |          |             |                |       |
|     |       | Properties | window        |          | for  | Timer1,  | set         | the Enabled    |       |
|     |       | property   | to            | True and | the  | Interval | property    | to             | 5000. |
|     |       | Add        | the following |          | code | to the   | Timer1_Tick |                | event |
routine:
Private Sub Timer1_Tick(ByVal sender As ...) Handles Timer1.Tick
GetQuotes()
| End    | Sub          |      |              |     |           |            |         |              |       |
| ------ | ------------ | ---- | ------------ | --- | --------- | ---------- | ------- | ------------ | ----- |
| Step   | 15           | Run  | the program. |     | Figure    | 17.5 shows |         | the results. |       |
| The    | timer        | will | tick every   |     | 5 seconds | and        | refresh | the          | data. |
| Trades | will execute |      | as before.   |     |           |            |         |              |       |
SUMMARY
In this chapter we have looked at two methods for connecting to
| real markets |          | through | connections |           | to  | the APIs | of  | two popular |     |
| ------------ | -------- | ------- | ----------- | --------- | --- | -------- | --- | ----------- | --- |
| financial    | industry |         | software    | packages. |     | Building |     | software    | for |
Team-LRN

| ConnectingtoTradingSoftware |     |     |     |     |     | 297 |
| --------------------------- | --- | --- | --- | --- | --- | --- |
monitoring real-time prices, performing analytics, and monitoring
| trade fills | and | portfolio | risk are | absolutely | necessary | for |
| ----------- | --- | --------- | -------- | ---------- | --------- | --- |
implementation of an automated trading system. Several of these
| key components |     | may already | be present | in  | COTS software. | APIs |
| -------------- | --- | ----------- | ---------- | --- | -------------- | ---- |
allow for proprietary analytics to be built on top of these systems.
| You | should | contact | the software | provider | for full documen- |     |
| --- | ------ | ------- | ------------ | -------- | ----------------- | --- |
tation of its API before attempting to build a trading system. The
documentation will have all the information on the classes and
| their functionalities |     | in the | API along | with sample | programs. |     |
| --------------------- | --- | ------ | --------- | ----------- | --------- | --- |
Team-LRN

| 298 |     |     |     | AdvancedVB.NET |     |
| --- | --- | --- | --- | -------------- | --- |
PROBLEMS
| 1. What | is the rule regarding |     | automated order | entry | of  |
| ------- | --------------------- | --- | --------------- | ----- | --- |
| options | orders?               |     |                 |       |     |
2. Whatistheproblemsituationwithoptionsorderentrythat
| we need   | to resolve?      |          |              |       |     |
| --------- | ---------------- | -------- | ------------ | ----- | --- |
| 3. If the | COTS application | is a COM | object, what | would | you |
do?
4. Whatistheprocessforcreatingobjectsoutoftheclassesin
an API?
| 5. Where | can you find | out more about | the objects | in an | API? |
| -------- | ------------ | -------------- | ----------- | ----- | ---- |
Team-LRN

ConnectingtoTradingSoftware 299
| PROJECT | 17.1 |     |     |
| ------- | ---- | --- | --- |
Create a single VB.NETapplication that connects to both the S&P
500eMinimarketontheCMEandtheS&P500cashoptionsmarket
on the CBOE using the TraderAPI and the OptionsAPI libraries.
| PROJECT | 17.2 |     |     |
| ------- | ---- | --- | --- |
To the program in Project 17.1, add a Portfolio object that keeps
trackoftheinstrumentsboughtandsoldandthenetpositions.This
will require the use of the StockOption class, the CallOption class,
| and a Futures | class, which | you will need | to create yourself. |
| ------------- | ------------ | ------------- | ------------------- |
Team-LRN

This page intentionally left blank.
Team-LRN

C H A P T E R 18
XML
O
ver the last 5 or so years, the ever-increasing demand for
flexibility in application messaging has spawned the Extensible
Markup Language (XML). XML is a fully portable and open
markup syntax for data description and messaging. Further,
beyond being just a markup language, XML is a metalanguage—a
language used to define new markup languages. Whereas
Hypertext Markup Language (HTML) is used for formatting and
displaying data, XML allows users to represent the contextual
meaning of the data they wish to model using human readable
tags.
In this chapter we will cover the basics of XML notation as
well as ways to describe and encapsulate data in an XML
document, also called an XML message. In addition, we will go
overhowtowriteVB.NETprogramsthatencapsulatedatainXML
messages and how to send them over the Internet. While only
skimming the surface of XML, this chapter will give you the
knowledge and the context you need to use XML in your VB.NET
programs.
XML AND FINANCIAL MARKETS
The ultimate goal of developing firmwide, real-time global
positioning systems that exploit profitable trading opportunities
and manage risk will require a much higher degree of
interconnectivity between departments within a firm, trading
counterparties, and exchanges than exists today. As a result,
institutions involved in the financial markets have caught on to
301
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for terms of use.
Team-LRN

302 AdvancedVB.NET
XMLasawaytomovelargequantitiesofdatainrealtimebetween
different technology systems. Financial markets, firms, and
professionals who utilize XML find it to be a powerful tool for
financial data representation and messaging and see it as the key
technology in meeting the challenges of global interconnectivity
(Bradley, 2002).
Because XML is a metalanguage, segments of the financial
markets industry have already been able to create their own
markup languages specifically for their own domains. In addition
tolearningthetechnologyofXMLinthischapter,wewillbeableto
see some of the business reasons why financial institutions are so
keen on developing XML-based technologies, even to the point of
inventing their own customized markup languages using XML.
In the following chapter, we will look at some specific XML
technologiesusedinthefinancialmarketsandcreateprogramsina
new industry XML protocol called FIXML.
CREATING A MARKUP LANGUAGE
As we mentioned, XML allows us to represent the contextual
meaningofthedatawewishtodescribeandtransmit.Thisisdone
through the definition of customized tags. As long as the
application that sends an XML message and the application that
receives it agree on what these tags mean, they can communicate
andexchangedata.Ifyouarenotfamiliarwithmarkuplanguages,
this idea of inventing or defining our own tags may seem
somewhat vague. So let’s take a quick look at an example.
Imagine for a minute that we could invent our own markup
language for describing a trade. What kind of tags might we want
to invent, and how would an XML document written with these
tags look? Intuitively, we would first probably describe the
information structure of a trade:
TradeInformation
Exchange
Tickersymbol
Buy/sell
Quantity
Price
Team-LRN

| XML |     |     |     |     |     |     |     | 303 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
TradeInformation
Clearingfirm
Trader
Time
Etc.
| Now | that | we have | listed | the | information | about | a trade, | let’s |
| --- | ---- | ------- | ------ | --- | ----------- | ----- | -------- | ----- |
define a markup language using XML tags to describe it and then
rewrite our trade in that language. We will call our new markup
| language   | FMML—the |           | Financial |       | Markets  | Markup      | Language,  |       |
| ---------- | -------- | --------- | --------- | ----- | -------- | ----------- | ---------- | ----- |
| pronounced |          | “fimmel.” | In        | the   | same     | way that    | a variable | in    |
| VB.NET     | should   | be        | named     | using | a naming | convention, |            | which |
describes the data held in the variable, our FMML tags should
| represent | the     | contextual | meaning |        | of the   | data being | held.    |     |
| --------- | ------- | ---------- | ------- | ------ | -------- | ---------- | -------- | --- |
| So        | the tag | for a      | trade   | should | probably | be named   | ,Trade.. |     |
Thetagfortheexchangenameshouldprobablybe,Exchange..
And so on. Simple, right? It is exactly this simplicity that makes
XML so popular. It is a completely intuitive way to describe data.
Before we go ahead and write our trade using these tags, we must
consideronemorething.ItmaybepossiblethataFMMLdocument
representing a trade may at times consist of more than one trade.
Forexample,wemaywanttodescribeaspreadtrade,whichwould
havetwolegs.Sowewillneedaroottag,orarootelement,within
which we can place a trade or trades. Let’s call our root element
| <Tradedoc> | for | trade     | document. |          |     |          |     |           |
| ---------- | --- | --------- | --------- | -------- | --- | -------- | --- | --------- |
| Now        | we  | are ready | to        | describe | our | trade in | XML | using our |
FMML tags.
| <?xml | version=’1.0’ |     |     | ?>  |     |     |     |     |
| ----- | ------------- | --- | --- | --- | --- | --- | --- | --- |
<Tradedoc>
<Trade>
|     | <Exchange | Acronym=’FMEX’/> |     |     |     |     |     |     |
| --- | --------- | ---------------- | --- | --- | --- | --- | --- | --- |
<Ticker>IBMDP</Ticker>
<BuySell Type=’Buy’/>
<Quantity>10</Quantity>
<Price Type=’Market’/>
<ClearingFirm>001</ClearingFirm>
<Trader>Ben</Trader>
|     | <Time>3/6/2003 |     | 1:45:06 |     | PM</Time> |     |     |     |
| --- | -------------- | --- | ------- | --- | --------- | --- | --- | --- |
</Trade>
</Tradedoc>
Team-LRN

| 304    |     |             |        |          |     |         | AdvancedVB.NET |      |
| ------ | --- | ----------- | ------ | -------- | --- | ------- | -------------- | ---- |
| Again, | so  | far we have | simply | invented |     | our own | markup         | tags |
that represent the contextual meaning of the data in a trade. Let’s
| take a closer |     | look at the | rules | of XML |     | using this | particular |     |
| ------------- | --- | ----------- | ----- | ------ | --- | ---------- | ---------- | --- |
documentormessage,whichiswritteninFMML,becausetherules
| of XML are | very  | strict.      |                 |               |     |           |      |         |
| ---------- | ----- | ------------ | --------------- | ------------- | --- | --------- | ---- | ------- |
| On the     | CD    | a file named |                 | sampleXML.xml |     | contains  |      | the XML |
| message    | shown | above.       | Double-clicking |               | on  | this file | will | cause   |
it to open in MS Internet Explorer (see Figure 18.1. Well-formed
| XML documents |     | such | as this | one | will | successfully |     | open in |
| ------------- | --- | ---- | ------- | --- | ---- | ------------ | --- | ------- |
Internet Explorer. XML documents that are not well formed will
| generate | an error | statement |     | in the | Internet | Explorer |     | window. |
| -------- | -------- | --------- | --- | ------ | -------- | -------- | --- | ------- |
FortunatelytheXMLdocumentwecreatedisbothwellformedand
valid.
| F I G U | R E | 18.1 |     |     |     |     |     |     |
| ------- | --- | ---- | --- | --- | --- | --- | --- | --- |
Team-LRN

XML 305
Well-Formed XML Documents
Every XML document must be well formed. A well-formed XML
document follows all the structural rules for XML, and make no
mistake, XML definitely does not allow ambiguous structure.
This is because part of the information contained in an XML
message has to do with how different elements relate to one
another.Ifthestructureisambiguous,soistheinformation.Aclean
and consistent structure is what allows XML documents to be
processed as data structures or trees, as we will briefly describe
later. Programs that intend to process XML, called parsers, will
reject any message that does not follow the structural rules for
beingwellformed.AmongthemostimportantrulesarethatXMLis
case-sensitive and that unclosed tags and overlapping tags are
notpermitted.
Every start tag must have a corresponding end tag. The start
tagbeginsanenclosedareaoftext,knownasanitem,accordingto
the tag name. <Ticker> is a start tag. </Ticker> is an end tag. The
element, defined by a tag, ends with the end tag. As we will point
out later, XML tags may also include one of a list of attributes
consisting of an attribute name and an attribute value.
A tag that opens inside another tag must close before the
containing tag closes. For example, take a look at this sequence:
<ClearingFirm>001<Trader>Ben</ClearingFirm>
</Trader>
ObviouslythisXMLmessageisnotwellformedbecause<Trader>
opensinside<ClearingFirm>butdoesnotclosepriortotheclosing
tag </ClearingFirm>. Put differently, the structure of an XML
document must be strictly hierarchical.
Assuming a particular XML message is, in fact, well formed,
wecanturnourattentiontowhetherornotitisvalid.Justbecause
anXMLdocumentiswellformeddoesnotmeanitisvalid.Making
sureourXML document is well formedis only half thebattle. The
other half is validation.
Valid XML Documents
When the XML tags in a well-formed document are queried for
their meanings, we say the document is being validated. A well-
formed XML message simply means that it has met all the syntax
Team-LRN

306 AdvancedVB.NET
requirements, whereas a valid XML message means that both the
sending and receiving parties are able to correctly identify the
document’s content according to an agreed-upon set of tag
definitions.
Earlierinthechapter,wedefinedXMLasasyntax,becauseit
is not truly a programming language. It is a plain markup
language; we developers make up the tags and the definitions
associated with those tags. The set of tag names that we came up
with to describe a trade we gave the name FMML. In this way
FMMLcanbethoughtofasadialectoftheXMLlanguage.FMML
is a specific set of XML tags with their respective meanings.
Eventually, if we intend to transmit our FMML trade
document to another application over a network or over the
Internet, we will need to make sure that the tag names are used
correctly with respect to our FMML definition. That is, we must
speak the dialect correctly. We could not, for example, use a tag
names<ExpMonth>,becauseitisnotpartofFMMLaswedefined
it. Furthermore the application that receives our FMML message
must be able to understand the FMML dialect as well. As long as
the receiver of our message understands FMML, we can
communicate using this dialect. If we sent our FMML message to
a widget factory for example or some other non-FMML speakers,
they would not be able to read it.
When sending or receiving an XML document, both parties
mustagreeonthemeaningoftheXMLtags;thatis,theymustagree
onthedialect.Justbecauseweareplacingthenumberofcontracts
in a trade within a <Quantity> tag does not mean that the server
receiving our document will understand the contents of the
<Quantity> element. What we need then is a system that both the
senderandreceivercanusetovalidatethemeaningofthetags.Of
course, these types of systems have already been developed.
There are two different methods used to validate XML
documents—document type definition (DTD) and XML schema.
The system we will look at is DTD.
ThepurposeofaDTDistodefinethelegalbuildingblocksof
anXMLdocument. Itdefines the documentstructure along witha
list of acceptable elements and tags. In addition to defining names
fortags,aDTDdefinesthebusinessrulesorvalidvaluesthatmay
Team-LRN

| XML |     |     |     |     |     |     |     | 307 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
be contained within the tags. As we will see, a DTD can be an
| external | reference. |     |     |     |     |     |     |     |
| -------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
Ifseveralfinancialinstitutionsandexchangesgettogetherand
| agree | on a dialect, | or  | DTD, | they | can communicate |     | between |     |
| ----- | ------------- | --- | ---- | ---- | --------------- | --- | ------- | --- |
themselves using that dialect of XML. As you can imagine then,
DTDs are very powerful. They define industry standards for the
meanings and business rules of an XML document. Earlier in this
| chapter | we mentioned |     | that XML | tags | mean | nothing |     | to the |
| ------- | ------------ | --- | -------- | ---- | ---- | ------- | --- | ------ |
computer.Buttopeople,theymeanalot.Technologyprofessionals
of entire segments within the financial markets industry meet and
| define  | DTDs that | become  | the     | standard | within | their  | particular |     |
| ------- | --------- | ------- | ------- | -------- | ------ | ------ | ---------- | --- |
| domain. | Any XML   | message | creator | who      | sends  | an XML | document   |     |
basedontheagreed-uponDTDcanbeassuredthattherecipientof
the document will be able to read it. This is one of the main
advantages of using XML to transfer data. It allows individual
firms or even entire industries to create their own customized
| markup | language. |     |     |     |     |     |     |     |
| ------ | --------- | --- | --- | --- | --- | --- | --- | --- |
Again,inthefollowingchapter,wewilllookatafewexamples
ofDTDsforfinancialmarkets.Butforrightnow,let’stakealookat
| how a     | DTD validates | an       | XML document. |         |           |     |          |     |
| --------- | ------------- | -------- | ------------- | ------- | --------- | --- | -------- | --- |
| DOCUMENT  |               | TYPE     | DEFINITION    |         |           |     |          |     |
| Seen from | a DTD         | point of | view,         | all XML | documents |     | are made | up  |
of simple building blocks—elements, tags, attributes, entities,
| PCDATA, | and CDATA. |     |     |     |     |     |     |     |
| ------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
Elements
| Elements | are the | main | building | blocks | of  | XML | documents. |     |
| -------- | ------- | ---- | -------- | ------ | --- | --- | ---------- | --- |
ExamplesofXMLelementsthatwehavelookedatare<Trade>and
<Ticker>.Elementscancontaintext,cancontainotherelements,or
can be empty.
Tags
Tags are used to mark up elements. A starting tag like <Ticker>
| marks | up the beginning |     | of an | element, | and | an ending | tag | like |
| ----- | ---------------- | --- | ----- | -------- | --- | --------- | --- | ---- |
Team-LRN

| 308       |       |        |     |       |          |             | AdvancedVB.NET |     |
| --------- | ----- | ------ | --- | ----- | -------- | ----------- | -------------- | --- |
| </Ticker> | marks | up the | end | of an | element. | Furthermore |                | XML |
permitsemptytags,denotedbyaslashbeforethefinalright-angle
bracketin the tag like this <Ticker/..This tagopensand closes in
| one statement. | Empty         | tags    | of  | this | sort may | have | within | them |
| -------------- | ------------- | ------- | --- | ---- | -------- | ---- | ------ | ---- |
| attributes     | and attribute | values. |     |      |          |      |        |      |
Attributes
| Attributes | provide | extra | information |     | about | elements |     | and are |
| ---------- | ------- | ----- | ----------- | --- | ----- | -------- | --- | ------- |
always placed inside the starting tag of an element. Attributes
always come in name-value pairs and are allowed to be empty if
not supplied at all. However, XML does not allow naked attribute
values. Attribute values must be in quotes. Forexample, we allow
the <BuySell> tag to take on an attribute of either Buy or Sell:
| <BuySell | Value=‘Buy’/>. |     |     |     |     |     |     |     |
| -------- | -------------- | --- | --- | --- | --- | --- | --- | --- |
Entities
Entities are variables used to define common text or characters.
| Entities | are then | expanded |     | when | an XML | parser | parses | a   |
| -------- | -------- | -------- | --- | ---- | ------ | ------ | ------ | --- |
document. For example, because they are special characters for
XML, <, >, &, “, and ‘ must be represented by special-character
entities.AnXMLmessageusing,say,thedouble-quotecharacterin
textenclosedinatagwouldnotbewellformed.Correctlydesigned
XML parsers will produce an error for such input. The following
| entities | are predefined | in               | XML: |     |           |     |     |     |
| -------- | -------------- | ---------------- | ---- | --- | --------- | --- | --- | --- |
|          |                | EntityReferences |      |     | Character |     |     |     |
|          |                | &lt;             |      |     | <         |     |     |     |
|          |                | &gt;             |      |     | >         |     |     |     |
|          |                | &amp;            |      |     | &         |     |     |     |
|          |                | &quot;           |      |     | "         |     |     |     |
|          |                | &apos;           |      |     | "         |     |     |     |
PCDATA
PCDATA means parsed character data. Character data is the text
found between the start tag and the end tag of an XML element.
PCDATAistextthatwillbeparsedbyaparser.Tagsinsidethetext
| will be | treated as markup, |     | and | entities | will | be expanded. |     |     |
| ------- | ------------------ | --- | --- | -------- | ---- | ------------ | --- | --- |
Team-LRN

XML 309
CDATA
CDATA means character data. CDATA is text that will not be
parsedbyaparser.Tagsplacedinsidethetextwillnotbetreatedas
markup, and entities will not be expanded.
Parsers
Aswediscussedpreviously,anXMLmessage’sstructureshouldbe
validatedagainstaDTD.Thisisdonethroughtheuseofaparser,a
programthatactuallyconductsthevalidationandreadsthedata.A
parser that has access to a DTD guarantees that all the required
elementsandattributesarepresentinanXMLdocumentaccording
to the DTD. As with XML itself, the rules for validation are very
strict.
XML validation is order-sensitive, and elements must appear
inthesameorderastheyarespecifiedintheDTD.Additionalfields
maynotbeaddedwithoutfirstdefiningthemintheDTDorinthe
XML message itself. There are two methods for parsing and
processing XML documents: the document object model (DOM)
and the simple API for XML (SAX) model. We will employ a SAX
parser in an example program later.
A parser using DOM reads the entire XML document into a
hierarchical tree structure. A tree is a nonlinear, two-dimensional
datastructurecapableofholdingtheelementsofanXMLmessage
innodes.Therootnodeisthefirstnodeofthetreeandcorresponds
to the root element in an XML document. Every otherelement is a
child of the parent root node. Unlike the tree-based structure in
DOM,SAX is event-based.SAXparsersnotify our applicationof a
stream of parsing events. Since both DOM and SAX are widely
standardized and supported, developers have a choice of free,
high-quality, third-party parsing software.
Aswewillsee,classesforcreatingandreadingXMLmessages
arefoundintheSystem.XMLnamespace.Fornowlet’stakealook
at the DTD for FMML and gain an understanding of how a parser
validates a FMML message.
<?xml version=’1.0’ encoding=’us-ascii’?>
<!ELEMENT Tradedoc (Trade+)>
Team-LRN

| 310 |     |     |     |     | AdvancedVB.NET |     |
| --- | --- | --- | --- | --- | -------------- | --- |
<!ELEMENT Trade (Exchange,Ticker,BuySell,Quantity,Price,ClearingFirm,Trader,
Time)>
| <!ELEMENT Exchange     | (#PCDATA)> |            |     |     |     |     |
| ---------------------- | ---------- | ---------- | --- | --- | --- | --- |
| <!ELEMENT Ticker       | (#PCDATA)> |            |     |     |     |     |
| <!ELEMENT BuySell      | (#PCDATA)> |            |     |     |     |     |
| <!ELEMENT Quantity     | (#PCDATA)> |            |     |     |     |     |
| <!ELEMENT Price        | (#PCDATA)> |            |     |     |     |     |
| <!ELEMENT ClearingFirm |            | (#PCDATA)> |     |     |     |     |
| <!ELEMENT Trader       | (#PCDATA)> |            |     |     |     |     |
| <!ELEMENT Time         | (#PCDATA)> |            |     |     |     |     |
<!ATTLIST Exchange Acronym (CBOE|ISE|BOX|AMEX|FMEX) #REQUIRED>
| <!ATTLIST BuySell | Type       | (Buy|Sell)   | #REQUIRED> |              |         |           |
| ----------------- | ---------- | ------------ | ---------- | ------------ | ------- | --------- |
| <!ATTLIST Price   | Type       | CDATA #FIXED | "Market">  |              |         |           |
| Let’s             | go through | line         | by line    | and describe | what is | going on. |
| <!ELEMENT         | Tradedoc   |              | (Trade+)>  |              |         |           |
This line specifies that this DTD is meant to validate an XML
message called a Tradedoc and that a Tradedoc is made up of at
| least one element | named |     | Trade. |     |     |     |
| ----------------- | ----- | --- | ------ | --- | --- | --- |
<!ELEMENT Trade (Exchange,Ticker,BuySell,Quantity,Price,ClearingFirm,Trader,
Time)>
| Here      | we can       | see that   | a <Trade>  | element    | contains | eight child |
| --------- | ------------ | ---------- | ---------- | ---------- | -------- | ----------- |
| elements. | No other     | elements   | are        | allowed.   |          |             |
| <!ELEMENT | Exchange     |            | (#PCDATA)> |            |          |             |
| <!ELEMENT | Ticker       | (#PCDATA)> |            |            |          |             |
| <!ELEMENT | BuySell      |            | (#PCDATA)> |            |          |             |
| <!ELEMENT | Quantity     |            | (#PCDATA)> |            |          |             |
| <!ELEMENT | Price        | (#PCDATA)> |            |            |          |             |
| <!ELEMENT | ClearingFirm |            |            | (#PCDATA)> |          |             |
| <!ELEMENT | Trader       | (#PCDATA)> |            |            |          |             |
| <!ELEMENT | Time         | (#PCDATA)> |            |            |          |             |
TheselinesintheDTDspecifythechildrenwithinaTradetaginthe
| order in | which they | must | be  | supplied. | The #PCData | notation |
| -------- | ---------- | ---- | --- | --------- | ----------- | -------- |
specifies that the contents of each tag are to be parsed character
data.Thisisabitmisleadingbecauseitsuggeststhatthecontentsof
XML tags are data-type-specific like numbers, strings, and dates.
XMLisnotdata-type-specific.Rather,thinkofcharacterdataasthe
textfoundbetweenthestarttagandtheendtagofanXMLelement
andnothingmore.TheDTDhasnowaytodefineanelement’sdata
type. In the FMML DTD above, the <Ticker> element is defined to
Team-LRN

XML 311
be an empty element with an attribute named type of PCDATA.
Parsed character data means that the parser reads the data ex-
tracted from the tag.
The DTD up to this point has only specified which elements
alongwiththeirchildrenandtagnamesmustbefoundintheXML
document, written in our made-up language called FMML. The
DTD has done nothing yet to help us determine whether good
information is contained in the tags. When simple business rules
need to be applied, attributes and attribute value lists may be
included.XMLattributescanbeaddedtoelementsifmoredetailed
information needs to be known about them. For example, the
<Exchange> tag can include an attribute to give us more
information on which exchange we are dealing with, such as
CBOE, ISE, or AMEX.
An XML element can contain as many attributes as needed.
The <Exchange> element has a single attribute as described in the
DTD and is known as Acronym.
<!ATTLIST Exchange Acronym (CBOE|ISE|BOX|AMEX|FMEX)
#REQUIRED>
The Acronym attribute will be validated against a set of legal
values: CBOE, ISE, BOX, AMEX, and FMEX. (As we will later see,
FMEXistheFinancialMarketsExchange,asimulated,hypothetical
exchangewecancommunicatewithovertheInternetusingFMML
toplaceordersandreceivefills.)Noticethatenumeratedvaluesare
containedinanopen-closesetofparenthesesandareseparatedby
thepipecharacter,|.Alsonoticethatthislistofenumeratedvalues
doesnotneedtobeinsingleordoublequotes;inXMLeverythingis
a string.
The <BuySell> and <Price> tags have attributes as well:
<!ATTLIST BuySell Type (Buy|Sell) #REQUIRED>
<!ATTLIST Price Type CDATA #FIXED "Market">
The<BuySell>taghasarequiredTypeattribute,whichcantakeon
the value of either Buy or Sell. The <Price> tag’s fixed Type
attributecanonlytakeonthevalue“Market”.Thatis,accordingto
the definition of FMML, only market orders are permissible. So
limit or stop orders are not allowed.
Team-LRN

| 312           |                              |          |              |                                       |           |             | AdvancedVB.NET |
| ------------- | ---------------------------- | -------- | ------------ | ------------------------------------- | --------- | ----------- | -------------- |
| The attribute |                              | type can | have         | the                                   | following | values:     |                |
| Value         |                              |          |              |                                       |           | Description |                |
| CDATA         |                              |          |              | Thevalueischaracterdata               |           |             |                |
| (X|Y|...)     |                              |          |              | Thevaluemustbeonefromanenumeratedlist |           |             |                |
| ID            |                              |          |              | ThevalueisauniqueID                   |           |             |                |
| IDREF         |                              |          |              | ThevalueistheIDofanotherelement       |           |             |                |
| IDREFS        |                              |          |              | ThevalueisalistofotherIDs             |           |             |                |
| NMTOKEN       |                              |          |              | ThevalueisavalidXMLname               |           |             |                |
| NMTOKENS      |                              |          |              | ThevalueisalistofvalidXMLnames        |           |             |                |
| ENTITY        |                              |          |              | Thevalueisanentity                    |           |             |                |
| ENTITIES      |                              |          |              | Thevalueisalistofentities             |           |             |                |
| NOTATION      |                              |          |              | Thevalueisanameofanotation            |           |             |                |
| xml:          |                              |          |              | ThevalueisapredefinedXMLvalue         |           |             |                |
| The default   | value                        | of       | an attribute |                                       | can be:   |             |                |
| Value         |                              |          |              | Description                           |           |             |                |
| Value         | Thedefaultnameoftheattribute |          |              |                                       |           |             |                |
#REQUIRED Theattributevaluemustbeincludedintheelementandisnotoptional
| #IMPLIED    | Theattributeisoptional   |                |     |     |      |          |            |
| ----------- | ------------------------ | -------------- | --- | --- | ---- | -------- | ---------- |
| #FIXEDvalue | Theattributevalueisfixed |                |     |     |      |          |            |
| For the     | sake                     | of simplicity, |     | our | FMML | DTD only | deals with |
PCDATA.AlthoughthereisalotmoretoXMLthanwecanfitinto
thischapter,theFMMLDTDwillbesufficienttovalidatemessages,
intheformoftrades,thatwewillsendovertheInternet,aslongas
we include the name and location of the .dtd file in our FMML
message.
| The FMML.dtd |     | file | we  | will | use to | validate | our FMML |
| ------------ | --- | ---- | --- | ---- | ------ | -------- | -------- |
messageswillactuallybeexternaltotheXMLdocumentswecreate
and send. External DTDs can exist as flat files both on the local
machineandonthelocalnetworkorasauniformresourcelocator
(URL) on the Internet. Whatever the case, DTDs usually exist as
| publicly available, |              | human | readable | ASCII | files.  |         |              |
| ------------------- | ------------ | ----- | -------- | ----- | ------- | ------- | ------------ |
| In our              | XML messages |       | we       | will  | need to | specify | the name and |
location of the DTD against which it should be validated by the
receiving parser. If the DTD is located in the current folder, the
| following syntax | should   |     | be included |             | in the | XML document: |     |
| ---------------- | -------- | --- | ----------- | ----------- | ------ | ------------- | --- |
| <!DOCTYPE        | Tradedoc |     | SYSTEM      | ’fmml.dtd’> |        |               |     |
Team-LRN

XML 313
Ifneeded,theentirepathtothe.dtd filecanbespecified—for
example, C:\ModelingFM\xml\fmml.dtd. If the DTD is public as
in the FMML case, meaning that it is available on the Internet, the
syntax will be:
<!DOCTYPE Tradedoc SYSTEM ’http://yorkville.rice. _
iit.edu:8100/FMML.dtd’>
When a DTD exists as a URI, it becomes especially powerful.
Assuming that all partners who exchange XML messages can
accesstheDTD,theyallcanuseittocreateandvalidatetheirXML
documents anywhere in the world. Let’s take a look.
CREATING XML DOCUMENTS
BeforewecreateanInternetapplication,let’sfirstdevelopasimple
VB.NETapplicationthatwillwriteanXMLdocumentandsaveitto
the C:\drive.
Step 1 InVB.NETcreateanewWindowsapplicationnamed
XMLexample.
Step 2 OnyourForm1,addcontrolstobuildtheGUIshown
in Figure 18.2.
There should be two combo boxes on your form. Name them
cboExchange and cboBuySell. In the Collection property of
cboExchange, add the elements CBOE, ISE, BOX, AMEX, and
FMEX. In the Collection property of cboBuySell, add the elements
Buyand Sell.Givethetext boxestheappropriate names:txtTicker,
txtQuantity, txtPrice, txtClearingFirm, and txtTrader.
Step 3 To the Button1_Click event, add the following code:
Imports System.IO
Public Class Form1
Inherits System.Windows.Forms.Form
[Windows Form Designer Generated Code]
Private Sub Button1_Click(ByVal sender As ...) Handles Button1.Click
Dim strTradeDoc As String
strXMLtrade = "<?xml version = ’1.0’?>"
strXMLtrade &= "<Tradedoc>"
strXMLtrade &="<Trade>"
strXMLtrade &= "<Exchange Acronym = ’" & cboExchange.Text & "’/>"
strXMLtrade &= "<Ticker>" & txtTicker.Text & "</Ticker>"
Team-LRN

| 314         |     |           |      |                        |     | AdvancedVB.NET |     |
| ----------- | --- | --------- | ---- | ---------------------- | --- | -------------- | --- |
| F I G U     | R E | 18.2      |      |                        |     |                |     |
| strXMLtrade | &=  | "<BuySell | Type | = ’" & cboBuySell.Text |     | & "’/>"        |     |
strXMLtrade &= "<Quantity>" & txtQuantity.Text & "</Quantity>"
| strXMLtrade | &=  | "<Price | Type = | ’" & txtPrice.Text |     | & "’/>" |     |
| ----------- | --- | ------- | ------ | ------------------ | --- | ------- | --- |
strXMLtrade &= "<ClearingFirm>"&txtClearingFirm.Text&"</ClearingFirm>"
| strXMLtrade | &=  | "<Trader>"    | & txtTrader.Text |             | & "</Trader>" |     |     |
| ----------- | --- | ------------- | ---------------- | ----------- | ------------- | --- | --- |
| strXMLtrade | &=  | "<Time>"      | & Now            | & "</Time>" |               |     |     |
| strXMLtrade | &=  | "</Trade>"    |                  |             |               |     |     |
| strXMLtrade | &=  | "</Tradedoc>" |                  |             |               |     |     |
Dim objWriter As New StreamWriter("C:\ModelingFM\myFirstXMLdoc.xml")
objWriter.Write(strXMLtrade)
objWriter.Close()
End Sub
End Class
| Step  | 4 Run                                      | the   | program. | Your    | results                   | should look | like the |
| ----- | ------------------------------------------ | ----- | -------- | ------- | ------------------------- | ----------- | -------- |
|       | screen                                     |       | shown in | Figure  | 18.3.                     |             |          |
| Step5 | NowfindthefilenamedmyFirstXMLdoc.xmlinyour |       |          |         |                           |             |          |
|       | C:\ModelingFMfolder                        |       |          |         | anddouble-clickonit,which |             |          |
|       | will                                       | cause | it to    | open in | MS Internet               | Explorer.   |          |
Team-LRN

| XML     |       |          |         |         |         |              | 315 |
| ------- | ----- | -------- | ------- | ------- | ------- | ------------ | --- |
| F I G   | U R E | 18.3     |         |         |         |              |     |
| If your | XML   | document | is well | formed, | it will | successfully |     |
open.Ifitisnotwellformed,InternetExplorer(IE)willgeneratean
error statement.
| SENDING | XML | MESSAGES |     |     |     |     |     |
| ------- | --- | -------- | --- | --- | --- | --- | --- |
CreatinganXMLmessageandsavingittoafileisnotreallyallthat
exciting. After all, XML was designed for communication. Let’s
| change our | program | so  | we can send | our | FMML | trade over | the |
| ---------- | ------- | --- | ----------- | --- | ---- | ---------- | --- |
Internet and receive a trade confirmation. We will be sending our
pseudotradestotheFinancialMarketsExchange,FMEX,whichisa
server that will receive FMML “trades,” post them in a database,
| and send | back | FMML trade | confirmations. |     | Once you | have | placed |
| -------- | ---- | ---------- | -------------- | --- | -------- | ---- | ------ |
yourtrade,youcanseewhethertheFMEXhasreceiveditathttp://
yorkville.rice.iit.edu:8100/servlet/fmex.GetTrades.Thiswebsiteshows
Team-LRN

316 AdvancedVB.NET
the contents of the FMEX database. So if your FMML document
was successfully received, it will be viewable on this site.
Step6 TocommunicatewiththeFMEXovertheInternet,we
will need to create a few objects that are based upon
classes found in the System.Net and System.XML
namespaces. Add the Imports System.Net and
Imports System.XML code at the very top of the
Form1 code window. In the general declarations
section of the Form1 code window, declare the
following objects:
Dim myUrl As Uri
Dim myReq As WebRequest
Dim myRes As WebResponse
Dim myReader As XmlTextReader
A URI is an object representation of a URL. AWebRequest object,
foundintheSystem.Netnamespace,makesarequesttoaURIover
theInternet.AWebResponseobjectsreceivesamessagefromaURI.
An XmlTextReader object, found in the System.XML name-
space,givesusfast,read-onlyaccesstoanXMLstream.Sobyusing
an XMLTextReader to read a stream, we will be implementing a
formofSAXparsertomakesuretheXMLmessageiswellformed.
However, an XmlTextReader object will not perform data
validation against a DTD. To perform data validation, we could
use an XmlValidatingReader object, but creating a full, validating
parser is beyond the scope of this chapter.
Step 7 Change the Button1_Click event to include the
following code:
Private Sub Button1_Click(ByVal sender As ...) Handles Button1.Click
Dim strCurrentTag, strStatus, strBuySell, strQty, strTicker, _
strPrice, strDate, strXMLtrade As String
strXMLtrade = "<?xml version = ’1.0’?>"
strXMLtrade += "<!DOCTYPE Tradedoc SYSTEM _
’http://yorkville.rice.iit.edu:8100/FMML.dtd’>"
strXMLtrade += "<Tradedoc>"
’ This code is the same as before.
strXMLtrade += "</Tradedoc>"
myUrl = New _
Uri("http://yorkville.rice.iit.edu:8100/servlet/fmex.XMLTrade?xmlfile=" _
& strXMLtrade)
myReq = WebRequest.Create(myUrl)
Team-LRN

XML 317
Try
myRes = myReq.GetResponse
myReader = New XmlTextReader(myRes.GetResponseStream())
Do While (myReader.Read())
If myReader.NodeType = XmlNodeType.Element Then
strCurrentTag = myReader.Name
End If
If myReader.NodeType = XmlNodeType.Text Then
Select Case strCurrentTag
Case "Status"
strStatus = myReader.Value
Case "BuySell"
strBuySell = myReader.Value
Case "Quantity"
strQty = myReader.Value
Case "Ticker"
strTicker = myReader.Value
Case "Price"
strPrice = myReader.Value
Case "Time"
strDate = myReader.Value
End Select
End If
Loop
myReader.Close()
Catch exc As Exception
MsgBox(exc.Message)
Exit Sub
End Try
lblConfirm.Text = strStatus & " " & strBuySell & " " & strQty & " _
" & strTicker & " at " & strPrice & " at " & strDate
End Sub
Step 8 One last thing: Add a label named lblConfirm to the
bottom of your Form1.
Step 9 Run the program (see Figure 18.4).
You can view the FMEX server at http://yorkville.rice.ii-
t.edu:8100/servlet/fmex.GetTrades. When the server receives your
“trade,” it will be posted on this website.
XML DATA SOURCES
ADO.NET provides additional functionality that allows us to
convert data in a database into XML. VB.NET DataSet objects
providemethodsthatcreateXMLdocumentsfromadatatableand
that also can convert XML data into a data source. This is
accomplished through the use of the GetXML(), WriteXML, and
ReadXML() member methods. Let’s look at a quick example:
Team-LRN

| 318   |        |      |     |        |         |             | AdvancedVB.NET |       |
| ----- | ------ | ---- | --- | ------ | ------- | ----------- | -------------- | ----- |
| F I G | U R E  | 18.4 |     |        |         |             |                |       |
| Step  | 1 Open | a    | new | VB.NET | Windows | application |                | named |
XMLdatasource.
| Step | 2 To | your | Form1 | add | a text | box with | the | multilane |
| ---- | ---- | ---- | ----- | --- | ------ | -------- | --- | --------- |
propertyturnedtoTrueandwithaverticalscrollbar.
|      | Also     | add | a         | button | and     | a data grid. | Leave | these   |
| ---- | -------- | --- | --------- | ------ | ------- | ------------ | ----- | ------- |
|      | controls |     | with      | their  | default | names.       |       |         |
| Step | 3 Add    | the | following |        | code    | to the Form1 | code  | window: |
Imports System.Data.OleDb
| Public Class  | Form1                     |           |     |       |     |     |     |     |
| ------------- | ------------------------- | --------- | --- | ----- | --- | --- | --- | --- |
| Inherits      | System.Windows.Forms.Form |           |     |       |     |     |     |     |
| [Windows Form | Designer                  | generated |     | code] |     |     |     |     |
Team-LRN

XML 319
F I G U R E 18.5
Team-LRN

320 AdvancedVB.NET
Private Sub Button1_Click(ByVal sender As ...) Handles Button1.Click
Dim myConnect As New _
OleDbConnection("Provider=Microsoft.Jet.OLEDB.4.0;Data _
Source=C:\ModelingFM\Options.mdb")
Dim myAdapter As New OleDbDataAdapter("Select * From OptionTrades, _
myConnect)
Dim myDataSet As New DataSet()
myConnect.Open()
myAdapter.Fill(myDataSet, "myData")
DataGrid1.DataSource = myDataSet
DataGrid1.DataMember = "myData"
myDataSet.WriteXml("OptionTrades.XML")
TextBox1.Text = myDataSet.GetXml()
myConnect.Close()
End Sub
End Class
Step 4 Run the program. It should look like Figure 18.5.
SUMMARY
This chapter presented the basics of the XML language, which is
reallyametalanguage.WeusedXMLtocreateourownmessaging
protocol, which we named FMML. All XML messages should be
bothwellformedandvalidaccordingtosomeDTD.Inthechapter
we broke down the elements of the FMML.dtd file to gain an
understanding of elements, tags, attributes, entities, CDATA, and
PCDATA. Furthermore, we briefly discussed parsers, which are
programs that read XML files. Finally, we used some of VB.NET’s
System.Net and System.XML namespace objects to communicate
over the Internet with a server using the FMML protocol.
Inthefollowingchapterwewilllookatsomereal-worldXML
protocols used every day in the financial markets.
Team-LRN

XML 321
PROBLEMS
| 1. What    | is a metalanguage? |                    |                   |           |
| ---------- | ------------------ | ------------------ | ----------------- | --------- |
| 2. What    | is the             | difference between | a well-formed     | XML mess- |
| age and    | a valid            | one?               |                   |           |
| 3. What    | is FMML,           | and how is it      | different from    | XML?      |
| 4. What    | is a DTD?          |                    |                   |           |
| 5. What    | objects            | are contained      | in the System.Net | and       |
| System.XML |                    | namespaces?        |                   |           |
Team-LRN

322 AdvancedVB.NET
| PROJECT | 18.1 |     |
| ------- | ---- | --- |
Trade confirmations received from FMEX should be posted in the
OptionTradestableoftheOptions.mdbdatabase.CreateaVB.NET
Windows application that inserts the necessary information into
| the appropriate | columns | in the table. |
| --------------- | ------- | ------------- |
| PROJECT         | 18.2    |               |
As trades are made on FMEX, your portfolio will change. Create a
VB.NETapplicationthatwillholdcallandputobjectsinaportfolio.
Be sure to add the functionality necessary to keep track of your
| portfolio statistics | in real | time. |
| -------------------- | ------- | ----- |
Team-LRN

| C         | H A | P T       | E R 19  |     |     |     |     |
| --------- | --- | --------- | ------- | --- | --- | --- | --- |
| XML       |     | Protocols |         |     | in  |     |     |
| Financial |     |           | Markets |     |     |     |     |
A
lthoughelectronictradinghasbecomewidespreadoverthelast
decade, communication between institutional trading firms is still
| often      | done | using    | such last-millennium |        |     | technologies | as the |
| ---------- | ---- | -------- | -------------------- | ------ | --- | ------------ | ------ |
| telephone. |      | Over the | coming               | years, | the | advantages   | of new |
technologies such as XML will change the way all companies do
business, but especially those involved in the financial markets
since the details of virtually all tradable instruments can be
represented and communicated in digital format. Furthermore, as
| we have | argued |     | in this | book, financial |     | industry | firms will |
| ------- | ------ | --- | ------- | --------------- | --- | -------- | ---------- |
increasingly use electronic trading systems (to select trades and
manage portfolios) and electronic markets (to execute trades). The
benefits of an entirely electronic platform will pave the way for
straight-through processing (STP). STP will require the trans-
mission of trade information across electronic networks using a
| common | messaging |     | protocol. |     |     |     |     |
| ------ | --------- | --- | --------- | --- | --- | --- | --- |
STPisasetofbusinessprocessesthatwillonedayachievethe
goal of automating end-to-end trade processing for all financial
instruments, thereby streamlining back-office activities and low-
| ering | trading | costs. | Thanks | to the | advent | of  | web services |
| ----- | ------- | ------ | ------ | ------ | ------ | --- | ------------ |
technology and messaging protocols, the focus of attention with
regard to STP is moving away from issues relating to connectivity
| between | software |             | applications    | and        | more     | toward      | the business |
| ------- | -------- | ----------- | --------------- | ---------- | -------- | ----------- | ------------ |
| content | of the   | information | being           | exchanged. |          |             |              |
| As      | we       | showed      | in the previous |            | chapter, | a messaging | protocol     |
suchasFMMLcanbecreatedanddefinedasastandardizedwayof
323
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

324 AdvancedVB.NET
communicating trade information between two market partici-
pantswithoutthenecessityofhumanintervention.Processessuch
as this, where the messaging protocol is not identical to a
proprietary data description methodology, are the very definition
of the issues around connectivity and system interoperability.
System interoperation permits individual market participants to
sharethefixedcostsoftechnologicalinfrastructuredevelopmentas
well as the benefits of subsequently lower transaction costs.
Within the financial markets industry, several XML protocols
have been developed for system interoperation within specific
industrysegments.TheseXMLstandardsprovideaframeworkfor
encodinginformationrelatingtodifferentpartsoftheindustryand
are being promoted by consortiums and organizations that set
documentdefinitionsintheformofXMLDTDsorschemas.Aswe
learnedinthepreviouschapter,aDTDdescribesthevalidstructure
and sequence of a message spoken in a particular dialect of XML.
ThemostinterestingoftheseXMLprotocolsordialectsusedinthe
financial markets are:
^ FIX/FIXML. FIXML is the XML version of FIX.
^ FpML. The Financial Products Markup Language.
^ Swift/SwiftML. SwiftML is the XML version of Swift.
^ RIXML. The Research Information Exchange Markup
Language.
^ MDDL. The Market Data Definition Language.
^ FinXML.
^ SFXL. The Securities Financing Extensible Markup
Language.
^ OFX. Open Financial Exchange.
^ XBRL. The Extensible Business Reporting Language.
^ IFX. Interactive Financial Exchange.
^ IRML. The Investment Research Markup Language.
^ XFRML. The Extensible Financial Research Markup
Language.
^ MDML. The Market Data Markup Language.
^ WeatherML. The Weather Markup Language.
^ STPML. The Straight-through Processing Markup
Language.
Team-LRN

| XMLProtocolsinFinancialMarkets |     |                 |     |                |     |          |        |          | 325     |
| ------------------------------ | --- | --------------- | --- | -------------- | --- | -------- | ------ | -------- | ------- |
| As                             | you | can imagine,    |     | an institution |     | of any   | size   | may      | need to |
| support                        | a   | multiplicity    | of  | standards      |     | within   | its    | trading, | risk    |
| management,                    |     | and back-office |     | systems.       |     | The most | widely |          | used of |
theprotocolsmentionedabove,however,areFIX,Swift,andFpML.
| Both Swift, |     | promoted | by  | the Society |     | for Worldwide |     | Interbank |     |
| ----------- | --- | -------- | --- | ----------- | --- | ------------- | --- | --------- | --- |
FinancialTelecommunications,andFIX,promotedbyFIXProtocol,
Ltd. (FPL), are currently non-XML protocols, but they are being
| converted | to  | XML | formats | known |     | as SwiftML |     | and | FIXML, |
| --------- | --- | --- | ------- | ----- | --- | ---------- | --- | --- | ------ |
respectively.
Furthermore,sincethereisobviouslyafairamountofoverlap
between the protocols listed, we will likely see convergence of the
| standards | over | the | coming | years. | In  | fact, | the FPL | and | Swift |
| --------- | ---- | --- | ------ | ------ | --- | ----- | ------- | --- | ----- |
organizationshaverecentlyagreedtoteamupandmergetheirtwo
messagingstandardsintoasingle,ISO15022XML-basedprotocol.
[ISO 15022 is the current International Standards Organization
| (ISO) | standard | that | defines | electronic |     | messages |     | exchanged |     |
| ----- | -------- | ---- | ------- | ---------- | --- | -------- | --- | --------- | --- |
between institutions involved in the securities industry.] It is
hoped that the new XML protocol will combine FIX’s agility in
tradeexecutionandSwift’spost-tradetalentstofurtherthegoalof
| straight-through |     | processing. |     |     |     |     |     |     |     |
| ---------------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
Ratherthandelveintoeachofthelistedprotocolsindepth,we
willbrieflydiscussFpMLandthenfocusinmoredepthonFIXML,
leaving it to the reader to further investigate the others should the
need arise. Whatever the case, since all the other listed standards
areXML-basedprotocols,messageswritteninanyoftheseformats
mustbewell-formedXMLdocumentsandvalidaccordingtotheir
| respective | DTDs. |     |     |     |     |     |     |     |     |
| ---------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
FpML
| The Financial |     | Products | Markup |             | Language |         | (FpML)           | is a | freely |
| ------------- | --- | -------- | ------ | ----------- | -------- | ------- | ---------------- | ---- | ------ |
| licensed      | XML | protocol |        | for trading |          | complex | over-the-counter |      |        |
financial derivative instruments, including equity, interest rate,
andforeignexchangederivativessuchasoptions,spots,forwards,
| swaps,   | and | swaptions. | Eventually     |     | it  | is hoped   | that | FpML    | will |
| -------- | --- | ---------- | -------------- | --- | --- | ---------- | ---- | ------- | ---- |
| automate | the | flow       | of information |     | for | electronic |      | trading | and  |
confirmations in all the types of negotiated OTC derivatives.
Team-LRN

326 AdvancedVB.NET
Let’s take a look at a sample FpML message taken from the
FpML Version 2.0 documentation, which can be found at
www.FpML.org. As you will see, this document contains the
information about a forward rate agreement trade. In some areas
we have abbreviated less interesting content.
On May 14, 1991, ABN AMRO Bank and Midland Bank
entered into a forward rate agreement in which ABN AMRO was
the seller of the contract and Midland was the buyer. The terms of
the contract are as follows:
^ Effective date: 01/07/1991
^ Termination date: 01/17/1992
^ Notional amount: CHF 25,000,000
^ Fixed rate: 4.00%
^ Day count fraction: Actual/360
HereisanXMLrepresentationofthisOTCtradeofaforward
rate agreement using the FpML protocol:
<?xml version="1.0" ?>
<FpML version="2-0" BusinessCenterSchemeDefault=http://www.fpml.org/...>
<trade>
<tradeHeader>
<partyTradeIdentifier>
<partyReference href="#MIDLAND" />
<tradeId tradeIdScheme="http://www.hsbc.com/...>123</tradeId>
</partyTradeIdentifier>
<partyTradeIdentifier>
<partyReference href="#ABNAMRO" />
<tradeId tradeIdScheme="http://www.abnamro.com/...>456</tradeId>
</partyTradeIdentifier>
<tradeDate>1991-05-14</tradeDate>
</tradeHeader>
<fra>
<buyerPartyReference href="#MIDLAND" />
<sellerPartyReference href="#ABNAMRO" />
<adjustedEffectiveDate id="resetDate">1991-07-17 _
</adjustedEffectiveDate>
<adjustedTerminationDate>1992-01-17</adjustedTerminationDate>
<paymentDate>
<unadjustedDate>1991-07-17</unadjustedDate>
<dateAdjustments>
<businessDayConvention>FOLLOWING</businessDayConvention>
<businessCenters>
<businessCenter>CHZU</businessCenter>
</businessCenters>
</dateAdjustments>
</paymentDate>
<fixingDateOffset>
Team-LRN

XMLProtocolsinFinancialMarkets 327
<periodMultiplier>-2</periodMultiplier>
<period>D</period>
<dayType>Business</dayType>
<businessDayConvention>NONE</businessDayConvention>
<businessCenters>
<businessCenter>GBLO</businessCenter>
</businessCenters>
<dateRelativeTo href="#resetDate">ResetDate</dateRelativeTo>
</fixingDateOffset>
<dayCountFraction>ACT/360</dayCountFraction>
<calculationPeriodNumberOfDays>184</calculationPeriodNumberOfDays>
<notional>
<currency>CHF</currency>
<amount>25000000.00</amount>
</notional>
<fixedRate>0.04</fixedRate>
<floatingRateIndex>CHF-LIBOR-BBA</floatingRateIndex>
<indexTenor>
<periodMultiplier>6</periodMultiplier>
<period>M</period>
</indexTenor>
<fraDiscounting>true</fraDiscounting>
</fra>
<party Id="MIDLAND">
<partyId>MIDLGB22</partyId>
</party>
<party id="ABNAMRO">
<partyId>ABNANL2A</partyId>
</party>
</trade>
</FpML>
AlthoughthisXMLdocumentisquitelengthy,youshouldbe
able to not only read it but, based upon what we learned in the
previous chapter, also understand the underlying structure and
determine how it may be created in VB.NETand how it could be
sent to a URL over the Internet. Now let’s look in more depth at
FIXML.
FIX AND FIXML
The Financial Information Exchange (FIX) protocol is a public
domain, non-XML messaging standard targeted toward insti-
tutionaltradingof exchange-traded securitiesand derivatives.FIX
was originally designed by Salomon Brothers and Fidelity to
automate messages between themselves, but over the years it has
becomewidelyusedbymostmajormarketparticipants.TodayFIX
Team-LRN

328 AdvancedVB.NET
Protocol,Ltd.(FPL),anindustryconsortium,overseestheongoing
development of FIX and FIXML, the XML version of the FIX
protocol.
FPL has designed FIX for the express purpose of commu-
nicating trades electronically and exchanging transaction data in
real time between exchanges, ECNs, FCMs, and broker-dealers.
Every day, FIX-compliant trading institutions and exchanges use
FIX to route and manage their flow of orders and confirmation
information more quickly and efficiently than prior or alternative
methods. The use of FIX messages greatly reduces the time and
expense necessary to perform transactions and transaction
processing in the financial markets. Due to its wide acceptance
by securities and derivatives exchanges as well as their member
firms, FIX is becoming a necessary and integral component of any
real-time trading system.
FIXML, on the other hand, is an attempt by the FPL
consortiumtocreateanXMLversionofFIX.Thatis,theconsortium
is aiming to rewrite the FIX protocol in XML. As we have learned,
sinceFIXMLisanXML-basedlanguage,thedefinitionofFIXMLis
encompassed in a DTD that is available on the Internet, as we will
see shortly. Although FIXML is only now narrowly used in the
industry,FPLisdesigningitinsuchawayastominimizeeffortand
expense for FIX-compliant firms to convert to it from their legacy
FIX-based systems. In general, FIXML simply takes FIX tag values
and represents them in XML format. The new FIXML messages
then are actually put inside the established FIX headers and
trailers.TheresultisthatFIXfirmscanconverttoFIXMLbysimply
adding an XML parser on top of their existing FIX engine.
Alternatively,FIXMLmessagescanalsostandontheirownoutside
the FIX framework.
Although FIXML messages are bigger and therefore require
more bandwidth than traditional FIX messages, the advantages of
usinganXMLformat,andtheadditionalfunctionalitiesitenables,
clearlyoutweighthedisadvantages.Oneofthebiggestadvantages
of the XML format is that it allows for interoperation between
FIXMLsystemsandothersimilarstandardssuchasOFX.Software
applications can easily pass fields through to connected systems
that use other DTDs to, for example, describe trades in terms of
price, quantity, and security name.
Team-LRN

XMLProtocolsinFinancialMarkets 329
| As we | have said, | over | the | long run | the use | of XML formats, |
| ----- | ---------- | ---- | --- | -------- | ------- | --------------- |
likeFIXML,SwiftML,andOFX,willmotivateaconvergenceofthe
variousprotocols.Theultimateprizewillbeasingledictionaryfor
theentirefinancialindustry,whichwillclearlyeasethetransitionto
| straight-through | processing. |     |     |     |     |     |
| ---------------- | ----------- | --- | --- | --- | --- | --- |
Aswementionedbefore,justaswithanyXMLstandard,there
isacorrespondingDTDwithFIXML.Itisknownasfixmlmain.dtd
| and is available | on      | the FPL | website, | www.FIXprotocol.org. |           |              |
| ---------------- | ------- | ------- | -------- | -------------------- | --------- | ------------ |
| Before           | we dive | in to   | creating | a FIXML              | document, | let’s take a |
quick look at some peculiarities of FIXML. FIXML messages, of
course,requirethatthecontentofamessagebeordered.Thatis,as
withanyXMLprotocol,elementsmustbeinaspecificorder.Also,
FIXML supports conditionally required content. So, for example,
options trades must contain the ,StrikePrice> element, whereas
futures trades do not. And lastly, FIXML makes use of certain
commonly used and well-known financial abbreviations. Here are
some examples:
|        | Abbreviation |          |     | Description          |         |                |
| ------ | ------------ | -------- | --- | -------------------- | ------- | -------------- |
|        | Amt          |          |     | Amount               |         |                |
|        | Comm         |          |     | Commission           |         |                |
|        | Comp         |          |     | Company              |         |                |
|        | Curr         |          |     | Currency             |         |                |
|        | DK           |          |     | Don’tknow            |         |                |
|        | Exch         |          |     | Exchange             |         |                |
|        | Forex        |          |     | Foreign              |         |                |
|        | Fut          |          |     | Futures              |         |                |
|        | ID           |          |     | Identifier           |         |                |
|        | IOI          |          |     | Indicationofinterest |         |                |
|        | Mkt          |          |     | Market               |         |                |
|        | Opt          |          |     | Option               |         |                |
|        | Ord          |          |     | Order                |         |                |
|        | Px           |          |     | Price                |         |                |
|        | Qty          |          |     | Quantity             |         |                |
| In the | following    | example, |     | we will              | build a | FIXML document |
step-by-step,element-by-element,fromthegroundup.Further,we
will be able to modify this document for use with equity trades,
options trades, and futures trades. As with all XML messages,
FIXML documents start with headers, including the XML version
| and the FIXML  | document |          | type, | which     | defines | the DTD against |
| -------------- | -------- | -------- | ----- | --------- | ------- | --------------- |
| which a parser | will     | validate | the   | document. |         |                 |
Team-LRN

| 330   |               |     |                  |     |     |     | AdvancedVB.NET |     |
| ----- | ------------- | --- | ---------------- | --- | --- | --- | -------------- | --- |
| <?xml | version=’1.1’ |     | encoding=‘UTF-8’ |     | ?>  |     |                |     |
<?DOCTYPE FIXML SYSTEM ’http://www.fixprotocol.org/specification/ _
fixml4.3v1.0.dtd’>
| Next | we add | the | root | element | ,FIXML> |     | with opening | and |
| ---- | ------ | --- | ---- | ------- | ------- | --- | ------------ | --- |
closing tags.
| <?xml     | version=’1.1’ |       | encoding=’UTF-8’ |            |     |        | ?>  |     |
| --------- | ------------- | ----- | ---------------- | ---------- | --- | ------ | --- | --- |
| <?DOCTYPE |               | FIXML | SYSTEM           | ’http:\... |     | .dtd’> |     |     |
<FIXML>
</FIXML>
AccordingtotheDTD,a<FIXML>elementcancontainoneor
| more <FIXMLMessage> |              |     | elements. |     | A                     | <FIXMLMessage> |     | must |
| ------------------- | ------------ | --- | --------- | --- | --------------------- | -------------- | --- | ---- |
| contain             | one <Header> |     | and       | one | <ApplicationMessage>. |                |     | The  |
<Header> element will contain the information about the parties
involvedinatransaction.The<ApplicationMessage>elementwill
| contain   | information   | about | the              | transaction |     | itself. |     |     |
| --------- | ------------- | ----- | ---------------- | ----------- | --- | ------- | --- | --- |
| <?xml     | version=’1.1’ |       | encoding=’UTF-8’ |             |     |         | ?>  |     |
| <?DOCTYPE |               | FIXML | SYSTEM           | ’http:\...  |     | .dtd’>  |     |     |
<FIXML>
<FIXMLMessage>
<Header>
</Header>
<ApplicationMessage>
</ApplicationMessage>
</FIXMLMessage>
</FIXML>
| The | <Header> | element |     | must | contain |     | a <Sender> | and a |
| --- | -------- | ------- | --- | ---- | ------- | --- | ---------- | ----- |
<Target>element. Optionally it can also contain an<onBehalfOf>,
| <DeliverTo>, | <SendingTime>, |     |     | <PossDupFlag>, |     |     | or <PossResend> |     |
| ------------ | -------------- | --- | --- | -------------- | --- | --- | --------------- | --- |
element.
<Header>
<Sender>
</Sender>
<Target>
</Target>
<SendingTime/>
</Header>
| The      | <Sender> | and        | <Target> |           | elements |       | must each     | contain |
| -------- | -------- | ---------- | -------- | --------- | -------- | ----- | ------------- | ------- |
| <CompID> | and      | optionally |          | a <SubID> |          | and a | <LocationID>. |         |
Team-LRN

| XMLProtocolsinFinancialMarkets |     |     |     |     |     |     | 331 |
| ------------------------------ | --- | --- | --- | --- | --- | --- | --- |
<Header>
<Sender>
<CompID></CompID>
<SubID></SubID>
</Sender>
<Target>
<CompID></CompID>
<SubID></SubID>
</Target>
<SendingTime/>
</Header>
| We  | can complete | the header |     | by adding | some | data. |     |
| --- | ------------ | ---------- | --- | --------- | ---- | ----- | --- |
<Header>
<Sender>
<CompID>BVV</CompID>
<SubID>BEN</SubID>
</Sender>
<Target>
<CompID>BH</CompID>
<SubID>Bob</SubID>
</Target>
<SendingTime>20030203-9:30:00</SendingTime>
</Header>
Nowthatthe<Header>iscomplete,wecanturnourattention
to the <ApplicationMessage> content. The <ApplicationMessage>
element can contain one of several elements, including but not
limitedtothefollowing:<Advertisement>,<Indication>,<News>,
| <Email>,           | <QuoteReq>,                 | <Quote>,      |     | <Order>,              |     | <ExecutionReport>, |          |
| ------------------ | --------------------------- | ------------- | --- | --------------------- | --- | ------------------ | -------- |
| <DK_Trade>,        | <OrderModificationRequest>, |               |     |                       |     | <OrderCancelRe-    |          |
| quest>,            | <OrderCancelReject>,        |               |     | <OrderStatusRequest>, |     |                    | <Settle- |
| mentInstructions>, |                             | <MarketData>, |     | <MarketDataReq>,      |     |                    | <Quote-  |
Cancel>, and <SecurityStatus>. For the purposes of this example,
| we are | sending an | order. |     |     |     |     |     |
| ------ | ---------- | ------ | --- | --- | --- | --- | --- |
<ApplicationMessage>
<Order>
</Order>
</ApplicationMessage>
| The         | <Order>       | element | must    | include         | tags | for | <ClOrdID>, |
| ----------- | ------------- | ------- | ------- | --------------- | ---- | --- | ---------- |
| <HandInst>, | <Instrument>, |         | <Side>, | <TransactTime>, |      |     | <Order-    |
Team-LRN

| 332        |     |              |     |             |     |         | AdvancedVB.NET |
| ---------- | --- | ------------ | --- | ----------- | --- | ------- | -------------- |
| Quantity>, | and | <OrderType>. |     | Optionally, |     | <Order> | can also       |
include other tags such as <ClientID>, <ExecBroker>, <Account>,
| <PrevClosePx>, |     | <Currency>, |     | <OrderDuration>, |     |     | <Commission>, |
| -------------- | --- | ----------- | --- | ---------------- | --- | --- | ------------- |
<Rule80A>, <Text>, <ClearingFirm>, or <ClearingAcct>. For this
| example      | we will    | include  | the          | required | elements |     | as well as the |
| ------------ | ---------- | -------- | ------------ | -------- | -------- | --- | -------------- |
| optional     | <Currency> | element. |              |          |          |     |                |
| Furthermore, |            | the      | <Instrument> |          | element  |     | will contain a |
required <Symbol> element and may include one of the optional
| elements        | such | as <SymbolSfx>, |     | <SecurityID>, |     | <SecurityType>, |     |
| --------------- | ---- | --------------- | --- | ------------- | --- | --------------- | --- |
| <SecurityExch>, |      | and <Issuer>.   |     |               |     |                 |     |
<ApplicationMessage>
<Order>
<ClOrdID></ClOrdID>
|     |     | <HandInst | />  |     |     |     |     |
| --- | --- | --------- | --- | --- | --- | --- | --- |
<Instrument>
<Symbol></Symbol>
<SecurityType></SecurityType>
</Instrument>
|     |     | <Side | />  |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- |
<TransactTime></TransactTime>
<OrderQuantity></OrderQuantity>
<OrderType></OrderType>
|     |     | <Currency | />  |     |     |     |     |
| --- | --- | --------- | --- | --- | --- | --- | --- |
</Order>
</ApplicationMessage>
| Now        | let’s add | some  | parsed    | character |     | data as | well as some |
| ---------- | --------- | ----- | --------- | --------- | --- | ------- | ------------ |
| attributes | to our    | order | elements. |           |     |         |              |
<ApplicationMessage>
<Order>
<ClOrdID>12345</ClOrdID>
|     |     | <HandInst | Value="1"/> |     |     |     |     |
| --- | --- | --------- | ----------- | --- | --- | --- | --- |
<Instrument>
<Symbol></Symbol>
<SecurityType></SecurityType>
</Instrument>
|     |     | <Side Value="1"/> |     |     |     |     |     |
| --- | --- | ----------------- | --- | --- | --- | --- | --- |
<TransactTime>20030203-9:30:00</TransactTime>
<OrderQuantity></OrderQuantity>
<OrderType></OrderType>
|     |     | <Currency | Value="USD"/> |     |     |     |     |
| --- | --- | --------- | ------------- | --- | --- | --- | --- |
</Order>
</ApplicationMessage>
Team-LRN

| XMLProtocolsinFinancialMarkets |      |        |          |      |        |              |     |          | 333 |
| ------------------------------ | ---- | ------ | -------- | ---- | ------ | ------------ | --- | -------- | --- |
| Let’s                          | take | a more | in-depth | look | at the | <Instrument> |     | element. |     |
The <SecurityType> element may contain elements corresponding
| to the         | different | tradable           |     | instruments, |           | including |               | <Equity>, |       |
| -------------- | --------- | ------------------ | --- | ------------ | --------- | --------- | ------------- | --------- | ----- |
| <FixedIncome>, |           | <ForeignExchange>, |     |              | <Future>, |           | <MutualFund>, |           |       |
| <Option>,      | and       | <Warrant>.         |     | The format   | for       | a common  |               | stock     | trade |
| looks like     | this:     |                    |     |              |           |           |               |           |       |
<Instrument>
<Symbol>IBM</Symbol>
<SecurityType>
|     |     | <Equity |     | Value="CS"> |     |     |     |     |     |
| --- | --- | ------- | --- | ----------- | --- | --- | --- | --- | --- |
</SecurityType>
</Instrument>
The format for a call <Option> trade looks like the following
example.Inthisexample,aputisacode“0”andacallisacode“1”.
<Instrument>
<Symbol>IBM</Symbol>
<SecurityType>
<Option>
|     |     |     | <PutCall |     | Value="1"/> |     |     |     |     |
| --- | --- | --- | -------- | --- | ----------- | --- | --- | --- | --- |
<Maturity>
<MonthYear>200304</MonthYear>
</Maturity>
<StrikePx>80.00</StrikePx>
</Option>
</SecurityType>
</Instrument>
Nowlet’stakealookatthefinishedFIXMLdocument,which
| incorporates |     | the <Header> |             | and the | <ApplicationMessage> |                 |     |          | along |
| ------------ | --- | ------------ | ----------- | ------- | -------------------- | --------------- | --- | -------- | ----- |
| with some    |     | additional   | information |         | for                  | <OrderQuantity> |     |          | and   |
| <OrderType>. |     | In           | this final  | message |                      | we have         |     | included | the   |
<Instrument> element for the purchase of 10 IBM April 80 call
| options             | at a | limit price      | of  | $5.00. |     |     |     |     |     |
| ------------------- | ---- | ---------------- | --- | ------ | --- | --- | --- | --- | --- |
| <?xml version=’1.0’ |      | encoding=’UTF-8’ |     | ?>     |     |     |     |     |     |
<!DOCTYPE FIXML SYSTEM ’http://www.fixprotocol.org/specification/ -
fixml4.3v1.0.dtd’>
<FIXML>
<FIXMLMessage>
<Header>
<Sender>
<CompID>BVV</CompID>
Team-LRN

334 AdvancedVB.NET
<SubID>BEN</SubID>
</Sender>
<Target>
<CompID>BH</CompID>
<SubID>Bob</SubID>
</Target>
<SendingTime>20030203-9:30:00</SendingTime>
</Header>
<ApplicationMessage>
<Order>
<ClOrdID>12345</ClOrdID>
<HandInst Value=’1’/>
<Instrument>
<Symbol>IBM</Symbol>
<SecurityType>
<Option>
<PutCall Value=’1’/>
<Maturity>
<MonthYear>200304</MonthYear>
</Maturity>
<StrikePx>80.00</StrikePx>
</Option>
</SecurityType>
</Instrument>
<Side Value=’1’/>
<TransactTime>20030203-9:30:00</TransactTime>
<OrderQuantity>
<OrderQty>10</OrderQty>
</OrderQuantity>
<OrderType>
<LimitOrder>
<Price>5.00</Price>
</LimitOrder>
</OrderType>
<Currency Value=’USD’/>
</Order>
</ApplicationMessage>
</FIXMLMessage>
</FIXML>
OntheCD,thefilesampleFIXML.xmlcontainsthecompleted
code above. Try opening this file in Internet Explorer. Since this
FIXMLmessageisbothwellformedandvalid,theonlythingleftto
do is to build a VB.NETapplication that creates FIXML messages.
This program mimics the FMML program in the previous
chapter and creates a FIXML document.
Step1 InVB.NETcreateanewWindowsapplicationnamed
FIXMLexample.
Step 2 OnyourForm1,addcontrolstobuildtheGUIshown
in Figure 19.1
Team-LRN

XMLProtocolsinFinancialMarkets 335
F I G U R E 19.1
There should be two combo boxes on your form.
Name them cboExchange and cboBuySell. In the
Collection property of cboExchange, add the
elements CBOE, ISE, BOX, AMEX, and FMEX. In
the Collection property of cboBuySell, add the
elements Buy and Sell. Give the text boxes the
appropriate names: txtTicker, txtQuantity, txtPrice,
txtClearingFirm, and txtTrader.
Step 3 To the Form1 code window, add the following code:
Imports System.IO
[Windows Form Designer generated code]
Public Class Form1
Inherits System.Windows.Forms.Form
Private Sub Button1_Click(ByVal sender As ...) Handles Button1.Click
Dim strXMLtrade As String
strXMLtrade = "<?xml version=’1.0’ ?>"
Team-LRN

336 AdvancedVB.NET
| strXMLtrade | &= "<!DOCTYPE | FIXML SYSTEM | _   |
| ----------- | ------------- | ------------ | --- |
’http://www.fixprotocol.org/specification/fixml4.3v1.0.dtd’>"
| strXMLtrade | &= "<FIXML>"        |     |     |
| ----------- | ------------------- | --- | --- |
| strXMLtrade | &= "<FIXMLMessage>" |     |     |
| strXMLtrade | &= "<Header>"       |     |     |
| strXMLtrade | &= "<Sender>"       |     |     |
strXMLtrade &= "<CompID>" & txtClearingFirm.Text & "</CompID>"
| strXMLtrade | &= "<SubID>"   | & txtTrader.Text | & "</SubID>" |
| ----------- | -------------- | ---------------- | ------------ |
| strXMLtrade | &= "</Sender>" |                  |              |
strXMLtrade &= "<Target><CompID>"&cboExchange.Text&"</CompID>
</Target>"
| strXMLtrade | &= "<SendingTime>"           | & Now | & "</SendingTime>" |
| ----------- | ---------------------------- | ----- | ------------------ |
| strxmlTRADE | &= "</Header>"               |       |                    |
| strxmltrade | &= "<ApplicationMessage>"    |       |                    |
| strXMLtrade | &= "<Order>"                 |       |                    |
| strXMLtrade | &= "<ClOrdID>Test</ClOrdID>" |       |                    |
| F I G U R   | E 19.2                       |       |                    |
Team-LRN

XMLProtocolsinFinancialMarkets 337
strXMLtrade &= "<HandInstValue=’1’SDValue=’"&cboBuySell.Text&"’/>"
strXMLtrade &= "<Instrument>"
strXMLtrade &= "<Symbol>" & txtTicker.Text & "</Symbol>"
strXMLtrade &= "<SecurityExchangeValue=’"&cboExchange.Text&"’/>"
strXMLtrade &= "</Instrument>"
strXMLtrade &= "<Side Value=’1’/>"
strXMLtrade &= "<TransactTime>" & Now & "</TransactTime>"
strXMLtrade &= "<OrderQtyData><OrderQty>" & txtQuantity.Text & _
"</OrderQty></OrderQtyData>"
strXMLtrade &= "<OrdTypeValue=’1’SDValue=’"&txtPrice.Text&"’/>"
strXMLtrade &= "</Order>"
strXMLtrade &= "</ApplicationMessage>"
strXMLtrade &= "</FIXMLMessage>"
strXMLtrade &= "</FIXML>"
DimobjWriterAsNewStreamWriter("C:\ModelingFM\myFirstFIXMLdoc.xml")
objWriter.Write(strXMLtrade)
objWriter.Close()
End Sub
Step 4 Run the program (see Figure 19.2).
Since this program produces a well-formed and valid FIXML
document, you may view it in Internet Explorer.
SUMMARY
In this chapter we looked at some real-world XML protocols used
everyday in the financial markets. Specifically, we presented the
basics of the FpML and in more depth, FIXML. As with XML
messages, those written in FpML and FIXML must be both well
formed and valid according to their respective DTDs.
Team-LRN

| 338 |     |     |     |     | AdvancedVB.NET |
| --- | --- | --- | --- | --- | -------------- |
PROBLEMS
| 1. What | is the         | relationship | between  | FIX         | and FIXML?       |
| ------- | -------------- | ------------ | -------- | ----------- | ---------------- |
| 2. What | is FpML        | primarily    |          | used for?   |                  |
| 3. What | are Swift      | and          | SwiftML? |             |                  |
| 4. Why  | is convergence |              | of XML   | protocols   | likely?          |
| 5. What | two            | pieces       | must     | every FIXML | message contain? |
| What    | do these       | two          | elements | represent?  |                  |
Team-LRN

| XMLProtocolsinFinancialMarkets |          |             |             |              |          | 339    |
| ------------------------------ | -------- | ----------- | ----------- | ------------ | -------- | ------ |
| PROJECT                        | 19.1     |             |             |              |          |        |
| Create                         | a VB.NET | Windows     | application | that accepts | user     | inputs |
| regarding                      | an OTC   | derivatives | trade       | and builds   | a valid  | FpML   |
| document.                      | Your     | program     | should      | save this    | document | as     |
myFirstFpMLdoc.xml.
| PROJECT | 19.2 |     |     |     |     |     |
| ------- | ---- | --- | --- | --- | --- | --- |
The program in the chapter does not distinguish between stocks,
futures, and options. Create a VB.NET application that accepts
tradeinformationfromtheusersimilartotheexampleprogramin
the chapter. Add a combo box so the user can select the product
type. Then build the correct FIXML message for the instrument
| type selected | according | to  | the instructions | in the chapter. |     |     |
| ------------- | --------- | --- | ---------------- | --------------- | --- | --- |
Team-LRN

This page intentionally left blank.
Team-LRN

| S E C | T I O N | F I V E |     |
| ----- | ------- | ------- | --- |
Object-Oriented
Programming
| Risk | Management      |                      |                     |
| ---- | --------------- | -------------------- | ------------------- |
| In   | theory, thereis | no differencebetween | theory andpractice. |
| But, | in practice,    | thereis.             |                     |
Janvan de Snepscheut
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

This page intentionally left blank.
Team-LRN

| C       | H A | P T E | R 20     |     |     |     |     |     |     |
| ------- | --- | ----- | -------- | --- | --- | --- | --- | --- | --- |
| Unified |     |       | Modeling |     |     |     |     |     |     |
Language
A
| s we | hope | you have | been | able | to  | see | over the | last | several |
| ---- | ---- | -------- | ---- | ---- | --- | --- | -------- | ---- | ------- |
chapters, object-oriented programming allows us to break down
computerprogramsintoseparateobjectsinaveryintuitiveway.If
| you were | new | to programming |     | when |     | you first | opened | this | book, |
| -------- | --- | -------------- | --- | ---- | --- | --------- | ------ | ---- | ----- |
you may very well have started with Chapter 3, fired up VB.NET,
and started to code. While this approach might work for simple
programs, it will certainly not work for larger ones. For example,
what if you were asked to create a large value-at-risk system to
| monitor | several | automated |     | trading | systems. |     | A project |     | of this |
| ------- | ------- | --------- | --- | ------- | -------- | --- | --------- | --- | ------- |
magnitudeistoobigtoimmediatelystartprogramming.Clearly,a
| good bit | of planning | would     |        | be required   |     | first. |           |        |     |
| -------- | ----------- | --------- | ------ | ------------- | --- | ------ | --------- | ------ | --- |
| In       | order       | to create | larger | applications, |     |        | we should | follow | a   |
detailed planning process for program design. This process must
include a comprehensive analysis of the project requirements and
result in a design, or blueprint, of the objects to be used in the
program, as well as a plan for project completion. As you will no
doubt learn over your career as a financial engineer, quality time
spent on planning will save countless hours of coding and may
| even prevent |     | failure of | projects. |     |     |     |     |     |     |
| ------------ | --- | ---------- | --------- | --- | --- | --- | --- | --- | --- |
Largesoftwareprojectshavelargeprobabilitiesoffailure.Very
| rarely,      | if ever, | do large   |     | software |     | applications |         | meet | all the |
| ------------ | -------- | ---------- | --- | -------- | --- | ------------ | ------- | ---- | ------- |
| requirements |          | as planned |     | on time  | and | within       | budget. |      | Proper  |
planning is the only way to ensure against failure before you start
to program. Furthermore, it is not enough just to plan; be sure to
haveyourdesignsandplansapprovedbymanagementbeforeyou
build anything.
343
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

| 344    |             |     |             |     |                 | Object-OrientedProgramming |         |         |     |
| ------ | ----------- | --- | ----------- | --- | --------------- | -------------------------- | ------- | ------- | --- |
| As     | described   | in  | Chapter     | 2,  | the Kumiega–Van |                            | Vliet   | Trading |     |
| System | Development |     | Methodology |     | requires        |                            | that we | build   | an  |
objectsandprogramdocumentaswellasgainmanagementbuy-in
priortoprogramming.Thisdocumentshouldlayoutalltheobjects
along with all their functionalities that will be needed to construct
| the system. | Again, |     | the | process | should | include | requirements |     |     |
| ----------- | ------ | --- | --- | ------- | ------ | ------- | ------------ | --- | --- |
analysis,todefinethespecificationsofthesoftware;object-oriented
analysis, to provide a framework within which all the objects can
cooperate to satisfy the requirements; and object-oriented design,
to lay out the class hierarchy. Fortunately, there is a graphical
languagecreatedexpresslyforthispurpose—theUnifiedModeling
Language.
| UNIFIED | MODELING |     |     | LANGUAGE |     |     |     |     |     |
| ------- | -------- | --- | --- | -------- | --- | --- | --- | --- | --- |
Although it’s also possible to describe a software system and its
design in words, most developers prefer to use pictures to help
visualize the system’s pieces and the relationships between them.
UML is a way to represent object-oriented applications using a
| standard | set | of graphical |     | notations. | With | UML | we  | can | create |
| -------- | --- | ------------ | --- | ---------- | ---- | --- | --- | --- | ------ |
blueprints in the form of diagrams before we start to program.
| Planning | with | UML | makes | the | entire | software | development |     |     |
| -------- | ---- | --- | ----- | --- | ------ | -------- | ----------- | --- | --- |
processmuchmorestructuredandmakesiteasiertocommunicate
ideas about system architecture. UML is not, however, a project
| management |     | tool. | Project | management |     | tools | and | software |     |
| ---------- | --- | ----- | ------- | ---------- | --- | ----- | --- | -------- | --- |
coordinate the various parts of a software project into a time line
| for completion. |     | UML | diagrams |     | show, | from | an  | architectural |     |
| --------------- | --- | --- | -------- | --- | ----- | ---- | --- | ------------- | --- |
perspective, the objects and the interrelationships between objects
| in a software | application. |     |     |     |     |     |     |     |     |
| ------------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
Wecanmodeljustaboutanyobject-orientedapplicationusing
UML. By creating models first, we can assure ourselves not only
that trading algorithms are completely and correctly formulated,
but also that the thorny issues of object-oriented implementation
| are worked | out | before | construction |     | begins | and | changes | become |     |
| ---------- | --- | ------ | ------------ | --- | ------ | --- | ------- | ------ | --- |
expensive.Blueprintsofclassesandcodemodules,eitherdrawnby
hand or built in a UML software suite, are much easier to change
| than existing | systems. |     |     |     |     |     |     |     |     |
| ------------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
Team-LRN

| UnifiedModelingLanguage |     |     |     |     |     |     | 345 |
| ----------------------- | --- | --- | --- | --- | --- | --- | --- |
In fact, dozens of products are available that facilitate the
creationofUMLdiagrams.Themostwell-knownUMLdesigntool
isRationalRose(www.rational.com).Usingthesetools,wecanbuild
new applications or analyze existing code to reverse-engineer the
UMLdiagrams.Attheextremeend,somesoftwarewillevengoso
| far as to generate   |     | program      | code | from UML | diagrams, | producing |     |
| -------------------- | --- | ------------ | ---- | -------- | --------- | --------- | --- |
| most of a production |     | application. |      |          |           |           |     |
Largeautomatedtradingsystemsmustbestructuredinaway
that facilitates error-free execution and a clear architecture so that
financial engineers can find and fix bugs quickly. UML helps us
visualize trading systemdesign from a technology standpointand
documenttheresultsofthemodelingprocess.Thisvisualizationis
enabledthroughtheuseofUML’stwelvediagramtypes,whichare
defined in three categories—model management, structural, and
| behavior diagrams. |       |     |            |          |     |                 |     |
| ------------------ | ----- | --- | ---------- | -------- | --- | --------------- | --- |
| High-level         | model |     | management | diagrams |     | lay out the way | we  |
organizeandmanagethecomponentsofanapplicationandconsist
of:
^
| Model       | diagrams |          |     |     |     |     |     |
| ----------- | -------- | -------- | --- | --- | --- | --- | --- |
| ^ Subsystem |          | diagrams |     |     |     |     |     |
| ^ Package   | diagrams |          |     |     |     |     |     |
Structuraldiagramsareusedtomodelthestaticstructureofa
| software application |     | and | consist | of: |     |     |     |
| -------------------- | --- | --- | ------- | --- | --- | --- | --- |
^
| Class          | diagrams      |          |      |               |           |            |     |
| -------------- | ------------- | -------- | ---- | ------------- | --------- | ---------- | --- |
| ^ Object       | diagrams      |          |      |               |           |            |     |
| ^ Component    |               | diagrams |      |               |           |            |     |
| ^ Deployment   |               | diagrams |      |               |           |            |     |
| Behavior       | diagrams      |          | show | the different | behaviors | of objects | in  |
| an application | and           | consist  | of:  |               |           |            |     |
| ^ Use          | case diagrams |          |      |               |           |            |     |
| ^ Sequence     |               | diagrams |      |               |           |            |     |
| ^ Activity     | diagrams      |          |      |               |           |            |     |
^
| Collaboration |       | diagrams |     |     |     |     |     |
| ------------- | ----- | -------- | --- | --- | --- | --- | --- |
| ^ State       | chart | diagrams |     |     |     |     |     |
Team-LRN

| 346   |            |     |     |     |          | Object-OrientedProgramming |     |     |     |
| ----- | ---------- | --- | --- | --- | -------- | -------------------------- | --- | --- | --- |
| MODEL | MANAGEMENT |     |     |     | DIAGRAMS |                            |     |     |     |
The process of modeling a software application is a process of
breakingdownalargesystemintosmallerandsmallersubsystems,
becauseassystemsgetlarger,itbecomesmoreandmoredifficultto
| understand  | how        | the          | pieces     | fit together. |            |            |          |             |     |
| ----------- | ---------- | ------------ | ---------- | ------------- | ---------- | ---------- | -------- | ----------- | --- |
| Model       | management |              |            | diagrams      | are        | high-level |          | designs     | to  |
| illustrate  | the        | organization |            | and           | management |            | of       | application |     |
| components. |            | Model        | management |               | diagrams   |            | describe | how         | the |
different pieces of a UML design will fit together. Subsequent
diagrams will refine the details, but for now model management
diagramswillincorporatealltheotherdiagramswewilllookatin
| order to  | show    | how     | the system | is       | structured. |            |       |           |     |
| --------- | ------- | ------- | ---------- | -------- | ----------- | ---------- | ----- | --------- | --- |
|           |         |         | Model      | Diagrams |             |            |       |           |     |
| Our model | diagram |         | follows    | the      | Kumiega–Van |            | Vliet | paradigm  |     |
| presented | in      | Chapter | 2 of       | this     | book for    | developing |       | automated |     |
trading systems. Thus the whole trading system software design
processisdefinedbythemodelscorrespondingtoeachofthefour
| steps along | the  | waterfall. |      |         |          |          |          |          |        |
| ----------- | ---- | ---------- | ---- | ------- | -------- | -------- | -------- | -------- | ------ |
| For         | each | of the     | four | models, | as an    | example, | subsets  |          | of the |
| twelve      | UML  | diagrams   | have | been    | selected | to       | show the | relevant |        |
areasofcommunication.Ineachofthefourmodels,instancesofall
the diagram types may be required, but nonetheless the focus will
| be on the | diagrams  |      | listed in   | Figure         | 20.1.         |     |                |      |       |
| --------- | --------- | ---- | ----------- | -------------- | ------------- | --- | -------------- | ---- | ----- |
| So,       | as shown  |      | in Figure   | 20.1,          | modeling      | of  | the algorithms |      | for   |
| trade     | selection | will | concentrate |                | on structural |     | diagrams       |      | and   |
| package   | diagrams. |      | Data and    | implementation |               |     | models         | will | focus |
on package diagrams and behavior diagrams. Portfolio and risk
managementmodelswillfocusonstructuralclassdiagramsaswell
| as behavior | diagrams. |           |     |     |          |     |     |     |     |
| ----------- | --------- | --------- | --- | --- | -------- | --- | --- | --- | --- |
|             |           | Subsystem |     |     | Diagrams |     |     |     |     |
Softwaresystemsaremadeupofsubsystems.Andsubsystemsare
| made of | packages. |     | A subsystem |     | diagram | breaks | down | a   | model |
| ------- | --------- | --- | ----------- | --- | ------- | ------ | ---- | --- | ----- |
diagram into the constituent subsystems of a software system and
provides a hierarchical view of a system’s overall structure.
Team-LRN

| UnifiedModelingLanguage |        |        |         |     |                    |     |      | 347     |
| ----------------------- | ------ | ------ | ------- | --- | ------------------ | --- | ---- | ------- |
| F I G                   | U R    | E 20.1 |         |     |                    |     |      |         |
| As                      | we saw | in     | Chapter | 2,  | the implementation |     | of a | trading |
system must manage three concurrent processes—trade selection,
| portfolio | management, |     | and        | risk | management. | So      | our subsystem |     |
| --------- | ----------- | --- | ---------- | ---- | ----------- | ------- | ------------- | --- |
| diagram   | organizes   |     | the models |      | into these  | logical | components.   |     |
Examples of the pieces of subsystems are shown in Figure 20.2.
|     |     |     | Package |     | Diagrams |     |     |     |
| --- | --- | --- | ------- | --- | -------- | --- | --- | --- |
Package diagrams break subsystems into packages of classes and
subpackages.Packagessimplifycomplexclassdiagramsandgroup
| together | logically | related  | program |            | elements. |       |         |         |
| -------- | --------- | -------- | ------- | ---------- | --------- | ----- | ------- | ------- |
| We       | draw      | packages | as      | rectangles | with      | small | tabs on | the top |
right-hand side (see Figure 20.3). As we will see, lines of different
| types show | relationships |     |     | between | packages. | We  | might say, | for |
| ---------- | ------------- | --- | --- | ------- | --------- | --- | ---------- | --- |
example,thatonepackagehasarelationshipwithanotherpackage
| if changes | in one | cause  | changes |     | in the other. |     |     |     |
| ---------- | ------ | ------ | ------- | --- | ------------- | --- | --- | --- |
| F I G      | U R    | E 20.2 |         |     |               |     |     |     |
Team-LRN

| 348                  |        |     |                                | Object-OrientedProgramming |     |     |     |
| -------------------- | ------ | --- | ------------------------------ | -------------------------- | --- | --- | --- |
| F I G U R            | E 20.3 |     |                                |                            |     |     |     |
| Thethreesubsystemsin |        |     | ourtradingsystemarepackages.We |                            |     |     |     |
can break down these subsystems further, into other subsystems
and classes.
| The classes | and subpackages |     | in Figure | 20.4 | are | connected | by  |
| ----------- | --------------- | --- | --------- | ---- | --- | --------- | --- |
relationshipstoillustratethefactthatclassessendmessagestoone
another. We will look at these relationships in greater detail when
we examine structural diagrams. One of the arts of UML design is
tominimizethedependenciesbetweenclasses,whichwillhavethe
| result of reducing | the | impact | of changing |     | a class | or package |     |
| ------------------ | --- | ------ | ----------- | --- | ------- | ---------- | --- |
definition.
| Over the | remainder | of  | this chapter, | we  | will not | be able | to  |
| -------- | --------- | --- | ------------- | --- | -------- | ------- | --- |
diagram all the aspects of a trading system in detail. From the
| package diagram | shown | in  | Figure | 20.4, | however, | and | the |
| --------------- | ----- | --- | ------ | ----- | -------- | --- | --- |
knowledge gained over the past chapters, you should be able to
| F I G U R | E 20.4 |     |     |     |     |     |     |
| --------- | ------ | --- | --- | --- | --- | --- | --- |
Team-LRN

| UnifiedModelingLanguage |     |          |     |     |            |     |      |      | 349     |
| ----------------------- | --- | -------- | --- | --- | ---------- | --- | ---- | ---- | ------- |
| piece together          | the | elements |     | and | subsystems |     | of a | full | trading |
system. For this chapter, though, we will focus on a simplified
project implementing portfolio and risk management using value
| at risk and | UML. | The | project | will | encompass |     | the | class | and |
| ----------- | ---- | --- | ------- | ---- | --------- | --- | --- | ----- | --- |
packages defined by the brackets in Figure 20.4. This project will
require that we define the packages and objects we will need to
buildtheapplicationaswellasspecificationsforhowtheseobjects
will interact with each other. The value-at-risk application will
present a subset of the features of UML, but will give you an
understanding of the steps necessary to create an objects and
| program document |         | with | UML. |     |     |     |     |     |     |
| ---------------- | ------- | ---- | ---- | --- | --- | --- | --- | --- | --- |
| VALUE            | AT RISK |      |      |     |     |     |     |     |     |
Value at risk (VaR) is a single number that estimates the possible
dollarlossonaportfolioofsecuritiesandderivativesoveraspecific
time horizon within a given confidence level. This VaR number
aggregatesalltherisks,includingthosethatmightoffseteachother,
in a portfolio into a single number so as to facilitate analysis of
hedging strategies and the discussions about risk with nonquant
personnel.Inthedifferentmarkets,therehavealwaysbeenspecific
risk measurements, such as duration for bonds, delta for options,
andeventhemuch-debatedbetaforstocks.WithVaR,however,we
canestimatetheaggregatedriskofaportfoliocontainingpositions
| in each of | these instruments. |     |         |        |         |      |     |     |        |
| ---------- | ------------------ | --- | ------- | ------ | ------- | ---- | --- | --- | ------ |
| According  | to                 | VaR | theory, | losses | greater | than | the | VaR | number |
can be expected only with a specified probability. For example, a
large trading institution with several hundred positions in dozens
ofmarketsmayquantifyitsvalueatriskbysayingthatthereisa5
percent chance that the firm will lose more than $1.5 million over
| the next month | given |          | the current | portfolio.  |     |        |     |         |     |
| -------------- | ----- | -------- | ----------- | ----------- | --- | ------ | --- | ------- | --- |
| As with        | most  | theories |             | in finance, |     | VaR is | not | without | its |
detractors. Indeed, it is important to understand the limitations of
VaRanalysis.VaRdoesnotestimateeventrisk,nordoesittakeinto
account liquidity differences among the various constituents of a
portfolio. Furthermore, just about every model forcalculating VaR
assumes that the portfolio under consideration will not change
| over the | time horizon. |     | And | lastly, | VaR | models | also | generally |     |
| -------- | ------------- | --- | --- | ------- | --- | ------ | ---- | --------- | --- |
Team-LRN

| 350 |     |     |     |     |     |     | Object-OrientedProgramming |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- |
assumeeitherthathistoricalpricemovementscontaininformation
aboutthefuturedistributionofreturnsorthatfuturereturnswillbe
normally distributed, neither of which may be true. To overcome
the issues inherent in trying to predict the future, several methods
for calculating VaR have been proposed by industry professionals
and academics.
In general, the approaches to VaR calculation fall into three
maincategories—deltanormalorparametric,historicalsimulation,
and Monte Carlo simulation. As we will briefly explain, each of
| these three | approaches |       | has    | its | strengths | and      | weaknesses. |     |     |
| ----------- | ---------- | ----- | ------ | --- | --------- | -------- | ----------- | --- | --- |
|             |            | Delta | Normal |     |           | Approach |             |     |     |
Delta normal, or parametric, approaches to VaR define risk as the
standard deviation of a portfolio’s log returns. We have actually
examined a version of this approach in Chapter10. Although they
are fast and straightforward, the quality of estimates generated by
| delta normal |     | VaR | methodologies |     | break | down | when | instruments |     |
| ------------ | --- | --- | ------------- | --- | ----- | ---- | ---- | ----------- | --- |
with nonlinear payoffs, such as options, are added to the portfolio
or when nonnormal events exist in the distribution of returns.
| Delta | normal |     | VaR usually |     | assumes | a normal |     | distribution | for |
| ----- | ------ | --- | ----------- | --- | ------- | -------- | --- | ------------ | --- |
both the changes in market prices and the changes in portfolio
value,andthecalculationisusuallyasimpletransformationofthe
| estimated | covariance |     | matrix. |            |      |           |            |               |        |
| --------- | ---------- | --- | ------- | ---------- | ---- | --------- | ---------- | ------------- | ------ |
| Delta     | normal     |     | methods | work       | well | for       | portfolios | with          | a very |
| limited   | number     | of  | options | positions. |      | Generally |            | these methods |        |
incorporate options by replacing them with a delta-equivalent
position in the underlying stock, a process called mapping. That
is, an option on a stock is thought of as a position in the stock
accordingtothedeltasinceforsmallchangesinthestockprice,the
| optionacts | likethestock. |     |     | So oncewehavemadethisreplacement, |     |     |     |     |     |
| ---------- | ------------- | --- | --- | --------------------------------- | --- | --- | --- | --- | --- |
we can estimate the risk of the portfolio as a portfolio of stocks.
However, this replacement method typically misstates the risk
| since delta | itself | changes |            | with | changes  | in the   | stock. |         |        |
| ----------- | ------ | ------- | ---------- | ---- | -------- | -------- | ------ | ------- | ------ |
| For         | many   | options | positions, |      | reliance | solely   | on     | delta   | can be |
| misleading. |        | Rather, | delta      | and  | gamma    | together | must   | be used | to     |
predictchangesin option prices givena changein thevalue of the
underlying stock. The error will likely be small, however, for VaR
Team-LRN

UnifiedModelingLanguage 351
computations done over short time horizons, because short
horizons tend to imply small movements in the stock. The
misstatement becomes significant, though, when measurements
are taken for longer horizons of, for example, 2 weeks or a month.
Larger changes in time result in larger changes in the price of the
underlying,andVaRestimatesgeneratedusingacovariancematrix
shouldnotberelieduponforportfolioswithsignificantnumbersof
positions in options.
Another issue related to delta normal methods and the
presence of options is the difficulty in incorporating random
changesinvolatilities,which,ofcourse,greatlyaffectthevaluation
of options. In the end, historical and Monte Carlo simulation
methods are better for portfolios with complex or nonlinear
instruments.
Historical Simulation
Historical simulation expresses a hypothetical distribution of
portfolio returns. Each return is calculated as though today’s
portfolio were held on a day’s past market movements.
Given a portfolio, we can obtain the historical values of the
factorsaffectingthatportfolioforthepast,say,5years.Thenwecan
subjectthecurrentportfoliotothefactorchangesexperiencedover,
say,1000differentrolling22-daytimeperiodswithinthose5years
toarriveatadiscretedistributionofhypotheticalmonthlyreturns.
Ranking these returns will allow us to find, for example, the 50th
worst loss, which is then the 1-month VaR at the 5 percent level.
Historical simulation methods work well on portfolios with
options becausethey recompute the entire portfolio value foreach
outcome of the underlying factors. Furthermore, historical
simulations can easily be extended to include a distribution of
volatilities.
By recomputing based upon the existence of several factors,
historical simulation methods better estimate a distribution of
returns on portfolios with options. Moreover, the historical
simulation method is easy to implement as long as reliable
historical data is available. If time-series data for the relevant
factors is not available, implementation will be very difficult.
Team-LRN

| 352         |                |     |          |            |     | Object-OrientedProgramming |            |     |
| ----------- | -------------- | --- | -------- | ---------- | --- | -------------------------- | ---------- | --- |
| While       | an improvement |     | over     | parametric |     | methods,                   | historical |     |
| simulations | are not        | a   | panacea. | Although   |     | it is free                 | from       | the |
assumptions of the normal distribution, the historical time period
chosen limits the range of potential outcomes. The distribution of
portfolio values generated can be misleading if the historical
| sample | is not indicative |     | of future | values.    |     |     |     |     |
| ------ | ----------------- | --- | --------- | ---------- | --- | --- | --- | --- |
|        | Monte             |     | Carlo     | Simulation |     |     |     |     |
MonteCarlosimulationalsocalculatesriskbybuildingahistogram
ofhypotheticalreturns.Asopposedtohistoricalsimulation,Monte
Carlo simulation finds hypothetical returns by choosing returns at
randomfromagivendistribution,theparametersofwhichmaybe
estimated by historical data. So Monte Carlo VaR methods are not
limited by actual historical returns. Furthermore, Monte Carlo
| simulation | can easily   | incorporate |     | stochastic |             | volatilities. |       |     |
| ---------- | ------------ | ----------- | --- | ---------- | ----------- | ------------- | ----- | --- |
| Given      | a portfolio, |             | we  | can make   | assumptions |               | about | the |
distributionsoftheunderlyingfactorsaffectingthatportfolio.Then
we can estimate the parameters of those distributions and run
thousands of scenarios to build a histogram of possible future
returns. For each scenario, we revalue the portfolio. As with
historical simulation then, the distribution of hypothetical returns
will allow us to rank the outcomes and find, for example, the 1-
| month    | VaR at a specific                             |       | probability. |         |     |       |         |      |
| -------- | --------------------------------------------- | ----- | ------------ | ------- | --- | ----- | ------- | ---- |
| As       | withthepreviousmethods,MonteCarlosimulationis |       |              |         |     |       |         | not  |
| perfect. | For one,                                      | Monte | Carlo        | methods |     | often | require | long |
computation times, especially as the number of random variables
and the numberof iterations increase. For two, financial engineers
must estimate the parameters of the distributions from which the
random values are being drawn, and these estimates may not be
indicative of the future distributions of factor movements. The
| distribution | of portfolio |     | values | generated |     | by  | Monte | Carlo |
| ------------ | ------------ | --- | ------ | --------- | --- | --- | ----- | ----- |
simulation depends upon these assumptions. Despite the caveats,
however, Monte Carlo is widely used in the industry for large
portfolios of positions containing complex, nonlinear derivative
instruments.
Team-LRN

| UnifiedModelingLanguage |         |     |     |     |     |     |     | 353 |
| ----------------------- | ------- | --- | --- | --- | --- | --- | --- | --- |
| STRESS                  | TESTING |     |     |     |     |     |     |     |
Stresstestingmeasurestheimpactofanabnormalmarketmoveon
a portfolio. Running abnormal scenarios allows us to quantify the
move’s effects on a portfolio, and if these effects are unacceptable,
the portfolio composition may need to be revised. Scenarios are
oftenhistoricalinnature.Forexample,whatwouldhavehappened
hadthisportfoliogonethroughthecrashof1987,orSeptember11?
What would happen if all our correlations go to 1? If our firm is
engagedindynamichedgingorconstantrebalancingofportfolios,
| what would |     | happen | if a | major | shock | occurred | overnight | and |
| ---------- | --- | ------ | ---- | ----- | ----- | -------- | --------- | --- |
market liquidity dries up? None of these scenarios is statistical in
nature, but clearly there are nonzero probabilities associated with
| them that        | must  | be addressed. |          |     |             |            |     |       |
| ---------------- | ----- | ------------- | -------- | --- | ----------- | ---------- | --- | ----- |
| Now              | let’s | incorporate   |          | UML | design      | techniques | and | Monte |
| Carlo simulation |       | into          | a simple | VaR | calculator. |            |     |       |
| STRUCTURAL       |       | DIAGRAMS      |          |     |             |            |     |       |
Structural diagrams show the static architecture of a software
project.
|     |     |     | Class | Diagram |     |     |     |     |
| --- | --- | --- | ----- | ------- | --- | --- | --- | --- |
A full class diagram displays an overview of an entire system
including the constituent classes and the relationships between
| them. However, |     | class      | diagrams |      | are static   | and | only show | what |
| -------------- | --- | ---------- | -------- | ---- | ------------ | --- | --------- | ---- |
| relationships  |     | exist, but | not      | when | they happen. |     |           |      |
UML notation for a class is a rectangle with three parts, one
eachfortheclassname,theattributes,andthemembermethodsor
functions. An individual class is represented in Figure 20.5. Here
MonteCarloisthenameoftheclass,anditrepresentsthedefinition
of a Monte Carlo simulation object. The 2 and þ signs define the
| private   | and               | public | visibility | of             | the    | attributes | and methods. |     |
| --------- | ----------------- | ------ | ---------- | -------------- | ------ | ---------- | ------------ | --- |
| Although  | not               | shown, | #          | would          | define | protected  | visibility.  |     |
| MyMarket, | CurrentPortfolio, |        |            | dblIterations, |        | and        | dblDaysAhead |     |
are all private attributes of the Monte Carlo class. The dblDaysA-
head attribute, for example, will hold the time horizon of the
Team-LRN

| 354 |         |      |     |     |     | Object-OrientedProgramming |     |     |     |
| --- | ------- | ---- | --- | --- | --- | -------------------------- | --- | --- | --- |
| F I | G U R E | 20.5 |     |     |     |                            |     |     |     |
simulation in terms of the numberof days. DblIterations will hold
| the number | of times |           | the simulation |     | will   | run.   |        |     |     |
| ---------- | -------- | --------- | -------------- | --- | ------ | ------ | ------ | --- | --- |
| The        | member   | functions |                | are | listed | in the | bottom | box | and |
includethepropertygetsandsets.Thesignaturesoftherespective
methods are also shown outlining the input and output argument
| types. | The New() | method, |     | of  | course, | is the | constructor, |     | and |
| ------ | --------- | ------- | --- | --- | ------- | ------ | ------------ | --- | --- |
StdNormRnd()isthefunctiondescribedinChapter5thatreturnsa
| standard   | normal | deviate. |      | In          | this case | the properties |     | are | all |
| ---------- | ------ | -------- | ---- | ----------- | --------- | -------------- | --- | --- | --- |
| WriteOnly, | and    | so only  | sets | are listed. |           |                |     |     |     |
Inadditiontotheclassesthemselves,wecanalsorepresentin
UML the class relationships. Relationships between classes are
shown as connecting links and come in five varieties—dependen-
cies, associations, composition, generalization, and aggregation.
Theselinksshouldalsodefinetherelationship’smultiplicityrules,
| which | we will discuss |     | shortly. |          |     |                |     |          |     |
| ----- | --------------- | --- | -------- | -------- | --- | -------------- | --- | -------- | --- |
| When  | a class         | has | as       | a member |     | another class, | we  | say that | it  |
dependsonthatclass.Thisisthenadependencyrelationshipandis
drawn as a dotted line with an arrow pointing to the containing
class. In the example shown in Figure 20.6, the Monte Carlo class
| depends | on the | Portfolio |     | class | and | has a constraint |     | that | the |
| ------- | ------ | --------- | --- | ----- | --- | ---------------- | --- | ---- | --- |
Team-LRN

| UnifiedModelingLanguage |          |     |     | 355 |
| ----------------------- | -------- | --- | --- | --- |
| F I G U                 | R E 20.6 |     |     |     |
relationshipnotbeempty.Ofcourse,ifthereisnoportfolio,thereis
no value at risk to calculate. A constraint, written in braces {},
requiresthateveryimplementationsatisfyacondition.Asyoucan
seefromFigure20.6,aswebegintomoveoutwardandtakealook
at the bigger picture, we may start to abbreviate or even omit
| details at     | lower levels. |                    |            |     |
| -------------- | ------------- | ------------------ | ---------- | --- |
| An association | is the most   | basic relationship | and in UML | is  |
drawn as a line connecting the two classes. As Figure 20.7 shows,
an association relationship exists between the Portfolio class and
| the Algorithms | Package. |     |     |     |
| -------------- | -------- | --- | --- | --- |
If a class exists only as a member of another class, then the
relationship is referred to as a composition within the containing
class.Acompositionisdrawnasalinewithasoliddiamondatthe
containingclassend,asshowninFigure20.8.Inourtradingsystem
| example, | the OleDbConnection, | OleDbDataAdapter, | and DataSet |     |
| -------- | -------------------- | ----------------- | ----------- | --- |
Team-LRN

| 356   |            |     | Object-OrientedProgramming |     |
| ----- | ---------- | --- | -------------------------- | --- |
| F I G | U R E 20.7 |     |                            |     |
classes,collectivelyreferredtoasaDataPackage,willexistonlyas
| members | of the Market | class. |     |     |
| ------- | ------------- | ------ | --- | --- |
A generalization is equivalent to an inheritance relationship
and is drawn as a line with a hollow arrow pointing to the base
class, as you can see in Figure 20.9. Inheritance—or in UMI-speak,
| generalization—shows |     | that Portfolio | is a derived | class of |
| -------------------- | --- | -------------- | ------------ | -------- |
HashTable, and of course inherits all the attributes and methods
of the parent. The Value property has also been added to the class
Portfolio.
| An  | aggregation | isa relationship | in which severalinstancesof |     |
| --- | ----------- | ---------------- | --------------------------- | --- |
a class belong to a Collection class. An aggregation is drawn as a
line with a hollow diamond pointing to the collection. In Figure
20.10, an aggregation exists between Portfolio and Stock. The
asterisk near the Stock class and the 1 near the Portfolio class
represent the multiplicities. A single portfolio can have many
stocks. Thus there is a one-to-many relationship between Portfolio
| F I G | U R E 20.8 |     |     |     |
| ----- | ---------- | --- | --- | --- |
Team-LRN

UnifiedModelingLanguage 357
| F I G | U R E 20.9 |     |     |     |     |     |
| ----- | ---------- | --- | --- | --- | --- | --- |
andStock.SinceaPortfoliohasStocksaselements,thediamondis
positionednearthePortfoliobox.WecouldalsoaddaStockOption
| to represent | another | type | of element |     | in a Portfolio. |     |
| ------------ | ------- | ---- | ---------- | --- | --------------- | --- |
Themultiplicityisthenumberofinstancesofaclassthatmay
beassociatedwithasingleinstanceoftheclassattheotherend.The
| following | table describes |     | the most          | common      | multiplicities. |     |
| --------- | --------------- | --- | ----------------- | ----------- | --------------- | --- |
|           | Multiplicity    |     |                   | Description |                 |     |
|           | 0..1            |     | Zerooroneinstance |             |                 |     |
0..(cid:1) or(cid:1)
Zeroormoreinstances
|     | 1   |     | Oneinstance |     |     |     |
| --- | --- | --- | ----------- | --- | --- | --- |
1..(cid:1)
Oneormoreinstances
| The | class diagram | in  | Figure | 20.11 | models | the entire Monte |
| --- | ------------- | --- | ------ | ----- | ------ | ---------------- |
Carlo simulationapplicationwe willcreate laterin thechapter.As
| you can | see, the central | class | is  | the Monte | Carlo | class. |
| ------- | ---------------- | ----- | --- | --------- | ----- | ------ |
Team-LRN

358 Object-OrientedProgramming
F I G U R E 20.10
Object Diagram
An object diagram is simply a snapshot of all the objects at any
given time. Object diagrams show instances of classes, and objects
come and go, sometimesrapidly. So object diagrams are useful for
Team-LRN

| UnifiedModelingLanguage |             |         |        |      |        |             | 359 |
| ----------------------- | ----------- | ------- | ------ | ---- | ------ | ----------- | --- |
| F I G                   | U R E 20.11 |         |        |      |        |             |     |
| explaining              | very small  | project | pieces | with | highly | complicated |     |
relationships, especially recursive ones. The object diagram in
Figure 20.12 instantiates the class diagram, replacing it with a
concrete example. Each rectangle in the object diagram corre-
| sponds      | to a single | instance  | of       | a class. | Instance    |           | names are |
| ----------- | ----------- | --------- | -------- | -------- | ----------- | --------- | --------- |
| underlined  | in UML      | diagrams. | Class    | names    |             | are often | omitted   |
| from object | diagrams    | since the | meanings |          | are usually | clear.    |           |
|             | Component   |           | Diagrams |          |             |           |           |
A component diagram describes the physical units of a software
| system | and the dependencies |     | between |     | them. | Software | com- |
| ------ | -------------------- | --- | ------- | --- | ----- | -------- | ---- |
ponents, such as the executable files and library files, are often
combined into a single system and as a result have relationships
| and dependencies | between         | them. |       |     |             |     |             |
| ---------------- | --------------- | ----- | ----- | --- | ----------- | --- | ----------- |
| In               | UML, components | are   | drawn | as  | rectangular |     | boxes, with |
two smaller rectangles sticking out the left side. Dependencies are
Team-LRN

| 360   |             |     |     |     | Object-OrientedProgramming |     |     |     |
| ----- | ----------- | --- | --- | --- | -------------------------- | --- | --- | --- |
| F I G | U R E 20.12 |     |     |     |                            |     |     |     |
dashedlineswitharrowspointingfromtheclientcomponenttothe
| supplier    | component      | upon | which        | it depends. |        | The    | TraderAPI |      |
| ----------- | -------------- | ---- | ------------ | ----------- | ------ | ------ | --------- | ---- |
| component   | contains       | an   | interface,   | shown       | in     | Figure | 20.13     | as a |
| “lollipop.” | The dependency |      | relationship |             | within | this   | diagram   |      |
indicates that the .exe file component refers to services offered by
| the TraderAPI | component  |     | via its | public interface. |     |     |     |     |
| ------------- | ---------- | --- | ------- | ----------------- | --- | --- | --- | --- |
|               | Deployment |     |         | Diagram           |     |     |     |     |
A deployment diagram illustrates the physical organization of
| hardware | in a system. | Each | node | on  | a deployment |     | diagram |     |
| -------- | ------------ | ---- | ---- | --- | ------------ | --- | ------- | --- |
representsahardwareunit,andcommunicationrelationshipsexist
between nodes. Nodes are drawn as three-dimensional boxes and
| contain | software components. |     |     |     |     |     |     |     |
| ------- | -------------------- | --- | --- | --- | --- | --- | --- | --- |
SincetheVaRmodelwehavebeenfollowingdoesnotrequire
| any Internet | or even   | LAN   | communication, |       |         | we will | show    | the |
| ------------ | --------- | ----- | -------------- | ----- | ------- | ------- | ------- | --- |
| hardware     | structure | of an | automated      | order | routing |         | system. | The |
Team-LRN

| UnifiedModelingLanguage |              |               |       |         |           |              |            |            | 361 |
| ----------------------- | ------------ | ------------- | ----- | ------- | --------- | ------------ | ---------- | ---------- | --- |
| F I G                   | U R          | E 20.13       |       |         |           |              |            |            |     |
| deployment              |              | diagram       | shown |         | in Figure |              | 20.14 lays | out        | the |
| communication           |              | relationships |       | between |           | the hardware |            | components |     |
| involved                | in automated |               | trade | entry.  |           |              |            |            |     |
| BEHAVIOR                |              | DIAGRAMS      |       |         |           |              |            |            |     |
A behavior diagram represents the different aspects of a system’s
behavior.
|     |     |     | Use | Case | Diagram |     |     |     |     |
| --- | --- | --- | --- | ---- | ------- | --- | --- | --- | --- |
A use case diagram describes from an outside observer’s point of
viewwhatasystemdoes,butnothowitdoesit.Ausecaseexplains
| what happenswhena |          |     | hypotheticaluseror |     |              | actor | interacts | withthe   |     |
| ----------------- | -------- | --- | ------------------ | --- | ------------ | ----- | --------- | --------- | --- |
| system.           | An actor |     | is someone         |     | or something |       | that      | initiates | an  |
interactionwiththesystem.Actuallyausecaseisverymuchlikea
scenario or a simple case study where an actor interacts with a
| system     | and is  | provided | services |         | by it.  |                     |            |     |        |
| ---------- | ------- | -------- | -------- | ------- | ------- | ------------------- | ---------- | --- | ------ |
| The        | picture | shown    | in       | Figure  | 20.15   | is a                | simplified | run | VaR    |
| simulation | use     | case.    | The      | actor   | is      | a financial         | engineer.  |     | The    |
| connection | between |          | actor    | and use | case    | is a communication. |            |     |        |
| Use        | case    | diagrams |          | are     | helpful | in determining      |            |     | system |
requirements. In fact, new use cases often bring to light new
requirementsasthesystemundergoesanevolutionarydesigncycle
and changes are made. Further, their simple, graphical notation
| facilitates | communication. |          |         |     |        |          |      |            |     |
| ----------- | -------------- | -------- | ------- | --- | ------ | -------- | ---- | ---------- | --- |
| A simple    |                | use case | diagram |     | can be | expanded | with | additional |     |
features to display more information. The use case diagram in
Figure 20.16 expands the original VaR simulation diagram with
| additional | features |     | for a | simplified |     | trading | system. | In  | this |
| ---------- | -------- | --- | ----- | ---------- | --- | ------- | ------- | --- | ---- |
Team-LRN

| 362   |             |     |     | Object-OrientedProgramming |     |
| ----- | ----------- | --- | --- | -------------------------- | --- |
| F I G | U R E 20–14 |     |     |                            |     |
expanded design, we could include the ability to place trades and
| populate | a portfolio. |              |         |                    |     |
| -------- | ------------ | ------------ | ------- | ------------------ | --- |
| Note     | again that   | the use case | diagram | does not represent | any |
sequence;itsimplyshowsthelistofscenarios.Asystemboundary
| rectangle | separates | the system | from | the external actors—the |     |
| --------- | --------- | ---------- | ---- | ----------------------- | --- |
financial engineer and the exchange. The <<uses>> relationship
links use cases to additional ones, such as in the case Calculate
Portfolio Value in Figure 20.16. Uses relationships like the one
Team-LRN

| UnifiedModelingLanguage |             |         |               |             | 363 |
| ----------------------- | ----------- | ------- | ------------- | ----------- | --- |
| F I G                   | U R E 20.15 |         |               |             |     |
| shown are               | especially  | helpful | when the same | subtask can | be  |
factored out of other use cases. In Figure 20.16, both Select Trades
andRunVaRSimulationuseCalculatePortfolioValueasasubtask.
In the diagram, the uses relationship is drawn as a line from the
baseusecasetotheusedusecase.Calculatingtheportfoliovalueis
not of the typeRun VaR Simulation,but is a taskthat constitutes a
| piece of | the overall | run simulation | use case. |     |     |
| -------- | ----------- | -------------- | --------- | --- | --- |
| F I G    | U R E 20.16 |                |           |     |     |
Team-LRN

| 364      |            |        |               | Object-OrientedProgramming |     |
| -------- | ---------- | ------ | ------------- | -------------------------- | --- |
| Although | not shown, | extend | relationships | are also possible.         |     |
Extends indicate that one use case is a version or variation of
| another use | case. Extends | are | also drawn | as lines with | an  |
| ----------- | ------------- | --- | ---------- | ------------- | --- |
<<extend>>label.Anextendedcasecanbethoughtofasasubtype
| of a use case. |          |     |         |     |     |
| -------------- | -------- | --- | ------- | --- | --- |
|                | Sequence |     | Diagram |     |     |
A sequence diagram describes the flow of messages as they are
passed from object to object. Whereas class diagrams describe a
staticstructure,sequencediagramsillustratethenatureandtiming
| of the interaction | between | classes. |     |     |     |
| ------------------ | ------- | -------- | --- | --- | --- |
Figure20.17isasequencediagramforrunningaMonteCarlo
simulation. The object initiating the sequence of messages is a
| Form1GUIwindow.The |     | sequenceof | eventsproceedsaswemove |     |     |
| ------------------ | --- | ---------- | ---------------------- | --- | --- |
down the diagram, and the objects are displayed from left to right
according to when they become part of the sequence. The dotted
lines, called lifelines, show that the portfolio exists before the
Monte Carlo is run and continues to exist afterward. On the other
hand, the Monte Carlo object itself and the Market object cease to
existafter the simulation is completed, as denoted by the large Xs.
| Message | calls are | represented | by arrows | from the sender | to  |
| ------- | --------- | ----------- | --------- | --------------- | --- |
the receiver’s lifeline. The activation bars, the hollow rectangles,
representthelengthoftimeoftheexecutionofthemessage.These
| F I G U | R E 20.17 |     |     |     |     |
| ------- | --------- | --- | --- | --- | --- |
Team-LRN

| UnifiedModelingLanguage |     |     |     |     |     |     |     | 365 |
| ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
barsindicatethescopeofamethodoccurringinaparticularobject.
The dotted lines show return values coming back to the calling
object. Notice that myMonteCarlo issues a self-call to generate a
| new random | number.     |     |            |       |     |                |     |          |
| ---------- | ----------- | --- | ---------- | ----- | --- | -------------- | --- | -------- |
| So         | to populate | the | portfolio, | Form1 |     | creates stocks |     | and adds |
them to myPortfolio. A user, presumably a financial engineer,
| inputs    | data into | the       | GUI.     | Form1 | creates         | myMonteCarlo |            | and |
| --------- | --------- | --------- | -------- | ----- | --------------- | ------------ | ---------- | --- |
| myMarket. | The       | GUI sends | messages |       | to myMonteCarlo |              | pertaining |     |
to the parameters of the simulation. Then myMonteCarlo gets the
volatility from the market, and finally the simulation runs and the
| value-at-risk | number | is            | returned | to  | the GUI. |     |     |     |
| ------------- | ------ | ------------- | -------- | --- | -------- | --- | --- | --- |
|               |        | Collaboration |          |     | Diagram  |     |     |     |
In a large software system, objects have to collaborate, and so we
| have collaboration |     | diagrams. |     | A collaboration |               | in  | UML-speak | is        |
| ------------------ | --- | --------- | --- | --------------- | ------------- | --- | --------- | --------- |
| an interaction     |     | between   | two | classes.        | Collaboration |     |           | diagrams, |
while conveying the same information as the previous sequence
diagrams do, focus on the roles that objects play in the overall
| scheme, | as opposed    | to  | the sequence    |             | of messages | being       | sent. |          |
| ------- | ------------- | --- | --------------- | ----------- | ----------- | ----------- | ----- | -------- |
| Each    | message       | in  | a collaboration |             | diagram     | has         | a     | sequence |
| number. | The top-level |     | message         | is numbered |             | 1. Messages |       | at the   |
same level have the same decimal prefix but have suffixes of 1, 2,
| etc., according | to     | when      | they      | occur. |           |         |     |          |
| --------------- | ------ | --------- | --------- | ------ | --------- | ------- | --- | -------- |
| In              | Figure | 20.18 the | financial |        | engineer, | through |     | the GUI, |
collaborates with myMonteCarlo by means of a button click and
| some property |     | sets and | the | run method. |     | Then | myMonteCarlo |     |
| ------------- | --- | -------- | --- | ----------- | --- | ---- | ------------ | --- |
collaborateswithmyPortfolioviathreepropertygetsandthevalue
| method.  | And myMonteCarlo |       |             | collaborates |     | with | myMarket | by  |
| -------- | ---------------- | ----- | ----------- | ------------ | --- | ---- | -------- | --- |
| means of | the volatility   |       | get method. |              |     |      |          |     |
|          |                  | State | Chart       | Diagram      |     |      |          |     |
Statechartdiagramsallowustopicturethelifecycleofaninstance
of a class and the timing of external events affecting it. State
diagrams consist mainly of two elements—states and transitions.
An object has states, which depend upon its current activity or
Team-LRN

| 366 |       |         |     |     |     | Object-OrientedProgramming |     |
| --- | ----- | ------- | --- | --- | --- | -------------------------- | --- |
| F I | G U R | E 20.18 |     |     |     |                            |     |
condition,andtransitions,whichdescribehowtheobjectresponds
| to outside | influences. |          |         |             |       |                 |          |
| ---------- | ----------- | -------- | ------- | ----------- | ----- | --------------- | -------- |
| An         | object      | performs |         | an activity | while | in a particular | state.   |
| Whereas    | actions     | are      | usually | thought     | of    | as processes    | that are |
performedquickly,activitiestakemuchlongertoprocessandmay
be interrupted by external events. An event, which could be a
buttonclick,orcouldbeasystem-generatedevent,orevencouldbe
internallygenerated,causesatransitionorchangeinthestateofan
object.
AsyoucanseeinFigure20.19,anobject’sinitialstateisshown
as a black circle. Intermediate states are rounded rectangles, and
the end state is shown as a black circle with another hollow circle
around it. Transitions are arrows from one state to the next. A
descriptionoftheeventthattriggersatransitionisusuallywritten
| beside | the transition |     | arrow.      |                |     |                   |     |
| ------ | -------------- | --- | ----------- | -------------- | --- | ----------------- | --- |
| Our    | example        |     | state chart | diagram—Figure |     | 20.19—illustrates |     |
thestates andtransitions of the MonteCarloobject. Aftercreation,
theobjectwaitswhiletheuserentersavalidportfolioandmarket,a
number of iterations, and a confidence level. Then the simulation
| executes. | The | setup | and | execution | can | be factored | into four |
| --------- | --- | ----- | --- | --------- | --- | ----------- | --------- |
nonoverlapping states: getting simulation data, getting market
volatility data, running the simulation, and calculating value at
risk.
Team-LRN

UnifiedModelingLanguage 367
| F I G U | R E 20.19                     |     |            |             |
| ------- | ----------------------------- | --- | ---------- | ----------- |
| While   | in its running-the-simulation |     | state, the | Monte Carlo |
objectdoesnotwaitforoutsideeventstotriggeratransitiontothe
nextstate.Thecompletionoftherunningsimulationactivitycauses
| its transition | to the subsequent | state. |     |     |
| -------------- | ----------------- | ------ | --- | --- |
Team-LRN

| 368      |     |         |     |     |     | Object-OrientedProgramming |     |     |
| -------- | --- | ------- | --- | --- | --- | -------------------------- | --- | --- |
| ACTIVITY |     | DIAGRAM |     |     |     |                            |     |     |
An activity diagram is very much like a flowchart. An activity
diagramfollowstheflowofactivitiesintheordertheyoccur.Being
in an activity state means that an object is doing something. That
somethingcouldbeanevent,suchasabuttonclickorformload,or
the execution of a class method. Unlike a state chart diagram,
which concentrates on a single object and its processes, an activity
diagram focuses on the process and the flow of activities from
object to object. In brief, an activity diagram states the basic
| sequencing | convention |         | the | system    | should | follow.  |     |               |
| ---------- | ---------- | ------- | --- | --------- | ------ | -------- | --- | ------------- |
| The        | activity   | diagram |     | describes | the    | sequence |     | of activities |
including any conditional or parallel behavior. A condition is
shown as a branching in the activity flow. A branch separates a
singletransitionintomultipleoutgoingtransitions.Soifbaddatais
entered, the program flow will proceed down one branch. If the
data is good, the other branch will be followed. Either way, the
programactivityflowmergesagainlateron.Obviously,sinceonly
one of the outgoing transitions can be taken, the conditions are
| mutually  | exclusive, |        | and a     | merge | marks    | the end | of  | conditional  |
| --------- | ---------- | ------ | --------- | ----- | -------- | ------- | --- | ------------ |
| behavior. | See        | Figure | 20.20.    |       |          |         |     |              |
| Some      | activities |        | can occur | at    | the same | time    | or  | in parallel. |
Although not shown, parallel behaviors are drawn as forks and
joins. As with a branch, a fork has one incoming transition and
severaloutgoingtransitions.Inafork,however,whentheincoming
transition is encountered, all the outgoing streams are taken at the
| same time.  |      | In the    | end a | join      | occurs     | when        | all the | incoming |
| ----------- | ---- | --------- | ----- | --------- | ---------- | ----------- | ------- | -------- |
| transitions | have | completed |       | their     | individual | activities. |         |          |
| Activity    |      | diagrams  | are   | sometimes |            | shown with  | object  | lanes,   |
often called swim lanes (see Figure 20.21). Lanes define which
| object is        | responsible |         | for which | activity. |         |             |     |            |
| ---------------- | ----------- | ------- | --------- | --------- | ------- | ----------- | --- | ---------- |
| Now              | that        | we have | completed |           | all the | diagrams    | for | our value- |
| at-risk program, |             | we      | are ready | to        | code.   |             |     |            |
| Step             | 1           | Create  | a new     | VB.NET    | Windows | application |     | named      |
MonteCarlo.
| Step | 2   | CreatetheGUIshowninFigure20.22.Namethetext |                |     |           |          |           |     |
| ---- | --- | ------------------------------------------ | -------------- | --- | --------- | -------- | --------- | --- |
|      |     | boxes                                      | txtIterations, |     | txtLevel, | txtDays, | txtValue, | and |
txtVaR.
Team-LRN

| UnifiedModelingLanguage |                  |             |                   |         |             | 369    |
| ----------------------- | ---------------- | ----------- | ----------------- | ------- | ----------- | ------ |
| F I G U                 | R E 20.20        |             |                   |         |             |        |
| Before                  | we can run       | a Monte     | Carlo simulation, |         | we will     | need   |
| some stocks             | and a portfolio. |             |                   |         |             |        |
| Step                    | 3 Add a class    | named       | Stock. We         | will    | try to keep | the    |
|                         | classes simple   | to          | illustrate the    | overall | design,     | so add |
|                         | the following    | definition: |                   |         |             |        |
| Public                  | Class Stock      |             |                   |         |             |        |
| Private                 | strTicker        | As String   |                   |         |             |        |
| Private                 | dblBeta As       | Double      |                   |         |             |        |
| Private                 | dblPrice         | As Double   |                   |         |             |        |
| Private                 | dblShares        | As Double   |                   |         |             |        |
Team-LRN

370 Object-OrientedProgramming
F I G U R E 20.21
Public Sub New(ByVal strTick As String, ByVal dblP As Double, _
ByVal dblB As Double, ByVal dblS As Double)
strTicker = strTick
dblPrice = dblP
dblBeta = dblB
dblShares = dblS
End Sub
Public ReadOnly Property Ticker()
Get
Return strTicker
End Get
End Property
Public ReadOnly Property Beta()
Get
Return dblBeta
End Get
End Property
Public ReadOnly Property Price()
Get
Return dblPrice
End Get
End Property
Public ReadOnly Property Shares()
Team-LRN

UnifiedModelingLanguage 371
| F I G U | R E 20.22 |     |     |     |
| ------- | --------- | --- | --- | --- |
Get
Return dblShares
|     | End Get |     |     |     |
| --- | ------- | --- | --- | --- |
End Property
End Class
| We could | calculate | a stock’s beta | using | the historical price |
| -------- | --------- | -------------- | ----- | -------------------- |
database,Finance.mdb,butforthesakeofsimplicity,wewillleave
this step out.
Step 4 Add a Portfolio class. This class will inherit from the
|     | Hashtable | class and add | a single | Value property as |
| --- | --------- | ------------- | -------- | ----------------- |
shown.
| Public Class | Portfolio |     |     |     |
| ------------ | --------- | --- | --- | --- |
Inherits Hashtable
| Public | ReadOnly | Property Value() |     |     |
| ------ | -------- | ---------------- | --- | --- |
Get
|     | Dim dblPortfolioValue | As                       | Double |                   |
| --- | --------------------- | ------------------------ | ------ | ----------------- |
|     | Dim enumerator        | As IDictionaryEnumerator |        | = GetEnumerator() |
While enumerator.MoveNext()
Team-LRN

| 372 |     |                   |     |     |                           | Object-OrientedProgramming |     |     |
| --- | --- | ----------------- | --- | --- | ------------------------- | -------------------------- | --- | --- |
|     |     | dblPortfolioValue |     |     | += enumerator.Value.Price |                            |     | * _ |
enumerator.Value.Shares
End While
|     |     | Return | dblPortfolioValue |     |     |     |     |     |
| --- | --- | ------ | ----------------- | --- | --- | --- | --- | --- |
End Get
End Property
| End   | Class       |                                             |                 |        |            |     |        |     |
| ----- | ----------- | ------------------------------------------- | --------------- | ------ | ---------- | --- | ------ | --- |
| Step5 |             | Nowthatwearereadytosetuptheportfolio,addthe |                 |        |            |     |        |     |
|       |             | following                                   | code            | to the | Form1_Load |     | event: |     |
| Dim   | myPortfolio | As                                          | New Portfolio() |        |            |     |        |     |
Private Sub Form1_Load(ByVal sender As ...) Handles MyBase.Load
|     | Dim                            | stock1 | As New | Stock("IBM",  | 80,     | 0.95,     | 2000) |     |
| --- | ------------------------------ | ------ | ------ | ------------- | ------- | --------- | ----- | --- |
|     | Dim                            | stock2 | As New | Stock("INTC", |         | 20, 1.25, | 3000) |     |
|     | Dim                            | stock3 | As New | Stock("GE",   | 50,     | 0.5,      | 5000) |     |
|     | myPortfolio.Add(stock1.Ticker, |        |        |               | stock1) |           |       |     |
|     | myPortfolio.Add(stock2.Ticker, |        |        |               | stock2) |           |       |     |
|     | myPortfolio.Add(stock3.Ticker, |        |        |               | stock3) |           |       |     |
| End | Sub                            |        |        |               |         |           |       |     |
Atthispointyoumaywanttorunyourprogramtomakesure
everything is in order so far. Now we are ready to add a Monte
| Carlo simulation |                  | object   | according    |             | to our | class | diagram. |     |
| ---------------- | ---------------- | -------- | ------------ | ----------- | ------ | ----- | -------- | --- |
| Step             | 6                | Add a    | class called | MonteCarlo. |        |       |          |     |
| Public Class     | MonteCarlo       |          |              |             |        |       |          |     |
| Private          | myMarket         | As       | Market       |             |        |       |          |     |
| Private          | CurrentPortfolio |          | As           | Portfolio   |        |       |          |     |
| Private          | dblIterations    |          | As Double    |             |        |       |          |     |
| Private          | dblDaysAhead     |          | As Double    |             |        |       |          |     |
| Public           | WriteOnly        | Property | Market()     |             |        |       |          |     |
| Set(ByVal        |                  | Value)   |              |             |        |       |          |     |
myMarket = Value
| End | Set |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
End Property
| Public    | WriteOnly        | Property | Portfolio() |     |     |     |     |     |
| --------- | ---------------- | -------- | ----------- | --- | --- | --- | --- | --- |
| Set(ByVal |                  | Value)   |             |     |     |     |     |     |
|           | CurrentPortfolio |          | = Value     |     |     |     |     |     |
| End       | Set              |          |             |     |     |     |     |     |
End Property
| Public    | WriteOnly     | Property | Iterations() |     |     |     |     |     |
| --------- | ------------- | -------- | ------------ | --- | --- | --- | --- | --- |
| Set(ByVal |               | Value)   |              |     |     |     |     |     |
|           | dblIterations |          | = Value      |     |     |     |     |     |
| End       | Set           |          |              |     |     |     |     |     |
End Property
| Public    | WriteOnly    | Property | DaysAhead() |     |     |     |     |     |
| --------- | ------------ | -------- | ----------- | --- | --- | --- | --- | --- |
| Set(ByVal |              | Value)   |             |     |     |     |     |     |
|           | dblDaysAhead |          | = Value     |     |     |     |     |     |
| End       | Set          |          |             |     |     |     |     |     |
End Property
| Public | Function | Run(ByVal | Level | As  | Double) | As Double |     |     |
| ------ | -------- | --------- | ----- | --- | ------- | --------- | --- | --- |
Randomize()
Team-LRN

UnifiedModelingLanguage 373
Dim x, y, z As Integer
Dim dblPortValue As Double = CurrentPortfolio.Value
Dim enumerator As IDictionaryEnumerator = CurrentPortfolio _
.GetEnumerator()
Dim randomprices As Double() = New Double(CurrentPortfolio.Count - 1) {}
Dim PortfolioValues As Double() = New Double(dblIterations - 1) {}
Dim PortfolioMoves As Double() = New Double(dblIterations - 1) {}
Dim dblNextMarketReturn As Double
Dim dblVol As Double = myMarket.GetVolatility()
For x = 0 To dblIterations - 1
dblNextMarketReturn = StdNormRnd() + dblVol * Math.Sqrt(dblDaysAhead _
/ 256)
z = 0
While enumerator.MoveNext()
randomprices(z) = enumerator.Value.Price * _
Math.Exp(dblNextMarketReturn * enumerator.Value.Beta)
PortfolioValues(x) += randomprices(z) * enumerator.Value.Shares
z += 1
End While
enumerator.Reset()
Next x
For x = 0 To dblIterations - 1
PortfolioMoves(x) = PortfolioValues(x) - dblPortValue
Next x
System.Array.Sort(portfoliomoves)
Return portfoliomoves(Level / 100 * dblIterations)
End Function
Private Function StdNormRnd() As Double
ReturnRnd()+Rnd()+Rnd()+Rnd()+Rnd()+Rnd()+Rnd()+Rnd()+_
Rnd() + Rnd() + Rnd() + Rnd() - 6
End Function
End Class
Step 7 The market volatility is set by accessing the
Finance.mdb database and calculating the standard
deviation of log returns on the SPX over the entire
data set. Add a class for the market with the
following definition:
Public Class Market
Private myConnection As OleDb.OleDbConnection
Private myDataAdapter As OleDb.OleDbDataAdapter
Private myDataSet As DataSet
Public Function GetVolatility()
Dim dblVolatility, x As Double
myConnection = New OleDb.OleDbConnection("Provider=Microsoft.Jet. _
OLEDB.4.0;Data Source=C:\ModelingFM\Finance.mdb")
myDataAdapter = New OleDb.OleDbDataAdapter("Select ClosePrice _
from SPX", myConnection)
myDataSet = New DataSet()
myConnection.Open()
myDataAdapter.Fill(myDataSet, "SPXdata")
myConnection.Close()
Dim intLength As Integer = myDataSet.Tables("SPXdata").Rows.Count
Team-LRN

374 Object-OrientedProgramming
Dim dblSPYreturns As Double() = New Double(intLength - 2) {}
For x = 1 To intLength - 1
dblSPYreturns(x - 1) = Math.Log(myDataSet.Tables("SPXdata").Rows(x). _
Item(0) / myDataSet.Tables("SPXdata").Rows(x - 1).Item(0))
Next x
dblVolatility = StDevP(dblSPYreturns)
Return dblVolatility * Math.Sqrt(256)
End Function
End Class
As you can see, the class definition also requires that we
includethedefinitionoftheStDevP()functionasaprivatemethod.
The StDevP() method necessitates also the VarP() and Average()
functions.
Step 8 To the class definition of Market, add as private
methods the functions StDevP(), VarP(), and
Average() from the CD.
F I G U R E 20.23
Team-LRN

| UnifiedModelingLanguage |     |                                               |            |      |     |         |             | 375 |
| ----------------------- | --- | --------------------------------------------- | ---------- | ---- | --- | ------- | ----------- | --- |
| Step                    | 9   | TotheButton1_Clickevent,addthefollowingcodeto |            |      |     |         |             |     |
|                         |     | set the                                       | simulation | data | and | run the | simulation: |     |
Private Sub Button1_Click(ByVal sender As ...) Handles Button1.Click
|      |     | Dim dblIters#           | = txtIterations.Text         |                     |                   |                   |     |     |
| ---- | --- | ----------------------- | ---------------------------- | ------------------- | ----------------- | ----------------- | --- | --- |
|      |     | Dim dblLevel#           | = txtLevel.Text              |                     |                   |                   |     |     |
|      |     | Dim dblDays#            | = txtDays.Text               |                     |                   |                   |     |     |
|      |     | Dim myMarket            | As New                       | Market()            |                   |                   |     |     |
|      |     | Dim myReturns           | As                           | Double              |                   |                   |     |     |
|      |     | Dim mySimulation        |                              | As New MonteCarlo() |                   |                   |     |     |
|      |     | mySimulation.Market     |                              | = myMarket          |                   |                   |     |     |
|      |     | mySimulation.Iterations |                              | = dblIters          |                   |                   |     |     |
|      |     | mySimulation.Portfolio  |                              | = myPortfolio       |                   |                   |     |     |
|      |     | mySimulation.DaysAhead  |                              | = dblDays           |                   |                   |     |     |
|      |     | myReturns               | = mySimulation.Run(dblLevel) |                     |                   |                   |     |     |
|      |     | txtValue.Text           | = Format(myPortfolio.Value,  |                     |                   | "###,###,###.00") |     |     |
|      |     | txtVaR.Text             | = Format(myReturns,          |                     | "###,###,###.00") |                   |     |     |
| End  | Sub |                         |                              |                     |                   |                   |     |     |
| Step | 10  | Run                     | the program                  | (see                | Figure            | 20.23).           |     |     |
SUMMARY
In this chapter we covered each of the 12 diagrams in UML, the
| Unified | Modeling |     | Language, | and applied |     | them to | a Monte | Carlo |
| ------- | -------- | --- | --------- | ----------- | --- | ------- | ------- | ----- |
simulation for a portfolio of stocks. The chapter example program
| was built     | from       | these  | diagrams.   | According |              | to the  | Kumiega–Van  |        |
| ------------- | ---------- | ------ | ----------- | --------- | ------------ | ------- | ------------ | ------ |
| Vliet Trading |            | System | Development |           | Methodology, |         | we           | should |
| build         | an objects | and    | program     | document  |              | before  | programming. |        |
| This document |            | should | lay         | out in    | UML          | all the | classes,     | with   |
their attributes and functionalities as well as system design and
behavior.
Team-LRN

| 376 |     |     | Object-OrientedProgramming |     |
| --- | --- | --- | -------------------------- | --- |
PROBLEMS
1. Describeeachofthe12UMLdiagramsinyourownwords.
| 2. Explain | the three | methods described | for calculating | value |
| ---------- | --------- | ----------------- | --------------- | ----- |
at risk.
| 3. How      | would you     | create an objects    | and program  | document |
| ----------- | ------------- | -------------------- | ------------ | -------- |
| using       | UML?          |                      |              |          |
| 4. Describe | each of       | the three categories | of diagrams. |          |
| 5. What     | is a package? |                      |              |          |
Team-LRN

| UnifiedModelingLanguage |      |     |     |     | 377 |
| ----------------------- | ---- | --- | --- | --- | --- |
| PROJECT                 | 20.1 |     |     |     |     |
The beta of stock is the covariance of the stock with the market
divided by the standard deviation of the market according to the
| following | formula: |     |     |     |     |
| --------- | -------- | --- | --- | --- | --- |
s
|     |     |     | b¼ s;m |     |     |
| --- | --- | --- | ------ | --- | --- |
s
m
| Create | a historical | simulation | program that | uses data | in the |
| ------ | ------------ | ---------- | ------------ | --------- | ------ |
Finance.mdb database to calculate the betas. The program should
select market returns at random from its distribution of historical
ones.
| PROJECT | 20.2 |     |     |     |     |
| ------- | ---- | --- | --- | --- | --- |
Add a connection to TraderAPI.dll and/or OptionsAPI.dll so that
theusercanbuyandsellassetsandbuildaportfolioofstocksand
optionsandcalculatevalueatriskusingaMonteCarlosimulation.
Team-LRN

This page intentionally left blank.
Team-LRN

References
CHAPTER 1
Bernstein,Peter.1992.CapitalIdeas.TheFreePress.
Norman,David.2002.ProfessionalElectronicTrading.JohnWiley&Sons(Asia)Pte
Ltd.
Van Vliet, Benjamin, and Andrew Kumiega. 2000, Winter. “Obsolescence of the
NakedTrader.”JournalofGlobalFinancialMarkets,pp.21–23.
CHAPTER 2
Boehm, Barry W. 1998, May. “A Spiral Model of Software Development and
Enhancement.”Computer,vol.21,no.5,pp.61–72.
Kumiega, Andrew, and Benjamin Van Vliet. 2001, October 23. “A Software
DevelopmentMethodologyforFinancialMarkets.”Paperpresentedatthe
11thInternationalConferenceonSoftwareQuality,Pittsburgh,PA.
Kumiega,Andrew,andBenjaminVanVliet.2003.“AnAutomatedTradingSystem
DevelopmentMethodology.”Aworkingpaper.
Rawlings, Bruce. 2003. “In Sample versus Out of Sample Testing for Financial
Markets.”Aworkingpaper.
Royce,WinstonW.1970,August.“ManagingtheDevelopmentofLargeSoftware
Systems.”
CHAPTER 4
Kolb,RobertW.1997.UnderstandingFuturesMarkets,5thed.BlackwellPublishers.
CHAPTER 5
Alexander,Carol.2001.MarketModels.JohnWiley&SonsLtd.
Bollerslev,T.1986.“GeneralizedAutoregressiveConditionalHeteroscedasticity.”
JournalofEconometrics,vol.31,pp.307–327.
379
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for terms of use.
Team-LRN

380 References
Engle, Robert F. 1982. “Autoregressive Conditional Heteroscedasticity with
Estimates of the Variance of UK Inflation.” Econometrica, vol. 50, pp. 987–
1007.
Garman, M. B., and M. J. Klass. 1980. “On the Estimation of Security Price
VolatilitiesfromHistoricalData.”JournalofBusiness,vol.53,pp.67–78.
Nelken, Israel. 1997. Volatility in the Capital Markets. Glenlake Publishing
Company.
Parkinson,M.1980.“TheExtremeValueMethodforEstimatingtheVarianceofthe
RateofReturn.”JournalofBusiness,vol.53,pp.61–65.
CHAPTER 6
Black,F.,andM.Scholes.1973.“ThePricingofOptionsandCorporateLiabilities.”
JournalofPoliticalEconomy,vol.81,pp.637–654.
CHAPTER 7
Whaley,RobertE.2000,Spring.“TheInvestorFearGauge.”TheJournalofPortfolio
Management,pp.12–17.
CHAPTER 8
Hull,JohnC.2000.Options,FuturesandOtherDerivatives,4thed.Prentice-Hall.
CHAPTER 9
Engle,RobertF.,andJosephMezrich.1996,August.“GARCHforGroups.”Risk,
vol.9,no.8,pp.36–40.
CHAPTER 10
Nelson,CharlesR.,andAndrewF.Siegel.1987.“ParsimoniousModellingofYield
Curves.”JournalofBusiness,vol.60,no.4,p.89.
Wilmer, Ram. 1996, June. “A New Tool for Portfolio Managers: Level, Slop and
CurvatureDurations.”JournalofFixedIncome.
CHAPTER 11
Hernandez,MichaelJ.1997.DatabaseDesignforMereMortals.Addison-Wesley.
Team-LRN

References 381
| CHAPTER | 13  |     |
| ------- | --- | --- |
Bowman, J. S., S. L. Emerson, and M. Darnovsky. 2001. The Practical SQL
Handbook.Addison-Wesley.
| CHAPTER | 15  |     |
| ------- | --- | --- |
Deitel,H.M.,P.J.Deitel,andT.R.Nieto.2002.VisualBasic.NET:HowtoProgram,
2ded.Prentice-Hall.
| CHAPTER | 16  |     |
| ------- | --- | --- |
Melamed, Leo. 2002. “Derivatives Exchanges in a Changed World Order.”
HandbookofWorldStock,DerivativeandCommodityExchanges.MondoVisione
Ltd.
| CHAPTER | 17  |     |
| ------- | --- | --- |
Black, Keith. 2003. “Applications of Optimization in Financial Markets.” A
workingpaper.
Cernauskas, Debra. 2003. “Maximum Likelihood Parameter Estimation for
FinancialModelBuildinginExcel.”Aworkingpaper.
| CHAPTERS | 18 AND | 19  |
| -------- | ------ | --- |
Bradley, Ronan. 2002, October 21. “XML and the Financial Services Industry.”
expoQDaily,www.ebizq.net.
FIXProtocol,Ltd.2003.www.fixprotocol.org.
InternationalSwapsandDerivativesAssociation.2003.www.FpML.org.
Pierce, Ryan. 2001, February 26. Townsend Analytics, Ltd. “Transitioning to
Advanced Versions of Messaging Standards.” Presented at FIXML
ProfessionalTrainingCourse,NewYork.
| CHAPTER | 20  |     |
| ------- | --- | --- |
Alhir,SinanSi.1998.UMLinaNutshell.O’Reilly.
Jorion,Philippe.2001.ValueatRisk,2ded.McGraw-Hill.
Roff,JasonT.2003.UML:ABeginner’sGuide.McGraw-Hill/Osborne.
Team-LRN

This page intentionally left blank.
Team-LRN

Acronyms
| ADO   | ActiveX             | Data           | Objects        |            |             |            |         |
| ----- | ------------------- | -------------- | -------------- | ---------- | ----------- | ---------- | ------- |
| API   | Application         |                | programming    |            | interface   |            |         |
| ATM   | At the              | money          |                |            |             |            |         |
| BOX   | Boston              | Options        | Exchange       |            |             |            |         |
| CBOE  | Chicago             | Board          | Options        |            | Exchange    |            |         |
| CLR   | Common              | language       |                | run        | time        |            |         |
| CME   | Chicago             | Mercantile     |                | Exchange   |             |            |         |
| COM   | Component           |                | object         | model      |             |            |         |
| COTS  | Commercial          |                | off the        | shelf      | (software)  |            |         |
| DOM   | Document            | object         | model          |            |             |            |         |
| DTD   | Document            | type           | definition     |            |             |            |         |
| DTMS  | Data transformation |                |                | management |             | system     |         |
| ECN   | Electronic          | communications |                |            | network     |            |         |
| FCM   | Futures             | commission     |                | merchant   |             |            |         |
| FIX   | Financial           | Information    |                | Exchange   |             | (protocol) |         |
| GARCH | Generalized         |                | Autoregressive |            | Conditional |            | Hetero- |
scedasticity
| GUI  | Graphical     | user        | interface    |          |             |                 |     |
| ---- | ------------- | ----------- | ------------ | -------- | ----------- | --------------- | --- |
| HTML | Hypertext     | Markup      |              | Language |             |                 |     |
| IDE  | Integrated    | Development |              |          | Environment |                 |     |
| ISE  | International |             | Securities   |          | Exchange    |                 |     |
| ISO  | International |             | Organization |          | for         | Standardization |     |
383
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for  terms of use.
Team-LRN

384 Acronyms
| MSIL  | Microsoft        | Intermediate           | Language   |        |
| ----- | ---------------- | ---------------------- | ---------- | ------ |
| NQLX  | Nasdaq           | Liffe Markets          |            |        |
| NYSE  | New York         | Stock Exchange         |            |        |
| OOP   | Object-Oriented  | Programming            |            |        |
| RCW   | Run-time         | callable wrapper       |            |        |
| RDBMS | Relational       | database               | management | system |
| RDM   | Relational       | database               | model      |        |
| SQL   | Structured       | Query Language         |            |        |
| STP   | Straight-through | processing             |            |        |
| TT    | Trading          | Technologies,          | Inc.       |        |
| UML   | Unified          | Modeling               | Language   |        |
| VBA   | Visual           | Basic for Applications |            |        |
| VIX   | S&P 100          | volatility             | index      |        |
| XML   | Extensible       | Markup                 | Language   |        |
Team-LRN

I N D E X
Abbreviations,financial,329 AVGfunction(SQL),227,228
Abs()function,91
Absolutevalue,91
Back-enddatasources,219
Abstraction,111
Back-endtradingsystem,8
AcceptChangesmethod,206,209
Backtesting,18–19
Accessdatabases(seeMSAccessdatabases)
Baseclass,116,117
Accessmodifiers,49–50,119
BEGINkeyword(SQL),236
Accessibility,49–50,273
BeginEditmethod,209
Activationbars,364
Behaviordiagrams,345,361–367
ActiveXcontrols,277
Betaofstock,377
ActiveXDataObjects(seeMSActiveXData
BETWEENoperator(SQL),223
Objects)
Binomialtrees,135–137,145–147
Activitydiagrams,368–375
BitArrayclass,257
Addmethod,206–208,244,246,247,259
Black-Scholesoptionpricingformula,3,
ADO(seeMSActiveXDataObjects)
86–90,121
Aggregatefunctions(SQL),226–236
Booleanvaluetype,48,95
Aggregationrelationships,356–358
BostonOptionsExchange(BOX),4
Aliasing,231
Bounds,133,134,137,139
AllowDbNullproperty,207
BOX(BostonOptionsExchange),4
ALTERTABLEstatement(SQL),238
Braces({}),355
Americancalloptions,145–147
Bracket([])wildcard,226
AmericanNationalStandardsInstitute(ANSI),
Breakpoints,158–160
219
Buttonclass,109
AMEX,289
ButtonClickevent,119
&amp;(entityreference),308
ByRefkeyword,84–85
Analyticaldatabases,188
ByValkeyword,84–85
ANDoperator,53,224
AndAlsooperator,53
Annualizedvolatilitynumber,77 Calendar-dayvolatilities,121–124
ANSI(AmericanNationalStandardsInstitute), CancelEditmethod,209
219 Carryingcharge,59
APIs(seeApplicationprogramminginterfaces) Case-sensitivity,221
&apos;(entityreference),308 CaseInsensitiveComparerclass,257
Applicationprogramminginterfaces(APIs),7, CaseInsensitiveHashCodeProviderclass,257
272–275,281,289 Cash-and-carryarbitrage,59
Arbitrage,58–60 Catchblocks(seeTry...Catch...Finally...EndTry
Arguments,82–86 blocks)
Arithmeticoperators,52 CBOE(seeChicagoBoardOptionsExchange)
Arrayindexout-of-rangeexceptions, CBool()function,95
153 CChar()function,95
ArrayListclass,257 CDATA,309,312
Arrays,68–69,133–148 CDate()function,95
ASmodifier(SQL),227 CDbl()function,95
Assemblies,173 CDec()function,95
Assemblymanifests,276 Ceiling()function,91
Assignmentoperators,52 Charvaluetype,48,92,95
Associationrelationships,355,356 CHAR()valuetype(SQL),238
Asterisk,212,222,356–358 Charactercode,91
At-the-money(ATM),120–129 Characterdata,308,309
ATMvolatility,120–129 ChicagoBoardofTrade,8,63
Attributes,308,311,312 ChicagoBoardOptionsExchange(CBOE),3,8,9,
AutoIncrementproperty,207 54,121,274,290
Automatedorderentry,4,289 ChicagoMercantileExchange(CME),8,9,54,274
Automatedtradeexecution,4,271 Childclass,116
“AnAutomatedTradingSystemDevelopment Chr()function,91
Methodology”(AndrewKumiegaandBenVan CInt()function,95
Vliet),11 Classdiagrams,353–359
Averagefunction,227,228 Classrelationships,354
Average()function,140 Classes,109,173
Averagereturn,142 Cleandata,19
385
Copyright © 2004 by The McGraw-Hill Companies, Inc. C lick here for terms of use.
Team-LRN

386 Index
Cleaningdata,248–250 CStr()function,95
Clearmethod,138,204,206,259,264 CType()function,95
CLng()function,95 Currency(curr),329
Clonemethod,204,206 Currencyformat,94
CLR(seeCommonlanguagerun–time)
CME(seeChicagoMercantileExchange) Data,5,18,19,141–143,248–250,272,
Collaborationdiagrams,365,366 317–320(SeealsoValuetypes)
Collectionclass,243–248 Data-awarecomponents,201–202
CollectionBaseclass,246,247,257 Datadefinitionlanguage(DDL),220,
Columnaliasing,231 236–238
ColumnChangedevent,206 Dataintegrity,189
ColumnNamemethod,208 Datamanipulationlanguage(DML),
Columns,206–208 220–226
Columnscollection,205 Datastructures,243–253,257–268
Columns.Addmethod,207 Datatransformationmanagementsystem(DTMS),
COM(seeComponentObjectModel 251–252
objects) DataAdapterobjects,203,207
COMclasstemplates,277 DatabaseDesignforMereMortals(Michael
Comm(commission),329 Hernandez),192
Comma,221 Databaseprogramming,187–197,201–215,
Commadelimiter,225 219–239,243–253,257–268
Commercialoff–the–shelf(COTS)software, Databases,187
273–275 DataColumnCollection,207–208
Commission(comm),329 DataColumns,207–208
COMMITkeyword(SQL),236 DataGrids,201–202
Commonlanguagerun–time(CLR),161,162,164, DataRowCollections,208–209,212–213,251–252
276,277 DataRows,208–209
Company(comp),329 DataSetmodel,202
Comparerclass,257 DataSets,203–205,212
Comparisonoperators,52,223–224 DataTables,205–207
Compiling,38–39,152 DATEvaluetype(SQL),238
TheCompleteGuidetoOptionPricingFormulas DateAdd()function,97
(EspenGaarderHaug),88 DateDiff()function,97,98
Componentdiagrams,359–361 Dates,50,95–98,224,234
ComponentObjectModel(COM)objects,272, DateSerial()function,97
275–277 DateValue()function,97
Compositionrelationships,355,356 Day()function,97
Concatenation,92 DDL(seeDatadefinitionlanguage)
Concatenationoperators,53 Deallocationcode,162
Conditionallyrequiredcontent,329 Debugging,151,160
Connecting(toadatabase),210–215 Decimal(@)valuetype,48,95
Connections,202 Declaration,47–49,133
Connectivity,281–297,302,324,328 Defaultvalues,49,312
Constants,49,96 Definitions,82,83
Constraints,355 DELETEstatement(SQL),235–236
Constraintsproperty,206 Delimitedstrings,92
Constructor(Hashtable),258 Deltanormalapproach,350–351
Constructormethods,113,117 Dependencyrelationships,354–355,
Content,conditionallyrequired,329 359–360
Continuebutton,160 Deploymentdiagrams,360–362
Continuous–improvementstrategy,27 Derivativesmarkets,8,271
Continuousratesofreturn,141–142 Derivedclass,116–117,118
Controlstructures,65–77 Descriptionoftradingidea,16–17
Controls,35–36 Descriptionproperty,166
Conversionfunctions,94–96 Design,database,192–193
Cost-of-carrymodel,56–57 Determinant,matrix,177
COTSsoftware(seeCommercialoff-the-shelf Developmentmethodology(seeKumiega–Van
software) Vliettradingsystemdevelopment
COUNTfunction(SQL),227,228 methodology)
Covarianceforecasting,153–158 Diamond,357,358
Covariancematrix,144 DictionaryBaseclass,257
CREATETABLEstatement(SQL),237–238 DictionaryEntryobject,258,259
CREATEVIEWstatement(SQL),236–237 DictionaryEntrystructure,257
CShort()function,95 Dimkeyword,133–134
CSng()function,95 Dimstatement,47–49,139
Team-LRN

Index 387
Directdatabaseinteraction,202 Fairvalue,58–59
DirtyFinance.mdbdatabase,194–195 Falsecondition,96
DISTINCTfunction(SQL),228–229 “Fattails”,6
Divisionbyzero,153,164 Fidelity,327
DK(don’tknow),329 Fields,188–190
.dllfiles,273,281 FillObjclass,283,285
DLLs(seeDynamiclinklibraryfiles) Finallyblock,162
DML(seeDatamanipulationlanguage) Finance.mdbdatabase,193–194
Documentobjectmodel(DOM),309 Financialabbreviations,329
Documenttypedefinitions(DTDs), Financialengineering,3–7
306–313,329 Financialengineers,4–5
Documentation,25,26 Financialfunctions,98–99
Do...LoopUntilloop,70 FinancialInformationExchange(FIX),324,325
Do...LoopWhileloop,70 Financialmarkets,evolutionof,3
DOM(documentobjectmodel),309 FinancialMarketsExchange(FMEX),
Don’tknow(DK),329 315–316
Double(#)valuetype,48,95 FinancialMarketsMarkupLanguage(FMML),
Do...Untilloop,69–70 303–320
Dowfutures,8 FinancialProductsMarkupLanguage(FpML),
DowJonesIndustrialAverage,54,63 324,325–327
Do...Whileloop,69 FinXML,324
DTDs(seeDocumenttypedefinitions) FIX(seeFinancialInformationExchange)
DTMS(seeDatatransformationmanagement FIXinterface,274
system) FIXProtocol,Ltd.(FPL),325,327–337
Duplicatesfilter,228–229 Fixedformat,94
Dynamiclinklibraryfiles(DLLs),173 Fixed-lengthcharacterfields,238
#FIXEDvalue,312
E(baseofnaturallogarithms),91 FIXML,324,325,328–337
E-Minicontracts,54 Flat-filestructures,187
E-MiniS&P,9 Floor()function,91
ECNs,289 FMEX(seeFinancialMarketsExchange)
ElectronicTradingSystem(CBOE),274 FMML(seeFinancialMarketsMarkupLanugage)
Electronictradingsystems,323 ForEach...Nextloop,68–69
Elements(DTD),307 Forecasting,73–77,153–158
Encapsulation,112–115 Foreign(forex),329
EndEditmethod,209 Foreignkeys,191
ENTITIESattribute,312 Forex(foreign),329
ENTITYattribute,312 Format()function,93–94
Entityreferences,308 For...Nextloop,68,71–72,135
Enumstatement,52 FPL(seeFIXProtocol,Ltd.)
Enumerations,51–52 FpML(seeFinancialProductsMarkupLanguage)
Equaloperator,53 Friendkeyword,119
Erasestatement,141 Front-endtradingsystems,7–8,219
Errobject,166 “Fullyqualified”objectnames,173
Errors,152,153,161 Functions,82–105,138–141
Events,37–38,42,118–119 Fut(seeFutures)
Excel(seeMicrosoftExcel) Futurevalueofannuityfunction,98,99
Exceptionhandlers,153,160–167 Futurescontracts,54,63
Exceptions,errorsvs.,161 Futures(fut),54–60,329
Exchange"backend,"8 Futuresmarketconnectivity,282–288
Exchange(exch),274–275,329 FV()function,98,99
Exclamationpoint(!)valuetype,48,95
Executablefiles(EXEs),173 GARCH(seeGeneralizedautoregressive
Executableprograms,38–42 conditionalheterscedasticitymodels)
Exitcommand,71 GARCH(1,1)model,74,76,249
ExitDocommand,71 Garman,M.B.,73
ExitForcommand,71 Garman-Klassestimator,73
Exp()function,91 Generalnumberformat,94
Exponentiation,52 Generalizationrelationships,356,357
Extendrelationships,364 Generalizedautoregressiveconditional
ExtensibleBusinessReportingLanguage,324 heterscedasticity(GARCH)models,
ExtensibleFinancialResearchMarkupLanguage 73–74
(XFRML),324 Globalvariables,50
ExtensibleMarkupLanguage(XML),272,301–320 Globexsystem,274
Extremevalueestimators,72–73 Graphicaluserinterface(GUI),35
Team-LRN

388 Index
Greaterthanoperator,53 InternationalStandardsOrganization(ISO),325
Greaterthanorequaloperator,53 Interopmarshaling,277
GROUPBYclause(SQL),229–230 Interoperability,271–278,324,328
&gt;(entityreference),308 Interoperabilityassembly,276–277
GUI(seeGraphicaluserinterface) InvalidCastException,164
Inversion,141,177
Hardware,360–361 InvestmentResearchMarkupLanguage(IRML),
Hashtables,258–265 324
Hashing,258 “TheInvestorFearGauge”(RobertWhaley),121
Hashtableclass,257 IOI(indicationofinterest),329
Haug,EspenGaarder,88 Ipmt()function,98
HAVINGclause(SQL),230–231 IRML(InvestmentResearchMarkupLanguage),
Help,38 324
Hernandez,Michael,192–193 IRR()function,98
Historicalmarketdata,5,18,19 IsArray()function,96
Historicalsimulation,351–352 IsConstant()function,96
Hoffer,Eric,185 IsDate()function,96
Hour()function,97 IsDBNull()function,255
HTML(HypertextMarkupLanguage),301 ISE(InternationalSecuritiesExchange),274
Hull,Blair,1 IsNullmethod,209
HypertextMarkupLanguage(HTML),301 IsNumeric()function,96
ISO15022,325
IBM,8–9 ISO(InternationalStandardsOrganization),325
IDattribute,312 IsReference()function,96
ID(identifier),329 Itemproperty,208,244,258
IDE(seeIntegrateddevelopmentenvironment) ItemArrayproperty,208
Identifier(ID),329
IDictionaryEnumerator,259–260,264 Jaggedarrays,135–137,145–147
IDREFattribute,312 Join()function,92
IDREFSattribute,312
Joiningtables,192,231–232
If...Then...Elsestatement,65–66
IFX(InteractiveFinancialExchange),324
Implementation(oftradingsystem),19–25 Kettering,Charles,269
#IMPLIEDvalue,312 Key-and-valuepairs,258
Impliedvolatility,100–105 Klass,M.J.,73
ImportRowmethod,206 Kumiega,Andrew,11,12,14
Importsstatement,173–175 Kumiega–VanVliettradingsystemdevelopment
INoperator(SQL),223 methodology,12–28
Index,134,225,243 Kurtosis,142
IndexOpclass,290
IndexOutOfRangeException,164 Languageindependence,39
Indicationofinterest(IOI),329 Leadingcharacters,226
Infiniteloops,71 Left()function,92,93
Inheritance,116–118 Len()function,92
Initializerlist,133–134 Lengthproperty,138
Inputarguments,83–86 Lessthanoperator,53
Insertmethod,246 Lessthanorequaloperator,53
INSERTstatement(SQL),233–235 Libraries,281
InStr()function,92 Libraryofquantitativemethods,17–18
InstrNotifyclass,283–284 Lifecycles,365
InstrObjclass,283 Lifelines,364
Instrumentproperty,284 LIKEoperator(SQL),223,225–226
Integer(%)valuetype,48,95 Linearregression,177
Integerdivision,52 Livemarketfeeds,272
Integergreaterthanorequaltoinputargument,91 Log()function,91
Integerlessthanorequaltoinputargument,91 Logreturns,214
Integrateddevelopmentenvironment(IDE),33– Logicerrors,152
38 Logicaloperators,52
Integrity,data,189 Lognormaldistribution,108
InteractiveFinancialExchange(IFX),324 LognormalRnd()function,100
Interestpaymentfunction,98 Long(&)valuetype,48,95
Interestratefunction,99 LongTermCapitalManagement,6
Interfaces,172–173 Lowenstein,Roger,6
Internalrateofreturnfunction,98 Lowerbounds,133
InternationalSecuritiesExchange(ISE),274 LSCmodel,178–179
Team-LRN

Index 389
&lt;(entityreference),308 MSActiveXDataObjects(ADO),189,
201–215
MSSQLServer,5,201
Machinelanguage,38,39 MsgBoxfunction,99
Managedmemory,276 MSIL(seeMicrosoftIntermediateLanguage)
Managingportfolioandrisk,26–27 MTranspose()function,177
Many-to-manyrelationships,191,195 Multiplelinearregression,177
Marketconnectivity,281 Multiplication,52,177
Marketdata,274 Multiplicities,356–358
MarketDataDefinitionLanguage(MDDL),324 MultRegression()function,177
MarketDataMarkupLanguage(MDML),324 MustInheritCollectionBaseclass,246
Market-value-weightedindex,54–55 MustInheritkeyword,116
Mathematicalfunctions,90–91 MustOverridekeyword,116
Matrixalgebra,144–145 MyBasekeyword,117
Matrixdeterminant,177
Matrixinversion,177 Name(offunction),82
Matrixmultiplication,177 Namespaces,173
Matrixtransposition,177 “NaN”(notanumber)value,164
MatrixMath.dll,177 Naturallog,62,66,91
Max()function,91 Negation,52
MAXfunction(SQL),227,228 Nelson,CharlesR.,178
.mdbextension,193 Nestedloops,71–72,135
MDDL(MarketDataDefinitionLanguage),324 .NETFramework,171,276–277
MDeterm()function,177 .NETIDEtoolbox,277
MDML(MarketDataMarkupLanguage),324 .NETobjects,COMobjectsvs.,275–277
Meandeviation,62,100 Netpresentvaluefunction,98
Memberfunctions,109 .NETtypesystem,171–182
Memory,275–276 Newkeyword,113–115,133
Menubar,35 Newmethod,203,204,206,207
Messageboxfunction,99 NMTOKENattribute,312
Messagecalls,364 NMTOKENSattribute,312
Messages,329,365 Nonproceduralprogramminglanguages,220
Metalanguages,301,302 Normaldistribution,100
Methodology,6 Normalform,192
Methodology,development(seeKumiega–Van Normalization,192
Vliettradingsystemdevelopment Norman,David,5
methodology) “Notanumber”(NaN)value,164
Methods(VisualBasic.NET),38,109 Notequaloperator,53
MH(seeMicroHedge,Inc.) NOTNULLkeyword,238
MHpositionclass,290 Notoperator,53
MHSBTclass,290 NOTATIONattribute,312
MicroHedge,Inc.(MH),9,289–291 Nothingkeyword,120,245
MicroHedgeclass,290 NotOverridablekeyword,116
Microsoft,189,201,272,275,276 Nowfunction,97
MicrosoftExcel,5,18,145,152,156,178,187 NPer()function,98
MicrosoftIntermediateLanguage(MSIL),38–39 NPV()function,98
Mid()function,92,93 NQLX,9
Middleware,272,273 NULLkeyword,234,238
Min()function,91 Numberofperiodsfunction,98
MINfunction(SQL),227,228 Numberproperty,166
Minute()function,97 Numbers,94–96
MInverse()function,177 NUMERIC()valuetype(SQL),238
MIRR()function,98 NYSE,8,289
MMult()function,145,177
MMult2by1()function,177 Objectdiagrams,358–360
Modoperator,52 ObjectLinkingandEmbeddingDatabases
Modeldiagrams,346,347 (OleDb),201–203
Modelmanagementdiagrams,345–349 Object-orientedprogramming(OOP),25,109,116
Modifiedinternalrateofreturnfunction,98 (SeealsoUnifiedModelingLanguage)
Modulos,52 Objects,109–131
Monitoringportfolios,26 OEXindex(seeS&P100index)
MonteCarlosimulation,79–80,352–375 OFX(seeOpenFinancialExchange.XBRL)
Month()function,97 OleDb(seeObjectLinkingandEmbedding
Moore’slaw,4 Databases)
MSAccessdatabases,193–196 OleDbCommand,202
Team-LRN

390 Index
OleDbCommandobject,234 Portfoliomanagement,26–27
OleDbConnectionclass,202,210,211 Portfoliomatrix,144
OleDbDataAdapterclass,203,210–212 Poundsign(#),48,95,224,234
OnErrorGoTostatement,164–166 PPmt()function,99
OnErrorResumeNextstatement,166 Predefinedformatfunctions,94
OneChicago,9 Presentvaluefunction,99
One-dimensionalarrays,133–134 Preservekeyword,139–140
One-periodvolatility,72–73 Priceproperty,284
One-to-manyrelationships,191,195 Price(px),329
One-to-onerelationships,191 Price-weightedindex,54
OOP(seeObject–orientedprogramming) Primarykeys,190
OpenFinancialExchange.XBRL(OFX),324,329 PrimaryKeyproperty,206
Open()method,283,284 Principalpaymentfunction,99
Opensourcecode,273 Privatekeyword,119
Operationaldatabases,188 Problemsolving,151–167
Operators,52–54 Proceduralprograms,55
Option(opt),329 Procedures,81–82,81–106(SeealsoFunctions;
OptionStrictOffstatement,51 Subroutines)
OptionStrictOnstatement,50–51 ProfessionalElectronicTrading(DavidNorman),5
Optionsymbols,67 Profitability,26
Optionalkeyword,83–84 Profitabilitytesting,18,19,25
Optionsexchanges,4 Programflowstatements,65–72
Optionslibrary,174–175 Programtrading,58
Optionsmarkets,9,289–296 Propertieswindow,37
OptionsAPI.dll,281,289–291 Protectedkeyword,119
Options.mdbdatabase,195–196 Publicinterface,109,112
ORoperator,53,224 Publickeyword,119
Oracle,5,189,219,236 PV()function,99
ORDERBYclause(SQL),224–225 Px(price),329
Order(ord),329
Orderrouting,274 Qty(quantity),329
Orderedmessages,329 Quantitativemethods,17–18
OrderProfileclass,283,284 Quantitativetradingsystems,6,11
OrderSetclass,283,284 Quantityproperty,284
OrElseoperator,53 Quantity(qty),329
Out-of-sampletesting,19 Queries,192
Overloading,120 Queueclass,257
Overloadskeyword,120 &quot;(entityreference),308
Overridablekeyword,116
Overrideskeyword,116 Randomnumberfunctions,99–100
Overridingdefinitions,115–117,116 Randomnumbergenerator,79–80,100
Randomize()function,100
Packagediagrams,347–349 Rangesofcharacters,226
Papertrading,25 Rankproperty,138
ParamArraykeyword,85–86 Rate()function,99
Parameterarray,85–86 RationalRose,345
ParameterlessCatch,162 RCW(run-timecallablewrapper),276
Parameters,optional,83–84 RDBMSs(seeRelationaldatabasemanagement
Parentclass,116 systems)
Parkinson,M.,73 RDM(seeRelationaldatabasemodel)
Parsedcharacterdata(PCDATA),308 ReadOnlykeyword,113
Parsers,305,309–313 ReadOnlyCollectionBaseclass,257
Parsingstrings,92 Records,188–190
Paymentfunciton,98 ReDim()procedure,139–140
PCDATA(parsedcharacterdata),308 References,validationfunctionfor,96
Percentformat,94 Registration,COMobject,277
Percentwildcard,225 Regsvr32utility,277
Persistentconnections,202 Relationaldatabasemanagementsystems
Pipecharacter(|),311 (RDBMSs),189
PL/SQL,219 Relationaldatabasemodel(RDM),188–189
Plainmarkuplanguage,306 Relationaldatabases,187–197
Pmt()function,98 Relationships,189,191
Polymorphism,118 Removemethod,244,246,259
Polynomialmodel,179–181 RemoveAt,246,247
Portfoliodeltacalculation,265 Repetitionstructures,67–72
Team-LRN

Index 391
#REQUIREDvalue,312 S&P500eMinifutures,282
ResearchInformationExchangeMarkup S&P500futures,8
Language(RIXML),324 S&P500index,54
Researchquantitativemethods,17–18 S&P100(OEX)index,121–123
Resumestatement,165 S&P500optionscontracts,290
Returnargument,81 Special-characterentities,308
Returnkeyword,86 Spiralmethodology,13–15
Returnvalue,81,82 Split()function,92–93
Returnvalues,86 SQL(seeStructuredQueryLanguage)
Reversecash-and-carryarbitrage,59–60 SqlClientobjects,201
Right()function,92,93 Sqrt()function,91
Riskmanagement,26–27 Squarebrackets([])wildcard,226
RIXML(ResearchInformationExchangeMarkup Squareroot,62,91
Language),324 Standarddeviation,62,100
Rnd()function,79–80,99–100 Standardformat,94
ROLLBACKkeyword(SQL),236 Startingpositionofstring,92
Rows,208–209 Statechartdiagrams,365–367
Rowscollection,205 States,365–367
Rows.Addmethod,208 StdNormRand()function,100
Run-timecallablewrapper(RCW),276 StepIntobutton,160
Run-timeerrors,153 StepOutbutton,160
StepOverbutton,160
SalomonBrothers,327 Stockindexfutures,54–60
SAX(simpleAPIforXML)model,309 StopDebuggingbutton,160
SBT(seeScreenBasedTrading) STP(seeStraight-throughprocessing)
Scientificformat,94 STPML(Straight-throughProcessingMarkup
Scopecreep,14 Language),324
Scopedocuments,20,23–24 Str()function,95
Scope(ofvariables),49–50 Straight-throughProcessingMarkupLanguage
ScreenBasedTrading(SBT),289,290 (STPML),324
SDK(softwaredeveloper’skit),289 Straight-throughprocessing(STP),272,323
Second()function,97 StrComp()function,92
SecuritiesFinancingExtensibleMarkupLanguage String($)valuetype,48,95,234
(SFXL),324 Stringcomparison,92,224–226
Securitiestrading,271 Stringfunctions,91–93,95
SelectCasestatement,66–67 Structuraldiagrams,345,353–361,353–362
Selectstatement(SQL),221–223 Structurestatement,51
Selectionstructures,65–67 Structuredexceptionhandlers,161–164
SendOrder()method,284 StructuredQueryLanguage(SQL),189,192,219–
Senge,Peter,31 239
Sequencediagrams,364–365 Structures,51
SetLimits()method,284 Subroutines,81,83–90
SetTradeParams()method,284 Subsystemdiagrams,346,347
SetTradeType()method,284 Subtraction,52
SFXL(SecuritiesFinancingExtensibleMarkup SUMfunction(SQL),227–228
Language),324 SWIFT(seeSocietyforWorldwideInterbank
Shadowskeyword,116 FinancialTelecommunications)
Sharedfields,189 SwiftML,324,325,329
Sharedkeyword,119 Sybase,189
Shortvaluetype,48,95 Syntaxerrors,152
Siegel,AndrewF.,178 System.Arraynamespace,138
Sign()function,91 System.Collectionsclasses,263
SimpleAPIforXML(SAX)model,309 System.Collections.namespace,246,257
Single(!)valuetype,48,95 System.Data.OleDbnamespace,210
Skew,142,177 System.DBNullobject,255
Smiles,volatility,176–181 System.Exceptionclass,162
Snepscheut,Janvande,341 System.XMLnamespace,309
SocietyforWorldwideInterbankFinancial
Telecommunications(SWIFT),324,325 Tableproperty,208
Software,9,271–278,359–360 TableNameproperty(DataTable),206
Softwaredeveloper’skit(SDK),289 Tables,188–190,237–238
SolutionExplorerwindow,36–37 Tablesproperty,204
Sort()function,138–139 Tables.Addmethod,206
SortedListclass,257 Tags,302–308
S&P500cashoptions,8,9 Technology,271–272,323
Team-LRN

392 Index
10-dayvolatilityforecast,77 Validationfunctions,96
Termination,conditionfor,14 Valueatrisk(VaR),26,349–375,350–352
Testing,18–19,353 Valuetypes,47–52,234,238
Third–partytradingsoftware,7,281 Values,attribute,312
Throwpoints,161 VanVliet,Ben,11,12,14
Throwstatement,166–167 VaR(seeValueatrisk)
Time,238 VARCHAR2()valuetype(SQL),238
Timeinterval,data,249 Variable-lengthcharacterfields,238
Timelydata,19 Variables,47–50
TimeOfDayfunction,97 Varianceofreturns,142
Timing(ofexternalevents),365 VBA(seeVisualBasicforApplications)
Todayfunction,97 VB.NET(seeVisualBasic.NET)
Toolbox,35–36 Views,creating,236–237
ToString()method,131,264 Visibility,50
TraderAPI,360–362 Visiondocuments,20–22
TraderAPI.dll,281–283,285,288 VisualBasic,versionsof,33
Trading-dayvolatilities,121–124 VisualBasicforApplications(VBA),5,33
TradingTechnologies,Inc.(TT),9,282 VisualBasic.NET(VB.NET),7,33–43,
Trailingcharacters,226 47–54,65–72,81–106,109–129,133–148,151–
Transact-SQL,219 167,171–182,188,271–278,281–297
Transitions,366–367 VisualStudio.Net,33–38
Transposition,141,177 Visualization,345
Trees,binomial,135–137,145–147 VIX(volatilityindex)methodology,121
Truecondition,96 Volatility,72–77,100–105,108,120–129
Try...Catch...Finally...EndTryblocks, Volatilityindex(VIX)methodology,121
161–164 Volatilitysmiles,176–181
TT(seeTradingTechnologies,Inc.)
Two-dimensionalarrays,134–135 Watchwindow,160
Typesystems,171–173 Waterfallmodel,12–13
Type(term),171 WeatherMarkupLanguage(WeatherML),324
WeatherML(WeatherMarkupLanguage),324
Ubound()function,141 Weekday()function,97
UML(seeUnifiedModelingLanguage)
Well-formedXMLdocuments,305
Underscore(_)wildcard,226 Whaley,Robert,121
UnifiedModelingLanguage(UML),25,344–349, WhenGeniusFailed(RogerLowenstein),6
353–375 Whereclause(SQL),223–224
Uniformresourcelocator(URL),312 While...EndWhileloop,71
UNIONkeyword(SQL),233
Wildcards,212,222,225,226
Uniquemethod,208
Wilmer,Ram,178
Unmanagedmemory,276 www.FIXprotocol.org,329
Unstructuredexceptionhandlers,164–166 www.FpML.org,326
Updatemethod,203
UPDATEstatement(SQL),235
Upperbounds,133,134,137,139,141 XFRML(ExtensibleFinancialResearchMarkup
URI(URLobjectrepresentation),316 Language),324
URL(uniformresourcelocator),312
XML(seeExtensibleMarkupLanguage)
U.S.Treasurybills(T–bills),122 XMLmessages,309,315–317
Usecasediagrams,361–364 XMLprotocols,323–337,325–337
User-defineddatatypes,51 XMLschema,306
User-definedformatfunctions,94
Xml:attribute,312
User-definedinterfaces,172
Xoroperator,53
Usesrelationships,362–363 X_Trader,9,282
Val()function,95 Year()function,97
ValidXMLdocuments,305–307 Yieldcurvemodels,178
Team-LRN
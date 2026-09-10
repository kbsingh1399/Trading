|             | Arbitrage,     |            | State   | Prices        | and Portfolio |         |         | Theory  |
| ----------- | -------------- | ---------- | ------- | ------------- | ------------- | ------- | ------- | ------- |
|             | Handbook       |            | of      | the Economics |               | of      | Finance |         |
|             |                | Philip     | Dybvig  |               |               | Stephen |         | A. Ross |
|             | Washington     | University |         | in Saint      | Louis         |         | MIT     |         |
| Firstdraft: | September,2001 |            |         |               |               |         |         |         |
| Thisdraft:  | September      |            | 19,2002 |               |               |         |         |         |

Abstract
Neoclassical financial models provide the foundation for our understanding of
finance. Thischapterintroducesthemainideasofneoclassicalfinanceinasingle-
periodcontextthatavoidsthetechnicaldifficultiesofcontinuous-timemodels,but
preservesthe principal intuitions of the subject. The startingpoint ofthe analysis
isthe formulationofstandardportfoliochoiceproblems.
A central conceptual result is the Fundamental Theorem of Asset Pricing, which
asserts the equivalence of absence of arbitrage, the existence of a positive linear
pricing rule, and the existence of an optimum for some agent who prefers more
to less. A related conceptual result is the Pricing Rule Representation Theorem,
which asserts that a positive linear pricing rule can be represented as using state
prices,risk-neutralexpectations,orastate-pricedensity. Differentequivalentrep-
resentationsareuseful indifferentcontexts.
Manyappliedresultscanbederivedfromthefirst-orderconditionsoftheportfolio
choiceproblem. Thefirst-orderconditionssaythatmarginalutilityineachstateis
proportional to a consistent state-price density, where the constant of proportion-
ality is determined by the budget constaint. If markets are complete, the implicit
state-price density is uniquely determined by investment opportunities and must
be the same as viewed by all agents, thus simplifying the choice problem. Solv-
ing first-order conditions for quantities givesus optimal portfolio choice, solving
them for prices gives us asset pricing models, solving them for utilities gives us
preferences,andsolving themforforprobabilitiesgivesus beliefs.
We look at two popular asset pricing models, the CAPM and the APT, as well
as complete-markets pricing. In the case of the CAPM, the first-order conditions
linknicelyto thetraditionalmeasuresofportfolioperformance.
Furtherconceptualresultsincludeaggregationandmutualfundseparationtheory,
bothofwhichare usefulforunderstandingequilibriumandasset pricing.

The modern quantitativeapproach to finance has its original roots in neoclassical
economics. Neoclassical economics studies an idealized world in which markets
work smoothly without impediments such as transaction costs, taxes, asymme-
try of information, or indivisibilities. This chapter considers what we learn from
single-period neoclassical models in finance. While dynamic models are becom-
ing more and more common, single-period models contain a surprisingly large
amount of the intuition and intellectual content of modern finance, and are also
commonly used by investment practitioners for the construction of optimal port-
folios and communication of investment results. Focusing on a single period is
also consistent with an important theme. While general equilibrium theory seeks
great generality and abstraction, finance has work to be done and seeks specific
models with strong assumptions and definite implications that can be tested and
implementedinpractice.
1 Portfolio Problems
In our analysis, there are two points of time, 0 and 1, with an interval of time in
between during which nothing happens. At time zero, our champion (the agent)
is making decisions that will affect the allocation of consumption between non-
random consumption, c , at time 0, and random consumption
0
(cid:0) cw
(cid:1)
across states
w
(cid:2)
1
(cid:3)
2
(cid:3)(cid:5) (cid:4)(cid:6) (cid:4)(cid:6) (cid:4)(cid:7) (cid:3)
W revealed at time 1. At time 0 and in each state at time 1, there is
a single consumption good, and therefore consumption at time 0 or in a state at
time 1 is a real number. This abstraction of a single good is obviously not “true”
in any literal sense, but this is not a problem, and indeed any useful theoretical
model is much simpler than reality. The abstraction does, however face us with
thequestionofhowtointerpretoursimplemodel(inthiscasewithasinglegood)
inapracticalcontextthatismorecomplex(hasmultiplegoods). Inusingasingle-
goodmodel,therearetwousualpractices: eitherusenominalvaluesandmeasure
consumption in dollars, or use real values and measure consumption in inflation-
adjusted dollars. Depending on the context, one or the other can make the most
sense. In this article, we will normally think of the consumption units as being
the numeraire, so that “cash flows” or “claims to consumption” have the same
meaning.
Followingthe usual practice from general equilibrium theory of thinking of units
2

ofconsumptionatvarioustimesandindifferentstatesofnatureasdifferentgoods,
atypicalconsumptionvectorisC (cid:0) (cid:0) c 0 c 1 cW ,where the realnumber c 0 de-
(cid:3) (cid:3) (cid:4)(cid:7) (cid:4)(cid:6) (cid:4)(cid:7) (cid:3)
notesconsumptionofthesinglegoodattimezero,andthevectorc (cid:1) c cW
(cid:0) (cid:0) 1
(cid:3) (cid:4)(cid:6) (cid:4)(cid:7) (cid:4)(cid:6) (cid:3)
ofrealnumbersc cW denotesrandomconsumptionofthesinglegoodineach (cid:1)
1
(cid:3) (cid:4)(cid:6) (cid:4)(cid:7) (cid:4)(cid:6) (cid:3)
| state1 | W attime                                                     | 1.  |     |
| ------ | ------------------------------------------------------------ | --- | --- |
|        | (cid:3) (cid:4)(cid:7) (cid:4)(cid:6) (cid:4)(cid:7) (cid:3) |     |     |
Ifthiswereatypicalexerciseingeneralequilibriumtheory,wewouldhaveaprice
vector for consumption across goods. For example, we might have the following
choice problem, which is named after two great pioneers of general equilibrium
theory,KennethArrowandGerardDebreu:
| Problem1            | Arrow-DebreuProblem |           |         |
| ------------------- | ------------------- | --------- | ------- |
| ChooseconsumptionsC |                     | (cid:0) c | c cW to |
|                     |                     | (cid:0) 0 | 1       |
(cid:3) (cid:3) (cid:1) (cid:4)(cid:6) (cid:4)(cid:7) (cid:4)(cid:6) (cid:3) (cid:1)
| maximizeutilityof |     | consumptionU | C subjectto |
| ----------------- | --- | ------------ | ----------- |
(cid:2)
thebudgetconstraint
W
(cid:229)
| (1) | c 0     | pw cw W         |     |
| --- | ------- | --------------- | --- |
|     | (cid:3) | (cid:2) (cid:4) |     |
w
(cid:4) 1
|     | (cid:1)(cid:6) (cid:5) |     |     |
| --- | ---------------------- | --- | --- |
Here,U is the utility function that represents preferences, p is the price vector,
(cid:2)
andW is wealth, which might be replaced by the market valueof an endowment.
We are taking consumption at time 0 to be the numeraire, and pw is the price of
the Arrow-Debreu security which is a claim to one unit of consumption at time 1
w
| instate | .   |     |     |
| ------- | --- | --- | --- |
The first-order condition for Problem 1 is the existence of a positive Lagrangian
(cid:1)
multiplierl (themarginal utility ofwealth)such thatU c l ,and forall w
0 (cid:7) 0 (cid:2)
(cid:2) (cid:2)
1 W ,
| (cid:3)(cid:5) (cid:4)(cid:6) (cid:4)(cid:6) (cid:4)(cid:7) (cid:3) |     |     | (cid:1) |
| ------------------------------------------------------------------- | --- | --- | ------- |
U cw l pw
w (cid:7) (cid:2)
(cid:2) (cid:4)
This is the usual result from neoclassical economics that the gradient of the util-
ity function is proportional to prices. Specializing to the leading case in finance
of time-separable von Neumann-Morgenstern preferences, named after John von
Neumann and Oscar Morgenstern, two great pioneers of utility theory, we have
|     | (cid:1) (cid:1) | (cid:229) W p | (cid:1) |
| --- | --------------- | ------------- | ------- |
that U C v c w u cw . We will take v and u to be differentiable,
|     | (cid:2) | 0 (cid:2) (cid:3) w (cid:4) 1 | (cid:2) |
| --- | ------- | ----------------------------- | ------- |
(cid:2)
strictly increasing (more is preferred to less), and strictly concave (risk averse).
3

Here, p w is the probability of state w . In this case, the first-order condition is the
existenceofl such that
v
(cid:7)
(cid:1) c
0 (cid:2)
(cid:2)
l
(cid:3)
(2)
andforallw
(cid:2)
1
(cid:3)
2
(cid:3)(cid:5) (cid:4)(cid:6) (cid:4)(cid:6) (cid:4)(cid:7) (cid:3)
n,
p w u (cid:7) (cid:1) cw (cid:2)
(cid:2)
(3) l pw
orequivalently
u (cid:7) (cid:1) cw (cid:2)
(cid:2)
lr w
(cid:3)
(4)
where r w (cid:0) pw
(cid:0)
p w is the state-price density (also called the stochastic discount
factor or pricing kernel), which is a measure of priced relative scarcity in state
of nature w . Therefore, the marginal utility of consumption in a state is pro-
portional to the relative scarcity. There is a solution if the problem is feasible,
prices and probabilities are positive, the von Neumann-Morgenstern utility func-
tion is increasing and strictly concave, and there is satisfied the Inada condition
lim c
(cid:1)
¥ u (cid:7) (cid:1) c (cid:2)
(cid:2)
0.1 There are different motivations of von Neumann-Morgenstern
preferences in the literature and the probabilities may be objective or subjective.
What is important for us that the von Neumann-Morgensternutility function rep-
resents preferences in the sense that expected utility is higher for more preferred
consumptionpatterns.2
Using von Neumann-Morganstern preferences has been popular in part because
of axiomatic derivations of the theory (see, for example, Herstein and Milnor
[1953] or Luce and Raiffa [1957], chapter 2). There is also a large literature
on alternatives and extensions to von Neumann-Morgenstern preferences. For
1Provingtheexistenceofanequilibriumrequiresmoreassumptionsincontinuous-statemod-
els.
2Later,whenwelookatmultiple-agentresults,wewillalsomaketheneoclassicalassumption
ofidenticalbeliefs,whichisprobablymostnaturallymotivatedbysymmetricobjectiveinforma-
tion.
4

single-periodmodels,seeKnight[1921],Bewley[1988],Machina[1982],Blume,
Brandenburger, and Dekel [1991], and Fishburn [1988]. There is an even richer
set of models in multiple periods, for example, time-separable von Neumann-
Morgenstern(thetraditionalstandard),habitformation(e.g. Duesenberry[1949],
Pollak [1970], Abel [1990], Constantinides [1991], and Dybvig [1995]), local
substitutability over time (Hindy and Huang [1992]), interpersonal dependence
(Duesenberry [1949] and Abel [1990]), preference for resolution of uncertainty
(KrepsandPorteus[1978]),timepreferencedependentonconsumption(Bergman
[1985]),andgeneralrecursiveutility(EpsteinandZin[1989]).
Recently, there have also been some attempts to revivethe age-old idea of study-
ingfinancialsituationsusingpsychologicaltheories(likeprospecttheory,Kahne-
man and Tversky [1979]). Unfortunately, these models do not translate well to
financial markets. For example, in prospect theory framing matters, that is, the
observedphenomenonofanagentmakingdifferentdecisionswhenfacingidenti-
cal decision problems describeddifferently. However,thisis analien conceptfor
financial economists and when they proxy for it in models they substitute some-
thingmorefamiliar(forexample,somehistorydependenceasinBarberis,Huang,
and Santos[2001]). Another problem with the psychological theories is that they
tend to be isolated stories rather than a general specification, and they are often
hardtogeneralize. Forexample,prospecttheorysaysthatagentsputextraweight
on very unlikely outcomes, but it is not at all clear what this means in a model
with a continuum of states. This literature also has problems with using ex post
explanations (positive correlations of returns are underreaction and negative cor-
relations are overreactions) and a lack of clarity of how much is going on that
cannotbeexplainedby traditionalmodels(andmuchofitcan).
In actual financial markets, Arrow-Debreu securities do not trade directly, even
if they can be constructed indirectly using a portfolio of securities. A security
is characterized by its cash flows. This description would not be adequate for
analysis of taxes, since different sources of cash flow might have very different
tax treatment, but we are looking at models without taxes. For an asset like a
commonstockorabond,thecashflowmightbenegativeattime0,frompayment
of the price, and positive or zero in each state at time 1, the positive amount
coming from any repayment of principal, dividends, coupons, or proceeds from
sale of the asset. For a futures contract, the cash flow would be 0 at time 0, and
the cash flow in different states at time 1 could be positive, negative, or zero,
depending on news about the value of the underlying commodity. In general, we
5

think of the negativeof the initial cash flow as the price of a security. We denote
byP (cid:0) P 1 P N thevectorofpricesofthe N securities1 N,andwedenote
| (cid:2) (cid:3) (cid:4)(cid:6) (cid:4)(cid:7) (cid:4)(cid:6) (cid:3) |     |     | (cid:3) | (cid:4)(cid:7) (cid:4)(cid:6) (cid:4)(cid:6) (cid:3) |
| -------------------------------------------------------------------- | --- | --- | ------- | ---------------------------------------------------- |
byX thepayoffmatrix. (cid:1) WehavethatP isthepricewepayforoneunitofsecurity
n
nandXw isthepayoffperunitofsecurityn attime1inthesinglestateofnature
n
w .
Withthe choiceofa portfolioofassets,ourchoiceproblemmightbecome
| Problem2 FirstPortfolioChoiceProblem |     |     |     |     |
| ------------------------------------ | --- | --- | --- | --- |
ChooseportfolioholdingsQ (cid:0) Q Q andconsumptionsC (cid:0) c cW to
|                   |              | (cid:0) 1 | n                                                                    | (cid:0) 0                                                            |
| ----------------- | ------------ | --------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
|                   |              | (cid:1)   | (cid:3) (cid:4)(cid:7) (cid:4)(cid:6) (cid:4)(cid:7) (cid:3) (cid:1) | (cid:3) (cid:4)(cid:6) (cid:4)(cid:7) (cid:4)(cid:6) (cid:3) (cid:1) |
| maximizeutilityof | consumptionU | C         | subjectto                                                            |                                                                      |
(cid:2)
XQ
| portfoliopayoffsc | (cid:0) c | cw  | and |     |
| ----------------- | --------- | --- | --- | --- |
(cid:0) 1
|                   |     | (cid:3) Q (cid:4)(cid:7) (cid:4)(cid:6) (cid:4)(cid:6) (cid:3) (cid:1) (cid:2) |     |     |
| ----------------- | --- | ------------------------------------------------------------------------------ | --- | --- |
| budgetconstraintc | P   | W.                                                                             |     |     |
0 (cid:3) (cid:7)
(cid:2)
Here, Q is the vector of portfolio weights. Time 0 consumption is the numeraire,
and wealth W is now chosen in time 0 consumption units and the entire endow-
Q
mentisreceivedattime0. Inthebudgetconstraint,thetermP isthecostofthe
(cid:7)
portfolio holding, which is the sum across securities n of the price P times the
n
| numberofsharesorotherunitQ |     | ThematrixproductXQ |                     |     |
| -------------------------- | --- | ------------------ | ------------------- | --- |
|                            |     | n .                | saysthattheconsump- |     |
tioninstatew iscw (cid:229) Xw Q ,i.e. thesumacrosssecuritiesnofthepayoffXw
|     | n   | n n |     | n   |
| --- | --- | --- | --- | --- |
(cid:2)
ofsecurityn instatew ,timesthenumberofsharesorotherunitsQ ofsecurityn
n
| ourchampionis | holding. |     |     |     |
| ------------- | -------- | --- | --- | --- |
The first-order condition for Problem 2 is the existence of a vector of shadow
andaLagrangianmultiplierl
| prices p |     |     | suchthat |     |
| -------- | --- | --- | -------- | --- |
(cid:1)
| (5) p u cw        | l pw |     |     |     |
| ----------------- | ---- | --- | --- | --- |
| w (cid:7) (cid:2) |      |     |     |     |
(cid:2)
where
| (6) P (cid:7) pX |     |     |     |     |
| ---------------- | --- | --- | --- | --- |
(cid:2) (cid:4)
The first equation is the same as in the Arrow-Debreu model, with an implicit
shadowpricevectorinplaceofthegivenArrow-Debreuprices. Thesecondequa-
tion is a pricing equation that says the prices of all assets mustbe consistent with
6

the shadow prices of the states. For the Arrow-Debreu model itself, the state-
space tableau X is I, the identity matrix, and the price vector P is p, the vector
ofArrow-Debreu state prices. Forthe Arrow-Debreumodel, the pricing equation
determinestheshadowpricesasequaltothe stateprices.
Even if the assets are not the Arrow-Debreu securities, Problem 2 may be essen-
tially equivalent to the Arrow-Debreu model in Problem 1. In economic terms,
the important feature of the Arrow-Debreu problem is that all payoff patterns are
spanned,i.e.,eachpotentialpayoffpatterncanbegeneratedatsomepricebysome
portolioofassets. Linearalgebra tellsusthat all payoffpatterns canbegenerated
ifthepayoffmatrixX hasfullrowrank. IfX hasfullrowrank, pisdetermined(or
over-determined)by(6). If pisuniquelydeterminedbythepricingequation(and
therefore alsoall Arrow-Debreuassets canbepurchased asportfoliosof assetsin
theeconomy),wesaythatmarketsarecomplete,andforallpracticalpurposeswe
arein anArrow-Debreuworld.
Forthe choice problemto haveasolution for anyagentwho prefers moreto less,
we also need for the price of each payoff pattern to be unique (the “law of one
price”) and positive, or else there would be arbitrage (i.e., a “money pump” or a
“free lunch”). If there is no arbitrage, then there is at least one vector of positive
state prices p solving the pricing equation (6). There is an arbitrage if the vector
ofstatepricesisoverdeterminedorifallconsistentvectorsofstatepricesassigna
negativeorzeropricetosomestate. Thenotionofabsenceofarbitrageisacentral
concept in finance, and we develop its implications more fully in the section on
preference-freeresults.
So far, we have been stating portfolio problems in prices and quantities, as we
would in general equilibrium theory. However, it is also common to describe
assetsintermsofratesofreturn,whicharerelativepricechanges(oftenexpressed
aspercentages). Thereturntosecurityn,whichistherelativechangeintotalvalue
(includinganydividends,splits,warrantissues,coupons,stockissues,andthelike
aswellaschangeintheprice). Thereisnotanabsolutestandardofwhatismeant
by return, in different contexts this can be the rate of rate of return, one plus the
rate of return, or the difference between two rates of return. It is necessary to
figurewhich isintendedby askingorfrom context. Usingthenotationabove,the
rateofreturninstate w isrw
n
= (cid:1) Xw
n
(cid:0)
P
n (cid:2)
(cid:0)
P .3 Often,consumptionatthe outset
n
3Oneunfortunatethingaboutreturnsisthattheyarenotdefinedforcontracts(likefutures)that
7

is suppressed, and we specialize to von Neumann-Morgenstern expected utility.
| Inthiscase,wehavethe |                              | followingcommonformofportfolioproblem. |     |     |     |     |
| -------------------- | ---------------------------- | -------------------------------------- | --- | --- | --- | --- |
| Problem3             | PortfolioProblemusingReturns |                                        |     |     |     |     |
Choose portfolio proportions q (cid:0) q q and consumptions c (cid:0) c cW
|     |     |     | (cid:0) 1              | n                                             |     | (cid:0) 1                                                            |
| --- | --- | --- | ---------------------- | --------------------------------------------- | --- | -------------------------------------------------------------------- |
|     |     |     | (cid:3) (cid:4)(cid:7) | (cid:4)(cid:6) (cid:4)(cid:7) (cid:3) (cid:1) |     | (cid:3) (cid:4)(cid:6) (cid:4)(cid:7) (cid:4)(cid:6) (cid:3) (cid:1) |
to
|                         |           |               |                 | W p         | (cid:1)           |         |
| ----------------------- | --------- | ------------- | --------------- | ----------- | ----------------- | ------- |
| maximizeexpectedutility |           | ofconsumption |                 | (cid:229)   | q u cw subjectto  |         |
|                         |           |               |                 | w (cid:4) 1 | (cid:2)           |         |
|                         |           | Wq            | (cid:1)         |             | budgetconstraintq |         |
| theconsumption          | equationc |               | 1               | r andthe    |                   | 1 1.    |
|                         |           |               | (cid:7) (cid:3) | (cid:2)     |                   | (cid:7) |
|                         |           | (cid:2)       |                 |             |                   | (cid:2) |
| p                       | p p       |               |                 |             | (cid:1) (cid:5)   |         |
Here, (cid:0) 1 W is a vectorof state probabilities, u (cid:2) is the von Neumann-
| (cid:2) | (cid:3) (cid:4)(cid:6) (cid:4)(cid:7) (cid:4)(cid:6) (cid:3) |     |     |     |     |     |
| ------- | ------------------------------------------------------------ | --- | --- | --- | --- | --- |
Morgenstern utility function, (cid:1) and 1 is a vector of 1’s. The dimensionality of 1 is
determined implicitly from the context, here the dimensionality is the number of
assets. The first-order condition for an optimum is the existence of shadow state
pricedensityvectorr andshadowmarginalutilityofwealth l such that
| (cid:1) | lr      |     |     |     |     |     |
| ------- | ------- | --- | --- | --- | --- | --- |
| (7) u   | cw w    |     |     |     |     |     |
| (cid:7) | (cid:2) |     |     |     |     |     |
(cid:2)
and
(cid:1)
| (8) 1 | E (cid:0) 1 r r |     |     |     |     |     |
| ----- | --------------- | --- | --- | --- | --- | --- |
(cid:3) (cid:2)
| (cid:2) | (cid:1) | (cid:4) |     |     |     |     |
| ------- | ------- | ------- | --- | --- | --- | --- |
These equations say that the state-price density is consistent with the marginal
| valuationby | theagentandwithpricinginthe |     |     | market. |     |     |
| ----------- | --------------------------- | --- | --- | ------- | --- | --- |
As our final typical problem, let us consider a mean-variance optimization. This
optimization is predicated on the assumption that investors care only about mean
and variance (typically preferring more mean and less variance), so we have a
(cid:1)
utilityfunctionV m v inmeanmandvariancev. Forthisproblem,supposethere
(cid:2)
(cid:3)
is a risk-free asset paying a return r (although the market-level implications of
mean-variance analysis can also be derived in a general model without a risky
havezeroprice.However,thiscanbefinessedformallybybundlingafutureswithabondorother
assetindefiningthesecuritiesandunbundlingthemwheninterpretingtheresults. Bundlingand
unbundlingdoes not change the underlying economics due to the linearity of consumptions and
constraintsintheportfoliochoiceproblem.
8

asset). In this case, portfolio proportions in the risky assets are unconstrained
(need not sum to 1) because the slack can be taken up by the risk-free asset. We
denoteby µ thevectorofmeanriskyasset returnsandbys the covariancematrix
ofriskyreturns. Thenourchampionsolvesthe followingchoiceproblem.
| Problem4                    | Mean-varianceoptimization |         |                                                              |                         |                            |           |
| --------------------------- | ------------------------- | ------- | ------------------------------------------------------------ | ----------------------- | -------------------------- | --------- |
| Chooseportfolioproportionsq |                           |         | q q                                                          |                         |                            |           |
|                             |                           |         | (cid:0)                                                      | to                      |                            |           |
|                             |                           | (cid:0) | 1                                                            | n                       |                            |           |
|                             |                           |         | (cid:3) (cid:4)(cid:7) (cid:4)(cid:6) (cid:4)(cid:7) (cid:3) | (cid:1) (cid:1) (cid:1) | q q Sq                     |           |
| maximizethe                 | mean-varianceutility      |         | functionV                                                    | r µ                     | r1 (cid:2) (cid:7) (cid:7) | (cid:2) . |
(cid:3)
|                               |     |           |     | (cid:0) | (cid:3) |     |
| ----------------------------- | --- | --------- | --- | ------- | ------- | --- |
| Thefirst-orderconditionforthe |     | problemis |     |         |         |     |
lSq
| (9) µ   | r1              |     |     |         |         |     |
| ------- | --------------- | --- | --- | ------- | ------- | --- |
| (cid:0) | (cid:2) (cid:3) |     |     |         |         |     |
|         |                 |     |     | (cid:1) | (cid:1) |     |
where l is twice the marginal rate of substitutionV m v V m v , evaluated at
|         |     |     |     | v (cid:7) | (cid:2) m (cid:7)       | (cid:2) |
| ------- | --- | --- | --- | --------- | ----------------------- | ------- |
| (cid:1) |     |     |     |           | (cid:3) (cid:0) (cid:3) |         |
m r µ r1 q and v q Sq , where q is the optimal choice of portfolio pro-
| (cid:3) | (cid:2) (cid:7) | (cid:7) |     |     |     |     |
| ------- | --------------- | ------- | --- | --- | --- | --- |
| (cid:2) | (cid:0)         | (cid:2) |     |     |     |     |
portions. The first-order condition (9) says that meanexcess returnfor each asset
is proportional to the marginal contribution of volatility to the agent’s optimal
portfolio.
We have seen a few of the typical types of portfolio problem. There are a lot
of variations. The problem might be stated in terms of excess returns (rate of
return less a risk-free rate) or total return (one plus the rate of return). Or, we
might constrain portfolio holdings to be positive (no short sales) or we might
require consumption to be nonnegative (limited liability). Many other variations
adapt the basic portfolio problem to handle institutional features not present in
a neoclassical formulation, such as transaction costs, bid-ask spreads, or taxes.
Theseextensions are veryinteresting,but beyondthe scopeof what we are doing
| here,whichis | toexplorethe | neoclassicalfoundations. |     |                 |     |         |
| ------------ | ------------ | ------------------------ | --- | --------------- | --- | ------- |
| 2 Absence    | of Arbitrage |                          | and | Preference-free |     | Results |
Before considering specific solutions and applications, let us consider some gen-
eral results that are useful for thinking about portfolio choice. These results are
9

preference-free in the sense that they do not depend on any specific assumptions
about preferences but only depend on an assumption that agents prefer more to
less. Centraltothissectionisthenotionofanarbitrage,whichisa“moneypump”
or a “free lunch”. If there is arbitrage, linearity of the neoclassical problem im-
plies that any candidate optimum can be dominated by adding the arbitrage. As
a result, no agent who prefers more to less would have an optimum if there ex-
ists arbitrage. Furthermore, this seemingly weak assumption is enough to obtain
two useful theorems. The Fundamental Theorem of Asset Pricing says that the
following are equivalent: absence of arbitrage, existence of a consistent positive
linearpricingrule,andexistenceofanoptimumforsomehypotheticalagentwho
prefers more to less. The Pricing Rule Representation Theorem gives different
equivalent forms for the consistent positivelinear pricing rule, using state prices,
risk-neutral probabilites (martingale valuation), state-price density (or stochastic
discount factor or pricing kernel), or an abstract positive linear operator. The re-
sults in this section are from Cox and Ross [1975], Ross [1976c, 1978b], and
DybvigandRoss[1987]. Theresultshavebeenformalizedincontinuoustimeby
HarrisonandKreps[1979]andHarrisonandPliska [1981].
Occasionally,the theorems in this section can be applied directly to obtain an in-
terestingresult. Forexample,linearity ofthe pricingruleis enoughto deriveput-
call parity without constructing the arbitrage. More often, the results in this sec-
tionhelptoanswerconceptualquestions. Forexample,anoptionpricingformula
that is derived using absence of arbitrage is always consistent with equilibrium,
as can be seen from the Fundamental Theorem. By the Fundamental Theorem,
absenceofarbitrageimpliesthereisanoptimumforsomehypotheticalagentwho
prefersmoretoless;wecanthereforeconstructanequilibriuminthesingle-agent
pureexchangeeconomyinwhichthisagentisendowedwiththeoptimalholding.
Byconstructiontheequilibriuminthiseconomywillhavethedesiredpricing,and
thereforeany no-arbitragepricingresult isconsistentwith someequilibrium.
Inthissection,wewillworkinthecontextofProblem2. Anarbitrageisachange
inthe portfoliothatmakesallagents whoprefermoreto lessbetteroff. Wemake
allsuchagentsbetteroffif weincreaseconsumptionsometime,andinsomestate
ofnature,andweneverdecreaseconsumption. Bycombiningthetwoconstraints
inProblem2,wecanwritetheconsumptionCassociatedwithanyportfoliochoice
10

Q
| usingthe | stackedmatrixequation |     |     |                     |     |     |     |
| -------- | --------------------- | --- | --- | ------------------- | --- | --- | --- |
|          |                       |     |     | (cid:0) W (cid:0) P |     |     |     |
|          |                       |     | C   | (cid:7)             | Q   |     |     |
(cid:3) (cid:0)
|     |     |     | (cid:2) | 0 X     | (cid:4) |     |     |
| --- | --- | --- | ------- | ------- | ------- | --- | --- |
|     |     |     |         | (cid:1) | (cid:1) |     |     |
Thefirstrow,W P Q ,is consumptionattime 0,which iswealthW lessthe cost
(cid:7)
|     |     | (cid:0) |     | XQ  |     |     |     |
| --- | --- | ------- | --- | --- | --- | --- | --- |
of our portfolio. The remaining rows, , give the random consumption across
statesattime1.
|     |     |     |     |     | Q   |     | Q h |
| --- | --- | --- | --- | --- | --- | --- | --- |
Now, when we move from the portfolio choice to the portfolio choice ,
(cid:3)
theinitialwealthtermcancelsandthe changeinconsumptioncannowbewritten
as
(cid:0)
P (cid:7)
|     |     |     | D   | C h |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
(cid:0) X
|     |     |     |     | (cid:2) | (cid:4) |     |     |
| --- | --- | --- | --- | ------- | ------- | --- | --- |
(cid:1)
This will be an arbitrage it D C is never negative and is positive in at least one
| component,which |     | wewillwriteas4 |     | D C 0 or |     |     |     |
| --------------- | --- | -------------- | --- | -------- | --- | --- | --- |
(cid:2)
(cid:0) P
(cid:7) h
0
(cid:0) X
|     |     |     |     | (cid:2) (cid:4) |     |     |     |
| --- | --- | --- | --- | --------------- | --- | --- | --- |
(cid:1)
Someauthorsdescribetaxonomiesofdifferenttypesofarbitrage,having perhaps
a negative price today and zero payoff tomorrow, a zero price today and a non-
negative but not identically zero payoff tomorrow, or a negative price today and
a positive payoff tomorrow. These are all examples of arbitrages that are sub-
sumed by our general formula. The important thing is that there is an increase in
consumption in some state of nature at some point of time and there is never any
decreaseinconsumption.
| Fundamental |     | Theorem | of  | Asset Pricing |     |     |     |
| ----------- | --- | ------- | --- | ------------- | --- | --- | --- |
Theorem 1 Fundamental Theorem of Asset Pricing The following conditions
| onprices | Pand | payoffsX | areequivalent: |     |     |     |     |
| -------- | ---- | -------- | -------------- | --- | --- | --- | --- |
(cid:0)
| (cid:1)               |     |     | (cid:1)                  | P (cid:7) |         |     |     |
| --------------------- | --- | --- | ------------------------ | --------- | ------- | --- | --- |
| i Absenceofarbitrage: |     |     | (cid:4) (cid:3)(cid:5) h | h 0       | .       |     |     |
| (cid:2)               |     |     | (cid:2)                  | (cid:0)   |         |     |     |
|                       |     |     | (cid:7) (cid:6)          | X (cid:2) | (cid:8) |     |     |
(cid:1)
4Weusethefollowingterminologyforvectorinequalities:
|                                           |                                                     |                                      |                                                                     |                                                                        | x y                                                | i x i y i                                                 | , x y                                               |
| ----------------------------------------- | --------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------- | --------------------------------------------------------- | --------------------------------------------------- |
|                                           |                                                     |                                      |                                                                     |                                                                        | (cid:9) (cid:10) (cid:11)(cid:13) (cid:12)(cid:14) | (cid:9)(cid:16)(cid:15) (cid:11)(cid:17) (cid:9) (cid:10) | (cid:11) (cid:9) (cid:18) (cid:11)(cid:19) (cid:12) |
| x y &                                     | i x                                                 | y ,and                               | x y                                                                 | i x y .                                                                |                                                    |                                                           |                                                     |
| (cid:9)(cid:20) (cid:9) (cid:10) (cid:11) | (cid:9)(cid:22) (cid:21) (cid:11)(cid:23) (cid:9) i | (cid:18) i (cid:11)(cid:20) (cid:11) | (cid:9) (cid:18)(cid:24) (cid:18) (cid:11)(cid:19) (cid:12)(cid:25) | (cid:9)(cid:16)(cid:15) (cid:11)(cid:23) (cid:9) i (cid:18) i (cid:11) |                                                    |                                                           |                                                     |
11

(cid:1)
ii Existence of a consistent positive linear pricing rule (positive state prices):
(cid:2)
| (cid:1)                 | (cid:1)             |                       |     |     |     |     |     |     |
| ----------------------- | ------------------- | --------------------- | --- | --- | --- | --- | --- | --- |
| (cid:5) p               | 0 (cid:2) P (cid:7) | p (cid:7) X (cid:2) . |     |     |     |     |     |     |
| (cid:1) (cid:2) (cid:2) |                     | (cid:2)               |     |     |     |     |     |     |
iii Some agent with strictly increasing preferencesU has an optimum in Prob-
(cid:2)
lem2.
|       |                                |     |     |     | (cid:1)         | (cid:1) (cid:1) (cid:1) |          | (cid:1)         |
| ----- | ------------------------------ | --- | --- | --- | --------------- | ----------------------- | -------- | --------------- |
| PROOF | Weprovetheequivalencebyshowing |     |     |     | i               | ii , ii                 | iii ,and | iii             |
|       |                                |     |     |     | (cid:2) (cid:1) | (cid:2) (cid:2) (cid:1) | (cid:2)  | (cid:2) (cid:1) |
(cid:1)
i .
(cid:2)
(cid:1) (cid:1)
i ii : This is the most subtle part, and it follows from a separation theorem
| (cid:2) (cid:1) | (cid:2) |     |     |     |     |     |     |     |
| --------------- | ------- | --- | --- | --- | --- | --- | --- | --- |
or the duality theorem from linear programming. From the definition of absence
| ofarbitrage,wehavethatthe |     |     | sets |     |     |     |     |     |
| ------------------------- | --- | --- | ---- | --- | --- | --- | --- | --- |
(cid:0)
|     |     |     | (cid:2)   | P (cid:7) |       |         |     |     |
| --- | --- | --- | --------- | --------- | ----- | ------- | --- | --- |
|     |     |     | S         |           | h h ´ | n       |     |     |
|     |     |     | 1 (cid:0) | (cid:0)   |       | (cid:5) |     |     |
X (cid:3) (cid:4)
(cid:1)
and
W
|     |     |     | S               | x ´     | 1 x 0           |         |     |     |
| --- | --- | --- | --------------- | ------- | --------------- | ------- | --- | --- |
|     |     |     | 2 (cid:0)       |         | (cid:8)         |         |     |     |
|     |     |     | (cid:7) (cid:6) | (cid:4) | (cid:3) (cid:2) | (cid:9) |     |     |
mustbedisjoint. Therefore,thereisaseparatinghyperplanezsuchthatz x 0for
(cid:7)
(cid:2)
all x S and z x 0 for all x S . (See ..., theorem ...) Normalizing so that the
|         | 1   | (cid:7) | 2       |     |     |     |     |     |
| ------- | --- | ------- | ------- | --- | --- | --- | --- | --- |
| (cid:4) |     | (cid:2) | (cid:4) |     |     |     |     |     |
firstcomponent(theshadowpriceoftimezeroconsumption)is1,wewillseethat
(cid:1)
p definedby 1p z z isthe consistentlinearpricingruleweseek. Constancy
|          |         | (cid:7) (cid:2) | 0               |           |              |         |         |          |
| -------- | ------- | --------------- | --------------- | --------- | ------------ | ------- | ------- | -------- |
|          |         | (cid:2) (cid:0) | (cid:0)         |           |              |         |         |          |
|          |         |                 | (cid:1)         | P (cid:7) |              |         |         |          |
| ofzxforx | S       | impliesthat     | 1p              |           | 0, whichisto | saythat | P       | p X,i.e. |
|          |         | 1               | (cid:7) (cid:2) | (cid:0) X |              |         | (cid:7) | (cid:7)  |
|          | (cid:4) |                 |                 |           | (cid:2)      |         | (cid:2) |          |
(cid:1)
p is a consistent linear pricing rule. Furthermore, z x positive for x S implies
|     |     |     |     |     |     | (cid:7) |     | 2   |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- |
(cid:4)
z 0 and consequently p 0, and p is indeed the desired consistent positive
| (cid:2) (cid:2) |     |     | (cid:2) (cid:2) |     |     |     |     |     |
| --------------- | --- | --- | --------------- | --- | --- | --- | --- | --- |
linearpricingrule.
| (cid:1) | (cid:1) |     |     |     |     | (cid:1) (cid:1) |     | Q   |
| ------- | ------- | --- | --- | --- | --- | --------------- | --- | --- |
ii (cid:1) iii : This part is proven by construction. LetU C 1p C, then 0
| (cid:2) | (cid:2) |     |     |     |     | (cid:2) | (cid:7) (cid:2) |         |
| ------- | ------- | --- | --- | --- | --- | ------- | --------------- | ------- |
|         |         |     |     |     |     | (cid:2) | (cid:1)         | (cid:2) |
solves Problem 2. To see this, note that the objective function U C is constant
(cid:2)
forallQ
| andequaltoW |         |                 | :   |     |     |     |     |     |
| ----------- | ------- | --------------- | --- | --- | --- | --- | --- | --- |
|             | (cid:1) | (cid:1)         |     |     |     |     |     |     |
| U           | C       | 1p C            |     |     |     |     |     |     |
|             | (cid:2) | (cid:7) (cid:2) |     |     |     |     |     |     |
(cid:2)
|     |     |                 | (cid:0)   | (cid:0)   |         |     |     |     |
| --- | --- | --------------- | --------- | --------- | ------- | --- | --- | --- |
|     |     | (cid:1)         | W         | P (cid:7) |         |     |     |     |
|     |     | 1p              |           |           | Q       |     |     |     |
|     |     | (cid:7) (cid:2) | 0 (cid:3) | (cid:0) X |         |     |     |     |
|     |     | (cid:2) (cid:6) |           |           | (cid:8) |     |     |     |
|     |     |                 | (cid:1)   |           | (cid:1) |     |     |     |
(cid:1)
|     |     | W               | P p X                           | Q   |     |     |     |     |
| --- | --- | --------------- | ------------------------------- | --- | --- | --- | --- | --- |
|     |     | (cid:3)         | (cid:7) (cid:3) (cid:7) (cid:2) |     |     |     |     |     |
|     |     | (cid:2) (cid:0) |                                 |     |     |     |     |     |
W
|     |     | (cid:2) (cid:4) |     |     |     |     |     |     |
| --- | --- | --------------- | --- | --- | --- | --- | --- | --- |
12

(Themotivationthisconstructionisobservationthattheexistenceoftheconsistent
linearpricingrulewithstateprices pimpliesthatallfeasibleconsumptionssatisfy
(cid:1)
1p
(cid:7) (cid:2)
C
(cid:2)
W.)
(cid:1)
iii (cid:2) (cid:1)
(cid:1)
i (cid:2) : This part is obvious, since any candidate optimum is dominated by
addingthearbitrage,andthereforetherecanbenoarbitrageifthereisanoptimum.
More formally, adding an arbitrage implies the change of consumption D C
(cid:2)
0,
whichimpliesanincrease inU
(cid:1)
C
(cid:2)
.
One feature of the proof that may seem strange is the degeneracy (linearity) of
the utility function whose existence is constructed. This was all that was needed
for this proof, but it could also be constructed to be strictly concave, additively
separableovertime,andofthevon Neumann-Morgensternclassforgivenproba-
bilities. Assuminganyoftheserestrictionsontheclasswouldmakesomepartsof
thetheoremweaker(
(cid:1)
iii
(cid:2)
implies
(cid:1)
i
(cid:2)
and
(cid:1)
ii
(cid:2)
)atthesametimethatitmakesother
parts stronger (
(cid:1)
i
(cid:2)
or
(cid:1)
ii
(cid:2)
implies
(cid:1)
iii
(cid:2)
). The point is that the theorem is still true
if (iii) is replaced by a much more restrictive class that imposes on U any or all
ofstrictconcavity,someorderofdifferentiability,additiveseparabilityovertime,
and a von Neumann-Morgenstern form with or without specifying the probabil-
ities in advance. All of these classes are restrictive enough to rule out arbitrage,
and general enough to contain a utility function that admits an optimum when
thereisno arbitrage.
The statement and proof of the theorem is a little more subtle if the state space is
infinite-dimensional. Theseparationtheorem istopologicalin nature,so wemust
restrict ourattentiontoa topologicallyrelevantsubsetofthe nonnegativerandom
variables. Also, we may lose the separating hyperplane theorem because the in-
terior of the positive orthant is empty in most of these spaces (unless we use the
sup-normtopology,in whichcase thedual isverylargeandincludesdualvectors
that do not support state prices). However, with some definition of arbitrage in
limits,theeconomic contentoftheFundamentalTheoremcanbemaintained.
13

Pricing Rule Representation Theorem
Dependingonthecontext,therearedifferentusefulwaysofrepresentingthepric-
ing rule. For some abstract applications(like provingput-call parity), it is easiest
touseageneralabstractrepresentationasalinearoperatorL
(cid:1)
c (cid:2) suchthatc
(cid:2)
0 (cid:1)
L
(cid:1)
c
(cid:2)
(cid:2)
0. For asset pricing applications, it is often useful to use either the the
state-pricerepresentationweusedintheFundamentalTheorem,L
(cid:1)
c
(cid:2)
(cid:2)
(cid:229)
w
pw cw ,
or risk-neutral probabilities, L (cid:1) c (cid:2)
(cid:2)
(cid:1) 1 (cid:3) r
(cid:0)
(cid:2) (cid:1) 1E
(cid:0)
(cid:0) cw
(cid:1) (cid:2)
(cid:1) 1 (cid:3) r
(cid:0)
(cid:2) (cid:1) 1(cid:229) p w
(cid:0)
w cw . The
intuition behind the risk-neutral representation (or martingale representation5) is
thatthepriceistheexpecteddiscountedvaluecomputedusingashadowrisk-free
rate (equal to the actual risk-free rate if there is one) and artificial risk-neutral
probabilities p
(cid:0)
that assign positive probability to the same states as do the true
probabilities. Risk-neutralpricing says that all investmentsare fair gambles once
we have adjusted for time preference by discounting and for risk preference by
adjusting the probabilities. The final representation using the state-price density
(orstochasticdiscountfactor)r towriteL (cid:1) c (cid:2)
(cid:2)
E (cid:0) r w cw
(cid:1) (cid:2)
(cid:229) w p w r w cw . Thestate
pricedensitysimplifiesfirst-orderconditionsofportfoliochoiceproblemsbecause
the state-price density measures priced scarcity of consumption. The state-price
density is also handy for continuous-state models in which individualstates have
zero state probabilities and state prices but there exists a well-defined positive
ratioofthe two.
Theorem 2 Pricing Rule Representation Theorem The consistent positive lin-
earpricingrule canberepresentedequivalentlyusing
(cid:1)
i
(cid:2)
anabstractlinearfunctionalL
(cid:1)
c
(cid:2)
thatis positive:
(cid:1)
c
(cid:2)
0
(cid:2) (cid:1)
(cid:1)
L
(cid:1)
c
(cid:2)
(cid:2)
0
(cid:1)
(cid:2)
ii
(cid:2)
positivestateprices p
(cid:2) (cid:2)
0: L (cid:1) c
(cid:2) (cid:2)
(cid:229) W
w (cid:4)
pw cw
1 (cid:1) iii
(cid:2)
positive risk-neutral probabilities p
(cid:0) (cid:2) (cid:2)
0 summing to 1 with associated
shadowrisk-freerater
(cid:0)
: L (cid:1) c (cid:2)
(cid:2)
(cid:1) 1 (cid:3) r
(cid:0)
(cid:2) (cid:1) 1E
(cid:0)
(cid:0) cw
(cid:1)
(cid:0) (cid:1) 1 (cid:3) r
(cid:0)
(cid:2) (cid:1) 1(cid:229) p w
(cid:0)
w cw
(cid:1) iv (cid:2) positivestate-pricedensitiesr
(cid:2) (cid:2)
0: L (cid:1) c (cid:2)
(cid:2)
E (cid:0) r c
(cid:1)
(cid:0) (cid:229) w p w r w cw .
PROOF (cid:1) i (cid:2) (cid:1) (cid:1) ii (cid:2) : Thisisthe knownformofalinearoperatorin´ W .
5Thereasonforcallingtheterm“martingalerepresentation”isthatusingtherisk-neutralprob-
abilitiesmakesthediscountedpriceprocessamartingale,whichisastochasticprocessthatdoes
notincreaseordecreaseonaverage.
14

(cid:1) (cid:1)
ii (cid:1) iii : Note first that the shadow risk-free rate must price the riskless asset
| (cid:2) | (cid:2) |     |     |     |     |
| ------- | ------- | --- | --- | --- | --- |
c 1:
| (cid:2) |     | W         |               |           |     |
| ------- | --- | --------- | ------------- | --------- | --- |
|         |     | (cid:229) | (cid:1) 1E    |           |     |
|         |     | pw        | 1 1 r (cid:1) | (cid:0) 1 |     |
(cid:3) (cid:2)
|     |     | w   | (cid:2) (cid:0) | (cid:0) (cid:1) (cid:3) |     |
| --- | --- | --- | --------------- | ----------------------- | --- |
(cid:4) 1
which implies (since E (cid:0) 1 1) that r 1 p 1 1. Then, matching coefficients
(cid:7)
|     |     | (cid:0) (cid:1) (cid:2) | (cid:0) (cid:2) (cid:0) (cid:0) |     |     |
| --- | --- | ----------------------- | ------------------------------- | --- | --- |
in
W
|     |     | (cid:229) | (cid:1) 1(cid:229) |                 |     |
| --- | --- | --------- | ------------------ | --------------- | --- |
|     |     | pw cw     | 1 r (cid:1)        | p cw            |     |
|     |     |           | (cid:3) (cid:2)    | w               |     |
|     |     |           | (cid:2) (cid:0) w  | (cid:0) (cid:3) |     |
w (cid:4) 1
wehavethatp p 1 p,whichsumsto1asrequiredandinheritspositivityfrom
(cid:7)
(cid:0) (cid:2) (cid:0)
p.
| (cid:1) (cid:1) | Simplyletr | (cid:1) | 1p                      |        | p       |
| --------------- | ---------- | ------- | ----------------------- | ------ | ------- |
| iii (cid:1) iv  | :          | w 1     | r (cid:1) w (whichisthe | sameas | pw w ). |
| (cid:2)         | (cid:2)    | (cid:3) | (cid:2)                 |        |         |
|                 |            | (cid:2) | (cid:0) (cid:0)         |        | (cid:0) |
(cid:1) (cid:1)
| iv i            | : immediate. |     |     |     |     |
| --------------- | ------------ | --- | --- | --- | --- |
| (cid:2) (cid:1) | (cid:2)      |     |     |     |     |
Perhaps what is most remarkable about the Fundamental Theorem and the Rep-
resentation Theorem is that neither probabilities nor preferences appear in the
determination of the pricing operator, beyond the initial identification of which
states have nonzero probability and the assumption that more is preferred to less.
It is this observation that empowers the theory of derivativeasset pricing, and is,
for example, the reason why the Black-Scholes option price does not depend on
the mean return on the underlyingstock. Preferences and beliefs are, however,in
the background: in equilibrium, they would influence the price vector P and/or
thepayoffmatrixX (orthe meanreturnprocessforthe Black-Scholesstock).
Although the focus of this chapter is on the single-period model, we should note
that the various representationshavenatural multiperiodextensions. The abstract
linear functionaland state prices haveessentially the same form, notingthat cash
flows now extend across time as well as states of nature and that there are also
conditionalversionsoftheformulaateachdateandcontingency. Insomemodels,
theinformationsetis generatedby thesamplepath ofsecurityprices; inthiscase
thestateofnatureisasamplepaththroughthetreeofpotentialsecurityprices. For
thestate-pricedensityinmultipleperiods,thereisingeneralastate-price-density
process (cid:0) r whose relativescan be used for valuation. Forexample, the valueat
t
(cid:1)
15

timesofreceiving subsequentcashflowsc
s
(cid:8)
,c
1 s
(cid:8)
... c isgivenby
2 t
t (cid:229)
t (cid:4) s
(cid:8)
E
s
1
(cid:0) r t
Pt
r
s (cid:1) (cid:3)
(10)
where E
s
(cid:0)
(cid:5)
(cid:1)
denotes expectation conditional on information available at time s.
Basically, this follows from iterated expectations and defining r as a cumulative
t
productofsingle-periodr ’s. Similary,wecanwrite risk-neutralvaluationas
P
s (cid:2)
E
(cid:0) s
(cid:0) Pt
(cid:1) 1 (cid:3) r (cid:0) s (cid:2) (cid:1) 1 (cid:3) r (cid:0) s (cid:8) 1 (cid:2) (cid:4)(cid:6) (cid:4)(cid:7) (cid:4) (cid:1) 1 (cid:3) r (cid:0) t (cid:2) (cid:1) (cid:4)
(11)
Note that unless the riskfree rate is nonrandom, we cannot take the discount fac-
tors out of the expectation.6 This is because of the way that the law of iterated
expectationsworks. Forexample,considerthe valueV attime 0ofthe cashflow
0
intime2.
V 0 (cid:2) (cid:1) 1 (cid:3) r (cid:0) 1 (cid:2) (cid:1) 1E (cid:0) 0 (cid:0) V 1 (cid:1) (12)
(cid:2) (cid:1) 1 (cid:3) r (cid:0) 1 (cid:2) (cid:1) 1E (cid:0) 0 (cid:0) (cid:1) 1 (cid:3) r (cid:0) 2 (cid:2) (cid:1) 1E (cid:0) 1 (cid:0) c 2
(cid:2) (cid:1)
(cid:1) (cid:1)
1 (cid:3) r (cid:0) 1 (cid:2) (cid:1) 1E (cid:0) 0 (cid:0) (cid:1) 1 (cid:3) r (cid:0) 2 (cid:2) (cid:1) 1c 2 (cid:1) (cid:4)
Now, (cid:1) 1 (cid:3) r
(cid:0)
1 (cid:2) (cid:1) 1 is outside the expectation (as could be (cid:1) 1 (cid:3) r
(cid:0)
s
(cid:8)
1 (cid:2) (cid:1) 1 in (11)), but
(cid:1) 1 (cid:3) r
(cid:0)
2 (cid:2) (cid:1) 1 cannot come outside the expectation unless it is nonrandom.7 So, it
is best to remember that when interest rates are stochastic, discounting for risk-
neutralvaluationshouldusethe rolled-overspotrate,within theexpectation.
6It would be possible to treat the wholetime period from s to t as a single period andapply
the pricing result to that large period in which case the discounting would be at the apropriate
(cid:9)
t
(cid:0)
s
(cid:11)
-periodrate. Theproblemwiththisisthattherisk-neutralprobabilitieswouldbedifferent
foreachpairofdates,whichisunnecessarilycumbersome.
7Inthespecialcaseinwhichc isuncorrelatedwith 2 (cid:9) 1 (cid:1) r (cid:2) 2 (cid:11)(cid:4) (cid:3) 1 (orinmultipleperiodsifcash
flowsareallindependentofshadowinterestratemoves),wecantaketheexpecteddiscountfac-
tor outside the expectation. In this case, we can use the multiperiod riskfree discount bond rate
for discounting a simple expectedfinal. However,in general, itis best to rememberthe general
formula(11)withtheratesinthedenominatorinsidetheexpectation.
16

3 Various Analyses: Arrow-Debreu World
The portfolioproblem is the starting point of a lot of types of analysis in finance.
Here are some implications that can be drawn from portfolio problems (usually
throughthefirst-order conditions):
(cid:0)
optimalportfoliochoice(assetallocationorstockselection)
(cid:0)
portfolioefficiency
(cid:0)
aggregationandmarket-levelimplications
(cid:0)
assetpricingandperformancemeasurement
(cid:0)
payoffdistributionpricing
(cid:0)
recoveryorestimationofpreferences
(cid:0)
inferenceofexpectations
We can think of many of these distinctions as a question of what we are solving
for when we look at the first-order conditions. In optimal portfolio choice andits
aggregation,wearesolvingforthe portfoliochoicegiventhe preferencesandbe-
liefsaboutreturns. Inassetpricing,wearecomputingtheprices(orrestrictionson
expectedreturns)givenpreferences,beliefsaboutpayoffs,andtheoptimalchoice
(which is itself often derivedusing an aggregation result). In recovery, we derive
preferencesfrombeliefsandidealizedobservationsaboutportfoliochoice,e.g. at
allwealthlevels. Estimationofpreferencesissimilar,butworkswithnoisyobser-
vations of demand at a finite set of data points and uses a restriction in the func-
tionalformorsmoothinginthestatisticalproceduretoidentifypreferences. And,
inferenceofexpectationsderivesprobabilitybeliefsfrompreferences,prices,and
the (observed) optimal demand. In this section, we illustrate the various analyses
inthe caseofanArrow-Debreuworld.
Analysisofthecomplete-marketsmodelhasbeendevelopedbymanypeopleover
a period of time. Some of the more important works include some of the origi-
nal work on competitive equilibrium such as Arrow and Debreu [1954], Debreu
17

[1959] and Arrow and Hahn [1971], as well as some early work specific to secu-
rity markets such as Arrow [1964], Rubinstein [1976], Ross [1976b], Banz and
Miller [1978], and Breeden and Litzenberger [1978]. There are also a lot of pa-
persset inmultipleperiodsthatmadecontributedtothe financeofcompletemar-
kets; although not strictly within the scope of this chapter, we mention just a few
here: Black andScholes [1973], Merton [1971,1973], Cox, Ross, and Rubinstein
[1979],andBreeden[1979].
Optimal portfolio choice The optimal portfolio choice is the choice of con-
sumptions (cid:1) c
0
(cid:3)
c
1
(cid:3) (cid:4)(cid:6) (cid:4)(cid:7) (cid:4)(cid:6) (cid:3)
cW
(cid:2)
andLagrangemultiplierl tosolvethebudgetconstraint
(1) and the first-order conditions (2) and (3). If the inverse I
(cid:1)(cid:6) (cid:5)
(cid:2)
of u
(cid:7)
(cid:1)(cid:6) (cid:5)
(cid:2)
and
the inverse J
(cid:1)(cid:6) (cid:5)
(cid:2)
of v
(cid:7)
(cid:1) (cid:5)
(cid:2)
are both known analytically, then finding the optimum
can be done using the one-dimensional monotone search for l such that J (cid:1) l
(cid:2) (cid:3)
(cid:229) W w (cid:4) pw I 1 (cid:1) l pw (cid:0) p w (cid:2) (cid:2) W. In a couple of special cases, we can solve the opti- mization analytically. For logarithmic utility, v (cid:1) c
(cid:2)
(cid:2)
log (cid:1) c
(cid:2)
and u (cid:1) c
(cid:2)
(cid:2)
d log (cid:1) c
(cid:2)
for some d
(cid:2)
0, optimal consumption is given by c
0 (cid:2)
W
(cid:0)
(cid:1) 1
(cid:3)
d
(cid:2)
and cw
(cid:2) p w Wd
(cid:0)
(cid:1) (cid:1) 1 (cid:3) d (cid:2) pw (cid:2) (for w
(cid:2)
1
(cid:3)(cid:5) (cid:4)(cid:6) (cid:4)(cid:6) (cid:4)(cid:7) (cid:3)
W ). The portfolio choice can also be solved
analyticallyforquadraticutility.
Efficient Portfolios Efficient portfolios are the ones that are chosen by some
agent in a given class of utility functions. For the Arrow-Debreu problem, we
might take the class of utility functions to be the class of differentiable, increas-
ing and strictly concave time-separable von Neumann-Morgenstern utility func-
tions U (cid:1) c (cid:2) (cid:2) v (cid:1) c 0 (cid:2) (cid:3) (cid:229) W w (cid:4) p w cw .8 Since u 1 (cid:1) (cid:5) (cid:2) is increasing and strictly concave, (cid:1)
cw
(cid:2)
cw
(cid:0) (cid:2) (cid:1)
u
(cid:7)
(cid:1)
cw
(cid:2)
(cid:3) (cid:2)
u
(cid:7)
(cid:1)
cw
(cid:2)
. Consequently,thefirst-ordercondition(4)implies
that (cid:1) cw
(cid:2)
cw (cid:0) (cid:2) (cid:1) (cid:1) r w
(cid:2)
r w (cid:0) (cid:2) . Sincethestate-pricedensityr w (cid:0) pw
(cid:0)
p w isamea-
sure of priced social scarcity in state w , this says that we consume less in states
in which consumptionis moreexpensive. This necessary condition for efficiency
isalsosufficient;ifconsumptionreversesthe orderacrossstatesofthe state-price
density, then it is easy to construct a utility function that satisfies the first-order
conditions. Formally,
Theorem 3 Arrow-Debreu Portfolio Efficiency Consider a complete-markets
world (in which agents solve Problem 1) in which state prices and probabilities
are all strictly positive, and let U be the class of differentiable, increasing and
strictlyconcavetime-separablevonNeumann-Morgensternutilityfunctionsofthe
8Anon-time-separableversionwouldbeoftheformU
(cid:9)
c
(cid:11)(cid:5) (cid:4)
(cid:229) W
w (cid:6)
u
1 (cid:9)
c
0 (cid:7)
cw
(cid:11)
.
18

|     | (cid:1) | (cid:1) | (cid:229) W | p   |     |     |     |     |
| --- | ------- | ------- | ----------- | --- | --- | --- | --- | --- |
formU c v c w w cw . ThenthereexistsautilityfunctionintheclassU
|     | (cid:2) | 0 (cid:2) (cid:3) | (cid:4) 1 |     |     |     |     |     |
| --- | ------- | ----------------- | --------- | --- | --- | --- | --- | --- |
(cid:2)
thatchoosestheconsumptionvectorcsatisfyingthe budgetconstraintifandonly
if consumptions at time 1 are in the opposite order as the state-price densities,
|       | (cid:1)             |                                                              | (cid:1) | (cid:1) | (cid:1)                 |         |                           |     |
| ----- | ------------------- | ------------------------------------------------------------ | ------- | ------- | ----------------------- | ------- | ------------------------- | --- |
| i.e., | (cid:1) (cid:0) w w | (cid:0) 1                                                    | W       | cw      | cw                      | r r     | .                         |     |
|       |                     | (cid:7)                                                      | (cid:2) |         | (cid:0) (cid:2) (cid:1) | w       | w (cid:0) (cid:2) (cid:2) |     |
|       | (cid:3)             | (cid:4) (cid:3) (cid:4)(cid:6) (cid:4)(cid:7) (cid:4)(cid:6) | (cid:3) | (cid:2) |                         | (cid:2) |                           |     |
(cid:1)
PROOF The “only if” part follows directly from the first-order condition and
concavity as noted in the paragraph above. For the “if” part, we are given a
consumption vector with the appropriate ordering and we will construct a utility
l
function that will choose it and satisfy the first-order condition with 1. For
|     |     | (cid:1) | (cid:1) | (cid:1) |     | (cid:1) |     | (cid:2) |
| --- | --- | ------- | ------- | ------- | --- | ------- | --- | ------- |
this, choose v c (cid:2) exp c c (cid:2) (cid:2) (so that v c (cid:2) 1 as required by (2), and
|     |         |         |         |         | 0   | (cid:7) | 0       |     |
| --- | ------- | ------- | ------- | ------- | --- | ------- | ------- | --- |
|     | (cid:1) | (cid:2) | (cid:0) | (cid:0) |     |         | (cid:2) |     |
choose u (cid:7) c (cid:2) to be any strictly positiveand strictly decreasing function satisfying
(cid:1)
| u cw    | r       | forallw | 1       | 2                                                                   | W ,forexample,by“connectingthedots”(with |     |     |     |
| ------- | ------- | ------- | ------- | ------------------------------------------------------------------- | ---------------------------------------- | --- | --- | --- |
| (cid:7) | (cid:2) | w       | (cid:0) |                                                                     |                                          |     |     |     |
|         | (cid:2) |         | (cid:2) | (cid:3) (cid:3)(cid:5) (cid:4)(cid:6) (cid:4)(cid:6) (cid:4)(cid:7) | (cid:3)                                  |     |     |     |
appropriate treatment past the endpoints) (cid:1) in the graph of r as a function of cw .
w
(cid:1) (cid:5)
Integratingthisfunctionyieldsautilityfunctionu suchthatthe vonNeumann-
(cid:2)
Morgenstern utility function satisfies the first-order conditions, and by concavity
thisfirst-ordersolutionisasolution.
FRIENDLY WARNING: Therearemanynotionsofefficiencyinfinance: Paretoef-
ficiency, informational efficiency, and the portfolio efficiency we have mentioned
are three leading examples. A common mistake in heuristic arguments is to as-
sumeincorrectlythatonesenseof efficiencynecessarilyimpliesanother.
AggregationAggregationresultstypicallyshowwhatfeaturesofindividualport-
folio choice are preserved at the market level. Many asset pricing results fol-
low from aggregation and the first-order conditions. The most common type of
aggregation result is the efficiency of the market portfolio. For most classes of
preferences we consider, the efficient set is unchanged by rescaling wealth, and
consequentlythemarketportfolioisefficientifandonlyiftheefficientsetiscon-
vex. This is because the market portfolio is a rescaled version of the individual
portfolios. (If the portfolios are written in terms of proportions, no rescaling is
needed.) When the market portfolio is efficient, then we can invertthe first-order
condition for the hypothetical agent who holds the market portfolio to obtain the
pricingrule.
In the Arrow-Debreu world, the market portfolio is always efficient. This is be-
cause the ordering across states is preserved when we sum individual portfolio
choices to form the market portfolio. Consider agents m 1 M with felicity
|     |     |     |     |     |     |     | (cid:2) (cid:3)(cid:5) (cid:4)(cid:6) (cid:4)(cid:6) (cid:4)(cid:7) (cid:3) |     |
| --- | --- | --- | --- | --- | --- | --- | --------------------------------------------------------------------------- | --- |
19

functionsv1 (cid:1)(cid:6) (cid:5) ,...,vM (cid:1) (cid:5) andu1 (cid:1)(cid:6) (cid:5) ,...,uM (cid:1)(cid:6) (cid:5) andoptimalconsumptionsC1 ,...,CM
.
|     | (cid:2) | (cid:2) | (cid:2) | (cid:2) |     |     | (cid:0) (cid:0) |
| --- | ------- | ------- | ------- | ------- | --- | --- | --------------- |
Thefollowingresultsarecloserelativesofstandardresultsingeneralequilibrium
theory.
Theorem 4 AggregationTheoremInapureexchangeequilibriuminacomplete
market,
(cid:1)
| i allagentsordertime |     | 1 consumptioninthe |     |     | sameorderacrossstates, |     |     |
| -------------------- | --- | ------------------ | --- | --- | ---------------------- | --- | --- |
(cid:2)
(cid:1)
| ii aggregate | time1 | consumptionisin |     | thesameorderacrossstates, |     |     |     |
| ------------ | ----- | --------------- | --- | ------------------------- | --- | --- | --- |
(cid:2)
(cid:1)
| iii equilibriumisPareto |     | optimal,and |     |     |     |     |     |
| ----------------------- | --- | ----------- | --- | --- | --- | --- | --- |
(cid:2)
(cid:1)
iv there is a time separable von Neumann-Morgenstern utility function that
(cid:2)
| wouldchooseoptimally |     | aggregateconsumption. |     |     |     |     |     |
| -------------------- | --- | --------------------- | --- | --- | --- | --- | --- |
(cid:1) (cid:1)
| PROOF | i and ii | Immediate,givenTheorem3 |     |     |     |     |     |
| ----- | -------- | ----------------------- | --- | --- | --- | --- | --- |
(cid:2) (cid:2)
(cid:1) Letl
iii mbetheLagrangianmultiplierattheoptimuminthefirstordercondition
(cid:2)
in agent m’s decision problem. Consider the problem of maximizing the linear
|     | functionwithweightsl |     |     | m,namely |     |     |     |
| --- | -------------------- | --- | --- | -------- | --- | --- | --- |
socialwelfare
W
N (cid:0)
|     |     | (cid:229) | l n vn | (cid:1) | (cid:229) un (cid:1) | cn  |     |
| --- | --- | --------- | ------ | ------- | -------------------- | --- | --- |
c
|     |     |             |     | 0 (cid:2) (cid:3) |             | w (cid:2)               |     |
| --- | --- | ----------- | --- | ----------------- | ----------- | ----------------------- | --- |
|     |     |             |     |                   |             | (cid:2) (cid:1) (cid:4) |     |
|     |     | n (cid:4) 1 |     |                   | w (cid:4) 1 |                         |     |
It is easy to verify from the first-order conditions from the equilibrium consump-
tions that they solve this problem too. This is a concave optimization, so the
first-orderconditions aresufficient,andsincethe welfareweightsare positivethe
solutionmustbeParetooptimal(orelseaParetoimprovementwouldincreasethe
objectivefunction).
| (cid:1) | (cid:1) |     |     | (cid:1) |     |     |     |
| ------- | ------- | --- | --- | ------- | --- | --- | --- |
iv Define vA c max (cid:229) N l nvn c to be the first-period aggregate felic-
| (cid:2) | (cid:2) (cid:0) | cn (cid:0) s |             | n (cid:2) |     |         |     |
| ------- | --------------- | ------------ | ----------- | --------- | --- | ------- | --- |
|         |                 | (cid:1)      | n (cid:4) 1 |           | W   | (cid:1) |     |
ity function and define uA c max (cid:229) l nun c to be the second-period
|     |     |     | (cid:2) (cid:0) | cn (cid:0) s | n 1     | n (cid:2) |         |
| --- | --- | --- | --------------- | ------------ | ------- | --------- | ------- |
|     |     |     |                 |              | (cid:4) | (cid:1)   | (cid:1) |
aggregate felicity function. Then the utility function vA c E (cid:0) uA cw is a a
|     |     |     |     |     |     | 0 (cid:2) (cid:3) | (cid:2) |
| --- | --- | --- | --- | --- | --- | ----------------- | ------- |
(cid:1)
time-separable von Neumann-Morgensternutility function that would choose the
market’s aggregate consumption, since the objective function is the same as for
(cid:1)
| thesocial | welfareproblemdescribedundertheproofof |     |     |     |     | iii . |     |
| --------- | -------------------------------------- | --- | --- | --- | --- | ----- | --- |
(cid:2)
There is a different perspective that gives an alternative proof of the existence of
a represenatitive agent (iv). The existence of a representative agent follows from
20

the convexityof the set of efficient portfolios derivedearlier. The main condition
werequire tohavethisworkis thatthe efficient set ofportfolioproportionsis the
sameatallwealthlevels,whichistruehereandtypicallyofthecasesweconsider.
Asset Pricing Asset pricing gets its name from valuation of cash flows, although
asset pricing formulas may be expressed in several different ways, for example
as a formula explaining expected returns across assets or as a moment condition
vA (cid:1)(cid:6) (cid:5) uA (cid:1)(cid:6) (cid:5)
satisfied by returns that can be tested econometrically. Let and be
(cid:2) (cid:2)
the assumed utility function for the hypothetical agent who holds aggregate con-
sumption, as guaranteed by the aggregation theorem, Theorem 4. Then we can
p uA (cid:1) cA vA (cid:1) cA
solve the first-order conditions (2) and (3) to compute pw w (cid:7) w (cid:2) (cid:7) (cid:2)
(cid:2) 0
andthereforethe time-0valuationofthetime-1cashflowvector c cW (cid:0) is
(cid:0) 1
(cid:3) (cid:4)(cid:6) (cid:4)(cid:7) (cid:4)(cid:6) (cid:3)
(cid:1)
(cid:1)
|      |         |                                                                             | W           | uA         | cA        |     |
| ---- | ------- | --------------------------------------------------------------------------- | ----------- | ---------- | --------- | --- |
|      | (cid:1) |                                                                             | (cid:229)   | (cid:7)    | w (cid:2) |     |
| (13) | L c     | cW                                                                          | p           |            | cw        |     |
|      | 1       | (cid:2)                                                                     |             | w (cid:1)  |           |     |
|      |         | (cid:3)(cid:5) (cid:4)(cid:6) (cid:4)(cid:6) (cid:4)(cid:7) (cid:3) (cid:2) |             | vA (cid:7) | cA        |     |
|      |         |                                                                             | w (cid:4) 1 |            | 0 (cid:2) |     |
(cid:1)
uA cA
|     |     |     |     | (cid:7) w (cid:2) |     |     |
| --- | --- | --- | --- | ----------------- | --- | --- |
|     |     |     | E   |                   | cw  |     |
vA (cid:1) cA
|     |     | (cid:2) | (cid:0) | (cid:7)   | (cid:1) (cid:4) |     |
| --- | --- | ------- | ------- | --------- | --------------- | --- |
|     |     |         |         | 0 (cid:2) |                 |     |
(cid:1) (cid:1)
This formula (with state-price density r uA cA vA cA is the right one for
|     |     |     |     |     |     | w (cid:7) w (cid:2) (cid:7) 0 (cid:2) |
| --- | --- | --- | --- | --- | --- | ------------------------------------- |
|     |     |     |     |     |     | (cid:2) (cid:0)                       |
pricing assets, but asset pricing equations are more often expressed as expla-
nations of mean returns across assets or as moment conditions satisfied by re-
turns. Defining the rate of return (the relative value change) for some asset as
(cid:1) w
rw cw P P where cw is the asset value in state and P is the asset’s price.
| (cid:0) |     | (cid:2) |     |     |     |     |
| ------- | --- | ------- | --- | --- | --- | --- |
(cid:0) (cid:0)
Letting r f be the riskfree rate of return (or the riskless interest rate), which must
be
1
(14) r
|            | f       | uA (cid:1) cA       | vA (cid:1) cA |         |     |     |
| ---------- | ------- | ------------------- | ------------- | ------- | --- | --- |
|            | (cid:2) | E (cid:0) (cid:7) w | (cid:7)       |         |     |     |
|            |         | (cid:2)             | 0 (cid:2)     |         |     |     |
|            |         |                     | (cid:0)       | (cid:1) |     |     |
| wehavethat |         | (13)implies         |               |         |     |     |
(cid:1)
|      |              |                 |                   | (cid:0) uA | cA                |                         |
| ---- | ------------ | --------------- | ----------------- | ---------- | ----------------- | ----------------------- |
|      |              | (cid:1)         |                   |            | (cid:7) w (cid:2) |                         |
| (15) | E (cid:0) rw | r 1             | r cov             |            |                   | rw                      |
|      |              | f (cid:3)       | (cid:3) f (cid:2) |            | (cid:1) cA        |                         |
|      |              | (cid:1) (cid:2) |                   | vA         | (cid:7)           | (cid:3) (cid:1) (cid:3) |
0 (cid:2)
21

so that the risk premium (the excess of expected return over the riskfree rate)
is proportional to covariance of return with the state-price density. This is the
representation of asset pricing in terms of expected returns, and is also the so-
calledconsumption-capitalassetpricingmodel(CCAPM)thatismorecommonly
studiedinamultiperiodsetting.
Either of the pricing relations could be used as moment conditions in an asset
| pricingtest,butit | ismorecommonto |     | usethe | momentcondition |     |
| ----------------- | -------------- | --- | ------ | --------------- | --- |
(cid:1)
uA (cid:7) cA
|        | w (cid:2) (cid:1)             |            |     |     |     |
| ------ | ----------------------------- | ---------- | --- | --- | --- |
| (16) 1 | E 1                           | rw (cid:2) |     |     |     |
|        | (cid:2) (cid:0) vA (cid:1) cA | (cid:3)    |     |     |     |
|        | (cid:7) (cid:2)               | (cid:1)    |     |     |     |
0
to test the CCAPM. This same equations characterize pricing for just about all
the pricing models (perhaps with optimal consumption for some agent in place
of aggregate consumption). Recall that the first-order conditions are just about
the same whether markets are complete or incomplete. The main difference is
that the state prices are shadowprices (Lagrangianmultipliers) whenmarkets are
incomplete,butactualassetpricesincompletemarkets. Eitherway,thefirst-order
| conditionsareconsistentwiththesameasset |     |     |     | pricingequations. |     |
| --------------------------------------- | --- | --- | --- | ----------------- | --- |
Payoff Distribution Pricing For von Neumann-Morgenstern preferences (ex-
pectedutility theory) andmoregeneral Machinapreferences, preferences depend
only on distributions of returns and payoffs and do not depend on the specific
states in which those returns are realized. Consider, for example, a simple ex-
|     |     |     | p   | p p |     |
| --- | --- | --- | --- | --- | --- |
ample with three equally probable states, 1 3. Suppose that an
|     |     |     | 1   | 2 3                     |         |
| --- | --- | --- | --- | ----------------------- | ------- |
|     |     |     |     | (cid:2) (cid:2) (cid:2) | (cid:0) |
individual has to choose one of the following payoff vectors for consumption at
|     | (cid:1) | (cid:1) |     | (cid:1) |     |
| --- | ------- | ------- | --- | ------- | --- |
time 1: c 1 (cid:7) 1 2 2 (cid:2) , c 2 (cid:7) 2 1 2 (cid:2) ,and c 3 (cid:7) 2 2 1 (cid:2) . These three consump-
|     | (cid:2) (cid:3) (cid:3) | (cid:2) (cid:3) | (cid:3) | (cid:2) (cid:3) (cid:3) |     |
| --- | ----------------------- | --------------- | ------- | ----------------------- | --- |
tion patterns have the same distribution of consumption, giving consumption of
1 with probability 1 3 and consumption of 2 with probability 2 3. Therefore, an
| agentwithvonNeumann-MorgensternpreferencesormoregeneralMachinapref- | (cid:0) |     |     |     | (cid:0) |
| ------------------------------------------------------------------- | ------- | --- | --- | --- | ------- |
erenceswould find all these consumptionvectorsare equally attractive. However
theydonotallcostthesameunlessthestatepricedensity(andintheexample,the
state price) is the same in all states. However, having the state-price density the
samein all states is a risk-neutral world – all consumption bundlespriced attheir
expected value – which is not very interesting since all risk-averse agents would
22

investment.9
choose a riskless In general, we expect the state-price density to be
highest ofstates of social scarcity, whenthe market is down or the economy is in
recession,sincebuyingconsumptionin statesofscarcityisaform ofinsurance.
(cid:1)
Suppose that the state-price vector is p 3 2 4 . Then the prices of the bun-
|         |         |                                 |         |                 | (cid:7)                 |                                 | (cid:2)                 |                 |                 |                 |         |
| ------- | ------- | ------------------------------- | ------- | --------------- | ----------------------- | ------------------------------- | ----------------------- | --------------- | --------------- | --------------- | ------- |
|         |         |                                 |         |                 | (cid:2)                 | (cid:4) (cid:3) (cid:4) (cid:3) | (cid:4)                 |                 |                 |                 |         |
| dles    | can     | be computed                     | as p    | ca              | 3 1                     | 2 2                             | 4 2                     | 1 5,            | p cb            | 3               | 2       |
|         |         |                                 |         | (cid:7)         | (cid:3)                 | (cid:3)                         |                         |                 | (cid:7)         |                 | (cid:3) |
|         |         |                                 |         | (cid:2)         | (cid:4) (cid:0) (cid:4) | (cid:0)                         | (cid:4) (cid:0)         | (cid:2) (cid:4) |                 | (cid:2) (cid:4) | (cid:0) |
| 2       | 1       | 4 2 1                           | 6,and p | cc              | 3 2 2                   | 2                               | 4 1                     | 1 4.            | Thecheapestcon- |                 |         |
|         | (cid:3) |                                 |         | (cid:7)         | (cid:3)                 | (cid:3)                         |                         |                 |                 |                 |         |
| (cid:4) | (cid:0) | (cid:4) (cid:0) (cid:2) (cid:4) | cc,     | (cid:2) (cid:4) | (cid:0) (cid:4)         | (cid:0)                         | (cid:4) (cid:0) (cid:2) | (cid:4)         |                 |                 |         |
sumption pattern is which places the larger consumption in the cheap states
and the smallest consumption in the most expensive state. This gives us a very
useful cash-value measure of the inefficiency of the other strategies. An agent
|     |     |     |     |     |     |     | cc  |     |     |     | ca  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
will save 1 5 1 4 0 1 cash up front by choosing up front instead of or
|     |     | (cid:4) (cid:4) | (cid:2) (cid:4) |     |     |     |     |     |     |     |     |
| --- | --- | --------------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
1 6 1 4 0 (cid:0) 2 cash up front by choosing cc instead of cb. Therefore, we can
| (cid:4) | (cid:4) | (cid:2) (cid:4) |     |     |     |     |     |     |     |     |     |
| ------- | ------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
interpret0 (cid:0) 1asalowerboundontheamountofinefficiencyinca,sinceanyagent
(cid:4)
would pay that amount to swap to cc and perhaps more to swap to something
better. The only assumption we need for this result is that the agent has prefer-
ences (such as von Neumann-Morgenstern preferences or Machina preferences)
that care only about the disbribution of consumption and not the identity of the
particularstates inwhich differentparts ofthe distributionare realized.
Thegeneral resultis basedon the “deep theoreticalinsight”that you should“buy
more when it is cheaper.” This means that efficient consumption is decreasing in
the state-price density. We can compute the (lower bound on the) inefficiency of
theportfoliobyreordingitsconsumptioninreverseorderasthestate-pricedensity
and computing the decline in cost. The payoff distributionalprice of a consump-
tionpatternisthe priceofgettingthe samedistributionthecheapestpossibleway
| (inreverseorderasthe |     |     | state-pricedensity). |     |     |     |     |     |     |     |     |
| -------------------- | --- | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:1)(cid:6) (cid:5)
Thereisanicegeneralformulaforthedistributionalprice. LetF c (cid:2) bethecumu-
(cid:1) (cid:5)
lative distribution function of consumption and let i be its inverse. Similarly,
c (cid:2)
(cid:1) (cid:5)
let Fr be the cumulative distribution function of the state-price density and let
(cid:2)
(cid:1)(cid:6) (cid:5)
i be its inverse. Let c be the efficient consumption pattern with distribution
r (cid:2)
|     |     | (cid:1)(cid:6) (cid:5) | (cid:0) |     |     |     |     |     |     |     |     |
| --- | --- | ---------------------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
function F . Then the distributional price of the consumption pattern can be
c (cid:2)
9Thisisdifferentfromthereexistingachangeofprobabilitythatgivesrisk-neutralpricing. In
arisk-neutralworld,theactualprobabilitiesarealsorisk-neutralprobabilities.
23

writtenas
|      |                         | (cid:0) 1               |         |     |
| ---- | ----------------------- | ----------------------- | ------- | --- |
| (17) | E c r                   | i (cid:1) z i (cid:1) 1 | z dz    |     |
|      | (cid:0)                 | c (cid:2) r             | (cid:2) |     |
|      | (cid:0) (cid:1) (cid:2) |                         | (cid:4) |     |
|      |                         | z (cid:4) 0             | (cid:0) |     |
Inthisexpression,zhasunitsofprobabilityandlabelsthestatesorderedinreverse
(cid:1) (cid:1)
ofthe state-pricedensity,i 1 z is state-pricedensityin statez,andi z is the
r (cid:2) c (cid:2)
optimal consumption c in state (cid:0) z. This formula is simplest to understand for a
(cid:0)
continuous state space, but also makes sense for finitely many equally-probable
states as in the example, provided we define the inverse distribution function at
| masspointsin |     | thenaturalway. |     |     |
| ------------ | --- | -------------- | --- | --- |
TheoriginalanalysisofPayoffDistributionpricingforcompletefrictionlessmar-
kets was presented by Dybvig [1988a,b]. Payoff Distribution pricing can also be
used in a model with incompletemarkets orfrictions, as developedby Jouini and
| Kallal[2001],butthatanalysisisbeyondthe |         |               | scopeofthischapter. |        |
| --------------------------------------- | ------- | ------------- | ------------------- | ------ |
| 4                                       | Capital | Asset Pricing | Model               | (CAPM) |
The Capital Asset Pricing Model (CAPM) is an asset pricing model based on
equilibrium with agents having mean-variance preferences (as in Problem 4). It
isbasedonthemean-varianceanalysispioneeredbyMarkowitz[1952]andTobin
[1958], and was extended to an equilibrium model by Sharpe [1964] and Lintner
[1965]. Even though there are many more modern pricing models, the CAPM is
stillthemostimportant. Thismodelgivesusmostofourbasicintuitionsaboutthe
trade-offbetweenriskandreturn,abouthowmarketriskispriced,andabouthow
idiosyncratic risk is not priced. The CAPM is also widely used in practice, not
only in the derivation of optimal portfolios but also in the ex post assessment of
performance. Sometimes people still refer to mean-variance analysis by the term
ModernPortfolioTheorywithoutintendingajoke,eventhoughweareapproach-
ingits50thanniversary.
Intheoreticalwork,themean-variancepreferencesassumedinProblem4areusu-
ally motivated by joint normality of returns (a restriction on beliefs) or by a re-
strictionon preferences(a quadraticvonNeumann-Morgensternutility function).
24

When returns are jointly normal, so are portfolio returns, so the entire distri-
bution of a portfolio’s return (and therefore utility that depends only on distri-
bution) is determined by the mean and variance. For quadratic utility, there is
an algebraic relation between expected utility and mean and variance. Letting
(cid:1)
| u c     | k k c       | k c2,   |     |     |     |     |     |
| ------- | ----------- | ------- | --- | --- | --- | --- | --- |
| (cid:2) | 1 (cid:3) 2 | 3       |     |     |     |     |     |
| (cid:2) |             | (cid:0) |     |     |     |     |     |
(cid:1)
| (18) E | (cid:0) u c | k k         | E (cid:0) c k E (cid:0) c2 |                 |                 |     |     |
| ------ | ----------- | ----------- | -------------------------- | --------------- | --------------- | --- | --- |
|        | (cid:2)     | 1 (cid:3) 2 | 3                          |                 |                 |     |     |
|        | (cid:1)     | (cid:2)     | (cid:1) (cid:0)            | (cid:1)         |                 |     |     |
|        |             |             | (cid:1)                    | (cid:1)         | (cid:1) 2       |     |     |
|        |             | k k         | E (cid:0) c k var          | c               | E (cid:0) c     |     |     |
|        |             | 1 (cid:3) 2 | 3                          | (cid:2) (cid:3) | (cid:2) (cid:2) |     |     |
|        |             | (cid:2)     | (cid:1) (cid:0)            |                 | (cid:1) (cid:3) |     |     |
which depends on the preferences parameters k , k , and k and the mean and
|     |     |     |     |     | 1 2 | 3   |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
variance of c and not on other features of the distribution (such as skewness or
kurtosis). Neitherassumptionisliterallytrue,butwemustrememberthatmodels
| mustbesimplerthan |     | theworld | iftheyare | tobeuseful. |     |     |     |
| ----------------- | --- | -------- | --------- | ----------- | --- | --- | --- |
Youmaywonderwhyweneedtomotivatetherepresentationofpreferencesbythe
(cid:1)
utilityfunctionV m v ,sinceitmayseemveryintuitivetowritedownpreferences
(cid:2)
(cid:3)
for risk an return directly. However, it is actually a little strange to assume that
these preferences apply to all random variables. For example, if there is a trade-
offbetweenriskandreturn(sothe agentcaresaboutrisk), thenthereshouldexist
|     |     |     |     |     | (cid:1) | (cid:1) |     |
| --- | --- | --- | --- | --- | ------- | ------- | --- |
m 1 m 2 andv 1 v 2 0such thatthe agentV m 1 v 1 (cid:2) V m 2 v 2 (cid:2) andtheagent
| (cid:2) |     | (cid:2) (cid:2) |     |     | (cid:3) (cid:2) | (cid:3) |     |
| ------- | --- | --------------- | --- | --- | --------------- | ------- | --- |
would turn down the higher return because of the higher risk. However,it is easy
to construct random variables x and x with x x that have means m and
|     |     |     | 1   | 2   | 1 2 |     | 1   |
| --- | --- | --- | --- | --- | --- | --- | --- |
(cid:2)
m and variances v and v . In other words, a non-trivial mean-variance utility
| 2   |     | 1   | 2   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
function (that does not simply maximize the mean) cannot always prefer more to
less.
The two typical motivations of mean-variance preferences have different resolu-
tionsofthisconundrum. Quadraticutilitydoesnotprefermoretoless,sothereis
no inconsistency. This is not a nice feature of quadratic utility but it may not be
a fatal problem either. Multivariate normality does not define preferences for all
random variables, and in particular the random variables that generate the para-
doxarenotavailable. Whenusinganymodel,weneedtothinkaboutwhetherthe
unrealisticfeaturesofthemodelare importantforthe applicationathand.
Many important features of the CAPM are illustrated by Figures 1 and 2. In
Figure 1, F is the efficient frontier of risky asset returns in means and standard
deviations. Other feasible portfolios of risky assets will plot to the right of F and
25

Figure1: Theefficientfrontierinmeansandstandarddeviations
standard deviation of return = q ’V q
)
(
-
m
’
q+
r1
r
=
nruter
naem
E
q M F
q i
r
f
will not be chosen by any agent who can choose only among the risky assets and
prefers less risk at a given mean. And, agents who choose higher mean given
the standard deviation, will only choose risky portfolios on the upper branch of
F, which is called the positively efficient frontier of risky assets. When the risk-
free asset r is always available, all agents preferring a higher mean at a given
f
standard deviation will choose a portfolio along the frontier E.10 One important
feature in either case is two-fund separation, namely, that the entire frontier F
or E is spanned by two portfolios, which can be chosen to be any portfolios at
two distinct points on the frontier. This is called a “mutual fund separation” re-
sult because we can separate the portfolio choice problem into two stages: first
findtwo “mutual funds”(portfolios)spanning the efficientfrontier (whichcan be
chosen independently of preferences) and then find the mixture of the two funds
appropriate for the particular preferences. For a typical agent who prefers more
to less and prefers to avoid risk, preferences are increasing up and to the left in
10Foragentswhopreferlessriskatagivenmeanbutmaynotpreferahighermeanatagiven
levelofrisk,thereisanotherbranchofE belowthatisthereflectionofitscontinuationtotheleft
oftheaxis.
26

Figure2: Thesecurity marketlineconnectingrisk andreturn
q ’ q q ’ q
beta = V V
M M M
)
(
-
m
’
q+
r1
r
=
nruter
naem
q M
q s
q e
a s
a u
q u
r
f
1.0
Figure1. Amorerisk-averseagentwillchooseaportfolioonthelowerleftpartof
thefrontier,withlowreturnbutlowrisk,andalessrisk-averseagentwillchoosea
portfolioon the upper right part ofthe frontier, acceptinghigher risk in exchange
forhigherreturn.
Figure 1 also illustrates the Sharpe ratio (Sharpe [1966]), which is used for per-
formance measurement. The line through the riskless asset r and the market
f
portfolio q M has a slope in Figure 1 that is larger than the slope for any ineffi-
cient portfolio such as q i. The slope of the line through a particular portfolio is
the Sharpe ratio for the particular portfolio. The Sharpe ratio is largest for an
efficient portfolio and the shortfall below that amount is the measure of ineffi-
ciency for any other portfolio. (An even greater Sharpe ratio would be possible
if the efficient proxy is inefficient in sample or if we are considering a portfolio,
say from an informed trading strategy, that is not a fixed portfolio of the assets.)
In practice, due to random sampling error, even an efficient portfolio will have a
measured Sharpe ratio that is not the largest value. When stock returnsare Gaus-
sian, there is an important connection between the measured Sharpe ratio of the
27

market portfolio and the likelihood ratio test of the CAPM (Gibbons, Ross, and
Shanken[1989]).
Figure 2 shows the security market line, which quantifies the relation between
risk and return in the CAPM. Risk is measured using the beta coefficient, which
is the slope coefficient of a linear regression of the asset’s return on the market’s
return. If the CAPM is true, all assets and portfolios will plot on the Security
MarketLine (SML) that goes through the riskfree asset r and the market portfo-
f
lio of risky assets q M. In practice, measured asset returns are affected by random
sampling error; if the CAPM is true it is entirely random whether a portfolio will
plot above or below the security market line ex post. The use of beta as the ap-
propriatemeasureofrisktellsus that investorsare rewardedfortakingon market
risk(correlatedwithmarketreturns)nottakingonidiosyncraticrisk(uncorrelated
withthemarket).
If the security market line tells us how much of a reward is justified for a given
amount of risk, it makes intuitive sense that deviations from the security market
linecanbeusedtomeasuresuperiororinferiorperformance. Thisistheintuition
behindtheTreynorIndexandJensen’salpha(Treynor[1965]andJensen[1969]).
For example, in Figure 2, Jensen’s alpha for q s is a s
(cid:2)
0, indicating superior
performance, and Jensen’s alpha for q u is a u
(cid:2)
0, indicating underperformance.
Unfortunately, any formal motivation for using Jensen’s alpha must come from
outsidethe CAPM, sinceif the CAPM is truethen the expectedvalueof Jensen’s
alpha is zero and the realized value is purely random. Theoretical models that
incorporate superior performance from information-gathering have given mixed
resultsonthevalueofusingthesecuritymarketlineformeasuringperformance: a
superiorperformerwithsecurity-specificinformationwillhaveapositiveJensen’s
alpha, but for market timing a superior performer may have a negative Jensen’s
alpha and may even plot inside the efficient frontier for static strategies (Mayers
and Rice [1979] and Dybvig and Ross [1985]). The Treynor Index is the slope
of the line through the evaluated portfolio and the riskfree asset in the security
marketline diagramFigure2. Performanceis determinedby comparingaportfo-
lio’s Treynor Index to that of the market; a larger Treynor Index indicates better
performance. The Treynor index will indicate superior or inferior performance
compared to the market the same as the Jensen measure. However, the ordering
ofsuperiororinferiorperformerscanbedifferentbecausetheTreynormeasureis
adjustedforleverage.
28

The main results of the CAPM can be derived from the first-order condition (9).
| Thefirst-orderconditionforagentn |     |         |         |     | is  |     |     |     |     |
| -------------------------------- | --- | ------- | ------- | --- | --- | --- | --- | --- | --- |
| (19)                             | µ   | r1      | l nSq n |     |     |     |     |     |     |
|                                  |     | (cid:2) | (cid:3) |     |     |     |     |     |     |
(cid:0)
|       | l   |              | (cid:1)           |           | (cid:1)          |             |     | (cid:1) | q               |
| ----- | --- | ------------ | ----------------- | --------- | ---------------- | ----------- | --- | ------- | --------------- |
| where |     | n 2Vn        | m v               | Vn        | m v ,evaluatedat | the optimum | m   | r       | µ r1 n          |
|       |     |              | v (cid:7) (cid:2) | m (cid:7) | (cid:2)          |             |     | (cid:3) | (cid:2) (cid:7) |
|       |     | q (cid:2) Sq | (cid:3)           | (cid:0)   | (cid:3)          |             |     | (cid:2) | (cid:0)         |
and v n n. Now, the market portfolio is the wealth-weighted average of all
(cid:7)
(cid:2)
agents’portfolios,
|      |     | (cid:229) N | wnq n     |     |     |     |     |     |     |
| ---- | --- | ----------- | --------- | --- | --- | --- | --- | --- | --- |
| (20) | q M | n           | (cid:4) 1 |     |     |     |     |     |     |
N
|     |     | (cid:2) (cid:229) | wn  | (cid:3) |     |     |     |     |     |
| --- | --- | ----------------- | --- | ------- | --- | --- | --- | --- | --- |
n (cid:4) 1
and consequently we have the wealth-weighted average of the first-order condi-
tions
|      |         |         | l MSq M |         |     |     |     |     |     |
| ---- | ------- | ------- | ------- | ------- | --- | --- | --- | --- | --- |
| (21) | µ       | r1      |         |         |     |     |     |     |     |
|      | (cid:0) | (cid:2) |         | (cid:3) |     |     |     |     |     |
where
|      |     | (cid:229) N       | wnl n     |         |     |     |     |     |     |
| ---- | --- | ----------------- | --------- | ------- | --- | --- | --- | --- | --- |
| (22) | l M | n                 | (cid:4) 1 |         |     |     |     |     |     |
|      |     | (cid:2) (cid:229) | N wn      | (cid:4) |     |     |     |     |     |
n 1
(cid:4)
solveforl
| Wecanplugin |     |     | themarketportfolioto |     |     | M andweobtain |     |     |     |
| ----------- | --- | --- | -------------------- | --- | --- | ------------- | --- | --- | --- |
Sq M
(cid:1)
| (23) | µ   | r1  |     | µM  | r   |     |     |     |     |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:2)
|     | (cid:0) | (cid:2) | q M Sq M | (cid:0) | (cid:3) |     |     |     |     |
| --- | ------- | ------- | -------- | ------- | ------- | --- | --- | --- | --- |
(cid:7)
whereµM q M µ isthe meanreturnon themarketportfolioofriskyassets.
|     |     | (cid:0) | (cid:7) |     |     |     |     |     |     |
| --- | --- | ------- | ------- | --- | --- | --- | --- | --- | --- |
Applying (23)to obtain the expectedexcessreturn ofa portfolioq of riskyassets
(withq 1 1sinceaportfolioofriskyassetsdoesnotincludeanyholdingsofthe
(cid:7)
(cid:2)
29

riskfreeasset),wehavethat11
| (24) q  | µ r l | Mq Sq M |     |     |     |     |     |
| ------- | ----- | ------- | --- | --- | --- | --- | --- |
| (cid:7) |       | (cid:7) |     |     |     |     |     |
(cid:2)
|     | (cid:0) b | q (cid:1) µM |     |     |     |     |     |
| --- | --------- | ------------ | --- | --- | --- | --- | --- |
r
(cid:2)
|     | (cid:2) | (cid:0) | (cid:3) |     |     |     |     |
| --- | ------- | ------- | ------- | --- | --- | --- | --- |
where b q is the portfolio’s beta, which is the slope coefficient of a regression of
| thereturnsofthe | portfolioq | ’sreturnon |     | themarketreturn, |     |     |     |
| --------------- | ---------- | ---------- | --- | ---------------- | --- | --- | --- |
q Sq M
| q   | (cid:7) |     |     |     |     |     |     |
| --- | ------- | --- | --- | --- | --- | --- | --- |
(25) b
(cid:0)
|     | q M Sq M | (cid:4) |     |     |     |     |     |
| --- | -------- | ------- | --- | --- | --- | --- | --- |
(cid:7)
| TheSMLequationweplottedin |                         |                 | Figure2is |     | (24). |     |     |
| ------------------------- | ----------------------- | --------------- | --------- | --- | ----- | --- | --- |
| Foraportfolioq            | ,Jensen’salphaisgivenby |                 |           |     |       |     |     |
| q                         | b q (cid:1) µM          |                 |           |     |       |     |     |
| (26)                      | µ r                     | r               |           |     |       |     |     |
| (cid:7)                   |                         | (cid:2)         |           |     |       |     |     |
|                           | (cid:0) (cid:0)         | (cid:0) (cid:3) |           |     |       |     |     |
itsTreynorindexis
q
|     | µ r |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
(27) (cid:7)
b q (cid:0)
(cid:3)
| anditsSharperatio |     | is  |     |     |     |     |     |
| ----------------- | --- | --- | --- | --- | --- | --- | --- |
| q                 | µ r |     |     |     |     |     |     |
(cid:7)
| (28) | (cid:0) |     |     |     |     |     |     |
| ---- | ------- | --- | --- | --- | --- | --- | --- |
q Sq
| (cid:0) | (cid:4) |     |     |     |     |     |     |
| ------- | ------- | --- | --- | --- | --- | --- | --- |
(cid:7)
The portfolios encountered in practice are actively managedand the formulas for
theseperformancemeasureswouldbemorecomplexthanforthesimplefixedmix
11We looked at the simpler case in the text, but the same pricing result holds for a portfolio
q
including a holding in the risky asset. In this case, the expected return on the portfolio is µ (cid:1)
| q randtheexpectedexcessreturnisq |     |     |     |                         | q q                              | q                       | (cid:1) |
| -------------------------------- | --- | --- | --- | ----------------------- | -------------------------------- | ----------------------- | ------- |
| 1 1                              |     |     |     | µ (cid:1) 1             | 1 r r                            | µ 1r.                   |         |
| (cid:9) (cid:0) (cid:1) (cid:11) |     |     |     | (cid:1) (cid:9) (cid:0) | (cid:1) (cid:11) (cid:0) (cid:4) | (cid:1) (cid:0) (cid:1) |         |
30

of assets q . However, the concepts are unchanged with the natural adaptations,
e.g.,replacing q
(cid:7)
µ by the sample meanreturn on the portfolioand replacingb q
(cid:2) q (cid:7) Sq M
(cid:0)
q M (cid:7) Sq M by the estimatedslopefrom the regressionofthe portfolioreturn
onthe marketreturn.
5 Mutual Fund Separation Theory
The general portfolio problem for arbitrary preferences and distributions is suf-
ficiently rich so as to allow for nearly any sort of qualitative behavior (see Hart
[1975] for negativeresults or Cass and Stiglitz [1972] for positive results in spe-
cial cases). In an effort to simplify this problem and obtain results that allow for
aggregationsothatthegeneralbehaviorofthemarketcanbeunderstoodinterms
of the primitive properties of risk aversion and of the underlying distributions a
collectionofresultsknownasseparationresultshavebeendeveloped.
MutualFundSeparationistheseparationofportfoliochoiceintotwo stages. The
firststageistheselectionofsmallsetof“mutualfunds”(portfolios)amongwhich
choice is to be made, and the second stage is the selection of an allocation to
the mutual funds. We have “k-fund separation” for a particular class of distribu-
tions and a particular class of utility functions if for each joint return distribution
in the class there exist k funds that can be used in the two-step procedure while
making agents with utility in the class and any wealth level just as well off as
the choosing in the whole market. The important restriction is that the choice
of the funds is done once for the entire class of utility functions. In the liter-
ature, there are two general approaches: one approach (Hakansson [1969] and
Cass and Stiglitz [1970]) restricts utility functions and has relatively unrestricted
distributions, while the other approach (Ross [1978a]) restricts distributions and
hasrelativelyunrestricted utility functions. Either approach is useful for deriving
assetpricingresultsbecause,forexample,ifindividualinvestorsholdmixturesof
twofunds,then themarketportfoliomustbeamixtureofthe sametwo funds.
31

| Preference |     | Approach |     |     |     |     |     |     |     |
| ---------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
The preference approach focuses on classes of special utility functions. Many
of the results involve utility functions that have properties of homotheticity or
invariance. It is important that we require the same funds to work for each utility
function at all wealth levels, since this avoids “accidental” cases such as a set
containinganytwoutilityfunctionsoverreturns. Analysisinthissectionwilluse
Problem3, insome casesaddingtheassumptionthat oneofthe assetsis riskless.
First, we consider one-fund separation, which requires all portfolio choices to
line in a ray. Giventhe budget constraint, this implies that the portfolio choice is
just proportional to wealth. For this to happen at all prices, the preferences have
to be homothetic. And, given the von Neumann-Morgenstern restriction, this is
|     |     |     |     |     |     | (cid:1) | (cid:1) |     | (cid:1) |
| --- | --- | --- | --- | --- | --- | ------- | ------- | --- | ------- |
equivalent to either logarithmic utility, u c log c , or power utility, u c
|     |           |             |     |     |     | (cid:2) | (cid:2) |     | (cid:2) |
| --- | --------- | ----------- | --- | --- | --- | ------- | ------- | --- | ------- |
| c1  | R (cid:1) |             |     |     |     | (cid:2) |         |     | (cid:2) |
|     | (cid:1) 1 | R (cid:2) . |     |     |     |         |         |     |         |
|     | (cid:0)   | (cid:0)     |     |     |     |         |         |     |         |
Theorem 5 (one-fundseparationfrompreferences) Thefollowingareequivalent
| propertiesofa |     |     | nonemptyclassU |     | of utilityfunctions: |     |     |     |     |
| ------------- | --- | --- | -------------- | --- | -------------------- | --- | --- | --- | --- |
1. Foreachjointdistributionsofsecurityreturnsthereexistsasingleportfolio
q ,suchthatanyu U isjustaswelloffchoosingamultipleofq aschoosing
(cid:4)
|     | fromthe |     | entiremarket. |     |     |     |     |     |     |
| --- | ------- | --- | ------------- | --- | --- | --- | --- | --- | --- |
2. The class U consists of a single utility function (up to an affine transform
|     |     |     |     |     |     |     |     | (cid:1) (cid:1) | (cid:1) |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------- | ------- |
that leaves preferences unchanged) of the form u c log c or u c
|     |     |         |         |     |     |     |     | (cid:2) (cid:2) | (cid:2) |
| --- | --- | ------- | ------- | --- | --- | --- | --- | --------------- | ------- |
|     |     | (cid:1) |         |     |     |     |     | (cid:2)         | (cid:2) |
|     | c1  | R 1     | R .     |     |     |     |     |                 |         |
|     |     | (cid:1) | (cid:2) |     |     |     |     |                 |         |
|     |     | (cid:0) | (cid:0) |     |     |     |     |                 |         |
PROOF : ((2) (1)) Let u be the single utility function in U. The objective
(cid:1)
(cid:1)
function in terms of portfolio proportions is E (cid:0) u wq r . In the log case, this is
|     |         |     |         |     |         |     | (cid:7) (cid:2) |     |     |
| --- | ------- | --- | ------- | --- | ------- | --- | --------------- | --- | --- |
|     | (cid:1) |     | (cid:1) |     | (cid:1) |     | (cid:1)         |     |     |
E (cid:0) log wq r log w E (cid:0) log q r ,andmaximizingtheobjectiveisthesameas
|     |     | (cid:7) (cid:2) | (cid:2) | (cid:3) | (cid:7) (cid:2) |     |     |     |     |
| --- | --- | --------------- | ------- | ------- | --------------- | --- | --- | --- | --- |
|     |     | (cid:1) (cid:2) |         |         | (cid:1)         |     |     |     |     |
maximizing the second term which does not depend on w. In the power case, the
|     |     |     | (cid:1) wq 1 | R (cid:1) | w1 RE | (cid:1) q 1 | R (cid:1) |     |     |
| --- | --- | --- | ------------ | --------- | ----- | ----------- | --------- | --- | --- |
objective is E (cid:0) r (cid:1) 1 R (cid:1) (cid:0) r (cid:1) 1 R , and maximizing
|     |     |     | (cid:7) (cid:2) |         | (cid:2)                 | (cid:7) (cid:2) |         | (cid:2)         |     |
| --- | --- | --- | --------------- | ------- | ----------------------- | --------------- | ------- | --------------- | --- |
|     |     |     |                 | (cid:0) | (cid:0) (cid:1) (cid:2) |                 | (cid:0) | (cid:0) (cid:1) |     |
the objectiveis the sameas maximizing the secondfactor which does not depend
on w. In either case, choosing the proportionsthat work at onewealth levelgives
| aportfolioinproportionsthat |     |     |     |     | willbeoptimal | atallwealth |     | levels. |     |
| --------------------------- | --- | --- | --- | --- | ------------- | ----------- | --- | ------- | --- |
32

((1)
(cid:1)
(2)) Suppose u is an element of the classU. Then, the first-order condition
foranoptimumimplies
E (cid:0) (cid:1) 1
(cid:3)
r
(cid:0)
g
(cid:2)
u
(cid:7)
(cid:1) Wq
(cid:7)
(cid:1) 1
(cid:3)
r
(cid:2) (cid:2)
(cid:1) (cid:2)
0
(cid:3)
(29)
where g
(cid:2)
l
(cid:0)
E (cid:0) u
(cid:7)
(cid:1) Wq
(cid:7)
(cid:1) 1
(cid:3)
r
(cid:2) (cid:2)
(cid:1)
. In general, r must satisfy (8) and may vary with
W,butforcompletemarketsr isuniquelydeterminedby(8)andmaybetakenas
given. Forthesameportfolioweightsq tobeoptimalforallW,itfollowsthatthe
derivativeofthe first-orderconditionis zeroandforcompletemarketswehave
E (cid:0) (cid:1) 1
(cid:3)
r
(cid:0)
g
(cid:2)
q
(cid:7)
(cid:1) 1
(cid:3)
r
(cid:2)
u
(cid:7)(cid:7)
(cid:1) Wq
(cid:7)
(cid:1) 1
(cid:3)
r
(cid:2) (cid:2)
(cid:1) (cid:2)
0
(cid:4)
(30)
Now, one-fund separation implies that in all complete markets (29) implies (30),
butthe onlywaythiscan alwaysbetrueif everwhere
cu
(cid:7)(cid:7)
(cid:1)
c
(cid:2)
(cid:2) (cid:0)
Ru
(cid:7)
(cid:1)
c
(cid:2)
(31)
whereR
(cid:2)
1implieslogarithmicutilityandanyotherR
(cid:0)
0impliespowerutility.
(R
(cid:0)
0 corresponds to a convex utility function.) And, all utility functions in the
classU must correspond to the same preferences or else is it is easy to show the
samefund wouldnotworkforbothinjustaboutany 2-stateexample.
The utility functions in the theorem comprise the Constant Relative Risk Aver-
sion (CRRA) class for which the Arrow-Pratt coefficient of relative risk aver-
sion
(cid:0)
cu
(cid:7)(cid:7)
(cid:1) c
(cid:2)
(cid:0)
u
(cid:7)
(cid:1) c
(cid:2)
is a constant. (See Arrow [1965] and Pratt [1964].12) Other
special utility functions lead to two-fund separation if there is a riskless asset.
The Constant Absolute Risk Aversion (CARA) class of utility functions of the
formu
(cid:1)
c
(cid:2)
(cid:2) (cid:0)
exp
(cid:1)
(cid:0)
Ac
(cid:2)
(cid:0)
AforwhichtheArrow-Prattcoefficientofabsoluterisk
aversion
(cid:0)
u
(cid:7)(cid:7)
(cid:1)
c
(cid:2)
(cid:0)
u
(cid:7)
(cid:1)
c
(cid:2)
is constant leads to a special two-fund separationresult in
which the risky portfolio holding is constant and only the investment in the risk-
free asset is changing as wealth changes. When there is a riskless asset, there is
also two-fund separation in the larger Linear Risk Tolerance (LRT) class which
12SomeotherwaysofcomparingriskaversionaregivenbyKihlstro¨m,
33

encompasses the other two classes as well as wealth-translated relative risk aver-
|     |     | (cid:1) (cid:1) | (cid:1) (cid:1) | 1 R (cid:1) |     |
| --- | --- | --------------- | --------------- | ----------- | --- |
sionpreferencesoftheformu c (cid:2) log c c 0 (cid:2) oru c (cid:2) c c 0 (cid:2) (cid:1) 1 R (cid:2) . The
|     |     | (cid:2) | (cid:2) | (cid:1) (cid:1) |     |
| --- | --- | ------- | ------- | --------------- | --- |
linearrisktoleranceclassisdefinedbytherisktolerance (cid:0) u (cid:0) c u (cid:0) c havingthe (cid:0)
(cid:7) (cid:2) (cid:7)(cid:7) (cid:2)
(cid:1)
linear form a c c . We can include in this class the satiated (cid:0) (cid:0) utility functions
|     | 0 (cid:2) |         |     |     |     |
| --- | --------- | ------- | --- | --- | --- |
|     | (cid:1)   | (cid:1) |     |     |     |
oftheform c (cid:0) c 1 R 1 R definedforc c (andis typicallyextendedto
|     | 0 (cid:2)       | (cid:1) (cid:2) | 0       |     |     |
| --- | --------------- | --------------- | ------- | --- | --- |
|     | (cid:0) (cid:0) | (cid:0) (cid:0) | (cid:0) |     |     |
c c in the obvious way in the quadratic case R 1). With quadratic utility,
0
| (cid:2) |     |     | (cid:2) (cid:0) |     |     |
| ------- | --- | --- | --------------- | --- | --- |
we have a special result of two-fund separation even without a riskfree asset due
to linearity of marginal utility. In these results, all utility functions in the classU
must have the same power (or absolute risk aversion coefficient for exponential
utility) but can have different translates c (but exponential utility is unchanged
0
undertranslation). Fordetailsandproofs,seeCassandStiglitz[1970].
Beliefs
We have already seen one case of separation based on beliefs, which is in mean-
variance analysis motivatedby multivariatenormality,as discussed in the section
on the CAPM. Mean-variance preferences can also be derived from more gen-
eral transformed spherically distributed preferences duscussed by Chamberlain
[1982]. We turn now to a strictly more general class, the separating distributions
ofRoss[1978a].
The central intuition behind the separating distributions is that risk-averse agents
willnotchoosetotakeonriskwithoutanyreward. Thisisthesameintuitionasin
mean-varianceanalysis,butitissomewhatmoresubtlebecauseriskcannolonger
becharacterizedbyvarianceforgeneralconcavevonNeumann-Morgensternpref-
erences. Theappropriatedefinitionofrisk is relatedto Jensen’sinequality,which
(cid:1) (cid:5) (cid:1)
says that for any convex function f and any random variable x, E f x
(cid:2) (cid:0) (cid:2)
| (cid:1) |     | (cid:1)(cid:6) (cid:5) |     |     | (cid:1) (cid:0) |
| ------- | --- | ---------------------- | --- | --- | --------------- |
f E (cid:0) x , with strict equality if f is strictly concave and x is not (almost surely)
| (cid:2) |     | (cid:2) |     |                        |     |
| ------- | --- | ------- | --- | ---------------------- | --- |
| (cid:1) |     |         |     | (cid:1)(cid:6) (cid:5) |     |
constant. A risk-averse von Neumann-Morgenstern utility function u is con-
(cid:2)
(cid:1)(cid:6) (cid:5)
cave (so that u is convex), and consequently for any random consumption c,
(cid:2)
| (cid:1) | (cid:1) (cid:0) |     |     |     |     |
| ------- | --------------- | --- | --- | --- | --- |
E (cid:0) u c u E (cid:0) c ,with strict inequality for strictly concave u and nonconstant c.
| (cid:2)        | (cid:2)         |     |     |     |     |
| -------------- | --------------- | --- | --- | --- | --- |
| (cid:1)(cid:1) | (cid:0) (cid:1) |     |     |     |     |
More importantly for portfolio choice problems, we can use Jensen’s inequality
and the law of iterated expectations to conclude that adding conditional-mean-
zeronoisemakesarisk-averseagentworseoff. Thatgivesusthefollowinguseful
result:
34

e
| Lemma1 | If E (cid:0) c          | 0 andu isconcave,then |     |     |
| ------ | ----------------------- | --------------------- | --- | --- |
|        | (cid:3)                 | (cid:1) (cid:2)       |     |     |
|        | (cid:1)                 | (cid:1)               |     |     |
| (32) E | (cid:0) u c e           | E (cid:0) u c         |     |     |
|        | (cid:2)                 | (cid:2)               |     |     |
|        | (cid:3) (cid:1) (cid:0) | (cid:1) (cid:4)       |     |     |
PROOF
|        | (cid:1) e       | (cid:1)                 | e                       |     |
| ------ | --------------- | ----------------------- | ----------------------- | --- |
| (33) E | (cid:0) u c     | E (cid:0) E (cid:0) u c | c                       |     |
|        | (cid:3) (cid:2) | (cid:3)                 | (cid:2)                 |     |
|        | (cid:1)         | (cid:2) (cid:1)         | (cid:3) (cid:1) (cid:1) |     |
|        |                 | E (cid:0) u E (cid:0) c | e c                     |     |
(cid:2)
|     |     | (cid:0) (cid:3) | (cid:3) (cid:1) (cid:1) |     |
| --- | --- | --------------- | ----------------------- | --- |
(cid:1)
E (cid:0) u c
(cid:2)
|                            |     | (cid:2) (cid:1) (cid:3)    |     |     |
| -------------------------- | --- | -------------------------- | --- | --- |
| byJensen’sinequalityandthe |     | lawofiteratedexpectations. |     |     |
In fact, it can be shown that one random variable is dominated by another with
the same mean for all concave utility functions if and only the first has the same
distribution as the second plus conditional-mean-zero noise. This is one of the
resultsofthetheoryofStochasticDominance,whichwaspioneeredbyQuirkand
Saposnik[1962]andHadarandRussell[1969]andwaspopularizedbyRothschild
andStiglitz[1970,1971].
The basic idea behind the separating distributions is that there are k funds (e.g. 2
funds for 2-fund separation) such that everything else is equal to some portfolio
| ofthek | funds,plusconditional-mean-zeronoise. |     |     | Formally,wehave |
| ------ | ------------------------------------- | --- | --- | --------------- |
Theorem 6 Consideraworldwithk fundsthatareportfolioswithweightsy1,...,
(cid:1)
yk summing (cid:1) (cid:0) j 1 yj 1 (or in vector notation, 1 y 1 ).13 Further assume that
|               | (cid:2) | (cid:7)      |     | (cid:7) (cid:7) |
| ------------- | ------- | ------------ | --- | --------------- |
|               |         | (cid:2)      |     | (cid:2)         |
| returnsoneach | asseti  | canbewritten | as  |                 |
k
|        | (cid:229) b yj | e         |     |     |
| ------ | -------------- | --------- | --- | --- |
| (34) r |                | (cid:7) r |     |     |
|        | i ij           | (cid:3) i |     |     |
(cid:2)
j (cid:4) 1
13As discussed earlier, the dimension of 1 is determined by context; in 1 y 1 , the first oc-
(cid:1) (cid:4) (cid:1)
| curenceof1isk | (cid:1) 1andthesecondoccurenceof1isn |     |     | (cid:1) 1. |
| ------------- | ------------------------------------ | --- | --- | ---------- |
35

|         | b                       | e ),where(cid:229) | k                              | b 1(i.e.,1b |         |                              |
| ------- | ----------------------- | ------------------ | ------------------------------ | ----------- | ------- | ---------------------------- |
| (i.e.,r | y r                     |                    |                                |             |         | 1)andforalllinearcombination |
|         | (cid:7) (cid:7) (cid:3) |                    | j (cid:4) 1                    | ij          |         |                              |
| h       | (cid:2) fundreturns,e   |                    |                                | (cid:2)     | (cid:2) |                              |
| ofthe   |                         |                    | is conditional-mean-zeronoise: |             |         |                              |
| (35)    | E (cid:0) e h b r       | 0                  |                                |             |         |                              |
(cid:7)
|     | (cid:3) | (cid:1) (cid:2) (cid:4) |     |     |     |     |
| --- | ------- | ----------------------- | --- | --- | --- | --- |
Then any agent with increasing and concave von Neumann-Morgenstern prefer-
ences will just as happy choosing a portfolio of the k funds. as choosing from
the entire market. More formally,for each monotone and concave u and for each
|     |     | q   | q   |     |     | h h |
| --- | --- | --- | --- | --- | --- | --- |
feasible portfolio with 1 1, there exists another portfolio with 1 such
(cid:7) (cid:7)
|        | (cid:1) h         | (cid:1) q    | (cid:2)   |     |     |     |
| ------ | ----------------- | ------------ | --------- | --- | --- | --- |
| thatEu | (cid:7) r (cid:2) | Eu (cid:7) r | (cid:2) . |     |     |     |
(cid:0)
| PROOF | Consideranyportfolioq |     |     | with1 q | 1.  | Then |
| ----- | --------------------- | --- | --- | ------- | --- | ---- |
(cid:7)
(cid:2)
|      | q       | q (cid:1) b     | e               |     |     |     |
| ---- | ------- | --------------- | --------------- | --- | --- | --- |
| (36) | r       | y r             |                 |     |     |     |
|      | (cid:7) | (cid:7) (cid:7) | (cid:3) (cid:2) |     |     |     |
(cid:2)
|     |     | q b y r | q e |     |     |     |
| --- | --- | ------- | --- | --- | --- | --- |
(cid:7) (cid:7) (cid:7)
|     | (cid:2) | (cid:3) |     |     |     |     |
| --- | ------- | ------- | --- | --- | --- | --- |
But yb q is a valid portfolio because 1 yb q 1 b q 1 q 1. And, the second
|     | (cid:7) |     |     | (cid:7) | (cid:7) | (cid:7) (cid:7) (cid:7) |
| --- | ------- | --- | --- | ------- | ------- | ----------------------- |
|     |         |     |     |         | (cid:2) | (cid:2) (cid:2)         |
termisconditional-mean-zeronoise. Therefore,byLemma1allagentswithcon-
cavepreferenceswouldbeatleastashappytoswitchfromq totheportfolioyb q
,
(cid:7)
|         |                 |     | funds(withweightsb |     |     | q   |
| ------- | --------------- | --- | ------------------ | --- | --- | --- |
| whichis | aportfolioofthe |     | k                  |     |     | ).  |
(cid:7)
Inthecaseof1-and2-fundseparatingdistributions,thecharacterizationisneces-
saryaswellassufficient(seeRoss[1978a]).
In the CAPM derived using multivariate normality, it is easy to show that the
SML implies that each mean-variance inefficient portfolio has a payoff equal to
the payoff of the efficient portfolio with the same mean plus conditional-mean-
zero noise. Given that the mean-variance frontier is spanned by two portfolios,
weseethattheCAPMwithmultivariatenormalityisindeedintheclassof2-fund
separatingdistributions.
36

6 Arbitrage Pricing Theory (APT)
The Arbitrage Pricing Theory, which was introduced in Ross [1976a] and Ross
[1976c], is a model of security pricing that generalizes the pricing relation in the
CAPM and also builds on the intuition of the separating distributions. First, we
startwithafactormodel ofreturnsofthe sortstudiedinstatistics:
r
(cid:2)
µ
(cid:3)
fb
(cid:3)
e
(cid:3)
(37)
whereµisavectorofmeanreturns(unrestrictedatthemomentbuttoberestricted
by the theory), f is a vector of factor returns, of dimensionality much less than
r, b is a matrix of factor loadings, and e is a vector of uncorrelated idiosyncratic
noise terms. We can represent the restriction to the factor model by writing the
covariancematrixas
var (cid:1) r
(cid:2)
(cid:2)
bb
(cid:7) (cid:3)
(38) D
where we have assumed an orthonormal set of factors with the identity matrix as
covariancematrix (withoutlossof generality because wecan alwayswork witha
linear transformation), and where D is a diagonal matrix which is the covariance
matrix of the vector of security-specific noise terms e . The factor model is a
useful restriction for empirical work on security returns: given that typically we
have many securities for the number of time periods, the full covariance matrix
is not identified but a sufficiently low dimensional factor model has many fewer
parametersandcanbeestimated.
Oneintuitionofthe APT isthat idiosyncraticrisk isnot veryimportanteconomi-
callyandshouldnotbepriced. AnotherintuitionoftheAPTisthatcompensation
for risk should be linear or else there will be arbitrage. For example, if there is a
single factor and two assets have different exposures to the factor (betas), excess
return must be proportional to the risk exposure. Suppose the compensation per
unit risk is larger for the asset with a larger risk exposure. Then a portfolio mix-
ture of the riskfree asset and the high-risk asset will have the same risk exposure
as the low-risk asset but a higher expected return, and combining a long position
in the mixture with a short position in the low-risk asset givesa pure profit. This
37

profit will be riskless in the absence of idiosyncratic risk; it will be profitable for
some agents if idiosyncraticrisk is diversifiable. Conversely,if the compensation
perunitriskislargerfortheassetwiththelowerriskexposure,theotherassetcan
be dominated by a combination of a long position in the less risky asset with a
short(borrowing)positioninthe riskfreeasset.
ThemainconsequenceoftheAPTisapricingequationthatlookslikeamultifac-
torversionofthe CAPMequation:
µ
(cid:2)
r 1
f (cid:3)
Gb
(cid:4)
(39)
Here, r is the riskfree rate and G is the vector of factor risk premia. There are
f
severalapproachestomotivatingthisAPTpricingequation;seeforexampleRoss
[1976a,1976c],Dybvig[1983],orGrinblattandTitman[1983].
The APT shares important features of the CAPM: the value of diversification,
compensation for taking on systematic risk, and no compensation for taking on
idiosyncratic risk. The main difference is that there may be multiple factors, and
that the priced factors are the common factors that appear in many securities and
notnecessarilyjustthe marketfactor.
7 Conclusion
On reflection it is surprising that even our simplest context of a single-period
neoclassical model of investments has such a rich theoretical development. We
have hit on many of the highlights but even so we cannot claim to an exhaustive
reviewofallthat isknown.
References
Abel, Andrew B., 1990, “Asset Prices under Habit Formation and Catching up
withtheJoneses,”AmericanEconomicReview80,38–42.
38

Arrow, K. J., 1964, “The Role of Securities in the Optimal Allocation of Risk-
bearing,”Reviewof EconomicStudies31,91–96.
Arrow, K. J., 1965, Aspects of the Theory of Risk-Bearing (Yrjo Jahnsson Lec-
tures),Helsinki: Yrjo¨ JahnssoninSa¨a¨tio¨, 1965.
Arrow, Kenneth, and Gerard Debreu, 1954, “Existence of an Equilibrium for a
CompetitiveEconomy,”Econometrica22,265–290.
Arrow,Kenneth,andFrankHahn,1971,GeneralCompetitiveAnalysis,SanFran-
cisco: Holden-Day.
Banz, R. W., and M. H. Miller, 1978, “Prices for state-contingent claims: some
estimatesandapplications,”Journalof Business51,653–72.
Bergman, Yaacov, 1985, “Time Preference and Capital Asset Pricing Models,”
Journalof FinancialEconomics14,145–159.
Bewley,Truman,1988,“KnightianUncertainty,”NancySchwartzLecture,Evanston:
NorthwesternMEDS.
Blume, Brandenburger, and Dekel, “Lexicographic Probabilities and Choice un-
derUncertainty,”Econometrica59,61–79.
Breeden, Douglas T., “An Intertemporal Asset Pricing Model with Stochastic
Consumption and Investment Opportunities,” Journal of Financial Economics 7,
265–296.
Breeden, Douglas T., and Robert H. Litzenberger, “Prices of State-contingent
ClaimsImplicitin OptionPrices,”Journalof Business51,621–651.
Cass, David, and Joseph E. Stiglitz, 1970, “The Structure of Investor Preferences
and Separability in Portfolio Allocation: A Contribution to the Pure Theory of
MutualFunds,”JournalofEconomoicTheory2,122–160.
Cass, David, and Joseph E. Stiglitz, 1972, “Risk Aversion and Wealth Effects on
PortfolioswithManyAssets,”Reviewof EconomicStudies39,331–354.
39

Chamberlain, Gary, 1983, “A Characterization of the Distributions that imply
Mean-VarianceUtilityFunctions,”JournalofEconomicTheory 29,185–201.
Constantinides,George,1991,“HabitFormation: AResolutionoftheEquityPre-
miumPuzzle,” Journalof PoliticalEconomy98,519–543.
Cox, John C., Stephen A. Ross, and Mark Rubinstein, 1979, “Option pricing: a
simplifiedapproach,”JournalofFinancialEconomics7,229–263.
Cox, John C., and Stephen A. Ross, 1975, “A Survey of Some New Results in
FinancialOptionPricingTheory,”JournalofFinance31,383–402.
Debreu,Gerard,1959,TheoryofValue: AnAxiomaticAnalysisofEconomicEqui-
librium,NewHaven: YaleUniversityPress.
Duesenberry,J. S.,1949,Income,Saving,and theTheory ofConsumerBehavior,
Cambridge,Mass.: HarvardUniversityPress.
Dybvig, Philip H., 1983, “An Explicit Bound on Individual Assets’ Deviations
fromAPTPricinginaFiniteEconomy,”JournalofFinancialEconomics12,483–
496.
Dybvig, Philip H., 1988a, “Distributional Analysis of Portfolio Choice,” Journal
ofBusiness61,369–393.
Dybvig, Philip H., 1988b, “Inefficient Dynamic Portfolio Strategies, or How to
ThrowAwayaMillion Dollarsin the StockMarket,”Reviewof FinancialStudies
1,67–88.
Dybvig, Philip H., 1995, “Duesenberry’s Ratcheting of Consumption: Optimal
DynamicConsumptionandInvestmentGivenIntoleranceforanyDeclineinStan-
dardofLiving,”ReviewofEconomicStudies62,287–313.
Dybvig,PhilipH.,andStephenA.Ross,1985,“DifferentialInformationandPer-
formance Measurement Using a Security Market Line,” Journal of Finance 40,
383–399.
Dybvig,PhilipH.,andStephenA.Ross,1987,“Arbitrage,”inTheNewPalgrave:
40

a Dictionaryof Economics,London: Macmillan.
Epstein, Larry G., and Stanley E. Zin, 1989, “Substitution, Risk Aversion, and
theTemporalBehaviorofConsumptionandAssetReturns: ATheoreticalFrame-
work,”Econometrica57,937–969.
Fishburn, Peter, 1988, Nonlinear Preference and Utility Theory, Baltimore: John
Hopkins.
Gibbons, Michael R., Stephen A. Ross, and Jay Shanken, 1989, “A Test of the
EfficiencyofaGivenPortfolio,”Econometrica57,1121–1152.
Grinblatt, Mark, and Sheridan Titman, 1983, “Factor Pricing in a Finite Econ-
omy,”JournalofFinancialEconomics12,497–507.
Hadar, Josef, and William R. Russell, 1969, “Rules for Ordering Uncertain
Prospects,”AmericanEconomicReview59,25–34.
Hakansson,NilsH.,1969,“RiskDispositionandtheSeparationPropertyinPort-
folioSelection,”Journalof Financialand QuantitativeAnalysis4,401–416.
Harrison,J. M. andKreps,D. M., 1979,Martingalesandarbitrage in multiperiod
securitiesmarkets,JournalofEconomicTheory20,381–408.
Harrison, J. M. and S. Pliska, 1981, “Martingales and Stochastic Integrals in the
Theory of Continuous Trading,” Stochastic Processesand Their Applications 11,
215–260.
Hart, Oliver D., 1975, “Some Negative Results on the Existence of Comparative
Statics Results in Portfolio Theory,” The Review of Economic Studies 42, 615–
621.
Herstein, I. N., and John Milnor, 1953, “An Axiomatic Approach to Measurable
Utility,”Econometrica21,291–297.
Hindy, Ayman, and Chi-fu Huang, 1992, “On Intertemporal Preferences for Un-
certain Consumption: A Continuous Time Approach,” Econometrica 60, 781–
801.
41

Jensen, Michael C., 1969, “Risk, The Pricing of Capital Assets, and The Evalua-
tionofInvestmentPortfolios,”Journalof Business42,167–247.
Jouini,Elyes,andHediKallal,2001,“EfficientTradingStrategiesinthePresence
ofMarketFrictions,”Reviewof FinancialStudies14,343–369.
Knight,Frank H.,1921,Risk,Uncertainty,andProfit,NewYork: HoughtonMif-
flin.
Kreps, David, andEvan Porteus, 1978, “Temporal Resolutionof Uncertainty and
DynamicChoiceTheory,”Econometrica46,185–200.
Lintner, John, 1965, “The Valuation of Risk Assets and the Selection of Risky
Investments in Stock Portfolios and Capital Budgets,” Review of Economics and
Statistics47,13–37.
Luce, R. Duncan, and Howard Raiffa, 1957, Games and Decisions, New York:
Wiley.
Machina, Mark J., 1982, “ ‘Expected Utility’ Analysis without the Independence
Axiom,”Econometrica50,277–324.
Markowitz,Harry,1952,“PortfolioSelection,”JournalofFinance7,77–91.
Markowitz, Harry, 1959, Portfolio Selection, Efficient Diversification of Invest-
ments,NewYork: Wiley.
Mayers, David, and Edward M. Rice, 1979, “Measuring Portfolio Performance
and the Empirical Content of Asset Pricing Models,” Journal of Financial Eco-
nomics7,3–28.
Merton,RobertC.,1971,“OptimalConsumptionandPortfolioRulesinaContinuous-
TimeModel,”JournalofEconomic Theory3,373–413.
Merton,RobertC.,1973,“AnIntertemporalCapitalAssetPricingModel,”Econo-
metrica41,867–887.
Pratt, John W., 1964, “Risk Aversion in the Small and the Large,” Econometrica
42

32,122–136.
Pratt, John W., 1976, “Risk Aversion in the Small and the Large (erratum),”
Econometrica55,420.
Sharpe,WilliamF.,1964,“CapitalAssetPrices: ATheoryofMarketEquilibrium
underConditionsofRisk,”JournalofFinance19,425–442.
Sharpe, William F., 1966, “Mutual Fund Performance,” Journal of Business 39,
119–138.
Tobin, James, 1958, “Liquidity Preference as Behavior TowardsRisk,” Reviewof
EconomicStudies25,65–86.
Ross, Stephen A.,1976a, “The Arbitrage Theoryof Capital Asset Pricing,” Jour-
nalofEconomic Theory13,341–60.
Ross, Stephen A., 1976b, “Options and Efficiency,” Quarterly Journal of Eco-
nomics90,75–89.
Ross, Stephen A., 1976c, “Return, Risk, and Arbitrage,” in Friend and Bicksler,
Eds.,Riskand ReturninFinance1,Cambridge,Mass.: Ballinger.
Ross, Stephen A., 1978a, “Mutual Fund Separation in Financial Theory—The
SeparatingDistributions,”JournalofEconomicTheory17,254–286.
Ross,StephenA.,1978b,“ASimpleApproachtotheValuationofRiskyStreams,”
Journalof Business51,453–475.
Rothschild, Michael, and Joseph E. Stiglitz, 1970, “Increasing Risk: I. A Defini-
tion,” Journalof Economic Theory 2, 225–243 (see also “Addendum to “Increas-
ingRisk: 1. ADefinition,”Journalof EconomicTheory5,306).
Rothschild, Michael, and Joseph E. Stiglitz, 1971, “Increasing Risk: II. Its Eco-
nomicConsequences,”Journalof EconomicTheory3,66–84.
Rubinstein, Mark, 1976, “The Valuation of Uncertain Income Streams and the
PricingofOptions,”BellJournalofEconomics7,407–425.
43

Samuelson, P. A., 1967, “General Proof that Diversification Pays,” Journal of
FinancialandQuantitativeAnalysis2,1–13.
Treynor, Jack, 1965, “How to Rate Management of Investment Funds,” Harvard
BusinessReview43,63–75.
44
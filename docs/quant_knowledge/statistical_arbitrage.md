Statistical
Arbitrage
| Algorithmic | Trading        | Insights     |
| ----------- | -------------- | ------------ |
|             | and Techniques |              |
| ANDREW      |                | POLE         |
|             | John Wiley     | & Sons, Inc. |

Statistical
Arbitrage

Founded in 1807, John Wiley & Sons is the oldest independent
publishing company in the United States. With offices in North
America, Europe, Australia, and Asia. Wiley is globally committed
to developing and marketing print and electronic products and
servicesforourcustomers’professionalandpersonalknowledgeand
understanding.
The Wiley Finance series contains books written specifically for
finance and investment professionals as well as sophisticated indi-
vidual investorsand theirfinancialadvisors. Booktopicsrange from
portfolio management to e-commerce, risk management, financial
engineering, valuation, and financial instrument analysis, as well as
much more.
For a list of available titles, visit our Web site at www.Wiley
Finance.com.

Statistical
Arbitrage
| Algorithmic | Trading        | Insights     |
| ----------- | -------------- | ------------ |
|             | and Techniques |              |
| ANDREW      |                | POLE         |
|             | John Wiley     | & Sons, Inc. |

Copyright(cid:1)c 2007byAndrewPole.Allrightsreserved.
PublishedbyJohnWiley&Sons,Inc.,Hoboken,NewJersey.
PublishedsimultaneouslyinCanada.
WileyBicentenniallogo:RichardJ.Pacifico.
Nopartofthispublicationmaybereproduced,storedinaretrievalsystem,ortransmittedin
anyformorbyanymeans,electronic,mechanical,photocopying,recording,scanning,or
otherwise,exceptaspermittedunderSection107or108ofthe1976UnitedStatesCopyright
Act,withouteitherthepriorwrittenpermissionofthePublisher,orauthorizationthrough
paymentoftheappropriateper-copyfeetotheCopyrightClearanceCenter,Inc.,222
RosewoodDrive,Danvers,MA01923,(978)750-8400,fax(978)750-4470,orontheWeb
atwww.copyright.com.RequeststothePublisherforpermissionshouldbeaddressedtothe
PermissionsDepartment,JohnWiley&Sons,Inc.,111RiverStreet,Hoboken,NJ07030,
(201)748-6011,fax(201)748-6008,oronlineathttp://www.wiley.com/go/permission.
LimitofLiability/DisclaimerofWarranty:Whilethepublisherandauthorhaveusedtheir
besteffortsinpreparingthisbook,theymakenorepresentationsorwarrantieswithrespectto
theaccuracyorcompletenessofthecontentsofthisbookandspecificallydisclaimanyimplied
warrantiesofmerchantabilityorfitnessforaparticularpurpose.Nowarrantymaybecreated
orextendedbysalesrepresentativesorwrittensalesmaterials.Theadviceandstrategies
containedhereinmaynotbesuitableforyoursituation.Youshouldconsultwitha
professionalwhereappropriate.Neitherthepublishernorauthorshallbeliableforanylossof
profitoranyothercommercialdamages,includingbutnotlimitedtospecial,incidental,
consequential,orotherdamages.
Forgeneralinformationonourotherproductsandservicesorfortechnicalsupport,please
contactourCustomerCareDepartmentwithintheUnitedStatesat(800)762-2974,outside
theUnitedStatesat(317)572-3993orfax(317)572-4002.
Wileyalsopublishesitsbooksinavarietyofelectronicformats.Somecontentthatappearsin
printmaynotbeavailableinelectronicbooks.FormoreinformationaboutWileyproducts,
visitourWebsiteatwww.wiley.com.
LibraryofCongressCataloging-in-PublicationData:
Pole,Andrew,1961–
Statisticalarbitrage:algorithmictradinginsightsandtechniques/
AndrewPole.
p.cm.—(Wileyfinanceseries)
Includesbibliographicalreferencesandindex.
ISBN978-0-470-13844-1(cloth)
1.Pairstrading.2.Arbitrage---Mathematicalmodels.3.Speculation-
-Mathematicalmodels. I.Title.
HG4661.P65 2007
332.64’5 — dc22
2007026257
ISBN978-0-470-13844-1
PrintedintheUnitedStatesofAmerica
10 9 8 7 6 5 4 3 2 1

To Eliza and Marina

Contents
Preface xiii
Foreword xix
Acknowledgments xxiii
CHAPTER1
MonteCarloorBust 1
Beginning 1
Whither?AndAllusions 4
CHAPTER2
StatisticalArbitrage 9
Introduction 9
NoiseModels 10
ReverseBets 11
MultipleBets 11
RuleCalibration 12
SpreadMarginsforTradeRules 16
PopcornProcess 18
IdentifyingPairs 20
RefiningPairSelection 21
EventAnalysis 22
CorrelationSearchintheTwenty-FirstCentury 26
PortfolioConfigurationandRiskControl 26
ExposuretoMarketFactors 29
MarketImpact 30
RiskControlUsingEventCorrelations 31
DynamicsandCalibration 32
EvolutionaryOperation:SingleParameterIllustration 34
vii

viii CONTENTS
CHAPTER3
StructuralModels 37
Introduction 37
FormalForecastFunctions 39
ExponentiallyWeightedMovingAverage 40
ClassicalTimeSeriesModels 47
AutoregressionandCointegration 47
DynamicLinearModel 49
VolatilityModeling 50
PatternFindingTechniques 51
FractalAnalysis 52
WhichReturn? 52
AFactorModel 53
FactorAnalysis 54
DefactoredReturns 55
PredictionModel 57
StochasticResonance 58
PracticalMatters 59
Doubling:ADeeperPerspective 61
FactorAnalysisPrimer 63
PredictionModelforDefactoredReturns 65
CHAPTER4
LawofReversion 67
Introduction 67
ModelandResult 68
The75percentRule 68
Proofofthe75percentRule 69
AnalyticProofofthe75percentRule 71
DiscreteCounter 73
Generalizations 73
InhomogeneousVariances 74
VolatilityBursts 75
NumericalIllustration 76
First-OrderSerialCorrelation 77
AnalyticProof 79
Examples 82
NonconstantDistributions 82
ApplicabilityoftheResult 84
ApplicationtoU.S.BondFutures 85

Contents ix
Summary 87
Appendix4.1:LookingSeveralDaysAhead 87
CHAPTER5
GaussIsNottheGodofReversion 91
Introduction 91
CamelsandDromedaries 92
DryRiverFlow 95
SomeBellsClang 98
CHAPTER6
InterstockVolatility 99
Introduction 99
TheoreticalExplanation 103
TheoryversusPractice 105
FinishtheTheory 105
FinishtheExamples 106
PrimeronMeasuringSpreadVolatility 108
CHAPTER7
QuantifyingReversionOpportunities 113
Introduction 113
ReversioninaStationaryRandomProcess 114
FrequencyofReversionaryMoves 117
AmountofReversion 118
MovementsfromQuantilesOtherThan
theMedian 135
NonstationaryProcesses:InhomogeneousVariance 136
SequentiallyStructuredVariances 136
SequentiallyUnstructuredVariances 137
SerialCorrelation 138
Appendix7.1:DetailsoftheLognormalCaseinExample6 139
CHAPTER8
NobelDifficulties 141
Introduction 141
EventRisk 142
WillNarrowingSpreadsGuaranteeProfits? 144
RiseofaNewRiskFactor 145

x CONTENTS
RedemptionTension 148
SuperchargedDestruction 150
TheStoryofRegulationFairDisclosure(FD) 150
CorrelationDuringLossEpisodes 151
CHAPTER9
TrinityTroubles 155
Introduction 155
Decimalization 156
EuropeanExperience 157
AdvocatingtheDevil 158
Stat.Arb.ArbedAway 159
Competition 160
InstitutionalInvestors 163
VolatilityIstheKey 163
InterestRatesandVolatility 165
TemporalConsiderations 166
TruthinFiction 174
ALitanyofBadBehavior 174
APerspectiveon2003 178
RealitiesofStructuralChange 179
Recap 180
CHAPTER10
AriseBlackBoxes 183
Introduction 183
ModelingExpectedTransactionVolumeandMarketImpact 185
DynamicUpdating 188
MoreBlackBoxes 189
MarketDeflation 189
CHAPTER11
StatisticalArbitrageRising 191
CatastropheProcess 194
CatastrophicForecasts 198
TrendChangeIdentification 200
UsingtheCuscoretoIdentifyaCatastrophe 202
IsItOver? 204
CatastropheTheoreticInterpretation 205
ImplicationsforRiskManagement 209

Contents xi
SignOff 211
Appendix11.1:UnderstandingtheCuscore 211
Bibliography 223
Index 225

Preface
T hesepagestellthestoryofstatisticalarbitrage.Itisbothahistory,
describingthefirstdaysofthestrategy’sgenesisatMorganStanley
in the 1980s through the performance challenging years of the early
twenty-first century, and an exegesis of how and why it works. The
presentation is from first principles and largely remains at the level
of a basic analytical framework. Nearly all temptation to compose
a technical treatise has been resisted with the goal of contributing a
workthatwillbereadilyaccessibletothelargerportionofinterested
readership.Isay‘‘nearlyall’’:Chapter7andtheappendixtoChapter
11 probably belong to the category of ‘‘temptation not resisted.’’
Muchofwhatisdonebymoresophisticatedpractitionersisdiscussed
in conceptual terms, with demonstrations restricted to models that
will be familiar to most readers. The notion of a pair trade—the
progenitor of statistical arbitrage—is employed to this didactic end
rather more broadly than actual trading utility admits. In adopting
this approach, one runs the risk of the work being dismissed as
a pairs trading manual; one’s experience, intent, and aspirations
for the text are more extensive, but the inevitability of the former
is anticipated. In practical trading terms, the simple, unelaborated
pair scheme is no longer very profitable, nonetheless it remains a
valuable tool for explication, retaining the capacity to demonstrate
insight, modeling, and analysis while not clouding matters through
complexity.Afteraquartercenturyinthemarketplace,forprofitable
schemes beyond paper understanding and illustration, one needs to
add some structural complexityand analytical subtlety.
One elaboration alluded to in the text is the assembling of a set
of similar pairs (without getting into much detail on what metrics
are used to gauge the degree of similarity), often designated as a
group.Modelingsuchgroupscanbedoneinseveralways,withsome
practitioners preferring to anchor a group on a notional archetype,
structuring forecasts in terms of deviation of tradable pairs from the
archetype; others create a formal implementation of the cohort as
xiii

xiv PREFACE
a gestalt or a synthetic instrument. Both of those approaches, and
others, can be formally analyzed as a hierarchical model, greatly
in vogue (and greatly productive of insight and application) in
mainstream statistical thinkingfor two decades; add to the standard
staticstructurethedynamicelementinatimeseriessettingandoneis
veryquicklybuildingananalyticalstructureofgreatersophistication
than routinely used as the didactic tool in this book. Nonetheless,
all such modeling developments rely on the insight and techniques
detailed herein.
Those readers with deeper knowledge of mathematical and sta-
tisticalsciencewill,hopefully,quicklyseewherethepresentationcan
be taken.
Maintaining focus on the structurally simple pair scheme invites
readers to treat this book as an explicit ‘‘how to’’ manual. From
this perspective, one may learn a reasonable history of the what
and the how and a decent knowledge of why it is possible. Con-
temporary successful execution will require from the reader some
additional thought and directed exploration as foregoing remarks
have indicated. For that task, the book serves as a map showing
major features and indicating where the reader must get out a com-
passandnotebook.Theoldcartographers’device‘‘Herebedragons’’
might be usefullyremembered when you venturethus.
Thetexthas,unashamedly,astatistician’sviewpoint:Modelscan
be useful. Maintaining a model’s utility is one theme of the book.
The statistician’s preoccupation with understanding variation—the
appreciation of the knowledge that one’s models are wrong, though
useful, and that the nature of the wrongness is illuminated by the
structure of ‘‘errors’’ (discrepancies between observations and what
a model predicts) is another theme of the book. Or, rather, not a
distincttheme, but an overriding,guidingcontextfor thematerial.
The notion of a pair trade is introduced in Chapter 1 and
elaborated upon in Chapter 2. Following explication and exemplifi-
cation,twosimpletheoreticalmodelsfortheunderlyingphenomenon
exploited by pairs, reversion, are proposed. These models are used
throughoutthetexttostudywhatispossible,illuminatehowthepos-
sibilities might be exploited, consider what kinds of change would
have negative impact on exploitation, and characterize the nature
of the impact. Approaches for selecting a universe of instruments
for modeling and trading are described. Consideration of change is

Preface xv
introducedfromthisfirsttoedippingintoanalysis,becausetemporal
dynamics underpin the entirety of the project. Without the dynamic
thereis no arbitrage.
In Chapter 3 we increase the depth and breadth of the analysis,
expanding the modeling scope from simple observational rules1 for
pairstoformalstatisticalmodelsformoregeneralportfolios.Several
popular models for time series are described but detailed focus is on
weighted moving averages at one extreme of complexity and factor
analysis at another, these extremes serving to carry the message as
clearly as we can make it. Pair spreads are referred to throughout
thetextserving,asalreadynoted,asthesimplestpracticalillustrator
of the notions discussed. Where necessary to make our urgencies
sensible, direct mention is made of other aspects of the arbitrageur’s
concern, including portfolio optimization and factor exposures. For
the most part though, incursions into multivariate territory are
avoided. Volatility modeling (and the fascinating idea of stochastic
resonance) are treated separately here and in Chapter 6; elsewhere
discussionissubsumed in that of themean forecast process.
Chapter 4 presents a probability theorem that illuminates the
prevalence of price moves amenable to exploitation by the simple
rules first applied in the late 1980s. The insight of this result guides
evaluation of exploitation strategies. Are results borne of brilliance
on the part of a modeler or would a high school graduate perform
similarly because the result is driven by structural dynamics, long
in the public domain, revealed by careful observation alone? Many
a claim of a ‘‘high’’ proportion of winning bets by a statistical
arbitrageur has more to do with the latter than any sophistication
of basic spread modeling or (importantly) risk management. When
markets are disrupted and the conditions underlying the theoretical
result are grossly violated, comparative practitioner performance
reveals much about basic understanding of the nature of the process
1Thereisnopejorativeintentintheuseoftheterm:Theruleswereeffective.Statistical
content waslimitedtomeasurement ofrangeofvariation;nodistributionalstudy,
modelformulation,estimation,erroranalysis,orforecastingwasundertakenprior
tomilkingtheobservationalinsight.Thoseactivitiescamesoonenough—afterthe
profitswerepilingup.Withtheexpandedstatisticalstudy,addingtradingexperience
tohistoricaldata,came insightintosubtletiesof thestockpricemotionsexploited
andthemarketforcesdrivingrepetitiousoccurrenceofopportunities.

xvi PREFACE
being exploited. Knowledge of the theoretical results often reveals
itselfmorewhenassumptionsareviolatedthanwhenthingsarehunky
dory and managers with solid understanding and those operating
intellectuallyblindgeneratepositivereturnsinequalmeasure.(Tony
O’Hagan suggested that the basic probability result is long known,
but I have been unable to trace it. Perhaps the result is too trivial
to be a named result and exists as a simple consequence, a textbook
exercise, of basic distribution theory. No matter, the implication
remains profoundlysignificantto thestatistical arbitrage story.)
Chapter 5 critiques a published article (whose authors remain
anonymousheretoprotecttheirembarrassment)toclarifythebroad
conditionsunderwhich thephenomenonof reversion occurs. A cen-
tralroleforthenormaldistributionisdismissed.Thetwinerroneous
claims that (a) a price series must exhibit a normal marginal distri-
bution for reversion to occur, and (b) a series exhibiting a normal
marginal distribution necessarily exhibits reversion are unceremo-
niously dispelled. There is reversion anywhere and everywhere, as
Chapter4 demonstrates.
Chapter 6 answers the question, important for quantifying the
magnitude of exploitable opportunities in reversion gambits, ‘‘How
much volatilityis therein a spread?’’
Chapter7isfortheenthusiastnoteasilydissuadedbythepresence
of the many hieroglyphs of the probability calculus. Anyone with
a good first course in probability theory can follow the arguments,
and most can manage the detailed derivations, too. The mechanics
arenotenormouslycomplicated.Someoftheconceptualdistinctions
may be challenging at first—read it twice! The effort will be repaid
as there is significant practical insight in the examples considered
at length. Knowledge of how close theoretical abstractions come
to reflecting measurable features of actual price series is invaluable
in assessing modeling possibilities and simulation or trading results.
Notwithstandingthatremark,itistruethattheremainderofthebook
does not rely on familiarity with the material in Chapter 7. While
youmaymisssomeofthesubtletyinthesubsequentdiscussions,you
will not lack understandingforomittingattentionto thischapter.
Chapters 8 through 10 might have been labeled ‘‘The Fall,’’ as
they characterize the problems that beset statistical arbitrage begin-
ning in 2000 and directly caused the catastrophic drop in return
during 2002–2004. An important lesson from this history is that
there was not a single condition or set of conditions that abruptly

Preface xvii
changed in 2000 and thereby eliminated forecast performance of
statistical arbitrage models. What a story that would be! Far more
dramaticthantheprosaicreality,whichisacomplexmixofmultiple
causes and timings. All the familiar one liners, including decimaliza-
tion, competition, and low volatility, had (and have) their moment,
butnoneindividually,northecombination,canhavedeliveredablow
to financial markets. Fundamentally altering the price dynamics of
markets in ways that drastically diminish the economic potential in
reversion schemes, mining value across the spectrum from the very
highfrequencyhareofintra-daytothevenerabletortoiseofamonth
ormore, requiresa moreprofoundexplanation.
Change upon change upon change cataloged in Chapter 9 is at
therootofthedearthofreturntostatisticalarbitragein2002–2004.
(Performance deterioration in 2000–2002 was evident but limited
to a subset of practitioners.) This unusual episode in recent U.S.
macroeconomic history is over, but the effects linger in the financial
markets reflecting emergent properties of the collective behavior of
millionsofinvestors;andsurelythoseinvestorscontinuetoembody,
no matter howlingering,thosechanges and the causes thereof.
The shift of trading from the floor of the New York Stock
Exchange to internal exchanges, in the guise of computer algo-
rithmsdesignedbylargebrokeragehousesandinvestmentbanks,has
cumulatively become a change with glacier-like implacability. Slow.
Massive. Irresistible. Crushing. Reforming.2 A frequently remarked
facet of the evolving dynamics is the decline of market volatility.
Where has market volatility gone? In large part the algorithms have
eatenit.Reducethevoiceofasingleparticipantyellinginacrowdand
thebabelisunaffected.Quiteasignificantproportionofparticipants
and the reduced babel is oddly deafening. Now that computer pro-
grams (Chapter 10) ‘‘manage’’ over 60 percent of U.S. equity trades
among‘‘themselves’’theextraodinaryresultisakintoadministering
a dose of ritalin to the hyperactive market child. In the commentary
onlowvolatilitytwothemesstandout:oneisalamentoverthelack
2Onemajorstructuralconsequence,fedalsobytechnicaladvanceinthecreditmar-
ketsandthedevelopmentofExchangeTradedFunds,isliterallytheforminganew
of patterns of price behaviordetemined by the interactionof computer algorithms
asagentsforsharedealings.Inadditiontothisre-forming,reformissimultaneously
underwaywithchangestoSecuritiesExchangeCommissionregulationsandNYSE
rules.

xviii PREFACE
of Keynes’ animal spirits, a concern that the entrepreneurial genius
of America is subdued even as Asian giants are stirring; the other is
a fear that investors have forgotten the risks inherent in investment
decisions, that inadvisable decisions are therefore being made that
willhavenegativeconsequencesinthenearfuture.Theinconsistency
in those two characterizations is stark, but it can be rationalized.
Contrary to the first notion, the spirit is quite animated—with a
billionandahalfshareschangingownershipdailyontheNYSEmart
alone, what other conclusion should one draw? There is plenty of
spirit: simply its animus is satisfied with less overt fuss. Algorithms
don’t have emotions. So there is plenty of innovative risk taking,
but low volatility by historical standards, induced by trading tech-
nologies, has not yet been properly internalized by many market
participants.Viewingcontemporaryvolatilitylevelsinthemannerto
whichhistoricalexperiencehasbeenaccustomedineluctablyleadsto
excessive risk taking.
Chapter 10 is interesting in its own right, notwithstanding any
relationship to the evolution of statistical arbitrage opportunities.
Algorithms and computer driven trading are changing the financial
world in many ways. Electronic exchanges have already been seen
off most of the world’s peopled trading places—and who among us
believes that the floor of the NYSE will be more than a museum,
parkinglot, ormemory in a year ortwo?
Chapter 11 describes the phoenix of statistical arbitrage, rising
outoftheashesofthefirecreatedandsustainedbythetechnological
developments in algorithmic trading. New, sustained patterns of
stock price dynamics are emerging. The story of statistical arbitrage
has returnedto a newbeginning.Will this fledglingfly?
The renaissance predicted in Chapter 11, drafted in 2005, is
already coming to pass. Since at least early 2006 there has been a
resurgence of performance from those practitioners who persisted
through the extremely challenging dynamic changes of 2003–2005.
Interestingly, while there are new systematic patterns in the move-
ments of relative equity prices, some old patterns have also regained
potency. Adoption of algorithmic trading is accelerating, with tools
now offered by more than 20 vendors. In another technology driven
development, beginning with Goldman Sachs in late 2006, at least
twoofferingsofgeneralhedgefundreplicationbyalgorithmicmeans
have been brought to market. This is an exciting as well as exacting
time forstatistical arbitrageurs.

Foreword
Mean reversion in prices, as in much of human activity, is a
powerful and fundamental force, driving systems and markets
to homeostatic relationships. Starting in the early 1980s, statistical
arbitragewasaformalandsuccessfulattempttomodelthisbehavior
in the pursuit of profit. Understanding the arithmetic of statistical
arbitrage (sometimes abbreviated as stat. arb.) is a cornerstone to
understanding the development of what has come to be known as
complexfinancial engineeringand risk modeling.
Thetradingstrategyreferredtoasstatisticalarbitrageisgenerally
regarded as an opaque investment discipline. The view is that it is
being driven by two complementary forces, both deriving from the
core nature of the discipline: the vagueness of practitioners and the
lack of quantitative knowledge on the part of investors. Statistical
arbitrage exploits mathematical models to generate returns from
systematic movements in securities prices. Granted, no investment
managerisinclinedtodivulgetheintricate‘‘how-tos’’ofhisbusiness.
Whilestock pickers can tell a good storywithoutrevealing theheart
of their decision making, that is not the case with model-based
strategiesdevelopedby‘‘quants.’’Adescriptionwithanymeaningful
detail at all quickly points to a series of experiments from which an
alert listener can try to reverse-engineer the strategy. That is why
quant practitioners talk in generalities that are only understandable
by themathematically trained.
Opacity has also increased the need for mathematical maturity
on the part of investors seeking to assess managers. To comprehend
what a statistical arbitrageur is saying beyonda glib level, oneneeds
to understand advanced mathematics beyond the college level. This,
naturally, limits the audience. The limitation is perpetuated by the
lack of reference material from which to learn. Statistical Arbitrage
nowfillsthat void.
Statistical arbitrage has been in existence for approximately 25
years. During that time, the general concepts have been widely
xix

xx FOREWORD
disseminated via the storytelling of early implementers to interested
investment bank analysts and academics. Nevertheless, opacity
remains because practitioners have steadily increased the sophistica-
tion of their modeling—and for good commercial reasons remained
obscure about their innovations. In the wide dissemination of basic
stat. arb. concepts, the term mean reversion as well as its variant,
reversion to the mean, looms very large. Reversion to the mean is a
simpleconcepttoillustrate:Childrenofunusuallytallparentsaretyp-
ically shorter than their parents; children of unusually short parents
aretypicallytallerthantheirparents.Thisisaconceptthatiseasyfor
mostpeopletograsp.Translatingthisideatothemotionsofsecurity
prices means that securities prices return to an average value. So far,
so good. But then we hit a problem. Height reversion is an intergen-
erational phenomenon,whilepricereversion isan entitydynamic.
Prices returning from where? And to what average value? The
average height of adults is a familiar concept, even if the precise
quantification requires a little work. Even children as young as
grade-schoolagecangiveareasonableestimateoftheaverageheight
of the adults they know, and by extension, of the average height
of local adult populations. There is no such common grounding of
observation or experience to apply to securities prices. They are all
over the map. Scaling is arbitrary. They can grow many fold. And
they can collapse to zero. People do not grow to the sky and then
revert back to someaverage, but security pricescan.
Even if we suppose that the questions have been reasonably
answered, other technicalities immediately pose themselves: How
does one identify when a price is away from the mean and by how
much?How longwill thereturn to the mean take?
Here is where the opacity enters the discussion and makes its
permanenthome.Thelanguageofmathematical modelscompounds
theunfamiliarityofthenotions,generatingasenseofdisquiet,afear
of lack of understanding.
InStatisticalArbitrage,Polehasgivenhisaudienceadidactictour
of the basic principles of statistical arbitrage, eliminating opacity at
the Statistical Arbitrage 101 level. In the 1980s and early 1990s,
Stat. Arb. 101 was, for the most part, all there was (exceptions such
as D.E. Shaw and Renaissance aside). Today, more than a decade
later,thereisamuchmoreextensiveandcomplexworldofstatistical
arbitrage.

Foreword xxi
This is not unlike the natural world, which is now populated
by incredibly complex biological organisms after four billion years
of evolution. Yet the simplest organisms thrive everywhere and still
makeupbyfarthelargestpartoftheplanet’sbiomass.Soisittruein
statisticalarbitrage,wherethebasicsunderpinmuchofcontemporary
practice.
Statistical Arbitrage describes the phenomena, the driving forces
generating those phenomena, the patterns of dynamic development
ofexploitableopportunities,andmodelsforexploitationofthebasic
reversion to the mean in securities prices. It also offers a good deal
more, from hints at more sophisticated models to valuable practi-
cal advice on model building and performance monitoring—advice
applicablefar beyondstatistical arbitrage.
Chapters 1 and 2 speak to the genesis of statistical arbitrage, the
venerable pairs trading schemes of the 1980s, with startling illustra-
tion of the enormous extent and productivity of the opportunities.
This demonstration sets the scene for theoretical development, pro-
vidingthefirststeptocriticalunderstandingofpracticalexploitation
withrulesforcalibratingtradeplacement.Morepenetrationofopac-
ityfollowsinChapter5wheretherelationshipbetween(a)reversion
insecuritiespriceswatchedday-by-dayand(b)statisticaldescriptions
(distributions) of collections of such daily prices viewed as a glob
devoid of theday-by-day context,isclearly spelledout.
Chapters 8 and 9 tell of the midlife crisis of statistical arbitrage.
The roiling of United States financial markets for many months,
beginning with the Enron debacle in 2000 and running through
the terrorist attacks of 2001 and what Pole calls ‘‘an appalling
litany’’ of corporate misconduct, is dissected for anticipated impact
on statistical arbitrage performance. Adding to that mix have been
technical changes in the markets, including decimalization and the
decline of independent specialists on the floor of the NYSE. Pole
draws a clear picture of why statistical arbitrage performance was
disrupted. Very clearly the impression is made that the disruption
was not terminal.
Chapters 10 and 11 speak to the arriving future of statistical
arbitrage.Tradingalgorithms,atfirstdestroyersofclassicalstat.arb.
are now, Pole argues, progenitors of new, systematically exploitable
opportunities. He labels one of the new motions the ‘‘catastrophe
move’’; a detailed exposition of modeling the dynamics follows a

xxii FOREWORD
catastrophe-theory explication of a possible rationale for the behav-
ioralpattern.Theunmistakableimpressionisthatstatisticalarbitrage
is risingonceagain.
The tone of Statistical Arbitrage is direct and thorough. Obfus-
cationis inshortsupply.Occasionally,thetoneis relievedwith abit
of lightheartedness—the tadpole-naming story in a note to Chapter
11 is a gem—and throughout,refreshingproseis to befound.
In describing mathematical models, authors readily produce
unmemorable, formulaic wording offering nothing by way of inter-
pretation or explanation beyond what is provided by the algebra
itself. Statistical Arbitrage is an exception—a break in the cloud of
opacity—a mean that Polehas avoided reverting to!
Gregory van Kipnis
April 23, 2007
New York City

Acknowledgments
Iwas
|     | introduced | to  | statistical |     | arbitrage | by  | Gregg | van Kipnis. | In  |
| --- | ---------- | --- | ----------- | --- | --------- | --- | ----- | ----------- | --- |
manyways,thecontentsofthisvolumearedirectlytheresultofour
collaborationanditisapleasuretoacknowledgetheintellectualdebt.
| Our                      | conversations       |           | often        | strayed    | far          | beyond                   | statistical | arbitrage       | to    |
| ------------------------ | ------------------- | --------- | ------------ | ---------- | ------------ | ------------------------ | ----------- | --------------- | ----- |
| macroeconomicsandgeneral |                     |           |              | scienceand |              | veryoftentopolitics,none |             |                 |       |
| of                       | which is reproduced |           | here         | in         | recognizable | form.                    | Those       | discussions     |       |
| were                     | not always          | motivated |              | by         | statistical  | arbitrage                |             | considerations, |       |
| though                   | occasionally        |           | we           | would      | hit on       | a useful                 | metaphor    | from            | an    |
| unrelated                | topic               | that      | subsequently |            | proved       | fruitful                 | in          | thinking        | about |
| statistical              | arbitrage.          |           | It is        | not in     | the nature   | of                       | things      | that individual |       |
suchrecollectionscannowbepointedtowithcertaintytosaywhose
ideaABCwas.CreditisrightfullyduetovanKipnis;therenditionin
| thesepages | isentirelymy  |     |            | responsibility. |       |           |     |            |      |
| ---------- | ------------- | --- | ---------- | --------------- | ----- | --------- | --- | ---------- | ---- |
|            | The editorial | and | production |                 | staff | at Wiley, | in  | particular | Bill |
Falloon,EmilieHerman,LauraWalsh,andStaceyFischkeltathough
weneverphysicallymet,havebeenhelpfulandcourteousthroughout
theproject.
xxiii

1
CHAPTER
Monte Carlo or Bust
Wemust always be ready to learn fromrepeatable
occurrenceshoweverodd theymay lookat first sight.
—Box onQuality and Design, G.E.P.Box
1.1 BEGINNING
In 1985 a small group of quantitatively trained researchers under
thetutelageofNunzioTartaglia1 createdaprogramtobuyandsell
stocks in pair combinations. Morgan Stanley’s Black Box was born
and quickly earned a reputation and a lot of money. A fifteen-year
rise to heroic status for statistical arbitrage (a term uncoined at that
time) was begun.
Details of the Black Box were guarded but soon rumor revealed
thebasictenetsandthename‘‘pairstrading’’appearedinthefinancial
lexicon. The premise of pairs trading was blindingly simple: Find a
pair of stocks that exhibit similar historical price behavior. When
the prices of the stocks diverge, bet on subsequent convergence.
Blindingly,beautifullysimple.And hugelyprofitable.
1In The Best of Wilmott, Paul Wilmott states that the MS pairs trading program
was initiated by Gerry Bamberger in 1982/1983, that Bamberger departed MS in
1985forPrincetonNewportPartnersandretiredin1987.Weareunabletoconfirm
whetherBamberger’sMSprogramwasdistinctfromTartaglia’s;othershaveclaimed
a group effort and complain that it is unfair to annoint either group head as ‘‘the
inventor.’’
Interestingly Wilmott claims that pairs trading was discovered at his firm as
earlyas1980.
1

2 STATISTICALARBITRAGE
40 CAL daily adjusted close price
$ AMR daily adjusted close price
35
30
25
20 B
A
15
10
5
0
Q1 Q2 Q3 Q4 Q1 Q2 Q3 Q4 Q1 Q2 Q3
2002 2003 2004
FIGURE 1.1 Dailyclosingprices,CALandAMR(2002–2004)
Where did Tartaglia get his insight? As with many stories of
invention,necessitywas themotivatingforce.Charteredbymanage-
ment to find a way to hedge the risks routinely incurred through
its lucrative activities with block trading, Tartaglia’s mathematical
training conjured up the notion of selling (short) a stock that exhib-
ited similar trading behavior to the stock being managed by the
block desk. Immediately the notion was invented, the more general
applicationofpairstradingwasinnovated.Veryshortly,anewprofit
center was addingto thebottomline.
Figure 1.1 shows the daily close price of two airline stocks,
Continental Airlines (CAL) and American Airlines (AMR). Notice
how the spread between the two price traces opens and closes. The
pairs trading scheme veritably yells at one: Buy the lower-priced
stock and short the higher-priced stock when the spread is ‘‘wide’’
(A), and reverse out thosepositionswhen thespread closes (B).
In 1985 computers were not familiar appliances in homes, and
daily stock price feeds were the tools of professionals alone. Sheer
numbercrunchingpower,crucialtoseriousimplementationofapairs

MonteCarloorBust 3
trading business, required tens of thousands of dollars of hardware.
Pairs trading, so beautifully simple in concept and for years now in
practice, was born in an era in which investment housesalone could
realistically research and deployit.
Many stories from the era infect the industry, mythologizing the
business and the practitioners. Two such stories that have genuine
substance and that have continued significance today are the SEC’s
useofalgorithmstodetectaberrantpricepatterns,andtheevolution
of specialist reaction to the contrarian traders from initial suspicion
to eventual embrace.
The SEC was intrigued no less than others by the aura around
theMorganStanleyblackbox.Uponlearningabouthowthemodels
workedtopredictcertainstockpricemotions,itwasquicklyrealized
howthetechnologycouldbeemployedtoflagsomekindsofunusual
and potentially illegal price movement, long before neural network
technologywas employedin thisrole.
In the late 1980s the NYSE was populated with over 50 inde-
pendent specialists. Largely family businesses with limited capital,
they were highly suspicious when the group at Morgan Stanley
began systematically sending orders to ‘‘buy weakness’’ and ‘‘sell
strength.’’ The greatest concern was that the big house was attempt-
ing to game the little specialist. Suspicion gradually evolved into
cozy comfort as the pattern of trading a stock was revealed. Even-
tually, comfort became full embrace such that when the specialist
sawMorganStanleyaccumulatingaweakstock,thespecialistwould
jump on the bandwagon ‘‘knowing’’ that the stock’s price was set
to rise.
Theearlyyearswereenormouslylucrative.Successsoonspawned
independent practitioners including D.E. Shaw and Double Alpha,
both created by former acolytes of Tartaglia. In subsequent years
other groups created pairs trading businesses, the founders of which
can be traced either to the original group at Morgan Stanley or to
second-generationshopssuchas Shaw. Asthepracticebecamemore
widely known, academic interest was piqued; published articles by
NBER, among others, made the general precept known to a wide
audience and with the rapid increase in power of low cost personal
computers,thepotentialpractitionerbaseexploded.Veryquickly,so
did theactual practitionerbase.

4 STATISTICALARBITRAGE
1.2 WHITHER? AND ALLUSIONS
Two decades later, the matured adult statistical arbitrage that grew
up from the pair trading infant faces a cataclysmic environmental
change. Returns have greatly diminished. Managers are beset by
difficulties and are adapting strategies to cope. The financial market
environment of the new century poses survival challenges one might
liken to those faced by earthly fauna millenia ago when the last
ice age dawned. The quick and adaptable survived. The slow and
morphologicallyfixedfroze or starved.
Statistical arbitrage’s ice age dawned in 2000 and entered full
‘‘frigidia’’ in 2004. Observers proclaimed the investment discipline’s
demise,investorswithdrewfunds,andpractitionersclosedshop.The
rout was comprehensive. A pall of defeat enveloped discussion of
thebusiness.
This judgment of a terminal moment for statistical arbitrage is
premature, I believe. Despite the problems for traditional statistical
arbitrage models presented by market structural changes, which are
documented and examined in later chapters, there are indications
of new opportunities. New patterns of stock price behavior are
occurring on at least two high-frequency timescales. Driving forces
areidentifiableintheinterplayofelectronictradingentities,therising
futureof stock tradingin theUnited States.
Theappearanceofthenewopportunities,admittedlyonlyroughly
characterizedatthistime,suggestssignificanteconomicexploitability,
andtheymaybeenoughtostaveoffthefateofextinctionforstatistical
arbitrage.Thecromagnonmanofclassicreversionplayswillbesuper-
sededbythehomosapiensof....Thatremainstobeseenbutoutlines
aredrawninChapter11.
I considered titling the book, The Rise and Fall and Rise? of
Statistical Arbitrage, reflecting the history and the possibilities now
emerging. The pattern is explicit in the preceding paragraphs of this
chapterandinthestructureofthebook,whichiswrittenalmostinthe
formofanannotatedhistory.Tothosereaderswhoseinterestisborne
of the question, ‘‘What are the prospects for statistical arbitrage?’’,
the historical setting and theoretical development in Chapters 1
through 7 may seem anachronistic, unworthy of attention. It might
be likened to suggesting to a student of applied mathematics that
the study of Copernicus’ system for the motions of astronomical

MonteCarloorBust 5
bodies is presently utilitarian. I maintain that there is value in the
historicalstudy(forthemathematician,too,butthatistakinganalogy
much further than it deserves). Knowing what worked previously in
statistical arbitrage, and how and why it did, provides the necessary
foundation for understanding why market structural changes have
negatively impacted thestrategy class. Knowingwhich changes have
had an effect and how those effects were realized illuminates what
might be anticipatedin thepresently congealingenvironment.
Interpreting the present in the context of the past is hardly a
novel notion. It is a sound bedrock of scientific investigation. Most
people are familiar with the admonition of political philosophers
that those who do not study the past are doomed to repeat its
mistakes.2 But that is not our reference point. While undoubtedly
somearbitrageurshavemadetheirindividualerrors,therecannotbe
a verdict that the collective of practitioners has ‘‘made a mistake’’
that ought to be guarded against ever after. Our reference point is
thefarmorecompellingscientificviewof‘‘standingontheshoulders
of giants.’’ Bereft of value judgments, scientific theories, right or
wrong, and no matter how pygmy the contribution, are set forth
for scrutiny forever. The promise of the new opportunities may be
understood and evaluated in the context of how market changes
rendered valueless that which was formerlylucrative.
Let’s be quite clear. There is no claim to a place in history
with the work reported here despite allusions to historical scientific
genius. Neither is the area of study justifiably on the same shelf as
physics, chemistry, and mathematics. It sits more appropriatelywith
economics and sociology because the primal forces are people. We
may label an emergent process as ‘‘reversion’’ (in prices), describe
temporal patterns, posit mathematical equations to succinctly repre-
sent those patterns, and commit ourselves to actions—trading—on
2‘‘Progress, far from consisting in change, depends on retentiveness. When change
is absolute there remains no being to improve and no direction is set for possible
improvement: and when experience is not retained, as among savages, infancy is
perpetual. Those who cannot remember the past are condemned to repeat it. In
the first stage of life the mind is frivolous and easily distracted, it misses progress
by failingin consecutiveness and persistence. This is the condition of children and
barbarians, in which instinct has learned nothing from experience.’’ The Life of
Reason,GeorgeSantayana.

6 STATISTICALARBITRAGE
the output of the same, but the theory, models, and analysis are
of an emergent process, not the causal mechanism(s) proper. No
matter how impressibly we may describe routines and procedures
of the regular players, from analysts (writing their reports) to fund
advisors (reading those reports, recommending portfolio changes)
to fund managers (making portfolio decisions) to traders (acting on
those decisions), the modeling is necessarily once removed from the
elemental processes. In that complex universe of interactions, only
the result of which is modeled, lies the genesis of the business and
now, more fatefully, the rotting root of the fall. Astonishingly, that
rottingroot isfertilizingtheseeds of therise(?) to bedescribed.
Unlike the study of history or political philosophy, which is
necessarily imbued with personal interpretations that change with
the discovery of new artifacts or by doubt cast on the authenticity
of previously sacred documents, the study of statistical arbitrage
benefits from an unalterable, unequivocal, complete data history
that any scholar may access. The history of security prices is, like
Brahe’s celestial observations, fixed. While Brahe’s tabulations are
subject to the physical limitations of his time3 and uncertainties
inherent in current relativistic understanding of nature’s physical
reality, the history of security prices, being a human construct, is
knownprecisely.
In exhorting the quality of our data, remember that Brahe was
measuring the effects of physical reality on the cosmic scale for
whichscientifictheoriescanbeadducedanddeduced.Ournumbers,
recordsoffinancialtransactions,mightbedevoidoferrorbuttheyare
measurementsofbargainsstruckbetweenhumans.Whatunchanging
physicalrealitymightbeappealedtointhat?Wemightbuildmodels
of price changes but the science is softening as we do so. The
data never changes but neither will it be repeated. How does one
scientificallyvalidate a theoryunder thoseconditions?
3ThefirstAstronomerRoyal,JohnFlamsteed(1646–1719),systematicallymapped
the observable heavens from the newly established Royal Observatory at Green-
wich,compiling30,000individualobservations,eachrecordedandconfirmedover
40yearsofdedicatednightlyeffort.‘‘Thecompletedstarcataloguetripledthenum-
berofentriesintheskyatlasTycoBrahehadcompiledatUraniborginDenmark,and
improvedtheprecisionofthecensusbyseveralordersofmagnitude.’’InLongitude
byDavaSobel.

7
MonteCarloorBust
Thequestionsareunanswerablehere.Onecannotofferaphilos-
| ophy or    | sociology |            | of finance. |     | But one can     | strive    | for scientific | rigor       |
| ---------- | --------- | ---------- | ----------- | --- | --------------- | --------- | -------------- | ----------- |
| in data    | analysis, | hypothesis |             |     | positing, model |           | building, and  | testing.    |
| That rigor | is        | the basis  | of          | any | belief one      | can claim | for the        | validity of |
understandingandcoherentactionsinexploitingemergentproperties
| of componentsof |        | thefinancial |                |            | emporium.    |     |                   |        |
| --------------- | ------ | ------------ | -------------- | ---------- | ------------ | --- | ----------------- | ------ |
| This            | volume | presents     |                | a critical | analysis     | of  | what statistical  | arbi-  |
| trage is—a      |        | formal       | theoretical    |            | underpinning |     | for the existence | of     |
| opportunities   |        | and          | quantification |            | thereof,     | and | an explication    | of the |
enormousshiftsinthestructureoftheU.S.economyreflectedinfinan-
cialmarketswithspecificattentiononthedramaticconsequencesfor
| arbitrage | possibilities. |     |     |     |     |     |     |     |
| --------- | -------------- | --- | --- | --- | --- | --- | --- | --- |

2
CHAPTER
Statistical Arbitrage
Much of what happenscan convenientlybethoughtof as
randomvariation, but sometimeshiddenwithinthe
variation are important signalsthat couldwarn usof
problemsor alert usto opportunities.
—Box on Quality and Discovery, G.E.P.Box
2.1 INTRODUCTION
T hepairtradingschemewaselaboratedinseveraldirectionsbegin-
ning with research pursued in Tartaglia’s group. As the analysis
techniquesusedbecamemoresophisticatedandthemodelsdeployed
more technical, so the sobriquet by which the discipline became
known was elaborated. The term ‘‘statistical arbitrage’’ was first
used in theearly 1990s.
Statistical arbitrage approaches range from the vanilla pairs
trading scheme of old to sophisticated, dynamic, nonlinear models
employingtechniquesincludingneuralnetworks,wavelets,fractals—
just about any pattern matching technology from statistics, physics,
and mathematics has been tried, tested, and in a lot of cases,
abandoned.
Laterdevelopmentscombinedtradingexperience,furtherempir-
ical observation, experimental analysis, and theoretical insight from
engineering and physics (fields as diverse as high energy particle
physics to fluid dynamics and employing mathematical techniques
from probability theory to differential and difference equations).
With so much intellectual energy active in research, the label ‘‘pairs
9

10 STATISTICALARBITRAGE
trading’’ seemed inadequate. Too mundane. Dowdy, even. ‘‘Statisti-
calarbitrage’’wasinvented,curiously,despitethelackofstatisticians
or statistical contentof much of the work.
2.2 NOISE MODELS
The first rules divined for trading pairs were plain mathematical
expressionsofthedescriptionofthevisualappearanceofthespread.
For a spread like the CAL–AMR spread in Figure 2.1, which ranges
from −$2 to $6, a simple, effective rule is to enter the spread bet
when thespread is $4and unwindthe bet when it is $0.
We deliberately use the term rules rather than model because
thereisnoattemptatelaborationofaprocesstoexplaintheobserved
behavior, but simply a description of salient patterns. That is not
to diminish the validity of the rules but to characterize the early
work accurately. As the record shows, the rules were fantastically
profitableforseveral years.
8
$
6
4
2
0
−2
−4
Q1 Q2 Q3 Q4 Q1 Q2 Q3 Q4 Q1 Q2 Q3
2002 2003 2004
FIGURE 2.1 Dailyclosingspread,CAL–AMR

StatisticalArbitrage 11
Applying the $4–$0 rule to the CAL–AMR spread, there is
a single trade in the calendar years 2002 and 2003. If this looks
like money for practically no effort, that is the astonishing situa-
tion Tartaglia discovered in 1985—writ large across thousands of
stock pairs.
Alternatives, elaborations,and generalizationsjump offthe page
asonelooksatthespreadandconsidersthatfirst,seductivelysimple
rule. Two such elaborationsare:
■ Makethe reverse bet, too.
■ Makerepeated betsat staged entrypoints.
2.2.1 Reverse Bets
Why sit out the second half of 2002 while the spread is increasing
from its narrow point toward the identified entry point of $4? Why
not bet on that movement? In a variant of the commodity traders’
‘‘turtletrade,’’rule1wasquicklyreplacedwithrule2,whichreplaced
the exit condition, ‘‘unwind the bet when the spread is $0,’’ with a
reversal,‘‘reversethelongandshortpositions.’’Nowapositionwas
always held, waiting on the spread to increase from a low value or
to declinefroma high value.
With that expansion of trading opportunities came more trades
and greater profitsforno additionalwork.
2.2.2 Multiple Bets
In the first quarter of 2002 the CAL–AMR spread varies over a $6
range from a high of $7 to a low of $1. Bets placed according to
rule 1 (and rule 2) experience substantial mark to market gains and
losses but do not capture any of that commotion. Since the spread
increases and decreases over days and weeks, meandering around
the trend that eventually leads to shrinkage to zero and bet exit
(rule 1) or reversal (rule 2), why not try to capture some of that
movement?
Rule 3 is designed to extract more from spreads by adding a
second entry point to that identified in rule 1. For CAL–AMR
the rule is: Make a second bet on the subsequent shrinking of the
spread when the spread increases to $6. Doubled bets on the spread
shrinkage would be made in both 2002 and 2003, increasing profit

12
STATISTICALARBITRAGE
CAL
AMR
55
$
50
45
40
35
30
25
20
| Jan | Feb | Mar Apr | May | Jun Jul | Aug Sep | Oct | Nov | Dec |
| --- | --- | ------- | --- | ------- | ------- | --- | --- | --- |
2000
FIGURE 2.2
Dailyclosingprices,CALandAMR(2000)
| by 150                  | percent!         | (Profit      | is increased |              | by a smaller  | percentage |          | in 2002  |
| ----------------------- | ---------------- | ------------ | ------------ | ------------ | ------------- | ---------- | -------- | -------- |
| over that               | obtained         |              | with rule    | 2 because    | rule 2        | gains      | from the | reverse  |
| bet which               | is               | unaltered    | in rule      | 3. There     | was no        | reverse    | bet      | in 2003, |
| thepositionbeingcarried |                  |              | into2004.)   |              |               |            |          |          |
| This                    | single           | illustration |              | demonstrates | in blinding   |            | clarity  | the mas- |
| sive opportunity        |                  | that         | lay before   | Tartaglia’s  |               | group      | in 1985, | an era   |
| when spreads            |                  | routinely    | varied       | over         | an even wider | range      | than     | exhib-   |
| ited in                 | the examples     |              | in this      | chapter.     |               |            |          |          |
| 2.2.3                   | Rule Calibration |              |              |              |               |            |          |          |
| Immediately             |                  | when         | one extends  | the analysis | beyond        |            | a single | pair, or |
examinesalongerhistoryofasinglepair,theproblemofcalibration
isencountered.InFigure2.2anotherpairofpricehistoriesisshown,

StatisticalArbitrage 13
25
$
20
15
10
5
0
Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
2000
FIGURE 2.3 Dailyclosingspread,CAL–AMR
now for the single year 2000. Figure 2.3 shows the corresponding
spread.1
Wow! We should have shown that example earlier. The spread
variesovera$20range,threetimestheopportunityoftheCAL–AMR
1The price series for AMR is adjusted for the spinoff of Sabre, the company’s
reservations business, on March 16, 2000. Without proper adjustment, the close
price series would drop from $60 to $30 overnight—an unrealistically dramatic
spread change! We elected to adjust prices moving back in time, so that the
pre-spinoffpricesarealteredfromthevaluesthatobtainedinthemarketatthetime,
preservingmorerecentprices.TradingAMRinJanuary2000,onewouldofcourse
havebeenworkingattheactualpre-spinofflevelofcirca$60.Howonemakesprice
adjustments, forward or backward, is a matter of taste, though it must be done
consistently.Returnseriescomputedfromadjustedpricehistoriesareuniqueandfor
thatandotherreasons,mostanalysisisdoneintermsofreturnsratherthanprices.
In this book, prices are used for demonstration because the elucidated points are
more graphicallymadetherewith. Priceadjustment forcorporate events, including
dividendsandsplits,iscriticaltopropercalculationofgainsfromtrading.

14 STATISTICALARBITRAGE
example examined in Figure 2.1. But right there in that rich oppor-
tunity lies the first difficulty for Rules 1–3: The previously derived
calibration is useless here. Applying it would create two trades for
Rule 3, entering when the spread exceeded $4 and $6 in January.
Significantstresswouldquicklyensueasthespreadincreasedtoover
$20 by July. Losses would still be on the books at the end of the
year.Clearlywewillhavetodetermineadifferentcalibrationforany
of Rules 1–3. Equally clearly, the basic form of the rules will work
just fine.
Now considerthe problem of calibration applied to hundredsor
thousandsofpotentialspreads.Eyeballinggraphswouldrequirealot
of eyeballs. A numerical procedure, an automatic way of calibrating
rules, is needed. Enter statistics. The trading rules were divined by
visually determining the range over which the spread varied. This
is trivially computed automatically: The maximum and minimum
spread in Figure 2.1 is −$2 and $7. Allowing a margin of, say, 20
percent, an automatic calibration would give entry and exit values
of $5 and $0 for rule 1. This is not exactly what we selected
by eye, but operationally it generates similar (though richer) trades.
Critically,theprocedureisreadilyrepeatedonanynumberofspreads
by computer.
Forthesecondexample(Figure2.2)thespreadrangeis$3to$22.
The 20 percent margin calibration gives trade entry and exit values
of $18 and $7 respectively. Applying Rule 1 with this automatic
calibration yields a profitabletrade in 2000.That desirableoutcome
stands in stark contrast to the silly application of the example one
calibration (entry at $4 and $6 and unwind at $0 as eyeballed from
Figure 2.1) to the spread in Figure 2.2 which leads to nauseating
mark to market loss.
CalibrationEpochs In the foregoing discussion of eyeball calibration,
we did not make explicit the span of time being considered, which
is two years in the first example, one in the second. Naturally,
both examples were selected to convey in stark terms the beautiful
simplicity and evident availability of the pair trading opportunity.
Nevertheless, the examples are not unrealistic. And so: How much
time isappropriate?
The stocks in Figures 2.1 and 2.2 are the same: CAL and AMR.
The question, ‘‘How much time is appropriate?’’, is now seen to be

StatisticalArbitrage 15
dramatically important continually, not just as a once-only decision
for each candidate pair. Imagine the consequences of using the
calibration of the CAL–AMR spread from 2000 for trading in
2002–2003.Inthiscase,theconsequenceslookbenign:notrades.But
thatisanegativeconsequencebecausevaluabletradingopportunities
aremissed.Inothercases,horriblycostlybetswouldbeplacedusing
a rulecalibrated on out-of-date pricehistory.
This question of how much price history to use to calibrate a
trading rule is critical. In contrast to the analysis described thus far,
one shot, static analysis in which the rule is applied to the same
price history as that from which it was derived, practical trading is
always an application of the past to the unknown future. In Figure
2.4, the four-year spread (2000–2003) history for CAL–AMR is
showntogetherwithupperandlower limits,maximum−20 percent
rangeandminimum+20percentrange,respectively,calculatedwith
alookbackwindowofthreemonths.Whiletheselimitsare,attimes,
notnearlyasgoodastheeyeballlimitspreviouslyexamined,theydo
25
Spread
$ Upper Trade Boundary
20 Lower Trade Boundary
15
10
5
0
-5
-10
Q1 Q2 Q3 Q4 Q1 Q2 Q3 Q4 Q1 Q2 Q3 Q4 Q1 Q2 Q3 Q4
2000 2001 2002 2003
FIGURE 2.4 Dailyclosingspread,CAL–AMR(withupperandlowertraderule
margins)

16 STATISTICALARBITRAGE
retain good properties for trade identification. Furthermore, unlike
the previous in sample calculations, the current estimates are out of
sample projections. On any day, the only price information used in
thecalculationispubliclyavailablehistory.Thecomputedlimitsare,
therefore, practically actionable.
ApplyingRule2,thereare19trades(ignoringthefirstquarterof
2000 since the limits are computed on insufficient data), comprising
4 losing trades and 15 winning trades. Both winning and losing
trades exhibit periods where substantial mark to market losses are
incurred before gains accrue toward the end of the trade. One last
observation:Noticehowthevolatilityofthespreadhassubstantially
declinedfrom2000–2003;muchwillbesaidaboutthatdevelopment
in later chapters.
2.2.4 Spread Margins for Trade Rules
Inresponsetothedemonstratedproblemofdeterminingoperational
limits on the spread range to guide trade decisions, we chose to use
marginsof20percent.Inthethree-monthwindowtheupperbound-
ary, ‘‘short the spread,’’ is max spread −20 percent range, the lower
boundary, ‘‘buy the spread,’’ is min spread +20 percent range. This
operationalprocedurehasthegreatmeritofreadyinterpretation.Itis
unambiguouslyclearwhatthemarginsare:onefifthofthecalculated
range of the spread over thepreviousthreemonths.
Less satisfactory is the use of the extreme values, max and min.
Extremes exhibit great variability. Projecting extremes is therefore
subject to great uncertainty: Think of outliers and all you have read
instatisticstextsaboutcarefulanalysisthereof.Modelingextremesis
acomplicatedandfascinatingareaofstudywithapplicationsranging
from peak river flow for flood prediction to electricity demand for
prediction of generation requirements and the likelihoodof outages,
among many others.
From the extensive variability of extremes comes the need for a
substantial margin (20 percent) for practicable trade rules. Suppose
that just the largest 10 percent of spread displacements served to
generate sufficient trading opportunities to sustain a business based
on historical analysis. It would be unwise to rely on that margin
for actual trading because of the inherent uncertainty in projecting
information into the future. Extremes in the future are certain to

StatisticalArbitrage 17
be different from extremes in the past. If a spread experiences a
‘‘quiet period,’’ business will be poor because few opportunities
will be identified even though there may be plenty of profitable
opportunities. Better to be conservative and use a larger margin. Of
course,aspreadmayexhibitavolatileperiod;theconsequencesthere
are more volatilityin mark to market revenue but nota reductionin
businessor total profit.
Greater stability is obtained between extremes. Projecting the
centrallocationofthespreadisdonewithconsiderablygreaterconfi-
dencethanprojectingtheextremes.Therefore,mostimplementations
modifythe‘‘goshort’’and‘‘golong’’limitstobecomputedasoffsets
fromthecenterratherthanoffsetsfromtheextremes.Bollingerbands,
mean plus or minus a standard deviation, are a classic example. In
spite of the rationale though, it is arguable how much stability is
improved by this switch of focus: The standard deviation is com-
putedfromallthedata,extremesincluded,andsinceobservationsare
squared, the extreme values actually receive proportionally greater
weight!Robustproceduresaresensiblyemployed,whichamountsto
excluding (in more sophisticated applications, down-weighting) the
mostextremevaluesinasamplebeforecomputingsummarystatistics
such as themean and standard deviation.
Extrapolatingpercentagepointsofthespreaddistribution,saythe
twentieth and eightieth percentile, is similarly robust but is seldom
seen. Operationally it is of no practical significance in the simple
trading rules described here. Greater significance is found where
models are more sophisticated and the asymmetry of distributions
has mercenary implications.
Greater (presumed) stability is achieved at the cost of some
interpretability.Thereisnouniquerelationshipbetweenthestandard
deviation of a distribution and the range. When presented with
standarddeviations,manyassumeordon’trealizetheyareassuming
an underlying normal distribution and equate mean plus and minus
one standard deviation as two-thirds probability and mean plus and
minus two standard deviations as 95 percent probability. Financial
data is typically nonnormal, exhibiting asymmetry and significantly
more observations several standard deviations from the mean, the
so-called ‘‘heavy tails.’’ These tails are heavy only by comparison
to the normal distribution, not by what is typical in finance data.
The use of tail area probabilities from the normal distribution is

18 STATISTICALARBITRAGE
thereforeafrequentcauseofmiscalculation—andusuallythatmeans
underestimation—of risk. Most errors of this kind are trivially
avoided by using the empirical distribution—the data itself—rather
than assumed mathematical forms. Moreover, it is quite simple to
examine the fit of a normal curve to a set of data and judge the
accuracy of probability calculations for intervals of interest, be they
inthetailorcenterofthedistribution.Chapter5demonstratesthese
pointsin a discussionof reversion in priceseries.
With so many potentially costly errors attached to the use of
sample moments (mean and standard deviation) why is the range
so readily abandoned? What has been gained by the sophistry? In
addition to the aforesaid (almost unconscious) action on the part of
many,thereistheconsciousactiononthepartofmanyothersthatis
driven by mathematical tractability of models. Extreme values (and
functions thereof) are difficult to work with analytically, whereas
standard deviations are generally much easier. For the normal dis-
tribution typically assumed, the mean and standard deviation are
definingcharacteristics and are thereforeessential.
While the technicalities are important for understanding and
analysis, the practical value for application in the late 1980s and
early 1990s was minimal: Reversion was evident on such a large
scaleandoversuchawiderangeofstocksthatitwasimpossiblenot
to make good returns except by deliberate bad practice! That rich
environment has not existed for several years. As volatility in some
industriesdeclined—theutilitiessectorisasplendidexample(Gatev,
et al.)—raw standard deviation rules were rendered inadequate as
the expected rate of return on a trade shrank below transaction
costs. Implementing a minimum rate of return lower bound on
trades solved that, and in later years provided a valuable risk mana-
gement tool.
2.3 POPCORN PROCESS
The trading rules exhibited thus far make the strong statement that
a spread will systematically vary from substantially above the mean
to substantially below the mean and so forth. The archetype of this
pattern of temporal development is the sine wave. In the early years
of pairs trading, that archetype provided the theoretical model for

StatisticalArbitrage 19
(a)
6.0
5.5
5.0
4.5
4.0
0 20 40 60 80 100
(b)
6.0
5.5
5.0
4.5
4.0
0 20 40 60 80 100
FIGURE 2.5 Processarchetypes:(a)sinusoidal,(b)popcorn
spread analysis, but many trade opportunities were observed to be
missed. An alternative archetype, which we shall call the ‘‘popcorn
process,’’ shown in Figure 2.5, provided new insight. Reversion to
the mean following a disturbance from that mean was more closely
focused upon. In this model, the constraint on spread motion of
undulation(evenifmoreirregularlythanthemathematicalarchetype)
is removed. An upward motion (move to a ‘‘distant’’ peak) may be
followed, after return to the local mean, by another excursion to a
distant peak. Similarly a decline to a distant trough may follow a
previous excursion to a distant trough without an intervening move
to a distant peak. The qualifier ‘‘distant’’ is used here to distinguish
substantive moves from the mean from minor variation about the
mean. Two troughsare bydefinitionseparated by a peak but a peak
is of trading interest only if it is sufficiently removed from the mean
such that movement back to the mean is economically beneficial.
The important point here is that a peak separating troughs can be
nearthemeanandisnotforcedorassumedtobesubstantiallyabove
themean.

20 STATISTICALARBITRAGE
Expressing the popcorn process mathematically is more com-
plicated than writing a sine function, but not much so. If the sine
functioniswritten:
y = sin(t)
t
then thepopcornfunctionmay besimilarly written:
y = I sin(t)
t t
where I is an indicator function taking values 1 or −1 signaling
t
a peak or a trough move. The math is not important here; the
insightfromthedescriptionandgraphicaldepictionoftheprocessis:
Exploiting the popcorn process is not efficiently accomplished using
theturtletrade.InFigure2.5,panel(b),theturtletraderuleidentifies
asingletradewithprofit$2.Thepopcornprocesssuggestsarulethat
signals to exit a trade when the spread returns to the mean, rather
than assuming it will continue beyond the mean to an extreme on
the opposite side from which the trade was entered. This new rule
identifies four trades with total profit $4. Another novel feature of
therule is that it containsperiods where nocapital is committed.
All the necessary calculationsfor the new rule have already been
described: local mean and range of the spread. The change is to the
trade rule.
Rule 4: When the spread increases (decreases) sufficiently far
from the mean (say, k standard deviations) sell (buy) the spread;
unwindthepositionswhen thespread returnsto themean.
Many of the more elaborate models built by statistical arbi-
trageurs,whetherforpairwisespreadsormorecomplicatedfunctions
ofstockpricehistories,arebasedontheunderstandingofthepopcorn
process,orreversiontothemean,ratherthanthesinusoidalorturtle
tradeprocess.Chapter3 describessomeofthemodelsandmodeling
considerations. The interesting phenomenon of stochastic resonance
(also described in Chapter 3) admits a valuable modification of the
exit conditionin Rule4.
2.4 IDENTIFYING PAIRS
Theopportunityishuge.Wehaveasetofoperationaltradingrulesand
automaticcalibrationprocedures.Now,whichpairscanwetrade?

StatisticalArbitrage 21
Early on, stocks were grouped by broad industry classification
andeverypairwithinthosegroupswasacandidate.Riskmanagement
wasrudimentarywithBarramodelsappliedtoconstructedportfolios
and identified factor exposures offset by trades away from the pair
portfolio (using stocks or Standard and Poor’s (S&P) futures to
neutralizeβ exposure, for example).
Elaborationswereintroducedasgreatercontroloverreturnvari-
ability became desirable and as experience showed where structural
weaknesses lay. Individual manager preference became influential
when hedge funds began marketing pairs trading and statistical
arbitrage strategies.
Maximizingcorrelationswas an early filter applied to pair selec-
tion: Compute the correlation of each candidate pair (using, for
example, two years of daily data) and retain only those pairs hav-
ing correlations greater than some minimum. On the assumption
that past correlation is predictive of future correlation, this filtering
eliminates pairs of stocks that exhibit little or no relationship. The
rationale holds that uncorrelated stocks are behaviorally unrelated
and, hence, unpredictableas a pair.
2.4.1 Refining Pair Selection
Reversion betting on pair spreads works best when the two con-
stituent stock prices continually move apart and together again.
That pattern of behavior, stock A increasing when stock B decreases
and vice versa, generates very low (even negative) correlation. So
from a profit or return perspective, were the early correlation filters
(searching for a high degree of correlation) quite wrong? No: In
the short term, profits may be forgone by excluding low correlation
pairs but the long-run risk situation is greatly improved. Stocks that
typically exhibit contrary or unrelated price movements are more
likely to respond disparately to fundamental market developments
than stocks that tend to move together. At some point, unrelated
stocksare very likelyto create a costly pairtrade.
That insight motivates a subtly different approach to the corre-
lationfilter.Definingriskmoments(orevents)astimeswhenastock
pricetracechangesdirectionsuch thatapeak ortroughisformed,it
is desirable for risk minimization purposes to select pairs that show
similareventhistories—peaksandtroughscloseintimewithsimilar

22 STATISTICALARBITRAGE
sized moves for the two stocks between these events. Such pairs
are less likely to react divergently (except, perhaps, in the imme-
diate aftermath) following a disturbance to the market (political,
industrialdevelopment,etc.). For profitmaximization,it is desirable
that between events the two stocks develop along different price
trajectories,exhibitingasmuchnegativecorrelation—movingapart,
then together—as possible. See Chapter 5 for a formal treatment of
desirableand undesirablepair correlations.
2.4.2 Event Analysis
Theturningpointalgorithm worksas follows:
1. A local maximum in the price series is a turning point if subse-
quently the price series declines by an amount giving a negative
return greater in absolute value than a specified fraction of the
local, annualized returnvolatility.
2. Similarly,alocalpriceminimumisaturningpointifsubsequently
the price rises by an amount giving a return greater than the
specified fractionof local, annualizedreturn volatility.
3. Look at the price trace in Figure 2.6 (General Motors, daily
adjusted prices). Given a turning point identified at a, where
is the next turning point? Point a is clearly a local minimum;
therefore,thenextturningpointmustbealocalpricemaximum.
Move forward in time looking at the price series from a to t.
Identify the local maximum price in the interval [a, t]; call it p.
Is the decline from the price at p to the price at t greater than
k percent of thelocal volatilityat t (lookingback)?
4. Whenp = mandt = t ,theanswerisno.Notuntilbisidentified
1
as the local maximum (t > t ) and then not until t = t , is the
2 3
answer yes.
5. Forthisexample,specificationisforawindowof20daystodefine
localvolatility,anannualizationfactorof16,andaturningpoint
qualifyingfractionof 30percent.
Figure 2.7 shows the General Motors price series again, this
time with turning points identified with a less demanding criterion:
A decline in price from a peak by 25 percent of the local volatility
qualifiesthepeakasaturningpoint.Fouradditionallocalextremaare

23
StatisticalArbitrage
80
$
b
(cid:127)
(cid:127)
70
c
|     |     |     |     |     | (cid:127) |     |     | (cid:127) |     |
| --- | --- | --- | --- | --- | --------- | --- | --- | --------- | --- |
m
| 60  |     |     |     |     |     | (cid:127)           |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | --- |
|     |     |     |     |     |     | (cid:127) (cid:127) |     |     |     |
(cid:127)
|     |     | (cid:127) |           |     |     | a   |     |     |     |
| --- | --- | --------- | --------- | --- | --- | --- | --- | --- | --- |
| 50  |     |           | (cid:127) |     |     |     |     |     |     |
(cid:127)
40
|            |                                                            |          |     |     |          |     | t1 t2    | t3  |     |
| ---------- | ---------------------------------------------------------- | -------- | --- | --- | -------- | --- | -------- | --- | --- |
| 19970102   |                                                            | 19970524 |     |     | 19971016 |     | 19980312 |     |     |
| FIGURE 2.6 | Adjustedclosepricetrace(GeneralMotors)with30percentturning |          |     |     |          |     |          |     |     |
pointsidentified
| identified | (ignoring  | the    | series     | end   | point) compared |             | with    | the default |     |
| ---------- | ---------- | ------ | ---------- | ----- | --------------- | ----------- | ------- | ----------- | --- |
| 30 percent | criterion. | Still, | two        | local | peaks           | and troughs |         | in mid-1997 |     |
| are not    | identified | by the | algorithm. |       | They            | provide     | returns | of about    |     |
−4
| percent | in  | a few days—a |     | fabulousannualizedrate |     |     | of  | return. |     |
| ------- | --- | ------------ | --- | ---------------------- | --- | --- | --- | ------- | --- |
Figure2.8showstheGeneralMotorspriceseriesoncemore,with
| an even            | lessstringentturningpointcriterion:A |                 |            |       |             | declineinpricefrom |                     |            |      |
| ------------------ | ------------------------------------ | --------------- | ---------- | ----- | ----------- | ------------------ | ------------------- | ---------- | ---- |
| a peak             | by 20                                | percent         | of the     | local | volatility  | qualifies          | the                 | peak       | as a |
| turningpoint.Eight |                                      | additionallocal |            |       | extrema     | are                | identified(ignoring |            |      |
| the series         | end                                  | point) compared |            | with  | the default | 30                 | percent             | criterion, |      |
| the same           | additional                           | four            | identified |       | by the      | 25 percent         | criterion           |            | plus |
anotherfour.
Inotherexamples,changingthewindowlength,thestrictcapture
byalessstringentcriterionofthecompletesetofturningpointsiden-
| tified by        | a more | stringent | criterion    |     | is not observed. |          | These | examples    |     |
| ---------------- | ------ | --------- | ------------ | --- | ---------------- | -------- | ----- | ----------- | --- |
| and observations |        | serve     | as reminders |     | that the         | analysis | here  | is strictly |     |
statistical.Theeventsreflectmarketsentimentbutthatmaybedriven
| by news        | unrelated | to           | the stock | or  | by no identifiable |     | cause. | Finding |     |
| -------------- | --------- | ------------ | --------- | --- | ------------------ | --- | ------ | ------- | --- |
| such reasonsis |           | an analyst’s | job.      |     |                    |     |        |         |     |

24 STATISTICALARBITRAGE
80
$
70
60
50
40
19970102 19970524 19971016 19980312
FIGURE 2.7 Adjustedclosepricetrace(GeneralMotors)with25-percentturning
pointsidentified
Table 2.1 gives a summary comparison of the alternative event
series for the pair Chrysler (before its acquisition by Daimler) and
General Motors. The increase in return correlation for interevent
returns is striking, as are the insignificant differences across alter-
native event series. The latter is a useful property—interevent
correlations are robust (not sensitive) to the precise calibration of
theeventidentificationalgorithm.Therefore,itisnotnecessarytobe
overly concerned about which set of events to use in the correlation
analysis as a screen forgood risk-controlledcandidatepairs.
Events in trading volume series provide information sometimes
not identified (by turning point analysis) in price series. Volume
patterns do not directly affect price spreads but volume spurts are a
usefulwarningthatastockmaybesubjecttounusualtradingactivity
and that price development may therefore not be as characterized
in statistical models that have been estimated on average recent
historical price series. In historical analysis, flags of unusual activity
areextremelyimportantintheevaluationof,forexample,simulation

25
StatisticalArbitrage
80
$
70
60
50
40
| 19970102 |     | 19970524 |     |     | 19971016 |     | 19980312 |     |
| -------- | --- | -------- | --- | --- | -------- | --- | -------- | --- |
FIGURE 2.8
Adjustedclosepricetrace(GeneralMotors)with20percentturning
pointsidentified
|     | TABLE     | 2.1 | EventreturnsummaryforChrysler–GM |         |                   |      |     |     |
| --- | --------- | --- | -------------------------------- | ------- | ----------------- | ---- | --- | --- |
|     | Criterion |     |                                  | #Events | ReturnCorrelation |      |     |     |
|     | daily     |     |                                  | 332     |                   | 0.53 |     |     |
|     | 30%move   |     |                                  | 22      |                   | 0.75 |     |     |
|     | 25%move   |     |                                  | 26      |                   | 0.73 |     |     |
|     | 20%move   |     |                                  | 33      |                   | 0.77 |     |     |
results.Identifyingvolumepeaksinhistoricaldataisscarcelydifferent
| from the        | demonstration |             |           | of peak       | identification |           | in price        | histories   |
| --------------- | ------------- | ----------- | --------- | ------------- | -------------- | --------- | --------------- | ----------- |
| documented      |               | previously. | In        | live trading, |                | however,  | forward-looking |             |
| monitoring      | for           | patterns    | of        | increased     | trading        | volume,   | an              | important   |
| risk management |               | tool,       | is subtly | different.    |                | One needs | to              | flag volume |
| increase        | during        | the         | build-up  | before        | a peak         | is        | identifiable    | because     |
identificationafterthefactisusuallytoolateforamelioratingimpact
on a portfolio.

26 STATISTICALARBITRAGE
2.4.3 Correlation Search in the Twenty-First Century
Several vendors now offer software tools for managing aspects of
pairs trading, from identifying tradable pair candidates to execution
channelsandportfoliomanagement.Correlationsearchesofthetype
described here were manually programmed and carried out in the
1980s.Nolongeristhisnecessary.CreditSuisseFirstBoston,forone,
offersatoolthatallowsausertooptimallyfitaBollingerband–type
pair trading model to any specified pair of stocks. The program
searches over a range of fixed-width windows simulating trading of
a mean plus or minus standard deviation model;simulation‘‘profit’’
isthemetricusedtocomparemodels(datawindowlength,Bollinger
bandwidth) and the maximum profit generating model is identified.
One can very quickly fit models to many pairs using such tools.
The dangers of relying solely on such shallow data analysis should
be immediately evident. Tools with similar capabilities are offered
by Goldman Sachs, Reynders Gray, and Lehman Brothers, among
others.
Atthistime,nocommercialtoolsareknowntoexistthatfacilitate
identification of event or turning points and compute interevent
correlations.
2.5 PORTFOLIO CONFIGURATION AND RISK CONTROL
As models were developed, increasing attention was directed to
portfolio risk control. Mean–variance approaches were favored for
alongtimeasprofitsrolledinandriskwasdeemed‘‘undercontrol.’’
Thefollyofthatthinkingwasrudelydemonstratedinthesummerof
1998,but that is gettingahead of thestory (seeChapter 8).
Some modelers incorporated risk exposure calculations along
with return forecasts into the portfolio construction process directly
(seesection2.4,andthedescriptionofthedefactormodelinChapter
3); others (particularly those whose model comprised a set of rules
with no explicit forecast function) first constructed a portfolio, then
calculated the exposure of that portfolio to certain defined market
factors, and controlled risk by hedging those exposures separately
fromthe betsconstitutingthe portfolio.
The objective is to select a portfolio of stocks that maximizes
return to employed capital. Given perfect foresight, the optimal

StatisticalArbitrage 27
portfolio consists of maximum possible investments in the stocks
with the greatest return until available capital is exhausted. Of
course, we do not have perfect foresight. In its stead, we make do
with the best forecast we have. The goal is still to maximize actual
returnbut,intheforecastingguessworld,wehavetofocusattention
on expected return.
Forecasts, unlike foresight, do not come with a guarantee of the
outcome. There is risk in acting on forecasts. A single pair spread
expected to ‘‘revert to its local mean’’ may continue to increase
beyond the point at which stop loss limits force exit from the
position. This new element, risk, complicates the goal, which now
becomes twofold: Maximize expected return and maintain the risk
of achieving that return belowa certain tolerance.
So far so good. Going from foresight to forecast we exchange
certainty for uncertainty; we move from guaranteed optimization
to constrained optimization of a best guess. However, in practice
matters are not quite as straightforward as that sentence seems to
imply.Thefirstobstacleispreciselyspecifyingthenotionofrisk—or,
at least, its practical implementation. Risk arises because there is no
guarantee that a particular forecast will be borne out in reality.
Indeed, the truth is that it would be an extraordinary event if a
forecast turned out to be 100 percent accurate. Only one outcome
yields complete forecast accuracy. But there is an infinity of possible
outcomesthattranslatetooddsofinfinitytooneagainsttheforecast
being correct. Hence, the remarkable fact that a forecast is almost
certainly goingto bewrong.
‘‘Go for the best’’ becomes ‘‘Go for the best guess—but bear in
mind what disasters might occur and do yourbest to protect against
thoseundesirableoutcomes.’’
Just as we have to guess at the best (forecast) we have to guess
at the disasters. Typically, we do this a little differently from the
way we look for the best guess: Rather than looking for particular
disaster scenarios we look at the range of disasters—from small to
large—that may befall us. This view is encapsulated in the forecast
variance. (Scenario analysis is often used to be aware of ‘‘unlikely’’
extreme situations notwithstanding routine, daily, ‘‘risk controlled’’
portfolioconstruction.Thedistinctionofextremeandroutineriskis
deliberatelyvague.)

28 STATISTICALARBITRAGE
The goal has, therefore, become: Maximize expected return sub-
ject to a limit on believed variation about that expected return. The
variance constraint reduces the admissible set of portfolios from the
set of all portfolios to the set of portfolios for which the expected
variation of theexpectedreturn is belowsomethreshold.
Itiscrucialnottolosesightofthefactthatallthesequantities—
forecast returns and variances thereof—are uncertain. The forecast
variance guides us as to how much the outcome may reasonably be
expected to deviate from the best guess. But that forecast variance
is itself a guess. It is not a known quantity. And remember what
was stated onlytwo paragraphs ago: Forecast variance characterizes
average behavior; anythingis possibleon any given instance.
With all those cautionary remarks having been said, it is true
that we are using a forecast constructed in the belief that it has
some predictive utility. That, on average—but not in any particular
case or set of cases—the forecasts will be better guesses of future
events than random guesses. And that the range of variation of
outcomesabouttheforecastsisreasonablyquantifiedbytheforecast
variances—again, on average.
Finally we are in a position to make operational the notion
and quantification of risk. We defined the risk of a portfolio as the
expectedvarianceofthatportfolio.Ouraversiontoriskisthentaken
to be a constant multiple of that variance. Thus, the goal becomes:
Maximize expected return subject to a limit on expected variance
of return.
Letusexpresstheseresultsinmathematicalform.First,definition
of terms:
n Number of stocks in investment universe
f Expectedforecast returnfor stock i; f = (f ,...,f ) (cid:1)
i 1 n
(cid:2) Expectedvariance of returns, V[f]
i Value to be invested in stock i; p = (p ,...,p ) (cid:1)
p 1 n
k Risk tolerancefactor
Now thegoal isexpressed as:
maximize p (cid:1) f −kp (cid:1) (cid:2)p

StatisticalArbitrage 29
2.5.1 Exposure to Market Factors
Statistical arbitrage fund managers typically do not want a portfolio
that takes long positions only: Such a portfolio is exposed to the
market.(Apairstradingscheme,bydefinition,willnotbebiasedbut
statistical arbitrage models more generally readily generate forecasts
that, unless constrained, would lead to a portfolio with long or
short bias.) If the market crashes, the value of the portfolio crashes
with it. This much we can say regardless of the precise composition
of the portfolio. Given a desire for a market neutral strategy, the
goal is to pick off moves in stock prices after allowing for overall
market movement. That begs the question of how one defines ‘‘the
market.’’Conventionally,theS&P500indexistakenas(aproxyto)
the market. Each stock in the portfolio is statistically examined to
quantifythestock’sexposuretotheS&Pindex.Thesequantifications
are then used to determine a portfolio’s exposure to the market.
Marketneutralityisachievedbyalteringtheproportionsofstocksin
theportfolio.
Makethe definition:
l Exposureof stock i to themarket; l = (l ,...,l ) (cid:1)
i 1 n
Then themarket exposureof theportfoliop is:
market exposure= p (cid:1) l
Withthedesireformarketneutrality,theobjectivefunctionismodi-
fied to:
p (cid:1) f −kp (cid:1) (cid:2)p−λp (cid:1) l
where λ is a Lagrange multiplier(relevant onlyto theoptimization).
The neutrality desire is extended from the market as a whole to
include market sectors. We want to avoid overall exposure to, for
example,theoilindustry.Thisisaccomplishedinthesamewayasis
market neutrality: Define exposures of stocks to ‘‘the oil industry.’’
Notice that this is a more general notion than simply defining an
indexfortheoilindustryandexposuresofoilindustrystockstothat
index. Potentially every stock, oil industry or not, has an exposure

30 STATISTICALARBITRAGE
to the oil industry market factor. Given this set of exposures, the
objectivefunctionextendsin a similar way as for themarket factor.
Makethe definition:
l Exposureof stocki to theoil industry; l = (l ,...,l ) (cid:1)
1,i 1 1,1 1,n
Theobjectivefunctionisextendedto:
p (cid:1) f −kp (cid:1) (cid:2)p−λp (cid:1) l−λ p (cid:1) l
1 1
where λ is anotherLagrange multiplier.
1
Obviously,othermarketfactorsmaybeincludedintheobjective
function to ensure zero portfolio exposure thereto. For q market
factors, the objectivefunctionis:
p (cid:1) f −kp (cid:1) (cid:2)p−λp (cid:1) l−λ p (cid:1) l −···−λ p (cid:1) l
1 1 q q
Determining the portfolio that maximizes the objective function is a
straightforward applicationof theLagrange multipliermethod.
2.5.2 Market Impact
We forecast IBMstock to yield annualized return of 10 percent over
thenextweek.Theforecastismorecertainthananyforecastwehave
ever made. We want to buy $10 million worth of stock. Ordinarily,
ademandofthatsizewillnotbefilledatthecurrentofferprice;most
likely the offer price will rise as the demand is filled. This is market
impact. Market impact is incurred with most trades, regardless of
size, since the market is not static between the time a forecast is
made (using the latest available price) and the time the desired trade
is placed and subsequently filled. Without actual trading history, it
is impossible to gauge market impact. Even with trading history,
it is possible only to make a guess: Once again we are forecasting
an uncertain event. (See Chapter 10 for recent developments with
critical implicationsfor statistical arbitrage.)
The importance of market impact is great. A good estimate of
the likely realizable fill price for desired trades enables the trading
system to filter potentially unprofitable trades from the portfolio
optimization.

StatisticalArbitrage 31
Immediately,aquestionarises:Ismarketimpactnotsubsumedin
theconstructionof theforecastfunction?Superficiallyonly.Thereis
an implicitassumptionthatthestockscan betradedinstantaneously
atthecurrentprice.Okay,butwhyshouldthetimedelaytocomplete
a physical trade result in a cost? Should we not expect that some
prices will go with the desired trade and some against, with every-
thing averaging out over numerous trades on many days? Again,
superficially only. Our participation in the market is not accounted
for in the model building process. A buy order from us adds to
demand, dragging up price; the opposite for a sell order. Thus, our
own trading introduces a force against us in the market. So our
forecasts are really only valid providing we do not act on them and
participatein themarket.
Onemightaskthat,sincethegoalistobuildaforecastmodelthat
isexploitable,whynotincludetheinformationthattheforecastswill
betradedintothemodelbuilding?Theshort—andprobablyalsothe
long—answer to that is that it is just too difficult.(Equivalently, the
necessary data is unavailable; see Chapter 10 for what is possible,
even routinefor a select few, at present.) Thepragmatic expedientis
thereforeto buildaforecast that isexpectedtobevalid if weremain
apassiveobserver,thenmakeanadjustmentfortheeffectouractive
participationislikelyto have.
Market impact is a function of what we decide to trade. Denot-
ing the current portfolio by c, the objective function is extended
generically to:
p (cid:1) f −market impact(p−c)−kp (cid:1) (cid:2)p−λp (cid:1) l−λ p (cid:1) l −···−λ p (cid:1) l
1 1 q q
Determining the functional form of ‘‘market impact’’ is an unsolved
research problem for most participants because of inadequate data
(typicallyrestrictedtoone’sownorderandfillrecords)and,insome
cases, lack of motivation. Again, see Chapter 10 for more recent
developments.
2.5.3 Risk Control Using Event Correlations
In the preceding section we explored the idea of event correlations
as a basis for identifyingcollectionsof stocks that existentiallyshare
common risk factors: Stocks repeatedly exhibit directional price

32 STATISTICALARBITRAGE
change at the same time, in the same orientation, and move by a
similar amount between such changes. Within a group, stocks have
similar elasticityto news orwhat onemight call ‘‘event betas.’’
Building a portfolio that is matched dollar-for-dollar long and
short from dollar-matched portfolios built from groups of stocks
characterized by similar event betas automatically incorporates sub-
stantial risk control. Each group defines a collection of stocks that
have repeatedly exhibited essentially the same price reaction to eco-
nomic developments meaningful for those stocks. The key feature
hereistherepeatednatureofthemoves.TobowdlerizeIanFleming,2
onceishappenstance,twiceiscoincidence,thethirdtimeiscommon
risk exposure. A portfolio thus formed has a low probability of
experiencing large loss generating disparate moves of constituent
stocks in response to a market shock. After the terrorist attacks on
the United States in 2001, event beta–neutral portfolios of large
capitalization stocks exhibited only mundane volatility in valua-
tion despite the dramatic market decline and spike in individual
stock volatility.
2.6 DYNAMICS AND CALIBRATION
The reversion exploitation model is applied to local data. For
example, estimated interstock volatilities are calculated using a
weighting scheme, discounting older data (see Chapter 3). In the
trade rules examined earlier in this chapter, we chose a 60-day
fixed-length window and computed trade limits on spreads as a
function of the spread range (a) directly, and (b) using the empirical
standard deviation of the spread distribution. These daily updated
estimates adjust current trade entry and exit points. Similarly, daily
updatedliquidityestimatesmodifytradedeal sizeandportfoliocon-
centration.Thus,evenwithan unchangedmodelthereiscontinuous
adaptation to local market conditions.
Occasionally the model is recalibrated (or a manager ‘‘blows
up’’). Recall the CAL–AMR spread, which changed radically from
$20 in 2000to $6 in 2002.
2SpokenbyAuricGoldfingertoJamesBondinIanFleming’sGoldfinger.

StatisticalArbitrage 33
The techniques of evolutionary operation (EVOP) can be
employed to help uncover persistent changes in the nature of the
reversion phenomenon exploited by a model. Reversion is exhibited
by stock price spreads on many frequencies (Mandelbrot, fractal
analysis), one of which is targeted by a modeler’s chosen calibra-
tion, that choice being dictated by factors including robustness of
the response to small changes in parameter values, modeler’s pref-
erence, research results, and luck. Applying EVOP, several other
frequencies (model calibrations) are monitored in tandem with the
tradedmodelto provideinformationonchanges inthenatureofthe
response across frequencies. There is always noise—one frequency
neverdominatesnearbyfrequenciesintermsofactualandsimulated
trading performance month after month. It is crucial to understand
the normal extent of this noise so that apparent (recent) underper-
formance by the traded model vis-a`-vis a nearby (in model space)
competitormodelisnotmisinterpretedasaneedforamodelchange.
There is also evolution. Over several years, trends in the reversion
response as revealed through comparative model performance stand
out from the local variation (noise). When identified, such a trend
shouldbeadapted to—thetraded modelcalibration revised.
Analysisofaclassicpair-tradingstrategyemployingafirst-order,
dynamic linear model (see Chapter 3) and exhibiting a holding
period of about two weeks applied to large capital equities shows a
fascinating and revealing development. In March 2000 a trend to a
lowerfrequencythatbeganin1996wasdiscovered.Firsthintedatin
1996, the scale of the change was within experienced local variation
bounds,sothehintwasonlyidentifiablelater.Movementin1997was
marginal. In 1998, the problems with international credit defaults
and the Long Term Capital Management debacle totally disrupted
allpatternsofperformancemakinginferencedifficultandhazardous.
Although the hint was detectable, the observation was considered
unreliable. By early 2000, the hint, there for the fourth consecutive
year and now cumulatively strong enough to outweigh expected
noise variation, was considered a signal. Structural parameters of
the ‘‘traded’’ model were recalibrated for the first time in five years,
a move expected to improve return for the next few years by two
or three points over what it would otherwise have been. Simulation
for 2000–2002 significantly exceeded that expectation as market
developments caused a decline in performance of higher frequency

34 STATISTICALARBITRAGE
compared with lower frequency strategies. See Chapter 9 for a
detailed discussionof theissues involved.
2.6.1 Evolutionary Operation: Single
Parameter Illustration
Evolutionaryoperationforasingleparameterisillustratedinthefour
panels of Figure 2.9. Panel (a) shows an archetypal response curve:
Forarangeofpossiblevaluesforamodelcoefficient,the(simulated)
returnfromoperatingthestrategyshowsasteadyincreasetailingoff
intoaplateauthenquicklyfallingoffacliff.Onewouldliketoidentify
thevalueoftheparameterforwhichreturnismaximized—andthatis
simplewhenanalyzingpastdataandwhentheresponserelationship
is invariant.
Panel (b) illustrates what one observes in practice. Every year
the response is different. Similar—that is why strategies work more
often than not—but different. When selecting a parameter value at
whichtooperateastrategy,itiscriticaltounderstandboththeform
oftheresponsecurveandthenaturalamountofvariationand relate
these to understanding of the phenomenon under study—reversion
in this case—when it is available. Picking the return-maximizing
value of the parameter from panel (a) is risky because in some years
theresponsecurveshiftssufficientlythatmodelperformancefallsoff
the cliff. Risk management operates at the model calibration stage,
too:Backaway fromthecliffandsettleforgenerallygoodyears and
low risk of a catastrophe rather than occasional outstanding years
and occasional disasters. Oneshouldexpect that disasterswill occur
fromuncontrollablefactors:Admittinglargeprobabilitiesofdisaster
from ‘‘controllable’’factors is not a soundrisk management policy.
Panel (c) showsan archetypal evolutionin response:Thegeneral
form moves smoothly through space over time (and the form may
itself smoothly change over time). In practice such evolution, when
it occurs, occurs in conjunction with normal system variation as
just seen in panel (b). Experience is thus like a combination of the
movementsin panels (b) and (c), illustratedin panel (d).
Astheresponsecurvechangesovertime,arangeoftheparameter
space consistently yields good strategy performance. Every year is
different and over time the parameter range to aim for gradually
moves. The original range continues to deliver reasonable perfor-
mance, but becomes less attractive over several years. Evolutionary

35
StatisticalArbitrage
| (a) |     |     |     |     | (b) |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| (c) |     |     |     |     | (d) |     |     |     |
4
2
1
3
| FIGURE 2.9 | Evolutionaryoperation:detectingsustainedsystemresponsechange |           |            |                   |          |           |             |             |
| ---------- | ------------------------------------------------------------ | --------- | ---------- | ----------------- | -------- | --------- | ----------- | ----------- |
| operation, | the                                                          | continual | monitoring |                   | of       | system    | performance | away        |
| from the   | currently                                                    | believed  |            | best calibration, |          | enables   | one         | to identify |
| transient  | and persistent                                               |           | system     | response          | changes. |           | Transient   | changes     |
| provide    | information                                                  | to        | update     | the               | view     | of normal | system      | response    |

36 STATISTICALARBITRAGE
variation; enduring system response changes can be adapted to,
improvinglong-term system performance.
As just exemplified, evolutionary operation monitoring looks
beguilingly simple—and, indeed, the concepts and rote application
are straightforward. Unsurprisingly, reality is more complex. The
time scale and timing of change may differ from the annual focus
explicitly used here. And, of course, models are typically defined by
a collectionof parameters, not just one.
Years are somewhat artificial and arbitrary time periods in this
monitoring context. Change can occur abruptly within a calendar
year (September 11, 2001) or slowly over one or more years. Mon-
itoring aspects of a strategy that reveal diagnostic information at
differentfrequenciesisanothercritical task.
Statistical arbitrage models have several critical defining param-
eters. The monitoring scheme is complicated because there are
interactioneffects:Theimpactofachangeinoneparameterdepends
uponthesettingsofotherparameters.Theschemeofcontinualassess-
ment of the performance of alternative model calibrations must be
designedtorevealchangesinthoseinteractionsaswellaschangesin
thedirectresponseofstrategyperformancetoindividualparameters.
More complicated models that involve several steps of analy-
sis formally may include hundreds or even thousands of estimated
parameters. Conceptually, the monitoring problem is ostensibly the
same: One is looking for evidence of change other than transient
noise over time. The practice is yet more complicated than for mod-
els with handfuls of parameters because these high-parameter-count
models often lack manageable interpretability of individual param-
eters. Answering the question, ‘‘What does change X in parameter
θ signify?’’, is impossible. Indeed, with such models even positing
the question is difficult. Groups of parameters may have a collective
interpretabilityin which case understandingcan be built component
by component,sometimeswith a hierarchical structure.
To close this section, it is worth reiterating an important point:
Underpinning monitoring activity, from mechanics to interpretation
toaction,isunderstandingofthephenomenonbeingexploited—why
it exists, what drives the opportunities, and how exploitation works
in the contextof themodel.

3
CHAPTER
Structural Models
Private informationis practically thesourceof every large
modern fortune.
—An Ideal Husband,Oscar Wilde
3.1 INTRODUCTION
T he discussion in Chapter 2 is couched largely in terms of trading
rules based on estimates of spread ranges calculated on moving
windows of data history. Figure 3.1 shows the bands calculated as
mean plus or minus one standard deviation using a window of 60
days for the CAL–AMR spread. (Compare this with Figure 2.4,
wherein the limits are calculated using the maximum −20 percent
range and minimum +20 percent range over a 60-day window, and
review the discussion in Section 2.2.) Implicit in these trading rules
isaforecastthatthespreadwillinthenearfuturereturntothelocal
mean.Figure3.2showstheCAL–AMRspread again,thistimewith
theimplied forecast function.
In formal terms the point forecast, or expected value, for every
future time period is the currently estimated mean value. Now it is
not really believed that the spread will actually equal the mean each
time period, or even one time period in the near future. (Obviously
thetradingrulesanticipatesystematicvariationaboveandbelowthe
mean.) It is simply that the best guess based on using the moving
averagemodelisthatinthenearfuture,thespreadwilllikelyexhibit
values centered on the mean. How near is ‘‘near’’ remains, like so
much else, unspecified.
37

38 STATISTICALARBITRAGE
25
Spread
$ Upper Trade Boundary
Lower Trade Boundary
20
15
10
5
0
−5
−10
2000 2001 2002 2003 2004
FIGURE 3.1 Dailyclosingspread,CAL–AMR,withstandarddeviationtrade
boundaries
The mean plus or minus standard deviation trading rules were
not compiled by formal statistical model building. Rather, simple
eyeballing and a little thinking lead to the hypotheses, expressed as
trade rules, which turned out to work satisfactorily. Nonetheless,
therules constituteamodelwiththeforecast functioninterpretation
just cited.
TheCSFBtool,mentionedinChapter2,goesalittlefurtherthan
our eyeballing and systematically searches through many alterna-
tive model specifications—window length and number of standard
deviationsfortrade entry boundaries.Thismodel fittingorselection
procedure implicitly uses a utility maximization criterion, maximize
simulatedtradingprofit,insteadofastatisticalestimationprocedure
suchasmaximumlikelihoodorleastsquares.Thatisasophisticated
approach, unfortunately undermined by the sole focus on in-sample
calculations. Effectively, the utility function is misstated for the pur-
pose of identifying models that might be expected to do somewhat
reasonablyinpractice.Whatisreallyofinterestismaximizingprofit
out of sample with some regard to draw-down limits, mimicking

StructuralModels 39
25
Spread
$
Moving Average
20
15
10
5
0
−5
−10
2000 2001 2002 2003 2004
FIGURE 3.2 Dailyclosingspread,CAL–AMR,withmovingaverageforecast
function
actual useof divined tradingrules, but thoseconsiderationsbegin to
take the tool in the direction of a strategy simulator, which is not
likelyto be offeredfree of charge.
3.2 FORMAL FORECAST FUNCTIONS
The value of thinking about a formal forecast function is that it
gives a specific set of values to compare to realizations and thereby
to judge the efficacy of model projections. Mark to market losses
on a trade will indicate the presence of a potential problem; the
pattern of forecast–outcome discrepancies provides information on
thepossiblenatureoftheproblem.Suchinformationadmitsaricher
set of responses to loss situations than a blunt stop loss rule such as
a simplepercentage loss.
Inthischapter,wewillconsiderafewofthestructurallysimplest
classical models for time series data. One or two non–time-series-
modelarchitectureswillalsobedescribedillustratingsomewhatmore
involved modelingof stock pricedata.

40 STATISTICALARBITRAGE
3.3 EXPONENTIALLY WEIGHTED MOVING AVERAGE
Moving average, or MA, models are familiar from Chapter 2. A
moreflexibleschemeforlocalsmoothingofseriesistheexponentially
weightedmovingaverage,orEWMA.Incontrasttothefixedwindow
of data with equal weights of the MA, the EWMA scheme applies
exponentially declining weights to the entire data history. Recent
data thereby have the most influence on the current estimate and
forecasts, while large events in the remote past retain influence. The
form of the projected forecast function (for k = 1,2,3,...,n steps
ahead) is, like that of the MA, a straight line. The value is different,
however. An EWMAiscomputedrecursively as:
x t = λx t−1 +(1−λ)y t−1
where y is the observation at time t, x is the EWMA estimate, and
t t
λ is the discount factor. The size of the discount factor 0 ≤ λ ≤ 1
dictateshowfastolderobservationsbecomeirrelevanttothecurrent
estimate (equivalently, how much data history contributes to the
current estimate).
The recursive form of the EWMA forecast calculation immedi-
ately reveals a simplification over MA schemes. Only the current
forecast x needs to be retained to combine with the next observa-
t
tion for updating the forecast. While computers don’t care whether
one or twenty or fifty pieces of information have to be retained in
memory, people do. In fact, the moving average can be expressed
in a recursive fashion that requires only two pieces of information
to be carried so the efficient memory support is unfairly hijacked
byEWMA.Muchmorecompellingaretheadvantagesdemonstrated
below;oncefamiliarwithexponentialsmoothingforforecasting,you
willwanttoconsignyourmovingaverageroutinestothe‘‘obsolete’’
folder.
Figure3.3showstheCAL–AMRspread withEWMA(0.04)and
MA(60) forecast functions. The EWMA discount factor, 0.04, was
selected specifically (by eye—a formal closeness criterion such as
minimum mean square could have been employed but this context
simplydoesn’trequirethatdegreeofformalism)togiveaclosematch
tothe60-daymovingaverage.Onlywhentherawseries(thespread),
changes dramatically, do the two forecast functions differ by an

StructuralModels 41
25
$ EWMA(0.04)
MA(60)
20
15
10
5
0
−5
−10
2000 2001 2002 2003 2004
FIGURE 3.3 CAL–AMRspreadwithEWMAandMAforecastfunctions
appreciable amount. Table 3.1 gives EWMA discount factors that
produce similar local mean estimates to a range of moving averages
(for‘‘well behaved’’ data series).
The utility of the EWMA’s flexibility is starkly apparent in two
situations where reversion plays fail: step changes and trends in
spreads. Figure 3.4 illustrates the situation where a spread suddenly
narrowsandsubsequentlyvariesaroundthenew,lowermeanvalue.
The mean and standard deviation bands (using a 20-day window)
indicate that the long bet entered on September 7 incurred a large
TABLE 3.1 EWMA–MA
equivalences
MA(k) EWMA(λ)
10 0.20
30 0.09
60 0.04

42 STATISTICALARBITRAGE
Spread
20 EWMA
MA
$ Upper Trade Boundary
Lower Trade Boundary
15
10
5
0
−5
−10
6 13 20 27 3 10 17 24 31 7 14 21 28 5 12
Jul Aug Sep
2001
FIGURE 3.4 LevelchangeinspreadandMA-EWMAforecastfunctions
mark to market loss, $11, at the time of the spread decrease and
eventually the bet closed at a loss of that magnitude on October 11
(assuming a popcorn process model). Using the EWMA instead of
the MA is of negligible difference. The flexibility advantage shows
up as soon as we introduceforecast monitoringand intervention.
When the large forecast error occurs (the day of the unusual
spread decrease) the monitoring system is triggered, alerting the
modeler to a potential violation of model assumptions, and hence,
invalidating the forecasts. Upon further investigation, the modeler
might discovera fundamentalreason forthe spread behavior, which
might lead to a decision to terminate the trade. (No search was
necessaryonSeptember17,2001butdecisionsonwhethertoholdor
exitbetswerecriticaltomanagerperformance.)Figure3.5illustrates
aforecastfunctioninwhichthehistoricaldevelopmentofthespread
isdiscardedinfavorofasinglenewobservation.Forecastuncertainty
wouldtypically belarge, illustratedby thewidelimits.
If no information is discovered, a reasonable action is to watch
closelyhowthespread developsover thenextfewdays (stilllooking

StructuralModels 43
Observation
Forecast
15 Forecast Uncertainty
10
5
0
−5
−10
1 1 1 1 1 1 1 1 1
29 33 37 41 45 49 53 57 61
FIGURE 3.5 Interventionforecastfunction
for fundamental news, of course). If the spread begins migrating
back to the pre-shift range, then no action is necessary. If the spread
continues to move around the newly established level, then the
model forecasts can be improved by introducing that knowledge
to the model. With the EWMA it is straightforward to make the
adjustment. By increasing the discount factor for just one period,
giving more weight to recent spread values, the forecasts quickly
become centered around the newly established level, as shown in
Figure 3.6. Judgments of the value of the open bet, and of new bets,
are improved much sooner than otherwise. The open bet is exited
sooner,onSeptember21,stillatalossbutthecapitalisfreedupand
thepositionriskeliminated.Profitablenewbetsarequicklyidentified
which, without the adjustment, would have been missed while the
routinemodelplayedcatchup:September27throughOctober2and
October8 through October10 fora combinedgain of $3.64.
Forecast monitoring and model adjustment are also feasible
with the MA model but the practicalities of the adjustment are
considerablymoreawkwardthantheone-timeuseofanintervention
discountfactorin the EWMA.Tryit and see!

44 STATISTICALARBITRAGE
15
10
5
0
−5
−10
1 1 1 1 1 1 1 1 1 1 1
29 33 37 41 45 49 53 57 61 65 69
FIGURE 3.6 Post-interventionforecasts
From where did the value of the intervention discount come?
Many sophisticated and fascinating control schemes exist in the
engineering literature, but for our purposes a simple calibration
procedure can be used. From a collection of spread histories, isolate
the points at which step changes in the spread occurred. Experiment
with a range of intervention discount factors until the pattern of
forecasts across all the cases is adequate. (Once more, subjective
terms such as ‘‘adequate’’are left to yourinterpretation.)
How large a spread is indicative of possible level shift? Look
again at your data: Three standard deviations from the mean occurs
how often? How many false monitor alarms would ensue with that
calibration? What about four standard deviations? How many level
shifts are missed? With what consequences for spread bets? It is
not useful to rely on probabilities of standard deviation moves for a
normaldistribution—3standarddeviationsfromthemeanoccurring
0.2 percent of the time—because spreads are typically not normally
distributed.Toseethis,formthedailyspreaddatafromyourfavorite
pair into a histogram, overlay the best fitting normal density curve
(matchthesamplemeanandvariance).Examinethequalityofthefit
in the tails and in the center of thedensity.

StructuralModels 45
1.5
1.0
0.5
0.0
−1.5 −1.0 −0.5 0.0 0.5 1.0 1.5
FIGURE 3.7 CAL–AMRspreadreturns,December2001toMay2002,with
normaldensity
Figure 3.7 illustrates a common situation. Daily returns from a
sample of six months of the CAL–AMR spread (December 2001
through May 2002) are displayed in a histogram; a normal den-
sity curve is fitted to the sample mean and standard deviation is
superimposed.I leave thecommentary to you.
Empirical experimentation is a sounder approach to developing
understandingthanblindassumptionofnormality,andagoodplace
fromwhichtobuildarepresentativeformalmodelifthatisyourgoal.
Chapter 5 debunks some common misconceptions about underlying
distributionsand reversion in time series data.
A more detailed discussion of forecast monitoring; intervention
and automatic adaptation schemes, including likelihood based tests
instead of the rudimentary standard deviation rules suggested here;
andevidenceaccumulationstrategiesisgiveninPoleetal.,1994.That
volume details the class of models known as dynamic linear models
(DLM) which contain as special cases MA and EWMA models,
and also autoregressive models that feature prominently in some
statisticalarbitrageurs’offerings.ThestructureoftheDLMprovides
fora rather richeranalysis than anythingdiscussed in thisvolume.

46 STATISTICALARBITRAGE
In Chapter 9, Section 2, a situation that practically screamed
for intervention is related: the forced liquidation of $4.4 billion in
October 2003 because of massive redemptions in response to the
New York attorney general’s investigation of Janus for mutual fund
market timing activities. Expected market reaction to the terrorist
attacks on the United States in September 2001 is a fine example of
the need for careful review and the value of well designed, selective
intervention.
Not all changes of level are as dramatic as in the preceding
example. Often a new level is reached after a migration over several
days rather than in a single, outsize leap. The British Petroleum
(BP)–Royal Dutch Shell (RD) spread shown in Figure 3.8 exhibits
several such migrations. Two EWMA forecast functions are illus-
trated. The first is a standard EWMA with discount factor 0.09
(which is similar to a moving average on 25 days except at times of
significant change where the MA lags the EWMA’s adjustment to
the data, as previously remarked), which adapts rather slowly to the
EWMA
8
EWMA with automatic trend adjustment
$
7
6
5
4
3
2
Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
2003
FIGURE 3.8 Trenddetectionandleveladjustment

StructuralModels 47
$4 change in spread level in the first quarter of 2003. The second
is an EWMA that switches to a high discount factor when a level
shift is detected to be underway. The increased pace of adaptation
is evident in the downward shift of the spread in February 2003,
the two subsequent shifts upward in April and June, and another
downward shiftin late July.
For this demonstration, the switching rule is quite crude: When
the spread exceeds a one standard deviation margin from the basic
EWMAforseveraldaysinsuccession,usethehighdiscountfactorfor
faster adjustment. (The local standard deviation is computed using
EWMAsmoothing.)
Before leaving the BP–RD spread, take another look. Over the
whole year, the spread exhibits a nicely controlled sinusoidal-like
variation about a mean of $5.What doyou makeof that?
3.4 CLASSICAL TIME SERIES MODELS
There are many books on the market that describe models for
characterizing time series and making forecasts. A few are listed in
thebibliographyandthoseareyourfirststoppingpointforadetailed
understanding of model forms, statistical estimation and forecasting
procedures, and practical guidance on data analysis and model
building. In this section we give heuristic descriptions of several
model types that have been successfully employed by statistical
arbitrageurs. The discussion will be grounded in the context of
the spread and reversion descriptions and archetypal underlying
processes (sinusoidaland popcorn).
3.4.1 Autoregression and Cointegration
Probably the most commonly applied time series model structure in
any field is the autoregressive model. Future values of a series are
projected as weighted averages of recently exhibited values in that
series. Examples already seen include the moving average and the
exponentiallyweighted movingaverage.
The autoregressive model of order p relates the series outcome
at time t to a linear combination of the p immediately preceding
outcomes:
y t = β 1 y t−1 +···+β t−p y t−p +(cid:3) t

48 STATISTICALARBITRAGE
The coefficients, β , or model parameters, are determined by estima-
i
tion from a set of observations of the series. The final term, (cid:3) is the
t
so-called‘‘errorterm’’ inwhichisconvenientlygathered allthevari-
ability that cannot readily be subsumed in the structural part of the
model. This is the term typically assumed to be normally distributed
when standard estimation methods are applied and properties of
parameter estimates orforecasts are discussed.
Autoregressive models often appear as ARIMA models, which
standsforautoregressiveintegratedmovingaverage.Theclassic,and
unsurpassed,referenceisBoxandJenkins(1976).Amovingaverage
model in this context is, confusingly, somewhat different from the
movingaveragepreviouslyencountered.Hereitisreallyashorthand
way of writing a very long moving average of a series past values
using a mathematical equivalence to an average of a few imaginary
terms. That is quite a mouthful as well as brain fag so we will not
pursueit here.
And what of the ‘‘integrated’’part? That is simply a differencing
operation applied to a series before investigating autoregression
structure.Forexample,dailydifferencesinprices,z = p −p inan
t t t−1
obviousnotation,mightexhibitautoregressionstructure.Themodel
for the raw price series is then called an integrated autoregression.
The EWMA forecast function, while originally developed in the
logical,dataanalyticwayforsmoothingvariableobservationsaswe
introduced it earlier, is actually derivable as the optimal forecast for
an integrated model.
Thisleadsnicelytocointegration.Oftenseveralseriesareobserved
tomovetogetherinwayssuggestiveofarelationship;commonsitua-
tionsinclude(a)oneseriesdrivinganother,and(b)severalseriesdriven
by common underlying processes. Multivariate forms of
ARIMAmodelscanrepresentverycomplicatedstructuresofthissort
includingcontemporaneousandlaggedfeedbackrelationships.
A structure familiar to spread modelers (but perhaps not known
by its technical name) is cointegration. Where two (or more) series
arenonstationaryindividuallybuttheirdifference(thespread,inour
context) is stationary (think of that as meaning ‘‘approximated in
good measure by an autoregression’’), the series are called cointe-
grated. The difference (and it may be a difference other than the
first though we will not pursue that here) is well modeled by an
autoregression.

StructuralModels 49
A related class of autoregression models provides parsimonious
structural forms for series with long-term serial correlation depen-
dencies. Long-term correlation can be directly captured by a very
high order autoregression, but estimation problems ensue because
of the high parameter count. Autoregressive fractionally integrated
moving average (ARFIMA) models overcome the parameter count
problem,essentially fittingARMA models to series after fractionally
differencing.
3.4.2 Dynamic Linear Model
All of the models discussed in the preceding section rely on a
considerable degree of stationarity in data series for their efficacy.
Model parameters are estimated over a long history of data and are
supposed to be unchanging. In financial practice, it is seldom that
relationships in data are even approximately unchanging for any
lengthoftime.Parameterupdatingproceduresareuniversal,refitting
models to moving windows of data, a commonly used (and useful)
device. The local mean and volatility calculations used in Chapter 2
exemplifytheprocedure.
Aflexiblemodelstructurethatdirectlyembodiestemporalmove-
mentindatadefiningqualities,localmeanforexample,isthedynamic
linear model. In the DLM, temporal change in model parameters is
explicitlyincludedthroughthespecificationofanevolutionequation.
Considera first orderautoregression:
y t = βy t−1 +(cid:3) t
in which the realizations of a series are composed of two parts:
a systematic propagation of a fixed portion of the immediate past
definedbytheparameterβ,andarandomaddition(cid:3) .Nowconsidera
t
flexiblegeneralizationof thatmodelinwhichthesystematicelement
propagated sequentially may vary in magnitude period by period.
The parameter β is now time indexed and its variation is strictly
formalized so that evolution is permitted but revolution is not.
The dynamic model is specified by two equations, one defining the
observationsequenceand onedefiningthesystematic evolution:
y t =β t y t−1 +(cid:3) t observation equation
β t =β t−1 +ω t system equation

50 STATISTICALARBITRAGE
In the system equation, the term ω is a random term that controls,
t
by the magnitude of its variance, how fast the regression coefficient
β can change. With ω identically zero, the dynamic model reduces
t t
to the familiar static model. With a ‘‘large’’ variance for ω , the
t
data series history is immediately discounted so that β = y /y .
t t t−1
Youmaybegintoseehowinterventioninthedynamiclinearmodel,
exemplifiedfortheEWMA modelin Section 3.3,is implemented.
The DLM includes ARIMA, EWMA, and regression models as
special cases, making it a rich, flexible class with which to work.
Monitoring and intervention strategies are readily defined for each
model component separately and in combination. See, Pole, et al.
forexamples.
3.4.3 Volatility Modeling
Volatilitymodelinghasanextensivepedigreeinquantitativefinance.
Use in statistical arbitrage is less direct than in derivative valuation
where most theoretical development and published applications are
seen, but it is nonetheless helpful. Consider just the simple spread
modeling that provides much of the background of the discussion in
this book: The variance of the return stream determines the richness
of potential bets (the basic viability of candidate raw material for a
strategy), variability of mark to market gains and losses while a bet
is extant (the risk profile of a strategy, stop loss rules), and return
stretchingby stochasticresonance(see Section 3.7).
Generalizedautoregressiveconditionalheteroscedastic(GARCH)
andstochasticvolatilitymodelsloomlargeinthemodelingofvolatil-
ities. The derivatives literature is replete with variants of the basic
GARCH model with acronyms ranging from AGARCH through
EGARCH to GJR GARCH, IGARCH, SGARCH and TGARCH.
GARCHmodelsarelinearregression modelswitha nonlinearstruc-
turalspecificationfortheerrorvariance.Theerrorvariance,inother
modelsassumedtobeaconstantoraknownfunctionofsomeaspect
of the model or time (see the discussion of variance laws in Pole,
et al.),isspecifiedtobealinearfunctionoftheerrorterminthebasic
regression function. Consider, again, the first-order autoregression
and nowadd a first-order GARCH component:
y t =βy t−1 +(cid:3) t , e t ∼ N(0,h t ),
h =α +α (cid:3)2
t 0 1 t−1

StructuralModels 51
Thenotation,e ∼N(0,h )meansthatthe(error)terme isassumed
t t t
toberandomlydistributedaccordingtothenormaldistributionwith
mean 0 and variance h . (The ‘‘TGARCH’’ model uses a Student t
t
distributionin place of the normal for smoother response to ‘‘large’’
deviations.) In this model, the disparity between a forecast and
the corresponding outcome feeds directly into subsequent forecast
variance. A large forecast error ‘‘forces’’ the model to anticipate
forthcoming large volatility. That, in turn, means that less weight
will be accorded to the next observation in updating parameter
estimates. Therefore, when a model with GARCH error structure is
fitted to data that exhibits volatility clusters (bursts of higher than
normalvolatility)theweightgiventothemorevariableobservations
in estimating the structural part of the model is reduced relative to
theweight given to lessvariable observations.
In contrast to weighted estimation procedures, which assume a
known functional form of variance variability (such as the ‘‘level to
the power 1.5’’ which arises often in product sales data being the
resultofacompoundPoissonprocess),theGARCHmodelestimates
the changing pattern of variation along with the structural part of
the model. The pattern of variability is not specified ahead of time,
but a rule of recognition is: Large forecast–outcome discrepancies
signifylarge volatility.
Modelsmayincludegreaterlagstructure—more(cid:3) t−k termsmuch
like higher order autoregression models for mean structure. Inter-
pretation of such models is difficult and, unsurprisingly, successful
applicationsare largely restricted to lowlag structures.
There is an enormous literature on GARCH models, begin-
ning with Engle’s 1982 paper, with applications in macroeconomics
and finance.
3.4.4 Pattern Finding Techniques
Exploiting persistent patterns of stock price behavior has been
approached directly through pattern finding procedures including
neural networks and wavelets. Wavelet analysis, a sort of local-
ized Fourier analysis, decomposes a time series into a collection of
locally orthogonal basis functions with weights appropriate to the
raw series in question. A neural network is a collection of weighted
transformation functions; there is no explicit temporal structure but

52 STATISTICALARBITRAGE
such structure is implicit in the transformation of the inputs (past
observations of a series) to theoutput(forecasts).
Neural networks are excellent tools for finding patterns in data.
Wherepatternsrecur,networkforecastscanbeextraordinarilygood.
A major drawback though is the lack of interpretability. While it is
possible to disentangle the transformations in a small network (at
most a single hidden layer, only a handful of nodes per layer, well
behaved transfer functions) and thereby attach theoretical under-
standing, this is not the routine situation. And what of that? If a
neural network successfully identifies predictive footprints in stock
price data, what does it matter if the intellectual grasp of the
input–output transformation is looser than a competitor’s model
built from autoregressions applied to (say) factor residuals (Section
3.6)?It may notmatterat all and weleave thecontentiousmatter to
yourconsideration.
A great advantage of neural networks is their flexibility, which
is the reason they are such good pattern identifiers to begin with.
When structural change occurs, neural networks can be very quick
to identify that a change is underway and subsequently characterize
newlystablepatterns.Theattendantdanger,alwaysapartnerofsuch
flexibility,isthatidentifiedpatternsmaybeephemeral,theirexistence
fleetingintermsofusableexploitationopportunities.Borrowingfrom
Orwell’s fancy: descriptionyes, predictionno.
3.4.5 Fractal Analysis
We refer the interested reader to the inventor, Benoit B. Mandelbrot
2004,who tellsit best.
3.5 WHICH RETURN?
Whichreturndoyouwanttoforecast?Theanswermayseemobvious
if you have a particular context in mind: Forecast return for today
and trade around that. In general the answer is not obvious outside
the context of theory, data analysis, and trading goals. Let’s assume
that thelatter is simplyto maximizestrategy return (subject to some
risk controls that will be left unspecified here). Without theoretical
guidance, we might proceed simply to explore some traditional time
scales, investigating patterns of daily, weekly, or monthly return.

StructuralModels 53
A littlemorethoughtmightsuggest investigatinghowreturnevolves
withduration:Examiningreturnsfor1,2,3,...,kdaysmightindicate
a natural time period for a particular type of series, whether it is
individual raw stock prices or functions thereof such as factors (see
Section 3.6); one might also want to examine the maximum return
over thenext m days.
Patternmatchingmodels,moreelaborateandtechnicallydemand-
ingthanthemodelsdiscussedinthisbook,leadonetoconsidermore
general, multivariatefunctionsofstockreturnseries.
3.6 A FACTOR MODEL
The modeling discussion thus far has focused on spreads between
pairs of stocks, the domain where statistical arbitrage, as pairs
trading, had its genesis. Now we will discuss some modeling
ideas applied to individual stock price series analyzed as a
collection.
The notion of common risk factors, familiar from Barra-type
models, lies at the heart of so-called factor models for stock returns:
The basic idea is that returns on a stock can be decomposed into
a part that is determined by one or more underlying factors in the
market(andincommonwithotherstocks)andapartthatisspecific
to thestock, so-called idiosyncraticreturn:
stock return = return to market factors+idiosyncraticreturn
Early models formed using this decomposition simply identified
marketfactorsasindustries(theS&Pindustrysectors)andageneral
marketfactor.Somemodelersusedindexesasproxiesforthefactors,
buildingmultipleregressionmodels,autoregressionmodels,orother
models for daily, weekly, or monthly returns; they also fashioned
forecasts from (a) forecast models for indexes (b) the constructed
regression (etc.) models,and built portfoliosaccordingly.
Later attempts used a more general model called a statistical
factor model. In a factor model, the factors are estimated from the
historical stock return data and a stock’s return may be dependent
on, or driven by, several of these factors.

54 STATISTICALARBITRAGE
3.6.1 Factor Analysis
A factor analysis of a multivariate data set seeks to estimate a
statistical model in which the data are ‘‘explained’’ by regression
on a set of m factors, each factor being itself a linear combination
(weighted average) of the observables.
Factor analysis has much in common with principal component
analysis (PCA) which, since it is more familiar, is good for compar-
ison. Factor analysis is a model based procedure whereas principal
componentanalysisisnot.PCAlooksatasetofdataandfindsthose
directions in observation space in which the data exhibits greatest
variation.Factoranalysisseekstoestimateweightsforasetoflinear
combinations of the observables—so-called factors—to minimize
discrepancybetween observationsand model fitted values.
If the distinction between PCA and factor analysis seems hazy,
good. It is. And we will say nomore aboutit.
Supposetheuniverseofstockshaspelements(stocks).Wemight
usefullyentertain thecomponentstocksof theS&P 500index (as of
a fixed date) as an orienting example. Pick a number of factors, m.
Given daily historicalreturnson the selected stock universe, a factor
analysis procedure will yield m factors defined by their respective
factor loadings. These loadings are weights applied to each of the
stocks. Thus, factor 1 has loadings l ,...,l . The other m − 1
1,1 1,500
factors similarlyhave theirown loadings.
Multiplyingtheloadingsbythe(unobserved)factorsyieldsvalues
for the returns. Thus, given the loadings matrix L, the columns of
whicharetheloadingsvectorsjustdescribed,estimatesofthefactors,
or factorscores, can be calculated.
So, after a factor analysis one has, in addition to the original
p stock return time series,m time series of factor estimates. It may
help to think of the parallel with industry index construction; some
statistical factors may look like industry indexes, and may even be
thought of that way. But keep in mind the important structural
distinction that statistical factors are a function solely of stock price
historywith no informationoncompany fundamentalsconsidered.
If onewere to regress the stock returns on the factors onewould
obtain a set of regression coefficients. For each stock, there is one
coefficientperfactor.Thesecoefficientsarethestockexposurestothe
factors.Byconstructionofthefactors,thereisnoothersetofmlinear
combinationsof the observables that can give a better regression for

StructuralModels 55
the chosen estimation criterion (most often maximum likelihood).
There are infinitely many equivalent sets, however. Strategies with
names such as varimax rotation and principal factors—related to
principal component analysis—are used to select a unique member
from thisinfiniteset.
Note that there is a duality between factor loadings and
stock exposures to factors. The duality, which is a consequence
ofthefactordefinitionandconstruction,issuchthat therowsofthe
loadings matrix are the stock exposures to the factors. That is, in
the p × m loadings matrix L, the element l is both the loading of
i,j
thejthfactorontheithstockandtheexposureoftheithstocktothe
jth factor.
What is the interpretation of a factor model? It is this: The
universe of p stocks is supposed to be a heavily confused view of
a much smaller set of fundamental entities—factors. Crudely, one
might suppose that the stock universe is really driven by one factor
called‘‘themarket.’’Lesscrudelyonemightsupposethat,inaddition
to the market, there are a dozen ‘‘industry’’ factors. The factor
analysis may then be viewed as a statistical procedure to disentangle
the structure—the factors—from the noisy image presented by the
full stock universe, and to show how the stock universe we observe
is constructedfromthe‘‘real’’ factor structure.
3.6.2 Defactored Returns
Anothersuccessfulmodelbasedonfactoranalysisreversedtheusual
thinking: Take out the market and sector movements from stock
returnsbeforebuildingaforecastmodel.Therationaleisthis:Tothe
extentthatmarketfactorsareunpredictablebutsentimentaboutthe
relativepositionof individualstocksisstableoverseveral days, such
filtered returns should exhibit more predictable structure. Let’s look
in a littlemoredetail at this interestingidea.
Residuals from the fitted regression model (stocks regressed on
estimated factors) will be referred to as defactored returns. It is
these defactored returns on which attention is focused. Why? The
notion is that return to a stock may be considered as being com-
posed of return to a set of underlying factors (market, industry,
or whatever other interpretation might be entertained) plus some
individualstock-specificamount.Forastockithismaybeexpressed

56 STATISTICALARBITRAGE
algebraically as:
r = r ,+···+r +r
i f1 fm si
For a market and industry neutral portfolio, it is the stock-specific
componentwhichremainsintheresidualofthestandardfittedmodel.
Moreover, the stock-specific component may be more predictable
than the others in the short term and following this construction.
For example, regardless of today’s overall market sentiment, the
relativepositions(value)ofasetofrelatedstocksarelikelytobethe
similar to what they were yesterday. In such situations, a portfolio
constructed from forecasts of ‘‘de-marketed’’ returns is still likely to
yield a positiveresult.
A simplified illustration may help to convey the essence of the
notion.Supposeamarketcomprisesjusttwostocksinroughlyequal
proportion (capitalization, value, price). On day t the return may
be denoted:
r = m +η ,
1,t t t
r = m −η
2,t t t
In this case, the factor model will include just one component and
historical data analysis will reveal the market to be essentially the
average of the two constituent stocks. (More generally, different
stocks will have different exposures to a factor—m would appear
t
weighted in the equations—but with weights intimately bound up
with the factor definition as already described.) In this case, the
stock-specific return will be of the same magnitude for each stock,
but signed differently. Now, if this quantity, η , can be predicted
t
better than by random guess, then regardless of the pattern of the
market return, a portfolio long stock 1 and short stock 2 (vice versa
when η isnegative) will, on average, yield a positivereturn.
In a more realistic situation, as long as many bets are made
and there is some forecast power in the defactored return model
(which may be a EWMA, autoregression, etc.), the trading strategy
should win. Making bets dependent on the size of forecast returns
andoptimizingselectedportfoliosforriskshouldimprovereturn/risk
performance.
Briefdetailsofthealgebraoffactoranalysisandtheconstruction
of the defactoredreturns model are given in Section 3.10.

StructuralModels 57
Operational Construction of Defactored Returns Factor loadings/expo-
sures must be updated periodically to maintain any reasonable
expectation of forecast (and hence trading) performance. Since the
statistical factors directly reflect (supposed) structure in the stock
price histories, it is not surprising to discover that the structure
is dynamic. Estimating factor relationships from stale data will
most likely produce results with unpromising forecast performance.
The selection of the frequency of factor updating is, like similar
dynamic model elements previously remarked on, a matter for the
investigator’s art. Quarterly or half yearly revision cycles are often
used.
Defactored returns must be calculated using the most recent
past set of loading estimates and not the contemporaneous set,
ensuring that the defactored return series are always defactored
out of sample. While this is deleterious for simulation results, it is
critical for strategy implementation. It is easy to pay lip service to
this commonly acknowledged matter but also easy in a complicated
model orestimation procedureto forget it.
A dynamic model, generalization of the DLM might be consid-
ered so that model parameters are revised each day according to a
structuralequation,buttheextracomputationalcomplexitywasnot
justified in the late 1980s. Today there is no such computational
concern and dynamic factor models have appeared in the statistical
literature with applications to stock price prediction. With these
complicatedmodelsitisincrediblyeasy,andtempting,toallowgreat
flexibility, unwittinglytaking a path to a model that does little more
than follow the data. More than one manager eventually fell victim
to theseduction,optimizedto oblivion.
3.6.3 Prediction Model
After all the work necessary to build the time series of defactored
returns for each stock, the modeler is still faced with constructing a
forecastmodelforthosereturns.Thatdoesnotimplyareturntofirst
basesincethatwouldmeanthattherationaleforthedefactorization
was void. Nonetheless, one is, as stated, faced with a forecast
model building task. One might consider autoregressive models,
for example. Note that cointegration models should presumably be
of little value here because common factors are supposedly removed
in thedefactorizationprocedure.

58 STATISTICALARBITRAGE
Many elaborations may be entertained. For instance, there may
bemorestabilityin factorestimationontimescaleswithgranularity
much longerthan oneday.
Thenaturalalternativeofbuildingaforecastmodelforthefactor
series and predicting those series may be entertained. However, this
would not replace the defactored return predictions: In the simple
example of the previous section, factor prediction is equivalent to
prediction of m (or a cumulative version thereof). The defactored
t
componentisstill present.
An unanswered question that arises in this consideration of
return forecasting is: What is the relationship between k-day ahead
cumulativestockreturnsandk-dayaheadfactorestimates?Fromthe
earlier discussion, another pertinent consideration is: If, as posited,
the market factors are more erratic than the defactored component,
then the forecasts will be less useful (in the sense that trading them
will yield more volatile results). These considerations indicate that
factor predictions are a secondary task for return exploitation (in
the context of a valid defactor model). However, factor prediction
models—defactor structured return model or not—are useful in
monitoring for market structural change and identifying the nature
and extent of such change.
3.7 STOCHASTIC RESONANCE
Withamodel-basedunderstandingofspreadorstockpricetemporal
dynamics, there is another crucial part of the process in which
analysiscandemonstrateexploitationpossibilities.Consideraspread
that may be characterized as a popcorn process: Occasionally the
spreaddepartsfromits(locallyintime)‘‘normal’’valuesubsequently
toreturntothatnormoverareasonablywelldefinedtrajectory.The
normallevelisnotconstant.Whennotsubjecttosomekindofmotion
inducingforcesuchasablocktrade,spreadsmeanderaroundalocal
average value, sometimes greater and sometimes less. This motion is
largelyrandom—itcan,atleast,besatisfactorilyconsideredrandom
inthepresentcontext.Knowingthatonceaspreadhas‘‘returned’’to
itsmeanitwillhenceforthexhibitessentiallyrandomvariationabout
that mean suggests that the reversion exit rule can be modified from
thebasic‘‘exitwhentheforecastiszero’’to‘‘exitalittleontheother

StructuralModels 59
side of the zero forecast from which the trade was entered.’’ Here
the ‘‘little’’ is calibrated by analysis of the range of variability of the
spreadinrecentepisodesofwanderingaboutthemeanbeforeittook
off (up or down). Volatility forecasting models, GARCH, stochastic
volatility, or other models may be usefulin this task.
The phenomenon of ‘‘noise at rest,’’ the random wandering
about the local mean just exemplified, is known as stochastic
resonance.
As you read the foregoing description, you may feel a sense of
deja vu. The description of modeling the variation about the mean
duringperiodsofzeroforecastactivityisquitethesameasthegeneral
descriptionofthevariationofthespreadoverall.Suchself-similarity
occurs throughout nature according to Benoit Mandelbrot, who
invented a branch of mathematics called fractals for the study and
analysis of such patterns. Mandelbrot, 2004, has argued that fractal
analysis provides a better model for understanding the movements
of prices of financial instruments than anything currently in the
mathematicalfinanceliterature.Itisunknownwhetheranysuccessful
trading strategies have been built using fractal analysis; Mandelbrot
himself does not believe his tools are yet sufficiently developed for
predictionof financialseries to befeasible.
3.8 PRACTICAL MATTERS
Forecasts of stock price movements are incredibly inaccurate. Take
this message to heart, especially if you have completed a standard
introductory course on statistical regression analysis. The tradi-
tional presentation proclaims that a regression model is not very
useful (some statisticians would say useless) if the R-square is less
than 70 percent. If you have not taken such a course and do not
know what an R-square is, no matter: Read on. The traditional
presentation is not wrong. It is just not appropriate to the situa-
tion we are concerned with here. Now, observing that your weekly
return regressions produced fitted R-squares of 10 percent or less,
perk up!
The key to successfully exploiting predictions that are not very
accurate is that the direction is forecast correctly somewhat better
than 50 percent of the time (assuming that up and down forecasts

60 STATISTICALARBITRAGE
areequallyaccurate).1 Ifamodelmakescorrectdirectionalforecasts
(50+(cid:3))% of the time, then the net gain is (50+(cid:3))−(50−(cid:3))% =
2(cid:3)% of the bets. This net gain can be realized if one can make a
sufficientnumberofbets.Thelattercaveatiscrucialbecauseaverages
are reliable indicatorsof performanceonlyin theaggregate.
Guaranteeing that 2(cid:3)% of one’s bets is the net outcome of a
strategy is not sufficient, by itself, to guarantee making a profit:
Thosebetsmustcovertransactioncosts.Andremember,itisnotthe
1The situation is actually more complicated in a manner that is advantageous to
a fund manager. Symmetry on gains and losses makes for a simple presentation
of the point that a small bias can drive a successful strategy; one can readily live
withrelativeoddsthatwouldcauseaphysiciannightmares.Thepracticaloutcome
of a collection of bets is determined by the sum of the gains minus the sum of
the losses. A big win pays for many small losses. The significance of this fact is
in directing a manager to construct stop loss rules (early exit from a bet that is
not working according to forecast expectation) that curtail losses without limiting
gains.Wherethisispossible,amodelwithseeminglytextbooksizedrelativeoddsin
favorofwinningforecastscanbeprofitablytradedwithinprescribedrisktolerances.
Technically, such rules modify the utility function of a model by altering the
characteristics of the outcome set by employing a procedure in which the forecast
modelisonlyoneofseveralelements.
A warning: Beware of being fooled by purveyors of tales of randomness.
A strategy that offers bets that typically generate a small loss and occasionally a
whopping gain sounds alluring when proffered as relief after a cunningly woven
web of disaster shown to seemingly inevitably follow plays where the odds are
conventionallyinfavorofwinning.Aftertheseexamplesofcatastrophearedepicted,
solaceisofferedintheguiseofanalternativecharacterizedbylowrisk(smalllosses)
with large gain potential. A crafty invocation of the straw man technique of
persuasion.Or,statisticulation,asHuffwouldcallit.
A fine artisan of the word weaves an impressing story of unavoidable doom
employing unimpeachable calculus of probability. Then, Pow! Batman saves the
‘‘WhatcanIdo?’’daywithataleoftheoccasionalbigwinboughtbyeasy-to-take
smalllosses.Acompletereversalofpattern.Thatcannot—canit?—butdispelthe
doominstantly.Oppositepatternmustbegetoppositeemotion.Joy!
Nowaboutthosesmalllosses.Lotsofsmalllosses.Totalupthosesmalllosses
and discover the shamelessly omitted (oops, I mean inadvertently hidden in the
detail) large cumulative loss over an extended period before the Batman surprise.
So what have we truly gotten? A few periods of glee before inevitablecatastrophe
supplanted with prolonged, ulcer inducing negativity, despondency, despair, and
(if you can stand the wait) possible vindication! It is still an uncertain game. Just
differentrules.
Therearemanykindsofrandomness.

StructuralModels 61
averagetransactioncostthatmustbecoveredbythenetgain.Itisthe
much larger total cost of all bets divided by the small percentage of
netgainbetsthatmustbecovered.Forexample,ifmymodelwins51
percent of the time, then the net gain is 51−49 = 2 percent of bets.
Thus,outof100bets(onaverage) 51willbewinnersand49willbe
losers. I make net 2 winning bets for each 100 placed. Statistically
guaranteed.Myfeeforplaying,though,isthefeeformakingall100
bets, not just the net 2. Thus, my 2 percent guaranteed net winners
must cover thecosts for all 100percent of thebets.
Statisticalforecastmodelscandomuchmorethansimplypredict
direction. They can predict magnitude also. Consider a first-order
autoregressivemodelforweeklyreturns,forexample:Thesizeofthe
return for next week is forecast explicitly (as a fraction of the return
forlastweek).Ifanestimatedstatisticalmodelhasanyvalidity,then
those magnitudes can be used to improve trade selection: Forecasts
thataresmallerthantradecostareignored.Nopointinmakingbets
that have expected gain less than thecost of thegame, isthere?
Now,whataboutallthatpredictioninaccuracywetalkedabout?
Ifpredictionsareokayonaveragebutlousyindividually,howcanwe
rely on individual forecasts to weed out trades with expected return
lowerthan tradecost? Won’twe throwaway tradesthat turn outto
beenormouslyprofitable?Andtaketradesthatreturnlessthancosts?
Indeed yes. Once again, it is the frequency argument that is
pertinenthere.Onaverage,thesetoftradesdiscardedasunprofitable
after costs has expected return lower than trade cost. Also, on
average, the set of retained trades has expected return greater than
trade cost. Thus, the statistically guaranteed net gain trades have
expected return greater than trade cost.2
3.9 DOUBLING: A DEEPER PERSPECTIVE
It is tempting after an extended discussion of technical models, even
at the limited descriptive level of this chapter, to be seduced into
2Recall footnote 1, on improving the outcome of a forecast model by imposing a
bet rationing (stop loss) rule. Such a procedure increases the average gain of bets
madeaccordingtotheforecastmodel,soonemightsqueezejustalittlemorefrom
anopportunitysetbyrealizingthatreturnbiascanconvertsomerawlosingtrades
(thosewithaveragegainlessthantransactioncost)intowinningtrades.Subtle.And
nice.SeealsothediscussionofstochasticresonanceinSection3.7.

62 STATISTICALARBITRAGE
forgetting that models are wrong. Some are useful and that is the
context in which we use them. When applying a model, an activity
of signal urgency and import is error analysis. Where and how a
model fails informs on weaknesses that could be ameliorated and
improvementsthat might be discovered.
In Chapter 2 we introduced ‘‘Rule 3,’’ a bet doubling scheme
in which a spread bet was doubled if the spread became suffi-
ciently large. The idea was motivated by observing spread patterns
in the context of an already formulated model, Rule 1 or 2—this
is error analysis notwithstanding the quasi informality of rule posit-
ing based on eyeballing data rather than formal statistical model
building.
With more complicated models, eyeball analysis is infeasible.
Then one must explicitly focus upon the results of trading a model,
either in practice (with dollars at risk) or synthetically, (using simu-
lations).Beyondthestandardfareofcomparingforecast returnwith
outcome one can examine the trajectory of bet outcome from the
point of placement to the point of unwinding. In the example of
the spread doubling the typical trajectory of cumulative return on
the original bet is a J curve: Losses at first are subsequently recov-
ered then (the doubling phase) profits accrue. Trade analysis from
any model, regardless of complexity, can reveal such evolutionary
patternsand,hence,providerawmaterialforstrategyenhancements
such as doubling.
Notice how the dynamic of the trade, not the identification
of placement and unwind conditions, reveals the opportunities in
this analysis. Dynamics, trade and other, are a recurring theme in
this text. While the end result is what makes it to the bank and
investor reports, dynamics of how the result is made are critical
for identifying problems and opportunities. They are also important
to understand from the perspective of explaining monthly return
variability to investorswhen tradesextend over calendar month-end
boundaries.
Figure 3.9 shows the archetypal trio of trade cumulative return
trajectories:(a)gainfromtradeinceptiontounwinding;(b)lossfrom
inceptiontotradecancellation;(c)theJ-curveofinitiallossfollowed
byrecoveryandgain.Analysisofcollectionsoftradesineachcategory
can reveal possibilities for strategy improvement. Imagine what you
would do with the discovery of a distinct characterization of price

StructuralModels 63
(a)
(b)
time from trade inception
nruter
(c)
FIGURE 3.9 Archetypaltradecumulativereturntrajectories
and volume historyimmediatelyprecedingtrade signals that divided
prospectivetradesinto thethree categories.3 Imagine.
3.10 FACTOR ANALYSIS PRIMER
The following material is based on the description of factor analysis
in The Advanced Theory of Statistics, Volume 3, Chapter 43, by Sir
Maurice Kendall, Alan Stuart, and Keith Ord (now called Kendall’s
Advanced Theory of Statistics [KS]). The notation is modified from
KS so that matrices are represented by capital letters. Thus, γ in KS
is (cid:8) here. This makes usage consistentthroughout.
Suppose there are p stocks, returns for which are determined
linearlyfrom values of m < p unobservablefactors:
(cid:1)m
r = l f +µ +(cid:3), j = 1,...,p
j jk k j j
k=1
3This type of research has received considerable attention in seismology where
predicting earthquakes remains a research priority for several countries, recently
highlighted by the tsunami death toll of over 200,000 from the December 2004
eventintheIndianOcean.

64 STATISTICALARBITRAGE
where the (cid:3)s are error terms (observation error, model residual
structure). The coefficients l are called factor loadings. The variable
means µ are usually subtracted before analysis. In our case, we
j
assume that returns have mean zero so that µ = 0. In matrix form:
j
r L f µ (cid:3)
= + +
(p×1) (p×m)(m×1) (p×1) (p×1)
where L is the p × m matrix of coefficients {l }. (Note that this
ij
expressionisforonesetofobservations;thatis,thesetofreturnson
p stocksfor a singleday.) Nowassume:
1. That the f’s are independent normal variables with zero mean
and unit variance
2. That each (cid:3) is independent of all other (cid:3)s and of all the fs and
j
has variance (orspecificity) σ2
j
It followsthat:
(cid:1)m
cov(r,r )= l l , j (cid:3)= k,
j k jt kt
t=1
(cid:1)m
var(r)= l2 +σ2
j jt j
t=1
These relationships may be expressed succinctly in vector/matrix
form as:
(cid:8) = LL (cid:4)+(cid:10)
where (cid:10) is the p × p matrix diag(σ2,...,σ2).
1 p
From the data, we observe empirical values of (cid:8). The objectives
are to determine the number of factors, m, and to estimate the
constants in L and (cid:10). Determination of m is highly subjective; it
is like choosing the number of components in principal component
analysis. Indeed, PCA is often used to get an initial estimate of m,
whichmayberefinedbylikelihoodratiotestingandresidualanalysis
of the m-factormodel.In what follows,assume that m is fixed.

StructuralModels 65
Insomecases,interestisontheimpliedfactorscoresforparticular
days in a sample. That is, given returns r = (r ,...,r ) (cid:4) on day
,t 1,t p,t
t, what are the implied values f = (f ,...,f ) (cid:4) for the m factors?
,t 1,t m,t
If L and (cid:10) are known, generalized least squares estimation of f is
,t
obtainedby minimizing:
(r −µ−Lf ) (cid:4) (cid:10) −1(r −µ−Lf )
,t ,t ,t ,t
Note that the mean stock return vector, µ, is assumed to be zero.
(Recall that µ is the mean return of stock j; µ is not the mean stock
j
return on day t.) Thesolutionof theminimizationis:
f ˆ = J −1L (cid:4) (cid:10) −1r
,t ,t
whereJ = L (cid:4) (cid:10) −1L.Inpractice,Land(cid:10) areunknown;theMLEsare
substituted.
An alternative estimator for the factor scores is given in S.J.
Press, Applied Multivariate Analysis, Section 10.3. (Our notation is
used for consistency herein.) Essentially, he assumes away the error
covariances when themodel is restated as:
f = Ar +u , t = 1,...,n
,t ,t ,t
where the factor scores at time t are linear combinations of the
stock returns at that time. A subsequent appeal to a large sample
approximationresults in the estimator:
f ˆ = Lˆ(cid:4) (nRR (cid:4) ) −1r
,t ,t
3.10.1 Prediction Model for Defactored Returns
In the model described in Section 3.6, interest is in the defactored
returns. For day t, the set of defactored stock returns is defined as
the difference between the observed set of returns and the weighted
factorscores (where theweightsare, of course,the factorloadings):
dfr = r −Lˆ(cid:4) f ˆ
,t ,t ,t
This vector of defactored returns, computed for each day in the
sample, provides the raw time series from which the prediction

66
STATISTICALARBITRAGE
| model    | is constructed. |     | In     | an autoregressive |     | model, | for example, | the |
| -------- | --------------- | --- | ------ | ----------------- | --- | ------ | ------------ | --- |
| entry in | theregression   |     | forday | t forstock        |     | j is:  |              |     |
(cid:1)k
|     | dfr |       | = β | dfr +···+β |     | dfr         | +(cid:3) |     |
| --- | --- | ----- | --- | ---------- | --- | ----------- | -------- | --- |
|     |     | j,t−a |     | 1 j,t−k    |     | q j,t−k−q+1 |          | j,t |
a=1
| This equation |                | states | that           | the k-day          | cumulative | defactored     |              | return to |
| ------------- | -------------- | ------ | -------------- | ------------------ | ---------- | -------------- | ------------ | --------- |
| day t is      | regressed      | on     | the            | q daily defactored |            | returns        | immediately  | pre-      |
| ceding        | the cumulation |        | period.        | Notice             | that       | the regression | coefficients |           |
| are common    |                | across | stocks.        |                    |            |                |              |           |
| The           | forecast       | of     | the k-day      | ahead              | cumulative | defactored     |              | return at |
| theend        | of day         | t is   | constructedas: |                    |            |                |              |           |
(cid:1)k
|     |     |     |       | = βˆ      | +···+βˆ |               |     |     |
| --- | --- | --- | ----- | --------- | ------- | ------------- | --- | --- |
|     |     | dfr | j,t+a | 1 dfr j,t |         | q dfr j,t−q+1 |     |     |
a=1
| Other    | forecast |            | models | may be | employed: | ‘‘You | pay your | money |
| -------- | -------- | ---------- | ------ | ------ | --------- | ----- | -------- | ----- |
| and take | your     | chances.’’ |        |        |           |       |          |       |

4
CHAPTER
Law of Reversion
Nowhere, you see it takes all therunningyou can do, to
keep in thesame place.
—ThroughtheLookingGlass, Lewis Carroll
4.1 INTRODUCTION
In this chapter, we begin a series of four excursions into the the-
oretical underpinnings of price movements exploited in statistical
arbitrage.Thefirstresult,presentedinthischapter,isasimpleprob-
abilitytheoremthat evincesabasiclawguaranteeingthepresenceof
reversion in prices in an efficient market. In Chapter 5 a common
confusion is cleared up regarding the potential for reversion where
pricedistributionsareheavytailed.Insummary,reversionispossible
withanysourcedistribution.Followingthatclarification,wediscuss
in Chapter 6 definitionand measurement of interstockvolatility, the
variation which is the main course of reversion plays. Finally in this
theoreticalseries, wepresentinChapter7 atheoreticalderivationof
howmuch reversion can beexpected fromtradinga pair.
Together these four chapters demonstrate and quantify the
opportunity for statistical arbitrage in ideal (not idealized) mar-
ket conditions. The material is not necessary for understanding the
remainderofthebook,butknowledgeofitwillamplifyappreciation
of the impact of market developments that have led to the practi-
cal elimination of the discipline of statistical arbitrage in the public
domain.
67

68 STATISTICALARBITRAGE
4.2 MODEL AND RESULT
We present a model for forecasting prices of financial instruments
thatguarantees75percentforecastingaccuracy.Thechosensettingis
predictionaboutthedailyspreadrangeofapairbutalittlereflection
will reveal a much wider applicability. Specifically, we focus on
predicting whether the spread tomorrow will be greater or smaller
than thespread today.
The model is quitesimple. If the spread today is greater than the
expected average spread, then predict that thespread tomorrowwill
be smaller than the spread today. On the other hand, if the spread
today was less than the expected average spread, then predict that
thespread tomorrowwill be greater than the spread today.
4.2.1 The 75 Percent Rule
The model just described is formalized as a probability model as
follows. Define a sequence of identically distributed, independent
continuous random variables {P ,t = 1,2,...} with support on the
t
nonnegativereal lineand median m. Then:
Pr[(P t > P t−1 ∩P t−1 < m)∪(P t < P t−1 ∩P t−1 > m)] = 0.75
In the language of the motivating spread problem, the random
quantityP isthespreadondayt(anonnegativevalue),anddaysare
t
consideredtobeindependent.Thetwocompoundeventscomprising
the probability statement are straightforwardly identified with the
actionsspecifiedintheinformalpredictionmodelabove.Butaword
isinorderregardingthedetailsofeachevent.Itiscrucialtonotethat
each event is a conjunction, and, and not a conditional, given that,
as might initially be considered appropriate to represent the if–then
nature of the informal model. The informal model is a prescription
of the action that will be taken; the probability in which we are
interested is the probability of how often those actions (predictions)
will be correct. Thus, looking to expected performance, we want to
knowhowoftenthespreadonagivendaywillexceedthespreadon
the previous day when at the same time the spread on that previous
day does not exceed the median value. Similarly, we want to know
how often the spread on a given day will not exceed the spread on

LawofReversion 69
the previous day when at the same time the spread on that previous
day exceeds the median.
Those distinctions may seem arcane but proper understanding
is critical to the correct evaluation of expected result of a strategy.
Suppose that on eight days out of ten the spread is precisely equal
to the median. Then the scheme makes a prediction only for 20
percent of the time. That understanding flows directly from the
conjunction/disjunction distinction. With the wrong understanding
a five-to-one ratio of expected return to actual return of a scheme
wouldensue.
Operationally,onemaybetontheoutcomeofthespreadtomor-
row once today’s spread is confirmed (close of trading). On those
days for which the spread is observed to be greater than the median
spread, the bet for tomorrow is that the exhibited spread tomorrow
will be less than the spread seen today. The proportion of winning
betsin such a schemeis theconditionalgiven that probability:
3
Pr[P t+1 < P t |P t >m] =
4
Similarly, bets in the other direction will be winners three quarters
ofthetime.Doesthismeanthatwewin‘‘1.5ofthetime?’’Nowthat
reallywouldbeastatisticalarbitrage!Themissingconsiderationisthe
relative frequency with which the conditioning event occurs. Now,
P <moccurshalfofthetimebydefinitionofthemedian.Therefore,
t
halfofthetimewewillbetonthespreaddecreasingrelativetotoday
and of those bets, three quarters will be winners. The other half of
the time we will bet on the spread increasing relative to today and
of those bets, three quarters will also be winners. Thus, over all
bets, three quarters will be winners. (In the previous illustration, the
conditioning events occur only 20 percent of the time and the result
wouldbe 3 × 1 orjust 3 .)
4 5 20
Before proceeding to the proof of the result, note that the
assumptionof continuityis crucial (hence theemphasisin themodel
statement). It is trivial to show that the result is not true for discrete
variables (see thefinal part of thissection).
4.2.2 Proof of the 75 Percent Rule
The proof of the result uses a geometric argument to promote
visualization of the problem structure. An added bonus is that one

70
STATISTICALARBITRAGE
| P   |     |     |     |     |     |     | P  = P t−1 |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- |
|     | t   |     |     |     |     |     | t          |     |     |
 < P
|     |     | P t−1 | t   | 1   |     |            |     |     |     |
| --- | --- | ----- | --- | --- | --- | ---------- | --- | --- | --- |
|     |     |       |     |     |     | P t−1  > P |     |     |     |
t
(b)
median
(a)
2
|            |                              |     | median |     |      |     | P t−1 |     |     |
| ---------- | ---------------------------- | --- | ------ | --- | ---- | --- | ----- | --- | --- |
| FIGURE 4.1 | DomainofjointdistributionofP |     |        |     | andP |     |       |     |     |
|            |                              |     |        |     | t    | t−1 |       |     |     |
canseethatcertainstructuralassumptionsmadeinthetheoremmay
berelaxed.Theserelaxationsarediscussedfollowingtheproofofthe
basic result.
| Consider  |     | the joint | distribution |     | of two        | consecutive |              | terms | of the  |
| --------- | --- | --------- | ------------ | --- | ------------- | ----------- | ------------ | ----- | ------- |
| sequence, | P   | and P     | . Assuming   |     | independence, |             | the contours |       | of this |
|           | t−1 |           | t            |     |               |             |              |       |         |
=
| jointdistributionare |     |     | symmetric(aboutthelineP |     |     |     | P t−1 | ) regardless |     |
| -------------------- | --- | --- | ----------------------- | --- | --- | --- | ----- | ------------ | --- |
t
| of the precise |     | form of | the underlying |     | distribution. |     | In particular, |     | it is |
| -------------- | --- | ------- | -------------- | --- | ------------- | --- | -------------- | --- | ----- |
notnecessarytoassumethatthedistributionhasasymmetricdensity
function.
| Consider |     | Figure | 4.1. The | domain | of  | the joint | distribution |     | (the |
| -------- | --- | ------ | -------- | ------ | --- | --------- | ------------ | --- | ---- |
positivequadrantof(cid:3)2
includingthezeroboundaries)ispartitioned
| in both | dimensions |     | at the | median | point. | By  | the definition |     | of the |
| ------- | ---------- | --- | ------ | ------ | ------ | --- | -------------- | --- | ------ |
median,thefourquadrantssoconstructedeachrepresent25percent
of the jointdistribution.
| The | lower | left and | upper | right | quadrants |     | are bisected |     | radially |
| --- | ----- | -------- | ----- | ----- | --------- | --- | ------------ | --- | -------- |
fromthejointmedianbytheaxisofsymmetry.Now,thesymmetryof
thedensitycontours—resultingfromindependent,identicalmarginal
| distributions—means |              |          | that              | both | halves   | of each        | quadrant | cover    | the    |
| ------------------- | ------------ | -------- | ----------------- | ---- | -------- | -------------- | -------- | -------- | ------ |
| same total          | probability. |          | Therefore,        |      | each     | half-quadrant  |          | accounts | for    |
| 12.5percent         | of           | thetotal | jointprobability. |      |          |                |          |          |        |
| The                 | remainder    | of       | the proof         |      | consists | of identifying |          | on the   | figure |
thoseregionscorrespondingtotheunionintheprobabilitystatement
madeearlier.Thisisclearlyandpreciselytheunionofshadedregions

LawofReversion 71
(a) and (b), which is the domain of the joint distribution excepting
unshaded regions (1) and (2). The latter regions each account for
12.5 percent of the total joint probability as shown in the previous
paragraph. Therefore, the union of regions (a) and (b) represents
exactly threequartersof thejointprobability.
It is worth noting at this point that we did not decompose the
upper left or lower right quadrants. Fortunately, it is not necessary
to do so since thereis no specificresult forthegeneral case.
4.2.3 Analytic Proof of the 75 Percent Rule
The purpose of giving a geometric argument is to facilitate under-
standing of generalizations of the result that will be presented in
the next section. Before proceeding thereto, we establish the result
analytically. Write X = P t and Y = P t−1 to simplify notation. The
two events:
{X < Y ∩Y > m} and {X > Y ∩Y < m}
are disjoint (easily seen from the fact that Y > m and Y < m cannot
occur simultaneously: On the graph, regions (a) and (b) do not
overlap), so the probability of the disjunction is simply the sum of
theindividualprobabilities.Considerthefirstpartofthedisjunction:
(cid:1) (cid:1)
∞ y
Pr[X < Y ∩Y >m] = f (x,y)dxdy
XY
m −∞
where f (x,y) denotes the joint density function of X and Y. By
XY
the assumption of independence,the joint density is just the product
of the individual marginal densities, which in this case are identical
(also by assumption). Denoting the marginal density generically by
f(.) and itscorrespondingdistributionby F(.),proceed as follows:
(cid:1) (cid:1) (cid:1) (cid:1)
∞ y ∞ y
f (x,y)dxdy= f(x)f(y)dxdy
XY
m −∞ (cid:1)m −∞
∞
= F(y)f(y)dy
(cid:1)m
∞
= F(y)dF(y)
m

72 STATISTICALARBITRAGE
The last step is simply recognition that the density function of
a random quantity is the analytic derivative of the corresponding
distributionfunction.Theremainingsteps are trivial:
(cid:1) (cid:2)
∞ (cid:2)∞
F(y)dF(y)= 1 F(y)2 (cid:2)
(cid:2)
2
m m
(cid:3) (cid:6)
(cid:4) (cid:5)
1 2
= lim F(t) −F(m)2
2 t→∞
(cid:7) (cid:10)
(cid:8) (cid:9)
1 1 2
= 1−
2 2
3
=
8
For the second part of the disjunction, the result follows from a
similar argument after an initial algebraic simplification. First, note
that the event Y < m may be expressed as the union of two disjoint
events:
Y < m≡ {(X > Y)∩(Y < m)}∪{(X < Y)∩(Y < m)}
By definition (recall that m is the median of the distribution), the
probability of the event Y < m is one half. Therefore, using the fact
that probabilitiesfordisjointeventsare additive,we may write:
1
Pr[X>Y ∩Y < m] = −Pr[X < Y ∩Y < m]
2
Now, proceedingmuch as for thefirst part:
(cid:1) (cid:1)
1 m y
Pr[X>Y ∩Y < m]= − f (x,y)dxdy
XY
2 −∞ −∞
(cid:1)
1 m
= − F(y)dF(y)
2 −∞
(cid:7) (cid:10)
(cid:8) (cid:9)
1 1 2
= − F(m)2− lim F(t)
2 2 t→−∞

LawofReversion 73
(cid:7) (cid:10)
(cid:8) (cid:9)
1 1 1 2
= −
2 2 2
3
=
8
Addingtheprobabilitiesof thetwo partsyieldsthe result.
4.2.4 Discrete Counter
Consider a random variable that takes on just two distinct values,
a and b, with probabilities p and 1 − p, respectively. Whenever
p (cid:7)= 1, the probability of the random variable exceeding the median
2
is also not equal to one half! Notwithstanding that minor oddity,
examine the probabilities of the two events comprising the theorem
statement:
{X < Y ∩Y >m} and {X>Y ∩Y < m}
In thisdiscreteexamplethese events are specifically:
{X = a∩Y = b} and {X = b∩Y = a}
which each have probability p(1 − p), hence, the probability in
the theorem is 2p(1 − p). The maximum value this probability can
assume is 1 when p = 1 (differentiate,equateto zero, solve).
2 2
4.2.5 Generalizations
Financial time series are notorious for the tenacity with which they
refuse to reveal underlying mathematical structure (though Mandel-
brot, 2004, may demur from that statement). Features of such data,
which often show up in statistical modeling, include: nonnormal
distributions (returns are frequently characterized by leptokurtosis);
nonconstantvariance(marketdynamicsoftenproduceburstsofhigh
and low volatility, and modelers have tried many approaches from
GARCH and its variants to Mandelbrot’s fractals, see Chapter 3);
andserialdependence.Theconditionsofthetheoremcanberelaxed
to accommodateall of thesebehaviors.

74 STATISTICALARBITRAGE
The result extends to arbitrary continuous random variables
directly:Theconstraintofsupportonthenonnegativereallineisnot
required. In the geometric argument, no explicit scaling is required
for the density axes (the zero origin is convenient for explication).
In the analytic argument, recall that we did not restrict the region of
supportof thedensities.
Note that if the underlying distribution has a symmetric density
function (implying either that the support is the whole real line
or a finite interval), then the pivotal point is the expected value
(mean)ofthedensityifitexists.TheCauchydistribution,sometimes
appropriate for modeling daily price moves, does not have a defined
expectedvalue,butitdoeshaveamedianandthestatedresultholds.
The 75 percent rule is extended for nonconstant variances in
Section 4.3.
Theindependenceassumptionisstraightforwardlyrelaxed:From
the geometric argument, it is only necessary that the contours of
the joint distribution be symmetric. Therefore, the independence
condition in the theorem can be replaced by zero correlation. An
analytical treatment, with examples, is presentedin Section 4.4.
Finally, generalizing the argument for the nonconstant variance
caseextendstheresultsothatthespreaddistributionmaybedifferent
every day, providing that certain frequency conditions are satisfied.
Details are given in Section 4.5.
4.3 INHOMOGENEOUS VARIANCES
Spreads are supposed to be generated independently each day from
a distribution in a given family of distributions. The family of
distributions is fixed but the particular member from which price is
generated on a given day is uncertain. Members of the family are
distinguishedonlybythevariance.Propertiesoftherealizedvariance
sequencenowdeterminewhat can be said about thepriceseries.
Whatcanbesaidifthevariances,daytoday,exhibitindependent
‘‘random’’ values? Then spreads will look as if drawn from, not a
memberoftheoriginalfamily,butfromanaverageofallthemembers
of the family where the averaging is over the relative frequencies of
the possible variances. In other words, the spread on day t is no
longer generated from F for a given σ but from the integrated

LawofReversion 75
distribution:
(cid:1)
F (p)= F (p)dσ
P σ
For example, suppose that the family of variance conditional distri-
butions is the normal family (with constant mean in this context)
and that the variances occur randomly as if generated from an
inverse gamma distribution; then spreads will look as if they were
generated by the Student t distribution. The key to the result
is the random element; it guarantees (probabilistically) that the
daily transitions look as if the underlying spread model is Student
t. (This point is expanded upon in Section 4.5 where a simi-
lar argument proves the result for arbitrarily different generating
distributions day-to-day. An extended discussion of the relation-
ship of marginal distribution to a time series of values is given
in Chapter 5.)
We can therefore state that the 75 percent rule is true in the case
of inhomogeneousvariance sequences.
Note that the distributions for spread (conditional on variance)
and for (unconditional) variance need not be of mathematically
convenient forms as used in the previous example. Any regular
(‘‘well behaved,’’ in terms of continuity) distributions will yield
the 75 percent result. There is no requirement for the density or
distribution function to be expressed in a closed form mathematical
expression.
4.3.1 Volatility Bursts
Autoregressive conditional heteroscedastic (ARCH) models (Engle,
1982)wereintroducedtocapturetheobservedclusteringofvariances
in macro economic data. In the past few years ARCH and GARCH
modelshavebeenheavilyused intheeconometricandfinancelitera-
ture,thelatterbecauseoftheoftremarkedphenomenonofvolatility
bursts. Most such bursts are of increased volatility from a regular
level, typically associated with bad news about a company. Histor-
ically, bursts of low volatility are less frequently experienced. Since
early 2003, however, volatility of stocks on the U.S. exchanges has
beendeclining.Spreadvolatilityreachedunprecedentedlowsin2003

76 STATISTICALARBITRAGE
and 2004; implications of that development for statistical arbitrage
are examined in Chapter9.
Whenvolatilityexhibitsbursts,variancesarenotgeneratedinde-
pendentlyeachdaybutexhibitserialcorrelation.The75percentrule
stillholdsbythisargument:Withinaburst,thetheoremappliesasif
thesituationwere(approximately)constantvariance.Therefore,only
the transition days could alter the result. There are comparatively
fewsuchdays,sotheresultwillstandtoaverycloseapproximation.
In fact, the result can be shown to hold exactly: The transitions
are irrelevant—see the argument in Section 4.5 for the general
nonconstant variance case. Chapter 5 presents analysis of related
patterns.
4.3.2 Numerical Illustration
Figure 4.2(a) shows the histogram of a sample of 1,000 values
generated from thenormal–inverseGamma scheme:
σ2 ∼ IG[a,b],
t
P ∼ N[0,σ2]
t t
First,generateanindependentdrawingofσ2fromtheinverseGamma
t
distribution (with parameters a and b—the actual specification of a
(a) Prices from normal-inverse gamma model; T_5 superimposed
1.5
1.0
0.5
0.0
−3 −2 −1 0 1
(b)
1
0
−1
−2
−3
0 200 400 600 800 1000
FIGURE 4.2 Randomsamplefromnormal–inverseGammamodel

LawofReversion 77
andb doesnotmatter: Anynonnegativevalueswilldo).Then,using
thisvalueofσ2,generateavalueforP fromthenormaldistribution
t t
with mean 0 and variance σ2. Superimposed on the histogram is the
t
densityfunctionoftheStudenttdistribution,whichisthetheoretical
marginaldistributionofspreadshere.Figure4.2(b)showsthesample
as a time series.
The proportion of one-day moves in the direction of the median
is 75.37percent, satisfyingly in accord with the rule.
4.4 FIRST-ORDER SERIAL CORRELATION
The result can be extended to the case of correlated variables. The
simplestcasetoconsideristhatofdistributionswithsymmetricden-
sity functions, since then the contours are circles (uncorrelated) or
ellipses (correlated). In the latter case, one can see that by dividing
up (cid:3)2 into quadrants along the major and minor axes of the con-
tours, then bisecting those quadrants radially from the joint median
pointaspreviously,oneisleftwithequiprobableregionsonceagain.
(Recall that, with symmetric densities, all quadrants are probablisti-
callybisectedthisway,notjustthosecorrespondingtothelowerleft
and upper right in the rotated coordinates.) The remaining task is
to identify the half quadrants with a correct statement (like the one
with which the original result was stated) in terms of the random
quantities. The result is easily seen by example. Suppose that P and
t
P t−1 have covariance c. Define a new variable as a linear combina-
tion of the correlated variables, Z t = a(P t −rP t−1 ). The coefficient r
is set to:
r = cov[P t ,P t−1 ]
var[P t−1 ]
(which is just the correlation between P t and P t−1 ) in order to make
P t−1 and Z t uncorrelated; the scale factor a is chosen to make the
variance of Z equal to thevariance ofP :
t t
a = (1−r2) −1 2
Now the theorem applies to P t−1 and Z t providing that Z t has the
same distributionas P t−1 , so that we have:
Pr[(Z t < P t−1 ∩P t−1 >m)∪(Z t >P t−1 ∩P t−1 < m)] = 0.75

78 STATISTICALARBITRAGE
Substitutingfor Z converts the expression into a form involving the
t
original variables:
Pr[(aP t −arP t−1 >P t−1 ∩P t−1 >m)
∪(aP t −arP t−1 >P t−1 ∩P t−1 < m)] = 0.75
Rearrangement of terms gives the requiredexpression:
Pr[(P t < (a −1+r)P t−1 ∩P t−1 >m)
∪(P t >(a −1+r)P t−1 ∩P t−1 < m)] = 0.75
Clearly, the case of zero correlation, equivalently r= 0 anda = 1,
with which we began isa special case of thismore general result.
The boundary, P t = (a −1+r)P t−1 , partitions the quadrants of
(cid:3)2 in proportions determined by the size of the correlation. In the
uncorrelated case, the quadrants are bisected √as we saw earlier.
Figure 4.3 shows the relationship(cid:11)of a −1+r = 1−r2+r with r.
√
The maximum, 2, occurs at r = 1 (easily shown analytically by
2
theusualprocedureofdifferentiating,equatingtozero,andsolving).
1.5
1.0
0.5
0.0
−0.5
−1.0
−1.0 −0.5 0.0 0.5 1.0
r
r
+
)2r
−
1(
(cid:12)
FIGURE 4.3 rversus (1−r2)+r

LawofReversion 79
It is important not to lose sight of the additional constraint
introduced in the argument here. The theorem applies to correlated
variables providing that a linear combination of variables with the
stated marginal distribution retains that distributional form. This is
true of normal variables, bivariate Student t variables, and lots of
others. Butit is not truein general.
AtthelimitwhenP t andP t−1 areperfectlycorrelated(r→1,a→
∞)theresultbreaksdown.Failureiscausedbythesingularityasthe
original two degrees of freedom (two distinct days or observations)
collapse into a single degree of freedom (two days constrained to
have the same price so the reversion statement of the theorem is
impossible).
4.4.1 Analytic Proof
The frequency of one-day moves in the direction of the median is
given by theprobability:
Pr[(P t < P t−1 ∩P t−1 >m)∪(P t >P t−1 ∩P t−1 < m)]
Considerthe first part of the disjunction:
(cid:1)
∞
Pr[P t <P t−1 ∩P t−1 >m]= Pr[P t < P t−1 ∩P t−1 = p]dp
(cid:1)m
∞
= Pr[P t <P t−1 |P t−1 = p]Pr[P t−1 = p]dp
(cid:1)m
∞
= Pr[P t < p|P t−1 = p]Pr[P t−1 = p]dp
m
Notation is abused here to emphasize the logic. For continuous
quantities,itisnotcorrecttowritePr[P t−1 = p]sincetheprobability
of the quantity taking on any specific value is zero. The correct
expressionis thedensityfunctionevaluated at p:
(cid:1)
∞
Pr[P t < P t−1 ∩P t−1 >m] = Pr[P t < p|P t−1 = p]f(p)dp
m
Note that the conditional cumulative probability (first term) reduces
to the unconditionalvalue Pr[P t < p] when P t and P t−1 are indepen-
dent, thecase consideredin Section 4.2.

80
STATISTICALARBITRAGE
| In      | order | to simplify | notation | in       | the remaining |      | derivation      | of the |
| ------- | ----- | ----------- | -------- | -------- | ------------- | ---- | --------------- | ------ |
| result, | let X | denote      | P and    | Y denote | P t−1 .       | Then | the probability | of     |
t
interest is:
(cid:1)
∞
|     |      | ∩Y  |     | =   |        | p|Y = |          |     |
| --- | ---- | --- | --- | --- | ------ | ----- | -------- | --- |
|     | Pr[X | < Y | >m] |     | Pr[X < |       | p]f(p)dp |     |
m
| ExpandtheconditionalcumulativeprobabilityPr[X |     |     |     |     |     |     | < p|Y | = p]into |
| --------------------------------------------- | --- | --- | --- | --- | --- | --- | ----- | -------- |
= Pr[X=
| the integral |     | of the conditional |     | density | to obtain | f   | X|Y (p) | x   |
| ------------ | --- | ------------------ | --- | ------- | --------- | --- | ------- | --- |
|Y = p]:
(cid:1) (cid:1)
∞ p
|     | Pr[X | < Y | ∩Y >m]= |     | f X|Y | (x)dxf(p)dp |     |     |
| --- | ---- | --- | ------- | --- | ----- | ----------- | --- | --- |
m −∞
(cid:1) (cid:1)
∞
p
=
f X|Y (x)f(p)dxdp
m −∞
(cid:1) (cid:1)
∞ p
|     |     |     |     | =   | f   | (x,p)dxdp |     |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | --- |
XY
−∞
m
| where | f (. | . .) denotesthe |     | jointdensityfunctionof |     |     | X and | Y.  |
| ----- | ---- | --------------- | --- | ---------------------- | --- | --- | ----- | --- |
XY
| Now, | using: |     |                 |     |     |     |     |     |
| ---- | ------ | --- | --------------- | --- | --- | --- | --- | --- |
|      |        |     | (cid:1) (cid:1) |     |     |     |     |     |
|      |        |     | ∞               | ∞   |     |     |     |     |
1
|     |     |     |     | f (x,p)dxdp= |     |     |     |     |
| --- | --- | --- | --- | ------------ | --- | --- | --- | --- |
XY
|     |     |     | −∞  |     |     | 2   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
m
(sincetheinnerintegralreducestothemarginaldensityofXand,by
definitionofthemedian,theouterintegralisthenpreciselyonehalf),
and notingthat:
|     | (cid:1) | (cid:1) |     | (cid:1) | (cid:1) |     |     |     |
| --- | ------- | ------- | --- | ------- | ------- | --- | --- | --- |
|     | ∞       | ∞       |     |         | ∞       |     |     |     |
p
(x,p)dxdp=
|     |     | f   |     |     |              | f (x,p)dxdp |     |     |
| --- | --- | --- | --- | --- | ------------ | ----------- | --- | --- |
|     |     | XY  |     |     |              | XY          |     |     |
|     | m   | −∞  |     |     | m(cid:1) − ∞ |             |     |     |
(cid:1)
|     |     |     |     |     | ∞ ∞ |             |     |     |
| --- | --- | --- | --- | --- | --- | ----------- | --- | --- |
|     |     |     |     | +   |     | f (x,p)dxdp |     |     |
XY
|     |     |     |     |     | m p |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
it followsimmediatelythat:
|     | (cid:1) | (cid:1) |           |     | (cid:1) (cid:1) |     |           |     |
| --- | ------- | ------- | --------- | --- | --------------- | --- | --------- | --- |
|     | ∞       | p       |           | 1   | ∞               | ∞   |           |     |
|     |         |         |           | =   | −               |     |           |     |
|     |         | f       | (x,p)dxdp |     |                 | f   | (x,p)dxdp |     |
|     |         | XY      |           | 2   |                 | XY  |           |     |
|     | m       | −∞      |           |     | m               | p   |           |     |

81
LawofReversion
| This may | seem | like an | irrelevant | diversion |     | but, | in fact, it takes | the |
| -------- | ---- | ------- | ---------- | --------- | --- | ---- | ----------------- | --- |
prooftowithintwostepsofcompletion.Atthispoint,weinvokethe
symmetryofthejointdensity(whichfollowsfromtheassumptionof
| identicalmarginal |         | distributions).Formally,anexpressionofsymme- |     |         |         |     |     |     |
| ----------------- | ------- | -------------------------------------------- | --- | ------- | ------- | --- | --- | --- |
| try is:           | (cid:1) | (cid:1)                                      |     | (cid:1) | (cid:1) |     |     |     |
|                   |         | ∞ p                                          |     |         | ∞ x     |     |     |     |
=
|          |           | f (x,p)dxdp         |     |              |         | f (x,p)dpdx |          |     |
| -------- | --------- | ------------------- | --- | ------------ | ------- | ----------- | -------- | --- |
|          |           | XY                  |     |              |         | XY          |          |     |
|          |           | m m                 |     | m            | m       |             |          |     |
| Now,     | reversing | the order           | of  | integration  | (be     | careful     | to watch | the |
| integral | limits)   | yields thealgebraic |     | equivalence: |         |             |          |     |
|          | (cid:1)   | (cid:1)             |     | (cid:1)      | (cid:1) |             |          |     |
|          |           | ∞ x                 |     |              | ∞ ∞     |             |          |     |
|          |           | f (x,p)dpdx         |     | =            |         | f (x,p)dxdp |          |     |
|          |           | XY                  |     |              |         | XY          |          |     |
|          | m         | m                   |     | m            | p       |             |          |     |
Therefore:
|                | (cid:1) | (cid:1)         |         | (cid:1)     | (cid:1)    |             |           |        |
| -------------- | ------- | --------------- | ------- | ----------- | ---------- | ----------- | --------- | ------ |
|                |         | ∞ p             |         |             | ∞ ∞        |             |           |        |
|                |         | f (x,p)dxdp     |         | =           |            | f (x,p)dxdp |           |        |
|                |         | XY              |         |             |            | XY          |           |        |
|                | m       | m               |         | m           | p          |             |           |        |
| Penultimately, |         | note that       | the sum | of          | the latter | two         | integrals | is one |
| quarter(again, |         | by definitionof |         | themedian): |            |             |           |        |
|                | (cid:1) | (cid:1)         |         | (cid:1)     | (cid:1)    |             |           |        |
|                |         | ∞ p             |         |             | ∞ ∞        |             |           |        |
|                |         | f (x,p)dxdp+    |         |             |            | f (x,p)dxdp |           |        |
|                |         | XY              |         |             |            | XY          |           |        |
|                |         | m m             |         | m           | p          |             |           |        |
|                |         | (cid:1) (cid:1) |         |             |            |             |           |        |
|                |         | ∞ ∞             |         |             |            |             |           |        |
1
|     |     | =   |     |     | =   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
f XY (x,p)dxdp
4
|     |     | m m |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
And so:
|     | (cid:1) | (cid:1) |     |     | (cid:1) (cid:1) |     |     |     |
| --- | ------- | ------- | --- | --- | --------------- | --- | --- | --- |
|     | ∞       | p       |     |     | ∞               | ∞   |     |     |
1
|     |     | f (x,p)dxdp= |     | −   |         | f       | (x,p)dxdp |     |
| --- | --- | ------------ | --- | --- | ------- | ------- | --------- | --- |
|     |     | XY           |     |     |         | XY      |           |     |
|     |     | −∞           |     | 2   |         |         |           |     |
|     | m   |              |     |     | m       | p       |           |     |
|     |     |              |     |     | (cid:8) | (cid:9) |           |     |
|     |     |              |     | 1   | 1 1     |         |           |     |
= −
|     |     |     |     | 2   | 2 4 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
3
=
8
| Theargument |     | issimilar | forthesecond |     | part | of the | disjunction. |     |
| ----------- | --- | --------- | ------------ | --- | ---- | ------ | ------------ | --- |

82 STATISTICALARBITRAGE
(a)
200
100
0
−4 −2 0 2 4
(b)
4
2
0
−4
0 200 400 600 800 1,000
FIGURE 4.4 Randomsamplefromautocorrelatedmodel
4.4.2 Examples
Example 1 One thousand terms were generated from a first-order
autoregressive model with serial correlation parameter r = 0.71 (see
Figure4.3andthefinalremarks inSection4.4regardingthischoice)
andnormallydistributedrandomterms.Figure4.4(b)showsthetime
plot;Figure 4.4(a)shows the samplemarginal distribution.
The proportion of reversionary moves exhibited by the series is
62 percent.
Adding a little more realism, we compute an estimate of the
mediantreatingtheseriesasifitwereobserveddaybyday.Analysis
of the local median adjusted series (using window length of 10) is
illustratedinFigure4.5.Aslightlygreaterproportionofreversionary
moves is exhibitedby theadjustedseries, 65 percent.
4.5 NONCONSTANT DISTRIBUTIONS
Suppose that spreads are generated from a normal distribution for
100 days, followed by a uniform distribution for 50 days. Within
each period the basic theorem is applicable; therefore, with one
exceptionin150daysthe75percentruleistrue.Supposethatonthe
one hundred fifty-first day, price range is generated from the normal
distributiononceagain. What can we say?

LawofReversion 83
(a)
300
200
100
0
−4 −2 0 2 4
(b)
4
2
0
−2
−4
0 200 400 600 800 1,000
FIGURE 4.5 Randomsamplefromautocorrelatedmodel,locallymedianadjusted:
(a)histogram(b)timeseries
Unequivocally we can say that the 75 percent rule is true on
average throughout the series. The crux of the proof is the two
transition days: (1) from normal to uniform, and (2) from uniform
to normal. Recall Figure 4.2. Region 1 is probabilistically bounded
by 0 < Pr[(1)]< 1 for random quantities from any two continuous,
4
independent distributions (by which it is meant that the probability
Pr[(1)]=Pr[(P t ,P t−1 )∈(1)]).Thisfollowsfromthedefinitionofthe
median as stated in Section 4.2. Denote this probability by p. Now,
thecomplementofregion1inthequadrantthereforehasprobability
1 −p (with the same kind of meaning attached to ‘‘probability of a
4
region’’aspreviously).Thetransitionsarethekeybecauseonlywhen
the distribution changes is the basic result in question. Indeed, it is
not hard to show that the result does not hold. For each transition
wherep > 1 (normaltouniformisacaseinpoint)thetheoremresult
8
is not 75 percent but 100(1 − 2p)% < 75%. However, for each
such transition, the reverse transition exhibits the complementary
probability 1 −p for region 1.
4
Similar analysis applies to region 2. And this is true irrespective
of whether the probability of region 2 is the same as the probability
ofregion1—whichitisnotifoneortheotherofthedistributionsis
asymmetric.
Thus,iftransitionsoccurinpairs,theexhibitedprobabilityisthe
averageand,hence,the75percentresultresurfaces.(Ifbothdensities

84 STATISTICALARBITRAGE
10
5
0
−5
0 50 100 150 200 250 300
FIGURE 4.6 Randomsamplefrommixednormal,lognormal,andStudentt
distributions
are symmetric, then the ‘‘pairs’’ condition is sufficient. However, if
at least one density is asymmetric, so that Pr[(1)] (cid:7)= Pr[(2)], then the
pairs must occur often enough to statistically guarantee that there
are few pairs in region 1–2 compared to 1–1 or 2–2.)
One can push the argument further to prove the case for three
alternative distributions, the key caveat being that each of the three
distinct pairwise transitions occur equally often in both directions.
An appeal to mathematical induction then completes the proof for
an arbitrary numberof alternativedistributions.
4.6 APPLICABILITY OF THE RESULT
After several pages of theoretical development, it is a good idea to
pause and ask, ‘‘What is the relevance to model-based stock trad-
ing?’’ A major starting assumption is stationarity—a conveniently
unaddressed, unmentioned in fact, thus far. We required spreads to
be ‘‘independent, identically distributed’’ (later relaxing the condi-
tions to allow for serial correlation); implicit therein in a time series
contextis stationarity.

LawofReversion 85
Now stock price series are not stationary. What about spreads?
They are typically not stationary either. However, dynamically
adjusted for local estimates of location and variance, a reasonable
approximationtostationaritycanbemade.Thereisalinkheretothe
idea of cointegration (see Chapter 3). It may be difficult to uncover
structure in individual price series but the difference between series
(spreads)morereadilyyieldspredictablerelationships.Extendingthe
basic notion of cointegration to locally defined series (we might use
thenomenclature‘‘locallycointegrated’’) identifiesthelink.
It is in this spirit of informed, dynamic approximation that the
theoretical result has guidingvalidity.
4.7 APPLICATION TO U.S. BOND FUTURES
The theorem presented in this chapter, while motivated by the dis-
cussion of spreads between stock prices of similar companies (the
classic pair of a pairs trade), is applicable with much greater gener-
ality. As long as the conditions on the ‘‘price’’ series are reasonably
met, the theorem applies to any financial instrument. Of course, the
rub is in the meeting of the conditions—many series do not (with-
out more attention to the structural development over time—trend
developments for example). Bond prices do show a good fit to the
theorem.
U.S. 30-year Treasury bond futures were studied with the sim-
ple forecasting model for changes in daily high–low price range.
The front future contract, being the most liquid, was examined.
(Because of concern about possible distortions arising from contract
expirations, the study was repeated with contract rollover at 15
business days prior to expiration of the front future. No distortions
were observed in the analysis, hence the results of the vanilla series
are reported.) Figure 4.7 shows the sample distribution of the data
for 1990–1994 used in the study—a strong skew is evident in the
distribution.A timeplot of theseries is given in Figure4.8.
In the prediction model, the median value was estimated each
day using data for the preceding 20 business days. Operationally,
this local median calculation is desirable to minimize the effects of
evolutionary change. One of the benefits is a reduction in serial
correlation: The raw series (equivalent to using a constant median)

86 STATISTICALARBITRAGE
300
200
100
0
0 1 2 3
FIGURE 4.7 Marginaldistributionofhigh–lowrangeoffrontU.S.30-yearbond
future
TABLE 4.1 EmpiricalstudyofU.S.30-yearbonds
Proportion Proportion Proportion
Year P t >P t−1 |P t−1 <m P t <P t−1 |P t−1 >m Overall
1990 70% 75% 73%
1991 77% 72% 74%
1992 78% 76% 77%
1993 78% 76% 77%
1994 78% 76% 77%
All 77% 75% 76%
Note:250tradingdaysperyear
exhibits autocorrelations in the range [0.15, 0.2] for many lags; the
local median adjustedseries exhibitsno significantautocorrelations.
Results of the forecasting exercise are presented in Table 4.1:
They are quiteconsistent with thetheorem.
The result confirmed by bond future prices is economically
exploitable. Some sophistication is required in the nature of the
implementation of the trading rule, particularly with respect to
managing tradingcosts, but thereare many possibilities.

LawofReversion 87
3.5
$
3.0
2.5
2.0
1.5
1.0
0.5
900102 910102 920102 930104 940103 941220
FIGURE 4.8 Dailyhigh–lowrangeoffrontU.S.30-yearbondfuture
4.8 SUMMARY
The implication of the theorem statement is a little provocative: The
75 percent forecast accuracy is guaranteed only if the conditions of
thetheoremaremet.Inpractice,theevidenceisthatmanystockprices
andspreadsdomeettheconditionsapproximatelyovershortperiods.
Moreover,therateofchange,whenchangeoccurs,isoftensufficiently
slow that a properly calibrated, dynamic model (local characteriza-
tion of the mean in the examples examined in this chapter) exhibits
reversion resultssimilar to thetheoretical prediction.
EmpiricalevidenceforU.S.30-yearTreasurybondssuggeststhat
this market, also, comes close to meeting the conditions. Certainly
the accuracy of the empirical model is not demonstrably different
from75percentforthefiveyears1990–1994.Withalittleingenuity,
many situations seemingly violating the conditions of the theorem
can bemade to approximatethem quiteclosely.
Appendix 4.1: LOOKING SEVERAL DAYS AHEAD
Assumingno persistent directionalmovement (trending),as we have
been doing in the theoretical development and proxying by local

88 STATISTICALARBITRAGE
n
57p
1.0
0.8
0.6
p = 0.75
p = 0.25
p = 0.35
p = 0.5
0.4
0.2
0.0
0 5 10 15 20
FIGURE 4.9 Probabilityofatleast1‘‘winningmove’’innextndays
location adjustment in the applications, there is obviously greater
opportunity for reversion if more than one day ahead may be
considered. Of course, it is crucial that each day in the k-day period
ahead can be looked at individually; if one may only look at k-day
movements, then the situation is essentially unchanged from the
one-day case. When each day may be considered, there are multiple
(independent) chances of a win (a reversion), so the probability of a
win increases.
Figure 4.9 shows the probability of a move from the current
position in the direction of the median occurring within the next k
days for k = 1,...,20. The probability of such a move occurring in
one day is 0.75 from the theorem. The other probabilities are cal-
culated from the binomial distribution as described next. The figure
also includes graphs assuming a winning probability of 0.25, 0.35,
and 0.5: In practice, a lower value than 0.75 will be observed under
thebest circumstancesbecause of theoremassumptionviolations.
By assumption, prices are independent each day. The theorem
states that the probability of a reversionary move from the current
position is 0.75 for any day. So, the probability of a reversionary
move from the price on day t is 0.75 for day t+1, for day t+2

LawofReversion 89
regardless of what happens on day t+1 (this is the independence
assumption), and so on. Thus, the number of days in the next k
days that show reversion from today’s price is a binomial quantity
withparametersk(thenumberoftrials)and0.75(theprobabilityof
successonagiventrial).Theprobabilityshowninthegraphisthen:
Pr[1 ormore successes in k days]=1−Pr[0 successes in k days]
(cid:8) (cid:9)
k
=1− 0.750(1−0.75)k−0
0
=1−0.25k
When the independence constraint is relaxed, the binomial result is
notvalid,deviationfromitbeingafunctionofthetemporalstructure
oftheseries.Wherethatstructureissimpletrending,thelongerahead
onelooksthelessaccuratethebinomialprobabilityis.Accuracymay
be restored by appropriate attention to the structural form of the
predictionfunction:addingan estimated trend component.

5
CHAPTER
Gauss Is Not the God of Reversion
It is betterto be roughlyright than precisely wrong.
—J.M. Keynes
5.1 INTRODUCTION
We begin with two quotes:
Thedistributionofnominalinterestratesindicatesthatthere
is no mean reversion in interest rates and the structure does
not resemblea normal distribution.
In contrast, real interest rates appear to be normally
distributed. The distribution suggests interest rates have the
characteristic of mean reversion.
Both of these quotes, from research publications (several years
ago) of a large, successful Wall Street firm, contain fallacious logical
implications. There is no explicit definition of what is meant by
‘‘mean reversion’’ and one might, therefore, take the depictions
of reversion through marginal distributions of yields as defining it
implicitly. But that would mean that the author is not talking about
mean reversion in thegeneral sense in which it is widelyinterpreted.
The first statement is wrong because time series that exhibit
marginal distributions of any shape whatsoever can be mean revert-
ing. The 75 Percent Theorem in Chapter 4 proves that unambigu-
ously. Note the caveat: can be. It is not sufficient to look at the
marginal distributionof a time series in order to be able to correctly
makeapronouncementonwhetherthatseriesexhibitsthequalityof
91

92 STATISTICALARBITRAGE
meanreversion.Thatiswhythesecondstatementisalsowrong.Itis
entirely possiblefora timeseries to be as far from mean reverting as
imaginable(well,almost)whileatthesametimeexhibitinganormal
marginal distribution, as is demonstrated in the final section of this
chapter.
Mean reversion by definition involves temporal dynamics: The
sequence in which data, samples from the marginal distribution,
occuris thecritical factor.
5.2 CAMELS AND DROMEDARIES
The report mentioned at the opening of this chapter shows a his-
togramoftheten-yearbondyieldssince1953,presentedinasection
called, ‘‘A Double Humped Distribution.’’ The claim is that a time
series exhibitingsuch an obviouslynonnormalmarginal distribution
cannot be reversionary. Despite the imagery of the title, there are,
in fact, several modes in the histogram. However, it is sufficient
to demonstrate a reversionary time series that has an extremely
pronouncedbimodaldistribution.
Figure5.1showsacombinedrandomsampleof500valuesfrom
the normal distribution with mean 4.5 and 500 values from the
normal distribution with mean 8.5 (and unit standard deviation for
both).Theselocationsaremotivatedbythemajormodesofthebond
yield distribution;theyare notcritical to thedemonstration.
Figure 5.2 shows one possible time series of these 1,000 points.
How much reversion is exhibited, from day 1, by this series? A lot.
Consider each segment separately. Take any point in either segment
far from the segment average (4.5 in the first segment, 8.5 in the
second). How many points must be passed before the time series
exhibitsavalueclosertothesegmentaverage?Typicallyonlyoneor
two.Theseriesneverdepartsfromthesegmentmeannevertoreturn;
onthecontrary,theseriescontinuallycrossestheaverage—almosta
definitionof reversion. A veritableexcited popcornprocess!
That leaves one to consider the implications of the single change
point: the move from the first segment to the second in which the
segment mean increases. Does a single mean shift in a time series
destroythepropertyofmeanreversion?Onlyiftheprocesshastobe
reverting to a global mean—that would be an unusually restrictive
interpretation of mean reversion; it would also be unhelpful and

200
150
100
50
0
2 4 6 8 10 12
FIGURE 5.1 Marginaldistribution:mixturedistributionofhalfN[4.5,1]andhalf
N[8.5,1]
10
8
6
4
2
0 200 400 600 800 1,000
FIGURE 5.2 TimeseriesrealizationofthesampledepictedinFigure5.1
93

94 STATISTICALARBITRAGE
misleading in a time series context, and misleading, too, in assessing
tradingopportunitiesthatnecessarilyoccurinatimeseries,sequential
manner. Suppose that the raw data are daily values. Then for two
years, the first segment of the combined series, the data would
unarguably be described as mean reverting. Shortly after the mean
increase the same conclusion would be acknowledged, albeit the
mean to which the series reverts is increased. Two more years of
splendidreversiontothe(new)meanthenfollow.Howcouldanyone
then look at the marginal distribution of the daily data, having
tradedwonderfullyprofitablythemostbasicmeanrevertingstrategy
describable, and announcethat theseries was notmean reverting?
A second distributional concern raised is that the bond data
distributionhasapronouncedright-handtail.Thisfeatureisactually
irrelevant insofar as the property of mean reversion is concerned.
Figure 5.3 shows a histogram of 1,200 points: the 1,000 from
the normal mixture of the previous example with 200 uniformly
randomlydistributedovertheinterval[10,14].Figure5.4showsone
possibletimeseriesofthe1,200points:Howmuchreversionisthere
in this series? A lot, once again. The first two segments are mean
reverting as demonstrated in the previous paragraphs. What about
the final segment? The points are a random sample from a uniform
200
150
100
50
0
2 4 6 8 10 12 14
FIGURE 5.3 Marginaldistributionwithheavyrighttail

GaussIsNottheGodofReversion 95
14
12
10
8
6
4
2
0 200 400 600 800 1,000 1,200
FIGURE 5.4 TimeseriesrealizationofthesampledepictedinFigure5.3
orderedbyunderlyingsamplingdistribution
distribution, not a normal distribution, and therefore according to
thereport,thetimeseriescannotbemeanreverting.Fromthegraph,
would you agree? If you do, I would like to entertain some gambles
with you!
One might reasonably charge that these examples are artificial.
Real time series don’t exhibit such convenient segmentation. This
is undeniable. But it is also not an issue. Figure 5.5 shows another
possible realization of the random sample in Figure 5.3. It was
obtained by randomly selecting, without replacement, the values in
the original sample of 1,200 and plotting in order of selection. How
much reversion is exhibited? Lots. Don’t you agree just from an
eyeball analysis?
Whetherthemarginaldistributionofatimeseriesisadromedary
oracamelreallydoesn’tmatterasfarasmeanreversionisconcerned.
To repeat: Temporal structureis thecritical feature.
5.2.1 Dry River Flow
Camels are distinguished largely by their remarkable adaptation to
life in arid regions, the twin key abilities bestowed by evolution
being the sponge-like capacity of the body to absorb water and the

96 STATISTICALARBITRAGE
14
12
10
8
6
4
2
0 200 400 600 800 1,000 1,200
FIGURE 5.5 TimeseriesrealizationofthesampledepictedinFigure5.3
randomlyreordered
drip-feed use thereof. Dry rivers, those with notable periods of no
streamflow,arecommoninaridlandscapes(andoftenthesourceof
replenishment for camels). Looking at a time series of stream flow
foradryriver,onewouldfindit difficulttodenytheclaim thatsuch
a series is reversionary. The series always returns to zero no matter
howfar it departs therefrom in therainy season.
What is the typical marginal distribution of dry river flow?
Obviously it is very asymmetric. So, entirely without recourse to
mathematical formalism or rigor, we have a proof that a reversion-
ary time series need not be characterized by a symmetric marginal
distributionsuch as thenormal.
The Bell Still Tolls Often a so-called Gamma distribution is a good
approximation (allowing for reasonable fudge for the zeroes) to dry
river flow. Now, a squared Gaussian variable is distributed as a
Chi-squared variable, which is also a Gamma variable. More than
curiouscoincidence?
ButNotforReversion Thedryriverflowexampleisjustoneparticular
case of self-evident reversion. To repeat: any marginal distribution
can beexhibitedby a reversionary timeseries.

300
250
200
150
100
50
0
−5 0 5 10
FIGURE 5.6 Randomsampleof1,000pointsfromN[2.65,2.442]
10
5
0
−5
0 200 400 600 800 1,000
FIGURE 5.7 TimeseriesrealizationofthesampledepictedinFigure5.6
97

98 STATISTICALARBITRAGE
5.3 SOME BELLS CLANG
Atimeseriesexhibitinganormalmarginaldistributionisnotpredis-
posed to exhibit mean reversion. Extraordinary diversion is equally
possible. Figure 5.6 shows a random sample from the normal dis-
tribution with mean 2.65 and standard deviation 2.44—the sample
values of the real yield data in the cited analysis. Figure 5.7 shows
one possible realization of this sample as a time series in which the
samplepointsaretakeninorderofmagnitude.Howmuchreversion
is exhibited, from day 1, by this series? Not one bit. As with my
earlier example, the charge of ‘‘unrealistic’’ or ‘‘points don’t occur
in [size] order’’ can bereadily made. Butsuch charges are irrelevant:
The point demonstrated, no matter how stylized the illustration, is
that a normal marginal distribution for a sample from a time series
revealsnothingaboutthetemporalpropertiesofthatseries,reversion
or any other.
Thepaperfromwhichthequotesatthebeginningofthischapter
aretaken,andthecontentofwhichiscriticallyexaminedhere,isnot
includedin thereferences list.

6
CHAPTER
Interstock Volatility
...the investordoes(orshould)considerexpected return a
desirablethingand variance of return an undesirablething.
—Harry Markowitz,Journal of Finance,
Vol. 7, No. 1, 1952
6.1 INTRODUCTION
T he reversion exploited in pairs trading is the reversion of stock
prices to each other following a movement apart, or a movement
apart following an unusual narrowing—the popcorn process of
Chapter 2. The amount of movement in stock prices is measured
by and expressed as stock volatility, which is the standard deviation
of price changes (returns). The volatility that is relevant to the
spread reversion scheme is the volatility of relative price movements
between stocks, hence interstock volatility. Figure 6.1(a) shows the
daily closing price (adjusted for splits and dividends) of two related
stocks, ENL and RUK, for the first six months of 1999. The price
seriestrackeachotherveryclosely,furtherdemonstratedbytheprice
difference(spread)seriesshowninFigure6.1(b).Ignoringthescales,
the spread series looks like any stock price series, and it will not be
surprising to discover that the volatility of the spread is similar in
character to stock price volatility.
Stock price volatility is the standard deviation of returns. But
what is the relevant measure of spread volatility? In Chapter 2 we
calibrated trade rules by directly computing the standard deviation
of thespread itself. Here we are interested in thetechnical definition
99

(a) Adjusted close price
ELN
RUK
45
40
35
$
30
25
20
Jan Feb Mar Apr May Jun Jul
1999
(b) Adjusted close price difference
ELN – RUK
10
5
0
$
−5
−10
−15
Jan Feb Mar Apr May Jun Jul
1999
(c) Annualized volatility
ELN
RUK
spread
100
% 50
0
Jan Feb Mar Apr May Jun Jul
1999
FIGURE 6.1 (a)DailyadjustedclosepricesofENLandRUK;(b)spread;
(c)volatilities
100

InterstockVolatility 101
of volatility, not simply a scale factor, and this requires focusing
on an appropriate return series. Considering the price difference in
Figure 6.1(b), with the trace variously above and below zero, it
is obvious that one should not treat the spread as a price—infinite
‘‘returns’’arereadilyexhibitedbysuchaseries!Therelevantmeasure
is apparent from consideration of how a basic reversion strategy
exploits spreads: When the spread widens or narrows beyond some
threshold whereupon reversion is subsequently expected, make two
bets, one on each stock, one a buy and the other a sell. Thus, the
spread bet return is the sum of the return on the stock bought and
thenegative return on thestock sold:
spread return= return onbuy−return on sell
(assuming equal dollar bets and measuring return to the long only).
Therefore, the value of interest, a measure of the range of variation
in the value of a spread bet or spread volatility, is directly computed
fromthespreadreturnseries, itselfthenumericdifferenceofthebuy
and sell return. (At this point of detail, one can begin to see how
theconsiderationsgeneralizebeyondthepairsettingtomoregeneral
statistical arbitrages.)
Figure 6.1(c) shows the volatility traces, using a trailing 20-day
window, of the two stocks ENL and RUK and of the spread
ENL–RUK. (In all of the examples in this chapter, volatilities are
computed under the conventional assumption of locally zero-mean
return.) The spread volatility is, as foreshadowed, visually similar to
the stock volatilities. Curiously, it is consistently greater than both
theindividualstock volatilities—more aboutthat later.
Another example is shown in Figure 6.2, this time for the pair
General Motors (GM) and Ford (F). Notice that the volatility of the
spread is sometimes greater and sometimes less than the volatility of
bothstocks, and sometimes greater than onebut less than the other.
These two examples expose many of the features of spread
volatility that are important in understanding and exploiting spread
relationships both for the simplest pairs, as illustrated, and more
general cases including baskets of stocks. Figure 6.3 shows another
example, this time of two unrelated stocks, Microsoft (MSFT) and
EXXON (XON).

(a) Adjusted close price
GM
F
80
75
70
$ 65
60
55
50
Jan Feb Mar Apr May Jun Jul
1999
(b) Adjusted close price difference
GM – F
20
15
$ 10
5
0
Jan Feb Mar Apr May Jun Jul
1999
(c) Annualized volatility
80 GM
F
spread
60
% 40
20
0
Jan Feb Mar Apr May Jun Jul
1999
FIGURE 6.2 (a) Daily adjusted close prices of GM and F; (b) spread;
(c) volatilities
102

InterstockVolatility 103
6.2 THEORETICAL EXPLANATION
Relative price movement is functionally dependent on the price
movementsofindividualstocks:Whatcouldbesimplerthanpriceof
A−priceofB?Whenlookingatthevariabilityofrelativeprices,the
relationshipismorecomplicated.Thekeyrelationshipisthatforthe
spread return already given:
spread return= return onbuy−return on sell
Writing A for the return on buy, B for the return on sell, and S for
thespread return,the spread volatilityis expressedas:
(cid:1) (cid:1)
V[S]= V[A−B]
(cid:1)
= V[A]+V[B]−2V[A,B]
where V[·] denotes (statistical or probabilistic) variance, and V[·, ·]
similarly denotes covariance. This expression immediately reveals
how and why the spread volatility can be less than, greater than, or
equaltothevolatilityofeitherconstituentstock.Thepertinentfactor
is thecovariance of (thereturns of) thosetwo stocks, V[A, B].
If the two stocks A and B (abusing notation quite deliberately)
are in fact the same stock, then the variances (the square of the
volatility) are the same and, crucially, the covariance is also equal
to the variance. Hence the volatility of the spread is zero: What else
couldit besincethe spread itself is identicallyzero?
Now, what if the two stocks are unrelated? Statistically, this is
equivalent to saying that the covariance is zero. Then the spread
volatilityreducesto:
(cid:1) (cid:1)
V[S] = V[A]+V[B]
That is, spread volatility is larger than both of the individual stock
volatilities. If the individual stocks have similar volatility, V[A] ≈
V[B], then theinflationfactoris about40 percent:
(cid:1) (cid:1)
V[S]= V[A]+V[B]
(cid:1)
≈ 2V[A]
(cid:1)
=1.414 V[A]

(a) Adjusted close price
MSFT
110
XON
100
90
$
80
70
60
Jan Feb Mar Apr May Jun Jul
1999
(b) Adjusted close price difference
MSFT – XON
30
20
$ 10
0
−10
Jan Feb Mar Apr May Jun Jul
1999
(c) Annualized volatility
MSFT
80
XON
spread
60
% 40
20
0
Jan Feb Mar Apr May Jun Jul
1999
FIGURE 6.3 (a)DailyadjustedclosepricesofMSFTandXON;(b)spread;
(c)volatilities
104

InterstockVolatility 105
6.2.1 Theory versus Practice
The illustration in Figure 6.1 shows the spread volatility for two
related stocks to be larger than both the individualstock volatilities.
Thetheoryadvancedintheprevioussectionsays(1)spreadvolatility
is zero for identical stocks, and (2) spread volatility is larger than
both individual stocks for unrelated stocks. Ugh? Surely ‘‘related
stocks’’ (such as ENL and RUK) are more like ‘‘identical stocks’’
than ‘‘unrelated stocks.’’ So according to the theory, shouldn’t the
volatilityof theENL–RUK spread besmall?
Now we must distinguish between statistical definitionsof terms
and English interpretations of the same terms. The two Elsevier
stocks, ENL and RUK, are indeed related—essentially they are
the same company. The historical traces of the price series show
extraordinarily similar behavior as befits that. Over the long term,
one is justified in stating that the prices are the same. However,
the price traces on the daily time scale seldom move precisely in
parallel; therefore the spread between the two does vary—seen in
Figure 6.1(b)—and spread volatility is not zero. In fact, over the
short term, the two price series show a negative relationship: In
Figure 6.1(a) the two price traces proceed sinuously like two snakes
entwined in a cartoon embrace, the one moving up when the other
moves down and vice versa. Statistically, this means that the two
seriesarenegativelycorrelated,particularlyontheshort-term return
scale which is pertinentto local volatilitycalculations.
Aha! Negative correlation (hence, negative covariance). Put that
intheformulaforspreadvolatilityandimmediatelyitisclearwhythe
Elsevier stocks’ spread volatility is greater than both the individual
stock volatilities.Profit in thebank for pairs trading!
6.2.2 Finish the Theory
Return to theexpressionforspread volatility:
(cid:1) (cid:1)
V[S] = V[A]+V[B]−2V[A,B]
Write σ2 = min(V[A],V[B]) and σ2 = max(V[A],V[B]), then it is
trivial to sandwich the spread volatility between multiples of the
individualstock volatilitiesfor uncorrelated stocks (V[A,B] = 0):
√ (cid:1) √
2σ ≤ V[S] ≤ 2σ

106 STATISTICALARBITRAGE
Two immediate observations have already been noted: For two
similarly volatile stocks, the spread will exhibit 40 percent more
volatility than the individual stocks; for two perfectly positively
correlated stocks, the spread will exhibit no volatility because it is
constant.Thatleavesoneextremecaseofrelatedness:whereAandB
areperfectlynegativelycorrelated,A= −B.Herethespreadvolatility
is doubletheindividualstockvolatility:
V[S]=V[A]+V[B]−2V[A,B]
=V[A]+V[−A]−2V[A,−A]
=V[A]+V[A]+2V[A,A]
=4V[A]
(cid:1) (cid:1)
Hence, V[S] = 2 V[A].Forstatisticalarbitragethisis(almost)the
grail of spread relationships.
6.2.3 Finish the Examples
What can be inferred about the GM–F and MSFT–XON examples
with the benefit of the theory for the volatility of spreads? Given a
description of the stock and spread volatility traces, one can point
to periods of changing local correlation, positive to negative. Of
course, one can observe correlation by direct calculation: See Figure
6.4. Average correlation in this first six months of 1999 is 0.58;
maximum 20-day correlation is 0.86; minimum 20-day correlation
is −0.15. Important to note here, for spread exploitation, are the
dynamicchangesincorrelationsand,hence,spreadvolatilityandthe
range of variation.
From late April the GM–F spread volatility was less than both
individualstockvolatilities,asitwasformostofMarch.Infact,from
thespread traceinFigure6.2(b)it is clear that for mostof Apriland
May, and again in June, the spread was practically constant in com-
parison to its valueoutsidethoseperiods.Thespread volatility trace
in Figure 6.2(c) shows a 50 percent hike in April and a similar drop
in May. Clearly these are artifacts of the unusually large (negative)
single day spread return on April 7 (see Figure 6.5) and the 20-day
window used to compute an estimate of volatility—review the local
correlationinFigure6.4.Outlierdown-weightingandsmoothingare

0.8
0.6
0.4
0.2
19990104 19990129 19990226 19990331 19990430 19990528 19990630
FIGURE 6.4 GM–Frolling20-daycorrelation
percent
0.05
0.0
−0.05
19990104 19990129 19990226 19990331 19990430 19990528 19990630
FIGURE 6.5 GM–Fspreaddailyreturn
107

108 STATISTICALARBITRAGE
typicalproceduresusedtoreduceunrealisticjumpsinsuchindirectly
measured quantities as volatility (see Chapter 3). Figure 6.5 shows
thespread return:return on GM minusreturn on F.
6.2.4 Primer on Measuring Spread Volatility
Let’sbeginbyaskingthequestion:Doesstatisticalarbitragegenerate
higherreturnswhen volatilityis high orwhen it islow?
Absentanystock-specificevents,higherinterstock(spread)volati-
lity should generate greater returns from a well calibrated model.
Figure 6.6 shows the average local volatility (20-day moving win-
dow) for pairwise spreads for stocks in the S&P 500 index from
1995 through 2003. Two years of outstanding returns for statistical
arbitragewere2000and2001.Bothwereyearsofrecordhighspread
volatility; 2000 higher in spread volatility and statistical arbitrage
return than 2001—nicely supporting the ceteris paribus answer.
But 1999 was the worst year for statistical arbitrage return in a
decade while spread volatility was equally high. There were many
0.15
0.10
0.05
199503 199703 199903 200103 200303
FIGURE 6.6 Averagelocalstandarddeviationofspreads

InterstockVolatility 109
stock-specific events, principally earnings related, with uniformly
negative impact on return in 1999. So noticeable, widespread, and
troublingweretheseeventsthattheSECeventuallypassedRegulation
Fair Disclosure(Reg. FD) to outlawtheactivities.
Using a local estimate of volatility, what picture is obtained
fromrepresentativespreadseries?Whatcanweinferfromthespread
volatilitychartinFigure6.6usingthesamplelocalvolatilityreference
patterns?
Figure 6.7 illustrates local volatility (using an equally weighted,
20-point window) for two sample spread series. The top panel, (a),
shows the spread series, the center panel, (b), the local volatility
estimates. There is nothing surprising here, the calculation being a
measure of variation about a constant line segment of the curves in
the top frame. Noteworthy is the observation that the average level
of local volatility issimilar forthetwo series.
What happens when a different measure of ‘‘local’’ is used? The
bottom panel, Figure 6.7(c), illustrates the situation for a 60-point
window:Thestrikingfeaturenowisthehigherlevelofvolatilityindi-
cated for the greater amplitude spread. (While we continueto couch
thepresentationintermsofaspread,thediscussionappliesequallyto
any time series.) Once again, there is no surprise here. The 60-point
window captures almost a complete cycle of the greater amplitude
series—the estimated volatility would be constant if precisely a full
cycle was captured—and, hence, the local volatility estimate reflects
the amplitude of the series. In the previous case, the shorter window
wasreflectingonlypartoftheslowermovingseriesvariation.Which
estimate of volatility reflects reversion return opportunity? Here the
answer is easy.
Now consider what picture would emerge if an average over a
setofsuchserieswereexamined,eachsuchseriesmixedwithitsown
‘‘noise’’on bothamplitudeand frequency.
Properlycautioned,whatcanbeinferredfromFigure6.6?Before
attemptingananswer,thearchetypalexampleanalysesclearlyadvise
looking at local volatility estimates from a range of windows (or
local weighting schemes)—it does seem advisable to concentrate on
evidence from shorter intervals and focus on average levels of local
volatility; mundanevariation in the estimate may be littlemore than
artifact. May be.

110 STATISTICALARBITRAGE
(a)
2
1
0
−1
−2
0 50 100 150 200
(b)
1.5
1.0
0.5
0.0
0 50 100 150 200
(c)
1.5
1.0
0.5
0.0
60 80 100 120 140 160 180 200
FIGURE 6.7 (a)Archetypalspreadseries;(b)localvolatilityestimate(20-point
window,equalweights)ofspreadseries;(c)localvolatilityestimate(60-point
window)ofspreadseries
Figure6.8reproducesthetwoexamplespreadcurvesfromFigure
6.7 and adds a third. The new series exhibits the same amplitude
as the original high-amplitude series and the same frequency as the
original higher frequency series. It therefore has the advantage of
more frequent and higher value reversion opportunities. The center
panel, (b), depicting local volatility estimates, indicates that the

InterstockVolatility 111
(a)
2
1
0
−1
−2
0 50 100 150 200
(b)
1.5
1.0
0.5
0.0
50 100 150 200
(c)
1.5
1.0
0.5
0.0
60 80 100 120 140 160 180 200
FIGURE 6.8 (a)Archetypalspreadseries;(b)localvolatilityestimate(20-point
window,equalweights)ofspreadseries;(c)localvolatilityestimate(60-point
window)ofspreadseries
average volatilityofthisthirdseriesistwicethat oftheoriginal two,
just as expected.
Now look at bottom panel, (c), which shows local volatility
estimates from the longer window. Interesting? Once again, the
analysis points to using a shorter, more local view when inferring
reversion opportunityfrom average levels of spread volatility.

112
STATISTICALARBITRAGE
| With               | these     | archetypal              | models,   | one           | can          | undertake      | an appropri-   |      |
| ------------------ | --------- | ----------------------- | --------- | ------------- | ------------ | -------------- | -------------- | ---- |
| ate time-frequency |           | analysis                |           | to precisely  | quantify     |                | the magnitude  | of   |
| reversionary       | moves.    | Real                    | spread    | series        | are          | less obliging, | beset          | with |
| nonstationarityand |           | ‘‘contaminating’’noise. |           |               |              |                |                |      |
| The                | foregoing | remarks                 |           | are generally | descriptive, |                | characterizing |      |
| how series         | variation | is                      | reflected | in empirical  |              | summary        | statistics     | and  |
indicatinghowthemagnitudeofpotentialgainfromsimplereversion
playsmaybeestimated.Actualreversionexploitationstrategiesmust
| be analyzed | directly |      | to make       | sensible | inferences  |               | on expectations |     |
| ----------- | -------- | ---- | ------------- | -------- | ----------- | ------------- | --------------- | --- |
| therefrom,  | whether  | in   | the idealized |          | settings    | of noise-free | sinusoidal      |     |
| series used | here     | orin | applicationto |          | real spread | histories.    |                 |     |
Chapter9revisitsinterstockvolatilityinthecontextofthedecline
| in statistical | arbitrage |     | performancesince2002. |     |     |     |     |     |
| -------------- | --------- | --- | --------------------- | --- | --- | --- | --- | --- |

7
CHAPTER
Quantifying Reversion
Opportunities
Fortitudinevincimus—By endurancewe conquer.
—Familymotto of Sir E. H. Shackleton,polarexplorer
7.1 INTRODUCTION
In this chapter, we extend the theoretical developments of the
previousthreechaptersinthesearchforadeeperunderstandingof
thepropertiesofreversionintimeseries.Therearemoreabstractions
and more difficultmathematics here than elsewhere in the book,but
in all cases, the theoretical development is subsequently grounded
in application. Most of the discussion is framed in the language of
price series, however, the developments generally apply to any time
series. In particular, the analysis can readily be applied, sometimes
withnecessaryrevisionofinference,totransformationsofpriceseries
includingreturns,spreads, spread returns, factors, and so forth.
Thequestion‘‘Whatis reversion?’’ is addressed in thecontextof
assumed probability models for stock price generation. The models
are highly stylized and oversimplified, being entertained purely as
a device for considering notions of reversion. There is no conceit
that the models serve even as first pass approximations to the
true, unknown, price generation mechanism. By determining the
implications of definitions of reversion under the very restrictive
assumptions of these simple models, it is hoped that a coherent
view of what reversion is will emerge. The goal is to extract from
such a view meaningful and quantifiable notions of reversion that
113

114 STATISTICALARBITRAGE
may be used in the study of realistic price generation models. It
is hoped that such understanding will provide new insight into
statistical arbitrage, helping us to analyze and understand how and
whystatisticalarbitrageworksatasystemsormechanisticlevel,and
from that build a valid market rationale for the driving forces of the
exploitable opportunities. That may be a little ambitious; perhaps
it is reaching to hope for more than indications of what kinds of
processestothinkaboutforsucharationale.Themechanicsandthe
rationale are both critical to investigating and solving the problems
thatbesetstatisticalarbitragestartingin2004andwhichcontinueto
affectperformancetoday:Howdomarketstructuralchangesimpact
strategy performance?
7.2 REVERSION IN A STATIONARY RANDOM PROCESS
Webeginthestudywithconsiderationofthesimpleststochasticsys-
tem,astationaryrandomprocess.Pricesaresupposedtobegenerated
independently each day from the same probability distribution, that
distributionbeingcharacterizedbyunchangingparameters.Weshall
assume a continuous distribution. Price on day t will be denoted by
P , lowercase being reserved for particular values (such as a realized
t
price).
Some considerationsthat immediatelysuggest themselvesare:
1. If P t lies in the tail of the distribution, then it is likely that P t+1
will be closer to the center of the distributionthan is P . In more
t
formal terms: Suppose that P > ninety-fifth percentile of the
t
distribution. Then the odds that P t+1 will be smaller than P t are
95 : 5 (19 : 1). A similar statement is obtained for the lower tail,
of course.
The 19 : 1 odds do not express quite the same idea as is
expressed in the first sentence. Being ‘‘closer to the center than’’
is not thesame as being ‘‘smaller than.’’ Certainly theodds ratio
quoted, and by implication the underlying scenario, are very
interesting. For completeness, it is useful to examine the ‘‘closer
tothecenter’’scenario.Theobviousnotionofclosertothecenter
is formally: the magnitude of the deviation from the center on
thepricescale.Analternativenotionistoconsiderdistancefrom

QuantifyingReversionOpportunities 115
the center in terms of percentiles of the underlying distribution
of prices. The two notions are equivalent for distributions with
symmetric densityfunctions,but nototherwise.
2. If P isclosetothecenterof thedistribution,then it islikelythat
t
P t+1 will befurtherfrom thecenter than P t .
After a little reflection, (ii) seems to offer infertile ground for a
reversionstudy;butinasequentialcontext,valuesclosetothecenter
areusefulflagsforsubsequentdeparturefromthecenterand,hence,
of future reversionary opportunities. Recall the popcorn process of
Chapter 2 and thediscussionof stochasticresonancein Chapter 3.
A generalization of the notion in (i) offers a potential starting
pointforthestudy:IfP >pthpercentileofthedistribution,thenthe
t
oddsthatP t+1 <P t arep : 100−p.Interesthereisconfinedtothose
cases where the odds are better than even. Investors largely prefer
strategiesthatexhibitmorewinningbetsthanlosingbets,considering
such relative frequency of outcomes a reflection of a stable process.
The thought process is deficient because by itself the win–lose ratio
imparts no information at all on the stability properties of a strat-
egy other than the raw win–lose ratio itself. Essential information
necessary for that judgment includes the description of the magni-
tudes of gains from winners and losses from losers. A strategy that
loses 80 percent of the time but that never exhibits individual losses
exceeding 0.1 percent and whose winners always gain 1 percent is
a stable and profitable system. Judgments about easily labeled but
complicated notions such as ‘‘stability’’ need careful specification
of personal preferences. Often these are not made explicit and are
therefore readily miscommunicated because individuals’ preferences
are quitevariable.
For P t > median, the odds that P t+1 < P t are greater than
one; similarly, for P t < median, the odds that P t+1 > P t are also
greater than one. The assumption of continuity is critical here, and
a reasonable approximation for price series notwithstanding the
discrete reality thereof. You may want to revisit Chapter 4 for a
rehearsal of thedifficultiesdiscretedistributionscan pose.
Two questionsare immediatelyapparent:
1. Isthe oddsresult exploitablein trading?
■ With artificial data followingtheassumed stationary process.

116 STATISTICALARBITRAGE
■ Withstockdatausinglocallydefinedmoments(toapproximate
conditionalstationarity).
2. How shouldreversion bedefined in thiscontext?
■ Reversion to the center requires modification of the foregoing
oddstosomethinglike75percent→50percentand25percent
→ 50 percent.
■ Reversion in the direction of the center—so that overshoot is
allowed and the oddsexhibitedare pertinent.
Whichever of (1) or (2) is appropriate (which in the context
of this chapter must be interpreted as ‘‘useful for the analysis and
interpretation of reversion in price series’’), how should reversion
be characterized? As the proportion of cases exhibiting the required
directional movement (a distributionfree quantity)?As theexpected
(average)pricemovementinthequalifyingreversionarycases(which
requires integration over an assumed price distribution and is not
distribution-free)?
Both aspects are important for a trading system. In a conven-
tional trading strategy, betting on direction and magnitude of price
movements, total profits are controlled by the expected amount of
reversion. If the model is reasonable, the greater the expected price
movement, the greater the expected profit. The volatility of profits
in such a system is determined in part by the proportion of winning
to losing moves. For the same unconditional price distributions, the
highertheratioofwinnerstolosers,thelowertheprofitvariancethus
spreading profit over more winning bets and fewer losing bets. Stop
loss rules and bet sizing significantly impact outcome characteristics
of a strategy, makingmoregeneral absolutestatementsunwise.
It is worth noting the following observation. Suppose we pick
onlythosetradesthatareprofitableroundtrip.Dailyprofitvariation
will still, typically, be substantial. Experiments with real data using
a popcorn process model show that the proportion of winning days
can be as low as 52 percent for a strategy with 75 percent winning
betsand a Sharperatio over 2.
Reversion defined as any movement from today’s price in the
direction of the center of the price distribution includes overshoot
cases. The scenario characterizes as reversionary movement a price
greaterthanthemedianthatmovestoanylowerprice—includingto
any price lower than the median, the so-called overshoot. Similarly,

QuantifyingReversionOpportunities 117
movement from a price below the median that moves to any higher
priceis reversionary.
7.2.1 Frequency of Reversionary Moves
Forany pricegreater than themedian price, P = p > m:
t t
Pr[P t+1 < p t ] = F P (p t )
where F (·) denotes the distribution function of the probability
P
distribution from which prices are assumed to be generated. (This
result is a direct consequence of the independence assumption.)
An overall measure of the occurrence of reversion in this situation
is then: (cid:1)
∞
3
F (p )f (p )dp =
P t P t t
8
m
wheref (.)isthedensityfunctionofthepricedistribution.Therefore,
p
also considering prices less than the median, P < m, we might say
t
thatreversionoccurs75percentofthetime.Thisistheresultproved
and discussed at length in Chapter4.
Previouslyitwasnotedthattheproportionofreversionarymoves
is a useful characterization of a price series. The 75 percent result
states that underlyingdistributionalform makes no differenceto the
proportion of reversionary moves. Therefore, low volatility stocks
willexhibitthesameproportionofopportunitiesforasystemexploit-
ing reversion as high volatility stocks. Furthermore, stocks that are
more prone to comparatively large moves (outliers, in statistical
parlance)willalsoexhibitthesameproportionofreversionaryoppor-
tunities as stocks that are not so prone. The practical significance
of this result is that the proportion of reversionary moves is not
a function of the distribution of the underlying randomness. Thus,
when structure is added to the model for price generation, there are
no complications arising from particular distribution assumptions.
Moreover, when analyzing real price series, observed differences in
theproportionofreversionarymovesunambiguouslyindicatediffer-
ences in temporal structureotherthan in therandom component.

118
STATISTICALARBITRAGE
| 7.2.2     | Amount | of Reversion |            |     |        |       |           |     |        |
| --------- | ------ | ------------ | ---------- | --- | ------ | ----- | --------- | --- | ------ |
| Following | the    | preceding    | discussion |     | of how | often | reversion | is  | exhib- |
ited,somepossiblemeasuresofthesizeofexpectedreversionfroma
| price greater |     | than themedian |     | are: |     |     |     |     |     |
| ------------- | --- | -------------- | --- | ---- | --- | --- | --- | --- | --- |
−P |P
| 1. E[P    | t+1   | >       | P t+1 ]    | Expectedamount |          | ofreversion, |     | given | that |
| --------- | ----- | ------- | ---------- | -------------- | -------- | ------------ | --- | ----- | ---- |
|           | t     | t       |            |                |          |              |     |       |      |
| reversion |       | occurs. |            |                |          |              |     |       |      |
| 2. E[P    | − P   | |P >    | m] Average |                | amountof | reversion.   |     |       |      |
|           | t t+1 | t       |            |                |          |              |     |       |      |
− |P
| 3. E[P | P t+1 | >   | P t+1 ]Pr[P | t+1 | < P ] | Overall | expectedamount |     | of  |
| ------ | ----- | --- | ----------- | --- | ----- | ------- | -------------- | --- | --- |
|        | t     | t   |             |     | t     |         |                |     |     |
reversion.
| Remarks:P | >misanunderlyingcondition.Thedifferencebetween |     |     |     |     |     |     |     |     |
| --------- | ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
t
| cases 1    | and 2                      | is that     | case      | 2 includes   | the               | 25 percent | of          | cases          | where  |
| ---------- | -------------------------- | ----------- | --------- | ------------ | ----------------- | ---------- | ----------- | -------------- | ------ |
| P > m      | but reversion              |             | does      | not occur,   | P                 | t+1 >      | P , while   | case           | 1 does |
| t          |                            |             |           |              |                   |            | t           |                |        |
| not. Case  | 1 includesonlyreversionary |             |           |              | moves.            |            |             |                |        |
| If case    | 1 is                       | taken       | to define | the          | total             | amount     | of ‘‘pure’’ | reversion      |        |
| in the     | system,                    | then        | case      | 2 may        | be considered     |            | as the      | ‘‘revealed’’   |        |
| reversion  | in                         | the system. | With      |              | this terminology, |            | it          | is possible    | to     |
| envisage   | a system                   | in          | which     | the revealed |                   | reversion  | is zero     | or negative    |        |
| while the  | pure                       | reversion   | is        | always       | positive          | (except    | in          | uninteresting, |        |
| degenerate | cases).                    |             |           |              |                   |            |             |                |        |
| Moves      | from                       | a price     |           | less than    | the               | median     | are         | characterized  |        |
analogously.
| PureReversion |     | Expectedpure |     | reversion |     | isdefined | as: |     |     |
| ------------- | --- | ------------ | --- | --------- | --- | --------- | --- | --- | --- |
1
|     |     | E[P −P | |P  | <   | P ,P | >m]× |     |     |     |
| --- | --- | ------ | --- | --- | ---- | ---- | --- | --- | --- |
|     |     | t      | t+1 | t+1 | t t  |      |     |     |     |
2
1
|     |     | +E[P |     | −P |P | >P  | ,P < | m]× |     |     |
| --- | --- | ---- | --- | ----- | --- | ---- | --- | --- | --- |
|     |     |      | t+1 | t     | t+1 | t t  |     |     |     |
2
Thetwopiecescorrespondto(a)downwardmovesfromapriceabove
themedianand(b)upwardmovesfromapricebelowthemedian.Itis
importanttokeepthetwopartsseparatebecausetheexpectedvalues
| of each | are generally |     | different; | only | for | symmetric | distributions |     | are |
| ------- | ------------- | --- | ---------- | ---- | --- | --------- | ------------- | --- | --- |
theyequal.Considerthefirsttermonly.FromFigure7.1,thecasesof
interestdefinetheconditionaldistributionrepresentedbytheshaded
| region. | For any | particular |     | price | P = p | > m, | the expected | amount |     |
| ------- | ------- | ---------- | --- | ----- | ----- | ---- | ------------ | ------ | --- |
|         |         |            |     |       | t     | t    |              |        |     |

QuantifyingReversionOpportunities 119
m p
t
FIGURE 7.1 Genericpricedistribution
of reversion is just P minus the expected value of the conditional
t
distribution:
(cid:1)
pt
p t −E Pt+1 |Pt+1<pt [P t+1 ] = p t − p t+1 f Pt+1 |Pt+1<pt (p t+1 )dp t+1
−∞
ThedensityoftheconditionaldistributionofP t+1 ,giventhatP t+1 <
P , is just the rescaled unconditionaldensity (from the independence
t
assumption), the scale factor being one minus the probability of the
subsetoftheoriginaldomainexcludedbytheconditioning.Expected
reversion is therefore:
(cid:1)
1 pt
p − pf (p)dp
t P
F P (p t ) −∞
Now we are interested in the expected value of this quantity
averaged over all thosepossiblevalues P = p > m:
t t
(cid:2) (cid:3)
E Pt>m (cid:1) P t (cid:4) −E Pt+1 |Pt+1<P (cid:1)t [P t+1 ] (cid:5)
∞ 1 pt
=
m
p t −
F P (p t ) −∞
pf P (p)dp f Pt |Pt>m (p t )dp t

120 STATISTICALARBITRAGE
Substituting for f (p ) = f (p )/(1−F (m)) = 2f (p ) for P >
Pt |Pt >m t P t P P t t
m, then the overall expected amount of pure (one-day) reversion
when P > m is:
t
E[P t −P t+1 |P t+1 < P t ,P t >m]
(cid:1) (cid:4) (cid:1) (cid:5)
∞ 1 pt
= 2 p − pf (p)dp f (p )dp
t P P t t
m F P (p t ) −∞
A similar analysis for the second term in the original expectation
yields:
E[P t+1 (cid:1) −P t(cid:4) |P t+1 >P t ,P (cid:1) t < m] (cid:5)
m 1 ∞
= 2 pf (p)dp−p f (p )dp
−∞ 1−F P (p t ) pt P t P t t
Adding (one half times) these two results gives the expected pure
reversion as:
(cid:1) (cid:4) (cid:1) (cid:5)
∞ 1 pt
p − pf (p)dp f (p )dp
t P P t t
m (cid:1) (cid:4) F P (p t ) −∞ (cid:1) (cid:5)
m 1 ∞
+ pf (p)dp−p f (p )dp
−∞ 1−F P (p t ) pt P t P t t
Some simplification of this expression would be nice. Example 1,
whichfollows,showssimplificationpossibleforthenormaldistribu-
tion, the double integral here reducing to a single integral; however,
even there, a closed form solution remains elusive. The symmetry is
suggestive. Would the result simplify if the cut-off is taken as the
meanratherthanthemedian?Certainlyanassumptionofasymmet-
ric densityleadsto cancellationof thetwo direct termsin P ; in fact,
t
the two parts of the sum are equal. Perhaps Fubini’s rule, revers-
ing the order of integration, can usefully be applied? We do know
that the result is positive! A closed-form theoretical result remains
unknown at this time, but computation of any specific example is
straightforward (see theexamplesthat follow).

QuantifyingReversionOpportunities 121
RevealedReversion Expectedrevealed reversion isdefinedas:
1 1
E[P t −P t+1 |P t > m]× +E[P t+1 −P t |P t < m]×
2 2
Considerthe first term of theexpression:
E[P t −P t+1 |P t >m]=E[P t |P t >m]−E[P t+1 |P t >m]
=E[P t |P t >m]−E[P t+1 ] by independence
=E[P |P >m]−µ
t t
where µ denotes the mean of the price distribution. Similarly, the
second term of the expression reduces to E[P t+1 −P t |P t < m] =
µ−E[P |P > m]. It is worth noting that both terms have the same
t t
value, whichfollowsfrom:
(cid:1)
∞
µ = E[P ]= pf (p)dp
t P
−∞
(cid:1) (cid:1)
m ∞
= pf (p)dp+ pf (p)dp
P P
−∞ m
1 1
= E[P |P < m]+ E[P |P >m]
t t t t
2 2
whereupon:
1 1
E[P |P >m]−µ=E[P |P >m]− E[P |P < m]− E[P |P >m]
t t t t t t t t
2 2
1 1
= E[P |P >m]− E[P |P < m]
t t t t
2 2
1 1
= E[P |P >m]+ E[P |P < m]−E[P |P < m]
t t t t t t
2 2
=µ−E[P |P < m]
t t
Total expected revealed reversion may therefore be expressed equiv-
alentlyas:
totalexpectedrevealedreversion =0.5×(E[P |P>m]−E[P |P <m])
t t t t
=E[P |P >m]−µ
t t
=µ−E[P |P < m]
t t

122 STATISTICALARBITRAGE
which (for continuous distributions) is positive except in uninterest-
ing, degenerate cases.
Note 1: This result provides a lower bound for case 1 since the
latter excludes those outcomes, included here, for which the actual
reversion is negative, namely {P t+1 : P t+1 > P t ,P t > m} and {P t+1 :
P t+1 < P t , P t < m}.
Note2:Adesirablepropertyforthereversionmeasuretohaveis
invariance to location shift. The amount of reversion, in price units,
should not change if every price is increased by $1. It is easy to
see that the expression for expected revealed reversion is location
invariant: Moving the distribution along the scale changes the mean
and median in the same amount. For the pure reversion result, it
is not very easy to see the invariance from the equation. However,
considerationof Figure7.1 fillsthat gap.
SomeSpecificExamples
Example 1 Prices are normally distributed. If X is normally dis-
tributed with mean µ and variance σ2, then the conditional distri-
bution of X such that X < µ is the half normal distribution. Total
expectedrevealedreversionis0.8σ.(Themeanofthetruncatednor-
mal distribution is given in Johnson and Kotz, Volume√1, p. 81; for
the half normal distribution the result is E[X(cid:3)] = 2σ/ 2π.) Thus,
the greater the dispersion of the underlying price distribution, the
greater theexpected revealed reversion: a result that is nicely in tune
with intuitionand desire.
From a random sample of size, 1,000 from the standard normal
distribution,thesamplevalueis0.8,whichisbeguilinglyclosetothe
theoretical value. Figure7.2 shows thesampledistribution.
The pure reversion general result can be reduced somewhat for
the normal distribution. First, as already remarked, the terms in P
t
cancel becausethe densityissymmetric, leaving:
(cid:1) (cid:4) (cid:1) (cid:5)
∞ 1 pt
− pf(p)dp f(p )dp
t t
m (cid:1) F (cid:4) (p t ) −∞ (cid:1) (cid:5)
m 1 ∞
+ pf(p)dp f(p )dp
−∞ 1−F(p t ) pt t t
(The subscript on f and F has been dropped since it is not necessary
to distinguish different conditional and unconditional distributions

QuantifyingReversionOpportunities 123
(a)
150
50
0
−4 −2 0 2
(b)
3
2
1
−1
−3
0 200 400 600 800 1,000
Index
FIGURE 7.2 Random‘‘price’’series:(a)sampledistribution,(b)sequential
ordering
here:Onlytheunconditionalpricedistributionisused.)Johnsonand
Kotz give results for moments of truncated normal distributions. In
particular, the expected values of singly truncated normals required
here are: (cid:1)
pt f(p )
pf(p)dp= − t
−∞ F(p t )
and (cid:1)
∞
f(p )
pf(p)dp= t
1−F(p )
pt t
Therefore, expectedpurereversion is:
(cid:1) (cid:1)
∞ 1 −f(p) m 1 f(p)
− f(p)dp+ f(p)dp
m F(p) F(p) −∞ 1−F(p)1−F(p)
(cid:1) (cid:4) (cid:5) (cid:1) (cid:4) (cid:5)
∞ f(p) 2 m f(p) 2
= dp+ dp
m F(p) −∞ 1−F(p)
For a symmetric density, inspection shows that the two terms in the
sum are equal. Algebraically, noting that f(m−(cid:3)) = f(m+(cid:3)) and
F(m−(cid:3)) = 1−F(m+(cid:3)), then a simple change of variable, q = −p,
gives the result immediately. The quantity (1 − F(x))/f(x) is known

124 STATISTICALARBITRAGE
as Mills’ ratio. Therefore, expected pure reversion for the normal
independent identically distributed (iid) model is twice the integral
of the inverse squared Mills’ ratio with integration over half the
real line: (cid:1)
m
2 M(p)
−2dp
−∞
Panel(b)ofFigure7.2showstherandomsamplereferredtoatthe
beginningofthesectionasatimeseries.Fromthisseries:Thenumber
of downward moves from above the median, {x t : x t > 0∩x t+1 <
x }, is 351; the number of upward moves from below the median,
t
{x t : x t < 0∩x t+1 > x t },is388;theproportionofreversionarymoves
is100∗(351+388)/999= 74%(thedenominatorisreducedbyone
becauseoftheneedtoworkwithpairs(x t ,x t+1 )and,ofcourse,there
is no value to pair withx ).
1,000
Revealed reversion for this time series Figure 7.3 shows the distri-
bution of one-day ‘‘price’’ differences for (a) moves from above the
median, {x t −x t+1 : x t > 0}, and (b) moves from below the median,
{x t+1 −x t : x t < 0}.Notsurprisingly,forsuchalargesamplethetwo
look remarkably similar (in fact, the sums, or sample estimates of
expected values, agree to four significant figures); the total of these
moves is 794/999= 0.795, which is very close to the theoretical
expected value of 0.8. Some discrepancy is expected because treat-
ing the random sample as a time series imposes constraints on the
componentsof thesets of pairs of values comprisingthemoves.
Purereversionforthistimeseries Figure7.4showsthedistribution
of one-day ‘‘price’’ differences for (a) moves from above the median
in a downward direction only, {x t −x t+1 : x t > 0∩x t > x t+1 }, and
(b) moves from below the median in an upward direction only,
{x t+1 −x t : x t < 0∩x t < x t+1 }. These histograms are simply trun-
cated versions of those in Figure 7.3, with 0 being the truncation
point.Total purereversion is 957/999= 0.95.
This exampledata is further discussed in Example5.
Example 2 Prices are distributed according to the Student t distri-
bution on 5 degrees of freedom. A Monte Carlo experiment yielded
the expected revealed reversion to be 0.95 (for the unit scale t
5
distribution). Notice that this value is larger than the corresponding

QuantifyingReversionOpportunities 125
(a)
120
80
40
0
−2 0 2 4
Moves from above median
(b)
100
60
20
0
−2 0 2 4
Negative moves from below median
FIGURE 7.3 Random‘‘price’’series:distributionofone-daymoves
(a)
60
40
20
0
0 1 2 3 4
Moves down from above median
(b)
100
60
20
0
0 1 2 3 4
Negative moves up from below median
FIGURE 7.4 Random‘‘price’’series:distributionofone-daymoves
value for the unit scale (standard) normal distribution (0.8). The
increase is a consequence of the pinching of the t density in the
center and stretching in the tails in comparison with the normal:
The heavier tails mean that more realizations occur at considerable

126 STATISTICALARBITRAGE
(a) Unit variance normal and Student t
5
0.4
Student t
5
Normal
0.2
0.0
−4 −2 0 2 4
(b) Unit variance normal and unit scale Student t
5
0.4
0.2
0.0
−6 −4 −2 0 2 4 6
FIGURE 7.5 ComparisonofnormalandStudenttdistributions
distancefromthecenter.Recallthatthevarianceofthetdistribution
isthescalemultipliedbydof/(dof −2)wheredof denotesthedegrees
of freedom; the unit scale t distribution has variance 5. Thus, the
5 3
t
5
distribution with scale 3
5
has unit(cid:6)variance and exhibits revealed
reversion (in this sample) of 0.95× 3/5 = 0.74, which is smaller
than thevalue for the standard normal distribution.
These comparisons may be more readily appreciated by looking
at Figure7.5.
Purereversion See theremarks in Example1.
Example3 PricesaredistributedaccordingtotheCauchydistribu-
tion. Since the moments of the Cauchy distribution are not defined,
themeasuresofexpectedreversionarealsonotdefined,sothisisnot
afruitfulexampleinthepresentcontext.Imposingfinitelimits—the
truncatedCauchydistribution—isaninterestingintellectualexercise,
one that is best pursued under the aegis of an investigation of the t
distribution,sincetheCauchy isthe t on onedegree of freedom.
Example4 Anempiricalexperiment.Dailyclosingprices(adjusted
fordividendsandstocksplits)forstockAAfortheperiod1987–1990
areshowninFigure7.6.Obviously,thedailypricesarenotindepen-
dent, nor could they reasonably be assumed to be drawn from the

QuantifyingReversionOpportunities 127
(a)
30
25
20
15
870102 871008 880714 890420 900125 901101
(b)
3
2
1
−1
−3
0 200 400 600 800 1,000
FIGURE 7.6 DailyclosepriceforstockAA(adjustedfordividendsandstock
splits):(a)actual,(b)standardizedforlocalmedianandstandarddeviation
same distribution. These violations can be mitigated somewhat by
locally adjusting the price series for location and spread. Even so, it
is notexpectedthat the75percent reversionresultwill beexhibited:
Serialcorrelationstructureinthedataisnotaddressedforonething.
Thepointofinterestisjusthowmuchreversionactuallyisexhibited
according to the measures suggested. (An unfinished task is appor-
tionment of the departure of empirical results from the theoretical
resultsto the several assumptionviolations.)
The daily price series is converted to a standardized series by
subtractingalocalestimateoflocation(meanormedian)anddividing
byasimilarlylocalestimateofstandarddeviation.Thelocalestimates
are based on an exponentially weighted moving average of recent
past data: In this way an operational online procedure is mimicked
(see Chapter 3). Figure 7.6 shows the standardized price series using
aneffectivewindowlengthof10businessdays;thelocationestimate
isthemedian.ComparethiswithFigure7.8,referred tolater, which
showstheprice series adjustedforlocation only.
For the location-adjusted series, not standardized for variance,
theproportionofreversionarymovesis58percent,considerablyless
than the theoretical 75 percent. Note that 0 is used as the median of
the adjusted series. By construction, the median should be close to
zero;moresignificantly,theprocedureretainsanoperationalfacility
by this choice. A few more experiments, with alternative weighting

128
STATISTICALARBITRAGE
| schemes | using | effective | window |     | lengths | up to | 20 business | days | and |
| ------- | ----- | --------- | ------ | --- | ------- | ----- | ----------- | ---- | --- |
usingthelocalmeaninplaceofthelocalmedianforlocationestimate,
| yield            | similar | results:    | the proportion |             | of      | reversionary |           | moves being  | in    |
| ---------------- | ------- | ----------- | -------------- | ----------- | ------- | ------------ | --------- | ------------ | ----- |
| the range        |         | 55 to       | 65 percent.    | The         | results | clearly      |           | suggest that | one   |
| or more          | of      | the theorem |                | assumptions |         | are not      | satisfied | by the       | local |
| locationadjusted |         |             | series.        |             |         |              |           |              |       |
Figure7.7showsthedistributionofpricechanges(close–previous
close)forthosedayspredictedtoberevertingdownwardand(previ-
ousclose–close)forthosedayspredictedtoberevertingupward.The
| price | changes | are | calculated | from | the | raw price | series | (not | median |
| ----- | ------- | --- | ---------- | ---- | --- | --------- | ------ | ---- | ------ |
adjusted)sincethosearethepricesthatwilldeterminetheoutcomeof
abettingstrategy.Figure7.7thereforeshowsthedistributionofraw
profitandloss(P&L)fromimplementingabettingstrategybasedon
stockpricemovementrelativetolocalaverageprice.Panel(a)shows
thedistributionoftradeP&Lforforecastdownwardreversionsfrom
| a price | above   | the          | local median, |           | panel      | (b) shows | the      | distribution | of  |
| ------- | ------- | ------------ | ------------- | --------- | ---------- | --------- | -------- | ------------ | --- |
| trade   | P&L     | for forecast | upward        |           | reversions | from      | a        | price below  | the |
| local   | median. | Clearly      | neither       | direction |            | is, on    | average, | profitable.  | In  |
$−31.95on
| sum,             | theprofitis |          |             | 962tradesof |          | the$15–30 |     | stock         | (there |
| ---------------- | ----------- | -------- | ----------- | ----------- | -------- | --------- | --- | ------------- | ------ |
| are 28           | days        | on which | the         | local       | median   | adjusted  |     | price is      | 0, and |
| 2×k              | = 20        | days     | are dropped | from        | the      | beginning |     | of the series | for    |
| initializationof |             | local    | median      | and         | standard | deviation |     | thereof).     |        |
(a)
120
80
40
0
|     | −1.0 |     | −0.5 | 0.0 |     | 0.5 |     | 1.0 |     |
| --- | ---- | --- | ---- | --- | --- | --- | --- | --- | --- |
Moves from above median
(b)
100
50
0
|     |     |     | −4  |     | −2  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0
Negative moves from below median
| FIGURE | 7.7 | StockAAone-daymovesaroundlocalmedian:(a)fromabovethe |     |     |     |     |     |     |     |
| ------ | --- | ---------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
medianand(b)frombelowthemedian

QuantifyingReversionOpportunities 129
(a)
2
0
−4
−8
0 200 400 600 800 1,000
(b)
200
100
0
−8 −6 −4 −2 0 2
FIGURE 7.8 StockAAlocalmedianadjustedcloseprice:(a)timeseriesand(b)
histogram
Figure 7.8 shows the distribution of price minus local median.
TakingthisasthedistributioninSection7.2(withthemediantherein
becomingzero),thetotalrevealedreversionis$597.79/990= $0.60
per day. The actual result reported in the preceding paragraph,
$−31.95, shows the extent to which assumption violations (with
unmodeled or poorly modeled structure) impact expected revealed
reversion in thisexample.
This‘‘missingstructure’’impactisperhapsmorereadilyappreci-
atedfromapureanalysisofthemedianadjustedseries.Therevealed
reversion from this series (in contrast to the already reported rever-
sionfromtherawpriceseriesgivensignalsfromtheadjustedseries)is
$70.17.Thismeansthatlessthanone-eighthoftherevealedreversion
from the independent, identically distributed model is recoverable
from the local location adjusted data series. (Outlier removal would
be a pertinent exercise in a study of an actual trading system. In an
operationalcontext,the large outliersituationswouldbe masked by
risk control procedures.) Example 5 attempts to uncover how much
reversion might belost throughlocal location adjustment.
Figure 7.9 shows the sample autocorrelation and partial auto-
correlation estimates: Evidently there is strong 1- and 2-day serial
correlation structure in the locally adjusted series. Undoubtedlythat

130 STATISTICALARBITRAGE
(a)
autocorrelation
1.0
0.8
0.6
0.4
0.2
0.0
0 5 10 15 20
(b)
partial autocorrelation
0.8
0.6
0.4
0.2
−0.2
FIGURE 7.9 StockAA:(a)autocorrelationsand(b)partialautocorrelationsof
localmedianadjustedcloseprice
accounts for part (most?) of the deviation of actual revealed rever-
sion from the theoretically expected value under the assumption of
independence.
Pure reversion For the record, total pure reversion in the median
adjusted priceseries (from theactual timeseries, since we do not yet
have a closed-form result to apply to the price-move distributions,
although we do know that it must exceed the sample estimate of the
theoreticalvalueofrevealedreversionor$597.79)is$191.44on562
days.Purereversionfromtherawpriceseries(usingsignalsfromthe
adjusted series) is just 60 percent of this at $117.74.
Example 5 This is an extended analysis of the data used in Exam-
ple 1. In Example 4, the operational procedure of local median

QuantifyingReversionOpportunities 131
(a)
150
50
0
−4 −2 0 2
(b)
2
0
−2
0 200 400 600 800 1,000
FIGURE 7.10 Randompriceseries,localmediananalogsofFigure7.2:
(a)histogramand(b)timeseries
adjustment was introduced as a pragmatic way of applying the 75
percent result to real, but nonstationary, data series. It is of interest
to understand the implications of the operational procedure for a
seriesthatisactuallystationary.Suchknowledgewillhelpdetermine
therelativeimpactofempiricaladjustmentforlocationagainstother
assumptionviolationssuch as serial correlation.
Figures7.10to7.12arelocalmedianadjustedversionsofFigures
7.2 to 7.4. (The local median is calculated from a window of the
preceding 10 data points.) The summary statistics, with values from
the original analysis in Example 1 in parentheses, are: 77 percent
(74percent)ofreversionarymoves;totalpurereversion= 900(952);
total revealed reversion= 753(794).
The analysis depicted in Figures 7.13 to 7.15 is perhaps more
pertinent. The median adjusted series determines when a point is
aboveorbelowthelocalmedianbut,incontrasttothecasereported
in the preceding paragraph, the raw, unadjusted series is used to
calculate the amount of reversion. This is the situation that would
beobtainedinpractice.Signalsmaybegeneratedbywhatevermodel
one chooses, but actual market prices determine the trading result.
Interestingly, pure reversion increases to 906—but this value is still

(a)
100
50
0
−2 0 2 4
Moves from above median
(b)
100
60
20
0
−2 −1 0 1 2 3 4
Negative moves from below median
FIGURE 7.11 Randompriceseries,localmediananalogsofFigure7.3:(a)moves
fromthemedianandabovethemedian(b)movesfrombelowthemedian
(a)
80
60
40
20
0
0 1 2 3 4
Moves down from above median
(b)
100
60
20
0
0 1 2 3 4
Negative moves up from below median
FIGURE 7.12 Randompriceseries,localmediananalogsofFigure7.4:(a)moves
fromabovethemedianand(b)movesfrombelowthemedium
132

QuantifyingReversionOpportunities 133
(a)
150
50
0
−4 −2 0 2
(b)
2
0
−2
0 200 400 600 800 1,000
FIGURE 7.13 Randompriceseries,signalsfromlocalmedianadjustedserieswith
reversionfromrawseries:(a)histogramand(b)timeseries
(a)
120
80
40
0
−2 0 2 4
Moves from above median
(b)
60
20
0
−2 0 2 4
Negative moves from below median
FIGURE 7.14 Randompriceseries,signalsfromlocalmedianadjustedserieswith
reversionfromrawseries:(a)movesfromabovemedianand(b)movesfrombelow
median
well below the unadjusted series result of 952. Revealed reversion
decreases to 733.
Figure 7.15 is interesting. Notice that there are negative ‘‘moves
down from above the median’’ which is logically impossible! This
reflects the fact that the signals are calculated from the local median

134 STATISTICALARBITRAGE
(a)
60
40
20
0
0 1 2 3 4
Moves down from above median
(b)
60
20
0
0 1 2 3 4
Negative moves up from below median
FIGURE 7.15 Randompriceseries,signalsfromlocalmedianadjustedserieswith
reversionfromrawseries:(a)movesfromabovethemedianand(b)movesfrom
belowthemedian
adjusted price series, but then moves for those signals are calculated
fromtheraw, unadjustedseries.Therelatively fewsmallmagnitude,
negative moves is expected. Curiously in this particular sample,
despitethenegativecontributionstopurereversion,thetotalactually
increases; that is the result of the more-than-offsetting changes in
magnitude of the positive moves (in the raw series compared with
thestandardized series).
Example6 Pricesaredistributedaccordingtothelognormaldistri-
bution. If log X is normally distributed with mean µ and variance
σ2, then X has the lognormal distribution with mean µ = exp(µ+
X
1/2σ2), variance σ2 = exp(2µ+σ2)(exp(σ2)−1), and median
X
exp(µ). Using results for the truncated lognormal distribution from
Johnson and Kotz, Volume 1, p.129, total expected revealed rever-
sion is:
exp(µ+σ2/2)[1−(cid:4)(−σ)]
where (cid:4)(.) denotes the cumulative standard normal distribution
function.DetailsaregiveninAppendix7.1attheendofthischapter.
Figure 7.16 shows the histogram and time series representation of
a random sample of 1,000 draws from the lognormal distribution

QuantifyingReversionOpportunities 135
(a)
400
200
0
0 5 10 15
(b)
15
10
5
0
0 200 400 600 800 1,000
Index
FIGURE 7.16 Randomsamplefromlognormaldistribution(withmedian
subtracted):(a)histogramand(b)timeseries
with µ = 0 and σ = 1. (The median, 1, is subtracted to center the
distributionon0.)Thesamplevalueofexpectedrevealedreversionis
1.08(theoreticalvalueis1.126).Treatingthesampleas atimeseries
inthemannerofExample5,thesampleestimateofpurereversionis
1.346.
7.2.3 Movements from Quantiles Other Than
the Median
The analysis thus far has concentrated on all moves conditional
on today’s price being above or below the median. Figure 7.17
shows that, for the normal and Student t distributions, the median
is the sensible focal point. For example, if we consider the subset of
moves when price exceeds the sixtieth percentile (and, by symmetry
here, does not exceed the fortieth percentile), the expected price
changefromtodaytotomorrowislessthantheexpectedvaluewhen
considering the larger subset of moves that is obtained when price
exceeds the median.
It is expected that this result will not remain true when serially
correlatedseriesareexamined.Tradingstrategiesmustalsoconsider
transaction costs, which are not includedin the analysis here.

136 STATISTICALARBITRAGE
percentile
elitnecrep
htp
>
)t(P
|
)1+t(P-)t(P[E
60
50 Student-t 3
40
normal
30
20
10
0
50 60 70 80 90 100
FIGURE 7.17 Expectedpurereversionbyconditioningpercentileofprice
distribution
7.3 NONSTATIONARY PROCESSES:
INHOMOGENEOUS VARIANCE
Theverystringentassumptionsofthestrictlystationary,independent,
identically distributed (iid) process examined in Section 7.2 are
relaxed in this section. Here we generalize the measures of pure
and revealed reversion to the inhomogeneous variance analog of
the iid process. See Chapter 4 for generalization of the ‘‘75 percent
theorem.’’
Prices are supposed to be generated independently each day
from a distribution in a given family of distributions. The family of
distributions is fixed but the particular member from which price is
generated on a given day is uncertain. Members of the family are
distinguishedonlybythevariance.Propertiesoftherealizedvariance
sequencenowdeterminewhat can be said about thepriceseries.
7.3.1 Sequentially Structured Variances
Conditional on known, but different, variances, each day a normal-
ized price series could be constructed, then the results of Section

QuantifyingReversionOpportunities 137
7.2 would apply directly to that normalized series. Retrospectively,
it is possible to compare a normalized price series with theoretical
expectations (much as we did in Section 7.3 where normalization
was not required); it is also possible to calculate actual pure and
revealed reversion, of course. However, it is not clear that one can
say anything prospectively and therefore construct a trading rule to
exploitexpected reversions.
Onepossibilityis tolookat therangeof variances exhibitedand
anysystematic patternsintheday-to-dayvalues. Intheextremecase
where it is possible to predict very well the variance tomorrow, a
suitable modification of the 75 percent rule and calculation of pure
and revealed reversion ispossible.Such calculationswould beuseful
providing that the same (or, in practice, very similar) circumstances
(variance today versus variance tomorrow) occur often enough to
apply expected values from probability distributions. This may be
a realistic hope as variance clusters frequently characterize financial
series: See Chapter3 for modelingpossibilities.
Asaparticularlysimplespecialcaseofperfectvarianceprediction,
supposethattheonlyvarianceinhomogeneityinapriceseriesisthat
variances on Fridays are always twice the value obtained for the
rest of the week. In this case, there is no need to expend effort
on discovering modified rules or expected reversion values: The 75
percentruleandcalculationsofexpectedpureandrevealedreversion
applyforthepriceserieswithFridaysomitted.Recallthatwearestill
assuming independence day to day so that selective deletion from a
price series history does not affect the validity of results. In practice,
serial correlation precludes such a simple solution. Moreover, why
give up Friday trading if, with a little work, a more general solution
may be derived?
7.3.2 Sequentially Unstructured Variances
This is the case analyzed in detail in Chapter 4, Section 3. For
the normal-inverse Gamma example explored there (see Figure
4.2) the expected reversion calculations yield the following. Actual
revealed reversion is 206.81/999= 0.21 per day; pure reversion is
260.00/999= 0.26perday.Noticethattheratioofpuretorevealed,
0.26/0.21= 1.24, is larger than for the normal example (Example
1) in Section 7.3, 0.94/0.8= 1.18.

138 STATISTICALARBITRAGE
7.4 SERIAL CORRELATION
InSection7.3,theanalysisofstockAA(Example4)showedthatthe
priceseries,actuallythelocalmedianadjustedseries,exhibitedstrong
first-orderautocorrelation,andweakerbutstillnotablesecond-order
autocorrelation. We commented that the presence of that serial
correlation was probably largely responsible for the discrepancy
between the theoretical results on expected reversion for iid series
(75 percent) and the actual amount calculated for the (median
adjusted) series (58 percent). The theoretical result is extended for
serial correlation in Section 4 of Chapter4. Weend thechapterhere
usingtheexample from Chapter4.
Example 7 One thousand terms were generated from a first-order
autoregressive model with serial correlation parameter r = 0.71 and
normally distributed random terms (see Example 1 in Chapter 4).
Figure4.4showsthetimeplotandthesamplemarginaldistribution.
The proportion of reversionary moves exhibited by the series is
62 percent; total revealed reversion is 315 and total pure reversion
is 601. Ignoring serial correlation and using the sample marginal
(a)
100
60
20
0
−3 −2 −1 0 1 2 3
Moves from above median
(b)
100
60
20
0
−2 0 2 4
Negative moves from below median
FIGURE 7.18 Analysisofautocorrelatedseries,Example7:(a)movesfromabove
themedianand(b)movesfrombelowthemedian

139
QuantifyingReversionOpportunities
(a)
150
50
0
| −4  |     |     | −2  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     | 0   |     | 2   |     |
Moves from above median
(b)
80
40
0
|     | −2  | −1  | 0   | 1   |     | 2   | 3   | 4   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Negative moves from below median
| FIGURE | 7.19 Analysisofautocorrelatedmodel,localmedianadjusted:(a)moves |     |     |     |     |     |     |     |
| ------ | --------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
fromabovethemedianand(b)movesfrombelowthemedian
| distribution           | to        | calculate | the result      | in Section | 7.2.2, | the           | theoretical |     |
| ---------------------- | --------- | --------- | --------------- | ---------- | ------ | ------------- | ----------- | --- |
| revealed               | reversion | is        | 592—almost      | double     | the    | actual value. | Figure      |     |
| 7.18illustratesaspects |           |           | of theanalysis. |            |        |               |             |     |
Thelocalmedianadjustedseries(windowlengthof10)isshown
| in Figure    | 4.4; aspects |              | of the reversion |            | assessment | are illustrated |       | in  |
| ------------ | ------------ | ------------ | ---------------- | ---------- | ---------- | --------------- | ----- | --- |
| Figure       | 7.19. A      | slightly     | greater          | proportion | of         | reversionary    | moves |     |
| is exhibited | by           | the adjusted | series,          | 65         | percent    | (compared       | with  | 62  |
percentpreviouslynotedfortherawseries).Totalrevealedreversion
is342(comparedto315intheunadjustedseries);totalpurereversion
| is 605(compared |      | to 601). |                  |     |      |     |     |     |
| --------------- | ---- | -------- | ---------------- | --- | ---- | --- | --- | --- |
| APPENDIX        | 7.1: | DETAILS  | OF THE LOGNORMAL |     | CASE |     |     |     |
| IN EXAMPLE      | 6    |          |                  |     |      |     |     |     |
|                 |      |          | =                | ∼   | ,σ2] |     |     |     |
|                 |      |          | Y logX           | N[µ |      |     |     |     |
Y Y
Set:
|     | E[X]=µ |     | = exp(µ | +σ2/2) |     |     |     |     |
| --- | ------ | --- | ------- | ------ | --- | --- | --- | --- |
|     |        |     | X       | Y      | Y   |     |     |     |

140 STATISTICALARBITRAGE
V[X]=σ2 = exp(2µ +σ2)(exp(σ2)−1)
X Y Y Y
median=exp(µ )
Y
Define Z = X truncated at X (equivalently, Y is truncated at Y =
0 0
logX . Then(Johnsonand Kotz, p. 129):
0
1−(cid:4)(U −σ )
E[Z] = µ = µ 0 Y
Z X 1−(cid:4)(U )
0
where:
logX −µ
U = 0 Y
0
σ
Y
Total expected revealed reversion can be written as E[X|X > m]−
E[X]. Now, E[X|X > m] = E[Z] with X = m = exp(µ ). In this
0 Y
case, U reduces to 0 and:
0
1−(cid:4)(−σ )
µ = µ Y = 2µ [1−(cid:4)(−σ )]
Z X 1−(cid:4)(0) X Y
Therefore, total expectedrevealed reversion is:
2µ [1−(cid:4)(−σ )]−µ =µ [1−(cid:4)(−σ )]
X Y X X Y
=exp(µ +σ2/2)[1−(cid:4)(−σ )]
Y Y Y
√
Special Case µ = 0,σ = 1. Then µ = e,σ2 = e(e−1),X =
Y Y X X 0
median = e0 = 1. Now, U = logX = 0, so that:
0 0
√ 1−(cid:4)(−1) √
µ = e = 2 e[1−(cid:4)(−1)]
Z 1−(cid:4)(0)
From standard statistical tables (see references in Johnson, Kotz,
and Balakrishnan), (cid:4)(−1) = 0.15865 so the mean of the median
truncated lognormaldistribution(with µ = 0,σ = 1) is 2.774.
Y

8
CHAPTER
Nobel Difficulties
Chancefavors the prepared mind.
—LouisPasteur
8.1 INTRODUCTION
Inthischapter,weexaminescenariosthatcreatenegativeresultsfor
statistical arbitrage plays. When operating an investment strategy,
and notwithstanding risk filters and stop loss rules, surprises should
be expected to occur with some frequency. The first demonstration
examines a single pair that exhibits textbook reversionary behavior
until a fundamentaldevelopment, a takeover announcement,creates
abreakpoint.Nextwediscussthetwofoldimpactofaninternational
economic development, the credit crisis of 1998: introducing a new
risk factor into the equity market—temporary price discrimination
as a function of credit rating on corporate debt—and turning a
profitable year (to May) into a negative year (to August). Next we
consider how large redemptions from funds such as hedge, mutual,
and pension, create temporary disruptions to stock price dynamics
with deleterious effects on statistical arbitrage performance. Next
we relate the story of Regulation FD. Finally, in all this discussion
of performance trauma we revisit the theme of Chapter 5, clearing
up misunderstandings, specifically on the matter of correlation of
manager performancein negative returnperiods.
141

142
STATISTICALARBITRAGE
| 8.2 EVENT    |           | RISK       |           |            |         |       |        |               |     |
| ------------ | --------- | ---------- | --------- | ---------- | ------- | ----- | ------ | ------------- | --- |
| Figure       | 8.1 shows |            | the price | histories  | (daily  | close | price, | adjusted      | for |
| stock splits | and       | dividends) |           | for stocks | Federal |       | Home   | Loan Mortgage |     |
Corporation(FRE)andSunamerica,Inc.(SAI)fromJanuary2,1996
| to March    | 31,      | 1998.    | The           | two price | traces | track        | each    | other          | closely |
| ----------- | -------- | -------- | ------------- | --------- | ------ | ------------ | ------- | -------------- | ------- |
| with a      | strong   | upward   | trend,        | the       | spread | between      | the     | two repeatedly |         |
| wideningand |          | closing. |               |           |        |              |         |                |         |
| The         | analysis | and      | demonstration |           |        | that follows | focuses |                | on pair |
spreadtrading,butthesalientpointsonstructuralshiftsarerelevant
| more widely    |           | to statistical |           | arbitrage | models.     | A   | factor       | model forecast- |     |
| -------------- | --------- | -------------- | --------- | --------- | ----------- | --- | ------------ | --------------- | --- |
| ing individual |           | stock          | movements |           | (in groups) |     | is similarly | vulnerable      |     |
| to the         | described | motions,       |           | but the   | mechanics   |     | are more     | involved        | and |
explanationrequiresgreatersubtletyofdetail.Wewillkeeptheanal-
ysissimpleandremindthereaderoncemorethatthebasicpointsare
| applicablemoregenerally |         |     |         | to statistical |     | arbitrage | models.   |              |     |
| ----------------------- | ------- | --- | ------- | -------------- | --- | --------- | --------- | ------------ | --- |
| Daily                   | returns |     | for the | two stocks     |     | do not    | correlate | particularly |     |
strongly;thecorrelationis0.4.However,lookingatreturnsbetween
| events, | the correlation |     | is  | much | higher | at 0.7. | Event | correlation |     |
| ------- | --------------- | --- | --- | ---- | ------ | ------- | ----- | ----------- | --- |
70
SAI
FRE
60
50
40
30
20
10
| 19960102 |     |     | 19961231 |     |     | 19971231 |     | 19980806 |     |
| -------- | --- | --- | -------- | --- | --- | -------- | --- | -------- | --- |
FIGURE 8.1
AdjustedpricehistoriesforFREandSAI

143
NobelDifficulties
70
SAI
FRE
60
50
40
30
20
10
| 19960102   |                                                    | 19961231       |          |            | 19971231     |      | 19980806     |            |
| ---------- | -------------------------------------------------- | -------------- | -------- | ---------- | ------------ | ---- | ------------ | ---------- |
| FIGURE     | 8.2 AdjustedpricehistoriesforFREandSAItoAugust1998 |                |          |            |              |      |              |            |
| indicates  | what                                               | might be       | expected | to         | trade        | well | in groups    | within     |
| prescribed | risk                                               | tolerances(see |          | Chapter2). |              |      |              |            |
| Visually   | and                                                | statistically, |          | it looks   | as though    | the  | pair         | [FRE, SAI] |
| will trade | profitably                                         | in             | a simple | spread     | reversion    |      | model.       | Simulation |
| of a basic | popcorn                                            | process        | model    | (see       | Chapter      | 2)   | demonstrates | that       |
| was indeed | thecase.                                           |                |          |            |              |      |              |            |
| Figure     | 8.2                                                | shows the      | adjusted |            | price series |      | for FRE      | and SAI    |
extendedthroughthesecondquarterof1998toAugust6.Interesting?
| The spread | widened  | considerably      |         | to          | more | than    | double   | the recent  |
| ---------- | -------- | ----------------- | ------- | ----------- | ---- | ------- | -------- | ----------- |
| historical | maximum. | As                | already | noted,      | the  | size of | the      | spread does |
| not give   | rise     | to losing trades, |         | the process | of   | spread  | widening | does.       |
Whenaspreadbeginsapersistentperiodofgrowth,tradestendtobe
| unwound(a)  |          | after a longer   | than    | usual       | period   | and          | (b) when | the local   |
| ----------- | -------- | ---------------- | ------- | ----------- | -------- | ------------ | -------- | ----------- |
| mean spread |          | is substantially |         | different   | from     | where        | it was   | when the    |
| trade was   | entered, | causing          | a       | loss. (This | analysis |              | assumes  | autopilot   |
| application | of       | the forecast     |         | model       | without  | intervention |          | schemes.    |
| Including   | monitors | and              | related | early       | exit     | [stop        | loss]    | rules would |
attenuatelossesbutcomplicatethedescriptionwithoutchangingthe
basic message.)

144 STATISTICALARBITRAGE
Using an exponentially weighted moving average model for an
assumed popcorn process with a constrained trend component (see
Chapter 3) trades in [FRE, SAI] entered in late February lasted
through late April, and trades entered in early June lasted through
early July. Both occasions returned substantial losses. (There was a
fast turnaround,profitabletrade in late July.)
8.2.1 Will Narrowing Spreads Guarantee Profits?
Sadly, there are no guarantees of profitablescenarios. However, one
beneficial asymmetry of decreasing volatility compared to increasing
volatilityis that in theformercase themodel’slagged view works to
advantage when the local mean is changing. (Recall that when the
local mean is not changing, changes in volatility are not a problem,
thoughtheremaybeopportunitycosts,intheformofmissedprofits,
if volatilityforecastsare slow to adapt.)
When the spread local mean is persistently moving in one direc-
tion in excess of the model’s limited pace of adaptation, the strategy
losesbecausethetradeexitpoint(zeroexpectedreturn)isbadrelative
to the trade entry. Contemporaneous entry and exit points exhibit
the proper relationship; the problem arises from changes over time
as thespread developsdifferentlyfromtheforecast madeat thetime
of the trade entry. If the prediction of local volatility is greater than
actualvolatility,thencurrenttradeentrieswillbeconservative(fewer
actualtrades,andeachwithhigherexpectedreturn).Whenthetrend
continuestothedisadvantageofthemodel,thisconservatismreduces
losses,quitethereverseofwhathappenswhenvolatilityisincreasing
and the modelis underestimatingit.
Cutting off losing trades when spread relationships change is
ideal. However, implementing this requires another prediction: a
prediction of the change. Typically the best we can do is identify
change soon after it happens, and characterize it soon after that.
Even thisischallenging.SeeChapter3andthereferenceddiscussion
in Poleet al., 1994.
Looking at current FRE–SAI trades from the perspective of
August1998weask:Mustwemaintainapersistentlylosingposition?
Obviouslynot;apositioncanbeunwoundatamanager’sdiscretion.
But when should the pair be readmitted to the candidate trade
universe?ThehistoricallytightcouplingofFREandSAIseemstobe

NobelDifficulties 145
breakingdown;if thebreakdownappliesto the underlyingcommon
structureofthestockreturnseries,thenthestockswillceasetosatisfy
pairselectioncriteriaandtradingwillcease.Ifthecommonstructure
remains, with spreads oscillating about a new level or returning to
the recent historical level, the stocks will continueto be selected and
will again be traded profitablyoncethedisturbanceisover.
On Thursday August 20, 1998 the takeover of SAI by AIG was
announced. SAI closed on Wednesday at $64 3 the all stock deal
8
valued SAI at a 25 percent premium (before the market opening).
One might seriously wonder at the nature of the buying pressure
behindtherun-upin priceof SAI beforethetakeover.
8.3 RISE OF A NEW RISK FACTOR
The international credit crisis of the summer of 1998 was an inter-
esting time for the practice of statistical arbitrage. Performance
problemsbegan inJuneand,formany,accelerated throughJulyand
August.Duringthistime,itbecamestarklyapparentforthefirsttime
that perceptions about the credit quality of a company had a direct
impact on investor confidence in near-term company valuation. As
sentimentbecamenegativeandstocksweremarked downacrossthe
market, the magnitude of price decline was strongly related to the
credit rating of outstanding corporate debt. Companies with lower
rating had their stock price decimated by a factor of three to one
more than companies with a higher rating. Such dramatic discrimi-
natory action had not previously been described; certainly there was
no prior episodein thehistoryof statistical arbitrage.
There are many hypotheses, fewer now entertained than was the
case at the time, about the nature of the linkages between credit and
equity markets in 1998, and why the price movements were so dra-
matic. Without doubt, the compounding factor of the demise of the
hedge fund Long-Term Capital Management and the unprecedented
salvage operationforcedbytheFederalReserveuponunenthusiastic
investmentbanksheightenedprevalentfearsofsystemicfailureofthe
U.S. financial system. At the naive end of the range of hypotheses is
thetrue,butnotbyitselfsufficient,notionthattheFed’sactionssim-
plyamplifiednormalpanicreactionstoamajoreconomicfailing.An
importantfactorwasthespeedwithwhichinformation,speculation,
gossip, and twaddle was disseminated and the breadth of popular

146 STATISTICALARBITRAGE
coverage from twenty-four hour ‘‘news’’ television channels to the
Internet. The large number of day traders and active individual par-
ticipantsdrawnintothemarketduringthe1990sbytheattractionof
the bull run, and trading made easy by technological developments,
provided a receptive audience for the broadcast noise and a fertile
environment in which to germinate and breed fear and panic. There
was much poor decision making borne of instantaneous judgments,
couched as ‘‘analysis’’ though often little more than the rambling of
the moment to fill immediate desire for sound bites, speedily imple-
mentedbythefacilitatingtechnology.Goodforvolatilityandstudies
of lemming-likebehaviorin cognitivelyhigher orderspecies, bad for
bloodpressureand ulcers.
When the impact of the Russian default began to be experienced
on the U.S. stock markets, concern grew that companies would be
progressively squeezed in the market for credit and this concern
led to stock price markdowns. As the crisis continued and stock
prices declined, the prices of companies with lower credit rating
declined faster and cumulatively by more than prices of companies
with higher credit rating, existentially proving the prevalent fear,
rational or not, that tightening credit markets (the link from the
Russian default to this outcome internationally or specifically in the
UnitedStatesnotconvincingly,coherentlymade)wouldmakeraising
finance more expensive. And what could be more logical than that
poorerratedcompanieswouldhavetopaymore?Theapparentlogic
for discriminatory stock price realignment looks unassailable on the
surface. Since that is as far as much ‘‘analysis’’ went (and goes) the
consequences were those of self fulfilling prophecy. Was there ever
a likelihood of U.S. interest rates being raised as a result of the
Russian default?
Corporate debt rating became a significant discriminatoryfactor
in U.S. equities in the summer of 1998. Any portfolio constructed
absent attention to this factor was likely to be exposed to valuation
loss directly as the lower rated stocks’ prices declined more than
proportionately compared with higher rated stocks. Whether con-
structed as a collection of matched pairs from a vanilla pair trading
strategyorfromasophisticatedfactor-basedreturnpredictionmodel
makes no differenceat theoutset. Lossesare inevitable.
As the discriminatory stock price patterns developed, discrim-
inatory results distinguished types of statistical arbitrage strategy,

NobelDifficulties 147
though manager action in the face of persistent and cumulatively
large losses complicates assessment: the mix of model versus man-
ager (to the extent that is meaningful) being impossible to identify.
Simulation studies devoid of manager contamination indicate that
factor models exhibited more resilience1 than pure spread-based
models, and quickerresumptionof positivereturns.
With recognition of a new risk factor, what should be done?
Factor models, when the factor decomposition is recomputed using
return history from the period affected, will naturally incorporate
‘‘debt rating,’’ so direct action is not necessary. Inaction does beg
a few questions though: What should be done during the evolving
episodeoncethefactorhasbeenidentified(orpositedatleast)?Isthe
bestonecandosimplytowaitforanewwindowofdatafromwhich
to estimate stock exposures to the factor (and meanwhile take a
performancewalloptothechin)?Answertothelatterisobviousbut,
beyond a simple ‘‘No,’’ sensible prescriptions are more demanding
to compose. General specification of the foremost requirement is
direct: Eliminate exposure to the posited factor from the portfolio.
Precise action to accomplish that is a tad more difficult—what are
theexposures?Inthehastenecessitatedbythestrongemotionalpush
and businessneed to staunch losses, luckplayed itsrole.
1Fromwheredoesthisgreaterresiliencederive?Apartialanswercanbeconstructed
bycontrastingabasicpairstrategywithabasicfactormodelstrategy(whichmodels
arepreciselythesourceofthesimulationresultsonwhichtheevidentialcommentary
is made). The pair portfolio consists of bets on pairs of stocks that are matched
onstandardfundamentalmeasuresincludingindustryclassification,capitalization,
and price–earnings ratio. A first-order DLM forecast model is assumed for the
spread(usingthelogpriceratioseries),withanapproximateGARCH-likevariance
law. Bets are made when the spread deviates from its forecast by 15 percent or
more (annualized). All signaled bets are taken and held until the model generates
an exit signal; bets are not rebalanced; no stop loss rule is applied. The factor
model is constructed as described in Chapter 3, with the optimization targeting
annualized15percentforcomparisonwiththepairmodel.Positionsarerebalanced
dailyaccordingtoforecastsandfactorexposures.
There is some evidence that credit rating was correlated with a combination
of the structural factors estimated for the factor model. To the extent that is true,
robustness of model performance to the new risk factor is clearly imparted. The
raw stock universe to which the factor analysis is applied (the trade candidates)
has some impact on results, as it does for the pair strategy. Nonetheless, with the
matchedstockuniverse,thefactormodeldisplayeddesirableperformancerobustness
comparedwiththepairmodel.

148 STATISTICALARBITRAGE
And what of nonfactor models? First, identify how factor risk
is managed in the strategy, then extend the approach to the debt
rating factor. For pair-based strategies, the obvious remedy is to
homogenize all admissible pair combinations with respect to debt
rating. That is, admit only those pair combinations of stocks in
whichthetwoconstituentstockshavesufficientlysimilardebtrating.
Then highly rated stocks will be paired with highly rated stocks,
low rated stocks with low rated stocks, thereby avoiding bets on
stocks that exhibited discordant price moves in response to concern
over the debt factor. Many other aspects of debt rating and related
issues would sensibly be investigated, too, including whether to
employ position weights decreasing with debt rating, restrict low
rated stocks to short positions, or an absolute veto on companies
with very poordebt ratings.
As the research is pursued, an important question to answer
is: What impact would have been seen on past performance of a
strategy from incorporation of new modeling restrictions? It is all
very well to congratulate oneself for finding the proximate cause
of performance problems, to determine and implement prophylactic
changes in one’s modeling, but one also needs to know what impact
on future performance (other than safeguarding when the factor is
activeinanegativesense)islikelytoensue.Moreextensivediscussion
of this subject in a broader context of performance disruption is
presented in Chapter9.
8.4 REDEMPTION TENSION
The pattern of redemption of a broad-based, long-only fund is
perfectly ‘‘designed’’ to adversely impact a fast-turn, long–short
reversion play. Selling off a long-only fund generates asymmetric
pressure on stock prices—it is all one way, down. If the selling is
broadbased,andtosomeextentpersistent,thentheimpactonspread
positionscan be onlynegative.
Itisassumedthat‘‘broadbased’’meansthatasubstantialportion
ofthestockstradedinthereversionstrategyisaffected—assumehalf.
The long portfolio investment strategy, and hence current positions,
is assumed to be unrelated to the reversion strategy: Approximate
this by the assumption that the selling affects equally long and short

NobelDifficulties 149
positions of the reversion strategy. So, ‘‘all’’ affected longs reduce in
valueunderthesellingpressureoftheredemptionactivity,and‘‘all’’
affected shortsreducein liability. On average there shouldbe no net
impact on thereversion strategy.
True ... to begin with. But what has happened to the universe
of spreads in the reversion strategy? Those spreads in which both
the long and the short are affected by the downward price pressure
are essentially unchanged: Assume roughly proportional reductions
in price. (In practice, stocks that have been relatively strong will
be the initial focus of selling as the fire sale lieutenant seeks to
maximize revenue—a one-sided, negative impact on a spread bet.
The resulting price change will be larger for weak stocks when they
aresoldoff,makingthenetresultforareversion-basedbooknegative
rather than nil. For this discussion, we continue with the optimistic
assumption of zero net impact.) But for those spreads in which only
the long or the short is in a stock facing redemption selling, the
spread will change. Some will narrow, making money; some will
widen, losing money. Still net nothing. But those narrowing spreads
lead to bet exits—profit taking. The widening spreads continue
to widen and lose more. Furthermore, continuing price reductions
causethespreadmodeltotakeonnewpositions,whichthenproceed
to lose money as the spreads continue to widen under continued
selling.Ifthesellingcontinueslongenough—andforalargeholding
this is almost guaranteed—the natural trade cycle of the spread
strategy will complete itself and those new trades will exit, locking
in losses.
The picture can get even worse. When the selling is over, some
stocks recover with a similar trend—as if there is persistent buying
pressure. Who knows why that should be—reversion of relative
value!Forthosestocks,newspreadpositionsareentered:Remember,
some previously entered positions finished on their natural dynamic
and so the model is sitting and waiting for new entry conditions.
Bingo,furnishedasthestockpricebeginstoreclaimlostground.And
thelosingspread bet (nowin theoppositedirection)is made again.
High-frequency reversion strategies make lots of bets on small
relative movements. Long-only fund redemptions cause price move-
ments of a cumulatively much larger magnitude; the mechanics
described in this section create the conditions for a blood bath for
statistical arbitrage.

150 STATISTICALARBITRAGE
8.4.1 Supercharged Destruction
A large equity statistical arbitrage portfolio is perfectly designed
to create, on liquidation, guaranteed losing conditions for other
statistical arbitrage portfolios. Size matters because the sell-off of
longsandthebuy-inofshortshastopersistoverthenaturalcycleof
otherplayers.Ifitdoesnot,theninitiallosseswillbereversedbefore
existing trades are unwound; damage is limited largely to (possibly
stomach churning) P&L volatility. Destruction, when it occurs, is
supercharged because both sides of spread bets are simultaneously
adversely affected.
In November 1994 Kidder Peabody, on being acquired, report-
edly eliminated a pair trading portfolio of over $1 billion. Long
Term Capital Management (LTCM), in addition to its advertized,
highlyleveraged,interestinstrumentbets,reportedlyhadalargepair
tradingportfoliothatwasliquidated(August1998)asmassivelosses
elsewhere threatened (and eventuallyundermined)solvency.
8.5 THE STORY OF REGULATION FAIR
DISCLOSURE (FD)
Regulation‘‘FairDisclosure’’wasproposedbytheSEConDecember
20, 1999 and had almost immediate practical impact. That imme-
diacy, ten months before the rule was officially adopted, is stark
testament to some of the egregious behavior of Wall Street analysts
now infamous for such practices as promoting a stock to clients
while privately disparaging it, or changing a negative opinion to a
positiveopiniontowinunderwritingbusinessandthenrestoringthe
negative opinion!
Activities eventually outlawed by Regulation FD had dramatic
negative impact on statistical arbitrage portfolios in 1999. Most
readilyidentifiablewastheselectivedisclosureofearningsinthedays
before official announcements. Typically, favored analysts would
receive a tip from a CEO or CFO. Analysts and favored clients
could then act on information before it became public. If the news
was good, a stock’s price would rise under buying pressure from
the in-crowd, statistical models would signal the relative strength
against matched stocks, and the stock would be shorted. Days later
when the news was made public, general enthusiasm would bid up

NobelDifficulties 151
the stock price further, generating losses on those short positions.
Long positions, signaled when the news was disappointing, suffered
similarly as prices declined, a lose–lose situation for short-term
statistical strategies.
Thispatternofbehaviorbecamesorifethatmanymarketpartic-
ipants yelled vituperation; the SEC heard and acted. Notable effects
of thepractice disappeared almost overnight.
Privileged information passed to analysts was not a new phe-
nomenonin1999.Widespreadabuseoftheprivilegewasnew,orsoit
seemsfromtheeventsjustoutlined.Ifabuseexistedpreviously,itwas
notnoticed.Aninterestingsidenotetothestoryistheeffectivenessof
analysts. Many analysts with star reputationsformaking timelyand
accurate forecasts of company performance became run-of-the-mill
forecasters after RegulationFD was announced.
8.6 CORRELATION DURING LOSS EPISODES
An investor lament heard when enduringportfoliolosses:
‘‘Your results are [highly] correlated with those of other mana-
gers...’’ The implication here is that similar bets are being made,
contradicting claims of differentiation through different methods of
stock universe selection, trade identification (forecast model), and
resulting trade characteristics such as holding period. Are the claims
of differentiationfalse? Is the performancecorrelationcoincidental?
Two distinct, broadly based portfolios of stocks traded with a
reversion model are very likely to exhibit high coincidence of losing
periods.Whennormalmarketbehavior(patternsofpricemovement
resulting from investor activities in normal times) is disrupted by an
event, international credit crisis and war are two recent examples,
there is a notable aggregate effect on stock prices: Recent trends of
relativestrengthandweaknessarepromoted.Duringeventoccasions
(and it is a near universal rule that ‘‘event’’ is synonymous with
‘‘bad’’ news), sell-off activity is always the result. Stocks perceived
as weak are sold off first and to a greater extent than stocks that
are perceived as strong (or, at least, not weak). This is the reverse
of what is expected from a fund satisfying redemption notices—see
Section 8.4. The implication for spread trades is blindingly obvious:
losses. Regardless of the precise definition of a manager’s strategy,

152 STATISTICALARBITRAGE
tradable universe, or specific collection of active bets at the time,
the common characteristic of all spread reversion bets, at a point in
time, is that stocks judged (relatively) weak are held long and stocks
judged (relatively) strong are held short. Mark to market losses
are inevitable.
The magnitude of losses, duration of losing streak, and time to
recovery will vary among managers, being strongly influenced by
individualreversion modelsand manager risk decisions.
Anyeconomic,political,orotherhappeningthatcausesinvestors
to become generally fearful instills a sell mentality. This has an
unambiguouseffectonallbroad-basedportfoliosofspreadpositions
on which mean reversion is being practiced. Unequivocally, perfor-
mance turns negative; directional correlation of managers is high.
Interestingly,numericalcorrelationmaynotbehigh.Themagnitude
of returns in negative performance periods can be quite different for
distinct portfolios. There is nothing in the rationale of fear-based
selling to suggest it should be ordered, evenly distributed across
market sectorsorcompanycapitalizations,orinanyotherway tidy.
Typically, a lot of untidinessshouldbe expected.Hence, whileman-
agers should be expected to experience common periods of unusual
losses, the correlation of actual returns in losing periods examined
collectively and separately from returns in winning periods may be
positive, negative, orzero.
Losing periods are always followed by winning periods, by defi-
nition. Extended intervals of market disruption punctuated by relief
must, on the arguments given, create similar patterns of losing and
winningintervalsforspread reversion strategies.
And what can one say about relative performance of strategies
duringgenerallypositiveperiodsforspreadtrading?Lesscorrespon-
dence of returns for distinct strategies is to be expected. Returns
are dependenton the precisedynamic moves exploitedby individual
models. There is no unifying force creating short-, medium-, and
long-term dispersion followed by reversion that parallels the neg-
ative influence of fear. Exuberance is, perhaps, the closest to such
a force, creating reversionary opportunities randomly and at large.
But exuberance is less tangible than fear. It is less likely to induce
common decisions or actions. Investment results for collections of
managers will exhibit looser correspondence, greater heterogeneity
than in periods unfavorableto reversion.

NobelDifficulties 153
Fund A Return %
%
nruteR
B
dnuF
2
1
0
−1
−2
−1 0 1 2
FIGURE 8.3 MonthlyreturnsforfundAandfundB,illustratingthefallacyof
correlation
Figure 8.3 illustrates the typical situation. Overall, fund A and
fundB showpositivelycorrelated returns, with a modest correlation
of 0.4. This correlation result is driven by the two quadrants where
both funds are winners or both are losers (positive–positive and
negative–negative)inwhichmosttradingoutcomeslie.Withinthose
two quadrants, the good and the bad strategy periods, correlation
is negative: −0.19 in the bad times and −0.22 in the good times.
This seeming contradiction, positive overall correlation but negative
correlation in all dominant subperiods, is an example of the fallacy
of correlation. Notice that the strength of the relationship between
returns in the negative quadrant is actually lower, at 0.19, than
in the positive quadrant (0.22), which is contrary to the general
expectation described earlier. This example serves to illustrate a
common theme described several times in the text, that while we
canidentifyandcharacterizepatterns—generaloraverage—thereis
always variability to appreciate and contend with. Notice, too, that
there are only ten data points in the negative quadrant, barely one

154 STATISTICALARBITRAGE
quarterofthatnumberinthepositivequadrant.Thus,thecorrelation
is less well estimated (there are fewer degrees of freedom, or pieces
ofinformation,instatisticalparlance).Andtenisasmallnumberfor
estimatinga variable relationship—isn’t it?
Itisnotsurprisingthatlosingperiodsareexperiencedincommon
by different spread reversion strategies. The visibility of such cor-
relation following two extraordinary years of market disruption is
understandable. Understanding why the result is obtained is impor-
tant: Attention is more likely to be rewarded if focus is shifted from
contemplating the unexceptional coincidence of negative returns to
examining where losses have best been contained. Attention should
also be focused on the prospects for a resurgence of the drivers of
spread reversion—on when and whetherthosedriverswill reemerge
strongly enough to create systematically profitable opportunities
for managers (see Chapter 11). Here, there is real possibility of
distinguishingfuturelikelywinners and losers.

9
CHAPTER
Trinity Troubles
Extinctionoccurs because selectionpromotes what is
immediatelyuseful even if the changemay befatal in the
longrun.
—T. Dobzhansky.1958.‘‘Evolutionat Work.’’
Science 1,091–1,098
9.1 INTRODUCTION
Beginning in early 2000, after nearly two decades of outstanding
profitability, the returns of many statistical arbitrage managers
collapsed to zero or worse. Some managers continued to generate
excellent returns for two more years but they, too, ceased to per-
form starting in early 2002. The split into failures and successes
in 2000 is an interesting historical point in the story of statistical
arbitrage, demarcating a state change in high frequency reversion
dynamics. Of greater significance because of its universal effect, the
performance watershed in 2002 was considered by many to mark
the death of statistical arbitrage as an absolute return generator,
though there remained a few observers who discerned temporary
structural problems and posited conditions under which statistical
arbitrage would rise again. Coherent analysis was not abundant,
investorpatiencewasrarer even thanthat,and thelatterbecamethe
realdeathknellasitledtoinvestmentwithdrawal,leavingmanagers
unableto meet payroll.
Attheendof2005thatwasthedirestateofstatistical arbitrage;
as an investment discipline it had become an unsaleable product.
The year 2006 saw a resurgence in performance, vindicating those
who had maintained that the performance collapse was explained
155

156 STATISTICALARBITRAGE
by a multiplicity of factors, many of which were transitory. With
the passing of those temporary disruptions to market coherence and
consistentlypredictablesecuritypricedynamics,thelikelypossibility
of a new productive period for statistical arbitrage was anticipated.
We are nownearly two years intojust that renewal.
In this chapter, we begin by examining several one-liners loudly
touted as the cause of statistical arbitrage return decline. While each
may havehad somenegative impact,it isunlikelythatthecombined
effecthasbeenmorethan30percentofhistoricalreturn.Asignificant
reduction, but not a coffin maker for the strategy. Next we expand
the perspective to consider major developments in the U.S. economy
and financial markets, describing the degree to which the impact on
statistical arbitrage is transient. One perspective on 2003 is offered
to set thecontext of thediscussion.
Chapter 10 continues the theme of searching for reasons for
performance decline and sources of a revival. The focus is on tech-
nical developmentsby large brokerage houses. Long-term impact on
statisticalarbitrageiscertain,negativeformanyextantstrategiesbut
creating new opportunities with increasing use of the tools by large
market participants(Chapter11).
9.2 DECIMALIZATION
‘‘The bid–ask spread reduced from a quarter to two cents has
eliminated thestatistical arbitrage edge.’’
Strategiesmaygobythesamegenericname,statisticalarbitrage,
but there are important distinctions that are critical to under-
standing performance disparities over the last few years as well
as prospects for future performance. Starting in mid-2000, prac-
titioners of high-frequency statistical arbitrage generally achieved
a poor return, in many cases actually negative for much of 2000
and 2001. The declining bid–ask spread, from prices quoted in
eighths to sixteenths to pennies, had an enormous negative impact
on thosereturns. Furthermore,consolidationof floorspecialistsinto
the now five majors plus two small independents resulted in much
of the intraday and day-to-day price reversion being internalized by
those specialists. With research budgets, computers, and manpower
resourcesexceedingmoststatisticalarbitragefundmanagers,andthe

TrinityTroubles 157
unfair advantage of order flow visibility, it should not be a surprise
that thishas happened(see Chapter10).
The statistical arbitrage edge was not eliminated. But the high-
frequencyopportunitywasspeedilyremovedfromthepublicdomain
and monopolized by a favored few. Strategies with a holding period
extendingover weeks or months rather than days were largely unaf-
fected by the change to decimalization. This dynamic characteristic
of models was significant in explaining the performance split over
2000–2002 described in the opening section of the chapter. To
thoseexploitingareversionprocessfundamentallydifferentfromthe
high-frequency strategies, the contribution to profit of longer term
betsfrombid–askspreadswasfractional.Theremayhavebeensome
performance deterioration from poorer execution, but not outright
elimination.Tosee this,let’s takea lookat some examples.
Consider an average stock priced at $40 per share. Suppose that
thegoalofastrategyistoearn12percentperannum,or1percenta
monthonaverage.Withaholdingperiodoftwomonths,areversion
bet is expected, on average, to yield 2 percent, or 80 cents. The loss
of the long-time standard bid–ask spread of a quarter, now reduced
to a couple of cents following decimalization, can at most have
eliminated one-thirdof the expected gain on a bet. Annual return is,
therefore,reducedfrom12percent to8 percent.Thisisaworst-case
analysis that ignores the ameliorating possibilities available from
trade timing tactics when trades can be made over several days—an
optionnotavailabletohigherfrequencystrategies.Theactualimpact
of decimalizationon the longerterm strategy is moremarginal.
The story doesn’t end with decimalization, of course, as sub-
sequent sections of this chapter show. Surviving the switch to
decimalization, showing longer term statistical arbitrage strategies
to splendid advantage in 2000 and 2001, did not help counter other
structural changes that cumulatedover 2002and 2003.
9.2.1 European Experience
The European markets have been decimalized for decades yet
high-frequency statistical arbitrage has developed successfully over
the same time. The conclusion must be that decimalization itself
is not a barrier to profit opportunity for the strategy; performance
problems are created by changes in market structure which causes

158 STATISTICALARBITRAGE
changesintemporaldynamics,disruptingthepatternsthatstatistical
arbitrageurs’ modelsare builtto predict.European marketsare fully
electronic, closer to the NASDAQ than the NYSE in that respect.
Yet statistical arbitrage in all those markets failed to generate a
returnin2003–2004.Whileitispossiblethatdifferentcausalfactors
explain the lack of performance in each of the ‘‘three markets,’’ it
is more likely that a common factor was active. What candidates
might be implicated? The early part of 2003 was dominated by the
Iraq war. But what of the final six months? And 2004? Economic
news gradually shifted from the uniformly gloomy and pessimistic
to generally optimistic, though the negative baggage of U.S. budget
and trade deficits caused much consternation (on the part of com-
mentators and professional economists). It is this change, and the
commensurate changes in investor behavior, that caused the non-
performanceofstatistical arbitrageacrossmarketsand managers. In
each of the markets, other market specific factors undoubtedly were
also present.
9.2.2 Advocating the Devil
Having just argued that decimalization was not a significant factor
in the reduction of return in statistical arbitrage, except for some
high-frequency strategies, let’s consider how the change could have
been detrimental.
There is a lot of anecdotal evidence that liquidity within the day
has changed directly as a result of decimalization: How do these
changes relate to the day-to-day price behavior and trading volume
for statistical arbitrage? Prima facie evidence, the decline of strategy
return, is that market price patterns changed. How? In what ways?
Can a logical connection be made between the observed changes,
decimalization, and statistical arbitrage performance? Without con-
sidering the purported changed mechanics of intraday pricing, let us
supposetheclaimofchangetobecorrect.Whataretheimplications
fordaily pricebehavior?
Can a process be elucidated under which continuous trading
from 9:30 a.m. through 4 p.m. will, ceteris paribus, generate daily
price patterns structurally, notably, describably different depending
on the size of the individual market price increment? If not, then
systematic trading models evaluated on daily closing prices will also

TrinityTroubles 159
not exhibit distinguishable outcomes except to the extent that the
bid–ask spread (at the close) is somehow captured by a strategy.
In fact, simulations of many such models exhibited poor returns
over 2003–2004. Either the observable, acknowledged, structural
changes to price moves within the day resulting from the change to
decimal quotes and penny increments led to change in the structure
ofend-of-daypricesacrosstime,orsomefactororfactorsotherthan
thechange to decimalizationexplain thesimulationoutcome.
If a contrary observation had been made, then a plausible argu-
mentfromdecimalizationtosystematictradingstrategyreturncould
beconstructed:Ifday-to-daytradingshowspositivereturnbutintra-
day trading shows no return then price moves in reaction to trades
eliminate the opportunity. The evidence to date neither supports
nor contradicts such a hypothesis. It is much more likely than not
that decimalization was a bit player in the explanation of statistical
arbitrage performancedecline.
Suppose that statistical arbitrage’s historical performance was
derived solely from systematic obtaining of the consumer surplus
when spreads jump over a trade threshold and fills are obtained at
or better than even that ‘‘excess.’’ If decimalization reduces, almost
to nil, the jump and, we might reasonably suppose (supported by
experience),priceimprovement,too,thentheexpectedreturnofbets
similarly reduces to almost nil. This scenario is seductive until one
realizesthatitislittlemorethananelaborationofthebid–askspread
argument.Theconsumersurplusofthejumppluspriceimprovement
is quite simply the bid–ask spread (jump) plus price improvement.
Unlesspriceimprovementwasamajorcomponentofstrategyreturn,
this argument is reduced to dust.
9.3 STAT. ARB. ARBED AWAY
‘‘Stat.arb.hasnotgeneratedareturnintwoyears.It’sedgehasbeen
‘arbed’ away.’’
Thiswasheardwithgrowingclamoras2004rolledon.Butwhat
kindofevidenceisthereforthedismissal?Withnothingfurtherthan
the observation of recent history offered to support the claim, we
must suppose that the performance evidence was deemed sufficient
proof. As such, the argument is refuted simply by looking a little

160 STATISTICALARBITRAGE
further back. Over the 18 months from mid-1998 through the end
of 1999, the strategy yielded almost nil return (factor-based models
faredbetterthanothers),yetthesubsequenttwoyearsyieldedrecord
rates of return.
An extended period of flat performance does not prove that
patternsofstockpricebehavior,thesourceofreturnfromsystematic
exploitation, have ceased to exist. Equally, there is no reason to
suppose, solely by examining the numbers, that unusually large
returns,oranyparticularpatternofreturns,willbeobtainedassoon
as a dry spell ends or, indeed, that there will be an end thereto. To
understand what is possible, one needs to understand the nature of
the stock price movements, the inefficiency that is exploited by the
strategy, and how exploitation is achieved. To go further and posit
what is likely requires one to make statements about various states
of the world and to make forecasts (Chapter 11). Now, of course,
the claim can also be refuted by looking forward from when it was
made to today. Literally, there have been many happy statistical
arbitrage returns.
9.4 COMPETITION
‘‘Competitionhas eliminatedthe stat. arb. game.’’
It is tempting to dismiss this claim in an equally disdainful man-
ner as in which it is presented. Leaving aside the implicit belittling
of statistical arbitrage as a ‘‘game,’’ those who practice it as such
are playing roulette. Winning streaks are possible but when things
go wrong the gamesters have no substance to fall back on. Rash
action, desperation, and inglorious exit from the industry follow.
For those who understand the drivers of their strategy and the sub-
tleties of its implementation, shocks are survived through discipline
and control.
Did competition eliminate risk arbitrage as an investment strat-
egy? Quite! The dearth of opportunity during 2002–2005 was not
because of a greater number of practitioners or increasing assets
managed in the strategy, both of which preceded the return decline,
but because of the structural change in the economy. As 2005 drew
to a close, anticipation was already building that merger activity
would increase, resuscitating the merger arbitrage business, with
just a few months of consistently positive economic news. Increased

TrinityTroubles 161
participationinthebusinesswillhaveanimpactonreturnasactivity
increases. The gains will be smaller on average; better, more expe-
rienced managers will do well if they discover and exploit the new
patterns described in Chapter 11; neophytes, relying on traditional
ideas, will have a moredifficulttime. Luckwill playno small role.
What is the difference between merger and statistical arbi-
trage such that massive structural change in the economy—caused
by reactions to terrorist attacks, wars, and a series of corporate
misdeeds—was accepted as temporarily interrupting the business of
one but terminating it (a judgment now known to be wrong) for the
other?Immenselyimportantisanunderstandingofthesourceofthe
returngeneratedbythebusinessandtheconditionsunderwhichthat
sourcepertains.Themagicwords‘‘dealflow’’echoininvestorheads
the moment merger arbitrage is mentioned. A visceral understand-
ing provides a comfortable intellectual hook: When the economy
improves (undefined—another internalized ‘‘understanding’’) there
will be a resurgence in management interest in risk taking. Mergers
and acquisitions will happen. The game will resume after an inter-
lude. There is no convenient label for the driver of opportunities in
statistical arbitrage (although some grasp at ‘‘volatility’’ in the hope
of an easy anchor—and partially it may be). There is no visceral
understanding of or belief in how statistical arbitrage works; noth-
ing to relate to observable macroeconomic developments; no simple
indicatortowatch.Beyondthevisceralonehastothinkdeeply.That
is difficult and, hence, there is much uncertainty, confusion, and
an unavoidable scramble to the conservative ‘‘Statistical arbitrage is
dead.’’ Howis theResurrection viewed, I wonder?
The competition argument deserves serious attention. Though
therearenopubliclyavailablefiguresrecordingtheamountofcapital
devoted by hedge funds and proprietary trading desks of investment
banks to systematic equity trading strategies, it can be deduced
from the remarks of clearing brokers; investors; listings in Barron’s,
Altvest, and so forth that both the number of funds and the amount
of money devoted to the discipline increased greatly before 2000.
An immediate counter to this observation as evidence supporting
the competition hypothesis is that the increase in assets and number
of managers has been taking place for two decades yet only with
performancedroughtisalinktoasset-classperformancebeingmade.
Statistical arbitrage performance did not decline in tandem with a

162 STATISTICALARBITRAGE
view of how assets/managers increased. The hypothesis was offered
onlytoexplainthecessationofperformancefortwoyears;anabrupt
halt to a preceding excellent history. The hypothesis requires, to
overcome the ‘‘convenient but not adequately matched to evidence’’
tag, an explanation of why the competition effect only recently, and
dramatically, became apparent.
Withthemarketinsteepdeclinefrom2000–2002,investorspre-
viously shy of hedge funds, including statistical arbitrage, increased
allocations to alternative investment disciplines. Therefore, it may
be argued that there was a step change (increase) in investment in
statistical arbitrage in 2002.
But ... it didnot all happenat thebeginningof 2002,did it?
What other evidence, besides assets invested in and number
of practicing managers, can be sought to support or discredit the
competition hypothesis? The superficial argument considered thus
far, increased attention correlated with poor performance, is barely
an argument at all; it is really only a coincidence of observations
with correlation taken for causality and no explanation of how a
causal mechanism might be expected to work. Thesimplest scenario
is ‘‘many managers were competing to trade the same stocks at the
same prices.’’ Even an approximation to this would be revealed to
participants through liquidity problems—unfilled trades, increased
slippage on filled trades, for example. Evidence to support such an
explanationhas notbeen widely claimed.
If competition during trading eliminates the ‘‘consumer sur-
plus’’andpriceimprovement(historicallypartofstatisticalarbitrage
return) then once again the effect should be visible in end-of-day
closingprices. Thefact thatmany betscontinuetobeidentifiedwith
a substantial consumer surplus component belies the argument. The
reduction in number of opportunities is directly related to volatility,
whichmayverywellbereducedinsomepartbygreatercompetition
among a larger number of statistical arbitrage managers. That still
leaves the important question: Why is the sum total of return on the
identifiedopportunitiesreduced to zero?
Let us accept that competition in systematic trading of equities
has increased. There is no evidence, notwithstanding performance
problems, to support concomitant increase of market impact, and
consequentlynoevidencethatgreatercompetitionisthemajorcause
of the declineof statistical arbitrage performance.

TrinityTroubles 163
9.5 INSTITUTIONAL INVESTORS
‘‘Pensionfundsandmutualfundshavebecomemoreefficientintheir
trading.’’
Threeyearsofmarketdeclinepushedmanyinstitutionalinvestors
toenormousefforttoreducecostsand,hence,lossesasreturngenera-
tioneludedmost;transactioncostswereprimetargets.Theargument
is that reversion opportunities historically set up by the large block
trades disappeared as traders of those blocks became smarter with
∗
theirtrading. ‘‘Fidelityhasbeen a ‘VWAP shop’forseveral years’’
is frequently heard as shorthand for the argument. Once again, we
must note that these changes did not happen overnight. To the
extent that such changes have been a factor in statistical arbitrage
performance decline, it is confounded with other changes. Assess-
ing the impact appears to be an insurmountable practical problem.
Certainly, institutional investors are major users of the trading tools
described in Chapter 10 and a substantial impact—negative for
statistical arbitrage—is undoubted.
9.6 VOLATILITY IS THE KEY
‘‘Marketvolatilitytickedup—isn’tthatsupposedtobegoodforstat.
arb.?’’
Fromthebeginningof2002,peoplebegansearchingforexplana-
tionsforthelackofreturnfromstatisticalarbitragestrategies.Many
managers had experienced a meager year in 2001 though many oth-
ers had a good year. But shortly into 2002 managers everywhere
(almost)wereexperiencingpoorperformance.Thedeclineinmarket
volatility was dragooned into service as ‘‘the’’ explanation for the
lack of statistical arbitrage performance. Impressively quickly the
volatility explanation became Antilochus’ hedgehog, a single ‘‘big’’
idea. Combined with investor pleading for silver bullet solutions to
theperformancedrought,observersmightbeforgivenforwondering
if they had entered a film set! This chapter and the sequel stand as
explanationin themodeof Antilochus’fox: many‘‘small’’ ideas.
∗VolumeWeightedAveragePrice.

164 STATISTICALARBITRAGE
0.15
0.10
0.05
199503 199703 199903 200103 200303
FIGURE 9.1 S&P500withinindustryaveragelocalpairwisevolatility
Spread bets exploitrelative price movement between stocks. It is
interstock volatility that is critical for performance; and interstock
volatility, while constrained by market volatility, is not a simple
function of it (see Chapter 6). Often interstock volatility moves in
the contrary direction to market volatility. In the third quarter of
2003, interstock volatility declined to a record low, even as market
volatilityincreased. Thedeclinecontinuedthrough 2004.
Justasinterstockvolatilityisnotsimplyrelatedtomarketvolatil-
ity, so the level of interstock volatility is also not simply related to
strategy profitability. Only a small proportion of the total volatility
is systematically exploited by spread models; large changes in the
levelofinterstockvolatilityareobservedtohaveonlyasmallimpact
onthemagnitudeofstrategyreturn(exceptwhenvolatilitydecreases
to extremely low levels as seen in 2004 and except for more sophis-
ticated models which capture more of the raw volatility) a larger
impact is observed on the variability of the return. Both relation-
ships are well demonstrated by the contrasting market conditions
andstrategyperformanceinthefirstandthirdquartersof2003.The

TrinityTroubles 165
record low level of interstock volatility in quarter three preempted
consistent profitability for the first time that year; volatility was
20 percent higher in the first quarter, yet performance was wholly
negative.
In September 2003, interstock volatility declined to a record
low level, yet reversion opportunities were rich. Statistical arbi-
trage strategies generated a 1 percent return unleveraged in two
weeks.
Unfortunately the trading activity of Janus, funding $4.4 billion
of redemptions precipitated by the firm’s disclosure of participation
in mutual fund timing schemes in contravention to statements in
fund declarations, disrupted price relationships in the second half
of the month. A corollary of the Janus story (the redemption detail
was published in the Financial Times on Friday, October 10) is that
almost certainly more ‘‘disruption’’ should have been anticipated
for October. Morningstar (Financial Times, Thursday, October 9)
advised investors to reduce or eliminate holdings in mutual funds
from Alliance Capital and Bank of America, as managers of those
fundshad also engaged in timingschemes.
9.6.1 Interest Rates and Volatility
Withverylowinterestrates,thevalueofadollarayearfromnow(or
five years orten years) is essentiallythesame as thevalue of a dollar
today. Notions of valuation of growth are dramatically different
thanwhenhigherinterestratesprevail,whentimehasadollarvalue.
Withsuchequalizationofvaluationsandwithdiscriminatoryfactors
rendered impotent, volatility between similar stocks will decrease.
Higher interest rates are one factor that will increase stock price
discrimination and increase the prevalence and richness of reversion
opportunities. The process of increasing interest rates began at the
end of 2004. The Federal Reserve raised rates in a long, unbroken
sequenceofsmallstepsto5percent,andstatisticalarbitagegenerated
decent returns again starting in 2006.
Volatilityhasnotincreasedsince2004.Indeed,itdeclinedfurther
torecordlowlevels.Canvolatilityrisetohistoricallevels?Absolutely.
Butthedevelopmentscitedhere,theriseofVWAP,participationand
relatedtrading,andthetradingtoolsdescribedinChapter10strongly
suggest that it wouldbefoolishto bet on it.

166 STATISTICALARBITRAGE
9.7 TEMPORAL CONSIDERATIONS
The foregoing analysis is entirely static in focus: decimalization,
competition, and so forth are not apparent for any individual trade
(on average) as evidenced through slippage calculations. (If you
prefer,conservatively,thereisimpactbutthemagnitudeisinsufficient
to cause the outcome of zero return.) Statistical arbitrage is not
simply a collection of individual trades either in distinct stocks,
or pairs of stocks, or more general collections of stocks. It is a
collection of linked trades related over time. The temporal aspect of
the trades is the source of strategy profit; trades at a point in time
are the means by which the opportunity is exploited. The foregoing
argumentdemonstratesthatcompetitionhasnotinhibitedtheability
ofmanagerstoexploitidentifiedopportunities.Buthascompetition,
or decimalization, or something else altered the temporal structure,
the evolution, of prices such that identified patterns ceased to yield
a positive return? Did short-term stock price structure change such
that systematic trading models were reduced to noise models? If
so, can the progenitor forces driving the evolution be identified?
Was decimalization or competition influential? Were they active
agents,catalysts,orsimplycoincidentalelements?Aretheystillactive
factors? If there are other factors, how have they caused structural
change? Is the process over? Is there a new stable state—now or yet
to be—established, orwill the statusquobe restored?
Once again, the starting point is the observation that statistical
arbitrage strategies, historically yielding good returns, did not gen-
erate a decent positive return in most cases in at least three years
through 2005. Many such strategies lost money in one or more of
those years. The foregoing analysis has considered widely posited
hypotheses that performance was crowded out by changes effective
at the point of trade placement and shown them not to reliably or
reasonably provide an explanation of the observed pattern of trad-
ing and opportunity set identification. What about the hypothesis
that from the same changes—decimalization, competition, or other
unidentified factors in conjunction therewith—has arisen a change
in the temporal structure of stock price behavior such that previ-
ous models that once had identifiable and systematically exploitable
forecast power now have none? What would one expect to see from
systematic trading strategies if the signal component of the model

TrinityTroubles 167
was reduced to noise? Bets would be placed that, on average (and
hence in the aggregate), have zero expected return. With random
elements and varying degrees of expertise on the part of managers
executing trades, systematic strategies would yield zero to negative
performance (transaction costs providing a negative bias to the zero
expected return of raw trades).
Onthefaceofit,threeyearsofessentiallyflatreturnbythe‘‘class’’
fits the hypothesis. Is there specific evidence that one might look for
to determine if the hypothesis is merely a fit to the observation
of overall performance or drove the result? If a model has no
forecastingpower,thenforecastreturnsshouldbeuncorrelatedwith
actual returns for a collection of identified bets. The evidence of one
fund is known in some detail. Unequivocally, the evidence refutes
the hypothesis. For the majority of trades over the three years, the
correlation between forecast return and achieved return is positive
(andstatisticallysignificant).Manyofthetradesgeneratedapositive
return, though, on average, a lower return than in previous years.
The minority of losing trades made bigger losses. This is the crux
oftheperformanceproblemformanystatisticalarbitragemanagers,
though there are some additional elements that contribute to the
story and have implications for prospective results. In somewhat
handwavingterms,onecancharacterizethesituationasfollows:The
signalremainedpresent(generallyhighpercentageofwinningbets);it
wassomewhatweaker(lowerrateofreturnonround-trip,completed
bets);thedynamicbecameerratic(variablylongerorshorterholding
periods); and the environmental noise increased (higher variance
on losing bets, proportion of winning bets, location of consistent
reversion).
An archetypal example of a wave function, a ripple in a pond, a
sinusoid for those of a technical bent, helps illustrate these compo-
nents,theircontributiontobet performance,andtheimplicationsof
thechanges discussed (Figure9.2).
Tobeginwith,rememberthatnoiseis good:Supposethatobser-
vations were simply scattered about the pure signal with an additive
random element, that is y = µ +(cid:1) with (cid:1) ∼ [0, σ]. Then a large
t t t t
noise variance σ would generate series such as Figure 9.3 compared
to lownoiseFigure9.4.
The same signal in Figure 9.3 admits a greater return through
understanding of the signal (model) and the impact of the noise

6.0
period
5.5
amplitude
5.0
4.5
4.0
0 20 40 60 80 100
FIGURE 9.2 Sinewave
8
a
7
6
5
4
c
3
b
2
0 20 40 60 80 100
FIGURE 9.3 Spreadswithunderlyingsinewavesignal
168

TrinityTroubles 169
8
7
6
5
4
3
2
0 20 40 60 80 100
FIGURE 9.4 Lowvolatilityspreadswithunderlyingsinewavesignal
component. We know where the signal is going and we know how
much variation about the signal may be preempted by the noise.
This leads one immediately to modify a simple exploitation of the
signal forecast, to one that also exploits knowledge of the variation
anticipated from noise. Rather than exiting a bet when the model
forecasts 0, one identifies an interval around the 0 and waits for
an outcome much to one’s favor that will occur according to the
distribution of the noise. This phenomenon is known as stochastic
resonance(seeChapter3).Enterata,exitatb andnotatc.Therewill
begainsandlosses(missedtrades,opportunitycosts)comparedtothe
‘‘exploit the signal’’ model; on average, with good calibration, one
will gain. Clearly, the trade-off of a noise gain against opportunity
cost (capital not available for another new bet) is different—there is
much less potentialnoisegain—in Figure9.4.
In 2003–2004, much commentary was made about the inaction
of institutional money managers; ‘‘sitting on the sidelines’’ is an apt
descriptionofboththelackofcommitmenttoactivedecisionmaking
and the wait-and-see posture adopted in response to a backdrop of
pooreconomicand political news, not to mentionan unprecedented

170 STATISTICALARBITRAGE
three-year rout of equity markets. This reduced level of investing
activity makes an impact on reversion structure (in prices of similar
stocks largely owned by institutions and followed by professional
analysts) in several ways. Foremost is the slowing down of the pace
of reversion—an increase in the period of oscillation in the wave
functioninFigure9.2.Pullaparttheendsofthewaveinthatfigure...
and ... things ... move ... more ... slowly. If nothing else changed,
this dynamic shift alone would dramatically reduce strategy return:
If it takes twice as long for a move to occur, then return from that
move ishalved.
Thepracticalimpactislargerthanthearchetypesuggests; return
isreducedbymorethanhalf,becausetherearecompoundingfactors.
Probably the most significant factor is the ability of a modeler to
recognize the occurrence of the change of dynamic and modify
models appropriately. Working with mathematical archetypes, one
can immediately identify and diagnose the nature of a change (of
periodinasinusoid,forexample).Withnoisydatainwhichthesignal
is heavily embedded in extraneous variation, the task is enormously
more difficult. In many cases, the change is swamped by the noise,
which itself may exhibit altered distribution characteristics as we
are seldom so fortunate that change occurs one factor at a time
or in some other conveniently ordered manner, with the result that
detectionofthechangetakestime—evidencehastobeaccumulated.
Delaysfromidentifyingachangeindynamicresultinreducedreturn
fromsystematic signal exploitation.
The process of change adds yet another level of complexity and
anothersourceofdragonreturn.Implicitintheprecedingdiscussion
has been the notion of instantaneous change from an established
equilibriumtoanewequilibrium.Rarelyisthathowsystemsdevelop.
Much more prevalent is a process of change, evolution. Such a
process may be more or less smooth but with a signal embedded in
considerable noise, such a distinction is practically moot. Whether
one posits a smoothly changing signal or a series of small but
discrete, differentially sized, changes as the path between equilibria
the outcome is largely the same: further reduction in return as one’s
models are shaped to reflect a new signal dynamic. Overshoot and
elastic-likereboundadd yet morevolatilityand, hence, uncertainty.
Responding to changes in the structure of prices (and other
metricswheretheyareused)isoneofthemoredifficulttasksfacinga

TrinityTroubles 171
modeler.Unlikephysicalprocessessuchasthemotionofapendulum
subject to friction and wear, or chemical processes where impurities
affect conversion properties, and so forth, there is no underlying
theory to guide one’s model building for distortions in the relative
pricing of equities and the impact on reversion mechanics. It is
not a mechanical process at all. It only appears ‘‘mechanical’’ in
‘‘normal’’ times when disturbances are infrequent and have limited
duration impact such that a statistically regular process is observed,
exploited,andreturnstreamsarepleasingtoinvestors.Bettermodels
areinherentlyadaptivesothatachangein,forexample,thevolatility
of a stock price, if persistent, will automatically be identified and
themodelappropriatelyrecalibrated.Akeyrequirementforeffective
operationof adaptivemodelsisthepersistenceofanewstate. When
uncertainty is reflected through a succession of changes (in, say,
volatility) first in one direction then in another, an adaptive model
can fail ignominiouslyas it flails hopelesslyagainst waves of varying
magnitude and direction. In such circumstances, rigidity is a better
bet. A modeler, observing markets, the induced adaptations in his
models, and the practical results of trading, ought to develop a
sense of when rigidity is a better vessel than continual adaptation.
A difficulty here is in choosing a model calibration at which ‘‘to
be rigid’’ and when to apply or remove rigidity restrictions. Left
to the informed judgment of the modeler alone, this is an art.
Some modelers are extraordinarily talented in this respect. Most are
hopeless. The temptation to tinker when things are going poorly is,
for many, irresistible, especially for those who do not have a firm
understanding of the process being exploited by the model or how
themodel’s performanceis affected by violationsof assumptions.
With a keen appreciation of the high probability of failure from
tinkering, and a realization of the nature of the difficulties besetting
a model (whether one is able to construct a coherent explanation
of why investors are behaving in ways that cause the aberrant
pricepatterns),agoodmodelerlookstobuildautomaticmonitoring
systemsandtodesignrobustfeedforwardandfeedbackmechanisms
to improvemodels.
Starting with an understanding of the signal that a model
is exploiting, a monitor scheme is constructed to repeatedly ask
the questions, ‘‘Is the data violating model assumptions?’’ ‘‘Which

172 STATISTICALARBITRAGE
assumptions are not being met?’’ One criterion, episodically infor-
mative and efficacious, is the set of conditions in which a model is
known to perform poorly: When a model is observed to be adapt-
ing frequently, back and forth or repeatedly in one direction or
cumulativelyby too much,a modeler’sinterventionis desirable.
Feedback mechanisms form the bread and butter of an adaptive
model.Ifstockpricevolatilityisobservedtohaveincreasedbyasuf-
ficientmargin,recalibratethemodel.Repeatedfeedbackadjustments
outside of the range (frequency, magnitude, cumulative impact) in
which the model is known to perform adequately are a warning
sign for the monitoring process. Feed forward mechanisms are not
typically available to managers: We cannot change environmental
conditionstocoerceadesiredchangeinpatternsofstockpricedevel-
opment.Largerfundsarereportedtoengageinactivitiesofthissort,
using,amongotherschemes,fakeorphantomtrades—realtradesto
revealtoothermarketparticipantsthemanager’ssupposedlydesired
moves, buy IBM for example; then wait for those others to follow
the lead, buying IBM and pushing up the price; then the fund sells
its holding—its original intention—at prices more favorable than
before the faking operation. Managers do not admit to such activi-
ties.Technologicaldevelopmentsmaybeprovidingmoreopportunity
forsecret tactical trading: See Chapters 10and 11.
We entered this discussion of monitoring for and adaptation to
structural change by considering the impact of relative inactivity by
institutionalmoneymanagers. Suchinactivity, orlackofenthusiasm
generally,inanenvironmentexclusiveofsourcesoffear,reducesthe
(reversion) opportunity set in a second way. Returning again to the
archetype in Figure 9.2, a lack of energy in a signal translates into
a smaller amplitude (peak to trough range). In terms of a spread
between prices of similar stocks, the action of prices moving apart
either because of nonspecific, local drift or in reaction to investors
pursuing a particular thesis, movements are muted in magnitude as
excitement is constrained by the prevailing environmental condition
of wariness (and in some cases lethargy) borne of a belief that as
things (market themes, prices, activity) are generally not changing
rapidly, there is no sense of likely opportunity loss to be incurred
from takingone’stime.
Asinstitutionalmoneymanagerssawreturnsdiminish(ordisap-
pear, or worse, for three years) many altered their trading tactics as

TrinityTroubles 173
part ofan attempttoreducecosts.Wheretraditionally(large) trades
weresimplyhandedovertoablocktradingdeskforexecution,man-
agersbeganworkingtradesdirectly,reducing(itisclaimed)brokerage
chargesandslippagecostsquitedramatically.Itissuggestedthatthis
change (a) contradicts the hypothesis that institutional money man-
agers were less active over 2002–2004, and (b) contributed to the
lack of statistical arbitrage performance.
We do not have figures from which to draw evidence to confirm
or deny (1) and in any case the episode is over, so we will leave it.
Regarding(2),theevidenceistothecontrary.Ifmanagersresponsible
for substantial volumes of trading have changed trading tactics to
become more efficient or to be more proactive in reducing market
impact or to reduce slippage of their trading, what would one
expecttoseeinstatisticalarbitragefocusedonstockslargelyheldby
institutions?
To the extent that block trading activity is a generator of inter-
stock dispersion (creating openings for reversion bets), a shift away
from block trades to more intensively managed, smaller trades with
greater control of slippage would reduce the reversion opportunity
set. We would see a diminution in the average richness of rever-
sion signals: A manager moving capital into, say, drug stocks would
cause, for example, the Pfizer-Glaxo spread to move by a smaller
amount than under the less demanding block trade approach. With
a smaller initial dislocation, the amount of reversion is reduced. It
is also possible that the number of economically interesting rever-
sion opportunities would be reduced, though with other sources of
market price movement present it is not obvious that this would
be a significant effect. By itself the reduction of average reversion
per bet would reduce strategy return. However, other effects of the
trade tactic change make that conclusionpremature. With managers
more directly active, it is likely that their own trading decisions that
act to enforce reversion would increase the pace at which reversion
occurs. Faster reversion works to increase return (assuming that
there are enough reversion opportunities to fully employ capital).
While it is possible to argue that managers will act in the manner
describedtoreduceaveragedispersion,hencepotentialreversion,yet
not act as robustly to correct a mispricing when seeing one, it is
unreasonable—you cannot have it both ways.

174 STATISTICALARBITRAGE
Is there any evidence to support the outcome that greater micro
trade management by institutional money managers implies? It is
abundantly evident that the pace of reversion slowed, not accel-
erated, during 2002–2004. The evidence on richness of reversion
opportunities is more equivocal. There have certainly been periods
whereinterstockvolatilityhasbeenatarecordlowlevel—Marchof
2003standsoutasaperiodwhenmoststocksmovedincloseunison.
But here the diminished volatility was the result of global security
concerns; it had nothingat all to dowith moneymanagers watching
thedollarsand cents.
9.8 TRUTH IN FICTION
The accusations flung at statistical arbitrage as reasons for its poor
showing each include a truth. Each of the causes posited have had a
negativeimpactonthesizeofreturnthatstatisticalarbitragemodels
are able to generate. But in sum these slivers of return amount to no
morethan30percentofthereturn‘‘normally’’(thatis,before2000)
generated. We are impelled1 to search for a wider rationale for the
performance collapse in statistical arbitrage. Hints are apparent in
the previous section on temporal dynamics. Now we can be more
explicit.
9.9 A LITANY OF BAD BEHAVIOR
Table9.1 listsa seriesof events spanningthetwo years 2002–2003,
each of which had a significant impact on business practices and
financial market activities greatly in excess of ‘‘normal’’ change.
Most events were negative, in that shock, disgust, and not a little
horrorcharacterized the reactionsof many.
The first few months of 2002 subjected people to an unprece-
dented (?) series of appalling revelations about the activities of
businessleadersandopinion-leadingWallStreetpersonalities.These
1StephenJ.Gould,2002,TheStructureofEvolutionaryTheory,providedthephrase
‘‘impelledtoprovide a wider rationalefor’’ shamelessly borrowed formy purpose
here.

TrinityTroubles 175
TABLE 9.1 Calendarofevents
Date Event
December2001 Enron
January2002 Accountingscandals,CEO/CFOmalfeasance
WallStreetresearch:lies,damnedlies,andmillionaire
analysts
August2002 Corporateaccountsign-off
October2002 Mutualfundretailinvestorpanic
November2002 SARS
March2003 Iraqwar
Dividendtaxlawrevision
NYSE/Grassocompensationscandal
October2003 Mutualfundmarkettimingscandal
December2003 Statisticalarbitrageinvestorflight
events delivered emotional punch after punch to a populace still in
a deep sense of shock following the terrorist attacks on the United
States on September 11, 2001. Unsurprisingly, the financial market
paralleltotheshiftsinmacroeconomicactivitywasstructuralchange
intherelationshipofstockpricesonahugescaleandwiththeeffects
of one change merging into the next. No rest. No respite. Conti-
nuousturmoil.
As 2002 was drawing to a close, the SARS (severe acute respira-
tory syndrome) scare dealt another blow to international air travel
withimpactoninternationaltourism.Inlate2004,theWorldHealth
Organization attempted to raise consciousness about Asian bird flu,
forecasting that the serious outbreak in Asia threatened to become a
worldwideepidemicthat could kill50 millionpeople.2
As of now there is no sense of panic, even urgency on the part
of political leaders or populations. Little heed at all seems to have
beentaken.Thatreactionisastonishinglydifferenttothereactionto
SARSjusttwoyearsearlier.Canitbethatpeoplehavebecomebored
with scare stories?
Along with SARS the world watched the inexorable buildup of
U.S. military forces in the Gulf of Arabia. Would the United States
2January 13, 2007: Thankfully no epidemic has occurred, but concern remains as
deathsoffarmersinChinaandelsewhereinAsiacontinuetobereported.

176
STATISTICALARBITRAGE
| invade    | Iraq? | The        | watching | and    | waiting | continued | through    |       | March |
| --------- | ----- | ---------- | -------- | ------ | ------- | --------- | ---------- | ----- | ----- |
| 2003 when |       | the United |          | States | did     | invade.   | During the | three | weeks |
hostilities,’’3
| of ‘‘active |          |     |     | the markets |     | ceased     | to demonstrate |     | evidence |
| ----------- | -------- | --- | --- | ----------- | --- | ---------- | -------------- | --- | -------- |
| of rational | behavior |     | on  | the part    | of  | investors. | If television  |     | showed   |
picturesofexplosionswithreportsofproblemsforAmericantroops,
| no matter | how           | local | a      | battle   | was | being described, | markets  |          | moved |
| --------- | ------------- | ----- | ------ | -------- | --- | ---------------- | -------- | -------- | ----- |
| down.     | If television |       | showed | pictures |     | of American      | military | hardware |       |
onthemoveorcruisemissilesrainingdownonsand,marketsmoved
up.Somuchforthesophisticationofthemostsophisticatedinvestors
| in the | world | in the | most | sophisticated |     | markets | in the | world. | If this |
| ------ | ----- | ------ | ---- | ------------- | --- | ------- | ------ | ------ | ------- |
werenotreal,withrealimplicationsforlivelihoods,itwouldbetruly
laughable.
Inthelastquarterof2003,evidenceofmaturinginvestorresponse
| to yet    | more       | bad news | was      | readily      |        | visible in     | the reactions   |              | to (then) |
| --------- | ---------- | -------- | -------- | ------------ | ------ | -------------- | --------------- | ------------ | --------- |
| New York  | attorney   |          | general  | Spitzer’s    |        | revelations    | of illegalities |              | on the    |
| part of   | mutual     | funds.   | No       | wholesale    |        | rout           | of the industry |              | ensued.   |
| Investors | calmly     |          | withdrew | from         | the    | shamed         | funds           | and promptly |           |
| handed    | over       | monies   | to       | competitors. |        | The surprise   | value           | of           | further   |
| bad faith | activities |          | on       | Wall         | Street | (a convenient, | if              | amorphously  |           |
uninformativelabel)wasmetwithrationalanalysisandnotshocked,
unthinkingpanic.Doubtlessarisingmarketforthefirsttimeinthree
| years had    | a powerfulaphrodisiaceffect. |           |             |         |           |             |                     |             |        |
| ------------ | ---------------------------- | --------- | ----------- | ------- | --------- | ----------- | ------------------- | ----------- | ------ |
| The          | sequence                     |           | of shocking |         | events,   | each        | starkly disgraceful |             | indi-  |
| vidually,    | is an                        | appalling |             | litany. | Added     | to globally | disruptive          |             | events |
| (war, health |                              | scare)    | there       | were    | two years | of          | uninterrupted       | instability |        |
in the financialmarkets.
| How | does | market | disruption |     | affect | the | process of | relative | stock |
| --- | ---- | ------ | ---------- | --- | ------ | --- | ---------- | -------- | ----- |
pricereversion?Figure9.5extendsthepreviousviewofanarchetype
spread(Figure9.2)tocoveraperiodofdisruption.Aspreadispushed
| unusually        | far | out | of its   | normal   | range | of variation | by    | undisciplined |       |
| ---------------- | --- | --- | -------- | -------- | ----- | ------------ | ----- | ------------- | ----- |
| investorbehavior |     |     | butafter | thecause |       | ofthepanicis | over, | oras          | panic |
reactiondissipatesanddisciplineisreestablished,thespreadresumes
| its normal | pattern |     | of variation. |     |     |     |     |     |     |
| ---------- | ------- | --- | ------------- | --- | --- | --- | --- | --- | --- |
3TheoccupationofIraqhasbeenanunendingrunofactivehostilities.Thehostility
ofinsurgentsremainsvirile;inearly2007PresidentBushdirected20,000additional
U.S.troopstobesenttoBaghdad.However,eventsinIraqhavelongceasedtohave
noticeableimpactonfinancialmarkets.

TrinityTroubles 177
10
8
6
losing rebound
4
2 t 1 t 2
0 50 100 150 200
FIGURE 9.5 Sinewavewithtemporaryperturbation
The model has at time t a different assessment of the normal
2
behavior of the spread than it does at time t (just as it potentially
1
hasadifferentviewatalltimesbutconsiderationofjustafewpoints
is sufficient for a clear illustration of the temporal development, the
evolution of views encapsulated in an adaptive model). Depending
on the model’s look back, the rate of information (data history)
discounting, the projection of future pattern—focus on the mean
for this analysis—will vary. A shorter look back (faster discount)
will project a higher mean (also greater amplitudeand longerphase)
and will signal exit too early, which will lock in a loss on the
trade. A longer look back (slower discount) will generate standard
profit (in this example) but over an extended duration, hence, much
lower return. Nowhere will gains be accelerated. Hence, return
unambiguouslymust decline(inthe absenceof intervention).
In the next section we offer a particular view of the unfolding
psychology of market participants over 2003. This is intended as a
serious analysis (though necessarily of limited scope) of the nature
andcausesofobservedchangesinmarketparticipantsandtheresult-
ingeffectsonsecuritypricedevelopment.Itbuildsonthedescription

178 STATISTICALARBITRAGE
ofeventsjustgiven,thegoalbeingtorevealtheextentofthechanges
in the U.S. macro economy, polity, and financial markets. Section
9.11describeshowsuchtectonicshiftsinenvironmentaffectquanti-
tativemodelsandwhatmodelerscandotomanagetheshifts.Section
9.8 foreshadows that discussion. There are no simple one-liners in
these descriptions and analyses. The world is not so obliging. Statis-
tical arbitrage did not generate a return in three years for multiple
reasons, differentially across strategies, differentially across time.
What happened in 2005 is not what happened two years previ-
ously. Attempting to explain the failure by citing one or two easily
spoken reasons, as if trying to pin a tail on a donkey, is unhelp-
ful. It simplifies the complexity beyond the point of understanding,
leadingtomisunderstanding.Iteliminatesanyabilitytosensiblypos-
tulate what is realistically possible for statistical arbitrage. With the
return of statistical arbitrage performance since 2006, the criticisms
voiced during 2003–2005 have magically been forgotten. Chapter
11 tells how the statistical arbitrage story is about to write a new,
positivechapter.
9.10 A PERSPECTIVE ON 2003
Trading intensity in the first quarter was low because of investor
hesitancy in taking positions as the United States prepared to go,
then went, to war. Following the three weeks of active hostilities,
investoractivityinthemarketswasattimestentative,skittish,manic.
As early as last quarter 2003, it was possible to see, swamped in
short-termvariability,atrendofsteadyimprovementintenor:Uncer-
tainty had decreased, conviction and the willingness to act thereon
had increased; companies were again investing strategically, imple-
menting long-term plans rather than substitutingshort-term holding
actions; individuals were increasingly leaning toward optimism on
prospects for employment opportunities and stability. Crucially, the
pervasive sense of fear, not at all well defined or articulated but
palpablefrom late 2002throughMay 2003,was gone.
The summer recess both interrupted and contributed to the
post-war recovery. Distance in time provides perspective; a change
inroutine,vacation,encouragesreflection.Thedoldrumsofsummer
(interstock) volatility were lower than had been seen before, partly

TrinityTroubles 179
because of the low pre-summer level and partly because of the clear
need for people to take a break. Two critical changes in perception
occurred.
The tragic, daily loss of servicepeople’s lives in Iraq impinged
on the general populace’s consciousness with the interest, intensity,
and indifference of the latest rush hour traffic accident: It is there,
it is unfortunate, but it is reality. The U.S. economy was discussed
in encouraging terms of growth and stable employment. Deflation
had resumed its traditional role as a textbook scenario. The number
of people who understand or care about government deficits and
the implications—until they occur—is tiny. Such broad changes in
perceptionhave an indelibleimprint on financialmarkets.
Transition from war edginess and economic gloom to war
weariness (dismissal) and the excitement of economic potential,
opportunity:Marketpricebehaviorinthelatterpartof2003reflected
investor fervor, alternately hesitant, rushed, somewhat erratic; gen-
erally untidy,undisciplined.
9.11 REALITIES OF STRUCTURAL CHANGE
The complexity of the process of change is revealed in the mixed
signals of market condition tracking and prediction models. From
March2003,earlyinstatisticalarbitrage’sperformancedesert,these
modelssimultaneouslyindicatedbothashiftfromnegativetopositive
bias and continuednegative bias. Uniquein more than a decade, the
schizophrenic indicators revealed a market structure in which that
structure is mixed up, unsettled, and in transition. The evolution
of the indicators, if one were to imbue them with some life force,
engenders the impression of a relentless striving for equilibrium,
increasinglyconfidenteach month.
Adapting to the changes in market price behavior that reflect
the enormous changes in perceptions, concerns, assessments, and
ultimately, actions of market participants is extraordinarilydifficult.
For models designed to exploit an identified pattern of behavior in
prices, the task can be impossible (if the exploited pattern vanishes)
and often models simply ‘‘do not work’’ during market structural
change. Evolution and adaptation are possible in better models but
large, abrupt shifts and repeated shifts are immensely difficult to
manage well.

180 STATISTICALARBITRAGE
Statistical arbitrage models have no special protection from the
impact of market upheaval. The fact that performance diminished
to little more than money market returns in conditions, known with
20–20 hindsight to be quite unfavorable for reversion exploitation
(lack of consistent behavior untrammeled by decisions borne of
panic),isatestamenttothecarefulconstructionoftradedportfolios,
strict adherence to model application where signals are detected,
and concerted focus on risk analysis. Critical to risk control is an
understanding of the process exploited by the model: in short, why
the model works. Reversion in relative prices of similar stocks did
not evaporate—models systematically identified opportunities and
trading has routinely exploited those opportunities. Reversion did
not evaporate. The environment in which reversion occurred was
changed, transforminghowreversion is identified.
Changesofstatearetypicallyunrewardingperiods,evennegative,
for statistical arbitrage. Models, good models, are crafted carefully
to adapt to changes in important characteristics of market price
behavior pertinent to model predictive performance. But no matter
how hard model builders try, diligence cannot compete with good
fortunewhenstructuralchangesoccur.Itbehoovesustoadmitthatif
wecanavoidlossesduringstructuralchange,whilerecraftingmodels
to encapsulatethe newstructures, then we have donewell.
9.12 RECAP
At this point we have concluded that a third of the historical
performance of statistical arbitrage may have been eliminated by
market developments during 2000–2002, changes that will not be
reversed. The loss of the bulk of the historical return in 2002–2003
wastheresultofaseriesofmassivedisruptionstotheU.S.economy,
theramificationsforstatisticalarbitragehaving(mostlikely)beenfelt
intheirentiretybysometime,probablyearly,in2004.Thefrequency
of disruptions has been greatly reduced; though there continue to
be market effects as the structural changes play out, the impact
on statistical arbitrage is no longer significant. Stock-specific events
continue to occur, two examples in 2004 being the withdrawal of
thedrugVioxxbyMerckandtheinvestigationofMarsh McLennan
by (then) New York attorney general Elliot Spitzer. Extraordinarily

181
TrinityTroubles
| low volatility  |              | coupled | with           | high      | correlations | is a           | major  | limitation |
| --------------- | ------------ | ------- | -------------- | --------- | ------------ | -------------- | ------ | ---------- |
| on what         | can          | be made | from           | reversion | plays.       | Correlations   |        | have now   |
| decreased,      | increasing   |         | the short-term |           | reversion    | opportunities. |        | Work-      |
| ing to keep     | correlations |         | higher         | than      | historical   | norms          | is the | growing    |
| use of exchange |              | traded  | funds.         | As        | investors    | shift to       | ETFs,  | ‘‘everyone |
becomesadefactoindexer.’’Volatilitywillcontinuetobeconstrained
| by the      | widespread      | use         | of                                     | sophisticated |       | trading tools | (Chapter | 10).  |
| ----------- | --------------- | ----------- | -------------------------------------- | ------------- | ----- | ------------- | -------- | ----- |
| Butthatvery |                 | same causal | factoriscontributingtotherenaissanceof |               |       |               |          |       |
| statistical | arbitrage       | by          | creating                               | new           | kinds | of systematic | stock    | price |
| patterns,   | as elucidatedin |             | Chapter                                |               | 11.   |               |          |       |

10
CHAPTER
Arise Black Boxes
Felixqui potuitrerun cognoscerecausas.
Happy ishe who can knowthecause of things.
—Virgil
10.1 INTRODUCTION
Having invented the pairs trading business two decades ago,
Morgan Stanley was at the forefront of the creation of a new
business in the early 2000s; a less risky, more sustainable business,
which,inawonderfulexampleofcommercialparricide,hassystemat-
ically destroyed opportunitiesfor old-linepairs trading. Algorithmic
tradingwasborn.Hugeorderflowfrominstitutionsandhedgefunds,
much of which is electronicallymatched in house,provided multiple
opportunities for bounty beyond the expected brokerage fees. Com-
bining the insight and knowledge learned from proprietary trading
(beginning with the classic pairs trading business) with analysis of
a warehouse of order flow data, Morgan Stanley and other brokers
built trading tools that incorporate models for forecasting market
impact as a function of order size and time of day, moderated by
specificdaily tradingvolumestock bystock.
Recognizing that there was an enormouslylucrative opportunity
hanging on simple to use, automatic trading technology that did not
systematically incur slippage, brokers elected to offer the tools to
clients.Itwasamasterfullytimeddecision.Comingasnewstatistical
arbitrageurs were appearing with abandon, vendors were able to
seduce those whom their tools would eventually help destroy, along
with existing clients thirsting for any new edge that had the promise
183

184 STATISTICALARBITRAGE
of lower transaction costs or marginal improvements in execution
price.Thegeniusofthebusinesswascompoundedastheinstitutional
and statistical arbitrageurs’ order flow provided an ongoing feast of
data for the data miners whose voracious appetite for such cannot
be sated.
Patterns of transaction volume by stock, by day of the week, by
time of day, and by current day’s trading volume were constructed
from the mined data. The mere ability to predict with measurable
efficacy how much would be given up from current price to buy or
sell a specific number of shares in a fixed period was a stunning
development to traders. Hedge funds had for years made their own
attempts; using their much less rich data than broker archives it is
unlikelytheirachievementmatchedthebrokers’success.Regardless,
an edge was eliminated.
Fitting logistic-type models to order flow and fill data quickly
produced the first generation of models, allowing traders to obtain
quantitativeanswers to frequentlyfaced, urgent questions:
■ How much will I have to pay to buy x thousand shares of XYZ
in the next half hour?
■ How much will I have to pay if I wait the remainder of the
tradingday?
■ How much can I sell of XYZ in one hour keeping the impact to
k cents?
An unadvertised beauty of these tools is the self-propagating
natureof theopportunityset. Astradersswitchedtothetechnology,
a new set of order flow information was presented to and collected
by vendors. Now it was possible to examine the trading of both the
impatient ‘‘pay up and get it done’’ and the relaxed ‘‘wait and see’’
players. Models of client profiles, built automatically from the client
orderflow,tradingtoolconfiguration,andfill/cancel–correctrecords
practically generate themselves. With the ability to gauge how much
a client would be willing to pay for a fill, and estimates of how long
it would take to get the trade at much lower market impact, the
manypossibilitiesfairlyscreamed themselvestoresearchers, echoing
and amplifying the old-line pairs trade screams heard by a previous
generation two decades earlier.

AriseBlackBoxes 185
All of this opportunityoffered itself for reaping without require-
ment of capital commitment. The risk of proprietary trading was
eliminated and the‘‘new’’ businessbecame infinitelyscalable.
Morgan Stanley has competitors, of course. Algorithmic trading
tools have been developed and marketed by Goldman Sachs, Credit
Suisse First Boston,LehmanBrothers, Bank of America, and others.
10.2 MODELING EXPECTED TRANSACTION VOLUME
AND MARKET IMPACT
The place to begin is the data mine. What data is available and
whichofitispertinenttoansweringthe‘‘Howmuch...?’’questions.
Suppose that for stock XYZ there is a history of daily transaction
volume data by individual trade, for over ten years. That is 2,500
days of daily transaction material. The first thing to do is examine
the cumulative trade volume by day: Every stock has a distinctive
character to its pattern of trading over the day, a footprint if you
like. Using a one-shoe-fits-all approach, forecasting an elephant’s
footprintusingagenericmammalfootprintmayworkbutwillsuffer
from needlessly large inaccuracies (noise or error variance). Worse
would be to use an asp’s footprint (try to describe it). You can see
theproblem.
Theproblemiseasilyaddressedbyapplyingamodicumofspeci-
ficity in the data analysis and model building. Computers don’t care
how many model variants they process. You should care, however;
overspecificitywhereitisunnecessaryalsoleadstoover-largepredic-
tionvariancebecauseafinitedataresourcedoesnotyieldaninfinitely
divisible reservoir of information. The more the data is carved into
differentanimals,thelessinformationthereisoneach.Iftwoormore
animalsareessentiallyidentical(forthepurposeunderinvestigation)
thedataisbestpooled.Moreover,themoremodelsonetestsondata,
the greater the likelihood of finding a spuriously good fit. These are
well known,though oftenignored, detailsof good appliedstatistical
analysis.
Begin looking at the data with a view to identifying a trading
day pattern in transaction volume. How to characterize it? While
it is unlikely that the daily pattern ten years ago is close to the
dailypatterntoday,itwouldbeinadvisabletoassumeso.Remember

186 STATISTICALARBITRAGE
thatreversion patternsexploitedbytheoriginalpairstradepersisted
witheconomicallyexploitablefrequencyandmagnitudeforadecade
and a half before technological and market developments caused a
dramaticchange.Examinesomedailycumulativetransactionvolume
charts from ten years ago, some from five years ago some from this
year.Youwillnoticeasimilarformtothegraph(curve)butobvious
differences—faster cumulation early in the day and again late in the
day comparing recent patterns to earlier patterns. Better not simply
aggregate all the dataand estimatean average curve then.
Look more closely at daily patterns for the last three months.
That is 60 charts. Examine a three-month set from ten years ago.
You notice quite a lot of overlap in the basic shapes. But look at the
scales: The stock trades at much higher volumes now than it did a
decade ago. Hmmm. Rescale the graphs to show cumulative percent
of daily total volume. Now all graphs are on the same 0–100 scale.
Aha!Thereismuchlessvariabilityinthepatternsofthelastquarter.
So, whethera given day is relatively high orrelatively lowvolume, a
similar pattern forthetradingover theday is revealed.
Howdoweusethisinsight?Onegoalistorepresentthecurve(of
cumulativepercentagetradevolumeinaday)inawayinwhichitwill
readilyyieldtheproportionofaday’stradevolumeinthemarketata
specifictime. Inotherwords,toprovideaready answer toquestions
such as, Howmuchof thevolumeistransacted by2 p.m.?Thereare
manymathematicalfunctionsthathavethegenericSshaperequired:
Cumulative density functions of probability distributions provide a
natural set since distributionsare precisely what are being examined
here. A convenient form for statistical model building (which we
have not yet considered)is thelogisticfunction.
Pick a function. Fit it to the data. You can now readily make
sensibly quantified stock-specific responses to the question: How
much of the day’svolumeis transacted by 2 p.m.? On average ...
Nowtodayhappenstobeareasonablyheavytradingdayforthe
stock, with 4 million shares traded by 11:30 a.m. How many shares
are expected to trade by 2 p.m.? From the estimated pattern, fully
30 percent of the day’s volumeis typically transacted by11:30a.m.,
and 40 percent by 2 p.m. Easily you compute 1.3 million shares
are expected to trade over the next 90 minutes. You want to trade
100,000shares.Shouldnothavetopaymuchtoachievethat.Right?

AriseBlackBoxes 187
Theforegoinganalysisconsideredonlytransactionvolume;price
information in the record has not yet been examined. Let’s redress
that directly. In the set of 60 days of trading data for XYZ, there
aremanyindividualbuyandselltransactionsforordersizesassmall
as 100 shares to as large as 100,000 shares. The fill information for
all orders is also recorded. Plotting order size against the change in
price from the order price (or market price at time of order) and the
averagefillpriceshowsadefiniterelationship(andalotofvariation).
Once again, some of the variation magically disappears when each
day is scaled according to that day’s overall volume in the stock.
Orders, up to a threshold labeled ‘‘visibility threshold,’’ have less
impact on large-volumedays.
Fitting a mathematical curve or statistical model to the order
size–market impact data yields a tool for answering the question:
How much will I have to pay to buy 10,000 shares of XYZ? Note
that buy and sell responses may be different and may be dependent
onwhetherthestockismovingupordownthatday.Breakingdown
the raw (60-day) data set and analyzing up days and down days
separatelywillilluminatethatissue.Moreformally,onecoulddefine
anencompassingstatisticalmodelincludinganindicatorvariablefor
upor downday andtest thesignificanceoftheestimated coefficient.
Given the dubious degree to which one could reasonably determine
independenceand otherconditionsnecessary for thevalidityof such
statistical tests (without a considerable amount of work) one will
be better off building prediction models for the combined data and
for the up/down days separately and comparing predictions. Are
the prediction differences of practical significance? What are the
differences?
One drawback of fitting separate models to the distinct data
categories is that interaction effects (between volume, up/down day,
buy/sell, etc.) cannot be estimated. If one is looking for understand-
ing, this is a serious omission as interactions reveal subtleties of
relationships often not even dimly suggested by one-factor-at-a-time
analysis.Ifoneislookingforadecentprediction,theomissionisintel-
lectually serious (if there are interactions) but practically (depending
on thenatureof the interactions)of less import.
Timeofdayisalsosignificantinmarketimpactestimation—recall
the analysis of the cumulative trading volume pattern over the day.
Filling an order during the ‘‘slow’’ or more thinly traded part of the

188 STATISTICALARBITRAGE
dayrequireseithermorepatienceforagiven slippagelimitora will-
ingness to increase that limit. Time of day was not addressed in the
order size–market impact analysis outlined previously. Obviously it
can be, and the obvious approach is to slice the data into buckets
for the slow and not slow parts of the day (or simply do it by, say,
half-hour segments) and estimate individual models for each. While
the statistical modeling and analysis can be made more sophisti-
cated,thesimplebucketingprocedurepositedhereservestoexemplify
the opportunity and the approach. (Examples of fruitful sophistica-
tion include formally modeling parameters across time slices with
a smooth function, and employing classification procedures such as
regression treesto identifynatural groupings.)
10.3 DYNAMIC UPDATING
Examining the basic patterns of daily trading volume from ten years
ago and more recently has prompted the realization that patterns
have changed. Immediately one is confronted by the problem of
how to manage the change in predictive models estimated from
the data. The first action was to use only recent data to build the
model to use now. We’ll assume recent time at 60 days. Now one
is confronted by the question, When should the models be revised?
We are once again faced with the questions about types of change,
rates of evolution, and methods of dynamic updating that were
discussed with respect to the reversion models in Chapter 2. The
basic issues here are no different. One might reasonably elect to use
a rolling 60-day window, reestimating modeled relationships each
day. One might also routinely compare the latest daily pattern with
the distribution of patterns seen (a) recently or (b) further distant
in time to make a judgment about whether today is unusual. If
it is, perhaps it would be wise to apply a ‘‘conservatism filter’’ to
the forecasts? A measure of the rate of change could be devised
(there are standard ways of comparing probability distributions,
from summary statistics, includingmoments, to integrated measures
of information), and employed to build a general dynamic updating
scheme that is more flexible than the simple 60-day moving history
window.

AriseBlackBoxes 189
10.4 MORE BLACK BOXES
WehavedeliberatelysingledoutMorganStanleyatthebeginningof
the chapter because of the link to the genesis of our major theme:
statistical arbitrage. But Morgan Stanley is not the only firm to
have analyzed transaction data and offered tools to the marketplace
encapsulating trading intelligence discovered therefrom. Goldman
Sachs’ operations on the floor of the NYSE—the Spear, Leeds &
Kellogspecialistsboughtin2000—representagoldminepotentially
evenmorevaluablethanMorganStanley’sdatabase.BankofAmerica
bought the technology of hedge fund Vector in 2002: ‘‘...computer
algorithms will factor in a particular stock’s trading characteristics
and BofA’s own position in it then generate buy and sell quotes’’
(InstitutionalInvestor,June2004;italicsaddedforemphasis).Credit
SuisseFirstBoston(CSFB)hiredaformeremployeeoftherenowned
andtechnologicallyadvancedhedgefundD.E.Shaw,andbuiltatool
that ‘‘processes fully 40% of its [CSFB’s] order flow’’ (Institutional
Investor,June2004);LehmanBrothersandmorethanadozenothers
are also in thebusiness.
In addition to the developments just listed, at least one new
brokerage, Miletus, has been spun out of a billion dollar hedge
fund to monetize the value in the trading algorithms developed for
the hedge fund’s own trading. In another technology driven devel-
opment, beginning with Goldman Sachs in late 2006, at least two
offeringsofgeneralhedgefundreplicationbyalgorithmicmeanshave
been brought to market. As these instruments gain popularity there
are likely to be new systematic pattern generating forces added to
themarket.
10.5 MARKET DEFLATION
Figure10.1depictsthemarketforbuyingandsellingstocks,ageneric
market where buyers and sellers come together to agree on a price
for mutually acceptable exchange of ownership. There are many
buyers and many sellers. Lots of individual excitors. Many points of
agreement. Substantial volatility.
Figure 10.2 depicts the arriving market for buying and selling
stocks. The many individual buyers and sellers come together by

190
STATISTICALARBITRAGE
|     |     | Buyers |     |     | Sellers |     |     |
| --- | --- | ------ | --- | --- | ------- | --- | --- |
MARKET
high volatility
|     |     | FIGURE 10.1 | Thewaythemarketwas |     |     |     |     |
| --- | --- | ----------- | ------------------ | --- | --- | --- | --- |
buyers
sellers
sellers
algorithm 17
algorithm 24
| buyers | algorithm 4 |     |     |     |     |     |     |
| ------ | ----------- | --- | --- | --- | --- | --- | --- |
buyers
r   e   s   i   d   u   a   l
| sellers |     | MARKET — low volatility |     |     |     |     |     |
| ------- | --- | ----------------------- | --- | --- | --- | --- | --- |
FIGURE 10.2
Adeflatedmarketmodel
theintermediatingmanagementofahandfulofcomputeralgorithms
| which internally |       | cross a        | substantial | portion  | of              | orders | and satisfy |
| ---------------- | ----- | -------------- | ----------- | -------- | --------------- | ------ | ----------- |
| the residual     |       | by restrained, | unexcitable |          | exchange        | in     | the central |
| market.          | There | are many       | buyers and  | sellers. | Many            | points | of agree-   |
| ment. But        | less  | unmitigated    | agitation   | than     | the traditional |        | bazaar.     |
Constrainedvolatility.

11
CHAPTER
Statistical Arbitrage Rising
...to worryabout everything isunnerving. It is also
counterproductive,forit can result in continualtinkering
with a correctly operatingsystem in responseto imagined
phantomsin the data.
—Statistical Controlby Monitoringand Feedback
Adjustment,Boxand Luceno
By the end of 2004, statistical arbitrage practitioners had been
beleaguered for a year. Investors and commentators cite perfor-
mance volatility but no return set against market advance (in 2003);
adduceaccusative assertionsof irreversible declinefromvisible mar-
ket changes; and largely turn deaf ears to the necessary complexity
of thereality (see Chapters9 and 10 fora full exegesis).
Set against that siege is the present discourse and a return of
performance since 2006. Chapters 2 to 8 set out the nature and
extentoftraditionalstatisticalarbitrageopportunities,approachesto
formal modeling and systematic exploitation of those opportunities,
the nature of market dynamics that wreaks havoc on portfolios
builtandmanagedaccordingtostatisticalarbitragemodels.Chapter
9 examines one-liner condemnations of the discipline, the logic of
whichis:Thischangeeliminatesapartofstatisticalarbitragereturn;
thechangeispermanent;youropportunitysetisthereforegone.The
claimsarefoundpertinentbutinadequatetoexplaintherecord.The
far more complex reality is no less devastating but, upon deeper
reflection, cannot support condemnation. In their complexity, the
enduring elements are not wholly destructive of statistical arbitrage.
To the contrary, some of the more far-reaching market structural
191

192 STATISTICALARBITRAGE
changes, set out in Chapter 10, necessarily create conditions for
a new statistical arbitrage paradigm. That emerging paradigm, its
driving forces and consequent statistically describable and therefore
exploitable stock price patterns, is set out in this chapter. It both
concludes the present volume and sets the scene for a subsequent
historyto be written someyears hence.
A few statistical arbitrage practitioners with long and outstand-
ing performance pedigrees continued to deliver reasonable to good
returns while most have failed as described in earlier chapters.
This evidence supports the claims of (a) incomplete destruction of
traditional statistical arbitrage opportunities and (b) genesis and
development of new opportunities, though only proprietary infor-
mationcouldreveal towhat extenttheevidencesupportseach claim
individually. Evidence in the analysis of the public record of stock
price history strongly suggests that the opportunity for extracting
outsize returns from high-frequency trading—intraday—is huge.
From the discussion throughout this book, it is clear that exploiting
that opportunityrequires different models than thetraditional mean
reversion type. Some such modelsare describedlater in thischapter.
Patterns of stock price movements within the trading day show
not reversion but momentum. There are also patterns of reversion
within the day but these patterns seem to be difficult to predict
(though there are claims for success here); they occur spasmodi-
cally for broad portfolios, with precursor signals that are not easily
identified. Indeed it may be inappropriate to label the movement
as reversion; reversal may be more indicative of the dynamic. The
distinctioniscrucial.Arevertingprocessassumesanunderlyingequi-
libriumtowhichprice(orrelativeprices)tendstoreturnfollowinga
disturbanceaway fromit(thepopcornprocess).Equilibratingforces
can be identified. The trends and reversals process makes no such
underlyingassumptionofequilibrium;rather,theprocessisonethat
moves for more or less extended periods in one direction and then
in the other without a strong link from the one move to the next
(a memoryless switching process). Critical to the description and
assessmentarethedurationandmagnitudeofthedirectionalmoves:
They endure sufficiently long (think of sufficiently many time steps
where each step is visible to a person) and the move is large enough
to be exploited systematically, given necessary lags for turning point
identification.

StatisticalArbitrageRising 193
Crucial to successful modeling is an understanding of the forces
in the market driving the trend creation. Penny moves are one
important factor, having already removed price friction eliminating
historicallyinnateinitial resistance to repeated (and thereforecumu-
lativelylarge)moves.Compoundingthisistheincreasingremovalof
human specialists from the price setting process as more trades are
crossed automatically on electronic exchanges and by the brokerage
houses’ trading programs described in Chapter 10. Most significant
arethose‘‘intelligent’’tradingenginesandthesignificantproportion
of transactions preempted as VWAP or TWAP. Old-line technical
analysis may, curiously, retain some efficacy in exploiting the new
intraday trend patterns; but greatest success will inhere to those
whose modeling incorporates knowledge of the underlying motive
forcesand algorithmictrading tactics.
Farremovedfromunderlyingequilibratingforces,drivenbypeo-
ple making judgments of fair valuation of company prospects both
short- and long-term, the new paradigm is one of unemotional—
uninterested—rule-based systems continually probing other similar
entities. The process is mechanistic as in a geological process, water
finding the lowest level. Here, however, the rules are defined by
human modelers and not the laws of the physical universe, and they
are changeable. Noise is omnipresent as human traders still directly
preempt a sizable chunkof market activity and originateall transac-
tions. Notwithstanding the noise, the new forces for equilibrium are
searching not for fair relative prices but fair (mutually accepted by
participating entities) market clearing. This new paradigm may be
a reversion (!!!) to an age-old paradigm of economics: perfect com-
petition. Now, on that train of thought one might conjure ideas of
dynamic cobweb algorithms, game theoretic strategies, and perhaps
a necessary repositioningof research intobehavioral finance.
Volatility will remain consumed by the algorithms. Instead of
human-to-human interaction either face-to-face on the floor of the
NYSE or face-to-screen-to-face in electronic marts, there will be
algorithm-to-algorithm exchange. A large and growing part of the
emotion surrounding trading is removed, and with that removal
goes volatility. Yet in this focus on algorithms, we must not forget
that people still drive the system. With trades managed by algo-
rithms implemented on incredibly fast processing computers, what
might be done by algorithms designed to go beyond passive market

194 STATISTICALARBITRAGE
participationtoactivemarketdetermination?Possiblyprobingother
algorithms for weakness, for opportunities to subvert naivete, or to
mislead into false judgment. Warfare by another name. The attrac-
tionforcertain managersandthechallengeforcertain programmers
is irresistible.
Speculationof course, I think.
11.1 CATASTROPHE PROCESS
Since early 2004, spread motions have been observed to exhibit an
asymmetric process where divergence is slow and continuous but
convergence—the ‘‘reversion to the mean’’ of old—is fast(er), even
suddenbycomparison.Convergenceisnotnecessarily‘‘tothemean’’
though it is in the direction of a suitably local view of the mean.
The first two characteristics contrast with those of the popcorn
process, which exhibits a faster-paced departure from the norm and
slower return. The third characteristic, the degree of reversion to an
underlying mean, also distinguishes the two processes: In the newly
emerging process, the extent of the retrenchment move is far more
variable than was the case forthepopcornprocess.
Now we enter a definitional quagmire, so careful examination
and explicationat length isdesirable.
Contrast the classical popcorn process with the new process
using Figure 11.1. The notable features of the new process are:
a slow, smooth divergence from local equilibrium; fast reversion
toward that former equilibrium; partial reversion only (in most
cases); repeated moves in quick succession delineating a substantive
localtrendawayfromtheunderlyingequilibrium.(Thelatteris,asin
all archetypal illustrations, depicted as a constant level. In practice,
it is superimposed, on long-term trend movements—for a positive
trend, turn the page counterclockwiseby several degrees to view the
archetype.)
The critical departure in this new ‘‘catastrophe’’ model is the
appearance of local trends within the period classically depicted as
sufficientlylocaltobeconstant.Thelocaltrend(withinatrend)must
now be depicted and formally incorporated in the analysis because
it is part of the opportunity driver and is crucial to the successful
exploitation of the new reversionary moves. It cannot be ignored as
noiseon an underlying(popcorn)process.

195
StatisticalArbitrageRising
(a)
6.0
5.5
5.0
4.5
4.0
| 0   |     | 20  | 40  |     | 60  |     | 80  |     | 100 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(b)
12
|     | A   |     |     | B   | C   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
10
8
6
4
| 0           | 20                                                     |     | 40  |     | 60  | 80  |     | 100 |     |
| ----------- | ------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- |
| FIGURE 11.1 | (a)Archetypeofthepopcornprocessshowingreversiontoamean |     |     |     |     |     |     |     |     |
(b)Newarchetype:catastropheprocess
| The | combination |     | of variable | amounts |     | of ‘‘reversion’’ |     | and | multi- |
| --- | ----------- | --- | ----------- | ------- | --- | ---------------- | --- | --- | ------ |
plemovesinthesamedirectionbeforealargerdirectionalshift(singly
| or, again,      | multiple   | small  | events)           | is    | driven   | by the           | interaction |             | of algo- |
| --------------- | ---------- | ------ | ----------------- | ----- | -------- | ---------------- | ----------- | ----------- | -------- |
| rithmic trades. |            | (There | may be            | other | drivers, | but              | they        | remain      | elusive  |
| at this time.)  | Patient    |        | algorithms        | ease  | up       | when             | prices      | move        | repeat-  |
| edly, penny     | by         | penny  | by penny—moves    |       |          | that specialists |             | are keen    | on       |
| following       | the change |        | to decimalization |       | and      | which            | are         | undoubtedly |          |
programmedintosomealgorithms.Whatusedtobeacertaininertia
tomoveswhenticksizewassubstantive,aneighth,isnoweagerness
torepeatedlypenny.Pennyingwasridiculouslylucrativeatfirstwhen
humantradersstilldominatedorderflow.Thepatienceanddiscipline
| ofalgorithmshavingreplaceddirecttrader |                     |     |              |     |          | involvementhavealtered |      |     |       |
| -------------------------------------- | ------------------- | --- | ------------ | --- | -------- | ---------------------- | ---- | --- | ----- |
| the dynamics                           | of                  | the | interaction. | The | results, | which                  | seem | now | to be |
| clear, are                             | thecatastrophemoves |     |              | we  | have     | described.             |      |     |       |
Noticetheimplicationsforthepopcornprocessmodelappliedto
| thecatastropheprocessrelative |     |     |     | priceevolution:zero |     |     | return. |     |     |
| ----------------------------- | --- | --- | --- | ------------------- | --- | --- | ------- | --- | --- |
Anaturalquestiontoaskis,Whathappensoveralongertimescale
| than that | encompassed |     | in A–C | in  | Figure | 11.1? | The description |     | just |
| --------- | ----------- | --- | ------ | --- | ------ | ----- | --------------- | --- | ---- |

196 STATISTICALARBITRAGE
6.2
6.0
5.8
5.6
5.4
5.2
5.0
5 10 15
FIGURE 11.2 Extendedpopcornmovewithcatastrophemovesindetail
given, serial moves in one direction punctuated by partial retrench-
ment, then essentially the same in the opposite direction, as shown
in Figure 11.2, and variant in Figure 11.3, sounds like little more
thana sharperfocusonthepopcornprocess,as if onesimplyturned
up the magnification to see more of the uninteresting, picture cloud-
ing, uneconomic detail. The proper interpretation is to extend the
time-scale so that the micro moves on the popcorn process become
astimesignificantastheoriginalpopcornmoveitself.Thus,thepop-
corn move may require as many as six (or even more) catastrophe
moves to complete—a long time in a dynamic market. Popcorn’s
return even under these ideal conditions is reduced many fold. But
the true picture, returning to Figure 11.1, is seriously worse. Over
the long time period just suggested, the local mean shifts more than
can be assumed away, invalidating the basic popcorn process. At
best, the outcomes become distributed across a range in which the
uninteresting values detract greatly from the interesting, as shown
in Figure 11.4, converting an exploitable structure to a textbook
or journal curiosity. Over the extended duration, the bet becomes
a fundamentally dominated play; for the statistical popcorn process

6.2
6.0
5.8
5.6
5.4
5.2
5.0
5 10 15
FIGURE 11.3 Variantonextendedpopcornmove
6.0
distribution of outcomes very
variable because of extended
5.8 elapsed time
5.6
5.4
5.2
5 10 15 20 25
FIGURE 11.4 Extendedpopcornmovehasvariableresult
197

198 STATISTICALARBITRAGE
not predicated on fundamental analysis, forecast power evaporates
and the return alongwith it.
11.2 CATASTROPHIC FORECASTS
The magnitude of a catastrophe reversion is not accurately forecast
in comparison to forecasts of the popcorn process. But the great
variation in results from both systems, popcorn applied to popcorn
data, catastrophe to catastrophe data—and where is the cutoff?
Say pre-2002 for popcorn, post–mid-2004 for catastrophe, with
the intermediate 18 months dominated by disruptive influences of
change—means that for a large collection of bets, the statistical
measureR2issimilar.Thesignificanceofthatobservationfortrading
is an overall expectation of similar rates of return if the number of
bets in a reasonable period is similar and the overall variation in
the two sets of bets is also similar. Reality, of course, is not so
obligingly straightforward. As the catastrophe process has come
to characterize spread motions more accurately than the popcorn
process, general levels of spread volatility have been decreasing (see
Chapter9).Before2003,whenthepopcornprocessprovidedavalid
representation of spread motions, volatility was nearly double that
prevailing in late 2004, when the catastrophe process provided a
moreaccuratemodel.Theseoutcomesarenotcoincidental.Bothare
drivenbytheincreasingmarketpenetrationoftradingalgorithms(as
described in Chapter 10).
A reduction in overall variance of which a similar fraction is
captured by model forecasts—on the face of it, that is a recipe for a
reduction in return commensurate with the variance shrinkage. But
theface,too,isaltered,intheshapeofshorterdurationmovesanda
greater frequency of moves. The resulting increase in the number of
bets counters the lower revenue from individual bets. It is a partial
counter only and is itself countered in turn by transaction costs of
theincreasedbetcount.Continueddownwardpressureonbrokerage
and trading technology fees has been and will continue to be an
inevitableresult.
At this point the critical question to answer is, How can sys-
tematic exploitation, trading the catastrophe signals, yield desirable
economicresults?

199
StatisticalArbitrageRising
Ideally,onewouldliketoidentifythebeginningofacatastrophe
| jump just      | before           | it occurs,    | allowing |          | sufficient   |      | time to            | make a bet |
| -------------- | ---------------- | ------------- | -------- | -------- | ------------ | ---- | ------------------ | ---------- |
| without        | market           | impact,       | and      | identify | the end      | of   | the move           | soon after |
| it is over     | to               | allow maximal |          | capture  | of           | the  | catastrophe.       | Neither    |
| identification |                  | task has      | proven   | easy     | thus         | far, | but approximations |            |
| based on       | durationmeasures |               | have     | been     | established. |      |                    |            |
Returntothegrowthanddrop(ordeclineandjump,ifyouprefer
| the antithetical |     | reversion) | archetype |     | catastrophe      |     | shown | in Figure |
| ---------------- | --- | ---------- | --------- | --- | ---------------- | --- | ----- | --------- |
| 11.5. Focusing   |     | on the     | build-up  | to  | the catastrophic |     | move, | one can   |
identifyadurationrulethatsignalsabetentrykperiodsfollowingthe
startofthetrenddevelopment.Thattrendonsetbecomesknownonly
severalperiodsintothemove.Statisticalanalysisrevealsadistribution
| of trend      | durations | preceding           |       | a catastrophic |      | retrenchment, |     | and bet   |
| ------------- | --------- | ------------------- | ----- | -------------- | ---- | ------------- | --- | --------- |
| entry is      | signaled  | at a fixed          | point | of             | that | distribution. | The | eightieth |
| percentileisa |           | good operatingrule. |       |                |      |               |     |           |
Timelyidentificationofthediscontinuity,thechangefromdiver-
gencetoreversion,iscriticaltosuccessfulexploitationofcatastrophe
| moves. | There | is much | less statistical |     | forgiveness |     | in the | timing of a |
| ------ | ----- | ------- | ---------------- | --- | ----------- | --- | ------ | ----------- |
betentrythanwasthecaseforpopcornmoves.Therelativespeedof
100
80
60
C
B
40
20
A
D
0
| 0   |     | 10  | 20  |     | 30  |     | 40  | 50  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
FIGURE 11.5
Catastrophemovearchetype

200 STATISTICALARBITRAGE
the catastrophereversion makes the opportunitylossfrom late iden-
tification of a catastrophe much greater than for late identification
of a popcorn move. Failure to enter before the cliff edge, point C
in Figure 11.5, essentially means missing the full opportunity. The
popcorn move seen in Figure 11.3 is quite different. Late entry will
lower return on a bet, but only marginally. Modeling and trading
catastrophemoves must embodya higherstate of alertness.
11.3 TREND CHANGE IDENTIFICATION
There is a rich statistical literature on change point identification
with many interesting models and approaches providing plenty of
fascination. Our purpose here is mundane by comparison, though
challenging nonetheless. (If any kind of pattern recognition in finan-
cial data were not so challenging, we would hardly be writing and
reading about it.) An extremely useful approach from statistical
process control relies on Cuscorestatistics (Box and Luceno1987).
Considerfirstacatastrophesuperimposedonanunderlyingrising
series.Figure11.6showsabasetrendwithslopecoefficient1.0with
a catastrophe move having slope coefficient 1.3 beginning at time
10. Let’s see how a Cuscore statistic for trend change works in this
readily understood illustration. The Cuscore statistic for detecting a
change in trend is:
(cid:1)
Q = (y −βt)t
t
wherey istheseriesofobservations,β istheregularslopecoefficient
t
(therateofchangeintheobservationseriesperunittime1)andt isa
time index. The Cuscore is shown in the lower panel of Figure 11.6.
Despitehavingseenmanysuchgraphsformanykindsoftimeseries,
1Modelsforparametricchangehavemuchwiderapplicabilitythanjusttimeindexed
series,whichisourfocushere.Spatialmodels,whereobservationseriesareindexed
by geographic location rather than sequentially in time, are employed in many
sciencesfromgeologytoseismology(whichoftenhasbothtimeandspaceindexing)
tobiology(EEGreadingsformspecificpatternsacrosstheheadaswellasparticular
temporal development at each site). In stock price analysis, indexing by trade
volumeisemployedintradingalgorithms(seeChapter10)andbysomestatistical
arbitrageurs.

201
StatisticalArbitrageRising
(a)
30
25
20
15
10
5
0
|     |     | 5   |     | 10  |     |     | 15  |     | 20  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(b)
200
150
100
50
0
|     |     | 5   |     | 10  |     |     | 15  |     | 20  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
FIGURE 11.6
Identificationoftrendchange:(a)gradient1.0shiftsto1.3attime
11;(b)Cuscore
Ineverceasetobeamazedattheseeminglymagicalwayinwhichthe
detectionstatisticuncoversanddisplaystheincontrovertibleevidence
| of change.      | The       | slope          | increase       | of            | 30 percent   | from           | initial      | value          | 1.0     |
| --------------- | --------- | -------------- | -------------- | ------------- | ------------ | -------------- | ------------ | -------------- | ------- |
| to subsequent   |           | value          | 1.3 looks,     | as            | just         | written,       | substantial. |                | Thirty  |
| percent         | is nearly | one-third      |                | and that      | surely       | is substantive |              | and            | ought   |
| to make         | us take   | notice.        |                | But the       | graph        | generates      | a            | very different |         |
| perception.     | Were      | it             | not for        | the dashed    | continuation |                | line,        | we             | would   |
| be hard-pressed |           | to notice      |                | the kink      | in the       | line at        | time         | 10. The        | visual  |
| discordance     | is        | too small.     | Pictures       | may           | paint        | many           | words        | but            | here is |
| a case in       | whichthe  | wordsare       |                | moredramatic. |              |                |              |                |         |
| The             | dramatic  | shift          | from           | constant      | to           | exponential    | increase     |                | in the  |
| Cuscore         | statistic | recovers       |                | the situation |              | efficiently    | and          | effectively.   |         |
| Now, how        | does      | the            | Cuscore        | perform       |              | when           | observed     | values         | do      |
| not fall        | neatly    | on prescribed  |                | mathematical  |              | lines?         | Figure       | 11.7           | adds    |
| random          | noise     | (Student       | t distribution |               | on           | five degrees   |              | of freedom,    | a       |
| heavier         | tailed    | distribution   |                | than the      | normal)      | to             | the series   | depicted       |         |
| in Figure       | 11.6.     | If the         | slope          | increase      | was          | visually       | difficult    | to             | discern |
| previously,     | it        | is practically |                | impossible    | now.         | How            | does         | the Cuscore    |         |
statisticfare?

202 STATISTICALARBITRAGE
(a)
30
25
20
15
10
5
0
5 10 15 20
(b)
200
150
100
50
0
5 10 15 20
FIGURE 11.7 Cuscoreidentificationoftrendchangefornoisydata:(a)timeseries;
(b)Cuscore
The illustration in Figure 11.7 is more dramatic than that in the
previous figure over which we were so excited. Eyeball analysis is
of little use here, serving only to generate eyestrain. The Cuscore
statistic, by stark contrast, signals a high probability of a trend
increase by time15 and practical certaintyoneor two periodslater.
11.3.1 Using the Cuscore to Identify a Catastrophe
Intheforegoingexamples,theunderlyingtrendwasconstantandthe
coefficient β in the Cuscore statistic was set to the known value of
1.0. Unfortunately,financial series do not cometo us packaged with
aconvenientquantificationofunderlyingrateofchange.Wehaveto
work with the raw observations. Completing the task of identifying
acatastrophemoveinaspreadseriesrequiresthespecificationofthe
underlying trend prior to the potential catastrophe. At first thought,
onemightsuggestusingalocalaveragecomputedusinganEWMAas
recommendedinChapter3.Butachickenandeggdifficultybecomes
apparentalmostassoonasthesuggestionismade.Thelocalaverage,
be it EWMA or some other formulation, will be contaminated as

StatisticalArbitrageRising 203
soon as the catastrophe move begins. The Cuscore will be in the
impossible position of detecting a change in slope using not the new
and old slope quantification but the new quantification and itself.
Whatisneededisanestimateofthetrendifnochangehadoccurred
allowing that a change may have occurred. Since the timing of a
potentialchange isunknown,what can onedo?
Two simple strategies have some efficacy. For underlying trend
estimation in the presence of potential catastrophes, one can use a
substantialperiodoftime,suchasseveralmultiplesofthecatastrophe
duration, obtained from inspection of the empirical distribution of
catastrophe moves in tradeable spreads.2 A second scheme is to
employanestimateoftheslopecoefficientobtainedfromtheEWMA
ordinarilyfoundtobesensiblefortheseriesunderstudy.Theformula
for themodifiedCuscorestatistic becomes:
(cid:1)
Q = (y −βˆ t)t
t t
whereβˆ istheestimatedcurrentslopecoefficient.Derivationofβˆ is
t t
given in Appendix 11.1 where the Cuscore statistic for trend change
detectionin stock pricesis examined in somedetail.
Operationally,thestatisticworkswell,buttheremaybesuperior
detection procedures for early catastrophe move identification. One
possibility (explored in Appendix 11.1) is to employ a lagged local
trend estimate to avoid the chicken and egg problem. Since it is
‘‘known’’ that catastrophe moves are identified five time-steps after
onset, it is reasonable to estimate the underlying trend by excluding
at least thefive most recent series observations.
Why not lag the EWMA by more than five observations, just to
be‘‘safe’’?(Technically,increasetheprobabilityofdetectingacatas-
trophe move in the presence of noise when the catastrophe build-up
is ‘‘gentle’’). That is a question of the modeler’s art as well as detec-
tor performance characteristics. Significant relevant considerations
2Identifyingcatastrophemovesinpastdataisfarsimplerthandoingsoonline.Any
candidatemovecanbeconfirmedbylaterdatabeforeitisassignedaclassification
andemployedinstudyofidentificationandcharacterizationrules.On-linedecisions
mustbemade,andtradingdecisionstaken,beforesuchconfirmationispossible.Of
course,confirmationiseventuallypossiblebutthatisafteronehasmadeaprofitor
incurredaloss.

204 STATISTICALARBITRAGE
as you pursuethisinvestigation are:
■ What is the distribution of differences between underlying trend
and catastropheprecursor trend?
■ What is the distribution of the magnitude of catastrophic rever-
sions?
■ What is the relationship of the magnitude of catastrophic rever-
sions to the duration of the build-up and the magnitude of the
difference between underlying trend and catastrophe precursor
trend?
■ What is the set of catastrophes that is economically desirable to
capture?
■ What is thecost of a falseidentificationof a catastrophe?
Good hunting!
11.3.2 Is It Over?
A popcorn move finishes when the spread series returns to the
(local) mean, plus a bit beyond the mean contributed by stochastic
resonance. When is a catastrophe move complete? I have most
proficientlyansweredthistodatethroughafixeddurationfollowing
detection of a spike in the opposite direction of the development of
the catastrophe. If the catastrophe developed as an increase over the
underlying trend, as in the previous examples, then the catastrophic
change endingthemovewould bea suddendecrease.
I have not answered the question with the success achieved in
otherareasofstatisticalarbitragemodeling.Whetherthecatastrophic
moveisasinglelargemoveoratrendoverseveralperiods,theonsetis
revealedbyCuscoremonitoring.AsecondmodifiedCuscorestatistic
is employed, recognizing the nature of the move: The underlying
trendisnowthebuild-upof thecatastropheitselfso theappropriate
estimate is based on the interval starting at the estimated onset of
the catastrophe and ending one or two periods before the latest
observation. The Cuscore is specifically looking for a spike in the
oppositedirectionofthecatastrophebuild-up;hereweallowaspike
to be over one or two periods, hence the need to exclude the latest
coupleofobservationsfromthetrendestimate.Includingthemwould
put the Cuscore in an impossible position similar to that described
earlier for the catastropheonsetdetection.

StatisticalArbitrageRising 205
Besteffortstodateinspecifyingabetexitrule,catastropheover,
is a combination of the duration and magnitude of the catastrophic
move. A significant danger is waiting too long and getting caught in
a subsequent catastrophe which negates the gains of the first. There
is plenty of room here for improvement in modeling and trade rule
prescription.
11.4 CATASTROPHE THEORETIC INTERPRETATION
Algorithms are formulaic and primitive; there is no comparison to
human consciousness. Most traders are inconsistent and unfaithful
to their model(s). Algorithms are dumbly consistent, unimaginative.
Still, with many algorithmic interactions taking place in the market
there may be emergent behaviors, unpredictable from pure analysis
of individualalgorithm to algorithm interaction.
Examine the Catastrophe surface3 shown in Figure 11.8. The
catastrophemove, a slowbuild-up then a suddendrop,is created by
3Ichosetocallthenewreversionpatternthecatastropheprocess,ratherthanpopcorn
2 or some other label, because it is catchy and does capture the rather different
move dynamic than is both suggested by the name and exhibited by the popcorn
process. The development of an explanatory model of investor behavior, which
might represent why the new style moves occur, is separated from the description
andexploitationofthosemoves.Theunderlyingelementsofalgorithm-to-algorithm
interactionandgrowingpopularityanduseoftradingalgorithmsinplaceofdirect
humanactionareundisputed.Theyareobservedfacts.Stockpricehistoriesarealso
incontrovertiblefacts.ThepatternsIhavediscernedinthosehistoriesaredebatable:
ThereisalotofnoiseinanyexampleIcouldshow.
Tradingmodelsbuilttoexploitthedynamicsrepresentedbythepopcornand
catastrophe processes have undeniable track records. That is existential proof of
modelefficacyandsupportsthevalidityofthepatterndescriptions,butitdoesnot
prove any theory of why the patterns are the way they are. The popcorn process
has been so long established and so widely exploited at multiple frequencies that
providing a rationale has not received much attention. The rise of a new pattern
with the background of failure (interms of economic exploitation)of the oldalso
doesnotrequirearationalization.Ifitpersistsandstatisticalarbitrageursbeginto
discoveritandchurnoutdecentreturns,onceagaininvestorswillexperiencetheir
owncatastrophicshiftfromskepticism(fearofloss)tohope(greed).
While a rationalization is not necessary for the rise of the phenomenon of
reversionbycatastrophe,anunderstandingofmarketforcesdrivingnewdynamics
and a cogent, plausible theory of how those forces interact and might produce
(Continued)

206 STATISTICALARBITRAGE
continuousmovesthroughatwo-dimensionalspace.Thedimensions
correspondtoa‘‘normal’’factoranda‘‘splitting’’factorincatastro-
phe theory parlance. At low levels of the splitting factor, variation
in the normal factor causes smooth variation in the outcome sur-
face. At high levels of the splitting factor, movement in the normal
factor generates outcomes in two distinct regions, separated by a
discontinuity—thecatastrophicjump.Thediscontinuityisasymmet-
ric: Jumps ‘‘up’’ and jumps ‘‘down’’ occur at different levels of the
normal factor for a constant level of splitting factor; this is known
as hysteresis, commonly interpreted as inertia or resistance. (Figure
11.9 shows a cross-section of the catastrophe surface, parallel to
the normal axis, at a high level of splitting factor, illustrating the
asymmetric jump process.)
Thisistheclassicaldescriptionofthetwo-dimensionalcuspcatas-
trophe. Application to stock price development identifies ‘‘avarice’’
withthenormalfactorand‘‘fear’’withthesplittingfactor.Consider
amovementoverthesurfacebeginningatA,withalowleveloffear.
emergentpatternsisnecessarytopromoteunbiasedcriticalattentionintheformative
period.Thesimplecatastrophetheorymodelpresentedinthetextisofferedasone
possiblewayinwhichidentifiedmarket forcesrecently introducedandgrowingin
influenceasoldbehaviorsandinteractionsaresupplantedmightbeunderstood.The
catastrophemodelisaplausiblerepresentationofwhatiscurrentlyknown,butitis
notaformalmodelfromwhichpredictionscanbemade.V.I.ArnoldinCatastrophe
Theory acidly remarks that ‘‘articles on catastrophe theory are distinguished by a
sharpandcatastrophicloweringofthelevelofdemandsofrigorandalsoofnovelty
ofpublishedresults.’’Youhavebeencautioned.
Arnoldfurther remarks, ‘‘Inthe majorityof serious applications... the result
was known before the advent of catastrophe theory.’’ The strong implication in
our context, despite the lapse of 20 years since Arnold wrote, is that even if the
representationandinterpretationofthemodelpresentedisvalid,itisprobablybetter
(morerigorously,moreconvincingly)constructedusingtoolsotherthancatastrophe
theory. I am, in fact, engaged in research using game theoretic tools to model
tradingalgorithminteractions.Thisworkisattooearlyastageofdevelopmentto
report here. Finally, to quote Arnold again, ‘‘In applications to the theory of the
behaviorofstockmarketplayers,liketheoriginalpremises,sotheconclusionsare
more of heuristic significance only.’’ My premises are rather more than heuristic,
algorithm-to-algorithm interaction and increasing dominance of algorithms and
removal of direct humaninteraction,andpatternsdiscerned fromstockprice data
historybeingthereforanyonetoinquireof.Nonetheless,itisquiterighttoregardthe
catastrophemodelofmarketagentbehaviorasheuristic.InkeepingwithArnold’s
tone, I propose to describe the model as the Tadpole theorem with the explicit
intentionthatitisjustalittlebitofPole!

normal factor (avarice)
B
splitting factor (fear)
(cid:127)
C
A
D
FIGURE 11.8 Catastrophesurface
FIGURE 11.9 Cross-sectionofcatastrophesurfaceathighlevelofsplittingfactor
207

208 STATISTICALARBITRAGE
The price develops smoothly in the direction of B with increasing
avarice. As the price increases further to C (the surface is tilted
upward along the splitting factor axis) fear begins to infect partic-
ipants. Eventually, fear surpasses avarice as the dominant concern
and there is a quick price pullback. What is the nature of the fear?
Simply that the divergence in price from recent local trend is not
fundamentally justified but is promoted by (algorithms’) attempts
to over-exploit buyers. (Algorithms don’t actually experience fear,
or have any experience at all, nor do they act from or demonstrate
emotion. Bear with the sloppy, informal use of descriptive language:
This is a work in progress. I have not by any means established
‘‘the’’ theory. Indeed, as you can see, I am still working on proper
explicationofwhatIhavehypothesizedabouttheprocessunderlying
observed price dynamics.) To repeat, algorithms have no conscious
experience.However,algorithmsdoencapsulatelearningaboutprice
movementdynamics(seeChapter10),knowledgeofhowmuchisto
be given up or gained through backing away from the market, and
waiting.Allthisaswellasinformationoncurrentmarketmovesfeeds
intoacalculatedreactionthathastheappearanceoffear—pullback.
The depiction of fear and avarice factors represents the combi-
nation of participants—buyers, sellers, specialists—as represented
through their algorithms. The avarice axis measures the maximum
state of avarice affecting traders and specialists: Whoever has the
greediest sentiment of the moment dominates interactions and price
movements. In like manner, the fear axis measures the maximum
state of fear infectingparticipants.
Asbuypressureisseenbythespecialist,pennyingbegins.Trading
algorithms, typically with some pricing room permitted in order to
completetrades,followthespecialistup.Responding,thespecialist’s
avarice increases and pennying continues (possibly picking up pace,
thoughthedescriptionheredoesnotrequirethatlevelofspecificity).
As these interactions continue, price is moved higher until trading
algorithms determine that it is time to suspend buying: Calibrated
on much previous data to ‘‘expect’’ how much will be necessary
to complete trades, unemotional algorithms display saintly patience.
Buypressureeases. Immediatelythespecialists’avarice turnstofear.
Keeping price high will generate no profit if buyers stay mute and
there is no business. Sellers share the fear. Price drops precipitously
(in comparisonwith the rise) to rekindlebuyer interest.

StatisticalArbitrageRising 209
One might ask, Why not smooth decline? Because reaction
to fear is different from satisfying avarice (whether it is fear of
sellingtoocheaplyorbuyingtooexpensively),notwithstandingalgo-
rithms.Rememberthatalgorithmsaredesignedandcodedbypeople.
Patience. Wait for a significant decline. Therefore, without interme-
diateactivity, downwardpennyingaccelerates and,inmanycases, is
observed as a multipennycatastrophicdrop.
Satisfied that patience has paid off, the cycle begins over again,
very likely from a starting price higher than the starting price of the
original move, as these short-term catastrophic retrenchments are
usually partial. Enthusiasm, avarice, builds again quickly and price
races ahead of the sustainable growth path. Realization sets in, fear,
and equilibriumis quickly,if temporarily,restored.
How does this description of algorithmic interaction and the
resulting behavior of stock prices relate to spreads? Directly. Stock
pricesmoveatdifferentialratesastheyalwayshave.Thecatastrophe
moves of individual stocks naturally combine to generate catastro-
phe moves in spreads. Dynamics are different; scaling is different.
But the basic description is identical.
11.5 IMPLICATIONS FOR RISK MANAGEMENT
A valuable risk management tool in the successful management of
many statistical arbitrage models is the so-called hurdle rate of
return. A model’s forecast function provides an explicit expected
rate of return for any contemplated bet. Managers typically specify
aminimumrateof return,thehurdle,whichmust besatisfied before
a bet is made to avoid collections of bets that are, in the aggregate,
probabilisticallysurelosers.Intimesofperceivedheightenedgeneral
risk,typicallyexemplifiedbyincreased volatility,actual orexpected,
a standard practice is to raise the hurdle. This prophylactic action is
designedtoavoidenteringreversionbetsearly,whiledivergenceisstill
a strong force, thereby avoiding initial losses and, hence, increasing
return. The tactic is a broad sweep action that is appropriate when
concern is of a general increase in variation not focused on specific
market sectors or stocks. (The tactic can, of course, be directed
toward specific market sectors or other collections of stocks if there
is reason to be so concerned.)
Forthepopcornprocess,thebasicforecastfunctionisaconstant,
thevalueatanytimebeingreasonablycomputedasanEWMA(with

210 STATISTICALARBITRAGE
moresophisticatedmodelersemployinglocaltrendcomponents,too,
depending on the time scale over which the move is exploited).
Whenthespreadpops,theexpectedreturniscalculatedasafraction
of the deviation between the spread and the forecast value. When
volatilityisexpectedtoincrease,thepopswillbeexpectedtoincrease
in magnitude; waiting for larger pops is obviously sensible. (Slow,
ratherthansudden,increasesinvolatilityareautomaticallymanaged,
feeding into dynamic recalibration of models. The scenario we are
concerned with here is an increase of sufficient magnitude in a short
interval that is outside the capacity of automatic model adjustment.
Thatisariskscenarioratherthanordinaryevolutiondynamics.)The
point is that the expectation-based information is not accessible to
the model from data analysis, but it can be communicated by the
modeler.
Are the considerations of risk, sudden nonspecific increases in
volatility, any different from those just articulated when considering
catastrophemoves? At first blushit doesnot appear so. Catastrophe
moves are a convergence following a divergence, so rescaling for a
spike in volatility is just as relevant as it is for popcorn (or other
reversion) models. That first blush might be of embarrassment upon
further reflection. Since early 2004 when the catastrophe process
emerged as the better descriptor of local price and spread motions,
thegenerallevelofmarket(andspread)volatilityhasbeenhistorically
low(seeChapter9).Wedonothaveanyempiricalguidanceonwhat
will happen when volatility spikes. Rescaling of local catastrophe
moves may be the result. But it could easily be something different.
A good argument can be made that increased volatility will swamp
the catastrophes, certainly sinking the ability to identify and exploit
them on line, leading to the return of the popcorn process. Is such a
developmentmorethantheoreticallyconceivableifthehypothesisof
algorithmic interaction driving price dynamics is and remains true?
What would cause volatility to spike? People, of course. Algorithms
are tools. Ultimately, people drive the process. We are largely in the
realmofspeculationatthispoint.Hereareacoupleoffurtherpoints
to guideyour thinking:
■ Waiting longer in a local trend: a duration criterion rather than
expected rate of return criterion. (Is there a return forecast that
can becombined?)

StatisticalArbitrageRising 211
■ Waiting longer for a bigger build-up means fewer opportunities
and the catastrophic responseis unchanged because in thecatas-
trophe move, the reaction is not to the mean but toward an old,
not really relevant, benchmark level.
11.6 SIGN OFF
The new paradigm is as yet in an inchoate state. It is actually
two paradigms, a mix of a continued variant of the old reversion
paradigm as interstock volatility increases, and the new trend and
reversal paradigm just outlined.
Traditionalinterstockvolatilitydrivenreversion playsmay stage
a resurgence in appeal as a source of systematic return. Rising inter-
est rates, increasing entrepreneurial risk-taking activity, or possibly
a sudden recession-induced market scramble, are the drivers of this
potential.Thepotentialistherebuttheextentoftheopportunitywill
be limited, returns constrained by the structural impact of decimal-
ization, patient institutional trading (VWAP and other algorithms),
and simplecompetition(Chapter9).
The promise of the new paradigm is certain. However, it is not
yet screaming—perhaps this kind of scream will only be heard, like
Santa’s sleigh bells, by believers?
APPENDIX 11.1: UNDERSTANDING
THE CUSCORE
The Cuscore statistic for detecting a change in trend was developed
bystatisticiansworkinginindustrialprocesscontrolwherethegoalis
tobealertedassoonaspossiblewhenaprocessrequiresadjustment.
An example is production of ball bearings of a specified diameter.
The target mean (diameter) is known. Samples of ball bearings are
takensequentiallyandmeasured,theaveragediametercalculatedand
plotted on a chart. Deviations from the target mean occur over time
as the productionmachine is subject to wear. Ball bearing diameters
begin to increase. A plot of the Cuscore statistic reveals the onset of
wearveryquickly.(Inpractice,therangeofdiametersinthesamples
would also be monitored; different kinds of machine wear create
differentkindsof outputvariation.)

212 STATISTICALARBITRAGE
In engineering applications, like the ball bearing example, the
underlying level is a known(cid:2)target value. Thus, in the Cuscore for
detecting a change in trend, (y − βt)t, the slope coefficient, β, is
t
given. As we noted in section 11.3.1, the situation with stock price
data is different. There is no target price at which one can direct
a causal mechanism (notwithstanding hopeful prognostications of
analysts).Therefore,todetectachangeinpricetrends,anestimateof
whatthetrendischangingfromisrequired.Calculatinganup-to-date
estimateof what thetrend isbelieved tobe, alocal trendestimate, is
thewayforward.Monitoringatimesequenceoflocaltrendestimates
itself providesdirect evidence aboutchange therein.
In this appendix we examine the detail of the Cuscore for trend
change detection. The study reveals how the Cuscore works and the
problemsinherentintheuseoflocallyestimatedtrends.Thislatteris
crucial.InsightabouthowestimatedtrendsaffecttheCuscoreiscriti-
caltosuccessfulimplementationofthedetectorand,hence,toonline
exploitation of catastrophe moves. Without timely identification,
there is no economicallydesirablereal opportunity.
InFigure11.10,thelineABCisanarchetypeofachangeoftrend,
the first segment, AB, having slope 0.5 and the second segment, BC,
having slope 1.5. The dashed line BD is the continuation of line AB.
The dashed line AE is parallel to segment BC, having slope 1.5. We
will use these straight line segments—suppose them to be noise-free
price traces to fix ideas, if that helps—to demonstrate the effects on
theCuscorestatisticfromdifferentassumptionsaboutanunderlying
trend when looking for a change in that trend. Knowledge of results
inthenoise-free, theoreticalmodelwill guideourexpectationswhen
we investigate nois(cid:2)ypriceseries.
The Cuscore, (y − βt)t, is the cumulative sum of deviations
t
of the observation series, y , and the expected value assuming the
t
slope β. In Figure 11.10, that translates into the vertical separation
ofyfromthelinesegmentAD.Thefirstobservationisthatallpoints
on AD will generate a zero contribution to Q. If there is no slope
change, Q isidenticallyzero.
When the slope changes, observations depart from the expected
valueunderthebasemodel(ofnochange).Valuesofyalongtheline
segment BC exceed the expected values on line segment BD by an
increasing amount with time. Cumulating these deviations in Q we
obtain thetrace labeled 1 in Figure 11.11.

StatisticalArbitrageRising 213
60
E
50
C
40
30
20
D
10
B
0 A
0 10 20 30 40
FIGURE 11.10 TrendchangearchetypeandCuscorecontributiondetail
Now suppose that we do not know in advance the slope of
line segments AB and BC or that there is a change in slope at B.
Suppose instead, that beginning at A, our best understanding is that
the process should exhibit a slope of 1.0 as shown by line segment
AC (not drawn to reduce clutter). The Cuscore is shown as the
trace labeled 2 in Figure 11.11. Once again, the visual appearance
of the Cuscore is startling. Deviations of a series from an assumed
base model—a difference in the slope of a trend—are made starkly
evident.Thissecondexamplerevealsboththeoccurrenceofachange
(the inflection point in the Cuscore trace) and the information that
theseriesbeginswithasmallerslopethanhypothesizedandswitches
to a slopelarger than hypothesized.
At this point, you probably have an inkling (or more) about the
next few steps.
ReviewFigure11.2.Thefirstthreecatastrophemovescompound
a strong positive trend; the subsequent moves compound a variably
declining trend. How can we operationally, in real time, provide
the Cuscore with a reasonable chance of detecting the superim-
posed catastrophes from the underlying, longer-term trend changes?

214 STATISTICALARBITRAGE
6,000
1
4,000
2,000
0
−2,000
2
−4,000
0 10 20 30 40
FIGURE 11.11 Cuscorewithβ =0andβ =1
An answer offered in the main text is to use a local trend estimate.
Let’s examine how the Cuscore behaves when a known, constant
trend is replaced with a local estimate.
In Figure 11.12, the EWMA consistently underestimates the real
series; that is a well known feature of moving averages, weighted or
otherwise, which are not designed to project a persistent trend. The
Cuscore reflects the ‘‘always trying to catch up’’ condition showing
anincreasingvaluefromthebeginningoftheseries.Theslopechange
is captured, the rate of increase in the Cuscore is picking up, but
thestrengthofinferenceis slowto buildcomparedwiththeCuscore
usinga knownconstanttrend. Theslownessproblem comes directly
from the use of the EWMA after the slope change. In Figure 11.12,
the Cuscore contributions are the differences between the new slope
andtheprojectedoldslope(verticaldifferencesBC–BD)exemplified
by p − q. With an estimated level, the projection of the initial trend
AB to BD generating p − q is replaced with the EWMA generating
themuchsmallerdeviancep−r.Thisisthechickenandeggproblem.
Weneedtoprojecttheearlytrendbeyondthechangepoint,whichis
unknown,to quicklydetect that change point!

(a)
60
50
EWMA
lagged EWMA
C
40
p
30 r
s
20
D
q
B
10
0 A
0 10 20 30 40
(b)
1,500
1,000
500
0
0 10 20 30 40
FIGURE 11.12 (a)Cuscorecontributionsusinglocalmeanand(b)Cuscoreusing
localmean
215

216 STATISTICALARBITRAGE
Updating the local mean estimate after the slope change reduces
thesensitivityoftheCuscoretodetectthatchange.Thissuggeststhat
sensitivity might be recovered by delaying the local mean update.
WhathappensifalaggedlocalmeanestimateisusedintheCuscore?
Returning to Figure 11.12, the Cuscore contribution postchange
increases from p − r to p − s, much nearer to the desirable p − q.
Unfortunately, this move does not eliminate the chicken and egg
problem; it simply relocates the henhouse! While the postchange
contributions to the Cuscore are indeed larger, so are the prechange
contributions. Thus, accurately distinguishing a change in the Cus-
core trace is not more easily accomplished: Premature signaling
may be the frequent result. Reducing the lag—we used five periods
becauseanalysisofacatalogofidentifiedcatastrophemovesinprice
histories strongly suggested that most such moves with subsequent
economically exploitable catastrophe retrenchments are identifiable
five periods into the move—might help, but as soon as we move
from noiseless archetypes to noisy real data, the situation returns to
nearly hopeless.
What we are searching for is something in the data that quickly
and consistently registers a substantive change following the trend
change. In Figure 11.12 the EWMA trace responds quickly to the
trend change. Perhaps an estimate of local trend from the EWMA
might be a sensitive diagnostic? Figure 11.13 shows the estimated
slopecoefficientcomputedastheaverage changeintheEWMAover
themost recent fourperiods:
βˆ t = 0.25(EWMA t −EWMA t−4 )
This estimate shows none of the tardiness of the EWMA-based
Cuscore.Unfortunately,assoonasevenmodestnoiseisaddedtothe
originalseries,theslopecoefficientestimatedeterioratesconsiderably
asasensitivediagnostic,thoughthesensitivityisgreaterforalonger
windowwhentheunderlyingtrendisconstantotherthanatthepoint
of focus here, as shownin Figure 11.14.
Atthispointwehavetwocandidatesfortrendchangedetection,
the Cuscore using a local mean estimate (EWMA) and local slope
coefficient estimates based on the EWMA, each of which looks
somewhat promising. The Cuscore signals the change but is tardy,
the slope signals the change but is also tardy when noisy data is

StatisticalArbitrageRising 217
1.5
1.0
0.5
0.0
0 10 20 30 40
FIGURE 11.13 Estimatedslopecoefficient,βˆ t =0.25(EWMA t −EWMA t−4 )
examined. Perhaps combining the two might amplify the result?
What do two ‘‘tardies’’ make? Before we reveal that, let’s review
the collection of Cuscore statistics examined so far. Figure 11.15
demonstrates the collection of Cuscore statics introduced in this
appendix applied to the noiseless trend change series. Q is the
theo
original Cuscore in which the initial trend is known. Q is the
mm
Cuscoreusingalocalmeanestimate(EWMA),Q istheCuscore
mmlag
usingalaggedlocalmeanestimate,Qb istheCuscoreusingalocally
1
estimatedslope,Qb1 istheCuscoreusingalocallyestimatedslope
lag
fromthelaggedlocalmean,andQb istheCuscoreusingtheactual
true
beforeand after change slopecoefficients.That’s a lot of Cuscores!
Q and Qb are theoretical benchmarks we would like an
theo true
operational Cuscore to approach as closely as possible. Qb is
true
singularly interesting. Return for a moment to Figure 11.10. Qb
true
cumulates deviations from the known line segment AB, so the value
isidenticallyzerofort = 1throught = 20.Att = 21weswitchfrom
the old slope coefficientβ = 0.5 to the new slope coefficient β = 1.5
andthencebegincumulatingdeviationsbetweenobservationsonline

(a)
60
50
observation series
EWMA
40
30
20
10
0
| 0   | 10  | 20  | 30  | 40  |
| --- | --- | --- | --- | --- |
(b)
1.5
1.0
0.5
0.0
| 0             | 10                                                    | 20  | 30  | 40  |
| ------------- | ----------------------------------------------------- | --- | --- | --- |
| FIGURE 11.14  | (a)Trendchangewithnoise;(b)estimatedslopecoefficient, |     |     |     |
| βˆ =0.25(EWMA | −EWMA                                                 | )   |     |     |
| t             | t                                                     | t−4 |     |     |
218

StatisticalArbitrageRising 219
1,500 Q mmlag Q theo
1,000 Q
mm
500
0
−500
−1,000 Qb
true
Qb1 Qb1
lag
−1,500
0 10 20 30 40
FIGURE 11.15 Cuscoresforseveralmodels
segment BC andthelineAE,whichisthenewbasemodel,assuming
gradientβ = 1.5 from inception.
AE is parallel to BC (both have gradient β = 1.5) so the growth
of Q is linear as the deviations are constant. This contrasts with
the standard Cuscore in which the individual deviations increase
sequentially(excludingnoise)and, hence, thecumulativesum grows
fasterthanlinearly(Q ).Qb hastheinitialadvantageoverQ
theo true theo
because the deviations begin large, hence, the speed of detection of
change is faster. The advantage is a function of the relative size
of the two gradients and the time origin of the cumulation—the
duration of segment AB. In our task of identifying catastrophes, the
largertheprechangeduration,thegreaterthediscrepancies(AE–BC)
feeding the Cuscore, the greater the initial advantage over the stan-
dard Cuscore and, therefore, the sooner the likely identification of a
trend change. Which of the noisy sample versions of the theoretical
benchmarks, Qb1 or Q , dominates in practical catastrophe iden-
mm
tificationdependsonthedynamicsofthecatastrophesandprecursor
periods.
Earlier we remarked that Q and Qb are theoretical bench-
theo true
marks that we would like an operational Cuscore to approach as

220 STATISTICALARBITRAGE
0
−2,000
−4,000
^
Qb
−6,000 Qb
true
−8,000
−10,000
0 10 20 30 40
FIGURE 11.16 Cuscoresfornoisydata
ˆ
closely as possible. Remarkably Qb, our ‘‘product of two tardies’’
Cuscore, achieves an impressive standard of closeness with noise-
less data. How is this possible? It is because larger discrepancies
between the observation and the estimated local mean (because of
thelaggardlyperformanceoftheEWMAinthepresenceofsustained
trending) are multiplied by a larger estimated slope following the
change. The efficacy of the Cuscore is not so much the result of two
tardies but of two enhanced discrepancies focused on a specific type
of change. Does the scheme really work with price data? Look at
Figure11.16anddecide.Andthenthinkabouthowonemightdetect
decreases in trend.
The presentation in this appendix is rather informal. For a rig-
orous treatment of dynamic modeling and identification of change,
see Pole et al, 1994. In that reference, the linear growth model pro-
vides explicit parameterization of a local mean and trend (growth),
dynamic updating of parameter estimates and forecasts, and formal
statistical diagnostics for parametric (slope, in our case) change.
Thestandard distributionalassumptionsof theDLM are strictly not
appropriate for stock price data, largely because of notable nonnor-
mality of (normalized) price and return distributions. Nonetheless,
the models are useful if one takes a robust view of the formalities,

221
StatisticalArbitrageRising
| concentrating         | on mean estimates,  | using standard | deviations        | as a |
| --------------------- | ------------------- | -------------- | ----------------- | ---- |
| guide to uncertainty, | and not counting    | on normality   | at all (so-called |      |
| LinearBayes           | methods).           |                |                   |      |
| Happy                 | catastrophehunting! |                |                   |      |

Bibliography
Arnold,V.I.CatastropheTheory.NewYork:Springer-Verlag,1986.
Bollen, N.P.B., T. Smith, and R.E. Whaley (2004). ‘‘Modeling the bid/ask spread:
measuring the inventory-holding premium,’’ Journal of Financial Economics,
72,97–141.
Bollerslev,T.(1986).‘‘GeneralizedAutoregressiveConditionalHeteroskedasticity,’’
JournalofEconometrics,31,307–327.
Box, G.E.P., and G. Jenkins. Time Series Analysis: Forecasting and Control. San
Francisco:Holden-Day,1976.
Box, G.E.P., and A. Luceno. Statistical Control by Monitoring and Feedback
Adjustment.NewYork:JohnWiley&Sons,1987.
Carey,T.W.SpeedThrills.Barrons,2004.
Engle,R.(1982).‘‘AutoregressiveConditionalHeteroskedasticitywithEstimatesof
theVarianceofUnitedKingdomInflation,’’Econometrica,50,987–1,008.
Fleming,I.Goldfinger.London:JonathanCape,1959.
Gatev,E.,W.Goetzmann,andK.G.Rouwenhorst.‘‘PairsTrading:Performanceof
aRelativeValueArbitrageRule,’’WorkingPaper7032,NBER,1999.
Gould,S.J.TheStructureofEvolutionaryTheory.Cambridge:HarvardUniversity
Press,2002.
Huff,D.HowtoLieWithStatistics.NewYork:W.W.Norton&Co.,1993.
InstitutionalInvestor.‘‘WallStreetSouth,’’InstitutionalInvestor,March2004.
Johnson,N.L.,S.Kotz,andN.Balakrishnan.ContinuousUnivariateDistributions,
VolumesIandII.NewYork:JohnWiley&Sons,1994.
LehmanBrothers.AlgorithmicTrading.NewYork:LehmanBrothers,2004.
Mandelbrot, B.B. Fractals and Scaling in Finance: Discontinuity, Concentration,
Risk.NewYork:Springer-Verlag,1997.
MandelbrotB.B.,andR.L.Hudson.The(Mis)BehaviorofMarkets:AFractalView
ofRisk,Ruin,andReward.NewYork:BasicBooks,2004.
Orwell,George.1984.NewYork:NewAmericanLibrary,1950.
Perold,A.F.(1988).‘‘TheImplementationShortfall,Papervs.Reality,’’Journalof
PortfolioManagement,14:3,4–9.
Pole,A.,M. West, andJ. Harrison.AppliedBayesianForecasting andTimeSeries
Analysis.NewYork:ChapmanandHall,1994.
Poston, T., and I. Stewart. Catastrophe Theory and its Applications. London:
Pitman,1978.
Schack,J.(2004).‘‘BattleoftheBlackBoxes,’’InstitutionalInvestor,June2004.
Sobel,D.Longitude.NewYork:PenguinBooks,1996.
223

Index
Accuracyissues,structuralmodels,59–61 Barramodel,21
Adaptivemodel,172 Barron’s,161
Adjustedprices,13n1 Bid-askspread,declining,156–159
AdvancedTheoryofStatistics,The(Kendall, Binomialdistribution,88–89
Stuart,andOrd),63 BlackBoxes,1,3,183–190
Algorithmictrading(BlackBoxes),1,3, dynamicupdating,188
183–190 marketdeflationand,189–190
dynamicupdating,188 modelingtransactionvolumeandmarket
marketdeflationand,189–190 impact,185–188
modelingtransactionvolumeandmarket Blocktradingactivity,173
impact,185–188 Bollingerbands,17,26
AllianceCapital,165 Bondfutures,85–87
Altvest,161 Box,G.E.P.,1,9,48,191
AmericanAirlines(AMR)–Continental Brahe,Tyco,6n3
Airlines(CAL)spread,2,10–16, BritishPetroleum(BP)–RoyalDutchShell
37–39,40–45 (RD)spread,46–47
Antilochus,163
AppliedMultivariateAnalysis(Press),65
‘‘Arbedaway’’claim,159–160 Calibration,12–16,13n1,32–36
ARCH(autoregressiveconditional Carroll,Lewis,67
heteroscedastic)models,75–76 Catastropheprocess,191–221,205n3
ARFIMA(autoregressivefractionally contrastedtopopcornprocess,194–198
integratedmovingaverage),49 Cuscorestatisticsand,200–205,211–221
ARIMA(autoregressiveintegratedmoving cusp,206,208
average),48–49 forecastswith,198–200
Arnold,V.I.,205–206n3 move,194–200
Asianbirdflu,175 normalfactor,206,207
Autocorrelation,129–130 riskmanagementand,209–211
Automatictrading,seeAlgorithmictrading splittingfactor,206,207
(BlackBoxes) surface,205–206,207
Autoregressionandcointegration,47–49 theoreticalinterpretationof,205–209
Autoregressiveconditionalheteroscedastic trendchangeidentificationand,200–205
(ARCH)models,75–76 CatastropheTheory(Arnold),205–206n3
Autoregressivefractionallyintegrated Cauchydistribution,74,126
movingaverage(ARFIMA),49 Changepointidentification,200
Autoregressiveintegratedmovingaverage Chi-squaredistribution,96
(ARIMA),48–49 Classicaltimeseriesmodels,47–52
Avarice,catastropheprocessand,205–209 autoregressionandcointegration,47–49
dynamiclinearmodel,49–50
Ballbearinganalogy,211–212 fractalanalysis,52
Bamberger,Gerry,1n1 patternfindingtechniques,51–52
BankofAmerica,165,185,189 volatilitymodeling,50–51
225

226 INDEX
Cointegrationandautoregression,47–49 DLM(dynamiclinearmodel),45,49–50,57
Competition,returndeclineand,160–162 Dobzhansky,T.,155
Conditionaldistribution,118–119, DoubleAlpha,3
121–122 Doubling,11–12,81–83
Conditionalprobability,69 Dynamiclinearmodel(DLM),45,49–50,57
Consumersurplus,159,162 Dynamics,calibrationand,32–36
ContinentalAirlines(CAL)–American Dynamicupdating,BlackBoxesand,188
Airlines(AMR)spread,2,10–16,
37–39,40–45
Earnings,RegulationFDand,150–151
Continuity,114–117
EEGanalogy,200n1
Correlation:
Elsevier(ENL)–RUKspread,99–101,105
first-orderserial,77–82
Empiricaldistribution,18
duringlossepisodes,151–154
Engle,R.,51,75
Correlationfilters,21–22
Equilibrium,192
Correlationsearches,withsoftware,26
ETFs(exchangetradedfunds),181
Covariance,103
Europeanmarkets,decimalizationand,
Creditcrisisof1998,riskand,145–148
157–158
CreditSuisseFirstBoston,26,38–39,185,
Eventanalysis,22–26
189
Eventcorrelations,31–32
Cuscorestatistics,200–205,211–221
Eventrisk,142–145
Evolutionaryoperation(EVOP),32–36
DaimlerChrysler,24 EWMA(Exponentiallyweightedmoving
Debtrating,riskand,145–148 average),40–47
Decimalization,156–159 catastropheprocessand,202–204,
Defactoredreturns,55–57,65–66 209–210
D.E.Shaw,3,189 Cuscorestatisticsand,216–221
Difference,48 Exchangetradedfunds(ETFs),181
Discountfactor,40,43 Expectedrevealedreversion,121–122
Discretedistribution,73,115 examples,123–124
Distributions: Exponentiallyweightedmovingaverage
binomial,88–89 (EWMA),40–47
Cauchy,74,126 catastropheprocessand,202–204,
Chi-square,96 209–210
conditional,118–119,121–122 Cuscorestatisticsand,216–221
discrete,73,115 Extremevalue,spreadmarginsand,16–18
empirical,18 ExxonMobil(XON)–Microsoft(MSFT)
Gamma,96 spread,101,104
inverseGamma,76–77
joint,70–71 Factoranalysis,54–55,63–66
lognormal,134–135 Factormodel,53–58
marginal,86,93 creditcrisisand,147
nonconstant,82–84 defactoredreturns,55–57
normalfactor,17–18,76–77,82–84, factoranalysis,54–55,63–66
92–98,120–124,134 predictionmodel,57–58
sample,123 FairDisclosureRegulation,150–151
Studentt,75,124–126,201 Fear,catastropheprocessand,205–209
truncated,123 FederalHomeLoanMortgageCorp.
uniform,82–84 (FRE)–Sunamerica,Inc.(SAI)spread,
Dividend,13n1 142–145

Index 227
FederalReserve,165 InverseGammadistribution,76–77
Feedbackmechanism,171–172 Iraq,U.S.invasionof,175–176,179
Fidelity,163
FinancialTimes,165 Janus,46,165
Flamsteed,John,6n3 Jcurve,62–63
Ford(F)–GeneralMotors(GM)spread, Jenkins,G.,48
101–102,106–107 Johnson,N.L.,134
Forecastmonitor,42–43,172 Jointdistribution,70–71
Forecasts:
withcatastropheprocess,198–200
Kendall,Maurice,63
signalnoiseand,167–174
Keynes,J.M.,91
Forecastvariance,26–28
KidderPeabody,150
Fractals,52,59,73
Kotz,S.,134
Gammadistribution,96 Lawofreversion,seeReversion,lawof
GARCH(generalizedautoregressive LehmanBrothers,26,185,189
conditionalheteroscedastic),50–51, Leptokurtosis,73
75–76 LinearBayes,221
Gauss,91 Liquidity,decimalizationand,158–159
Generalizedautoregressiveconditional Logisticfunction,188
heteroscedastic(GARCH),50–51, Lognormaldistribution,134–135
75–76 LongTermCapitalManagement(LTCM),
GeneralMotors,turningpointexample, 145,150
22–25 Lossepisodes,correlationduring,151–154
GeneralMotors(GM)–Ford(F)spread, Luceno,A.,191
101–102,106–107
Geologyanalogy,200n1 Managers:
GlaxoSmithKline(GSK)–Pfizer(PFE)spread, performanceandcorrelation,151–154
173 relativeinactivityof,166–174
GoldmanSachs,26,185,189 Mandelbrot,BenoitB.,52,59
Gould,S.J.,174n1 Marginaldistribution,86,93
Marketdeflation,189–190
Marketexposure,29–30
Heavytails,17–18,91–98
Marketimpact,30–31,185–188
Hurdlerateofreturn,209
Marketneutrality,29
Markowitz,Harry,99
IBM,30 Marsh&McLennan,180
Inhomogeneousvariances,74–77,136–137 Merck,180
InstitutionalInvestor,189 Mergers,returndeclineand,161
Institutionalinvestors,returndeclineand, Microsoft(MSFT)–ExxonMobil(XOM)
163 spread,101,104
Integratedautoregression,48 Miletus,189
Interestrates,91,211 Mill’sratio,123
creditcrisisand,145–148 Moment,sample,17–18,188
volatilityand,165 Momentum,187–188
Internationaleconomicdevelopments,risk MorganStanley,1,3,183–185
and,145–148 Morningstar,165
Interstockvolatility,67,99–112,164–165 Movingaverage,seeExponentiallyweighted
Interventiondiscount,43–45 movingaverage(EWMA)

228 INDEX
Multiplebets,11–12 Redemptiontension,148–150
Mutualfunds,176 RegulationFairDisclosure(FD),150–151
Relativepricemovement,seeInterstock
NationalBureauofEconomicResearch volatility
(NBER),3,18 Resilience,147n1
NBER(NationalBureauofEconomic Returndecline,155–181.SeealsoReturn
Research),3,18 revival;Riskscenarios
Neuralnetworks,51–52 ‘‘arbedaway’’claim,159–160
Newriskfactors,145–148 competitionand,160–162
NewYorkStockExchange(NYSE),3,189 decimalizationand,156–159
Noisemodels,10–18 institutionalinvestorsand,163
multiplebets,11–12 structuralchangeand,179–180
reversebets,11 temporalconsiderations,166–174
rulecalibration,12–16 2003and,178–179
spreadmargins,16–18 volatilityand,163–165
Nonconstantdistributions,82–84 worldeventsandbusinesspracticesand
Nonfactormodels,creditcrisisand,148 recent,174–178
Nonmedianquantilemovements,135–136 Returnrevival,191–221.SeealsoReturn
Nonstationaryprocesses,136–137 decline
Normalfactordistribution,17–18,76–77, catastropheprocess,194–198
82–84,92–98,120–124,134 catastropheprocessforecasts,198–200
NYSE(NewYorkStockExchange),3,189 catastropheprocesstheoretical
interpretation,205–209
Cuscorestatisticsand,200–205,211–221
Observationalrules,xvn1,10–18,37–39
riskmanagementand,209–211
calibration,12–16
trendchangeidentification,200–205
spreadmargins,16–18
Revealedreversion,seeExpectedrevealed
Ord,Keith,63
reversion
Outliers,106,117,129
Reversebets,11
Reversion,lawof,67–89,113–114,
Pairidentification,20–26
139–140
Pairstrading,1–3,9–10
first-orderserialcorrelationand,77–82
Partialautocorrelation,129
inhomogeneousvariancesand,74–77
Patternfindingtechniques,51–52.Seealso
interstockvolatilityand,67,99–112,
Algorithmictrading(BlackBoxes)
164–165
PCA(principalcomponentanalysis),54
lookingseveraldaysaheadand,87–89
Pfizer(PFE)–GlaxoSmithKline(GSK)spread,
nonconstantdistributionsand,82–84
173
innonstationaryprocess,136–137
Poissonprocess,51
serialcorrelation,138–139
Popcornprocess,18–20,58,92
75percentruleand,68–74
contrastedtocatastropheprocess,
instationaryrandomprocess,114–136
194–198,205n3,209–210
temporaldynamicsand,91–98
Predictionmodel,57–58
U.S.bondfuturesand,85–87
Press,S.J.,65
ReyndersGray,26
Principalcomponentanalysis(PCA),54
Riskarbitrage,competitionand,160–161
Probability,conditional,69
Riskcontrol,26–32
Processadjustment,211
eventcorrelations,31–32
Purereversion,118–120
forecastvariance,26–28
examples,122–123,124,126–135,
marketexposure,29–30
139–140
marketimpact,30–31

Index 229
Risksscenarios,141–154 Stationarity,49,84–85
catastropheprocessand,209–211 Stationaryrandomprocess,reversionin,
correlationduringlossepisodes,151–154 114–136
eventrisk,142–145 amountofreversion,118–135
newriskfactors,145–148 frequencyofmoves,117
redemptiontension,148–150 movementsfromotherthanmedian,
RegulationFairDisclosure(FD),150–151 135–136
RoyalDutchShell(RD)–BritishPetroleum Statisticalarbitrage,1–7,9–10
(BP)spread,46–47 Stochasticresonance,20,50,58–59,169,
204
Stochasticvolatility,50–51
S&P(Standard&Poor’s):
Stocksplit,13n1
S&P500,28
Stoploss,39
futuresandexposure,21
Structuralchange,returndeclineand,
Sampledistribution,123
179–180
Santayana,George,5n2
Structuralmodels,37–66
SARS(severeacuterespiratorysyndrome),
accuracyissues,59–61
175
classicaltimeseriesmodels,47–52
SecuritiesandExchangeCommission(SEC),
doublingand,81–83
3,150–151
exponentiallyweightedmovingaverage,
Seismologyanalogy,200n1
40–47
September11terroristattacks,175
factormodel,53–58,63–66
Sequentiallystructuredvariances,136–137
stochasticresonance,58–59
Sequentiallyunstructuredvariances,137
Stuart,Alan,63
Serialcorrelation,138–139
Studenttdistribution,75,124–126,201
75percentrule,68–74,117
Sunamerica,Inc.(SAI)–FederalHomeLoan
first-orderserialcorrelationand,77–82
MortgageCorp.(FRE)spread,142–145
inhomogeneousvariancesand,74–77,
136–137
Tailarea,17–18
lookingseveraldaysaheadand,87–89
Takeoverannouncements,eventriskand,
nonconstantdistributionsand,82–84
142–145
U.S.bondfuturesand,85–87
Tartaglia,Nunzio,1–2,11–12
Severeacuterespiratorysyndrome(SARS),
Temporalconsiderations:
175
BlackBoxesand,185–188
Shackleton,E.H.,113
returndeclineand,166–174
Sharperatio,116
Timeweightedaverageprice(TWAP),193
Shaw(D.E.),3,189
Transactionvolume,BlackBoxesand,
Shell,seeRoyalDutchShell(RD)–British
185–188
Petroleum(BP)spread
Truncateddistribution,123
Sinusoid,19–20,170
Turningpointalgorithm,22–25
Spatialmodelanalogy,200n1
Turtletraderule,11,20
Specialists,3,156–157
TWAP(timeweightedaverageprice),193
Speer,Leeds&Kellog,189
Spitzer,Elliot,176,180
Spreadmargins,16–18.Seealsospecific Uniformdistributions,82–84
companies U.S.bondfutures,85–87
Standard&Poor’s(S&P): Utilityfunction,38
S&P500,28
futuresandexposure,21 Variances,inhomogeneous,74–77,136–137
Standarddeviations,16–18 Vector,189

230 INDEX
Vioxx,180 Volatilitymodeling,50–51
Virgil,183 Volumepatterns,24–25
Volatility: VWAP(volumeweightedaverageprice),
BlackBoxesand,189–190,193–194 163,165,193
catastropheprocessand,209–211
interstock,67,99–112,164 Waveletanalysis,51–52
measuringspread,108–112 Wilde,Oscar,37
returndeclineand,163–165 Wilmott,Paul,1n1
Volatilitybursts,75–76 Worldevents,returndeclineand,174–178
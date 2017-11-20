# Lokaverkefni-3-onn
## Lokaverkefni fyrir FORR2HF05CU, GSF2A3U og VEFÞ2VF05CU
### Markmið Verkefnis
Búa til nokkurskonar hlutabréfamarkað þar sem margir geta tekið þátt en einnig verða tölvur sem spila. Notendur munu geta keypt og selt
hluti fyrir mismunandi verð og mun leikurinn snúast um að afla sem mestum fjár en hlutir á markaðnum munu sveiflast samkvæmt "fréttum"
sem breyta gengi hluta umtalsvert en einnig munu verð breytast eftir því á hvaða verði notendur kaupa og selja og þriðji parturinn sem 
hefur áhrif á gengi er hvernig hlutnum gengur (fréttir hafa mikil áhrif á þetta).
### balancing
⋅⋅*. Það munu vera limits fyrir því hversu mikið spilendur geta ráðið verðinu við hverja færslu til að koma í
veg fyrir markaðsmisnotkun og þannig að fréttir og gengi hlutna hafi áhrif á leikinn.
⋅⋅*. Mögulega mun vera banki sem við getum notað til að jafna leikinn út og flýta fyrir hlutum ef þess þarf. t.d. gæti bankinn keypt hluti undir
markaðsverði ef við sjáum að hlutir seljast mjög hægt eða hann mundi selja hluti rétt yfir markaðsverð fyrir sömu ástæðum. Mögulega hægt að
ávaxta pening eða fá lánað hjá bankanum fyrir ákveðna vexti. Verslun við bankan mundi aldrei vera gróðvænleg og lán mundi skera niður 
hagnað vegna vaxta sem og að ávaxta mundi vera rétt nóg til að koma út í plús en ætti þó aldrei að fara fram úr eða verða betra en að
ávaxta í góðum hlutum. Þannig gæti bankinn komið í veg fyrir að fólk seldi hluti á fáránlegu verði, komið í veg fyrir gjaldþrot eða kannski
ef þú finnur mjög góða fjárfestingu að það borgi sig að fá lánað hjá bankanum til að kaupa meira og að geyma pening í banka mundi búa til
auka markmið sem væri að græða meiri prósentu en bankinn getur gefið.
⋅⋅*. Bankinn mundi bara lána ákveðið háa upphæð(fer mögulega eftir heildarstöðu notenda)
⋅⋅*. Vextir sem bankinn gefur gætu mögulega breyst eftir því hversu mikill peningur er í heild sinni í ávöxtun hjá bankanum.
### Eiginleikar
1. Gagnagrunnur sem heldur utan um allar upplýsingar.
⋅⋅*. Upplýsingar og staða notenda og bots.
⋅⋅*. Upplýsingar um alla hluti sem er verslað með.
⋅⋅*. Upplýsingar um færslur sem hafa átt sér stað.
⋅⋅*. Upplýsingar um fréttir sem hafa átt sér stað.
⋅⋅*. Upplýsingar um bankan
⋅⋅*. Upplýsingar munu uppfærast í töflum sjálfkrafa 
2. Vefsíða sem notendur nota til að taka þátt í leiknum.
⋅⋅*. Síða sem verður sett á netið og mun uppfæra verð og gengi hluta á tilteknu fresti
⋅⋅*. Frétta síða sem birtir fréttir sem hafa áhrif á markaðin, sem og gengi hluta(mögulega vinsælustu hlutirnir)
⋅⋅*. Loggin fyrir notendur
⋅⋅*. Sessions fyrir þær upplýsingar sem eru ekki geymdar í gagnagrunninum
⋅⋅*. Uppflettisíða þar sem verður hægt að fletta upp hlutum, birta upplýsingum um hlutinn og ef notandi er innskráður þá leyfa honum 
að kaupa
⋅⋅*. Sérstök síða fyrir notendur þar sem verður hægt að sjá upplýsingar um stöðu notenda og þá hluti sem hann á.
⋅⋅*. Highscore síða sem mun birta hverjir notendur eru með mestan pening ( mögulega birta peningin sem notandi á sem og áætlaða heildareign)
3. Virkni forrits
⋅⋅*. Öll virkni sem þarf að eiga sér stað milli gagnagrunns og vefsíðunar. 
⋅⋅*. Bots sem munu spila eftir settum reglum (til að auka magn "spilenda" í leikinn þar sem leikurinn þarf á spilendum að halda til að virka)
bots munu vera misgóð í leiknu og taka mismiklar áhættur.
⋅⋅*. Stærðfræði sem sér um að áætla markaðsverð hluta

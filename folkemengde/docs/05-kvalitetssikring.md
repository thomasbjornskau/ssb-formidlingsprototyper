Steg 5 i formidlingsprototype for folkemengde · versjon 0.2 · 30.10.2026 · Status: del A kontrollert av fagseksjonen 30.10.2026. B og C er ikke besvart

# Kvalitetssikring: Befolkning (folkemengde)

Listen samler alt fra stegene 1–4 som er tolkning, eget valg eller ikke bekreftet, og den **erstatter** listene i `01-innsikt.md` (avsnitt 7 og 8), `02-kvalitetssikring.md`, `03-kildekart.md` (hull og hindre) og `04-byggenotat.md` (nye valg). Prototypen er også gått gjennom på nytt for påstander som ikke sto i noen liste. To ble rettet, se «Avklart underveis».

**Prototypen:** https://thomasbjornskau.github.io/ssb-formidlingsprototyper/folkemengde/index.html

Kildene `[K1]`–`[K10]` viser til `01-innsikt.md`. Tallene er hentet fra statistikkbanken 21.10.2026 og kontrollert av `scripts/lag_data.py` ved hvert bygg (se `04-byggenotat.md`, avsnitt 3).

## A. Må avklares

Dette kan være feil, eller kan gi et misvisende inntrykk hvis det er feil.

| # | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes | Svar |
|---|---|---|---|---|---|
| 1 | Den negative nettoinnvandringen i 2. kvartal 2026 (−1 590) skyldes i stor grad opprydding i folkeregisteret, og mange av utvandringene skjedde tidligere. Kvartalet er merket «Opprydding i registeret», og søylene viser at 205 av 357 kommuner hadde negativ nettoinnvandring, mot 148 året før | Lesehjelpen, kvartalsvisningen, søylene for kommuner med negativ nettoinnvandring | `[K2]` (artikkel 19.8.2026) | Hvor stor del av de 11 685 utvandringene skyldes oppryddingen? Gjelder det samme 2. kvartal 2020 og 2021, de to andre kvartalene med negativ nettoinnvandring siden 1997? Bør de også merkes? | **Magnus Haug 30.10.2026:** Det er alltid noen slike utvandringer, og i enkeltkvartaler (som regel 2. eller 3.) hoper de seg opp. Se vedlegg 26_1411. **Gjort:** noten under søylene og lesehjelpen sier nå at etterregistreringer skjer hele tiden og hoper seg opp i enkelte kvartaler. Merket står bare på 2. kvartal 2026, som artikkelen omtaler. Vedlegget er ikke lagt inn i repoet |
| 2 | «Noen står registrert som bosatt selv om de har flyttet ut. SSB anslår dem til om lag 0,44 prosent» | Lesehjelpen, konseptgrafikken | SSB Notater 2024/3 `[K4]`. Feilkildeteksten i «Om statistikken» viser ellers bare til undersøkelser fra 1990-tallet `[K1]` | Er 0,44 prosent tallet dere vil at vi bruker? Bør det stå som et spenn, eller med årstall? | **Magnus Haug 30.10.2026:** Greit å ta utgangspunkt i tallet, men formuleringen må vise usikkerhet. **Gjort:** «SSB har anslått at det gjelder om lag 0,4 prosent, men anslaget er usikkert», i lesehjelpen og konseptgrafikken |
| 3 | Kommunetallene følger «Kommuner 2024, sammenslåtte tidsserier». 0 i tabellen tolkes som at kommunen ikke fantes, og vises skravert. Ti kommuner har et slikt opphold midt i serien, for eksempel Hole 1964–1976 og Haram 2020–2023. 17 kommuner starter etter 1951 | Kortet for valgt kommune, den lange linjen, komponentene | 06913 `[K7]`, kildekartet avsnitt 2 | Er tolkningen riktig? Er sammenslåtte tidsserier det dere anbefaler for en kommunevelger? | **Magnus Haug 30.10.2026:** Riktig for folketall. Enkeltkommuner kan ha 0 i fødsler, døde eller flyttinger i enkeltkvartaler. **Sjekket:** prototypen tolker bare 0 i folketallet som at kommunen ikke fantes, ikke 0 i komponentene |
| 4 | Kommunene summerer til landet hvert år fra 1971. I 1952–1970 avviker de med inntil 3 294 personer (1969). Landstallet hentes derfor fra 05803, og kommuneseriene vises fra 1951 med merknad | Den lange linjen, bunnteksten | 06913 mot 05803, kontrollert ved bygging | Hva skyldes avviket? Er kommunetallene før 1971 gode nok til å vises? | **Magnus Haug 30.10.2026:** Tallene er publisert, så vi kan anta at de er gode nok. **Ingen endring** |
| 5 | Aldersfordelingen for 1915 (10211) summerer til 2 483 269, mens befolkningen i 05803 er 2 486 269. Avviket er nøyaktig 3 000. Fem andre år avviker med −3 til +2 | Pyramiden med glidebryter (1915) | 10211 mot 05803, kontrollert ved bygging | Er dette en feil i én av tabellene? Hvilken? | **Magnus Haug 30.10.2026:** En unøyaktighet i en eller flere aldersgrupper i 10211. Tallet i 05803 stemmer med det aldersfordelte folketallet i de historiske tabellene (NOS A 986). Jf. tabellnoten til 10211: «Det kan forekomme små unøyaktigheter i enkelte årganger». **Gjort:** pyramiden for 1915 har en merknad, og forklaringen står i kommentaren til kontrollen i `lag_data.py` |
| 6 | Korreksjonen forklares som «forsinkede meldinger og rettinger i registeret». Den regnes av oss for hver kommune og hvert år (befolkningsendring minus fødte, døde og flyttinger). I komponentstolpene er den ikke tegnet, og streken viser folkeveksten | Regnskapet for siste år, toppgrafikken, komponentene, nøkkeltallet «Korreksjon» for kommuner | Definisjonen av korreksjonspost `[K1]`. For 2025 er den 375 for landet og ulik 0 i 206 kommuner (største: Oslo 49) | Er forklaringen riktig, og godtar dere at stolpene ikke summerer eksakt til veksten? | **Magnus Haug 30.10.2026:** Ja, i tillegg til endringer i registeret som er så spesielle at de ikke fanges opp når statistikkfilene lages. Det tallet fag får flest spørsmål om ved årspubliseringen. Forsinkelser betyr noe for 4. kvartal, men skal ideelt sett ikke påvirke helårstallet. Formuleringen bør være «tilstrekkelig ullen uten å være parodisk unnvikende». **Gjort:** «endringer i befolkningen som ikke fanges opp når statistikken lages, blant annet forsinkede meldinger». Stolpene som ikke summerer eksakt, er godtatt |
| 7 | Tidligere kommunenavn i søket kommer fra Klass 131 (184 søkeord). Fem er rettet for hånd og merket som usikre: Skodje, Ørskog og Sandøy → Ålesund; Stokke → Sandefjord; Varteig → Sarpsborg. Kortet sier «tidligere kommune, nå en del av …» | Søket og kortet | Klass 131 `[T]` | Er de fem koblingene riktige? Er det andre søkeord som gir feil kommune? | **Magnus Haug 30.10.2026:** Ja, så lenge koblingene kommer fra statistikkbanken eller Klass. **Merk:** de fem er rettet for hånd, så svaret dekker dem ikke helt. Bør nevnes ved neste kontakt |

## B. Bør leses

Formuleringer, tolkninger og egne valg.

| # | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 8 | «Bare den som skal bo i Norge minst seks måneder, telles» og «Bostedet er der man sover». Nordiske flyttinger, studenter, gifte, militære og diplomater er utelatt | Lesehjelpen, konseptgrafikken | 6-månedersregelen og døgnhvile `[K1]` | Om forenklingen er godt nok |
| 9 | Asylsøkere uten vedtak nevnes ikke særskilt blant dem som ikke er med | Lesehjelpen, konseptgrafikken | `[K1]` | Om de bør nevnes |
| 10 | Fem hendelser i konseptgrafikken: fødsel, dødsfall, flytter til Norge, flytter fra Norge, flytter til ny kommune | Konseptgrafikken | 01222 `[K6]` | Om andre registerhendelser bør nevnes |
| 11 | Setningen i toppgrafikken velges etter forholdet mellom veksten siste år og for tre år siden: «falt kraftig» (≤ 0,4), «omtrent halvert» (≤ 0,6), «lavere» (< 0,9), «samme nivå», «høyere». For landet: «Veksten er omtrent halvert på tre år» (33 060 mot 63 714) | Toppgrafikken | Eget valg `[T]` | Om tersklene og ordene er rimelige |
| 12 | «Det er den laveste veksten siden X» brukes bare når alle årene etter X var høyere, og X er minst tre år tilbake | Toppgrafikken | Eget valg | Om formuleringen kan misforstås |
| 13 | Det store tallet avrundes, også for små kommuner: Hole vises som «7 210», og 7 205 står i kortet og tabellene | Toppgrafikken | Eget valg mot fasitlesning | Om små kommuner bør vise eksakt tall |
| 14 | Varsel om små tall under 2 000 innbyggere | Kortet | Samme grense som i regfram | Ingen, med mindre dere har en annen praksis |
| 15 | Andelene etter alder bruker under 20, 65+ og 80+ | Alder | Eget valg. regfram bruker 70+ | Om dere vil ha 67+ eller 70+ |
| 16 | Pyramiden for en kommune har landet som omriss, regnet om fra ettårig alder (10211) til femårsgrupper | Alder | Regnet av oss | Ingen |
| 17 | «De ti største kommunene har 36 prosent av befolkningen, men fikk 42 prosent av veksten» | Ingressen til «Hvor vokser det» | Regnet fra 06913, ti største etter folketall 1.1.2025 | Om sammenligningen er rimelig |
| 18 | Tospråklige navn vises hele, for eksempel «Hábmer – Hamarøy», fordi det samiske navnet ofte står først | Overalt | Statistikkbanken | Om dere foretrekker en annen form |
| 19 | For en kommune heter flyttebalansen «nettoinnflytting» og har en egen farge (marine), fordi den omfatter innenlandsk flytting. For landet heter den «nettoinnvandring» (blå) | Toppgrafikken, komponentene | 06913 slår sammen innenlandsk flytting og inn- og utvandring | Om skillet er tydelig nok |
| 20 | Kvartalsvisningen sier «ikke sesongjustert: sammenlign med samme kvartal året før» | Komponentene per kvartal | `[K1]` | Ingen |
| 21 | Kvartalstall summerer ikke eksakt til årstall: fødte 2025 er 55 381 i kvartalene og 55 401 i årstabellen. Prototypen bruker årstall for hele år | Bunnteksten | 01222 mot 05803 | Om forklaringen i bunnteksten holder |
| 22 | Flyttetall mangler («..») for Sirdal, Haugesund, Sunndal og Smøla i 1951–1957. Vises skravert med merknad | Komponentene per år | 06913 | Ingen, med mindre tallene finnes et annet sted |
| 23 | Innenlandsk innflytting og utflytting summerer ikke til null over kommunene i 2016–2019 (avvik inntil 226 per kvartal), men gjør det fra 2020. Vi antar at det skyldes Svalbard eller uoppgitt kommune `[T]` | Vises ikke | 01222 | Om antakelsen stemmer |
| 24 | Befolkningen ved utgangen av 4. kvartal 2025 er ikke lik 1.1.2026 for Indre Østfold (+29), Nordre Follo (−27) og Vestby (−2). Vi antar en grensejustering 1.1.2026 `[T]` | Vises ikke | 01222 mot 06913 | Om antakelsen stemmer |
| 25 | Etnedal økte med 27 prosent i 2025 (414 innvandringer). Prototypen forklarer ikke hvorfor | Histogrammet, tabellen | 06913, 09588 | Om noe bør sies |

## C. Spørsmål

| # | Spørsmål | Grunnlag |
|---|---|---|
| 26 | Stemmer hypotesene om misforståelser? Hvilke møter dere oftest, og hvilke mangler? H1: folketallet er alle som bor i Norge. H2: «Befolkning 2026» handler om 2026. H3: utvandringen i et kvartal er folk som flyttet det kvartalet. H4: et kvartal kan sammenlignes med kvartalet før. H5: veksten skyldes først og fremst fødsler. H6: innvandring betyr innvandrere. H7: når Norge vokser, vokser kommunene. H8: en kommunes tidsserie er sammenlignbar bakover. H9: store prosentendringer i små kommuner viser en trend. H10: fire kvartaler summerer til årstallet | `01-innsikt.md`, avsnitt 4 |
| 27 | Artikkelen 19.8.2026 sier at fødselstallet nådde bunnen i 2023. Årstallene i 05803 viser 51 480 i 2022 og 51 980 i 2023. Gjelder artikkelen halvårstall? Prototypen sier ingenting om dette ennå | `[K2]`, `[K5]` |
| 28 | Er dette de riktige hovedtallene å løfte fram: folketallet, veksten delt i fødselsoverskudd og nettoinnvandring, antall kommuner med nedgang og alderssammensetningen? | `01-innsikt.md`, avsnitt 2 |
| 29 | Er Magnus Haug riktig fagkontakt, eller bør andre se på deler av prototypen (statsborgerskap, flytting)? | Kontaktperson for 05803, 06913 og 01222, og forfatter av artikkelen 19.8.2026 |

## Avklart underveis

| Hva | Løst |
|---|---|
| Toppgrafikk B sa først «to av tre nye innbyggere kom fra innvandring» | Rettet i steg 2 til «to tredjedeler av folkeveksten kom fra nettoinnvandring». **Ingressen hadde den samme feilen** («kom fra innvandring») og ble rettet i denne gjennomgangen. Andelen regnes nå fra tallene |
| «Folketallet har vokst nesten hvert år siden 1735» var skrevet fast | Rettet i denne gjennomgangen. Teksten genereres nå: «økt i 281 av 291 år siden 1735. Siste år med nedgang var 1882» |
| Lesehjelpen sier at Skatteetaten rydder i folkeregisteret (B3 i byggenotatet) | Står i definisjonene i «Om statistikken» `[K1]`: Skatteetaten rydder løpende og melder ut personer som har flyttet uten å melde fra |
| Årstallene publiseres «i februar» | Rettet i steg 2 til «februar eller mars». 2023-tallene kom 1. mars 2024 |
| «Laveste veksten siden 2024» for Hole, der 2025 var høyere enn 2024 | Regelen ble strammet inn i steg 4 (punkt 12) |
| Toppverdien i toppgrafikken ble først merket på 2012 | Rettet i steg 2 til 2011 (65 565) |
| Tospråklige navn ble talt til 23 i steg 1 | Talt i rådataene i steg 3: 29 |
| Kommuner som ble delt i 2024, viste tomme kvartaler før 2020 | Skravert som «kommunen fantes ikke» i steg 4 |
| Teknisk, ikke fagets ansvar: `selection[...]` i API-URL-ene ignoreres av PxWebApi v2 | Folkemengde bruker `valueCodes[...]`. URL-ene i kpi, regfram, muh og lonnansatt må rettes, men rådataene der er riktige |
| Teknisk: `felles/grafikk.py` finnes ikke i repoet | `lag_grafikk.py` har en lokal reserve |
| Teknisk: filstørrelse 1,76 MB | Akseptert for prototypen |
| Teknisk: kontroll av kommuner mot fylker i 1986 | Nordland og Trøndelag er unntatt, fordi fem kommuner som ble delt i 2024, ligger i restkoden |

Steg 4 i formidlingsprototype for folkemengde · versjon 1.0 · 21.10.2026 · Status: utkast

# Byggenotat: Befolkning (folkemengde)

Bygger på `03-kildekart.md` og den valgte grafikken fra steg 2. Malen tar utgangspunkt i `regfram` (kommunevalg, figurfunksjoner, CSS) og søket i `lonnansatt` (combobox med forslag, «Se alle»). Siden er én fil på 1,76 MB, og to bygg gir identisk fil.

## 1. Hva som er bygget

| Del | Svarer på | Innhold |
|---|---|---|
| Hode | – | Ingress generert fra tallene, kommunesøk med tidligere navn, «Se alle kommuner» (alle 357 etter fylke), «Vis hele landet» og fem eksempler (Oslo, Utsira, Etnedal, Skedsmo, Tråante) |
| Kort for valgt kommune | 4 | Fylke, kommunenummer, folketall og rangering. Viser hvorfor treffet kom («Funnet med søkeordet «Skedsmo»: tidligere kommune, nå en del av Lillestrøm»), når serien starter, år kommunen ikke fantes, og varsel om små tall under 2 000 innbyggere |
| Lesehjelpen | H1, H2, H3, H7 | Fire punkter: bosatt og ikke til stede, tidspunkt og år, registrert og skjedd, landet og kommunen. Tre av dem er generert fra tallene for valgt kommune. Konseptgrafikken ligger i «Slik lages tallene» |
| Toppgrafikk | 1, 2 | Variant A med todelingen fra B: stort avrundet tall, setning valgt etter forholdet mellom veksten nå og for tre år siden, stablede stolper 2006–siste år med folkeveksten som strek, fire nøkkeltall |
| Hvor mange er vi? | 1 | Lang linje (landet fra 1735, kommunen fra 1951) med bryter til vekst per år i prosent. Skravering for år kommunen ikke fantes |
| Hva driver veksten? | 2 | Komponenter per år fra 1951 og per kvartal fra 2016 (bryter). Kvartalsvisningen skiller innvandring og innenlandsk flytting for kommuner. Søyler for antall kommuner med negativ nettoinnvandring per kvartal, med prikker for valgt kommune. Regnskapet for siste år som fossefall med korreksjonen |
| Alder | 3 | Pyramide. For landet: ettårig alder med glidebryter 1846–2026 og 2026 som omriss. For kommunen: femårsgrupper 1986, 2006 og 2026 med landet som omriss. Andel under 20, 65+ og 80+ for landet 1846–2026, med kommunens tre år som prikker |
| Hvor vokser det? | 4 | Histogram over kommunenes vekst (siste år eller siste ti år) med landet og valgt kommune markert. Stolpene kan klikkes og filtrerer tabellen. Fylkene som liggende stolper med antall kommuner i nedgang. Sorterbar tabell over alle kommuner |
| Bunntekst | – | Om tallene, egne beregninger, kilder og hentedato |

Alle figurer har «Vis tallene» og kildelinje med tabellnummer og oppdateringsdato fra json-stat-svaret. Valgt kommune ligger i adressen (`#kommune=3310`). Histogramstolpene og søkeforslagene kan brukes med tastatur.

## 2. Hvordan hull i data vises

- **Kommunen fantes ikke** (0 i sammenslåtte tidsserier): skravert felt i den lange linjen, i komponentene per år og per kvartal. «Kommunen fantes ikke» i tabeller og tips. Linjen brytes og trekkes ikke over hullet. Kortet sier hvilke år det gjelder.
- **Serien starter senere** (17 kommuner): figurene starter i første år med tall, og kortet sier det.
- **Flyttetall mangler** (Sirdal, Haugesund, Sunndal og Smøla 1951–1957): skravert i komponentene per år, med egen merknad for de fire kommunene.
- **Aldersfordeling mangler for 1986 og 2006** (de fem kommunene som ble delt i 2024): årsknappene er deaktivert med forklaring.
- **Landet før 1951**: komponentene vises bare fra 1951, fordi innvandring mangler før det. Veksten i prosent vises fra 1816.

## 3. Kontroller

`lag_data.py` stopper bygget med «Kontroll feilet: …». Negativ test: én verdi i `kommune_kvartal.json` ble økt med 1, og bygget stoppet med «kommunene summerer ikke til landet for Dode3 i 2020K1». Filen ble satt tilbake og er identisk med originalen.

| Kontroll | Toleranse | Største faktiske avvik |
|---|---|---|
| Nøkkeltall 2025–2026 er de publiserte | 0 | 0 |
| Befolkning(t+1) − befolkning(t) = folketilvekst(t), landet | 0 | 0 |
| Kommuner + restkoder = landet | 0 fra 1971. Før 1971: inntil 3 500 | 3 294 (1969) |
| Kommuner = fylker, 1986 og 2026 | 0. Nordland og Trøndelag unntatt i 1986, fordi fem kommuner ligger i restkoden | 0 |
| Kommuner = landet per kvartal (fødte, døde, innvandring, utvandring) | 0 | 0 |
| 2026K2: utgang 5 636 904, nettoinnvandring −1 590 | 0 | 0 |
| Aldersfordeling = befolkning, landet | 3 personer, og −3 000 i 1915 | −3 000 (1915) |
| Aldersfordeling = befolkning, hver kommune 1986, 2006, 2026 | 0 | 0 |
| Kommuneår uten flyttetall | Nøyaktig 28 | 28 |
| Synonymer peker på kommuner som finnes | 0 | 0 |

## 4. Nye valg til kvalitetssikring

Nummerert videre fra `02-kvalitetssikring.md` (T11).

| # | Valg eller påstand | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| B1 | Setningen i toppgrafikken velges etter forholdet mellom veksten siste år og for tre år siden: «falt kraftig» (≤ 0,4), «omtrent halvert» (≤ 0,6), «lavere» (< 0,9), «samme nivå», «høyere» | Eget valg | Om tersklene er rimelige |
| B2 | «Det er den laveste veksten siden X» brukes bare når alle årene etter X var høyere, og X er minst tre år tilbake | Eget valg. Første versjon skrev «laveste siden 2024» for Hole, der 2025 var høyere enn 2024. Rettet | Ingen |
| B3 | Lesehjelpen sier at Skatteetaten ryddet i folkeregisteret i 2. kvartal 2026 | `[K2]` sier at registeret ble ryddet. At Skatteetaten gjorde det, er vår tilføyelse, fordi Skatteetaten forvalter registeret `[T]` | At formuleringen er riktig |
| B4 | Merket «Opprydding i registeret» står på siste kvartal i kvartalsvisningen, også for kommuner | `[K2]` | Om oppryddingen også gjelder 2. kvartal 2020 og 2021 (spørsmål 2 til fag), og om merket bør stå der |
| B5 | Kortet sier «tidligere kommune, nå en del av …» for synonymer fra Klass | Klass 131 | Fem synonymer er rettet for hånd og merket usikre (Skodje, Ørskog, Sandøy → Ålesund; Stokke → Sandefjord; Varteig → Sarpsborg) |
| B6 | Tospråklige navn vises hele, for eksempel «Hábmer – Hamarøy», fordi det samiske navnet ofte står først | Statistikkbanken | Om fag foretrekker en annen form |
| B7 | Varsel om små tall under 2 000 innbyggere | Samme grense som regfram | Ingen |
| B8 | Ingressen til seksjon 4: «De ti største kommunene har 36 prosent av befolkningen, men fikk 42 prosent av veksten» | Regnet fra 06913, ti største etter folketall 1.1.2025 | Om sammenligningen er rimelig |
| B9 | Andelene etter alder bruker 0–19, 65+ og 80+ | Eget valg. regfram bruker 70+ | Om fag vil ha 67+ eller 70+ |
| B10 | Pyramiden for en kommune har landet som omriss, regnet om fra ettårig alder i 10211 til femårsgrupper | Regnet av oss | Ingen |
| B11 | Histogrammet for siste ti år mangler fem kommuner som ble delt i 2024 | 06913 | Ingen |

## 5. Kjente svakheter

- **Filstørrelse.** 1,76 MB er størst i repoet, og om lag 1,2 MB er data. Kommuneseriene fra 1951 og aldersfordelingen for landet hvert år står for det meste. Kan krympes ved å lagre aldersfordelingen for landet bare hvert femte år før 1950.
- **Store tall avrundes også for kommuner.** Hole vises som «7 210», og det eksakte tallet 7 205 står i kortet og i tabellene. Avrundingen motvirker fasitlesning, men kan virke rart for små kommuner.
- **Fargen for nettoinnflytting** (marine) er en annen enn for nettoinnvandring (blå). Det skal vise at kommunetallet omfatter innenlandsk flytting. Det kan forvirre når man bytter mellom landet og en kommune.
- **Kvartalene viser innenlandsk flytting bare fra 2016.** Rådataene for 1997–2015 er ikke hentet.
- **Søket finner ikke stedsnavn som ikke har vært kommuner**, for eksempel «Sandvika».
- **Ingen kart.** Det var ikke prioritert i steg 1, og kommunegrensene måtte ha vært bakt inn.
- **Ikke publisert ennå.** Claude kan ikke pushe til repoet. Thomas legger inn filene selv.

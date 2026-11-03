`Steg 5 i formidlingsprototype for pasient · versjon 0.1 · 03.11.2026 · Status: til faglig kontroll`

# Kvalitetssikringsliste: Pasienter i spesialisthelsetjenesten

Listen samler alt som er tolkning, eget valg eller ubekreftet i prototypen. Den erstatter listene i `01-innsikt.md` (avsnitt 7 og 8), `02-kvalitetssikring.md`, `03-kildekart.md` (avsnitt 6) og `04-byggenotat.md` (avsnitt 4). Numrene i parentes viser til de tidligere listene.

**Prototypen:** https://thomasbjornskau.github.io/ssb-formidlingsprototyper/pasient/

Del A er det vi trenger svar på før prototypen brukes videre. Del B kan kommenteres når det passer. Del C er spørsmål vi vil lære av.

## A. Må avklares

| # | Påstand eller valg | Hvor | Grunnlag | Hva som må sjekkes |
|---|---|---|---|---|
| 1 | En pasient telles i hvert diagnosekapittel hun er behandlet for. Kontakter, opphold og døgn hører til ett kapittel hver. Vi tolker det som at hver kontakt fordeles etter hoveddiagnosen | Lesehjelp, konseptgrafikk trinn 4, diagnoseseksjonen, toppgrafikken | Mengdetallene summerer eksakt over kapitlene, mens pasientene summerer til 1,9 ganger totalen (14824, 2025) | Om fordelingen bygger på hoveddiagnose, eller om bidiagnoser også teller. Teksten er gjort nøytral inntil svaret er kjent |
| 2 | Aldersjustert rate for «I alt» er lik den ujusterte hvert år (450 og 484). Vi tolker det som at standardbefolkningen er årets egen befolkning, og at den justerte tidsserien derfor ikke er renset for aldring | Innvandringsseksjonen (aldersjustert som standard), lesehjelp | 14827 (H4, spørsmål 2) | Hvilken standardbefolkning som brukes, og om det er riktig å si at justeringen bare gjør grupper sammenlignbare innenfor samme år |
| 3 | Egne rater per aldersgruppe og fordelingen av veksten: halvparten fra flere innbyggere, en femdel fra aldring og resten fra økt bruk per person | «Hvem er pasientene?» | Middelfolkemengde fra 07459. Metoden gjenskaper SSBs publiserte rater for alle kapitler innenfor avrundingen, unntatt XV (G17–G19, spørsmål 6) | Om metoden er faglig forsvarlig, og om SSB har grunner til ikke å publisere slike rater |
| 4 | Raten for svangerskap og fødsel (XV) kan ikke gjenskapes. Vår beregning ligger opptil 1,4 per 1 000 under publisert rate, i 10 av 11 år (2025: 10,9 mot 12). De andre kapitlene treffer innenfor 0,51 | Datakontroll D6. Prototypen bruker publisert rate | 14827 og 07459 (G22, hull 8) | Hvilken nevner eller hvilket utvalg 14827 bruker for XV |
| 5 | Døgnopphold for XV falt fra 26 544 i 2016 til 13 584 i 2018, samtidig som O60–O75 falt fra 9 588 til 1 944 pasienter. Siden sier at det ser ut som en endring i kodingen | Toppgrafikken og blokkene for XV | 14824 (G21, hull 4) | Hva som skjedde. Gjelder også P00–P04 (0 fra 2024) og toppen i R95–R99 i 2020 |
| 6 | Raten i psykisk helsevern for voksne falt fra 46 til 44 per 1 000, mens antall pasienter økte 8 prosent. Siden bruker det som eksempel på at en fallende rate skjuler at de unge øker | Psykisk helsevern, kortet om unge | 14820, 14823 (hull 5, spørsmål 5) | Om nevneren er hele befolkningen eller bare 18 år og eldre. Er det hele befolkningen, er raten lite egnet til å vise utvikling |

## B. Bør leses

| # | Påstand eller valg | Hvor | Grunnlag | Hva som må sjekkes |
|---|---|---|---|---|
| 7 | «Sykehus, private institusjoner med avtale og avtalespesialister rapporterer hver kontakt til Norsk pasientregister» | Konseptgrafikk trinn 1 | «Om statistikken» (G1) | Om avtalespesialistenes data kommer inn på samme måte |
| 8 | «13 500 kontakter uten personnummer» faller ut | Konseptgrafikk trinn 2 | «Om statistikken» (G2) | At det er disse som faller ut, og at de er kontakter |
| 9 | «Pasienttall avrundes til nærmeste tall delelig med 3», vår omskriving av «base 3» | Konseptgrafikk trinn 5 | «Om statistikken» (G5) | At det er vanlig avrunding, ikke tilfeldig |
| 10 | Den grå boksen sier at fastlege, kommunale tjenester, ventetid og kostnader ikke er med. «Om statistikken» nevner bare barn og unge i psykisk helsevern og rus | Konseptgrafikk, lesehjelp | Vår avgrensning (G6) | At det ikke leses som at SSB har sagt dette |
| 11 | Definisjonene av poliklinisk konsultasjon og dagbehandling er våre forenklinger. Døgnopphold er rettet til «en innleggelse», etter «Om statistikken» | Ingressen til «Hva får pasientene?» | «Om statistikken», omsorgsnivå 1–3 i NPR | Om forenklingene holder |
| 12 | Korte kapittelnavn i hele prototypen, for eksempel «Øyet» og «Hormoner, ernæring og stoffskifte», med ICD-kodespenn i velgeren | Overalt | Eget valg (G15, G20) | Om fag godtar navnene, eller vil ha ICD-navnene |
| 13 | «Kontroller, oppfølging og annen kontakt» som beskrivelse av Z-kapitlet | Diagnoseseksjonen, variant B | ICD-10 (G14) | Om beskrivelsen er dekkende. Kapitlet omfatter også blant annet screening og risikofaktorer |
| 14 | «Korona» er markert med stiplet linje ved 2020. Det er ikke et brudd i serien | Toppgrafikken og tidsseriene | SSBs artikkel om innvandringsbakgrunn (G11) | At markeringen ikke leses som brudd |
| 15 | «Like mange innleggelser som i 2015» bruker døgnopphold som mål på innleggelser | Ingress, toppgrafikk | 14824 (G12) | At døgnopphold er riktig mål |
| 16 | Aldersgruppene i psykisk helsevern vises som antall, ikke rate | Psykisk helsevern | Ingen publiserte rater per alder (G23) | Om antall er godt nok |
| 17 | Kontakter per pasient bruker pasienter i poliklinikk som nevner | Nøkkeltall, liggetidskortet | Eget valg (G24) | Ingen. Nevnt for fullstendighet |
| 18 | Aldersjustert rate er standardvisning i innvandringsseksjonen | Innvandring | SSBs artikkel bruker begge (G25) | Henger sammen med punkt 2 |
| 19 | «Statistikken har ikke diagnoser her», om psykisk helsevern | Seksjonsingress | 14820–14823 (G26) | At det ikke finnes diagnosetall et annet sted hos SSB |
| 20 | «Lav bruk kan skyldes god helse, men også språk, avstand eller ulik henvisningspraksis.» Avstand er vårt tillegg | Lesehjelp | SSBs artikkel (G27) | Om «avstand» skal stå |
| 21 | Diagnosekapittel V (psykiske lidelser, 51 360 pasienter) står i somatikken uten forklaring | Diagnoseseksjonen | 14824 (spørsmål 4) | Om det er psykiske diagnoser satt i somatiske avdelinger, og om det trenger en setning |

## C. Spørsmål

| # | Spørsmål | Grunnlag |
|---|---|---|
| 22 | Stemmer hypotesene om misforståelser? Særlig at pasienttallet leses som sykdom (H1), at kapitlene summeres (H2), at veksten leses som flere innleggelser (H3) og at lav bruk blant innvandrere leses som bedre helse (H5) | `01-innsikt.md`, avsnitt 4 |
| 23 | Hvilke misforståelser møter dere oftest fra brukere og presse? | – |
| 24 | Nøkkeltabellen på ssb.no har 580 713 pasienter i somatisk døgnbehandling og 199 161 i psykisk helsevern for 2025. Statistikkbanken har 580 716 og 199 158. Er det avrunding i to omganger? | Spørsmål 3 i innsiktsnotatet |
| 25 | Bør siden forklare hvorfor tallene avviker fra Helsedirektoratets og FHIs tall fra samme register, med lenke? | H8, «Om statistikken» |
| 26 | Er Jostein Starrfelt riktig fagkontakt for prototypen, med Geir Hjemås som andre? | Kontaktperson på alle tabellene, forfattere av artikkelen |

## D. Før en eventuell lansering på ssb.no

Fagseksjonen spurte hvor lett det er å få dette som statistikkside. Punktene under er ikke fagkontroll, men de avgjør svaret.

| # | Forhold | Grunnlag |
|---|---|---|
| 27 | Del A må være avklart, og egne beregninger (punkt 3) må enten godkjennes som SSB-tall, med publisering kl. 08.00 og varsling i statistikkalenderen, eller tas ut | «Om statistikken», likebehandling |
| 28 | Plattform: ssb.no er bygget i Enonic XP med React, SSBs komponentbibliotek og Highcharts. Interaktive verktøy som KPI-kalkulatoren og navnesøket er laget som egne sidedeler. Prototypen er en frittstående fil med d3. Tre veier: lenke ut fra statistikksiden, bygge den inn som én side (vi fant ingen mekanisme for det), eller ny sidedel laget av webteamet | Kildekoden bak ssb.no (`statisticsnorway/mimir`), lest 03.11.2026 |
| 29 | Tallene er frosset ved bygging (02.11.2026). En ekstern versjon må hente ferske tall ved hver publisering | `03-kildekart.md` |
| 30 | Universell utforming etter regelverket (WCAG 2.1 AA), testet med skjermleser og tastatur | Ikke gjort |
| 31 | Eierskap: hvem retter, oppdaterer og svarer på henvendelser. Repoet ligger i dag på en privat GitHub-konto | – |
| 32 | Bør: engelsk versjon, brukertest med de tre brukergruppene, avklaring av hvordan KI-bruken skal opplyses | `01-innsikt.md`, avsnitt 5 |

## Avklart underveis

| # | Hva | Hvordan |
|---|---|---|
| 33 | Antall diagnosekapitler sto først som 21 | Rettet til 20 kapitler pluss «Annen» i steg 3. XX (ytre årsaker) ligger i «Annen» |
| 34 | Teksten om diagnoser sa «har fått en diagnose i» og «en person med to diagnoser» | Gjort nøytral i steg 5 («er behandlet for diagnoser fra to kapitler»), i påvente av punkt 1. Gjelder lesehjelp, konseptgrafikk, diagnoseseksjonen og toppgrafikken |
| 35 | Døgnopphold var beskrevet som «innleggelse med minst én overnatting» | Rettet i steg 5 til «Om statistikken»s definisjon. Snittet for XV er 1,6 oppholdsdøgn, så korte opphold finnes |
| 36 | «Uansett hvor mange ganger hun har vært på sykehuset» utelot avtalespesialistene | Rettet til «uansett hvor mange kontakter og innleggelser hun har hatt» |
| 37 | Middelfolkemengde som snitt av 1. januar i året og året etter (G17) | Bekreftet ved at metoden gjenskaper publiserte rater for 21 av 22 kapitler, alle år (D6) |
| 38 | Avrunding, indeks, avkortet akse, utheving og «793 000» (G9, G10, G13, G16) | Ingen sjekk nødvendig |
| 39 | Rådata | Hentet direkte fra PxWebApi v2, uendret. Sju kontroller (D1–D7) stopper bygget, og negativ test er kjørt |
| 40 | Teknisk: kontrollrenderingen av SVG-ene brukte en reservefont, og bygget gir byte for byte lik fil | Ikke fagets ansvar |

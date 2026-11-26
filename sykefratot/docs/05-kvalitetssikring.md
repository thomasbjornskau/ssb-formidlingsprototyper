Steg 5 i formidlingsprototype for sykefratot · versjon 1.0 · 26.11.2026 · Status: til faglig kontroll

# Kvalitetssikring til faglig kontroll: Sykefravær (sykefratot)

**Prototypen:** https://thomasbjornskau.github.io/ssb-formidlingsprototyper/sykefratot/ (versjon 0.1)

Denne listen samler alt som må avklares, og **erstatter listene i 01-innsikt (avsnitt 7–8), 02-kvalitetssikring, 03-kildekart (avsnitt 5) og 04-byggenotat (avsnitt 5)**. Punktene er nummerert fortløpende. Tallene i prototypen er hentet fra statistikkbanken 26.11.2026 og kontrolleres hver gang siden bygges. Det som står her, er tolkninger, formuleringer og egne valg.

**Merking.** `[K1]`–`[K16]`: kilde, se listen nederst. `[T]`: vår tolkning eller vårt valg. `[H]`: hypotese om en misforståelse.

Svar gjerne kort, direkte i listen eller i en e-post med punktnumrene.

## A. Må avklares

Dette kan være feil, eller kan gi et misvisende inntrykk hvis det er feil.

| # | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 1 | Toppen i den sesongjusterte serien er merket «Toppen: 8,01 i 2003», og serien fra 2000 er tegnet som én linje | Toppgrafikken | «Om statistikken» sier at bare sesong- og influensajusterte tall er sammenlignbare før og etter a-ordningen `[K1]`. Endringsraten for 2015K1 er «.» også i de justerte seriene `[K7]` | Kan den sesongjusterte serien sammenlignes over 2015? Hvis ikke: skal vi bytte til sesong- og influensajustert, stiple serien før 2015, eller fjerne annoteringen? |
| 2 | Egenmeldte tilfeller (fra utvalget) og legemeldte tilfeller (fra registeret) står i samme stolpe: «2 av 3 fravær er egenmeldinger» | Korte egenmeldinger eller lange sykmeldinger? | Tabell 12946 har begge i samme variabel `[K10]` | Kan tilfellene sammenlignes på tvers av kildene? Er «fraværstilfelle» definert likt for egenmeldt og legemeldt? |
| 3 | «Prosenten måler dagsverk, ikke personer»: 4,9 prosent av dagsverkene, mens 6,3 prosent av lønnstakerne hadde en sykmelding på referansedagen. Gradering forklarer forskjellen | Slik leser du tallene, punkt 2 | Definisjonene `[K1]`, tabell 12446 `[K12]`. Andre grunner: én referansedag mot tre referanseuker, og hovedarbeidsforhold mot alle jobber `[K1]` `[T]` | Er sammenligningen riktig og rettferdig? Hvilken forklaring vil dere bruke? |
| 4 | SSBs hovedtall og Navs tabeller vises som to måter å lese samme kvartal på: 6,65 prosent (sesongjustert, −0,3 prosent fra kvartalet før) mot 4,9 prosent (legemeldt, ujustert, +1,9 prosent fra året før) | Samme kvartal, to tall | Navs tabellside `[K6]`, Navs pressemeldinger for 3. kvartal 2025 og 2026 `[K6]` `[K16]`. Tallene er gjenskapt fra 12439 `[K7]` | Er beskrivelsen av Navs praksis riktig? I 2026 brukte Nav det sesongjusterte totaltallet som hovedtall, i 2025 det legemeldte |
| 5 | Sykefraværsdagsverk for 2024K2 er 9 400 600 i 12439 og 9 394 200 i 12946 | Ikke synlig i prototypen. Holdt utenfor kontroll B4 | Rådata 26.11.2026 `[K7]` `[K10]` | Er den ene tabellen revidert uten den andre? Alle andre kvartaler er like |
| 6 | Hele landet i kommunefiguren er legemeldt, ujustert fra 12439 (4,9 prosent) | Min kommune | 12451 har ikke landstall `[T]` | Er 12439 sammenlignbar med summen av kommunene i 12451? Begge gjelder bosatte lønnstakere |
| 7 | Egenmeldt på detaljert næringsnivå i 12440 ligger utenfor spennet til undergruppene. Helse og sosial (Q) har 1,0, men helsetjenester (86) har 1,7 og pleie og omsorg (87–88) 1,6. Det gjelder alle 47 kvartaler fra 2015, og industri har samme mønster | Ikke brukt i prototypen. Publisert i statistikkbanken | Tabell 12440 `[K8]` | Hva betyr de detaljerte egenmeldte tallene, og er de riktige? |
| 8 | Jordbruk, skogbruk og fiske (A) og bergverksdrift og utvinning (B) har identiske ujusterte tall i 2025K3 og 2026K3, for i alt, egenmeldt og legemeldt | Ikke brukt i prototypen. Står i tabell 2 og 3 på statistikksiden | 12440 og 13935 `[K8]` `[K13]`. De sesongjusterte tallene er ulike (5,03 og 4,72) | Er det tilfeldig? Det har skjedd i 4 av 75 kvartaler |

## B. Bør leses

Formuleringer, tolkninger, søkeord og egne valg.

| # | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 9 | «Navs sykmeldingsregister: alle legemeldte sykmeldinger» | Konseptgrafikken, trinn 1 | Registeret skal omfatte alt legemeldt fravær. Om lag 5 prosent kunne ikke kobles til et arbeidsforhold i 2022 `[K1]` | Holder forenklingen, eller bør det stå «nesten alle»? |
| 10 | «Hver arbeidsdag med fravær teller, vektet med stillingsprosent og sykmeldingsgrad», med eksempelet 0,5 × 0,8 = 0,4 dagsverk | Konseptgrafikken, trinn 2 | Definisjonen av sykefraværsdagsverk `[K1]`. Multiplikasjonen er vår lesning `[T]` | At regnestykket er riktig. Dager på jobb under aktiv sykmelding er ikke nevnt |
| 11 | Brøken viser ikke antall avtalte dagsverk | Konseptgrafikken, trinn 3 | Ikke funnet publisert `[T]` | Er tallet publisert et sted? Da bør det stå i brøken |
| 12 | «Tallene revideres ved hver publisering» | Konseptgrafikken, trinn 4 | Sesongjusterte tall fra 2015 re-estimeres `[K1]` | Presist nok? Tall før 2015 er låst |
| 13 | «Av 100 avtalte dagsverk gikk i underkant av 7 tapt til egen sykdom» | Ingressen | 6,65 sesongjustert `[K7]`, omregning `[T]` | Formuleringen |
| 14 | «Nesten flatt siden starten av 2025». Brukes når spennet siden starten av året før er under 0,25 prosentpoeng | Toppgrafikken | Mellom 6,54 og 6,67 siden 2025K1 `[K7]` `[T]` | Ordvalg og terskel |
| 15 | Overskriften avrundes til 6,7 prosent. Figuren og nøkkeltallene har 6,65 | Toppgrafikken | Mot fasitlesning `[T]` | – |
| 16 | Den ujusterte serien er tegnet i grått over hele perioden, med bruddlinje i 2015 | Toppgrafikken | Ikke korrigert for bruddet `[K1]` | Bør den stiples før 2015? |
| 17 | Kildelinjen sier at tall før og etter 2015 «bare er sammenlignbare med forbehold» | Toppgrafikken | Venter på punkt 1 | Formuleringen |
| 18 | «Sammenlign med kvartalet før med sesongjusterte tall, og med samme kvartal året før med ujusterte» | Slik leser du tallene, punkt 4 | `[T]` | Er rådet riktig, og slik dere selv sier det? |
| 19 | Prosentpoeng i lesehjelpen er regnet fra publiserte nivåer (6,67 − 6,65 = 0,02) | Slik leser du tallene, punkt 3 | `[T]`. Endringer i prosent er alltid publiserte tall | – |
| 20 | Varighetsgruppene 1–8 og 9–16 dager er slått sammen, fordi arbeidsgiverperioden er 16 dager | Korte egenmeldinger eller lange sykmeldinger? | `[K1]` `[T]` | Er grupperingen faglig rimelig? |
| 21 | Varigheten gjelder bare dagene innenfor kvartalet, og det står i noten | Samme sted | `[K1]` | Godt nok forklart? Mange lange fravær er lengre enn figuren viser |
| 22 | «Det er de lange fraværene som bærer tallet» og «Gapet mellom tilfeller og dagsverk har holdt seg siden 2015» | Samme sted | 12946, alle kvartaler `[K10]` `[T]` | Ordvalget |
| 23 | Etikettene i stolpene rundes med største rest, så de summerer til 100. Andelene er regnet fra antall | Samme sted | `[T]`. Avviker høyst 0,1 fra publiserte andeler | – |
| 24 | Ni yrkesgrupper i figuren. Uoppgitt er utelatt, og høyskole- og militære yrker vises samlet slik tabellen gjør | Hvem har høyest sykefravær? | 12452 `[K11]` `[T]` | – |
| 25 | Yrket som vises først, er Helsefagarbeidere | Finn yrket ditt | Høyest blant de store yrkene i artikkelen `[K2]` | – |
| 26 | 100 søkeord for yrker, 21 av dem merket usikre (for eksempel «jordmor» → spesialsykepleiere, «hjelpepleier» → helsefagarbeidere) | Finn yrket ditt, `data/synonymer.json` | Vårt valg `[T]` | Les listen. Er noen koblinger feil? |
| 27 | «Små yrker kan svinge mye». Yrkene kan ikke vises med størrelse | Finn yrket ditt | 12452 har ikke antall jobber `[T]` | Se punkt 36 |
| 28 | «Omtrent som alle yrker eller hele landet» ved under 0,25 prosentpoeng forskjell. Teksten om svingninger i små kommuner vises når spennet er minst 2 prosentpoeng | Yrke og kommune | `[T]` | Tersklene |
| 29 | «Legemeldt sykefravær for lønnstakere som bor i kommunen, uansett hvor de jobber» | Min kommune | Bostedskommune `[K1]` | – |
| 30 | Kommunetallene har ingen publisert usikkerhet. Prototypen viser hele serien fra 2024 i stedet for bare siste tall | Min kommune | `[T]` | Bør det stå mer om usikkerhet? |
| 31 | Næring er utelatt med vilje til SN2025-tabellene kommer | Om tallene | `[K3]` | Formuleringen |
| 32 | Kjønnsvalget styrer toppgrafikken, SSBs og Navs tall, varighet og yrker | Hele siden | `[T]` | – |
| 32b | «Samme kvartal hvert år» er standard for alle figurer med tall som ikke er sesongjustert. Sesongjusterte figurer viser alltid alle kvartaler | Valget «Sammenlign» øverst | Lagt til etter steg 4 `[T]`. Følger rådet i lesehjelpen (punkt 18) | Er det riktig standard, og er skillet mellom justerte og ujusterte figurer tydelig nok? |

## C. Spørsmål

| # | Spørsmål | Grunnlag |
|---|---|---|
| 33 | Stemmer hypotesene om misforståelser? Hvilke møter dere oftest, og hva mangler? H1 SSB og Nav melder ulikt. H2 6,7 prosent leses som andel syke. H3 fravær er mest korte egenmeldinger. H4 prosent og prosentpoeng blandes. H5 fraværet er rekordhøyt. H6 Norge har verdens høyeste fravær. H7 ujustert og sesongjustert blandes. H8 sesongjusterte dagsverk leses som faktisk omfang. H9 næringsserier over brudd. H10 statistikken dekker alt fravær | 01-innsikt, avsnitt 4 |
| 34 | Er dere riktige mottakere, eller bør andre se på deler av dette? | «Om statistikken» `[K1]` |
| 35 | Artikkelen for 3. kvartal oppgir «9,87 millioner tapte dagsverk», som er sesongjustert. Faktisk tapt i kvartalet var 8,91 millioner. Er det et bevisst valg? | `[K2]` `[K7]`, H8 |
| 36 | Finnes antall jobber eller lønnstakere per yrke, så små yrker kan merkes? | 03-kildekart, hull 2 |
| 37 | Når kommer SN2025-tabellene, og hvor langt tilbake blir de regnet? Prototypen får en næringsseksjon da | `[K3]` |
| 38 | Er avtalte dagsverk publisert et sted? | Punkt 11 |

## Avklart underveis

| # | Hva | Hvordan |
|---|---|---|
| 39 | Navs melding for 3. kvartal 2026 var ikke lest da prototypen ble bygget | Lest 26.11.2026 gjennom pressedekningen `[K16]`. Nav brukte det sesongjusterte totaltallet (6,7 prosent, samme nivå som kvartalet før) som hovedtall. Legemeldt fravær for kvinner gikk fra 6,1 til 6,3 prosent, og menn lå fast på 3,7. Det stemmer med 12439. Prototypen er rettet: «Slik melder Nav» er nå «Navs tabeller», og lesehjelpen sier ikke lenger at Nav melder 4,9 som hovedtall. Se punkt 4 |
| 40 | Lange sykmeldinger var oppgitt som 11,5 prosent av tilfellene | Rettet til 11,6, regnet fra antall i stedet for summen av avrundede andeler (01-innsikt, versjon 1.1) |
| 41 | Etikettene for varighet summerte til 101 | Rettet med største rest |
| 42 | Endringsrater regnet fra nivåer avviker fra de publiserte i 54 av 104 kvartaler | Prototypen bruker bare publiserte endringsrater |
| 43 | Konfidensialitetsavsnittet i «Om statistikken» har maltekst som ikke er fylt ut: «[ev. fyll inn riktig enhet her]» og «[undertrykking, avrunding, støylegging]» | Til orientering for statistikksiden, ikke prototypen |
| 44 | Tekniske forhold som ikke er fagets ansvar: Roboto Condensed er ikke bakt inn i konseptgrafikken. Tipsboksene vises bare med mus, og tallene finnes i «Vis tallene». Siden er 959 kB. Toppannoteringen krysser bruddlinjen på smal skjerm. `naturregnskap` bygger ikke med `felles/bygg.py`, så kontrollen på GitHub kan feile uavhengig av denne prototypen | 04-byggenotat, avsnitt 6 |

## Kilder

- `[K1]` SSB: Sykefravær, statistikkside. Oppdatert 26.11.2026, «Om statistikken» sist oppdatert 3.9.2026. https://www.ssb.no/sykefratot
- `[K2]` Rakel Gading: «Uendret sykefravær i 3. kvartal». SSB, 26.11.2026
- `[K3]` Rakel Gading og Mari Kristine Knutsen: «Økning i sykefraværet». SSB, 28.5.2026
- `[K4]` Tonje Køber og Erik Horgen: «Om å sammenligne sykefraværet internasjonalt». SSB, 6.9.2024
- `[K5]` Tonje Køber og Håvard Lien: «Sykefraværet i Norge øker mer enn i nabolandene». SSB innsikt 2025/2
- `[K6]` Nav: «Nedgangen i sykefraværet fortsatte i 3. kvartal» (2025) og «Sykefraværsstatistikk – kvartalsstatistikk». https://www.nav.no/no/nav-og-samfunn/statistikk/sykefravar-statistikk/sykefravar
- `[K7]`–`[K13]` Statistikkbanken, tabell 12439, 12440, 12441, 12946, 12452, 12446 og 13935, hentet 26.11.2026
- `[K14]` Stortinget: Innst. 149 S (2025–2026)
- `[K15]` Erik Herstad Horgen: «Bedre sykefraværstall uten feriekorrigering». SSB, 20.3.2019
- `[K16]` Navs pressemelding for 3. kvartal 2026, gjengitt av NTB, NRK og Aftenposten 26.11.2026. https://www.nrk.no/artikkel/nav-sykefravar-ligger-hoyt-pa-et-stabilt-niva-1534052 og https://www.aftenposten.no/norge/i/7P0WJK/nav-stabilt-hoeyt-sykefravaer. Navs egen side er ikke lest direkte

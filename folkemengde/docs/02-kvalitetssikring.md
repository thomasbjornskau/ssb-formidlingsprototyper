Steg 2 i formidlingsprototype for folkemengde · versjon 1.0 · 21.10.2026 · Status: godkjent av Thomas

# Kvalitetssikring etter steg 2: grafikk

Påstander og valg i konseptgrafikken og toppgrafikkvariantene som er tolkning, eget valg eller ikke bekreftet. Listen samles med de andre stegene i `05-kvalitetssikring.md`. Kildene `[K1]`–`[K10]` viser til `01-innsikt.md`.

## Konseptgrafikken «Slik lages tallene»

| # | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| G1 | Fødsler, dødsfall og flyttinger meldes til Folkeregisteret hos Skatteetaten | `[K1]` sier at grunnlaget er folkeregisteret. At Skatteetaten forvalter registeret, er vår tilføyelse `[T]` | At det er riktig og ønsket å nevne Skatteetaten |
| G2 | Fem hendelsestyper (fødsel, dødsfall, flytter til Norge, flytter fra Norge, flytter til ny kommune) | Komponentene i 01222 `[K6]` | Om andre registerhendelser (statsborgerskap, sivilstand, annullering) bør nevnes |
| G3 | «Den som skal bo her minst seks måneder, blir bosatt» | 6-månedersregelen `[K1]` | Forenkling: Nordiske flyttinger og særregler (studenter, militære, diplomater) er utelatt. Godt nok for lesehjelpen? |
| G4 | «Bostedet er der man sover» | Døgnhvile `[K1]` | Forenkling: gifte og studenter følger egne regler |
| G5 | SSB får endringene hver dag | `[K1]` | Ingen |
| G6 | Regnskapet 2025 med korreksjon 375 | Tabell 05803, regnet ut: 33 060 − 10 361 − 22 324 `[K5]`. Samme tall i tabell 1 på statistikksiden `[K1]` | Om «korreksjon» er godt nok forklart uten fotnote |
| G7 | Kvartalstall om lag seks uker etter, hele året i februar eller mars | `[K1]`. Artikkellisten viser årstall publisert 21.2.2023, 1.3.2024, 25.2.2025 og 25.2.2026 `[K10]` | Ingen. Første utkast sa «i februar», men 2023-tallene kom 1. mars 2024 |
| G8 | «En opprydding kan samle utvandringer fra flere kvartaler i ett» | `[K2]` om 2. kvartal 2026 | At dette gjelder generelt, ikke bare 2026 (spørsmål 2 til fag) |
| G9 | Overdekning «om lag 0,44 prosent» | SSB Notater 2024/3 `[K4]` | Om tallet er det fag vil bruke (spørsmål 4 til fag) |
| G10 | «Ikke med: opphold under seks måneder og personer uten lovlig opphold» | `[K1]` | Om asylsøkere uten vedtak bør nevnes særskilt |

## Toppgrafikkvariantene

| # | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| T1 | A: «5,6 millioner» som avrundet overskrift | 5 627 400 `[K5]` | Ingen. Avrundet med vilje for å unngå fasitlesning |
| T2 | A: «Veksten er halvert på tre år» | 63 714 i 2022 og 33 060 i 2025, en nedgang på 48 prosent `[K5]` | Om «halvert» er presist nok |
| T3 | A: Utheving av 2022 og 2025 | Eget valg | Ingen |
| T4 | B: «To tredjedeler av folkeveksten kom fra nettoinnvandring» | 22 324 av 33 060, 67,5 prosent `[K5]` | Første utkast sa «to av tre nye innbyggere kom fra innvandring». Det var feil: det blandet nettoinnvandring med antall nye innbyggere (55 243 innvandringer og 55 401 fødte). Rettet før levering |
| T5 | B: Korreksjonsposten (69–464 per år i 2016–2025) er utelatt i stablingen | Regnet fra 05803 `[K5]` | Om fag godtar at stolpene da ikke summerer eksakt til folkeveksten |
| T6 | C: «1 av 3 kommuner» fikk færre innbyggere | 128 av 357, 35,9 prosent `[K7]` | Ingen |
| T7 | C: Inndeling «Kommuner 2024, sammenslåtte tidsserier» | `[K7]` | Spørsmål 5 til fag |
| T8 | C: Tre kommuner uten endring er regnet til «vekst eller uendret» | Eget valg | Ingen |
| T9 | C: Klasser på 0,5 prosentpoeng, med en samleklasse for 3 prosent og mer (to kommuner, 5,6 og 27,0 prosent) | Eget valg | Kommunen med +27,0 prosent (kode 3450) er ikke navnesjekket |

## Avvik fra standardene

- **Konseptgrafikken** følger formatet til prototypene (1200 bred, 390 smal), ikke 1920 × 1080 fra `ssb-konseptfigurer`. Det er samme valg som i regfram og kpi.
- **Variant C** bruker to farger for nedgang og vekst. Grensen er også merket direkte med tekst, så fargen bærer ikke alene.
- **Lyse flatetoner** (blå i B, oker i C) har under 3:1 mot hvitt. De er merket direkte.
- **Kommunenavn** er ikke hentet ennå. SSB-tilkoblingen ga bare koder for kommunelisten. Det løses i steg 3.
- **`felles/grafikk.py`** fantes ikke i arbeidsområdet. `lag_grafikk.py` har en lokal reserve med samme grensesnitt og bytter automatisk når repoet er på plass.

## Beslutning 21.10.2026

Thomas valgte variant A som toppgrafikk, med todelingen fra B i stolpene (fødselsoverskudd og nettoinnvandring, 2006–2025). Konseptgrafikken er godkjent. C blir kandidat til seksjonen om kommunene, med «Min kommune» uthevet i fordelingen.

| # | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| T10 | A (v0.2): Toppverdiene merket er 2011 (65 565), 2022 (63 714) og 2025 (33 060) | `[K5]`. Første utkast av v0.2 merket 2012 (65 405), men 2011 var høyere. Rettet | Ingen |
| T11 | A (v0.2): Korreksjonsposten (−294 til 464 per år i 2006–2025) er ikke tegnet, og tallet over stolpen er folkeveksten | `[K5]` | Samme som T5 |

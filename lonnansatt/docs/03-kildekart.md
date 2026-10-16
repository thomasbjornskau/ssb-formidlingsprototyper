Steg 3 i formidlingsprototype for lonnansatt · versjon 0.1 · 15.10.2026 · Status: utkast

# Kildekart: Lønn (lonnansatt)

**Merkeforklaring.** `[K1]`–`[K13]` viser til kildelisten i `01-innsikt.md`. `[T]` er vår tolkning eller egen beregning. Kontrollene K1–K10 kjøres med `scripts/kontroll_kilder.py`.

**Valg som ligger til grunn.** Toppgrafikk A (desilene mot gjennomsnitt og median) og konseptgrafikken er godkjent i steg 2. Yrket styrer prototypen, og B blir yrkesseksjonen med velger (15.10.2026). Yrkesvelgeren viser nivå og spredning: gjennomsnitt, median, kvartiler og antall jobber, for begge kjønn og per kjønn, 2016–2025. Sammensetning og sektor per yrke og synonymsøk er valgt bort (15.10.2026).

## 1. Spørsmål, datasett og seksjon

| Spørsmål | Datasett | Tabell | Seksjon i prototypen |
|---|---|---|---|
| Toppgrafikk: hva tjener de fleste? | `desiler`, `hovedtall` | 13860, 11419 | Topp |
| 1 Hva er månedslønn, og hva er ikke med? | `hovedtall` | 11419 | Lesehjelp og «Slik lages tallene» |
| 2 Gjennomsnitt, median og fordeling | `desiler`, `hovedtall` | 13860, 11419 | Topp, utdypet i egen seksjon |
| 3 Hva tjener et yrke? | `yrker` | 11418 | Velg et yrke |
| 4 Kjønnsforskjellen | `hovedtall`, `desiler`, `yrker` | 11419, 13860, 11418 | Egen seksjon, og per yrke i velgeren |
| 5 Flere tall for lønnsveksten | `hovedtall`, `arslonn_utbetalt`, `arslonn_palopt` | 11419, 11536, 14858 | Egen seksjon (variant C fra steg 2) |

Alle tabeller er de nyeste i serien, med 2016 som første sammenlignbare år. **Ikke brukt:** 12521 (desiler etter sektor, kan vente), 14378 og 11420 (utdanning, foreløpig til juni og utenfor), 11421, 13310–13312 (alder), 12524, 12525, 13976, 13977 (innvandrere), 11422 og 12852 (fylke og kommune), 12851 (lærlinger), 14756 og 14757 (lønnsintervaller), 11417 (årslønn etter næring). Avsluttede serier før 2015 er ikke brukt.

## 2. Struktur som former prototypen

**Yrkeshierarkiet (11418).** 582 yrkeskoder: totalen, 9 hovedgrupper, 43 tosifrede, 122 tresifrede og 407 firesifrede koder. Hovedgruppe 3 har koden `3_01-03` og omfatter de tre militære yrkene (01–03). En kode `3` finnes ikke. Uten «uoppgitt» (0000) er det 406 firesifrede yrker:

| Hovedgruppe | 1 | 2 | 3 (med militære) | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| Firesifrede yrker | 30 | 92 | 79 | 26 | 38 | 13 | 61 | 39 | 28 |

**Historikk for de 406 yrkene** (gjennomsnitt, begge kjønn):

| | Antall |
|---|---|
| Tall alle år 2016–2025 | 353 |
| Tall fra et sted i perioden og i 2025 | 7 |
| Tall i 2016 og 2025, men hull mellom | 1 |
| Tall tidligere, men ikke i 2025 | 7 |
| Ingen tall noe år | 38 |

361 yrker har tall i 2025. Alle 361 har også median og kvartiler. 302 har tall for både kvinner og menn, 53 for bare ett kjønn, og 6 bare for begge kjønn samlet. Yrkene med tall i 2025 dekker 3 067 350 av 3 080 913 jobber, 99,6 prosent `[T]`.

**Størrelsene er svært ulike.** 264 yrker har minst 1 000 jobber, 129 minst 5 000, 37 minst 20 000. Det største er butikkmedarbeidere med 187 647, deretter barnehage- og skolefritidsassistenter (118 927) og helsefagarbeidere (116 127). Det minste med tall har 108 jobber (9623 Måleravlesere mv.). **Konsekvens for velgeren:** listen sorteres etter antall jobber eller grupperes etter hovedgruppe, ikke alfabetisk. Antall jobber vises ved hvert yrke, så leseren ser hvor tynt et snitt er.

**Kjønn.** 26 av 314 yrker med kjønnstall har minst 80 prosent kvinner, 75 har minst 80 prosent menn `[T]`. Kjønnsforskjellen per yrke kan bare vises for de 302 yrkene der begge kjønn har tall. For resten skal velgeren si at tallet for det ene kjønnet er skjult.

**Navnene er statistikkbankens.** «Høyere saksbehandlere i offentlig og privat virksomhet», «Andre pleiemedarbeidere», «Barnehage- og skolefritidsassistenter mv.» er ikke ordene folk søker på. Synonymsøk er valgt bort. Velgeren må derfor ha søk på deler av ord og gruppering etter hovedgruppe (hull 4).

**Desiler (13860).** Ti desiler og persentil 91–100 for alle næringer og per kjønn. Desil 10 og persentil 100 har ingen øvre grense og står med `:` (60 celler). Ellers ingen tomme celler.

**Hovedtall (11419).** Ingen tomme celler i utvalget. Delene av månedslønna finnes for alle sektorer, kjønn og heltid/deltid.

## 3. Metoder som er testet

| Metode | Resultat |
|---|---|
| Vekst per yrke regnet fra kroner | Treffer alle de 20 publiserte ratene i `[K3]` på første desimal (K4). Det finnes ingen publiserte rater per yrke i statistikkbanken, så dette er eneste vei. Avrunding til 10 kr gir høyst ±0,02 prosentpoeng `[T]`. |
| Vektet snitt av yrkene gjenskaper totalen | Med heltidsekvivalenter som vekt: 62 085 mot publisert 62 070 i 2025, 43 651 mot 43 640 i 2016. Med jobber som vekt: 59 444, altså feil vekt (K3). Avviket på 15 kr skyldes de undertrykte yrkene. |
| Hovedgruppe fra firesifrede yrker | Gruppe 2 gir 69 652 mot publisert 69 650 `[T]`. |
| Månedslønn = avtalt + tillegg + bonus | Stemmer innen 10 kr for alle 8 640 kombinasjoner av sektor, kjønn, arbeidstid og år (K5). Regnestykket i konseptgrafikken holder. |
| Median = grense for desil 5 | Stemmer for alle tre kjønnsvalg og alle år 2016–2025 (K6). |
| «Minst 6 av 10 under gjennomsnittet» | Grensen for desil 6 ligger under gjennomsnittet og grensen for desil 7 over, hvert år 2016–2025 (K8). Påstanden i toppgrafikken holder for hele perioden. |

## 4. Kontroller

| # | Kontroll | Resultat |
|---|---|---|
| K1 | Nøkkeltall i 11418 mot statistikksiden: 62 070, 55 800, handels- og skipsmeglere 172 630 og 771 jobber | OK |
| K2 | Jobber menn + kvinner = begge kjønn, alle yrker og år | OK, 0 avvik |
| K3 | Vektet snitt av yrkene ≈ publisert total (2016 og 2025) | OK, innen 0,03 prosent |
| K4 | Vekst fra kroner = publisert rate for 20 yrker | OK |
| K5 | Månedslønn = avtalt + tillegg + bonus | OK, største avvik 10 kr |
| K6 | Median i 11419 = grense desil 5 i 13860 | OK, 30 av 30 |
| K7 | 11419 og 11418 gir samme gjennomsnitt og median | **Ett kjent avvik:** menn 2023, 59 460 og 52 290 i 11419, 59 450 og 52 280 i 11418 (hull 2) |
| K8 | Gjennomsnittet mellom grensene for desil 6 og 7, alle år | OK |
| K9 | Utbetalt årslønn: publisert endring ≈ regnet fra kroner | OK, alle sektorer 2017–2025 |
| K10 | Påløpt årslønn 2025 = 746 700, +4,9, reallønn +1,8 | OK |

## 5. Datamengde og strategi

| Datasett | Celler | Råfil | Innbakt |
|---|---|---|---|
| `yrker` | 104 760 | 780 kB | 417 koder (firesifret, hovedgrupper, total): 75 060 celler, om lag 430 kB som kompakt tabell |
| `hovedtall` | 8 640 | 53 kB | Delmengde etter seksjon |
| `desiler` | 1 200 | 10 kB | Alt |
| `arslonn_utbetalt` | 88 | 2 kB | Alt |
| `arslonn_palopt` | 168 | 3 kB | 2016–2025, eventuelt hele serien fra 1970 |

Alle spørringer er langt under API-grensen på 800 000 celler. **Strategi:** alt bakes inn i `index.html`. Yrkene er 85 prosent av datamengden. Om siden blir for tung, kan tre- og tosifrede koder droppes (gjort allerede) og år 2017–2023 hentes bare for gjennomsnitt `[T]`. Valgt av Thomas 15.10.2026: nivå og spredning, 2016–2025.

## 6. Hull og hindre

1. **Tilkoblingen tåler ikke store json-stat2-svar.** Hele yrkestabellen som json-stat2 brøt forbindelsen. Rådataene er hentet som CSV og bygd om til json-stat2 med etiketter fra metadata. Små svar ble hentet fra øktloggen, ikke skrevet av. `hent_data.py` er skrevet for API-et, men ikke kjørt.
2. **11418 og 11419 avviker for menn i 2023** med 10 kr i gjennomsnitt og median (K7). 11418 er oppdatert 28.08.2026, 11419 05.02.2026. Trolig revisjon i august. Spørsmål til fag: hva ble endret, og skal 11419 oppdateres?
3. **Påløpt årslønn i 14858 er oppdatert 20.08.2026.** Fortsatt uavklart hvem som eier tabellen og hvorfor 5,0 ble 4,9 (spørsmål 2 og 5 i innsiktsnotatet).
4. **Uten synonymsøk må yrkesnavnene fungere som de er.** «Lærer» finner ikke «Grunnskolelærere» med eksakt søk. Søket må matche deler av ord, og velgeren bør grupperes etter hovedgruppe. Bør testes på noen vanlige søk i steg 4.
5. **Yrker vektes likt i prikkdiagrammet** (fra steg 2, T5). Antall jobber per yrke finnes i dataene og kan brukes til å skalere punktene, men det er ikke valgt.
6. **Sektor og sammensetning per yrke er valgt bort.** For yrker som finnes i flere sektorer (sykepleiere i kommune, stat og privat) skjuler snittet store forskjeller. Bør nevnes i lesehjelpen ved yrket.
7. **Ingen publiserte rater per yrke.** Veksten regnes fra kroner (K4). Det må stå i prototypen at raten er regnet av oss.
8. **Militære yrker ligger i hovedgruppe 3.** Velgeren må vise dem under «Høyskoleyrker», slik statistikkbanken gjør, eller skille dem ut. Eget valg i steg 4.

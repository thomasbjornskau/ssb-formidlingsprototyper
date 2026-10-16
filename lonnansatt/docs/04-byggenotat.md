Steg 4 i formidlingsprototype for lonnansatt · versjon 0.1 · 15.10.2026 · Status: utkast

# Byggenotat: Lønn (lonnansatt)

Bygger på `01-innsikt.md` (godkjent), toppgrafikk A og konseptgrafikken fra steg 2 (godkjent) og kildekartet fra steg 3. Yrket styrer prototypen. Velgeren viser nivå og spredning 2016–2025, uten sektor, sammensetning eller synonymsøk (valgt 15.10.2026).

## Hva er bygget

| Seksjon | Svarer på | Innhold |
|---|---|---|
| Hode | 3 | Ingress generert fra tallene, søk etter yrke med forslagsliste, «Se alle yrker» og fem eksempler |
| Kort for valgt yrke | 3, 4 | Snitt og median, midterste halvdel (kvartiler), antall jobber, kvinner og menn, endring fra året før, plassering i fordelingen, linje 2016–2025 mot alle jobber, tabell |
| Slik leser du lønnsstatistikken | 1, 2, 3, 5 | Fire punkter mot H1, H2, H3 og H4, og konseptgrafikken i `<details>` (bred og smal) |
| Toppgrafikk | 2 | «6 av 10», desilene mot gjennomsnitt og median, fire nøkkeltall |
| Hva er månedslønn? | 1 | Avtalt lønn, tillegg og bonus for alle, menn og kvinner. Jobber mot heltidsekvivalenter, heltid og deltid |
| Hva tjener de fleste? | 2 | Gjennomsnitt og median 2016–2025. Lønnsvekst per desil |
| Hva tjener et yrke? | 3 | Prikkdiagram med 361 yrker (variant B), klikkbart. De 15 største yrkene, klikkbare med tastatur |
| Kvinner og menn | 4 | Fire mål for 2025. Tre mål 2016–2025 |
| Hvor mye steg lønna? | 5 | Månedslønn og utbetalt årslønn etter sektor (variant C). Fire vekstmål 2017–2025 |
| Bunntekst | – | Om tallene, egne beregninger, kilder og hentedato |

Valget ligger i adressen (`#yrke=2223`) og følger tilbake-knappen. Hovedgruppene kan også velges. Siden er 783 kB, av dette er rundt 300 kB data.

## Slik vises hull og spesialtilfeller

- **Yrke uten tall noe år** (38 yrker, for eksempel 2356 Andre IKT-lærere): kortet sier «Tallet er skjult» og forklarer undertrykkingen. Hovedgruppens snitt vises.
- **Yrke uten jobber** (status `.` alle år, 4 yrker, for eksempel 6114): «Ingen jobber».
- **Yrke med tall tidligere, men ikke i 2025** (7 yrker, for eksempel 5242 Demonstrasjonsselgere): siste år med tall vises, med varsel. Yrket er ikke med i prikkdiagrammet eller i rekkefølgen.
- **Kjønn skjult**: kortet sier hvilket kjønn som mangler. Kjønnsandelen vises bare når begge har tall.
- **Få jobber**: under 1 000 jobber gir en setning om at snittet er usikkert.
- **Tabellen i kortet** viser `:` for skjult og `.` for ingen jobber, med forklaring under.
- **Søk uten treff** gir en lenke til hele lista og et hint om å søke på en del av ordet.

## Kontroller i byggeskriptet

`scripts/lag_data.py` stopper bygget med «Kontroll feilet» hvis en kontroll ikke går opp.

| # | Kontroll | Største faktiske avvik | Toleranse |
|---|---|---|---|
| K2 | Jobber menn + kvinner = begge kjønn, alle yrker og år (4 595 kombinasjoner) | 0 | 0 |
| K3 | Snitt av yrkene vektet med heltidsekvivalenter ≈ total | 0,05 prosent | 0,1 prosent |
| K4 | Vekst fra kroner = publisert for 20 yrker | 0 | 0 (én desimal) |
| K5 | Månedslønn = avtalt + tillegg + bonus | 10 kr | 20 kr |
| K6 | Median = grense desil 5 | 0 | 0 |
| K7 | 11419 = 11418 for alle yrker, utenom kjent avvik | 10 kr (menn 2023, kjent) | 0 for nye avvik |
| K8 | Gjennomsnittet mellom grensene for desil 6 og 7, alle år | – | – |
| K9 | Utbetalt årslønn: publisert endring ≈ regnet | 0,049 prosentpoeng | 0,1 |
| K10 | Påløpt årslønn 2025: 746 700 kr, +4,9, reallønn +1,8 | 0 | 0 |
| K11 | Vekst i månedslønn fra kroner = publisert, fire sektorer | 0 | 0 (én desimal) |

**Negativ test:** en kopi av `hovedtall.json` med 62 070 endret til 62 170 stoppet bygget på K5. Originalen er urørt.

**Bygget to ganger** gir identisk `index.html` (sha1 410907fd…).

## Test

Playwright i 1280 og 390 px: ingen feil i konsollen, `scrollWidth` lik bredden også etter sju kort åpnet etter hverandre. Søk på «sykepleier», «lærer», «lege», «snekker» og «xyzq». Kort for 2223, 3324, 5242, 2356, 6114, hovedgruppe 2 og 5223. «Se alle yrker» viser 406. Tastatur: piltast og Enter i søket, Enter på en stolpe i «De 15 største».

Rettet etter første test: hovedgruppe 3 manglet for høyskoleyrkene (330 av 406 i lista), siden ble 415 px bred på mobil fordi hovedrutenettet manglet minstebredde, sektorene kom i feil rekkefølge fordi JavaScript sorterer tallaktige nøkler først, og etiketter overlappet i toppgrafikken og prikkdiagrammet på mobil.

## Nye valg til kvalitetssikring

| # | Valg | Grunnlag |
|---|---|---|
| B1 | Toppgrafikken bruker «Minst 6 av 10», regnet som antall desiler med øvre grense under gjennomsnittet | K8, alle år. Avhenger av spørsmål 3 til fag |
| B2 | Vekst per yrke og per desil regnes av oss fra kroner, merket i kortet og bunnteksten | Ingen publiserte rater i statistikkbanken. K4 viser at metoden treffer |
| B3 | Kortet plasserer yrkets snitt i en desil av alle jobber | Vår sammenstilling av to tabeller. Et snitt er ikke en enkeltlønn, så setningen sier «snittet i yrket ligger i desil …» |
| B4 | Kvinners lønn som andel av menns, fire mål, også «bare heltidsansatte» | Regnet av oss fra 11419. Andelene for snitt, median og avtalt stemmer med artikkelen `[K4]` |
| B5 | Veksten i månedslønn i tidsserien er regnet fra gjennomsnittet. Årslønn og reallønn er publiserte tall | 2025 stemmer med publisert 4,5 (K11). Tidligere år er ikke sjekket mot publiserte rater |
| B6 | «Lønnsoppgjørene bruker påløpt årslønn» | TBU viser til SSBs foreløpige påløpte årslønn `[K12]`. Formuleringen er vår |
| B7 | Setningen om konflikten i staten 2024 og etterbetalingen i 2025 | `[K3]` forklarer statens månedslønn med dette. At det løfter utbetalt årslønn, er vår tolkning |
| B8 | Søket rangerer navn eksakt, starter med, ord starter med og inneholder, og deretter etter antall jobber. Ingen synonymer | Valgt av Thomas. «lærer» gir Grunnskolelærere som femte forslag |
| B9 | Linjediagrammene for kroner har avkortet y-akse | Utviklingen er poenget. Tillatt i diagramstandarden for linjediagram |
| B10 | Hovedgruppe 3 vises som «Høyskole- og militære yrker», slik statistikkbanken kaller den | Løser hull 8 i kildekartet |
| B11 | Fire faste yrker merket i prikkdiagrammet når ingen yrke er valgt. Valgt yrke erstatter dem | Fra variant B i steg 2 |
| B12 | Under 1 000 jobber gir merknad om usikkert snitt | Eget valg. SSB undertrykker først under 100 |

## Kjente svakheter

1. **Punktene i prikkdiagrammet kan ikke velges med tastatur.** 361 punkter i tabulatorrekkefølgen ville gjort siden tung å bruke. Søket, lista og «De 15 største» gir samme valg med tastatur.
2. **Yrker vektes likt i prikkdiagrammet.** Det står i noten. Fag bør godta det (T5 i steg 2).
3. **Synonymsøk mangler.** «Lærer» gir grunnskolelærerne som femte forslag, og vanlige ord som «doktor» eller «snekker» treffer bare der ordet står i SSBs navn.
4. **Sektor per yrke vises ikke.** Kortet sier at snittet gjelder alle sektorer samlet.
5. **Rådataene er rekonstruert**, og `hent_data.py` er ikke kjørt mot API-et.
6. **Det kjente avviket i K7** må fjernes fra koden hvis SSB oppdaterer 11419.

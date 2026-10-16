Steg 5 i formidlingsprototype for lonnansatt · versjon 1.0 · 16.10.2026 · Status: til faglig kontroll

# Kvalitetssikring: Lønn (lonnansatt)

Denne listen erstatter de tidligere listene i `01-innsikt.md` (spørsmål og hull), `02-kvalitetssikring.md`, `03-kildekart.md` (hull og hindre) og `04-byggenotat.md` (nye valg). Tidligere nummer står i kolonnen «Grunnlag», slik at sporet kan følges.

**Prototypen:** https://thomasbjornskau.github.io/ssb-formidlingsprototyper/lonnansatt/index.html (versjon 0.1)

Tallene i prototypen er hentet fra statistikkbanken og kontrollert ved hvert bygg (ti sum- og metodekontroller, se `04-byggenotat.md`). Det som skal kontrolleres her, er tolkninger, egne beregninger, avgrensninger og formuleringer. «Om statistikken» er lest i versjonen som ble oppdatert 30.09.2026.

## A. Må avklares

Det som kan være feil, eller som gir et misvisende inntrykk hvis det er feil.

| # | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 1 | «Minst 6 av 10 har lavere månedslønn enn gjennomsnittet.» Regnet som antall desiler der øvre grense ligger under gjennomsnittet: grensen for desil 6 er 60 310 kr, gjennomsnittet 62 070 kr | Toppgrafikken, lesehjelpen | Tabell 13860 og 11419. Gjelder alle år 2016–2025 (kontroll K8). Steg 1 spørsmål 3, steg 2 T1, steg 4 B1 | Er avledningen forsvarlig? Den gjelder heltidsekvivalenter, ikke personer eller jobber |
| 2 | Lønnsvekst per yrke og per desil er regnet av oss fra kronebeløpene, som er avrundet til 10 kr | Kortet for hvert yrke, «Hva tjener de fleste?» | Treffer alle 20 publiserte yrkesrater i «Høyest lønnsvekst i toppen» på første desimal (K4). Desil 1 og 10 gir 4,1 og 5,1 som i artikkelen. Steg 3 hull 7, steg 4 B2 | Er det greit å vise slike rater, merket som egne beregninger? |
| 3 | Fire mål for lønnsveksten side om side: månedslønn (4,5), utbetalt årslønn (5,2), påløpt årslønn (4,9) og reallønn (1,8). Teksten sier at TBU bruker påløpt årslønn, og at påløpt årslønn 2025 først ble publisert som 5,0 | Lesehjelpen, «Hvor mye steg lønna?», konseptgrafikken | Tabell 11419, 11536, 14858 og TBUs pressemelding 13.02.2026. Steg 1 spørsmål 2, steg 2 G9 og T9, steg 3 hull 3, steg 4 B5 og B6 | Er framstillingen riktig? Hvem eier 14858, lønnsstatistikken eller nasjonalregnskapet? Hvorfor ble 5,0 til 4,9, og er det riktig å si det slik? |
| 4 | «Konflikten i staten i 2024 forsinket lønnsoppgjøret der, og noen fikk to oppgjør i 2025. Utbetalt årslønn fører etterbetalinger i året de blir utbetalt, og det løfter den i staten i 2025.» Staten: 5,0 prosent i månedslønn, 6,3 i utbetalt årslønn | «Hvor mye steg lønna?» | Første del er fra «Høyest lønnsvekst i toppen». Andre del er vår tolkning ut fra definisjonen av utbetalt årslønn. Steg 4 B7 | Er forklaringen av forskjellen i staten riktig? |
| 5 | Kvinners lønn som andel av menns, med fire mål: gjennomsnitt (87,9), median (93,4), avtalt månedslønn (90,2) og bare heltidsansatte (89,8). Teksten sier at statistikken ikke kan svare på om kvinner og menn får ulik lønn for samme arbeid | «Hvor stor er forskjellen …», kortet for hvert yrke | Regnet av oss fra 11419. Tallene stemmer med «Lønnsforskjeller mellom kvinner og menn». Steg 1 H6–H7, steg 4 B4 | Er utvalget av mål og formuleringene forsvarlige? |
| 6 | Yrkesvelgeren viser snittet for alle sektorer samlet, ett punkt per yrke i prikkdiagrammet uansett størrelse, og en merknad om usikkert snitt når yrket har under 1 000 jobber | Søket, kortet, «Hva tjener et yrke?» | Tabell 11418. Valgt bort sektor per yrke (15.10.2026). Steg 1 spørsmål 4, steg 2 T5, steg 3 hull 5–6, steg 4 B12 | Er det forsvarlig å vise yrkene slik? Bør grensen på 1 000 jobber endres eller fjernes? |
| 7 | 11418 og 11419 gir ulikt gjennomsnitt og median for menn i 2023, med 10 kr. 11418 ble oppdatert 28.08.2026, 11419 05.02.2026. 14858 ble oppdatert 20.08.2026 | Kildelinjene. Prototypen bruker 11418 for yrker og 11419 for totalen | Kontroll K7. Steg 1 spørsmål 5–6, steg 3 hull 2 | Hva ble endret i august? Skal 11419 oppdateres? |

## B. Bør leses

Formuleringer, kortnavn, tolkninger og egne valg.

| # | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 8 | Kortet plasserer snittet i et yrke i en desil av alle jobber: «snittet i yrket ligger i desil 6, under gjennomsnittet for alle» | Kortet for hvert yrke | Vår sammenstilling av 11418 og 13860. Steg 4 B3 | Om sammenstillingen er forsvarlig. Et snitt er ikke en enkeltlønn |
| 9 | «Grupper med under 100 jobber vises ikke.» Forenklet fra «færre enn 100 arbeidsforhold uten imputert lønn». Kortet for skjulte yrker nevner også dominerende foretak | Konseptgrafikken, kortet, bunnteksten | «Om statistikken». Steg 2 G8 | Om forenklingen er akseptabel i konseptgrafikken |
| 10 | Konseptgrafikken: a-meldingen har «lønn, stillingsprosent og yrke for hver jobb», «Fulltelling, ikke utvalg. Alle jobber med lønn i a-meldingen er med» og fire trinn uten eget trinn for kontroll og imputering | Konseptgrafikken | «Om statistikken». Steg 2 G1, G2, G11 | Om forenklingene skjuler noe vesentlig. Yrkeskode var frivillig for frilansere fram til 2019 |
| 11 | «Ikke med i månedslønna»: overtid, naturalytelser og forsikringer, feriepenger og sluttvederlag, styrehonorar og honorarer for utvalg, skatt, selvstendig næringsdrivende. Fungeringstillegg er utelatt for plassens skyld | Konseptgrafikken | «Om statistikken». Steg 2 G10 | Om lista er riktig og dekkende |
| 12 | Toppgrafikken farger desil 1–6 grønt som «hele tidelen under gjennomsnittet», og gjennomsnitt og median er mørke stiplede linjer | Toppgrafikken | Eget valg. Steg 2 T2–T3 | Om fargekodingen kan leses som en vurdering |
| 13 | Fire faste yrker merket i prikkdiagrammet (butikkmedarbeidere, sykepleiere, administrerende direktører, handels- og skipsmeglere), og «om lag 34 000 til 173 000 kroner» i overskriften | «Hva tjener et yrke?» | Valgt etter størrelse og ytterpunkter. Begge ytterpunktene har under 1 000 jobber. Steg 2 T6–T7, steg 4 B11 | Om utvalget kan leses som en rangering, og om ytterpunktene bør vises |
| 14 | Hovedgruppe 3 vises som «Høyskole- og militære yrker», og de militære gradene (offiserer, befal, menige) ligger der | Søket, lista over alle yrker | Statistikkbankens navn på koden `3_01-03`. Steg 2 T4, steg 4 B10 | Ingen, til orientering |
| 15 | Søket bruker bare SSBs yrkesnavn, uten synonymer. «Lærer» gir grunnskolelærerne som femte forslag | Søket | Valgt 15.10.2026. Steg 4 B8 | Om vanlige søkeord bør legges til |
| 16 | Veksten i månedslønn per år i tidsserien er regnet fra gjennomsnittet. Bare 2025 er sjekket mot publisert rate | «Hvor mye steg lønna?» | K11. Steg 4 B5 | Om tidligere år bør hentes som publiserte rater |
| 17 | TBUs tall per forhandlingsområde er ikke med | «Hvor mye steg lønna?» | Forhandlingsområdene svarer ikke til SSBs sektorer. Steg 2 T10 | Om de bør nevnes |
| 18 | «Gjennomsnittet dras opp av de høyeste lønningene, der menn er flest, og menn får oftere bonus og tillegg» | «Hvor stor er forskjellen …», ingress | «Lønnsforskjeller mellom kvinner og menn» og «Høyest lønnsvekst i toppen». Rettet i steg 5 | Formuleringen |
| 19 | Linjediagrammene i kroner har avkortet y-akse | «Hva tjener de fleste?», kortet | Utviklingen er poenget. Steg 4 B9 | Ingen, til orientering |

## C. Spørsmål

| # | Spørsmål | Grunnlag |
|---|---|---|
| 20 | Stemmer hypotesene om misforståelser (H1–H10 i `01-innsikt.md`)? Hvilke møter dere oftest, og mangler noen? | Steg 1, del 4 |
| 21 | Bør kortet vise median ved siden av snittet for hvert yrke, slik det gjør nå, eller er snittet nok? | Steg 1 spørsmål 4 |
| 22 | Er 2016 riktig startår for tidsseriene, når 2015 er per september og etter gammel arbeidstidsmetode? | «Om statistikken», steg 3 |
| 23 | Er dere rett mottaker, eller bør andre se på deler av prototypen, for eksempel nasjonalregnskapet for påløpt årslønn (punkt 3)? | Fagkontakt ikke bekreftet |

## Avklart underveis

| # | Hva | Hvordan |
|---|---|---|
| 24 | «Om statistikken» kunne leses i sin helhet | Bekreftet 15.10.2026. Definisjonene bygger på versjonen oppdatert 30.09.2026, ikke på en arkivversjon |
| 25 | Hvor de militære yrkene hører hjemme | Statistikkbanken kaller hovedgruppe 3 «Høyskole- og militære yrker». Steg 3 hull 8 |
| 26 | At regnestykket i konseptgrafikken holder | Månedslønn = avtalt + tillegg + bonus innen 10 kr for alle 8 640 kombinasjoner (K5). Steg 2 G5 |
| 27 | Seks formuleringer rettet ved gjennomgangen i steg 5 | «Halvparten av jobbene hadde under 55 800» ble «regnet om til heltid tjente halvparten under 55 800», fordi desilene er heltidsekvivalenter. «Gjennomsnitt for alle som har jobben» ble «for alle jobbene i yrket». «Ingen egen undersøkelse og intet utvalg. Alle jobber med lønn er med» ble «Fulltelling, ikke utvalg. Alle jobber med lønn i a-meldingen er med», fordi frilansere og sene meldinger delvis faller utenfor. «Lønnsoppgjørene bruker påløpt årslønn» ble «TBU bruker påløpt årslønn», som er det kilden sier. Forklaringen av kjønnsforskjellen i snitt og median og forklaringen av statens årslønn er skrevet om etter kildene |
| 28 | Feil rettet i steg 4 | 76 yrker manglet hovedgruppe i lista, siden ble for bred på mobil, sektorene kom i feil rekkefølge, og etiketter overlappet på mobil |
| 29 | Teknisk, ikke fagets ansvar: rådataene er rekonstruert fra SSB-tilkoblingen, og `hent_data.py` er ikke kjørt mot API-et | Kjøres før neste versjon. Kontrollene stopper bygget hvis tallene ikke går opp. Steg 3 hull 1 |
| 30 | Teknisk: `felles/grafikk.py` finnes ikke i repoet | Erstattet av `scripts/grafikk_lonn.py`, som i muh. Bør bli felles fil. Steg 2 F1 |
| 31 | Teknisk: kontroll K7 har ett kjent avvik i koden | Må fjernes hvis SSB retter 11419 eller 11418 |
| 32 | Teknisk: punktene i prikkdiagrammet kan ikke velges med tastatur | Søket, lista og «De 15 største» gir samme valg. Steg 4, kjente svakheter 1 |

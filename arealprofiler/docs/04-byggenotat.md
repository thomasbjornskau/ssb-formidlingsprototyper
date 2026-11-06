Steg 4 i formidlingsprototype for arealprofiler · versjon 0.1 · 06.11.2026 · Status: utkast

# Byggenotat: Arealprofiler

**Merking.** `[T]` er vår tolkning eller vårt valg. Q-nummereringen fortsetter fra `02-kvalitetssikring.md`.

## 1. Hva som er bygget

Én side, `index.html` (1 060 kB, ingen eksterne kall). Kommunen er valget som styrer alt. Den ligger i adressen (`#kommune=3405`) og kan deles. Uten valg vises Lillehammer, merket som eksempelkommune.

| Seksjon | Svarer på | Innhold |
|---|---|---|
| Hode og søk | – | Søk på kommunenavn, også samiske navn og ti tidligere kommunenavn (`data/synonymer.json`). Liste over alle kommuner etter fylke |
| Kort for valgt kommune | 1 | Fylke, sentralitetsklasse, antall kommuner i klassen, hvor mange indikatorer som mangler og hvorfor |
| Slik leser du arealprofilen | H1, H2, H3, H5 | Fire punkter med tall for valgt kommune. Konseptgrafikken bak «Slik lages tallene» |
| Toppgrafikk (variant C) | 1 | Kommunens navn, setning om tetthet laget av tallene, fem indikatorer mot sentralitetsklassen, fire nøkkeltall |
| Hele profilen | 1 | Alle 35 indikatorer i seks grupper: prikk for kommunen, bånd for 10.–90. persentil, median, median for alle kommuner, liten tidsserie. Bryter mellom samme sentralitet og alle kommuner |
| Bygger vi tettere? | 2 | Andel nye boliger utenfor tettsted og i blokk for landet (egne beregninger) med kommunen. Avstand til sentrumssonen for alle og nye boliger, med median i klassen |
| Hva bygger vi ned? | 3 | Landstall fra 11776 mot jordvernmålet. Kommunens omdisponerte dyrka og dyrkbar jord. Nye bygg i strandsonen og tilgjengelig strandsone |
| Hva er satt av i planen? | 4 | Ledig areal til bolig i kommuneplanen, 2023 og 2024, mot medianen i klassen |
| Bygger vi i fareområder? | 5 | Nye bygninger i aktsomhets- og naturfareområder, 2024 og 2025 |
| Bunntekst | – | Om tallene, egne beregninger, kilder, hentedato |

Alle figurer har «Vis tallene» og kildelinje. Overskrifter, ingresser og noter er laget av tallene.

## 2. Hvordan hull i data vises

| Situasjon | Visning |
|---|---|
| Kommunen mangler tall | Teksten fra `lag_data.py` (`MANGLER`) står der tallet skulle stått: «Ingen tettsted», «Ikke kystkommune», «Ingen nye boliger», «Ingen registrert», «Ingen tall: null eller ikke rapportert» (B4) |
| Null som betyr ikke aktuelt | A3 = 0 vises som «Ingen tettsted», C6 = 0 som «Ingen sentrumssone». Prikken tegnes likevel på 0 |
| Ikke kystkommune | Strandsonekortet viser forklaring i stedet for tom figur |
| Ingen omdisponering | Jordkortet viser forklaring i stedet for tom figur |
| År som mangler i serien | B3 2020: «mangler» i stolpen. Linjer brytes ved hull |
| Klasse med få kommuner | Båndet tegnes bare når klassen har minst ti kommuner med tall. Klasse 1 (fem kommuner) vises som prikker |
| Bare ett år for kommunen | Den lille tidsserien viser «bare ett år» |

## 3. Kontroller i `lag_data.py`

| | Kontroll | Toleranse | Største faktiske avvik |
|---|---|---|---|
| K1 | 105 476 rader, 357 kommuner, 35 indikatorer | Eksakt | 0 |
| K3 | Alle kommuner har sentralitet (Klass 1417) og fylke (Klass 104) | Eksakt | 0 |
| K4 | Sum C3 mot 11776 dyrka jord, alle formål, 2020–2024 | 40 dekar | 32 dekar (2024, Lillestrøm og Time rettet 15.06.2026) |
| K4 | Sum C4 mot 11776 dyrkbar jord, alle formål, 2020–2024 | 15 dekar | 10 dekar |
| K5 | B8-klassene summerer til 90–102 prosent | 90–102 | 90,9 (Utsira 2024) og 101,5 |
| – | Alle synonymer viser til kommuner som finnes | Eksakt | 0 |

Negativ test: én verdi i en kopi av `kofola_land.json` endret med 500 dekar. Bygget stoppet med «Kontroll feilet: sum C3 2020 = 4760, tabell 11776 = 5239.9, avvik 480 > 40». Fila er satt tilbake.

Bygget er kjørt to ganger, og `index.html` ble identisk begge gangene.

## 4. Testet

Playwright i 1280 og 390 piksler bredde: ingen feil i konsollen, `scrollWidth` lik bredden for standardvisning, Oslo, Utsira, Haram, Karasjok og Trysil. Søk: «skedsmo» gir Lillestrøm (tidligere kommune), «Kautokeino» gir Guovdageaidnu - Kautokeino, «sandvika» gir Bærum (merket som sted), «xyzq» gir ingen treff med lenke til listen, «ås» gir Ås først. Enter velger første forslag.

## 5. Nye valg til kvalitetssikring

| | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| Q24 | Lillehammer som eksempelkommune når ingen er valgt | Eget valg `[T]` | Om siden heller skal starte uten kommune |
| Q25 | Setningen i toppgrafikken: «tettere enn de fleste» når over 60 prosent av klassen har lavere andel i tettsted, «mer spredt» under 40 prosent | Eget valg `[T]` | Om grensene og formuleringen er rimelige, og om A3 er riktig indikator for «tett» |
| Q26 | Gruppering av de 35 indikatorene i seks tema i «Hele profilen» | `data/indikatorer.json`, eget valg `[T]` | Om temaene og rekkefølgen passer planleggernes behov |
| Q27 | Korte navn på indikatorene, for eksempel «Andel husholdninger som leier» for A5 | Eget valg `[T]` | At kortnavnene ikke endrer betydningen |
| Q28 | Tekstene for manglende tall (`MANGLER` i `lag_data.py`) | Kildekartet, avsnitt 2 `[T]` | Særlig B4 og B10: betyr manglende tall null? |
| Q29 | Spredning vist som 10.–90. persentil, uvektet | Eget valg `[T]` | Som Q15 |
| Q30 | Landsmedian (median for alle kommuner) som referanse | Eget valg `[T]` | At det ikke leses som landstall |
| Q31 | Jordvernmålet tegnet som 2 000 dekar hvert år 2015–2025 | `[K7]` | Målet gjelder fra et bestemt år. Bør linjen bare vises fra da? |
| Q32 | Ti synonymer for tidligere kommunenavn, «Sandvika» merket som usikker | Eget valg `[T]` | Om listen bør utvides |
| Q33 | B8 vist som de tre største arealklassene, uten sammenligning | Eget valg `[T]` | Om B8 heller skal ha egen figur |

## 6. Kjente svakheter

1. **Ikke årets tall.** Prototypen bygger på datagrunnlaget for Arealprofiler 2025. Når 14478/14488 er publisert, må `lag_data.py` bygges om. Etikettene er annerledes der, og B9, B11 og B12 må få ny behandling.
2. **B9 i toppgrafikken og i planseksjonen** bygger på to år og en metode som er endret.
3. **Landstall for nye boliger** er egne beregninger, og A7 er avrundet til hele prosent.
4. **Fireårsperiodene** er ikke avklart (Q5).
5. **Mobiloppsettet** av den lille tidsserien er skjult under 640 piksler, så tidsutviklingen vises bare i seksjonene.
6. **Tastatur:** prikkene i stripene har bare `<title>` for mus. Verdiene finnes i «Vis tallene».
7. **Mouseover** finnes på linjer og stolper, ikke på stripene.

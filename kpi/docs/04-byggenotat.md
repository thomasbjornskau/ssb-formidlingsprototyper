# Byggenotat, steg 4 (kpi)

Versjon 0.1 av prototypen, 14.10.2026. Bygget fra `src/index.template.html` og `data/raw/` med `felles/bygg.py`.

## Hva er bygget

| Seksjon | Svarer på | Innhold |
|---|---|---|
| Søk og kort | 3 | Søkefelt øverst med forslag mens man skriver. Valget åpner et kort med tolvmånedersendring mot hele KPI, linje fra 2015, vekt og bidrag der det finnes, sti opp i hierarkiet og undergrupper. «Se alle grupper» viser hele treet. Valget ligger i adressen, for eksempel `#gruppe=04.5.1` |
| Slik leser du KPI | H1–H4 | Fire punkter om de vanligste misforståelsene, og konseptgrafikken bak «Slik lages tallene» |
| Toppgrafikk A | 1 | Tolvmånedersvekst i KPI og KPI-JAE fra 2015, med toppen markert. Fire nøkkeltall |
| Hva driver prisveksten? | 2 | Bidrag per hovedgruppe med vekt × endring ved siden av, og bidrag per måned fra 2017 som stablede søyler |
| Hva er med i KPI? | 3 | Vekter 2026 med 2015 som strek. Klikk åpner kortet |
| Hvorfor flere KPI-er? | 4 | Velg blant de åtte seriene, fra 2015 eller 1995. Liste med siste tall og forklaring |
| Pengeverdi | 5 | Beløp, måned og år fra 1920, regnet om til siste måned, med linje over tid |

## Slik håndterer søket hullene i tabellen

| Tilfelle | Eksempel | Visning |
|---|---|---|
| Indeks og tolvmånedersendring | Brød, diesel | Stort tall, linje mot hele KPI |
| Bare indeks fra 2026 | Nøttesmør | Indeksnivå, og når endringen kan regnes |
| Vekt, men ingen indeks | Restauranter og kaféer | «Ingen tall», med lenke til gruppen over |
| Ingen egen vekt | Alle under tredje nivå | Nærmeste gruppe med vekt, og hvorfor bidrag mangler |
| Søkeord som ikke er gruppenavn | strøm, cola, frisør | Treff via synonymlisten, merket «Funnet med søkeordet» |

## Kontroller i byggeskriptet

`scripts/lag_data.py` stopper bygget hvis ett av disse ikke stemmer:

- hovedgruppenes vekter summerer til 1 000 (±0,5) hvert år 2015–2026
- totalindeksen i 14700 er lik KPI i 14706 og den historiske serien i 14710, alle måneder fra 2015
- totalindeksen gjenskapes fra hovedgruppene med årets vekter, med avvik under 0,15 (største faktiske: 0,11)
- bidragene fra hovedgruppene summerer til publisert tolvmånedersvekst, med avvik under 0,2 prosentpoeng (største faktiske: 0,16, i mars 2017)
- alle koder i synonymlisten finnes i tabellen

En negativ test med en vekt endret med 5 promille stoppet bygget som ventet.

Avvikene skyldes at indeksene er avrundet til én desimal, og at publisert tolvmånedersvekst er avrundet. For september 2026 summerer bidragene til 3,43 mot publisert 3,4. Det står under figuren.

## Nye valg til kvalitetssikring

| | Valg | Begrunnelse |
|---|---|---|
| 11 | Synonymlisten, 109 søkeord, 12 merket usikre (blant annet barnehage og SFO til `13.3`, strømmetjeneste til `08.3` og `09.6`) | Folk søker ikke på SSBs gruppenavn |
| 12 | Varighetskoden vises som tekst: ikke-varig vare, halvvarig vare, varig vare, tjeneste | Tolkning av IV, HV, V og T |
| 13 | Bidrag regnes for alle grupper med vekt, også på andre og tredje nivå, med samme metode som for hovedgruppene | SSB publiserer ikke bidrag i statistikkbanken. Bør sjekkes mot SSBs egne tall |
| 14 | Merknad om strømstøtte og Norgespris på `04.5.1`, og forklaring av beregnet husleie på `04.2` og `04.2.1` | Formuleringene er våre |
| 15 | KPI-JA ligger 1,8 prosentpoeng over KPI. Teksten sier at avgiftsendringer har trukket KPI ned | Følger av definisjonen. Hvilke avgifter det gjelder, er ikke forklart |
| 16 | Kortnavn for hovedgruppene, for eksempel «Bolig og strøm» og «Mat og alkoholfri drikke» | Fulle navn står i kortet, verktøytips og tabeller |
| 17 | Bolig og strøm økte fra 25,3 til 31,2 prosent av vektene fra 2025 til 2026 | Nesten hele økningen er beregnet husleie (13,9 til 20,6 prosent). Vises som tall, årsaken er ikke forklart |
| 18 | Pengeverdi fra 1920 regnet fra indeks med én desimal | Avrundingen gir avvik på flere prosent for de eldste årene. Merket under figuren |

## Kjente svakheter

- Linjediagrammene kan ikke leses med tastatur. «Vis tallene» dekker det samme. Stolpene for bidrag og vekter er knapper og kan brukes med tastatur.
- Filen er om lag 1 MB fordi alle 336 grupper fra 2015, d3 og skrift er bakt inn.
- Søket finner bare det som står i gruppenavnene eller i synonymlisten. Skrivefeil gir ingen treff.
- Bidrag per måned starter i 2017, fordi metoden trenger desember to år tilbake.

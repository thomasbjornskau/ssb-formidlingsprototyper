Steg 2 i formidlingsprototype for lonnansatt · versjon 1.0 · 15.10.2026 · Status: godkjent av Thomas (toppgrafikk A valgt, B blir yrkesseksjonen med velger, konseptgrafikk godkjent)

# Kvalitetssikring: grafikk (lonnansatt)

Påstander og valg i konseptgrafikken og toppgrafikken som er tolkning, eget valg eller ikke bekreftet av en gjeldende kilde. Kildemerkene viser til `01-innsikt.md`. Listen samles i `05-kvalitetssikring.md`.

## Konseptgrafikken

| # | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| G1 | Alle som betaler lønn, sender a-melding hver måned med lønn, stillingsprosent og yrke for hver jobb. | `[K2]` | At yrke er dekkende: yrkeskode er ikke påkrevd for alle arbeidsforholdstyper, og frilansere rapporterte frivillig til 2019. |
| G2 | «Ingen egen undersøkelse og intet utvalg. Alle jobber med lønn er med.» | `[K2]` (fulltelling fra a-ordningen) | At formuleringen ikke overdriver. Frilansere og noen grupper fanges bare delvis opp, og sene a-meldinger kommer ikke med. |
| G3 | Jobbene som er aktive i uka med den 16. november og har fått lønn den måneden. | `[K2]` | Ingen. |
| G4 | 3 080 913 jobber med lønn, 2 418 216 heltidsekvivalenter. | `[K6]`, tabell 11419 | Ingen for tallene. Om «Regnet om til heltid» er et godt nok navn på heltidsekvivalenter. |
| G5 | Regnestykket 58 450 + 2 090 + 1 530 = 62 070 kr. | `[K6]`, tabell 11419 | Ingen. Delene summerer til det publiserte tallet. |
| G6 | Tillegg og bonus fordeles som snitt per måned fra januar til november. | `[K2]` | Ingen. |
| G7 | Yrkeskoden gjøres om til STYRK-08. Næring, sektor, kjønn, alder og utdanning hentes fra registre. | `[K2]` | Ingen. |
| G8 | «Grupper med under 100 jobber vises ikke.» | `[K2]`: færre enn 100 arbeidsforhold *uten imputert lønn* | Forenkling. At den er akseptabel, eller om grafikken skal si «uten imputert lønn». Dominerende foretak er ikke nevnt. |
| G9 | Veksten i påløpt årslønn 2025 ble først publisert som 5,0 prosent og er nå 4,9. | `[K3][K10]` | Når og hvorfor endringen kom. Tabell 14858 er oppdatert 20.08.2026, ikke i mars. |
| G10 | «Ikke med i månedslønna»: overtid, naturalytelser og forsikringer, feriepenger og sluttvederlag, styrehonorar og honorarer for utvalg, skatt, selvstendig næringsdrivende. | `[K2]` | Ingen. Fungeringstillegg er utelatt for plassens skyld. |
| G11 | Fire trinn. Kontroll, editering og imputering er ikke eget trinn. | Eget valg | At fag ikke vil ha imputeringen fram, siden den påvirker undertrykkingen. |

## Toppgrafikken

| # | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| T1 | A: «Minst 6 av 10 har lavere månedslønn enn gjennomsnittet.» | `[K8][T]`: øvre grense for desil 6 er 60 310 kr, under gjennomsnittet på 62 070 | At avledningen er godtatt. Gjelder heltidsekvivalenter, ikke personer eller jobber. |
| T2 | A: Desil 1–6 er grønne fordi hele tidelen ligger under gjennomsnittet. | `[K8][T]` | Ingen for tallene. At fargekodingen ikke leses som en vurdering. |
| T3 | A: Gjennomsnitt og median som stiplede referanselinjer. | Eget valg. Diagramstandarden sier grå linje, vi bruker mørk stiplet for å skille dem fra de grå stolpene. | Avvik fra standarden, nevnes her. |
| T4 | B: 406 yrker, 361 med tall, 45 uten. | `[K7][T]`, talt fra 11418 | Ingen for tellingen. «Uoppgitt» er holdt utenfor. Militære grader (offiserer, befal, menige) er med. |
| T5 | B: Ett punkt per yrke, gruppert i intervaller på 2 500 kr. | Eget valg | At fag godtar at yrker vektes likt. Et yrke med 771 jobber teller like mye som ett med 187 647. Står i grafikken. |
| T6 | B: Utvalgte yrker: butikkmedarbeidere, sykepleiere, administrerende direktører, handels- og skipsmeglere. | Eget valg, `[K7]` | At utvalget ikke leses som en rangering. Valgt etter størrelse og ytterpunkter. |
| T7 | B: «Om lag 34 000 til 173 000 kroner.» | `[K7]`: 33 500 (hjelpearbeidere i husdyrproduksjon) og 172 630 | At ytterpunktene er stabile. Begge yrkene har under 1 000 jobber. |
| T8 | C: Vekst i månedslønn etter sektor: 4,5, 5,0, 4,7, 3,4. Utbetalt årslønn: 5,2, 6,3, 5,1, 4,4. | `[K1][K9]`, publiserte rater | Ingen for tallene. |
| T9 | C: «Årslønna tar med hele året og etterbetalinger.» Påløpt årslønn fører etterbetalinger i året de er opptjent. | `[K2]` | At forklaringen er dekkende. |
| T10 | C: TBUs tall er ikke med. | Eget valg: forhandlingsområdene svarer ikke til SSBs sektorer | Om fag mener TBUs tall bør nevnes i lesehjelpen. |

## Felles

| # | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| F1 | Grafikken er laget med `scripts/grafikk_lonn.py`, en kopi av muhs primitiver, fordi `felles/grafikk.py` ikke finnes i repoet. | Eget valg | Bør bli felles fil før neste prototype. |
| F2 | Tallene er hentet gjennom SSB-tilkoblingen 15.10.2026 og ligger i `data/grafikk-utkast.json`. | — | Erstattes av `data/raw/` i steg 3. |

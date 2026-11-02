`Steg 2 i formidlingsprototype for arblonn · versjon 1.0 · 30.10.2026 · Status: godkjent av Thomas`

> Kvalitetssikringspunktene er samlet i `05-kvalitetssikring.md`, som erstatter listen her.

> **Godkjent 30.10.2026.** Toppgrafikk C (månedsendring med foreløpige og endelige sesongjusterte tall) er valgt, og konseptgrafikken er godkjent. A (jobber og mennesker) og B (hvilken lønn) er kandidater til egne seksjoner. C skal kunne vise valgt næring. Forutsetning for C: G13 må bekreftes i steg 3.

# Kvalitetssikring etter steg 2: grafikk

Påstander og valg i konseptgrafikken og toppgrafikken som er tolkning, eget valg eller ikke uttrykkelig bekreftet. Samles i `05-kvalitetssikring.md` før fagkontrollen.

| # | Påstand eller valg | Hvor | Grunnlag | Må sjekkes |
|---|---|---|---|---|
| G1 | «Hver måned sender alle arbeidsgivere a-melding med arbeidsforhold, lønn og stillingsprosent.» | Konsept 1 | K1 (lest gjennom oppsummering) | At stillingsprosent er fast felt i a-meldingen for alle arbeidsforhold. |
| G2 | «En jobb telles når det er lønn eller ytelse i uka med den 16.» | Konsept 2 | K1: lønn er hovedkriteriet, men jobber med sykepenger, foreldrepenger og korte permitteringer er med. | Om «lønn eller ytelse» er en riktig forenkling. |
| G3 | «Sesongjobb uten lønn den uka faller ut.» | Konsept 2 | K1 nevner sesongarbeidere uten lønn i referanseuka. | Ingen, bare formulering. |
| G4 | «Hver person telles én gang, med én hovedjobb.» | Konsept 3 | K1, K3 | Hvordan hovedjobben velges (største stilling, høyest lønn?). Ikke nevnt i grafikken. |
| G5 | Kontantlønn regnes per jobb, avtalt månedslønn og månedslønn per heltidsekvivalent. | Konsept 4 | K1 | Ingen. |
| G6 | «Første tall kommer 3–4 uker etter måneden. Endelige tall en måned senere.» | Konsept 5 | K1 | Ingen. |
| G7 | «August 2026: endelig tall 67 276 jobber høyere.» Gjelder sesongjusterte tall. | Konsept 5, topp C | K6, tabell 13126 | Om forskjellen i ujusterte tall er like stor. Om forskjellen er typisk (den har ligget på 45 000–67 000 siden 2023M09) og hvorfor den har økt. |
| G8 | «Ikke med: småbeløp under fritaksgrensene i a-ordningen.» | Konsept, grå boks | K4 (2018) | At fritaksgrensene fortsatt gjelder. |
| G9 | Overskrift «3,2 millioner jobber» avrundet fra 3 166 971. «2,5 millioner månedsverk» fra 2 468 029. | Topp A | K6 | Ingen. Bevisst avrunding mot fasitlesning. |
| G10 | Heltidsekvivalenter vist som stolpe ved siden av jobber og personer, selv om enheten er en annen (månedsverk). | Topp A | Eget valg [T] | Om fag mener det blander enheter på en villedende måte. |
| G11 | «Halvparten ligger under 53 650 kroner.» Medianen er per heltidsekvivalent. | Topp B | K6 | Om median beregnes over jobber eller over heltidsekvivalenter. «Halvparten» kan leses som «halvparten av folk». |
| G12 | «Med bonus og uregelmessige tillegg blir snittet 63 700 kroner.» Overtid er ikke med. | Topp B | K1 | Om overtid bør nevnes eksplisitt i grafikken. |
| G13 | Foreløpig sesongjustert serie tegnet som den første versjonen for hver måned. | Topp C | K6 | Om foreløpige sesongjusterte tall i 13126 er låst slik de ble publisert, eller re-estimert. K1 sier at foreløpige tall ikke overskrives. |
| G14 | Avkortet y-akse (3,05–3,20 millioner) i C. | Topp C | Diagramstandard: lov i linjediagram når endringen er poenget | Ingen. Nevnes for fullstendighet. |
| G15 | «+24 800» avrundet fra +24 775. | Topp C | K2, K6 | Ingen. |

**Teknisk merknad.** Grafikken lages av `scripts/lag_grafikk.py` med primitivene i `scripts/grafikk_arblonn.py`. Kontrollrenderingen er gjort med DejaVu Sans, som er bredere enn Open Sans.

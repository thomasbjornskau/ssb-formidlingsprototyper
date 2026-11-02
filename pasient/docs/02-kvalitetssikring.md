`Steg 2 i formidlingsprototype for pasient · versjon 1.0 · 02.11.2026 · Status: godkjent av Thomas`

> **Godkjent 02.11.2026.** Toppgrafikk A (pasienter, kontakter, døgnopphold og oppholdsdøgn som indeks 2015 = 100) er valgt, og konseptgrafikken er godkjent. B (diagnosekapitler) og C (hva driver veksten) er kandidater til egne seksjoner. A skal kunne vise valgt diagnosekapittel. Forutsetning for C: G17–G19 må godtas av fag.

# Kvalitetssikring etter steg 2: grafikk

Påstander og valg i konseptgrafikken og toppgrafikken som er tolkning, eget valg eller ikke uttrykkelig bekreftet. Samles i `05-kvalitetssikring.md` før fagkontrollen. Kildemerkene viser til `01-innsikt.md`.

| # | Påstand eller valg | Hvor | Grunnlag | Må sjekkes |
|---|---|---|---|---|
| G1 | «Sykehus, private institusjoner med avtale og avtalespesialister rapporterer hver kontakt til Norsk pasientregister.» | Konsept 1 | K2 (aktørbegrepet, NPR som eneste kilde), lest gjennom oppsummering | At avtalespesialistenes data kommer gjennom NPR på samme måte (KUHR-data?). |
| G2 | «Kontakter uten gyldig fødsels- eller D-nummer faller ut.» Tallet 13 500 for 2025. | Konsept 2 | K2: «Om statistikken» sier at 13 500 somatiske kontakter manglet personnummer i 2025 | At disse 13 500 er de som faller ut, og at de er kontakter (ikke opphold eller personer). |
| G3 | «Hver person telles én gang, uansett hvor mange kontakter eller innleggelser.» | Konsept 3 | K2 | Ingen. |
| G4 | «Diagnosekapitlene: 5,16 mill.» Summen av 20 kapitler pluss «Annen», 2025. (Rettet 02.11.2026: sto først «21 kapitler».) | Konsept 4, topp B | K4, tabell 14824, egen sum | Om summering av unikt telte grupper er en god måte å vise dobbelttellingen på, eller om fag foretrekker et annet mål (f.eks. diagnoser per pasient). |
| G5 | «Pasienttall avrundes til nærmeste tall delelig med 3.» Vår omskriving av «base 3». | Konsept 5 | K2 | At «avrunding til base 3» betyr nærmeste multiplum av 3, og ikke tilfeldig avrunding. |
| G6 | «Ikke med: fastlege og kommunale tjenester · ventetid og kostnader.» | Konsept, grå boks | Vår avgrensning `[T]`. K2 nevner bare barn og unge i psykisk helsevern og TSB. | At listen ikke gir inntrykk av at SSB har sagt noe om disse. |
| G7 | Konseptgrafikken viser bare somatikk. Psykisk helsevern for voksne har ikke diagnoser i statbanken. | Konsept | K4 | Om psykisk helsevern skal ha egen markering i konseptgrafikken. |
| G8 | Aldersjusteringen er holdt utenfor konseptgrafikken. | Konsept | Eget valg til spørsmål 2 i innsiktsnotatet er besvart | Tas inn når fag har bekreftet standardbefolkningen. |
| G9 | Indeks 2015 = 100 for fire serier med ulike enheter (personer, kontakter, opphold, døgn). | Topp A | Diagramstandard: indeks i stedet for to y-akser | Ingen. Valget nevnes. |
| G10 | Avkortet y-akse (85–130) i indeksdiagrammet. | Topp A | Diagramstandard: lov i linjediagram når endringen er poenget | Ingen. |
| G11 | «Korona» markert ved 2020 som stiplet linje. Ikke et brudd i serien. | Topp A | K3 nevner fallet i 2020 og utsatte behandlinger | At stiplet linje ikke leses som brudd. Kan bli annotasjon uten linje. |
| G12 | «Like mange innleggelser som i 2015.» 897 840 og 901 848 døgnopphold. | Topp A | K4 | At døgnopphold er riktig mål på «innleggelser». |
| G13 | «793 000» avrundet fra 793 185. | Topp B | K4 | Ingen. Bevisst avrunding. |
| G14 | «… var til kontroll, oppfølging eller annen kontakt (Z-kapitlet).» Vår beskrivelse av Z00–Z99. | Topp B | ICD-10-kapittelnavn: «Faktorer som har betydning for helsetilstand og kontakt med helsetjenesten» | At beskrivelsen er dekkende. Z-kapitlet omfatter også bl.a. screening og risikofaktorer. |
| G15 | Korte kapittelnavn («Øyet», «Symptomer og funn», «Skader og forgiftninger»). | Topp B | Eget valg `[T]` | Bryter regelen om etablerte navn. Fag velger: korte navn i figuren og fullt navn i velgeren, eller fullt navn overalt. |
| G16 | Uthevet stolpe for valgt kapittel, grå for resten. | Topp B | Diagramstandard: uthev én mot grå | Ingen. |
| G17 | Middelfolkemengde regnet som snitt av folkemengden 1. januar i året og året etter, med samme aldersgrupper. | Topp C | K2 sier middelfolkemengde. Totalraten treffer 450 og 484 eksakt. `[T]` | At SSB definerer middelfolkemengde slik, og at alder ved årets slutt ikke gir merkbart avvik per gruppe. |
| G18 | Dekomponering av veksten: folketall (190 000), aldersstruktur (70 000), bruk per aldersgruppe (119 000). Rekkefølgen påvirker størrelsen på leddene. | Topp C | Egen beregning `[T]` | Om fag godtar metoden, og om rekkefølgen bør oppgis i grafikken. Ikke publisert av SSB. |
| G19 | Rater per aldersgruppe (f.eks. 80–89 år: 814 → 881 per 1 000). | Topp C | Egen beregning fra 14824 og 07459 `[T]` | Spørsmål 6 i innsiktsnotatet: om SSB har grunner til ikke å publisere slike rater. |

**Teknisk merknad.** Grafikken lages av `scripts/lag_grafikk.py` med primitivene i `scripts/grafikk_pasient.py` (kopi av arblonn sine). Samlesiden lages av `scripts/lag_samleside.py`. Kontrollrenderingen er gjort med rsvg-convert og en reservefont, som er bredere enn Open Sans. Folketallet for C ligger i `data/raw/07459-folkemengde-alder.csv`, hentet gjennom SSB-tilkoblingen.

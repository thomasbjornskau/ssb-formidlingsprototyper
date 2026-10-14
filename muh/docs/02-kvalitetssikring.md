Steg 2 i formidlingsprototype for muh · versjon 1.0 · 14.10.2026 · Status: godkjent av Thomas (toppgrafikk C valgt, konseptgrafikk godkjent)

# Kvalitetssikring: grafikk (muh)

Påstander og valg i konseptgrafikken og toppgrafikken som er tolkning, eget valg eller ikke bekreftet av en gjeldende kilde. Kildemerkene viser til `01-innsikt.md`. Listen samles i `05-kvalitetssikring.md`.

## Konseptgrafikken

| # | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| G1 | De fleste varer meldes i en tolldeklarasjon. | `[K2]`, versjon 2015 | At dette fortsatt gjelder, og om TVINN er erstattet av nytt tollsystem. |
| G2 | Olje og gass rapporteres fra operatørene og Sokkeldirektoratet, strøm måles ved kablene, skip og plattformer fra registre og selskaper. | `[K2]`, versjon 2015 | At kildene er de samme i dag. «Kablene til utlandet» er vår forenkling av «målt ved grensekryssingspunktene». |
| G3 | Eksport regnes uten frakt videre fra grensen, import med frakt og forsikring fram til grensen. | `[K2]` (FOB og CIF) | At omskrivingen av FOB og CIF er faglig dekkende. |
| G4 | Olje og gass får først en anslått pris fra Brent og europeiske spotpriser, som senere byttes med faktisk pris. | `[K2][K3]` | At «faktisk pris» er riktig ord for det endelige tallet fra rettighetshaverne. |
| G5 | Regnestykket for fastlandseksport, august 2026: 191,0 − 42,6 − 77,7 − 0,01 = 70,6 mrd. kr. | `[K9]`, tabell 08792 | Delene summerer til 70 628 mill. kr, mot publisert 70 627. Avviket på 1 mill. kr er avrunding. Må oppdateres med septembertallene 15.10. |
| G6 | Hver ny måned kan endre de tidligere månedene i året. Endelige tall i mai to år etter. | `[K2][K11]` | At revisjonsrutinen er den samme som i 2015-versjonen. Tabell 12308 tyder på det. |
| G7 | Juli 2026: 173,6 mrd. kr først, 179,0 mrd. kr en måned senere. | `[K3][K11]` | Ingen. Tallene er hentet fra 12308. |
| G8 | «Ikke med»: tjenester, renter og utbytte, transitt, småsendinger under om lag 1 000 kr. | `[K2]` for transitt og småsendinger, `[T]` for tjenester, renter og utbytte | Beløpsgrensen er fra 2015 og kan være endret. Bør fag heller nevne midlertidig inn- og utførsel? |
| G9 | Fire trinn, ikke fem. Sortering på vare og land og fastlandsregnestykket er slått sammen i trinn 3. | Eget valg | At sammenslåingen ikke skjuler noe fag vil ha fram. |

## Toppgrafikken

| # | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| T1 | A: «Nesten 6 av 10 eksportkroner kom fra olje og gass i 2025.» Olje og gass er råolje, naturgass og kondensater. | `[K8][T]`: 1 010 476 av 1 778 791 mill. kr = 56,8 prosent | At avgrensningen er den fag bruker. Avviket fra Wass-rapportens «godt over 60 prosent» `[K6]` er ikke forklart. |
| T2 | A: Andelen følger prisene, 42 prosent i 2020 og 74 prosent i 2022. | `[K8][T]` | Ingen for tallene. «Følger prisene» er vår tolkning, støttet av B. |
| T3 | A: Årstall, ikke siste måned. | Eget valg: månedsandelen svinger (63 prosent i august 2026) | Om fag foretrekker siste tolv måneder. |
| T4 | A: Skip og plattformer under 2 prosent alle år 2015–2025. | `[K8][T]`: høyest 1,66 prosent i 2016 og 2017 | Ingen. |
| T5 | B: Eksportprisene steg 81,8 prosent i 2022, volumet 0,2 prosent. Overskriften runder til 82. | `[K10]`, publiserte endringsrater | At volum- og prisindeksene kan brukes i en muh-prototype. Kontakt i statistikkbanken er produsentprisindeksen. |
| T6 | B: Volumindeksen kalles «mengde». | Eget valg, for å treffe H1 | At ordet er faglig forsvarlig. |
| T7 | B: «Mest av økningen kom fra høyere gasspriser.» | `[K8][K10][T]`: gass stod for om lag 72 prosent av verdiøkningen 2021–2022, med gasspris +128,5 og volum +4,5 prosent | Sjekkes mot gassindeksen i steg 3, og av fag. |
| T8 | C: «Fastlands-Norge kjøpte varer for om lag 350 mrd. kr mer enn det solgte i 2025.» | `[K8]`: −347 737 mill. kr | At «fastlands-Norge kjøpte» er en forsvarlig forenkling. Importen i fastlandsbalansen omfatter også råolje og varer til sokkelen. |
| T9 | C: Fastlandsbalansen negativ alle år 2015–2025. | `[K8]` | Ingen. Lengre tilbake er ikke sjekket. |
| T10 | Farger: fastland grønn, olje og gass blå, handelsbalansen oker, skip og plattformer grå. | Eget valg etter `ssb-diagramstandard` | Samme farge for samme kategori i hele prototypen. Oker og blå flatetone har under 3:1 mot hvitt og er merket direkte. |
| T11 | Toppgrafikken er 1200 × 330 og blir liten på mobil. | Kjent fra pilotene | Mobilversjon av valgt variant lages i steg 4. |

## Teknisk

| # | Forhold | Hva må gjøres |
|---|---|---|
| X1 | `felles/grafikk.py` er gjenskapt midlertidig fordi repoet ikke var tilgjengelig. | Bytt til repoets versjon og kjør `scripts/lag_grafikk.py` på nytt før steg 4. |
| X2 | Tallene ligger i `data/grafikk-utkast.json`. | Erstattes av `data/raw/` i steg 3. |

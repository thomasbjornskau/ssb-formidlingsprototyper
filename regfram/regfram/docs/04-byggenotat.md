# Byggenotat, steg 4 (regfram)

Versjon 0.2 av prototypen, 14.10.2026. Bygget fra `src/index.template.html` og `data/raw/` med `felles/bygg.py`.

## Hva er endret fra versjon 0.1

| Forslag fra sammenligningen | Løsning |
|---|---|
| Lesehjelp høyt oppe | Boksen «Slik leser du en framskriving» med fire punkter, og konseptgrafikken bak «Slik lages tallene» |
| Tallet for hele landet (H4) | Egen setning i toppgrafikken når hele landet er valgt, og i fotnoten |
| Sentralisering | Alle kommuner som prikker farget etter sentralitet, og vekst per sentralitetsklasse |
| 70+ i stedet for 67+ | Tiårige aldersgrupper. 70+ i nøkkeltall, personrute, fylkesfigur og tabell |
| Min kommune | Alle 357 kommuner kan velges i nedtrekkslisten, med søk, ved klikk i tabell og prikkfigur, og via adressen (`#omrade=1804`) |
| Avrundede tall i tekst | Toppgrafikken avrunder. Eksakte tall står i «Vis tallene» og tabellen |
| Komponenter 2026–2049 | Rettet, og ny figur med samlet bidrag over perioden |

## Kontroller i byggeskriptet

`scripts/lag_data.py` stopper bygget hvis ett av disse ikke stemmer: kommunene summerer til fylkene og fylkene til landet, alle år og alternativer; aldersgruppene summerer til folkemengden; endring per år = fødte − døde + nettoinnvandring + innenlands flytting; kommunene summerer til klassetallene for sentralitet.

## Nye valg til kvalitetssikring (samlet i `05-kvalitetssikring.md`)

| | Valg | Begrunnelse |
|---|---|---|
| 10 | Varsel om små tall for kommuner under 2 000 innbyggere | Vår grense, for H3. Bør avklares med fagkontakten |
| 11 | Prikkfigur med aksen kuttet ved −20 og +45 prosent | Dekker alle kommuner i 2026-runden (−17,4 til +43,8). Må sjekkes ved ny publisering |
| 12 | Sentralitetsklasse 1 i mørkest grønn | Sekvensiell skala fra diagramstandarden, trinn 2–7. Klasse 6 er lys og har lav kontrast mot hvitt, men står også i tabellen |
| 13 | Overskrifter generert fra tallene, for eksempel «flere døde enn fødte fra 2046» | Teksten følger valgt område. Formuleringene bør leses av fagkontakten for et utvalg kommuner |

## Kjente svakheter

- Prikkfiguren kan ikke brukes med tastatur. Tabellen under dekker det samme.
- Filen er 790 kB fordi data, d3 og skrift er bakt inn. Det er valgt for at siden skal virke uten eksterne kall.

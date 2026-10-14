# Regionale befolkningsframskrivinger (regfram)

> **Prototype til faglig kontroll.** Ikke en offisiell SSB-publisering. Tallene er fra statistikkbanken, men tolkninger og overskrifter er ikke kvalitetssikret ennå.

**Se prototypen:** [index.html](index.html) (på GitHub Pages: `…/ssb-formidlingsprototyper/regfram/`)

Prototypen viser framskrevet folkemengde for landet, alle fylker og alle 357 kommuner fram mot 2050, basert på SSBs publisering 12. juni 2026. Alle sider kan vises for én kommune eller ett fylke, og valget ligger i adressen, for eksempel `#omrade=1804` for Bodø.

## Hva prototypen svarer på

| | Spørsmål | Seksjon |
|---|---|---|
| 1 | Hvor mange blir vi, og hvor sikkert er det? | Toppgrafikken med avrundet tall og spennet mellom lav og høy nasjonal vekst |
| 2 | Hvor vokser og hvor krymper det? | Alle kommuner etter sentralitet, vekst per sentralitetsklasse og per fylke |
| 3 | Hvorfor endrer folketallet seg? | Fødte minus døde, nettoinnvandring og flytting, samlet og år for år |
| 4 | Hvor raskt eldes befolkningen? | Andel 70 år og eldre, endring etter alder, fylkene sammenlignet |
| 5 | Hva skjer i min kommune? | Hele siden for valgt kommune, og kommunetabellen |

Øverst står «Slik leser du en framskriving», fire punkter om de vanligste misforståelsene.

## Til faglig kontroll

Det vi trenger vurdert, står i [docs/05-kvalitetssikring.md](docs/05-kvalitetssikring.md). Bakgrunnen står i:

- [docs/01-innsikt.md](docs/01-innsikt.md): nøkkelbudskap, begreper og hypoteser om misforståelser
- [docs/01b-sammenligning.md](docs/01b-sammenligning.md): hva innsikten endret i prototypen
- [docs/03-kildekart.md](docs/03-kildekart.md): tabeller, spørringer og kontroller
- [docs/04-byggenotat.md](docs/04-byggenotat.md): hva som er bygget og kjente svakheter
- [docs/grafikk/](docs/grafikk/): de tre variantene av toppgrafikk som ble vurdert

## Kilder

| Tabell | Innhold |
|---|---|
| [14746](https://www.ssb.no/statbank/table/14746) | Framskrevet folkemengde etter region, kjønn og alder, ni alternativer |
| [14747](https://www.ssb.no/statbank/table/14747) | Framskrevne fødte, døde, nettoinnvandring og innenlands nettoinnflytting |
| [14740](https://www.ssb.no/statbank/table/14740) | Den nasjonale framskrivingen, brukt til å forklare avviket for hele landet |
| [Klass, korrespondanse 1417](https://dataportal.ssb.no/classifications/128/versions/1427/correspondences/1417) | Sentralitetsklasse for hver kommune |

Spørringene står i [data/kilder.json](data/kilder.json). Fagkontakter for statistikken: Stefan Leknes og Sturla A. Løkken, SSB.

## Oppdatere

Fra roten av repoet:

```
python regfram/scripts/hent_data.py
python felles/bygg.py regfram
```

Merk: rådataene i `data/raw/` er i denne versjonen rekonstruert som json-stat2 fra svar hentet gjennom SSB-tilkoblingen 13.10.2026. `hent_data.py` er ikke kjørt direkte mot API-et ennå. Første kjøring bør gi en `index.html` med samme tall. Gjør den ikke det, stopper kontrollene bygget eller tallene endres, og det bør undersøkes før noe publiseres.

Koblingen mellom kommune og sentralitet (`data/raw/kommune_sentralitet.json`) hentes manuelt, og kontrolleres mot statistikkbanken ved hvert bygg.

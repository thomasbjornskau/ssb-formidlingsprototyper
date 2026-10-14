# Konsumprisindeksen (kpi)

> **Prototype til faglig kontroll.** Ikke en offisiell SSB-publisering. Tallene er fra statistikkbanken, men tolkninger, søkeord og overskrifter er ikke kvalitetssikret ennå.

**Se prototypen:** [https://thomasbjornskau.github.io/ssb-formidlingsprototyper/kpi/index.html](https://thomasbjornskau.github.io/ssb-formidlingsprototyper/kpi/index.html)

Prototypen viser prisveksten i KPI og lar deg søke på alle 336 vare- og tjenestegrupper i indeksen, med tall fra januar 2015 til september 2026. Valgt gruppe ligger i adressen, for eksempel `#gruppe=04.5.1` for strøm.

## Hva prototypen svarer på

| | Spørsmål | Seksjon |
|---|---|---|
| 1 | Hvor mye stiger prisene nå? | Toppgrafikken med KPI og KPI-JAE fra 2015 |
| 2 | Hva driver prisveksten? | Bidrag per hovedgruppe, og bidrag per måned fra 2017 |
| 3 | Hva er med i KPI, og hvor mye veier det? | Søket øverst, kortet for hver gruppe og vektene |
| 4 | Hvorfor finnes det flere KPI-er? | De åtte seriene i tabell 14706 sammenlignet |
| 5 | Hva er en krone verdt over tid? | Pengeverdi fra 1920 |

Øverst står «Slik leser du KPI», fire punkter om de vanligste misforståelsene.

## Til faglig kontroll

Bakgrunnen står i:

- [docs/01-innsikt.md](docs/01-innsikt.md): nøkkelbudskap, begreper og hypoteser om misforståelser
- [docs/02-kvalitetssikring.md](docs/02-kvalitetssikring.md): det som er tolket i grafikken
- [docs/03-kildekart.md](docs/03-kildekart.md): tabeller, spørringer, hierarkiet og bidragsmetoden
- [docs/04-byggenotat.md](docs/04-byggenotat.md): hva som er bygget, kontroller og kjente svakheter
- [docs/05-kvalitetssikring.md](docs/05-kvalitetssikring.md): samlet kvalitetssikring
- - [docs/grafikk/](docs/grafikk/): de tre variantene av toppgrafikk som ble vurdert

## Kilder

| Tabell | Innhold |
|---|---|
| [14700](https://www.ssb.no/statbank/table/14700) | Indeks, tolvmånedersendring og vekter for alle grupper (COICOP 2018) |
| [14706](https://www.ssb.no/statbank/table/14706) | KPI og avledede serier (KPI-JA, KPI-JAE, KPI-JE, KPI-JEL og XADM) fra 1995 |
| [14710](https://www.ssb.no/statbank/table/14710) | KPI fra 1920 |

Spørringene står i [data/kilder.json](data/kilder.json). Søkeordene står i [data/synonymer.json](data/synonymer.json).

## Oppdatere

Fra roten av repoet:

```
python kpi/scripts/hent_data.py
python felles/bygg.py kpi
```

Merk: rådataene i `data/raw/` er i denne versjonen rekonstruert som json-stat2 fra svar hentet gjennom SSB-tilkoblingen 14.10.2026. `hent_data.py` er ikke kjørt direkte mot API-et ennå. Første kjøring bør gi en `index.html` med samme tall. Gjør den ikke det, stopper kontrollene bygget eller tallene endres, og det bør undersøkes før noe publiseres.

`scripts/lag_grafikk.py` lager konseptgrafikken og toppgrafikkutkastene fra steg 2.

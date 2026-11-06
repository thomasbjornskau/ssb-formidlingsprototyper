# Arealprofiler (arealprofiler)

> **Prototype under arbeid.** Ikke en offisiell SSB-publisering. Tolkningene er ikke kvalitetssikret av fagseksjonen ennå. Det som skal kontrolleres, står i [02-kvalitetssikring](docs/02-kvalitetssikring.md) og [04-byggenotat](docs/04-byggenotat.md).

**Se prototypen:** [https://thomasbjornskau.github.io/ssb-formidlingsprototyper/arealprofiler/index.html](https://thomasbjornskau.github.io/ssb-formidlingsprototyper/arealprofiler/index.html)

Arealprofilene er 35 indikatorer per kommune for planleggere i kommuner og fylkeskommuner. Prototypen er et alternativ til dagens Tableau-app: én side per kommune i stedet for én side per indikator, og kommunen sammenlignet med kommuner med samme sentralitet i stedet for rangert. Kommunen ligger i adressen, for eksempel `#kommune=3405` for Lillehammer.

## Hva prototypen svarer på

| | Spørsmål | Seksjon |
|---|---|---|
| 1 | Hvordan står min kommune mot lignende kommuner? | Toppgrafikken og «Hele profilen» med alle 35 indikatorer |
| 2 | Bygger vi tettere og nærmere sentrum? | Nye boliger utenfor tettsted og i blokk, avstand til sentrumssonen |
| 3 | Hvor mye jord, strand og natur bygges ned? | Omdisponert jord for landet og kommunen, strandsonen |
| 4 | Hva er satt av i planen? | Ledig areal til bolig i kommuneplanen |
| 5 | Hvor mye bygges i fareområder? | Aktsomhets- og naturfareområder |

## Dokumentasjon

- [docs/01-innsikt.md](docs/01-innsikt.md): nøkkelbudskap, begreper og hypoteser om misforståelser
- [docs/01b-sammenligning.md](docs/01b-sammenligning.md): gjennomgang av dagens Tableau-app
- [docs/02-kvalitetssikring.md](docs/02-kvalitetssikring.md): det som er tolket i grafikken
- [docs/03-kildekart.md](docs/03-kildekart.md): kilder, struktur, metoder og kontroller
- [docs/04-byggenotat.md](docs/04-byggenotat.md): hva som er bygget, kontroller og kjente svakheter
- [docs/grafikk/](docs/grafikk/): konseptgrafikken og variantene av toppgrafikk

## Kilder

| Kilde | Innhold |
|---|---|
| Datagrunnlaget for Arealprofiler 2025 | `data/raw/arealprofiler2024_ettark.xlsx`, 35 indikatorer, 357 kommuner, 2015–2025. Publisert 29.08.2025 |
| [Tabell 11776](https://www.ssb.no/statbank/table/11776) | Omdisponert dyrka og dyrkbar jord for landet |
| [Klass 128](https://www.ssb.no/klass/klassifikasjoner/128) | Sentralitet 2020 for kommuneinndelingen 2024 |
| [Klass 104](https://www.ssb.no/klass/klassifikasjoner/104) | Fylker 2024 |

Tabell 14478 og 14488 med årets arealprofiler er ikke publisert eksternt. URL-ene står klare i [data/kilder.json](data/kilder.json).

## Oppdatere

Fra roten av repoet:

```
python arealprofiler/scripts/hent_data.py   # henter Klass og tabell 11776 på nytt
python felles/bygg.py arealprofiler
```

Datagrunnlaget for arealprofilene ligger uendret som Excel-fil i `data/raw/` og hentes ikke av `hent_data.py`. Klass og tabell 11776 er hentet direkte fra API-ene 06.11.2026, uendret. `scripts/lag_data.py` lager byggfilen og stopper bygget hvis kontrollene feiler. Toleransene er forklart i skriptet.

`scripts/lag_grafikk_data.py` og `scripts/lag_grafikk.py` lager konseptgrafikken og toppgrafikkutkastene fra steg 2. `scripts/lag_samleside.py` lager samlesiden i `docs/grafikk/`. `scripts/analyser_struktur.py` teller strukturen til kildekartet.

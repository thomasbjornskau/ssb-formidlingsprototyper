# Innvandrere og norskfødte med innvandrerforeldre i kommunene (`innvbef-omrade`)

> **Prototype.** Laget for å prøve ut formidling av statistikken. Ikke en offisiell SSB-publisering. Tolkninger, egne beregninger og overskrifter er ikke kvalitetssikret ennå. Se [byggenotatet](docs/04-byggenotat.md).

**Lenke:** https://thomasbjornskau.github.io/ssb-formidlingsprototyper/innvbef-omrade/

En variant av [`innvbef`](../innvbef/), med kommune eller fylke som hovedvalg og et kart over alle 357 kommuner. Landbakgrunn velges for kartet, for eksempel for å se hvor de med polsk bakgrunn bor. Valget ligger i adressen, for eksempel `#omrade=1835&land=131` for Træna og Polen.

## Hva prototypen svarer på

| | Spørsmål | Seksjon |
|---|---|---|
| 1 | Hvem regnes med? | Lesehjelpen og «Slik lages tallene» |
| 2 | Hvordan har antallet og andelen endret seg i området? | Toppgrafikken, 1970–2026 (andel fra 1986) |
| 3 | Hvor kommer de fra? | Verdensdeler over tid og de største landbakgrunnene i området |
| 4 | Hvor bor de? | Kartet og sammenligningen med de andre kommunene i fylket |

## Dokumentasjon

- [docs/04-byggenotat.md](docs/04-byggenotat.md): kilder, hva som er bygget, kontroller og kjente svakheter
- Innsikt, grafikk og kvalitetssikring fra steg 1–2: se [`innvbef/docs/`](../innvbef/docs/)

## Kilder

| Tabell | Innhold |
|---|---|
| [05182](https://www.ssb.no/statbank/table/05182) | Personer etter innvandringskategori, hele landet |
| [05803](https://www.ssb.no/statbank/table/05803) | Befolkning 1. januar, hele landet |
| [07108](https://www.ssb.no/statbank/table/07108) | Innvandrere og norskfødte etter verdensdel, kommuner og fylker med sammenslåtte tidsserier |
| [07459](https://www.ssb.no/statbank/table/07459) | Folketall, kommuner og fylker med sammenslåtte tidsserier |
| [09817](https://www.ssb.no/statbank/table/09817) | Kommune- og fylkestall etter landbakgrunn |
| [robhop/fylker-og-kommuner](https://github.com/robhop/fylker-og-kommuner) | Kommunegrenser 2024 fra Kartverket, forenklet. `data/raw/kommuner2024-S.geojson` |

Spørringene står i [data/kilder.json](data/kilder.json). Tidligere kommunenavn i søket (`data/synonymer.json`) er kopiert fra `folkemengde` (Klass 131), og landsynonymene (`data/land-synonymer.json`) fra `innvbef`.

## Oppdatere

Fra roten av repoet:

```
python innvbef-omrade/scripts/hent_data.py     # henter ferske tall og kodelisten fra statistikkbanken
python felles/bygg.py innvbef-omrade           # kontrollerer og bygger innvbef-omrade/index.html
```

Rådataene i `data/raw/` er hentet direkte fra PxWebApi v2 med `hent_data.py` 11.11.2026, ikke rekonstruert. Kartfilen er kopiert fra `arealprofiler` og hentes ikke av skriptet.

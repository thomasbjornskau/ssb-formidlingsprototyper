# Innvandrere og norskfødte med innvandrerforeldre (innvbef)

> **Prototype.** Ikke en offisiell SSB-publisering. Tallene er fra statistikkbanken, men tolkninger, egne beregninger og overskrifter er ikke kvalitetssikret ennå. Se [byggenotatet](docs/04-byggenotat.md).

**Se prototypen:** [https://thomasbjornskau.github.io/ssb-formidlingsprototyper/innvbef/index.html](https://thomasbjornskau.github.io/ssb-formidlingsprototyper/innvbef/index.html)

Prototypen viser hvor mange innvandrere og norskfødte med innvandrerforeldre som bor i Norge, hvem som regnes med, hvorfor antallet endrer seg, hvor de kommer fra og hvor de bor. Du kan velge blant 215 landbakgrunner, også ved å søke på adjektiv som «polsk» eller eldre navn som «Burma». Valgt land ligger i adressen, for eksempel `#land=131` for Polen, og styrer alle seksjonene.

## Hva prototypen svarer på

| | Spørsmål | Seksjon |
|---|---|---|
| 1 | Hvem regnes som innvandrer? | SSBs seks kategorier og de 30 kombinasjonene av tre generasjoner |
| 2 | Hvordan og hvorfor endrer antallet seg? | Toppgrafikken (antall og andel 1970–2026) og befolkningsregnskapet 2016–2025 |
| 3 | Hvor kommer de fra, og når kom de? | De største landbakgrunnene og botid |
| 4 | Hvor bor de? | Kommunene med høyest andel eller flest, og alle 357 kommuner |
| – | Hvem telles som bosatt? | Lesehjelpen og «Slik lages tallene» |

## Dokumentasjon

- [docs/01-innsikt.md](docs/01-innsikt.md): nøkkelbudskap, begreper og hypoteser om misforståelser
- [docs/02-kvalitetssikring.md](docs/02-kvalitetssikring.md): det som er tolket i grafikken
- [docs/03-kildekart.md](docs/03-kildekart.md): tabeller, spørringer, struktur og kontroller
- [docs/04-byggenotat.md](docs/04-byggenotat.md): hva som er bygget, kontroller og kjente svakheter
- [docs/grafikk/](docs/grafikk/): variantene av toppgrafikk som ble vurdert

## Kilder

| Tabell | Innhold |
|---|---|
| [05182](https://www.ssb.no/statbank/table/05182) | Personer etter innvandringskategori 1970–2026 |
| [05803](https://www.ssb.no/statbank/table/05803) | Befolkning 1. januar |
| [12548](https://www.ssb.no/statbank/table/12548) | Hele befolkningen fordelt på tre generasjoner 2004–2026 |
| [10516](https://www.ssb.no/statbank/table/10516) | Befolkningsendringer etter innvandringskategori |
| [10518](https://www.ssb.no/statbank/table/10518) | Befolkningsendringer etter verdensdel og utvalgte land |
| [13880](https://www.ssb.no/statbank/table/13880) | Innvandrere og norskfødte med innvandrerforeldre etter landbakgrunn 2004–2026 |
| [10598](https://www.ssb.no/statbank/table/10598) | Innvandrere etter landbakgrunn og botid |
| [09817](https://www.ssb.no/statbank/table/09817) | Kommunetall etter landbakgrunn og andel av befolkningen |
| [07459](https://www.ssb.no/statbank/table/07459) | Folkemengde per kommune |

Spørringene og kodelisten for verdensdeler står i [data/kilder.json](data/kilder.json).

## Oppdatere

Fra roten av repoet:

```
python innvbef/scripts/hent_data.py     # henter ferske tall og kodelisten fra statistikkbanken
python felles/bygg.py innvbef           # kontrollerer og bygger innvbef/index.html
```

Rådataene i `data/raw/` er hentet direkte fra PxWebApi v2 med `hent_data.py` 26.10.2026, ikke rekonstruert. Kontrollene i `lag_data.py` har toleranser satt etter faktiske avvik fra avrundede småceller. Endrer SSB tallene slik at en kontroll feiler, stopper bygget, og avviket må undersøkes før noe publiseres.

`scripts/lag_grafikk.py` og `scripts/lag_samleside.py` lager konseptgrafikken og grafikkutkastene fra steg 2.

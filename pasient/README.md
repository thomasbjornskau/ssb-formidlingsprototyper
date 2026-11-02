# Pasienter i spesialisthelsetjenesten (pasient)

> **Prototype under arbeid.** Ikke en offisiell SSB-publisering. Tolkningene er ikke kvalitetssikret av fagseksjonen ennå. Det som skal kontrolleres, står i [02-kvalitetssikring](docs/02-kvalitetssikring.md) og [04-byggenotat](docs/04-byggenotat.md).

**Se prototypen:** [https://thomasbjornskau.github.io/ssb-formidlingsprototyper/pasient/index.html](https://thomasbjornskau.github.io/ssb-formidlingsprototyper/pasient/index.html)

Prototypen viser hvor mange som får behandling i somatisk spesialisthelsetjeneste og psykisk helsevern for voksne, hva de får, hvem de er og hva de behandles for. Diagnosekapittel er valget som styrer seksjonene, og det ligger i adressen, for eksempel `#kapittel=II` for svulster. Dette er den første prototypen av en statistikk utenfor Topp20.

## Hva prototypen svarer på

| | Spørsmål | Seksjon |
|---|---|---|
| 1 | Hvor mange får behandling, og hva får de? | Toppgrafikken og «Hva får pasientene?»: pasienter, kontakter, døgnopphold og oppholdsdøgn |
| 2 | Hvem er pasientene? | Rater per aldersgruppe, veksten fordelt på folketall, aldring og bruk, kvinner og menn |
| 3 | Hva behandles de for? | 20 diagnosekapitler og 200 kategoriblokker |
| 4 | Bruker innvandrere og barna deres tjenestene annerledes? | Ujusterte og aldersjusterte rater |
| 5 | Psykisk helsevern for voksne: hva skjer med de unge? | Pasienter etter alder og kjønn |

## Dokumentasjon

- [docs/01-innsikt.md](docs/01-innsikt.md): nøkkelbudskap, begreper og hypoteser om misforståelser
- [docs/02-kvalitetssikring.md](docs/02-kvalitetssikring.md): det som er tolket i grafikken
- [docs/03-kildekart.md](docs/03-kildekart.md): tabeller, struktur, metoder og kontroller
- [docs/04-byggenotat.md](docs/04-byggenotat.md): hva som er bygget, kontroller og kjente svakheter
- [docs/grafikk/](docs/grafikk/): konseptgrafikken og variantene av toppgrafikk som ble vurdert

## Kilder

| Tabell | Innhold |
|---|---|
| [14824](https://www.ssb.no/statbank/table/14824) | Somatikk: pasienter, kontakter, dagbehandlinger, døgnopphold og oppholdsdøgn etter kjønn, alder og diagnose, 2015–2025 |
| [14827](https://www.ssb.no/statbank/table/14827) | Somatikk: pasienter per 1 000 innbyggere etter kjønn, innvandringskategori og diagnosekapittel |
| [14820](https://www.ssb.no/statbank/table/14820) | Psykisk helsevern for voksne etter kjønn og alder |
| [14823](https://www.ssb.no/statbank/table/14823) | Psykisk helsevern for voksne: pasienter per 1 000 etter kjønn og innvandringskategori |
| [07459](https://www.ssb.no/statbank/table/07459) | Folkemengde etter alder, til egne rater per aldersgruppe |

Spørringene står i [data/kilder.json](data/kilder.json).

## Oppdatere

Fra roten av repoet:

```
python pasient/scripts/hent_data.py   # henter ferske tall fra statistikkbanken
python felles/bygg.py pasient
```

Rådataene i `data/raw/` er hentet direkte fra PxWebApi v2 med `hent_data.py` 02.11.2026, uendret. De er ikke rekonstruert. `scripts/lag_data.py` lager byggfilen og stopper bygget hvis en av kontrollene D1–D7 feiler. Toleransene er satt etter faktiske avvik fra avrunding og står forklart i skriptet.

`scripts/lag_grafikk.py` lager konseptgrafikken og toppgrafikkutkastene fra steg 2, med primitivene i `scripts/grafikk_pasient.py`. `scripts/lag_samleside.py` lager samlesiden i `docs/grafikk/`.

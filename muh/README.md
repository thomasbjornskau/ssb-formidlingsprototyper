# Utenrikshandel med varer (muh)

> **Prototype til faglig kontroll, versjon 0.2.** Ikke en offisiell SSB-publisering. Fagseksjonen har svart på de viktigste punktene (del A, 04.11.2026), og svarene er innarbeidet. Delen om pris og volum skal kontrolleres av prisseksjonen, og resten av [kvalitetssikringslisten](docs/05-kvalitetssikring.md) er ikke besvart ennå.

**Se prototypen:** [https://thomasbjornskau.github.io/ssb-formidlingsprototyper/muh/index.html](https://thomasbjornskau.github.io/ssb-formidlingsprototyper/muh/index.html)

Prototypen viser Norges handel med varer: hvor mye som er olje og gass, hva handelsoverskuddet forteller, og hvem Norge handler med. Du kan søke etter alle land Norge har handlet med 2015–2025. Valgt land ligger i adressen, for eksempel `#land=PL` for Polen.

## Hva prototypen svarer på

| | Spørsmål | Seksjon |
|---|---|---|
| 1 | Hvor mye av eksporten er olje og gass, og hvor mye er fastlandet? | Eksport 1960–2025 fordelt, og regnestykket for fastlandseksporten |
| 2 | Hvorfor svinger eksportverdien så mye: pris eller volum? | Pris- og volumindekser fra 2000 |
| 3 | Hva forteller handelsoverskuddet, og hvorfor har fastlandet underskudd? | Toppgrafikken og balansene per måned og år |
| 4 | Hva eksporterer fastlands-Norge? | De største varegruppene i 2025 og fra 2015 |
| 5 | Hvem handler Norge med? | Søket øverst, kortet for hvert land og de største handelspartnerne |

Øverst står «Slik leser du utenrikshandelen», fire punkter om de vanligste misforståelsene. Nederst viser en figur hvor mye månedstallene endres etter første publisering.

## Til faglig kontroll

Den samlede listen over det som må avklares, bør leses og spørsmålene til fagseksjonen står i [docs/05-kvalitetssikring.md](docs/05-kvalitetssikring.md). Den erstatter listene fra de tidligere stegene.

## Dokumentasjon

- [docs/01-innsikt.md](docs/01-innsikt.md): nøkkelbudskap, begreper og hypoteser om misforståelser
- [docs/02-kvalitetssikring.md](docs/02-kvalitetssikring.md): det som er tolket i grafikken
- [docs/03-kildekart.md](docs/03-kildekart.md): tabeller, spørringer, struktur og kontroller
- [docs/04-byggenotat.md](docs/04-byggenotat.md): hva som er bygget, kontroller og kjente svakheter
- [docs/05-kvalitetssikring.md](docs/05-kvalitetssikring.md): samlet kvalitetssikring
- [docs/grafikk/](docs/grafikk/): de tre variantene av toppgrafikk som ble vurdert

## Kilder

| Tabell | Innhold |
|---|---|
| [08800](https://www.ssb.no/statbank/table/08800) | Hovedtall per år fra 1960 |
| [08792](https://www.ssb.no/statbank/table/08792) | Hovedtall per måned |
| [08804](https://www.ssb.no/statbank/table/08804) | Hovedtall etter land |
| [08809](https://www.ssb.no/statbank/table/08809) | Varegrupper (ensifret SITC) etter land |
| [08819](https://www.ssb.no/statbank/table/08819) | Varegrupper (tresifret SITC) |
| [06322](https://www.ssb.no/statbank/table/06322) | Pris- og volumindekser |
| [12308](https://www.ssb.no/statbank/table/12308) | Foreløpige og reviderte månedstall |

Spørringene står i [data/kilder.json](data/kilder.json). Søkeordene står i [data/synonymer.json](data/synonymer.json).

## Oppdatere

Fra roten av repoet:

```
python muh/scripts/hent_data.py
python felles/bygg.py muh
```

Rådataene i `data/raw/` er hentet direkte fra PxWebApi v2 med `hent_data.py` 04.11.2026. URL-ene bruker `valueCodes[...]`. Endrer SSB tallene slik at summene ikke går opp, stopper kontrollene i `lag_data.py` bygget, og avviket må undersøkes før noe publiseres.

`scripts/lag_grafikk.py` lager konseptgrafikken og toppgrafikkutkastene fra steg 2. `scripts/kontroll_kilder.py` kjører strukturtellingene og kontrollene fra steg 3.

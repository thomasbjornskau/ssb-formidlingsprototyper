# Navn (navn)

> **Prototype til faglig kontroll.** Ikke en offisiell SSB-publisering. Tallene er fra statistikkbanken, men tolkninger, egne beregninger og overskrifter er ikke kvalitetssikret ennå. Se [kvalitetssikringslisten](docs/05-kvalitetssikring.md).

**Se prototypen:** [https://thomasbjornskau.github.io/ssb-formidlingsprototyper/navn/index.html](https://thomasbjornskau.github.io/ssb-formidlingsprototyper/navn/index.html)

Prototypen lar deg finne ditt eget navn og se hvor stor andel av de nyfødte som har fått det hvert år siden 1880, hvor mange som heter det i dag, og hvordan det plasserer seg. Den forklarer også hvorfor topplisten og statistikkbanken gir ulike tall: topplisten slår sammen skrivemåter som Lucas og Lukas. Valgt navn ligger i adressen, for eksempel `#navn=2LUKAS`, og styrer seksjonene.

## Hva prototypen svarer på

| | Spørsmål | Seksjon |
|---|---|---|
| 1 | Hvordan har ditt navn utviklet seg? | Kortet og «Hvordan har navnet utviklet seg?» (andel fra 1880, antall fra 1945) |
| 2 | Hvilke navn var mest populære i 2025, og hvor mye betyr det? | Toppgrafikken: topp 5 med skrivemåter, for jente- og guttenavn |
| 3 | Er toppnavnene mindre dominerende enn før? | «Er toppnavnene mindre dominerende enn før?» |
| 4 | Hva er forskjellen på populært og vanlig? | «Populært eller vanlig?» og de vanligste fornavnene i befolkningen |
| 5 | Hvilke etternavn er vanligst? | De 15 vanligste etternavnene |

## Dokumentasjon

- [docs/01-innsikt.md](docs/01-innsikt.md): nøkkelbudskap, begreper og hypoteser om misforståelser
- [docs/02-kvalitetssikring.md](docs/02-kvalitetssikring.md): det som er tolket i grafikken
- [docs/03-kildekart.md](docs/03-kildekart.md): tabeller, spørringer, struktur og kontroller
- [docs/04-byggenotat.md](docs/04-byggenotat.md): hva som er bygget, kontroller og kjente svakheter
- [docs/05-kvalitetssikring.md](docs/05-kvalitetssikring.md): samlet kvalitetssikring, erstatter listene i de tidligere dokumentene
- [docs/grafikk/](docs/grafikk/): variantene av toppgrafikk som ble vurdert

## Kilder

| Kilde | Innhold |
|---|---|
| [10467](https://www.ssb.no/statbank/table/10467) | Fødte etter jente- og guttenavn 1880–2025 |
| [10501](https://www.ssb.no/statbank/table/10501) | Personer etter jente- og guttenavn 2013–2025 |
| [12891](https://www.ssb.no/statbank/table/12891) | Etternavn brukt av 200 personer eller flere 2018–2025 |
| [Jentenavn](https://www.ssb.no/befolkning/navn/artikler/jentenavn) og [Guttenavn](https://www.ssb.no/befolkning/navn/artikler/guttenavn) | Topplistene for 2025 med skrivemåter, brukt i `data/synonymer.json` |

Spørringene står i [data/kilder.json](data/kilder.json).

## Oppdatere

Fra roten av repoet:

```
python navn/scripts/hent_data.py    # henter ferske tall fra statistikkbanken
python felles/bygg.py navn          # kontrollerer og bygger navn/index.html
```

Når nye topplister publiseres, må `data/synonymer.json` oppdateres for hånd fra artiklene «Jentenavn» og «Guttenavn». Grupperingen av skrivemåter finnes ikke som data. Bygget stopper hvis skrivemåtene i statistikkbanken ikke stemmer med artiklene.

Rådataene i `data/raw/` er hentet direkte fra PxWebApi v2 med `hent_data.py` 23.10.2026, ikke rekonstruert. `scripts/lag_grafikk.py` lager konseptgrafikken og toppgrafikkutkastene fra steg 2, med primitivene i `scripts/grafikk_navn.py`.

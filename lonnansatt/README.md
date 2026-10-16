# Lønn (lonnansatt)

> **Prototype til faglig kontroll.** Ikke en offisiell SSB-publisering. Tallene er fra statistikkbanken, men tolkninger, egne beregninger og overskrifter er ikke kvalitetssikret ennå. Se [kvalitetssikringslisten](docs/05-kvalitetssikring.md).

**Se prototypen:** [https://thomasbjornskau.github.io/ssb-formidlingsprototyper/lonnansatt/index.html](https://thomasbjornskau.github.io/ssb-formidlingsprototyper/lonnansatt/index.html)

Prototypen viser hva lønnsstatistikken sier og hva den ikke sier: at de fleste tjener mindre enn gjennomsnittet, hva månedslønna består av, lønna i over 400 yrker, forskjellen mellom kvinner og menn og hvorfor det finnes flere tall for lønnsveksten. Du kan søke etter alle yrker. Valgt yrke ligger i adressen, for eksempel `#yrke=2223` for sykepleiere.

## Hva prototypen svarer på

| | Spørsmål | Seksjon |
|---|---|---|
| 1 | Hva er månedslønn, og hva er ikke med? | Lesehjelpen, «Slik lages tallene» og «Hva er månedslønn?» |
| 2 | Hva tjener de fleste? | Toppgrafikken (desilene mot gjennomsnitt og median) og «Hva tjener de fleste?» |
| 3 | Hva tjener et yrke? | Søket øverst, kortet for hvert yrke, prikkdiagrammet og de 15 største yrkene |
| 4 | Hvor stor er forskjellen mellom kvinner og menn, og hva betyr tallet? | «Hvor stor er forskjellen …» og kortet for hvert yrke |
| 5 | Hvorfor finnes det flere tall for lønnsveksten? | «Hvor mye steg lønna?» |

## Dokumentasjon

- [docs/01-innsikt.md](docs/01-innsikt.md): nøkkelbudskap, begreper og hypoteser om misforståelser
- [docs/02-kvalitetssikring.md](docs/02-kvalitetssikring.md): det som er tolket i grafikken
- [docs/03-kildekart.md](docs/03-kildekart.md): tabeller, spørringer, struktur og kontroller
- [docs/04-byggenotat.md](docs/04-byggenotat.md): hva som er bygget, kontroller og kjente svakheter
- [docs/05-kvalitetssikring.md](docs/05-kvalitetssikring.md): samlet kvalitetssikring, erstatter listene i de tidligere dokumentene
- [docs/grafikk/](docs/grafikk/): de tre variantene av toppgrafikk som ble vurdert

## Kilder

| Tabell | Innhold |
|---|---|
| [11418](https://www.ssb.no/statbank/table/11418) | Månedslønn etter yrke (firesifret STYRK-08), kjønn og sektor |
| [11419](https://www.ssb.no/statbank/table/11419) | Månedslønn og delene av den etter sektor, kjønn og arbeidstid |
| [13860](https://www.ssb.no/statbank/table/13860) | Desil- og persentilfordelt månedslønn |
| [11536](https://www.ssb.no/statbank/table/11536) | Årslønn, utbetalt, etter sektor |
| [14858](https://www.ssb.no/statbank/table/14858) | Årslønn påløpt, nominelt og reelt |

Spørringene står i [data/kilder.json](data/kilder.json).

## Oppdatere

Fra roten av repoet:

```
python lonnansatt/scripts/hent_data.py
python felles/bygg.py lonnansatt
```

Merk: rådataene i `data/raw/` er i denne versjonen rekonstruert som json-stat2 fra svar hentet gjennom SSB-tilkoblingen 15.10.2026. `hent_data.py` er ikke kjørt direkte mot API-et ennå. Første kjøring bør gi samme tall. Stopper kontrollene bygget, bør det undersøkes før noe publiseres. Kontroll K7 har ett kjent avvik (menn 2023) som må fjernes fra listen hvis SSB retter det.

`scripts/lag_grafikk.py` lager konseptgrafikken og toppgrafikkutkastene fra steg 2. `scripts/kontroll_kilder.py` kjører kontrollene fra steg 3. `scripts/lag_data.py` lager byggfilen og stopper bygget hvis en kontroll feiler.

# Antall arbeidsforhold og lønn (arblonn)

> **Prototype til faglig kontroll.** Ikke en offisiell SSB-publisering. Tolkningene er ikke kvalitetssikret av fagseksjonen ennå. Det som skal kontrolleres, står i [kvalitetssikringslisten](docs/05-kvalitetssikring.md).

**Se prototypen:** [https://thomasbjornskau.github.io/ssb-formidlingsprototyper/arblonn/index.html](https://thomasbjornskau.github.io/ssb-formidlingsprototyper/arblonn/index.html)

Prototypen viser hvor mange jobber og lønnstakere det er i Norge, hvilken lønn SSB oppgir, og om det blir flere eller færre jobber nå. Næring er valget som styrer alle seksjonene, og det ligger i adressen, for eksempel `#naering=86-88` for helse og sosial. Fylke kan velges i seksjonen om hvor jobbene vokser.

## Hva prototypen svarer på

| | Spørsmål | Seksjon |
|---|---|---|
| 1 | Hvor mange jobber er det, og hvor mange mennesker har dem? | «Hvor mange jobber …»: jobber, lønnstakere og heltidsekvivalenter, deltid og alder |
| 2 | Hvilken lønn er det SSB oppgir? | «Hvilken lønn …»: snitt og median, avtalt månedslønn og månedslønn, kvinner og menn |
| 3 | Blir det flere eller færre jobber nå? | Toppgrafikken og «Blir det flere …»: foreløpige og endelige tall, næringenes bidrag, sesongjustering |
| 4 | Hvor vokser jobbene, og hvor er lønna høyest? | Næringer, fylker og tosifrede undernæringer |
| 5 | Hva betyr lønnsveksten? | Lønnsvekst per næring og vekst i snitt og median |

## Dokumentasjon

- [docs/01-innsikt.md](docs/01-innsikt.md): nøkkelbudskap, begreper og hypoteser om misforståelser
- [docs/02-kvalitetssikring.md](docs/02-kvalitetssikring.md): det som er tolket i grafikken
- [docs/03-kildekart.md](docs/03-kildekart.md): tabeller, struktur, metoder og kontroller
- [docs/04-byggenotat.md](docs/04-byggenotat.md): hva som er bygget, kontroller og kjente svakheter
- [docs/05-kvalitetssikring.md](docs/05-kvalitetssikring.md): samlet kvalitetssikring, erstatter listene i de tidligere dokumentene
- [docs/grafikk/](docs/grafikk/): konseptgrafikken og variantene av toppgrafikk som ble vurdert

## Kilder

| Tabell | Innhold |
|---|---|
| [13126](https://www.ssb.no/statbank/table/13126) | Lønnstakere, jobber og kontantlønn per måned og næring, foreløpige og endelige tall, 2003–2026 |
| [11654](https://www.ssb.no/statbank/table/11654) | Lønnstakere, jobber, heltidsekvivalenter, lønn og lønnsindeks per næring og fylke, kvartal 2016–2026 |
| [13871](https://www.ssb.no/statbank/table/13871) | Heltid og deltid per næring og kjønn |
| [11652](https://www.ssb.no/statbank/table/11652) | Kjønn og alder, hele landet |
| [12314](https://www.ssb.no/statbank/table/12314) | Tosifret næring (88 grupper), hele landet |

Spørringene står i [data/kilder.json](data/kilder.json).

## Oppdatere

Fra roten av repoet:

```
python arblonn/scripts/hent_data.py         # henter ferske tall fra statistikkbanken
python arblonn/scripts/kontroll_kilder.py   # kontrollene fra steg 3
python felles/bygg.py arblonn
```

Rådataene i `data/raw/` er hentet direkte fra PxWebApi v2 med `hent_data.py` 30.10.2026, uendret. De er ikke rekonstruert. Kontrollene har kjente avvik skrevet inn med verdi, for eksempel −305 jobber mellom 2024M11 og 2024K4. Endrer SSB tallene slik at en kontroll feiler, stopper bygget, og avviket må undersøkes før noe publiseres.

`scripts/lag_grafikk.py` lager konseptgrafikken og toppgrafikkutkastene fra steg 2, med primitivene i `scripts/grafikk_arblonn.py`. `scripts/lag_data.py` lager byggfilen og stopper bygget hvis en kontroll feiler.

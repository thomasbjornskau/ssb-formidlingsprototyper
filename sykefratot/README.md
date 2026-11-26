# Sykefravær (sykefratot)

> **Prototype under arbeid, versjon 0.1.** Ikke en offisiell SSB-publisering. Tallene er kontrollert ved bygging, men tolkninger, overskrifter og utforming er ikke kvalitetssikret av fagseksjonen ennå.

**Se prototypen:** [https://thomasbjornskau.github.io/ssb-formidlingsprototyper/sykefratot/index.html](https://thomasbjornskau.github.io/ssb-formidlingsprototyper/sykefratot/index.html)

Prototypen viser SSBs sykefraværsstatistikk for 3. kvartal 2026. Den forklarer hva sykefraværsprosenten måler, hvorfor SSB og Nav melder ulike tall samme dag, og hvor mye av fraværet som er lange sykmeldinger. Du kan velge kjønn, søke på yrke og søke på kommune. Valgene ligger i adressen, for eksempel `#kjonn=kvinner&yrke=2223&kommune=3403`.

## Hva prototypen svarer på

| | Spørsmål | Seksjon |
|---|---|---|
| 1 | Hvor høyt er sykefraværet, og går det opp eller ned? | Toppgrafikken |
| 2 | Hva betyr «6,7 prosent» egentlig? | Slik leser du tallene og Slik lages tallene |
| 3 | Er det korte egenmeldinger eller lange sykmeldinger som utgjør fraværet? | Korte egenmeldinger eller lange sykmeldinger? |
| 4 | Hvem har høyest fravær? | Kvinner og menn, yrkesgrupper, Finn yrket ditt, Min kommune |
| – | Hvorfor melder SSB og Nav ulike tall? | Samme kvartal, to tall: SSB og Nav |

Næring er utelatt med vilje. Sykefraværsstatistikken går over til ny næringsstandard (SN2025) fra 1. kvartal 2027, og tabellene etter SN2007 avsluttes.

## Dokumentasjon

- [docs/01-innsikt.md](docs/01-innsikt.md): nøkkelbudskap, begreper, hypoteser og spørsmål til fag
- [docs/02-kvalitetssikring.md](docs/02-kvalitetssikring.md): det som er tolket i grafikken
- [docs/03-kildekart.md](docs/03-kildekart.md): tabeller, struktur, kontroller og hull
- [docs/04-byggenotat.md](docs/04-byggenotat.md): hva som er bygget, kontroller og kjente svakheter
- [docs/grafikk/](docs/grafikk/): de tre variantene av toppgrafikk som ble vurdert

## Kilder

| Tabell | Innhold |
|---|---|
| [12439](https://www.ssb.no/statbank/table/12439) | Sykefravær etter type og kjønn, sesongjustert og ikke-sesongjustert, fra 2000 |
| [12946](https://www.ssb.no/statbank/table/12946) | Sykefraværsdagsverk og -tilfeller etter varighet, fra 2015 |
| [12446](https://www.ssb.no/statbank/table/12446) | Legemeldt sykefravær og lønnstakere med legemelding, hele landet |
| [12452](https://www.ssb.no/statbank/table/12452) | Legemeldt sykefravær etter yrke (STYRK08), fra 2015 |
| [12451](https://www.ssb.no/statbank/table/12451) | Legemeldt sykefravær etter bostedskommune, fra 2024 |

Søkeordene for yrker i `data/synonymer.json` er vårt valg og skal leses av fagkontakten.

## Oppdatering

Rådataene i `data/raw/` er hentet direkte fra statistikkbanken med `scripts/hent_data.py` 26.11.2026 og er uendret. De har de ekte statussymbolene. Ingenting er rekonstruert. Slik oppdateres prototypen, fra roten av repoet:

```
python sykefratot/scripts/hent_data.py
python felles/bygg.py sykefratot
```

`bygg.py` kjører `scripts/lag_data.py`, som kontrollerer summene og stopper bygget hvis de ikke går opp. Kontrollen B9 sammenligner med grafikken fra steg 2 bare så lenge siste kvartal er det samme. B8 stopper hvis antall yrker eller kommuner endrer seg, og det er med vilje. Neste publisering er 25.02.2027.

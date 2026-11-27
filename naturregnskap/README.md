# Naturregnskap – formidlingsprototype

**Prototype.** Laget for å prøve ut formidling av statistikken. Ikke en offisiell SSB-publisering. Ikke faglig kontrollert ennå.

Side: https://thomasbjornskau.github.io/ssb-formidlingsprototyper/naturregnskap/

Svarer på: Hvor mye natur har vi? Hvordan har naturen det? Hva gir naturen oss? Hvor sikre er tallene?
Hele siden styres av valgt hovedøkosystem (`#oko=04` gir skog). Tallene gjelder hele landet og fem landsdeler. Kommunetall finnes ikke ennå.

## Dokumenter
- `docs/01-innsikt.md` – statistikken, misforståelser (H1–H10), prioriterte spørsmål
- `docs/02-kvalitetssikring.md`, `docs/grafikk/` – konseptgrafikk og toppgrafikk
- `docs/03-kildekart.md` – tabeller, struktur, testede metoder, kontroller, hull
- `docs/04-byggenotat.md` – hva som er bygget, test, kontroller, nye valg

## Bygg og oppdatering
Fra roten av repoet:
```
python naturregnskap/scripts/hent_data.py   # henter data/raw/ på nytt fra PxWebApi v2
python felles/bygg.py naturregnskap         # kjører lag_data.py (med kontroller) og skriver index.html
python naturregnskap/scripts/test_side.py   # valgfritt: Playwright i 1280 og 390 px
```
`lag_data.py` stopper bygget hvis summene eller totalindeksene ikke går opp.

## Kilder
SSB, statistikkbanken: tabell 14967, 14968, 14994, 14996, 14998, 15012–15016, 15036 og 15038 (publisert 25.11.2026). Tabell 14852, 14995, 14997, 14999 og 15000 er hentet og brukt i kontrollene. Rådataene i `data/raw/` er hentet 27.11.2026 direkte fra API-et, ikke rekonstruert. Kodelister fra KLASS i `data/klass/`.
Fordelingen av indikatorer på tilstandsegenskap for skog og fjell: Miljødirektoratet/NINA, «Økologisk tilstand for skog» og «… for fjell» (utkast 01.10.2026).
Kvalitetsvurderingen av tjenestene: SSBs metodenotat, tabell 3.7.1. Ikoner: Lucide (ISC-lisens). Fonter: Open Sans, Roboto og Roboto Condensed (SIL Open Font License 1.1).

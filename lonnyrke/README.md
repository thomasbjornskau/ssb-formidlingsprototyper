# Lønn i yrket ditt (`lonnyrke`)

> **Prototype.** Laget for å prøve ut formidling av statistikken. Ikke en offisiell SSB-publisering.

**Lenke:** https://thomasbjornskau.github.io/ssb-formidlingsprototyper/lonnyrke/

Et kommunikasjonsdashbord på ett skjermbilde, laget som gjennomgående eksempel i veileder E om dashbord i SSB («Hvordan bygger vi prototypen?»). Det er en forenklet variant av [`lonnansatt`](../lonnansatt/), som er den fullstendige formidlingsprototypen for lønn.

## Hva den svarer på

- Hva er median månedslønn i yrket ditt, og hvordan ligger det an mot alle yrker?
- Hvor stor er forskjellen mellom kvinner og menn i yrket, og hvordan har den utviklet seg siden 2016?
- Hvor ligger yrket blant alle yrker, både i lønnsnivå og i forskjellen mellom kvinner og menn?

Ett valg, yrke, styrer hele siden. Valget ligger i adressen (`#yrke=2223`).

## Dokumenter

- `docs/04-byggenotat.md`: hva som er bygget, kontrollene og valg til kvalitetssikring
- Innsikt, konseptgrafikk og kildekart: se `lonnansatt/docs/`

## Kilder og oppdatering

SSB, tabell 11418 (yrkesfordelt månedslønn). Rådataene er hentet direkte fra data.ssb.no 04.11.2026 med `scripts/hent_data.py` og ligger uendret i `data/raw/`.

```
python lonnyrke/scripts/hent_data.py
python felles/bygg.py lonnyrke
```

Konseptgrafikken er gjenbrukt fra `lonnansatt` uten endringer.

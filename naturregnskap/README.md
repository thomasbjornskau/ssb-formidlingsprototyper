# Naturregnskap – formidlingsprototype

**Prototype.** Laget for å prøve ut formidling av statistikken. Ikke en offisiell SSB-publisering.
**Alle tall er dummydata** fram til publiseringen 25. november 2026.

Svarer på: Hvor mye natur har vi? Hvordan har naturen det? Hva gir naturen oss? Hvor sikre er tallene?
Hele siden styres av valgt naturtype (`#oko=04` gir skog).

## Dokumenter
- `docs/01-innsikt.md` – statistikken, misforståelser (H1–H10), prioriterte spørsmål
- `docs/02-kvalitetssikring.md`, `docs/grafikk/` – konseptgrafikk og toppgrafikk
- `docs/03-kildekart.md` – tabeller, struktur, kontroller, hull
- `docs/04-byggenotat.md` – hva som er bygget, test, nye valg

## Bygg
```
python scripts/lag_dummy.py   # bare fram til 25.11 – lager data/raw/ med ekte koder og oppdiktede tall
python scripts/bygg.py        # kjører lag_data.py (med kontroller) og skriver index.html
```
Etter publisering: rett kodene i `data/kilder.json`, kjør `python scripts/hent_data.py`, deretter `bygg.py`.

## Kilder
SSB, statistikkbanken: tabell 14967, 14968, 14994, 14996, 14998, 15012–15016 og 15036 (ikke publisert per 10.11.2026). Kodelister fra KLASS (988, 939, 959, 966, 967, 992) i `data/klass/`.
Metodenotat og «Når naturen telles» (utkast v1). Ikoner: Lucide (ISC-lisens).

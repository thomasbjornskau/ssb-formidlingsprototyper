# Lønnsforskjeller mellom kvinner og menn (`lonnutforsk`)

> **Prototype.** Laget for å prøve ut formidling av statistikken. Ikke en offisiell SSB-publisering.

**Lenke:** https://thomasbjornskau.github.io/ssb-formidlingsprototyper/lonnutforsk/

Et utforskende dashbord, laget som internt eksempel i veileder E om dashbord i SSB. Brukerne er statistikere og analytikere som kjenner tallene. Dashbordet har sju faner, én per formål fra vedlegg B1 i veileder B, og felles valg for år, sektor, arbeidstid, mål og næring. Valgene ligger i adressen og kan deles.

| Fane | Formål | Svarer på |
|---|---|---|
| Næringer | Sammenligning | Hvor er forskjellen størst? |
| Over tid | Utvikling over tid | Hvordan har forskjellen endret seg i hver sektor? |
| Lønnens deler | Del av helhet | Ligger forskjellen i avtalt lønn, tillegg eller bonus? |
| Spredning etter alder | Fordeling | Hvordan er spredningen for kvinner og menn i hver aldersgruppe? |
| Kvinneandel | Sammenheng | Er forskjellen større der det er få kvinner? |
| Yrke og næring | Sammenligning i to dimensjoner | Hvor er forskjellen innenfor samme yrkesgruppe og næring? |
| Yrker over tid | Rangering og avvik | Hvilke yrker har endret seg mest siden 2016? |

Kommunikasjonsdashbordet for publikum er [`lonnyrke`](../lonnyrke/).

## Kilder og oppdatering

SSB, tabell 11421, 11419 og 11418. Rådataene er hentet direkte fra data.ssb.no 04.11.2026 og ligger uendret i `data/raw/`.

```
python lonnutforsk/scripts/hent_data.py
python felles/bygg.py lonnutforsk
```

I veileder E er dette eksempelet beskrevet som et Dash-dashbord på Dapla. Denne versjonen er en statisk HTML-side som viser samme innhold, og kan brukes som spesifikasjon for en Dash-versjon.

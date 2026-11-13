Steg 3 i formidlingsprototype for likekom · versjon 0.1 · 13.11.2026 · Status: utkast

# Kildekart

Steg 1 er ikke gjort. Spørsmålene under er arbeidsspørsmål fra filmen og grafikken i steg 2, ikke godkjente prioriteringer.

## Spørsmål, datasett og seksjon

| Spørsmål | Datasett | Tabell | Seksjon i prototypen |
|---|---|---|---|
| Hvor likestilte er vi? | `skar` | 09292 | Hode, toppgrafikk, «Tolv indikatorer, én ring» |
| Hva ligger bak skåren? | `grunnlag` | 09293 | Vippehuskene, kortet for valgt indikator |
| Hva har rørt seg siden 2008? | `skar`, `grunnlag` | 09292, 09293 | «Hva har rørt seg siden 2008?», tidsseriene i kortet |

Begge tabellene er oppdatert 20.01.2026 og hentet direkte fra PxWebApi v2 med `scripts/hent_data.py` 13.11.2026. Nye tall kommer 24.11.2026.

## Struktur, talt fra dataene

- 09292 har 12 statistikkvariabler (én skår per indikator), 17 år (2008–2024) og 979 regionkoder.
- 09293 har 20 statistikkvariabler: 8 par for kvinner og menn, 2 andeler (barnehage, fedrekvote) og 2 skårer (næringsstruktur, utdanningsprogram).
- Landstallene har ingen manglende verdier og ingen statussymboler.
- 8 av 12 indikatorer har ett tall for kvinner og ett for menn, og kan vises som vippehuske. 4 kan ikke det.

## Metoden er testet

Skåren er regnet på nytt fra grunnlagstallene for alle år, med metoden i Om statistikken, og sammenlignet med publisert skår.

| Type | Indikatorer | Metode | Største avvik |
|---|---|---|---|
| Fordeling | Kommunestyre, offentlig sektor, privat sektor, ledere | min(kvinner, menn) / 50 | Innenfor 0,011, med ett unntak |
| Forhold | Utdanningsnivå, arbeidsstyrke, inntekt, deltid | min(kvinner/menn, menn/kvinner) | 0,0053 (utdanningsnivå 2020) |
| Andel | Barnehage, fedrekvote | andel / 100 | Innenfor 0,011 |
| Skår | Næringsstruktur, utdanningsprogram | samme tall i begge tabeller | Innenfor 0,011 |

Kvinner og menn summerer til 100 prosent (± 0,1) i alle fordelingene, alle år.

**Ett avvik:** Kommunestyre 2010. Grunnlagstallene er 38,2 prosent kvinner, som gir 0,76. Publisert skår er 0,75, som i 2008 og 2009. Kvinneandelen 38,2 står i 09293 fra 2010, året før valget i 2011. Prototypen viser publisert skår.

## Datamengde og valg

| Alternativ | Celler | Gjør mulig |
|---|---|---|
| **Valgt: hele landet, alle år** | 544 | Ringen, vippehuskene og tidsseriene. 8 kB i `index.html` |
| Fylker i tillegg | ca. 8 700 | Sammenligning mellom fylker |
| Alle kommuner, alle år | ca. 530 000 | «Min kommune». Krever opprydding i 979 regionkoder og kommunesammenslåinger |

Valgt av Claude 13.11.2026 etter Thomas' føring «vi må starte med landsbildet». Kommunenivået er neste utvidelse.

## Hull og hindre

1. Kommunestyre 2010: de to tabellene stemmer ikke overens (se over).
2. Arbeidsstyrke: Om statistikken oppgir brudd i 2017. Grunnlagstallene hopper fra 2014 til 2015 (menn 83,1 til 77,1 prosent). Prototypen merker bruddet i 2015.
3. Deltid: bruddet er i 2015. Om statistikken sier at definisjonen gjelder 2008–2014 og fra 2016, så 2015 er et overgangsår.
4. Fedrekvote: brudd i 2013, og nytt datagrunnlag fra 2019-kullet. Prototypen merker bare 2013.
5. Næringsstruktur og utdanningsprogram har ikke grunnlagstall i 09293. De vises som «bare skår».
6. 09293 har tallet 0,6 der 09292 har 0,60, altså færre desimaler i noen år for de to skår-indikatorene.
7. Kommunenivået er ikke hentet. Tabellene har 979 regionkoder med både gamle og nye kommuner.

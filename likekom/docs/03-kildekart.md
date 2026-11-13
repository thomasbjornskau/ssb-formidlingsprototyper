Steg 3 i formidlingsprototype for likekom · versjon 0.2 · 13.11.2026 · Status: utkast

# Kildekart

## Spørsmål, datasett og seksjon

| Nr | Spørsmål | Datasett | Tabell | Seksjon i prototypen |
|---|---|---|---|---|
| 1 | Hvor likestilte er vi, i landet og i min kommune? | `skar` | 09292 | Hode med kommunevelger, ringen |
| 2 | Hva ligger bak skåren? | `grunnlag` | 09293 | Vippehuskene, kortet for valgt indikator |
| 3 | Hvordan ligger kommunen an mot landet og andre? | `skar`, `klass_kommuner`, `klass_fylker` | 09292, Klass 131 og 104 | Stiplet landslinje, «Hvor i landet?» |
| 4 | Hva har endret seg siden 2008? | `skar`, `grunnlag` | 09292, 09293 | «Hva har rørt seg siden 2008?», tidsseriene i kortet |

Alt er hentet direkte fra API-ene med `scripts/hent_data.py` 13.11.2026. Tabellene er oppdatert 20.01.2026. Nye tall kommer 24.11.2026.

## Struktur, talt fra dataene

- Begge tabellene har 979 regionkoder: landet, 41 tosifrede fylkeskoder og 936 firesifrede kommunekoder, gamle og nye, og koden «0716u» for Våle (til 2001).
- I 2024 har 357 kommuner og 15 fylker tall. Alle 357 finnes i kartet.
- Tidsseriene ligger på koden som gjaldt hvert år. Av dagens 357 kommunenummer har bare 83 tall for alle år, 242 fra 2020 og alle 357 fra 2024.
- Statussymboler: «.» (koden gjaldt ikke) 111 948 ganger i 09292, og «..» (tall mangler) 1 370 ganger. I 09293: 187 560 og 1 418.
- 8 av 12 indikatorer har ett tall for kvinner og ett for menn. 2 er andeler, og 2 har bare skår.

## Lenking av tidsserier

Klass 131 har 516 endringer i kommuneinndelingen 2008–2024, og Klass 104 har 24 for fylkene. En serie lenkes bakover bare når endringen er ren omnummerering: én gammel kode til én ny. Ved sammenslåing eller deling stopper serien.

| Serien starter | Kommuner |
|---|---|
| 2008 | 307 |
| 2012–2018 | 6 |
| 2020 | 42 |
| 2024 | 2 |

For fylkene har Oslo, Rogaland, Møre og Romsdal og Nordland hel serie. Trøndelag har fra 2018, Innlandet, Agder og Vestland fra 2020, og de sju andre bare 2024. Østfold og de andre fylkene som ble gjenopprettet i 2024, lenkes ikke til fylkene før 2020, fordi Klass viser deling av Viken.

Med lenking har 312 av 373 områder hel serie. Innenfor seriene mangler 147 skårer («..»).

## Metoden er testet

Skåren er regnet på nytt fra grunnlagstallene og sammenlignet med publisert skår.

| Nivå | Resultat |
|---|---|
| Hele landet, alle år | Største avvik 0,0053 (utdanningsnivå 2020). Ett avvik over 0,011: kommunestyre 2010 |
| Kommuner og fylker, alle år | 129 avvik over 0,05, alle for offentlig sektor i 2012. Ingen andre |

Kvinner og menn summerer til 100 prosent (± 0,1) i alle fordelinger, alle områder og år.

## Datamengde og valg

| Alternativ | Tall i `index.html` | Gjør mulig |
|---|---|---|
| Bare landet | 544 | Landsbildet |
| **Valgt: landet, 15 fylker og 357 kommuner, alle år** | ca. 190 000, 791 kB | Kommunevelger, kart alle år, tidsserier per kommune |
| Bare siste år for kommunene | ca. 11 000 | Kart og kommunevelger, men ingen tidsserie for kommunen |

Valgt av Claude 13.11.2026 etter Thomas' ønske om kommunevelger og kart. `index.html` er 1,3 MB, og kartet er 123 kB av det.

## Kart

Kommunegrenser fra Kartverket (CC BY 4.0), hentet fra `github.com/robhop/fylker-og-kommuner` (Kommuner-S, 2024). `scripts/lag_kart.py` projiserer og forenkler til `src/kart.json`. Rådataene ligger i `data/raw/kommuner-S.geojson`.

## Hull og hindre

1. Kommunestyre 2010, hele landet: grunnlagstallene gir 0,76, publisert skår er 0,75.
2. Offentlig sektor 2012: i 129 kommuner og fylker stemmer ikke skår og grunnlagstall overens. Eksempel: Bardu, der grunnlagstallene gir 1,00 og publisert skår er 0,54. Landstallet stemmer.
3. Arbeidsstyrke: Om statistikken oppgir brudd i 2017, grunnlagstallene hopper i 2015.
4. Deltid: 2015 er et overgangsår mellom to definisjoner.
5. Fedrekvote: nytt datagrunnlag fra 2019-kullet er ikke merket, bare bruddet i 2013.
6. Næringsstruktur og utdanningsprogram har ikke grunnlagstall i 09293.
7. 50 kommuner og 11 fylker har ikke hel tidsserie på grunn av grenseendringer.
8. Klass viser ikke grensejusteringer. En kommune kan ha fått justert grensene uten at serien brytes her.
9. Det er ikke kjent om hver indikator følger bosted eller arbeidssted.
10. Kartfilen er hentet fra en tredjepart. Den bør byttes med en fil hentet direkte fra Kartverket.

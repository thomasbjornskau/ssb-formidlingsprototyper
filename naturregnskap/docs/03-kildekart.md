Steg 3 i formidlingsprototype for naturregnskap · versjon 0.2 · 10.11.2026 · Status: utkast (dummydata med ekte kodelister)

# Kildekart

Tabellene publiseres 25.11.2026. Siden 10.11 bruker dummydataene **ekte kodelister fra KLASS**, hentet fra data.ssb.no/api/klass 10.11.2026 og lagret i `data/klass/`. **Tallene er fortsatt oppdiktet.** Det samme gjelder koblingen mellom indikator, økosystem og egenskap. Strukturen bygger på tabelltitlene og fagseksjonens svar 10.11.2026.

## Spørsmål → tabell → seksjon

| Spørsmål | Tabell | Seksjon |
|---|---|---|
| Hvordan har naturen det? (toppgrafikk B) | 15012, 15013 og 15016: totalindeks som egen indikatorkode | Toppgrafikk, kort for valgt naturtype |
| Hvor mye natur har vi? | 15036, hovedøkosystemer, status | «Hvor mye natur har vi?» |
| Hvor mye er bygd ut? | Ikke avklart. Foreløpige tall 2018–2024 | samme |
| Hvilke målinger trekker opp og ned? | 15012–15016, indikatorer gruppert etter egenskap | «Hvordan har naturen det?» |
| Forskjell mellom landsdeler? | 15012, 15013 (totalindeks) og 15015 (Naturindeks) | samme |
| Hva gir naturen oss? | 14967, åtte tjenester | «Hva gir naturen oss?» |
| Endringer i karbonlager | 14998, EU-økosystemtyper | samme |
| Hvem bruker tjenestene? | 14968, anvendelse etter KLASS 992 | samme |
| Utvikling over tid | 14994, 14996 | samme |
| Hvor sikre er tallene? | Metodenotatet, tabell 3.7.1 (ekte) | «Hvor sikre er tallene?» |

Ikke brukt: 15034 (EU-typer per kommune), 14852, 14995, 14997, 14999 og 15000.

## Struktur, talt fra KLASS og dummydataene

- **Hovedøkosystemer:** 11 koder fra variant 3622. Kodene er sammensatte: 02-03, 05.1+06.1, 05.2+06.2, 10+12.1 og 12.2. Adressen bruker dem kodet, for eksempel `#oko=05.1%2B06.1`.
- **EU-typer:** 12 på nivå 1 (versjon 3621). Hovedøkosystemer kobles til EU-typer ved å lese kodene. Fjell og åpent lavland deler EU-typene 05 og 06. Kystvann og åpent hav deler EU-type 12.
- **Indikatorer:** 85 koder i KLASS 959. Dummydataene bruker 85 indikatorverdier fordelt på 9 hovedøkosystemer.
- **Tilstandsegenskaper:** 6 koder (966). Landsdeler: 5 koder (967). Koden for hele landet («0») er antatt.
- **Anvendelse:** 5 koder (992), også bruttoinvestering i fast realkapital.
- **Tjenester:** KLASS 939 har 9 tjenester på nivå 1. Global klimaregulering har to variabler: 05.01 årlige endringer i karbonlager og 05.02 karbonlager.

## Kontroller (i `lag_data.py`)

| Kontroll | Toleranse | Største avvik |
|---|---|---|
| Kodene i 15036 er de samme som i KLASS-varianten for hovedøkosystemer | – | ok |
| Alle indikatorkoder finnes i KLASS 959 | – | ok |
| Sum av areal = I alt (15036) | under 1 (1000 ha) | 0 |
| Sum av utbygd areal = I alt | under 1 ha | 0 |
| Totalindeks = snitt av egenskaper, der egenskap = snitt av indikatorene (metode fra [K1]) | 0,006 | 0,0042 |
| Alle tilstandsverdier ligger mellom 0 og 1 | – | ok |
| Sum av tilgang = I alt (14967), og sum av endring = I alt (14998) | 0,1 % | 0 |
| Anvendelse i alt (14968) = tilgang i alt (14967 og 14998) | 0,1 % | 0 |

Negativ test: én indikatorverdi i 15012 ble senket med 0,3. Bygget stoppet med «totalindeks 0.51 ≠ beregnet 0.460».

## Hull og hindre

1. Tallene er dummy. Koblingen mellom indikator, økosystem og egenskap er gjettet.
2. Tabellnummeret for utbygging er ikke avklart.
3. Dimensjons-id-ene i `kilder.json` er gjettet. Det gjelder også koden for hele landet i tilstandstabellene.
4. Det er usikkert om metodekontrollen for totalindeksen holder for de ekte tallene. Vekting og manglende indikatorer kan gi avvik.
5. Nevneren for «andel av landarealet» er ikke bekreftet.
6. Det er ikke avklart om temperaturregulering i grader kan summeres over økosystemer.
7. Det er ikke avklart om usikkerhetsintervallene for tilstand finnes i tabellene. Prototypen viser dem ikke.

Steg 3 i formidlingsprototype for naturregnskap · versjon 0.1 · 05.11.2026 · Status: utkast (dummydata)

# Kildekart

**Viktig:** Tabellene er ikke publisert. data.ssb.no svarer «Non-existent table» (testet 05.11.2026). Alle kodelister og tall i `data/raw/` er **oppdiktet** av `scripts/lag_dummy.py` etter tabelltitlene i Thomas' skjermbilde. Strukturen er en kvalifisert gjetning, og den må kontrolleres mot de ekte tabellene 25.11.

## Spørsmål → datasett → seksjon

| Spørsmål | Datasett | Tabell | Seksjon i prototypen |
|---|---|---|---|
| Hvordan har naturen det? (toppgrafikk B) | totalindeks per økosystem | 15012, 15013, 15015, 15016 | Toppgrafikk, kort for valgt naturtype |
| Hvor mye natur har vi? | areal, utbygd areal | utbredelse (nummer ukjent) | «Hvor mye natur har vi?» |
| Hva trekker opp og ned? | egenskaper | 15012–15016 | «Hvordan har naturen det?» |
| Forskjell mellom landsdeler? | totalindeks per landsdel | 15012, 15013, 15015 | samme |
| Hva gir naturen oss? | tilgang per økosystem | 14967 | «Hva gir naturen oss?» |
| Hvem bruker tjenestene? | anvendelse | 14968 | samme |
| Utvikling over tid | avlinger, tømmer | 14994, 14996 | samme |
| Hvor sikre er tallene? | kvalitetsvurdering | metodenotatet, tabell 3.7.1 (ekte) | «Hvor sikre er tallene?» |

Ikke brukt: 14852 (uskalert), 14995, 14997, 14999 og 15000 (detaljer per avlingstype, landsdel og by). De passer under «Kan vente».

## Struktur i dummydataene (talt)

- 11 økosystemtyper, kodet 01–11, pluss «00 I alt». Andelen av landarealet regnes av 01–09 (land og ferskvann), som er 31,18 millioner hektar.
- Tilstand per økosystem:

  | Type | Antall | Økosystemer | Tabell |
  |---|---|---|---|
  | Totalindeks | 5 | skog, fjell, elver, innsjøer, kystvann | – |
  | Naturindeks | 1 | våtmark | – |
  | Egenskaper uten totalindeks | 2 | jordbruksmark, åpent lavland | – |
  | Bare uskalerte variabler | 1 | bebygd | 14852 |
  | Ingenting | 2 | kyststrender, hav | – |

- Landsdel finnes bare for skog, fjell og våtmark. 2019 finnes for de samme tre.
- Tjenestene bruker 9 koder og 9 ulike enheter. Én tjeneste har tilgang fra mellom 1 og 7 økosystemtyper.
- Anvendelse fordeles på 4 brukere: næringer, husholdninger, offentlig forvaltning og eksport.
- Statussymboler: utbygging av bebygd areal, kystvann og hav er satt til «.» (kan ikke forekomme). Totalindeksen for jordbruksmark og lavland er også «.».

## Kontroller (i `lag_data.py`)

| Kontroll | Toleranse | Største avvik |
|---|---|---|
| Sum av areal per økosystem = I alt | under 1 (1000 ha) | 0 |
| Sum av utbygd areal = I alt | under 1 ha | 0 |
| Totalindeks = snitt av egenskaper | 0,006 (to desimaler) | 0,0033 |
| Tilstand per landsdel ligger mellom 0 og 1 | – | ok |
| Sum av tilgang = I alt per tjeneste (14967) | 0,1 % | 0 |
| Tilgang i alt = anvendelse i alt (14967 mot 14968) | 0,1 % | 0 |
| Sum av anvendelse = I alt (14968) | 0,1 % | 0 |

Negativ test: én tilgangsverdi i 14967 ble økt med 50. Bygget stoppet med «Kontroll feilet: 14967 AVL: sum tilgang 4250 ≠ I alt 4200». Filen er satt tilbake.

## Datamengde og strategi

Rådataene er på omtrent 1 000 celler. `build/naturregnskap.json` er 6,5 kB, og `index.html` er 149 kB, mest innbakte fonter. Alt bakes inn i siden. Valgt 05.11.2026, uten valgpunkt, fordi omfanget er lite.

## Hull og hindre

1. Tabellene er ikke publisert. Alle tall og koder er dummy.
2. Utbredelsestabellen er ikke identifisert.
3. Klimaregulering, turisme og rekreasjon har ingen egne tabeller. Vi antar at de ligger i 14967 og 14968.
4. Nevneren for «andel av landarealet» er ikke bekreftet.
5. Det er ukjent om totalindeksen ligger som egen kode, eller om den må regnes ut.
6. Det er ikke kjent om temperaturregulering (°C) kan summeres over økosystemer, slik dummydataene gjør.
7. Enheten for klimaregulering er ikke bekreftet: CO₂-ekvivalenter eller karbon.
8. `hent_data.py` er skrevet på nytt, fordi repoet ikke er tilgjengelig. Kodene i `kilder.json` må rettes.

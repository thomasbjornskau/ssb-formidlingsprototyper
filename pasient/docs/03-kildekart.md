`Steg 3 i formidlingsprototype for pasient · versjon 1.0 · 02.11.2026 · Status: godkjent av Thomas`

> **Godkjent 02.11.2026.** Thomas valgte middels omfang: alle sju mål per diagnosekapittel, kjønn og alder for hele landet, pasienter per kategoriblokk, rater etter innvandringskategori og psykisk helsevern for voksne. Region er utelatt.

# Kildekart: Pasienter i spesialisthelsetjenesten

Alle tabeller er oppdatert 22.06.2026 (07459: 25.02.2026). Rådataene i `data/raw/` er hentet 02.11.2026 direkte fra PxWebApi v2 med `scripts/hent_data.py` og er API-svarene uendret. Spørringene står i `data/kilder.json`.

## 1. Spørsmål, datasett og seksjon

| Spørsmål (fra steg 1) | Datasett | Tabell | Seksjon i prototypen |
|---|---|---|---|
| 1 Hvor mange får behandling, og hva får de? | `somatikk_kapittel` | 14824 | Toppgrafikk A og «Hva får pasientene?» |
| 2 Hvem er pasientene? | `somatikk_kapittel`, `somatikk_rate`, `folkemengde` | 14824, 14827, 07459 | «Hvem er pasientene?», med dekomponeringen fra variant C |
| 3 Hva behandles de for? | `somatikk_kapittel`, `somatikk_blokk` | 14824 | «Hva behandles de for?», variant B med blokkene under valgt kapittel |
| 4 Bruker innvandrere og barna deres tjenestene annerledes? | `somatikk_rate`, `psykisk_rate` | 14827, 14823 | «Innvandringsbakgrunn» |
| 5 Psykisk helsevern for voksne: hva skjer med de unge? | `psykisk`, `psykisk_rate` | 14820, 14823 | «Psykisk helsevern for voksne» |

Funnet, men ikke brukt: 14821 og 14822 (psykisk helsevern etter innvandringskategori og landbakgrunn), 14825 og 14826 (somatikk etter innvandringskategori med bosted, og landbakgrunn). De kan bli en senere seksjon om landbakgrunn. 14022 (kostnader) hører til `speshelse`.

## 2. Struktur som former prototypen

**Diagnosehierarkiet (14824), talt fra kodene:**

| Nivå | Antall | Merknad |
|---|---|---|
| I alt | 1 | `_T` |
| Kapittel | 20 + «Annen» | I–XIX og XXI. XX (ytre årsaker) og U-koder ligger i «Annen» (`zz1`) |
| Kategoriblokk | 200 | Fra 4 (II, VIII) til 21 (I, XIX) per kapittel. XIX har 10 S-blokker og 11 T-blokker |
| Sum | 222 | Stemmer med metadataene |

Blokkene står ikke alltid under kapitlet sitt i kodelisten: D00–D48 står etter III, men hører til II (svulster). Hierarkiet leses derfor fra kodespennet i `lag_data.py`, ikke fra rekkefølgen. Én kode har et uvanlig format: `T4n-T50`. «Annen» og «I alt» har ingen blokker.

**Historikk.** Alle 222 koder har tall for alle år 2015–2025. Ingen `..` eller `.` i noen av de hentede utsnittene. P00–P04 er 0 i 2024 og 2025, som ekte null etter avrunding.

**Psykisk helsevern for voksne** har fem aldersgrupper (i alt, 18–29, 30–49, 50–66, 67+) og ingen diagnose.

**Region (ikke hentet).** 14824 og 14820 har tre generasjoner fylker der 0 betyr at fylket ikke fantes. Bare Oslo, Rogaland, Møre og Romsdal og Nordland har hele serien. Helseregionene (4) har hele perioden.

## 3. Metoder som er testet

| Metode | Test | Resultat |
|---|---|---|
| Mengdetall summerer over kapitlene | Sum av 20 kapitler + Annen mot «I alt», 2025 | Kontakter, døgnopphold og oppholdsdøgn: avvik 0. Dagbehandlinger: −6 (avrunding) |
| Pasienter summerer ikke over kapitlene | Samme | 5 157 357 mot 2 716 218, faktor 1,90 |
| Kjønn summerer til begge kjønn | 2025 | 1 484 946 + 1 231 272 = 2 716 218, avvik 0 |
| Alder summerer til alle aldre | 2025 | Avvik 0 |
| Middelfolkemengde som snitt av 1. januar i året og året etter | Gjenskape publisert rate for «I alt» og alle kapitler i 14827, 2015–2025 | Treffer innenfor avrunding (±0,51) for alle kapitler og år, unntatt XV |
| Grafikkutkastet i steg 2 | Kjørt på nytt med API-rådata for 07459 i stedet for avskrift | SVG-ene er identiske |

## 4. Kontroller (kjøres i `lag_data.py`)

| # | Kontroll | Toleranse | Grunnlag |
|---|---|---|---|
| D1 | Kontakter, døgnopphold og oppholdsdøgn summerer over kapitlene | 36 per år og mål | 21 celler avrundet til base 6. Største faktiske avvik er 18 (døgnopphold og oppholdsdøgn 2016); 2025 alene viste bare 6 |
| D2 | Dagbehandlinger summerer over kapitlene | 36 | Samme. Største faktiske avvik 6 |
| D3 | Kvinner + menn = begge kjønn, alle mål, kapitler og aldre | Pasienter 9, mengdetall 18 | Base 3/6. Største faktiske avvik 6 og 12 |
| D4 | Sum av aldersgrupper = alle aldre | Pasienter 18, mengdetall 36 | Sju grupper, base 3/6. Største faktiske avvik 9 og 18 |
| D5 | Blokkene i hvert kapittel finnes og er minst like store som største blokk | Eksakt | Unik telling |
| D6 | Egen rate per kapittel treffer publisert rate i 14827, alle år | 0,55 (XV: 1,5) | Publisert rate er heltall. Største avvik 0,51 (XXI 2024). XV (svangerskap og fødsel) ligger 0–1,4 under publisert, se hull 8 |
| D7 | Antall kapitler = 20, antall blokker = 200 | Eksakt | Tellingen over |

## 5. Datamengde og strategi

| Datasett | Celler |
|---|---|
| `somatikk_kapittel` | 40 656 |
| `somatikk_blokk` | 2 442 |
| `somatikk_rate` | 5 808 |
| `psykisk` | 660 |
| `psykisk_rate` | 264 |
| `folkemengde` | 1 272 |
| **Sum** | **51 102** |

Alt bakes inn i `index.html` som kompakte matriser. Anslag: 350–450 kB data. Valgt 02.11.2026: middels.

## 6. Hull og hindre

1. **Ingen rater per aldersgruppe eller kjønn per kapittel i SSBs tabeller.** Seksjonen «Hvem er pasientene?» regner dem selv (G17–G19). Metoden gjenskaper de publiserte totalratene.
2. **Ingen diagnoser i psykisk helsevern.** Kapittelvelgeren virker ikke der, og prototypen må si det.
3. **Aldersjusteringen er uavklart over tid** (spørsmål 2 i innsiktsnotatet). Prototypen viser aldersjusterte rater bare mellom grupper i samme år.
4. **Kodebrudd i noen blokker** (O60–O75, P00–P04, R95–R99). Vises med merknad når blokken er valgt.
5. **Nevneren for raten i psykisk helsevern** er ikke bekreftet (hele befolkningen eller 18+).
6. **Avtalespesialister** er ikke hentet. Overlappet mellom aktørene (650 211 personer i 2025) står bare i lesehjelpen.
7. **Nøkkeltabellen på ssb.no** avviker med 3 fra statistikkbanken på to tall (spørsmål 3 i innsiktsnotatet). Prototypen bruker statistikkbanken.
8. **Raten for svangerskap og fødsel (XV) kan ikke gjenskapes.** Egen beregning ligger 0–1,4 per 1 000 under publisert rate hvert år (2025: 10,9 mot 12). Kanskje en annen nevner eller et annet pasientutvalg. Prototypen bruker publisert rate og spør fag.

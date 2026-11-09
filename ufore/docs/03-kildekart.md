Steg 3 i formidlingsprototype for ufore · versjon 0.2 · 09.11.2026 · Status: godkjent av Thomas (dataomfang stor)

# Kildekart

Bygger på de godkjente spørsmålene i `01-innsikt.md` (gjennomgående valg: alder) og toppgrafikk A fra steg 2. All data er hentet direkte fra data.ssb.no (PxWebApi v2) 09.11.2026, med ekte statussymboler. SSB-tilkoblingen er ikke brukt.

## 1. Spørsmål, tabell og seksjon

| Spørsmål | Datasett | Tabell | Seksjon i prototypen |
|---|---|---|---|
| 1 Hvor mange, og blir det flere? | antall og andel etter kjønn, 2015–2025 | 11695 | Toppgrafikk A |
| 1 | bosatt og ikke bosatt | 11824 | Lesehjelp: Slik lages tallene |
| 1 | befolkning 18–67 år etter ettårig alder og kjønn, 1.1.2016–2026 | 07459 | Toppgrafikk A (dekomponering), nevner |
| 2 Hvem, etter alder? | uføretrygdede etter kjønn og ettårig alder, 2015–2025 | 11828 | Aldersvelgeren (gjennomgående) |
| 2 | nye uføretrygdede etter kjønn og alder | 11736 | Aldersseksjonen |
| 3 Jobber uføre? | arbeidsintensitet etter kjønn og alder | 11850 | Arbeid |
| 3 | uføregrad etter kjønn og alder | 11696 | Arbeid |
| 4 Utdanning | uføretrygdede etter kjønn, alder og utdanningsnivå | 11714 | Utdanning |
| 5 Min kommune | antall og andel etter kjønn, kommuner og fylker | 11695 (K) | Kommune og fylke |
| 5 | befolkning etter kommune og ettårig alder | 07459 | Aldersjustert indeks per kommune |
| 5 | kommuneendringer | Klass 131 | Bare ved tidsserie per kommune |
| Kan vente | lavinntekt for uføretrygdede (2015–2024) | 13094 | Eventuelt inntekt |

Ikke brukt: tabellene 11079, 11096–11116 og 11108–11113 (2006–2014, avsluttet før uførereformen) og 13653–13661 (funksjonsnedsettelse, annen populasjon).

## 2. Struktur som former prototypen

**Alder.** 11828 har 50 ettårige aldre (18–67) pluss totalen, for kvinner, menn og begge, alle år 2015–2025. Ingen statussymboler. Kjønnene summerer til totalen i alle celler. Aldersgruppene i de andre tabellene er ulike: 11850, 11714 og 11733 har 7 grupper (18–24 … 62–67), 11736 har 8 (18–19 og 20–24 skilt), 11696 og 11857 har 6 (18–34 samlet). Aldersvelgeren må derfor slå opp riktig gruppe per tabell.

**Regioner.** 11695 har 979 regionkoder: 1 land, 41 fylkeskoder og 937 kommunekoder, inkludert historiske og «uoppgitt». Hvert år bruker kommunelisten det året. Gyldige per år, talt fra statussymbolene i andelen:

| År | Kommuner | Fylker |
|---|---|---|
| 2015 | 428 | 19 |
| 2019 | 422 | 18 |
| 2020–2023 | 356 | 11 |
| 2024–2025 | 357 | 15 |

**Fallgruve: 0 betyr ikke null.** For regioner som ikke fantes et år, er antallet 0 uten statussymbol, mens andelen har «.» (kan ikke forekomme). 18 981 av 32 307 andelsceller har «.». Gyldige regioner må derfor velges fra andelens status, aldri fra antallet.

**Kommuneendringer 2016–2024** (Klass 131): 506 kodeendringer, flest i 2020 (317) og 2024 (118). Fire delinger: Stokke 2017, Tysfjord 2020, Snillfjord 2020 og Ålesund/Haram 2024. Kommunene som kom ut av delingene, kan ikke få tidsserie før delingen.

**Små kommuner.** Minste antall i 2025: Utsira 16, Røyrvik 22, Modalen 24. Ingen celler med 0–3 for kjønn i 2025, så konfidensialitetsavrundingen synes ikke på kommunenivå, men andeler i små kommuner er ustabile.

## 3. Metoder testet

**M1 Nevneren (G5 bekreftet).** Andelen er antall / bosatte i samme kjønn og alder per 1.1. året etter (07459). Gjenskapt for alle 1 650 celler i 11828 (3 kjønn × 50 aldre × 11 år) og alle 357 kommuner i 2025: ingen avvik over 0,05 prosentpoeng.

| År | Uføretrygdede | Befolkning 18–67 | Egen andel | Publisert |
|---|---|---|---|---|
| 2015 | 327 992 | 3 397 264 | 9,65 | 9,7 |
| 2020 | 370 049 | 3 486 076 | 10,62 | 10,6 |
| 2025 | 389 023 | 3 626 571 | 10,73 | 10,7 |

**M2 Summer.** Kommuner summerer til fylker og fylker til landet uten avvik i 2025 (389 023). Kvinner + menn = begge kjønn i alle 979 regioner.

**M3 Dekomponering av +61 031 (2015–2025), G9.** Endringen deles i befolkningsvekst (N), alderssammensetning (s) og andel per alder (r). Resultatet avhenger av rekkefølgen:

| Rekkefølge | Vekst | Aldring | Andel per alder |
|---|---|---|---|
| N → s → r (brukt i steg 2) | 22 139 | 11 427 | 27 465 |
| N → r → s | 22 139 | 10 511 | 28 381 |
| s → N → r | 22 861 | 10 704 | 27 465 |
| s → r → N | 24 598 | 10 704 | 25 729 |
| r → N → s | 23 933 | 10 511 | 26 586 |
| r → s → N | 24 598 | 9 847 | 26 586 |
| **Snitt av alle seks** | **23 378** | **10 618** | **27 036** |

Anbefaling: bruk snittet av alle rekkefølger (Shapley-dekomponering, symmetrisk og uavhengig av rekkefølge), avrundet til nærmeste tusen i grafikken: 23 000, 11 000 og 27 000. Budskapet tåler alle rekkefølgene: 55–58 prosent av økningen skyldes befolkningsvekst og aldring. Toppgrafikk A rettes til dette i steg 4.

**M4 Aldersjustert indeks per kommune (indirekte standardisering).** Forventet antall = landets andel per ettårig alder × kommunens befolkning i hver alder. Indeks = faktisk / forventet × 100. 100 betyr samme nivå som landet når alderen er tatt hensyn til.

| Kommune | Andel | Forventet ut fra alder | Indeks |
|---|---|---|---|
| Bærum | 5,4 | 11,2 | 48 |
| Oslo | 6,6 | 9,4 | 70 |
| Bergen | 8,1 | 10,0 | 81 |
| Trondheim | 9,1 | 9,6 | 95 |
| Hamar | 11,8 | 11,0 | 107 |
| Kristiansand | 12,6 | 10,3 | 122 |
| Kongsvinger | 17,4 | 11,8 | 147 |
| Iveland | 22,1 | 11,2 | 196 |

**Funn som endrer H8:** alderssammensetningen forklarer bare om lag en firedel av forskjellene mellom kommunene (korrelasjon 0,49 mellom forventet og faktisk andel). Oslo er lavt også etter justering. H8 i innsiktsnotatet («mye skyldes alderssammensetning») er for sterk og må skrives om: alder forklarer en del, men store forskjeller står igjen. Indeksen er egen beregning og må godkjennes av fag.

## 4. Datamengde

| Datasett | Tabell | Celler |
|---|---|---|
| Landsnivå: andel og antall | 11695 | 66 |
| Bosettingsstatus | 11824 | 33 |
| Ettårig alder × kjønn | 11828 | 3 366 |
| Befolkning land, alder × kjønn | 07459 | 1 100 |
| Arbeidsintensitet | 11850 (land) | 2 310 |
| Uføregrad | 11696 (land) | 1 584 |
| Utdanning | 11714 | 2 310 |
| Nye uføretrygdede | 11736 (land) | 528 |
| **Sum landsnivå** | | **11 297** |
| Kommuner og fylker, kjønn, 2024–2025 | 11695 (K) | 4 476 |
| Uføregrad per kommune 2025 | 11720 (K) | 2 984 |
| Befolkning per kommune × alder × kjønn, 1.1.2026 | 07459 | 35 700 |
| Alle regioner 2015–2025 | 11695 (K) | 64 614 |
| Befolkning per kommune × alder, 2016–2026 | 07459 | om lag 393 000 i flere spørringer |

Alle spørringer er under grensen på 800 000 celler. Lange regionlister må sendes som POST, fordi URL-en blir for lang (404). Innbakt i `index.html` lagres bare det som vises (andeler, antall og indekser), ikke befolkningen per alder.

## 5. Hull og hindre

1. Dekomponeringen (M3) og den aldersjusterte indeksen (M4) er egne beregninger. SSB publiserer ingen av dem.
2. Kommuneserier før 2024 krever omkoding gjennom Klass. Kommunene fra de fire delingene får ikke tall før delingen.
3. Andeler i små kommuner er ustabile. Iveland (189 uføretrygdede) har høyeste indeks.
4. Aldersgruppene er ulike mellom tabellene (6, 7 eller 8 grupper).
5. Antall 0 for regioner som ikke fantes, uten statussymbol (se fallgruve over).
6. `hent_data.py` er skrevet for ufore fordi datasettene for befolkning per kommune må sendes som POST. Den leser `kilder.json` på samme måte som i de andre prototypene.

## 6. Valg av dataomfang

**Valg 09.11.2026: Stor.** Landsnivå, kommuner og fylker 2015–2025 omkodet til 2025-inndeling gjennom Klass, og aldersjustert indeks per kommune. Begrunnelse fra Thomas: kommunefordelingen er svært relevant.

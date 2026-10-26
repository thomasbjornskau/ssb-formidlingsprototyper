Steg 3 i formidlingsprototype for innvbef · versjon 1.0 · 26.10.2026 · Status: godkjent av Thomas

# Kildekart

Bygger på de fire spørsmålene i `01-innsikt.md` og valgene i steg 2: toppgrafikk B med veksling mellom absolutte og relative tall, landbakgrunn som gjennomgående valg, de seks kategoriene lenger ned, og en seksjon med de 30 kombinasjonene i tabell 12548.

## 1. Spørsmål, tabell og seksjon

| Seksjon i prototypen | Spørsmål | Datasett | Tabell | Periode |
|---|---|---|---|---|
| Toppgrafikk, absolutt | 2. Hvordan har antallet endret seg? | `kategorier_tid` | 05182 | 1970, 1980, 1986–2026 |
| Toppgrafikk, relativ (til 100 prosent) | 2 | `kategorier_tid` + `folkemengde` | 05182, 05803 | som over |
| Hvem regnes med (seks kategorier) | 1. Hvem regnes som innvandrer? | `kategorier_tid` | 05182 | som over |
| De 30 kombinasjonene | 1 | `tre_generasjoner` | 12548 | 2004–2026 |
| Regnskapet: inn, ut, født, død | 2 | `endringer`, `endringer_land` | 10516, 10518 | 2011–2025 |
| Landbakgrunn over tid (valgt land) | 3. Hvor kommer de fra? | `land_tid` | 13880 (og 05183 før 2004) | 2004–2026 |
| Botid for valgt land | 3 | `land_botid` | 10598 | 2026 |
| Hvor bor de (valgt land per kommune) | 4. Hvor bor de? | `kommune_land` + `kommune_bef` | 09817, 07459 | 2026 |
| Hvor bor de (utvikling i kommunen) | 4 | `kommune_tid` | 09817 | 2010–2026, se fallgruve |

**Ikke brukt:** 05183 er bare nødvendig hvis landserien skal gå tilbake til 1970 (bare totalen for innvandrere og norskfødte, ikke delt). 07108 og 07111 (verdensdel per kommune og fylke) erstattes av 09817. 12610, 05752 og 13882 (bydeler i Oslo) står under «Kan vente». Framskrivingstabellene (14740–14743) er utenfor.

## 2. Struktur som former prototypen

**Tabell 12548 har 30 grupper pluss total:** eget fødested (Norge, utlandet) × antall utenlandsfødte foreldre (0, 1, 2) × antall utenlandsfødte besteforeldre (0–4). Talt fra metadataene, 2 × 3 × 5 = 30. Ingen gruppe er tom i 2026, men fire har under 100 personer (talt).

**12548 lar seg ikke summere til de seks kategoriene i 05182.** Kontrollert for 2026:

| | 05182 | Summert fra 12548 | Differanse |
|---|---:|---:|---:|
| Innvandrere | 987 120 | 987 120 (124) | 0 |
| Norskfødte med innvandrerforeldre | 238 507 | 238 507 (024) | 0 |
| Født i Norge, to norskfødte foreldre | 4 003 379 | 3 967 957 (000–004) | +35 422 |
| Norskfødte med én utenlandsfødt forelder | 317 386 | 344 909 (010–014) | −27 523 |
| Utenlandsfødte med to norskfødte foreldre | 39 163 | 37 759 (100–104) | +1 404 |
| Utenlandsfødte med én norskfødt forelder | 41 845 | 41 631 (110–114) | +214 |
| Ikke plassert: født i Norge, to utenlandsfødte foreldre, færre enn fire utenlandsfødte besteforeldre | | 7 899 (020–023) | |
| Ikke plassert: født i utlandet, samme | | 1 618 (120–123) | |

Summene for født i Norge (4 559 272) og født i utlandet (1 068 128) stemmer begge veier. Det er fordelingen innenfor dem som er ulik. [T] Den seksdelte standarden ser ut til å bruke foreldrenes *innvandringskategori*, ikke bare fødested: en forelder født i utlandet av norske foreldre teller trolig som norsk. Det forklarer at 27 523 flyttes fra «én utenlandsfødt forelder» til «to norskfødte foreldre». Dette er ikke bekreftet og er hull H1 nedenfor.

Konsekvens for seksjonen: de seks brede gruppene kan ikke vises som summer av de 30. De må komme fra 05182, med en forklaring på at de to tabellene bruker ulike regler. Alternativt viser vi 12548s egne seks naturlige grupper (eget fødested × antall utenlandsfødte foreldre), som summerer riktig, men som ikke er SSBs standardkategorier.

**Brudd i 2016 i 12548.** Flere grupper hopper fra 2015 til 2016: 024 (norskfødte med innvandrerforeldre) øker med 14 074 mot rundt 9 500 i årene før, og 101, 102 og 113 faller med 20–60 prosent. Hoppet i 024 står også i 05182. [T] Trolig bedre kobling til foreldre i registeret. Må markeres som brudd i tidsserien hvis fag bekrefter det (hull H2).

**05182 før 1986.** Bare 1970 og 1980 finnes før årlige tall fra 1986. Tegnes prikket, som i grafikkutkastet. «Om statistikken» sier sammenlignbart fra 1995 (hull H3).

**Landbakgrunn.** 13880 har 252 landkoder, 05183 har 276 og 09817 250. Kodelistene er ikke like. Antall land med personer i 2026 telles når rådataene er hentet. Koder for land som ikke lenger finnes (Sovjetunionen, Jugoslavia, Serbia og Montenegro) har null i 2026, mens Serbia og Montenegro hadde 8 840 innvandrere i 2004. Valgt land må derfor ha en merknad når serien har slike brudd.

## 3. Kontroller som er kjørt

| Kontroll | Resultat |
|---|---|
| Summen av de 30 gruppene i 12548 = «Befolkningen i alt», alle år 2004–2026 | OK |
| 12548 «Befolkningen i alt» = 05803 befolkning 1. januar (2004, 2016, 2026) | OK |
| 12548 kode 124 = innvandrere i 05182, kode 024 = norskfødte med innvandrerforeldre (2026) | OK |
| 05182 fem kategorier + 4 003 379 = folkemengden 5 627 400 (2026) | OK |
| 12548 summert til seks kategorier = 05182 | **Avvik**, se tabellen over |
| 13880 innvandrere + norskfødte = 05183 for de ti største landene (2026) | OK |
| Regnskap 10516 for innvandrere 2025: 965 113 + 49 179 − 24 407 − 2 860 + 1 = 987 026, tilvekst 22 007 | Rest 94, ikke forklart |
| 10516: utgang − inngang = folketilvekst, alle kategorier | OK 2016–2025. **Avvik** 2011–2015 (innvandrere −6 766 i 2013) |
| 10516: inngang for innvandrere = 05182 samme år (2011, 2015, 2016, 2025) | OK |
| 09817: summen av landbakgrunner = «Alle land», per kommune og kategori | Største avvik 3 (avrundede småceller) |
| 09817: «Norden, EU/EFTA …» + «Europa utenom EU/EFTA …» = «Alle land» | Største avvik 1 |
| 09817: kommunene + 9999 = landet 2026 | Innvandrere OK. Norskfødte 238 508 mot 238 507 |
| 09817: publisert andel = antall / folkemengde fra 07459, 2026 | Største avvik 0,00 prosentpoeng |
| 10598: botid summert per land = innvandrere i 13880 | Største avvik 11 (land 296, 41 avrundede celler) |
| 13880: summen av land = landet (2004, 2016, 2026) | Største avvik 2 |

## 4. Datamengde

**Valg (Thomas, 26.10.2026):** stort omfang. Alle kommuner × alle landbakgrunner for 2026. Seksjonen om tre generasjoner bruker 12548s egne seks grupper. Rådataene er hentet direkte fra API-et med `scripts/hent_data.py`, ikke rekonstruert: data.ssb.no svarte fra arbeidsområdet denne dagen.

| Datasett | Celler | Ca. størrelse i `index.html` |
|---|---:|---:|
| `kategorier_tid` (05182, hele landet, 5 kategorier, 43 år) + `folkemengde` (05803, 57 år) | 272 | 3 kB |
| `tre_generasjoner` (12548, 31 grupper, 23 år) | 713 | 6 kB |
| `endringer` (10516) + `endringer_land` (10518, 31 land og grupper) | 5 130 | 35 kB |
| `land_tid` (13880, 252 land, innvandrere og norskfødte, 2004–2026) | 11 592 | 70 kB |
| `land_botid` (10598, 247 land × 41 botidsår, 2026) | 10 127 | 60 kB |
| `kommune_tid` (hentet: 3 kategorier × 2 variabler): 357 kommuner, innvandrere og norskfødte, alle land samlet, antall og andel, 2010–2026 | 36 516 | 150 kB |
| `kommune_land`: 358 regioner (med 9999) × 2 × 250 landbakgrunner, 2026 | 179 000 | 1–1,5 MB, før bortfall av nuller |
| `kommune_bef` (07459, 2026) | 360 | 5 kB |

Alle spørringer er langt under API-grensen på 800 000 celler.

## 5. Hull og hindre

| # | Hull | Går videre til |
|---|---|---|
| H1 | Hvorfor 12548 og 05182 fordeler ulikt innenfor født i Norge og født i utlandet | Fag, før seksjonen om de 30 gruppene bygges |
| H2 | Brudd i 2016 i 12548 og 05182 | Fag |
| H3 | Sammenlignbarhet for 1970 og 1980 | Fag |
| H4 | Restposten 94 i regnskapet for innvandrere 2025, og én fødsel blant innvandrere | Fag |
| H5 | Landkoder som skifter (Serbia og Montenegro, Sovjetunionen) | Merknad i prototypen |
| H6 | 10518 har bare 24 enkeltland. For andre land finnes ikke regnskap | Seksjonen viser regnskap bare der det finnes |
| H7 | Regnskapet i 10516 går ikke opp i 2011–2015 | Vises fra 2016. Fag |
| H8 | Kommuneserier i 09817 er ikke harmonisert: 115 kommuner har tall bare fra 2024, 129 fra 2020 | Prototypen viser «tall for dagens kommune finnes fra …». Fag: finnes en tabell med sammenslåtte tidsserier? |
| H9 | Ukraina og Syria mangler i 10518 før 2021 | «Mangler data» |
| H10 | 215 landkoder har personer i 2026 (13880). Innsiktsnotatet sa 216, rettet | — |

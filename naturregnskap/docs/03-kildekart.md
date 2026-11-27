Steg 3 i formidlingsprototype for naturregnskap · versjon 1.0 · 27.11.2026 · Status: utkast (ekte tall, publisert 25.11.2026)

# Kildekart

Tabellene ble publisert 25.11.2026. Rådataene i `data/raw/` ble hentet 27.11.2026 med `scripts/hent_data.py` direkte fra PxWebApi v2, så statussymbolene er ekte. Dummydataene fra versjon 0.2 er tatt vare på utenfor repoet og brukes ikke lenger. `lag_dummy.py` kan slettes i steg 4.

## Spørsmål → tabell → seksjon

| Spørsmål | Tabell | Seksjon |
|---|---|---|
| Hvordan har naturen det? (toppgrafikk B) | 15012, 15013, 15016: totalindeks som egen indikatorkode. 15014: naturindeks for åpent lavland. 15015: våtmark | Toppgrafikk, kort for valgt naturtype |
| Hvor mye natur har vi? | 15036, hovedøkosystemer, hele landet | «Hvor mye natur har vi?» |
| Hvor mye er bygd ut? | **15038**, endring til bebygd areal 2018–2024 etter fra-økosystem, hele landet. Foreløpige tall | samme |
| Hvilke målinger trekker opp og ned? | 15012–15016, indikatorer gruppert etter egenskap | «Hvordan har naturen det?» |
| Forskjell mellom landsdeler? | 15012, 15013 (totalindeks), 15015 (våtmark) | samme |
| Hva gir naturen oss? | 14967, alle tjenester per hovedøkosystem | «Hva gir naturen oss?» |
| Flomdemping og luftrensing per landsdel | **15000**, **14997** | samme (nytt, valgfritt) |
| Endringer i karbonlager | 14998, 2010–2024, EU-typer | samme |
| Hvem bruker tjenestene? | 14968 | samme |
| Utvikling over tid | 14994 (avlinger 2010–2024), 14996 (tømmer 2015–2024) | samme |
| Hvor sikre er tallene? | Konfidensintervall i 15012, 15013, 15015. Usikkerhetsgrenser i 15014, 15016. Metodenotatet, tabell 3.7.1 | «Hvor sikre er tallene?» |

Hentet, men ikke planlagt brukt ennå: 14852 (uskalerte variabler, 25 tall), 14995 (pollinering per avlingstype), 14999 (kjøling i åtte byer). Ikke hentet: 15034 (EU-typer, 48 koder) og 15035 (Svalbard og Jan Mayen).

## Valg av dataomfang: kommunevalg

Thomas ønsket kommunevalg hvis tallene finnes (27.11.2026). **Det gjør de ikke.**

- 15036 har regiondimensjon med hele landet, 15 fylker og 357 kommuner (373 koder). Av 4 103 celler har 653 tall. Alle 642 tallene under landsnivå er **0**: åpent hav i innlandskommuner, kystvann i Innlandet og lignende. De andre 3 450 cellene er `..`.
- 15038 har 375 regionkoder og 6 000 celler, men bare 10 tall, alle for hele landet. Resten er `.` eller `..`.
- Alle andre tabeller har hele landet eller fem landsdeler.

**Valgt 27.11.2026:** hele landet og landsdeler. URL-ene for 15036 og 15038 henter bare `Region=0`. Hele uttrekket er 4 615 celler og 220 kB rådata, så det er ingen størrelsesgrense å ta hensyn til.

## Struktur, talt fra dataene

**Økosystemkodene er ulike i tabellene.** Dette er en fallgruve.

| Hovedøkosystem | 15036 (KLASS 3622) | Tjenestetabellene (14967, 15000 m.fl.) |
|---|---|---|
| Jordbruksmark | `02-03` | `02+03` |
| Fastmark i fjellet | `05.1+06.1` | `05.01+06.01` |
| Åpent lavland | `05.2+06.2` | `05.02+06.02` |
| Kystvann | `10+12.1` | `10+12.01` |
| Åpent hav | `12.2` | `12.02` |
| I alt | finnes ikke | `_T` |

Tjenestetabellene blander nasjonal typologi og EU-typologi i samme dimensjon (18 koder). Jordbruksmark er dyrket mark pluss grasmark. Fjell og åpent lavland er en annen inndeling av hei og buskmark og lite vegetert mark. Velg én typologi før summering. `lag_data.py` trenger en koblingstabell.

**Tilstand, antall indikatorer med tall for hele landet 2024 (utenom totalindeks og naturindeks):**

| Økosystem | Tabell | Indikatorer | Samleindeks | Landsdeler | 2019 |
|---|---|---|---|---|---|
| Skog | 15012 | 21 | Totalindeks 0,53 | ja | 17 av 21 indikatorer. Totalindeks `..` |
| Fastmark i fjellet | 15013 | 11 | Totalindeks 0,61 | ja | 7 av 11. Totalindeks `..` |
| Åpent lavland | 15014 | 11 | Naturindeks 0,45 | nei | nei |
| Jordbruksmark | 15014 | 2 (dagsommerfugler, humler) | ingen (`.`) | nei | nei |
| Våtmark | 15015 | ingen | én verdi, 0,64 | ja | ja, 0,66 |
| Elver, bekker og kanaler | 15016 | 13 | Totalindeks 0,75 | nei | nei |
| Innsjøer og vannmagasiner | 15016 | 10 | Totalindeks 0,87 | nei | nei |
| Kystvann | 15016 | 8, pluss to delindekser (ålegress, hardbunn) | Totalindeks 0,78 og naturindeks 0,77 | nei | nei |
| Bebygd, kyststrender, åpent hav | – | ingen | ingen | – | – |

- **Tilstandsegenskap er ikke en dimensjon i tabellene**, selv om tabelltitlene nevner den. Koblingen indikator → egenskap for skog og fjell er hentet fra Miljødirektoratets tilstandsrapporter [K2], [K3].
  - Skog: A1 (2), A2 (1), B1 (6), B2 (3), B3 (7), C1 (2).
  - Fjell: A1 (3), B1 (5), B2 (1), B3 (2).
  - Vassdrag og kystvann mangler koblingen.
- Indikatorkodene i tabellene (`NO_AIVS_001`, `indeks_skog`) er ikke de samme som i KLASS 3492 (`Indeks_skog`). Kontrollen «alle indikatorkoder finnes i KLASS» må skrives om eller fjernes.
- **Landsdeler:** koden `0` er «Hele Norge» i tilstands- og tjenestetabellene og «Hele landet» i arealtabellene. Landsdelene har kodene `1`–`5` (Øst, Sør, Vest, Midt, Nord). Nord mangler strukturelle egenskaper for fjell (reinlav `.`).
- **Statussymboler** (celler med symbol / celler i alt):
  - 15012: `..` 90, `.` 18 av 792.
  - 15013: `..` 90, `.` 6 av 432.
  - 15016: `.` 195 av 306. Det er kombinasjoner av indikator og økosystem som ikke finnes.
  - 14967: `..` 43, `.` 58 av 234.
  - 14998: `..` 184, `.` 30 av 390.
  - 14968: `..` 50 av 65. Anvendelse er bare oppgitt for 15 kombinasjoner.
- **Tidsserier:** avlinger 2010–2024, karbon 2010–2024 og tømmer 2015–2024. Tilstand har 2019 bare for noen indikatorer og for våtmark. Alt annet gjelder 2024.

## Metodene som er testet

**Totalindeks = snitt av egenskapene, der hver egenskap er snittet av sine indikatorer** (metodenotatet kap. 3.7 [K1], «Om statistikken» [K4]).

| Region | Skog publisert | Skog beregnet | Fjell publisert | Fjell beregnet |
|---|---|---|---|---|
| Hele Norge | 0,53 | 0,529 | 0,61 | 0,615 |
| Øst | 0,52 | 0,514 | 0,57 | 0,568 |
| Sør | 0,56 | 0,560 | 0,62 | 0,630 |
| Vest | 0,50 | 0,496 | 0,59 | 0,592 |
| Midt | 0,55 | 0,554 | 0,58 | 0,587 |
| Nord | 0,54 | 0,537 | 0,60 | 0,604 |

Største avvik er 0,0095 (fjell, Sør). Det skyldes at indikatorene er publisert med to desimaler. Et rent snitt av alle indikatorene gir 0,477 for skog og 0,568 for fjell, altså tydelig feil. Kontrollen settes til toleranse 0,01.

**Andel av arealet:** SSB bruker alle 11 hovedøkosystemer som nevner, 469 239 km², med kystvann og åpent hav. Skog utgjør 123 680 km², og 123 680 / 469 239 = 26,4 prosent, som stemmer med nøkkeltallet [K4]. Dummyen antok landarealet som nevner, og det var feil. Hovedøkosystemene unntatt kystvann og åpent hav summerer til 323 778 km².

## Kontroller (til `lag_data.py`)

| Kontroll | Resultat 27.11.2026 | Foreslått toleranse |
|---|---|---|
| Flomdemping: sum av 6 nasjonale typer = I alt (15000, 14967) | 154 328 = 154 328 | 0 |
| Flomdemping: sum av landsdeler = Hele Norge (15000) | størst +15 ha (I alt), skog +9 | 0,02 prosent (avrunding per landsdel) |
| Etterspørsel etter flomdemping: sum av landsdeler = Hele Norge | 292 984 = 292 984 | 0 |
| Utbygging: nasjonal sum = EU-sum (15038) | 237,56 og 237,55 km² | 0,05 km² |
| Jordbruksmark = dyrket mark + grasmark (15038) | 42,31 = 34,62 + 7,69 | 0,01 |
| Totalindeks skog og fjell = snitt av egenskaper, alle regioner | største avvik 0,0095 | 0,01 |
| Alle skalerte tilstandsverdier mellom 0 og 1 | ok | – |
| Tjenester i 14967: sum av nasjonale typer = I alt | ok for flomdemping, luftrensing, pollinering, tømmer og avlinger (avvik ≤ 1). Se hull 4 og 5 | 0,1 prosent per tjeneste, med unntak for turisme og rekreasjon |
| Kjøling i byer: sum av bidrag = I alt (14999) | 1,00 = 1 | 0,02 |

Negativ test kjøres i steg 4, når kontrollene er skrevet inn i `lag_data.py`.

## Konsekvenser for prototypen

1. **Toppgrafikk B kan ikke vise 2019 → 2024.** Totalindeksen for 2019 er `..` for både skog og fjell. «Om statistikken» sier at tilstandsindeksene bare er beregnet for 2024 [K4]. Dette besvarer punkt 8 i `02-kvalitetssikring.md`: nei. Toppgrafikken må vise 2024 alene, eventuelt med konfidensintervall.
2. **Andelene i «Hvor mye natur har vi?» må regnes med 469 239 km² som nevner**, slik SSB gjør.
3. **Utbygging er én sum for 2018–2024**, ikke en årlig serie. Det blir en fordeling på fra-økosystem: skog 155 av 238 km².
4. **Flomdemping og luftrensing finnes per landsdel.** Det er ikke nødvendig å bruke dem, men de passer til landsdelsvisningen.
5. **Kjøling i byer:** bruk «bidrag» (kan summeres), ikke «gjennomsnittlig kjøling» (kan ikke summeres) [14999, merknad].

## Hull og hindre

1. ~~Tallene er dummy.~~ Løst 27.11.2026.
2. ~~Tabellnummeret for utbygging er ikke avklart.~~ Løst: 15038.
3. ~~Dimensjons-id-ene er gjettet.~~ Løst. Kodene er ulike mellom tabellene (se over).
4. **Rekreasjon summerer ikke.** I alt er 599,05 millioner dagsturer, mens summen av typene er 639,25. Avviket på 40 millioner er for stort til å skyldes avrunding. Trolig kan én tur telle i flere økosystemer. Må bekreftes av fag.
5. **Karbonlager i 14967:** I alt (4 615 587) omfatter EU-typer som ikke har tall i den nasjonale typologien. Karbon bør fortsatt vises per EU-type fra 14998.
6. **Indikator → egenskap** er hentet fra Miljødirektoratets utkast til tilstandsrapporter (01.10.2026), ikke fra SSBs tabeller. Kontrollen bekrefter fordelingen for skog og fjell. For vassdrag og kystvann mangler koblingen, så indikatorene der vises ugruppert.
7. **Indikatorer med 2019-tall:** 17 av 21 for skog og 7 av 11 for fjell. Fjellrapporten sier at 2024 ikke kan sammenlignes med tidligere vurderinger fordi indikatorer og skaleringsverdier er endret [K3]. Prototypen bør ikke vise endring for indikatorene før fag har sagt om det er forsvarlig.
8. **Våtmark** har en verdi for 2019 og 2024 per landsdel, men den er en naturindeks for biologisk mangfold, ikke en totalindeks. Merkingen «bare biologisk mangfold» bør stå.
9. **Kommunetall** finnes i tabellstrukturen, men alle verdiene er 0 eller mangler. Ifølge fagseksjonens svar 10.11 kommer kommunetall for utbygging 26.02.2027.
10. **Temperaturregulering, EU-metode:** I alt er 0,78, mens summen av typene er 0,68. Prototypen bruker nasjonal metode.

## Kilder

- [K1] SSB: Metodenotat naturregnskap, utkast v1, kap. 3.7 Totalindekser.
- [K2] Miljødirektoratet/NINA: Økologisk tilstand for skog, utkast 01.10.2026. https://www.miljodirektoratet.no/globalassets/arrangementer/2026/oktober/okologisk-tilstand-for-skog_utkast_011026.pdf
- [K3] Miljødirektoratet/NINA: Økologisk tilstand for fjell, utkast 01.10.2026. https://www.miljodirektoratet.no/globalassets/arrangementer/2026/oktober/okologisk-tilstand-for-fjell_utkast_011026.pdf
- [K4] SSB: Naturregnskap, statistikkside og «Om statistikken» (sist oppdatert 24.11.2026), lest 27.11.2026 gjennom en oppsummering, ikke ordrett. https://www.ssb.no/natur-og-miljo/naturregnskap/statistikk/naturregnskap
- Statistikkbanken, tabell 14852, 14967, 14968, 14994–15000, 15012–15016, 15036 og 15038, oppdatert 25.11.2026, hentet 27.11.2026.

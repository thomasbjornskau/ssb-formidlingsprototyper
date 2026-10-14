Steg 3 i formidlingsprototype for muh · versjon 0.1 · 14.10.2026 · Status: utkast

# Kildekart: Utenrikshandel med varer (muh)

**Merkeforklaring.** `[K1]`–`[K12]` viser til kildelisten i `01-innsikt.md`. `[T]` er vår tolkning. Kontrollene K1–K10 kjøres med `scripts/kontroll_kilder.py`.

**Valg som ligger til grunn.** Toppgrafikk C (handelsbalansen og fastlandsbalansen) og konseptgrafikken er godkjent i steg 2. Landvalget er det fullverdige interaktive valget (14.10.2026). Dataomfanget for land er hvert år 2015–2025 med varegrupper for 2025 (valgt 14.10.2026).

## 1. Spørsmål, datasett og seksjon

| Spørsmål | Datasett | Tabell | Seksjon i prototypen |
|---|---|---|---|
| Toppgrafikk: hva forteller handelsoverskuddet? | `hovedtall_aar` | 08800 | Topp |
| 1 Hvor mye er olje og gass, hvor mye fastland? | `hovedtall_aar`, `hovedtall_mnd` | 08800, 08792 | Olje, gass og fastland |
| 2 Pris eller mengde? | `indekser` | 06322 | Pris eller mengde |
| 3 Handelsoverskuddet og fastlandsbalansen | `hovedtall_aar`, `hovedtall_mnd` | 08800, 08792 | Topp, utdypet i egen seksjon |
| 4 Hva eksporterer fastlands-Norge? | `varer_aar`, `land_varer` | 08819, 08809 | Hva fastlands-Norge selger |
| 5 Hvem handler Norge med? | `land_aar`, `land_varer` | 08804, 08809 | Velg et land |
| Lesehjelp: foreløpige tall | `revisjoner`, `hovedtall_mnd` | 12308, 08792 | Lesehjelp |

Alle tabeller er de nyeste i serien. Årstabellene ble sist oppdatert 15.05.2026, månedstabellene 15.09.2026. **Ikke brukt:** 08801/08799 (varenummer, for detaljert), 08806/08818 (månedlig etter SITC, ikke nødvendig når årstall er valgt), 08864 (sesongjustert, kan vente), 11356/11357 (næring og foretak, avsluttet 2015).

## 2. Struktur som former prototypen

**Land (08804).** 278 landkoder: 16 aggregater (verdensdeler, handelsområder og «Uspesifisert» 90), 13 historiske land uten tall i perioden (for eksempel Sovjetunionen og Øst-Tyskland), og 249 koder med tall. De 249 er 248 land og «Uspesifisert» (97). 230 land har handel minst ett år 2015–2025.

- **Handelen er konsentrert.** De ti største eksportlandene tok 80,9 prosent av eksporten i 2025. 199 land hadde eksport på minst 0,5 mill. kr, 172 hadde import.
- **Olje og gass gjør de store landene like.** Storbritannia, Tyskland, Frankrike, Belgia og Finland har alle 76–80 prosent olje og gass i eksporten. USA har 1,4 prosent. Bare 27 land fikk olje eller gass fra Norge i 2025.
- **Konsekvens for landvalget:** landlisten sorteres etter handel, ikke alfabetisk, og hvert land vises med og uten olje og gass (H5). Land med «0» må vises som «under 0,5 mill. kr», ikke som null.
- **Søk trenger synonymer.** Statistikkbanken bruker «Storbritannia», «USA», «Nederland» og «Tsjekkia». Folk skriver «England», «Amerika», «Holland». Synonymlisten lages i steg 4 (`data/synonymer.json`).

**Uspesifisert import.** Kode 97 har import fra 2023: 20 556 mill. kr i 2023, 23 973 i 2024 og 29 874 i 2025, 2,7 prosent av importen. Den er med i totalen, men ikke på noe land. Kode 90 har samme verdier, men er en gruppe. Bare 97 skal telles `[T]`.

**Aggregatene endrer innhold.** EU (03) følger medlemskapet hvert år. Eksporten til EU var 456 864 mill. kr i 2020, mens EU unntatt Storbritannia (16) var 440 408. Differansen er Storbritannias januar 2020 `[T]`. Kode 16 finnes fra 2017. OECD (04) er ikke det samme i 08804 og 08809 (1 508 846 og 1 624 084 mill. kr i 2025). Prototypen bruker derfor bare enkeltland og «Alle land».

**Varegrupper (08819).** 262 tresifrede SITC-grupper og «Varer i alt». Seks grupper hadde ingen eksport 2015–2025. **De tresifrede gruppene summerer ikke til totalen**: i 2025 manglet 16 790 mill. kr av eksporten, 16 711 i gruppe 5 Kjemiske produkter og 79 i gruppe 3. Avviket var 7 263–9 435 mill. kr i årene 2015–2020 og 12 744–21 597 mill. kr fra 2021. Ensifret SITC (08809) summerer. Andeler som skal gå opp i 100 lages derfor på ensifret nivå.

**Indekser (06322).** 81 varegrupper, 2000–2025, basis 2000 = 100. 140 tomme celler, alle i de publiserte endringsratene for år 2000, der det ikke finnes et år før.

**Revisjoner (12308).** Hver måned fra 2016 finnes slik den var ved første publisering, ved hver senere publisering i året, i mai året etter og endelig i mai to år etter. 14 publiseringstrinn.

## 3. Metoder som er testet

| # | Metode | Resultat |
|---|---|---|
| M1 | Fastlandseksport fra varegrupper: «Varer i alt» − 333 (råolje og kondensater) − 343 (naturgass) − skip og plattformer fra 08800 | Gjenskaper 08800 alle år 2015–2025, største avvik 0,8 mill. kr (K5). Bekrefter at 342 (propan og butan) og 351 (strøm) er med i fastlandseksporten. |
| M2 | Olje og gass per land: hentet direkte (Eoljegass), ikke regnet som eksport minus fastland | Identiteten eksport = fastland + olje og gass + skip og plattformer holder per land og år, største avvik 1 mill. kr (K2). |
| M3 | Fastlandsbalansen per land: fastlandseksport − (import − import av skip og plattformer) | Gjenskaper fastlandsbalansen for «Alle land» i 08800, største avvik 1 mill. kr (K3b). |
| M4 | Pris- og volumendring | Publiserte rater brukes. Rater regnet fra indeksene i 06322 avviker 0,0 prosentpoeng (K10). |
| M5 | Revisjonsstørrelse: første publiserte tall mot endelig tall, eksport i alt | Snitt absolutt revisjon 1,8–3,7 prosent i de fleste år, men 8,0 prosent i 2021 og 11,0 prosent i 2022. Største enkeltrevisjon +23,6 prosent (2021). Gasspriser med foreløpig pris er en sannsynlig årsak `[T]`. |

## 4. Kontroller

| # | Kontroll | Resultat |
|---|---|---|
| K1 | Sum av land = «Alle land» (08804), 6 strømmer, 11 år | OK, største avvik 9 mill. kr (avrunding av 249 tall) |
| K2 | Eksport = fastland + olje og gass + skip og plattformer per land og år | OK, største avvik 1 mill. kr |
| K3 | Handelsbalansen og fastlandsbalansen gjenskapes fra komponentene, 1960–2025 | OK, største avvik 1 mill. kr |
| K4 | «Alle land» i 08804 = 08800 | OK, ingen avvik |
| K5 | Fastlandseksport fra tresifret SITC = 08800 | OK, største avvik 0,8 mill. kr |
| K6 | Tresifret SITC mot totalen | Summerer ikke. Avviket (16 790 mill. kr i 2025) ligger på ensifret nivå og er kartlagt |
| K7 | Ensifret SITC summerer per land; total per enkeltland i 08809 = 08804 | OK, største avvik 2 tusen kr og 0,5 mill. kr |
| K8 | Månedene 2025 (08792) summerer til årstallet (08800) | OK, største avvik 2 mill. kr |
| K9 | Endelige månedstall (12308) summerer til årstallet, 2016–2024 | OK, største avvik 0,5 mill. kr |
| K10 | Rater fra indekser mot publiserte rater | Ingen avvik |
| K11 | Avskrevne CSV-svar mot maskinlest svar (08804) | 14 410 celler, ingen avvik. Rådataene er bygd fra det maskinleste svaret |

## 5. Datamengde og strategi

| Datasett | Celler | Rå fil |
|---|---|---|
| `hovedtall_aar` (08800) | 1 716 | 15 kB |
| `hovedtall_mnd` (08792) | 832 | 7 kB |
| `land_aar` (08804) | 18 348 | 98 kB |
| `land_varer` (08809) | 6 116 | 34 kB |
| `varer_aar` (08819) | 5 786 | 66 kB |
| `indekser` (06322) | 16 848 | 85 kB |
| `revisjoner` (12308) | 7 168 | 92 kB |
| Sum | 56 814 | 398 kB |

Alle spørringer er langt under API-grensen på 800 000 celler, og sju spørringer holder seg under 30 per minutt. Innbakt i `index.html` uten utvalg blir dataene om lag 280 kB: 100 kB for landvalget og 180 kB for de nasjonale seriene. Med utvalg i steg 4 (bare brukte indeksgrupper, bare de siste årene for varegruppene, bare totalene fra revisjonstabellen) bør det komme ned mot 150 kB. Valget av omfang for landene ble tatt 14.10.2026: hvert år 2015–2025 for alle land, varegrupper for 2025.

**Rådata.** Arbeidsområdet når ikke data.ssb.no. Alle tall er hentet gjennom SSB-tilkoblingen. Store svar ble lagret direkte til fil av tilkoblingen, slik at ingen tall i `data/raw/` er skrevet av for hånd. Filene er gjenoppbygd som json-stat2 med `note` om at de er rekonstruert. `scripts/hent_data.py` henter de samme datasettene direkte fra PxWebApi.

## 6. Hull og hindre

1. **URL-ene er ikke testet.** Arbeidsområdet når ikke data.ssb.no. URL-ene i `kilder.json` bruker `valueCodes[...]`, som er PxWebApi v2-formatet slik vi kjenner det. Tilkoblingens egen URL-generator bruker `selection[...]`. Første kjøring av `hent_data.py` må avgjøre hvilket som virker.
2. **Symbolene for tomme celler er delvis tapt.** Tilkoblingen gir tomme celler som `null` i json. I 08804 er `.` og `-` gjenopprettet fra CSV for alle celler der vi hadde CSV. 998 tomme celler (olje og gass og skip og plattformer for land uten slik eksport) og alle tomme celler i 08800, 06322, 08819 og 12308 har status `?`. `hent_data.py` henter dem riktig.
3. **«0» tolket som under 0,5 mill. kr** etter SSBs vanlige symbolbruk `[T]`. Ikke sjekket mot dagens «Om statistikken».
4. **Kode 90 mot 97.** Vi bruker 97 fordi den har tallet 0 der 90 har «.» for import av skip `[T]`. Fag bør bekrefte.
5. **Hvorfor «Uspesifisert» import fra 2023?** 29 874 mill. kr i 2025. Fag bør forklare, og prototypen må vise den som egen linje i landlisten.
6. **Hvorfor summerer ikke tresifret SITC?** 16 790 mill. kr av eksporten i 2025 finnes bare på ensifret nivå, nesten alt i kjemiske produkter. Konfidensialitet er en mulig forklaring `[T]`. Fag bør bekrefte før prototypen viser tresifrede grupper.
7. **OECD og andre aggregater er ulike mellom tabeller.** Ikke brukt.
8. **Månedstallene blir utdatert 15.10.2026**, dagen etter henting. `hent_data.py` kjøres på nytt før steg 4 bygges ferdig.
9. **Repoet mangler i arbeidsområdet.** `hent_data.py` er skrevet nytt, ikke kopiert fra en eksisterende prototype, og `felles/` er fortsatt midlertidig.
10. **Revisjonene i 2021–2022 er store.** Påstanden om at gasspriser er årsaken er vår tolkning og må prøves i fagkontrollen.

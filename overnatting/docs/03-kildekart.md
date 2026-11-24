Steg 3 i formidlingsprototype for overnatting · versjon 0.2 · 24.11.2026 · Status: utkast, dataomfang valgt av Thomas

# Kildekart: Overnattingar (overnatting)

**Merking.** `[K1]`–`[K14]` viser til kildelisten i `01-innsikt.md`, nye kilder [K15]–[K17] står nederst. `[T]` er vår tolkning. Kontrollene K1–K12 kjøres med `scripts/kontroll_kilder.py` på `data/raw/` og stopper bygget hvis en feiler. Alle gikk gjennom 24.11.2026.

**Valg som ligger til grunn.** Spørsmålene i `01-innsikt.md` er godkjent, med reiselivsregion (Reiselivsregionar 2024) som fullverdig valg (24.11.2026). Toppgrafikk A og konseptgrafikken er godkjent. C blir egen seksjon, B går inn i «Slik lages tallene» (24.11.2026). **Dataomfang: landtall per reiselivsregion for hele perioden fra 2018M01, fordi 24 måneder gir for kort trend (valgt av Thomas 24.11.2026).**

**Tilgang.** data.ssb.no svarte direkte 24.11.2026. Rådataene i `data/raw/` er hentet med `scripts/hent_data.py` (kopiert fra muh, utvidet med KLASS-filene) og har de ekte statussymbolene. KLASS-API-et svarte også. Eurostats API og public.tableau.com er sperret i arbeidsområdet.

---

## 1. Spørsmål, datasett og seksjon

| Spørsmål | Datasett | Tabell | Seksjon i prototypen |
|---|---|---|---|
| Topp A: rekord, men ikke opp | `hotell_formal`, `sesongjustert` | 14166, 14178 | Topp |
| 1 Hvordan går det nå? | `fylke_type`, `sesongjustert` | 14162, 14178 | Topp, utdypet i «Måned for måned» |
| 2 Hvem overnatter? (C) | `land_nasjonalt`, `region_land` | 14162, 14172 | Hvem overnatter |
| 3 Hvor og når, «Min reiselivsregion» | `region_tid`, KLASS 527, kart | 14172 | Min reiselivsregion |
| 4 Hva tjener hotellene, hvor fulle er de? | `region_hotell` | 14176 | Hotellene i regionen |
| 5 Hva teller statistikken? (B) | `reiseundersokelsen`, `fritidsbolig` | 11270, 13100 | Slik lages tallene |
| Lesehjelp: overnatting og gjest | `gjester` | 14165 | Lesehjelp |
| Lesehjelp: formål (kan vente) | `hotell_formal` | 14166 | Lesehjelp eller ute |

Alle tabeller er de nyeste i serien og ble oppdatert 4.11.2026, bortsett fra 11270 (27.8.2026) og årstabellene 14163/14167 (4.2.2026). **Ikke brukt:** 14163 og 14167 (årstall, gjenskapes fra månedene, se K8), 14177 (nøkkelindikatorer, har hatt to rettelser og trengs ikke), 14175 (formål per region, kan vente), 14179 (sesongjustert losjiomsetning, kan vente), 12894/12898 (kommune fra 2024, se H8), 14170/14171 (camping etter overnattingsmåte, kan vente). Eldre tabeller med 2020-inndelingen av reiselivsregioner brukes ikke.

---

## 2. Struktur som former prototypen

**Reiselivsregioner (KLASS 527, versjon 2024).** 66 regioner. 14172 og 14176 har nøyaktig de samme 66 kodene, pluss 0N og 16 fylker (83 regionkoder i alt). Ingen gamle koder, og hele serien fra 2016 er regnet om til 2024-inndelingen. Merknaden til 14172 advarer mot små feil til og med 2020 [K13].

**Kommune til region.** Korrespondansetabell 1512 i KLASS (Reiselivsregioner 2024 – Kommuneinndeling 2024) [K15]. Alle 357 kommuner har nøyaktig én region, og ingen region krysser fylkesgrensen (talt). 65 regioner har kommuner. Svalbard (21101) har ingen. Antall kommuner per region: 1–18. Sju regioner består av én kommune: Oslo, Bodø, Sarpsborg, Ringsaker, Trysil, Sunnfjord og Tromsø.

**Kart.** `innvbef-omrade/data/raw/kommuner2024-S.geojson` (robhop/fylker-og-kommuner, Kartverket 2024) har de samme 357 kommunene som KLASS. Regionene kan lages ved å slå sammen kommunene. Fylkesgeometrien har 15 fylker og **ikke Svalbard**. Svalbard må vises som eget felt [T].

**Undertrykking per region (14172).** Når «I alt» er undertrykt, er også Norge og utlandet det (alle 2 493 tilfeller). Andel undertrykte region-måneder, «I alt»:

| År | Hotell | Camping, hyttegrender og vandrerhjem |
|---|---|---|
| 2016 | 84 av 792 | 161 av 792 |
| 2020 | 91 av 792 | 183 av 792 |
| 2025 | 82 av 792 | 112 av 792 |
| 2026 (9 mnd) | 38 av 594 | 42 av 594 |

Regionen har ikke noe «alle innkvarteringstyper» i 14172. **Total for en region kan bare vises når begge gruppene er publisert** [T].

**Hele år per region er ofte ikke mulig.** Antall regioner (av 66) der alle tolv månedene er publisert:

| År | Hotell | Camping, hyttegrender og vandrerhjem | Begge |
|---|---|---|---|
| 2018 | 51 | 19 | 16 |
| 2022 | 51 | 39 | 32 |
| 2025 | 50 | 40 | 35 |

Konsekvens for «Min reiselivsregion»: månedsserien med synlige hull er grunnformen. Årstall og 12-månederssummer vises bare der alle månedene er publisert, og ellers med «:» og antall manglende måneder [T]. Dette er det viktigste designvalget i steg 4.

**Landtall per region undertrykkes ikke alene.** Når «Utlandet i alt» er publisert for en region og måned, er alle landene publisert (talt for 2018, 2022 og 2025). Det finnes altså ingen delvis skjulte landfordelinger. Er regionen synlig, er landene det også.

**Sekundær undertrykking virker.** I ingen fylke-måned er bare én region undertrykt mens fylket er publisert (talt for alle 16 fylker, 2 grupper og 129 måneder). Tallene kan ikke regnes tilbake fra fylket, og prototypen skal ikke prøve.

**Bostedsland (14162, 14172).** 74 koder: 3 aggregater (I alt, Utlandet i alt, Norge), 64 land, 5 restgrupper (Resten av Europa, Asia, Afrika, Sør-Amerika, Oseania), samt «Resten av Asia -2017» og «Uoppgitt», som bare har «.». **Landlisten ble utvidet i 2017 og 2018**: 24 land har 0, ikke «.», i alle måneder i 2016 (talt), for eksempel India, Kosovo og Thailand. Bulgaria, Kroatia og Romania har 0 også i 2017, og Israel har tall først fra august 2020. Nullene betyr «ikke målt», ikke «ingen gjester» [T]. **Landene summerer ikke til «Utlandet i alt» før 2018** (K3): i 2016 mangler 531 797 overnattinger (5,5 prosent av de utenlandske), i 2017 er 185 493 for mye (−1,9 prosent). Fra 2018 er avviket 0, bortsett fra 57 overnattinger i 2020. Konsekvens: **landtall vises fra 2018**. Utlandet i alt kan vises fra 2016.

**Hotellmål per region (14176).** Seks mål, samme 83 regioner. 74–97 region-måneder per mål undertrykt i 2025. Pris per rom = losjiomsetning / utleide rom, høyst 1 krone i avvik (K10). Kapasitetsutnytting finnes for senger og rom.

**Sesongjustert (14178).** Landet og 16 fylker, tre grupper (I alt, hotell, camping med mer), tre innhold (ujustert, sesongjustert, trend). For Østfold, Akershus, Oslo, Vestfold, Troms og Finnmark er I alt og camping-gruppen undertrykt i alle måneder. Bare hotell har sesongjusterte tall der. Ingen reiselivsregioner. SSBs navn på den glattede serien er «Trend».

**Reiseundersøkelsen (11270).** Kvartalstall i millioner, 16–79 år bosatt i Norge [K16]. «Annen kommersiell innkvartering» omfatter også leid privat feriebolig via formidler (Airbnb o.l.), cruise og ferger. «Ikke kommersiell» er egen fritidsbolig, slekt og venner og annet ubetalt (bobil, telt, båt utenfor organiserte plasser) [K16]. Hele reisen plasseres etter den innkvarteringen som ble brukt mest [K16].

**Gjester (14165).** Bekreftet i skjemaveiledningen RA-0366: personer telles per bestilling hos bedriften i måneden [K17]. En rundreise med flere bedrifter gir flere gjester. Dette er grunnlaget for eksempelet i konseptgrafikken (Q1 i `02-kvalitetssikring.md`).

---

## 3. Metoder som er testet

| # | Metode | Resultat |
|---|---|---|
| M1 | «Flest i en september noen gang»: september 2026 mot alle septembre 1986–2025 i 14166 | 2 579 128 er høyest. Deretter 2025 (2 510 517) og 2024. Bruddene i 1985 og 2020 er ikke korrigert for [T] |
| M2 | Sesongjustert endring fra forrige måned regnet fra publiserte nivåer i 14178 | −0,8 prosent august–september 2026. SSB publiserer ikke raten. Avklares med fag (A3) |
| M3 | Regionens total = hotell + camping-gruppen | Bare når begge er publisert. Ellers vises totalen som «:» |
| M4 | Land per region over 12 måneder: sum av månedene | Gyldig bare når alle 12 månedene er publisert. Ellers «:» [T] |
| M5 | Pris per rom og losjiomsetning per tilgjengelig rom | Publiserte tall brukes. Pris = losjiomsetning / utleide rom, avvik ≤ 1 kr (K10) |
| M6 | Endring fra samme måned i fjor | Regnes fra publiserte heltall, ikke avrundede tall. SSB publiserer ingen endringsrater i tabellene |

---

## 4. Kontroller

| # | Kontroll | Resultat |
|---|---|---|
| K1 | Hotell + camping + hyttegrender og vandrerhjem = I alt, landet, for I alt, Norge og utlandet, 2016–2026 (14162) | OK, avvik 0 |
| K2 | Norge + utlandet = I alt, alle regioner og måneder uten undertrykking (14172) | OK, avvik 0 |
| K3 | Sum av land og restgrupper = Utlandet i alt (14162), landet, alle grupper | **Avvik i 2016 (+531 797) og 2017 (−185 493).** OK fra 2018, bortsett fra 57 i 2020. Kontrollen krever samsvar fra 2018. Landtall vises fra 2018 |
| K4 | Sum av reiselivsregioner = fylket, når ingen region er undertrykt (14172) | OK, 2 928 fylke-måneder, avvik 0 |
| K5 | Aldri én undertrykt region alene i et publisert fylke (14172) | OK |
| K6 | 14178 «Ujustert» = 14162 | **Avvik i 2024M05** for landet og Møre og Romsdal, opptil 38 overnattinger: 14162 er rettet, 14178 ikke. Ujusterte tall hentes fra 14162. Kontrollen godtar bare dette kjente avviket |
| K7 | 14166 hotell i alt = 14162 hotell, 2016–2026, og formålene summerer | OK for totalen (avvik 0). Formålene summerer ikke i 10 enkeltmåneder (2005, 2013–2015, 2018), avvik opptil 99. Brukes bare som andeler |
| K8 | `region_land` (to deler) = `region_tid` for I alt, Norge og utlandet; land summerer til utlandet per region fra 2018 | OK, avvik 0. Landene summerer i 15 358 region-måneder, største avvik 57 |
| K9 | 66 regionkoder i 14172 og 14176 = KLASS 527 versjon 2024 | OK |
| K10 | Pris per rom = losjiomsetning / utleide rom (14176) | OK innenfor avrundingen. Losjiomsetning er i hele 1 000 kr, så små regioner kan avvike med noen kroner (største 2,71) |
| K11 | 357 kommuner i KLASS-korrespondansen = 357 i geometrien | OK |
| K12 | Tall i steg 1 og 2 gjenskapes fra rådataene | OK, 8 av 8 |
| – | Sum av måneder = årstall i 14163, 2016–2025 | OK, avvik 0 (kjørt mot API-et, 14163 hentes ikke) |

---

## 5. Datamengde

Målt 24.11.2026. API-grensen er 800 000 celler per spørring. **Valgt: alternativ 3 fra 2018 (Thomas, 24.11.2026).**

| Datasett | Tabell | Omfang | Celler | Rå fil |
|---|---|---|---|---|
| `region_tid` | 14172 | 83 regioner × 2 grupper × 3 (I alt, Norge, utlandet) × 2016M01– | 64 242 | 437 kB |
| `region_hotell` | 14176 | 83 regioner × 6 mål × 2016M01– | 64 242 | 353 kB |
| `fylke_type` | 14162 | 17 × 4 grupper × 3 × 2016M01– | 26 316 | 180 kB |
| `land_nasjonalt` | 14162 | landet × 4 grupper × 74 land × 2016M01– | 38 184 | 184 kB |
| `sesongjustert` | 14178 | 17 × 3 × 3 × 3 × 2016M01– | 59 211 | ca. 350 kB |
| `hotell_formal` | 14166 | landet × 4 formål × 1986M01– | 1 956 | ca. 15 kB |
| `gjester` | 14165 | landet × 4 × 3 × 2016M01– | 1 548 | ca. 12 kB |
| `fritidsbolig` | 13100 | landet × 3 × 2020M01– | 243 | ca. 3 kB |
| `reiseundersokelsen` | 11270 | 6 × innenlands × 2016K1– | ca. 250 | ca. 5 kB |
| `region_land` | 14172 | 83 × 2 × 74 land × **valgt periode** | se valget | |

`region_land` er det eneste datasettet der omfanget er et reelt valg:

| Alternativ | Periode | Celler | Rå fil | Gjør mulig |
|---|---|---|---|---|
| 1 | Ingen. Land bare for landet | 0 | 0 | C bare for hele landet |
| 2 | Siste 24 måneder (2024M10–2026M09) | 294 816 | ca. 1,3 MB | C per region: siste 12 måneder mot de 12 før, og topp land |
| 3 | Hele perioden fra 2018 (landtall er ikke konsistente før) | 1 289 820 | 8,2 MB, to spørringer | Landtrend per region over flere år. **Valgt** |

**Hentet 24.11.2026:** 11 datasett, 1 546 014 celler, 10,3 MB rådata, pluss KLASS (50 kB) og kartet (1,06 MB). `region_land` er delt i `region_land_a` (2018–2022, 737 040 celler, 4,9 MB) og `region_land_b` (fra 2023, 552 780 celler, 3,3 MB). Del b vokser med 12 284 celler per måned og når API-grensen etter om lag 20 måneder, sommeren 2028. Da må den deles igjen [T].

**Strategi for siden:** landtall per region legges inn som årssummer 2018–2025 og siste 12 måneder, bare der alle månedene er publisert, og bare for land og restgrupper med overnattinger. Anslått 83 × 2 × 71 × 9 ≈ 106 000 tall før nuller og hull fjernes, ca. 0,5 MB [T]. Kartet forenkles til regionene (ca. 0,2 MB). Anslått side: 1,3–1,6 MB. Tallene byttes ut med målte tall i byggenotatet.

Inn i `index.html` legges bearbeidede tall, ikke rådataene.

---

## 6. Hull og hindre

1. **Svalbard mangler i kartgrunnlaget.** Må vises som eget felt eller i listen.
2. **Plattformtall fra Eurostat** kan ikke hentes fra arbeidsområdet. Nyeste norske tall vi har er 6,4 millioner i 2023 [K6]. Eurostat har tall for 2024 og 2025, men ikke lest for Norge.
3. **Landtallene er ikke konsistente før 2018** (K3), og 24 land har 0 i 2016 fordi de ikke ble målt. Landtall vises fra 2018. Hva forklarer avviket i 2017? Spørsmål til fag.
4. **Totalt per region finnes ikke** i 14172 og må regnes som hotell + resten. Blir «:» når én av dem er undertrykt.
5. **Ny campingmetode fra februar 2026** er ikke markert i tabellene. Bruddet må legges inn av oss (H7, C2).
6. **Bruddet i 2020** (flere hotell) er ikke tallfestet (A4).
7. **Reiseundersøkelsen og overnattingsstatistikken** har ulike populasjoner (16–79 år mot alle gjester). Sammenligningen i B og konseptgrafikken må si det.
8. **Revisjon.** 14177 har hatt rettelser. 14172 og 14176 har ingen merknad om det. Vi henter alt på nytt før hver versjon.
9. **14178 har ikke fått rettelsen i 14162 for mai 2024** (K6). Spørsmål til fag om det også gjelder de sesongjusterte tallene.
10. **Hele år per region mangler ofte** (35 av 66 regioner i 2025). Prototypen må vise hull, ikke skjule regionene.
11. **Skjemaveiledningen** RA-0366 gjelder utleieenheter (hyttegrender med mer) og er fra august 2020. Veiledningene for hotell og camping er ikke lest.

---

## Nye kilder

- [K15] SSB KLASS, korrespondansetabell 1512: Reiselivsregioner 2024 – Kommuneinndeling 2024. https://data.ssb.no/api/klass/v1/correspondencetables/1512, hentet 24.11.2026.
- [K16] SSB: Reiseundersøkelsen, «Om statistikken», sist oppdatert 18.12.2025. https://www.ssb.no/reise
- [K17] SSB: Veiledning til utfylling av skjema RA-0366, Overnattingsvirksomhet i utleieenheter, august 2020. https://www.ssb.no/innrapportering/overnattinger/

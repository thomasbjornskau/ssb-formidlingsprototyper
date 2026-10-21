Steg 3 i formidlingsprototype for folkemengde · versjon 1.1 · 21.10.2026 · Status: godkjent av Thomas

# Kildekart: Befolkning (folkemengde)

Bygger på de godkjente spørsmålene i `01-innsikt.md` og grafikken fra steg 2 (toppgrafikk A med todeling, «Min kommune» som gjennomgående valg). Kildene `[K1]`–`[K10]` viser til innsiktsnotatet.

Rådataene er hentet direkte fra PxWebApi v2 med `scripts/hent_data.py`, etter at Thomas åpnet data.ssb.no for arbeidsområdet 21.10.2026. Det er første prototype der hentingen faktisk er kjørt. Statistikkbankens metadata bekrefter kortnavnet: tabell 05803 er knyttet til `KORTNAVN:folkemengde`.

## 1. Spørsmål, datasett og seksjoner

| Spørsmål (01-innsikt) | Datasett | Tabell | Seksjon i prototypen |
|---|---|---|---|
| 1 Hvor mange er vi, og hvor fort vokser vi? | `land_aar` | 05803 | Toppgrafikk, den lange linjen 1735–2026 |
| 1, 4 for Min kommune | `kommune_aar` | 06913 | Kommunens lange linje 1951–2026 |
| 2 Hva driver veksten? (år) | `land_aar`, `kommune_aar` | 05803, 06913 | Komponenter per år, fra 1951 |
| 2 Hva driver veksten? (kvartal) | `land_kvartal`, `kommune_kvartal` | 01222 | Kvartalsvisning med innvandring og innenlandsk flytting hver for seg |
| 3 Alderssammensetningen | `land_alder`, `kommune_alder` | 10211, 07459 | Befolkningspyramide: landet hvert år 1846–2026, kommunen 1986, 2006 og 2026 |
| 4 Hvor vokser det, og hvor krymper det? | `kommune_aar` | 06913 | Fordelingen av kommunenes vekst, med valgt kommune uthevet |
| Kommunevelgeren | `kommune_aar` (navn), Klass 131 | 06913, Klass | Søk på navn, tidligere navn og tospråklige navn |

**Brukes ikke:** 07459 med «Kommuner 2024, sammenslåtte tidsserier» for befolkningstotaler (06913 dekker 1951–2026, 07459 bare fra 1986). 09588 (flyttinger per kommune 2002–2025) har bare dagens inndeling uten sammenslåtte serier, med 0 før kommunen fantes. Splitten mellom innvandring og innenlandsk flytting hentes derfor fra kvartalstallene i 01222.

## 2. Strukturen som former prototypen

Alt er talt fra rådataene med `scripts/kontroll_kilder.py`.

**Kommuner.** 357 kommuner i 15 fylker. Innlandet har flest (46), Oslo én. 174 kommuner har under 5 000 innbyggere, 22 under 1 000. Utsira er minst (219), Oslo størst (728 714). Hver tabell har i tillegg 3–4 restkoder (delte kommuner og uoppgitt, Svalbard og Jan Mayen, kontinentalsokkelen).

**Historikk per kommune** (første år med befolkning over 0 i 06913):

| Fra | Antall | Kommuner |
|---|---|---|
| 1951 | 340 | |
| 1962–1977 | 12 | Dønna (1962); Vaksdal, Osterøy, Rauma, Averøy, Rana (1964); Moskenes (1976); Ringerike, Stryn, Sula, Brønnøy, Salangen (1977) |
| 2020 | 5 | Heim, Hitra, Orkland, Narvik, Hamarøy |

I tillegg har **ti kommuner 0 midt i serien**, fordi de var slått sammen med en nabo i en periode: Hole, Eidfjord, Sømna og Lavangen (1964–1976), Flakstad (1964–1975), Tolga og Os (1966–1975), Nord-Fron og Sør-Fron (1966–1976), Haram (2020–2023). Statistikkbanken skriver 0, ikke «.». Kommunevelgeren må vise disse årene som «kommunen fantes ikke». En linje som stuper til null, vil leses som at alle flyttet ut.

**Navn.** 29 kommuner har tospråklige navn i statistikkbanken, for eksempel «Trondheim - Tråante» og «Guovdageaidnu - Kautokeino». I innsiktsnotatet sto det 23. Det var talt for tidlig, og tallet er nå talt i rådataene. Klass 131 gir 559 kommuneendringer siden 1990. Av dem er laget 184 søkeord i `data/synonymer.json`, for eksempel Skedsmo → Lillestrøm og Oppegård → Nordre Follo. Åtte søkeord peker på flere kommuner. Tre av dem er riktige (Snillfjord → Heim, Hitra og Orkland; Tysfjord → Narvik og Hamarøy). Fem er trolig for brede (se hull H5).

**Landet.** Befolkningen finnes fra 1735, fødte og døde fra 1735, utvandring fra 1821, folketilvekst fra 1816 og innvandring fra 1951. Hele regnskapet kan derfor bare vises fra 1951. Aldersfordelingen finnes for hvert år fra 1846, med 106 alderskoder (0–104 og 105+).

**Kvartaler.** Kommunene har kvartalstall fra 1997K4. Prototypen henter fra 2016K1, altså 42 kvartaler. Det finnes ingen manglende celler. I 2. kvartal 2026 hadde 205 av 357 kommuner negativ nettoinnvandring, mot 148 i 2. kvartal 2025 og 85 i 3. kvartal 2025. Det støtter hypotesen om registeropprydding (H3), og vi har nå tall per kommune å vise den med.

## 3. Metoder og kontroller

`scripts/kontroll_kilder.py` kjører alle kontrollene og stopper med feilkode hvis en feiler. Resultat 21.10.2026: alle kontroller OK, med de kjente avvikene under listet eksplisitt.

| # | Kontroll | Resultat |
|---|---|---|
| K1 | Nøkkeltall 2025–2026 mot statistikksiden (5 627 400; 55 401 fødte; 45 040 døde; 55 243 innv.; 32 919 utv.; 33 060 vekst; korreksjon 375) | OK |
| K1d | Befolkning(t+1) − befolkning(t) = folketilvekst(t), alle år | OK, 0 avvik |
| K2 | 2026K2: utgang 5 636 904, vekst 3 134, nettoinnvandring −1 590 | OK |
| K2b | Negativ nettoinnvandring for landet bare i 2020K2, 2021K2 og 2026K2 | OK |
| K3 | Sum alder × kjønn (10211) = befolkning (05803) | 175 av 181 år OK. Avvik på −3 til +2 personer i 1863, 1864, 1973, 1988 og 1996, og **−3 000 i 1915** |
| K4b | Sum kommuner + restkoder = landet | OK hvert år fra 1971. I 1952–1970 avvik i 14 år, fra −2 565 til +3 294 |
| K4c | Ingen 0 midt i serien utenom de ti kjente | OK |
| K4e | 128 kommuner med nedgang i 2025 | OK |
| K5 | Sum kommuner = landet per kvartal for fødte, døde, innvandring og utvandring | OK, 0 avvik i 42 kvartaler |
| K5b | Innenlandsk innflytting = innenlandsk utflytting summert over kommunene | OK fra 2020. I 2016–2019 avvik på −17 til +226 per kvartal |
| K5c | Oslo, innvandring 2025 summert over kvartalene | 9 501, mot 9 484 som årstall i 09588 |
| K5d | Befolkning ved utgangen av 2025K4 = befolkning 1.1.2026 per kommune | OK, unntatt Indre Østfold (+29), Nordre Follo (−27) og Vestby (−2), som summerer til 0 |
| K6 | Sum aldersfordeling per kommune = landet (1986, 2006, 2026) og = kommunens total 2026 | OK |

**Kvartal mot år.** For 2025 gir kvartalene 55 381 fødte, 45 059 døde, 55 331 innvandringer og 32 991 utvandringer. Årstallene er 55 401, 45 040, 55 243 og 32 919. Per kommune avviker fødte i 31 kommuner (−4 til +2) og innflyttinger i 52 (−5 til +17). Prototypen bruker årstall for hele år og kvartalstall bare for kvartalsvisningen (fallgruve 3 i `kilder.json`).

**Korreksjon per kommune.** For 2025 er befolkningsendringen ulik fødte − døde + inn − ut i 206 av 357 kommuner. Summen er 375, som for landet. Størst er korreksjonen i Oslo (49), Trondheim (35) og Bergen (24). Den er liten, men komponentstolpene for en kommune vil ikke summere eksakt til veksten. Det må nevnes i grafikken, som i toppgrafikken.

## 4. Datamengde og strategi

Valgt av Thomas 21.10.2026: alternativ B.

| Datasett | Celler | Verdier som JSON |
|---|---|---|
| `land_aar` | 2 044 | 11 KB |
| `land_kvartal` | 805 | 4 KB |
| `land_alder` | 38 372 | 197 KB |
| `kommune_aar` | 137 180 | 517 KB |
| `kommune_kvartal` | 105 840 | 324 KB |
| `kommune_alder` | 45 360 | 151 KB |
| **Sum** | **329 601** | **om lag 1,2 MB** |

Det er mer enn de 280 000 cellene jeg anslo i valgpunktet. Grunnen er at hele aldersserien for landet (1846–2026) er tatt med, slik at pyramiden kan ha glidebryter for hvert år. Innbakt i `index.html` blir det trolig 1,2–1,4 MB. Steg 4 kan krympe det ved å fjerne restkoder og lagre kommuneseriene som heltall i kompakte lister.

Største spørring er 137 180 celler, godt under API-grensen på 800 000. Seks spørringer med tre sekunders pause tar om lag 20 sekunder.

## 5. Hull og hindre

- **H1. `selection[...]` virker ikke i de andre prototypene.** API-et ignorerer `selection[...]` og returnerer standardutvalget uten feilmelding. URL-ene i `kilder.json` for kpi, regfram, muh og lonnansatt bruker den syntaksen. Testet 21.10.2026: kpi får 8 × 1 × 3 celler mot 8 × 3 × 381 i repoet, lonnansatt får 407 × 1 × 1 × 2 × 3 mot 6 × 582 × 1 × 3 × 1 × 1 × 10. Rådataene i repoet er riktige, fordi de ble hentet gjennom tilkoblingen. Men kjører noen `hent_data.py` i de fire mappene, blir rådataene overskrevet med feil utvalg. `hent_data.py` sjekker bare at svaret er json-stat2, ikke størrelsen. Folkemengde bruker `valueCodes[...]`.
- **H2. Aldersfordelingen for 1915 avviker med 3 000 personer** fra befolkningen i 05803 (2 483 269 mot 2 486 269). Det ser ut som en tastefeil i én av tabellene. Spørsmål til fag.
- **H3. Kommunesummene i 1952–1970 stemmer ikke med landstallet.** Avviket er på inntil 3 294 personer. Den lange linjen for landet må derfor hentes fra 05803, og kommunetallene for disse årene bør merkes som mindre sikre. Spørsmål til fag.
- **H4. Grensejustering 1.1.2026** mellom Indre Østfold, Nordre Follo og Vestby er vår tolkning av avviket i K5d `[T]`. Den er ikke bekreftet.
- **H5. Fem synonymer er trolig for brede.** Skodje, Ørskog og Sandøy peker på både Ålesund og Haram. Klass følger koden for Ålesund 2020–2023, som ble delt i 2024. Det samme gjelder Stokke (Tønsberg og Sandefjord) og Varteig (Sarpsborg og Rakkestad), som trolig er grensejusteringer. Bør rettes for hånd i steg 4. Kommunevelgeren bør uansett si «tidligere kommune, nå en del av …».
- **H6. Innenlandsk flytting summerer ikke til null i 2016–2019.** Avviket er på inntil 226 per kvartal, trolig på grunn av flyttinger til og fra Svalbard eller uoppgitt kommune `[T]`. Ikke synlig i prototypen, men bør nevnes for fag.
- **H7. Pyramide for kommunene bare i tre år.** 1986, 2006 og 2026 er valgt, og de fem kommunene som ble delt i 2024, mangler 1986. Glidebryter per år finnes bare for landet.
- **H8. `felles/grafikk.py` finnes ikke i repoet.** Steg 2-skillen viser til den, men repoet har bare `felles/bygg.py`. `lag_grafikk.py` bruker en lokal reserve med samme grensesnitt.
- **H9. Etnedal.** Kommunen hadde 414 innvandringer i 2025 (+27 prosent i folketallet). Årsaken er fortsatt ikke kjent. Prototypen bør ikke forklare den uten kilde.
- **H10. Flyttetall mangler** («..») for Sirdal, Haugesund, Sunndal og Smøla i 1951–1957 (28 kommuneår). Funnet i steg 4.

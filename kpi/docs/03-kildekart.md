# Kildekart: Konsumprisindeksen (KPI)

Steg 3 i formidlingsprototype for `kpi` · versjon 0.1 · 14.10.2026

Notatet viser hvilke tabeller i statistikkbanken som svarer på de fem prioriterte spørsmålene fra `01-innsikt.md`, med søk på detaljerte varer og varegrupper som eget krav. Spørringene står i maskinlesbar form i `data/kilder.json`. Fagkontakten bør se over tabellvalget i steg 5.

## Spørsmål, tabeller og seksjoner

| Spørsmål | Datasett | Tabell | Seksjon i prototypen |
|---|---|---|---|
| 1. Hvor mye stiger prisene nå? | hovedserier, grupper | 14706, 14700 | Toppgrafikk A og tolvmånedersvekst over tid |
| 2. Hva driver prisveksten? | grupper, vekter | 14700 | Bidrag per hovedgruppe, med SSBs metode |
| 3. Hva er med i KPI, og hvor mye veier det? | vekter, grupper | 14700 | Handlekurven, og **søk på varer og varegrupper** |
| 4. Hva viser de avledede prisindeksene? | hovedserier | 14706 | KPI, KPI-JA, KPI-JE, KPI-JAE og XADM sammenlignet |
| 5. Hva er en krone verdt over tid? | historisk | 14710 | Pengeverdi fra 1920 |

Alle tabellene er nye fra 2026 (basisår 2025 = 100, COICOP 2018). De gamle tabellene 03013, 03014, 05327 og 05335 er arkivert.

## Grunnlaget for søk

Tabell 14700 har 336 koder i et hierarki som leses rett ut av koden:

| Nivå | Eksempel | Antall | Har vekt |
|---|---|---|---|
| Totalindeks | `00` I alt | 1 | Ja |
| Hovedgruppe | `01` Matvarer og alkoholfrie drikkevarer | 13 | Ja |
| Gruppe | `01.1` Matvarer | 40 | Ja |
| Undergruppe 1 | `01.1.1` Brød og kornprodukter | 82 | Ja |
| Undergruppe 2 | `01.1.1.3` Brød og bakervarer | 74 | Nei |
| Vare eller varegruppe | `01.1.1.3_1` Brød | 126 | Nei |

Antallet per nivå er talt fra de 336 kodene i tabellen, med nivået lest ut av koden.

**Funn som former søket:**

- **Hierarkiet er svært skjevt.** 205 av de 336 kodene er mat og alkoholfrie drikkevarer. Klær, bolig, transport og tjenester stopper på tredje nivå. Unntak er drivstoff (diesel, bensin og hurtiglading) og noen tobakksvarer. Et søk på «mobil», «frisør» eller «strøm» treffer derfor en gruppe, ikke en vare. [T] Søket må vise hvor i hierarkiet treffet ligger.
- **Vekter finnes bare ned til tredje nivå.** Brød og bakervarer har ingen egen vekt, bare Brød og kornprodukter (1,16 prosent). For detaljerte varer kan vi vise prisutvikling, men ikke bidrag. Det bør stå tydelig ved hvert treff.
- **Mange grupper mangler historikk.** Av de 336 kodene har 263 indeks fra januar 2015, 10 starter et sted mellom 2015 og 2025, og 37 har bare tall fra januar 2026. Et eksempel på det siste er nøttesmør. De resterende 26 har vekt, men ingen indeks i det hele tatt. Blant dem er restauranter og kaféer (`11.1.1`), renovasjon (`04.4.2`) og annen betalt husleie (`04.1.2`). Søket må skille mellom «ingen tall» og «tall bare fra 2026».
- **Etikettene har en varighetskode** i parentes: IV, HV, V og T. Det er trolig ikke-varige varer, halvvarige varer, varige varer og tjenester. Koden må forklares eller fjernes i visningen, og tolkningen må bekreftes av fagkontakten.
- **Store utslag finnes på detaljnivå.** Diesel steg 34,9 prosent siste tolv måneder, mens totalindeksen steg 3,4. Søket vil derfor vise mange tall som ser dramatiske ut. Konteksten må alltid stå ved siden av: totalindeksen og vekten til gruppen over.

**Navn er ikke det folk søker på.** «Brus og leskedrikker» finnes, men ikke «cola». «Elektrisitet inkludert nettleie» finnes, men ikke «strøm». En liten liste med synonymer for de 30–50 vanligste søkeordene vil gi mye. Listen er vårt valg og bør leses av fagkontakten. [T]

## Bidrag til prisveksten: metoden er testet

SSB beregner bidrag med indekser og vekter for to år, fordi vektene skifter i januar. Vi har gjenskapt metoden for hovedgruppene i september 2026:

- Bidraget fra september 2025 til desember 2025 regnes med vektene for 2025.
- Bidraget fra desember 2025 til september 2026 regnes med vektene for 2026, skalert med totalindeksens endring fram til desember.
- Summen av bidragene ble 3,44 prosentpoeng. Publisert tolvmånedersvekst er 3,4. Avviket skyldes at indeksene er avrundet til én desimal.

| Hovedgruppe | Bidrag, prosentpoeng |
|---|---|
| Bolig, elektrisitet og brensel | 1,03 |
| Transport | 0,66 |
| Servering og overnatting | 0,37 |
| Fritid, sport og kultur | 0,35 |
| Matvarer og alkoholfrie drikkevarer | 0,22 |
| Øvrige åtte grupper | 0,81 |

Det grove anslaget i steg 2 (vekt × endring) ga 1,1 for bolig og summerte til 3,5. SSBs metode gir et ryddigere tall. Toppgrafikk C kan nå bygges riktig.

## Kontroller som er kjørt

| Kontroll | Resultat |
|---|---|
| Totalindeksen gjenskapt fra hovedgruppene med 2025-vekter, september og desember 2025 | 100,61 mot publisert 100,6. 101,0 mot publisert 101,0 |
| Totalindeksen gjenskapt med 2026-vekter, september 2026 | 104,07 mot publisert 104,0. Avviket skyldes avrunding |
| Hovedgruppenes vekter summerer til 1 000 | 1 000,1 (avrunding) |
| Sum av bidrag mot publisert tolvmånedersvekst | 3,44 mot 3,4 |
| Tolvmånedersvekst regnet fra indeks mot publisert | 3,38 mot 3,4. **Publiserte endringer må brukes direkte** |

## Datamengde og strategi

| Datasett | Celler |
|---|---|
| hovedserier (14706, fra 1995) | om lag 9 100 |
| grupper (14700, alle nivåer, fra 2015) | om lag 142 000 |
| vekter (14700, januar 2015–2026) | om lag 4 000 |
| historisk (14710, fra 1920) | 1 279 |

Alt er godt under API-ets grense på 800 000 celler per spørring. Gruppene utgjør nesten alt.

**Valgt 14.10.2026: alle grupper fra januar 2015.**

For å holde filen nede tar prototypen med to mål per gruppe og måned: indeks og publisert tolvmånedersendring. Det blir om lag 336 × 2 × 141 ≈ 95 000 verdier, trolig 0,5–0,7 MB innbakt i `index.html`.

Månedsendring tas bare med for totalindeksen og de avledede seriene (14706), der den trengs i forklaringen av H6.

Vektene tas med for alle år, fordi bidragsberegningen trenger både fjorårets og årets vekter.

## Hull og hindre

1. **Varighetskodene (IV, HV, V, T)** er tolket, ikke bekreftet.
2. **Hva SSB anbefaler om bidrag for undergrupper,** der bare noen nivåer har vekt.
3. **Synonymlisten** for søk er laget i steg 4 (`data/synonymer.json`, 109 søkeord). Den er vårt valg, og tolv koblinger er merket usikre.
4. **URL-ene i `kilder.json` er ikke kjørt direkte** mot API-et. Spørringene er testet gjennom SSB-tilkoblingen, som CSV.
5. **Strømstøtten og Norgespris:** hvordan de inngår i `04.5.1`, er ikke avklart. Det er spørsmål 2 til fagkontakten i innsiktsnotatet.

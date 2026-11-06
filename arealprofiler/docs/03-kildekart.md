Steg 3 i formidlingsprototype for arealprofiler · versjon 0.1 · 06.11.2026 · Status: godkjent av Thomas

# Kildekart: Arealprofiler

**Merking.** `[K1]`–`[Kn]` viser til kildelisten i `01-innsikt.md`. `[T]` er vår tolkning.

**Valg av kilde (Thomas, 06.11.2026).** Prototypen bygges på fjorårets datagrunnlag, `arealprofiler2024_ettark.xlsx`, som er det som ligger bak Arealprofiler 2025 (publisert 29.08.2025). Tabell 14478 og 14488 er ikke publisert eksternt, og årets tall har revisjoner og hull som ikke er avklart (se avviksrapporten). Når tabellene er publisert, byttes kilden. URL-ene står klare i `data/kilder.json`.

## 1. Spørsmål, datasett og seksjon

| Spørsmål (fra steg 1) | Datasett | Kilde | Seksjon i prototypen |
|---|---|---|---|
| 1. Hvordan står min kommune mot lignende kommuner? | `arealprofiler`, `sentralitet` | Fila, Klass 128/1417 | Toppgrafikk C (valgt) og indikatorstripen for alle 35 |
| 2. Bygger vi tettere og nærmere sentrum? | `arealprofiler` (A1–A8, C5–C12) | Fila | «Bygger vi tettere?» med variant A som hovedfigur |
| 3. Hvor mye jord, strand og natur bygges ned? | `arealprofiler` (C1, C3, C4, B1–B4, B8), `kofola_land` | Fila, tabell 11776 | «Hva bygger vi ned?» med variant B, landstall fra 11776 |
| 4. Hvor mye er satt av i planen? | `arealprofiler` (B9) | Fila | «Hva er planlagt?» Bare B9, bare 2023–2024 |
| 5. Hvor mye bygges i fareområder? | `arealprofiler` (B5, B10) | Fila | «Bygger vi i fareområder?» Bare 2024–2025 |
| Kan vente | `arealprofiler` (A5, A9–A14, B6, B7) | Fila | Med i indikatorstripen, ingen egen seksjon |

## 2. Strukturen

Talt med `scripts/analyser_struktur.py`. Detaljer i `docs/03-struktur.json`.

**Omfang.** 105 476 rader, 35 indikatorer, 357 kommuner (inndeling 2024), 2015–2025. B8 har sju arealklasser. Fordelt etter hvordan tallene lages: 12 fra registre, 4 fra KOSTRA, 18 kartbaserte, 1 fra kommuneplanen.

**Siste år.** 2025 for 16 indikatorer, 2024 for 17 og 2023 for 2 (A11 og C5). Indikatorstripen må derfor vise årstallet på hver rad.

**Lengde og hull i seriene.**

| Serie | Indikatorer |
|---|---|
| 2015–2025 eller 2015–2024 uten hull | 26 indikatorer |
| Starter senere | B3 fra 2019, C6 fra 2019, B9 fra 2023, B5, B8 og B10 fra 2024 |
| Annethvert år | B6 og B7: 2022 og 2024 |
| Hull | B2 mangler 2016–2018. B3 mangler 2020 |

**Fireårssummer.** 10 indikatorer er summer for siste fire år: A6, A7, A8, B1, B3, B5, B10, C8, C10 og C12.

**Manglende tall og nuller (siste år).** Fila har ingen statussymboler. Et tall som mangler, er en rad som ikke finnes. Hva det betyr, må leses av indikatoren:

| Indikator | Kommuner med tall | Mangler | Nuller | Tolkning |
|---|---|---|---|---|
| A2 Bosatte per km² tettsted | 335 | 22 | 0 | Ingen tettsted: ikke aktuelt |
| A3 Andel i tettsted | 357 | 0 | 22 | Samme 22 kommuner, men her som 0 |
| B2 Tilgjengelig strandsone, B3 Nye bygg i strandsonen | 226 | 131 | 0 / 9 | Ikke kystkommune: ikke aktuelt |
| B4 Dispensasjoner i 100-metersbeltet | 103 | 254 | 0 | **Uavklart:** null dispensasjoner, ikke kyst eller ikke rapportert |
| B10 Bygninger i naturfareområder | 195 | 162 | 0 | Trolig 0. Tabell 14478 har 0 for de samme kommunene |
| B6, B7 Trygg tilgang | 333 | 24 | 0 | Ingen tettsted: ikke aktuelt |
| C6 Andel som jobber i sentrum | 357 | 0 | 135 | Ingen sentrumssone: 0 |
| C12 Nye næringsbygg, avstand til sentrum | 318 | 39 | 1 | Ingen nye næringsbygg på fire år |
| A6–A8, C8, C10 | 352 | 5 | – | Ingen nye boliger på fire år |
| A12 Kommunalt disponerte boliger | 346 | 11 | 0 | Mangler |

Prototypen må vise tre tilstander: tallet mangler, ikke aktuelt (ingen tettsted, sentrumssone eller kyst) og null. Det er H5 fra steg 1. A3 og C6 lagrer «ingen tettsted» og «ingen sentrumssone» som 0. De bør vises som ikke aktuelt, ikke som 0 prosent.

**Sentralitet.** Klass 128, versjon 2020, korrespondanse mot kommuneinndelingen 2024 (tabell 1417). 357 kommuner fordelt på klasse 1: 5, 2: 21, 3: 54, 4: 65, 5: 104, 6: 108. Klasse 1 er for liten til et spredningsbånd. Der må stripen vise de fem kommunene som punkter `[T]`.

## 3. Metoder som er testet

**Spredning i klassen** (toppgrafikk C). 10., 50. og 90. persentil med lineær interpolasjon. For Lillehammer (klasse 3) har 34 av 54 kommuner lavere andel bosatte i tettsted (A3 2024: 87 prosent). Persentilene er ikke vektet, så de er ikke landstall.

**Vektet landsandel for nye boliger** (seksjon 2, variant A). Kommunenes andel (A7, A8) ganget med antall nye boliger (A6), summert og delt på summen av A6. For 2025 ga det 10,4 prosent utenfor tettsted og 50,6 prosent i blokk (2015: 20,0 og 38,2). A7 er avrundet til hele prosent i fila, så blokkandelen blir usikker med noen tideler. Det er en egen beregning, merket `[T]`.

**Landstall for omdisponert jord** (seksjon 3, variant B). Summen av C3 for kommunene sammenlignet med tabell 11776 for landet:

| År | Sum C3 | 11776 alle formål | 11776 andre formål enn landbruk | Sum C4 | 11776 dyrkbar, alle formål |
|---|---|---|---|---|---|
| 2015 | 6 079 | 6 422 | 6 313 | 6 285 | 6 327 |
| 2019 | 3 644 | 3 843 | 3 803 | 4 829 | 4 865 |
| 2020 | 4 760 | 4 740 | 4 604 | 7 081 | 7 071 |
| 2022 | 3 613 | 3 604 | 3 528 | 4 325 | 4 322 |
| 2023 | 2 997 | 2 988 | 2 787 | 4 008 | 4 004 |
| 2024 | 2 981 | 2 949 | 2 479 | 2 794 | 2 786 |
| 2025 | – | 1 964 | 1 793 | – | 2 350 |

Resultatet: C3 og C4 er omdisponering til **alle formål**, også landbruksformål. Fra 2020 avviker summen fra 11776 med 9–32 dekar. Det skyldes trolig revisjoner: kommunetallene for Lillestrøm og Time for 2024 ble rettet 15. juni 2026, etter at fila ble laget. For 2015–2019 er summen for lav fordi 4–13 kommuner mangler. Jordvernmålet og kofolas hovedtall gjelder **andre formål enn landbruk**. Det forklarer avviket fra steg 1 (H9): 1 964 mot 1 793 dekar i 2025.

## 4. Kontroller

| | Kontroll | Resultat |
|---|---|---|
| K1 | Fila mot uttrekket i Tableau-arbeidsboka 2025 | Lik rad for rad, 0 avvik |
| K2 | Den vedlagte fila (06.11) mot den fra 05.11 | Samme innhold. Filene har ulik sjekksum, men ingen rad avviker |
| K3 | Sentralitet fra Klass mot kommunenøkkelen i arbeidsboka | 357 av 357 like |
| K4 | Sum C3/C4 mot tabell 11776 | Se tabellen i avsnitt 3. Avvik forklart |
| K5 | B8: de sju klassene summerer til 100 | 45 kommune-år avviker mer enn 1,5 prosentpoeng, ned til 90,9 (1151 Utsira, 2024). Trolig avrunding og areal som ikke er klassifisert `[T]` |
| K6 | Lillehammers tall i grafikken mot fila | Like (hentet av skript) |
| K7 | Antall kommuner og indikatorer i konseptgrafikken | Talt fra fila: 35 og 357 |

Ikke kjørt: A6 mot SSBs tall for igangsatte boliger, A2/A3 mot tabell 04861, A11 mot 06947. Det kan gjøres i steg 4 hvis tid.

## 5. Datamengde

| Alternativ | Innhold | Celler | Størrelse i `index.html` | Gjør mulig |
|---|---|---|---|---|
| Liten | Siste år for alle 35 indikatorer og 357 kommuner, sentralitet | 14 637 | 104 kB (26 kB komprimert) | Kommuneprofil og indikatorstripe. Ingen tidsserier |
| **Middels** | Alle år 2015–2025 for alle indikatorer, sentralitet, landstall for jord fra 11776 | 111 741 | 570 kB (132 kB komprimert) | I tillegg små tidsserier per indikator, seksjonene med variant A og B, og «min kommune over tid» |
| Stor | Middels pluss fylkesvise summer og sammenligning med valgfri kommune | om lag 112 000 | om lag 600 kB | Sammenlign to kommuner, fylkesoversikt. Fylkessummer er bare mulig for antall, ikke for andeler |

Alle tre ligger langt under API-grensen og kan bakes inn i `index.html`. **Anbefaling: middels.** Tidsseriene trengs for spørsmål 2 og 3, og de koster lite. Fylkessummer i «stor» bryter med at prototypen ikke skal lage egne landstall.

## 6. Hull og hindre

1. **Tabell 14478/14488 er ikke publisert.** Prototypen bygger på en fil som ikke kan hentes på nytt med `hent_data.py`. Fila ligger uendret i `data/raw/`.
2. **B4 mangler for 254 kommuner.** Om det betyr null, ikke kyst eller ikke rapportert, må fag svare på.
3. **A3 og C6 lagrer «ingen tettsted» og «ingen sentrumssone» som 0.** Prototypen må gjøre om disse til «ikke aktuelt». Det krever en regel: A3 = 0 og A2 mangler gir ikke aktuelt.
4. **C3 og C4 er ikke jordverntallene.** Seksjonen om jord må bruke 11776 for landet og forklare forskjellen på alle formål og andre formål enn landbruk.
5. **B9 dekker bare 2023–2024** og har ny definisjon i årets tabell. Seksjonen om planreserver blir tynn og må merke bruddet når kilden byttes.
6. **Fireårsperiodene** (Q5 i steg 2). Fila sier ikke hvilke fire år «2025» dekker.
7. **B8 summerer ikke til 100** for 45 kommune-år.
8. **Persentiler og median** for sentralitetsklassen er uvektede og regnet av oss. De må merkes som sammenligningsgrunnlag, ikke som landstall.
9. **Klasse 1 har fem kommuner.** Spredningsbåndet er meningsløst der. Vis punkter.
10. **Kildetabell er oppgitt for bare 11 av 35 indikatorer** i forklaringstekstene. Resten må fag fylle inn til «Om tallene».

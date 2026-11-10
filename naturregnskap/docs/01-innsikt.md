Steg 1 i formidlingsprototype for naturregnskap · versjon 0.3 · 10.11.2026 · Status: godkjent av Thomas, kommentert av fagseksjonen 10.11.2026

# Innsikt: Naturregnskap

**Merking:** `[K1]`–`[Kn]` er kilde (liste nederst). `[T]` er vår tolkning. `[H]` er en hypotese om misforståelse, som skal prøves i fagkontrollen.

**Om dette notatet.** Naturregnskapet publiseres for første gang 25. november 2026, med referanseår 2024. Statistikkbanktabellene finnes ennå ikke i det åpne API-et: data.ssb.no svarer «Non-existent table» for 15012, og et søk på «naturregnskap» gir ingen treff (testet 05.11.2026). Notatet bygger derfor på tabelltitlene i Thomas' skjermbilde fra den interne statistikkbanken [K3] og på de to utkastene som publiseres sammen med tallene [K1, K2]. Ingen tall i notatet er kontrollert mot statistikkbanken, fordi det ikke finnes tall å kontrollere mot. Nøkkelbudskapene med tall må skrives etter 25.11.

Kortnavnet `naturregnskap` er foreløpig. Statistikksiden finnes ikke ennå, så det er ikke bekreftet [T].

---

## 0. Variablene i statistikkbanktabellene

Variablene er utledet fra tabelltitlene. Kodelistene er ikke sett [T]. «(I)» i titlene tolker vi som ikke publisert.

| Tabell | Delregnskap | Måltall og enhet | Dimensjoner (fra tittelen) | År |
|---|---|---|---|---|
| (ikke oppgitt) | Utbredelse | Areal, hektar [K2] | Økosystemtype (EU-typer og hovedøkosystemer) × region (land, fylke, kommune). Utbygging 2017–2024 på landsnivå [K1] | 2024 |
| 14967 | Tjenester | Tilgang, i tjenestens egen enhet | Økosystemtjeneste × økosystemtype | 2024 |
| 14968 | Tjenester | Anvendelse, i tjenestens egen enhet | Økosystemtjeneste × økonomisk enhet (næringer, husholdninger, offentlig, eksport) | 2024 |
| 14994 | Tjenester: avlinger | 1000 tonn | Økosystemtype × avlingstype | 2010–2024 |
| 14995 | Tjenester: pollinering | 1000 tonn | Økosystemtype × avlingstype | 2024 |
| 14996 | Tjenester: tømmer | 1000 m³ | Skog (produktiv og uproduktiv) [K1] | 2015–2024 |
| 14997 | Tjenester: luftrensing | 1000 tonn PM2,5 og PM10 | Økosystemtype × landsdel | 2024 |
| 14999 | Tjenester: temperaturregulering | Grader celsius | Økosystemtype × utvalgte byer | 2024 |
| 15000 | Tjenester: flomdemping | Hektar | Økosystemtype × landsdel | 2024 |
| 15012 | Tilstand: skog | Skalert 0–1 | Indikator × egenskap × landsdel | 2019–2024 |
| 15013 | Tilstand: fjell | Skalert 0–1 | Indikator × egenskap × landsdel | 2019–2024 |
| 15014 | Tilstand: åpent lavland og jordbruksmark | Skalert 0–1 | Indikator × egenskap × økosystemtype | 2024 |
| 15015 | Tilstand: våtmark | Skalert 0–1 | Landsdel (Naturindeks) | 2019–2024 |
| 15016 | Tilstand: vassdrag og kystvann | Skalert 0–1 | Indikator × egenskap × økosystemtype (elver, innsjøer, kystvann) | 2024 |
| 14852 | Tilstand: uskalert | Egen enhet per variabel | Variabel × egenskap × økosystemtype | 2024 |

Observasjoner:

- **Tre tjenester har ingen egen tabell:** global klimaregulering, naturbasert turisme og naturbasert rekreasjon. Nummeret 14998 mangler i rekken. Vi antar at de bare finnes i 14967/14968, eller at én tabell ikke er med i skjermbildet [T]. Klimaregulering har tidsserie fra 2010 [K1], så en egen tabell ville vært naturlig. **Må avklares.**
- **Tidsseriene er få.** Bare avlinger (2010–), tømmer (2015–) og tilstand for skog, fjell og våtmark (2019 og 2024) har mer enn ett år. Et dashbord for allmennheten blir derfor mest et statusbilde, ikke en utviklingshistorie [T].
- **Tilstand ligger i fem tabeller med ulik struktur.** Skog og fjell har landsdel og to år. Våtmark har bare landsdel. Lavland, jordbruk, vassdrag og kystvann har bare 2024 og nasjonalt nivå. Totalindeksen ligger trolig som en egen verdi i indikatordimensjonen [T]. **Må sjekkes i kodelistene.**
- **Enhetene er forskjellige for hver tjeneste:** tonn, m³, hektar, °C, overnattinger og dagsturer. Tjenestene kan ikke summeres og ikke sammenlignes i størrelse.
- **Geografien er forskjellig per delregnskap:** kommune for utbredelse, landsdel for tilstand og noen tjenester, utvalgte byer for temperatur.
- **Den samme økosystemtypen går igjen** i nesten alle tabeller. Den er den eneste dimensjonen som binder delregnskapene sammen [T].

## 1. Statistikken på ett ark

| | |
|---|---|
| **Hva den er** | Et regnskap i fysiske størrelser over Norges økosystemer: hvor mye det er av hver type (utbredelse), hvor nær intakt tilstand de er (tilstand), og hva de leverer til samfunnet (økosystemtjenester) [K1, K2] |
| **Hva den ikke er** | Ikke en verdsetting i kroner. Ikke en vurdering av enkeltområder. Ikke en fullstendig beskrivelse av naturens verdi, fordi ikke-bruksverdier, egenverdi og relasjonelle verdier ikke er med [K2] |
| **Rammeverk** | FNs SEEA EA (2021). EU-forordning 2024/3024, som gjelder gjennom EØS [K2] |
| **Frekvens** | Til Eurostat: tjenester årlig, utbredelse og tilstand hvert tredje år. Endring i utbredelse første gang i 2029 [K2] |
| **Referanseår** | 2024. Tilstand også 2019. Tidsserier for avlinger (2010–) og tømmer (2015–) [K1] |
| **Klassifisering** | 12 EU-økosystemtyper og 11 nasjonale hovedøkosystemer (Klass 988, nasjonal variant) [K1] |
| **Geografi** | Utbredelse: land, fylke og kommune. Tilstand og noen tjenester: fem egne landsdeler (Øst, Sør, Vest, Midt, Nord) som avviker fra SSBs standard [K1] |
| **Datakilder** | Grunnkartet 2025, Fagsystemet for økologisk tilstand, Naturindeks, vannforskriften, Landsskogtakseringen, klimagassregnskapet, rekreasjonsundersøkelsen, modeller (INCA m.fl.) [K1] |
| **Revisjon** | Metodene er under utvikling gjennom 2027. Kildene revideres, for eksempel Landsskogtakseringen [K1, K2] |
| **Bruk** | Kunnskapsgrunnlag for naturmeldingen (mål 1, 11, 14, 21), rapportering til Eurostat, forvaltning [K2] |
| **Bruksvolum** | Ukjent, siden statistikken er ny |

## 2. Nøkkelbudskap

Det finnes ingen tall ennå. Budskapene under er strukturelle og må fylles med tall etter 25.11.

1. Det første nasjonale naturregnskapet viser hvor mye natur Norge har, hvordan den har det og hva den gir oss, for 2024 [K2].
2. Utbredelsen er den delen som kan brytes ned til kommune. Endring gjelder foreløpig bare utbygging 2017–2024, og bare for hele landet [K1].
3. Det finnes en samlet tilstandsindeks for skog, fjell, elver, innsjøer og kystvann. For skog og fjell kan 2019 og 2024 sammenlignes per landsdel [K1, K2].
4. Ni økosystemtjenester er tallfestet, hver i sin egen enhet. Sju av dem rapporteres til EU [K1].
5. SSB vurderer selv kvaliteten per tjeneste på tre dimensjoner. Ingen tjeneste har høy vurdering på alle tre [K1].
6. *[Resultat: største økosystemtype og andel skog]*, *[resultat: utbygd areal 2017–2024]*, *[resultat: skogens totalindeks 2019→2024]*. Disse fylles inn 25.11.

## 3. Vanskelige begreper

Skrevet uten tall. Eksemplene byttes ut med ekte verdier når tallene finnes.

- **Utbredelse.** Arealet av hver økosystemtype. «Skog dekker *[x]* prosent av fastlands-Norge.»
- **Tilstandsindikator, skalert 0–1.** 1 er intakt natur (referansetilstand), 0 er helt ødelagt. Død ved i skog måles i m³ per hektar og omregnes mot en referanseverdi som eksperter har satt. «Skog har totalindeks *[0,xx]*» betyr ikke at *[xx]* prosent av skogen er intakt [K2].
- **Tilstandsegenskap og totalindeks.** Indikatorene grupperes i seks egenskaper. Totalindeksen er snittet av egenskapene, der hver egenskap teller likt [K2].
- **Uskalert variabel (14852).** Måles i egen enhet uten referanseverdi, for eksempel svevestøv. Den sier ikke om noe er godt eller dårlig.
- **Tilgang og anvendelse.** Begrepene er lånt fra nasjonalregnskapet. Tilgang betyr hvilke økosystemer som leverer tjenesten. Anvendelse betyr hvem som bruker den: næringer, husholdninger, det offentlige eller eksport. For allmennheten bør de omskrives til «hvor kommer det fra» og «hvem bruker det» [T].
- **Hovedøkosystem kontra EU-type.** Det er to inndelinger av samme kart, og de gir ulike tall for for eksempel jordbruk og fjell [K1].

## 4. Sannsynlige misforståelser

| | Misforståelse | Grunnlag | Prototypen må |
|---|---|---|---|
| H1 | Indeks 0,7 betyr at 70 prosent av naturen er intakt | Rapporten advarer eksplisitt mot dette [K2] | Vise skalaen med en forklaring ved første tilstandstall |
| H2 | Endring i utbredelse viser all naturendring | Bare utbygging er med. Gjengroing, og myr som blir skog, er ikke med [K1, K2] | Kalle det «utbygd areal», ikke «endring i natur» |
| H3 | Tjenestene kan summeres eller sammenlignes i størrelse | Hver tjeneste har sin egen enhet [K3] [T] | Aldri vise tjenestene på felles akse. Én tjeneste om gangen, eller andeler per økosystem |
| H4 | De tre delregnskapene kan leses i sammenheng, for eksempel at mer tjenester betyr bedre natur | Ulike kilder, metoder og år. Tilstand og tjenester kan trekke hver sin vei, for eksempel død ved mot tømmer [K2]. Fagseksjonen: kanskje den alvorligste misforståelsen [K6] | Si det ved alle steder der tallene står side om side. Ikke plassere tilstand og tjenester slik at de leses som årsak og virkning |
| H5 | Alle økosystemer har en tilstandsindeks | Bare 5 av 11 har det. Hav og kyststrender har ingen indikatorer [K1] | Vise hull som hull, med «mangler data», ikke nuller |
| H6 | Tallene gjelder min kommune | Bare utbredelse (EU-typer) finnes per kommune. Utbygging per kommune kommer 26.02.2027 [K6] | Ikke tilby kommunevalg for tilstand og tjenester (lavere prioritet etter februar 2027) |
| H7 | Naturregnskapet viser naturens verdi i kroner | Monetære regnskap er ikke med i 2026 [K2] | Si det tidlig, i lesehjelpen |
| H8 | Landsdel betyr SSBs vanlige landsdeler | Naturregnskapet bruker fem egne landsdeler [K1] | Vise landsdelene på kart med navn |
| H9 | EU-tallene og de nasjonale tallene er de samme | Ulik inndeling og ulike indikatorer [K2] | Bruke de nasjonale tallene, og si det (lav prioritet) |
| H10 | Uskalerte variabler viser god eller dårlig tilstand | De mangler referanse [K2] | Holde 14852 utenfor dashbordet (lav prioritet) |

## 5. Brukere og hva de trenger

1. **Allmennheten og pressen.** Vil vite om naturen har det bra, hvor mye som bygges ned, og hva naturen gir oss. Trenger få tall, tydelige forbehold og enkelt språk.
2. **Kommuner og lokalt engasjerte.** Vil se sin egen kommune. Kan få utbredelse, men må bli fortalt hvor grensen går (H6). Miljødirektoratets kommunale løsning kommer senere våren 2027 [K6].
3. **Skoleelever og lærere.** Trenger at begrepene forklares, særlig skalaen og forskjellen på de tre delregnskapene.

Prototypen skal ikke være et analyseverktøy for forvaltningen, og ikke en kopi av statistikkbanken med alle indikatorer.

## 6. Prioritering

Kriterier: (a) sentralt i SSBs egne budskap, (b) stor fare for misforståelse, (c) kan besvares fra statistikkbanken, (d) passer i en oversikt.

**Forslag til gjennomgående valg: økosystemtype** («Velg natur»: skog, fjell, våtmark, jordbruksmark, kystvann …). Det er den eneste dimensjonen som går igjen i nesten alle tabeller, og den lar ett valg styre alle tre delregnskapene [T]. Valget er forenlig med H3: én natur om gangen, og tjenestene vist som andeler. Alternativet, «Min kommune», faller bort fordi bare utbredelse finnes per kommune.

| Prioritet | Spørsmål | Kriterier | Hypoteser | Kilde |
|---|---|---|---|---|
| 1 | Hvor mye natur har vi, og hvor mye er bygd ned? | a, b, c, d | H2, H6 | Utbredelsestabellen (kommune), utbygging (land) |
| 2 | Hvordan har naturen det? | a, b, c, d | H1, H5, H8 | 15012, 15013, 15015, 15016 (totalindeks per økosystem, landsdel for skog og fjell, 2019→2024) |
| 3 | Hva gir naturen oss, og hvem bruker det? | a, b, c | H3, H4 | 14967, 14968 |
| 4 | Hvor sikre er tallene? | a, b, d | H1, H3, H7 | Kvalitetsvurdering i metodenotatet [K1] (ikke statistikkbanken) |

**Må med uansett (lesehjelp):** de tre delregnskapene på ett ark (H7), skalaen 0–1 (H1), og at endring bare er utbygging (H2).

**Kan vente:** tidsserier for avlinger og tømmer, luftrensing og flom per landsdel, temperatur per by, enkeltindikatorer per egenskap.

**Utenfor:** uskalerte EU-variabler (14852), EU-inndelingen, monetære verdier.

## 7. Spørsmål til fagkontakten

1. Stemmer hypotesene H1–H10? Hvilke ser dere oftest?
2. Hvor ligger tallene for global klimaregulering, naturbasert turisme og naturbasert rekreasjon? Finnes 14998?
3. Hvilket nummer har utbredelsestabellen, og har den endring (utbygging) som egen tabell?
4. Ligger totalindeksen og egenskapene som egne koder i 15012–15016?
5. Er det greit at prototypen bruker hovedøkosystemer og ikke EU-typer?
6. Kan vi få en testuttrekk eller dummyfil med riktige kodelister før 25.11?

## 7b. Svar fra fagseksjonen (10.11.2026)

- **Hypotesene:** H1, H2 og H7 er mest relevante. H4 utvides til at delregnskapene ikke kan leses i sammenheng, og er kanskje den alvorligste. H3, H5 og H8 er designspørsmål. H6 blir mindre aktuell etter februar 2027. Vurderingen er foreløpig.
- **Tabeller:**

  | Innhold | Tabell |
  |---|---|
  | Global klimaregulering, ikke fordelt på hovedøkosystemer | 14998 |
  | Turisme, rekreasjon og alle tjenester aggregert per økosystemtype | 14967 |
  | Utbredelse, EU-typologi med kommunal oppløsning | 15034 |
  | Utbredelse, hovedøkosystemer, bare statustall | 15036 |
  | Utbygging | ikke avklart |

  Utbyggingstallene er foreløpige. Tall per kommune, basert på satellittdata, kommer 26.02.2027.
- **Tilstand:** totalindeksen er en egen variabel (Indeks_skog, Indeks_fjell, Indeks_elv_bekk, Indeks_innsjo_vann, Indeks_kystvann). Egenskapene filtrerer indikatorene, men har ingen egne verdier.
- **Hovedøkosystemer fungerer** for alt unntatt global klimaregulering.
- **Kodelister i KLASS:**

  | Nummer | Kodeliste |
  |---|---|
  | 988 | Økosystemtyper, med variant for hovedøkosystemer |
  | 939 | Økosystemtjenester |
  | 959 | Indikatorer |
  | 966 | Egenskaper |
  | 967 | Landsdeler |
  | 992 | Anvendelse |

  De er hentet 10.11.2026 og ligger i `data/klass/`.

## 8. Hull i grunnlaget

- Ingen tall og ingen kodelister. Tabellstrukturen er utledet fra titler.
- Utbredelsestabellen er ikke identifisert.
- Statistikksiden og «Om statistikken» finnes ikke ennå.
- Metodenotatet og den kvalitative rapporten er utkast v1 med åpne felt («XXXX», «[resultater]»).
- Fagkontakt er ikke avklart. Forfatterne av metodenotatet er kandidater.

## 9. Kilder

- [K1] SSB: *Metodenotat, nasjonalt naturregnskap*, utkast v1 (2026). Vedlegg fra Thomas.
- [K2] SSB: *Når naturen telles. Kvalitativ rapport til naturregnskapet*, utkast v1 (2026). Vedlegg fra Thomas.
- [K3] Skjermbilde av mappen «Naturregnskap» i den interne statistikkbanken, 05.11.2026 (tabell 14852, 14967, 14968, 14994–14997, 14999, 15000, 15012–15016).
- [K4] Miljødirektoratet: «Hva er et naturregnskap?», https://www.miljodirektoratet.no/ansvarsomrader/overvaking-arealplanlegging/naturregnskap/
- [K6] Fagseksjonen, skriftlige svar på spørsmålene i dette notatet og på kvalitetssikringslistene, 10.11.2026.
- [K5] Miljødirektoratet: «Kommunale naturregnskap – hva er status og hva skjer i 2026?», https://www.miljodirektoratet.no/aktuelt/fagmeldinger/2026/mars-2026/kommunale-naturregnskap--hva-er-status-og-hva-skjer-i-2026/

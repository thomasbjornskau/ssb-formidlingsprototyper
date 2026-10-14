# Innsiktsnotat: Konsumprisindeksen (KPI)

Steg 1 i formidlingsprototype for `kpi` · versjon 0.1 · 14.10.2026 · Status: utkast, ikke fagkontrollert

**Merking**

- **[K1]–[K9]** viser til en SSB-kilde eller annen navngitt kilde i kildelista nederst.
- **[T]** er vår tolkning.
- **[H]** er en hypotese om misforståelse. Den skal prøves i fagkontrollen (steg 5).

**Om dette notatet.** Dette er første framoverrettede pilot: notatet er skrevet før det finnes noen prototype for KPI. Tall er hentet fra statistikkbanken 14.10.2026 og gjelder september 2026.

---

## 1. Statistikken på ett ark

| | |
|---|---|
| Hva den er | KPI måler prisutviklingen på varer og tjenester husholdningene kjøper i Norge [K1] |
| Hva den ikke er | Ikke et mål på prisnivå, og ikke på boligpriser eller renter. Kjøp av bolig regnes som investering, ikke konsum [K4] |
| Frekvens | Månedlig, rundt den 10. i måneden etter. Siste publisering 9.10.2026 (september), neste 10.11.2026 [K1] |
| Basisår | 2025 = 100 fra januar 2026. Før var det 2015 = 100 [K2] |
| Klassifisering | COICOP 2018 fra januar 2026, med 13 hovedgrupper i stedet for 12. «Forsikring og finansielle tjenester» er ny egen gruppe [K2] |
| Vekter | Husholdningenes konsum i nasjonalregnskapet. Oppdateres hver januar og holdes faste gjennom året [K3] |
| Datakilder | Strekkodedata for mat, drikke, dagligvarer, apotekvarer og drivstoff. Bilpriser fra OFV. Strømpriser fra nettet. Månedlig undersøkelse blant knapt 2 000 virksomheter. Husleie fra et fast utvalg på om lag 2 500 utleieboliger [K3] |
| Revisjon | Originale indekser revideres ikke. Sesongjusterte serier revideres fire år tilbake [K3] |
| Avledede serier | KPI-JA (justert for avgiftsendringer), KPI-JE (uten energivarer), KPI-JAE (begge), KPI-JEL (uten elektrisitet), KPI-XADM (uten administrerte priser) med varianter [K3], [K5] |
| Bruk | Departementer, Norges Bank, partene i arbeidslivet, finans og analyse. Mye brukt til å regulere kontraktsbeløp [K3] |
| Bruksvolum | Nr. 5 blant statistikkene etter uttak fra statistikkbanken i 2026, med 52 412 uttak (regnearket «Bruk av statbank») |

## 2. Nøkkelbudskap (september 2026)

1. **Prisene var 3,4 prosent høyere enn for ett år siden** [K1], [K5].
2. **Den underliggende prisveksten, målt med KPI-JAE, var 3,0 prosent** [K1], [K5].
3. **Prisveksten er langt lavere enn toppen i 2022**, da tolvmånedersveksten var 7,5 prosent i oktober. Siden juli 2024 har den ligget mellom 2,3 og 3,6 prosent [K5].
4. **Tjenester stiger mer enn varer:** 3,8 mot 3,0 prosent [K1].
5. **Bolig er den største posten.** Bolig, lys og brensel veier 31 prosent av KPI i 2026. Av dette er beregnet husleie for selveiere alene 21 prosent [K5]. Vekten for beregnet husleie økte fra 13,9 til 20,6 prosent i 2026 etter revisjonen av nasjonalregnskapet [K3].
6. **Bolig bidrar mest til prisveksten.** Et grovt anslag (vekt × endring) gir om lag 1,1 av de 3,4 prosentpoengene fra bolig, 0,7 fra transport og 0,4 fra restauranter og overnatting [K5, egen beregning].
7. **Politiske vedtak slår ut i KPI.** Strømstøtten regnes som en negativ avgift, og lavere priser på barnehage og SFO trakk KPI ned med om lag 0,4 prosentpoeng fra august 2025 [K7].
8. **KPI-JA er høyere enn KPI, 5,2 mot 3,4 prosent.** I 2023–2025 skyldtes forskjellen særlig strømstøtten [K7]. Hvorfor gapet har økt gjennom 2026, er ikke avklart (se del 7).

## 3. Vanskelige begreper

- **Indeks mot endring.** Indeksen for september 2026 er 104,0 med 2025 = 100 [K1]. Tallet sier hvor høyt prisnivået er i forhold til gjennomsnittet i 2025, ikke hvor mye prisene steg siste år [T].
- **Månedsendring mot tolvmånedersendring.** Klær steg 4,0 prosent fra august til september, men bare 2,2 prosent på tolv måneder [K5]. Månedstall påvirkes av salg, sesong og tidspunkt for påske [K7].
- **De avledede seriene.**
  - KPI-JA: justert for avgiftsendringer.
  - KPI-JE: uten energivarer.
  - KPI-JAE: begge deler. NOU 2026:5 omtaler den som den underliggende inflasjonen [K7].
  - KPI-XADM: uten priser myndighetene i stor grad bestemmer, som husleie i Vinmonopolet, nettleie, kommunale avgifter og barnehage [K3].
  - Bokstavene er korte og ligner hverandre [T].
- **Beregnet husleie.** Selveiernes boligkonsum måles som hva det ville kostet å leie den samme boligen, kalt leieekvivalensprinsippet. Kjøpesummen for boligen er ikke med [K4].
- **Vekter i promille.** Hovedgruppenes vekter summerer til 1 000 [K5].
- **Bidrag til endringen.** En gruppes bidrag avhenger av både vekt og prisendring. En gruppe med kraftig prisvekst og liten vekt bidrar lite [K6]. Forsikring og finansielle tjenester steg 7,9 prosent, men veier bare 2,7 prosent [K5].
- **Prisutvikling, ikke prisnivå.** Matvareindeksen sammenligner samme vare over tid, med tilbud og rabatter, og vektes etter løpende omsetning [K8].

## 4. Sannsynlige misforståelser

Alle punktene er hypoteser [H] til fagkontakten har vurdert dem.

| | Misforståelse | Grunnlag | Hva prototypen må gjøre |
|---|---|---|---|
| H1 | Lavere prisvekst leses som at prisene faller | Vanlig forveksling av nivå og vekst [T] | Vise nivå og vekst hver for seg, og si det med ord |
| H2 | KPI forventes å stemme med «min» prisvekst | KPI viser gjennomsnittshusholdningen med faste vekter [K3]. Bolig veier 31 prosent, mat 10 prosent [K5] [T] | Vise hva som er med og hvor mye det veier |
| H3 | Renter og boligpriser antas å være med | De er ikke med. Bolig inngår som husleie og beregnet husleie [K4] | Lage en «dette er ikke med»-boks |
| H4 | KPI-JA og KPI-JAE forveksles, eller KPI-JAE leses som «den egentlige» prisveksten | Like navn [T]. KPI-JA er nå høyere enn KPI, mens KPI-JAE er lavere [K5] | Forklare seriene med navn og formål, ikke bare bokstaver |
| H5 | Indeksverdien leses som prosentvis endring, eller tall med gammelt basisår sammenlignes med nye | Basisåret ble endret til 2025 = 100 i 2026 [K2] [T] | Vise endringer, ikke indeksnivå, i hovedbudskapet. Merke basisår |
| H6 | Store månedsendringer leses som trender | Sesong, salg og påske gir utslag [K7] [T] | Bruke tolvmånedersvekst som hovedmål |
| H7 | Gruppen med høyest prisvekst antas å drive KPI | Bidrag = vekt × endring [K6] | Vise bidrag, ikke bare endring |
| H8 | Lavere KPI etter politiske vedtak leses som at markedsprisene faller | Strømstøtte og barnehagepriser [K7] | Forklare at KPI måler hva husholdningene betaler |
| H9 | KPI for mat sammenlignes med medienes handlekurver | Matvareindeksen sammenligner like varer over tid med løpende vekter [K8] [T] | Lav prioritet. Mulig fotnote |
| H10 | «SSB undervurderer prisveksten» | Målefeil er anslått til 0,4–1,1 prosentpoeng per år, med retning ikke oppgitt i kilden [K3] | Lav prioritet. Avklares med fag før det brukes |

## 5. Brukere og hva de trenger [T]

- **Husholdninger og journalister:** siste tall, om prisene stiger mer eller mindre enn før, og hvorfor.
- **Den som skal regulere en kontrakt, husleie eller et beløp:** riktig tall for riktig måned, og hvordan man regner. SSB har egen priskalkulator.
- **Partene i arbeidslivet og økonomer:** tolvmånedersvekst, KPI-JAE og bidrag. Disse henter trolig tallene i statistikkbanken og trenger mest å bli sendt videre.

Prototypen skal gi riktig førsteinntrykk og forklare de vanskelige begrepene. Den skal ikke erstatte statistikkbanken eller priskalkulatoren [T].

## 6. Prioritering: spørsmål prototypen bør svare på

**Kriterier:**

- (a) Spørsmålet er sentralt i SSBs egne nøkkelbudskap.
- (b) Faren for misforståelse er stor.
- (c) Spørsmålet kan besvares med tall fra statistikkbanken.
- (d) Det passer i en oversikt, ikke et analyseverktøy.

| Prioritet | Spørsmål | Kriterier | Hypoteser | Mulig kilde (verifiseres i steg 3) |
|---|---|---|---|---|
| 1 | Hvor mye stiger prisene nå, og er det mye? | a b c d | H1 H5 H6 | 14700 og 14706, tolvmånedersvekst over tid |
| 2 | Hva driver prisveksten? | a b c d | H7 | 14700, vekter og endring per hovedgruppe |
| 3 | Hva er med i KPI, og hvor mye veier det? | b c d | H2 H3 | 14700, vekter |
| 4 | Hvorfor finnes det flere KPI-er? | a b c | H4 H8 | 14706 |
| 5 | Hva er en krone verdt over tid? | c d | H5 | 14710, historisk serie fra 1920 |

**Må med uansett:** en kort «Slik leser du KPI»-boks som dekker H1, H3, H5 og H6, og en linje om basisår og ny klassifisering fra 2026.

**Kan vente:** sesongjusterte serier, leveringssektor, harmonisert KPI (HKPI) og de mer enn 300 detaljerte varegruppene.

**Utenfor:** prognoser og Norges Banks egne indikatorer, som ikke er SSB-statistikk.

## 7. Spørsmål vi tar med til fagkontakten (grunnlag for steg 5)

1. Stemmer H1–H10? Hvilke misforståelser møter dere oftest?
2. Hvorfor har gapet mellom KPI-JA (5,2) og KPI (3,4) økt gjennom 2026? Er det fortsatt strømstøtten, og hvordan inngår Norgespris?
3. Hvilken av KPI og KPI-JAE bør stå som hovedtall i en formidlingsside?
4. Er det riktig å vise et grovt anslag på bidrag (vekt × endring), eller bør vi bare bruke SSBs egen metode?
5. Hvordan bør målefeilen i H10 omtales, om i det hele tatt?
6. Finnes det ofte stilte spørsmål eller henvendelser vi bør bygge på?

## Hull i grunnlaget

- **Media:** ingen gjennomgang av mediebruk er gjort. Hypotesene bygger på SSBs og NOU-ens egne tekster og våre tolkninger.
- **Sammendragsverktøy:** kildene er lest gjennom et sammendragsverktøy. Sitater og tall er sjekket mot statistikkbanken der det var mulig.
- **Vekten for beregnet husleie:** 13,9 prosent for 2025 er hentet fra «Om statistikken» [K3], ikke fra statistikkbanken.
- **Bidragstallene** er et grovt anslag. SSBs metode tar hensyn til vektskiftet i januar [K6] og beregnes riktig i steg 3.
- **Fagkontakter:** «Om statistikken» viser bare et telefonnummer. Forfattere av artiklene er Espen Kristiansen, Ragnhild Nygaard og Fredrik Lorentz Stende. Hvem som er riktig kontakt, er ikke avklart.

## Kilder

- [K1] SSB: Konsumprisindeksen, statistikkside, oppdatert 9.10.2026. https://www.ssb.no/kpi
- [K2] Kristiansen: «Ny konsumklassifisering og nytt basisår i KPI fra 2026», 10.12.2025, endret 13.3.2026. https://www.ssb.no/priser-og-prisindekser/konsumpriser/statistikk/konsumprisindeksen/artikler/ny-konsumklassifisering-og-nytt-basisar-i-kpi-fra-2026
- [K3] SSB: Om statistikken, Konsumprisindeksen. https://www.ssb.no/priser-og-prisindekser/konsumpriser/statistikk/konsumprisindeksen
- [K4] Kristiansen: «Hvordan fanges bokostnader opp i KPI?», 5.7.2024. https://www.ssb.no/priser-og-prisindekser/konsumpriser/artikler/hvordan-fanges-bokostnader-opp-i-kpi
- [K5] Statistikkbanken, tabell 14700 og 14706, hentet 14.10.2026
- [K6] Nygaard: «Hvor mye påvirker enkeltgrupper den totale prisendringen i KPI?», 10.8.2017. https://www.ssb.no/priser-og-prisindekser/artikler-og-publikasjoner/hvor-mye-pavirker-enkeltgrupper-den-totale-prisendringen-i-kpi
- [K7] NOU 2026:5 Grunnlaget for inntektsoppgjørene 2026, kapittel 3. https://www.regjeringen.no/no/dokumenter/nou-2026-5/id3155079/?ch=4
- [K8] Nygaard: «Slik beregner SSB prisutviklingen på matvarer», 8.9.2022. https://www.ssb.no/priser-og-prisindekser/konsumpriser/artikler/slik-beregner-ssb-prisutviklingen-pa-matvarer
- [K9] SSB: «Endringer i konsumprisindeksen (KPI)», endret 10.2.2026. https://www.ssb.no/priser-og-prisindekser/konsumpriser/statistikk/konsumprisindeksen/artikler/endringer-i-konsumprisindeksen-kpi

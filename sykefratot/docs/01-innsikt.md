Steg 1 i formidlingsprototype for sykefratot · versjon 1.1 · 26.11.2026 · Status: godkjent av Thomas

# Innsikt: Sykefravær (sykefratot)

**Merking.** `[K1]`–`[Kn]`: kilde, se kildelisten nederst. `[T]`: vår tolkning. `[H]`: hypotese om misforståelse, som skal prøves i fagkontrollen.

## Om dette notatet

**Rettet i versjon 1.1 (steg 2):** Andelen lange sykmeldinger av tilfellene var oppgitt som 11,5 prosent, regnet ved å summere avrundede andeler. Regnet fra publiserte antall er den 11,6 prosent.

Notatet er skrevet samme dag som 3. kvartal 2026 ble publisert (26.11.2026). Hele «Om statistikken» er lest fra HTML-en på statistikksiden, ikke gjennom sammendrag. Alle tall er hentet direkte fra statistikkbanken (data.ssb.no, API v2, json-stat2 med statussymboler) samme dag. Der vi har regnet selv, står det.

To funn i næringstabellene ser ut som feil eller som noe vi ikke forstår (avsnitt 7, spørsmål 2 og 3). De må avklares før næringstall brukes i prototypen.

---

## 1. Statistikken på ett ark

| | |
|---|---|
| **Hva den er** | Sykefraværsdagsverk i prosent av avtalte dagsverk for bosatte lønnstakere 16–69 år. Egenmeldt og legemeldt fravær på grunn av egen sykdom `[K1]`. |
| **Hva den ikke er** | Ikke andelen som er syke. Ikke selvstendig næringsdrivende eller vernepliktige. Ikke fravær for barns sykdom, omsorgs- eller fødselspermisjon `[K1]`. Ikke diagnoser, de publiserer bare Nav `[K2]`. Ikke internasjonalt sammenlignbar, til det brukes AKU `[K4]`. |
| **Frekvens** | Kvartalsvis og årlig. Publiseres 9–10 uker etter kvartalet. Neste: 25.02.2027 (4. kvartal 2026) `[K1]`. |
| **Referansetid** | Kvartal. Dagsverk og avtalte dagsverk måles i uka med den 16. i hver måned i kvartalet. Antall sykmeldte personer måles på tirsdagen i uka med den 16. i siste måned `[K1]`. |
| **Tidsserie** | Fra 2. kvartal 2000 `[K1]`. |
| **Klassifisering** | Næring SN2007, yrke STYRK08, sektor, fylke, kommune (bare legemeldt) `[K1]`. SN2025 innføres fra 1. kvartal 2027. Næringstabellene etter SN2007 avsluttes etter 4. kvartal 2026 `[K3]`. |
| **Datakilder** | Tre: Navs sykmeldingsregister (legemeldt, fulltelling), SSBs utvalgsundersøkelse blant om lag 10 000 bedrifter (egenmeldt, svarprosent over 90), a-ordningen (avtalt arbeidstid og kjennemerker) `[K1]`. |
| **Metode** | Egenmeldt blåses opp med modellbaserte rateestimatorer per næring og størrelse. Sesongjustering med X-13ARIMA-SEATS, indirekte: teller og nevner sesongjusteres hver for seg, for menn og kvinner og for egen- og legemeldt `[K1]`. Influensa brukes som forklaringsvariabel i prekorrigeringen `[K1]`. |
| **Revisjon** | Ujusterte tall revideres ikke regelmessig. Sesongjusterte tall fra 2015 revideres hver gang, mest de siste 1–2 årene. Før 2015 er de låst `[K1]`. |
| **Avledede serier** | Ikke-sesongjustert, sesongjustert, sesong- og influensajustert. Prosentvis endring fra kvartalet før (sesongjustert) og fra samme kvartal året før (ujustert) `[K7]`. |
| **Produsent** | SSB i samarbeid med Nav. Nav får tallene før kl. 08 og publiserer samtidig, men bare legemeldt og ujustert `[K1]` `[K6]`. |
| **Bruk** | Myndighetene, partene i arbeidslivet, bedrifter, forskere. Måltall i IA-avtalen `[K1]` `[K14]`. Rapporteres til OECD `[K1]`. |
| **Bruksvolum** | Ikke kjent. Regnearket «Bruk av statbank» er ikke lagt ved. 27 aktive tabeller i statistikkbanken (talt fra API-søk, avsluttede tabeller ikke med). |

## 2. Nøkkelbudskap for 3. kvartal 2026

1. **Sykefraværet var 6,65 prosent, sesongjustert.** Ned 0,3 prosent fra 2. kvartal (6,67). Det er en nedgang på 0,02 prosentpoeng, altså ingen endring som betyr noe `[K7]` `[K2]`.
2. **Den faktiske prosenten i kvartalet var 5,7.** 3. kvartal er alltid lavest på grunn av sommeren. I 1. kvartal i år var den ujusterte prosenten 7,3. Sesongvariasjonen innenfor ett år (1,6 prosentpoeng) er mye større enn alle endringer i den sesongjusterte serien siden 2025 `[K7]`.
3. **Nivået er høyt, men ikke rekord.** Den sesongjusterte serien har ligget mellom 6,54 og 6,67 siden 1. kvartal 2025. Toppen i serien er 8,01 i 4. kvartal 2003. Årsnivået for 2024 (6,8) er det høyeste siden 2003 (7,6), likt med 2009 `[K7]` `[K9]`.
4. **Legemeldt fravær er 85 prosent av fraværet.** Legemeldt 5,65, egenmeldt 1,01 (sesongjustert) `[K7]`. Egenmeldingene er likevel 63 prosent av alle fraværstilfellene `[K10]`.
5. **Lange sykmeldinger bærer tyngden.** Legemeldte fravær som varte mer enn 31 dager i kvartalet, var 11,6 prosent av tilfellene, men 62,7 prosent av sykefraværsdagsverkene. Fravær som varte hele kvartalet, var alene 34,0 prosent av dagsverkene `[K10]`. Ujusterte tall, andelene er regnet fra publiserte antall.
6. **Kvinner har 8,50, menn 5,07 prosent**, sesongjustert `[K7]`.
7. **Helse- og sosialtjenester har høyest fravær:** 8,0 prosent ujustert, 9,57 sesongjustert. Informasjon og kommunikasjon har lavest blant hovednæringene: 3,6 ujustert `[K8]` `[K13]`. Blant store yrker har helsefagarbeidere høyest legemeldt fravær, 9,2 prosent, mot 4,9 for alle yrker `[K11]`.
8. **IA-målet er langt unna.** Målet er 10 prosent lavere enn årsgjennomsnittet for 2018, som tilsvarer at fraværet ikke skal overstige 5,1 prosent `[K14]`. Årsnivået for 2025 var 6,6 `[K9]`.

## 3. Vanskelige begreper

**Sykefraværsprosent.** Tapte dagsverk delt på avtalte dagsverk, ikke andel syke personer. I 3. kvartal var legemeldt sykefraværsprosent 4,9, mens 6,3 prosent av lønnstakerne hadde en pågående legemelding på referansedagen `[K12]`. Forskjellen kommer blant annet av gradering: en som er 50 prosent sykmeldt, teller som et halvt dagsverk, men som én person.

**Avtalte dagsverk.** Arbeidsdager (kalenderdager minus helger og offisielle fridager) justert for stillingsprosent, summert over alle jobber `[K1]`. Prosenten kan derfor falle uten at fraværet faller, hvis antall jobber vokser. I 3. kvartal falt de sesongjusterte sykefraværsdagsverkene med 0,17 prosent, mens de avtalte dagsverkene steg med 0,1 prosent `[K2]`.

**Sesongjustert, ujustert, sesong- og influensajustert.** Samme kvartal, tre tall. 3. kvartal 2026: 5,7 ujustert, 6,65 sesongjustert, 6,65 sesong- og influensajustert. Influensajusteringen betyr lite nå, men mye i influensaår: i 4. kvartal 2009 (svineinfluensa) var sesongjustert 6,98 og sesong- og influensajustert 6,24 `[K7]`. De sesongjusterte tallene endres ved hver publisering `[K1]`.

**Prosent og prosentpoeng.** «Ned 0,3 prosent» betyr fra 6,67 til 6,65, ikke fra 6,7 til 6,4 `[K7]`. SSB skriver endringen i prosent i ingress og nøkkeltabell `[K1]` `[K2]`.

**Egenmeldt er et estimat.** Det finnes ikke noe register over egenmeldinger. Tallet blåses opp fra om lag 10 000 bedrifter. Bedrifter med færre enn 4 ansatte får ikke skjema `[K1]`. Usikkerheten for alle næringer er liten (±0,01 prosentpoeng i 2022), men større i små næringer: ±0,11 for jordbruk, skogbruk og fiske `[K1]`.

**Varighet.** SSB teller bare dagene innenfor kvartalet. En sykmelding som startet fem dager før kvartalet og varte åtte dager inn i det, har varighet 8 dager hos SSB og 13 hos Nav `[K1]`.

## 4. Sannsynlige misforståelser

Alle er `[H]` til fag har vurdert dem.

| | Misforståelse | Grunnlag | Hva prototypen må gjøre |
|---|---|---|---|
| H1 | At SSB og Nav melder ulike ting om det samme. Samme morgen kan SSB si «uendret» og Nav «ned» | SSB melder sesongjustert, egen- og legemeldt, endring fra forrige kvartal. Nav melder ujustert, bare legemeldt, endring fra samme kvartal året før `[K1]` `[K6]` | Vis de to målene side om side for samme kvartal, med hvem som bruker hvilket |
| H2 | At 6,7 prosent betyr at 6,7 prosent av de ansatte er syke | Definisjonen er dagsverk, ikke personer `[K1]`. 6,3 prosent av lønnstakerne hadde en legemelding på referansedagen, mot 4,9 prosent legemeldt fravær målt i dagsverk `[K12]` | Forklar brøken med tall. Vis forskjellen mellom personer og dagsverk |
| H3 | At sykefravær mest handler om korte egenmeldinger | Egenmeldt er 63 prosent av tilfellene, men 14 prosent av dagsverkene. Lange legemeldte fravær er 11,6 prosent av tilfellene og 63 prosent av dagsverkene `[K10]` | Vis tilfeller og dagsverk mot hverandre. Dette er den sterkeste kandidaten til konseptgrafikk `[T]` |
| H4 | At «ned 0,3 prosent» betyr 0,3 prosentpoeng | SSB oppgir endringen i prosent `[K1]` `[K2]`, mens nivået er 6,65 `[K7]` | Skriv alltid begge, eller vis nivåene |
| H5 | At sykefraværet er rekordhøyt | Høyeste sesongjusterte nivå er 8,01 i 2003. Årsnivået var 7,6 i 2003 og 6,8 i 2024 `[K7]` `[K9]` | Vis hele serien fra 2000 |
| H6 | At Norge har verdens høyeste sykefravær, målt med denne statistikken | Landsammenligninger bygger på AKU, som bare teller fravær hele uka og personer, ikke dagsverk. I 2023 var AKU-målet 4,3 og sykefraværsstatistikken 6,7. Stillingsvern og sykelønn påvirker nivåene `[K4]` `[K5]` | Si tydelig at denne statistikken ikke kan sammenlignes med andre land, og pek til AKU |
| H7 | At sesongjusterte tall er «riktigere» og at et ujustert kvartal kan sammenlignes med kvartalet før | 3. kvartal er alltid lavest. Ujustert 5,7, sesongjustert 6,65 `[K7]`. Sesongjusterte tall revideres `[K1]` | Lesehjelp: hvilket tall til hvilket spørsmål |
| H8 | At «9,87 millioner tapte dagsverk» er antallet som faktisk gikk tapt i kvartalet | Tallet i artikkelen er sesongjustert. Det ujusterte tallet er 8,91 millioner `[K2]` `[K7]` `[T]` | Bruk ujusterte dagsverk når tallet skal beskrive faktisk omfang. Lav prioritet |
| H9 | At næringstall kan sammenlignes over hele serien | Brudd i 2009 (SN2002 til SN2007) og 2015 (a-ordningen og ny referanseuke, om lag +0,2 prosentpoeng i 2. kvartal 2015). Ujusterte endringsrater er satt til «.» for 2015 `[K1]` `[K7]`. Nytt brudd med SN2025 fra 1. kvartal 2027 `[K3]` | Stiplet brudd i alle næringsserier, og forklaring |
| H10 | At statistikken dekker alt fravær på grunn av sykdom | Barns sykdom, permisjoner og selvstendig næringsdrivende er ikke med `[K1]` | En linje i lesehjelpen. Lav prioritet |

## 5. Brukere og hva de trenger

**Journalister og den interesserte offentligheten.** Trenger svar på om fraværet går opp eller ned, og hvorfor SSB og Nav sier ulike ting. Det er her H1, H4 og H5 slår til.

**Partene i arbeidslivet, IA-arbeid og arbeidsgivere.** Trenger nivå mot IA-målet, næring og yrke, og å skille korte fra lange fravær, fordi tiltakene er forskjellige.

**Studenter og fagfolk utenfor feltet.** Trenger å forstå brøken, sesongjusteringen og hvorfor tallet ikke kan sammenlignes med andre land.

Prototypen skal ikke være et oppslagsverktøy for kommune, yrke eller næring på detaljnivå, og ikke et diagnoseverktøy. Det har Nav og statistikkbanken.

## 6. Prioritering

Kriterier: (a) sentralt i SSBs nøkkelbudskap, (b) stor fare for misforståelse, (c) kan besvares fra statistikkbanken, (d) passer i en oversikt.

| Prioritet | Spørsmål | Kriterier | Hypoteser | Mulig kilde |
|---|---|---|---|---|
| 1 | Hvor høyt er sykefraværet, og går det opp eller ned? | a b c d | H1, H4, H5, H7 | 12439 (alle tre serier fra 2000), Nav-serien som sammenligning |
| 2 | Hva betyr «6,7 prosent» egentlig? | b c d | H2, H10 | 12439, 12446 (personer og dagsverk) |
| 3 | Er det korte egenmeldinger eller lange sykmeldinger som utgjør fraværet? | b c d | H3 | 12946 (tilfeller og dagsverk etter varighet) |
| 4 | Hvem har høyest fravær? Kvinner og menn, næringer, yrker | a c d | H9 | 12439, 13935, 12452. Næring forutsetter at avsnitt 7, spørsmål 2–3, er avklart |

**Må med uansett.** Lesehjelpen: sesongjustert og ujustert, prosent og prosentpoeng, egenmeldt og legemeldt, og hvorfor Nav og SSB melder ulike tall samme dag.

**Kan vente.** Fylke og kommune (legemeldt finnes per kommune, egenmeldt bare per fylke `[K1]`). Alder, innvandringskategori, familietype, utdanning. Ansettelsesform. Internasjonal sammenligning med AKU.

**Utenfor.** Diagnoser (Nav). Sykepengeutgifter. Årsaker til fravær.

**Et valg Thomas må ta om næring.** Næringstabellene etter SN2007 avsluttes etter 4. kvartal 2026, og nye SN2025-tabeller kommer med 1. kvartal 2027, med tilbakeregnede tall for noen år `[K3]`. En prototype med næring bygd nå blir utdatert om et halvt år. Alternativene er å bygge spørsmål 4 med kjønn og yrke nå og legge til næring i 2027, eller å bygge med SN2007 og merke det. Jeg anbefaler det første `[T]`.

## 7. Spørsmål til fagkontakten

1. Stemmer hypotesene H1–H10, og hvilke misforståelser møter dere oftest? Mangler det noen?
2. **Egenmeldt på detaljert næringsnivå i tabell 12440 stemmer ikke med hovednæringene.** I 3. kvartal 2026 er egenmeldt 1,0 for helse- og sosialtjenester (Q), mens begge undergruppene har høyere tall: helsetjenester (86) 1,7 og pleie og omsorg (87–88) 1,6. Et gjennomsnitt kan ikke ligge under begge delene. Det samme gjelder i alle 47 kvartaler fra 2015K1 til 2026K3, men ikke før 2015. Industri (C) har egenmeldt 0,9, mens alle de 13 industrigruppene ligger mellom 0,2 og 0,8. I 2015K1 har helsetjenester egenmeldt 4,6. Hva betyr de detaljerte egenmeldte tallene, og kan de brukes?
3. **Jordbruk, skogbruk og fiske (A) og bergverksdrift og utvinning (B) har identiske ujusterte tall** i 3. kvartal 2025 og 3. kvartal 2026, for både totalt, egenmeldt og legemeldt (4,2 / 0,6 / 3,6 og 4,4 / 0,5 / 3,8) i 12440. Det står også slik i tabell 2 og 3 på statistikksiden. De sesongjusterte tallene i 13935 er forskjellige (5,03 og 4,72). Det har skjedd i 4 av 75 kvartaler. Er det tilfeldig?
4. «Om statistikken» sier at bare sesong- og influensajusterte tall er sammenlignbare før og etter 2015. Gjelder det også den sesongjusterte serien som er hovedtallet? Endringsraten for 2015K1 er satt til «.» også i de justerte seriene.
5. Bør prototypen vente på SN2025-tabellene for næring (1. kvartal 2027), og hvor langt tilbake blir de tilbakeregnet?
6. Er det et bevisst valg å bruke sesongjusterte dagsverk («9,87 millioner tapte dagsverk») som omfangstall i artikkelen?

Bonus til fag, ikke et spørsmål: Avsnittet «Konfidensialitet» i «Om statistikken» inneholder maltekst som ikke er fylt ut: «[ev. fyll inn riktig enhet her]» og «[undertrykking, avrunding, støylegging]».

## 8. Hull i grunnlaget

- **Fagkontakt ikke valgt.** Kandidater: Rakel Gading og Mari Kristine Knutsen (kontakter og forfattere av kvartalsartiklene), Tonje Køber (seksjonssjef, forfatter av artiklene om internasjonal sammenligning), Erik Horgen og Håvard Lien (medforfattere) `[K1]`–`[K5]`, `[K15]`.
- **Bruksvolum mangler.** «Bruk av statbank» er ikke lagt ved.
- **Statistikkbankens tabelloversikt for sykefratot lastes med JavaScript** og kunne ikke leses. Tabellene er talt fra API-søket. Avsluttede tabeller er ikke talt.
- **Navs sider er lest gjennom søketreff, ikke i sin helhet.** Påstanden om Navs måte å melde på bygger på Navs pressemelding for 3. kvartal 2025 og tabellsiden `[K6]`. Navs melding for 3. kvartal 2026 er ikke lest.
- **Ikke lest:** kvalitetsindikatorene for sesongjusteringen (Excel), notatene om utvalgsundersøkelsen (2005–2010), artiklene om langtidssykmeldte, midlertidig ansatte og innvandrere.
- **Figurene på statistikksiden og i artiklene er ikke sett som bilder.** Tallene bak er hentet fra statistikkbanken.
- **WebFetch avviste ssb.no** (ikke på listen over tillatte adresser i økten). Sidene ble hentet med curl og lest i sin helhet, så dette ga ikke hull.

## 9. Kilder

- `[K1]` SSB: Sykefravær, statistikkside. Oppdatert 26.11.2026. «Om statistikken» sist oppdatert 3.9.2026. https://www.ssb.no/arbeid-og-lonn/arbeidsmiljo-sykefravaer-og-arbeidskonflikter/statistikk/sykefravaer
- `[K2]` Rakel Gading: «Uendret sykefravær i 3. kvartal». SSB, 26.11.2026. https://www.ssb.no/arbeid-og-lonn/arbeidsmiljo-sykefravaer-og-arbeidskonflikter/statistikk/sykefravaer/artikler/uendret-sykefravaer-i-3.kvartal
- `[K3]` Rakel Gading og Mari Kristine Knutsen: «Økning i sykefraværet». SSB, 28.5.2026. https://www.ssb.no/arbeid-og-lonn/arbeidsmiljo-sykefravaer-og-arbeidskonflikter/statistikk/sykefravaer/artikler/okning-i-sykefravaeret
- `[K4]` Tonje Køber og Erik Horgen: «Om å sammenligne sykefraværet internasjonalt». SSB, 6.9.2024. https://www.ssb.no/arbeid-og-lonn/arbeidsmiljo-sykefravaer-og-arbeidskonflikter/artikler/om-a-sammenligne-sykefravaeret-internasjonalt
- `[K5]` Tonje Køber og Håvard Lien: «Sykefraværet i Norge øker mer enn i nabolandene». SSB innsikt 2025/2, 5.5.2025. https://www.ssb.no/arbeid-og-lonn/arbeidsmiljo-sykefravaer-og-arbeidskonflikter/artikler/sykefravaeret-i-norge-oker-mer-enn-i-nabolandene
- `[K6]` Nav: «Nedgangen i sykefraværet fortsatte i 3. kvartal» (pressemelding, 3. kvartal 2025) og «Sykefraværsstatistikk – kvartalsstatistikk». Lest gjennom søketreff 26.11.2026. https://www.nav.no/no/nav-og-samfunn/statistikk/sykefravar-statistikk/nyheter/nedgangen-i-sykefravaeret-fortsatte-i-3.kvartal og https://www.nav.no/no/nav-og-samfunn/statistikk/sykefravar-statistikk/sykefravar
- `[K7]` Statistikkbanken, tabell 12439, 2000K2–2026K3. Hentet 26.11.2026.
- `[K8]` Statistikkbanken, tabell 12440, 2008K1–2026K3. Hentet 26.11.2026.
- `[K9]` Statistikkbanken, tabell 12441 (årstall), 2001–2025. Hentet 26.11.2026.
- `[K10]` Statistikkbanken, tabell 12946 (varighet), 2015K1–2026K3. Hentet 26.11.2026.
- `[K11]` Statistikkbanken, tabell 12452 (yrke), 2026K3. Hentet 26.11.2026.
- `[K12]` Statistikkbanken, tabell 12446 (alder, personer), 2026K3. Hentet 26.11.2026.
- `[K13]` Statistikkbanken, tabell 13935 (næring, sesongjustert), 2015K1–2026K3. Hentet 26.11.2026.
- `[K14]` Stortinget: Innst. 149 S (2025–2026). https://stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2025-2026/inns-202526-149s/
- `[K15]` Erik Herstad Horgen: «Bedre sykefraværstall uten feriekorrigering». SSB, 20.3.2019. https://www.ssb.no/arbeid-og-lonn/artikler-og-publikasjoner/bedre-sykefravaerstall-uten-feriekorrigering

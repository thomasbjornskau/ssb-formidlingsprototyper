Steg 5 i formidlingsprototype for arbstatus-neet · versjon 0.1 · 10.11.2026 · Status: til faglig kontroll

# Kvalitetssikringsliste: unge utenfor

Denne listen erstatter listene i `02-kvalitetssikring.md`, `03-kildekart.md` (hull og hindre) og `04-byggenotat.md` (nye valg). Den samler alt som er tolkning, eget valg eller ubekreftet.

Prototype: https://thomasbjornskau.github.io/ssb-formidlingsprototyper/arbstatus-neet/

**Del A** er det som kan være feil, eller som gir et misvisende inntrykk hvis det er feil. **Del B** kan leses når det passer. **Del C** er spørsmål. Korte svar holder, også bare «ok» eller «feil».

Tallene er hentet fra statistikkbanken (tabell 12424, 12427, 14158 og 13347) 10.11.2026 og kontrollert ved bygging: 19 kontroller over 217 441 celler, blant annet at NEET summert fra 12424 avviker høyst 6 personer fra NEET i tabell 13556. Tallene for 2025 er foreløpige.

## A. Må avklares

| # | Påstand eller valg | Hvor | Grunnlag | Hva som må sjekkes |
|---|---|---|---|---|
| 1 | NEET er bygd av tre statuser: registrerte ledige (A.09) + AAP/uføretrygd (U.04-U.05) + «andre, ikke på tiltak» (U.90B, som omfatter ukjent status). I forløpstabellene: A.09 + U.04-U.05 + U.90A i startåret og U.90E senere | Hele siden | Summen i 12424 er lik NEET-koden i 13556 for alle år, kjønn og alder (avvik høyst 6 personer). 12427 gjenskaper 12424 i startåret | At dette er riktig måte å lage NEET på i 12424, 12427 og 14158. Særlig: er U.90A og U.90E det samme, og hva er forskjellen? |
| 2 | **Strøm inn:** 47 232 gikk fra arbeid, utdanning eller tiltak i 2024 til utenfor i 2025. **Strøm ut:** 38 900 motsatt vei. Beskrevet som en nedre grense | Nøkkeltall, «Hvor mange blir nye i gruppen?», påstandsprøven | Egen beregning fra 12427. Status måles i november; korte opphold innenfor året og nye 15-åringer er ikke med | At metoden er forsvarlig, og at «nedre grense» er riktig beskrivelse. Bruker dere selv slike tall? |
| 3 | **«Utenforskapet varer lenger enn før.»** Andelen som fortsatt var utenfor året etter, økte fra 49,9 prosent (2008) til 57,9 prosent (2024). Fem år etter: fra 35 til 39 prosent (2008 og 2020) | Ingressen øverst, «Hvor lenge er de utenfor?», påstandsprøven (dom: støttet) | Egen beregning fra 12427. «Fortsatt utenfor» betyr utenfor i november det året, ikke sammenhengende | Om konklusjonen tåler endringene i datagrunnlaget i perioden (a-ordningen 2015, AAP 2010, ukjent status). Dette er hovedbudskapet i prototypen |
| 4 | **Toppgrafikken: «Dobbelt så mange unge utenfor er på AAP eller uføretrygd som i 2008»** (12 462 → 27 621, faktor 2,2). Varigheten på AAP/uføretrygd fem år etter: 62,5 prosent (2008), 56,8 (2010), 70,0 (2020) | Toppgrafikken, «Hvor lenge er de utenfor?» | 12424 og 12427. «Om statistikken» sier at statusgrupperingen før 2015 er lagt om for å unngå brudd | Om AAP og uføretrygd er sammenlignbare tilbake til 2008, gitt AAP-reformen 2010 og uførereformen 2015. Hvis ikke: start serien i 2010, eller marker brudd |
| 5 | **Innvandrere:** 73 prosent av innvandrere som er utenfor, har ukjent status (41 prosent ellers). 29 prosent av dem som var utenfor i 2020, var ute av befolkningen fem år senere (3 prosent ellers). Tolkning på siden: kortere varighet blant innvandrere er ikke det samme som bedre utfall | «Innvandrere og befolkningen ellers», påstandsprøven | 12424, 12427. Faktasiden om NEET og artikkelen fra desember 2025 om ukjent status | At tolkningen er rimelig. Hvor stor del av ukjent status anslår dere er uregistrert utvandring? |
| 6 | **25–29-åringer med studieforberedende uten mer utdanning er 2,1 ganger så ofte utenfor som dem med yrkesfag** (16,8 mot 8,2 prosent), og flere blir værende (42 mot 32 prosent fem år etter 2020) | «Hvem er i størst fare?», tittel og ingress | Egen beregning fra 14158 | Om gruppen blander dem som har avbrutt høyere utdanning med dem som aldri begynte, og om funnet kan stå i en tittel |
| 7 | **Barnevern:** unge som har hatt omsorgstiltak, er 7,6 ganger så ofte på helserelaterte ytelser seks år etter grunnskolen (22,9 mot 3,0 prosent). Faktaboks, merket som annen populasjon | Faktaboksen under «Hvem er i størst fare?» | Tabell 13347 (kontakt: Rachel Ekren). Elever om lag 22 år, ikke 15–29-åringer; statusene er ikke NEET | Om sammenligningen er forsvarlig, om «helserelaterte ytelser» kan omtales som nærmest AAP/uføretrygd, og om faktaboksen hører hjemme i denne prototypen |
| 8 | **Påstandsprøven:** åtte påstander med dom. Særlig «Over 100 000 unge sitter fast utenfor» (ikke støttet), «Utenforskapet blant unge øker» (ikke støttet) og «Innvandrere er tre ganger så ofte utenfor» (med forbehold) | «Påstandsprøven» | Egne vurderinger, tallene generert fra tabellene | Om dommene og begrunnelsene er riktige, og om det mangler påstander dere ofte møter |

## B. Bør leses

| # | Påstand eller valg | Hvor | Grunnlag | Hva som må sjekkes |
|---|---|---|---|---|
| 9 | Navn: tittelen er «Unge utenfor arbeid, utdanning og tiltak», og siden bruker «utenfor», «NEET», «befolkningen utenom innvandrere» og «andre ordninger». Tabellene bruker «Utenfor arbeid, utdanning og arbeidsmarkedstiltak (NEET)», «Befolkningen eksklusive innvandrere» og «Andre ordninger, ikke på tiltak» | Hele siden | SSBs navn i 13556, 12424 og på faktasiden | Om forkortelsene er akseptable, eller om SSBs navn skal brukes fullt ut |
| 10 | Lesehjelpen: «Registrene gir høyere NEET-andel for Norge enn arbeidskraftundersøkelsen som brukes i EU-sammenligninger» | «Slik leser du tallene» | Faktasiden om NEET | Formuleringen |
| 11 | Eksempelet på prioritering: «Den som både studerer og har uføretrygd, telles som student» | Lesehjelpen, konseptgrafikken | Noten i 12424 og «Om statistikken» | Ingen, står i SSBs tekst |
| 12 | Avrunding i overskrifter: «Dobbelt så mange» (2,2), «1 av 10» (10,1 prosent). Eksakte tall står i figurene og tabellene | Toppgrafikken | Valg for å unngå at overskriften leses som fasit | Om «Dobbelt så mange» er for svakt når faktoren er 2,2 |
| 13 | Årsforklaringer i teksten: «Oljeprisfallet ga en topp i 2015, koronapandemien en topp i 2020». Koronaårene er markert i strømfiguren | «Hva betyr det å være utenfor?», «Hvor mange blir nye?» | Vår tolkning, står ikke i statistikken | Om forklaringene kan stå |
| 14 | Boblediagrammet: x er andel av gruppen som er utenfor, y er andel av de utenfor som er på AAP/uføretrygd. Viser 25–29 år når velgeren står på 15–29 eller 15–19 år. Noten sier at y-aksen viser hva slags utenforskap, ikke varighet | «Hvem er i størst fare?» | Egen konstruksjon. Utdanningsnivå gir lite mening for 15–19 år | Om figuren kan misleses som et mål på risiko |
| 15 | Små grupper i velgeren (under 1 000 bosatte eller 100 utenfor) får et varsel om at andelene kan svinge. 15 av 48 fineste grupper er under 1 000 bosatte | Kortet øverst | Avrunding av celler med 1 og 2 | Om grensene er rimelige |
| 16 | Forløpstallene følger bare innvandringskategorien i velgeren. Velges kjønn, alder eller utdanning, sier noten at figuren viser alle unge eller innvandringskategorien | «Hvor mange blir nye?», «Hvor lenge?» | 12427 er hentet uten kjønn og utdanning (valgt bort i steg 3 for å unngå avrundingsstøy) | Ingen, men si fra hvis forløp etter kjønn er viktig |
| 17 | Strøm inn regnes fra arbeid, utdanning og tiltak, ikke fra AFP/alderspensjon | «Hvor mange blir nye?» | Nesten ingen 15–29-åringer i AFP/alderspensjon | Ingen |
| 18 | 13347: fra 2023 er død/utvandret slått sammen med «annet». Kategorien vises som manglende fra 2023, og celler med «..» vises som «..» | Faktaboksen, tabellen | Noten i 13347 | Ingen |
| 19 | Farger følger kategorien: AAP/uføretrygd grønn, ledige blå, andre ordninger oker, ukjent grå, fortsatt utenfor marine, arbeid/utdanning/tiltak rosa, ute av befolkningen grå, innvandrere magenta. Avvik fra diagramstandarden: enkeltserier om NEET er marine, ikke SSB-grønn | Hele siden | Grønt brukes allerede for AAP/uføretrygd i toppgrafikken | Thomas |

## C. Spørsmål

| # | Spørsmål | Grunnlag |
|---|---|---|
| 20 | Stemmer hypotesene om misforståelser (H1–H10 i `01-innsikt.md`)? Hvilke møter dere oftest? Viktigst: at NEET leses som én langvarig gruppe (H2), og at høy andel blant innvandrere leses som tungt utenforskap (H4) | Innsiktsnotatet |
| 21 | Har dere publisert, eller planlagt, tall om varighet og strøm inn og ut etter artikkelen fra 2019 («Hvordan går det med unge som faller utenfor?»)? Er det tall dere heller ville at prototypen viste? | 12427 og 14158 gir dette nå, men vi har ikke funnet publiserte tall om det |
| 22 | Er det andre tabeller dere ville brukt, for eksempel 13349 (status 7–10 år etter grunnskolen etter barnevern) eller 13679 (fagfelt)? | Hele emnet arbstatus er gått gjennom; begrunnelse for hver tabell som er valgt bort, står i `03-kildekart.md` |
| 23 | Er Malin Pettersen og Pål Nordby riktige kontakter for 12424, 12427 og 14158, og Rachel Ekren for 13347? | Kontaktene i statistikkbanken. Pettersen er også medforfatter av artikkelen om ukjent status (desember 2025) |

## Avklart underveis

| # | Hva | Hvordan |
|---|---|---|
| 24 | Innsiktsnotatet sa at statistikkbanken ikke kan si noe om nye i NEET eller varighet | Feil. Gjaldt bare 12424. Tabell 12427 ble funnet i steg 3 og tatt inn. Rettet i `01-innsikt.md` versjon 0.2 |
| 25 | To påstander var skrevet fast i siden og holdt ikke for alle valg: «om lag halvparten er ute innen et år» og «studieforberedende blir lenger enn yrkesfag» | Rettet i steg 5: begge genereres nå fra tallene (42 prosent av 2024-kullet var ute et år senere). Påstanden om studieforberedende vises bare når forskjellen finnes |
| 26 | Varigheten etter utdanning regnet «fem år etter» fra 2019 i stedet for 2020, fordi kravet til antall oppfølgingsår var ett år for strengt | Rettet i steg 5. Tallene stemmer nå med kildekartet (42,1 mot 32,1 prosent) |
| 27 | Pseudokohort (aldersgrupper fulgt gjennom tverrsnittet) | Ikke brukt. Erstattet av ekte forløp fra 12427 og 14158 |
| 28 | 12438 (landbakgrunn) | Har ikke aldersgruppen 15–29 år. Ikke brukt |
| 29 | Rådata | Hentet uendret fra data.ssb.no 10.11.2026, ikke rekonstruert. 13347 har 120 celler med «..», andre tabeller ingen statussymboler |
| 30 | Teknisk, ikke fagets ansvar: grafikkhjelperne ligger i prototypens egen mappe, fordi repoet ikke har en felles grafikkmodul. `naturregnskap` stopper det felles bygget i GitHub Actions (ukjent plassholder `/*__IKONER__*/`). Skillen for steg 4 oppgir en utdatert sti til Chromium | Meldt til Thomas |

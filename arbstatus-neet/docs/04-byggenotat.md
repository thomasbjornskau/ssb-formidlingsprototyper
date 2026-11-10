Steg 4 i formidlingsprototype for arbstatus-neet · versjon 0.1 · 10.11.2026 · Status: utkast, til Thomas før publisering

# Byggenotat: unge utenfor

**Annerledes enn de andre prototypene.** Denne er bygd fra én tabell (12424) for et konkret artikkeløyemed: en artikkel om varigheten av utenforskapet blant unge. Den skal både få forfatteren til å se hva tallene bærer, og vise hvordan funnene kan formidles. Derfor har den en egen seksjon, «Påstandsprøven», og en avsluttende boks, «Dette kan tallene ikke si». I steg 3 ble tre tabeller lagt til: 12427 og 14158 (forløp) og 13347 (barnevern).

## Hva som er bygget

| Seksjon | Svarer på | Innhold |
|---|---|---|
| Hode med gruppevelger | Hvem gjelder det? | Kjønn, alder, innvandringskategori og høyeste utdanning (180 grupper). Kortet viser NEET-andel, antall, sammenligning med alle unge, andel AAP/uføre og ukjent, og en minilinje 2008–2025. Varsel ved små grupper (under 1 000 bosatte eller 100 utenfor). Valget ligger i adressen (`#kjonn=1&alder=20-24&innv=B&utd=1-2`) |
| Slik leser du tallene | H2, H1, H7, H6 | Fire punkter med tall fra dataene, og konseptgrafikken i `<details>` |
| Toppgrafikk B | Er utenforskapet tyngre enn før? | «Dobbelt så mange» (generert fra forholdstallet 2,2), stablede stolper 2008–2025, fire nøkkeltall: utenfor, andel, nye inn, fortsatt utenfor etter ett år |
| Hva betyr det å være utenfor? | P1 | Fordeling på fire statuser for valgt gruppe mot alle (fra grafikk A). Andel over tid for valgt gruppe mot alle |
| Hvor mange blir nye i gruppen? | Nye i NEET | Strøm inn og ut 2009–2025, koronaårene markert. Netto endring i teksten, med forklaring på hvorfor den ikke er inn minus ut |
| Hvor lenge er de utenfor? | Varighet, lenger enn før | Fortsatt utenfor ett år etter, per startår. Kullkurver 1–10 år etter for fem startår. Fem års varighet på AAP/uføretrygd, med strek ved AAP-innføringen 2010 |
| Innvandrere og befolkningen ellers | P3 (seksjon C) | Fordeling på statuser (grafikk C). Status fem år etter: fortsatt utenfor, i arbeid/utdanning/tiltak, ute av befolkningen. Andel over tid for begge grupper og alle |
| Hvem er i størst fare? | P5 (seksjon D) | Boblediagram for 25–29 år (eller 20–24 år ved valg), etter innvandringskategori og utdanning. Varighet etter todelt videregående (14158) med valg av aldersgruppe. Faktaboks om barnevern (13347), tydelig merket som annen populasjon |
| Påstandsprøven | Artikkelforfatteren | Åtte påstander med dom (støttet, med forbehold, ikke støttet) og tallene bak. All tekst generert fra dataene |
| Dette kan tallene ikke si | H1 | Sammenhengende varighet, nedre grense for tilgang, årsaker, forløp per gruppe, EU-sammenligning |

Forløpsseksjonene følger innvandringskategorien i velgeren. Velges kjønn, alder eller utdanning, sier noten at forløpstabellen ikke har den inndelingen, og hvilken gruppe figuren viser i stedet.

## Hvordan hull i data vises

- **Små grupper** i velgeren gir et stiplet varsel i kortet. Andelene vises likevel, fordi tallene er publisert.
- **«..» i 13347** vises som «..» i tabellen, aldri som 0. Figuren bruker bare helserelaterte ytelser, som ikke har «..».
- **Død/utvandret i 13347 fra 2023** er satt til manglende i datasteget, fordi tabellen har slått kategorien sammen med «annet». Datasteget stopper hvis tallet ikke lenger er 0 fra 2023.
- **År før startåret i 12427 og 14158** er strukturelt tomme og tegnes ikke.
- **Grupper uten nok forløp:** kullkurvene viser bare de årene kullet er fulgt (2024-kullet har ett punkt).

## Kontrollene i `scripts/lag_data.py`

19 kontroller over 217 441 celler. Bygget stopper hvis en grense brytes.

| Kontroll | Toleranse | Største faktiske avvik |
|---|---|---|
| K1 12424 TOT, U.04-U.05 og U.90B = sum av undernivåene | 0 | 0 |
| K2 12424 kjønn, alder, utdanning og innvandring summerer | 0 | 0 |
| K3 NEET-antall 12424 = NEET i 13556 | 10 | 6 |
| K4 NEET-andel regnet fra 12424 = publisert i 13556 (tideler) | 1 | 1 (kvinner 2023: 9,95 blir 9,9) |
| K5 12427 år før startåret er 0 | 0 | 0 |
| K6 12427 startåret = 12424 samme år | 30 | 14 |
| K7 12427 kullet er like stort hvert år | 50 | 47 (av 955 000) |
| K8 12427 status i tidsserien summerer til i alt | 30 | 0 |
| K9 12427 innvandring summerer | 30 | 0 |
| K10 NEET i startåret (12427) = NEET (12424) | 30 | under 30 |
| K11 14158 år før startåret er 0 | 0 | 0 |
| K12 14158 status i tidsserien summerer | 30 | 0 |
| K13 14158 utdanningshierarkiet summerer | 30 | 0 |
| K14 14158 tre aldersgrupper = 12427 15–29 år | 60 | 44 |
| K15 13347 statusene summerer til alle | 20 | 0 |
| K16 13347 barnevernsgruppene summerer | 20 | 0 |
| K17 13347 publisert prosent = antall / alle (tideler) | 1 | 1 |

Toleransene over 0 skyldes SSBs avrunding av celler med 1 og 2 i hver tabell for seg.

**Negativ test (10.11.2026):** +50 i én celle i 12424 stoppet bygget i K1. +200 i én celle i 12427 stoppet bygget i K8. Originalfilene er urørt.

**Bygget to ganger:** `index.html` er identisk (624 kB).

**Testet i Playwright, 1280 og 390 px:** ingen feil i konsollen, `scrollWidth` lik bredden for seks adresser (start, innvandrer-menn 20–24 med grunnskole, kvinner 25–29 utenom innvandrere med videregående, liten gruppe 15–19 innvandrere med uoppgitt utdanning, menn 25–29 med høyere utdanning, ugyldig adresse). Velgere, knapper og adressen er prøvd. Skjermbildene er sett på, og overlapp i boblediagram, kullkurver, tegnforklaringer og akseetiketter er rettet.

## Nye valg til kvalitetssikring (fortsetter fra 02)

16. **Farger følger kategorien, også for nye kategorier.** AAP/uføretrygd grønn, ledige blå, andre ordninger oker, ukjent grå (fra steg 2). Nye: fortsatt utenfor og strøm inn marine, arbeid/utdanning/tiltak rosa, ute av befolkningen grå, innvandrere magenta, befolkningen utenom innvandrere mørk skifer. Avvik fra diagramstandarden: enkeltserier som handler om NEET (andel, fortsatt utenfor), er marine, ikke `#00824d`, slik at «utenfor» har samme farge overalt. Grått brukes både for ukjent status og ute av befolkningen; de står aldri i samme figur.
17. **«Dobbelt så mange»** er generert fra forholdstallet 2,2 (12 462 → 27 621). Den nøyaktige verdien ligger i `title` og i tabellen.
18. **Strøm inn** er definert som i arbeid, utdanning eller tiltak ett år og utenfor året etter. Overgang fra AFP/alderspensjon er utelatt (nesten ingen i alderen).
19. **Påstandsprøven:** valget av de åtte påstandene og dommene er våre. Særlig «Over 100 000 unge sitter fast utenfor» (ikke støttet) og «Innvandrere er tre ganger så ofte utenfor» (med forbehold) bør vurderes av fag.
20. **Boblediagrammet bruker 25–29 år** når velgeren står på 15–29 eller 15–19, fordi utdanningsnivået er lite meningsfullt for 15–19-åringer.
21. **Varighetsfiguren etter utdanning** sammenligner 2016 og 2024 for ett år etter. Tittelen påstår bare at studieforberedende er oftere utenfor enn yrkesfag når forholdet er minst 1,3; ellers handler tittelen om grunnskole. For 20–24 år er de to like.
22. **Barnevern i samme prototype:** faktaboksen har egen farge (lilla aksentkant) og merkelapp. Fag bør vurdere om den hører hjemme her.
23. **Seksjonstekster med årsforklaringer** («Oljeprisfallet ga en topp i 2015, koronapandemien en topp i 2020») er vår tolkning og står ikke i statistikken.
24. **`felles/grafikk.py` fantes ikke i repoet.** Hjelpefunksjonene ligger i `arbstatus-neet/scripts/grafikk.py`. Ingen felles filer er endret, utenom rad i `README.md` og kort i `index.html`.
25. **Skillen for steg 4 oppgir feil sti til Chromium** (`chromium-1194`). I denne økten lå den under `chromium-1243`, og Playwright fant den uten eksplisitt sti.

## Kjente svakheter

- Kullkurvene ligger tett; forskjellen mellom kullene er reell, men liten i figuren. Søylene for «fortsatt utenfor ett år etter» viser trenden tydeligere.
- På mobil får boblediagrammet korte etiketter, og en etikett kan utelates når det ikke er plass. Tallene står i hoverteksten og i tabellen.
- Forløp følger bare innvandringskategorien i velgeren, ikke kjønn og utdanning (alternativ 3 i steg 3 ble valgt bort).
- Tallene for 2025 er foreløpige. Endelige tall kommer 19.01.2027.

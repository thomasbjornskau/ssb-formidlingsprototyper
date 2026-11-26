Steg 4 i formidlingsprototype for sykefratot · versjon 0.1 · 26.11.2026 · Status: utkast

# Byggenotat: Sykefravær (sykefratot)

**Merking.** `[K1]`–`[K15]` som i `01-innsikt.md`. `[T]`: vårt valg eller vår tolkning.

Prototypen er bygget med `python felles/bygg.py sykefratot` fra `src/index.template.html`, `build/sykefratot.json` (fra `scripts/lag_data.py`) og konseptgrafikken i `src/`. Malen bygger på `ufore` (kjønnsknapper, lesehjelp, toppgrafikk, kort med «Vis tallene», kommunesøk), med synonymformat fra `kpi`. Ferdig fil: 959 kB.

## 1. Hva som er bygget

| Seksjon | Svarer på | Innhold |
|---|---|---|
| Hode | – | Ingress generert fra tallene, kjønnsvelger (begge, kvinner, menn) |
| Slik leser du tallene | H1, H2, H4, H7 | Fire punkter med tall. Konseptgrafikken bred og smal i `<details>` |
| Toppgrafikk A | Spørsmål 1, H5 | Stort tall (avrundet), setning, linje fra 2000 med sesongjustert og ujustert, brudd 2015, toppen i 2003, fire nøkkeltall |
| Samme kvartal, to tall: SSB og Nav | H1 | Bryter mellom SSBs og Navs måte å melde. SSB: sesongjustert, siste 12 kvartaler. Nav: legemeldt ujustert, samme kvartal hvert år fra 2015 |
| Korte egenmeldinger eller lange sykmeldinger? | Spørsmål 3, H3 | Variant C fra steg 2 med kvartalsvelger, og egenmeldingenes andel av tilfeller og dagsverk over tid (klikkbar) |
| Hvem har høyest sykefravær? | Spørsmål 4 | Kvinner og menn fra 2000. Ni yrkesgrupper, klikkbare |
| Finn yrket ditt | Spørsmål 4 | Søk med synonymer, sti i hierarkiet, tallkort, serie fra 2015 mot alle yrker, undergrupper, «Se alle yrker» |
| Min kommune | Spørsmål 4 | Søk, tallkort, serie fra 2024K1 mot hele landet, «Se alle kommuner» |
| Om tallene | – | Definisjon, egne beregninger, hvorfor næring mangler, tabeller og datoer |

Valgene ligger i adressen: `#kjonn=menn&visning=nav&kvartal=2022K1&yrke=5321&kommune=0301`.

## 2. Hvordan hull i data vises

- **«:» (undertrykt)** i yrke: tekst om at tallet ikke er publisert av hensyn til enkeltpersoner, med forslag om «Begge» eller en overordnet gruppe. I tabellen står «:». Undergruppelisten viser «undertrykt».
- **«..» og manglende kvartaler** i yrke: brudd i linjen, «..» i tabellen, og en linje som sier hvor mange kvartaler yrket har tall for. Yrker uten tall i det hele tatt får ingen figur, bare forklaring.
- **Publisert endring mangler** for 115 kommuner i 2024: «..» i tabellen. Tallkortet bruker siste kvartal, der endringen finnes for alle.
- **9999 Uoppgitt kommune** er filtrert bort i `lag_data.py`.
- **Endringsrater med «.»** (2015, start av serien) vises som «.» i tabellen under toppgrafikken.
- Sykefraværsdagsverk før 2015 («..») brukes ikke.

## 3. Kontroller i `lag_data.py`

Alle stopper bygget med «Kontroll feilet: …». Største faktiske avvik 26.11.2026:

| | Kontroll | Toleranse | Største avvik |
|---|---|---|---|
| B1 | Egenmeldt + legemeldt = i alt, sesongjustert | 0,015 | 0,01 |
| B1 | Samme, ujustert | 0,1 | 0,1 |
| B2 | Menn + kvinner = begge, dagsverk | 100 | 100 |
| B3 | Navs tall for 2025K3 (4,8 og −6,3) gjenskapes | eksakt | 0 |
| B4 | Dagsverk i 12946 = 12439 | 100 | 0 (2024K2 med 6 400 holdt utenfor som kjent avvik) |
| B5 | Varighet summerer, tilfeller | 0 (kjønn 1) | 0 (kjønn 1) |
| B5 | Varighet summerer, dagsverk | 200 | 200 |
| B6 | Andeler fra antall = publiserte andeler | 0,1 | 0,1 |
| B7 | Synonymkodene finnes i 12452 | – | OK, 100 ord |
| B8 | 407 yrkeskoder på 4-siffernivå, 357 kommuner med hel serie | eksakt | OK |
| B9 | Tallene i toppgrafikken = steg 2, når siste kvartal er det samme | eksakt | OK |

**Negativ test:** +500 tilfeller i én celle i `varighet.json` stoppet bygget på B4. 5,65 endret til 5,75 i `hoved.json` stoppet bygget på B1. Filene ble satt tilbake og kontrollert med `cmp`.

## 4. Test

Playwright i 1280 og 390 px bredde:
- Ingen feil eller advarsler i konsollen. `scrollWidth` lik bredden i begge.
- **Yrkessøk:** «sykepleier» gir Sykepleiere og Spesialsykepleiere først. «lærer» gir Grunnskolelærere først. «lege» gir legene før Tannleger. «politi» gir Politibetjenter før Politikere. «programmerer» treffer via synonym. «xyzq» gir ingen treff og lenke til hele treet.
- **Kommunesøk:** «Tromsø», «oslove», «Porsáŋgu» (statistikkbanken skriver Porsángu, normaliseringen gjør ŋ til n), «tråante», «kar» (tre treff). «Gotham» gir ingen treff og lenke til alle kommuner.
- **Tastatur:** pil ned og Enter i forslagslisten. Hovedgruppene i yrkesfiguren kan velges med Enter og mellomrom. Kvartal kan velges med piltaster i tidsfiguren.
- **Tilstander:** adressen med `kjonn=menn&visning=nav&kvartal=2022K1` gjenopprettes. Yrke 2111 for menn (undertrykt), 0110 (ingen tall) og 2521 for kvinner (38 av 47 kvartaler) gir riktig tekst.
- **Deterministisk bygg:** `build/` slettet, bygget på nytt, samme sha1.

Rettet etter skjermbildene:
- Årstall som overlappet i SSB-figuren.
- Etiketter som summerte til 101 (nå største rest).
- Et for langt gruppenavn.
- «Oslo (Oslo)» i overskriften.
- Tallkort som brakk på smal skjerm.
- Bruddtekst som kolliderte med toppannoteringen.
- Aksetittel oppå endringsteksten.
- «fra 3,7 til 3,7» når de avrundede nivåene er like.

## 5. Nye valg til kvalitetssikring

Nummerert videre fra `02-kvalitetssikring.md` (1–27).

| # | Valg | Grunnlag | Må sjekkes |
|---|---|---|---|
| 28 | Ingressen sier «i underkant av 7 av 100» for 6,65 | Omregning `[T]` | Formuleringen |
| 29 | «Nesten flatt» brukes når spennet siden starten av året før er under 0,25 prosentpoeng | Regel `[T]` | Terskelen |
| 30 | Toppgrafikken følger kjønnsvelgeren | Valg `[T]` | – |
| 31 | «Slik melder Nav» bruker SSBs tabell 12439 med Navs metode | Kontrollert mot Navs melding for 2025K3 (B3) `[K6]` | Navs melding for 2026K3 er ikke lest (kildekart, hull 10) |
| 32 | Nav-visningen viser samme kvartal fra 2015, ikke tidligere | Ujusterte tall er brutt i 2015 `[K1]` | – |
| 33 | SSB-visningen har avkortet y-akse | Linjediagram der endringen er poenget (ssb-diagramstandard) | – |
| 34 | Etikettene i stolpene for varighet rundes med største rest | Så de summerer til 100 `[T]` | – |
| 35 | Overskriften «Gapet mellom tilfeller og dagsverk har holdt seg siden 2015» | 12946, alle kvartaler `[T]` | – |
| 36 | Ni yrkesgrupper. Uoppgitt (0b) er utelatt i figuren | `[T]` | – |
| 37 | Yrket som er valgt fra start, er Helsefagarbeidere | Høyest blant store yrker i artikkelen `[K2]` | – |
| 38 | Synonymlisten: 100 ord, 21 merket usikre | Vårt valg `[T]` | Fag bør lese listen |
| 39 | Søkerangering: synonym, eksakt navn, starten av navnet, starten av et ord, inneholder (fra 3 tegn). Lavere nivå først ved likt | Som i kpi `[T]` | – |
| 40 | Hele landet i kommunefiguren er 12439, legemeldt og ujustert | Tabell 12451 har ikke landstall `[T]` | Om 12439 og summen av 12451 er sammenlignbare (bosatte lønnstakere i begge) |
| 41 | Teksten om at små kommuner svinger, vises når spennet i serien er minst 2 prosentpoeng | `[T]` | Terskelen |
| 42 | «Omtrent som for alle yrker eller hele landet» brukes ved under 0,25 prosentpoeng forskjell | `[T]` | – |
| 43 | Prosentpoeng i lesehjelpen er regnet fra publiserte nivåer | `[T]` | – |
| 44 | Fylkesnavn til søket er satt fra kommunenummeret (Klass 104, 2024) | Statistikkbanken har ikke fylke i 12451 | – |
| 45 | Kildelinjen i toppgrafikken sier at tall før og etter 2015 bare er sammenlignbare med forbehold | Venter på fagspørsmål 4 i 01-innsikt | Formuleringen når fag har svart |

## 6. Kjente svakheter

- **Tallene for Nav i 2026K3 er ikke sjekket** mot Navs egen melding.
- **Næring mangler** til SN2025-tabellene kommer.
- **Yrker kan ikke vektes eller filtreres på størrelse.**
- **Tipsboksene vises bare med mus.** Tastatur og skjermleser får tallene i «Vis tallene».
- **Toppannoteringen krysser bruddlinjen** på smal skjerm. Den er lesbar, men ikke pen.
- **Konseptgrafikken bruker Roboto Condensed.** Fonten er ikke bakt inn, så nettleseren faller tilbake til Arial Narrow eller Arial.
- **Siden er 959 kB**, mest yrkesserien (se kildekart, avsnitt 4). Den er bakt inn som i de andre prototypene, ikke lastet separat.

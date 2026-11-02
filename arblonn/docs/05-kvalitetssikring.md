`Steg 5 i formidlingsprototype for arblonn · versjon 0.1 · 02.11.2026 · Status: til faglig kontroll`

# Kvalitetssikring: Antall arbeidsforhold og lønn

Prototype: https://thomasbjornskau.github.io/ssb-formidlingsprototyper/arblonn/index.html

Listen samler det som er tolkning, eget valg eller ikke bekreftet i prototypen. Den **erstatter** listene i `01-innsikt.md` (spørsmål og hull), `02-kvalitetssikring.md` (G1–G15), `03-kildekart.md` (hull og hindre) og `04-byggenotat.md` (G16–G26). Opprinnelig nummer står i parentes.

Tallene er hentet fra statistikkbanken 30.10.2026 og kontrollert ved hvert bygg (26 kontroller, se `03-kildekart.md`). Det er tolkningene og forklaringene som trenger faglig blikk.

**Merking:** `[K]` = SSB-kilde, se kildelisten nederst · `[T]` = vår tolkning.

## A. Må avklares

Dette kan være feil, eller gi et misvisende inntrykk hvis det er feil.

| # | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 1 | Toppgrafikken viser endelig sesongjustert linje og bare de **to siste foreløpige** punktene, ikke en foreløpig historikk. Grunnen er at den foreløpige serien i 13126 endres bakover: juli–august 2023 ble publisert som om lag −16 850 jobber, mens serien viser −2 276 i dag. (G13, G16) | Toppen | Statistikkbanken; [K3]; «sesongjusterte tall kan revideres» [K1] | Er det riktig forstått at også de foreløpige sesongjusterte tallene beregnes på nytt? Bør en foreløpig historikk vises, og i så fall hvordan? |
| 2 | «Det endelige tallet for august ble 67 276 jobber høyere enn det foreløpige. Det endelige tallet tar med forsinkede meldinger og rettinger, og jobber som fikk lønn først måneden etter.» Tallet er sesongjustert. Ujustert er forskjellen 94 755. (G7, G17) | Toppen, lesehjelpen, konseptgrafikken trinn 5 | [K4]: 25 000–100 000 arbeidsforhold mangler i første versjon | Skyldes noe av forskjellen at foreløpige og endelige tall sesongjusteres hver for seg? Er 67 276 i august uvanlig høyt? Siden 2023M09 har forskjellen ligget på 45 000–67 000. |
| 3 | «Lønnsveksten … er ikke det den enkelte fikk i tillegg: når det blir flere jobber i høyt- eller lavtlønnede grupper, endres snittet selv om ingen fikk ny lønn.» I tillegg: «Når snitt og median vokser ulikt, endrer fordelingen seg.» (H8, G25) | «Hva betyr lønnsveksten?» | Indeksen er snittet delt på snittet i 1. kvartal 2024 (kontroll K7) [T] | Stemmer forklaringen? Har SSB et mål for lønnsvekst justert for sammensetning som prototypen bør vise til? |
| 4 | «Forskjellen, 327 724, er bijobber.» Antall jobber minus antall lønnstakere. Hver lønnstaker telles i næringen til hovedjobben. (G4, G19, G21) | Lesehjelpen, «Hvor mange jobber …» | Jobber omfatter hoved- og bijobber [K5]; næringene summerer eksakt til totalen for lønnstakere (K2) [T] | Er differansen lik antall bijobber? Hvordan velges hovedjobben: største stilling, høyest lønn eller noe annet? |
| 5 | «Medianen er lønna i midten når alle lønningene er regnet om til heltid og sortert.» Medianen 53 650 kr er tolket som median over heltidsekvivalenter. (G11) | «Hvilken lønn …» | Gjelder den årlige lønnsstatistikken [K6] | Beregnes median avtalt månedslønn i arblonn på samme måte, vektet etter heltidsekvivalenter? |
| 6 | «45 prosent av kvinnenes jobber er deltid, 26 prosent av mennenes.» Deltid er kategorien «Deltid» i 13871. (G20) | «Hvor mange jobber …» | 13871, kodelisten «Avtalt heltid/deltid» | Hva er grensen for deltid i tabellen? Er andelen av jobber riktig mål, eller bør den være av lønnstakere? |

## B. Bør leses

| # | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 7 | «Hver måned sender alle arbeidsgivere a-melding med arbeidsforhold, lønn og stillingsprosent.» (G1) | Konseptgrafikken trinn 1 | [K1] | Om stillingsprosent er med for alle arbeidsforhold |
| 8 | «En jobb telles når det er lønn eller ytelse i uka med den 16.» Jobber med sykepenger, foreldrepenger og korte permitteringer er med. (G2) | Konseptgrafikken trinn 2 | [K1] | Om «lønn eller ytelse» er en riktig forenkling |
| 9 | «Ikke med: … småbeløp under fritaksgrensene i a-ordningen.» (G8) | Konseptgrafikken, grå boks | [K2], fra 2018 | Om fritaksgrensene fortsatt gjelder |
| 10 | Heltidsekvivalenter er vist som stolpe ved siden av jobber og lønnstakere, selv om enheten er en annen. (G10) | «Hvor mange jobber …» | Eget valg [T] | Om det blander enheter på en villedende måte |
| 11 | Overskriften i sesongkortet: «Ujusterte tall svinger med årstiden: … jobber mellom [måned] og [måned]». Målet er høyeste minus laveste måned siste tolv måneder, og inneholder også trend. (G23) | «Blir det flere …», sesongkortet | Eget valg [T] | Om et annet mål er bedre |
| 12 | Brudd i 1. kvartal 2020 er markert i lønnsvekstfiguren: «bedre lønnsrapportering og ny metode for arbeidstid påvirker veksten gjennom 2020, mest i bergverk og utvinning». (ny) | «Hva betyr lønnsveksten?» | Fotnote i 11654; [K1] om ny arbeidstidsmetode | Om den nye arbeidstidsmetoden påvirker lønn per heltidsekvivalent, eller bare fordelingen av lønnstakere |
| 13 | «Lønnstakere som ikke er bosatt i Norge, er med. Derfor viser AKU andre tall.» (ny) | Lesehjelpen | [K2], [K3] | Om «derfor» er for snevert, siden AKU også skiller seg ut med selvstendige, alder og utvalg |
| 14 | Egne kortnavn på næringer, for eksempel «Teknisk tjenesteyting og eiendom», «Offentlig administrasjon og forsvar», «Helse og sosial». (ny) | Velgeren og alle figurer | Eget valg | Om kortnavnene er akseptable |
| 15 | «Jobbene øker mest for 67 år eller eldre» vises for alle næringer, men gjelder hele landet. Notatet sier at tallene ikke finnes per næring. (ny) | «Hvor mange jobber …», alderskortet | 11652 har ikke næring | Om kortet bør skjules når en næring er valgt |

## C. Spørsmål

| # | Spørsmål | Grunnlag |
|---|---|---|
| 16 | Stemmer hypotesene H1–H10 om misforståelser, og mangler det en dere ofte møter? | `01-innsikt.md`, avsnitt 4 |
| 17 | Hvilke spørsmål får dere oftest etter publisering? | – |
| 18 | Er næring det riktige gjennomgående valget, eller er fylke viktigere for brukerne deres? | `01-innsikt.md`, avsnitt 6 |
| 19 | Hva bør brukerne velge når de vil ha den ferskeste lønna: kontantlønn per måned eller avtalt månedslønn per kvartal? | `01-innsikt.md`, avsnitt 7 |
| 20 | Endelig ujustert jobbtall for november 2024 (13126) er 305 lavere enn tallet for 4. kvartal 2024 (11654). Andre kvartaler avviker med høyst 12. Hva er forklaringen? | Kontroll K10 |
| 21 | Er gjennomsnittlig avtalt arbeidstid (29,0 timer) per jobb eller per lønnstaker? | Tabellen i alderskortet |
| 22 | Er du riktig person å se på dette, eller bør andre i seksjonen se på deler av det, for eksempel sesongjusteringen? | – |

## Avklart underveis

| # | Hva | Hvordan |
|---|---|---|
| 23 | Om den foreløpige serien ligger fast (G13) | Testet mot publisert tall fra 2023. Den gjør ikke det. Toppgrafikken ble endret, se punkt 1 |
| 24 | «Summen av næringene avviker … fordi næringene sesongjusteres hver for seg» | Feil. Totalen for jobber og lønnstakere er summen av de sesongjusterte næringene [K4]. Rettet til at avviket skyldes avrunding |
| 25 | Om bergverk og utvinning sesongjusteres | [K4] (2021) sier nei. Dataene og fotnoten i 13126 viser at bare uoppgitt næring står uten sesongjustering i dag. Ingen endring |
| 26 | Små avvik mellom tabellene (K5b, K6, K10, G22) | Forklart av fotnoten om at ett- og totall er endret til 0 eller 3 for personvern. Toleransene er satt etter det |
| 27 | Forklaringen på forskjellen mellom foreløpig og endelig («sene meldinger») | Gjort mer presis med [K4]. Konseptgrafikken sier nå at tallet er sesongjustert |
| 28 | «Halvparten av heltidsekvivalentene har avtalt lønn under medianen» | Omformulert, se punkt 5 |
| 29 | Brudd i 2. kvartal 2018 og 3. kvartal 2019 (sokkeljobber flyttet til Rogaland og Hordaland) | Ligger utenfor fylkesvisningen, som starter i 2024 |
| 30 | G3, G5, G6, G9, G12, G14, G15, G18, G24, G26 | Bekreftet mot [K1] eller egne valg uten faglig risiko: avrunding i overskrifter, avkortet y-akse, lønnsvekst regnet fra kroner (treffer 18 av 18 publiserte tall) |
| 31 | Hull i fylkestall før 2024, skjult lønn (finans i Finnmark 2025K1), næringer uten undernæringer (84, 85) | Vises med egen tekst, aldri som null |
| 32 | Teknisk: konseptgrafikken har faste tall fra august 2026 og må lages på nytt med `scripts/lag_grafikk.py` når tallene oppdateres. `docs/grafikk/02-topp-c.svg` viser utkastet fra steg 2 med foreløpig historikk, ikke den publiserte versjonen | Ikke fagets ansvar |

## Kilder

- **[K1]** SSB: «Om statistikken» – Antall arbeidsforhold og lønn. Sist oppdatert 11.09.2025. https://www.ssb.no/arbeid-og-lonn/statistikker/arblonn
- **[K2]** Christoffer Berge: «Ulike tall om lønnstakere». SSB, 04.01.2018. https://www.ssb.no/arbeid-og-lonn/artikler-og-publikasjoner/ulike-tall-om-lonnstakere
- **[K3]** Magnus Berglund Johnsen og Sofie Hillestad Baumann: «Nedgang i antall jobber i august». SSB, 27.09.2023. https://www.ssb.no/arbeid-og-lonn/sysselsetting/statistikk/arbeidskraftundersokelsen/artikler/nedgang-i-antall-jobber-i-august
- **[K4]** Øyvind Bruer-Skarsbø, Rakel Gading og Stine Bakke: «Nye sesongjusterte jobbtall». SSB, 05.07.2021. https://www.ssb.no/arbeid-og-lonn/sysselsetting/statistikk/antall-arbeidsforhold-og-lonn/artikler/nye-sesongjusterte-jobbtall
- **[K5]** Ole Villund: «Nye månedlige jobbtall tilbake til 2003». SSB, 02.07.2024. https://www.ssb.no/arbeid-og-lonn/sysselsetting/statistikk/antall-arbeidsforhold-og-lonn/artikler/nye-manedlige-jobbtall-tilbake-til-2003
- **[K6]** Hanna Haugen Strand: «Hva er vanlig lønn i Norge?» SSB, 29.03.2022, sist endret 27.05.2026. https://www.ssb.no/arbeid-og-lonn/lonn-og-arbeidskraftkostnader/artikler/hva-er-vanlig-lonn-i-norge
- Statistikkbanken, tabell 13126, 11654, 13871, 11652 og 12314, med fotnoter. Hentet 30.10.2026, fotnoter lest 02.11.2026.

`Steg 4 i formidlingsprototype for arblonn · versjon 1.0 · 30.10.2026 · Status: godkjent av Thomas (02.11.2026)`

> Punktene i avsnitt 4 er flyttet til `05-kvalitetssikring.md`, som erstatter listen her. Rettinger gjort i steg 5 står under «Avklart underveis» der.

# Byggenotat

**Merking:** `[T]` = vår tolkning.

## 1. Hva er bygget

Én frittstående side, `index.html` (1 077 kB), bygget med `python felles/bygg.py arblonn`. Næringsvalget (16 næringer og «Alle næringer») ligger i adressen, for eksempel `#naering=86-88`, og styrer alle seksjonene. Fylke er et filter i seksjon 4: `#naering=05-09&fylke=56`.

| Seksjon | Svarer på | Innhold | Tabell |
|---|---|---|---|
| Hode | – | Prototypemerking, ingress generert fra tallene, næringsvalg og fire eksempler | 11654, 13126 |
| Slik leser du tallene | H1, H2, H4, H7 | Fire punkter med tall, konseptgrafikken bak «Slik lages tallene» | 11654, 13126 |
| Toppgrafikk C | Spørsmål 3, H7 | Månedsendring, sesongjustert og foreløpig. Endelig linje (siste tre år eller fra 2003), de to siste foreløpige punktene og avstanden mellom versjonene for nest siste måned. Fire nøkkeltall | 13126 |
| Hvor mange jobber, og hvor mange mennesker har dem? | Spørsmål 1, H1, H6 | Jobber, lønnstakere og heltidsekvivalenter; deltid etter kjønn; jobbvekst etter alder (hele landet) | 11654, 13871, 11652 |
| Hvilken lønn er det SSB oppgir? | Spørsmål 2, H4, H5, H6 | Median, snitt avtalt månedslønn og snitt månedslønn, med kontantlønn i teksten; kvinner og menn med snitt og median | 11654, 13126, 13871 |
| Blir det flere eller færre jobber nå? | Spørsmål 3, H3, H7 | Næringenes bidrag til siste månedsendring (klikkbare); ujustert mot sesongjustert for valgt næring, fire år | 13126 |
| Hvor vokser jobbene, og hvor er lønna høyest? | Spørsmål 4, H10 | Næringer rangert etter jobbvekst eller avtalt månedslønn, for landet eller et fylke; fylkene for valgt næring; tosifrede undernæringer | 11654, 12314 |
| Hva betyr lønnsveksten? | Spørsmål 5, H8 | Lønnsvekst per næring med totalen som referanse; vekst i snitt og median over tid for valgt næring | 11654 |
| Bunntekst | – | Om tallene, egne beregninger, kilder og hentedato | alle |

Alle figurer har overskrift som sier poenget, generert fra tallene, kildelinje og «Vis tallene». Klikkbare stolper kan brukes med tastatur (`role="button"`, Enter og mellomrom).

## 2. Hull og tilstander uten data

| Tilstand | Hvordan den vises |
|---|---|
| Næringene 84 og 85 har ingen undernæringer | «… har ingen undernæringer» med forklaring. «Vis tallene» skjules |
| Skjult lønn (`:`) i undernæringer og fylker | Teksten «tallet er skjult» ved stolpen, «skjult» i tabellen. Aldri null |
| Undernæring uten tall for jobbvekst | «ingen tall» |
| Fylkestall før 2024 | Ikke hentet. Notatet under kortet sier at fylkestallene finnes fra 2024 |
| Alder per næring | Finnes ikke. Kortet viser hele landet og sier det |
| Siste måned har bare foreløpig tall | Vises som punkt, ikke som del av linja |

## 3. Kontroller

`lag_data.py` kjører alle kontrollene i `kontroll_kilder.py` og deretter B1–B4. Bygget stopper ved feil.

| Kontroll | Største avvik 30.10.2026 | Toleranse |
|---|---|---|
| K1–K13 (se `03-kildekart.md`) | som i kildekartet | som i kildekartet |
| K2b Heltidsekvivalenter, næringer = alle (ny i steg 4) | 4 | 10 |
| B1 Næringenes bidrag = totalendring siste måned | 2 | 5 |
| B2 Jobb- og lønnsvekst i byggfilen = publisert, 18 næringskoder | 0 | eksakt på én desimal |
| B3 Siste måned bare foreløpig, nest siste begge | – | eksakt |
| B4 Alle tosifrede næringer har gruppe, alle grupper har minst én | – | eksakt |

**Negativ test.** Én jobbcelle i `kvartal_naering.json` endret med +50: K2 og K6 feilet, og bygget stoppet. Én celle for heltidsekvivalenter endret med +50: første forsøk gikk gjennom, fordi ingen kontroll summerte heltidsekvivalenter. K2b ble lagt til, og samme endring stopper nå bygget. Filen ble satt tilbake, og bygget gir identisk `index.html`.

**Determinisme.** To bygg etter hverandre gir byte-identisk `index.html`.

**Nettleser.** Playwright i 1280 og 390 px, med sju tilstander (standard, helse og sosial, offentlig administrasjon, bergverk + Finnmark, overnatting + Oslo, finans + Finnmark, industri): ingen konsollfeil, `scrollWidth` lik bredden, ingen tomme figurer.

## 4. Nye valg til kvalitetssikring

Nummerert videre fra `02-kvalitetssikring.md` (G1–G15).

| # | Påstand eller valg | Hvor | Grunnlag | Må sjekkes |
|---|---|---|---|---|
| G16 | Toppgrafikk C viser bare de to siste foreløpige punktene, ikke en foreløpig historikk | Toppen | Kildekartet: den foreløpige serien sesongjusteres på nytt (G13 holdt ikke) | Om fag er enig i at historikken ikke bør vises |
| G17 | «Det endelige tallet for august ble 67 276 jobber høyere … fordi sene meldinger kom med» | Toppen | K1, K8 [T] | Forskjellen gjelder sesongjusterte tall. Om noe av den skyldes ny sesongjustering, ikke bare sene meldinger |
| G18 | Store tall i overskriften avrundes: til hundre fra 1 000, ellers til ti | Toppen | Eget valg | Ingen |
| G19 | «Forskjellen, 327 724, er bijobber.» Jobber minus lønnstakere | Lesehjelpen | Definisjonen i K1 [T] | At alle jobber utover hovedjobben kan kalles bijobber |
| G20 | Deltid er kategorien «Deltid» i 13871 | Seksjon 1 | 13871 | SSBs grense for deltid i denne tabellen |
| G21 | Jobber per lønnstaker i en næring blander egne og andres hovedjobber | Seksjon 1, note | Kildekartet [T] | Om forklaringen er riktig |
| G22 | Kvinner og menn hentes fra 13871 (i alt for heltid og deltid), ikke 11652, fordi 11652 ikke har næring | Seksjon 2 | 13871 | Avvik på noen få jobber mellom tabellene (K5b) |
| G23 | Svingningen i ujusterte tall er høyeste minus laveste måned siste tolv måneder, og inneholder også trend | Seksjon 3 | Eget valg [T] | Om et annet mål er bedre |
| G24 | Fylkesfilteret gjelder bare næringskortet. Fylkeskortet viser alle fylker for valgt næring, og klikk velger fylke | Seksjon 4 | Eget valg | Ingen |
| G25 | «Når snitt og median vokser ulikt, endrer fordelingen seg» | Seksjon 5 | [T] | Om forklaringen holder, og om SSB har et mål justert for sammensetning (spørsmål 2 i innsiktsnotatet) |
| G26 | Lønnsveksten er regnet fra kronebeløpene, ikke fra indeksen | Seksjon 5 | K11, fallgruve i kilder.json | Ingen |

## 5. Kjente svakheter

- Liggende stolper har ikke verktøytips, bare verdien ved stolpen og tabellen.
- Undernæringskortet viser de 15 største. Industri har 24, og resten ligger bare i tabellen.
- Toppgrafikkutkastet `docs/grafikk/02-topp-c.svg` viser fortsatt den foreløpige historikken fra steg 2. Det er beholdt som dokumentasjon av hva som ble vurdert, men prototypen bruker den rettede versjonen.
- Fylke og undernæring kan ikke kombineres: 12314 har ikke fylke.
- Kortene i samme rad får lik høyde, så noen kort har luft nederst.

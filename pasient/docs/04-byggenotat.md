`Steg 4 i formidlingsprototype for pasient · versjon 0.1 · 02.11.2026 · Status: utkast, til Thomas`

# Byggenotat

**Merking:** `[T]` = vår tolkning.

## 1. Hva er bygget

Én frittstående side, `index.html` (787 kB), bygget med `python felles/bygg.py pasient`. Diagnosevalget (20 kapitler, «Annen» og «Alle diagnoser») ligger i adressen, for eksempel `#kapittel=II`, og styrer alle seksjonene unntatt psykisk helsevern, som ikke har diagnoser.

| Seksjon | Svarer på | Innhold | Tabell |
|---|---|---|---|
| Hode | – | Prototypemerking, ingress generert fra tallene, kapittelvalg og fire eksempler | 14824, 14827, 14820 |
| Slik leser du tallene | H1, H2, H5, H6 | Fire punkter med tall: pasient er person, én gang per gruppe, bruk og ikke sykdom, hva som ikke er med. Konseptgrafikken bak «Slik lages tallene» | 14824 |
| Toppgrafikk A | Spørsmål 1, H3 | Stort tall og setning for valgt kapittel. Pasienter, polikliniske kontakter, døgnopphold og oppholdsdøgn som indeks 2015 = 100, med korona markert. Fire nøkkeltall | 14824 |
| Hva får pasientene? | Spørsmål 1, H3 | Endring 2015–2025 for alle sju mål; oppholdsdøgn per døgnopphold og kontakter per pasient over tid | 14824 |
| Hvem er pasientene? | Spørsmål 2, H3, H4 | Pasienter per 1 000 per aldersgruppe 2015 og 2025 (egen beregning); veksten fordelt på folketall, aldring og bruk (variant C fra steg 2, egen beregning); kvinner og menn over tid (publisert rate) | 14824, 07459, 14827 |
| Hva behandles de for? | Spørsmål 3, H1, H2 | Alle 20 kapitler og «Annen», klikkbare og tastaturbrukbare; kategoriblokkene i valgt kapittel, eller de 15 største blokkene når ingen er valgt; merknad om brudd i O60–O75, P00–P04 og R95–R99 | 14824 |
| Bruker innvandrere og barna deres spesialisthelsetjenesten annerledes? | Spørsmål 4, H4, H5 | Bryter mellom aldersjustert og ujustert. Somatikk for valgt kapittel og psykisk helsevern, 2025 | 14827, 14823 |
| Psykisk helsevern for voksne | Spørsmål 5, H6, H7 | Pasienter etter alder over tid; kvinner og menn 18–29 år, med merknad om fallende rate og økende antall | 14820, 14823 |
| Bunntekst | H8 | Om tallene, egne beregninger, kilder og hentedato | – |

Hver figur har «Vis tallene» med tabell og kildelinje. Overskriftene er generert fra tallene for valgt kapittel.

## 2. Hull og tilstander uten data

- Det finnes ingen manglende verdier i rådataene. `lag_data.py` stopper hvis det dukker opp `..`, `.` eller statusflagg.
- «Annen» har ingen kategoriblokker. Kortet sier hva gruppen inneholder i stedet for å vise en tom figur.
- «Alle diagnoser» viser de 15 største blokkene på tvers av kapitlene i stedet for en tom figur.
- Kapitler uten døgnopphold får tekst i stedet for figur i liggetidskortet. Ingen kapitler treffer dette i dag, men tilstanden er bygget.
- Ugyldig kapittel i adressen gir «Alle diagnoser».

## 3. Kontroller

Kjøres i `lag_data.py` og stopper bygget. Negativ test: én verdi i `somatikk_kapittel.json` økt med 60 stoppet bygget med D3. Filen ble satt tilbake og bygget gikk igjennom.

| # | Kontroll | Toleranse | Største faktiske avvik |
|---|---|---|---|
| D1 | Kontakter, døgnopphold og oppholdsdøgn summerer over kapitlene | 36 | 18 |
| D2 | Dagbehandlinger summerer over kapitlene | 36 | 6 |
| D3 | Kvinner + menn = begge kjønn | Pasienter 9, mengdetall 18 | 12 |
| D4 | Aldersgrupper = alle aldre | Pasienter 18, mengdetall 36 | 18 |
| D5 | Hver blokk hører til nøyaktig ett kapittel, og kapitlet er minst like stort som største blokk. Kapitlene er like i begge utsnittene av 14824 | Eksakt | 0 |
| D6 | Egen rate per kapittel = publisert rate i 14827 | 0,55 (XV: 1,5) | 0,51 (XV: 1,37) |
| D7 | 20 kapitler og 200 blokker | Eksakt | 0 |

Bygget er kjørt to ganger, og `index.html` ble byte for byte lik.

**Testet med Playwright** i 1280 og 390 px: alle kapitler i adressen (alle, II, XV, «Annen», VII, XVI, ugyldig), tastaturvalg i kapittelfiguren (Enter velger og oppdaterer adressen). Ingen feil i konsollen, og `scrollWidth` er lik bredden i begge. Første versjon hadde horisontal rulling på mobil fordi kapittelvelgeren var for bred, «+0 prosent» i teksten, dobbel indeksmerking i toppgrafikken, like akseverdier (1, 1, 2, 2) i liggetidsfiguren og en merkelapp som gikk ned i årstallene. Alt er rettet.

## 4. Nye valg til kvalitetssikring

Nummerert videre fra `02-kvalitetssikring.md`.

| # | Valg eller påstand | Hvor | Grunnlag | Må sjekkes |
|---|---|---|---|---|
| G20 | Korte kapittelnavn i hele prototypen («Øyet», «Hormoner, ernæring og stoffskifte»), med ICD-kodespenn i velgeren | Overalt | Eget valg `[T]`, utvidelse av G15 | Om fag godtar navnene |
| G21 | «Fallet i døgnopphold fra 2016 til 2018 … ser ut som en endring i kodingen.» | Toppgrafikk, XV | `[T]`. Døgnopphold for XV falt fra 26 544 (2016) til 13 584 (2018), samtidig som pasienter i O60–O75 falt fra 9 588 til 1 944 | Hva som skjedde, og om teksten bør stå |
| G22 | Raten for XV (svangerskap og fødsel) kan ikke gjenskapes: egen beregning ligger opptil 1,4 under publisert | Datasteget D6 | Kildekart, hull 8 | Hvilken nevner eller hvilket utvalg 14827 bruker for XV |
| G23 | Aldersgruppene for psykisk helsevern er tegnet som antall, ikke rate | Psykisk helsevern | Ingen rater per alder publisert, og vi har ikke regnet dem | Om antall er godt nok, eller om rater per alder trengs |
| G24 | «Kontakter per pasient» bruker pasienter i poliklinikk som nevner, ikke alle pasienter | Nøkkeltall, liggetidskort | Eget valg `[T]` | Ingen. Nevnt for fullstendighet |
| G25 | Aldersjustert rate er standardvisning i innvandringsseksjonen | Innvandring | SSBs artikkel bruker begge `[K3]` | At aldersjustert er riktig standard, gitt spørsmål 2 i innsiktsnotatet |
| G26 | «Statistikken har ikke diagnoser her» om psykisk helsevern | Seksjonsingress | Tabell 14820–14823 har ikke diagnose | At det ikke finnes diagnosetall for psykisk helsevern et annet sted hos SSB |
| G27 | «Lav bruk i en gruppe kan skyldes god helse, men også språk, avstand eller ulik henvisningspraksis.» | Lesehjelp | `[K3]` nevner språk, kjennskap til tjenestene og henvisningspraksis. Avstand er vårt tillegg `[T]` | Om «avstand» skal stå |

## 5. Kjente svakheter

- Region er ikke med (valgt bort i steg 3).
- Fordelingen av veksten (seksjon 2) avhenger av rekkefølgen på leddene. Rekkefølgen står i teksten, men alternativene vises ikke.
- Ratene per aldersgruppe gjelder begge kjønn. Kjønnsfordelt middelfolkemengde er ikke hentet.
- Lange blokknavn kuttes med «…» i figuren. Fullt navn står i tooltip og tabell.
- Kontrollrenderingen av SVG-ene i steg 2 brukte en reservefont. Siden selv bruker Open Sans fra `felles/vendor/`.

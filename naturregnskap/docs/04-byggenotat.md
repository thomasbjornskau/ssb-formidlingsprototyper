Steg 4 i formidlingsprototype for naturregnskap · versjon 0.1 · 05.11.2026 · Status: utkast (dummydata)

# Byggenotat

## Hva er bygget

Hele siden styres av ett valg: **naturtype** (økosystemtype), med 11 knapper med ikoner. Valget ligger i adressen (`#oko=04`). Det kan også gjøres ved å klikke på en stolpe eller et punkt i figurene, med mus eller tastatur.

| Seksjon | Svarer på | Innhold |
|---|---|---|
| Hode | – | Prototypemerking, dummymerking, ingress generert fra tallene, velger |
| Kort for valgt naturtype | – | Ikon og tre nøkkeltall: utbredelse, tilstand og tjenester, med fargekanten til hvert delregnskap |
| Slik leser du | H1, H2, H3, H7 | Fire punkter og konseptgrafikken i `<details>`, bred og smal |
| Toppgrafikk B | Hvordan har naturen det? | Stort tall for valgt naturtype og prikkdiagram 2019 → 2024. Våtmark er merket med * fordi den bruker Naturindeks. Fire nøkkeltall |
| Hvor mye natur har vi? | H2, H6 | Andel av landarealet, og utbygd areal 2017–2024 |
| Hvordan har naturen det? | H1, H5, H8 | Egenskapsprofil og landsdeler |
| Hva gir naturen oss? | H3, H4 | Andel av hver tjeneste som kommer fra valgt naturtype, med verdi og enhet. Hvem bruker tjenestene. Tidsserie for skog og jordbruksmark |
| Hvor sikre er tallene? | H1, H3 | Kvalitetsmatrise med ikoner. Tjenester som ikke kommer fra valgt naturtype, er nedtonet |
| Bunntekst | – | Om tallene, egne beregninger, kilder |

## Slik vises hull i data

- **Ingen samlet indeks:** jordbruksmark og åpent lavland får tekst og en egenskapsprofil.
- **Bare uskalerte variabler:** bebygd areal får en tekstboks.
- **Ingen tilstand:** kyststrender og hav får en tekstboks.
- **Utbygging som ikke kan forekomme:** bebygd areal, kystvann og hav står ikke i stolpediagrammet. I tabellen står de som «kan ikke forekomme».
- **Ingen landsdel eller tidsserie:** egen tekst som sier hvilke naturtyper som har det.
- **Tjenester:** når naturtypen ikke bidrar, er stolpen 0 og verdien «–».

## Test (Playwright, 1280 og 390 px)

- Sju naturtyper testet: skog, fjell, våtmark, jordbruksmark, bebygd, hav og innsjøer.
- `scrollWidth` var lik bredden i alle 14 tilfeller.
- Ingen feil i konsollen.
- Klikk på en velgerknapp oppdaterer adressen.
- Bygget er kjørt to ganger, og filen ble identisk (samme md5).

Rettet etter første skjermbilder: forklaringen til prikkdiagrammet lå oppå akseetiketten på mobil, akseetikettene for utbygd areal overlappet, forklaringen til brukerfordelingen ble kuttet på mobil, og verdiene i tjenestefiguren kolliderte med enhetskolonnen.

## Nye valg til kvalitetssikring (fortsetter fra 02, nr. 13–)

13. Våtmark vises i toppgrafikken med Naturindeks og *, ikke som en egen totalindeks.
14. «Andel av landarealet» bruker økosystem 01–09 som nevner.
15. Brukerfordelingen bruker fargene mørk 5, himmelblå, lilla og grå. Dette er ikke en etablert SSB-palett.
16. Kvalitetsmatrisen er ekte og hentet fra metodenotatet. Alt annet er dummy.
17. Ikonene er Lucide (ISC-lisens), i Feather-stil. Profil har ikke sett dem.
18. Tidsserier vises bare for avlinger og tømmer. Klimaregulering (2010–) mangler egen tabell.
19. Siden bruker egen `bygg.py` og vanilla SVG i stedet for `felles/bygg.py` og d3, fordi repoet ikke er tilgjengelig.

## Kjente svakheter

- Alle tall er oppdiktet. Fordelinger og nivåer kan gi feil inntrykk til de byttes ut.
- Valget av naturtype styrer ikke brukerfordelingen, fordi 14968 ikke har økosystemdimensjonen.
- Det er ingen kartvisning av landsdelene, selv om H8 tilsier det.
- Toppgrafikken viser «–» som stort tall for naturtyper uten indeks. Det kan virke tomt.

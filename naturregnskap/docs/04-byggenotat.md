Steg 4 i formidlingsprototype for naturregnskap · versjon 0.2 · 10.11.2026 · Status: utkast (dummydata med ekte kodelister)

# Byggenotat

## Endringer i versjon 0.2 (fagseksjonens svar 10.11.2026)

| Tilbakemelding | Endring i prototypen |
|---|---|
| H4 er kanskje den alvorligste: delregnskapene kan ikke leses i sammenheng | Punkt 1 i «Slik leser du» er skrevet om. Kortet for valgt naturtype har fått en egen merknad under de tre tallene |
| Egenskapene har ingen egne verdier | Seksjonen viser nå hver indikator, gruppert etter egenskap. Det er ingen snitt per egenskap og ingen egne beregninger |
| Totalindeksen er en egen variabel | Leses fra Indeks_*-kodene. Snittet av egenskapene brukes bare som kontroll |
| Global klimaregulering ligger i 14998 og ikke per hovedøkosystem | Egen figur, «Endringer i karbonlager», per EU-type. EU-typene til valgt hovedøkosystem er uthevet, og negative tall har egen farge. Karbon er tatt ut av andelsfiguren, som nå teller «N av 8» |
| Bruk «Endringer i karbonlager», 1000 tonn karbon. Tallene kan være negative | Navn og enhet er endret, og figuren tåler negative tall |
| Naturindeks skal ikke sidestilles med totalindeksen | Våtmark er tatt ut av toppgrafikken. Våtmark og åpent lavland merkes «bare biologisk mangfold» |
| Utbredelse ligger i 15036 (hovedøkosystemer, status) | Kilden er endret |
| Utbygging 2018–2024 er foreløpige tall. Kommunetall kommer 26.02.2027 | Periode, merking og tekst er endret |
| Kodelister finnes i KLASS | Alle koder og navn er ekte: 11 hovedøkosystemer, 85 indikatorer, 6 egenskaper, 5 landsdeler, 5 brukere og 9 tjenester |
| Flomdemping | Tjenestene har fått navn nær fagnavnene: Avlinger, Pollinering, Tømmer, Luftrensing, Endringer i karbonlager, Kjøling av byer, Naturbasert turisme, Naturbasert rekreasjon og Flomdemping |
| Usikkerheten er vurdert kvalitativt, men ikke tallfestet. Tilstand har intervaller | Ny tekst i «Hvor sikre er tallene?» |
| «Intakt natur», ikke «uberørt» | Brukt i hele prototypen |

## Hva er bygget

| Seksjon | Svarer på | Innhold |
|---|---|---|
| Hode og velger | – | 11 hovedøkosystemer med ikoner. Valget lagres i adressen |
| Kort for valgt naturtype | H4 | Tre tall med merknaden om at de ikke kan leses i sammenheng |
| Slik leser du | H1, H2, H4, H7 | Fire punkter og konseptgrafikken |
| Toppgrafikk B | Hvordan har naturen det? | Totalindeks for 5 hovedøkosystemer, 2019 → 2024 |
| Hvor mye natur har vi? | H2, H6 | 15036, og utbygging som foreløpige tall |
| Hvordan har naturen det? | H1, H5, H8 | Indikatorer per egenskap og landsdeler |
| Hva gir naturen oss? | H3, H4 | Andel av 8 tjenester, karbon per EU-type, brukere og tidsserie |
| Hvor sikre er tallene? | H1, H3 | Kvalitetsmatrise (ekte) |

## Test

Testet med Playwright i 1280 og 390 px bredde for 8 hovedøkosystemer: skog, fjell, våtmark, jordbruksmark, bebygd, åpent hav, kystvann og åpent lavland. Ingen feil i konsollen, og ingen vannrett rulling. Klikk på velgeren oppdaterer adressen, også for sammensatte koder. To bygg ga identisk fil (md5).

Rettet underveis:
- **Lange indikatornavn på mobil** står nå over prikkene, på opptil tre linjer.
- **Merkelapper for negative karbontall** kolliderte med kategorinavnene.
- **Aksen viste «−0».**
- **Landsdelsfiguren ble skalert opp** i bred visning.
- **Det store tallet** vises ikke lenger som «–» for naturtyper uten indeks.

## Nye valg til kvalitetssikring (fortsetter fra 02)

13. Indikatorer vises enkeltvis per egenskap. Det er ikke regnet snitt per egenskap.
14. Hovedøkosystemer kobles til EU-typer ved å lese kodene, for eksempel 05.1+06.1 → 05 og 06. Uthevingen i karbonfiguren er derfor delvis for fjell, åpent lavland, kystvann og åpent hav, og det står i teksten.
15. Andelsfiguren for tjenester teller 8 tjenester. Karbon står for seg.
16. Brukerfordelingen har fem farger, også en for investering. Det er ikke en etablert SSB-palett.
17. Ikonene er fra Lucide, og profil har ikke sett dem.
18. Siden bruker egen `bygg.py` og vanilla SVG, fordi repoet ikke er tilgjengelig.

## Kjente svakheter

- Tallene og koblingen mellom indikator og økosystem er oppdiktet.
- Brukerfordelingen er ikke styrt av valget av naturtype, fordi 14968 ikke har økosystem.
- Usikkerhetsintervallene for tilstand vises ikke ennå.
- Det er ingen kartvisning av landsdelene.

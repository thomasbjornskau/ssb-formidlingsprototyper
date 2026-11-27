Steg 4 i formidlingsprototype for naturregnskap · versjon 1.0 · 27.11.2026 · Status: utkast (ekte tall, ikke faglig kontrollert)

# Byggenotat

## Endringer i versjon 1.0 (ekte tall, 27.11.2026)

| Funn i kildekartet | Endring i prototypen |
|---|---|
| Totalindeksen finnes bare for 2024 | Toppgrafikk B viser et bilde av de fem hovedøkosystemene med totalindeks i 2024 (Thomas, 27.11.2026). Det fjerde nøkkeltallet er nå antall målinger bak indeksene (65), ikke endring i skog |
| 2019-tall finnes for noen indikatorer, men kan ikke sammenlignes (kildekart, hull 7) | Ingen 2019-verdier vises noe sted |
| Konfidensintervall finnes for skog, fjell og våtmark | Vises som strek i toppgrafikken og landsdelsfiguren, og i «Vis tallene» |
| Nevneren for andelene er alle 11 hovedøkosystemer, 469 239 km² | Andelene er regnet på nytt. Kortet og figuren sier «av hele arealet» |
| Arealet er i km², ikke 1000 hektar | Alle arealer og utbygging vises i km² |
| Utbygging er 15038, én sum for 2018–2024 | Ny kilde. Bebygd er ikke med som fra-type, og vann har ikke tall. Begge får egen tekst |
| Ingen kommunetall | Ingen kommunevelger. Teksten om kommunetall 26.02.2027 står |
| Indikator → egenskap finnes ikke i tabellene | Skog og fjell grupperes etter Miljødirektoratets tilstandsvurderinger. Åpent lavland, jordbruksmark, vassdrag og kystvann vises ugruppert, med en setning om hvorfor |
| Åpent lavland har naturindeks 0,45 | Vises i kortet og i teksten, merket «bare biologisk mangfold» |
| Tømmer er to variabler, luftrensing to | Tømmer er summen av de to. Luftrensing er PM2,5 |
| Rekreasjon summerer ikke over økosystemene | Unntatt fra summekontrollen. Teksten sier at én tur kan telle i flere økosystemer |
| `/*__IKONER__*/` og egen `bygg.py` stoppet bygget på GitHub | Ikonene ligger i `src/ikoner.json` og Roboto i `src/fonter-roboto.css`. Begge bakes inn med `/*__INKLUDER__*/`. Prototypen bygges nå med `felles/bygg.py`. `scripts/bygg.py` og `lag_dummy.py` er slettet |

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
| Toppgrafikk B | Hvordan har naturen det? | Totalindeks for 5 hovedøkosystemer, 2024, med konfidensintervall for skog og fjell |
| Hvor mye natur har vi? | H2, H6 | 15036 (km² og andel av 469 239 km²), og utbygging 2018–2024 fra 15038 som foreløpige tall |
| Hvordan har naturen det? | H1, H5, H8 | 78 indikatorer, gruppert etter egenskap for skog og fjell. Landsdeler med konfidensintervall for skog, fjell og våtmark |
| Hva gir naturen oss? | H3, H4 | Andel av 8 tjenester, karbon per EU-type, brukere og tidsserie |
| Hvor sikre er tallene? | H1, H3 | Kvalitetsmatrise (ekte) |

## Test

Versjon 1.0, 27.11.2026: testet med Playwright (`scripts/test_side.py`) i 1280 og 390 px bredde for alle 11 hovedøkosystemer og en ukjent kode. Ingen feil i konsollen, og ingen vannrett rulling. Klikk på velgeren oppdaterer adressen. To bygg med `felles/bygg.py` ga identisk fil (md5).

Rettet underveis:
- Forklaringen «95 % konfidensintervall» ble kuttet i 390 px. Den er forkortet til «95 %-intervall» i smal visning.
- Tømmerserien het «netto tilvekst», men er summen av netto tilvekst og avvirkning fra ikke-produktiv skog.
- Ingressen sa «areal på land og langs kysten», men nevneren omfatter åpent hav.

Versjon 0.2 ble testet på samme måte med dummydata.

### Kontroller i `lag_data.py` (største avvik 27.11.2026)

| Kontroll | Toleranse | Største avvik |
|---|---|---|
| Totalindeks = snitt av egenskapene, skog og fjell, alle 6 regioner | 0,01 | 0,0095 |
| Tjenester: sum av hovedøkosystemer = I alt (14967), unntatt turisme og rekreasjon | 0,1 prosent | 0,017 prosent |
| Anvendelse i alt (14968) = tilgang i alt (14967) | 0,1 prosent | 0 |
| Karbon: sum av EU-typer = I alt (14998) | 2 (1000 tonn) | 1 |
| Flomdemping: sum av landsdeler = hele landet (15000) | 5 ha eller 0,02 prosent | 15 ha (I alt) |
| Utbygging: nasjonal sum = EU-sum, og jordbruksmark = dyrket + grasmark (15038) | 0,05 og 0,02 km² | 0,01 km² |
| Kjøling: sum av bidrag = I alt (14999) | 0,02 | 0 |
| Tidsserie 2024 = tilgang i 14967 (avlinger, tømmer) | 1 | 0 |
| Alle skalerte tilstandsverdier mellom 0 og 1, alle indikatorer for skog og fjell har egenskap | – | ok |

Negativ test: grøfting i skog 2024 for hele landet ble endret fra 0,94 til 0,44 i en kopi av 15012. Bygget stoppet med «totalindeks 0.53 ≠ beregnet 0.487». Filen ble satt tilbake. Første forsøk traff 2019-verdien, som ikke inngår, og bygget gikk gjennom. Det er riktig oppførsel.

## Nye valg til kvalitetssikring (fortsetter fra 02)

13. Indikatorer vises enkeltvis per egenskap. Det er ikke regnet snitt per egenskap.
14. Hovedøkosystemer kobles til EU-typer ved å lese kodene, for eksempel 05.1+06.1 → 05 og 06. Uthevingen i karbonfiguren er derfor delvis for fjell, åpent lavland, kystvann og åpent hav, og det står i teksten.
15. Andelsfiguren for tjenester teller 8 tjenester. Karbon står for seg.
16. Brukerfordelingen har fem farger, også en for investering. Det er ikke en etablert SSB-palett.
17. Ikonene er fra Lucide, og profil har ikke sett dem.
18. Siden bruker egen `bygg.py` og vanilla SVG, fordi repoet ikke er tilgjengelig.

19. Toppgrafikken viser 2024 alene. Variant B er beholdt, men uten utvikling.
20. Indikator → egenskap for skog og fjell er hentet fra Miljødirektoratets utkast til tilstandsrapporter (01.10.2026), ikke fra SSB. Kontrollen av totalindeksen bekrefter fordelingen.
21. Luftrensing vises som PM2,5. PM10 er ikke med.
22. Tømmer er summen av netto tilvekst av produktiv skog og avvirkning fra ikke-produktiv skog.
23. Kjøling av byer bruker «bidrag», som kan summeres, ikke «gjennomsnittlig kjøling».
24. Andel av tjenesten for rekreasjon og turisme er regnet mot I alt, selv om typene summerer til mer.
25. Punkt 1 i «Slik leser du» sier fortsatt «til dels for ulike år». Det stemmer for utbygging og tidsseriene, men tilstand og tjenester gjelder 2024.

## Kjente svakheter

- Konfidensintervallet for skog (0,52–0,54) er smalere enn prikken og synes ikke i toppgrafikken. Det står i «Vis tallene».
- Vassdrag og kystvann har totalindeks uten konfidensintervall, og indikatorene er ikke gruppert. Totalindeksen kan derfor ikke kontrolleres for dem.
- Brukerfordelingen er ikke styrt av valget av naturtype, fordi 14968 ikke har økosystem.
- Flomdemping og luftrensing per landsdel (15000, 14997) er hentet og kontrollert, men ikke vist.
- Karbonlager har tidsserie fra 2010 i 14998, men bare 2024 vises.
- Det er ingen kartvisning av landsdelene.

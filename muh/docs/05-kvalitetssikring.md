Steg 5 i formidlingsprototype for muh · versjon 1.0 · 14.10.2026 · Status: til faglig kontroll

# Kvalitetssikring: Utenrikshandel med varer (muh)

Denne listen erstatter de tidligere listene i `01-innsikt.md` (spørsmål og hull), `02-kvalitetssikring.md`, `03-kildekart.md` (hull og hindre) og `04-byggenotat.md` (nye valg). Tidligere nummer står i kolonnen «Grunnlag», slik at sporet kan følges.

**Prototypen:** https://thomasbjornskau.github.io/ssb-formidlingsprototyper/muh/index.html (versjon 0.1)

Tallene i prototypen er hentet fra statistikkbanken og kontrollert ved hvert bygg (elleve sum- og metodekontroller, se `04-byggenotat.md`). Det som skal kontrolleres her, er tolkninger, avgrensninger og formuleringer.

## A. Må avklares

Det som kan være feil, eller som gir et misvisende inntrykk hvis det er feil.

| # | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 1 | Fastlandsbalansen brukes som motstykke til handelsoverskuddet, og toppgrafikken sier at «fastlands-Norge kjøpte varer for om lag 350 milliarder kroner mer enn det solgte i 2025» | Toppgrafikk, «Hva forteller handelsoverskuddet?» | Tabell 08800 (Hbtusorn). Steg 2 T8 | Er dette en forsvarlig lesning? Importen i fastlandsbalansen omfatter også råolje og varer til sokkelen |
| 2 | Pris- og volumindeksene (06322) brukes til å skille pris og mengde, og volumindeksen kalles «mengde». Teksten sier at verdien kan endre seg mye uten at Norge selger mer, når prisene på olje og gass svinger | «Slik leser du», «Pris eller mengde?» | 06322: pris +81,8 og volum +0,2 prosent i 2022. Steg 2 T5–T6 | Er indeksene egnet til dette, og er «mengde» riktig ord? Tabellen har produsentprisindeksen som kontakt |
| 3 | «Olje og gass» er råolje, naturgass og kondensater. Andelen var 57 prosent i 2025 | Ingress, «Hvor mye av eksporten er olje og gass?» | 08800. Steg 2 T1 | Er avgrensningen den dere bruker? SSB-rapporten «Norges varehandel med utlandet» (2026/27) sier «godt over 60 prosent», ifølge et sammendrag vi har lest |
| 4 | Tresifret SITC summerer ikke til totalen: 16,8 mrd. kr av eksporten i 2025 finnes bare på ensifret nivå, nesten alt i kjemiske produkter | «Hva selger fastlands-Norge?», merknad under figuren | 08819 mot 08809, kontroll K6. Steg 3 hull 6, steg 4 B5 | Hva er årsaken? Er det konfidensialitet, og kan det stå i prototypen? |
| 5 | «Uspesifisert» import (kode 97) vises som egen grå stolpe: 29,9 mrd. kr i 2025, finnes fra 2023 | «Hvem handler Norge med?», kortet for Uspesifisert | 08804. Kode 90 har samme tall, men vi bruker 97. Steg 3 hull 4–5, steg 4 B6 | Hva er denne importen, hvorfor fra 2023, og er 97 riktig kode å telle? |
| 6 | «Olje og gass i rør føres som eksport til landet røret går til, selv om den kan selges videre derfra» | «Hvem handler Norge med?», kortet for hvert land med olje og gass | «Om statistikken» (2015) sier dette om olje til Storbritannia. Vi bruker det også om gass. Steg 4 B3 | Gjelder det gass og alle rørledninger? Er formuleringen riktig? |
| 7 | Revisjonene: eksporten i en måned ble i snitt endret 4,3 prosent fra første til endelige tall, mest i desember 2021 (+23,6 prosent). Teksten knytter revisjonene til anslått pris på olje og gass | «Hvor sikre er de siste tallene?», «Slik leser du» | 12308, vår beregning. Steg 2 G4, G6, steg 3 hull 10 | Er dette en riktig framstilling, og er anslått pris hovedårsaken til de store revisjonene i 2021–2022? |
| 8 | Definisjonene i konseptgrafikken og bunnteksten bygger på «Om statistikken» fra 2015: tolldeklarasjoner, FOB og CIF forenklet, småsendinger under om lag 1 000 kr og transitt holdt utenfor | Konseptgrafikken, bunnteksten | Vi har ikke fått lest dagens «Om statistikken». Steg 1, steg 2 G1–G3, G8 | Er definisjonene og grensene fortsatt riktige? |

## B. Bør leses

Formuleringer, kortnavn, tolkninger, søkeord og egne valg.

| # | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 9 | «Handelsoverskuddet følger prisene på olje og gass, ikke hvordan det går i fastlandsøkonomien» | Toppgrafikk | Vår tolkning, støttet av 06322 og av at fastlandsbalansen har vært negativ hvert år. Steg 4 B2 | Formuleringen |
| 10 | Synonymlisten: 32 søkeord, 7 merket usikre (england, skottland, wales og nord-irland til Storbritannia, korea til Sør-Korea, dubai og abu dhabi til De forente arabiske emirater) | Søket | `data/synonymer.json`. Steg 4 B1 | Om noen koblinger er misvisende, og om viktige søkeord mangler |
| 11 | Kortnavn for ensifret SITC, for eksempel «Olje, gass, strøm og annen energi» for gruppe 3 og «Ferdigvarer» for gruppe 8 | Kortet for hvert land | Fulle navn i tabeller og verktøytips. Steg 4 B4 | Kortnavnene |
| 12 | Fastlandsbalansen regnes også per land: fastlandseksport minus import utenom skip og plattformer | Kortet for hvert land | Samme definisjon som for hele landet. SSB publiserer den ikke per land. Steg 4 B7 | Om den bør vises per land |
| 13 | Revisjonsfiguren bruker siste kjente tall for måneder som ikke er endelige, merket grått | «Hvor sikre er de siste tallene?» | Steg 4 B8 | Om framstillingen er rimelig |
| 14 | Prosentendring vises ikke for beløp under 0,5 mrd. kr | Regnestykket for fastlandseksporten | Kondensater, skip og plattformer var 14 mill. kr i august 2026. Steg 4 B9 | Ingen, til orientering |
| 15 | Konseptgrafikken har fire trinn. Strøm er forenklet til «målt ved kablene til utlandet», og endelig pris for olje og gass kalles «faktisk pris» | Konseptgrafikken | Steg 2 G2, G4, G9 | Forenklingene |
| 16 | «0» i landtabellen vises som «under 0,5 mill. kr», ikke som null | Kortet og søket | SSBs vanlige symbolbruk. Steg 3 hull 3 | At tolkningen er riktig |
| 17 | Landvalget viser bare enkeltland. EU, Norden, OECD og andre grupper er utelatt | Søket | EU skifter innhold fra år til år, og OECD er ulik i 08804 og 08809. Steg 3 hull 7 | Om grupper bør med |
| 18 | Toppgrafikken bruker siste hele år (2025), og nøkkeltallene viser også januar–august 2026 | Toppgrafikk | Månedsandelen svinger mye. Steg 2 T3 | Om siste tolv måneder er bedre |
| 19 | «Bare varer er med. Frakt, reiser, konsulentarbeid, renter og utbytte er ikke med. Hele regnskapet med utlandet står i utenriksregnskapet» | «Slik leser du» | Vår formulering. Steg 1 H3 | Formuleringen |

## C. Spørsmål

| # | Spørsmål | Grunnlag |
|---|---|---|
| 20 | Stemmer hypotesene om misforståelser (H1–H10 i `01-innsikt.md`)? Hvilke møter dere oftest, og mangler noen? | Steg 1, del 4 |
| 21 | Bør en slik oversikt bygge på siste måned, eller på årstall med siste måned som tillegg, slik den gjør nå? | Steg 1 spørsmål 2 |
| 22 | Hvem bør kontrollere delen om pris og volum? | Steg 1 spørsmål 4 |
| 23 | Hva har endret seg i «Om statistikken» siden 2015-versjonen (HS-versjon, sesongjustering, kilder)? | Steg 1 spørsmål 6 |
| 24 | Er dere rett mottaker, eller bør andre se på deler av prototypen, for eksempel utenriksregnskapet for punkt 19? | Fagkontakt ikke bekreftet |

## Avklart underveis

| # | Hva | Hvordan |
|---|---|---|
| 25 | Om propan, butan og strøm er med i fastlandseksporten | Bekreftet: fastlandseksporten gjenskapes nøyaktig som total minus råolje, kondensater, naturgass og skip og plattformer (kontroll K5). Var åpent i steg 1 |
| 26 | Fire formuleringer rettet ved gjennomgangen i steg 5 | «selges videre» ble «kan selges videre». «Tallene er ikke sesongjustert» ble «tallene her er ikke sesongjustert», fordi SSB publiserer sesongjusterte tall (08864). «Største varen» ble «største varegruppen». «Negativ hvert år siden 1960» ble «fra 1960 til 2025», fordi serien starter i 1960 |
| 27 | Tidligere avvik i prototypen | Doble årstall på månedsaksene, meningsløs prosent på et lite beløp, «Uspesifisert» rangert som land og kortet som ikke fulgte tilbakeknappen er rettet i steg 4 |
| 28 | Teknisk, ikke fagets ansvar: rådataene er rekonstruert fra SSB-tilkoblingen, og `hent_data.py` er ikke kjørt mot API-et | Kjøres før neste versjon. Kontrollene stopper bygget hvis tallene ikke går opp. Steg 3 hull 1–2 |
| 29 | Teknisk: URL-formatet i `kilder.json` | Bruker `selection[...]` som kpi og regfram |
| 30 | Teknisk: månedstallene gjelder publiseringen 15.09.2026 | Oppdateres med `hent_data.py` før versjon 0.2. Steg 3 hull 8 |
| 31 | Teknisk: midlertidig grafikkbibliotek fra steg 2 | Erstattet av `scripts/grafikk_muh.py` i statistikkmappen. Steg 2 X1 |

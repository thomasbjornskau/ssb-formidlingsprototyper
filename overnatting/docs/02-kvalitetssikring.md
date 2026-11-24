Steg 2 i formidlingsprototype for overnatting · versjon 0.2 · 24.11.2026 · Status: godkjent av Thomas

**Valg 24.11.2026.** Konseptgrafikken er godkjent. Toppgrafikk A er valgt. C skal bli en egen seksjon («Hvem overnatter»), og B går inn i «Slik lages tallene».

# Kvalitetssikring av konseptgrafikk og toppgrafikk

**Merking** som i `01-innsikt.md`. Kildene [K1]–[K14] står der. Tallene i grafikken er hentet fra data.ssb.no 24.11.2026 og ligger i `data/grafikk-utkast.json`. De erstattes av `data/raw/` i steg 3.

Kolonnen «Sjekkes av» skiller mellom det vi kan sjekke selv i steg 3 og det fag må svare på i steg 5.

## Konseptgrafikken «Slik lages tallene»

| # | Påstand eller valg | Grunnlag | Hva må sjekkes | Sjekkes av |
|---|---|---|---|---|
| Q1 | Eksempelet gir «10 overnattinger og 4 ankomne gjester» for et par med to opphold | [K1]: en ankomst telles én gang per person og opphold. At ankomst telles per bedrift er [T] | Telles ankomst per bedrift? Dette er H2, og eksempelet bygger på det | Fag |
| Q2 | «Det er bostedet som teller, ikke passet» | [K1] | Ingenting. Formuleringen «passet» er vår | – |
| Q3 | Månedlig rapportering i Altinn, skjema eller bookingsystem, frist 10 dager | [K1] | Ingenting | – |
| Q4 | Lista over hvem som rapporterer: alle hotell, camping ≥ 20 enheter, hyttegrender ≥ 10 senger, alle vandrerhjem, 42 formidlere | [K1] gjennom oppsummering | Les panelet «Omfang» ordrett. Har hotell virkelig ingen nedre grense? | Steg 3, deretter fag |
| Q5 | «Hotellene oppgir også formål, rom, senger og losjiomsetning» | [K1], tabellene 14166 og 14176 | Ingenting | – |
| Q6 | Om lag 2 prosent frafall, anslått fra bedrifter som har svart | [K1] sier ca. 2 prosent i ett panel og under 3 prosent i Feilkilder | Hvilket tall gjelder? | Fag |
| Q7 | Ny campingmetode fra februar 2026, faste faktorer per måned og fylke, vær og etterspørsel kommer ikke med | [K1][K2][K4] | Ingenting. Bruddet skal stå i tidsseriene (H7) | – |
| Q8 | Publisering 3–4 uker etter, land, fylke, 66 reiselivsregioner og kommune | [K1][K12] | Ingenting | – |
| Q9 | «Tall fra færre enn tre bedrifter vises som «:»» | [K1]: «normalt» når færre enn tre enheter | Vi har strøket «normalt». Er det greit? | Fag |
| Q10 | September 2026: 3 448 079 kommersielle overnattinger og 77 403 i fritidsboliger | Tabell 14162 og 13100 | Sjekkes mot `data/raw/` | Steg 3 |
| Q11 | «Land og fylker får også sesongjusterte tall» | Tabell 14178 har 17 regioner, ingen reiselivsregioner | Ingenting | – |
| Q12 | Ikke med: egen hytte, familie og venner, 58,2 mill. i 2025 | Tabell 11270, «ikke kommersiell innkvartering». Eksemplene hytte, familie og venner er [T] | Hva omfatter «ikke kommersiell» i Reiseundersøkelsen? | Steg 3, fagkontakt for Reiseundersøkelsen |
| Q13 | Ikke med: 6,4 mill. overnattinger via plattformer i 2023 | [K6], eksperimentell statistikk | Finnes tall for 2024 eller 2025? Bruk det nyeste | Steg 3 |
| Q14 | Ikke med: bobil og telt utenfor campingplass, cruiseskip | [T]: følger av omfanget i [K1], men står ikke der | Bekreft | Fag |
| Q15 | Fargevalg: lilla for gjest (person), grønn for data og tall, stiplet grå for det som er utenfor | `ssb-konseptfigurer` | Ingenting | – |

## Toppgrafikk A: rekord, men ikke opp

| # | Påstand eller valg | Grunnlag | Hva må sjekkes | Sjekkes av |
|---|---|---|---|---|
| A1 | 2 579 128 hotellovernattinger, flest i en september | 14162. SSB sier det samme [K2] | «Noen gang» gjelder serien fra 1985 [K1]. 14162 starter i 2016 | Steg 3: sjekk 14166 tilbake til 1986 |
| A2 | +2,7 prosent fra september 2025 | Regnet fra 14162, samme som SSB [K2] | Ingenting | – |
| A3 | −0,8 prosent fra august, sesongjustert | Regnet fra publiserte sesongjusterte nivåer i 14178. SSB publiserer ikke endringsraten | Er det en endring SSB står inne for? Sesongjusterte tall revideres årlig | Fag (spørsmål 6 i 01) |
| A4 | Brudd markert mellom 2019 og 2020 | [K1]: «utvidingar kom også i 2020» for hotell | Hvor stort var bruddet? Ligger det i september 2020? Merket kan blandes med pandemien | Fag |
| A5 | Avkortet y-akse (2,2–2,5 mill.) i linjen | Lov i linjediagram når endringen er poenget (`ssb-diagramstandard`) | Den sesongjusterte serien er hakkete. Leseren kan tro at fallet er stort | Thomas |

## Toppgrafikk B: 7 av 10 netter er ikke med

| # | Påstand eller valg | Grunnlag | Hva må sjekkes | Sjekkes av |
|---|---|---|---|---|
| B1 | 58,2 av 83,4 mill. overnattinger var ikke-kommersielle, «7 av 10» | Tabell 11270, 2025K1–K4 summert | Kan kvartalene summeres til år? Populasjon og alder i Reiseundersøkelsen | Steg 3 |
| B2 | «De er ikke med i overnattingsstatistikken» | [K1]: omfanget | Kan noe ikke-kommersielt likevel være med, for eksempel fritidsboliger via formidler? | Fag |
| B3 | Søyle 2: 26,4 mill. norske overnattinger i overnattingsstatistikken | 14162, 2025 | At den ligger nær 25,2 mill. kommersielt i Reiseundersøkelsen er en grov sammenligning av to ulike kilder, og det står i grafikken | Fag |
| B4 | Kombinerer to statistikker i én toppgrafikk | Bevisst valg for å svare på spørsmål 5 og H1 | Vil seksjonen akseptere at Reiseundersøkelsen står i overnattingsprototypen? | Thomas, deretter fag |

## Toppgrafikk C: utlendinger på hotell driver veksten

| # | Påstand eller valg | Grunnlag | Hva må sjekkes | Sjekkes av |
|---|---|---|---|---|
| C1 | +58 075 utenlandske hotellovernattinger, større enn hele veksten i kommersielle overnattinger (+53 750) | 14162, regnet fra publiserte nivåer | Ingenting. Tallet i overskriften er avrundet til +58 000 | – |
| C2 | Campingplassene hadde 18 547 færre overnattinger | 14162 | Nedgangen kom samme år som den nye metoden, som skulle gi høyere tall [K2]. Skal det stå et forbehold? | Fag |
| C3 | «Utenlandske gjester registreres etter landet de bor i» | [K1] | Plattformbooking kan gi feil land [K2] (H6). Linjen tar ikke med det forbeholdet | Thomas |
| C4 | Farger: blå for utenlandske, grønn for norske, i flatetone | `ssb-diagramstandard`, plass 1 og 2. Merket direkte | Ingenting | – |

## Felles valg

| # | Valg | Begrunnelse | Avvik |
|---|---|---|---|
| F1 | Stort tall i Open Sans Bold, ikke Roboto Condensed | `ssb-diagramstandard`, tittelfonten er en åpen avgjørelse | Kan avvike fra kpi og regfram. Sjekkes mot malen i repoet |
| F2 | Kildelinje 13 px | Diagramstandarden har 12 px som minimum på skjerm | – |
| F3 | Primitivene ligger i `scripts/grafikk_overnatting.py` | Repoet har ingen `felles/grafikk.py`. Samme praksis som `grafikk_muh.py` | – |
| F4 | Roboto Condensed finnes ikke i arbeidsområdet. Tittelen i konseptgrafikken ble rendret med reservefont | Fontoppsett | Sjekk i nettleser med Roboto Condensed |
| F5 | Konseptgrafikken bruker bare hele landet, ikke reiselivsregion | Den forklarer metoden, ikke tallene | – |

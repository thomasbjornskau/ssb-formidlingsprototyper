Steg 4 i formidlingsprototype for ufore · versjon 0.1 · 09.11.2026 · Status: utkast, til gjennomsyn hos Thomas

# Byggenotat

Bygger på `01-innsikt.md` (gjennomgående valg: alder), toppgrafikk A fra steg 2 og dataomfanget «stor» fra steg 3.

## Hva som er bygget

| Seksjon | Svarer på | Innhold |
|---|---|---|
| Hode | – | Prototype-merking, ingress generert fra tallene, velger for alder (alle, 18–67 ettårig) og kjønn |
| Kort for valgt alder | 2 | Andel og antall for valgt alder og kjønn i 2025, endring fra 2015, liten linje |
| Slik leser du tallene | H1, H3, H5, H6 | Fire punkter og konseptgrafikken (bred og smal) i `<details>` |
| Toppgrafikk A | 1 | 389 000, andel 2015–2025, dekomponering av økningen, fire nøkkeltall |
| Hvem er uføretrygdet? | 2 (H2, H4, H10) | Aldersprofil 2015 mot 2025 med valgt alder (klikk eller piltaster), utvikling for valgt alder mot 18–67, nye uføretrygdede for aldersgruppen |
| Jobber uføre? | 3 (H5, H6) | Arbeidsintensitet og uføregrad etter aldersgruppe 2025, valgt gruppe markert |
| Utdanning | 4 (H7) | Andel etter utdanningsnivå 2015 og 2025 for valgt aldersgruppe og kjønn, med antall i kildelinjen |
| Min kommune | 5 (H8) | Søk (kommune eller fylke), tekst og fire nøkkeltall med aldersjustert indeks, tidsserie 2015–2025 med «ut fra alder» og landet, spredningsdiagram for alle 357 kommuner (klikk for å velge), fylkene sortert etter indeks |
| Om tallene | – | Definisjon, egne beregninger, tabeller med oppdateringsdato, hentedato |

Valget ligger i adressen: `#alder=29&kjonn=kvinner&kommune=3401`. Ugyldige verdier faller tilbake til standard (alle, begge kjønn, hele landet).

Alle figurer har «Vis tallene» med tabell, kildelinje med tabellnummer og oppdateringsdato, og tekstalternativ (`aria-label`). Aldersfiguren kan styres med piltaster, Home og End. Fylkesnavnene i fylkesfiguren kan velges med Enter og mellomrom. Søket er en `combobox` med `listbox`, piltaster, Enter og Escape.

## Hvordan hull i data vises

- **Kommuner uten sammenlignbar serie** (fra delingene Stokke 2017, Tysfjord 2020, Snillfjord 2020 og Ålesund 2024): stiplet boks med hvilke år som mangler og hvilken kommune som ble delt, stiplet loddrett linje «Ny inndeling» i tidsserien, og «mangler» i tabellen. Linjen brytes, den trekkes ikke over hullet. Det gjelder ni kommuner: Tønsberg og Sandefjord (2015–2016), Narvik, Hamarøy, Heim, Hitra og Orkland (2015–2019), Ålesund og Haram (2015–2023).
- **Søk uten treff:** tekst med lenke til tabellen over alle kommunene.
- **Små kommuner** (under 300 uføretrygdede): egen setning om at tallene kan svinge.
- Ingen celler i rådataene hadde statussymbol utenom «.» for regioner som ikke fantes.

## Kontroller i `lag_data.py`

86 kontroller. Bygget stopper hvis én feiler. Negativ test 09.11.2026: +7 på Oslo 2020 i `regioner.json` stoppet bygget i K9.

| Kontroll | Toleranse | Største faktiske avvik |
|---|---|---|
| K1 kvinner + menn = begge (land) | 0 | 0 |
| K2 bosatt i 11824 = antall i 11695 | 5 | 3 (konfidensialitetsavrunding mellom tabeller) |
| K3 ettårige aldre summerer til 18–67 | 0 | 0 |
| K4 11828 = 11695 for landet | 0 | 0 |
| K5 egen andel per alder og kjønn = publisert (nevneren) | 0,051 | under 0,05 |
| K6 dekomponeringen summerer til endringen | 0,5 | under 0,01 |
| K7 arbeidsintensitet summerer til 100 | 0,21 | under 0,21 |
| K8 utdanningsnivåene summerer til i alt | 0 | 0 |
| K9 kommunene summerer til landet, hvert år | 0 | 0 |
| K10 befolkning i kommunene = landet 18–67, hvert år | 0 | 0 |
| K11 omkodet sum + kommuner uten serie = landet, hvert år | 0 | 0 |
| K12 egen kommuneandel 2024–2025 = publisert | 0,051 | under 0,05 (unntatt Risør og Tvedestrand 2024, se G21) |
| K13 sum forventet = landets antall, 2024–2025 | 0,5 | under 0,5 |
| K14 fylker 2024–2025 = publisert | 0 | 0 |
| K15 fylkene summerer til landet, hvert år | 0 | 0 |
| K16 egen fylkesandel 2025 = publisert | 0,051 | under 0,05 |

I tillegg stopper bygget hvis en kommune har antall ulikt 0 der andelen har «.», hvis en kode ikke kan føres fram til en gyldig 2025-kode, eller hvis en delt kommune spenner over flere fylker.

## Nye valg til kvalitetssikring

Nummerert videre fra `02-kvalitetssikring.md`.

| Nr. | Valg eller påstand | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| G17 | Dekomponeringen bruker snittet av alle seks rekkefølger (Shapley), med alder × kjønn som celler: vekst 23 377, aldring 10 833, høyere andel 26 821. Vist avrundet til tusen | Kildekartet M3 [T] | Om fag godtar metoden og at den vises på siden. Toppgrafikk A i steg 2 (SVG-utkastet) har de gamle tallene og er ikke brukt i prototypen |
| G18 | Aldersjustert indeks (indirekte standardisering etter alder og kjønn), landet = 100, og «andel ut fra alder og kjønn» | Kildekartet M4 [T] | Om fag godtar betegnelsene og metoden. Indeksen har ingen usikkerhetsmål |
| G19 | Kommuneserier 2015–2023 omkodet til 2025-inndeling via Klass 131. Uføretallene og befolkningen omkodes hver for seg, fordi befolkningen per 1.1. bruker inndelingen per 1.1. | Klass-endringer 2015–2025 [T] | At sammenslåtte kommuner kan summeres bakover. Grensejusteringer uten kodeendring er ikke med |
| G20 | Kommuneandeler før 2024 er egne beregninger (antall / befolkning), ikke publiserte tall. 2024 og 2025 er publiserte andeler | K5 og K12 viser at metoden gjenskaper publiserte andeler [T] | At egne andeler for omkodede år kan presenteres på linje med publiserte |
| G21 | Risør og Tvedestrand 2024: egen andel avviker 0,3 prosentpoeng fra publisert, trolig grensejustering 1.1.2025. Prototypen viser publisert andel | Feilet K12 første gang [T] | Hva som skjedde mellom Risør og Tvedestrand |
| G22 | Teksten om små kommuner kommer under 300 uføretrygdede | Eget valg [T] | Om grensen er rimelig |
| G23 | Fylkene sorteres etter indeks, ikke andel | Eget valg for å motvirke H8 [T] | Ingen faglig |
| G24 | H8 omformulert: alder og kjønn forklarer om lag en firedel av forskjellene mellom kommunene | Korrelasjon 0,49 mellom forventet og faktisk andel 2025 (kildekartet M4) | At påstanden i seksjonsingressen («en del av forskjellen») er dekkende |
| G25 | Nye uføretrygdede: «Tilgangen svinger med regler og saksbehandling for AAP, som de fleste kommer fra» | NAV statistikknotis juni 2026 [K7]: 81,9 prosent fra AAP i 2. kvartal 2026 | At NAVs forklaring kan brukes i en SSB-prototype |
| G26 | Utdanningsnote: «Unge som blir syke, fullfører sjeldnere videre utdanning» | [T], støttet av SSB-artikkel 2026 [K3] | At formuleringen ikke går lenger enn grunnlaget |
| G27 | NAV-tallet 374 900 står i lesehjelpen | SSB-artikkel 23.06.2026 [K3] | Som G7 |

## Kjente svakheter

- Bygget med repoets egen `felles/bygg.py` og `felles/vendor/` (d3 7.9.0 og Open Sans). Ingen nye fellesfiler. Overskrifter og store tall bruker Open Sans, som i `pasient`, fordi Roboto ikke finnes i `felles/vendor/`. Konseptgrafikken bruker fontstakkene fra konseptfigurstandarden, med Arial som reserve.
- Byggekontrollen for hele repoet ble kjørt lokalt 09.11.2026: alle prototyper bygger likt, men `naturregnskap` stopper med «ukjent plassholder igjen i malen: /*__IKONER__*/». Feilen fantes før ufore og gjør trolig kontrollen i GitHub Actions rød.
- Filen er 621 kB, hvorav d3 er 280 kB, Open Sans 110 kB og data om lag 170 kB.
- Spredningsdiagrammet har ikke tastaturnavigasjon mellom prikkene. Kommunene velges med søket.
- `scripts/lag_grafikk.py` og `scripts/grafikk_ufore.py` er grafikkutkastene fra steg 2 (samme mønster som `grafikk_pasient.py`). `lag_grafikk.py` leser rådatafiler fra steg 2 som er erstattet av `data/raw/`, og er ikke en del av bygget.
- Arbeidsintensitet og uføregrad vises bare for 2025. 2015 står i tabellen.
- Ingen kart. Kommunegrenser for 2025 er ikke hentet. Det kan legges til.

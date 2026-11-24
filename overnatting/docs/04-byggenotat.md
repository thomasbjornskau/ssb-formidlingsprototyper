Steg 4 i formidlingsprototype for overnatting · versjon 0.1 · 24.11.2026 · Status: sett av Thomas, til faglig kontroll

# Byggenotat: Overnattingar (overnatting)

**Merking** som i `01-innsikt.md`. Kontrollene K1–K12 står i `03-kildekart.md`, B1–B5 i `scripts/lag_data.py`.

**Valg som ligger til grunn.** Reiselivsregion (Reiselivsregionar 2024) er hovedvalget. Toppgrafikk A, konseptgrafikken, C som egen seksjon og B i «Slik lages tallene» (steg 2). Landtall per region fra 2018 (steg 3). Månedsserien med synlige hull er grunnformen, og årstall vises bare når alle månedene er publisert (valgt av Thomas 24.11.2026).

**Utgangspunkt.** CSS, verktøy (`lerret`, `yakse`, `talltabell`, `visTips`) og søket (`lagSok`, `kobleSok`) er kopiert fra `innvbef-omrade`. Kartprojeksjonen er den samme som i `arealprofiler` og `innvbef-omrade`. Innholdet er skrevet nytt.

**Siden** er én fil på 1 433 kB. Datafilen er 938 kB, kartet 187 kB av den. To bygg gir identisk fil. Testet i Chromium i 1280 og 390 px uten feil i konsollen og uten horisontal rulling.

---

## 1. Hva som er bygget

| Seksjon | Svarer på | Innhold |
|---|---|---|
| Hode | – | Ingress generert fra siste måned. Fylkesvelger, søk på reiselivsregion, kommune eller sted, «Se alle regioner» og eksempler (Hemsedal, Geiranger, Lofoten, Midt-Telemark, Jotunheimen, Atlantis) |
| Kort for valgt område | 3 | Navn, fylke, kommunene i regionen (fra KLASS), søkeordet treffet kom fra, hotell og camping m.m. siste 12 måneder med antall skjulte måneder, andel utenlandske på hotell |
| Slik leser du tallene | H1, H2, H3, H8, H11 | Fire punkter med tall: overnatting og gjest, rekord og vekst, bare kommersielle, hull er ikke null. I «Slik lages tallene»: konseptgrafikken (bred og smal) og B som figur (Reiseundersøkelsen mot overnattingsstatistikken) |
| Toppgrafikk A | 1 | Alltid hele landet, hotell. Samme måned hvert år 2016–2026 med brudd i 2020, og sesongjustert linje for de siste 24 månedene. Fire nøkkeltall: alle kommersielle overnattinger, andel utenlandske, losjiomsetning, pris per rom |
| Måned for måned | 1, 3 | Bryter hotell eller camping m.m. Månedslinje for norske og utenlandske med skravur der tallet er skjult, siste tre år eller alle måneder fra 2016. Brudd: flere hotell 2020, ny campingmetode februar 2026 |
| Per år | 3 | Stablede stolper 2018–2025 og siste 12 måneder. «:» der minst én måned er skjult, med antall måneder i teksten |
| Kart | 3, H6 | De 66 regionene. Andel utenlandske eller endring fra året før, siste 12 måneder, for valgt gruppe. Skravur der en måned er skjult. Svalbard som egen rute. Klikk og piltaster velger region |
| Hvem overnatter | 2 (C) | Endring fra samme måned året før etter gruppe og bostedsland (tre grupper for landet og fylker, to for regioner). Største land siste 12 måneder med endring. Valgt land per år 2018–siste 12 måneder |
| Hotellene | 4, H5 | Kapasitetsutnytting av rom og senger fra 2022, med hele landet som stiplet referanse. Punktstriper for alle regioner siste måned: kapasitetsutnytting av rom, pris per rom, losjiomsetning per tilgjengelig rom |
| Bunntekst | – | Om tallene, egne beregninger, kilder, kartkilde, hentedato og lenke til ssb.no/overnatting |

Valget ligger i adressen: `#omrade=33104` (Hallingdal), `#omrade=46` (Vestland), `#omrade=18105&land=144` (Lofoten, Tyskland).

---

## 2. Hvordan hull i data vises

- **Måneder:** skravert bakgrunn i månedslinjen og et varsel med antall skjulte måneder det siste året. Linjen brytes, den trekkes aldri over hullet.
- **År og 12 måneder:** «:» når minst én måned er skjult, med antall måneder i noten og i tabellen.
- **Regionens total:** finnes bare når både hotell og camping m.m. er publisert. Kortet viser gruppene hver for seg.
- **Land per region:** når én gruppe er skjult, brukes den andre. Stolpen skraveres, og teksten sier hvilken gruppe den gjelder.
- **Alt skjult:** en tekst i stedet for figuren, med forslag om å velge den andre gruppen, fylket eller hele landet. Aldri en tom akse.
- **Kart:** skravur for regioner med minst én skjult måned. 14 regioner for hotell, siste 12 måneder.
- **Endring fra et lite tall:** landendring vises bare når landet hadde minst 100 overnattinger året før (India gikk fra 2 til 255 i Midt-Telemark).

---

## 3. Kontroller i bygget

| # | Kontroll | Største faktiske avvik |
|---|---|---|
| K1–K12 | Kontrollene fra steg 3, kjørt fra `lag_data.py` | Som i kildekartet. Bygget stopper hvis én feiler |
| B1 | Landene summerer til utlandet i alt per område, gruppe og periode der alle måneder er publisert | 57 (2020, kjent fra K3). Toleranse 100 |
| B2 | Regionene summerer til fylket per periode der alle regionene er hele | 0 |
| B3 | 65 regioner har kartflate, Svalbard ikke | – |
| B4 | Synonymene peker på kommuner i KLASS | – |
| B5 | Tallene i toppgrafikken er de samme som i steg 2 (for september 2026) | 0 |

**Negativ test.** Én verdi i `region_tid.json` ble økt med 1. Bygget stoppet med «Kontroll feilet: kontrollene fra steg 3: … K2, K8». Filen ble satt tilbake, og bygget gikk gjennom.

---

## 4. Nye valg til kvalitetssikring

Nummerert videre fra `02-kvalitetssikring.md`.

| # | Valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| N1 | Toppgrafikken viser alltid hele landet, også når en region er valgt | Sesongjusterte tall finnes ikke per region (14178) | Thomas: er det forståelig når resten av siden følger regionen? |
| N2 | «Flest i en september siden serien starter i 1986» | 14166 fra 1986. Om statistikken: sammenlignbart fra 1985, utvidelse i 2020 | Fag: kan vi si det slik med bruddet i 2020? |
| N3 | Sesongjustert endring fra forrige måned som eget tall | Egen beregning fra publiserte nivåer (A3) | Fag |
| N4 | Kartklasser: kvintiler for andel utenlandske, faste grenser (±2 og ±10 prosent) for endring | Diagramstandarden sier kvantiler. Faste grenser gjør null til midtpunkt i den divergerende skalaen | Thomas |
| N5 | Kartet og «Største land» bruker siste 12 måneder, ikke siste måned | Gir stabile tall og færre hull | – |
| N6 | Regionene som kartflater er laget ved å slå sammen kommunegrensene etter KLASS | Ikke et SSB-kart. Kommunegrensene fra robhop (som `innvbef-omrade`, C9) | Om SSB har et offisielt kart for reiselivsregioner |
| N7 | Svalbard vises som en rute uten geografi | Ingen kommune og ingen geometri | – |
| N8 | Søk på alle 357 kommunenavn og 28 steder i `data/synonymer.json`. Fem er merket usikre (Jotunheimen, Hardanger, Sørlandet, Nord-Norge, Fjord-Norge) | Egen liste | Thomas: flere steder? Er de usikre nyttige eller forvirrende? |
| N9 | Land per region når én gruppe er skjult: bare den andre gruppen, skravert | Valg 24.11.2026 om hull | Fag: er det greit å vise «bare camping» for en region? |
| N10 | Landendring vises bare når året før har minst 100 overnattinger | Unngår «+12 650 %» | – |
| N11 | Punktstripene viser siste måned, som svinger med sesongen | Ingen publiserte 12-månederstall for hotellmålene | Thomas: heller siste 12 måneder regnet av oss? |
| N12 | Endringsfiguren har tre grupper for landet og fylker (14162), men to for regioner (14172) | Tabellene har ulik inndeling | – |
| N13 | B-figuren setter Reiseundersøkelsen ved siden av norske overnattinger i 14172 | B1–B4 i steg 2, populasjon i kildekartet | Fag, og fagkontakt for Reiseundersøkelsen |
| N14 | Lesehjelpen sier at «Polen og Litauen kan være arbeidsreiser» | H12, skjemaveiledningen RA-0366 | Fag |

---

## 5. Kjente svakheter

- **Kartet kan ikke nås region for region med Tab.** Piltastene velger neste og forrige region, og søket og tabellen under kartet er alternativene.
- **Fylkesmarkeringen** tegner omrisset av alle regionene i fylket, også grensene mellom dem.
- **Siden er 1,4 MB.** Landtallene per region (2018–) er det meste. Fullt dataomfang var et bevisst valg.
- **Hotellmålene per region** vises fra 2022, ikke fra 2016.
- **Roboto Condensed** finnes ikke i arbeidsområdet. Tittelen i konseptgrafikken er sett med reservefont.
- **Bruddet i campingtallene** fra februar 2026 er bare markert i campingvisningen og i teksten, ikke i kartet.
- **Synonymlisten er kort.** Navn på fjell, øyer og skisteder bør prøves av brukere.

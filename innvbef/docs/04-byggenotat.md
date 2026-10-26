Steg 4 i formidlingsprototype for innvbef · versjon 1.0 · 26.10.2026 · Status: utkast

# Byggenotat: Innvandrere og norskfødte med innvandrerforeldre (innvbef)

Bygger på `03-kildekart.md` og valgene i steg 2 og 3. Malen tar utgangspunkt i `folkemengde` (CSS, verktøy, stablede stolper, combobox-søket). Siden er én fil på 821 kB, og to bygg gir identisk fil. Testet i Chromium i 1280 og 390 px uten feil i konsollen og uten horisontal rulling.

## 1. Hva som er bygget

| Del | Svarer på | Innhold |
|---|---|---|
| Hode | – | Ingress generert fra tallene, søk etter landbakgrunn (navn og 69 synonymer, for eksempel «polsk» og «Burma»), «Se alle land» gruppert etter verdensdel, «Vis alle landbakgrunner» og seks eksempler, også ett uten treff (Atlantis) |
| Kort for valgt land | 3 | Verdensdel, landkode, antall innvandrere og norskfødte, rangering blant 215 landbakgrunner og tallet for 2004. Egen tekst for land uten bosatte i 2026 (for eksempel Serbia og Montenegro), varsel om små tall under 100, og hvilket søkeord som ga treffet |
| Lesehjelpen | H1, H2, H5, H7 | Fødested, ikke pass. To grupper, ikke én. Hvor mange som bor her, ikke hvor mange som kom. Registrert bosatt. Punkt 2 og 3 er generert fra tallene. Konseptgrafikken ligger i «Slik lages tallene» |
| Toppgrafikk (variant B) | 2 | Stort avrundet tall, setning valgt etter endringen siste år mot tidligere år, fire nøkkeltall. Bryter **Antall** (linjer for innvandrere og norskfødte, prikket før 1986) og **Andel av befolkningen** (stablet areal med øvrig befolkning til 100 prosent). Brudd 2016 markert. For valgt land: tall fra 2004 |
| Hvem regnes som innvandrer? | 1 | Venstre: SSBs seks kategorier 2026 (05182), de to i statistikken uthevet. Høyre: tabell 12548 med bryter mellom **Seks grupper** (eget fødested × antall utenlandsfødte foreldre) og **Alle 30 kombinasjoner** (rutenett 6 × 5 med fargeklasser og tall i hver rute). Valgt gruppe eller rute viser utviklingen 2004–2026 |
| Hvorfor endrer antallet seg? | 2 | Befolkningsregnskap 2016–2025 som stablede stolper fra null, med endringen gjennom året som strek. Bryter mellom innvandrere og norskfødte. For valgt land brukes 10518 (samlet). Finnes ikke landet der, vises en liste over de 24 landene med lenker |
| Hvor kommer de fra, og når kom de? | 3 | De 15 største landbakgrunnene delt i innvandrere og norskfødte, valgt land lagt til nederst hvis det ikke er blant dem. Radene kan velges med mus og tastatur. Botid for valgt land som histogram 0–39 år og 40+ |
| Hvor bor de? | 4 | De 15 kommunene med høyest andel eller flest, med brytere for gruppe (innvandrere, norskfødte, begge) og mål (andel, antall). Grå strek for hele landet. Varsel når toppkommunen har under 2 000 innbyggere. Prikkdiagram over alle 357 kommuner med median, landet og Oslo |
| Bunntekst | – | Om tallene, egne beregninger, kilder og hentedato |

Alle figurer har «Vis tallene» og kildelinje med tabellnummer og oppdateringsdato fra json-stat-svaret. Valgt land ligger i adressen (`#land=131`).

## 2. Hvordan hull i data vises

- **1970–1986 i 05182**: bare tre årstall. Prikket linje i antall, skravert felt i andel, og forklaring under figuren.
- **Brudd 2016**: stiplet loddrett strek merket «Brudd 2016» i toppgrafikken og i utviklingen for tre generasjoner.
- **Regnskapet før 2016**: vises ikke, fordi det ikke går opp (kildekartet H7). Står i notatet under figuren.
- **Ukraina og Syria i 10518 før 2021**: skravert som «mangler data» i regnskapet, også i tabellen.
- **Land uten regnskap**: ingen figur, men en liste over landene som har det.
- **Land uten bosatte i 2026**: kortet sier det, toppgrafikken viser serien til den faller til null, botid og kommune viser egen tekst i stedet for tom figur.
- **Land med bare norskfødte**: botid sier at det ikke finnes innvandrere å vise.

## 3. Kontroller

`lag_data.py` stopper bygget med «Kontroll feilet: …». Negativ test: én verdi i `tre_generasjoner.json` ble økt med 10, og bygget stoppet med «12548 2021: de 30 gruppene summerer til 5391379, ikke 5391369». Filen ble satt tilbake fra kopi.

| Kontroll | Toleranse | Største faktiske avvik |
|---|---|---|
| 30 grupper i 12548 = i alt = 05803, alle år | 0 | 0 |
| 12548 kode 124 og 024 = 05182, alle år | 0 | 0 |
| 05182: øvrig befolkning er positiv, alle år | – | – |
| 10516: utgang − inngang = tilvekst, og inngang/utgang = 05182, 2016–2025 | 0 | 0 |
| 10516: restposten i regnskapet | 1 000 | 849 (norskfødte 2017) |
| 13880: sum av land = landet | 5 | 2 |
| 10598: botid summert = innvandrere i 13880 | 15 | 11 |
| 09817: sum av land = «Alle land» per kommune | 5 | 3 |
| 09817: kommunene = landet 2026 | 2 | 1 |
| 09817: publisert andel = antall / 07459 | 0,011 prosentpoeng | 0 |
| Synonymer peker på land som finnes, alle land har verdensdel | 0 | 0 |

## 4. Nye valg til kvalitetssikring

Nummerert videre fra K1–K8 og T1–T9 i `02-kvalitetssikring.md`.

| # | Valg eller påstand | Grunnlag | Må sjekkes |
|---|---|---|---|
| B1 | Andelsvisningen går til 100 prosent bare for alle land. For valgt land viser den andelen av hele befolkningen med aksen tilpasset, fordi et land ville blitt usynlig mot 100 prosent | Eget valg, avvik fra spesifikasjonen i steg 2 | Thomas |
| B2 | «Økningen i 2025 var den laveste siden 2021»: regel som sammenligner endringen siste år med alle tidligere sammenhengende år | Samme regel som folkemengde | Fag: ordbruk |
| B3 | Bruddet i 2016 forklares med «kan skyldes en endring i registeret» | [T], kildekartet H2 | Fag |
| B4 | De seks gruppene i 12548 vises ved siden av SSBs seks kategorier, med differansen (35 422) i teksten | Valg av Thomas 26.10.2026 | Fag: hvorfor de avviker |
| B5 | Fargeklasser i rutenettet: under 100, 100–999, 1 000–9 999, 10 000–99 999, 100 000+, trinn 1, 2, 3, 5 og 6 i grønn 7 for å få 4,5:1 på teksten | Eget valg | – |
| B6 | «Andre endringer» i regnskapet er egen beregning. 10516 oppgir 1 fødsel blant innvandrere i 2025, og den vises | Kildekartet H4 | Fag |
| B7 | For enkeltland viser regnskapet innvandrere og norskfødte samlet (10518) | Tabellens innhold | – |
| B8 | Botid: «halvparten har bodd her i X år eller kortere» regnet fra hele år | Egen beregning | Fag |
| B9 | Kommuneandel for valgt land er egen beregning med folketall fra 07459. Avrundede småceller (3) kan gi små falske andeler | Egen beregning | Fag |
| B10 | Varsel om små tall når toppkommunen har under 2 000 innbyggere, med mottak som eksempel på årsak | Om statistikken 2021 | Fag |
| B11 | Synonymer i søket. «Korea» peker på Sør-Korea og er merket usikker. Folkegrupper og land som ikke finnes lenger, er bevisst ikke med | Eget valg | – |

## 5. Kjente svakheter

- Kommuneutviklingen over tid er ikke bygget. 09817 har bare harmoniserte tall for dagens kommuner fra 2024 for 115 kommuner (kildekartet H8). `kommune_tid` er hentet og brukt i kontrollen, men ikke vist.
- Bydeler i Oslo er ikke med.
- Prikkdiagrammet krymper prikkene når mange kommuner har nesten lik andel. For land med svært små andeler blir kolonnene tette.
- «Om statistikken» i gjeldende versjon er fortsatt ikke lest (innsiktsnotatet, avsnitt 8).

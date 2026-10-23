Steg 3 i formidlingsprototype for navn · versjon 1.0 · 23.10.2026 · Status: godkjent av Thomas

# Kildekart: navn

Bygger på spørsmålene i `01-innsikt.md` og valget i steg 2: toppgrafikk C (skrivemåtene, topp 5) med veksler mellom gutter og jenter, og *mitt navn* som gjennomgående valg.

**Viktig for resten av arbeidet:** `data.ssb.no` var tilgjengelig i denne økten. Rådataene er derfor hentet direkte fra PxWebApi v2 med `scripts/hent_data.py`, ikke rekonstruert gjennom SSB-tilkoblingen.

## Spørsmål, tabell og seksjon

| Spørsmål | Datasett | Tabell | Seksjon i prototypen |
|---|---|---|---|
| 2. Topplisten 2025 med skrivemåter | `fodte` + `synonymer.json` | 10467 + SSB-artiklene | Toppgrafikk C, veksler jenter/gutter |
| 1. Hvordan har ditt navn utviklet seg? | `fodte` | 10467 | *Mitt navn*: navnebølgen (tidligere variant A) |
| 4. Populært eller vanlig | `fodte`, `personer` | 10467, 10501 | *Mitt navn*: nyfødte mot personer (tidligere variant B) |
| 3. Er toppnavnene mindre dominerende? | `fodte` | 10467 | Egen seksjon: toppnavnets og topp 10s andel over tid |
| 5. Etternavn | `etternavn` | 12891 | Kort seksjon, kan vente |

Ingen arkiverte tabeller ble funnet for fornavn. Fylkes- og kommunelistene finnes bare som tabeller på ssb.no og er ikke med.

## Strukturen, talt fra dataene

**10467 Fødte etter navn.** 1 974 navnekoder: 1 042 jentenavn (prefiks `1`) og 932 guttenavn (prefiks `2`). Fem navn finnes for begge kjønn: Isa, Kim, Marian, Nikola, Thanh. Hver skrivemåte har egen kode.

| Når navnet første gang har andel over 0 | Antall navn |
|---|---|
| 1880 | 611 |
| 1881–1944 | 1 074 |
| 1945–1999 | 190 |
| 2000–2025 | 99 |

I 2025 har 1 054 navn et tall, og 920 har «.».

**Manglende verdier i 10467.**

| År | Antall (Personer) | Andel (prosent) |
|---|---|---|
| 1880 | 1 865 «..», 109 «.» | 611 over 0, 1 254 lik 0, 109 «.» |
| 1945 | 712 med tall, 1 185 «.», 77 «..» | 789 med tall, 1 185 «.» |
| 2025 | 1 054 med tall, 920 «.» | 1 054 med tall, 920 «.» |

Antall finnes ikke før 1945. Andelen finnes fra 1880.

**Tabellnotene i 10467 svarer på tre spørsmål fra steg 1 og 2:**
- Navnelisten omfatter fornavn brukt av minst 200 personer året før. Det er terskelen for statistikkbanken (H6, K-4).
- Tallene viser fødte etter **fødselsår før 2021** og etter **navngivningsår fra og med 2021**. Det er et brudd i serien som ikke var kjent i steg 1 (ny hypotese, se hull 2).
- Tall under 4 personer oppgis ikke.

**10501 Personer etter navn.** 2 152 koder, 1 134 jente og 1 018 gutte. Alle 1 974 navnene i 10467 finnes her, og 178 navn finnes bare i 10501. Referansetid 31.12. Bare navn med flere enn 200 bærere har tall. Navn med bindestrek er regnet sammen med navnet før bindestreken i 2021–2024. Bare personer med norsk personnummer er med.

**12891 Etternavn.** 3 706 koder, 2018–2025, per 31.12. Bare navn med 200 eller flere bærere.

## Hva strukturen betyr for interaksjonen

- **Søket i *mitt navn*** trenger 2 152 navn. 178 av dem har bare personer, ikke fødte. Søket må si fra når et navn ikke har noen kurve.
- **Navn som ikke finnes** (under 200 bærere) må gi et svar, ikke et tomt resultat: «Navnet har færre enn 200 bærere og er ikke i statistikkbanken. Prøv navnesøket på ssb.no.»
- **Kjønn i søket.** Fem navn finnes for begge kjønn. Søket må vise begge.
- **Skrivemåter i søket.** Den som skriver «Lukas», får Lukas, ikke Lucas. Søket kan foreslå beslektede skrivemåter for topp 5 fra `synonymer.json`, men ikke for andre navn, siden grupperingen ikke er publisert.
- **Vekslerens fasit** er publisert total, ikke summen i statistikkbanken (se kontroll 2).

## Kontroller

| # | Kontroll | Resultat |
|---|---|---|
| 1 | Topp 10 for gutter og jenter summert fra publiserte totaler | Gutter 3 833, jenter 3 494. Stemmer med artiklene |
| 2 | Topp 5 per kjønn gjenskapt ved å summere skrivemåtekodene i 10467 | 9 av 10 stemmer. **Nora:** Nora 357 + Norah 6 = 363, publisert 366. Summert fra statistikkbanken havner Sofie (364) foran Nora |
| 3 | Andel av topp 10 gjenskapt fra antall og publisert andel | Gutter 13,7 prosent (publisert 13,7). Jenter 13,1 prosent (publisert 13,2). Nevneren er regnet fra Emmas avrundede andel, så avviket kan være avrunding |
| 4 | Antall og andel henger sammen | Noah 460 og 1,647 prosent gir rundt 27 930 navngitte gutter. Emma 386 og 1,450 prosent gir rundt 26 620 jenter |
| 5 | «Per 1 000» på statistikksiden | Noah: 477 / 27 930 × 1 000 = 17. Stemmer med siden. Per 1 000 er altså per 1 000 navngitte av samme kjønn (bekrefter tolkningen i steg 1) |
| 6 | Toppnavnets andel over tid, eksakt skrivemåte | Jenter: 9,0 prosent (1881) → 4,7 (1964) → 1,45 (2025). Gutter: 5,5 → 3,2 → 1,65. Topp 10: rundt 27–30 prosent i 1881, 12,4–12,5 prosent i 2025 |
| 7 | Vanligste fornavn blant personer 2025 | Anne 55 625, Jan 43 472, Bjørn 33 777, Per 32 539, Ole 29 629 |

Kontroll 6 er regnet fra eksakte skrivemåter. SSBs egne topp 10-andeler bruker sammenslåtte skrivemåter og blir litt høyere.

## Metode for toppgrafikken

For hvert av de fem navnene per kjønn:
- **Vanligste skrivemåte:** antall fra 10467.
- **Andre skrivemåter:** publisert total minus vanligste skrivemåte. For Nora er 6 av de 9 Norah, og 3 er ukjent.
- **Total:** publisert total fra artiklene.

Når neste års tall kommer, må `synonymer.json` oppdateres for hånd fra de nye artiklene. Det kan ikke automatiseres så lenge grupperingen ikke er publisert som data.

## Datamengde

| Datasett | Celler | Rå json-stat2 | Innbakt kompakt (rå / gzip) |
|---|---|---|---|
| `fodte`, andel 1880– og antall 1945– | 576 408 | 6,3 MB | 2,0 / 0,39 MB |
| `fodte`, bare andel 1880– | | | 1,4 / 0,26 MB |
| `fodte`, andel og antall fra 1945 | | | 1,5 / 0,29 MB |
| `personer` | 27 976 | 0,24 MB | 0,13 / 0,05 MB |
| `etternavn` | 29 648 | 0,27 MB | 0,12 / 0,04 MB |

Alle spørringene er under grensen på 800 000 celler. GitHub Pages leverer gzip, så det brukeren laster ned er under 0,5 MB i alle alternativene.

**Valgt strategi (23.10.2026):** alternativ 1, andel fra 1880 og antall fra 1945 for alle navn, valgt av Thomas for å vise hele bølgen.

## Hull og hindre

1. **Nora-avviket** (kontroll 2). Tre jenter er med i den publiserte totalen uten å finnes i statistikkbanken. Spør fag hvilken skrivemåte det er.
2. **Brudd i 2021.** Fødselsår før 2021, navngivningsår etter. Må markeres i kurven i *mitt navn* og forklares i lesehjelpen. Bør bli hypotese H11: «Tallene for 2021 og senere kan sammenlignes direkte med tallene før.»
3. **Tegnet «.» har to betydninger** i notene til 10467: «færre enn 4 personer» og «kategorien var ikke i bruk». Prototypen kan ikke skille dem og bør vise «færre enn 4 eller ikke i bruk».
4. **Andel 0,000** kan være avrundet ned fra et lite tall. Vises som «under 0,001 prosent», ikke null.
5. **Bindestreknavn i 10501** er regnet sammen med navnet før bindestreken i 2021–2024. Det kan blåse opp tall som Anne og Ole i de årene. Spør fag om 2025 er tilbake på gammel praksis, og om det gir brudd.
6. **Grupperingen av skrivemåter** er hentet fra artiklene, ikke fra en datakilde. Gjelder bare topp 50.
7. **Metadata merker bestand som «Flow»** i 10501 og 12891. Kosmetisk, men kan villede maskinlesere.
8. **Fristen på seks måneder** (K-1) er ikke bekreftet, men noten om navngivningsår fra 2021 gjør den mindre viktig.

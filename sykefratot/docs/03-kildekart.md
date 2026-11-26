Steg 3 i formidlingsprototype for sykefratot · versjon 0.1 · 26.11.2026 · Status: utkast

# Kildekart: Sykefravær (sykefratot)

**Merking.** `[K1]`–`[K15]` som i `01-innsikt.md`. `[T]`: vår tolkning eller vårt valg.

Rådataene er hentet direkte fra data.ssb.no (PxWebApi v2, json-stat2) med `scripts/hent_data.py` 26.11.2026, samme dag som 3. kvartal 2026 ble publisert. API-et svarte fra arbeidsområdet, så SSB-tilkoblingen trengte ikke brukes. Rådataene i `data/raw/` er uendret og har de ekte statussymbolene. Ingenting er rekonstruert.

## Valg fra Thomas, 26.11.2026

| Valg | Beslutning |
|---|---|
| Toppgrafikk | Variant A (nivå og trend). Variant C blir seksjon lenger ned |
| Interaktive funksjoner | Kjønnsvelger, SSB/Nav-bryter, yrkesoppslag, Min kommune |
| Yrke | Hele serien fra 2015K1, alle tre kjønnsvalg |
| Kommune | Fra 2024K1 (gjeldende kommuneinndeling), begge kjønn |
| Næring | Utsatt til SN2025-tabellene kommer med 1. kvartal 2027 (godkjent i steg 1) |

## 1. Spørsmål, datasett og seksjon

| Spørsmål (01-innsikt) | Datasett | Tabell | Seksjon i prototypen |
|---|---|---|---|
| 1 Nivå og trend | `hoved` | 12439 | Toppgrafikk A, kjønnsvelger |
| Lesehjelp: SSB og Nav | `hoved` | 12439 | SSB/Nav-bryter |
| 2 Hva 6,7 prosent betyr | `hoved`, `personer` | 12439, 12446 | Konseptgrafikken, lesehjelp om personer og dagsverk |
| 3 Korte og lange fravær | `varighet` | 12946 | Seksjon C, kjønnsvelger |
| 4 Hvem har høyest fravær | `hoved`, `yrke`, `yrke_endring`, `kommune` | 12439, 12452, 12451 | Kjønn, yrkesoppslag, Min kommune |

**Tabeller som ikke brukes:**
- **Næring** (12440, 12441, 12442, 12450, 13935). SN2007-tabellene avsluttes etter 4. kvartal 2026 `[K3]`, og egenmeldt på detaljnivå i 12440 stemmer ikke med hovednæringene (01-innsikt, fagspørsmål 2).
- **Fylke** (12443, 14341, 14814). Ikke valgt. Min kommune dekker det regionale.
- **Alder og kommune** (12448). For stor (6,8 millioner celler), og ikke valgt.
- **AKU** (04547). En annen statistikk. Brukes eventuelt bare som henvisning i lesehjelpen.

## 2. Strukturen som former prototypen

Alt er talt fra `data/raw/`.

**Hovedtabellen (12439).** 3 kjønn × 3 typer × 9 statistikkvariabler × 106 kvartaler (2000K2–2026K3).
- Dagsverk mangler før 2015: 1 062 celler med «..» i de to dagsverksvariablene.
- Endringsratene har «.» i 180 celler: de første kvartalene i serien, og bruddet i 2015. Ujustert endring fra året før mangler for 2015K1–K4, justert endring for 2015K1.
- Kjønnskodene kommer i rekkefølgen 0 Begge kjønn, 2 Kvinner, 1 Menn.

**Varighet (12946).** 8 grupper: i alt, egenmeldt i alt, legemeldt i alt, legemeldt 1–8, 9–16, 17–31, 32 dager til kvartalet minus én, og hele kvartalet. 47 kvartaler fra 2015K1. Ingen statussymboler. Mønsteret i seksjon C er stabilt i 3. kvartal over tid:

| Kvartal | Egenmeldt, andel av tilfellene | Egenmeldt, andel av dagsverkene | 32 dager eller mer, andel av tilfellene | 32 dager eller mer, andel av dagsverkene |
|---|---|---|---|---|
| 2015K3 | 57,9 | 12,4 | 12,3 | 61,7 |
| 2019K3 | 59,8 | 12,7 | 11,9 | 62,2 |
| 2024K3 | 61,7 | 13,6 | 11,4 | 62,0 |
| 2025K3 | 62,6 | 13,8 | 11,5 | 62,4 |
| 2026K3 | 62,7 | 13,7 | 11,6 | 62,7 |
| 2026K1 | 66,8 | 16,8 | 11,1 | 61,8 |
| 2022K1 | 66,1 | 23,5 | 7,5 | 48,4 |

Prosent, begge kjønn, regnet fra antall. 1. kvartal har mer egenmelding, og 2022K1 (omikron) skiller seg kraftig ut. Seksjon C bør derfor la brukeren se andre kvartaler enn det siste, eller si tydelig at bildet gjelder 3. kvartal `[T]`.

**Yrke (12452).** 583 koder i fem nivåer, talt ut fra kodene:

| Nivå | Koder | Merknad |
|---|---|---|
| Alle yrker | 1 | `0-9` |
| 1 siffer | 10 | 8 hovedgrupper, `3_01-03` (høyskole- og militære yrker slått sammen) og `0b` Uoppgitt |
| 2 siffer | 43 | Med `00` Uoppgitt og `01`–`03` militære |
| 3 siffer | 122 | |
| 4 siffer | 407 | Med `0000` Uoppgitt og militære |

- Historikk, begge kjønn: 527 koder har tall i alle 47 kvartaler, 44 i deler av perioden, 12 aldri. På 4-siffernivå har 363 av 399 koder med tall en hel serie.
- 23 yrker på 4-siffernivå er undertrykt («:») i 2026K3 for begge kjønn. I hele nivåserien er 327 celler undertrykt.
- 5 549 celler med «..», mest i kjønnsfordelte serier for yrker der det ene kjønnet mangler.
- **Søket trenger synonymer og ordstart-treff.** Etikettene er gruppenavn i flertall («Sykepleiere», «Grunnskolelærere»). Et vanlig delstreng-søk gir feil treff: «lege» finner «Tannleger», «politi» finner «Politikere». «Lærer» treffer 11 yrker og «ingeniør» 18. Det trengs en `data/synonymer.json`, som i kpi.

**Kommune (12451).** 937 regionkoder i tabellen. 357 kommuner har tall i alle 11 kvartaler fra 2024K1. I tillegg kommer 9999 Uoppgitt kommune med verdien 0 uten statussymbol. Den skal ikke vises.
- Publisert endring fra året før mangler («..») for 115 av dagens kommuner i alle fire kvartaler i 2024, fordi de fikk ny kode i 2024. Fra 2025 er endringen publisert for alle.
- Spredningen er stor i små kommuner. I 2026K3 går den fra 2,7 (Rollag) til 9,1 (Karlsøy). Det finnes ingen publisert usikkerhet.

## 3. Metoder og kontroller

| # | Kontroll | Resultat |
|---|---|---|
| K1 | Egenmeldt + legemeldt = totalt, sesongjustert, alle kvartaler | Største avvik 0,01. Ujustert største avvik 0,1 (én desimal). OK |
| K2 | Menn + kvinner = begge kjønn, sykefraværsdagsverk | Største avvik 100 dagsverk, avrunding. OK |
| K3 | Endring fra forrige kvartal regnet fra publiserte nivåer mot publisert endring | Avvik i 54 av 104 kvartaler, størst 0,2 (2018K3: regnet 0,54, publisert 0,7). **Publiserte endringsrater brukes alltid** |
| K4 | Gjenskape Navs tall for 3. kvartal 2025: legemeldt 4,8 prosent, ned 6,3 prosent fra året før `[K6]` | 12439 gir 4,8 og −6,3. OK. Samme metode gir for 2026K3: legemeldt 4,9, **opp 1,9 prosent** fra året før, mens SSB melder 6,65, ned 0,3 prosent. Det er SSB/Nav-bryterens poeng |
| K5 | Dagsverk i alt i 12946 = dagsverk i 12439 | Likt i 46 av 47 kvartaler. **2024K2 avviker med 6 400 dagsverk** (9 394 200 mot 9 400 600). Se hull 1 |
| K6 | Varighet: egenmeldt + legemeldt = i alt, og summen av varighetsgruppene = legemeldt | Tilfeller går opp, med høyst 1 i avvik mellom kjønn. Dagsverk avviker med høyst 200, avrunding. OK |
| K7 | Andeler regnet fra antall mot publiserte prosentandeler i 12946 | Største avvik 0,1. OK. Vi bruker andeler regnet fra antall, så stolpene summerer til 100 |
| K8 | 2026K3-tallene i grafikkutkastet (steg 2) mot `data/raw/` | Samme tall, samme kilde, samme dag |

## 4. Datamengde og strategi

| Datasett | Celler | Rådata | Innbakt (anslag) |
|---|---|---|---|
| `hoved` | 8 586 | 76 KB | 40 KB |
| `varighet` | 4 512 | 36 KB | 25 KB |
| `personer` | 954 | 16 KB | 4 KB |
| `yrke` | 82 203 | 512 KB | 333 KB med etiketter |
| `yrke_endring` | 1 749 | 48 KB | 8 KB |
| `kommune` | 20 614 | 332 KB | 40 KB (bare 357 kommuner) |
| **Sum** | **118 618** | **1,0 MB** | **ca. 450 KB** |

Alle spørringer ligger godt under API-grensen på 800 000 celler. Seks spørringer, med 2,5 sekunders pause mellom dem.

**Anbefalt strategi `[T]`:** Bak alt inn i `index.html` unntatt yrkesserien, som legges i en egen `data/yrke.json` og lastes når brukeren åpner yrkesoppslaget. Da blir siden rundt 120 KB ved første visning. Valget tas i steg 4.

**Valgt i steg 4 (26.11.2026):** Alt er bakt inn i `index.html`, slik `felles/bygg.py` og de andre prototypene gjør det. Siden ble 959 kB, som er innenfor det de andre prototypene har (0,6–2,7 MB).

## 5. Hull og hindre

1. **Dagsverk i 2024K2 er ulike i 12439 og 12946** (6 400 dagsverk, 0,07 prosent). Den ene tabellen er trolig revidert uten den andre. Spørsmål til fag.
2. **Yrkene kan ikke filtreres på størrelse.** Artikkelen viser «yrker med mer enn 15 000 jobber» `[K2]`, men 12452 har ikke antall jobber. Små yrker kan derfor få store utslag uten at prototypen kan varsle om det. Spørsmål til fag: finnes antall jobber per yrke i en annen tabell?
3. **Kommunetallene har ingen publisert usikkerhet**, og små kommuner svinger mye. Prototypen må vise serien, ikke bare siste tall, og si at små kommuner svinger `[T]`.
4. **Kommune er bosted, ikke arbeidssted, og bare legemeldt** `[K1]`. Det må stå ved oppslaget.
5. **Publisert endring mangler for 115 kommuner i 2024.** Ikke et problem for siste kvartal, men tidslinjen kan ikke vise endring for 2024 der.
6. **9999 Uoppgitt kommune har verdien 0** uten statussymbol. Den filtreres bort.
7. **Seksjon C er sesongavhengig.** Egenmeldt andel av dagsverkene var 16,8 prosent i 2026K1 mot 13,7 i 2026K3, og 23,5 i 2022K1.
8. **Sammenlignbarhet over bruddet i 2015** for den sesongjusterte serien er ikke avklart (01-innsikt, fagspørsmål 4). Det påvirker annoteringen av toppen i 2003 i toppgrafikk A.
9. **Egenmeldte og legemeldte tilfeller** kommer fra ulike kilder (utvalg og register). At de kan stå i samme stolpe, er ikke bekreftet (02-kvalitetssikring, punkt 20).
10. **Navs melding for 3. kvartal 2026 er ikke lest.** Bryteren bygger på Navs metode, som er kontrollert mot 2025K3 (K4). Les Navs melding før publisering og sjekk at Nav faktisk skriver +1,9 prosent.
11. **Repoet var ikke i arbeidsområdet.** `scripts/hent_data.py` er skrevet på nytt etter samme oppskrift, ikke kopiert. Den bruker `valueCodes[...]`, `top(1)` og `from(...)`. Sammenlign med de andre prototypene i steg 4.
12. **Yrkesserien er stor** (333 KB innbakt). Se strategien i avsnitt 4.
13. **Næring mangler i denne versjonen.** Når SN2025-tabellene kommer i mai 2027, må prototypen få en ny næringsseksjon. Uten den kan brukerne savne det SSB selv løfter fram, særlig helse og sosial.

Steg 3 i formidlingsprototype for arbstatus-neet · versjon 0.2 · 10.11.2026 · Status: utkast (utvidet med 14158 og 13347)

# Kildekart: unge utenfor

**Merking:** `[K]` viser til kildelisten i `01-innsikt.md`. `[T]` er vår tolkning.

**Valgt omfang (10.11.2026, Thomas):** alternativ 2. Tabell 12424 for tverrsnittet med alle dimensjoner, og tabell 12427 for forløp, 15–29 år, i alt og etter innvandringskategori. Tabell 13556 brukes bare i kontrollene. Forløp etter kjønn og utdanning fra 12427 (alternativ 3) er valgt bort. Utvidet samme dag, etter gjennomgang av hele emnet arbstatus: 14158 (forløp etter todelt videregående og aldersgruppe) og 13347 (barnevern og foreldrenes utdanning, som egen faktaboks).

**Viktigste endring siden steg 1:** 12427 følger de samme personene fra år til år. Den gir dermed svar på tre spørsmål innsiktsnotatet sa at banken ikke kunne svare på: hvor mange som er nye i NEET, hvor lenge folk er utenfor, og om utenforskapet varer lenger enn før. `01-innsikt.md` er rettet (versjon 0.2).

## 1. Spørsmål, datasett, tabell og seksjon

| Spørsmål | Datasett | Tabell | Seksjon i prototypen |
|---|---|---|---|
| Hva betyr «utenfor»? | `tverrsnitt` | 12424 | Lesehjelp (konseptgrafikken) |
| Er utenforskapet tyngre enn før? | `tverrsnitt` | 12424 | Toppgrafikk B |
| Hvor mange er nye i NEET? | `forlop` | 12427 | Ny seksjon: Strømmen inn og ut |
| Hvor lenge er folk utenfor? Er det lenger enn før? | `forlop` | 12427 | Ny seksjon: Hvem er fortsatt utenfor etter ett, tre og fem år? |
| Innvandrere og befolkningen ellers | `tverrsnitt` + `forlop` | 12424, 12427 | Seksjon C, utvidet med forløp og «ut av befolkningen» |
| Kjønn, alder og utdanning | `tverrsnitt` | 12424 | Gruppevelger |
| Hvem er i størst fare? | `tverrsnitt` + `forlop` | 12424, 12427 | Seksjon D, med varigheten for AAP/uføretrygd |
| Hvor bør tiltakene settes inn? Varighet etter utdanning og alder | `forlop_utdanning` | 14158 | Seksjon D, forløpsdel |
| Barnevern og foreldrenes utdanning som risikomarkør | `barnevern` | 13347 | Faktaboks under D, tydelig adskilt fra NEET |
| Kontroll av NEET-tallene | `kontroll_neet` | 13556 | Ikke i prototypen |

**Hele emnet arbstatus er gått gjennom** (15 aktive tabeller, 10.11.2026). Vurdert og ikke tatt inn:

| Tabell | Hvorfor ikke |
|---|---|
| 12438 Landbakgrunn | Har ikke aldersgruppen 15–29 år (bare 15+ og 30–61) |
| 13678 Todelt videregående, fylke | Tverrsnittet på landsnivå finnes allerede i startåret i 14158 |
| 13556, 13563 Kommune | Region er holdt utenfor prototypen |
| 12423, 12425, 12426 | Andre aldersgrupper |
| 13679 Fagfelt | Fagfelt gir for små grupper for unge; kan vurderes senere |
| 12580, 12836, 12837, 12838 | Om sysselsatte (arbeidstid, lønn, barn) |
| 13346, 13348, 13349 Barnevern | Fylkesfordelt (13346, 13348) og 7–10 år etter grunnskolen (13348, 13349); 13347 dekker landsnivået seks år etter. 13349 kan bli aktuell hvis faktaboksen skal vise utvikling etter flere år |

Ingen arkiverte tabeller dekker spørsmålene.

## 2. Struktur som former prototypen

**NEET er ikke en kode i 12424 eller 12427.** Den må bygges av tre statuser:

| Tabell | NEET = |
|---|---|
| 12424 | A.09 registrerte ledige + U.04-U.05 AAP/uføretrygd + U.90B andre, ikke på tiltak (U.90B = U.90B.00 andre ordninger + UX.00 ukjent status) |
| 12427, startåret | A.09 + U.04-U.05 + U.90A «Andre» |
| 12427, tidsserien | A.09 + U.04-U.05 + U.90E «Andre». UT.01 «Ut av populasjonen» (utvandret eller død) er egen kategori |

**12424, talt:** 3 kjønn × 4 aldersgrupper × 5 utdanningsnivåer × 3 innvandringskategorier × 11 statuser (av 24) × 18 år = 35 640 celler. 48 fineste grupper (kjønn × tre aldersgrupper × fire utdanningsnivåer × to innvandringskategorier). I 2025 har 15 av dem under 1 000 bosatte og 4 under 100 NEET. Gruppevelgeren bør vise et varsel ved små grupper.

**12427, talt:** 18 startår × 3 innvandringskategorier × 8 statuser i startåret × 9 statuser i tidsserien × 18 år = 69 984 celler. 33 048 av dem gjelder år før startåret og er 0. Hvert startår følges til 2025, så 2008-kullet har 17 år, mens 2024-kullet har ett.

**Status i tidsserien er et øyeblikksbilde i november.** «Fortsatt NEET etter fem år» betyr NEET i november det femte året, ikke sammenhengende utenfor.

**14158, talt:** 10 startår (2016–2025) × 8 × 9 statuser × 9 utdanningsnivåer × 3 aldersgrupper × 10 år = 194 400 celler. Utdanningsnivåene er hierarkiske: alle = grunnskole + videregående + fagskole + høyere + uoppgitt, og videregående = studieforberedende + yrkesfag + uoppgitt. Ingen 15–29 i alt; de tre aldersgruppene summerer til 12427. For 15–19 år er nesten alle registrert med grunnskole som høyeste utdanning, fordi de går på skole. Utdanningssammenligningen gir derfor bare mening fra 20 år.

**13347, talt:** 8 statuser × 3 kjønn × 6 nivåer for foreldrenes utdanning × 5 barnevernsgrupper × 2 statistikkvariabler × 7 år = 10 080 celler. Populasjonen er elever som avsluttet grunnskolen seks år før, om lag 22 år gamle, og ikke 15–29-åringer. Statusene er ikke NEET: «helserelaterte ytelser» er nærmest AAP/uføretrygd, «annet» er nærmest ukjent status. Tallene er støylagt. **Brudd:** Fra 2023 er død/utvandret slått sammen med «annet».

**Manglende verdier:** Ingen statussymboler i 12424, 12427, 14158 og 13556. 13347 har 120 celler med «..» (tallgrunnlag mangler), alle små: mest død/utvandret og annet i undergrupper. De skal vises som manglende, aldri som 0. Avrunding (1 og 2 blir 0 eller 3) gir små avvik mellom tabeller og år, se kontrollene.

## 3. Metodene som er testet

### Tilgang: hvor mange blir nye i NEET?

Metode: personer 15–29 år som var i arbeid, utdanning eller tiltak i november ett år, og som var NEET i november året etter. Tilsvarende for strømmen ut. Fra `forlop`.

| Til år | Inn fra arbeid, utdanning, tiltak | Ut til arbeid, utdanning, tiltak | Ut av befolkningen fra NEET | Netto endring i NEET (12424) |
|---|---|---|---|---|
| 2009 | 52 818 | 38 585 | 4 273 | +11 202 |
| 2015 | 67 120 | 49 769 | 5 516 | +11 301 |
| 2020 | 56 666 | 41 785 | 4 025 | +3 855 |
| 2021 | 41 777 | 49 030 | 4 916 | −15 835 |
| 2025 | 47 232 | 38 900 | 4 430 | +2 343 |

Strømmene er mange ganger større enn netto endring. Netto fra 12424 inkluderer også nye 15-åringer, innvandring og dem som fyller 30, så kolonnene summerer ikke. `[T]` Tilgangen er en nedre grense: den som går inn og ut i løpet av året, synes ikke.

Etter innvandringskategori, inn i 2025: 33 409 i befolkningen ekskl. innvandrere, 13 823 innvandrere.

### Varighet: hvor mange er fortsatt NEET?

Metode: alle som var NEET i november i startåret. Andel som var NEET, i arbeid, utdanning eller tiltak, eller ute av befolkningen 1, 3, 5 og 10 år senere. Nevner: alle NEET i startåret.

| Startår | NEET i startåret | Fortsatt NEET etter 1 år | etter 3 år | etter 5 år | etter 10 år |
|---|---|---|---|---|---|
| 2008 | 85 502 | 49,9 | 37,5 | 35,0 | 31,8 |
| 2010 | 103 778 | 47,6 | 36,7 | 34,2 | 32,1 |
| 2012 | 106 720 | 51,2 | 39,1 | 34,3 | 30,7 |
| 2015 | 124 814 | 49,5 | 37,0 | 35,8 | 30,9 |
| 2018 | 111 105 | 54,5 | 41,3 | 36,6 | – |
| 2020 | 112 420 | 52,0 | 40,1 | 38,7 | – |
| 2022 | 97 162 | 55,7 | 47,0 | – | – |
| 2024 | 102 974 | 57,9 | – | – | – |

Prosent av NEET i startåret. `[T]` Utenforskapet varer lenger enn før: Andelen som fortsatt er NEET året etter, har økt fra 48–50 prosent i 2008–2015 til 58 prosent i 2024-kullet. Fem år etter har den økt fra 34–35 til 39 prosent.

**Innvandrere og befolkningen ellers, fem år etter (2020-kullet):**

| | Fortsatt NEET | I arbeid, utdanning, tiltak | Ute av befolkningen |
|---|---|---|---|
| Befolkningen ekskl. innvandrere | 42,3 | 54,3 | 3,4 |
| Innvandrere | 31,3 | 39,8 | 28,9 |

`[T]` Innvandrere ser ut til å komme raskere ut av NEET, men nesten tre av ti går ut av befolkningen. Lavere varighet blant innvandrere er derfor ikke det samme som bedre utfall. I befolkningen ekskl. innvandrere har femårsvarigheten økt fra 36,9 prosent (2010) til 42,3 prosent (2020).

### Varighet på AAP og uføretrygd

Andel av unge på AAP/uføretrygd i startåret som fortsatt var det fem år senere: 2008: 62,5 · 2010: 56,8 · 2015: 64,8 · 2018: 70,0 · 2020: 70,0 prosent. Dippen i 2010 kan henge sammen med AAP-reformen samme år (H10).

### Varighet etter utdanning og alder (14158)

Andel NEET blant alle i gruppen, og andel av dem som fortsatt var NEET ett og fem år senere. Utdanning og alder i startåret.

| Alder, utdanning | NEET-andel 2020 | Fortsatt NEET etter 1 år, 2016 → 2024 | etter 5 år, 2016 → 2020 |
|---|---|---|---|
| 20–24, grunnskole | 30,7 | 57,4 → 66,4 | 44,1 → 48,7 |
| 20–24, studieforberedende | 6,5 | 32,9 → 34,5 | 21,5 → 22,3 |
| 20–24, yrkesfag | 7,4 | 28,7 → 34,2 | 16,3 → 19,1 |
| 20–24, universitet/høgskole | 5,2 | 40,1 → 44,4 | 17,1 → 23,6 |
| 25–29, grunnskole | 34,1 | 65,1 → 77,4 | 51,1 → 55,2 |
| 25–29, studieforberedende | 16,8 | 52,3 → 65,5 | 37,4 → 42,1 |
| 25–29, yrkesfag | 8,2 | 43,1 → 55,3 | 28,0 → 32,1 |
| 25–29, universitet/høgskole | 8,8 | 45,0 → 53,5 | 18,6 → 20,9 |

Prosent. `[T]` To funn skiller seg ut. Varigheten har økt i alle grupper, mest for 25–29-åringer med grunnskole, der tre av fire som var NEET i 2024, fortsatt var det i 2025. Og 25–29-åringer med studieforberedende uten høyere utdanning er dobbelt så ofte NEET som dem med yrkesfag, og blir lenger.

### Barnevern og foreldrenes utdanning (13347)

Status seks år etter grunnskolen, prosent (publiserte andeler):

| 2024 | Elever | Høyere utdanning | Sysselsatt | Helserelaterte ytelser | Andre ytelser | Annet |
|---|---|---|---|---|---|---|
| Uten barnevernstiltak | 53 320 | 51,9 | 32,6 | 3,0 | 1,1 | 4,5 |
| Med hjelpetiltak | 8 117 | 23,2 | 43,2 | 11,4 | 4,8 | 6,7 |
| Med omsorgstiltak | 1 128 | 18,6 | 36,6 | 22,9 | 4,8 | 6,3 |

Andelen på helserelaterte ytelser blant dem med omsorgstiltak har vært stabil: 21,9 prosent i 2018 og 22,9 i 2024. Innenfor omsorgsgruppen betyr foreldrenes utdanning lite: 23,8 prosent med foreldre med grunnskole, 19,9 prosent med foreldre med kortere høyere utdanning. Gruppene er små, ned mot 26 personer. `[T]` Barnevernsbakgrunn er en sterkere markør enn foreldrenes utdanning.

## 4. Kontroller (kjørt 10.11.2026; nå i `scripts/lag_data.py`, som stopper bygget)

| Kontroll | Celler | Avvik | Maks | Resultat |
|---|---|---|---|---|
| 12424: TOT, U.04-U.05 og U.90B = sum av undernivåene | 3 × 3 240 | 0 | 0 | OK |
| 12424: kjønn, alder, utdanning, innvandring summerer | 39 798 | 0 | 0 | OK |
| NEET-antall fra 12424 = NEET i 13556 (kjønn × alder × år) | 216 | 174 | 6 personer | OK, avrunding |
| NEET-andel regnet fra 12424 = publisert andel i 13556 | 216 | 1 | 0,1 | OK (kvinner 2023: 9,95 blir 9,9) |
| 12427: år før startåret er 0 | 33 048 | 0 | 0 | OK |
| 12427: startåret = 12424 samme år | 378 | 248 | 14 personer | OK, avrunding |
| 12427: kullet er like stort hvert år | 4 104 | 2 832 | 47 personer | OK, avrunding (av 955 000) |
| 12427: status i tidsserien summerer til i alt | 4 104 | 0 | 0 | OK |
| 12427: innvandring summerer | 12 312 | 0 | 0 | OK |
| 14158: år før startåret er 0 | 87 480 | 0 | 0 | OK |
| 14158: status i tidsserien summerer til i alt | 11 880 | 0 | 0 | OK |
| 14158: utdanningshierarkiet summerer (alle nivåer, todelt vgs) | 2 × 1 320 | 0 | 0 | OK |
| 14158: tre aldersgrupper = 12427 15–29 år | 3 960 | 2 540 | 44 personer | OK, avrunding |
| 13347: statusene summerer til alle (celler uten «..») | 595 | 0 | 0 | OK |
| 13347: barnevernsgruppene summerer | 1 956 | 0 | 0 | OK |
| 13347: publisert prosent = antall / alle | 4 980 | 6 | 0,1 | OK |

Kontrollene ligger nå i `scripts/lag_data.py` og stopper bygget i CI hvis en grense brytes. Grafikken fra steg 2 ble laget på nytt fra de nye rådataene og er identisk.

## 5. Datamengde og strategi

| Datasett | Celler | Rå json | Innbakt (anslag) |
|---|---|---|---|
| `tverrsnitt` (12424) | 35 640 | 165 kB | om lag 150 kB |
| `forlop` (12427) | 69 984 | 231 kB | om lag 60 kB etter forhåndsberegning |
| `forlop_utdanning` (14158) | 194 400 | 522 kB | om lag 30 kB etter forhåndsberegning |
| `barnevern` (13347) | 10 080 | 48 kB | om lag 5 kB (landsnivå, begge kjønn) |
| `kontroll_neet` (13556) | 864 | 12 kB | 0, bare kontroll |

Strategi, valgt 10.11.2026: rådataene hentes uendret med `scripts/hent_data.py` direkte fra data.ssb.no (API-et svarte i økten, så SSB-tilkoblingen trengs ikke). I steg 4 forhåndsberegnes forløpene til NEET-aggregatene (tilgang, varighet, ut av befolkningen) før innbaking, i stedet for å bake inn hele matrisene. Samlet om lag 0,25 MB.

## 6. Hull og hindre

1. **«Fortsatt NEET» er ikke sammenhengende NEET.** Status måles én gang i året. Må stå ved hver varighetsfigur.
2. **Tilgangen er en nedre grense** og gjelder bare dem som var 15–29 år og bosatt året før. Nye 15-åringer og nyankomne innvandrere er ikke med.
3. **U.90A og U.90E** («Andre» i startåret og i tidsserien) er like i startåret, men forskjellen mellom dem er ikke dokumentert i metadataene. Spør fag.
4. **Avrundingsstøy i små grupper.** Kullene svinger med opptil 47 personer fra år til år. I små grupper gir det merkbare utslag: 751 innvandrere på AAP/uføretrygd i 2008 svinger med opptil 2,7 prosent. Vis ikke forløp for grupper under om lag 1 000.
5. **AAP-reformen 2010 og uførereformen 2015 (H10)** står fortsatt åpne. Varigheten på AAP/uføretrygd faller i 2010 og stiger igjen.
6. **Korona:** Tilgangen var høy i 2020 og lav i 2021. Dette bør markeres i tidsseriene.
7. **2025 er foreløpige tall.** Endelige tall kommer 19.01.2027, og da kan siste punkt i alle serier endres.
8. **Steg 1 må rettes.** H1 og «det viktigste først» sa at nye og varighet ikke kan besvares fra banken. Rettet i 01 versjon 0.2. Påstandsprøven fra steg 2 må skrives om i steg 4.
9. **Forløp etter kjønn og utdanning** finnes i 12427, men er valgt bort (alternativ 3). Gruppevelgeren gjelder derfor bare tverrsnittet.
10. **Grafikkhjelperne** ligger i `scripts/grafikk.py`. Repoet har ingen felles grafikkmodul.
11. **13347 er en annen populasjon og andre statuser.** Faktaboksen må si det i første setning og ikke stå i samme diagram som NEET-tallene.
12. **Brudd i 13347 fra 2023:** Død/utvandret er slått sammen med «annet». Vis bare 2024, eller marker bruddet.
13. **Små celler i 13347:** Omsorgstiltak etter foreldrenes utdanning går ned mot 26 elever. Den fordelingen bør ikke vises.
14. **14158 for 15–19 år:** Utdanningsnivået er nesten alltid grunnskole fordi de går på skole. Utdanningssammenligningen vises fra 20 år.
15. **Tolkning av studieforberedende uten høyere utdanning (25–29 år):** Gruppen kan blande personer som har avbrutt høyere utdanning med personer som aldri begynte. Spør fag.

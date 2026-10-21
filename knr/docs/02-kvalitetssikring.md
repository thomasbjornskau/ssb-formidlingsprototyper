Steg 2 i formidlingsprototype for knr · versjon 1.0 · 21.10.2026 · Status: godkjent av Thomas

# Kvalitetssikring etter steg 2: grafikk

Påstander og valg i konseptgrafikken og toppgrafikkvariantene som er tolkning, eget valg eller ikke bekreftet. Listen samles med de andre stegene i `05-kvalitetssikring.md`. Kildene `[K1]`–`[K9]` viser til `01-innsikt.md`.

## Konseptgrafikken «Slik lages tallene»

| # | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| G1 | Produksjonssiden: bruttoprodukt Fastlands-Norge (3 910) + oljevirksomhet og utenriks sjøfart (1 114) + produktavgifter og -subsidier (488) = BNP (5 511), 2025, milliarder kroner | 09189 `[K5]`. Summen går eksakt opp, kontrollert | Om det er riktig å sette olje og sjøfart (markedsverdi) ved siden av Fastlands-Norge (basisverdi) i samme søyle |
| G2 | Anvendelsessiden: konsum i husholdninger (2 341) + offentlig konsum (1 255) + bruttoinvestering i alt (1 265) + eksport (2 512) − import (1 861) = 5 511 | 09189 `[K5]`. Summen går eksakt opp. «Konsum, husholdninger» omfatter ideelle organisasjoner | Etiketten er «Konsum, husholdninger mv.», som i Konjunkturtendensene (12880). Ingen |
| G3 | «Bruttoproduktet er produksjon minus innsats av varer og tjenester» | Standarddefinisjon `[T]`. «Om statistikken» er ikke lest | Ordlyden |
| G4 | «Olje, gass og utenriks sjøfart trekkes ut, fordi de svinger med priser og felt» | `[T]`. Begrunnelsen står ikke i kildene vi har lest | Om dette er SSBs egen begrunnelse |
| G5 | 2. kvartal 2026: +8,7 prosent i løpende priser og +2,0 prosent i volum mot samme kvartal i fjor | 09190 `[K6]`. 8,7 er regnet av oss fra løpende priser, 2,0 er publisert | Ingen |
| G6 | «Volum holder prisene fra 2023 fast» | Faste 2023-priser og kjedede volumtall `[K5][K6]` | Forenkling: kjedingen er utelatt |
| G7 | Kvartalstall om lag åtte uker etter, endelige tall to år etter, hovedrevisjon om lag hvert femte år | `[K1][K3][K4]` | Om åtte uker er riktig regel |
| G8 | «Det BNP ikke måler: velferd, fordeling eller formue. Ulønnet arbeid i hjemmet er ikke med» | `[T]`. Ikke lest i SSBs dokumentasjon | Om formuleringen er riktig og ønsket |

## Toppgrafikkvariantene

| # | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| T1 | A: «+0,3 prosent vekst i fastlandsøkonomien fra kvartalet før» | 09190 `[K6]` | Ingen |
| T2 | A: «SSB omtaler det som nær normal vekst» | Sitat av Julian Paulsen Blytt `[K1]` | Ingen |
| T3 | A: 2023K3 og 2023K4 er 0,0 og vises som en tynn strek | 09190 | Ingen |
| T4 | B: «Den uthevede ruten er tallet SSB løfter fram i overskriften» | Artikkelen 27.8.2026 innleder med Fastlands-BNP fra forrige kvartal `[K1]` | Om det gjelder alle publiseringer |
| T5 | B: Fra samme kvartal i fjor er ujustert, fra forrige kvartal er sesongjustert | Statistikkvariablene i 09190 `[K6]` | Ingen |
| T6 | C: Oljeandelen = «Oljevirksomhet og utenriks sjøfart» / BNP i løpende priser | Regnet av oss fra 09189 | Om utenriks sjøfart bør være med i et mål på oljeandel |
| T7 | C: «Derfor er Fastlands-BNP hovedtallet» | `[T]`, samme som G4 | Om begrunnelsen holder |
| T8 | C: «En femdel» i overskriften for 20,2 prosent | Avrundet med vilje | Ingen |

## Variant D, lagt til 21.10.2026

Thomas syntes A, B og C bommet og ba om noe mer klassisk: årlig vekst over en rekke år. Konseptgrafikken er godkjent.

| # | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| T9 | D: «1,7 prosent vekst i fastlandsøkonomien i fjor» (2025) | 09189 `[K5]` | Ingen |
| T10 | D: «Snittet de siste ti årene var 1,9 prosent» (2016–2025, 1,86 avrundet) | Regnet av oss fra 09189 | Om snitt av årlige rater er riktig mål, eller om geometrisk snitt bør brukes |
| T11 | D: «Siden 1971 har fastlandsøkonomien bare krympet i fire år: 1988, 1989, 2009 og 2020» | 09189 `[K5]` | Ingen |
| T12 | D: 2024 og 2025 vises som foreløpige | Tabellnote i 09189: tall etter basisåret 2023 er foreløpige `[K5]` | Ingen |
| T13 | D: BNP vises som strek i samme figur | Eget valg | Om det blir for tett. Alternativt bare Fastlands-BNP |

**Beslutning 21.10.2026:** Thomas valgte D som toppgrafikk, med BNP-streken. A, B og C er kandidater til seksjoner: A og B under spørsmål 1 og 4, C under spørsmål 2.

## Avvik fra standardene

- **Variant B** er en tabell med fire store tall, ikke et diagram. Valgt fordi poenget er at tallene sammenligner med forskjellige ting, ikke hvor store de er.
- **Variant C** bruker arealdiagram fra null med én serie i marine, fordi grønn er brukt for Fastlands-Norge.
- **`felles/grafikk.py`** er laget i dette steget. Den er hentet ordrett fra reserven i folkemengde, som fortsatt bygger identisk.

Steg 5 i formidlingsprototype for navn · versjon 0.1 · 23.10.2026 · Status: til faglig kontroll

# Kvalitetssikring: Navn (navn)

Denne listen erstatter spørsmålene og listene i `01-innsikt.md`, `02-kvalitetssikring.md`, `03-kildekart.md` og `04-byggenotat.md`. Prototypen: https://thomasbjornskau.github.io/ssb-formidlingsprototyper/navn/index.html

Del A er det som kan være feil eller misvisende. Del B er formuleringer og egne valg. Del C er åpne spørsmål. Korte svar holder.

## A. Må avklares

| # | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 1 | Topplisten slår sammen skrivemåter (Lucas 225 + Lukas 186 = 411), mens statistikkbanken har én kode per skrivemåte | Toppgrafikken, lesehjelpen, konseptgrafikken trinn 3, kortet | Artiklene «Jentenavn» og «Guttenavn», tabell 10467 | Hvilken regel avgjør hva som er samme navn? Kan grupperingen deles som data? |
| 2 | Nora har 366 i topplisten, men Nora 357 + Norah 6 = 363. De 3 vises som «andre skrivemåter». Summert fra statistikkbanken ville Sofie (364) stått foran Nora | Toppgrafikken, jentenavn | Artikkelen «Jentenavn», tabell 10467 | Hvilken skrivemåte er de 3? Er rekkefølgen Nora foran Sofie riktig? |
| 3 | Fra 2021 telles barn etter navngivningsår, før det etter fødselsår. Markert som brudd i kurvene | Navnebølgen, dominansfiguren, lesehjelpen, konseptgrafikken trinn 1 | Note i tabell 10467 | Kan årene før og etter 2021 sammenlignes direkte? Hvor stor er forskjellen i praksis? |
| 4 | Andelen før 1945 vises som en del av samme kurve som senere år. Antall finnes fra 1945, full telling fra 1964 | Navnebølgen, dominansfiguren, ingressen («9 av 100 jenter fikk navnet Anna i 1881») | Tabell 10467, artikkelen «De mest brukte navnene i Norge gjennom tidene» | Hva bygger tallene før 1964 på? Er døde og utvandrede med? Er det forsvarlig å vise 1881 i ingressen? |
| 5 | «Personer som heter navnet» i 10501 tolkes som alle med navnet som fornavn | Populært eller vanlig, kortet, vanligste fornavn | Tabell 10501 | Gjelder tallet første fornavn eller alle fornavn? Anne: 55 625 |
| 6 | I 10501 er bindestreknavn regnet sammen med navnet før bindestreken i 2021–2024. Årene er merket. Anna stiger i 2021–2024 og faller i 2025 | Personer over tid | Note i tabell 10501 | Er 2025 tilbake på gammel praksis? Bør 2021–2024 heller utelates? |
| 7 | Topp 10s samlede andel var 26–27 prosent rundt 1945, nesten like høyt som i 1880 | Dominansfiguren | Egen beregning fra tabell 10467, eksakte skrivemåter | Er toppen reell, eller et utslag av grunnlaget før 1964? |

## B. Bør leses

| # | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 8 | Ordene «populært» (nyfødte) og «vanlig» (personer) | Lesehjelpen, egen seksjon, konseptgrafikken trinn 4 | Vårt begrepsvalg | Godtar fag ordene, eller finnes etablerte betegnelser? |
| 9 | «Alle folkeregistrerte personer er med» | Konseptgrafikken trinn 2 | Ingressen på statistikksiden | Gjelder det også tabell 10467? Noten til 10501 sier «personer med norsk personnummer» |
| 10 | Tegnet «.» i 10467 vises som «færre enn 4 eller ikke i bruk», fordi notene gir to betydninger | Navnebølgen, tips, tabeller | Notene til 10467 | Riktig lesning? |
| 11 | Andel 0,000 tegnes som null, men tipset sier «kan være avrundet ned» | Navnebølgen | Tolkning | Er 0,000 null eller et lite tall? |
| 12 | Plassering etter eksakt skrivemåte, for eksempel «Lukas nr. 34 av 523» | Kortet | Regnet fra 10467 | Er det greit at plasseringen avviker fra topplisten? |
| 13 | Navngitte jenter og gutter (om lag 26 600 og 27 900) regnet som medianen av antall delt på andel | Toppgrafikken, nøkkeltall | Egen beregning, kontrollert ved bygging | Publiseres antall navngitte et sted? |
| 14 | Mest brukte navn og topp 10-andel per år er regnet fra eksakte skrivemåter og blir lavere enn SSBs tall (12,4 mot 13,7 prosent for gutter) | Dominansfiguren | Egen beregning, forklart i figuren | – |
| 15 | Søket foreslår andre skrivemåter bare for topp 5-gruppene. Mohammad og Muhammad er ikke koblet | Søket | `data/synonymer.json` | Bør flere grupper med? |
| 16 | Navn som bare finnes i 10501 forklares med «brukt av færre enn 200 personer året før, eller har bindestrek» | Kortet, navnebølgen | Tolkning av notene | Riktig forklaring? Gjelder for eksempel Kateryna og Anne-Brit |
| 17 | Uten valgt navn vises Anna som eksempel | Kortet og alle seksjoner med *mitt navn* | Eget valg | – |
| 18 | «De vanligste navnene i befolkningen er navnene som var mest brukt da de som lever i dag ble født» | Seksjonen om befolkningen | Tolkning. Toppårene (Anne 1958, Jan 1957) er regnet | – |
| 19 | Overskriften i toppgrafikken velger navnet der flest har en annen skrivemåte (Lucas, Leah) | Toppgrafikken | Eget valg | – |
| 20 | Varsel om små tall under 20 barn | Kortet | Eget valg | Passer grensen? |
| 21 | Endring i etternavn skrives med %-tegn i stolpeetikettene | Etternavn | Plassmangel | – |

## C. Spørsmål

| # | Spørsmål | Grunnlag |
|---|---|---|
| 22 | Stemmer hypotesene om misforståelser? Vi tror de viktigste er at topplisten og statistikkbanken skal stemme overens (H1, H2), at populært og vanlig er det samme (H3), og at toppnavn i dag er like dominerende som før (H4) | `01-innsikt.md`, avsnitt 4 |
| 23 | Hvilke spørsmål om navn får dere oftest, og hvilke misforståelser møter dere? | «Om statistikken» sier lite om bruk og feilkilder |
| 24 | Artikkelen «De mest brukte navnene i Norge gjennom tidene» ser ut til å si «rundt 121 000» for Anna og Anne samlet, mens tabellen gir 88 500 + 84 900. Er det riktig lest? | Lest gjennom et sammendrag, ikke bekreftet |
| 25 | Er navn den mest brukte statistikken i statistikkbanken, målt i uttrekk? | Thomas' opplysning, ikke kontrollert mot «Bruk av statbank» |
| 26 | Er dere riktige kontaktpersoner, eller bør andre se på dette? | Kontaktpersoner i «Om statistikken» og tabellene |

## Avklart underveis

- **Terskelen for statistikkbanken** (tidligere K-4, H6): notene sier at 10467 har navn brukt av minst 200 personer året før, og at 10501 og 12891 har navn med flere enn 200 bærere. Konseptgrafikken er rettet fra «tre eller færre bærere vises ikke» til terskelen på 200, med navnesøket som eget punkt.
- **Fristen på seks måneder** (tidligere K-1): kom fra 2000-publiseringen og var ikke bekreftet. Konseptgrafikken sier nå det notene sier: navngivningsår fra 2021, fødselsår før.
- **«Per 1 000»** på statistikksiden er per 1 000 navngitte av samme kjønn. Bekreftet ved å regne Noah: 477 / 27 930 × 1 000 = 17.
- **Lavpunktet for Anna** var feil i første utkast av `01-innsikt.md` (0,3 prosent i 1964). Riktig er 0,2 prosent i 1957.
- **Topp 10-andelen** gjenskapes fra publiserte totaler: gutter 13,7 prosent (publisert 13,7), jenter 13,1 (publisert 13,2). Avviket kommer trolig av avrundet andel i nevneren.
- **Tekniske forhold, ikke fagets ansvar:** metadata i 10501 og 12891 merker bestand som «Flow». Rådata er hentet direkte fra PxWebApi v2. `felles/grafikk.py`, som arbeidsprosessen viser til, finnes ikke i repoet, så grafikkfunksjonene ligger i `scripts/grafikk_navn.py`. Siden er 2,66 MB, rundt 0,5 MB med gzip.

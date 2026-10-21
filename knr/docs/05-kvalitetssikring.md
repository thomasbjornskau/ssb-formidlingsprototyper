Steg 5 i formidlingsprototype for knr · versjon 0.1 · 21.10.2026 · Status: til faglig kontroll

# Kvalitetssikring: Nasjonalregnskap (knr)

Listen samler alt fra stegene 1–4 som er tolkning, eget valg eller ikke bekreftet. Den **erstatter** listene i `01-innsikt.md` (avsnitt 7 og 8), `02-kvalitetssikring.md`, `03-kildekart.md` (hull og hindre) og `04-byggenotat.md` (nye valg). Prototypen er også gått gjennom på nytt, og «Om statistikken» (sist oppdatert 1.9.2026) er nå lest. To forhold ble rettet, se «Avklart underveis».

**Prototypen:** https://thomasbjornskau.github.io/ssb-formidlingsprototyper/knr/index.html

Kildene `[K1]`–`[K9]` viser til `01-innsikt.md`. `[OS]` er «Om statistikken» på statistikksiden. Tallene er hentet fra statistikkbanken 21.10.2026 og kontrollert av `scripts/lag_data.py` ved hvert bygg (se `04-byggenotat.md`, avsnitt 3).

## A. Må avklares

Dette kan være feil, eller kan gi et misvisende inntrykk hvis det er feil.

| # | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 1 | «Olje, gass og utenriks sjøfart trekkes ut, fordi de svinger med priser og felt», og «Fastlands-BNP svinger mindre med oljeprisene» | Konseptgrafikken (trinn 3), lesehjelpen | Vår begrunnelse `[T]`. Verken artiklene eller `[OS]` sier hvorfor Fastlands-BNP er hovedtallet | Er dette SSBs begrunnelse? Hvordan ville dere sagt det i én setning? |
| 2 | Oljeandelen regnes som «Oljevirksomhet og utenriks sjøfart» / BNP i løpende priser: 20,2 prosent i 2025, 34,9 prosent i 2022 | «BNP, Fastlands-BNP og olje og gass», konseptgrafikken | Regnet av oss fra 09189 | Er det riktig å kalle dette oljeandelen når utenriks sjøfart er med? Bør figuren bare vise oljevirksomheten? |
| 3 | «I kroner» er regnet av oss fra løpende priser. Noten sier «Forskjellen er i hovedsak prisendring». Lesehjelpen: BNP 2. kvartal 2026 var 8,7 prosent høyere i kroner, men 2,0 prosent høyere i volum | Kroner mot volum, lesehjelpen, konseptgrafikken (trinn 4) | 09189, 09190. SSBs prisendring står i tabellen under figuren. Artikkelen 27.8.2026 knytter økningen i løpende priser til konflikten i Midtøsten `[K1]` | Holder formuleringen, gitt kjedingen? Er 8,7 prosent et tall dere selv ville brukt? |
| 4 | Den grønne ruten i «fire tall» er Fastlands-BNP fra forrige kvartal, sesongjustert, med teksten «tallet SSB løfter fram i overskriften» | «Hvor fort vokser økonomien nå?» | Artikkelen 27.8.2026 `[K1]` | Gjelder det alle publiseringer? Er dette tallet dere vil at brukere skal sitere? |
| 5 | Når nivået er null eller negativt (lagerendring og statistiske avvik), viser kvartalsfiguren SSBs publiserte rater, som kan være flere hundre prosent, med en advarsel. Figuren for kroner mot volum vises ikke | Kvartalsfiguren og kroner mot volum, når lagerendring er valgt | 09190. `[OS]`: sesongjusterte tall for lagerendring og statistiske avvik beregnes residualt | Bør rater for lagerendring vises i det hele tatt? Bør lagerendring tas ut av velgeren? |
| 6 | Hovedrevisjonen: nivåendringer for 2022 for sju størrelser, skrevet inn for hånd fra artikkelen. «Den største enkeltendringen var boligtjenester fra selveide boliger. Veksten ble endret mindre enn nivået» | «Hvor sikre er tallene?», lesehjelpen (Fastlands-BNP +5,1 prosent) | `[K2][K4]`. Står ikke i statistikkbanken | Er tallene riktig avskrevet? Er formuleringen om boligtjenester riktig? |
| 7 | «Når tallene kommer»: kvartal ca. 40 dager etter, endelig år 21 måneder etter, hovedrevisjon ca. hvert 5. år | Konseptgrafikken (trinn 5) | `[OS]` sier 40 dager for måned og kvartal, og 21 måneder for endelige tall. Men 2. kvartal 2026 kom 27.8, 58 dager etter. `[OS]` nevner hovedrevisjoner i 2002, 2006, 2011 og 2014, og den siste kom i 2025 `[K4]` | Hva er riktig regel å oppgi for kvartalet? Er «ca. hvert 5. år» riktig? |

## B. Bør leses

Formuleringer, tolkninger, søkeord og egne valg.

| # | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 8 | Produksjonssiden i én søyle: Fastlands-Norge (3 910) + olje og sjøfart (1 114) + produktavgifter og -subsidier (488) = BNP (5 511) | Konseptgrafikken (trinn 1) | 09189, summen går eksakt opp. `[OS]`: BNP i markedsverdi = bruttoprodukt i basisverdi + produktskatter − produktsubsidier | Om fordelingen er riktig vist (Fastlands-Norge og olje i basisverdi, avgiftene for seg) |
| 9 | Kortnavnene «Privat konsum» og «Offentlig konsum» i konseptgrafikken, «Konsum, husholdninger mv.» i figuren for anvendelse | Konseptgrafikken (trinn 2), «Hva driver veksten?» | 09189 har «Konsum i husholdninger og ideelle organisasjoner» | Hvilke kortnavn dere foretrekker |
| 10 | «Volum holder prisene fra 2023 fast» | Konseptgrafikken (trinn 4) | `[OS]` om kjeding: fastpristall bakover beregnes ved å kjede med volumvekstratene | Forenkling: kjedingen er utelatt. God nok? |
| 11 | «Det BNP ikke måler: velferd, fordeling eller formue. Ulønnet arbeid i hjemmet er ikke med» | Konseptgrafikken | `[T]`. Står ikke i `[OS]` | Om formuleringen er riktig og ønsket |
| 12 | Referansestreken er Fastlands-BNP for alle størrelser, og BNP når Fastlands-BNP er valgt | Toppgrafikken, kvartalsfiguren | Eget valg | Om streken gir mening for små størrelser |
| 13 | Kortet viser andel av BNP for alle størrelser, også import, eksport og samlet sluttanvendelse | Kortet for valgt størrelse | Regnet av oss | Om andel av BNP er misvisende for disse |
| 14 | «Snittet de siste ti årene var 1,9 prosent» (2016–2025, aritmetisk snitt av årlige rater, 1,86) | Toppgrafikken | Regnet av oss fra 09189 | Om geometrisk snitt bør brukes |
| 15 | Næringsfiguren viser bruttoprodukt i basisverdi. Fastlands-Norge samlet er +1,8 prosent i 2025, mens Fastlands-BNP i markedsverdi er +1,7. Noten forklarer forskjellen | «Hva driver veksten?» | 09170, 09189, `[OS]` | Om forklaringen er god nok |
| 16 | Fire synonymer i søket er usikre: boligbygging, turisme, handel med utlandet, offentlig pengebruk | Søket | `data/synonymer.json` | Om de peker på riktige størrelser, og om andre søkeord mangler |
| 17 | Varsel om små størrelser under 50 milliarder kroner | Kortet | Eget valg | Om grensen er rimelig |
| 18 | Månedsfiguren viser 24 måneder. Overskriften gir spennet i månedsendringen. For andre størrelser enn BNP og Fastlands-BNP vises Fastlands-BNP med forklaring | «Hvor sikre er tallene?» | 11721. `[OS]`: tremånedersveksten i mars, juni, september og desember tilsvarer kvartalsveksten | Om månedstallene bør vises, se også spørsmål 22 |
| 19 | 2024 og 2025 vises som foreløpige (lysere) i alle figurer | Toppgrafikken, kvartalsfiguren | Tabellnote i 09189 `[K5]`. `[OS]`: endelige tall 21 måneder etter året | Om 2024 nå skal regnes som endelig (21 måneder etter er september 2026) |

## C. Spørsmål

| # | Spørsmål | Grunnlag |
|---|---|---|
| 20 | Stemmer hypotesene H1–H10 om misforståelser? Hvilke ser dere oftest i henvendelser, og hvilke mangler? | `01-innsikt.md`, avsnitt 4 |
| 21 | Hvor store er de vanlige revisjonene av kvartalsveksten i Fastlands-BNP? Finnes det en nyere revisjonsanalyse? | `[OS]` viser til en studie fra 2004 (BNP-veksten oppjustert 0,5 prosentpoeng i snitt). `[K8]` dekker 2012–2013. Statistikkbanken har ingen revisjonsserie |
| 22 | Bør månedstallene være med i en oversikt for allmennheten, eller er de for usikre? | `[OS]`: kvartalstall er summen av tre måneder |
| 23 | Hvordan bør boligtjenester forklares, når de sto for en stor del av oppjusteringen ved hovedrevisjonen? | `[K2]` |
| 24 | Sesongjusterte kvartaler summerer ikke alltid til året (Fastlands-BNP 2025: +7,3 milliarder). Bør prototypen forklare det? | Kildekartet, kontroll K7. `[OS]` sier at slik konsistens bare gjelder enkelte serier |
| 25 | Publiseres bidrag til vekst (konsum, investering, eksport) et sted? Prototypen viser bare nivåer for anvendelsen | `01-innsikt.md`, avsnitt 8 |
| 26 | Er Johan Nitter-Hauge og Pål Sletten riktige mottakere, eller bør Julian Paulsen Blytt (kontakt for 09190, sitert 27.8.2026) være med? | `[OS]`, `[K1]` |

## Avklart underveis

- **«Om statistikken» er lest** (var hull H1). Det bekrefter definisjonen av bruttoprodukt (G3), at BNP i markedsverdi er bruttoprodukt i basisverdi pluss produktskatter minus subsidier, at kvartalstall er summen av tre måneder og at tremånedersveksten i siste måned i kvartalet er kvartalsveksten (kontroll K9), kjedingsavviket (H9, kontroll K8), og at seriene er konsistente fra 1970 (år) og 1978 (kvartal).
- **Rettet i konseptgrafikken:** «Kvartal ca. 8 uker etter» er endret til «ca. 40 dager etter», og «Endelig år to år etter» til «21 mnd. etter», som i `[OS]`. Avviket for 2. kvartal står som punkt 7.
- **Rettet i konseptgrafikken:** «Konsum, husholdninger mv.» overlappet tallet i bred visning. Endret til «Privat konsum» og «Offentlig konsum» (punkt 9).
- **Rettet i steg 4:** feil i konsollen for lagerendring, avkuttede næringsnavn på mobil, og prosentvis endring for størrelser med negativt nivå.
- **Bekreftet uten merknad:** T1–T3, T5, T8, T9, T11 og G2 (tallene stemmer med statistikkbanken). Fiske og havbruk +5,1 prosent i 2. kvartal 2026 stemmer med artikkelen `[K1]`.
- **Hierarkiet i makrostørrelsene** (H4 i kildekartet) vises med innrykk som i statistikkbanken. Ikke fagets ansvar.
- **Tekniske forhold:** `hent_data.py` stopper hvis svaret har færre celler enn ventet (H5 i kildekartet), og bør tas inn i de andre prototypene. Figurfunksjonene bør flyttes til `felles/`. Endringene ligger lokalt og er ikke pushet.

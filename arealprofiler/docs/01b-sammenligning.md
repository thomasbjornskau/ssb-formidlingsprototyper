Steg 1b i formidlingsprototype for arealprofiler · versjon 0.1 · 05.11.2026 · Status: utkast

# Dagens Tableau-app mot innsikten

**Grunnlag.** Vurderingen bygger på arbeidsboka (`vis-arealprofiler-v3.twb`: 113 ark og 44 dashbord), dataene i 14478/14488 og innsiktsnotatet `01-innsikt.md`. Den publiserte versjonen på Tableau Public er ikke sett i nettleser, så bruksopplevelsen (lastetid, mobil, skjermleser) er vurdert ut fra oppsettet, ikke testet. `[T]` gjelder hele vurderingen.

## 1. Hvordan appen er bygd

- Forside med tre temaknapper (A, B, C), og under dem én side per indikator. Hver indikatorside har tre visninger: en tabell for valgt kommune etter år, søyler som sammenligner kommuner med filter for fylke og sentralitet, og en tidslinje.
- Tre oversikter: kart (én indikator om gangen), nøkkeltallstabell (alle indikatorer for én kommune) og barometer (persentilrangering på alle indikatorer).
- Navigasjon med knappene hjem, forrige og neste. Fast størrelse 1200 × 1000 piksler. Mobiloppsettet er ufullstendig og har tre døde knapper.
- Forklaringene ligger i tekstfelt under hver visning. Data kan lastes ned som én Excel-fil.

## 2. Hva appen gjør riktig, hva den mangler

| Tema | Gjør riktig | Mangler eller gjør feil | Forslag |
|---|---|---|---|
| Min kommune | Kommunevalg på hver side, nøkkeltallstabell for én kommune | Kommunevalget må gjøres på nytt per side. Ingen side samler kommunens profil | Én kommuneside som er utgangspunktet, med alle indikatorene samlet |
| Sammenligning | Filter for fylke og sentralitet | Ingen referanseverdi: verken landet, fylket eller medianen i sentralitetsgruppen. Søylene med 357 kommuner er uleselige | Vis kommunen mot medianen og spredningen i sentralitetsgruppen (H3) |
| Retning | – | Barometeret rangerer etter persentil uten fortegn. Det blander indikatorer med 103 og 357 kommuner (H3, H5) | Fjern samlet rangering. Vis plassering per indikator uten «best» og «dårligst» |
| Kart | Kommunekart med alle indikatorer | Farger etter absolutte tall (antall boliger, bygninger, dekar), så store kommuner dominerer (H4) | Kart bare for andeler og rater. Antall som søyler eller punkter |
| Tid | Tidslinje per indikator | Rullerende fireårssummer vises som vanlige tidsserier (H2). Årsfiltrene er hardkodet, og siste år varierer (H6) | Merk perioden («2023–2026»). Vis siste år for hver indikator |
| Begreper | Gode forklaringstekster i arbeidsboka | Forklaringen står i små tekstfelt, ofte nederst. Navnene er tunge og ulike mellom ark og data. «Boligareal» uten forklaring (H1) | Lesehjelp ved hvert tall. Korte navn på klart språk. Konseptgrafikk for grunnareal, sentrumssone og arealreserve |
| Struktur | Tre temaer | Inndelingen i sosialt, miljø og økonomi følger ikke spørsmålene planleggerne stiller. Kodene A1–C12 sier ingenting | Organiser etter spørsmål: tetthet, nedbygging, reserver, fare |
| Hull | – | «..», 0 og «ikke aktuelt» vises likt eller ikke i det hele tatt (H5). Indre Østfold mangler uten forklaring | Egen markering og forklaring |
| Brudd | – | B9 har ny definisjon og A5 er revidert uten merking (H8) | Stiplet strek og forklaring |
| Gjenbruk | Excel-nedlasting | Figurene kan ikke tas rett inn i et plandokument. Ingen lenke til en bestemt kommune | Lenke per kommune, figurer som PNG/SVG og en utskriftsvennlig kommuneprofil |
| Vedlikehold | – | 113 ark, hardkodede år, etiketter som må stemme tegn for tegn og manuell kopiering ved nye indikatorer | Bygg fra Statistikkbanken med skript: ny årgang betyr å kjøre bygget på nytt |
| Plattform | Gratis og raskt å publisere | Tableau Public er en ekstern plattform med eget grensesnitt og egne vilkår, og den følger ikke SSBs designsystem. Universell utforming er ikke kontrollert. Siden kan bare bygges inn som iframe | Egen HTML-side på SSBs eller prototyprepoets plattform |

## 3. Forslag til ny tilnærming

### Visualisering: fra 38 sider til én kommuneprofil og fire spørsmål

**Grep 1: «Min kommune» som gjennomgående valg.** Valget gjøres én gang, og alt annet følger, slik som i folkemengde. Øverst står kommunen med fire nøkkeltall, ett per spørsmål. Lenken inneholder kommunen (`#3201`), så en planlegger kan sende eller sitere nettopp den profilen.

**Grep 2: Indikatorstripe i stedet for barometer.** Én rad per indikator, gruppert etter spørsmålene i innsikten. Hver rad viser kommunen som en prikk på en strek med spredningen i sentralitetsgruppen (10–90 prosent), og landsmedianen som merke. Til høyre står tallet, året eller perioden og en liten tidsserie. Hele profilen blir én side som kan leses og skrives ut. Det tar seg av H3, H5 og H6.

**Grep 3: Fire spørsmålsseksjoner med én hovedfigur hver:**

1. *Bygger vi tettere?* Nye boliger mot alle boliger, med avstand til sentrum (C9 mot C10) og andelen utenfor tettsted. Hovedbudskapet er at nye boliger i 70 prosent av kommunene ligger nærmere sentrum enn boligmassen som helhet.
2. *Hva bygger vi ned?* Omdisponert jord over tid, med jordvernmålet på 2 000 dekar og kofola som landstall. Under: strandsonebygg og dispensasjoner.
3. *Hva er planlagt?* Reserve mot bruk: arealreserve for bolig, fritid og næring ved siden av det som faktisk er bygd siste fire år. Det tar seg av H7. Bruddet i B9 merkes.
4. *Bygger vi i fareområder?* Aktsomhets- og naturfareområder side om side, med forklaring på forskjellen.

**Grep 4: Konseptgrafikk øverst.** Én figur som forklarer grunnlaget: kommunen sett ovenfra med tettsted, sentrumssone, arbeidsplassklynger, 100-metersbeltet, dyrka jord og planlagt areal. Den forklarer begrepene i H1, sentrumssone og arealreserve før tallene kommer.

**Bevisst utelatt:** samlet rangering, kart over absolutte tall og tidslinjer for fireårssummer uten periodemerking.

### Publisering: tre nivåer

| Nivå | Hva | For hvem | Vedlikehold |
|---|---|---|---|
| 1. Statistikkbanken | 14478/14488 publisert eksternt, helst med landstall og fylkestall | Analytikere, API-brukere, andre verktøy | Fagseksjonen, årlig |
| 2. Kommuneprofil på nett | Statisk HTML-side bygd fra API-et (formidlingsprototype), med lenke per kommune | Planleggere, statsforvalter, presse | Ny årgang betyr å kjøre bygget på nytt. Ingen manuelt arbeid i et verktøy |
| 3. Kommunerapport | Utskriftsvennlig profil per kommune (PDF eller utskrift fra nettsiden) med figurer og kildehenvisning | Planleggere som skriver planstrategi | Lages automatisk fra samme bygg |

Tableau-appen kan leve videre til nivå 1 og 2 er på plass. Deretter bør den avvikles, ikke vedlikeholdes i parallell.

**Kostnad og risiko.** Nivå 2 og 3 krever at 14478/14488 blir publisert eksternt (eller at prototypen bruker kildetabellene). De krever også en avklaring av landstall, hullene i Indre Østfold og enheten for B11/B12. Prototypen kan bygges på CSV-uttrekket i mellomtiden, merket som foreløpig.

## 4. Arbeidsliste til steg 4

1. Kommuneside med `#kommunenummer` i lenken
2. Indikatorstripe mot sentralitetsgruppen og landsmedianen
3. Fire spørsmålsseksjoner med hovedfigur
4. Konseptgrafikk (steg 2)
5. Lesehjelp og markering av mangler, null og ikke aktuelt
6. Periodemerking for fireårssummer, brudd i B9 og A5
7. Utskriftsvisning per kommune
8. Byggeskript fra Statistikkbanken, uten hardkodede år

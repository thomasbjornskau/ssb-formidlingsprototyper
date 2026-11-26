Steg 2 i formidlingsprototype for sykefratot · versjon 1.0 · 26.11.2026 · Status: godkjent av Thomas

# Kvalitetssikring av grafikken

**Merking.** Kildene `[K1]`–`[K15]` er de samme som i `01-innsikt.md`. `[T]`: vår tolkning eller vårt valg.

Tallene i grafikken ligger i `data/grafikk-utkast.json`. De er hentet direkte fra data.ssb.no (API v2, json-stat2) 26.11.2026 og erstattes av `data/raw/` i steg 3.

## Valg 26.11.2026

Thomas godkjente konseptgrafikken, valgte variant A som toppgrafikk og vil ha variant C som egen seksjon lenger ned. Variant B brukes ikke som egen grafikk. Spørsmål 2 dekkes av konseptgrafikken.

## Konseptgrafikken («Slik lages tallene»)

| # | Påstand eller valg | Grunnlag | Må sjekkes |
|---|---|---|---|
| 1 | Navs sykmeldingsregister har «alle legemeldte sykmeldinger» | Registeret skal omfatte alt legemeldt fravær `[K1]`. Om lag 5 prosent av sykmeldingene i 2022 kunne ikke kobles til et arbeidsforhold `[K1]` | Om forenklingen er akseptabel, eller om det bør stå «nesten alle» |
| 2 | Egenmeldinger fra om lag 10 000 bedrifter | `[K1]` | – |
| 3 | «Hver arbeidsdag med fravær teller, vektet med stillingsprosent og sykmeldingsgrad» | Definisjonen av sykefraværsdagsverk `[K1]` | At forenklingen holder. Dager på jobb under aktiv sykmelding teller også `[K1]`, og det er ikke nevnt |
| 4 | Eksempelet 0,5 × 0,8 = 0,4 dagsverk per dag | Eksempeltall, merket. Multiplikasjonen er vår lesning av definisjonen `[T]` | At stillingsprosent og sykmeldingsgrad faktisk ganges slik |
| 5 | 8,91 millioner tapte dagsverk, ikke sesongjustert | Tabell 12439 og 12946 `[K7]` `[K10]` | – |
| 6 | Brøken viser ikke antall avtalte dagsverk | Avtalte dagsverk er ikke publisert i 12439 `[T]` | Om nevneren er publisert et sted. Da bør tallet stå i brøken |
| 7 | 5,7 prosent ujustert, 6,65 sesongjustert | `[K7]` | – |
| 8 | «Tallene revideres ved hver publisering» | Sesongjusterte tall fra 2015 re-estimeres når nye rådata kommer `[K1]` | Om formuleringen er presis nok. Tall før 2015 er låst |
| 9 | Sesongfiguren viser 2025K1–2026K3 | Valg for å vise mønsteret med få punkter `[T]` | – |
| 10 | Ikke med: barns sykdom, permisjoner, selvstendig næringsdrivende, vernepliktige, diagnoser | `[K1]` `[K2]` | – |

## Toppgrafikk A: nivå og trend

| # | Påstand eller valg | Grunnlag | Må sjekkes |
|---|---|---|---|
| 11 | «Nesten flatt siden starten av 2025» | Sesongjustert mellom 6,54 og 6,67 i alle kvartaler fra 2025K1 `[K7]`. Ordvalget er vårt `[T]` | – |
| 12 | Overskriften avrundes til 6,7 prosent, figuren viser 6,65 | Malens regel om avrunding | – |
| 13 | «Toppen: 8,01 i 2003» | Høyeste sesongjusterte verdi i serien `[K7]` | Om den sesongjusterte serien er sammenlignbar før og etter 2015. Fagspørsmål 4 i 01-innsikt |
| 14 | Bruddlinje bare ved 2015 | A-ordningen og ny referanseuke `[K1]`. SN2007-bruddet i 2009 gjelder bare næringstall `[K1]` | At ingen andre brudd påvirker totalen |
| 15 | Den ujusterte serien er tegnet over hele perioden | Den er ikke korrigert for bruddet i 2015 `[K1]` | Om den bør stiples før 2015, eller starte i 2015 |

## Toppgrafikk B: hva 6,7 prosent betyr

| # | Påstand eller valg | Grunnlag | Må sjekkes |
|---|---|---|---|
| 16 | «Av 100 avtalte arbeidsdager gikk nesten 7 tapt til sykdom» | Sykefraværsprosenten, sesongjustert 6,65 `[K7]`. Omregningen er vår `[T]` | At «arbeidsdager» er et akseptabelt hverdagsord for avtalte dagsverk |
| 17 | Rutenettet viser sesongjustert, søylene viser legemeldt ujustert | To ulike mål i samme grafikk, merket hver for seg `[T]` | Om blandingen forvirrer mer enn den forklarer |
| 18 | 6,3 prosent av lønnstakerne hadde legemelding, 4,9 prosent av dagsverkene | Tabell 12446 `[K12]` | – |
| 19 | «Gradert sykmelding er én grunn til at tallene er forskjellige» | Personer telles uten gradering, dagsverk med `[K1]`. Andre grunner: ulik referanseperiode (én dag mot tre uker) og at personer telles i hovedarbeidsforholdet `[K1]` `[T]` | Hvilken forklaring fag vil bruke |

## Toppgrafikk C: korte og lange fravær

| # | Påstand eller valg | Grunnlag | Må sjekkes |
|---|---|---|---|
| 20 | «2 av 3 fravær er egenmeldinger» | 62,7 prosent av tilfellene `[K10]` | Om egenmeldte tilfeller fra utvalgsundersøkelsen kan sammenlignes med legemeldte tilfeller fra registeret |
| 21 | Gruppene 1–16, 17–31 og 32 dager eller mer | Tabellens 1–8 og 9–16 er slått sammen av oss, fordi arbeidsgiverperioden er 16 dager `[K1]` `[T]` | At grupperingen er faglig rimelig |
| 22 | Varigheten gjelder bare dagene innenfor kvartalet | `[K1]`. Det betyr at mange av de lengste fraværene er lengre enn grafikken viser | Om dette må stå tydeligere enn i en linje |
| 23 | Andelene er regnet av oss fra antall | `[K10]`. Etikettene summerer til 100 i begge stolpene | – |

## Tekniske valg

| # | Valg | Grunnlag | Må sjekkes |
|---|---|---|---|
| 24 | `scripts/grafikk.py` er en lokal kopi med samme funksjonsnavn som `felles/grafikk.py` | Repoet var ikke i arbeidsområdet | Slås sammen med `felles/` i steg 4 |
| 25 | Roboto Condensed vises som Roboto i vår rendering | Fonten finnes bare som variabel Roboto her `[T]` | Sjekk i nettleser med fontene lastet |
| 26 | Én tekstfarge `#274247` (mørk 5) i begge grafikktypene | Diagramstandardens foreløpige `#274246` er praktisk talt lik | – |
| 27 | Sekvensiell grønn skala for varighet i C | Kategoriene har naturlig rekkefølge (ssb-diagramstandard) | – |

Steg 4 i formidlingsprototype for navn · versjon 1.0 · 23.10.2026 · Status: utkast

# Byggenotat: Navn (navn)

Bygger på `03-kildekart.md` og valgene i steg 1–3: *mitt navn* som gjennomgående valg, toppgrafikk C med veksler mellom jente- og guttenavn, og full bølge fra 1880 (alternativ 1). Malen tar utgangspunkt i `folkemengde` (CSS, søk med forslag, «Se alle», figurfunksjoner). Siden er én fil på 2,66 MB (rundt 0,5 MB med gzip), og to bygg gir identisk fil.

## 1. Hva som er bygget

| Del | Svarer på | Innhold |
|---|---|---|
| Hode | – | Ingress generert fra tallene, navnesøk over alle 2 152 navn, «Se alle navn» (alfabetisk, med antall bærere) og seks eksempler: Anna, Lukas, Kim (begge kjønn), Thomas, Kateryna (bare personer) og Fiolina (ingen treff) |
| Kort for valgt navn | 1, 4 | Kjønn, nyfødte siste år med plassering etter eksakt skrivemåte, året navnet var mest brukt, personer som heter det, og hvordan SSBs toppliste grupperer det (Lukas regnes med Lucas). Lenke til samme navn for det andre kjønnet. Varsel om små tall under 20 barn. Uten valg vises Anna, merket som eksempel |
| Lesehjelpen | H1, H3, H5, H6 | Fire punkter: topplisten slår sammen skrivemåter (Lucas), populært og vanlig (generert for valgt navn), brudd i tidsserien, sjeldne navn. Konseptgrafikken i «Slik lages tallene» |
| Toppgrafikk | 2 | Variant C: topp 5 med vanligste og andre skrivemåter, veksler for jente- og guttenavn. Stort tall og setning velges etter navnet der flest har en annen skrivemåte (Lucas, Leah). Stolpene kan klikkes og velger navnet. Fire nøkkeltall |
| Hvordan har navnet utviklet seg? | 1 | Navnebølgen for valgt navn: andel 1880–2025 eller antall 1945–2025 (bryter). Stiplede linjer for 1945, 1964 og 2021. Toppåret og siste år merket |
| Populært eller vanlig? | 4 | To paneler med hver sin skala: nyfødte siste år og personer, for valgt navn, toppnavnet blant nyfødte og det vanligste navnet i befolkningen (samme kjønn). Personer 2013–2025 som stolper, der 2021–2024 er merket for bindestreknavn |
| Er toppnavnene mindre dominerende? | 3 | Topp 10 samlet og det mest brukte navnet, andel av nyfødte 1880–2025, veksler for kjønn. Tipset viser hvilket navn som var mest brukt hvert år |
| Hvilke navn er vanligst i befolkningen? | 4, 5 | Ti vanligste jente- og guttenavn med felles skala, valgt navn uthevet. 15 vanligste etternavn med endring fra 2018 |
| Bunntekst | – | Om tallene, egne beregninger, kilder, hentedato og lenke til navnesøket på ssb.no |

Alle figurer har «Vis tallene» og kildelinje med tabellnummer og oppdateringsdato fra json-stat-svaret. Valgt navn ligger i adressen (`#navn=2LUKAS`). Stolpene i toppgrafikken, parpanelene og fornavnslistene kan brukes med tastatur.

## 2. Hvordan hull i data vises

- **Færre enn 4 eller ikke i bruk** («.» i 10467): linjen brytes. Tips og tabell sier «færre enn 4 eller ikke i bruk». Enkeltår uten naboer vises som prikk.
- **Antall før 1945** («..»): bryteren for antall starter i 1945. Tipset sier «finnes ikke før 1945».
- **Andel 0,000**: tegnes som null, men tipset sier «kan være avrundet ned».
- **Navn som bare finnes i 10501** (178 navn): kortet forklarer det, og navnebølgen viser en tekst i stedet for en tom figur. Bryteren skjules.
- **200 eller færre bærere** («.» i 10501): «200 eller færre» i stolpe, tips og tabell. Er alle år under grensen, vises en tekst.
- **Ingen treff i søket**: forklaring om grensen på 200 bærere, lenke til navnesøket på ssb.no og «se alle navn».

## 3. Kontroller i `lag_data.py`

| Kontroll | Toleranse | Største faktiske avvik |
|---|---|---|
| Kjente tall: Anna 1881 (9,036), Noah 2025 (460), Emma 2025 (386), Anne personer (55 625), Hansen (47 879) | Eksakt | 0 |
| Alle navn i 10467 finnes i 10501 | Eksakt | 0 |
| Skrivemåtene i topp 5 er like i statistikkbanken og artiklene | Eksakt | 0 |
| Publisert total minus skrivemåtene | 0–3 | 3 (Nora) |
| Topp 10-totalene summerer til publisert antall | Eksakt | 0 |
| Publisert topp 10-andel gjenskapt fra antall og nevner | 0,1 prosentpoeng | 0,07 (jenter, 13,13 mot 13,2) |
| Nevneren (antall / andel) er lik for alle navn med minst 100 barn samme år og kjønn | 0,5 prosent | 0,36 prosent |

**Negativ test:** Lukas 2025 endret fra 186 til 190 i en kopi av rådataene. Bygget stoppet med «Kontroll feilet: 2LUKAS: 190 i statistikkbanken, 186 i artikkelen». Filen ble satt tilbake, og bygget ga identisk fil.

## 4. Test i nettleser

Playwright i 1280 og 390 px: ingen feil i konsollen, `scrollWidth` lik bredden. Søk testet på Lukas (gir også Lucas som «samme navn i SSBs toppliste»), Kim (begge kjønn), Kateryna (bare personer), Fiolina (ingen treff), Anne, noah (små bokstaver) og Mohammad. Rettet etter første runde: overlappende årstall på aksene og ved bruddlinjene i smal visning, etikettene for toppår og siste år oppå hverandre, bestemt form («jentene»), og en ingress om befolkningen som ikke var regnet fra tallene.

## 5. Nye valg til kvalitetssikring

Nummerert videre fra `02-kvalitetssikring.md`.

| # | Valg eller påstand | Grunnlag | Må sjekkes |
|---|---|---|---|
| T-10 | Uten valgt navn vises Anna som eksempel | Eget valg: navnet med tydeligst bølge [T] | – |
| T-11 | Plassering etter eksakt skrivemåte («Lukas nr. 34 av 523») | Regnet fra 10467 | Godtar fag en plassering som avviker fra topplisten? |
| T-12 | Mest brukte navn og topp 10-andel per år er regnet fra eksakte skrivemåter | Egen beregning | Toppen rundt 1945 for topp 10 (26–27 prosent): reell, eller et utslag av grunnlaget før 1964? |
| T-13 | Navngitte barn er regnet som medianen av antall / andel | Egen beregning, kontroll i `lag_data.py` | Finnes antall navngitte publisert et sted? |
| T-14 | Søket foreslår andre skrivemåter bare for topp 5-gruppene | `synonymer.json` | Mohammad og Muhammad er ikke koblet, selv om SSB slår dem sammen i artikkelen |
| T-15 | Teksten for navn som bare finnes i 10501: «brukt av færre enn 200 personer året før, eller har bindestrek» | Tolkning av notene [T] | Riktig forklaring? |
| T-16 | Personer 2021–2024 er merket for bindestreknavn. Anna stiger i de årene og faller i 2025 | Note i 10501 | Er 2025 tilbake på gammel praksis, og bør 2021–2024 heller utelates? |
| T-17 | Endring i etternavn skrives med %-tegn i stolpeetiketten | Plassmangel. Avvik fra regelen om å skrive «prosent» | – |
| T-18 | «De vanligste navnene i befolkningen er navnene som var mest brukt da de som lever i dag ble født» | Tolkning [T], tallene for toppår er regnet | – |

## 6. Kjente svakheter

- Filen er 2,66 MB. Med gzip på GitHub Pages er nedlastingen rundt 0,5 MB, men den er den største i repoet.
- Fylkes- og kommunelister er ikke med, fordi de bare finnes som tabeller på ssb.no.
- Grupperingen av skrivemåter må oppdateres for hånd i `synonymer.json` når nye artikler kommer.
- Grafikkfunksjonene ligger i `scripts/grafikk_navn.py`. `felles/grafikk.py`, som skillen viser til, finnes ikke i repoet.
- Søket fjerner aksenter i søkeordet, slik SSB slår sammen tegn i dataene, så «Zoé» finner Zoe.

## 7. Rettet i steg 5

- Konseptgrafikken trinn 1: fristen på seks måneder er byttet ut med det notene til 10467 sier (navngivningsår fra 2021, fødselsår før).
- Konseptgrafikken, boksen «Ikke med»: terskelen på 200 for statistikkbanken står nå skilt fra navnesøkets grense på tre bærere.

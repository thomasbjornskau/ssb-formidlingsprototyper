# Formidlingsprototyper for SSB-statistikk

> **Prototyper.** Sidene her er laget for å prøve ut nye måter å formidle statistikk fra Statistisk sentralbyrå (SSB) på. De er ikke offisielle SSB-publiseringer. Tallene er hentet fra SSBs statistikkbank, men tolkninger, overskrifter og utforming er ikke kvalitetssikret av fagmiljøene før det står i statuskolonnen under.

Hver prototype tar én mye brukt statistikk og viser det viktigste på en pedagogisk måte: hva statistikken måler, hva som er vanskelig å forstå, og hva brukerne ofte misforstår. Prototypene er ikke komplette, og erstatter ikke statistikkbanken.

## Prototyper

| Statistikk | Kortnavn | Status | Sist endret |
|---|---|---|---|
| [Regionale befolkningsframskrivinger](regfram/) | `regfram` | Til faglig kontroll | 14.10.2026 |
| [Konsumprisindeksen](kpi/) | `kpi` | Til faglig kontroll | 14.10.2026 |
| [Utenrikshandel med varer](muh/) | `muh` | Under arbeid, ikke faglig kontrollert | 14.10.2026 |

## Arbeidsprosess

Hver prototype går gjennom de samme stegene, og dokumentasjonen fra hvert steg ligger i `<kortnavn>/docs/`:

1. **Innsikt.** Hva statistikken måler, nøkkelbudskap, vanskelige begreper og sannsynlige misforståelser. Gir 3–5 spørsmål prototypen skal svare på.
2. **Konseptgrafikk og toppgrafikk.** En figur som forklarer hvordan statistikken lages, og en toppgrafikk som viser hovedbudskapet.
3. **Kildekart.** Hvilke tabeller i statistikkbanken som svarer på hvert spørsmål, med testede spørringer og kontroller.
4. **Bygging.** Prototypen, bygget etter SSBs uttrykk og en egen diagramstandard.
5. **Faglig kontroll.** Kontaktpersonene for statistikken går gjennom en samlet kvalitetssikringsliste.
6. **Publisering** her på GitHub Pages.

## Oppbygging

```
README.md                 denne filen
index.html                forside med lenke til hver prototype
LICENSE                   MIT for koden
felles/bygg.py            bygger <kortnavn>/index.html
felles/vendor/            d3 og Open Sans, med lisenser
.github/workflows/        kontroll ved hver endring
<kortnavn>/
  README.md               hva prototypen viser, kilder, status
  index.html              prototypen, ferdig bygget
  data/kilder.json        spørringene mot statistikkbanken
  data/raw/               svarene fra statistikkbanken, uendret
  scripts/hent_data.py    henter data/raw/ på nytt
  scripts/lag_data.py     kontrollerer summene og lager datafilen
  src/                    mal og grafikk
  docs/                   dokumentasjon fra stegene 1–5
```

## Bygge og oppdatere

Krever bare Python 3.10 eller nyere, ingen andre pakker.

```
python <kortnavn>/scripts/hent_data.py    # henter ferske tall fra statistikkbanken
python felles/bygg.py <kortnavn>           # kontrollerer og bygger <kortnavn>/index.html
```

Bygget stopper hvis en datakontroll feiler, for eksempel hvis kommunene ikke summerer til fylkene.

## Valg om kodekvalitet

Repoet følger et utvalg av praksisen fra SSBs gruppe for kvalitet i kode og koding ([KVAKK](https://github.com/statisticsnorway/kvakk-doc)), tilpasset at dette er prototyper:

| Praksis | Her | Begrunnelse |
|---|---|---|
| README og lisens | Ja | I roten og i hver prototype |
| Rådata lagres uendret, utdata lages på nytt | Ja | `data/raw/` er innsjekket, `build/` er ikke |
| Kontroller som stopper bygget | Ja | Summekontroller i hver `lag_data.py` |
| CI i GitHub Actions | Ja | Bygger alt på nytt og sjekker at `index.html` er oppdatert |
| Ferdigbygd `index.html` i git | Ja, bevisst avvik | GitHub Pages kan vise siden uten byggesteg, og fagmiljøet ser nøyaktig det som er kontrollert |
| Låste avhengigheter (uv), pre-commit, pytest, SonarCloud | Ikke nå | Skriptene bruker bare Pythons standardbibliotek. Vurderes hvis repoet flyttes til statisticsnorway |
| `SECURITY.md` | Ikke nå | Ingen hemmeligheter eller innlogging i repoet |

## Kilder og lisens

Tallene er fra SSBs statistikkbank og brukes etter [CC BY 4.0](https://www.ssb.no/en/api/statbank-pxwebapi-user-guide). Koden er MIT-lisensiert. d3 (ISC) og Open Sans (SIL OFL 1.1) har egne lisenser i `felles/vendor/`.

Kontakt: Thomas Bjørnskau.

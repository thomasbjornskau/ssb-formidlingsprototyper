# Indikatorer for kjønnslikestilling i kommunene (`likekom`)

**Prototype.** Laget for å prøve ut formidling av statistikken. Ikke en offisiell SSB-publisering. Status: utkast, ikke sendt til faglig kontroll.

Åpne `index.html`, eller se siden på GitHub Pages under `likekom/`.

## Hva den svarer på

- Hvor likestilte er vi, målt med tolv indikatorer på en skala fra 0 til 1?
- Hva ligger bak hver skår? Grunnlagstallene vises som vippehusker.
- Hvordan ligger kommunen an mot landet og andre kommuner? Kart.
- Hva har rørt seg siden 2008?

For hele landet, 15 fylker og 357 kommuner, 2008–2024.

## Dokumentene

- `docs/02-kvalitetssikring.md` og `docs/grafikk/`: grafikken fra steg 2
- `docs/03-kildekart.md`: tabeller, metodetest, hull og hindre
- `docs/04-byggenotat.md`: hva som er bygget, kontroller og nye valg
- `docs/01-innsikt.md` og `docs/01b-sammenligning.md`: innsikt, hypoteser og sammenligning med første versjon. Ikke godkjent.

## Kilder

SSB, tabell 09292 (skår) og 09293 (grunnlagstall), PxWebApi v2, CC BY 4.0, og Klass 131 og 104 for endringer i kommune- og fylkesinndelingen. Kartgrunnlag: Kartverket, CC BY 4.0, hentet fra github.com/robhop/fylker-og-kommuner. Rådataene i `data/raw/` er hentet direkte fra API-et 13.11.2026 og er uendret.

Ikon 115 «kvinne og mann» er fra `ssb-ikoner`. Skriften ET Book (MIT-lisens) ligger i `felles/vendor/et-book/`.

## Oppdatering

```
python likekom/scripts/hent_data.py
python likekom/scripts/lag_kart.py   # bare når kommuneinndelingen endres
python felles/bygg.py likekom
```

Nye tall kommer 24.11.2026. `scripts/lag_grafikk.py` lager konseptgrafikken og variantene fra steg 2 på nytt.

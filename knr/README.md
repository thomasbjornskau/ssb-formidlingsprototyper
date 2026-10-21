# Nasjonalregnskap (knr)

> **Prototype under arbeid.** Ikke en offisiell SSB-publisering. Tallene er fra statistikkbanken, men tolkninger, egne beregninger og overskrifter er ikke faglig kontrollert. Se [byggenotatet](docs/04-byggenotat.md) for valg som skal kvalitetssikres.

**Se prototypen:** [https://thomasbjornskau.github.io/ssb-formidlingsprototyper/knr/index.html](https://thomasbjornskau.github.io/ssb-formidlingsprototyper/knr/index.html)

Prototypen viser hvor fort norsk økonomi vokser, forskjellen på BNP og Fastlands-BNP, hva som driver veksten og hvor sikre tallene er. Du kan velge blant 51 makrostørrelser, også ved å søke på hverdagsord som «forbruk» eller «oljeinvesteringer». Valgt størrelse ligger i adressen, for eksempel `#storrelse=koh.nrpriv` for konsum i husholdningene, og styrer alle seksjonene.

## Hva prototypen svarer på

| | Spørsmål | Seksjon |
|---|---|---|
| 1 | Hvor fort vokser økonomien? | Toppgrafikken (årlig vekst fra 1971) og «Hvor fort vokser økonomien nå?» |
| 2 | Hva er forskjellen på BNP og Fastlands-BNP? | «BNP, Fastlands-BNP og olje og gass»: oljeandelen, kroner mot volum |
| 3 | Hva driver veksten? | Anvendelsen av BNP og veksten i 24 næringer, per år og per kvartal |
| 4 | Hvor sikre er tallene? | Månedstall mot tremånederssum og hovedrevisjonen i 2025 |

## Dokumentasjon

- [docs/01-innsikt.md](docs/01-innsikt.md): nøkkelbudskap, begreper og hypoteser om misforståelser
- [docs/02-kvalitetssikring.md](docs/02-kvalitetssikring.md): det som er tolket i grafikken
- [docs/03-kildekart.md](docs/03-kildekart.md): tabeller, spørringer, struktur og kontroller
- [docs/04-byggenotat.md](docs/04-byggenotat.md): hva som er bygget, kontroller og kjente svakheter
- [docs/grafikk/](docs/grafikk/): variantene av toppgrafikk som ble vurdert

## Kilder

| Tabell | Innhold |
|---|---|
| [09189](https://www.ssb.no/statbank/table/09189) | Makroøkonomiske hovedstørrelser, årlig 1970–2025 |
| [09190](https://www.ssb.no/statbank/table/09190) | Makroøkonomiske hovedstørrelser, kvartal fra 1978, sesongjustert |
| [11721](https://www.ssb.no/statbank/table/11721) | BNP og Fastlands-BNP per måned |
| [09170](https://www.ssb.no/statbank/table/09170) | Produksjon og bruttoprodukt etter næring, årlig |
| [09171](https://www.ssb.no/statbank/table/09171) | Bruttoprodukt etter næring, kvartal |
| [Hovedrevisjonen av nasjonalregnskapet](https://www.ssb.no/nasjonalregnskap-og-konjunkturer/nasjonalregnskap/artikler/nasjonalregnskapet-revideres-i-2024) | Nivåendringer for 2022, artikkel 13.11.2025. Ikke i statistikkbanken |

Spørringene står i [data/kilder.json](data/kilder.json).

## Oppdatere

Fra roten av repoet:

```
python knr/scripts/hent_data.py     # henter ferske tall fra statistikkbanken
python felles/bygg.py knr
```

Rådataene i `data/raw/` er hentet direkte fra PxWebApi v2 med `hent_data.py` 21.10.2026, ikke rekonstruert. URL-ene bruker `valueCodes[...]`, og `hent_data.py` stopper hvis svaret har færre celler enn `kilder.json` sier. Kontrollene i `lag_data.py` stopper bygget hvis summene ikke går opp eller nøkkeltallene endres. Ved ny publisering må nøkkeltallene i `lag_data.py` oppdateres for hånd. Hovedrevisjonen er skrevet inn i `lag_data.py` (konstanten `HOVEDREVISJON`).

`scripts/lag_grafikk.py` og `scripts/lag_samleside.py` lager konseptgrafikken og toppgrafikkutkastene fra steg 2.

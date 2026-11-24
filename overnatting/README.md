# Overnattinger (overnatting)

> **Prototype til faglig kontroll, versjon 0.1.** Ikke en offisiell SSB-publisering. Tallene er kontrollert ved bygging, men tolkninger, overskrifter og utforming er ikke kvalitetssikret av fagseksjonen ennå.

**Se prototypen:** [https://thomasbjornskau.github.io/ssb-formidlingsprototyper/overnatting/index.html](https://thomasbjornskau.github.io/ssb-formidlingsprototyper/overnatting/index.html)

Prototypen viser overnattinger ved hotell, campingplasser, hyttegrender og vandrerhjem i Norge. Hovedvalget er de 66 reiselivsregionene (Reiselivsregionar 2024). Du kan velge region i kartet, i fylkesvelgeren eller ved å søke på en kommune eller et sted, for eksempel «Hemsedal» eller «Geiranger». Valgt område ligger i adressen, for eksempel `#omrade=33104` for Hallingdal.

## Hva prototypen svarer på

| | Spørsmål | Seksjon |
|---|---|---|
| 1 | Hvordan går det nå, og er det egentlig rekord? | Toppgrafikken: samme måned hvert år og sesongjustert utvikling |
| 2 | Hvem overnatter: nordmenn eller utlendinger, og fra hvilke land? | Hvem overnatter |
| 3 | Hvor overnatter de, og når på året? | Måned for måned, per år og kartet, for valgt reiselivsregion |
| 4 | Hva tjener hotellene, og hvor fulle er de? | Hotellene |
| 5 | Hva teller statistikken, og hva ligger utenfor? | Slik leser du tallene og Slik lages tallene |

Tall som SSB har skjult av hensyn til konfidensialitet («:»), vises som hull. Summer for år og 12 måneder vises bare når alle månedene er publisert.

## Til faglig kontroll

Den samlede listen over det som må avklares, bør leses og spørsmålene til fagseksjonen står i [docs/05-kvalitetssikring.md](docs/05-kvalitetssikring.md). Den erstatter listene fra de tidligere stegene.

## Dokumentasjon

- [docs/01-innsikt.md](docs/01-innsikt.md): nøkkelbudskap, begreper og hypoteser om misforståelser
- [docs/01b-sammenligning.md](docs/01b-sammenligning.md): sammenligning med Tableau-visningen for reiselivsregioner
- [docs/02-kvalitetssikring.md](docs/02-kvalitetssikring.md): det som er tolket i grafikken
- [docs/03-kildekart.md](docs/03-kildekart.md): tabeller, spørringer, struktur og kontroller
- [docs/04-byggenotat.md](docs/04-byggenotat.md): hva som er bygget, kontroller og kjente svakheter
- [docs/05-kvalitetssikring.md](docs/05-kvalitetssikring.md): samlet kvalitetssikring til faglig kontroll
- [docs/grafikk/](docs/grafikk/): de tre variantene av toppgrafikk som ble vurdert

## Kilder

| Tabell | Innhold |
|---|---|
| [14172](https://www.ssb.no/statbank/table/14172) | Overnattinger per reiselivsregion, etter innkvarteringstype og bostedsland |
| [14176](https://www.ssb.no/statbank/table/14176) | Hotell per reiselivsregion: kapasitetsutnytting, pris og omsetning |
| [14162](https://www.ssb.no/statbank/table/14162) | Overnattinger per fylke etter innkvarteringstype og bostedsland |
| [14178](https://www.ssb.no/statbank/table/14178) | Overnattinger, sesongjustert |
| [14166](https://www.ssb.no/statbank/table/14166) | Hotellovernattinger etter formål, fra 1986 |
| [14165](https://www.ssb.no/statbank/table/14165) | Ankomne gjester |
| [13100](https://www.ssb.no/statbank/table/13100) | Fritidsboliger formidlet av norske formidlere |
| [11270](https://www.ssb.no/statbank/table/11270) | Reiseundersøkelsen: nordmenns overnattinger etter innkvartering |

Reiselivsregionar 2024 og kommunetilknytningen er hentet fra KLASS (klassifikasjon 527 og korrespondansetabell 1512). Kommunegrensene 2024 er fra Kartverket, forenklet av [robhop/fylker-og-kommuner](https://github.com/robhop/fylker-og-kommuner), og kopiert fra `innvbef-omrade`.

## Oppdatering

Rådataene i `data/raw/` er hentet direkte fra statistikkbanken med `scripts/hent_data.py` 24.11.2026 og er uendret. De har de ekte statussymbolene. Slik oppdateres prototypen, fra roten av repoet:

```
python overnatting/scripts/hent_data.py
python felles/bygg.py overnatting
```

`bygg.py` kjører `scripts/lag_data.py`, som kjører kontrollene i `scripts/kontroll_kilder.py` og stopper bygget hvis summene ikke går opp. `region_land_b` (fra 2023) når API-grensen på 800 000 celler sommeren 2028 og må da deles.

Grafikken fra steg 2 lages med `scripts/lag_grafikk.py` (krever Pillow for tekstmåling, ellers et anslag) og `scripts/lag_samleside.py`.

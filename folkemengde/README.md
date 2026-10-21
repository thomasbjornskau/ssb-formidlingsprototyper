# Befolkning (folkemengde)

> **Prototype til faglig kontroll.** Ikke en offisiell SSB-publisering. Tallene er fra statistikkbanken, men tolkninger, egne beregninger og overskrifter er ikke kvalitetssikret ennå. Se [kvalitetssikringslisten](docs/05-kvalitetssikring.md).

**Se prototypen:** [https://thomasbjornskau.github.io/ssb-formidlingsprototyper/folkemengde/index.html](https://thomasbjornskau.github.io/ssb-formidlingsprototyper/folkemengde/index.html)

Prototypen viser hvor mange som bor i Norge og i hver kommune, hva som driver veksten, og hvordan alderssammensetningen endrer seg. Du kan velge blant alle 357 kommuner, også ved å søke på tidligere kommunenavn som Skedsmo eller Snillfjord. Valgt kommune ligger i adressen, for eksempel `#kommune=1804` for Bodø, og styrer alle seksjonene.

## Hva prototypen svarer på

| | Spørsmål | Seksjon |
|---|---|---|
| 1 | Hvor mange er vi, og hvor fort vokser vi? | Toppgrafikken og «Hvor mange er vi …» (landet fra 1735, kommunene fra 1951) |
| 2 | Hva driver veksten? | «Hva driver veksten?»: komponenter per år og per kvartal, opprydding i registeret, regnskapet for siste år |
| 3 | Hvordan endrer alderssammensetningen seg? | Befolkningspyramide (landet hvert år fra 1846, kommunen i 1986, 2006 og 2026) og andeler etter alder |
| 4 | Hvor vokser det, og hvor krymper det? | Fordelingen av kommunenes vekst, fylkene og tabellen over alle kommuner |
| – | Hvem teller som bosatt? | Lesehjelpen og «Slik lages tallene» |

## Dokumentasjon

- [docs/01-innsikt.md](docs/01-innsikt.md): nøkkelbudskap, begreper og hypoteser om misforståelser
- [docs/02-kvalitetssikring.md](docs/02-kvalitetssikring.md): det som er tolket i grafikken
- [docs/03-kildekart.md](docs/03-kildekart.md): tabeller, spørringer, struktur og kontroller
- [docs/04-byggenotat.md](docs/04-byggenotat.md): hva som er bygget, kontroller og kjente svakheter
- [docs/05-kvalitetssikring.md](docs/05-kvalitetssikring.md): samlet kvalitetssikring, erstatter listene i de tidligere dokumentene
- [docs/grafikk/](docs/grafikk/): variantene av toppgrafikk som ble vurdert

## Kilder

| Tabell | Innhold |
|---|---|
| [05803](https://www.ssb.no/statbank/table/05803) | Endringer i befolkningen i løpet av året, hele landet 1735–2026 |
| [06913](https://www.ssb.no/statbank/table/06913) | Befolkning og endringer i kommunene 1951–2026, sammenslåtte tidsserier |
| [01222](https://www.ssb.no/statbank/table/01222) | Endringer i befolkningen i løpet av kvartalet, kommunene og landet |
| [10211](https://www.ssb.no/statbank/table/10211) | Alders- og kjønnsfordeling i hele befolkningen 1846–2026 |
| [07459](https://www.ssb.no/statbank/table/07459) | Alders- og kjønnsfordeling i kommunene og fylkene |
| [Klass 131](https://www.ssb.no/klass/klassifikasjoner/131) | Kommuneendringer, brukt til tidligere kommunenavn i søket |

Spørringene står i [data/kilder.json](data/kilder.json).

## Oppdatere

Fra roten av repoet:

```
python folkemengde/scripts/hent_data.py     # henter ferske tall fra statistikkbanken
python folkemengde/scripts/hent_klass.py    # henter kommuneendringer og lager data/synonymer.json
python folkemengde/scripts/kontroll_kilder.py
python felles/bygg.py folkemengde
```

Rådataene i `data/raw/` er hentet direkte fra PxWebApi v2 med `hent_data.py` 21.10.2026, ikke rekonstruert. URL-ene bruker `valueCodes[...]`. Kontrollene i `lag_data.py` har kjente avvik skrevet inn med verdi (1915 i aldersfordelingen, kommunesummer før 1971, flyttetall som mangler 1951–1957). Endrer SSB tallene, stopper bygget, og avviket må undersøkes før noe publiseres.

`scripts/lag_grafikk.py` lager konseptgrafikken og toppgrafikkutkastene fra steg 2. `scripts/kontroll_kilder.py` kjører kontrollene fra steg 3. `scripts/lag_data.py` lager byggfilen og stopper bygget hvis en kontroll feiler.

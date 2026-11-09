# Uføretrygdede – formidlingsprototype

> **Prototype.** Laget for å prøve ut formidling av statistikken. Ikke en offisiell SSB-publisering. Ikke kvalitetssikret av fagseksjonen ennå.

Side: https://thomasbjornskau.github.io/ssb-formidlingsprototyper/ufore/

## Hva prototypen svarer på

1. Hvor mange er uføretrygdet, og blir det flere? (antall mot andel, SSB mot NAV, hva økningen består av)
2. Hvem er uføretrygdet etter alder? Alder er det gjennomgående valget og styrer alle seksjonene.
3. Jobber uføre? (arbeidsintensitet og uføregrad)
4. Hvilken rolle spiller utdanning?
5. Hvordan er det i min kommune eller mitt fylke? (med aldersjustert indeks og serier 2015–2025 i dagens kommuneinndeling)

## Dokumenter

| Fil | Innhold |
|---|---|
| `docs/01-innsikt.md` | Statistikken, nøkkelbudskap, hypoteser om misforståelser, prioriterte spørsmål |
| `docs/02-kvalitetssikring.md` | Konseptgrafikk og toppgrafikk: påstander og valg som må sjekkes |
| `docs/03-kildekart.md` | Tabeller, struktur, metodetester, datamengde og valg av dataomfang |
| `docs/04-byggenotat.md` | Hva som er bygget, kontrollene og nye valg til kvalitetssikring |
| `docs/grafikk/` | Grafikkutkast fra steg 2 |

## Kilder

SSB statistikkbanken, tabell 11695, 11824, 11828, 07459, 11850, 11696, 11714 og 11736, og Klass 131 (kommuneinndeling). Se `data/kilder.json`.

## Oppdatering

```
python ufore/scripts/hent_data.py     # henter rådata til data/raw/
python felles/bygg.py ufore           # kjører kontrollene og bygger index.html
```

Rådataene i `data/raw/` er hentet uendret fra data.ssb.no 9. november 2026, med statussymboler. De er ikke rekonstruert. Kodelistene for befolkning per kommune i `kilder.json` er skrevet ut eksplisitt per år. Kommer nye statistikkår, må listene og årene i `kilder.json` utvides.

Egne beregninger (dekomponering, omkoding til 2025-inndeling, aldersjustert indeks) er beskrevet i `docs/03-kildekart.md` og merket på siden.

# Unge utenfor arbeid, utdanning og tiltak – formidlingsprototype

> **Prototype.** Laget for å prøve ut formidling av statistikken. Ikke en offisiell SSB-publisering. Status: under arbeid, ikke faglig kontrollert.

Side: https://thomasbjornskau.github.io/ssb-formidlingsprototyper/arbstatus-neet/

Bygd fra statistikkbanktabell 12424 for en artikkel om varigheten av utenforskapet blant unge (NEET), fra statistikken [Tilknytning til arbeid, utdanning og velferdsordninger](https://www.ssb.no/arbstatus). Utvidet med forløpstabellene 12427 og 14158 og barnevernstabellen 13347.

## Hva prototypen svarer på

1. Hva betyr det å være utenfor? NEET er fire ulike grupper, og over halvparten har ukjent status.
2. Er utenforskapet tyngre enn før? (toppgrafikk: dobbelt så mange på AAP eller uføretrygd som i 2008)
3. Hvor mange blir nye i gruppen hvert år, og hvor mange går ut?
4. Hvor lenge er de utenfor, og er det lenger enn før?
5. Innvandrere og befolkningen ellers: høyere andel, annet innhold, og mange flytter fra landet.
6. Hvem er i størst fare? Etter utdanning, innvandringskategori og barnevernsbakgrunn.

En gruppevelger (kjønn, alder, innvandringskategori, utdanning) styrer kortet øverst og seksjonene. Påstandsprøven prøver åtte vanlige påstander mot tallene.

## Dokumenter

| Fil | Innhold |
|---|---|
| `docs/01-innsikt.md` | Statistikken, nøkkelbudskap, hypoteser om misforståelser, prioriterte spørsmål (versjon 0.2, med rettelse om 12427) |
| `docs/02-kvalitetssikring.md` | Konseptgrafikk og toppgrafikk: påstander og valg som må sjekkes |
| `docs/03-kildekart.md` | Tabeller, struktur, metodetester, kontroller og valg av dataomfang |
| `docs/04-byggenotat.md` | Hva som er bygget, kontrollene og nye valg til kvalitetssikring |
| `docs/grafikk/` | Grafikkutkast fra steg 2 |

## Kilder

SSB statistikkbanken, tabell 12424, 12427, 14158 og 13347. Tabell 13556 brukes bare til å kontrollere NEET-tallene. Se `data/kilder.json`.

## Oppdatering

```
python arbstatus-neet/scripts/hent_data.py     # henter rådata til data/raw/
python felles/bygg.py arbstatus-neet           # kjører kontrollene og bygger index.html
python arbstatus-neet/scripts/lag_grafikk.py   # lager konsept- og toppgrafikken på nytt (SVG)
```

Rådataene i `data/raw/` er hentet uendret fra data.ssb.no 10. november 2026, med statussymboler. De er ikke rekonstruert.

Egne beregninger (NEET summert fra statuser, strøm inn og ut, varighet) er beskrevet i `docs/03-kildekart.md` og merket på siden.

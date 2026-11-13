Steg 2 i formidlingsprototype for likekom · versjon 0.1 · 13.11.2026 · Status: utkast

# Kvalitetssikring av grafikken

Steg 1 (innsiktsnotatet) er ikke gjort. Grafikken bygger på filmen fra 13.11.2026, Om statistikken [K1] og metodenotatet [K2]. Variantene er derfor ikke knyttet til godkjente spørsmål og hypoteser.

| Nr | Påstand eller valg | Grunnlag | Må sjekkes |
|---|---|---|---|
| 1 | Alle tall er for hele landet, 2024 | Tabell 09292 og 09293, hentet 13.11.2026, lagret i `data/grafikk-utkast.json` | Hentes på nytt til `data/raw/` i steg 3. Nye tall kommer 24.11.2026 [K1] |
| 2 | Skår for ledere = minste andel / 0,5 = 0,79 | [K1], [K2] avsnitt 4.1 | Ingen. 39,3 / 50 = 0,786 |
| 3 | Vippehusken tipper 40 grader ved skår 0, og den tyngste siden er kjønnet med høyest verdi | [T] Eget valg, ikke fra statistikken | Om «tyngst» leses riktig for deltid, der høy verdi ikke er et gode |
| 4 | Barnehage og fedrekvote vises som fylt måler, ikke vippehuske | [K1]: andelen brukes direkte som skår | Om fedrekvoten heller bør få en vippehuske mot mødre. Grunnlagstall for det finnes ikke i 09293 |
| 5 | Næringsstruktur og utdanningsprogram vises som «bare skår» | 09293 har bare skåren for disse to | Om næringsfordelingen bak kan hentes fra en annen tabell |
| 6 | De tolv er gruppert i fem: rammer, arbeid og omsorg, ressurser, politikk, penger | Thomas' gruppering, etter perspektivene i [K2] | Om fagseksjonen bruker samme inndeling og navn |
| 7 | «Ikke med: én samlet skår per kommune» | [K1]: fra 2012 publiseres ingen samlet skår | Ingen |
| 8 | «Hver har sin egen målestokk» | [T] Skårene regnes på tre ulike måter [K1] | Hvor langt fagseksjonen mener skårene kan sammenlignes på tvers |
| 9 | «Om lag hver tredje kvinne jobber deltid, mot hver sjette mann» (variant C) | 33,4 og 15,8 prosent av sysselsatte 20–66 år | Formuleringen gjelder sysselsatte, ikke alle kvinner og menn |
| 10 | Kortnavn i grafikken: «Utdanningsprogram», «Arbeidsstyrke», «Kommunestyre» m.fl. | [T] Egne kortformer | SSBs egne navn på indikatorene bør brukes i prototypen der det er plass |
| 11 | Rød #DC3400 for kvinner, blå #0D81CF for menn, sort for skår | Thomas' valg av rød. Blå er regnet til samme lyshet (OKLCH 0,585) | Blåfargen står ikke i SSBs palett. Nærmeste er #148ED7 |
| 12 | Skrift ET Book, papirhvit bunn, ingen SSB-grønn | Bevisst avvik fra `ssb-konseptfigurer` og `ssb-diagramstandard`, etter ønske | Skriften ligger i `felles/vendor/et-book/` med lisens (MIT, fra tufte-css) |
| 13 | Ikon 115 «kvinne og mann» er delt i to med klipping | `ssb-ikoner` | Ingen |
| 14 | SVG-ene bruker `transform`, `clipPath`, `use` og `textPath` | Avvik fra SVG-reglene i `ssb-konseptfigurer` | Gruppenavnene langs buen (variant A) vises ikke i alle SVG-lesere utenfor nettleser |
| 15 | `felles/grafikk.py` finnes ikke i repoet | Hjelpefunksjonene ligger i `likekom/scripts/lag_grafikk.py` | Om de skal flyttes til `felles/` |

## Kilder

- [K1] SSB: Indikatorer for kjønnslikestilling i kommunene, statistikksiden med Om statistikken. https://www.ssb.no/befolkning/likestilling/statistikk/indikatorer-for-kjonnslikestilling-i-kommunene
- [K2] SSB Notater 2009/65: metodenotatet om revidert indeks for kjønnslikestilling (vedlagt av Thomas 13.11.2026).

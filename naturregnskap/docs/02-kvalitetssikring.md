Steg 2 i formidlingsprototype for naturregnskap · versjon 0.1 · 05.11.2026 · Status: utkast

# Kvalitetssikring av grafikken

| # | Påstand eller valg | Grunnlag | Må sjekkes |
|---|---|---|---|
| 1 | Grunnkartet er satt sammen av kart fra NIBIO, Kartverket og SSB | [K1] Grunnkartet: AR5, AR50, FKB-vann, N50 og SSB-arealbruk | Forenklet til tre etater. Er det greit for allmennheten? |
| 2 | «Settes på en skala fra 0 til 1» mot intakt natur | [K1, K2] | Referansetilstand er ikke alltid intakt natur. Er forenklingen akseptabel? |
| 3 | Ni tjenester, «som tømmer, karbon og turer» | [K1] | «Karbon» står for global klimaregulering. Se merknaden om «lagring av karbon» i foilserien |
| 4 | De tre delene legges ikke sammen og er målt i ulike år | [K2] om tre bruddpunkter | – |
| 5 | Ikke med: kroner, endringer utover utbygging, det meste av havet | [K1, K2] | «Det meste av havet»: kystvann har tilstand, åpent hav har areal |
| 6 | Alle tall i variant A–C | Eksempeltall i `data/grafikk-utkast.json` | Byttes ut 25.11. Ingen tall er kontrollert |
| 7 | A: andel av fastlands-Norge per naturtype | [T] | Gir utbredelsestabellen andeler, eller må de regnes fra hektar? Hva er nevneren: land, land og ferskvann, eller med kystvann? |
| 8 | B: 2019 → 2024 for skog og fjell | [K3] tabelltitlene for 15012 og 15013 | Finnes totalindeks for 2019 for begge? |
| 9 | C: «7 av 9 tjenester kommer delvis fra skog» | [T], utledet fra metodene: tømmer, klima, luft, temperatur, flom, turisme og rekreasjon | Bekreftes fra 14967. Hvis skog ikke har tilgang i temperatur eller flom, endres tallet |
| 10 | C viser bare andeler, aldri tjenester på felles skala | H3 | – |
| 11 | Farger: Okabe-Ito for delregnskapene (blå, grønn, oransje) | Samme unntak som i foilseriene | Avvik fra SSBs diagramfarger (grønn 3). Avklares før publisering på ssb.no |
| 12 | Grafikken er bygget med konseptfigurbiblioteket, ikke `felles/grafikk.py` | Repoet er ikke tilgjengelig i økten | Flyttes til `felles/grafikk.py` når repoet er tilgjengelig |

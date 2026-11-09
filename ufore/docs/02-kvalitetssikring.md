Steg 2 i formidlingsprototype for ufore · versjon 0.2 · 09.11.2026 · Status: godkjent av Thomas

**Valg 09.11.2026:** Konseptgrafikken er godkjent. Toppgrafikk A (antall, andel og dekomponering av økningen) er valgt. B og C er kandidater til egne seksjoner. Dekomponeringen (G9) må avklares i steg 3 og med fag.

# Kvalitetssikring av grafikken

Alt i konseptgrafikken og toppgrafikkene som er tolkning, eget valg eller ikke står uttrykkelig i en kilde. Samles i `05-kvalitetssikring.md`. Kildene `[K1]`–`[K8]` er de samme som i `01-innsikt.md`.

| Nr. | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| G1 | Trinn 1: «SSB får opplysningene per person, måned for måned» | «Om statistikken», Produksjon [K1] | At formuleringen er presis nok. SSB får dem årlig, med månedlige opplysninger. |
| G2 | Trinn 2: 401 262 hadde vedtak i 2025 | Tabell 11824, «Bosettingsstatus i alt» [K2] | At tallet kan presenteres som «hadde vedtak i 2025» og omfatter 18–67 år på samme måte som hovedtallet. |
| G3 | Trinn 2: «også de som ikke fikk utbetalt fordi de tjente for mye» | NAV-siden om ulike tall [K6]. SSBs side sier bare «uavhengig av utbetaling» [K1] | At inntekt over grensen er hovedgrunnen til vedtak uten utbetaling. |
| G4 | Trinn 3: 12 239 «døde eller flyttet ut» | Definisjonen av ikke-registrert bosatt [K1], tabell 11824 [K2] | At gruppen bare består av døde og utflyttede, og ikke for eksempel personer med uavklart bostatus. Fordeling mellom døde og utflyttede er ikke publisert. |
| G5 | Trinn 4: nevneren er 3 626 571, bosatte 18–67 år per 1.1.2026 (tabell 07459) | 389 023 / 3 626 571 = 10,73 prosent, som stemmer med 10,7 [T] | At SSB bruker nøyaktig denne nevneren. Spørsmål 2 til fagkontakten i 01-innsikt. |
| G6 | «Kobles med»: folkeregisteret 31.12, NUDB 1.10, a-ordningen | «Om statistikken», Produksjon [K1] | Ingen utover at «hver måned» for a-ordningen er vår forenkling. |
| G7 | NAV-boksen: 374 900 ved utgangen av 2025, «bare dem som får utbetalt» | SSB-artikkelen 23.06.2026 [K3], NAV-siden [K6] | NAV teller også bare 18–67 og bare dem med løpende utbetaling. Tallet er hentet fra SSB-artikkelen, ikke fra NAV direkte. |
| G8 | «Ikke med»: diagnose, timer i arbeid, private ordninger | «Om statistikken» [K1] og artikkelen fra 2020 [K5] | At listen er de tre som er mest nyttige å vise. Diagnoser finnes hos NAV. |
| G9 | Variant A: dekomponering av +61 031: befolkningsvekst 22 139, aldring 11 427, høyere andel i hver alder 27 465 | Egen beregning fra 11828 (ettårig alder) og 07459 (befolkning 1.1.2016 og 1.1.2026). Trinnvis: vekst med 2015-andelen, så 2025-alderssammensetningen, så 2025-andelene [T] | Metoden er én av flere mulige rekkefølger. Rekkefølgen påvirker fordelingen. Må godkjennes av fag før den publiseres, eller merkes tydelig som egen beregning. Avgjøres i steg 3. |
| G10 | Variant A: «Litt over halvparten skyldes at befolkningen har vokst og blitt eldre» | 22 139 + 11 427 = 33 566, 55 prosent av 61 031 [T] | Følger av G9. |
| G11 | Variant A: avkortet y-akse (9–11,5 prosent) på andelslinjen | Diagramstandarden tillater det når endringen er poenget [T] | At det ikke overdriver endringen. Alternativ: akse fra null og tallet direkte på linjen. |
| G12 | Variant B: «Over 4 av 100» for 4,4 prosent av 29-åringene | Tabell 11828 [K2] | At 29 år er et rimelig utvalgt alder. Valgt fordi det er siste år i «unge uføre» (18–29) [K1]. Kan virke plukket. Alternativ: 18–29 samlet (2,7 prosent). |
| G13 | Variant B: «dobbelt så høy som i 2015» | 2,1 → 4,4 prosent, faktor 2,1 [K2] | Ingen. |
| G14 | Variant C: «3 av 4» og «1 av 7» | 75,7 og 14,5 prosent i 11850 [K2] | At arbeidsintensitet bare måler lønnstakere. Selvstendige mangler [K1]. |
| G15 | Variant C: sekvensiell grønn for arbeidsintensitet | Kategoriene er ordnet (ingen–full) [T] | Ingen faglig. Lyseste klasse har kant for kontrast. |
| G16 | Variant C: «85 prosent har 100 prosent uføregrad» | 84,9 prosent i 11720, avrundet [K2] | Ingen. |

## Tekniske merknader

- `felles/grafikk.py` var ikke tilgjengelig. Grafikken er laget med en lokal kopi av de samme primitivene i `scripts/grafikk.py`. Den slås sammen med felles i steg 4.
- Tallene ligger i `data/grafikk-utkast.json`, bygd fra `data/raw/` (hentet direkte fra data.ssb.no 09.11.2026, med statussymboler). Ingen celler hadde statussymbol.
- Kildelinjene er 12 px. Konseptfigurstandarden har 14 px som minimum, diagramstandarden 12 px. Valgt fordi kildelinjen er sekundær og skal være lik i hele prototypen.
- SVG-ene har `<title>` og `<desc>` som tekstalternativ, i tillegg til de tillatte tegneelementene.
- Fire farger i variant A (`#5763a6`, `#d5a640`, `#339b71`) er flatetoner fra den ssb-justerte kategoriske paletten. De tre delene er kategorier, ikke rangering.

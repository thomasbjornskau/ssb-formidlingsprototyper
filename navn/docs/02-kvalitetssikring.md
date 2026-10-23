Steg 2 i formidlingsprototype for navn · versjon 1.0 · 23.10.2026 · Status: godkjent av Thomas

**Valg 23.10.2026:** Thomas valgte toppgrafikk C (skrivemåtene, topp 5) med veksler mellom gutter og jenter. Konseptgrafikken er godkjent. A (navnebølgen) og B (populært eller vanlig) blir seksjoner under *mitt navn*.

# Kvalitetssikring av grafikken

Alt i konseptgrafikken og toppgrafikkene som er tolkning, eget valg eller ikke bekreftet direkte i kilden. Samles i `05-kvalitetssikring.md`.

## Konseptgrafikken

| # | Påstand eller valg | Grunnlag | Må sjekkes |
|---|---|---|---|
| K-1 | Fristen for å melde navn er seks måneder, så barn født sent i året kan komme med året etter | 2000-publiseringen [K10] | Gjelder fristen fortsatt? Teller dagens statistikk navngitte barn i året eller fødte i året? |
| K-2 | «Alle folkeregistrerte personer er med» | Ingressen på statistikksiden [K1] | Gjelder det også 10467, eller bare 10501 og navnesøket? |
| K-3 | Topplisten slår sammen stavemåter, statistikkbanken gjør det ikke | Lucas 411 i artikkelen [K3], Lucas 225 og Lukas 186 i 10467 [K5] | Regelen for gruppering. Hvem bestemmer hva som er samme navn? |
| K-4 | Navn med tre eller færre bærere vises ikke | Ingressen [K1] | Gjelder terskelen navnesøket. Terskelen for statistikkbanken er ukjent |
| K-5 | Før 1945 bare andeler, full telling fra 1964 | Statistikkbanken (antall mangler før 1945) [K5], artikkel [K4] | Hva bygger tallene før 1964 på? |
| K-6 | Trinn 4 kaller nyfødte «populært» og personer «vanlig» | Vårt begrepsvalg [T] | Godtar fag ordene, eller finnes det etablerte betegnelser? |

## Toppgrafikkene

| # | Variant | Påstand eller valg | Grunnlag | Må sjekkes |
|---|---|---|---|---|
| T-1 | A | Overskriften «9 av 100» er avrundet fra 9,036 prosent (1881) | 10467 [K5] | Er andelen for 1881 regnet av fødte jenter samme år? |
| T-2 | A | Kurven trekkes sammenhengende over 1945 og 1964, med bruddene markert | Eget valg [T] | Er det riktig å vise andelene før 1945 som en del av samme serie? |
| T-3 | A | Laveste andel er 0,2 prosent i 1957 | Hele serien 1880–2025 [K5] | – |
| T-4 | B | «55 600» er avrundet fra 55 625 | 10501 [K6] | Er 55 625 personer med Anne som første fornavn, eller som et av fornavnene? |
| T-5 | B | Panelene har hver sin skala | Eget valg, nødvendig fordi tallene skiller med faktor 100+ [T] | – |
| T-6 | B | Emma er valgt som kontrast fordi hun er toppnavnet i 2025 | Eget valg [T] | – |
| T-7 | C | Tallene for skrivemåter er fra SSB-artikkelen, ikke statistikkbanken | Artikkelen «Guttenavn» [K3]. Lucas og Lukas er kontrollert mot 10467 | De andre skrivemåtene (Jacob, Oscar, Noa) kontrolleres i steg 3 |
| T-8 | C | «Vanligste skrivemåte» og «andre skrivemåter» er vår inndeling | Eget valg [T] | – |
| T-9 | Alle | Kildelinjen bruker «sist oppdatert 28.01.2026» for tabellene | Oppdateringsdato i metadata for 10467, 10501 og 12891 | – |

## Teknisk

- `felles/grafikk.py` finnes ikke i arbeidsområdet. `scripts/_grafikk_lokal.py` etterligner grensesnittet (`Svg`, `nb`, `sgn`, `bryt`) og byttes ut i steg 4.
- Hvit tekst på grønn flatetone (`#339b71`) i variant C har kontrast rundt 3,6:1, under 4,5:1 for vanlig tekst. Tallene står også i totalen ved stolpeenden.

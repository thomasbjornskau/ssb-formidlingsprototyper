# Kildekart: Regionale befolkningsframskrivinger

Steg 3 i formidlingsprototype for `regfram` · versjon 0.2 · 14.10.2026

Notatet viser hvilke tabeller i statistikkbanken som svarer på de fem prioriterte spørsmålene fra `01-innsikt.md`. Spørringene står i maskinlesbar form i `data/kilder.json`. Alle er testet gjennom SSB-tilkoblingen, og summene er kontrollert. Fagkontakten bør se over tabellvalget i steg 5.

## Spørsmål, tabeller og seksjoner

| Spørsmål | Datasett | Tabell | Seksjon i prototypen |
|---|---|---|---|
| 1. Hvor mange blir vi, og hvor sikkert er det? | folkemengde, nasjonal | 14746, 14740 | Toppgrafikk A, linje om tallet for hele landet |
| 2. Hvor vokser og hvor krymper det? | folkemengde, sentralitet | 14746 | Plassering blant kommunene (variant C), vekst etter sentralitet, fylkene sammenlignet |
| 3. Hvorfor? | komponenter | 14747 | Fødselsoverskudd, innvandring og flytting |
| 4. Hvor raskt eldes befolkningen? | alder | 14746 | Hvor mange av 100 er 70+ (variant B), endring etter alder |
| 5. Min kommune | alle over, per kommune | 14746, 14747 | Hele siden med valgt kommune |

## Kontroller som er kjørt

| Kontroll | Resultat |
|---|---|
| Fylke = sum av kommuner, landet = sum av fylker, alle år | Stemmer |
| Folkemengde neste år = i år + fødte − døde + nettoinnvandring + innenlands nettoinnflytting | Stemmer eksakt for alle 373 regioner og alle år |
| Sum av aldersgrupper = folkemengde | Stemmer for alle 373 regioner |
| Andel 70+ i kommunene mot rapporten (9–26 → 15–32 prosent) | 9,5–26,4 → 15,1–32,2. Stemmer |
| Andel i sentralitetsklasse 1–3 mot rapporten (71,5 → 73,9 prosent) | Stemmer |
| Sum av sentralitetsklasser = hele landet | Stemmer |
| Kommunene summert per klasse etter Klass-koblingen = klassetallene i tabellen, 2026 og 2050 | Stemmer for alle seks klasser (5, 21, 54, 65, 104 og 108 kommuner) |
| Tallet for hele landet mot den nasjonale framskrivingen | Avviker med 18 212 i 2050, som forventet (H4) |

## Funn som endrer byggingen

- **Komponentene for år t forklarer endringen fra 1. januar t til 1. januar t+1.** Prototypen viser i dag komponentene til og med 2050. Når de settes opp mot endringen 2026–2050, skal 2026–2049 brukes.
- **70+ hentes direkte.** Tiårige aldersgrupper gir både 70+ og 80+ for alle kommuner, og gir en finere fordeling i figuren for endring etter alder enn de seks gruppene prototypen bruker i dag.
- **Sentralitet fungerer både for klassene og per kommune.** Datasettet for sentralitet gir de seks klassene. Klasse 5 er den eneste som krymper (567 037 til 564 038), i tråd med rapporten. Koblingen mellom kommune og klasse er hentet fra SSBs klassifikasjonsdatabase (Klass) og ligger i `data/raw/kommune_sentralitet.json`.

## Datamengde og strategi

Alt samlet er om lag 74 000 verdier, eller rundt 450 kB som kompakt JSON. Det er for mye til å legge inn i én HTML-fil som skal leses i git, men lite for nettleseren.

Valgt løsning: `scripts/hent_data.py` henter svarene som json-stat2 til `data/raw/`. `scripts/lag_data.py` kontrollerer summene og lager datafilen, og `felles/bygg.py` baker den inn i `index.html`.

En direkte henting fra API-et i nettleseren er ikke valgt. Det er ikke testet om SSBs API tillater kall fra GitHub Pages, og prototypen skal virke uansett.

## Hull og hindre

1. ~~Kobling mellom kommune og sentralitetsklasse.~~ Løst 14.10.2026 med Klass-korrespondanse 1417. Merk at korrespondansen er merket Sentralitet 2020 mot kommuner 2024, mens tabellens kodeliste heter «Sentralitet 2024». Summene er identiske, så inndelingen er den samme, men navnebruken bør avklares med fagkontakten.
2. **Navn.** Navnene tas fra etikettene i json-stat2-svaret.
3. **URL-ene er ikke kjørt direkte.** Rådataene i `data/raw/` er rekonstruert fra svar hentet gjennom SSB-tilkoblingen. `hent_data.py` er ikke kjørt mot API-et ennå. Første kjøring bør gi samme `index.html`.
4. **Feil i SSB-tilkoblingen.** Ved json-stat2 og flere statistikkvariabler i én spørring havner verdiene på feil rader. Bør meldes til den som eier tilkoblingen.

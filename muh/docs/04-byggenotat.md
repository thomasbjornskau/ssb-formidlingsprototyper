Steg 4 i formidlingsprototype for muh · versjon 0.2 · 04.11.2026 · Status: rettet etter fagets svar på del A

# Byggenotat: Utenrikshandel med varer (muh)

Versjon 0.1 av prototypen. Bygget fra `src/index.template.html` og `data/raw/` med `felles/bygg.py`. Mal, CSS og diagramfunksjoner bygger på kpi.

## Hva er bygget

| Seksjon | Svarer på | Innhold |
|---|---|---|
| Hode og søk | 5 | Ingress generert fra tallene. Søk etter land med forslag mens man skriver, og «Se alle land». Valget ligger i adressen, for eksempel `#land=PL`, og følger tilbakeknappen |
| Kort for valgt land | 5, H5 | Eksport, import og balanse i 2025, andel olje og gass, fastlandsbalansen, skip og plattformer, linje 2015–2025, og hva Norge selger til og kjøper fra landet (ensifret SITC) |
| Slik leser du utenrikshandelen | H1, H2, H3, H6 | Fire punkter, og konseptgrafikken bak «Slik lages tallene» |
| Toppgrafikk C | 3 | Fastlandsbalansen −350 mrd. kr, handelsbalansen og fastlandsbalansen 2015–2025, fire nøkkeltall |
| Hvor mye av eksporten er olje og gass? | 1, H4 | Eksport 1960–2025 fordelt på fastland, olje og gass og skip og plattformer. Regnestykket for fastlandseksporten i siste måned |
| Pris eller mengde? | 2, H1 | Pris- og volumindeks 2000–2025 for alle varer, råolje, naturgass, fastlandsvarer og fisk |
| Hva forteller handelsoverskuddet? | 3, H2, H7, H8 | Balansene per måned 2024–2026 og per år 1960–2025, med merknad om prosent på underskudd |
| Hva selger fastlands-Norge? | 4 | De tolv største tresifrede varegruppene i 2025, og de fire største 2015–2025 |
| Hvem handler Norge med? | 5, H5 | De 15 største eksport- og importlandene i 2025. Eksporten delt i fastland og olje og gass. «Uspesifisert» grå i importen |
| Hvor sikre er de siste tallene? | H6 | Endring fra første til siste kjente tall for hver måned fra 2016, endelige og ikke endelige tall skilt |

## Slik vises hull og spesialtilfeller

| Tilfelle | Eksempel | Visning |
|---|---|---|
| Handel hvert år | Polen | Fullt kort |
| Handel under 0,5 mill. kr | Bhutan | «under 0,5 mill. kr», ikke null |
| Ingen handel 2015–2025 | Pitcairn | «Ingen handel», med forklaring |
| Ikke et land | Uspesifisert | «Ikke fordelt på land», ingen plass i rekkefølgen, merknad om at den finnes fra 2023 |
| Søkeord som ikke er landnavn | england, holland, amerika | Treff via synonymlisten, merket «Funnet med søkeordet» |
| Historisk land | Sovjet | Ingen treff. De 13 historiske landene uten tall er holdt utenfor |
| Ingen treff | xyzzy | «Ingen treff», med lenke til alle land |

## Kontroller i byggeskriptet

`scripts/lag_data.py` stopper bygget hvis en kontroll feiler. Toleransene er satt etter de faktiske avvikene, som skyldes avrunding (08804 er i mill. kr, 08809, 08819 og 12308 i 1 000 kr).

| | Kontroll | Største avvik | Grense |
|---|---|---|---|
| K1 | Sum av land = «Alle land» (08804) | 9 mill. kr | 20 |
| K2 | Eksport = fastland + olje og gass + skip og plattformer, per land og år | 1 mill. kr | 2 |
| K3 | Handelsbalansen og fastlandsbalansen fra komponentene (08800) | 1 mill. kr | 2 |
| K4 | «Alle land» i 08804 = 08800 | 0 | 0 |
| K5 | Fastlandseksport fra tresifret SITC = 08800 | 0,8 mill. kr | 2 |
| K6 | Det som mangler på tresifret nivå, ligger på ensifret nivå | 0 | 2 |
| K7 | Ensifret SITC summerer per land, og total per land i 08809 = 08804 | 2 tusen kr og 0,5 mill. kr | 20 og 0,5 |
| K8 | Månedene 2025 = årstallet 2025 | 3 mill. kr | 12 |
| K9 | Endelige månedstall = årstall | 0,5 mill. kr | 1 |
| K10 | Publiserte pris- og volumendringer mot indeksene | 0,05 prosentpoeng | 0,15 |
| K11 | Månedstabellene har samme siste måned, og alle synonymer peker på land som finnes | – | – |

**Negativ test.** Eksporten til Storbritannia i 2025 ble endret med 300 mill. kr i en kopi av rådataene. Bygget stoppet med «Kontroll feilet: K1 sum av land: avvik 300 er over grensen 20». Filen ble satt tilbake.

**Testet i nettleser** i 1280 og 390 px: ingen feil i konsollen, ingen vannrett rulling, søk og kort for Polen, england, holland, Amerika, Kina, Bhutan, Uspesifisert, Pitcairn, Sovjet og xyzzy. Bygget to ganger med identisk fil.

## Nye valg til kvalitetssikring

Nummerert videre fra steg 2 (G1–G9, T1–T11, X1–X2).

| | Valg | Begrunnelse |
|---|---|---|
| B1 | Synonymlisten: 32 søkeord, 7 merket usikre (england, skottland, wales og nord-irland til Storbritannia, korea til Sør-Korea, dubai og abu dhabi til De forente arabiske emirater) | Folk søker ikke på statistikkbankens navn |
| B2 | Setningen «Handelsoverskuddet følger prisene på olje og gass, ikke hvordan det går i fastlandsøkonomien» | Vår tolkning, støttet av pris- og volumindeksene (06322) og av at fastlandsbalansen har vært negativ hvert år |
| B3 | «Olje og gass i rør føres som eksport til landet røret går til, selv om den kan selges videre derfra» | «Om statistikken» 2015 sier det om olje til Storbritannia. Vi bruker det om gass også |
| B4 | Kortnavn for ensifret SITC, for eksempel «Olje, gass, strøm og annen energi» for gruppe 3 | Fulle navn i tabeller og verktøytips |
| B5 | Fastlandsvarene vises som tresifret SITC, med merknad om at 16,8 mrd. kr ikke er fordelt | Årsaken til avviket er ikke bekreftet (hull 6 i kildekartet) |
| B6 | «Uspesifisert» vises som egen grå stolpe blant importlandene, men får ingen plass i rekkefølgen | Den er ikke et land, men er for stor til å utelates |
| B7 | Fastlandsbalansen per land: fastlandseksport minus import utenom skip og plattformer | Samme definisjon som for landet, men SSB publiserer den ikke per land |
| B8 | Revisjonsfiguren bruker siste kjente tall for måneder som ikke er endelige ennå, merket grått | Ellers ville de siste to årene mangle |
| B9 | Ingen prosentendring for beløp under 0,5 mrd. kr i regnestykket | Liten base gir meningsløse prosenter (kondensater, skip og plattformer) |
| B10 | Sammenligning med samme måned året før, ikke forrige måned | Tallene er ujusterte (H8) |

## Kjente svakheter

- Linjediagrammene kan ikke brukes med tastatur. «Vis tallene» dekker det samme. Stolpene for land er knapper.
- Filen er 620 kB: data 147 kB, d3 og skrift resten.
- Månedstallene gjelder publiseringen 15.09.2026. `hent_data.py` må kjøres for septembertallene fra 15.10.2026.
- Rådataene er rekonstruert fra SSB-tilkoblingen. `hent_data.py` er ikke kjørt mot API-et.
- Søket finner bare landnavn og synonymer. Skrivefeil gir ingen treff.
- Landvalget viser bare enkeltland. EU, Norden og andre grupper er utelatt fordi de skifter innhold og er ulike mellom tabellene.

## Versjon 0.2 (04.11.2026)

Rettet etter fagseksjonens svar på del A i `05-kvalitetssikring.md`, og bygget med ferske tall.

| Endring | Hvor | Grunnlag |
|---|---|---|
| Rådata hentet direkte fra PxWebApi med `hent_data.py`, ikke rekonstruert. URL-ene bruker `valueCodes[...]`, fordi `selection[...]` ikke filtrerer riktig | `data/raw/`, `data/kilder.json` | Punkt 28–29. Årstabellene er identiske med de rekonstruerte |
| Månedstall til og med september 2026 (publisert 15.10.2026) | Hele siden | Punkt 30 |
| «Fastlandsbalansen» heter nå «handelsbalansen fastland» | Hele siden | Punkt 1, 32 |
| Toppgrafikken: «Norge importerte varer for om lag 350 milliarder kroner mer enn fastlands-Norge eksporterte», med setning om utstyr til sokkelen, «i stor grad» og fisk og aluminium | Toppgrafikk, balanseseksjonen | Punkt 1 |
| «Mengde» byttet med «volum», og ny merknad om hva volumindeksen er og ikke er | «Pris eller volum?» | Punkt 2 |
| Undertrykte tall forklarer hvorfor varegruppene ikke summerer | «Hva selger fastlands-Norge?» | Punkt 4 |
| «Uspesifisert» forklart som lavverdisendinger, med egne titler i kortet og fem nye søkeord | Kortet, importlandene, søket | Punkt 5 |
| Brudd i importserien fra 2023 markert med stiplet strek og forklart | Toppgrafikk, balansene fra 1960 | Punkt 33 |
| Rørledningenes landingspunkt, også for gass | Landkortene, «Hvem handler Norge med?» | Punkt 6 |
| «Foreløpig pris» i stedet for «anslått pris», og når tallene blir endelige | Revisjoner, «Slik leser du», konseptgrafikken | Punkt 7 |
| «Småsendinger» fjernet fra «Ikke med i tallene» | Konseptgrafikken | Punkt 8 |

Nye funksjoner i diagramkoden: `brudd` i `kolonner()` og `linjediagram()` tegner en stiplet strek mellom året før og bruddåret.

**Testet:** 1280 og 390 px uten konsollfeil og uten vannrett rulling, søk på de ti tilfellene fra versjon 0.1 og på «lavverdisendinger» og «netthandel». Bygget to ganger med identisk fil. Kontrollene har samme største avvik som i versjon 0.1.

**Kjente svakheter som står igjen:** dagens «Om statistikken» er ikke lest (punkt 23), og pris og volum er ikke kontrollert av prisseksjonen (punkt 2).

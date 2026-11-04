Steg 4 i formidlingsprototype for lonnyrke · versjon 0.1 · 04.11.2026 · Status: utkast

# Byggenotat: Lønn i yrket ditt (lonnyrke)

## Hvorfor en egen variant

Prototypen er eksempelet på et kommunikasjonsdashbord i veileder E. Den bygger på stegene 1–3 i `lonnansatt` (innsikt, konseptgrafikk og kildekart er gjenbrukt), men har et annet format: hele dashbordet skal vises på ett skjermbilde uten rulling (valgt av Thomas 04.11.2026). Derfor avviker den fra den faste rekkefølgen i steg 4: det er ingen seksjoner, «Slik leser du» og konseptgrafikken ligger i dialoger, og «Vis tallene» åpner en dialog i stedet for en utvidbar tabell.

## Hva som er bygget

| Del | Svarer på | Innhold |
|---|---|---|
| Hode | Hvilket yrke? | Tittel, ingress generert fra tallene, søk etter yrke |
| Nøkkeltall | Hva tjener de? | Median månedslønn mot alle yrker, kvinners lønn i prosent av menns, antall jobber og andel kvinner |
| Figur 1 | Hvordan har det utviklet seg? | Median for kvinner og menn 2016–2025, med alle yrker som grå referanse |
| Figur 2 | Hvor ligger yrket? | Alle 302 yrker med tall for begge kjønn: lønn mot kvinners lønn i prosent av menns. Valgt yrke fremhevet, samme hovedgruppe mørkere |
| Bunn | Hva er tallene? | Definisjon i én setning, «Slik lages tallene», «Om tallene», lenke til ssb.no |

## Hull i data

- Yrker uten tall noen gang er tatt ut av velgeren (38 av 406).
- Siste år mangler: ingressen og nøkkeltallene sier at tallet er skjult. Figur 1 viser årene som finnes.
- Tall for ett kjønn er skjult: nøkkeltallet for forskjellen viser en forklaring, og figur 1 viser linjen for begge kjønn. Yrket er ikke med i figur 2, og det står i noten over figuren.
- Ingen treff i søket: lenke til listen over alle yrker, gruppert etter hovedgruppe.

## Kontroller (scripts/lag_data.py)

| Kontroll | Resultat 04.11.2026 |
|---|---|
| K1 jobber for menn + kvinner = begge kjønn | 2 905 kombinasjoner, største avvik 0 |
| K2 406 firesifrede yrker uten «uoppgitt» | 406 |
| K3 hver manglende verdi har statussymbol | 0 uten symbol |
| K4 median for alle yrker finnes for alle år og kjønn | ok |
| K5 kvinner i prosent av menn mellom 50 og 150 | 302 yrker, alle innenfor |

Negativ test: en endret verdi i rådataene stoppet bygget i K1. Filen er satt tilbake.

## Nye valg til kvalitetssikring

Nummerert videre fra `lonnansatt`.

| Nr | Valg | Begrunnelse |
|---|---|---|
| V1 | Median, ikke gjennomsnitt | Medianen er mindre påvirket av de høyeste lønningene og lettere å forklare for publikum |
| V2 | Alle arbeidstider, regnet om til heltid | Samme valg som i `lonnansatt` |
| V3 | Kvinners lønn i prosent av menns per yrke er egen beregning fra avrundede kronebeløp | Ingen publisert rate per yrke |
| V4 | Sykepleiere som standardvisning | Et kjent yrke med mange jobber og tall for begge kjønn |
| V5 | Hovedgruppe 3 omfatter de militære yrkene (01–03), som i 11418 | Følger tabellens egen gruppering |

## Kjente svakheter

- Søket har ingen synonymer. «Lærer» finner ikke «Grunnskolelærere» øverst.
- Punktene i figur 2 kan bare velges med mus. Tastaturbrukere velger med søket.
- På smal skjerm (under 760 px) kan siden rulle. Ett skjermbilde gjelder bred skjerm fra 1280 × 720.

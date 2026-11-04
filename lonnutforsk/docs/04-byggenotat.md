Steg 4 i formidlingsprototype for lonnutforsk · versjon 0.1 · 04.11.2026 · Status: utkast

# Byggenotat: Lønnsforskjeller mellom kvinner og menn (lonnutforsk)

## Formål og format

Internt, utforskende dashbord for veileder E. Det har en annen form enn formidlingsprototypene: felles valg øverst, fire nøkkeltall og sju faner, én per formål fra vedlegg B1. Rekkefølgen i steg 4 (lesehjelp, toppgrafikk og seksjoner) er bevisst ikke fulgt, fordi brukerne kjenner statistikken. Steg 1–3 er ikke kjørt egne. Innsikt og konseptgrafikk finnes i `lonnansatt`.

## Hva som er bygget

| Fane | Formål | Data | Figur | Valg som gjelder |
|---|---|---|---|---|
| 1 Næringer | Sammenligning | 11421 | Liggende søyler, sortert, linje for alle næringer. Klikk velger næring | år, sektor, arbeidstid, mål |
| 2 Over tid | Utvikling | 11421 | Linje per sektor for valgt næring, pek på et år | alle |
| 3 Lønnens deler | Del av helhet | 11421 | Stablede søyler for kvinner og menn: avtalt lønn, tillegg, bonus | år, sektor |
| 4 Spredning etter alder | Fordeling | 11421 | Kvartilspenn med median for kvinner og menn per aldersgruppe | år, sektor, arbeidstid |
| 5 Kvinneandel | Sammenheng | 11421 | Bobler per næring: kvinneandel mot forskjell, størrelse = heltidsekvivalenter | år, sektor, arbeidstid, mål |
| 6 Yrke og næring | To dimensjoner | 11419 | Rutenett med divergerende farge rundt 100 % | år (2016 eller 2025) |
| 7 Yrker over tid | Rangering og avvik | 11418 | Manualdiagram 2016 mot valgt år, avvik over 4 prosentpoeng fremhevet | år |

Valg som ikke gjelder en fane, er dempet og forklart under valgene. Nøkkeltallene og ingressen følger valgene og fanen.

## Hull i data

- Næringer og yrker med skjulte tall tas ut av figuren og listes under den.
- Rutenettet viser skjulte ruter i grått.
- Tabellen bak hver figur («Vis tallene») viser «skjult» eller «ingen».

## Kontroller (scripts/lag_data.py)

| Kontroll | Største avvik 04.11.2026 | Toleranse |
|---|---|---|
| K1 heltidsekvivalenter menn + kvinner = begge | 1 | 2 |
| K2 avtalt + tillegg + bonus = månedslønn | 30 kr (én kombinasjon i «Uoppgitt») | 30 kr |
| K3 nedre kvartil ≤ median ≤ øvre kvartil | 0 brudd | 0 |
| K4 23 næringskoder med «Alle næringer» og «Uoppgitt» | ok | |
| K5 manglende verdier har statussymbol | ok | |
| K6 median alle i 11421 = 11419 | 0 kr | 0 |

Negativ test: en endret komponent stoppet bygget i K2. Filen er satt tilbake. To bygg gir identisk fil.

## Valg til kvalitetssikring

| Nr | Valg |
|---|---|
| V1 | Kvinners lønn i prosent av menns er standardmålet for forskjellen, ikke differansen i kroner |
| V2 | Heltidsansatte og median er standardvisning |
| V3 | Heltidsekvivalenter, ikke antall jobber, brukes for kvinneandel og boblestørrelse |
| V4 | Grensen for avvik i fane 7 er 4 prosentpoeng, satt skjønnsmessig |
| V5 | Fargeskala i fane 6 er avgrenset til 80–120 %. Verdier utenfor får endefargen |
| V6 | «Uoppgitt» og «Alle næringer» er tatt ut av rangeringen. «Alle næringer» vises som referanse |

## Kjente svakheter

- Små grupper gir store utslag. Eksempler er «Bønder, fiskere mv.» i undervisning (43 %) og «Befal med sersjant grad» (−14,7 prosentpoeng). Tallene er publisert, men bør leses med forsiktighet. Antall heltidsekvivalenter vises i tabellene for 11421, ikke for 11418 og 11419.
- Rutene i fane 6 og punktene i fane 7 kan ikke velges med tastatur. Tallene finnes i tabellen.
- Etiketter i boblediagrammet kan overlappe.
- På smal skjerm blir figurene trange. Dashbordet er laget for skjerm fra 1280 px.

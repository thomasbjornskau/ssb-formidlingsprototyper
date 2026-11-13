Steg 4 i formidlingsprototype for likekom · versjon 0.2 · 13.11.2026 · Status: utkast

# Byggenotat

## Hva som er bygget

| Seksjon | Svarer på | Innhold |
|---|---|---|
| Hode | Spørsmål 1 | Ingress generert fra tallene, søk etter kommune eller fylke, knappen «Hele landet» |
| Ringen (variant A, og B på mobil) | Spørsmål 1 og 2 | Årsvelger, ringen med hele landet som stiplet linje (2008 når landet er valgt), tolv vippehusker eller målere |
| Kort for valgt indikator | Spørsmål 2 | SSBs navn og dimensjon, skår, stor vippehuske, tidsserier for grunnlagstall og skår, landet som stiplet linje |
| Slik leser du indikatorene | H1–H6 | Fem punkter og konseptgrafikken |
| Hvor i landet? | Spørsmål 3 | Kommunekart for valgt indikator og år, fem høyeste og laveste, alle tall i tabell |
| Hva har rørt seg siden 2008? | Spørsmål 4 | Tolv små tidsserier på samme skala, landet i grått |

Valget ligger i adressen: `#omrade=5610&aar=2024&ind=InntektBrutto`.

## Endret fra versjon 0.1

- Toppgrafikken (variant C) er fjernet. Siden starter med ringen.
- Årsvelgeren er flyttet fra hodet til ringen.
- Kommunevelger, 15 fylker og 357 kommuner er lagt inn.
- Kart er lagt inn.
- Fem grupper er rettet til SSBs seks dimensjoner.
- Lesehjelpen står etter ringen, ikke før. Det avviker fra den faste rekkefølgen i malen.

## Hull i data

- «tall mangler» der skåren mangler.
- År før kommunens serie starter: ringen er tom, og en merknad sier fra hvilket år tallene finnes. Når en kommune velges, flyttes året fram til første år med tall.
- Kommuner uten tall i kartet er hvite med grå kant, og antallet står i teksten.
- Endring siden 2008 vises ikke for indikatorer med brudd, og ikke når serien er kortere enn hele perioden.

## Kontroller i `lag_data.py`

- 357 kommuner og 15 fylker med tall siste år, og kommunene er de samme som i kartet.
- Landet: skår gjenskapt fra grunnlagstall, største avvik 0,0053. Kjent avvik: kommunestyre 2010.
- Kommuner og fylker: 129 avvik over 0,05, alle offentlig sektor 2012. Bygget stopper ved avvik andre steder.
- Kvinner + menn = 100 prosent i alle fordelinger.
- Negativ test 13.11.2026: kvinneandel blant ledere i Oslo 2024 økt med 9. Bygget stoppet med «Oslo - Oslove Ledere 2024: kvinner + menn = 109.0, ikke 100».
- Bygget to ganger med identisk fil.

## Test

1280 og 390 px: ingen feil i konsollen, ingen vannrett rulling. Søk testet med «oslo» (kommune før fylke), «tana» og «karasjok» (samiske dobbeltnavn), «våler» (to kommuner), «ålesund» (serie fra 2024), «finnmark» (fylke), «sand» (flere treff) og «xyzzy» (ingen treff). Klikk i kartet og bytte av indikator i kartet er testet.

## Nye valg til kvalitetssikring (nummerert videre fra steg 2)

16. Kommunestyre 2010: 09292 og 09293 stemmer ikke overens for hele landet.
17. Offentlig sektor 2012: skår og grunnlagstall stemmer ikke overens i 129 kommuner og fylker.
18. Bruddet for arbeidsstyrke er satt til 2015, ikke 2017 som i Om statistikken.
19. Tidsserier er lenket gjennom rene nummerendringer med Klass. Metoden er vår.
20. Fylkene som ble gjenopprettet i 2024, har bare tall for 2024 i prototypen.
21. Listene «høyest skår» og «lavest skår» er en rangering av kommuner. Innsikten sier at prototypen ikke skal rangere (H2, H5).
22. Kartet bruker faste klasser (under 0,5 til 0,9 og over) for alle indikatorer og år. SSBs eget kart bruker relative farger.
23. Kartet har grå toner, ikke rødt og blått, fordi de fargene betyr kvinner og menn her.
24. Varselet om små kommuner vises for alle kommuner, også Oslo. Prototypen har ikke folketall.
25. Ingressen i tidsseksjonen bruker grensen 0,05 for «steget» og «falt».
26. Kortet bruker SSBs navn fra tabellen, med skrivefeilene «næringsstuktur» og «offtentlig».
27. Y-aksen for grunnlagstall i kortet starter ikke på null for prosent.
28. Kartfilen er hentet fra en tredjepart som bygger på Kartverket.
29. For offentlig sektor 2012 skriver kortet at avviket står på listen til faglig kontroll.

## Kjente svakheter

- Innsikten er ikke godkjent, og fagkontakten har ikke sett noe.
- Kommunene i kartet kan ikke nås med tastatur. Søket og listene er veien inn.
- `index.html` er 1,3 MB.
- Gruppenavnene langs buen er små.
- Gjettespillet er ikke bygget.
- Ikke sjekket på GitHub Pages eller med skjermleser.

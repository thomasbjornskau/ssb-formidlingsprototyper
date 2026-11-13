Steg 4 i formidlingsprototype for likekom · versjon 0.1 · 13.11.2026 · Status: utkast

# Byggenotat

## Hva som er bygget

| Seksjon | Svarer på | Innhold |
|---|---|---|
| Hode | Hvor likestilte er vi? | Ingress generert fra tallene, og årsvelger 2008–2024 som styrer hele siden |
| Slik leser du indikatorene | Hva betyr skåren? | Fire punkter og konseptgrafikken bak «Slik lages tallene» |
| Toppgrafikk (variant C) | Hvor stort er spennet? | Laveste og høyeste skår, ringen, vippehusken for indikatoren lengst unna, fire nøkkeltall |
| Tolv indikatorer, én ring (variant A, og B på mobil) | Hva ligger bak skåren? | Ringen med 2008 som stiplet skygge, tolv vippehusker eller målere, sortert liste på mobil |
| Kort for valgt indikator | Hva ligger bak denne skåren? | SSBs navn, skår, stor vippehuske, tidsserier for grunnlagstall og skår |
| Hva har rørt seg siden 2008? | Hva har endret seg? | Tolv små tidsserier på samme skala, med brudd som opphold |

Valget av år og indikator ligger i adressen (`#aar=2024&ind=Ledere`). Alle figurer har «Vis tallene». Indikatorene kan velges med tastatur.

## Avvik fra malen

- Siden bruker ET Book, papirhvit bunn og sort, rødt og blått, som i filmen. Den bruker ikke `/*__FONT__*/` (Open Sans) eller d3.
- Skriften er bakt inn fra `src/etbook.css` (283 kB) nederst i siden. `index.html` er 371 kB.
- Figurene tegnes med ren JavaScript som SVG-tekst. Tegnefunksjonene er de samme som i `scripts/lag_grafikk.py`.
- Prototypen har ikke søk.

## Hull i data

- Fire indikatorer uten tall for kvinner og menn får en måler og teksten «bare skår» eller andelen.
- Endring siden 2008 vises ikke for de tre indikatorene med brudd, og de er holdt utenfor «størst økning» og «størst fall».

## Kontroller i `lag_data.py`

- Skår gjenskapt fra grunnlagstall: største avvik 0,0053 (utdanningsnivå 2020), toleranse 0,011.
- Kvinner + menn = 100 prosent i fordelingene, toleranse 0,11.
- Kjent avvik: kommunestyre 2010. Bygget stopper hvis det kommer nye avvik eller dette forsvinner.
- Negativ test 13.11.2026: kvinneandel blant ledere 2024 endret til 45,0. Bygget stoppet med «Ledere 2024: kvinner + menn = 105.7, ikke 100».
- Bygget to ganger med identisk fil. Testet i 1280 og 390 px: ingen feil i konsollen, ingen vannrett rulling.

## Nye valg til kvalitetssikring (nummerert videre fra steg 2)

16. Kommunestyre 2010: 09292 og 09293 stemmer ikke overens. Bør meldes til fagseksjonen.
17. Bruddet for arbeidsstyrke er satt til 2015, ikke 2017 som i Om statistikken.
18. Ingressen i tidsseksjonen bruker grensen 0,05 for «steget» og «falt». Eget valg.
19. Kortet bruker SSBs navn fra tabellen, for eksempel «Forholdet mellom menn og kvinners bruttoinntekt». Figurene bruker kortnavn.
20. Tabellen har skrivefeilene «næringsstuktur» og «offtentlig». Prototypen gjengir dem uendret fra API-et.
21. Teksten «0 betyr at bare det ene kjønnet er med» passer for fordelingene, ikke for barnehage og fedrekvote.
22. Y-aksen for grunnlagstall i kortet starter ikke på null for prosent. Den starter på null for kroner.
23. Inntekt er i løpende kroner. Det står ikke i figuren.

## Kjente svakheter

- Steg 1 mangler. Seksjonene er ikke knyttet til godkjente spørsmål og hypoteser.
- Bare landstall. Statistikkens hovedpoeng, kommunene, er ikke med.
- Gjettespillet fra konseptet er ikke bygget.
- Gruppenavnene langs buen kan være vanskelige å lese i venstre halvdel.
- Ikke sjekket på GitHub Pages, og ikke med skjermleser.

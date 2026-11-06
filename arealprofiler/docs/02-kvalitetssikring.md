Steg 2 i formidlingsprototype for arealprofiler · versjon 0.2 · 06.11.2026 · Status: godkjent av Thomas (toppgrafikk C)

# Kvalitetssikring av grafikken

Alt i konseptgrafikken og toppgrafikken som er tolkning, eget valg eller ikke bekreftet. Listen samles i `05-kvalitetssikring.md`.

Q1–Q6 gjelder konseptgrafikken i versjon 0.1, som er erstattet. Q4–Q6 utgår. Q1–Q3 går videre i Q19–Q22. Variant A og B (Q7–Q12) blir seksjoner, og C (Q13–Q16) er valgt toppgrafikk.

| | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| Q1 | De seks kildene i trinn 1 dekker indikatorene | Forklaringstekstene i arbeidsboka `[K5]` | Om noen kilder mangler, for eksempel Enhetsregisteret til sentrumssoner og arbeidsplassklynger, eller vegnettet til B6/B7 |
| Q2 | Skissen i trinn 2 (sjø, 100-metersbelte, tettsted, sentrumssone) | Egen skisse `[T]` | At den ikke antyder at sentrumssonen alltid ligger inni tettstedet. Arbeidsplassklynger er ikke tegnet |
| Q3 | «For hver bygning finner SSB ut hvor den ligger» (trinn 3) | Forklaringstekstene `[K5]` | At alle indikatorene i trinn 3 faktisk regnes per bygning. A1 og B9 regnes per areal, ikke per bygning |
| Q4 | Lillehammers tall 2026: 194 nye boliger, 5,2 %, 2,0 km, 239 m², 796 dekar | 14478 `[K4]` | Ingen, tallene er hentet direkte. De byttes ut med `data/raw/` i steg 3 |
| Q5 | «Siste 4 år» tegnet som fire år som slutter i årstallet | 14478 `[K4][T]` | **Hvilke fire år «2026» dekker**: 2022–2025 eller 2023–2026. Avgjør teksten i variant A |
| Q6 | «Siste år varierer: 2024, 2025 eller 2026» | Talt fra 14478 `[K4]` | Ingen |
| Q7 | Variant A: 10,7 % utenfor tettsted og 50,4 % i blokk for landet | Egen beregning: kommunenes andeler vektet med antall nye boliger, 350 kommuner `[T]` | Om SSB har landstall som kan brukes i stedet. Om vektingen gir riktig resultat når A7/A8 er avrundet til én desimal |
| Q8 | Variant A: «For ti år siden var det 1 av 5» (20,5 % i perioden fram til 2016) | Egen beregning `[T]` | Som Q7. Avrundingen «1 av 5» er bevisst |
| Q9 | Variant B: omdisponert dyrka jord | Sum av C3 `[K4]` | **Forklart i steg 3:** C3 gjelder alle formål, kofola (1 793 dekar i 2025) andre formål enn landbruk. Seksjonen må bruke 11776 for landstall |
| Q10 | Variant B: «for første gang siden 2015» | Serien i 14478 starter i 2015 `[K4]` | Om omdisponeringen var under 2 000 dekar før 2015 (kofola har lengre serier) |
| Q11 | Variant B: jordvernmålet er 2 000 dekar | Tittel på regjeringen.no `[K7]` | Målåret (2030?) og vedtaket. Siden er ikke lest |
| Q12 | Variant B: 2015–2019 mangler 4–13 kommuner | Talt fra 14478 `[K4]` | Om summen for disse årene skal vises i det hele tatt, eller merkes som brudd |
| Q13 | Variant C: Lillehammer «bor tettere enn de fleste kommuner med samme sentralitet» | 36 av 54 kommuner i klasse 3 har lavere andel i tettsted (A3) `[K4][T]` | Om «de fleste» er dekkende (to av tre). Setningen må kunne lages automatisk for alle kommuner |
| Q14 | Variant C: sammenligning mot SSBs seks sentralitetsklasser (indeks 2020) | Kommunenøkkelen i arbeidsboka `[K5]` | Om det finnes en nyere sentralitetsindeks. Dagens app slår sammen til tre grupper, med grenser som ikke stemmer med klassene (H10) |
| Q15 | Variant C: «midtre 80 prosent» (10.–90. persentil) som spredningsmål | Eget valg `[T]` | Om fag foretrekker kvartiler. Klasse 1 har bare fem kommuner, så spredningsmålet virker dårlig der |
| Q16 | Variant C: rekkefølgen og utvalget av de fem indikatorene | Eget valg, ett fra hvert spørsmål `[T]` | Om utvalget er representativt |
| Q17 | Grunnareal som navn på A1 | Arbeidsboka: «bebygd og opparbeidet areal til bolig» `[K5]` | Om «grunnareal» er et etablert SSB-begrep, eller om SSBs eget navn skal brukes |
| Q18 | Enheten dekar for B9 i trinn 4 | 14478 oppgir dekar for B9 `[K4]` | Ingen for B9. Enheten for B11/B12 må bekreftes (fra steg 1) |

## Profilavvik

- Titlene er i Open Sans, som i folkemengde, ikke i Roboto Condensed.
- Toppgrafikken bruker blå `#1d9de2` fra diagrampaletten som andre serie (variant A). Konseptgrafikken bruker bare profilfargene.
- `felles/grafikk.py` finnes ikke i repoet. Skriptet bruker den lokale reserven med samme grensesnitt, som i folkemengde.

## Versjon 0.2 (06.11.2026): ny konseptgrafikk

| | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| Q19 | Fire måter: register (12), KOSTRA (4), kart (18), plan (1) | Egen gruppering ut fra forklaringstekstene `[K5][T]` | At A4, A6, A7 og B1 (Matrikkelen) hører under «register» og ikke «kart». At C5 (pendling) er register |
| Q20 | «Kommunene rapporterer vedtak og saksbehandling til SSB gjennom KOSTRA» | Kildetabellene 13128, 08123 og 11776 `[K5]` | Om B4 kommer fra KOSTRA plan og byggesak |
| Q21 | Eksempelrader i registerboksen (person 67 år, husholdning som leier, bolig i blokk) | Eksempler, ikke statistikk `[T]` | Om de bør merkes som eksempler |
| Q22 | Kildene i kolonne 3: Matrikkelen, Folkeregisteret, SSBs arealbrukskart og soner, NVE, Kartverket | Forklaringstekstene `[K5]` | Om Enhetsregisteret (sentrumssoner, arbeidsplassklynger) og vegnettet (B6, B7) skal nevnes |
| Q23 | Tallene er fra fjorårets fil (siste år 2023–2025) | Valg av Thomas 06.11.2026 | Ingen |

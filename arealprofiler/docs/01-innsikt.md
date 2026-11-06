Steg 1 i formidlingsprototype for arealprofiler · versjon 0.1 · 05.11.2026 · Status: godkjent av Thomas (ved start av steg 2)

# Innsikt: Arealprofiler

**Merking.** `[K1]`–`[Kn]` er navngitte kilder (liste nederst). `[T]` er vår tolkning. `[H]` er en hypotese om misforståelse som fag skal vurdere.

**Om dette notatet.** Arealprofiler er ikke én statistikk, men et produkt bygd av rundt 20 andre statistikker: arealbruk, bolig, befolkning, sysselsetting, KOSTRA landbruk og plan, tettsteder og sentrumssoner. Det finnes derfor ingen egen statistikkside med «Om statistikken». Notatet bygger på siden på ssb.no, de faglige forklaringene som ligger i Tableau-arbeidsboka (tekstene under hver indikator), Statistikkbanken (tabell 14478 og 14488, hentet internt 05.11.2026), «Om statistikken» for kofola og to eksterne kilder. Det er en retrospektiv innsikt: dagens Tableau-app finnes, og vurderingen av den står i `01b-sammenligning.md`. Jeg har sett arbeidsboka før notatet ble skrevet, så skillet mellom de to notatene er ikke så rent som skillen forutsetter.

## 1. Statistikken på ett ark

| | |
|---|---|
| Hva den er | 38 indikatorer per kommune for arealbruk, boligbygging, nedbygging, tilgang til natur og arealreserver i kommuneplanen. De er laget som kunnskapsgrunnlag for den overordnede planleggingen: planstrategi og kommuneplanens samfunnsdel og arealdel. `[K1][K3]` |
| Hva den ikke er | Ikke et arealregnskap og ikke en måling av måloppnåelse. Indikatorene har ingen fast retning der høyt er godt eller dårlig. Ikke tall for landet eller fylket. Tabellene har bare kommuner. `[T]` |
| Oppdragsgiver | Kommunal- og moderniseringsdepartementet (nå KDD). Forprosjekt Rambøll 2018, første versjon med 24 indikatorer i juni 2020, 35 indikatorer i desember 2021. `[K2][K3]` |
| Frekvens | Årlig. Siste oppdatering i 2025-utgaven var 29.08.2025. `[K1]` |
| Referansetid | Varierer mellom indikatorene. Bygningsbaserte indikatorer går til 2026, registerbaserte til 2025, inntekt (A11) til 2024 og strandsone (B3) fortsatt til 2024. 14 indikatorer er rullerende summer for «siste 4 år». `[K4]` |
| Inndeling | 357 kommuner etter 2024-strukturen, pluss Longyearbyen arealplanområde i 14478. Tre tema: A Sosiale forhold (14), B Miljø og klima (12), C Økonomi (12). Sammenligning etter fylke og sentralitetsgruppe. `[K4][K5]` |
| Datakilder | Matrikkelen, SSBs arealbrukskart, tettsteds- og sentrumssoneavgrensning, arbeidsplassklynger, befolknings-, bolig-, inntekts- og sysselsettingsregistrene, KOSTRA (landbruk, plan og byggesak), NVE/Kartverket (fare- og aktsomhetsområder) og kommuneplanenes arealdel. `[K5]` |
| Revisjon | Hele serier revideres. Mellom 2025-utgaven og tabell 14478 er A5 Andel leid bolig revidert med 3–6 prosentpoeng, og B2, B5 og B10 er revidert for mange kommuner. B9 har brudd. `[K4]` |
| Statistikkbanken | 14478 (37 indikatorer) og 14488 (B8). Ikke publisert eksternt per 05.11.2026. `[K4]` |
| Bruk | Planleggere i kommuner, fylkeskommuner og hos statsforvalteren. Bruksvolumet er ikke kjent: «Bruk av statbank» dekker ikke tabellene, og vi har ikke Tableau-statistikk. |

## 2. Nøkkelbudskap

Tallene er regnet fra 14478. Tabellen har ingen landstall, så summer og vektede andeler er `[T]`.

1. **Nye boliger bygges oftere i tettsted og i blokk.** Av boligene som ble igangsatt de siste fire årene før 2016, lå 20,5 prosent utenfor tettsted. Før 2026 var andelen 10,7 prosent. Blokkandelen økte fra 37 til 50 prosent. `[K4][T]` Andelene er vektet med antall nye boliger per kommune.
2. **Nye boliger ligger nærmere sentrum enn boligene som allerede står der.** I 244 av 350 kommuner (70 prosent) er gjennomsnittsavstanden fra nye boliger til sentrumssonen kortere enn for alle boliger. Medianen er 4,8 km for nye boliger og 6,5 km for alle. I 2015 gjaldt dette 60 prosent av kommunene. `[K4][T]`
3. **Omdisponering av dyrka jord har falt kraftig.** Summen av C3 er 1 971 dekar i 2025, mot 6 079 dekar i 2015. Kofola oppgir 1 793 dekar for 2025 `[K6]`. Avviket må avklares, se H9. Det nasjonale jordvernmålet er 2 000 dekar `[K7]`.
4. **Arealreservene i kommuneplanene er store.** Ledig areal til boligbygging er 331 000 dekar i 2026. Reservene til fritidsbebyggelse er 1,03 millioner dekar, tre ganger så mye. Statistikkbanken oppgir ikke enhet for B11. `[K4][T]`
5. **Bygging i aktsomhetsområder er vanlig, i naturfareområder sjelden.** 42 217 bygninger ble igangsatt i aktsomhetsområder de siste fire årene før 2026. I naturfareområder var tallet 3 061, og 160 kommuner hadde ingen. `[K4]`
6. **«Boligareal per bosatt» måler grunnareal, ikke boligens størrelse.** Medianen er 356 m² per bosatt. Oslo har 69 m², Stor-Elvdal 683 m². Tallet er bebygd og opparbeidet areal til bolig delt på antall bosatte, ikke bruksareal i boligen. `[K4][K5]`
7. **Strandsonen bygges fortsatt ut, men stadig mindre.** Antall bygninger igangsatt innenfor 100 meter fra kystlinja de siste fire årene sank fra 14 164 (2019) til 13 024 (2024). Det gjelder 226 kystkommuner. `[K4]`

## 3. Vanskelige begreper

- **Boligareal per bosatt (A1)** er grunnarealet: tomter, hager og veier inne i boligområdet. I Oslo er det 69 m², omtrent som en stor leilighet, men det er tomta, ikke leiligheten. `[K5]`
- **«Siste 4 år»** er en rullerende sum. A6 Nye boliger 2026 = 84 293 boliger igangsatt i fireårsperioden fram til 2026. Fra ett år til det neste er tre av fire år de samme. `[K4][T]`
- **Sentrumssone** er avgrenset av SSB ut fra tettheten av virksomheter med sentrumsfunksjon: høyst 50 meter mellom dem og minst fire hovednæringsgrupper. Ikke alle kommuner har en sentrumssone, og avstanden måles på tvers av kommunegrenser. C6 er derfor 0 eller tom i 135 kommuner. `[K5][K4]`
- **Arbeidsplassklynge:** minst 3 virksomheter med minst 50 ansatte til sammen, og høyst 300 meter mellom virksomhetene. Metoden er hentet fra SCB. Arbeidsboka kaller den selv «en enkel måte å identifisere områdene på». `[K5]`
- **Aktsomhetsområde og naturfareområde (B5, B10):** Aktsomhetsområder er grove kart over mulig fare (NVE og Kartverket). Naturfareområder er utredede faresoner. Derfor er tallene så ulike: 42 217 mot 3 061. `[K5][T]`
- **Arealreserve (B9, B11, B12):** areal som er satt av til et formål i kommuneplanens arealdel, men som ikke er bygd ut ennå. Tallet beregnes ved å legge planen over SSBs kart over faktisk arealbruk. Metoden er endret etter 2022. `[K5][K8]`
- **Sentralitetsgruppe:** SSBs sentralitetsindeks fra 2020, med seks klasser slått sammen til tre i appen. `[K5]`

## 4. Sannsynlige misforståelser

| | Misforståelse | Grunnlag | Hva prototypen må gjøre |
|---|---|---|---|
| H1 | «Boligareal per bosatt» leses som boligstørrelse | Navnet. Arbeidsboka advarer selv mot forveksling med bruksareal `[K5]` | Si «grunnareal til bolig», med en tegning av tomt mot bolig |
| H2 | Endringer fra år til år i «siste 4 år»-indikatorene leses som det som skjedde i ett år | Rullerende summer i 14 indikatorer `[K4]` | Vis hvilke år perioden dekker. Ikke bruk vanlige tidslinjer uten forklaring |
| H3 | Høy eller lav verdi leses som godt eller dårlig | Barometeret rangerer etter persentil uten retning `[K5]` | Ingen rangering uten fortegn. Vis plassering mot lignende kommuner, ikke en poengsum |
| H4 | Absolutte tall sammenlignes mellom store og små kommuner | Kartet farger etter verdi også for antall (A6, B5, B9) `[K5]` | Bruk andeler eller tall per innbygger/areal i kart. Vis antall som søyler |
| H5 | Manglende tall leses som null, eller null som manglende | B10 har 0 for 160 kommuner, C6 mangler der det ikke finnes sentrumssone, B2/B3 gjelder bare 226 kystkommuner `[K4]` | Skill «ikke aktuelt», «mangler» og «null» i grafikken |
| H6 | Tall fra ulike år sammenlignes som om de var samtidige | Siste år er 2024, 2025 eller 2026 avhengig av indikator `[K4]` | Vis årstallet ved hvert tall |
| H7 | Arealreserver leses som det som bygges ut | B9/B11/B12 er planlagt, ikke realisert `[K8][T]` | Sett reserven ved siden av faktisk bygging (A6, B1) |
| H8 | Brudd og revisjoner blir ikke oppdaget | B9 ny definisjon, A5 revidert hele serien `[K4]` | Stiplet strek og forklaring ved brudd |
| H9 | Summen for kommunene leses som landstallet | C3 2025: 1 971 dekar i 14478, kofola 1 793 dekar `[K4][K6]` | Avklar med fag. Vis kofola som landstall hvis det er det riktige |
| H10 | Sentralitetsgruppene leses som SSBs offisielle klasser | Kartteksten oppgir grensene 870/650/295, mens dataene har seks klasser med andre grenser `[K5]` (lav prioritet) | Bruk SSBs seks klasser, eller forklar sammenslåingen |

## 5. Brukere og hva de trenger

1. **Kommune- og fylkesplanleggere** (hovedmålgruppen `[K1]`) skriver kunnskapsgrunnlag for planstrategi og kommuneplan. De trenger min kommune mot lignende kommuner og over tid, med tall og figurer de kan sette rett inn i et plandokument, og med lenke til kilden.
2. **Statsforvalter og fylkeskommune** følger opp nasjonale mål: jordvern, strandsone og samordnet areal- og transportplanlegging. De trenger oversikt over mange kommuner og hvem som skiller seg ut, med riktige landstall.
3. **Lokalpolitikere, presse og innbyggere** trenger få og forståelige budskap: bygger vi tett eller spredt, og bygger vi ned jord og strand? `[K2]` nevner dem som sekundær målgruppe.

Prototypen skal ikke være et analyseverktøy med alle 38 indikatorer i like stor grad, og den skal ikke rangere kommuner.

## 6. Prioritering

Kriterier: (a) sentralt i SSBs egne budskap, (b) stor fare for misforståelse, (c) kan besvares fra Statistikkbanken, (d) passer i en oversikt.

| Prioritet | Spørsmål | Kriterier | Hypoteser | Mulig kilde |
|---|---|---|---|---|
| 1 | Hvordan står **min kommune** sammenlignet med lignende kommuner og over tid? | a, b, c, d | H3, H4, H5, H6 | 14478 alle indikatorer, sentralitet |
| 2 | Bygger vi **tettere og nærmere sentrum**? | a, c, d | H2, H1 | A3, A6–A8, C9–C12 |
| 3 | Hvor mye **jord, strand og natur** bygges ned? | a, b, c | H2, H9 | C3, C4, B3, B4, B8, kofola |
| 4 | Hvor mye areal har kommunen **satt av** i planen, og hva er brukt? | b, c, d | H7, H8 | B9, B11, B12 mot A6, B1 |
| 5 | Hvor mye bygges i **fare- og aktsomhetsområder**? | b, c | H5 | B5, B10 |

**Må med uansett:** lesehjelp for hver indikator (hva den måler, år og periode, kilde), og et skille mellom mangler, null og ikke aktuelt.

**Kan vente:** demografi og bolig (A5, A9–A14), som allerede finnes i andre SSB-produkter. Tilgang til rekreasjon og nærturterreng (B6, B7), som bare oppdateres annethvert år. Andel bebygd areal etter klasse (B8).

**Utenfor:** C2 (ingen tall), Longyearbyen, egne beregninger av mål eller rangering.

## 7. Spørsmål til fagkontakten

1. Stemmer hypotesene H1–H10, og hvilke er viktigst for planleggerne dere møter?
2. Hvorfor gir summen av C3 for 2025 1 971 dekar når kofola har 1 793? Hvilket tall er riktig som landstall?
3. Kan 14478/14488 få landstall og fylkestall, eller bør prototypen hente dem fra kildestatistikkene?
4. Hva skjedde med B9 (ny definisjon?) og A5 (revidert hele serien), og hvilken enhet har B11 og B12?
5. Hvorfor mangler Indre Østfold for åtte indikatorer i 14478?
6. Hvilke indikatorer bruker planleggerne faktisk? Har dere tilbakemeldinger eller brukertester siden 2020?

## 8. Hull i grunnlaget

- Siden på ssb.no `[K1]` er bare lest gjennom en oppsummering. WebFetch ville ikke gjengi teksten ordrett, så fotnotene og lenkene der er ikke kontrollert.
- Regjeringen.no-siden om arealprofiler `[K3]` og pressemeldingen om jordvernmålet `[K7]` kunne ikke hentes. Nøkkelbudskap 3 bygger på tittelen i søketreffet og på kofola.
- Metodenotatet om arealreserver `[K8]` er ikke lest. Arbeidsboka sier at metoden er endret etter 2022 og at dokumentasjonen ikke er ferdig.
- Brukertesten fra høsten 2020 `[K2]` er ikke funnet.
- Bruksvolum er ukjent, både for Tableau Public og for Excel-nedlastingen.
- Fagkontakter: Erik Engelien og Jørn Kristian Undelstvedt `[K1][K3]`. Thomas står selv som kontaktperson på siden.

## 9. Kilder

- `[K1]` SSB: «Arealprofiler 2025». Publisert 20.12.2021, sist endret 29.08.2025. https://www.ssb.no/natur-og-miljo/areal/arealprofiler (lest gjennom WebFetch 05.11.2026)
- `[K2]` Mari Olea Lie, KMD: «Arealprofiler», presentasjon på nettverkssamling for regional og kommunal planlegging, 03.12.2020. https://cms12.regjeringen.no/contentassets/158ab0e44c9d4245a70100e806d5ebfa/34_lie_kmd.pdf
- `[K3]` Jørn Kristian Undelstvedt og Erik Engelien, SSB: «Arealbruk i din kommune 2021», 20.12.2021. https://www.ssb.no/natur-og-miljo/areal/artikler/arealbruk-i-din-kommune-2021
- `[K4]` SSB, Statistikkbanken tabell 14478 og 14488 (intern), hentet som CSV 05.11.2026. Sammenligning med 2025-utgaven: `avviksrapport_arealprofiler_2026.xlsx`.
- `[K5]` SSB: Tableau-arbeidsboka vis-arealprofiler (v2, lagret 05.11.2026), forklaringstekstene under hver indikator.
- `[K6]` SSB: «Kommunal forvaltning av landbruksarealer» (kofola). Oppdatert 15.06.2026, «Om statistikken» sist oppdatert 25.11.2025. https://www.ssb.no/kofola
- `[K7]` Regjeringen.no: «Under det nye jordvernmålet på 2 000 dekar for første gang» (søketreff, siden ikke lest). https://www.regjeringen.no/no/aktuelt/under-det-nye-jordvernmalet-pa-2-000-dekar-for-forste-gang/id3165625/
- `[K8]` SSB Notat 2022/02: «Arealreserver i kommuneplaner for bolig- og næringsbebyggelse. En kartbasert analyse» (ikke lest). https://www.ssb.no/natur-og-miljo/areal/artikler/arealreserver-i-kommuneplaner-for-bolig-og-naeringsbebyggelse.en-kartbasert-analyse

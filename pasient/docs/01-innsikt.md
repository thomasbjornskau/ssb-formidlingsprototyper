Steg 1 i formidlingsprototype for pasient · versjon 1.0 · 02.11.2026 · Status: godkjent av Thomas

> **Godkjent 02.11.2026.** De fem prioriterte spørsmålene er godkjent. Diagnosekapittel er det gjennomgående valget som styrer prototypen.

# Innsikt: Pasienter i spesialisthelsetjenesten

**Merking.** `[K1]`–`[K6]`: navngitt kilde (liste nederst). `[T]`: vår tolkning. `[H]`: hypotese om misforståelse, som skal prøves i fagkontrollen.

**Om dette notatet.** Grunnlaget for prototypen av `pasient`, den første av de mindre brukte statistikkene vi tar gjennom metoden. Statistikken er ny i dagens form (publisert første gang i 2026, tall fra 2015), har én artikkel og åtte tabeller. Det gjør den til en annen test enn kpi og folkemengde: mindre tekst å lene seg på, færre etablerte misforståelser å hente fra, og mer som må utledes av tabellene selv. Alle tall i avsnitt 2 og 3 er hentet fra statistikkbanken 02.11.2026.

---

## 1. Statistikken på ett ark

| | |
|---|---|
| **Hva den er** | Antall *personer* som har fått behandling i somatisk spesialisthelsetjeneste og i psykisk helsevern for voksne, med kontakter, dagbehandlinger, døgnopphold og oppholdsdøgn. Fordelt på kjønn, alder, bosted (fylke, helseregion), aktør, diagnose (somatikk) og innvandringskategori/landbakgrunn. [K2] |
| **Hva den ikke er** | Ikke et mål på sykelighet eller behov, bare registrert bruk [K3]. Ikke ventetider, kapasitet eller kostnader (kostnader ligger i `speshelse`, tabell 14022). Dekker ikke psykisk helsevern for barn og unge eller tverrfaglig spesialisert rusbehandling (TSB) [K2]. |
| **Telleenhet** | Unike personer per gruppe. Samme person telles én gang i «i alt», men kan telles i flere diagnoser, aktører eller behandlingsnivåer. Summen av undergrupper blir derfor større enn totalen. [K2] |
| **Frekvens og referansetid** | Årlig, kalenderår. Siste publisering 22.06.2026 med 2025-tall. Neste publisering ikke fastsatt. [K1] |
| **Klassifisering** | ICD-10 (20 kapitler pluss «Annen», 200 kategoriblokker; 222 koder i alt med totalen i 14824), standard for helseregioner, fylkesinndeling, innvandringskategori. [K2] |
| **Datakilde** | Norsk pasientregister (NPR) som eneste kilde, koblet til SSBs befolkningsregister. Personer uten gyldig fødsels- eller D-nummer er utelatt. [K2] |
| **Avledede serier** | Pasienter per 1 000 innbyggere, ujustert og aldersjustert (femårsgrupper til 85+, middelfolkemengde som nevner), bare etter innvandringskategori (14823, 14827). [K2] |
| **Avrunding** | Pasienter avrundes til base 3, mengdetall (kontakter, opphold, døgn) til base 6. [K2] |
| **Revisjon** | Ikke relevant ifølge SSB. [K2] |
| **Historikk** | Dagens statistikk fra 2026, tall fra 2015. Eldre somatikkstatistikk (fra 1999) i arkivtabeller, ikke fullt sammenlignbar fordi den talte behandlinger, ikke personer. Psykisk helsevern for voksne er nytt. [K2] |
| **Tabeller** | 8: 14820–14823 (psykisk helsevern), 14824–14827 (somatikk). Alle 2015–2025. [K4] |
| **Bruk** | Allmennheten, helsemyndigheter m.fl. [K2] Bruksvolum ukjent, men statistikken er utenfor Topp20. |
| **Fagkontakter** | Jostein Starrfelt og Geir Hjemås, seksjon for helse-, omsorg- og sosialstatistikk. [K1] |

## 2. Nøkkelbudskap for 2025

1. **2 716 218 personer fikk somatisk behandling i 2025**, 16,2 % flere enn i 2015 (2 336 748). Det er omtrent halvparten av befolkningen: 484 per 1 000 innbyggere, opp fra 450. [K4: 14824, 14827]
2. **Veksten er nesten bare poliklinisk.** Polikliniske kontakter økte 26,6 % og dagbehandlinger 26,9 % fra 2015 til 2025. Antall døgnopphold var nesten uendret (897 840 → 901 848), og oppholdsdøgn falt 9,4 % (3 940 758 → 3 569 154). Gjennomsnittlig antall oppholdsdøgn per døgnopphold gikk fra 4,4 til 4,0. [K4: 14824, egen beregning `[T]`]
3. **De eldste driver veksten.** Somatiske pasienter i alderen 67–79 år økte 33,5 % og 80–89 år 42,3 %, mot 4–5 % for 0–17 og 18–29 år. Tabellene gir ikke rater per aldersgruppe, så hvor mye som er flere eldre og hvor mye som er mer bruk per eldre, krever folketallet ved siden av. [K4: 14824; `[T]`]
4. **Psykisk helsevern for voksne: 199 158 pasienter**, 7,7 % flere enn i 2015, men raten falt fra 46 til 44 per 1 000. De unge voksne skiller seg ut: 18–29 år økte 18,1 %, og kvinner 18–29 år 23,9 %. 67 år og eldre gikk ned 7,7 %. Nesten hver tredje pasient (31 %) er 18–29 år. [K4: 14820, 14823]
5. **Avtalespesialistene går hver sin vei.** I somatikk økte pasientene hos avtalespesialister 22,9 % (til 1 196 148). I psykisk helsevern falt de 18,3 % (50 997 → 41 649). [K4: 14824, 14820]
6. **Innvandringsbakgrunn snur når alderen justeres bort.** Ujustert har norskfødte med innvandrerforeldre lavest somatisk rate (394 per 1 000). Aldersjustert har de høyest (520), over befolkningen ellers (494). Innvandrere er lavest i begge (401 og 424). I psykisk helsevern har norskfødte med innvandrerforeldre høyest rate både ujustert (75) og justert (57). [K3, K4: 14823, 14827]
7. **Koronaåret er synlig, men lite.** Somatiske pasienter falt 2,4 % fra 2019 til 2020, oppholdsdøgn mer. Psykisk helsevern økte i 2020. [K3, K4]

## 3. Vanskelige begreper

**Pasient vs. kontakt vs. opphold.** En pasient er en person. I 2025 var det 2 592 768 personer med poliklinisk konsultasjon i somatikken og 9 790 080 polikliniske kontakter, i snitt 3,8 kontakter per person. Statistikken teller altså mennesker, men belastningen på sykehusene ligger i kontaktene og døgnene. `[T]`

**Unik telling.** Summen av de 20 diagnosekapitlene pluss «Annen» er 5 157 357 for 2025, nær dobbelt så mye som 2 716 218 pasienter totalt. Samme person med både diabetes og en skade telles i begge kapitlene. Det samme gjelder aktør: 2 170 281 hos helseforetak og private institusjoner pluss 1 196 148 hos avtalespesialister er 3 366 429, altså minst 650 211 personer i begge. [K2, K4: 14824; egen beregning]

**Døgnopphold vs. oppholdsdøgn.** Et døgnopphold er én innleggelse. Oppholdsdøgn er antall døgnskifter fra inn- til utskriving. 901 848 opphold ga 3 569 154 oppholdsdøgn i 2025. [K2, K4]

**Somatikk.** Alt som ikke er psykisk helsevern og rus. Somatikken inkluderer likevel diagnosekapittel V «Psykiske lidelser» (51 360 pasienter i 2025): psykiske diagnoser satt i somatiske avdelinger. `[T]`, må bekreftes.

**Det største diagnosekapitlet er ikke en sykdom.** Kapittel XXI (Z00–Z99) «Faktorer som har betydning for helsetilstand og kontakt med helsetjenesten», dvs. kontroller, oppfølging, screening og lignende, hadde 793 185 pasienter i 2025. Neste er R-kapitlet «Symptomer og tegn» (446 073). Sykdomsgrupper folk forventer, som svulster (286 419) og hjerte-kar (276 759), kommer lenger ned. [K4: 14824]

**Ujustert og aldersjustert rate.** Ujustert rate bruker gruppens faktiske alderssammensetning. Aldersjustert regner alle grupper om til en felles standardbefolkning. Innvandrere har median alder 41 år, norskfødte med innvandrerforeldre 11 år [K3]. Uten justering ser barna av innvandrere ut til å bruke lite, fordi barn generelt bruker lite.

**Hva aldersjusteringen ikke gjør.** For «i alt» er ujustert og aldersjustert rate identiske hvert år (450 og 450 i 2015, 484 og 484 i 2025). Det tyder på at standardbefolkningen er det enkelte årets egen befolkning. I så fall gjør justeringen grupper sammenlignbare innenfor et år, men fjerner ikke befolkningsaldringen i tidsserien. Økningen fra 450 til 484 er da delvis aldring. [K4: 14827; `[T]`, må bekreftes]

## 4. Sannsynlige misforståelser

| | Misforståelse | Grunnlag | Hva prototypen må gjøre |
|---|---|---|---|
| H1 | «Halve Norge er sykt.» Høyt pasienttall leses som sykdom, ikke bruk. | SSB skriver selv at bruk ikke er behov [K3]. Største diagnosekapittel er kontroller og oppfølging (Z). | Si «fikk behandling», ikke «var syke». Vis Z-kapitlet tydelig. |
| H2 | Diagnosegrupper eller aktører summeres til totalen. | Unik telling per gruppe [K2]; diagnosene summerer til 1,9× totalen. | Vis dobbelttellingen eksplisitt i lesehjelpen, aldri stablede søyler som ser ut til å summere. |
| H3 | Vekst i pasienter leses som at nordmenn blir sykere, eller at sykehusene får flere innleggelser. | Veksten er poliklinisk; døgnopphold flate, oppholdsdøgn ned [K4]. | Skill pasienter, kontakter, opphold og døgn i én graf. |
| H4 | Aldersjustert tidsserie tolkes som renset for aldring. | Identiske justerte og ujusterte tall for «i alt» [K4]. `[T]` | Bekreft med fag; forklar hva justeringen gjør og ikke gjør. |
| H5 | Lav rate for innvandrere leses som at de er friskere, eller som at de bruker «mindre enn sin del» uten aldersjustering. | SSB nevner barrierer, friske nyankomne og heterogenitet [K3]. | Vis ujustert og justert side om side, med forbeholdet om bruk vs. behov. |
| H6 | Psykisk helsevern-tallene oppfattes som hele psykiske helsetjenester. | Barn/unge, TSB, kommunale tjenester og fastlege er ikke med [K2]. | Tydelig avgrensning ved hver psykisk helse-figur. |
| H7 | Fallende rate i psykisk helsevern (46 → 44) leses som mindre psykisk uhelse, mens de unge øker kraftig. | 14820, 14823 [K4]. | Vis aldersfordelingen, ikke bare totalraten. |
| H8 | Tall avviker fra Helsedirektoratets eller FHIs NPR-tall og tolkes som feil. | Ulike variabler for behandlingstype, og SSB krever gyldig personnummer [K2]. | Kort note om sammenheng med annen statistikk. |
| H9 | Fylker sammenlignes på antall eller ujustert andel uten hensyn til alderssammensetning. `[T]` | Bosted er i tabellene, men uten rater og uten aldersjustering [K4]. | Lav prioritet; hvis med, bruk rater og et forbehold. |
| H10 | Brudd mot arkivtabellene (fra 1999) leses som reelle endringer. | Arkivet talte behandlinger, ikke personer [K2]. | Lav prioritet; nevn i «Om tallene». |

## 5. Brukere og hva de trenger

**Journalister og allmennheten** vil ha ett tall og én retning: hvor mange, flere eller færre, og hvem. De trenger hjelp til å ikke lese bruk som sykdom.

**Helsemyndigheter, planleggere og analytikere** bruker strukturen: poliklinikk vs. døgn, aldersprofil, regionale forskjeller. De har trolig også Helsedirektoratets SAMDATA og trenger å vite hvorfor SSBs tall avviker.

**Fagmiljøer på innvandrerhelse** er den gruppen SSBs egen artikkel snakker til. De trenger aldersjusterte rater og forbeholdene.

**Prototypen skal ikke være** et analyseverktøy for diagnoser på kodenivå (222 koder), et ventelisteverktøy eller en kostnadsoversikt.

## 6. Prioritering

Kriterier: (a) sentralt i SSBs egne nøkkelbudskap, (b) stor fare for misforståelse, (c) kan besvares fra statistikkbanken, (d) passer i en oversikt.

| Pri | Spørsmål | Kriterier | Hypoteser | Kilde |
|---|---|---|---|---|
| 1 | **Hvor mange får behandling, og hva er det de får?** Pasienter, kontakter, opphold og døgn 2015–2025, somatikk og psykisk helsevern. | a, b, c, d | H1, H3 | 14824, 14820 |
| 2 | **Hvem er pasientene?** Alder og kjønn, og hvordan aldringen driver veksten. | b, c, d | H3, H7 | 14824, 14820 (+ folketall 07459 for rater) |
| 3 | **Hva behandles de for?** De 20 diagnosekapitlene, med dobbelttellingen synlig. | b, c, d | H1, H2 | 14824 |
| 4 | **Bruker innvandrere og barna deres spesialisthelsetjenesten annerledes?** Ujustert og aldersjustert rate. | a, b, c, d | H4, H5 | 14823, 14827 |
| 5 | **Psykisk helsevern for voksne: hva skjer med de unge?** | b, c, d | H6, H7 | 14820, 14823 |

**Må med uansett (lesehjelpen):** pasient vs. kontakt vs. opphold; unik telling; bruk er ikke behov; hva som ikke er med (barn og unge i psykisk helsevern, TSB, kommunale tjenester).

**Kan vente:** regionale forskjeller etter fylke og helseregion (H9), avtalespesialister som egen seksjon, landbakgrunn (14822, 14826), diagnoser på underkategori.

**Utenfor:** ventetider, kostnader (14022), arkivserien fra 1999.

**Kandidat til gjennomgående valg** `[T]`: *diagnosekapittel* (somatikk). Det gir en naturlig «finn din sykdom»-inngang, slik «Min kommune» og «mitt navn» ga i tidligere prototyper, og tvinger frem dobbelttellingsforklaringen. Alternativet er *aldersgruppe*, som bærer hovedforklaringen på veksten men er mindre engasjerende. Fylke er tredje valg, men tabellene mangler rater per fylke.

## 7. Spørsmål til fagkontakten

1. Stemmer hypotesene H1–H10? Hvilke misforståelser møter dere faktisk fra brukere og presse?
2. Er standardbefolkningen i aldersjusteringen det enkelte årets egen befolkning? I så fall: er det riktig å si at den aldersjusterte tidsserien ikke er renset for befolkningsaldring?
3. Hvorfor gir statistikksidens nøkkeltabell 580 713 pasienter i somatisk døgnbehandling og 199 161 i psykisk helsevern for 2025, mens 14824 og 14820 gir 580 716 og 199 158? Avrunding i to omganger?
4. Er diagnosekapittel V (psykiske lidelser) i somatikktabellen psykiske diagnoser satt i somatiske avdelinger, og hvordan bør det forklares?
5. Hvilken befolkning er nevneren for raten i psykisk helsevern for voksne: hele befolkningen eller bare 18 år og eldre?
6. Er det greit å regne rater per fylke og aldersgruppe med folketall fra 07459, eller finnes det grunner til at SSB ikke publiserer dem?

## 8. Hull i grunnlaget

- **ssb.no lest gjennom oppsummering.** Både statistikksiden og «Om statistikken» er lest med WebFetch, som oppsummerer. Datostempelet (19.06.2026) og de siste panelene (Feilkilder, Revisjon) kom med, så teksten er trolig ikke kuttet, men ordlyden er ikke kontrollert mot originalen.
- **Artikkelen** [K3] er lest gjennom sammendrag. Tallene for innvandringsbakgrunn er kontrollert mot 14823 og 14827 og stemmer.
- **Ingen metodeartikkel** om omleggingen i 2026 er funnet. Den kan finnes.
- **Helsedirektoratets og FHIs NPR-statistikk** er ikke lest. Den trengs for H8.
- **Bruksvolum** er ikke sjekket; regnearket «Bruk av statbank» er ikke lagt ved.
- **Rater per alder og fylke** er ikke regnet. Nøkkelbudskap 3 sier derfor bare noe om antall.
- **Fagkontakt:** Jostein Starrfelt (kontakt på alle tabellene) og Geir Hjemås, begge forfattere av artikkelen.

## 9. Kilder

- [K1] SSB: Pasienter i spesialisthelsetjenesten, statistikkside, publisert 22.06.2026. https://www.ssb.no/pasient
- [K2] SSB: «Om statistikken», Pasienter i spesialisthelsetjenesten, sist oppdatert 19.06.2026. https://www.ssb.no/pasient
- [K3] Starrfelt, J. og Hjemås, G. (2026): Forskjeller i bruk av spesialisthelsetjenester etter innvandringsbakgrunn. SSB, 22.06.2026. https://www.ssb.no/helse/helsetjenester/statistikk/pasienter-pa-sykehus/artikler/forskjeller-i-bruk-av-spesialisthelsetjenester-etter-innvandringsbakgrunn
- [K4] SSB statistikkbanken, tabell 14820, 14823, 14824 og 14827, oppdatert 22.06.2026, hentet 02.11.2026. Tabell 14821, 14822, 14825 og 14826 er funnet, men ikke hentet.
- [K5] SSB statistikkbanken, tabell 14022 (kostnader, `speshelse`), brukt bare til avgrensning.
- [K6] Arkivtabeller for eldre somatikkstatistikk, nevnt i [K2], ikke lest.

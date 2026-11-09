Steg 5 i formidlingsprototype for ufore · versjon 0.1 · 09.11.2026 · Status: til faglig kontroll

# Kvalitetssikringsliste for prototypen Uføretrygdede

Prototype: https://thomasbjornskau.github.io/ssb-formidlingsprototyper/ufore/

Listen samler det som er tolkning, eget valg eller ikke bekreftet i prototypen og i notatene fra steg 1–4. **Den erstatter de tidligere listene** i `02-kvalitetssikring.md` og `04-byggenotat.md` (G1–G27) og spørsmålene i `01-innsikt.md`. Henvisningen i parentes viser hvor punktet kom fra.

Kildene `[K1]`–`[K8]` er listet i `01-innsikt.md`. Alle tall er hentet fra statistikkbanken 09.11.2026 og kontrollert ved bygging (86 kontroller, se `04-byggenotat.md`).

## A. Må avklares

Det som kan være feil, eller som gir et misvisende inntrykk hvis det er feil.

| Nr. | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 1 | Økningen på 61 031 uføretrygdede 2015–2025 deles i befolkningsvekst (om lag 23 000), aldring (11 000) og høyere andel i hver alder (27 000). «Litt over halvparten skyldes at befolkningen har vokst og blitt eldre» | Toppgrafikken, lesehjelpen | Egen beregning: snitt av alle seks rekkefølger (Shapley), celler alder × kjønn. Andre rekkefølger gir 55–58 prosent demografi (G9, G17) | Om metoden er faglig forsvarlig, og om SSB kan stå bak at den vises i en prototype med merket «egen beregning» |
| 2 | Aldersjustert indeks (landet = 100) og «andel ut fra alder og kjønn» per kommune og fylke | Min kommune, fylkesfiguren | Egen beregning: indirekte standardisering med landets andel per ettårig alder og kjønn. Summen av forventet stemmer med landets antall (G18) | Om metoden og ordene «aldersjustert indeks» og «andel ut fra alder og kjønn» er riktige og forståelige. Indeksen har ikke usikkerhetsmål, og små kommuner svinger mye |
| 3 | «En del av forskjellen skyldes at noen kommuner har eldre befolkning». Alder og kjønn forklarer om lag en firedel av forskjellene mellom kommunene | Ingressen til Min kommune | Korrelasjon 0,49 mellom faktisk og forventet andel i 2025. Dette erstattet hypotesen om at forskjellene «mest» skyldes alder (G24, H8) | Om dette stemmer med det fag vet om regionale forskjeller, og om andre forklaringer bør nevnes |
| 4 | Kommuneserier 2015–2023 er omkodet til 2025-inndeling via Klass, og andelene er egne beregninger (antall / befolkning per 1.1. året etter). Ni kommuner fra delinger har ikke tall før delingen | Min kommune, tidsserien og fylkene | Metoden gjenskaper alle publiserte andeler for 2024–2025, med unntak av Risør og Tvedestrand 2024 (avvik 0,3, trolig grensejustering). Summene stemmer med landet hvert år (G19, G20, G21) | At sammenslåtte kommuner kan summeres bakover, og om egne andeler for omkodede år kan vises på linje med publiserte |
| 5 | SSB teller alle med vedtak i løpet av året (389 023). NAV teller dem som får utbetalt ved utgangen av året (374 900). «Begge tallene er riktige» | Lesehjelpen, konseptgrafikken | NAV-siden om ulike tall [K6] og SSB-artikkelen 23.06.2026 [K3]. NAV-tallet er hentet fra SSB-artikkelen (G3, G7, G27) | At forklaringen er dekkende, og at forskjellen ikke også skyldes andre avgrensninger, for eksempel alder eller bosatte |
| 6 | Konseptgrafikken trinn 3: 12 239 som «døde eller flyttet ut» trekkes fra, slik at 401 262 blir 389 023 | Slik lages tallene | Definisjonen av ikke-registrert bosatt [K1], tabell 11824 (G4) | At gruppen bare består av døde og utflyttede |
| 7 | «Full» arbeidsintensitet betyr lønnsarbeid i alle månedene som uføretrygdet, ikke full stilling. «Uføregrad er ikke arbeidstid» | Lesehjelpen, Jobber uføre? | «Om statistikken» [K1] og artikkelen fra 2020 [K5] (G14) | At forenklingene ikke går lenger enn definisjonene, og at selvstendig næringsdrivende er riktig beskrevet som ikke med |

## B. Bør leses

Formuleringer, tolkninger og egne valg.

| Nr. | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 8 | «Bak det stabile tallet har unge og eldste gått hver sin vei» | Ingressen | 29 år: 2,1 → 4,4 prosent. 67 år: 34,4 → 28,5 prosent, tabell 11828 | Om formuleringen er rettferdig når andelen også har økt i de fleste mellomaldre |
| 9 | 29-åringer som eksempel på unge | Ingressen til Hvem er uføretrygdet? | 29 er siste alder i «unge uføre» (18–29) [K1] (G12) | Om eksemplet virker plukket. Alternativ: 18–29 samlet, 2,7 prosent |
| 10 | Andelslinjen i toppgrafikken har y-akse fra 9 til 11,5 prosent | Toppgrafikken | Diagramstandarden tillater avkortet akse når endringen er poenget (G11) | Om det overdriver økningen |
| 11 | «Mønsteret har knapt endret seg siden uførereformen» | Jobber uføre? | 75,4 prosent uten arbeid i 2015 og 75,7 i 2025, tabell 11850. Serien starter i reformåret | Om formuleringen holder når 2015 er første år |
| 12 | «Tilgangen svinger med regler og saksbehandling for AAP, som de fleste kommer fra» | Nye uføretrygdede | NAV statistikknotis juni 2026 [K7]: 81,9 prosent av nye kom fra AAP (G25) | Om NAVs forklaring kan brukes |
| 13 | «Unge som blir syke, fullfører sjeldnere videre utdanning, så sammenhengen kan gå begge veier» | Utdanning | Tolkning, støttet av SSB-artikkelen 2026 [K3] (G26) | Om formuleringen går lenger enn grunnlaget |
| 14 | Setningen om små kommuner vises under 300 uføretrygdede | Min kommune | Eget valg (G22) | Om grensen er rimelig |
| 15 | Fylkene er sortert etter indeks, ikke etter andel | Fylkesfiguren | Eget valg for å motvirke rangering etter rå andel (G23) | Om det er riktig vekt |
| 16 | «Lav» og «høy» arbeidsintensitet forklart som under og over halvparten av månedene | Jobber uføre? | «Om statistikken» [K1] | At grensen «nøyaktig halvparten» er riktig plassert |
| 17 | Konseptgrafikken: «SSB får opplysningene per person, måned for måned», og koblingene til folkeregisteret, NUDB og a-ordningen | Slik lages tallene | «Om statistikken», Produksjon [K1] (G1, G6) | Formuleringene |
| 18 | «Ikke med i statistikken»: diagnose, timer i arbeid, private uføreforsikringer uten vedtak i folketrygden | Slik lages tallene | [K1], [K5] (G8) | Om dette er de tre viktigste å nevne |
| 19 | Kommunenavn vises slik de står i statistikkbanken, med samisk og kvensk navn, for eksempel «Hábmer - Hamarøy» | Søk og kommunetekster | Tabell 11695 | Ingen faglig, men si fra om noe er feil |

## C. Spørsmål

| Nr. | Spørsmål | Grunnlag |
|---|---|---|
| 20 | Stemmer hypotesene H1–H10 om misforståelser? Hvilke møter dere oftest i henvendelser og medieomtale, og hvilke er feil? | `01-innsikt.md`, avsnitt 4. H8 er allerede justert (punkt 3) |
| 21 | Hvordan behandles personer som fyller 18 eller 67 i løpet av året, i telleren og nevneren? | Andelen per ettårig alder er gjenskapt eksakt med bosatte per 1.1. året etter, men behandlingen av endepunktene er ikke beskrevet |
| 22 | Kan en person telles som ny uføretrygdet mer enn én gang i samme år? | Definisjonen «vedtak i måned m, ikke i m–1» [K1] |
| 23 | Finnes det data om timer eller arbeidsinntekt som kan gjøre arbeidsintensitet mindre misvisende? | Punkt 7 |
| 24 | Bruker SSB selv aldersjusterte uføretall regionalt, eller anbefaler dere en annen metode? | Punkt 2. NAV publiserer aldersstandardiserte tall per fylke [K7] |
| 25 | Er Tor Morten Normann riktig fagkontakt, eller bør andre også se på kommunedelen? | Kontaktperson på statistikksiden og forfatter av alle tre artiklene [K3]–[K5] |

## Avklart underveis

| Nr. | Hva | Hvordan |
|---|---|---|
| 26 | Nevneren i andelen (G5) | Gjenskapt for alle 1 650 celler i tabell 11828 og alle 357 kommuner i 2025 med 07459 per 1.1. året etter. Ingen avvik over avrundingen |
| 27 | Dekomponeringen var avhengig av rekkefølgen (G9) | Erstattet med snittet av alle rekkefølger. Se punkt 1 |
| 28 | Påstanden fra sammendraget av SSB-artikkelen om at antallet nye uføretrygdede i 2025 var «nær tiårssnittet» | Utelatt. Stemte ikke med statistikkbanken (snitt 2015–2024 er 28 571) |
| 29 | «Sannsynligheten for å være uføretrygdet øker kraftig med alderen» | Rettet til «Andelen uføretrygdede øker kraftig med alderen» 09.11.2026. Statistikken måler andel, ikke sannsynlighet |
| 30 | Toppgrafikkvariantene B og C fra steg 2 | Ikke brukt som toppgrafikk, men innholdet er bygget inn i seksjonene om alder og arbeid |
| 31 | Teknisk, ikke fagets ansvar: befolkningen per 1.1. bruker kommuneinndelingen per 1.1., ikke statistikkårets | Uføretall og befolkning omkodes hver for seg, kontrollert mot landstallet hvert år |
| 32 | Teknisk: `naturregnskap` stopper byggekontrollen i repoet («/*__IKONER__*/») | Feilen fantes før ufore, og må rettes separat |
| 33 | Teknisk: `scripts/lag_grafikk.py` leser grafikkutkastenes rådata fra steg 2 | Ikke del av bygget |

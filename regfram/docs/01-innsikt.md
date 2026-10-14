# Innsiktsnotat: Regionale befolkningsframskrivinger

Steg 1 i formidlingsprototype for `regfram` · versjon 0.1 · 13.10.2026 · Status: utkast, ikke fagkontrollert

**Merking**

- **[K1]–[K6]** viser til en SSB-kilde i kildelista nederst.
- **[T]** er vår tolkning.
- **[H]** er en hypotese om misforståelse. Den skal prøves i fagkontrollen (steg 5).

**Om dette notatet.** Notatet er en tilbakeskuende pilot: det er skrevet etter at prototypen fantes. Prioriteringen i del 6 er gjort ut fra kildene og kriteriene som står der, ikke ut fra prototypen. Sammenligningen med prototypen kommer som eget steg når prioriteringen er godkjent.

---

## 1. Statistikken på ett ark

| | |
|---|---|
| Hva den er | Beregninger av hvordan befolkningen i kommunene utvikler seg framover, gitt forutsetninger om fruktbarhet, dødelighet, flytting, innvandring og utvandring [K1] |
| Utgangspunkt | Registrert befolkning 1. januar 2026, etter kjønn og alder [K3] |
| Horisont | Til 2050, år for år. Den nasjonale framskrivingen går til 2100 [K2] |
| Nivå | Kommuner og fylker. Fylkestallene er summen av kommunene [K5, egen kontroll] |
| Modell | BEFREG, en kohort-komponentmodell. Den bruker forutsetningene fra den nasjonale modellen BEFINN og legger til innenlands flytting [K2] |
| Alternativer | Ni i statistikkbanken (tabell 14746). Den nasjonale framskrivingen har femten (tabell 14740) [K5] |
| Publisering | 12. juni 2026, med neste oppdatering foreløpig ikke fastsatt [K1]. Forrige runde var juni 2024 [K6]. Det tyder på at statistikken lages annethvert år [T] |
| Kontakt | Stefan Leknes og Sturla A. Løkken [K3] |
| Bruk | Planlegging av helse- og omsorgskapasitet, skoleplasser, bolig og areal, og infrastruktur [K4 s. 14–15] |
| Bruksvolum | Nr. 26 blant statistikkene etter uttak fra statistikkbanken i 2026, med 8 952 uttak (regnearket «Bruk av statbank») |

## 2. Nøkkelbudskap (hovedalternativet)

1. **Vi blir flere.** Befolkningen vokser om lag 10 prosent fra 2026 til 2050 [K4 s. 7].
2. **Veksten samles i sentrale strøk.** Akershus vokser 20 prosent og Oslo 16 prosent [K3]. Alle kommuner i de tre mest sentrale sentralitetsklassene vokser. Andelen som bor i de mest sentrale klassene, øker fra 71,5 til 73,9 prosent [K4 s. 10].
3. **Nordland er det eneste fylket som krymper**, med −3,0 prosent [K1, tabell 1].
4. **To av tre kommuner vokser.** Det gjelder 224 kommuner, eller 63 prosent [K4 s. 8]. De øvrige 133 krymper.
5. **Befolkningen eldes overalt.** Andelen 70 år og eldre i kommunene går fra 9–26 prosent i 2026 til 15–32 prosent i 2050 [K4 s. 11].
6. **Fødselsoverskuddet forsvinner.** I 2050 har bare Oslo og Rogaland flere fødte enn døde blant fylkene [K3]. Fem fylker har fødselsunderskudd allerede i 2026 [K4 s. 12].
7. **Innvandringen de siste årene endrer ikke hovedmønstrene.** Det gjelder også bosettingen av ukrainere over hele landet [K3].
8. **Usikkerheten øker jo lenger fram i tid og jo mindre området er** [K2], [K4 s. 14–15].

## 3. Vanskelige begreper

- **Framskriving.** SSB beskriver det som hva som skjer dersom forutsetningene slår til [K2]. Forskjellen fra en prognose er ikke forklart eksplisitt i kildene vi har lest [T].
- **Alternativkodene.** Fire bokstaver står for fruktbarhet, levealder, innenlands flytting og innvandring, i den rekkefølgen. M er middels, L lav, H høy og 0 null [K2], [K4 vedlegg A]. Den nasjonale framskrivingen bruker tre bokstaver og egne koder som MME og MKM [K5]. Det er to kodesett for det som ser ut som samme ting [T].
- **Lav og høy nasjonal vekst (LLML/HHMH).** Disse varierer bare forutsetninger på nasjonalt nivå. Innenlands flytting har ingen høy- eller lavvariant. Spennet kan derfor undervurdere usikkerheten for kommunene [K4 s. 14–15 og 30–34]. Spennet er ikke et konfidensintervall [T].
- **Komponentene.** Fødselsoverskudd, nettoinnvandring og innenlands nettoinnflytting. Flytting telles bare som endret bosted fra starten til slutten av året [K4 s. 30].
- **Sentralitetsklasser 1–6** er SSBs sentralitetsindeks [K4 s. 10]. Tabell 14746 har en egen kodeliste for sentralitet [K5].
- **«Hele landet» i den regionale tabellen er ikke den nasjonale framskrivingen.** For 2050 gir den regionale tabellen 6 195 859, mens den nasjonale gir 6 214 071, en forskjell på 18 212 [K5, egen beregning]. Forklaringen er at det er to modeller, slik at sum av kommuner og nasjonalt tall ikke trenger å være like [K2], [K4 s. 42].

## 4. Sannsynlige misforståelser

Alle punktene er hypoteser [H] til fagkontakten har vurdert dem.

| | Misforståelse | Grunnlag | Hva prototypen må gjøre |
|---|---|---|---|
| H1 | Framskrivingen leses som prognose: «Bodø får 54 358 innbyggere i 2050» | SSB understreker at det er scenarioberegninger [K2], [K4 s. 15]. Tall gitt med presisjon til én person inviterer til fasitlesning [T] | Bruke hvis-språk, vise spenn og vurdere avrunding i tekst |
| H2 | Spennet mellom lav og høy leses som sikkerhetsmargin | SSB sier spennet kan undervurdere den faktiske usikkerheten [K4] | Si eksplisitt hva spennet er og ikke er |
| H3 | Store prosentendringer i små kommuner leses som trender | Små bevegelser gir store prosentvise utslag [K4 s. 9]. Utsira har 219 innbyggere og +43,8 prosent [K5] | Varsle om små tall og ikke rangere på prosent alene |
| H4 | To ulike «Norge i 2050»-tall svekker tilliten | 6 214 071 nasjonalt mot 6 195 859 regionalt [K5]. Avviket er forklart i [K2], men ikke synlig der tallene vises [T] | Forklare kort hvor tallet for hele landet kommer fra |
| H5 | Alternativkodene misforstås, for eksempel at MMMM og MMM er det samme | To kodesett [K5] [T] | Bruke navn foran koder og forklare koder én gang |
| H6 | Brukere tror lokale planer er med, som nye boligfelt, arbeidsplasser eller mottak | Slike forhold inngår ikke før de finnes i observerte trender [K2], [K4 s. 15] | Lage en «dette er ikke med»-boks |
| H7 | Nedgang forklares med utflytting alene | Aldring svekker fødselsoverskuddet [K3]. Innlandet har størst fødselsunderskudd, −30 000 [K4 s. 7–8] [T] | Vise komponentene side om side |
| H8 | En revisjon mellom rundene leses som at «SSB tok feil» | 2050-tallet er 81 000 høyere enn i 2024-framskrivingen [K4 s. 13] [T] | Lav prioritet. Mulig fotnote |
| H9 | Ulike grenser for «eldre» gir tall som ikke stemmer med SSBs omtale | Rapporten bruker 70+ [K4 s. 11]. Statistikkbankens grupperinger tilbyr 67+ og 80+ [K5] [T] | Bruke 70+ som SSB, eller begrunne et annet valg |

## 5. Brukere og hva de trenger [T]

- **Kommunale og regionale planleggere.** Dette er primærbrukerne ifølge [K4]. De trenger sin egen kommune, aldersgrupper og årstall, og vil sannsynligvis hente selve tallene i statistikkbanken.
- **Journalister.** De trenger hvilke kommuner som vokser og krymper, og et sitat om usikkerheten.
- **Politikere og innbyggere.** De vil vite om kommunen sin vokser, og om den blir eldre.

En oversiktsprototype skal ikke erstatte statistikkbanken for planleggere. Den skal gi riktig førsteinntrykk og sende dem videre [T].

## 6. Prioritering: spørsmål prototypen bør svare på

**Kriterier:**

- (a) Spørsmålet er sentralt i SSBs egne nøkkelbudskap.
- (b) Faren for misforståelse er stor.
- (c) Spørsmålet kan besvares med tall fra statistikkbanken.
- (d) Det passer i en oversikt, ikke et analyseverktøy.

| Prioritet | Spørsmål | Kriterier | Hypoteser | Mulig kilde (verifiseres i steg 3) |
|---|---|---|---|---|
| 1 | Hvor mange blir vi, og hvor sikkert er det? | a b c d | H1 H2 H4 | 14746, ev. 14740 for nasjonalt tall |
| 2 | Hvor vokser og hvor krymper det, og hvor sterk er sentraliseringen? | a b c d | H3 | 14746 med fylker, kommuner og sentralitetskodeliste |
| 3 | Hvorfor: fødte, døde, flytting og innvandring? | a b c | H7 | 14747 |
| 4 | Hvor raskt eldes befolkningen? | a c d | H9 | 14746 med aldersgrupper |
| 5 | Hva skjer i min kommune? | c d | H3 H6 | 14746 og 14747 per kommune |

**Må med uansett:** en kort «Slik leser du en framskriving»-boks som dekker H1, H2, H5 og H6, og en linje om tallet for hele landet (H4).

**Kan vente:** alternativene utover lav og høy nasjonal vekst (sterk og svak aldring, ingen flytting), kjønn og revisjonen fra 2024 (H8).

**Utenfor:** innvandrerbakgrunn, som bare finnes i den nasjonale framskrivingen [K5], og de detaljerte forutsetningene om fruktbarhet og dødelighet.

## 7. Spørsmål vi tar med til fagkontakten (grunnlag for steg 5)

1. Stemmer H1–H9? Hvilke misforståelser møter dere oftest?
2. Hvordan vil dere at avviket mellom nasjonalt og regionalt tall (H4) forklares?
3. Er det riktig å bruke 70+ som grense for «eldre», slik rapporten gjør?
4. Bør tall for små kommuner avrundes eller merkes, og fra hvilken størrelse?
5. Er det greit å vise lav og høy nasjonal vekst som et skravert spenn, og hvordan bør det beskrives?
6. Finnes det en «Om statistikken»-side eller ofte stilte spørsmål vi bør lenke til?

## Hull i grunnlaget

- **«Om statistikken»:** seksjonen lot seg ikke lese fra statistikksiden, så definisjonene der er ikke sjekket.
- **Ofte stilte spørsmål:** ingen side med det er lenket fra emnesiden.
- **Media:** ingen gjennomgang av mediebruk er gjort. Hypotesene bygger på SSBs egne tekster og våre tolkninger.
- **Rapporten:** [K4] er lest gjennom et sammendragsverktøy. Sidetallene bør sjekkes mot PDF-en før notatet brukes eksternt.

## Kilder

- [K1] SSB: Regionale befolkningsframskrivinger, statistikkside, oppdatert 12.06.2026. https://www.ssb.no/regfram
- [K2] Tømmerås, Løkken og Leknes: «Slik lager SSB befolkningsframskrivinger», 12.06.2026. https://www.ssb.no/befolkning/befolkningsframskrivinger/artikler/slik-lager-ssb-befolkningsframskrivinger
- [K3] Leknes og Løkken: «Befolkningsframskrivinger for kommunene 2026», 12.06.2026. https://www.ssb.no/befolkning/befolkningsframskrivinger/artikler/befolkningsframskrivinger-for-kommunene-2026
- [K4] Leknes og Løkken: Befolkningsframskrivinger for kommunene 2026. Rapporter 2026/22 (PDF, lenket fra [K3])
- [K5] Statistikkbanken, tabell 14746 og 14740 (metadata og data hentet 13.10.2026)
- [K6] SSB: emnesiden Befolkningsframskrivinger, med artikkellisten. https://www.ssb.no/befolkning/befolkningsframskrivinger

Steg 4 i formidlingsprototype for innvbef-omrade · versjon 0.1 · 11.11.2026 · Status: utkast

# Byggenotat: Innvandrere og norskfødte med innvandrerforeldre i kommunene (innvbef-omrade)

En variant av [`innvbef`](../../innvbef/), bestilt av Thomas 11.11.2026: kommune eller fylke er hovedvalget, og siden har et kart. Landbakgrunn er et valg for kartet, ikke for hele siden (valgt av Thomas samme dag). Innsikten, konseptgrafikken og kvalitetssikringen fra steg 1–2 i `innvbef` gjelder også her. Konseptgrafikken er kopiert uendret.

Malen bygger på `innvbef` (CSS, verktøy, søk) og kartet i `arealprofiler` (projeksjon, forenkling, piltaster). Siden er én fil på 1,58 MB, og to bygg gir identisk fil. Testet i Chromium i 1280 og 390 px uten feil i konsollen og uten horisontal rulling.

## 1. Kilder og struktur

| Datasett | Tabell | Innhold | Brukt i |
|---|---|---|---|
| `landet_tid`, `landet_bef` | 05182, 05803 | Hele landet 1970–2026, innvandrere og norskfødte hver for seg | Toppgrafikk for hele landet |
| `komm_tid`, `fylke_tid` | 07108 | Innvandrere og norskfødte **samlet** etter verdensdel, kommuner og fylker 2024 med **sammenslåtte tidsserier**, 1970, 1980, 1986–2026 | Toppgrafikk, verdensdeler, sammenligning |
| `komm_bef`, `fylke_bef` | 07459 | Folketall med sammenslåtte tidsserier, 1986–2026 | Andeler |
| `komm_delt`, `fylke_delt` | 09817 | Innvandrere og norskfødte hver for seg, ikke sammenslått | «Hvem bor her», kartet |
| `komm_land`, `fylke_land` | 09817 | Per landbakgrunn, 2026 | Kartet for valgt land, landbakgrunner i området |
| Kart | robhop/fylker-og-kommuner | Kommunegrenser 2024 fra Kartverket, kopiert fra `arealprofiler` | Kartet |

**Funn som former siden:**

- Den sammenslåtte tidsserien i 07108 finnes bare for innvandrere og norskfødte samlet. Hver for seg finnes de bare i 09817, uten sammenslåing: alle kommuner fra 2024, noen fra 2010. Toppgrafikken for kommuner og fylker viser derfor gruppene samlet, og skillet vises bare for 2026.
- Folketall per kommune finnes fra 1986. Andelen vises derfor fra 1986, antallet fra 1970.
- Seks kommuner kan ikke følges hele veien, fordi de er satt sammen av deler av kommuner som ble delt. Heim, Hitra, Orkland, Narvik og Hamarøy har tall fra 2020. Haram mangler 2020–2023, da den var en del av Ålesund. Personene ligger i restkoden «Delte kommuner og uoppgitt». Hullene vises skravert som «Kan ikke følges», ikke som null.
- 09817 har 213 landbakgrunner med personer i 2026 (13880 i `innvbef` har 215). Tallene per land for hele landet er summen av fylkene.

## 2. Hva som er bygget

| Del | Svarer på | Innhold |
|---|---|---|
| Hode | – | Ingress generert fra tallene, søk etter kommune eller fylke (også tidligere kommunenavn fra Klass, for eksempel Skedsmo, og tospråklige navn som Tråante), «Se alle kommuner» etter fylke med andelen ved hvert navn, «Vis hele landet», sju eksempler, også ett uten treff (Atlantis) |
| Kort for valgt område | – | Fylke som lenke, kommunenummer, innbyggere, innvandrere og norskfødte med andel, rangering blant 357 kommuner, tekst om hull i serien, søkeordet som ga treffet, varsel under 2 000 innbyggere |
| Lesehjelpen | H1, H2, H6, H7 | Fødested, ikke pass. To grupper, ikke én (tall for området). Andel og antall forteller ulike historier (flest og høyest andel). Registrert bosatt. Konseptgrafikken i «Slik lages tallene» |
| Toppgrafikk | 2 | Stort avrundet tall, setning som sammenligner andelen med landet, fire nøkkeltall. Bryter **Antall** (linje, prikket før 1986; for landet to linjer) og **Andel av innbyggerne** (stablet areal til 100 prosent med øvrig befolkning, fra 1986, med landet som stiplet linje) |
| Hvor bor de? (kartet) | 4 | Koroplet over alle kommuner med fem kvintilklasser og egen klasse for «Ingen». Brytere for innvandrere, norskfødte eller begge, og søk etter landbakgrunn (med synonymer fra `innvbef`). Kartet zoomer til fylket for valgt kommune eller fylke, med knapp for hele landet. Valgt kommune har oker kant. Ved siden av: de ti med høyest andel i utsnittet, valgt kommune lagt til, og landet som strek |
| Hvem bor i …? | 1, 3 | Andel innvandrere og norskfødte i området, fylket og landet, med andelen av gruppen som er født i Norge i overskriften. Verdensdeler 1970–2026 som stablet areal |
| Hvor kommer de fra? | 3 | De 15 største landbakgrunnene i området, delt i innvandrere og norskfødte. En rad setter landet på kartet |
| Sammenligning | 4 | Kommunene i fylket (eller fylkene) med andel 2016 og 2026 som prikker. Over 20 kommuner: ti høyeste, fem laveste og valgt kommune |
| Bunntekst | – | Om tallene, egne beregninger, kilder, kartkilde, hentedato og lenke til `innvbef` |

Valgt område og kartland ligger i adressen: `#omrade=1835&land=131`. Søkefeltene følger adressen. Kartet kan brukes med piltastene (neste og forrige kommune), og alle rader i listene kan velges med tastatur.

## 3. Kontroller

`lag_data.py` stopper bygget med «Kontroll feilet: …». Negativ test: Halden, Europa, 1970 ble økt med 5 i `komm_tid.json`, og bygget stoppet med «07108 1970, verdensdel 1: kommunene summerer til 5 mer enn fylkene». Filen ble satt tilbake og er byte for byte lik originalen.

Den første negative testen (+500 i samme celle) gikk **ikke** gjennom kontrollen. 1970 avvek allerede med −208 mot landet, så +500 ga +292, innenfor toleransen på 350. Derfor ble den eksakte kontrollen mellom kommuner og fylker lagt til.

| Kontroll | Toleranse | Største faktiske avvik |
|---|---|---|
| 07108: kommuner (med restkoder) = fylker (med restkoder), per verdensdel og år | 0 | 0 |
| 07108: alle regioner = landet i 05182 | 350 før 1988, ellers 40 | 314 (1987) |
| 07108: kommunene i hvert fylke = fylket, fra 2024 | 40 | 0 |
| 07108 = 09817 per kommune, 2026 | 3 | 1 |
| 07459: kommuner og fylker = landet i 05803, alle år | 0 | 0 |
| 07459 mangler folketall ⇒ 07108 har ingen personer samme år | 0 | 0 |
| 09817: sum av land = «Alle land», per kommune og fylke | 5 | 3 |
| 09817: publisert andel = antall / 07459, 2026 | 0,011 prosentpoeng | 0 |
| Kartet og tabellene har de samme 357 kommunene | 0 | 0 |
| Synonymer peker på kommuner og land som finnes | 0 | 0 |

## 4. Nye valg til kvalitetssikring

Nummerert videre fra B1–B11 i `innvbef/docs/04-byggenotat.md`.

| # | Valg eller påstand | Grunnlag | Må sjekkes |
|---|---|---|---|
| C1 | Toppgrafikken for kommuner og fylker viser innvandrere og norskfødte samlet, fordi bare den serien er sammenslått | 07108 | Fag: finnes en sammenslått serie hver for seg? |
| C2 | Kartet bruker kvintiler blant kommunene med personer i gruppen, og «Ingen» som egen klasse | Diagramstandarden, eget valg | – |
| C3 | Andel per kommune for valgt land, for norskfødte og for begge er egne beregninger mot 07459 | Egen beregning | Fag |
| C4 | Tall per land for hele landet er summen av fylkene i 09817, ikke tallet i 13880 | Egen beregning | Avvik fra `innvbef` på inntil 3 per land |
| C5 | Verdensdelene er slått sammen til fem: Europa, Asia, Afrika, Amerika og «Oseania, statsløse og uoppgitt». Europa omfatter Tyrkia, Russland og Ukraina | 07108, eget valg | Fag: ønsker dere SSBs grupper? |
| C6 | Teksten «Kan ikke følges» og forklaringen om delte kommuner | 07108, 07459 | Fag: ordbruk |
| C7 | Tospråklige fylkesnavn er forkortet til det norske navnet i løpende tekst (Nordland, Troms). Kommunenavn er beholdt offisielle, unntatt Oslo | Eget valg | Språkrådet/fag |
| C8 | Prosentvis vekst vises bare når utgangspunktet er minst 500 personer | Eget valg | – |
| C9 | Kartgrunnlaget er robhop/fylker-og-kommuner, ikke en SSB-kilde | Samme som Q35 i `arealprofiler` | Lisens, og om SSB har et eget forenklet kart |

## 5. Kjente svakheter

- Kartet kan brukes med piltaster, men kommunene kan ikke nås én og én med Tab. Den fulle tabellen under kartet og søket er alternativene.
- Befolkningsregnskap og botid per kommune er ikke med. 10598 har botid per fylke, men ikke per kommune.
- Oslo-bydeler er ikke med.
- Den samlede siden er 1,58 MB, mest tidsseriene per verdensdel (07108) og kartstiene (237 kB).

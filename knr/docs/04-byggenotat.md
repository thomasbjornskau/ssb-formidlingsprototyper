Steg 4 i formidlingsprototype for knr · versjon 1.0 · 21.10.2026 · Status: utkast

# Byggenotat: Nasjonalregnskap (knr)

Bygger på `03-kildekart.md` (dataomfang B: makro og næring) og toppgrafikk D fra steg 2. Malen tar CSS, figurfunksjoner og søk fra `folkemengde`. Siden er én fil på 986 kB, og to bygg gir identisk fil.

## 1. Hva som er bygget

| Del | Svarer på | Innhold |
|---|---|---|
| Hode | – | Ingress generert fra tallene, søk blant 51 makrostørrelser med 23 synonymer, «Se alle 51 størrelser» (liste med innrykk som i statistikkbanken) og fem eksempler |
| Kort for valgt størrelse | – | Sti opp i hierarkiet som lenker, nivå i milliarder kroner, andel av BNP, volumendring siste år, søkeordet som ga treffet og undergrupper. Varsel for størrelser under 50 milliarder kroner |
| Lesehjelpen | H1–H4 | Fire punkter: Fastlands-BNP er hovedtallet, kroner er ikke volum, samme kvartal gir flere veksttall, tallene endres. Generert fra tallene. Konseptgrafikken ligger i «Slik lages tallene» |
| Toppgrafikk | 1 | Variant D for valgt størrelse: stort tall, årlig volumvekst 1971–siste år som stolper, streken for Fastlands-BNP (eller BNP når Fastlands-BNP er valgt), foreløpige år lyse, fire nøkkeltall |
| Hvor fort vokser økonomien nå? | 1, 4 | «Fire tall»: valgt størrelse og referansen, fra forrige kvartal (sesongjustert) og fra samme kvartal i fjor (ujustert). Stolper for de siste 16 kvartalene med bryter mellom de to målene |
| BNP, Fastlands-BNP og olje og gass | 2 | Oljeandelen av BNP 1970–siste år. Kroner mot volum for valgt størrelse de siste 30 årene |
| Hva driver veksten? | 3 | Anvendelsen av BNP siste år i milliarder kroner, med valgt størrelse uthevet. Volumvekst for 24 næringer, siste år eller siste kvartal (bryter) |
| Hvor sikre er tallene? | 4 | Fastlands-BNP per måned de siste 24 månedene, med tremånederssummen som strek. Hovedrevisjonen i 2025 for sju hovedstørrelser |
| Bunntekst | – | Om tallene, egne beregninger, kilder og hentedato |

Alle figurer har «Vis tallene» og kildelinje med tabellnummer og oppdateringsdato fra json-stat-svaret. Valgt størrelse ligger i adressen (`#storrelse=koh.nrpriv`). Søkeforslagene og bryterne kan brukes med tastatur.

## 2. Hvordan hull i data vises

- **Endringsrate mangler** (første år, og år der nivået er null eller skifter fortegn): stolpen utelates, og tabellen og tipset sier «ikke beregnet». I næringsfiguren står «ikke beregnet» ved navnet.
- **Nivået er null eller negativt** (lagerendring og statistiske avvik): figuren for kroner mot volum erstattes av en tekst og en tabell med nivået. Kvartalsfiguren beholder SSBs publiserte rater, men noten advarer om at de ikke kan leses som vekst. Kortet viser varselet om små størrelser.
- **Lange navn i smal visning**: næringsnavnene kortes inn med «…». Hele navnet står i tipset og i «Vis tallene».
- **Revisjonen**: tallene står ikke i statistikkbanken og er skrevet inn fra artikkelen 13.11.2025. Kildelinjen sier det.

## 3. Kontroller

`lag_data.py` stopper bygget med «Kontroll feilet: …». Negativ test: én verdi i `makro_aar.json` (celle 5000) ble endret, og bygget stoppet i K4b. Filen ble satt tilbake og er identisk med originalen.

| Kontroll | Toleranse | Største faktiske avvik |
|---|---|---|
| K1 Anvendelsessiden = BNP, løpende priser | 15 millioner | 11 millioner |
| K2, K3 Produksjonssiden = BNP | 0 | 0 |
| K4 Årlig volum fra faste priser = publisert, fire hovedstørrelser | 0,05 prosentpoeng | 220 av 220 treff |
| K4b Samme for alle størrelser | 0,15, eller nivå under 50 milliarder | Innenfor |
| K5 Kvartalsvekst fra sesongjusterte nivåer = publisert, BNP og Fastlands-BNP | 0,05 | 0 |
| K6 Sum av kvartaler = årstall | 8 millioner | 6 millioner (BNP 2012) |
| K9 Tremånederssum i siste måned i kvartalet = kvartalsvekst | 0,15 | 0 |
| K10 Toppnæringer = totalen, og totalen minus olje og sjøfart = Fastlands-Norge | 5 millioner | 3 millioner |
| K11 Fastlands-Norge i 09170 = 09189 | 0 | 0 |
| Nøkkeltall: BNP 2025 = 5 511 334, Fastlands-BNP 2. kvartal 2026 = +0,3 | 0 | 0 |
| Synonymer peker på koder som finnes | 0 | 0 |

## 4. Nye valg til kvalitetssikring

Nummerert videre fra `02-kvalitetssikring.md` (T13).

| # | Valg eller påstand | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| B1 | Referansestreken er Fastlands-BNP for alle størrelser, og BNP når Fastlands-BNP er valgt | Eget valg, utvidet fra T13 | Om streken gir mening for små størrelser som eksport av tjenester |
| B2 | Kortet viser andel av BNP for alle størrelser, også import og eksport | Regnet av oss | Om andel av BNP er misvisende for import, eksport og samlet sluttanvendelse |
| B3 | «Kroner mot volum»: verdiendringen er regnet av oss fra løpende priser. Noten sier «Forskjellen er i hovedsak prisendring» | 09189. SSBs prisendring står i tabellen | Om formuleringen holder, gitt kjedingen |
| B4 | Når nivået er null eller negativt, vises ingen prosentvis endring i kroner mot volum. Kvartalsfiguren viser SSBs publiserte rater med advarsel | Eget valg | Om SSB bør vise rater for lagerendring i det hele tatt |
| B5 | Fire synonymer er merket usikre: boligbygging, turisme, handel med utlandet, offentlig pengebruk | `data/synonymer.json` | Om kodene er de riktige |
| B6 | Varsel om små størrelser under 50 milliarder kroner | Eget valg, samme grense som K4b | Om grensen er rimelig |
| B7 | Næringsfiguren viser bruttoprodukt i basisverdi. Totalen for Fastlands-Norge (+1,8 i 2025) avviker derfor fra Fastlands-BNP i markedsverdi (+1,7) | 09170 og 09189 | Om forskjellen bør forklares mer |
| B8 | Nedgang vises i oker i nærings- og revisjonsfiguren | Diagramstandarden | Ingen |
| B9 | Revisjonsfiguren: «Den største enkeltendringen var boligtjenester fra selveide boliger» | `[K4]` | Om dette gjelder nivå eller andel av endringen (rettet i steg 1) |
| B10 | Månedsfiguren viser 24 måneder. Overskriften gir spennet i månedsendringen | 11721 | Om månedstallene bør vises uten tremånederssummen |
| B11 | Lesehjelp 2 og «Fire tall» bruker ujustert endring fra samme kvartal i fjor | 09190 | Ingen |

## 5. Kjente svakheter

- «Om statistikken» er ikke lest (hull H1 i kildekartet). Formuleringene i lesehjelpen og konseptgrafikken er ikke sjekket mot SSBs egen dokumentasjon.
- Hierarkiet i makrostørrelsene er vist med innrykk, ikke kontrollert som summerende tre (H4).
- Revisjonen er bare hovedrevisjonen. Revisjoner mellom publiseringer finnes ikke som tidsserie (H2).
- Figurfunksjonene er kopiert fra folkemengde og utvidet (`linjer` med direkte etiketter og punkter, `liggende` med innkorting). De bør flyttes til `felles/` når neste prototype trenger dem.

# Kvalitetssikring (kpi)

Samlet liste over det i prototypen som er tolkning, eget valg eller ikke bekreftet. Grunnlag for fagkontrollen i steg 5. Listen erstatter `02-kvalitetssikring.md` og punktene i `04-byggenotat.md`.

**Prioritet.** A må avklares før prototypen deles videre. B bør leses. C er spørsmål der svaret kan forbedre prototypen.

## A. Må avklares

| | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 1 | «Ikke med i KPI: renter og avdrag på lån» | Konseptgrafikken | Ikke sagt uttrykkelig i artikkelen om bokostnader. FISIM ble tatt ut av KPI i 2015 | Stemmer det, og er formuleringen presis? |
| 2 | «Strømstøtten regnes som en negativ avgift og trekker indeksen ned. Hvordan Norgespris inngår, er ikke avklart.» | Kortet for strøm (`04.5.1`) | NOU 2026:5, kapittel 3 | Riktig? Og hvordan inngår Norgespris? |
| 3 | «KPI-JA er nå 1,8 prosentpoeng høyere enn KPI. Det betyr at endringer i avgifter har trukket prisveksten i KPI ned.» | Hvorfor flere KPI-er? | Følger av definisjonen av KPI-JA | Riktig forklaring? Hvorfor har gapet økt gjennom 2026? |
| 4 | Bidrag til prisveksten regnet av oss med SSBs metode, i to ledd før og etter desember. Også for grupper på andre og tredje nivå | Hva driver prisveksten? og kortene | Nygaard (2017). Gjenskaper publisert vekst innenfor 0,16 prosentpoeng fra 2017 | Er metoden riktig brukt? Har SSB egne bidragstall vi kan sammenligne med? |
| 5 | «Bidragene summerer til 3,43 prosentpoeng. Publisert tolvmånedersvekst er 3,4. Forskjellen skyldes at indeksene er avrundet til én desimal.» | Under bidragsfiguren | Egen beregning | Er forklaringen god nok, eller bør bidragene skaleres? |
| 6 | 26 grupper har vekt, men ingen indeks. Kortet sier «SSB publiserer ikke prisindeks for denne gruppen» | Kortet, for eksempel restauranter og kaféer (`11.1.1`) | Tabell 14700 | Hvorfor mangler indeksen (konfidensialitet, kvalitet, nytt)? Bør vi si mer? |

## B. Bør leses

| | Påstand eller valg | Hvor | Grunnlag | Hva må sjekkes |
|---|---|---|---|---|
| 7 | Datakildene: strekkoder fra dagligvarebutikker, apotek og bensinstasjoner, knapt 2 000 virksomheter, om lag 2 500 utleieboliger, strøm fra nettet, biler fra OFV | Konseptgrafikken | «Om statistikken» | Oppdatert og dekkende? |
| 8 | «Samme vare sammenlignes over tid. Tilbud og rabatter er med.» | Konseptgrafikken | Artikkelen om matvareindeksen (2022) | Gjelder dette alle grupper? |
| 9 | Eksempelet 30,00 kr til 31,20 kr | Konseptgrafikken | Vårt valg, merket som eksempeltall | Villedende når mat beregnes med multilateral metode? |
| 10 | De fire punktene i «Slik leser du KPI» | Øverst | Hypotesene H1–H7 | Er de riktige og de viktigste? |
| 11 | Beskrivelsen av de åtte seriene, for eksempel «Uten priser som i stor grad fastsettes av myndighetene» for KPI-XADM | Hvorfor flere KPI-er? | Navnene i tabell 14706 og «Om statistikken». Formuleringene er våre | Presise nok? |
| 12 | KPI-JAE omtalt som «underliggende prisvekst», og som den Norges Bank legger vekt på | Toppgrafikken og ingressen til seksjonen | NOU 2026:5 | Bruker SSB selv denne betegnelsen? |
| 13 | Beregnet husleie forklart som «hva det ville kostet å leie en tilsvarende bolig» | Kortene for `04.2` og `04.2.1` | «Hvordan fanges bokostnader opp i KPI?» (2024) | Presist nok? |
| 14 | Bolig og strøm økte fra 25,3 til 31,2 prosent av vektene i 2026, nesten bare beregnet husleie, «etter revisjonen av nasjonalregnskapet» | Under vektfiguren | Tabell 14700 og «Om statistikken» | Riktig årsak? |
| 15 | Kortnavn for hovedgruppene, for eksempel «Bolig og strøm» og «Restaurant og overnatting». Fulle navn i kort, verktøytips og tabeller | Figurene | Vårt valg | Akseptable? |
| 16 | Varighetskodene IV, HV, V og T vist som ikke-varig vare, halvvarig vare, varig vare og tjeneste | Kortene | Tolket fra etikettene i tabell 14700 | Riktig tolkning? |
| 17 | 109 søkeord som ikke står i gruppenavnene, for eksempel strøm, cola og frisør. 12 er merket usikre: barnehage, SFO, strømmetjeneste, trening, treningssenter, taxi, bompenger, parkering, skinke, taco, brunost og fiskepinner | Søket | `data/synonymer.json` | Er koblingene riktige? Hvor ligger barnehage og SFO? |
| 18 | Pengeverdi: 100 kroner i september 2015 tilsvarer 142 kroner nå. Regnet fra indeks med én desimal | Toppgrafikken og «Hva er en krone verdt» | Tabell 14700 og 14710 | Gir priskalkulatoren samme svar? Er avrundingen for årene rundt 1920 et problem? |
| 19 | Tabellvalget: 14700, 14706 og 14710 | Hele prototypen | `03-kildekart.md` | Riktige tabeller? |

## C. Spørsmål fra innsikten

| | Spørsmål | Grunnlag |
|---|---|---|
| 20 | Stemmer hypotesene H1–H10, og hvilke misforståelser møter dere oftest? | `01-innsikt.md`, del 4 |
| 21 | Bør KPI eller KPI-JAE være hovedtallet på en formidlingsside? Prototypen bruker KPI, med KPI-JAE ved siden av | `01-innsikt.md`, del 7 |
| 22 | Bør målefeilen i KPI omtales (H10)? Prototypen nevner den ikke | `01-innsikt.md`, del 4 |
| 23 | Finnes det ofte stilte spørsmål eller henvendelser vi bør bygge på? | |
| 24 | Hvem er riktig fagkontakt for prototypen? | «Om statistikken» viser bare et telefonnummer |

## Avklart underveis

- Bidrag som grovt anslag (vekt × endring) i steg 2 er erstattet av SSBs metode.
- Tolvmånedersendringer vises som publisert, ikke regnet fra indeksene.
- Rådataene er rekonstruert fra svar hentet gjennom SSB-tilkoblingen. `hent_data.py` er ikke kjørt direkte mot API-et. Dette er en teknisk sak for oss, ikke for fagkontakten.

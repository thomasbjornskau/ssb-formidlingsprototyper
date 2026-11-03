# Byggenotat, steg 4 (regfram)

Versjon 0.3 av prototypen, 03.11.2026 (0.2: 14.10.2026). Bygget fra `src/index.template.html` og `data/raw/` med `felles/bygg.py`.

## Endret i versjon 0.3, etter møte i fagseksjonen 02.11.2026

| Innspill fra fag | Løsning |
|---|---|
| Figurer etter valgt nivå | Kartet zoomer til fylket. Prikkfiguren farger kommunene i fylket grønne og resten grå. Sentralitet vises innenfor fylket. Eldrefiguren viser kommunene i fylket i stedet for fylkene. Oslo, som er både fylke og kommune, har egne overskrifter |
| Kart | Koropletkart over endring 2026–2050 per kommune, seks klasser i blå–oker uten midtpunkt (oker = nedgang, blå = vekst). Kommunegrenser 2024 fra Kartverket, forenklet til 126 kB. Klikk velger kommunen. Overskriften gjelder kommuner med minst 2 000 innbyggere |
| «Slik lages tallene» | Ikke endret. Foreslått som eget arbeid sammen med fag |
| Fargene i prikkfiguren | Én rad per sentralitetsklasse, så klassen leses av plasseringen. Én farge. Ved valgt fylke er de andre kommunene grå, ikke blekede |
| Sentralitet innenfor fylke | Vises når et fylke eller en kommune er valgt. Antall kommuner står i parentes, og klasser med færre enn tre kommuner er grå |
| Eldre: én figur | Én rute med 100 personer: mørk grønn er 70 år og eldre i 2026, lys grønn er økningen fram mot 2050 |
| Mengden tekst | Ingressen er kortet til to setninger, og flere figurnotater er kortet. Kildelinjen står fortsatt synlig under hver figur |

Andre rettelser: tittelen gjorde siden for bred på mobil (390 px), årstallene i viftediagrammet overlappet på mobil, og aksemerkene i stolpefigurene kunne gå i evig løkke når null stod midt mellom to merker.

## Hva ble endret i versjon 0.2

| Forslag fra sammenligningen | Løsning |
|---|---|
| Lesehjelp høyt oppe | Boksen «Slik leser du en framskriving» med fire punkter, og konseptgrafikken bak «Slik lages tallene» |
| Tallet for hele landet (H4) | Egen setning i toppgrafikken når hele landet er valgt, og i fotnoten |
| Sentralisering | Alle kommuner som prikker farget etter sentralitet, og vekst per sentralitetsklasse |
| 70+ i stedet for 67+ | Tiårige aldersgrupper. 70+ i nøkkeltall, personrute, fylkesfigur og tabell |
| Min kommune | Alle 357 kommuner kan velges i nedtrekkslisten, med søk, ved klikk i tabell og prikkfigur, og via adressen (`#omrade=1804`) |
| Avrundede tall i tekst | Toppgrafikken avrunder. Eksakte tall står i «Vis tallene» og tabellen |
| Komponenter 2026–2049 | Rettet, og ny figur med samlet bidrag over perioden |

## Kontroller i byggeskriptet

`scripts/lag_data.py` stopper bygget hvis ett av disse ikke stemmer: kommunene summerer til fylkene og fylkene til landet, alle år og alternativer; aldersgruppene summerer til folkemengden; endring per år = fødte − døde + nettoinnvandring + innenlands flytting; kommunene summerer til klassetallene for sentralitet; kartet har de samme 357 kommunenumrene som tallene (lagt til i 0.3, negativ test med ett endret kommunenummer stoppet bygget).

## Nye valg til kvalitetssikring (samlet i `05-kvalitetssikring.md`)

| | Valg | Begrunnelse |
|---|---|---|
| 10 | Varsel om små tall for kommuner under 2 000 innbyggere | Vår grense, for H3. Bør avklares med fagkontakten |
| 11 | Prikkfigur med aksen kuttet ved −20 og +45 prosent | Dekker alle kommuner i 2026-runden (−17,4 til +43,8). Må sjekkes ved ny publisering |
| 12 | Sentralitetsklasse 1 i mørkest grønn | Sekvensiell skala fra diagramstandarden, trinn 2–7. Klasse 6 er lys og har lav kontrast mot hvitt, men står også i tabellen |
| 13 | Overskrifter generert fra tallene, for eksempel «flere døde enn fødte fra 2046» | Teksten følger valgt område. Formuleringene bør leses av fagkontakten for et utvalg kommuner |

## Kjente svakheter

- Prikkfiguren og kartet kan ikke brukes med tastatur. Tabellen under prikkfiguren og kommunetabellen dekker det samme.
- Kartet er tegnet plant med lengdegradene krympet med cos(65°). Det gir rimelige proporsjoner for Norge, men er ikke en offisiell kartprojeksjon.
- Filen er 924 kB fordi data, d3 og skrift er bakt inn. Det er valgt for at siden skal virke uten eksterne kall.

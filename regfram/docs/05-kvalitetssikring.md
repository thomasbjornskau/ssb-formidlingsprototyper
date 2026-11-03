# Kvalitetssikring (regfram)

Samlet liste over det som er tolkning, eget valg eller ikke bekreftet. Grunnlag for fagkontrollen i steg 5.

## Grafikk og tekst

| | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| 1 | Fruktbarhet «om lag 1,6 på sikt» | «Slik lager SSB befolkningsframskrivinger» sier 1,64. Rapporten (lest gjennom sammendragsverktøy) sier 1,63 fra 2035 | Riktig tall. Avrundet til «om lag 1,6» inntil det er avklart |
| 2 | Levealder i 2050: kvinner 88,5 og menn 85,8 år | «Slik lager SSB befolkningsframskrivinger» | Bekreftet i to kilder. Ingen handling |
| 3 | Netto innvandring om lag 22 300 i 2025 og 17 100 i 2050 | Samme artikkel. Rapporten sier om lag 22 000 og 17 000 | Ingen handling |
| 4 | Flyttemønster fra 2016–2025 | Rapporten, kapittel 4 (via sammendrag) | Sjekk mot PDF |
| 5 | Valgene per forutsetning: fruktbarhet L/M/H, levealder L/M/H, flytting 0/M, innvandring 0/L/M/H | Utledet av de ni alternativene i tabell 14746 | Er dette en riktig og nyttig forenkling? MMM0 er nøytral nettoinnvandring, ikke null innvandring |
| 6 | «Ett år i modellen»: fødte, døde, innvandrere, utvandrere, flytting | Kohort-komponentmetoden slik den er beskrevet i metodeartikkelen | Rekkefølgen i modellen er ikke vist. Er det greit? |
| 7 | «Ikke med før det synes i statistikken»: boligfelt, arbeidsplasser, nedleggelser, asylmottak | Rapporten nevner planlagte prosjekter, arbeidsplassendringer og asylmottak. Metodeartikkelen nevner utbygging, ny infrastruktur og nedleggelser | Er formuleringen presis nok? |
| 8 | Avrunding i toppgrafikken (millioner med én desimal, ellers tusen, hundre eller ti) | Vårt valg, for å motvirke fasitlesning (H1) | Godtar fagmiljøet avrunding i formidlingen? |
| 9 | Andel eldre vises som 70+ | Rapporten bruker 70+ (H9) | Er 70+ riktig grense for formidlingen? |
| 10 | Varsel om små tall for kommuner under 2 000 innbyggere | Vår grense, for H3. Bør avklares med fagkontakten | Avklares med fagkontakten |
| 11 | Prikkfigur med aksen kuttet ved −20 og +45 prosent | Dekker alle kommuner i 2026-runden (−17,4 til +43,8). Må sjekkes ved ny publisering | Avklares med fagkontakten |
| 12 | Sentralitetsklasse 1 i mørkest grønn | Sekvensiell skala fra diagramstandarden, trinn 2–7. Klasse 6 er lys og har lav kontrast mot hvitt, men står også i tabellen | Avklares med fagkontakten |
| 13 | Overskrifter generert fra tallene, for eksempel «flere døde enn fødte fra 2046» | Teksten følger valgt område. Formuleringene bør leses av fagkontakten for et utvalg kommuner | Avklares med fagkontakten |

## Nye valg i versjon 0.3

| | Påstand eller valg | Grunnlag | Hva må sjekkes |
|---|---|---|---|
| 18 | Kartet: seks klasser med grensene −10, −5, 0, 10 og 20 prosent, blå–oker | Diagramstandarden anbefaler fem klasser, men et midtpunkt ved null gir partall. Grensene er valgt for denne runden, ikke kvantiler | Er klassene nyttige for fag, og skal de være faste mellom publiseringer? |
| 19 | Kommunegrenser 2024 fra Kartverket, via en åpen GitHub-samling, forenklet | Samme kommuneinndeling som tallene (357) | Bør SSBs egne kartdata brukes i en offisiell versjon? |
| 20 | Sentralitet innenfor fylke, med klasser under tre kommuner grå | Vårt valg mot tilfeldige prosenter | Er grensen fornuftig? |
| 21 | Eldrefiguren for fylke viser de ti høyeste og ti laveste kommunene når fylket har flere enn 20 | Plass. Alle står i tabellen | Godt nok? |
| 22 | Kartoverskriften nevner ytterpunktene blant kommuner med minst 2 000 innbyggere | Samme grense som varselet om små tall (punkt 10) | Avklares sammen med punkt 10 |

## Svar fra fagseksjonen 02.11.2026

Fra møtet i fagseksjonen: ingen feil i tekst, og ingenting som er veldig misvisende. Innspillene om figurer etter nivå, kart, farger i prikkfiguren, sentralitet innenfor fylke, eldrefiguren og mengden tekst er fulgt opp i versjon 0.3. Innspillet om «Slik lages tallene» er foreslått som eget arbeid. Punkt 12 om grønne klassefarger er ikke lenger aktuelt: prikkfiguren bruker én rad per klasse.

## Data og begreper

| | Spørsmål | Grunnlag |
|---|---|---|
| 14 | Riktig navn på sentralitetsinndelingen: «Sentralitet 2020» (Klass) eller «Sentralitet 2024» (statistikkbanken)? | Inndelingen gir identiske summer. Se `03-kildekart.md` |
| 15 | Er tabellvalget riktig for de fem spørsmålene? | `03-kildekart.md` |
| 16 | Hvordan bør avviket mellom nasjonal og regional framskriving forklares (H4)? | Prototypen viser begge tallene for hele landet |
| 17 | Stemmer hypotesene H1–H9 om misforståelser, og hvilke møter dere oftest? | `01-innsikt.md` |

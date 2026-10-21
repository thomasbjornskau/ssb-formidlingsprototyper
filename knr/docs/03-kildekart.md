Steg 3 i formidlingsprototype for knr · versjon 1.0 · 21.10.2026 · Status: godkjent av Thomas

# Kildekart: Nasjonalregnskap (knr)

Bygger på `01-innsikt.md` (makrostørrelse som gjennomgående valg) og toppgrafikk D fra steg 2. Rådataene er hentet direkte fra PxWebApi v2 med `scripts/hent_data.py` 21.10.2026. Dataomfang B ble valgt av Thomas samme dag.

## 1. Spørsmål, datasett og seksjoner

| Spørsmål | Datasett | Tabell | Seksjon |
|---|---|---|---|
| 1 Hvor fort vokser økonomien? | `makro_aar` | 09189 | Toppgrafikk D (årlig vekst 1971–2025) for valgt størrelse |
| 1 og 4 Kvartalet, «fire tall» | `makro_kvartal` | 09190 | Fra forrige kvartal og fra samme kvartal i fjor, siste tolv kvartaler |
| 2 BNP, Fastlands-BNP, olje og gass | `makro_aar` | 09189 | Oljeandelen, kroner mot volum |
| 3 Hva driver veksten? | `makro_aar`, `naering_aar`, `naering_kvartal` | 09189, 09170, 09171 | Anvendelsen av BNP, vekst etter næring per år og kvartal |
| 4 Hvor sikre er tallene? | `maaned`, `makro_kvartal`, hovedrevisjonen `[K4]` | 11721, 09190 | Måned mot tremånederssum, revisjon i 2025 |
| Velgeren | `makro_aar` | 09189 | 51 størrelser med hierarki |

**Brukes ikke:** 09842 (BNP per innbygger), som stopper i 2024 og ikke er oppdatert etter hovedrevisjonen. 12880, som blander regnskap og prognoser. 11713 (fylkesfordelt), som stopper i 2023.

## 2. Strukturen som former prototypen

Alt er talt fra rådataene.

- **Makrostørrelsene.** 51 størrelser i fem nivåer, lest ut av ¬-tegnene i etikettene: 17 på øverste nivå, så 17, 8, 5 og 4. Alle har tall fra 1970 (år) og 1978K1 (kvartal). Hierarkiet er ikke et rent tre: noen ¬-ledd henger under forrige toppnivå i rekkefølgen, men noen toppnivåer er aggregater av andre toppnivåer (BNP, Samlet sluttanvendelse). Velgeren må vise det som en liste med innrykk, ikke som et summerende tre.
- **Manglende verdier.** Ingen nivåer mangler. Endringsrater mangler («..») for første periode og for 4 serier der nivået er null eller skifter fortegn: lagerendring og statistiske avvik (32 år), tjenester tilknyttet utvinning (15), utenriks sjøfart, investering (2) og verdigjenstander (1). Lagerendring har negative nivåer i 78 kvartaler.
- **Næringer.** 46 koder per år og 51 per kvartal. 24 er toppnæringer. Fiske og havbruk var +5,1 prosent fra 1. til 2. kvartal 2026, som i artikkelen `[K1]`. Lavest var jordbruk og skogbruk (−3,9) og høyest utenriks sjøfart (+5,4). Volumendring mangler for utvinning og rørtransport i noen år.

## 3. Metoder og kontroller

| # | Kontroll | Resultat |
|---|---|---|
| K1 | Konsum + investering + eksport − import = BNP, løpende priser, 1970–2025 | Avvik høyst 11 millioner (avrunding) |
| K2 | Bruttoprodukt Fastlands-Norge + olje og sjøfart + produktavgifter = BNP | 0 avvik alle år |
| K3 | BNP Fastlands-Norge + oljevirksomhet og utenriks sjøfart = BNP | 0 avvik alle år |
| K4 | Årlig volumendring regnet fra faste priser = publisert | 220 av 220 treff på én desimal (BNP, Fastlands-BNP, konsum, eksport) |
| K5 | Kvartalsvekst regnet fra sesongjusterte nivåer = publisert | 237 avvik av 9 697, alle på 0,1 eller i små serier. 0 avvik for BNP og Fastlands-BNP. **Prototypen bruker publiserte rater** |
| K6 | Sum av kvartaler = årstall, løpende og faste priser | Avvik høyst 6 millioner over 1978–2025 (BNP 2012). Første test dekket bare tre år og viste 2 |
| K7 | Sum av sesongjusterte kvartaler = årstall | Ikke alltid. Fastlands-BNP 2025: +7,3 milliarder. 2010: 0 |
| K8 | Kjedingsavvik: anvendelse i faste priser minus BNP | 18,7 milliarder (1990), 51,0 (2010), 5,7 (2022), 0 fra 2023 |
| K9 | Tremånederssum i juni = kvartalsvekst 2. kvartal | BNP 0,7 = 0,7, Fastlands-BNP 0,3 = 0,3. Også mars mot 1. kvartal |
| K10 | Toppnæringer summerer til totalen, og totalen minus utvinning, rørtransport og utenriks sjøfart = Fastlands-Norge | Avvik høyst 3 millioner, Fastlands-Norge eksakt |
| K11 | Bruttoprodukt Fastlands-Norge i 09170 = samme størrelse i 09189 | Eksakt |

## 4. Datamengde

| Datasett | Celler |
|---|---|
| `makro_aar` | 11 424 |
| `makro_kvartal` | 49 470 |
| `maaned` | 504 |
| `naering_aar` | 5 152 |
| `naering_kvartal` | 29 682 |
| **Sum** | **96 232** |

Innbakt i `index.html` blir det om lag 0,5 MB.

## 5. Hull og hindre

- **H1. «Om statistikken» er ikke lest** (se `01-innsikt.md`, avsnitt 8).
- **H2. Ingen revisjonsdata i statistikkbanken.** Spørsmål 4 bygger på hovedrevisjonen `[K2][K4]` og eksemplet fra 1. kvartal 2026 `[K1]`, ikke på en tidsserie av publiseringer.
- **H3. Sesongjusterte kvartaler summerer ikke til året** (K7). Hvorfor bør fag forklare.
- **H4. Hierarkiet i makrostørrelsene er ikke et summerende tre.** Innrykk vises som i statistikkbanken, uten summekontroll per nivå.
- **H5. `hent_data.py` stopper nå hvis svaret har færre celler enn «omfang» i `kilder.json` sier.** Det er en forbedring som bør tas inn i de andre prototypene (se folkemengde, hull H1).

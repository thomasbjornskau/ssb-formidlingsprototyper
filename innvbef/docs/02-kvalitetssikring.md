Steg 2 i formidlingsprototype for innvbef · versjon 1.0 · 26.10.2026 · Status: godkjent av Thomas

# Kvalitetssikring av grafikken

**Beslutning (Thomas, 26.10.2026):** Konseptgrafikken er godkjent. Toppgrafikk B (utvikling over tid) er valgt, med veksling mellom absolutte tall (linjediagram, innvandrere og norskfødte med innvandrerforeldre) og relative tall (stablet areal til 100 prosent, med øvrig befolkning). Inndelingen i seks kategorier kommer lenger ned. En egen seksjon viser de 30 kombinasjonene i tabell 12548, med valg mellom alle variantene og de seks brede gruppene.

Alt i konsept- og toppgrafikken som er tolkning, eget valg eller ikke bekreftet av fag. Samles i `05-kvalitetssikring.md`. Tallene er hentet fra statistikkbanken 26.10.2026 (`data/grafikk-utkast.json`) og byttes med `data/raw/` i steg 3.

## Konseptgrafikken

| # | Påstand eller valg | Grunnlag | Må sjekkes |
|---|---|---|---|
| K1 | «Bosatt: lovlig opphold, skal bo her minst seks måneder» | Om statistikken 2021 [K2 i 01] | At regelen står uendret i gjeldende «Om statistikken» |
| K2 | Familietrærne: innvandrer har seg selv, to foreldre og fire besteforeldre født i utlandet | Definisjonen [K2] | Om besteforeldrekravet fortsatt brukes, eller om fire *utenlandsfødte besteforeldre* nå er implisitt |
| K3 | De tre «andre» kategoriene slått sammen til «Tre andre kategorier», 7,1 prosent | Eget valg for lesbarhet. Etiketten innfører ikke noe nytt begrep | Om sammenslåingen er akseptabel |
| K4 | Landbakgrunn: morens fødeland når foreldrene er født i ulike land | [K2] | Gjelder dette også når bare én forelder er innvandrer? (Da er personen ikke i statistikken, så trolig uten betydning) |
| K5 | Eksemplene i trinn 4 er konstruerte | Eget valg | Merket «Eksempler» i grafikken |
| K6 | Regnskapet for innvandrere 2025: 965 113 + 49 179 − 24 407 − 2 860 + 95 = 987 120 | Tabell 10516 | «Andre endringer» (95) er differansen mellom tilveksten og komponentene. Tabellen oppgir 1 fødsel blant innvandrere. Hva består posten av? |
| K7 | «Barn født i Norge blir norskfødte, ikke innvandrere» | Definisjonen | Bare når begge foreldrene er innvandrere. Teksten forenkler [T] |
| K8 | Overdekning 2,3 prosent blant innvandrere | Notater 2024/3, 2,29 prosent | Notatet gjelder et tidligere år. Er det et nyere anslag? |

## Toppgrafikken

| # | Variant | Påstand eller valg | Grunnlag | Må sjekkes |
|---|---|---|---|---|
| T1 | A | Andelene 17,5, 19,0, 21,8 og 28,9 prosent | Regnet fra 05182, summen av kategoriene er lik folkemengden 5 627 400 | Om fag vil vise 21,8 og 28,9 (spørsmål 4 i innsiktsnotatet) |
| T2 | A | «+ andre født i utlandet» omfatter utenlandsfødte med én eller to norskfødte foreldre, «også adopterte» | 05182, kategoriene 5 og 7 | At utenlandsadopterte faktisk ligger i kategori 7 |
| T3 | A | Etiketten «Alle utenom norskfødte med norskfødte foreldre» | Beskrivende etikett, bygget på SSBs kategorinavn | Om SSB har en etablert betegnelse |
| T4 | B | «Økningen i 2025 var den laveste siden 2021» | Endring 1.1.2025–1.1.2026 = 22 007. Endring 1.1.2021–1.1.2022 = 19 262 | Stemmer. Avviker i ordlyd fra SSBs «laveste på flere år» |
| T5 | B | «Mer enn firedoblet siden 2000» | 987 120 / 238 462 = 4,14 | Stemmer |
| T6 | B | 1970–1986 tegnet prikket | Tabellen har bare 1970, 1980 og 1986 før årlige tall | At tallene for 1970 og 1980 er sammenlignbare med senere år. «Om statistikken» sier sammenlignbart fra 1995 |
| T7 | C | Ti land = 45 prosent | 555 974 / 1 225 627 | Stemmer |
| T8 | C | Pakistan 44 prosent norskfødte, Ukraina 3 prosent | 13880 | Stemmer. Tolkningen (speiler når gruppen kom) er [T], H9 |
| T9 | C | Rangering etter innvandrere og norskfødte samlet | Eget valg | Rangeringen endres hvis bare innvandrere telles (Sverige foran Somalia, Pakistan, Irak og Eritrea) |

## Felles

- `felles/grafikk.py` finnes ikke i repoet. Skriptet bruker samme reserve med samme grensesnitt som de andre prototypene. Bør legges inn i `felles/` eller fjernes fra skill-beskrivelsen.
- Fargene i C og B er flatetoner fra ssb-justert palett. Blå `#3face6` har under 3:1 mot hvitt og er merket direkte eller med tegnforklaring.

`Steg 3 i formidlingsprototype for arblonn · versjon 1.0 · 30.10.2026 · Status: godkjent av Thomas (stort omfang, 30.10.2026)`

> Kvalitetssikringspunktene er samlet i `05-kvalitetssikring.md`, som erstatter listen her.

# Kildekart

**Merking:** `[K1]`–`[K7]` som i `01-innsikt.md` · `[T]` = vår tolkning.

## 1. Spørsmål, datasett og seksjon

| Spørsmål (01-innsikt) | Datasett | Tabell | Seksjon i prototypen |
|---|---|---|---|
| Toppgrafikk C | `maned` | 13126 | Toppen: månedsendring, sesongjustert, endelig linje og siste foreløpige punkter |
| 1 Jobber og mennesker | `kvartal_naering`, `arbeidstid`, `kjonn_alder` | 11654, 13871, 11652 | Jobber, lønnstakere og heltidsekvivalenter per næring; heltid/deltid; kjønn og alder |
| 2 Hvilken lønn | `kvartal_naering`, `arbeidstid`, `kjonn_alder` | 11654, 13871, 11652 | Snitt og median, avtalt månedslønn og månedslønn, per næring og kjønn |
| 3 Flere eller færre jobber nå | `maned` | 13126 | Lang sesongjustert serie fra 2003; næringenes bidrag til siste endring |
| 4 Hvor vokser jobbene | `kvartal_naering`, `kvartal_fylke`, `naering88` | 11654, 12314 | Næringer rangert; fylke som filter fra 2024; tosifrede undernæringer i valgt næring |
| 5 Lønnsvekst | `kvartal_naering` | 11654 | Vekst i avtalt månedslønn per næring, regnet fra kroner |

Ikke brukt: 12315 (innvandringskategori), 12316 og 13876 (jobb- og arbeidskraftsstrømmer), 11656 og 11658 (88 næringer og yrker etter kjønn og alder). Ingen arkiverte tabeller er aktuelle.

## 2. Struktur som former prototypen

**Næring.** 17 grupper (SN2007) og «00 Uoppgitt», likt i alle tabellene. 12314 har 87 tosifrede næringer og «00». Fordelingen per gruppe er talt fra kodene:

| Gruppe | Tosifrede | | Gruppe | Tosifrede |
|---|---|---|---|---|
| 01-03 Jordbruk, skogbruk, fiske | 3 | | 58-63 Informasjon og kommunikasjon | 6 |
| 05-09 Bergverk og utvinning | 5 | | 64-66 Finans og forsikring | 3 |
| 10-33 Industri | 24 | | 68-75 Teknisk tjenesteyting, eiendom | 8 |
| 35-39 Elektrisitet, vann, renovasjon | 5 | | 77-82 Forretningsmessig tjenesteyting | 6 |
| 41-43 Bygg og anlegg | 3 | | 84 Offentlig administrasjon | 1 |
| 45-47 Varehandel | 3 | | 85 Undervisning | 1 |
| 49-53 Transport og lagring | 5 | | 86-88 Helse og sosial | 3 |
| 55-56 Overnatting og servering | 2 | | 90-99 Personlig tjenesteyting | 9 |

Konsekvens: for 84 og 85 finnes ingen undernæringer. Prototypen sier det i stedet for å vise én stolpe. [T]

**Tid.**
- Kvartalstall 2016K1–2026K2 (42 kvartaler) i 11654, 11652, 13871 og 12314.
- Månedstall i 13126 fra 2003M05 til 2026M09 (281 måneder), men ikke for alt. Talt fra `..` og `.` i dataene:

| Variabel i 13126 | Endelige | Foreløpige |
|---|---|---|
| Jobber og lønnstakere, sesongjustert | 2003M05–2026M08 | 2016M01–2026M09 |
| Jobber, ujustert | 2003M05–2026M08 | 2016M01–2026M09 |
| Lønnstakere, ujustert | 2016M01–2026M08 | 2016M01–2026M09 |
| Kontantlønn, begge former | 2016M01–2026M08 (`.` før) | 2016M01–2026M09 |

**Fylke.**
- Med inndelingen «Fylker 2024-» har sju fylker (31, 32, 33, 39, 40, 55, 56) verdien **0** før 2024K1. Fire til (34, 42, 46, 50) har 0 før 2018K1 eller 2020K1.
- 0 betyr at fylket ikke fantes, ikke null jobber. Fylkesdata hentes derfor bare fra 2024K1: 10 kvartaler, og år-mot-år fra 2025K1.
- Fylket er arbeidssted.

**Manglende verdier.**

| Datasett | Symbol | Antall | Hvor |
|---|---|---|---|
| `maned` | `..` / `.` | 16 524 / 10 944 | Se tidstabellen over. Siste måned har bare foreløpig tall |
| `kvartal_fylke` | `:` | 1 754 | Nesten alt i «00 Uoppgitt» og i regionene «uoppgitt fylke» og «ikke Fastlands-Norge». I de 15 fylkene × 16 næringene er bare finans i Finnmark 2025K1 skjult (6 lønnsvariabler) |
| `naering88` | `:` | 1 303 | Lønn og indeks for små næringer. I 2026K2: 05, 12, 15, 19, 99 og delvis 39 |
| `arbeidstid` | `:` | 16 | Lønn for kvinner på heltid i «00 Uoppgitt», fire kvartaler |
| `kvartal_naering`, `kjonn_alder` | | 0 | |

## 3. Metoder testet

| Metode | Resultat |
|---|---|
| Lønnsvekst regnet fra kronebeløpene, 2025K2–2026K2, 18 næringskoder | 18 av 18 treffer publisert endring på første desimal (statistikksiden, tabell 4) |
| Jobbvekst regnet fra antall | 18 av 18 treffer |
| Lønnsvekst regnet fra den avrundede indeksen | Gir 4,0 for alle næringer mot publisert 3,9. Brukes ikke |
| Lønnsindeks = snitt / snitt 2024K1 × 100 | Stemmer for alle næringer og kvartaler, største avvik 0,10 (avrunding) |
| Månedsendring innenfor samme versjon | Gjenskaper alle seks publiserte endringer i tabell 1 eksakt |
| Næringenes bidrag til siste månedsendring (sesongjustert, foreløpig) | Sum 24 773 mot total 24 775. Helse og sosial: +10 309 |

## 4. Kontroller (`scripts/kontroll_kilder.py`)

Alle 26 går, 30.10.2026. Toleransene er satt etter de faktiske avvikene.

| Kontroll | Største avvik | Toleranse |
|---|---|---|
| K1 Nøkkeltall 2026K2 mot statistikksiden | 0 | eksakt |
| K2 17 næringer = alle næringer, jobber og lønnstakere, alle kvartaler | 0 | 0 |
| K3 Fylker + uoppgitt + ikke Fastlands-Norge = landet, alle næringer, fra 2024K1 | 0 | 3 |
| K4 Aldersgrupper og kjønn = totalen | 0 | 2 |
| K5 Heltid + deltid = i alt | 0 | 2 |
| K5b 13871 mot 11654, jobber i alt | 9 | 10 |
| K6 Tosifrede næringer summert til 17 grupper | 11 (567 av 756 celler avviker, uten skjulte celler) | 15 |
| K7 Lønnsindeks mot snitt | 0,10 | 0,11 |
| K8 Publiserte månedsendringer | 0 | eksakt |
| K9 Næringer = total i 13126 (ujustert / sesongjustert) | 0 / 5 | 0 / 5 |
| K10 Endelig midtmåned = kvartalstall | 12, utenom 2024M11 (−305, kjent) | 15 |
| K11 Vekst fra kroner og antall = publisert | 18 av 18 | alle |
| K12–K13 Hvilke perioder har tall | som i tidstabellen | eksakt |

## 5. Funn som endrer grafikken

**G13 holder ikke.** Den foreløpige sesongjusterte serien sesongjusteres på nytt hver måned.
- For juli–august 2023 publiserte SSB om lag −16 850 jobber og −11 200 lønnstakere [K8]. Serien viser i dag −2 276 og −827.
- Toppgrafikk C tegnes derfor med endelig linje og bare de to siste foreløpige punktene. Den stiplete historiske foreløpige linja fra steg 2 utgår.

**G7 i ujusterte tall.** Endelig minus foreløpig for august 2026 er 94 755 jobber ujustert, og 67 276 sesongjustert. SSB oppgir at foreløpige tall mangler om lag 20 000–90 000 jobber [K8].

## 6. Datamengde og strategi

Valgt av Thomas 30.10.2026: **stort omfang**.

| Datasett | Celler | Rådata |
|---|---|---|
| `maned` | 60 696 | 826 kB |
| `kvartal_naering` | 6 804 | 60 kB |
| `kvartal_fylke` | 27 540 | 217 kB |
| `arbeidstid` | 54 432 | 383 kB |
| `kjonn_alder` | 6 804 | 58 kB |
| `naering88` | 33 642 | 254 kB |
| **Sum** | **189 918** | **1,8 MB** |

`lag_data.py` velger ut det prototypen bruker, så den innbakte filen blir mindre enn rådataene. Ingen spørring er i nærheten av grensen på 800 000 celler.

**Rådata.** `data.ssb.no` var tilgjengelig fra arbeidsområdet 30.10.2026. Rådataene er derfor svarene fra API-et, uendret, hentet med `scripts/hent_data.py`. De er ikke rekonstruert, som i tidligere prototyper.

## 7. Hull og hindre

1. Den foreløpige historikken kan ikke vises som publisert. Den publiserte førsteversjonen finnes bare i artikler, ikke i statistikkbanken.
2. Kjent avvik 2024M11 mot 2024K4 (−305 jobber) er ikke forklart. Spørsmål til fag.
3. 12314 avviker fra 11654 med opptil 11 jobber per celle. Prototypen viser tosifrede næringer fra 12314 og grupper fra 11654, og skal ikke summere mellom dem.
4. Fylke kan bare følges fra 2024. Rogaland-bruddet i 2018 er dermed utenfor fylkesvisningen, men synes i månedsserien for bergverk.
5. Ujusterte lønnstakere og kontantlønn mangler før 2016. Den lange serien viser bare jobber og sesongjusterte lønnstakere.
6. Finans i Finnmark 2025K1 er skjult. Det gir et hull i år-mot-år-sammenligningen for 2026K1.

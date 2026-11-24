Steg 1b i formidlingsprototype for overnatting · versjon 0.1 · 24.11.2026 · Status: utkast

# Sammenligning med Tableau-visningen «vis-overnattingar-i-reiselivsregionar»

**Merking** som i `01-innsikt.md`: `[K]` kilde, `[T]` tolkning, `[H]` hypotese.

**Grunnlag.** To skjermbilder fra Thomas 24.11.2026 av Tableau Public-visningen [K14], fanene «Reiselivsregionar» og «Nøkkeltall». Visningen er ikke åpnet interaktivt, så tooltips, undertrykte celler og standardvalg er ikke sett. Skjermbildene viser 2021 og april 2021. Det tyder på at visningen ikke er oppdatert etter 2021 [T].

Innsikten i `01-innsikt.md` ble skrevet før visningen ble sett, slik retrospektiv variant krever.

---

## Hva visningen gjør

**Fanen «Reiselivsregionar».** Velgere for år, innkvarteringstype (alle, hotell, camping/hyttegrender/vandrerhjem), bostedsland og enkeltmåned. Et fargekart over reiselivsregionene med «START HER: Klikk på en region». Klikket filtrerer tre diagrammer: månedlig utvikling 2016–2021, topp 10 bostedsland og fordeling på innkvarteringstype.

**Fanen «Nøkkeltall».** Seks hotellindikatorer fra 14176 som punktstriper: kapasitetsutnytting av senger og rom, pris per rom, utleide rom, losjiomsetning per tilgjengelig rom og losjiomsetning. Hver region er ett punkt. Laveste og høyeste region er navngitt i endene, og valgt region er uthevet med navn og verdi. Månedsvelger og fritt valg av regioner.

---

## Hva visningen gjør riktig

| | Grep | Hvorfor det virker | Ta med? |
|---|---|---|---|
| R1 | Kartet er inngangen, og klikk på region filtrerer alt | Reiselivsregionen er brukerens eget nivå. Én handling gir hele bildet for regionen | Ja, som «Min reiselivsregion» |
| R2 | Månedlig linje over flere år | Sesongen blir synlig med en gang. 3,18 mill. i juli mot under 0,35 mill. om vinteren for camping og hyttegrender | Ja, men med samme måned i fjor (H3) |
| R3 | Punktstriper med valgt region uthevet mot alle andre | Svarer på «hvordan ligger vi an?» uten rangeringstabell. Ytterpunktene gir skala | Ja, det beste grepet i visningen |
| R4 | Laveste og høyeste region navngitt i endene | Direkte merking i stedet for akse og forklaring | Ja |
| R5 | Senger og rom som to separate rader | Gjør forskjellen synlig (9 mot 15 prosent for Nord-Gudbrandsdal i april 2021) | Ja, men forklart (H5) |
| R6 | Kort brukerrettet tekst ved velgerne | Forteller hva som skjer når du velger | Ja |

---

## Hva visningen mangler eller gjør vanskelig

| | Problem | Hypotese | Hva prototypen bør gjøre |
|---|---|---|---|
| M1 | Bygger på Reiselivsregionar 2020: Hadeland/Ringerike står i forklaringen [K12] | H11 | Bruke 2024-versjonen med 66 regioner og forklare endringen kort |
| M2 | Står på 2021, et pandemiår, og viser ikke siste måned | H3 | Åpne på siste publiserte måned og hente data automatisk |
| M3 | Ingen sammenligning med samme måned i fjor, ingen sesongjustering | H3 | Endring fra samme måned i fjor som hovedtall, sesongjustert linje for landet |
| M4 | Fargeforklaring med én farge per region i «Nøkkeltall». 66 farger bærer ingen informasjon og blir grå bakgrunnsstøy | – | Grå punkter, én uthevingsfarge (`ssb-diagramstandard`) |
| M5 | Volum (utleide rom, losjiomsetning) og forholdstall (kapasitet, pris) står i samme punktstripe. Volum handler mest om størrelsen på regionen | H4 | Skille størrelse fra intensitet. Vise volum som andel eller endring, ikke nivå |
| M6 | Ingen forklaring av forskjellen på senger og rom, eller på losjiomsetning | H4, H5 | Lesehjelp ved indikatorene |
| M7 | Overnatting og gjest forklares ikke | H2 | Lesehjelp |
| M8 | Topp 10 bostedsland uten forbehold. For camping og hyttegrender 2021 topper Polen, Litauen og Slovakia, som neppe er turistmarkeder | H6, ny H12 | Forbehold om bostedsland. Se H12 under |
| M9 | Ingen markering av brudd i 2017 (Altinn, ny landliste) og 2020 (flere hotell) innenfor 2016–2021 | H7 | Stiplet strek og tekst |
| M10 | Kan ikke se hvordan undertrykte celler vises. Kartskalaen starter på 322, så små regioner kan mangle uten at det sies | H11 | Vise «:» som hull med forklaring, ikke som null eller tom farge |
| M11 | Ingenting om hva statistikken ikke dekker | H1 | Konseptgrafikken i steg 2 |
| M12 | Kartet er lite, og små regioner på Østlandet er vanskelige å klikke | – | Søkbar regionvelger i tillegg til kart |

---

## Ny hypotese fra visningen

**H12. Overnattinger fra utlandet er turisme.** I visningen topper Polen, Litauen og Slovakia lista for camping og hyttegrender i 2021. For hele landet var Polen femte største utenlandske marked for camping, hyttegrender og vandrerhjem både i 2021 (104 471) og i 2025 (229 185), og blant de fem største i månedene november–februar begge år [K10]. Grunnlaget er at gjester klassifiseres etter bostedsland, og at personer som har tenkt å bo under ett år i Norge regnes som bosatt i hjemlandet [K1]. Formål registreres bare for hotell [K1]. Vår tolkning er at en del av disse overnattingene er arbeidstakere på oppdrag, ikke turister [T]. Det må prøves i fagkontrollen. Prioritet: middels.

---

## Forslag til arbeidslisten i steg 4

1. «Min reiselivsregion» med kart og søk, 2024-inndelingen (R1, M1, M12).
2. Punktstripe for hotellindikatorene med valgt region uthevet, grå for de andre, navngitte ytterpunkter (R3, R4, M4).
3. Bare forholdstall i punktstripen: kapasitetsutnytting senger og rom, pris per rom, losjiomsetning per tilgjengelig rom. Volum vises som endring fra i fjor (M5).
4. Månedslinje med fjoråret som referanse, og sesongjustert linje for landet (R2, M3).
5. Lesehjelp ved senger/rom, losjiomsetning, overnatting/gjest og bostedsland (M6–M8).
6. Undertrykte celler som synlige hull (M10).
7. Brudd i seriene markert (M9).
8. Åpne på siste publiserte måned (M2).

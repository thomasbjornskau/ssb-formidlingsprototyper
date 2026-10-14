# Sammenligning: innsiktsnotat mot eksisterende prototype

Tilbakeskuende pilot for `regfram` · 13.10.2026

Notatet her sammenligner de fem prioriterte spørsmålene og de pedagogiske kravene i `01-innsikt.md` med prototypen `regfram-index.html` (versjon 9.10.2026). Hensikten er å teste om metoden ville ha gitt en annen prototype enn den vi bygget uten metode.

## Resultat

| Krav fra innsiktsnotatet | Prototypen i dag | Vurdering |
|---|---|---|
| **1. Hvor mange blir vi, og hvor sikkert er det?** | Nøkkeltall og linjediagram med spenn for lav og høy nasjonal vekst | **Delvis.** Spennet vises, men det står ikke at det kan undervurdere usikkerheten (H2). Tallene er gitt med presisjon til én person også i ingress og nøkkeltall (H1) |
| **2. Hvor vokser og hvor krymper det, og hvor sterk er sentraliseringen?** | Stolper per fylke, kommunetabell og antall kommuner som krymper | **Delvis.** Fylker og kommuner er dekket, men sentralisering, som er SSBs nest viktigste budskap, mangler helt |
| **3. Hvorfor?** | Linjer for fødselsoverskudd, nettoinnvandring og innenlands flytting | **Dekket** |
| **4. Hvor raskt eldes befolkningen?** | Andel 67+, antall 80+, endring etter aldersgruppe | **Dekket, men med en annen grense enn SSB.** Rapporten bruker 70+ (H9) |
| **5. Hva skjer i min kommune?** | Bare som rad i kommunetabellen. Nedtrekkslisten har bare fylker | **Svakt** |
| **«Slik leser du en framskriving»** | En fotnote nederst om bokstavkoder og at det ikke er prognoser | **Svakt.** Står for langt ned, og mangler H6 (lokale planer er ikke med) |
| **Tallet for hele landet (H4)** | Viser 6 195 859 uten å nevne at den nasjonale framskrivingen gir 6 214 071 | **Mangler** |
| **Små kommuner (H3)** | Merknad over tabellen og sortering etter folkemengde | **Dekket** |

## Hva sammenligningen sier om metoden

- **Metoden skiller.** Den ville gitt en merkbart annen prototype. To av SSBs egne hovedbudskap ble ikke dekket uten metode: sentraliseringen og hvordan framskrivingen skal leses. Det tyder på at steg 1 tilfører noe og ikke bare bekrefter det vi ellers ville gjort.
- **Hypotesene treffer prototypen selv.** Prototypen har flere av svakhetene innsiktsnotatet advarer mot (H1, H2, H4). Det er et argument for at steg 1 må komme før byggingen også i praksis, ikke bare på papiret.
- **Det prototypen gjorde bedre enn notatet foreslo.** Endring etter aldersgruppe og sammenligning av eldreandelen mellom fylkene viser aldringen tydeligere enn ett enkelt tall. Dette bør inn som mønster for statistikker av typen befolkning.

## Forslag til revisjon av prototypen

Tallgrunnlaget for punkt 2, 3 og 5 avklares i steg 3 (kildekart).

1. **«Slik leser du en framskriving»** høyt oppe på siden: hvis-språk, hva spennet er og ikke er, hva bokstavkodene betyr, og at lokale planer ikke er med.
2. **En linje om tallet for hele landet** ved nøkkeltallet, med det nasjonale tallet og forklaringen.
3. **En ny seksjon om sentralisering**, med vekst etter sentralitetsklasse. Tabell 14746 har kodelisten «Sentralitet 2024».
4. **70+ i stedet for 67+**, i tråd med SSBs omtale. Kodelisten «0-24, 25-34, 35-44, 45-69, 70-79, 80+» gir 70+ direkte.
5. **Min kommune**: mulighet til å velge kommune, ikke bare fylke.
6. **Avrundede tall i løpende tekst** («om lag 6,2 millioner») og eksakte tall i tabeller.

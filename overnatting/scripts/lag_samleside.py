"""Lager docs/grafikk/02-grafikk-utkast.html med SVG-ene innebygd.

Kjøres fra overnatting/ etter lag_grafikk.py.
"""
import os

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def svg(sti):
    with open(os.path.join(ROT, sti), encoding="utf-8") as f:
        s = f.read()
    return s.replace("<svg ", '<svg style="max-width:100%;height:auto" ', 1)


TRINN = [
    ("Gjesten sjekker inn",
     "Overnatting og gjest forklares med én konkret reise (H2). Eksempelet er merket som eksempeltall. "
     "Bostedsland kommer inn allerede her, fordi det styrer alle landtall senere (H6, H12)."),
    ("Bedriften rapporterer",
     "Viser hvem som er med og størrelsesgrensene. Grensene forklarer hvorfor små steder mangler, "
     "og hvorfor hotellene har mer innhold enn resten (formål, rom, omsetning)."),
    ("SSB kontrollerer og beregner",
     "Frafall og den nye campingmetoden. Metoden fra februar 2026 er det ferskeste bruddet i "
     "statistikken (H7), og den gir beregnede, ikke talte, overnattinger."),
    ("Tallene publiseres",
     "Nivåene, også de 66 reiselivsregionene, og «:» for undertrykte tall (H8, H11). Ett ekte tall for "
     "siste måned forankrer figuren."),
    ("Ikke med",
     "Den stiplede boksen svarer på spørsmål 5 og H1 med størrelsesordener: hytte, familie og venner, "
     "plattformutleie, og det som er utenfor grensene."),
]

VARIANTER = [
    ("A", "Rekord, men ikke opp", "02-topp-a.svg",
     "Spørsmål 1: Hvordan går det nå, og er det egentlig rekord?",
     "H3, H7",
     "Rekord og nedgang er begge riktige, de svarer på ulike spørsmål. Viser samme måned i fjor og "
     "sesongjustert utvikling side om side.",
     "Sesongjustert endring fra forrige måned er regnet av oss, ikke publisert av SSB. Fag bør godta "
     "målet (A3). Sesongjusterte tall finnes bare for land og fylker, ikke reiselivsregioner. Bruddet "
     "i 2020 må tallfestes (A4)."),
    ("B", "7 av 10 netter er ikke med", "02-topp-b.svg",
     "Spørsmål 5: Hva teller statistikken, og hva ligger utenfor?",
     "H1, H2",
     "Det sterkeste motgiftet mot den største misforståelsen. Ingen andre varianter sier hva "
     "statistikken ikke er.",
     "Bygger på Reiseundersøkelsen (11270), en annen statistikk. Populasjon og definisjonen av "
     "«ikke kommersiell» må leses i steg 3 (B1, B2). Kan ikke lages per reiselivsregion."),
    ("C", "Utlendinger på hotell driver veksten", "02-topp-c.svg",
     "Spørsmål 2: Hvem overnatter, nordmenn eller utlendinger?",
     "H6, H7, H12",
     "Svarer på hva som driver tallet, i en form som kan gjentas hver måned. Viser at camping gikk "
     "ned samme måned som hotellene satte rekord.",
     "Kan lages per reiselivsregion fra 14172, men bare med to innkvarteringsgrupper. "
     "Campingtallet trenger forbehold om ny metode (C2). Landtall trenger forbehold om bostedsland."),
]

css = """
body{font-family:'Open Sans','Segoe UI',Arial,sans-serif;color:#274247;margin:0;background:#f3f5f5}
main{max-width:1240px;margin:0 auto;padding:32px 20px 64px}
h1{font-family:'Roboto Condensed','Arial Narrow',Arial,sans-serif;font-size:36px;margin:0 0 4px}
h2{font-family:Roboto,Arial,sans-serif;font-size:24px;margin:48px 0 8px}
h3{font-family:Roboto,Arial,sans-serif;font-size:18px;margin:0 0 6px}
.status{color:#5e787a;font-size:14px;margin-bottom:24px}
.kort{background:#fff;padding:20px;margin:16px 0;border-top:5px solid #00824d}
.forklaring{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:16px}
.forklaring div{background:#fff;padding:14px;font-size:15px;line-height:1.5}
.meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;font-size:15px;line-height:1.5;margin-top:12px}
.meta b{display:block;font-size:14px;color:#5e787a}
.smal{display:flex;gap:32px;align-items:flex-start;flex-wrap:wrap}
.smal p{max-width:520px;line-height:1.6}
"""

deler = [f"<!DOCTYPE html><html lang='nb'><head><meta charset='utf-8'>"
         f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
         f"<title>Overnatting – grafikkutkast steg 2</title><style>{css}</style></head><body><main>",
         "<h1>Overnatting: grafikkutkast</h1>",
         "<div class='status'>Steg 2 i formidlingsprototype for overnatting · versjon 0.1 · 24.11.2026 · "
         "Status: utkast. Tall hentet fra data.ssb.no 24.11.2026. Se docs/02-kvalitetssikring.md.</div>",
         "<h2>Konseptgrafikken: Slik lages tallene</h2>",
         f"<div class='kort'>{svg('src/konsept-bred.svg')}</div>",
         "<div class='forklaring'>"]
for i, (t, f) in enumerate(TRINN):
    nr = f"{i + 1}. " if i < 4 else ""
    deler.append(f"<div><h3>{nr}{t}</h3>{f}</div>")
deler.append("</div>")
deler.append("<h2>Smal versjon (390 px)</h2><div class='smal'>"
             f"<div class='kort' style='padding:0;width:390px'>{svg('src/konsept-smal.svg')}</div>"
             "<p>Trinnene står under hverandre med piler nedover. «Ikke med» blir en liste. "
             "Tekst og eksempel er de samme som i den brede versjonen.</p></div>")
deler.append("<h2>Toppgrafikk: tre varianter</h2>")
for kode, navn, fil, spm, hyp, hvorfor, krav in VARIANTER:
    deler.append(f"<div class='kort'><h3>Variant {kode}: {navn}</h3>{svg('docs/grafikk/' + fil)}"
                 f"<div class='meta'><div><b>Svarer på</b>{spm}</div><div><b>Hypoteser</b>{hyp}</div>"
                 f"<div><b>Hvorfor</b>{hvorfor}</div><div><b>Må til for å bygge riktig</b>{krav}</div></div></div>")
deler.append("</main></body></html>")
with open(os.path.join(ROT, "docs", "grafikk", "02-grafikk-utkast.html"), "w", encoding="utf-8") as f:
    f.write("\n".join(deler))
print("Skrev docs/grafikk/02-grafikk-utkast.html")

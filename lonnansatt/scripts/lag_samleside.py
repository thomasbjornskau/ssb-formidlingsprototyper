"""Lager docs/grafikk/02-grafikk-utkast.html: samleside for valget i steg 2."""

from pathlib import Path

ROT = Path(__file__).resolve().parents[1]


def svg(sti):
    return (ROT / sti).read_text(encoding="utf-8")


TRINN = [
    ("Arbeidsgiveren rapporterer", "Alle som betaler lønn, sender a-melding hver måned. Fulltelling, ikke utvalg. Forebygger at leseren tror tallene er et anslag.", "K2"),
    ("Én uke i november", "Jobbene som er aktive i uka med den 16. november og har fått lønn. Viser jobber mot heltidsekvivalenter med ekte tall (H3).", "K2, K6"),
    ("Lønna regnes om til heltid", "Regnestykket avtalt månedslønn + uregelmessige tillegg + bonus = 62 070 kr, med ekte tall fra 2025 (H1, H7).", "K2, K6"),
    ("Koblet, sikret og publisert", "Omkoding av yrke, registerkobling, undertrykking og revisjon av foreløpig årslønn: 5,0 ble 4,9 prosent (H4).", "K2, K10"),
]

VARIANTER = [
    ("A", "02-topp-a.svg", "Hva tjener de fleste? Gjennomsnitt, median og fordeling", "H2",
     "Bygger direkte på 13860 og 11419. «Minst 6 av 10» er vår avledning av desilgrensene og må godkjennes av fag (spørsmål 3 i innsiktsnotatet). Kan senere vise hvor et valgt yrke ligger i fordelingen."),
    ("B", "02-topp-b.svg", "Hva tjener et yrke?", "H3, H5, H8",
     "Bygger på 11418 på firesiffernivå. Svarer direkte på valget om at yrket styrer prototypen: velgeren kan utheve leserens yrke i stedet for de fire faste. Ett punkt per yrke vekter ikke etter antall jobber, og det må stå i grafikken. Grensene for hvilke yrker som vises, må avklares med fag."),
    ("C", "02-topp-c.svg", "Hvorfor finnes det flere tall for lønnsveksten?", "H4, H5",
     "Bygger på 11419, 11536 og 14858. Påløpt årslønn finnes bare for alle sektorer og står derfor i teksten, ikke i figuren. Hvem som eier 14858, og hva som ble endret i august, må avklares. TBUs tall er holdt utenfor fordi forhandlingsområdene ikke svarer til SSBs sektorer."),
]

kort_trinn = "\n".join(
    f"<li><strong>{t}.</strong> {b} <span class='k'>[{k}]</span></li>" for t, b, k in TRINN)

var_html = "\n".join(f"""
<section class="variant">
  <h3>Variant {v}</h3>
  <p class="spm"><strong>Spørsmål:</strong> {spm} · <strong>Hypoteser:</strong> {hyp}</p>
  <div class="figur">{svg('docs/grafikk/' + fil)}</div>
  <p class="bygg"><strong>Hva som må til:</strong> {bygg}</p>
</section>""" for v, fil, spm, hyp, bygg in VARIANTER)

html = f"""<!doctype html>
<html lang="nb">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>lonnansatt grafikkutkast</title>
<style>
  :root {{ --mork:#274246; --gra:#5e787a; --linje:#cdd3d4; --bak:#f3f5f5; }}
  body {{ margin:0; background:var(--bak); color:var(--mork);
         font-family:'Open Sans','Segoe UI',Arial,sans-serif; line-height:1.5; }}
  main {{ max-width:1240px; margin:0 auto; padding:24px 16px 64px; }}
  .status {{ font-size:13px; color:var(--gra); }}
  h1 {{ font-size:28px; margin:8px 0 4px; }}
  h2 {{ font-size:21px; margin:40px 0 8px; }}
  h3 {{ font-size:17px; margin:0 0 4px; }}
  .figur {{ background:#fff; border:1px solid var(--linje); overflow-x:auto; }}
  .figur svg {{ display:block; max-width:100%; height:auto; }}
  .smal {{ width:390px; max-width:100%; }}
  .variant {{ margin:24px 0 32px; }}
  .spm, .bygg {{ font-size:15px; margin:4px 0 8px; }}
  ol li {{ margin-bottom:6px; }}
  .k {{ color:var(--gra); font-size:13px; }}
  .rad {{ display:flex; gap:24px; align-items:flex-start; flex-wrap:wrap; }}
</style>
</head>
<body>
<main>
<p class="status">Steg 2 i formidlingsprototype for lonnansatt · versjon 1.0 · 15.10.2026 · Status: godkjent av Thomas (toppgrafikk A valgt, B blir yrkesseksjonen med velger)</p>
<h1>Grafikkutkast: Lønn</h1>
<p>Konseptgrafikken ligger bak «Slik lages tallene» i lesehjelpen. Toppgrafikken velges blant tre varianter. Tallene er hentet 15.10.2026 og byttes ut med rådataene i steg 3. Kildemerkene viser til innsiktsnotatet.</p>

<h2>Konseptgrafikk, bred</h2>
<div class="figur">{svg('src/konsept-bred.svg')}</div>
<ol>
{kort_trinn}
</ol>
<p><strong>Ikke med i månedslønna:</strong> overtid, naturalytelser og forsikringer, feriepenger og sluttvederlag, styrehonorar, skatt og selvstendig næringsdrivende. Boksen svarer på H1. Alt er hentet fra «Om statistikken», oppdatert 30.09.2026.</p>

<h2>Konseptgrafikk, smal</h2>
<div class="rad"><div class="figur smal">{svg('src/konsept-smal.svg')}</div></div>

<h2>Toppgrafikk</h2>
{var_html}
</main>
</body>
</html>
"""

(ROT / "docs" / "grafikk" / "02-grafikk-utkast.html").write_text(html, encoding="utf-8")
print("Ferdig")

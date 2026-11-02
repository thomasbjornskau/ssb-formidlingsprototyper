"""Lager docs/grafikk/02-grafikk-utkast.html: samleside for valget i steg 2."""

from pathlib import Path

ROT = Path(__file__).resolve().parents[1]


def svg(sti):
    return (ROT / sti).read_text(encoding="utf-8")


TRINN = [
    ("Behandlingen registreres", "Sykehus, private institusjoner med avtale og avtalespesialister rapporterer til Norsk pasientregister (NPR), som er eneste kilde. Ekte tall: 9 790 080 polikliniske kontakter i somatikken i 2025.", "K2, K4"),
    ("Koblet til person", "Kontaktene kobles til SSBs befolkningsregister, og de uten gyldig fødsels- eller D-nummer faller ut. 13 500 somatiske kontakter manglet personnummer i 2025, mot over 66 000 i 2015.", "K2"),
    ("Kontakter blir pasienter", "Statistikken teller personer, ikke behandlinger. Her ligger hovedforskjellen mot arkivserien fra 1999 (H10) og forklaringen på H3.", "K2"),
    ("Én gang per gruppe", "Unik telling per gruppe: diagnosekapitlene summerer til 5,16 millioner mot 2 716 218 pasienter. Trinnet bærer det gjennomgående valget og H2.", "K2, K4"),
    ("Avrundet og satt i forhold", "Avrunding til base 3 og rater per 1 000 innbyggere. Aldersjusteringen er bevisst holdt utenfor grafikken til spørsmål 2 i innsiktsnotatet er besvart (H4).", "K2, K4"),
]

VARIANTER = [
    ("A", "02-topp-a.svg", "1: Hvor mange får behandling, og hva får de?", "H1, H3",
     "Bygger direkte på 14824. Fire serier som indeks med direkte merking. Diagnosevelgeren kan styre alle fire linjene, for eksempel svulster eller skader. Korona-markeringen er vår, ikke et brudd i serien."),
    ("B", "02-topp-b.svg", "3: Hva behandles de for?", "H1, H2",
     "Bygger direkte på 14824 med kodelisten for hovedkategorier. Det uthevede kapitlet er stedet der velgeren virker: leseren velger kapittel, og stolpen og overskriften følger. De korte kapittelnavnene er våre og må godkjennes, eller byttes med SSBs fulle navn i velgeren."),
    ("C", "02-topp-c.svg", "2: Hvem er pasientene?", "H3, H4",
     "Krever egen beregning: rater per aldersgruppe med middelfolkemengde fra 07459 (snitt av 1. januar i året og året etter) og en dekomponering i rekkefølgen folketall, aldersstruktur, bruk. Totalraten treffer SSBs publiserte 450 og 484 eksakt, men SSB publiserer ikke ratene per alder. Fag må godta metoden før C kan brukes. Gjelder ikke diagnose direkte, men kan gjøres per kapittel."),
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
<title>pasient grafikkutkast</title>
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
<p class="status">Steg 2 i formidlingsprototype for pasient · versjon 1.0 · 02.11.2026 · Status: godkjent av Thomas (toppgrafikk A, konseptgrafikk godkjent)</p>
<h1>Grafikkutkast: Pasienter i spesialisthelsetjenesten</h1>
<p>Konseptgrafikken ligger bak «Slik lages tallene» i lesehjelpen. Toppgrafikken velges blant tre varianter. Det gjennomgående valget er diagnosekapittel. Tallene er hentet 02.11.2026 og byttes ut med rådataene i steg 3. Kildemerkene viser til innsiktsnotatet.</p>

<h2>Konseptgrafikk, bred</h2>
<div class="figur">{svg('src/konsept-bred.svg')}</div>
<ol>
{kort_trinn}
</ol>
<p><strong>Ikke med:</strong> psykisk helsevern for barn og unge og tverrfaglig rusbehandling (fra «Om statistikken», 19.06.2026), samt fastlege, kommunale tjenester, ventetid og kostnader (vår avgrensning). Boksen svarer på H1 og H6.</p>

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

"""Lager docs/grafikk/02-grafikk-utkast.html: samleside for valget i steg 2."""

from pathlib import Path

ROT = Path(__file__).resolve().parents[1]


def svg(sti):
    return (ROT / sti).read_text(encoding="utf-8")


TRINN = [
    ("Varen krysser grensen", "Tolldeklarasjoner for de fleste varer, egne kilder for olje og gass, strøm og skip. Forebygger at leseren tror tallene er anslag eller utvalg.", "K2"),
    ("Verdien settes ved grensen", "Eksport FOB, import CIF, uten toll og mva. Viser at olje og gass først får en anslått pris, som er en kilde til revisjon.", "K2, K3"),
    ("Fordelt på vare og land", "Mottakerland og opprinnelsesland, og fastlandseksporten som et regnestykke med ekte tall fra august 2026 (H4, H5).", "K2, K9"),
    ("Publisert, så revidert", "Juli 2026 ble 5,4 mrd. kr høyere en måned senere. Endelige tall kommer i mai to år etter (H6).", "K3, K11"),
]

VARIANTER = [
    ("A", "02-topp-a.svg", "Hvor mye av eksporten er olje og gass, og hvor mye er fastlandet?", "H2, H4",
     "Andelen er regnet av oss fra 08800. Kan bygges direkte i steg 3. Bør vise siste hele år, ikke siste måned, fordi månedsandelen svinger (63 prosent i august 2026)."),
    ("B", "02-topp-b.svg", "Hvorfor svinger eksportverdien så mye: pris eller mengde?", "H1, H9",
     "Bygger på volum- og prisindeksene i 06322, som har produsentprisindeksen som kontakt. Fag må bekrefte at indeksene kan brukes slik, og at «mengde» er et forsvarlig ord for volumindeksen. Påstanden om gass må sjekkes mot gassindeksen i steg 3."),
    ("C", "02-topp-c.svg", "Hva forteller handelsoverskuddet, og hvorfor har fastlandet underskudd?", "H2, H3, H7",
     "Kan bygges direkte fra 08800. Fag bør bekrefte at fastlandsbalansen er riktig motstykke til handelsoverskuddet, siden den trekker fra import av skip og plattformer, men ikke import av råolje."),
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
<title>muh grafikkutkast</title>
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
<p class="status">Steg 2 i formidlingsprototype for muh · versjon 1.0 · 14.10.2026 · Status: godkjent av Thomas (toppgrafikk C valgt)</p>
<h1>Grafikkutkast: Utenrikshandel med varer</h1>
<p>Konseptgrafikken ligger bak «Slik lages tallene» i lesehjelpen. Toppgrafikken velges blant tre varianter. Tallene er hentet 14.10.2026 og byttes ut med rådataene i steg 3. Kildemerkene viser til innsiktsnotatet.</p>

<h2>Konseptgrafikk, bred</h2>
<div class="figur">{svg('src/konsept-bred.svg')}</div>
<ol>
{kort_trinn}
</ol>
<p><strong>Ikke med:</strong> tjenester, renter og utbytte, transitt og småsendinger. Boksen svarer på H3. Grensen for småsendinger og transitt er fra 2015-versjonen av «Om statistikken» og må bekreftes.</p>

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

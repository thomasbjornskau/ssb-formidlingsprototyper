"""Samleside for steg 2: docs/grafikk/02-grafikk-utkast.html. Kjør etter lag_grafikk.py."""
import os, re
ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def svg(p):
    s = open(os.path.join(ROT, p), encoding="utf-8").read()
    return re.sub(r'width="\d+" height="\d+"', 'width="100%" style="height:auto;display:block"', s, count=1)

trinn = [
 ("Bosatt", "Bare personer registrert bosatt i Folkeregisteret telles: lovlig opphold og minst seks måneders planlagt botid. Asylsøkere er ikke med (H7)."),
 ("Hvor er du født?", "Kategorien avgjøres av fødeland for personen, foreldrene og besteforeldrene. Familietrærne viser forskjellen på innvandrer og norskfødt med innvandrerforeldre (H1, H2, H4)."),
 ("Seks kategorier", "Ekte andeler 1.1.2026 fra tabell 05182. De tre «andre»-kategoriene er slått sammen til 7,1 prosent for å holde trinnet lesbart (H3)."),
 ("Landbakgrunn", "Tre eksempler, ikke statistikk. Viser at landbakgrunn er fødeland, og regelen om morens fødeland."),
 ("Telles 1. januar", "Ekte regnskap for innvandrere i 2025 fra tabell 10516. «Andre endringer» (95) er differansen mot tilveksten, se kvalitetssikringen (H5)."),
]
var = [
 ("A", "Hvem regnes med?", "Spørsmål 1: Hvem regnes som innvandrer?", "H1, H2, H3, H4",
  "Kan bygges direkte fra 05182. Treffer de viktigste hypotesene. Fag må godkjenne at vi viser 21,8 og 28,9 prosent (spørsmål 4 i innsiktsnotatet). Kobles bare svakt til landbakgrunnsvalget."),
 ("B", "Tallet og trenden", "Spørsmål 2: Hvordan har antallet endret seg?", "H5",
  "Kan bygges fra 05182. Mest nøytral, men sier minst om definisjonene. Kan få en linje for valgt landbakgrunn (13880 har tall fra 2004, 05183 fra 1970)."),
 ("C", "Ti land, ulike generasjoner", "Spørsmål 3: Hvor kommer de fra, og når kom de?", "H9",
  "Passer best med landbakgrunn som gjennomgående valg: valgt land kan utheves eller legges til under de ti. Trenger landnavn og en avklaring av hvilke små grupper som kan vises (steg 3)."),
]
h = ['''<!doctype html><html lang="nb"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Innvandrere: grafikkutkast</title>
<style>
body{margin:0;background:#f3f5f5;color:#274246;font-family:"Open Sans","Segoe UI",Arial,sans-serif;line-height:1.5}
main{max-width:1240px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:28px;margin:8px 0 4px}h2{font-size:21px;margin:40px 0 8px}h3{font-size:17px;margin:0 0 4px}
.status{font-size:13px;color:#5e787a}.kort{background:#fff;border:1px solid #d9dfe0;padding:16px;margin:12px 0}
.trinn{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}.trinn div{background:#fff;border:1px solid #d9dfe0;padding:12px;font-size:14px}
.smal{max-width:390px}.meta{font-size:14px;color:#5e787a;margin:8px 0 0}.meta b{color:#274246}
</style></head><body><main>
<p class="status">Steg 2 i formidlingsprototype for innvbef · versjon 1.0 · 26.10.2026 · Status: godkjent av Thomas (variant B)</p>
<h1>Innvandrere og norskfødte med innvandrerforeldre: forslag til grafikk</h1>
<p>Konseptgrafikken ligger bak «Slik lages tallene» i lesehjelpen. Tre toppgrafikkvarianter svarer på hvert sitt prioriterte spørsmål fra innsiktsnotatet. Gjennomgående valg er landbakgrunn. Tallene er hentet fra statistikkbanken 26.10.2026 og erstattes av rådataene i steg 3.</p>
<h2>Konseptgrafikk, bred (1200 px)</h2><div class="kort">''', svg("src/konsept-bred.svg"), '</div><div class="trinn">']
for i,(t,f) in enumerate(trinn,1): h.append(f'<div><h3>{i}. {t}</h3>{f}</div>')
h.append('</div><h2>Konseptgrafikk, smal (390 px)</h2><div class="kort smal">'+svg("src/konsept-smal.svg")+'</div>')
h.append('<h2>Toppgrafikk: tre varianter</h2>')
for k,n,q,hy,v in var:
    h.append(f'<div class="kort"><h3>Variant {k}: {n}</h3>'+svg(f"docs/grafikk/02-topp-{k.lower()}.svg")+f'<p class="meta"><b>{q}</b> · Hypoteser: {hy}</p><p class="meta">{v}</p></div>')
h.append('</main></body></html>')
open(os.path.join(ROT,"docs","grafikk","02-grafikk-utkast.html"),"w",encoding="utf-8").write("\n".join(h))
print("ok")

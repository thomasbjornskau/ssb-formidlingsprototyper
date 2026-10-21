"""Samleside for steg 2: docs/grafikk/02-grafikk-utkast.html. Kjør etter lag_grafikk.py."""
import os, re
ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def svg(p):
    s = open(os.path.join(ROT, p), encoding="utf-8").read()
    return re.sub(r'width="\d+" height="\d+"', 'width="100%" style="height:auto;display:block"', s, count=1)

trinn = [
 ("Noe skjer", "Folketallet bygger på hendelser som meldes til Folkeregisteret: fødsler, dødsfall, flytting til og fra Norge og flytting mellom kommuner."),
 ("Bosatt eller ikke?", "Bare den som skal bo i Norge minst seks måneder, blir registrert som bosatt. Bostedet er der man har døgnhvile. Svarer på H1."),
 ("SSB teller", "SSB får endringene daglig og teller bosatte per 1. januar og ved hvert kvartal. Tidspunkt, ikke periode (H2)."),
 ("Regnskapet går opp", "Ekte tall for 2025: 5 594 340 + fødte − døde + innvandringer − utvandringer + korreksjon = 5 627 400. Viser hva korreksjonsposten er (H5, H10)."),
 ("Tallene publiseres", "Tallene følger registreringen. En opprydding i registeret kan samle utvandringer fra flere kvartaler i ett, som i 2. kvartal 2026 (H3)."),
]
var = [
 ("A", "Tallet og trenden", "Spørsmål 1: Hvor mange er vi, og hvor fort vokser vi?", "H2",
  "Kan bygges direkte fra tabell 05803. Mest nøytral, men minst forklarende: den sier at veksten faller, ikke hvorfor."),
 ("B", "Hva driver veksten", "Spørsmål 2: Hva driver veksten?", "H5, H6",
  "Kan bygges fra 05803. Må avklare med fag om korreksjonsposten kan utelates i stablingen. Svarer direkte på H5, at veksten skyldes fødsler."),
 ("C", "Kommunene spriker", "Spørsmål 4: Hvor vokser det, og hvor krymper det?", "H7, H9",
  "Passer best med «Min kommune» som gjennomgående valg: den valgte kommunen kan utheves i fordelingen. Trenger kommunenavn og avklaring av sammenslåtte tidsserier i steg 3."),
]
h = ['''<!doctype html><html lang="nb"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Folkemengde: grafikkutkast</title>
<style>
body{margin:0;background:#f3f5f5;color:#274246;font-family:"Open Sans","Segoe UI",Arial,sans-serif;line-height:1.5}
main{max-width:1240px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:28px;margin:8px 0 4px}h2{font-size:21px;margin:40px 0 8px}h3{font-size:17px;margin:0 0 4px}
.status{font-size:13px;color:#5e787a}.kort{background:#fff;border:1px solid #d9dfe0;padding:16px;margin:12px 0}
.trinn{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}.trinn div{background:#fff;border:1px solid #d9dfe0;padding:12px;font-size:14px}
.smal{max-width:390px}.meta{font-size:14px;color:#5e787a;margin:8px 0 0}.meta b{color:#274246}
</style></head><body><main>
<p class="status">Steg 2 i formidlingsprototype for folkemengde · versjon 0.1 · 21.10.2026 · Status: utkast</p>
<h1>Folkemengde: forslag til grafikk</h1>
<p>Konseptgrafikken ligger bak «Slik lages tallene» i lesehjelpen. Tre toppgrafikkvarianter svarer på hvert sitt prioriterte spørsmål fra innsiktsnotatet. Tallene er hentet fra statistikkbanken 21.10.2026 og erstattes av rådataene i steg 3.</p>
<h2>Konseptgrafikk, bred (1200 px)</h2><div class="kort">''', svg("src/konsept-bred.svg"), '</div><div class="trinn">']
for i,(t,f) in enumerate(trinn,1): h.append(f'<div><h3>{i}. {t}</h3>{f}</div>')
h.append('</div><h2>Konseptgrafikk, smal (390 px)</h2><div class="kort smal">'+svg("src/konsept-smal.svg")+'</div>')
h.append('<h2>Toppgrafikk: tre varianter</h2>')
for k,n,q,hy,v in var:
    h.append(f'<div class="kort"><h3>Variant {k}: {n}</h3>'+svg(f"docs/grafikk/02-topp-{k.lower()}.svg")+f'<p class="meta"><b>{q}</b> · Hypoteser: {hy}</p><p class="meta">{v}</p></div>')
h.append('</main></body></html>')
open(os.path.join(ROT,"docs","grafikk","02-grafikk-utkast.html"),"w",encoding="utf-8").write("\n".join(h))
print("ok")

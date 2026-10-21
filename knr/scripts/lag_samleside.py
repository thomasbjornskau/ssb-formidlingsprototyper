"""Samleside for steg 2: docs/grafikk/02-grafikk-utkast.html. Kjør etter lag_grafikk.py."""
import os, re
ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def svg(p):
    s = open(os.path.join(ROT, p), encoding="utf-8").read()
    return re.sub(r'width="\d+" height="\d+"', 'width="100%" style="height:auto;display:block"', s, count=1)

trinn = [
 ("Verdiskaping", "BNP regnet fra produksjonssiden: bruttoprodukt i Fastlands-Norge, oljevirksomhet og utenriks sjøfart, og produktavgifter. Tall for 2025 i milliarder kroner."),
 ("Samme BNP, brukt", "Den samme summen regnet fra anvendelsessiden: konsum, investering og eksport minus import. Begge sider gir 5 511 milliarder."),
 ("Fastlands-Norge", "Olje, gass, rør og utenriks sjøfart trekkes ut. Svarer på H1."),
 ("Kroner blir volum", "Løpende priser mot faste priser, med 2. kvartal 2026 som eksempel: +8,7 prosent i kroner og +2,0 prosent i volum. Svarer på H2 og H6."),
 ("Tallene modnes", "Kvartalstall, endelige årstall og hovedrevisjon. Svarer på H4 og H8."),
]
var = [
 ("A", "Tallet og trenden", "Spørsmål 1: Hvor fort vokser norsk økonomi nå?", "H1, H6",
  "Kan bygges direkte fra 09190. Viser SSBs hovedtall, men sier ikke at det finnes andre veksttall for samme kvartal."),
 ("B", "Fire tall for samme kvartal", "Spørsmål 1 og 4: Hvilket veksttall gjelder?", "H1, H3, H6",
  "Treffer den misforståelsen notatet rangerte høyest. Passer godt med makrostørrelse som valg: rutene kan vise hvilken som helst størrelse. Trenger ingen ny metode."),
 ("D", "Årlig vekst over tid", "Spørsmål 1: Hvor fort vokser norsk økonomi?", "H1, H4",
  "Lagt til etter ønske fra Thomas 21.10.2026. Klassisk tidsserie fra 1971 med Fastlands-BNP som stolper og BNP som strek. Foreløpige år (2024–2025) i lysere grønn. Kan bygges direkte fra 09189."),
 ("C", "Olje og gass i BNP", "Spørsmål 2: Hva er forskjellen på BNP og Fastlands-BNP?", "H1, H2",
  "Andelen er regnet av oss fra løpende priser i 09189. Må bekreftes av fag at «oljevirksomhet og utenriks sjøfart» er riktig mål på oljeandelen."),
]
h = ['''<!doctype html><html lang="nb"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nasjonalregnskap: grafikkutkast</title>
<style>
body{margin:0;background:#f3f5f5;color:#274246;font-family:"Open Sans","Segoe UI",Arial,sans-serif;line-height:1.5}
main{max-width:1240px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:28px;margin:8px 0 4px}h2{font-size:21px;margin:40px 0 8px}h3{font-size:17px;margin:0 0 4px}
.status{font-size:13px;color:#5e787a}.kort{background:#fff;border:1px solid #d9dfe0;padding:16px;margin:12px 0}
.trinn{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}.trinn div{background:#fff;border:1px solid #d9dfe0;padding:12px;font-size:14px}
.smal{max-width:390px}.meta{font-size:14px;color:#5e787a;margin:8px 0 0}.meta b{color:#274246}
</style></head><body><main>
<p class="status">Steg 2 i formidlingsprototype for knr · versjon 0.1 · 21.10.2026 · Status: utkast</p>
<h1>Nasjonalregnskap: forslag til grafikk</h1>
<p>Konseptgrafikken ligger bak «Slik lages tallene» i lesehjelpen. Tre toppgrafikkvarianter svarer på hvert sitt prioriterte spørsmål fra innsiktsnotatet. Tallene er hentet fra statistikkbanken 21.10.2026 og erstattes av rådataene i steg 3.</p>
<h2>Konseptgrafikk, bred (1200 px)</h2><div class="kort">''', svg("src/konsept-bred.svg"), '</div><div class="trinn">']
for i,(t,f) in enumerate(trinn,1): h.append(f'<div><h3>{i}. {t}</h3>{f}</div>')
h.append('</div><h2>Konseptgrafikk, smal (390 px)</h2><div class="kort smal">'+svg("src/konsept-smal.svg")+'</div>')
h.append('<h2>Toppgrafikk: tre varianter</h2>')
for k,n,q,hy,v in sorted(var, key=lambda x: x[0] != 'D'):
    h.append(f'<div class="kort"><h3>Variant {k}: {n}</h3>'+svg(f"docs/grafikk/02-topp-{k.lower()}.svg")+f'<p class="meta"><b>{q}</b> · Hypoteser: {hy}</p><p class="meta">{v}</p></div>')
h.append('</main></body></html>')
open(os.path.join(ROT,"docs","grafikk","02-grafikk-utkast.html"),"w",encoding="utf-8").write("\n".join(h))
print("ok")

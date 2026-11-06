"""Samleside for steg 2: docs/grafikk/02-grafikk-utkast.html. Kjør etter lag_grafikk.py."""
import os, re
ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def svg(p):
    s = open(os.path.join(ROT, p), encoding="utf-8").read()
    return re.sub(r'width="\d+" height="\d+"', 'width="100%" style="height:auto;display:block"', s, count=1)


trinn = [
    ("Telt i registrene", "12 indikatorer: personer, husholdninger, boliger og bygg telles i registrene og føres til kommunen. Ingen kart."),
    ("Rapportert av kommunen", "4 indikatorer fra KOSTRA: dispensasjoner i 100-metersbeltet, omdisponert og nydyrket jord. Omdisponering gjelder alle formål, også landbruk."),
    ("Plassert i kartet", "18 indikatorer: bygninger og bosatte holdes opp mot tettsted, sentrumssone, arbeidsplassklynger, strandsone, fareområder, arealbruk og trygge gangveier til natur."),
    ("Planen mot virkeligheten", "1 indikator: kommuneplanens arealdel lagt over kartet over faktisk arealbruk. Det som er satt av, men ikke bygd, er reserven (H7)."),
]
var = [
    ("A", "Tettere boligbygging", "Spørsmål 2: Bygger vi tettere og nærmere sentrum?", "H2, H6",
     "Kan bygges fra 14478 (A6–A8). Andelene for landet er egne beregninger, vektet med antall nye boliger, fordi tabellen mangler landstall. Hvilke fire år «fram til 2026» dekker, må bekreftes i steg 3."),
    ("B", "Jordvern", "Spørsmål 3: Hvor mye jord, strand og natur bygges ned?", "H2, H9",
     "Avviket er forklart i steg 3: arealprofilenes C3 gjelder alle formål, kofola og jordvernmålet andre formål enn landbruk. Som seksjon må den bruke tabell 11776 for landstallet."),
    ("C", "Min kommune", "Spørsmål 1: Hvordan står min kommune mot lignende kommuner?", "H3, H4, H5, H6",
     "Valgt av Thomas 06.11.2026. Viser grepet som skal bære hele prototypen: kommunen mot spredningen i sin sentralitetsklasse og mot landsmedianen. Setningen må lages automatisk per kommune, og det krever regler for hva som kan sies uten å rangere."),
]
h = ['''<!doctype html><html lang="nb"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Arealprofiler: grafikkutkast</title>
<style>
body{margin:0;background:#f3f5f5;color:#274246;font-family:"Open Sans","Segoe UI",Arial,sans-serif;line-height:1.5}
main{max-width:1240px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:28px;margin:8px 0 4px}h2{font-size:21px;margin:40px 0 8px}h3{font-size:17px;margin:0 0 4px}
.status{font-size:13px;color:#5e787a}.kort{background:#fff;border:1px solid #d9dfe0;padding:16px;margin:12px 0}
.trinn{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}.trinn div{background:#fff;border:1px solid #d9dfe0;padding:12px;font-size:14px}
.smal{max-width:390px}.meta{font-size:14px;color:#5e787a;margin:8px 0 0}.meta b{color:#274246}
</style></head><body><main>
<p class="status">Steg 2 i formidlingsprototype for arealprofiler · versjon 0.2 · 06.11.2026 · Status: toppgrafikk C valgt av Thomas, ny konseptgrafikk til godkjenning</p>
<h1>Arealprofiler: forslag til grafikk</h1>
<p>Konseptgrafikken ligger bak «Slik lages tallene» i lesehjelpen. Tre toppgrafikkvarianter svarer på hvert sitt prioriterte spørsmål fra innsiktsnotatet. Tallene er fra fjorårets datagrunnlag (Arealprofiler 2025, publisert 29.08.2025), valgt som kilde 06.11.2026. Versjon 0.2 har ny konseptgrafikk som dekker alle 35 indikatorene: versjon 0.1 forklarte bare de kartbaserte. Lillehammer er eksempelkommune: Bærum, som er standard i dagens app, ligger i en sentralitetsklasse med bare fem kommuner.</p>
<h2>Konseptgrafikk, bred (1200 px)</h2><div class="kort">''', svg("src/konsept-bred.svg"), '</div><div class="trinn">']
for i, (t, f) in enumerate(trinn, 1):
    h.append(f'<div><h3>{i}. {t}</h3>{f}</div>')
h.append('</div><h2>Konseptgrafikk, smal (390 px)</h2><div class="kort smal">' + svg("src/konsept-smal.svg") + '</div>')
h.append('<h2>Toppgrafikk: tre varianter</h2>')
for k, n, q, hy, v in var:
    h.append(f'<div class="kort"><h3>Variant {k}: {n}</h3>' + svg(f"docs/grafikk/02-topp-{k.lower()}.svg") +
             f'<p class="meta"><b>{q}</b> · Hypoteser: {hy}</p><p class="meta">{v}</p></div>')
h.append('</main></body></html>')
open(os.path.join(ROT, "docs", "grafikk", "02-grafikk-utkast.html"), "w", encoding="utf-8").write("\n".join(h))
print("ok")

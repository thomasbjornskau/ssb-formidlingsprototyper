"""Samleside for steg 2: docs/grafikk/02-grafikk-utkast.html med SVG-ene lagt inn direkte."""
import pathlib

ROT = pathlib.Path(__file__).resolve().parents[1]
G = ROT / "docs" / "grafikk"


def svg(p):
    t = (ROT / p).read_text(encoding="utf-8")
    return t.replace("<svg ", '<svg style="width:100%;height:auto;display:block" ', 1)


VARIANTER = [
    ("A", "02-topp-A.svg", "Hva betyr det å være «utenfor»?", "Prioritet 1 · H2, H7",
     "Én stolpe delt i de fire statusene som til sammen er NEET. Viser at «utenfor» ikke er én gruppe, og at "
     "ukjent status er den største delen.",
     "Kan bygges direkte fra 12424. Trygg som inngang, men forteller ikke noe om utvikling."),
    ("B", "02-topp-B.svg", "Er utenforskapet tyngre enn før?", "Prioritet 2 · H3, H10",
     "Stablede stolper 2008–2025: AAP/uføretrygd i grønt, resten i grått. Totalen er nokså stabil, den grønne delen vokser.",
     "Grafikken sier bare at sammensetningen har endret seg, ikke at folk er utenfor lenger. Før bygging må fag "
     "bekrefte at AAP og uføretrygd er sammenlignbare tilbake til 2008 (AAP-reformen 2010, uførereformen 2015). "
     "Hvis ikke: start serien i 2010 eller marker brudd."),
    ("C", "02-topp-C.svg", "Innvandrere og befolkningen ellers", "Prioritet 3 · H4, H5",
     "To 100-prosentstolper med samme fire statuser. Viser at innvandrere oftere er utenfor, men at innholdet er et annet.",
     "Kan bygges direkte. Bør få en setning om at ukjent status delvis kan være uregistrert utvandring, "
     "men den påstanden kommer fra SSBs metodetekst, ikke fra tabellen."),
]

SEKSJONER = [
    ("Lesehjelp", "Konseptgrafikken over, bak «Slik lages tallene». Med den stiplede boksen om hva som ikke er med."),
    ("Utvikling for din gruppe", "Linjediagram 2008–2025: NEET-andel for gruppen valgt i gruppevelgeren, mot alle unge i grått. "
     "Under: samme stablede sammensetning som i B, for den valgte gruppen. Svarer på prioritet 2 per gruppe."),
    ("Kjønn og alder", "Små multipler, tre ruter (15–19, 20–24, 25–29 år) med én linje for kvinner og én for menn. "
     "Viser at kjønnsforskjellen snur med alder. Felles y-akse."),
    ("Hvem er i størst fare?", "Seksjonsforslag D under. Plassert etter hvor stor andel som er utenfor og hvor stor del av dem som er "
     "på AAP/uføretrygd. Prioritet 5."),
    ("Aldersgruppen gjennom tid", "Pseudokohort for befolkningen ekskl. innvandrere: 15–19-åringer i 2008, 2010 og 2015 fulgt "
     "fem og ti år fram. Stiger AAP/uføre-andelen raskere for de seneste kullene? Merkes tydelig: dette er aldersgrupper, "
     "ikke de samme personene. Bør vurderes av fag før det kommer med (H8)."),
    ("Påstandsprøven", "Kort for artikkelforfatteren, ikke diagram: typiske påstander merket «støttet av tabellen», "
     "«bare som tolkning» eller «ikke støttet». For eksempel er «20 000 unge blir NEET hvert år» ikke støttet."),
]

css = """
:root{--t:#274246;--s:#5e787a;--l:#d9dfe0;--g:#00824d;--bg:#f3f5f5}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--t);font:16px/1.5 'Open Sans','Segoe UI',Arial,sans-serif}
main{max-width:1240px;margin:0 auto;padding:24px 16px 64px}
h1{font-family:'Roboto Condensed','Arial Narrow',Arial,sans-serif;font-size:34px;margin:0 0 4px}
h2{font-family:Roboto,Arial,sans-serif;font-size:22px;margin:40px 0 8px}
h3{font-family:Roboto,Arial,sans-serif;font-size:18px;margin:0 0 4px}
.status{color:var(--s);font-size:14px;margin:0 0 20px}
.kort{background:#fff;border-top:5px solid var(--g);padding:16px;margin:12px 0}
.meta{color:var(--s);font-size:14px;margin:0 0 8px}
.trinn{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-top:12px}
.trinn div{background:#fff;padding:12px;border-left:5px solid var(--g)}
.smal{max-width:390px}
ul{padding-left:20px}li{margin:6px 0}
.krav{background:#fff;border:1px dashed #b9c5c6;padding:10px 12px;font-size:15px}
"""

h = [f"<!doctype html><html lang='no'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
     f"<title>Unge utenfor – grafikk</title><style>{css}</style></head><body><main>",
     "<h1>Unge utenfor: forslag til grafikk</h1>",
     "<p class='status'>Steg 2 i formidlingsprototype for arbstatus-neet · versjon 0.1 · 10.11.2026 · Status: godkjent av Thomas 10.11.2026 (konsept godkjent, toppgrafikk B; C og D blir seksjoner). "
     "Avgrenset til det tabell 12424 kan besvare. Alle tall er regnet fra tabellen, hentet 10.11.2026.</p>",
     "<h2>Konseptgrafikk: Slik lages tallene</h2><div class='kort'>", svg("src/konsept-bred.svg"), "</div>",
     "<div class='trinn'>",
     "<div><h3>1 Alle unge som bor i Norge</h3>Utgangspunktet er alle registrert bosatte 15–29 år i november. Ikke et utvalg.</div>",
     "<div><h3>2 Én status per person</h3>Prioriteringen avgjør hvor folk havner. Eksempelet med studenten på uføretrygd "
     "svarer på H7.</div>",
     "<div><h3>3 Utenfor = NEET</h3>Viser at NEET er en sum av fire statuser, med ekte tall for 2025. "
     "Det er grunnlaget for alle toppgrafikkene.</div>",
     "<div><h3>4 Fordelt på grupper</h3>De fire dimensjonene i tabellen, som gruppevelgeren bygger på.</div>",
     "</div><p class='meta' style='margin-top:12px'>Den stiplede boksen er H1: det tabellen ikke kan si.</p>",
     "<h3 style='margin-top:24px'>Smal versjon (mobil)</h3><div class='kort smal'>", svg("src/konsept-smal.svg"), "</div>",
     "<h2>Toppgrafikk: tre varianter</h2>"]
for kode, fil, sp, pri, hva, krav in VARIANTER:
    h += [f"<div class='kort'><h3>{kode} · {sp}</h3><p class='meta'>{pri}</p>", svg(f"docs/grafikk/{fil}"),
          f"<p>{hva}</p><p class='krav'><strong>For å bygge riktig:</strong> {krav}</p></div>"]
h += ["<h2>Forslag til seksjoner under toppgrafikken</h2><div class='kort'><ul>"]
h += [f"<li><strong>{t}.</strong> {x}</li>" for t, x in SEKSJONER]
h += ["</ul></div><h3>Seksjonsforslag D · Hvem er i størst fare?</h3><p class='meta'>Prioritet 5 · H2, H4, H9</p>",
      "<div class='kort'>", svg("docs/grafikk/02-seksjon-D.svg"),
      "<p class='krav'><strong>For å bygge riktig:</strong> Aksen «andel på AAP eller uføretrygd» er et mål på sammensetning, "
      "ikke på risiko eller varighet. Gruppevelgeren kan bytte alder og kjønn. Gruppene med uoppgitt utdanning er små og "
      "bør få en merknad.</p></div>",
      "</main></body></html>"]
(G / "02-grafikk-utkast.html").write_text("\n".join(h), encoding="utf-8")
print("ok")

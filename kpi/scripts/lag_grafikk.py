"""Steg 2 for kpi: konseptgrafikk og tre varianter av toppgrafikk.

Bruk, fra roten av repoet:
    python kpi/scripts/lag_grafikk.py

Leser kpi/data/grafikk-utkast.json. Skriver SVG-filer til kpi/src/ og
kpi/docs/grafikk/, og en samleside til kpi/docs/grafikk/02-grafikk-utkast.html.
"""
import json
import pathlib
import sys

ROT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROT / "felles"))
from grafikk import (BG_FLATE, BG_FLATE_S, BLA, BLEKK, DEMPET, GRA, GRONN, GRONN_MORK, GRONN_XL, MORK, NULL,  # noqa: E402
                     STOTTE, UTENFOR, UTENFOR_BG, Svg, bryt, nb, sgn)

K = ROT / "kpi"
D = json.loads((K / "data" / "grafikk-utkast.json").read_text(encoding="utf8"))
GR = sorted(D["grupper"], key=lambda g: -g[3])
VEKT_SUM = sum(g[3] for g in GR)
BEREGNET = D["beregnet_husleie_vekt"]
I = D["indeks"]
SIST_TOLV = D["tolv"]["KPI"][-1]
SIST_JAE = D["tolv"]["KPI-JAE"][-1]


def mnd_liste():
    aar, m = int(D["tolv_fra"][:4]), int(D["tolv_fra"][5:])
    ut = []
    for _ in D["tolv"]["KPI"]:
        ut.append((aar, m))
        m += 1
        if m > 12:
            aar, m = aar + 1, 1
    return ut


MND = mnd_liste()
MNDNAVN = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"]
TOPP = max(range(len(MND)), key=lambda i: D["tolv"]["KPI"][i])


def handlekurv(s, x0, y0, w, h, etikett_over=True, smal=False):
    """Stablet stolpe med vektene. De tre største i grønt, resten grått, beregnet husleie markert."""
    x = x0
    for i, (kode, _, kort, vekt, _) in enumerate(GR):
        bw = w * vekt / VEKT_SUM
        farge = GRONN if i < 3 else DEMPET
        s.rect(x, y0, bw - 1.5, h, farge)
        if kode == "04":
            bh = w * BEREGNET / VEKT_SUM
            s.rect(x, y0, bh, h, GRONN_MORK)
            ly = y0 + h + 18
            s.line(x, y0 + h + 4, x + bh, y0 + h + 4, MORK, 1)
            s.text(x, ly, f"herav beregnet husleie for selveiere: {nb(BEREGNET / 10, 1)} %", 13 if smal else 14, MORK)
        if i < 3:
            ty = y0 - 10 if etikett_over else y0 + h + 40
            s.text(x, ty, f"{kort} {nb(vekt / 10, 1)} %", 13 if smal else 15, MORK, 700)
        x += bw
    rest = sum(g[3] for g in GR[3:])
    s.text(x0 + w, y0 - 10 if etikett_over else y0 + h + 40, f"{len(GR) - 3} andre grupper {nb(rest / 10, 1)} %", 13 if smal else 15, GRA, 400, "end")


def konsept_bred():
    s = Svg(1400, 680, "Slik lages konsumprisindeksen")
    # 1 Innsamling
    s.markor(30, 52, 1)
    s.rect(50, 36, 420, 196, GRONN_XL, GRONN, rx=6)
    s.text(70, 66, "Priser samles inn hver måned", 18, MORK, 700)
    kilder = ["Strekkoder fra kassene i dagligvarebutikker,", "apotek og bensinstasjoner",
              "Undersøkelse blant knapt 2 000 virksomheter", "Husleie fra om lag 2 500 utleieboliger",
              "Strømpriser fra nettet, bilpriser fra OFV"]
    y = 96
    for i, t in enumerate(kilder):
        if i != 1:
            s.circle(76, y - 5, 3, GRONN)
        s.text(88, y, t, 15, MORK)
        y += 26 if i != 0 else 22
    s.pil(470, 134, 516, 134, BLEKK)
    # 2 Prisendring per vare
    s.markor(500, 52, 2)
    s.rect(520, 36, 420, 196, BG_FLATE, BG_FLATE_S, rx=6)
    s.text(540, 66, "Samme vare sammenlignes over tid", 18, MORK, 700)
    s.linjer(540, 92, ["Prisendringen beregnes for hver vare.", "Tilbud og rabatter er med."], 15, MORK)
    # Eksempel med to prislapper
    for j, (mnd, pris) in enumerate((("August", "30,00 kr"), ("September", "31,20 kr"))):
        px = 540 + j * 200
        s.rect(px, 146, 150, 52, "#fff", BG_FLATE_S, rx=4)
        s.text(px + 12, 166, mnd, 13, GRA)
        s.text(px + 12, 188, pris, 17, MORK, 700)
    s.pil(694, 172, 736, 172, BLEKK, 1.5)
    s.text(895, 178, "+4,0 %", 17, GRONN, 700, "end")
    s.text(540, 220, "Eksempeltall, ikke statistikk", 12, GRA)
    # 3 Vekter
    s.pil(730, 232, 730, 270, BLEKK)
    s.markor(30, 300, 3)
    s.text(50, 296, "Prisendringene veies etter hvor mye husholdningene bruker på hver gruppe", 18, MORK, 700)
    handlekurv(s, 50, 350, 1300, 46)
    s.text(50, 446, "Vektene kommer fra nasjonalregnskapet og oppdateres hver januar. Vekter for 2026, prosent av samlet forbruk.", 14, GRA)
    # 4 Resultat
    s.pil(1050, 460, 1050, 500, BLEKK)
    s.markor(740, 518, 4)
    s.rect(760, 500, 590, 160, "#fff", GRONN, rx=6)
    s.text(780, 532, "Én indeks for alt husholdningene kjøper", 18, MORK, 700)
    s.text(780, 572, f"Indeks september 2026: {nb(I['2026M09'], 1)}", 17, MORK)
    s.text(780, 596, "(gjennomsnittet for 2025 = 100)", 14, GRA)
    s.text(780, 636, f"= {nb(SIST_TOLV, 1)} prosent høyere enn september 2025", 17, GRONN, 700)
    # Ikke med
    s.rect(50, 500, 660, 160, UTENFOR_BG, UTENFOR, rx=6, dash="6 5")
    s.text(70, 532, "Ikke med i KPI", 18, MORK, 700)
    s.linjer(70, 562, ["Kjøp av bolig og boligprisene. Det regnes som investering.",
                       "Selveiere er med gjennom beregnet husleie: hva det ville",
                       "kostet å leie den samme boligen.",
                       "Renter og avdrag på lån."], 15, GRA, lh=1.45)
    return s


def konsept_smal():
    s = Svg(390, 1150, "Slik lages konsumprisindeksen")
    x0, w = 44, 330
    s.markor(22, 30, 1)
    s.rect(x0, 14, w, 196, GRONN_XL, GRONN, rx=6)
    s.text(x0 + 14, 40, "Priser samles inn hver måned", 15, MORK, 700)
    y = 66
    for t in ["Strekkoder fra kassene i dagligvare-", "butikker, apotek og bensinstasjoner", "Undersøkelse blant knapt 2 000", "virksomheter", "Husleie fra om lag 2 500 utleieboliger", "Strømpriser fra nettet, bilpriser fra OFV"]:
        if not t[0].islower() and t not in ("butikker, apotek og bensinstasjoner", "virksomheter"):
            s.circle(x0 + 18, y - 4, 2.5, GRONN)
        s.text(x0 + 28, y, t, 13, MORK)
        y += 22
    s.pil(x0 + w / 2, 210, x0 + w / 2, 240, BLEKK)
    s.markor(22, 260, 2)
    s.rect(x0, 244, w, 190, BG_FLATE, BG_FLATE_S, rx=6)
    s.text(x0 + 14, 270, "Samme vare sammenlignes over tid", 15, MORK, 700)
    s.linjer(x0 + 14, 294, ["Prisendringen beregnes for hver vare.", "Tilbud og rabatter er med."], 13, MORK)
    for j, (mnd, pris) in enumerate((("August", "30,00 kr"), ("September", "31,20 kr"))):
        px = x0 + 14 + j * 150
        s.rect(px, 330, 120, 48, "#fff", BG_FLATE_S, rx=4)
        s.text(px + 10, 348, mnd, 12, GRA)
        s.text(px + 10, 369, pris, 15, MORK, 700)
    s.text(x0 + w - 14, 404, "+4,0 %", 15, GRONN, 700, "end")
    s.text(x0 + 14, 422, "Eksempeltall, ikke statistikk", 12, GRA)
    s.pil(x0 + w / 2, 434, x0 + w / 2, 464, BLEKK)
    s.markor(22, 484, 3)
    s.linjer(x0, 482, ["Prisendringene veies etter hvor mye", "husholdningene bruker på hver gruppe"], 14, MORK, 700)
    # Smal handlekurv: liste med stolper
    y = 540
    rest = 0
    for i, (kode, _, kort, vekt, _) in enumerate(GR):
        if i < 3:
            s.text(x0, y, kort, 13, MORK, 700)
            s.text(x0 + w, y, f"{nb(vekt / 10, 1)} %", 13, MORK, 700, "end")
            s.rect(x0, y + 6, w * vekt / 450, 14, GRONN)
            if kode == "04":
                s.rect(x0, y + 6, w * BEREGNET / 450, 14, GRONN_MORK)
                s.text(x0, y + 38, f"herav beregnet husleie {nb(BEREGNET / 10, 1)} %", 12, MORK)
                y += 18
            y += 46
        else:
            rest += vekt
    s.text(x0, y, f"{len(GR) - 3} andre grupper", 13, GRA)
    s.text(x0 + w, y, f"{nb(rest / 10, 1)} %", 13, GRA, 400, "end")
    s.rect(x0, y + 6, w * rest / 450, 14, DEMPET)
    y += 44
    s.linjer(x0, y, ["Vekter for 2026, fra nasjonalregnskapet.", "Oppdateres hver januar."], 12, GRA)
    y += 30
    s.pil(x0 + w / 2, y, x0 + w / 2, y + 30, BLEKK)
    y += 34
    s.markor(22, y + 16, 4)
    s.rect(x0, y, w, 130, "#fff", GRONN, rx=6)
    s.text(x0 + 14, y + 26, "Én indeks for alt", 15, MORK, 700)
    s.text(x0 + 14, y + 56, f"September 2026: {nb(I['2026M09'], 1)}", 15, MORK)
    s.text(x0 + 14, y + 76, "(gjennomsnittet for 2025 = 100)", 12, GRA)
    s.linjer(x0 + 14, y + 104, [f"= {nb(SIST_TOLV, 1)} prosent høyere enn", "september 2025"], 14, GRONN, 700, lh=1.3)
    y += 146
    s.rect(x0, y, w, 128, UTENFOR_BG, UTENFOR, rx=6, dash="6 5")
    s.text(x0 + 14, y + 26, "Ikke med i KPI", 15, MORK, 700)
    s.linjer(x0 + 14, y + 50, ["Kjøp av bolig og boligprisene.", "Selveiere er med gjennom beregnet", "husleie.", "Renter og avdrag på lån."], 13, GRA)
    s.h = y + 140
    return s


# ---------- Toppgrafikk ----------
B, HT = 1200, 330


def hode(s, etikett, stort, linje, under):
    s.text(0, 30, etikett.upper(), 13, GRA, 700)
    s.text(0, 84, stort, 44, MORK, 700)
    s.text(0, 124, linje, 20, MORK)
    s.linjer(0, 166, under, 15, GRA, lh=1.45)


def variant_trend():
    s = Svg(B, HT, "Tolvmånedersvekst i KPI og KPI-JAE 2015–2026")
    t = MND[TOPP]
    hode(s, "Konsumprisindeksen · september 2026", f"{nb(SIST_TOLV, 1)} prosent",
         "høyere priser enn for ett år siden",
         [f"Underliggende prisvekst (KPI-JAE): {nb(SIST_JAE, 1)} prosent.",
          f"Toppen var {nb(D['tolv']['KPI'][TOPP], 1)} prosent i {MNDNAVN[t[1] - 1]} {t[0]}."])
    x0, x1, y0, y1 = 640, 1050, 44, 290
    hi = 8
    X = lambda i: x0 + (x1 - x0) * i / (len(MND) - 1)
    Y = lambda v: y1 - (y1 - y0) * v / hi
    s.text(x0, y0 - 18, "Endring fra samme måned året før, prosent", 13, GRA)
    for v in range(0, hi + 1, 2):
        s.line(x0, Y(v), x1, Y(v), NULL if v == 0 else STOTTE, 1)
        s.text(x0 - 8, Y(v) + 4, nb(v), 12, GRA, 400, "end")
    for aar in (2015, 2020, 2026):
        i = MND.index((aar, 1)) if aar != 2026 else len(MND) - 1
        s.text(X(i), y1 + 20, str(aar), 12, GRA, 400, "middle" if aar == 2020 else ("start" if aar == 2015 else "end"))
    for navn, farge, bredde in (("KPI-JAE", BLA, 2), ("KPI", GRONN, 2.5)):
        v = D["tolv"][navn]
        s.path("M " + " L ".join(f"{X(i):.1f} {Y(x):.1f}" for i, x in enumerate(v)), stroke=farge, sw=bredde)
    ender = sorted([(Y(SIST_TOLV), "KPI", GRONN), (Y(SIST_JAE), "KPI-JAE", BLA)])
    if ender[1][0] - ender[0][0] < 18:
        ender[1] = (ender[0][0] + 18, ender[1][1], ender[1][2])
    for y, t_, f in ender:
        s.text(x1 + 10, y + 5, f"{t_} {nb(SIST_TOLV if t_ == 'KPI' else SIST_JAE, 1)}", 13, MORK, 700)
    s.circle(X(TOPP), Y(D["tolv"]["KPI"][TOPP]), 4, GRONN)
    return s


def variant_kroner():
    s = Svg(B, HT, "Hva 100 kroner i 2015 tilsvarer i dag")
    k = {a: 100 * I[f"{a}M09"] / I["2015M09"] for a in (2015, 2020, 2025, 2026)}
    hode(s, "Konsumprisindeksen · september 2026", f"{nb(round(k[2026]))} kroner",
         "for det som kostet 100 kroner i september 2015",
         ["Gjennomsnitt for alt husholdningene kjøper.",
          f"Siste tolv måneder: 100 kroner ble {nb(100 + SIST_TOLV, 2)}."])
    x0, y0, y1 = 660, 50, 280
    hi = 160
    Y = lambda v: y1 - (y1 - y0) * v / hi
    s.line(x0 - 10, y1, x0 + 4 * 110, y1, NULL, 1)
    s.text(x0 - 10, y0 - 22, "Kroner, september hvert år", 13, GRA)
    for j, (aar, v) in enumerate(k.items()):
        x = x0 + j * 110
        s.rect(x, Y(v), 64, y1 - Y(v), GRONN if aar == 2026 else DEMPET)
        s.text(x + 32, Y(v) - 8, nb(round(v)), 15, MORK, 700, "middle")
        s.text(x + 32, y1 + 20, str(aar), 13, GRA, 400, "middle")
    return s


def variant_bidrag():
    s = Svg(B, HT, "Bidrag til prisveksten fra hver gruppe, september 2026")
    bid = sorted(((g[3] * g[4] / 1000, g[2]) for g in GR), reverse=True)
    topp = bid[:3]
    rest = sum(b for b, _ in bid[3:])
    tot = sum(b for b, _ in bid)
    hode(s, "Konsumprisindeksen · september 2026", f"{nb(SIST_TOLV, 1)} prosent",
         "Bolig og strøm står for om lag en tredel av prisveksten",
         ["Bidrag til tolvmånedersveksten, prosentpoeng.",
          f"Grovt anslag (vekt × endring) som summerer til {nb(tot, 1)}, ikke {nb(SIST_TOLV, 1)}.",
          "Beregnes med SSBs metode i steg 3."])
    x0, x1, y = 560, 1180, 150
    skala = (x1 - x0) / tot
    x = x0
    s.text(x0, y + 96, "Bidrag i prosentpoeng", 13, GRA)
    for j, (b, navn) in enumerate(topp + [(rest, f"{len(bid) - 3} andre grupper")]):
        w = b * skala
        s.rect(x, y - 30, w - 2, 46, GRONN if j == 0 else DEMPET)
        s.text(x + 8, y - 1, nb(b, 1), 15, "#fff" if j == 0 else MORK, 700)
        if w >= 110:
            for k_, l in enumerate(bryt(navn, w - 8, 13)):
                s.text(x + 4, y + 36 + k_ * 17, l, 13, MORK)
        else:
            s.line(x + w / 2, y - 34, x + w / 2, y - 46, MORK, 1)
            s.text(x + w / 2, y - 52, navn, 13, MORK, 400, "middle")
        x += w
    return s


def bygg():
    ut = K / "docs" / "grafikk"
    ut.mkdir(parents=True, exist_ok=True)
    bred, smal = konsept_bred(), konsept_smal()
    (K / "src" / "konsept-bred.svg").write_text(bred.svg(), encoding="utf8")
    (K / "src" / "konsept-smal.svg").write_text(smal.svg(), encoding="utf8")
    varianter = [("trend", "A. Tallet og trenden", variant_trend(), "Svarer på spørsmål 1. Viser siste tall i lys av de siste ti årene og skiller KPI fra KPI-JAE (H1, H4, H6)."),
                 ("kroner", "B. Hva 100 kroner er blitt", variant_kroner(), "Svarer på spørsmål 5. Konkret og lett å huske, men sier lite om dagens prisvekst."),
                 ("bidrag", "C. Hva som driver prisveksten", variant_bidrag(), "Svarer på spørsmål 2. Viser at vekt betyr mer enn endring (H7), men bygger her på et grovt anslag.")]
    seksjoner = []
    for vid, tittel, svg, tekst in varianter:
        (ut / f"02-topp-{vid}.svg").write_text(svg.svg(), encoding="utf8")
        seksjoner.append(f"<section><h2>{tittel}</h2><p>{tekst}</p><figure>{svg.svg()}</figure></section>")
    font = (ROT / "felles" / "vendor" / "opensans.css").read_text(encoding="utf8")
    html = f"""<!doctype html><html lang="nb"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>KPI steg 2: grafikk</title><link rel="icon" href="data:,"><style>{font}
body{{margin:0;background:#f3f5f5;color:{MORK};font-family:'Open Sans',system-ui,sans-serif;font-size:15px;line-height:1.5}}
main{{max-width:1280px;margin:0 auto;padding:32px 24px;display:grid;gap:28px}} h1{{font-size:28px;margin:0}} h2{{font-size:18px;margin:0 0 4px}}
p{{margin:0 0 12px;color:{GRA};max-width:62rem}} section{{background:#fff;padding:24px}} figure{{margin:0}} figure svg,.k svg{{width:100%;height:auto;display:block}}
.smal{{max-width:390px}} ol{{margin:16px 0 0;padding-left:1.2em;display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:10px 28px}}
</style></head><body><main>
<header><h1>KPI, steg 2: konseptgrafikk og toppgrafikk</h1><p>Utkast til vurdering, 14.10.2026. Tallene er fra SSB, tabell 14700 og 14706, hentet 14.10.2026. Beskrivelsen av innsamling og vekter bygger på «Om statistikken» for KPI og artiklene om matvareindeksen og bokostnader.</p></header>
<section><h2>Konseptgrafikk: slik lages KPI</h2><div class="k">{bred.svg()}</div>
<ol><li><b>Priser samles inn</b> hver måned fra butikkenes kasser, fra virksomheter, fra utleieboliger og fra nettet.</li>
<li><b>Samme vare sammenlignes</b> fra måned til måned, slik at prisendringen ikke blandes med at vi kjøper andre ting.</li>
<li><b>Endringene veies</b> etter hvor mye husholdningene bruker på hver gruppe. Bolig veier mest.</li>
<li><b>Resultatet er én indeks.</b> Prisveksten leses som endringen fra samme måned året før.</li></ol></section>
<section><h2>Konseptgrafikk, smal versjon for mobil</h2><div class="k smal">{smal.svg()}</div></section>
{''.join(seksjoner)}
<p>Kilde: SSB, tabell 14700 og 14706. Sist oppdatert: 09.10.2026.</p>
</main></body></html>"""
    (ut / "02-grafikk-utkast.html").write_text(html, encoding="utf8")
    print("ok:", sorted(p.name for p in ut.iterdir()))


if __name__ == "__main__":
    bygg()

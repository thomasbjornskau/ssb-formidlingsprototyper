"""Lager konseptgrafikk og toppgrafikkvarianter for knr (steg 2).

Kjør fra mappen knr/:  python3 scripts/lag_grafikk.py
"""
import json
import os
import sys

HER = os.path.dirname(os.path.abspath(__file__))
ROT = os.path.dirname(HER)
sys.path.insert(0, os.path.join(ROT, "..", "felles"))
from grafikk import Svg, nb, sgn, bryt  # noqa: E402

MORK, GRA, LINJE = "#274246", "#5e787a", "#cdd3d4"
BG_FLATE, BG_KANT = "#eff8fa", "#c4dddb"
GR, GR_BG = "#00824d", "#ecfeed"
GRAA, GRAA_BG = "#b9c5c6", "#f3f5f5"
STOTTE, NULL = "#d9dfe0", "#a9b5b7"
F_GRONN, F_BLA, F_OKER, F_ROSA, F_MARINE = "#339b71", "#3face6", "#d5a640", "#cd83b0", "#5763a6"

D = json.load(open(os.path.join(ROT, "data", "grafikk-utkast.json"), encoding="utf-8"))
B = D["bnp2025"]
mrd = lambda v: nb(round(v / 1000))   # millioner → milliarder


def pil_ned(s, x, y, l=18):
    s.line(x, y, x, y + l - 7, stroke=GRA, sw=1.5)
    s.polygon([(x - 5, y + l - 8), (x + 5, y + l - 8), (x, y + l)], fill=GRA)


def pil_hoyre(s, x, y, l=14):
    s.line(x, y, x + l - 7, y, stroke=GRA, sw=1.5)
    s.polygon([(x + l - 8, y - 5), (x + l - 8, y + 5), (x + l, y)], fill=GRA)


def nummer(s, x, y, n):
    s.circle(x, y, 13, fill=MORK)
    s.text(x, y + 5, n, size=14, fill="#ffffff", weight=700, anchor="middle")


def stabel(s, x, y, w, deler, total_h=150, etikett_inne=True):
    """Liggende stabel som loddrett søyle: deler = [(navn, verdi, farge)], tegnes ovenfra og ned."""
    tot = sum(v for _, v, _ in deler)
    yy = y
    for navn, v, farge in deler:
        h = total_h * v / tot
        s.rect(x, yy, w * 0.28, h, fill=farge)
        s.text(x + w * 0.28 + 8, yy + h / 2 + 4, f"{navn}", size=12, fill=MORK)
        s.text(x + w, yy + h / 2 + 4, mrd(v), size=12, fill=MORK, anchor="end", weight=600)
        yy += h
    return yy


# ---------- Trinn ----------
def v_produksjon(s, x, y, w):
    yb = stabel(s, x, y, w, [("Fastlands-Norge", B["bruttoprodukt_fn"], F_GRONN), ("Olje og sjøfart", B["olje_sjofart"], F_MARINE),
                             ("Produktavgifter", B["produktavgifter"], GRAA)])
    s.line(x, yb + 6, x + w, yb + 6, stroke=MORK)
    s.text(x, yb + 24, "BNP 2025", size=13, weight=700, fill=GR)
    s.text(x + w, yb + 24, mrd(B["bnp"]), size=13, weight=700, fill=GR, anchor="end")
    return yb + 28


def v_anvendelse(s, x, y, w):
    rader = [("Privat konsum", B["konsum_hush"], ""), ("Offentlig konsum", B["konsum_off"], "+"), ("Investering", B["investering"], "+"),
             ("Eksport", B["eksport"], "+"), ("Import", B["import"], "−")]
    ry = y + 12
    for navn, v, tegn in rader:
        s.text(x, ry, tegn, size=13, fill=GRA, weight=600)
        s.text(x + 14, ry, navn, size=12.5, fill=MORK)
        s.text(x + w, ry, mrd(v), size=12.5, fill=MORK, anchor="end")
        ry += 22
    s.line(x, ry - 13, x + w, ry - 13, stroke=MORK)
    s.text(x + 14, ry + 6, "BNP 2025", size=13, weight=700, fill=GR)
    s.text(x + w, ry + 6, mrd(B["bnp"]), size=13, weight=700, fill=GR, anchor="end")
    return ry + 10


def v_fastland(s, x, y, w):
    rader = [("BNP", B["bnp"], MORK, 400), ("− olje, gass, rør og utenriks sjøfart", B["olje_sjofart"], F_MARINE, 400),
             ("= BNP Fastlands-Norge", B["fn"], GR, 700)]
    ry = y
    for navn, v, farge, vekt in rader:
        linjer = bryt(navn, 26)
        for i, l in enumerate(linjer):
            s.text(x, ry + 14 + i * 16, l, size=12.5, fill=farge if vekt == 700 else MORK, weight=vekt)
        s.text(x + w, ry + 14, mrd(v), size=13, fill=farge if vekt == 700 else MORK, anchor="end", weight=vekt)
        ry += 16 * len(linjer) + 14
    andel = 100 * B["olje_sjofart"] / B["bnp"]
    s.rect(x, ry, w, 18, fill=F_GRONN)
    s.rect(x + w * (1 - andel / 100), ry, w * andel / 100, 18, fill=F_MARINE)
    s.text(x, ry + 34, f"Olje og sjøfart: {nb(andel, 1)} prosent av BNP", size=12, fill=GRA)
    return ry + 38


def v_volum(s, x, y, w):
    nv = D["nominell_vs_volum_2026K2"]
    s.text(x, y + 12, "BNP, 2. kvartal 2026 mot året før", size=12, fill=GRA)
    maks = max(nv["lopende_yoy"], nv["volum_yoy"])
    for i, (navn, v, farge) in enumerate([("I kroner", nv["lopende_yoy"], GRAA), ("I volum", nv["volum_yoy"], GR)]):
        yy = y + 26 + i * 34
        s.text(x, yy + 15, navn, size=12.5, fill=MORK)
        bx = x + 64
        bw = (w - 64 - 52) * v / maks
        s.rect(bx, yy + 2, bw, 20, fill=farge)
        s.text(bx + bw + 6, yy + 17, f"{sgn(v, 1)} %", size=12.5, fill=MORK, weight=600)
    s.lines(x, y + 108, bryt("Volum holder prisene fra 2023 fast. Kvartal og måned sesongjusteres i tillegg.", int(w / 6.4)), size=12, lh=16, fill=MORK)
    return y + 140


def v_revisjon(s, x, y, w):
    trinn = [("Kvartal", "ca. 40 dager etter"), ("Endelig år", "21 mnd. etter"), ("Hovedrevisjon", "ca. hvert 5. år")]
    s.text(x, y + 12, "Når tallene kommer", size=12, fill=GRA)
    for i, (a, b) in enumerate(trinn):
        yy = y + 24 + i * 34
        s.rect(x, yy, w, 28, fill=BG_FLATE if i < 3 else GRAA_BG, stroke=BG_KANT if i < 3 else GRAA, dash=None if i < 3 else "4 3")
        s.text(x + 8, yy + 18, a, size=12.5, fill=MORK, weight=600)
        s.text(x + w - 8, yy + 18, b, size=12, fill=GRA, anchor="end")
    return y + 24 + 3 * 34


TRINN = [
    ("Verdiskaping", "Næringene skaper verdier. Bruttoproduktet er produksjon minus innsats av varer og tjenester.", v_produksjon),
    ("Samme BNP, brukt", "Det som lages, brukes til konsum, investering og eksport. Import trekkes fra.", v_anvendelse),
    ("Fastlands-Norge", "Olje, gass og utenriks sjøfart trekkes ut, fordi de svinger med priser og felt.", v_fastland),
    ("Kroner blir volum", "For å måle vekst holdes prisene faste. Ellers ville høye oljepriser se ut som mer produksjon.", v_volum),
    ("Tallene modnes", "De første tallene bygger på foreløpige kilder. De revideres når nye kilder kommer.", v_revisjon),
]
IKKE_MED = "Ikke et mål på velferd, fordeling eller formue. Ulønnet arbeid i hjemmet er ikke med."
KILDE_K = "Kilde: SSB, tabell 09189 (2025, løpende priser, milliarder kroner) og 09190. Sist oppdatert: 28.05.2026 og 27.08.2026."


def konsept_bred():
    s = Svg(1200, 560)
    s.text(40, 46, "Slik lages tallene", size=26, weight=700)
    s.text(40, 72, "Fra verdiskaping i næringene til BNP for Fastlands-Norge, med tall for 2025 i milliarder kroner", size=15, fill=GRA)
    s.line(40, 88, 1160, 88, stroke=LINJE)
    x0, w, gap = 40, 208, 20
    for i, (tittel, tekst, tegn) in enumerate(TRINN):
        x = x0 + i * (w + gap)
        nummer(s, x + 13, 118, str(i + 1))
        s.text(x + 34, 124, tittel, size=16, weight=700)
        s.lines(x, 154, bryt(tekst, 31), size=13, lh=18, fill=MORK)
        tegn(s, x, 236, w)
        if i < len(TRINN) - 1:
            pil_hoyre(s, x + w + 3, 118, 14)
    s.rect(40, 452, 1120, 52, fill=GRAA_BG, stroke=GRAA, dash="6 4")
    s.text(56, 476, "Det BNP ikke måler", size=14, weight=700)
    s.text(56, 494, IKKE_MED, size=13, fill=MORK)
    s.text(40, 540, KILDE_K, size=12, fill=GRA)
    s.save(os.path.join(ROT, "src", "konsept-bred.svg"))


def konsept_smal():
    B_ = 390
    s = Svg(B_, 10)
    s.text(16, 36, "Slik lages tallene", size=22, weight=700)
    s.lines(16, 60, bryt("Fra verdiskaping i næringene til BNP for Fastlands-Norge, med tall for 2025 i milliarder kroner", 44), size=14, lh=19, fill=GRA)
    y = 60 + 19 * 3 + 6
    s.line(16, y - 10, B_ - 16, y - 10, stroke=LINJE)
    y += 22
    w = B_ - 32 - 34
    for i, (tittel, tekst, tegn) in enumerate(TRINN):
        nummer(s, 29, y - 5, str(i + 1))
        s.text(50, y, tittel, size=16, weight=700)
        ty = s.lines(50, y + 26, bryt(tekst, 40), size=13, lh=18, fill=MORK)
        yb = tegn(s, 50, ty + 6, w)
        if i < len(TRINN) - 1:
            s.line(29, y + 12, 29, yb + 10, stroke=LINJE, sw=1.5)
        y = yb + 44
    linjer = bryt(IKKE_MED, 46)
    h = 40 + len(linjer) * 18
    s.rect(16, y - 14, B_ - 32, h, fill=GRAA_BG, stroke=GRAA, dash="6 4")
    s.text(28, y + 10, "Det BNP ikke måler", size=14, weight=700)
    s.lines(28, y + 32, linjer, size=13, lh=18)
    y = s.lines(16, y - 14 + h + 24, bryt(KILDE_K, 56), size=12, lh=16, fill=GRA)
    s.h = int(y + 6)
    s.save(os.path.join(ROT, "src", "konsept-smal.svg"))


# ---------- Toppgrafikk ----------
def topp_ramme(etikett, tall, setning, linjer, kilde):
    s = Svg(1200, 330)
    s.text(40, 46, etikett, size=13, fill=GRA, weight=600, ls="1.2")
    s.text(40, 118, tall, size=64, weight=700, fill=MORK)
    ys = s.lines(40, 162, bryt(setning, 40), size=22, lh=29, weight=600)
    s.lines(40, ys + 18, linjer, size=14.5, lh=21, fill=MORK)
    s.text(40, 312, kilde, size=12, fill=GRA)
    return s


def y_akse(s, x0, x1, ytop, ybot, lo, hi, steg, enhet, des=0):
    ys = lambda v: ybot - (v - lo) / (hi - lo) * (ybot - ytop)
    v = lo
    while v <= hi + 1e-9:
        s.line(x0, ys(v), x1, ys(v), stroke=NULL if abs(v) < 1e-9 else STOTTE)
        s.text(x0 - 6, ys(v) + 4, nb(v, des), size=12, fill=GRA, anchor="end")
        v += steg
    s.text(x0 - 46, ytop - 16, enhet, size=12, fill=GRA)
    return ys


KV = D["kvartal"]
SIST = KV[-1]
kvnavn = lambda k: f"{k[-1]}. kvartal {k[:4]}"


def topp_a():
    s = topp_ramme(
        f"NASJONALREGNSKAP · {kvnavn(SIST['k']).upper()}",
        f"{sgn(SIST['fn_qoq'], 1)} prosent",
        "vekst i fastlandsøkonomien fra kvartalet før.",
        bryt(f"Sesongjustert volumvekst i BNP Fastlands-Norge. SSB omtaler det som nær normal vekst. "
             f"Mot samme kvartal i fjor var veksten {nb(SIST['fn_yoy'], 1)} prosent.", 62),
        "Kilde: SSB, tabell 09190. Sist oppdatert: 27.08.2026.",
    )
    pts = KV[-12:]
    x0, x1, ytop, ybot = 640, 1160, 70, 270
    s.text(x0 - 46, 34, "BNP Fastlands-Norge, endring fra kvartalet før", size=14, weight=600)
    ys = y_akse(s, x0, x1, ytop, ybot, -0.5, 1.0, 0.5, "prosent", 1)
    slot = (x1 - x0) / len(pts)
    bw = slot * 0.66
    for i, p in enumerate(pts):
        x = x0 + i * slot + (slot - bw) / 2
        v = p["fn_qoq"]
        s.rect(x, min(ys(v), ys(0)), bw, abs(ys(v) - ys(0)), fill=GR if i == len(pts) - 1 else "#91cd9a")
        if p["k"].endswith("K1"):
            s.text(x + bw / 2, ybot + 18, p["k"][:4], size=12, fill=GRA, anchor="middle")
        if v == 0:
            s.line(x, ys(0), x + bw, ys(0), stroke="#91cd9a", sw=2)
        if i == len(pts) - 1 or v == max(q["fn_qoq"] for q in pts) or v < 0 or v == 0:
            s.text(x + bw / 2, (ys(v) - 6) if v >= 0 else ys(v) + 15, nb(v, 1).replace("-", "−"), size=12, fill=MORK, anchor="middle", weight=600)
    s.text(x0 - 46, 312, "Sesongjustert, faste priser.", size=12, fill=GRA)
    s.save(os.path.join(ROT, "docs", "grafikk", "02-topp-a.svg"))


def topp_b():
    s = topp_ramme(
        f"NASJONALREGNSKAP · {kvnavn(SIST['k']).upper()}",
        "Fire tall",
        "for veksten i samme kvartal.",
        bryt("BNP eller Fastlands-BNP, og endring fra kvartalet før eller fra samme kvartal i fjor. "
             "Alle fire er riktige. De svarer på ulike spørsmål.", 62),
        "Kilde: SSB, tabell 09190. Sist oppdatert: 27.08.2026.",
    )
    x0, ytop = 640, 70
    s.text(x0 - 46, 34, f"Volumvekst, {kvnavn(SIST['k'])}, prosent", size=14, weight=600)
    kol = [("Fra kvartalet før", "sesongjustert", "qoq"), ("Fra samme kvartal i fjor", "ujustert", "yoy")]
    rad = [("Fastlands-BNP", "fn", GR), ("BNP", "bnp", F_MARINE)]
    cw, rh = 200, 80
    for j, (t1, t2, _) in enumerate(kol):
        s.text(x0 + 110 + j * cw + cw / 2, ytop + 8, t1, size=13, weight=600, anchor="middle")
        s.text(x0 + 110 + j * cw + cw / 2, ytop + 26, t2, size=12, fill=GRA, anchor="middle")
    for i, (navn, k, farge) in enumerate(rad):
        yy = ytop + 44 + i * rh
        s.text(x0 + 100, yy + rh / 2 + 4, navn, size=14, weight=600, anchor="end")
        for j, (_, _, kk) in enumerate(kol):
            v = SIST[f"{k}_{kk}"]
            cx = x0 + 110 + j * cw
            s.rect(cx + 8, yy + 6, cw - 16, rh - 12, fill=GR_BG if k == "fn" else "#f1f1fe", stroke=farge if (k == "fn" and kk == "qoq") else LINJE, sw=2 if (k == "fn" and kk == "qoq") else 1)
            s.text(cx + cw / 2, yy + rh / 2 + 12, f"{sgn(v, 1)}", size=34, weight=700, fill=farge, anchor="middle")
    s.text(x0 - 46, 312, "Den uthevede ruten er tallet SSB løfter fram i overskriften.", size=12, fill=GRA)
    s.save(os.path.join(ROT, "docs", "grafikk", "02-topp-b.svg"))


def topp_c():
    ol = D["oljeandel"]
    sist = ol[-1]
    topp = max(ol, key=lambda d: d["pst"])
    s = topp_ramme(
        f"NASJONALREGNSKAP · {sist['aar']}",
        "En femdel",
        "av BNP kom fra olje, gass og utenriks sjøfart.",
        bryt(f"Andelen var {nb(sist['pst'], 1)} prosent i {sist['aar']} og {nb(topp['pst'], 1)} prosent i {topp['aar']}. "
             f"Den svinger med olje- og gassprisene. Derfor er Fastlands-BNP hovedtallet.", 62),
        "Kilde: SSB, tabell 09189. Sist oppdatert: 28.05.2026. Egen beregning av andelen.",
    )
    x0, x1, ytop, ybot = 640, 1130, 70, 270
    s.text(x0 - 46, 34, "Oljevirksomhet og utenriks sjøfart, andel av BNP i løpende priser", size=14, weight=600)
    ys = y_akse(s, x0, x1, ytop, ybot, 0, 40, 10, "prosent")
    a0, a1 = ol[0]["aar"], ol[-1]["aar"]
    xs = lambda a: x0 + (a - a0) / (a1 - a0) * (x1 - x0)
    pts = [(xs(d["aar"]), ys(d["pst"])) for d in ol]
    s.polygon([(xs(a0), ys(0))] + pts + [(xs(a1), ys(0))], fill="#d4d8ec")
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        s.line(xa, ya, xb, yb, stroke=F_MARINE, sw=2)
    for a in range(1970, a1 + 1, 10):
        s.text(xs(a), ybot + 18, str(a), size=12, fill=GRA, anchor="middle")
    s.text(xs(a1), ybot + 18, str(a1), size=12, fill=GRA, anchor="middle")
    for d in (topp, sist):
        s.circle(xs(d["aar"]), ys(d["pst"]), 4, fill=F_MARINE)
        s.text(xs(d["aar"]) + (6 if d is sist else -8), ys(d["pst"]) - 8, f"{nb(d['pst'], 1)}", size=12, weight=600, fill=MORK, anchor="start" if d is sist else "end")
    s.save(os.path.join(ROT, "docs", "grafikk", "02-topp-c.svg"))


def topp_d():
    aar = D["aarsvekst"]
    sist = aar[-1]
    snitt10 = sum(d["fn"] for d in aar if d["aar"] > sist["aar"] - 10) / 10
    neg = [d["aar"] for d in aar if d["fn"] < 0]
    s = topp_ramme(
        f"NASJONALREGNSKAP \u00b7 {sist['aar']}",
        f"{nb(sist['fn'], 1)} prosent",
        "vekst i fastlandsøkonomien i fjor.",
        bryt(f"Snittet de siste ti årene var {nb(snitt10, 1)} prosent. Siden {aar[0]['aar']} har fastlandsøkonomien bare krympet i "
             f"{['null', 'ett', 'to', 'tre', 'fire', 'fem', 'seks'][len(neg)]} år: {', '.join(map(str, neg[:-1]))} og {neg[-1]}.", 62),
        "Kilde: SSB, tabell 09189. Sist oppdatert: 28.05.2026.",
    )
    x0, x1, ytop, ybot = 640, 1160, 70, 262
    s.text(x0 - 46, 34, f"Volumvekst per år, {aar[0]['aar']}–{sist['aar']}", size=14, weight=600)
    ys = y_akse(s, x0, x1, ytop, ybot, -4, 8, 2, "prosent")
    slot = (x1 - x0) / len(aar)
    bw = slot * 0.72
    forelopig = [d for d in aar if d["aar"] > 2023]
    for i, d in enumerate(aar):
        x = x0 + i * slot + (slot - bw) / 2
        v = d["fn"]
        farge = GR if d["aar"] <= 2023 else "#91cd9a"
        s.rect(x, min(ys(v), ys(0)), bw, abs(ys(v) - ys(0)), fill=farge)
        s.line(x - 0.5, ys(d["bnp"]), x + bw + 0.5, ys(d["bnp"]), stroke=MORK, sw=1.6)
        if d["aar"] % 10 == 0 or d["aar"] == sist["aar"]:
            s.text(x + bw / 2, ybot + 16, str(d["aar"]), size=12, fill=GRA, anchor="middle")
    xl = x0 + (len(aar) - 1) * slot + slot / 2
    s.text(xl, ys(sist["fn"]) - 18, nb(sist["fn"], 1), size=12, fill=MORK, anchor="middle", weight=700)
    # tegnforklaring over figuren, til høyre
    lx = x1 - 300
    s.rect(lx, 50, 12, 12, fill=GR); s.text(lx + 18, 60, "Fastlands-BNP", size=12, fill=MORK)
    s.line(lx + 112, 56, lx + 126, 56, stroke=MORK, sw=2); s.text(lx + 132, 60, "BNP", size=12, fill=MORK)
    s.rect(lx + 172, 50, 12, 12, fill="#91cd9a"); s.text(lx + 190, 60, "foreløpig", size=12, fill=MORK)
    s.text(x0 - 46, 312, "Tall etter 2023 er foreløpige.", size=12, fill=GRA)
    s.save(os.path.join(ROT, "docs", "grafikk", "02-topp-d.svg"))


if __name__ == "__main__":
    konsept_bred()
    konsept_smal()
    topp_a()
    topp_b()
    topp_c()
    topp_d()

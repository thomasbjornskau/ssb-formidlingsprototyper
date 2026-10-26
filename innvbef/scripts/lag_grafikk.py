"""Lager konseptgrafikk og toppgrafikkvarianter for innvbef (steg 2).

Bruker Svg, nb, sgn og bryt fra felles/grafikk.py. Mangler repoet, brukes
en lokal reserve med samme grensesnitt (se nederst i try/except).

Kjør fra mappen innvbef/:  python3 scripts/lag_grafikk.py
"""
import json
import os
import sys

HER = os.path.dirname(os.path.abspath(__file__))
ROT = os.path.dirname(HER)
sys.path.insert(0, os.path.join(ROT, "..", "felles"))

try:
    from grafikk import Svg, nb, sgn, bryt  # felles/grafikk.py i repoet
except ImportError:  # reserve til repoet er på plass
    from xml.sax.saxutils import escape

    def nb(x, des=0):
        s = f"{abs(x):,.{des}f}".replace(",", " ").replace(".", ",")
        return ("−" if x < 0 else "") + s

    def sgn(x, des=0):
        return ("+" if x > 0 else "") + nb(x, des)

    def bryt(tekst, n):
        ord_, linjer, l = tekst.split(), [], ""
        for o in ord_:
            if l and len(l) + 1 + len(o) > n:
                linjer.append(l)
                l = o
            else:
                l = (l + " " + o).strip()
        if l:
            linjer.append(l)
        return linjer

    class Svg:
        def __init__(self, b, h):
            self.b, self.h, self.e = b, h, []

        def rect(self, x, y, w, h, fill="none", stroke="none", sw=1, dash=None, rx=0):
            d = f' stroke-dasharray="{dash}"' if dash else ""
            self.e.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

        def line(self, x1, y1, x2, y2, stroke="#cdd3d4", sw=1, dash=None):
            d = f' stroke-dasharray="{dash}"' if dash else ""
            self.e.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

        def circle(self, x, y, r, fill="#274246", stroke="none", sw=1):
            self.e.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

        def polygon(self, pts, fill="#274246"):
            p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
            self.e.append(f'<polygon points="{p}" fill="{fill}"/>')

        def text(self, x, y, t, size=14, fill="#274246", weight=400, anchor="start", ls=None):
            l = f' letter-spacing="{ls}"' if ls else ""
            self.e.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Open Sans, Segoe UI, Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{l} style="font-variant-numeric:tabular-nums">{escape(str(t))}</text>')

        def lines(self, x, y, linjer, size=14, lh=None, **kw):
            lh = lh or round(size * 1.4)
            for i, l in enumerate(linjer):
                self.text(x, y + i * lh, l, size=size, **kw)
            return y + len(linjer) * lh

        def save(self, sti):
            with open(sti, "w", encoding="utf-8") as f:
                f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.b}" height="{self.h}" viewBox="0 0 {self.b} {self.h}">\n')
                f.write(f'<rect x="0" y="0" width="{self.b}" height="{self.h}" fill="#ffffff"/>\n')
                f.write("\n".join(self.e))
                f.write("\n</svg>\n")

# Palett (ssb-konseptfigurer og ssb-diagramstandard)
MORK, GRA, LINJE = "#274246", "#5e787a", "#cdd3d4"
BG_FLATE, BG_KANT = "#eff8fa", "#c4dddb"
GR, GR_LYS, GR_BG = "#00824d", "#b6e9b8", "#ecfeed"
LI, LI_LYS, LI_BG, LI_TXT = "#7d5fea", "#c3baff", "#f1f1fe", "#4b2fb0"
GRAA, GRAA_BG = "#b9c5c6", "#f3f5f5"
STOTTE, NULL = "#d9dfe0", "#a9b5b7"
F_GRONN, F_BLA, F_OKER = "#339b71", "#3face6", "#d5a640"

D = json.load(open(os.path.join(ROT, "data", "grafikk-utkast.json"), encoding="utf-8"))
SER ={r["aar"]: r for r in D["serie"]}
KAT = D["kategorier_2026"]
BEF = D["bef_2026"]
R = D["regnskap_innvandrere_2025"]
LAND = D["land_2026"]
SUM_BG = D["sum_innv_nmi_2026"]


def pst(x, des=1):
    return nb(100 * x / BEF, des)


# Andeler, regnet fra 05182 (sum lik folkemengden)
ANDEL = {
    "innv": KAT["innvandrere"] / BEF * 100,
    "utl": (KAT["innvandrere"] + KAT["utenlandsfodte_en_norskfodt"] + KAT["utenlandsfodte_to_norskfodte"]) / BEF * 100,
    "innv_nmi": (KAT["innvandrere"] + KAT["norskfodte_innvforeldre"]) / BEF * 100,
    "alle": (BEF - KAT["norskfodte_to_norskfodte"]) / BEF * 100,
}
ANDRE = R["folketilvekst"] - (R["innflyttinger"] - R["utflyttinger"] - R["dode"])


def pil_ned(s, x, y, l=18):
    s.line(x, y, x, y + l - 7, stroke=GRA, sw=1.5)
    s.polygon([(x - 5, y + l - 8), (x + 5, y + l - 8), (x, y + l)], fill=GRA)


def pil_hoyre(s, x, y, l=14):
    s.line(x, y, x + l - 7, y, stroke=GRA, sw=1.5)
    s.polygon([(x + l - 8, y - 5), (x + l - 8, y + 5), (x + l, y)], fill=GRA)


def chip(s, x, y, w, t, fill, kant, tfarge=MORK, h=24, size=12.5, dash=None):
    s.rect(x, y, w, h, fill=fill, stroke=kant, dash=dash)
    s.text(x + 8, y + h / 2 + 4.5, t, size=size, fill=tfarge)


def nummer(s, x, y, n):
    s.circle(x, y, 13, fill=MORK)
    s.text(x, y + 5, n, size=14, fill="#ffffff", weight=700, anchor="middle")


# ---------- Konseptgrafikk ----------

def v_bosatt(s, x, y, w):
    s.rect(x, y, w, 34, fill=BG_FLATE, stroke=BG_KANT)
    s.text(x + w / 2, y + 22, "Folkeregisteret", size=13, anchor="middle", weight=600)
    pil_ned(s, x + w / 2, y + 36, 20)
    s.rect(x, y + 60, w, 40, fill=GR_BG, stroke=GR)
    s.text(x + 8, y + 76, "Bosatt: lovlig opphold,", size=12.5, fill=GR, weight=600)
    s.text(x + 8, y + 92, "skal bo her minst 6 mnd", size=12.5, fill=GR, weight=600)
    s.rect(x, y + 110, w, 40, fill=GRAA_BG, stroke=GRAA, dash="4 3")
    s.text(x + 8, y + 126, "Ikke med: asylsøkere og", size=12.5, fill=MORK)
    s.text(x + 8, y + 142, "korte opphold", size=12.5, fill=MORK)
    return y + 150


def tre(s, cx, y, person_ute, tittel_linjer):
    """Familietre: fire besteforeldre, to foreldre, personen. Fylt = født i utlandet."""
    r = 7
    bx = [cx - 33, cx - 13, cx + 13, cx + 33]
    fx = [cx - 23, cx + 23]
    for x in bx:
        s.line(x, y + r, (fx[0] if x < cx else fx[1]), y + 32 - r, stroke=LINJE, sw=1)
    for x in fx:
        s.line(x, y + 32 + r, cx, y + 64 - r, stroke=LINJE, sw=1)
    for x in bx:
        s.circle(x, y, r, fill=LI, stroke=LI)
    for x in fx:
        s.circle(x, y + 32, r, fill=LI, stroke=LI)
    s.circle(cx, y + 64, r + 2, fill=LI if person_ute else "#ffffff", stroke=LI, sw=2)
    for i, t in enumerate(tittel_linjer):
        s.text(cx, y + 92 + i * 16, t, size=12.5, fill=LI_TXT, weight=600, anchor="middle")


def v_fodested(s, x, y, w):
    tre(s, x + w * 0.25, y + 8, True, ["Innvandrer"])
    tre(s, x + w * 0.75, y + 8, False, ["Norskfødt med", "innvandrer-", "foreldre"])
    s.circle(x + 6, y + 160, 6, fill=LI, stroke=LI)
    s.text(x + 18, y + 164, "født i utlandet", size=12, fill=GRA)
    s.circle(x + 6, y + 180, 6, fill="#ffffff", stroke=LI, sw=2)
    s.text(x + 18, y + 184, "født i Norge", size=12, fill=GRA)
    return y + 186


def v_kategorier(s, x, y, w):
    rader = [
        ("Innvandrere", KAT["innvandrere"], True),
        ("Norskfødte m. innvandrerforeldre", KAT["norskfodte_innvforeldre"], True),
        ("Tre andre kategorier", KAT["utenlandsfodte_en_norskfodt"] + KAT["norskfodte_en_utenlandsfodt"] + KAT["utenlandsfodte_to_norskfodte"], False),
        ("Født i Norge av norskfødte", KAT["norskfodte_to_norskfodte"], False),
    ]
    maks = 75.0
    ry = y
    for navn, v, med in rader:
        p = v / BEF * 100
        s.text(x, ry + 12, navn, size=12, fill=MORK if med else GRA, weight=600 if med else 400)
        bw = (w - 44) * p / maks
        s.rect(x, ry + 18, max(bw, 1.5), 13, fill=GR if med else GRAA)
        s.text(x + max(bw, 1.5) + 5, ry + 29, nb(p, 1), size=12, fill=MORK)
        ry += 40
    s.text(x, ry + 6, "Prosent av befolkningen 1.1.2026.", size=12, fill=GRA)
    s.text(x, ry + 22, "Grønt er med i statistikken.", size=12, fill=GRA)
    return ry + 22


def v_landbakgrunn(s, x, y, w):
    eks = [
        ("Født i Polen", "Polen"),
        ("Født i Norge, foreldre", "fra Pakistan → Pakistan"),
        ("Foreldre fra to land", "→ morens fødeland"),
    ]
    yy = y
    for l1, l2 in eks:
        s.rect(x, yy, w, 40, fill=LI_BG, stroke=LI_LYS)
        s.text(x + 8, yy + 16, l1 if "→" in l2 else l1 + " → " + l2, size=12.5, fill=LI_TXT)
        if "→" in l2:
            s.text(x + 8, yy + 32, l2, size=12.5, fill=LI_TXT)
        yy += 48
    s.lines(x, yy + 8, bryt("Eksempler. Landbakgrunn er fødeland, ikke statsborgerskap.", int(w / 6.4)), size=12, lh=16, fill=GRA)
    return yy + 40


def v_regnskap(s, x, y, w):
    rader = [
        ("", "Innvandrere 1.1.2025", R["bosatt_start"]),
        ("+", "flyttet til Norge", R["innflyttinger"]),
        ("−", "flyttet fra Norge", R["utflyttinger"]),
        ("−", "døde", R["dode"]),
        ("+", "andre endringer", ANDRE),
    ]
    ry = y + 12
    for tegn, navn, v in rader:
        s.text(x, ry, tegn, size=13, fill=GRA, weight=600)
        s.text(x + 14, ry, navn, size=13, fill=MORK)
        s.text(x + w, ry, nb(v), size=13, fill=MORK, anchor="end")
        ry += 21
    s.line(x, ry - 13, x + w, ry - 13, stroke=MORK, sw=1)
    s.rect(x - 4, ry - 9, w + 8, 26, fill=GR_BG, stroke=GR)
    s.text(x + 14, ry + 8, "= 1.1.2026", size=13, fill=GR, weight=700)
    s.text(x + w, ry + 8, nb(R["bosatt_slutt"]), size=13, fill=GR, weight=700, anchor="end")
    s.lines(x, ry + 40, bryt("Barn født i Norge blir norskfødte, ikke innvandrere.", int(w / 6.4)), size=12, lh=16, fill=GRA)
    return ry + 56


TRINN = [
    ("Bosatt", "Bare de som er registrert bosatt i Folkeregisteret, telles.", v_bosatt),
    ("Hvor er du født?", "Fødeland for deg, foreldrene og besteforeldrene avgjør kategorien.", v_fodested),
    ("Seks kategorier", "Hele befolkningen deles i seks. To av dem er med i denne statistikken.", v_kategorier),
    ("Landbakgrunn", "Eget fødeland for innvandrere, foreldrenes for norskfødte.", v_landbakgrunn),
    ("Telles 1. januar", "Tallet er en beholdning. Endringen fra året før er et regnskap.", v_regnskap),
]

IKKE_MED = "Ikke med: asylsøkere, opphold under seks måneder og personer uten lovlig opphold."
OVERDEKNING = ("Med, men bor ikke her: innvandrere som har flyttet ut uten å melde fra. "
               "SSB anslo dem til 2,3 prosent av innvandrerne.")
KILDE_K = ("Kilde: SSB, tabell 05182 (sist oppdatert 05.03.2026) og 10516 (17.04.2026). "
           "Overdekning: SSB Notater 2024/3.")


def konsept_bred():
    B, H = 1200, 600
    s = Svg(B, H)
    s.text(40, 46, "Slik lages tallene", size=26, weight=700)
    s.text(40, 72, "Fra en person i folkeregisteret til en kategori og en landbakgrunn", size=15, fill=GRA)
    s.line(40, 88, 1160, 88, stroke=LINJE)
    x0, w, gap = 40, 208, 20
    for i, (tittel, tekst, tegn) in enumerate(TRINN):
        x = x0 + i * (w + gap)
        nummer(s, x + 13, 118, str(i + 1))
        s.text(x + 34, 124, tittel, size=16, weight=700)
        s.lines(x, 154, bryt(tekst, 31), size=13, lh=18, fill=MORK)
        tegn(s, x, 220, w)
        if i < len(TRINN) - 1:
            s_x = x + w + 3
            pil_hoyre(s, s_x, 118, 14)
    s.rect(40, 464, 1120, 90, fill=GRAA_BG, stroke=GRAA, dash="6 4")
    s.text(56, 488, "Det tallene ikke fanger", size=14, weight=700, fill=MORK)
    s.lines(56, 512, bryt(IKKE_MED, 70), size=13, lh=18, fill=MORK)
    s.lines(620, 512, bryt(OVERDEKNING, 70), size=13, lh=18, fill=MORK)
    s.text(40, 580, KILDE_K, size=12, fill=GRA)
    s.save(os.path.join(ROT, "src", "konsept-bred.svg"))


def konsept_smal():
    B = 390
    s = Svg(B, 10)
    s.text(16, 36, "Slik lages tallene", size=22, weight=700)
    s.lines(16, 60, bryt("Fra en person i folkeregisteret til en kategori og en landbakgrunn", 44), size=14, lh=19, fill=GRA)
    s.line(16, 104, B - 16, 104, stroke=LINJE)
    y = 136
    w = B - 32 - 34
    for i, (tittel, tekst, tegn) in enumerate(TRINN):
        nummer(s, 29, y - 5, str(i + 1))
        s.text(50, y, tittel, size=16, weight=700)
        ty = s.lines(50, y + 26, bryt(tekst, 40), size=13, lh=18, fill=MORK)
        yb = tegn(s, 50, ty + 6, w)
        if i < len(TRINN) - 1:
            s.line(29, y + 12, 29, yb + 10, stroke=LINJE, sw=1.5)
        y = yb + 44
    linjer1 = bryt(IKKE_MED, 46)
    linjer2 = bryt(OVERDEKNING, 46)
    hboks = 40 + (len(linjer1) + len(linjer2)) * 18 + 14
    s.rect(16, y - 14, B - 32, hboks, fill=GRAA_BG, stroke=GRAA, dash="6 4")
    s.text(28, y + 10, "Det tallene ikke fanger", size=14, weight=700)
    y2 = s.lines(28, y + 34, linjer1, size=13, lh=18)
    s.lines(28, y2 + 10, linjer2, size=13, lh=18)
    y = y - 14 + hboks + 26
    y = s.lines(16, y, bryt(KILDE_K, 56), size=12, lh=16, fill=GRA)
    s.h = int(y + 6)
    s.save(os.path.join(ROT, "src", "konsept-smal.svg"))


# ---------- Toppgrafikk: felles mal 1200 × 330 ----------

def topp_ramme(etikett, tall, setning, linjer, kilde):
    s = Svg(1200, 330)
    s.text(40, 46, etikett, size=13, fill=GRA, weight=600, ls="1.2")
    s.text(40, 118, tall, size=64, weight=700, fill=MORK)
    ys_ = s.lines(40, 162, bryt(setning, 40), size=22, lh=29, weight=600)
    s.lines(40, ys_ + 18, linjer, size=14.5, lh=21, fill=MORK)
    s.text(40, 312, kilde, size=12, fill=GRA)
    return s


def topp_a():
    s = topp_ramme(
        "INNVANDRERE · 1. JANUAR 2026",
        "17,5 prosent",
        "av befolkningen er innvandrere. Eller flere, alt etter hvem du teller.",
        bryt(f"{nb(KAT['innvandrere'])} er født i utlandet av to utenlandsfødte foreldre. "
             "Tallet blir større jo videre grensen trekkes.", 62),
        "Kilde: SSB, tabell 05182. Sist oppdatert: 05.03.2026.",
    )
    trapp = [
        ("Innvandrere", ANDEL["innv"], "født i utlandet, to utenlandsfødte foreldre", True),
        ("+ andre født i utlandet", ANDEL["utl"], "alle utenlandsfødte, også adopterte", False),
        ("Innvandrere og norskfødte", ANDEL["innv_nmi"], "med innvandrerforeldre", False),
        ("Alle utenom norskfødte med norskfødte foreldre", ANDEL["alle"], "selv eller minst én forelder født i utlandet", False),
    ]
    x0, x1 = 640, 1040
    s.text(x0, 34, "Andel av befolkningen med ulike definisjoner", size=14, weight=600)
    s.text(x0, 54, "prosent", size=12, fill=GRA)
    maks = 30.0
    for v in (0, 10, 20, 30):
        xv = x0 + (x1 - x0) * v / maks
        s.line(xv, 62, xv, 286, stroke=NULL if v == 0 else STOTTE)
        s.text(xv, 300, nb(v), size=12, fill=GRA, anchor="middle")
    y = 66
    for navn, p, forkl, hoved in trapp:
        bw = (x1 - x0) * p / maks
        s.text(x0 + 6, y + 14, navn, size=13, weight=700 if hoved else 600, fill=MORK)
        s.text(x0 + 6, y + 30, forkl, size=12, fill=GRA)
        s.rect(x0, y + 36, bw, 14, fill=GR if hoved else GRAA)
        s.text(x0 + bw + 6, y + 48, nb(p, 1), size=13, weight=700, fill=MORK)
        y += 56
    s.save(os.path.join(ROT, "docs", "grafikk", "02-topp-a.svg"))


def topp_b():
    v26 = SER[2026]["innvandrere"] - SER[2025]["innvandrere"]
    s = topp_ramme(
        "INNVANDRERE · 1970–2026",
        "987 000",
        "innvandrere bor i Norge. Økningen i 2025 var den laveste siden 2021.",
        bryt(f"Antallet har økt med {nb(v26)} siden 1. januar 2025, og er mer enn firedoblet siden 2000. "
             f"I tillegg er {nb(SER[2026]['norskfodte'])} norskfødte med innvandrerforeldre.", 62),
        "Kilde: SSB, tabell 05182. Sist oppdatert: 05.03.2026.",
    )
    x0, x1, ytop, ybot = 660, 1080, 70, 270
    s.text(x0 - 46, 34, "Bosatte 1. januar, 1970–2026", size=14, weight=600)
    maks, steg = 1000000, 250000

    def ys(v):
        return ybot - v / maks * (ybot - ytop)

    def xs(a):
        return x0 + (a - 1970) / (2026 - 1970) * (x1 - x0)

    for v in range(0, maks + 1, steg):
        s.line(x0, ys(v), x1, ys(v), stroke=NULL if v == 0 else STOTTE)
        s.text(x0 - 6, ys(v) + 4, nb(v), size=12, fill=GRA, anchor="end")
    s.text(x0 - 52, ytop - 16, "personer", size=12, fill=GRA)
    for a in (1970, 1980, 1990, 2000, 2010, 2026):
        s.text(xs(a), ybot + 18, str(a), size=12, fill=GRA, anchor="middle")
    for felt, farge in (("innvandrere", GR), ("norskfodte", "#1d9de2")):
        pts = [(xs(a), ys(SER[a][felt])) for a in sorted(SER)]
        # 1970–1986: bare tre målepunkter, tegnes prikket
        s.e.append('<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts[:3]) +
                   f'" fill="none" stroke="{farge}" stroke-width="2" stroke-dasharray="2 4"/>')
        s.e.append('<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts[2:]) +
                   f'" fill="none" stroke="{farge}" stroke-width="2.5"/>')
        for x, y in pts[:3]:
            s.circle(x, y, 2.5, fill=farge)
    s.text(x1 + 8, ys(SER[2026]["innvandrere"]) + 4, "Innvandrere", size=12.5, weight=600)
    s.text(x1 + 8, ys(SER[2026]["norskfodte"]) - 4, "Norskfødte med", size=12.5, weight=600)
    s.text(x1 + 8, ys(SER[2026]["norskfodte"]) + 12, "innvandrerforeldre", size=12.5, weight=600)
    s.text(x0 - 52, 312, "Prikket: bare tall for 1970, 1980 og 1986. Årlige tall fra 1986.", size=12, fill=GRA)
    s.save(os.path.join(ROT, "docs", "grafikk", "02-topp-b.svg"))


def topp_c():
    top = sorted(LAND, key=lambda r: -(r["innvandrere"] + r["norskfodte"]))
    andel10 = sum(r["innvandrere"] + r["norskfodte"] for r in top) / SUM_BG * 100
    pak = next(r for r in top if r["land"] == "Pakistan")
    ukr = next(r for r in top if r["land"] == "Ukraina")
    p_pak = pak["norskfodte"] / (pak["innvandrere"] + pak["norskfodte"]) * 100
    p_ukr = ukr["norskfodte"] / (ukr["innvandrere"] + ukr["norskfodte"]) * 100
    s = topp_ramme(
        "LANDBAKGRUNN · 1. JANUAR 2026",
        "Ti land",
        "står for nesten halvparten. Polen er størst.",
        bryt(f"{nb(andel10)} prosent av innvandrerne og de norskfødte har bakgrunn fra disse ti landene. "
             f"Blant dem med pakistansk bakgrunn er {nb(p_pak)} prosent født i Norge, "
             f"blant dem med ukrainsk {nb(p_ukr)} prosent.", 62),
        "Kilde: SSB, tabell 13880. Sist oppdatert: 05.03.2026.",
    )
    x0, x1 = 690, 1080
    maks = 140000
    s.text(600, 34, "De ti største landbakgrunnene, personer", size=14, weight=600)
    # tegnforklaring over diagrammet
    s.rect(600, 46, 12, 12, fill=F_GRONN)
    s.text(618, 57, "innvandrere", size=12, fill=MORK)
    s.rect(710, 46, 12, 12, fill=F_BLA)
    s.text(728, 57, "norskfødte med innvandrerforeldre", size=12, fill=MORK)
    y, rad = 70, 23
    for v in (0, 50000, 100000):
        xv = x0 + (x1 - x0) * v / maks
        s.line(xv, y - 4, xv, y + rad * 10, stroke=NULL if v == 0 else STOTTE)
        s.text(xv, y + rad * 10 + 14, nb(v), size=12, fill=GRA, anchor="middle")
    for r in top:
        i, n = r["innvandrere"], r["norskfodte"]
        wi = (x1 - x0) * i / maks
        wn = (x1 - x0) * n / maks
        s.text(x0 - 8, y + 14, r["land"], size=12.5, fill=MORK, anchor="end")
        s.rect(x0, y + 3, wi, rad - 8, fill=F_GRONN)
        s.rect(x0 + wi, y + 3, wn, rad - 8, fill=F_BLA)
        s.text(x0 + wi + wn + 5, y + 15, nb(i + n), size=12, fill=MORK)
        y += rad
    s.save(os.path.join(ROT, "docs", "grafikk", "02-topp-c.svg"))


if __name__ == "__main__":
    konsept_bred()
    konsept_smal()
    topp_a()
    topp_b()
    topp_c()
    print("andeler", {k: round(v, 2) for k, v in ANDEL.items()}, "andre endringer", ANDRE)

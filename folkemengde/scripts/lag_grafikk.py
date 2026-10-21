"""Lager konseptgrafikk og toppgrafikkvarianter for folkemengde (steg 2).

Bruker Svg, nb, sgn og bryt fra felles/grafikk.py. Mangler repoet, brukes
en lokal reserve med samme grensesnitt (se nederst i try/except).

Kjør fra mappen folkemengde/:  python3 scripts/lag_grafikk.py
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
AAR = {a["aar"]: a for a in D["aar"]}
A25 = AAR[2025]


def pil_ned(s, x, y, l=18):
    s.line(x, y, x, y + l - 7, stroke=GRA, sw=1.5)
    s.polygon([(x - 5, y + l - 8), (x + 5, y + l - 8), (x, y + l)], fill=GRA)


def pil_hoyre(s, x, y, l=14):
    s.line(x, y, x + l - 7, y, stroke=GRA, sw=1.5)
    s.polygon([(x + l - 8, y - 5), (x + l - 8, y + 5), (x + l, y)], fill=GRA)


def chip(s, x, y, w, t, fill, kant, tfarge=MORK, h=24, size=12.5):
    s.rect(x, y, w, h, fill=fill, stroke=kant)
    s.text(x + 8, y + h / 2 + 4.5, t, size=size, fill=tfarge)


# ---------- Konseptgrafikk: ett trinn = (tittel, tekst, tegnefunksjon) ----------

def v_hendelser(s, x, y, w):
    for i, t in enumerate(["Fødsel", "Dødsfall", "Flytter til Norge", "Flytter fra Norge", "Flytter til ny kommune"]):
        chip(s, x, y + i * 29, w, t, LI_BG, LI_LYS, LI_TXT)
    return y + 5 * 29 - 5


def v_bosatt(s, x, y, w):
    # tidslinje 0–12 måneder med terskel ved 6
    s.text(x, y + 12, "Planlagt opphold", size=12, fill=GRA)
    ly = y + 38
    s.rect(x, ly - 7, w / 2, 14, fill=GRAA_BG, stroke=GRAA, dash="4 3")
    s.rect(x + w / 2, ly - 7, w / 2, 14, fill=GR_BG, stroke=GR)
    s.line(x + w / 2, ly - 14, x + w / 2, ly + 14, stroke=MORK, sw=1.5)
    s.text(x, ly + 28, "0", size=12, fill=GRA)
    s.text(x + w / 2, ly + 28, "6 mnd", size=12, fill=MORK, anchor="middle", weight=600)
    s.text(x + w, ly + 28, "12", size=12, fill=GRA, anchor="end")
    s.text(x + w / 4, ly + 52, "ikke bosatt", size=12.5, fill=GRA, anchor="middle")
    s.text(x + 3 * w / 4, ly + 52, "bosatt", size=12.5, fill=GR, weight=600, anchor="middle")
    return ly + 56


def v_ssb(s, x, y, w):
    s.rect(x, y, w, 34, fill=BG_FLATE, stroke=BG_KANT)
    s.text(x + w / 2, y + 22, "Folkeregisteret", size=13, anchor="middle", weight=600)
    pil_ned(s, x + w / 2, y + 36, 20)
    s.rect(x, y + 58, w, 34, fill=BG_FLATE, stroke=BG_KANT)
    s.text(x + w / 2, y + 80, "SSB kontrollerer og teller", size=13, anchor="middle", weight=600)
    pil_ned(s, x + w / 2, y + 94, 20)
    s.rect(x, y + 116, w, 34, fill=GR_BG, stroke=GR)
    s.text(x + w / 2, y + 138, "Bosatte per tidspunkt", size=13, anchor="middle", weight=600, fill=GR)
    return y + 150


def v_regnskap(s, x, y, w):
    rader = [
        ("", "Bosatt 1.1.2025", A25["bef_start"]),
        ("+", "fødte", A25["fodte"]),
        ("−", "døde", A25["dode"]),
        ("+", "innvandringer", A25["innvandring"]),
        ("−", "utvandringer", A25["utvandring"]),
        ("+", "korreksjon", A25["korreksjon"]),
    ]
    ry = y + 12
    for tegn, navn, v in rader:
        s.text(x, ry, tegn, size=13, fill=GRA, weight=600)
        s.text(x + 14, ry, navn, size=13, fill=MORK)
        s.text(x + w, ry, nb(v), size=13, fill=MORK, anchor="end")
        ry += 21
    s.line(x, ry - 13, x + w, ry - 13, stroke=MORK, sw=1)
    s.rect(x - 4, ry - 9, w + 8, 26, fill=GR_BG, stroke=GR)
    s.text(x + 14, ry + 8, "Bosatt 1.1.2026", size=13, fill=GR, weight=700)
    s.text(x + w, ry + 8, nb(D["bef_2026"]), size=13, fill=GR, weight=700, anchor="end")
    return ry + 17


def v_publisering(s, x, y, w):
    chip(s, x, y, w, "Kvartal: ca. seks uker etter", BG_FLATE, BG_KANT)
    chip(s, x, y + 30, w, "Hele året: februar eller mars", BG_FLATE, BG_KANT)
    s.rect(x, y + 66, w, 76, fill=GRAA_BG, stroke=GRAA, dash="5 4")
    s.lines(x + 8, y + 84, bryt("Registrert er ikke det samme som skjedd. En opprydding kan samle utvandringer fra flere kvartaler i ett.", int((w - 16) / 6.6)), size=12, lh=16, fill=MORK)
    return y + 142


TRINN = [
    ("Noe skjer", "Fødsler, dødsfall og flyttinger meldes til Folkeregisteret hos Skatteetaten.", v_hendelser),
    ("Bosatt eller ikke?", "Den som skal bo her minst seks måneder, blir bosatt. Bostedet er der man sover.", v_bosatt),
    ("SSB teller", "SSB får endringene hver dag og teller hvor mange som er bosatt 1. januar og ved hvert kvartal.", v_ssb),
    ("Regnskapet går opp", "Hvert år skal fødte, døde og flyttinger forklare endringen i folketallet.", v_regnskap),
    ("Tallene publiseres", "Tallene gjelder registreringen, ikke nødvendigvis når hendelsen skjedde.", v_publisering),
]

IKKE_MED = ("Ikke med i folketallet: opphold under seks måneder og personer uten lovlig opphold.")
OVERDEKNING = ("Med, men bor ikke her: personer som har flyttet ut uten å melde fra. "
               "SSB anslår dem til om lag 0,44 prosent av befolkningen.")
KILDE_K = "Kilde: SSB, statistikken Befolkning og tabell 05803. Sist oppdatert: 15.04.2026. Overdekning: SSB Notater 2024/3."


def nummer(s, x, y, n):
    s.circle(x, y, 13, fill=MORK)
    s.text(x, y + 5, n, size=14, fill="#ffffff", weight=700, anchor="middle")


def konsept_bred():
    B, H = 1200, 560
    s = Svg(B, H)
    s.text(40, 46, "Slik lages tallene", size=26, weight=700)
    s.text(40, 72, "Fra en hendelse i folkeregisteret til et publisert folketall", size=15, fill=GRA)
    s.line(40, 88, 1160, 88, stroke=LINJE)
    x0, w, gap = 40, 208, 20
    for i, (tittel, tekst, tegn) in enumerate(TRINN):
        x = x0 + i * (w + gap)
        nummer(s, x + 13, 118, str(i + 1))
        s.text(x + 34, 124, tittel, size=16, weight=700)
        ty = s.lines(x, 154, bryt(tekst, 31), size=13, lh=18, fill=MORK)
        tegn(s, x, 240, w)
        if i < len(TRINN) - 1:
            pil_hoyre(s, x + w + 3, 118, 14)
    # det tallene ikke fanger
    s.rect(40, 424, 1120, 90, fill=GRAA_BG, stroke=GRAA, dash="6 4")
    s.text(56, 448, "Det tallene ikke fanger", size=14, weight=700, fill=MORK)
    s.lines(56, 472, bryt(IKKE_MED, 70), size=13, lh=18, fill=MORK)
    s.lines(620, 472, bryt(OVERDEKNING, 70), size=13, lh=18, fill=MORK)
    s.text(40, 540, KILDE_K, size=12, fill=GRA)
    s.save(os.path.join(ROT, "src", "konsept-bred.svg"))


def konsept_smal():
    B = 390
    s = Svg(B, 10)
    s.text(16, 36, "Slik lages tallene", size=22, weight=700)
    s.lines(16, 60, bryt("Fra en hendelse i folkeregisteret til et publisert folketall", 44), size=14, lh=19, fill=GRA)
    s.line(16, 90, B - 16, 90, stroke=LINJE)
    y = 122
    w = B - 32 - 34
    for i, (tittel, tekst, tegn) in enumerate(TRINN):
        nummer(s, 29, y - 5, str(i + 1))
        s.text(50, y, tittel, size=16, weight=700)
        ty = s.lines(50, y + 26, bryt(tekst, 40), size=13, lh=18, fill=MORK)
        yb = tegn(s, 50, ty + 6, w)
        if i < len(TRINN) - 1:
            s.line(29, y + 12, 29, yb + 10, stroke=LINJE, sw=1.5)
        y = yb + 44
    s.rect(16, y - 14, B - 32, 10, fill="none")
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


def y_akse(s, x0, x1, ytop, ybot, maks, steg, enhet, fmt=nb, minv=0):
    def ys(v):
        return ybot - (v - minv) / (maks - minv) * (ybot - ytop)
    v = minv
    while v <= maks + 1e-9:
        y = ys(v)
        s.line(x0, y, x1, y, stroke=NULL if v == 0 else STOTTE, sw=1)
        s.text(x0 - 6, y + 4, fmt(v), size=12, fill=GRA, anchor="end")
        v += steg
    s.text(x0 - 6 - 40, ytop - 16, enhet, size=12, fill=GRA)
    return ys


def topp_a():
    aar = list(range(2006, 2026))
    s = topp_ramme(
        "BEFOLKNING · 1. JANUAR 2026",
        "5,6 millioner",
        "Veksten er halvert på tre år.",
        bryt(f"Folketallet økte med {nb(AAR[2025]['folkevekst'])} i 2025, mot {nb(AAR[2022]['folkevekst'])} i 2022. "
             f"Det er den laveste veksten siden 2020.", 62),
        "Kilde: SSB, tabell 05803. Sist oppdatert: 15.04.2026.",
    )
    # Versjon 0.2: A med todelingen fra B (vedtatt av Thomas 21.10.2026)
    x0, x1, ytop, ybot = 640, 1060, 70, 270
    s.text(x0 - 46, 34, "Folkevekst per år, 2006–2025", size=14, weight=600)
    ys = y_akse(s, x0, x1, ytop, ybot, 70000, 10000, "personer")
    n = len(aar)
    slot = (x1 - x0) / n
    bw = slot * 0.66
    for i, a in enumerate(aar):
        r = AAR[a]
        f, ni = r["fodselsoverskudd"], r["nettoinnvandring"]
        x = x0 + i * slot + (slot - bw) / 2
        s.rect(x, ys(f), bw, ybot - ys(f), fill=F_GRONN)
        s.rect(x, ys(f + ni), bw, ys(f) - ys(f + ni), fill=F_BLA)
        if a % 5 == 0 or a == 2025:
            s.text(x + bw / 2, ybot + 18, str(a), size=12, fill=GRA, anchor="middle")
        if a in (2011, 2022, 2025):
            s.text(x + bw / 2, ys(f + ni) - 6, nb(r["folkevekst"]), size=12, fill=MORK, anchor="middle", weight=600)
    xl = x1 + 8
    f, ni = A25["fodselsoverskudd"], A25["nettoinnvandring"]
    s.text(xl, (ys(f) + ybot) / 2 + 4, "Fødsels-", size=12.5, fill=MORK, weight=600)
    s.text(xl, (ys(f) + ybot) / 2 + 20, "overskudd", size=12.5, fill=MORK, weight=600)
    s.text(xl, (ys(f + ni) + ys(f)) / 2 + 4, "Netto-", size=12.5, fill=MORK, weight=600)
    s.text(xl, (ys(f + ni) + ys(f)) / 2 + 20, "innvandring", size=12.5, fill=MORK, weight=600)
    kor = [AAR[a]["korreksjon"] for a in aar]
    s.text(x0 - 46, 312, f"Tallene over stolpene er folkeveksten. Korreksjonsposten ({nb(min(kor))} til {nb(max(kor))} per år) er ikke tegnet.", size=12, fill=GRA)
    s.save(os.path.join(ROT, "docs", "grafikk", "02-topp-a.svg"))


def topp_b():
    aar = list(range(2016, 2026))
    kor = [AAR[a]["korreksjon"] for a in aar]
    andel = A25["nettoinnvandring"] / A25["folkevekst"] * 100
    s = topp_ramme(
        "BEFOLKNING · FOLKEVEKST 2025",
        "To tredjedeler",
        "av folkeveksten i 2025 kom fra nettoinnvandring.",
        bryt(f"Nettoinnvandringen var {nb(A25['nettoinnvandring'])}, eller {nb(andel, 1)} prosent av veksten. "
             f"Fødselsoverskuddet var {nb(A25['fodselsoverskudd'])}.", 62),
        "Kilde: SSB, tabell 05803. Sist oppdatert: 15.04.2026.",
    )
    x0, x1, ytop, ybot = 640, 1060, 70, 270
    s.text(x0 - 46, 34, "Folkeveksten delt i to, 2016–2025", size=14, weight=600)
    ys = y_akse(s, x0, x1, ytop, ybot, 70000, 10000, "personer")
    n = len(aar)
    slot = (x1 - x0) / n
    bw = slot * 0.66
    for i, a in enumerate(aar):
        r = AAR[a]
        x = x0 + i * slot + (slot - bw) / 2
        f, ni = r["fodselsoverskudd"], r["nettoinnvandring"]
        s.rect(x, ys(f), bw, ybot - ys(f), fill=F_GRONN)
        s.rect(x, ys(f + ni), bw, ys(f) - ys(f + ni), fill=F_BLA)
        if a % 2 == 0 or a == 2025:
            s.text(x + bw / 2, ybot + 18, str(a), size=12, fill=GRA, anchor="middle")
    # direkte merking ved siste stolpe
    xl = x1 + 8
    f, ni = A25["fodselsoverskudd"], A25["nettoinnvandring"]
    s.text(xl, (ys(f) + ybot) / 2 + 4, "Fødsels-", size=12.5, fill=MORK, weight=600)
    s.text(xl, (ys(f) + ybot) / 2 + 20, "overskudd", size=12.5, fill=MORK, weight=600)
    s.text(xl, (ys(f + ni) + ys(f)) / 2 + 4, "Netto-", size=12.5, fill=MORK, weight=600)
    s.text(xl, (ys(f + ni) + ys(f)) / 2 + 20, "innvandring", size=12.5, fill=MORK, weight=600)
    s.text(x0 - 46, 312, f"Korreksjonsposten, fra {nb(min(kor))} til {nb(max(kor))} personer per år, er ikke vist.", size=12, fill=GRA)
    s.save(os.path.join(ROT, "docs", "grafikk", "02-topp-b.svg"))


def topp_c():
    kom = D["kommuner"]
    n = len(kom)
    ned = sum(1 for k in kom if k["endring"] < 0)
    norge = A25["folkevekst"] / A25["bef_start"] * 100
    s = topp_ramme(
        "BEFOLKNING · KOMMUNENE 2025",
        "1 av 3",
        "kommuner fikk færre innbyggere i 2025.",
        bryt(f"{ned} av {n} kommuner krympet, mens folketallet i hele landet økte med {nb(norge, 2)} prosent.", 62),
        "Kilde: SSB, tabell 07459, kommuner 2024. Sist oppdatert: 25.02.2026.",
    )
    lo, hi, bin_ = -5.0, 3.0, 0.5
    nb_ = int((hi - lo) / bin_)
    teller = [0] * (nb_ + 1)  # siste = over hi
    for k in kom:
        p = k["endring_prosent"]
        if p >= hi:
            teller[-1] += 1
        else:
            teller[int((p - lo) // bin_)] += 1
    x0, x1, ytop, ybot = 640, 1130, 70, 260
    s.text(x0 - 46, 34, "Antall kommuner etter endring i folketallet 2025", size=14, weight=600)
    maks = 80
    ys = y_akse(s, x0, x1, ytop, ybot, maks, 20, "kommuner")
    slot = (x1 - x0) / (nb_ + 1.6)

    def xs(p):
        return x0 + (p - lo) / bin_ * slot

    for i, t in enumerate(teller[:-1]):
        a = lo + i * bin_
        farge = F_OKER if a < 0 else F_GRONN
        s.rect(xs(a), ys(t), slot - 0.5, ybot - ys(t), fill=farge)
    # overflow-stolpe
    xo = xs(hi) + 0.6 * slot
    s.rect(xo, ys(teller[-1]), slot - 0.5, ybot - ys(teller[-1]), fill=F_GRONN)
    s.text(xo + slot / 2, ybot + 18, "3+", size=12, fill=GRA, anchor="middle")
    for p in (-4, -2, 0, 2):
        s.text(xs(p), ybot + 18, sgn(p) if p else "0", size=12, fill=GRA, anchor="middle")
    s.text(x1 + 10, ybot + 18, "prosent", size=12, fill=GRA)
    # landsgjennomsnitt
    xn = xs(norge)
    s.line(xn, ytop - 4, xn, ybot, stroke=MORK, sw=1.2, dash="4 3")
    s.text(xn + 6, ytop + 6, f"Hele landet {sgn(norge, 2)} prosent", size=12, fill=MORK, weight=600)
    s.text(xs(-4.6), ys(44), f"{ned} med nedgang", size=12.5, fill=MORK, weight=600)
    s.text(xs(1.3), ys(52), f"{n - ned} med vekst", size=12.5, fill=MORK, weight=600)
    s.text(xs(1.3), ys(52) + 16, "eller uendret", size=12.5, fill=MORK, weight=600)
    s.save(os.path.join(ROT, "docs", "grafikk", "02-topp-c.svg"))
    return teller


if __name__ == "__main__":
    konsept_bred()
    konsept_smal()
    topp_a()
    topp_b()
    print("histogram", topp_c())

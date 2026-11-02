"""SVG-primitiver for pasient (konsept- og toppgrafikk).

Samme funksjonsnavn som i de andre prototypene: Svg, nb, sgn, bryt.
"""
from xml.sax.saxutils import escape

FONT = "Open Sans, Segoe UI, Arial, sans-serif"

# Konseptfigurpalett
MORK = "#274246"
BLEKK = "#1e3a3f"
GRA_TEKST = "#5e787a"
LINJE = "#cdd3d4"
BG_FLATE, BG_KANT = "#eff8fa", "#c4dddb"
GRONN, GRONN_LYS, GRONN_BG = "#00824d", "#b6e9b8", "#ecfeed"
LILLA, LILLA_LYS, LILLA_BG, LILLA_TEKST = "#7d5fea", "#c3baff", "#f1f1fe", "#4b2fb0"
GRA, GRA_BG = "#b9c5c6", "#f3f5f5"
# Diagramstandard
STOTTE = "#d9dfe0"
NULL = "#a9b5b7"


def nb(x, des=0):
    """Norsk tallformat: mellomrom som tusenskille, komma som desimaltegn."""
    s = f"{abs(x):,.{des}f}".replace(",", " ").replace(".", ",")
    return ("−" if x < 0 else "") + s


def sgn(x, des=0):
    """Tall med fortegn: +1 234 / −1 234."""
    return ("+" if x > 0 else "") + nb(x, des)


def bryt(tekst, maks):
    """Manuell linjebryting etter antall tegn."""
    linjer, lin = [], ""
    for ord_ in [o for o in tekst.split(" ") if o]:  # ikke del på hardt mellomrom i tall
        if lin and len(lin) + 1 + len(ord_) > maks:
            linjer.append(lin)
            lin = ord_
        else:
            lin = f"{lin} {ord_}".strip()
    if lin:
        linjer.append(lin)
    return linjer


class Svg:
    def __init__(self, b, h, tittel=""):
        self.b, self.h = b, h
        self.deler = []
        self.tittel = tittel

    def add(self, s):
        self.deler.append(s)

    def rect(self, x, y, b, h, fyll="none", strek="none", sb=1, stiplet=False):
        d = ' stroke-dasharray="6 4"' if stiplet else ""
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{b:.1f}" height="{h:.1f}" '
                 f'fill="{fyll}" stroke="{strek}" stroke-width="{sb}"{d}/>')

    def linje(self, x1, y1, x2, y2, strek=LINJE, sb=1, stiplet=False):
        d = ' stroke-dasharray="5 4"' if stiplet else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{strek}" stroke-width="{sb}"{d}/>')

    def polyline(self, punkter, strek, sb=2, stiplet=False):
        d = ' stroke-dasharray="6 4"' if stiplet else ""
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in punkter)
        self.add(f'<polyline points="{p}" fill="none" stroke="{strek}" '
                 f'stroke-width="{sb}" stroke-linejoin="round"{d}/>')

    def sirkel(self, x, y, r, fyll, strek="none", sb=1):
        self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fyll}" '
                 f'stroke="{strek}" stroke-width="{sb}"/>')

    def tekst(self, x, y, s, str_=16, farge=MORK, vekt=400, anker="start"):
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{str_}" '
                 f'font-weight="{vekt}" fill="{farge}" text-anchor="{anker}" '
                 f'style="font-variant-numeric:tabular-nums">{escape(str(s))}</text>')

    def tekstlinjer(self, x, y, linjer, str_=16, farge=MORK, vekt=400, anker="start", lh=None):
        lh = lh or round(str_ * 1.35)
        for i, l in enumerate(linjer):
            self.tekst(x, y + i * lh, l, str_, farge, vekt, anker)
        return y + len(linjer) * lh

    def pil(self, x1, y1, x2, y2, farge=GRA_TEKST, sb=2, spiss=9):
        import math
        v = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - spiss * math.cos(v), y2 - spiss * math.sin(v)
        self.linje(x1, y1, bx, by, farge, sb)
        p1 = (x2, y2)
        p2 = (bx + spiss * 0.55 * math.sin(v), by - spiss * 0.55 * math.cos(v))
        p3 = (bx - spiss * 0.55 * math.sin(v), by + spiss * 0.55 * math.cos(v))
        self.add('<polygon points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in (p1, p2, p3))
                 + f'" fill="{farge}"/>')

    def markor(self, x, y, n, fyll=MORK):
        self.sirkel(x, y, 15, fyll)
        self.tekst(x, y + 6, n, 17, "#ffffff", 700, "middle")

    def lagre(self, sti):
        t = f"<title>{escape(self.tittel)}</title>" if self.tittel else ""
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.b}" height="{self.h}" '
               f'viewBox="0 0 {self.b} {self.h}">{t}'
               f'<rect width="{self.b}" height="{self.h}" fill="#ffffff"/>'
               + "".join(self.deler) + "</svg>")
        with open(sti, "w", encoding="utf-8") as f:
            f.write(svg)

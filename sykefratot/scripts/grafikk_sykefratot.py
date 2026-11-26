"""SVG-primitiver for konsept- og toppgrafikk.

Brukes av lag_grafikk.py for sykefratot. Samme primitiver som i de andre
prototypene (Svg, nb, sgn, bryt). Bare Pythons standardbibliotek.
"""
from xml.sax.saxutils import escape

SANS = "Open Sans, Segoe UI, Arial, sans-serif"
ROBOTO = "Roboto, Arial, sans-serif"
COND = "Roboto Condensed, Arial Narrow, Arial, sans-serif"

# Profilfarger (ssb-konseptfigurer) og nøytrale diagramfarger (ssb-diagramstandard)
M5, M2, M1 = "#274247", "#c3dcdc", "#f0f8f9"
G4, G2, G1 = "#00824d", "#b6e8b8", "#ecfeed"
GRA_TEKST, LINJE = "#5e787a", "#cdd3d4"
GRA, GRA_FLATE = "#b9c5c6", "#f3f5f5"
TEKST = "#274247"  # mørk 5; diagramstandardens foreløpige #274246 er samlet hit
STOTTE, NULL = "#d9dfe0", "#a9b5b7"
GRONN5 = ["#cff1d0", "#91cd9a", "#58a772", "#00824d", "#075745"]


def nb(x, des=1):
    """Norsk tallformat: komma som desimaltegn, mellomrom som tusenskille."""
    s = f"{x:,.{des}f}"
    return s.replace(",", "\u00a0").replace(".", ",")


def sgn(x, des=1):
    """Fortegn med ekte minustegn."""
    return ("+" if x > 0 else "−" if x < 0 else "") + nb(abs(x), des)


def bryt(tekst, maks):
    """Manuell linjebryting etter antall tegn."""
    linjer, cur = [], ""
    for ord_ in tekst.split(" "):
        if cur and len(cur) + 1 + len(ord_) > maks:
            linjer.append(cur)
            cur = ord_
        else:
            cur = (cur + " " + ord_).strip()
    if cur:
        linjer.append(cur)
    return linjer


class Svg:
    def __init__(self, w, h, tittel=""):
        self.w, self.h, self.el = w, h, []
        self.tittel = tittel

    def rect(self, x, y, w, h, fill="none", stroke="none", sw=1, rx=0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
                       f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def line(self, x1, y1, x2, y2, stroke=M5, sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                       f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def polyline(self, pts, stroke=G4, sw=2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.el.append(f'<polyline points="{p}" fill="none" stroke="{stroke}" stroke-width="{sw}" '
                       f'stroke-linejoin="round"{d}/>')

    def polygon(self, pts, fill=M5):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.el.append(f'<polygon points="{p}" fill="{fill}"/>')

    def circle(self, cx, cy, r, fill=M5, stroke="none", sw=1):
        self.el.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, s, size=15, fill=TEKST, weight=400, anchor="start", font=SANS):
        st = ' font-stretch="condensed"' if font == COND else ""
        self.el.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}"{st} '
                       f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')

    def lines(self, x, y, linjer, size=15, lh=None, **kw):
        lh = lh or round(size * 1.4)
        for i, l in enumerate(linjer):
            self.text(x, y + i * lh, l, size=size, **kw)
        return y + len(linjer) * lh

    def pil(self, x1, y1, x2, y2, farge=M5, sw=2, spiss=9):
        """Rett pil, vannrett eller loddrett, spiss som polygon."""
        if y1 == y2:
            r = 1 if x2 > x1 else -1
            self.line(x1, y1, x2 - r * spiss, y2, farge, sw)
            self.polygon([(x2, y2), (x2 - r * spiss, y2 - spiss * 0.6), (x2 - r * spiss, y2 + spiss * 0.6)], farge)
        else:
            r = 1 if y2 > y1 else -1
            self.line(x1, y1, x2, y2 - r * spiss, farge, sw)
            self.polygon([(x2, y2), (x2 - spiss * 0.6, y2 - r * spiss), (x2 + spiss * 0.6, y2 - r * spiss)], farge)

    def markor(self, cx, cy, n, r=15):
        self.circle(cx, cy, r, M5)
        self.text(cx, cy + 5.5, str(n), size=15, fill="#ffffff", weight=700, anchor="middle", font=ROBOTO)

    def svg(self):
        t = f"<title>{escape(self.tittel)}</title>" if self.tittel else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}">{t}<rect x="0" y="0" width="{self.w}" height="{self.h}" '
                f'fill="#ffffff"/>' + "".join(self.el) + "</svg>")

    def lagre(self, sti):
        with open(sti, "w", encoding="utf-8") as f:
            f.write(self.svg())

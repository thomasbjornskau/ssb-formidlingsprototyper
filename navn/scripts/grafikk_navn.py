"""SVG-primitiver for konsept- og toppgrafikken i navn: Svg, nb, sgn og bryt.

Bare Pythons standardbibliotek.
"""
from xml.sax.saxutils import escape

FONT = "'Open Sans', 'Segoe UI', Arial, sans-serif"


def nb(x, des=0):
    """Norsk tallformat: mellomrom som tusenskille, komma som desimaltegn."""
    s = f"{x:,.{des}f}"
    return s.replace(",", " ").replace(".", ",")


def sgn(x, des=1):
    """Tall med fortegn, norsk format."""
    return ("+" if x > 0 else "−" if x < 0 else "") + nb(abs(x), des)


def bryt(tekst, maks):
    """Manuell linjebryting på antall tegn."""
    linjer, cur = [], ""
    for ord_ in tekst.split():
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

    def add(self, s):
        self.el.append(s)

    def rect(self, x, y, w, h, fill="none", stroke="none", sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def line(self, x1, y1, x2, y2, stroke="#a9b5b7", sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def polyline(self, pts, stroke="#00824d", sw=2.5):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.add(f'<polyline points="{p}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>')

    def polygon(self, pts, fill="#274246"):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.add(f'<polygon points="{p}" fill="{fill}"/>')

    def circle(self, x, y, r, fill="#00824d", stroke="none", sw=1):
        self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, s, size=14, fill="#274246", weight=400, anchor="start"):
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" style="font-variant-numeric:tabular-nums">{escape(s)}</text>')

    def tekstblokk(self, x, y, linjer, size=14, lh=1.4, **kw):
        for i, l in enumerate(linjer):
            self.text(x, y + i * size * lh, l, size=size, **kw)
        return y + len(linjer) * size * lh

    def pil(self, x1, y1, x2, y2, stroke="#5e787a", sw=1.5):
        """Pil med pilspiss som polygon (horisontal eller vertikal)."""
        self.line(x1, y1, x2, y2, stroke=stroke, sw=sw)
        if y1 == y2:
            s = 1 if x2 > x1 else -1
            self.polygon([(x2, y2), (x2 - 9 * s, y2 - 5), (x2 - 9 * s, y2 + 5)], fill=stroke)
        else:
            s = 1 if y2 > y1 else -1
            self.polygon([(x2, y2), (x2 - 5, y2 - 9 * s), (x2 + 5, y2 - 9 * s)], fill=stroke)

    def markor(self, x, y, n, r=15):
        self.circle(x, y, r, fill="#274246")
        self.text(x, y + 5, str(n), size=14, fill="#ffffff", weight=700, anchor="middle")

    def svg(self):
        t = f"<title>{escape(self.tittel)}</title>" if self.tittel else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}">{t}<rect width="{self.w}" height="{self.h}" fill="#ffffff"/>'
                + "".join(self.el) + "</svg>")

    def lagre(self, sti):
        with open(sti, "w", encoding="utf-8") as f:
            f.write(self.svg())

"""Minimale SVG-primitiver for konsept- og toppgrafikk.

Brukes av lag_grafikk.py i arbstatus-neet. Repoet har ingen felles grafikkmodul,
så den ligger her, i prototypens egen mappe. Bare Pythons standardbibliotek.
"""
from xml.sax.saxutils import escape

F_TITTEL = "Roboto Condensed, Arial Narrow, Arial, sans-serif"
F_MELLOM = "Roboto, Arial, sans-serif"
F_TEKST = "Open Sans, Segoe UI, Arial, sans-serif"


def nb(x, des=0):
    """Norsk tallformat: mellomrom som tusenskille, komma som desimaltegn."""
    s = f"{x:,.{des}f}".replace(",", " ").replace(".", ",")
    return s.replace("-", "−")


def sgn(x, des=0):
    """Tall med fortegn (+ / −)."""
    return ("+" if x > 0 else "") + nb(x, des)


def bryt(tekst, maks):
    """Bryter tekst manuelt på ord, maks tegn per linje."""
    linjer, linje = [], ""
    for ord_ in tekst.split():
        if linje and len(linje) + 1 + len(ord_) > maks:
            linjer.append(linje)
            linje = ord_
        else:
            linje = (linje + " " + ord_).strip()
    if linje:
        linjer.append(linje)
    return linjer


class Svg:
    def __init__(self, b, h, bakgrunn="#ffffff", tittel=None):
        self.b, self.h = b, h
        self.deler = []
        if tittel:
            self.deler.append(f"<title>{escape(tittel)}</title>")
        if bakgrunn:
            self.rect(0, 0, b, h, fill=bakgrunn)

    @staticmethod
    def _a(**kw):
        return " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items() if v is not None)

    def rect(self, x, y, b, h, fill="none", stroke=None, sw=None, rx=None, dash=None):
        self.deler.append(f"<rect {self._a(x=round(x,2), y=round(y,2), width=round(b,2), height=round(h,2), fill=fill, stroke=stroke, stroke_width=sw, rx=rx, stroke_dasharray=dash)}/>")

    def line(self, x1, y1, x2, y2, stroke="#274247", sw=1, dash=None):
        self.deler.append(f"<line {self._a(x1=round(x1,2), y1=round(y1,2), x2=round(x2,2), y2=round(y2,2), stroke=stroke, stroke_width=sw, stroke_dasharray=dash)}/>")

    def polyline(self, pts, stroke="#274247", sw=2, fill="none"):
        p = " ".join(f"{round(x,2)},{round(y,2)}" for x, y in pts)
        self.deler.append(f"<polyline {self._a(points=p, fill=fill, stroke=stroke, stroke_width=sw, stroke_linejoin='round')}/>")

    def polygon(self, pts, fill="#274247", stroke=None):
        p = " ".join(f"{round(x,2)},{round(y,2)}" for x, y in pts)
        self.deler.append(f"<polygon {self._a(points=p, fill=fill, stroke=stroke)}/>")

    def circle(self, cx, cy, r, fill="#274247", stroke=None, sw=None):
        self.deler.append(f"<circle {self._a(cx=round(cx,2), cy=round(cy,2), r=round(r,2), fill=fill, stroke=stroke, stroke_width=sw)}/>")

    def text(self, x, y, t, size=16, fill="#274247", font=F_TEKST, weight=None, anchor=None, num=False):
        stil = "font-variant-numeric:tabular-nums" if num else None
        self.deler.append(f"<text {self._a(x=round(x,2), y=round(y,2), font_family=font, font_size=size, font_weight=weight, fill=fill, text_anchor=anchor, style=stil)}>{escape(str(t))}</text>")

    def tekstblokk(self, x, y, t, maks, size=16, lh=None, **kw):
        lh = lh or round(size * 1.4)
        linjer = bryt(t, maks)
        for i, l in enumerate(linjer):
            self.text(x, y + i * lh, l, size=size, **kw)
        return y + len(linjer) * lh

    def pil(self, x1, y1, x2, y2, farge="#274247", sw=2, spiss=10):
        """Rett pil med fylt trekant som spiss (vannrett eller loddrett)."""
        if y1 == y2:
            r = 1 if x2 > x1 else -1
            self.line(x1, y1, x2 - r * spiss, y2, stroke=farge, sw=sw)
            self.polygon([(x2, y2), (x2 - r * spiss, y2 - spiss * 0.6), (x2 - r * spiss, y2 + spiss * 0.6)], fill=farge)
        else:
            r = 1 if y2 > y1 else -1
            self.line(x1, y1, x2, y2 - r * spiss, stroke=farge, sw=sw)
            self.polygon([(x2, y2), (x2 - spiss * 0.6, y2 - r * spiss), (x2 + spiss * 0.6, y2 - r * spiss)], fill=farge)

    def lagre(self, sti):
        with open(sti, "w", encoding="utf-8") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.b}" height="{self.h}" viewBox="0 0 {self.b} {self.h}">\n')
            f.write("\n".join(self.deler))
            f.write("\n</svg>\n")

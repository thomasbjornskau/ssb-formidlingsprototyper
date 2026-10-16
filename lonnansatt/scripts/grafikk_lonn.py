"""SVG-primitiver for konsept- og toppgrafikk i formidlingsprototypene.

Kopi av muh/scripts/grafikk_muh.py. kpi/scripts/lag_grafikk.py importerer felles/grafikk.py,
men den filen finnes ikke i repoet. Denne gjenskaper grensesnittet (Svg, nb,
sgn, bryt) med bare standardbiblioteket, slik at lonnansatt kan bygge grafikken selv.

Reglene fra ssb-konseptfigurer: bare enkle elementer, ingen CSS-klasser,
filtre eller markører, pilspisser som polygoner, farger som attributter.
"""

from xml.sax.saxutils import escape

FONT = "'Open Sans', 'Segoe UI', Arial, sans-serif"

# Farger fra ssb-konseptfigurer og ssb-diagramstandard
MORK = "#274246"
BLEKK = "#1e3a3f"
GRA_TEKST = "#5e787a"
LINJE = "#cdd3d4"
BLAGRONN_LYS = "#eff8fa"
BLAGRONN = "#c4dddb"
GRONN = "#00824d"
GRONN_MID = "#b6e9b8"
GRONN_LYS = "#ecfeed"
GRA = "#b9c5c6"
GRA_LYS = "#f3f5f5"
STOTTELINJE = "#d9dfe0"
NULLINJE = "#a9b5b7"
# Kategorisk ssb-justert: (strek, flate)
KAT = [("#00824d", "#339b71"), ("#1d9de2", "#3face6"), ("#c78800", "#d5a640"),
       ("#c775a7", "#cd83b0"), ("#0f2080", "#5763a6"), ("#a3136c", "#a3136c")]

MINUS = "−"
NBSP = " "


def nb(x, des=0):
    """Norsk tallformat: hardt mellomrom som tusenskille, komma som desimaltegn, ekte minus."""
    s = f"{abs(x):,.{des}f}".replace(",", NBSP).replace(".", ",")
    return (MINUS if x < 0 else "") + s


def sgn(x, des=0):
    """Tall med fortegn: +1,2 eller −1,2."""
    return ("+" if x > 0 else "") + nb(x, des)


def bryt(tekst, maks):
    """Manuell linjebryting på ord, maks tegn per linje."""
    linjer, linje = [], ""
    for ord_ in [o for o in tekst.split(" ") if o]:
        if linje and len(linje) + 1 + len(ord_) > maks:
            linjer.append(linje)
            linje = ord_
        else:
            linje = f"{linje} {ord_}" if linje else ord_
    if linje:
        linjer.append(linje)
    return linjer


def _a(**kw):
    deler = []
    for k, v in kw.items():
        if v is None:
            continue
        k = k.rstrip("_").replace("_", "-")
        deler.append(f'{k}="{v}"')
    return " ".join(deler)


class Svg:
    def __init__(self, b, h, tittel=None, beskrivelse=None):
        self.b, self.h = b, h
        self.deler = []
        self.tittel, self.beskrivelse = tittel, beskrivelse

    def rect(self, x, y, b, h, fill="none", stroke=None, sw=None, dash=None):
        self.deler.append(f"<rect {_a(x=x, y=y, width=b, height=h, fill=fill, stroke=stroke, stroke_width=sw, stroke_dasharray=dash)}/>")

    def line(self, x1, y1, x2, y2, stroke=LINJE, sw=1, dash=None):
        self.deler.append(f"<line {_a(x1=x1, y1=y1, x2=x2, y2=y2, stroke=stroke, stroke_width=sw, stroke_dasharray=dash)}/>")

    def polyline(self, punkter, stroke, sw=2, dash=None):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in punkter)
        self.deler.append(f'<polyline points="{p}" {_a(fill="none", stroke=stroke, stroke_width=sw, stroke_dasharray=dash, stroke_linejoin="round")}/>')

    def polygon(self, punkter, fill):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in punkter)
        self.deler.append(f'<polygon points="{p}" fill="{fill}"/>')

    def circle(self, cx, cy, r, fill, stroke=None, sw=None):
        self.deler.append(f"<circle {_a(cx=cx, cy=cy, r=r, fill=fill, stroke=stroke, stroke_width=sw)}/>")

    def text(self, x, y, tekst, size=16, fill=MORK, weight=400, anchor="start"):
        self.deler.append(
            f'<text {_a(x=x, y=y, font_family=FONT, font_size=size, font_weight=weight, fill=fill, text_anchor=anchor)}>'
            f'{escape(tekst)}</text>')
        # Open Sans har tabellsifre som standard, så tallkolonner står rett uten CSS.

    def tekstblokk(self, x, y, linjer, size=16, linjeavstand=None, **kw):
        la = linjeavstand or round(size * 1.35)
        for i, l in enumerate(linjer):
            self.text(x, y + i * la, l, size=size, **kw)
        return y + (len(linjer) - 1) * la

    def pil(self, x1, y1, x2, y2, stroke=MORK, sw=2, spiss=9):
        """Rett pil med pilspiss som polygon. Linjen stopper ved spissens bakkant."""
        import math
        v = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - spiss * math.cos(v), y2 - spiss * math.sin(v)
        self.line(x1, y1, bx, by, stroke=stroke, sw=sw)
        px, py = -math.sin(v) * spiss * 0.55, math.cos(v) * spiss * 0.55
        self.polygon([(x2, y2), (bx + px, by + py), (bx - px, by - py)], stroke)

    def markor(self, cx, cy, n, r=16, fill=MORK):
        """Nummerert markør."""
        self.circle(cx, cy, r, fill)
        self.text(cx, cy + r * 0.38, str(n), size=round(r * 1.05), fill="#ffffff", weight=700, anchor="middle")

    def lagre(self, sti):
        hode = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.b}" height="{self.h}" viewBox="0 0 {self.b} {self.h}" role="img">']
        if self.tittel:
            hode.append(f"<title>{escape(self.tittel)}</title>")
        if self.beskrivelse:
            hode.append(f"<desc>{escape(self.beskrivelse)}</desc>")
        hode.append(f'<rect x="0" y="0" width="{self.b}" height="{self.h}" fill="#ffffff"/>')
        with open(sti, "w", encoding="utf-8") as f:
            f.write("\n".join(hode + self.deler + ["</svg>"]) + "\n")

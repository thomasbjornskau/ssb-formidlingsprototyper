"""SVG-primitiver for grafikkutkastene i ufore (steg 2), etter mønster fra grafikk_pasient.py.
Brukes bare av scripts/lag_grafikk.py, ikke av bygget."""

from xml.sax.saxutils import escape

TITTEL = "Roboto Condensed, Arial Narrow, Arial, sans-serif"
MELLOM = "Roboto, Arial, sans-serif"
BROD = "Open Sans, Segoe UI, Arial, sans-serif"

# Konseptfigurfarger (ssb-konseptfigurer)
M5, M1, M2 = "#274247", "#f0f8f9", "#c3dcdc"
G4, G2, G1 = "#00824d", "#b6e8b8", "#ecfeed"
GRA_T, GRA_L = "#5e787a", "#cdd3d4"
GRA_S, GRA_F = "#b9c5c6", "#f3f5f5"
HVIT = "#ffffff"
# Diagramfarger (ssb-diagramstandard)
STOTTE, NULL = "#d9dfe0", "#a9b5b7"
TEKST = "#274246"


def nb(x, des=0):
    """Norsk tallformat: hardt mellomrom som tusenskille, komma som desimaltegn."""
    s = f"{x:,.{des}f}".replace(",", " ").replace(".", ",")
    return s.replace("-", "−")


def sgn(x, des=0):
    return ("+" if x > 0 else "") + nb(x, des)


def bryt(tekst, maks):
    """Manuell linjebryting etter antall tegn."""
    linjer, linje = [], ""
    for ord_ in tekst.split(" "):
        if linje and len(linje) + 1 + len(ord_) > maks:
            linjer.append(linje)
            linje = ord_
        else:
            linje = f"{linje} {ord_}".strip()
    if linje:
        linjer.append(linje)
    return linjer


class Svg:
    def __init__(self, b, h, tittel=None, beskrivelse=None):
        self.b, self.h, self.deler = b, h, []
        self.tittel, self.beskrivelse = tittel, beskrivelse

    def rect(self, x, y, b, h, fyll=HVIT, strek=None, sb=1, rx=2, stiplet=False):
        a = f'<rect x="{x:.1f}" y="{y:.1f}" width="{b:.1f}" height="{h:.1f}" rx="{rx}" fill="{fyll}"'
        if strek:
            a += f' stroke="{strek}" stroke-width="{sb}"'
            if stiplet:
                a += ' stroke-dasharray="6 4"'
        self.deler.append(a + "/>")

    def line(self, x1, y1, x2, y2, strek=M5, sb=1, stiplet=False):
        a = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{strek}" stroke-width="{sb}"'
        if stiplet:
            a += ' stroke-dasharray="5 4"'
        self.deler.append(a + "/>")

    def polyline(self, pkt, strek=G4, sb=2):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pkt)
        self.deler.append(f'<polyline points="{p}" fill="none" stroke="{strek}" stroke-width="{sb}" stroke-linejoin="round"/>')

    def polygon(self, pkt, fyll=M5):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pkt)
        self.deler.append(f'<polygon points="{p}" fill="{fyll}"/>')

    def circle(self, x, y, r, fyll=G4, strek=None, sb=1):
        a = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fyll}"'
        if strek:
            a += f' stroke="{strek}" stroke-width="{sb}"'
        self.deler.append(a + "/>")

    def text(self, x, y, tekst, str_=16, font=BROD, vekt=400, farge=M5, anker="start", linjeh=None, tall=False):
        linjer = tekst if isinstance(tekst, list) else [tekst]
        lh = linjeh or round(str_ * 1.35)
        stil = ' font-variant-numeric="tabular-nums"' if tall else ""
        for i, l in enumerate(linjer):
            self.deler.append(
                f'<text x="{x:.1f}" y="{y + i * lh:.1f}" font-family="{font}" font-size="{str_}" '
                f'font-weight="{vekt}" fill="{farge}" text-anchor="{anker}"{stil}>{escape(l)}</text>')
        return y + (len(linjer) - 1) * lh

    def pil(self, x1, y1, x2, y2, farge=M5, sb=2, spiss=9):
        """Rett pil med pilspiss som polygon (bare vannrett eller loddrett)."""
        if y1 == y2:
            r = 1 if x2 > x1 else -1
            self.line(x1, y1, x2 - r * spiss, y2, farge, sb)
            self.polygon([(x2, y2), (x2 - r * spiss, y2 - spiss * 0.6), (x2 - r * spiss, y2 + spiss * 0.6)], farge)
        else:
            r = 1 if y2 > y1 else -1
            self.line(x1, y1, x2, y2 - r * spiss, farge, sb)
            self.polygon([(x2, y2), (x2 - spiss * 0.6, y2 - r * spiss), (x2 + spiss * 0.6, y2 - r * spiss)], farge)

    def markor(self, x, y, n, r=14):
        self.circle(x, y, r, G4)
        self.text(x, y + 5, str(n), 15, MELLOM, 700, HVIT, "middle")

    def svg(self):
        hode = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.b} {self.h}" '
                f'width="{self.b}" height="{self.h}" role="img">')
        meta = ""
        if self.tittel:
            meta += f"<title>{escape(self.tittel)}</title>"
        if self.beskrivelse:
            meta += f"<desc>{escape(self.beskrivelse)}</desc>"
        return hode + meta + f'<rect x="0" y="0" width="{self.b}" height="{self.h}" fill="{HVIT}"/>' + "".join(self.deler) + "</svg>"

    def lagre(self, sti):
        with open(sti, "w", encoding="utf-8") as f:
            f.write(self.svg())

"""SVG-primitiver for konsept- og toppgrafikk i overnatting.

Egen kopi for overnatting, som i muh (grafikk_muh.py): repoet har ingen
felles/grafikk.py. Samme grensesnitt (Svg, nb, sgn, bryt). Bare
standardbiblioteket, med PIL som valgfri hjelp til tekstmåling ved bryting.
"""
from xml.sax.saxutils import escape

F_TITTEL = "Roboto Condensed, Arial Narrow, Arial, sans-serif"
F_OVERSKRIFT = "Roboto, Arial, sans-serif"
F_TEKST = "Open Sans, Segoe UI, Arial, sans-serif"

_FONTFILER = {
    "open": "/usr/share/fonts/truetype/google-fonts/ofl/opensans/OpenSans[wdth,wght].ttf",
    "roboto": "/usr/share/fonts/truetype/google-fonts/ofl/roboto/Roboto[wdth,wght].ttf",
}
_cache = {}


def _font(familie, storrelse, vekt):
    nokkel = (familie, storrelse, vekt)
    if nokkel not in _cache:
        try:
            from PIL import ImageFont
            f = ImageFont.truetype(_FONTFILER[familie], storrelse)
            f.set_variation_by_name("Bold" if vekt >= 600 else "Regular")
            _cache[nokkel] = f
        except Exception:
            _cache[nokkel] = None
    return _cache[nokkel]


def bredde(tekst, storrelse=14, vekt=400, familie="open"):
    f = _font(familie, storrelse, vekt)
    if f is None:
        return len(tekst) * storrelse * (0.56 if vekt >= 600 else 0.52)
    return f.getlength(tekst)


def bryt(tekst, maks_bredde, storrelse=14, vekt=400, familie="open"):
    """Bryt tekst manuelt i linjer som får plass i maks_bredde piksler."""
    linjer, linje = [], ""
    for ord_ in tekst.split(" "):
        forsok = (linje + " " + ord_).strip()
        if linje and bredde(forsok, storrelse, vekt, familie) > maks_bredde:
            linjer.append(linje)
            linje = ord_
        else:
            linje = forsok
    if linje:
        linjer.append(linje)
    return linjer


def nb(x, des=0):
    """Norsk tallformat: hardt mellomrom som tusenskille, komma som desimaltegn."""
    s = f"{abs(x):,.{des}f}".replace(",", "\u00a0").replace(".", ",")
    return ("−" if x < 0 else "") + s


def sgn(x, des=0):
    """Tall med fortegn: +1,9 eller −0,8 (ekte minustegn)."""
    return ("+" if x > 0 else "") + nb(x, des)


class Svg:
    def __init__(self, b, h, bakgrunn="#ffffff", tittel=None, beskrivelse=None):
        self.b, self.h, self.el = b, h, []
        if tittel:
            self.el.append(f"<title>{escape(tittel)}</title>")
        if beskrivelse:
            self.el.append(f"<desc>{escape(beskrivelse)}</desc>")
        if bakgrunn:
            self.rect(0, 0, b, h, fyll=bakgrunn)

    def rect(self, x, y, b, h, fyll="none", strek="none", sb=1, r=0, stiplet=None):
        d = f' stroke-dasharray="{stiplet}"' if stiplet else ""
        self.el.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{b:.1f}" height="{h:.1f}" rx="{r}" '
                       f'fill="{fyll}" stroke="{strek}" stroke-width="{sb}"{d}/>')

    def line(self, x1, y1, x2, y2, strek="#274247", sb=1, stiplet=None):
        d = f' stroke-dasharray="{stiplet}"' if stiplet else ""
        self.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                       f'stroke="{strek}" stroke-width="{sb}"{d}/>')

    def polyline(self, pkt, strek="#00824d", sb=2):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pkt)
        self.el.append(f'<polyline points="{p}" fill="none" stroke="{strek}" stroke-width="{sb}" '
                       f'stroke-linejoin="round" stroke-linecap="round"/>')

    def polygon(self, pkt, fyll="#274247"):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pkt)
        self.el.append(f'<polygon points="{p}" fill="{fyll}"/>')

    def circle(self, x, y, r, fyll="#00824d", strek="none", sb=1):
        self.el.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fyll}" stroke="{strek}" stroke-width="{sb}"/>')

    def text(self, x, y, tekst, str_=14, fyll="#274247", vekt=400, familie=F_TEKST, anker="start", tall=False):
        t = ' font-variant-numeric="tabular-nums"' if tall else ""
        self.el.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{familie}" font-size="{str_}" '
                       f'font-weight="{vekt}" fill="{fyll}" text-anchor="{anker}"{t}>{escape(tekst)}</text>')

    def tekstblokk(self, x, y, tekst, maks_bredde, str_=14, linjeh=None, **kw):
        """Skriv brutt tekst. Returnerer y for neste linje etter blokken."""
        linjeh = linjeh or round(str_ * 1.45)
        fam = "roboto" if "Roboto" in kw.get("familie", F_TEKST) else "open"
        for ln in bryt(tekst, maks_bredde, str_, kw.get("vekt", 400), fam):
            self.text(x, y, ln, str_, **kw)
            y += linjeh
        return y

    def pil(self, x1, y1, x2, y2, farge="#274247", sb=2, spiss=10):
        """Rett pil med fylt trekant som spiss (ingen SVG-markører)."""
        import math
        v = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - spiss * math.cos(v), y2 - spiss * math.sin(v)
        self.line(x1, y1, bx, by, farge, sb)
        n = spiss * 0.55
        self.polygon([(x2, y2), (bx + n * math.sin(v), by - n * math.cos(v)),
                      (bx - n * math.sin(v), by + n * math.cos(v))], farge)

    def markor(self, x, y, nr, r=15, fyll="#00824d"):
        self.circle(x, y, r, fyll)
        self.text(x, y + 5.5, str(nr), 16, "#ffffff", 700, F_OVERSKRIFT, "middle")

    def lagre(self, sti):
        with open(sti, "w", encoding="utf-8") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.b}" height="{self.h}" '
                    f'viewBox="0 0 {self.b} {self.h}">\n' + "\n".join(self.el) + "\n</svg>\n")

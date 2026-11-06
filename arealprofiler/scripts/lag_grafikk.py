"""Lager konseptgrafikk og toppgrafikkvarianter for arealprofiler (steg 2).

Bruker Svg, nb, sgn og bryt fra felles/grafikk.py. Mangler den, brukes en lokal
reserve med samme grensesnitt (samme som i folkemengde).

Kjør fra mappen arealprofiler/:  python3 scripts/lag_grafikk.py
"""
import json
import os
import sys

HER = os.path.dirname(os.path.abspath(__file__))
ROT = os.path.dirname(HER)
sys.path.insert(0, os.path.join(ROT, "..", "felles"))

try:
    from grafikk import Svg, nb, sgn, bryt  # felles/grafikk.py i repoet
except ImportError:  # reserve til felles/grafikk.py er på plass
    from xml.sax.saxutils import escape

    def nb(x, des=0):
        s = f"{abs(x):,.{des}f}".replace(",", "\u00a0").replace(".", ",")
        return ("−" if x < 0 else "") + s

    def sgn(x, des=0):
        return ("+" if x > 0 else "") + nb(x, des)

    def bryt(tekst, n):
        ord_, linjer, l = [o for o in tekst.split(" ") if o], [], ""
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

        def polyline(self, pts, stroke="#274246", sw=2, dash=None):
            d = f' stroke-dasharray="{dash}"' if dash else ""
            p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
            self.e.append(f'<polyline points="{p}" fill="none" stroke="{stroke}" stroke-width="{sw}"{d}/>')

        def circle(self, x, y, r, fill="#274246", stroke="none", sw=1):
            self.e.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

        def polygon(self, pts, fill="#274246", stroke="none", sw=1, dash=None):
            d = f' stroke-dasharray="{dash}"' if dash else ""
            p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
            self.e.append(f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

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
BG_FLATE, BG_KANT = "#f0f8f9", "#c3dcdc"
GR, GR_LYS, GR_BG = "#00824d", "#b6e8b8", "#ecfeed"
LI, LI_LYS, LI_BG, LI_TXT = "#7e5ee8", "#d2ceff", "#f2f0ff", "#4b2fb0"
GRAA, GRAA_BG = "#b9c5c6", "#f3f5f5"
STOTTE, NULL = "#d9dfe0", "#a9b5b7"
S_GRONN, S_BLA = "#00824d", "#1d9de2"        # strektoner
F_GRONN = "#339b71"                          # flatetone


D = json.load(open(os.path.join(ROT, "data", "grafikk-utkast.json"), encoding="utf-8"))
IND = json.load(open(os.path.join(ROT, "data", "indikatorer.json"), encoding="utf-8"))
EKS = D["eksempelkommune"]
ET_ = EKS["tall"]
NB = {r["aar"]: r for r in D["nye_boliger"]}
OM = {r["aar"]: r for r in D["omdisponering"]}
KILDE = "Kilde: SSB, datagrunnlaget for Arealprofiler 2025 (publisert 29.08.2025)."
TYPER = D["typer"]
SISTE = D["siste_aar"]


def pil_hoyre(s, x, y, l=14):
    s.line(x, y, x + l - 7, y, stroke=GRA, sw=1.5)
    s.polygon([(x + l - 8, y - 5), (x + l - 8, y + 5), (x + l, y)], fill=GRA)


def chip(s, x, y, w, t, fill, kant, tfarge=MORK, h=24, size=12.5, weight=400, dash=None):
    s.rect(x, y, w, h, fill=fill, stroke=kant, rx=2, dash=dash)
    s.text(x + 8, y + h / 2 + 4.5, t, size=size, fill=tfarge, weight=weight)


def nummer(s, x, y, n):
    s.circle(x, y, 13, fill=MORK)
    s.text(x, y + 5, n, size=14, fill="#ffffff", weight=700, anchor="middle")


def eks(kode, des=1):
    e = ET_[kode]
    return nb(e["verdi"], des), e["aar"]


# ---------- Konseptgrafikk: fire måter tallene lages på ----------

def t_register(s, x, y, w):
    s.rect(x, y, w, 118, fill="#ffffff", stroke=LINJE, rx=2)
    s.rect(x, y, w, 26, fill=GR_BG, stroke=GR_LYS, rx=2)
    s.text(x + 10, y + 18, "Register", size=12.5, weight=700, fill=MORK)
    s.text(x + w - 10, y + 18, "kommune", size=12, fill=GRA, anchor="end")
    for i, (t, k) in enumerate([("person, 67 år", "3405"), ("husholdning, leier", "3405"),
                                ("bolig i blokk, 2024", "3405")]):
        yy = y + 46 + i * 26
        s.text(x + 10, yy, t, size=12.5)
        s.text(x + w - 10, yy, k, size=12.5, fill=GRA, anchor="end")
        s.line(x + 8, yy + 8, x + w - 8, yy + 8, stroke=STOTTE)
    return y + 118


def t_kostra(s, x, y, w):
    s.rect(x, y, w, 118, fill="#ffffff", stroke=LINJE, rx=2)
    s.rect(x, y, 5, 118, fill=LI)
    s.text(x + 14, y + 20, "Kommunens rapport til SSB", size=12.5, weight=700, fill=LI_TXT)
    for i, (t, v) in enumerate([("Dispensasjoner, 100 m", "antall"), ("Omdisponert dyrka jord", "dekar"),
                                ("Nydyrket areal", "dekar")]):
        yy = y + 48 + i * 26
        s.text(x + 14, yy, t, size=12.5)
        s.rect(x + w - 64, yy - 14, 54, 20, fill=LI_BG, stroke=LI_LYS, rx=2)
        s.text(x + w - 37, yy + 1, v, size=12, fill=LI_TXT, anchor="middle")
    return y + 118


def t_kart(s, x, y, w):
    h = 118
    s.rect(x, y, w, h, fill="#ffffff", stroke=LINJE, rx=2)
    s.rect(x, y, 24, h, fill=BG_FLATE)
    s.rect(x + 24, y, 16, h, fill=GRAA_BG, stroke=GRAA, dash="4 3")
    s.rect(x + 60, y + 16, w - 76, 74, fill=GR_BG, stroke=GR_LYS, rx=2)
    s.text(x + 66, y + 31, "tettsted", size=12, fill=MORK)
    s.rect(x + 86, y + 40, 96, 34, fill=GR_LYS, stroke=GR, rx=2)
    s.text(x + 134, y + 61, "sentrumssone", size=12, fill=MORK, anchor="middle", weight=600)
    s.rect(x + w - 70, y + 94, 56, 18, fill="#ffffff", stroke=MORK, rx=2)
    s.text(x + w - 42, y + 107, "fare", size=12, fill=MORK, anchor="middle")
    for bx, by in [(x + 196, y + 82), (x + 74, y + 80), (x + 32, y + 60), (x + 110, y + 104), (x + w - 30, y + 30)]:
        s.rect(bx - 4, by - 4, 8, 8, fill=MORK)
    s.text(x + 12, y + h - 8, "sjø", size=12, fill=GRA, anchor="middle")
    return y + h


def t_plan(s, x, y, w):
    h = 118
    s.rect(x, y, w, h, fill="#ffffff", stroke=LINJE, rx=2)
    s.rect(x + 16, y + 30, w - 32, 66, fill=LI_BG, stroke=LI, dash="6 4", rx=2)
    s.text(x + 16, y + 20, "Planlagt boligområde", size=12, fill=LI_TXT, weight=600)
    s.rect(x + 16, y + 30, (w - 32) * 0.5, 66, fill=GR_LYS, stroke=GR, rx=2)
    s.text(x + 26, y + 68, "bygd", size=12.5, fill=MORK, weight=600)
    s.text(x + 16 + (w - 32) * 0.75, y + 60, "ledig", size=12.5, fill=LI_TXT, weight=600, anchor="middle")
    s.text(x + 16 + (w - 32) * 0.75, y + 78, "= reserve", size=12.5, fill=LI_TXT, weight=600, anchor="middle")
    s.text(x + 16, y + 112, "plan lagt over kart over faktisk arealbruk", size=12, fill=GRA)
    return y + h


KOLONNER = [
    ("register", "Telt i registrene", t_register,
     "Personer, husholdninger, boliger og bygg telles i registrene og føres til kommunen de hører til.",
     "alder, inntekt, leie, flytting, pendling, nye boliger og fritidsbygg",
     lambda: "{} % over 60 år ({})".format(*eks("A9")),
     "Folkeregisteret, Matrikkelen, inntekts- og sysselsettingsregistre"),
    ("kostra", "Rapportert av kommunen", t_kostra,
     "Kommunene rapporterer vedtak og saksbehandling til SSB gjennom KOSTRA.",
     "dispensasjoner i strandsonen, omdisponert og nydyrket jord",
     lambda: "{} dekar nydyrket ({})".format(*eks("C1", 0)),
     "KOSTRA plan og byggesak, KOSTRA landbruk"),
    ("kart", "Plassert i kartet", t_kart,
     "Bygninger og bosatte plasseres i kartet og holdes opp mot soner: tettsted, sentrum, arbeidsplassklynger, strandsone, fareområder, natur.",
     "tetthet, avstander, strandsone, fare, bebygd areal, tilgang til natur",
     lambda: "{} % av nye boliger utenfor tettsted ({})".format(*eks("A8")),
     "Matrikkelen, Folkeregisteret, SSBs arealbrukskart og soner, NVE, Kartverket"),
    ("plan", "Planen mot virkeligheten", t_plan,
     "Kommuneplanens arealdel legges over kartet. Det som er satt av, men ikke bygd, er reserven.",
     "ledig areal til bolig",
     lambda: "{} dekar ledig til bolig ({})".format(*eks("B9", 0)),
     "Kommuneplanens arealdel, SSBs arealbrukskart"),
]

N_IND = D["antall_indikatorer"]
FELLES = (f"Ett tall per kommune og år, for {N_IND} indikatorer og 357 kommuner (inndeling 2024). "
          f"{D['fireaarssummer']} indikatorer er summer for de siste fire årene, så tre av fire år går igjen fra ett år til det neste. "
          f"Siste år er {', '.join(map(str, SISTE[:-1]))} eller {SISTE[-1]}, avhengig av indikatoren.")
IKKE_MED = [
    "Grunnareal er ikke boligstørrelse: tomt og uteareal til bolig, ikke bruksarealet i boligen.",
    "En reserve er planlagt, ikke bygd. Det finnes ingen landstall i datagrunnlaget.",
    "Kommuner uten tettsted, sentrumssone eller kyst mangler noen tall. Det er ikke null.",
]
KILDE_K = (f"{KILDE} Definisjoner: forklaringstekstene i arealprofilene. "
           f"{EKS['navn']} er eksempelkommune.")


def kolonne(s, x, y, w, i, k, tegn_w=None):
    typ, tittel, tegn, tekst, gir, eksempel, kilder = k
    nummer(s, x + 13, y, str(i + 1))
    s.text(x + 34, y + 6, tittel, size=16, weight=700)
    yy = y + 24
    chip(s, x, yy, 118, f"{TYPER[typ]} indikator" + ("er" if TYPER[typ] != 1 else ""), GR_BG if typ in ("register", "kart") else LI_BG,
         GR_LYS if typ in ("register", "kart") else LI_LYS, size=12.5, weight=600)
    yy = s.lines(x, yy + 46, bryt(tekst, int(w / 6.9)), size=13, lh=18) + 4
    return yy


def kolonne_rest(s, x, yy, w, k):
    typ, tittel, tegn, tekst, gir, eksempel, kilder = k
    yy = tegn(s, x, yy, w) + 22
    s.text(x, yy, "Gir blant annet", size=12, fill=GRA, weight=600)
    yy = s.lines(x, yy + 17, bryt(gir, int(w / 6.6)), size=12.5, lh=17) + 8
    s.text(x, yy, EKS["navn"], size=12, fill=GR, weight=700)
    yy = s.lines(x, yy + 17, bryt(eksempel(), int(w / 6.6)), size=12.5, lh=17) + 8
    yy = s.lines(x, yy, bryt("Kilder: " + kilder, int(w / 6.3)), size=12, lh=16, fill=GRA)
    return yy


def konsept_bred():
    B = 1200
    s = Svg(B, 10)
    s.text(40, 46, "Slik lages tallene", size=26, weight=700)
    s.text(40, 72, f"{N_IND} indikatorer per kommune, laget på fire måter", size=15, fill=GRA)
    s.line(40, 88, 1160, 88, stroke=LINJE)
    x0, w, gap = 40, 265, 20
    ys = [kolonne(s, x0 + i * (w + gap), 120, w, i, k) for i, k in enumerate(KOLONNER)]
    ystart = max(ys)
    yend = max(kolonne_rest(s, x0 + i * (w + gap), ystart, w, k) for i, k in enumerate(KOLONNER))
    for i in range(1, 4):
        s.line(x0 + i * (w + gap) - gap / 2, 108, x0 + i * (w + gap) - gap / 2, yend, stroke=STOTTE)
    y = yend + 26
    # felles og ikke med
    fl = bryt(FELLES, 74)
    il = [bryt(t, 66) for t in IKKE_MED]
    hb = max(40 + len(fl) * 18, 40 + sum(len(l) for l in il) * 18 + 6 * (len(il) - 1)) + 10
    s.rect(40, y, 550, hb, fill=BG_FLATE, stroke=BG_KANT, rx=2)
    s.rect(40, y, 550, 5, fill=GR)
    s.text(56, y + 28, "Felles for alle", size=14, weight=700)
    s.lines(56, y + 52, fl, size=13, lh=18)
    s.rect(610, y, 550, hb, fill=GRAA_BG, stroke=GRAA, dash="6 4")
    s.text(626, y + 28, "Det tallene ikke viser", size=14, weight=700)
    yy = y + 52
    for l in il:
        yy = s.lines(626, yy, l, size=13, lh=18) + 6
    y += hb + 24
    y = s.lines(40, y, bryt(KILDE_K, 170), size=12, lh=16, fill=GRA)
    s.h = int(y + 10)
    s.save(os.path.join(ROT, "src", "konsept-bred.svg"))


def konsept_smal():
    B = 390
    s = Svg(B, 10)
    s.text(16, 36, "Slik lages tallene", size=22, weight=700)
    s.lines(16, 60, bryt(f"{N_IND} indikatorer per kommune, laget på fire måter", 44), size=14, lh=19, fill=GRA)
    s.line(16, 90, B - 16, 90, stroke=LINJE)
    y = 122
    for i, k in enumerate(KOLONNER):
        yy = kolonne(s, 16, y, 358, i, k)
        yy = kolonne_rest(s, 16, yy, 358, k)
        s.line(16, yy + 16, B - 16, yy + 16, stroke=STOTTE)
        y = yy + 52
    fl = bryt(FELLES, 48)
    s.rect(16, y - 14, B - 32, 40 + len(fl) * 18 + 6, fill=BG_FLATE, stroke=BG_KANT, rx=2)
    s.rect(16, y - 14, B - 32, 5, fill=GR)
    s.text(28, y + 12, "Felles for alle", size=14, weight=700)
    y = s.lines(28, y + 36, fl, size=13, lh=18) + 30
    il = [bryt(t, 46) for t in IKKE_MED]
    hb = 40 + sum(len(l) for l in il) * 18 + 8 * len(il)
    s.rect(16, y - 14, B - 32, hb, fill=GRAA_BG, stroke=GRAA, dash="6 4")
    s.text(28, y + 12, "Det tallene ikke viser", size=14, weight=700)
    yy = y + 36
    for l in il:
        yy = s.lines(28, yy, l, size=13, lh=18) + 8
    y = y - 14 + hb + 26
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
    s.text(40, 316, kilde, size=12, fill=GRA)
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
    s.text(x0 - 40, ytop - 14, enhet, size=12, fill=GRA)
    return ys


def topp_a():
    aar = sorted(NB)
    sist, ti = NB[aar[-1]], NB[aar[-1] - 10]
    s = topp_ramme(
        f"NYE BOLIGER · FIREÅRSPERIODER FRAM TIL {aar[-1]}",
        "1 av 10" if sist["andel_utenfor_tettsted"] < 15 else f"{nb(sist['andel_utenfor_tettsted'])} %",
        "nye boliger bygges utenfor tettsted. For ti år siden var det 1 av 5.",
        bryt(f"Av {nb(sist['nye_boliger'])} boliger igangsatt i perioden fram til {aar[-1]} lå "
             f"{nb(sist['andel_utenfor_tettsted'], 1)} prosent utenfor tettsted, mot "
             f"{nb(ti['andel_utenfor_tettsted'], 1)} prosent i perioden fram til {aar[-1] - 10}. "
             f"Halvparten er nå i blokk.", 62),
        KILDE + " Egne beregninger.",
    )
    x0, x1, ytop, ybot = 660, 1010, 70, 262
    s.text(x0 - 40, 34, "Andel av nye boliger, siste fire år", size=14, weight=600)
    ys = y_akse(s, x0, x1, ytop, ybot, 60, 10, "prosent")
    n = len(aar)
    xs = lambda i: x0 + i * (x1 - x0) / (n - 1)
    it = aar.index(aar[-1] - 10)
    for key, farge, navn in [("andel_blokk", S_BLA, "i blokk"), ("andel_utenfor_tettsted", S_GRONN, "utenfor tettsted")]:
        pts = [(xs(i), ys(NB[a][key])) for i, a in enumerate(aar)]
        s.polyline(pts, stroke=farge, sw=2.5)
        s.circle(*pts[-1], 3.5, fill=farge)
        s.circle(*pts[it], 3.5, fill=farge)
        s.text(pts[-1][0] + 8, pts[-1][1] + 4, f"{nb(sist[key], 1)} {navn}", size=12.5, fill=MORK, weight=600)
        s.text(pts[it][0], pts[it][1] - 8, nb(ti[key], 1), size=12, fill=MORK, anchor="middle")
    for i, a in enumerate(aar):
        if a in (aar[0], aar[-1]) or a % 5 == 0:
            s.text(xs(i), ybot + 18, str(a), size=12, fill=GRA, anchor="middle")
    s.text(x0 - 40, 298, "Årstallet er slutten av fireårsperioden. Kommunenes andeler er vektet med antall nye boliger.",
           size=12, fill=GRA)
    s.save(os.path.join(ROT, "docs", "grafikk", "02-topp-a.svg"))


def topp_b():
    aar = sorted(OM)
    maal, sist = D["jordvernmaal_dekar"], OM[aar[-1]]
    s = topp_ramme(
        f"JORDVERN · OMDISPONERT DYRKA JORD {aar[0]}–{aar[-1]}",
        f"{nb(round(sist['dyrka'], -2))} dekar",
        f"dyrka jord ble omdisponert i {aar[-1]}, halvparten av nivået i {aar[0]}.",
        bryt(f"Summen for kommunene er {nb(sist['dyrka'])} dekar i {aar[-1]}, mot {nb(OM[aar[0]]['dyrka'])} i {aar[0]}. "
             f"Jordvernmålet er {nb(maal)} dekar. Landstallet i kofola kan avvike fra summen.", 62),
        KILDE + " Jordvernmål: Stortinget.",
    )
    x0, x1, ytop, ybot = 660, 1070, 70, 262
    s.text(x0 - 40, 34, "Omdisponert dyrka jord, sum for kommunene", size=14, weight=600)
    ys = y_akse(s, x0, x1, ytop, ybot, 7000, 1000, "dekar")
    n = len(aar)
    slot = (x1 - x0) / n
    bw = slot * 0.66
    for i, a in enumerate(aar):
        v = OM[a]["dyrka"]
        x = x0 + i * slot + (slot - bw) / 2
        s.rect(x, ys(v), bw, ybot - ys(v), fill=S_GRONN)
        if a in (aar[0], aar[-1]) or a % 5 == 0:
            s.text(x + bw / 2, ybot + 18, str(a), size=12, fill=GRA, anchor="middle")
        if a in (aar[0], aar[-1]):
            s.text(x + bw / 2, ys(v) - 6, nb(v), size=12, fill=MORK, anchor="middle", weight=600)
    s.line(x0, ys(maal), x1, ys(maal), stroke=MORK, sw=1.2, dash="5 4")
    s.text(x1 + 8, ys(maal) - 4, "Jordvern-", size=12, fill=MORK, weight=600)
    s.text(x1 + 8, ys(maal) + 12, "målet", size=12, fill=MORK, weight=600)
    mangler = [OM[a]["kommuner"] for a in aar if a < 2020]
    if mangler and min(mangler) < 357:
        s.text(x0 - 40, 298, f"{aar[0]}–2019 mangler tall for {357 - max(mangler)}–{357 - min(mangler)} kommuner.",
               size=12, fill=GRA)
    s.save(os.path.join(ROT, "docs", "grafikk", "02-topp-b.svg"))


def topp_c():
    st = D["stripe"]
    a3 = next(r for r in st if r["kode"] == "A3")
    a8 = next(r for r in st if r["kode"] == "A8")
    s = topp_ramme(
        f"MIN KOMMUNE · {EKS['navn'].upper()}",
        EKS["navn"],
        "bor tettere enn de fleste kommuner med samme sentralitet.",
        bryt(f"{nb(a3['kommune'])} prosent bor i tettsted ({a3['aar']}), mot {nb(a3['gruppe_median'])} i midten av gruppen. "
             f"{nb(a8['kommune'], 1)} prosent av de nye boligene ligger utenfor tettsted ({a8['aar']}).", 62),
        KILDE + " Sentralitet: SSBs standard 2020 (Klass).",
    )
    x0, x1 = 640, 1100
    s.text(x0, 34, f"Mot {a3['gruppe_n']} kommuner i sentralitetsklasse {EKS['sentralitetsklasse']}", size=14, weight=600)
    ly = 52
    s.rect(x0, ly - 7, 22, 10, fill=GR_LYS)
    s.text(x0 + 28, ly + 2, "midtre 80 prosent av klassen", size=12, fill=GRA)
    s.line(x0 + 222, ly - 9, x0 + 222, ly + 5, stroke=MORK, sw=2)
    s.text(x0 + 230, ly + 2, "median", size=12, fill=GRA)
    s.polygon([(x0 + 292, ly - 2), (x0 + 297, ly - 7), (x0 + 302, ly - 2), (x0 + 297, ly + 3)], fill="#ffffff", stroke=MORK, sw=1.2)
    s.text(x0 + 308, ly + 2, "landsmedian", size=12, fill=GRA)
    s.circle(x0 + 404, ly - 2, 5, fill=S_GRONN)
    s.text(x0 + 414, ly + 2, EKS["navn"], size=12, fill=GRA)
    y = 82
    for r in st:
        vals = [r["gruppe_p10"], r["gruppe_p90"], r["kommune"], r["land_median"]]
        lo, hi = min(vals), max(vals)
        pad = (hi - lo) * 0.08 or 1
        lo, hi = max(0, lo - pad), hi + pad
        xs = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
        s.text(x0, y, f"{r['navn']} ({r['enhet']}, {r['aar']})", size=12.5, fill=MORK)
        sy = y + 14
        s.line(x0, sy, x1, sy, stroke=STOTTE)
        s.rect(xs(r["gruppe_p10"]), sy - 5, xs(r["gruppe_p90"]) - xs(r["gruppe_p10"]), 10, fill=GR_LYS)
        s.line(xs(r["gruppe_median"]), sy - 8, xs(r["gruppe_median"]), sy + 8, stroke=MORK, sw=2)
        lx = xs(r["land_median"])
        s.polygon([(lx - 5, sy), (lx, sy - 5), (lx + 5, sy), (lx, sy + 5)], fill="#ffffff", stroke=MORK, sw=1.2)
        s.circle(xs(r["kommune"]), sy, 5.5, fill=S_GRONN)
        s.text(x1 + 10, sy + 4, nb(r["kommune"], 1 if r["enhet"] == "km" or r["kommune"] % 1 else 0),
               size=12.5, fill=MORK, weight=700)
        y += 44
    s.text(x0, 298, "Hver rad har sin egen skala. Ingen retning er god eller dårlig i seg selv.", size=12, fill=GRA)
    s.save(os.path.join(ROT, "docs", "grafikk", "02-topp-c.svg"))


if __name__ == "__main__":
    os.makedirs(os.path.join(ROT, "src"), exist_ok=True)
    os.makedirs(os.path.join(ROT, "docs", "grafikk"), exist_ok=True)
    konsept_bred()
    konsept_smal()
    topp_a()
    topp_b()
    topp_c()
    print("ok")

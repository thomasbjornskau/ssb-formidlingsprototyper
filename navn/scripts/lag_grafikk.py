"""Lager konseptgrafikken og toppgrafikkvariantene for navn (steg 2).

Leser data/grafikk-utkast.json. Skriver src/konsept-bred.svg, src/konsept-smal.svg
og docs/grafikk/02-topp-{a,b,c}.svg.
SVG-primitivene ligger i scripts/grafikk_navn.py, som i lonnansatt.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from grafikk_navn import Svg, nb, bryt  # noqa: E402

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROT, "data", "grafikk-utkast.json"), encoding="utf-8"))

MORK, GRA, LINJE = "#274246", "#5e787a", "#cdd3d4"
BG_FILL, BG_STREK = "#eff8fa", "#c4dddb"
GRONN, GRONN_FLATE = "#00824d", "#339b71"
GRID, NULL = "#d9dfe0", "#a9b5b7"
UTENFOR_FILL, UTENFOR_STREK = "#f3f5f5", "#b9c5c6"
DATO = D["sist_oppdatert"]

# ---------------------------------------------------------------- konsept
k = D["konsept"]
TRINN = [
    ("Barnet får navn",
     "Foreldrene melder navnet til Folkeregisteret. Fra 2021 telles barnet i året det fikk navn, før det i året det ble født."),
    ("Kopi per 1. januar",
     "SSB bruker en kopi av Folkeregisteret per 1. januar hvert år. Alle folkeregistrerte personer er med."),
    ("Skrivemåter ryddes",
     "Tegn utenfor det norske alfabetet slås sammen: É blir E, Ö blir Ø. Topplisten slår i tillegg sammen stavemåter:"),
    ("To ulike tall",
     "Samme navn gir to svar. Populært: hvor mange nyfødte fikk det. Vanlig: hvor mange som heter det."),
]
IKKE_MED = ("Ikke med: navn brukt av færre enn 200 personer er ikke i statistikkbanken, men navnesøket på ssb.no viser navn med flere enn tre bærere. Før 1945 finnes bare andeler, "
            "og før 1964 er tellingen ikke fullstendig. Betydning og opprinnelse er ikke en del av statistikken.")
KILDE_K = f"Kilde: SSB, navnestatistikken, tabell 10467 og 10501. Sist oppdatert: {DATO}."


def tall_trinn3(s, x, y):
    s.text(x, y, f"Lucas {nb(k['lucas'])} + Lukas {nb(k['lukas'])}", size=15, fill=MORK, weight=600)
    s.text(x, y + 22, f"= {nb(k['lucas'] + k['lukas'])} i topplisten", size=15, fill=GRONN, weight=700)
    return y + 22


def tall_trinn4(s, x, y):
    s.text(x, y, "Anne, 2025", size=13, fill=GRA)
    s.text(x, y + 26, nb(k["anne_nyfodte_2025"]), size=24, fill=GRONN, weight=700)
    s.text(x + 96, y + 26, "nyfødte fikk navnet", size=13, fill=MORK)
    s.text(x, y + 56, nb(k["anne_personer_2025"]), size=24, fill=GRONN, weight=700)
    s.text(x + 96, y + 56, "personer heter det", size=13, fill=MORK)
    return y + 56


EKSTRA = {2: (tall_trinn3, 50), 3: (tall_trinn4, 66)}


def boks(s, x, y, w, i, tekst_bredde):
    tittel, tekst = TRINN[i]
    linjer = bryt(tekst, tekst_bredde)
    h = 62 + len(linjer) * 14 * 1.45 + (EKSTRA[i][1] + 12 if i in EKSTRA else 0) + 10
    return linjer, h


def tegn_boks(s, x, y, w, h, i, linjer):
    s.rect(x, y, w, h, fill=BG_FILL, stroke=BG_STREK, sw=1)
    s.markor(x + 26, y + 28, i + 1)
    s.text(x + 50, y + 34, TRINN[i][0], size=17, fill=MORK, weight=700)
    ny = s.tekstblokk(x + 18, y + 66, linjer, size=14, lh=1.45, fill=MORK)
    if i in EKSTRA:
        EKSTRA[i][0](s, x + 18, ny + 8)


def konsept_bred():
    W, H = 1200, 480
    s = Svg(W, H, "Slik lages navnestatistikken")
    s.text(40, 44, "Slik lages tallene", size=24, weight=700, fill=MORK)
    s.text(40, 72, "Fra navnet blir registrert til det står i statistikken", size=15, fill=GRA)
    bw, gap, x0, y0 = 248, 36, 40, 98
    data = [boks(s, 0, 0, bw, i, 30) for i in range(4)]
    h = max(d[1] for d in data)
    for i, (linjer, _) in enumerate(data):
        x = x0 + i * (bw + gap)
        tegn_boks(s, x, y0, bw, h, i, linjer)
        if i < 3:
            s.pil(x + bw + 6, y0 + h / 2, x + bw + gap - 6, y0 + h / 2)
    yb = y0 + h + 24
    il = bryt(IKKE_MED, 150)
    bh = 26 + len(il) * 20
    s.rect(x0, yb, 4 * bw + 3 * gap, bh, fill=UTENFOR_FILL, stroke=UTENFOR_STREK, sw=1.2, dash="6 4")
    s.tekstblokk(x0 + 18, yb + 26, il, size=14, lh=1.43, fill=GRA)
    s.text(x0, yb + bh + 30, KILDE_K, size=12, fill=GRA)
    s.h = int(yb + bh + 44)
    s.lagre(os.path.join(ROT, "src", "konsept-bred.svg"))


def konsept_smal():
    W = 390
    s = Svg(W, 100, "Slik lages navnestatistikken")
    s.text(20, 36, "Slik lages tallene", size=22, weight=700, fill=MORK)
    s.tekstblokk(20, 62, bryt("Fra navnet blir registrert til det står i statistikken", 44), size=14, fill=GRA)
    y, bw = 104, 350
    for i in range(4):
        linjer, h = boks(s, 0, 0, bw, i, 42)
        tegn_boks(s, 20, y, bw, h, i, linjer)
        y += h
        if i < 3:
            s.pil(W / 2, y + 4, W / 2, y + 26)
            y += 30
    y += 20
    il = bryt(IKKE_MED, 44)
    bh = 24 + len(il) * 20
    s.rect(20, y, bw, bh, fill=UTENFOR_FILL, stroke=UTENFOR_STREK, sw=1.2, dash="6 4")
    s.tekstblokk(36, y + 24, il, size=14, lh=1.43, fill=GRA)
    y += bh + 28
    y = s.tekstblokk(20, y, bryt(KILDE_K, 56), size=12, fill=GRA)
    s.h = int(y + 10)
    s.lagre(os.path.join(ROT, "src", "konsept-smal.svg"))


# ---------------------------------------------------------------- toppgrafikk
TW, TH = 1200, 330
FX0, FX1, FY0, FY1 = 640, 1150, 64, 270  # figurflate


def ramme_topp(tittel, etikett, stort, setning, linjer, kilde):
    s = Svg(TW, TH, tittel)
    s.text(40, 48, etikett.upper(), size=13, fill=GRA, weight=600)
    s.text(40, 128, stort, size=64, fill=GRONN, weight=700)
    y = s.tekstblokk(40, 172, bryt(setning, 52), size=20, lh=1.35, fill=MORK, weight=600)
    s.tekstblokk(40, y + 10, bryt(linjer, 70), size=15, lh=1.45, fill=GRA)
    s.text(40, TH - 16, kilde, size=12, fill=GRA)
    return s


def topp_a():
    a = D["A_anna_andel"]
    v, x0 = a["verdier"], a["aar_fra"]
    s = ramme_topp("Toppgrafikk A: navnebølgen", "Navn · nyfødte · 1880–2025", "9 av 100",
                   "jenter fikk navnet Anna i 1881. I 2025 var det under 1 av 100.",
                   "Velg et navn og se bølgen. Tall før 1964 er mindre presise, og før 1945 finnes bare andeler.",
                   f"Kilde: SSB, tabell 10467. Sist oppdatert: {DATO}.")
    ymax = 10
    X = lambda aar: FX0 + (aar - 1880) / (2025 - 1880) * (FX1 - FX0)
    Y = lambda p: FY1 - p / ymax * (FY1 - FY0)
    s.text(FX0, FY0 - 22, "Andel av fødte jenter, prosent", size=13, fill=GRA)
    for p in range(0, 11, 2):
        s.line(FX0, Y(p), FX1, Y(p), stroke=NULL if p == 0 else GRID)
        s.text(FX0 - 8, Y(p) + 4, nb(p), size=12, fill=GRA, anchor="end")
    for aar in (1880, 1920, 1960, 2000, 2025):
        s.text(X(aar), FY1 + 20, str(aar), size=12, fill=GRA, anchor="middle")
    for aar, tekst in ((1945, "Antall fra 1945"), (1964, "Full telling fra 1964")):
        s.line(X(aar), FY0 + 4, X(aar), FY1, stroke=NULL, dash="4 4")
    s.text(X(1945) - 6, FY0 + 14, "Antall fra 1945", size=12, fill=GRA, anchor="end")
    s.text(X(1964) + 6, FY0 + 14, "Full telling fra 1964", size=12, fill=GRA)
    s.polyline([(X(x0 + i), Y(p)) for i, p in enumerate(v)], stroke=GRONN, sw=2.5)
    s.circle(X(1881), Y(v[1]), 4, fill=GRONN)
    s.text(X(1881) + 9, Y(v[1]) + 4, f"{nb(v[1], 1)} (1881)", size=13, fill=MORK, weight=600)
    s.circle(X(1957), Y(v[77]), 3.5, fill=GRONN)
    s.text(X(1957), Y(v[77]) - 12, f"{nb(v[77], 1)} (1957)", size=12, fill=MORK, anchor="middle")
    s.circle(X(2025), Y(v[-1]), 4, fill=GRONN)
    s.text(X(2025), Y(v[-1]) - 12, f"{nb(v[-1], 1)}", size=13, fill=MORK, weight=600, anchor="middle")
    s.lagre(os.path.join(ROT, "docs", "grafikk", "02-topp-a.svg"))


def topp_b():
    b = D["B_populaert_vanlig"]
    s = ramme_topp("Toppgrafikk B: populært eller vanlig", "Navn · 2025", "55 600",
                   f"heter Anne. Bare {b['nyfodte_2025']['Anne']} jenter fikk navnet i 2025.",
                   "Populært og vanlig er to ulike tall: hvor mange nyfødte som fikk navnet, og hvor mange som heter det.",
                   f"Kilde: SSB, tabell 10467 og 10501. Sist oppdatert: {DATO}.")
    navn = ["Emma", "Anne"]
    farge = {"Anne": GRONN, "Emma": UTENFOR_STREK}
    paneler = [("Nyfødte som fikk navnet", b["nyfodte_2025"], FX0 + 40, FX0 + 230),
               ("Personer som heter navnet", b["personer_2025"], FX0 + 320, FX1 - 20)]
    for tittel, verdier, x0, x1 in paneler:
        s.text(x0 - 40, FY0 + 6, tittel, size=13, fill=GRA, weight=600)
        mx = max(verdier.values())
        bh, gap = 38, 26
        for i, n in enumerate(navn):
            y = FY0 + 40 + i * (bh + gap)
            w = verdier[n] / mx * (x1 - x0 - 70)
            s.text(x0 - 8, y + bh / 2 + 5, n, size=14, fill=MORK, anchor="end", weight=600 if n == "Anne" else 400)
            s.rect(x0, y, w, bh, fill=farge[n])
            s.text(x0 + w + 8, y + bh / 2 + 5, nb(verdier[n]), size=14, fill=MORK, weight=600 if n == "Anne" else 400)
        s.line(x0, FY0 + 30, x0, FY0 + 40 + 2 * bh + gap + 10, stroke=NULL)
    s.text(FX0, FY1 + 12, "Hvert panel har egen skala.", size=12, fill=GRA)
    s.lagre(os.path.join(ROT, "docs", "grafikk", "02-topp-b.svg"))


def topp_c():
    c = D["C_skrivemaater"]
    s = ramme_topp("Toppgrafikk C: skrivemåtene", "Guttenavn · 2025", "411",
                   "gutter fikk navnet Lucas i 2025. Men bare 225 av dem skrives Lucas.",
                   "Topplisten slår sammen skrivemåter. I statistikkbanken står hver skrivemåte for seg.",
                   f"Kilde: SSB, artikkelen «Guttenavn» og tabell 10467. Sist oppdatert: {DATO}.")
    x0, x1 = FX0 + 60, FX1 - 50
    mx = 500
    s.text(x0, FY0 - 22, "Antall nyfødte gutter, topp 5", size=13, fill=GRA)
    s.rect(x0 + 205, FY0 - 34, 12, 12, fill=GRONN_FLATE)
    s.text(x0 + 222, FY0 - 23, "vanligste skrivemåte", size=12, fill=GRA)
    s.rect(x0 + 352, FY0 - 34, 12, 12, fill="#d5a640")
    s.text(x0 + 369, FY0 - 23, "andre skrivemåter", size=12, fill=GRA)
    bh, gap = 28, 13
    for i, (navn, deler, tot) in enumerate(c["rader"]):
        y = FY0 + i * (bh + gap)
        uth = navn == "Lucas"
        s.text(x0 - 10, y + bh / 2 + 5, navn, size=14, fill=MORK, anchor="end", weight=700 if uth else 400)
        xx = x0
        for j, (sk, n) in enumerate(deler):
            w = n / mx * (x1 - x0)
            s.rect(xx, y, w, bh, fill=GRONN_FLATE if j == 0 else "#d5a640")
            if uth or w > 60:
                s.text(xx + 6, y + bh / 2 + 5, f"{sk} {nb(n)}" if uth else nb(n), size=12,
                       fill="#ffffff" if j == 0 else MORK, weight=600)
            xx += w
        s.text(xx + 8, y + bh / 2 + 5, nb(tot), size=14, fill=MORK, weight=700 if uth else 400)
    s.line(x0, FY0 - 6, x0, FY0 + 5 * (bh + gap) - gap + 6, stroke=NULL)
    s.lagre(os.path.join(ROT, "docs", "grafikk", "02-topp-c.svg"))


if __name__ == "__main__":
    konsept_bred()
    konsept_smal()
    topp_a()
    topp_b()
    topp_c()
    print("ok")

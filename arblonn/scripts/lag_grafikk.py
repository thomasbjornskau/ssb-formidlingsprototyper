"""Lager konseptgrafikken og toppgrafikkutkastene for arblonn (steg 2).

Tall fra data/grafikk-utkast.json (hentet 30.10.2026).
"""
import json
import os
import sys

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROT, "scripts"))
from grafikk_arblonn import (  # noqa: E402
    Svg, nb, sgn, bryt, MORK, BLEKK, GRA_TEKST, LINJE, BG_FLATE, BG_KANT,
    GRONN, GRONN_BG, GRA, GRA_BG, STOTTE, NULL,
)

D = json.load(open(os.path.join(ROT, "data", "grafikk-utkast.json"), encoding="utf-8"))
K = D["kvartal_2026K2"]
M = D["mnd_jobber_sesongjustert"]
SEP_F = M["forelopige"][-1]
AUG_F = M["forelopige"][-2]
AUG_E = M["endelige"][-2]

ETIKETT = "ANTALL ARBEIDSFORHOLD OG LØNN"

# ---------- Konseptgrafikk ----------
TRINN = [
    ("Arbeidsgiveren melder",
     "Hver måned sender alle arbeidsgivere a-melding med arbeidsforhold, lønn og stillingsprosent.",
     "Fulltelling, ikke utvalg"),
    ("SSB teller aktive jobber",
     "En jobb telles når det er lønn eller ytelse i uka med den 16. i måneden.",
     "Sesongjobb uten lønn den uka faller ut"),
    ("Jobber blir lønnstakere",
     "Hver person telles én gang, med én hovedjobb.",
     f"{nb(K['jobber'])} jobber, {nb(K['lonnstakere'])} lønnstakere"),
    ("Lønna regnes om til heltid",
     "Avtalt månedslønn og månedslønn regnes per heltidsekvivalent. Kontantlønn regnes per jobb.",
     f"{nb(K['avtalt_mndlonn_snitt'])} kr i avtalt månedslønn"),
    ("Først foreløpig, så endelig",
     "Første tall kommer 3–4 uker etter måneden. Endelige tall kommer en måned senere, med forsinkede meldinger og rettinger.",
     f"August 2026, sesongjustert: endelig tall {nb(AUG_E - AUG_F)} jobber høyere"),
]
IKKE_MED = ("Ikke med: selvstendig næringsdrivende · frilansere og oppdragstakere uten lønn "
            "i uka · småbeløp under fritaksgrensene i a-ordningen")
KILDE_K = ("Kilde: SSB, Om statistikken for Antall arbeidsforhold og lønn; "
           "tabell 11652 (2. kvartal 2026) og 13126 (sesongjustert).")


def konsept_bred(sti):
    B = 1200
    n = len(TRINN)
    gap = 28
    bredde = (B - 80 - gap * (n - 1)) / n
    y0 = 122

    def maal(overskrift, tekst, tall):
        o, t, z = bryt(overskrift, 15), bryt(tekst, 23), bryt(tall, 24)
        topp = max(27 + len(o) * 20, 62) + 10           # overskrift og markør
        midt = len(t) * 19 + 12                          # brødtekst
        bunn = 18 + len(z) * 17 + 10                     # tallfelt og marg
        return o, t, z, topp, midt, bunn

    m = [maal(*tr) for tr in TRINN]
    hboks = max(topp + midt + bunn for *_, topp, midt, bunn in m)
    H = y0 + hboks + 22 + 40 + 38
    s = Svg(B, H, "Slik lages tallene")
    s.tekst(40, 50, "Slik lages tallene", 28, MORK, 700)
    s.tekst(40, 80, "Fra a-meldingen til tallene i statistikken", 17, GRA_TEKST)
    s.linje(40, 96, B - 40, 96, LINJE)
    for i, (o, t, z, topp, midt, bunn) in enumerate(m):
        x = 40 + i * (bredde + gap)
        s.rect(x, y0, bredde, hboks, BG_FLATE, BG_KANT)
        s.markor(x + 26, y0 + 30, str(i + 1))
        s.tekstlinjer(x + 50, y0 + 27, o, 16, BLEKK, 700, lh=20)
        s.tekstlinjer(x + 14, y0 + topp, t, 14, MORK, lh=19)
        th = 18 + len(z) * 17
        ty = y0 + hboks - th - 10
        s.rect(x + 10, ty, bredde - 20, th, GRONN_BG, GRONN)
        s.tekstlinjer(x + 18, ty + 20, z, 13, GRONN, 700, lh=17)
        if i < n - 1:
            s.pil(x + bredde + 3, y0 + hboks / 2, x + bredde + gap - 3, y0 + hboks / 2, GRA_TEKST, 2, 9)
    yb = y0 + hboks + 22
    s.rect(40, yb, B - 80, 40, GRA_BG, GRA, 1.2, stiplet=True)
    s.tekst(56, yb + 26, IKKE_MED, 14, GRA_TEKST)
    s.tekst(40, H - 16, KILDE_K, 12, GRA_TEKST)
    s.lagre(sti)


def konsept_smal(sti):
    B = 390
    blokker = []
    for overskrift, tekst, tall in TRINN:
        blokker.append((bryt(overskrift, 30), bryt(tekst, 38), bryt(tall, 36)))
    hoyde = lambda o, t, z: 32 + len(o) * 21 + 4 + len(t) * 19 + 6 + len(z) * 17
    H = 110
    for o, t, z in blokker:
        H += hoyde(o, t, z) + 28
    ikke = bryt(IKKE_MED, 46)
    kilde = bryt(KILDE_K, 58)
    H += len(ikke) * 18 + 30 + len(kilde) * 15 + 20
    s = Svg(B, H, "Slik lages tallene")
    s.tekst(16, 38, "Slik lages tallene", 24, MORK, 700)
    s.tekst(16, 64, "Fra a-meldingen til tallene", 15, GRA_TEKST)
    s.linje(16, 78, B - 16, 78, LINJE)
    y = 96
    for i, (o, t, z) in enumerate(blokker):
        hb = hoyde(o, t, z)
        s.rect(16, y, B - 32, hb, BG_FLATE, BG_KANT)
        s.markor(40, y + 26, str(i + 1))
        yy = s.tekstlinjer(66, y + 32, o, 16, BLEKK, 700, lh=21)
        yy = s.tekstlinjer(66, yy + 4, t, 14, MORK, lh=19)
        s.tekstlinjer(66, yy + 6, z, 13, GRONN, 700, lh=17)
        y += hb
        if i < len(blokker) - 1:
            s.pil(B / 2, y + 3, B / 2, y + 25, GRA_TEKST, 2, 9)
        y += 28
    hi = len(ikke) * 18 + 16
    s.rect(16, y - 8, B - 32, hi, GRA_BG, GRA, 1.2, stiplet=True)
    s.tekstlinjer(28, y + 12, ikke, 13, GRA_TEKST, lh=18)
    y += hi + 14
    s.tekstlinjer(16, y, kilde, 11, GRA_TEKST, lh=15)
    s.lagre(sti)


# ---------- Toppgrafikk ----------
def topp_ramme(tittel, periode, stort, setning, linjer, kilde, str_stort=60):
    s = Svg(1200, 330, tittel)
    s.tekst(40, 42, f"{ETIKETT} · {periode}", 13, GRA_TEKST, 700)
    s.tekst(40, 112, stort, str_stort, MORK, 700)
    s.tekst(40, 150, setning, 20, MORK)
    y = 186
    for l in linjer:
        y = s.tekstlinjer(40, y, bryt(l, 62), 15, GRA_TEKST, lh=21) + 4
    s.tekst(40, 312, kilde, 12, GRA_TEKST)
    return s


def stolper(s, x0, y0, bredde, rader, maks, ticks, aksetekst, tickfmt):
    """Liggende stolper fra null. rader = [(navn, verdi, etikett)]."""
    lab_b = 190
    xa = x0 + lab_b
    plot_b = bredde - lab_b - 110
    h_st, luft = 34, 17
    s.tekst(xa, y0 - 14, aksetekst, 13, GRA_TEKST)
    ybunn = y0 + len(rader) * (h_st + luft)
    for t in ticks:
        x = xa + plot_b * t / maks
        s.linje(x, y0 - 4, x, ybunn - luft + 6, STOTTE)
        s.tekst(x, ybunn + 8, tickfmt(t), 12, GRA_TEKST, anker="middle")
    for i, (navn, v, etikett) in enumerate(rader):
        y = y0 + i * (h_st + luft)
        s.rect(xa, y, plot_b * v / maks, h_st, GRONN)
        nl = bryt(navn, 22)
        s.tekstlinjer(xa - 10, y + h_st / 2 + 5 - (len(nl) - 1) * 9, nl, 14, MORK, anker="end", lh=18)
        s.tekst(xa + plot_b * v / maks + 8, y + h_st / 2 + 5, etikett, 14, MORK, 700)
    s.linje(xa, y0 - 4, xa, ybunn - luft + 6, NULL, 1.2)


def topp_a(sti):
    s = topp_ramme(
        "Toppgrafikk A: jobber og mennesker", "2. KVARTAL 2026",
        "3,2 millioner jobber",
        "men 2,8 millioner mennesker har dem.",
        ["En person kan ha flere jobber. Lønnstakere telles én gang, med hovedjobben.",
         "Regnet om til heltid blir jobbene 2,5 millioner månedsverk."],
        "Kilde: SSB, tabell 11652. Sist oppdatert: 13.08.2026.", 54)
    rader = [("Jobber", K["jobber"], nb(K["jobber"])),
             ("Lønnstakere (personer)", K["lonnstakere"], nb(K["lonnstakere"])),
             ("Heltidsekvivalenter", K["heltidsekvivalenter"], nb(K["heltidsekvivalenter"]))]
    stolper(s, 600, 74, 600, rader, 3_500_000, [0, 1e6, 2e6, 3e6], "antall, millioner",
            lambda t: nb(t / 1e6))
    s.lagre(sti)


def topp_b(sti):
    s = topp_ramme(
        "Toppgrafikk B: hvilken lønn", "2. KVARTAL 2026",
        "59 000 kroner",
        "er om lag snittet for avtalt månedslønn, før skatt.",
        ["Halvparten ligger under 53 650 kroner (median). Med bonus og uregelmessige tillegg blir snittet 63 700 kroner.",
         "Alle tallene er regnet om til heltid."],
        "Kilde: SSB, tabell 11652. Sist oppdatert: 13.08.2026.")
    rader = [("Median avtalt månedslønn", K["avtalt_mndlonn_median"], f"{nb(K['avtalt_mndlonn_median'])} kr"),
             ("Snitt avtalt månedslønn", K["avtalt_mndlonn_snitt"], f"{nb(K['avtalt_mndlonn_snitt'])} kr"),
             ("Snitt månedslønn (med bonus og tillegg)", K["mndlonn_snitt"], f"{nb(K['mndlonn_snitt'])} kr")]
    stolper(s, 600, 74, 600, rader, 75_000, [0, 20_000, 40_000, 60_000], "kroner per måned, heltid",
            lambda t: nb(t))
    s.lagre(sti)


def topp_c(sti):
    s = topp_ramme(
        "Toppgrafikk C: flere eller færre jobber nå", "SEPTEMBER 2026",
        f"{sgn(round((SEP_F - AUG_F) / 100) * 100)} jobber",
        "fra august til september, sesongjustert.",
        ["Tallet er foreløpig. Endelige tall ligger høyere og kommer en måned senere.",
         "Sammenlign derfor aldri et foreløpig tall med et endelig."],
        "Kilde: SSB, tabell 13126. Sist oppdatert: 22.10.2026.")
    x0, x1, y0, y1 = 670, 1080, 74, 262
    vmin, vmax = 3_040_000, 3_200_000
    n = len(M["maned"])
    fx = lambda i: x0 + (x1 - x0) * i / (n - 1)
    fy = lambda v: y1 - (y1 - y0) * (v - vmin) / (vmax - vmin)
    s.tekst(x0 - 60, y0 - 14, "jobber, millioner, sesongjustert", 13, GRA_TEKST)
    for v in (3_050_000, 3_100_000, 3_150_000, 3_200_000):
        s.linje(x0, fy(v), x1, fy(v), STOTTE)
        s.tekst(x0 - 8, fy(v) + 4, nb(v / 1e6, 2), 12, GRA_TEKST, anker="end")
    for i, mnd in enumerate(M["maned"]):
        if mnd.endswith("M01"):
            s.linje(fx(i), y0, fx(i), y1, STOTTE)
            s.tekst(fx(i), y1 + 18, mnd[:4], 12, GRA_TEKST, anker="middle")
    end = [(fx(i), fy(v)) for i, v in enumerate(M["endelige"]) if v is not None]
    fore = [(fx(i), fy(v)) for i, v in enumerate(M["forelopige"])]
    s.polyline(fore, "#1d9de2", 2, stiplet=True)
    s.polyline(end, GRONN, 2.5)
    s.sirkel(*end[-1], 4, GRONN)
    s.sirkel(*fore[-2], 4, "#1d9de2")
    s.sirkel(*fore[-1], 5, "#1d9de2")
    # direkte merking
    s.tekst(x1 + 10, end[-1][1] - 4, "Endelige", 13, MORK, 700)
    s.tekst(x1 + 10, end[-1][1] + 12, f"aug.: {nb(AUG_E / 1e6, 2)} mill.", 12, MORK)
    s.tekst(x1 + 10, fore[-1][1] + 6, "Foreløpige", 13, MORK, 700)
    s.tekst(x1 + 10, fore[-1][1] + 22, f"sep.: {nb(SEP_F / 1e6, 2)} mill.", 12, MORK)
    # avstand i august
    xa = fore[-2][0] - 14
    s.linje(xa, end[-1][1] + 5, xa, fore[-2][1] - 5, GRA_TEKST, 1)
    s.tekst(xa - 6, (end[-1][1] + fore[-2][1]) / 2 + 4, f"{nb(AUG_E - AUG_F)}", 12, GRA_TEKST, 700, "end")
    s.lagre(sti)


if __name__ == "__main__":
    konsept_bred(os.path.join(ROT, "src", "konsept-bred.svg"))
    konsept_smal(os.path.join(ROT, "src", "konsept-smal.svg"))
    topp_a(os.path.join(ROT, "docs", "grafikk", "02-topp-a.svg"))
    topp_b(os.path.join(ROT, "docs", "grafikk", "02-topp-b.svg"))
    topp_c(os.path.join(ROT, "docs", "grafikk", "02-topp-c.svg"))
    print("ferdig")

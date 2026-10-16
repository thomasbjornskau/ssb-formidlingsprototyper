"""Lager konseptgrafikk og toppgrafikkvarianter for lonnansatt (steg 2).

Leser data/grafikk-utkast.json. Skriver
  src/konsept-bred.svg, src/konsept-smal.svg
  docs/grafikk/02-topp-a.svg, -b.svg, -c.svg
Bare Pythons standardbibliotek og scripts/grafikk_lonn.py.
"""

import json
import sys
from pathlib import Path

ROT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from grafikk_lonn import (Svg, nb, bryt, MORK, GRA_TEKST, BLAGRONN_LYS, BLAGRONN,  # noqa: E402
                          GRONN, GRONN_LYS, GRA, GRA_LYS, STOTTELINJE, NULLINJE, KAT)

D = json.loads((ROT / "data" / "grafikk-utkast.json").read_text(encoding="utf-8"))
M = D["manedslonn_2025"]
DES = D["desiler_2025"]
Y = D["yrker_2025"]
V = D["vekst_2025"]
DATO = D["tabelldatoer"]

GRONN_STREK, GRONN_FLATE = KAT[0]
BLA_STREK, BLA_FLATE = KAT[1]
OKER_STREK, OKER_FLATE = KAT[2]
NBSP = " "


def kr(x):
    return nb(x) + NBSP + "kr"


# ---------------------------------------------------------------- konsept

def kort_innhold():
    """De fire trinnene. Kilde i kommentar (merkene viser til 01-innsikt.md)."""
    return [
        {   # [K2]
            "tittel": "Arbeidsgiveren rapporterer",
            "blokker": [
                ("tekst", "Alle som betaler lønn, sender hver måned en a-melding til Skatteetaten: lønn, stillingsprosent og yrke for hver jobb."),
                ("merknad", "Fulltelling, ikke utvalg. Alle jobber med lønn i a-meldingen er med."),
            ],
        },
        {   # [K2][K6]
            "tittel": "Én uke i november",
            "blokker": [
                ("tekst", "SSB tar med jobbene som er aktive i uka med den 16. november, og som har fått lønn den måneden. Én person kan ha flere jobber."),
                ("regnestykke", {
                    "overskrift": "November 2025",
                    "rader": [
                        ("Jobber med lønn", nb(M["jobber_med_lonn"]), False),
                        ("Regnet om til heltid", nb(M["heltidsekvivalenter"]), False),
                    ],
                }),
            ],
        },
        {   # [K2][K6]
            "tittel": "Lønna regnes om til heltid",
            "blokker": [
                ("tekst", "Deltidslønn regnes om til hva den ville vært i full stilling. Tillegg og bonus fordeles som snitt per måned fra januar til november."),
                ("regnestykke", {
                    "overskrift": "Snitt november 2025, kr",
                    "rader": [
                        ("Avtalt månedslønn", nb(M["avtalt"]), False),
                        ("+ Uregelmessige tillegg", nb(M["uregelmessige_tillegg"]), False),
                        ("+ Bonus", nb(M["bonus"]), False),
                        ("= Månedslønn", nb(M["gjennomsnitt"]), True),
                    ],
                }),
            ],
        },
        {   # [K2][K10]
            "tittel": "Koblet, sikret og publisert",
            "blokker": [
                ("tekst", "Yrkeskoden gjøres om til STYRK-08. Næring, sektor, kjønn, alder og utdanning hentes fra registre. Grupper med under 100 jobber vises ikke."),
                ("merknad", "Publiseres i februar. Årslønn er foreløpig til mars: veksten i påløpt årslønn 2025 ble først publisert som 5,0 prosent og er nå 4,9."),
            ],
        },
    ]


def tegn_kort(s, x, y, b, kort, nr, tegn=True, tegn_per_linje=27):
    """Tegner ett trinn. Returnerer høyden innholdet trenger."""
    pad = 18
    iy = y + 26
    if tegn:
        s.markor(x + pad + 14, iy, nr, r=14)
    tl = bryt(kort["tittel"], max(14, tegn_per_linje - 8))
    ty = iy + 6
    if tegn:
        s.tekstblokk(x + pad + 38, ty, tl, size=18, linjeavstand=23, weight=700, fill=MORK)
    cy = ty + (len(tl) - 1) * 23 + 30
    for typ, innhold in kort["blokker"]:
        if typ == "tekst":
            linjer = bryt(innhold, tegn_per_linje)
            if tegn:
                s.tekstblokk(x + pad, cy, linjer, size=15, linjeavstand=21, fill=MORK)
            cy += len(linjer) * 21 + 10
        elif typ == "merknad":
            linjer = bryt(innhold, tegn_per_linje - 2)
            bh = len(linjer) * 19 + 16
            if tegn:
                s.rect(x + pad, cy - 6, b - 2 * pad, bh, fill=GRA_LYS)
                s.tekstblokk(x + pad + 10, cy + 12, linjer, size=14, linjeavstand=19, fill=GRA_TEKST)
            cy += bh + 10
        elif typ == "regnestykke":
            rader = innhold["rader"]
            bh = 32 + len(rader) * 22 + 12
            if tegn:
                bx, bw = x + pad, b - 2 * pad
                s.rect(bx, cy - 6, bw, bh, fill=GRONN_LYS)
                s.text(bx + 10, cy + 12, innhold["overskrift"], size=13, fill=GRA_TEKST, weight=600)
                ry = cy + 38
                for tekst, verdi, sum_ in rader:
                    if sum_:
                        s.line(bx + 10, ry - 16, bx + bw - 10, ry - 16, stroke=GRONN, sw=1)
                    vekt = 700 if sum_ else 400
                    farge = GRONN if sum_ else MORK
                    s.text(bx + 10, ry, tekst, size=14, fill=farge, weight=vekt)
                    s.text(bx + bw - 10, ry, verdi, size=14, fill=farge, weight=vekt, anchor="end")
                    ry += 22
            cy += bh + 10
    return cy - y + 8


IKKE_MED = ("Ikke med i månedslønna", [
    "Overtid (publiseres for seg, per jobb)",
    "Naturalytelser og forsikringer",
    "Feriepenger og sluttvederlag",
    "Styrehonorar og honorarer for utvalg",
    "Skatt: alle tall er før skatt",
    "Selvstendig næringsdrivende",
])

KILDE_KONSEPT = (f"Kilde: SSB, Om statistikken (oppdatert 30.09.2026), tabell 11419 og 14858. "
                 f"Sist oppdatert: {DATO['11419']} og {DATO['14858']}.")
UNDERTITTEL = "Lønnsstatistikken: fra lønnsslippen til publisert tall"


def konsept_bred():
    B = 1200
    marg, mellom = 36, 34
    kb = (B - 2 * marg - 3 * mellom) / 4
    kort = kort_innhold()
    dummy = Svg(B, 10)
    h = max(tegn_kort(dummy, 0, 0, kb, k, i + 1, tegn=False) for i, k in enumerate(kort))
    ky = 96
    ikke_y = ky + h + 28
    ikke_h = 58 + 3 * 24
    H = ikke_y + ikke_h + 40
    s = Svg(B, H, tittel="Slik lages tallene",
            beskrivelse="Fire trinn fra arbeidsgiverens a-melding til publisert månedslønn, og hva som ikke er med i månedslønna.")
    s.text(marg, 44, "Slik lages tallene", size=26, weight=700, fill=MORK)
    s.text(marg, 72, UNDERTITTEL, size=16, fill=GRA_TEKST)
    for i, k in enumerate(kort):
        x = marg + i * (kb + mellom)
        s.rect(x, ky, kb, h, fill=BLAGRONN_LYS, stroke=BLAGRONN, sw=1)
        tegn_kort(s, x, ky, kb, k, i + 1)
        if i < 3:
            s.pil(x + kb + 7, ky + 26, x + kb + mellom - 7, ky + 26, stroke=MORK, sw=2, spiss=9)
    s.rect(marg, ikke_y, B - 2 * marg, ikke_h, fill=GRA_LYS, stroke=GRA, sw=1.5, dash="6 5")
    s.text(marg + 18, ikke_y + 30, IKKE_MED[0], size=16, weight=700, fill=GRA_TEKST)
    kol = (B - 2 * marg - 36) / 2
    for i, p in enumerate(IKKE_MED[1]):
        px = marg + 18 + (i % 2) * kol
        py = ikke_y + 58 + (i // 2) * 24
        s.text(px, py, "–  " + p, size=15, fill=GRA_TEKST)
    s.text(B - marg, H - 14, KILDE_KONSEPT, size=12, fill=GRA_TEKST, anchor="end")
    s.lagre(ROT / "src" / "konsept-bred.svg")


def konsept_smal():
    B = 390
    marg = 16
    kb = B - 2 * marg
    tpl = 40
    kort = kort_innhold()
    dummy = Svg(B, 10)
    hoyder = [tegn_kort(dummy, 0, 0, kb, k, i + 1, tegn=False, tegn_per_linje=tpl) for i, k in enumerate(kort)]
    mellom = 34
    under = bryt(UNDERTITTEL, 44)
    y0 = 64 + len(under) * 19 + 18
    ikke_linjer = sum(len(bryt(p, 42)) for p in IKKE_MED[1])
    ikke_h = 44 + ikke_linjer * 21 + 8
    kilde_linjer = bryt(KILDE_KONSEPT, 58)
    H = y0 + sum(hoyder) + mellom * 3 + 24 + ikke_h + 20 + len(kilde_linjer) * 16 + 10
    s = Svg(B, H, tittel="Slik lages tallene",
            beskrivelse="Fire trinn fra arbeidsgiverens a-melding til publisert månedslønn, og hva som ikke er med i månedslønna.")
    s.text(marg, 38, "Slik lages tallene", size=24, weight=700, fill=MORK)
    s.tekstblokk(marg, 64, under, size=15, linjeavstand=19, fill=GRA_TEKST)
    y = y0
    for i, (k, h) in enumerate(zip(kort, hoyder)):
        s.rect(marg, y, kb, h, fill=BLAGRONN_LYS, stroke=BLAGRONN, sw=1)
        tegn_kort(s, marg, y, kb, k, i + 1, tegn_per_linje=tpl)
        if i < 3:
            s.pil(marg + 32, y + h + 6, marg + 32, y + h + mellom - 6, stroke=MORK, sw=2, spiss=9)
        y += h + mellom
    y += 24 - mellom
    s.rect(marg, y, kb, ikke_h, fill=GRA_LYS, stroke=GRA, sw=1.5, dash="6 5")
    s.text(marg + 16, y + 28, IKKE_MED[0], size=16, weight=700, fill=GRA_TEKST)
    py = y + 54
    for p in IKKE_MED[1]:
        linjer = bryt(p, 42)
        s.text(marg + 16, py, "–", size=15, fill=GRA_TEKST)
        s.tekstblokk(marg + 32, py, linjer, size=15, linjeavstand=19, fill=GRA_TEKST)
        py += len(linjer) * 21
    s.tekstblokk(marg, y + ikke_h + 24, kilde_linjer, size=12, linjeavstand=16, fill=GRA_TEKST)
    s.lagre(ROT / "src" / "konsept-smal.svg")


# ---------------------------------------------------------------- toppgrafikk

TB, TH = 1200, 330
FX0, FX1, FY0, FY1 = 640, 1150, 70, 252  # figurflate


def topp_tekst(s, etikett, stort, setning, linjer, stor_storrelse=66):
    s.text(40, 46, etikett.upper(), size=13, weight=600, fill=GRA_TEKST)
    s.text(40, 122, stort, size=stor_storrelse, weight=700, fill=MORK)
    sl = bryt(setning, 44)
    sy = s.tekstblokk(40, 164, sl, size=21, linjeavstand=27, weight=700, fill=MORK)
    s.tekstblokk(40, sy + 34, [l for linje in linjer for l in bryt(linje, 62)],
                 size=15, linjeavstand=21, fill=GRA_TEKST)


def kilde(s, tekst):
    s.text(FX1, TH - 12, tekst, size=12, fill=GRA_TEKST, anchor="end")


def topp_a():
    """Spørsmål 2: hva tjener de fleste? Desilfordelingen mot gjennomsnitt og median."""
    snitt, median = M["gjennomsnitt"], M["median"]
    d = DES["snitt"]
    s = Svg(TB, TH, tittel="Minst 6 av 10 har lavere lønn enn gjennomsnittet",
            beskrivelse=(f"Gjennomsnittlig månedslønn i hver tidel av heltidsekvivalentene, november 2025. "
                         f"Gjennomsnittet er {nb(snitt)} kroner, medianen {nb(median)}. "
                         f"Hele tidel 1 til 6 ligger under gjennomsnittet."))
    topp_tekst(s, "Lønn · november 2025", "6 av 10",
               "Minst 6 av 10 har lavere månedslønn enn gjennomsnittet.",
               [f"Gjennomsnittet var {kr(snitt)}, medianen {kr(median)}.",
                f"De 10 prosent best betalte hadde {kr(d[9])} i snitt og drar gjennomsnittet opp.",
                "Regnet i heltidsekvivalenter."])
    ymax = 130000

    def ys(v):
        return FY1 - v / ymax * (FY1 - FY0)
    s.text(FX0, FY0 - 22, "kroner per måned", size=12, fill=GRA_TEKST)
    for v in (0, 50000, 100000):
        s.line(FX0 + 52, ys(v), FX1 - 150, ys(v), stroke=NULLINJE if v == 0 else STOTTELINJE, sw=1)
        s.text(FX0 + 44, ys(v) + 4, nb(v), size=12, fill=GRA_TEKST, anchor="end")
    x0, x1 = FX0 + 62, FX1 - 160
    sone = (x1 - x0) / 10
    bw = sone / 1.5
    for i, v in enumerate(d):
        x = x0 + i * sone + (sone - bw) / 2
        under = DES["ovre_grense"][i] is not None and DES["ovre_grense"][i] < snitt
        s.rect(x, ys(v), bw, ys(0) - ys(v), fill=GRONN if under else GRA)
        s.text(x + bw / 2, FY1 + 18, str(i + 1), size=12, fill=GRA_TEKST, anchor="middle")
        if i == 9:
            s.text(x + bw / 2, ys(v) - 6, nb(v), size=12, fill=MORK, weight=700, anchor="middle")
    s.text(x0, FY1 + 36, "Tidel (desil), fra lavest til høyest lønn", size=11, fill=GRA_TEKST)
    # Referanselinjer: gjennomsnitt og median, grå med direkte merking
    for v, navn, dy in ((snitt, "Gjennomsnitt", -5), (median, "Median", 14)):
        s.line(x0 - 8, ys(v), x1 + 6, ys(v), stroke=MORK, sw=1.2, dash="4 3")
        s.text(x1 + 12, ys(v) + dy, f"{navn} {nb(v)}", size=12, fill=MORK, weight=600)
    s.rect(x1 + 12, FY1 - 40, 10, 10, fill=GRONN)
    s.text(x1 + 28, FY1 - 31, "Hele tidelen under", size=11, fill=GRA_TEKST)
    s.text(x1 + 28, FY1 - 17, "gjennomsnittet", size=11, fill=GRA_TEKST)
    kilde(s, f"Kilde: SSB, tabell 13860 og 11419. Sist oppdatert: {DATO['13860']}.")
    s.lagre(ROT / "docs" / "grafikk" / "02-topp-a.svg")


def topp_b():
    """Spørsmål 3: hva tjener et yrke? Prikkhistogram, ett punkt per yrke."""
    verdier = [v for v in Y["verdier"].values() if v is not None]
    uten = sum(1 for v in Y["verdier"].values() if v is None)
    lav, hoy = min(verdier), max(verdier)
    vis = ("5223", "2223", "1120", "3324")  # yrker som merkes i grafikken
    utv = {k: v for k, v in Y["utvalgte"].items() if k in vis}
    s = Svg(TB, TH, tittel="Snittlønna varierer mye mellom yrkene",
            beskrivelse=(f"Gjennomsnittlig månedslønn i {len(verdier)} yrker, november 2025, ett punkt per yrke. "
                         f"Fra {nb(lav)} til {nb(hoy)} kroner. Utvalgte yrker er merket."))
    topp_tekst(s, f"Lønn · november 2025 · {len(Y['verdier'])} yrker", f"{len(Y['verdier'])} yrker",
               "Snittlønna i yrkene går fra om lag 34 000 til 173 000 kroner i måneden.",
               [f"Hvert punkt er ett yrke, uansett hvor mange jobber det har. {uten} yrker mangler tall for 2025.",
                f"Gjennomsnittet for alle jobber var {kr(M['gjennomsnitt'])}."])
    bin_ = 2500
    xmin, xmax = 30000, 177500
    gx0, gx1 = FX0 + 10, FX1 - 10

    def xs(v):
        return gx0 + (v - xmin) / (xmax - xmin) * (gx1 - gx0)
    r = 2.6
    trinn = 5.4
    base = FY1 - 4
    hoyde = {}
    utvalgt_pos = {}
    utvalgt_v = {info[1]: kode for kode, info in utv.items()}
    for kode, v in sorted(Y["verdier"].items(), key=lambda kv: (kv[1] is None, kv[0] in utv, kv[1] or 0)):
        if v is None:
            continue
        b = v // bin_ * bin_
        n = hoyde.get(b, 0)
        cx = xs(b + bin_ / 2)
        cy = base - n * trinn
        hoyde[b] = n + 1
        if kode in utv:
            utvalgt_pos[kode] = (cx, cy)
        else:
            s.circle(cx, cy, r, GRONN_FLATE)
    for kode, (cx, cy) in utvalgt_pos.items():
        s.circle(cx, cy, r + 1.6, OKER_STREK, stroke="#ffffff", sw=1)
    # Akse
    s.line(gx0, FY1 + 2, gx1, FY1 + 2, stroke=NULLINJE, sw=1)
    for v in (50000, 100000, 150000):
        s.line(xs(v), FY1 + 2, xs(v), FY1 + 7, stroke=NULLINJE, sw=1)
        s.text(xs(v), FY1 + 20, nb(v), size=12, fill=GRA_TEKST, anchor="middle")
    s.text(gx1, FY1 + 36, "kroner per måned", size=12, fill=GRA_TEKST, anchor="end")
    # Gjennomsnitt alle jobber
    xa = xs(M["gjennomsnitt"])
    s.line(xa, FY0 - 18, xa, FY1 + 2, stroke=MORK, sw=1.2, dash="4 3")
    s.text(xa + 6, FY0 - 22, f"Gjennomsnitt alle jobber {nb(M['gjennomsnitt'])}", size=12, fill=MORK, weight=600)
    # Etiketter for utvalgte yrker: (kode, ankerside, etikett-y)
    plassering = {
        "5223": ("end", FY0 + 50), "2223": ("knekk", FY0 + 40),
        "1120": ("middle", FY1 - 70), "3324": ("end", FY1 - 46),
    }
    for kode, (anker, ly) in plassering.items():
        navn, v, _ = utv[kode]
        cx, cy = utvalgt_pos[kode]
        if anker == "knekk":
            # Etikett til høyre for gjennomsnittslinjen, knekt strek ned til punktet
            tx, anker = xa + 10, "start"
            s.polyline([(tx - 3, ly - 4), (cx, ly - 4), (cx, cy - r - 2)], stroke=GRA_TEKST, sw=0.8)
            s.text(tx, ly, navn, size=12, fill=MORK, weight=600, anchor=anker)
            s.text(tx, ly + 14, nb(v), size=12, fill=MORK, anchor=anker)
            continue
        tx = cx - 4 if anker == "end" else (cx + 4 if anker == "start" else cx)
        s.line(cx, cy - r - 2, cx, ly + 20, stroke=GRA_TEKST, sw=0.8)
        s.text(tx, ly, navn, size=12, fill=MORK, weight=600, anchor=anker)
        s.text(tx, ly + 14, nb(v), size=12, fill=MORK, anchor=anker)
    kilde(s, f"Kilde: SSB, tabell 11418 og 11419. Sist oppdatert: {DATO['11418']} og {DATO['11419']}.")
    s.lagre(ROT / "docs" / "grafikk" / "02-topp-b.svg")


def topp_c():
    """Spørsmål 5: hvorfor finnes det flere tall for lønnsveksten?"""
    mnd, utb, pal = V["manedslonn_nov_nov"], V["arslonn_utbetalt"], V["arslonn_palopt"]
    rader = [("alle", "Alle sektorer"), ("stat", "Statsforvaltningen"),
             ("privat", "Privat sektor og off. eide foretak"), ("kommune", "Kommuneforvaltningen")]
    s = Svg(TB, TH, tittel="Lønnsveksten i 2025 avhenger av hva som måles",
            beskrivelse=(f"Vekst i månedslønn november til november og i utbetalt årslønn 2025, etter sektor. "
                         f"Alle sektorer: {nb(mnd['alle'], 1)} og {nb(utb['alle'], 1)} prosent. "
                         f"Påløpt årslønn: {nb(pal['alle'], 1)} prosent."))
    topp_tekst(s, "Lønn · 2025", f"{nb(mnd['alle'], 1)} eller {nb(utb['alle'], 1)}?",
               "Hvor mye lønna steg i 2025, avhenger av hva som måles.",
               ["Månedslønna sammenligner november med november. Årslønna tar med hele året og etterbetalinger.",
                f"Påløpt årslønn, der etterbetalinger føres i året de er opptjent, steg {nb(pal['alle'], 1)} prosent."],
               stor_storrelse=60)
    lx = FX0
    x0, x1 = FX0 + 236, FX1 - 40
    xmax = 7.0

    def xs(v):
        return x0 + v / xmax * (x1 - x0)
    # Tegnforklaring over diagrammet
    ty = FY0 - 22
    s.rect(lx, ty - 10, 12, 12, fill=GRONN_FLATE)
    s.text(lx + 18, ty, "Månedslønn, november til november", size=12, fill=MORK)
    s.rect(lx + 250, ty - 10, 12, 12, fill=BLA_STREK)
    s.text(lx + 268, ty, "Årslønn, utbetalt", size=12, fill=MORK)
    for v in (0, 2, 4, 6):
        s.line(xs(v), FY0 - 4, xs(v), FY1 + 2, stroke=NULLINJE if v == 0 else STOTTELINJE, sw=1)
        s.text(xs(v), FY1 + 18, nb(v), size=12, fill=GRA_TEKST, anchor="middle")
    s.text(x1, FY1 + 34, "prosent", size=12, fill=GRA_TEKST, anchor="end")
    rh = (FY1 - FY0) / len(rader)
    bh = 14
    for i, (kode, navn) in enumerate(rader):
        yt = FY0 + i * rh + (rh - 2 * bh - 3) / 2
        for j, (verdier, farge) in enumerate(((mnd, GRONN_FLATE), (utb, BLA_STREK))):
            y = yt + j * (bh + 3)
            s.rect(xs(0), y, xs(verdier[kode]) - xs(0), bh, fill=farge)
            s.text(xs(verdier[kode]) + 5, y + bh - 2, nb(verdier[kode], 1), size=12, fill=MORK,
                   weight=700 if kode == "alle" else 400)
        s.text(lx, yt + bh + 6, navn, size=13, fill=MORK, weight=700 if kode == "alle" else 400)
    kilde(s, f"Kilde: SSB, tabell 11419, 11536 og 14858. Sist oppdatert: {DATO['11419']}, {DATO['11536']} og {DATO['14858']}.")
    s.lagre(ROT / "docs" / "grafikk" / "02-topp-c.svg")


if __name__ == "__main__":
    (ROT / "src").mkdir(exist_ok=True)
    (ROT / "docs" / "grafikk").mkdir(parents=True, exist_ok=True)
    konsept_bred()
    konsept_smal()
    topp_a()
    topp_b()
    topp_c()
    print("Ferdig")

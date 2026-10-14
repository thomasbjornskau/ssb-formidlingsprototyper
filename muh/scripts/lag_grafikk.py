"""Lager konseptgrafikk og toppgrafikkvarianter for muh (steg 2).

Leser data/grafikk-utkast.json. Skriver
  src/konsept-bred.svg, src/konsept-smal.svg
  docs/grafikk/02-topp-a.svg, -b.svg, -c.svg
Bare Pythons standardbibliotek og felles/grafikk.py.
"""

import json
import sys
from pathlib import Path

ROT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from grafikk_muh import (Svg, nb, bryt, MORK, GRA_TEKST, LINJE, BLAGRONN_LYS, BLAGRONN,
                     GRONN, GRONN_LYS, GRA, GRA_LYS, STOTTELINJE, NULLINJE, KAT)

D = json.loads((ROT / "data" / "grafikk-utkast.json").read_text(encoding="utf-8"))
AAR = D["aar"]
A = D["aarstall"]
AUG = D["august_2026"]
REV = D["revisjon_juli_2026"]

GRONN_STREK, GRONN_FLATE = KAT[0]
BLA_STREK, BLA_FLATE = KAT[1]
OKER_STREK, OKER_FLATE = KAT[2]


def mrd(mill, des=1):
    return nb(mill / 1000, des)


# ---------------------------------------------------------------- konsept

def kort_innhold():
    """De fire trinnene. Hver blokk: (type, innhold). Kilde i kommentar."""
    jul_forst = REV["forste_publisert_1000kr"] / 1e6
    jul_sept = REV["publisert_september_1000kr"] / 1e6
    rest = (AUG["Ekondens"] + AUG["Eskipplat"])
    return [
        {   # [K2]
            "tittel": "Varen krysser grensen",
            "blokker": [
                ("tekst", "De fleste varer meldes i en tolldeklarasjon når de går inn eller ut av landet."),
                ("liste", ["Olje og gass: operatørene og Sokkeldirektoratet",
                           "Strøm: målt ved kablene til utlandet",
                           "Skip og plattformer: registre og selskaper"]),
            ],
        },
        {   # [K2][K3]
            "tittel": "Verdien settes ved grensen",
            "blokker": [
                ("tekst", "Eksport regnes uten frakt videre fra grensen, import med frakt og forsikring fram til grensen. Toll og merverdiavgift er ikke med."),
                ("merknad", "Olje og gass får først en anslått pris, fra Brent og europeiske spotpriser for gass. Den byttes senere ut med faktisk pris."),
            ],
        },
        {   # [K2][K9]
            "tittel": "Fordelt på vare og land",
            "blokker": [
                ("tekst", "Eksport føres på landet varen sendes til, import på landet den er laget i. Så trekkes olje, gass, skip og plattformer fra."),
                ("regnestykke", {
                    "overskrift": "August 2026, mrd. kr",
                    "rader": [
                        ("Eksport i alt", mrd(AUG["Etot"]), False),
                        ("Råolje", "−" + mrd(AUG["Eolje"]), False),
                        ("Naturgass", "−" + mrd(AUG["Egass"]), False),
                        ("Kondensater, skip og plattformer", "−" + nb(rest / 1000, 2), False),
                        ("Fastlandseksport", mrd(AUG["Etotusorn"]), True),
                    ],
                }),
            ],
        },
        {   # [K2][K3][K11]
            "tittel": "Publisert, så revidert",
            "blokker": [
                ("tekst", "Tallene kommer rundt den 15. i måneden etter. Hver ny måned kan endre de tidligere månedene i året."),
                ("stolper", {
                    "overskrift": "Eksport juli 2026, mrd. kr",
                    "rader": [("Først publisert", jul_forst), ("En måned senere", jul_sept)],
                }),
                ("merknad", "Endelige tall kommer i mai to år etter."),
            ],
        },
    ]


def tegn_kort(s, x, y, b, kort, nr, h=None, tegn=True, tegn_per_linje=30):
    """Tegner ett trinn. Returnerer høyden innholdet trenger."""
    pad = 18
    iy = y + 26
    if tegn:
        s.markor(x + pad + 14, iy, nr, r=14)
    tl = bryt(kort["tittel"], max(14, tegn_per_linje - 13))
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
        elif typ == "liste":
            for punkt in innhold:
                linjer = bryt(punkt, tegn_per_linje - 2)
                if tegn:
                    s.circle(x + pad + 3, cy - 5, 2.5, GRA_TEKST)
                    s.tekstblokk(x + pad + 12, cy, linjer, size=14, linjeavstand=19, fill=GRA_TEKST)
                cy += len(linjer) * 19 + 4
            cy += 6
        elif typ == "merknad":
            linjer = bryt(innhold, tegn_per_linje - 2)
            bh = len(linjer) * 19 + 16
            if tegn:
                s.rect(x + pad, cy - 6, b - 2 * pad, bh, fill=GRA_LYS)
                s.tekstblokk(x + pad + 10, cy + 12, linjer, size=14, linjeavstand=19, fill=GRA_TEKST)
            cy += bh + 10
        elif typ == "regnestykke":
            rader = innhold["rader"]
            bh = 32 + sum(2 if len(bryt(r[0], tegn_per_linje - 9)) > 1 else 1 for r in rader) * 20 + 14
            if tegn:
                bx, bw = x + pad, b - 2 * pad
                s.rect(bx, cy - 6, bw, bh, fill=GRONN_LYS)
                s.text(bx + 10, cy + 12, innhold["overskrift"], size=13, fill=GRA_TEKST, weight=600)
            ry = cy + 36
            for tekst, verdi, sum_ in rader:
                linjer = bryt(tekst, tegn_per_linje - 9)
                if tegn:
                    bx, bw = x + pad, b - 2 * pad
                    if sum_:
                        s.line(bx + 10, ry - 15, bx + bw - 10, ry - 15, stroke=GRONN, sw=1)
                    s.tekstblokk(bx + 10, ry, linjer, size=14, linjeavstand=18,
                                 fill=GRONN if sum_ else MORK, weight=700 if sum_ else 400)
                    s.text(bx + bw - 10, ry + (len(linjer) - 1) * 18, verdi, size=14,
                           fill=GRONN if sum_ else MORK, weight=700 if sum_ else 400, anchor="end")
                ry += len(linjer) * 20
            cy += bh + 10
        elif typ == "stolper":
            rader = innhold["rader"]
            maks = max(v for _, v in rader)
            bh = 30 + len(rader) * 40 + 4
            if tegn:
                bx, bw = x + pad, b - 2 * pad
                s.text(bx, cy + 8, innhold["overskrift"], size=13, fill=GRA_TEKST, weight=600)
                tallplass = 48
                skala = (bw - tallplass) / maks
                for i, (tekst, v) in enumerate(rader):
                    ry = cy + 26 + i * 40
                    s.text(bx, ry + 6, tekst, size=13, fill=MORK)
                    farge = GRA if i == 0 else GRONN
                    s.rect(bx, ry + 12, v * skala, 14, fill=farge)
                    s.text(bx + v * skala + 6, ry + 24, nb(v, 1), size=13, fill=MORK, weight=600)
                s.line(bx, cy + 30, bx, cy + 26 + len(rader) * 40 - 8, stroke=NULLINJE, sw=1)
            cy += bh + 6
    return cy - y + 8


IKKE_MED = ("Ikke med i tallene", [
    "Tjenester, som frakt, reiser og konsulentarbeid",
    "Renter og utbytte",
    "Varer i transitt gjennom Norge",
    "Småsendinger under om lag 1 000 kr",
])

KILDE_KONSEPT = "Kilde: SSB, Om statistikken (arkivversjon 2015) og tabell 08792 og 12308. Sist oppdatert: 15.09.2026."


def konsept_bred():
    B = 1200
    marg, mellom = 36, 34
    kb = (B - 2 * marg - 3 * mellom) / 4
    kort = kort_innhold()
    dummy = Svg(B, 10)
    h = max(tegn_kort(dummy, 0, 0, kb, k, i + 1, tegn=False) for i, k in enumerate(kort))
    ky = 96
    ikke_y = ky + h + 28
    H = ikke_y + 96 + 34
    s = Svg(B, H, tittel="Slik lages tallene",
            beskrivelse="Fire trinn fra varen krysser grensen til tallene publiseres og revideres, og hva som ikke er med.")
    s.text(marg, 44, "Slik lages tallene", size=26, weight=700, fill=MORK)
    s.text(marg, 72, "Utenrikshandel med varer: fra grensen til publisert tall", size=16, fill=GRA_TEKST)
    for i, k in enumerate(kort):
        x = marg + i * (kb + mellom)
        s.rect(x, ky, kb, h, fill=BLAGRONN_LYS, stroke=BLAGRONN, sw=1)
        tegn_kort(s, x, ky, kb, k, i + 1)
        if i < 3:
            s.pil(x + kb + 7, ky + 26, x + kb + mellom - 7, ky + 26, stroke=MORK, sw=2, spiss=9)
    # Ikke med
    s.rect(marg, ikke_y, B - 2 * marg, 96, fill=GRA_LYS, stroke=GRA, sw=1.5, dash="6 5")
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
    y0 = 102
    ikke_linjer = sum(len(bryt(p, 42)) for p in IKKE_MED[1])
    ikke_h = 44 + ikke_linjer * 21 + 8
    kilde_linjer = bryt(KILDE_KONSEPT, 58)
    H = y0 + sum(hoyder) + mellom * 3 + 24 + ikke_h + 20 + len(kilde_linjer) * 16 + 10
    s = Svg(B, H, tittel="Slik lages tallene",
            beskrivelse="Fire trinn fra varen krysser grensen til tallene publiseres og revideres, og hva som ikke er med.")
    s.text(marg, 38, "Slik lages tallene", size=24, weight=700, fill=MORK)
    s.tekstblokk(marg, 64, bryt("Utenrikshandel med varer: fra grensen til publisert tall", 44),
                 size=15, linjeavstand=19, fill=GRA_TEKST)
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


def topp_tekst(s, etikett, stort, setning, linjer, stor_farge=MORK):
    # Tall og «mrd. kr» skal ikke brytes fra hverandre
    setning = setning.replace(" mrd. kr", " mrd. kr")
    linjer = [l.replace(" mrd. kr", " mrd. kr") for l in linjer]
    s.text(40, 46, etikett.upper(), size=13, weight=600, fill=GRA_TEKST)
    s.text(40, 122, stort, size=66, weight=700, fill=stor_farge)
    sl = bryt(setning, 44)
    sy = s.tekstblokk(40, 164, sl, size=21, linjeavstand=27, weight=700, fill=MORK)
    s.tekstblokk(40, sy + 34, [l for linje in linjer for l in bryt(linje, 62)],
                 size=15, linjeavstand=21, fill=GRA_TEKST)


def y_akse(s, verdier, ymin, ymax, enhet, fmt=lambda v: nb(v)):
    def ys(v):
        return FY1 - (v - ymin) / (ymax - ymin) * (FY1 - FY0)
    s.text(FX0, FY0 - 22, enhet, size=12, fill=GRA_TEKST)
    for v in verdier:
        y = ys(v)
        s.line(FX0 + 44, y, FX1, y, stroke=NULLINJE if v == 0 else STOTTELINJE, sw=1)
        s.text(FX0 + 36, y + 4, fmt(v), size=12, fill=GRA_TEKST, anchor="end")
    return ys


def x_etiketter(s, xs, y):
    for i, (aar, x) in enumerate(zip(AAR, xs)):
        if i % 2 == 0 or i == len(AAR) - 1:
            s.text(x, y, aar, size=12, fill=GRA_TEKST, anchor="middle")


def kilde(s, tekst):
    s.text(FX1, TH - 12, tekst, size=12, fill=GRA_TEKST, anchor="end")


def topp_a():
    """Spørsmål 1: hvor mye er olje og gass, hvor mye fastland."""
    s = Svg(TB, TH, tittel="Olje og gass er over halvparten av vareeksporten",
            beskrivelse="Vareeksport 2015–2025 fordelt på olje og gass, fastlandseksport og skip og plattformer. I 2025 var olje og gass 57 prosent.")
    andel = [o / t * 100 for o, t in zip(A["Eoljegass"], A["Etot"])]
    topp_tekst(s, "Utenrikshandel med varer · 2025", "6 av 10",
               "Nesten 6 av 10 eksportkroner kom fra olje og gass i 2025.",
               [f"Andelen følger prisene: {nb(andel[5])} prosent i 2020, {nb(andel[7])} prosent i 2022.",
                f"Fastlandseksporten var {mrd(A['Etotusorn'][-1], 0)} mrd. kr."])
    ymax = 2800
    ys = y_akse(s, [0, 1000, 2000], 0, ymax, "mrd. kr", fmt=lambda v: nb(v))
    n = len(AAR)
    sone = (FX1 - 150 - (FX0 + 54)) / n
    bw = sone / 1.5
    xs = []
    for i in range(n):
        x = FX0 + 54 + i * sone + (sone - bw) / 2
        xs.append(x + bw / 2)
        y = FY1
        for verdi, farge in ((A["Etotusorn"][i], GRONN_FLATE), (A["Eoljegass"][i], BLA_FLATE), (A["Eskipplat"][i], GRA)):
            hh = verdi / 1000 / ymax * (FY1 - FY0)
            s.rect(x, y - hh, bw, hh, fill=farge)
            y -= hh
        s.text(x + bw / 2, ys(A["Etot"][i] / 1000) - 6, nb(andel[i]), size=11, fill=MORK, anchor="middle",
               weight=700 if i in (5, 7, n - 1) else 400)
    s.line(FX0 + 44, FY1, FX1 - 150, FY1, stroke=NULLINJE)
    x_etiketter(s, xs, FY1 + 18)
    # direkte merking ved siste stolpe
    lx = xs[-1] + bw / 2 + 10
    s.text(lx, ys(A["Etotusorn"][-1] / 2000) + 4, "Fastland", size=13, fill=MORK, weight=600)
    s.text(lx, ys((A["Etotusorn"][-1] + A["Eoljegass"][-1] / 2) / 1000) + 4, "Olje og gass", size=13, fill=MORK, weight=600)
    s.text(FX1 - 150 + 10, FY0 - 22, "Tall over stolpene: andel", size=11, fill=GRA_TEKST)
    s.text(FX1 - 150 + 10, FY0 - 8, "olje og gass, prosent", size=11, fill=GRA_TEKST)
    s.text(FX0 + 54, FY1 + 40, "Grått øverst: skip og plattformer, under 2 prosent alle år.", size=11, fill=GRA_TEKST)
    kilde(s, "Kilde: SSB, tabell 08800. Sist oppdatert: 15.05.2026.")
    s.lagre(ROT / "docs" / "grafikk" / "02-topp-a.svg")


def topp_b():
    """Spørsmål 2: pris eller mengde."""
    I = D["indekser_eksport_i_alt"]
    e = I["endring_2022"]
    s = Svg(TB, TH, tittel="Eksportverdien følger prisene, ikke mengden",
            beskrivelse="Pris- og volumindeks for vareeksporten 2015–2025, 2000 = 100. I 2022 steg prisene 81,8 prosent og volumet 0,2 prosent.")
    topp_tekst(s, "Utenrikshandel med varer · 2022", "+82 %",
               "Eksportprisene steg 82 prosent i 2022. Mengden sto nesten stille.",
               [f"Volumet økte {nb(e['VolumEndr'], 1)} prosent. Eksportverdien gikk fra {mrd(A['Etot'][6], 0)} til {mrd(A['Etot'][7], 0)} mrd. kr.",
                "Mest av økningen kom fra høyere gasspriser."], stor_farge=MORK)
    ys = y_akse(s, [0, 100, 200, 300, 400], 0, 480, "indeks, 2000 = 100")
    n = len(AAR)
    x0, x1 = FX0 + 64, FX1 - 130
    xs = [x0 + i * (x1 - x0) / (n - 1) for i in range(n)]
    for serie, farge, navn in (("Volumindeks", GRONN_STREK, "Mengde"), ("Prisindeks", OKER_STREK, "Pris")):
        pts = [(x, ys(v)) for x, v in zip(xs, I[serie])]
        s.polyline(pts, stroke=farge, sw=3)
        s.circle(*pts[7], 4.5, farge)
        s.text(xs[-1] + 10, ys(I[serie][-1]) + 5, navn, size=14, weight=700, fill=MORK)
    s.text(xs[7], ys(I["Prisindeks"][7]) - 12, nb(I["Prisindeks"][7], 1), size=12, weight=700, fill=MORK, anchor="middle")
    s.text(xs[7], ys(I["Volumindeks"][7]) - 12, nb(I["Volumindeks"][7], 1), size=12, weight=700, fill=MORK, anchor="middle")
    x_etiketter(s, xs, FY1 + 18)
    kilde(s, "Kilde: SSB, tabell 06322. Sist oppdatert: 15.05.2026.")
    s.lagre(ROT / "docs" / "grafikk" / "02-topp-b.svg")


def topp_c():
    """Spørsmål 3: handelsbalansen og fastlandsbalansen."""
    s = Svg(TB, TH, tittel="Overskudd med olje og gass, underskudd for fastlandet",
            beskrivelse="Handelsbalansen og fastlandsbalansen 2015–2025. I 2025 var handelsbalansen 660,9 mrd. kr og fastlandsbalansen minus 347,7 mrd. kr.")
    topp_tekst(s, "Utenrikshandel med varer · 2025", "−350 mrd. kr",
               "Fastlands-Norge kjøpte varer for om lag 350 mrd. kr mer enn det solgte i 2025.",
               [f"Med olje og gass ble det likevel et overskudd på {mrd(A['Hbtot'][-1], 0)} mrd. kr.",
                "Fastlandsbalansen har vært negativ alle år 2015–2025."])
    ymin, ymax = -500, 1750
    ys = y_akse(s, [-500, 0, 500, 1000, 1500], ymin, ymax, "mrd. kr")
    n = len(AAR)
    x0, x1 = FX0 + 54, FX1 - 150
    sone = (x1 - x0) / n
    bw = sone / 1.5 / 2
    xs = []
    for i in range(n):
        xm = x0 + i * sone + sone / 2
        xs.append(xm)
        for j, (verdi, farge) in enumerate(((A["Hbtot"][i], OKER_FLATE), (A["Hbtusorn"][i], GRONN_FLATE))):
            v = verdi / 1000
            x = xm - bw + j * bw
            y0, y1 = ys(max(v, 0)), ys(min(v, 0))
            s.rect(x, y0, bw, y1 - y0, fill=farge)
    s.line(FX0 + 44, ys(0), x1, ys(0), stroke=NULLINJE)
    x_etiketter(s, xs, FY1 + 18)
    lx = xs[-1] + sone / 2 + 6
    s.text(lx, ys(A["Hbtot"][-1] / 1000) + 4, "Handelsbalansen", size=13, weight=600, fill=MORK)
    s.text(lx, ys(A["Hbtot"][-1] / 1000) + 20, mrd(A["Hbtot"][-1]), size=12, fill=MORK)
    s.text(lx, ys(A["Hbtusorn"][-1] / 1000) + 4, "Fastlandsbalansen", size=13, weight=600, fill=MORK)
    s.text(lx, ys(A["Hbtusorn"][-1] / 1000) + 20, mrd(A["Hbtusorn"][-1]), size=12, fill=MORK)
    s.text(FX0 + 54, FY1 + 40, "Fastlandsbalansen: fastlandseksport minus import utenom skip og plattformer.", size=11, fill=GRA_TEKST)
    kilde(s, "Kilde: SSB, tabell 08800. Sist oppdatert: 15.05.2026.")
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

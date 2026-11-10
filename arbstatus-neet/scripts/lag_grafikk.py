"""Lager konseptgrafikk, toppgrafikkvarianter og samleside for arbstatus-neet (steg 2).

Leser json-stat2 fra data/raw/ (hentet direkte fra data.ssb.no 10.11.2026)
og skriver data/grafikk-utkast.json, src/konsept-*.svg og docs/grafikk/.
Bare Pythons standardbibliotek.
"""
import itertools
import json
import pathlib
import sys

ROT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROT / "scripts"))
from grafikk import Svg, nb, bryt, F_TITTEL, F_MELLOM, F_TEKST  # noqa: E402

# ---------- data ----------
RAW = ROT / "data" / "raw" / "tverrsnitt.json"
d = json.load(open(RAW, encoding="utf-8"))
OPPDATERT = d["updated"][:10]  # 2026-09-04
dims = [list(d["dimension"][k]["category"]["index"]) for k in d["id"]]
V = {combo: d["value"][i] for i, combo in enumerate(itertools.product(*dims))}
assert not d.get("status"), "Statussymboler i svaret – må tolkes før bruk"

NEET = ["A.09", "U.04-U.05", "U.90B"]
DELER = [  # rekkefølge og farge brukes likt i alle varianter
    ("U.04-U.05", "AAP eller uføretrygd", "#339b71"),
    ("A.09", "Registrert ledige", "#3face6"),
    ("U.90B.00", "Andre ordninger, ikke på tiltak", "#d5a640"),
    ("UX.00", "Ukjent status", "#b9c5c6"),
]


def v(s, t="2025", k="0", a="15-29", u="TOT", i="A-G"):
    if s == "NEET":
        return sum(V[(k, a, u, i, x, "Bosatte", t)] for x in NEET)
    return V[(k, a, u, i, s, "Bosatte", t)]


AAR = [str(y) for y in range(2008, 2026)]
data = {
    "kilde": "SSB, tabell 12424",
    "sist_oppdatert": OPPDATERT,
    "merknad": "Utkast til steg 2. Tall regnet fra data/raw/12424_bosatte.json; erstattes av kildekartet i steg 3. 2025 er foreløpige tall.",
    "neet_definisjon": "A.09 + U.04-U.05 + U.90B (stemmer med NEET-koden i tabell 13556)",
    "2025": {"bosatte": v("TOT"), "neet": v("NEET"), **{n: v(c) for c, n, _ in DELER}},
    "tidsserie": {t: {"neet": v("NEET", t), "aap_ufore": v("U.04-U.05", t), "bosatte": v("TOT", t)} for t in AAR},
    "innvandring": {},
    "fare_25_29": [],
}
for kode, navn in [("B", "Innvandrere"), ("A_C-G", "Befolkningen ekskl. innvandrere")]:
    data["innvandring"][navn] = {"bosatte": v("TOT", i=kode), "neet": v("NEET", i=kode),
                                 **{n: v(c, i=kode) for c, n, _ in DELER}}
UTD = [("1-2", "Grunnskole"), ("3-5", "Videregående"), ("6-8", "Universitet/høgskole"), ("0_9", "Uoppgitt/ingen")]
for kode, navn in [("A_C-G", "Ekskl. innvandrere"), ("B", "Innvandrere")]:
    for u, un in UTD:
        n_ = v("NEET", a="25-29", u=u, i=kode)
        data["fare_25_29"].append({"gruppe": navn, "utdanning": un, "neet": n_,
                                   "bosatte": v("TOT", a="25-29", u=u, i=kode),
                                   "aap_ufore": v("U.04-U.05", a="25-29", u=u, i=kode)})
data["fare_25_29_alle"] = {"neet": v("NEET", a="25-29"), "bosatte": v("TOT", a="25-29"),
                           "aap_ufore": v("U.04-U.05", a="25-29")}
(ROT / "data" / "grafikk-utkast.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

D25 = data["2025"]
pct = lambda a, b: 100 * a / b  # noqa: E731
DATO = ".".join(reversed(OPPDATERT.split("-")))
KILDE = f"Kilde: SSB, tabell 12424. Sist oppdatert: {DATO}. Tallene for 2025 er foreløpige."

# farger
TXT, SEK, GRID, NULL = "#274246", "#5e787a", "#d9dfe0", "#a9b5b7"
M5, M1, M2, G4, G2, G1 = "#274247", "#f0f8f9", "#c3dcdc", "#00824d", "#b6e8b8", "#ecfeed"
GRA, GRA1 = "#b9c5c6", "#f3f5f5"

GRAF = ROT / "docs" / "grafikk"
SRC = ROT / "src"


# ---------- konseptgrafikk ----------
TRINN = [
    ("Alle unge som bor i Norge",
     f"{nb(D25['bosatte'])} personer 15–29 år var registrert bosatt i november 2025."),
    ("Én status per person",
     "Registre over arbeid, utdanning, tiltak og ytelser kobles. Har noen flere statuser, "
     "teller den høyest prioriterte. Studerer du og har uføretrygd, telles du som student."),
    ("Utenfor = NEET",
     f"Den som verken er i arbeid, utdanning eller arbeidsmarkedstiltak, er utenfor: "
     f"{nb(D25['neet'])} personer. De fordeler seg på fire statuser."),
    ("Fordelt på grupper",
     "Tallene fordeles på kjønn, alder (15–19, 20–24 og 25–29 år), utdanningsnivå og "
     "innvandrere og befolkningen ellers. Små celler avrundes."),
]
IKKE_MED = ("Ikke med: hvem som er nye, og hvor lenge hver person har vært utenfor. "
            "Tabellen tar et bilde i november hvert år og følger ikke de samme personene.")


def minibar(s, x, y, b, h=22, etiketter=True):
    """NEET delt i fire, med tall under."""
    tot = D25["neet"]
    xx = x
    for kode, navn, farge in DELER:
        w = b * D25[navn] / tot
        s.rect(xx, y, w, h, fill=farge)
        xx += w
    if etiketter:
        yy = y + h + 22
        for kode, navn, farge in DELER:
            s.rect(x, yy - 11, 11, 11, fill=farge)
            s.text(x + 18, yy, f"{navn.replace(', ikke på tiltak', '')}: {nb(D25[navn])}", size=14, fill=TXT, num=True)
            yy += 21
        return yy
    return y + h


def konsept_bred():
    B, H = 1200, 470
    s = Svg(B, H, tittel="Slik lages tallene for unge utenfor")
    bw, gap, x0, y0, bh = 264, 28, 30, 30, 330
    for n, (tit, tekst) in enumerate(TRINN):
        x = x0 + n * (bw + gap)
        s.rect(x, y0, bw, bh, fill=G1 if n == 2 else M1, stroke=M2, sw=1, rx=2)
        s.rect(x, y0, bw, 5, fill=G4)
        s.circle(x + 30, y0 + 40, 16, fill=M5)
        s.text(x + 30, y0 + 46, n + 1, size=16, fill="#ffffff", font=F_MELLOM, weight="bold", anchor="middle")
        yy = s.tekstblokk(x + 56, y0 + 46, tit, 18, size=19, font=F_MELLOM, weight="bold", fill=TXT, lh=24)
        yy = s.tekstblokk(x + 18, max(yy, y0 + 80) + 14, tekst, 30, size=15, fill=TXT, lh=22)
        if n == 2:
            minibar(s, x + 18, yy + 4, bw - 36)
        if n < 3:
            s.pil(x + bw + 4, y0 + 40, x + bw + gap - 4, y0 + 40, farge=M5)
    # det som ikke er med
    y = y0 + bh + 22
    s.rect(x0, y, B - 2 * x0, 62, fill=GRA1, stroke=GRA, sw=1, rx=2, dash="6 4")
    s.tekstblokk(x0 + 20, y + 26, IKKE_MED, 130, size=15, fill=SEK, lh=22)
    s.lagre(SRC / "konsept-bred.svg")


def konsept_smal():
    B = 390
    s = Svg(B, 1300, tittel="Slik lages tallene for unge utenfor")
    x, y = 16, 16
    for n, (tit, tekst) in enumerate(TRINN):
        linjer = bryt(tekst, 38)
        bh = 70 + len(linjer) * 22 + (130 if n == 2 else 0)
        s.rect(x, y, B - 2 * x, bh, fill=G1 if n == 2 else M1, stroke=M2, sw=1, rx=2)
        s.rect(x, y, 5, bh, fill=G4)
        s.circle(x + 34, y + 32, 15, fill=M5)
        s.text(x + 34, y + 38, n + 1, size=15, fill="#ffffff", font=F_MELLOM, weight="bold", anchor="middle")
        s.text(x + 60, y + 38, tit, size=18, font=F_MELLOM, weight="bold", fill=TXT)
        yy = s.tekstblokk(x + 20, y + 74, tekst, 38, size=15, fill=TXT, lh=22)
        if n == 2:
            minibar(s, x + 20, yy, B - 2 * x - 40)
        y += bh
        if n < 3:
            s.pil(B / 2, y + 4, B / 2, y + 26, farge=M5)
            y += 30
    y += 16
    linjer = bryt(IKKE_MED, 40)
    s.rect(x, y, B - 2 * x, 30 + len(linjer) * 22, fill=GRA1, stroke=GRA, sw=1, rx=2, dash="6 4")
    yy = s.tekstblokk(x + 16, y + 28, IKKE_MED, 40, size=15, fill=SEK, lh=22)
    s.h = int(yy + 20)
    s.deler[1] = f'<rect x="0" y="0" width="{B}" height="{s.h}" fill="#ffffff"/>'
    s.lagre(SRC / "konsept-smal.svg")


# ---------- toppgrafikk: felles ramme ----------
def topp_ramme(s, etikett, stort, setning, under, storrelse=64):
    s.text(40, 46, etikett, size=15, fill=SEK, weight="600")
    s.text(40, 122, stort, size=storrelse, fill=TXT, font=F_TITTEL, weight="bold")
    y = s.tekstblokk(40, 164, setning, 40, size=21, fill=TXT, weight="600", lh=28)
    s.tekstblokk(40, y + 8, under, 62, size=15, fill=SEK, lh=21)
    s.text(40, 314, KILDE, size=13, fill=SEK)


def topp_a():
    s = Svg(1200, 330, tittel="Toppgrafikk A: hva betyr utenfor")
    topp_ramme(s, "Unge utenfor · 15–29 år · 2025", "1 av 10",
               "unge er verken i arbeid, utdanning eller arbeidsmarkedstiltak.",
               f"{nb(D25['neet'])} personer i november 2025. Over halvparten av dem har ukjent status: "
               "de bor i Norge, men finnes ikke i registrene over arbeid, utdanning, tiltak eller ytelser.")
    x0, b, y0, h = 620, 540, 78, 50
    s.text(x0, y0 - 16, f"{nb(D25['neet'])} unge utenfor, fordelt etter status", size=15, fill=TXT, weight="600")
    tot, xx = D25["neet"], x0
    kol = [x0, x0 + 138, x0 + 276, x0 + 414]
    for j, (kode, navn, farge) in enumerate(DELER):
        w = b * D25[navn] / tot
        s.rect(xx, y0, w, h, fill=farge)
        if j:
            s.line(xx, y0, xx, y0 + h, stroke="#ffffff", sw=2)
        mid = xx + w / 2
        s.polyline([(mid, y0 + h + 4), (mid, y0 + h + 14), (kol[j] + 2, y0 + h + 30), (kol[j] + 2, y0 + h + 38)],
                   stroke=NULL, sw=1)
        yy = s.tekstblokk(kol[j], y0 + h + 58, navn, 17, size=14, fill=TXT, weight="bold", lh=19)
        s.text(kol[j], yy + 4, nb(D25[navn]), size=20, fill=TXT, weight="bold", num=True)
        s.text(kol[j], yy + 26, f"{nb(pct(D25[navn], tot))} prosent", size=14, fill=SEK, num=True)
        xx += w
    s.lagre(GRAF / "02-topp-A.svg")


def topp_b():
    ts = data["tidsserie"]
    s = Svg(1200, 330, tittel="Toppgrafikk B: tyngre enn før")
    a08, a25 = ts["2008"]["aap_ufore"], ts["2025"]["aap_ufore"]
    topp_ramme(s, "Unge utenfor · 15–29 år · 2008–2025", "Dobbelt så mange",
               "unge utenfor er på AAP eller uføretrygd som i 2008.",
               f"Andelen unge utenfor er omtrent den samme ({nb(pct(ts['2008']['neet'], ts['2008']['bosatte']), 1)} "
               f"prosent i 2008, {nb(pct(ts['2025']['neet'], ts['2025']['bosatte']), 1)} i 2025). "
               f"Men gruppen på AAP eller uføretrygd har økt fra {nb(a08)} til {nb(a25)}.", storrelse=54)
    x0, x1, y0, y1 = 690, 1050, 64, 280
    ymax = 140000
    Y = lambda val: y1 - (y1 - y0) * val / ymax  # noqa: E731
    s.text(x0 - 50, y0 - 18, "antall personer", size=13, fill=SEK)
    for g in range(0, ymax + 1, 40000):
        s.line(x0, Y(g), x1, Y(g), stroke=NULL if g == 0 else GRID, sw=1)
        s.text(x0 - 8, Y(g) + 5, nb(g), size=13, fill=SEK, anchor="end", num=True)
    slot = (x1 - x0) / len(AAR)
    bw = slot * 2 / 3
    for n, t in enumerate(AAR):
        x = x0 + n * slot + (slot - bw) / 2
        a, r = ts[t]["aap_ufore"], ts[t]["neet"] - ts[t]["aap_ufore"]
        s.rect(x, Y(a), bw, Y(0) - Y(a), fill="#00824d")
        s.rect(x, Y(a + r), bw, Y(a) - Y(a + r), fill=GRA)
        if t in ("2008", "2015", "2025"):
            s.text(x + bw / 2, y1 + 20, t, size=13, fill=SEK, anchor="middle")
    # direkte merking til høyre for siste stolpe
    xl = x1 + 10
    s.text(xl, Y(a25 / 2) - 4, "AAP eller", size=13, fill=TXT, weight="bold")
    s.text(xl, Y(a25 / 2) + 12, "uføretrygd", size=13, fill=TXT, weight="bold")
    s.text(xl, Y(a25 / 2) + 30, nb(a25), size=13, fill=TXT, num=True)
    rest25 = ts["2025"]["neet"] - a25
    s.text(xl, Y(a25 + rest25 / 2) - 4, "Andre", size=13, fill=SEK, weight="bold")
    s.text(xl, Y(a25 + rest25 / 2) + 12, "utenfor", size=13, fill=SEK, weight="bold")
    s.text(xl, Y(a25 + rest25 / 2) + 30, nb(rest25), size=13, fill=SEK, num=True)
    # 2008-verdi
    s.text(x0 + slot / 2, Y(a08) - 30, nb(a08), size=13, fill=TXT, anchor="start", num=True, weight="bold")
    s.line(x0 + slot / 2, Y(a08) - 26, x0 + slot / 2, Y(a08) - 2, stroke=TXT, sw=1)
    s.lagre(GRAF / "02-topp-B.svg")


def topp_c():
    inn = data["innvandring"]
    I, E = inn["Innvandrere"], inn["Befolkningen ekskl. innvandrere"]
    s = Svg(1200, 330, tittel="Toppgrafikk C: innvandrere og befolkningen ellers")
    topp_ramme(s, "Unge utenfor · 15–29 år · 2025", "Nær 3 av 4",
               "innvandrere som er utenfor, har ukjent status. Ellers gjelder det 4 av 10.",
               f"Innvandrere er oftere utenfor ({nb(pct(I['neet'], I['bosatte']), 1)} prosent) enn befolkningen "
               f"ellers ({nb(pct(E['neet'], E['bosatte']), 1)} prosent). Men de er sjeldnere på AAP eller uføretrygd.")
    x0, b = 620, 540
    # tegnforklaring over
    lx, ly = x0, 44
    for kode, navn, farge in DELER:
        kort = navn.replace("Andre ordninger, ikke på tiltak", "Andre ordninger")
        s.rect(lx, ly - 11, 12, 12, fill=farge)
        s.text(lx + 18, ly, kort, size=13, fill=TXT)
        lx += 28 + len(kort) * 7.2
    for r, (navn, g) in enumerate([("Innvandrere", I), ("Befolkningen ekskl. innvandrere", E)]):
        y = 92 + r * 100
        s.text(x0, y, navn, size=15, fill=TXT, weight="bold")
        s.text(x0 + b, y, f"{nb(g['neet'])} utenfor · {nb(pct(g['neet'], g['bosatte']), 1)} prosent av alle",
               size=14, fill=SEK, anchor="end", num=True)
        xx = x0
        for kode, dn, farge in DELER:
            w = b * g[dn] / g["neet"]
            s.rect(xx, y + 10, w, 44, fill=farge)
            if xx > x0:
                s.line(xx, y + 10, xx, y + 54, stroke="#ffffff", sw=2)
            p = pct(g[dn], g["neet"])
            if w > 38:
                s.text(xx + w / 2, y + 38, f"{nb(p)} %", size=14, fill=TXT, anchor="middle", weight="bold", num=True)
            else:
                s.text(xx + w / 2, y + 72, f"{nb(p)} %", size=14, fill=TXT, anchor="middle", weight="bold", num=True)
            xx += w
    s.text(x0, 300, "Fordeling av de som er utenfor, prosent", size=13, fill=SEK)
    s.lagre(GRAF / "02-topp-C.svg")


def seksjon_d():
    """Forslag til seksjon: hvem er i størst fare? 25–29 år."""
    pts = data["fare_25_29"]
    alle = data["fare_25_29_alle"]
    W, H = 1200, 560
    s = Svg(W, H, tittel="Seksjonsforslag D: hvem er i størst fare")
    s.text(40, 46, "Unge utenfor · 25–29 år · 2025", size=15, fill=SEK, weight="600")
    s.text(40, 86, "Blant unge med bare grunnskole er mange utenfor – og de fleste av dem er på AAP eller uføretrygd",
           size=24, fill=TXT, font=F_TITTEL, weight="bold")
    s.text(40, 114, "Hver sirkel er en gruppe. Arealet viser hvor mange som er utenfor.", size=15, fill=SEK)
    x0, x1, y0, y1 = 110, 900, 160, 490
    X = lambda p: x0 + (x1 - x0) * p / 60  # noqa: E731
    Y = lambda p: y1 - (y1 - y0) * p / 80  # noqa: E731
    for g in range(0, 61, 10):
        s.line(X(g), y0, X(g), y1, stroke=NULL if g == 0 else GRID)
        s.text(X(g), y1 + 20, nb(g), size=13, fill=SEK, anchor="middle")
    for g in range(0, 81, 20):
        s.line(x0, Y(g), x1, Y(g), stroke=NULL if g == 0 else GRID)
        s.text(x0 - 8, Y(g) + 5, nb(g), size=13, fill=SEK, anchor="end")
    s.text(x1, y1 + 42, "Andel av gruppen som er utenfor, prosent", size=13, fill=SEK, anchor="end")
    s.text(x0 - 60, y0 - 18, "Andel av de utenfor som er på AAP eller uføretrygd, prosent", size=13, fill=SEK)
    ra, rb = pct(alle["neet"], alle["bosatte"]), pct(alle["aap_ufore"], alle["neet"])
    s.line(X(ra), y0, X(ra), y1, stroke=SEK, sw=1, dash="4 4")
    s.line(x0, Y(rb), x1, Y(rb), stroke=SEK, sw=1, dash="4 4")
    s.text(X(ra) + 6, y0 + 14, f"Alle 25–29 år: {nb(ra, 1)} prosent", size=13, fill=SEK)
    s.text(x1 - 4, Y(rb) - 6, f"Alle 25–29 år: {nb(rb, 1)} prosent", size=13, fill=SEK, anchor="end")
    farger = {"Ekskl. innvandrere": "#00824d", "Innvandrere": "#1d9de2"}
    maks = max(p["neet"] for p in pts)
    for p in sorted(pts, key=lambda q: -q["neet"]):
        px, py = pct(p["neet"], p["bosatte"]), pct(p["aap_ufore"], p["neet"])
        r = 6 + 26 * (p["neet"] / maks) ** 0.5
        s.circle(X(px), Y(py), r, fill=farger[p["gruppe"]], stroke="#ffffff", sw=1.5)
    # etiketter (plassert for hånd etter første render)
    plass = {("Ekskl. innvandrere", "Grunnskole"): (36, 0, "start"),
             ("Ekskl. innvandrere", "Videregående"): (32, -6, "start"),
             ("Ekskl. innvandrere", "Universitet/høgskole"): (26, -24, "start"),
             ("Ekskl. innvandrere", "Uoppgitt/ingen"): (14, 4, "start"),
             ("Innvandrere", "Grunnskole"): (32, 4, "start"),
             ("Innvandrere", "Videregående"): (-22, -10, "end"),
             ("Innvandrere", "Universitet/høgskole"): (30, 6, "start"),
             ("Innvandrere", "Uoppgitt/ingen"): (14, -12, "start")}
    for p in pts:
        px, py = pct(p["neet"], p["bosatte"]), pct(p["aap_ufore"], p["neet"])
        dx, dy, anc = plass[(p["gruppe"], p["utdanning"])]
        s.text(X(px) + dx, Y(py) + dy, f"{p['utdanning']} ({nb(p['neet'])})", size=13, fill=TXT, anchor=anc, num=True)
    # tegnforklaring til høyre
    lx, ly = 940, 180
    s.text(lx, ly, "Befolkningsgruppe", size=14, fill=TXT, weight="bold")
    for n, (g, f) in enumerate(farger.items()):
        s.circle(lx + 8, ly + 26 + n * 26, 7, fill=f)
        s.text(lx + 22, ly + 31 + n * 26, g, size=14, fill=TXT)
    s.tekstblokk(lx, ly + 100, "Tall i parentes: antall utenfor. Gruppene uoppgitt/ingen utdanning er små.", 30,
                 size=13, fill=SEK, lh=19)
    s.tekstblokk(lx, ly + 196, "Forslag til seksjon. Kan styres av gruppevelgeren (alder, kjønn).", 30,
                 size=13, fill=SEK, lh=19)
    s.text(40, 540, KILDE, size=13, fill=SEK)
    s.lagre(GRAF / "02-seksjon-D.svg")


if __name__ == "__main__":
    for f in (konsept_bred, konsept_smal, topp_a, topp_b, topp_c, seksjon_d):
        f()
    print("ok", json.dumps(data["2025"], ensure_ascii=False))

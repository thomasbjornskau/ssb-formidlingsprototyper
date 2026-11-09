"""Lager konseptgrafikk og toppgrafikkvarianter for ufore (steg 2).
Leser rådata fra data/raw/, skriver data/grafikk-utkast.json, src/konsept-*.svg og docs/grafikk/02-topp-*.svg."""

import itertools, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from grafikk_ufore import *  # noqa: F403

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda *p: os.path.join(ROT, *p)


def les(fil):
    """json-stat2 til {(kode, kode, ...): verdi} i dimensjonsrekkefølge, pluss status."""
    d = json.load(open(R("data", "raw", fil), encoding="utf-8"))
    kat = [d["dimension"][i]["category"] for i in d["id"]]
    nokler = [sorted(c["index"], key=c["index"].get) for c in kat]
    st = d.get("status") or {}
    ut = {}
    for n, k in enumerate(itertools.product(*nokler)):
        ut[k] = d["value"][n]
        if str(n) in st:
            raise SystemExit(f"Statussymbol {st[str(n)]} i {fil} {k}: må tolkes før bruk")
    return d["id"], ut


# ---------- tall ----------
_, t11695 = les("11695.json")      # Region, Kjonn, ContentsCode, Tid
_, t11824 = les("11824.json")      # Bosettingsstatus, ContentsCode, Tid
_, t11828 = les("11828.json")      # Kjonn, Alder, ContentsCode, Tid
_, t11850 = les("11850.json")      # Region, Kjonn, Alder, Intensitet, ContentsCode, Tid
_, t11720 = les("11720.json")
ar = [str(a) for a in range(2015, 2026)]
andel = {a: t11695[("0", "0", "UforetrygdPros", a)] for a in ar}
antall = {a: t11695[("0", "0", "UforetygdPers", a)] for a in ar}
bos = {k: t11824[(k, "UforetrygdPers", "2025")] for k in "012"}
alder = {a: {y: t11828[("0", f"{y:03d}", "UforetrygdPros", a)] for y in range(18, 68)} for a in ("2015", "2025")}
alder_ant = {a: {y: t11828[("0", f"{y:03d}", "UforetrygdPers", a)] for y in range(18, 68)} for a in ("2015", "2025")}
pop = {}
for a, fil in (("2015", "07459_2016.json"), ("2025", "07459_2026.json")):
    _, p = les(fil)   # Region, Kjonn, Alder, ContentsCode, Tid
    for k, v in p.items():
        pop.setdefault(a, {}).setdefault(int(k[2]), 0)
        pop[a][int(k[2])] += v
intens = {a: {i: t11850[("0", "0", "18-67", i, "UforetrygdPros", a)] for i in ("01", "02", "03", "04")} for a in ("2015", "2025")}
grad100 = t11720[("0", "03", "UforetrygdPros", "2025")]

# Dekomponering av endringen i antall 2015-2025 [T]: befolkningsvekst, aldring, endret andel per alder
Y = range(18, 68)
c15, c25 = sum(alder_ant["2015"][y] for y in Y), sum(alder_ant["2025"][y] for y in Y)
p15, p25 = sum(pop["2015"][y] for y in Y), sum(pop["2025"][y] for y in Y)
vekst = (p25 - p15) * c15 / p15
med15rater = sum(alder_ant["2015"][y] / pop["2015"][y] * pop["2025"][y] for y in Y)
aldring = med15rater - c15 - vekst
rater = c25 - med15rater
dek = {"befolkningsvekst": round(vekst), "aldring": round(aldring), "hoyere_andel_per_alder": round(rater), "sum": c25 - c15}
assert abs(sum(v for k, v in dek.items() if k != "sum") - dek["sum"]) <= 2

utkast = {
    "merknad": "Utkast til steg 2. Hentet fra data.ssb.no 09.11.2026. Erstattes av data/raw/ og lag_data.py i steg 3.",
    "andel_18_67": {"kilde": "11695", "verdier": andel},
    "antall_18_67": {"kilde": "11695", "verdier": antall},
    "bosettingsstatus_2025": {"kilde": "11824", "i_alt": bos["0"], "bosatt": bos["1"], "ikke_bosatt": bos["2"]},
    "befolkning_18_67": {"kilde": "07459 (1.1. året etter)", "2015": p15, "2025": p25},
    "nav_arsslutt_2025": {"kilde": "NAV kvartalsstatistikk via SSB-artikkel 23.06.2026", "verdi": 374900},
    "alder_andel": {"kilde": "11828", "verdier": alder},
    "arbeidsintensitet": {"kilde": "11850", "verdier": intens, "koder": {"01": "Ingen", "02": "Lav", "03": "Høy", "04": "Full"}},
    "uforegrad_100_2025": {"kilde": "11720", "verdi": grad100},
    "dekomponering_2015_2025": {"kilde": "11828 og 07459, egen beregning [T]", **dek},
}
json.dump(utkast, open(R("data", "grafikk-utkast.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(dek), andel["2025"], p25)

# ---------- konseptgrafikk ----------
TRINN = [
    ("Vedtak hos NAV",
     "NAV registrerer hvem som har vedtak om uføretrygd, måned for måned. SSB får opplysningene per person.",
     None, None),
    ("Ett år samles",
     "Alle med vedtak minst én måned i året telles, også de som ikke fikk utbetalt fordi de tjente for mye.",
     nb(bos["0"]), "hadde vedtak i 2025"),
    ("Bare bosatte",
     f"De som døde eller flyttet ut i løpet av året, trekkes fra: {nb(bos['2'])} personer.",
     nb(bos["1"]), "uføretrygdede 18–67 år"),
    ("Andel av befolkningen",
     f"Antallet deles på alle bosatte 18–67 år ved årsslutt: {nb(p25)} personer.",
     nb(andel["2025"], 1) + " prosent", "av befolkningen 18–67 år"),
]
KOBLES = [("Alder og bosted", "folkeregisteret, 31.12"), ("Utdanning", "NUDB, 1.10"), ("Arbeid", "a-ordningen, hver måned")]
IKKE = ["Diagnose eller årsak til uførheten", "Hvor mange timer uføre jobber", "Private uføreforsikringer uten vedtak i folketrygden"]
NAVTXT = f"NAV teller bare dem som får utbetalt ved utgangen av perioden: {nb(374900)} ved utgangen av 2025."
KILDE_K = "Kilde: SSB, tabell 11824, 11695 og 07459. Om statistikken, 15.09.2026."


def boks_trinn(s, x, y, b, h, n, t, maks, str_tall):
    tittel, tekst, tall, under = t
    s.rect(x, y, b, h, M1, M2)
    s.rect(x, y, b, 5, G4, rx=0)
    s.markor(x + 26, y + 36, n)
    s.text(x + 48, y + 42, tittel, 18, MELLOM, 700)
    yy = s.text(x + 18, y + 76, bryt(tekst, maks), 15, linjeh=21)
    if tall:
        s.text(x + 18, y + h - 42, tall, str_tall, TITTEL, 700, G4, tall=True)
        s.text(x + 18, y + h - 16, under, 14, farge=GRA_T)


def konsept_bred():
    s = Svg(1200, 560, "Slik lages tallene",
            "Fire trinn fra vedtak hos NAV til andel uføretrygdede i befolkningen 18–67 år.")
    b, g, x0, y0, h = 258, 40, 24, 24, 268
    for i, t in enumerate(TRINN):
        x = x0 + i * (b + g)
        boks_trinn(s, x, y0, b, h, i + 1, t, 29, 34)
        if i < 3:
            s.pil(x + b + 8, y0 + h / 2, x + b + g - 8, y0 + h / 2)
    # koblinger
    y = 320
    s.rect(24, y, 1152, 74, G1, G2)
    s.text(42, y + 30, "Kobles med", 16, MELLOM, 700)
    s.text(42, y + 54, "for å fordele tallene", 14, farge=GRA_T)
    for i, (a, b_) in enumerate(KOBLES):
        x = 250 + i * 310
        s.text(x, y + 30, a, 16, BROD, 600)
        s.text(x, y + 54, b_, 14, farge=GRA_T)
    # NAV og ikke med
    y = 416
    s.rect(24, y, 560, 120, HVIT, M5)
    s.text(42, y + 32, "Hvorfor NAV har et lavere tall", 17, MELLOM, 700)
    s.text(42, y + 60, bryt(NAVTXT, 64), 15, linjeh=21)
    s.text(42, y + 108, "Begge tallene er riktige. De svarer på ulike spørsmål.", 14, farge=GRA_T)
    s.rect(616, y, 560, 120, GRA_F, GRA_S, stiplet=True)
    s.text(634, y + 32, "Ikke med i statistikken", 17, MELLOM, 700, GRA_T)
    for i, l in enumerate(IKKE):
        s.text(634, y + 60 + i * 22, "– " + l, 15, farge=GRA_T)
    s.text(1176, 556, KILDE_K, 12, farge=GRA_T, anker="end")
    s.lagre(R("src", "konsept-bred.svg"))


def konsept_smal():
    b, x0 = 342, 24
    h = 196
    s = Svg(390, 24 + 4 * (h + 36) + 380, "Slik lages tallene",
            "Fire trinn fra vedtak hos NAV til andel uføretrygdede i befolkningen 18–67 år.")
    y = 24
    for i, t in enumerate(TRINN):
        hh = 140 if t[2] is None else h
        boks_trinn(s, x0, y, b, hh, i + 1, t, 38, 30)
        y += hh
        if i < 3:
            s.pil(x0 + b / 2, y + 6, x0 + b / 2, y + 30)
            y += 36
    y += 20
    s.rect(x0, y, b, 132, G1, G2)
    s.text(x0 + 16, y + 28, "Kobles med", 16, MELLOM, 700)
    for i, (a, b_) in enumerate(KOBLES):
        s.text(x0 + 16, y + 56 + i * 24, f"{a}: {b_}", 14)
    y += 152
    s.rect(x0, y, b, 176, HVIT, M5)
    s.text(x0 + 16, y + 28, "Hvorfor NAV har et lavere tall", 16, MELLOM, 700)
    yy = s.text(x0 + 16, y + 54, bryt(NAVTXT, 40), 14, linjeh=20)
    s.text(x0 + 16, yy + 30, bryt("Begge tallene er riktige. De svarer på ulike spørsmål.", 44), 14, farge=GRA_T, linjeh=20)
    y += 196
    s.rect(x0, y, b, 142, GRA_F, GRA_S, stiplet=True)
    s.text(x0 + 16, y + 28, "Ikke med i statistikken", 16, MELLOM, 700, GRA_T)
    yy = y + 54
    for l in IKKE:
        yy = s.text(x0 + 16, yy, bryt("– " + l, 42), 14, farge=GRA_T, linjeh=19) + 23
    s.h = y + 142 + 40
    s.text(x0, s.h - 14, bryt(KILDE_K, 56), 12, farge=GRA_T, linjeh=15)
    s.h += 16
    s.lagre(R("src", "konsept-smal.svg"))


# ---------- toppgrafikk ----------
def topp_ramme(s, etikett, stort, setning, linjer, kilde):
    s.text(40, 46, etikett.upper(), 14, BROD, 600, GRA_T)
    s.text(40, 112, stort, 60, TITTEL, 700, G4, tall=True)
    yy = s.text(40, 150, bryt(setning, 50), 19, BROD, 600, TEKST, linjeh=26)
    yy += 34
    for l in linjer:
        yy = s.text(40, yy, bryt(l, 58), 15, farge=TEKST, linjeh=21) + 27
    s.text(1160, 318, kilde, 12, farge=GRA_T, anker="end")


def yakse(s, x0, x1, y_av, verdier, fmt, tittel, ytit):
    for v in verdier:
        y = y_av(v)
        s.line(x0, y, x1, y, STOTTE)
        s.text(x0 - 8, y + 5, fmt(v), 13, anker="end", farge=GRA_T, tall=True)
    s.text(x0 - 8, ytit, tittel, 13, farge=GRA_T, anker="start")


def topp_a():
    s = Svg(1200, 330, "Toppgrafikk A",
            "Andelen uføretrygdede har ligget på 10,7 prosent siden 2021, mens antallet har økt med 61 000 siden 2015.")
    topp_ramme(s, "Uføretrygdede · 2015–2025", "389 000",
               "personer 18–67 år var uføretrygdet i 2025. Andelen har stått nesten stille i fem år.",
               [f"Antallet har økt med {nb(round(dek['sum'], -3))} siden 2015.",
                "Litt over halvparten av økningen skyldes at befolkningen har vokst og blitt eldre."],
               "Kilde: SSB, tabell 11695, 11828 og 07459. Sist oppdatert: 02.09.2026. Dekomponering: egen beregning.")
    # linje: andel
    x0, x1, yt, yb = 620, 1150, 64, 150
    lo, hi = 9, 11.5
    ya = lambda v: yb - (v - lo) / (hi - lo) * (yb - yt)
    xa = lambda i: x0 + i * (x1 - x0) / 10
    yakse(s, x0, x1, ya, [10, 11], lambda v: nb(v), "prosent", 44)
    s.text(x1, 44, "Andel av befolkningen 18–67 år", 13, farge=GRA_T, anker="end")
    pk = [(xa(i), ya(andel[a])) for i, a in enumerate(ar)]
    s.polyline(pk, G4, 2.5)
    for i in (0, 10):
        s.circle(*pk[i], 4, G4)
    s.text(pk[0][0] + 6, pk[0][1] + 20, nb(andel["2015"], 1), 13, BROD, 600, tall=True)
    s.text(pk[10][0], pk[10][1] - 10, nb(andel["2025"], 1), 13, BROD, 600, anker="end", tall=True)
    for i in (0, 5, 10):
        s.text(xa(i), yb + 18, ar[i], 13, farge=GRA_T, anker="middle", tall=True)
    # stablet stolpe: dekomponering
    yb2 = 214
    s.text(x0, yb2 - 14, "Hva økningen i antall består av, 2015–2025", 13, farge=GRA_T)
    deler = [("Befolkningsvekst", dek["befolkningsvekst"], "#5763a6"),
             ("Aldring", dek["aldring"], "#d5a640"),
             ("Høyere andel i hver alder", dek["hoyere_andel_per_alder"], "#339b71")]
    tot = dek["sum"]
    x = x0
    for i, (navn, v, f) in enumerate(deler):
        b = v / tot * (x1 - x0)
        s.rect(x, yb2, b - 2, 34, f, rx=0)
        s.text(x + 8, yb2 + 23, "+" + nb(v), 14, BROD, 600, HVIT if i != 1 else TEKST, tall=True)
        s.text(x, yb2 + 56, bryt(navn, 16 if b < 150 else 30), 13, linjeh=17)
        x += b
    s.lagre(R("docs", "grafikk", "02-topp-A.svg"))


def topp_b():
    s = Svg(1200, 330, "Toppgrafikk B",
            "Andelen uføretrygdede etter alder: doblet blant de unge, lavere blant de eldste, 2015 mot 2025.")
    topp_ramme(s, "Uføretrygdede etter alder · 2015 og 2025", "Over 4 av 100",
               "29-åringer var uføretrygdet i 2025. Andelen er dobbelt så høy som i 2015.",
               [f"Blant 67-åringer falt andelen fra {nb(alder['2015'][67], 1)} til {nb(alder['2025'][67], 1)} prosent.",
                "Den samlede andelen skjuler at unge og eldste har gått hver sin vei."],
               "Kilde: SSB, tabell 11828. Sist oppdatert: 02.09.2026.")
    x0, x1, yt, yb = 620, 1130, 56, 270
    ya = lambda v: yb - v / 35 * (yb - yt)
    xa = lambda a: x0 + (a - 18) / 49 * (x1 - x0)
    yakse(s, x0, x1, ya, [0, 10, 20, 30], lambda v: nb(v), "prosent", 40)
    s.line(x0, yb, x1, yb, NULL)
    for a in (18, 30, 40, 50, 60, 67):
        s.text(xa(a), yb + 20, str(a), 13, farge=GRA_T, anker="middle", tall=True)
    s.text(x0 - 22, yb + 20, "alder", 13, farge=GRA_T, anker="end")
    for ar_, f, sb in (("2015", NULL, 2), ("2025", G4, 2.5)):
        s.polyline([(xa(a), ya(alder[ar_][a])) for a in Y], f, sb)
    s.text(xa(67) + 6, ya(alder["2015"][67]) + 5, "2015", 13, BROD, 600, GRA_T)
    s.text(xa(67) + 6, ya(alder["2025"][67]) + 5, "2025", 13, BROD, 600, G4)
    # markering 29 år
    for ar_, f in (("2015", NULL), ("2025", G4)):
        s.circle(xa(29), ya(alder[ar_][29]), 4, f)
    s.line(xa(29), ya(alder["2025"][29]) - 8, xa(29), ya(12), GRA_L)
    s.text(xa(29) - 4, ya(12) - 22, "29 år:", 13, BROD, 600, anker="middle")
    s.text(xa(29) - 4, ya(12) - 6, f"{nb(alder['2015'][29], 1)} → {nb(alder['2025'][29], 1)}", 13, anker="middle", tall=True)
    s.lagre(R("docs", "grafikk", "02-topp-B.svg"))


def topp_c():
    s = Svg(1200, 330, "Toppgrafikk C",
            "Tre av fire uføretrygdede hadde ikke lønnsarbeid noen av månedene de var uføre, både i 2015 og 2025.")
    topp_ramme(s, "Uføretrygdede og arbeid · 2025", "3 av 4",
               "uføretrygdede hadde ikke lønnsarbeid noen av månedene de var uføre i 2025.",
               ["1 av 7 hadde lønnsarbeid i alle månedene, men målet teller måneder, ikke timer.",
                f"{nb(grad100, 0)} prosent har 100 prosent uføregrad."],
               "Kilde: SSB, tabell 11850 og 11720. Sist oppdatert: 02.09.2026.")
    x0, x1 = 680, 1150
    farger = {"01": "#cff1d0", "02": "#91cd9a", "03": "#58a772", "04": "#00824d"}
    navn = {"01": "Ingen", "02": "Lav", "03": "Høy", "04": "Full"}
    s.text(x0, 44, "Andel av månedene som uføre med lønnsarbeid. Prosent", 13, farge=GRA_T)
    for j, ar_ in enumerate(("2015", "2025")):
        y = 92 + j * 96
        s.text(x0 - 12, y + 30, ar_, 15, BROD, 600, anker="end", tall=True)
        x = x0
        for k in ("01", "02", "03", "04"):
            v = intens[ar_][k]
            b = v / 100 * (x1 - x0)
            s.rect(x, y, b - 2, 46, farger[k], "#91cd9a" if k == "01" else None, rx=0)
            if k in ("01", "04"):
                s.text(x + b / 2, y + 30, nb(v, 1), 15, BROD, 600, HVIT if k == "04" else TEKST, "middle", tall=True)
            else:
                s.text(x + b / 2 - 1, y + 64, nb(v, 1), 13, anker="middle", tall=True)
            if j == 0:
                s.text(x + b / 2 - 1, y - 10, navn[k], 13, BROD, 600, anker="middle")
            x += b
    s.text(x0, 272, bryt("Ingen = ingen måneder med lønnsarbeid. Lav = under halvparten. Høy = over halvparten. Full = alle månedene.", 72), 13, farge=GRA_T, linjeh=17)
    s.lagre(R("docs", "grafikk", "02-topp-C.svg"))


os.makedirs(R("src"), exist_ok=True)
os.makedirs(R("docs", "grafikk"), exist_ok=True)
konsept_bred(); konsept_smal(); topp_a(); topp_b(); topp_c()
print("ferdig")

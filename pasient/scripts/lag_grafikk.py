"""Lager konseptgrafikken og toppgrafikkutkastene for pasient (steg 2).

Tall fra data/grafikk-utkast.json og data/raw/folkemengde.json (07459, hentet 02.11.2026).
"""
import json
import os
import sys

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROT, "scripts"))
from grafikk_pasient import (  # noqa: E402
    Svg, nb, sgn, bryt, MORK, BLEKK, GRA_TEKST, LINJE, BG_FLATE, BG_KANT,
    GRONN, GRONN_BG, GRA, GRA_BG, STOTTE, NULL,
)

D = json.load(open(os.path.join(ROT, "data", "grafikk-utkast.json"), encoding="utf-8"))
S = D["somatikk"]
AAR = D["aar"]
DIAG = D["diagnosekapittel_2025"]
ALD = D["alder"]

BLA, OKER, ROSA = "#1d9de2", "#c78800", "#c775a7"
BLA_F, OKER_F = "#3face6", "#d5a640"
GRONN_F = "#339b71"

ETIKETT = "PASIENTER I SPESIALISTHELSETJENESTEN"
SIST = "Sist oppdatert: 22.06.2026."


# ---------- Avledede tall ----------
def middelfolkemengde():
    """Snitt av folkemengden 1. januar i året og året etter, per aldersgruppe (07459)."""
    f = json.load(open(os.path.join(ROT, "data", "raw", "folkemengde.json"), encoding="utf-8"))
    aldre = list(f["dimension"]["Alder"]["category"]["index"])
    tider = list(f["dimension"]["Tid"]["category"]["index"])
    v = f["value"]  # rekkefølge: Alder, ContentsCode (1), Tid
    verdi = lambda a, t: v[aldre.index(a) * len(tider) + tider.index(t)]
    alder = lambda a: 105 if a.startswith("105") else int(a)
    ut = {}
    for aar in ("2015", "2025"):
        neste = str(int(aar) + 1)
        ut[aar] = [sum((verdi(a, aar) + verdi(a, neste)) / 2 for a in aldre if lo <= alder(a) <= hi)
                   for lo, hi in ALD["grenser"]]
    return ut


MF = middelfolkemengde()
P15, P25 = ALD["pasienter_2015"], ALD["pasienter_2025"]
RATE15 = [p / m for p, m in zip(P15, MF["2015"])]
RATE25 = [p / m for p, m in zip(P25, MF["2025"])]
TOT15, TOT25 = sum(P15), sum(P25)
BEF15, BEF25 = sum(MF["2015"]), sum(MF["2025"])
# Dekomponering: først folketallet, så alderssammensetningen, så bruken per aldersgruppe.
STR = TOT15 * BEF25 / BEF15 - TOT15
ALDRING = sum(r * m for r, m in zip(RATE15, MF["2025"])) - TOT15 - STR
BRUK = TOT25 - TOT15 - STR - ALDRING

SUM_KAP = sum(v[2] for v in DIAG.values())


def indeks(serie):
    return [v / serie[0] * 100 for v in serie]


# ---------- Konseptgrafikk ----------
TRINN = [
    ("Behandlingen registreres",
     "Sykehus, private institusjoner med avtale og avtalespesialister rapporterer hver kontakt til Norsk pasientregister.",
     f"{nb(S['kontakter_poliklinikk'][-1])} polikliniske kontakter i 2025"),
    ("Koblet til person",
     "SSB kobler kontaktene til befolkningsregisteret. Kontakter uten gyldig fødsels- eller D-nummer faller ut.",
     f"{nb(S['kontakter_uten_personnummer']['2025'])} kontakter uten personnummer"),
    ("Kontakter blir pasienter",
     "Hver person telles én gang, uansett hvor mange kontakter eller innleggelser den har hatt.",
     f"{nb(S['pasienter'][-1])} pasienter i 2025"),
    ("Én gang per gruppe",
     "En person med to diagnoser telles i begge. Gruppene summerer derfor til mer enn totalen.",
     f"Diagnosekapitlene: {nb(SUM_KAP / 1e6, 2)} mill."),
    ("Avrundet og satt i forhold",
     "Pasienttall avrundes til nærmeste tall delelig med 3. Rater regnes per 1 000 innbyggere.",
     f"{S['pasienter_per_1000']['2025']} per 1 000 innbyggere"),
]
IKKE_MED = ("Ikke med: psykisk helsevern for barn og unge · tverrfaglig rusbehandling · "
            "fastlege og kommunale tjenester · ventetid og kostnader")
KILDE_K = ("Kilde: SSB, Om statistikken for Pasienter i spesialisthelsetjenesten (19.06.2026); "
           "tabell 14824 og 14827. Tallene gjelder somatikk, 2025.")
UNDERTITTEL = "Fra behandling i spesialisthelsetjenesten til tallene i statistikken"


def konsept_bred(sti):
    B = 1200
    n = len(TRINN)
    gap = 28
    bredde = (B - 80 - gap * (n - 1)) / n
    y0 = 122

    def maal(overskrift, tekst, tall):
        o, t, z = bryt(overskrift, 15), bryt(tekst, 23), bryt(tall, 24)
        topp = max(27 + len(o) * 20, 62) + 10
        midt = len(t) * 19 + 12
        bunn = 18 + len(z) * 17 + 10
        return o, t, z, topp, midt, bunn

    m = [maal(*tr) for tr in TRINN]
    hboks = max(topp + midt + bunn for *_, topp, midt, bunn in m)
    H = y0 + hboks + 22 + 40 + 38
    s = Svg(B, H, "Slik lages tallene")
    s.tekst(40, 50, "Slik lages tallene", 28, MORK, 700)
    s.tekst(40, 80, UNDERTITTEL, 17, GRA_TEKST)
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
    blokker = [(bryt(o, 30), bryt(t, 38), bryt(z, 36)) for o, t, z in TRINN]
    hoyde = lambda o, t, z: 32 + len(o) * 21 + 4 + len(t) * 19 + 6 + len(z) * 17
    H = 110
    for o, t, z in blokker:
        H += hoyde(o, t, z) + 28
    ikke = bryt(IKKE_MED, 46)
    kilde = bryt(KILDE_K, 58)
    und = bryt(UNDERTITTEL, 44)
    H += len(ikke) * 18 + 30 + len(kilde) * 15 + 20 + (len(und) - 1) * 19
    s = Svg(B, H, "Slik lages tallene")
    s.tekst(16, 38, "Slik lages tallene", 24, MORK, 700)
    yy = s.tekstlinjer(16, 64, und, 15, GRA_TEKST, lh=19)
    s.linje(16, yy - 5, B - 16, yy - 5, LINJE)
    y = yy + 13
    for i, (o, t, z) in enumerate(blokker):
        hb = hoyde(o, t, z)
        s.rect(16, y, B - 32, hb, BG_FLATE, BG_KANT)
        s.markor(40, y + 26, str(i + 1))
        ya = s.tekstlinjer(66, y + 32, o, 16, BLEKK, 700, lh=21)
        ya = s.tekstlinjer(66, ya + 4, t, 14, MORK, lh=19)
        s.tekstlinjer(66, ya + 6, z, 13, GRONN, 700, lh=17)
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
    y = s.tekstlinjer(40, 150, bryt(setning, 52), 20, MORK, lh=26) + 10
    for l in linjer:
        y = s.tekstlinjer(40, y, bryt(l, 64), 15, GRA_TEKST, lh=21) + 4
    s.tekst(40, 312, kilde, 12, GRA_TEKST)
    return s


def topp_a(sti):
    """Hvor mange, og hva får de? Indeks 2015 = 100."""
    vekst = lambda k: round((S[k][-1] / S[k][0] - 1) * 100)
    s = topp_ramme(
        "Toppgrafikk A: flere pasienter, ikke flere innleggelser", "SOMATIKK 2015–2025",
        "2,7 millioner",
        f"fikk somatisk behandling i 2025, {vekst('pasienter')} prosent flere enn i 2015.",
        [f"Veksten er poliklinisk: {vekst('kontakter_poliklinikk')} prosent flere kontakter, "
         "men like mange innleggelser som i 2015.",
         f"Oppholdsdøgnene på sykehus er {abs(vekst('oppholdsdogn'))} prosent færre."],
        f"Kilde: SSB, tabell 14824. {SIST}")
    x0, x1, y0, y1 = 690, 1020, 70, 268
    vmin, vmax = 85, 130
    n = len(AAR)
    fx = lambda i: x0 + (x1 - x0) * i / (n - 1)
    fy = lambda v: y1 - (y1 - y0) * (v - vmin) / (vmax - vmin)
    s.tekst(x0 - 36, y0 - 16, "indeks, 2015 = 100", 13, GRA_TEKST)
    for v in (90, 100, 110, 120, 130):
        s.linje(x0, fy(v), x1, fy(v), NULL if v == 100 else STOTTE, 1.2 if v == 100 else 1)
        s.tekst(x0 - 8, fy(v) + 4, str(v), 12, GRA_TEKST, anker="end")
    for i, a in enumerate(AAR):
        if a in (2015, 2020, 2025):
            s.tekst(fx(i), y1 + 18, str(a), 12, GRA_TEKST, anker="middle")
    i20 = AAR.index(2020)
    s.linje(fx(i20), y0, fx(i20), y1, STOTTE, 1, stiplet=True)
    s.tekst(fx(i20) + 5, y0 + 10, "Korona", 12, GRA_TEKST)
    serier = [("kontakter_poliklinikk", "Polikliniske kontakter", GRONN),
              ("pasienter", "Pasienter", BLA),
              ("dognopphold", "Døgnopphold", OKER),
              ("oppholdsdogn", "Oppholdsdøgn", ROSA)]
    for k, navn, farge in serier:
        ind = indeks(S[k])
        s.polyline([(fx(i), fy(v)) for i, v in enumerate(ind)], farge, 2.5)
        s.sirkel(fx(n - 1), fy(ind[-1]), 4, farge)
        s.tekst(x1 + 10, fy(ind[-1]) + 1, navn, 13, MORK, 700)
        s.tekst(x1 + 10, fy(ind[-1]) + 16, nb(ind[-1]), 12, MORK)
    s.lagre(sti)


def topp_b(sti):
    """Hva behandles de for? Diagnosekapitler 2025."""
    z = DIAG["XXI"][2]
    s = topp_ramme(
        "Toppgrafikk B: største diagnosegruppe", "SOMATIKK 2025",
        f"{nb(round(z, -3))}",
        "pasienter var til kontroll, oppfølging eller annen kontakt (Z-kapitlet). "
        "Det er den største diagnosegruppen.",
        ["Samme person kan stå i flere kapitler. Kapitlene summerer til "
         f"{nb(SUM_KAP / 1e6, 1)} millioner, nesten dobbelt så mange som pasientene."],
        f"Kilde: SSB, tabell 14824. {SIST}")
    rader = sorted([(k, v) for k, v in DIAG.items() if k != "zz1"], key=lambda kv: -kv[1][2])[:8]
    xa, y0 = 870, 66
    plot_b = 220
    h_st, luft = 18, 9
    maks = 800_000
    s.tekst(xa, y0 - 12, "pasienter, tusen", 13, GRA_TEKST)
    ybunn = y0 + len(rader) * (h_st + luft) - luft
    for t in (0, 200_000, 400_000, 600_000, 800_000):
        x = xa + plot_b * t / maks
        s.linje(x, y0 - 4, x, ybunn + 4, STOTTE)
        s.tekst(x, ybunn + 18, nb(t / 1000), 12, GRA_TEKST, anker="middle")
    for i, (k, (kode, navn, v)) in enumerate(rader):
        y = y0 + i * (h_st + luft)
        farge = GRONN if k == "XXI" else GRA
        s.rect(xa, y, plot_b * v / maks, h_st, farge)
        s.tekst(xa - 8, y + 14, f"{navn} ({kode.split('–')[0][0]})", 13,
                MORK, 700 if k == "XXI" else 400, "end")
        s.tekst(xa + plot_b * v / maks + 6, y + 14, nb(round(v / 1000)), 13, MORK, 700 if k == "XXI" else 400)
    s.linje(xa, y0 - 4, xa, ybunn + 4, NULL, 1.2)
    s.tekst(xa - 8, ybunn + 36, "De åtte største av 20 kapitler", 12, GRA_TEKST, anker="end")
    s.lagre(sti)


def topp_c(sti):
    """Hvem er pasientene? Hva driver veksten 2015–2025."""
    tot = TOT25 - TOT15
    andel = lambda x: round(x / tot * 100)
    s = topp_ramme(
        "Toppgrafikk C: hva driver veksten", "SOMATIKK 2015–2025",
        f"{sgn(round(tot, -3))}",
        "flere pasienter fra 2015 til 2025. Halvparten fordi vi er flere innbyggere.",
        [f"En femdel fordi befolkningen er eldre. Resten fordi alle aldersgrupper "
         f"bruker mer: blant 80–89-åringene fra {round(RATE15[5] * 1000)} til "
         f"{round(RATE25[5] * 1000)} per 1 000.",
         "Egen beregning med SSBs folketall. Ikke publisert av SSB."],
        f"Kilde: SSB, tabell 14824 og 07459. Egen beregning. {SIST}")
    deler = [("Flere innbyggere", STR, GRONN_F, GRONN),
             ("Eldre befolkning", ALDRING, BLA_F, BLA),
             ("Mer bruk per person", BRUK, OKER_F, OKER)]
    # Tre liggende stolper fra null, felles skala
    xa, plot_b = 820, 190
    y0, h_st, luft = 70, 22, 11
    maks = 200_000
    s.tekst(xa, y0 - 12, "økning i antall pasienter, 2015–2025", 13, GRA_TEKST)
    ybunn = y0 + len(deler) * (h_st + luft) - luft
    for t in (0, 100_000, 200_000):
        x = xa + plot_b * t / maks
        s.linje(x, y0 - 4, x, ybunn + 4, STOTTE)
        s.tekst(x, ybunn + 18, nb(t), 12, GRA_TEKST, anker="middle")
    for i, (navn, v, _, _) in enumerate(deler):
        y = y0 + i * (h_st + luft)
        s.rect(xa, y, plot_b * v / maks, h_st, GRONN)
        s.tekst(xa - 8, y + 16, navn, 13, MORK, 400, "end")
        s.tekst(xa + plot_b * v / maks + 6, y + 16,
                f"{sgn(round(v, -3))} ({andel(v)} prosent)", 13, MORK, 700)
    s.linje(xa, y0 - 4, xa, ybunn + 4, NULL, 1.2)
    # Rater per aldersgruppe, liten tabell under
    yt = ybunn + 54
    xt, kol = 740, 64
    s.tekst(xt - 50, yt - 4, "pasienter per 1 000 innbyggere", 13, GRA_TEKST)
    for i, g in enumerate(ALD["grupper"]):
        cx = xt + kol * i + kol / 2
        s.tekst(cx, yt + 16, g, 12, GRA_TEKST, 400, "middle")
        s.tekst(cx, yt + 34, str(round(RATE15[i] * 1000)), 13, MORK, 400, "middle")
        s.tekst(cx, yt + 52, str(round(RATE25[i] * 1000)), 13, MORK, 700, "middle")
    s.tekst(xt - 2, yt + 34, "2015", 12, GRA_TEKST, anker="end")
    s.tekst(xt - 2, yt + 52, "2025", 12, GRA_TEKST, 700, "end")
    s.lagre(sti)


if __name__ == "__main__":
    konsept_bred(os.path.join(ROT, "src", "konsept-bred.svg"))
    konsept_smal(os.path.join(ROT, "src", "konsept-smal.svg"))
    topp_a(os.path.join(ROT, "docs", "grafikk", "02-topp-a.svg"))
    topp_b(os.path.join(ROT, "docs", "grafikk", "02-topp-b.svg"))
    topp_c(os.path.join(ROT, "docs", "grafikk", "02-topp-c.svg"))
    print(f"Dekomponering: tot {TOT25 - TOT15:.0f}, folketall {STR:.0f}, aldring {ALDRING:.0f}, bruk {BRUK:.0f}")
    print("Sum kapitler", SUM_KAP)
    print("ferdig")

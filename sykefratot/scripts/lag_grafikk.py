"""Lager konseptgrafikken og tre toppgrafikkvarianter for sykefratot (steg 2).

Leser data/grafikk-utkast.json. Skriver src/konsept-bred.svg, src/konsept-smal.svg
og docs/grafikk/02-topp-{a,b,c}.svg.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from grafikk_sykefratot import (Svg, nb, bryt, SANS, ROBOTO, COND, M5, M2, M1, G4, G1, GRA_TEKST,
                     GRA, GRA_FLATE, TEKST, STOTTE, NULL, GRONN5, LINJE)

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROT, "data", "grafikk-utkast.json"), encoding="utf-8"))
S, SER, VAR, PER = D["siste"], D["serie_12439"], D["varighet_12946"], D["personer_12446"]
OPPDATERT = "26.11.2026"

# ---------------------------------------------------------------- innhold
KILDER = [
    ("Navs sykmeldingsregister", "Alle legemeldte sykmeldinger"),
    ("SSBs utvalgsundersøkelse", "Egenmeldinger fra om lag 10\u00a0000 bedrifter"),
    ("A-ordningen", "Jobber, stillingsprosent og avtalt arbeidstid"),
]
T2 = ("Hver arbeidsdag med fravær teller, vektet med stillingsprosent og sykmeldingsgrad.")
T3 = ("Avtalte dagsverk er arbeidsdagene folk har avtalt å jobbe, justert for stillingsprosent. "
      "Prosenten måler dagsverk, ikke hvor mange som er syke.")
T4 = ("Sommeren gir alltid lavere fravær enn vinteren. Sesongjusteringen fjerner det faste mønsteret, "
      "så kvartalene kan sammenlignes. Tallene revideres ved hver publisering.")
IKKE_MED = ["Fravær for barns sykdom", "Foreldre- og omsorgspermisjon",
            "Selvstendig næringsdrivende", "Vernepliktige", "Diagnoser (publiseres av Nav)"]
TRINN = ["Tre kilder", "Tell tapte dagsverk", "Del på avtalte dagsverk", "Sesongjuster"]
MLN = nb(S["dagsverk_ujustert"] / 1e6, 2)
KILDELINJE = f"Kilde: SSB, tabell 12439 og Om statistikken. Sist oppdatert: {OPPDATERT}."


def eksempelboks(s, x, y, w):
    s.rect(x, y, w, 100, fill="#ffffff", stroke=M2, rx=2)
    s.text(x + 14, y + 26, "50 prosent sykmeldt i", 15)
    s.text(x + 14, y + 46, "80 prosent stilling:", 15)
    s.text(x + 14, y + 68, "0,5 × 0,8 = 0,4 dagsverk per dag", 15, weight=600)
    s.text(x + 14, y + 88, "Eksempeltall, ikke statistikk", 14, fill=GRA_TEKST)
    return y + 100


def broek(s, x, y, w):
    s.text(x + w / 2, y, f"{MLN} millioner tapte dagsverk", 15, weight=600, anchor="middle")
    s.line(x + 10, y + 12, x + w - 10, y + 12, M5, 1.5)
    s.text(x + w / 2, y + 34, "alle avtalte dagsverk", 15, weight=600, anchor="middle")
    s.text(x + w / 2, y + 80, f"= {nb(S['ujustert'])} prosent", 30, weight=700, anchor="middle", font=COND)
    return y + 90


def sesongfigur(s, x, y, w, h):
    """Ujustert mot sesongjustert, siste sju kvartaler."""
    tid = SER["tid"][-7:]
    u, sj = SER["ujustert"][-7:], SER["sesongjustert"][-7:]
    lo, hi = 5, 8
    X = lambda i: x + 10 + i * (w - 110) / (len(tid) - 1)
    Y = lambda v: y + h - (v - lo) / (hi - lo) * h
    for v in (5, 6, 7, 8):
        s.line(x, Y(v), x + w - 100, Y(v), STOTTE, 1)
        s.text(x - 6, Y(v) + 5, str(v), 14, fill=GRA_TEKST, anchor="end")
    s.text(x - 6, y - 14, "prosent", 14, fill=GRA_TEKST, anchor="start")
    s.polyline([(X(i), Y(v)) for i, v in enumerate(u)], stroke=GRA, sw=2)
    s.polyline([(X(i), Y(v)) for i, v in enumerate(sj)], stroke=G4, sw=2.5)
    for i, v in enumerate(u):
        s.circle(X(i), Y(v), 3, GRA)
    xe = X(len(tid) - 1)
    s.text(xe + 10, Y(sj[-1]) - 2, nb(sj[-1], 2), 15, weight=700)
    s.text(xe + 10, Y(sj[-1]) + 15, "sesongjustert", 14, fill=GRA_TEKST)
    s.text(xe + 10, Y(u[-1]) + 4, nb(u[-1]), 15, weight=700)
    s.text(xe + 10, Y(u[-1]) + 21, "ujustert", 14, fill=GRA_TEKST)
    for i, t in enumerate(tid):
        if t.endswith("K1"):
            s.text(X(i), y + h + 20, t[:4], 14, fill=GRA_TEKST, anchor="middle")
    return y + h + 24


def ikke_med(s, x, y, w, smal=False):
    if smal:
        h = 40 + 22 * len(IKKE_MED)
        s.rect(x, y, w, h, fill=GRA_FLATE, stroke=GRA, rx=2, dash="5,4")
        s.text(x + 14, y + 26, "Ikke med i statistikken", 15, weight=700, font=ROBOTO, fill=GRA_TEKST)
        for i, t in enumerate(IKKE_MED):
            s.text(x + 14, y + 50 + i * 22, "– " + t, 15, fill=GRA_TEKST)
        return y + h
    h = 64
    s.rect(x, y, w, h, fill=GRA_FLATE, stroke=GRA, rx=2, dash="5,4")
    s.text(x + 16, y + 26, "Ikke med i statistikken", 15, weight=700, font=ROBOTO, fill=GRA_TEKST)
    s.text(x + 16, y + 49, "  ·  ".join(IKKE_MED), 15, fill=GRA_TEKST)
    return y + h


# ---------------------------------------------------------------- konsept, bred
def konsept_bred():
    s = Svg(1200, 600, "Slik lages tallene: sykefraværsprosenten i fire trinn")
    s.text(40, 46, "Slik lages tallene", 30, weight=700, font=COND)
    s.text(40, 74, "Sykefraværsprosenten for 3. kvartal 2026, i fire trinn", 16, fill=GRA_TEKST)
    s.line(40, 92, 1160, 92, M2, 1)
    W, GAP, X0, YM = 250, 40, 40, 128
    xs = [X0 + i * (W + GAP) for i in range(4)]
    for i, x in enumerate(xs):
        s.markor(x + 15, YM, i + 1)
        s.text(x + 40, YM + 6, TRINN[i], 18, weight=700, font=ROBOTO)
        if i < 3:
            s.pil(x + W + 6, YM, xs[i + 1] - 6, YM)
    y0 = YM + 36
    # 1
    for j, (n, t) in enumerate(KILDER):
        y = y0 + j * 84
        s.rect(xs[0], y, W, 72, fill=G1, stroke=G4, rx=2)
        s.text(xs[0] + 14, y + 26, n, 15, weight=700)
        s.lines(xs[0] + 14, y + 48, bryt(t, 30), 14, lh=19)
    # 2
    y = s.lines(xs[1], y0 + 14, bryt(T2, 31), 15, lh=21)
    y = eksempelboks(s, xs[1], y + 6, W)
    s.text(xs[1], y + 46, f"{MLN} millioner", 30, weight=700, font=COND)
    s.lines(xs[1], y + 70, ["tapte dagsverk i 3. kvartal 2026,", "ikke sesongjustert"], 15, lh=20)
    # 3
    y = broek(s, xs[2], y0 + 22, W)
    s.lines(xs[2], y + 22, bryt(T3, 31), 15, lh=21)
    # 4
    y = sesongfigur(s, xs[3] + 26, y0 + 30, W - 26, 108)
    s.lines(xs[3], y + 26, bryt(T4, 31), 15, lh=21)
    ikke_med(s, 40, 484, 1120)
    s.text(40, 580, KILDELINJE, 14, fill=GRA_TEKST)
    return s


# ---------------------------------------------------------------- konsept, smal
def konsept_smal():
    W, X = 350, 20
    s = Svg(390, 1700, "Slik lages tallene: sykefraværsprosenten i fire trinn")
    s.text(X, 40, "Slik lages tallene", 28, weight=700, font=COND)
    y = s.lines(X, 66, ["Sykefraværsprosenten for 3. kvartal", "2026, i fire trinn"], 16, lh=22, fill=GRA_TEKST)
    s.line(X, y, X + W, y, M2, 1)
    y += 34

    def hode(n, y):
        s.markor(X + 15, y, n)
        s.text(X + 40, y + 6, TRINN[n - 1], 18, weight=700, font=ROBOTO)
        return y + 30

    def pil_ned(y):
        s.pil(X + 15, y + 8, X + 15, y + 40)
        return y + 62

    y = hode(1, y)
    for n, t in KILDER:
        ll = bryt(t, 40)
        h = 52 + 19 * (len(ll) - 1)
        s.rect(X, y, W, h, fill=G1, stroke=G4, rx=2)
        s.text(X + 14, y + 24, n, 15, weight=700)
        s.lines(X + 14, y + 44, ll, 14, lh=19)
        y += h + 10
    y = pil_ned(y - 6)
    y = hode(2, y)
    y = s.lines(X, y + 8, bryt(T2, 44), 15, lh=21)
    y = eksempelboks(s, X, y + 4, W)
    s.text(X, y + 42, f"{MLN} millioner", 28, weight=700, font=COND)
    y = s.lines(X, y + 66, ["tapte dagsverk i 3. kvartal 2026,", "ikke sesongjustert"], 15, lh=20)
    y = pil_ned(y)
    y = hode(3, y)
    y = broek(s, X, y + 22, W)
    y = s.lines(X, y + 20, bryt(T3, 44), 15, lh=21)
    y = pil_ned(y)
    y = hode(4, y)
    y = sesongfigur(s, X + 26, y + 30, W - 26, 108)
    y = s.lines(X, y + 26, bryt(T4, 44), 15, lh=21)
    y = ikke_med(s, X, y + 18, W, smal=True)
    y = s.lines(X, y + 30, bryt(KILDELINJE, 46), 14, lh=19, fill=GRA_TEKST)
    s.h = int(y + 10)
    return s


# ---------------------------------------------------------------- toppgrafikk
def topp_venstre(s, stort, setning, linjer, kilde):
    s.text(40, 44, "Sykefravær · 3. kvartal 2026", 15, fill=GRA_TEKST, weight=600)
    s.text(36, 116, stort, 64, weight=700, font=COND)
    y = s.lines(40, 154, bryt(setning, 40), 21, lh=28, weight=600)
    y = s.lines(40, y + 8, sum((bryt(l, 58) for l in linjer), []), 15, lh=21, fill=GRA_TEKST)
    s.text(40, 314, kilde, 14, fill=GRA_TEKST)


def topp_a():
    s = Svg(1200, 330, "Sykefraværet har ligget nesten flatt siden starten av 2025")
    topp_venstre(s, "6,7 prosent",
                 "Sykefraværet har ligget nesten flatt siden starten av 2025.",
                 [f"Sesongjustert {nb(S['sesongjustert'], 2)}, ned fra {nb(S['forrige'], 2)} i 2. kvartal (\u22120,3 prosent).",
                  f"Den faktiske prosenten i kvartalet var {nb(S['ujustert'])}. Sommeren trekker alltid ned."],
                 f"Kilde: SSB, tabell 12439. Sist oppdatert: {OPPDATERT}.")
    tid, sj, u = SER["tid"], SER["sesongjustert"], SER["ujustert"]
    x0, x1, y0, y1, lo, hi = 640, 1060, 56, 276, 4, 9
    X = lambda i: x0 + i * (x1 - x0) / (len(tid) - 1)
    Y = lambda v: y1 - (v - lo) / (hi - lo) * (y1 - y0)
    for v in range(lo, hi + 1):
        s.line(x0, Y(v), x1, Y(v), STOTTE)
        s.text(x0 - 8, Y(v) + 5, str(v), 14, fill=GRA_TEKST, anchor="end")
    s.text(x0 - 22, y0 - 20, "prosent", 14, fill=GRA_TEKST)
    for i, t in enumerate(tid):
        if t.endswith("K1") and int(t[:4]) % 5 == 0:
            s.line(X(i), y1, X(i), y1 + 5, NULL)
            s.text(X(i), y1 + 22, t[:4], 14, fill=GRA_TEKST, anchor="middle")
    ib = tid.index("2015K1")
    s.line(X(ib), y0 - 4, X(ib), y1, M5, 1, dash="4,3")
    s.text(X(ib) + 6, y0 + 8, "Brudd 2015:", 14, fill=GRA_TEKST)
    s.text(X(ib) + 6, y0 + 26, "a-ordningen", 14, fill=GRA_TEKST)
    s.polyline([(X(i), Y(v)) for i, v in enumerate(u)], stroke=GRA, sw=1)
    s.polyline([(X(i), Y(v)) for i, v in enumerate(sj)], stroke=G4, sw=2.5)
    it = sj.index(max(sj))
    s.circle(X(it), Y(sj[it]), 3.5, G4)
    s.text(X(it) + 8, Y(sj[it]) - 6, f"Toppen: {nb(sj[it], 2)} i {tid[it][:4]}", 14)
    xe = X(len(tid) - 1)
    s.circle(xe, Y(sj[-1]), 3.5, G4)
    s.text(xe + 10, Y(sj[-1]) + 2, nb(sj[-1], 2), 16, weight=700)
    s.text(xe + 10, Y(sj[-1]) + 19, "sesongjustert", 14, fill=GRA_TEKST)
    s.text(xe + 10, Y(u[-1]) + 10, nb(u[-1]), 16, weight=700)
    s.text(xe + 10, Y(u[-1]) + 27, "ikke sesongjustert", 14, fill=GRA_TEKST)
    return s


def topp_b():
    s = Svg(1200, 330, "Av 100 avtalte arbeidsdager gikk nesten 7 tapt til sykdom")
    topp_venstre(s, "7 av 100",
                 "Av 100 avtalte arbeidsdager gikk nesten 7 tapt til sykdom.",
                 [f"Sesongjustert sykefraværsprosent {nb(S['sesongjustert'], 2)}.",
                  "Prosenten teller dagsverk, ikke personer. Den som er 50 prosent sykmeldt, teller som et halvt dagsverk."],
                 f"Kilde: SSB, tabell 12439 og 12446. Sist oppdatert: {OPPDATERT}.")
    # rutenett 10 x 10 avtalte dagsverk
    gx, gy, c, g = 612, 66, 18, 3
    v = S["sesongjustert"]
    s.text(gx, 50, "100 avtalte dagsverk", 15, weight=600)
    for k in range(100):
        r, col = divmod(k, 10)
        x, y = gx + col * (c + g), gy + r * (c + g)
        s.rect(x, y, c, c, fill="#ffffff", stroke=LINJE)
        if k < int(v):
            s.rect(x, y, c, c, fill=G4)
        elif k == int(v):
            s.rect(x, y, c * (v - int(v)), c, fill=G4)
    s.text(gx, gy + 10 * (c + g) + 18, f"{nb(v, 2)} tapt til sykdom", 15)
    # personer mot dagsverk, legemeldt
    bx, bw, mx = 900, 220, 8
    s.text(bx, 50, "Legemeldt, ikke sesongjustert", 15, weight=600)
    rader = [("Andel av lønnstakerne med", "sykmelding på referansedagen", PER["andel_lonnstakere_med_legemelding"]),
             ("Andel av de avtalte", "dagsverkene", PER["legemeldt_sykefravaersprosent"])]
    for j, (l1, l2, val) in enumerate(rader):
        y = 84 + j * 92
        s.text(bx, y, l1, 15)
        s.text(bx, y + 20, l2, 15)
        s.rect(bx, y + 32, bw * val / mx, 24, fill=G4)
        s.text(bx + bw * val / mx + 8, y + 50, f"{nb(val)} prosent", 15, weight=700)
    s.line(bx, 112, bx, 244, NULL)
    s.lines(bx, 272, ["Gradert sykmelding er én grunn", "til at tallene er forskjellige."], 14, lh=19, fill=GRA_TEKST)
    return s


def topp_c():
    s = Svg(1200, 330, "Egenmeldinger er to av tre fravær, men 14 prosent av de tapte dagsverkene")
    dv, tf = VAR["dagsverk"], VAR["tilfeller"]
    kat = list(dv)
    lang = kat[-1]
    topp_venstre(s, "2 av 3",
                 "fravær er egenmeldinger. De er likevel bare "
                 f"{nb(dv['Egenmeldt']['prosent'], 0)} prosent av de tapte dagsverkene.",
                 [f"Sykmeldinger på 32 dager eller mer er {nb(tf[lang]['prosent'], 0)} prosent av fraværene "
                  f"og {nb(dv[lang]['prosent'], 0)} prosent av dagsverkene.",
                  "Ikke sesongjustert. Varigheten er regnet innenfor kvartalet."],
                 f"Kilde: SSB, tabell 12946. Sist oppdatert: {OPPDATERT}.")
    farger = GRONN5[1:]
    tekstf = [TEKST, "#ffffff", "#ffffff", "#ffffff"]
    x0, bw = 620, 540
    # tegnforklaring over
    for n, (k, f) in enumerate(zip(kat, farger)):
        lx, ly = x0 + (n % 2) * 240, 34 + (n // 2) * 22
        s.rect(lx, ly, 14, 14, fill=f)
        s.text(lx + 20, ly + 12, k, 14)
    for j, (navn, d, tot) in enumerate([("Fraværstilfeller", tf, VAR["tilfeller_total"]),
                                         ("Tapte dagsverk", dv, VAR["dagsverk_total"])]):
        y = 112 + j * 96
        s.text(x0, y - 12, f"{navn} ({nb(tot / 1e6, 2)} millioner)", 15, weight=600)
        x = x0
        for k, f, tc in zip(kat, farger, tekstf):
            w = bw * d[k]["antall"] / tot
            s.rect(x, y, w, 40, fill=f)
            lab = f"{nb(d[k]['prosent'], 0)}"
            if w > 34:
                s.text(x + w / 2, y + 26, lab, 15, fill=tc, weight=700, anchor="middle")
            else:
                s.text(x + w / 2, y + 60, lab, 15, weight=700, anchor="middle")
            x += w
    s.text(x0, 290, "Prosent av alle i 3. kvartal 2026. Andelene er regnet fra publiserte antall.", 14, fill=GRA_TEKST)
    return s


if __name__ == "__main__":
    ut = {"src/konsept-bred.svg": konsept_bred(), "src/konsept-smal.svg": konsept_smal(),
          "docs/grafikk/02-topp-a.svg": topp_a(), "docs/grafikk/02-topp-b.svg": topp_b(),
          "docs/grafikk/02-topp-c.svg": topp_c()}
    for sti, s in ut.items():
        s.lagre(os.path.join(ROT, sti))
        print("skrev", sti, s.w, "x", s.h)

"""Lager infografikken «Hvem bor i Norge?» for folkemengde, i bred og smal (stående) variant.

Leser build/folkemengde.json (lag den med felles/bygg.py først) og SSB-ikonene fra repoet
ssb-ikoner, som ventes ved siden av dette repoet (../ssb-ikoner/svg) eller i miljøvariabelen
SSB_IKONER. Skriver src/infografikk-bred.svg og src/infografikk-smal.svg, som committes,
slik at bygget på GitHub ikke trenger ikonrepoet.

Rutenettet: fire like hvite bokser med samme dataflate (DT under boksens topp, DH høy),
slik at datamerkene står i flukt. Stolper er 2/3 av radhøyden, luften 1/3.
"""
import json, math, os, re
from xml.sax.saxutils import escape

MAPPE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(MAPPE)
IKDIR = os.environ.get("SSB_IKONER", os.path.join(os.path.dirname(REPO), "ssb-ikoner", "svg"))

d = json.load(open(os.path.join(MAPPE, "build", "folkemengde.json")))
L = d["land"]

def nb(x, des=0):
    s = f"{abs(x):,.{des}f}".replace(",", " ").replace(".", ",")
    return ("−" if x < 0 else "") + s
def ix(a): return L["aar"].index(a)

# ---------- tall ----------
SIST = L["aar"][-2]                      # siste hele år med komponenter
NYAAR = L["aar"][-1]                     # 1. januar etter
i = ix(SIST)
fodte, dode, innv, utv, vekst = (L[k][i] for k in ("fodte", "dode", "innv", "utv", "vekst"))
fo, ni = fodte - dode, innv - utv
korr = vekst - fo - ni
bef = L["bef"][ix(NYAAR)]
fo2010 = L["fodte"][ix(2010)] - L["dode"][ix(2010)]
oekt = sum(1 for j in range(1, len(L["bef"])) if L["bef"][j] > L["bef"][j - 1])
K = d["kommAar"]; kn = K["aar"].index(NYAAR)
kvekst = sorted(((v[0][kn] - v[0][kn - 1]) / v[0][kn - 1] for v in K["v"].values() if v[0][kn] and v[0][kn - 1]))
ned = sum(1 for x in kvekst if x < 0)
fu = sum(1 for v in K["v"].values() if v[1][-1] is not None and v[1][-1] < v[2][-1])
A = d["landAlder"]
def alder(a):
    return A["v"][A["aar"].index(a)]
m86, k86 = alder(1986); mny, kny = alder(NYAAR)
o80 = lambda m, k: sum(m[80:]) + sum(k[80:])
andel_ni = round(100 * ni / vekst)
HENTET = ".".join(reversed(d["kilde"]["hentet"].split("-")))

# ---------- farger ----------
TEKST, DEMP, STOTTE, NULL = "#274246", "#5d7174", "#d9dfe0", "#a9b5b7"
GR, GRL, BLA, BLAL, OKER = "#00824d", "#91cd9a", "#1d9de2", "#9cc9e3", "#c78800"
MENN, MENN80, KV, KV80 = "#7cc3ea", "#0f6fa8", "#e6c37a", "#9a6a00"
BG = "#eef3f1"

def bryt(t, n):
    ord_, linjer, l = t.split(" "), [], ""  # bare vanlig mellomrom: tall med hardt mellomrom deles ikke
    for o in ord_:
        if l and len(l) + 1 + len(o) > n:
            linjer.append(l); l = o
        else:
            l = (l + " " + o).strip()
    return linjer + [l] if l else linjer


def lag(v):
    """v er 'bred' eller 'smal'."""
    bred = v == "bred"
    P = f"ig{v[0]}"                       # prefiks for id-er, fordi begge ligger i samme side
    if bred:
        W, M, GAP, PAD, BH, DT, DH, KOL = 1232, 36, 24, 26, 384, 108, 196, 2
        T = dict(kick=13, h1=32, big=72, sub=16, q=27, bt=20, bs=14, lab=15, val=15, sm=13, sq=16)
    else:
        W, M, GAP, PAD, BH, DT, DH, KOL = 380, 12, 14, 16, 372, 96, 168, 1
        T = dict(kick=11, h1=24, big=48, sub=13, q=21, bt=17, bs=12.5, lab=13, val=13, sm=12, sq=14.5)
    BW = (W - 2 * M - (KOL - 1) * GAP) / KOL
    e = []
    add = e.append
    def txt(x, y, t, size, fill=TEKST, w=400, anchor="start"):
        add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" font-weight="{w}" text-anchor="{anchor}">{escape(str(t))}</text>')
    def rect(x, y, w, h, fill, rx=0, stroke="none", op=1):
        add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}"/>')
    def line(x1, y1, x2, y2, s=STOTTE, sw=1):
        add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{s}" stroke-width="{sw}"/>')
    nk = [0]
    def ikon(nr, x, y, px, farge=TEKST, del_=None):
        s = open(os.path.join(IKDIR, f"ikon-{nr:03d}.svg")).read()
        vb = float(re.search(r'viewBox="0 0 ([\d.]+)', s).group(1))
        inner = s[s.index(">") + 1: s.rindex("</svg>")]
        k = px / vb
        if del_:
            nk[0] += 1
            cid = f"{P}-k{nk[0]}"
            a, b = del_
            add(f'<clipPath id="{cid}"><rect x="{vb * a:.1f}" y="0" width="{vb * (b - a):.1f}" height="{vb}"/></clipPath>')
            x -= vb * (a + b) / 2 * k - px / 2
            add(f'<g transform="translate({x:.1f},{y:.1f}) scale({k:.4f})" color="{farge}"><g clip-path="url(#{cid})">{inner}</g></g>')
        else:
            add(f'<g transform="translate({x:.1f},{y:.1f}) scale({k:.4f})" color="{farge}">{inner}</g>')

    # ---------- hode ----------
    y = 52 if bred else 36
    txt(M, y, f"SSB · BEFOLKNING · 1. JANUAR {NYAAR}", T["kick"], DEMP, 600)
    y += 40 if bred else 32
    txt(M, y, "Hvem bor i Norge?", T["h1"], TEKST, 700)
    y += 26 if bred else 18
    isz = 78 if bred else 52
    ikon(21, M - 4, y, isz)
    txt(M + isz + 10, y + isz * 0.86, nb(bef), T["big"], TEKST, 700)
    y += isz + (34 if bred else 30)
    under = f"personer var bosatt i Norge. Det er {nb(vekst)} flere enn året før, en vekst på {nb(L['vekstpst'][i], 2)} prosent."
    for n, l in enumerate(bryt(under, 64 if bred else 50)):
        txt(M, y + n * (T["sub"] + 6), l, T["sub"], DEMP)
    y += (T["sub"] + 6) * len(bryt(under, 64 if bred else 50))
    # spørsmålsboksen
    if bred:
        qx, qy, qw, qh = M + BW + GAP, 32, BW, 206
    else:
        qx, qy, qw, qh = M, y + 8, BW, 170
    rect(qx, qy, qw, qh, "#ffffff", 8, STOTTE)
    ikon(161, qx + PAD, qy + 20, 40 if bred else 32, OKER)
    txt(qx + PAD + (52 if bred else 42), qy + (46 if bred else 41), "Spørsmålet", T["sm"] + 1, OKER, 700)
    ql = ["Norge vokser.", f"Hvorfor krymper da {ned} kommuner?"] if bred else ["Norge vokser.", "Hvorfor krymper da", f"{ned} kommuner?"]
    for n, l in enumerate(ql):
        txt(qx + PAD, qy + (100 if bred else 82) + n * (T["q"] + 9), l, T["q"], TEKST, 700)
    if bred:
        txt(qx + PAD, qy + qh - 24, f"{ned} av {len(kvekst)} kommuner hadde færre innbyggere 1.1.{NYAAR} enn ett år før.", T["sm"], DEMP)
    GY = (max(qy + qh, y) + 28) if bred else (qy + qh + 18)

    def boks(nr, tittel, under, ikonnr):
        kol, rad = (nr % 2, nr // 2) if bred else (0, nr)
        x = M + kol * (BW + GAP)
        y = GY + rad * (BH + GAP)
        rect(x, y, BW, BH, "#ffffff", 8, STOTTE)
        isz = 38 if bred else 30
        ikon(ikonnr, x + BW - PAD - isz, y + 18, isz, DEMP)
        txt(x + PAD, y + (44 if bred else 38), tittel, T["bt"], TEKST, 700)
        for n, l in enumerate(bryt(under, 80 if bred else 46)):
            txt(x + PAD, y + (70 if bred else 60) + n * (T["bs"] + 5), l, T["bs"], DEMP)
        return x + PAD, y + DT, BW - 2 * PAD, y

    # ---------- 1: regnskapet ----------
    x0, y0, dw, by = boks(0, f"Slik vokste vi i {SIST}", "Fire strømmer avgjør folketallet", 82)
    rader = [(23, "Fødte", fodte, GR, "+"), (140, "Døde", dode, "#8a9a9c", "−"),
             (73, "Innvandring", innv, BLA, "+"), (156, "Utvandring", utv, BLAL, "−")]
    step = DH / 5
    bh = step * 2 / 3
    lab = 170 if bred else 112
    vw = 72 if bred else 60
    sk = (dw - lab - vw) / max(r[2] for r in rader)
    isz = 30 if bred else 24
    for n, (nr, navn, val, f, t) in enumerate(rader):
        yy = y0 + n * step
        ikon(nr, x0, yy + bh / 2 - isz / 2, isz)
        txt(x0 + isz + 10, yy + bh / 2 + 5, navn, T["lab"])
        rect(x0 + lab, yy, val * sk, bh, f, 2)
        txt(x0 + lab + val * sk + 6, yy + bh / 2 + 5, f"{t}{nb(val)}", T["val"], TEKST, 700)
    yy = y0 + 4 * step
    line(x0, yy - step / 6, x0 + dw, yy - step / 6, TEKST)
    txt(x0 + isz + 10, yy + 4 + bh / 2 + 5, "Vekst", T["lab"], TEKST, 700)
    s2 = (dw - lab - vw) / vekst
    rect(x0 + lab, yy + 4, fo * s2, bh, GR, 2)
    rect(x0 + lab + fo * s2 + 2, yy + 4, ni * s2 - 2, bh, BLA, 2)
    if bred:
        txt(x0 + lab + 7, yy + 4 + bh / 2 + 5, f"+{nb(fo)}", T["val"], "#ffffff", 700)
        txt(x0 + lab + fo * s2 + 9, yy + 4 + bh / 2 + 5, f"+{nb(ni)}", T["val"], "#ffffff", 700)
    txt(x0 + lab + vekst * s2 + 6, yy + 4 + bh / 2 + 5, f"+{nb(vekst)}", T["val"], TEKST, 700)
    yb = by + DT + DH + (30 if bred else 26)
    lt = (f"Fødte minus døde: +{nb(fo)}", f"Nettoinnvandring: +{nb(ni)}") if not bred else ("Fødte minus døde", "Nettoinnvandring")
    rect(x0, yb - 11, 12, 12, GR, 1.5); txt(x0 + 18, yb, lt[0], T["sm"], TEKST, 700)
    if bred:
        rect(x0 + 160, yb - 11, 12, 12, BLA, 1.5); txt(x0 + 178, yb, lt[1], T["sm"], TEKST, 700)
    else:
        yb += 20; rect(x0, yb - 11, 12, 12, BLA, 1.5); txt(x0 + 18, yb, lt[1], T["sm"], TEKST, 700)
    for n, l in enumerate(bryt(f"{andel_ni} prosent av veksten kom fra nettoinnvandring. Korreksjon: +{nb(korr)}.", 90 if bred else 52)):
        txt(x0, yb + 28 + n * 17, l, T["sm"], DEMP)

    # ---------- 2: lang linje ----------
    x0, y0, dw, by = boks(1, f"{len(L['bef']) - 1} år med tall", f"Folketallet har økt i {oekt} av {len(L['bef']) - 1} år siden {L['aar'][0]}", 114)
    a0, a1, vmax = L["aar"][0], NYAAR, 6_000_000
    cw = dw - (58 if bred else 46)
    X = lambda a: x0 + (a - a0) / (a1 - a0) * cw
    Y = lambda val: y0 + DH - val / vmax * DH
    for val in (2e6, 4e6, 6e6):
        line(x0, Y(val), x0 + cw, Y(val)); txt(x0 + cw + 6, Y(val) + 4, f"{int(val / 1e6)} mill.", T["sm"], DEMP)
    line(x0, Y(0), x0 + cw, Y(0), NULL)
    pts = " ".join(f"{X(a):.1f},{Y(b):.1f}" for a, b in zip(L["aar"], L["bef"]))
    add(f'<polygon points="{X(a0):.1f},{Y(0):.1f} {pts} {X(a1):.1f},{Y(0):.1f}" fill="{GR}" fill-opacity="0.14"/>')
    add(f'<polyline points="{pts}" fill="none" stroke="{GR}" stroke-width="2.5" stroke-linejoin="round"/>')
    for a in ((1750, 1800, 1850, 1900, 1950, 2000) if bred else (1800, 1900, 2000)):
        txt(X(a), Y(0) + 20, a, T["sm"], DEMP, anchor="middle")
    merk = [(a0, "start", 0, -12, f"{nb(L['bef'][0])} i {a0}"), (1950, "end", -8, -10, f"{nb(L['bef'][ix(1950)] / 1e6, 1)} mill. i 1950"),
            (NYAAR, "end", -10, 5, f"{nb(bef / 1e6, 1)} mill.")]
    for a, anch, dx, dy, t in merk:
        b = L["bef"][ix(a)]
        add(f'<circle cx="{X(a):.1f}" cy="{Y(b):.1f}" r="4" fill="{GR}"/>')
        txt(X(a) + dx, Y(b) + dy, t, T["val"] - 1, TEKST, 700, anch)
    txt(x0, by + DT + DH + (56 if bred else 52), "Bosatte 1. januar hvert år, hele landet.", T["sm"], DEMP)

    # ---------- 3: kommunene ----------
    x0, y0, dw, by = boks(2, f"{len(kvekst)} kommuner", f"Én rute per kommune, sortert etter vekst i {SIST}", 143)
    rows = 12
    cols = math.ceil(len(kvekst) / rows)
    st = min(DH / rows, dw / cols)
    sz = st * 2 / 3
    for n, val in enumerate(kvekst):
        c_, r_ = divmod(n, rows)
        rect(x0 + c_ * st, y0 + DH - (rows - r_) * st + (st - sz), sz, sz, OKER if val < 0 else GRL, 1.5)
    yb = by + DT + DH + (30 if bred else 26)
    rect(x0, yb - 11, 12, 12, OKER, 1.5); txt(x0 + 18, yb, f"Nedgang: {ned}", T["sm"], TEKST, 700)
    rect(x0 + (150 if bred else 120), yb - 11, 12, 12, GRL, 1.5)
    txt(x0 + (168 if bred else 138), yb, f"Vekst eller uendret: {len(kvekst) - ned}", T["sm"], TEKST, 700)
    txt(x0, yb + 28, f"I {fu} kommuner døde flere enn det ble født i {SIST}.", T["sm"], DEMP)

    # ---------- 4: alder ----------
    x0, y0, dw, by = boks(3, "Vi blir eldre", f"80 år og eldre: {nb(o80(m86, k86))} i 1986, {nb(o80(mny, kny))} i {NYAAR}", 61)
    grp = lambda a: [sum(a[j:j + 5]) for j in range(0, 100, 5)] + [sum(a[100:])]
    ng = 21
    st = DH / ng
    bh = st * 2 / 3
    gmax = max(max(grp(x)) for x in (m86, k86, mny, kny))
    leg = 140 if bred else 0
    half = (dw - leg - 30) / 4
    skp = half / gmax
    def pyramide(xm, m, k, aar):
        gm, gk = grp(m), grp(k)
        for j in range(ng):
            yy = y0 + DH - (j + 1) * st + (st - bh)
            eldre = j >= 16
            rect(xm - 1 - gm[j] * skp, yy, gm[j] * skp, bh, MENN80 if eldre else MENN, 1)
            rect(xm + 1, yy, gk[j] * skp, bh, KV80 if eldre else KV, 1)
        txt(xm, by + DT + DH + 24, aar, T["lab"], TEKST, 700, "middle")
    pyramide(x0 + half, m86, k86, "1986")
    pyramide(x0 + 3 * half + 30, mny, kny, str(NYAAR))
    isz = 36 if bred else 28
    if bred:
        lx, ly = x0 + 4 * half + 52, y0 + 6
        pos = [(lx, ly), (lx, ly + 62)]
    else:
        ly = by + DT + DH + 44
        pos = [(x0, ly), (x0 + 130, ly)]
    for (px, py), (ik, navn, c1, c2) in zip(pos, (((115, (0.5, 0.88)), "Menn", MENN, MENN80), ((115, (0.12, 0.5)), "Kvinner", KV, KV80))):
        ikon(ik[0], px - 6, py, isz, c2, ik[1])
        txt(px + isz - 4, py + isz * 0.45, navn, T["lab"], TEKST, 700)
        rect(px + isz - 4, py + isz * 0.62, 13, 9, c1, 1); rect(px + isz + 12, py + isz * 0.62, 13, 9, c2, 1)
    if bred:
        txt(lx, ly + 150, "Mørk farge:", T["sm"], DEMP); txt(lx, ly + 167, "80 år og eldre", T["sm"], DEMP)
    else:
        txt(x0, ly + isz + 18, "Mørk farge: 80 år og eldre. Femårige grupper.", T["sm"], DEMP)

    # ---------- spørsmål ----------
    rader_ = 2 if bred else 4
    sy = GY + rader_ * (BH + GAP) + (14 if bred else 10)
    txt(M, sy + 18, "Tre spørsmål statistikken kan svare på", T["bt"] + (2 if bred else 0), TEKST, 700)
    sp = [(13, "Hvem teller som bosatt?", "Bare den som skal bo her minst seks måneder. Noen har flyttet ut uten å melde fra."),
          (138, "Hva skjer når nesten like mange dør som fødes?", f"Fødselsoverskuddet var {nb(fo2010)} i 2010 og {nb(fo)} i {SIST}."),
          (97, "Hvorfor krymper kommuner når landet vokser?", "Fødsler, dødsfall og flytting virker ulikt fra kommune til kommune.")]
    isz = 42 if bred else 34
    cwq = (W - 2 * M - 2 * GAP) / 3 if bred else W - 2 * M
    yq = sy + 46
    hmax = 0
    for n, (nr, q, svar) in enumerate(sp):
        x = M + n * (cwq + GAP) if bred else M
        y = yq if bred else yq + hmax
        ikon(nr, x, y, isz, GR)
        yy = y + 16
        ql = bryt(q, 30 if bred else 32)
        for l in ql:
            txt(x + isz + 14, yy, l, T["sq"], TEKST, 700); yy += T["sq"] + 6
        for l in bryt(svar, 42 if bred else 40):
            txt(x + isz + 14, yy, l, T["sm"] + 1, DEMP); yy += T["sm"] + 7
        if not bred:
            hmax += yy - y + 14
        else:
            hmax = max(hmax, yy - y)
    H = (yq + hmax + 52) if bred else (yq + hmax + 48)
    kilde = f"Kilde: SSB, statistikkbanken tabell 05803, 06913 og 10211. Hentet {HENTET}. Ikoner: SSB."
    for n, l in enumerate(bryt(kilde, 200 if bred else 58)):
        txt(M, H - 26 + n * 16 - (16 if not bred else 0), l, T["sm"] - 1, DEMP)

    # ---------- bakgrunn (legges først) ----------
    bgr = [f'<rect width="{W}" height="{H:.0f}" rx="10" fill="{BG}"/>',
           f'<defs><filter id="{P}-blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{70 if bred else 40}"/></filter>'
           f'<clipPath id="{P}-ramme"><rect width="{W}" height="{H:.0f}" rx="10"/></clipPath></defs>',
           f'<g clip-path="url(#{P}-ramme)">']
    for cx, cy, r, f, op in ((0.88, 0.06, 0.2, GRL, .5), (0.06, 0.92, 0.24, "#bfe3f4", .5), (0.52, 0.52, 0.18, "#e8f1dc", .6), (0.95, 0.8, 0.16, "#f3e3bd", .5)):
        bgr.append(f'<circle cx="{cx * W:.0f}" cy="{cy * H:.0f}" r="{r * max(W, H * 0.6):.0f}" fill="{f}" fill-opacity="{op}" filter="url(#{P}-blur)"/>')
    for n in range(8):
        r0 = (50 + n * 30) * (1 if bred else 0.6)
        pts = []
        for a in range(0, 361, 6):
            rad = math.radians(a)
            rr = r0 * (1 + 0.12 * math.sin(3 * rad + n * 0.5) + 0.06 * math.sin(7 * rad))
            pts.append(f"{W * 0.9 + rr * math.cos(rad) * 1.4:.1f},{(90 if bred else 60) + rr * math.sin(rad) * 0.8:.1f}")
        bgr.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="#9fb9b0" stroke-opacity="{0.3 - n * 0.03:.2f}" stroke-width="1"/>')
    bgr.append("</g>")

    tittel = f"Infografikk: {nb(bef)} bosatte i Norge 1. januar {NYAAR}. Veksten i {SIST}, folketallet siden {L['aar'][0]}, kommunene og aldersfordelingen."
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}" role="img" aria-labelledby="{P}-t" '
           f'font-family="Open Sans, system-ui, sans-serif"><title id="{P}-t">{escape(tittel)}</title>'
           + "".join(bgr) + "".join(e) + "</svg>")
    ut = os.path.join(MAPPE, "src", f"infografikk-{v}.svg")
    open(ut, "w").write(svg + "\n")
    print(f"  {os.path.relpath(ut, REPO)}: {W} x {H:.0f}, {round(len(svg) / 1024)} kB")


if __name__ == "__main__":
    if not os.path.isdir(IKDIR):
        raise SystemExit(f"Finner ikke SSB-ikonene i {IKDIR}. Klon ssb-ikoner ved siden av repoet, eller sett SSB_IKONER.")
    lag("bred")
    lag("smal")

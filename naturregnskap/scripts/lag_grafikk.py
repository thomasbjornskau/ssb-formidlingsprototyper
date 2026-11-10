"""Steg 2: konseptgrafikk (bred/smal) og toppgrafikk A–C for naturregnskap.
Bruker primitivene fra konseptfigurbiblioteket (plib) fordi felles/grafikk.py ikke er tilgjengelig i økten.
Alle tall i toppgrafikken er EKSEMPELTALL fra data/grafikk-utkast.json, ikke statistikk."""
import sys, os, json
sys.path.insert(0, "/tmp/claude-0/-home-claude/789c6c70-e699-5834-81b4-581ee87ddeca/scratchpad/nr")
from plib import T, TM, R, L, A, C, tw, DARK, INK, GREY, LINE, TEAL_BG, GREY_M, GREY_BG

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OI = {"blue": "#0072B2", "green": "#009E73", "orange": "#E69F00", "verm": "#D55E00"}
TINT = {"blue": "#e2eef7", "green": "#dff3ec", "orange": "#fcf0d6", "verm": "#fae3d6"}
EKS = "Eksempeltall, ikke statistikk"


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'{R(0, 0, w, h, "#ffffff", "none", 0, 0)}{body}</svg>')


def save(rel, s):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(s)


STEPS = [("1", "Kartlegge naturen", "blue",
          "Kart fra NIBIO, Kartverket og SSB settes sammen til ett grunnkart. Det gir arealet av hver naturtype.", "Utbredelse"),
         ("2", "Måle tilstanden", "green",
          "Målinger som død ved og vannkvalitet sammenlignes med intakt natur og settes på en skala fra 0 til 1.", "Tilstand"),
         ("3", "Telle hva naturen gir", "orange",
          "Ni tjenester, som tømmer, flomdemping og turer, måles hver i sin enhet og fordeles på naturtype og bruker.", "Økosystemtjenester"),
         ("4", "Sette regnskapene side om side", None,
          "De tre delene vises per naturtype, men legges ikke sammen. De er målt på ulike måter og til dels i ulike år.", "Naturregnskapet")]
IKKE = "Ikke med i 2026: naturens verdi i kroner, endringer utover utbygging, og det meste av havet."


def konsept_bred():
    W, H = 1200, 400
    b = ""
    cw, gp = 270, 40
    for i, (n, h, key, d, lab) in enumerate(STEPS):
        x = 20 + i * (cw + gp)
        col = OI[key] if key else DARK
        tint = TINT[key] if key else TEAL_BG
        b += R(x, 20, cw, 270, tint, "none", 0, 2) + R(x, 20, cw, 5, col, "none", 0, 0)
        b += C(x + 34, 66, 16, col) + T(x + 34, 72, n, 17, 700, "#fff" if key != "orange" else INK, "middle", small=True)
        s, hh = TM(x + 60, 72, h, 18, cw - 76, 22, 700, INK); b += s
        s, _ = TM(x + 20, 72 + hh + 22, d, 15, cw - 40, 21, 400, INK); b += s
        b += T(x + 20, 272, lab.upper(), 14, 700, col if key != "orange" else INK)
        if i < 3:
            b += A([(x + cw + 4, 155), (x + cw + gp - 4, 155)], GREY, 2, hs=10)
    b += R(20, 316, 1160, 64, "#ffffff", GREY_M, 1, 2, "6 4")
    b += T(44, 354, IKKE, 16, 400, GREY)
    return svg(W, H, b)


def konsept_smal():
    W = 390
    b = ""
    y = 16
    for i, (n, h, key, d, lab) in enumerate(STEPS):
        col = OI[key] if key else DARK
        tint = TINT[key] if key else TEAL_BG
        _, dh = TM(0, 0, d, 15, W - 92, 21)
        hgt = 60 + dh + 42
        b += R(10, y, W - 20, hgt, tint, "none", 0, 2) + R(10, y, 5, hgt, col, "none", 0, 0)
        b += C(42, y + 30, 15, col) + T(42, y + 36, n, 16, 700, "#fff" if key != "orange" else INK, "middle", small=True)
        b += T(68, y + 36, h, 17, 700, INK)
        s, _ = TM(68, y + 62, d, 15, W - 92, 21); b += s
        b += T(68, y + hgt - 14, lab.upper(), 14, 700, col if key != "orange" else INK)
        y += hgt
        if i < 3:
            b += A([(W / 2, y + 2), (W / 2, y + 22)], GREY, 2, hs=9)
            y += 26
    y += 14
    s, hh = TM(30, y + 30, IKKE, 15, W - 60, 21, 400, GREY)
    b += R(10, y, W - 20, hh + 34, "#ffffff", GREY_M, 1, 2, "6 4") + s
    return svg(W, y + hh + 50, b)


# ------------------------------------------------------------ toppgrafikk
D = json.load(open(os.path.join(ROOT, "data/grafikk-utkast.json")))


def topp_ramme(etikett, tall, setning, linjer, key):
    b = T(30, 46, etikett.upper(), 14, 700, GREY)
    b += T(30, 120, tall, 64, 700, OI[key] if key != "orange" else INK)
    s, hh = TM(30, 160, setning, 20, 470, 26, 700, INK); b += s
    y = 160 + hh + 12
    for l in linjer:
        s, h2 = TM(30, y, l, 15, 470, 20, 400, INK); b += s
        y += h2 + 4
    b += R(30, 300, tw(EKS, 14, 700) + 24, 22, TINT["verm"], "none", 0, 11) + T(42, 316, EKS, 14, 700, INK, small=True)
    return b


def topp_a():
    d = D["utbredelse"]
    b = topp_ramme("Naturregnskap · utbredelse 2024", f'{round(d["andel"]["Skog"])} %',
                   "av fastlands-Norge er skog", [f'Utbygd areal 2017–2024: om lag {d["utbygd_ha"]:,} hektar.'.replace(",", " "),
                                                  "Bare utbygging telles som endring."], "blue")
    x0, x1, y = 560, 1170, 70
    b += T(x0, y - 22, "Andel av landarealet, prosent", 14, 400, GREY)
    sel = "Skog"
    for i, (k, v) in enumerate(sorted(d["andel"].items(), key=lambda kv: -kv[1])):
        yy = y + i * 30
        w = (x1 - x0 - 230) * v / 40
        b += T(x0, yy + 16, k, 15, 700 if k == sel else 400, INK)
        b += R(x0 + 170, yy + 4, w, 18, OI["blue"] if k == sel else GREY_M, "none", 0, 0)
        b += T(x0 + 176 + w, yy + 18, f"{v:.0f}".replace(".", ","), 14, 700 if k == sel else 400, INK)
    b += L(x0 + 170, y, x0 + 170, y + 8 * 30, LINE, 1)
    return svg(1200, 330, b)


def topp_b():
    d = D["tilstand"]
    b = topp_ramme("Naturregnskap · tilstand 2024", f'{d["Skog"]["2024"]:.2f}'.replace(".", ","),
                   "er tilstanden i skog, målt fra 0 til 1",
                   ["1 er intakt natur, 0 er helt ødelagt.", "0,5 betyr ikke at halve skogen er intakt."], "green")
    x0, x1, y0 = 640, 1150, 70
    sx = lambda v: x0 + (x1 - x0) * v
    b += T(x0, y0 - 22, "Totalindeks, 0–1", 14, 400, GREY)
    for v in (0, 0.25, 0.5, 0.75, 1):
        b += L(sx(v), y0, sx(v), y0 + 5 * 42, LINE, 1)
        b += T(sx(v), y0 + 5 * 42 + 20, f"{v:g}".replace(".", ","), 14, 400, GREY, "middle")
    for i, (k, v) in enumerate(d.items()):
        yy = y0 + 22 + i * 42
        sel = k == "Skog"
        b += T(x0 - 14, yy + 5, k, 15, 700 if sel else 400, INK, "end")
        if "2019" in v:
            b += A([(sx(v["2019"]), yy), (sx(v["2024"]) + (-9 if v["2024"] > v["2019"] else 9), yy)], GREY, 1.5, hs=7)
            b += C(sx(v["2019"]), yy, 5, "#ffffff", GREY, 1.5)
        b += C(sx(v["2024"]), yy, 9 if sel else 7, OI["green"] if sel else "#7fcfb8")
    b += C(x1 - 150, y0 - 27, 5, "#ffffff", GREY, 1.5) + T(x1 - 138, y0 - 22, "2019", 14, 400, GREY)
    b += C(x1 - 70, y0 - 27, 7, OI["green"]) + T(x1 - 56, y0 - 22, "2024", 14, 400, GREY)
    return svg(1200, 330, b)


def topp_c():
    d = D["tjenester"]
    n = sum(1 for v in d.values() if v.get("Skog", 0) > 0)
    b = topp_ramme("Naturregnskap · økosystemtjenester 2024", f"{n} av 9",
                   "tjenester kommer delvis fra skog", ["Hver tjeneste har sin egen enhet og kan ikke legges sammen.",
                                                        "Figuren viser skogens andel av hver tjeneste."], "orange")
    x0, x1, y0 = 760, 1150, 54
    b += T(560, y0 - 14, "Andel fra skog, prosent", 14, 400, GREY)
    for i, (k, v) in enumerate(sorted(d.items(), key=lambda kv: -kv[1].get("Skog", 0))):
        yy = y0 + i * 27
        s = v.get("Skog", 0)
        b += T(560, yy + 16, k, 14, 400, INK)
        b += R(x0, yy + 4, x1 - x0, 16, GREY_BG, "none", 0, 0)
        if s:
            b += R(x0, yy + 4, (x1 - x0) * s / 100, 16, OI["orange"], "none", 0, 0)
        b += T(x0 + (x1 - x0) * s / 100 + 6 if s < 85 else x1 + 6, yy + 17, f"{s:.0f}", 14, 700, INK)
    return svg(1200, 330, b)


if __name__ == "__main__":
    save("src/konsept-bred.svg", konsept_bred())
    save("src/konsept-smal.svg", konsept_smal())
    save("docs/grafikk/02-topp-A.svg", topp_a())
    save("docs/grafikk/02-topp-B.svg", topp_b())
    save("docs/grafikk/02-topp-C.svg", topp_c())

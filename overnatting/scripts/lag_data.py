"""Lager build/overnatting.json fra rådata i data/raw/ og kontrollerer summene.

Kjøres av felles/bygg.py. Stopper med «Kontroll feilet: …» hvis en kontroll ikke går opp.

1. Kjører kontrollene K1–K12 fra steg 3 (scripts/kontroll_kilder.py).
2. Bygger datafilen og kontrollerer det som regnes her:
   B1 landene summerer til utlandet i alt for hver periode (år og 12 måneder) der alle måneder er publisert,
      per område og gruppe. Toleranse 100: K3 viser 57 overnattinger uten land i 2020.
   B2 regionene summerer til fylket per periode der alle regionene i fylket er hele. Toleranse 0.
   B3 de 65 regionene med kommuner har kart, Svalbard (21101) har ikke.
   B4 synonymene peker på kommuner som finnes i KLASS.
   B5 tallene i toppgrafikken og ingressen er de samme som i steg 2.
Bare standardbiblioteket.
"""
import itertools
import json
import math
import pathlib
import subprocess
import sys
from collections import defaultdict

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "overnatting.json"
AVVIK = {}
AAR = list(range(2018, 2026))           # hele år med konsistente landtall (K3)
HOTELL_FRA = "2022M01"                  # hotellmål per region i figurene


def feil(tekst):
    sys.exit(f"Kontroll feilet: {tekst}")


def avvik(navn, v):
    AVVIK[navn] = max(AVVIK.get(navn, 0), abs(v))


def les(navn):
    """Leser et json-stat2-svar. Siste dimensjon varierer raskest. Statussymbol beholdes."""
    d = json.loads((RAW / f"{navn}.json").read_text(encoding="utf8"))
    koder = []
    for dim in d["id"]:
        idx = d["dimension"][dim]["category"]["index"]
        koder.append(sorted(idx, key=idx.get) if isinstance(idx, dict) else list(idx))
    if [len(k) for k in koder] != d["size"]:
        feil(f"{navn}: dimensjonene stemmer ikke med size")
    status = {int(k): v for k, v in (d.get("status") or {}).items()}
    celler = {}
    for n, komb in enumerate(itertools.product(*koder)):
        v = d["value"][n]
        celler[komb] = None if status.get(n) in (":", ".", "..") else v
    etiketter = {dim: d["dimension"][dim]["category"].get("label", {}) for dim in d["id"]}
    return {"navn": navn, "celler": celler, "dims": d["id"], "koder": koder,
            "etiketter": etiketter, "oppdatert": d.get("updated", "")[:10]}


def hent(t, **fast):
    nokkel = []
    for dim, koder in zip(t["dims"], t["koder"]):
        if dim in fast:
            nokkel.append(str(fast[dim]))
        elif len(koder) == 1:
            nokkel.append(koder[0])
        else:
            feil(f"{t['navn']}: dimensjonen {dim} må velges")
    if tuple(nokkel) not in t["celler"]:
        feil(f"{t['navn']}: finnes ikke: {fast}")
    return t["celler"][tuple(nokkel)]


def koder(t, dim):
    return t["koder"][t["dims"].index(dim)]


def mnd_bak(m, n):
    a, k = int(m[:4]), int(m[5:])
    k -= n
    while k <= 0:
        k += 12
        a -= 1
    return f"{a}M{k:02d}"


# ---------------------------------------------------------------- kart
def regionkart(geojson, komm_til_reg):
    """Reiselivsregioner fra kommunegrensene (robhop, Kartverket 2024).
    Projeksjon som i arealprofiler og innvbef-omrade: transvers Mercator med sentralmeridian 15° Ø.
    Regionene lages ved kantkansellering: en kant som to kommuner i samme region deler, fjernes.
    Kantene som blir igjen, kjedes til lukkede ringer og forenkles med Douglas-Peucker."""
    l0 = math.radians(15)

    def proj(lon, lat):
        lam, phi = math.radians(lon) - l0, math.radians(lat)
        b = math.cos(phi) * math.sin(lam)
        return 0.5 * math.log((1 + b) / (1 - b)), -math.atan2(math.tan(phi), math.cos(lam))

    def dp(pts, eps):
        if len(pts) < 3:
            return pts
        (x1, y1), (x2, y2) = pts[0], pts[-1]
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy) or 1e-12
        imax, dmax = 0, 0
        for i in range(1, len(pts) - 1):
            d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / n
            if d > dmax:
                imax, dmax = i, d
        if dmax <= eps:
            return [pts[0], pts[-1]]
        return dp(pts[:imax + 1], eps)[:-1] + dp(pts[imax:], eps)

    seg = defaultdict(lambda: defaultdict(int))   # region -> kant -> antall
    alle = []
    for f in geojson["features"]:
        r = komm_til_reg[f["properties"]["kommunenummer"]]
        g = f["geometry"]
        for poly in (g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]):
            for ring in poly:
                for a, b in zip(ring, ring[1:]):
                    a, b = tuple(a[:2]), tuple(b[:2])
                    if a != b:
                        seg[r][(a, b) if a < b else (b, a)] += 1
                alle += [proj(*c[:2]) for c in ring]
    x0 = min(p[0] for p in alle)
    y0 = min(p[1] for p in alle)
    skala = 1000 / (max(p[0] for p in alle) - x0)
    hoyde = math.ceil((max(p[1] for p in alle) - y0) * skala)

    def xy(c):
        x, y = proj(*c)
        return ((x - x0) * skala, (y - y0) * skala)

    stier, boks = {}, {}
    for r, kanter in seg.items():
        ytre = [k for k, n in kanter.items() if n % 2 == 1]
        nabo = defaultdict(list)
        for a, b in ytre:
            nabo[a].append(b)
            nabo[b].append(a)
        ubrukt, ringer = set(ytre), []
        for a, b in ytre:
            if (a, b) not in ubrukt:
                continue
            ubrukt.discard((a, b))
            ring, cur = [a, b], b
            while cur != a:
                neste = next((n for n in nabo[cur] if ((cur, n) if cur < n else (n, cur)) in ubrukt), None)
                if neste is None:
                    break
                ubrukt.discard((cur, neste) if cur < neste else (neste, cur))
                ring.append(neste)
                cur = neste
            ringer.append(ring)
        deler, bx, by = [], [], []
        for ring in ringer:
            pts = [xy(c) for c in ring]
            bx += [p[0] for p in pts]
            by += [p[1] for p in pts]
            # Lukket ring: start og slutt er samme punkt, så den deles i punktet lengst fra start før forenkling
            i = max(range(len(pts)), key=lambda j: (pts[j][0] - pts[0][0]) ** 2 + (pts[j][1] - pts[0][1]) ** 2)
            pts = dp(pts[:i + 1], 0.35)[:-1] + dp(pts[i:], 0.35)
            if len(pts) < 4:
                continue
            xs_, ys_ = [p[0] for p in pts], [p[1] for p in pts]
            if (max(xs_) - min(xs_)) * (max(ys_) - min(ys_)) < 0.25:
                continue
            deler.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts[:-1]) + "Z")
        if not deler:
            feil(f"region {r} forsvant i kartet")
        stier[r] = "".join(deler)
        boks[r] = [round(min(bx), 1), round(min(by), 1), round(max(bx), 1), round(max(by), 1)]
    return {"b": 1000, "h": hoyde, "p": stier, "boks": boks}


# ---------------------------------------------------------------- hovedløp
def main():
    r = subprocess.run([sys.executable, "-I", str(MAPPE / "scripts" / "kontroll_kilder.py")], capture_output=True, text=True)
    if r.returncode:
        print(r.stdout)
        feil("kontrollene fra steg 3: " + (r.stderr.strip() or r.stdout.strip().splitlines()[-1]))
    print("K1–K12 fra steg 3: OK")

    rt = les("region_tid")
    la, lb = les("region_land_a"), les("region_land_b")
    rh = les("region_hotell")
    ft = les("fylke_type")
    sj = les("sesongjustert")
    hf = les("hotell_formal")
    gj = les("gjester")
    fb = les("fritidsbolig")
    ru = les("reiseundersokelsen")
    klass = json.loads((RAW / "klass_527.json").read_text(encoding="utf8"))["codes"]
    korr = json.loads((RAW / "klass_527_kommune.json").read_text(encoding="utf8"))["correspondenceMaps"]
    geo = json.loads((RAW / "kommuner2024-S.geojson").read_text(encoding="utf8"))
    syn = json.loads((MAPPE / "data" / "synonymer.json").read_text(encoding="utf8"))

    MND = koder(rt, "Tid")
    SISTE = MND[-1]
    REG = [c["code"] for c in klass]
    REGN = {c["code"]: c["name"] for c in klass}
    alle_reg = koder(rt, "Region")
    FYL = [r for r in alle_reg if len(r) == 2 and r != "0N"]
    OMR = ["0N"] + FYL + REG
    fylkenavn = rt["etiketter"]["Region"]
    G = ["01", "02+03+04"]

    # Perioder: hele år 2018–2025, siste 12 måneder og de 12 før
    PER = {str(a): [f"{a}M{m:02d}" for m in range(1, 13)] for a in AAR}
    PER["s12"] = [mnd_bak(SISTE, i) for i in range(11, -1, -1)]
    PER["f12"] = [mnd_bak(SISTE, i) for i in range(23, 11, -1)]
    PNAVN = list(PER)

    # ---- tidsserier per område: hotell og camping m.m., i alt og utlandet
    tid = {}
    for o in OMR:
        rad = []
        for g in G:
            for l in ("00000", "ccc"):
                rad.append([hent(rt, Region=o, InnKvartering1=g, Landkoder2=l, Tid=m) for m in MND])
        tid[o] = rad

    # ---- land per område og periode (bare der alle måneder er publisert)
    LAND = [l for l in koder(la, "Landkoder2") if l not in ("00000", "ccc", "000")
            and any(v is not None for (rr, g, ll, c, t), v in la["celler"].items() if ll == l and rr == "0N")]
    landnavn = la["etiketter"]["Landkoder2"]

    def lc(o, g, l, m):
        t = la if m < "2023M01" else lb
        return hent(t, Region=o, InnKvartering1=g, Landkoder2=l, Tid=m)

    lreg = {}
    for o in OMR:
        ut = {}
        for gi, g in enumerate(G):
            hel = []
            for p in PNAVN:
                hel.append(all(lc(o, g, "ccc", m) is not None for m in PER[p]))
            verdier = {}
            for li, l in enumerate(LAND):
                v = [sum(lc(o, g, l, m) or 0 for m in PER[p]) if hel[pi] else None for pi, p in enumerate(PNAVN)]
                if any(v):
                    verdier[li] = v
            # B1: landene summerer til utlandet i alt
            for pi, p in enumerate(PNAVN):
                if hel[pi]:
                    tot = sum(lc(o, g, "ccc", m) for m in PER[p])
                    s = sum(verdier[li][pi] for li in verdier)
                    avvik("B1 land = utlandet", tot - s)
            ut["f" + str(gi)] = [1 if h else 0 for h in hel]
            ut["v" + str(gi)] = verdier
            ut["n" + str(gi)] = [sum(lc(o, g, "000", m) for m in PER[p]) if hel[pi] else None for pi, p in enumerate(PNAVN)]
        lreg[o] = ut
    if AVVIK.get("B1 land = utlandet", 0) > 100:
        feil(f"B1: landene summerer ikke til utlandet i alt (avvik {AVVIK['B1 land = utlandet']})")

    # B2: regionene summerer til fylket
    for f in FYL:
        rr = [r for r in REG if r[:2] == f]
        for gi in range(2):
            for pi in range(len(PNAVN)):
                if all(lreg[r]["f" + str(gi)][pi] for r in rr) and lreg[f]["f" + str(gi)][pi]:
                    s = sum(sum(lreg[r]["v" + str(gi)][li][pi] for li in lreg[r]["v" + str(gi)]) + lreg[r]["n" + str(gi)][pi] for r in rr)
                    fv = sum(lreg[f]["v" + str(gi)][li][pi] for li in lreg[f]["v" + str(gi)]) + lreg[f]["n" + str(gi)][pi]
                    avvik("B2 regioner = fylke", s - fv)
    if AVVIK.get("B2 regioner = fylke", 0) > 100:
        feil(f"B2: regionene summerer ikke til fylket (avvik {AVVIK['B2 regioner = fylke']})")

    # ---- hotellmål per område fra 2022
    HM = ["KapasitetRom", "KapasitetSeng", "PrisRom", "LosjiOmsRom"]
    hmnd = [m for m in koder(rh, "Tid") if m >= HOTELL_FRA]
    hotell = {o: [[hent(rh, Region=o, ContentsCode=c, Tid=m) for m in hmnd] for c in HM] for o in OMR}

    # ---- toppgrafikk A og nøkkeltall (hele landet)
    sept = [[int(m[:4]), hent(hf, Region="0N", HotellFormal="00", Tid=m)] for m in koder(hf, "Tid") if m.endswith("M09")]
    samnd = [m for m in koder(sj, "Tid") if m >= mnd_bak(SISTE, 23)]
    sa = [hent(sj, Region="0N", InnKvartering1="01", Landkoder2="00000", ContentsCode="OvernattingerSesongj", Tid=m) for m in samnd]
    ifjor = mnd_bak(SISTE, 12)
    nasj = {}
    for o in ["0N"] + FYL:
        nasj[o] = {g: [hent(ft, Region=o, InnKvartering1=g, Landkoder2=l, Tid=m) for m in (SISTE, ifjor) for l in ("000", "ccc")]
                   for g in ("00", "01", "02", "03+04")}
    sm_mnd = SISTE[-2:]
    sammeM = [[int(m[:4]), hent(hf, Region="0N", HotellFormal="00", Tid=m)] for m in koder(hf, "Tid") if m.endswith("M" + sm_mnd)]
    topp = {
        "mnd": SISTE, "sammeMnd": sammeM, "sa": sa, "saMnd": samnd,
        "losji": [hent(rh, Region="0N", ContentsCode="LosjiOms", Tid=m) for m in (SISTE, ifjor)],
        "pris": [hent(rh, Region="0N", ContentsCode="PrisRom", Tid=m) for m in (SISTE, ifjor)],
        "kapRom": hent(rh, Region="0N", ContentsCode="KapasitetRom", Tid=SISTE),
        "kapSeng": hent(rh, Region="0N", ContentsCode="KapasitetSeng", Tid=SISTE),
        "fritid": [hent(fb, Landsdel="0", Landkoder="00000", Tid=m) for m in (SISTE, ifjor)],
    }
    gjest = {}
    for g in ("00", "01", "02", "03+04"):
        gjest[g] = [sum(hent(gj, Region="0N", InnKvartering1=g, Landkoder2="00000", Tid=f"2025M{m:02d}") for m in range(1, 13)),
                    sum(hent(ft, Region="0N", InnKvartering1=g, Landkoder2="00000", Tid=f"2025M{m:02d}") for m in range(1, 13))]
    reise = {k: round(sum(hent(ru, InnKvartering=k, Reisetype="01", Tid=f"2025K{q}") for q in range(1, 5)), 2)
             for k in koder(ru, "InnKvartering")}

    # B5: tallene fra steg 2
    if SISTE == "2026M09":
        sjekk = [(nasj["0N"]["01"][0] + nasj["0N"]["01"][1], 2579128), (sa[-1], 2408544), (sa[-2], 2428988),
                 (sum(nasj["0N"]["00"][:2]), 3448079), (topp["pris"][0], 1568)]
        for a, b in sjekk:
            if a != b:
                feil(f"B5: {a} er ikke {b}")
        if max(v for a, v in sept) != sept[-1][1]:
            feil("B5: september 2026 er ikke den høyeste septemberverdien")

    # ---- kart
    k2r = {m["targetCode"]: m["sourceCode"] for m in korr}
    kart = regionkart(geo, k2r)
    if sorted(kart["p"]) != sorted(r for r in REG if r != "21101") or "21101" in kart["p"]:
        feil("B3: kartet har ikke de 65 regionene med kommuner")

    # ---- kommuner og søkeord
    rkomm = defaultdict(list)
    for m in korr:
        rkomm[m["sourceCode"]].append(m["targetName"].split(" - ")[0])
    sokeord = []
    for s in syn["ord"]:
        regs = []
        for k in s["kommuner"]:
            if k not in k2r:
                feil(f"B4: synonymet {s['ord']} peker på kommune {k}, som ikke finnes i KLASS")
            regs.append(k2r[k])
        if s.get("region"):
            regs.append(s["region"])
        sokeord.append([s["ord"], sorted(set(regs)), 1 if s.get("usikker") else 0])
    kommuner = sorted([m["targetName"], m["sourceCode"]] for m in korr)

    pent = lambda n: n.split(" - ")[0]
    omr = [["0N", "Hele landet", "L", ""]] + [[f, pent(fylkenavn[f]), "F", ""] for f in FYL] + [[r, REGN[r], "R", r[:2]] for r in REG]
    data = {
        "kilde": {"oppdatert": {"14172": rt["oppdatert"], "14176": rh["oppdatert"], "14162": ft["oppdatert"], "14178": sj["oppdatert"],
                                "14166": hf["oppdatert"], "14165": gj["oppdatert"], "13100": fb["oppdatert"], "11270": ru["oppdatert"]},
                  "hentet": json.loads((RAW / "_hentet.json").read_text())["hentet"]},
        "mnd": MND, "per": PNAVN, "perMnd": {p: [PER[p][0], PER[p][-1]] for p in PNAVN},
        "omr": omr, "rkomm": {r: sorted(v) for r, v in rkomm.items()},
        "tid": tid, "land": [[l, landnavn[l]] for l in LAND], "lreg": lreg,
        "hmnd": hmnd, "hotell": hotell, "sept": sept, "topp": topp, "nasj": nasj, "gjest": gjest, "reise": reise,
        "kart": kart, "syn": sokeord, "kommuner": kommuner,
    }
    UT.parent.mkdir(exist_ok=True)
    tekst = json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    UT.write_text(tekst, encoding="utf8")
    print(f"build/overnatting.json: {len(tekst) // 1024} kB · {len(OMR)} områder · {len(LAND)} land · "
          f"kart {sum(len(p) for p in kart['p'].values()) // 1024} kB · avvik: "
          + ", ".join(f"{k} {v}" for k, v in AVVIK.items()))


if __name__ == "__main__":
    main()

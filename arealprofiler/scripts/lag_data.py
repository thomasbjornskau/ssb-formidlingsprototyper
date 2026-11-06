"""Lager build/arealprofiler.json fra data/raw/ og stopper bygget hvis kontrollene feiler.

Kjøres av felles/bygg.py. Bare Pythons standardbibliotek.

Rådata:
  data/raw/arealprofiler2024_ettark.xlsx   datagrunnlaget for Arealprofiler 2025 (uendret)
  data/raw/sentralitet.json                Klass 128, korrespondanse 1417 (kommuner 2024)
  data/raw/fylker.json                     Klass 104, fylker 2024
  data/raw/kofola_land.json                tabell 11776, landet (json-stat2)
  data/raw/kommuner2024-S.geojson          kommunegrenser 2024, forenklet (robhop/fylker-og-kommuner, Kartverket)
"""
import math
import itertools
import json
import os
import statistics as st
import sys

HER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HER)
from lag_grafikk_data import les_xlsx, tall  # noqa: E402

ROT = os.path.dirname(HER)
RAW = os.path.join(ROT, "data", "raw")
BUILD = os.path.join(ROT, "build")


def jload(*p):
    with open(os.path.join(ROT, *p), encoding="utf-8") as f:
        return json.load(f)


def stopp(t):
    sys.exit("Kontroll feilet: " + t)


# Hva en manglende verdi betyr, per indikator (steg 3, avsnitt 2). Brukes som tekst i prototypen.
MANGLER = {
    "A2": "Ingen tettsted", "B6": "Ingen tettsted", "B7": "Ingen tettsted",
    "B2": "Ikke kystkommune", "B3": "Ikke kystkommune",
    "B4": "Ingen tall: null eller ikke rapportert",
    "B10": "Ingen registrert",
    "A6": "Ingen nye boliger", "A7": "Ingen nye boliger", "A8": "Ingen nye boliger",
    "C8": "Ingen nye boliger", "C10": "Ingen nye boliger",
    "C12": "Ingen nye næringsbygg",
}
# Sentralitetsklassene 1 og 2 slås sammen: klasse 1 har bare fem kommuner (valgt 06.11.2026).
SENTRALITETSGRUPPE = {1: "1–2", 2: "1–2", 3: "3", 4: "4", 5: "5", 6: "6"}


def kartstier(geojson, knr):
    """Projiserer kommunegrensene (sfærisk transvers Mercator, sentralmeridian 15° Ø, som UTM 33)
    og forenkler med Douglas-Peucker. Gir SVG-stier i et koordinatsystem 1000 piksler bredt."""
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

    feats = {f["properties"]["kommunenummer"]: f["geometry"] for f in geojson["features"]}
    proj_ringer = {}
    xs, ys = [], []
    for k in knr:
        g = feats[k]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        ringer = []
        for poly in polys:
            for ring in poly:
                r = [proj(*c[:2]) for c in ring]
                ringer.append(r)
                xs += [p[0] for p in r]
                ys += [p[1] for p in r]
        proj_ringer[k] = ringer
    x0, y0 = min(xs), min(ys)
    skala = 1000 / (max(xs) - x0)
    hoyde = math.ceil((max(ys) - y0) * skala)
    stier = {}
    for k in knr:
        deler = []
        for r in proj_ringer[k]:
            pts = [((x - x0) * skala, (y - y0) * skala) for x, y in r]
            pts = dp(pts, 0.5)
            if len(pts) < 4:
                continue
            xs_, ys_ = [p[0] for p in pts], [p[1] for p in pts]
            if (max(xs_) - min(xs_)) * (max(ys_) - min(ys_)) < 0.3:   # små holmer forsvinner
                continue
            deler.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts[:-1]) + "Z")
        if not deler:   # en kommune skal aldri forsvinne helt: ta største ring uforenklet
            r = max(proj_ringer[k], key=len)
            deler.append("M" + "L".join(f"{(x - x0) * skala:.1f},{(y - y0) * skala:.1f}" for x, y in r[:-1]) + "Z")
        stier[k] = "".join(deler)
    return {"b": 1000, "h": hoyde, "p": stier}


# Null som betyr «ikke aktuelt» heller enn null prosent
NULL_BETYR = {"A3": "Ingen tettsted", "C6": "Ingen sentrumssone"}


def main():
    ind = jload("data", "indikatorer.json")["indikatorer"]
    e2k = {i["etikett"]: i["kode"] for i in ind}
    rader = les_xlsx(os.path.join(RAW, "arealprofiler2024_ettark.xlsx"))

    # ---------- Kommuner, sentralitet, fylker ----------
    sentr = jload("data", "raw", "sentralitet.json")
    kl = {m["targetCode"]: (m["targetName"], int(m["sourceCode"])) for m in sentr["correspondenceMaps"]}
    fylker = {c["code"]: c["name"] for c in jload("data", "raw", "fylker.json")["codes"] if c["code"] != "99"}

    d, navn = {}, {}
    for r in rader:
        if r["statistikkvariabel"] not in e2k:
            stopp(f"ukjent indikator i datagrunnlaget: {r['statistikkvariabel']}")
        k = e2k[r["statistikkvariabel"]]
        knr = str(r["kommunenr"]).split(".")[0].zfill(4)
        navn[knr] = r["kommune"]
        d[(k, knr, int(float(r["år"])), r.get("klasse") or "")] = tall(r["verdi"])
    knr = sorted(navn)

    # K1: omfang som i kildekartet
    if len(rader) != 105476 or len(knr) != 357 or len({k for k, *_ in d}) != 35:
        stopp(f"omfang: {len(rader)} rader, {len(knr)} kommuner, {len({k for k, *_ in d})} indikatorer")
    # K3: alle kommuner har sentralitet og fylke, klassene summerer til 357
    if set(knr) != set(kl):
        stopp(f"kommuner uten sentralitet: {sorted(set(knr) ^ set(kl))[:5]}")
    if any(k[:2] not in fylker for k in knr):
        stopp("kommune uten fylke")

    # ---------- Indikatorer ----------
    ut_ind, verdier = [], {}
    for i in ind:
        k = i["kode"]
        aar = sorted({a for (kk, _, a, _) in d if kk == k})
        klasser = sorted({c for (kk, _, _, c) in d if kk == k and c})
        if klasser:
            v = [[[d.get((k, n, a, c)) for c in klasser] for a in aar] for n in knr]
        else:
            v = [[d.get((k, n, a, "")) for a in aar] for n in knr]
        alle = [x for (kk, *_), x in d.items() if kk == k and x is not None]
        des = 0 if all(float(x).is_integer() for x in alle) else 1
        verdier[k] = {"aar": aar, "v": v, **({"klasser": klasser} if klasser else {})}
        ut_ind.append({**{x: i[x] for x in ("kode", "kort_navn", "etikett", "enhet", "type", "seksjon", "fire_aar", "kildetabell")},
                       "des": des, "mangler": MANGLER.get(k, "Mangler"), "null_betyr": NULL_BETYR.get(k)})

    # K5: B8-klassene summerer til nær 100 (faktisk 90,9–100,8; se kildekartet K5)
    b8 = {}
    for (kk, n, a, c), x in d.items():
        if kk == "B8" and x is not None:
            b8[(n, a)] = b8.get((n, a), 0) + x
    b8_min, b8_maks = min(b8.values()), max(b8.values())
    if b8_min < 90 or b8_maks > 102:
        stopp(f"B8 summerer til {b8_min:.1f}–{b8_maks:.1f}, forventet 90–102")

    # ---------- Landstall for jord (11776) ----------
    js = jload("data", "raw", "kofola_land.json")
    ids = js["id"]
    dims = [sorted(js["dimension"][x]["category"]["index"], key=js["dimension"][x]["category"]["index"].get) for x in ids]
    kof = {}
    for kombo, x in zip(itertools.product(*dims), js["value"]):
        kof[tuple(kombo)] = x
    pos = {x: ids.index(x) for x in ids}
    kof_aar = dims[pos["Tid"]]

    def kv(arealtype, formaal, lov, aar):
        key = [None] * len(ids)
        for dim, kode in (("KOKarealtype0000", arealtype), ("KOKformaal0000", formaal), ("KOKlovanvendelse0000", lov),
                          ("KOKkommuneregion0000", "EAK"), ("ContentsCode", "KOSarealomd0000"), ("Tid", aar)):
            key[pos[dim]] = kode
        return kof[tuple(key)]

    jord = {"aar": [int(a) for a in kof_aar],
            "dyrka_annet": [kv("dyrka", "omdispannetland", "total", a) for a in kof_aar],
            "dyrka_alle": [kv("dyrka", "total", "total", a) for a in kof_aar],
            "dyrkbar_alle": [kv("dyrkbar", "total", "total", a) for a in kof_aar]}

    # K4: sum av C3/C4 for kommunene mot 11776 «alle formål», 2020–2024.
    # Faktisk største avvik 32 dekar (C3 2024, Lillestrøm og Time rettet i 11776 15.06.2026) og 10 dekar (C4).
    # Før 2020 mangler 4–13 kommuner i C3/C4, så de årene kontrolleres ikke.
    storst = 0
    for kode, serie, tol in (("C3", "dyrka_alle", 40), ("C4", "dyrkbar_alle", 15)):
        for a in range(2020, 2025):
            s = sum(x for (kk, _, aa, _), x in d.items() if kk == kode and aa == a and x is not None)
            ref = jord[serie][jord["aar"].index(a)]
            avvik = abs(s - ref)
            storst = max(storst, avvik)
            if avvik > tol:
                stopp(f"sum {kode} {a} = {s:.0f}, tabell 11776 = {ref}, avvik {avvik:.0f} > {tol}")

    # ---------- Landet, egne beregninger: nye boliger vektet (variant A) ----------
    nb_aar = verdier["A6"]["aar"]
    land_nye = {"aar": nb_aar, "utenfor": [], "blokk": [], "antall": []}
    for j, a in enumerate(nb_aar):
        a6 = {n: verdier["A6"]["v"][x][j] for x, n in enumerate(knr)}
        a7 = {n: verdier["A7"]["v"][x][verdier["A7"]["aar"].index(a)] for x, n in enumerate(knr)}
        a8 = {n: verdier["A8"]["v"][x][verdier["A8"]["aar"].index(a)] for x, n in enumerate(knr)}
        f = [n for n in knr if a6[n] is not None and a8[n] is not None]
        sm = sum(a6[n] for n in f)
        land_nye["utenfor"].append(round(sum(a6[n] * a8[n] for n in f) / sm, 1))
        land_nye["blokk"].append(round(sum(a6[n] * (a7[n] or 0) for n in f) / sm, 1))
        land_nye["antall"].append(round(sum(a6[n] for n in f)))

    geo = jload("data", "raw", "kommuner2024-S.geojson")
    geo_k = {f["properties"]["kommunenummer"] for f in geo["features"]}
    if geo_k != set(knr):   # K6: kartet har nøyaktig de samme kommunene
        stopp(f"kartet og dataene har ulike kommuner: {sorted(geo_k ^ set(knr))[:5]}")
    kart = kartstier(geo, knr)

    synonymer = jload("data", "synonymer.json")["synonymer"]
    for s in synonymer:
        for k in s["k"]:
            if k not in navn:
                stopp(f"synonymet «{s['ord']}» viser til {k}, som ikke finnes")

    hentet = jload("data", "raw", "_hentet.json")["hentet"]
    ut = {
        "kilde": {"oppdatert": {"arealprofiler": "2025-08-29", "kofola_land": js.get("updated", "")[:10],
                                "sentralitet": sentr.get("lastModified", "")[:10]},
                  "hentet": hentet},
        "kommuner": [[n, navn[n], n[:2], SENTRALITETSGRUPPE[kl[n][1]], kl[n][1]] for n in knr],
        "kart": kart,
        "fylker": fylker,
        "indikatorer": ut_ind,
        "d": verdier,
        "jord": jord,
        "landNye": land_nye,
        "synonymer": [[s["ord"], s["k"], s["usikker"]] for s in synonymer],
    }
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(BUILD, "arealprofiler.json"), "w", encoding="utf-8") as f:
        json.dump(ut, f, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    print(f"lag_data: {len(knr)} kommuner, {len(ind)} indikatorer, {sum(len(x['aar']) for x in verdier.values())} indikatorår. "
          f"Største avvik mot 11776: {storst:.0f} dekar. B8-summer {b8_min:.1f}–{b8_maks:.1f}. "
          f"Kart: {len(kart['p'])} kommuner, {sum(len(x) for x in kart['p'].values()) // 1024} kB stier.")


if __name__ == "__main__":
    main()

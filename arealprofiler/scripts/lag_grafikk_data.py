"""Tall til grafikken (data/grafikk-utkast.json).

Leser fjorårets datagrunnlag, data/raw/arealprofiler2024_ettark.xlsx (det som ligger bak
arealprofilene publisert 29.08.2025), og data/raw/sentralitet.csv. Bare standardbiblioteket:
xlsx leses som zip/XML.

Kjør fra mappen arealprofiler/:  python3 scripts/lag_grafikk_data.py
"""
import csv
import json
import os
import re
import statistics as st
import zipfile
import xml.etree.ElementTree as ET

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROT, "data", "raw")
EKSEMPEL = "3405"  # Lillehammer, sentralitetsklasse 3
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

KODE = json.load(open(os.path.join(ROT, "data", "indikatorer.json"), encoding="utf-8"))
ETIKETT2KODE = {i["etikett"]: i["kode"] for i in KODE["indikatorer"]}


def les_xlsx(sti):
    z = zipfile.ZipFile(sti)
    delt = [("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS)]
    ark = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    rader = []
    for r in ark.iter("{%s}row" % NS["m"]):
        rad = {}
        for c in r.findall("m:c", NS):
            col = re.match(r"[A-Z]+", c.get("r")).group(0)
            v = c.find("m:v", NS)
            if v is None:
                isv = c.find("m:is/m:t", NS)
                rad[col] = isv.text if isv is not None else None
            elif c.get("t") == "s":
                rad[col] = delt[int(v.text)]
            else:
                rad[col] = v.text
        rader.append(rad)
    hode = [rader[0][k] for k in sorted(rader[0])]
    ut = []
    for rad in rader[1:]:
        d = dict(zip(hode, [rad.get(k) for k in sorted(rader[0])]))
        ut.append(d)
    return ut


def tall(v):
    return None if v in (None, "", "..", ".") else float(str(v).replace(",", "."))


def kvantil(xs, q):
    xs = sorted(xs)
    i = (len(xs) - 1) * q
    lo, hi = int(i), min(int(i) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)


def main():
    rader = les_xlsx(os.path.join(RAW, "arealprofiler2024_ettark.xlsx"))
    d, navn, aar_per = {}, {}, {}
    for r in rader:
        k = ETIKETT2KODE[r["statistikkvariabel"]]
        knr = str(r["kommunenr"]).split(".")[0].zfill(4)
        navn[knr] = r["kommune"]
        aar_per.setdefault(k, set()).add(int(float(r["år"])))
        if r.get("klasse"):
            continue
        v = tall(r["verdi"])
        if v is not None:
            d[(k, knr, int(float(r["år"])))] = v
    sentr = {}
    with open(os.path.join(RAW, "sentralitet.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter=";"):
            sentr[r["kommunenr"]] = int(r["sentralitetsklasse"])
    v = lambda k, a: {kn: x for (kk, kn, aa), x in d.items() if kk == k and aa == a}
    siste = lambda k: max(aar_per[k])
    aar = sorted({a for (_, _, a) in d})

    nye = []
    for a in aar:
        a6, a7, a8 = v("A6", a), v("A7", a), v("A8", a)
        f = [k for k in a6 if k in a8]
        if f:
            n = sum(a6[k] for k in f)
            nye.append({"aar": a, "nye_boliger": round(sum(a6.values())), "kommuner": len(f),
                        "andel_utenfor_tettsted": round(sum(a6[k] * a8[k] for k in f) / n, 1),
                        "andel_blokk": round(sum(a6[k] * a7.get(k, 0) for k in f) / n, 1)})
    omd = [{"aar": a, "dyrka": round(sum(v("C3", a).values())), "dyrkbar": round(sum(v("C4", a).values())),
            "kommuner": len(v("C3", a))} for a in aar if v("C3", a)]

    stripe = []
    for kode, navn_ind, enhet in [("A1", "Grunnareal til bolig per bosatt", "m²"),
                                  ("A3", "Andel bosatte i tettsted", "prosent"),
                                  ("A8", "Andel nye boliger utenfor tettsted", "prosent"),
                                  ("C10", "Nye boliger, avstand til sentrumssone", "km"),
                                  ("B6", "Trygg tilgang til rekreasjonsareal", "prosent")]:
        a = siste(kode)
        alle = v(kode, a)
        gr = [x for k, x in alle.items() if sentr.get(k) == sentr[EKSEMPEL]]
        stripe.append({"kode": kode, "aar": a, "navn": navn_ind, "enhet": enhet, "kommune": alle.get(EKSEMPEL),
                       "gruppe_p10": round(kvantil(gr, .1), 1), "gruppe_median": round(st.median(gr), 1),
                       "gruppe_p90": round(kvantil(gr, .9), 1), "gruppe_n": len(gr),
                       "under_kommunen": sum(1 for x in gr if x < alle.get(EKSEMPEL)),
                       "land_median": round(st.median(alle.values()), 1), "land_n": len(alle)})

    eks = {k: {"aar": siste(k), "verdi": d.get((k, EKSEMPEL, siste(k)))}
           for k in ["A1", "A6", "A8", "A9", "C1", "C4", "C9", "C10", "B9"]}
    typer = {}
    for i in KODE["indikatorer"]:
        typer.setdefault(i["type"], []).append(i["kode"])
    ut = {
        "kilde": "SSB, arealprofiler2024_ettark.xlsx (datagrunnlaget for Arealprofiler 2025, publisert 29.08.2025)",
        "merknad": "Summer og vektede andeler for landet er egne beregninger.",
        "antall_indikatorer": len(KODE["indikatorer"]),
        "typer": {k: len(x) for k, x in typer.items()},
        "fireaarssummer": sum(1 for i in KODE["indikatorer"] if i["fire_aar"]),
        "siste_aar": sorted({siste(i["kode"]) for i in KODE["indikatorer"]}),
        "eksempelkommune": {"kommunenr": EKSEMPEL, "navn": navn[EKSEMPEL], "sentralitetsklasse": sentr[EKSEMPEL],
                            "tall": eks},
        "nye_boliger": nye, "omdisponering": omd, "stripe": stripe,
        "jordvernmaal_dekar": 2000,
    }
    with open(os.path.join(ROT, "data", "grafikk-utkast.json"), "w", encoding="utf-8") as f:
        json.dump(ut, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: ut[k] for k in ["antall_indikatorer", "typer", "fireaarssummer", "siste_aar",
                                          "eksempelkommune", "stripe"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

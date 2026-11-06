"""Teller strukturen i datagrunnlaget og regner ut datamengden for steg 3.

Skriver docs/03-struktur.json. Kjør fra mappen arealprofiler/:
    python3 scripts/analyser_struktur.py
"""
import gzip
import json
import os
import statistics as st
import sys

HER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HER)
from lag_grafikk_data import les_xlsx, tall, ROT, RAW  # noqa: E402

IND = json.load(open(os.path.join(ROT, "data", "indikatorer.json"), encoding="utf-8"))["indikatorer"]
E2K = {i["etikett"]: i["kode"] for i in IND}


def main():
    rader = les_xlsx(os.path.join(RAW, "arealprofiler2024_ettark.xlsx"))
    kommuner = {}
    d = {}
    ikke_tall = 0
    for r in rader:
        knr = str(r["kommunenr"]).split(".")[0].zfill(4)
        kommuner[knr] = r["kommune"]
        v = tall(r["verdi"])
        if isinstance(r["verdi"], str) and "," in r["verdi"]:
            ikke_tall += 1
        d[(E2K[r["statistikkvariabel"]], knr, int(float(r["år"])), r.get("klasse") or "")] = v
    per = []
    for i in IND:
        k = i["kode"]
        cel = {(kn, a): v for (kk, kn, a, kl), v in d.items() if kk == k and kl == ""}
        if k == "B8":
            cel = {}
            for (kk, kn, a, kl), v in d.items():
                if kk == k:
                    cel[(kn, a)] = cel.get((kn, a), 0) + (v or 0)
        aar = sorted({a for _, a in cel})
        siste = aar[-1]
        vs = [v for (kn, a), v in cel.items() if a == siste and v is not None]
        per.append({
            "kode": k, "kort_navn": i["kort_navn"], "aar_fra": aar[0], "aar_til": siste, "antall_aar": len(aar),
            "kommuner_siste_aar": len(vs), "mangler_siste_aar": len(kommuner) - len(vs),
            "nuller_siste_aar": sum(1 for v in vs if v == 0),
            "hull_i_serien": sorted(set(range(aar[0], siste + 1)) - set(aar)),
            "min": min(vs), "median": st.median(vs), "maks": max(vs),
        })
    # B8: sum av klassene per kommune og år
    b8 = {}
    for (kk, kn, a, kl), v in d.items():
        if kk == "B8":
            b8[(kn, a)] = b8.get((kn, a), 0) + (v or 0)
    b8_avvik = sorted([(kn, a, round(s, 1)) for (kn, a), s in b8.items() if abs(s - 100) > 1.5])

    # Datamengde: kompakt JSON innbakt i index.html
    def storrelse(obj):
        b = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        return len(b), len(gzip.compress(b))

    knr = sorted(kommuner)
    alt = {}
    siste_bare = {}
    for i in IND:
        k = i["kode"]
        aar = sorted({a for (kk, kn, a, kl) in d if kk == k})
        if k == "B8":
            kl = sorted({kl for (kk, kn, a, kl) in d if kk == k})
            alt[k] = {"aar": aar, "klasser": kl,
                      "v": [[[d.get((k, kn, a, c)) for c in kl] for a in aar] for kn in knr]}
            siste_bare[k] = {"aar": aar[-1:], "klasser": kl,
                             "v": [[[d.get((k, kn, aar[-1], c)) for c in kl]] for kn in knr]}
        else:
            alt[k] = {"aar": aar, "v": [[d.get((k, kn, a, "")) for a in aar] for kn in knr]}
            siste_bare[k] = {"aar": aar[-1:], "v": [[d.get((k, kn, aar[-1], ""))] for kn in knr]}
    meta = {"kommuner": [[k, kommuner[k]] for k in knr]}
    celler = lambda o: sum(len(x["v"]) * len(x["aar"]) * len(x.get("klasser", [None])) for x in o.values())
    ut = {
        "rader": len(rader), "kommuner": len(kommuner), "indikatorer": len(IND),
        "verdier_med_desimalkomma_som_tekst": ikke_tall,
        "per_indikator": per, "b8_summer_utenfor_100_pm_1_5": b8_avvik[:20], "b8_antall_avvik": len(b8_avvik),
        "datamengde": {
            "liten_siste_aar": {"celler": celler(siste_bare), "bytes_gzip": storrelse({**meta, "d": siste_bare})},
            "middels_alle_aar": {"celler": celler(alt), "bytes_gzip": storrelse({**meta, "d": alt})},
        },
    }
    json.dump(ut, open(os.path.join(ROT, "docs", "03-struktur.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in ut.items() if k != "per_indikator"}, ensure_ascii=False, indent=1))
    for p in per:
        print(p)


if __name__ == "__main__":
    main()

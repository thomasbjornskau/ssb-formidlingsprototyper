"""Henter rådata for formidlingsprototypen fra data.ssb.no (PxWebApi v2).

Leser data/kilder.json og lagrer hvert datasett uendret som json-stat2 i
data/raw/<id>.json, med statussymbolene slik API-et gir dem. Skriver
data/raw/_hentet.json med tidspunkt, URL, oppdateringsdato og antall celler.

Bruk:  python3 scripts/hent_data.py            (alle datasett)
       python3 scripts/hent_data.py hoved yrke (bare disse)

Prototype: sykefratot. Bare Pythons standardbibliotek.
"""
import json, os, sys, time, urllib.request
from collections import Counter
from datetime import datetime, timezone

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROT, "data", "raw")
MAKS_CELLER = 800_000      # API-grense per spørring
PAUSE = 2.5                # holder oss godt under 30 spørringer per minutt


def hent(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ssb-formidlingsprototyper/sykefratot"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def main(valgte):
    kilder = json.load(open(os.path.join(ROT, "data", "kilder.json"), encoding="utf-8"))
    os.makedirs(RAW, exist_ok=True)
    logg_sti = os.path.join(RAW, "_hentet.json")
    logg = json.load(open(logg_sti, encoding="utf-8")) if os.path.exists(logg_sti) else {}
    for i, ds in enumerate(kilder["datasett"]):
        if valgte and ds["id"] not in valgte:
            continue
        if i:
            time.sleep(PAUSE)
        d = hent(ds["url"])
        n = len(d["value"])
        if n > MAKS_CELLER:
            sys.exit(f"{ds['id']}: {n} celler er over API-grensen")
        status = d.get("status") or {}
        with open(os.path.join(RAW, ds["id"] + ".json"), "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False)
        logg[ds["id"]] = {
            "tabell": ds["tabell"],
            "url": ds["url"],
            "hentet": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "updated": d.get("updated"),
            "celler": n,
            "statussymboler": dict(Counter(status.values())),
            "kilde": "data.ssb.no, PxWebApi v2, json-stat2, uendret",
        }
        print(f"{ds['id']:13} tabell {ds['tabell']}  {n:>7} celler  oppdatert {d.get('updated', '?')[:10]}  "
              f"status {dict(Counter(status.values()))}")
    with open(logg_sti, "w", encoding="utf-8") as f:
        json.dump(logg, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(set(sys.argv[1:]))

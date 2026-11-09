"""Henter rådata for formidlingsprototypen ufore fra data.ssb.no.

Bruk:  python ufore/scripts/hent_data.py
Leser ufore/data/kilder.json og skriver hvert datasett uendret til ufore/data/raw/<id>.json,
og en logg i ufore/data/raw/_hentet.json. Bare Pythons standardbibliotek.
Datasett med "metode": "POST" sender "utvalg" som PxWebApi v2-spørring (lange regionlister).
"""

import json
import os
import sys
import time
import urllib.request

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROT, "data", "raw")


def hent(ds):
    if ds.get("metode") == "POST":
        body = {"selection": [{"variableCode": k, "valueCodes": v.split(",")} for k, v in ds["utvalg"].items()]}
        req = urllib.request.Request(ds["url"], data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
    else:
        req = urllib.request.Request(ds["url"], headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def main():
    kilder = json.load(open(os.path.join(ROT, "data", "kilder.json"), encoding="utf-8"))
    os.makedirs(RAW, exist_ok=True)
    logg = {"hentet": time.strftime("%Y-%m-%dT%H:%M:%S"), "datasett": {}}
    for ds in kilder["datasett"]:
        for forsok in range(3):
            try:
                d = hent(ds)
                break
            except Exception as e:  # noqa: BLE001 – nettfeil prøves på nytt
                if forsok == 2:
                    sys.exit(f"Henting feilet for {ds['id']}: {e}")
                time.sleep(5)
        with open(os.path.join(RAW, ds["id"] + ".json"), "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, separators=(",", ":"))
        celler = len(d["value"]) if isinstance(d, dict) and "value" in d else None
        logg["datasett"][ds["id"]] = {"tabell": ds["tabell"], "oppdatert": d.get("updated") if isinstance(d, dict) else None,
                                      "celler": celler}
        print(f"{ds['id']:32} {ds['tabell']:10} {celler}")
        time.sleep(2.1)  # under 30 spørringer per minutt
    with open(os.path.join(RAW, "_hentet.json"), "w", encoding="utf-8") as f:
        json.dump(logg, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()

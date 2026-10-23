"""Henter rådata for navn fra PxWebApi v2 til data/raw/<id>.json.

Leser data/kilder.json. Bare Pythons standardbibliotek.
Bruk: python3 scripts/hent_data.py
"""
import datetime
import json
import os
import time
import urllib.request

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    kilder = json.load(open(os.path.join(ROT, "data", "kilder.json"), encoding="utf-8"))
    hentet = {"hentet": datetime.datetime.now().isoformat(timespec="seconds"),
              "metode": "PxWebApi v2 via scripts/hent_data.py", "filer": {}}
    for ds in kilder["datasett"]:
        with urllib.request.urlopen(ds["url"], timeout=120) as r:
            data = json.load(r)
        sti = os.path.join(ROT, "data", "raw", f"{ds['id']}.json")
        with open(sti, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        hentet["filer"][ds["id"]] = data.get("updated")
        print(f"{ds['id']}: tabell {ds['tabell']}, {len(data['value'])} celler")
        time.sleep(3)  # under 30 spørringer per minutt
    with open(os.path.join(ROT, "data", "raw", "_hentet.json"), "w", encoding="utf-8") as f:
        json.dump(hentet, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()

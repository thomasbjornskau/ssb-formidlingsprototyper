"""Henter rådata fra SSBs statistikkbank (PxWebApi v2) til data/raw/.

Bruk, fra mappen regfram:
    python scripts/hent_data.py

Leser data/kilder.json, henter hver URL som json-stat2 og lagrer svaret uendret
i data/raw/<id>.json. Skriver hentedatoen til data/raw/_hentet.json.
Kjør deretter python ../felles/bygg.py regfram fra roten.

Koblingen mellom kommune og sentralitet hentes ikke her (se "manuelt" i kilder.json).
"""
import datetime
import json
import pathlib
import time
import urllib.request

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"


def hent(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "ssb-formidlingsprototyper"})
    with urllib.request.urlopen(req, timeout=60) as svar:
        return json.loads(svar.read().decode("utf8"))


def main():
    kilder = json.loads((MAPPE / "data" / "kilder.json").read_text(encoding="utf8"))
    RAW.mkdir(parents=True, exist_ok=True)
    for i, ds in enumerate(kilder["datasett"]):
        if i:
            time.sleep(3)  # API-et tillater 30 spørringer per minutt
        data = hent(ds["url"])
        for nokkel in ("id", "size", "dimension", "value"):
            if nokkel not in data:
                raise SystemExit(f"{ds['id']}: svaret mangler '{nokkel}', er det json-stat2?")
        (RAW / f"{ds['id']}.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf8")
        print(f"{ds['id']}: tabell {ds['tabell']}, {len(data['value'])} verdier, oppdatert {data.get('updated', '?')}")
    (RAW / "_hentet.json").write_text(json.dumps({"hentet": datetime.date.today().isoformat()}), encoding="utf8")


if __name__ == "__main__":
    main()

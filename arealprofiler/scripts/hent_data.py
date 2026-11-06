"""Henter rådata fra SSB (PxWebApi v2 og Klass) til data/raw/.

Bruk, fra roten av repoet:
    python arealprofiler/scripts/hent_data.py

Leser data/kilder.json. Datasett med type «pxweb» lagres som json-stat2, «klass» som
Klass-JSON, uendret i data/raw/<id>.json. Datasett med type «fil» hentes ikke: fila
ligger uendret i data/raw/ (se kilder.json). Skriver hentedatoen til data/raw/_hentet.json.
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
    hentet = {"hentet": datetime.date.today().isoformat(), "datasett": {}}
    for ds in kilder["datasett"]:
        if ds.get("type") == "fil":
            if not (MAPPE / ds["fil"]).exists():
                raise SystemExit(f"{ds['id']}: mangler {ds['fil']}")
            print(f"{ds['id']}: fil, hentes ikke ({ds['fil']})")
            continue
        time.sleep(3)  # API-et tillater 30 spørringer per minutt
        data = hent(ds["url"])
        if ds.get("type", "pxweb") == "pxweb":
            for nokkel in ("id", "size", "dimension", "value"):
                if nokkel not in data:
                    raise SystemExit(f"{ds['id']}: svaret mangler '{nokkel}', er det json-stat2?")
            info = f"{len(data['value'])} verdier, oppdatert {data.get('updated', '?')}"
        else:
            info = f"{len(data.get('correspondenceMaps', data.get('codes', [])))} koder"
        (RAW / f"{ds['id']}.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf8")
        hentet["datasett"][ds["id"]] = info
        print(f"{ds['id']}: {ds['tabell']}, {info}")
    (RAW / "_hentet.json").write_text(json.dumps(hentet, ensure_ascii=False, indent=1), encoding="utf8")


if __name__ == "__main__":
    main()

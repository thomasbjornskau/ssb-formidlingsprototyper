"""Henter rådata for arbstatus-neet fra PxWebApi v2.

Leser data/kilder.json, lagrer hvert svar uendret som data/raw/<id>.json
og skriver data/raw/_hentet.json med tidspunkt, oppdateringsdato og antall celler.
Bare Pythons standardbibliotek.

Bruk:  python scripts/hent_data.py
"""
import datetime
import json
import os
import pathlib
import ssl
import time
import urllib.request

ROT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROT / "data" / "raw"


def kontekst():
    ca = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    return ssl.create_default_context(cafile=ca) if ca else ssl.create_default_context()


def hent(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ssb-formidlingsprototyper/arbstatus-neet"})
    with urllib.request.urlopen(req, timeout=120, context=kontekst()) as r:
        return r.read()


def main():
    kilder = json.loads((ROT / "data" / "kilder.json").read_text(encoding="utf-8"))
    RAW.mkdir(parents=True, exist_ok=True)
    logg = {"hentet": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "datasett": {}}
    for ds in kilder["datasett"]:
        innhold = hent(ds["url"])
        d = json.loads(innhold)
        celler = len(d["value"])
        (RAW / f"{ds['id']}.json").write_bytes(innhold)
        logg["datasett"][ds["id"]] = {"tabell": ds["tabell"], "oppdatert": d.get("updated"),
                                      "celler": celler, "statussymboler": len(d.get("status") or {})}
        print(f"{ds['id']:15s} tabell {ds['tabell']}  {celler:7d} celler  oppdatert {d.get('updated')}")
        time.sleep(2.5)  # holder oss godt under 30 spørringer i minuttet
    (RAW / "_hentet.json").write_text(json.dumps(logg, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()

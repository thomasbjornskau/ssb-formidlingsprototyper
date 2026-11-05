"""Henter ekte data for naturregnskap fra PxWebApi v2 etter publisering 25.11.2026.
Leser data/kilder.json og skriver data/raw/<id>.json. Bruk: python scripts/hent_data.py
Bare standardbiblioteket. Kodene i url-ene må rettes mot de ekte kodelistene først."""
import json, os, sys, time, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
k = json.load(open(os.path.join(ROOT, "data", "kilder.json")))
for d in k["datasett"]:
    if not d["url"]:
        print("hopper over", d["id"], "(mangler tabellnummer)"); continue
    with urllib.request.urlopen(d["url"], timeout=60) as r:
        data = json.load(r)
    json.dump(data, open(os.path.join(ROOT, "data", "raw", d["id"] + ".json"), "w"), ensure_ascii=False, indent=1)
    print("hentet", d["id"]); time.sleep(2.5)

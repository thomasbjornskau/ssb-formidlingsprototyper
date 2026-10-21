"""Henter kommuneendringer fra Klass (klassifikasjon 131) og lager data/synonymer.json.

Bruk, fra roten av repoet:
    python folkemengde/scripts/hent_klass.py

Synonymene lar kommunevelgeren finne dagens kommune når noen søker på et
tidligere kommunenavn (for eksempel «Skedsmo» → Lillestrøm) eller på én del av
et tospråklig navn (for eksempel «Tråante» → Trondheim). Kommuneendringene
lagres uendret i data/raw/klass_131_endringer.json.
"""
import json
import pathlib
import urllib.request

MAPPE = pathlib.Path(__file__).resolve().parent.parent
URL = "https://data.ssb.no/api/klass/v1/classifications/131/changes.json?from=1990-01-01&to=2026-01-02"


def main():
    req = urllib.request.Request(URL, headers={"Accept": "application/json", "User-Agent": "ssb-formidlingsprototyper"})
    with urllib.request.urlopen(req, timeout=60) as svar:
        endringer = json.loads(svar.read().decode("utf8"))
    (MAPPE / "data" / "raw" / "klass_131_endringer.json").write_text(json.dumps(endringer, ensure_ascii=False), encoding="utf8")

    # Dagens kommuner med navn fra statistikkbanken (sammenslåtte tidsserier)
    raw = json.loads((MAPPE / "data" / "raw" / "kommune_aar.json").read_text(encoding="utf8"))
    navn = {k[2:]: v for k, v in raw["dimension"]["Region"]["category"]["label"].items() if k[2:].isdigit()}

    # Følg hver gammel kode fram til dagens koder
    fram = {}
    for e in endringer["codeChanges"]:
        fram.setdefault(e["oldCode"], set()).add(e["newCode"])

    def dagens(kode, sett=frozenset()):
        """Dagens kode(r) for en kode. En kode som finnes i dag, er seg selv; grensejusteringer følges ikke."""
        if kode in navn:
            return {kode}
        if kode in sett:
            return set()
        ut = set()
        for ny in fram.get(kode, set()) - {kode}:
            ut |= dagens(ny, sett | {kode})
        return ut

    syn = {}
    for e in endringer["codeChanges"]:
        mål = sorted(k for k in dagens(e["oldCode"]) if k in navn)
        gammel = e["oldName"].strip()
        if mål and all(gammel.lower() != navn[k].lower() for k in mål):
            syn.setdefault(gammel, set()).update(mål)
    for kode, n in navn.items():
        if " - " in n:
            for del_ in n.split(" - "):
                if del_.strip().lower() != n.lower():
                    syn.setdefault(del_.strip(), set()).add(kode)
    syn = {k: sorted(v) for k, v in sorted(syn.items())}
    ut = {
        "merknad": "Søkeord som ikke er dagens kommunenavn, med dagens kommunekode(r). Tidligere navn fra Klass 131 "
                   "(endringer 1990–2026) og delene av tospråklige navn. Et navn kan peke på flere kommuner når en kommune er delt.",
        "kilde": URL,
        "synonymer": syn,
    }
    (MAPPE / "data" / "synonymer.json").write_text(json.dumps(ut, ensure_ascii=False, indent=1), encoding="utf8")
    flere = {k: v for k, v in syn.items() if len(v) > 1}
    print(f"{len(endringer['codeChanges'])} endringer, {len(syn)} synonymer, {len(flere)} peker på flere kommuner")
    for k in ("Skedsmo", "Oppegård", "Tråante", "Snillfjord", "Kautokeino", "Askim", "Stokke", "Sandøy", "Hamarøy"):
        print(f"  {k}: {[navn[x] for x in syn.get(k, [])]}")


if __name__ == "__main__":
    main()

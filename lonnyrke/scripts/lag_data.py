"""Lager build/lonnyrke.json fra data/raw/yrker.json (tabell 11418) og kontrollerer tallene.

Kjøres av felles/bygg.py. Stopper med feil hvis en kontroll ikke går opp:
- K1  jobber for menn + kvinner = begge kjønn, for alle yrker og år der alle tre finnes
- K2  406 firesifrede yrker, uten «uoppgitt» (0000)
- K3  hver manglende verdi har et statussymbol (: eller .), ingen blir null
- K4  median for alle yrker finnes for alle år og begge kjønn
- K5  kvinners lønn i prosent av menns ligger mellom 50 og 150 for alle yrker der begge finnes

Toleransen i K1 er 0, fordi antall jobber er heltall og ikke avrundet (avvik 0 per 04.11.2026).
Grensene i K5 er vide med vilje. De fanger byttede kolonner eller kroner i feil enhet, ikke ekte forskjeller.
"""
import itertools
import json
import pathlib
import sys

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "lonnyrke.json"
HOVEDGRUPPER = {"1": "Ledere", "2": "Akademiske yrker", "3_01-03": "Høyskoleyrker og militære yrker",
                "4": "Kontoryrker", "5": "Salgs- og serviceyrker", "6": "Bønder, fiskere mv.",
                "7": "Håndverkere", "8": "Operatører, sjåfører mv.", "9": "Renholdere, hjelpearbeidere mv."}


def feil(tekst):
    sys.exit(f"Kontroll feilet: {tekst}")


def les(navn):
    """Leser et json-stat2-svar. Verdiene ligger i radrekkefølge med siste dimensjon raskest."""
    d = json.loads((RAW / f"{navn}.json").read_text(encoding="utf8"))
    koder = []
    for dim in d["id"]:
        idx = d["dimension"][dim]["category"]["index"]
        koder.append(sorted(idx, key=idx.get) if isinstance(idx, dict) else list(idx))
    if [len(k) for k in koder] != d["size"]:
        feil(f"{navn}: dimensjonene stemmer ikke med size")
    status = d.get("status") or {}
    celler, symbol = {}, {}
    for n, komb in enumerate(itertools.product(*koder)):
        celler[komb] = d["value"][n]
        if str(n) in status:
            symbol[komb] = status[str(n)]
    etiketter = {dim: d["dimension"][dim]["category"].get("label", {}) for dim in d["id"]}
    return {"navn": navn, "celler": celler, "symbol": symbol, "dims": d["id"], "koder": koder,
            "etiketter": etiketter, "oppdatert": d.get("updated", "")[:10]}


def nokkel(t, **fast):
    return tuple(fast[dim] if dim in fast else t["koder"][i][0] for i, dim in enumerate(t["dims"]))


def hent(t, **fast):
    k = nokkel(t, **fast)
    if k not in t["celler"]:
        feil(f"{t['navn']}: finner ikke {fast}")
    return t["celler"][k]


def symbol(t, **fast):
    return t["symbol"].get(nokkel(t, **fast))


def koder(t, dim):
    return t["koder"][t["dims"].index(dim)]


def gruppe(kode):
    return "3_01-03" if kode[0] == "0" else kode[0]


def main():
    t = les("yrker")
    aar = koder(t, "Tid")
    alle_yrker = koder(t, "Yrke")
    fire = [k for k in alle_yrker if len(k) == 4 and k.isdigit() and k != "0000"]
    navn = t["etiketter"]["Yrke"]

    # K2
    if len(fire) != 406:
        feil(f"K2: {len(fire)} firesifrede yrker, ventet 406")

    # K3
    nuller = [k for k, v in t["celler"].items() if v is None and k not in t["symbol"]]
    if nuller:
        feil(f"K3: {len(nuller)} manglende verdier uten statussymbol, for eksempel {nuller[0]}")

    # K1
    k1 = 0
    for y in fire + ["0-9"]:
        for a in aar:
            b, m, k = (hent(t, MaaleMetode="10", Yrke=y, Kjonn=s, Tid=a) for s in ("0", "1", "2"))
            if None not in (b, m, k):
                k1 += 1
                if m + k != b:
                    feil(f"K1: {navn[y]} {a}: menn {m} + kvinner {k} = {m + k}, ikke {b}")

    # K4
    for s in ("0", "1", "2"):
        for a in aar:
            if hent(t, MaaleMetode="01", Yrke="0-9", Kjonn=s, Tid=a) is None:
                feil(f"K4: median for alle yrker mangler for kjønn {s} i {a}")

    def serie(y, s):
        return [hent(t, MaaleMetode="01", Yrke=y, Kjonn=s, Tid=a) for a in aar]

    def symboler(y, s):
        return [symbol(t, MaaleMetode="01", Yrke=y, Kjonn=s, Tid=a) or "" for a in aar]

    yrker = []
    k5 = 0
    for y in fire:
        b, m, k = serie(y, "0"), serie(y, "1"), serie(y, "2")
        if all(v is None for v in b):
            continue  # yrket har aldri hatt tall, vises ikke i velgeren
        siste = len(aar) - 1
        if m[siste] and k[siste]:
            p = 100 * k[siste] / m[siste]
            k5 += 1
            if not 50 <= p <= 150:
                feil(f"K5: {navn[y]}: kvinner {p:.1f} prosent av menn")
        yrker.append({
            "k": y, "n": navn[y], "g": gruppe(y),
            "b": b, "m": m, "kv": k,
            "sb": symboler(y, "0")[-1], "sm": symboler(y, "1")[-1], "sk": symboler(y, "2")[-1],
            "j": [hent(t, MaaleMetode="10", Yrke=y, Kjonn=s, Tid=aar[-1]) for s in ("0", "1", "2")],
        })

    ut = {
        "aar": [int(a) for a in aar],
        "oppdatert": t["oppdatert"],
        "hentet": json.loads((RAW / "_hentet.json").read_text(encoding="utf8"))["hentet"],
        "alle": {"b": serie("0-9", "0"), "m": serie("0-9", "1"), "kv": serie("0-9", "2"),
                 "j": [hent(t, MaaleMetode="10", Yrke="0-9", Kjonn=s, Tid=aar[-1]) for s in ("0", "1", "2")]},
        "grupper": HOVEDGRUPPER,
        "yrker": yrker,
    }
    UT.parent.mkdir(exist_ok=True)
    UT.write_text(json.dumps(ut, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(f"lonnyrke: {len(yrker)} yrker med tall, {k5} med begge kjønn i {aar[-1]}. "
          f"K1 {k1} kontroller, største avvik 0. K2–K5 ok.")


if __name__ == "__main__":
    main()

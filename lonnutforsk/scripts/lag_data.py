"""Lager build/lonnutforsk.json fra rådata i data/raw/ og kontrollerer tallene.

Kjøres av felles/bygg.py. Stopper med feil hvis en kontroll ikke går opp:
- K1  heltidsekvivalenter for menn + kvinner = begge kjønn (11421, næring)
- K2  avtalt månedslønn + uregelmessige tillegg + bonus = månedslønn, gjennomsnitt (11421)
- K3  nedre kvartil <= median <= øvre kvartil overalt (11421, næring og alder)
- K4  23 koder for næringshovedområde, med «Alle næringer» og «Uoppgitt» (11421)
- K5  hver manglende verdi har et statussymbol (alle tabeller)
- K6  median for alle næringer i 11421 = median for alle yrker i 11419, alle år og kjønn

Toleransene er satt etter de faktiske avvikene 04.11.2026, med margin. Kronebeløpene er
avrundet til 10 kr. Per 04.11.2026 avviker 1 438 av 2 102 kombinasjoner med 0 kr, 660 med 10 kr,
tre med 20 kr og én med 30 kr. De største avvikene er i «Uoppgitt» og i små grupper der et tillegg
er avrundet til 30 kr. Toleransen er derfor 30 kr.
Manglende verdier skrives som statussymbolet (":" eller "."), aldri som null.
"""
import itertools
import json
import pathlib
import sys

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "lonnutforsk.json"
AVVIK = {}


def feil(tekst):
    sys.exit(f"Kontroll feilet: {tekst}")


def avvik(navn, v):
    AVVIK[navn] = max(AVVIK.get(navn, 0), v)


def les(navn):
    d = json.loads((RAW / f"{navn}.json").read_text(encoding="utf8"))
    koder = []
    for dim in d["id"]:
        idx = d["dimension"][dim]["category"]["index"]
        koder.append(sorted(idx, key=idx.get) if isinstance(idx, dict) else list(idx))
    if [len(k) for k in koder] != d["size"]:
        feil(f"{navn}: dimensjonene stemmer ikke med size")
    status = d.get("status") or {}
    celler = {}
    for n, komb in enumerate(itertools.product(*koder)):
        v = d["value"][n]
        if v is None:
            s = status.get(str(n))
            if s is None:
                feil(f"K5: {navn}: manglende verdi uten statussymbol i {komb}")
            v = s
        celler[komb] = v
    return {"navn": navn, "celler": celler, "dims": d["id"], "koder": koder,
            "etiketter": {dim: d["dimension"][dim]["category"].get("label", {}) for dim in d["id"]},
            "oppdatert": d.get("updated", "")[:10]}


def hent(t, **fast):
    k = tuple(fast[dim] if dim in fast else t["koder"][i][0] for i, dim in enumerate(t["dims"]))
    if k not in t["celler"]:
        feil(f"{t['navn']}: finner ikke {fast}")
    return t["celler"][k]


def koder(t, dim):
    return t["koder"][t["dims"].index(dim)]


def tall(v):
    return isinstance(v, (int, float))


def kube(t, akser, **fast):
    """Nestede lister i rekkefølgen til akser, siste akse innerst."""
    dim, *rest = akser
    return [kube(t, rest, **fast, **{dim: k}) if rest else hent(t, **fast, **{dim: k}) for k in koder(t, dim)]


def main():
    N, A, K = les("naering"), les("alder"), les("komponenter")
    YN, Y2 = les("yrke_naering"), les("yrker2")
    aar = koder(N, "Tid")
    nar = koder(N, "NACE2007")

    # K4
    if len(nar) != 23 or nar[0] != "A-S" or "00" not in nar:
        feil(f"K4: {len(nar)} næringskoder, ventet 23 med A-S først og 00")

    # K1
    for kom in itertools.product(koder(N, "Sektor"), nar, koder(N, "ArbeidsTid"), aar):
        s, n, a, t = kom
        b, m, k = (hent(N, MaaleMetode="11", Sektor=s, NACE2007=n, ArbeidsTid=a, Tid=t, Kjonn=x) for x in "012")
        if tall(b) and tall(m) and tall(k):
            avvik("K1", abs(m + k - b))
    if AVVIK.get("K1", 0) > 2:
        feil(f"K1: heltidsekvivalenter menn + kvinner avviker med {AVVIK['K1']} fra begge kjønn")

    # K2
    for s, n, x, t in itertools.product(koder(K, "Sektor"), nar, "012", aar):
        v = {c: hent(K, Sektor=s, NACE2007=n, Kjonn=x, Tid=t, ContentsCode=c)
             for c in ("Manedslonn", "AvtaltManedslonn", "Uregtil", "Bonus")}
        if all(tall(z) for z in v.values()):
            avvik("K2", abs(v["AvtaltManedslonn"] + v["Uregtil"] + v["Bonus"] - v["Manedslonn"]))
    if AVVIK.get("K2", 0) > 30:
        feil(f"K2: delene av månedslønn avviker med {AVVIK['K2']} kr fra summen")

    # K3
    for t, ekstra in ((N, {}), (A, {})):
        andre = [d for d in t["dims"] if d not in ("MaaleMetode",)]
        for kom in itertools.product(*(koder(t, d) for d in andre)):
            f = dict(zip(andre, kom))
            lo, me, hi = (hent(t, MaaleMetode=m, **f) for m in ("051", "01", "061"))
            if tall(lo) and tall(me) and tall(hi) and not lo <= me <= hi:
                feil(f"K3: {t['navn']} {f}: kvartilene {lo}, {me}, {hi} står i feil rekkefølge")

    # K6
    for x, t in itertools.product("012", aar):
        a = hent(N, MaaleMetode="01", NACE2007="A-S", Sektor="ALLE", ArbeidsTid="0", Kjonn=x, Tid=t)
        b = hent(YN, MaaleMetode="01", Yrke="0-9", NACE2007="A-S", Kjonn=x, Tid=t) if t in koder(YN, "Tid") else a
        avvik("K6", abs(a - b))
    if AVVIK["K6"] > 0:
        feil(f"K6: median for alle i 11421 og 11419 avviker med {AVVIK['K6']} kr")

    yrker_yn = [y for y in koder(YN, "Yrke") if y not in ("1120",)]
    yrker2 = [y for y in koder(Y2, "Yrke") if y != "00"]
    ut = {
        "aar": [int(a) for a in aar],
        "oppdatert": {"11421": N["oppdatert"], "11419": YN["oppdatert"], "11418": Y2["oppdatert"]},
        "hentet": json.loads((RAW / "_hentet.json").read_text(encoding="utf8"))["hentet"],
        "maal": {k: N["etiketter"]["MaaleMetode"][k] for k in koder(N, "MaaleMetode")},
        "sektor": [[k, N["etiketter"]["Sektor"][k]] for k in koder(N, "Sektor")],
        "arbtid": [[k, N["etiketter"]["ArbeidsTid"][k]] for k in koder(N, "ArbeidsTid")],
        "naering": [[k, N["etiketter"]["NACE2007"][k]] for k in nar],
        "alder": [[k, A["etiketter"]["Alder"][k]] for k in koder(A, "Alder")],
        # [mål][sektor][arbeidstid][kjønn][næring][år]
        "N": kube(N, ["MaaleMetode", "Sektor", "ArbeidsTid", "Kjonn", "NACE2007", "Tid"]),
        # [mål][sektor][arbeidstid][kjønn][alder][år]
        "A": kube(A, ["MaaleMetode", "Sektor", "ArbeidsTid", "Kjonn", "Alder", "Tid"]),
        # [del][sektor][kjønn][næring][år], gjennomsnitt, alle arbeidstider
        "Kdel": [[k, K["etiketter"]["ContentsCode"][k]] for k in koder(K, "ContentsCode")],
        "K": kube(K, ["ContentsCode", "Sektor", "Kjonn", "NACE2007", "Tid"]),
        # [mål 01/11][yrke][næring][kjønn][2016, 2025]
        "YNaar": [int(a) for a in koder(YN, "Tid")],
        "YNyrke": [[k, YN["etiketter"]["Yrke"][k]] for k in yrker_yn],
        "YN": [[[[[hent(YN, MaaleMetode=m, Yrke=y, NACE2007=n, Kjonn=x, Tid=t) for t in koder(YN, "Tid")]
                  for x in "012"] for n in nar] for y in yrker_yn] for m in ("01", "11")],
        # [mål 01/11][yrke][kjønn][år], tosifret yrke, alle næringer
        "Y2yrke": [[k, Y2["etiketter"]["Yrke"][k]] for k in yrker2],
        "Y2": [[[[hent(Y2, MaaleMetode=m, Yrke=y, Kjonn=x, Tid=t) for t in aar] for x in "012"]
                for y in yrker2] for m in ("01", "11")],
    }
    UT.parent.mkdir(exist_ok=True)
    UT.write_text(json.dumps(ut, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(f"lonnutforsk: 5 datasett, {len(nar)} næringer, {len(yrker_yn)} yrkesgrupper, {len(yrker2)} tosifrede yrker. "
          f"Største avvik: K1 {AVVIK['K1']}, K2 {AVVIK['K2']} kr, K6 {AVVIK['K6']} kr. K3–K5 ok.")


if __name__ == "__main__":
    main()

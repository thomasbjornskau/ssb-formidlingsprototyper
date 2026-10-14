"""Lager build/regfram.json fra rådata i data/raw/ og kontrollerer summene.

Kjøres av felles/bygg.py. Stopper med feil hvis en kontroll ikke går opp:
- kommunene summerer til fylkene og fylkene til landet, alle år og alternativer
- aldersgruppene summerer til folkemengden
- endringen per år = fødte - døde + nettoinnvandring + innenlands nettoinnflytting
- kommunene summert per sentralitetsklasse = klassetallene i statistikkbanken
"""
import itertools
import json
import pathlib
import sys

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "regfram.json"

AAR = list(range(2026, 2051))
GRUPPER = ["F00-09", "F10-19", "F20-29", "F30-39", "F40-49", "F50-59", "F60-69", "F70-79", "F80-89", "F90-99", "F100G10+"]
GRUPPENAVN = ["0–9 år", "10–19 år", "20–29 år", "30–39 år", "40–49 år", "50–59 år", "60–69 år", "70–79 år", "80–89 år", "90 år og eldre"]


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
    verdier = d["value"]
    celler = {}
    for n, kombinasjon in enumerate(itertools.product(*koder)):
        celler[kombinasjon] = verdier.get(str(n)) if isinstance(verdier, dict) else verdier[n]
    etiketter = {dim: d["dimension"][dim]["category"].get("label", {}) for dim in d["id"]}
    return {"navn": navn, "celler": celler, "dims": d["id"], "koder": koder,
            "etiketter": etiketter, "oppdatert": d.get("updated", "")[:10]}


def hent(t, **fast):
    """Slår opp én verdi. Dimensjoner som ikke er oppgitt, må ha én kategori."""
    nokkel = []
    for dim, koder in zip(t["dims"], t["koder"]):
        if dim in fast:
            nokkel.append(str(fast[dim]))
        elif len(koder) == 1:
            nokkel.append(koder[0])
        else:
            feil(f"{t['navn']}: dimensjonen {dim} må velges")
    v = t["celler"].get(tuple(nokkel))
    if v is None:
        feil(f"{t['navn']}: mangler verdi for {fast}")
    return v


def koder(t, dim):
    return t["koder"][t["dims"].index(dim)]


def main():
    fm, km, al, se, na = (les(n) for n in ("folkemengde", "komponenter", "alder", "sentralitet", "nasjonal"))
    sentral = json.loads((RAW / "kommune_sentralitet.json").read_text(encoding="utf8"))["klasse"]
    hentet = json.loads((RAW / "_hentet.json").read_text(encoding="utf8"))["hentet"]

    regioner = koder(fm, "Region")
    navn = fm["etiketter"]["Region"]
    folk = {r: [[hent(fm, Region=r, ContentsCode=m, Tid=a) for a in AAR] for m in ("Personer", "Personer1", "Personer2")] for r in regioner}
    komp = {r: [[hent(km, Region=r, ContentsCode=m, Tid=a) for a in AAR[:-1]] for m in ("Fodt", "Dode", "Nettoinnvandring", "NettoinnflyttingInnl")] for r in regioner}
    alder = {}
    for r in regioner:
        v = [[hent(al, Region=r, Alder=g, Tid=a) for g in GRUPPER] for a in (2026, 2050)]
        alder[r] = [x[:9] + [x[9] + x[10]] for x in v]  # 90–99 og 100+ slås sammen

    kom = [r for r in regioner if len(r) == 4]
    fyl = [r for r in regioner if len(r) == 2]
    if "0" not in regioner or len(kom) + len(fyl) + 1 != len(regioner):
        feil("uventede regionkoder")
    if set(kom) != set(sentral):
        feil(f"kommunene i tabellen og i sentralitetskoblingen er ulike: {sorted(set(kom) ^ set(sentral))[:5]}")

    # Kontroller
    for i, a in enumerate(AAR):
        for m in range(3):
            if sum(folk[f][m][i] for f in fyl) != folk["0"][m][i]:
                feil(f"fylkene summerer ikke til landet, {a}")
            for f in fyl:
                if sum(folk[k][m][i] for k in kom if k[:2] == f) != folk[f][m][i]:
                    feil(f"kommunene i {f} summerer ikke til fylket, {a}")
    for r in regioner:
        if sum(alder[r][0]) != folk[r][0][0] or sum(alder[r][1]) != folk[r][0][-1]:
            feil(f"aldersgruppene i {r} summerer ikke til folkemengden")
        for i in range(len(AAR) - 1):
            f, d, iv, il = (komp[r][j][i] for j in range(4))
            if folk[r][0][i + 1] - folk[r][0][i] != f - d + iv + il:
                feil(f"komponentene i {r} forklarer ikke endringen {AAR[i]}–{AAR[i + 1]}")
    for kode in koder(se, "Region"):
        c = kode.split("-")[-1].zfill(2)
        for i, a in ((0, 2026), (-1, 2050)):
            if sum(folk[k][0][i] for k in kom if sentral[k] == c) != hent(se, Region=kode, Tid=a):
                feil(f"kommunene i sentralitetsklasse {c} summerer ikke til klassetallet, {a}")

    omrader = [[r, navn.get(r, r), "land" if r == "0" else "fylke" if len(r) == 2 else "kommune",
                r[:2] if len(r) == 4 else None, int(sentral[r]) if len(r) == 4 else None] for r in regioner]
    nasjonal = {k: [hent(na, Framskriv=alt, Tid=a) for a in (2026, 2050)] for k, alt in (("m", "MMM"), ("l", "LLL"), ("h", "HHH"))}
    data = {
        "kilde": {"14746": fm["oppdatert"], "14747": km["oppdatert"], "14740": na["oppdatert"], "hentet": hentet},
        "aar": AAR, "aldersgrupper": GRUPPENAVN, "omrader": omrader,
        "folk": folk, "komp": komp, "alder": alder, "nasjonal": nasjonal,
    }
    UT.parent.mkdir(exist_ok=True)
    UT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(f"regfram: kontroller ok, {len(kom)} kommuner, {len(fyl)} fylker")


if __name__ == "__main__":
    main()

"""Lager build/lonnansatt.json fra rådata i data/raw/ og kontrollerer tallene.

Kjøres av felles/bygg.py. Stopper med feil hvis en kontroll ikke går opp:
- K2  jobber for menn + kvinner = begge kjønn, alle yrker og år (11418)
- K3  snitt av firesifrede yrker vektet med heltidsekvivalenter ≈ publisert total (11418)
- K4  vekst regnet fra kroner = publiserte rater for 20 yrker i «Høyest lønnsvekst i toppen»
- K5  månedslønn = avtalt månedslønn + uregelmessige tillegg + bonus (11419)
- K6  median i 11419 = øvre grense for desil 5 i 13860
- K7  11419 og 11418 gir samme gjennomsnitt og median, utenom ett kjent avvik
- K8  gjennomsnittet ligger mellom grensene for desil 6 og 7, alle år
- K9  utbetalt årslønn: publisert endring ≈ endring regnet fra kroner (11536)
- K10 påløpt årslønn 2025 er 746 700 kr, +4,9 prosent, reallønn +1,8 (14858)
- K11 vekst i månedslønn regnet fra kroner = publiserte rater på statistikksiden, alle sektorer

Toleransene er satt etter de faktiske avvikene 15.10.2026, med litt margin.
Kronebeløpene er avrundet til 10 kr, endringer til én desimal.
"""
import itertools
import json
import pathlib
import sys

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "lonnansatt.json"
FRA = "2016"  # første sammenlignbare år. 2015 er per september og etter gammel arbeidstidsmetode.
HOVEDGRUPPER = ["1", "2", "3_01-03", "4", "5", "6", "7", "8", "9"]
SEKTORER = {"ALLE": "Alle sektorer", "6100": "Statsforvaltningen", "A+B+D+E": "Privat sektor og offentlig eide foretak",
            "6500": "Kommuneforvaltningen"}
AVVIK = {}


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


def hent(t, **fast):
    """Én verdi. Dimensjoner som ikke er oppgitt, tar første kode."""
    nokkel = tuple(fast[dim] if dim in fast else t["koder"][i][0] for i, dim in enumerate(t["dims"]))
    if nokkel not in t["celler"]:
        feil(f"{t['navn']}: finner ikke {fast}")
    return t["celler"][nokkel]


def symbol(t, **fast):
    nokkel = tuple(fast[dim] if dim in fast else t["koder"][i][0] for i, dim in enumerate(t["dims"]))
    return t["symbol"].get(nokkel)


def serie(t, tid, **fast):
    return [hent(t, Tid=x, **fast) for x in tid]


def koder(t, dim):
    return t["koder"][t["dims"].index(dim)]


def avvik(navn, verdi):
    AVVIK[navn] = max(AVVIK.get(navn, 0), verdi)


Y, H, D, U, P = les("yrker"), les("hovedtall"), les("desiler"), les("arslonn_utbetalt"), les("arslonn_palopt")
TID = [t for t in koder(Y, "Tid") if t >= FRA]
if koder(H, "Tid") != TID or koder(D, "Tid") != TID:
    feil("11418, 11419 og 13860 har ikke samme år")
SIST, FJOR = TID[-1], TID[-2]


def y(m, yrke, kj, aar):
    return hent(Y, MaaleMetode=m, Yrke=yrke, Sektor="ALLE", Kjonn=kj, AvtaltVanlig="0", ContentsCode="Manedslonn", Tid=aar)


def h(m, kj="0", sektor="ALLE", arb="0", c="Manedslonn", aar=SIST):
    return hent(H, MaaleMetode=m, Yrke="0-9", Sektor=sektor, Kjonn=kj, AvtaltVanlig=arb, ContentsCode=c, Tid=aar)


YRKER = koder(Y, "Yrke")
FIRE = [k for k in YRKER if len(k) == 4 and k != "0000"]

# ---------------------------------------------------------------- kontroller

# K2 Jobber: menn + kvinner = begge kjønn
n = 0
for k in YRKER:
    for a in TID:
        v = [y("10", k, kj, a) for kj in "012"]
        if None not in v:
            n += 1
            if v[1] + v[2] != v[0]:
                feil(f"K2 jobber menn + kvinner ≠ begge kjønn for {k} {a}: {v}")

# K3 Vektet snitt av firesifrede yrker (med heltidsekvivalenter) ≈ publisert total.
# Faktisk avvik 15.10.2026: 0,024 prosent i 2025 (62 085 mot 62 070) fordi undertrykte yrker mangler.
for a in TID:
    par = [(y("02", k, "0", a), y("11", k, "0", a)) for k in FIRE + ["0000"]]
    par = [(s, w) for s, w in par if s is not None and w is not None]
    vs = sum(s * w for s, w in par) / sum(w for _, w in par)
    rel = abs(vs / y("02", "0-9", "0", a) - 1) * 100
    avvik("K3 vektet snitt, prosent", rel)
    if rel > 0.1:
        feil(f"K3 vektet snitt av yrkene {vs:.0f} avviker {rel:.2f} prosent fra totalen i {a}")

# K4 Vekst per yrke fra kroner = publiserte rater (Strand og Bye, 05.02.2026, tabell 1 og 2)
PUB_YRKE = {"2223": 2.8, "2221": 2.7, "5329": 2.6, "5120": 3.0, "5321": 3.1, "2341": 3.6, "2212": 3.5,
            "2224": 3.4, "2330": 3.4, "5311": 3.3, "2413": 6.9, "1219": 5.9, "1120": 5.7, "2411": 5.7,
            "5246": 5.7, "1221": 5.5, "2422": 5.3, "2310": 5.3, "3313": 5.2, "3511": 5.2}
for k, p in PUB_YRKE.items():
    r = round((y("02", k, "0", SIST) / y("02", k, "0", FJOR) - 1) * 100, 1)
    if r != p:
        feil(f"K4 vekst for yrke {k} regnet fra kroner er {r}, publisert {p}")

# K5 Månedslønn = avtalt + uregelmessige tillegg + bonus. Faktisk største avvik 10 kr (avrunding).
for komb, v in H["celler"].items():
    d = dict(zip(H["dims"], komb))
    if d["ContentsCode"] != "Manedslonn" or d["MaaleMetode"] != "02":
        continue
    sum_ = sum(hent(H, **{**d, "ContentsCode": c}) for c in ("AvtaltManedslonn", "Uregtil", "Bonus"))
    avvik("K5 månedslønn mot delene, kr", abs(sum_ - v))
    if abs(sum_ - v) > 20:
        feil(f"K5 månedslønn {v} ≠ delene {sum_} for {d}")

# K6 Median = øvre grense desil 5
for kj in "012":
    for a in TID:
        if hent(D, Kjonn=kj, Desiler="05", ContentsCode="GrvManedslonn", Tid=a) != h("01", kj, aar=a):
            feil(f"K6 median ≠ grense desil 5 for kjønn {kj} {a}")

# K7 11419 = 11418 for alle yrker. Kjent avvik: menn 2023, 10 kr, trolig revisjon av 11418 28.08.2026.
KJENT = {("02", "1", "2023"), ("01", "1", "2023")}
for m in ("02", "01"):
    for kj in "012":
        for a in TID:
            ulik = h(m, kj, aar=a) != y(m, "0-9", kj, a)
            if ulik and (m, kj, a) not in KJENT:
                feil(f"K7 11419 og 11418 avviker for mål {m}, kjønn {kj}, {a}")
            if ulik:
                avvik("K7 kjente avvik 11419 mot 11418, kr", abs(h(m, kj, aar=a) - y(m, "0-9", kj, a)))

# K8 «Minst 6 av 10 under gjennomsnittet»: grense desil 6 < gjennomsnitt < grense desil 7
for a in TID:
    g6 = hent(D, Kjonn="0", Desiler="06", ContentsCode="GrvManedslonn", Tid=a)
    g7 = hent(D, Kjonn="0", Desiler="07", ContentsCode="GrvManedslonn", Tid=a)
    if not g6 < h("02", aar=a) < g7:
        feil(f"K8 gjennomsnittet ligger ikke mellom grensene for desil 6 og 7 i {a}")

# K9 Utbetalt årslønn: publisert endring ≈ regnet fra kroner. Faktisk største avvik under 0,05 prosentpoeng.
for s in koder(U, "Sektor"):
    for a in koder(U, "Tid")[2:]:
        pub = hent(U, Sektor=s, ContentsCode="ArslonnEndring", Tid=a)
        regn = (hent(U, Sektor=s, ContentsCode="Arslonn", Tid=a) / hent(U, Sektor=s, ContentsCode="Arslonn", Tid=str(int(a) - 1)) - 1) * 100
        avvik("K9 årslønn, prosentpoeng", abs(regn - pub))
        if abs(regn - pub) > 0.1:
            feil(f"K9 utbetalt årslønn {s} {a}: publisert {pub}, regnet {regn:.2f}")

# K10 Påløpt årslønn 2025
if (hent(P, ContentsCode="Arslonn", Tid="2025"), hent(P, ContentsCode="ArslonnEndring", Tid="2025"),
        hent(P, ContentsCode="ReallonnEndring", Tid="2025")) != (746700, 4.9, 1.8):
    feil("K10 påløpt årslønn 2025 er ikke 746 700 kr, +4,9 og reallønn +1,8")

# K11 Vekst i månedslønn regnet fra kroner = publiserte rater på statistikksiden (05.02.2026)
PUB_SEKTOR = {"ALLE": 4.5, "6100": 5.0, "A+B+D+E": 4.7, "6500": 3.4}
for s, p in PUB_SEKTOR.items():
    r = round((h("02", sektor=s) / h("02", sektor=s, aar=FJOR) - 1) * 100, 1)
    if r != p:
        feil(f"K11 vekst i månedslønn for {s} regnet fra kroner er {r}, publisert {p}")

# ---------------------------------------------------------------- byggfil

def rund(v, des=2):
    return None if v is None else round(v, des)


def yrkesserie(m, k, kj):
    return [y(m, k, kj, a) for a in TID]


def punkt(k):
    """Årene der yrket har «.» (ingen jobber), i motsetning til «:» (skjult)."""
    return [i for i, a in enumerate(TID) if symbol(Y, MaaleMetode="02", Yrke=k, Sektor="ALLE", Kjonn="0",
                                                   AvtaltVanlig="0", ContentsCode="Manedslonn", Tid=a) == "."]


ETIKETT = Y["etiketter"]["Yrke"]
yrker = []
for k in HOVEDGRUPPER + FIRE:
    # Høyskoleyrker (3) og militære yrker (0) ligger i samme hovedgruppe, «3_01-03»
    hg = k if k in HOVEDGRUPPER else ("3_01-03" if k[0] in "03" else k[0])
    yrker.append({
        "k": k, "n": ETIKETT[k], "g": hg,
        "s": [yrkesserie("02", k, kj) for kj in "012"],
        "m": [yrkesserie("01", k, kj) for kj in "012"],
        "q": [yrkesserie("051", k, "0"), yrkesserie("061", k, "0")],
        "j": [yrkesserie("10", k, kj) for kj in "012"],
        "p": punkt(k),
    })

desil = {}
for kj in "012":
    desil[kj] = {
        "snitt": [[hent(D, Kjonn=kj, Desiler=dk, ContentsCode="Manedslonn", Tid=a) for a in TID] for dk in koder(D, "Desiler")],
        "grense": [[hent(D, Kjonn=kj, Desiler=dk, ContentsCode="GrvManedslonn", Tid=a) for a in TID] for dk in koder(D, "Desiler")],
    }

tot = {
    "snitt": {kj: [h("02", kj, aar=a) for a in TID] for kj in "012"},
    "median": {kj: [h("01", kj, aar=a) for a in TID] for kj in "012"},
    "jobber": {kj: [h("10", kj, aar=a) for a in TID] for kj in "012"},
    "hte": {kj: [h("11", kj, aar=a) for a in TID] for kj in "012"},
    "deler": {kj: {c: [h("02", kj, c=c, aar=a) for a in TID] for c in ("AvtaltManedslonn", "Uregtil", "Bonus", "Overtid", "AvtArbTid")} for kj in "012"},
    "arbeidstid": {arb: {kj: {"snitt": h("02", kj, arb=arb), "jobber": h("10", kj, arb=arb), "hte": h("11", kj, arb=arb)}
                         for kj in "012"} for arb in ("0", "5", "6")},
    "sektor": {s: [h("02", sektor=s, aar=a) for a in TID] for s in SEKTORER},
}
arslonn = {
    "tid": koder(U, "Tid"),
    "utbetalt": {s: {"v": serie(U, koder(U, "Tid"), Sektor=s, ContentsCode="Arslonn"),
                     "e": serie(U, koder(U, "Tid"), Sektor=s, ContentsCode="ArslonnEndring")} for s in SEKTORER},
    "palopt_tid": koder(P, "Tid"),
    "palopt": {c: serie(P, koder(P, "Tid"), ContentsCode=c) for c in ("Arslonn", "ArslonnEndring", "ReallonnEndring")},
}
ut = {
    "hentet": "2026-10-15",
    "oppdatert": {"11418": Y["oppdatert"], "11419": H["oppdatert"], "13860": D["oppdatert"], "11536": U["oppdatert"], "14858": P["oppdatert"]},
    "tid": TID, "sektorer": SEKTORER, "hovedgrupper": HOVEDGRUPPER,
    "publisert_sektorvekst": PUB_SEKTOR,
    "tot": tot, "desil": desil, "desilkoder": koder(D, "Desiler"), "arslonn": arslonn, "yrker": yrker,
}
UT.parent.mkdir(exist_ok=True)
UT.write_text(json.dumps(ut, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
med = sum(1 for r in yrker if r["k"] in FIRE and r["s"][0][-1] is not None)
print(f"build/lonnansatt.json: {round(UT.stat().st_size / 1024)} kB, {len(FIRE)} yrker ({med} med tall i {SIST}), "
      f"{n} kjønnssummer kontrollert. Største avvik: "
      + ", ".join(f"{k} {v:.3f}".replace(".", ",") for k, v in AVVIK.items()))

"""Datasteget for formidlingsprototypen ufore.

Bruk:  python ufore/scripts/lag_data.py
Leser ufore/data/raw/*.json, kjører kontrollene og skriver ufore/build/ufore.json (kompakt).
Stopper med «Kontroll feilet: …» hvis en kontroll ikke holder. Bare Pythons standardbibliotek.
"""

import itertools
import json
import os
import sys
from collections import defaultdict
from itertools import permutations

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROT, "data", "raw")
AR = [str(a) for a in range(2015, 2026)]
ALDRE = list(range(18, 68))
KJONN = {"0": "begge", "2": "kvinner", "1": "menn"}
avvik_logg = []


def feil(melding):
    sys.exit("Kontroll feilet: " + melding)


def les(ds_id):
    """json-stat2 til (dimensjons-id-er, kategorier, {nøkkeltuppel: (verdi, status)}, oppdatert)."""
    d = json.load(open(os.path.join(RAW, ds_id + ".json"), encoding="utf-8"))
    kat = [d["dimension"][i]["category"] for i in d["id"]]
    nokler = [sorted(c["index"], key=c["index"].get) for c in kat]
    st = d.get("status") or {}
    verdier = {k: (d["value"][n], st.get(str(n))) for n, k in enumerate(itertools.product(*nokler))}
    return d["id"], kat, verdier, d.get("updated", "")[:10]


def dato(iso):
    return f"{iso[8:10]}.{iso[5:7]}.{iso[:4]}" if iso else ""


def kontroll(navn, avvik, toleranse, forklaring):
    avvik_logg.append((navn, avvik, toleranse))
    if avvik > toleranse:
        feil(f"{navn}: største avvik {avvik} er over toleransen {toleranse} ({forklaring})")


oppdatert = {}

# ---------------- Landsnivå ----------------
_, _, V, oppdatert["11695"] = les("land_kjonn")
land = {KJONN[k]: {"antall": [V[("0", k, "UforetygdPers", a)][0] for a in AR],
                   "andel": [V[("0", k, "UforetrygdPros", a)][0] for a in AR]} for k in KJONN}
kontroll("K1 kvinner + menn = begge (land)",
         max(abs(land["kvinner"]["antall"][i] + land["menn"]["antall"][i] - land["begge"]["antall"][i]) for i in range(11)),
         0, "kjønn skal summere eksakt")

_, _, V, oppdatert["11824"] = les("bosetting")
bosetting = {n: [V[(k, "UforetrygdPers", a)][0] for a in AR] for k, n in (("0", "i_alt"), ("1", "bosatt"), ("2", "ikke_bosatt"))}
# Tabellene lages fra ulike datamatriser, og enere og toere erstattes med 0 eller 3 i hver av dem
# («Om statistikken»). Avvik på noen få personer mellom tabellene er derfor ventet.
kontroll("K2 bosatt (11824) = antall (11695)", max(abs(bosetting["bosatt"][i] - land["begge"]["antall"][i]) for i in range(11)), 5,
         "konfidensialitetsavrunding mellom tabeller")

# Alder × kjønn
_, _, V, oppdatert["11828"] = les("alder")
alder = {KJONN[k]: {"antall": [[V[(k, f"{y:03d}", "UforetrygdPers", a)][0] for a in AR] for y in ALDRE],
                    "andel": [[V[(k, f"{y:03d}", "UforetrygdPros", a)][0] for a in AR] for y in ALDRE]} for k in KJONN}
kontroll("K3 sum ettårige aldre = 18–67 (11828)",
         max(abs(sum(alder[KJONN[k]]["antall"][j][i] for j in range(50)) - V[(k, "18-67", "UforetrygdPers", AR[i])][0])
             for k in KJONN for i in range(11)), 0, "aldrene skal summere eksakt")
kontroll("K4 alder (11828) = land (11695)",
         max(abs(sum(alder["begge"]["antall"][j][i] for j in range(50)) - land["begge"]["antall"][i]) for i in range(11)), 0,
         "samme populasjon")

# Befolkning land: statistikkår t = 07459 per 1.1. t+1
_, _, V, oppdatert["07459"] = les("befolkning_land")
bef = {(s, y, a): V[("0", s, f"{y:03d}", "Personer1", str(int(a) + 1))][0] for s in ("1", "2") for y in ALDRE for a in AR}
for s in ALDRE:
    pass
bef_k = lambda s, y, a: bef[("1", y, a)] + bef[("2", y, a)] if s == "0" else bef[(s, y, a)]

# K5 nevneren: egen andel = publisert andel for alle celler (avrundet til én desimal)
st = max(abs(round(alder[KJONN[s]]["antall"][j][i] / bef_k(s, y, a) * 100, 1) - alder[KJONN[s]]["andel"][j][i])
         for s in KJONN for j, y in enumerate(ALDRE) for i, a in enumerate(AR))
kontroll("K5 egen andel per alder og kjønn = publisert (nevner 07459 1.1. året etter)", round(st, 3), 0.051,
         "avrunding til én desimal gir høyst 0,05")
bef18_67 = [sum(bef_k("0", y, a) for y in ALDRE) for a in AR]

# Dekomponering 2015–2025: befolkningsvekst (N), alderssammensetning (s), andel per alder (r).
# Snitt over alle seks rekkefølger (Shapley). Aldre × kjønn som celler.
celler = [(s, y) for s in ("1", "2") for y in ALDRE]


def komponenter(a):
    N = sum(bef[(s, y, a)] for s, y in celler)
    andel = {c: bef[(c[0], c[1], a)] / N for c in celler}
    rate = {c: alder[KJONN[c[0]]]["antall"][ALDRE.index(c[1])][AR.index(a)] / bef[(c[0], c[1], a)] for c in celler}
    return {"N": N, "s": andel, "r": rate}


def modell(v):
    return v["N"] * sum(v["s"][c] * v["r"][c] for c in celler)


def shapley(a0, a1):
    v0, v1 = komponenter(a0), komponenter(a1)
    bidrag = {"N": 0.0, "s": 0.0, "r": 0.0}
    rekkefolger = list(permutations("Nsr"))
    for rf in rekkefolger:
        cur = dict(v0)
        forrige = modell(cur)
        for x in rf:
            cur[x] = v1[x]
            ny = modell(cur)
            bidrag[x] += (ny - forrige) / len(rekkefolger)
            forrige = ny
    return bidrag


dek = shapley("2015", "2025")
tot = land["begge"]["antall"][10] - land["begge"]["antall"][0]
kontroll("K6 dekomponeringen summerer til endringen", round(abs(sum(dek.values()) - tot), 3), 0.5,
         "flyttall; modellen gjenskaper antallet eksakt")
dekomp = {"fra": "2015", "til": "2025", "endring": tot, "befolkningsvekst": round(dek["N"]),
          "aldring": round(dek["s"]), "hoyere_andel": round(dek["r"])}

# ---------------- Tabeller etter aldersgruppe ----------------
def tabell(ds_id, dimkode, utelat_region=True):
    ids, kat, V, upd = les(ds_id)
    return ids, kat, V, upd


ids, kat, V, oppdatert["11850"] = les("arbeid")
grp7 = sorted(kat[2]["index"], key=kat[2]["index"].get)
arbeid = {KJONN[k]: {g: {i: [V[("0", k, g, i, "UforetrygdPros", a)][0] for a in AR] for i in ("01", "02", "03", "04")}
                     for g in grp7} for k in KJONN}
arbeid_antall = {KJONN[k]: {g: [V[("0", k, g, "00", "UforetrygdPers", a)][0] for a in AR] for g in grp7} for k in KJONN}
kontroll("K7 arbeidsintensitet summerer til 100 prosent",
         round(max(abs(sum(arbeid[k][g][i][n] for i in ("01", "02", "03", "04")) - 100) for k in arbeid for g in grp7 for n in range(11)), 2),
         0.21, "fire avrundede andeler kan avvike opptil 0,2")

ids, kat, V, oppdatert["11696"] = les("uforegrad")
grp6 = sorted(kat[2]["index"], key=kat[2]["index"].get)
grad = {KJONN[k]: {g: {i: [V[("0", k, g, i, "UforetrygdPros", a)][0] for a in AR] for i in ("01", "02", "03")} for g in grp6}
        for k in KJONN}

ids, kat, V, oppdatert["11714"] = les("utdanning")
nivaer = sorted(kat[2]["index"], key=kat[2]["index"].get)
utd = {KJONN[k]: {g: {n: {"antall": [V[(k, g, n, "UforetygdPers", a)][0] for a in AR],
                          "andel": [V[(k, g, n, "UforetrygdPros", a)][0] for a in AR]} for n in nivaer} for g in grp7}
       for k in KJONN}
kontroll("K8 utdanningsnivåene summerer til i alt",
         max(abs(sum(utd[k][g][n]["antall"][i] for n in nivaer[1:]) - utd[k][g]["TOT"]["antall"][i])
             for k in utd for g in grp7 for i in range(11)), 0, "nivåene skal summere eksakt")

ids, kat, V, oppdatert["11736"] = les("nye")
grp8 = sorted(kat[2]["index"], key=kat[2]["index"].get)
nye = {KJONN[k]: {g: {"antall": [V[("0", k, g, "UforetygdPers", a)][0] for a in AR],
                      "andel": [V[("0", k, g, "UforetrygdPros", a)][0] for a in AR]} for g in grp8} for k in KJONN}

# ---------------- Kommuner og fylker ----------------
ids, kat, R, _ = les("regioner")
rnavn = kat[0]["label"]
regkoder = sorted(kat[0]["index"], key=kat[0]["index"].get)
gyldig = {a: [r for r in regkoder if len(r) == 4 and R[(r, "0", "UforetrygdPros", a)][1] is None] for a in AR}
fylker25 = [r for r in regkoder if len(r) == 2 and R[(r, "0", "UforetrygdPros", "2025")][1] is None]
for a in AR:
    s = sum(R[(r, "0", "UforetygdPers", a)][0] for r in gyldig[a])
    kontroll(f"K9 kommunene summerer til landet {a}", abs(s - land["begge"]["antall"][AR.index(a)]), 0, "eksakt")
    if any(R[(r, "0", "UforetrygdPros", a)][1] == "." and R[(r, "0", "UforetygdPers", a)][0] != 0
           for r in regkoder if len(r) == 4):
        feil(f"antall ulikt 0 for en kommune med «.» i andelen, {a}")

# Klass-endringer, i datorekkefølge
endr = json.load(open(os.path.join(RAW, "klass_kommuneendringer.json"), encoding="utf-8"))["codeChanges"]
per_dato = defaultdict(lambda: defaultdict(set))
for e in endr:
    per_dato[e["changeOccurred"]][e["oldCode"]].add(e["newCode"])
datoer = sorted(per_dato)


def til_2025(kode, ar):
    """Mengden 2025-kommunekoder som kommunekode i statistikkår «ar» er blitt til."""
    m = {kode}
    for dt in datoer:
        if int(dt[:4]) > int(ar):
            m = set().union(*[per_dato[dt].get(x, {x}) for x in m])
    return m


gyldig25 = set(gyldig["2025"])
koblinger = {}
for a in AR:
    for r in gyldig[a]:
        mål = til_2025(r, a)
        if not mål <= gyldig25:
            feil(f"kommune {r} ({a}) blir til {mål}, som ikke er gyldige 2025-koder")
        koblinger[(r, a)] = mål
delt = {(r, a): m for (r, a), m in koblinger.items() if len(m) > 1}

# Befolkning per kommune: statistikkår a bruker 07459 per 1.1. a+1, i kommuneinndelingen per 1.1. a+1.
befk = {}       # (kommunekode i befolkningsfilen, kjønn, alder, a) -> personer
befkoder = {}   # a -> kodene i befolkningsfilen
for a in AR:
    _, katp, P, oppdatert["07459k"] = les(f"befolkning_kommuner_{a}")
    befkoder[a] = sorted(katp[0]["index"], key=katp[0]["index"].get)
    for (reg, s, y, _, _), (v, stt) in P.items():
        befk[(reg, s, int(y), a)] = v or 0
    sum_bef = sum(befk[(r, s, y, a)] for r in befkoder[a] for s in ("1", "2") for y in ALDRE)
    kontroll(f"K10 befolkning i kommunene = landet 18–67 {a}", abs(sum_bef - bef18_67[AR.index(a)]), 0, "eksakt")


def befolkning_ar(a):
    return str(min(int(a) + 1, 2025))


# Harmonisert antall og befolkning per 2025-kommune
nk = {k: {"antall": [None] * 11, "bef": [None] * 11, "forv": [None] * 11} for k in gyldig25}
mangler = {k: set() for k in gyldig25}
for (r, a), m in delt.items():
    for k in m:
        mangler[k].add(a)
for i, a in enumerate(AR):
    sum_a = defaultdict(int); sum_b = defaultdict(int); sum_f = defaultdict(float)
    rate = {(s, y): alder[KJONN[s]]["antall"][ALDRE.index(y)][i] / bef[(s, y, a)] for s in ("1", "2") for y in ALDRE}
    for r in gyldig[a]:
        mål = koblinger[(r, a)]
        if len(mål) == 1:
            sum_a[next(iter(mål))] += R[(r, "0", "UforetygdPers", a)][0]
    for r in befkoder[a]:
        mål = til_2025(r, befolkning_ar(a))
        if not mål <= gyldig25:
            feil(f"befolkningskode {r} ({a}) blir til {mål}, som ikke er gyldige 2025-koder")
        if len(mål) > 1:
            if not all(a in mangler[k] for k in mål):
                feil(f"befolkningskode {r} ({a}) er delt, men målkommunene mangler ikke uføretall")
            continue
        k = next(iter(mål))
        sum_b[k] += sum(befk[(r, s, y, a)] for s in ("1", "2") for y in ALDRE)
        sum_f[k] += sum(rate[(s, y)] * befk[(r, s, y, a)] for s in ("1", "2") for y in ALDRE)
    for k in gyldig25:
        if a not in mangler[k]:
            nk[k]["antall"][i], nk[k]["bef"][i], nk[k]["forv"][i] = sum_a[k], sum_b[k], sum_f[k]
    # Utelatt: alle gamle kommuner som helt eller delvis ble til en kommune uten sammenlignbar serie i år a
    rest = sum(R[(r, "0", "UforetygdPers", a)][0] for r in gyldig[a] if any(a in mangler[k] for k in koblinger[(r, a)]))
    s = sum(v["antall"][i] for v in nk.values() if v["antall"][i] is not None)
    kontroll(f"K11 harmonisert sum + delte kommuner = landet {a}", abs(s + rest - land["begge"]["antall"][i]), 0, "eksakt")

# Egen andel 2024 og 2025 (ingen omkoding) = publisert
# Unntak: grensejustering mellom Risør og Tvedestrand 1.1.2025. Befolkningen per 1.1.2025 har de nye grensene,
# uføretallene for 2024 de gamle. Avviket er 0,3 prosentpoeng. Prototypen bruker publisert andel for 2024–2025.
GRENSEJUSTERT = {("4201", "2024"), ("4213", "2024")}
st = max(abs(round(nk[k]["antall"][i] / nk[k]["bef"][i] * 100, 1) - R[(k, "0", "UforetrygdPros", AR[i])][0])
         for k in gyldig25 for i in (9, 10) if (k, AR[i]) not in GRENSEJUSTERT)
kontroll("K12 egen kommuneandel 2024–2025 = publisert", round(st, 3), 0.051, "avrunding til én desimal")
# Forventet sum over kommuner = landets antall (indirekte standardisering skal gå i null for landet)
for i, a in enumerate(AR):
    if i < 9:
        continue
    f = sum(v["forv"][i] for v in nk.values())
    kontroll(f"K13 sum forventet = landets antall {a}", round(abs(f - land["begge"]["antall"][i]), 2), 0.5, "flyttall")


def fylke25(k):
    return k[:2]


fylker = {}
for f in fylker25:
    ks = [k for k in gyldig25 if fylke25(k) == f]
    rad = {"antall": [], "bef": [], "forv": []}
    for i, a in enumerate(AR):
        rate = {(s, y): alder[KJONN[s]]["antall"][ALDRE.index(y)][i] / bef[(s, y, a)] for s in ("1", "2") for y in ALDRE}
        ant = b = fv = 0
        for r in gyldig[a]:
            m = koblinger[(r, a)]
            if len({fylke25(x) for x in m}) > 1:
                feil(f"kommune {r} ({a}) er delt mellom flere fylker")
            if fylke25(next(iter(m))) == f:
                ant += R[(r, "0", "UforetygdPers", a)][0]
        for r in befkoder[a]:
            m = til_2025(r, befolkning_ar(a))
            if fylke25(next(iter(m))) == f:
                b += sum(befk[(r, s, y, a)] for s in ("1", "2") for y in ALDRE)
                fv += sum(rate[(s, y)] * befk[(r, s, y, a)] for s in ("1", "2") for y in ALDRE)
        rad["antall"].append(ant); rad["bef"].append(b); rad["forv"].append(fv)
    fylker[f] = rad
    for i in (9, 10):
        kontroll(f"K14 fylke {f} {AR[i]} = publisert", abs(rad["antall"][i] - R[(f, "0", "UforetygdPers", AR[i])][0]), 0, "eksakt")
for i in range(11):
    kontroll(f"K15 fylkene summerer til landet {AR[i]}", abs(sum(v["antall"][i] for v in fylker.values()) - land["begge"]["antall"][i]), 0, "eksakt")


def rund(x, d=1):
    return None if x is None else round(x, d)


def region_ut(navn, v, kvinner=None, menn=None):
    return {"navn": navn,
            "antall": v["antall"],
            "andel": [rund(v["antall"][i] / v["bef"][i] * 100) if v["antall"][i] is not None else None for i in range(11)],
            "indeks": [round(v["antall"][i] / v["forv"][i] * 100) if v["antall"][i] is not None and v["forv"][i] else None for i in range(11)],
            "forventet": [rund(v["forv"][i] / v["bef"][i] * 100) if v["antall"][i] is not None else None for i in range(11)],
            "bef": v["bef"][10]}


def rent_navn(n):
    return n.split(" (")[0]


def publisert_siste(reg, rad):
    """2024–2025 er uten omkoding: bruk publisert andel der."""
    for i in (9, 10):
        rad["andel"][i] = R[(reg, "0", "UforetrygdPros", AR[i])][0]
    return rad


kommuner_ut = {k: dict(publisert_siste(k, region_ut(rent_navn(rnavn[k]), nk[k])), fylke=fylke25(k),
                        kvinner=R[(k, "2", "UforetrygdPros", "2025")][0], menn=R[(k, "1", "UforetrygdPros", "2025")][0],
                        mangler=sorted(mangler[k]))
               for k in sorted(gyldig25)}
fylker_ut = {f: dict(region_ut(rent_navn(rnavn[f]), fylker[f]),
                     kvinner=R[(f, "2", "UforetrygdPros", "2025")][0], menn=R[(f, "1", "UforetrygdPros", "2025")][0])
             for f in fylker25}
delinger = sorted({(r, a, tuple(sorted(m))) for (r, a), m in delt.items()}, key=lambda x: (x[1], x[0], x[2]))
delinger_ut = []
for r, a, m in delinger:
    if not any(d["kode"] == r and d["til"] == list(m) for d in delinger_ut):
        delinger_ut.append({"kode": r, "navn": rent_navn(rnavn[r]), "til": list(m), "siste_ar": a})
    else:
        next(d for d in delinger_ut if d["kode"] == r and d["til"] == list(m))["siste_ar"] = a

# Kontroll: egne andeler i 2025 stemmer med publisert for fylkene
st = max(abs(fylker_ut[f]["andel"][10] - R[(f, "0", "UforetrygdPros", "2025")][0]) for f in fylker25)
kontroll("K16 egen fylkesandel 2025 = publisert", round(st, 3), 0.051, "avrunding")

ut = {
    "ar": AR,
    "oppdatert": {k: dato(v) for k, v in oppdatert.items()},
    "land": land,
    "befolkning": bef18_67,
    "bosetting": bosetting,
    "nav_2025": 374900,
    "dekomponering": dekomp,
    "alder": alder,
    "arbeid": arbeid, "arbeid_antall": arbeid_antall, "grupper7": grp7,
    "grad": grad, "grupper6": grp6,
    "utdanning": utd, "nivaer": nivaer,
    "nye": nye, "grupper8": grp8,
    "kommuner": kommuner_ut,
    "fylker": fylker_ut,
    "delinger": delinger_ut,
}
os.makedirs(os.path.join(ROT, "build"), exist_ok=True)
with open(os.path.join(ROT, "build", "ufore.json"), "w", encoding="utf-8") as f:
    json.dump(ut, f, ensure_ascii=False, separators=(",", ":"), sort_keys=True)

storst = max(avvik_logg, key=lambda x: x[1] / x[2] if x[2] else (0 if x[1] == 0 else 1e9))
print(f"{len(avvik_logg)} kontroller bestått. Største relative avvik: {storst[0]} = {storst[1]} (toleranse {storst[2]}). "
      f"Dekomponering: {dekomp}. Kommuner: {len(kommuner_ut)}, fylker: {len(fylker_ut)}, delinger: {len(delinger_ut)}.")

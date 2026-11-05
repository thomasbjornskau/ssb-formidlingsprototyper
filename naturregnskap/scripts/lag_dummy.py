"""Lager DUMMYDATA i json-stat2 for naturregnskap, med samme tabellnumre som i den interne statistikkbanken.

ALLE TALL OG KODELISTER ER OPPDIKTET. Tabellene publiseres 25.11.2026. Da erstattes filene i data/raw/
med ekte svar fra hent_data.py. Strukturen følger tabelltitlene, ikke de faktiske kodelistene.
Bare standardbiblioteket."""
import json, os, itertools

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
NOTE = "DUMMYDATA: oppdiktede tall og koder for å bygge prototypen før publisering 25.11.2026. Erstattes av ekte data."
UPDATED = "2026-11-05T12:00:00Z"

OKO = [("01", "Bebygd og opparbeidet areal"), ("02", "Jordbruksmark"), ("03", "Åpent lavland"), ("04", "Skog"),
       ("05", "Fastmark i fjellet"), ("06", "Våtmark"), ("07", "Elver og bekker"), ("08", "Innsjøer og dammer"),
       ("09", "Kyststrender"), ("10", "Kystvann"), ("11", "Åpent hav")]
OKO_T = [("00", "I alt")] + OKO
LD = [("0", "Hele landet"), ("1", "Øst"), ("2", "Sør"), ("3", "Vest"), ("4", "Midt"), ("5", "Nord")]
EG = [("TOT", "Totalindeks"), ("A1", "Fysiske egenskaper"), ("A2", "Kjemiske egenskaper"), ("B1", "Biologisk mangfold"),
      ("B2", "Strukturelle egenskaper"), ("B3", "Funksjonelle egenskaper"), ("C1", "Landskapsegenskaper")]


def jsonstat(label, dims, values, status=None, unit="", extra=None):
    """dims: list of (id, label, [(code, label)]); values: dict keyed by tuple of codes -> value or None."""
    ids = [d[0] for d in dims]
    size = [len(d[2]) for d in dims]
    vals, stat = [], {}
    for i, combo in enumerate(itertools.product(*[[c for c, _ in d[2]] for d in dims])):
        v = values.get(combo)
        if v is None or isinstance(v, str):
            vals.append(None)
            stat[str(i)] = v if isinstance(v, str) else ".."
        else:
            vals.append(v)
    out = {"version": "2.0", "class": "dataset", "label": label, "source": "Statistisk sentralbyrå", "updated": UPDATED,
           "note": [NOTE], "id": ids, "size": size,
           "dimension": {d[0]: {"label": d[1], "category": {"index": {c: k for k, (c, _) in enumerate(d[2])},
                                                             "label": {c: l for c, l in d[2]}}} for d in dims},
           "value": vals}
    if stat:
        out["status"] = stat
    if unit:
        out["extension"] = {"enhet": unit}
    if extra:
        out["extension"] = {**out.get("extension", {}), **extra}
    return out


def save(name, obj):
    os.makedirs(RAW, exist_ok=True)
    json.dump(obj, open(os.path.join(RAW, name + ".json"), "w"), ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- utbredelse (tabellnummer ukjent)
AREAL = {"01": 650, "02": 1100, "03": 2600, "04": 12100, "05": 10300, "06": 2300, "07": 150, "08": 1900, "09": 80,
         "10": 9000, "11": 200000}  # 1000 hektar
UTBYGD = {"01": ".", "02": 6500, "03": 4000, "04": 18000, "05": 3500, "06": 2000, "07": 0, "08": 0, "09": 0, "10": ".", "11": "."}  # hektar 2017–2024
v = {}
for c, _ in OKO:
    v[(c, "Areal")] = AREAL[c]
    v[(c, "Utbygd")] = UTBYGD[c]
v[("00", "Areal")] = sum(AREAL.values())
v[("00", "Utbygd")] = sum(x for x in UTBYGD.values() if not isinstance(x, str))
save("utbredelse", jsonstat("Utbredelse og utbygd areal, etter økosystemtype. Hele landet (DUMMY)",
                            [("Okosystem", "økosystemtype", OKO_T), ("ContentsCode", "statistikkvariabel",
                              [("Areal", "Areal 2024 (1000 hektar)"), ("Utbygd", "Utbygd areal 2017–2024 (hektar)")])], v))

# ---------------------------------------------------------------- tilstand
def tilstand(tab, label, eko, years, regions, data):
    vv = {}
    for (e, r, y, g), x in data.items():
        vv[(e, g, r, y)] = x
    dims = [("Okosystem", "økosystemtype", eko), ("Egenskap", "tilstandsegenskap", EG),
            ("Region", "landsdel", regions), ("Tid", "år", [(y, y) for y in years])]
    save(tab, jsonstat(label, dims, vv, unit="skalert 0–1"))


def profil(vals_by_eg):
    d = {g: x for g, x in vals_by_eg.items()}
    if d:
        d["TOT"] = round(sum(d.values()) / len(d), 2)
    return d


SKOG = {"2019": {"A1": .70, "A2": .80, "B1": .44, "B2": .28, "B3": .50, "C1": .28},
        "2024": {"A1": .71, "A2": .82, "B1": .45, "B2": .31, "B3": .52, "C1": .33}}
SKOG_LD = {"1": (.47, .49), "2": (.52, .53), "3": (.55, .56), "4": (.51, .53), "5": (.54, .55)}
FJELL = {"2019": {"A1": .80, "B1": .64, "B3": .68, "C1": .76}, "2024": {"A1": .78, "B1": .62, "B3": .66, "C1": .74}}
FJELL_LD = {"1": (.69, .67), "2": (.70, .69), "3": (.73, .71), "4": (.72, .70), "5": (.74, .72)}
for tab, lab, code, name, base, ld in [("15012", "Tilstandsregnskap for skog (DUMMY)", "04", "Skog", SKOG, SKOG_LD),
                                       ("15013", "Tilstandsregnskap for fastmark i fjellet (DUMMY)", "05", "Fastmark i fjellet", FJELL, FJELL_LD)]:
    d = {}
    for y in ("2019", "2024"):
        for g, x in profil(base[y]).items():
            d[(code, "0", y, g)] = x
        for r, (a, b) in ld.items():
            d[(code, r, y, "TOT")] = a if y == "2019" else b
    tilstand(tab, lab, [(code, name)], ["2019", "2024"], LD, d)

# 15014 åpent lavland og jordbruksmark: egenskaper, ingen totalindeks
d = {}
for code, eg in [("03", {"B1": .55, "B2": .48, "B3": .60}), ("02", {"A2": .64, "B1": .41, "B3": .52})]:
    for g, x in eg.items():
        d[(code, "0", "2024", g)] = x
    d[(code, "0", "2024", "TOT")] = "."
tilstand("15014", "Tilstandsregnskap for åpent lavland og jordbruksmark (DUMMY)", [("02", "Jordbruksmark"), ("03", "Åpent lavland")],
         ["2024"], LD[:1], d)

# 15015 våtmark: bare Naturindeks per landsdel
d = {}
for r, (a, b) in {"0": (.63, .62), "1": (.58, .57), "2": (.61, .60), "3": (.66, .65), "4": (.64, .62), "5": (.65, .65)}.items():
    d[("06", r, "2019", "TOT")] = a
    d[("06", r, "2024", "TOT")] = b
tilstand("15015", "Tilstandsregnskap for våtmark (Naturindeks) (DUMMY)", [("06", "Våtmark")], ["2019", "2024"], LD, d)

# 15016 vassdrag og kystvann
d = {}
for code, eg in [("07", {"A2": .75, "B1": .61, "B3": .68}), ("08", {"A1": .80, "A2": .78, "B1": .66, "B3": .72}),
                 ("10", {"A1": .70, "A2": .72, "B1": .58, "B3": .64})]:
    for g, x in profil(eg).items():
        d[(code, "0", "2024", g)] = x
tilstand("15016", "Tilstandsregnskap for vassdrag og kystvann (DUMMY)",
         [("07", "Elver og bekker"), ("08", "Innsjøer og dammer"), ("10", "Kystvann")], ["2024"], LD[:1], d)

# ---------------------------------------------------------------- tjenester
TJ = [("AVL", "Forsyning av avlinger", "1000 tonn"), ("TOM", "Forsyning av tømmer", "1000 m³"),
      ("POL", "Pollinering av avlinger", "1000 tonn"), ("KLI", "Global klimaregulering", "1000 tonn CO₂-ekvivalenter"),
      ("TMP", "Temperaturregulering i byer", "grader celsius"), ("FLO", "Flomdemping", "hektar"),
      ("LUF", "Luftrensing", "1000 tonn"), ("TUR", "Naturbasert turisme", "1000 overnattinger"),
      ("REK", "Naturbasert rekreasjon", "1000 dagsturer")]
TILGANG = {"AVL": {"02": 4200}, "TOM": {"04": 10800}, "POL": {"02": 95},
           "KLI": {"04": 21000, "03": 400, "05": 200, "01": 300},
           "TMP": {"04": 1.2, "01": 0.8, "08": 0.2},
           "FLO": {"04": 600000, "06": 250000, "02": 80000, "03": 50000},
           "LUF": {"04": 9.5, "03": 1.2, "01": 0.6, "02": 0.4, "05": 0.8},
           "TUR": {"05": 4200, "04": 2600, "09": 1800, "10": 1500, "08": 500},
           "REK": {"04": 95000, "05": 30000, "09": 18000, "08": 9000, "01": 22000, "10": 8000, "03": 6000}}
v = {}
for t, _, _ in TJ:
    for c, _ in OKO:
        v[(t, c)] = TILGANG[t].get(c, 0)
    v[(t, "00")] = round(sum(TILGANG[t].values()), 3)
save("14967", jsonstat("Regnskap for økosystemtjenester, etter tilgang fra økosystemtype 2024 (DUMMY)",
                       [("Tjeneste", "økosystemtjeneste", [(t, n) for t, n, _ in TJ]), ("Okosystem", "økosystemtype", OKO_T)], v,
                       extra={"enheter": {t: u for t, _, u in TJ}}))

BR = [("NAER", "Næringer"), ("HUS", "Husholdninger"), ("OFF", "Offentlig forvaltning"), ("EKS", "Eksport")]
ANDEL = {"AVL": {"NAER": 1}, "TOM": {"NAER": 1}, "POL": {"NAER": 1}, "KLI": {"OFF": 1}, "TMP": {"HUS": 1},
         "FLO": {"HUS": 1}, "LUF": {"HUS": 1}, "TUR": {"HUS": .45, "EKS": .55}, "REK": {"HUS": 1}}
v = {}
for t, _, _ in TJ:
    tot = round(sum(TILGANG[t].values()), 3)
    for b, _ in BR:
        v[(t, b)] = round(tot * ANDEL[t].get(b, 0), 3)
    v[(t, "TOT")] = tot
save("14968", jsonstat("Regnskap for økosystemtjenester, etter anvendelse fra økonomisk enhet 2024 (DUMMY)",
                       [("Tjeneste", "økosystemtjeneste", [(t, n) for t, n, _ in TJ]), ("Bruker", "økonomisk enhet", [("TOT", "I alt")] + BR)], v,
                       extra={"enheter": {t: u for t, _, u in TJ}}))

# tidsserier
AVL = [4310, 4120, 4480, 3960, 4400, 4520, 4250, 4380, 3550, 4190, 4460, 4300, 4080, 3920, 4200]
TOM = [10200, 10650, 11000, 11400, 11050, 10900, 11300, 10500, 10600, 10800]
save("14994", jsonstat("Forsyning av avlinger (1000 tonn) 2010–2024 (DUMMY)",
                       [("Okosystem", "økosystemtype", [("02", "Jordbruksmark")]), ("Tid", "år", [(str(y), str(y)) for y in range(2010, 2025)])],
                       {("02", str(2010 + i)): x for i, x in enumerate(AVL)}, unit="1000 tonn"))
save("14996", jsonstat("Forsyning av tømmer (1000 m³) 2015–2024 (DUMMY)",
                       [("Okosystem", "økosystemtype", [("04", "Skog")]), ("Tid", "år", [(str(y), str(y)) for y in range(2015, 2025)])],
                       {("04", str(2015 + i)): x for i, x in enumerate(TOM)}, unit="1000 m³"))

json.dump({"hentet": "2026-11-05", "metode": "DUMMY, laget av scripts/lag_dummy.py", "note": NOTE,
           "filer": sorted(f for f in os.listdir(RAW) if f.endswith(".json") and not f.startswith("_"))},
          open(os.path.join(RAW, "_hentet.json"), "w"), ensure_ascii=False, indent=1)
print("dummy:", len(os.listdir(RAW)) - 1, "filer")

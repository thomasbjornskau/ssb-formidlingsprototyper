"""Lager DUMMYDATA i json-stat2 for naturregnskap med EKTE kodelister fra KLASS, men OPPDIKTEDE tall.

Kodelister (hentet 10.11.2026 fra data.ssb.no/api/klass):
  988 / variant 3622  Nasjonal variant for hovedøkosystemer (11 koder) og EU-typologi (12 typer på nivå 1)
  939 / 3447          Økosystemtjenester
  992 / 3608          Anvendelse av økosystemtjenester
  959 / 3492          Indikatorer og variabler i tilstandsregnskapet
  966 / 3519          Tilstandsegenskaper
  967 / 3531          Landsdelsinndeling for naturregnskap
Hvilke indikatorer som hører til hvilket økosystem og hvilken egenskap, er GJETTET. Tabellstrukturen er utledet
fra tabelltitler og svar fra fagseksjonen 10.11.2026. Alle tall erstattes av ekte data etter publisering 25.11.2026.
Bare standardbiblioteket."""
import json, os, itertools

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
KL = os.path.join(ROOT, "data", "klass")
NOTE = "DUMMYDATA: ekte kodelister fra KLASS, men oppdiktede tall og koblinger. Erstattes av ekte data etter 25.11.2026."
UPDATED = "2026-11-10T12:00:00Z"


def klass(fil):
    d = json.load(open(os.path.join(KL, fil)))
    return {i["code"]: i["name"].strip() for i in d["classificationItems"]}


HOVED = klass("var_3622.json")               # 11 hovedøkosystemer
EU = {c: n for c, n in klass("ver_3621.json").items() if "." not in c}   # 12 EU-typer, nivå 1
TJN = klass("ver_939.json")
ANV = klass("ver_3608.json")
IND = klass("ver_3492.json")
EGS = klass("ver_3519.json")
LDS = klass("ver_3531.json")
HOVED_L = [(c, HOVED[c]) for c in HOVED]
LAND = "0"
REG = [(LAND, "Hele landet")] + [(c, n) for c, n in LDS.items()]  # koden for hele landet er antatt


def jsonstat(label, dims, values, unit="", extra=None, tabell=""):
    ids = [d[0] for d in dims]
    vals, stat = [], {}
    for i, combo in enumerate(itertools.product(*[[c for c, _ in d[2]] for d in dims])):
        v = values.get(combo, ".")
        if isinstance(v, str):
            vals.append(None); stat[str(i)] = v
        else:
            vals.append(v)
    out = {"version": "2.0", "class": "dataset", "label": label, "source": "Statistisk sentralbyrå", "updated": UPDATED,
           "note": [NOTE], "id": ids, "size": [len(d[2]) for d in dims],
           "dimension": {d[0]: {"label": d[1], "category": {"index": {c: k for k, (c, _) in enumerate(d[2])},
                                                             "label": {c: l for c, l in d[2]}}} for d in dims},
           "value": vals, "extension": {"tabell": tabell}}
    if stat:
        out["status"] = stat
    if unit:
        out["extension"]["enhet"] = unit
    if extra:
        out["extension"].update(extra)
    return out


def save(name, obj):
    os.makedirs(RAW, exist_ok=True)
    json.dump(obj, open(os.path.join(RAW, name + ".json"), "w"), ensure_ascii=False, indent=1)


for f in os.listdir(RAW) if os.path.isdir(RAW) else []:
    os.remove(os.path.join(RAW, f))

# ---------------------------------------------------------------- 15036 utbredelse, hovedøkosystemer (status)
AREAL = {"01": 650, "02-03": 1100, "04": 12100, "05.1+06.1": 10300, "05.2+06.2": 2600, "07": 2300, "08": 150,
         "09": 1900, "10+12.1": 9000, "11": 80, "12.2": 200000}  # 1000 hektar
v = {(c, "Areal"): AREAL[c] for c in HOVED}
v[("00", "Areal")] = sum(AREAL.values())
save("15036", jsonstat("Utbredelse, etter hovedøkosystem 2024 (DUMMY)",
                       [("Okosystem", "hovedøkosystem", [("00", "I alt")] + HOVED_L), ("ContentsCode", "statistikkvariabel", [("Areal", "Areal (1000 hektar)")])],
                       v, unit="1000 hektar", tabell="15036"))

# ---------------------------------------------------------------- utbygging (tabell ikke avklart, foreløpige tall)
UTB = {"01": ".", "02-03": 6500, "04": 18000, "05.1+06.1": 3500, "05.2+06.2": 4000, "07": 2000, "08": 0, "09": 0,
       "10+12.1": ".", "11": 0, "12.2": "."}
v = {(c, "Utbygd"): UTB[c] for c in HOVED}
v[("00", "Utbygd")] = sum(x for x in UTB.values() if not isinstance(x, str))
save("utbygging", jsonstat("Utbygd areal 2018–2024, etter hovedøkosystem. Foreløpige tall (DUMMY)",
                           [("Okosystem", "hovedøkosystem", [("00", "I alt")] + HOVED_L), ("ContentsCode", "statistikkvariabel", [("Utbygd", "Utbygd areal (hektar)")])],
                           v, unit="hektar", tabell="ikke avklart", extra={"forelopig": True, "periode": "2018–2024"}))

# ---------------------------------------------------------------- tilstand
# indikatorer per økosystem og egenskap: GJETTET. Verdier oppdiktet.
SETT = {
 "04": {"A1": {"NO_FUHR_002": .78}, "A2": {"NO_FUNI_XXX": .74, "NO_FUPH_001": .86},
        "B1": {"NO_BUMB_XXX": .58, "NO_BFLY_XXX": .52, "NO_LYNX_001": .41, "NO_WOLF_001": .12, "NO_BEAR_001": .18, "NO_JERV_001": .44, "NO_AATS_001": .83},
        "B2": {"NO_DWTO_001": .24, "NO_DTVS_001": .31, "NO_BGSK_001": .22, "NO_DLTA_001": .35, "NO_MLFA_001": .43},
        "B3": {"NO_BLAA_001": .62, "NO_ROSE_001": .38, "NO_MOOS_001": .55, "NO_DEER_001": .60, "NO_ROED_001": .45},
        "C1": {"NO_CONN_002": .33}},
 "05.1+06.1": {"A1": {"NO_SNOW_001": .81, "NO_GLAC_001": .64, "NO_FUHR_002": .70},
               "B1": {"NO_PTAR_001": .48, "NO_AFOX_001": .30, "NO_GOLD_001": .79, "NO_ALIE_XXX": .95},
               "B3": {"NO_LAVH_001": .58, "NO_RODE_001": .66}, "C1": {"NO_CONN_002": .80, "NO_SLIT_001": .72}},
 "08": {"A2": {"NO_WPHX_XXX": .82, "NO_WTPX_XXX": .74, "NO_WANC_001": .80, "NO_WLAL_001": .77},
        "B1": {"NO_SALM_001": .48, "NO_WAMI_001": .70, "NO_WSPT_001": .66, "NO_WAIP_001": .73, "NO_WPIT_001": .69, "NO_NIPR_002": .55},
        "B3": {"NIVA_Flom": .61, "Pilot_Elvemusling": .40, "Pilot_Oerret": .64}},
 "09": {"A1": {"NO_WLEV_001": .70}, "A2": {"NO_WTPX_XXX": .79, "NO_WPHX_XXX": .85, "NO_WANC_001": .81},
        "B1": {"NO_WPTI_001": .72, "NO_NIPR_001": .60, "Pilot_Dyreplankton": .66}, "B3": {"NO_WPPB_001": .77, "Pilot_Tic": .70, "KlorofyllA_XXX": .74}},
 "10+12.1": {"A1": {"NIVA_Fjord": .74, "NIVA_Secchi": .68}, "A2": {"NIVA_FosforSommer": .76, "NIVA_FosforVinter": .72, "NIVA_NitroSommer": .70, "NIVA_NitroVinter": .66, "NIVA_Oksygen": .62, "NIVA_PH": .88},
             "B1": {"NIVA_Hardbunn": .58, "NIVA_Aalegress": .54, "Naturindeks_KY": .62}, "B3": {"KlorofyllA_XXX": .64}},
 "05.2+06.2": {"B1": {"Naturindeks_AAL": .55, "NO_ALIE_XXX": .82, "NO_BUMB_XXX": .50, "NO_BFLY_XXX": .44},
               "B2": {"NO_FUBS_001": .38, "NO_FUJS_001": .52, "NO_FUJN_001": .60, "NO_SLIT_001": .74},
               "B3": {"NO_FULI_001": .57, "NO_FUMO_XXX": .63, "NO_POPO_001": .48, "NO_FUHR_002": .69}},
 "02-03": {"B1": {"NO_BUMB_XXX": .46, "NO_BFLY_XXX": .39}, "B3": {"NO_POPO_001": .51, "Pilot_JordOeko": .12}, "C1": {"Pilot_JordDiv": .47}},
}
INDEKS = {"04": "Indeks_skog", "05.1+06.1": "Indeks_fjell", "08": "Indeks_elv_bekk", "09": "Indeks_innsjo_vann", "10+12.1": "Indeks_kystvann"}


def totalindeks(sett):
    eg = [sum(g.values()) / len(g) for g in sett.values()]
    return round(sum(eg) / len(eg), 2)


def tilstandstabell(tab, label, ekos, aar, regioner, ld_tot=None, endring=None):
    inds = []
    for e in ekos:
        for g, ii in SETT[e].items():
            inds += [c for c in ii if c not in inds]
        if e in INDEKS:
            inds.append(INDEKS[e])
    dims = [("Okosystem", "hovedøkosystem", [(e, HOVED[e]) for e in ekos]),
            ("Indikator", "tilstandsindikator", [(c, IND[c].strip()) for c in inds]),
            ("Egenskap", "tilstandsegenskap", [("TOT", "Alle egenskaper")] + [(c, n) for c, n in EGS.items()]),
            ("Region", "landsdel", regioner), ("Tid", "år", [(y, y) for y in aar])]
    v = {}
    for e in ekos:
        for y in aar:
            d = endring if (endring and y == "2019") else 0
            sett = {g: {c: round(x - d, 2) for c, x in ii.items()} for g, ii in SETT[e].items()}
            for g, ii in sett.items():
                for c, x in ii.items():
                    v[(e, c, g, LAND, y)] = x
            if e in INDEKS:
                v[(e, INDEKS[e], "TOT", LAND, y)] = totalindeks(sett)
                for r, vals in (ld_tot or {}).get(e, {}).items():
                    v[(e, INDEKS[e], "TOT", r, y)] = vals[0 if y == "2019" else 1]
    save(tab, jsonstat(label, dims, v, unit="skalert 0–1", tabell=tab))


tilstandstabell("15012", "Tilstandsregnskap for skog. Skalert (DUMMY)", ["04"], ["2019", "2024"], REG,
                {"04": {"1": (.49, .51), "2": (.52, .53), "3": (.55, .56), "4": (.51, .53), "5": (.54, .55)}}, endring=0.02)
tilstandstabell("15013", "Tilstandsregnskap for fastmark i fjellet. Skalert (DUMMY)", ["05.1+06.1"], ["2019", "2024"], REG,
                {"05.1+06.1": {"1": (.69, .67), "2": (.70, .68), "3": (.72, .70), "4": (.71, .69), "5": (.73, .71)}}, endring=-0.02)
tilstandstabell("15014", "Tilstandsregnskap for åpent lavland og jordbruksmark. Skalert (DUMMY)", ["02-03", "05.2+06.2"], ["2024"], REG[:1])
tilstandstabell("15016", "Tilstandsregnskap for vassdrag og kystvann. Skalert (DUMMY)", ["08", "09", "10+12.1"], ["2024"], REG[:1])
# 15015 våtmark: bare Naturindeks (biologisk mangfold), per landsdel
v = {}
for r, (a, b) in {"0": (.63, .62), "1": (.58, .57), "2": (.61, .60), "3": (.66, .65), "4": (.64, .62), "5": (.65, .65)}.items():
    v[("07", "Naturindeks_VM", "B1", r, "2019")] = a
    v[("07", "Naturindeks_VM", "B1", r, "2024")] = b
save("15015", jsonstat("Tilstandsregnskap for våtmark, etter landsdel. Skalert (DUMMY)",
                       [("Okosystem", "hovedøkosystem", [("07", HOVED["07"])]), ("Indikator", "tilstandsindikator", [("Naturindeks_VM", IND["Naturindeks_VM"])]),
                        ("Egenskap", "tilstandsegenskap", [("B1", EGS["B1"])]), ("Region", "landsdel", REG), ("Tid", "år", [("2019", "2019"), ("2024", "2024")])],
                       v, unit="skalert 0–1", tabell="15015"))

# ---------------------------------------------------------------- 14967 tilgang (alle tjenester unntatt global klimaregulering)
TJ = ["01", "02", "03", "04", "06", "07", "08", "09"]
ENH = {"01": "1000 tonn", "02": "1000 tonn", "03": "1000 m³", "04": "1000 tonn", "06": "grader celsius",
       "07": "1000 overnattinger", "08": "1000 dagsturer", "09": "hektar"}
TILG = {"01": {"02-03": 4200}, "02": {"02-03": 95}, "03": {"04": 10800},
        "04": {"04": 9.5, "05.2+06.2": 1.2, "01": 0.6, "02-03": 0.4, "05.1+06.1": 0.8},
        "06": {"04": 1.2, "01": 0.8, "09": 0.2},
        "07": {"05.1+06.1": 4200, "04": 2600, "11": 1800, "10+12.1": 1500, "09": 500},
        "08": {"04": 95000, "05.1+06.1": 30000, "11": 18000, "09": 9000, "01": 22000, "10+12.1": 8000, "05.2+06.2": 6000},
        "09": {"04": 600000, "07": 250000, "02-03": 80000, "05.2+06.2": 50000}}
v = {}
for t in TJ:
    for c in HOVED:
        v[(t, c)] = TILG[t].get(c, 0)
    v[(t, "00")] = round(sum(TILG[t].values()), 3)
save("14967", jsonstat("Regnskap for økosystemtjenester, etter tilgang fra økosystemtype 2024 (DUMMY)",
                       [("Tjeneste", "økosystemtjeneste", [(t, TJN[t]) for t in TJ]), ("Okosystem", "hovedøkosystem", [("00", "I alt")] + HOVED_L)],
                       v, tabell="14967", extra={"enheter": ENH}))

# ---------------------------------------------------------------- 14968 anvendelse
ANDEL = {"01": {"01": 1}, "02": {"01": 1}, "03": {"01": 1}, "05": {"02": 1}, "04": {"03": 1}, "06": {"03": 1},
         "07": {"03": .45, "05": .55}, "08": {"03": 1}, "09": {"03": 1}}
KLI_TOT = 6055
v = {}
for t in TJ + ["05"]:
    tot = KLI_TOT if t == "05" else round(sum(TILG[t].values()), 3)
    for b in ANV:
        v[(t, b)] = round(tot * ANDEL[t].get(b, 0), 3)
    v[(t, "00")] = tot
save("14968", jsonstat("Regnskap for økosystemtjenester, etter anvendelse fra økonomisk enhet 2024 (DUMMY)",
                       [("Tjeneste", "økosystemtjeneste", [(t, TJN[t]) for t in sorted(TJ + ["05"])]), ("Bruker", "anvendelse", [("00", "I alt")] + list(ANV.items()))],
                       v, tabell="14968", extra={"enheter": {**ENH, "05": "1000 tonn karbon"}}))

# ---------------------------------------------------------------- 14998 global klimaregulering, EU-typer
ENDR = {"01": -150, "02": -80, "03": 10, "04": 6300, "05": 40, "06": 5, "07": -70, "08": 0, "09": 0, "10": ".", "11": 0, "12": "."}
LAGER = {"01": 30, "02": 160, "03": 120, "04": 1250, "05": 160, "06": 40, "07": 900, "08": ".", "09": ".", "10": ".", "11": 2, "12": "."}  # mill. tonn karbon
v = {}
for c in EU:
    v[(c, "05.01")] = ENDR[c]
    v[(c, "05.02")] = LAGER[c]
v[("00", "05.01")] = sum(x for x in ENDR.values() if not isinstance(x, str))
v[("00", "05.02")] = sum(x for x in LAGER.values() if not isinstance(x, str))
assert v[("00", "05.01")] == KLI_TOT
save("14998", jsonstat("Global klimaregulering, etter EU-økosystemtype 2024 (DUMMY)",
                       [("Okosystem", "økosystemtype (EU)", [("00", "I alt")] + list(EU.items())),
                        ("Tjeneste", "økosystemtjeneste", [("05.01", TJN["05.01"]), ("05.02", TJN["05.02"])])],
                       v, tabell="14998", extra={"enheter": {"05.01": "1000 tonn karbon", "05.02": "mill. tonn karbon"}}))

# ---------------------------------------------------------------- tidsserier
AVL = [4310, 4120, 4480, 3960, 4400, 4520, 4250, 4380, 3550, 4190, 4460, 4300, 4080, 3920, 4200]
TOM = [10200, 10650, 11000, 11400, 11050, 10900, 11300, 10500, 10600, 10800]
save("14994", jsonstat("Forsyning av avlinger (1000 tonn) 2010–2024 (DUMMY)",
                       [("Okosystem", "hovedøkosystem", [("02-03", HOVED["02-03"])]), ("Tid", "år", [(str(y), str(y)) for y in range(2010, 2025)])],
                       {("02-03", str(2010 + i)): x for i, x in enumerate(AVL)}, unit="1000 tonn", tabell="14994"))
save("14996", jsonstat("Forsyning av tømmer (1000 m³) 2015–2024 (DUMMY)",
                       [("Okosystem", "hovedøkosystem", [("04", HOVED["04"])]), ("Tid", "år", [(str(y), str(y)) for y in range(2015, 2025)])],
                       {("04", str(2015 + i)): x for i, x in enumerate(TOM)}, unit="1000 m³", tabell="14996"))

json.dump({"hentet": "2026-11-10", "metode": "DUMMY med ekte KLASS-koder, laget av scripts/lag_dummy.py", "note": NOTE,
           "filer": sorted(f for f in os.listdir(RAW) if f.endswith(".json") and not f.startswith("_"))},
          open(os.path.join(RAW, "_hentet.json"), "w"), ensure_ascii=False, indent=1)
print("dummy:", len(os.listdir(RAW)) - 1, "filer")

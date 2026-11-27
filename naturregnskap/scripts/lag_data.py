"""Leser data/raw/*.json (json-stat2 fra PxWebApi v2, publisert 25.11.2026) og skriver build/naturregnskap.json.
Stopper med «Kontroll feilet» hvis summene eller totalindeksene ikke går opp. Bare standardbiblioteket."""
import itertools, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
KL = os.path.join(ROOT, "data", "klass")


def les(tab):
    """Returnerer (rådata, {kodekombinasjon: verdi eller statussymbol})."""
    d = json.load(open(os.path.join(RAW, tab + ".json"), encoding="utf8"))
    cats = [koder(d, i) for i in d["id"]]
    st = d.get("status") or {}
    out = {}
    for k, combo in enumerate(itertools.product(*cats)):
        v = d["value"][k]
        out[combo] = v if v is not None else st.get(str(k), "..")
    return d, out


def koder(d, dim):
    idx = d["dimension"][dim]["category"]["index"]
    return sorted(idx, key=lambda c: idx[c]) if isinstance(idx, dict) else list(idx)


def lab(d, dim, c):
    return d["dimension"][dim]["category"]["label"][c].strip()


def klass(fil):
    return {i["code"]: i["name"].strip() for i in json.load(open(os.path.join(KL, fil), encoding="utf8"))["classificationItems"]}


num = lambda x: x is not None and not isinstance(x, str)
feil, avvik = [], {}


def kontroll(navn, diff, tol, msg):
    """Registrerer største avvik per kontroll og feiler når avviket er over toleransen."""
    avvik[navn] = max(avvik.get(navn, 0), abs(diff))
    if abs(diff) > tol:
        feil.append(msg)


HOVED = klass("var_3622.json")
EGS = klass("ver_3519.json")
KORT = {"01": "Bebygd", "02-03": "Jordbruksmark", "04": "Skog", "05.1+06.1": "Fjell", "05.2+06.2": "Åpent lavland", "07": "Våtmark",
        "08": "Elver og bekker", "09": "Innsjøer", "10+12.1": "Kystvann", "11": "Kyststrender", "12.2": "Åpent hav"}
IKON = {"01": "house", "02-03": "tractor", "04": "trees", "05.1+06.1": "mountain-snow", "05.2+06.2": "sprout", "07": "droplets",
        "08": "waves", "09": "droplet", "10+12.1": "sailboat", "11": "umbrella", "12.2": "fish"}
# Tjenestetabellene (14967, 15000 m.fl.) skriver hovedøkosystemene med andre koder enn KLASS-varianten i 15036.
TJ_TIL_HOVED = {"01": "01", "02+03": "02-03", "04": "04", "05.01+06.01": "05.1+06.1", "05.02+06.02": "05.2+06.2", "07": "07",
                "08": "08", "09": "09", "10+12.01": "10+12.1", "11": "11", "12.02": "12.2"}
EU_KORT = {"01": "Bebygd", "02": "Dyrket mark", "03": "Grasmark", "04": "Skog", "05": "Hei og buskmark", "06": "Lite vegetert mark og isbreer",
           "07": "Våtmark", "08": "Elver og bekker", "09": "Innsjøer", "10": "Kystinnløp og overgangsvann", "11": "Kyststrender", "12": "Hav"}
# Tjenestene i prototypen: egen kode (som i KLASS 939), kortnavn, ikon og variablene i 14967 som summeres.
TJ = [("01", "Avlinger", "wheat", ["ForsyningAvlinger"]), ("02", "Pollinering", "flower", ["PollineringAvlinger"]),
      ("03", "Tømmer", "tree-pine", ["NettoTilvekstSkog", "AvvirkIkkeProdSkog"]), ("04", "Luftrensing (PM2,5)", "wind", ["LuftrensingPM25"]),
      ("05", "Endringer i karbonlager", "leaf", ["NettoKarbonlagring"]), ("06", "Kjøling av byer", "thermometer", ["TempRegByerNasj"]),
      ("07", "Naturbasert turisme", "luggage", ["NaturbasertTurisme"]), ("08", "Naturbasert rekreasjon", "mountain", ["NaturbasertRekreasjo"]),
      ("09", "Flomdemping", "waves", ["Flomdemping"])]
# Turisme og rekreasjon: summen over økosystemer er større enn I alt (92,56 mot 92,39 og 639,25 mot 599,05).
# Én tur kan trolig telle i flere økosystemer (kildekart, hull 4). De to unntas fra summekontrollen.
IKKE_SUM = {"07", "08"}
# Kvalitetsvurdering fra metodenotatet, tabell 3.7.1: data, metodekonsensus, konseptuell dekning, EU-pliktig.
KVAL = {"01": ("H", "H", "L", True), "03": ("M", "H", "M", True), "02": ("M", "M", "L", True), "05": ("H", "H", "M", True),
        "06": ("L", "M", "M", True), "09": ("M", "L", "M", False), "04": ("M", "M", "L", True), "07": ("H", "M", "H", True), "08": ("H", "M", "H", False)}
# Indikator -> tilstandsegenskap. Finnes ikke i statistikkbanken. Hentet fra Miljødirektoratet/NINA, «Økologisk tilstand for skog»
# og «… for fjell», utkast 01.10.2026, tabell 1. Bekreftes av kontrollen av totalindeksen under.
EGENSKAP = {
    "15012": {"A1": ["Grøfting", "Vegetasjonsindikator for fuktighet"], "A2": ["Vegetasjonsindikator for nitrogen"],
              "B1": ["Fremmede bartrær", "Fremmede plantearter", "Humler", "Dagsommerfugler", "Dødvedmengde", "Rogn, osp og selje"],
              "B2": ["Dødvedandel", "Store trær", "Flersjiktet skog"], "B3": ["Blåbærdekning", "Brunbjørn", "Ulv", "Gaupe", "Elg", "Hjort", "Rådyr"],
              "C1": ["Biologisk gammel skog", "Konnektivitet og arealbruksintensitet"]},
    "15013": {"A1": ["Isbreer", "Snødybde", "Vegetasjonsindikator for varmekrav"], "B1": ["Fjellrev", "Fremmede plantearter", "Kongeørn", "Jerv", "Fjellrype"],
              "B2": ["Reinlav i villreinkommuner"], "B3": ["Smågnagere", "Terrengskade"]}}
AAR = "2024"


def eu_av(kode):
    """hovedøkosystem -> EU-typer på nivå 1, og om koblingen er hel eller delvis"""
    ut = []
    for del_ in kode.split("+"):
        if "-" in del_:
            a, b = del_.split("-")
            ut += [f"{i:02d}" for i in range(int(a), int(b) + 1)]
        else:
            ut.append(del_.split(".")[0])
    return sorted(set(ut)), any("." in d for d in kode.split("+"))


def renske(navn):
    """Tar bort enhet i parentes fra navn på skalerte indikatorer, for eksempel «Dødvedmengde (m3/ha)»."""
    return navn.split(" (m3/ha)")[0]


# ---------------- utbredelse 15036 og utbygging 15038 (bare hele landet, se kildekartet)
du, u = les("15036")
oko_k = koder(du, "Oekosystemtype")
if set(oko_k) != set(HOVED):
    feil.append("15036: kodene stemmer ikke med KLASS-varianten for hovedøkosystemer")
areal = {c: u[("0", c, "Areal", AAR)] for c in oko_k}
if not all(num(x) for x in areal.values()):
    feil.append("15036: mangler areal for et hovedøkosystem")
total = sum(areal.values())  # SSB bruker alle 11 hovedøkosystemer som nevner (469 239 km², nøkkeltall på ssb.no)
db, ub = les("15038")
UB = {c: ub[("0", c, "Areal", AAR)] for c in koder(db, "Oekosystemtype1")}
# Utbygging summert med nasjonal typologi skal være lik summen med EU-typologi. Toleranse 0,05 km²: tallene har to desimaler.
nas = sum(UB[c] for c in oko_k if c in UB and num(UB[c]))
eu = sum(UB[c] for c in ["02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] if num(UB.get(c)))
kontroll("Utbygging: nasjonal sum = EU-sum (km²)", nas - eu, 0.05, f"15038: nasjonal sum {nas:.2f} ≠ EU-sum {eu:.2f}")
kontroll("Utbygging: jordbruksmark = dyrket mark + grasmark (km²)", UB["02-03"] - UB["02"] - UB["03"], 0.02, "15038: jordbruksmark ≠ dyrket + grasmark")
oko = []
for c in oko_k:
    x = UB.get(c, ".")  # bebygd areal er ikke med som fra-type: kan ikke forekomme
    e, delvis = eu_av(c)
    oko.append({"kode": c, "navn": HOVED[c], "kort": KORT[c], "ikon": IKON[c], "areal": areal[c], "andel": round(100 * areal[c] / total, 1),
                "utbygd": x if num(x) else None, "utbygd_status": None if num(x) else x, "eu": e, "eu_delvis": delvis})

# ---------------- tilstand
til = {c: {"type": "ingen"} for c in oko_k}
til["01"] = {"type": "uskalert", "kilde": "14852"}
VERDI = "OekologiskTilstand"


def ki(t, key_lo, key_hi):
    lo, hi = t.get(key_lo), t.get(key_hi)
    return [lo, hi] if num(lo) and num(hi) else None


def ny(tab):
    return {"kilde": tab, "grupper": [], "tot": {}, "ci": None, "landsdel": {}, "landsdel_ci": {}, "naturindeks": {}, "gruppert": tab in EGENSKAP}


# skog og fjell: totalindeks, indikatorer per egenskap og landsdeler
landsdeler = {}
for tab, kode in [("15012", "04"), ("15013", "05.1+06.1")]:
    d, t = les(tab)
    cc = koder(d, "ContentsCode")  # verdi, nedre, øvre
    regs = koder(d, "LandsdelNaturregn")
    landsdeler = {r: lab(d, "LandsdelNaturregn", r) for r in regs if r != "0"}
    ind_k = koder(d, "NaturregnTilstInd")
    tot_k = [i for i in ind_k if i.startswith("indeks_")][0]
    navn = {i: renske(lab(d, "NaturregnTilstInd", i)) for i in ind_k}
    rec = ny(tab)
    v = lambda i, r, c=cc[0]: t[(i, r, c, AAR)]
    for eg, liste in EGENSKAP[tab].items():
        inds = []
        for i in ind_k:
            if navn[i] in liste and num(v(i, "0")):
                if not 0 <= v(i, "0") <= 1:
                    feil.append(f"{tab} {navn[i]}: utenfor 0–1")
                inds.append({"kode": i, "navn": navn[i], "v": {AAR: v(i, "0")}})
        rec["grupper"].append({"eg": eg, "navn": EGS[eg], "ind": inds})
    plassert = {i["kode"] for g in rec["grupper"] for i in g["ind"]}
    rest = [navn[i] for i in ind_k if i != tot_k and i not in plassert and num(v(i, "0"))]
    if rest:
        feil.append(f"{tab}: indikatorer uten egenskap: {rest}")
    rec["tot"] = {AAR: v(tot_k, "0")}
    rec["ci"] = ki({"lo": v(tot_k, "0", cc[1]), "hi": v(tot_k, "0", cc[2])}, "lo", "hi")
    for r in regs:
        # Totalindeks = snitt av egenskapene, der hver egenskap er snittet av sine indikatorer (metodenotatet 3.7).
        # Toleranse 0,01: indikatorene er publisert med to desimaler. Største avvik 27.11.2026 var 0,0095 (fjell, Sør).
        eg = []
        for g, liste in EGENSKAP[tab].items():
            xs = [v(i, r) for i in ind_k if navn[i] in liste and num(v(i, r))]
            if xs:
                eg.append(sum(xs) / len(xs))
        sn = sum(eg) / len(eg)
        kontroll("Totalindeks = snitt av egenskapene (skog og fjell, alle regioner)", sn - v(tot_k, r), 0.01,
                 f"{tab} region {r}: totalindeks {v(tot_k, r)} ≠ beregnet {sn:.3f}")
        if r != "0":
            rec["landsdel"][r] = {AAR: v(tot_k, r)}
            rec["landsdel_ci"][r] = ki({"lo": v(tot_k, r, cc[1]), "hi": v(tot_k, r, cc[2])}, "lo", "hi")
    rec["type"] = "indeks"
    til[kode] = rec

# våtmark: én verdi per landsdel, Naturindeks for våtmark (bare biologisk mangfold)
d, t = les("15015")
cc = koder(d, "ContentsCode")
rec = ny("15015")
rec["type"] = "naturindeks"
rec["naturindeks"] = {AAR: t[("0", cc[0], AAR)]}
rec["ci"] = [t[("0", cc[1], AAR)], t[("0", cc[2], AAR)]]
for r in koder(d, "LandsdelNaturregn"):
    if r != "0":
        rec["landsdel"][r] = {AAR: t[(r, cc[0], AAR)]}
        rec["landsdel_ci"][r] = [t[(r, cc[1], AAR)], t[(r, cc[2], AAR)]]
til["07"] = rec

# åpent lavland, jordbruksmark (15014) og vassdrag, kystvann (15016): bare hele landet, ingen kobling til egenskap
for tab in ["15014", "15016"]:
    d, t = les(tab)
    cc = koder(d, "ContentsCode")
    for e in koder(d, "Oekosystemtype"):
        kode = TJ_TIL_HOVED[e] if e in TJ_TIL_HOVED else {v_: k for k, v_ in HOVED.items()}.get(lab(d, "Oekosystemtype", e))
        if kode not in HOVED:
            feil.append(f"{tab}: ukjent økosystem {e}")
            continue
        rec = ny(tab)
        inds = []
        for i in koder(d, "NaturregnTilstInd"):
            x = t[(i, e, cc[0], AAR)]
            if not num(x):
                continue
            if not 0 <= x <= 1:
                feil.append(f"{tab} {i}: utenfor 0–1")
            n = lab(d, "NaturregnTilstInd", i)
            if n.startswith("Totalindeks"):
                rec["tot"] = {AAR: x}
                rec["ci"] = ki({"lo": t[(i, e, cc[1], AAR)], "hi": t[(i, e, cc[2], AAR)]}, "lo", "hi")
            elif n.startswith("Naturindeks"):
                rec["naturindeks"] = {AAR: x}
            else:
                inds.append({"kode": i, "navn": renske(n), "v": {AAR: x}})
        rec["grupper"] = [{"eg": "", "navn": "Indikatorer", "ind": inds}]
        rec["type"] = "indeks" if rec["tot"] else "profil"
        til[kode] = rec

for rec in til.values():
    if "grupper" in rec:
        rec["n_ind"] = sum(len(g["ind"]) for g in rec["grupper"])
        rec["n_eg"] = len(rec["grupper"]) if rec["gruppert"] else 0
        rec["aar"] = [AAR]

# ---------------- tjenester 14967, anvendelse 14968, karbon 14998
dt, tg = les("14967")
da, an = les("14968")
dk, kl = les("14998")
tj_oko = koder(dt, "Oekosystemtype")
enhet = lambda d, c: lab(d, "ContentsCode", c).rsplit("(", 1)[1].rstrip(")")
BR = koder(da, "OkonomiskEnhet")
tjen = []
for kode, kort, ik, var in TJ:
    tot = sum(tg[("_T", c, AAR)] for c in var)
    tilg = None
    if kode != "05":
        tilg = {}
        for e in tj_oko:
            if e in TJ_TIL_HOVED:
                xs = [tg[(e, c, AAR)] for c in var if num(tg[(e, c, AAR)])]
                if xs and sum(xs):
                    tilg[TJ_TIL_HOVED[e]] = round(sum(xs), 4)
        if kode not in IKKE_SUM:
            # Sum over hovedøkosystemer = I alt. Toleranse 0,1 prosent, for avrunding (SSBs merknad til 14967).
            kontroll("Tjenester: sum av hovedøkosystemer = I alt (14967)", (sum(tilg.values()) - tot) / tot, 0.001,
                     f"14967 {kort}: sum {sum(tilg.values())} ≠ I alt {tot}")
    anv = {b: sum(an[(b, c, AAR)] for c in var if num(an[(b, c, AAR)])) for b in BR}
    anv = {b: x for b, x in anv.items() if x}
    kontroll("Anvendelse i alt (14968) = tilgang i alt (14967)", (sum(anv.values()) - tot) / tot, 0.001,
             f"{kort}: anvendelse {sum(anv.values())} ≠ tilgang {tot}")
    q = KVAL[kode]
    navn = "Forsyning av tømmer (netto tilvekst av produktiv skog og avvirkning fra ikke-produktiv skog)" if kode == "03" else lab(dt, "ContentsCode", var[0]).rsplit(" (", 1)[0]
    tjen.append({"kode": kode, "navn": navn, "kort": kort, "ikon": ik, "enhet": enhet(dt, var[0]),
                 "total": round(tot, 4), "tilgang": tilg, "anvendelse": anv, "kvalitet": {"data": q[0], "metode": q[1], "dekning": q[2]}, "eu": q[3]})

kl_eu = [c for c in koder(dk, "Oekosystemtype") if c != "_T"]
endr = {c: kl[("05.01", c, "GlobalKlimareg", AAR)] for c in kl_eu}
lager = {c: kl[("05.02", c, "GlobalKlimareg", AAR)] for c in kl_eu}
kontroll("Karbon: sum av EU-typer = I alt (14998)", sum(x for x in endr.values() if num(x)) - kl[("05.01", "_T", "GlobalKlimareg", AAR)], 2,
         "14998: sum endring ≠ I alt")  # toleranse 2 (1000 tonn): ti avrundede tall
klima = {"enhet_endring": "1000 tonn", "enhet_lager": "1000 tonn",
         "eu": [{"kode": c, "navn": lab(dk, "Oekosystemtype", c), "kort": EU_KORT[c], "endring": endr[c] if num(endr[c]) else None,
                 "lager": lager[c] if num(lager[c]) else None} for c in kl_eu],
         "endring": kl[("05.01", "_T", "GlobalKlimareg", AAR)], "lager": kl[("05.02", "_T", "GlobalKlimareg", AAR)]}

# ---------------- tidsserier
d, s = les("14994")
avl = [[int(y), s[("01", "02+03", "ForsyningAvlinger", y)]] for y in koder(d, "Tid")]
d, s = les("14996")
tom = [[int(y), s[("03.01", "ForsyningToemmer", y)] + s[("03.02", "ForsyningToemmer", y)]] for y in koder(d, "Tid")]
serier = {"01": {"tabell": "14994", "oko": "02-03", "data": avl}, "03": {"tabell": "14996", "oko": "04", "data": tom}}
for k, sr in serier.items():
    siste = [t_ for t_ in tjen if t_["kode"] == k][0]["tilgang"][sr["oko"]]
    kontroll("Tidsserie 2024 = tilgang i 14967", sr["data"][-1][1] - siste, 1, f"serie {k}: 2024 ≠ 14967")

# ---------------- kjøling i byer: bidragene summerer til I alt (merknad i 14999). Bare nasjonal typologi, ellers telles jordbruksmark to ganger
d, s = les("14999")
bid = sum(s[(e, "_T", "BidragKjoling", AAR)] for e in koder(d, "Oekosystemtype") if e in TJ_TIL_HOVED and num(s.get((e, "_T", "BidragKjoling", AAR))))\
    if ("_T", "_T", "BidragKjoling", AAR) in s else None
if bid is not None:
    kontroll("Kjøling: sum av bidrag = I alt (14999)", bid - s[("_T", "_T", "BidragKjoling", AAR)], 0.02, "14999: bidrag summerer ikke")

# ---------------- flomdemping per landsdel (15000): landsdelene summerer til hele landet.
# Toleranse: 5 ha eller 0,02 prosent, det største. Landsdelene er avrundet hver for seg. Største avvik 27.11.2026:
# 3 ha for enkelttyper og 15 ha for I alt (154 328 ha, 0,01 prosent).
d, s = les("15000")
for e in koder(d, "Oekosystemtype"):
    x0 = s[(e, "0", "Flomdemping", AAR)]
    if num(x0) and x0:
        sm = sum(s[(e, r, "Flomdemping", AAR)] for r in "12345" if num(s[(e, r, "Flomdemping", AAR)]))
        kontroll("Flomdemping: sum av landsdeler = hele landet (15000), ha", sm - x0, max(5, 0.0002 * x0), f"15000 {e}: landsdeler {sm} ≠ hele landet {x0}")

if feil:
    sys.exit("Kontroll feilet: " + "; ".join(feil))

out = {"meta": {"oppdatert": du["updated"][:10], "hentet": json.load(open(os.path.join(RAW, "_hentet.json")))["hentet"],
                "totalareal": round(total, 2), "utbygging_periode": "2018–2024", "utbygging_forelopig": True},
       "oko": oko, "tilstand": til, "landsdel": landsdeler,
       "brukere": {b: lab(da, "OkonomiskEnhet", b) for b in BR}, "tjenester": tjen, "klima": klima, "serier": serier}
os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
json.dump(out, open(os.path.join(ROOT, "build", "naturregnskap.json"), "w", encoding="utf8"), ensure_ascii=False, separators=(",", ":"), sort_keys=True)
print(f"OK: {len(oko)} hovedøkosystemer, {len(tjen)} tjenester, {sum(1 for v in til.values() if v['type'] == 'indeks')} med totalindeks, "
      f"{sum(v.get('n_ind', 0) for v in til.values())} indikatorverdier.")
for k, v in avvik.items():
    print(f"  største avvik: {k}: {v:.4g}")

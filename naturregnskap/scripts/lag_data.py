"""Leser data/raw/*.json (json-stat2) og skriver build/naturregnskap.json. Stopper ved feil i kontrollene.
Bare standardbiblioteket."""
import json, os, sys, itertools

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
KL = os.path.join(ROOT, "data", "klass")


def les(name):
    d = json.load(open(os.path.join(RAW, name + ".json")))
    cats = [sorted(d["dimension"][i]["category"]["index"], key=lambda c: d["dimension"][i]["category"]["index"][c]) for i in d["id"]]
    st = d.get("status", {})
    out = {}
    for k, combo in enumerate(itertools.product(*cats)):
        v = d["value"][k]
        out[combo] = v if v is not None else st.get(str(k), "..")
    return d, out


def koder(d, dim):
    idx = d["dimension"][dim]["category"]["index"]
    return sorted(idx, key=lambda c: idx[c])


def lab(d, dim, c):
    return d["dimension"][dim]["category"]["label"][c].strip()


def klass(fil):
    return {i["code"]: i["name"].strip() for i in json.load(open(os.path.join(KL, fil)))["classificationItems"]}


num = lambda x: not isinstance(x, str) and x is not None
feil = []
def kontroll(ok, msg):
    if not ok:
        feil.append(msg)

HOVED = klass("var_3622.json")
IND = klass("ver_3492.json")
EGS = klass("ver_3519.json")
KORT = {"01": "Bebygd", "02-03": "Jordbruksmark", "04": "Skog", "05.1+06.1": "Fjell", "05.2+06.2": "Åpent lavland", "07": "Våtmark",
        "08": "Elver og bekker", "09": "Innsjøer", "10+12.1": "Kystvann", "11": "Kyststrender", "12.2": "Åpent hav"}
IKON = {"01": "house", "02-03": "tractor", "04": "trees", "05.1+06.1": "mountain-snow", "05.2+06.2": "sprout", "07": "droplets",
        "08": "waves", "09": "droplet", "10+12.1": "sailboat", "11": "umbrella", "12.2": "fish"}
IKKE_LAND = {"10+12.1", "12.2"}   # nevner for andel: alt unntatt kystvann og åpent hav
EU_KORT = {"01": "Bebygd", "02": "Dyrket mark", "03": "Grasmark", "04": "Skog", "05": "Hei og buskmark", "06": "Lite vegetert mark og isbreer",
           "07": "Våtmark", "08": "Elver og bekker", "09": "Innsjøer", "10": "Kystinnløp og overgangsvann", "11": "Kyststrender", "12": "Hav"}
TJ_KORT = {"01": "Avlinger", "02": "Pollinering", "03": "Tømmer", "04": "Luftrensing", "05": "Endringer i karbonlager",
           "06": "Kjøling av byer", "07": "Naturbasert turisme", "08": "Naturbasert rekreasjon", "09": "Flomdemping"}
TJ_IKON = {"01": "wheat", "02": "flower", "03": "tree-pine", "04": "wind", "05": "leaf", "06": "thermometer", "07": "luggage", "08": "mountain", "09": "waves"}
# Kvalitetsvurdering fra metodenotatet, tabell 3.7.1 (ekte, ikke dummy). Data, metodekonsensus, konseptuell dekning, EU-pliktig
KVAL = {"01": ("H", "H", "L", True), "03": ("M", "H", "M", True), "02": ("M", "M", "L", True), "05": ("H", "H", "M", True),
        "06": ("L", "M", "M", True), "09": ("M", "L", "M", False), "04": ("M", "M", "L", True), "07": ("H", "M", "H", True), "08": ("H", "M", "H", False)}


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


# ---------------- utbredelse 15036 og utbygging
du, u = les("15036")
oko_k = [c for c in koder(du, "Okosystem") if c != "00"]
kontroll(set(oko_k) == set(HOVED), "15036: kodene stemmer ikke med KLASS-varianten for hovedøkosystemer")
s = sum(u[(c, "Areal")] for c in oko_k)
kontroll(abs(s - u[("00", "Areal")]) < 1, f"15036: sum {s} ≠ I alt {u[('00', 'Areal')]}")  # heltall i 1000 ha
db, ub = les("utbygging")
land = sum(u[(c, "Areal")] for c in oko_k if c not in IKKE_LAND)
oko = []
for c in oko_k:
    x = ub[(c, "Utbygd")]
    eu, delvis = eu_av(c)
    oko.append({"kode": c, "navn": HOVED[c], "kort": KORT[c], "ikon": IKON[c], "areal": u[(c, "Areal")],
                "andel": None if c in IKKE_LAND else round(100 * u[(c, "Areal")] / land, 1),
                "utbygd": x if num(x) else None, "utbygd_status": None if num(x) else x, "eu": eu, "eu_delvis": delvis})
kontroll(abs(sum(o["utbygd"] or 0 for o in oko) - ub[("00", "Utbygd")]) < 1, "utbygging: summerer ikke til I alt")

# ---------------- tilstand
til = {c: {"type": "ingen"} for c in oko_k}
til["01"] = {"type": "uskalert", "kilde": "14852"}
maks = 0
for tab in ["15012", "15013", "15014", "15015", "15016"]:
    d, t = les(tab)
    yrs, regs = koder(d, "Tid"), koder(d, "Region")
    for e in koder(d, "Okosystem"):
        kontroll(e in HOVED, f"{tab}: ukjent økosystemkode {e}")
        rec = {"kilde": tab, "aar": yrs, "grupper": [], "tot": {}, "landsdel": {}, "naturindeks": {}}
        for g in EGS:
            inds = []
            for i in koder(d, "Indikator"):
                vals = {y: t[(e, i, g, "0", y)] for y in yrs if num(t.get((e, i, g, "0", y)))}
                if vals:
                    kontroll(i in IND, f"{tab}: indikator {i} finnes ikke i KLASS 959")
                    kontroll(all(0 <= x <= 1 for x in vals.values()), f"{tab} {e} {i}: utenfor 0–1")
                    inds.append({"kode": i, "navn": IND[i], "v": vals})
                    if i.startswith("Naturindeks"):
                        rec["naturindeks"] = vals
                        for r in regs:
                            if r != "0":
                                rv = {y: t[(e, i, g, r, y)] for y in yrs if num(t.get((e, i, g, r, y)))}
                                if rv:
                                    rec["landsdel"][r] = rv
            if inds:
                rec["grupper"].append({"eg": g, "navn": EGS[g], "ind": inds})
        tot_k = [i for i in koder(d, "Indikator") if i.startswith("Indeks_")]
        for i in tot_k:
            for y in yrs:
                x = t.get((e, i, "TOT", "0", y))
                if num(x):
                    rec["tot"][y] = x
                    # metodekontroll: totalindeks = snitt av egenskapene, der hver egenskap er snittet av sine indikatorer.
                    # Toleranse 0,006 fordi totalindeksen er publisert med to desimaler.
                    eg = [sum(ii["v"][y] for ii in gr["ind"] if y in ii["v"]) / len([1 for ii in gr["ind"] if y in ii["v"]])
                          for gr in rec["grupper"] if any(y in ii["v"] for ii in gr["ind"]) and not all(ii["kode"].startswith("Naturindeks") for ii in gr["ind"])]
                    sn = sum(eg) / len(eg)
                    maks = max(maks, abs(sn - x))
                    kontroll(abs(sn - x) <= 0.006, f"{tab} {e} {y}: totalindeks {x} ≠ beregnet {sn:.3f}")
                for r in regs:
                    if r != "0" and num(t.get((e, i, "TOT", r, y))):
                        rec["landsdel"].setdefault(r, {})[y] = t[(e, i, "TOT", r, y)]
        rec["n_ind"] = sum(len(g["ind"]) for g in rec["grupper"])
        rec["n_eg"] = len(rec["grupper"])
        rec["type"] = "indeks" if rec["tot"] else ("naturindeks" if tab == "15015" else "profil")
        til[e] = rec

# ---------------- tjenester 14967, 14968, 14998
dt, tg = les("14967")
da, an = les("14968")
dk, kl = les("14998")
enh = da["extension"]["enheter"]
BR = [b for b in koder(da, "Bruker") if b != "00"]
tjen = []
for t in koder(da, "Tjeneste"):
    if t == "05":
        tot = kl[("00", "05.01")]
        s = sum(kl[(c, "05.01")] for c in koder(dk, "Okosystem") if c != "00" and num(kl[(c, "05.01")]))
        kontroll(abs(s - tot) < 1, f"14998: sum endring {s} ≠ I alt {tot}")
        tilg = None
    else:
        tilg = {c: tg[(t, c)] for c in oko_k if tg[(t, c)]}
        tot = tg[(t, "00")]
        kontroll(abs(sum(tilg.values()) - tot) <= 0.001 * max(1, abs(tot)), f"14967 {t}: sum tilgang ≠ I alt")
    kontroll(abs(an[(t, "00")] - tot) <= 0.001 * max(1, abs(tot)), f"{t}: anvendelse i alt ({an[(t, '00')]}) ≠ tilgang i alt ({tot})")
    anv = {b: an[(t, b)] for b in BR if an[(t, b)]}
    kontroll(abs(sum(anv.values()) - an[(t, "00")]) <= 0.001 * max(1, abs(tot)), f"14968 {t}: sum anvendelse ≠ I alt")
    q = KVAL[t]
    tjen.append({"kode": t, "navn": lab(da, "Tjeneste", t), "kort": TJ_KORT[t], "ikon": TJ_IKON[t], "enhet": enh[t], "total": tot,
                 "tilgang": tilg, "anvendelse": anv, "kvalitet": {"data": q[0], "metode": q[1], "dekning": q[2]}, "eu": q[3]})
klima = {"enhet_endring": dk["extension"]["enheter"]["05.01"], "enhet_lager": dk["extension"]["enheter"]["05.02"],
         "eu": [{"kode": c, "navn": lab(dk, "Okosystem", c), "kort": EU_KORT[c], "endring": kl[(c, "05.01")] if num(kl[(c, "05.01")]) else None,
                 "lager": kl[(c, "05.02")] if num(kl[(c, "05.02")]) else None} for c in koder(dk, "Okosystem") if c != "00"],
         "endring": kl[("00", "05.01")], "lager": kl[("00", "05.02")]}

serier = {}
for tab, t in [("14994", "01"), ("14996", "03")]:
    d, s = les(tab)
    e = koder(d, "Okosystem")[0]
    serier[t] = {"tabell": tab, "oko": e, "data": [[int(y), s[(e, y)]] for y in koder(d, "Tid")]}

if feil:
    sys.exit("Kontroll feilet: " + "; ".join(feil))

out = {"meta": {"dummy": "DUMMY" in du["note"][0], "oppdatert": du["updated"][:10], "note": du["note"][0], "landareal": land,
                "utbygging_periode": db["extension"]["periode"], "utbygging_forelopig": db["extension"]["forelopig"]},
       "oko": oko, "tilstand": til, "landsdel": {k: v.strip() for k, v in klass("ver_3531.json").items()},
       "brukere": {b: lab(da, "Bruker", b) for b in BR}, "tjenester": tjen, "klima": klima, "serier": serier}
os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
json.dump(out, open(os.path.join(ROOT, "build", "naturregnskap.json"), "w"), ensure_ascii=False, separators=(",", ":"), sort_keys=True)
print(f"OK: {len(oko)} hovedøkosystemer, {len(tjen)} tjenester, {sum(1 for v in til.values() if v['type'] == 'indeks')} med totalindeks, "
      f"{sum(v.get('n_ind', 0) for v in til.values())} indikatorverdier. Største avvik totalindeks: {maks:.4f}")

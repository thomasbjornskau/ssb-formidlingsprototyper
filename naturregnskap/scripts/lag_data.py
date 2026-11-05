"""Leser data/raw/*.json (json-stat2) og skriver build/naturregnskap.json. Stopper ved feil i kontrollene.
Bare standardbiblioteket."""
import json, os, sys, itertools

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")


def les(name):
    d = json.load(open(os.path.join(RAW, name + ".json")))
    ids, size = d["id"], d["size"]
    cats = [sorted(d["dimension"][i]["category"]["index"], key=lambda c: d["dimension"][i]["category"]["index"][c]) for i in ids]
    st = d.get("status", {})
    out = {}
    for k, combo in enumerate(itertools.product(*cats)):
        v = d["value"][k]
        out[combo] = v if v is not None else st.get(str(k), "..")
    return d, out


def lab(d, dim, code):
    return d["dimension"][dim]["category"]["label"][code]


KORT = {"01": "Bebygd", "02": "Jordbruksmark", "03": "Åpent lavland", "04": "Skog", "05": "Fjell", "06": "Våtmark",
        "07": "Elver", "08": "Innsjøer", "09": "Kyststrender", "10": "Kystvann", "11": "Hav"}
IKON = {"01": "house", "02": "tractor", "03": "sprout", "04": "trees", "05": "mountain-snow", "06": "droplets",
        "07": "waves", "08": "droplet", "09": "umbrella", "10": "sailboat", "11": "fish"}
LAND = ["01", "02", "03", "04", "05", "06", "07", "08", "09"]  # nevner for andel: land og ferskvann
TJ_IKON = {"AVL": "wheat", "TOM": "tree-pine", "POL": "flower", "KLI": "leaf", "TMP": "thermometer", "FLO": "waves",
           "LUF": "wind", "TUR": "luggage", "REK": "mountain"}
TJ_KORT = {"AVL": "Mat fra jordbruket", "TOM": "Tømmer", "POL": "Pollinering", "KLI": "Lagring av karbon",
           "TMP": "Kjøling av byer", "FLO": "Demping av flom", "LUF": "Renere luft", "TUR": "Turisme i naturen", "REK": "Turer i naturen"}
# Kvalitetsvurdering fra metodenotatet, tabell 3.7.1 (ekte, ikke dummy)
KVAL = {"AVL": ("H", "H", "L", True), "TOM": ("M", "H", "M", True), "POL": ("M", "M", "L", True), "KLI": ("H", "H", "M", True),
        "TMP": ("L", "M", "M", True), "FLO": ("M", "L", "M", False), "LUF": ("M", "M", "L", True), "TUR": ("H", "M", "H", True),
        "REK": ("H", "M", "H", False)}

feil = []
def kontroll(ok, msg):
    if not ok:
        feil.append(msg)

# ---------------- utbredelse
du, u = les("utbredelse")
oko_koder = [c for c in sorted(du["dimension"]["Okosystem"]["category"]["index"], key=lambda c: du["dimension"]["Okosystem"]["category"]["index"][c]) if c != "00"]
sum_areal = sum(u[(c, "Areal")] for c in oko_koder)
avvik_areal = abs(sum_areal - u[("00", "Areal")])
kontroll(avvik_areal < 1, f"utbredelse: sum økosystemer {sum_areal} ≠ I alt {u[('00', 'Areal')]}")  # 1000 ha, heltall
land = sum(u[(c, "Areal")] for c in LAND)
oko = []
for c in oko_koder:
    a = u[(c, "Areal")]
    ub = u[(c, "Utbygd")]
    oko.append({"kode": c, "navn": lab(du, "Okosystem", c), "kort": KORT[c], "ikon": IKON[c], "areal": a,
                "andel": round(100 * a / land, 1) if c in LAND else None, "utbygd": ub if not isinstance(ub, str) else None,
                "utbygd_status": ub if isinstance(ub, str) else None})
utb_tot = sum(o["utbygd"] or 0 for o in oko)
kontroll(abs(utb_tot - u[("00", "Utbygd")]) < 1, "utbredelse: utbygd areal summerer ikke")

# ---------------- tilstand
til = {c: {"type": "ingen", "kilde": None} for c in oko_koder}
til["01"] = {"type": "uskalert", "kilde": "14852"}
maks_tot = 0
for tab in ["15012", "15013", "15014", "15015", "15016"]:
    d, t = les(tab)
    ekos = list(d["dimension"]["Okosystem"]["category"]["index"])
    yrs = list(d["dimension"]["Tid"]["category"]["index"])
    regs = list(d["dimension"]["Region"]["category"]["index"])
    egs = [g for g in d["dimension"]["Egenskap"]["category"]["index"] if g != "TOT"]
    for e in ekos:
        rec = {"kilde": tab, "aar": yrs, "eg": {}, "tot": {}, "landsdel": {}}
        for y in yrs:
            prof = {g: t[(e, g, "0", y)] for g in egs if not isinstance(t.get((e, g, "0", y)), str)}
            if prof:
                rec["eg"][y] = prof
            tot = t[(e, "TOT", "0", y)]
            if not isinstance(tot, str):
                rec["tot"][y] = tot
                if prof:
                    snitt = sum(prof.values()) / len(prof)
                    maks_tot = max(maks_tot, abs(snitt - tot))
                    # toleranse 0,006: totalindeksen er publisert med to desimaler
                    kontroll(abs(snitt - tot) <= 0.006, f"{tab} {e} {y}: totalindeks {tot} ≠ snitt av egenskaper {snitt:.3f}")
            for r in regs:
                if r == "0":
                    continue
                x = t.get((e, "TOT", r, y))
                if not isinstance(x, str) and x is not None:
                    kontroll(0 <= x <= 1, f"{tab} {e} {r} {y}: utenfor 0–1")
                    rec["landsdel"].setdefault(r, {})[y] = x
        rec["type"] = "naturindeks" if tab == "15015" else ("indeks" if rec["tot"] else "profil")
        til[e] = rec
LD = {"1": "Øst", "2": "Sør", "3": "Vest", "4": "Midt", "5": "Nord"}
EGN = {"A1": "Fysiske", "A2": "Kjemiske", "B1": "Biologisk mangfold", "B2": "Strukturelle", "B3": "Funksjonelle", "C1": "Landskap"}

# ---------------- tjenester
dt, tg = les("14967")
da, an = les("14968")
enh = dt["extension"]["enheter"]
tjen = []
maks_tj = 0
for t in dt["dimension"]["Tjeneste"]["category"]["index"]:
    tilg = {c: tg[(t, c)] for c in oko_koder if tg[(t, c)]}
    tot = tg[(t, "00")]
    s = sum(tilg.values())
    maks_tj = max(maks_tj, abs(s - tot))
    kontroll(abs(s - tot) <= 0.001 * max(1, abs(tot)), f"14967 {t}: sum tilgang {s} ≠ I alt {tot}")
    anv = {b: an[(t, b)] for b in da["dimension"]["Bruker"]["category"]["index"] if b != "TOT" and an[(t, b)]}
    kontroll(abs(an[(t, "TOT")] - tot) <= 0.001 * max(1, abs(tot)), f"{t}: anvendelse ≠ tilgang")
    kontroll(abs(sum(anv.values()) - an[(t, "TOT")]) <= 0.001 * max(1, abs(tot)), f"14968 {t}: sum anvendelse ≠ I alt")
    q = KVAL[t]
    tjen.append({"kode": t, "navn": lab(dt, "Tjeneste", t), "kort": TJ_KORT[t], "ikon": TJ_IKON[t], "enhet": enh[t], "total": tot,
                 "tilgang": tilg, "anvendelse": anv, "kvalitet": {"data": q[0], "metode": q[1], "dekning": q[2]}, "eu": q[3]})
BRN = {b: lab(da, "Bruker", b) for b in da["dimension"]["Bruker"]["category"]["index"] if b != "TOT"}

# ---------------- tidsserier
serier = {}
for tab, t, e in [("14994", "AVL", "02"), ("14996", "TOM", "04")]:
    d, s = les(tab)
    serier[t] = {"tabell": tab, "oko": e, "data": [[int(y), s[(e, y)]] for y in d["dimension"]["Tid"]["category"]["index"]]}

if feil:
    sys.exit("Kontroll feilet: " + "; ".join(feil))

out = {"meta": {"dummy": "DUMMY" in du["note"][0], "oppdatert": du["updated"][:10], "note": du["note"][0], "landareal": land},
       "oko": oko, "tilstand": til, "landsdel": LD, "egenskaper": EGN, "tjenester": tjen, "brukere": BRN, "serier": serier}
os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
json.dump(out, open(os.path.join(ROOT, "build", "naturregnskap.json"), "w"), ensure_ascii=False, separators=(",", ":"), sort_keys=True)
print(f"OK: {len(oko)} økosystemer, {len(tjen)} tjenester, {sum(1 for v in til.values() if v['type'] == 'indeks')} med totalindeks. "
      f"Største avvik: areal {avvik_areal}, totalindeks {maks_tot:.4f}, tjenester {maks_tj:.4f}")

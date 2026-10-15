"""Lager build/kpi.json fra rådata i data/raw/ og kontrollerer tallene.

Kjøres av felles/bygg.py. Stopper med feil hvis en kontroll ikke går opp:
- hovedgruppenes vekter summerer til 1 000 hvert år
- totalindeksen i 14700 er lik KPI i 14706, og lik den historiske serien i 14710
- totalindeksen kan gjenskapes fra hovedgruppene med vektene for året
- bidragene fra hovedgruppene summerer til publisert tolvmånedersvekst, før normering
- alle koder i synonymlisten finnes i tabell 14700

Bidrag regnes slik SSB gjør det: i to ledd før og etter desember, fordi vektene
skifter i januar. Deretter normeres de, slik fagseksjonen anbefaler: hvert bidrag
ganges med publisert tolvmånedersendring delt på summen av bidragene fra
hovedgruppene, så de summerer til den publiserte raten med én desimal.
Endringsrater tas som publisert, ikke regnet fra indeksene.
"""
import itertools
import json
import pathlib
import re
import sys

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "kpi.json"

# Grupper i figuren over bidrag per måned. Valgt 15.10.2026 etter innspill fra fagseksjonen.
STABEL = [("Strøm", ["04.5.1"]), ("Husleie", ["04.1", "04.2"]),
          ("Mat og alkoholfri drikke", ["01"]), ("Transport", ["07"])]

KORTNAVN = {
    "01": "Mat og alkoholfri drikke", "02": "Alkohol og tobakk", "03": "Klær og sko",
    "04": "Bolig og strøm", "05": "Møbler og husholdning", "06": "Helse", "07": "Transport",
    "08": "Informasjon og kommunikasjon", "09": "Fritid og kultur", "10": "Utdanning",
    "11": "Restaurant og overnatting", "12": "Forsikring og finans", "13": "Andre varer og tjenester",
}
VARIGHET = {"IV": "ikke-varig vare", "HV": "halvvarig vare", "V": "varig vare", "T": "tjeneste"}


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


def serie(t, mnd, **fast):
    """Henter en tidsserie som liste, med None der tall mangler."""
    ut = []
    for m in mnd:
        nokkel = tuple(m if dim == "Tid" else (fast[dim] if dim in fast else t["koder"][i][0])
                       for i, dim in enumerate(t["dims"]))
        ut.append(t["celler"].get(nokkel))
    return ut


def koder(t, dim):
    return t["koder"][t["dims"].index(dim)]


def nivaa(kode):
    """0 = I alt, 1 = hovedgruppe, 2 = gruppe, 3 og 4 = undergrupper, 5 = vare."""
    if kode == "00":
        return 0
    if "_" in kode:
        return 5
    return kode.count(".") + 1


def forelder(kode, finnes):
    """Nærmeste overordnede kode som finnes i tabellen. Leses ut av koden."""
    if kode == "00":
        return None
    k = kode.split("_")[0] if "_" in kode else kode.rsplit(".", 1)[0] if "." in kode else "00"
    while k not in finnes:
        k = k.rsplit(".", 1)[0] if "." in k else "00"
    return k


def main():
    gr, ve, hs, hi = (les(n) for n in ("grupper", "vekter", "hovedserier", "historisk"))
    hentet = json.loads((RAW / "_hentet.json").read_text(encoding="utf8"))["hentet"]
    synonymer = json.loads((MAPPE / "data" / "synonymer.json").read_text(encoding="utf8"))

    mnd = koder(gr, "Tid")
    if mnd[0] != "2015M01" or any(not re.fullmatch(r"\d{4}M\d\d", m) for m in mnd):
        feil("grupper: uventet tidsdimensjon")
    sist = mnd[-1]
    alle = koder(gr, "VareTjenesteGrp")
    finnes = set(alle)
    ind = {k: serie(gr, mnd, VareTjenesteGrp=k, ContentsCode="KpiIndMnd") for k in alle}
    tolv = {k: serie(gr, mnd, VareTjenesteGrp=k, ContentsCode="Tolvmanedersendring") for k in alle}
    vaar = [int(t[:4]) for t in koder(ve, "Tid")]
    vekt = {k: dict(zip(vaar, serie(ve, koder(ve, "Tid"), VareTjenesteGrp=k))) for k in koder(ve, "VareTjenesteGrp")}
    if set(vekt) != finnes:
        feil("vekter og grupper har ulike koder")
    hoved = [k for k in alle if nivaa(k) == 1]
    if len(hoved) != 13:
        feil(f"forventet 13 hovedgrupper, fant {len(hoved)}")

    # 1. Vektene summerer til 1 000
    for a in vaar:
        s = sum(vekt[k][a] for k in hoved)
        if abs(s - 1000) > 0.5:
            feil(f"hovedgruppenes vekter i {a} summerer til {s}")
        if vekt["00"][a] != 1000:
            feil(f"vekten for I alt i {a} er {vekt['00'][a]}")

    # 2. Totalindeksen er lik i de tre tabellene
    smnd = koder(hs, "Tid")
    sind = {s: serie(hs, smnd, KPIavledetSerie=s, ContentsCode="KPIJustIndMnd") for s in koder(hs, "KPIavledetSerie")}
    hmnd = koder(hi, "Tid")
    hind = serie(hi, hmnd)
    kpi = dict(zip(smnd, sind["KPI"]))
    hist = dict(zip(hmnd, hind))
    for i, m in enumerate(mnd):
        if ind["00"][i] != kpi.get(m):
            feil(f"I alt i 14700 ({ind['00'][i]}) er ulik KPI i 14706 ({kpi.get(m)}) i {m}")
        if hist.get(m) is None or abs(hist[m] - ind["00"][i]) > 0.051:
            feil(f"14710 ({hist.get(m)}) er ulik 14700 ({ind['00'][i]}) i {m}")
    if hmnd[-1] != sist or smnd[-1] != sist:
        feil("tabellene har ikke samme siste måned")

    def I(k, m):
        return ind[k][mnd.index(m)] if m in mnd else None

    # 3. Totalindeksen gjenskapt fra hovedgruppene. Indeksene er avrundet til én
    #    desimal, så små avvik er ventet. Toleransen er satt etter faktiske avvik 2016–2026.
    storst = 0
    for m in mnd[12:]:
        a = int(m[:4])
        des = f"{a - 1}M12"
        anslag = I("00", des) * sum(vekt[k][a] / 1000 * I(k, m) / I(k, des) for k in hoved)
        storst = max(storst, abs(anslag - I("00", m)))
        if abs(anslag - I("00", m)) > 0.15:
            feil(f"totalindeksen gjenskapes ikke i {m}: {anslag:.2f} mot {I('00', m)}")

    # 4. Bidrag med SSBs metode. Avvik opp mot 0,16 prosentpoeng skyldes avrundede
    #    indekser og at publisert tolvmånedersvekst er avrundet til én desimal.
    def bidrag(k, m):
        a = int(m[:4])
        fjor = f"{a - 1}{m[4:]}"
        des1, des2 = f"{a - 1}M12", f"{a - 2}M12"
        verdier = [I(k, m), I(k, fjor), I(k, des1), I(k, des2), vekt[k].get(a), vekt[k].get(a - 1)]
        if any(v is None for v in verdier) or des2 not in mnd:
            return None
        im, ifj, id1, id2, w, wf = verdier
        ledd1 = I("00", des2) * wf / 1000 * (id1 - ifj) / id2
        ledd2 = I("00", des1) * w / 1000 * (im - id1) / id1
        return 100 * (ledd1 + ledd2) / I("00", fjor)

    bmnd = [m for m in mnd if m >= "2017M01"]
    bid = {k: [bidrag(k, m) for m in bmnd] for k in hoved}
    avvik = 0
    for j, m in enumerate(bmnd):
        s = sum(bid[k][j] for k in hoved)
        pub = tolv["00"][mnd.index(m)]
        avvik = max(avvik, abs(s - pub))
        if abs(s - pub) > 0.2:
            feil(f"bidragene i {m} summerer til {s:.2f}, publisert {pub}")
    faktor = {m: tolv["00"][mnd.index(m)] / sum(bid[k][j] for k in hoved) for j, m in enumerate(bmnd)}
    bid = {k: [b * faktor[m] for b, m in zip(v, bmnd)] for k, v in bid.items()}
    for j, m in enumerate(bmnd):
        if abs(sum(bid[k][j] for k in hoved) - tolv["00"][mnd.index(m)]) > 1e-9:
            feil(f"normerte bidrag i {m} summerer ikke til publisert rate")

    stabel = []
    for navn_, ks in STABEL:
        v = [sum(bidrag(k, m) * faktor[m] for k in ks) for m in bmnd]
        stabel.append({"navn": navn_, "koder": ks, "v": [round(x, 3) for x in v]})
    andre = [round(tolv["00"][mnd.index(m)] - sum(g["v"][j] for g in stabel), 3) for j, m in enumerate(bmnd)]

    # 5. Synonymene peker på koder som finnes
    for ord_, ks in synonymer["ord"].items():
        for k in ks:
            if k not in finnes:
                feil(f"synonymet «{ord_}» peker på {k}, som ikke finnes")

    navn = gr["etiketter"]["VareTjenesteGrp"]
    grupper = []
    for k in alle:
        tekst = navn[k]
        treff = re.search(r"\s*\((IV|HV|V|T)\)$", tekst)
        grupper.append({
            "k": k, "n": tekst[:treff.start()] if treff else tekst,
            "v": treff.group(1) if treff else None, "f": forelder(k, finnes), "l": nivaa(k),
            "i": ind[k], "t": tolv[k],
            "w": [vekt[k][a] for a in vaar] if any(vekt[k][a] is not None for a in vaar) else None,
            "b": round(bidrag(k, sist) * faktor[sist], 3) if bidrag(k, sist) is not None else None,
        })

    start_s = smnd.index("1995M01") if "1995M01" in smnd else 0
    serier = {s: {mal: serie(hs, smnd[start_s:], KPIavledetSerie=s, ContentsCode=mal)
                  for mal in ("KPIJustIndMnd", "Manedsendring", "Tolvmanedersendring")}
              for s in koder(hs, "KPIavledetSerie")}

    serienavn = hs["etiketter"]["KPIavledetSerie"]
    data = {
        "sist": sist, "oppdatert": gr["oppdatert"], "hentet": hentet,
        "start": mnd[0], "vekt_aar": vaar, "kortnavn": KORTNAVN, "varighet": VARIGHET,
        "grupper": grupper,
        "bidrag": {"start": bmnd[0], "serier": {k: [round(b, 3) for b in v] for k, v in bid.items()},
                   "stabel": stabel, "andre": andre},
        "serier": {"start": smnd[start_s], "data": serier, "navn": serienavn},
        "historisk": {"start": hmnd[0], "i": hind},
        "synonymer": synonymer["ord"], "usikre_synonymer": synonymer["usikker"],
    }
    UT.parent.mkdir(exist_ok=True)
    UT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(f"kpi: {len(grupper)} grupper, {len(mnd)} måneder til {sist}. "
          f"Største avvik: totalindeks {storst:.2f}, bidragssum {avvik:.2f} prosentpoeng. "
          f"{UT.stat().st_size // 1024} kB")


if __name__ == "__main__":
    main()

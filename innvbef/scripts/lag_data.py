"""Lager build/innvbef.json fra rådata i data/raw/ og kontrollerer summene.

Kjøres av felles/bygg.py. Stopper med feil hvis en kontroll ikke går opp:
- de 30 gruppene i 12548 summerer til «Befolkningen i alt», og den er lik 05803, alle år 2004–2026
- 12548 kode 124 og 024 er lik innvandrere og norskfødte med innvandrerforeldre i 05182, alle år
- 05182: de fem kategoriene er mindre enn folkemengden (øvrig befolkning er positiv), alle år
- 10516 fra 2016: utgang − inngang = folketilvekst, inngang = 05182 samme år, utgang = 05182 året etter
- 13880: summen av land = landstallet i 05182, alle år
- 10598: botid summert per land = innvandrere i 13880 for 2026
- 09817: summen av land = «Alle land» per kommune og kategori, kommunene summerer til landet
- 09817: publisert andel = antall / folkemengde fra 07459
- synonymene peker på land som finnes, og alle land har en verdensdel
Toleransene er satt etter faktiske avvik (se kildekartet) og er forklart der de står.
Bare standardbiblioteket.
"""
import itertools
import json
import pathlib
import sys

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "innvbef.json"
AVVIK = {}


def feil(tekst):
    sys.exit(f"Kontroll feilet: {tekst}")


def avvik(navn, v):
    AVVIK[navn] = max(AVVIK.get(navn, 0), abs(v))


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


def hent(t, tom=False, **fast):
    """Slår opp én verdi. Dimensjoner som ikke er oppgitt, må ha én kategori. tom=True tillater None."""
    nokkel = []
    for dim, koder in zip(t["dims"], t["koder"]):
        if dim in fast:
            nokkel.append(str(fast[dim]))
        elif len(koder) == 1:
            nokkel.append(koder[0])
        else:
            feil(f"{t['navn']}: dimensjonen {dim} må velges")
    v = t["celler"].get(tuple(nokkel))
    if v is None and not tom:
        feil(f"{t['navn']}: mangler verdi for {fast}")
    return v


def koder(t, dim):
    return t["koder"][t["dims"].index(dim)]


def main():
    kt, fm, tg, en, el, lt, lb, kl, ktid, kb = (les(n) for n in (
        "kategorier_tid", "folkemengde", "tre_generasjoner", "endringer", "endringer_land",
        "land_tid", "land_botid", "kommune_land", "kommune_tid", "kommune_bef"))
    vd = json.loads((RAW / "verdensdel.json").read_text(encoding="utf8"))
    syn = json.loads((MAPPE / "data" / "synonymer.json").read_text(encoding="utf8"))

    # ---------- Kategorier over tid (05182) og folkemengde (05803) ----------
    aar = koder(kt, "Tid")
    KAT = {"innv": "2", "nmi": "3", "E": "5", "F": "6", "G": "7"}
    kat = {"aar": [int(a) for a in aar]}
    for navn, kode in KAT.items():
        kat[navn] = [hent(kt, InnvandrKat=kode, Tid=a) for a in aar]
    kat["bef"] = [hent(fm, Tid=a) for a in aar]
    for i, a in enumerate(aar):
        if sum(kat[k][i] for k in KAT) >= kat["bef"][i]:
            feil(f"05182 {a}: kategoriene er like store som folkemengden")

    # ---------- Tre generasjoner (12548) ----------
    tg_aar = koder(tg, "Tid")
    tg_koder = [k for k in koder(tg, "InnvandrKat3gen") if k != "TOT"]
    if len(tg_koder) != 30:
        feil(f"12548 har {len(tg_koder)} grupper, ventet 30")
    tre = {"aar": [int(a) for a in tg_aar], "koder": tg_koder,
           "navn": {k: tg["etiketter"]["InnvandrKat3gen"][k] for k in tg_koder},
           "v": {k: [hent(tg, InnvandrKat3gen=k, Tid=a) for a in tg_aar] for k in tg_koder},
           "tot": [hent(tg, InnvandrKat3gen="TOT", Tid=a) for a in tg_aar]}
    for i, a in enumerate(tg_aar):
        s = sum(tre["v"][k][i] for k in tg_koder)
        if s != tre["tot"][i]:
            feil(f"12548 {a}: de 30 gruppene summerer til {s}, ikke {tre['tot'][i]}")
        if tre["tot"][i] != hent(fm, Tid=a):
            feil(f"12548 {a}: befolkningen i alt er ulik 05803")
        j = aar.index(a)
        if tre["v"]["124"][i] != kat["innv"][j] or tre["v"]["024"][i] != kat["nmi"][j]:
            feil(f"12548 {a}: kode 124/024 er ulik 05182")

    # ---------- Befolkningsregnskap (10516), fra 2016 ----------
    # 2011–2015 går ikke opp (utgang − inngang ≠ tilvekst, se kildekartet H7). Regnskapet brukes fra 2016.
    e_aar = [a for a in koder(en, "Tid") if int(a) >= 2016]
    endr = {"aar": [int(a) for a in e_aar]}
    for kat_kode, kat_navn, k05182 in (("B", "innv", "2"), ("C", "nmi", "3")):
        r = {c: [hent(en, InnvandrKat=kat_kode, ContentsCode=c, Tid=a) for a in e_aar]
             for c in ("Folkemengde", "Fodte", "Dode", "Innflyttinger", "Utflyttinger", "Folketilvekst", "Folkemengde2")}
        for i, a in enumerate(e_aar):
            if r["Folkemengde2"][i] - r["Folkemengde"][i] != r["Folketilvekst"][i]:
                feil(f"10516 {kat_kode} {a}: utgang − inngang ≠ tilvekst")
            if r["Folkemengde"][i] != hent(kt, InnvandrKat=k05182, Tid=a) or r["Folkemengde2"][i] != hent(kt, InnvandrKat=k05182, Tid=str(int(a) + 1)):
                feil(f"10516 {kat_kode} {a}: folkemengden er ulik 05182")
            rest = r["Folketilvekst"][i] - (r["Fodte"][i] - r["Dode"][i] + r["Innflyttinger"][i] - r["Utflyttinger"][i])
            # Største faktiske rest er 849 (norskfødte 2017). Over 1 000 tyder på feil i dataene.
            if abs(rest) > 1000:
                feil(f"10516 {kat_kode} {a}: restposten er {rest}")
            avvik("regnskap, rest", rest)
        endr[kat_navn] = {"ib": r["Folkemengde"], "fodte": r["Fodte"], "dode": r["Dode"], "inn": r["Innflyttinger"],
                          "ut": r["Utflyttinger"], "tilv": r["Folketilvekst"]}

    # ---------- Land over tid (13880) ----------
    l_aar = koder(lt, "Tid")
    alle_land = [l for l in koder(lt, "Landbakgrunn") if l != "000"]
    land_tid = {}
    for l in alle_land:
        inn = [hent(lt, Landbakgrunn=l, ContentsCode="Innvandrere", Tid=a) for a in l_aar]
        nmi = [hent(lt, Landbakgrunn=l, ContentsCode="NorskFodtInnvForeld", Tid=a) for a in l_aar]
        if any(inn) or any(nmi):
            land_tid[l] = [inn, nmi]
    for i, a in enumerate(l_aar):
        j = aar.index(a)
        for m, navn in ((0, "innv"), (1, "nmi")):
            d = sum(v[m][i] for v in land_tid.values()) - kat[navn][j]
            # Små celler er avrundet. Største faktiske avvik er 2.
            if abs(d) > 5:
                feil(f"13880 {a}: summen av land avviker {d} fra 05182 ({navn})")
            avvik("land mot landet", d)
    land_2026 = {l: v[0][-1] + v[1][-1] for l, v in land_tid.items()}
    med_folk = [l for l in land_tid if land_2026[l] > 0]

    # Verdensdel fra kodelisten
    vd_av = {}
    for g in vd["values"]:
        for k in g.get("valueMap", []):
            vd_av[k] = g["code"]
    mangler_vd = [l for l in land_tid if l not in vd_av]
    if mangler_vd:
        feil(f"land uten verdensdel: {mangler_vd}")
    navn_l = lt["etiketter"]["Landbakgrunn"]
    land = [[l, navn_l[l], vd_av[l]] for l in sorted(land_tid, key=lambda x: -land_2026[x])]

    # ---------- Botid (10598), 2026 ----------
    b_koder = koder(lb, "Botid")
    botid = {}
    for l in koder(lb, "Lanbakgrunn"):
        v = [hent(lb, Lanbakgrunn=l, Botid=b) for b in b_koder]
        if l in land_tid and sum(v):
            # 41 avrundede småceller per land. Største faktiske avvik er 11 (land 296).
            d = sum(v) - land_tid[l][0][-1]
            if abs(d) > 15:
                feil(f"10598 {l}: botid summerer til {sum(v)}, 13880 har {land_tid[l][0][-1]}")
            avvik("botid mot land", d)
            botid[l] = v

    # ---------- Befolkningsregnskap per land (10518), fra 2016 ----------
    el_aar = [a for a in koder(el, "Tid") if int(a) >= 2016]
    endr_land = {}
    for l in koder(el, "LandBakgr"):
        if l not in land_tid:
            continue   # verdensdeler og «Alle land» brukes ikke
        r = {c: [hent(el, tom=True, LandBakgr=l, ContentsCode=c, Tid=a) for a in el_aar]
             for c in ("Folkemengde", "Fodte", "Dode", "Innflyttinger", "Utflyttinger", "Folketilvekst")}
        endr_land[l] = {"ib": r["Folkemengde"], "fodte": r["Fodte"], "dode": r["Dode"], "inn": r["Innflyttinger"],
                        "ut": r["Utflyttinger"], "tilv": r["Folketilvekst"]}

    # ---------- Kommuner (09817 og 07459), 2026 ----------
    kom_koder = [r for r in koder(kl, "Region") if r != "9999"]
    kb_v = {r[-4:]: hent(kb, Region=r) for r in koder(kb, "Region")}
    komm = []
    for r in kom_koder:
        if r not in kb_v:
            feil(f"07459 mangler kommune {r}")
        komm.append([r, kl["etiketter"]["Region"][r], kb_v[r]])
    landkoder_k = [l for l in koder(kl, "Landbakgrunn") if l not in ("999", "VES", "IVE")]
    komm_land = {}
    for kat_kode, m in (("B", 0), ("C", 1)):
        for i, r in enumerate(koder(kl, "Region")):
            tot = hent(kl, Region=r, InnvandrKat=kat_kode, Landbakgrunn="999")
            s = 0
            for l in landkoder_k:
                v = hent(kl, Region=r, InnvandrKat=kat_kode, Landbakgrunn=l)
                s += v
                if v and r != "9999":
                    komm_land.setdefault(l, {}).setdefault(kom_koder.index(r), [0, 0])[m] = v
            # Små celler er avrundet. Største faktiske avvik er 3.
            if abs(s - tot) > 5:
                feil(f"09817 {r} {kat_kode}: summen av land er {s}, «Alle land» er {tot}")
            avvik("kommune, land mot alle", s - tot)
            if r != "9999":
                komm_land.setdefault("999", {}).setdefault(kom_koder.index(r), [0, 0])[m] = tot
        landet = sum(hent(kl, Region=r, InnvandrKat=kat_kode, Landbakgrunn="999") for r in koder(kl, "Region"))
        d = landet - kat["innv" if kat_kode == "B" else "nmi"][-1]
        # Norskfødte 2026: 238 508 mot 238 507 (avrunding).
        if abs(d) > 2:
            feil(f"09817 {kat_kode}: kommunene summerer til {landet}, ikke landstallet")
        avvik("kommuner mot landet", d)
    for r in kom_koder:
        a = hent(ktid, Region=r, InnvandrKat="B", ContentsCode="AndelBefolkning", Tid="2026")
        b = hent(ktid, Region=r, InnvandrKat="B", ContentsCode="Personer1", Tid="2026")
        d = round(100 * b / kb_v[r], 2) - a
        if abs(d) > 0.011:
            feil(f"09817 {r}: publisert andel {a} er ulik egen beregning")
        avvik("andel kommune (prosentpoeng)", round(d, 3))
    # Kompakt: land -> [[kommuneindeks, innvandrere, norskfødte], ...]
    komm_land = {l: [[k, v[0], v[1]] for k, v in sorted(d.items())] for l, d in komm_land.items()}

    # ---------- Synonymer ----------
    for ord_, ks, _ in syn:
        for k in ks:
            if k not in land_tid:
                feil(f"synonymet «{ord_}» peker på {k}, som ikke finnes")

    ut = {
        "kilde": {"oppdatert": {t["navn"]: t["oppdatert"] for t in (kt, fm, tg, en, el, lt, lb, kl, ktid, kb)},
                  "hentet": json.loads((RAW / "_hentet.json").read_text(encoding="utf8"))["hentet"]},
        "kat": kat, "tre": tre, "endr": endr, "endrLand": endr_land,
        "land": land, "landTid": {"aar": [int(a) for a in l_aar], "v": land_tid}, "botid": botid,
        "verdensdel": [[g["code"], g["label"]] for g in vd["values"]],
        "komm": komm, "kommLand": komm_land, "synonymer": syn,
    }
    UT.parent.mkdir(exist_ok=True)
    UT.write_text(json.dumps(ut, ensure_ascii=False, separators=(",", ":"), sort_keys=True), encoding="utf8")
    print(f"build/innvbef.json: {round(UT.stat().st_size / 1024)} kB · {len(land)} land ({len(med_folk)} med personer 2026) · "
          f"{len(komm)} kommuner · {sum(len(v) for v in komm_land.values())} kommune×land-celler · største avvik: "
          + ", ".join(f"{k} {v}" for k, v in AVVIK.items()))


if __name__ == "__main__":
    main()

"""Lager build/muh.json fra rådata i data/raw/ og kontrollerer tallene.

Kjøres av felles/bygg.py. Stopper med feil hvis en kontroll ikke går opp:
- K1  summen av enkeltland er lik «Alle land» (08804)
- K2  eksport = fastland + olje og gass + skip og plattformer, per land og år
- K3  handelsbalansen og fastlandsbalansen kan gjenskapes fra komponentene (08800)
- K4  «Alle land» i 08804 er lik 08800
- K5  fastlandseksporten kan gjenskapes fra tresifret SITC (08819)
- K6  eksporten som mangler på tresifret nivå, ligger på ensifret nivå (08819 mot 08809)
- K7  ensifret SITC summerer per land, og totalen per land er lik 08804
- K8  månedene i 2025 (08792) summerer til årstallet (08800)
- K9  endelige månedstall (12308) summerer til årstallene (08800)
- K10 publiserte pris- og volumendringer stemmer med indeksene (06322)
- K11 månedstabellene har samme siste måned, og alle synonymer peker på land som finnes

Toleransene er satt etter de faktiske avvikene 14.10.2026, med litt margin.
De skyldes avrunding: 08804 er i mill. kr, 08809, 08819 og 12308 i 1 000 kr.
Endringsrater tas som publisert, ikke regnet fra indeksene.
"""
import itertools
import json
import pathlib
import sys

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "muh.json"

# Aggregater i landdimensjonen. 90 «Uspesifisert» er en gruppe med samme verdier som 97.
AGGREGATER = {"00", "01", "02", "03", "04", "05", "06", "10", "16", "17", "20", "40", "60", "70", "80", "90"}
# Eksportgrupper med pris- og volumindeks i prototypen (06322)
INDEKSGRUPPER = ["-", "T02", "333", "34", "03"]
# Korte navn til figurene. SSBs navn står i tabellen og i verktøytipset.
KORT_SITC1 = {"0": "Mat og levende dyr", "1": "Drikke og tobakk", "2": "Råvarer", "3": "Olje, gass, strøm og annen energi",
              "4": "Oljer og fett", "5": "Kjemiske produkter", "6": "Bearbeidde varer", "7": "Maskiner og transportmidler",
              "8": "Ferdigvarer", "9": "Andre varer"}
KORT_SITC3 = {"034": "Fersk og fryst fisk", "035": "Tørket, saltet og røkt fisk", "684": "Aluminium",
              "334": "Raffinerte oljeprodukter", "771": "Elektriske kraftmaskiner", "351": "Strøm",
              "874": "Måleinstrumenter", "342": "Propan og butan", "683": "Nikkel", "764": "Telekomutstyr",
              "671": "Råjern og jernpulver", "742": "Pumper", "772": "Elektrisk koblingsutstyr", "793": "Skip og båter",
              "036": "Krepsdyr og bløtdyr", "037": "Fiskevarer, bearbeidd", "081": "Dyrefor", "562": "Gjødsel",
              "251": "Papirmasse", "641": "Papir og papp", "282": "Jern- og stålskrap", "699": "Metallvarer",
              "728": "Maskiner til særlige næringer", "723": "Anleggsmaskiner", "541": "Medisinske produkter",
              "542": "Legemidler", "511": "Hydrokarboner", "522": "Uorganiske grunnstoffer", "516": "Andre organiske kjemikalier"}
PUBREKKE = ["02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "01", "13", "14"]
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
    verdier = d["value"]
    status = d.get("status") or {}
    celler, symbol = {}, {}
    for n, kombinasjon in enumerate(itertools.product(*koder)):
        celler[kombinasjon] = verdier.get(str(n)) if isinstance(verdier, dict) else verdier[n]
        s = status.get(str(n)) if isinstance(status, dict) else (status[n] if n < len(status) else None)
        if s:
            symbol[kombinasjon] = s
    etiketter = {dim: d["dimension"][dim]["category"].get("label", {}) for dim in d["id"]}
    return {"navn": navn, "celler": celler, "symbol": symbol, "dims": d["id"], "koder": koder,
            "etiketter": etiketter, "oppdatert": d.get("updated", "")[:10]}


def hent(t, **fast):
    """Én verdi. Dimensjoner som ikke er oppgitt, tar første kode (statistikkvariabelen)."""
    nokkel = tuple(fast[dim] if dim in fast else t["koder"][i][0] for i, dim in enumerate(t["dims"]))
    if nokkel not in t["celler"]:
        feil(f"{t['navn']}: finner ikke {fast}")
    return t["celler"][nokkel]


def serie(t, tid, **fast):
    return [hent(t, Tid=x, **fast) for x in tid]


def koder(t, dim):
    return t["koder"][t["dims"].index(dim)]


def null(v):
    return 0 if v is None else v


def kontroll(navn, avvik, grense):
    AVVIK[navn] = avvik
    if avvik > grense:
        feil(f"{navn}: avvik {avvik} er over grensen {grense}")


def main():
    H, M, L, W, V, I, R = (les(n) for n in ("hovedtall_aar", "hovedtall_mnd", "land_aar", "land_varer",
                                             "varer_aar", "indekser", "revisjoner"))
    hentet = json.loads((RAW / "_hentet.json").read_text(encoding="utf8"))["hentet"]
    synonymer = json.loads((MAPPE / "data" / "synonymer.json").read_text(encoding="utf8"))

    haar = koder(H, "Tid")
    laar = koder(L, "Tid")
    land = koder(L, "Land")
    stromer = koder(L, "HovedVareStrommer")
    historiske = [k for k in land if k not in AGGREGATER
                  and all(L["symbol"].get((s, k, "Verdi", t)) == "." for s in ("Etot", "Itot") for t in laar)]
    enkelt = [k for k in land if k not in AGGREGATER and k not in historiske]

    def lv(s, k, t):
        return hent(L, HovedVareStrommer=s, Land=k, Tid=t)

    def hv(s, t):
        return hent(H, HovedVareStrommer=s, Tid=t)

    # K1 Summen av enkeltland er lik «Alle land». 249 tall avrundet til hele mill. kr; faktisk største avvik 9.
    kontroll("K1 sum av land", max(abs(sum(null(lv(s, k, t)) for k in enkelt) - lv(s, "00", t))
                                   for s in stromer for t in laar), 20)

    # K2 Eksport = fastland + olje og gass + skip og plattformer. Faktisk største avvik 1 mill. kr.
    kontroll("K2 eksport = fastland + olje og gass + skip og plattformer",
             max(abs(lv("Etot", k, t) - sum(null(lv(s, k, t)) for s in ("Etotusorn", "Eoljegass", "Eskipplat")))
                 for k in enkelt + ["00"] for t in laar if lv("Etot", k, t) is not None), 2)

    # K3 Balansene, 1960–2025. Faktisk største avvik 1 mill. kr.
    kontroll("K3 handelsbalansen", max(abs(null(hv("Etot", t)) - null(hv("Itot", t)) - null(hv("Hbtot", t))) for t in haar), 2)
    kontroll("K3 fastlandsbalansen", max(abs(null(hv("Etotusorn", t)) - null(hv("Itotuso", t)) - null(hv("Hbtusorn", t)))
                                         for t in haar), 2)

    # K4 «Alle land» i 08804 er lik 08800. Skal være eksakt.
    kontroll("K4 08804 = 08800", max(abs(lv(s, "00", t) - hv(s, t)) for s in stromer for t in laar), 0)

    # K5 Fastlandseksport = total − 333 (råolje og kondensater) − 343 (naturgass) − skip og plattformer.
    #    08819 er i 1 000 kr. Faktisk største avvik 0,8 mill. kr.
    vaar = koder(V, "Tid")
    vk = [k for k in koder(V, "SITC") if k != "-"]

    def vv(ie, k, t):
        return null(hent(V, ImpEks=ie, SITC=k, Tid=t)) / 1000

    kontroll("K5 fastlandseksport fra varegrupper",
             round(max(abs(vv("2", "-", t) - vv("2", "333", t) - vv("2", "343", t) - hv("Eskipplat", t) - hv("Etotusorn", t))
                       for t in vaar), 1), 2)

    # K6 Det som mangler på tresifret nivå (mest kjemiske produkter), finnes på ensifret nivå i 08809.
    #    Faktisk avvik 0 mill. kr i 2025.
    sist_aar = vaar[-1]
    if koder(W, "Tid") != [sist_aar]:
        feil("08809 og 08819 har ikke samme siste år")
    uford = {t: round(vv("2", "-", t) - sum(vv("2", k, t) for k in vk)) for t in vaar}
    en = {s: null(hent(W, ImpEks="2", Land="00", SITC=s, Tid=sist_aar)) / 1000 for s in "0123456789"}
    tre = {s: sum(vv("2", k, sist_aar) for k in vk if k[0] == s) for s in "0123456789"}
    kontroll("K6 manglende tresifret ligger på ensifret", abs(round(sum(en[s] - tre[s] for s in en)) - uford[sist_aar]), 2)

    # K7 Ensifret SITC summerer per land (faktisk 2 tusen kr), og totalen per enkeltland er lik 08804
    #    (faktisk 0,499 mill. kr, altså avrunding til hele millioner).
    maks_s = maks_l = 0
    for ie, k in itertools.product(("1", "2"), enkelt + ["00"]):
        tot = hent(W, ImpEks=ie, Land=k, SITC="-", Tid=sist_aar)
        if tot is None:
            continue
        maks_s = max(maks_s, abs(sum(null(hent(W, ImpEks=ie, Land=k, SITC=s, Tid=sist_aar)) for s in "0123456789") - tot))
        h = lv("Itot" if ie == "1" else "Etot", k, sist_aar)
        if h is not None:
            maks_l = max(maks_l, abs(tot / 1000 - h))
    kontroll("K7 ensifret summerer per land (1 000 kr)", maks_s, 20)
    kontroll("K7 total per land 08809 = 08804", round(maks_l, 3), 0.5)

    # K8 Månedene i 2025 summerer til årstallet. Faktisk største avvik 3 mill. kr (fem strømmer).
    mtid = koder(M, "Tid")
    kontroll("K8 måneder 2025 = år 2025", max(abs(sum(hent(M, HovedVareStrommer=s, Tid=f"2025M{m:02d}") for m in range(1, 13))
                                                  - hv(s, "2025")) for s in ("Etot", "Itot", "Etotusorn", "Hbtot", "Hbtusorn")), 12)

    # K9 Endelige månedstall summerer til årstallet, 2016 til siste år med endelige tall. Faktisk 0,5 mill. kr.
    rtid = koder(R, "Tid")

    def rv(ie, sitc, pub, t):
        return hent(R, ImpEks=ie, SITC=sitc, PubliseringMnd=pub, Tid=t)

    endelige_aar = sorted({t[:4] for t in rtid if rv("2", "-", "14", t) is not None})
    endelige_aar = [a for a in endelige_aar if all(rv("2", "-", "14", f"{a}M{m:02d}") is not None for m in range(1, 13))]
    kontroll("K9 endelige måneder = år", round(max(abs(sum(rv(ie, "-", "14", f"{a}M{m:02d}") for m in range(1, 13)) / 1000 - hv(s, a))
                                                   for a in endelige_aar for ie, s in (("2", "Etot"), ("1", "Itot"))), 2), 1)

    # K10 Publiserte endringer mot indeksene. Indeksene har én desimal; faktisk avvik 0,0 prosentpoeng.
    itid = koder(I, "Tid")
    maks = 0
    for ie, g in itertools.product(("1", "2"), koder(I, "ImpEkspGr")):
        for a, b in zip(itid, itid[1:]):
            vals = [hent(I, ImpEks=ie, ImpEkspGr=g, ContentsCode=c, Tid=t) for c, t in
                    (("Prisindeks", a), ("Prisindeks", b), ("PrisEndr", b), ("Volumindeks", a), ("Volumindeks", b), ("VolumEndr", b))]
            if None in vals or 0 in (vals[0], vals[3]):
                continue
            maks = max(maks, abs((vals[1] / vals[0] - 1) * 100 - vals[2]), abs((vals[4] / vals[3] - 1) * 100 - vals[5]))
    kontroll("K10 endringsrater mot indekser", round(maks, 2), 0.15)

    # K11 Samme siste måned i 08792 og 12308, og synonymene peker på land som finnes
    if mtid[-1] != rtid[-1]:
        feil(f"08792 slutter {mtid[-1]}, 12308 slutter {rtid[-1]}")
    for ord_, ks in synonymer["ord"].items():
        for k in ks:
            if k not in enkelt:
                feil(f"synonymet «{ord_}» peker på {k}, som ikke er et land i 08804")

    # ---------- Datafilen ----------
    aar_strom = ["Etot", "Itot", "Eoljegass", "Eolje", "Egass", "Ekondens", "Etotusorn", "Eskipplat",
                 "Itotuso", "Iskipplat", "Hbtot", "Hbtusorn"]
    mnd_strom = ["Etot", "Itot", "Eoljegass", "Eolje", "Egass", "Etotusorn", "Eskipplat", "Itotuso", "Hbtot", "Hbtusorn"]

    sitc1 = W["etiketter"]["SITC"]
    landnavn = L["etiketter"]["Land"]
    landliste = []
    for k in enkelt:
        rad = {"k": k, "n": landnavn[k]}
        for s, kort in (("Etot", "e"), ("Etotusorn", "f"), ("Eoljegass", "o"), ("Eskipplat", "s"), ("Itot", "i"), ("Iskipplat", "is")):
            rad[kort] = [lv(s, k, t) for t in laar]
        for ie, kort in (("2", "ve"), ("1", "vi")):
            rad[kort] = [hent(W, ImpEks=ie, Land=k, SITC=s, Tid=sist_aar) for s in "0123456789"]
        landliste.append(rad)

    fastland = []
    for k in vk:
        if k in ("333", "343"):
            continue
        v = [round(vv("2", k, t), 1) for t in vaar]
        if any(v):
            fastland.append({"k": k, "n": V["etiketter"]["SITC"][k], "kn": KORT_SITC3.get(k), "v": v})

    indekser = {}
    for g in INDEKSGRUPPER:
        indekser[g] = {"n": I["etiketter"]["ImpEkspGr"][g]}
        for c, kort in (("Prisindeks", "p"), ("Volumindeks", "v"), ("PrisEndr", "pe"), ("VolumEndr", "ve")):
            indekser[g][kort] = serie(I, itid, ImpEks="2", ImpEkspGr=g, ContentsCode=c)

    rev = {"mnd": rtid}
    for ie, kort in (("2", "e"), ("1", "i")):
        forste, siste, sistepub = [], [], []
        for t in rtid:
            rekke = [(p, rv(ie, "-", p, t)) for p in PUBREKKE]
            rekke = [(p, v) for p, v in rekke if v is not None]
            forste.append(rekke[0][1] if rekke else None)
            siste.append(rekke[-1][1] if rekke else None)
            sistepub.append(rekke[-1][0] if rekke else None)
        rev[kort] = {"f": forste, "s": siste, "p": sistepub}

    data = {
        "oppdatert_aar": H["oppdatert"], "oppdatert_mnd": M["oppdatert"], "oppdatert_ind": I["oppdatert"], "hentet": hentet,
        "aar": {"tid": haar, "s": {s: serie(H, haar, HovedVareStrommer=s) for s in aar_strom}},
        "mnd": {"tid": mtid, "s": {s: serie(M, mtid, HovedVareStrommer=s) for s in mnd_strom}},
        "land": {"tid": laar, "liste": landliste},
        "sitc1": {s: sitc1[s] for s in "0123456789"}, "kort_sitc1": KORT_SITC1,
        "varer": {"tid": vaar, "fastland": fastland, "uford": [uford[t] for t in vaar]},
        "ind": {"tid": itid, "grupper": indekser},
        "rev": rev,
        "synonymer": synonymer["ord"], "usikre_synonymer": synonymer["usikker"],
    }
    UT.parent.mkdir(exist_ok=True)
    UT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(f"muh: {len(enkelt)} land, {len(haar)} år, {len(mtid)} måneder til {mtid[-1]}. "
          f"Kontroller OK, største avvik: " + "; ".join(f"{k} {v}" for k, v in AVVIK.items()) + f". {UT.stat().st_size // 1024} kB")


if __name__ == "__main__":
    main()

"""Struktur og kontroller for rådataene i muh (steg 3).

Leser data/raw/*.json (json-stat2), teller strukturen og kjører kontrollene
som er beskrevet i docs/03-kildekart.md. Avslutter med feilkode hvis en
kontroll feiler, slik at den kan stoppe bygget i steg 4.

Bare Pythons standardbibliotek.
"""

import itertools
import json
import sys
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
AGGREGATER = {"00", "01", "02", "03", "04", "05", "06", "10", "16", "17", "20", "40", "60", "70", "80", "90"}
FEIL = []


class Kube:
    def __init__(self, navn):
        self.d = json.loads((RAW / f"{navn}.json").read_text(encoding="utf-8"))
        self.ids = self.d["id"]
        self.kat = {x: list(self.d["dimension"][x]["category"]["index"]) for x in self.ids}
        self.lab = {x: self.d["dimension"][x]["category"]["label"] for x in self.ids}
        self.status = {int(k): v for k, v in self.d.get("status", {}).items()}
        self._ix = {}
        mult = 1
        self._mult = {}
        for x, n in reversed(list(zip(self.ids, self.d["size"]))):
            self._mult[x] = mult
            mult *= n

    def pos(self, **koder):
        return sum(self.kat[x].index(koder[x]) * self._mult[x] for x in self.ids)

    def v(self, **koder):
        return self.d["value"][self.pos(**koder)]

    def s(self, **koder):
        return self.status.get(self.pos(**koder))


def sjekk(navn, ok, detalj):
    print(f"  [{'OK ' if ok else 'FEIL'}] {navn}: {detalj}")
    if not ok:
        FEIL.append(navn)


def tall(v):
    return 0 if v is None else v


def main():
    print("STRUKTUR")
    L = Kube("land_aar")
    land = L.kat["Land"]
    hist = [k for k in land if k not in AGGREGATER and all(L.s(HovedVareStrommer=s, Land=k, ContentsCode="Verdi", Tid=t) == "."
                                   for s in ("Etot", "Itot") for t in L.kat["Tid"])]
    agg = [k for k in land if k in AGGREGATER]
    enkelt = [k for k in land if k not in AGGREGATER and k not in hist]
    print(f"  08804: {len(land)} landkoder = {len(agg)} aggregater (inkl. 90) + {len(hist)} historiske uten tall + {len(enkelt)} land og 97 Uspesifisert")
    aar = L.kat["Tid"]
    for t in ("2015", "2025"):
        e = sum(1 for k in enkelt if tall(L.v(HovedVareStrommer="Etot", Land=k, ContentsCode="Verdi", Tid=t)) > 0)
        i = sum(1 for k in enkelt if tall(L.v(HovedVareStrommer="Itot", Land=k, ContentsCode="Verdi", Tid=t)) > 0)
        print(f"  {t}: land med eksport minst 0,5 mill. kr: {e}, med import: {i}")
    noe = [k for k in enkelt if any(tall(L.v(HovedVareStrommer=s, Land=k, ContentsCode="Verdi", Tid=t)) > 0
                                     for s in ("Etot", "Itot") for t in aar)]
    print(f"  Land med handel minst ett år 2015–2025: {len(noe)}")
    og = [k for k in enkelt if tall(L.v(HovedVareStrommer="Eoljegass", Land=k, ContentsCode="Verdi", Tid="2025")) > 0]
    print(f"  Land med eksport av olje og gass i 2025: {len(og)}")
    tot25 = L.v(HovedVareStrommer="Etot", Land="00", ContentsCode="Verdi", Tid="2025")
    topp = sorted(enkelt, key=lambda k: -tall(L.v(HovedVareStrommer="Etot", Land=k, ContentsCode="Verdi", Tid="2025")))
    andel10 = sum(tall(L.v(HovedVareStrommer="Etot", Land=k, ContentsCode="Verdi", Tid="2025")) for k in topp[:10]) / tot25
    print(f"  Ti største eksportland 2025 tar {andel10 * 100:.1f} prosent av eksporten")
    for k in topp[:10]:
        e = L.v(HovedVareStrommer="Etot", Land=k, ContentsCode="Verdi", Tid="2025")
        o = tall(L.v(HovedVareStrommer="Eoljegass", Land=k, ContentsCode="Verdi", Tid="2025"))
        print(f"    {k} {L.lab['Land'][k]:<16} eksport {e:>8}  olje og gass {o / e * 100:5.1f} prosent")
    u = [L.v(HovedVareStrommer="Itot", Land="97", ContentsCode="Verdi", Tid=t) for t in aar]
    print(f"  Uspesifisert import (97) 2015–2025: {u}")
    eu = {t: (L.v(HovedVareStrommer="Etot", Land="03", ContentsCode="Verdi", Tid=t),
              L.v(HovedVareStrommer="Etot", Land="16", ContentsCode="Verdi", Tid=t)) for t in ("2019", "2020", "2021")}
    print(f"  EU (03) mot EU unntatt Storbritannia (16), eksport: {eu}")

    V = Kube("varer_aar")
    koder = [k for k in V.kat["SITC"] if k != "-"]
    print(f"  08819: {len(koder)} tresifrede varegrupper + «Varer i alt»")
    tomme = sum(1 for k in koder if all(V.v(ImpEks="2", SITC=k, ContentsCode="Verdi", Tid=t) in (None, 0) for t in V.kat["Tid"]))
    print(f"  Varegrupper uten eksport noe år 2015–2025: {tomme}")

    I = Kube("indekser")
    print(f"  06322: {len(I.kat['ImpEkspGr'])} varegrupper, {len(I.kat['Tid'])} år, tomme celler {sum(1 for v in I.d['value'] if v is None)}")

    print("KONTROLLER")
    # K1 Sum av land = Alle land
    maks = 0
    for s in ("Etot", "Etotusorn", "Eoljegass", "Eskipplat", "Itot", "Iskipplat"):
        for t in aar:
            sm = sum(tall(L.v(HovedVareStrommer=s, Land=k, ContentsCode="Verdi", Tid=t)) for k in enkelt)
            maks = max(maks, abs(sm - L.v(HovedVareStrommer=s, Land="00", ContentsCode="Verdi", Tid=t)))
    sjekk("K1 sum av land = Alle land (08804)", maks <= 20, f"største avvik {maks} mill. kr over 6 strømmer og 11 år")

    # K2 Eksport = fastland + olje og gass + skip og plattformer, per land og år
    maks = 0
    for k, t in itertools.product(land, aar):
        e = L.v(HovedVareStrommer="Etot", Land=k, ContentsCode="Verdi", Tid=t)
        if e is None:
            continue
        d = e - sum(tall(L.v(HovedVareStrommer=s, Land=k, ContentsCode="Verdi", Tid=t)) for s in ("Etotusorn", "Eoljegass", "Eskipplat"))
        maks = max(maks, abs(d))
    sjekk("K2 eksport = fastland + olje og gass + skip og plattformer (08804)", maks <= 2, f"største avvik {maks} mill. kr")

    # K3 Balansene i 08800
    H = Kube("hovedtall_aar")
    maks_hb = maks_fb = 0
    for t in H.kat["Tid"]:
        g = lambda s: tall(H.v(HovedVareStrommer=s, ContentsCode="Verdi", Tid=t))
        maks_hb = max(maks_hb, abs(g("Etot") - g("Itot") - g("Hbtot")))
        maks_fb = max(maks_fb, abs(g("Etotusorn") - g("Itotuso") - g("Hbtusorn")))
    sjekk("K3a handelsbalansen = eksport − import (08800, 1960–2025)", maks_hb <= 2, f"største avvik {maks_hb}")
    sjekk("K3b fastlandsbalansen = fastlandseksport − import utenom skip og plattformer", maks_fb <= 2, f"største avvik {maks_fb}")

    # K4 08804 Alle land = 08800
    maks = 0
    for s in ("Etot", "Etotusorn", "Eoljegass", "Eskipplat", "Itot", "Iskipplat"):
        for t in aar:
            maks = max(maks, abs(L.v(HovedVareStrommer=s, Land="00", ContentsCode="Verdi", Tid=t)
                                 - H.v(HovedVareStrommer=s, ContentsCode="Verdi", Tid=t)))
    sjekk("K4 08804 «Alle land» = 08800", maks == 0, f"største avvik {maks}")

    # K5 Fastlandseksport fra varegrupper: total − 333 − 343 − skip og plattformer
    maks = 0
    for t in V.kat["Tid"]:
        g = lambda k: tall(V.v(ImpEks="2", SITC=k, ContentsCode="Verdi", Tid=t)) / 1000
        regnet = g("-") - g("333") - g("343") - H.v(HovedVareStrommer="Eskipplat", ContentsCode="Verdi", Tid=t)
        maks = max(maks, abs(regnet - H.v(HovedVareStrommer="Etotusorn", ContentsCode="Verdi", Tid=t)))
    sjekk("K5 fastlandseksport = total − SITC 333 − 343 − skip og plattformer (08819 mot 08800)", maks <= 2, f"største avvik {maks:.1f} mill. kr")

    # K6 Tresifrede varegrupper mot «Varer i alt» (08819). Summerer ikke: en del finnes bare på ensifret nivå.
    W = Kube("land_varer")
    gap = {}
    for t in V.kat["Tid"]:
        sm = sum(tall(V.v(ImpEks="2", SITC=k, ContentsCode="Verdi", Tid=t)) for k in koder)
        gap[t] = round((V.v(ImpEks="2", SITC="-", ContentsCode="Verdi", Tid=t) - sm) / 1000)
    print(f"  [INFO] K6 eksport som ikke ligger på noen tresifret varegruppe (08819), mill. kr: {gap}")
    per_gruppe = {}
    for s_ in "0123456789":
        tre = sum(tall(V.v(ImpEks="2", SITC=k, ContentsCode="Verdi", Tid="2025")) for k in koder if k[0] == s_)
        en = W.v(ImpEks="2", Land="00", SITC=s_, ContentsCode="Verdi", Tid="2025")
        if abs(en - tre) > 1000:
            per_gruppe[s_] = round((en - tre) / 1000)
    print(f"  [INFO]    fordelt på ensifret SITC i 2025 (08809 minus sum av tresifret), mill. kr: {per_gruppe}")
    sjekk("K6 avviket mellom tre- og ensifret er det samme som avviket mot totalen (2025)",
          abs(sum(per_gruppe.values()) - gap["2025"]) <= 2, f"{sum(per_gruppe.values())} mot {gap['2025']} mill. kr")

    # K7 08809: ensifret SITC summerer per land, og total per land = 08804
    maks_s = maks_l = 0
    for ie, k in itertools.product(("1", "2"), W.kat["Land"]):
        tot = W.v(ImpEks=ie, Land=k, SITC="-", ContentsCode="Verdi", Tid="2025")
        if tot is None:
            continue
        sm = sum(tall(W.v(ImpEks=ie, Land=k, SITC=str(s), ContentsCode="Verdi", Tid="2025")) for s in range(10))
        maks_s = max(maks_s, abs(sm - tot))
        h = L.v(HovedVareStrommer="Itot" if ie == "1" else "Etot", Land=k, ContentsCode="Verdi", Tid="2025")
        if h is not None and k not in AGGREGATER:
            maks_l = max(maks_l, abs(tot / 1000 - h))
    sjekk("K7a ensifret SITC summerer per land (08809)", maks_s <= 20, f"største avvik {maks_s} tusen kr")
    sjekk("K7b total per enkeltland i 08809 = 08804", maks_l <= 0.5, f"største avvik {maks_l:.3f} mill. kr")
    oecd = (W.v(ImpEks="2", Land="04", SITC="-", ContentsCode="Verdi", Tid="2025") / 1000,
            L.v(HovedVareStrommer="Etot", Land="04", ContentsCode="Verdi", Tid="2025"))
    print(f"  [INFO] K7c OECD (04) eksport 2025 i 08809 og 08804: {oecd[0]:.0f} mot {oecd[1]} mill. kr. Aggregatene er ikke like mellom tabellene.")

    # K8 Månedstall 2025 summerer til årstallet
    M = Kube("hovedtall_mnd")
    maks = 0
    for s in ("Etot", "Itot", "Etotusorn"):
        sm = sum(M.v(HovedVareStrommer=s, ContentsCode="VerdiUjustert", Tid=f"2025M{m:02d}") for m in range(1, 13))
        maks = max(maks, abs(sm - H.v(HovedVareStrommer=s, ContentsCode="Verdi", Tid="2025")))
    sjekk("K8 sum av månedene 2025 (08792) = årstall 2025 (08800)", maks <= 12, f"største avvik {maks} mill. kr")

    # K9 Endelige månedstall summerer til endelig årstall (12308 mot 08800), 2016–2024
    R = Kube("revisjoner")
    maks = 0
    for aar_ in range(2016, 2025):
        for ie, s in (("2", "Etot"), ("1", "Itot")):
            pub = "14" if aar_ <= 2024 else "13"
            sm = sum(tall(R.v(ImpEks=ie, SITC="-", PubliseringMnd=pub, ContentsCode="Verdi", Tid=f"{aar_}M{m:02d}"))
                     for m in range(1, 13)) / 1000
            maks = max(maks, abs(sm - H.v(HovedVareStrommer=s, ContentsCode="Verdi", Tid=str(aar_))))
    sjekk("K9 endelige månedstall summerer til årstallet (12308 mot 08800, 2016–2024)", maks <= 1, f"største avvik {maks:.2f} mill. kr")

    # K10 Publiserte endringsrater mot rater regnet fra avrundede indekser
    maks = 0
    for ie, g in itertools.product(("1", "2"), I.kat["ImpEkspGr"]):
        for a, b in zip(I.kat["Tid"], I.kat["Tid"][1:]):
            p0 = I.v(ImpEks=ie, ImpEkspGr=g, ContentsCode="Prisindeks", Tid=a)
            p1 = I.v(ImpEks=ie, ImpEkspGr=g, ContentsCode="Prisindeks", Tid=b)
            pub = I.v(ImpEks=ie, ImpEkspGr=g, ContentsCode="PrisEndr", Tid=b)
            if None in (p0, p1, pub) or p0 == 0:
                continue
            maks = max(maks, abs((p1 / p0 - 1) * 100 - pub))
    print(f"  [INFO] K10 prisendring regnet fra indeksene avviker fra publisert med inntil {maks:.1f} prosentpoeng. Bruk publiserte rater.")

    # Revisjonsstørrelse: første publisering mot endelig, eksport i alt
    print("REVISJONER (eksport i alt, første publisering mot endelig)")
    for aar_ in range(2016, 2025):
        rel = []
        for m in range(1, 13):
            t = f"{aar_}M{m:02d}"
            pub_forste = f"{m + 1:02d}" if m < 12 else "01"
            f = R.v(ImpEks="2", SITC="-", PubliseringMnd=pub_forste, ContentsCode="Verdi", Tid=t)
            e = R.v(ImpEks="2", SITC="-", PubliseringMnd="14", ContentsCode="Verdi", Tid=t)
            if f and e:
                rel.append((e / f - 1) * 100)
        if rel:
            print(f"  {aar_}: snitt absolutt revisjon {sum(abs(x) for x in rel) / len(rel):.1f} prosent, største {max(rel, key=abs):+.1f} prosent")

    if FEIL:
        print(f"\n{len(FEIL)} kontroller feilet: {FEIL}")
        sys.exit(1)
    print("\nAlle kontroller bestått.")


if __name__ == "__main__":
    main()

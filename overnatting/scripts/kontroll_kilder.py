"""Struktur og kontroller for rådataene i overnatting (steg 3).

Leser data/raw/*.json (json-stat2 og KLASS), teller strukturen og kjører
kontrollene K1–K12 som er beskrevet i docs/03-kildekart.md. Avslutter med
feilkode hvis en kontroll feiler, slik at den kan stoppe bygget i steg 4.

Bruk, fra roten av repoet:
    python overnatting/scripts/kontroll_kilder.py

Bare Pythons standardbibliotek.
"""

import json
import sys
from collections import Counter
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
FEIL = []
UTLAND_AGG = {"00000", "ccc", "000"}


class Kube:
    def __init__(self, navn):
        self.d = json.loads((RAW / f"{navn}.json").read_text(encoding="utf-8"))
        self.ids = self.d["id"]
        self.kat = {x: list(self.d["dimension"][x]["category"]["index"]) for x in self.ids}
        self.lab = {x: self.d["dimension"][x]["category"]["label"] for x in self.ids}
        self.status = {int(k): v for k, v in (self.d.get("status") or {}).items()}
        self._pos = {x: {k: i for i, k in enumerate(self.kat[x])} for x in self.ids}
        self._mult, m = {}, 1
        for x, n in reversed(list(zip(self.ids, self.d["size"]))):
            self._mult[x] = m
            m *= n

    def pos(self, **k):
        return sum(self._pos[x][k[x]] * self._mult[x] for x in self.ids)

    def v(self, **k):
        return self.d["value"][self.pos(**k)]

    def s(self, **k):
        return self.status.get(self.pos(**k))


def sjekk(navn, ok, detalj):
    print(f"  [{'OK ' if ok else 'FEIL'}] {navn}: {detalj}")
    if not ok:
        FEIL.append(navn)


def nb(x):
    return f"{x:,}".replace(",", " ")


def main():
    rt = Kube("region_tid")
    ft = Kube("fylke_type")
    ln = Kube("land_nasjonalt")
    sj = Kube("sesongjustert")
    hf = Kube("hotell_formal")
    rh = Kube("region_hotell")
    la, lb = Kube("region_land_a"), Kube("region_land_b")
    klass = json.loads((RAW / "klass_527.json").read_text(encoding="utf-8"))["codes"]
    korr = json.loads((RAW / "klass_527_kommune.json").read_text(encoding="utf-8"))["correspondenceMaps"]
    geo = json.loads((RAW / "kommuner2024-S.geojson").read_text(encoding="utf-8"))

    REG = [c["code"] for c in klass]
    FYL = sorted({r[:2] for r in REG})
    T = rt.kat["Tid"]
    G2 = rt.kat["InnKvartering1"]

    print("Struktur")
    print(f"  Reiselivsregioner i KLASS 527: {len(REG)}. Regionkoder i 14172: {len(rt.kat['Region'])}")
    print(f"  Måneder i region_tid: {T[0]}–{T[-1]} ({len(T)})")
    for kube, navn in ((rt, "region_tid"), (la, "region_land_a"), (lb, "region_land_b"), (rh, "region_hotell")):
        c = Counter(kube.status.values())
        print(f"  {navn}: {nb(len(kube.d['value']))} celler, status {dict(c)}")
    land = [l for l in ln.kat["Landkoder2"] if l not in UTLAND_AGG]
    null16 = [l for l in land if all(ln.v(Region="0N", InnKvartering1="00", Landkoder2=l, ContentsCode="Overnattinger",
                                           Tid=f"2016M{m:02d}") == 0 for m in range(1, 13))]
    print(f"  Landkoder: {len(ln.kat['Landkoder2'])}, med 0 i hele 2016: {len(null16)}")

    print("Kontroller")
    # K1 innkvarteringsgruppene summerer
    maks = 0
    for r in ft.kat["Region"]:
        for l in ("00000", "000", "ccc"):
            for t in ft.kat["Tid"]:
                k = dict(Region=r, Landkoder2=l, ContentsCode="Overnattinger", Tid=t)
                deler = [ft.v(InnKvartering1=g, **k) for g in ("01", "02", "03+04")]
                tot = ft.v(InnKvartering1="00", **k)
                if None in deler or tot is None:
                    continue
                maks = max(maks, abs(sum(deler) - tot))
    sjekk("K1", maks == 0, f"hotell + camping + hyttegrender og vandrerhjem = i alt, landet og fylker, største avvik {maks}")

    # K2 Norge + utlandet = i alt, og felles undertrykking
    maks, ulik = 0, 0
    for r in rt.kat["Region"]:
        for g in G2:
            for t in T:
                k = dict(Region=r, InnKvartering1=g, ContentsCode="Overnattinger", Tid=t)
                ss = {rt.s(Landkoder2=l, **k) for l in ("00000", "000", "ccc")}
                if len(ss) > 1:
                    ulik += 1
                    continue
                if ss == {None}:
                    maks = max(maks, abs(rt.v(Landkoder2="000", **k) + rt.v(Landkoder2="ccc", **k) - rt.v(Landkoder2="00000", **k)))
    sjekk("K2", maks == 0 and ulik == 0, f"Norge + utlandet = i alt per region, avvik {maks}; ulik undertrykking {ulik}")

    # K3 land summerer til utlandet i alt fra 2018
    avvik = Counter()
    for t in ln.kat["Tid"]:
        for g in ln.kat["InnKvartering1"]:
            k = dict(Region="0N", InnKvartering1=g, ContentsCode="Overnattinger", Tid=t)
            d = ln.v(Landkoder2="ccc", **k) - sum(ln.v(Landkoder2=l, **k) or 0 for l in land)
            if g == "00":
                avvik[t[:4]] += d
    fra18 = max(abs(v) for a, v in avvik.items() if a >= "2018")
    sjekk("K3", fra18 <= 100, f"land = utlandet i alt fra 2018, største årsavvik {fra18}. "
          f"Før 2018: 2016 {nb(avvik['2016'])}, 2017 {nb(avvik['2017'])} (kjent, landtall brukes fra 2018)")

    # K4 og K5 regioner mot fylker
    maks, n_ok, alene = 0, 0, 0
    for f in FYL:
        rr = [r for r in REG if r[:2] == f]
        for g in G2:
            for t in T:
                k = dict(InnKvartering1=g, Landkoder2="00000", ContentsCode="Overnattinger", Tid=t)
                sup = [r for r in rr if rt.s(Region=r, **k)]
                if len(sup) == 1 and not rt.s(Region=f, **k):
                    alene += 1
                if sup or rt.s(Region=f, **k):
                    continue
                n_ok += 1
                maks = max(maks, abs(sum(rt.v(Region=r, **k) for r in rr) - rt.v(Region=f, **k)))
    sjekk("K4", maks == 0, f"sum av regioner = fylket i {nb(n_ok)} fylke-måneder uten undertrykking, største avvik {maks}")
    sjekk("K5", alene == 0, f"én undertrykt region alene i et publisert fylke: {alene} tilfeller")

    # K6 ujustert i 14178 = 14162. Kjent avvik: 2024M05 for landet og Møre og Romsdal,
    # der 14162 er rettet uten at 14178 er oppdatert (funnet 24.11.2026).
    KJENT_K6 = {"2024M05"}
    maks, utenfor = 0, []
    for r in sj.kat["Region"]:
        for l in ("00000", "000", "ccc"):
            for t in sj.kat["Tid"]:
                for g in ("00", "01", "02+03+04"):
                    v = sj.v(Region=r, InnKvartering1=g, Landkoder2=l, ContentsCode="Overnattinger", Tid=t)
                    if v is None:
                        continue
                    k = dict(Region=r, Landkoder2=l, ContentsCode="Overnattinger", Tid=t)
                    ref = (ft.v(InnKvartering1="02", **k) + ft.v(InnKvartering1="03+04", **k)) if g == "02+03+04" \
                        else ft.v(InnKvartering1=g, **k)
                    if v != ref:
                        maks = max(maks, abs(v - ref))
                        if t not in KJENT_K6:
                            utenfor.append((r, g, l, t))
    sjekk("K6", not utenfor, f"ujustert i 14178 = 14162 utenom kjent avvik i 2024M05 (største {maks}); nye avvik: {len(utenfor)}")

    # K7 formål
    avv1 = [abs(sum(hf.v(Region="0N", HotellFormal=f, ContentsCode="Overnattinger", Tid=t) for f in ("01", "02", "03"))
                - hf.v(Region="0N", HotellFormal="00", ContentsCode="Overnattinger", Tid=t)) for t in hf.kat["Tid"]]
    maks1, n1 = max(avv1), sum(1 for a in avv1 if a)
    maks2 = max(abs(hf.v(Region="0N", HotellFormal="00", ContentsCode="Overnattinger", Tid=t)
                    - ft.v(Region="0N", InnKvartering1="01", Landkoder2="00000", ContentsCode="Overnattinger", Tid=t))
                for t in ft.kat["Tid"])
    sjekk("K7", maks1 <= 100 and n1 <= 10 and maks2 == 0,
          f"formål summerer til i alt utenom {n1} måneder med avvik ≤ {maks1} (kjent); 14166 = 14162 hotell 2016– (avvik {maks2})")

    # K8 region_land = region_tid for aggregatene, og land summerer per region fra 2018
    maks, sumavvik, n_sum = 0, 0, 0
    for kube in (la, lb):
        rland = [l for l in kube.kat["Landkoder2"] if l not in UTLAND_AGG]
        for r in kube.kat["Region"]:
            for g in G2:
                for t in kube.kat["Tid"]:
                    for l in ("00000", "000", "ccc"):
                        k = dict(Region=r, InnKvartering1=g, Landkoder2=l, ContentsCode="Overnattinger", Tid=t)
                        a, b = kube.v(**k), rt.v(**k)
                        if (a is None) != (b is None) or (a is not None and a != b):
                            maks = max(maks, abs((a or 0) - (b or 0)) or 1)
                    k = dict(Region=r, InnKvartering1=g, ContentsCode="Overnattinger", Tid=t)
                    if kube.s(Landkoder2="ccc", **k) or any(kube.s(Landkoder2=l, **k) == ":" for l in rland):
                        continue
                    n_sum += 1
                    sumavvik = max(sumavvik, abs(kube.v(Landkoder2="ccc", **k) - sum(kube.v(Landkoder2=l, **k) or 0 for l in rland)))
    sjekk("K8", maks == 0 and sumavvik <= 100,
          f"region_land = region_tid (avvik {maks}); land = utlandet per region i {nb(n_sum)} tilfeller uten undertrykte land, største avvik {sumavvik}")

    # K9 regionkoder
    rk = {r for r in rt.kat["Region"] if len(r) == 5}
    hk = {r for r in rh.kat["Region"] if len(r) == 5}
    sjekk("K9", rk == set(REG) == hk, f"66 regionkoder i 14172 og 14176 = KLASS 527 ({len(rk)}, {len(hk)}, {len(REG)})")

    # K10 pris per rom
    # Losjiomsetning er i hele 1 000 kr, så avrundingen gir inntil 500 / utleide rom kroner, pluss avrunding av prisen.
    maks, over = 0, 0
    for r in rh.kat["Region"]:
        for t in rh.kat["Tid"]:
            p, lo, ur = (rh.v(Region=r, ContentsCode=c, Tid=t) for c in ("PrisRom", "LosjiOms", "UtleigdeRom"))
            if None in (p, lo, ur) or ur == 0:
                continue
            a = abs(p - lo * 1000 / ur)
            maks = max(maks, a)
            if a > 500 / ur + 0.5:
                over += 1
    sjekk("K10", over == 0, f"pris per rom = losjiomsetning / utleide rom innenfor avrunding; største avvik {maks:.2f} kr, utenfor {over}")

    # K11 kommuner og kart
    kk = Counter(m["targetCode"] for m in korr)
    gk = {f["properties"]["kommunenummer"] for f in geo["features"]}
    feil_fylke = sum(1 for m in korr if m["sourceCode"][:2] != m["targetCode"][:2])
    uten = [r for r in REG if r not in {m["sourceCode"] for m in korr}]
    sjekk("K11", set(kk) == gk and max(kk.values()) == 1 and feil_fylke == 0 and uten == ["21101"],
          f"{len(kk)} kommuner i KLASS = {len(gk)} i kartet, hver i én region, {feil_fylke} på tvers av fylke; regioner uten kommune: {uten}")

    # K12 tall brukt i steg 1 og 2
    v = lambda **k: ft.v(ContentsCode="Overnattinger", **k)
    aar25 = sum(v(Region="0N", InnKvartering1="00", Landkoder2="00000", Tid=f"2025M{m:02d}") for m in range(1, 13))
    fb = Kube("fritidsbolig")
    ru = Kube("reiseundersokelsen")
    ikke = sum(ru.v(InnKvartering="75", Reisetype="01", ContentsCode="Overnattinger", Tid=f"2025K{q}") for q in range(1, 5))
    forventet = [
        ("hotell sept. 2026", v(Region="0N", InnKvartering1="01", Landkoder2="00000", Tid="2026M09"), 2579128),
        ("kommersielle sept. 2026", v(Region="0N", InnKvartering1="00", Landkoder2="00000", Tid="2026M09"), 3448079),
        ("utenlandske hotell sept. 2026", v(Region="0N", InnKvartering1="01", Landkoder2="ccc", Tid="2026M09"), 841630),
        ("fritidsbolig sept. 2026", fb.v(Landsdel="0", Landkoder="00000", ContentsCode="Overnattinger", Tid="2026M09"), 77403),
        ("sesongjustert hotell aug. 2026", sj.v(Region="0N", InnKvartering1="01", Landkoder2="00000",
                                               ContentsCode="OvernattingerSesongj", Tid="2026M08"), 2428988),
        ("sesongjustert hotell sept. 2026", sj.v(Region="0N", InnKvartering1="01", Landkoder2="00000",
                                                ContentsCode="OvernattingerSesongj", Tid="2026M09"), 2408544),
        ("kommersielle 2025", aar25, 40590017),
        ("ikke-kommersielle 2025, mill.", round(ikke, 1), 58.2),
    ]
    avvik = [(n, a, b) for n, a, b in forventet if a != b]
    sjekk("K12", not avvik, f"{len(forventet)} tall fra steg 1–2 gjenskapt" + (f", avvik: {avvik}" if avvik else ""))

    if FEIL:
        sys.exit(f"Kontroller feilet: {', '.join(FEIL)}")
    print("Alle kontroller OK")


if __name__ == "__main__":
    main()

"""Lager build/innvbef-omrade.json fra rådata i data/raw/ og kontrollerer summene.

Kjøres av felles/bygg.py. Stopper med feil hvis en kontroll ikke går opp:
- 07108: kommunene og fylkene (med restkoder) summerer helt likt per verdensdel og år
- 07108: alle regioner summerer til landet i 05182, alle år (avrunding gir inntil 314)
- 07108: kommunene i hvert fylke summerer til fylket, fra 2024 (før det ligger delte kommuner i restkoden)
- 07108 og 09817 gir samme antall per kommune i 2026
- 07459: kommunene og restkodene summerer til landet i 05803, og fylkene likeså
- 09817: summen av landbakgrunner = «Alle land» per kommune og fylke, 2026
- 09817: publisert andel = antall / folkemengde fra 07459, 2026
- kartet har nøyaktig de samme 357 kommunene som tabellene
- synonymene peker på kommuner og land som finnes
Toleransene er satt etter faktiske avvik og er forklart der de står. Bare standardbiblioteket.
"""
import itertools
import json
import math
import pathlib
import sys

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "innvbef-omrade.json"
AVVIK = {}
SISTE = "2026"


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


def kartstier(geojson, knr):
    """Fra arealprofiler: sfærisk transvers Mercator med sentralmeridian 15° Ø (som UTM 33),
    Douglas-Peucker-forenkling og SVG-stier i et koordinatsystem 1000 piksler bredt.
    Gir også en avgrensningsboks per kommune, brukt til å zoome til fylket."""
    l0 = math.radians(15)

    def proj(lon, lat):
        lam, phi = math.radians(lon) - l0, math.radians(lat)
        b = math.cos(phi) * math.sin(lam)
        return 0.5 * math.log((1 + b) / (1 - b)), -math.atan2(math.tan(phi), math.cos(lam))

    def dp(pts, eps):
        if len(pts) < 3:
            return pts
        (x1, y1), (x2, y2) = pts[0], pts[-1]
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy) or 1e-12
        imax, dmax = 0, 0
        for i in range(1, len(pts) - 1):
            d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / n
            if d > dmax:
                imax, dmax = i, d
        if dmax <= eps:
            return [pts[0], pts[-1]]
        return dp(pts[:imax + 1], eps)[:-1] + dp(pts[imax:], eps)

    feats = {f["properties"]["kommunenummer"]: f["geometry"] for f in geojson["features"]}
    proj_ringer, xs, ys = {}, [], []
    for k in knr:
        g = feats[k]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        ringer = []
        for poly in polys:
            for ring in poly:
                r = [proj(*c[:2]) for c in ring]
                ringer.append(r)
                xs += [p[0] for p in r]
                ys += [p[1] for p in r]
        proj_ringer[k] = ringer
    x0, y0 = min(xs), min(ys)
    skala = 1000 / (max(xs) - x0)
    hoyde = math.ceil((max(ys) - y0) * skala)
    stier, boks = {}, {}
    for k in knr:
        deler, bx, by = [], [], []
        for r in proj_ringer[k]:
            pts = [((x - x0) * skala, (y - y0) * skala) for x, y in r]
            bx += [p[0] for p in pts]
            by += [p[1] for p in pts]
            pts = dp(pts, 0.4)
            if len(pts) < 4:
                continue
            xs_, ys_ = [p[0] for p in pts], [p[1] for p in pts]
            if (max(xs_) - min(xs_)) * (max(ys_) - min(ys_)) < 0.2:   # små holmer forsvinner
                continue
            deler.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts[:-1]) + "Z")
        if not deler:   # en kommune skal aldri forsvinne helt: ta største ring uforenklet
            r = max(proj_ringer[k], key=len)
            deler.append("M" + "L".join(f"{(x - x0) * skala:.1f},{(y - y0) * skala:.1f}" for x, y in r[:-1]) + "Z")
        stier[k] = "".join(deler)
        boks[k] = [round(min(bx), 1), round(min(by), 1), round(max(bx), 1), round(max(by), 1)]
    return {"b": 1000, "h": hoyde, "p": stier, "boks": boks}


def main():
    lt, lb, kt, ft, kb, fb, kd, fd, kl, fl = (les(n) for n in (
        "landet_tid", "landet_bef", "komm_tid", "fylke_tid", "komm_bef", "fylke_bef",
        "komm_delt", "fylke_delt", "komm_land", "fylke_land"))
    vdk = json.loads((RAW / "verdensdel.json").read_text(encoding="utf8"))
    geo = json.loads((RAW / "kommuner2024-S.geojson").read_text(encoding="utf8"))
    syn_k = json.loads((MAPPE / "data" / "synonymer.json").read_text(encoding="utf8"))["synonymer"]
    syn_l = json.loads((MAPPE / "data" / "land-synonymer.json").read_text(encoding="utf8"))

    aar = koder(kt, "Tid")
    vd = koder(kt, "Landbakgrunn")              # 8 verdensdeler, også statsløse og uoppgitt
    if len(vd) != 8:
        feil(f"07108 har {len(vd)} verdensdeler, ventet 8")
    vd_navn = [kt["etiketter"]["Landbakgrunn"][v] for v in vd]

    # ---------- Områdene ----------
    kom_geo = {f["properties"]["kommunenummer"] for f in geo["features"]}
    kom = [r[2:] for r in koder(kt, "Region") if r[2:] in kom_geo]
    if len(kom) != 357 or set(kom) != kom_geo:
        feil(f"kartet og 07108 har ikke de samme kommunene ({len(kom)} av {len(kom_geo)})")
    rest = [r for r in koder(kt, "Region") if r[2:] not in kom_geo]   # Svalbard og Jan Mayen, sokkelen, delte og uoppgitt
    fyl = [r[2:] for r in koder(ft, "Region") if r[2:] not in ("21", "22", "23")]
    for k in kom:
        if k[:2] not in fyl:
            feil(f"kommune {k} har ikke et fylke")
    navn = {k: kt["etiketter"]["Region"]["K-" + k] for k in kom}
    navn.update({f: ft["etiketter"]["Region"]["F-" + f] for f in fyl})

    def tot(t, r, a):
        return sum(hent(t, Region=r, Landbakgrunn=v, Tid=a) for v in vd)

    # ---------- Kontroller på tidsseriene ----------
    # Kommunene og fylkene i 07108 er to aggregeringer av samme tall. De summerer helt likt per verdensdel og år,
    # så denne kontrollen har toleranse 0 og fanger endringer som avrundingen mot 05182 ville skjult.
    for a in aar:
        for v in vd:
            d = sum(hent(kt, Region=r, Landbakgrunn=v, Tid=a) for r in koder(kt, "Region")) - sum(hent(ft, Region=r, Landbakgrunn=v, Tid=a) for r in koder(ft, "Region"))
            if d:
                feil(f"07108 {a}, verdensdel {v}: kommunene summerer til {d} mer enn fylkene")
    for a in aar:
        landet = hent(lt, InnvandrKat="2", Tid=a) + hent(lt, InnvandrKat="3", Tid=a)
        d = sum(tot(kt, r, a) for r in koder(kt, "Region")) - landet
        # Små celler er avrundet i 07108. Største faktiske avvik er 314 (1987) og under 35 fra 1988.
        if abs(d) > (350 if int(a) < 1988 else 40):
            feil(f"07108 {a}: regionene summerer til {d} mer enn landet")
        avvik("07108 regioner mot landet", d)
        d = sum(tot(ft, r, a) for r in koder(ft, "Region")) - landet
        if abs(d) > (350 if int(a) < 1988 else 40):
            feil(f"07108 {a}: fylkene summerer til {d} mer enn landet")
        avvik("07108 fylker mot landet", d)
        if int(a) >= 2024:
            # Fra 2024 er det ingen delte kommuner i restkoden. Før det kan ikke kommunene summeres til fylket.
            for f in fyl:
                d = tot(ft, "F-" + f, a) - sum(tot(kt, "K-" + k, a) for k in kom if k[:2] == f)
                if abs(d) > 40:
                    feil(f"07108 {a}: kommunene i {f} summerer til {d} mer enn fylket")
                avvik("07108 kommuner mot fylke fra 2024", d)
    for k in kom:
        d = tot(kt, "K-" + k, SISTE) - hent(kd, Region=k, InnvandrKat="B-C", ContentsCode="Personer1", Tid=SISTE)
        if abs(d) > 3:   # største faktiske avvik er 1
            feil(f"{k}: 07108 og 09817 gir ulikt antall i {SISTE} ({d})")
        avvik("07108 mot 09817 per kommune", d)
    b_aar = koder(kb, "Tid")
    for a in b_aar:
        if sum(hent(kb, Region=r, Tid=a) for r in koder(kb, "Region")) != hent(lb, Tid=a):
            feil(f"07459 {a}: kommunene summerer ikke til landet")
        if sum(hent(fb, Region=r, Tid=a) for r in koder(fb, "Region")) != hent(lb, Tid=a):
            feil(f"07459 {a}: fylkene summerer ikke til landet")

    # ---------- Tidsserier per område ----------
    # tid[omr] = {"vd": [8 serier], "bef": [...]}. 0 i både teller og nevner for en kommune betyr at
    # kommunen ikke kan følges det året (delt kommune): lagres som null, ikke 0.
    bef_i = [aar.index(a) for a in b_aar]
    tid = {}
    for k in kom:
        b = [hent(kb, Region="K-" + k, Tid=a) or None for a in b_aar]
        s = [[hent(kt, Region="K-" + k, Landbakgrunn=v, Tid=a) for a in aar] for v in vd]
        for j, a in enumerate(b_aar):
            if b[j] is None:   # kommunen kan ikke følges dette året
                if any(s[i][aar.index(a)] for i in range(8)):
                    feil(f"{k} {a}: folketall mangler, men 07108 har personer")
                for i in range(8):
                    s[i][aar.index(a)] = None
        if b[0] is None:
            # Kommunen kan ikke følges fra 1986. Da kan den heller ikke følges i 1970 og 1980, der 07459 mangler.
            for a in aar[:aar.index(b_aar[0])]:
                if any(s[i][aar.index(a)] for i in range(8)):
                    feil(f"{k} {a}: kommunen har personer før første år med folketall")
                for i in range(8):
                    s[i][aar.index(a)] = None
        tid[k] = {"vd": s, "bef": b}
    for f in fyl:
        tid[f] = {"vd": [[hent(ft, Region="F-" + f, Landbakgrunn=v, Tid=a) for a in aar] for v in vd],
                  "bef": [hent(fb, Region="F-" + f, Tid=a) for a in b_aar]}
    landet = {"innv": [hent(lt, InnvandrKat="2", Tid=a) for a in aar], "nmi": [hent(lt, InnvandrKat="3", Tid=a) for a in aar],
              "bef": [hent(lb, Tid=a) for a in aar],
              # Verdensdeler for hele landet: summen av alle fylker og restkoder i 07108 (avviker høyst 314 fra 05182)
              "vd": [[sum(hent(ft, Region=r, Landbakgrunn=v, Tid=a) for r in koder(ft, "Region")) for a in aar] for v in vd]}
    hull = {k: [a for a, v in zip(b_aar, tid[k]["bef"]) if v is None] for k in kom}
    hull = {k: v for k, v in hull.items() if v}

    # ---------- Innvandrere og norskfødte hver for seg (09817) ----------
    d_aar = koder(kd, "Tid")
    delt = {}
    for t, omr in ((kd, kom), (fd, fyl)):
        for o in omr:
            inn = [hent(t, Region=o, InnvandrKat="B", ContentsCode="Personer1", Tid=a) for a in d_aar]
            nmi = [hent(t, Region=o, InnvandrKat="C", ContentsCode="Personer1", Tid=a) for a in d_aar]
            # 0 for begge betyr at dagens områdekode ikke fantes det året (09817 er ikke sammenslått)
            delt[o] = [[x if (x or y) else None for x, y in zip(inn, nmi)], [y if (x or y) else None for x, y in zip(inn, nmi)]]
    for o in kom:
        a = hent(kd, Region=o, InnvandrKat="B", ContentsCode="AndelBefolkning", Tid=SISTE)
        bef = tid[o]["bef"][-1]
        d = round(100 * delt[o][0][-1] / bef, 2) - a
        if abs(d) > 0.011:
            feil(f"09817 {o}: publisert andel {a} er ulik egen beregning")
        avvik("andel kommune (prosentpoeng)", round(d, 3))

    # ---------- Landbakgrunn per område, 2026 ----------
    landkoder = [l for l in koder(kl, "Landbakgrunn") if l not in ("999", "VES", "IVE")]
    landnavn = {l: kl["etiketter"]["Landbakgrunn"][l] for l in landkoder}
    land = {}   # land -> {omr: [innv, nmi]}
    for t, omr in ((kl, kom), (fl, fyl)):
        for o in omr:
            for kat, m in (("B", 0), ("C", 1)):
                s = 0
                for l in landkoder:
                    v = hent(t, Region=o, InnvandrKat=kat, Landbakgrunn=l)
                    s += v
                    if v:
                        land.setdefault(l, {}).setdefault(o, [0, 0])[m] = v
                d = s - hent(t, Region=o, InnvandrKat=kat, Landbakgrunn="999")
                if abs(d) > 5:   # avrundede småceller, største faktiske avvik er 3
                    feil(f"09817 {o} {kat}: summen av land avviker {d} fra «Alle land»")
                avvik("land mot alle land", d)
    # Landet: summen av fylkene (og Svalbard), fordi 09817 ikke er hentet for hele landet per land
    for l, per in land.items():
        per["0"] = [sum(per[f][m] for f in fyl if f in per) for m in (0, 1)]
    land = {l: per for l, per in land.items() if any(per["0"])}
    vd_av = {}
    for g in vdk["values"]:
        for k in g.get("valueMap", []):
            vd_av[k] = g["code"]
    mangler = [l for l in land if l not in vd_av]
    if mangler:
        feil(f"land uten verdensdel: {mangler}")
    landliste = sorted(land, key=lambda l: -sum(land[l]["0"]))

    # ---------- Synonymer ----------
    for ord_, ks in syn_k.items():
        for k in ks:
            if k not in navn:
                feil(f"kommunesynonymet «{ord_}» peker på {k}, som ikke finnes")
    for ord_, ks, _ in syn_l:
        for k in ks:
            if k not in land:
                feil(f"landsynonymet «{ord_}» peker på {k}, som ikke har personer")

    kart = kartstier(geo, kom)

    # Kompakt: land -> [[områdekode, innv, nmi], ...]
    land_ut = {l: [[o, v[0], v[1]] for o, v in sorted(land[l].items())] for l in landliste}
    ut = {
        "kilde": {"oppdatert": {t["navn"]: t["oppdatert"] for t in (lt, lb, kt, ft, kb, fb, kd, fd, kl, fl)},
                  "hentet": json.loads((RAW / "_hentet.json").read_text(encoding="utf8"))["hentet"]},
        "aar": [int(a) for a in aar], "befAar": [int(a) for a in b_aar], "deltAar": [int(a) for a in d_aar],
        "vd": vd_navn, "landet": landet, "tid": tid, "delt": delt, "hull": hull,
        "fylker": [[f, navn[f]] for f in fyl], "kommuner": [[k, navn[k]] for k in kom],
        "land": [[l, landnavn[l], vd_av[l]] for l in landliste], "landOmr": land_ut,
        "verdensdel": [[g["code"], g["label"]] for g in vdk["values"]],
        "synK": syn_k, "synL": syn_l, "kart": kart,
    }
    UT.parent.mkdir(exist_ok=True)
    UT.write_text(json.dumps(ut, ensure_ascii=False, separators=(",", ":"), sort_keys=True), encoding="utf8")
    print(f"build/innvbef-omrade.json: {round(UT.stat().st_size / 1024)} kB · {len(kom)} kommuner, {len(fyl)} fylker, "
          f"{len(landliste)} land · kart {sum(len(p) for p in kart['p'].values()) // 1024} kB · "
          f"kommuner med hull: {', '.join(f'{navn[k]} {v[0]}–{v[-1]}' for k, v in hull.items())} · største avvik: "
          + ", ".join(f"{k} {v}" for k, v in AVVIK.items()))


if __name__ == "__main__":
    main()

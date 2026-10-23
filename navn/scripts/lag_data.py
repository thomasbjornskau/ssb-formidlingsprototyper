"""Lager build/navn.json fra rådata i data/raw/ og kontrollerer tallene.

Kjøres av felles/bygg.py. Stopper med feil hvis en kontroll ikke går opp:
- kjente tall stemmer med det som er publisert (Anna 1881, Noah og Emma 2025, Anne, Hansen)
- alle navn i 10467 finnes i 10501, og alle koder i synonymer.json finnes i 10467
- skrivemåtene i topp 5 er like i statistikkbanken og i SSB-artiklene
- summen av skrivemåtene avviker fra publisert total med høyst 3 (Nora, kjent avvik)
- topp 10-totalene summerer til publisert antall, og publisert andel gjenskapes innen 0,1 prosentpoeng
- antall og andel henger sammen: nevneren (antall / andel) er lik for alle navn samme år og kjønn
Bare standardbiblioteket.
"""
import itertools
import json
import pathlib
import sys

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "navn.json"
AAR = list(range(1880, 2026))
ANTALL_FRA = 1945


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
    fo, pe, et = les("fodte"), les("personer"), les("etternavn")
    syn = json.loads((MAPPE / "data" / "synonymer.json").read_text(encoding="utf8"))
    hentet = json.loads((RAW / "_hentet.json").read_text(encoding="utf8"))

    fkoder, pkoder = koder(fo, "Fornavn"), koder(pe, "Fornavn")
    if [str(a) for a in AAR] != koder(fo, "Tid"):
        feil("10467 har ikke årene 1880–2025")
    p_aar = koder(pe, "Tid")
    e_aar = koder(et, "Tid")

    # 1. Kjente tall
    kjente = [
        (hent(fo, Fornavn="1ANNA", ContentsCode="PersonerProsent", Tid="1881"), 9.036, "Anna 1881, andel"),
        (hent(fo, Fornavn="2NOAH", ContentsCode="Personer", Tid="2025"), 460, "Noah 2025"),
        (hent(fo, Fornavn="1EMMA", ContentsCode="Personer", Tid="2025"), 386, "Emma 2025"),
        (hent(pe, Fornavn="1ANNE", Tid="2025"), 55625, "personer som heter Anne 2025"),
        (hent(et, Etternavn="HANSEN", Tid="2025"), 47879, "Hansen 2025"),
    ]
    for v, fasit, hva in kjente:
        if v != fasit:
            feil(f"{hva}: {v}, ventet {fasit}")

    # 2. Kodene henger sammen
    mangler = set(fkoder) - set(pkoder)
    if mangler:
        feil(f"{len(mangler)} navn i 10467 mangler i 10501, f.eks. {sorted(mangler)[:3]}")
    if any(k[0] not in "12" for k in pkoder):
        feil("navnekode uten kjønnsprefiks 1 eller 2")

    # 3. Topp 5 med skrivemåter
    topp5 = {}
    storste_rest = 0
    for kj, liste in syn["topp5"].items():
        rader = []
        for r in liste:
            deler = []
            for kode, artikkel in r["skrivemaater"]:
                if kode not in fkoder:
                    feil(f"synonymer.json: {kode} finnes ikke i 10467")
                v = hent(fo, Fornavn=kode, ContentsCode="Personer", Tid="2025")
                if v != artikkel:
                    feil(f"{kode}: {v} i statistikkbanken, {artikkel} i artikkelen")
                deler.append([kode, v])
            rest = r["total"] - sum(v for _, v in deler)
            # Toleranse 3: Nora har 3 jenter i totalen som verken står i artikkelen eller statistikkbanken (kildekartet, hull 1)
            if not 0 <= rest <= 3:
                feil(f"{r['navn']}: publisert total {r['total']} avviker {rest} fra skrivemåtene")
            storste_rest = max(storste_rest, rest)
            rader.append({"navn": r["navn"], "total": r["total"], "deler": deler, "rest": rest,
                          "usikker": r.get("usikker")})
        if [x["total"] for x in rader] != sorted((x["total"] for x in rader), reverse=True):
            feil(f"topp 5 {kj} er ikke sortert etter total")
        topp5[kj] = rader

    # 4. Andel og antall: nevneren (navngitte barn av samme kjønn) skal være lik for alle navn samme år
    nevner = {}
    storste_spenn = 0.0
    for kj, pre in (("j", "1"), ("g", "2")):
        nevner[kj] = []
        for a in AAR:
            if a < ANTALL_FRA:
                nevner[kj].append(None)
                continue
            anslag = []
            for k in fkoder:
                if k[0] != pre:
                    continue
                n = hent(fo, tom=True, Fornavn=k, ContentsCode="Personer", Tid=a)
                p = hent(fo, tom=True, Fornavn=k, ContentsCode="PersonerProsent", Tid=a)
                if n and p and n >= 100:
                    anslag.append(n / p * 100)
            if not anslag:
                nevner[kj].append(None)
                continue
            spenn = (max(anslag) - min(anslag)) / min(anslag)
            storste_spenn = max(storste_spenn, spenn)
            # Andelen er publisert med tre desimaler. For navn med minst 100 barn gir det høyst om lag 0,1 prosent usikkerhet
            # i nevneren; 0,5 prosent gir rom for avrunding uten å slippe gjennom en feil kolonne eller et feil år.
            if spenn > 0.005:
                feil(f"nevneren for {kj} {a} spriker {spenn:.2%} mellom navn")
            anslag.sort()
            nevner[kj].append(round(anslag[len(anslag) // 2]))

    # 5. Topp 10 publisert
    for kj, t in syn["topp10"].items():
        if sum(t["totaler"]) != t["antall"]:
            feil(f"topp 10 {kj}: totalene summerer til {sum(t['totaler'])}, ikke {t['antall']}")
        if [r["total"] for r in topp5[kj]] != t["totaler"][:5]:
            feil(f"topp 10 {kj}: topp 5 stemmer ikke med synonymer.json")
        egen = t["antall"] / nevner[kj][-1] * 100
        # Jenter: 13,1 mot publisert 13,2. Nevneren er anslått fra avrundede andeler (kildekartet, kontroll 3)
        if abs(egen - t["andel"]) > 0.1:
            feil(f"topp 10 {kj}: {egen:.2f} prosent regnet, {t['andel']} publisert")

    # 6. Datafilen
    navn, andel, antall, personer = [], {}, {}, {}
    i_fodte = set(fkoder)
    for k in pkoder:
        navn.append([k, pe["etiketter"]["Fornavn"][k]])
        if k in i_fodte:
            andel[k] = [hent(fo, tom=True, Fornavn=k, ContentsCode="PersonerProsent", Tid=a) for a in AAR]
            antall[k] = [hent(fo, tom=True, Fornavn=k, ContentsCode="Personer", Tid=a) for a in AAR if a >= ANTALL_FRA]
        personer[k] = [hent(pe, tom=True, Fornavn=k, Tid=a) for a in p_aar]

    # Mest brukte navn og topp 10 per år, eksakt skrivemåte (egen beregning)
    dominans = {}
    for kj, pre in (("j", "1"), ("g", "2")):
        rad = []
        for i, a in enumerate(AAR):
            sh = sorted(((andel[k][i] or 0, k) for k in fkoder if k[0] == pre), reverse=True)
            rad.append([sh[0][1], sh[0][0], round(sum(x for x, _ in sh[:10]), 3)])
        dominans[kj] = rad

    etter = sorted(((hent(et, tom=True, Etternavn=k, Tid=e_aar[-1]) or 0, k) for k in koder(et, "Etternavn")), reverse=True)[:20]
    etternavn = [[et["etiketter"]["Etternavn"][k], hent(et, tom=True, Etternavn=k, Tid=e_aar[0]), v] for v, k in etter]

    ut = {
        "aar": AAR, "antallFra": ANTALL_FRA, "personerAar": [int(a) for a in p_aar], "etternavnAar": [int(e_aar[0]), int(e_aar[-1])],
        "navn": navn, "andel": andel, "antall": antall, "personer": personer,
        "nevner": nevner, "dominans": dominans, "topp5": topp5, "topp10": syn["topp10"],
        "etternavn": etternavn, "etternavnAntall": len(koder(et, "Etternavn")),
        "kilde": {"oppdatert": {"fodte": fo["oppdatert"], "personer": pe["oppdatert"], "etternavn": et["oppdatert"]},
                  "hentet": hentet["hentet"][:10], "artikler": syn["kilde"]},
    }
    UT.parent.mkdir(exist_ok=True)
    tekst = json.dumps(ut, ensure_ascii=False, separators=(",", ":"))
    UT.write_text(tekst, encoding="utf8")
    print(f"build/navn.json: {len(navn)} navn, {len(andel)} med fødte, {round(len(tekst) / 1024)} kB. "
          f"Største avvik: rest i topp 5 {storste_rest}, spenn i nevneren {storste_spenn:.2%}")


if __name__ == "__main__":
    main()

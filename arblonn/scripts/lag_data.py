"""Lager build/arblonn.json fra rådata i data/raw/ og kontrollerer tallene.

Kjøres av felles/bygg.py. Kjører først alle kontrollene i kontroll_kilder.py
(K1–K13, se docs/03-kildekart.md). Deretter disse, som stopper bygget hvis de
ikke går opp:
- B1 næringenes bidrag til siste månedsendring summerer til totalendringen (±5,
     sesongjusterte næringer summerer med opptil 5 i avvik, K9b)
- B2 jobbvekst og lønnsvekst i build-filen = publiserte tall for alle næringer
     (kopi av K11 på de utvalgte seriene)
- B3 siste måned har foreløpig tall og ikke endelig, nest siste har begge
- B4 alle tosifrede næringer har en gruppe, og hver gruppe har minst én

Bare Pythons standardbibliotek.
"""
import itertools
import json
import pathlib
import runpy
import sys

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "arblonn.json"
AVVIK = {}

N17 = ["01-03", "05-09", "10-33", "35-39", "41-43", "45-47", "49-53", "55-56", "58-63",
       "64-66", "68-75", "77-82", "84", "85", "86-88", "90-99"]
KORT = {
    "00-99": "Alle næringer", "01-03": "Jordbruk, skogbruk og fiske", "05-09": "Bergverk og utvinning",
    "10-33": "Industri", "35-39": "Elektrisitet, vann og renovasjon", "41-43": "Bygg og anlegg",
    "45-47": "Varehandel", "49-53": "Transport og lagring", "55-56": "Overnatting og servering",
    "58-63": "Informasjon og kommunikasjon", "64-66": "Finans og forsikring",
    "68-75": "Teknisk tjenesteyting og eiendom", "77-82": "Forretningsmessig tjenesteyting",
    "84": "Offentlig administrasjon og forsvar", "85": "Undervisning", "86-88": "Helse og sosial",
    "90-99": "Personlig tjenesteyting", "00": "Uoppgitt næring",
}
FYLKER = ["03", "32", "46", "11", "50", "34", "42", "15", "33", "31", "18", "39", "55", "40", "56"]


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
    status = d.get("status") or {}
    celler, symbol = {}, {}
    for n, komb in enumerate(itertools.product(*koder)):
        celler[komb] = d["value"][n]
        if str(n) in status:
            symbol[komb] = status[str(n)]
    etiketter = {dim: d["dimension"][dim]["category"].get("label", {}) for dim in d["id"]}
    return {"navn": navn, "celler": celler, "symbol": symbol, "dims": d["id"], "koder": koder,
            "etiketter": etiketter, "oppdatert": d.get("updated", "")[:10]}


def hent(t, **fast):
    nokkel = tuple(fast[dim] for dim in t["dims"])
    if nokkel not in t["celler"]:
        feil(f"{t['navn']}: finner ikke {fast}")
    return t["celler"][nokkel]


def serie(t, tid, **fast):
    return [hent(t, Tid=x, **fast) for x in tid]


def koder(t, dim):
    return t["koder"][t["dims"].index(dim)]


def avvik(navn, verdi):
    AVVIK[navn] = max(AVVIK.get(navn, 0), verdi)


def gruppe(kode):
    """Tosifret næringskode til gruppe i 17-inndelingen."""
    if kode == "00":
        return "00"
    n = int(kode)
    for g in N17:
        a, _, b = g.partition("-")
        if int(a) <= n <= int(b or a):
            return g
    return None


def main():
    # Kontrollene fra steg 3 stopper bygget med «Kontroll feilet: …»
    runpy.run_path(str(MAPPE / "scripts" / "kontroll_kilder.py"), run_name="__main__")

    m = les("maned")
    q = les("kvartal_naering")
    f = les("kvartal_fylke")
    a = les("arbeidstid")
    ka = les("kjonn_alder")
    e = les("naering88")
    alle = ["00-99"] + N17 + ["00"]

    # --- Månedstall ---
    TM = koder(m, "Tid")
    mnd = {}
    for n in alle:
        r = {}
        for nok, (ver, v) in {"je": ("02", "AntArbForholdSesong"), "jf": ("01", "AntArbForholdSesong"),
                              "le": ("02", "AntLonnstakSesong"), "lf": ("01", "AntLonnstakSesong"),
                              "ke": ("02", "GjsnKontantlonn"), "kf": ("01", "GjsnKontantlonn"),
                              "ue": ("02", "AntArbForhold"), "uf": ("01", "AntArbForhold")}.items():
            r[nok] = serie(m, TM, NACE2007=n, ForelopigEndelig=ver, ContentsCode=v)
        mnd[n] = r
    # B3 siste måned bare foreløpig, nest siste begge
    t = mnd["00-99"]
    if not (t["jf"][-1] is not None and t["je"][-1] is None and t["je"][-2] is not None and t["jf"][-2] is not None):
        feil("B3: forventet foreløpig, ikke endelig, for siste måned og begge for nest siste")
    # B1 bidrag til siste månedsendring
    tot = t["jf"][-1] - t["jf"][-2]
    sum_bidrag = sum(mnd[n]["jf"][-1] - mnd[n]["jf"][-2] for n in N17 + ["00"])
    avvik("B1 bidrag mot total", abs(sum_bidrag - tot))
    if abs(sum_bidrag - tot) > 5:
        feil(f"B1: næringenes bidrag {sum_bidrag} mot total {tot}")

    # --- Kvartalstall, landet ---
    TQ = koder(q, "Tid")
    var_q = {"j": "AntArbForhold", "l": "Lonsstakere", "h": "HeltidsEkvMnd", "a": "GjAvtaltMdlonn",
             "m": "GjMdTotal", "am": "MedianAvtMndLonn", "mm": "MedianMndLonn"}
    kv = {n: {k: serie(q, TQ, Region="Ialt", NACE2007=n, ContentsCode=v) for k, v in var_q.items()} for n in alle}
    # B2 publiserte endringer 2025K2–2026K2 (statistikksiden, tabell 4)
    publ_lonn = [3.9, 4.6, 4.0, 4.6, 4.0, 4.3, 3.6, 3.5, 3.4, 4.5, 4.3, 4.2, 3.7, 4.6, 3.8, 3.6, 3.9, 6.2]
    publ_jobb = [0.8, 1.3, 0.5, 0.6, -0.3, -1.2, 0.9, 2.5, 2.1, -0.4, -0.5, 0.5, 1.0, 2.6, -0.5, 1.1, 1.7, -1.0]
    i1, i0 = TQ.index("2026K2"), TQ.index("2025K2")
    for n, pl, pj in zip(alle, publ_lonn, publ_jobb):
        vl = round((kv[n]["a"][i1] / kv[n]["a"][i0] - 1) * 100, 1)
        vj = round((kv[n]["j"][i1] / kv[n]["j"][i0] - 1) * 100, 1)
        avvik("B2 vekst mot publisert", max(abs(vl - pl), abs(vj - pj)))
        if abs(vl - pl) > 0.05 or abs(vj - pj) > 0.05:
            feil(f"B2: {n} lønnsvekst {vl} (publ. {pl}), jobbvekst {vj} (publ. {pj})")

    # --- Fylker fra 2024K1 ---
    TF = koder(f, "Tid")
    fy_lab = f["etiketter"]["Region"]
    fylke = {}
    for r in FYLKER:
        fylke[r] = {n: {k: serie(f, TF, Region=r, NACE2007=n, ContentsCode=var_q[k]) for k in ("j", "l", "h", "a", "am")}
                    for n in alle}

    # --- Heltid og deltid per næring og kjønn ---
    TA = koder(a, "Tid")
    tid_ = {}
    for n in alle:
        tid_[n] = {}
        for kj in ("0", "1", "2"):
            tid_[n][kj] = {}
            for ht in ("H", "D", "H+D"):
                tid_[n][kj][ht] = {k: serie(a, TA, ArbeidsTidRen=ht, NACE2007=n, Kjonn=kj, ContentsCode=v)
                                   for k, v in (("j", "AntJobber"), ("h", "HeltidsEkvMnd"),
                                                ("a", "AvtaltMndlonn"), ("am", "MedianAvtMndLonn"))}

    # --- Kjønn og alder, landet ---
    alder = koder(ka, "Alder")
    ka_ut = {kj: {al: {k: serie(ka, TQ, Region="Ialt", Kjonn=kj, Alder=al, ContentsCode=v)
                       for k, v in (("j", "AntArbForhold"), ("l", "Lonsstakere"), ("a", "GjAvtaltMdlonn"),
                                    ("am", "MedianAvtMndLonn"), ("t", "GjAvtArbtid"))}
                  for al in alder} for kj in ("0", "1", "2")}

    # --- Tosifrede næringer ---
    e_lab = e["etiketter"]["NACE2007"]
    sub = []
    for k in koder(e, "NACE2007"):
        if k in ("00-99", "00"):
            continue
        g = gruppe(k)
        if g is None:
            feil(f"B4: {k} har ingen gruppe")
        sub.append({"k": k, "n": e_lab[k], "g": g,
                    **{x: serie(e, TQ, NACE2007=k, ContentsCode=v) for x, v in
                       (("j", "AntArbForhold"), ("a", "GjAvtaltMdlonn"), ("am", "MedianAvtMndLonn"))}})
    mangler = [g for g in N17 if not any(s["g"] == g for s in sub)]
    if mangler:
        feil(f"B4: grupper uten tosifrede næringer: {mangler}")

    hentet = json.loads((RAW / "_hentet.json").read_text(encoding="utf8"))["hentet"]
    ut = {
        "hentet": hentet,
        "oppdatert": {"13126": m["oppdatert"], "11654": q["oppdatert"], "13871": a["oppdatert"],
                      "11652": ka["oppdatert"], "12314": e["oppdatert"]},
        "naeringer": [{"k": n, "n": KORT[n]} for n in alle],
        "tm": TM, "mnd": mnd,
        "tq": TQ, "kv": kv,
        "tf": TF, "fylker": [{"k": r, "n": fy_lab[r].split(" - ")[0]} for r in FYLKER], "fylke": fylke,
        "ta": TA, "arbtid": tid_,
        "alder": [{"k": al, "n": ka["etiketter"]["Alder"][al]} for al in alder], "ka": ka_ut,
        "sub": sub,
    }
    UT.parent.mkdir(exist_ok=True)
    UT.write_text(json.dumps(ut, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(f"build/arblonn.json: {round(UT.stat().st_size / 1024)} kB, {len(sub)} tosifrede næringer, "
          f"{len(TM)} måneder, {len(TQ)} kvartaler, {len(FYLKER)} fylker. Største avvik: "
          + ", ".join(f"{k} {v}" for k, v in AVVIK.items()))


if __name__ == "__main__":
    main()

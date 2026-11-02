"""Lager build/pasient.json fra rådata i data/raw/ og kontrollerer tallene.

Kjøres av felles/bygg.py. Kontrollene (D1–D7, se docs/03-kildekart.md) stopper
bygget med «Kontroll feilet: …» hvis de ikke går opp:
- D1 kontakter, døgnopphold og oppholdsdøgn summerer over kapitlene (±36: 21 celler avrundet
     til base 6; største faktiske avvik er 18, i 2016)
- D2 dagbehandlinger summerer over kapitlene (±36, samme grunn)
- D3 kvinner + menn = begge kjønn for alle mål, kapitler og aldre (pasienter ±9, mengdetall ±18;
     største faktiske avvik 6 og 12)
- D4 aldersgruppene summerer til alle aldre (pasienter ±18, mengdetall ±36;
     største faktiske avvik 9 og 18)
- D5 hvert kapittel har blokker, og kapitlet er minst like stort som største blokk
- D6 egen rate per kapittel (pasienter / middelfolkemengde) treffer publisert rate i 14827
     (±0,55: publisert rate er heltall; største faktiske avvik 0,51). Unntak: XV (svangerskap)
     ligger 0–1,4 under publisert hvert år og kontrolleres med ±1,5. Spørsmål til fag.
- D7 20 kapitler og 200 kategoriblokker

Bare Pythons standardbibliotek.
"""
import itertools
import json
import pathlib
import re
import sys

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "pasient.json"
AVVIK = {}

# Korte navn er våre (G15 i 02-kvalitetssikring). Fullt ICD-navn følger med i datafila.
KORT = {
    "_T": "Alle diagnoser", "I": "Infeksjonssykdommer", "II": "Svulster", "III": "Blod og immunsystem",
    "IV": "Hormoner, ernæring og stoffskifte", "V": "Psykiske lidelser", "VI": "Nervesystemet",
    "VII": "Øyet", "VIII": "Øret", "IX": "Hjerte og kar", "X": "Åndedrett", "XI": "Fordøyelse",
    "XII": "Hud", "XIII": "Muskler og skjelett", "XIV": "Urinveier og kjønnsorganer",
    "XV": "Svangerskap og fødsel", "XVI": "Tilstander rundt fødselen", "XVII": "Medfødte misdannelser",
    "XVIII": "Symptomer og funn", "XIX": "Skader og forgiftninger",
    "XXI": "Kontroller, oppfølging og annen kontakt", "zz1": "Annen",
}
MAAL = ["Pasient", "PasientPolikl", "PasientDognBeh", "KontaktPolikl", "DagBehandl", "DognOpphold", "OppholdDogn"]
MENGDE = ["KontaktPolikl", "DagBehandl", "DognOpphold", "OppholdDogn"]
ALDER_S = ["00-17", "18-29", "30-49", "50-66", "67-79", "80-89", "90+"]
GRENSER = {"00-17": (0, 17), "18-29": (18, 29), "30-49": (30, 49), "50-66": (50, 66),
           "67-79": (67, 79), "80-89": (80, 89), "90+": (90, 200)}


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
    if d.get("status"):
        feil(f"{navn}: har statusflagg {set(d['status'].values())}, som prototypen ikke håndterer")
    celler = {komb: d["value"][n] for n, komb in enumerate(itertools.product(*koder))}
    if any(v is None for v in celler.values()):
        feil(f"{navn}: har manglende verdier")
    etiketter = {dim: d["dimension"][dim]["category"].get("label", {}) for dim in d["id"]}
    return {"navn": navn, "celler": celler, "dims": d["id"], "koder": koder,
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


def spenn(kode):
    """«A00-B99» → ('A00', 'B99'). Strengsammenligning holder for ICD-koder (også T4n)."""
    a, _, b = kode.partition("-")
    return a, b or a


def main():
    sk = les("somatikk_kapittel")
    sb = les("somatikk_blokk")
    sr = les("somatikk_rate")
    ps = les("psykisk")
    pr = les("psykisk_rate")
    fm = les("folkemengde")

    T = koder(sk, "Tid")
    KAP = koder(sk, "Diagnose")
    ALDRE = koder(sk, "Alder")
    fast = dict(Region="0", Aktor="_T")

    # --- Somatikk per kapittel, kjønn, alder og mål ---
    s = {k: {kj: {al: {m: serie(sk, T, Kjonn=kj, Alder=al, Diagnose=k, ContentsCode=m, **fast) for m in MAAL}
                   for al in ALDRE} for kj in ("0", "1", "2")} for k in KAP}

    kapitler = [k for k in KAP if k not in ("_T", "zz1")]
    # D7 antall kapitler
    if len(kapitler) != 20:
        feil(f"D7: {len(kapitler)} kapitler, ventet 20")

    for i, _ in enumerate(T):
        for m in MENGDE:
            tot = s["_T"]["0"]["999A"][m][i]
            sm = sum(s[k]["0"]["999A"][m][i] for k in kapitler + ["zz1"])
            navn = "D2 dagbehandlinger" if m == "DagBehandl" else "D1 mengdetall over kapitler"
            avvik(navn, abs(sm - tot))
            if abs(sm - tot) > 36:
                feil(f"{navn[:2]}: {m} {T[i]} summerer til {sm}, totalen er {tot}")
    for k in KAP:
        for m in MAAL:
            for i, _ in enumerate(T):
                for al in ALDRE:
                    b, kv, mn = (s[k][kj][al][m][i] for kj in ("0", "2", "1"))
                    avvik("D3 kjønn", abs(kv + mn - b))
                    if abs(kv + mn - b) > (18 if m in MENGDE else 9):
                        feil(f"D3: {k} {m} {al} {T[i]}: {kv} + {mn} ≠ {b}")
                for kj in ("0", "1", "2"):
                    tot = s[k][kj]["999A"][m][i]
                    sm = sum(s[k][kj][al][m][i] for al in ALDER_S)
                    avvik("D4 alder", abs(sm - tot))
                    if abs(sm - tot) > (36 if m in MENGDE else 18):
                        feil(f"D4: {k} {m} kjønn {kj} {T[i]}: aldre {sm} ≠ {tot}")

    # --- Kategoriblokker ---
    kap_lab = sk["etiketter"]["Diagnose"]
    kap_spenn = {}
    for k in kapitler:
        m = re.match(r"\(([A-Z]\d\d)-([A-Z]\d\d)\)", kap_lab[k])
        if not m:
            feil(f"D5: finner ikke kodespenn i «{kap_lab[k]}»")
        kap_spenn[k] = (m.group(1), m.group(2))
    TB = koder(sb, "Tid")
    if TB != T:
        feil("somatikk_blokk har andre år enn somatikk_kapittel")
    b_lab = sb["etiketter"]["Diagnose"]
    blokker = []
    for kode in koder(sb, "Diagnose"):
        if kode in KAP:
            # kapitlene og totalen ligger også i blokkdatasettet: må være lik kapittelserien
            v = serie(sb, T, Region="0", Kjonn="0", Alder="999A", Aktor="_T", Diagnose=kode, ContentsCode="Pasient")
            if v != s[kode]["0"]["999A"]["Pasient"]:
                feil(f"D5: {kode} har ulike tall i de to utsnittene av 14824")
            continue
        a, _ = spenn(kode)
        eier = [k for k, (fra, til) in kap_spenn.items() if fra <= a <= til]
        if len(eier) != 1:
            feil(f"D5: blokk {kode} hører til {eier}")
        navn = re.sub(r"^\([^)]*\)\s*", "", b_lab[kode]).strip()
        blokker.append({"k": kode, "n": navn, "kap": eier[0],
                        "v": serie(sb, T, Region="0", Kjonn="0", Alder="999A", Aktor="_T",
                                   Diagnose=kode, ContentsCode="Pasient")})
    if len(blokker) != 200:
        feil(f"D7: {len(blokker)} blokker, ventet 200")
    for k in kapitler:
        egne = [b for b in blokker if b["kap"] == k]
        if not egne:
            feil(f"D5: kapittel {k} har ingen blokker")
        for i, _ in enumerate(T):
            storst = max(b["v"][i] for b in egne)
            if s[k]["0"]["999A"]["Pasient"][i] < storst:
                feil(f"D5: kapittel {k} {T[i]} er mindre enn største blokk")

    # --- Middelfolkemengde per aldersgruppe og år (07459) ---
    FA = koder(fm, "Alder")
    alder = lambda a: 105 if a.startswith("105") else int(a)
    mf = {}
    for al, (lo, hi) in GRENSER.items():
        mf[al] = [round(sum((hent(fm, Alder=a, ContentsCode="Personer1", Tid=t) +
                             hent(fm, Alder=a, ContentsCode="Personer1", Tid=str(int(t) + 1))) / 2
                            for a in FA if lo <= alder(a) <= hi)) for t in T]
    mf["999A"] = [sum(mf[al][i] for al in ALDER_S) for i in range(len(T))]

    # --- Rater, somatikk ---
    KAT = koder(sr, "InnvandrKat")
    rate = {k: {kj: {kat: {"u": serie(sr, T, Kjonn=kj, InnvandrKat=kat, Diagnose=k, ContentsCode="Pasient1000innb"),
                           "a": serie(sr, T, Kjonn=kj, InnvandrKat=kat, Diagnose=k, ContentsCode="Pasient1000alder")}
                     for kat in KAT} for kj in ("0", "1", "2")} for k in KAP}
    # D6 egen totalrate mot publisert
    for k in KAP:
        for i, _ in enumerate(T):
            egen = s[k]["0"]["999A"]["Pasient"][i] / mf["999A"][i] * 1000
            publ = rate[k]["0"]["A-G"]["u"][i]
            grense = 1.5 if k == "XV" else 0.55
            avvik("D6 rate XV" if k == "XV" else "D6 rate", round(abs(egen - publ), 2))
            if abs(egen - publ) > grense:
                feil(f"D6: {k} {T[i]} egen rate {egen:.2f}, publisert {publ}")

    # --- Psykisk helsevern for voksne ---
    PA = koder(ps, "Alder")
    PM = koder(ps, "ContentsCode")
    psyk = {kj: {al: {m: serie(ps, T, Region="0", Kjonn=kj, Alder=al, Aktor="_T", ContentsCode=m) for m in PM}
                 for al in PA} for kj in ("0", "1", "2")}
    for m in PM:
        for i, _ in enumerate(T):
            b, kv, mn = (psyk[kj]["Ialt"][m][i] for kj in ("0", "2", "1"))
            avvik("D3 kjønn", abs(kv + mn - b))
            if abs(kv + mn - b) > (18 if m in ("OppholdDogn", "KontaktPolikl") else 9):
                feil(f"D3: psykisk {m} {T[i]}")
    PKAT = koder(pr, "InnvandrKat")
    prate = {kj: {kat: {"u": serie(pr, T, Kjonn=kj, InnvandrKat=kat, ContentsCode="Pasient1000innb"),
                        "a": serie(pr, T, Kjonn=kj, InnvandrKat=kat, ContentsCode="Pasient1000alder")}
                  for kat in PKAT} for kj in ("0", "1", "2")}

    hentet = json.loads((RAW / "_hentet.json").read_text(encoding="utf8"))["hentet"]
    ut = {
        "hentet": hentet,
        "oppdatert": {"14824": sk["oppdatert"], "14827": sr["oppdatert"], "14820": ps["oppdatert"],
                      "14823": pr["oppdatert"], "07459": fm["oppdatert"]},
        "aar": T,
        "kap": [{"k": k, "n": KORT[k], "full": re.sub(r"^\([^)]*\)\s*", "", kap_lab[k]) if k != "_T" else "I alt",
                 "kode": "{}–{}".format(*kap_spenn[k]) if k in kap_spenn else ""} for k in KAP],
        "maal": MAAL,
        "alder": [{"k": a, "n": sk["etiketter"]["Alder"][a]} for a in ALDRE],
        "s": s, "blokker": blokker, "mf": mf,
        "kat": [{"k": k, "n": sr["etiketter"]["InnvandrKat"][k]} for k in KAT], "rate": rate,
        "palder": [{"k": a, "n": ps["etiketter"]["Alder"][a]} for a in PA], "pmaal": PM,
        "psyk": psyk, "prate": prate,
    }
    UT.parent.mkdir(exist_ok=True)
    UT.write_text(json.dumps(ut, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(f"build/pasient.json: {round(UT.stat().st_size / 1024)} kB, {len(kapitler)} kapitler, "
          f"{len(blokker)} blokker, {len(T)} år. Største avvik: "
          + ", ".join(f"{k} {v}" for k, v in AVVIK.items()))


if __name__ == "__main__":
    main()

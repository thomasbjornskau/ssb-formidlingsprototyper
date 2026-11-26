"""Lager build/sykefratot.json fra rådata i data/raw/ og kontrollerer tallene.

Kjøres av felles/bygg.py. Stopper med «Kontroll feilet: …» hvis en kontroll ikke går opp.
Kontrollene er de samme som K1–K7 i docs/03-kildekart.md:

- B1 (K1) egenmeldt + legemeldt = i alt. Sesongjustert: toleranse 0,015 (største avvik 0,01, to desimaler).
         Ikke sesongjustert: toleranse 0,1 (én desimal, største avvik 0,1).
- B2 (K2) menn + kvinner = begge kjønn, sykefraværsdagsverk ujustert og sesongjustert.
         Toleranse 100 dagsverk (tallene er avrundet til hundre, største avvik 100).
- B3 (K4) Navs tall for 3. kvartal 2025 gjenskapes: legemeldt ujustert 4,8 prosent, −6,3 prosent fra året før.
- B4 (K5) dagsverk i alt i 12946 = dagsverk i 12439. Toleranse 100. Kjent avvik: 2024K2 (6 400 dagsverk),
         ført som hull 1 i kildekartet og spørsmål til fag.
- B5 (K6) varighet: egenmeldt + legemeldt = i alt, og varighetsgruppene summerer til legemeldt.
         Tilfeller: toleranse 0 for begge kjønn, 1 mellom kjønn. Dagsverk: toleranse 200 (avrunding).
- B6 (K7) andeler regnet fra antall = publiserte prosentandeler i 12946. Toleranse 0,1 (én desimal).
- B7 alle koder i data/synonymer.json finnes i 12452.
- B8 strukturen er som talt i steg 3: 407 yrkeskoder på 4-siffernivå og 357 kommuner med tall i alle kvartaler.
- B9 tallene i toppgrafikken er de samme som i steg 2, så lenge siste kvartal er det samme.

Endringsrater brukes slik de er publisert (K3: regnet fra nivåer avviker de i 54 av 104 kvartaler).
Bare standardbiblioteket.
"""
import itertools
import json
import pathlib
import sys

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "sykefratot.json"
KJONN = {"0": "begge", "2": "kvinner", "1": "menn"}
TYPER = {"Alt": "alt", "E": "egen", "L": "lege"}
KJENTE_AVVIK_B4 = {"2024K2"}
EPS = 1e-9
AVVIK = {}
# Fylkesnavn for kommunenumrene (Klass 104, inndeling fra 2024). Brukes bare til visning i søket.
FYLKER = {"03": "Oslo", "11": "Rogaland", "15": "Møre og Romsdal", "18": "Nordland", "31": "Østfold",
          "32": "Akershus", "33": "Buskerud", "34": "Innlandet", "39": "Vestfold", "40": "Telemark",
          "42": "Agder", "46": "Vestland", "50": "Trøndelag", "55": "Troms", "56": "Finnmark"}


def feil(tekst):
    sys.exit(f"Kontroll feilet: {tekst}")


def avvik(navn, v):
    AVVIK[navn] = max(AVVIK.get(navn, 0), abs(v))


def les(navn):
    """Leser et json-stat2-svar. Siste dimensjon varierer raskest. Statussymbol beholdes for seg."""
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
        s = status.get(str(n))
        celler[komb] = None if s in (":", ".", "..") else d["value"][n]
        if s:
            symbol[komb] = s
    etiketter = {dim: d["dimension"][dim]["category"].get("label", {}) for dim in d["id"]}
    return {"navn": navn, "celler": celler, "symbol": symbol, "dims": d["id"], "koder": koder,
            "etiketter": etiketter, "oppdatert": d.get("updated", "")[:10]}


def nokkel(t, fast):
    return tuple(str(fast[dim]) for dim in t["dims"])


def hent(t, **fast):
    k = nokkel(t, fast)
    if k not in t["celler"]:
        feil(f"{t['navn']}: finnes ikke: {fast}")
    return t["celler"][k]


def sym(t, **fast):
    return t["symbol"].get(nokkel(t, fast))


def koder(t, dim):
    return t["koder"][t["dims"].index(dim)]


def dato(iso):
    return f"{iso[8:10]}.{iso[5:7]}.{iso[:4]}" if iso else ""


def forelder(k):
    """Overordnet kode i yrkeshierarkiet i 12452."""
    if k == "0-9":
        return None
    if len(k) == 1 or k in ("3_01-03", "0b"):
        return "0-9"
    if len(k) == 2:
        if k == "00":
            return "0b"
        if k[0] in "03":
            return "3_01-03"
        return k[0]
    return k[:-1]


def niva(k):
    if k == "0-9":
        return 0
    if len(k) == 1 or k in ("3_01-03", "0b"):
        return 1
    return len(k)


def main():
    H, V, P = les("hoved"), les("varighet"), les("personer")
    Y, YE, K = les("yrke"), les("yrke_endring"), les("kommune")
    tid = koder(H, "Tid")
    tidV = koder(V, "Tid")

    # ---------- B1 egenmeldt + legemeldt = i alt ----------
    for k in KJONN:
        for t in tid:
            for c, tol in (("SykefravProsSesJust", 0.015), ("SykefravProsent", 0.1)):
                e, l, a = (hent(H, Kjonn=k, Sykefraver2=x, ContentsCode=c, Tid=t) for x in ("E", "L", "Alt"))
                avvik("B1 " + c, e + l - a)
                if abs(e + l - a) > tol + EPS:
                    feil(f"B1 {c} {k} {t}: {e} + {l} ≠ {a}")

    # ---------- B2 menn + kvinner = begge, dagsverk ----------
    for c in ("DagsverkIkkeSesJust", "DagsverkSesJust"):
        for typ in TYPER:
            for t in tid:
                b = hent(H, Kjonn="0", Sykefraver2=typ, ContentsCode=c, Tid=t)
                if b is None:
                    continue
                m = hent(H, Kjonn="1", Sykefraver2=typ, ContentsCode=c, Tid=t)
                w = hent(H, Kjonn="2", Sykefraver2=typ, ContentsCode=c, Tid=t)
                avvik("B2 dagsverk", m + w - b)
                if abs(m + w - b) > 100:
                    feil(f"B2 {c} {typ} {t}: {m} + {w} ≠ {b}")

    # ---------- B3 Navs tall for 2025K3 ----------
    if (hent(H, Kjonn="0", Sykefraver2="L", ContentsCode="SykefravProsent", Tid="2025K3"),
            hent(H, Kjonn="0", Sykefraver2="L", ContentsCode="ProsentvisEndring", Tid="2025K3")) != (4.8, -6.3):
        feil("B3 Navs tall for 3. kvartal 2025 (4,8 prosent, −6,3 prosent) gjenskapes ikke")

    # ---------- B4 dagsverk i 12946 = 12439 ----------
    for t in tidV:
        a = hent(V, Kjonn="0", VarighetTypeSyk="F0", ContentsCode="Dagsverk", Tid=t)
        b = hent(H, Kjonn="0", Sykefraver2="Alt", ContentsCode="DagsverkIkkeSesJust", Tid=t)
        if t in KJENTE_AVVIK_B4:
            continue
        avvik("B4 dagsverk 12946/12439", a - b)
        if abs(a - b) > 100:
            feil(f"B4 {t}: 12946 har {a}, 12439 har {b}")

    # ---------- B5 og B6 varighet ----------
    F = [f"F{i}" for i in range(8)]
    for k in KJONN:
        for t in tidV:
            for c, tol in (("Tilfeller", 0), ("Dagsverk", 200)):
                g = {f: hent(V, Kjonn=k, VarighetTypeSyk=f, ContentsCode=c, Tid=t) for f in F}
                d1 = g["F1"] + g["F2"] - g["F0"]
                d2 = sum(g[f] for f in F[3:]) - g["F2"]
                avvik(f"B5 {c}", max(abs(d1), abs(d2)))
                if max(abs(d1), abs(d2)) > tol:
                    feil(f"B5 {c} {k} {t}: summene går ikke opp ({d1}, {d2})")
                for f in F[1:]:
                    p = hent(V, Kjonn=k, VarighetTypeSyk=f, ContentsCode=c + "Pros" if c == "Tilfeller" else "DagsverkPros", Tid=t)
                    r = round(100 * g[f] / g["F0"], 1)
                    avvik("B6 andeler", r - p)
                    if abs(r - p) > 0.1 + EPS:
                        feil(f"B6 {c} {f} {k} {t}: regnet {r}, publisert {p}")
    for t in tidV:
        for f in F:
            m, w, b = (hent(V, Kjonn=x, VarighetTypeSyk=f, ContentsCode="Tilfeller", Tid=t) for x in ("1", "2", "0"))
            avvik("B5 tilfeller kjønn", m + w - b)
            if abs(m + w - b) > 1:
                feil(f"B5 tilfeller kjønn {f} {t}")

    # ---------- yrke ----------
    ykoder = koder(Y, "Yrke")
    ylab = Y["etiketter"]["Yrke"]
    tidY = koder(Y, "Tid")
    syn = json.loads((MAPPE / "data" / "synonymer.json").read_text(encoding="utf8"))
    for o, ks in syn["ord"].items():
        for k in ks:
            if k not in ylab:
                feil(f"B7 synonymet «{o}» peker på {k}, som ikke finnes i 12452")
    for o in syn["usikker"]:
        if o not in syn["ord"]:
            feil(f"B7 «{o}» står som usikker, men finnes ikke i ordlisten")
    if sum(1 for k in ykoder if len(k) == 4) != 407:
        feil("B8 antall yrkeskoder på 4-siffernivå er ikke 407")
    yrker = []
    for k in ykoder:
        f = forelder(k)
        if f is not None and f not in ylab:
            feil(f"yrkeskoden {k} har ingen forelder ({f})")
        yrker.append([k, ylab[k], niva(k), f])
    yverdi, ysym, yendr = {}, {}, {}
    for kk, kn in KJONN.items():
        yverdi[kn] = {k: [hent(Y, Kjonn=kk, Yrke=k, ContentsCode="Sykefraversprosent", Tid=t) for t in tidY] for k in ykoder}
        ysym[kn] = {k: s for k in ykoder if (s := sym(Y, Kjonn=kk, Yrke=k, ContentsCode="Sykefraversprosent", Tid=tidY[-1]))}
        yendr[kn] = {k: hent(YE, Kjonn=kk, Yrke=k, ContentsCode="SykefraversprosEndr", Tid=tidY[-1]) for k in ykoder}
    if koder(YE, "Tid") != [tidY[-1]]:
        feil("yrke_endring gjelder ikke siste kvartal i yrkesserien")

    # ---------- kommune ----------
    tidK = koder(K, "Tid")
    klab = K["etiketter"]["Region"]
    kommuner = {}
    for k in koder(K, "Region"):
        if len(k) != 4 or k == "9999":
            continue
        s = [hent(K, Region=k, Kjonn="0", ContentsCode="Sykefraversprosent", Tid=t) for t in tidK]
        if s[-1] is None:
            continue
        if None in s:
            feil(f"B8 kommunen {k} mangler tall i deler av perioden")
        if k[:2] not in FYLKER:
            feil(f"kommunen {k} har ukjent fylkesnummer")
        kommuner[k] = {"navn": klab[k], "fylke": FYLKER[k[:2]], "pros": s,
                       "endr": [hent(K, Region=k, Kjonn="0", ContentsCode="SykefraversprosEndr", Tid=t) for t in tidK]}
    if len(kommuner) != 357:
        feil(f"B8 {len(kommuner)} kommuner med tall, ventet 357")

    # ---------- B9 toppgrafikken fra steg 2 ----------
    g = json.loads((MAPPE / "data" / "grafikk-utkast.json").read_text(encoding="utf8"))
    if g["siste"]["periode"] == tid[-1]:
        for felt, typ, c in (("sesongjustert", "Alt", "SykefravProsSesJust"), ("ujustert", "Alt", "SykefravProsent"),
                             ("egenmeldt_sj", "E", "SykefravProsSesJust"), ("legemeldt_sj", "L", "SykefravProsSesJust")):
            if g["siste"][felt] != hent(H, Kjonn="0", Sykefraver2=typ, ContentsCode=c, Tid=tid[-1]):
                feil(f"B9 {felt} i toppgrafikken avviker fra rådataene")

    # ---------- datafilen ----------
    def serie(kk, typ, c):
        return [hent(H, Kjonn=kk, Sykefraver2=typ, ContentsCode=c, Tid=t) for t in tid]
    hoved = {kn: {TYPER[typ]: {"sj": serie(kk, typ, "SykefravProsSesJust"), "uj": serie(kk, typ, "SykefravProsent"),
                               "si": serie(kk, typ, "SykefravProsSesInflu"), "endr_sj": serie(kk, typ, "EndringSesJust"),
                               "endr_aar": serie(kk, typ, "ProsentvisEndring"), "pp_aar": serie(kk, typ, "ProsentpoengEndr"),
                               "dv_uj": serie(kk, typ, "DagsverkIkkeSesJust"), "dv_sj": serie(kk, typ, "DagsverkSesJust")}
                  for typ in TYPER} for kk, kn in KJONN.items()}
    varighet = {kn: {c: {f: [hent(V, Kjonn=kk, VarighetTypeSyk=f, ContentsCode=c, Tid=t) for t in tidV] for f in F}
                     for c in ("Dagsverk", "Tilfeller")} for kk, kn in KJONN.items()}
    tidP = koder(P, "Tid")
    personer = {kn: {c: [hent(P, Region="0", Kjonn=kk, Alder="16-69", ContentsCode=c, Tid=t) for t in tidP]
                     for c in ("Sykefraversprosent", "ArbeidstakereSykePro", "ArbeidstakereSykefra")} for kk, kn in KJONN.items()}
    data = {
        "oppdatert": {"12439": dato(H["oppdatert"]), "12946": dato(V["oppdatert"]), "12446": dato(P["oppdatert"]),
                      "12452": dato(Y["oppdatert"]), "12451": dato(K["oppdatert"])},
        "hentet": json.loads((RAW / "_hentet.json").read_text(encoding="utf8"))["hoved"]["hentet"][:10],
        "tid": tid, "hoved": hoved,
        "tidV": tidV, "varighet": varighet,
        "tidP": tidP, "personer": personer,
        "tidY": tidY, "yrker": yrker, "yverdi": yverdi, "ysym": ysym, "yendr": yendr,
        "synonymer": syn["ord"], "usikre_synonymer": syn["usikker"],
        "tidK": tidK, "kommuner": kommuner,
    }
    UT.parent.mkdir(exist_ok=True)
    UT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True), encoding="utf8")
    print("Kontroller OK: " + "; ".join(f"{k} {round(v, 3) if isinstance(v, float) else v}" for k, v in sorted(AVVIK.items())))
    print(f"Kjent avvik holdt utenfor B4: {', '.join(sorted(KJENTE_AVVIK_B4))}")
    print(f"{UT.relative_to(MAPPE)}: {round(UT.stat().st_size / 1024)} kB")


if __name__ == "__main__":
    main()

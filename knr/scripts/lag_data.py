"""Lager build/knr.json fra rådata i data/raw/ og kontrollerer summene.

Kjøres av felles/bygg.py. Stopper med «Kontroll feilet: …» hvis en kontroll ikke går opp.
Kontrollene er de samme som i kildekartet (K1–K11). Bare standardbiblioteket.
"""
import itertools
import json
import pathlib
import sys

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "knr.json"

# Hovedrevisjonen 2025, BNP-størrelser for 2022, milliarder kroner, løpende priser.
# Kilde: SSB, «Hovedrevisjonen av nasjonalregnskapet», 13.11.2025 (01-innsikt.md, [K4]). Ikke i statistikkbanken.
HOVEDREVISJON = {
    "kilde": "SSB, «Hovedrevisjonen av nasjonalregnskapet», 13.11.2025",
    "aar": 2022,
    "rader": [["BNP", 5733, 5935], ["BNP Fastlands-Norge", 3679, 3865], ["Konsum i husholdninger og ideelle org.", 1857, 2026],
              ["Konsum i offentlig forvaltning", 1035, 1046], ["Bruttoinvestering i fast realkapital", 1053, 1159], ["Eksport", 3182, 3180], ["Import", 1554, 1563]],
}


def feil(tekst):
    sys.exit(f"Kontroll feilet: {tekst}")


def les(navn):
    d = json.loads((RAW / f"{navn}.json").read_text(encoding="utf8"))
    koder = []
    for dim in d["id"]:
        idx = d["dimension"][dim]["category"]["index"]
        koder.append(sorted(idx, key=idx.get) if isinstance(idx, dict) else list(idx))
    if [len(k) for k in koder] != d["size"]:
        feil(f"{navn}: dimensjonene stemmer ikke med size")
    v = d["value"]
    celler = {k: (v.get(str(n)) if isinstance(v, dict) else v[n]) for n, k in enumerate(itertools.product(*koder))}
    return {"navn": navn, "c": celler, "dims": d["id"], "koder": koder,
            "lab": {dim: d["dimension"][dim]["category"].get("label", {}) for dim in d["id"]}, "oppdatert": d.get("updated", "")[:10]}


def serie(t, fast, tid):
    """Liste av verdier over tid. fast = koder for de andre dimensjonene i rekkefølge."""
    return [t["c"][tuple(fast) + (x,)] for x in tid]


def main():
    ma, mk, mn, na, nk = (les(n) for n in ("makro_aar", "makro_kvartal", "maaned", "naering_aar", "naering_kvartal"))
    hentet = json.loads((RAW / "_hentet.json").read_text(encoding="utf8"))["hentet"]
    aar, kv, mnd = ma["koder"][2], mk["koder"][2], mn["koder"][2]
    M = ma["koder"][0]
    A = lambda m, c, y: ma["c"][(m, c, y)]

    # K1–K3: regnskapet går opp i løpende priser
    k1 = max(abs(A("koh.nrpriv", "Priser", y) + A("koo.nroff", "Priser", y) + A("bif.nr8_", "Priser", y) + A("eks.nrtot", "Priser", y)
                 - A("imp.nrtot", "Priser", y) - A("bnpb.nr23_9", "Priser", y)) for y in aar)
    if k1 > 15:  # avrunding i millioner gir inntil 11 (kildekartet K1)
        feil(f"anvendelsen summerer ikke til BNP (avvik {k1})")
    for y in aar:
        if A("bnpb.nr23_6fn", "Priser", y) + A("bnpb.nr23oljsj", "Priser", y) + A("bnpb.nr29korr", "Priser", y) != A("bnpb.nr23_9", "Priser", y):
            feil(f"produksjonssiden summerer ikke til BNP i {y}")
        if A("bnpb.nr23_9fn", "Priser", y) + A("bnpb.nr23oljsj", "Priser", y) != A("bnpb.nr23_9", "Priser", y):
            feil(f"Fastlands-BNP + olje og sjøfart ≠ BNP i {y}")
    # K4: årlig volum fra faste priser = publisert, for hovedstørrelsene
    for m in ("bnpb.nr23_9", "bnpb.nr23_9fn", "koh.nrpriv", "eks.nrtot"):
        for i in range(1, len(aar)):
            r = round(100 * (A(m, "Faste", aar[i]) / A(m, "Faste", aar[i - 1]) - 1), 1)
            if abs(r - A(m, "Volum", aar[i])) > 0.05:
                feil(f"volumvekst for {m} {aar[i]} regnet {r}, publisert {A(m, 'Volum', aar[i])}")
    # K4b: årlig volum fra faste priser for alle størrelser. Avvik over 0,15 prosentpoeng tillates bare
    # for små serier (nivå under 50 milliarder), der avrunding i millioner gir store utslag (kildekartet K4).
    stor_avvik = []
    for m in M:
        for i in range(1, len(aar)):
            f0, f1, p = A(m, "Faste", aar[i - 1]), A(m, "Faste", aar[i]), A(m, "Volum", aar[i])
            if None in (f0, f1, p) or f0 <= 0 or f1 <= 0:
                continue
            r = 100 * (f1 / f0 - 1)
            if abs(r - p) > 0.15 and min(f0, f1) >= 50000:
                stor_avvik.append((m, aar[i], round(r, 2), p))
    if stor_avvik:
        feil(f"volumvekst regnet fra faste priser avviker fra publisert: {stor_avvik[:3]}")
    # K5: kvartalsvekst for BNP og Fastlands-BNP fra sesongjusterte nivåer = publisert
    Q = lambda m, c, t: mk["c"][(m, c, t)]
    for m in ("bnpb.nr23_9", "bnpb.nr23_9fn"):
        for i in range(1, len(kv)):
            r = round(100 * (Q(m, "FastePriserSesJust", kv[i]) / Q(m, "FastePriserSesJust", kv[i - 1]) - 1), 1)
            if abs(r - Q(m, "VolumEndrSesJust", kv[i])) > 0.05:
                feil(f"kvartalsvekst {m} {kv[i]} regnet {r}, publisert {Q(m, 'VolumEndrSesJust', kv[i])}")
    # K6: kvartaler summerer til året (ujustert)
    k6 = 0
    for m in ("bnpb.nr23_9", "bnpb.nr23_9fn", "koh.nrpriv"):
        for y in aar:
            if int(y) < 1978:
                continue
            for c in ("Priser", "Faste"):
                k6 = max(k6, abs(sum(Q(m, c, f"{y}K{n}") for n in range(1, 5)) - A(m, c, y)))
    if k6 > 8:  # avrunding i millioner: høyst 6 over 1978–2025 (BNP 2012). Kildekartet K6 testet bare tre år
        feil(f"kvartalene summerer ikke til året (avvik {k6})")
    # K9: tremånederssum = kvartalsvekst
    MN = lambda m, c, t: mn["c"][(m, c, t)]
    for m in ("bnpb.nr23_9", "bnpb.nr23_9fn"):
        for t in kv:
            if int(t[:4]) < 2016 or (t[:4] == "2016" and t[-1] == "1"):
                continue
            mm = f"{t[:4]}M{int(t[-1]) * 3:02d}"
            if mm in mnd and abs(MN(m, "VolumEndrRull3md", mm) - Q(m, "VolumEndrSesJust", t)) > 0.15:
                feil(f"tremånederssum {mm} ≠ kvartalsvekst {t} for {m}")
    # K10–K11: næringer
    NA = lambda c, k, y: na["c"][(c, k, y)]
    nlab = na["lab"]["NACE"]
    topp = [c for c in na["koder"][0] if not nlab[c].startswith("¬") and c not in ("nr23_6", "nr23_6fn")]
    for y in aar:
        if abs(sum(NA(c, "BNPB", y) for c in topp) - NA("nr23_6", "BNPB", y)) > 5:
            feil(f"næringene summerer ikke til totalen i {y}")
        if NA("nr23_6", "BNPB", y) - NA("pub2X06", "BNPB", y) - NA("pub2X49B", "BNPB", y) - NA("pub2X50A", "BNPB", y) != NA("nr23_6fn", "BNPB", y):
            feil(f"Fastlands-Norge i næringstabellen går ikke opp i {y}")
        if NA("nr23_6fn", "BNPB", y) != A("bnpb.nr23_6fn", "Priser", y):
            feil(f"bruttoprodukt Fastlands-Norge ulikt i 09170 og 09189 i {y}")
    # Nøkkeltall
    if A("bnpb.nr23_9", "Priser", "2025") != 5511334 or Q("bnpb.nr23_9fn", "VolumEndrSesJust", "2026K2") != 0.3:
        feil("nøkkeltallene er ikke de publiserte")

    mlab = ma["lab"]["Makrost"]
    makro = [[m, mlab[m].lstrip("¬ ").strip(), mlab[m].count("¬")] for m in M]
    syn = json.loads((MAPPE / "data" / "synonymer.json").read_text(encoding="utf8"))["synonymer"]
    for s in syn:
        if any(k not in M for k in s["koder"]):
            feil(f"synonymet {s['ord']} peker på en kode som ikke finnes")
    nk_lab = nk["lab"]["NACE"]
    ut = {
        "kilde": {"hentet": hentet, "oppdatert": {t["navn"]: t["oppdatert"] for t in (ma, mk, mn, na, nk)}},
        "aar": [int(y) for y in aar], "kvartaler": kv, "maaneder": mnd,
        "makro": makro,
        "A": {m: [serie(ma, (m, c), aar) for c in ("Priser", "Faste", "Volum", "Endringer")] for m in M},
        "Q": {m: [serie(mk, (m, c), kv) for c in ("Priser", "Faste", "FastePriserSesJust", "Volum", "VolumEndrSesJust")] for m in M},
        "Mnd": {m: [serie(mn, (m, c), mnd) for c in ("VolumEndrSesJust", "VolumEndrRull3md")] for m in mn["koder"][0]},
        "naering": [[c, nlab[c].lstrip("¬ ").strip(), nlab[c].count("¬")] for c in na["koder"][0]],
        "NA": {c: [serie(na, (c, k), aar) for k in ("BNPB", "BNPB4")] for c in na["koder"][0]},
        "naeringKv": [[c, nk_lab[c].lstrip("¬ ").strip(), nk_lab[c].count("¬")] for c in nk["koder"][0]],
        "NQ": {c: [serie(nk, (c, k), kv) for k in ("BNPB", "BNPB4", "BNPB4sesjust")] for c in nk["koder"][0]},
        "synonymer": syn, "hovedrevisjon": HOVEDREVISJON,
    }
    UT.parent.mkdir(exist_ok=True)
    UT.write_text(json.dumps(ut, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(f"  {UT.relative_to(MAPPE)}: {round(UT.stat().st_size / 1024)} kB · K1 avvik {k1} · K6 avvik {k6} · {len(M)} størrelser, "
          f"{len(kv)} kvartaler, {len(na['koder'][0])} næringer")


if __name__ == "__main__":
    main()

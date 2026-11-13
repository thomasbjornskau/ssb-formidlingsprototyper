"""Lager build/likekom.json fra rådata i data/raw/ og kontrollerer tallene.

Kjøres av felles/bygg.py. Stopper med feil hvis en kontroll ikke går opp:
- begge tabellene har de samme 17 årene og ingen manglende verdier
- fordelingene (kvinner + menn) summerer til 100 prosent
- skåren kan gjenskapes fra grunnlagstallene med metoden i Om statistikken
- næringsstruktur og utdanningsprogram er like i de to tabellene

Prototypen viser publisert skår, ikke skår regnet fra grunnlagstallene.
"""
import itertools
import json
import pathlib
import sys

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "likekom.json"

# kode i 09292, kortnavn, SSBs navn, gruppe, type, (kvinner, menn) eller andel i 09293
IND = [
    ("Barnehage", "Barnehage", 0, "andel", "Barnehage"),
    ("UtdanningVGS", "Utdanningsprogram", 0, "skar", "UtdanningVGS"),
    ("Naringsstruktur", "Næringsstruktur", 0, "skar", "Naringsstruktur"),
    ("OffentligSektor", "Offentlig sektor", 0, "fordeling", ("KvinnerOffentligSyss", "MennOffentligSyss")),
    ("PrivatSektor", "Privat sektor", 0, "fordeling", ("KvinnerPrivatSyss", "MennPrivatSyss")),
    ("Arbeid", "Arbeidsstyrke", 1, "forhold", ("KvinnerTjueSekstisek", "MennTjueSekstiseks")),
    ("Deltidsarbeid", "Deltid", 1, "forhold", ("KvinnerDeltid", "MennDeltid")),
    ("Fedrekvote", "Fedrekvote", 1, "andel", "Fedrekvote"),
    ("UtdNiva", "Utdanningsnivå", 2, "forhold", ("UtdKvinner", "UtdMenn")),
    ("Ledere", "Ledere", 2, "fordeling", ("KvinnerLedere", "MennLedere")),
    ("KomRepresentant", "Kommunestyre", 3, "fordeling", ("KomRepresentant", "KomReprMenn")),
    ("InntektBrutto", "Inntekt", 4, "forhold", ("BruttoKvinner", "BruttoMenn")),
]
GRUPPER = ["Rammer", "Arbeid og omsorg", "Ressurser", "Politikk", "Penger"]
ENHET = {"InntektBrutto": "kr"}
# Første år etter bruddet. Fedrekvote og deltid etter Om statistikken. For arbeidsstyrke oppgir
# Om statistikken 2017, men grunnlagstallene hopper i 2015 (a-ordningen). Står på kvalitetssikringslisten.
BRUDD = {"Fedrekvote": 2013, "Deltidsarbeid": 2015, "Arbeid": 2015}
# Kjente avvik mellom de to tabellene, funnet 13.11.2026 og ført på kvalitetssikringslisten.
# Bygget stopper hvis det kommer nye avvik, eller hvis et kjent avvik forsvinner.
KJENTE_AVVIK = {("KomRepresentant", "2010")}  # 38,2 prosent kvinner gir 0,76, publisert skår er 0,75 som i 2008–2009

HVA = {
    "Barnehage": "Andel barn 1–5 år i barnehage",
    "UtdanningVGS": "Hvor kjønnsbalanserte utdanningsprogram elevene i videregående velger",
    "Naringsstruktur": "Hvor kjønnsbalanserte næringene de sysselsatte jobber i, er",
    "OffentligSektor": "Kvinner og menn blant sysselsatte i offentlig sektor",
    "PrivatSektor": "Kvinner og menn blant sysselsatte i privat sektor",
    "Arbeid": "Andel kvinner og menn 20–66 år i arbeidsstyrken",
    "Deltidsarbeid": "Andel sysselsatte kvinner og menn 20–66 år som jobber deltid",
    "Fedrekvote": "Andel fedre som tar hele fedrekvoten eller mer",
    "UtdNiva": "Andel kvinner og menn med høyere utdanning",
    "Ledere": "Kvinner og menn blant ledere 20–66 år",
    "KomRepresentant": "Kvinner og menn blant kommunestyrerepresentantene",
    "InntektBrutto": "Gjennomsnittlig bruttoinntekt for kvinner og menn",
}


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
    celler = {k: (verdier.get(str(n)) if isinstance(verdier, dict) else verdier[n])
              for n, k in enumerate(itertools.product(*koder))}
    if d.get("status"):
        feil(f"{navn}: svaret har statussymboler, og de er ikke håndtert: {sorted(set(d['status'].values()))}")
    return {"celler": celler, "dims": d["id"], "koder": koder,
            "etiketter": d["dimension"]["ContentsCode"]["category"]["label"], "oppdatert": d.get("updated", "")[:10]}


def serie(t, kode, aar):
    ut = [t["celler"].get(("0", kode, a)) for a in aar]
    if any(v is None for v in ut):
        feil(f"{kode}: tall mangler for {[a for a, v in zip(aar, ut) if v is None]}")
    return ut


def main():
    s, g = les("skar"), les("grunnlag")
    aar = s["koder"][s["dims"].index("Tid")]
    if aar != g["koder"][g["dims"].index("Tid")]:
        feil("de to tabellene har ulike år")
    if len(aar) != int(aar[-1]) - int(aar[0]) + 1:
        feil("det mangler år i serien")
    if len(s["koder"][1]) != 12:
        feil(f"ventet 12 indikatorer i 09292, fant {len(s['koder'][1])}")

    ind, storst, hvor, avvik = [], 0.0, "", set()
    for kode, navn, gruppe, typ, gk in IND:
        sk = serie(s, kode, aar)
        post = {"kode": kode, "navn": navn, "ssbnavn": s["etiketter"][kode], "hva": HVA[kode], "gruppe": gruppe,
                "type": typ, "skar": sk, "brudd": BRUDD.get(kode), "enhet": ENHET.get(kode, "%")}
        if typ in ("fordeling", "forhold"):
            kv, mn = serie(g, gk[0], aar), serie(g, gk[1], aar)
            post["kv"], post["menn"] = kv, mn
            for a, k, m, p in zip(aar, kv, mn, sk):
                if typ == "fordeling":
                    # Andelene er avrundet til én desimal hver for seg.
                    if abs(k + m - 100) > 0.11:
                        feil(f"{navn} {a}: kvinner + menn = {k + m}, ikke 100")
                    r = min(k, m) / 50
                else:
                    r = min(k / m, m / k)
                # Toleranse 0,011: skåren er publisert med to desimaler og grunnlagstallene er avrundet.
                # Største faktiske avvik skrives ut under.
                if abs(r - p) > 0.011:
                    avvik.add((kode, a)); print(f"  avvik: {navn} {a}: skår fra grunnlagstall {r:.3f}, publisert {p}")
                elif abs(r - p) > storst:
                    storst, hvor = abs(r - p), f"{navn} {a}"
        elif typ == "andel":
            an = serie(g, gk, aar)
            post["andel"] = an
            for a, v, p in zip(aar, an, sk):
                if abs(v / 100 - p) > 0.011:
                    avvik.add((kode, a)); print(f"  avvik: {navn} {a}: andel {v} prosent, publisert skår {p}")
                elif abs(v / 100 - p) > storst:
                    storst, hvor = abs(v / 100 - p), f"{navn} {a}"
        else:
            # Skåren står i begge tabellene. I 09293 mangler andre desimal i noen år.
            for a, v, p in zip(aar, serie(g, gk, aar), sk):
                if abs(v - p) > 0.011:
                    avvik.add((kode, a)); print(f"  avvik: {navn} {a}: {v} i 09293, {p} i 09292")
        ind.append(post)

    if avvik != KJENTE_AVVIK:
        feil(f"avvikene mellom 09292 og 09293 er endret. Nye: {sorted(avvik - KJENTE_AVVIK)}. Borte: {sorted(KJENTE_AVVIK - avvik)}")

    hentet = json.loads((RAW / "_hentet.json").read_text(encoding="utf8"))["hentet"]
    ut = {"aar": [int(a) for a in aar], "grupper": GRUPPER, "ind": ind,
          "avvik": sorted(f"{k} {a}" for k, a in avvik), "oppdatert": {"09292": s["oppdatert"], "09293": g["oppdatert"]}, "hentet": hentet}
    UT.parent.mkdir(exist_ok=True)
    UT.write_text(json.dumps(ut, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(f"likekom: {len(ind)} indikatorer, {len(aar)} år ({aar[0]}–{aar[-1]}). "
          f"Største avvik mellom publisert skår og skår fra grunnlagstall: {storst:.4f} ({hvor}).")


if __name__ == "__main__":
    main()

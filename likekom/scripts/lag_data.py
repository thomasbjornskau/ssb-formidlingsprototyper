"""Lager build/likekom.json fra rådata i data/raw/ og kontrollerer tallene.

Kjøres av felles/bygg.py. Stopper med feil hvis en kontroll ikke går opp:
- begge tabellene har de samme 17 årene, og bare statussymbolene «.» og «..»
- det er 357 kommuner og 15 fylker med tall siste år, og alle kommunene finnes i kartet
- fordelingene (kvinner + menn) summerer til 100 prosent
- skåren kan gjenskapes fra grunnlagstallene med metoden i Om statistikken
- landstallene har ingen hull

Tidsserier for kommuner og fylker lenkes bakover gjennom nummerendringer med Klass.
En serie lenkes bare når endringen er ren omnummerering: én gammel kode til én ny.
Ved sammenslåing eller deling stopper serien, og tidligere år blir tomme.

Prototypen viser publisert skår, ikke skår regnet fra grunnlagstallene.
"""
import collections
import json
import pathlib
import sys

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "likekom.json"

# De seks dimensjonene er SSBs (Notater 2009/65 og Om statistikken). Kortnavnene er prototypens.
DIM = ["Tilrettelegging", "Næring og utdanning", "Arbeid og omsorg", "Ressurser", "Politikk", "Penger"]
DIMSSB = ["Offentlig tilrettelegging for potensiell likestilling", "Næringsstruktur og utdanningsmønster",
          "Fordeling av tidsbruk, arbeid og omsorg", "Fordeling av individuelle ressurser og innflytelse",
          "Fordeling av politisk innflytelse", "Fordeling av penger"]
# kode i 09292, kortnavn, dimensjon, type, kode(r) i 09293
IND = [
    ("Barnehage", "Barnehage", 0, "andel", "Barnehage"),
    ("UtdanningVGS", "Utdanningsprogram", 1, "skar", "UtdanningVGS"),
    ("Naringsstruktur", "Næringsstruktur", 1, "skar", "Naringsstruktur"),
    ("OffentligSektor", "Offentlig sektor", 1, "fordeling", ("KvinnerOffentligSyss", "MennOffentligSyss")),
    ("PrivatSektor", "Privat sektor", 1, "fordeling", ("KvinnerPrivatSyss", "MennPrivatSyss")),
    ("Arbeid", "Arbeidsstyrke", 2, "forhold", ("KvinnerTjueSekstisek", "MennTjueSekstiseks")),
    ("Deltidsarbeid", "Deltid", 2, "forhold", ("KvinnerDeltid", "MennDeltid")),
    ("Fedrekvote", "Fedrekvote", 2, "andel", "Fedrekvote"),
    ("UtdNiva", "Utdanningsnivå", 3, "forhold", ("UtdKvinner", "UtdMenn")),
    ("Ledere", "Ledere", 3, "fordeling", ("KvinnerLedere", "MennLedere")),
    ("KomRepresentant", "Kommunestyre", 4, "fordeling", ("KomRepresentant", "KomReprMenn")),
    ("InntektBrutto", "Inntekt", 5, "forhold", ("BruttoKvinner", "BruttoMenn")),
]
ENHET = {"InntektBrutto": "kr"}
# Første år etter bruddet. Fedrekvote og deltid etter Om statistikken. For arbeidsstyrke oppgir
# Om statistikken 2017, men grunnlagstallene hopper i 2015 (a-ordningen). Står på kvalitetssikringslisten.
BRUDD = {"Fedrekvote": 2013, "Deltidsarbeid": 2015, "Arbeid": 2015}
# Kjente avvik i landstallene mellom de to tabellene. Bygget stopper hvis listen endrer seg.
KJENTE_AVVIK = {("KomRepresentant", "2010")}  # 38,2 prosent kvinner gir 0,76, publisert skår er 0,75
HVA = {
    "Barnehage": "Andel barn 1–5 år i barnehage",
    "UtdanningVGS": "Hvor kjønnsbalanserte utdanningsprogram elevene i videregående velger",
    "Naringsstruktur": "Hvor kjønnsbalanserte næringene de sysselsatte jobber i, er",
    "OffentligSektor": "Kvinner og menn blant sysselsatte 20–66 år i offentlig sektor",
    "PrivatSektor": "Kvinner og menn blant sysselsatte 20–66 år i privat sektor",
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


class Tabell:
    """Et json-stat2-svar med dimensjonene Region, ContentsCode, Tid. Siste dimensjon går raskest."""
    def __init__(self, navn):
        d = json.loads((RAW / f"{navn}.json").read_text(encoding="utf8"))
        if d["id"] != ["Region", "ContentsCode", "Tid"]:
            feil(f"{navn}: uventede dimensjoner {d['id']}")
        def koder(dim):
            idx = d["dimension"][dim]["category"]["index"]
            return sorted(idx, key=idx.get) if isinstance(idx, dict) else list(idx)
        self.reg, self.var, self.aar = koder("Region"), koder("ContentsCode"), koder("Tid")
        if [len(self.reg), len(self.var), len(self.aar)] != d["size"]:
            feil(f"{navn}: dimensjonene stemmer ikke med size")
        self.ri = {r: i for i, r in enumerate(self.reg)}
        self.vi = {v: i for i, v in enumerate(self.var)}
        self.v = d["value"]
        self.regnavn = d["dimension"]["Region"]["category"]["label"]
        self.varnavn = d["dimension"]["ContentsCode"]["category"]["label"]
        self.oppdatert = d.get("updated", "")[:10]
        ukjent = set(d.get("status", {}).values()) - {".", ".."}
        if ukjent:
            feil(f"{navn}: statussymboler som ikke er håndtert: {sorted(ukjent)}")

    def tall(self, reg, var, t):
        if reg not in self.ri:
            return None
        return self.v[(self.ri[reg] * len(self.var) + self.vi[var]) * len(self.aar) + t]

    def har(self, reg, t):
        return any(self.tall(reg, v, t) is not None for v in self.var)


def lenker(klass, aar):
    """Endringer per år: {år: [(gammel, ny), ...]} for endringer som skjedde 1. januar det året."""
    ut = collections.defaultdict(list)
    for c in json.loads((RAW / f"{klass}.json").read_text(encoding="utf8"))["codeChanges"]:
        ut[int(c["changeOccurred"][:4])].append((c["oldCode"], c["newCode"]))
    return ut


def kjede(kode, endr, s, aar):
    """Koden som gjaldt hvert år, bakover fra siste år, så lenge endringene er ren omnummerering."""
    ut = [None] * len(aar)
    ut[-1] = kode
    for t in range(len(aar) - 1, 0, -1):
        e = endr.get(int(aar[t]), [])
        forgjengere = [g for g, n in e if n == kode]
        if not forgjengere:
            neste = kode
        elif len(forgjengere) == 1 and len([n for g, n in e if g == forgjengere[0]]) == 1:
            neste = forgjengere[0]
        else:
            break                                    # sammenslåing eller deling
        if not s.har(neste, t - 1):
            break
        kode = neste
        ut[t - 1] = kode
    return ut


def skar_fra(typ, k, m):
    return min(k, m) / 50 if typ == "fordeling" else min(k / m, m / k)


def main():
    s, g = Tabell("skar"), Tabell("grunnlag")
    aar, n = s.aar, len(s.aar)
    if aar != g.aar:
        feil("de to tabellene har ulike år")
    if n != int(aar[-1]) - int(aar[0]) + 1:
        feil("det mangler år i serien")
    if len(s.var) != 12:
        feil(f"ventet 12 indikatorer i 09292, fant {len(s.var)}")

    kart = json.loads((MAPPE / "src" / "kart.json").read_text(encoding="utf8"))["k"]
    kommuner = [r for r in s.reg if len(r) == 4 and s.har(r, n - 1)]
    fylker = [r for r in s.reg if len(r) == 2 and s.har(r, n - 1)]
    if len(kommuner) != 357 or len(fylker) != 15:
        feil(f"ventet 357 kommuner og 15 fylker med tall i {aar[-1]}, fant {len(kommuner)} og {len(fylker)}")
    if set(kommuner) != set(kart):
        feil(f"kommunene i tabellen og i kartet er ikke de samme: {sorted(set(kommuner) ^ set(kart))[:8]}")

    ek, ef = lenker("klass_kommuner", aar), lenker("klass_fylker", aar)
    regioner, hele, storst, hvor, avvik, mangler, grove = [], 0, 0.0, "", set(), 0, []
    rekke = [("0", "l")] + [(f, "f") for f in sorted(fylker)] + \
            [(k, "k") for k in sorted(kommuner, key=lambda k: (s.regnavn[k].lower(), k))]
    for kode, niva in rekke:
        kj = [kode] * n if niva == "l" else kjede(kode, ek if niva == "k" else ef, s, aar)
        fra = next(t for t in range(n) if kj[t])
        hele += fra == 0
        S, G = [], []
        for ikode, navn, dim, typ, gk in IND:
            sk = [s.tall(kj[t], ikode, t) if kj[t] else None for t in range(n)]
            if niva == "l" and any(v is None for v in sk):
                feil(f"hele landet mangler skår for {navn}")
            mangler += sum(1 for t in range(fra, n) if sk[t] is None)
            S.append([None if v is None else round(v * 100) for v in sk])
            if typ in ("fordeling", "forhold"):
                kv = [g.tall(kj[t], gk[0], t) if kj[t] else None for t in range(n)]
                mn = [g.tall(kj[t], gk[1], t) if kj[t] else None for t in range(n)]
                for t in range(n):
                    k, m, p = kv[t], mn[t], sk[t]
                    if k is None or m is None or p is None or k == 0 or m == 0:
                        continue
                    if typ == "fordeling" and abs(k + m - 100) > 0.11:
                        feil(f"{s.regnavn[kode]} {navn} {aar[t]}: kvinner + menn = {k + m}, ikke 100")
                    d = abs(skar_fra(typ, k, m) - p)
                    if niva == "l":
                        # Toleranse 0,011: skåren har to desimaler og grunnlagstallene er avrundet.
                        if d > 0.011:
                            avvik.add((ikode, aar[t]))
                        elif d > storst:
                            storst, hvor = d, f"{navn} {aar[t]}"
                    elif d > 0.05:
                        # I små kommuner gir avrundede prosenttall større utslag. Over 0,05 er det ikke avrunding.
                        grove.append((ikode, aar[t], f"{s.regnavn[kode]} {navn} {aar[t]}: {skar_fra(typ, k, m):.2f} mot {p}"))
                f = 1 if typ == "forhold" and ENHET.get(ikode) == "kr" else 10
                G.append([[None if v is None else round(v * f) for v in kv], [None if v is None else round(v * f) for v in mn]])
            elif typ == "andel":
                an = [g.tall(kj[t], gk, t) if kj[t] else None for t in range(n)]
                G.append([[None if v is None else round(v * 10) for v in an]])
            else:
                G.append(None)
        regioner.append({"k": kode, "n": s.regnavn[kode], "t": niva, "fra": int(aar[fra]), "s": S, "g": G})

    if avvik != KJENTE_AVVIK:
        feil(f"avvikene i landstallene er endret. Nye: {sorted(avvik - KJENTE_AVVIK)}. Borte: {sorted(KJENTE_AVVIK - avvik)}")
    # Kjent per 13.11.2026: offentlig sektor 2012 har 129 kommuner og fylker der skår og grunnlagstall
    # ikke stemmer overens. Landstallet for 2012 stemmer. Bygget stopper ved avvik andre steder.
    nye = [tekst for ikode, a, tekst in grove if (ikode, a) not in KJENTE_GROVE]
    if nye:
        feil(f"{len(nye)} nye avvik over 0,05 mellom skår og grunnlagstall i kommuner og fylker: {nye[:5]}")

    ind = [{"kode": k, "navn": nv, "ssbnavn": s.varnavn[k], "hva": HVA[k], "dim": dm, "type": ty,
            "brudd": BRUDD.get(k), "enhet": ENHET.get(k, "%"),
            "avvik": sorted({int(a) for ik, a, _ in grove if ik == k})} for k, nv, dm, ty, _ in IND]
    hentet = json.loads((RAW / "_hentet.json").read_text(encoding="utf8"))["hentet"]
    ut = {"aar": [int(a) for a in aar], "dim": DIM, "dimssb": DIMSSB, "ind": ind, "reg": regioner,
          "oppdatert": {"09292": s.oppdatert, "09293": g.oppdatert}, "hentet": hentet}
    UT.parent.mkdir(exist_ok=True)
    UT.write_text(json.dumps(ut, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(f"likekom: {len(regioner)} områder (1 + {len(fylker)} + {len(kommuner)}), {n} år. "
          f"{hele} har hel serie fra {aar[0]}. {mangler} skårer mangler («..»). "
          f"Landet: største avvik skår mot grunnlagstall {storst:.4f} ({hvor}). "
          f"Kommuner og fylker: {len(grove)} avvik over 0,05. {round(UT.stat().st_size / 1024)} kB.")


KJENTE_GROVE = {("OffentligSektor", "2012")}

if __name__ == "__main__":
    main()

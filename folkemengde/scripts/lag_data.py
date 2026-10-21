"""Lager build/folkemengde.json fra rådata i data/raw/ og kontrollerer summene.

Kjøres av felles/bygg.py. Stopper med feil hvis en kontroll ikke går opp:
- nøkkeltallene 2025–2026 er de publiserte
- befolkning(t+1) − befolkning(t) = folketilvekst(t) for landet, alle år
- kommunene + restkodene summerer til landet hvert år fra 1971 (avvik før 1971 er kjent, se kildekartet)
- kommunene summerer til fylkene 1986 og 2026
- kommunene summerer til landet per kvartal for fødte, døde, innvandring og utvandring
- aldersfordelingen summerer til befolkningen, for landet og hver kommune
- alle synonymer peker på kommuner som finnes
Bare standardbiblioteket.
"""
import itertools
import json
import pathlib
import sys

MAPPE = pathlib.Path(__file__).resolve().parent.parent
RAW = MAPPE / "data" / "raw"
UT = MAPPE / "build" / "folkemengde.json"

AAR_LAND = list(range(1735, 2027))
AAR_KOMM = list(range(1951, 2027))
ALDERSAAR_KOMM = ["1986", "2006", "2026"]

# Synonymer der Klass-kjeden gir for mange kommuner (kildekartet, hull H5). Rettes for hånd og merkes usikre.
SYN_RETT = {
    "Skodje": (["1508"], True),   # slått sammen med Ålesund 2020; Klass følger Ålesund 2020–2023, som ble delt i 2024
    "Ørskog": (["1508"], True),
    "Sandøy": (["1508"], True),
    "Stokke": (["3907"], True),   # slått sammen med Sandefjord 2017; Tønsberg-koden kommer trolig av en grensejustering
    "Varteig": (["3105"], True),  # slått sammen med Sarpsborg 1992; Rakkestad-koden kommer trolig av en grensejustering
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
    la, lk, lal, ka, kk, kal, fy = (les(n) for n in
                                    ("land_aar", "land_kvartal", "land_alder", "kommune_aar", "kommune_kvartal", "kommune_alder", "fylker"))
    hentet = json.loads((RAW / "_hentet.json").read_text(encoding="utf8"))["hentet"]

    # ---------- Landet per år ----------
    L = lambda m, a: hent(la, tom=True, ContentsCode=m, Tid=a)
    land = {
        "bef": [L("Personer", a) for a in AAR_LAND],
        "fodte": [L("Levendefodte", a) for a in AAR_LAND],
        "dode": [L("Dode", a) for a in AAR_LAND],
        "innv": [L("Innflyttinger", a) for a in AAR_LAND],
        "utv": [L("Utflyttinger", a) for a in AAR_LAND],
        "vekst": [L("AbsTilvekst", a) for a in AAR_LAND],
        "vekstpst": [L("Tilvekst", a) for a in AAR_LAND],
    }
    if (L("Personer", 2026), L("Levendefodte", 2025), L("Dode", 2025), L("Innflyttinger", 2025), L("Utflyttinger", 2025), L("AbsTilvekst", 2025)) \
            != (5627400, 55401, 45040, 55243, 32919, 33060):
        feil("nøkkeltallene for 2025–2026 er ikke de publiserte")
    avvik = [a for a in AAR_LAND[:-1] if None not in (L("Personer", a), L("Personer", a + 1), L("AbsTilvekst", a))
             and L("Personer", a + 1) - L("Personer", a) != L("AbsTilvekst", a)]
    if avvik:
        feil(f"befolkning(t+1) − befolkning(t) ≠ folketilvekst i {avvik}")

    # ---------- Kommuner ----------
    regioner = koder(ka, "Region")
    komm = [r for r in regioner if r[2:].isdigit() and len(r) == 6]
    rest = [r for r in regioner if r not in komm]
    if len(komm) != 357:
        feil(f"{len(komm)} kommuner, ventet 357")
    navn = ka["etiketter"]["Region"]
    fylkenavn = {k[2:]: v for k, v in fy["etiketter"]["Region"].items() if k[2:] not in ("21", "22", "23")}
    if len(fylkenavn) != 15:
        feil(f"{len(fylkenavn)} fylker, ventet 15")

    K = lambda r, m, a: hent(ka, ContentsCode=m, Region=r, Tid=a)
    kaar = {}
    mangler = 0
    for r in komm:
        bef = [K(r, "Folkemengde", a) for a in AAR_KOMM]
        finnes = [b > 0 for b in bef]
        # 0 betyr at kommunen ikke fantes (sammenslått eller ikke opprettet). Komponentene gjelder året
        # mellom 1. januar t og t+1 og vises bare når kommunen fantes begge dager.
        # Flyttinger mangler («..») for Sirdal, Haugesund, Sunndal og Smøla 1951–1957. De blir None.
        komp = lambda m: [hent(ka, tom=True, ContentsCode=m, Region=r, Tid=a) if finnes[i] and finnes[i + 1] else None
                          for i, a in enumerate(AAR_KOMM[:-1])]
        kaar[r[2:]] = [[b if b > 0 else None for b in bef], komp("Levende"), komp("Dode"), komp("Innflyttinger"), komp("Utflyttinger")]
        mangler += sum(1 for i, x in enumerate(kaar[r[2:]][3]) if x is None and finnes[i] and finnes[i + 1])

    if mangler != 28:
        feil(f"{mangler} kommuneår uten flyttetall, ventet 28 (fire kommuner 1951–1957)")

    # Kommunene + restkodene = landet hvert år fra 1971. Før 1971 avviker de med inntil 3 294 (kildekartet, H3).
    stor = 0
    for a in AAR_KOMM:
        s = sum(K(r, "Folkemengde", a) or 0 for r in regioner)
        d = s - L("Personer", a)
        if a >= 1971 and d:
            feil(f"kommunene summerer ikke til landet i {a} ({d})")
        stor = max(stor, abs(d))
    if stor > 3500:
        feil(f"avviket mellom kommunene og landet før 1971 er {stor}, mer enn de kjente 3 294")
    print(f"  kommuner = landet fra 1971; største avvik 1952–1970: {stor}")

    # I 1986 mangler de fem kommunene som ble delt i 2024 (Trøndelag og Nordland). De ligger i restkoden.
    for a in ("1986", "2026"):
        for f in fylkenavn:
            if a == "1986" and f in ("18", "50"):
                continue
            s = sum(K(r, "Folkemengde", a) for r in komm if r[2:4] == f)
            if s != hent(fy, Region="F-" + f, Tid=a):
                feil(f"kommunene i fylke {f} summerer ikke til fylket i {a}")

    # ---------- Kvartaler ----------
    kvartaler = [q for q in koder(kk, "Tid")]
    Q = lambda r, m, q: hent(kk, Region=r, ContentsCode=m, Tid=q)
    kregioner = koder(kk, "Region")
    kkv = {}
    for r in kregioner:
        if not (r[2:].isdigit() and len(r) == 6):
            continue
        kkv[r[2:]] = [[Q(r, m, q) for q in kvartaler] for m in ("Fodte2", "Dode3", "Innvandring5", "Utvandring6", "Tilflytting7", "Fraflytting8", "Folketallet11")]
    if set(kkv) != set(kaar):
        feil("kommunene i kvartalstallene og årstallene er ikke de samme")
    for m in ("Fodte2", "Dode3", "Innvandring5", "Utvandring6"):
        for q in kvartaler:
            if sum(Q(r, m, q) for r in kregioner) != hent(lk, Region="0", ContentsCode=m, Tid=q):
                feil(f"kommunene summerer ikke til landet for {m} i {q}")
    LQ = lambda m, q: hent(lk, Region="0", ContentsCode=m, Tid=q)
    land_kv = [[LQ(m, q) for q in kvartaler] for m in ("Fodte2", "Dode3", "Innvandring5", "Utvandring6", "Folketallet11")]
    if (LQ("Folketallet11", "2026K2"), LQ("Innvandring5", "2026K2") - LQ("Utvandring6", "2026K2")) != (5636904, -1590):
        feil("2026K2 er ikke de publiserte tallene")

    # ---------- Alder ----------
    aldre = koder(lal, "Alder")
    laar = koder(lal, "Tid")
    land_alder = {}
    for a in laar:
        v = [[hent(lal, Alder=x, Kjonn=kj, Tid=a) for x in aldre] for kj in ("1", "2")]
        land_alder[a] = v
        d = sum(v[0]) + sum(v[1]) - L("Personer", int(a))
        # Sju år avviker fra 05803. 1863–1996: −3 til +2 personer; 1915: −3 000 (kildekartet, H2).
        if d and not (abs(d) <= 3 or (a == "1915" and d == -3000)):
            feil(f"aldersfordelingen for landet {a} avviker med {d} fra befolkningen")
    grupper = koder(kal, "Alder")
    gruppenavn = [kal["etiketter"]["Alder"][g] for g in grupper]
    kalder = {}
    for r in koder(kal, "Region"):
        if not (r[2:].isdigit() and len(r) == 6):
            continue
        v = {a: [[hent(kal, Region=r, Kjonn=kj, Alder=g, Tid=a) for g in grupper] for kj in ("1", "2")] for a in ALDERSAAR_KOMM}
        for a in ALDERSAAR_KOMM:
            if sum(v[a][0]) + sum(v[a][1]) != (kaar[r[2:]][0][AAR_KOMM.index(int(a))] or 0):
                feil(f"aldersfordelingen for {r} i {a} summerer ikke til befolkningen")
        kalder[r[2:]] = [v[a] for a in ALDERSAAR_KOMM]

    # ---------- Synonymer ----------
    syn = json.loads((MAPPE / "data" / "synonymer.json").read_text(encoding="utf8"))["synonymer"]
    synonymer = []
    for ord_, mål in syn.items():
        mål, usikker = SYN_RETT.get(ord_, (mål, len(mål) > 1 and not ord_.startswith("Tysfjord") and ord_ != "Snillfjord"))
        if any(k not in kaar for k in mål):
            feil(f"synonymet {ord_} peker på en kommune som ikke finnes: {mål}")
        synonymer.append([ord_, mål, usikker])

    ut = {
        "kilde": {"hentet": hentet, "oppdatert": {t["navn"]: t["oppdatert"] for t in (la, lk, lal, ka, kk, kal)}},
        "land": {"aar": AAR_LAND, **land},
        "landKvartal": land_kv,
        "kvartaler": kvartaler,
        "landAlder": {"aar": [int(a) for a in laar], "aldre": aldre, "v": [land_alder[a] for a in laar]},
        "kommuner": [[r[2:], navn[r], r[2:4]] for r in komm],
        "fylker": fylkenavn,
        "kommAar": {"aar": AAR_KOMM, "v": kaar},
        "kommKvartal": kkv,
        "kommAlder": {"aar": [int(a) for a in ALDERSAAR_KOMM], "grupper": gruppenavn, "v": kalder},
        "synonymer": synonymer,
    }
    UT.parent.mkdir(exist_ok=True)
    UT.write_text(json.dumps(ut, ensure_ascii=False, separators=(",", ":")), encoding="utf8")
    print(f"  {UT.relative_to(MAPPE)}: {round(UT.stat().st_size / 1024)} kB, {len(komm)} kommuner, {len(kvartaler)} kvartaler, "
          f"{len(laar)} aldersår, {len(synonymer)} synonymer")


if __name__ == "__main__":
    main()

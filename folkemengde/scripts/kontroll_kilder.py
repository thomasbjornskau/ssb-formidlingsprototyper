"""Kontroller av rådataene for folkemengde (steg 3).

Leser data/raw/*.json og sjekker dem mot publiserte tall og mot hverandre.
Skriver også strukturtall som brukes i kildekartet. Avslutter med feilkode
hvis en kontroll feiler. Bare Pythons standardbibliotek.
"""
import collections
import itertools
import json
import sys
from pathlib import Path

ROT = Path(__file__).resolve().parents[1]
FEIL = []


def les(navn):
    d = json.loads((ROT / "data" / "raw" / f"{navn}.json").read_text(encoding="utf-8"))
    ids = d["id"]
    kat = [sorted(d["dimension"][i]["category"]["index"], key=d["dimension"][i]["category"]["index"].get) for i in ids]
    verdi = {k: d["value"][n] for n, k in enumerate(itertools.product(*kat))}
    return d, ids, kat, verdi


def sjekk(nr, tekst, ok, detalj=""):
    print(f"{nr:6} {'OK  ' if ok else 'FEIL'} {tekst} {detalj}")
    if not ok:
        FEIL.append(nr)


def info(tekst):
    print(f"       ·    {tekst}")


# ---------- Landet per år ----------
_, ids, kat, la = les("land_aar")
L = lambda v, a: la[(v, str(a))]
sjekk("K1", "Befolkning 1.1.2026 = 5 627 400", L("Personer", 2026) == 5627400)
f, d, i, u, g = (L(v, 2025) for v in ("Levendefodte", "Dode", "Innflyttinger", "Utflyttinger", "AbsTilvekst"))
sjekk("K1b", "2025: fødte 55 401, døde 45 040, innv. 55 243, utv. 32 919, vekst 33 060",
      (f, d, i, u, g) == (55401, 45040, 55243, 32919, 33060))
sjekk("K1c", "Korreksjon 2025 = 375", g - (f - d) - (i - u) == 375)
avvik = [a for a in range(1735, 2026) if L("Personer", a) is not None and L("Personer", a + 1) is not None
         and L("AbsTilvekst", a) is not None and L("Personer", a + 1) - L("Personer", a) != L("AbsTilvekst", a)]
sjekk("K1d", "Befolkning(t+1) − befolkning(t) = folketilvekst(t), alle år", not avvik, f"({len(avvik)} avvik: {avvik[:8]})")
mangler = {v: sum(1 for a in kat[1] if la[(v, a)] is None) for v in kat[0]}
info(f"land_aar: år uten tall per variabel {mangler}")
korr = {a: L("AbsTilvekst", a) - (L("Levendefodte", a) - L("Dode", a)) - (L("Innflyttinger", a) - L("Utflyttinger", a))
        for a in range(1735, 2026) if None not in (L("AbsTilvekst", a), L("Levendefodte", a), L("Dode", a), L("Innflyttinger", a), L("Utflyttinger", a))}
info(f"land_aar: korreksjon finnes for {min(korr)}–{max(korr)} ({len(korr)} år); største |korr| "
     f"{sorted(korr.items(), key=lambda x: -abs(x[1]))[:3]}")

# ---------- Landet per kvartal ----------
_, ids, kat, lk = les("land_kvartal")
K = lambda v, q: lk[("0", v, q)]
sjekk("K2", "2026K2: utgang 5 636 904, vekst 3 134, innv − utv = −1 590",
      K("Folketallet11", "2026K2") == 5636904 and K("Folketilvekst10", "2026K2") == 3134
      and K("Innvandring5", "2026K2") - K("Utvandring6", "2026K2") == -1590)
q25 = [f"2025K{n}" for n in range(1, 5)]
info(f"Kvartalssum 2025 mot årstall: fødte {sum(K('Fodte2', q) for q in q25)} / {L('Levendefodte', 2025)}, "
     f"døde {sum(K('Dode3', q) for q in q25)} / {L('Dode', 2025)}, innv. {sum(K('Innvandring5', q) for q in q25)} / {L('Innflyttinger', 2025)}, "
     f"utv. {sum(K('Utvandring6', q) for q in q25)} / {L('Utflyttinger', 2025)}")
neg = [q for q in kat[2] if K("Innvandring5", q) - K("Utvandring6", q) < 0]
sjekk("K2b", "Kvartaler med negativ nettoinnvandring = 2020K2, 2021K2, 2026K2", neg == ["2020K2", "2021K2", "2026K2"], str(neg))

# ---------- Landet etter alder ----------
_, ids, kat, al = les("land_alder")
aar_alder = kat[3]
avvik = [a for a in aar_alder if sum(al[(x, k, "Personer", a)] or 0 for k in ("1", "2") for x in kat[0]) != L("Personer", int(a))]
KJENT_K3 = {"1863", "1864", "1915", "1973", "1988", "1996"}  # avvik −3 til +2, og −3 000 i 1915 (se kildekartet, hull H6)
sjekk("K3", "Sum alder × kjønn = befolkning 1.1. i 05803, unntatt seks kjente år", set(avvik) == KJENT_K3, f"({len(avvik)} avvik: {avvik})")
info(f"land_alder: {len(kat[0])} alderskoder ({kat[0][0]}–{kat[0][-1]}), {len(aar_alder)} år, "
     f"{sum(1 for v in al.values() if v is None)} celler uten tall")

# ---------- Kommuner per år ----------
dka, ids, kat, ka = les("kommune_aar")
navn = dka["dimension"]["Region"]["category"]["label"]
komm = [k for k in kat[0] if k[2:].isdigit() and len(k) == 6]
kommkode = {k[2:]: k for k in komm}
rest = [k for k in kat[0] if k not in komm]
sjekk("K4", "357 kommuner i kommune_aar", len(komm) == 357, f"(restkoder: {rest})")
avvik = [a for a in kat[2] if sum(ka[(k, "Folkemengde", a)] or 0 for k in kat[0]) != L("Personer", int(a))]
sjekk("K4b", "Sum kommuner + restkoder = landet hvert år fra 1971", all(int(a) < 1971 for a in avvik),
      f"({len(avvik)} avvik, alle i 1952–1970: {avvik})")
avvik = [a for a in kat[2] if sum(ka[(k, "Folkemengde", a)] or 0 for k in komm) != L("Personer", int(a))]
info(f"Sum bare kommuner (uten restkoder) avviker fra landet i {len(avvik)} av {len(kat[2])} år; "
     f"restkode 2026 = {[ka[(k, 'Folkemengde', '2026')] for k in rest]}")
start = {}
for k in komm:
    ar = [a for a in kat[2] if (ka[(k, "Folkemengde", a)] or 0) > 0]
    start[k] = ar[0] if ar else None
fordeling = collections.Counter(start.values())
info(f"Første år med befolkning > 0: {sorted(fordeling.items())}")
info("Kommuner som starter etter 1951: " + ", ".join(f"{navn[k]} ({start[k]})" for k in komm if start[k] != "1951"))
# hull: 0 midt i serien
hull = [k for k in komm if any((ka[(k, "Folkemengde", a)] or 0) == 0 for a in kat[2] if int(a) > int(start[k] or 9999))]
KJENT_HULL = {"K_3310", "K_3426", "K_3430", "K_3436", "K_3438", "K_4619", "K_1580", "K_1812", "K_1859", "K_5518"}
sjekk("K4c", "Kommuner med 0 midt i serien er de ti kjente (sammenslått i perioder)", set(hull) == KJENT_HULL,
      "; ".join(f"{navn[k]} {min(a for a in kat[2] if int(a) > int(start[k]) and not ka[(k, 'Folkemengde', a)])}–"
                f"{max(a for a in kat[2] if int(a) > int(start[k]) and not ka[(k, 'Folkemengde', a)])}" for k in hull))
for nr, (kode, aar, tall) in enumerate([("K_0301", "2026", 728714), ("K_1151", "2026", 219), ("K_3450", "2025", 1254)]):
    sjekk(f"K4d{nr}", f"{navn[kode]} {aar} = {tall}", ka[(kode, "Folkemengde", aar)] == tall)
# regnskap per kommune 2025: bef 2026 − bef 2025 mot fødte − døde + inn − ut
rk = {k: ka[(k, "Folkemengde", "2026")] - ka[(k, "Folkemengde", "2025")]
      - (ka[(k, "Levende", "2025")] - ka[(k, "Dode", "2025")] + ka[(k, "Innflyttinger", "2025")] - ka[(k, "Utflyttinger", "2025")])
      for k in komm}
info(f"Korreksjon per kommune 2025: sum {sum(rk.values())}, ulik 0 i {sum(1 for v in rk.values() if v)} kommuner, "
     f"største {sorted(((navn[k], v) for k, v in rk.items()), key=lambda x: -abs(x[1]))[:3]}")
ned = sum(1 for k in komm if ka[(k, "Folkemengde", "2026")] < ka[(k, "Folkemengde", "2025")])
sjekk("K4e", "128 kommuner med nedgang i 2025", ned == 128, f"({ned})")

# ---------- Kommuner per kvartal ----------
dkk, ids, kat, kk = les("kommune_kvartal")
kommk = [k for k in kat[0] if k[2:].isdigit() and len(k) == 6]
avvik = [(v, q) for v in ("Fodte2", "Dode3", "Innvandring5", "Utvandring6") for q in kat[2]
         if sum(kk[(k, v, q)] or 0 for k in kat[0]) != K(v, q)]
sjekk("K5", "Sum kommuner = landet per kvartal (fødte, døde, innv., utv.)", not avvik, f"({len(avvik)} avvik: {avvik[:5]})")
avvik = [q for q in kat[2] if sum(kk[(k, "Tilflytting7", q)] or 0 for k in kommk) != sum(kk[(k, "Fraflytting8", q)] or 0 for k in kommk)]
sjekk("K5b", "Innenlandsk inn = innenlandsk ut summert over kommunene fra 2020", all(q < "2020" for q in avvik),
      f"({len(avvik)} kvartaler avviker, alle 2016–2019)")
osl = sum(kk[("K-0301", "Innvandring5", q)] for q in q25)
sjekk("K5c", "Oslo, innvandring summert over kvartalene 2025 = 9 501", osl == 9501, f"({osl}; årstall i 09588: 9 484)")
avvik = [k for k in kommk if kk[(k, "Folketallet11", "2025K4")] != ka.get((kommkode[k[2:]], "Folkemengde", "2026"))]
sjekk("K5d", "Utgang 2025K4 = 1.1.2026 per kommune, unntatt Indre Østfold, Nordre Follo og Vestby (+29, −27, −2)",
      sorted(avvik) == ["K-3118", "K-3207", "K-3216"], f"({len(avvik)} avvik: {avvik})")
diff = {k: sum(kk[(k, "Fodte2", q)] for q in q25) - ka[(kommkode[k[2:]], "Levende", "2025")] for k in kommk}
info(f"Fødte 2025, kvartalssum − årstall per kommune: ulik 0 i {sum(1 for v in diff.values() if v)}, "
     f"spenn {min(diff.values())} til {max(diff.values())}")
diff = {k: sum((kk[(k, "Innvandring5", q)] + kk[(k, "Tilflytting7", q)]) for q in q25) - ka[(kommkode[k[2:]], "Innflyttinger", "2025")] for k in kommk}
info(f"Innflyttinger 2025 (innv. + innenlands), kvartalssum − årstall: ulik 0 i {sum(1 for v in diff.values() if v)}, "
     f"spenn {min(diff.values())} til {max(diff.values())}")
mangl = collections.Counter(v is None for v in kk.values())
info(f"kommune_kvartal: {mangl[True]} celler uten tall av {sum(mangl.values())}")
neg = collections.Counter(q for q in kat[2] for k in kommk if (kk[(k, "Utvandring6", q)] or 0) > (kk[(k, "Innvandring5", q)] or 0))
info(f"Kommuner med negativ nettoinnvandring, 2026K2: {neg['2026K2']}, 2025K2: {neg['2025K2']}, 2025K3: {neg['2025K3']}")

# ---------- Kommuner etter alder ----------
dal, ids, kat, ka2 = les("kommune_alder")
kommA = [k for k in kat[0] if k[2:].isdigit() and len(k) == 6]
for aar in ("1986", "2006", "2026"):
    s = sum(v or 0 for (k, kj, x, c, a), v in ka2.items() if a == aar)
    sjekk(f"K6-{aar}", f"Sum kommune_alder {aar} = landet", s == L("Personer", int(aar)), f"({s} / {L('Personer', int(aar))})")
avvik = [k for k in kommA if sum(ka2[(k, kj, x, "Personer1", "2026")] or 0 for kj in kat[1] for x in kat[2]) != ka[(kommkode[k[2:]], "Folkemengde", "2026")]]
sjekk("K6b", "Per kommune: sum alder 2026 = kommune_aar 2026", not avvik, f"({len(avvik)} avvik)")
info(f"Aldersgrupper: {kat[2][0]}–{kat[2][-1]} ({len(kat[2])}); etiketter {dal['dimension']['Alder']['category']['label'][kat[2][-1]]}")
null1986 = [navn.get(k, k) for k in kommA if sum(ka2[(k, kj, x, "Personer1", "1986")] or 0 for kj in kat[1] for x in kat[2]) == 0]
info(f"Kommuner uten aldersfordeling i 1986: {len(null1986)} {null1986}")

# ---------- Navn ----------
tospraak = [navn[k] for k in komm if " - " in navn[k]]
info(f"Tospråklige navn: {len(tospraak)}")
fylker = collections.Counter(k[2:4] for k in komm)
info(f"Fylker: {len(fylker)}, kommuner per fylke {sorted(fylker.items())}")

print()
print("Alle kontroller OK" if not FEIL else f"FEIL i {FEIL}")
sys.exit(1 if FEIL else 0)

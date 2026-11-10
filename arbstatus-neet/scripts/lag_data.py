"""Datasteget for formidlingsprototypen arbstatus-neet (unge utenfor arbeid, utdanning og tiltak).

Bruk:  python arbstatus-neet/scripts/lag_data.py
Leser arbstatus-neet/data/raw/*.json, kjører kontrollene og skriver arbstatus-neet/build/arbstatus-neet.json (kompakt).
Stopper med «Kontroll feilet: …» hvis en kontroll ikke holder. Bare Pythons standardbibliotek.

NEET finnes ikke som kode i 12424, 12427 eller 14158 og bygges av tre statuser:
  12424:            A.09 + U.04-U.05 + U.90B
  12427/14158 start: A.09 + U.04-U.05 + U.90A
  12427/14158 senere: A.09 + U.04-U.05 + U.90E   (UT.01 = ut av populasjonen, egen kategori)
"""

import itertools
import json
import os
import sys

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROT, "data", "raw")
avvik_logg = []


def feil(melding):
    sys.exit("Kontroll feilet: " + melding)


def les(ds_id):
    """json-stat2 til (kategorinøkler per dimensjon, {nøkkeltuppel: (verdi, status)}, oppdatert)."""
    d = json.load(open(os.path.join(RAW, ds_id + ".json"), encoding="utf-8"))
    kat = [d["dimension"][i]["category"] for i in d["id"]]
    nokler = [sorted(c["index"], key=c["index"].get) for c in kat]
    st = d.get("status") or {}
    verdier = {k: (d["value"][n], st.get(str(n))) for n, k in enumerate(itertools.product(*nokler))}
    return nokler, verdier, d.get("updated", "")[:10]


def dato(iso):
    return f"{iso[8:10]}.{iso[5:7]}.{iso[:4]}" if iso else ""


def kontroll(navn, avvik_liste, toleranse, forklaring):
    avvik = max((abs(x) for x in avvik_liste), default=0)
    avvik_logg.append((navn, avvik, toleranse, len(avvik_liste)))
    if avvik > toleranse:
        feil(f"{navn}: største avvik {avvik} er over toleransen {toleranse} ({forklaring})")


oppdatert = {}
# Avrunding: SSB avrunder celler med 1 eller 2 til 0 eller 3 i hver tabell for seg («Om statistikken»).
# Tabeller og år som lages fra hver sin datamatrise, kan derfor avvike med noen titalls personer.

# ---------------- 12424: tverrsnitt ----------------
(K, A, U, I, S, _, T), V, oppdatert["12424"] = les("tverrsnitt")
AR = T
g = lambda k, a, u, i, s, t: V[(k, a, u, i, s, "Bosatte", t)][0]  # noqa: E731
if any(st for _, st in V.values()):
    feil("12424 har statussymboler; de må tolkes før bruk")
HIER = {"TOT": ["A.01", "A.09", "U.01", "U.03", "U.04-U.05", "U.90B"], "U.04-U.05": ["U.04.00", "U.05.00"], "U.90B": ["U.90B.00", "UX.00"]}
for p, ch in HIER.items():
    kontroll(f"K1 12424 {p} = sum av undernivåene", [g(k, a, u, i, p, t) - sum(g(k, a, u, i, c, t) for c in ch)
             for k, a, u, i, t in itertools.product(K, A, U, I, T)], 0, "eksakt i tabellen")
kontroll("K2 12424 kjønn, alder, utdanning og innvandring summerer",
         [g("0", a, u, i, s, t) - g("1", a, u, i, s, t) - g("2", a, u, i, s, t) for s, t, a, u, i in itertools.product(S, T, A, U, I)]
         + [g(k, "15-29", u, i, s, t) - sum(g(k, x, u, i, s, t) for x in A[1:]) for s, t, k, u, i in itertools.product(S, T, K, U, I)]
         + [g(k, a, "TOT", i, s, t) - sum(g(k, a, x, i, s, t) for x in U[1:]) for s, t, k, a, i in itertools.product(S, T, K, A, I)]
         + [g(k, a, u, "A-G", s, t) - g(k, a, u, "A_C-G", s, t) - g(k, a, u, "B", s, t) for s, t, k, a, u in itertools.product(S, T, K, A, U)],
         0, "eksakt i tabellen")
neet = lambda k, a, u, i, t: g(k, a, u, i, "A.09", t) + g(k, a, u, i, "U.04-U.05", t) + g(k, a, u, i, "U.90B", t)  # noqa: E731

# ---------------- 13556: kontroll av NEET ----------------
(_, K2, A2, _, _, T2), W, oppdatert["13556"] = les("kontroll_neet")
kontroll("K3 NEET-antall 12424 = NEET i 13556", [neet(k, a, "TOT", "A-G", t) - W[("0", k, a, "NEET", "Bosatte", t)][0]
         for k, a, t in itertools.product(K2, A2, T2)], 10, "avrunding mellom tabeller, faktisk største 6")
kontroll("K4 NEET-andel regnet fra 12424 = publisert i 13556 (tideler)",
         [round(10 * (100 * neet(k, a, "TOT", "A-G", t) / g(k, a, "TOT", "A-G", "TOT", t) - W[("0", k, a, "NEET", "BosatteProsent", t)][0]))
          for k, a, t in itertools.product(K2, A2, T2)], 1, "én celle ligger på grensen (9,95)")

STATUS_UT = ["TOT", "A.01", "U.03", "U.01", "A.09", "U.04.00", "U.05.00", "U.90B.00", "UX.00"]
grupper = {f"{k}|{a}|{u}|{i}": [[g(k, a, u, i, s, t) for t in T] for s in STATUS_UT] for k, a, u, i in itertools.product(K, A, U, I)}

# ---------------- 12427: forløp ----------------
(SA, _, _, _, IN, S1, S2, _, TT), F, oppdatert["12427"] = les("forlop")
f = lambda sa, i, s1, s2, t: F[(sa, "0", "15-29", "TOT", i, s1, s2, "Bosatte", t)][0]  # noqa: E731
N1, N2, IKKE = ["A.09", "U.04-U.05", "U.90A"], ["A.09", "U.04-U.05", "U.90E"], ["A.01", "U.01", "U.03"]
kontroll("K5 12427 år før startåret er 0", [f(sa, i, a, b, t) for sa, i, a, b, t in itertools.product(SA, IN, S1, S2, TT) if t < sa], 0, "strukturelt tomme")
par = [("TOT2", "TOT"), ("A.01", "A.01"), ("A.09", "A.09"), ("U.01", "U.01"), ("U.03", "U.03"), ("U.04-U.05", "U.04-U.05"), ("U.90A", "U.90B")]
kontroll("K6 12427 startåret = 12424 samme år", [f(t, i, a, "TOT2", t) - g("0", "15-29", "TOT", i, b, t) for t in SA for i in IN for a, b in par],
         30, "avrunding mellom tabeller, faktisk største 14")
kontroll("K7 12427 kullet er like stort hvert år", [f(sa, i, s, "TOT2", t) - f(sa, i, s, "TOT2", sa)
         for sa, i, s, t in itertools.product(SA, IN, S1, TT) if t >= sa], 50, "avrunding per år, faktisk største 47 av 955 000")
kontroll("K8 12427 status i tidsserien summerer til i alt", [f(sa, i, s, "TOT2", t) - sum(f(sa, i, s, x, t) for x in S2[1:])
         for sa, i, s, t in itertools.product(SA, IN, S1, TT) if t >= sa], 30, "faktisk 0")
kontroll("K9 12427 innvandring summerer", [f(sa, "A-G", a, b, t) - f(sa, "A_C-G", a, b, t) - f(sa, "B", a, b, t)
         for sa, a, b, t in itertools.product(SA, S1, S2, TT) if t >= sa], 30, "faktisk 0")

forlop = {}
for i in IN:
    tilgang = {}
    for t in SA[:-1]:
        t1 = str(int(t) + 1)
        tilgang[t1] = [sum(f(t, i, a, b, t1) for a in IKKE for b in N2), sum(f(t, i, a, b, t1) for a in N1 for b in IKKE),
                       sum(f(t, i, a, "UT.01", t1) for a in N1)]
    varighet = {}
    for sa in SA:
        base = sum(f(sa, i, s, "TOT2", sa) for s in N1)
        rad = [[base, 0, 0]]
        for t in TT:
            if t > sa:
                rad.append([sum(f(sa, i, a, b, t) for a in N1 for b in N2), sum(f(sa, i, a, b, t) for a in N1 for b in IKKE),
                            sum(f(sa, i, a, "UT.01", t) for a in N1)])
        varighet[sa] = rad
    aap = {sa: [f(sa, i, "U.04-U.05", "TOT2", sa)] + [f(sa, i, "U.04-U.05", "U.04-U.05", t) for t in TT if t > sa] for sa in SA}
    forlop[i] = {"tilgang": tilgang, "varighet": varighet, "aap": aap}
# Startåret i varigheten må være lik NEET i 12424 samme år
kontroll("K10 NEET i startåret (12427) = NEET (12424)", [forlop[i]["varighet"][t][0][0] - neet("0", "15-29", "TOT", i, t) for i in IN for t in SA],
         30, "avrunding mellom tabeller")

# ---------------- 14158: forløp etter utdanning og alder ----------------
(SA4, S14, S24, UT4, _, AL4, _, _, _, TT4), H, oppdatert["14158"] = les("forlop_utdanning")
h = lambda sa, a, b, u, al, t: H[(sa, a, b, u, "00", al, "0", "A-G", "Bosatte", t)][0]  # noqa: E731
gyldig = [(sa, a, u, al, t) for sa, a, u, al, t in itertools.product(SA4, S14, UT4, AL4, TT4) if t >= sa]
kontroll("K11 14158 år før startåret er 0", [h(sa, a, b, u, al, t) for sa, a, b, u, al, t in itertools.product(SA4, S14, S24, UT4, AL4, TT4) if t < sa], 0, "strukturelt tomme")
kontroll("K12 14158 status i tidsserien summerer", [h(sa, a, "TOT2", u, al, t) - sum(h(sa, a, x, u, al, t) for x in S24[1:]) for sa, a, u, al, t in gyldig], 30, "faktisk 0")
kontroll("K13 14158 utdanningshierarkiet summerer",
         [h(sa, a, "TOT2", "0", al, t) - sum(h(sa, a, "TOT2", u, al, t) for u in ["1-2", "3-5", "11", "6-8", "0_9"]) for sa, a, u, al, t in gyldig if u == "0"]
         + [h(sa, a, "TOT2", "3-5", al, t) - sum(h(sa, a, "TOT2", u, al, t) for u in ["3-4a", "3-4b", "3-4c"]) for sa, a, u, al, t in gyldig if u == "0"],
         30, "faktisk 0")
kontroll("K14 14158 tre aldersgrupper = 12427 15–29 år", [sum(h(sa, a, b, "0", al, t) for al in AL4) - f(sa, "A-G", a, b, t)
         for sa, a, b, t in itertools.product(SA4, S14, S24, TT4) if t >= sa], 60, "avrunding mellom tabeller, faktisk største 44")
UTD_VIS = ["0", "1-2", "3-4a", "3-4b", "6-8"]
utdanning = {}
for al in AL4:
    for u in UTD_VIS:
        for sa in SA4:
            base = sum(h(sa, s, "TOT2", u, al, sa) for s in N1)
            utdanning[f"{al}|{u}|{sa}"] = [h(sa, "TOT2", "TOT2", u, al, sa), base] + [sum(h(sa, a, b, u, al, t) for a in N1 for b in N2) for t in TT4 if t > sa]

# ---------------- 13347: barnevern ----------------
(SB, KB, FB, BB, _, TB), B, oppdatert["13347"] = les("barnevern")
mangler = {k for k, (v, st) in B.items() if st == ".."}
if any(st not in (None, "..") for _, st in B.values()):
    feil("13347 har andre statussymboler enn «..»")
b = lambda s, k, fu, bv, c, t: B[(s, k, fu, bv, c, t)][0]  # noqa: E731
ok = lambda *kk: not any(x in mangler for x in kk)  # noqa: E731
kontroll("K15 13347 statusene summerer til alle", [b("0", k, fu, bv, "Elever", t) - sum(b(s, k, fu, bv, "Elever", t) for s in SB[1:])
         for k, fu, bv, t in itertools.product(KB, FB, BB, TB) if ok(*[(s, k, fu, bv, "Elever", t) for s in SB])], 20, "støylagt, faktisk 0")
kontroll("K16 13347 barnevernsgruppene summerer",
         [b(s, k, fu, "0", "Elever", t) - b(s, k, fu, "1", "Elever", t) - b(s, k, fu, "2", "Elever", t)
          for s, k, fu, t in itertools.product(SB, KB, FB, TB) if ok(*[(s, k, fu, x, "Elever", t) for x in "012"])]
         + [b(s, k, fu, "2", "Elever", t) - b(s, k, fu, "3", "Elever", t) - b(s, k, fu, "4", "Elever", t)
            for s, k, fu, t in itertools.product(SB, KB, FB, TB) if ok(*[(s, k, fu, x, "Elever", t) for x in "234"])], 20, "støylagt, faktisk 0")
kontroll("K17 13347 publisert prosent = antall / alle (tideler)",
         [round(10 * (100 * b(s, k, fu, bv, "Elever", t) / b("0", k, fu, bv, "Elever", t) - b(s, k, fu, bv, "EleverProsent", t)))
          for s, k, fu, bv, t in itertools.product(SB, KB, FB, BB, TB)
          if ok((s, k, fu, bv, "Elever", t), (s, k, fu, bv, "EleverProsent", t)) and b("0", k, fu, bv, "Elever", t) > 0], 1, "avrunding")
# Brudd: fra 2023 er «død/utvandret» (6) slått sammen med «annet» (9) i tabellen. Kategorien vises da som manglende, ikke 0.
for bv in BB:
    for t in TB:
        if t >= "2023" and b("6", "0", "0-10", bv, "EleverProsent", t) not in (0, None):
            feil(f"13347 død/utvandret er ikke 0 i {t}; bruddet fra 2023 må vurderes på nytt")
barnevern = {f"{bv}|{t}": {"elever": b("0", "0", "0-10", bv, "Elever", t),
                           "prosent": [None if (s, "0", "0-10", bv, "EleverProsent", t) in mangler or (s == "6" and t >= "2023")
                                       else b(s, "0", "0-10", bv, "EleverProsent", t) for s in SB[1:]]}
             for bv, t in itertools.product(BB, TB)}

# ---------------- ut ----------------
ut = {
    "ar": AR, "startar": SA, "startar_utd": SA4, "ar_bv": TB,
    "oppdatert": {k: dato(v) for k, v in oppdatert.items()},
    "status": STATUS_UT, "grupper": grupper,
    "forlop": forlop, "utdanning": utdanning, "barnevern": barnevern,
    "bv_status": ["I høyere utdanning", "I lavere utdanning", "Sysselsatt", "Helserelaterte ytelser", "Andre ytelser", "Død eller utvandret", "Annet"],
}
os.makedirs(os.path.join(ROT, "build"), exist_ok=True)
with open(os.path.join(ROT, "build", "arbstatus-neet.json"), "w", encoding="utf-8") as fil:
    json.dump(ut, fil, ensure_ascii=False, separators=(",", ":"), sort_keys=True)

storst = max(avvik_logg, key=lambda x: x[1] / x[2] if x[2] else (0 if x[1] == 0 else 1e9))
print(f"{len(avvik_logg)} kontroller bestått ({sum(x[3] for x in avvik_logg)} celler). "
      f"Største relative avvik: {storst[0]} = {storst[1]} (toleranse {storst[2]}). Grupper: {len(grupper)}, 13347 med «..»: {len(mangler)}.")

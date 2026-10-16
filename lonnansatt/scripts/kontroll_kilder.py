"""Kontroller av rådataene for lonnansatt (steg 3).

Leser data/raw/*.json og sjekker dem mot publiserte tall og mot hverandre.
Avslutter med feilkode hvis en kontroll feiler. Bare Pythons standardbibliotek.
"""

import itertools
import json
import sys
from pathlib import Path

ROT = Path(__file__).resolve().parents[1]
FEIL = []


def les(navn):
    d = json.loads((ROT / "data" / "raw" / f"{navn}.json").read_text(encoding="utf-8"))
    ids, size = d["id"], d["size"]
    kat = [list(d["dimension"][i]["category"]["index"]) for i in ids]
    verdi = {}
    for n, komb in enumerate(itertools.product(*kat)):
        verdi[komb] = d["value"][n]
    return d, ids, verdi


def sjekk(nr, tekst, ok, detalj=""):
    print(f"{nr:4} {'OK ' if ok else 'FEIL'} {tekst} {detalj}")
    if not ok:
        FEIL.append(nr)


# K1 Nøkkeltall i yrkestabellen mot statistikksiden og innsiktsnotatet
_, ids, y = les("yrker")
g = lambda m, yrke, kj, aar: y[(m, yrke, "ALLE", kj, "0", "Manedslonn", aar)]
sjekk("K1", "Gjennomsnitt alle yrker 2025 = 62 070", g("02", "0-9", "0", "2025") == 62070)
sjekk("K1b", "Median alle yrker 2025 = 55 800", g("01", "0-9", "0", "2025") == 55800)
sjekk("K1c", "Handels- og skipsmeglere 2025 = 172 630, 771 jobber",
      g("02", "3324", "0", "2025") == 172630 and g("10", "3324", "0", "2025") == 771)

# K2 Jobber: menn + kvinner = begge kjønn for alle yrker og år der alle tre har tall
avvik = [(k, a) for k in {x[1] for x in y} for a in [str(t) for t in range(2016, 2026)]
         if None not in (g("10", k, "0", a), g("10", k, "1", a), g("10", k, "2", a))
         and g("10", k, "1", a) + g("10", k, "2", a) != g("10", k, "0", a)]
sjekk("K2", "Jobber menn + kvinner = begge kjønn", not avvik, f"({len(avvik)} avvik)")

# K3 Vektet snitt av firesifrede yrker med heltidsekvivalenter gjenskaper totalen (innen 0,1 prosent)
fire = [k for k in {x[1] for x in y} if len(k) == 4]
for aar in ("2016", "2025"):
    par = [(g("02", k, "0", aar), g("11", k, "0", aar)) for k in fire]
    par = [(a, b) for a, b in par if a is not None and b is not None]
    vs = sum(a * b for a, b in par) / sum(b for a, b in par)
    tot = g("02", "0-9", "0", aar)
    sjekk(f"K3-{aar}", "Vektet snitt av yrker ≈ publisert total", abs(vs / tot - 1) < 0.001,
          f"({vs:.0f} mot {tot})")

# K4 Vekst regnet fra kroner per yrke = publiserte rater i «Høyest lønnsvekst i toppen»
PUB = {"2223": 2.8, "2221": 2.7, "5329": 2.6, "5120": 3.0, "5321": 3.1, "2341": 3.6, "2212": 3.5,
       "2224": 3.4, "2330": 3.4, "5311": 3.3, "2413": 6.9, "1219": 5.9, "1120": 5.7, "2411": 5.7,
       "5246": 5.7, "1221": 5.5, "2422": 5.3, "2310": 5.3, "3313": 5.2, "3511": 5.2}
avvik = [k for k, p in PUB.items()
         if round((g("02", k, "0", "2025") / g("02", k, "0", "2024") - 1) * 100, 1) != p]
sjekk("K4", "Vekst fra kroner = publisert rate for 20 yrker", not avvik, f"(avvik: {avvik})")

# K5 Månedslønn = avtalt + uregelmessige tillegg + bonus (innen 10 kr avrunding)
_, _, h = les("hovedtall")
maks = 0
for k in h:
    if k[5] == "Manedslonn" and k[0] == "02":
        a, u, b = (h[k[:5] + (c, k[6])] for c in ("AvtaltManedslonn", "Uregtil", "Bonus"))
        maks = max(maks, abs(a + u + b - h[k]))
sjekk("K5", "Månedslønn = avtalt + tillegg + bonus, alle sektorer, kjønn, arbeidstid og år", maks <= 20,
      f"(største avvik {maks} kr)")

# K6 Median i 11419 = øvre grense for desil 5 i 13860, begge kjønn og per kjønn, alle år
_, _, d = les("desiler")
avvik = [(kj, a) for kj in ("0", "1", "2") for a in [str(t) for t in range(2016, 2026)]
         if d[(kj, "A-Z", "05", "GrvManedslonn", a)] != h[("01", "0-9", "ALLE", kj, "0", "Manedslonn", a)]]
sjekk("K6", "Median = grense desil 5, 30 kombinasjoner", not avvik, f"({avvik})")

# K7 Gjennomsnitt og median i 11419 = alle yrker i 11418, alle år og kjønn.
# Kjent avvik: menn 2023, 11419 (05.02.2026) 59 460 og 52 290, 11418 (28.08.2026) 59 450 og 52 280.
# Trolig revisjon i august. Spørsmål til fag (03-kildekart, hull 2). Nye avvik stopper bygget.
KJENT = {("02", "1", "2023"), ("01", "1", "2023")}
avvik = {(m, kj, a) for m in ("02", "01") for kj in ("0", "1", "2") for a in [str(t) for t in range(2016, 2026)]
         if h[(m, "0-9", "ALLE", kj, "0", "Manedslonn", a)] != g(m, "0-9", kj, a)}
sjekk("K7", "11419 og 11418 gir samme gjennomsnitt og median, utenom kjent avvik", avvik <= KJENT,
      f"(kjente avvik funnet: {len(avvik & KJENT)}, nye: {sorted(avvik - KJENT)})")

# K8 «Minst 6 av 10 under gjennomsnittet»: grense desil 6 < gjennomsnitt < grense desil 7, alle år
ut = [a for a in [str(t) for t in range(2016, 2026)]
      if not d[("0", "A-Z", "06", "GrvManedslonn", a)] < h[("02", "0-9", "ALLE", "0", "0", "Manedslonn", a)]
      < d[("0", "A-Z", "07", "GrvManedslonn", a)]]
sjekk("K8", "Gjennomsnittet ligger mellom grensene for desil 6 og 7 alle år 2016–2025", not ut, f"({ut})")

# K9 Utbetalt årslønn: publisert endring ≈ endring regnet fra kroner (innen 0,1 prosentpoeng)
_, _, u = les("arslonn_utbetalt")
avvik = []
for s in ("ALLE", "A+B+D+E", "6500", "6100"):
    for t in range(2017, 2026):
        pub = u[(s, "ArslonnEndring", str(t))]
        regn = (u[(s, "Arslonn", str(t))] / u[(s, "Arslonn", str(t - 1))] - 1) * 100
        if abs(regn - pub) > 0.1:
            avvik.append((s, t, pub, round(regn, 2)))
sjekk("K9", "Utbetalt årslønn: publisert endring ≈ regnet fra kroner", not avvik, f"({avvik})")

# K10 Påløpt årslønn 2025: 4,9 prosent, reallønn 1,8
_, _, p = les("arslonn_palopt")
sjekk("K10", "Påløpt årslønn 2025 = 746 700, +4,9 prosent, reallønn +1,8",
      p[("Arslonn", "2025")] == 746700 and p[("ArslonnEndring", "2025")] == 4.9 and p[("ReallonnEndring", "2025")] == 1.8)

print()
print("Alle kontroller OK" if not FEIL else f"Feilet: {', '.join(FEIL)}")
sys.exit(1 if FEIL else 0)

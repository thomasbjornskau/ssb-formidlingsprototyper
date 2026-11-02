"""Kontroller av rådataene for arblonn (steg 3).

Leser data/raw/*.json og sjekker dem mot publiserte tall og mot hverandre.
Skriver største avvik per kontroll. Avslutter med feilkode hvis en kontroll
feiler. Bare Pythons standardbibliotek.

Fasit: statistikksiden ssb.no/arbeid-og-lonn/statistikker/arblonn, publisert
22.10.2026 (tabell 1–4), lest 30.10.2026.
"""
import itertools
import json
import sys
from pathlib import Path

ROT = Path(__file__).resolve().parents[1]
FEIL = []
N17 = ["01-03", "05-09", "10-33", "35-39", "41-43", "45-47", "49-53", "55-56", "58-63",
       "64-66", "68-75", "77-82", "84", "85", "86-88", "90-99", "00"]


def les(navn):
    d = json.loads((ROT / "data" / "raw" / f"{navn}.json").read_text(encoding="utf-8"))
    kat = []
    for i in d["id"]:
        idx = d["dimension"][i]["category"]["index"]
        kat.append(sorted(idx, key=idx.get))
    verdi = {k: d["value"][n] for n, k in enumerate(itertools.product(*kat))}
    status = {k: d.get("status", {}).get(str(n)) for n, k in enumerate(itertools.product(*kat))}
    return d["id"], kat, verdi, status


def sjekk(nr, tekst, ok, detalj=""):
    print(f"{nr:4} {'OK ' if ok else 'FEIL'} {tekst} {detalj}")
    if not ok:
        FEIL.append(nr)


def tosifret_til_17(kode):
    """Tosifret næringskode (SN2007) til gruppe i 17-inndelingen."""
    if kode == "00":
        return "00"
    n = int(kode)
    for g in N17[:-1]:
        a, _, b = g.partition("-")
        if int(a) <= n <= int(b or a):
            return g
    return None


# --- Tabellene ---
_, kq, q, sq = les("kvartal_naering")      # Region, NACE2007, ContentsCode, Tid
_, kf, f, sf = les("kvartal_fylke")        # Region, NACE2007, ContentsCode, Tid
_, km, m, sm = les("maned")                # NACE2007, ForelopigEndelig, ContentsCode, Tid
_, ka, a, sa = les("kjonn_alder")          # Region, Kjonn, Alder, ContentsCode, Tid
_, kt, t, st = les("arbeidstid")           # ArbeidsTidRen, NACE2007, Kjonn, ContentsCode, Tid
_, k8, e, s8 = les("naering88")            # NACE2007, ContentsCode, Tid
KV = kq[3]
MND = km[3]

# K1 Nøkkeltall mot statistikksiden
Q = lambda n, v, tid="2026K2": q[("Ialt", n, v, tid)]
sjekk("K1", "Jobber 2026K2 = 3 166 972 (tabell 4) og 3 166 971 (tabell 2)",
      Q("00-99", "AntArbForhold") == 3166972 and a[("Ialt", "0", "999A", "AntArbForhold", "2026K2")] == 3166971)
sjekk("K1b", "Lønnstakere 2026K2 = 2 839 248, avtalt månedslønn 58 970, median 53 650",
      Q("00-99", "Lonsstakere") == 2839248 and Q("00-99", "GjAvtaltMdlonn") == 58970
      and Q("00-99", "MedianAvtMndLonn") == 53650)

# K2 Sum av 17 næringer = alle næringer, jobber og lønnstakere, alle kvartaler
storst = 0
for v in ("AntArbForhold", "Lonsstakere"):
    for tid in KV:
        storst = max(storst, abs(sum(Q(n, v, tid) for n in N17) - Q("00-99", v, tid)))
sjekk("K2", "17 næringer summerer til alle næringer (jobber, lønnstakere)", storst == 0, f"største avvik {storst}")
# Heltidsekvivalenter er avrundet per næring. Toleranse 10, satt etter faktisk avvik 30.10.2026.
storst = max(abs(sum(Q(n, "HeltidsEkvMnd", tid) for n in N17) - Q("00-99", "HeltidsEkvMnd", tid)) for tid in KV)
sjekk("K2b", "17 næringer summerer til alle næringer (heltidsekvivalenter)", storst <= 10, f"største avvik {storst}")

# K3 15 fylker + uoppgitt + ikke Fastlands-Norge = landet, jobber, fra 2024K1
storst = 0
for tid in kf[3]:
    for n in ["00-99"] + N17:
        s = sum((f[(r, n, "AntArbForhold", tid)] or 0) for r in kf[0])
        storst = max(storst, abs(s - Q(n, "AntArbForhold", tid)))
sjekk("K3", "Fylker summerer til landet for alle næringer, 2024K1–2026K2", storst <= 3,
      f"største avvik {storst} (skjulte celler i «uoppgitt»)")
for r in ("31", "32", "33", "39", "40", "55", "56"):
    pass
# fylker som er 0 før 2024 i inndelingen, kontrollert i steg 3 med eget kall
sjekk("K3b", "Ingen 0 eller manglende for 15 fylker × 17 næringer (unntatt «00») fra 2024K1",
      all((f[(r, n, "AntArbForhold", tid)] or 0) > 0 for r in kf[0][:15] for n in N17[:-1] for tid in kf[3]))

# K4 Kjønn og alder summerer
storst = 0
for tid in KV:
    for kj in ("0", "1", "2"):
        s = sum(a[("Ialt", kj, al, "AntArbForhold", tid)] for al in ka[2][1:])
        storst = max(storst, abs(s - a[("Ialt", kj, "999A", "AntArbForhold", tid)]))
    s = a[("Ialt", "1", "999A", "AntArbForhold", tid)] + a[("Ialt", "2", "999A", "AntArbForhold", tid)]
    storst = max(storst, abs(s - a[("Ialt", "0", "999A", "AntArbForhold", tid)]))
sjekk("K4", "Aldersgrupper og kjønn summerer til totalen (jobber, 11652)", storst <= 2, f"største avvik {storst}")

# K5 Heltid + deltid = i alt
storst = 0
for tid in kt[4]:
    for n in ["00-99"] + N17:
        for kj in ("0", "1", "2"):
            h, d_, ia = (t[(x, n, kj, "AntJobber", tid)] for x in ("H", "D", "H+D"))
            if None in (h, d_, ia):
                continue
            storst = max(storst, abs(h + d_ - ia))
sjekk("K5", "Heltid + deltid = i alt (jobber, 13871)", storst <= 2, f"største avvik {storst}")
# Toleranse 10: tabellene avviker med 0–9 jobber per kvartal (avrunding/anonymisering, målt 30.10.2026).
storst = max(abs(t[("H+D", "00-99", "0", "AntJobber", tid)] - Q("00-99", "AntArbForhold", tid)) for tid in KV)
sjekk("K5b", "13871 i alt ≈ 11654 (jobber, alle næringer, alle kvartaler)", storst <= 10, f"største avvik {storst}")

# K6 88 næringer aggregert til 17 = 11654
storst, ukjent = 0, [k for k in k8[0] if k != "00-99" and tosifret_til_17(k) is None]
for tid in k8[2]:
    agg = {}
    for k in k8[0]:
        if k == "00-99":
            continue
        g = tosifret_til_17(k)
        agg[g] = agg.get(g, 0) + (e[(k, "AntArbForhold", tid)] or 0)
    for g in N17:
        storst = max(storst, abs(agg.get(g, 0) - Q(g, "AntArbForhold", tid)))
# Toleranse 15: 567 av 756 celler avviker med 1–11 jobber uten skjulte celler (anonymisering, målt 30.10.2026).
sjekk("K6", "Tosifrede næringer (12314) summerer til 17 grupper (11654)", storst <= 15 and not ukjent,
      f"største avvik {storst}, koder uten gruppe: {ukjent}")

# K7 Lønnsindeks = snitt / snitt 2024K1 × 100
storst = 0
for n in ["00-99"] + N17[:-1]:
    for tid in KV:
        for v, iv in (("GjAvtaltMdlonn", "GjAvtaltMdlonnIndeks"), ("GjMdTotal", "GjMdTotalIndeks")):
            beregnet = Q(n, v, tid) / Q(n, v, "2024K1") * 100
            storst = max(storst, abs(round(beregnet, 1) - Q(n, iv, tid)))
sjekk("K7", "Lønnsindeks = snitt / snitt 2024K1 × 100, alle næringer og kvartaler", storst <= 0.11,
      f"største avvik {storst:.2f} indekspoeng")

# K8 Publiserte endringer i månedstall (tabell 1)
M = lambda n, ver, v, tid: m[(n, ver, v, tid)]
endr = lambda ver, v, fra, til: M("00-99", ver, v, til) - M("00-99", ver, v, fra)
sjekk("K8", "Aug–sep 2026 foreløpig: +24 775 jobber, +18 604 lønnstakere, +170 kr",
      (endr("01", "AntArbForholdSesong", "2026M08", "2026M09"), endr("01", "AntLonnstakSesong", "2026M08", "2026M09"),
       endr("01", "GjsnKontantlonn", "2026M08", "2026M09")) == (24775, 18604, 170))
sjekk("K8b", "Jul–aug 2026 endelig: +3 502 jobber, +750 lønnstakere, +200 kr",
      (endr("02", "AntArbForholdSesong", "2026M07", "2026M08"), endr("02", "AntLonnstakSesong", "2026M07", "2026M08"),
       endr("02", "GjsnKontantlonn", "2026M07", "2026M08")) == (3502, 750, 200))

# K9 Sesongjusterte og ujusterte næringstall summerer til totalen
# Sesongjustert: totalen er summen av de sesongjusterte næringene (indirekte, «Nye sesongjusterte jobbtall», SSB 2021).
# Toleranse 5 for avrunding av 18 serier, største faktiske avvik 5 (30.10.2026).
for v, tol in (("AntArbForhold", 0), ("AntArbForholdSesong", 5)):
    storst = 0
    for ver in ("01", "02"):
        for tid in MND:
            tot = M("00-99", ver, v, tid)
            if tot is None:
                continue
            storst = max(storst, abs(sum(M(n, ver, v, tid) or 0 for n in N17) - tot))
    sjekk("K9" + ("b" if "Sesong" in v else ""), f"Næringer summerer til totalen, {v}", storst <= tol,
          f"største avvik {storst}")

# K10 Midtmåneden i kvartalet (endelig, ujustert) = kvartalstallet
# Toleranse 15. Kjent avvik: 2024K4 / 2024M11 = −305 jobber (målt 30.10.2026). Står i kildekartet.
KJENT_K10 = {"2024K4": -305}
storst = 0
for tid in KV:
    if tid in KJENT_K10:
        mnd = "2024M11"
        sjekk("K10b", "Kjent avvik 2024M11 mot 2024K4 er uendret", 
              M("00-99", "02", "AntArbForhold", mnd) - Q("00-99", "AntArbForhold", tid) == KJENT_K10[tid])
        continue
    mnd = tid[:4] + "M" + {"K1": "02", "K2": "05", "K3": "08", "K4": "11"}[tid[4:]]
    if mnd in MND and M("00-99", "02", "AntArbForhold", mnd) is not None:
        storst = max(storst, abs(M("00-99", "02", "AntArbForhold", mnd) - Q("00-99", "AntArbForhold", tid)))
sjekk("K10", "Endelig midtmåned (13126) = kvartalstall (11654), jobber, utenom kjent avvik", storst <= 15, f"største avvik {storst}")

# K11 Vekst regnet fra kroner og jobber = publiserte endringer per næring (tabell 4)
publ_lonn = [3.9, 4.6, 4.0, 4.6, 4.0, 4.3, 3.6, 3.5, 3.4, 4.5, 4.3, 4.2, 3.7, 4.6, 3.8, 3.6, 3.9, 6.2]
publ_jobb = [0.8, 1.3, 0.5, 0.6, -0.3, -1.2, 0.9, 2.5, 2.1, -0.4, -0.5, 0.5, 1.0, 2.6, -0.5, 1.1, 1.7, -1.0]
treff_l = treff_j = 0
for n, pl, pj in zip(["00-99"] + N17, publ_lonn, publ_jobb):
    vl = (Q(n, "GjAvtaltMdlonn") / Q(n, "GjAvtaltMdlonn", "2025K2") - 1) * 100
    vj = (Q(n, "AntArbForhold") / Q(n, "AntArbForhold", "2025K2") - 1) * 100
    treff_l += abs(round(vl, 1) - pl) < 0.05
    treff_j += abs(round(vj, 1) - pj) < 0.05
sjekk("K11", "Lønnsvekst fra kroner = publisert, 18 næringskoder", treff_l == 18, f"{treff_l} av 18")
sjekk("K11b", "Jobbvekst fra antall = publisert, 18 næringskoder", treff_j == 18, f"{treff_j} av 18")
iv = (Q("00-99", "GjAvtaltMdlonnIndeks") / Q("00-99", "GjAvtaltMdlonnIndeks", "2025K2") - 1) * 100
sjekk("K11c", "Fallgruve: vekst fra avrundet indeks avviker fra publisert 3,9", round(iv, 1) != 3.9,
      f"indeksen gir {round(iv, 1)}")

# K12 Foreløpige tall finnes fra 2016M01, endelige til nest siste måned
forste_f = next(tid for tid in MND if M("00-99", "01", "AntArbForhold", tid) is not None)
siste_e = [tid for tid in MND if M("00-99", "02", "AntArbForhold", tid) is not None][-1]
sjekk("K12", "Foreløpige fra 2016M01, endelige til 2026M08", (forste_f, siste_e) == ("2016M01", "2026M08"),
      f"{forste_f}, {siste_e}")

# K13 Før 2016 har månedstabellen bare sesongjusterte jobber og lønnstakere.
# Ujusterte lønnstakere og kontantlønn (begge former) starter 2016M01.
for v in ("Lonsstakere", "GjKontLonn", "GjsnKontantlonn"):
    forste = next(tid for tid in MND if M("00-99", "02", v, tid) is not None)
    sjekk("K13", f"{v}: endelige tall fra 2016M01", forste == "2016M01", forste)
forste = next(tid for tid in MND if M("00-99", "02", "AntArbForholdSesong", tid) is not None)
sjekk("K13b", "Jobber, sesongjustert: endelige tall fra 2003M05", forste == "2003M05", forste)
forste = next(tid for tid in MND if M("00-99", "02", "AntLonnstakSesong", tid) is not None)
sjekk("K13c", "Lønnstakere, sesongjustert: endelige tall fra 2003M05", forste == "2003M05", forste)

# Symboler som brukes i dataene
for navn, s in (("maned", sm), ("kvartal_naering", sq), ("kvartal_fylke", sf), ("kjonn_alder", sa),
                ("arbeidstid", st), ("naering88", s8)):
    teller = {}
    for v in s.values():
        if v:
            teller[v] = teller.get(v, 0) + 1
    print(f"     symboler i {navn}: {teller or 'ingen'}")

if FEIL:
    sys.exit(f"Kontroll feilet: {', '.join(FEIL)}")
print("Alle kontroller OK")

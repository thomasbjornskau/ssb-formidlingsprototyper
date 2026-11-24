"""Lager konseptgrafikk (bred og smal) og toppgrafikk A, B og C for overnatting.

Kjøres fra overnatting/: python3 scripts/lag_grafikk.py
Tallene leses fra data/grafikk-utkast.json (steg 2). I steg 3 byttes kilden til data/raw/.
"""
import json
import os
import sys

HER = os.path.dirname(os.path.abspath(__file__))
ROT = os.path.dirname(HER)
sys.path.insert(0, HER)
from grafikk_overnatting import Svg, nb, sgn, bryt, F_TITTEL, F_OVERSKRIFT, F_TEKST  # noqa: E402

# Konseptfigurpalett (ssb-konseptfigurer)
MORK5, MORK1, MORK2 = "#274247", "#f0f8f9", "#c3dcdc"
GRONN4, GRONN2, GRONN1 = "#00824d", "#b6e8b8", "#ecfeed"
LILLA3, LILLA2, LILLA1, LILLATEKST = "#7e5ee8", "#d2ceff", "#f2f0ff", "#4b2fb0"
GRATEKST, GRALINJE = "#5e787a", "#cdd3d4"
GRA_STREK, GRA_FYLL = "#b9c5c6", "#f3f5f5"
# Diagrampalett (ssb-diagramstandard)
STOTTE, NULL = "#d9dfe0", "#a9b5b7"
BLA_FLATE = "#3face6"
GRONN_FLATE = "#339b71"

D = json.load(open(os.path.join(ROT, "data", "grafikk-utkast.json"), encoding="utf-8"))["serier"]


def verdier(nokkel, **filter_):
    s = D[nokkel]
    ut = {}
    for v in s["verdier"]:
        k = dict(zip(s["dims"], v["koder"]))
        if all(k[a] == b for a, b in filter_.items()):
            ut[k["Tid"]] = v["verdi"]
    return ut


# ---------------------------------------------------------------- tall
HOT_SEP = verdier("hotell_september")
SA = verdier("hotell_sesongjustert", ContentsCode="OvernattingerSesongj")
END = {}
for v in D["sept_endring"]["verdier"]:
    k = dict(zip(D["sept_endring"]["dims"], v["koder"]))
    END.setdefault((k["InnKvartering1"], k["Landkoder2"]), {})[k["Tid"]] = v["verdi"]
DIFF = {k: t["2026M09"] - t["2025M09"] for k, t in END.items()}
RU = {}
for v in D["reiseundersokelsen_2025"]["verdier"]:
    RU[v["koder"][0]] = RU.get(v["koder"][0], 0) + (v["verdi"] or 0)
NORSKE_KOMM_2025 = sum(v["verdi"] for v in D["norske_kommersielle_2025"]["verdier"])

KOMM_SEP26 = 3448079     # 14162, I alt, heile landet, 2026M09 (sjekket i steg 1)
FRITID_SEP26 = 77403     # 13100, 2026M09 (sjekket i steg 1)

# ---------------------------------------------------------------- konseptgrafikk
TRINN = [
    dict(tittel="Gjesten sjekker inn",
         tekst="Bedriften registrerer hver person og hver natt, og hvilket land gjesten bor i. "
               "Det er bostedet som teller, ikke passet.",
         boks=dict(type="eksempel",
                   etikett="Eksempeltall, ikke statistikk",
                   tekst="Et par som bor i Tyskland, sover 3 netter på hotell i Bergen og 2 netter "
                         "på en campingplass i Lofoten.",
                   uthevet="= 10\u00a0overnattinger og 4\u00a0ankomne gjester")),
    dict(tittel="Bedriften rapporterer",
         tekst="Hver måned i Altinn, på skjema eller rett fra bookingsystemet. "
               "Fristen er 10 dager etter månedsslutt.",
         boks=dict(type="fakta",
                   etikett="Disse rapporterer",
                   tekst="Alle hotell · campingplasser med minst 20 enheter · hyttegrender med minst "
                         "10 senger · alle vandrerhjem · 42 norske formidlere av fritidsboliger",
                   uthevet="Hotellene oppgir også formål, rom, senger og losjiomsetning")),
    dict(tittel="SSB kontrollerer og beregner",
         tekst="Tallene sjekkes for feil. Om lag 2 prosent svarer ikke, og overnattingene deres "
               "anslås ut fra bedrifter som har svart.",
         boks=dict(type="fakta",
                   etikett="Camping, ny metode fra februar 2026",
                   tekst="Vet plassen bare hvor mange sesongkontrakter som er i bruk, beregner SSB "
                         "overnattingene med faste faktorer per måned og fylke.",
                   uthevet="Vær og etterspørsel kommer ikke med")),
    dict(tittel="Tallene publiseres",
         tekst="3–4 uker etter månedsslutt, for landet, fylker, 66 reiselivsregioner og kommuner. "
               "Tall fra færre enn tre bedrifter vises som «:».",
         boks=dict(type="tall",
                   etikett="September 2026",
                   tekst=f"{nb(KOMM_SEP26)} overnattinger ved kommersielle bedrifter, og "
                         f"{nb(FRITID_SEP26)} i fritidsboliger via formidler",
                   uthevet="Land og fylker får også sesongjusterte tall")),
]

IKKE_MED = [
    ("Egen hytte, familie og venner",
     f"Nordmenn hadde {nb(RU['75'], 1)} millioner ikke-kommersielle overnattinger på reiser i Norge "
     "i 2025 (Reiseundersøkelsen)."),
    ("Airbnb, Booking og lignende",
     "6,4 millioner overnattinger i norske boliger og fritidsboliger i 2023 (eksperimentell "
     "statistikk fra Eurostat)."),
    ("Resten utenfor grensene",
     "Bobil og telt utenfor campingplass, cruiseskip, og campingplasser og hyttegrender under "
     "størrelsesgrensene."),
]
KONSEPT_KILDE = ("Kilde: SSB, Om statistikken for Overnattingar (oppdatert 9.9.2026), tabell 14162, "
                 "13100 og 11270. Eurostat, plattformstatistikk.")

BOKSFARGER = {"eksempel": (LILLA1, LILLA2, LILLATEKST),
              "fakta": (GRONN1, GRONN2, GRONN4),
              "tall": (GRONN1, GRONN2, GRONN4)}


def tegn_trinn(s, x, y, b, nr, t, hoyde=None, dry=False):
    """Tegner ett trinn. Returnerer høyden. Med dry=True tegnes ingenting."""
    pad = 16
    indre = b - 2 * pad
    tittellinjer = bryt(t["tittel"], indre - 40, 18, 700, "roboto")
    yy = y + 64 + (len(tittellinjer) - 1) * 22
    tekstlinjer = bryt(t["tekst"], indre, 15)
    yy += len(tekstlinjer) * 22 + 10
    bk = t["boks"]
    et = bryt(bk["etikett"], indre - 24, 14, 600)
    tk = bryt(bk["tekst"], indre - 24, 14)
    ut = bryt(bk["uthevet"], indre - 24, 14, 700)
    boks_h = 14 + len(et) * 20 + 4 + len(tk) * 20 + 6 + len(ut) * 20 + 8
    total = (yy - y) + boks_h + pad
    if dry:
        return total
    h = hoyde or total
    s.rect(x, y, b, h, fyll=MORK1, strek=MORK2, r=2)
    s.markor(x + pad + 15, y + 30, nr)
    s.tekstblokk(x + pad + 40, y + 36, t["tittel"], indre - 40, 18, 22, fyll=MORK5, vekt=700,
                 familie=F_OVERSKRIFT)
    ty = y + 78 + (len(tittellinjer) - 1) * 22 + (6 if len(tittellinjer) > 1 else 0)
    for ln in tekstlinjer:
        s.text(x + pad, ty, ln, 15, MORK5)
        ty += 22
    # boksen legges i bunnen av trinnet, slik at alle bokser flukter
    fyll, strek, tf = BOKSFARGER[bk["type"]]
    by = y + h - pad - boks_h
    s.rect(x + pad, by, indre, boks_h, fyll=fyll, strek=strek, r=2)
    s.rect(x + pad, by, 4, boks_h, fyll=tf if bk["type"] != "eksempel" else LILLA3)
    yy = by + 22
    for ln in et:
        s.text(x + pad + 14, yy, ln, 14, tf, 600)
        yy += 20
    yy += 4
    for ln in tk:
        s.text(x + pad + 14, yy, ln, 14, MORK5)
        yy += 20
    yy += 6
    for ln in ut:
        s.text(x + pad + 14, yy, ln, 14, MORK5, 700)
        yy += 20
    return h


def tegn_ikke_med(s, x, y, b, kolonner):
    pad = 18
    s_h_kol = []
    kb = (b - 2 * pad - (kolonner - 1) * 24) / kolonner
    for tittel, tekst in IKKE_MED:
        s_h_kol.append(22 + len(bryt(tekst, kb, 14)) * 20)
    if kolonner == 1:
        h = 52 + sum(s_h_kol) + 12 * (len(IKKE_MED) - 1) + pad
    else:
        h = 52 + max(s_h_kol) + pad
    s.rect(x, y, b, h, fyll=GRA_FYLL, strek=GRA_STREK, sb=1.5, r=2, stiplet="6 4")
    s.text(x + pad, y + 32, "Ikke med i overnattingsstatistikken", 17, MORK5, 700, F_OVERSKRIFT)
    yy = y + 62
    for i, (tittel, tekst) in enumerate(IKKE_MED):
        if kolonner > 1:
            kx, ky = x + pad + i * (kb + 24), yy
        else:
            kx, ky = x + pad, yy
        s.text(kx, ky, tittel, 14, MORK5, 700)
        ny = s.tekstblokk(kx, ky + 22, tekst, kb, 14, 20, fyll=MORK5)
        if kolonner == 1:
            yy = ny + 12
    return h


def konsept_bred():
    B = 1200
    x0, gap, n = 30, 40, 4
    b = (B - 2 * x0 - (n - 1) * gap) / n
    tmp = Svg(B, 10)
    h = max(tegn_trinn(tmp, 0, 0, b, i + 1, t, dry=True) for i, t in enumerate(TRINN))
    y0 = 96
    # høyde på ikke-med-boksen
    probe = Svg(B, 10)
    ikke_h = tegn_ikke_med(probe, x0, 0, B - 2 * x0, 3)
    H = y0 + h + 28 + ikke_h + 56
    s = Svg(B, H, tittel="Slik lages tallene i Overnattingar",
            beskrivelse="Fire trinn fra gjesten sjekker inn til tallene publiseres, og hva som ikke er med.")
    s.text(x0, 44, "Slik lages tallene", 30, MORK5, 700, F_TITTEL)
    s.text(x0, 72, "Fra resepsjonen til statistikkbanken, hver måned", 16, GRATEKST)
    for i, t in enumerate(TRINN):
        x = x0 + i * (b + gap)
        tegn_trinn(s, x, y0, b, i + 1, t, hoyde=h)
        if i < n - 1:
            s.pil(x + b + 6, y0 + 30, x + b + gap - 6, y0 + 30, MORK5)
    tegn_ikke_med(s, x0, y0 + h + 28, B - 2 * x0, 3)
    s.text(x0, H - 22, KONSEPT_KILDE, 14, GRATEKST)
    s.lagre(os.path.join(ROT, "src", "konsept-bred.svg"))


def konsept_smal():
    B = 390
    x0 = 16
    b = B - 2 * x0
    tmp = Svg(B, 10)
    hs = [tegn_trinn(tmp, 0, 0, b, i + 1, t, dry=True) for i, t in enumerate(TRINN)]
    probe = Svg(B, 10)
    ikke_h = tegn_ikke_med(probe, x0, 0, b, 1)
    kilde = bryt(KONSEPT_KILDE, b, 14)
    gap = 36
    y0 = 112
    H = y0 + sum(hs) + gap * 3 + 28 + ikke_h + 24 + len(kilde) * 20 + 10
    s = Svg(B, H, tittel="Slik lages tallene i Overnattingar",
            beskrivelse="Fire trinn fra gjesten sjekker inn til tallene publiseres, og hva som ikke er med.")
    s.text(x0, 42, "Slik lages tallene", 28, MORK5, 700, F_TITTEL)
    s.tekstblokk(x0, 70, "Fra resepsjonen til statistikkbanken, hver måned", b, 16, 22, fyll=GRATEKST)
    y = y0
    for i, t in enumerate(TRINN):
        tegn_trinn(s, x0, y, b, i + 1, t, hoyde=hs[i])
        y += hs[i]
        if i < 3:
            s.pil(x0 + 31, y + 4, x0 + 31, y + gap - 4, MORK5)
            y += gap
    y += 28
    tegn_ikke_med(s, x0, y, b, 1)
    y += ikke_h + 30
    for ln in kilde:
        s.text(x0, y, ln, 14, GRATEKST)
        y += 20
    s.lagre(os.path.join(ROT, "src", "konsept-smal.svg"))


# ---------------------------------------------------------------- toppgrafikk
def topp_tekst(s, etikett, stort, setning, linjer):
    x = 40
    s.text(x, 46, etikett, 14, GRATEKST, 600)
    s.text(x, 112, stort, 60, MORK5, 700, tall=True)
    y = s.tekstblokk(x, 148, setning, 470, 19, 26, fyll=MORK5)
    y += 8
    for ln in linjer:
        s.rect(x, y - 11, 3, 14, fyll=GRONN4)
        y = s.tekstblokk(x + 12, y, ln, 458, 15, 21, fyll=GRATEKST) + 4


def kildelinje(s, tekst):
    s.text(1160, 314, tekst, 13, GRATEKST, anker="end")


def topp_a():
    s = Svg(1200, 330, tittel="Toppgrafikk A: rekord, men ikke opp",
            beskrivelse="Hotellovernattinger i september 2016–2026 og sesongjustert utvikling okt. 2024–sept. 2026.")
    sep26, sep25 = HOT_SEP["2026M09"], HOT_SEP["2025M09"]
    aug, sep = SA["2026M08"], SA["2026M09"]
    topp_tekst(s, "OVERNATTINGAR · HOTELL · SEPTEMBER 2026",
               f"{nb(sep26 / 1e6, 1)} millioner",
               "hotellovernattinger, flest i en september noen gang. Men justert for sesong var det "
               "litt færre enn i august.",
               [f"{sgn(100 * (sep26 / sep25 - 1), 1)} prosent fra september 2025",
                f"{sgn(100 * (sep / aug - 1), 1)} prosent fra august 2026, sesongjustert"])
    # panel 1: september hvert år
    px, py, pb, ph = 600, 86, 258, 180
    s.text(px, 52, "Hver september", 14, MORK5, 700)
    s.text(px, 72, "millioner overnattinger", 13, GRATEKST)
    maks = 3.0
    for g in (0, 1, 2, 3):
        yy = py + ph - g / maks * ph
        s.line(px + 18, yy, px + pb, yy, NULL if g == 0 else STOTTE, 1)
        s.text(px + 10, yy + 4, nb(g), 13, GRATEKST, anker="end", tall=True)
    ar = list(range(2016, 2027))
    slot = (pb - 24) / len(ar)
    bw = slot / 1.5
    for i, a in enumerate(ar):
        v = HOT_SEP[f"{a}M09"] / 1e6
        x = px + 24 + i * slot + (slot - bw) / 2
        y = py + ph - v / maks * ph
        s.rect(x, y, bw, py + ph - y, fyll=GRONN4 if a == 2026 else GRA_STREK)
        if a in (2016, 2020, 2026):
            s.text(x + bw / 2, py + ph + 18, str(a), 13, GRATEKST, anker="middle", tall=True)
        if a == 2026:
            s.text(x + bw, y - 8, nb(HOT_SEP["2026M09"]), 13, MORK5, 700, anker="end", tall=True)
        if a == 2020:
            bx = x - (slot - bw) / 2
            s.line(bx, py - 6, bx, py + ph, GRATEKST, 1, stiplet="4 3")
            s.text(bx + 4, py + 4, "brudd", 12, GRATEKST)
    # panel 2: sesongjustert
    qx, qb = 900, 260
    s.text(qx, 52, "Sesongjustert, per måned", 14, MORK5, 700)
    s.text(qx, 72, "millioner overnattinger", 13, GRATEKST)
    lo, hi = 2.2, 2.5
    for g in (2.2, 2.3, 2.4, 2.5):
        yy = py + ph - (g - lo) / (hi - lo) * ph
        s.line(qx + 28, yy, qx + qb - 100, yy, STOTTE, 1)
        s.text(qx + 22, yy + 4, nb(g, 1), 13, GRATEKST, anker="end", tall=True)
    ks = sorted(SA)
    pkt = []
    for i, k in enumerate(ks):
        x = qx + 34 + i * (qb - 140) / (len(ks) - 1)
        y = py + ph - (SA[k] / 1e6 - lo) / (hi - lo) * ph
        pkt.append((x, y))
    s.polyline(pkt, GRONN4, 2)
    for k in ("2026M08", "2026M09"):
        x, y = pkt[ks.index(k)]
        s.circle(x, y, 3.5, GRONN4)
    xs, ys = pkt[-1]
    xa, ya = pkt[-2]
    s.text(xs + 10, ya - 6, f"aug. {nb(SA['2026M08'])}", 13, GRATEKST, tall=True)
    s.text(xs + 10, ys + 14, f"sept. {nb(SA['2026M09'])}", 13, MORK5, 700, tall=True)
    for aar in ("2025", "2026"):
        x = pkt[ks.index(aar + "M01")][0]
        s.line(x, py + ph, x, py + ph + 4, NULL, 1)
        s.text(x, py + ph + 18, aar, 13, GRATEKST, anker="middle", tall=True)
    kildelinje(s, "Kilde: SSB, tabell 14162 og 14178. Sist oppdatert: 4.11.2026.")
    s.lagre(os.path.join(ROT, "docs", "grafikk", "02-topp-a.svg"))


def topp_b():
    s = Svg(1200, 330, tittel="Toppgrafikk B: 7 av 10 netter er ikke med",
            beskrivelse="Nordmenns overnattinger på reiser i Norge 2025 etter innkvarteringstype, og norske "
                        "overnattinger i overnattingsstatistikken.")
    tot, ikke = RU["00"], RU["75"]
    komm = RU["10"] + RU["20"] + RU["30"]
    andel = round(10 * ikke / tot)
    topp_tekst(s, "REISEUNDERSØKELSEN OG OVERNATTINGAR · 2025",
               f"{andel} av 10",
               "netter nordmenn sov borte på reiser i Norge, var i ikke-kommersiell innkvartering. "
               "De er ikke med i overnattingsstatistikken.",
               [f"{nb(ikke, 1)} av {nb(tot, 1)} millioner overnattinger, ifølge Reiseundersøkelsen",
                "Overnattingsstatistikken teller hotell, camping, hyttegrender, vandrerhjem og "
                "formidlede fritidsboliger"])
    px, pb = 600, 560
    k = pb / tot
    # søyle 1
    s.text(px, 52, "Nordmenns overnattinger på reiser i Norge", 14, MORK5, 700)
    s.text(px, 72, "Reiseundersøkelsen, millioner overnattinger", 13, GRATEKST)
    y1, bh = 98, 46
    s.rect(px, y1, komm * k, bh, fyll=GRONN4)
    s.rect(px + komm * k, y1, ikke * k, bh, fyll=GRALINJE)
    s.text(px + 10, y1 + 29, nb(komm, 1), 15, "#ffffff", 700, tall=True)
    s.text(px + komm * k + 12, y1 + 29, f"Ikke-kommersiell: {nb(ikke, 1)}", 15, MORK5, 700, tall=True)
    s.text(px, y1 + bh + 20, "Hotell, camping og annen", 13, MORK5)
    s.text(px, y1 + bh + 37, "kommersiell innkvartering", 13, MORK5)
    s.text(px + pb, y1 + bh + 20, f"I alt {nb(tot, 1)}", 13, GRATEKST, anker="end", tall=True)
    # søyle 2
    y2 = 228
    s.text(px, y2 - 10, "Norske overnattinger i overnattingsstatistikken", 14, MORK5, 700)
    v2 = NORSKE_KOMM_2025 / 1e6
    s.rect(px, y2, v2 * k, 30, fyll=GRONN4)
    s.text(px + v2 * k + 8, y2 + 21, nb(v2, 1), 15, MORK5, 700, tall=True)
    s.text(px, y2 + 50, "To undersøkelser med ulike metoder. Bruk dem til å se størrelsene, ikke til å "
                       "regne differanser.", 13, GRATEKST)
    s.line(px, y1 - 6, px, y2 + 36, NULL, 1)
    kildelinje(s, "Kilde: SSB, tabell 11270 (sist oppdatert 27.8.2026) og 14162 (sist oppdatert 4.11.2026).")
    s.lagre(os.path.join(ROT, "docs", "grafikk", "02-topp-b.svg"))


def topp_c():
    s = Svg(1200, 330, tittel="Toppgrafikk C: utlendinger på hotell driver veksten",
            beskrivelse="Endring i overnattinger fra september 2025 til september 2026 etter "
                        "innkvarteringstype og bostedsland.")
    total = sum(DIFF.values())
    camping = DIFF[("02", "000")] + DIFF[("02", "ccc")]
    utl_hot = DIFF[("01", "ccc")]
    topp_tekst(s, "OVERNATTINGAR · SEPTEMBER 2026 MOT SEPTEMBER 2025",
               f"+{nb(round(utl_hot, -3) / 1000)} 000",
               f"flere utenlandske hotellovernattinger. Det er mer enn hele veksten i kommersielle "
               f"overnattinger, som var {sgn(total)}.",
               [f"Campingplassene hadde {nb(-camping)} færre overnattinger",
                "Utenlandske gjester registreres etter landet de bor i"])
    grupper = [("Hotell", "01"), ("Hyttegrender og vandrerhjem", "03+04"), ("Camping", "02")]
    px = 600
    s.text(px, 52, "Endring i antall overnattinger", 14, MORK5, 700)
    s.text(px, 72, "fra september 2025 til september 2026", 13, GRATEKST)
    lo = min(DIFF.values())
    hi = max(DIFF.values())
    x_null = 880
    k = (1150 - 80 - x_null) / hi
    if x_null - (-lo) * k < 790:
        k = min(k, (x_null - 790) / -lo)
    y = 92
    rad_h, bh = 31, 18
    for gnavn, kode in grupper:
        s.text(px, y + 16, gnavn, 14, MORK5, 700)
        y += 22
        for lnavn, l, farge in (("Utenlandske", "ccc", BLA_FLATE), ("Norske", "000", GRONN_FLATE)):
            v = DIFF[(kode, l)]
            s.text(px + 14, y + 14, lnavn, 14, MORK5)
            if v >= 0:
                s.rect(x_null, y, v * k, bh, fyll=farge)
                s.text(x_null + v * k + 6, y + 14, sgn(v), 13, MORK5, 600, tall=True)
            else:
                s.rect(x_null + v * k, y, -v * k, bh, fyll=farge)
                s.text(x_null + v * k - 6, y + 14, sgn(v), 13, MORK5, 600, anker="end", tall=True)
            y += rad_h - 9
        y += 4
    s.line(x_null, 88, x_null, y - 6, NULL, 1)
    kildelinje(s, "Kilde: SSB, tabell 14162. Sist oppdatert: 4.11.2026.")
    s.lagre(os.path.join(ROT, "docs", "grafikk", "02-topp-c.svg"))


if __name__ == "__main__":
    konsept_bred()
    konsept_smal()
    topp_a()
    topp_b()
    topp_c()
    print("Ferdig: 5 SVG-er")

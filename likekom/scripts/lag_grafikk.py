"""Steg 2 for likekom: konseptgrafikk og tre varianter av hovedgrafikken.

Bare standardbiblioteket. Leser data/grafikk-utkast.json og src/ikon-115.svg.
Uttrykket følger filmen (ET Book, papirhvit bunn, sort skår, rødt og blått
bare på grunnlagstallene) og avviker bevisst fra ssb-konseptfigurer.
"""
import json, math, re, pathlib

ROT = pathlib.Path(__file__).resolve().parents[1]
D = json.load(open(ROT / "data/grafikk-utkast.json", encoding="utf-8"))
S, G = D["skar"], D["grunnlag"]
IKON = re.search(r"<svg[^>]*>(.*)</svg>", (ROT / "src/ikon-115.svg").read_text(), re.S).group(1)

PAPIR, SORT, GRAA, LYS, KV, MA = "#fffff8", "#111111", "#55554e", "#c9c9bf", "#DC3400", "#0D81CF"
MAKSV = 40  # grader ved skår 0

def nb(v, d=1):
    return ("−" if v < 0 else "") + f"{abs(v):.{d}f}".replace(".", ",")
def kr(v):
    return f"{round(v):,}".replace(",", " ")

# navn, kode, gruppe, type, (kvinner, menn)
IND = [
 ("Barnehage", "Barnehage", 0, "andel", G["Barnehage"]),
 ("Utdanningsprogram", "UtdanningVGS", 0, "skar", None),
 ("Næringsstruktur", "Naringsstruktur", 0, "skar", None),
 ("Offentlig sektor", "OffentligSektor", 0, "pst", (G["KvinnerOffentligSyss"], G["MennOffentligSyss"])),
 ("Privat sektor", "PrivatSektor", 0, "pst", (G["KvinnerPrivatSyss"], G["MennPrivatSyss"])),
 ("Arbeidsstyrke", "Arbeid", 1, "pst", (G["KvinnerTjueSekstisek"], G["MennTjueSekstiseks"])),
 ("Deltid", "Deltidsarbeid", 1, "pst", (G["KvinnerDeltid"], G["MennDeltid"])),
 ("Fedrekvote", "Fedrekvote", 1, "andel", G["Fedrekvote"]),
 ("Utdanningsnivå", "UtdNiva", 2, "pst", (G["UtdKvinner"], G["UtdMenn"])),
 ("Ledere", "Ledere", 2, "pst", (G["KvinnerLedere"], G["MennLedere"])),
 ("Kommunestyre", "KomRepresentant", 3, "pst", (G["KomRepresentant"], G["KomReprMenn"])),
 ("Inntekt", "InntektBrutto", 4, "kr", (G["BruttoKvinner"], G["BruttoMenn"])),
]
GRUPPER = [("Rammer", 0, 4), ("Arbeid og omsorg", 5, 7), ("Ressurser", 8, 9), ("Politikk", 10, 10), ("Penger", 11, 11)]

class Svg:
    def __init__(self, w, h, fontsti, pre=""):
        self.w, self.h, self.e, self.pre = w, h, [], pre
        self.hode = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            '<style>' + ('' if fontsti is None else f'@font-face{{font-family:"ETB";src:url("{fontsti}et-book-roman-old-style-figures.ttf")}}'
            f'@font-face{{font-family:"ETB";font-style:italic;src:url("{fontsti}et-book-display-italic-old-style-figures.ttf")}}'
            f'@font-face{{font-family:"ETL";src:url("{fontsti}et-book-roman-line-figures.ttf")}}') +
            'text{font-family:"ETB",Palatino,"Palatino Linotype",Georgia,serif;fill:#111111}'
            '.t{font-family:"ETL",Palatino,Georgia,serif}.i{font-style:italic;fill:#55554e}.g{fill:#55554e}'
            '.sc{text-transform:uppercase;letter-spacing:.14em;fill:#85857c}</style>'
            f'<defs><clipPath id="{pre}kk"><rect x="0" y="0" width="40" height="80"/></clipPath><clipPath id="{pre}km"><rect x="40" y="0" width="40" height="80"/></clipPath>'
            f'<g id="{pre}iw" clip-path="url(#{pre}kk)">{IKON}</g><g id="{pre}im" clip-path="url(#{pre}km)">{IKON}</g></defs>'
            f'<rect width="{w}" height="{h}" fill="{PAPIR}"/>')
    def add(self, s): self.e.append(s)
    def tekst(self, x, y, s, st=20, kl="", anker="start", fyll=None, ekstra=""):
        f = f' style="fill:{fyll}"' if fyll else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{st}" text-anchor="{anker}" class="{kl}"{f}{ekstra}>{s}</text>')
    def linjer(self, x, y, ls, st=17, kl="i", anker="start", lh=1.35):
        for k, l in enumerate(ls): self.tekst(x, y + k * st * lh, l, st, kl, anker)
    def linje(self, x1, y1, x2, y2, farge=SORT, b=1, ekstra=""):
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{farge}" stroke-width="{b}"{ekstra}/>')
    def ikon(self, kvinne, x, bunn, h):
        s = h / 68.37; cx = 23.4 if kvinne else 60.7
        i = self.pre + ("iw" if kvinne else "im")
        self.add(f'<use xlink:href="#{i}" href="#{i}" color="{KV if kvinne else MA}" transform="translate({x - cx * s:.2f} {bunn - 74.17 * s:.2f}) scale({s:.4f})"/>')
    def vippe(self, cx, cy, L, skar, kv_tyngst, ih, vk=None, vm=None, st=15, b=3):
        a = math.radians((1 - skar) * MAKSV * (-1 if kv_tyngst else 1))
        dx, dy = L / 2 * math.cos(a), L / 2 * math.sin(a)
        t = ih * .34
        self.add(f'<path d="M{cx:.1f} {cy + b / 2:.1f}L{cx - t * .6:.1f} {cy + t:.1f}L{cx + t * .6:.1f} {cy + t:.1f}Z" fill="{SORT}"/>')
        self.linje(cx - dx, cy - dy, cx + dx, cy + dy, SORT, b, ' stroke-linecap="round"')
        i = .84
        self.ikon(True, cx - dx * i, cy - dy * i - b / 2, ih); self.ikon(False, cx + dx * i, cy + dy * i - b / 2, ih)
        if vk: self.tekst(cx - dx * i, cy - dy * i - ih - st * .55, vk, st, "t", "middle", KV)
        if vm: self.tekst(cx + dx * i, cy + dy * i - ih - st * .55, vm, st, "t", "middle", MA)
    def maaler(self, cx, cy, L, andel, b=7):
        self.add(f'<rect x="{cx - L / 2:.1f}" y="{cy - b / 2:.1f}" width="{L}" height="{b}" fill="none" stroke="{SORT}" stroke-width="1"/>')
        self.add(f'<rect x="{cx - L / 2:.1f}" y="{cy - b / 2:.1f}" width="{L * andel:.1f}" height="{b}" fill="{SORT}"/>')
    def ring(self, cx, cy, R, merk=None, buer=True, prikk=5):
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{SORT}" stroke-width="1.4"/>')
        for f in (.25, .5, .75): self.add(f'<circle cx="{cx}" cy="{cy}" r="{R * f:.1f}" fill="none" stroke="{LYS}" stroke-width="{1 if f == .5 else .6}"/>')
        pts = []
        for k, ind in enumerate(IND):
            th = math.radians(k * 30); sx, sy = math.sin(th), -math.cos(th); v = S[ind[1]]
            self.linje(cx, cy, cx + R * sx, cy + R * sy, SORT, 3.5 if merk == k else .7)
            pts.append((cx + R * v * sx, cy + R * v * sy))
        self.add('<path d="M' + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + f'Z" fill="{SORT}" fill-opacity=".15" stroke="{SORT}" stroke-width="1.8" stroke-linejoin="round"/>')
        for k, (x, y) in enumerate(pts): self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{prikk * (2 if merk == k else 1)}" fill="{SORT}"/>')
        if buer:
            for n, a, b_ in GRUPPER:
                t0, t1 = math.radians(a * 30 - 10), math.radians(b_ * 30 + 10); r = R + 10
                self.add(f'<path d="M{cx + r * math.sin(t0):.1f} {cy - r * math.cos(t0):.1f}A{r} {r} 0 {1 if t1 - t0 > math.pi else 0} 1 {cx + r * math.sin(t1):.1f} {cy - r * math.cos(t1):.1f}" fill="none" stroke="{SORT}" stroke-width="2.4"/>')
    def gruppenavn(self, cx, cy, R, st=12):
        for j, (n, a, b_) in enumerate(GRUPPER):
            t0, t1 = math.radians(a * 30 - 14), math.radians(b_ * 30 + 14); midt = (a + b_) * 15
            if 100 < midt < 260:   # nedre halvdel: snu retningen så teksten står rett vei
                r = R + 30
                d = f"M{cx + r * math.sin(t1):.1f} {cy - r * math.cos(t1):.1f}A{r} {r} 0 0 0 {cx + r * math.sin(t0):.1f} {cy - r * math.cos(t0):.1f}"
            else:
                r = R + 20
                d = f"M{cx + r * math.sin(t0):.1f} {cy - r * math.cos(t0):.1f}A{r} {r} 0 {1 if t1 - t0 > math.pi else 0} 1 {cx + r * math.sin(t1):.1f} {cy - r * math.cos(t1):.1f}"
            self.add(f'<path id="gb{j}" d="{d}" fill="none"/><text font-size="{st}" class="sc" text-anchor="middle"><textPath href="#gb{j}" xlink:href="#gb{j}" startOffset="50%">{n}</textPath></text>')
    def hode_tekst(self, x=40, tittel="Hvor likestilte er vi?", st=44):
        self.tekst(x, 44, f"Indikatorer for kjønnslikestilling · hele landet · {D['aar']}", 14, "sc")
        self.tekst(x, 44 + st * 1.2, tittel, st)
    def kilde(self, x, y, anker="start"):
        self.tekst(x, y, "Kilde: Statistisk sentralbyrå, tabell 09292 og 09293. Prototype, ikke kvalitetssikret.", 13, "i", anker)
    def lagre(self, sti):
        p = ROT / sti; p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.hode + "".join(self.e) + "</svg>", encoding="utf-8"); print("skrev", sti)

def verdier(ind):
    navn, kode, g, typ, v = ind
    if typ == "kr": return kr(v[0]), kr(v[1])
    return nb(v[0]), nb(v[1])

def satellitt(s, ind, px, py, L=120, ih=40):
    navn, kode, g, typ, v = ind; sk = S[kode]
    s.tekst(px, py - (80 if typ in ("pst", "kr") else 40), navn, 20, "", "middle")
    if typ in ("pst", "kr"):
        vk, vm = verdier(ind)
        s.vippe(px, py + 18, L, sk, v[0] > v[1], ih, vk + ("" if typ == "kr" else " %"), vm + ("" if typ == "kr" else " %"), 14 if typ == "kr" else 15)
    else:
        s.maaler(px, py + 12, L, sk)
        s.tekst(px, py - 6, (nb(v) + " % av barna" if kode == "Barnehage" else nb(v) + " % av fedrene") if typ == "andel" else "bare skår", 15, "t g" if typ == "andel" else "i", "middle")
    s.tekst(px, py + 66, nb(sk, 2), 24, "t", "middle")

# ---------- A: kransen ----------
def variant_a(fontsti, sti):
    s = Svg(1200, 1120, fontsti); s.hode_tekst()
    s.linjer(40, 128, ["Tolv indikatorer rundt én ring.", "Jo mer av ringen som er fylt, desto likere."], 18)
    cx, cy, R = 600, 610, 200
    s.ring(cx, cy, R); s.gruppenavn(cx, cy, R)
    s.tekst(cx + 5, cy - R * .5 + 15, "0,5", 12, "t g")
    for k, ind in enumerate(IND):
        th = math.radians(k * 30)
        satellitt(s, ind, cx + 445 * math.sin(th), cy - 405 * math.cos(th) - 6)
    s.linjer(40, 1040, ["Vippa står i vater når kvinner og menn har like mye. Tallet under er skåren:", "0 er bare det ene kjønnet, 1 er full likestilling. To indikatorer har bare skår."], 15)
    s.ikon(True, 980, 1062, 30); s.tekst(994, 1056, "kvinner", 15, "g"); s.ikon(False, 1076, 1062, 30); s.tekst(1090, 1056, "menn", 15, "g")
    s.kilde(40, 1100); s.lagre(sti)

# ---------- B: ring og rekke ----------
def variant_b(fontsti, sti):
    s = Svg(1200, 790, fontsti); s.hode_tekst()
    cx, cy, R = 350, 455, 190
    s.ring(cx, cy, R)
    for k, ind in enumerate(IND):
        th = math.radians(k * 30); sx, sy = math.sin(th), -math.cos(th)
        an = "start" if sx > .25 else "end" if sx < -.25 else "middle"
        s.tekst(cx + (R + 26) * sx, cy + (R + 26) * sy + (-6 if k == 0 else 18 if k == 6 else 6), ind[0], 16, "", an)
    s.tekst(cx + 5, cy - R * .5 + 15, "0,5", 12, "t g")
    x0, y0, dy = 690, 150, 46
    s.tekst(x0, y0 - 34, "Sortert etter skår", 13, "sc"); s.tekst(1160, y0 - 34, "Skår", 13, "sc", "end")
    for r, ind in enumerate(sorted(IND, key=lambda i: -S[i[1]])):
        navn, kode, g, typ, v = ind; y = y0 + r * dy; sk = S[kode]
        s.linje(x0, y - 26, 1160, y - 26, LYS, .6)
        s.tekst(x0, y + 6, navn, 19)
        if typ in ("pst", "kr"):
            vk, vm = verdier(ind); e = "" if typ == "kr" else " %"
            s.vippe(985, y + 6, 84, sk, v[0] > v[1], 26, b=2.4)
            s.tekst(985 - 58, y + 6, vk + e, 15, "t", "end", KV); s.tekst(985 + 58, y + 6, vm + e, 15, "t", "start", MA)
        else:
            s.maaler(985, y + 1, 84, sk)
            s.tekst(985 + 58, y + 6, (nb(v) + " %") if typ == "andel" else "bare skår", 15, "t g" if typ == "andel" else "i")
        s.tekst(1160, y + 7, nb(sk, 2), 22, "t", "end")
    s.linjer(40, 735, ["Vippa står i vater når kvinner og menn har like mye. Barnehage og fedrekvote er andeler, ikke fordelinger."], 15)
    s.kilde(40, 768); s.lagre(sti)

# ---------- C: toppgrafikk 1200 x 330 ----------
def variant_c(fontsti, sti):
    s = Svg(1200, 330, fontsti)
    lav = min(IND, key=lambda i: S[i[1]]); hoy = max(S.values())
    s.tekst(40, 44, f"Indikatorer for kjønnslikestilling · hele landet · {D['aar']}", 14, "sc")
    s.tekst(40, 138, f"{nb(S[lav[1]], 2)} – {nb(hoy, 2)}", 84, "t")
    s.tekst(40, 186, "Tolv indikatorer på en skala der 1 er full likestilling.", 23)
    s.linjer(40, 226, ["Nærmest: barnehage og arbeidsstyrke.", "Lengst unna: deltid. Om lag hver tredje kvinne jobber deltid, mot hver sjette mann."], 17)
    s.ring(760, 170, 118, merk=6, buer=False, prikk=3.2)
    vk, vm = verdier(lav)
    s.vippe(1030, 214, 190, S[lav[1]], True, 62, vk + " %", vm + " %", 18, 4)
    s.tekst(1030, 282, f"Deltid {nb(S[lav[1]], 2)}", 20, "", "middle")
    s.kilde(40, 308); s.lagre(sti)

# ---------- konseptgrafikk ----------
def markor(s, x, y, n):
    s.add(f'<circle cx="{x}" cy="{y}" r="15" fill="{SORT}"/>'); s.tekst(x, y + 7, str(n), 19, "t", "middle", PAPIR)
def pil(s, x1, y, x2):
    s.linje(x1, y, x2 - 8, y, GRAA, 1.4); s.add(f'<polygon points="{x2},{y} {x2 - 11},{y - 6} {x2 - 11},{y + 6}" fill="{GRAA}"/>')
def pil_ned(s, x, y1, y2):
    s.linje(x, y1, x, y2 - 8, GRAA, 1.4); s.add(f'<polygon points="{x},{y2} {x - 6},{y2 - 11} {x + 6},{y2 - 11}" fill="{GRAA}"/>')
def trinn(s, n, x, y, bredde):
    led = IND[9]; kv, mn = led[4]; sk = S[led[1]]; m = x + bredde / 2
    markor(s, x + 15, y + 15, n)
    if n == 1:
        s.tekst(x + 42, y + 23, "Grunnlagstall", 24)
        s.ikon(True, m - 62, y + 236, 130); s.ikon(False, m + 62, y + 236, 130)
        s.tekst(m - 62, y + 92, nb(kv) + " %", 24, "t", "middle", KV); s.tekst(m + 62, y + 92, nb(mn) + " %", 24, "t", "middle", MA)
        s.linjer(m, y + 272, ["Kvinner og menn blant ledere, 2024."], 17, "i", "middle")
    if n == 2:
        s.tekst(x + 42, y + 23, "Vippehuske", 24)
        s.vippe(m, y + 200, 230, sk, False, 76, b=4.5)
        s.tekst(m, y + 92, f"{nb(kv)} / 50 = {nb(sk, 2)}", 24, "t", "middle")
        s.linjer(m, y + 272, ["Skåren er den minste andelen delt på 0,5.", "Står vippa i vater, er skåren 1."], 17, "i", "middle")
    if n == 3:
        s.tekst(x + 42, y + 23, "Ringen", 24)
        s.ring(m, y + 150, 92, merk=9, buer=False, prikk=2.6)
        s.tekst(m - 100, y + 62, f"Ledere {nb(sk, 2)}", 17, "t", "end")
        s.linjer(m, y + 272, ["Tolv skårer, én eike hver.", "Fylt ring betyr full likestilling."], 17, "i", "middle")
def ikke_med(s, x, y, w, ls):
    h = 22 + len(ls) * 23
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#85857c" stroke-width="1.2" stroke-dasharray="6 5"/>')
    s.linjer(x + 16, y + 30, ls, 17, "i")
    return h

def konsept_bred(fontsti, sti):
    s = Svg(1200, 440, fontsti, "b")
    for n, x in ((1, 40), (2, 430), (3, 820)): trinn(s, n, x, 30, 340)
    pil(s, 372, 190, 420); pil(s, 778, 190, 826)
    ikke_med(s, 40, 372, 1120, ["Ikke med: én samlet skår per kommune. De tolv indikatorene publiseres hver for seg, og hver har sin egen målestokk."])
    s.lagre(sti)
def konsept_smal(fontsti, sti):
    s = Svg(390, 1130, fontsti, "s")
    for n, y in ((1, 24), (2, 372), (3, 720)): trinn(s, n, 20, y, 350)
    pil_ned(s, 195, 336, 366); pil_ned(s, 195, 684, 714)
    ikke_med(s, 20, 1040, 350, ["Ikke med: én samlet skår per kommune.", "Hver indikator har sin egen målestokk."])
    s.lagre(sti)

if __name__ == "__main__":
    F2, F3 = "../../felles/vendor/et-book/", "../../../felles/vendor/et-book/"
    # Konseptgrafikken bakes inn i index.html og bruker skriften derfra, uten egen @font-face.
    konsept_bred(None, "src/konsept-bred.svg"); konsept_smal(None, "src/konsept-smal.svg")
    variant_a(F3, "docs/grafikk/02-topp-a.svg"); variant_b(F3, "docs/grafikk/02-topp-b.svg"); variant_c(F3, "docs/grafikk/02-topp-c.svg")

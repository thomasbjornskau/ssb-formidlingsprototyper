"""Lager src/kart.json fra data/raw/kommuner-S.geojson.

Kjøres for hånd når kommuneinndelingen endres:  python likekom/scripts/lag_kart.py
Kartgrunnlag: Kartverket, CC BY 4.0, hentet fra github.com/robhop/fylker-og-kommuner (Kommuner-S, 2024).
Projeksjon: transversal Mercator med sentralmeridian 15 grader øst. Forenklet med Douglas–Peucker.
"""
import json, math, pathlib

MAPPE = pathlib.Path(__file__).resolve().parent.parent
B, H, TOL, MINAREAL = 560, 700, 0.6, 2.0
L0 = math.radians(15)

def proj(lon, lat):
    l, p = math.radians(lon) - L0, math.radians(lat)
    return math.atanh(math.sin(l) * math.cos(p)), -math.atan2(math.tan(p), math.cos(l))
def areal(r):
    return 0.5 * sum(r[i][0] * r[(i + 1) % len(r)][1] - r[(i + 1) % len(r)][0] * r[i][1] for i in range(len(r)))
def dp(pts, tol):
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; dx, dy = b[0] - a[0], b[1] - a[1]; n = math.hypot(dx, dy) or 1e-9
    dm, im = 0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dx * (pts[i][1] - a[1]) - dy * (pts[i][0] - a[0])) / n
        if d > dm: dm, im = d, i
    if dm <= tol: return [a, b]
    return dp(pts[:im + 1], tol)[:-1] + dp(pts[im:], tol)

geo = json.loads((MAPPE / "data/raw/kommuner-S.geojson").read_text(encoding="utf8"))
alle, F = [], {}
for f in geo["features"]:
    g = f["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    ringer = [[proj(*c[:2]) for c in p[0]] for p in polys]
    F[f["properties"]["kommunenummer"]] = ringer; alle += [p for r in ringer for p in r]
x0, x1 = min(p[0] for p in alle), max(p[0] for p in alle); y0, y1 = min(p[1] for p in alle), max(p[1] for p in alle)
s = min(B / (x1 - x0), H / (y1 - y0)); ox, oy = (B - (x1 - x0) * s) / 2, (H - (y1 - y0) * s) / 2
ut = {}
for k in sorted(F):
    rs = sorted(([(ox + (p[0] - x0) * s, oy + (p[1] - y0) * s) for p in r] for r in F[k]), key=lambda r: -abs(areal(r)))
    behold = []
    for n, r in enumerate(rs):
        if n and abs(areal(r)) < MINAREAL: continue      # små øyer droppes, men største flate beholdes alltid
        h = len(r) // 2; q = dp(r[:h + 1], TOL)[:-1] + dp(r[h:], TOL)[:-1]
        behold.append(q if len(q) >= 3 else r)
    ut[k] = "".join("M" + "L".join(f"{a:.1f} {b:.1f}" for a, b in r) + "Z" for r in behold)
(MAPPE / "src/kart.json").write_text(json.dumps({"b": B, "h": H, "k": ut}, separators=(",", ":")), encoding="utf8")
print(f"src/kart.json: {len(ut)} kommuner, {round((MAPPE / 'src/kart.json').stat().st_size / 1024)} kB")

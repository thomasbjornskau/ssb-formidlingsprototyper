"""Bygger index.html fra src/index.template.html. Erstatter felles/bygg.py til repoet er tilgjengelig.
Fonter bakes inn som base64. Ikoner er Lucide (ISC-lisens), lest fra lucide-static.
Bare standardbiblioteket."""
import base64, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = "/tmp/claude-0/-home-claude/789c6c70-e699-5834-81b4-581ee87ddeca/scratchpad/"
FONTS = [("Open Sans", 400, SP + "fonts/package/files/open-sans-latin-400-normal.woff2"),
         ("Open Sans", 700, SP + "fonts/package/files/open-sans-latin-700-normal.woff2"),
         ("Roboto", 700, SP + "npmp/node_modules/@fontsource/roboto/files/roboto-latin-700-normal.woff2"),
         ("Roboto Condensed", 700, SP + "npmp/node_modules/@fontsource/roboto-condensed/files/roboto-condensed-latin-700-normal.woff2")]
LUC = SP + "npmp/node_modules/lucide-static/icons/"
IKONER = ["house", "tractor", "sprout", "trees", "mountain-snow", "droplets", "waves", "droplet", "umbrella", "sailboat", "fish",
          "wheat", "tree-pine", "flower", "leaf", "thermometer", "wind", "luggage", "mountain"]

subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "lag_data.py")], check=True)
t = open(os.path.join(ROOT, "src", "index.template.html")).read()
font = "".join(f"@font-face{{font-family:'{f}';font-weight:{w};font-display:swap;src:url(data:font/woff2;base64,"
               f"{base64.b64encode(open(p, 'rb').read()).decode()}) format('woff2')}}" for f, w, p in FONTS)
t = t.replace("/*__FONT__*/", font)
ik = {}
for n in IKONER:
    s = open(LUC + n + ".svg").read()
    ik[n] = "".join(re.findall(r"<(?:path|circle|line|rect|polyline|polygon|ellipse)\b[^>]*/>", s))
t = t.replace("/*__IKONER__*/", json.dumps(ik, ensure_ascii=False, sort_keys=True))
t = re.sub(r"/\*__INKLUDER:([^_]+?)__\*/", lambda m: open(os.path.join(ROOT, m.group(1))).read().strip(), t)
open(os.path.join(ROOT, "index.html"), "w").write(t)
print("index.html:", len(t.encode()) // 1024, "kB")

"""Bygger index.html for én statistikk.

Bruk, fra roten av repoet:
    python felles/bygg.py regfram

1. Kjører <statistikk>/scripts/lag_data.py hvis den finnes. Skriptet lager
   build/-filene og stopper med feil hvis datakontrollene ikke går opp.
2. Leser <statistikk>/src/index.template.html og bytter ut plassholderne:
     /*__FONT__*/            felles/vendor/opensans.css
     /*__D3__*/              felles/vendor/d3.min.js
     /*__INKLUDER:sti__*/    fil relativt til statistikkmappen
3. Skriver <statistikk>/index.html, én frittstående fil uten eksterne kall.
"""
import pathlib
import re
import subprocess
import sys

ROT = pathlib.Path(__file__).resolve().parent.parent


def bygg(navn):
    mappe = ROT / navn
    lag = mappe / "scripts" / "lag_data.py"
    if lag.exists():
        if subprocess.run([sys.executable, "-I", str(lag)], cwd=mappe).returncode:
            sys.exit(f"{navn}: lag_data.py feilet, index.html er ikke bygget")
    mal = (mappe / "src" / "index.template.html").read_text(encoding="utf8")

    def les(sti):
        tekst = sti.read_text(encoding="utf8")
        if sti.suffix in (".js", ".json") and "</script" in tekst.lower():
            sys.exit(f"{sti} inneholder </script og kan ikke bakes inn")
        return tekst

    faste = {
        "/*__FONT__*/": "/* Open Sans, SIL Open Font License 1.1 */\n" + les(ROT / "felles/vendor/opensans.css"),
        "/*__D3__*/": "/* d3 7.9.0, ISC-lisens */\n" + les(ROT / "felles/vendor/d3.min.js"),
    }
    for plass, innhold in faste.items():
        if mal.count(plass) > 1:
            sys.exit(f"{plass} finnes flere ganger i malen")
        mal = mal.replace(plass, innhold)

    def inkluder(m):
        sti = (mappe / m.group(1)).resolve()
        if mappe.resolve() not in sti.parents:
            sys.exit(f"{m.group(1)} ligger utenfor {navn}/")
        return les(sti)

    mal = re.sub(r"/\*__INKLUDER:([^*]+)__\*/", inkluder, mal)
    if "/*__" in mal:
        sys.exit("ukjent plassholder igjen i malen: " + mal[mal.index("/*__"):][:60])
    ut = mappe / "index.html"
    ut.write_text(mal, encoding="utf8")
    print(f"{ut.relative_to(ROT)}: {round(ut.stat().st_size / 1024)} kB")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("bruk: python felles/bygg.py <statistikk>")
    bygg(sys.argv[1])

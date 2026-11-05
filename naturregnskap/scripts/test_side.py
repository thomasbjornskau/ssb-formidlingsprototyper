import asyncio, os, sys
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in (1280, 390):
            pg = await b.new_page(viewport={"width": w, "height": 900})
            errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            for k in ["04", "05", "06", "02", "01", "11", "08"]:
                await pg.goto(f"file://{ROOT}/index.html#oko={k}")
                await pg.wait_for_timeout(300)
                sw = await pg.evaluate("document.documentElement.scrollWidth")
                print(w, k, "scrollWidth", sw, "OK" if sw <= w else "FOR BRED")
                if k in ("04", "06", "11"):
                    await pg.screenshot(path=f"{ROOT}/docs/test/{w}-{k}.png", full_page=True)
            # klikk i figur
            await pg.goto(f"file://{ROOT}/index.html#oko=04")
            await pg.click("#velg button[data-kode='05']")
            print(w, "hash etter klikk:", await pg.evaluate("location.hash"))
            print(w, "feil:", errs or "ingen")
        await b.close()
asyncio.run(main())

# -*- coding: utf-8 -*-
"""Programmatic check of the HTML guide before delivery.

    python3 revisa_html.py <guia.html> [carpeta_capturas_png]

Checks at 1600x900, 1366x768 and 390x844: sheets taller than the viewport,
horizontal scroll, images that did not load, pending-capture placeholders, and
that printing gives one page per sheet with every image drawn. Exit 1 on a
blocking failure. Optional folder: writes a PNG per sheet at 1600x900 to look at.
"""
import asyncio, os, sys
from playwright.async_api import async_playwright


async def main(path, shots=None):
    url = "file://" + os.path.abspath(path)
    fallos, avisos = [], []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, h in [(1600, 900), (1366, 768), (390, 844)]:
            pg = await b.new_page(viewport={"width": w, "height": h})
            await pg.goto(url)
            await pg.wait_for_timeout(700)
            r = await pg.evaluate("""() => ({
              n: document.querySelectorAll('.sheet').length,
              altas: [...document.querySelectorAll('.sheet')].map((s,i)=>[i+1,s.scrollHeight]).filter(x=>x[1]>innerHeight+2).map(x=>x[0]),
              hscroll: document.documentElement.scrollWidth > innerWidth,
              rotas: [...document.querySelectorAll('.sheet img')].filter(i=>!i.complete||i.naturalWidth===0).length,
              pendientes: document.querySelectorAll('.ph').length,
              menu: document.querySelectorAll('#navbtns button').length})""")
            tag = "%dx%d" % (w, h)
            if r["hscroll"]:
                fallos.append("%s: scroll horizontal" % tag)
            if r["rotas"]:
                fallos.append("%s: %d imagenes sin cargar" % (tag, r["rotas"]))
            if r["pendientes"]:
                fallos.append("%s: %d capturas pendientes" % (tag, r["pendientes"]))
            if r["altas"] and w >= 1600:
                fallos.append("%s: laminas mas altas que la pantalla %s" % (tag, r["altas"]))
            elif r["altas"] and w >= 1366:
                avisos.append("%s: laminas con scroll interno %s" % (tag, r["altas"]))
            print(tag, "laminas", r["n"], "menu", r["menu"], "altas", r["altas"])
            if shots and w == 1600:
                os.makedirs(shots, exist_ok=True)
                for i in range(r["n"]):
                    await pg.evaluate("i => document.querySelectorAll('.sheet')[i].scrollIntoView()", i)
                    await pg.wait_for_timeout(250)
                    await pg.screenshot(path=os.path.join(shots, "lamina_%02d.png" % (i + 1)))
            await pg.close()
        pg = await b.new_page(viewport={"width": 1600, "height": 900})
        await pg.goto(url)
        await pg.wait_for_timeout(700)
        n = await pg.evaluate("document.querySelectorAll('.sheet').length")
        await pg.emulate_media(media="print")
        pdf = path + ".print-check.pdf"
        await pg.pdf(path=pdf, width="13.333in", height="7.5in", print_background=True)
        await b.close()
    try:
        import pymupdf
        d = pymupdf.open(pdf)
        if len(d) != n:
            fallos.append("impresion: %d paginas para %d laminas" % (len(d), n))
        sin = [i + 1 for i in range(len(d)) if not d[i].get_images() and i not in (0, len(d) - 1)]
        if sin:
            avisos.append("impresion: paginas sin imagen %s (revisar si deberian llevar captura)" % sin)
        d.close()
    except ImportError:
        avisos.append("pymupdf no instalado: no se reviso la impresion")
    os.remove(pdf)
    for a in avisos:
        print("  aviso ", a)
    for f in fallos:
        print("  FALLO ", f)
    print("Todo conforme." if not fallos else "No se entrega hasta corregir.")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)))

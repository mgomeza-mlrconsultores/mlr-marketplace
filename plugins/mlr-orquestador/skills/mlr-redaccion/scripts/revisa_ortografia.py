# -*- coding: utf-8 -*-
"""
Revision ortografica de entregables de MLR: tildes y enes faltantes.

Revisa el NOMBRE de cada archivo y su CONTENIDO (PDF, Word, Excel, HTML, Markdown o
texto). En Excel revisa tambien el nombre de cada hoja y todas las celdas de texto,
no las formulas. Devuelve 0 si no hay hallazgos y 1 si los hay.

    python3 revisa_ortografia.py "Informes/20260928/1. MLR - Propuesta Económica - Cliente.pdf" ...
    python3 revisa_ortografia.py --nombres-solo "carpeta/*"

En Excel revisa ademas las etiquetas cortas escritas con mayuscula en cada palabra al
estilo ingles («Listas de Materiales»): en espanol solo va mayuscula la primera palabra
y los nombres propios («Listas de materiales»).

Metodo: una palabra se marca solo cuando NO existe en el diccionario del espanol y
una variante suya con una tilde o una ene SI existe ("economica" -> "económica",
"Diagnostico" -> "Diagnóstico", "Anos" -> "Años"). Los nombres propios, los terminos
tecnicos y el ingles no tienen variante acentuada en el diccionario y no se marcan.
Las parejas validas en los dos sentidos (esta/está, mas/más, solo, que/qué) no se
pueden decidir sin contexto y quedan a la revision de quien redacta.

Requiere spylls (pip install spylls) y, para PDF, pymupdf; para Excel, openpyxl.
El diccionario va incluido en scripts/diccionario.
"""
import sys, os, re, glob, zipfile, argparse, functools, html

AQUI = os.path.dirname(os.path.abspath(__file__))
DICC = os.path.join(AQUI, "diccionario", "es_MX")

# Palabras que el diccionario no resuelve y que la firma escribe asi a proposito.
# MONICA: linea de firmantes fijada por direccion en documento_mlr. Martin: nombre del cliente
# tal como aparece en el documento aprobado por direccion (Comband DTH).
# Inter, Medium: nombre y peso de tipografias. name, min, max: terminos de codigo y de HTML.
EXCEPCIONES = {"MONICA", "Martin", "Inter", "Medium", "name", "min", "max"}

# Forms that exist as verbs without tilde but in a deliverable are almost always the noun or
# adjective: «formulas» (verb formular) is «fórmulas», «numero» is «número». The dictionary
# accepts both, so they are listed here.
HOMOGRAFOS = {w: c for w, c in (x.split(">") for x in (
    "formula>fórmula formulas>fórmulas numero>número ultimo>último ultima>última ultimos>últimos "
    "ultimas>últimas calculo>cálculo modulo>módulo practica>práctica practicas>prácticas "
    "practico>práctico catalogo>catálogo linea>línea caratula>carátula caratulas>carátulas "
    "publico>público limite>límite termino>término terminos>términos deposito>depósito "
    "transito>tránsito titulo>título indice>índice articulo>artículo critico>crítico "
    "critica>crítica analitico>analítico basico>básico estandar>estándar diagnostico>diagnóstico "
    "pagina>página paginas>páginas").split())}
HOMOGRAFOS.update({w.capitalize(): c.capitalize() for w, c in list(HOMOGRAFOS.items())})

VAR = {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "úü", "n": "ñ",
       "A": "Á", "E": "É", "I": "Í", "O": "Ó", "U": "ÚÜ", "N": "Ñ"}
ACENTOS = set("áéíóúüñÁÉÍÓÚÜÑ")
PALABRA = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+")
# URLs, emails, paths, identifiers (snake_case, kebab-case), file names and inline code are not prose.
LIMPIA = re.compile(r"https?://\S+|www\.\S+|\S+@\S+|\S*[_/\\]\S*|`[^`\n]*`"
                    r"|\S*[A-Za-z0-9]-[A-Za-z]\S*|\S+\.(?:md|py|docx|xlsx|pdf|html|json|txt)\b")
# Spanish words that stay lowercase inside a title: articles, prepositions, conjunctions.
MINUSCULAS = set("a al ante bajo con contra de del desde durante e el en entre hacia hasta la las "
                 "lo los mediante o para por según sin sobre tras u un una unos unas y".split())


@functools.lru_cache(maxsize=1)
def _dic():
    try:
        from spylls.hunspell import Dictionary
    except ImportError:
        sys.exit("Falta spylls: pip install spylls")
    return Dictionary.from_files(DICC)


@functools.lru_cache(maxsize=None)
def existe(p):
    return _dic().lookup(p)


@functools.lru_cache(maxsize=None)
def corrige(p):
    """Returns the accented form if `p` lacks a tilde/eñe, else None."""
    if p in HOMOGRAFOS:
        return HOMOGRAFOS[p]
    if (len(p) < 3 or p in EXCEPCIONES or ACENTOS & set(p)
            or (p.isupper() and len(p) <= 4) or existe(p)):   # short acronyms: SAT, PUE, IVA
        return None
    # the eñe goes first: «anade» is «añade», not «ánade»
    cands = [(i, alt) for i, ch in enumerate(p) for alt in VAR.get(ch, "")]
    cands.sort(key=lambda x: x[1] not in "ñÑ")
    for i, alt in cands:
        c = p[:i] + alt + p[i + 1:]
        if existe(c):
            return c
    return None


# «esta» before a participle or «en/bien/mal» is the verb: «está en», «está calibrado».
ESTA = re.compile(r"\b([Ee])sta(n?) (en|bien|mal|dentro|listo|lista|pendiente|disponible|"
                  r"[a-záéíóú]+(?:ado|ada|ados|adas|ido|ida|idos|idas|ierto|ierta|uelto|uelta|echo|echa))\b")


def revisa_texto(texto):
    """List of (word, suggestion) pairs, unique and in order of appearance."""
    vistos, out = set(), []
    limpio = LIMPIA.sub(" ", texto)
    for m in ESTA.finditer(limpio):
        w = m.group(0)
        if w not in vistos:
            vistos.add(w)
            out.append((w, "%sstá%s %s" % m.groups()))
    for w in PALABRA.findall(limpio):
        if w in vistos:
            continue
        vistos.add(w)
        c = corrige(w)
        if c:
            out.append((w, c))
    return out


def revisa_mayusculas(etiqueta, propios=()):
    """Title Case check for short labels (Excel cells, task names, headings).
    Spanish capitalizes only the first word and proper nouns: «Listas de materiales»,
    not «Listas de Materiales». Returns the sentence-case form, or None."""
    s = etiqueta.strip()
    ws = s.split()
    if not 2 <= len(ws) <= 7 or re.search(r"[\d.;:,()]", s):
        return None
    malas = [w for w in ws[1:] if PALABRA.fullmatch(w) and len(w) > 2 and w[0].isupper()
             and not w.isupper() and w not in propios
             and w.lower() not in MINUSCULAS and existe(w.lower())]
    if not malas:
        return None
    return " ".join([ws[0]] + [w.lower() if w in malas else w for w in ws[1:]])


def revisa_nombre(ruta):
    base = os.path.splitext(os.path.basename(ruta))[0]
    return revisa_texto(base.replace("_", " ").replace("-", " "))


def texto_de(ruta):
    ext = os.path.splitext(ruta)[1].lower()
    if ext == ".pdf":
        import pymupdf
        return " ".join(p.get_text() for p in pymupdf.open(ruta))
    if ext == ".docx":
        xml = zipfile.ZipFile(ruta).read("word/document.xml").decode("utf8")
        return " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", xml))
    if ext in (".xlsx", ".xlsm"):
        from openpyxl import load_workbook
        wb = load_workbook(ruta)
        partes = []
        for ws in wb:
            partes.append(ws.title)
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and not c.value.startswith("="):
                        partes.append(c.value)
        return " ".join(partes)
    if ext in (".html", ".htm"):
        t = open(ruta, encoding="utf8", errors="ignore").read()
        t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
        return html.unescape(re.sub(r"<[^>]+>", " ", t))
    if ext in (".md", ".txt", ".csv"):
        t = open(ruta, encoding="utf8", errors="ignore").read()
        return re.sub(r"(?s)```.*?```", " ", t)
    return ""


def etiquetas_xlsx(ruta):
    from openpyxl import load_workbook
    out = []
    for ws in load_workbook(ruta):
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and not c.value.startswith("="):
                    out.append(c.value)
    return out


def revisa_archivo(ruta, nombres_solo=False, propios=()):
    # The client name closes the MLR file name («... - Ah Cacao»): its words are proper nouns.
    base = os.path.splitext(os.path.basename(ruta))[0]
    propios = set(propios) | set(base.rsplit(" - ", 1)[-1].split()) if " - " in base else set(propios)
    r = {"nombre": revisa_nombre(ruta)}
    if not nombres_solo:
        r["contenido"] = revisa_texto(texto_de(ruta))
        if os.path.splitext(ruta)[1].lower() in (".xlsx", ".xlsm"):
            vistos, may = set(), []
            for e in etiquetas_xlsx(ruta):
                c = revisa_mayusculas(e, propios)
                if c and e not in vistos:
                    vistos.add(e); may.append((e, c))
            r["mayúsculas de estilo inglés"] = may
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rutas", nargs="+")
    ap.add_argument("--nombres-solo", action="store_true")
    ap.add_argument("--propios", default="", help="nombres propios separados por coma")
    a = ap.parse_args()
    rutas = [x for r in a.rutas for x in (glob.glob(r) or [r])]
    total = 0
    for ruta in rutas:
        r = revisa_archivo(ruta, a.nombres_solo, [w for x in a.propios.split(",") for w in x.split()])
        n = sum(len(v) for v in r.values())
        total += n
        print("%s %s" % ("OK   " if not n else "FALLA", os.path.basename(ruta)))
        for k, v in r.items():
            if v:
                print("   %s: %s" % (k, ", ".join("%s -> %s" % p for p in v)))
    print("\n%d hallazgo(s) de ortografía." % total if total else "\nOrtografía conforme.")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""Word version of an MLR functional guide, on the letterhead, from contenido.py.

    python3 genera_docx.py <carpeta_con_contenido_y_capturas> <salida.docx> [datos.json]

The folder holds contenido.py (see contenido_ejemplo.py) and capturas/NN.jpg|png.
Figures use Documento.imagen() from mlr-identidad-visual: approved capture standard,
size taken from the image, 4.4 in height cap. Then ALWAYS export to PDF and run
verifica_documento.py; nothing is delivered until it passes.
"""
import os, sys, json, importlib.util

AQUI = os.path.dirname(os.path.abspath(__file__))
IDENTIDAD = os.environ.get("MLR_IDENTIDAD") or os.path.normpath(
    os.path.join(AQUI, "..", "..", "mlr-identidad-visual", "scripts"))
sys.path.insert(0, IDENTIDAD)
from documento_mlr import Documento  # noqa: E402


def carga_contenido(carpeta):
    spec = importlib.util.spec_from_file_location("contenido", os.path.join(carpeta, "contenido.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def captura(carpeta, key):
    for ext in ("jpg", "png"):
        p = os.path.join(carpeta, "capturas", "%s.%s" % (key, ext))
        if os.path.exists(p):
            return p
    return None


def construye(carpeta, destino, datos=None):
    C = carga_contenido(carpeta)
    datos = datos or getattr(C, "DATOS", {})
    d = Documento(titulo=C.TITULO, cliente=C.CLIENTE, fecha=C.FECHA, saludo=C.SALUDO)
    d.parrafo(C.INTRO)
    faltan = []
    for sid, menu, titulo, bloques in C.SECCIONES:
        d.seccion(titulo)
        for b in bloques:
            k = b[0]
            if k == "p":
                d.parrafo(datos.get("produccion", "") if b[1] == "__PRODUCCION__" else b[1])
            elif k == "h":
                d.subtitulo(b[1])
            elif k == "v":
                d.vinetas(b[1])
            elif k == "fig":
                ruta = captura(carpeta, b[1])
                if ruta:
                    d.imagen(ruta, b[2])
                else:
                    faltan.append(b[1])
            elif k == "kpi":
                d.cuadro(["Indicador", "Cifra"], [[l[0].upper() + l[1:], a] for a, l in b[1]], [7000, 1800])
            elif k == "t":
                filas = datos.get("pruebas", []) if b[2] == "__PRUEBAS__" else b[2]
                d.cuadro(b[1], filas, b[3], ultima_columna_negrita=(len(b[1]) == 3))
            elif k == "flujo":
                pass  # HTML only; in Word the text already tells the sequence
            else:
                raise ValueError("Bloque desconocido: %r" % (k,))
    d.cierre()
    if faltan:
        print("AVISO: faltan capturas", ", ".join(faltan), "- no se entrega así")
    return d.guarda(destino)


if __name__ == "__main__":
    carpeta, destino = sys.argv[1], sys.argv[2]
    datos = json.load(open(sys.argv[3], encoding="utf8")) if len(sys.argv) > 3 else None
    print(construye(carpeta, destino, datos))

# -*- coding: utf-8 -*-
"""Shared helpers. The project is chosen with the environment variable PROY:
contabilidad, inventario or integral."""
import sys, os
# folder with documento_mlr.py (mlr-identidad-visual/scripts); override with MLR_IDENTIDAD
SK = os.environ.get("MLR_IDENTIDAD", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "..", "..", "..", "mlr-identidad-visual", "scripts"))
sys.path.insert(0, SK)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from documento_mlr import Documento
import ruta

# letterhead template; override with MLR_PLANTILLA
PLANTILLA = os.environ.get("MLR_PLANTILLA", "/mnt/user-data/uploads/MLR Odoo/Plantillas/Hoja Membretada MLR - varias paginas.docx")
KEY = os.environ.get("PROY", "contabilidad")
P = ruta.PARAMS
C = ruta.cifras(KEY)
ETAPA = ruta.HITOS[KEY]
RUTA = ruta.ruta(KEY)
SUF = {"contabilidad": "Freshbox Contabilidad", "inventario": "Freshbox Inventario",
       "integral": "Freshbox Contabilidad e Inventario"}[KEY]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
N1 = "1. Propuesta Económica - " + SUF
N2 = "2. Plan de Trabajo y Alcance Detallado - " + SUF
NX = "3. Anexo de Ruta y Horas - " + SUF


def m(v): return "$%s" % format(round(v, 2), ",.2f")
def h(v): return ("%g" % v)


def doc(titulo):
    return Documento(titulo=titulo,
                     cliente="Freshbox — Atención: Dirección General",
                     fecha=P["fecha_emision"], saludo="Estimada Dirección General de Freshbox:",
                     plantilla=PLANTILLA)

# -*- coding: utf-8 -*-
"""One run of a journal and period, start to end, in its work folder. Used for the first run and for
every run after corrections in Odoo, so the workbook always reflects Odoo as it is now.

    python3 corrida.py <carpeta_trabajo> [--sin-odoo] [--plantilla ...]

The folder holds params.json, banco.json (leer_estado_cuenta.py) and cfdi.json (leer_cfdi.py), and,
when they exist, decisiones.json and the previous workbook. The previous workbook is moved to
versiones/ and its light-blue captures and approvals are carried into the new one.
Output: Conciliacion_<Mes>_<Año>_<Empresa>_<Diario>.xlsx and conciliacion.json.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]


def limpio(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "_", t).strip("_")


def py(script, *args):
    r = subprocess.run([sys.executable, os.path.join(AQUI, script)] + list(args), text=True, capture_output=True)
    print(r.stdout.strip())
    if r.returncode not in (0,):
        print(r.stderr.strip()[-2000:])
        raise SystemExit("%s terminó con código %d" % (script, r.returncode))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("--sin-odoo", action="store_true", help="reuse odoo.json (no new extraction)")
    ap.add_argument("--plantilla")
    a = ap.parse_args()
    c = a.carpeta
    j = lambda n: os.path.join(c, n)
    P = json.load(open(j("params.json")))
    for n in ("banco.json", "cfdi.json"):
        if not os.path.exists(j(n)):
            raise SystemExit("Falta %s en la carpeta de trabajo" % n)
    if not a.sin_odoo:
        py("extraer_odoo.py", j("params.json"), j("odoo.json"))
    extra = ["--decisiones", j("decisiones.json")] if os.path.exists(j("decisiones.json")) else []
    if P.get("lista_69b"):
        extra += ["--lista-69b", P["lista_69b"]]
    py("conciliar.py", j("params.json"), j("banco.json"), j("odoo.json"), j("cfdi.json"), j("conciliacion.json"), *extra)
    d = datetime.date.fromisoformat(P["desde"])
    nombre = "Conciliacion_%s_%d_%s_%s.xlsx" % (MESES[d.month - 1], d.year, limpio(P.get("empresa_corta") or P.get("empresa", "")), limpio(P.get("diario", "")))
    salida = j(nombre)
    if not os.path.exists(j("sesion.json")):
        # start of the work on this journal (UTC, like Odoo's create_date): verificar.py counts what was created since
        json.dump({"inicio_utc": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}, open(j("sesion.json"), "w"))
    nuevo = salida.replace(".xlsx", ".nuevo.xlsx")
    args = [j("conciliacion.json"), nuevo]
    if os.path.exists(salida):
        os.makedirs(j("versiones"), exist_ok=True)
        previo = j(os.path.join("versiones", nombre.replace(".xlsx", "_%s.xlsx" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))))
        shutil.copy2(salida, previo)          # copy, not move: if this run fails the current workbook stays in place
        args += ["--anterior", salida]
    if a.plantilla:
        args += ["--plantilla", a.plantilla]
    py("llenar_libro.py", *args)
    os.replace(nuevo, salida)
    calc = nuevo.replace(".xlsx", ".calc.xlsx")
    if os.path.exists(calc):
        os.replace(calc, salida.replace(".xlsx", ".calc.xlsx"))
    print("Listo:", salida)


if __name__ == "__main__":
    main()

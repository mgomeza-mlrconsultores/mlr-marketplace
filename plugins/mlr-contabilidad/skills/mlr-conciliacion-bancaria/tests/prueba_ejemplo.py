# -*- coding: utf-8 -*-
"""Regression test of the engine and the workbook filler against the anonymized August example.

    python3 tests/prueba_ejemplo.py [carpeta_salida] [--sin-ligas]

Rebuilds banco.json, odoo.json and cfdi.json from the demo workbook, runs conciliar.py and
llenar_libro.py, and compares link type and status of every item against the example.
--sin-ligas removes the invoice links that Odoo already had, to exercise rules E02-E08 alone.
"""
import datetime
import json
import os
import subprocess
import sys

import openpyxl

AQUI = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(AQUI, "..", "scripts")
EJ = os.path.join(AQUI, "..", "assets", "Ejemplo_Conciliacion_Agosto_2026_Demo.xlsx")
sys.path.insert(0, SCR)


def iso(v):
    return v.date().isoformat() if isinstance(v, datetime.datetime) else v


def construye(salida, sin_ligas=False):
    wb = openpyxl.load_workbook(EJ)
    ec, ax, cc, fv, im = (wb[s] for s in ("Estado de cuenta", "Auxiliar Odoo", "Conciliación", "Facturas vs Odoo", "Impuestos vs Odoo"))
    L = lambda r: ec.cell(r, 12).value
    car = {"banco": L(8), "saldo_inicial": L(16), "abonos": L(17), "n_abonos": ec.cell(17, 13).value, "cargos": L(18),
           "n_cargos": ec.cell(18, 13).value, "saldo_final": L(19), "saldo_promedio": L(20), "comisiones": L(21),
           "titular": L(10), "rfc": L(11), "cuenta": L(12), "clabe": L(13)}
    import leer_estado_cuenta as LE
    movs = []
    for r in range(8, ec.max_row + 1):
        if not ec.cell(r, 1).value:
            continue
        movs.append(LE.enriquece({"partida": ec.cell(r, 1).value, "fecha": iso(ec.cell(r, 2).value), "codigo": ec.cell(r, 3).value,
                                  "descripcion": ec.cell(r, 4).value, "cargo": ec.cell(r, 5).value, "abono": ec.cell(r, 6).value,
                                  "saldo_banco": None}))
    banco = {"fuente": "ejemplo", "perfil": "bbva", "caratula": car, "movimientos": movs, "control": LE.control(movs, car)}
    # CFDI rebuilt from the CFDI block of the reconciliation plus the invoices sheet
    cf, rep = {}, {}
    filas_c = []
    for r in range(8, cc.max_row + 1):
        g = lambda c: cc.cell(r, c).value
        if not g(1):
            continue
        filas_c.append({"r": r, "partida": g(1), "renglon": g(6), "enlace": g(14), "uuid": g(15), "folio": g(16), "fecha_cfdi": iso(g(17)),
                        "contraparte": g(18), "rfc": g(19), "metodo": g(20), "tipo_ret": g(21), "total": g(22), "aplicado": g(23),
                        "ab": g(28), "base": g(32), "iva": g(33), "ivar": g(34), "isrr": g(35), "tipo": g(36), "fecha_banco": iso(g(2)),
                        "codigo_banco": None})
    for f in filas_c:
        if not f["uuid"]:
            continue
        u = f["uuid"]
        emit = f["tipo"] == "Cobro"
        folio = str(f["folio"] or "")
        serie = "".join(ch for ch in folio if not ch.isdigit())[:4] if folio and folio[0].isalpha() and emit else ""
        c = cf.setdefault(u, {"uuid": u, "direccion": "emitido" if emit else "recibido", "tipo": "I", "estado_sat": "Vigente",
                              "fecha": f["fecha_cfdi"], "serie": serie, "folio": folio[len(serie):], "total": f["total"],
                              "subtotal": f["base"], "descuento": 0, "iva": f["iva"], "iva_ret": f["ivar"], "isr_ret": f["isrr"],
                              "metodo_pago": f["metodo"], "forma_pago": "", "moneda": "MXN", "conceptos": "",
                              "regimen_emisor": "626" if "RESICO" in (f["tipo_ret"] or "") else "",
                              ("nombre_receptor" if emit else "nombre_emisor"): f["contraparte"], ("rfc_receptor" if emit else "rfc_emisor"): f["rfc"],
                              ("rfc_emisor" if emit else "rfc_receptor"): "CDT260505AB1", "fecha_pago_real": None, "pagos": []})
        pago = (datetime.date.fromisoformat(f["fecha_banco"]) + datetime.timedelta(days=f["ab"] or 0)).isoformat() if f["fecha_banco"] else None
        c["fecha_pago_real"] = c["fecha_pago_real"] or pago
        if f["enlace"] == "REP":
            rep.setdefault(u, []).append({"rep": "REP-" + u[:8], "fecha": pago, "monto": f["aplicado"], "imp_pagado": f["aplicado"], "parcialidad": 1})
    for r in range(8, fv.max_row + 1):
        u = fv.cell(r, 3).value
        if u and u not in cf:
            emit = fv.cell(r, 1).value == "Emitida"
            cf[u] = {"uuid": u, "direccion": "emitido" if emit else "recibido", "tipo": "I", "estado_sat": fv.cell(r, 6).value,
                     "fecha": iso(fv.cell(r, 4).value), "serie": "", "folio": fv.cell(r, 2).value or "", "total": fv.cell(r, 7).value,
                     "subtotal": round((fv.cell(r, 7).value or 0) / 1.16, 2), "iva": 0, "iva_ret": 0, "isr_ret": 0, "metodo_pago": "PUE",
                     ("nombre_receptor" if emit else "nombre_emisor"): fv.cell(r, 5).value, "pagos": []}
    # card terminal deposits: the invoices they settle were paid by card
    cod = {m["partida"]: m["codigo"] for m in movs}
    for f in filas_c:
        if f["uuid"] and cod.get(f["partida"]) in ("V42", "V45"):
            cf[f["uuid"]]["forma_pago"] = "04"
    for u, rs in rep.items():
        cf[u]["pagos"] = []
    cfdi = {"cfdi": cf, "indices": {"rep_por_factura": rep}}
    # Odoo: ledger, invoices it settles, VAT detail
    aux = []
    for r in range(8, ax.max_row + 1):
        if not ax.cell(r, 1).value:
            continue
        aux.append({"renglon": ax.cell(r, 1).value, "fecha": iso(ax.cell(r, 2).value), "asiento": ax.cell(r, 3).value,
                    "concepto": ax.cell(r, 4).value, "contacto": ax.cell(r, 5).value or "", "cargo": ax.cell(r, 6).value,
                    "abono": ax.cell(r, 7).value, "facturas": [], "move_id": r})
    idx = {a["renglon"]: a for a in aux}
    facturas, fid = {}, 1000
    por_uuid = {}
    for u, c in cf.items():
        fid += 1
        facturas[fid] = {"id": fid, "numero": (c.get("serie") or "") + str(c.get("folio") or "") if c["direccion"] == "emitido" else "BILL/%d" % fid,
                         "ref": "", "tipo": "out_invoice" if c["direccion"] == "emitido" else "in_invoice", "estado": "posted",
                         "total": c["total"], "pendiente": c["total"] if sin_ligas else 0.0, "partner": c.get("nombre_receptor") or c.get("nombre_emisor"), "partner_id": None,
                         "fecha": c["fecha"], "uuid": u, "politica": c["metodo_pago"], "del_mes": (c["fecha"] or "")[:7] == "2026-08"}
        por_uuid[u] = fid
    if not sin_ligas:
        for f in filas_c:
            if f["uuid"] and f["renglon"] in idx and f["enlace"] in ("1 a 1", "Parcial", "REP", "Varios CFDI"):
                idx[f["renglon"]]["facturas"].append({"id": por_uuid[f["uuid"]], "importe": f["aplicado"]})
    iva = []
    for cuenta, clave, fila in (("118.01.01", "iva_acreditable_pagado", 9), ("208.01.01", "iva_trasladado_cobrado", 10)):
        s = -1 if clave.endswith("cobrado") else 1
        det = []
        for r in range(16, im.max_row + 1):
            if im.cell(r, 2).value == cuenta:
                det.append({"origen_id": r, "numero": im.cell(r, 3).value, "partner": im.cell(r, 4).value, "uuid": im.cell(r, 5).value or "",
                            "iva": s * (im.cell(r, 6).value or 0), "reversiones": 0, "diarios": im.cell(r, 11).value or ""})
        iva.append({"clave": clave, "cuenta": cuenta, "nombre": im.cell(fila, 2).value, "saldo_inicial": s * (im.cell(fila, 3).value or 0),
                    "movimiento": s * ((im.cell(fila, 5).value or 0) - (im.cell(fila, 3).value or 0)), "detalle": det})
    si = ax.cell(12, 10).value
    odoo = {"version": "saas~19.4+e", "compania": {"id": 1, "nombre": car["titular"], "rfc": "CDT260505AB1"},
            "diario": {"id": 13, "nombre": "BBVA", "codigo": "BBVA", "tipo": "bank", "cuenta": "102.01.01", "cuenta_nombre": "Banco BBVA",
                       "moneda_extranjera": False},
            "periodo": {"desde": "2026-08-01", "hasta": "2026-08-31"}, "saldo_inicial": si,
            "saldo_final": round(si + sum((a["abono"] or 0) - (a["cargo"] or 0) for a in aux), 2),
            "auxiliar": aux, "facturas": facturas, "contactos": {}, "iva": iva, "lineas_extracto_sin_conciliar": [],
            "saldo_suspenso": 0, "diarios_caja": ["CSH1"], "hallazgos": [], "avisos": []}
    params = {"empresa": "Clínica Demo Terapia SA de CV", "empresa_corta": "Clínica Demo", "rfc_empresa": "CDT260505AB1", "compania_id": 1,
              "diario_id": 13, "diario": "BBVA", "cuenta_banco": "0100000001", "desde": "2026-08-01", "hasta": "2026-08-31",
              "tolerancia_importe": 1.0, "tolerancia_dias": 3, "modo_diario": "sin_estado", "banco_emite_cfdi_comisiones": True,
              "primer_ejercicio": True, "inicio_operaciones": "2026-05-05", "entorno": "pruebas",
              "cuentas": {"iva_acreditable_pagado": "118.01.01", "iva_trasladado_cobrado": "208.01.01", "comisiones": "701.10.01",
                          "iva_comisiones": "118.01.01", "otros_ingresos": "403.01.01"},
              "previo_manual": {"iva_cobrado": 67769.22, "iva_pagado": 13411.89, "iva_retenido": 744.54, "isr_retenido": 175.70}}
    os.makedirs(salida, exist_ok=True)
    for n, o in (("banco", banco), ("odoo", odoo), ("cfdi", cfdi), ("params", params)):
        json.dump(o, open(os.path.join(salida, n + ".json"), "w"), ensure_ascii=False, indent=1, default=str)
    return {f["partida"]: f for f in filas_c if cc.cell(f["r"], 38).value == 1}, wb


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    salida = args[0] if args else "/tmp/prueba_conciliacion"
    sin = "--sin-ligas" in sys.argv
    plantilla = next((sys.argv[i + 1] for i, x in enumerate(sys.argv) if x == "--plantilla"), None) or \
        os.path.join(AQUI, "..", "assets", "Plantilla_Conciliacion_Banco_Odoo_CFDI.xlsx")
    esperado, wb = construye(salida, sin)
    j = lambda n: os.path.join(salida, n)
    subprocess.run([sys.executable, os.path.join(SCR, "conciliar.py"), j("params.json"), j("banco.json"), j("odoo.json"), j("cfdi.json"),
                    j("conciliacion.json")], check=True)
    res = json.load(open(j("conciliacion.json")))
    ok = mal = 0
    for f in res["conciliacion"]:
        if not f["primera"] or f["partida"] not in esperado:
            continue
        e = esperado[f["partida"]]
        if f["enlace"] == e["enlace"]:
            ok += 1
        else:
            mal += 1
            print("  %s esperado %-16s obtenido %-16s regla %s" % (f["partida"], e["enlace"], f["enlace"], f["regla"]))
    print("Enlace igual al ejemplo: %d de %d" % (ok, ok + mal))
    if sin:
        # without Odoo links the rules alone must still find at least 95 of the 107 items of the example
        return 0 if ok >= 95 else 1
    # workbook: fill, recalculate and compare the figures that matter with the example recalculated
    from llenar_libro import recalcula
    subprocess.run([sys.executable, os.path.join(SCR, "llenar_libro.py"), j("conciliacion.json"), j("libro.xlsx"), "--plantilla", plantilla], check=True)
    import shutil
    shutil.copy(EJ, j("ejemplo.xlsx"))
    _, err, calc_ej = recalcula(j("ejemplo.xlsx"))
    a = openpyxl.load_workbook(calc_ej, data_only=True)
    b = openpyxl.load_workbook(j("libro.calc.xlsx"), data_only=True)
    celdas = {"Resumen": ["D9", "D14", "H9", "H10", "H11", "H12", "H13", "H14", "D19", "D20", "D21", "D22", "D23", "D24", "H19", "H20", "H21",
                          "H22", "D29", "D30", "D31", "D32", "D33", "H31", "H32"],
              "Previo": ["E13", "E14", "E15", "E25", "E26", "E32", "F36"], "Desglose fiscal": ["B18", "C18", "B32", "C32", "D32", "E32", "B40", "B43", "C43"]}
    difs = [(h, c, a[h][c].value, b[h][c].value) for h, cs in celdas.items() for c in cs if a[h][c].value != b[h][c].value]
    for d in difs:
        print("  %s!%s ejemplo %s libro %s" % d)
    print("Cifras del libro iguales al ejemplo: %d de %d" % (sum(len(v) for v in celdas.values()) - len(difs), sum(len(v) for v in celdas.values())))
    return mal + len(difs)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)

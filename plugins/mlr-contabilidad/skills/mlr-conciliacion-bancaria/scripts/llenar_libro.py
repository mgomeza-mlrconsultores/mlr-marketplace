# -*- coding: utf-8 -*-
"""Fill the MLR reconciliation workbook from conciliacion.json without breaking a single formula.

    python3 llenar_libro.py <conciliacion.json> <salida.xlsx> [--plantilla Plantilla_Conciliacion_Banco_Odoo_CFDI.xlsx]
           [--anterior libro_de_la_corrida_anterior.xlsx]

- Template: the one in the shared drive folder when it is reachable, otherwise the copy in assets/.
- Every table is resized to the real number of rows. The template was drawn for a month of 107
  movements; with fewer rows the blank formulas would count as "No identificado", with more they
  would fall outside every SUMIF. All ranges that point to a table, in any sheet, are rewritten.
- Improvements applied on top of the template (idempotent): "¿Se puede enviar el Previo?" in the
  Resumen, warning banner in the Previo, cash journals read from the observation instead of a fixed
  journal code, labels of the VAT explanation block, and the Acciones, Verificación and Bitácora sheets.
- --anterior keeps what the user typed in light-blue cells (payroll ISR, credit applied, approvals,
  comments) from the previous run of the same journal and period.
- Recalculates with LibreOffice when available and fails if any formula returns an error.
"""
import argparse
import copy
import datetime
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import openpyxl
from openpyxl.formula.tokenizer import Tokenizer
from openpyxl.formula.translate import Translator
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import column_index_from_string, get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

AQUI = os.path.dirname(os.path.abspath(__file__))
DRIVE = [r"G:\Unidades compartidas\MMLR 2025\Hoja Membretada\Conciliación Bancaria",
         os.path.expanduser("~/mnt/Conciliación Bancaria")]
TEAL, AZUL, CAFE, TINTA = "24606C", "E6F3FB", "452E27", "2B2B2B"
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# sheet: (first data row, column whose formula marks the table length, first col, last col)
TABLAS = {"Estado de cuenta": (8, "G", "A", "G"), "Auxiliar Odoo": (8, "H", "A", "H"), "Conciliación": (8, "AD", "A", "AL"),
          "Facturas vs Odoo": (8, "L", "A", "M"), "Impuestos vs Odoo": (16, "I", "A", "K")}
REF = re.compile(r"^(?:(?P<sh>'[^']+'|[^'!]+)!)?(?P<a>\$?[A-Z]{1,3}\$?\d+)(?::(?P<b>\$?[A-Z]{1,3}\$?\d+))?$")
CELDA = re.compile(r"(\$?)([A-Z]{1,3})(\$?)(\d+)")


def plantilla_por_defecto():
    for d in DRIVE:
        p = os.path.join(d, "Plantilla_Conciliacion_Banco_Odoo_CFDI.xlsx")
        if os.path.exists(p):
            return p
    return os.path.join(AQUI, "..", "assets", "Plantilla_Conciliacion_Banco_Odoo_CFDI.xlsx")


# ---------------------------------------------------------------- range rewriting
def reescribe(formula, hoja_actual, cambios, solo_rangos=False):
    """cambios: sheet -> (old_last, new_last). Range ends at old_last go to new_last; rows below the
    table move with it. solo_rangos=True for formulas inside the table rows themselves."""
    tok = Tokenizer(formula)
    for t in tok.items:
        if t.type != "OPERAND" or t.subtype != "RANGE":
            continue
        m = REF.match(t.value)
        if not m:
            continue
        sh = (m.group("sh") or hoja_actual).strip("'")
        if sh not in cambios:
            continue
        viejo, nuevo = cambios[sh]
        delta = nuevo - viejo

        def mueve(ref, es_rango):
            def f(mm):
                r = int(mm.group(4))
                if r == viejo and (es_rango or not solo_rangos):
                    r = nuevo
                elif r > viejo and not solo_rangos:
                    r += delta
                return "%s%s%s%d" % (mm.group(1), mm.group(2), mm.group(3), r)
            return CELDA.sub(f, ref)
        a, b = m.group("a"), m.group("b")
        pre = t.value[:m.start("a")]
        if b:
            t.value = pre + a + ":" + mueve(b, True) if solo_rangos else pre + mueve(a, False) + ":" + mueve(b, True)
        else:
            t.value = pre + mueve(a, False)
    return "=" + "".join(t.value for t in tok.items)


def largo_tabla(ws, inicio, col):
    c = column_index_from_string(col)
    ultimo = inicio
    for r in range(inicio, ws.max_row + 1):
        v = ws.cell(r, c).value
        if isinstance(v, str) and v.startswith("="):
            ultimo = r
    return ultimo


def redimensiona(wb, nuevos):
    """nuevos: sheet -> number of data rows. Returns sheet -> (first, last) of the resized tables."""
    cambios, info = {}, {}
    for sh, (ini, colf, c1, c2) in TABLAS.items():
        ws = wb[sh]
        viejo = largo_tabla(ws, ini, colf)
        nuevo = ini + max(nuevos.get(sh, 0), 1) - 1
        cambios[sh] = (viejo, nuevo)
        # template row = first data row: styles and formulas
        patron = {}
        for c in range(column_index_from_string(c1), column_index_from_string(c2) + 1):
            cel = ws.cell(ini, c)
            patron[c] = (cel.value if isinstance(cel.value, str) and cel.value.startswith("=") else None, copy.copy(cel._style))
        seg = {}
        for c in patron:  # second row pattern for running balances (G9 = G8 + ...)
            v = ws.cell(ini + 1, c).value
            if isinstance(v, str) and v.startswith("="):
                seg[c] = v
        info[sh] = dict(ini=ini, viejo=viejo, nuevo=nuevo, patron=patron, seg=seg, c1=c1, c2=c2, alto=ws.row_dimensions[ini].height)
    # 1. rewrite every formula outside the table rows
    for ws in wb.worksheets:
        t = info.get(ws.title)
        for row in ws.iter_rows():
            for c in row:
                if not (isinstance(c.value, str) and c.value.startswith("=")):
                    continue
                if t and t["ini"] <= c.row <= t["viejo"] and column_index_from_string(t["c1"]) <= c.column <= column_index_from_string(t["c2"]):
                    continue
                c.value = reescribe(c.value, ws.title, cambios)
    # 2. move the rows under each table, clear the table and write the pattern rows
    for sh, t in info.items():
        ws = wb[sh]
        delta = t["nuevo"] - t["viejo"]
        c1, c2 = column_index_from_string(t["c1"]), column_index_from_string(t["c2"])
        for r in range(t["ini"], t["viejo"] + 1):          # empty the old table
            for c in range(c1, c2 + 1):
                cel = ws.cell(r, c)
                cel.value = None
                cel.style = "Normal"
        if delta and ws.max_row > t["viejo"]:
            merges = [m for m in ws.merged_cells.ranges if m.min_row > t["viejo"]]
            for m in merges:
                ws.unmerge_cells(str(m))
            ws.move_range("A%d:%s%d" % (t["viejo"] + 1, get_column_letter(ws.max_column), ws.max_row), rows=delta, translate=False)
            for m in merges:
                ws.merge_cells(start_row=m.min_row + delta, end_row=m.max_row + delta, start_column=m.min_col, end_column=m.max_col)
        for r in range(t["ini"], t["nuevo"] + 1):
            for c in range(c1, c2 + 1):
                cel = ws.cell(r, c)
                f, estilo = t["patron"][c]
                cel._style = copy.copy(estilo)
                if not f:
                    continue
                if r > t["ini"] and c in t["seg"]:
                    base, origen = t["seg"][c], "%s%d" % (get_column_letter(c), t["ini"] + 1)
                else:
                    base, origen = f, "%s%d" % (get_column_letter(c), t["ini"])
                g = Translator(base, origin=origen).translate_formula("%s%d" % (get_column_letter(c), r))
                cel.value = reescribe(g, sh, cambios, solo_rangos=True)
            if t["alto"]:
                ws.row_dimensions[r].height = t["alto"]
        # conditional formats, filters, validations
        cf = ws.conditional_formatting
        nuevas = []
        for rng in list(cf):
            sq = re.sub(r"(\d+)$", lambda m: str(t["nuevo"]) if int(m.group(1)) == t["viejo"] else m.group(1), str(rng.sqref))
            nuevas.append((sq, rng.rules))
        cf._cf_rules.clear()
        for sq, rules in nuevas:
            for rule in rules:
                ws.conditional_formatting.add(sq, rule)
        if ws.auto_filter.ref:
            ws.auto_filter.ref = re.sub(r"\d+$", str(t["nuevo"]), ws.auto_filter.ref)
    return cambios


# ---------------------------------------------------------------- styling helpers
def estilo_encabezado(c):
    c.font = Font(name="Lexend", size=9, bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor=TEAL)
    c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)


def estilo_dato(c, captura=False, fmt=None):
    c.font = Font(name="Lexend", size=9, color=TINTA)
    c.border = Border(bottom=Side(style="thin", color="D8DEE0"))
    c.alignment = Alignment(vertical="top", wrap_text=True)
    if captura:
        c.fill = PatternFill("solid", fgColor=AZUL)
    if fmt:
        c.number_format = fmt


def cabecera_hoja(ws, titulo, sub, linea):
    ws["C1"], ws["C2"], ws["C3"], ws["A5"] = "MLR CONSULTORES", titulo, sub, linea
    for k, sz in (("C1", 9), ("C2", 14), ("C3", 10)):
        ws[k].font = Font(name="Lexend", size=sz, bold=k != "C3", color=TEAL)
    ws["A5"].font = Font(name="Lexend", size=9, italic=True, color="5A6B6E")


NUM = '#,##0.00;\\(#,##0.00\\);\\-'


# ---------------------------------------------------------------- main fill
def llena(J, salida, plantilla, anterior=None):
    P = J["params"]
    wb = openpyxl.load_workbook(plantilla)
    B, filas, fvo = J["estado_cuenta"], J["conciliacion"], J["facturas_vs_odoo"]
    aux = J["auxiliar"]
    imp = J["impuestos"]
    redimensiona(wb, {"Estado de cuenta": len(B["movimientos"]), "Auxiliar Odoo": len(aux["renglones"]), "Conciliación": len(filas),
                      "Facturas vs Odoo": len(fvo), "Impuestos vs Odoo": len(imp["detalle"])})
    fd = lambda s: datetime.date.fromisoformat(s[:10]) if s else None
    d0 = fd(P["desde"])
    mes = "%s %d" % (MESES[d0.month - 1], d0.year)
    sub = "%s  ·  %s" % (P.get("empresa") or P.get("empresa_corta", ""), mes)
    for ws in wb.worksheets:
        if isinstance(ws["C3"].value, str) and "·" in ws["C3"].value or ws["C3"].value is None and ws["C1"].value == "MLR CONSULTORES":
            ws["C3"] = sub
    wb["Resumen"]["A5"] = "Cuenta %s · Periodo %s al %s. Todo se calcula solo a partir de las hojas del libro." % (
        P.get("cuenta_banco") or B["caratula"].get("cuenta", ""), fd(P["desde"]).strftime("%d/%m/%Y"), fd(P["hasta"]).strftime("%d/%m/%Y"))
    wb["Guía"]["C40"] = ("Fuentes: estado de cuenta %s de %s (%s); de Odoo, el auxiliar del diario %s, las facturas del mes y el libro mayor "
                         "de las cuentas de IVA en flujo; CFDI del acumulado de Mi Admin y de los XML, con sus complementos de pago."
                         % (B["caratula"].get("banco") or P.get("banco", "del banco"), mes.lower(), B.get("fuente", "PDF"), P.get("diario", "")))
    wb["Auxiliar Odoo"]["A5"] = "Exportado de Odoo, diario %s. Se usa tal como llegó; no se edita." % P.get("diario", "")
    wb["Impuestos vs Odoo"]["A12"] = ("Signos: el IVA trasladado se muestra en positivo para leerlo igual que el acreditable. Fuente: libro mayor de %s "
                                      "leído de Odoo." % mes.lower())
    pv = wb["Previo"]
    pv["C7"] = "Cálculo de impuestos correspondientes al mes de %s" % mes
    pv["H19"] = ("Primer ejercicio (inició el %s): sin pago provisional según el art. 14 de la LISR. Por confirmar." % P["inicio_operaciones"]
                 if P.get("primer_ejercicio") else "Captura el pago provisional determinado en el papel de trabajo.")
    man = P.get("previo_manual")
    if man:
        for fila, k in ((43, "iva_cobrado"), (44, "iva_pagado"), (45, "iva_retenido"), (46, "isr_retenido")):
            pv.cell(fila, 5).value = man.get(k)
        pv["C47"] = "Fuente de la columna Manual: previo del analista para %s. Se borra al terminar las pruebas." % mes.lower()
    else:
        for r in range(41, 48):
            for c in range(3, 9):
                pv.cell(r, c).value = None
    # --- Estado de cuenta
    ws = wb["Estado de cuenta"]
    for i, m in enumerate(B["movimientos"]):
        r = 8 + i
        for c, v in zip("ABCDEF", (m["partida"], fd(m["fecha"]), m.get("codigo"), m["descripcion"], m.get("cargo"), m.get("abono"))):
            ws["%s%d" % (c, r)] = v
    car = B["caratula"]
    for fila, k in ((8, "banco"), (9, "producto"), (10, "titular"), (11, "rfc"), (12, "cuenta"), (13, "clabe"), (14, "cliente"),
                    (16, "saldo_inicial"), (17, "abonos"), (18, "cargos"), (19, "saldo_final"), (20, "saldo_promedio"), (21, "comisiones")):
        ws.cell(fila, 12).value = car.get(k)
    ws["M17"], ws["M18"] = car.get("n_abonos"), car.get("n_cargos")
    # --- Auxiliar
    ws = wb["Auxiliar Odoo"]
    for i, a in enumerate(aux["renglones"]):
        r = 8 + i
        for c, v in zip("ABCDEFG", (a["renglon"], fd(a["fecha"]), a["asiento"], a["concepto"], a["contacto"], a.get("cargo"), a.get("abono"))):
            ws["%s%d" % (c, r)] = v
    ws["J12"] = aux["saldo_inicial"]
    # --- Conciliación
    ws = wb["Conciliación"]
    col = {"partida": "A", "fecha_banco": "B", "concepto_banco": "C", "cargo_banco": "D", "abono_banco": "E", "renglon_odoo": "F",
           "fecha_odoo": "G", "asiento": "H", "contacto": "I", "cargo_odoo": "J", "abono_odoo": "K", "enlace": "N", "uuid": "O",
           "folio": "P", "fecha_cfdi": "Q", "contraparte": "R", "rfc": "S", "metodo": "T", "tipo_ret": "U", "total_cfdi": "V",
           "aplicado": "W", "dias_pago": "AB", "observacion": "AE", "base_cfdi": "AF", "iva_cfdi": "AG", "ivaret_cfdi": "AH",
           "isrret_cfdi": "AI", "tipo": "AJ", "primera": "AL"}
    gris = PatternFill("solid", fgColor="F2F4F5")
    for i, f in enumerate(filas):
        r = 8 + i
        for k, c in col.items():
            v = f.get(k)
            if k.startswith("fecha"):
                v = fd(v) if v else None
            if k in ("cargo_banco", "abono_banco", "cargo_odoo", "abono_odoo") and not v:
                v = None
            ws["%s%d" % (c, r)] = v
        if not f["primera"]:
            for c in "ABCDE":
                ws["%s%d" % (c, r)].fill = gris
                ws["%s%d" % (c, r)].font = Font(name="Lexend", size=9, color="8A9699")
    # --- Facturas vs Odoo
    ws = wb["Facturas vs Odoo"]
    for i, x in enumerate(fvo):
        r = 8 + i
        for c, k in zip("ABCDEFGHIJ", ("tipo", "numero", "uuid", "fecha", "contraparte", "estado_sat", "total_cfdi", "estado_odoo", "total_odoo", "pendiente")):
            v = x.get(k)
            ws["%s%d" % (c, r)] = fd(v) if k == "fecha" and v else (v if v != "" else None)
        ws["M%d" % r] = x.get("observacion") or None
    # --- Impuestos vs Odoo
    ws = wb["Impuestos vs Odoo"]
    for s in imp["saldos"]:
        fila = 9 if s["cuenta"] == P["cuentas"].get("iva_acreditable_pagado") else 10
        ws.cell(fila, 1).value, ws.cell(fila, 2).value = s["cuenta"], s["nombre"]
        ws.cell(fila, 3).value, ws.cell(fila, 5).value = s["saldo_inicial"], s["saldo_final"]
    for i, x in enumerate(imp["detalle"]):
        r = 16 + i
        for c, k in zip("ABCDEF", ("iva", "cuenta", "factura", "contacto", "uuid", "iva_odoo")):
            ws["%s%d" % (c, r)] = x.get(k) or (0 if k == "iva_odoo" else None)
        ws["J%d" % r], ws["K%d" % r] = x.get("observacion") or None, x.get("diario") or None
    parches(wb, len(imp["detalle"]))
    wb["Reglas"]["C7"], wb["Reglas"]["C8"] = float(P.get("tolerancia_importe", 1.0)), int(P.get("tolerancia_dias", 3))
    hojas_control(wb, J, sub)
    if anterior:
        conserva_capturas(wb, anterior)
    wb.calculation.fullCalcOnLoad = True
    wb.save(salida)
    return salida


def parches(wb, n_imp):
    """Improvements over the template. Safe to apply twice."""
    im = wb["Impuestos vs Odoo"]
    last = 16 + max(n_imp, 1) - 1
    for r in range(16, last + 1):
        v = im["I%d" % r].value
        if isinstance(v, str):
            im["I%d" % r].value = v.replace('ISNUMBER(SEARCH("CSH1",K%d))' % r, 'ISNUMBER(SEARCH("Pagada por caja",J%d))' % r)
    # explanation block under the detail: restore its labels and read cash journals from the observation
    base = last + 4
    etiquetas = ["¿De dónde salen las diferencias de IVA?",
                 "IVA en Odoo de facturas que la conciliación no encontró cobradas en el banco",
                 "IVA en Odoo mayor al de la conciliación en facturas encontradas",
                 "IVA acreditable pagado por caja, que no pasa por el banco",
                 "IVA acreditable de otras facturas no encontradas en el banco",
                 "IVA acreditable de facturas de meses anteriores (sin folio fiscal)",
                 "Referencia: IVA del excedente de los depósitos en revisión (excedente / 1.16 x 0.16)"]
    for i, t in enumerate(etiquetas):
        im.cell(base - 1 + i, 1).value = t
        im.cell(base - 1 + i, 1).font = Font(name="Lexend", size=9, bold=i == 0, color=TEAL if i == 0 else TINTA)
    for r in range(base, base + 7):
        v = im.cell(r, 6).value
        if isinstance(v, str) and '"*CSH1*"' in v:
            im.cell(r, 6).value = re.sub(r"'Impuestos vs Odoo'!\$K\$(\d+):\$K\$(\d+)", r"'Impuestos vs Odoo'!$J$\1:$J$\2", v).replace('"*CSH1*"', '"*Pagada por caja*"')
    rs = wb["Resumen"]
    rs["G21"] = 'Importe pagado a "COMISIONES" sin CFDI'
    rs["C34"] = "¿Se puede enviar el Previo al cliente?"
    rs["C34"].font = Font(name="Lexend", size=10, bold=True, color=TEAL)
    rs["C35"] = ('=IF(AND(H11=0,H12=0,ABS(D23)<=Reglas!$C$7,ABS(D24)<=Reglas!$C$7,'
                 "ABS('Desglose fiscal'!B40)+ABS('Desglose fiscal'!C40)<=Reglas!$C$7,ABS(H31)<=Reglas!$C$7,ABS(H32)<=Reglas!$C$7),"
                 '"Sí. Todo el flujo del mes quedó explicado y el IVA coincide con Odoo.",'
                 '"Todavía no. Hay partidas sin identificar o por revisar, excedentes o diferencias de IVA contra Odoo que cambian el Previo.")')
    rs["C35"].alignment = Alignment(wrap_text=True, vertical="top")
    rs.merge_cells("C35:H35") if "C35:H35" not in [str(m) for m in rs.merged_cells.ranges] else None
    rs.row_dimensions[35].height = 30
    pv = wb["Previo"]
    pv["C8"] = '=IF(LEFT(Resumen!C35,2)="Sí","","PRELIMINAR INCOMPLETO: "&Resumen!C35)'
    pv["C8"].font = Font(name="Lexend", size=9, bold=True, color="B23A3A")


def hojas_control(wb, J, sub):
    """Acciones, Verificación and Bitácora, the approval layer of MLR_Plantilla_Conciliacion_Bancaria_Odoo.xlsx."""
    for n in ("Acciones", "Verificación", "Bitácora"):
        if n in wb.sheetnames:
            del wb[n]
    ws = wb.create_sheet("Acciones", 2)
    cabecera_hoja(ws, "Acciones propuestas y aprobación", sub,
                  "La skill propone, tú apruebas y la skill aplica solo las filas con Aprobado = Sí. Aprobar una fila no aprueba la siguiente.")
    cab = ["ID", "Tipo", "Partida", "Importe", "Concepto", "Documentos", "Propuesta", "Regla", "Confianza", "Operación (la llena la skill)",
           "Aprobado", "Comentario", "Estado", "IDs resultado", "Verificado"]
    anchos = [7, 13, 9, 12, 38, 16, 48, 8, 10, 30, 10, 30, 11, 16, 10]
    for j, (h, w) in enumerate(zip(cab, anchos), 1):
        estilo_encabezado(ws.cell(7, j, h))
        ws.column_dimensions[get_column_letter(j)].width = w
    for j in (11, 12):
        ws.cell(7, j).fill = PatternFill("solid", fgColor=CAFE)
    acc = J.get("acciones", [])
    for i, a in enumerate(acc, 8):
        vals = [a["id"], a["tipo"], a.get("partida"), a.get("importe"), a.get("concepto"), a.get("documentos"), a.get("propuesta"),
                a.get("regla"), a.get("confianza"), json.dumps(a["operacion"], ensure_ascii=False) if a.get("operacion") else "",
                a.get("aprobado") or None, a.get("comentario"), a.get("estado", "Pendiente"), a.get("ids_resultado"), a.get("verificado")]
        for j, v in enumerate(vals, 1):
            estilo_dato(ws.cell(i, j, v), captura=j in (11, 12), fmt=NUM if j == 4 else None)
    last = max(8, 7 + len(acc))
    for rng, lista in (("K8:K%d" % (last + 50), '"Sí,No,Modificar"'), ("M8:M%d" % (last + 50), '"Pendiente,Aplicado,Resuelto,Error,Revalidar"'),
                       ("O8:O%d" % (last + 50), '"Sí,No"')):
        dv = DataValidation(type="list", formula1=lista, allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(rng)
    ws.freeze_panes = "C8"
    # Verificación
    ws = wb.create_sheet("Verificación", 3)
    cabecera_hoja(ws, "Verificación de cierre del diario", sub,
                  "El diario se cierra cuando todos los controles dicen OK. Los que dicen «lo escribe la skill» se leen de Odoo al terminar.")
    for j, h in enumerate(["Control", "Valor", "Esperado", "Resultado", "Fuente"], 1):
        estilo_encabezado(ws.cell(7, j, h))
    for j, w in enumerate([52, 16, 16, 12, 52], 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ok = lambda r: '=IF(B{0}="","Pendiente",IF(ROUND(B{0}-C{0},2)=0,"OK","Revisar"))'.format(r)
    ctr = [("Diferencia del PDF contra la carátula", "='Estado de cuenta'!L27", 0, "Estado de cuenta"),
           ("Movimientos del PDF contra la carátula", "='Estado de cuenta'!M27", 0, "Estado de cuenta"),
           ("Partidas no identificadas", "=Resumen!H12", 0, "Resumen, pregunta 2"),
           ("Partidas por revisar sin explicación aceptada", '=COUNTIFS(Conciliación!$AL:$AL,1,Conciliación!$AD:$AD,"Conciliado (revisar)",Conciliación!$AE:$AE,"<>*aceptada por el usuario*")', 0, "Conciliación"),
           ("Diferencia del flujo explicado, cobros", "=Resumen!D23", 0, "Desglose fiscal"),
           ("Diferencia del flujo explicado, pagos", "=Resumen!D24", 0, "Desglose fiscal"),
           ("Saldo final de Odoo menos saldo del banco", "=Resumen!H14", 0, "Auxiliar Odoo"),
           ("Acciones aprobadas pendientes de aplicar o de resolver", '=COUNTIFS(Acciones!$K:$K,"Sí",Acciones!$M:$M,"<>Aplicado",Acciones!$M:$M,"<>Resuelto")', 0, "Acciones"),
           ("Acciones con error o por revalidar", '=COUNTIF(Acciones!$M:$M,"Error")+COUNTIF(Acciones!$M:$M,"Revalidar")', 0, "Acciones"),
           ("Acciones aplicadas sin verificar", '=COUNTIFS(Acciones!$M:$M,"Aplicado",Acciones!$O:$O,"<>Sí")', 0, "Acciones"),
           ("Líneas de extracto sin conciliar en Odoo (lo escribe la skill)", None, 0, "account.bank.statement.line"),
           ("Saldo de la cuenta de suspenso (lo escribe la skill)", None, 0, "Cuenta de suspenso del diario"),
           ("Pagos y asientos creados sin aprobación (lo escribe la skill)", None, 0, "Conteo antes y después contra la bitácora"),
           ("Suma total de la balanza (lo escribe la skill)", None, 0, "Balanza de comprobación")]
    for i, (n, f, esp, fu) in enumerate(ctr, 8):
        for j, v in enumerate([n, f, esp, ok(i), fu], 1):
            estilo_dato(ws.cell(i, j, v), fmt=NUM if j in (2, 3) else None)
    fin = 8 + len(ctr)
    ws.cell(fin + 1, 1, "Estado del diario")
    ws.cell(fin + 1, 1).font = Font(name="Lexend", size=10, bold=True, color=TEAL)
    ws.cell(fin + 1, 4, '=IF(COUNTIF(D8:D%d,"Revisar")+COUNTIF(D8:D%d,"Pendiente")=0,"CERRADO","ABIERTO")' % (fin - 1, fin - 1))
    ws.cell(fin + 1, 4).font = Font(name="Lexend", size=10, bold=True, color=CAFE)
    # Bitácora
    ws = wb.create_sheet("Bitácora", 4)
    cabecera_hoja(ws, "Bitácora de escrituras en Odoo", sub,
                  "Una fila por escritura. La llena la skill desde bitacora.jsonl; cada fila apunta a su respaldo JSON para revertir.")
    for j, (h, w) in enumerate(zip(["Fecha y hora", "Aprobación", "Entorno", "Modelo", "Método", "IDs", "Valores anteriores", "Valores nuevos",
                                    "Resultado", "Respaldo", "Usuario"], [17, 11, 10, 22, 18, 14, 40, 40, 22, 30, 26]), 1):
        estilo_encabezado(ws.cell(7, j, h))
        ws.column_dimensions[get_column_letter(j)].width = w
    for i, b in enumerate(J.get("bitacora", []), 8):
        for j, k in enumerate(["fecha", "aprobacion", "entorno", "modelo", "metodo", "ids", "antes", "nuevos", "resultado", "respaldo", "usuario"], 1):
            v = b.get(k)
            estilo_dato(ws.cell(i, j, v if isinstance(v, (str, int, float)) or v is None else json.dumps(v, ensure_ascii=False, default=str)[:3000]))


def conserva_capturas(wb, anterior):
    """Carry over the light-blue captures and the approvals of a previous run.

    An approval only survives if the operation it approved is the same one. When the new run proposes a
    different operation for the same item, the approval is dropped and the comment says why. An operation
    completed in the chat (new run proposes none) is carried over together with its approval."""
    old = openpyxl.load_workbook(anterior)
    pv_o, pv_n = old["Previo"], wb["Previo"]
    for k in ("E12", "E19", "E20", "E21", "E27"):
        pv_n[k] = pv_o[k].value
    rg_o, rg_n = old["Reglas"], wb["Reglas"]
    for k in ("C32", "C33", "C34", "C35"):
        rg_n[k] = rg_o[k].value
    if "Acciones" not in old.sheetnames:
        return
    a = old["Acciones"]
    prev = {}
    for r in range(8, a.max_row + 1):
        if a.cell(r, 1).value:
            prev[(a.cell(r, 2).value, a.cell(r, 3).value, a.cell(r, 5).value)] = [a.cell(r, j).value for j in range(1, 16)]
    ws = wb["Acciones"]
    for r in range(8, ws.max_row + 1):
        clave = (ws.cell(r, 2).value, ws.cell(r, 3).value, ws.cell(r, 5).value)
        v = prev.get(clave)
        if not v:
            continue
        op_new, op_old = ws.cell(r, 10).value or "", v[9] or ""
        if not op_new and op_old:
            ws.cell(r, 10).value = op_old                     # completed in the chat
            op_new = op_old
        mismo = _json_igual(op_new, op_old)
        for j in (11, 12, 13, 14, 15):
            val = v[j - 1]
            if val in (None, ""):
                continue
            if j == 11 and not mismo:
                ws.cell(r, 12).value = ((v[11] or "") + " | La operación cambió desde la aprobación: vuelve a aprobar").strip(" |")
                continue
            if j in (13, 14, 15) and not mismo and v[12] != "Aplicado":
                continue
            ws.cell(r, j).value = val if j != 12 or ws.cell(r, 12).value in (None, "") else ws.cell(r, 12).value


def _json_igual(a, b):
    try:
        return json.loads(a or "null") == json.loads(b or "null")
    except ValueError:
        return (a or "") == (b or "")


# ---------------------------------------------------------------- recalculation
def recalcula(ruta):
    """Recalculate with LibreOffice and read back every value; returns (n_formulas, errors)."""
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        return None, ["LibreOffice no está instalado: Excel recalcula al abrir, pero no se pudo revisar errores aquí"]
    tmp = tempfile.mkdtemp()
    perfil = "file://" + os.path.join(tmp, "perfil")
    subprocess.run([soffice, "-env:UserInstallation=" + perfil, "--headless", "--calc", "--convert-to", "xlsx", "--outdir", tmp, ruta],
                   check=True, capture_output=True, timeout=240)
    calc = os.path.join(tmp, os.path.basename(ruta))
    wf, wv = openpyxl.load_workbook(ruta), openpyxl.load_workbook(calc, data_only=True)
    n, errores = 0, []
    for ws in wf.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("="):
                    n += 1
                    v = wv[ws.title][c.coordinate].value
                    if isinstance(v, str) and v.startswith("#") or v in ("#REF!", "#VALUE!", "#NAME?", "#DIV/0!", "Err:502", "Err:504"):
                        errores.append("%s!%s %s" % (ws.title, c.coordinate, v))
    return n, errores, calc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("conciliacion")
    ap.add_argument("salida")
    ap.add_argument("--plantilla")
    ap.add_argument("--anterior")
    ap.add_argument("--sin-recalculo", action="store_true")
    a = ap.parse_args()
    J = json.load(open(a.conciliacion))
    carpeta = os.path.dirname(os.path.abspath(a.conciliacion))
    bit = os.path.join(carpeta, "bitacora.jsonl")
    if os.path.exists(bit):
        J["bitacora"] = [json.loads(x) for x in open(bit) if x.strip()]
    plantilla = a.plantilla or plantilla_por_defecto()
    llena(J, a.salida, plantilla, a.anterior)
    print("Libro:", a.salida, "· plantilla:", plantilla)
    if not a.sin_recalculo:
        res = recalcula(a.salida)
        if res[0] is None:
            print("  aviso:", res[1][0])
            return
        n, err, calc = res
        print("  %d fórmulas recalculadas, %d con error" % (n, len(err)))
        for e in err[:20]:
            print("   ", e)
        if err:
            sys.exit(3)
        # keep the recalculated copy next to it so Resumen values can be read by verificar.py
        shutil.copy(calc, a.salida.replace(".xlsx", "") + ".calc.xlsx")


if __name__ == "__main__":
    main()

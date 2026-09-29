# -*- coding: utf-8 -*-
"""Record in the workbook and in decisiones.json what the person decided in the chat.

    python3 acciones.py completar  <libro.xlsx> A004 '{"op": "asiento_manual", ...}'   # operation completed in the chat
    python3 acciones.py aprobar    <libro.xlsx> A004 "Aprobado en el chat por <nombre>"   # only after an explicit yes
    python3 acciones.py rechazar   <libro.xlsx> A004 "motivo"
    python3 acciones.py resolver   <libro.xlsx> A001 "Se decidió no cambiar el diario de base de efectivo"
    python3 acciones.py enlace     <carpeta> B-068 <UUID> <importe>                       # breaks a tie (E11)
    python3 acciones.py aceptar    <carpeta> B-069 "Pago registrado con la fecha de la factura"
    python3 acciones.py no-requiere <carpeta> B-058 "Traspaso a la cuenta de inversión"

The first five edit the Acciones sheet (close Excel first). The last three edit decisiones.json in the
journal's work folder; the next corrida.py applies them and they survive every later run.
"resolver" is for rows that need no write in Odoo (a configuration finding the person decided to leave,
an answered question): they stop blocking the close. "aprobar" never runs on the assistant's own
initiative: it records a yes the person gave in the chat.
"""
import json
import os
import sys

import openpyxl

COL = {"operacion": 10, "aprobado": 11, "comentario": 12, "estado": 13}
CAMPOS = {"registrar_pago": {"factura_ids", "importe", "fecha"}, "asiento_manual": {"diario_id", "fecha", "lineas"},
          "linea_extracto": {"statement_line_id", "contrapartidas"}, "conciliar_apuntes": {"line_ids"},
          "ligar_xml": {"factura_id", "xml_ruta"}, "adjuntar_rep": {"res_model", "res_id", "xml_ruta", "nota"},
          "escribir_campos": {"modelo", "ids", "valores"}}


def fila(ws, ident):
    for r in range(8, ws.max_row + 1):
        if ws.cell(r, 1).value == ident:
            return r
    raise SystemExit("No existe la acción %s en la hoja Acciones" % ident)


def libro(cmd, ruta, ident, valor):
    wb = openpyxl.load_workbook(ruta)
    ws = wb["Acciones"]
    r = fila(ws, ident)
    com = ws.cell(r, COL["comentario"]).value or ""
    if cmd == "completar":
        op = json.loads(valor)
        falta = CAMPOS.get(op.get("op"), {"op"}) - set(op)
        if op.get("op") not in CAMPOS or falta:
            raise SystemExit("Operación incompleta: %s" % (sorted(falta) or "tipo desconocido %r" % op.get("op")))
        if op["op"] == "asiento_manual" and round(sum((l.get("debe") or 0) - (l.get("haber") or 0) for l in op["lineas"]), 2):
            raise SystemExit("El asiento no cuadra")
        ws.cell(r, COL["operacion"]).value = json.dumps(op, ensure_ascii=False)
        if ws.cell(r, COL["aprobado"]).value == "Sí":   # a new operation needs a new approval
            ws.cell(r, COL["aprobado"]).value = None
            com = (com + " | Operación completada: vuelve a aprobar").strip(" |")
    elif cmd == "aprobar":
        if not ws.cell(r, COL["operacion"]).value and ws.cell(r, 2).value not in ("Configuración", "Pregunta", "Pedir CFDI", "Revisión"):
            raise SystemExit("La fila no tiene operación: complétala antes de aprobar")
        ws.cell(r, COL["aprobado"]).value = "Sí"
        com = (com + " | " + valor).strip(" |")
    elif cmd == "rechazar":
        ws.cell(r, COL["aprobado"]).value = "No"
        com = (com + " | " + valor).strip(" |")
    elif cmd == "resolver":
        ws.cell(r, COL["estado"]).value = "Resuelto"
        com = (com + " | Resuelto: " + valor).strip(" |")
    ws.cell(r, COL["comentario"]).value = com
    wb.save(ruta)
    print("%s %s: %s" % (ident, cmd, com))


def decisiones(cmd, carpeta, partida, args):
    ruta = os.path.join(carpeta, "decisiones.json")
    d = json.load(open(ruta)) if os.path.exists(ruta) else {}
    for k in ("enlaces", "aceptados", "no_requiere"):
        d.setdefault(k, {})
    if cmd == "enlace":
        d["enlaces"].setdefault(partida, []).append({"uuid": args[0].upper(), "importe": float(args[1])})
    elif cmd == "aceptar":
        d["aceptados"][partida] = args[0]
    elif cmd == "no-requiere":
        d["no_requiere"][partida] = args[0]
    json.dump(d, open(ruta, "w"), ensure_ascii=False, indent=1)
    print("decisiones.json: %s %s" % (cmd, partida))


if __name__ == "__main__":
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd in ("completar", "aprobar", "rechazar", "resolver"):
        libro(cmd, sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd in ("enlace", "aceptar", "no-requiere"):
        decisiones(cmd, sys.argv[2], sys.argv[3], sys.argv[4:])
    else:
        sys.exit(__doc__)

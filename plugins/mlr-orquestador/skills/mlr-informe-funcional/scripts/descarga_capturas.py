# -*- coding: utf-8 -*-
"""Pull the captures that captura_odoo.js left as ir.attachment on the TEST base.

    ODOO_URL=https://cliente-test.odoo.com ODOO_DB=cliente-test ODOO_USER=user@x \
    ODOO_KEY=<api key, from the environment only> \
    python3 descarga_capturas.py <carpeta>/capturas [--rm]

Writes NN.jpg per attachment named mlr_cap_NN.jpg; with --rm deletes them from
the base afterwards. Refuses a URL or database that looks like production unless
ODOO_ES_PRUEBAS=1 is set after Marcos confirmed in the chat that it is a copy.
"""
import base64, os, sys, xmlrpc.client

url, db = os.environ["ODOO_URL"].rstrip("/"), os.environ["ODOO_DB"]
if not any(t in (url + db).lower() for t in ("test", "prueba", "staging", "dup", "edu")) \
        and os.environ.get("ODOO_ES_PRUEBAS") != "1":
    sys.exit("La base no parece de pruebas. Confirmar con Marcos y exportar ODOO_ES_PRUEBAS=1.")
common = xmlrpc.client.ServerProxy(url + "/xmlrpc/2/common", allow_none=True)
uid = common.authenticate(db, os.environ["ODOO_USER"], os.environ["ODOO_KEY"], {})
if not uid:
    sys.exit("No autentico.")
M = xmlrpc.client.ServerProxy(url + "/xmlrpc/2/object", allow_none=True)
x = lambda model, method, *a, **k: M.execute_kw(db, uid, os.environ["ODOO_KEY"], model, method, list(a), k)

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
campos = x("ir.attachment", "fields_get", attributes=["type"])
campo = "raw" if "raw" in campos else "datas"
filas = x("ir.attachment", "search_read", [["name", "like", "mlr_cap_%"]], fields=["id", "name", campo])
for r in filas:
    d = r[campo]
    if isinstance(d, xmlrpc.client.Binary):
        d = d.data
    if isinstance(d, str):
        d = base64.b64decode(d)
    if d[:2] != b"\xff\xd8":      # stored as base64 text
        d = base64.b64decode(d)
    key = r["name"][len("mlr_cap_"):-4]
    open(os.path.join(out, key + ".jpg"), "wb").write(d)
    print(key, len(d))
if "--rm" in sys.argv and filas:
    x("ir.attachment", "unlink", [r["id"] for r in filas])
    print("borradas de la base", len(filas))

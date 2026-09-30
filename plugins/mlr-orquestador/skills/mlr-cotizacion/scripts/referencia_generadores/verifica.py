# -*- coding: utf-8 -*-
from comun import *
import re, json, pymupdf
from openpyxl import load_workbook
wb = load_workbook(os.path.join(OUT, "rec", NX + ".xlsx"), data_only=True)
K = json.load(open(os.path.join(OUT, "celdas.json")))
F, ok = [], [0]
def v(k): s, c = K[k]; return wb[s][c].value
def chk(e, got, exp, tol=0.005):
    if got is None or (isinstance(got, str)): F.append("%s sin evaluar (%r)" % (e, got)); return
    if abs(float(got) - float(exp)) > tol: F.append("%s: %s != %s" % (e, got, exp)); return
    ok[0] += 1
for ws in wb:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and (c.value.startswith("=") or c.value.startswith("#")):
                F.append("%s!%s %s" % (ws.title, c.coordinate, c.value))
chk("ruta total", v("ruta_total"), C["tot"])
for a, hh in C["apps"].items(): chk("app " + a, v("app " + a), hh)
chk("res h", v("res_h"), C["tot"]); chk("res %", v("res_pct"), 1)
chk("res pref", v("res_p"), C["p"])
chk("A anticipo", v("ant"), C["ant"])
for k in C["hitos"]:
    chk(k + " h", v(k + " h"), C["hitos"][k]); chk(k + " $", v(k + " $"), C["hito_saldo"][k])
chk("A total", v("A total"), C["p"]); chk("B", v("B"), C["b"]); chk("C desc", v("Cdesc"), C["desc"])
chk("C pago", v("Cpago"), C["c"]); chk("C tarifa", v("Ctarifa"), C["tarifa_c"])
chk("mezcla total", v("mez_total"), C["tot"])
chk("mezcla conf+datos", v("mez_cd"), C["tipos"]["Configuración"] + C["tipos"]["Datos"])
print("Excel: %d comprobaciones correctas | fallos %d" % (ok[0], len(F)))
for f in F: print("  -", f)

anexo = set()
for ws in wb:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, (int, float)): anexo.add(round(float(c.value), 2))
def texto(n): return re.sub(r"\s+", " ", " ".join(p.get_text() for p in pymupdf.open(os.path.join(OUT, n + ".pdf"))))
t1, t2 = texto(N1), texto(N2)
DIAG = set()
for nom, t in (("Propuesta", t1), ("Plan", t2)):
    mon = sorted(set(float(x.replace(",", "")) for x in re.findall(r"\$([\d,]+\.\d{2})", t)))
    huer = [x for x in mon if round(x, 2) not in anexo and x not in DIAG]
    print("%s: %d importes, sin gemelo en el anexo: %s" % (nom, len(mon), huer or "ninguno"))
    print("   contingencia:", "APARECE" if re.search("contingencia", t, re.I) else "cero")
    for s in ("%s horas" % h(C["tot"]), "%d tareas" % C["n"]):
        if s not in t: print("   FALTA", s)
propios = [x for x in set(float(y.replace(",", "")) for y in re.findall(r"\$([\d,]+\.\d{2})", t2)) if x not in DIAG]
print("Plan con importes de la propuesta:", propios or "ninguno (correcto)")
esper = [C[k] for k in ("p", "ant", "b", "desc", "c", "tarifa_c")] + list(C["hito_saldo"].values()) + [P["tarifa_pref"]]
if KEY == "integral":
    for kk in ("contabilidad", "inventario"):
        X = ruta.cifras(kk); esper += [X["p"], X["b"], X["c"]]
    for i, kk in enumerate(("contabilidad", "inventario", "integral")):
        X = ruta.cifras(kk); chk("op%d h" % i, v("op%d h" % i), X["tot"]); chk("op%d $" % i, v("op%d $" % i), X["p"])
        chk("op%d c" % i, v("op%d c" % i), X["c"]); chk("op%d b" % i, v("op%d b" % i), X["b"])

falta = [x for x in esper if m(x) not in t1]
print("Cifras esperadas en la propuesta: %d | ausentes: %s" % (len(esper), falta or "ninguna"))
for n in (N1, N2): print(n, "planas:", len(pymupdf.open(os.path.join(OUT, n + ".pdf"))))
# internal-only sweep of every client file (xlsx text included)
txt = " ".join(str(c.value) for ws in load_workbook(os.path.join(OUT, NX + ".xlsx")) for row in ws.iter_rows() for c in row if c.value)
print("Anexo contingencia:", "APARECE" if re.search("contingencia", txt, re.I) else "cero")
# offered rate only: no list rate, no preferential rate, no benefit (management, 29-sep-2026)
VETO = r"tarifa de lista|de lista|preferencial|beneficio"
for nom, t in (("Propuesta", t1), ("Plan", t2), ("Anexo", txt)):
    hall = sorted(set(x.lower() for x in re.findall(VETO, t, re.I)))
    print("%s tarifa de lista o preferencial:" % nom, hall or "cero")

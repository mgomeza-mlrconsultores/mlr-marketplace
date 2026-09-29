# -*- coding: utf-8 -*-
"""Bank statement reader: PDF (text layer or OCR), CSV or XLSX -> banco.json with the cover and the control.

    python3 leer_estado_cuenta.py <estado.pdf|.csv|.xlsx> <salida/banco.json> --anio 2026 [--perfil bbva]
           [--caratula caratula.json] [--ocr]

Nothing downstream runs until the control closes at zero:
  calculated closing - cover closing, read credits - cover credits, read debits - cover debits,
  and the movement counts against the cover. If the PDF cover cannot be read, pass the cover
  values typed by the user in caratula.json ({"saldo_inicial": .., "abonos": .., "n_abonos": ..,
  "cargos": .., "n_cargos": .., "saldo_final": ..}).

Profiles describe how each bank prints its detail: date pattern, column headers and cover labels.
BBVA is the one proven on real statements; add banks in PERFILES and in references/codigos-banco.md.
"""
import argparse
import csv
import json
import os
import re
import subprocess
import sys
import unicodedata

MESES = {"ENE": 1, "FEB": 2, "MAR": 3, "ABR": 4, "MAY": 5, "JUN": 6, "JUL": 7, "AGO": 8,
         "SEP": 9, "SET": 9, "OCT": 10, "NOV": 11, "DIC": 12}
IMPORTE = re.compile(r"^-?\$?\(?\d{1,3}(?:,\d{3})*\.\d{2}\)?$")
RFC = re.compile(r"\b([A-ZÑ&]{3,4})\s?(\d{6})\s?([A-Z0-9]{3})\b")
REF = re.compile(r"Ref\.\s*([\w*]+)", re.I)

PERFILES = {
    "bbva": {
        "fecha": re.compile(r"^(\d{2})/([A-Z]{3})$"),
        "dos_fechas": True,                   # FECHA OPER and FECHA LIQ
        "codigo": re.compile(r"^[A-Z]\d{2}$"),
        "columnas": {"cargo": ["CARGOS"], "abono": ["ABONOS"], "saldo": ["OPERACIÓN", "OPERACION"],
                     "saldo_liq": ["LIQUIDACIÓN", "LIQUIDACION"]},
        "fin_detalle": ["Total de Movimientos", "TOTAL IMPORTE CARGOS", "Total de Movimientos"],
        "caratula": {
            "saldo_inicial": [r"Saldo de Liquidaci[oó]n Inicial", r"Saldo Anterior", r"Saldo Inicial"],
            "abonos": [r"Dep[oó]sitos\s*/\s*Abonos\s*\(\+\)"],
            "cargos": [r"Retiros\s*/\s*Cargos\s*\(-\)"],
            "saldo_final": [r"Saldo Final\s*\(\+\)", r"Saldo Final"],
            "saldo_promedio": [r"Saldo Promedio"],
            "comisiones": [r"Total Comisiones", r"Comisiones\s+Cobradas"],
        },
        "datos": {"cuenta": r"No\.?\s*de\s*Cuenta\s*:?\s*(\d{8,12})", "clabe": r"CLABE\s*:?\s*(\d{18})",
                  "cliente": r"No\.?\s*de\s*Cliente\s*:?\s*(\w+)", "rfc": r"R\.?F\.?C\.?\s*:?\s*([A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3})"},
    },
}


def num(s):
    if s is None or s == "":
        return None
    if isinstance(s, (int, float)):
        return round(float(s), 2)
    s = str(s).strip().replace("$", "").replace(" ", "")
    neg = s.startswith("(") and s.endswith(")") or s.startswith("-")
    s = s.strip("()-").replace(",", "")
    try:
        v = round(float(s), 2)
    except ValueError:
        return None
    return -v if neg else v


def norm(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().upper()
    return re.sub(r"\s+", " ", t).strip()


def enriquece(m):
    d = m["descripcion"]
    r = REF.search(d)
    m["referencia"] = r.group(1) if r else ""
    f = RFC.search(d.upper())
    m["rfc"] = "".join(f.groups()) if f else ""
    return m


# ---------------------------------------------------------------- PDF by column position
def _texto_pdf(ruta, ocr=False):
    if ocr:
        # scanned statement: OCR to a searchable PDF first, then read positions as usual
        salida = ruta + ".ocr.pdf"
        subprocess.run(["ocrmypdf", "--force-ocr", "-l", "spa", ruta, salida], check=True)
        return salida
    return ruta


def lee_pdf(ruta, anio, perfil, ocr=False):
    import pdfplumber
    P = PERFILES[perfil]
    ruta = _texto_pdf(ruta, ocr)
    movs, texto_total, cols = [], [], None
    with pdfplumber.open(ruta) as pdf:
        for page in pdf.pages:
            texto_total.append(page.extract_text() or "")
            words = page.extract_words(keep_blank_chars=False, use_text_flow=False, x_tolerance=1.5)
            # group words into lines by their top coordinate
            lineas = {}
            for w in words:
                lineas.setdefault(round(w["top"] / 3), []).append(w)
            for k in sorted(lineas):
                ws = sorted(lineas[k], key=lambda w: w["x0"])
                textos = [w["text"] for w in ws]
                up = [norm(t) for t in textos]
                # header row: remember the x-center of each amount column
                enc = {}
                for nombre, claves in P["columnas"].items():
                    for w, u in zip(ws, up):
                        if u in [norm(c) for c in claves]:
                            enc[nombre] = (w["x0"], w["x1"])
                if "cargo" in enc and "abono" in enc:
                    cols = enc
                    continue
                if cols is None or not ws:
                    continue
                if any(norm(f) in norm(" ".join(textos)) for f in P["fin_detalle"]):
                    cols = None
                    continue
                m = P["fecha"].match(textos[0])
                if m and m.group(2) in MESES:
                    dia, mes = int(m.group(1)), MESES[m.group(2)]
                    resto = ws[2:] if P["dos_fechas"] and len(ws) > 1 and P["fecha"].match(textos[1]) else ws[1:]
                    mov = {"fecha": "%04d-%02d-%02d" % (anio, mes, dia), "codigo": "", "descripcion": "",
                           "cargo": None, "abono": None, "saldo_banco": None}
                    desc = []
                    for w in resto:
                        t = w["text"]
                        if IMPORTE.match(t):
                            # amounts are right-aligned under their header in most statements: compare right edges,
                            # and centers as a second opinion for left-aligned layouts
                            xc = (w["x0"] + w["x1"]) / 2
                            borde = max(cols["cargo"][1], cols["abono"][1])
                            if w["x0"] > borde + 4:
                                # anything right of the cargo/abono columns is a running balance, never an amount
                                col = "saldo" if mov["saldo_banco"] is None else "saldo_liq"
                            else:
                                col = min(("cargo", "abono"), key=lambda c: min(abs(cols[c][1] - w["x1"]), abs((cols[c][0] + cols[c][1]) / 2 - xc)))
                            if col == "cargo":
                                mov["cargo"] = num(t)
                            elif col == "abono":
                                mov["abono"] = num(t)
                            elif col == "saldo":
                                mov["saldo_banco"] = num(t)
                        elif not mov["codigo"] and not desc and P["codigo"].match(t):
                            mov["codigo"] = t
                        else:
                            desc.append(t)
                    mov["descripcion"] = " ".join(desc)
                    movs.append(mov)
                elif movs:
                    # continuation line of the previous movement (reference, RFC, beneficiary)
                    extra = [w["text"] for w in ws if not IMPORTE.match(w["text"])]
                    if extra:
                        movs[-1]["descripcion"] = (movs[-1]["descripcion"] + " " + " ".join(extra)).strip()
    return movs, "\n".join(texto_total)


def lee_caratula(texto, perfil):
    P = PERFILES[perfil]
    car = {}
    for campo, patrones in P["caratula"].items():
        for p in patrones:
            m = re.search(p + r"[^\d\n]{0,40}?(\d+)?\s+\$?\s*(-?[\d,]+\.\d{2})", texto, re.I)
            if m:
                car[campo] = num(m.group(2))
                if campo in ("abonos", "cargos") and m.group(1):
                    car["n_" + campo] = int(m.group(1))
                break
    for campo, p in P["datos"].items():
        m = re.search(p, texto, re.I)
        if m:
            car[campo] = m.group(1)
    return car


# ---------------------------------------------------------------- CSV / XLSX exports
ALIAS = {"fecha": ["fecha", "fecha operacion", "fecha oper", "dia"],
         "descripcion": ["descripcion", "concepto", "concepto / referencia", "detalle", "movimiento"],
         "codigo": ["codigo", "cod", "clave"],
         "cargo": ["cargo", "cargos", "retiro", "retiros", "debito"],
         "abono": ["abono", "abonos", "deposito", "depositos", "credito"],
         "saldo_banco": ["saldo", "saldo operacion"]}


def lee_tabla(ruta):
    if ruta.lower().endswith((".xlsx", ".xlsm")):
        import openpyxl
        ws = openpyxl.load_workbook(ruta, data_only=True).active
        filas = [[c for c in r] for r in ws.iter_rows(values_only=True)]
    else:
        with open(ruta, newline="", encoding="utf-8-sig") as f:
            filas = list(csv.reader(f))
    for i, fila in enumerate(filas):
        cab = [norm(str(c or "")).lower() for c in fila]
        mapa = {k: next((j for j, c in enumerate(cab) if c in v), None) for k, v in ALIAS.items()}
        if mapa["fecha"] is not None and (mapa["cargo"] is not None or mapa["abono"] is not None):
            break
    else:
        raise SystemExit("No encontré encabezados de fecha y cargo/abono en %s" % ruta)
    movs = []
    for fila in filas[i + 1:]:
        g = lambda k: fila[mapa[k]] if mapa[k] is not None and mapa[k] < len(fila) else None
        if not g("fecha"):
            continue
        f = g("fecha")
        f = f.date().isoformat() if hasattr(f, "date") else _fecha_texto(str(f))
        movs.append({"fecha": f, "codigo": str(g("codigo") or ""), "descripcion": str(g("descripcion") or ""),
                     "cargo": num(g("cargo")), "abono": num(g("abono")), "saldo_banco": num(g("saldo_banco"))})
    return movs


def _fecha_texto(s):
    m = re.match(r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})", s)
    if m:
        d, mth, y = m.groups()
        y = int(y) + (2000 if len(y) == 2 else 0)
        return "%04d-%02d-%02d" % (y, int(mth), int(d))
    return s[:10]


# ---------------------------------------------------------------- control
def control(movs, car):
    ab = round(sum(m["abono"] or 0 for m in movs), 2)
    cg = round(sum(m["cargo"] or 0 for m in movs), 2)
    n_ab = sum(1 for m in movs if m["abono"])
    n_cg = sum(1 for m in movs if m["cargo"])
    si = car.get("saldo_inicial")
    c = {"abonos_leidos": ab, "cargos_leidos": cg, "n_abonos_leidos": n_ab, "n_cargos_leidos": n_cg}
    if si is not None:
        c["saldo_final_calculado"] = round(si + ab - cg, 2)
    faltan = [k for k in ("saldo_inicial", "abonos", "cargos", "saldo_final") if car.get(k) is None]
    if faltan:
        c["estado"] = "SIN CARÁTULA: captura %s en caratula.json" % ", ".join(faltan)
        c["cuadra"] = False
        return c
    c["dif_saldo_final"] = round(c["saldo_final_calculado"] - car["saldo_final"], 2)
    c["dif_abonos"] = round(ab - car["abonos"], 2)
    c["dif_cargos"] = round(cg - car["cargos"], 2)
    c["dif_n_abonos"] = n_ab - car["n_abonos"] if car.get("n_abonos") is not None else None
    c["dif_n_cargos"] = n_cg - car["n_cargos"] if car.get("n_cargos") is not None else None
    # running balance printed by the bank, where present, must follow the read amounts
    saldo, rotos = si, []
    for m in movs:
        saldo = round(saldo + (m["abono"] or 0) - (m["cargo"] or 0), 2)
        if m.get("saldo_banco") is not None and abs(saldo - m["saldo_banco"]) > 0.005:
            rotos.append(m["partida"])
            saldo = m["saldo_banco"]
    c["saldo_corrido_roto_en"] = rotos[:10]
    difs = [c["dif_saldo_final"], c["dif_abonos"], c["dif_cargos"], c["dif_n_abonos"] or 0, c["dif_n_cargos"] or 0]
    c["cuadra"] = all(d == 0 for d in difs) and not rotos
    c["estado"] = "CUADRA con la carátula" if c["cuadra"] else "NO CUADRA: corrige la lectura antes de seguir"
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("salida")
    ap.add_argument("--anio", type=int, required=True)
    ap.add_argument("--perfil", default="bbva")
    ap.add_argument("--caratula", help="JSON with the cover values typed by the user")
    ap.add_argument("--ocr", action="store_true")
    a = ap.parse_args()
    car = {}
    if a.entrada.lower().endswith(".pdf"):
        movs, texto = lee_pdf(a.entrada, a.anio, a.perfil, a.ocr)
        if not movs and not a.ocr:
            sys.exit("El PDF no trae capa de texto o el perfil no reconoce el detalle; repite con --ocr o usa el Excel del banco.")
        car = lee_caratula(texto, a.perfil)
    else:
        movs = lee_tabla(a.entrada)
    if a.caratula:
        car.update(json.load(open(a.caratula)))
    for i, m in enumerate(movs, 1):
        m["partida"] = "B-%03d" % i
        enriquece(m)
    c = control(movs, car)
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    json.dump({"fuente": os.path.basename(a.entrada), "perfil": a.perfil, "caratula": car,
               "movimientos": movs, "control": c}, open(a.salida, "w"), ensure_ascii=False, indent=1)
    print("%d movimientos · %s" % (len(movs), c["estado"]))
    for k in ("dif_saldo_final", "dif_abonos", "dif_cargos", "dif_n_abonos", "dif_n_cargos", "saldo_corrido_roto_en"):
        if k in c:
            print("  %s: %s" % (k, c[k]))
    sys.exit(0 if c["cuadra"] else 2)


if __name__ == "__main__":
    main()

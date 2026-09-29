# -*- coding: utf-8 -*-
"""CFDI reader: Mi Admin accumulated workbook and/or ZIP (or folder) of XML -> cfdi.json indexed by UUID.

    python3 leer_cfdi.py <salida/cfdi.json> --rfc-empresa ATA2605052K6
           [--acumulado "XML Acumulados 2026.xlsx"] [--xml carpeta_o.zip ...]

The XML is the source of truth: when both are given, fields read from the XML override the
workbook, and the workbook only adds what the XML does not carry (real payment date, pending
balance, SAT status as last queried by Mi Admin). Payment complements (REP, pago20) are read
with every related document, paid amount and installment number.

Known limits of the Mi Admin workbook (checked on a real case): it has no issuer tax regime,
and for suppliers it only carries LugarExpedicion, which is not necessarily their fiscal zip.
Both come from the XML or from the supplier's Constancia de Situación Fiscal.
"""
import argparse
import datetime
import io
import json
import os
import re
import sys
import unicodedata
import zipfile

NS = {"cfdi": "http://www.sat.gob.mx/cfd/4", "cfdi3": "http://www.sat.gob.mx/cfd/3",
      "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital", "pago20": "http://www.sat.gob.mx/Pagos20",
      "pago10": "http://www.sat.gob.mx/Pagos"}


def norm(t):
    t = unicodedata.normalize("NFKD", str(t or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9%]+", " ", t).strip()


def f2(v):
    try:
        return round(float(str(v).replace(",", "").replace("$", "")), 2) if v not in (None, "") else 0.0
    except ValueError:
        return 0.0


def fecha(v):
    if v in (None, ""):
        return None
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.date().isoformat() if isinstance(v, datetime.datetime) else v.isoformat()
    s = str(v).strip()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return "%s-%s-%s" % m.groups()
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        return "%s-%02d-%02d" % (m.group(3), int(m.group(2)), int(m.group(1)))
    return s[:10]


# ---------------------------------------------------------------- XML
def _uno(nodo, xpath):
    r = nodo.xpath(xpath, namespaces=NS)
    return r[0] if r else None


def lee_xml(contenido, rfc_empresa):
    from lxml import etree
    raiz = etree.fromstring(contenido.lstrip(b"\xef\xbb\xbf"))  # some XML carry a BOM
    ns = "cfdi" if raiz.tag.startswith("{%s}" % NS["cfdi"]) else "cfdi3"
    a = raiz.attrib
    em, rc = _uno(raiz, "%s:Emisor" % ns), _uno(raiz, "%s:Receptor" % ns)
    tfd = _uno(raiz, ".//tfd:TimbreFiscalDigital")
    if tfd is None:
        return None
    imp = _uno(raiz, "%s:Impuestos" % ns)
    iva = iva_ret = isr_ret = 0.0
    if imp is not None:
        for t in imp.xpath("%s:Traslados/%s:Traslado" % (ns, ns), namespaces=NS):
            if t.get("Impuesto") == "002":
                iva += f2(t.get("Importe"))
        for t in imp.xpath("%s:Retenciones/%s:Retencion" % (ns, ns), namespaces=NS):
            if t.get("Impuesto") == "002":
                iva_ret += f2(t.get("Importe"))
            elif t.get("Impuesto") == "001":
                isr_ret += f2(t.get("Importe"))
    rel = []
    for cr in raiz.xpath("%s:CfdiRelacionados" % ns, namespaces=NS):
        for u in cr.xpath("%s:CfdiRelacionado" % ns, namespaces=NS):
            rel.append({"tipo": cr.get("TipoRelacion"), "uuid": u.get("UUID", "").upper()})
    rfc_em = em.get("Rfc") if em is not None else ""
    d = {
        "uuid": tfd.get("UUID", "").upper(), "fuente": "xml", "version": a.get("Version"),
        "tipo": a.get("TipoDeComprobante"), "fecha": fecha(a.get("Fecha")), "fecha_timbrado": tfd.get("FechaTimbrado"),
        "serie": a.get("Serie", ""), "folio": a.get("Folio", ""), "lugar_expedicion": a.get("LugarExpedicion"),
        "rfc_emisor": rfc_em, "nombre_emisor": em.get("Nombre") if em is not None else "",
        "regimen_emisor": em.get("RegimenFiscal") if em is not None else "",
        "rfc_receptor": rc.get("Rfc") if rc is not None else "", "nombre_receptor": rc.get("Nombre") if rc is not None else "",
        "regimen_receptor": rc.get("RegimenFiscalReceptor") if rc is not None else "",
        "cp_receptor": rc.get("DomicilioFiscalReceptor") if rc is not None else "",
        "uso": rc.get("UsoCFDI") if rc is not None else "",
        "subtotal": f2(a.get("SubTotal")), "descuento": f2(a.get("Descuento")), "iva": round(iva, 2),
        "iva_ret": round(iva_ret, 2), "isr_ret": round(isr_ret, 2), "total": f2(a.get("Total")),
        "moneda": a.get("Moneda"), "tipo_cambio": f2(a.get("TipoCambio")) or 1.0,
        "forma_pago": a.get("FormaPago", ""), "metodo_pago": a.get("MetodoPago", ""),
        "conceptos": " | ".join(c.get("Descripcion", "") for c in raiz.xpath("%s:Conceptos/%s:Concepto" % (ns, ns), namespaces=NS))[:500],
        "relacionados": rel, "pagos": [],
    }
    d["direccion"] = "emitido" if rfc_em.upper() == rfc_empresa.upper() else "recibido"
    for pag in raiz.xpath(".//pago20:Pago | .//pago10:Pago", namespaces=NS):
        doctos = [{"uuid": dr.get("IdDocumento", "").upper(), "imp_pagado": f2(dr.get("ImpPagado")),
                   "parcialidad": int(dr.get("NumParcialidad") or 0), "saldo_anterior": f2(dr.get("ImpSaldoAnt")),
                   "saldo_insoluto": f2(dr.get("ImpSaldoInsoluto"))}
                  for dr in pag.xpath("pago20:DoctoRelacionado | pago10:DoctoRelacionado", namespaces=NS)]
        d["pagos"].append({"fecha": fecha(pag.get("FechaPago")), "forma": pag.get("FormaDePagoP"), "monto": f2(pag.get("Monto")),
                           "num_operacion": pag.get("NumOperacion", ""), "doctos": doctos})
    return d


def lee_xml_origen(origen, rfc_empresa):
    """A ZIP (RFC/Emitidas|Recibidas/AAAA/MM/UUID@....xml) or a folder with the same layout."""
    out, malos = {}, []
    if zipfile.is_zipfile(origen):
        z = zipfile.ZipFile(origen)
        items = [(n, lambda n=n: z.read(n)) for n in z.namelist() if n.lower().endswith(".xml")]
    else:
        items = [(os.path.join(r, f), lambda p=os.path.join(r, f): open(p, "rb").read())
                 for r, _, fs in os.walk(origen) for f in fs if f.lower().endswith(".xml")]
    for nombre, leer in items:
        try:
            d = lee_xml(leer(), rfc_empresa)
            if d:
                d["archivo"] = nombre
                out[d["uuid"]] = d
        except Exception as e:
            malos.append("%s: %s" % (nombre, e))
    return out, malos


# ---------------------------------------------------------------- Mi Admin workbook
COLS = {
    "estado_sat": ["estado sat", "estatus sat", "estado"], "version": ["version"], "tipo": ["efecto", "tipo de comprobante", "tipo comprobante", "tipo"],
    "fecha": ["fecha emision", "fecha de emision", "fecha"], "fecha_timbrado": ["fecha timbrado", "fecha de timbrado", "fecha certificacion"],
    "serie": ["serie"], "folio": ["folio"], "uuid": ["uuid", "folio fiscal"], "tipo_relacion": ["tipo relacion", "tipo de relacion"],
    "uuid_relacionado": ["uuid relacionado", "uuids relacionados", "cfdi relacionado"],
    "rfc_emisor": ["rfc emisor"], "nombre_emisor": ["nombre emisor", "razon emisor", "razon social emisor"],
    "lugar_expedicion": ["lugar expedicion", "lugar de expedicion"], "rfc_receptor": ["rfc receptor"],
    "nombre_receptor": ["nombre receptor", "razon receptor", "razon social receptor"], "uso": ["uso cfdi", "uso"],
    "subtotal": ["subtotal", "sub total"], "descuento": ["descuento"], "iva": ["iva 16%", "iva 16", "iva trasladado 16%", "iva"],
    "iva_ret": ["retenido iva", "iva retenido", "ret iva"], "isr_ret": ["retenido isr", "isr retenido", "ret isr"],
    "total": ["total"], "moneda": ["moneda"], "tipo_cambio": ["tipo cambio", "tipo de cambio"],
    "forma_pago": ["forma pago", "forma de pago"], "metodo_pago": ["metodo pago", "metodo de pago"],
    "conceptos": ["conceptos", "concepto", "descripcion"], "archivo": ["archivo xml", "archivo"],
    "regimen_receptor": ["regimenfiscalreceptor", "regimen fiscal receptor"], "cp_receptor": ["domiciliofiscalreceptor", "domicilio fiscal receptor"],
    "fecha_pago_real": ["fecha real de pago", "fecha de pago", "fecha real de cobro", "fecha pago", "fecha cobro"],
    "saldo_pendiente": ["saldo pendiente", "saldo insoluto", "saldo"],
}
COLS_PAGO = {
    "uuid": ["uuid", "uuid rep", "folio fiscal"], "fecha": ["fecha pago", "fecha de pago"], "forma": ["forma de pago", "forma pago", "forma de pago p"],
    "monto": ["monto", "importe"], "uuid_rel": ["uuid relacionado", "id documento", "iddocumento", "documento relacionado"],
    "imp_pagado": ["imp pagado", "importe pagado", "imppagado"], "parcialidad": ["parcialidad", "num parcialidad", "numparcialidad"],
    "num_operacion": ["numero de operacion", "num operacion", "numoperacion"], "cta_ordenante": ["cuenta ordenante", "cta ordenante"],
    "cta_beneficiaria": ["cuenta beneficiaria", "cta beneficiario", "cuenta beneficiario"],
}


def _mapa(cab, cols):
    """Header -> column. Exact names first for every field, then partial matches, so that a column
    such as "Tipo Cambio" is never taken for "Tipo" when "Efecto" or "Tipo de comprobante" exists."""
    n = [norm(c) for c in cab]
    m = {}
    for k, alias in cols.items():
        for al in alias:
            j = next((i for i, c in enumerate(n) if c == al and i not in m.values()), None)
            if j is not None:
                m[k] = j
                break
    exactos = {a for alias in cols.values() for a in alias}
    for k, alias in cols.items():
        if k in m:
            continue
        for al in alias:
            j = next((i for i, c in enumerate(n) if al in c and i not in m.values() and c not in exactos), None)
            if j is not None:
                m[k] = j
                break
    return m


def _hoja(wb, claves):
    for ws in wb.worksheets:
        if all(k in norm(ws.title) for k in claves):
            return ws
    return None


def _filas(ws, cols):
    filas = list(ws.iter_rows(values_only=True))
    for i, f in enumerate(filas[:15]):
        m = _mapa([c for c in f], cols)
        if "uuid" in m and ("total" in m or "monto" in m):
            return m, filas[i + 1:], [c for c in f]
    return None, [], []


def lee_acumulado(ruta, rfc_empresa):
    import openpyxl
    wb = openpyxl.load_workbook(ruta, data_only=True, read_only=True)
    out, avisos = {}, []
    for claves, direccion in ((["emitid"], "emitido"), (["recibid"], "recibido")):
        ws = next((w for w in wb.worksheets if all(k in norm(w.title) for k in claves) and "pago" not in norm(w.title)), None)
        if ws is None:
            avisos.append("No encontré la hoja de CFDI %ss (ACUM. %sS)" % (direccion, direccion.upper()))
            continue
        m, filas, cab = _filas(ws, COLS)
        if not m:
            avisos.append("Hoja %s sin encabezados reconocibles" % ws.title)
            continue
        faltan = [k for k in ("estado_sat", "tipo", "fecha", "uuid", "rfc_emisor", "rfc_receptor", "total", "metodo_pago") if k not in m]
        if faltan:
            avisos.append("%s: no encontré las columnas %s" % (ws.title, ", ".join(faltan)))
        for f in filas:
            g = lambda k: f[m[k]] if k in m and m[k] < len(f) else None
            u = str(g("uuid") or "").strip().upper()
            if len(u) != 36:
                continue
            tipo = str(g("tipo") or "").strip()
            d = {"uuid": u, "fuente": "acumulado", "direccion": direccion, "estado_sat": str(g("estado_sat") or "").strip(),
                 "tipo": {"ingreso": "I", "egreso": "E", "pago": "P", "nomina": "N", "traslado": "T"}.get(norm(tipo), tipo[:1].upper()),
                 "fecha": fecha(g("fecha")), "fecha_timbrado": str(g("fecha_timbrado") or ""), "serie": str(g("serie") or ""),
                 "folio": str(g("folio") or ""), "rfc_emisor": str(g("rfc_emisor") or ""), "nombre_emisor": str(g("nombre_emisor") or ""),
                 "rfc_receptor": str(g("rfc_receptor") or ""), "nombre_receptor": str(g("nombre_receptor") or ""),
                 "lugar_expedicion": str(g("lugar_expedicion") or ""), "uso": str(g("uso") or ""),
                 "subtotal": f2(g("subtotal")), "descuento": f2(g("descuento")), "iva": f2(g("iva")), "iva_ret": f2(g("iva_ret")),
                 "isr_ret": f2(g("isr_ret")), "total": f2(g("total")), "moneda": str(g("moneda") or "MXN"),
                 "tipo_cambio": f2(g("tipo_cambio")) or 1.0, "forma_pago": str(g("forma_pago") or "")[:2],
                 "metodo_pago": str(g("metodo_pago") or "")[:3].upper(), "conceptos": str(g("conceptos") or "")[:500],
                 "regimen_receptor": str(g("regimen_receptor") or ""), "cp_receptor": str(g("cp_receptor") or ""),
                 "fecha_pago_real": fecha(g("fecha_pago_real")), "saldo_pendiente": f2(g("saldo_pendiente")) if g("saldo_pendiente") not in (None, "") else None,
                 "relacionados": [{"tipo": str(g("tipo_relacion") or ""), "uuid": x.strip().upper()}
                                  for x in re.split(r"[,;\s]+", str(g("uuid_relacionado") or "")) if len(x.strip()) == 36],
                 "pagos": [], "archivo": str(g("archivo") or "")}
            out[u] = d
        raros = sorted({d["tipo"] for d in out.values() if d.get("direccion") == direccion and d["tipo"] not in ("I", "E", "P", "N", "T")})
        if raros:
            avisos.append("%s: tipos de comprobante no reconocidos %s; revisa qué columna es el Tipo o Efecto" % (ws.title, raros))
    # payment complements (REP)
    for claves, direccion in ((["pago", "emitid"], "emitido"), (["pago", "recibid"], "recibido")):
        ws = next((w for w in wb.worksheets if all(k in norm(w.title) for k in claves)), None)
        if ws is None:
            continue
        m, filas, _ = _filas(ws, COLS_PAGO)
        if not m:
            avisos.append("Hoja %s sin encabezados reconocibles" % ws.title)
            continue
        for f in filas:
            g = lambda k: f[m[k]] if k in m and m[k] < len(f) else None
            u = str(g("uuid") or "").strip().upper()
            if len(u) != 36:
                continue
            rep = out.setdefault(u, {"uuid": u, "fuente": "acumulado", "direccion": direccion, "tipo": "P", "pagos": [], "total": 0.0,
                                     "relacionados": [], "estado_sat": "Vigente"})
            rel = str(g("uuid_rel") or "").strip().upper()
            fecha_p = fecha(g("fecha"))
            pago = next((p for p in rep["pagos"] if p["fecha"] == fecha_p and p["monto"] == f2(g("monto"))), None)
            if pago is None:
                pago = {"fecha": fecha_p, "forma": str(g("forma") or "")[:2], "monto": f2(g("monto")),
                        "num_operacion": str(g("num_operacion") or ""), "cta_ordenante": str(g("cta_ordenante") or ""),
                        "cta_beneficiaria": str(g("cta_beneficiaria") or ""), "doctos": []}
                rep["pagos"].append(pago)
            if len(rel) == 36:
                pago["doctos"].append({"uuid": rel, "imp_pagado": f2(g("imp_pagado")) or f2(g("monto")),
                                       "parcialidad": int(f2(g("parcialidad")) or 0)})
    return out, avisos


def combina(acum, xmls):
    out = dict(acum)
    for u, x in xmls.items():
        base = out.get(u, {})
        mezcla = dict(base)
        mezcla.update({k: v for k, v in x.items() if v not in (None, "", [])})
        for k in ("estado_sat", "fecha_pago_real", "saldo_pendiente"):  # only the workbook knows these
            if base.get(k) not in (None, ""):
                mezcla[k] = base[k]
        mezcla["fuente"] = "xml+acumulado" if base else "xml"
        out[u] = mezcla
    return out


def indices(cfdis):
    """Lookups used by the matching engine."""
    rep_por_factura = {}
    for u, d in cfdis.items():
        for p in d.get("pagos", []):
            for dr in p["doctos"]:
                rep_por_factura.setdefault(dr["uuid"], []).append({"rep": u, "fecha": p["fecha"], "monto": p["monto"],
                                                                   "imp_pagado": dr["imp_pagado"], "parcialidad": dr.get("parcialidad", 0),
                                                                   "forma": p.get("forma")})
    return {"rep_por_factura": rep_por_factura}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("salida")
    ap.add_argument("--rfc-empresa", required=True)
    ap.add_argument("--acumulado")
    ap.add_argument("--xml", nargs="*", default=[])
    a = ap.parse_args()
    acum, avisos = lee_acumulado(a.acumulado, a.rfc_empresa) if a.acumulado else ({}, [])
    xmls, malos = {}, []
    for o in a.xml:
        x, m = lee_xml_origen(o, a.rfc_empresa)
        xmls.update(x)
        malos += m
    cfdis = combina(acum, xmls)
    solo_acum = [u for u in acum if u not in xmls] if xmls else []
    res = {"cfdi": cfdis, "indices": indices(cfdis), "avisos": avisos + ["XML ilegible: " + m for m in malos],
           "sin_xml": solo_acum}
    json.dump(res, open(a.salida, "w"), ensure_ascii=False, indent=1)
    por = {}
    for d in cfdis.values():
        k = "%s %s" % (d.get("direccion"), d.get("tipo"))
        por[k] = por.get(k, 0) + 1
    print("%d CFDI · %s" % (len(cfdis), ", ".join("%s: %d" % kv for kv in sorted(por.items()))))
    for av in res["avisos"]:
        print("  aviso:", av)
    if solo_acum:
        print("  %d CFDI del acumulado sin XML en el ZIP" % len(solo_acum))


if __name__ == "__main__":
    main()

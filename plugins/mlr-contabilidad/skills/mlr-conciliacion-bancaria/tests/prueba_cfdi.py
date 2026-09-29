# -*- coding: utf-8 -*-
"""Reads a synthetic CFDI 4.0 invoice, its payment complement (pago20) and a Mi Admin-style workbook,
and checks the merge: XML wins, the workbook adds the real payment date and the SAT status."""
import json, os, subprocess, sys, tempfile, zipfile
import openpyxl

AQUI = os.path.dirname(os.path.abspath(__file__))
U1, U2 = "11111111-2222-4333-8444-555555555555", "99999999-8888-4777-8666-555555555555"
FACT = f'''﻿<?xml version="1.0" encoding="UTF-8"?>
<cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4" xmlns:tfd="http://www.sat.gob.mx/TimbreFiscalDigital" Version="4.0"
 Serie="F" Folio="120" Fecha="2026-08-03T10:00:00" SubTotal="10000.00" Total="10266.67" Moneda="MXN" TipoDeComprobante="I"
 MetodoPago="PPD" FormaPago="99" LugarExpedicion="06600">
 <cfdi:Emisor Rfc="ROVA800101AB1" Nombre="PROVEEDORA DEMO" RegimenFiscal="612"/>
 <cfdi:Receptor Rfc="CDT260505AB1" Nombre="CLINICA DEMO TERAPIA" DomicilioFiscalReceptor="06600" RegimenFiscalReceptor="601" UsoCFDI="G03"/>
 <cfdi:Conceptos><cfdi:Concepto Descripcion="Honorarios por asesoría contable" Importe="10000.00"/></cfdi:Conceptos>
 <cfdi:Impuestos TotalImpuestosTrasladados="1600.00" TotalImpuestosRetenidos="2066.67">
  <cfdi:Retenciones><cfdi:Retencion Impuesto="001" Importe="1000.00"/><cfdi:Retencion Impuesto="002" Importe="1066.67"/></cfdi:Retenciones>
  <cfdi:Traslados><cfdi:Traslado Base="10000.00" Impuesto="002" TipoFactor="Tasa" TasaOCuota="0.160000" Importe="1600.00"/></cfdi:Traslados>
 </cfdi:Impuestos>
 <cfdi:Complemento><tfd:TimbreFiscalDigital UUID="{U1}" FechaTimbrado="2026-08-03T10:01:00"/></cfdi:Complemento>
</cfdi:Comprobante>'''.encode("utf-8")
REP = f'''<?xml version="1.0" encoding="UTF-8"?>
<cfdi:Comprobante xmlns:cfdi="http://www.sat.gob.mx/cfd/4" xmlns:tfd="http://www.sat.gob.mx/TimbreFiscalDigital" xmlns:pago20="http://www.sat.gob.mx/Pagos20"
 Version="4.0" Serie="P" Folio="7" Fecha="2026-08-20T09:00:00" SubTotal="0" Total="0" Moneda="XXX" TipoDeComprobante="P" LugarExpedicion="06600">
 <cfdi:Emisor Rfc="ROVA800101AB1" Nombre="PROVEEDORA DEMO" RegimenFiscal="612"/>
 <cfdi:Receptor Rfc="CDT260505AB1" Nombre="CLINICA DEMO TERAPIA" DomicilioFiscalReceptor="06600" RegimenFiscalReceptor="601" UsoCFDI="CP01"/>
 <cfdi:Complemento>
  <pago20:Pagos Version="2.0"><pago20:Pago FechaPago="2026-08-19T12:00:00" FormaDePagoP="03" MonedaP="MXN" Monto="5000.00">
   <pago20:DoctoRelacionado IdDocumento="{U1.lower()}" NumParcialidad="1" ImpSaldoAnt="10266.67" ImpPagado="5000.00" ImpSaldoInsoluto="5266.67"/>
  </pago20:Pago></pago20:Pagos>
  <tfd:TimbreFiscalDigital UUID="{U2}" FechaTimbrado="2026-08-20T09:01:00"/>
 </cfdi:Complemento>
</cfdi:Comprobante>'''.encode("utf-8")

tmp = tempfile.mkdtemp()
zp = os.path.join(tmp, "xml.zip")
with zipfile.ZipFile(zp, "w") as z:
    z.writestr("CDT260505AB1/Recibidas/2026/08/%s@1.xml" % U1, FACT)
    z.writestr("CDT260505AB1/Recibidas/2026/08/%s@2.xml" % U2, REP)
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "ACUM. RECIBIDOS"
ws.append(["Estado SAT", "Versión", "Tipo", "Fecha Emisión", "Serie", "Folio", "UUID", "RFC Emisor", "Nombre Emisor", "RFC Receptor",
           "Nombre Receptor", "SubTotal", "IVA 16%", "Retenido IVA", "Retenido ISR", "Total", "Método Pago", "Forma Pago", "Fecha real de pago", "Saldo pendiente"])
ws.append(["Vigente", "4.0", "Ingreso", "2026-08-03", "F", "120", U1, "ROVA800101AB1", "PROVEEDORA DEMO", "CDT260505AB1", "CLINICA DEMO",
           10000, 1600, 1066.67, 1000, 10266.67, "PPD", "99", "2026-08-19", 5266.67])
wb.create_sheet("ACUM. EMITIDOS").append(["Estado SAT", "UUID", "Total"])
wp = wb.create_sheet("PAGOS RECIBIDOS")
wp.append(["UUID", "Fecha de pago", "Forma de pago", "Monto", "UUID relacionado", "Número de operación"])
wp.append([U2, "2026-08-19", "03", 5000, U1, "123456"])
xl = os.path.join(tmp, "acum.xlsx")
wb.save(xl)
out = os.path.join(tmp, "cfdi.json")
subprocess.run([sys.executable, os.path.join(AQUI, "..", "scripts", "leer_cfdi.py"), out, "--rfc-empresa", "CDT260505AB1",
                "--acumulado", xl, "--xml", zp], check=True)
d = json.load(open(out))
f = d["cfdi"][U1]
assert f["fuente"] == "xml+acumulado" and f["direccion"] == "recibido" and f["regimen_emisor"] == "612", f
assert (f["iva"], f["iva_ret"], f["isr_ret"]) == (1600.0, 1066.67, 1000.0)
assert f["fecha_pago_real"] == "2026-08-19" and f["estado_sat"] == "Vigente"
rep = d["indices"]["rep_por_factura"][U1][0]
assert rep["imp_pagado"] == 5000.0 and rep["parcialidad"] == 1 and rep["rep"] == U2
print("CFDI: factura, REP y acumulado combinados correctamente")

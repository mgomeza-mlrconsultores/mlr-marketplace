# Lista mensual del contador de despacho (cliente en Odoo)

Cada punto indica qué se revisa, dónde se ve en Odoo y qué evidencia se guarda. Los plazos son los generales; la regla específica se confirma en `parametros-2026.md` y en la RMF vigente.

## Recepción (días 1 a 5)
Estados de cuenta de todas las cuentas bancarias importados y con saldo final igual al del banco. CFDI emitidos fuera de Odoo identificados con su UUID. Comprobantes de caja chica con CFDI; los que no tengan comprobante se registran como no deducibles. Altas, bajas y cambios de salario en nómina con su aviso IMSS. Contratos nuevos de clientes y proveedores en el expediente de materialidad.

## Registro y conciliación (días 5 a 10)
Todos los CFDI recibidos del mes existen en Odoo como factura de proveedor con UUID y estado válido ante el SAT; los que están en el SAT y no en Odoo se cargan o se documenta por qué no (no corresponden, están cancelados, son de otro ejercicio). Todas las facturas de cliente de Odoo tienen UUID y estado vigente; las canceladas tienen su acuse. Conciliación bancaria sin partidas antiguas sin explicar. Cuentas puente revisadas: IVA trasladado no cobrado e IVA acreditable no pagado cuadran contra las facturas pendientes; anticipos de clientes y a proveedores aplicados; deudores y acreedores diversos con nombre y soporte. Depreciaciones del mes corridas y cuadradas con el registro de activos. Provisiones de nómina, aguinaldo, vacaciones y PTU registradas. Nómina timbrada igual a nómina contabilizada e igual a la base de cotización del IMSS.

## Determinación (días 10 a 15)
Pago provisional de ISR con el coeficiente de utilidad vigente o con flujo de efectivo en RESICO; comparar con los ingresos facturados y cobrados del periodo. IVA del mes a partir del reporte de impuestos de Odoo con base en flujo de efectivo, cruzado contra los complementos de pago emitidos y recibidos. Retenciones de ISR e IVA por tipo de tercero y su entero. Impuesto sobre nóminas estatal con la tasa de la entidad. IEPS y otros según el giro. Papel de trabajo con firma de quien calculó y quien revisó.

## Presentación y pago (días 15 a 17)
Declaraciones presentadas y líneas de captura pagadas antes del vencimiento; acuses guardados en Odoo (Documentos) o en el expediente del cliente. Cuotas IMSS mensuales y, en meses impares, bimestrales de RCV e INFONAVIT. Impuesto sobre nóminas estatal.

## Después del 17
DIOT presentada con los proveedores del mes y sus importes de IVA por tasa, conciliada contra el IVA acreditable declarado. Balanza de comprobación electrónica enviada en plazo (personas morales en los primeros tres días del segundo mes posterior; personas físicas en los primeros cinco). Opinión de cumplimiento consultada y archivada. Listas 69-B revisadas contra los proveedores del mes. Estados financieros emitidos y nota al cliente enviada.

## Evidencia mínima que queda
Papel de trabajo de impuestos, acuses, comprobantes de pago, conciliaciones firmadas, lista de CFDI faltantes con resolución y la nota mensual al cliente.

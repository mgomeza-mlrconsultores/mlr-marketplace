# Patrones de práctica contable en bases Odoo (PC-01 a PC-16)

Cada patrón indica cómo se detecta en solo lectura, qué consecuencia tiene y cómo se corrige. Se cita el patrón en el hallazgo; la cifra y el folio van en la evidencia.

PC-01 Facturas de proveedor validadas sin XML ni folio fiscal. Detección: facturas de proveedor publicadas con folio fiscal vacío o sin adjunto XML. Consecuencia: deducción y acreditamiento sin soporte; DIOT inconsistente. Corrección: cargar el XML o reclasificar a no deducible; regla interna de validación.

PC-02 Folios fiscales duplicados. Detección: dos documentos con el mismo UUID. Consecuencia: doble deducción. Corrección: cancelar el duplicado en Odoo y revisar el periodo declarado.

PC-03 CFDI en el SAT que no están en Odoo. Detección: cruce por UUID contra la descarga masiva. Consecuencia: ingresos omitidos (emitidos) o deducciones perdidas (recibidos). Corrección: registrar o justificar cada uno; declaración complementaria si afectó un periodo presentado.

PC-04 Documentos con estado SAT cancelado y contabilizados como vigentes. Detección: estado SAT distinto de vigente en documentos publicados y no revertidos. Consecuencia: ingreso o deducción inexistente. Corrección: revertir con nota de crédito o reversión y corregir la declaración.

PC-05 Impuestos sin base de flujo de efectivo o con cuentas puente que no se vacían. Detección: saldos crecientes en IVA trasladado no cobrado o IVA acreditable no pagado sin facturas pendientes que los expliquen. Consecuencia: IVA declarado distinto del causado. Corrección: configurar los impuestos con exigibilidad en pago y conciliar las cuentas puente contra cartera.

PC-06 Cuentas sin código agrupador del SAT. Detección: cuentas de movimiento con el campo vacío. Consecuencia: contabilidad electrónica rechazada o incompleta. Corrección: asignar código y reenviar el catálogo.

PC-07 Asientos manuales en cuentas de resultados sin documento. Detección: apuntes en diario de operaciones diversas sobre cuentas de ingresos y gastos sin referencia ni adjunto. Consecuencia: estados financieros no soportados; deducciones sin CFDI. Corrección: documentar o revertir; restringir el diario.

PC-08 Periodos abiertos después de declarar. Detección: fecha de bloqueo anterior al último periodo presentado. Consecuencia: cambios posteriores a la declaración sin complementaria. Corrección: fecha de bloqueo mensual y bloqueo fiscal anual.

PC-09 Nómina timbrada distinta de la contabilizada y de la base IMSS. Detección: suma de percepciones y deducciones de los XML contra la póliza de nómina y contra la emisión bimestral. Consecuencia: carta invitación, diferencias de retenciones, deducción de nómina rechazada. Corrección: conciliar por periodo y corregir el origen (conceptos, exentos, SBC).

PC-10 Proveedores relevantes sin expediente de materialidad. Detección: proveedores con compras acumuladas altas sin contrato ni entregables en Documentos. Consecuencia: rechazo de deducción e IVA en revisión. Corrección: integrar el expediente y la regla de orden de compra o contrato.

PC-11 Proveedores en listado 69-B sin revisar. Detección: cruce del RFC de proveedores contra la lista definitiva. Consecuencia: deducción no procedente, autocorrección obligatoria en treinta días desde la publicación, riesgo de 69-B propio. Corrección: autocorregir o acreditar materialidad ante la autoridad; bloquear al proveedor.

PC-12 Gastos pagados en efectivo arriba del límite o sin medio bancarizado. Detección: pagos registrados en diario de caja por más de dos mil pesos ligados a facturas de proveedor. Consecuencia: no deducible. Corrección: reclasificar y política de pagos.

PC-13 Depreciación contable igual a la fiscal sin conciliación. Detección: categorías de activos con porcentajes fiscales usados como vidas útiles contables sin política. Consecuencia: estados financieros fuera de NIF C-6 o conciliación fiscal inexistente. Corrección: vida útil contable por política y papel de conciliación.

PC-14 Anticipos de clientes facturados como ingreso o no facturados. Detección: cobros sin CFDI de anticipo o anticipos registrados en ingresos. Consecuencia: IVA e ISR en periodo incorrecto; CFDI de anticipo y aplicación mal emitidos. Corrección: flujo de anticipos de la localización y cuenta de pasivo.

PC-15 Deudores diversos y préstamos a socios sin contrato ni intereses. Detección: saldos de socios y empleados sin documento. Consecuencia: dividendos fictos, ingreso presunto. Corrección: contrato, intereses, calendario de pago o reclasificación.

PC-16 Sin control de vencimientos de e.firma, CSD y opinión de cumplimiento. Detección: no existe registro de vigencias ni consulta mensual. Consecuencia: paro de facturación, pérdida de contratos. Corrección: calendario en Odoo (actividades) con alertas a sesenta y treinta días.

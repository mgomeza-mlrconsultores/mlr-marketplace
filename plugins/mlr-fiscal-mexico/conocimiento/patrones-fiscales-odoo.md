# Patrones fiscales en bases Odoo de México (catálogo F)

Vigente al 2026-10-03. Cada patrón: detección en solo lectura, evidencia y remediación. Se usa en diagnósticos junto con los catálogos contables.

## F-01 Configuración de la localización incompleta
Compañía sin RFC, régimen fiscal o código postal correctos; certificados CSD vencidos o de otra razón social; PAC sin credenciales de producción; pruebas con PAC de pruebas en producción. Detección: ajustes de contabilidad y `l10n_mx_edi`; estado de los últimos timbrados. Remediación: completar y probar un ciclo de timbrado en pruebas.

## F-02 Productos y unidades sin claves SAT
Productos sin clave de producto o servicio o con clave genérica inadecuada; unidades sin clave de unidad; servicios con claves de bienes. Detección: `product.template` y `uom.uom` con campos de la localización vacíos. Remediación: catálogo de claves por familia, validación antes de facturar.

## F-03 Receptores con datos fiscales inconsistentes
Nombre distinto de la constancia, código postal, régimen o uso del CFDI incompatible; RFC genérico usado para clientes identificados. Detección: facturas rechazadas por el PAC, contactos sin régimen. Remediación: depuración de contactos con constancias; uso del CFDI por defecto por cliente.

## F-04 Método y forma de pago incorrectos
PUE en operaciones a crédito; PPD cobrado sin complemento de pago; forma de pago «por definir» en PUE. Detección: facturas PPD con pagos conciliados sin complemento emitido; PUE con términos de pago a 30 días. Remediación: método por término de pago; emisión de complementos por pago registrado; revisión del quinto día natural.

## F-05 Cancelaciones sin control
CFDI cancelados con motivo erróneo, sin sustituto cuando hubo pago, fuera de plazo, o cancelados en el PAC pero vivos en Odoo. Detección: estado SAT contra estado del documento; motivos de cancelación. Remediación: política de cancelación y conciliación de estados.

## F-06 Factura global mal configurada
Punto de venta o tiendas sin factura global, con periodicidad incorrecta o duplicando ventas ya facturadas a clientes identificados. Detección: ventas de público general sin CFDI global del periodo; globales que incluyen tickets ya facturados. Remediación: configuración por punto de venta y conciliación mensual.

## F-07 CFDI recibidos sin registro y registros sin CFDI
Gastos pagados sin comprobante registrado; facturas de proveedor registradas sin UUID; XML descargados y no importados. Detección: descarga del SAT contra `account.move` de proveedor por UUID. Remediación: importación de XML, política de registro mensual, bloqueo de pagos sin CFDI.

## F-08 Retenciones no configuradas o no enteradas
Honorarios, arrendamiento, fletes y servicios de personal sin retención de IVA e ISR; retenciones calculadas sin cuenta ni declaración. Detección: impuestos de retención ausentes en facturas de esas categorías; saldos de retenciones sin entero. Remediación: catálogo de impuestos de retención por posición fiscal.

## F-09 DIOT inconsistente
Proveedores sin tipo de tercero o tipo de operación; IVA no acreditable sin clasificar; proveedores extranjeros tratados como nacionales. Detección: campos de la localización vacíos en proveedores; comparación DIOT generada contra CFDI recibidos. Remediación: completar catálogos y validar la DIOT antes de enviar.

## F-10 Contabilidad electrónica sin código agrupador
Cuentas sin código agrupador o con códigos inconsistentes con su naturaleza; balanza XML que no cuadra con la anual. Detección: `account.account` con el campo de código agrupador vacío; comparación de balanza. Remediación: catálogo completo con códigos; revisión del contador.

## F-11 Proveedores en el 69-B
Pagos a emisores listados; falta de expediente de materialidad. Detección: cruce de RFC de proveedores contra la lista vigente del SAT. Remediación: suspender pagos, acreditar materialidad o autocorregir.

## F-12 Nómina timbrada que no coincide con IMSS
Trabajadores sin alta, SBC distinto, subsidio mal calculado, periodicidad inconsistente. Detección: CFDI de nómina contra movimientos afiliatorios y cuotas. Remediación: ver plugin de nómina.

## F-13 Base de pruebas que timbra en producción
Copias de la base con PAC y sellos activos que emiten comprobantes reales o envían correos. Detección: parámetros del sistema de la copia. Remediación: neutralización al crear la copia.

## F-14 Opinión de cumplimiento negativa o sellos restringidos
Detección: consulta del 32-D y del estado de los CSD. Remediación: ver `perspectiva-sat.md`; prioridad máxima porque detiene la operación.

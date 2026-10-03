# CFDI que no nacen en Odoo: carga manual y control

## Casos reales
Facturas de clientes emitidas en otro sistema, en la aplicación gratuita del SAT o por un PAC externo antes o durante la implementación. Facturas de proveedor que llegan por correo o se descargan del portal del SAT. Notas de crédito y complementos de pago emitidos fuera. Nómina timbrada por una maquila de nómina y registrada en Odoo por póliza. Comprobantes de retenciones e información de pagos.

## Reglas que no cambian con la versión
Un CFDI que ya tiene UUID nunca se vuelve a timbrar: en Odoo se registra el documento con su folio fiscal y se adjunta el XML. El RFC, el régimen fiscal y el código postal del receptor deben coincidir con la constancia de situación fiscal; en CFDI 4.0 el PAC rechaza diferencias. Un UUID solo puede existir una vez en la base; la duplicidad se detecta por el folio fiscal, no por el número de factura. El estado que vale es el del SAT (vigente o cancelado), no el estado del documento en Odoo. Lo que está en el SAT y no está en Odoo es tan grave como lo contrario: ambos se concilian cada mes por UUID.

## Cómo se hace en Odoo según la versión
Facturas de proveedor: desde la versión 16 el XML del CFDI se sube en Facturas de proveedor y Odoo crea el documento con proveedor por RFC, líneas, impuestos y folio fiscal; a partir de la 17 la localización registra los documentos fiscales en un modelo propio y guarda el estado ante el SAT. En versiones anteriores el XML se adjunta y el UUID se captura en el campo de folio fiscal. La verificación del estado ante el SAT la hace una acción programada; se confirma que esté activa y con qué frecuencia corre.

Facturas de cliente emitidas fuera: se verifica si la versión y edición instaladas permiten registrar un CFDI emitido externamente sin volver a timbrar; si no, se registra la factura con el XML adjunto y el folio fiscal capturado, y se deja sin intentar el timbrado. Nunca se emite un segundo CFDI por la misma operación para "que quede en Odoo".

Nómina de maquila: la póliza de nómina se registra con el detalle por concepto y centro de costo; el timbrado queda en los XML de la maquila, que se adjuntan en Documentos; el cruce nómina timbrada contra contabilidad se hace por periodo.

Descarga del SAT: si la versión no sincroniza con el SAT, la conciliación mensual se hace contra la descarga masiva de metadatos o XML del portal del SAT. El cruce por UUID produce tres listas: en SAT y en Odoo (correcto), solo en SAT (falta registrar o justificar) y solo en Odoo (verificar cancelación o error de captura).

## Controles mínimos
Reporte mensual de facturas sin folio fiscal, de folios duplicados y de documentos con estado SAT distinto de vigente. Facturas de proveedor validadas sin XML adjunto en cero. Fecha del CFDI dentro del periodo contable en que se registra o justificación en la póliza. Referencia de pago en el complemento de pago coincide con la conciliación bancaria.

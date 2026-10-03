# Catálogo de patrones: contabilidad y fiscal

Lo fiscal específico de `México` se verifica contra `fuentes-oficiales.md`; los patrones generales aplican en cualquier localización.

## C-01 Cuentas puente de banco con saldo (líneas de extracto sin conciliar)
Detección: cuenta transitoria o puente del diario de banco con saldo distinto de cero; `account.bank.statement.line` sin conciliar por antigüedad. Evidencia: lista por fecha y monto. Remediación: conciliación con aprobación fila por fila (ver plugin de contabilidad).

## C-02 Pendientes de cobro y pago envejecidos
Detección: cuentas de pagos pendientes (outstanding receipts/payments) con saldo por partida; pagos sin factura y facturas pagadas sin pago vinculado. Remediación: emparejar o reclasificar con evidencia del comprobante.

## C-03 Catálogo de cuentas con duplicadas, archivadas en uso y jerarquía rota
Detección: códigos duplicados o cuentas con nombres equivalentes; `account.account` archivadas referenciadas en diarios, impuestos, categorías o la compañía; grupos de cuentas incompletos. Remediación: fusión documentada y reasignación antes de archivar.

## C-04 Diarios con cuentas por defecto incorrectas
Detección: diarios de venta y compra con cuenta de ingreso o gasto por defecto que no corresponde; diarios de banco sin cuenta puente; diario de nómina o misceláneo usado para operación. Remediación: corrección y revisión de asientos generados.

## C-05 Impuestos mal configurados
Detección: impuestos con cuentas vacías o repetidas, base imponible contra criterio de caja mal definidos, retenciones sin cuenta, posiciones fiscales sin mapeo; en `México` cruzar con los regímenes y claves que exige la autoridad. Remediación: catálogo de impuestos mínimo con pruebas en base de pruebas.

## C-06 Fechas de bloqueo ausentes
Detección: compañía sin fecha de bloqueo fiscal ni de impuestos; asientos modificados en periodos declarados. Remediación: bloqueos por periodo con responsable.

## C-07 Asientos manuales en cuentas de control (clientes, proveedores, inventario, impuestos)
Detección: apuntes en cuentas por cobrar o por pagar sin `partner_id` o desde diario misceláneo; apuntes manuales en cuentas de impuestos. Remediación: reversión o reclasificación y restricción de cuentas.

## C-08 Borradores antiguos y asientos sin publicar
Detección: `account.move` en borrador con fecha anterior al último cierre; facturas en borrador con comprobante fiscal ya emitido. Remediación: publicar o cancelar con criterio y corte.

## C-09 Multimoneda con tipos de cambio desactualizados
Detección: `res.currency.rate` sin actualizar; diferencias cambiarias no reconocidas; cuentas de ganancia y pérdida cambiaria vacías. Remediación: política de tipos de cambio y revaluación de saldos.

## C-10 Intercompañía descuadrada
Detección: saldos entre compañías del grupo que no se cancelan entre sí; facturas intercompañía sin contraparte; reglas de intercompañía desactivadas. Remediación: conciliación intercompañía mensual y automatización de contrapartes.

## C-11 Cobertura analítica incompleta
Detección: apuntes de ingreso y gasto sin distribución analítica en planes marcados como obligatorios; planes sin uso. Remediación: reglas de distribución por defecto y obligatoriedad por cuenta.

## C-12 Comprobantes fiscales contra contabilidad
Detección (`México`): facturas con estado fiscal distinto del contable (emitidas sin registro, canceladas con asiento vivo), pagos sin complemento cuando la forma de pago lo exige, sustituciones no reflejadas, identificadores fiscales capturados a mano. Evidencia: el comprobante leído, no el campo de estado. Remediación: regularización contra el padrón de la autoridad.

## C-13 Activos fijos y diferidos sin movimiento
Detección: activos sin depreciación publicada, diferidos sin reconocimiento mensual. Remediación: calendarios y publicación con revisión.

## C-14 Cierre anual no ejecutado
Detección: resultados de ejercicios anteriores sin traspaso, cuentas de resultados con saldo acumulado de años previos. Remediación: cierre con asiento de traspaso y bloqueo.

## C-15 Contactos duplicados con saldos repartidos
Detección: `res.partner` con identificador fiscal repetido o nombre equivalente y saldos en varios registros. Remediación: fusión con evidencia y reconciliación de partidas.

## C-16 Pagos registrados sin conciliar con factura (doble cobro aparente)
Detección: pagos publicados sin conciliar y facturas pagadas con otro pago; antes de concluir doble cobro, leer el comprobante (sustituciones, adjuntos de otra factura). Remediación: conciliación y, si procede, devolución documentada.

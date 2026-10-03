# Catálogo de patrones: inventario y valuación

Cada patrón: síntoma que ve el cliente, causa raíz típica, cómo se detecta (solo lectura), evidencia que se exige y remediación. El auditor recorre el catálogo completo antes de dar por terminada su revisión y propone patrones nuevos cuando los comprueba.

## I-01 Valuación de inventario que no cuadra con la cuenta contable
Síntoma: el reporte de valuación y el saldo de la cuenta de inventario difieren. Causas: asientos manuales en la cuenta de inventario; categorías con valuación manual mezcladas con tiempo real; movimientos sin asiento por ubicaciones sin cuenta (19) o por categorías sin cuentas (≤18); revaluaciones; migración. Detección: en ≤18 sumar `stock.valuation.layer.value` por categoría contra apuntes de la cuenta de valuación por periodo; en 19 sumar `stock.move.value` de movimientos hechos y `product.value` contra la cuenta; separar la diferencia por origen (manual, sin asiento, revaluación, redondeo). Evidencia: cifra por dos caminos, lista de asientos manuales con folio. Remediación: política de valuación por categoría, bloqueo de asientos manuales en cuentas de inventario, regularización con asiento documentado y, en 19, uso controlado del cierre de valuación.

## I-02 Categorías de producto sin cuentas o con cuentas equivocadas
Causa: configuración incompleta o copiada. Detección: `product.category` con `property_valuation = real_time` y cuentas vacías o apuntando a cuentas de gasto. Evidencia: lista de categorías y productos almacenables afectados con existencia. Remediación: completar cuentas y recalcular el efecto histórico.

## I-03 Método de costo inconsistente entre categorías equivalentes
Causa: categorías creadas en momentos distintos. Detección: `property_cost_method` distinto (estándar, promedio, FIFO) en categorías del mismo giro. Remediación: unificar con plan de transición (el cambio de método genera asientos).

## I-04 Productos almacenables con costo cero y existencia
Causa: alta sin costo, recálculo FIFO tras migración, revaluaciones no tomadas. Detección: `product.product` con `qty_available > 0` y `standard_price = 0` o valor total cero; cruzar con fecha de creación y migraciones. Remediación: fijar costo con evidencia (última compra, costo estándar) y asiento de revaluación.

## I-05 Unidades de medida con factores erróneos
Síntoma: sobrevaluación o faltantes por conversión. Causa: unidades con factor 1 respecto de la pieza (Caja, KG, Metro) o la «Docena» nativa renombrada. Detección: `uom.uom` por categoría con `factor` y `uom_type`; cruzar con compras y ventas que usan unidades distintas a la del producto. Evidencia: documento con folio donde la conversión produce la cifra errónea. Remediación: crear unidades correctas, no editar factores con histórico; regularizar existencias afectadas.

## I-06 Existencias negativas
Causa: entregas antes de recepciones, ajustes, reglas de disponibilidad relajadas, ubicaciones archivadas con existencia. Detección: `stock.quant` con `quantity < 0` por producto, ubicación y lote. Remediación: regularización de existencias por conteo, corrección de secuencia operativa, política de reserva.

## I-07 Asientos manuales en cuentas de inventario o de valuación
Detección: `account.move.line` en cuentas de valuación cuyo `move_id` no proviene de inventario (`stock_move_id` vacío, diario general). Evidencia: folio de cada asiento. Remediación: reversión documentada o reclasificación; bloquear la cuenta a asientos manuales.

## I-08 Transitorias de mercancía recibida y entregada sin factura con saldo envejecido (≤18 y herencia en 19)
Causa: recepciones nunca facturadas, facturas sin orden, reaperturas, diferencias de unidad. Detección: saldo de las cuentas de entrada y salida por antigüedad y por documento origen; en 19, herencia que la versión ya no mueve. Remediación: facturar o cancelar lo pendiente, depurar el saldo por origen antes de cualquier rebalanceo.

## I-09 Recepciones no facturadas y entregas no facturadas acumuladas
Detección: `stock.picking` hechos con `purchase_line.qty_invoiced < qty_received` o `sale_line.qty_invoiced < qty_delivered`; antigüedad. Riesgo: al facturarlas tarde cargan inventario otra vez (19) o distorsionan el corte. Remediación: política de facturación y limpieza por lotes con corte.

## I-10 Costes en destino no aplicados o aplicados a producto equivocado
Detección: `stock.landed.cost` en borrador, facturas de flete sin coste en destino, productos con `landed_cost_ok`. Remediación: flujo de costes en destino con reparto definido.

## I-11 Ubicaciones archivadas o internas mal tipificadas con existencia
Detección: `stock.location` con `active = False` y quants; ubicaciones de tipo tránsito o proveedor con existencia interna. Remediación: traslados de regularización y depuración de ubicaciones.

## I-12 Perecederos sin lote ni caducidad
Detección: productos de giro perecedero con `tracking = none` o con caducidad marcada sin lote; lotes vencidos con existencia; sin FEFO. Remediación: activar lote y caducidad, capturar lotes en conteo físico, fijar FEFO.

## I-13 Regularizaciones de existencias contra cuentas equivocadas
Detección: ajustes de inventario cuyo asiento va a cuenta distinta de la de regularización definida; ajustes masivos sin motivo. Remediación: cuenta de regularización por ubicación de inventario y motivo obligatorio.

## I-14 Kits y listas de materiales que distorsionan la valuación
Detección: productos kit con existencia propia, componentes sin costo, listas de materiales con cantidades o unidades erróneas, variaciones de costo no analizadas en fabricación. Remediación: política de kits, revisión de listas, análisis de variaciones por orden.

## I-15 Devoluciones y rutas que generan valuación cruzada
Detección: devoluciones a ubicaciones de otro tipo, rutas de reabastecimiento o dropship con cuentas de ubicación distintas, movimientos intercompañía sin contrapartida. Remediación: revisar rutas y cuentas por ubicación.

## I-16 Productos duplicados y catálogo sin código
Detección: nombres normalizados repetidos, `default_code` vacío, variantes huérfanas. Remediación: depuración con fusión documentada y codificación.

## I-17 Diferencias por moneda en compras
Detección: órdenes de compra en moneda extranjera con tipo de cambio desactualizado; diferencia entre costo recibido y facturado llevada a cuenta incorrecta. Remediación: política de tipos de cambio y cuenta de diferencia de precio.

## I-18 Fabricación: producto en proceso abierto y órdenes sin cerrar
Detección: `mrp.production` en progreso con antigüedad, consumos sin producción terminada, costos de centro de trabajo en cero. Remediación: cierre de órdenes con conteo y análisis de variaciones.

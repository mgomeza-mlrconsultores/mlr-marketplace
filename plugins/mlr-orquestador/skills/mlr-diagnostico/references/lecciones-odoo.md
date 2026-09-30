# Lecciones de mecánica y de método ya comprobadas

Cada punto salio de un diagnóstico real y se comprobó en código o en datos. Antes de reutilizarlo en otra versión, se vuelve a leer el código de esa versión.

## Valuación de inventario en Odoo 19 (stock_account)

- No existe `stock.valuation.layer`. El valor vive en `stock.move.value`, `remaining_value` y `value_manual`, en `product.value` (revaluaciones) y en `product.product.total_value`.
- Las categorías tienen `property_valuation` periódica o en tiempo real, sin cuentas transitorias de entrada y salida.
- Un movimiento de inventario solo genera asiento si la ubicación origen o destino tiene `valuation_account_id` (`stock_move._should_create_account_move`).
- Factura de proveedor de un almacenable en tiempo real: la línea va a la cuenta de valuación de la categoría (`account_move_line._compute_account_id`).
- Factura de cliente: genera el costo de venta contra la cuenta de valuación (`account_move._stock_account_prepare_realtime_out_lines_vals`).
- Cierre de valuación (`res.company.action_close_stock_valuation`, botón «Generar asiento» del reporte): contabiliza valuación menos saldo de la cuenta de inventario contra `account_stock_variation_id` de la cuenta o, si no hay, contra `company.expense_account_id`. Medir la cifra antes de que alguien lo oprima.
- La migración desde 17 deja una acción de servidor para «rebalancear» las transitorias; ejecutarla sin depurar puede vaciar millones en la cuenta de inventario.
- Al recalcular FIFO desde movimientos, las revaluaciones sin movimiento de la versión anterior no se toman: productos con existencia y valor cero.
- Tras migrar, `stock.move.account_move_id` puede quedar vacío. El vinculo asiento–albarán se reconstruye por `account.move.ref` («albarán - producto») y `product_id` del apunte.

## Lotes y fechas de caducidad en perecederos (Odoo 19)

Revisión obligada si el cliente vende alimentos, químicos o cualquier producto con vida útil (Freshbox, 29-sep-2026):

- Que el módulo de caducidades (`product_expiry`) esté instalado y que el grupo de lotes (`stock.group_production_lot`) esté implícito en los usuarios internos. Instalado no quiere decir usado.
- Por producto almacenable activo: `tracking` (`lot`, `serial`, `none`) y `use_expiration_date` con sus plazos (`expiration_time`, `use_time`, `removal_time`, `alert_time`). Contar cuántos perecederos quedan en `none` y cuáles tienen caducidad marcada sin lote, que no sirve de nada.
- `stock.lot` con `expiration_date` pasada y existencia, lotes con cantidad negativa y lotes de prueba que se quedaron en la base.
- Estrategia de retiro (`removal_strategy_id`) en categorías y en la ubicación de existencias: sin FEFO el sistema no sugiere sacar primero lo que vence primero.
- En el informe se cuenta con la lista de lotes (vencidos y negativos a la vista) y un pivote de productos por categoría y seguimiento. La corrección es activar lote y caducidad en los perecederos, capturar lotes en el conteo físico y fijar FEFO; en la cotización es la tarea «Lotes y fechas de caducidad» dentro de inventario.

## Herencia de 17 que hay que reconocer

- Cuentas transitorias de mercancía recibida sin factura y enviada sin factura con saldos que la 19 ya no mueve. Descomponer su saldo por origen (reaperturas, errores de unidad de medida, entradas sin orden) antes de proponer el saneamiento.
- Recepciones de 17 no facturadas y entregas no facturadas: al facturarlas en 19 cargan otra vez la cuenta de inventario. Medirlas.

## Campos y estados que cambian de nombre (romper código a medida)

- `res.groups.users` → `user_ids` en 19. Automatizaciones que usan `grupo.users` fallan para todos.
- Estado de pago `cancel` → `canceled` en 19.
- `purchase.order.line.product_uom` → `product_uom_id`.
- Revisar código a medida que escribe `state` directamente: deja documentos cancelados con movimientos o conciliaciones vivas.
- Estados agregados por módulos propios (por ejemplo «en proceso de cancelación») pueden sacar documentos validos de saldos y reportes.

## Trampas de medición

- `amount_total` está en la moneda del documento. Para sumar, `amount_total_signed` o débitos y créditos en moneda de la compania.
- `create_date` vacío en filas insertadas por SQL durante la migración.
- Unidades de medida con factor 1 respecto de la pieza (Caja, KG, Metro…) o la Docena nativa renombrada: causa raíz de sobrevaluaciones.
- Cuentas archivadas que siguen configuradas en diarios, impuestos o la compania: fallan al publicar.
- Lo fiscal se confirma en el XML adjunto: sustituciones (TipoRelacion 04), PUE contra PPD, UUID capturado a mano.
- Consultas pesadas: por lotes, con tiempo de espera, y cache local cuando varios agentes leen lo mismo.

## Capturas por navegador sin modificar nada

- Las URL directas de registro a veces pintan en blanco. Funciona abrir Odoo y navegar con `odoo.__WOWL_DEBUG__.root.env.services.action.doAction({...})` (tipo `ir.actions.act_window`, `res_model`, `res_id` o `domain`, `views`).
- Esperas cortas (máximo 10 s) y reintento. No borrar nodos del DOM ni hacer zoom sobre el `body`: congela el render.
- Recortar a la zona que prueba el hallazgo y guardar numerado (`01_...jpg`). El pie de la figura cita el folio y la cifra que se ve.
- Columnas opcionales (por ejemplo «Valor» en existencias) se activan desde el selector de columnas, sin guardar vista.

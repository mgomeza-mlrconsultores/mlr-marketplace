# Lecciones de mecanica y de metodo ya comprobadas

Cada punto salio de un diagnostico real y se comprobo en codigo o en datos. Antes de reutilizarlo en otra version, se vuelve a leer el codigo de esa version.

## Valuacion de inventario en Odoo 19 (stock_account)

- No existe `stock.valuation.layer`. El valor vive en `stock.move.value`, `remaining_value` y `value_manual`, en `product.value` (revaluaciones) y en `product.product.total_value`.
- Las categorias tienen `property_valuation` periodica o en tiempo real, sin cuentas transitorias de entrada y salida.
- Un movimiento de inventario solo genera asiento si la ubicacion origen o destino tiene `valuation_account_id` (`stock_move._should_create_account_move`).
- Factura de proveedor de un almacenable en tiempo real: la linea va a la cuenta de valuacion de la categoria (`account_move_line._compute_account_id`).
- Factura de cliente: genera el costo de venta contra la cuenta de valuacion (`account_move._stock_account_prepare_realtime_out_lines_vals`).
- Cierre de valuacion (`res.company.action_close_stock_valuation`, boton «Generar asiento» del reporte): contabiliza valuacion menos saldo de la cuenta de inventario contra `account_stock_variation_id` de la cuenta o, si no hay, contra `company.expense_account_id`. Medir la cifra antes de que alguien lo oprima.
- La migracion desde 17 deja una accion de servidor para «rebalancear» las transitorias; ejecutarla sin depurar puede vaciar millones en la cuenta de inventario.
- Al recalcular FIFO desde movimientos, las revaluaciones sin movimiento de la version anterior no se toman: productos con existencia y valor cero.
- Tras migrar, `stock.move.account_move_id` puede quedar vacio. El vinculo asiento–albaran se reconstruye por `account.move.ref` («albaran - producto») y `product_id` del apunte.

## Herencia de 17 que hay que reconocer

- Cuentas transitorias de mercancia recibida sin factura y enviada sin factura con saldos que la 19 ya no mueve. Descomponer su saldo por origen (reaperturas, errores de unidad de medida, entradas sin orden) antes de proponer el saneamiento.
- Recepciones de 17 no facturadas y entregas no facturadas: al facturarlas en 19 cargan otra vez la cuenta de inventario. Medirlas.

## Campos y estados que cambian de nombre (romper codigo a medida)

- `res.groups.users` → `user_ids` en 19. Automatizaciones que usan `grupo.users` fallan para todos.
- Estado de pago `cancel` → `canceled` en 19.
- `purchase.order.line.product_uom` → `product_uom_id`.
- Revisar codigo a medida que escribe `state` directamente: deja documentos cancelados con movimientos o conciliaciones vivas.
- Estados agregados por modulos propios (por ejemplo «en proceso de cancelacion») pueden sacar documentos validos de saldos y reportes.

## Trampas de medicion

- `amount_total` esta en la moneda del documento. Para sumar, `amount_total_signed` o debitos y creditos en moneda de la compania.
- `create_date` vacio en filas insertadas por SQL durante la migracion.
- Unidades de medida con factor 1 respecto de la pieza (Caja, KG, Metro…) o la Docena nativa renombrada: causa raiz de sobrevaluaciones.
- Cuentas archivadas que siguen configuradas en diarios, impuestos o la compania: fallan al publicar.
- Lo fiscal se confirma en el XML adjunto: sustituciones (TipoRelacion 04), PUE contra PPD, UUID capturado a mano.
- Consultas pesadas: por lotes, con tiempo de espera, y cache local cuando varios agentes leen lo mismo.

## Capturas por navegador sin modificar nada

- Las URL directas de registro a veces pintan en blanco. Funciona abrir Odoo y navegar con `odoo.__WOWL_DEBUG__.root.env.services.action.doAction({...})` (tipo `ir.actions.act_window`, `res_model`, `res_id` o `domain`, `views`).
- Esperas cortas (maximo 10 s) y reintento. No borrar nodos del DOM ni hacer zoom sobre el `body`: congela el render.
- Recortar a la zona que prueba el hallazgo y guardar numerado (`01_...jpg`). El pie de la figura cita el folio y la cifra que se ve.
- Columnas opcionales (por ejemplo «Valor» en existencias) se activan desde el selector de columnas, sin guardar vista.

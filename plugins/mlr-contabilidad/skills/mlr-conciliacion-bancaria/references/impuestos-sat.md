# Pagos al SAT y determinación de impuestos

## Cruce de pagos contra acuses

Cada movimiento P14 se cruza con los PDF de la carpeta de impuestos del mes: «LC …» (línea de captura), «Detalle …» (declaración), «Comprobante de pago …». Se desglosa en impuesto, recargos y actualización, y se distingue normal de complementaria. El total por movimiento debe coincidir con el cargo del banco; el SAT recibe pesos enteros y la diferencia contra Odoo va a redondeo.

Casos reales de 2026 que muestran por qué no se registra un P14 sin su acuse:

| Fecha en banco | Importe | Qué pagó |
|---|---|---|
| 08/07 | 2,234.00 | ISR retenido por servicios profesionales de mayo 2,202 + recargos 32 |
| 08/07 | 2,248.00 | IVA retenido de mayo en la normal (declarado 2,202 por error) + recargos 46 |
| 16/07 | 147.00 | Complementaria: IVA retenido correcto 2,349 + 46 de recargos, menos 2,248 ya pagados |
| 21/08 | 15,591.00 | IVA de julio 15,117 + recargos 313 e IVA retenido 158 + recargos 3. Una complementaria posterior convirtió julio en saldo a favor de 7,482 y lo pagado quedó como pago en exceso, aplicado en agosto |

## Registro de un pago que ya está en el banco

- Con estado de cuenta cargado: la línea en suspenso se concilia repartiéndola entre la cuenta del impuesto, recargos y redondeo (operación `linea_extracto`).
- Sin estado de cuenta: asiento en el diario del banco o en Operaciones varias contra la cuenta del banco (operación `asiento_manual`).

## Determinación mensual de IVA

Asiento manual, criterio del responsable del cliente en el caso de origen:

- Fecha: la de presentación de la declaración; si hubo complementarias, la de la última, con sus cifras finales.
- Cargo a IVA trasladado cobrado por el saldo del mes; abono a IVA acreditable pagado por lo declarado; diferencia a IVA a favor o a IVA por pagar.
- En el mes en que se aplican saldos a favor, incluidos pagos en exceso: cargo a IVA por pagar y abono a IVA a favor por lo aplicado.
- Centavos a redondeo.
- Se registra con lo declarado y las diferencias contra Odoo se dejan visibles. Caso real: 199.81 de IVA de una factura pagada en agosto con tres REP y no declarada se quedó como acreditable pendiente mientras se decidía la complementaria.

## Retenciones

Se acumulan solas desde las facturas (ISR de honorarios, IVA retenido efectivamente pagado) y se cancelan con el pago. Recargos a su cuenta propia; su deducibilidad la decide el área fiscal. Los recargos pagados sobre un IVA que después resultó saldo a favor se recuperan dentro de ese saldo.

## Cierre de impuestos nativo de Odoo

Evaluado y descartado en el caso de origen. Toma los impuestos de las facturas y no aplica saldos a favor ni redondeos a pesos; cierra con cifras de Odoo, no con lo declarado; en México el reporte ligado es la DIOT; probarlo en un mes ya cerrado a mano duplica el cierre; y marcar una declaración como presentada fija la fecha de bloqueo. Si algún cliente lo quiere usar, los grupos de impuestos deben cerrar contra cuentas por pagar no comerciales (`liability_payable`, `non_trade = True`).

## Primer ejercicio

Una persona moral en su primer ejercicio no hace pagos provisionales de ISR (art. 14 LISR). El Previo lo dice como «por confirmar» y el área fiscal lo confirma.

## Criterios que decide el área fiscal

Retención de IVA a fletes (4 %) y a comisiones (2/3); primer ejercicio; deducibilidad de recargos; deducción e IVA de gastos mayores a 2,000 pesos pagados con tarjetas personales de socios (art. 27 fr. III LISR); IVA de comisiones sin CFDI del banco; compras con tarjeta sin CFDI. La skill los pregunta, los deja visibles en el libro y los guarda en la memoria del cliente cuando se deciden.

# Compras

## Decisiones que gobiernan el resultado
Política de control de facturas (cantidades pedidas contra recibidas) que decide si una recepción sin factura queda en tránsito; aprobación por monto mínimo y doble validación; tarifas de proveedor con plazos y cantidades mínimas; acuerdos de compra y licitaciones; recepciones en una, dos o tres etapas y su efecto en inventario; unidades de compra distintas a las de inventario; costes en destino por factura de flete; compras en moneda extranjera y tipo de cambio del día de la recepción contra el de la factura; dropship y subcontratación.

## Patrones de error
Recepciones no facturadas acumuladas (transitoria con saldo envejecido, I-08, I-09); facturas registradas sin orden que duplican el gasto; unidades de compra con factor erróneo (I-05); proveedores duplicados; órdenes confirmadas por años sin cerrar; compras de servicios tratadas como almacenables; costes en destino en borrador.

## Por versión
16–17: `product_uom` → `product_uom_id` en líneas (rompe código a medida); 17: aprobación y recepción con interfaz nueva; 18–19: cambios en el flujo de recepción y en facturación desde recepción (verificar); 19: cuentas transitorias de entrada eliminadas en la valuación (ver `odoo-versiones.md`), lo que cambia cómo se concilia la compra con el inventario.

## Lo que pregunta un senior
¿Quién puede comprar y hasta cuánto? ¿Se factura lo recibido o lo pedido? ¿Qué pasa con la diferencia entre costo de la orden y de la factura? ¿Cuántas recepciones del año pasado siguen sin factura?

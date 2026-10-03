# Inventario (operación)

Complementa `patrones-inventario-valuacion.md`, que cubre la valuación.

## Decisiones que gobiernan el resultado
Almacenes y ubicaciones (física contra lógica, tránsito, mermas, calidad); rutas y reglas (fabricar, comprar, bajo pedido, reabastecer desde otro almacén); estrategias de retiro (FIFO, LIFO, FEFO) y de almacenaje; lotes y series con caducidad; unidades y empaquetados; reglas de reabastecimiento con mínimos y máximos; recepciones y entregas en etapas; transferencias por lotes y oleadas; códigos de barras; inventario cíclico y conteos; reservas y disponibilidad; operaciones intercompañía.

## Patrones de error
Ubicaciones archivadas con existencia; existencias negativas por reglas de reserva relajadas; rutas sin regla final que dejan necesidades sin atender; reglas de reabastecimiento sin plazo de entrega; conteos sin congelar operación; traslados internos usados como ventas; devoluciones a ubicaciones de proveedor con existencia; falta de lotes en perecederos; unidades de venta y compra sin relación con la de inventario.

## Por versión
15–16: rutas y reglas con interfaz clásica; 17: rediseño, operaciones en lote y oleadas (Enterprise), cambios en el reporte de existencias; 18: cambios en empaquetados y unidades (verificar), «reabastecimiento» rediseñado; 19: valuación sin capas (ver versiones), cambios en reservas y en la aplicación de códigos de barras (verificar).

## Lo que pregunta un senior
¿Dónde está físicamente la mercancía y coincide con las ubicaciones del sistema? ¿Qué se cuenta, cuándo y quién firma la diferencia? ¿Qué producto se vence y cómo se saca primero? ¿Qué movimiento genera asiento y cuál no, y por qué?

# Fabricación

## Decisiones que gobiernan el resultado
Listas de materiales (normal, kit, subcontratación) con unidades y mermas; rutas de producción y centros de trabajo con costo por hora; órdenes de trabajo y hojas de ruta; producto en proceso y su contabilización; subproductos y desechos; planificación maestra y bajo pedido; costeo de la orden (materiales, mano de obra, gastos) y variaciones contra estándar; subcontratación con reabastecimiento de componentes; calidad en puntos de control; mantenimiento de equipos.

## Patrones de error
Kits con existencia propia; listas con cantidades por unidad equivocada; órdenes en progreso por meses que distorsionan el costo (I-18); centros de trabajo con costo cero; consumos sin producción terminada; subcontratación sin rutas multietapa ni ubicación de almacenamiento configurada (caso de referencia); variaciones nunca analizadas; fabricación bajo pedido desde punto de venta sin ruta MTO correcta.

## Por versión
16: costeo y órdenes de trabajo clásicos; 17: rediseño de órdenes, cambios en subcontratación y en el flujo de órdenes de trabajo; 18: planificación y hojas de ruta mejoradas (verificar); 19: cambios en costeo ligados a la nueva valuación sin capas; revisar `mrp_account` en la rama antes de afirmar cómo se contabiliza el producto en proceso.

## Lo que pregunta un senior
¿El costo estándar está vigente o es de hace tres años? ¿Quién cierra las órdenes y cuándo? ¿Qué variación es normal en este giro? ¿Qué se subcontrata y quién pone los componentes?

# Ventas y CRM

## Decisiones que gobiernan el resultado
Equipos de venta y asignación; etapas del pipeline con probabilidad y actividades; oportunidades maestras e hijas cuando un cliente tiene varios frentes (casos de consultoría y licitación); listas de precios (fija, por porcentaje, por fórmula, por cantidad) y su orden de prioridad; política de facturación (cantidades pedidas contra entregadas) que decide cuándo nace el ingreso y el costo; plantillas de cotización con secciones opcionales; descuentos y aprobaciones (nativo por grupo o automatización); términos de pago y posiciones fiscales por cliente; entregas en una o varias etapas; devoluciones; comisiones (módulo o analítica).

## Patrones de error
Listas de precio replicadas por cliente en lugar de reglas; descuentos aprobados por automatización que escribe el estado; pedidos confirmados sin entrega que inflan el ingreso al facturar por pedido; clientes duplicados con saldos repartidos; equipos sin responsable; etapas sin criterio de salida; vendedores con permisos de administrador para «ver todo»; cotizaciones de servicios sin producto de servicio que impide el proyecto automático.

## Por versión
15–16: `sale.order` con `invoice_status`; 17: rediseño de interfaz, catálogo de productos en el pedido, cambios en plantillas; 18: catálogo y variantes mejorados, cambios en descuentos (verificar); 19: campos y agentes de IA en CRM (Enterprise), puntuación de prospectos (verificar alcance por edición). Facturación electrónica de la localización: la factura nace del pedido, el CFDI exige uso, método y forma de pago del cliente correctos.

## Lo que pregunta un senior
¿Quién decide el precio y cómo se autoriza una excepción? ¿Cuándo se considera vendido: al confirmar, al entregar o al facturar? ¿Qué devoluciones existen y qué pasa con su costo? ¿Cuántas listas de precios reales hay en el negocio (no en el sistema)?

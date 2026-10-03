# Migraciones de versión: qué cambia y cómo se gobierna

Vigente al 2026-10-03. Verificar en las notas de versión y en el código de la rama antes de afirmar.

## Rutas de actualización
- **SaaS (Odoo Online):** Odoo actualiza; el cliente elige ventana; las personalizaciones de Studio se migran; las automatizaciones con código deben probarse en la base de pruebas de la actualización que Odoo entrega antes.
- **Odoo.sh:** solicitud de actualización desde la plataforma; se prueba en rama de staging con la base actualizada; los módulos propios se migran por el equipo del cliente o del partner; se repite hasta que staging esté limpio.
- **Local (on-premise):** Enterprise con el servicio de actualización de Odoo (carga de la base, descarga actualizada, pruebas); Community con OpenUpgrade de la OCA y migración manual de módulos propios.

## Plan de migración que no falla
1. Inventario: versión, edición, módulos propios y de terceros, automatizaciones, Studio, integraciones externas, API usada.
2. Línea de tiempo y limpieza previa: borradores antiguos, documentos abiertos sin sentido, duplicados, cuentas archivadas en uso, existencias negativas, transitorias con saldo.
3. Prueba de actualización en copia; lista de errores por módulo; decisión por módulo (migrar, sustituir por nativo, retirar).
4. Pruebas funcionales por área con casos del cliente (compra→recepción→factura→pago; venta→entrega→factura→cobro; cierre contable; nómina si aplica; CFDI si aplica).
5. Cuadres antes y después: balanza, valuación de inventario contra cuenta, saldos de clientes y proveedores, existencias por ubicación.
6. Ventana de corte con respaldo, plan de reversión y comunicación a usuarios; capacitación en lo que cambia.

## Cambios que pegan por salto
- **16 → 17:** sintaxis de vistas (`attrs`, `states`), `tree`→`list`, `name_get`→`_compute_display_name`, `_read_group` nueva firma, disparadores de automatización, interfaz nueva, `product_uom`→`product_uom_id` en compras. Pruebas: todas las vistas heredadas y automatizaciones.
- **17 → 18:** cambios en unidades y empaquetados (verificar), conciliación y reportes contables (verificar), API de ORM (verificar), requisitos de Python/PostgreSQL. Pruebas: inventario y contabilidad completas.
- **18 → 19:** valuación sin capas (`stock.valuation.layer` desaparece; transitorias de entrada/salida eliminadas; cierre de valuación), `res.groups.users`→`user_ids`, estado de pago `canceled`, nueva API JSON y obsolescencia de XML-RPC en SaaS, funciones de IA Enterprise. Riesgos específicos: acción de rebalanceo de transitorias, revaluaciones sin movimiento, vínculo asiento–albarán vacío, recepciones y entregas de 17/18 no facturadas que recargan inventario al facturarse.

## Señales para recomendar migrar en lugar de estabilizar
Base en versión con recargo de licencia o cercana a perder soporte; decenas de desarrollos a la medida sobre funciones que la versión nueva trae nativas; costo de estabilizar la versión actual mayor al de migrar y volver a configurar; integraciones propietarias del partner saliente que no viajan.

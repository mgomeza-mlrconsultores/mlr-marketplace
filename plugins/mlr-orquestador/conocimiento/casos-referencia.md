# Casos de referencia (anonimizados) y lecciones que ya costaron

Patrones vistos en proyectos reales de consultoría Odoo en México y Latinoamérica. Sin nombres ni datos de clientes. Cada agente los consulta para reconocer situaciones y no repetir errores.

## Alcance y horas
- **Horas trabajadas muy por encima de las facturadas** en un proyecto con rutas intercompañía multietapa, aprobaciones de descuento y controles de acceso a precios que crecieron sin contrato de alcance. Lección: contrato de alcance cerrado al inicio, control de horas contra ruta cotizada, cambio de alcance por escrito con precio.
- **Cotizaciones rechazadas por horas exageradas** en pymes: la ruta debe calibrarse contra el registro real; en bases vivas se cotiza depuración y reconstrucción, no creación; configuración puntual no pasa de hora y media.
- **Dirección recorta la ruta** y regala la configuración contable como beneficio comercial; el servicio contable recurrente va aparte en iguala.

## Inventario y valuación
- **Fluctuación agresiva del costo** (productos de miles a millones o a cero) en una comercializadora con decenas de sucursales: método oficial PEPS con categorías en estándar, facturación antes de recibir que impide encontrar capa válida, y automatizaciones intercompañía a la medida que omiten la valuación. Lección: antes de cualquier arreglo, mapa de métodos por categoría, orden operativo recepción→factura, y revisión de cada automatización que toca movimientos.
- **Duplicar una orden de venta y facturarla en cero** para dar salida y entrada a inventario de eventos: antipatrón que distorsiona ventas y costo. Lección: rutas de salida y retorno con documentos propios (traslados, devoluciones), no ventas ficticias.
- **Cadena de abastecimiento bajo pedido rota** por método de suministro mal configurado en una regla de traslado interno; **subcontratación en 19 que no genera reabastecimiento de componentes** al confirmar la compra por falta de rutas multietapa y ubicación de almacenamiento. Lección: rutas y reglas se leen completas antes de culpar al módulo.
- **Reajustes de inventario sin bitácora**: el cliente pide criterios para ajustes, almacenes y ubicaciones de ajuste, productos obsoletos y equipo de demostración. Lección: ubicación de inventario por motivo, cuenta de regularización por ubicación, política de obsoletos y demo.
- **Perecederos sin lote ni caducidad** en alimentos. Lección: revisión obligada en todo giro con vida útil.

## Contabilidad, multiempresa y unidades de negocio
- **Una razón social con varias unidades de negocio** (fábrica, tiendas, servicios compartidos): el esquema de compraventa entre empresas bajo un mismo RFC infla ingresos e IVA; se prefiere una sola compañía con almacenes por unidad, traslados al costo, utilidad por analítica y cuenta transitoria de tesorería para los adeudos internos; si son compañías separadas, DIOT y reportes deben consolidarse. Lección: la arquitectura se decide con el marco fiscal delante, no con la comodidad del reporte.
- **Grupo con tres líneas de negocio y dos empresas pero una sola que factura**: tres compañías que se facturan servicios integrales bajo maquila; verificado en 19 que las cuentas analíticas sin compañía viajan a la factura recíproca y las que tienen compañía se pierden.
- **Dos compañías en la misma base sin configuración multiempresa** y contabilidad fiscal fuera de Odoo (sistemas distintos por país). Lección: el diagnóstico formal antecede a la multiempresa; desarrollos sobre campos nativos para no comprometer migraciones.
- **Catálogo de cuentas con cuentas de activo usadas como ingreso o costo** (un 191 donde va 401 o 501); **todo el gasto en «otros gastos generales»** porque desde la orden de compra no aparece la etiqueta analítica; **contador externo que declara en otro sistema** y no cuadra con Odoo. Lección: corte contable a inicio de año, carga de facturas de proveedor por XML, visibilidad del IVA por pagar durante el mes.
- **Moneda con seis decimales** en una base SaaS: Odoo bloquea reducir decimales con asientos existentes; la corrección por SQL desde acción de servidor es último recurso y se documenta.
- **Cliente que cambió de régimen** (RESICO a general) y operó sin contabilidad formal en ejercicios previos: el saneamiento empieza por definir qué ejercicio se reconstruye y qué se declara.

## Migraciones y cortes de sistema
- **Corte de un ERP heredado a Odoo 16 local** con más de cien módulos propios: validar que cada saldo esté respaldado por su auxiliar, migrar activos con costo y depreciación acumulada, multimoneda con diferencia cambiaria, paralelo el último trimestre y ejercicio completo en el nuevo sistema; el cliente ejecuta, la firma valida y dictamina; un control que impide registrar sin dato contable no es defecto, se hace gobernable durante la carga.
- **Partner saliente con integración propietaria** (facturación electrónica) que no viaja al cambiar de socio. Lección: inventariar qué desarrollos son del cliente y cuáles no, antes de cotizar.
- **Recargo de licencia por versión antigua** al salir una versión nueva: la fecha de lanzamiento es un disparador comercial de migración.
- **Cambio de partner en Odoo.sh**: solicitud de accesos para que el cliente tome control de su proyecto y repositorios.

## Integraciones y soporte
- **Soporte SaaS acotado a 70–80 horas**: identificación determinista de contactos por identificador fiscal, correo y teléfono (sin campos de IA), creación de proyecto al ganar la oportunidad, formularios externos por webhook nativo o integrador, WhatsApp con API oficial.
- **Comercio electrónico con conector** (tienda en línea) y conciliación manual con operador logístico; la elección Odoo.sh con módulo frente a SaaS con integrador cambia licencias, mantenimiento y migraciones y se presenta como dos opciones.
- **Integración bancaria** cotizada a tarifa de especialización superior a la estándar.
- **Nómina mexicana en Odoo**: existe la localización, pero una firma puede decidir esperar una versión por los cambios que trae; va en segundo alcance.

## Infraestructura
- **Servidor Windows en la nube con RDP que deja de aceptar sesiones**: causa raíz en licenciamiento de escritorio remoto, no en red ni contraseñas; rodeo con sesión administrativa; limpieza de roles y directivas; cerrar puertos sin uso; MFA en cuenta raíz con segundo factor portátil; usuario con permisos mínimos para reinicios.

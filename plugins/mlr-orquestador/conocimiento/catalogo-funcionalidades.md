# Catálogo de funcionalidades de Odoo para rutas de cotización

Las tareas y subtareas de una ruta se nombran con la funcionalidad de Odoo, con mayúscula solo en la primera palabra, y la descripción es general (dice qué trabajo se hace en esa funcionalidad, sin cifras ni nombres del cliente). Un concepto contable no es una funcionalidad. El desarrollo es siempre la última aplicación, separada y condicional.

## Orden fijo de la ruta
1. Descubrimiento (levantamiento por área: inventario, compras, ventas, listas de materiales, valoración, contabilidad, cobranza y bancos; flujo objetivo).
2. Configuración general (usuarios y permisos, compañías, ajustes generales).
3. Aplicaciones que toca el proyecto, en el orden del flujo operativo.
4. Capacitación y cierre (sesiones por tema y rol, material, aceptación formal).
5. Desarrollo (condicional, al final, con su propio total).

## Inventario
Categorías de producto · Catálogo de productos · Variantes y atributos · Unidades de medida y empaquetados · Almacenes · Ubicaciones y rutas · Reglas de reabastecimiento · Lotes y fechas de caducidad · Estrategias de retiro · Costes en destino · Regularización de existencias · Valoración de inventario · Cierre de valoración · Transferencias por lotes · Códigos de barras · Inventario cíclico · Reportes de inventario

## Compras
Proveedores y tarifas de proveedor · Solicitudes de cotización y órdenes de compra · Aprobación por monto mínimo · Acuerdos de compra · Control de facturas de proveedor · Recepciones en varias etapas · Regularización de históricos de compras

## Ventas
Clientes y equipos de venta · Listas de precios · Cotizaciones y pedidos · Política de facturación · Entregas en varias etapas · Devoluciones · Plantillas de cotización · Regularización de históricos de ventas

## Fabricación
Listas de materiales · Centros de trabajo y rutas de producción · Órdenes de producción · Órdenes de trabajo · Subproductos y desechos · Costeo de fabricación y variaciones · Planificación maestra · Subcontratación

## Contabilidad
Plan de cuentas · Diarios · Impuestos y posiciones fiscales · Saldos iniciales · Pagos y métodos de pago · Extractos bancarios · Modelos de conciliación · Conciliación bancaria · Regularización contra comprobantes fiscales · Facturación electrónica de la localización (como funcionalidad de contabilidad, no como aplicación) · Activos fijos · Diferidos · Presupuestos · Contabilidad analítica · Multimoneda · Intercompañía · Fechas de bloqueo y cierre · Reportes financieros

## Punto de venta
Configuración de puntos de venta · Métodos de pago y cierre de sesión · Categorías y productos del punto de venta · Restaurante (mesas, cocina) · Programas de fidelidad · Reportes de ventas por sesión

## Transversales
Usuarios y permisos · Compañías y configuración general · Documentos y plantillas de impresión · Correo y plantillas · Importación de datos maestros · Depuración de datos · Material de capacitación · Sesiones de capacitación · Aceptación formal

## Nombres vetados y su sustituto
«Costo de ventas» → la funcionalidad que lo produce (Valoración de inventario, Política de facturación) · «Cuentas por cobrar» / «Cartera al corte» → Pagos y métodos de pago, Conciliación bancaria, Regularización de históricos de ventas · «Contabilidad electrónica» → Reportes financieros y la facturación electrónica de la localización como tarea de Contabilidad · «Ajustes de inventario» → Regularización de existencias · «Facturas de proveedor» y «Facturas de cliente» como tareas → Regularización de históricos de compras y de ventas · «Análisis de proceso» sin entregable → Diagrama de flujo objetivo (Descubrimiento) · «Integral» → se cotiza por separado y, si dirección quiere, opción conjunta

## Qué no es tarea
Lo que hace el sistema solo (tipos de operación al crear un almacén), lo estándar que no se modifica, tableros y reportes nativos sin cambios, análisis sin entregable, tareas de minutos (se absorben).

## Ficha de cada subtarea
Número (1.1.1), nombre de funcionalidad, tipo de trabajo (configuración, datos, definición, prueba, capacitación, desarrollo), descripción general, entregable verificable, hito de facturación, horas (0.5 a 16).

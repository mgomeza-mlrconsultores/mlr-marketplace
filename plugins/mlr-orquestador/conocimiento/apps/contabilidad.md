# Contabilidad (configuración funcional)

Complementa `patrones-contabilidad.md`.

## Decisiones que gobiernan el resultado
Plan de cuentas de la localización y su código agrupador; diarios por tipo con cuentas por defecto y secuencias; impuestos con cuentas, base de efectivo cuando aplique, retenciones; posiciones fiscales por tipo de cliente y proveedor; términos de pago; cuentas pendientes de cobro y pago; conciliación bancaria con modelos; multimoneda con tipos de cambio automáticos; analítica por planes y reglas de distribución; activos fijos con métodos de depreciación; diferidos; presupuestos; fechas de bloqueo; cierre de ejercicio; reportes financieros y declaraciones de la localización (en México: DIOT, contabilidad electrónica, CFDI).

## Patrones de error
Ver catálogo C-01 a C-16. Además: diario misceláneo usado para operación; impuestos duplicados por importación de datos; posiciones fiscales que mapean a cuentas archivadas; términos de pago con porcentajes que no suman cien; analítica obligatoria sin reglas de distribución; tipos de cambio manuales; cierre de ejercicio nunca ejecutado.

## Por versión
13+: `account.move` único; 16: planes analíticos múltiples y distribución en porcentaje; 17: nuevo widget de conciliación, fechas de bloqueo por tipo, `display_type`; 18: cambios en conciliación y en reportes (verificar); 19: estados de pago (`canceled`), cambios en pagos y en el flujo de conciliación (verificar en código), valuación sin capas que cambia la relación inventario–contabilidad. Localización mexicana: módulos `l10n_mx`, `l10n_mx_edi` y extensiones; versiones de CFDI y complementos por versión de Odoo (ver plugin fiscal).

## Lo que pregunta un senior
¿Quién firma las declaraciones y con qué sistema cuadra? ¿Qué cuentas de control admiten asientos manuales y por qué? ¿Qué día se bloquea el mes y quién lo decide? ¿Cuántas monedas operan y quién actualiza el tipo de cambio?

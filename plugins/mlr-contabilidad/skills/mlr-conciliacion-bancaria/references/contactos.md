# Depuración de contactos

Caso de uso ligado a la conciliación: un contacto sin RFC o duplicado hace que los CFDI no enlacen y que la DIOT salga mal.

- Cruce de contactos de Odoo contra el acumulado de Mi Admin: por RFC; si no hay RFC, por el UUID de sus facturas; si no, por nombre normalizado. En el caso de origen, 47 por RFC y 121 por nombre, y ninguno quedó sin pareja.
- Clientes: código postal de `DomicilioFiscalReceptor` y régimen de `RegimenFiscalReceptor` de sus facturas emitidas.
- Proveedores: régimen solo del XML o de la Constancia de Situación Fiscal. El código postal de `LugarExpedicion` no está confirmado como domicilio fiscal, y así se marca si la persona lo acepta.
- Criterios del caso de origen, que se confirman en cada cliente: a los proveedores sin fuente solo RFC y código postal, sin país ni nota; RFC genéricos (XAXX010101000, XEXX010101000) fuera del cruce; duplicados por RFC se fusionan.
- Cada corrección va como fila de Acciones con operación `escribir_campos`. Recordar el efecto de asignar país México: régimen 601 automático, así que el régimen va en el mismo cambio.
- La fusión de duplicados se hace con la persona en Odoo, una por una, porque es irreversible.

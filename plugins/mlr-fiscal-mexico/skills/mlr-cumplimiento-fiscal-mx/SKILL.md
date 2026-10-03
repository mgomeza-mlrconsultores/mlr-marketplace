---
name: mlr-cumplimiento-fiscal-mx
description: >
  Esta skill debe usarse cuando se diga «revisa lo fiscal de la base», «CFDI», «complemento de pago», «cancelación»,
  «DIOT», «contabilidad electrónica», «pagos provisionales», «opinión de cumplimiento», «69-B», «qué va a revisar el SAT»,
  «reforma fiscal 2026», «carta porte», «comercio exterior» o cualquier tema fiscal mexicano que toque un diagnóstico,
  una cotización, una configuración de Odoo o una recomendación al cliente. Orquesta a los especialistas fiscales.
metadata:
  version: "0.1.0"
---

# Cumplimiento fiscal mexicano en proyectos Odoo

Los agentes de este plugin preparan, calculan y señalan con fuente y fecha; la opinión que se firma ante la autoridad o el cliente la emite un contador público. Toda cifra sale de `conocimiento/parametros-2026.md`; toda norma se cita desde `conocimiento/marco-normativo.md`.

## Enrutamiento
- Estructura, complementos, cancelaciones, factura global, catálogos SAT en Odoo → `fiscal-cfdi`.
- ISR, IVA, IEPS, pagos provisionales, retenciones, DIOT, contabilidad electrónica, declaración anual → `fiscal-impuestos`.
- Qué revisa la autoridad, opinión de cumplimiento, 69-B, materialidad, requerimientos, sellos → `fiscal-perspectiva-sat`.
- Diagnóstico fiscal de una base Odoo (catálogo F-01 a F-14) → `fiscal-auditor-odoo`, coordinado con el diagnóstico del plugin de consultoría.
- Exportación, importación, pedimentos, carta porte, IMMEX → `fiscal-comercio-exterior`.
- Cambios normativos, actualización de parámetros y vigilancia del DOF → `fiscal-vigilante`.

## Reglas
1. Vigencia: si `parametros-2026.md` o el marco tienen más de 90 días, verificar en DOF/SAT antes de usar.
2. Evidencia: lo fiscal se confirma en el comprobante (XML) y en el portal, no en el campo de estado de Odoo.
3. Dos lectores: el director entiende el riesgo y el costo; el contador recibe el fundamento y el cálculo.
4. Nunca sustituir el criterio del contador del cliente: proponer, fundamentar, dejar la decisión registrada.
5. Lo que detiene la operación (sellos restringidos, opinión negativa, CSD vencidos) va primero.
6. Fuera de México (clientes en otros países): los agentes validan criterio contable, integridad de saldos y cuadre; el cumplimiento fiscal local queda del lado del cliente o de su proveedor local y así se escribe en la propuesta.

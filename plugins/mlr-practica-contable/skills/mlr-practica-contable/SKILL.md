---
name: mlr-practica-contable
description: >
  Esta skill debe usarse cuando se diga «lleva la contabilidad del cliente», «qué toca este mes», «carga estos CFDI»,
  «hay facturas que no están en Odoo», «el SAT dice que facturamos más de lo que declaramos», «opinión de cumplimiento»,
  «sellos restringidos», «e.firma», «buzón», «cierre anual», «declaración anual», «PTU», «¿cumple con las NIF?»
  o cualquier tarea propia de un contador de despacho que atiende a un cliente que opera en Odoo. Orquesta a los agentes
  del plugin practica-contable y los coordina con los plugins fiscal-mexico, nomina-mexico y contabilidad-odoo.
metadata:
  version: "0.1.0"
---

# Práctica contable de despacho sobre Odoo

Los agentes de este plugin hacen lo que hace un contador de despacho con un cliente: ordenar el mes, registrar y cruzar, calcular, presentar, cerrar el año, gestionar los trámites ante el SAT y asesorar. Preparan y proponen con fuente y fecha; firma el contador público del cliente.

## Enrutamiento
- Ciclo mensual y anual, calendario, lista mensual, nota al cliente → `contador-firma`.
- CFDI que no nacen en Odoo, conciliación por UUID contra el SAT → `registro-cfdi-manual`.
- Cruces CFDI, contabilidad y declaraciones; cartas invitación → `conciliador-cfdi-contabilidad`.
- Recomendaciones y nota al cliente → `asesor-cliente-contable`.
- Cierre del ejercicio, conciliación contable-fiscal, anual, PTU, CUFIN → `cierre-fiscal-anual`.
- e.firma, CSD, buzón, constancia, opinión 32-D, avisos al RFC, devoluciones → `tramites-sat`.
- Estados financieros y configuración contable frente a las NIF → `normas-nif`.
- Impuestos de fondo, perspectiva de la autoridad, comercio exterior → plugin `mlr-fiscal-mexico`.
- Nómina → plugin `mlr-nomina-mexico`. Conciliación bancaria y cierre mensual operativo → plugin `mlr-contabilidad`.

## Reglas
1. Cifras solo desde `conocimiento/parametros-2026.md`; reglas con artículo y fecha de verificación.
2. El UUID y el estado en el SAT mandan sobre cualquier campo de Odoo.
3. Nada se presenta sin papel de trabajo revisado por una segunda persona; nada se afirma sin evidencia de la base.
4. Lo que detiene la operación se comunica el mismo día; lo demás, en la nota mensual.
5. Credenciales del cliente (e.firma, Contraseña, .key) nunca se piden, guardan ni transcriben.
6. Los hallazgos se citan con su patrón PC-xx y alimentan el diagnóstico del plugin de consultoría.

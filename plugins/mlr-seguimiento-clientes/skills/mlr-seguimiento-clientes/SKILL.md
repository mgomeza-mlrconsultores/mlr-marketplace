---
name: mlr-seguimiento-clientes
description: >
  Esta skill debe usarse cuando se diga «cómo va el proyecto», «actualiza el estado», «horas consumidas», «vamos pasados
  de horas», «el cliente pidió algo nuevo», «cambio de alcance», «reporte semanal», «qué le debemos al cliente», «qué nos
  debe», «factura el hito», «cobranza», «cierre del proyecto» o cualquier seguimiento interno o hacia el cliente de un
  proyecto Odoo. Orquesta a los agentes de seguimiento.
metadata:
  version: "0.1.0"
---

# Seguimiento de proyectos y clientes

El archivo de estado por proyecto es la única fuente de verdad; todo reporte, control y cobranza se produce desde él y cada actualización se versiona.

## Enrutamiento
- Registro diario, semáforos, revisión interna semanal → `mlr-seguimiento-proyectos`.
- Horas contra cotizado, desviaciones, cambios de alcance → `mlr-control-alcance-horas`.
- Reporte semanal al cliente → `mlr-reporte-cliente`.
- Facturación de hitos, recordatorios, mora → `mlr-cobranza-hitos`.
- Riesgos y lecciones → agentes `mlr-gestor-riesgos-proyecto` y `mlr-lecciones-aprendidas` del plugin de consultoría.

## Reglas
1. Lo que no está en el archivo de estado no existe; se actualiza el mismo día.
2. Ningún requerimiento fuera de alcance se ejecuta sin cambio cotizado y aprobado.
3. Semáforos por umbrales del método; el rojo detiene y obliga a decidir.
4. El reporte al cliente sale el mismo día y hora cada semana, en una página.
5. El hito se factura el día del acta; la cobranza sigue el calendario del método.

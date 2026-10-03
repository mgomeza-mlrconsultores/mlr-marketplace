---
name: mlr-actualizar-conocimiento
description: >
  Esta skill debe usarse cuando se diga «actualiza el conocimiento de los agentes», «qué cambió en Odoo este mes»,
  «revisa las novedades de la versión», «actualiza los catálogos de patrones» o cuando venza la rutina mensual de
  actualización. Dirige al agente investigador-odoo por las fuentes oficiales, registra los cambios en la base de
  conocimiento y propone mejoras concretas a los agentes afectados.
metadata:
  version: "0.1.0"
---

# Actualizar la base de conocimiento

Los agentes valen lo que vale su conocimiento. Esta rutina lo mantiene al día sin que nadie tenga que recordarlo; se ejecuta el primer lunes de cada mes y cada vez que se publique una versión mayor de Odoo.

## Rutina
1. Leer `conocimiento/CAMBIOS.md` para saber qué se revisó la vez anterior y hasta qué fecha.
2. Lanzar `investigador-odoo` con estas búsquedas, en este orden, verificando en fuente primaria antes de registrar:
   - Notas de la versión vigente y de la siguiente: cambios en inventario, valuación, contabilidad, fabricación, punto de venta, API externa y Studio.
   - Repositorio `odoo/odoo`: commits recientes en `stock_account`, `account`, `stock`, `mrp`, `purchase`, `sale` de la rama vigente que cambien comportamiento.
   - Repositorios OCA del dominio: módulos migrados a la versión vigente, módulos nuevos relevantes, cambios en guías de contribución y migración.
   - Autoridad fiscal de `México`: comunicados con fecha de entrada en vigor, cambios en catálogos y comprobantes.
   - Comunidad: fallos conocidos reportados en los foros oficiales que afecten a los patrones del catálogo.
3. Por cada hallazgo relevante: qué cambia, a qué agente afecta, qué línea de la base de conocimiento se agrega o se marca obsoleta (con la versión en que dejó de aplicar). Nunca borrar conocimiento anterior.
4. Aplicar los cambios en `odoo-versiones.md`, los catálogos de patrones, `fuentes-oficiales.md` y, si procede, en los agentes; registrar cada cambio en `CAMBIOS.md` con fecha y fuente.
5. Entregar un boletín corto en prosa (máximo 300 palabras): qué cambió, qué hay que probar en la base demo y qué entregables en curso se ven afectados.
6. Si se sincroniza con la versión de la firma, portar los cambios al plugin de la firma en la misma sesión (skill `sincronizar-genericos` del plugin de plan de carrera o el procedimiento equivalente).

## Reglas
Fuente primaria siempre; fecha de consulta en cada registro; distinguir Community, Enterprise y SaaS; marcar «verificar» lo que no se pudo confirmar en código. La rutina no toca bases de clientes.

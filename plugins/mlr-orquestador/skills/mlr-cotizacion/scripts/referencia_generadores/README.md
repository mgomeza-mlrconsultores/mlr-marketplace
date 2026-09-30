# Generadores de referencia de una cotización

Implementación real de la cotización de Freshbox (29-sep-2026): dos proyectos, contabilidad e inventario, y la opción conjunta, cada uno con sus tres entregables. Se copia a `Documentos extras\<AAAAMMDD>\Interno\Cotización\` del cliente nuevo y se reescribe el contenido; la mecánica se conserva.

- `ruta.py` es el único origen de verdad: parámetros (tarifa ofertada, vigencia, anticipo, pagos B, descuento C, plazos), una ruta por proyecto con número, aplicación, tarea, subtarea, tipo, horas, hito y descripción, los nombres de hito, las tareas comunes que la conjunta fusiona y la contingencia interna, que nunca sale a un entregable. `cifras()` calcula todos los importes.
- `comun.py` elige el proyecto con la variable `PROY` (`contabilidad`, `inventario` o `integral` para la conjunta) y fija nombres de archivo. `MLR_IDENTIDAD` apunta a `mlr-identidad-visual/scripts` y `MLR_PLANTILLA` a la hoja membretada si no están en la ruta por defecto.
- `genera_propuesta.py`, `genera_plan.py` y `genera_xlsx.py` producen la propuesta económica, el plan de trabajo y el anexo de cinco hojas con fórmulas vivas.
- `verifica.py` cruza Word, PDF y Excel recalculado contra `ruta.py` y barre la contingencia y cualquier mención de tarifa de lista, preferencial o beneficio. La ortografía y la ocupación de planas se revisan aparte con `verifica_documento.py` y `revisa_ortografia.py`.
- `build.sh` corre todo para un proyecto: `PROY=inventario ./build.sh`.

La ruta se aprueba antes en el chat, en texto. Estos scripts no se corren hasta tener esa aprobación.

# Fase 7 — Entregables

**No se abre este archivo hasta que Marcos aprobo el contenido completo en el chat.**

## Origen unico de verdad

Antes de generar cualquier documento se escribe un solo modulo de datos — `datos.py` en la carpeta de trabajo interno — con:

- Tarifas, fecha limite de la preferencial, numero de sedes, porcentaje de anticipo.
- La ruta completa: numero, tarea, tipo de trabajo, horas, hito.
- Los importes derivados, calculados, nunca teclados.

Word y Excel se construyen desde ese modulo. Si una cifra aparece distinta en los dos documentos, es porque alguien la escribio a mano.

Regla firme: **cuando Marcos edita un archivo a mano, ese archivo ya no se regenera desde el script.** Se edita.

## Propuesta en Word

El formato, el membrete y el registro de redaccion **no se definen aqui**: se cargan de `mlr-redaccion`, `mlr-identidad-visual` y las directrices vigentes en memoria. Esta seccion solo fija lo que es propio de una cotizacion.

El molde es el documento aprobado por direccion, `Cotizacion_Comband DTH_Maquila Nomina.pdf`. Se abre y se copia su estructura; no se disena una distinta.

**Esqueleto, en este orden:**

1. Bloque de caratula en la parte alta de la primera plana: titulo, firmantes en mayusculas, y solo dos metadatos —Cliente (con la atencion en la misma linea) y Fecha—. **Sin portada aparte.**
2. Saludo nominal: `Estimado Sr. <Nombre>:`
3. Parrafo de presentacion: «Por medio de la presente, MLR Consultores presenta a <cliente> la propuesta economica para <objeto>, considerando <los datos de partida>.»
4. `1. Alcance del servicio propuesto` — lista con guiones de lo que incluye.
5. `2. <Tarifas o inversion>` — cuadro de cifras.
6. `3. <Estimado por fase, etapas o calendario>` — cuadro de cifras.
7. `4. Condiciones comerciales` — lista con guiones: moneda e IVA, vigencia, forma de pago, lo que se contrata aparte.
8. Cierre de cortesia: «Quedamos atentos a sus comentarios y esperamos contar con su aprobacion para definir los siguientes pasos.»
9. Bloque de contacto.

**Extension: 3 a 5 planas.** El documento aprobado resuelve una cotizacion completa en 3. Cuatro a seis secciones numeradas, no doce. Si el contenido no cabe, el detalle se va al anexo en hoja de calculo, nunca a mas planas de prosa.

- El desglose de tareas, horas y etapas **no** va en el documento principal. Va en el anexo. El principal presenta los totales, los hitos y las condiciones.
- Los cuadros son de cifras. Un cuadro descriptivo, que sustituye un argumento por una retícula de frases, no va.
- Cada cifra del texto tiene su gemela en el anexo, con el mismo valor.
- El registro de redaccion es el de `mlr-redaccion`, que esta tomado de ese mismo archivo aprobado. Es la parte que direccion critica primero.

## Anexo en Excel

Hojas tipicas: ruta de implementacion, resumen por etapa, programa y avance, mezcla del proyecto, condiciones economicas, criterios y supuestos.

- Formulas vivas, nunca valores calculados y pegados.
- Las formulas referencian los nombres de hoja exactos, con su acentuacion. Si se renombra una hoja, se ajustan las formulas.
- Los importes por hito se redondean en la formula, no a ojo, y el ultimo hito absorbe el redondeo.

## Verificacion antes de entregar, programatica

1. **Recalculo completo** del libro. Cero errores, cero formulas sin evaluar.
2. **Cuadre de cifras.** Total de horas, suma por etapa, suma por hito, suma por tipo de trabajo, importes y precio por sede: todo contra el origen unico.
3. **Cruce Word contra Excel.** Cada cifra del texto existe igual en el anexo.
4. **Ortografia y acentuacion.** Verificacion automatizada sobre el texto final, con proteccion de nombres de archivo, de hoja y de identificadores tecnicos. Un documento de cliente sin acentos es un defecto grave.
5. **Revision visual real.** Exportar a PDF, renderizar a imagen y mirarla. Paginas, ocupacion, invasion del membrete, cuadros partidos. Lo que no se ve, no se afirma.
6. **Barrido de contingencia.** Buscar la palabra y el importe interno en los dos entregables. Cero apariciones.

Si alguna verificacion no se pudo ejecutar — por ejemplo, exportacion a PDF no disponible en la maquina — se declara en el chat que quedo sin revisar visualmente. No se da por bueno lo que no se vio.

## Archivo y registro

Ruta local del cliente con la estructura MLR vigente, separando la carpeta de trabajo interno de la carpeta que ve el cliente.

Al cerrar, registrar en memoria los parametros del proyecto: horas totales, etapas, tareas, tarifas, exclusiones y lo que quedo pendiente. Esa es la calibracion de la siguiente cotizacion.

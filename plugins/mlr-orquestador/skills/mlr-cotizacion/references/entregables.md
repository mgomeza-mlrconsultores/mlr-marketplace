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
4. `1. Alcance del servicio propuesto` — lista con guiones de los entregables, construida sobre funcionalidad nativa.
5. `2. Esfuerzo estimado` — cuadro de dos columnas, aplicacion y horas, con el total. Debajo, un parrafo que separa configuracion, datos y documentacion del desarrollo, declara que son horas efectivas de consultoria y no dias naturales, y remite el desglose por tarea al anexo.
6. `3. Plazo de ejecucion` — plazo en meses desde la orden de inicio, condicionado a la oportunidad con que el cliente entregue informacion y personal, con la evaluacion conjunta a partir del mes siguiente al plazo.
7. `4. Inversion y programa de pagos` — tarifa de lista con su importe, tarifa preferencial con fecha limite explicita y el beneficio en pesos, y las dos modalidades: **A**, anticipo contra firma y saldo por hito; **B**, pagos mensuales iguales sin anticipo. Un cuadro por modalidad.
8. `5. Desarrollo` — cuando existe: sus tareas, su total y la frase que deja la decision al cliente. Si se puede sustituir por un producto de mercado, la comparacion con su costo.
9. `6. Costos de plataforma a cargo del cliente` — cuando aplique: suscripcion, alojamiento, conectores, con el tipo de cambio del DOF del dia y el numero de usuarios supuesto. Se declara que no forman parte de los honorarios.
10. `7. Supuestos, exclusiones y condiciones` — lista con guiones: moneda e IVA, vigencia de la preferencial, que el alcance del apartado 1 es el alcance contratado, lo que se contrata aparte, trabajo sobre base de pruebas, y lo que queda fuera nombrado uno por uno.
11. `8. Observaciones sobre la base actual` — solo cuando se audito una base viva: los hallazgos que el cliente necesita conocer, redactados como observacion tecnica y sin senalar al implementador anterior.
12. Cierre de cortesia: «Quedamos atentos a sus comentarios y esperamos contar con su aprobacion para definir los siguientes pasos.»
13. Bloque de contacto.

Los apartados 5, 6 y 8 se omiten cuando el proyecto no los tiene, y los siguientes se renumeran.

**Extension: 3 a 6 planas.** Cotizacion_Comband resuelve una cotizacion de servicio en 3; Aire Libre LATAM y Dunedin, con ruta por aplicaciones y cuadros de hitos, quedaron en 6. Cuatro a seis secciones numeradas, no doce. Si el contenido no cabe, el detalle se va al anexo en hoja de calculo, nunca a mas planas de prosa.

- El desglose de tareas, horas y etapas **no** va en el documento principal. Va en el anexo. El principal presenta los totales, los hitos y las condiciones.
- Los cuadros son de cifras. Un cuadro descriptivo, que sustituye un argumento por una retícula de frases, no va.
- Cada cifra del texto tiene su gemela en el anexo, con el mismo valor.
- El registro de redaccion es el de `mlr-redaccion`, que esta tomado de ese mismo archivo aprobado. Es la parte que direccion critica primero.

## Anexo en Excel

**Cinco hojas, con estos nombres exactos y en este orden:**

1. `Parametros` — dos columnas, concepto y valor: cliente, fecha de emision, tarifa de lista, tarifa preferencial, fecha limite de la preferencial, anticipo, numero de sedes o empresas, numero de pagos de la modalidad B. Todo lo demas referencia esta hoja.
2. `Ruta` — seis columnas: `Num.` (jerarquico, 1.1, 1.2), `Aplicacion`, `Tarea`, `Tipo de trabajo`, `Horas`, `Hito`. Una fila por tarea y una fila final de total con `SUM`.
3. `Resumen por etapa` — una fila por aplicacion con `SUMIF` contra `Ruta`, mas porcentaje del proyecto, importe preferencial e importe de lista, todos calculados contra `Parametros`.
4. `Hitos` — anticipo y un renglon por hito, con horas e importe. Los importes salen del total y del porcentaje de anticipo, nunca tecleados.
5. `Mezcla` — horas y porcentaje por tipo de trabajo con `SUMIF`, y al pie la separacion entre el bloque de desarrollo y el de configuracion, datos y documentacion.

El desarrollo aparece en `Ruta` como su propia aplicacion, de modo que sale de los tres resumenes sin tocar ninguna formula.

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

Los entregables se guardan en la carpeta del cliente dentro de `MLR Odoo\`. **Si el cliente ya tiene carpeta, se usa la suya; nunca se crea una paralela ni se inventa un nombre nuevo.** Si no existe, se crea con esta estructura:

```
MLR Odoo\<Cliente>\
  Informes\<AAAAMMDD>\              lo que recibe el cliente
  Documentos extras\<AAAAMMDD>\     lo que mando el cliente y el trabajo de esa fecha
    Interno\                        scripts, origen unico de datos, salidas de diagnostico
      Version reemplazada\          entregables sustituidos despues de emitidos
  Capturas de pantalla\<AAAAMMDD>\
  Contexto\                         ficha del cliente y memoria
```

Reglas del archivo:

- La carpeta de fecha es `AAAAMMDD` sin guiones, la del dia de emision. Una fecha por ronda de entrega: si se reemite, se abre una carpeta nueva y la anterior queda intacta.
- **Todo entregable al cliente va en `Informes\<AAAAMMDD>\`**, incluidas las cotizaciones. No se crea una carpeta `Propuesta` suelta: ese patron quedo superado.
- El origen unico de datos, los generadores y las salidas del diagnostico van en `Documentos extras\<AAAAMMDD>\Interno\`, nunca junto a los archivos que abre el cliente.
- **Ningun script archivado lleva credenciales.** La llave de API se lee de variable de entorno; si el script de trabajo la tuvo, se retira antes de archivarlo.
- Cuando el cliente tiene varios proyectos vivos a la vez, la estructura completa se repite dentro de una carpeta por proyecto.

Al cerrar, registrar en memoria los parametros del proyecto: horas totales, etapas, tareas, tarifas, exclusiones y lo que quedo pendiente. Esa es la calibracion de la siguiente cotizacion.

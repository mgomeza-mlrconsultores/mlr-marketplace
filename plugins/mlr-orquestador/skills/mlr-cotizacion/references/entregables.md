# Fase 7 — Entregables

**No se abre este archivo hasta que Marcos aprobo el contenido completo en el chat.**

## Origen unico de verdad

Antes de generar cualquier documento se escribe un solo modulo de datos — `datos.py` en la carpeta de trabajo interno — con:

- Tarifas, fecha limite de la preferencial, numero de sedes, porcentaje de anticipo.
- La ruta completa: numero, tarea, tipo de trabajo, horas, hito.
- Los importes derivados, calculados, nunca teclados.

Word y Excel se construyen desde ese modulo. Si una cifra aparece distinta en los dos documentos, es porque alguien la escribio a mano.

Regla firme: **cuando Marcos edita un archivo a mano, ese archivo ya no se regenera desde el script.** Se edita.

## Dos documentos en Word

Direccion fijo el 23 de septiembre de 2026 el modelo que armo el contador para Saguapac: la parte comercial y la parte de proyecto van en **dos documentos separados**, y el anexo en hoja de calculo va aparte. El cliente lee primero cuanto y como paga en dos o tres hojas, y el detalle del proyecto lo consulta en su propio documento.

| Pieza | Nombre del archivo | Extension |
|---|---|---|
| Propuesta economica | `1. MLR - Propuesta Economica - <Cliente>.docx` | **2 a 3 planas** |
| Plan de trabajo y alcance detallado | `2. MLR - Plan de Trabajo y Alcance Detallado - <Cliente>.docx` | hasta 6 planas |
| Anexo de ruta y horas | `MLR - Anexo de Ruta y Horas - <Cliente>.xlsx` | cinco hojas |

El formato, el membrete y el registro **no se definen aqui**: se cargan de `mlr-redaccion`, `mlr-identidad-visual` y las directrices vigentes en memoria. Los dos documentos se construyen con `documento_mlr.py` y pasan el verificador cada uno por separado.

### 1. Propuesta economica

Titulo de caratula `Cotizacion / Proyecto Odoo`. Todo lo que tiene precio vive aqui y solo aqui.

1. Caratula, saludo nominal y parrafo de presentacion «Por medio de la presente, MLR Consultores presenta a <cliente> la propuesta economica para <objeto>, considerando <datos de partida>.»
2. Un parrafo que remite al plan de trabajo y al anexo.
3. `1. Alcance del servicio propuesto` — un solo parrafo con las horas totales y los entregables enunciados de corrido, y la mencion del desarrollo aparte con sus horas. El detalle esta en el plan.
4. `2. Inversion` — tarifa de lista y preferencial con fecha limite, y los importes y el beneficio de cada opcion de alcance, en prosa.
5. `3. Esquemas de pago` — un parrafo que explica A, B y C con sus cifras de mensualidad y descuento, el cuadro comparativo de los tres esquemas con una columna por opcion de alcance, y el cuadro de hitos del esquema A.
6. `4. Condiciones esenciales` — moneda e IVA con vigencia, **la clausula de pago anticipado**, adicionales y precio de replica, lo que se contrata aparte y el requisito de inicio.
7. Parrafo de alcance negociable, cierre con la sesion de revision previa a la firma y bloque de contacto.

Si no cabe en tres planas, lo que sobra es prosa: se recorta texto, no se quitan los cuadros de esquemas.

### 2. Plan de trabajo y alcance detallado

Titulo de caratula `Plan de trabajo / y alcance detallado`. Abre declarando que forma parte de la propuesta economica de la misma fecha y que **los importes no se repiten aqui**. No lleva un solo importe de honorarios: solo horas. Las cifras del diagnostico del cliente si van.

1. `1. Alcance del servicio propuesto` — el mismo titulo que en la propuesta, con los entregables en vinetas, uno por renglon de alcance.
2. `2. Esfuerzo estimado` — cuadro de etapas y horas, y el parrafo que separa configuracion, datos y lo demas, declara horas efectivas y remite al anexo.
3. `3. Plazo de ejecucion`.
4. `4. Desarrollo complementario, a decisión de <cliente>` — cuando existe. Se explica en dos parrafos que el cliente entienda sin conocer Odoo: primero, que resuelve ya el alcance contratado sin el desarrollo y que se ve con eso; despues, que agrega el desarrollo, con la regla de negocio del propio cliente escrita con sus cifras (en Ah Cacao, la tarifa interna del 50% del precio al publico con precios fijos), cuando se registra y que efecto contable y fiscal tiene. Las tareas del cuadro se nombran por lo que hacen para el cliente, no por la tecnica. Cierra con la remision a la propuesta economica para su importe.
5. `5. Observaciones sobre la base actual` — cuando se audito una base viva.
6. `6. Supuestos, exclusiones y condiciones` — sin moneda ni importes.
7. Cierre de cortesia y bloque de contacto.

Los apartados 4 y 5 se omiten cuando no aplican, y los siguientes se renumeran.

### Reglas comunes

- Este par **no** sigue la regla de espejo de numeracion de la directiva de informe principal y anexo tecnico: la propuesta es comercial y el plan es de proyecto, y sus indices son distintos por naturaleza. Lo que si se exige es que el apartado 1 lleve el mismo titulo en los dos, que las etapas se llamen igual en los dos y en el anexo, y que toda cifra coincida.
- El desglose de tareas vive en el anexo. Los cuadros son de cifras; un cuadro descriptivo no va.
- Registro de `mlr-redaccion`, que es la parte que direccion critica primero.

## Anexo en Excel

**Cinco hojas, con estos nombres exactos y en este orden:**

1. `Parametros` — dos columnas, concepto y valor: cliente, fecha de emision, tarifa de lista, tarifa preferencial, fecha limite de la preferencial, anticipo del esquema A, numero de pagos del esquema B, descuento del esquema C, numero de sedes o empresas. Todo lo demas referencia esta hoja.
2. `Ruta` — seis columnas: `Num.` (jerarquico, 1.1, 1.2), `Aplicacion`, `Tarea`, `Tipo de trabajo`, `Horas`, `Hito`. Una fila por tarea y una fila final de total con `SUM`.
3. `Resumen por etapa` — una fila por aplicacion con `SUMIF` contra `Ruta`, mas porcentaje del proyecto, importe preferencial e importe de lista, todos calculados contra `Parametros`.
4. `Hitos` — el esquema A con anticipo y un renglon por hito, con una columna por opcion de alcance; debajo, la mensualidad del esquema B y el descuento, el pago y la tarifa efectiva del esquema C. Los importes salen del total y de los porcentajes, nunca tecleados.
5. `Mezcla` — horas y porcentaje por tipo de trabajo con `SUMIF`, y al pie la separacion entre el bloque de desarrollo y el de configuracion, datos y documentacion.

El desarrollo aparece en `Ruta` como su propia aplicacion, de modo que sale de los tres resumenes sin tocar ninguna formula.

- Formulas vivas, nunca valores calculados y pegados.
- Las formulas referencian los nombres de hoja exactos, con su acentuacion. Si se renombra una hoja, se ajustan las formulas.
- Los importes por hito se redondean en la formula, no a ojo, y el ultimo hito absorbe el redondeo.

## Verificacion antes de entregar, programatica

1. **Recalculo completo** del libro. Cero errores, cero formulas sin evaluar.
2. **Cuadre de cifras.** Total de horas, suma por etapa, suma por hito, suma por tipo de trabajo, importes y precio por sede: todo contra el origen unico.
3. **Cruce de los dos Word contra el Excel.** Cada cifra de la propuesta existe igual en el anexo, y el plan de trabajo no contiene ningun importe de honorarios.
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

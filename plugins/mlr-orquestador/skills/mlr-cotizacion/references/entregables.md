# Fase 7 — Entregables

**No se abre este archivo hasta que Marcos aprobó el contenido completo en el chat.**

## Origen único de verdad

Antes de generar cualquier documento se escribe un solo módulo de datos — `datos.py` en la carpeta de trabajo interno — con:

- Tarifa ofertada y su fecha límite, número de sedes, porcentaje de anticipo, pagos del esquema B y descuento del esquema C.
- La ruta completa: número, tarea, tipo de trabajo, horas, hito.
- Los importes derivados, calculados, nunca teclados.

Cuando hay varias cotizaciones del mismo cliente (contabilidad, inventario y la conjunta) el origen es uno solo, `ruta.py`, con una ruta por proyecto y la conjunta armada por código a partir de las otras dos; el proyecto se elige con una variable de entorno y un `build.sh` genera, convierte a PDF, recalcula y verifica las tres. Implementación de referencia en `scripts/referencia_generadores/` (Freshbox, 29-sep-2026).

Word y Excel se construyen desde ese módulo. Si una cifra aparece distinta en los dos documentos, es porque alguien la escribió a mano.

Regla firme: **cuando Marcos edita un archivo a mano, ese archivo ya no se regenera desde el script.** Se edita.

## Dos documentos en Word

Dirección fijo el 23 de septiembre de 2026 el modelo que armo el contador para Saguapac: la parte comercial y la parte de proyecto van en **dos documentos separados**, y el anexo en hoja de cálculo va aparte. El cliente lee primero cuanto y como paga en dos o tres hojas, y el detalle del proyecto lo consulta en su propio documento.

| Pieza | Nombre del archivo | Extensión |
|---|---|---|
| Propuesta económica | `1. Propuesta Económica - <Cliente>.docx` | **2 a 3 planas** |
| Plan de trabajo y alcance detallado | `2. Plan de Trabajo y Alcance Detallado - <Cliente>.docx` | hasta 6 planas |
| Anexo de ruta y horas | `3. Anexo de Ruta y Horas - <Cliente>.xlsx` | cinco hojas |

Los nombres de archivo **no llevan el prefijo «MLR»**: arrancan con el número y el nombre del documento, con tildes, y cierran con el nombre del cliente. La firma ya va en el membrete; el Word y el PDF llevan el mismo nombre.

El formato, el membrete y el registro **no se definen aquí**: se cargan de `mlr-redaccion`, `mlr-identidad-visual` y las directrices vigentes en memoria. Los dos documentos se construyen con `documento_mlr.py` y pasan el verificador cada uno por separado.

### 1. Propuesta económica

Título de carátula `Cotizacion / Proyecto Odoo`. Todo lo que tiene precio vive aquí y solo aquí.

1. Carátula, saludo nominal y párrafo de presentación «Por medio de la presente, MLR Consultores presenta a <cliente> la propuesta económica para <objeto>, considerando <datos de partida>.»
2. Un párrafo que remite al plan de trabajo y al anexo.
3. `1. Alcance del servicio propuesto` — un solo párrafo con las horas totales y los entregables enunciados de corrido, y la mención del desarrollo aparte con sus horas. El detalle está en el plan.
4. `2. Inversión` — la tarifa ofertada con su fecha límite y el importe de cada opción de alcance, en prosa. Sin tarifa de lista, sin preferencial y sin beneficio (dirección, 29-sep-2026).
5. `3. Esquemas de pago` — un párrafo que explica A, B y C con sus cifras de mensualidad y descuento, el cuadro comparativo de los tres esquemas con una columna por opción de alcance, y el cuadro de hitos del esquema A.
6. `4. Condiciones esenciales` — moneda e IVA con vigencia, **la clausula de pago anticipado**, adicionales y precio de replica, lo que se contrata aparte y el requisito de inicio.
7. Párrafo de alcance negociable, cierre con la sesión de revisión previa a la firma y bloque de contacto.

Si no cabe en tres planas, lo que sobra es prosa: se recorta texto, no se quitan los cuadros de esquemas.

### 2. Plan de trabajo y alcance detallado

Título de carátula `Plan de trabajo / y alcance detallado`. Abre declarando que forma parte de la propuesta económica de la misma fecha y que **los importes no se repiten aquí**. No lleva un solo importe de honorarios: solo horas. Las cifras del diagnóstico del cliente si van.

1. `1. Alcance del servicio propuesto` — el mismo título que en la propuesta, con los entregables en viñetas, uno por renglón de alcance.
2. `2. Esfuerzo estimado` — cuadro de etapas y horas, y el párrafo que separa configuración, datos y lo demás, declara horas efectivas y remite al anexo.
3. `3. Plazo de ejecucion`.
4. `4. Desarrollo complementario, a decisión de <cliente>` — cuando existe. Se explica en dos párrafos que el cliente entienda sin conocer Odoo: primero, que resuelve ya el alcance contratado sin el desarrollo y que se ve con eso; después, que agrega el desarrollo, con la regla de negocio del propio cliente escrita con sus cifras (en Ah Cacao, la tarifa interna del 50% del precio al público con precios fijos), cuando se registra y que efecto contable y fiscal tiene. Las tareas del cuadro se nombran por lo que hacen para el cliente, no por la técnica. Cierra con la remisión a la propuesta económica para su importe.
5. `5. Observaciones sobre la base actual` — cuando se audito una base viva.
6. `6. Supuestos, exclusiones y condiciones` — sin moneda ni importes.
7. Cierre de cortesía y bloque de contacto.

Los apartados 4 y 5 se omiten cuando no aplican, y los siguientes se renumeran.

### Reglas comunes

- Este par **no** sigue la regla de espejo de numeración de la directiva de informe principal y anexo técnico: la propuesta es comercial y el plan es de proyecto, y sus indices son distintos por naturaleza. Lo que si se exige es que el apartado 1 lleve el mismo título en los dos, que las etapas se llamen igual en los dos y en el anexo, y que toda cifra coincida.
- El desglose de tareas vive en el anexo. Los cuadros son de cifras; un cuadro descriptivo no va.
- Registro de `mlr-redaccion`, que es la parte que dirección crítica primero.

## Anexo en Excel

**Cinco hojas, con estos nombres exactos y en este orden:**

1. `Parametros` — dos columnas, concepto y valor: cliente, atención, fecha de emisión, vigencia de la tarifa ofertada, tarifa ofertada, anticipo del esquema A, número de pagos del esquema B, descuento del esquema C, plazo y número de sedes o empresas. En la opción conjunta, además, las horas y pagos B de cada proyecto por separado. Todo lo demás referencia esta hoja.
2. `Ruta` — seis columnas: `Num.` (jerárquico, 1.1, 1.2), `Aplicacion`, `Tarea`, `Tipo de trabajo`, `Horas`, `Hito`. Una fila por tarea y una fila final de total con `SUM`.
3. `Resumen por etapa` — una fila por aplicación con `SUMIF` contra `Ruta`: horas, porcentaje del proyecto e importe a la tarifa ofertada, calculados contra `Parametros`. Sin columna de lista ni de beneficio. En la conjunta, `Ruta` lleva una columna `Proyecto` y el resumen agrega debajo el comparativo de las tres opciones con sus horas e importes.
4. `Hitos` — el esquema A con anticipo y un renglón por hito, con una columna por opción de alcance; debajo, la mensualidad del esquema B y el descuento, el pago y la tarifa efectiva del esquema C. Los importes salen del total y de los porcentajes, nunca tecleados.
5. `Mezcla` — horas y porcentaje por tipo de trabajo con `SUMIF`, y al pie la separación entre el bloque de desarrollo y el de configuración, datos y documentación.

El desarrollo aparece en `Ruta` como su propia aplicación, de modo que sale de los tres resúmenes sin tocar ninguna fórmula.

- Fórmulas vivas, nunca valores calculados y pegados.
- Las fórmulas referencian los nombres de hoja exactos, con su acentuación. Si se renombra una hoja, se ajustan las fórmulas.
- Los importes por hito se redondean en la fórmula, no a ojo, y el último hito absorbe el redondeo.

## Verificación antes de entregar, programática

1. **Recalculo completo** del libro. Cero errores, cero fórmulas sin evaluar.
2. **Cuadre de cifras.** Total de horas, suma por etapa, suma por hito, suma por tipo de trabajo, importes y precio por sede: todo contra el origen único.
3. **Cruce de los dos Word contra el Excel.** Cada cifra de la propuesta existe igual en el anexo, y el plan de trabajo no contiene ningún importe de honorarios.
4. **Ortografía y acentuación.** `verifica_documento.py` ya revisa el texto y el nombre de cada PDF; además se corre `mlr-redaccion/scripts/revisa_ortografia.py` sobre los tres archivos, Word, PDF y Excel, que revisa también los nombres de hoja, cada celda de texto del anexo y las mayúsculas de estilo inglés en tareas y encabezados. Los nombres de archivo llevan tildes («Propuesta Económica»); un archivo o una celda sin tilde es un defecto grave y no se entrega.
5. **Revisión visual real.** Exportar a PDF, renderizar a imagen y mirarla. Páginas, ocupación, invasión del membrete, cuadros partidos. Lo que no se ve, no se afirma.
6. **Barrido de contingencia.** Buscar la palabra y el importe interno en los dos entregables. Cero apariciones.

Si alguna verificación no se pudo ejecutar — por ejemplo, exportación a PDF no disponible en la maquina — se declara en el chat que quedo sin revisar visualmente. No se da por bueno lo que no se vio.

## Archivo y registro

Los entregables se guardan en la carpeta del cliente dentro de `MLR Odoo\`. **Si el cliente ya tiene carpeta, se usa la suya; nunca se crea una paralela ni se inventa un nombre nuevo.** Si no existe la carpeta del cliente, alguna de sus carpetas fijas o la de fecha, se crean completas, con todas las intermedias, antes de guardar y sin preguntar. La regla única está en `mlr-orquestador/references/carpetas-y-entrega.md`:

```
MLR Odoo\<Cliente>\
  Informes\<AAAAMMDD>\              lo que recibe el cliente
  Documentos extras\<AAAAMMDD>\     lo que mandó el cliente y el trabajo de esa fecha
    Interno\                        scripts, origen unico de datos, salidas de diagnostico
      Version reemplazada\          entregables sustituidos despues de emitidos
  Capturas de pantalla\<AAAAMMDD>\  evidencia visual numerada; nunca dentro de Informes
  Contexto\                         ficha del cliente y memoria
```

Reglas del archivo:

- La carpeta de fecha es `AAAAMMDD` sin guiones, la del día de emisión. Una fecha por ronda de entrega: si se reemite, se abre una carpeta nueva y la anterior queda intacta.
- **Todo entregable al cliente va en `Informes\<AAAAMMDD>\`**, incluidas las cotizaciones. No se crea una carpeta `Propuesta` suelta: ese patrón quedo superado.
- El origen único de datos, los generadores y las salidas del diagnóstico van en `Documentos extras\<AAAAMMDD>\Interno\`, nunca junto a los archivos que abre el cliente.
- **Ningún script archivado lleva credenciales.** La llave de API se lee de variable de entorno; si el script de trabajo la tuvo, se retira antes de archivarlo.
- Cuando el cliente tiene varios proyectos vivos a la vez, la estructura completa se repite dentro de una carpeta por proyecto.

Al cerrar, registrar en memoria los parámetros del proyecto: horas totales, etapas, tareas, tarifas, exclusiones y lo que quedo pendiente. Esa es la calibración de la siguiente cotización.

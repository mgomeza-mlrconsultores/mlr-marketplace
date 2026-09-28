# Carátula y estructura del documento formal

Todo esto está medido sobre el documento que dirección aprobó y envío a cliente:

**`G:\Unidades compartidas\MMLR 2025\Hoja Membretada\Cotizacion_Comband DTH_Maquila Nomina.pdf`**

Autora: C.P. Mónica Arellano. Es el patrón de la firma. Ante cualquier duda, se abre y se
copia. No se diseña una carátula nueva ni se «mejora» la existente.

## No hay portada aparte

El error que dirección rechazo fue componer una portada dedicada —título grande, nueve
etiquetas de metadatos y media plana en blanco— y empezar el contenido en la plana 2. **Eso
no se hace.**

La carátula es un **bloque de cabecera en la parte alta de la primera plana**. Debajo, en la
misma plana, arranca el saludo y el contenido. Un documento de tres planas tiene tres planas
de contenido.

## Bloque de carátula, medidas exactas

Sobre hoja carta, con la plantilla `Hoja Membretada MLR - varias paginas.docx`:

| Elemento | Especificación |
|---|---|
| Título | **42 pt**, teal `#23656F`, negritas, centrado. Una o dos lineas, nunca tres. |
| Firmantes | **16 pt**, teal `#23656F`, negritas, centrado, **en mayúsculas**: `C.P. MONICA ARELLANO \| C.P. JUAN MARCOS LÓPEZ` |
| Etiqueta de metadato | **13 pt**, teal `#23656F`, negritas. Sangría de 260 tw desde el margen. |
| Valor de metadato | **13 pt**, negro, negritas. A 1480 tw desde el margen. |
| Saludo | **15 pt**, teal `#23656F`, negritas, alineado al margen izquierdo: `Estimado Sr. <Nombre>:` |
| Cuerpo | **11 pt**, negro, justificado |
| Encabezado de sección | **13 pt**, teal `#23656F`, negritas, numerado `1. Titulo`. **Sin filete debajo.** |

## Ritmo vertical, medido en el documento aprobado

Posiciones del borde superior de cada bloque, en puntos desde el borde de la hoja. **Se
calibran renderizando a PDF y midiendo, no a ojo:** la diferencia entre 235 y 251 no se ve
en una captura, pero el documento entero queda desplazado.

| Bloque | Posición |
|---|---|
| Título, primer renglón | 130 pt |
| Título, segundo renglón | 183 pt (interlineado exacto de 53 pt, `w:line="1060" w:lineRule="exact"`) |
| Firmantes | 235 pt |
| Primer metadato | 277 pt |
| Segundo metadato | 306 pt |
| Saludo | 357 pt |
| Primer párrafo del cuerpo | 379 pt |

El título nunca pasa de dos renglones. Si el nombre del servicio no cabe en dos a 42 pt
—unos 20 caracteres por renglón—, se acorta el título; **no se baja el tamaño**.

### Descendentes en el título

Con interlineado exacto de 53 pt, la cola de una **g, j, p, q o y** a 42 pt se sale de la
caja y aterriza sobre la línea de firmantes. El documento aprobado no lo sufre porque su
segundo renglón, «de Nómina Semanal», no lleva ninguna.

Medido sobre tinta real: el hueco entre el título y los firmantes es de **11.5 pt** en el
aprobado. Con una «y» en el último renglón queda en 3.8, que es la colisión. Se despejan
**274 tw** de espacio posterior, y solo cuando el último renglón lo necesita; con eso el
hueco vuelve a 11.5 exactos.

Todo lo que va debajo —firmantes, metadatos y saludo— baja esos 13.7 pt, y el verificador
espera ese desplazamiento cuando detecta un descendente. Ojo con la diferencia: **7.7 pt es
lo que se come la cola; 13.7 es el espacio que hay que añadir.** No son el mismo número.

Comparar posiciones de tinta entre títulos distintos engaña: «Cotización Maquila» tiene una
q que desciende y «de Nómina Semanal» una ó que sube sobre la altura de mayúsculas. Lo que
se compara es la línea base, y esas coinciden al punto.

## Interlineado y espacio entre párrafos

Medido renglón a renglón sobre el documento aprobado. **Interlineado exacto**, que es lo que
produce su archivo; el automático da otra cosa. Valores en twips (1 pt = 20).

| Bloque | Interlineado | Espacio antes | Espacio después |
|---|---|---|---|
| Cuerpo | `317` (15.85 pt) | 0 | `145` (7.25 pt) |
| Viñeta | `308` (15.40 pt) | 0 | `72` (3.60 pt) |
| Nota al pie de cuadro | `288` (14.40 pt) | 0 | `145` |
| Encabezado de sección | automático | `240` (12 pt) | `80` (4 pt) |
| Título de carátula | `1060` (53 pt) exacto | — | 0 |

Comprobación: entre renglones de un mismo párrafo tiene que salir 15.8–15.9 pt; entre
viñetas, 19.0; de párrafo a encabezado, 25.9; de encabezado a párrafo, 24.7. Si no cuadra,
el interlineado está en automático.

## Saltos de plana

1. **Ningún cuadro se parte.** `<w:cantSplit/>` en cada fila para que no se rompa un renglón,
   y `<w:keepNext/>` en todas las filas menos la última para que la tabla entre completa en
   una plana. La cabecera lleva ademas `<w:tblHeader/>`.
2. **Ningún encabezado se queda solo al pie.** `<w:keepNext/>` y `<w:keepLines/>` en el
   encabezado, de modo que arrastra consigo su párrafo de entrada y el arranque del cuadro.
3. **Ninguna plana por debajo del 85% de ocupación**, salvo la última. Si forzar un cuadro
   entero deja un hueco grande, no se mete un salto: se **acorta el contenido de las celdas**.
   Las celdas del documento aprobado son frases cortas, no párrafos.
4. **El bloque de contacto cabe en la última plana de contenido.** Reserva 2" exactas, así que
   el texto tiene que terminar 144 pt antes del límite inferior de la caja. Si no cabe, se
   recorta contenido; nunca se deja una plana con solo el bloque de contacto.

**Trampa de la plantilla:** su párrafo de anclaje trae `<w:spacing>` después de `<w:rPr>`
dentro de `<w:pPr>`, orden que el esquema OOXML no admite. Word lo tolera; otros motores
ignoran el alto exacto y mandan el bloque a una plana nueva. Al generar, se reordena.

## Metadatos: solo dos

El documento aprobado lleva **Cliente** y **Fecha**. Nada mas.

```
Cliente:    Comband DTH — Atención: Martin Ortiz
Fecha:      24 de agosto de 2026
```

La atención va dentro de la línea de Cliente, separada por raya. Si el proyecto exige folio
o vigencia, se enuncian en el cuerpo o en las condiciones comerciales, **no** como etiquetas
adicionales de carátula. Nueve etiquetas es lo que dirección rechazo.

## Margenes

Laterales **1440 tw (1 pulgada)**, que es lo que usa el documento aprobado. Superior e
inferior según `margenes-membrete.md`: 1584 y 2016 tw, encabezado 1138, pie 1512. Esos dos
últimos protegen el membrete impreso y no se tocan.

## Paleta real de los documentos

| Uso | Valor |
|---|---|
| Teal de títulos, etiquetas y encabezados | `#23656F` |
| Cuerpo | `#000000` |
| Nota al pie y aclaraciones | `#595959` |
| Texto sobre cabecera de cuadro | `#FFFFFF` |

`#23656F` es el teal que aparece en los entregables reales. La guía de marca registra
`#24606C`; la diferencia es mínima y **manda el documento aprobado**.

## Cuadros

Cabecera con fondo teal `#23656F` y texto blanco en negritas, centrado. Filas de fondo
blanco con filete teal fino. Las cifras de importe, centradas; la columna de resultado, en
negritas. Los cuadros son de **cifras**, no descriptivos: un cuadro que sustituye un
argumento por una retícula de frases no va.

## Viñetas

Guion simple `-`, texto en 11 pt negro, una o dos lineas por viñeta. Sin topo teal y sin
entradilla en negritas seguida de párrafo.

## Cierre

Párrafo de cortesía («Quedamos atentos a sus comentarios…») y, debajo, el **bloque de
contacto** de la hoja membretada: Director General y Directora Comercial. Nunca firma en
texto. Fluye tras el último párrafo, no se ancla al pie de la hoja.

## Verificación

Render a PDF y comparación visual **lado a lado** contra el documento de referencia:

1. La primera plana lleva título, firmantes, dos metadatos, saludo y ya contenido.
2. Ninguna plana con media hoja en blanco.
3. El total de planas está dentro del límite de `mlr-redaccion`.
4. Ningún encabezado de sección con filete.
5. Viñetas con guion, no con topo.
6. La última plana cierra con cortesía y bloque de contacto.

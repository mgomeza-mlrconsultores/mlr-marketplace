# Caratula y estructura del documento formal

Todo esto esta medido sobre el documento que direccion aprobo y envio a cliente:

**`G:\Unidades compartidas\MMLR 2025\Hoja Membretada\Cotizacion_Comband DTH_Maquila Nomina.pdf`**

Autora: C.P. Monica Arellano. Es el patron de la firma. Ante cualquier duda, se abre y se
copia. No se disena una caratula nueva ni se «mejora» la existente.

## No hay portada aparte

El error que direccion rechazo fue componer una portada dedicada —titulo grande, nueve
etiquetas de metadatos y media plana en blanco— y empezar el contenido en la plana 2. **Eso
no se hace.**

La caratula es un **bloque de cabecera en la parte alta de la primera plana**. Debajo, en la
misma plana, arranca el saludo y el contenido. Un documento de tres planas tiene tres planas
de contenido.

## Bloque de caratula, medidas exactas

Sobre hoja carta, con la plantilla `Hoja Membretada MLR - varias paginas.docx`:

| Elemento | Especificacion |
|---|---|
| Titulo | **42 pt**, teal `#23656F`, negritas, centrado. Una o dos lineas, nunca tres. |
| Firmantes | **16 pt**, teal `#23656F`, negritas, centrado, **en mayusculas**: `C.P. MONICA ARELLANO \| C.P. JUAN MARCOS LÓPEZ` |
| Etiqueta de metadato | **13 pt**, teal `#23656F`, negritas. Sangria de 260 tw desde el margen. |
| Valor de metadato | **13 pt**, negro, negritas. A 1480 tw desde el margen. |
| Saludo | **15 pt**, teal `#23656F`, negritas, alineado al margen izquierdo: `Estimado Sr. <Nombre>:` |
| Cuerpo | **11 pt**, negro, justificado |
| Encabezado de seccion | **13 pt**, teal `#23656F`, negritas, numerado `1. Titulo`. **Sin filete debajo.** |

## Ritmo vertical, medido en el documento aprobado

Posiciones del borde superior de cada bloque, en puntos desde el borde de la hoja. **Se
calibran renderizando a PDF y midiendo, no a ojo:** la diferencia entre 235 y 251 no se ve
en una captura, pero el documento entero queda desplazado.

| Bloque | Posicion |
|---|---|
| Titulo, primer renglon | 130 pt |
| Titulo, segundo renglon | 183 pt (interlineado exacto de 53 pt, `w:line="1060" w:lineRule="exact"`) |
| Firmantes | 235 pt |
| Primer metadato | 277 pt |
| Segundo metadato | 306 pt |
| Saludo | 357 pt |
| Primer parrafo del cuerpo | 379 pt |

El titulo nunca pasa de dos renglones. Si el nombre del servicio no cabe en dos a 42 pt
—unos 20 caracteres por renglon—, se acorta el titulo; **no se baja el tamano**.

## Interlineado y espacio entre parrafos

Medido renglon a renglon sobre el documento aprobado. **Interlineado exacto**, que es lo que
produce su archivo; el automatico da otra cosa. Valores en twips (1 pt = 20).

| Bloque | Interlineado | Espacio antes | Espacio despues |
|---|---|---|---|
| Cuerpo | `317` (15.85 pt) | 0 | `145` (7.25 pt) |
| Vineta | `308` (15.40 pt) | 0 | `72` (3.60 pt) |
| Nota al pie de cuadro | `288` (14.40 pt) | 0 | `145` |
| Encabezado de seccion | automatico | `240` (12 pt) | `80` (4 pt) |
| Titulo de caratula | `1060` (53 pt) exacto | — | 0 |

Comprobacion: entre renglones de un mismo parrafo tiene que salir 15.8–15.9 pt; entre
vinetas, 19.0; de parrafo a encabezado, 25.9; de encabezado a parrafo, 24.7. Si no cuadra,
el interlineado esta en automatico.

## Saltos de plana

1. **Ningun cuadro se parte.** `<w:cantSplit/>` en cada fila para que no se rompa un renglon,
   y `<w:keepNext/>` en todas las filas menos la ultima para que la tabla entre completa en
   una plana. La cabecera lleva ademas `<w:tblHeader/>`.
2. **Ningun encabezado se queda solo al pie.** `<w:keepNext/>` y `<w:keepLines/>` en el
   encabezado, de modo que arrastra consigo su parrafo de entrada y el arranque del cuadro.
3. **Ninguna plana por debajo del 85% de ocupacion**, salvo la ultima. Si forzar un cuadro
   entero deja un hueco grande, no se mete un salto: se **acorta el contenido de las celdas**.
   Las celdas del documento aprobado son frases cortas, no parrafos.
4. **El bloque de contacto cabe en la ultima plana de contenido.** Reserva 2" exactas, asi que
   el texto tiene que terminar 144 pt antes del limite inferior de la caja. Si no cabe, se
   recorta contenido; nunca se deja una plana con solo el bloque de contacto.

**Trampa de la plantilla:** su parrafo de anclaje trae `<w:spacing>` despues de `<w:rPr>`
dentro de `<w:pPr>`, orden que el esquema OOXML no admite. Word lo tolera; otros motores
ignoran el alto exacto y mandan el bloque a una plana nueva. Al generar, se reordena.

## Metadatos: solo dos

El documento aprobado lleva **Cliente** y **Fecha**. Nada mas.

```
Cliente:    Comband DTH — Atención: Martín Ortiz
Fecha:      24 de agosto de 2026
```

La atencion va dentro de la linea de Cliente, separada por raya. Si el proyecto exige folio
o vigencia, se enuncian en el cuerpo o en las condiciones comerciales, **no** como etiquetas
adicionales de caratula. Nueve etiquetas es lo que direccion rechazo.

## Margenes

Laterales **1440 tw (1 pulgada)**, que es lo que usa el documento aprobado. Superior e
inferior segun `margenes-membrete.md`: 1584 y 2016 tw, encabezado 1138, pie 1512. Esos dos
ultimos protegen el membrete impreso y no se tocan.

## Paleta real de los documentos

| Uso | Valor |
|---|---|
| Teal de titulos, etiquetas y encabezados | `#23656F` |
| Cuerpo | `#000000` |
| Nota al pie y aclaraciones | `#595959` |
| Texto sobre cabecera de cuadro | `#FFFFFF` |

`#23656F` es el teal que aparece en los entregables reales. La guia de marca registra
`#24606C`; la diferencia es minima y **manda el documento aprobado**.

## Cuadros

Cabecera con fondo teal `#23656F` y texto blanco en negritas, centrado. Filas de fondo
blanco con filete teal fino. Las cifras de importe, centradas; la columna de resultado, en
negritas. Los cuadros son de **cifras**, no descriptivos: un cuadro que sustituye un
argumento por una retícula de frases no va.

## Vinetas

Guion simple `-`, texto en 11 pt negro, una o dos lineas por vineta. Sin topo teal y sin
entradilla en negritas seguida de parrafo.

## Cierre

Parrafo de cortesia («Quedamos atentos a sus comentarios…») y, debajo, el **bloque de
contacto** de la hoja membretada: Director General y Directora Comercial. Nunca firma en
texto. Fluye tras el ultimo parrafo, no se ancla al pie de la hoja.

## Verificacion

Render a PDF y comparacion visual **lado a lado** contra el documento de referencia:

1. La primera plana lleva titulo, firmantes, dos metadatos, saludo y ya contenido.
2. Ninguna plana con media hoja en blanco.
3. El total de planas esta dentro del limite de `mlr-redaccion`.
4. Ningun encabezado de seccion con filete.
5. Vinetas con guion, no con topo.
6. La ultima plana cierra con cortesia y bloque de contacto.

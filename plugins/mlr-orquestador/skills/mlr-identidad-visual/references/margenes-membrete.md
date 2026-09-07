# Margenes del membrete — valores de produccion

Estos valores estan medidos de los entregables reales de MLR, no calculados. **Aplicarlos siempre al construir un documento formal sobre la plantilla.**

## Como esta hecho el membrete

No es un encabezado de franja: es una **imagen de pagina completa de 21.70 x 28.03 cm, anclada y colocada detras del texto**. Ocupa la hoja entera. El texto se escribe encima.

De ahi que los margenes no sean decorativos: son lo unico que impide que el texto invada la banda impresa del logotipo arriba y los datos de contacto abajo.

Hay dos variantes en el archivo, porque la primera pagina lleva membrete distinto al resto (`titlePg` activo): `header1.xml` para la portada y `header2.xml` para las paginas siguientes.

## El problema de la plantilla en crudo

La plantilla trae el encabezado desplazado 2.01 cm desde el borde. Como la imagen esta anclada a esa referencia, el grafico no queda a ras de pagina y aparece una banda vacia arriba y abajo. Es el exceso de espacio que Marcos senala.

## Valores corregidos, validados en produccion

Medidos de `Diagnostico de Inventario V_final.docx` (Reciservicios, 20260827), que es el documento de referencia de la firma:

| Propiedad | Plantilla en crudo | **Valor a aplicar** |
|---|---|---|
| Margen superior | 1584 tw · 2.79 cm | **3000 tw · 5.29 cm** |
| Margen inferior | 2016 tw · 3.56 cm | **2560 tw · 4.51 cm** |
| Margen izquierdo | 1238 tw · 2.18 cm | **1240 tw · 2.19 cm** |
| Margen derecho | 1238 tw · 2.18 cm | **1240 tw · 2.19 cm** |
| Encabezado desde el borde | 1138 tw · 2.01 cm | **0 tw · 0.00 cm** |
| Pie desde el borde | 1512 tw · 2.67 cm | **1901 tw · 3.35 cm** |
| Primera pagina distinta | si | **si**, se conserva |

El cambio decisivo es **el encabezado a 0**: pone la imagen del membrete a ras de la hoja y elimina la banda vacia. Los margenes superior e inferior mayores no son desperdicio, son lo que despeja la zona impresa del membrete para que el texto no se encime.

La plantilla de una sola pagina viene con margenes muy superiores (4.44 cm arriba y 7.37 cm abajo). Corregirla a los mismos valores de la tabla.

## Aplicacion

En el XML del documento, dentro del ultimo `<w:sectPr>`:

```xml
<w:pgMar w:top="3000" w:right="1240" w:bottom="2560" w:left="1240"
         w:header="0" w:footer="1901" w:gutter="0"/>
```

Las unidades son twips: 1 cm = 567 twips, 1 pulgada = 1440 twips.

Si se edita desde Word en lugar del XML: Diseno de pagina, Margenes personalizados, pestana Margenes para superior, inferior, izquierdo y derecho; y pestana Diseno para las distancias de encabezado y pie desde el borde.

## Pie de pagina

El pie lleva unicamente la numeracion de pagina. Sin texto adicional: los datos de contacto ya vienen impresos en la imagen del membrete y repetirlos duplica la informacion.

## Verificacion obligatoria

Renderizar el documento a PDF y comprobar en la primera pagina y en una intermedia:

1. Que la imagen del membrete llega al borde de la hoja, sin banda blanca arriba.
2. Que ninguna linea de texto se encima con el logotipo ni con los datos de contacto impresos.
3. Que no hay encabezados de seccion colgados al final de pagina. Si un salto deja una pagina con menos de 22 lineas, mover el salto al subtitulo anterior.
4. Que la numeracion aparece y es correlativa.

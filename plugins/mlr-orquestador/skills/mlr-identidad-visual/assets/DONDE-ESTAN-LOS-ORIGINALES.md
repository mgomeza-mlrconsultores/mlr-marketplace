# Originales que NO viven en este repositorio

Este marketplace es público. La cotización aprobada por dirección lleva precios y
datos de contacto de un cliente, y las hojas membretadas son material de marca.
Ninguna de las dos se sube aquí.

## Documento de referencia del formato y la redacción

`G:\Unidades compartidas\MMLR 2025\Hoja Membretada\Cotizacion_Comband DTH_Maquila Nomina.pdf`

Autora: C.P. Mónica Arellano. Es el patrón de la firma: carátula, tipografía,
interlineado, cuadros, saltos y registro de redacción salen de ahí. Ante cualquier
duda se abre y se copia.

## Molde del formato de solicitud de información

`G:\Unidades compartidas\MMLR 2025\Hoja Membretada\Formato_Cotizacion_MLR.docx`

La carta con la que se le piden datos al cliente antes de cotizar. `formato_cotizacion.py`
—en `mlr-cotizacion`— clona ese paquete y solo cambia el texto. Trae el membrete de plana
completa dentro del encabezado, así que tampoco se sube.

## Hojas membretadas calibradas

- `C:\Users\mgome\Claude\Projects\MLR Odoo\Plantillas\`
- `G:\Unidades compartidas\MMLR 2025\Hoja Membretada\`

`Hoja Membretada MLR - varias paginas.docx` para informes, anexos y propuestas.
`Hoja Membretada MLR - 1 pagina.docx` para cartas y notas de una plana.

`documento_mlr.py` las busca en esas rutas por su cuenta. Si se trabaja en otra
maquina, se copia la que toque a `assets/plantillas/` **sin subirla al repositorio**
(esa carpeta está en .gitignore).

## Fuentes

`assets/fuentes/` si trae las tres familias de Lexend: son de licencia abierta (OFL)
y sin ellas no se puede incrustar, que es lo que hace que el documento se vea igual
en una maquina sin Lexend instalada.

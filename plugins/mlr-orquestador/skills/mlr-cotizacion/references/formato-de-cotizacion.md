# Formato de solicitud de informacion para cotizar

El documento que se le manda al cliente **antes** de cotizar, para pedirle los datos que
mueven el precio. No es la propuesta: la propuesta va despues, con el formato de
`references/entregables.md`.

## El molde

**`G:\Unidades compartidas\MMLR 2025\Hoja Membretada\Formato_Cotizacion_MLR.docx`**

Es el archivo que direccion aprueba. No se rehace la maqueta ni se reconstruye el
membrete: `scripts/formato_cotizacion.py` **clona el paquete** y reemplaza unicamente
`word/document.xml`. Estilos, encabezado de plana completa, margenes y bloque de contacto
quedan identicos por construccion.

Consecuencia practica: este documento **no** usa el constructor de `mlr-identidad-visual`
—nada de caratula, firmantes, Lexend incrustado ni verificador de ritmo vertical—. Son dos
formatos distintos y los dos estan aprobados. La propuesta usa el de identidad visual; esta
carta usa su propio molde.

## Lo que fija el molde

| Elemento | Como es |
|---|---|
| Cuerpo | Calibri 11, color `344447`, interlineado 259 automatico |
| Titulo | Estilo `Ttulo`, 21 pt, negro, `Informacion para cotizar nuestros servicios` |
| Bajada | Versalitas 9 pt, negrita, teal `24646C` |
| Encabezado de bloque | Negrita, teal `24646C`, `01` + tres espacios + nombre |
| Punto | Vineta `•` mas dos espacios en teal, texto en color de cuerpo, sangria 245 colgante |
| Cierre | Centrado, negrita, teal: `Quedamos pendientes de sus comentarios.` |
| Plana | Carta, margenes 2635 / 1440 / 4032 / 1440 twips |

El teal de este formato es `24646C`, no el `23656F` de la propuesta. Se respeta el del
molde.

## Redaccion

Los puntos son **frases nominales, no preguntas**: «Numero de facturas de venta mensuales.»,
no «¿Cuantas facturas emiten al mes?». Una linea, punto final, sin parentesis explicativos.

El cuestionario interno de la reunion —`scripts/preguntas.py`— si esta en preguntas, porque
se lee en voz alta. Cuando ese contenido pasa a este formato, se convierte a frase nominal.

## Orden de los bloques

Fijado por direccion, por logica y por peso en el precio:

1. Ficha del sistema
2. Contabilidad y cumplimiento fiscal
3. Nomina y viaticos
4. Seguimiento comercial
5. Ventas
6. Suscripciones y contratos recurrentes
7. Punto de venta
8. Compras
9. Inventario y almacen
10. Fabricacion y listas de materiales
11. Proyectos
12. Servicio de campo
13. Mantenimiento
14. Datos, calendario y alcance

Lo contable manda y va arriba, con nomina pegada. Despues la cadena comercial —comercial,
ventas, recurrente, mostrador—, luego la cadena de abasto, luego los bloques de servicio, y
al final el cierre de datos y calendario. Los bloques que no apliquen al cliente se borran
del modulo de contenido antes de generar; no se dejan vacios ni marcados como opcionales.

## Salto de plana

Cada bloque se mantiene entero. El script encadena `keepNext` desde el encabezado hasta el
penultimo punto, con `keepLines` en todos: un bloque que no cabe arranca completo en la
plana siguiente. Nunca se parte un bloque ni se deja un encabezado solo al pie.

Si un bloque llegara a ser mas alto que la caja de texto util —9 173 twips, unas 26 lineas—
no cabria entero y Word lo partiria igual. Antes de llegar ahi se divide en dos bloques con
nombre propio.

## Verificacion antes de entregar

1. Abrir el paquete y validar que `word/document.xml` es XML bien formado.
2. Exportar a PDF y contar planas: cada una tiene que arrancar con un encabezado de bloque
   o continuar uno que empezo arriba.
3. Renderizar la plana 1 y mirarla contra el molde. Titulo, bajada, saludo y primer bloque
   caen en la misma coordenada vertical: 131.8, 162.4, 183.3 y 254.3 puntos.
4. Comprobar que el membrete aparece en todas las planas y que ningun texto invade el
   bloque de contacto.

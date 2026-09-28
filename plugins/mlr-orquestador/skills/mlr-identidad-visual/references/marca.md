# Marca MLR Consultores — valores oficiales

Fuente: *Manual de Identidad Corporativa* y `Guia_de_Marca_MLR.md`, con decisiones de marca cerradas el 2026-06-14. Estos son los valores reales, no aproximaciones.

Razón social completa: **MM&LR Consultores Fiscales**, de uso corriente **MLR Consultores**.
Mensaje central: **«Contadores que sí le entienden a Odoo.»**

## Paleta

**Primarios**

| Color | HEX | Pantone | Uso |
|---|---|---|---|
| Teal / petroleo | `#24606C` | 7715 C | Dominante: titulares, formas, bloques |
| Café institucional | `#452E27` | 4625 C | Acento y palabra destacada |

**Secundario**

| Color | HEX | Uso |
|---|---|---|
| Azul claro | `#E6F3FB` | Fondos limpios |

**Neutros y extensiones digitales**

| Color | HEX | Uso |
|---|---|---|
| Blanco | `#FFFFFF` | Texto sobre teal o café; fondos |
| Gris carbón | `#2B2B2B` | Cuerpo de texto sobre fondo claro |
| Teal oscuro | `#18454E` | Profundidad, hover, degradados |
| Teal medio | `#6FA3AB` | Gráficos, lineas, detalles |

**Reglas de color.** Teal dominante. Café solo como acento o palabra destacada, nunca como fondo extenso. Azul claro para fondos. Texto blanco sobre teal y café; gris carbón o teal sobre fondo claro. **Solo colores institucionales: no recolorear fuera de la gama.**

## Tipografía

| Rol | Fuente del manual | Sustituto digital |
|---|---|---|
| Titulares y logotipo | DIN Alternate Bold | Oswald Bold |
| Texto y papelería | Gill Sans | Inter Regular |

Jerarquía: titular en Bold y mayúsculas, en teal, con la palabra clave en café. Subtitulo en Medium. Cuerpo en Regular.

### Documentos formales: Lexend 11

**Decisión de dirección del 2026-09-09, de aplicación obligatoria.** Todo informe, diagnóstico, propuesta, convenio y anexo en hoja de cálculo se compone en **Lexend a 11 puntos** para el cuerpo del texto. No es una preferencia estética: Lexend está diseñada para reducir el esfuerzo de lectura, y estos documentos los leen directivos y contadores de un tirón.

Aplica al cuerpo, a las viñetas, a los pies de tabla y a las celdas del anexo. Los títulos de sección conservan su jerarquía de tamaño y su teal, pero también en Lexend. Oswald se reserva para presentaciones, piezas web y material de marketing; no aparece en documentos formales.

En el archivo de Word esto se fija en `docDefaults` de `styles.xml`, no run por run: `rFonts` con `ascii`, `hAnsi` y `cs` en `Lexend`, y `sz` en 22 medios puntos. Fijarlo solo en algunos párrafos deja el resto heredando la fuente del tema y el documento sale mezclado.

**Pesos, extraídos de las fuentes incrustadas en el documento aprobado.** El peso se expresa con el **nombre de familia**, no con `<w:b/>`: Word trata cada peso de Lexend como familia propia, y usar ademas la negrita del procesador lo engorda de mas.

| Elemento | Familia | Tamaño | Color |
|---|---|---|---|
| Título de carátula | `Lexend ExtraBold` | 42 pt (`sz 84`) | `#23656F` |
| Firmantes | `Lexend SemiBold` | 16 pt (`sz 32`) | `#23656F` |
| Saludo | `Lexend ExtraBold` | 15 pt (`sz 30`) | `#23656F` |
| Encabezado de sección | `Lexend ExtraBold` | 13 pt (`sz 26`) | `#23656F` |
| Etiqueta de metadato | `Lexend SemiBold` | 13 pt (`sz 26`) | `#23656F` |
| Valor de metadato | `Lexend SemiBold` | 13 pt (`sz 26`) | `#000000` |
| Cuerpo y viñetas | `Lexend` | 11 pt (`sz 22`) | `#000000` |
| Cabecera de cuadro | `Lexend ExtraBold` | 10.5 pt (`sz 21`) | `#FFFFFF` sobre `#23656F` |
| Celda de cuadro | `Lexend` | 11 pt (`sz 22`) | `#000000` |
| Cifra de resultado | `Lexend ExtraBold` | 11 pt (`sz 22`) | `#000000` |
| Nota al pie de cuadro | `Lexend` | 10 pt (`sz 20`) | `#595959` |

### Las fuentes se incrustan en el archivo. Sin excepción.

**Lexend no está instalada en las maquinas de MLR.** El documento aprobado se ve bien en
cualquier equipo porque **incrusta sus fuentes**: Word las guarda como partes
`word/fonts/*.odttf`. Un `.docx` que solo declara `Lexend` sin incrustarla se abre con la
fuente del tema —Cambria, serif— y no se parece en nada al modelo. Fue el defecto reportado
el 2026-09-09.

Lo que hay que añadir al paquete:

1. Las tres familias como partes `word/fonts/*.odttf`, ofuscadas según ECMA-376 17.8.1: se
   toman los 16 bytes del `fontKey` **en orden inverso** y se aplican por XOR sobre los
   primeros 32 bytes del `.ttf`. La operación es involutiva, así que sirve para ofuscar y
   para comprobar.
2. En `word/fontTable.xml`, una entrada por familia:
   `<w:font w:name="Lexend ExtraBold"><w:embedRegular r:id="..." w:fontKey="{GUID}"/></w:font>`
3. La relación correspondiente en `word/_rels/fontTable.xml.rels`, de tipo `.../font`.
4. `<w:embedTrueTypeFonts/>` en `word/settings.xml`, y **sin** `<w:saveSubsetFonts/>`, para
   que viaje la fuente completa y no solo los glifos usados.
5. **Un `<Override PartName="/word/fonts/<archivo>.odttf">` por cada fuente añadida**, en
   `[Content_Types].xml`, con `ContentType="application/vnd.openxmlformats-officedocument.obfuscatedFont"`.

**Aquí esta la trampa, y costo un entregable dañado el 2026-09-09.** `odttf` **no** va como
`<Default Extension>`: la plantilla declara un `Override` por archivo, uno para Calibri y
otro para Cambria. Añadir las tres fuentes sin declararlas deja tres partes del paquete sin
tipo de contenido, y una sola parte sin declarar invalida el paquete entero. Word lo abre
como «contenido no legible» y **no dice cual es la parte**. Se diagnóstico abriendo nueve
variantes con Word por automatización hasta aislarlo.

`verifica_documento.py` lo comprueba ahora: toda parte del paquete tiene que tener tipo de
contenido, por `Default` o por `Override`, y toda relación tiene que apuntar a una parte que
exista.

**Comprobación obligatoria:** desofuscar cada parte con su propio `fontKey` y verificar que
el nombre de familia del `.ttf` recuperado coincide con el declarado. Si no coincide, Word
ignora la incrustación en silencio.

Para que el render de control sea fiel, las tres familias también tienen que estar instaladas
en la maquina que exporta el PDF. Si faltan, se instancian del archivo variable de Lexend en
los pesos 400, 600 y 800 y se registran con esos nombres exactos. Sin eso el render miente y
la revisión visual no vale nada.

**Discrepancia registrada.** La guía de marca propone Barlow o Saira para titulares y Lato o Mulish para cuerpo. Los entregables reales de la firma usan Oswald e Inter. Se adopta Oswald e Inter por ser el estándar en producción; Oswald reproduce mejor la geometría condensada de DIN Alternate. **Confirmar con Marcos si prefiere alinear a la guía escrita.**

## Logotipo

**Composición.** Isotipo cuadrado con monograma MLR de trazos verticales tipo columnas, que evoca estructura, solidez y orden. Acompañado del texto CONSULTORES y la bajada CONSULTORÍA FISCAL ESPECIALIZADA.

**Archivos aprobados**, en `Projects\Marketing y Manejo de Publicaciones de Redes Sociales MM&LR Consultores\00_marca\logos\`:

| Archivo | Uso |
|---|---|
| `logo_MLR_color_vertical.png` | Logotipo completo a color, fondo transparente. Uso general sobre fondos claros |
| `isotipo_MLR_teal.png` | Solo isotipo. Avatares, favicons, sellos |
| `isotipo_MLR_blanco.png` | Isotipo blanco. Fondos oscuros, teal o café |

Para piezas HTML existe una versión del logotipo en SVG vectorial; ver `../../mlr-presentaciones/references/logo-svg.md`.

**Reglas del manual.** Tamaño mínimo: logotipo completo 1.8 cm, isotipo solo 0.5 cm. Área de aislamiento equivalente al tamaño de una pieza del isotipo; no invadir ese aire. No recrear el logotipo, no deformarlo, no sustituir el nombre de la firma por el símbolo dentro de un texto corrido.

## Membrete y datos de contacto aprobados

Pie de toda pieza formal:

- Teléfonos: 55 6302 8143 / 55 8772 9395
- Correos: direccionjm@mlrconsultores.com / m.arellano@mlrconsultores.com
- Web: https://mlrconsultores.com
- Dirección: Av. Presidente Plutarco Elias Calles 957, Int. 1, Col. Iztaccihuatl, C.P. 03520, Benito Juarez, Ciudad de México (la de Calle Eugenia ya no es vigente)

**Plantillas de Word.** Unidad compartida de la empresa en Google Drive, carpeta `MLR > Hoja Membretada`, identificador `15QKXzczjEMo1XYv8Hb-aWBH8k-tyC5De`:

| Archivo | Identificador | Cuando se usa |
|---|---|---|
| `Hoja Membretada MLR - varias paginas.docx` | `1hn1L7Q2VAM0KAZTm2HOI6ZD-4ou72v9H` | Informes, diagnósticos y propuestas. **Uso habitual** |
| `Hoja Membretada MLR - 1 pagina.docx` | `1zN82MOBbW46yEllnYi891JExd8AGT_uO` | Cartas, notas, constancias |
| `Hoja Membretada MLR.docx` | `1lHgYXNL7ZtXxb7r-v_f07pmaWrX0fvFC` | Versión base |

**No preguntar donde esta el membrete.** Estos identificadores son la respuesta. Todo documento formal se construye descargando la plantilla y escribiendo dentro, nunca recreando el encabezado.

**Copia local de las plantillas:** `<carpeta local de proyectos MLR>\Plantillas\`.

**Margenes.** La plantilla en crudo deja demasiado espacio arriba y abajo. Los valores corregidos, validados en producción, están en `margenes-membrete.md` y son de aplicación obligatoria en todo documento formal.

## Estilo visual de la firma

- Fondos en azul claro o blanco; bloques teal sólidos.
- Círculos y formas orgánicas teal como decoración y para enmarcar fotografía.
- Fotografía de profesionales reales y capturas de tableros de Odoo. No banco de imágenes genéricas.
- Titulares que resaltan la palabra clave en color.
- Recurso narrativo de comparación antes y después.
- El símbolo de Contabilidad de Odoo aparece como sello recurrente. Usar el icono oficial de Odoo, nunca recrearlo.

## Tono de voz

Autoridad técnica con cercanía. Claro y directo, tratando de «tu» en piezas de marketing y en registro directivo en entregables de cliente. Orientado al beneficio del negocio. Español de México.

Evitar: tecnicismos sin explicar, promesas vagas o exageradas, tono frio o robotico, y hablar solo de la firma en lugar del problema del cliente.

Frases de marca en uso: «Contadores que sí le entienden a Odoo», «Tu contabilidad en tiempo real», «Del caos a la claridad», «No segmentes tu negocio: ten toda tu operación en un solo lugar».

## Formatos de pieza social

Post cuadrado 1080x1080. Vertical 1080x1350. Reel o historia 1080x1920.

# Marca MLR Consultores — valores oficiales

Fuente: *Manual de Identidad Corporativa* y `Guia_de_Marca_MLR.md`, con decisiones de marca cerradas el 2026-06-14. Estos son los valores reales, no aproximaciones.

Razon social completa: **MM&LR Consultores Fiscales**, de uso corriente **MLR Consultores**.
Mensaje central: **«Contadores que sí le entienden a Odoo.»**

## Paleta

**Primarios**

| Color | HEX | Pantone | Uso |
|---|---|---|---|
| Teal / petroleo | `#24606C` | 7715 C | Dominante: titulares, formas, bloques |
| Cafe institucional | `#452E27` | 4625 C | Acento y palabra destacada |

**Secundario**

| Color | HEX | Uso |
|---|---|---|
| Azul claro | `#E6F3FB` | Fondos limpios |

**Neutros y extensiones digitales**

| Color | HEX | Uso |
|---|---|---|
| Blanco | `#FFFFFF` | Texto sobre teal o cafe; fondos |
| Gris carbon | `#2B2B2B` | Cuerpo de texto sobre fondo claro |
| Teal oscuro | `#18454E` | Profundidad, hover, degradados |
| Teal medio | `#6FA3AB` | Graficos, lineas, detalles |

**Reglas de color.** Teal dominante. Cafe solo como acento o palabra destacada, nunca como fondo extenso. Azul claro para fondos. Texto blanco sobre teal y cafe; gris carbon o teal sobre fondo claro. **Solo colores institucionales: no recolorear fuera de la gama.**

## Tipografia

| Rol | Fuente del manual | Sustituto digital |
|---|---|---|
| Titulares y logotipo | DIN Alternate Bold | Oswald Bold |
| Texto y papeleria | Gill Sans | Inter Regular |

Jerarquia: titular en Bold y mayusculas, en teal, con la palabra clave en cafe. Subtitulo en Medium. Cuerpo en Regular.

### Documentos formales: Lexend 11

**Decision de direccion del 2026-09-09, de aplicacion obligatoria.** Todo informe, diagnostico, propuesta, convenio y anexo en hoja de calculo se compone en **Lexend a 11 puntos** para el cuerpo del texto. No es una preferencia estetica: Lexend esta disenada para reducir el esfuerzo de lectura, y estos documentos los leen directivos y contadores de un tiron.

Aplica al cuerpo, a las vinetas, a los pies de tabla y a las celdas del anexo. Los titulos de seccion conservan su jerarquia de tamano y su teal, pero tambien en Lexend. Oswald se reserva para presentaciones, piezas web y material de marketing; no aparece en documentos formales.

En el archivo de Word esto se fija en `docDefaults` de `styles.xml`, no run por run: `rFonts` con `ascii`, `hAnsi` y `cs` en `Lexend`, y `sz` en 22 medios puntos. Fijarlo solo en algunos parrafos deja el resto heredando la fuente del tema y el documento sale mezclado.

**Pesos, extraidos de las fuentes incrustadas en el documento aprobado.** El peso se expresa con el **nombre de familia**, no con `<w:b/>`: Word trata cada peso de Lexend como familia propia, y usar ademas la negrita del procesador lo engorda de mas.

| Elemento | Familia | Tamano | Color |
|---|---|---|---|
| Titulo de caratula | `Lexend ExtraBold` | 42 pt (`sz 84`) | `#23656F` |
| Firmantes | `Lexend SemiBold` | 16 pt (`sz 32`) | `#23656F` |
| Saludo | `Lexend ExtraBold` | 15 pt (`sz 30`) | `#23656F` |
| Encabezado de seccion | `Lexend ExtraBold` | 13 pt (`sz 26`) | `#23656F` |
| Etiqueta de metadato | `Lexend SemiBold` | 13 pt (`sz 26`) | `#23656F` |
| Valor de metadato | `Lexend SemiBold` | 13 pt (`sz 26`) | `#000000` |
| Cuerpo y vinetas | `Lexend` | 11 pt (`sz 22`) | `#000000` |
| Cabecera de cuadro | `Lexend ExtraBold` | 10.5 pt (`sz 21`) | `#FFFFFF` sobre `#23656F` |
| Celda de cuadro | `Lexend` | 11 pt (`sz 22`) | `#000000` |
| Cifra de resultado | `Lexend ExtraBold` | 11 pt (`sz 22`) | `#000000` |
| Nota al pie de cuadro | `Lexend` | 10 pt (`sz 20`) | `#595959` |

### Las fuentes se incrustan en el archivo. Sin excepcion.

**Lexend no esta instalada en las maquinas de MLR.** El documento aprobado se ve bien en
cualquier equipo porque **incrusta sus fuentes**: Word las guarda como partes
`word/fonts/*.odttf`. Un `.docx` que solo declara `Lexend` sin incrustarla se abre con la
fuente del tema —Cambria, serif— y no se parece en nada al modelo. Fue el defecto reportado
el 2026-09-09.

Lo que hay que anadir al paquete:

1. Las tres familias como partes `word/fonts/*.odttf`, ofuscadas segun ECMA-376 17.8.1: se
   toman los 16 bytes del `fontKey` **en orden inverso** y se aplican por XOR sobre los
   primeros 32 bytes del `.ttf`. La operacion es involutiva, asi que sirve para ofuscar y
   para comprobar.
2. En `word/fontTable.xml`, una entrada por familia:
   `<w:font w:name="Lexend ExtraBold"><w:embedRegular r:id="..." w:fontKey="{GUID}"/></w:font>`
3. La relacion correspondiente en `word/_rels/fontTable.xml.rels`, de tipo `.../font`.
4. `<w:embedTrueTypeFonts/>` en `word/settings.xml`, y **sin** `<w:saveSubsetFonts/>`, para
   que viaje la fuente completa y no solo los glifos usados.
5. El `Default` de extension `odttf` en `[Content_Types].xml` —la plantilla ya lo trae,
   porque incrusta Calibri y Cambria.

**Comprobacion obligatoria:** desofuscar cada parte con su propio `fontKey` y verificar que
el nombre de familia del `.ttf` recuperado coincide con el declarado. Si no coincide, Word
ignora la incrustacion en silencio.

Para que el render de control sea fiel, las tres familias tambien tienen que estar instaladas
en la maquina que exporta el PDF. Si faltan, se instancian del archivo variable de Lexend en
los pesos 400, 600 y 800 y se registran con esos nombres exactos. Sin eso el render miente y
la revision visual no vale nada.

**Discrepancia registrada.** La guia de marca propone Barlow o Saira para titulares y Lato o Mulish para cuerpo. Los entregables reales de la firma usan Oswald e Inter. Se adopta Oswald e Inter por ser el estandar en produccion; Oswald reproduce mejor la geometria condensada de DIN Alternate. **Confirmar con Marcos si prefiere alinear a la guia escrita.**

## Logotipo

**Composicion.** Isotipo cuadrado con monograma MLR de trazos verticales tipo columnas, que evoca estructura, solidez y orden. Acompanado del texto CONSULTORES y la bajada CONSULTORÍA FISCAL ESPECIALIZADA.

**Archivos aprobados**, en `Projects\Marketing y Manejo de Publicaciones de Redes Sociales MM&LR Consultores\00_marca\logos\`:

| Archivo | Uso |
|---|---|
| `logo_MLR_color_vertical.png` | Logotipo completo a color, fondo transparente. Uso general sobre fondos claros |
| `isotipo_MLR_teal.png` | Solo isotipo. Avatares, favicons, sellos |
| `isotipo_MLR_blanco.png` | Isotipo blanco. Fondos oscuros, teal o cafe |

Para piezas HTML existe una version del logotipo en SVG vectorial; ver `../../mlr-presentaciones/references/logo-svg.md`.

**Reglas del manual.** Tamano minimo: logotipo completo 1.8 cm, isotipo solo 0.5 cm. Area de aislamiento equivalente al tamano de una pieza del isotipo; no invadir ese aire. No recrear el logotipo, no deformarlo, no sustituir el nombre de la firma por el simbolo dentro de un texto corrido.

## Membrete y datos de contacto aprobados

Pie de toda pieza formal:

- Telefonos: 55 6302 8143 / 55 8772 9395
- Correos: direccionjm@mlrconsultores.com / m.arellano@mlrconsultores.com
- Web: https://mlrconsultores.com
- Direccion: Calle Eugenia #830, Col. Del Valle, C.P. 03100, Ciudad de Mexico

**Plantillas de Word.** Unidad compartida de la empresa en Google Drive, carpeta `MLR > Hoja Membretada`, identificador `15QKXzczjEMo1XYv8Hb-aWBH8k-tyC5De`:

| Archivo | Identificador | Cuando se usa |
|---|---|---|
| `Hoja Membretada MLR - varias paginas.docx` | `1hn1L7Q2VAM0KAZTm2HOI6ZD-4ou72v9H` | Informes, diagnosticos y propuestas. **Uso habitual** |
| `Hoja Membretada MLR - 1 pagina.docx` | `1zN82MOBbW46yEllnYi891JExd8AGT_uO` | Cartas, notas, constancias |
| `Hoja Membretada MLR.docx` | `1lHgYXNL7ZtXxb7r-v_f07pmaWrX0fvFC` | Version base |

**No preguntar donde esta el membrete.** Estos identificadores son la respuesta. Todo documento formal se construye descargando la plantilla y escribiendo dentro, nunca recreando el encabezado.

**Copia local de las plantillas:** `<carpeta local de proyectos MLR>\Plantillas\`.

**Margenes.** La plantilla en crudo deja demasiado espacio arriba y abajo. Los valores corregidos, validados en produccion, estan en `margenes-membrete.md` y son de aplicacion obligatoria en todo documento formal.

## Estilo visual de la firma

- Fondos en azul claro o blanco; bloques teal solidos.
- Circulos y formas organicas teal como decoracion y para enmarcar fotografia.
- Fotografia de profesionales reales y capturas de tableros de Odoo. No banco de imagenes genericas.
- Titulares que resaltan la palabra clave en color.
- Recurso narrativo de comparacion antes y despues.
- El simbolo de Contabilidad de Odoo aparece como sello recurrente. Usar el icono oficial de Odoo, nunca recrearlo.

## Tono de voz

Autoridad tecnica con cercania. Claro y directo, tratando de «tu» en piezas de marketing y en registro directivo en entregables de cliente. Orientado al beneficio del negocio. Espanol de Mexico.

Evitar: tecnicismos sin explicar, promesas vagas o exageradas, tono frio o robotico, y hablar solo de la firma en lugar del problema del cliente.

Frases de marca en uso: «Contadores que sí le entienden a Odoo», «Tu contabilidad en tiempo real», «Del caos a la claridad», «No segmentes tu negocio: ten toda tu operacion en un solo lugar».

## Formatos de pieza social

Post cuadrado 1080x1080. Vertical 1080x1350. Reel o historia 1080x1920.

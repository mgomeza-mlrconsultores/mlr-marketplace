---
name: mlr-identidad-visual
description: Estándar visual de MLR Consultores para documentos, presentaciones, páginas web, artifacts, tableros y gráficas. Define membrete, paleta, tipografía, profundidad y jerarquía, y elimina los rasgos que delatan diseño generado por IA. Cargar antes de decidir un solo color o una sola tipografía.
---

# Identidad visual MLR

El criterio de aceptación es que la pieza parezca hecha por un estudio de diseño, no por un asistente.

## 1. Marca

Los valores oficiales están en `references/marca.md`: paleta, tipografía, reglas de logotipo, datos de membrete y estilo de la firma. **No preguntar por ellos ni inventarlos.**

Lo esencial, para no tener que abrir el archivo en cada pieza:

- **Teal `#24606C`** dominante. **Café `#452E27`** solo como acento o palabra destacada. **Azul claro `#E6F3FB`** para fondos.
- **Documentos formales: Lexend 11** en todo el cuerpo, obligatorio. Se fija en `docDefaults` de `styles.xml`, nunca run por run.
- Fuera de documentos formales: titulares en **Oswald Bold**, cuerpo en **Inter Regular**.
- Texto blanco sobre teal o café; gris carbón `#2B2B2B` o teal sobre fondo claro.
- Solo colores institucionales. No recolorear fuera de la gama.

## 0. Documentos formales: no se escribe OOXML a mano

Un entregable formal de MLR se construye con **`scripts/documento_mlr.py`** y no se entrega
sin que **`scripts/verifica_documento.py`** pase en verde. Las dos cosas son obligatorias.

```python
import sys; sys.path.insert(0, "<ruta a la skill>/scripts")
from documento_mlr import Documento

d = Documento(titulo=["Cotización", "Proyecto Odoo"],
              cliente="Grupo Haus — Atención: Sr. Luis Ponce de León",
              fecha="8 de septiembre de 2026",
              saludo="Estimado Sr. Luis Ponce de León:")
d.parrafo("Por medio de la presente, MLR Consultores presenta a ...")
d.seccion("1. Alcance del servicio propuesto")
d.vinetas([...])
d.cuadro(["Hito", "Se libera contra", "Importe"], filas, [700, 4600, 1760])
d.subtitulo("3.1 Registrar la orden")                    # guias y manuales
d.imagen("capturas/01.jpg", "Orden S07976 marcada como venta sin factura.")
d.cierre()
d.guarda("ruta/Documento.docx")
```

El módulo trae ya medidos, del documento aprobado por dirección, la carátula, los tres pesos
de Lexend, el interlineado exacto, los espacios entre bloques, los cuadros que no se parten,
la incrustación de fuentes y el cierre con el bloque de contacto. **Cambiar esos valores a
ojo rompe la equivalencia con el archivo que el cliente aprueba.**

`imagen()` aplica el estándar aprobado de capturas (en línea, centrada, keepNext con su pie,
contorno 0.5 pt #BFD4DA, pie "Figura N." Lexend 9 pt #595959) y fija el tamaño desde la imagen:
hasta 6.3 in de ancho sin pasar de px/150 y hasta 4.4 in de alto, para que quepan dos figuras
por plana. El metadato `cliente` cabe en un renglón; si salta, la carátula baja 20 pt y el
verificador la rechaza. La guía funcional completa, con capturas y versión HTML, está en
`mlr-informe-funcional`.

Después de exportar a PDF:

```
python3 scripts/verifica_documento.py "Documento.pdf" --docx "Documento.docx"
```

Comprueba las seis posiciones de la carátula contra las medidas de referencia, el
interlineado por mediana, la ocupación de cada plana, los encabezados colgados, que el
bloque de contacto quepa, la incrustación de las tres familias —desofuscando cada parte y
verificando el nombre recuperado—, los margenes y las construcciones de redacción
prohibidas. **Sus umbrales están calibrados para que el documento aprobado pase limpio: si
alguna vez ese archivo falla, el umbral está mal, no el archivo.** Un fallo no se justifica
en el chat, se corrige.

`assets/fuentes/` trae las tres familias de Lexend. El documento de referencia y las hojas
membretadas no están en este repositorio, que es público: sus rutas están en
`assets/DONDE-ESTAN-LOS-ORIGINALES.md`.

**Documentos formales.** Se construyen sobre la plantilla de Word del membrete, descargándola de la unidad compartida y escribiendo dentro. Nunca recreando el encabezado. Identificadores en `references/marca.md`.

**Tipografía de documentos formales.** Lexend a 11 puntos en el cuerpo, sin excepción, fijada en `docDefaults`. Los títulos conservan su jerarquía de tamaño y su teal, también en Lexend. Oswald no aparece en documentos formales.

**Margenes del membrete.** No se estiman ni se copian de un entregable anterior: ya vienen calibrados en las plantillas oficiales de `Plantillas\`. Se abre **Hoja Membretada MLR - varias paginas.docx** (o la de 1 página), se vacía el cuerpo conservando la sección final, los encabezados y el párrafo que ancla el bloque de contacto, y se escribe dentro. Multipagina: `w:top="1584" w:bottom="2016" w:left/right="1238" w:header="1138" w:footer="1512"`. Detalle en `references/margenes-membrete.md`.

**Carátula.** **No existe portada aparte.** La carátula es un bloque de cabecera en la parte alta de la primera plana —título a 42 pt teal, firmantes en mayúsculas a 16 pt, y solo dos metadatos: Cliente y Fecha— y debajo, en esa misma plana, arranca el saludo y el contenido. Componer una portada dedicada con media plana en blanco es lo que dirección rechazo. Medidas exactas, paleta y cuadros en `references/caratula-y-estructura.md`, tomadas del documento aprobado `Cotizacion_Comband DTH_Maquila Nomina.pdf`.

**Cierre.** Todo documento formal termina con el párrafo de cortesía y el **bloque de contacto** de la hoja membretada —Director General y Directora Comercial—, nunca con una firma en texto. Es el último párrafo del cuerpo de la plantilla: se conserva intacto y se coloca al final.

**Revisión visual obligatoria.** Ningún documento formal se entrega sin renderizarlo a PDF y mirar la portada, una página interior y la última. Un hueco de dos o tres centímetros bajo el logotipo, un cierre sin bloque de contacto, un bloque de firma partido entre hojas o una página casi vacía son defectos de entrega, no detalles.

**Presentaciones.** Tienen su propio patrón de la firma. Cargar `mlr-presentaciones`.

## 2. Profundidad

Lo que en MLR se pide como "que se vea 3D" es jerarquía por elevación, no efectos tridimensionales.

- **Sombras en capas, nunca una sola.** Tres paradas: una muy cercana y tenue que define el borde, una media que da despegue, una amplia y muy difusa que asienta el elemento. Las tres tintadas con el matiz del fondo, jamas negro puro.
- **Fuente de luz única y constante** en toda la pieza.
- **Escala de elevación de cuatro niveles**: fondo, superficie, elemento destacado, elemento flotante. Nada intermedio improvisado.
- **Filo superior iluminado**: una línea de 1px blanca a muy baja opacidad en el borde superior de las superficies elevadas. Es el detalle que separa lo moldeado de lo pegado.
- **Profundidad por solape y desfase**, no solo por sombra. Que un elemento invada el territorio de otro genera mas sensación de capas que cualquier sombra.
- **Grano o textura a opacidad casi imperceptible** sobre los fondos grandes. Mata el aspecto de plástico plano.
- **Gradientes de un solo tono**, variando luminosidad y no matiz, sobre superficies amplias.

## 3. Lista negra

Cada uno de estos delata origen de IA a primera vista:

- El gradiente morado a azul. Ninguna variante.
- Emojis como iconos, viñetas o marcadores de sección.
- Héroe centrado seguido de tres tarjetas idénticas en fila.
- Radio de esquina uniforme en absolutamente todo.
- Paletas de cinco o mas matices distintos compitiendo.
- Formas abstractas, blobs y mallas de puntos de relleno.
- Sombra única y plana repetida en cada elemento.
- Tipografía por defecto sin decisión: la misma familia en todo, sin par tipográfico.
- Todas las secciones del mismo peso visual y la misma altura.
- Copy de plantilla: «Transforma tu», «Potencia tu», «Impulsa tu», «Descubre el poder de».
- Iconografía genérica de librería sin relación con el contenido real.

## 4. Composición

- **Asimetría deliberada.** Retícula editorial de 12 columnas con bloques de anchos distintos. La simetría total lee como plantilla.
- **Densidad variable.** Alterna bloques densos con aire. Una pieza de ritmo constante se lee como generada.
- **Un solo foco por vista.** Si todo destaca, nada destaca.
- **Espaciado en escala geométrica**, no valores sueltos.
- **Los datos mandan sobre la decoración.** Si un gráfico y un adorno compiten por el espacio, gana el gráfico.

## 5. Por medio

**Documentos formales.** Membrete MLR, secciones numeradas, prosa. La sobriedad tipográfica es el diseño. Sin tablas decorativas ni cajas de nota, salvo petición expresa.

**Presentaciones.** Una idea por lamina. El titular es la conclusión, no la etiqueta del tema. Datos grandes, contexto pequeño.

**Páginas y artifacts.** Autocontenidos, paleta declarada en tokens, adaptados a tema claro y oscuro. Nunca dejes un color definido solo dentro de un bloque de tema.

**Gráficas.** Carga la skill de visualización de datos antes de escribir código de gráfico, y después alinea la paleta a la de la firma.

## 6. Verificación

Antes de entregar, revisa la pieza contra la lista negra elemento por elemento. Si detectas uno, corrígelo antes de mostrarla. Cuando sea posible, renderiza y mira el resultado en vez de asumirlo.

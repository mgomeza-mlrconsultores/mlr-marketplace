---
name: mlr-identidad-visual
description: Estandar visual de MLR Consultores para documentos, presentaciones, paginas web, artifacts, tableros y graficas. Define membrete, paleta, tipografia, profundidad y jerarquia, y elimina los rasgos que delatan diseno generado por IA. Cargar antes de decidir un solo color o una sola tipografia.
---

# Identidad visual MLR

El criterio de aceptacion es que la pieza parezca hecha por un estudio de diseno, no por un asistente.

## 1. Marca

Los valores oficiales estan en `references/marca.md`: paleta, tipografia, reglas de logotipo, datos de membrete y estilo de la firma. **No preguntar por ellos ni inventarlos.**

Lo esencial, para no tener que abrir el archivo en cada pieza:

- **Teal `#24606C`** dominante. **Cafe `#452E27`** solo como acento o palabra destacada. **Azul claro `#E6F3FB`** para fondos.
- Titulares en **Oswald Bold**, cuerpo en **Inter Regular**.
- Texto blanco sobre teal o cafe; gris carbon `#2B2B2B` o teal sobre fondo claro.
- Solo colores institucionales. No recolorear fuera de la gama.

**Documentos formales.** Se construyen sobre la plantilla de Word del membrete, descargandola de la unidad compartida y escribiendo dentro. Nunca recreando el encabezado. Identificadores en `references/marca.md`.

**Margenes del membrete.** La plantilla en crudo deja una banda vacia arriba y abajo. Aplicar siempre los valores corregidos de `references/margenes-membrete.md`: superior 3000 tw, inferior 2560 tw, laterales 1240 tw, encabezado a 0 y pie a 1901 tw. El encabezado a 0 es lo que pone la imagen del membrete a ras de hoja y elimina el exceso de espacio.

**Presentaciones.** Tienen su propio patron de la firma. Cargar `mlr-presentaciones`.

## 2. Profundidad

Lo que en MLR se pide como "que se vea 3D" es jerarquia por elevacion, no efectos tridimensionales.

- **Sombras en capas, nunca una sola.** Tres paradas: una muy cercana y tenue que define el borde, una media que da despegue, una amplia y muy difusa que asienta el elemento. Las tres tintadas con el matiz del fondo, jamas negro puro.
- **Fuente de luz unica y constante** en toda la pieza.
- **Escala de elevacion de cuatro niveles**: fondo, superficie, elemento destacado, elemento flotante. Nada intermedio improvisado.
- **Filo superior iluminado**: una linea de 1px blanca a muy baja opacidad en el borde superior de las superficies elevadas. Es el detalle que separa lo moldeado de lo pegado.
- **Profundidad por solape y desfase**, no solo por sombra. Que un elemento invada el territorio de otro genera mas sensacion de capas que cualquier sombra.
- **Grano o textura a opacidad casi imperceptible** sobre los fondos grandes. Mata el aspecto de plastico plano.
- **Gradientes de un solo tono**, variando luminosidad y no matiz, sobre superficies amplias.

## 3. Lista negra

Cada uno de estos delata origen de IA a primera vista:

- El gradiente morado a azul. Ninguna variante.
- Emojis como iconos, vinetas o marcadores de seccion.
- Heroe centrado seguido de tres tarjetas identicas en fila.
- Radio de esquina uniforme en absolutamente todo.
- Paletas de cinco o mas matices distintos compitiendo.
- Formas abstractas, blobs y mallas de puntos de relleno.
- Sombra unica y plana repetida en cada elemento.
- Tipografia por defecto sin decision: la misma familia en todo, sin par tipografico.
- Todas las secciones del mismo peso visual y la misma altura.
- Copy de plantilla: «Transforma tu», «Potencia tu», «Impulsa tu», «Descubre el poder de».
- Iconografia generica de libreria sin relacion con el contenido real.

## 4. Composicion

- **Asimetria deliberada.** Reticula editorial de 12 columnas con bloques de anchos distintos. La simetria total lee como plantilla.
- **Densidad variable.** Alterna bloques densos con aire. Una pieza de ritmo constante se lee como generada.
- **Un solo foco por vista.** Si todo destaca, nada destaca.
- **Espaciado en escala geometrica**, no valores sueltos.
- **Los datos mandan sobre la decoracion.** Si un grafico y un adorno compiten por el espacio, gana el grafico.

## 5. Por medio

**Documentos formales.** Membrete MLR, secciones numeradas, prosa. La sobriedad tipografica es el diseno. Sin tablas decorativas ni cajas de nota, salvo peticion expresa.

**Presentaciones.** Una idea por lamina. El titular es la conclusion, no la etiqueta del tema. Datos grandes, contexto pequeno.

**Paginas y artifacts.** Autocontenidos, paleta declarada en tokens, adaptados a tema claro y oscuro. Nunca dejes un color definido solo dentro de un bloque de tema.

**Graficas.** Carga la skill de visualizacion de datos antes de escribir codigo de grafico, y despues alinea la paleta a la de la firma.

## 6. Verificacion

Antes de entregar, revisa la pieza contra la lista negra elemento por elemento. Si detectas uno, corrigelo antes de mostrarla. Cuando sea posible, renderiza y mira el resultado en vez de asumirlo.

# Formato HTML de dirección con la barra de la firma

Origen: documento HTML que hizo dirección para Reciservicios (11-sep-2026), aprobado como formato de la firma. La guía funcional le suma la barra superior del deck de `mlr-presentaciones`. Lo implementa `scripts/genera_html.py`; este archivo explica que no se toca.

## Laminas

- `section.sheet` por idea, `min-height: calc(100vh - var(--hd))`, contenido en `.wrap` blanco con radio 14 px, sombra en tres capas y filete inferior teal 62 % / bruma 38 %.
- `.topline` en IBM Plex Mono mayúsculas: a la izquierda la ceja ("Paso 3.2 · Entregar la mercancía"), a la derecha el cliente.
- `h2` es el titular-conclusion en Archivo 800 condensada, teal, de 30 a 50 px según la pantalla, máximo 18 caracteres de ancho de línea, con una barra de acento teal de 56 x 4 px encima.
- Contenedor ancho (`min(92vw, 1600px)`) que llena la altura de la pantalla, con márgenes generosos: se aprovecha la pantalla sin que se vea cargada (Freshbox, 29-sep-2026).

## Acomodos de la lamina

Criterio de dirección: impacto, no vistas cargadas. El texto manda a la izquierda y las capturas acompañan a la derecha sin dominar.

- `.split`: texto a la izquierda (5 fr) y figuras a la derecha (7 fr), centrados verticalmente. `.split.par` (4.2 fr / 7.8 fr) cuando las figuras van lado a lado o en rejilla.
- Figuras `pila` (una sobre otra) por defecto; `fila` (lado a lado, columnas proporcionales a su ancho) cuando son dos y alguna es vertical o ninguna es muy ancha; `rejilla` de dos columnas con tres o cuatro.
- Cada imagen se dibuja a su tamaño real por 1.25 como máximo y el bloque de figuras nunca pasa del 64 % del alto de la pantalla. Un script en el navegador las reduce en proporción hasta que la lamina cabe; se recalcula al cargar, con las fuentes y al cambiar el tamaño.
- `.split.tabla`: si hay cuadro y capturas, el titular cruza la lamina y debajo van cuadro y capturas a partes iguales.
- `.texto`: sin figuras y solo prosa o guiones, titular a la izquierda y texto a la derecha.
- `.solo`: sin figuras pero con cifras `kpi`, `flujo` o cuadro, a lo ancho.
- En pantalla menor a 980 px todo pasa a una columna.
- Portada y cierre con `data-bg="dark"`: degradado teal, logotipo, kicker, titular, metadatos (cliente, atención, plataforma, fecha, emite) y en el cierre el bloque de contacto y el lema.
- El cierre busca impacto: frase de cierre grande (32 a 60 px, condensada, blanca, máximo 26 caracteres de ancho), logotipo de 64 px arriba, contacto abajo y lema de 22 px. Nada de un párrafo chico perdido en la lamina.

## Paleta y tipografía

Teal #22646E, teal oscuro #16313A, bruma #7EBFC9, rojo #B03A2B, ámbar #9A6614, café #452E27, verde de resultado #2E7D5B. Archivo para títulos y cuerpo, IBM Plex Mono para cejas, contador y etiquetas. Google Fonts con familias locales de respaldo: la página abre sin internet.

## Barra superior (de `mlr-presentaciones`)

- `header.nav` fija, fondo teal oscuro, logotipo SVG y texto del tema.
- `#navbtns` se llena por código desde los `data-nav` de las laminas: un botón por grupo, marcado el del grupo visible (IntersectionObserver).
- `#progress` al pie de la barra según el desplazamiento; `#pgtxt` con "05 / 15".
- Teclado: flechas y AvPag/RePag avanzan o retroceden una lamina, Inicio y Fin. Escape cierra el lightbox.
- Botón "Tema" que alterna claro y oscuro sobre `data-theme`; sin elección manda `prefers-color-scheme`.

## Figuras

- `figure.shot` con fondo suave, borde y sombra; la imagen con borde #BFD4DA. Clic o Enter abre `#lb` a pantalla completa con el pie.
- Rejilla `.figs.n2/n3/n4`; con tres, la primera ocupa el ancho.
- Con una sola figura, la imagen se limita a la altura disponible de la pantalla.
- Sin `loading="lazy"`.

## Impresión

`@page` 13.333 x 7.5 in, una lamina por página, barra y lightbox ocultos. Para imprimir en papel se usa el modo claro.

## Que no hacer

- No meter tablas densas en una lamina con figuras; el cuadro va solo a la derecha.
- No numerar laminas ni armar el menú a mano.
- No copiar textos del Word si no caben: la lamina lleva el mismo contenido, pero el titular es propio del HTML (`TITULARES`).
- No agrandar las capturas hasta llenar la lamina: se ven cargadas y el mensaje se pierde. El tope del 64 % no se sube.
- No contar en una lamina cómo se hizo el trabajo (herramientas, accesos, rondas, verificaciones). La lamina dice lo que pasa en la base del cliente.

# Formato HTML de direccion con la barra de la firma

Origen: documento HTML que hizo direccion para Reciservicios (11-sep-2026), aprobado como formato de la firma. La guia funcional le suma la barra superior del deck de `mlr-presentaciones`. Lo implementa `scripts/genera_html.py`; este archivo explica que no se toca.

## Laminas

- `section.sheet` por idea, `min-height: calc(100vh - var(--hd))`, contenido en `.wrap` blanco con radio 14 px, sombra en tres capas y filete inferior teal 62 % / bruma 38 %.
- `.topline` en IBM Plex Mono mayusculas: a la izquierda la ceja ("Paso 3.2 · Entregar la mercancia"), a la derecha el cliente.
- `h2` es el titular-conclusion en Archivo 800 condensada, teal, maximo 22 caracteres de ancho de linea.
- `.split`: texto a la izquierda (5 fr) y figuras o cuadro a la derecha (7 fr). `.solo` si no hay figuras.
- Portada y cierre con `data-bg="dark"`: degradado teal, logotipo, kicker, titular, metadatos (cliente, atencion, plataforma, fecha, emite) y en el cierre el bloque de contacto y el lema.

## Paleta y tipografia

Teal #22646E, teal oscuro #16313A, bruma #7EBFC9, rojo #B03A2B, ambar #9A6614, cafe #452E27, verde de resultado #2E7D5B. Archivo para titulos y cuerpo, IBM Plex Mono para cejas, contador y etiquetas. Google Fonts con familias locales de respaldo: la pagina abre sin internet.

## Barra superior (de `mlr-presentaciones`)

- `header.nav` fija, fondo teal oscuro, logotipo SVG y texto del tema.
- `#navbtns` se llena por codigo desde los `data-nav` de las laminas: un boton por grupo, marcado el del grupo visible (IntersectionObserver).
- `#progress` al pie de la barra segun el desplazamiento; `#pgtxt` con "05 / 15".
- Teclado: flechas y AvPag/RePag avanzan o retroceden una lamina, Inicio y Fin. Escape cierra el lightbox.
- Boton "Tema" que alterna claro y oscuro sobre `data-theme`; sin eleccion manda `prefers-color-scheme`.

## Figuras

- `figure.shot` con fondo suave, borde y sombra; la imagen con borde #BFD4DA. Clic o Enter abre `#lb` a pantalla completa con el pie.
- Rejilla `.figs.n2/n3/n4`; con tres, la primera ocupa el ancho.
- Con una sola figura, la imagen se limita a la altura disponible de la pantalla.
- Sin `loading="lazy"`.

## Impresion

`@page` 13.333 x 7.5 in, una lamina por pagina, barra y lightbox ocultos. Para imprimir en papel se usa el modo claro.

## Que no hacer

- No meter tablas densas en una lamina con figuras; el cuadro va solo a la derecha.
- No numerar laminas ni armar el menu a mano.
- No copiar textos del Word si no caben: la lamina lleva el mismo contenido, pero el titular es propio del HTML (`TITULARES`).

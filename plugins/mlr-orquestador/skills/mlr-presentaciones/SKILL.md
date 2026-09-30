---
name: mlr-presentaciones
description: Construye presentaciones y decks de MLR Consultores en HTML autocontenido con el patrón de la firma: barra superior con logotipo vectorial, menú de grupos, diapositivas navegables por teclado, barra de progreso y contador. Cargar ante cualquier petición de presentación, deck, laminas o exposición para cliente.
---

# Presentaciones MLR

La firma tiene un patrón propio de deck en HTML, ya probado con clientes. **No inventes una estructura nueva.** Reproduce este patrón y cambia el contenido.

Un archivo HTML único, sin dependencias externas ni compilación. Se abre en cualquier navegador, se proyecta y se envía por correo.

## Esqueleto

```
<header class="nav">
  <div class="bar">
    <div class="brand">  [logotipo SVG]  <span>Tema — Cliente — Odoo</span>  </div>
    <nav id="navbtns"></nav>
  </div>
</header>

<div id="deck">
  <section class="slide" data-bg="dark" data-nav="Inicio"> ... </section>
  <section class="slide" data-nav="Resumen"> ... </section>
  ...
</div>

<footer>  <div id="progress"></div>  <span id="pgtxt">01 / 12</span>  </footer>
```

Cada diapositiva lleva un `<div class="wrap">` interior que centra y limita el ancho del contenido. La portada usa `data-bg="dark"` con dos `<div class="orb o1">` y `o2` como formas decorativas teal, y el logotipo completo en `class="cover-logo"`.

## Tokens

Declarar en `:root`, derivados de la paleta oficial de la firma:

```css
:root{
  --teal:#24606C; --teal-d:#18454E; --teal-l:#6FA3AB; --teal-soft:#E6F3FB;
  --brown:#452E27; --amber:#C9772E; --alert:#B23A3A; --ok:#2E7D5B;
  --ink:#2B2B2B; --muted:#5A6B6E; --line:#D8DEE0; --bg:#F5F7F8; --white:#fff;
  --f-head:'Oswald','Archivo','DejaVu Sans',system-ui,sans-serif;
  --f-body:'Inter','Source Sans 3','DejaVu Sans',system-ui,sans-serif;
  --hd:60px; --ft:54px;
}
```

`--amber`, `--alert` y `--ok` son de estado: señalan advertencia, error y correcto en diagramas y cuadros de hallazgo. No decoran.

Incluir siempre las alternativas `DejaVu Sans` y `system-ui` en las pilas tipográficas: el deck debe verse bien sin acceso a internet, en la sala del cliente.

## Navegación

El menú se construye por código desde un arreglo de grupos, no a mano. Cada grupo apunta al índice de la diapositiva donde empieza:

```js
const groups=[['Inicio',0],['Resumen',1],['El flujo',2],['Beneficios',8],['Cierre',9]];
```

La función `show(i)` activa la diapositiva, actualiza el contador con formato `01 / 12`, mueve la barra de progreso y marca con la clase `act` el grupo al que pertenece la lamina actual. Al cambiar de lamina, el scroll interno vuelve al inicio.

Teclado obligatorio: flecha derecha, abajo y PageDown avanzan; flecha izquierda, arriba y PageUp retroceden; Home va a la primera; End a la última.

Entre cuatro y seis grupos. Mas de seis y el menú deja de orientar.

## Contenido

- **Una idea por lamina.** Si necesita dos, son dos laminas.
- **El titular es la conclusión, no la etiqueta del tema.** «El costo no llega al asiento» y no «Análisis de costos».
- Cifras grandes, contexto pequeño.
- Capturas reales de Odoo, guardadas en `assets/` junto al HTML y referenciadas de forma relativa. Nunca recreaciones de la interfaz.
- El logotipo va en la barra en todas las laminas, y completo solo en la portada.
- Cierre con los datos de contacto aprobados de la firma.

## Criterio estético de dirección

Fijado con Marcos en el diagnóstico de Freshbox (29-sep-2026), aplica a todo deck y a toda presentación HTML de informe:

- **Impacto, no vistas cargadas.** Poco texto por lamina, titular grande y aire alrededor. Si la lamina se ve llena, sobra algo.
- **Texto a la izquierda, capturas a la derecha, sin que dominen.** Las capturas acompañan: nunca más del 64 % del alto de la pantalla ni más del 125 % de su tamaño real. Agrandarlas para llenar la pantalla fue lo primero que dirección rechazó.
- Contenedor ancho, pero con márgenes amplios; una barra corta de acento teal sobre cada titular.
- **Cierre con impacto:** una frase grande y condensada, el logotipo y el contacto. Un párrafo chico en la última lamina se ve flojo.
- Ninguna lamina explica cómo se hizo el trabajo: ni accesos, ni herramientas, ni rondas de verificación.

Las presentaciones de diagnóstico e informe se generan con `mlr-informe-funcional/scripts/genera_html.py`, que ya aplica estos criterios y elige el acomodo de cada lamina por la proporción de sus capturas. Detalle en `mlr-informe-funcional/references/formato-html-direccion.md`.

## Archivos

Nombre: `MLR_Presentacion_<Tema>_<Cliente>_<AAAA-MM-DD>.html`.

Ubicación: `MLR Odoo\<Cliente>\Informes\<AAAAMMDD>\`, con las imágenes incrustadas o en `assets\` dentro de esa misma carpeta de fecha, y las capturas originales en `Capturas de pantalla\<AAAAMMDD>\`. Si la carpeta del cliente, alguna de las tres carpetas fijas o la de fecha no existen, se crean completas antes de guardar, sin preguntar (regla única en `mlr-orquestador/references/carpetas-y-entrega.md`).

Toda presentación se acompaña de su informe en Word sobre el membrete de la firma. El deck expone; el informe sustenta.

## Verificación

Abrir el archivo en el navegador y recorrerlo completo con el teclado antes de entregarlo. Comprobar que el menú marca el grupo correcto, que el contador cuadra con el número de laminas y que ninguna imagen falta.

Ver `references/logo-svg.md` para el logotipo vectorial y `references/patron-deck.md` para el detalle de clases y comportamiento.

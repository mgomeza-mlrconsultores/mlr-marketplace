# Patrón de deck MLR — detalle

## Clases

| Clase o id | Función |
|---|---|
| `header.nav` | Barra superior fija, fondo teal. Altura `--hd` |
| `.bar` | Contenedor interno de la barra: marca a la izquierda, menú a la derecha |
| `.brand` | Logotipo SVG mas un `<span>` con tema, cliente y sistema |
| `#navbtns` | Contenedor del menú. Se llena por código, nunca a mano |
| `#deck` | Contenedor de todas las diapositivas |
| `.slide` | Una diapositiva. Oculta salvo que tenga `active` |
| `.slide.active` | La visible |
| `.wrap` | Contenedor interior que centra y limita el ancho |
| `.orb o1` / `.orb o2` | Formas orgánicas teal decorativas. Solo en portada y cierre |
| `.cover-logo` | Logotipo completo, solo en portada |
| `#progress` | Barra de avance. Ancho en porcentaje |
| `#pgtxt` | Contador con formato `01 / 12` |
| `button.act` | Grupo activo del menú |

## Atributos de datos

- `data-bg="dark"` en las laminas de fondo teal: portada, separadores de sección y cierre.
- `data-nav="<Grupo>"` documenta a que grupo pertenece la lamina. Sirve de referencia legible; el menú se construye desde el arreglo `groups`.

## Comportamiento

`show(i)` acota el índice al rango valido, alterna la clase `active`, actualiza contador y barra, resuelve que grupo del menú marcar recorriendo `groups` y quedándose con el último cuyo índice de inicio sea menor o igual al actual, y devuelve el scroll de la lamina al inicio.

`go(d)` avanza o retrocede una posición.

Al final del script, `show(0)` deja el deck en la portada.

## Impresión y PDF

Las laminas de fondo oscuro consumen mucho tóner. Si el cliente pide el deck impreso, generar una variante con `data-bg` retirado y fondo claro, no imprimir la versión de proyección.

## Que no hacer

- No cargar librerías externas: ni framework de presentaciones, ni tipografías remotas sin alternativa local, ni iconos de CDN. El deck debe abrir sin internet.
- No animar transiciones entre laminas. El cambio es inmediato.
- No numerar las laminas a mano: el contador se calcula.
- No meter tablas densas. Si el dato necesita una tabla, va en el informe de Word.

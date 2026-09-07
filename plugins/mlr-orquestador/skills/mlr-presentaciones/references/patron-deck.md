# Patron de deck MLR — detalle

## Clases

| Clase o id | Funcion |
|---|---|
| `header.nav` | Barra superior fija, fondo teal. Altura `--hd` |
| `.bar` | Contenedor interno de la barra: marca a la izquierda, menu a la derecha |
| `.brand` | Logotipo SVG mas un `<span>` con tema, cliente y sistema |
| `#navbtns` | Contenedor del menu. Se llena por codigo, nunca a mano |
| `#deck` | Contenedor de todas las diapositivas |
| `.slide` | Una diapositiva. Oculta salvo que tenga `active` |
| `.slide.active` | La visible |
| `.wrap` | Contenedor interior que centra y limita el ancho |
| `.orb o1` / `.orb o2` | Formas organicas teal decorativas. Solo en portada y cierre |
| `.cover-logo` | Logotipo completo, solo en portada |
| `#progress` | Barra de avance. Ancho en porcentaje |
| `#pgtxt` | Contador con formato `01 / 12` |
| `button.act` | Grupo activo del menu |

## Atributos de datos

- `data-bg="dark"` en las laminas de fondo teal: portada, separadores de seccion y cierre.
- `data-nav="<Grupo>"` documenta a que grupo pertenece la lamina. Sirve de referencia legible; el menu se construye desde el arreglo `groups`.

## Comportamiento

`show(i)` acota el indice al rango valido, alterna la clase `active`, actualiza contador y barra, resuelve que grupo del menu marcar recorriendo `groups` y quedandose con el ultimo cuyo indice de inicio sea menor o igual al actual, y devuelve el scroll de la lamina al inicio.

`go(d)` avanza o retrocede una posicion.

Al final del script, `show(0)` deja el deck en la portada.

## Impresion y PDF

Las laminas de fondo oscuro consumen mucho toner. Si el cliente pide el deck impreso, generar una variante con `data-bg` retirado y fondo claro, no imprimir la version de proyeccion.

## Que no hacer

- No cargar librerias externas: ni framework de presentaciones, ni tipografias remotas sin alternativa local, ni iconos de CDN. El deck debe abrir sin internet.
- No animar transiciones entre laminas. El cambio es inmediato.
- No numerar las laminas a mano: el contador se calcula.
- No meter tablas densas. Si el dato necesita una tabla, va en el informe de Word.

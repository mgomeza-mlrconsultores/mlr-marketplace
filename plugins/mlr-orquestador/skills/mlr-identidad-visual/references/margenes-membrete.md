# Hoja membretada: de donde se parte y como se cierra

**Regla primera y no negociable: no se estiman margenes ni se reconstruye el membrete.**
Se abre la plantilla oficial calibrada, se vacía el cuerpo conservando la sección final,
los encabezados y el párrafo que ancla el bloque de contacto, y se escribe dentro.
Copiar los margenes de un entregable anterior es el error que se ha repetido; un documento
previo sirve para confirmar, nunca como fuente.

## Las dos plantillas

En `C:\Users\mgome\Claude\Projects\MLR Odoo\Plantillas\` y en
`G:\Unidades compartidas\Marcos 2026\Marcos 2026\`:

- **Hoja Membretada MLR - 1 pagina.docx** — cartas, notas, fichas, cualquier cosa de una plana.
- **Hoja Membretada MLR - varias paginas.docx** — informes, anexos y propuestas.

`Hoja Membretada MLR (base documentos).docx` es el original sin calibrar. **No se usa.**

## Geometría calibrada, ya dentro de las plantillas

| Propiedad | 1 página | Varias páginas |
|---|---|---|
| Superior | 2520 tw · 1.75" | **1584 tw · 1.10"** |
| Inferior | 4176 tw · 2.90" | **2016 tw · 1.40"** |
| Laterales | 1238 tw · 0.86" | **1238 tw · 0.86"** |
| Encabezado desde el borde | 1138 tw · 0.79" | **1138 tw · 0.79"** |
| Pie desde el borde | sin folio | **1512 tw · 1.05"** |
| Primera página distinta | si | **si** |

```xml
<w:pgMar w:top="1584" w:right="1238" w:bottom="2016" w:left="1238"
         w:header="1138" w:footer="1512" w:gutter="0"/>
```

El logotipo de portada termina en 1.49"; el monograma de las páginas interiores, en 0.84";
el lema empieza en 10.02". De ahí salen los valores: el texto arranca justo debajo de lo
impreso y termina justo encima, con el folio en medio. **Si en el PDF se ve un hueco de dos
o tres centímetros bajo el logotipo, se partió de la plantilla equivocada.**

## El membrete se ancla a la página, nunca al margen

En los `header*.xml` la imagen va con `<wp:positionV relativeFrom="page">`. Con anclaje al
margen, cambiar el margen mueve el membrete y el lema deja de coincidir con el papel
impreso. Las plantillas calibradas ya vienen ancladas a la página; si un documento heredado
trae `relativeFrom="margin"`, se corrige.

## El cierre es el bloque de contacto, nunca una firma en texto

Todo documento termina con el bloque de Director General y Directora Comercial, con correo
y teléfono. Es una imagen flotante anclada a la página, `posOffset` vertical **7525512** EMU,
centrada, dentro de un párrafo que reserva 2" de altura exacta (`w:spacing w:line="2880"
w:lineRule="exact"`). Esa altura exacta es lo que hace que, si el texto llega demasiado
abajo, el párrafo no quepa y se lleve el bloque a la página siguiente en lugar de solaparse.

Ese párrafo es el último del cuerpo de la plantilla: **se conserva intacto y se coloca al
final del documento generado.** El primer párrafo de la plantilla, con
`w:spacing w:before="1224"`, protege la portada de invadir el logotipo grande; los
documentos que componen su propia portada con párrafos vacíos no lo necesitan.

Antes de insertar nada, se cuentan los `w:drawing` del cuerpo: si Marcos ya coloco el
bloque en su versión, volver a insertarlo lo duplica.

## Tipografía

Cuerpo en **Lexend 11**, fijado en `docDefaults` de `styles.xml`, nunca run por run. Ver
`marca.md`. Lexend es mas ancha que Calibri: al cambiar la fuente hay que revisar la portada,
porque títulos que antes cabían en una línea pasan a dos y las sangrías simuladas se parten.

## Folio

Las plantillas no traen `footer1.xml`. Si el documento lleva folio, se injerta la parte,
se declara en `[Content_Types].xml`, se añade la relación en `document.xml.rels` y se mete
`<w:footerReference w:type="default" r:id="..."/>` en el `sectPr`. El pie ya está calibrado
a 1512 tw, que sitúa el folio entre el fin del texto y el lema.

## Verificación obligatoria

No se entrega un documento formal sin renderizarlo a PDF y **mirarlo**: portada, una página
interior y la última. La revisión no se sustituye por leer el XML.

1. La imagen del membrete llega al borde de la hoja, sin banda blanca arriba.
2. Entre el logotipo y la primera línea hay una holgura corta. Un hueco de dos o tres
   centímetros significa margenes mal.
3. El texto no invade el monograma ni el lema; el folio queda entre ambos.
4. La última página cierra con el bloque de contacto, sin solaparse con el lema.
5. Cero encabezados colgados y cero bloques de firma partidos entre hojas.
6. Ninguna página de contenido por debajo del 85% de ocupación.
7. La numeración aparece y es correlativa.

## Errores registrados, para no repetirlos

- **Partir de un entregable anterior en vez de la plantilla oficial.** Así se arrastraron
  margenes de 3000 / 2560 tw que dejaban unos 3 cm muertos arriba y mas de 2 abajo, y así se
  perdió el bloque de contacto del cierre. Dirección lo rechazo el 2026-09-09.
- **Cerrar con firma en texto.** El cierre es el bloque de contacto. Siempre.
- **Sangrías de portada simuladas con espacios.** Al cambiar margenes o fuente, la línea
  larga se parte y la continuación cae fuera del bloque. La sangría se hace con `w:ind`.
- **Cambiar la fuente y no revisar la portada.** El título pasa a dos lineas sin avisar.

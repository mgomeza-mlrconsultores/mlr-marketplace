---
name: mlr-informe-funcional
description: Guía o informe funcional de un desarrollo de Odoo para el usuario del cliente, paso a paso y con capturas reales, entregado en Word membretado y en HTML con el formato aprobado por dirección (laminas, menú arriba, lightbox, modo oscuro). Cargar cuando se pida explicar como funciona un desarrollo, un manual de usuario, una guía de operación o un informe funcional no técnico.
---

# Informe funcional MLR

Explica a quien opera el sistema como se usa lo que se construyo. No es el informe técnico de cierre (ese lo hace `mlr-report-writer` con campos, vistas y pasos de migración). Aquí no aparecen nombres técnicos de campos, modelos, XML ids ni código: aparecen pantallas, botones, documentos y lo que el sistema hace solo.

Se entrega siempre en dos formatos que salen de **una sola fuente de contenido**:

- Word sobre la hoja membretada, con `documento_mlr.py` de `mlr-identidad-visual` y su verificador.
- HTML autocontenido con el formato de dirección (Reciservicios, 11-sep-2026) mas la barra de la firma: logotipo, menú de grupos arriba, barra de progreso, contador, teclado y botón de tema.

Carga también `mlr-redaccion` antes de escribir una línea. Las reglas de allí mandan sobre cualquier cosa de aquí.

## 1. Orden de trabajo

1. **Datos de demostración en la base de pruebas.** Un caso que recorra el proceso entero con documentos reales: orden, entrega, devolución, cobro, factura, pago. Anota los identificadores (S07976, INV/2026/00661...) porque los pies de figura los citan. Si se crean borradores solo para provocar un mensaje de error, se eliminan al terminar.
2. **Capturas.** Una por paso, sobre esos documentos. Método en `references/capturas-odoo.md`.
3. **Mira cada captura antes de escribir su pie.** El texto describe lo que la pantalla muestra, no lo que el desarrollo debería mostrar. Casos reales que se corrigieron así:
   - La factura PPD no muestra la forma de pago en pantalla (Odoo la oculta con PPD). El pie no puede decir "forma de pago Transferencia" sobre esa captura.
   - El formulario de una entrega de salida no muestra la ubicación destino. Para probar que la mercancía fue a consignación se usa el historial de movimientos (Desde / Hacia).
   - Los productos estaban en kg, no en piezas.
4. **Contenido** en `contenido.py` (copia `scripts/contenido_ejemplo.py`). Título, cliente, saludo, introducción, secciones con bloques, titulares del HTML, portada y datos que llegan tarde (tabla de pruebas, párrafo de producción).
5. **Word:** `python3 scripts/genera_docx.py <carpeta> <salida.docx> [datos.json]`, exportar a PDF y `verifica_documento.py` hasta que salga limpio.
6. **HTML:** `python3 scripts/genera_html.py <carpeta> <salida.html> [datos.json]` y `python3 scripts/revisa_html.py <salida.html> <carpeta_png>`; mirar las laminas generadas.
7. **Archivo:** `<Cliente>/Informes/AAAAMMDD/` para Word, PDF y HTML; `<Cliente>/Capturas de Pantalla/AAAAMMDD/` para las capturas. Nombre: `MLR_Guia_Funcional_<Tema>_<Cliente>_<AAAA-MM-DD>`.

## 2. Estructura del contenido

Carta, no manual de software: saludo nominal, "Por medio de la presente...", secciones numeradas en prosa, cierre de cortesía. Secciones típicas:

1. Que resuelve el desarrollo. El problema de antes y lo que hace ahora el sistema. Cuatro cifras como máximo en `kpi`.
2. Que se configuro y quien lo usa. Elementos nuevos en lenguaje de usuario, visibilidad por grupos. Un bloque `flujo` con los pasos del proceso para el HTML.
3. El proceso paso a paso. Un subapartado `("h", "3.1 ...")` por paso, texto corto y su captura. Cada subapartado es una lamina del HTML.
4. Que impide el sistema. Cuadro situación / que hace el sistema, con la captura de un mensaje real.
5. Pruebas realizadas. Que se probo, en que base, resultado. Solo lo que se ejecuto; lo pendiente no se lista como prueba.
6. Puesta en producción y pendientes. Fecha, versión, resultado de la instalación y decisiones abiertas en guiones.

Tipos de bloque: `p`, `h`, `v` (guiones), `fig` (clave de captura y pie), `t` (cabecera, filas, anchos en twips), `kpi`, `flujo`. `__PRUEBAS__` y `__PRODUCCION__` se llenan desde `datos.json`.

## 3. Reglas de redacción propias de la guía

- Pies de figura con el documento y la cifra que se ve: "Asiento STJ/2026/09/0183, que carga 267.46 pesos a la cuenta 115.01.03". Nunca "Pantalla de la orden".
- Titulares del HTML como conclusión: "La entrega se desvía sola a consignación y deja su asiento", no "Entrega".
- Nombres de botones y menús tal como salen en pantalla, en el idioma del usuario.
- Oraciones de 30 palabras de media como máximo; el verificador avisa por encima.
- "Integral" como adjetivo es relleno para el verificador: recorrido completo, prueba completa.
- El `cliente` del Word cabe en un renglón. El destinatario va en el saludo; en el HTML va en `ATENCION`.

## 4. Word: como pasar el verificador con figuras

- `Documento.imagen()` limita cada figura a 4.4 in de alto y a px/150 de ancho. Así caben dos por plana.
- Capturas altas (formularios completos): recortar o componer. Ejemplo aprobado: cabecera de la orden + casilla + lineas + importes, sin el espacio vacío de en medio.
- Asistentes y mensajes: capturar el `.modal-content`, no la pantalla oscurecida.
- Si una plana queda por debajo de 70 % es porque una figura o un cuadro indivisible no cupo. Se corrige moviendo la figura antes del cuadro, pasando un párrafo antes o después de la figura, o recortando la captura. Nunca con saltos de página.
- El último renglón puede quedar solo en la plana final; el verificador lo admite.

## 5. HTML

Detalle del formato en `references/formato-html-direccion.md`. Lo que no se negocia:

- Una lamina por idea; el menú de arriba se construye desde `data-nav`, nunca a mano.
- Las capturas van incrustadas y sin `loading="lazy"`: con carga diferida la impresión a PDF sale sin imágenes.
- Una sola figura por lamina se limita a la altura de la pantalla; con dos a cuatro va en rejilla.
- `revisa_html.py` en verde: sin scroll horizontal, sin imágenes rotas ni capturas pendientes, ninguna lamina mas alta que 1600x900 y una página impresa por lamina.

## 6. Seguridad

Las capturas y los datos de demostración se hacen solo en bases de pruebas confirmadas por Marcos. `captura_odoo.js` escribe adjuntos en la base y `descarga_capturas.py` los borra después. El asistente no introduce contraseñas: si el navegador no tiene sesión en esa base, se pide a Marcos que la abra.

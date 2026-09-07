# Tabla de enrutamiento MLR

Clasifica la peticion en una fila y carga TODO lo de su columna derecha, en ese orden.

## Texto para el cliente

Informe, diagnostico, memo, propuesta, cotizacion, correo formal, minuta, resumen ejecutivo.

`mlr-redaccion` → `docx` (Word) o `pdf` (PDF) → verificacion de cifras.

Nunca redactes un entregable sin `mlr-redaccion` cargada, ni siquiera un correo corto.

## Presentacion

`mlr-identidad-visual` → `pptx`, o el tipo de artifact de presentacion si esta disponible.

Una idea por lamina. El titular es la conclusion, no la etiqueta del tema.

## Pagina web, artifact, tablero o calculadora

`mlr-identidad-visual` → `ui-ux-pro-max` → `artifact-design` → `web-artifacts-builder`.

Si la pieza lleva movimiento, anade `mlr-animacion-web`.

## Grafica, indicador o visualizacion de datos

`dataviz` antes de escribir la primera linea de codigo de grafico. Nunca improvises paleta.

Despues `mlr-identidad-visual` para alinear la paleta a la marca.

## Diagrama

Proceso, flujo, arquitectura, modelo de datos, secuencia, estados.

`mlr-diagramas-odoo` → Mermaid con el tema de la firma. Para flujos que Mermaid no sepa organizar, D2.

Para co-disenar en reunion con el cliente, pizarra tipo Excalidraw; el entregable final se pasa despues a Mermaid.

## Video

Explicativo de proceso, demostracion de Odoo, animacion de datos.

`mlr-video`.

## Odoo

Campos, modelos, vistas, acciones de servidor, automatizaciones, acciones programadas.

`mlr-odoo-orchestrator` y los agentes especializados de creacion de campos, modelos, vistas y acciones.

Al terminar, informe en espanol con `mlr-redaccion`.

## Analisis de negocio y decision

- Optimizacion de proceso, riesgo operativo, capacidad, plan de cambio → plugin de operaciones.
- Analisis de varianza, estados financieros, conciliacion → plugin de finanzas.
- Riesgo legal, revision de contrato, verificacion de proveedor → plugin legal.
- Analisis de datos, consultas, validacion → plugin de datos.

Nombra siempre el marco que estas aplicando. Un analisis sin marco declarado es una opinion.

## Investigacion

Mercado, proveedor, competencia, precios, normativa.

Busqueda en vivo → verificacion en fuente primaria → cita de fuentes.

Nunca afirmes un precio, una cifra de mercado o un dato regulatorio sin haberlo comprobado en esta sesion.

## Hoja de calculo o modelo

`xlsx`. Formulas vivas, nunca valores calculados y pegados.

## Peticion ambigua

Explora requisitos antes de construir. Una pregunta bien hecha ahorra un entregable descartado.

# Tabla de enrutamiento MLR Consultores

Clasifica la petición en una fila y carga TODO lo de su columna derecha, en ese orden.

## Cotización y plan de implementación de Odoo

Propuesta económica, presupuesto, alcance, ruta por etapas, tareas, horas, precio por sede.

`cotizacion` → al llegar a los entregables, `redaccion` → `docx` y `xlsx`.

Se carga antes de listar tareas o estimar horas, no después. La skill impone el orden — cliente y base, preguntas, diagrama, ruta, horas, condiciones, entregables — y la regla de que nada se escribe en archivo antes de la aprobación en el chat.

## Diagnóstico de una base de Odoo

Auditoria, revisión de salud, estado real de inventario y valuación, contabilidad, migraciones, código a medida. Con o sin cotización posterior.

`diagnostico` → al llegar al informe, `redaccion` → Word con `documento_firma.py` y `verifica_documento.py`.

Solo lectura por API con lista blanca de métodos. Línea de tiempo de versiones antes de juzgar un saldo. Rondas desde cero, con agente ciego y verificadores, con mínimo 4 y máximo 10, y cierre cuando dos seguidas no traen errores o solo traen hallazgos menores. Cada hallazgo con folio, cifra y captura. Cuando después hay cotización, `cotizacion` toma el resultado en su fase 1.

## Conciliación bancaria y cierre de bancos

Conciliar un diario de banco, caja, tarjeta o acreedor en un periodo; saber si el mes cuadró; partidas sin identificar; cruce del estado de cuenta contra Odoo y los CFDI; previo de impuestos por flujo; pagos al SAT contra acuses; reversiones de IVA en base de efectivo.

`conciliacion-bancaria` (plugin `contabilidad`) → `xlsx` para el libro → al llegar al correo o informe del cliente, `redaccion` e `identidad-visual`.

Arranque guiado un dato a la vez, estado de cuenta con control de carátula en cero, libro por diario y periodo, acciones que solo se aplican con `Aprobado = Sí`, una fila por tipo antes del lote y cierre con la hoja Verificación en CERRADO. Los criterios fiscales del cliente se leen y se guardan con `memoria`. Si la revisión de configuración destapa problemas de fondo, se pasa a `diagnostico`.

## Texto para el cliente

Informe, diagnóstico, memo, propuesta, cotización, correo formal, minuta, resumen ejecutivo.

`redaccion` → `docx` (Word) o `pdf` (PDF) → verificación de cifras.

Nunca redactes un entregable sin `redaccion` cargada, ni siquiera un correo corto.

## Guía o informe funcional

Como funciona un desarrollo, paso a paso, para quien lo opera. Manual de usuario, guía de operación, informe funcional no técnico.

`informe-funcional` → `redaccion` → Word con `documento_firma.py` y `verifica_documento.py` → HTML con `genera_html.py` y `revisa_html.py`.

Capturas reales sobre documentos de demostración en la base de pruebas, con pie que cita el documento y la cifra que se ve. El informe técnico de cierre de Odoo (campos, vistas, migración) sigue siendo de `report-writer`.

## Presentación

`presentaciones` → HTML autocontenido con el patrón de la firma: barra con logotipo vectorial, menú de grupos, navegación por teclado, barra de progreso y contador.

Solo usar `pptx` cuando el cliente pida expresamente un archivo de PowerPoint editable.

Una idea por lamina. El titular es la conclusión, no la etiqueta del tema.

## Página web, artifact, tablero o calculadora

`identidad-visual` → `ui-ux-pro-max` → `artifact-design` → `web-artifacts-builder`.

Si la pieza lleva movimiento, añade `animacion-web`.

## Gráfica, indicador o visualización de datos

`dataviz` antes de escribir la primera línea de código de gráfico. Nunca improvises paleta.

Después `identidad-visual` para alinear la paleta a la marca.

## Diagrama

Proceso, flujo, arquitectura, modelo de datos, secuencia, estados.

`diagramas-odoo` → Mermaid con el tema de la firma. Para flujos que Mermaid no sepa organizar, D2.

Para co-disenar en reunión con el cliente, pizarra tipo Excalidraw; el entregable final se pasa después a Mermaid.

## Video

Explicativo de proceso, demostración de Odoo, animación de datos.

`video`.

## Odoo

Campos, modelos, vistas, acciones de servidor, automatizaciones, acciones programadas.

`odoo-orchestrator` y los agentes especializados de creación de campos, modelos, vistas y acciones.

Al terminar, informe en español con `redaccion`.

## Análisis de negocio y decisión

- Optimización de proceso, riesgo operativo, capacidad, plan de cambio → plugin de operaciones.
- Análisis de varianza y estados financieros → plugin de finanzas. La conciliación bancaria de un cliente en Odoo va a `conciliacion-bancaria`, no al plugin genérico.
- Riesgo legal, revisión de contrato, verificación de proveedor → plugin legal.
- Análisis de datos, consultas, validación → plugin de datos.

Nombra siempre el marco que estas aplicando. Un análisis sin marco declarado es una opinión.

## Investigación

Mercado, proveedor, competencia, precios, normativa.

Búsqueda en vivo → verificación en fuente primaria → cita de fuentes.

Nunca afirmes un precio, una cifra de mercado o un dato regulatorio sin haberlo comprobado en esta sesión.

## Hoja de cálculo o modelo

`xlsx`. Fórmulas vivas, nunca valores calculados y pegados.

## Petición ambigua

Explora requisitos antes de construir. Una pregunta bien hecha ahorra un entregable descartado.

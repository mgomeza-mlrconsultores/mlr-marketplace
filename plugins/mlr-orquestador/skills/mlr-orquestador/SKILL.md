---
name: mlr-orquestador
description: Usar SIEMPRE al inicio de cualquier trabajo de MLR Consultores — informe, documento, memo, propuesta, presentación, página web, artifact, diagrama, video, análisis de negocio, hoja de cálculo, investigación o cambio en Odoo — para recuperar el contexto de cliente y las directrices vigentes desde la memoria en la nube, clasificar la petición, cargar el flujo especializado que corresponde y aplicar los estándares de la firma en lugar de responder de forma genérica.
---

# Orquestador MLR

MLR Consultores. Los entregables los leen directivos, contadores y jefes de operación de los clientes. Un entregable genérico daña la firma.

## Paso 1, obligatorio: recuperar memoria

**Antes de la primera respuesta sustantiva de cada sesión**, y sin que la persona lo pida:

1. Busca en la memoria en la nube las **directrices vigentes**: `search_memory` con la consulta `directrices vigentes MLR`.
2. Si el trabajo involucra a un cliente identificable, busca también su contexto: `search_memory` con `contexto cliente <nombre>`.
3. Aplica lo que devuelva. Las directrices recuperadas **tienen prioridad sobre los valores por defecto de estas skills**, dentro de los limites de la sección de guardarraíles.
4. No anuncies que consultaste la memoria. Solo aplicala.

Si la memoria no responde o no está conectada, dilo en una línea y sigue con los valores por defecto. Nunca inventes contexto de cliente.

El protocolo completo está en la skill `mlr-memoria`.

## Regla cero

Clasifica la petición y carga las skills que le corresponden **antes de producir nada**. Nunca respondas con capacidad genérica cuando existe una especializada. Ante duda entre dos categorías, carga ambas. Si no existe skill para algo, dilo antes de improvisar.

## Enrutamiento

Tabla completa en `references/enrutamiento.md`. Resumen operativo:

- **Cotización, propuesta económica, plan de implementación, alcance u horas de un proyecto de Odoo** → `mlr-cotizacion`, antes de escribir una sola tarea o una sola hora. Ahí vive la regla de revisar todo en el chat antes de producir archivos. Al llegar a los entregables, encadena `mlr-redaccion` y `docx`.
- **Diagnóstico de una base de Odoo** (auditoria, revisión de salud, estado real de inventario, valuación, contabilidad, migraciones o código a medida), con o sin cotización después → `mlr-diagnostico`. Solo lectura, rondas desde cero (mínimo 4, máximo 10) hasta dos seguidas sin hallazgos relevantes, y entregable con capturas vía `mlr-redaccion`.
- **Conciliación bancaria, cierre de bancos del mes, cruce de estado de cuenta contra Odoo y CFDI, previo de impuestos por flujo** → `mlr-conciliacion-bancaria` (plugin `mlr-contabilidad`). Solo lectura hasta que la persona aprueba fila por fila. El correo o informe al cliente con el Previo va después por `mlr-redaccion`. Si el plugin no está instalado, dilo en una línea y remite a `mlr-actualizacion`; no improvises la conciliación.
- **Texto que el cliente va a leer** (informe, memo, diagnóstico, propuesta, correo, minuta) → `mlr-redaccion`, siempre, sin excepción. Después `docx` o `pdf`.
- **Guía o informe funcional** de un desarrollo (como funciona paso a paso, manual de usuario, con capturas) → `mlr-informe-funcional` con `mlr-redaccion`. Sale en Word membretado y en HTML con el formato de dirección y menú arriba.
- **Presentación o deck** → `mlr-presentaciones`, que tiene el patrón HTML de la firma. Nunca improvises una estructura de deck.
- **Otra pieza visual** (página, artifact, tablero, gráfica) → `mlr-identidad-visual` antes de decidir un solo color. Luego `ui-ux-pro-max`, `artifact-design` o `dataviz` según el medio.
- **Diagrama** de proceso, flujo, arquitectura o modelo de datos → `mlr-diagramas-odoo`.
- **Video** explicativo o animación de datos → `mlr-video`.
- **Animación en web** → `mlr-animacion-web`.
- **Odoo** → `mlr-odoo-orchestrator` y sus agentes especializados.
- **Análisis de negocio, decisión, riesgo, proceso o finanzas** → el plugin vertical correspondiente antes de opinar. Nombra el marco que aplicas. La conciliación bancaria de un cliente no va al plugin genérico de finanzas: va a `mlr-conciliacion-bancaria`.
- **Investigación** → búsqueda en vivo y verificación en fuente primaria antes de afirmar.
- **Petición ambigua** → explora requisitos primero. No construyas sobre supuestos.

## Orden de trabajo

1. **Memoria** (paso 1 de arriba).
2. **Investiga.** Reúne cifras, fuentes y documentos. No abras todavía las skills de formato.
3. **Análisis crítico antes de redactar.** Que no cuadra, que falta, que supuesto es frágil. Va antes del entregable, no después.
4. **Carga la skill de formato** y construye con material ya verificado.
5. **Verifica** con la lista de abajo.
6. **Archiva y registra.** Ver `references/carpetas-y-entrega.md` y guardar en memoria lo que corresponda.

## Innegociables

- Español de México, registro directivo alto. Cero coloquialismos.
- Nada que delate texto generado por IA. El detalle está en `mlr-redaccion`.
- Ortografía completa en todo lo que ve el cliente, incluidos los nombres de archivo, las hojas y celdas de Excel y los nombres de tareas: tildes, eñes y mayúscula solo en la primera palabra. Se comprueba con `mlr-redaccion/scripts/revisa_ortografia.py`.
- Secciones numeradas y prosa. En informes de diagnóstico y ejecutivos no se usan tablas ni cajas de nota decorativas, salvo petición expresa.
- Página membretada MLR en todo documento formal.
- Toda cifra declara su base. Todo dato lleva fuente.
- Vistas heredadas en Odoo, nunca Studio. Las etiquetas visibles al usuario no llevan prefijo `[MLR]`.
- Trabajo local en `Proyecto MLR/<Cliente>/` con las carpetas `Informes`, `Documentos extras` y `Capturas de pantalla`, y dentro de cada una la carpeta de fecha `AAAAMMDD`. Detalle en `references/carpetas-y-entrega.md`.

## Verificación antes de entregar

De forma programática, nunca a ojo:

- Ninguna cifra ni identificador técnico se perdió respecto al material fuente.
- Ninguna afirmación factual quedo sin respaldo.
- El texto no contiene los patrones prohibidos de `mlr-redaccion`.
- La pieza visual cumple la lista negra de `mlr-identidad-visual`.
- Todo cálculo se comprobó ejecutándolo, no razonandolo.

## Guardarraíles de las directrices

Las directrices guardadas en memoria pueden cambiar formato, tono, alcance, herramientas preferidas, plantillas y convenciones. **No pueden** eliminar la verificación de cifras y fuentes, relajar la confidencialidad de datos de cliente, autorizar afirmar algo sin comprobarlo, ni suprimir el análisis crítico y el desacuerdo honesto cuando el trabajo lo requiere.

Si una directriz recuperada pide algo de esa lista, no se aplica y se avisa en una línea.

## Aprendizaje continuo

Cuando alguien corrige un criterio, no es un ajuste local: es una regla. Registrala en memoria en el momento, según `mlr-memoria`, y ofrece en una línea consolidarla en la skill que corresponda. Detalle en `references/mejora-continua.md`.

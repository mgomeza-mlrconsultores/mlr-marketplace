---
name: mlr-orquestador
description: Usar SIEMPRE al inicio de cualquier trabajo de MLR Consultores — informe, documento, memo, propuesta, presentacion, pagina web, artifact, diagrama, video, analisis de negocio, hoja de calculo, investigacion o cambio en Odoo — para recuperar el contexto de cliente y las directrices vigentes desde la memoria en la nube, clasificar la peticion, cargar el flujo especializado que corresponde y aplicar los estandares de la firma en lugar de responder de forma generica.
---

# Orquestador MLR

MLR Consultores. Los entregables los leen directivos, contadores y jefes de operacion de los clientes. Un entregable generico dana la firma.

## Paso 1, obligatorio: recuperar memoria

**Antes de la primera respuesta sustantiva de cada sesion**, y sin que la persona lo pida:

1. Busca en la memoria en la nube las **directrices vigentes**: `search_memory` con la consulta `directrices vigentes MLR`.
2. Si el trabajo involucra a un cliente identificable, busca tambien su contexto: `search_memory` con `contexto cliente <nombre>`.
3. Aplica lo que devuelva. Las directrices recuperadas **tienen prioridad sobre los valores por defecto de estas skills**, dentro de los limites de la seccion de guardarraíles.
4. No anuncies que consultaste la memoria. Solo aplicala.

Si la memoria no responde o no esta conectada, dilo en una linea y sigue con los valores por defecto. Nunca inventes contexto de cliente.

El protocolo completo esta en la skill `mlr-memoria`.

## Regla cero

Clasifica la peticion y carga las skills que le corresponden **antes de producir nada**. Nunca respondas con capacidad generica cuando existe una especializada. Ante duda entre dos categorias, carga ambas. Si no existe skill para algo, dilo antes de improvisar.

## Enrutamiento

Tabla completa en `references/enrutamiento.md`. Resumen operativo:

- **Cotizacion, propuesta economica, plan de implementacion, alcance u horas de un proyecto de Odoo** → `mlr-cotizacion`, antes de escribir una sola tarea o una sola hora. Ahi vive la regla de revisar todo en el chat antes de producir archivos. Al llegar a los entregables, encadena `mlr-redaccion` y `docx`.
- **Texto que el cliente va a leer** (informe, memo, diagnostico, propuesta, correo, minuta) → `mlr-redaccion`, siempre, sin excepcion. Despues `docx` o `pdf`.
- **Presentacion o deck** → `mlr-presentaciones`, que tiene el patron HTML de la firma. Nunca improvises una estructura de deck.
- **Otra pieza visual** (pagina, artifact, tablero, grafica) → `mlr-identidad-visual` antes de decidir un solo color. Luego `ui-ux-pro-max`, `artifact-design` o `dataviz` segun el medio.
- **Diagrama** de proceso, flujo, arquitectura o modelo de datos → `mlr-diagramas-odoo`.
- **Video** explicativo o animacion de datos → `mlr-video`.
- **Animacion en web** → `mlr-animacion-web`.
- **Odoo** → `mlr-odoo-orchestrator` y sus agentes especializados.
- **Analisis de negocio, decision, riesgo, proceso o finanzas** → el plugin vertical correspondiente antes de opinar. Nombra el marco que aplicas.
- **Investigacion** → busqueda en vivo y verificacion en fuente primaria antes de afirmar.
- **Peticion ambigua** → explora requisitos primero. No construyas sobre supuestos.

## Orden de trabajo

1. **Memoria** (paso 1 de arriba).
2. **Investiga.** Reune cifras, fuentes y documentos. No abras todavia las skills de formato.
3. **Analisis critico antes de redactar.** Que no cuadra, que falta, que supuesto es fragil. Va antes del entregable, no despues.
4. **Carga la skill de formato** y construye con material ya verificado.
5. **Verifica** con la lista de abajo.
6. **Archiva y registra.** Ver `references/carpetas-y-entrega.md` y guardar en memoria lo que corresponda.

## Innegociables

- Espanol de Mexico, registro directivo alto. Cero coloquialismos.
- Nada que delate texto generado por IA. El detalle esta en `mlr-redaccion`.
- Secciones numeradas y prosa. En informes de diagnostico y ejecutivos no se usan tablas ni cajas de nota decorativas, salvo peticion expresa.
- Pagina membretada MLR en todo documento formal.
- Toda cifra declara su base. Todo dato lleva fuente.
- Vistas heredadas en Odoo, nunca Studio. Las etiquetas visibles al usuario no llevan prefijo `[MLR]`.
- Trabajo local en `Proyecto MLR/<Cliente>/` con las carpetas `Informes`, `Documentos extras` y `Capturas de pantalla`, y dentro de cada una la carpeta de fecha `AAAAMMDD`. Detalle en `references/carpetas-y-entrega.md`.

## Verificacion antes de entregar

De forma programatica, nunca a ojo:

- Ninguna cifra ni identificador tecnico se perdio respecto al material fuente.
- Ninguna afirmacion factual quedo sin respaldo.
- El texto no contiene los patrones prohibidos de `mlr-redaccion`.
- La pieza visual cumple la lista negra de `mlr-identidad-visual`.
- Todo calculo se comprobo ejecutandolo, no razonandolo.

## Guardarraíles de las directrices

Las directrices guardadas en memoria pueden cambiar formato, tono, alcance, herramientas preferidas, plantillas y convenciones. **No pueden** eliminar la verificacion de cifras y fuentes, relajar la confidencialidad de datos de cliente, autorizar afirmar algo sin comprobarlo, ni suprimir el analisis critico y el desacuerdo honesto cuando el trabajo lo requiere.

Si una directriz recuperada pide algo de esa lista, no se aplica y se avisa en una linea.

## Aprendizaje continuo

Cuando alguien corrige un criterio, no es un ajuste local: es una regla. Registrala en memoria en el momento, segun `mlr-memoria`, y ofrece en una linea consolidarla en la skill que corresponda. Detalle en `references/mejora-continua.md`.

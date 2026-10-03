---
name: mlr-orquestador-consultoria
description: Usar SIEMPRE al inicio de cualquier trabajo de MLR Consultores — informe, documento, memo, propuesta, presentación, página web, artifact, diagrama, video, análisis de negocio, hoja de cálculo, investigación o cambio en Odoo — para recuperar el contexto de cliente y las directrices vigentes desde la memoria en la nube, clasificar la petición, cargar el flujo especializado que corresponde y aplicar los estándares de la firma en lugar de responder de forma genérica.
---

# Orquestador MLR Consultores

MLR Consultores. Los entregables los leen directivos, contadores y jefes de operación de los clientes. Un entregable genérico daña la firma.

## Paso 1, obligatorio: recuperar memoria

**Antes de la primera respuesta sustantiva de cada sesión**, y sin que la persona lo pida:

1. Busca en la memoria en la nube las **directrices vigentes**: `search_memory` con la consulta `directrices vigentes MLR Consultores`.
2. Si el trabajo involucra a un cliente identificable, busca también su contexto: `search_memory` con `contexto cliente <nombre>`.
3. Aplica lo que devuelva. Las directrices recuperadas **tienen prioridad sobre los valores por defecto de estas skills**, dentro de los limites de la sección de guardarraíles.
4. No anuncies que consultaste la memoria. Solo aplicala.

Si la memoria no responde o no está conectada, dilo en una línea y sigue con los valores por defecto. Nunca inventes contexto de cliente.

El protocolo completo está en la skill `memoria`.

## Regla cero

Clasifica la petición y carga las skills que le corresponden **antes de producir nada**. Nunca respondas con capacidad genérica cuando existe una especializada. Ante duda entre dos categorías, carga ambas. Si no existe skill para algo, dilo antes de improvisar.

## Enrutamiento

Tabla completa en `references/enrutamiento.md`. Resumen operativo:

- **Cotización, propuesta económica, plan de implementación, alcance u horas de un proyecto de Odoo** → `cotizacion`, antes de escribir una sola tarea o una sola hora. Ahí vive la regla de revisar todo en el chat antes de producir archivos. Al llegar a los entregables, encadena `redaccion` y `docx`.
- **Diagnóstico de una base de Odoo** (auditoria, revisión de salud, estado real de inventario, valuación, contabilidad, migraciones o código a medida), con o sin cotización después → `diagnostico`. Solo lectura, rondas desde cero (mínimo 4, máximo 10) hasta dos seguidas sin hallazgos relevantes, y entregable con capturas vía `redaccion`.
- **Conciliación bancaria, cierre de bancos del mes, cruce de estado de cuenta contra Odoo y CFDI, previo de impuestos por flujo** → `conciliacion-bancaria` (plugin `contabilidad`). Solo lectura hasta que la persona aprueba fila por fila. El correo o informe al cliente con el Previo va después por `redaccion`. Si el plugin no está instalado, dilo en una línea y remite a `actualizacion`; no improvises la conciliación.
- **Texto que el cliente va a leer** (informe, memo, diagnóstico, propuesta, correo, minuta) → `redaccion`, siempre, sin excepción. Después `docx` o `pdf`.
- **Guía o informe funcional** de un desarrollo (como funciona paso a paso, manual de usuario, con capturas) → `informe-funcional` con `redaccion`. Sale en Word membretado y en HTML con el formato de dirección y menú arriba.
- **Presentación o deck** → `presentaciones`, que tiene el patrón HTML de la firma. Nunca improvises una estructura de deck.
- **Otra pieza visual** (página, artifact, tablero, gráfica) → `identidad-visual` antes de decidir un solo color. Luego `ui-ux-pro-max`, `artifact-design` o `dataviz` según el medio.
- **Diagrama** de proceso, flujo, arquitectura o modelo de datos → `diagramas-odoo`.
- **Video** explicativo o animación de datos → `video`.
- **Animación en web** → `animacion-web`.
- **Odoo** → `odoo-orchestrator` y sus agentes especializados.
- **Análisis de negocio, decisión, riesgo, proceso o finanzas** → el plugin vertical correspondiente antes de opinar. Nombra el marco que aplicas. La conciliación bancaria de un cliente no va al plugin genérico de finanzas: va a `conciliacion-bancaria`.
- **Investigación** → búsqueda en vivo y verificación en fuente primaria antes de afirmar.
- **Petición ambigua** → explora requisitos primero. No construyas sobre supuestos.

## Enrutamiento ampliado por etapa y especialidad
Cada etapa y cada tipo de salida tiene un especialista y un revisor distinto del que produce; el orquestador los invoca en este orden y no entrega nada sin la segunda lectura. Consulta `conocimiento/etapas/README.md` y `conocimiento/revision-cruzada.md`.

- **Descubrimiento y requerimientos** → `analista-descubrimiento`, después `levantamiento-requerimientos`; diseño con `arquitecto-solucion`.
- **Diagnóstico** → `diagnostico` (rondas con `auditor-*`, `app-*` por aplicación y los auditores de `fiscal-mexico`, `nomina-mexico` y `practica-contable`); verificación con `verificador-hallazgos`.
- **Cotización** → `cotizador`, revisión con `revisor-cotizaciones`; lectura de mercado con `analista-mercado-precios` y efecto de herramientas con `evaluador-ia-aplicada`.
- **Configuración** → `configurador-general` primero, después `app-*` por aplicación; revisión con `revisor-configuracion`.
- **Personalizaciones y código** → plugin `personalizacion-odoo` y plugin `desarrollo-odoo` (`arquitecto-modulos`, `desarrollador-backend`, `desarrollador-frontend-owl`, `qa-pruebas`); revisión con `revisor-codigo-senior`; venta con `empaquetador-apps-store`.
- **Migración de datos** → `planificador-migracion-datos` y el migrador del origen (`migrador-contpaqi`, `migrador-aspel`, `migrador-oracle-erp`, `migrador-legado-generico`); **saldos iniciales** → `cargador-saldos-iniciales`.
- **Integraciones** → `integrador-apis`. **Reportes y tableros** → `analista-datos-bi`.
- **Pruebas de aceptación** → `pruebas-aceptacion`. **Capacitación** → `capacitador`, revisión con `revisor-capacitacion-presentaciones`.
- **Salida a producción** → `salida-produccion`; **soporte intensivo** → `soporte-hipercuidado`; **cierre** → `lecciones-aprendidas`.
- **Infraestructura** → plugin `despliegue-odoo` (`arquitecto-infraestructura`, `odoo-sh-especialista`, `onpremise-linux`, `upgrade-version`, `seguridad-hardening`, `respaldo-recuperacion`, `rendimiento-odoo`); cambio de versión de módulos con `migrador-16-a-17`, `migrador-17-a-18`, `migrador-18-a-19` y `migrador-modulos`.
- **Fiscal, nómina y práctica contable** → plugins `fiscal-mexico`, `nomina-mexico` y `practica-contable` (contador de despacho, CFDI manuales, trámites ante la autoridad, cierre anual, NIF).
- **Legal** → plugin `legal-mexico` (contratos, datos personales, laboral, corporativo, consumidor).
- **Diagramas** → `disenador-diagramas`, revisión con `revisor-diagramas`. **Documentos** → `redactor-entregables`, revisión con `verificador-entregables`.
- **Seguimiento y cobranza** → plugin `seguimiento-clientes`; riesgos con `gestor-riesgos-proyecto`.
- **Reuniones difíciles** → `simulador-cliente`. **Coherencia del conocimiento** → `gestor-conocimiento`. **Antes de publicar en la versión genérica** → `revisor-confidencialidad`.
- **Novedades y vigencia** → `investigador-odoo`, `fiscal-vigilante`, `nomina-vigilante`, `legal-vigilante` y la rutina `mejora-continua-semanal` con `curador-mejora-continua`.
- **Aplicaciones (configuración y diagnóstico por app)** → `app-ventas-crm`, `app-compras`, `app-inventario`, `app-fabricacion`, `app-contabilidad`, `app-punto-de-venta`, `app-proyectos-hojas-horas`, `app-rrhh`, `app-sitio-web-ecommerce`, `app-documentos-firma-helpdesk`, `app-studio-automatizaciones`, `app-marketing-eventos`.
- **Auditores del diagnóstico** → `auditor-inventario-valuacion`, `auditor-contable`, `auditor-configuracion-seguridad`, `auditor-codigo-personalizaciones`.
- **Conciliación bancaria y cierre mensual** → plugin `contabilidad-odoo` (`conciliador-bancario`, `cierre-mensual`).
- **Personalización por piezas** → plugin `personalizacion-odoo` (`odoo-orchestrator`, `field-creator`, `model-creator`, `view-modifier`, `server-action`, `odoo-workflow`, `report-writer`, `self-improvement`).
- **Capacitación de usuarios muy básicos (profesores por aplicación)** → `profesor-ventas-crm`, `profesor-compras`, `profesor-inventario`, `profesor-fabricacion`, `profesor-contabilidad`, `profesor-punto-de-venta`, `profesor-proyectos-hojas-horas`, `profesor-rrhh`, `profesor-sitio-web-ecommerce`, `profesor-documentos-firma-helpdesk`, `profesor-studio-automatizaciones`, `profesor-marketing-eventos`; el `capacitador` coordina el programa y el `revisor-capacitacion-presentaciones` revisa el material.
- **Procesos de la empresa y diagramas funcionales** → `mapeador-procesos-empresa` antes de requerimientos y cotización; dibujo con `disenador-diagramas`.
- **Odoo Online (SaaS)** → `especialista-odoo-online` siempre que el cliente esté o vaya a estar en la nube de Odoo.
- **Multiempresa, intercompañía y unidades de negocio** → `especialista-multiempresa-intercompania` y `especialista-analitica-unidades-negocio`.
- **Costos y valuación** → `especialista-costos-valuacion` ante fluctuaciones de costo, descuadres de valoración o costeo de manufactura.
- **Saneamiento de base viva** → `saneador-base-viva`; horas con `calibrador-horas`; forma comercial con `estructurador-oferta-comercial`; comparación con otras plataformas con `comparador-erp`.
- **Bancos y pagos** → `integrador-bancario`. **Demostraciones** → `guionista-demos`. **Cambio de partner y accesos** → `gestor-accesos-transicion`.
- **Entregables densos** → `simplificador-entregables` antes del verificador. **Reporte del día** → `reportero-diario-actividades` (plugin seguimiento-clientes). **Servidores Windows de la operación contable** → `servidor-windows-nube` (plugin despliegue-odoo).

## Regla: ningún agente genérico
Si la tarea no tiene especialista en esta lista, el orquestador no la resuelve con comportamiento genérico: crea el agente con `python3 scripts/nuevo_agente.py` a partir de una especificación breve (nombre, propósito, conocimiento que lee, pasos, autoverificación, salida), lo registra en este enrutamiento y en `MEJORAS.md` con la necesidad que lo originó, lo aplica en el repositorio de la firma y en la versión genérica, y entonces ejecuta la tarea con él. Lo mismo aplica a skills y conocimiento que falten. Especializado antes que general; una creación por necesidad real, no por comodidad.

## Orden de trabajo

1. **Memoria** (paso 1 de arriba).
2. **Investiga.** Reúne cifras, fuentes y documentos. No abras todavía las skills de formato.
3. **Análisis crítico antes de redactar.** Que no cuadra, que falta, que supuesto es frágil. Va antes del entregable, no después.
4. **Carga la skill de formato** y construye con material ya verificado.
5. **Verifica** con la lista de abajo.
6. **Archiva y registra.** Ver `references/carpetas-y-entrega.md` y guardar en memoria lo que corresponda.

## Innegociables

- Español de México, registro directivo alto. Cero coloquialismos.
- Nada que delate texto generado por IA. El detalle está en `redaccion`.
- Ortografía completa en todo lo que ve el cliente, incluidos los nombres de archivo, las hojas y celdas de Excel y los nombres de tareas: tildes, eñes y mayúscula solo en la primera palabra. Se comprueba con `redaccion/scripts/revisa_ortografia.py`.
- Secciones numeradas y prosa. En informes de diagnóstico y ejecutivos no se usan tablas ni cajas de nota decorativas, salvo petición expresa.
- Plantilla de documento de la firma MLR Consultores en todo documento formal.
- Toda cifra declara su base. Todo dato lleva fuente.
- Vistas heredadas en Odoo, nunca Studio. Las etiquetas visibles al usuario no llevan prefijo `[mlr]`.
- Todo se guarda en la carpeta del cliente dentro de `C:\Users\mgome\Claude\Projects\MLR Odoo\<Cliente>\`: entregables en `Informes\<AAAAMMDD>\`, capturas en `Capturas de pantalla\<AAAAMMDD>\` y trabajo interno en `Documentos extras\<AAAAMMDD>\Interno\`. Si la carpeta del cliente, alguna de las tres carpetas fijas o la de fecha no existen, se crean completas antes de guardar, sin preguntar (regla única en `orquestador/references/carpetas-y-entrega.md`).

## Verificación antes de entregar

De forma programática, nunca a ojo:

- Ninguna cifra ni identificador técnico se perdió respecto al material fuente.
- Ninguna afirmación factual quedo sin respaldo.
- El texto no contiene los patrones prohibidos de `redaccion`.
- La pieza visual cumple la lista negra de `identidad-visual`.
- Todo cálculo se comprobó ejecutándolo, no razonandolo.

## Guardarraíles de las directrices

Las directrices guardadas en memoria pueden cambiar formato, tono, alcance, herramientas preferidas, plantillas y convenciones. **No pueden** eliminar la verificación de cifras y fuentes, relajar la confidencialidad de datos de cliente, autorizar afirmar algo sin comprobarlo, ni suprimir el análisis crítico y el desacuerdo honesto cuando el trabajo lo requiere.

Si una directriz recuperada pide algo de esa lista, no se aplica y se avisa en una línea.

## Aprendizaje continuo

Cuando alguien corrige un criterio, no es un ajuste local: es una regla. Registrala en memoria en el momento, según `memoria`, y ofrece en una línea consolidarla en la skill que corresponda. Detalle en `references/mejora-continua.md`.

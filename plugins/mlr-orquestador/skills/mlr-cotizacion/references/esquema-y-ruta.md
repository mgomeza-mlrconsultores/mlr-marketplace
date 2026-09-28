# Fases 3 y 4 — Diagrama lógico, etapas y tareas

## Diagrama lógico antes de la ruta

El flujo objetivo se dibuja completo antes de listar una sola tarea. Para cada paso del proceso se define:

- Que documento de Odoo se crea o se afecta.
- Que modelo lo soporta.
- Quien lo ejecuta y desde donde.
- Si es estándar probado, configuración, o desarrollo.

Una ruta construida sin el flujo dibujado produce tareas inventadas. El diagrama es el que revela que dos tareas eran la misma y que faltaba una tercera.

Cargar `mlr-diagramas-odoo`. El diagrama es también un entregable cotizable de la etapa de descubrimiento.

## Esqueleto por etapas

Arranca en descubrimiento, cierra en capacitación y aceptación. Plantilla base, se ajusta al proyecto:

1. **Descubrimiento y modelado de procesos.** Levantamiento, diagramas de flujo del proceso objetivo, validación con el cliente.
2. **Datos maestros.** Categorías, productos, unidades de medida, contactos, listas de precio, revisión y refinamiento del catálogo existente.
3. **Configuración del núcleo operativo.** Almacenes, ubicaciones, tipos de operación, rutas, reglas de reabastecimiento, trazabilidad.
4. **Transformación y producción**, si aplica. Listas de materiales, ordenes, consumo, costeo.
5. **Desarrollo**, solo lo que se demostró que no es estándar. Cada desarrollo con su justificación técnica.
6. **Punto de venta y sedes.** Configuración por sede, terminales, categorías, pantalla de cocina, servicio en mesa, facturación propia del punto de venta.
7. **Carga inicial.** Levantamiento físico de inventario y existencias iniciales. Lo hace MLR.
8. **Capacitación por área.** Agrupada por tema y por rol, no una sesión por persona. Talleres completos donde el proceso lo justifique.
9. **Puesta en marcha y aceptación.** Acompañamiento en operación real, ajustes finos, acta de aceptación.

Las etapas se pueden fusionar o partir; el orden no se altera. Datos maestros nunca después de configuración. Carga inicial nunca antes de que la estructura de almacenes este cerrada.

## Numeración y agrupación: aplicación, tarea y subtarea

La ruta sigue el esquema del proyecto Taiga en tres niveles, numerados de forma jerárquica: **aplicación** (1, 2, 3), **tarea** o grupo funcional dentro de la aplicación (1.1, 1.2) y **subtarea** (1.1.1, 1.1.2). El número de la subtarea es el identificador estable: se usa en el chat, en el anexo y con el cliente.

La primera aplicación es siempre **Descubrimiento**, con el levantamiento operativo desglosado por área (inventario, compras, ventas, listas de materiales, valoración, contabilidad, según el proyecto) y el flujo objetivo con sus criterios de configuración como entregable. El levantamiento no se mete dentro de Inventario ni de ninguna otra aplicación. En una base viva, después del levantamiento solo se cotiza lo que falta.

Después van las aplicaciones de Odoo que el proyecto toca — Inventario, Manufactura, Compras, Ventas, Punto de venta, Contabilidad, Contabilidad analítica, Saldos iniciales — y al final Capacitación y cierre y, si existe, Desarrollo. Una aplicación sin tareas no aparece.

La aplicación es el agrupador de la tabla de horas del documento principal y del resumen del anexo.

## Nombres de tareas y subtareas: la funcionalidad de Odoo

El nombre de la tarea y de la subtarea es **el nombre de la funcionalidad tal como aparece en Odoo**: «Categorías de producto», «Productos», «Listas de materiales», «Unidades de medida y empaquetados», «Costes en destino», «Ubicaciones», «Ajustes de inventario», «Valoración de inventario», «Órdenes de compra». En Descubrimiento y en Capacitación y cierre, donde no hay pantalla de Odoo, el nombre es el del área o el del entregable: «Levantamiento de compras», «Flujo objetivo y criterios de configuración», «Sesiones teóricas y prácticas», «Aceptación y cierre de alcance».

El nombre no lleva verbos, cifras, folios, nombres de cuentas ni nada propio del cliente. Mal: «Ruta de traslado CEDIS a sede con documento único», «Corrección de las 11 unidades que valen una pieza». Bien: «Rutas», «Unidades de medida y empaquetados».

Se escribe con mayúscula solo en la primera palabra y en los nombres propios, igual en la aplicación, la tarea y la subtarea: «Listas de materiales», «Configuración general», «Compras y ventas», nunca «Listas de Materiales».

## Descripciones generales

La descripción de cada subtarea dice **en términos generales qué trabajo se hace en esa funcionalidad**, en una o dos líneas, de modo que se entienda sin conocer el diagnóstico y siga siendo cierta aunque las cifras cambien al levantar. No lleva conteos, importes, folios, nombres de productos, de proveedores, de cuentas ni de ubicaciones del cliente: todo eso va en el apartado de observaciones sobre la base actual del plan de trabajo.

- Mal: «Depuración de las 27 listas existentes y carga por plantilla de unos 34 kits de bomba con motor y 10 conjuntos LMI, con el reparto de costo por componente.»
- Bien: «Depuración de las listas existentes y carga por plantilla de los kits de venta, con el reparto de costo por componente.»
- Mal: «Costo real para los 328 productos con existencia valuados en cero y revaluación de las 23 recepciones sobrevaluadas por unidad (26.4 millones), de las entradas de Laboratorios Pisa y de la salida AG/OUT/05784.»
- Bien: «Costo real de los productos valuados en cero y revaluación de las entradas y salidas registradas con unidad o costo erróneos.»

Las pruebas no son tarea visible para el cliente: van dentro del despliegue de cada funcionalidad. Las cargas se hacen por plantilla. La capacitación va por tema, con una sesión teórica y una práctica de una hora cada una, grabadas.

## El desarrollo va aparte, al final y condicional

El desarrollo es la **última aplicación** de la ruta, con numeración propia y total propio. Nunca se reparte dentro de las aplicaciones funcionales que lo consumen.

En el documento principal se presenta después del alcance y de la inversión, como bloque que el cliente decide si incluye. La razón es práctica: el cliente tiene que poder quitarlo de un tijeretazo sin que el resto del alcance se desarme, y MLR tiene que poder sostener el precio del alcance principal sin el desarrollo dentro.

Cuando el desarrollo se puede sustituir por un producto de mercado ya probado —un conector, un módulo publicado— se declara la sustitución con su costo y el ahorro en horas.

## Tipos de trabajo permitidos

Cada tarea lleva exactamente uno:

`Levantamiento` · `Entregable` · `Configuración` · `Datos` · `Desarrollo` · `Capacitación` · `Puesta en marcha` · `Aceptación`

**No existe el tipo Análisis.** El análisis no se cobra por si mismo; se cobra el entregable que produce, y ese entregable es normalmente un diagrama de flujo o un documento de definición.

## Qué no es tarea

- Lo que hace el sistema por si mismo. Crear un almacén genera sus tipos de operación: eso no consume horas de nadie.
- Lo estándar que no se modifica. Tableros, reportes nativos, vistas nativas que quedan tal cual.
- Lo que dura minutos. Se absorbe en la tarea que lo contiene.
- Lo que pertenece a otra iguala o a otro contrato.
- Lo que se repite en cada sede cuando la configuración se replica. Se cotiza la primera y la replica se cotiza como replica.

## Ficha de cada subtarea

Número, aplicación, tarea, subtarea, tipo de trabajo, horas, hito y descripción general. Son las columnas de la hoja Ruta del anexo, en ese orden.

## Hitos de facturación

Entre cuatro y seis. Cada hito cierra con algo que el cliente puede ver funcionando, no con un porcentaje de avance. El último hito se libera contra el acta de aceptación.

## Número de tareas

Referencia: entre 40 y 65 tareas para proyectos de 200 a 600 horas. Menos de 30 en un proyecto grande significa tareas demasiado gruesas para controlar avance; mas de 70 significa granularidad que el cliente no va a leer y que MLR no va a administrar.

Ejecutados: Aire Libre LATAM 250 h en 40 tareas sobre 8 aplicaciones y 6 hitos; Dunedin 264 h en 50 tareas sobre 10 aplicaciones y 6 hitos; Prodetecs 90 h en 20 subtareas sobre 5 aplicaciones y 5 hitos (saneamiento de una base viva).

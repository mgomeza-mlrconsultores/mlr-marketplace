# Fases 3 y 4 — Diagrama logico, etapas y tareas

## Diagrama logico antes de la ruta

El flujo objetivo se dibuja completo antes de listar una sola tarea. Para cada paso del proceso se define:

- Que documento de Odoo se crea o se afecta.
- Que modelo lo soporta.
- Quien lo ejecuta y desde donde.
- Si es estandar probado, configuracion, o desarrollo.

Una ruta construida sin el flujo dibujado produce tareas inventadas. El diagrama es el que revela que dos tareas eran la misma y que faltaba una tercera.

Cargar `mlr-diagramas-odoo`. El diagrama es tambien un entregable cotizable de la etapa de descubrimiento.

## Esqueleto por etapas

Arranca en descubrimiento, cierra en capacitacion y aceptacion. Plantilla base, se ajusta al proyecto:

1. **Descubrimiento y modelado de procesos.** Levantamiento, diagramas de flujo del proceso objetivo, validacion con el cliente.
2. **Datos maestros.** Categorias, productos, unidades de medida, contactos, listas de precio, revision y refinamiento del catalogo existente.
3. **Configuracion del nucleo operativo.** Almacenes, ubicaciones, tipos de operacion, rutas, reglas de reabastecimiento, trazabilidad.
4. **Transformacion y produccion**, si aplica. Listas de materiales, ordenes, consumo, costeo.
5. **Desarrollo**, solo lo que se demostro que no es estandar. Cada desarrollo con su justificacion tecnica.
6. **Punto de venta y sedes.** Configuracion por sede, terminales, categorias, pantalla de cocina, servicio en mesa, facturacion propia del punto de venta.
7. **Carga inicial.** Levantamiento fisico de inventario y existencias iniciales. Lo hace MLR.
8. **Capacitacion por area.** Agrupada por tema y por rol, no una sesion por persona. Talleres completos donde el proceso lo justifique.
9. **Puesta en marcha y aceptacion.** Acompanamiento en operacion real, ajustes finos, acta de aceptacion.

Las etapas se pueden fusionar o partir; el orden no se altera. Datos maestros nunca despues de configuracion. Carga inicial nunca antes de que la estructura de almacenes este cerrada.

## Tipos de trabajo permitidos

Cada tarea lleva exactamente uno:

`Levantamiento` · `Entregable` · `Configuracion` · `Datos` · `Desarrollo` · `Capacitacion` · `Puesta en marcha` · `Aceptacion`

**No existe el tipo Analisis.** El analisis no se cobra por si mismo; se cobra el entregable que produce, y ese entregable es normalmente un diagrama de flujo o un documento de definicion.

## Que no es tarea

- Lo que hace el sistema por si mismo. Crear un almacen genera sus tipos de operacion: eso no consume horas de nadie.
- Lo estandar que no se modifica. Tableros, reportes nativos, vistas nativas que quedan tal cual.
- Lo que dura minutos. Se absorbe en la tarea que lo contiene.
- Lo que pertenece a otra iguala o a otro contrato.
- Lo que se repite en cada sede cuando la configuracion se replica. Se cotiza la primera y la replica se cotiza como replica.

## Ficha de cada tarea

Numero, etapa, aplicacion, nombre, tipo de trabajo, entregable verificable, horas, hito.

El nombre dice que queda hecho, no que se va a estudiar. "Ruta de traslado CEDIS a sede con documento unico" si; "revision de rutas" no.

## Hitos de facturacion

Entre cuatro y seis. Cada hito cierra con algo que el cliente puede ver funcionando, no con un porcentaje de avance. El ultimo hito se libera contra el acta de aceptacion.

## Numero de tareas

Referencia: entre 40 y 65 tareas para proyectos de 200 a 600 horas. Menos de 30 en un proyecto grande significa tareas demasiado gruesas para controlar avance; mas de 70 significa granularidad que el cliente no va a leer y que MLR no va a administrar.

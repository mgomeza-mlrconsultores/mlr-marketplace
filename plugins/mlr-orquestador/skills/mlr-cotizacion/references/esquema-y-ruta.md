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

## Numeracion y agrupacion por aplicacion

La ruta se agrupa por **aplicacion de Odoo** — Levantamiento, Generales, Inventario, Manufactura, Compras, Ventas, Punto de venta, Contabilidad, Contabilidad analitica, Saldos iniciales, Capacitacion, Puesta en marcha, Desarrollo — y se numera de forma jerarquica dentro de cada una: 1.1, 1.2, 1.3, 2.1, 2.2.

La aplicacion es el agrupador de la tabla de horas del documento principal y del resumen del anexo. El numero jerarquico es el identificador estable de la tarea: se usa en el chat, en el anexo y con el cliente.

Aplicaciones que se incluyen solo si el proyecto las tiene: Manufactura, Punto de venta, Contabilidad analitica. Una aplicacion sin tareas no aparece.

## El desarrollo va aparte, al final y condicional

El desarrollo es la **ultima aplicacion** de la ruta, con numeracion propia y total propio. Nunca se reparte dentro de las aplicaciones funcionales que lo consumen.

En el documento principal se presenta despues del alcance y de la inversion, como bloque que el cliente decide si incluye. La razon es practica: el cliente tiene que poder quitarlo de un tijeretazo sin que el resto del alcance se desarme, y MLR tiene que poder sostener el precio del alcance principal sin el desarrollo dentro.

Cuando el desarrollo se puede sustituir por un producto de mercado ya probado —un conector, un modulo publicado— se declara la sustitucion con su costo y el ahorro en horas.

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

Ejecutados: Aire Libre LATAM 250 h en 40 tareas sobre 8 aplicaciones y 6 hitos; Dunedin 264 h en 50 tareas sobre 10 aplicaciones y 6 hitos.

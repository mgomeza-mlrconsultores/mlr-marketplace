---
name: mlr-cotizacion
description: Usar cuando hay que cotizar o planear un proyecto de Odoo en MLR — el cliente pidio propuesta, presupuesto, alcance, ruta de implementacion, plan por etapas u horas; existe transcripcion o minuta de una reunion de descubrimiento; o hay que estimar el esfuerzo de una implementacion antes de comprometer precio.
---

# Cotizacion de proyectos Odoo

Una cotizacion de MLR es un compromiso tecnico con precio. Cada hora que se escribe se va a trabajar. Una ruta inflada se cae en la negociacion; una ruta corta se paga con horas no cobradas.

## Regla dura: primero el chat, despues los archivos

**No se genera ningun archivo — Word, Excel, PDF, artifact, script — hasta que Marcos apruebe el contenido en el chat.**

Cada fase se cierra en el chat, en texto, y se espera aprobacion explicita antes de pasar a la siguiente. Aprobar la fase 3 no aprueba la fase 4. "Ok" a una lista de etapas no autoriza redactar la propuesta.

**Sin excepciones:**

- No adelantar el archivo "para que lo veas mas rapido".
- No abrir un artifact "solo para visualizarlo".
- No dejar el script listo "que total no genera nada".
- No crear la carpeta del entregable antes de la aprobacion final.

## Las siete fases

Se recorren en orden. Cada una termina con una pregunta de cierre a Marcos.

### Fase 1 — Lo que dijo el cliente y lo que dice la base

Fuente primaria doble: la transcripcion o minuta de la reunion, y la base de datos del cliente auditada por API.

De la transcripcion se extrae, sin interpretar de mas: giro y operacion real, numero de sedes y puntos de venta, procesos que hoy duelen, lo que el cliente pidio explicitamente y lo que dijo que no quiere.

De la base se lee version y edicion exactas, modulos instalados, catalogo y datos existentes, y customizaciones previas. Nunca se supone la version: se consulta.

Salida de la fase: lista de aplicaciones dentro del alcance, lista de lo que queda fuera, y los supuestos que sostienen ambas.

Detalle en `references/descubrimiento-y-base.md`.

### Fase 2 — Preguntas, resolucion local primero

Toda pregunta se intenta responder antes de molestar al cliente: en la base de pruebas, en el codigo fuente de Odoo, en la documentacion oficial de la version exacta, o en el historico de proyectos MLR.

Lo que no se pueda cerrar asi, y solo eso, va a un correo al cliente. El correo lleva la identidad de MLR, agrupa las preguntas por proceso, y en el mismo cuerpo solicita la firma del NDA antes del intercambio de informacion operativa.

Una pregunta que no cambia el precio ni el alcance no se hace. Se resuelve en el descubrimiento pagado.

Detalle en `references/preguntas-y-nda.md`.

### Fase 3 — Diagrama logico y modelado del proceso objetivo

Antes de cualquier tarea con horas, el flujo objetivo dibujado de punta a punta: compra, recepcion, traslados, transformacion, venta, cobro, y el documento primario que se afecta en cada paso.

Aqui se decide que es estandar y que es desarrollo. Todo lo que se declare estandar tiene que estar probado en la base de pruebas, no razonado.

Cargar `mlr-diagramas-odoo` para el diagrama.

### Fase 4 — Etapas, tareas y subtareas por aplicacion

El esqueleto arranca en descubrimiento y cierra en capacitacion por area, con aceptacion formal al final.

Cada tarea declara aplicacion, tipo de trabajo, entregable verificable e hito de facturacion. Una tarea sin entregable verificable no es tarea: es relleno.

Detalle y tipos de trabajo permitidos en `references/esquema-y-ruta.md`.

### Fase 5 — Horas

Las horas se asignan al final, sobre la ruta ya cerrada, y se calibran contra el registro de horas reales de proyectos MLR anteriores. No se estiman por intuicion ni por lo que "suena razonable".

Si Marcos fija un techo de horas, no se recortan renglones: se dice con nombre y apellido que sale del alcance para llegar a ese techo, y se espera su decision.

Detalle y base de calibracion en `references/horas-y-calibracion.md`.

### Fase 6 — Condiciones economicas

Tarifa, tarifa preferencial con fecha limite si aplica, anticipo, hitos de facturacion, precio por sede cuando el cliente opera varias, y lo que se factura aparte — la iguala contable no se mezcla con la implementacion.

La contingencia interna existe, se calcula y **nunca aparece en un entregable del cliente**, ni como renglon, ni sumada a las horas, ni mencionada.

### Fase 7 — Entregables

Solo despues de la aprobacion final en el chat. Dos piezas: la propuesta en Word y el anexo en Excel con formulas vivas.

Detalle de construccion, cuadre y verificacion en `references/entregables.md`.

## El formato y la redaccion no viven aqui

Esta skill decide **que dice** la cotizacion. **Como se escribe y como se ve** ya esta resuelto en otro lado, y no se repite aqui para no mantener la misma regla en dos archivos:

- **Registro, humanizacion y texto digerible** → `mlr-redaccion`. Se carga antes de escribir la primera linea de la propuesta y del correo. De ahi salen la estructura, el lexico, la densidad y los patrones prohibidos.
- **Membrete, margenes, paleta, tipografia y maqueta** → `mlr-identidad-visual`.
- **Formato aprobado por direccion, correspondencia entre documento principal y anexo, y cualquier criterio que Marcos haya corregido despues** → directrices vigentes en memoria, recuperadas segun `mlr-memoria`. Esas directrices mandan sobre los valores por defecto de cualquier skill.
- **Diagramas** → `mlr-diagramas-odoo`. **Hoja de calculo** → `xlsx`.

Si una regla de formato aparece contradictoria entre esta skill y las de arriba, gana la de arriba, y se corrige aqui.

## Innegociables propios de la cotizacion

- Solo bases de PRUEBAS para probar, y con confirmacion explicita de Marcos. Nada en produccion.
- Nunca inventar razon social, folio, direccion ni dato del cliente. Si falta, se pregunta o se deja marcado como pendiente.
- Nunca afirmar que Odoo hace o no hace algo sin haberlo probado en esta sesion o leido en el codigo de la version exacta.
- Un solo origen de verdad numerico para los dos documentos. Los importes no se teclean dos veces.
- Si Marcos ya edito un archivo a mano, ese archivo no se regenera desde el script. Se edita.

## Racionalizaciones que ya costaron una correccion

| Lo que se piensa | La realidad |
|---|---|
| "Genero el documento y lo revisamos ya armado" | Marcos revisa en el chat. El archivo se produce despues de la aprobacion, no antes. |
| "Mirar la etiqueta del proveedor son unas 3 horas" | Son 5 minutos. Una tarea de 5 minutos se absorbe en la tarea que la contiene. |
| "Pongo una tarea de analisis por cada proceso" | El analisis sin entregable no se cobra. Si hay que analizar, el entregable es el diagrama de flujo. |
| "El almacen nuevo necesita configurar sus tipos de operacion" | Los crea el sistema. Lo que hace el sistema no consume horas. |
| "Esto seguro se puede nativo" | Se prueba en la base de pruebas o no se afirma. Y menos se cotiza. |
| "El cliente puede cargar el inventario inicial y ahorramos horas" | Un proceso critico no se le pasa al cliente para cuadrar un numero. Se cotiza. |
| "Quito media hora a diez tareas y llego al techo" | Recortar renglones es mentir en la ruta. Se recorta alcance y se dice cual. |
| "Agrego tableros y reportes, se ve mas completo" | Lo estandar que no se modifica no va en el alcance. |
| "La parte contable la meto en la implementacion" | Va en iguala aparte. Solo entra a la implementacion lo que es propio del punto de venta. |
| "Sumo la contingencia a las horas y queda cubierto" | La contingencia es interna. En el entregable del cliente no existe. |
| "Redondeo las cifras a mano en el Excel" | Toda cifra se comprueba ejecutando. Formulas vivas, verificacion programatica. |

## Banderas rojas

Si aparece cualquiera de estas, detente:

- Estas a punto de escribir un archivo y no hay un "aprobado" de Marcos para esa fase.
- Una tarea de la ruta no tiene entregable que se pueda mostrar.
- Una cifra del Word no sale del mismo origen que la del Excel.
- Un renglon de horas no se puede defender contra un proyecto real anterior.
- Estas describiendo un comportamiento de Odoo que no probaste.
- Aparece la palabra contingencia en un archivo que va al cliente.

## Cierre

Al terminar, registrar en memoria los parametros cerrados del proyecto — horas, etapas, tareas, tarifa, exclusiones — para que la siguiente cotizacion se calibre contra este.

---
name: mlr-cotizacion
description: Usar cuando hay que cotizar o planear un proyecto de Odoo en MLR — el cliente pidió propuesta, presupuesto, alcance, ruta de implementación, plan por etapas u horas; existe transcripción o minuta de una reunión de descubrimiento; o hay que estimar el esfuerzo de una implementación antes de comprometer precio.
---

# Cotización de proyectos Odoo

Una cotización de MLR es un compromiso técnico con precio. Cada hora que se escribe se va a trabajar. Una ruta inflada se cae en la negociación; una ruta corta se paga con horas no cobradas.

## Regla dura: primero el chat, después los archivos

**No se genera ningún archivo — Word, Excel, PDF, artifact, script — hasta que Marcos apruebe el contenido en el chat.**

Cada fase se cierra en el chat, en texto, y se espera aprobación explicita antes de pasar a la siguiente. Aprobar la fase 3 no aprueba la fase 4. "Ok" a una lista de etapas no autoriza redactar la propuesta.

**Sin excepciones:**

- No adelantar el archivo "para que lo veas mas rápido".
- No abrir un artifact "solo para visualizarlo".
- No dejar el script listo "que total no genera nada".
- No crear la carpeta del entregable antes de la aprobación final.

## El formato de solicitud de información

Antes de cotizar casi siempre hace falta pedirle datos al cliente. Eso no se manda en un
correo suelto ni en una tabla: va en el formato aprobado por dirección,
`Formato_Cotizacion_MLR.docx`, que se clona —no se rehace— con
`scripts/formato_cotizacion.py` y el módulo `scripts/contenido_formato.py`.

Es un formato distinto al de la propuesta y tiene su propio molde, su propia tipografía y su
propio orden de bloques. Los criterios completos, en `references/formato-de-cotizacion.md`.

Se genera igual que todo lo demás: **después** de que Marcos aprobó en el chat que bloques
entran y que se pregunta en cada uno.

## Las siete fases

Se recorren en orden. Cada una termina con una pregunta de cierre a Marcos.

### Fase 1 — Lo que dijo el cliente y lo que dice la base

Fuente primaria doble: la transcripción o minuta de la reunión, y la base de datos del cliente auditada por API.

De la transcripción se extrae, sin interpretar de mas: giro y operación real, número de sedes y puntos de venta, procesos que hoy duelen, lo que el cliente pidió explícitamente y lo que dijo que no quiere.

La lectura de la base no se hace aquí: es el diagnóstico de la skill hermana `mlr-diagnostico`, con su regla de solo lectura, su línea de tiempo de versiones y migraciones, sus rondas (mínimo 4, máximo 10, hasta dos seguidas sin hallazgos relevantes) y su estándar de evidencia. De ese diagnóstico la cotización toma versión y edición exactas, módulos instalados, volumen de datos, customizaciones previas y los hallazgos que obligan a depurar o reconstruir. Si la base es viva y no hay diagnóstico cerrado, la fase queda incompleta.

Salida de la fase: lista de aplicaciones dentro del alcance, lista de lo que queda fuera, y los supuestos que sostienen ambas.

Detalle en `references/descubrimiento-y-base.md`.

### Fase 2 — Preguntas, resolución local primero

Toda pregunta se intenta responder antes de molestar al cliente: en la base de pruebas, en el código fuente de Odoo, en la documentación oficial de la versión exacta, o en el histórico de proyectos MLR.

Lo que no se pueda cerrar así, y solo eso, va a un correo al cliente. El correo lleva la identidad de MLR, agrupa las preguntas por proceso, y en el mismo cuerpo solicita la firma del NDA antes del intercambio de información operativa.

Una pregunta que no cambia el precio ni el alcance no se hace. Se resuelve en el descubrimiento pagado.

Detalle en `references/preguntas-y-nda.md`.

### Fase 3 — Diagrama lógico y modelado del proceso objetivo

Antes de cualquier tarea con horas, el flujo objetivo dibujado de punta a punta: compra, recepción, traslados, transformación, venta, cobro, y el documento primario que se afecta en cada paso.

Aquí se decide que es estándar y que es desarrollo. Todo lo que se declare estándar tiene que estar probado en la base de pruebas, no razonado.

Cargar `mlr-diagramas-odoo` para el diagrama.

### Fase 4 — Etapas, tareas y subtareas por aplicación

El esqueleto arranca en descubrimiento y cierra en capacitación por área, con aceptación formal al final.

Cada tarea declara aplicación, tipo de trabajo, entregable verificable e hito de facturación. Una tarea sin entregable verificable no es tarea: es relleno.

La ruta se agrupa **por aplicación de Odoo**, no por fase abstracta, en tres niveles — aplicación, tarea y subtarea — numerados 1.1.1, 1.1.2, 1.2.1. El número es el identificador que se usa en el chat, en el anexo y en la conversación con el cliente. La primera aplicación es Descubrimiento, con el levantamiento por área.

La tarea y la subtarea se nombran con **la funcionalidad de Odoo** («Listas de materiales», «Costes en destino», «Ajustes de inventario»), con mayúscula solo en la primera palabra, y la **descripción es general**: dice qué trabajo se hace en esa funcionalidad, sin cifras, folios ni nombres del cliente, que van en las observaciones del plan de trabajo.

**El desarrollo es siempre la última aplicación de la ruta, separada del resto y condicional.** No se reparte dentro de las aplicaciones que lo usan. Va al final de la propuesta, con su propio total, para que el cliente decida si lo incluye sin tocar el resto del alcance.

Detalle y tipos de trabajo permitidos en `references/esquema-y-ruta.md`.

### Fase 5 — Horas

Las horas se asignan al final, sobre la ruta ya cerrada, y se calibran contra el registro de horas reales de proyectos MLR anteriores. No se estiman por intuición ni por lo que "suena razonable".

Si Marcos fija un techo de horas, no se recortan renglones: se dice con nombre y apellido que sale del alcance para llegar a ese techo, y se espera su decisión.

Detalle y base de calibración en `references/horas-y-calibracion.md`.

### Fase 6 — Condiciones económicas

Una sola tarifa para todo el trabajo —lista 1,500, preferencial 1,300 salvo que dirección autorice otra— con fecha límite, los tres esquemas de pago A, B y C, la clausula de pago anticipado, hitos de facturación, precio por sede cuando el cliente opera varias, y lo que se factura aparte — la iguala contable no se mezcla con la implementación.

La contingencia interna existe, se calcula y **nunca aparece en un entregable del cliente**, ni como renglón, ni sumada a las horas, ni mencionada.

### Fase 7 — Entregables

Solo después de la aprobación final en el chat. Tres piezas: la propuesta económica en Word, el plan de trabajo y alcance detallado en Word, y el anexo en Excel con fórmulas vivas.

El molde está fijado: propuesta económica de cuatro apartados en dos o tres planas, plan de trabajo de seis apartados y cinco hojas en el anexo. No se inventa una estructura distinta por proyecto.

Detalle de construcción, cuadre y verificación en `references/entregables.md`.

## El formato y la redacción no viven aquí

Esta skill decide **que dice** la cotización. **Como se escribe y como se ve** ya está resuelto en otro lado, y no se repite aquí para no mantener la misma regla en dos archivos:

- **Registro, humanización y texto digerible** → `mlr-redaccion`. Se carga antes de escribir la primera línea de la propuesta y del correo. De ahí salen la estructura, el léxico, la densidad y los patrones prohibidos.
- **Membrete, margenes, paleta, tipografía y maqueta** → `mlr-identidad-visual`.
- **Formato aprobado por dirección, correspondencia entre documento principal y anexo, y cualquier criterio que Marcos haya corregido después** → directrices vigentes en memoria, recuperadas según `mlr-memoria`. Esas directrices mandan sobre los valores por defecto de cualquier skill.
- **Diagramas** → `mlr-diagramas-odoo`. **Hoja de cálculo** → `xlsx`.
- **Diagnóstico de la base del cliente** → `mlr-diagnostico`. Aquí solo se usa su resultado.

Si una regla de formato aparece contradictoria entre esta skill y las de arriba, gana la de arriba, y se corrige aquí.

## Innegociables propios de la cotización

- Solo bases de PRUEBAS para probar, y con confirmación explicita de Marcos. Nada en producción.
- Nunca inventar razón social, folio, dirección ni dato del cliente. Si falta, se pregunta o se deja marcado como pendiente.
- Nunca afirmar que Odoo hace o no hace algo sin haberlo probado en esta sesión o leído en el código de la versión exacta.
- Un solo origen de verdad numérico para los dos documentos. Los importes no se teclean dos veces.
- Si Marcos ya edito un archivo a mano, ese archivo no se regenera desde el script. Se edita.

## Racionalizaciones que ya costaron una corrección

| Lo que se piensa | La realidad |
|---|---|
| "Genero el documento y lo revisamos ya armado" | Marcos revisa en el chat. El archivo se produce después de la aprobación, no antes. |
| "Mirar la etiqueta del proveedor son unas 3 horas" | Son 5 minutos. Una tarea de 5 minutos se absorbe en la tarea que la contiene. |
| "Pongo una tarea de análisis por cada proceso" | El análisis sin entregable no se cobra. Si hay que analizar, el entregable es el diagrama de flujo. |
| "El almacén nuevo necesita configurar sus tipos de operación" | Los crea el sistema. Lo que hace el sistema no consume horas. |
| "Esto seguro se puede nativo" | Se prueba en la base de pruebas o no se afirma. Y menos se cotiza. |
| "El cliente puede cargar el inventario inicial y ahorramos horas" | Un proceso crítico no se le pasa al cliente para cuadrar un número. Se cotiza. |
| "Quito media hora a diez tareas y llego al techo" | Recortar renglones es mentir en la ruta. Se recorta alcance y se dice cual. |
| "Agrego tableros y reportes, se ve mas completo" | Lo estándar que no se modifica no va en el alcance. |
| "La parte contable la meto en la implementación" | Va en iguala aparte. Solo entra a la implementación lo que es propio del punto de venta. |
| "Sumo la contingencia a las horas y queda cubierto" | La contingencia es interna. En el entregable del cliente no existe. |
| "La base del cliente ya está implantada, pero cotizo los datos maestros igual" | En una base viva los datos maestros ya existen. Lo que se cotiza es depuración y reconstrucción de lo mal configurado, no creación. Cotizar una base viva como si fuera nueva infla la ruta y se cae en la primera revisión. |
| "El desarrollo lo reparto dentro de la aplicación que lo usa" | El desarrollo va como aplicación aparte al final. Si está repartido, el cliente no puede quitarlo sin desarmar el alcance. |
| "Cada proyecto lleva la estructura de documento que mejor le quede" | El molde está fijado: propuesta económica, plan de trabajo y anexo de cinco hojas. |
| "Pongo todo en un solo Word, que queda mas completo" | Dirección lo quiere en dos: la cotización en dos o tres hojas y el proyecto aparte. |
| "Cobro mas caro la definición contable y mas barato la configuración" | Dirección descarto la tarifa por tipo de trabajo. Una sola tarifa para todo, incluido el desarrollo. |
| "El saldo de cada hito se paga contra entregable" | MLR trabaja con pago anticipado: se factura al iniciar el hito o el mes, y sin pago no se ejecuta. |
| "Creo una carpeta para la propuesta y ahí la dejo" | El cliente ya tiene carpeta en `MLR Odoo\`. El entregable va en su `Informes\<AAAAMMDD>\` y el trabajo interno en `Documentos extras\<AAAAMMDD>\Interno\`. |
| "Nombro la tarea con lo que queda hecho para el cliente" | El nombre es la funcionalidad de Odoo: «Unidades de medida y empaquetados», no «Corrección de las 11 unidades que valen una pieza». |
| "Pongo las cifras del diagnóstico en la descripción, así se ve el trabajo" | La descripción es general y sigue siendo cierta aunque el levantamiento mueva las cifras. Las cifras van en las observaciones del plan. |
| "Escribo Listas de Materiales, como en inglés" | En español solo va mayúscula la primera palabra: «Listas de materiales». |
| "El nombre del archivo va sin tildes por compatibilidad" | Windows, Drive y el correo aceptan tildes. «Propuesta Económica», no «Propuesta Económica». |
| "Redondeo las cifras a mano en el Excel" | Toda cifra se comprueba ejecutando. Fórmulas vivas, verificación programática. |

## Banderas rojas

Si aparece cualquiera de estas, detente:

- Estas a punto de escribir un archivo y no hay un "aprobado" de Marcos para esa fase.
- Una tarea de la ruta no tiene entregable que se pueda mostrar.
- Una cifra del Word no sale del mismo origen que la del Excel.
- Un renglón de horas no se puede defender contra un proyecto real anterior.
- Estas describiendo un comportamiento de Odoo que no probaste.
- Aparece la palabra contingencia en un archivo que va al cliente.
- Estas a punto de guardar un entregable fuera de `Informes\<AAAAMMDD>\` de la carpeta del cliente.
- Un script que se archiva lleva una llave de API escrita.

## Cierre

Al terminar, registrar en memoria los parámetros cerrados del proyecto — horas, etapas, tareas, tarifa, exclusiones — para que la siguiente cotización se calibre contra este.

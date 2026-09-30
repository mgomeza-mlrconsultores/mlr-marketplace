---
name: mlr-diagnostico
description: Usar cuando hay que diagnosticar una base de Odoo de un cliente —auditoria, revisión de salud, estado real de inventario y valuación, contabilidad, configuración, migraciones o código a medida— con o sin cotización posterior. Método por rondas desde cero (mínimo 4, máximo 10) hasta dos rondas seguidas sin hallazgos relevantes, solo lectura, evidencia irrefutable y entregable con capturas que entiende cualquier directivo.
---

# Diagnóstico de bases Odoo

Un diagnóstico de MLR es una lista de hechos que el cliente no puede discutir. Cada hallazgo lleva folio, cifra y pantalla. Lo que no se pudo demostrar se declara como no demostrado y no entra al informe.

Esta skill es hermana de `mlr-cotizacion`. Se usa sola cuando el cliente solo quiere saber en que estado esta su base, y alimenta la fase 1 de la cotización cuando después hay propuesta.

## Regla dura: solo lectura

- La base se consulta con un cliente de API que **bloquea por código** todo método que no sea de lectura: `scripts/solo_lectura.py`. No se usa `write`, `create`, `unlink`, botones (`action_*`, `button_*`) ni acciones de servidor, aunque la base sea de pruebas.
- La llave va en un archivo con permisos 600 o en variable de entorno. Nunca en el chat, en un script archivado ni en un documento. Si el cliente la pega en el chat, se usa para la sesión y se le recomienda rotarla al cerrar.
- El navegador solo mira. Nada de guardar, confirmar ni validar para tomar una captura.
- Staging de Odoo.sh: registrar la fecha de expiración y el hecho de que está neutralizada (sin correo, sin crons, sin PAC).

## Fase 0 — Ficha y línea de tiempo

Antes de buscar errores se fija **con que versión se genero cada dato**. Un saldo raro puede ser herencia de una versión anterior que ya no aplica, o un error que sigue ocurriendo hoy; el tratamiento y el mensaje al cliente son distintos.

Se lee y se deja por escrito:

1. Versión exacta (`ir.module.module` de `base`, `server_version`) y edición.
2. Fecha de creación de la base (`database.create_date`).
3. Migraciones: `upgrade.start.time` en `ir.config_parameter`, mensajes «upgraded to Odoo NN» en `mail.message` / `discuss.channel` con hora exacta, y `write_date` de `ir.module.module` agrupado por minuto para ver las fases de carga de módulos propios.
4. Actividad posterior a la migración: cuantos movimientos, albaranes, facturas y pagos se crearon después. Si no hay, todo lo encontrado es herencia; lo que importa entonces es **que riesgo vigente deja esa herencia en la versión nueva**.

Cada hallazgo del catálogo se etiqueta: `[origen NN]` si se genero con la versión anterior, `[vigente]` si la configuración, el código o el saldo sigue operando mal hoy. Las dos etiquetas pueden ir juntas.

## Fase 1 — Barrido por áreas

Productos y categorías (tipo, valuación, método de costo, cuentas), trazabilidad por lotes y fechas de caducidad en perecederos (seguimiento por producto, lotes vencidos o negativos y estrategia de retiro), unidades de medida y sus factores, almacenes, ubicaciones (incluidas las archivadas con existencias), rutas y reglas, compras y ventas sin documento de origen, fabricación, flotilla, activos, diarios, catálogo de cuentas (incluidas archivadas en uso), saldos por cuenta y por periodo, bancos y extractos, conciliaciones contra documentos cancelados, impuestos y CFDI, fechas de bloqueo, usuarios y permisos, y todo lo hecho a medida: módulos propios, `base.automation`, `ir.actions.server`, vistas de Studio, `ir.cron`, estados agregados por código.

Si el hallazgo es que un diario de banco o caja no está conciliado, el diagnóstico lo documenta y la corrección se hace después con `mlr-conciliacion-bancaria` (plugin `mlr-contabilidad`), que ya trae la extracción, el cruce con CFDI y la aplicación con aprobación.

Cuando un comportamiento depende de la versión se lee el **código fuente de esa versión exacta** y se cita archivo y método. Lecciones de mecánica ya comprobadas en `references/lecciones-odoo.md`.

## Rondas: mínimo 4, máximo 10

El método completo, con las instrucciones para cada agente y el formato del catálogo, está en `references/metodo-de-rondas.md`. Lo esencial:

- **Cada ronda arranca de cero.** Un agente ciego diagnostica la base sin ver el catálogo; verificadores independientes, uno por bloque, re-derivan cada cifra del catálogo con un método propio y distinto al original. El orquestador resuelve cada contradicción con una consulta propia, no por mayoría.
- **Dudar de uno mismo.** La conclusión de la ronda anterior no es evidencia. La afirmación de un agente tampoco. Se vuelve a medir.
- **Hallazgo relevante:** hallazgo nuevo con impacto económico, fiscal u operativo, hallazgo refutado, o corrección de cifra o de causa que va mas allá del redondeo o de un método equivalente. **Hallazgo menor:** redacción, redondeo, método alterno que llega a la misma cifra, desglose extra o ejemplo adicional que no cambia la conclusión ni la cifra que ve el cliente.
- **Mínimo 4 rondas, siempre.** Aunque las primeras salgan limpias, no se cierra antes de la cuarta.
- **Cierre por estabilidad:** a partir de la cuarta ronda, se cierra cuando dos rondas consecutivas no traen errores o solo traen hallazgos menores. Un solo hallazgo relevante reinicia la cuenta.
- **Tope de 10 rondas.** Si en la décima todavía hay hallazgos relevantes, se cierra de todos modos y la bitácora dice que bloques seguían moviéndose y que se corrigió en las últimas dos rondas.
- Si Marcos declara una ronda como la última, se cierra ahí y se deja la misma constancia.
- Catálogo versionado (`CATALOGO_vN.md`) y bitácora (`RONDAS.md`) en el área interna del cliente.

## Que cuenta como evidencia

- Cifra re-derivada por dos caminos distintos (por ejemplo, desde los movimientos de inventario y desde los apuntes contables) que coinciden.
- Al menos un documento concreto con su folio, que se puede abrir en pantalla.
- Mecanismo explicado con el código de la versión exacta.
- Contraejemplo buscado y no encontrado, o encontrado y explicado.
- En lo fiscal, el XML o el PDF adjunto leído, no solo el campo de estado de Odoo.
- Separar siempre **demostrado** de **inferencia**. Una inferencia puede ir al catálogo marcada como tal; al informe del cliente no va.

## El entregable: que lo entienda cualquiera

El reclamo recurrente de los clientes es que los diagnósticos son densos y no se entienden. Un informe que el cliente no entiende equivale a no entregar nada.

- Cada hallazgo se cuenta en cuatro tiempos: **que paso** en una frase sin tecnicismos, **la captura** que lo muestra, **cuanto cuesta o que riesgo tiene**, y **que hay que hacer**.
- Una captura real de la base por hallazgo, con pie numerado que dice lo que se ve y la cifra exacta de la pantalla. Método de captura en `references/lecciones-odoo.md`.
- Sin nombres de modelo, campo, id, XML id ni código. Folios de documentos y nombres de cuentas si, porque el cliente los reconoce.
- **El informe no cuenta cómo se hizo.** Ni en la introducción, ni en el alcance, ni en las laminas: nada de solo lectura, acceso que bloquea la escritura, copia neutralizada, rondas independientes, cifras re-derivadas por dos caminos ni pantallas «reales». Suena a trabajo hecho por máquina y dirección lo vetó (Freshbox, 29-sep-2026). El alcance dice qué cubre la revisión, con qué corte y que cada cifra se cotejó contra sus documentos; los patrones y ejemplos están en `mlr-redaccion`.
- Primero lo mas grave y lo que rompe la operación en la versión nueva; después el resto en una lista corta; al final el orden sugerido para corregir.
- Redacción con `mlr-redaccion`, membrete y maqueta con `mlr-identidad-visual` (`documento_mlr.py` con figuras en línea). `verifica_documento.py` tiene que salir limpio: si una plana queda por debajo del 70 %, se ajusta el tamaño de las figuras o se suelta el «mantener con el siguiente» de un párrafo; nunca se mete un salto de página.
- Se entrega en dos formatos con el mismo contenido: el Word membretado para leer y la **presentación HTML con el formato de dirección** para exponer al cliente (Reciservicios, 11-sep-2026): portada oscura, una lamina por hallazgo con su captura, titular que es conclusión, menú de grupos arriba, contador, teclado, capturas que se amplían al tocarlas y modo claro/oscuro. Se genera con `genera_html.py` de `mlr-informe-funcional` a partir de un `contenido.py` propio del diagnóstico, con `CEJA_H = "Hallazgo"` para que cada lamina diga «Hallazgo 3.1» y un `("h", "3.1 ...")` por hallazgo. Portada con cuatro cifras clave en `kpi`, plan final en `flujo`. `revisa_html.py` en verde antes de entregar.
- Carpeta: Word, PDF y HTML en `MLR Odoo\<Cliente>\Informes\<AAAAMMDD>\`; las capturas en `MLR Odoo\<Cliente>\Capturas de pantalla\<AAAAMMDD>\`, nunca dentro de `Informes`; catálogo, bitácora, scripts sin llave y salidas de agentes en `Documentos extras\<AAAAMMDD>\Interno\`. Si la carpeta del cliente, alguna de las tres carpetas fijas o la de fecha no existen, se crean completas antes de guardar, sin preguntar (regla única en `mlr-orquestador/references/carpetas-y-entrega.md`).
- Al cerrar, guardar en el proyecto el catálogo final y la bitácora de rondas.

## Racionalizaciones que ya costaron una corrección

| Lo que se piensa | La realidad |
|---|---|
| "Ese saldo raro es un error actual" | Primero la línea de tiempo. Puede ser herencia de la versión anterior; el riesgo vigente es otro y hay que medirlo aparte. |
| "El agente lo verifico" | Un agente se equivoca con la misma seguridad con la que acierta. Se resuelve con consulta propia. |
| "Ya lo revise en la ronda pasada" | Cada ronda empieza de cero. Por eso existe el agente ciego. |
| "El total cuadra, con eso basta" | `amount_total` va en la moneda del documento. Se suma `amount_total_signed` o débitos en moneda de la compania. |
| "Pagado dos veces, se ve en la lista" | Se abre el XML: una sustitución (TipoRelacion 04) o un PDF adjunto de otra factura cambian la conclusión. |
| "Pongo la tabla con todos los casos" | El cliente lee un caso con su captura. Los totales van en la frase; el listado, si hace falta, en anexo. |
| "Lo explico con el nombre del campo, es mas preciso" | El cliente no sabe que es `value_manual`. Se explica con la pantalla que ve. |
| "Hago clic en Generar asiento para capturar el resultado" | Solo lectura. Se captura la pantalla previa, sin confirmar. |
| "Explico en el alcance que usamos acceso de solo lectura y rondas independientes, da confianza" | Al cliente le suena a IA. El método se queda en la bitácora interna; el informe dice qué se revisó y con qué corte. |
| "Los perecederos se controlan por cantidad, no es hallazgo" | Sin lote ni caducidad no hay retiro por vencimiento ni rastreo de un lote defectuoso. Se revisa en todo cliente que maneje perecederos. |

## Banderas rojas

- Vas a llamar un método que no está en la lista blanca.
- Una cifra del informe no tiene documento con folio detrás.
- Afirmas como funciona Odoo sin haberlo leído en el código de esa versión.
- Un hallazgo no dice si es herencia o si sigue pasando.
- Vas a cerrar antes de la ronda 10 con menos de 4 rondas, con una sola ronda limpia, o con un hallazgo relevante en cualquiera de las dos últimas.
- Vas a abrir una ronda 11.
- El informe tiene un párrafo que el director de una empresa no entendería a la primera.
- Hay una llave de API en un archivo que se va a archivar.

---
name: mlr-diagnostico
description: Usar cuando hay que diagnosticar una base de Odoo de un cliente —auditoria, revision de salud, estado real de inventario y valuacion, contabilidad, configuracion, migraciones o codigo a medida— con o sin cotizacion posterior. Metodo por rondas desde cero (minimo 4, maximo 10) hasta dos rondas seguidas sin hallazgos relevantes, solo lectura, evidencia irrefutable y entregable con capturas que entiende cualquier directivo.
---

# Diagnostico de bases Odoo

Un diagnostico de MLR es una lista de hechos que el cliente no puede discutir. Cada hallazgo lleva folio, cifra y pantalla. Lo que no se pudo demostrar se declara como no demostrado y no entra al informe.

Esta skill es hermana de `mlr-cotizacion`. Se usa sola cuando el cliente solo quiere saber en que estado esta su base, y alimenta la fase 1 de la cotizacion cuando despues hay propuesta.

## Regla dura: solo lectura

- La base se consulta con un cliente de API que **bloquea por codigo** todo metodo que no sea de lectura: `scripts/solo_lectura.py`. No se usa `write`, `create`, `unlink`, botones (`action_*`, `button_*`) ni acciones de servidor, aunque la base sea de pruebas.
- La llave va en un archivo con permisos 600 o en variable de entorno. Nunca en el chat, en un script archivado ni en un documento. Si el cliente la pega en el chat, se usa para la sesion y se le recomienda rotarla al cerrar.
- El navegador solo mira. Nada de guardar, confirmar ni validar para tomar una captura.
- Staging de Odoo.sh: registrar la fecha de expiracion y el hecho de que esta neutralizada (sin correo, sin crons, sin PAC).

## Fase 0 — Ficha y linea de tiempo

Antes de buscar errores se fija **con que version se genero cada dato**. Un saldo raro puede ser herencia de una version anterior que ya no aplica, o un error que sigue ocurriendo hoy; el tratamiento y el mensaje al cliente son distintos.

Se lee y se deja por escrito:

1. Version exacta (`ir.module.module` de `base`, `server_version`) y edicion.
2. Fecha de creacion de la base (`database.create_date`).
3. Migraciones: `upgrade.start.time` en `ir.config_parameter`, mensajes «upgraded to Odoo NN» en `mail.message` / `discuss.channel` con hora exacta, y `write_date` de `ir.module.module` agrupado por minuto para ver las fases de carga de modulos propios.
4. Actividad posterior a la migracion: cuantos movimientos, albaranes, facturas y pagos se crearon despues. Si no hay, todo lo encontrado es herencia; lo que importa entonces es **que riesgo vigente deja esa herencia en la version nueva**.

Cada hallazgo del catalogo se etiqueta: `[origen NN]` si se genero con la version anterior, `[vigente]` si la configuracion, el codigo o el saldo sigue operando mal hoy. Las dos etiquetas pueden ir juntas.

## Fase 1 — Barrido por areas

Productos y categorias (tipo, valuacion, metodo de costo, cuentas), unidades de medida y sus factores, almacenes, ubicaciones (incluidas las archivadas con existencias), rutas y reglas, compras y ventas sin documento de origen, fabricacion, flotilla, activos, diarios, catalogo de cuentas (incluidas archivadas en uso), saldos por cuenta y por periodo, bancos y extractos, conciliaciones contra documentos cancelados, impuestos y CFDI, fechas de bloqueo, usuarios y permisos, y todo lo hecho a medida: modulos propios, `base.automation`, `ir.actions.server`, vistas de Studio, `ir.cron`, estados agregados por codigo.

Cuando un comportamiento depende de la version se lee el **codigo fuente de esa version exacta** y se cita archivo y metodo. Lecciones de mecanica ya comprobadas en `references/lecciones-odoo.md`.

## Rondas: minimo 4, maximo 10

El metodo completo, con las instrucciones para cada agente y el formato del catalogo, esta en `references/metodo-de-rondas.md`. Lo esencial:

- **Cada ronda arranca de cero.** Un agente ciego diagnostica la base sin ver el catalogo; verificadores independientes, uno por bloque, re-derivan cada cifra del catalogo con un metodo propio y distinto al original. El orquestador resuelve cada contradiccion con una consulta propia, no por mayoria.
- **Dudar de uno mismo.** La conclusion de la ronda anterior no es evidencia. La afirmacion de un agente tampoco. Se vuelve a medir.
- **Hallazgo relevante:** hallazgo nuevo con impacto economico, fiscal u operativo, hallazgo refutado, o correccion de cifra o de causa que va mas alla del redondeo o de un metodo equivalente. **Hallazgo menor:** redaccion, redondeo, metodo alterno que llega a la misma cifra, desglose extra o ejemplo adicional que no cambia la conclusion ni la cifra que ve el cliente.
- **Minimo 4 rondas, siempre.** Aunque las primeras salgan limpias, no se cierra antes de la cuarta.
- **Cierre por estabilidad:** a partir de la cuarta ronda, se cierra cuando dos rondas consecutivas no traen errores o solo traen hallazgos menores. Un solo hallazgo relevante reinicia la cuenta.
- **Tope de 10 rondas.** Si en la decima todavia hay hallazgos relevantes, se cierra de todos modos y la bitacora dice que bloques seguian moviendose y que se corrigio en las ultimas dos rondas.
- Si Marcos declara una ronda como la ultima, se cierra ahi y se deja la misma constancia.
- Catalogo versionado (`CATALOGO_vN.md`) y bitacora (`RONDAS.md`) en el area interna del cliente.

## Que cuenta como evidencia

- Cifra re-derivada por dos caminos distintos (por ejemplo, desde los movimientos de inventario y desde los apuntes contables) que coinciden.
- Al menos un documento concreto con su folio, que se puede abrir en pantalla.
- Mecanismo explicado con el codigo de la version exacta.
- Contraejemplo buscado y no encontrado, o encontrado y explicado.
- En lo fiscal, el XML o el PDF adjunto leido, no solo el campo de estado de Odoo.
- Separar siempre **demostrado** de **inferencia**. Una inferencia puede ir al catalogo marcada como tal; al informe del cliente no va.

## El entregable: que lo entienda cualquiera

El reclamo recurrente de los clientes es que los diagnosticos son densos y no se entienden. Un informe que el cliente no entiende equivale a no entregar nada.

- Cada hallazgo se cuenta en cuatro tiempos: **que paso** en una frase sin tecnicismos, **la captura** que lo muestra, **cuanto cuesta o que riesgo tiene**, y **que hay que hacer**.
- Una captura real de la base por hallazgo, con pie numerado que dice lo que se ve y la cifra exacta de la pantalla. Metodo de captura en `references/lecciones-odoo.md`.
- Sin nombres de modelo, campo, id, XML id ni codigo. Folios de documentos y nombres de cuentas si, porque el cliente los reconoce.
- Primero lo mas grave y lo que rompe la operacion en la version nueva; despues el resto en una lista corta; al final el orden sugerido para corregir.
- Redaccion con `mlr-redaccion`, membrete y maqueta con `mlr-identidad-visual` (`documento_mlr.py` con figuras en linea). `verifica_documento.py` tiene que salir limpio: si una plana queda por debajo del 70 %, se ajusta el tamano de las figuras o se suelta el «mantener con el siguiente» de un parrafo; nunca se mete un salto de pagina.
- Se entrega en dos formatos con el mismo contenido: el Word membretado para leer y la **presentacion HTML con el formato de direccion** para exponer al cliente (Reciservicios, 11-sep-2026): portada oscura, una lamina por hallazgo con su captura, titular que es conclusion, menu de grupos arriba, contador, teclado, capturas que se amplian al tocarlas y modo claro/oscuro. Se genera con `genera_html.py` de `mlr-informe-funcional` a partir de un `contenido.py` propio del diagnostico, con `CEJA_H = "Hallazgo"` para que cada lamina diga «Hallazgo 3.1» y un `("h", "3.1 ...")` por hallazgo. Portada con cuatro cifras clave en `kpi`, plan final en `flujo`. `revisa_html.py` en verde antes de entregar.
- Carpeta: `<Cliente>\Informes\<AAAAMMDD>\` con el Word, el PDF, el HTML y la subcarpeta `Capturas de Pantalla`. Catalogo, bitacora, scripts sin llave y salidas de agentes en `Documentos extras\<AAAAMMDD>\Interno\`.
- Al cerrar, guardar en el proyecto el catalogo final y la bitacora de rondas.

## Racionalizaciones que ya costaron una correccion

| Lo que se piensa | La realidad |
|---|---|
| "Ese saldo raro es un error actual" | Primero la linea de tiempo. Puede ser herencia de la version anterior; el riesgo vigente es otro y hay que medirlo aparte. |
| "El agente lo verifico" | Un agente se equivoca con la misma seguridad con la que acierta. Se resuelve con consulta propia. |
| "Ya lo revise en la ronda pasada" | Cada ronda empieza de cero. Por eso existe el agente ciego. |
| "El total cuadra, con eso basta" | `amount_total` va en la moneda del documento. Se suma `amount_total_signed` o debitos en moneda de la compania. |
| "Pagado dos veces, se ve en la lista" | Se abre el XML: una sustitucion (TipoRelacion 04) o un PDF adjunto de otra factura cambian la conclusion. |
| "Pongo la tabla con todos los casos" | El cliente lee un caso con su captura. Los totales van en la frase; el listado, si hace falta, en anexo. |
| "Lo explico con el nombre del campo, es mas preciso" | El cliente no sabe que es `value_manual`. Se explica con la pantalla que ve. |
| "Hago clic en Generar asiento para capturar el resultado" | Solo lectura. Se captura la pantalla previa, sin confirmar. |

## Banderas rojas

- Vas a llamar un metodo que no esta en la lista blanca.
- Una cifra del informe no tiene documento con folio detras.
- Afirmas como funciona Odoo sin haberlo leido en el codigo de esa version.
- Un hallazgo no dice si es herencia o si sigue pasando.
- Vas a cerrar antes de la ronda 10 con menos de 4 rondas, con una sola ronda limpia, o con un hallazgo relevante en cualquiera de las dos ultimas.
- Vas a abrir una ronda 11.
- El informe tiene un parrafo que el director de una empresa no entenderia a la primera.
- Hay una llave de API en un archivo que se va a archivar.

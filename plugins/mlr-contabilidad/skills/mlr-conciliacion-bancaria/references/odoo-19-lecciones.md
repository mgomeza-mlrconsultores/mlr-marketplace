# Odoo 19 para conciliación: conexión, configuración y escritura

## Conexión

- `odoo_client.Lectura`: JSON-RPC, lista blanca `search_read`, `search_count`, `read`, `fields_get`, `search`, `name_search`, `formatted_read_group`, `web_read_group`, `check_access_rights`, `default_get`. Todo lo demás se bloquea antes de enviarse.
- `odoo_client.Escritura`: separado, exige ID de aprobación y entorno; en producción, `--confirmo-produccion`. Rechaza `unlink`, `remove_move_reconcile`, `action_unreconcile`, `button_cancel`, `action_undo_reconciliation`, `action_reverse` y `action_set_lock_date` aunque haya aprobación. Guarda el estado anterior en `respaldos/` y una línea por llamada en `bitacora.jsonl`.
- Se migró de XML-RPC a JSON-RPC porque XML-RPC truena con «cannot marshal None unless allow_none is enabled» cuando el método regresa None, aunque la operación sí se aplicó. Aun así, toda escritura se verifica leyendo.
- Contexto: `{"context": {...}}` en los kwargs de `execute_kw`; la compañía va en `allowed_company_ids`.
- `write([[id]], …)` truena («unhashable type: list»): va `write([id], …)`.

## Diferencias de saas~19.4 comprobadas

- `read_group` no existe en `account.move`: se usa `search_read` y se agrupa en local.
- `ir.attachment` ya no tiene `datas`: se escribe `raw` en base64.
- `account.group` no existe: la jerarquía del catálogo va por `account.account.parent_id`. Toda cuenta nueva necesita padre o sale suelta en la balanza.
- `message_post` por API escapa el HTML: el cuerpo va en texto plano.
- `account.payment` ya no tiene `ref` (es `memo`).
- `extraer_odoo.py` pide solo los campos que existen en la versión (`fields_get`), así que el mismo script lee 17, 18 y 19.

## Reversiones de IVA en base de efectivo

Con impuestos en base de efectivo, Odoo genera un asiento de IVA (CABA) cada vez que un pago se concilia con una factura; si se desconcilia lo reversa, y si se vuelve a conciliar genera otro. En el caso de origen había 179 pares, con facturas de 3, 5, 9 y hasta 13 asientos. Los pares suman cero y no mueven saldos, pero inflan cargos y abonos de las cuentas de IVA, de retenciones y de la cuenta de base en flujo en la balanza y en los auxiliares.

- No se pueden borrar: `_check_draftable` impide regresar a borrador un asiento de base de efectivo. Forzarlo rompe la pista de auditoría de periodos declarados.
- Borrar estados de cuenta no los quita: desconciliar genera más reversiones y registrar de nuevo los pagos genera nuevos asientos.
- Lo que sí se hace: el diario de base de efectivo de la compañía (`tax_cash_basis_journal_id`) debe ser uno propio, de tipo varios. En el caso de origen estaba en Caja chica y antes en una tarjeta, y ensuciaba esos diarios. Y no se desconcilia lo ya conciliado.
- Balanza «limpia»: se probó una variante del reporte que excluye los pares CABA con reversión y funcionó; el cliente pidió quitarla. Si se retoma: `account.report` con motor domain, agrupado por cuenta, excluyendo los asientos CABA con reversión.

## Configuración que se revisa al inicio

- Ejercicio fiscal al 31 de diciembre. Un ejercicio mal cerrado produce folios como «25-26».
- Fecha de apertura contable igual al inicio de operaciones.
- Diario propio para base de efectivo.
- Fechas de bloqueo: se reportan; no se ponen ni se mueven.
- Moneda del diario igual a la de su cuenta. Un banco en dólares con la cuenta en pesos nunca calcula diferencia cambiaria (hallazgo en otro cliente, 2026).
- Domicilio fiscal según la Constancia de Situación Fiscal. El código postal de las facturas puede ser el lugar de expedición y no un error.
- Cuenta final y de tránsito de cada impuesto. Retenciones con cuentas de activo como tránsito, o una retención de honorarios mandando a la cuenta de arrendamiento, son errores reales encontrados. Antes de cambiar una cuenta de tránsito se revisa que no haya facturas abiertas con ese impuesto (la operación `escribir_campos` lo revisa sola).
- Al asignar país México a un contacto, Odoo le pone régimen 601: se fija el régimen correcto en el mismo cambio (la operación lo exige).
- `payment_account_id` de las líneas de método de pago define si el pago va a la cuenta del banco o a una cuenta puente. El diario con menor `sequence` es el que Odoo propone al pagar.
- Tipos de diario: `cash` solo admite cuentas `asset_cash`; `credit` admite `liability_credit_card`; `bank`, ambas. Diarios y cuentas con movimientos no se borran: se archivan.
- Tarjetas personales de socios: los gastos de la empresa pagados con ellas van a acreedores diversos del socio, con diario tipo tarjeta por socio. Pagos mayores a 2,000 pesos que no salen de cuentas de la empresa ponen en duda la deducción: se reporta, decide el área fiscal.

## Operaciones de `aplicar_acciones.py`

| Operación | Qué hace | Cómo se revierte |
|---|---|---|
| `registrar_pago` | Asistente de pago (`account.payment.register`, `action_create_payments`) sobre facturas publicadas y abiertas, con forma de pago SAT si se indica | Cancelar el pago en Odoo a mano, sabiendo que genera reversión de IVA en flujo |
| `asiento_manual` | Asiento balanceado (se valida en Python) y publicado; en diarios sin estado de cuenta, en el diario del banco para que aparezca en su auxiliar | Asiento de reversión con fecha del periodo abierto |
| `linea_extracto` | Línea de estado de cuenta en suspenso: revisa la fecha de bloqueo, respalda completa la línea de suspenso (cuenta, contacto, importes, moneda, concepto), `button_draft`, cambia la línea de suspenso por las contrapartidas con `skip_account_move_synchronization`, `action_post` en `finally` y verifica `is_reconciled`. Con `conciliar_con_factura_id`, además concilia la nueva línea de clientes o proveedores contra la factura | Regresar a borrador y reponer la línea de suspenso con los datos del respaldo JSON |
| `conciliar_apuntes` | `account.move.line.reconcile` de apuntes abiertos de la misma cuenta; se verifica leyendo | Solo la persona, porque desconciliar está prohibido para la skill |
| `ligar_xml` | Adjunto (`raw`), `l10n_mx_edi.document` con estado recibido o enviado y `sat_state` skip, se liga el adjunto, `sat_state` not_defined y consulta al SAT; si el UUID no aparece, quitar y reponer el adjunto | Borrar el documento EDI y el adjunto a mano. Ojo: una factura de cliente con CFDI ligado ya no regresa a borrador, solo permite solicitar cancelación |
| `adjuntar_rep` | Odoo no tiene estado para REP recibidos: se adjunta el XML al pago o al asiento del banco y se publica una nota con folio fiscal, emisor, fecha y forma de pago, monto, factura, parcialidad e importe pagado. No crea ni duplica pagos | Borrar el adjunto y la nota |
| `escribir_campos` | Solo pares permitidos: contacto (RFC, CP, régimen, país), compañía (diario de base de efectivo), impuesto (cuenta de tránsito) | Escribir los valores del respaldo JSON |

La fusión de contactos (`base.partner.merge.automatic.wizard`) es irreversible y queda fuera de `aplicar_acciones.py`: se hace en Odoo con la persona, después de revisar la lista de duplicados en `contactos.md`.

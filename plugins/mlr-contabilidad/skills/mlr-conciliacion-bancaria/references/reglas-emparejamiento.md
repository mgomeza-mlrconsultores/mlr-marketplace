# Reglas de emparejamiento, estatus y observaciones

Hay dos catálogos y no se mezclan:

- **E01 a E11**: cómo el motor enlaza un movimiento con sus CFDI al construir el libro. Solo leen.
- **R01 a R14** (hoja 11_Catalogos de la plantilla de control): con qué regla se propone una corrección en Odoo en la hoja Acciones. Solo proponen; aplicar exige aprobación.

El documento de origen numeraba las dos listas como R01 en adelante con significados distintos (en una, R07 era «No requiere CFDI»; en la otra, «Diferencia de centavos»). La skill usa E para el motor y deja R para las acciones, como en la plantilla de control. Las filas de Acciones que vienen de la revisión de configuración llevan «Diagnóstico» en lugar de regla.

## Nivel 1: banco contra Odoo

Para cada movimiento del banco se busca el renglón del auxiliar con el mismo importe con signo (abono del banco = cargo contable a la cuenta de bancos) y fecha a no más de 10 días o tres veces la tolerancia. El texto no descarta candidatos, los ordena: primero los que comparten la referencia del banco, después los que comparten más palabras, y al final por cercanía de fecha. Se asigna de uno a uno. Lo que queda sin pareja aparece en el libro como «Está en el banco y no en Odoo» o, con partida `SB-O-xxx`, como «Está en Odoo y no en el banco».

## Nivel 2: movimiento contra CFDI

Se aplican en orden; la primera que encuentra pareja única gana. El orden de proceso pone primero los movimientos que Odoo ya liga a facturas, para que los saldos restantes que usan las demás reglas sean los correctos.

| Regla | Criterio | Enlace |
|---|---|---|
| D | Decisión de la persona en `decisiones.json`: enlace fijado (`acciones.py enlace`) o partida que no requiere CFDI (`acciones.py no-requiere`) | Según el caso |
| E12 | La contrapartida en Odoo es otra cuenta de banco o tarjeta (traspaso entre cuentas propias), o una cuenta listada en `cuentas_sin_cfdi` de params.json (préstamos y reembolsos de socios, inversiones) | No requiere CFDI |
| E07 | No requiere CFDI individual: comisiones e IVA de comisión (V43/V46/S39, V44/V47/S40), pago de impuestos (P14), nómina (contacto o concepto NOMINA), depósito de validación menor a 1 peso | No requiere CFDI |
| E01 | Facturas que Odoo ya concilió con el renglón (siguiendo conciliaciones hasta dos saltos: banco, cuenta puente, pago, cliente o proveedor, factura), o UUID o serie-folio en el texto. En un depósito de terminal con excedente, busca además el lote del resto (E08) | 1 a 1, Parcial, Varios CFDI o REP |
| E02 | RFC del texto del banco igual al de la contraparte del CFDI, mismo importe restante | 1 a 1 |
| E03 | Mismo importe restante, mismo contacto por nombre normalizado (sin S.A. de C.V., S.A.P.I., S. de R.L., acentos ni signos) y fecha dentro de la ventana | 1 a 1 |
| E08 | Depósito de terminal (V42/V45): factura pagada con tarjeta (forma 04 o 28) del mismo importe, o **lote**: combinación única de facturas de clientes distintos pagadas con tarjeta dentro de la tolerancia de días (el mismo día incluido) cuya suma iguala el depósito | 1 a 1 o Varios CFDI |
| E04 | Un movimiento, varias facturas del mismo contacto cuya suma lo iguala (búsqueda por subconjuntos acotada a 20 candidatos y 6 facturas) | Varios CFDI |
| E05 | Abono parcial a la única factura abierta del contacto con saldo mayor al movimiento | Parcial |
| E10 | Sin pareja | Sin CFDI |
| E11 | Empate: dos o más candidatos con mismo importe y contacto | Sin CFDI con la lista de candidatos; nunca se asigna solo |

Dentro de E01 a E05, una factura PPD que tiene su REP en las exportaciones se clasifica como «REP» con la fecha y el importe del complemento, y una diferencia de centavos dentro de la tolerancia no cambia el enlace. La numeración salta E06 y E09 porque en el documento de origen eran esos dos casos, que en la skill forman parte de las demás reglas.

**Saldo restante de cada factura.** Es el total del CFDI (en la moneda del diario) menos lo aplicado en esta corrida, topado con lo que Odoo dice que quedaba al empezar el periodo: saldo pendiente de hoy más lo que las líneas del periodo liquidaron. Así una factura que ya estaba pagada en julio no se empareja con un pago de agosto del mismo importe.

**Moneda.** Banco, auxiliar y columna V (total CFDI) van en la moneda del diario; base, IVA y retenciones (AF a AI) siempre en pesos, con el tipo de cambio del CFDI, porque alimentan el Previo. Un CFDI en pesos no se empareja en un diario en dólares, porque no hay tipo de cambio con que convertirlo.

Caso real de E11: dos facturas de la misma gasolinera del 28 de julio por 500.00 cada una. Se resolvió con el folio y la hora de timbrado del XML (folios consecutivos a las 13:10 y 13:11), sabiendo que Odoo había numerado esa serie del más reciente al más antiguo. La decisión se guarda en `decisiones.json`.

E08 es una mejora sobre el caso de origen: la regla anterior solo buscaba varias facturas del mismo contacto, y la terminal deposita en bruto las ventas del día de varios clientes. En agosto quedaron tres depósitos con 38,726.47 pesos de excedente sin enlazar, y el IVA de ese excedente (5,341.58) es la diferencia exacta entre el IVA trasladado del libro y el de Odoo.

## Importes fiscales por renglón

- Cada renglón es una factura que ampara un movimiento. Si un depósito paga tres facturas, la partida tiene tres renglones y el importe del banco aparece solo en el primero (columna AL «Primera» = 1).
- W, importe aplicado: la parte del movimiento que se aplica a esa factura.
- X, Y, Z, AA (base, IVA, IVA retenido, ISR retenido) se prorratean con los del CFDI (AF a AI): `=IF(OR(V="",V=0),0,ROUND(W/V*AF,2))`. Un cobro parcial lleva solo la parte proporcional del IVA, que es lo que exige el flujo de efectivo.
- Base del CFDI = subtotal menos descuento, en pesos (por el tipo de cambio del CFDI si la moneda no es MXN).
- AB, días contra la fecha de pago: solo en enlaces 1 a 1 y REP, contra la fecha del REP o la fecha real de pago de Mi Admin. En parcialidades no se compara, porque Mi Admin guarda una sola fecha por factura.

## Tipo de retención (columna U)

Con la retención que trae el XML, el régimen del emisor y palabras del concepto:

- Arrendamiento: renta, arrend, alquiler.
- Fletes: flete, autotransporte, transporte de carga, maniobra.
- Comisiones: comision.
- Honorarios: honorario, servicios profesionales, consultoria, asesoria, contable, juridic, auditoria.

| Tipo de proveedor (persona moral paga a persona física) | ISR retenido | IVA retenido |
|---|---|---|
| Honorarios | 10 % | 2/3 del IVA |
| Arrendamiento | 10 % | 2/3 del IVA |
| RESICO con actividad empresarial (régimen 626) | 1.25 % | No hay |
| RESICO con honorarios | 1.25 % | 2/3 del IVA |
| RESICO con arrendamiento | 1.25 % | 2/3 del IVA |
| Fletes | No hay | 4 % (art. 1-A, fr. II, inc. c, LIVA), por confirmar criterio |
| Comisiones | No hay | 2/3 del IVA (art. 3, fr. I, RLIVA), por confirmar criterio |
| Actividad empresarial no RESICO | No hay | No hay |

La retención de IVA del 6 % no se usa. Las alertas de retención usan esta tabla; el importe retenido siempre sale del XML. Valores de U: Sin retención, Honorarios, Arrendamiento, RESICO actividad empresarial, RESICO honorarios, RESICO arrendamiento, Fletes, Comisiones, Otra retención.

## Estatus (columna AD), siempre por fórmula

- **No identificado**: la partida no tiene importe de banco, no tiene renglón de Odoo o su enlace es «Sin CFDI».
- **Conciliado (revisar)**: tiene pareja, pero la diferencia banco contra Odoo o movimiento contra CFDI pasa la tolerancia de importe, o el desfase pasa la de días.
- **Conciliado (validar)**: enlace «Varios CFDI» o «Parcial».
- **Conciliado**: banco, Odoo y CFDI coinciden dentro de tolerancias. Incluye comisiones, impuestos y nómina.

`conciliar.py` calcula el mismo estatus en Python para informarlo en el chat antes de abrir el Excel; si alguna vez difiere del libro, manda el libro y se corrige el script.

## Observaciones: frases fijas

El Resumen cuenta con comodines sobre estas frases; cambiarlas rompe los conteos.

Informativas: «Mismo importe y fecha dentro de N días»; «Mismo importe, pero N días de diferencia contra la fecha de pago registrada»; «Abono parcial: quedan X por aplicar de esta factura»; «El movimiento es mayor que el saldo de la factura por X»; «Pago de factura PPD amparado con el REP <UUID>»; «No requiere CFDI individual»; «Comisión bancaria: la ampara el CFDI mensual del banco»; «IVA de comisión bancaria: lo ampara el CFDI mensual del banco»; «Pago de impuestos: se ampara con la declaración y su línea de captura»; «Nómina: se ampara con los CFDI de nómina, fuera de este control»; «Depósito de validación de cuenta (N)»; «Ningún CFDI vigente del mes coincide con este movimiento»; «sin contacto en Odoo»; «contacto en Odoo: X»; «Lote de terminal: N cobros con tarjeta de la misma fecha»; «Empate: …»; «Está en el banco y no en Odoo»; «Está en Odoo y no en el banco»; «Explicación aceptada por el usuario: …»; «Criterio del usuario: …»; «Traspaso entre cuentas propias (…)».

Alertas (la primera lleva «Alerta:», las siguientes van separadas por punto y coma):

- PUE cobrada (o pagada) en un mes distinto al de emisión: revisa el método de pago.
- PUE cobrada (o pagada) en parcialidades.
- Pago a "<contacto>" sin comprobante. El Resumen suma aparte el importe de las que dicen COMISIONES.
- Posible retención omitida.
- **Nuevas en la skill:** la línea de extracto sigue en la cuenta de suspenso en Odoo (modo con estado de cuenta); PPD sin complemento de pago en las exportaciones (el emisor tiene hasta el día 5 del mes siguiente); CFDI cancelado ante el SAT; PUE con forma de pago 99; posible pago duplicado (el CFDI ya se aplicó en otra partida por más de su total); pago en efectivo mayor a 2,000 pesos (art. 27 fr. III LISR, solo en diarios de caja); RFC en la lista 69-B del SAT, si se da la lista descargada.

En agosto hubo 23 alertas de PUE cobrada en otro mes y 12 de PUE en parcialidades: la empresa factura PUE paquetes que se cobran después o en abonos. Es un hallazgo fiscal real que se reporta al cliente, no un error del libro.

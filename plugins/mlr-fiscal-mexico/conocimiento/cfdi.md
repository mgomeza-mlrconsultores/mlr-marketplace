# CFDI 4.0 y complementos: lo que un consultor debe dominar

Vigente al 2026-10-03.

## Estructura y validaciones del CFDI 4.0
Emisor (RFC, nombre exacto según constancia, régimen fiscal), receptor (RFC, nombre exacto en mayúsculas sin régimen societario según constancia, código postal del domicilio fiscal, régimen fiscal, uso del CFDI compatible con el régimen), conceptos con clave de producto o servicio y clave de unidad del catálogo SAT, objeto de impuesto, impuestos trasladados y retenidos por concepto, forma de pago, método de pago (PUE pago en una exhibición, PPD pago en parcialidades o diferido), exportación, información global para factura al público general (periodicidad, meses, año), CFDI relacionados con tipo de relación (01 nota de crédito, 04 sustitución, 07 anticipo, entre otros). Timbrado por un PAC con sello del SAT; el XML es el documento, el PDF es representación.

## Complementos que más aparecen en diagnósticos
- **Recepción de pagos 2.0:** obligatorio cuando la factura es PPD; se emite al recibir el pago, a más tardar el quinto día natural del mes siguiente; incluye documentos relacionados, saldos e impuestos del pago. Patrón de error: PPD cobrado sin complemento, PUE cobrado en parcialidades.
- **Nómina 1.2:** percepciones, deducciones, otros pagos (subsidio causado), datos del trabajador y del patrón, registro patronal, salario base de cotización y salario diario integrado; ver plugin de nómina.
- **Carta porte:** para traslado de mercancías por vía terrestre, aérea, marítima o férrea; versión vigente 3.1 (verificar en el portal del SAT); afecta a quien transporta y a quien contrata transporte; patrón de error: fletes facturados sin complemento cuando corresponde.
- **Comercio exterior 2.0:** exportaciones definitivas con pedimento; ver agente de comercio exterior.
- **Otros:** impuestos locales, INE, donatarias, leyendas fiscales, notarios, divisas.

## Cancelación
Motivos 01 (con relación de sustitución, exige CFDI sustituto), 02 errores sin relación, 03 no se llevó a cabo la operación, 04 operación nominativa relacionada con factura global. Cancelación con aceptación del receptor cuando aplica (monto y plazo según regla vigente); plazo para cancelar comprobantes del ejercicio: a más tardar en el mes en que se presenta la declaración anual del ejercicio (verificar regla vigente). Patrón de error: cancelar sin sustituir cuando hubo pago, o sustituir sin relacionar.

## Factura global (público general)
Para operaciones con el público en general (punto de venta, tiendas): RFC genérico XAXX010101000, uso S01, periodicidad y periodo declarados, desglose por operación según regla; en punto de venta, Odoo genera la factura global por sesión o periodo según configuración.

## Catálogos SAT que viven en Odoo
Clave de producto o servicio y clave de unidad en productos y unidades de medida; régimen fiscal del emisor y de cada receptor; uso del CFDI por cliente; forma y método de pago por término de pago y por pago; código agrupador del SAT en cada cuenta contable (contabilidad electrónica); tipo de tercero y tipo de operación para la DIOT por proveedor.

## CFDI recibidos
Descarga masiva del portal del SAT o vía PAC; validación de vigencia y estado; conciliación contra facturas de proveedor registradas; detección de CFDI recibidos sin registro (gasto no deducido o no reconocido) y de registros sin CFDI (gasto no deducible). En Odoo: importación de XML a factura de proveedor, vínculo del UUID, validación contra el SAT.

## Lo que mira la autoridad
Consistencia entre CFDI emitidos y declarados; CFDI recibidos de contribuyentes listados en el 69-B; retenciones enteradas; complementos de pago faltantes; nómina timbrada contra IMSS; cancelaciones masivas. Ver `perspectiva-sat.md`.

# Códigos de concepto por banco

## BBVA México (comprobado en estados de cuenta reales de 2026)

| Código | Qué es | Tratamiento |
|---|---|---|
| T20 SPEI RECIBIDO | Cobro por transferencia; trae banco emisor, nombre y a veces concepto | Cliente por nombre, RFC o importe |
| T17 SPEI ENVIADO | Pago por transferencia; puede traer «RFC:XXXX» | Proveedor por RFC (E02) |
| N06 PAGO CUENTA DE TERCERO | Transferencia BBVA a otra cuenta; puede traer RFC e «IVA:» | Proveedor, cobro de cliente o reembolso a socio si es su cuenta |
| N05 PAGO TARJETA DE TERCEROS | Pago a la tarjeta de un tercero | Revisar: posible tarjeta de socio |
| A15 | Compra con tarjeta de débito de la empresa (comercio, a veces RFC con espacio y autorización) | Factura del comercio; sin CFDI, no deducible con aprobación |
| P14 SAT | Pago de impuestos con REF de línea de captura | Contra el acuse (`impuestos-sat.md`) |
| V42 / V45 | Venta con terminal, débito o crédito: depósito en bruto de varias ventas | Cobro a clientes, lote de terminal (E08) |
| V43 / V46 | Comisión de terminal («APLI TASA DE DES») | Comisiones bancarias |
| V44 / V47 | IVA de la comisión de terminal | Acreditable solo con CFDI del banco |
| S39 / S40 | Comisión de banca por internet e IVA | Igual que comisiones |
| K08 / K45 | Domiciliación o cargo recurrente (seguros, flotilla) | Proveedor por RFC o referencia |
| C02 | Depósito en efectivo | Cobro a identificar |

La terminal cobra la comisión y su IVA en movimientos separados con la misma referencia del lote («Ref. 175118705»), distinta de la del depósito.

El detalle del PDF de BBVA trae dos fechas (operación y liquidación), código, descripción en una o varias líneas, cargos, abonos y dos saldos (operación y liquidación). La carátula trae «Saldo de Liquidación Inicial», «Depósitos / Abonos (+)» con número de movimientos, «Retiros / Cargos (-)» con número de movimientos, «Saldo Final (+)», saldo promedio y total de comisiones.

## Cómo agregar un banco

1. Pedir a la persona, si existe, el Excel o CSV que exporta el banco: se lee sin perfil (`leer_estado_cuenta.py` reconoce encabezados de fecha, descripción, cargo, abono y saldo) y es más confiable que el PDF.
2. Si solo hay PDF, agregar un perfil en `PERFILES` de `leer_estado_cuenta.py`: patrón de fecha, si trae dos fechas, patrón de código, textos de los encabezados de cargo, abono y saldo, frase de fin de detalle, etiquetas de la carátula y de los datos de la cuenta.
3. Correr la lectura sobre un estado real y no aceptar el perfil hasta que el control cierre en cero en saldos y en número de movimientos. El lector asigna cada importe a la columna cuyo borde derecho queda más cerca, y todo lo que está a la derecha de cargos y abonos lo trata como saldo, nunca como importe.
4. Documentar aquí los códigos del banco con su tratamiento, y en `conciliar.py` (`NO_REQUIERE`, `TERMINAL_VENTA`) los que no requieren CFDI y los depósitos de terminal.

Santander, Banorte, Banamex, HSBC, Scotiabank y Banregio no están probados todavía: la primera conciliación de cada uno trae su perfil a esta tabla.

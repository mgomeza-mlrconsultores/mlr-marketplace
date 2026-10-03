# CFDI de nómina 1.2

Vigente al 2026-10-03. Verificar catálogos vigentes en el portal del SAT.

## Estructura
CFDI 4.0 tipo N con complemento de nómina 1.2: emisor con registro patronal (y RFC del patrón origen en pagos por cuenta de terceros), receptor trabajador con CURP, número de seguridad social, fecha de inicio de relación laboral, antigüedad, tipo de contrato, tipo de régimen (02 sueldos, 09 asimilados honorarios, 11 asimilados otros, entre otros), periodicidad de pago, banco y cuenta, SBC, salario diario integrado, clave de entidad federativa; percepciones con clave SAT (001 sueldos, 002 aguinaldo, 019 horas extra, 021 prima vacacional, 022 prima dominical, 028 comisiones, 038 otros ingresos por salarios, etc.) con importe gravado y exento; deducciones (001 seguridad social, 002 ISR, 004 otros, 006 descuento por incapacidad, 010 INFONAVIT, 020 ausencias, etc.); otros pagos (002 subsidio para el empleo con subsidio causado, 001 reintegro de ISR, 004 aplicación de saldo a favor); incapacidades y horas extra en nodos propios; método de pago PUE, forma de pago 99, uso del CFDI CN01.

## Plazos
Antes de pagar o dentro del plazo que la regla concede según número de trabajadores y periodicidad (días hábiles posteriores al pago). Cancelación con sustitución cuando hay error en importes; timbrado de finiquitos con sus claves.

## Validaciones que fallan
Nombre del trabajador distinto de su constancia; CURP o NSS inválidos; SBC o SDI fuera de rango; subsidio causado en periodos donde no corresponde; percepciones exentas por encima del límite; registro patronal que no corresponde al centro de trabajo; régimen asimilado en subordinados reales.

## Conciliación mensual
Suma de CFDI de nómina del mes contra provisión y pago de nómina en contabilidad; retenciones de ISR timbradas contra entero del día 17; cuotas obrero timbradas contra SUA; ausencias e incapacidades contra IMSS.

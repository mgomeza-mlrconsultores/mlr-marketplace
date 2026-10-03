# Nómina en Odoo para México: localización y alternativas

Vigente al 2026-10-03 (documentación de Odoo consultada en esa fecha; verificar en la versión exacta).

## Localización oficial (Enterprise)
Módulos: `l10n_mx_hr_payroll` (campos y datos de nómina y ausencias), `l10n_mx_hr_payroll_account` (cálculos y contabilidad) y `l10n_mx_hr_payroll_account_edi` (timbrado del CFDI de nómina con PAC). Calcula ISR y subsidio, cuotas IMSS, INFONAVIT y SAR. Configuración requerida: RFC de la compañía, prima de riesgo, tipo de régimen de contratación, estructura salarial (fijo u horario), registro patronal, UMA y salarios mínimos vigentes en los parámetros de reglas; estructuras instaladas: nómina regular y aguinaldo. Limitación documentada: no genera entradas de trabajo desde Asistencias ni Planificación (las ausencias y los extras se capturan en nómina). Disponibilidad y alcance por versión: verificar en la documentación de la versión del cliente (la documentación «master» describe la más reciente); una firma puede decidir esperar una versión por los cambios que trae.

## Lo que hay que revisar antes de ofrecerla
Periodicidades soportadas, cálculo de SDI y variables bimestrales, finiquitos y liquidaciones, PTU, ajuste anual, incapacidades, pensiones alimenticias, créditos INFONAVIT por modalidad, impuesto sobre nóminas estatal, reportes para SUA/IDSE, timbrado masivo y cancelación, asimilados. Lo que no cubra se resuelve con reglas salariales propias o fuera de Odoo.

## Alternativa: nómina externa integrada
Sistemas de nómina locales (los de uso extendido en México) calculan y timbran; Odoo recibe la póliza de nómina por importación (provisiones, retenciones, cuotas) y los CFDI de nómina se importan para cuadre; empleados y ausencias pueden sincronizarse. Ventaja: cumplimiento probado; costo: doble mantenimiento de catálogos y conciliación mensual. Es el esquema típico cuando la firma maquila la nómina del cliente.

## Contabilidad de la nómina en Odoo
Asiento de provisión por periodo (sueldos, prestaciones, cuotas patronales, impuesto sobre nóminas) con analítica por departamento o unidad; cuentas por pagar de retenciones (ISR, IMSS obrero, INFONAVIT, pensiones) con entero el día 17; pago a trabajadores por lote bancario; conciliación del pago con el banco; provisiones anuales (aguinaldo, vacaciones, PTU) conforme a NIF D-3.

## Patrones en bases Odoo
Nómina timbrada en Odoo sin cuadre con la contabilidad (provisión registrada por otro camino); empleados con SBC o SDI sin actualizar; reglas salariales con UMA o salario mínimo del año anterior; impuesto sobre nóminas con tasa de otra entidad; póliza de nómina externa cargada a una sola cuenta de gasto sin desglose; retenciones sin cuenta por pagar propia.

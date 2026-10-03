# IMSS e INFONAVIT para el consultor de nómina

Vigente al 2026-10-03. Cuotas en `parametros-2026.md`.

## Afiliación y movimientos (IDSE)
Alta dentro de los cinco días hábiles siguientes al inicio; modificaciones de salario (fijas dentro de cinco días; variables al inicio de cada bimestre con el promedio del bimestre anterior); bajas. Registro patronal por domicilio y clase de riesgo. Errores típicos: altas tardías, SBC menor al real, trabajadores sin alta (asimilados que son subordinados), omisión de variables.

## Salario base de cotización
Integra los elementos del art. 27 LSS con sus exclusiones (instrumentos de trabajo, ahorro con aportación igual, despensa hasta 40 % de UMA, premios de asistencia y puntualidad hasta 10 % cada uno, PTU, tiempo extra dentro de los márgenes legales, alimentación y habitación con reglas). Tope 25 UMA. El SBC del CFDI de nómina debe coincidir con el del IMSS.

## Cuotas y pago (SUA/SIPARE)
Mensual (enfermedades y maternidad, invalidez y vida, guarderías, riesgos de trabajo) a más tardar el día 17; bimestral (retiro, cesantía y vejez, INFONAVIT 5 % y amortizaciones de crédito) con el pago de los meses impares. Prima de riesgo: declaración anual de siniestralidad en febrero; clase y prima por registro patronal. Reforma de pensiones 2020: la cuota patronal de cesantía y vejez sube gradualmente de 2023 a 2030 según el nivel salarial (tabla del año en `parametros-2026.md`).

## INFONAVIT
Aportación patronal 5 % del SBC bimestral; retención de créditos conforme al aviso (porcentaje, cuota fija en veces UMA o salario mínimo); avisos de suspensión y reinicio; ajuste cuando el trabajador causa baja.

## Cruces que hacen IMSS e INFONAVIT con el SAT
CFDI de nómina contra movimientos afiliatorios (trabajadores timbrados sin alta, SBC distinto), subcontratación sin REPSE (deducción improcedente), dictamen IMSS cuando aplica. Opinión de cumplimiento en materia de seguridad social (propia del IMSS e INFONAVIT) exigida en contratación pública.

## Patrones en bases Odoo
Empleados sin número de seguridad social o sin registro patronal; SBC sin recalcular tras cambios de salario o variables; cuotas provisionadas distintas a las pagadas en SUA; prima de riesgo desactualizada; INFONAVIT con créditos vencidos aún descontados; bimestres de variables sin reportar.

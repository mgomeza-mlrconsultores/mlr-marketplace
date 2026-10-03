---
name: mlr-nomina-mx
description: >
  Esta skill debe usarse cuando se diga «nómina», «calcula el ISR del trabajador», «salario diario integrado», «IMSS»,
  «INFONAVIT», «CFDI de nómina», «finiquito», «liquidación», «PTU», «aguinaldo», «vacaciones», «impuesto sobre nóminas»,
  «REPSE», «jornada de 40 horas», «configura la nómina en Odoo» o «audita la nómina». Orquesta a los especialistas de
  nómina mexicana con los parámetros vigentes y fundamento legal.
metadata:
  version: "0.1.0"
---

# Nómina mexicana en proyectos Odoo

Los agentes calculan, configuran y auditan con `conocimiento/parametros-2026.md` como única fuente de cifras y la LFT, LSS, LISR y catálogos SAT como fundamento; el cálculo que se paga lo valida un contador o especialista de nómina del cliente.

## Enrutamiento
- Cálculo de un periodo, finiquito, liquidación, PTU, aguinaldo, ajuste anual → `mlr-nomina-calculo`.
- Afiliación, SBC, cuotas, prima de riesgo, INFONAVIT, SUA/IDSE → `mlr-nomina-imss-infonavit`.
- Jornada, prestaciones, contratos, REPSE, NOM-035/037, reforma de 40 horas → `mlr-nomina-cumplimiento-laboral`.
- Estructura y validación del CFDI de nómina, cancelaciones, conciliación con contabilidad → `mlr-nomina-cfdi`.
- Configurar o evaluar la nómina en Odoo (localización o nómina externa integrada) → `mlr-nomina-odoo-config`.
- Diagnóstico de nómina de una base (catálogo N-01 a N-17) → `mlr-nomina-auditor`.
- Cambios de UMA, salario mínimo, tarifas, cuotas, reformas → `mlr-nomina-vigilante`.

## Reglas
1. Cifras siempre desde `parametros-2026.md`, con fecha; si tiene más de 90 días, verificar antes.
2. Todo cálculo se muestra desarrollado (base, tarifa, cuota, exento y gravado) para que el especialista lo valide.
3. Lo que afecta a personas (descuentos, despidos) se trata con el cuidado legal correspondiente y se deriva al plugin legal cuando hay controversia.
4. Nómina timbrada, IMSS y contabilidad deben contar la misma historia; el auditor lo comprueba.

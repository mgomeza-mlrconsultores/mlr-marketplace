---
name: mlr-cumplimiento-legal
description: >
  Esta skill debe usarse cuando se diga «revisa el contrato», «propiedad intelectual», «licencia del módulo», «aviso de
  privacidad», «datos personales», «¿cumplimos la ley de datos?», «contratos laborales», «REPSE», «servicios
  especializados», «poderes», «quién firma», «beneficiario controlador», «lavado de dinero», «PROFECO», «tienda en línea
  legal», «términos y condiciones» o «qué cambió en la ley»; también cuando un diagnóstico, cotización o salida a
  producción en Odoo toque alguno de esos temas. Orquesta a los agentes legales.
metadata:
  version: "0.1.0"
---

# Cumplimiento legal en proyectos Odoo

Los agentes de este plugin estructuran, detectan riesgos, preparan expedientes y proponen redacciones; la opinión legal la emite un abogado titulado y así se dice en cada entregable. Toda cita legal lleva artículo, fuente y fecha de verificación.

## Enrutamiento
- Contratos de implementación, soporte, desarrollo, licencias, confidencialidad → `legal-contratos-ti`.
- Datos personales en base, sitio, portal, respaldos y terceros → `legal-datos-personales`.
- Relación laboral, expedientes, normas STPS, servicios especializados, terminaciones → `legal-laboral` (cálculos en `nomina-mexico`).
- Sociedad, poderes, libros, beneficiario controlador, prevención de lavado, términos de venta → `legal-mercantil-corporativo`.
- Tienda en línea, punto de venta y ventas a consumidores → `legal-consumidor-ecommerce`.
- Reformas y criterios nuevos → `legal-vigilante`.

## Reglas
1. Fuente primaria o nada: DOF, ley vigente publicada, portal de la autoridad; se anota la fecha de verificación.
2. Riesgo con consecuencia medible (multa en UMA desde `parametros-2026.md` del plugin fiscal, nulidad, laudo, pérdida de deducción) y corrección concreta en Odoo o en el documento.
3. Lo que exige fe pública, resolución de asamblea, registro ante autoridad o interpretación se eleva al abogado con el expediente preparado.
4. Los hallazgos se citan con su patrón L-xx y alimentan el diagnóstico del plugin de consultoría.
5. Datos personales de clientes y empleados nunca se copian al chat ni a bases de prueba sin enmascarar.

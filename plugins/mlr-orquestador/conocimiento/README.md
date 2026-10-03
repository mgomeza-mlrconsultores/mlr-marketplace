# Base de conocimiento de los agentes

Los agentes de este marketplace no razonan «en general»: cargan estos archivos antes de actuar y los citan. La base se mantiene con la skill `actualizar-conocimiento` y el agente `investigador-odoo`, que la revisan cada mes contra las fuentes oficiales y registran cada cambio en `CAMBIOS.md`.

| Archivo | Qué contiene | Quién lo carga |
| --- | --- | --- |
| `odoo-versiones.md` | Diferencias por versión (15 a 19) que cambian un diagnóstico, una cotización o una personalización | Todos |
| `patrones-inventario-valuacion.md` | Catálogo de patrones de error en inventario y valuación, con causa raíz, detección y remediación | auditor-inventario-valuacion, cotizador, arquitecto-solucion |
| `patrones-contabilidad.md` | Catálogo de patrones de error contables y fiscales | auditor-contable, conciliador-bancario, cierre-mensual |
| `patrones-configuracion-seguridad.md` | Catálogo de riesgos de configuración, seguridad y automatizaciones | auditor-configuracion-seguridad, auditor-codigo-personalizaciones |
| `catalogo-funcionalidades.md` | Nombres de funcionalidad de Odoo por aplicación para rutas de cotización; nombres vetados | cotizador, analista-descubrimiento |
| `checklist-evidencia.md` | Qué cuenta como evidencia y cómo se registra | Auditores y verificador |
| `fuentes-oficiales.md` | Dónde se verifica cada afirmación: documentación, código fuente, OCA, autoridad fiscal de `México` | investigador-odoo y todos |
| `glosario-es-en.md` | Términos de Odoo, finanzas e inventario en español e inglés | Redactores y agentes que leen código |
| `CAMBIOS.md` | Bitácora de actualizaciones de la base de conocimiento | investigador-odoo |

Regla: una afirmación sobre cómo funciona Odoo que no esté respaldada por la documentación o el código de la versión exacta se marca como hipótesis. Si un agente descubre algo nuevo y comprobado, lo propone para esta base en el mismo turno.

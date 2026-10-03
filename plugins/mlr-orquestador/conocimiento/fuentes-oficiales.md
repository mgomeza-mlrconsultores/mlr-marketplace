# Fuentes oficiales y cómo se consultan

Antes de afirmar cómo funciona Odoo o qué exige la autoridad fiscal, se consulta la fuente y se cita en la bitácora interna. Orden de preferencia: código fuente de la versión exacta, documentación oficial de esa versión, notas de versión, repositorios de la OCA, documentación de la autoridad fiscal.

## Odoo
- Código fuente: repositorio `odoo/odoo` en GitHub, rama de la versión (`17.0`, `18.0`, `19.0`); módulos Enterprise en `odoo/enterprise` (acceso restringido) o leídos en la base con `ir.model.fields` y `ir.ui.view`.
- Documentación: documentación oficial de Odoo seleccionando la versión; guías de desarrollo (ORM, vistas, acciones de servidor), referencia de la API externa, documentación de localizaciones.
- Notas de versión por lanzamiento (una por versión mayor) y hoja de ruta pública.
- Base demo propia de la versión para probar comportamiento antes de afirmarlo (`https://edu-demo-mlr.odoo.com`).

## OCA
- Repositorios por dominio (`OCA/stock-logistics-warehouse`, `OCA/account-financial-tools`, `OCA/manufacture`, `OCA/l10n-<pais>`), guías de contribución y de migración, y el estado de migración por versión en cada repositorio.

## Autoridad fiscal de `México`
- Portal oficial de la autoridad: catálogos vigentes de comprobantes, complementos, regímenes, claves y formas de pago; calendario de obligaciones; cambios normativos con fecha de entrada en vigor. Se cita la página y la fecha de consulta.
- Normas contables aplicables (`NIF`: por ejemplo NIF o IFRS) para criterios de valuación y reconocimiento.

## Rutina de verificación de una afirmación
1. Formular la afirmación con versión y módulo.
2. Buscar el método o la vista en el código de la rama; leer la lógica.
3. Confirmar en la base demo con un caso mínimo.
4. Si la afirmación es fiscal, confirmar en el portal oficial y anotar fecha.
5. Registrar en la bitácora: fuente, ruta o enlace, fecha, conclusión.

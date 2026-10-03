# Patrones de defectos en módulos (K-01 a K-16)

K-01 SQL con formato de cadenas o concatenación. Riesgo: inyección. Corrección: ORM o `SQL` con parámetros.
K-02 `sudo()` generalizado o para esquivar reglas sin razón. Riesgo: fuga de datos entre empresas o usuarios. Corrección: acotar y documentar.
K-03 Modelo sin `ir.model.access.csv` o con acceso total a todos. Corrección: CSV por grupo y reglas de registro.
K-04 Cálculos almacenados con `@api.depends` incompleto. Riesgo: datos obsoletos silenciosos. Corrección: dependencias completas o no almacenar.
K-05 Búsquedas dentro de bucles (N+1), `browse` repetidos, `search` sin límite. Riesgo: lentitud creciente. Corrección: `read_group`, prefetch, dominios combinados.
K-06 `cr.commit()` en lógica de negocio. Riesgo: inconsistencias y pérdida de atomicidad. Corrección: eliminar; usar colas o `with_delay` cuando aplique.
K-07 Identificadores de registros fijos en código (ids numéricos). Corrección: identificadores externos.
K-08 Vistas con `attrs` o `states` en 17 o superior; `tree` en 18 o superior; `name_get` en 17 o superior; `_sql_constraints` en 19. Corrección: migrar conforme a `api-por-version.md`.
K-09 Controladores públicos sin `auth` explícito, sin CSRF o que exponen registros por id. Corrección: autenticación, CSRF, validación de acceso.
K-10 Sin pruebas o pruebas que no fallan nunca. Corrección: pruebas que reproducen casos reales con usuario sin privilegios.
K-11 Textos sin traducir, `string` con mayúsculas inconsistentes, sin `i18n`. Corrección: `_()` y archivos `.po`.
K-12 Empresa, moneda, diario o cuentas fijas en código. Riesgo: rompe multiempresa. Corrección: configuración y `check_company`.
K-13 Modificación directa de archivos del núcleo o de módulos de terceros. Riesgo: se pierde al actualizar. Corrección: herencia.
K-14 Lógica pesada en `onchange` o en `write` que debería ser cálculo o acción. Corrección: rediseño.
K-15 Licencia ausente o incompatible en el manifiesto; código copiado de Enterprise. Corrección: `licencias.md`.
K-16 Manifiesto sin `version` de Odoo, dependencias faltantes, `auto_install` sin razón, datos de demostración en `data`. Corrección: manifiesto conforme a `estandares-codigo.md`.

# Originales de la conciliación bancaria

El marketplace de la firma es público. Los originales viven en la unidad compartida y no se suben aquí:

`G:\Unidades compartidas\MMLR 2025\Hoja Membretada\Conciliación Bancaria\`

| Archivo | Qué es | ¿Hay copia aquí? |
|---|---|---|
| `Plantilla_Conciliacion_Banco_Odoo_CFDI.xlsx` | Libro vacío con sus 1,796 fórmulas | Sí, con los textos del caso de origen neutralizados |
| `MLR_Plantilla_Conciliacion_Bancaria_Odoo.xlsx` | Control y aprobación: parámetros, diagnóstico, propuesta, ajustes, impuestos, verificación, reversión, bitácora, catálogo R01 a R14 | Sí, con el renglón de ejemplo de cada hoja anonimizado |
| `Ejemplo_Conciliacion_Agosto_2026_<cliente>_v2_1.xlsx` | El caso real lleno | **No.** Aquí va `Ejemplo_Conciliacion_Agosto_2026_Demo.xlsx`, con personas, negocios, RFC, UUID, cuentas y referencias sustituidos de forma consistente; cifras, fechas, folios y fórmulas intactos, y resultados idénticos al original en cada celda numérica y de estatus |
| `CONTEXTO_Conciliacion_Bancaria_MLR.md` | Documento de origen de la skill | No; su contenido está repartido en `SKILL.md` y `references/` |

`llenar_libro.py` usa la plantilla de la unidad cuando la encuentra (en Windows por la letra G:, o montada como carpeta conectada) y la de esta carpeta si no.

Si se actualiza la plantilla en la unidad, correr `tests/prueba_ejemplo.py` con `--plantilla` apuntando a ella antes de usarla con un cliente, y copiar aquí la versión neutralizada.

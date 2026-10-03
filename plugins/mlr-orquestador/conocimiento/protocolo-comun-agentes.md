# Protocolo común de los agentes

Todo agente de este marketplace sigue estas reglas antes de las propias.

1. **Cargar conocimiento antes de actuar.** Leer `odoo-versiones.md`, el catálogo de patrones de su dominio y `checklist-evidencia.md`. Identificar la versión y edición de la base y la línea de tiempo de migraciones antes de la primera consulta.
2. **Fuente de verdad.** Ninguna afirmación sobre el comportamiento de Odoo sin código o documentación de la versión exacta (`fuentes-oficiales.md`). Lo no verificado se marca hipótesis.
3. **Solo lectura por defecto.** Las consultas a la base pasan por el cliente de solo lectura (`scripts/odoo_readonly.py` o el helper equivalente del plugin de diagnóstico). Nada de `write`, `create`, `unlink`, botones ni acciones de servidor, aunque sea base de pruebas, salvo en el plugin de personalización y con aprobación explícita.
4. **Lectura del negocio primero.** Qué vende, cómo compra, cómo produce, cómo cobra y qué le duele al director; se escribe en el contexto del trabajo antes de la técnica.
5. **Evidencia por afirmación.** Cifra por dos caminos, folio, mecanismo con código, contraejemplo, comprobante fiscal leído. Demostrado contra inferencia, siempre separados.
6. **Catálogo completo.** Recorrer el catálogo de patrones entero antes de dar por terminada una revisión; proponer patrones nuevos comprobados para la base de conocimiento.
7. **Dos lectores.** Toda salida tiene capa directiva (qué está mal, qué cuesta o arriesga, qué se hace) y capa técnica (cómo se detectó, cómo se corrige, con qué riesgo). El informe al cliente no narra el método.
8. **Autoverificación antes de entregar.** Releer la propia salida buscando afirmaciones sin evidencia, cifras sin fuente, recomendaciones sin dueño ni orden, y términos de la lista negra de redacción.
9. **Registro.** Lo que se mide va al catálogo; lo que se decide va a la bitácora; lo que se aprende de Odoo va propuesto a `CAMBIOS.md`.
10. **Economía.** Consultas por lotes, campos mínimos, caché local para cargas pesadas; no repetir lecturas que ya hizo otro agente si el orquestador las comparte.

## Formato de salida de un auditor
Encabezado: base, versión y edición, corte, método de acceso, línea de tiempo. Luego, por patrón revisado: estado (sin hallazgo / hallazgo / no medible), cifra con sus dos caminos, folio de ejemplo, etiqueta de origen, impacto estimado y remediación propuesta con orden. Cierre: lista de hipótesis no demostradas y lo que falta medir.

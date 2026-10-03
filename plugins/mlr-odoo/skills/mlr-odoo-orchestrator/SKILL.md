---
name: mlr-odoo-orchestrator
description: Flujo MLR para personalizar Odoo en Cowork. Usar ante cualquier pedido de personalizacion de Odoo (campos, modelos, vistas, acciones de servidor, automatizaciones). Reune contexto, ejecuta el cambio, verifica en navegador con captura, consulta Context7 y documenta en informe en espanol.
---

# Orquestacion MLR de Odoo (Cowork)

Cuando el usuario pida una personalizacion de Odoo, sigue este flujo:

1. **Reune contexto**: version de Odoo (SaaS normalmente), modelo afectado, requisito exacto. Consulta **Context7** (connector) para la documentacion mas reciente de Odoo antes de programar.
2. **Ejecuta el cambio** con las herramientas/plugins de Odoo (odoo-development, odoo-query) segun el tipo:
   - Campos (text/integer/selection/many2one/computed...), modelos nuevos, vistas XML (form/list/kanban/search/pivot), acciones de servidor / automatizaciones / cron / botones.
   - Nombres y etiquetas **sin** prefijo `[MLR]` (ver Directiva general abajo).
3. **Verifica en el navegador** (Claude-in-Chrome / Playwright connector): abre la vista afectada, confirma que renderiza y funciona, y **toma una captura**.
4. **Documenta** un informe en **espanol** (resumen ejecutivo, detalle tecnico, resultado de pruebas, instrucciones de rollback). Usa estilo ui-ux-pro-max si aplica.
5. **Idiomas**: codigo/identificadores en ingles; informes y comunicacion en espanol.

Nota: en Cowork estas reglas viven como skill (Cowork prioriza skills sobre agentes). Los agentes MLR equivalentes vienen tambien en este plugin (carpeta agents/) por si se usan.

## Directiva general del Proyecto MLR (obligatoria)

### 1. Nombres y etiquetas visibles: SIN `[MLR]`
Nada de lo que ve el usuario final lleva el prefijo `[MLR]`, porque aparece en las
ventanas de trabajo del cliente: nombres de modelos, etiquetas de campos, menus,
titulos de asistentes y ventanas, acciones contextuales del menu "Acciones",
grupos de seguridad y asuntos de correo. Se nombran en lenguaje funcional y claro
(ej. `Facturas globales por pagos (en lote)`, `Forzar reinicio`).

`[MLR]` **solo** se conserva en lo puramente tecnico e invisible para el usuario:
los mensajes de registro (`ir.logging`, via `log()`), con el formato
`[MLR][GP] ...` / `[MLR][TM] ...`, para poder filtrarlos.

Los **nombres tecnicos** (no visibles) siguen igual: `x_mlr_...`, `mlr_...`.

### 2. Comentarios en el codigo: casi ninguno, y funcionales
El codigo de acciones de servidor, crones y campos calculados va **sin comentarios
narrativos**: nada de cabeceras explicando el flujo, ni comentarios que cuentan lo
que ya dice el codigo, ni notas de tipo "FIX/NOTA/OJO".

Solo se admite un comentario corto, **en espanol**, junto a las **variables y
banderas configurables**, explicando que valores se pueden poner:

```python
SOLO_PREVISIONES = True   # True = solo previsiones | False = tambien inmediato y mantenimiento
PRESUPUESTO = 300.0       # segundos de trabajo por pasada del cron
PROD_GLOBAL = 7333        # producto que se usa en la linea de la factura nueva
```

Objetivo: que cualquiera pueda cambiar el comportamiento a futuro tocando las
constantes de arriba, sin leer prosa.

### 3. Donde se guardan los archivos (obligatorio)
Todo (codigo, informes, capturas, bundles) se guarda en el proyecto, nunca solo en
el chat: **`<carpeta local de proyectos MLR>`**, respetando la
organizacion y la nomenclatura que ya existe:

```
<Cliente>/Contexto/                         Historial_Chat_*.md, README_Contexto_<Cliente>.md, Memoria_Cowork
<Cliente>/Informes/<YYYYMMDD>/              MLR_<Tema>_<Cliente>_<YYYY-MM-DD>.<md|docx|pdf|pptx>
<Cliente>/Capturas de pantalla/<YYYYMMDD>/  evidencias numeradas: 01_..., 02_... (nunca dentro de Informes)
<Cliente>/Documentos extras/<YYYYMMDD>/    exports, xlsx, material de apoyo; lo interno en Interno/
Desarrollos/<Nombre del desarrollo>/        README.md + Instalador/<YYYYMMDD>/
Instalador Odoo MLR/Bundles de codigos/     bundles maestros .zip para la Plataforma MLR
```

Reglas:
- **Cliente nuevo** -> se crea su carpeta con esa misma estructura, sin inventar variantes.
- El **codigo de un desarrollo** va en `Desarrollos/<desarrollo>/Instalador/<fecha>/`, y el
  `README.md` del desarrollo se actualiza con lo que cambio, el estado y las pruebas.
- Los **informes y capturas** van a la carpeta del cliente dentro de `MLR Odoo`, en `Informes/<YYYYMMDD>/` y `Capturas de pantalla/<YYYYMMDD>/`. Si la carpeta del cliente, alguna de las tres carpetas fijas (`Informes`, `Documentos extras`, `Capturas de pantalla`) o la de fecha no existen, se crean completas, con sus intermedias, antes de guardar y sin preguntar.
- Si un desarrollo ya existe, se **amplia** su carpeta y su README; no se crea una nueva.
- Carpetas conectadas: si la carpeta no esta conectada a la sesion, se pide acceso con
  `device_request_folder_access` sobre `<carpeta local de proyectos MLR>`.

### 4. Código mínimo: Odoo cobra cada línea (obligatorio)
Odoo cobra al cliente el mantenimiento del código a medida por cada 100 líneas
(1,440 por cada 100 líneas, dato de Marcos del 3-oct-2026). Cada línea que queda en
la base es un costo recurrente para el cliente, así que el código se limita al mínimo
que resuelve el requisito, sin quitar ninguna protección.

Qué cuenta (medido en Acretex, saas~19.3, 3-oct-2026):
- Las líneas de código Python de acciones de servidor (incluidas las de
  automatizaciones y crones) y de campos calculados. Aparecen como `odoo/studio` en el
  conteo de mantenimiento. Los comentarios y las líneas en blanco NO cuentan
  (probado: 2 líneas de código + 4 comentarios + 2 en blanco sumaron 2).
- Las acciones de servidor no tienen archivado: aunque su automatización esté
  archivada, sus líneas se siguen cobrando. Lo que ya no se usa se ELIMINA, no se
  archiva, después de respaldar su código en `Documentos extras/<fecha>/Interno/` y en
  el bundle del desarrollo.
- No se ha medido si cuentan las vistas heredadas; se mantienen igual de mínimas.
- Cómo medir: crear una acción temporal con
  `raise UserError(repr(env['publisher_warranty.contract']._get_message()['maintenance']))`,
  ejecutarla, leer `odoo/studio` y borrarla en el acto (mientras existe, su propia
  línea cuenta). Se mide antes y después de cada entrega y la diferencia va en el
  informe.

Reglas:
- Primero lo nativo y la configuración (campos relacionados, valores por defecto,
  dominios, reglas de registro, vistas heredadas, acciones de ventana); el código es el
  último recurso.
- Una sola acción por responsabilidad. Al reemplazar una acción, la anterior se elimina
  en el mismo cambio, cuando la nueva ya pasó sus pruebas; nada de versiones paralelas
  (v1 archivada junto a v2 activa).
- Sin código muerto, sin ramas que nunca se ejecutan, sin validaciones que ya hace
  Odoo, sin variables intermedias que no aportan.
- Compacto pero legible: se junta lo que se lee igual de claro; no se comprime hasta
  volverlo críptico.
- A prueba de fallos no se negocia: las validaciones que protegen datos (`UserError`
  antes de escribir, cuadres, idempotencia) se quedan aunque sumen líneas. Se recorta
  lo superfluo, nunca la seguridad.
- Pruebas, diagnósticos y migraciones corren por API desde fuera, nunca como acciones
  guardadas en la base del cliente; cualquier acción temporal se borra en la misma
  sesión.

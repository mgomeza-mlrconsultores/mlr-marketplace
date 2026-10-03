---
name: mlr-personalizacion-odoo
description: Flujo MLR Consultores para personalizar Odoo en Cowork. Usar ante cualquier pedido de personalizacion de Odoo (campos, modelos, vistas, acciones de servidor, automatizaciones). Reune contexto, ejecuta el cambio, verifica en navegador con captura, consulta Context7 y documenta en informe en espanol.
---

# Orquestacion MLR Consultores de Odoo (Cowork)

Cuando el usuario pida una personalizacion de Odoo, sigue este flujo:

1. **Reune contexto**: version de Odoo (SaaS normalmente), modelo afectado, requisito exacto. Consulta **Context7** (connector) para la documentacion mas reciente de Odoo antes de programar.
2. **Ejecuta el cambio** con las herramientas/plugins de Odoo (odoo-development, odoo-query) segun el tipo:
   - Campos (text/integer/selection/many2one/computed...), modelos nuevos, vistas XML (form/list/kanban/search/pivot), acciones de servidor / automatizaciones / cron / botones.
   - Nombres y etiquetas **sin** prefijo `[mlr]` (ver Directiva general abajo).
3. **Verifica en el navegador** (Claude-in-Chrome / Playwright connector): abre la vista afectada, confirma que renderiza y funciona, y **toma una captura**.
4. **Documenta** un informe en **espanol** (resumen ejecutivo, detalle tecnico, resultado de pruebas, instrucciones de rollback). Usa estilo ui-ux-pro-max si aplica.
5. **Idiomas**: codigo/identificadores en ingles; informes y comunicacion en espanol.

Nota: en Cowork estas reglas viven como skill (Cowork prioriza skills sobre agentes). Los agentes MLR Consultores equivalentes vienen tambien en este plugin (carpeta agents/) por si se usan.

## Directiva general del C:\Users\mgome\Claude\Projects\MLR Odoo (obligatoria)

### 1. Nombres y etiquetas visibles: SIN `[mlr]`
Nada de lo que ve el usuario final lleva el prefijo `[mlr]`, porque aparece en las
ventanas de trabajo del cliente: nombres de modelos, etiquetas de campos, menus,
titulos de asistentes y ventanas, acciones contextuales del menu "Acciones",
grupos de seguridad y asuntos de correo. Se nombran en lenguaje funcional y claro
(ej. `Facturas globales por pagos (en lote)`, `Forzar reinicio`).

`[mlr]` **solo** se conserva en lo puramente tecnico e invisible para el usuario:
los mensajes de registro (`ir.logging`, via `log()`), con el formato
`[mlr][GP] ...` / `[mlr][TM] ...`, para poder filtrarlos.

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
el chat: **`<carpeta local de proyectos MLR Consultores>`**, respetando la
organizacion y la nomenclatura que ya existe:

```
<Cliente>/Contexto/                         Historial_Chat_*.md, README_Contexto_<Cliente>.md, Memoria_Cowork
<Cliente>/Informes/<YYYYMMDD>/              <Tema>_<Cliente>_<YYYY-MM-DD>.<md|docx|pdf|pptx>
<Cliente>/Capturas de pantalla/<YYYYMMDD>/  evidencias numeradas: 01_..., 02_... (nunca dentro de Informes)
<Cliente>/Documentos extras/<YYYYMMDD>/    exports, xlsx, material de apoyo; lo interno en Interno/
Desarrollos/<Nombre del desarrollo>/        README.md + Instalador/<YYYYMMDD>/
Instalador Odoo MLR Consultores/Bundles de codigos/     bundles maestros .zip para la Plataforma MLR Consultores
```

Reglas:
- **Cliente nuevo** -> se crea su carpeta con esa misma estructura, sin inventar variantes.
- El **codigo de un desarrollo** va en `Desarrollos/<desarrollo>/Instalador/<fecha>/`, y el
  `README.md` del desarrollo se actualiza con lo que cambio, el estado y las pruebas.
- Los **informes y capturas** van a la carpeta del cliente dentro de `C:\Users\mgome\Claude\Projects\MLR Odoo`, en `Informes/<YYYYMMDD>/` y `Capturas de pantalla/<YYYYMMDD>/`. Si la carpeta del cliente, alguna de las tres carpetas fijas (`Informes`, `Documentos extras`, `Capturas de pantalla`) o la de fecha no existen, se crean completas, con sus intermedias, antes de guardar y sin preguntar.
- Si un desarrollo ya existe, se **amplia** su carpeta y su README; no se crea una nueva.
- Carpetas conectadas: si la carpeta no esta conectada a la sesion, se pide acceso con
  `device_request_folder_access` sobre `<carpeta local de proyectos MLR Consultores>`.

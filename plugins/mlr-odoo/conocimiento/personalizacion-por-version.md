# Personalización de Odoo por versión y por tipo de despliegue

Conocimiento que todo agente de personalización carga antes de tocar una base. Verificar en código y en la base demo lo marcado como «verificar».

## Antes de cualquier cambio
1. Versión y edición exactas, tipo de despliegue (SaaS, Odoo.sh, local), módulos instalados y si Studio está licenciado.
2. Inventario de lo que ya existe sobre el modelo objetivo: campos `x_` y de Studio (`x_studio_`), vistas heredadas, automatizaciones y acciones de servidor; nunca duplicar lo que ya hay.
3. Convenciones del cliente: idioma de etiquetas, prefijo técnico, grupos de seguridad existentes, compañías.
4. Base de pruebas o copia neutralizada para la primera ejecución; producción solo con aprobación explícita de cada cambio.
5. Plan de reversión escrito antes de ejecutar: qué registros se crearán y cómo se eliminan.

## Campos
- Vía API: `ir.model.fields.create` con `state='manual'`, `name` con prefijo `x_` obligatorio, `ttype`, `field_description`, `model_id`; relacionales con `relation` (y `relation_field` para one2many); selección como lista de pares; `store`, `copy`, `tracking`, `required`, `readonly`, `help`, `groups`.
- Campos calculados: `compute` con código Python de sandbox, `depends` obligatorio; decidir `store` según uso en búsquedas y reportes; evitar cálculos pesados por registro.
- Monetarios requieren `currency_field`; flotantes con `digits` cuando la precisión importa.
- Traducciones: etiquetas en el idioma del cliente; si la base es multilingüe, cargar la traducción del campo.
- Índices: solo en campos de búsqueda frecuente y con justificación.

## Vistas
- Siempre `ir.ui.view` heredada con `inherit_id` y `mode='extension'`; `arch` con `xpath` mínimos; nunca editar el `arch` de la vista base.
- 17 y posteriores: sin `attrs` ni `states`; usar `invisible`, `readonly`, `required`, `column_invisible` con expresiones; la lista es `<list>` (verificar compatibilidad de `<tree>` en la versión exacta); `decoration-*` y `widget` según versión.
- Botones inteligentes en `div name="button_box"`; pestañas con `page` y `name` propio; filtros y agrupaciones en la vista de búsqueda.
- Después de crear la vista, validar que renderiza (abrir la vista, no solo confiar en el `create`) y que no rompe otras vistas heredadas.

## Modelos nuevos
- `ir.model.create` con `model` con prefijo `x_`, `name` funcional visible; campos estándar (`x_name`, estado, compañía si aplica, activo).
- Permisos: `ir.model.access` por grupo (usuario y responsable); reglas de registro si hay multiempresa.
- Menú y acción de ventana: pedir el menú padre; nombres visibles sin prefijo técnico.
- Máquina de estados con selección y botones por acción de servidor; registrar transiciones en el chatter si el modelo hereda `mail.thread`.

## Lógica: acciones de servidor, automatizaciones y crons
- Acciones de servidor con código Python en sandbox: sin importaciones externas, sin acceso a archivos, con `env`, `model`, `record`/`records`, `log`, `UserError`, `datetime`, `dateutil`, `time`, `json`.
- `base.automation`: disparadores por versión (`on_create_or_write`, `on_time`, `on_unlink`, `on_change`, por etapa, etiqueta o usuario, y webhook en 17+; verificar nombres en la versión); filtro de dominio antes del código; evitar escrituras en el mismo modelo que disparan recursión.
- Crons (`ir.cron`): intervalo, usuario, `numbercall`, código; presupuesto de tiempo por pasada en una constante configurable.
- Código: operaciones en lote, sin búsquedas dentro de bucles, sin `sudo` salvo necesidad documentada, sin identificadores numéricos fijos (usar `env.ref` o búsquedas), sin escribir `state` directamente cuando exista método de transición, mensajes de error claros para el usuario.
- Comentarios: solo junto a constantes configurables, en español, indicando valores admitidos.

## Verificación obligatoria
1. Lectura por API de cada registro creado (campo, vista, acción) con su identificador.
2. Apertura en navegador de la vista afectada y prueba funcional con captura; en 17+ comprobar que la vista compila sin advertencias.
3. Revisión de `ir.logging` por errores posteriores al cambio.
4. Informe en el idioma del cliente con identificadores técnicos, pruebas realizadas y reversión paso a paso.

## SaaS (Odoo Online)
Sin módulos Python ni acceso a servidor; todo vía Studio, `x_` por API o acciones de servidor. Exportar las personalizaciones como módulo (Studio) de forma periódica para respaldo. API externa: XML-RPC y JSON-RPC hasta 18; en 19 la API JSON nueva (`/json/2/<modelo>/<método>`, token Bearer, base en cabecera) y las anteriores marcadas como obsoletas (verificar fecha de retiro vigente).

## Renombres y cambios que rompen personalizaciones
Ver `odoo-versiones.md` del plugin de consultoría: `product_uom` → `product_uom_id`, `res.groups.users` → `user_ids` (19), estados de pago (`cancel` → `canceled` en 19), cambios en `display_type` de líneas, planes analíticos (16), sintaxis de vistas (17).

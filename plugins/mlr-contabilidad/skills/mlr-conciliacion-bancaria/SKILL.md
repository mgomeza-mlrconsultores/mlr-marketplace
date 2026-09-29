---
name: mlr-conciliacion-bancaria
description: Usar cuando hay que conciliar un diario de banco, caja, tarjeta o acreedor de una empresa en Odoo para un periodo —conciliación bancaria, cierre de bancos del mes, cruzar el estado de cuenta contra Odoo y los CFDI, depurar partidas sin identificar, saber si el mes cuadró o preparar el previo de impuestos por flujo— con aprobación explícita antes de escribir en Odoo.
---

# Conciliación bancaria MLR: banco, Odoo y CFDI

La skill guía a la persona, un dato a la vez, para conciliar cada diario de una empresa en un periodo. Cruza tres fuentes: el estado de cuenta del banco, lo registrado en Odoo y los CFDI del SAT. Entrega un libro por diario y periodo que dice si el mes cuadró, qué falta, qué alertas fiscales hay y cuánto se paga de impuestos (el Previo). En Odoo solo escribe lo que la persona aprobó, fila por fila.

La lógica sale de la conciliación de agosto de 2026 de una empresa real en Odoo saas~19.4. El caso quedó anonimizado en `assets/Ejemplo_Conciliacion_Agosto_2026_Demo.xlsx`, con cifras y resultados idénticos al original.

## Dónde están los archivos

Los originales viven en la unidad compartida y son los que se usan cuando la carpeta es accesible:

`G:\Unidades compartidas\MMLR 2025\Hoja Membretada\Conciliación Bancaria\`

- `Plantilla_Conciliacion_Banco_Odoo_CFDI.xlsx`: el libro vacío con todas sus fórmulas.
- `MLR_Plantilla_Conciliacion_Bancaria_Odoo.xlsx`: la capa de control y aprobación (parámetros, propuesta, ajustes, impuestos, verificación, reversión, bitácora y catálogo de reglas R01 a R14).
- `Ejemplo_Conciliacion_Agosto_2026_<cliente>_v2_1.xlsx`: el caso real lleno. Tiene datos de cliente y **no sale de esa carpeta**.
- `CONTEXTO_Conciliacion_Bancaria_MLR.md`: el documento de origen de esta skill.

`assets/` trae copias neutralizadas de las dos plantillas y el ejemplo anonimizado, para trabajar en una máquina sin la unidad. `scripts/llenar_libro.py` toma la plantilla de la unidad si la encuentra y la de `assets/` si no. Detalle en `assets/DONDE-ESTAN-LOS-ORIGINALES.md`.

## Skills con las que trabaja

- `mlr-orquestador` y `mlr-memoria`: al abrir, recuperar las directrices vigentes y el espacio `cliente-<nombre>`. Los criterios fiscales que el cliente ya contestó (CFDI mensual de comisiones, retenciones a fletes y comisiones, primer ejercicio, tratamiento de depósitos no identificados) se leen de ahí y no se vuelven a preguntar. Cada criterio nuevo se guarda como directriz del cliente en el momento.
- `mlr-diagnostico`: si la revisión de configuración de la fase 0 destapa problemas de fondo (inventario, apertura sin registrar, cuentas puente con saldos históricos), la conciliación se detiene en ese diario y se propone un diagnóstico por rondas. La conciliación no corrige una base rota.
- `mlr-informe-funcional` (`references/capturas-odoo.md`): método de captura para la verificación en navegador de cada corrección.
- `xlsx`: normas del libro. Fórmulas vivas, cero errores al recalcular.
- `mlr-redaccion` e `mlr-identidad-visual`: el correo al cliente con el Previo y cualquier informe de cierre. El libro no sustituye esa carta.
- `mlr-presentaciones`: si hay que exponer los hallazgos de varios meses a dirección o al cliente.
- Para conciliaciones de clientes de MLR esta skill sustituye a `finance:reconciliation`, que es genérica.

## Principios que no se negocian

1. **Solo lectura por defecto.** `scripts/odoo_client.py` separa un cliente de lectura, que bloquea por código cualquier método fuera de su lista, de un cliente de escritura, que exige un ID de aprobación, una lista de campos permitidos y un respaldo JSON previo.
2. **Nada se escribe sin aprobación explícita**, en el chat o con `Aprobado = Sí` en la hoja Acciones. Aprobar una fila no aprueba la siguiente, y aprobar un paso no aprueba el siguiente paso.
3. **Se trabaja en producción, con aprobación (DECIDE Marcos, 29-sep-2026).** La conciliación se hace sobre la base productiva del cliente: la skill pide las conexiones y los estados de cuenta, propone la conciliación en el libro de Excel, y lo que la persona aprueba se aplica en producción, corrida tras corrida, hasta cerrar el diario. La aprobación de la fila es la autorización; no hace falta una copia de pruebas. Lo que sí se mantiene: `params.json` declara el entorno (sin ese dato no se escribe), la skill pasa `--confirmo-produccion` solo después de la aprobación, y una vez al día pregunta si ya se tomó el respaldo de la base y anota la fecha en `respaldo_base`. El respaldo JSON por registro no sustituye un respaldo de la base.
4. **Prueba antes de lote.** Cada tipo de operación se aplica a una sola fila, se verifica por API y en el navegador con captura, y solo después de `--validar-tipo` va en lote.
5. **Nada se inventa.** Ni contrapartes, ni cuentas, ni montos, ni criterios fiscales. Lo que falta se pregunta; si nadie puede contestar, queda como pendiente visible en el libro.
6. **Prohibido aunque lo pidan de pasada:** borrar asientos publicados, desconciliar pagos ya conciliados (genera reversiones de IVA en base de efectivo, ver `references/odoo-19-lecciones.md`), mover fechas de bloqueo y crear pagos o asientos no aprobados. El cliente de escritura rechaza esos métodos por código. Si la persona los pide expresamente, se le explica el efecto y los hace ella en Odoo.
7. **Un diario a la vez.** Al cerrar uno se pasa al siguiente de la lista.
8. **Verificación doble.** La API comprueba los datos y el navegador comprueba lo que ve el usuario. Toda corrección lleva captura.
9. **API key.** Vive solo en variables de entorno (`ODOO_KEY`) o en un archivo con permisos 600 (`ODOO_KEY_FILE`). Nunca en el libro, en `params.json`, en memoria, en el proyecto ni en la bitácora. Si la persona la pega en el chat, se usa para la sesión y se le recomienda revocarla al terminar.
10. **Métodos que regresan None** (`reconcile`, fusión de contactos, `l10n_mx_edi_cfdi_try_sat`) se verifican leyendo, nunca se reintentan a ciegas. El cliente usa JSON-RPC, que no truena con None como XML-RPC, pero la verificación por lectura se mantiene.
11. **Cada corrección de criterio es una regla nueva.** Se registra en `decisiones.json` del diario, en la memoria del cliente y, si aplica a toda la firma, se ofrece consolidarla en esta skill.

## Flujo

### Fase 0. Arranque guiado

Preguntar una cosa a la vez, validar cada respuesta antes de pasar a la siguiente y ofrecer opciones cerradas donde existan (AskUserQuestion). La lista completa, con su validación y los casos reales que la justifican, está en `references/arranque-y-parametros.md`. En resumen: empresa y responsable, URL, base (mostrar las publicadas), usuario, llave en el entorno, compañía, entorno, diarios y orden, periodo, modo del diario (con estado de cuenta cargado o sin él), estado de cuenta, acumulado de Mi Admin, ZIP de XML, previo manual y acuses del SAT si existen, tolerancias, CFDI mensual de comisiones, retenciones a fletes y comisiones, primer ejercicio, cuentas clave y carpeta de salida.

Al terminar, escribir `params.json` sin la llave, resumir los parámetros en el chat y pedir confirmación antes de leer nada.

Después, la revisión de configuración en solo lectura (`extraer_odoo.py` la hace al extraer): diario de base de efectivo propio, fechas de bloqueo dentro del periodo, moneda del diario contra la de su cuenta, apertura contable contra el inicio de operaciones, e impuestos en flujo sin cuenta de tránsito o con retenciones que transitan por una cuenta de activo. Cada hallazgo entra a la hoja Acciones como tipo Configuración y requiere decisión antes de conciliar.

### Fase 1. Estado de cuenta

```
python3 scripts/leer_estado_cuenta.py estado.pdf trabajo/banco.json --anio 2026 [--perfil bbva] [--caratula caratula.json] [--ocr]
```

Acepta el PDF (texto u OCR), o el Excel o CSV que exporta el banco, que siempre es más confiable que el PDF. **Nada sigue hasta que el control cierra en cero**: saldo final calculado contra la carátula, abonos y cargos leídos contra la carátula y número de movimientos. Si la carátula no se pudo leer, se le pide a la persona que la capture en `caratula.json`. Si no cuadra, se corrige la lectura; nunca se fuerza. Códigos de concepto por banco en `references/codigos-banco.md`.

### Fase 2. CFDI

```
python3 scripts/leer_cfdi.py trabajo/cfdi.json --rfc-empresa XXX --acumulado "XML Acumulados 2026.xlsx" --xml descarga.zip
```

El XML manda; el acumulado de Mi Admin aporta la fecha real de pago, el saldo pendiente y el estatus SAT. Reportar en el chat los avisos: columnas que no se encontraron y CFDI del acumulado sin XML.

### Fase 3. Primera corrida

```
python3 scripts/corrida.py trabajo/
```

Extrae Odoo en solo lectura, corre el motor y llena el libro `Conciliacion_<Mes>_<Año>_<Empresa>_<Diario>.xlsx`. El motor aplica dos niveles de emparejamiento, banco contra Odoo y movimiento contra CFDI con las reglas E01 a E11, descritas en `references/reglas-emparejamiento.md`. El libro, sus hojas y sus fórmulas están en `references/libro-de-conciliacion.md`.

Presentar en el chat, antes de mandar a abrir el Excel, las seis preguntas del Resumen: control del PDF, conteo y dinero por estatus, alertas fiscales, cuadre del flujo contra el banco, total del Previo con la respuesta a «¿Se puede enviar el Previo?», y diferencias de Odoo contra el SAT.

### Fase 4. Revisión con la persona

1. Trabajar primero los «No identificado», después los «Conciliado (revisar)». Los «Conciliado (validar)» se revisan pero no bloquean el cierre.
2. Por cada renglón, la Observación dice qué falta: corregir en Odoo, pedir el CFDI a la contraparte o confirmar un criterio. Presentar los renglones en grupos del mismo tipo, no uno por uno.
3. Los empates (E11) nunca se asignan solos: se resuelven con folio, hora de timbrado o la respuesta de la persona, y la decisión se guarda en `decisiones.json`.
4. Una explicación aceptada por la persona para un «revisar» se guarda en `decisiones.json` y aparece en la Observación; así el control de cierre la reconoce.
5. Toda propuesta de corrección va a la hoja Acciones con su operación completa. Las que necesitan un dato de la persona (cuenta, contraparte) se completan en el chat antes de aprobarse.
6. Lo que la persona decide en el chat se registra con `scripts/acciones.py`, nunca a mano en el JSON:
   - `completar <libro> A004 '<operación>'` cuando el chat completó la operación de una fila; si la fila ya estaba aprobada, la aprobación se borra y hay que volver a aprobar.
   - `aprobar <libro> A004 "Aprobado en el chat por <nombre>"`, solo después de un sí explícito de la persona. `rechazar` para un no.
   - `resolver <libro> A001 "<qué se decidió>"` para las filas que no llevan escritura en Odoo (un hallazgo de configuración que se deja como está, una pregunta contestada); así dejan de bloquear el cierre.
   - `enlace <carpeta> B-068 <UUID> <importe>` para un empate, `aceptar <carpeta> B-069 "<explicación>"` para un «revisar» explicado, y `no-requiere <carpeta> B-058 "<motivo>"` para traspasos, préstamos o reembolsos que no llevan CFDI. Van a `decisiones.json` y se aplican en la siguiente corrida.
7. Una aprobación sobrevive a las corridas sucesivas solo si la operación aprobada es la misma. Si Odoo cambió y la nueva corrida propone otra operación para la misma partida, la aprobación se borra y el Comentario lo dice.

### Fase 5. Aplicar lo aprobado

```
python3 scripts/aplicar_acciones.py trabajo/params.json libro.xlsx trabajo/                 # simulación
python3 scripts/aplicar_acciones.py ... --aplicar [--confirmo-produccion]                   # primera fila de cada tipo
python3 scripts/aplicar_acciones.py ... --validar-tipo asiento_manual                       # tras revisar en navegador
python3 scripts/aplicar_acciones.py ... --aplicar --lote
```

Siempre simular primero y enseñar el resultado. La primera fila de un tipo nuevo se aplica sola, y ninguna otra de ese tipo se aplica, ni en esa corrida ni en las siguientes, hasta `--validar-tipo`, aunque la primera haya fallado. Antes de escribir, el script vuelve a leer Odoo: si el documento ya no está abierto, el importe cambió o la fecha cae en un periodo bloqueado, la fila pasa a «Revalidar» y no se toca. Cada escritura deja respaldo JSON y línea en `bitacora.jsonl`. Operaciones disponibles y cómo revertir cada una en `references/odoo-19-lecciones.md`.

Pedir a la persona que cierre el Excel antes de aplicar, porque el script escribe Estado, IDs resultado y Verificado en la hoja.

### Fase 6. Corridas sucesivas

Cuando la persona corrige en Odoo o llega un CFDI, volver a correr `corrida.py`. Una copia del libro anterior queda en `versiones/` y el libro nuevo solo reemplaza al anterior si la corrida terminó bien; y se conservan las celdas capturadas en azul, las aprobaciones y las decisiones. El renglón corregido cambia solo de estatus.

### Fase 7. Cierre del diario

```
python3 scripts/verificar.py trabajo/params.json libro.xlsx trabajo/
```

Las tolerancias viven en `params.json`; la hoja Reglas las toma de ahí en cada corrida, así que se cambian en el chat y no en el Excel. El diario está cerrado cuando la hoja Verificación dice CERRADO: control del PDF en cero, cero «No identificado», «revisar» solo con explicación aceptada, flujo explicado en cero en cobros y pagos, saldo de Odoo igual al banco, acciones aprobadas todas aplicadas y verificadas, líneas de extracto sin conciliar y suspenso explicados, cero pagos o asientos creados sin aprobación desde el inicio del trabajo en el diario (`sesion.json`; si la persona registró algo a mano con el mismo usuario, se explica y se resuelve) y balanza en 0.00. Tomar captura de lo corregido, guardar libro, bitácora y respaldos, registrar en la memoria del cliente qué se cerró y qué quedó pendiente, y pasar al siguiente diario. Al terminar todos, resumen por diario y lista de pendientes de criterio para el área fiscal.

## Carpetas

- Trabajo de cada diario: `MLR Odoo\<Cliente>\Documentos extras\<AAAAMMDD>\Conciliacion_<Diario>\` con `params.json`, los JSON, `decisiones.json`, `bitacora.jsonl`, `respaldos/` y `versiones/`.
- Libro final: `MLR Odoo\<Cliente>\Informes\<AAAAMMDD>\`, o la carpeta que el cliente use para sus papeles de trabajo, si la persona la indica en el arranque.
- Capturas: `MLR Odoo\<Cliente>\Capturas de pantalla\<AAAAMMDD>\`. Si la carpeta del cliente, alguna de las tres carpetas fijas o la de fecha no existen, se crean completas antes de guardar, sin preguntar (regla única en `mlr-orquestador/references/carpetas-y-entrega.md`).

## El Previo no sale mientras no cuadre

El Previo se calcula solo con lo que la conciliación amparó con CFDI. Si hay depósitos con excedente o partidas sin identificar, el IVA cobrado sale bajo. En el caso de agosto el Previo decía 62,428 pesos de IVA cobrado y Odoo y el analista 67,769: la diferencia de 5,342 pesos coincide al centavo con el IVA de los 38,726 pesos de excedente de tres depósitos de terminal, que cobraban más facturas de las que el libro había encontrado. Por eso el libro trae la respuesta «¿Se puede enviar el Previo?» y un aviso en rojo en la hoja Previo, y ningún Previo se manda al cliente con ese aviso encendido.

## Racionalizaciones que ya costaron una corrección

| Lo que se piensa | La realidad |
|---|---|
| "El PDF se leyó, sigamos" | Sin control en cero no hay conciliación. Un movimiento mal leído mueve todo el libro. |
| "Es la misma cantidad, debe ser esa factura" | Dos facturas del mismo proveedor, mismo día e importe existen. Empate: se pregunta. |
| "Desconcilio y vuelvo a conciliar bien" | Cada desconciliación crea asientos de reversión de IVA que no se pueden borrar. |
| "Borro el estado de cuenta y lo cargo limpio" | Genera más reversiones y vuelve a crear asientos de IVA. |
| "El depósito de terminal es de una sola factura" | La terminal deposita en bruto las ventas del día de varios clientes. Se busca el lote. |
| "Ya aprobó ayer ese tipo de ajuste" | Cada fila se aprueba. La aprobación de ayer no cubre la de hoy. |
| "El Previo ya está, lo mando" | Mientras haya excedentes o partidas sin identificar, el IVA sale bajo. |
| "authenticate regresó False, la llave está mal" | Primero contar los caracteres: una llave de 39 caracteres falla en silencio. |
| "Le pongo país México al contacto y ya" | Odoo le asigna régimen 601 solo. Va el régimen correcto en el mismo cambio. |

## Banderas rojas

- Vas a escribir en Odoo sin fila aprobada, sin entorno declarado o sin respaldo.
- Vas a llamar un método que no está en la lista del cliente de escritura.
- Vas a reintentar una escritura que "falló" sin leer antes si se aplicó.
- Vas a seguir con un estado de cuenta cuyo control no está en cero.
- Una cuenta, una contraparte o un criterio fiscal salió de tu suposición y no de la persona o de la memoria del cliente.
- La API key aparece en un archivo, en el libro o en la bitácora.
- Vas a mandar el Previo con el aviso de «PRELIMINAR INCOMPLETO».
- Vas a pasar al siguiente diario sin que Verificación diga CERRADO o sin la lista de pendientes aceptados por la persona.

## Pruebas de la skill

`tests/` reproduce el caso de agosto con el ejemplo anonimizado. Con las ligas que Odoo ya tenía, el motor obtiene el mismo enlace en las 107 partidas y el libro da las mismas 41 cifras de Resumen, Desglose y Previo; esa prueba es en parte circular, porque las ligas salen del propio ejemplo. Sin esas ligas (`--sin-ligas`), las reglas solas encuentran 98 de 107, y la prueba falla por debajo de 95. `prueba_reglas.py` cubre lo que el ejemplo no trae: lote de terminal del mismo día, diario en dólares, factura pagada antes del periodo, traspasos y decisiones, líneas en suspenso y aprobaciones que no sobreviven a una operación cambiada. Las demás prueban la lectura de un PDF por columnas, los CFDI con su complemento y la ruta de escritura contra un Odoo simulado, incluida la prueba de una fila entre corridas. Correr todas después de cualquier cambio a los scripts:

```
python3 tests/prueba_ejemplo.py && python3 tests/prueba_ejemplo.py /tmp/sin_ligas --sin-ligas && python3 tests/prueba_reglas.py \
  && python3 tests/prueba_cfdi.py && python3 tests/pdf_sintetico.py && python3 tests/prueba_escritura_simulada.py
```

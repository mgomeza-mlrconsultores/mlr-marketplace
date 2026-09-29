# Arranque guiado y params.json

Una pregunta a la vez, en este orden. Cada respuesta se valida antes de pasar a la siguiente. Antes de preguntar un criterio, buscarlo en la memoria del cliente (`contexto cliente <nombre>`): si ya está contestado, se muestra y se confirma en una línea, no se vuelve a preguntar.

| # | Dato | Cómo se valida | Caso real que lo justifica |
|---|---|---|---|
| 1 | Empresa y responsable | Informativo | |
| 2 | URL de Odoo | `/jsonrpc` servicio `common.version()` responde; se anota `server_version` | saas~19.4+e |
| 3 | Base de datos | Se listan las bases publicadas (`POST URL/web/database/list`) y la persona elige | Dieron un nombre de base que no existía; la única publicada era otra |
| 4 | Usuario | Formato de correo | |
| 5 | API key | La persona la pone en `ODOO_KEY` o en un archivo 600 (`ODOO_KEY_FILE`); el cliente revisa que tenga 40 caracteres hexadecimales antes de autenticar y que `authenticate()` regrese un uid | Una llave de 39 caracteres hacía que `authenticate()` regresara `False` sin mensaje |
| 6 | Compañía | Lista de `res.company`; si hay varias, se fija `compania_id` y todo se lee con `allowed_company_ids` | |
| 7 | Entorno | Normalmente producción: lo aprobado en el libro se aplica ahí. Antes de la primera escritura de cada día, preguntar si ya se tomó el respaldo de la base y anotar la fecha en `respaldo_base` | La conciliación de agosto se hizo sobre la base productiva |
| 8 | Diarios y orden | Lista de diarios `bank`, `cash` y `credit` con su cuenta por defecto; la persona marca cuáles y en qué orden | |
| 9 | Periodo | Fechas válidas; aviso si una fecha de bloqueo cae dentro | |
| 10 | Modo del diario | `con_estado` (estados de cuenta cargados en Odoo) o `sin_estado` (pagos manuales durante el mes y conciliación al cierre). No se crean ni se modifican líneas de estado de cuenta si la persona no lo pide | La empresa del ejemplo no carga estados de cuenta |
| 11 | Estado de cuenta | PDF, o mejor el Excel o CSV del banco. Debe cuadrar con la carátula (`leer_estado_cuenta.py`) | |
| 12 | Acumulado de XML de Mi Admin | Hojas ACUM. EMITIDOS, ACUM. RECIBIDOS, PAGOS EMITIDOS, PAGOS RECIBIDOS | |
| 13 | ZIP de XML (recomendado) | Se indexa por UUID leyendo el TimbreFiscalDigital; da el régimen del emisor, que el acumulado no trae | |
| 14 | Previo manual o papel de trabajo (opcional) | Solo mientras se prueba la skill con un cliente nuevo: llena el comparativo del Previo | |
| 15 | Acuses y líneas de captura del SAT (opcional) | Carpeta del mes con LC, Detalle y Comprobante de pago | Desglose de los pagos P14 |
| 16 | Tolerancias | Por defecto 1.00 peso y 3 días; se cambian en la hoja Reglas | |
| 17 | ¿El banco emite CFDI mensual de comisiones? | Sí: comisiones e IVA van como «No requiere CFDI». No: el IVA de comisiones no es acreditable y se pregunta la cuenta | Criterio distinto en dos momentos del mismo cliente |
| 18 | Retención de IVA a fletes (4 %) y a comisiones (2/3) | Se pregunta si aplican; mientras no, queda «por confirmar criterio» | |
| 19 | ¿Primer ejercicio? | Si sí, fecha de inicio de operaciones: el Previo lleva la nota del art. 14 LISR, por confirmar | La empresa inició el 5 de mayo de 2026 |
| 20 | Cuentas clave | Se leen del catálogo y se confirman una por una (tabla de abajo) | |
| 21 | Carpeta de salida | Por defecto la estructura MLR; la persona puede indicar la carpeta de papeles de trabajo del cliente | |

Al terminar, resumir los parámetros sin la llave y pedir confirmación antes de leer Odoo.

## params.json

Lo escribe la skill en la carpeta de trabajo del diario. Nunca lleva la llave. `entorno` es obligatorio para escribir; en producción, `respaldo_base` debe tener la fecha del día en que la persona respaldó la base, o `aplicar_acciones.py` no escribe. `cuentas_sin_cfdi` lista prefijos de cuenta cuya contrapartida no lleva CFDI (préstamos y reembolsos de socios, inversiones propias); los traspasos entre bancos propios se reconocen solos.

```json
{
  "empresa": "Clínica Demo Terapia SA de CV", "empresa_corta": "Clínica Demo", "rfc_empresa": "CDT260505AB1",
  "compania_id": 1, "diario_id": 13, "diario": "BBVA", "cuenta_banco": "0100000001", "banco": "BBVA México",
  "desde": "2026-08-01", "hasta": "2026-08-31", "entorno": "produccion", "respaldo_base": "2026-09-29", "modo_diario": "sin_estado",
  "tolerancia_importe": 1.0, "tolerancia_dias": 3, "ventana_busqueda_dias": 45,
  "banco_emite_cfdi_comisiones": true, "retencion_fletes": "por confirmar", "retencion_comisiones": "por confirmar",
  "primer_ejercicio": true, "inicio_operaciones": "2026-05-05",
  "cuentas": {"iva_acreditable_pagado": "118.01.01", "iva_trasladado_cobrado": "208.01.01", "comisiones": "701.10.01",
              "iva_comisiones": "118.01.01", "no_deducibles": "601.83.01", "otros_ingresos": "403.01.01",
              "otros_gastos": "601.84.01", "recargos": "601.84.04", "iva_a_favor": "113.01.01", "iva_por_pagar": "213.01.01",
              "clientes": "105.01.01", "proveedores": "201.01.01"},
  "cuentas_sin_cfdi": {"205.02": "Movimiento con acreedor socio: se ampara con su comprobación", "103.01": "Inversión propia"},
  "previo_manual": {"iva_cobrado": 67769.22, "iva_pagado": 13411.89, "iva_retenido": 744.54, "isr_retenido": 175.70},
  "lista_69b": "ruta/opcional/Listado_Completo_69-B.csv"
}
```

## Cuentas que se confirman en cada empresa

| Uso | Cuenta en el caso de agosto |
|---|---|
| Banco | 102.01.01 |
| Suspenso | 102.01.02 |
| Clientes / Proveedores | 105.01.01 / 201.01.01 |
| IVA a favor | 113.01.01 |
| IVA acreditable pagado / pendiente | 118.01.01 / 119.01.01 |
| IVA trasladado cobrado / no cobrado | 208.01.01 / 209.01.01 |
| IVA por pagar | 213.01.01 |
| ISR retenido honorarios / pendiente de pago | 216.04.01 / 216.04.02 |
| IVA retenido pendiente / pagado | 216.10.10 / 216.10.20 |
| Acreedores diversos por socio | 205.02.xx |
| Otros ingresos, redondeo a favor | 403.01.01 |
| No deducibles | 601.83.01 |
| Otros gastos, redondeo en contra | 601.84.01 |
| Recargos y actualizaciones | 601.84.04 |
| Comisiones bancarias | 701.10.01 |
| Base de impuestos en flujo | 899.01.99 |

## Variables de entorno

```
ODOO_URL=https://empresa.odoo.com  ODOO_DB=empresa  ODOO_USER=usuario@mlrconsultores.com
ODOO_KEY=<40 hex>  (o ODOO_KEY_FILE=~/.odoo_key con chmod 600)  ODOO_COMPANY_ID=1
```

Se definen en la terminal de la sesión o en la configuración del conector; no se escriben en ningún archivo que se vaya a archivar.

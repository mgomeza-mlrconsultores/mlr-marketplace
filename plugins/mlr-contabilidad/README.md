# MLR Contabilidad

Procesos contables de MLR Consultores sobre Odoo. Hoy instala una skill; el plugin está pensado para crecer con los demás procesos de cierre (determinación de impuestos, DIOT, depuración de contactos).

## Qué instala

**`mlr-conciliacion-bancaria`** — Guía a la persona, un dato a la vez, para conciliar cada diario de banco, caja, tarjeta o acreedor de una empresa en un periodo. Cruza el estado de cuenta (PDF, Excel o CSV), lo registrado en Odoo y los CFDI del SAT (acumulado de Mi Admin y XML, con sus complementos de pago). Entrega un libro por diario y periodo que dice si el mes cuadró, qué falta, qué alertas fiscales hay y cuánto se paga de impuestos, y responde si el Previo ya se puede mandar al cliente. En Odoo solo escribe lo aprobado fila por fila, con revalidación, respaldo, bitácora, prueba de una fila antes del lote y verificación en navegador.

Trae los scripts que hacen el trabajo (lectura del estado de cuenta con control de carátula, lectura de CFDI, extracción de Odoo en solo lectura, motor de emparejamiento, llenado del libro con tablas del tamaño real del mes, aplicación de acciones aprobadas y controles de cierre) y cuatro pruebas que reproducen al centavo un caso real anonimizado.

## Con qué trabaja

- **`mlr-orquestador`** (plugin de la firma): enruta aquí toda petición de conciliación, y aporta memoria de cliente y de firma, redacción, identidad visual y archivo. Sin él la skill funciona, pero no recuerda los criterios fiscales de cada cliente.
- Skills `xlsx` y de captura en navegador para el libro y la verificación visual.

## Originales

Las plantillas y el caso real viven en la unidad compartida, `MMLR 2025 > Hoja Membretada > Conciliación Bancaria`. El plugin trae copias neutralizadas y un ejemplo anonimizado; el caso real no sale de la unidad. Ver `skills/mlr-conciliacion-bancaria/assets/DONDE-ESTAN-LOS-ORIGINALES.md`.

## Requisitos

Python 3 con `openpyxl`, `lxml` y `pdfplumber`; LibreOffice para recalcular y revisar el libro antes de entregarlo; `ocrmypdf` solo para estados de cuenta escaneados. La conexión a Odoo va por variables de entorno (`ODOO_URL`, `ODOO_DB`, `ODOO_USER`, `ODOO_KEY` u `ODOO_KEY_FILE`); la llave nunca se escribe en archivos.

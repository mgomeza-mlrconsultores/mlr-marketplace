# Fase 1 — Lo que dijo el cliente y lo que dice la base

Dos fuentes primarias. Ninguna sustituye a la otra.

## 0. La reunión se conduce con el cuestionario

Antes de la reunión de descubrimiento se imprime o se abre el libro de captura, y se llena
**en vivo, delante del cliente**. Lo que no quede registrado ahí, no se cotiza.

- `scripts/preguntas.py` — origen único de las preguntas: ficha del sistema, 17 bloques por
  aplicación y cierre. Si una pregunta cambia, cambia aquí y se regeneran los dos documentos.
- `scripts/libro.py` — genera el libro de captura en Excel, con casillas, listas cerradas y
  una hoja de resumen que cuenta sola los detonantes de costo.
- `scripts/guia.py` — genera la guía de la reunión en formato MLR, con el reparto de los 30
  minutos y como se conduce.

El recorrido obligatorio —ficha, contabilidad, facturación, ventas, compras, inventario y
cierre— suma **30 minutos exactos**. Los otros doce bloques son condicionales y solo se
abren si el cliente los menciona.

**El orden no es arbitrario.** Contabilidad y facturación van primero porque en México el
comprobante fiscal, el catálogo de cuentas y el número de razones sociales condicionan la
configuración de todo lo demás; definirlos al final obliga a rehacer.

Cada bloque de aplicación arranca con la misma espina dorsal, que son las cuatro respuestas
que mueven el precio: donde vive hoy el proceso, que volumen tiene, que hay que migrar, y
que de eso **no** se resuelve como lo hace Odoo de fabrica. La cuarta es la que destapa el
desarrollo y la que mas se olvida.

## 1. Lectura de la transcripción

Extraer y dejar por escrito en el chat, en este orden:

1. **Giro y operación real.** Que compra, que transforma, que vende, en que unidad y a quien.
2. **Escala física.** Sedes, almacenes, puntos de venta, terminales, personas por área.
3. **Dolores declarados.** Lo que hoy se lleva en papel, en Excel o en la cabeza de alguien.
4. **Peticiones explicitas.** Lo que el cliente pidió con esas palabras.
5. **Exclusiones declaradas.** Lo que dijo que no quiere o que no toca ahora.
6. **Compromisos de terceros.** Lo que el cliente afirma sobre proveedores, etiquetas, equipos o sistemas que no controlamos.

Los puntos 4, 5 y 6 se citan casi textuales. Son la defensa del alcance cuando aparezca la ampliación.

Lo que el cliente afirma sobre un tercero se registra como afirmación del cliente, no como hecho. Si el proyecto depende de eso — por ejemplo, que la etiqueta del proveedor sea única y no se repita — se convierte en supuesto explicito de la propuesta.

## 2. Diagnóstico de la base

La auditoria de la base —versión, módulos, datos, customizaciones previas, estructura de
compania— y la verificación de comportamiento contra el código de la versión exacta viven
en la skill hermana `mlr-diagnostico`. Se carga ahí, se corre con su método de rondas y
aquí solo se usa el resultado.

Lo que la cotización toma del diagnóstico:

- Versión y edición exactas. En Online no hay filesystem ni módulos propios, y eso cambia el alcance.
- Módulos instalados: lo que ya está pagado y lo que hay que activar.
- Volumen real de datos. Un catálogo cargado a medias cuesta mas que uno vacío.
- Customizaciones previas y lo que se rompe en la versión vigente.
- Hallazgos que obligan a depurar o reconstruir: cada uno puede ser una tarea de la ruta.

Cuando el proyecto depende de que Odoo haga algo especifico, se prueba en la base de pruebas
o se lee en el código de la versión exacta, con el mismo estándar de evidencia del
diagnóstico. Si el código dice que no existe, se declara desarrollo y se cotiza como
desarrollo.

Código fuente de Odoo disponible localmente en:

`G:\Unidades compartidas\Marcos 2026\Marcos 2026\Trabajo\MLR Consultores\Quimibond\Codigo BD\mi_codigo_quimibond`

Sin conexión todavía, la fase se declara incompleta y se dice en el chat. No se cotiza a ciegas.

## 3. Salida de la fase

Tres listas en el chat, nada mas:

- **Aplicaciones dentro del alcance**, con una línea de para que entra cada una.
- **Fuera del alcance**, con el motivo: no lo pidió, va en otra iguala, es estándar sin cambios, o depende de algo que no está listo.
- **Supuestos**, numerados. Cada supuesto que se caiga es una ampliación, y por eso van escritos.

Cierre: preguntar a Marcos si las tres listas quedan así antes de pasar a las preguntas.

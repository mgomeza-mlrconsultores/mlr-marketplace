# Fase 1 — Lo que dijo el cliente y lo que dice la base

Dos fuentes primarias. Ninguna sustituye a la otra.

## 0. La reunion se conduce con el cuestionario

Antes de la reunion de descubrimiento se imprime o se abre el libro de captura, y se llena
**en vivo, delante del cliente**. Lo que no quede registrado ahi, no se cotiza.

- `scripts/preguntas.py` — origen unico de las preguntas: ficha del sistema, 17 bloques por
  aplicacion y cierre. Si una pregunta cambia, cambia aqui y se regeneran los dos documentos.
- `scripts/libro.py` — genera el libro de captura en Excel, con casillas, listas cerradas y
  una hoja de resumen que cuenta sola los detonantes de costo.
- `scripts/guia.py` — genera la guia de la reunion en formato MLR, con el reparto de los 30
  minutos y como se conduce.

El recorrido obligatorio —ficha, contabilidad, facturacion, ventas, compras, inventario y
cierre— suma **30 minutos exactos**. Los otros doce bloques son condicionales y solo se
abren si el cliente los menciona.

**El orden no es arbitrario.** Contabilidad y facturacion van primero porque en Mexico el
comprobante fiscal, el catalogo de cuentas y el numero de razones sociales condicionan la
configuracion de todo lo demas; definirlos al final obliga a rehacer.

Cada bloque de aplicacion arranca con la misma espina dorsal, que son las cuatro respuestas
que mueven el precio: donde vive hoy el proceso, que volumen tiene, que hay que migrar, y
que de eso **no** se resuelve como lo hace Odoo de fabrica. La cuarta es la que destapa el
desarrollo y la que mas se olvida.

## 1. Lectura de la transcripcion

Extraer y dejar por escrito en el chat, en este orden:

1. **Giro y operacion real.** Que compra, que transforma, que vende, en que unidad y a quien.
2. **Escala fisica.** Sedes, almacenes, puntos de venta, terminales, personas por area.
3. **Dolores declarados.** Lo que hoy se lleva en papel, en Excel o en la cabeza de alguien.
4. **Peticiones explicitas.** Lo que el cliente pidio con esas palabras.
5. **Exclusiones declaradas.** Lo que dijo que no quiere o que no toca ahora.
6. **Compromisos de terceros.** Lo que el cliente afirma sobre proveedores, etiquetas, equipos o sistemas que no controlamos.

Los puntos 4, 5 y 6 se citan casi textuales. Son la defensa del alcance cuando aparezca la ampliacion.

Lo que el cliente afirma sobre un tercero se registra como afirmacion del cliente, no como hecho. Si el proyecto depende de eso — por ejemplo, que la etiqueta del proveedor sea unica y no se repita — se convierte en supuesto explicito de la propuesta.

## 2. Auditoria de la base por API

Conexion por JSON-RPC. Lo que se lee, siempre:

- **Version y edicion exactas.** Mayor, menor, Community o Enterprise, on-premise, Odoo.sh u Online. El alcance cambia con esto: en Online no hay filesystem ni modulos propios.
- **Modulos instalados.** `ir.module.module` con estado. Distingue lo que ya esta pagado de lo que hay que activar.
- **Datos existentes.** Volumen real de productos, contactos, listas de precio, movimientos. Un catalogo cargado a medias cuesta mas que uno vacio: hay que revisarlo y refinarlo.
- **Customizaciones previas.** Campos `x_`, vistas heredadas, `base.automation`, `ir.cron`, acciones de servidor. Es donde se esconde el trabajo del implementador anterior.
- **Estructura de compania.** Companias activas, almacenes, ubicaciones, diarios.

Sin conexion todavia, la fase se declara incompleta y se dice en el chat. No se cotiza a ciegas.

## 3. Verificacion de comportamiento

Cuando el proyecto depende de que Odoo haga algo especifico — escaneo que actualiza el documento primario, peso variable por paquete, fabricacion disparada por llegada — no se afirma: se prueba.

Orden de verificacion:

1. Reproducirlo en la base de pruebas por API, punta a punta, con datos reales del caso.
2. Si no se reproduce, leer el codigo fuente de la version exacta.
3. Si el codigo dice que no existe, se declara desarrollo y se cotiza como desarrollo.

Codigo fuente de Odoo disponible localmente en:

`G:\Unidades compartidas\Marcos 2026\Marcos 2026\Trabajo\MLR Consultores\Quimibond\Codigo BD\mi_codigo_quimibond`

La verificacion visual va siempre por navegador. El API cambia y comprueba datos; el navegador comprueba lo que ve el usuario.

## 4. Salida de la fase

Tres listas en el chat, nada mas:

- **Aplicaciones dentro del alcance**, con una linea de para que entra cada una.
- **Fuera del alcance**, con el motivo: no lo pidio, va en otra iguala, es estandar sin cambios, o depende de algo que no esta listo.
- **Supuestos**, numerados. Cada supuesto que se caiga es una ampliacion, y por eso van escritos.

Cierre: preguntar a Marcos si las tres listas quedan asi antes de pasar a las preguntas.

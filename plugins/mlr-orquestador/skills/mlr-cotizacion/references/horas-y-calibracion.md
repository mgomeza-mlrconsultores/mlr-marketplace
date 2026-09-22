# Fases 5 y 6 — Horas, calibracion y condiciones economicas

## Las horas van al final

Primero la ruta cerrada y aprobada. Despues las horas. Estimar mientras se define el alcance produce numeros que defienden la ruta en lugar de medirla.

## Calibracion contra horas reales

Las horas no se estiman por intuicion. Se comparan contra el registro de horas reales de proyectos MLR ya ejecutados. Referencias utiles del registro Taiga (horas reales, no estimadas):

| Trabajo | Horas reales |
|---|---|
| Categorias de producto | 8 |
| Catalogo de productos | 33.5 |
| Listas de materiales | 34.5 |
| Contactos | 3 |
| Unidades de medida | 6 |
| Levantamiento fisico de inventario | 6 |
| Rutas multietapa | 25.5 |
| Costes en destino | 2 |
| Carga de existencias iniciales | 34 |
| Aprobacion por monto minimo | 1 |
| Tarifas de proveedor | 3 |
| Equipos de venta | 2 |
| Listas de precio | 8.5 |
| Configuracion de fabricacion (bloque completo) | 39 |

Lecturas que hay que retener de ese registro: los datos maestros y la carga inicial pesan mucho mas de lo que parece, y las tareas de configuracion puntual pesan mucho menos. Quien estima al reves se equivoca en las dos direcciones a la vez.

Proyecto de referencia completo: 206 horas reales sobre 42 tareas.

Cotizaciones cerradas que sirven de calibracion:

| Proyecto | Situacion de partida | Horas | Tareas | Aplicaciones |
|---|---|---|---|---|
| Taiga | ejecutado, horas reales | 206 | 42 | — |
| Aire Libre LATAM | implantacion nueva, 3 empresas, catalogo menor a 500 productos | 250 | 40 | 8 |
| Dunedin | base viva en produccion, 1 empresa, 5 almacenes, 29 rutas de venta | 264 | 50 | 10 |
| Ah Cacao | base viva, 8 companias a consolidar en una, 8 almacenes, 12 cajas, 1,373 productos, fabricacion activa | 215 | 48 | 11 |

## Base viva contra implantacion nueva

Es el ajuste que mas se equivoca. Cuando el cliente ya opera sobre Odoo, los datos maestros **ya existen**: productos cargados, categorias con su valuacion, contactos con su RFC, almacenes construidos. Cotizar eso como si hubiera que crearlo infla la ruta entre un tercio y la mitad, y se cae en cuanto el cliente abre su propia base.

En una base viva se cotiza:

- **Depuracion** de lo que esta incompleto: productos sin codigo o sin costo, contactos sin dato fiscal, existencias negativas, documentos en rezago.
- **Reconstruccion** de lo que esta mal resuelto: automatizaciones que suplen configuracion, catalogos de cuentas usados como dimension, listas de precio de precio fijo replicadas por cliente.
- **Retiro** de lo que sobra, que casi siempre cuesta mas que construir de cero porque hay que sostener la operacion mientras se quita.

Y no se cotiza lo que ya funciona. Antes de escribir una hora de una aplicacion hay que abrir la base y ver si esa aplicacion ya esta resuelta. Si lo esta, se dice en la propuesta que queda fuera porque opera correctamente: es argumento de venta, no renuncia.

## Reglas de asignacion

- Ninguna tarea baja de 0.5 h ni sube de 16 h. Lo que pasa de 16 h esta mal partido.
- Una tarea que dura minutos no lleva horas propias: se absorbe.
- La replica por sede se cotiza como replica, con una hora unitaria menor que la primera configuracion.
- La capacitacion se cotiza por sesion agrupada por tema y rol, con su preparacion incluida.
- El desarrollo lleva analisis, construccion, prueba y documentacion dentro de la misma cifra.

## Techo de horas impuesto

Cuando Marcos o el cliente fijan un techo por debajo de la estimacion:

1. Se dice con claridad que el techo exige recortar alcance, y se sostiene con la evidencia del registro real.
2. Se presenta la lista de lo que sale, no una version adelgazada de todo.
3. Se marca lo que **no** puede salir: procesos criticos como la carga inicial de inventario no se le trasladan al cliente para cuadrar un numero.
4. Decide Marcos. Una vez decidido, se ejecuta sin reabrir el debate.

Recortar minutos a cada renglon para llegar al numero es falsificar la ruta.

## Contingencia

Se calcula y se distribuye por tarea en un archivo de uso interno de MLR. **Nunca aparece en un entregable del cliente**: ni como renglon, ni sumada a las horas publicadas, ni mencionada en el texto.

## Condiciones economicas

- **Tarifa de lista** y, cuando aplique, **tarifa preferencial** con fecha limite explicita. Se muestra el ahorro en importe.
- **Tarifas vigentes 2026, diferenciadas por tipo de trabajo.** No se cotiza todo al mismo precio: el cliente paga tarifa de consultoria senior solo en lo que la requiere, y eso se muestra en la propuesta como cuadro propio. La vigencia de la preferencial corre al 30 de septiembre para todos los clientes.

| Rango | Tipos de trabajo que lo componen | Preferencial | Lista |
|---|---|---|---|
| Configuracion y migracion de datos | Configuracion, Datos | 1,100 | 1,300 |
| Diseno y definicion contable | Entregable (definicion, arquitectura, regularizaciones, reportes fiscales) | 1,700 | 1,950 |
| Capacitacion y acompanamiento | Capacitacion, Puesta en marcha, Aceptacion, manuales | 1,200 | 1,400 |
| Desarrollo a medida | Desarrollo | 1,400 | 1,600 |

  Por que asi: el grueso de un proyecto es configuracion y datos, y ese renglon es el que el cliente compara contra otras ofertas. Bajarlo a 1,100 deja la propuesta competitiva en lo comparable sin regalar el trabajo de criterio, que es donde esta el valor de la firma y el contador socio. El desarrollo va por encima de la configuracion porque es lo mas caro de producir y lo unico que hay que reconstruir en cada salto de version mayor, y por debajo de la definicion contable porque ahi el valor lo pone el criterio del contador socio y no las horas de construccion.

  El promedio ponderado resultante ronda 1,230 MXN por hora en un proyecto tipico. El importe de cada hito se calcula con la tarifa del rango de cada tarea, no con el promedio: por eso un hito corto y de mucha definicion sale mas caro por hora que uno largo de configuracion, y eso se deja ver.

- **Nunca se compara el precio con el paquete de implementacion de Odoo en un entregable del cliente.** Odoo publica su precio por hora en pesos y es menor; meter la comparacion en la propuesta invita a discutir tarifa en lugar de alcance. La diferenciacion por rangos cumple la misma funcion sin nombrar a nadie.
- **Dos modalidades de pago, siempre las dos**: A, anticipo del 30% contra firma y saldo contra aceptacion de cada hito; B, pagos mensuales iguales sin anticipo. Un cuadro por modalidad.
- **Horas efectivas de consultoria, no dias naturales.** El plazo va en su propio apartado y no se deriva de las horas.
- **Configuracion contable e iguala son cosas distintas.** La configuracion contable del sistema entra en la propuesta: se cobra cuando es el peso del proyecto, o se declara incluida sin costo cuando se usa como beneficio comercial. El servicio contable recurrente siempre se contrata aparte y se nombra en las exclusiones.
- **Anticipo** como porcentaje del total, contra orden de inicio.
- **Hitos de facturacion** con importe por hito. Los importes cierran exactamente contra el total; el redondeo lo absorbe el ultimo hito.
- **Precio por sede** cuando el cliente opera varias: total entre numero de sedes, dejando claro que incluye todas.
- **Lo que se factura aparte**, nombrado: la iguala contable mensual no se mezcla con la implementacion.
- **Ampliaciones**: tarifa por sede adicional o por alcance adicional, para que la conversacion futura ya tenga precio.

Todo importe sale de un solo origen numerico y se comprueba ejecutando el calculo, nunca razonandolo.

## Cierre de la propuesta

Toda propuesta termina declarando que el alcance es negociable en las dos direcciones y ofreciendo una sesion de revision antes de la firma. No es una concesion: es lo que convierte un documento cerrado en una conversacion, y lo que evita que el cliente descarte la propuesta en silencio por un renglon que no entendio.

El parrafo dice tres cosas y ninguna mas: que el alcance puede ampliarse o reducirse segun lo que el negocio necesite, que hay una sesion disponible para revisar los puntos que quieran ajustar, y que de esa sesion sale la version definitiva que se firma.

Registro directivo, sin adulacion. No se ruega la firma, no se agradece de antemano, no se usan formulas como "sera un placer" ni "quedamos a sus ordenes para lo que guste". Se enuncia el siguiente paso y se cierra.

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
- **Tarifas vigentes 2026**: lista 1,500 MXN por hora, preferencial 1,300 MXN por hora. La vigencia de la preferencial corre al 30 de septiembre para todos los clientes.
- **Dos modalidades de pago, siempre las dos**: A, anticipo del 30% contra firma y saldo contra aceptacion de cada hito; B, pagos mensuales iguales sin anticipo. Un cuadro por modalidad.
- **Horas efectivas de consultoria, no dias naturales.** El plazo va en su propio apartado y no se deriva de las horas.
- **Configuracion contable e iguala son cosas distintas.** La configuracion contable del sistema entra en la propuesta: se cobra cuando es el peso del proyecto, o se declara incluida sin costo cuando se usa como beneficio comercial. El servicio contable recurrente siempre se contrata aparte y se nombra en las exclusiones.
- **Anticipo** como porcentaje del total, contra orden de inicio.
- **Hitos de facturacion** con importe por hito. Los importes cierran exactamente contra el total; el redondeo lo absorbe el ultimo hito.
- **Precio por sede** cuando el cliente opera varias: total entre numero de sedes, dejando claro que incluye todas.
- **Lo que se factura aparte**, nombrado: la iguala contable mensual no se mezcla con la implementacion.
- **Ampliaciones**: tarifa por sede adicional o por alcance adicional, para que la conversacion futura ya tenga precio.

Todo importe sale de un solo origen numerico y se comprueba ejecutando el calculo, nunca razonandolo.

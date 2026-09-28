# Fases 5 y 6 — Horas, calibración y condiciones económicas

## Las horas van al final

Primero la ruta cerrada y aprobada. Después las horas. Estimar mientras se define el alcance produce números que defienden la ruta en lugar de medirla.

## Calibración contra horas reales

Las horas no se estiman por intuición. Se comparan contra el registro de horas reales de proyectos MLR ya ejecutados. Referencias útiles del registro Taiga (horas reales, no estimadas):

| Trabajo | Horas reales |
|---|---|
| Categorías de producto | 8 |
| Catálogo de productos | 33.5 |
| Listas de materiales | 34.5 |
| Contactos | 3 |
| Unidades de medida | 6 |
| Levantamiento físico de inventario | 6 |
| Rutas multietapa | 25.5 |
| Costes en destino | 2 |
| Carga de existencias iniciales | 34 |
| Aprobación por monto mínimo | 1 |
| Tarifas de proveedor | 3 |
| Equipos de venta | 2 |
| Listas de precio | 8.5 |
| Configuración de fabricación (bloque completo) | 39 |

Lecturas que hay que retener de ese registro: los datos maestros y la carga inicial pesan mucho mas de lo que parece, y las tareas de configuración puntual pesan mucho menos. Quien estima al revés se equivoca en las dos direcciones a la vez.

Proyecto de referencia completo: 206 horas reales sobre 42 tareas.

Cotizaciones cerradas que sirven de calibración:

| Proyecto | Situación de partida | Horas | Tareas | Aplicaciones |
|---|---|---|---|---|
| Taiga | ejecutado, horas reales | 206 | 42 | — |
| Aire Libre LATAM | implantación nueva, 3 empresas, catálogo menor a 500 productos | 250 | 40 | 8 |
| Dunedin | base viva en producción, 1 empresa, 5 almacenes, 29 rutas de venta | 264 | 50 | 10 |
| Ah Cacao | base viva, 8 companias a consolidar en una, 8 almacenes, 12 cajas, 1,373 productos, fabricación activa; preferencial 1,200 | 215 | 48 | 11 |

## Base viva contra implantación nueva

Es el ajuste que mas se equivoca. Cuando el cliente ya opera sobre Odoo, los datos maestros **ya existen**: productos cargados, categorías con su valuación, contactos con su RFC, almacenes construidos. Cotizar eso como si hubiera que crearlo infla la ruta entre un tercio y la mitad, y se cae en cuanto el cliente abre su propia base.

En una base viva se cotiza:

- **Depuración** de lo que esta incompleto: productos sin código o sin costo, contactos sin dato fiscal, existencias negativas, documentos en rezago.
- **Reconstrucción** de lo que está mal resuelto: automatizaciones que suplen configuración, catálogos de cuentas usados como dimensión, listas de precio de precio fijo replicadas por cliente.
- **Retiro** de lo que sobra, que casi siempre cuesta mas que construir de cero porque hay que sostener la operación mientras se quita.

Y no se cotiza lo que ya funciona. Antes de escribir una hora de una aplicación hay que abrir la base y ver si esa aplicación ya está resuelta. Si lo esta, se dice en la propuesta que queda fuera porque opera correctamente: es argumento de venta, no renuncia.

## Reglas de asignación

- Ninguna tarea baja de 0.5 h ni sube de 16 h. Lo que pasa de 16 h está mal partido.
- Una tarea que dura minutos no lleva horas propias: se absorbe.
- La replica por sede se cotiza como replica, con una hora unitaria menor que la primera configuración.
- La capacitación se cotiza por sesión agrupada por tema y rol, con su preparación incluida.
- El desarrollo lleva análisis, construcción, prueba y documentación dentro de la misma cifra.

## Techo de horas impuesto

Cuando Marcos o el cliente fijan un techo por debajo de la estimación:

1. Se dice con claridad que el techo exige recortar alcance, y se sostiene con la evidencia del registro real.
2. Se presenta la lista de lo que sale, no una versión adelgazada de todo.
3. Se marca lo que **no** puede salir: procesos críticos como la carga inicial de inventario no se le trasladan al cliente para cuadrar un número.
4. Decide Marcos. Una vez decidido, se ejecuta sin reabrir el debate.

Recortar minutos a cada renglón para llegar al número es falsificar la ruta.

## Contingencia

Se calcula y se distribuye por tarea en un archivo de uso interno de MLR. **Nunca aparece en un entregable del cliente**: ni como renglón, ni sumada a las horas publicadas, ni mencionada en el texto.

## Condiciones económicas

- **Tarifa de lista** y **tarifa preferencial** con fecha límite explicita. Se muestra el beneficio en importe.
- **Una sola tarifa para todo el trabajo, incluido el desarrollo.** Dirección lo fijo el 23 de septiembre de 2026: no se diferencia la tarifa por tipo de trabajo ni se presenta un cuadro de rangos. Tarifa de lista **1,500 MXN por hora** y preferencial **1,300 MXN por hora**, iguales para configuración, datos, definición contable, capacitación, acompañamiento y desarrollo. Dirección puede autorizar una preferencial menor para un proyecto concreto —Ah Cacao quedo en 1,200—; la de lista no se mueve. La preferencial lleva fecha límite explicita en cada ronda.
- **Nunca se compara el precio con el paquete de implementación de Odoo en un entregable del cliente.** Odoo publica su precio por hora en pesos y es menor; meter la comparación en la propuesta invita a discutir tarifa en lugar de alcance.
- **Tres esquemas de pago, siempre los tres**, con un cuadro que los pone lado a lado:
  - **A, por hitos:** anticipo del 30% a la firma y el 70% de cada hito facturado al iniciarlo.
  - **B, mensual:** pagos mensuales iguales, sin anticipo, facturados al inicio de cada mes.
  - **C, pago único:** un solo pago a la firma con 5% de descuento por pronto pago, aprobado por dirección como esquema permanente. El descuento se calcula sobre el importe preferencial de cada opción de alcance, es el 5% redondeado al centavo, mitad hacia arriba, y el pago es la diferencia. La propuesta dice el descuento en pesos y la tarifa efectiva por hora que resulta (1,300 x 0.95 = 1,235 con la preferencial general). El descuento rige solo dentro de la vigencia de la preferencial. El total de C queda siempre por debajo del de A y B; si no, el cálculo está mal.
- **Pago anticipado, nunca vencido.** Toda factura se paga antes de ejecutar el mes o el hito que ampara, y MLR no inicia el trabajo de un periodo cuya factura no este cubierta. La clausula va escrita en las condiciones de la propuesta económica; dirección la pidió expresamente porque las propuestas anteriores no la decían.
- **Opciones de alcance y esquemas de pago no se mezclan.** Las opciones son lo que el cliente contrata —base, ampliado, con o sin desarrollo—; los esquemas son como lo paga. Cuando hay mas de una opción, cada cuadro de esquemas lleva una columna por opción, lado a lado, y ningún renglón combina las dos cosas. Sin colores distintos por opción: saturan el documento.
- **Horas efectivas de consultoría, no días naturales.** El plazo va en su propio apartado y no se deriva de las horas.
- **Configuración contable e iguala son cosas distintas.** La configuración contable del sistema entra en la propuesta: se cobra cuando es el peso del proyecto, o se declara incluida sin costo cuando se usa como beneficio comercial. El servicio contable recurrente siempre se contrata aparte y se nombra en las exclusiones.
- **Anticipo** como porcentaje del total, contra orden de inicio.
- **Hitos de facturación** con importe por hito. Los importes cierran exactamente contra el total; el redondeo lo absorbe el último hito.
- **Precio por sede** cuando el cliente opera varias: total entre número de sedes, dejando claro que incluye todas.
- **Lo que se factura aparte**, nombrado: la iguala contable mensual no se mezcla con la implementación.
- **Ampliaciones**: tarifa por sede adicional o por alcance adicional, para que la conversación futura ya tenga precio.

Todo importe sale de un solo origen numérico y se comprueba ejecutando el cálculo, nunca razonandolo.

## Cierre de la propuesta

Toda propuesta termina declarando que el alcance es negociable en las dos direcciones y ofreciendo una sesión de revisión antes de la firma. No es una concesión: es lo que convierte un documento cerrado en una conversación, y lo que evita que el cliente descarte la propuesta en silencio por un renglón que no entendió.

El párrafo dice tres cosas y ninguna mas: que el alcance puede ampliarse o reducirse según lo que el negocio necesite, que hay una sesión disponible para revisar los puntos que quieran ajustar, y que de esa sesión sale la versión definitiva que se firma.

Registro directivo, sin adulación. No se ruega la firma, no se agradece de antemano, no se usan fórmulas como "sera un placer" ni "quedamos a sus ordenes para lo que guste". Se enuncia el siguiente paso y se cierra.

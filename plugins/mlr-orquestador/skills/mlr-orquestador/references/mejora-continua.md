# Mejora continua del estandar MLR

El estandar debe volverse mas preciso con el uso. Sin este ciclo, los mismos errores se repiten en cada sesion.

## Dos niveles

**Nivel 1, memoria en la nube.** Inmediato, sin reinstalar nada, disponible en la siguiente sesion desde cualquier dispositivo. Aqui van las correcciones en cuanto ocurren. Protocolo en la skill `mlr-memoria`.

**Nivel 2, skills del plugin.** Consolidacion trimestral de lo que demostro ser estable. Requiere reempaquetar y subir version.

Toda correccion entra por el nivel 1. Solo asciende al nivel 2 lo que se repitio y no cambio.

## Que dispara un registro

- Alguien corrige el estilo, el tono o la estructura de un entregable.
- Un cliente devuelve una observacion sobre forma o claridad.
- Se toma una decision de criterio que va a repetirse.
- Se descarta una herramienta o un enfoque por una razon concreta.
- Un entregable se rehace. La causa de que se rehiciera es la regla que faltaba.

## Como se registra

En el mismo turno en que ocurre, no al final del trabajo. Formato de directriz en `mlr-memoria`, con campo de origen obligatorio.

Despues, una linea a la persona: "Esto lo dejo fijo en el estandar para que no vuelvas a pedirlo."

## Revision trimestral

1. Listar las directrices acumuladas en el espacio de firma.
2. Contrastarlas con los entregables reales del periodo: cuales se cumplieron, cuales se incumplieron, cuales estorbaron.
3. Consolidar en las skills las que resultaron estables.
4. Eliminar las obsoletas y fusionar las duplicadas.
5. Subir version del plugin y reempaquetar.

Una memoria contradictoria produce comportamiento erratico. La limpieza no es opcional.

## Que no se consolida

- Preferencias de una sola vez atadas a un entregable concreto.
- Directrices especificas de un cliente. Esas se quedan en el espacio de ese cliente.
- Reglas que relajarian la verificacion, la confidencialidad o la honestidad. Esas no se aplican en ningun nivel.

# Mejora continua del estándar MLR

El estándar debe volverse mas preciso con el uso. Sin este ciclo, los mismos errores se repiten en cada sesión.

## Dos niveles

**Nivel 1, memoria en la nube.** Inmediato, sin reinstalar nada, disponible en la siguiente sesión desde cualquier dispositivo. Aquí van las correcciones en cuanto ocurren. Protocolo en la skill `mlr-memoria`.

**Nivel 2, skills del plugin.** Consolidación trimestral de lo que demostró ser estable. Requiere reempaquetar y subir versión.

Toda corrección entra por el nivel 1. Solo asciende al nivel 2 lo que se repitió y no cambio.

## Que dispara un registro

- Alguien corrige el estilo, el tono o la estructura de un entregable.
- Un cliente devuelve una observación sobre forma o claridad.
- Se toma una decisión de criterio que va a repetirse.
- Se descarta una herramienta o un enfoque por una razón concreta.
- Un entregable se rehace. La causa de que se rehiciera es la regla que faltaba.

## Como se registra

En el mismo turno en que ocurre, no al final del trabajo. Formato de directriz en `mlr-memoria`, con campo de origen obligatorio.

Después, una línea a la persona: "Esto lo dejo fijo en el estándar para que no vuelvas a pedirlo."

## Revisión trimestral

1. Listar las directrices acumuladas en el espacio de firma.
2. Contrastarlas con los entregables reales del periodo: cuales se cumplieron, cuales se incumplieron, cuales estorbaron.
3. Consolidar en las skills las que resultaron estables.
4. Eliminar las obsoletas y fusionar las duplicadas.
5. Subir versión del plugin y reempaquetar.

Una memoria contradictoria produce comportamiento errático. La limpieza no es opcional.

## Que no se consolida

- Preferencias de una sola vez atadas a un entregable concreto.
- Directrices especificas de un cliente. Esas se quedan en el espacio de ese cliente.
- Reglas que relajarían la verificación, la confidencialidad o la honestidad. Esas no se aplican en ningún nivel.

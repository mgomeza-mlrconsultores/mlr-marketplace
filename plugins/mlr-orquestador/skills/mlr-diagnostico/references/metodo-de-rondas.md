# Método de rondas

## Archivos de trabajo (área interna del cliente)

- `CONTEXTO_AGENTE.md` — brief común para todos los agentes. Solo hechos de conexión y de versión, **ninguna conclusión**: cliente y giro, base y versión, la regla de solo lectura, como usar el helper, donde esta el código fuente de la versión, línea de tiempo de migraciones y la regla de evidencia.
- `CATALOGO_vN.md` — afirmaciones numeradas por bloque. Una afirmación por línea, con cifra, folio de ejemplo y etiqueta `[origen NN]` / `[vigente]`. Bloques sugeridos: M (migración y transición), I (inventario y valuación), C (contabilidad y fiscal), S (seguridad y código). Se crea una versión nueva en cada ronda con cambios; la anterior no se edita.
- `RONDAS.md` — una línea por ronda: agentes que corrieron, cambios materiales con su código de afirmación, y si la ronda cuenta como limpia.
- `rN_ciego.md`, `rN_verif_<bloque>.md` — salida de cada agente, tal cual.

## Composición de una ronda

1. **Agente ciego.** Recibe solo `CONTEXTO_AGENTE.md`. Diagnostica la base completa en su propia fase 1. Después, en una fase 2, lee el catálogo y reporta: hallazgos suyos no cubiertos, contradicciones con evidencia, y autocorrecciones que hizo al leerlo (comprobadas en vivo).
2. **Un verificador por bloque.** Recibe el contexto y el bloque del catálogo. Por cada afirmación: CONFIRMADA / REFUTADA / CIFRA DISTINTA, la cifra propia, el método propio (modelo + filtro, distinto del obvio cuando sea posible) y si la diferencia es material. Encabezado obligatorio: `DIFERENCIAS MATERIALES: n`.
3. **Orquestador.** Lee las salidas, re-consulta cada contradicción y cada hallazgo nuevo, decide, escribe el catálogo nuevo y la línea de bitácora.

Los agentes corren en paralelo. Para cargas pesadas conviene que descarguen una vez los modelos grandes a cache local y trabajen sobre ella.

## Instrucción base para el agente ciego

> Eres auditor independiente de una base Odoo. Lee `CONTEXTO_AGENTE.md` y nada mas de la carpeta. Solo lectura con el helper. Diagnostica inventario, valuación, contabilidad, fiscal, seguridad y código a medida. Cada hallazgo con cifra exacta re-derivada por dos caminos, el método y al menos un documento con folio; marca demostrado o inferencia y si es herencia de la versión anterior o riesgo vigente. Al terminar la fase 1 escribe tu salida; después lee `CATALOGO_vN.md` y agrega: hallazgos materiales no cubiertos, contradicciones con evidencia y autocorrecciones comprobadas.

## Instrucción base para el verificador

> Eres auditor escéptico. Tu trabajo es tumbar el catálogo, no confirmarlo. Para cada afirmación del bloque <X> re-deriva la cifra con un método propio, busca contraejemplos y lee el código de la versión cuando la afirmación hable de mecánica. Reporta CONFIRMADA / REFUTADA / CIFRA DISTINTA, con cifra, método y si la diferencia es material. Empieza con `DIFERENCIAS MATERIALES: n`.

## Relevante contra menor

- Relevante (material): hallazgo nuevo con impacto económico, fiscal u operativo; afirmación refutada; cifra que cambia mas allá del redondeo o de un método equivalente ya explicado; causa distinta; algo que cambia lo que se le dice al cliente o lo que tiene que hacer.
- Menor (estético): matiz de redacción, redondeo, método alterno que llega a la misma cifra, desglose o ejemplo adicional que no cambia la conclusión ni la cifra del informe.
- Ante la duda, se clasifica como relevante.

## Cuantas rondas y cuando se para

- **Mínimo 4 rondas.** No se cierra antes de terminar la cuarta, aunque todas salgan limpias.
- **Cierre por estabilidad:** desde la cuarta, se para cuando dos rondas consecutivas terminan sin errores o solo con hallazgos menores en todos los bloques. Un hallazgo relevante en cualquier bloque reinicia la cuenta.
- **Máximo 10 rondas.** Al terminar la décima se cierra aunque siga habiendo hallazgos relevantes. La bitácora y el informe interno dicen que bloques seguían moviéndose y que se corrigió en las dos últimas rondas; lo no estabilizado no entra al informe del cliente como hecho cerrado.
- Un bloque puede quedar estable antes que otro; se anota, pero el cierre es global.
- Si Marcos corta antes, la bitácora lo dice con la misma constancia.
- Cada línea de `RONDAS.md` termina con el estado de la cuenta: «relevantes: n · menores: n · rondas estables seguidas: n».

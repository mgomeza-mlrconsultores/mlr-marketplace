# Metodo de rondas

## Archivos de trabajo (area interna del cliente)

- `CONTEXTO_AGENTE.md` — brief comun para todos los agentes. Solo hechos de conexion y de version, **ninguna conclusion**: cliente y giro, base y version, la regla de solo lectura, como usar el helper, donde esta el codigo fuente de la version, linea de tiempo de migraciones y la regla de evidencia.
- `CATALOGO_vN.md` — afirmaciones numeradas por bloque. Una afirmacion por linea, con cifra, folio de ejemplo y etiqueta `[origen NN]` / `[vigente]`. Bloques sugeridos: M (migracion y transicion), I (inventario y valuacion), C (contabilidad y fiscal), S (seguridad y codigo). Se crea una version nueva en cada ronda con cambios; la anterior no se edita.
- `RONDAS.md` — una linea por ronda: agentes que corrieron, cambios materiales con su codigo de afirmacion, y si la ronda cuenta como limpia.
- `rN_ciego.md`, `rN_verif_<bloque>.md` — salida de cada agente, tal cual.

## Composicion de una ronda

1. **Agente ciego.** Recibe solo `CONTEXTO_AGENTE.md`. Diagnostica la base completa en su propia fase 1. Despues, en una fase 2, lee el catalogo y reporta: hallazgos suyos no cubiertos, contradicciones con evidencia, y autocorrecciones que hizo al leerlo (comprobadas en vivo).
2. **Un verificador por bloque.** Recibe el contexto y el bloque del catalogo. Por cada afirmacion: CONFIRMADA / REFUTADA / CIFRA DISTINTA, la cifra propia, el metodo propio (modelo + filtro, distinto del obvio cuando sea posible) y si la diferencia es material. Encabezado obligatorio: `DIFERENCIAS MATERIALES: n`.
3. **Orquestador.** Lee las salidas, re-consulta cada contradiccion y cada hallazgo nuevo, decide, escribe el catalogo nuevo y la linea de bitacora.

Los agentes corren en paralelo. Para cargas pesadas conviene que descarguen una vez los modelos grandes a cache local y trabajen sobre ella.

## Instruccion base para el agente ciego

> Eres auditor independiente de una base Odoo. Lee `CONTEXTO_AGENTE.md` y nada mas de la carpeta. Solo lectura con el helper. Diagnostica inventario, valuacion, contabilidad, fiscal, seguridad y codigo a medida. Cada hallazgo con cifra exacta re-derivada por dos caminos, el metodo y al menos un documento con folio; marca demostrado o inferencia y si es herencia de la version anterior o riesgo vigente. Al terminar la fase 1 escribe tu salida; despues lee `CATALOGO_vN.md` y agrega: hallazgos materiales no cubiertos, contradicciones con evidencia y autocorrecciones comprobadas.

## Instruccion base para el verificador

> Eres auditor esceptico. Tu trabajo es tumbar el catalogo, no confirmarlo. Para cada afirmacion del bloque <X> re-deriva la cifra con un metodo propio, busca contraejemplos y lee el codigo de la version cuando la afirmacion hable de mecanica. Reporta CONFIRMADA / REFUTADA / CIFRA DISTINTA, con cifra, metodo y si la diferencia es material. Empieza con `DIFERENCIAS MATERIALES: n`.

## Que es material

- Material: hallazgo nuevo con impacto economico, fiscal u operativo; afirmacion refutada; cifra que cambia mas alla del redondeo o de un metodo equivalente ya explicado; causa distinta.
- No material: matiz de redaccion, metodo alterno que llega a la misma cifra, desglose adicional que no cambia la conclusion.

## Cierre

- Dos rondas consecutivas con cero cambios materiales en todos los bloques.
- Un bloque puede quedar estable antes que otro; se anota, pero el cierre es global.
- Si Marcos corta antes, la bitacora lo dice y el informe interno lista los bloques que seguian moviendose.

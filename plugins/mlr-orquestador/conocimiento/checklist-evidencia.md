# Qué cuenta como evidencia

1. Cifra re-derivada por dos caminos distintos que coinciden (por ejemplo, desde movimientos de inventario y desde apuntes contables).
2. Al menos un documento concreto con folio que se puede abrir en pantalla.
3. Mecanismo explicado con el código de la versión exacta (archivo y método citados en la bitácora interna).
4. Contraejemplo buscado y no encontrado, o encontrado y explicado.
5. En lo fiscal, el comprobante leído (XML o PDF adjunto), no el campo de estado.
6. Separación explícita entre demostrado e inferencia; la inferencia no entra al informe del cliente.
7. Captura real de la pantalla con pie numerado que dice qué se ve y la cifra exacta.
8. Etiqueta de origen: `[origen NN]` si lo generó una versión anterior, `[vigente]` si sigue operando mal.

## Trampas de medición
`amount_total` en moneda del documento (usar el firmado o débitos y créditos); `create_date` vacío en filas insertadas por SQL en migraciones; unidades con factor 1; cuentas archivadas en uso; consultas pesadas por lotes y con caché local.

## Registro
Catálogo versionado (`CATALOGO_vN.md`) con una afirmación por línea, cifra, folio de ejemplo y etiqueta; bitácora de rondas (`RONDAS.md`) con relevantes, menores y rondas estables seguidas; salidas de agentes tal cual.

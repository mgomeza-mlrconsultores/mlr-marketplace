# Auditoría de la lógica de origen y decisiones de diseño

Qué se encontró al revisar el documento de contexto, las dos plantillas y el libro de agosto del caso de origen, y qué se cambió en la skill. Sirve para quien mantenga la skill y para que dirección sepa en qué se aparta del caso original.

## Hallazgos en la lógica y en las plantillas

1. **Plantilla del tamaño de un solo mes.** La plantilla vacía tenía exactamente 107 renglones de conciliación, 87 de facturas y 80 de IVA, los de agosto. En otro mes, las fórmulas vacías de Facturas vs Odoo contaban como «No identificado» y el Resumen reportaba facturas pendientes inexistentes; con más movimientos, los sobrantes quedaban fuera de todos los SUMIF. Se resolvió con el redimensionado automático de `llenar_libro.py`.
2. **Código de diario escrito en la fórmula.** El estatus de Impuestos vs Odoo y un renglón del bloque de diferencias buscaban «CSH1», el código del diario de caja de una sola empresa. Ahora se lee de la Observación, que el script escribe con los diarios de caja reales.
3. **El Previo salía aunque la conciliación no estuviera completa.** En agosto el libro calculó 62,428 pesos de IVA cobrado contra 67,769 del analista y de Odoo. La diferencia coincide al centavo con el IVA de 38,726 pesos de excedente de tres depósitos de terminal. Se agregó «¿Se puede enviar el Previo?», el aviso en la hoja Previo, y la regla de lote de terminal (E08).
4. **Depósitos de terminal por lote.** La terminal deposita en bruto las ventas del día de varios clientes; la regla de varios CFDI solo buscaba facturas del mismo contacto. E08 busca combinaciones de facturas pagadas con tarjeta en la tolerancia de días.
5. **Dos catálogos con la misma numeración.** El documento numeraba R01 a R11 las reglas del motor y la plantilla de control R01 a R14 las de corrección, con significados distintos. El motor pasó a E01 a E11.
6. **Etiquetas perdidas.** Al vaciar la plantilla se borraron los textos del bloque «¿De dónde salen las diferencias de IVA?»; se reponen al llenar.
7. **Unidades mezcladas en el Resumen.** La pregunta 4 mostraba conteos y un importe con la misma apariencia («Pagos a COMISIONES sin CFDI» sumaba pesos). Se aclaró la etiqueta.
8. **Dos libros por diario.** El análisis y la aprobación vivían en libros distintos, y un cambio en uno no se veía en el otro. Las hojas Acciones, Verificación y Bitácora se integraron al libro de conciliación.
9. **La llave de API en el chat.** El documento de origen pedía la llave en cada sesión. La skill la toma de variables de entorno o de un archivo 600, como el resto de las skills de la firma, y si se pega en el chat se recomienda revocarla.
10. **Producción.** El documento decía que las reglas valen igual en producción y en pruebas, pero la conciliación de un cliente se hace sobre su base productiva y las reglas de la firma solo permiten escribir en pruebas. **DECIDE Marcos (29-sep-2026):** la conciliación se trabaja en producción; la skill propone en el libro y aplica lo aprobado, hasta el final. Se conservan la declaración del entorno, la prueba de una fila por tipo antes del lote y la pregunta diaria por el respaldo de la base.
11. **XML-RPC y None.** La lección de «reintentar a ciegas duplica» se atacó de raíz: el cliente usa JSON-RPC y, además, verifica por lectura.
12. **Fecha de pago en parcialidades.** Mi Admin guarda una sola «fecha real de pago» por factura; comparar cada parcialidad contra esa fecha marcaba falsos «revisar». Solo se compara en enlaces 1 a 1 y REP.

## Mejoras agregadas

- Alertas nuevas: PPD sin complemento de pago, CFDI cancelado, PUE con forma de pago 99, posible pago duplicado, pago en efectivo mayor a 2,000 pesos en diarios de caja y RFC en la lista 69-B.
- Facturas de Odoo del mes sin CFDI en las exportaciones, además de los CFDI sin registro en Odoo.
- Revisión de configuración al extraer: diario de base de efectivo, fechas de bloqueo, moneda del diario contra la de su cuenta.
- Seguimiento de conciliaciones de dos saltos (banco, cuenta puente, pago, factura) para reconocer pagos conciliados desde la línea del estado de cuenta que no existen como `account.payment`.
- `decisiones.json` para que los empates resueltos y las explicaciones aceptadas sobrevivan a las corridas sucesivas.
- Revalidación antes de escribir, prueba de una fila por tipo y lote solo tras validar, todo en código y no solo en instrucciones.
- Lector de estado de cuenta por posición de columna con perfiles por banco, entrada por Excel o CSV y control de saldo corrido además del de carátula.
- Pruebas automáticas contra el caso de agosto anonimizado.

## Revisión independiente antes de publicar

Un agente ciego siguió la skill sobre el ejemplo y buscó fallas. Lo que encontró y se corrigió:

- Una aprobación sobrevivía aunque la nueva corrida propusiera otra operación para la misma partida, y la operación completada en el chat se perdía en la corrida siguiente. Ahora la aprobación exige la misma operación y la operación completada se conserva.
- La prueba de una fila por tipo solo valía dentro de una corrida, y un primer intento fallido no contaba. Ahora el tipo queda «en prueba» entre corridas, falle o no, hasta `--validar-tipo`.
- Un `params.json` sin entorno se trataba como pruebas. Ahora no se escribe sin entorno, y en producción se exige la fecha del respaldo del día.
- El respaldo de `linea_extracto` no bastaba para reponer la línea de suspenso, y no revisaba la fecha de bloqueo.
- El control de creados sin aprobación decía 0 sin bitácora y comparaba hora local contra la hora UTC de Odoo. Ahora parte de `sesion.json` en UTC y queda pendiente si no hay inicio registrado.
- Los lotes de terminal del mismo día quedaban fuera, y E08 no corría cuando Odoo ya ligaba una factura al depósito.
- En diarios en moneda extranjera se mezclaban dólares y pesos; el saldo restante no descontaba pagos de meses anteriores; los diarios de caja se reconocían por nombre y no por código; el encabezado «Tipo Cambio» del acumulado se podía tomar como «Tipo».
- Traspasos entre cuentas propias y movimientos con socios no tenían salida y bloqueaban el cierre; tampoco las filas aprobadas que no llevan escritura. Se agregaron E12, `cuentas_sin_cfdi`, `acciones.py no-requiere` y el estado «Resuelto».
- El modo con estado de cuenta no proponía nada para las líneas en suspenso. Ahora las marca con alerta y propone `linea_extracto`.
- Una corrida fallida podía perder el libro anterior: ahora se copia a `versiones/` y el nuevo solo reemplaza al anterior al terminar bien.
- Diferencias entre la documentación y el código (numeración de reglas en Acciones, argumentos de `leer_cfdi.py`, tolerancias del libro contra las del motor) y una prueba que siempre pasaba.

## Lo que no se pudo probar en esta versión

- La lectura de un PDF real de BBVA: se probó con un PDF sintético del mismo acomodo. El control de carátula protege la primera lectura real.
- Las escrituras contra un Odoo real: se probaron la revalidación contra una base de pruebas en solo lectura y la ruta completa de escritura contra un Odoo simulado. La primera aplicación de cada tipo en la base de un cliente es la prueba real, y por eso va sola y con captura.
- El acumulado real de Mi Admin: se reconocen sus columnas por nombre con alias; los avisos de columnas no encontradas dicen qué ajustar.

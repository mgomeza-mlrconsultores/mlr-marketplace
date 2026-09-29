# El libro de conciliación

Un libro por diario y periodo: `Conciliacion_<Mes>_<Año>_<Empresa>_<Diario>.xlsx`. Formato MLR: encabezado C1 «MLR CONSULTORES», C2 título, C3 «<Empresa> · <Mes Año>», A5 una línea que explica la hoja; teal #24606C con texto blanco en encabezados, azul claro #E6F3FB en las únicas celdas que se capturan, café #452E27 como acento. Todo lo demás es fórmula y el libro se entrega con cero errores al recalcular.

## Hojas

1. **Guía**: cuatro pasos de uso, qué hay en cada hoja, leyenda de colores por tipo de retención y fuentes.
2. **Resumen, «¿Cuadró el mes?»**: seis preguntas con fórmula (PDF bien leído; cómo quedó cada movimiento; dinero por estatus y cuadre del flujo; alertas fiscales; cuánto se paga; si Odoo dice lo mismo que el SAT y el banco) y, agregada por la skill, **«¿Se puede enviar el Previo al cliente?»** en C34:C35.
3. **Acciones** (agregada): propuestas con su regla R01 a R14, confianza y operación en JSON; la persona llena Aprobado (Sí, No, Modificar) y Comentario, o la skill los registra con `acciones.py` cuando la persona decide en el chat; la skill llena Estado (Pendiente, Aplicado, Resuelto, Error, Revalidar), IDs resultado y Verificado. «Resuelto» es para las filas que no llevan escritura en Odoo.
4. **Verificación** (agregada): controles de cierre; los que dicen «lo escribe la skill» los llena `verificar.py` leyendo Odoo. Estado CERRADO o ABIERTO.
5. **Bitácora** (agregada): una fila por escritura, desde `bitacora.jsonl`, con su respaldo.
6. **Conciliación**: columnas A a AL. BANCO (A-E), ODOO (F-M), CFDI (N-AC), RESULTADO (AD-AL). Estatus con formato condicional; renglones de continuación en gris en la parte del banco; color por tipo de retención en los conciliados; renglón de totales al final.
7. **Facturas vs Odoo**: cada CFDI del mes, emitido o recibido, contra Odoo (emitidas por serie y folio, recibidas por folio fiscal) y, agregado por la skill, las facturas de Odoo del mes que no aparecen en las exportaciones.
8. **Impuestos vs Odoo**: saldos de las cuentas de IVA en flujo contra la conciliación, detalle por factura y el bloque «¿De dónde salen las diferencias de IVA?».
9. **Desglose fiscal**: IVA y retenciones por tipo de retención, cobros y pagos, y el cuadre del flujo contra el banco (amparado con CFDI, no requiere CFDI, sin CFDI, excedente en revisión, total explicado contra estado de cuenta).
10. **Previo**: cálculo preliminar para el cliente, con el redondeo del art. 20 CFF (`ROUNDDOWN(x+0.49,0)`), el aviso «PRELIMINAR INCOMPLETO» en C8 y, solo mientras se prueba con un cliente nuevo, el comparativo contra el previo manual.
11. **Estado de cuenta**: movimientos con saldo corrido, carátula a la derecha y control en K23:M28.
12. **Auxiliar Odoo**: el auxiliar tal como se leyó, con saldo inicial (J12), final y diferencia contra el banco.
13. **Reglas**: tolerancias (C7 importe, C8 días), definición de estatus, tabla de retenciones y palabras clave.

## Celdas que captura la persona

Previo E12 (ISR de la nómina del mes), E19 a E21 (pago provisional, pagos anteriores, recargos), E27 (saldo a favor que se aplica); Reglas C32 a C35 (palabras clave); Acciones columnas Aprobado y Comentario. `llenar_libro.py --anterior` las conserva de una corrida a otra; la aprobación, solo si la operación aprobada no cambió. Las tolerancias (Reglas C7 y C8) se llenan desde `params.json` en cada corrida, para que el libro y el motor usen las mismas.

## Tamaño de las tablas

La plantilla está dibujada para 107 movimientos, 87 facturas y 80 renglones de IVA, que es exactamente el mes de agosto del caso de origen. Con menos renglones, las fórmulas vacías de Facturas vs Odoo cuentan como «No identificado» y el Resumen dice que hay facturas por atender que no existen; con más, los movimientos quedan fuera de todos los SUMIF. `llenar_libro.py` redimensiona cada tabla al número real de renglones y reescribe todas las referencias que apuntan a ella en cualquier hoja: rangos, celdas de último renglón (G y H del saldo corrido), formato condicional, filtros y los bloques que están debajo (totales de Conciliación, explicación de diferencias de IVA). Se probó con 20 y con 214 movimientos sin un solo error.

## Mejoras que `llenar_libro.py` aplica sobre la plantilla

Se aplican también sobre la plantilla original de la unidad, así que la plantilla no hay que editarla.

- El estatus de Impuestos vs Odoo reconocía los pagos por caja buscando el código de diario CSH1 escrito en la fórmula, que solo existe en una empresa. Ahora busca la frase «Pagada por caja» que el script escribe en la Observación con los diarios de caja reales de cada empresa.
- El bloque «¿De dónde salen las diferencias de IVA?» había perdido sus etiquetas en la plantilla vacía; se reponen.
- «¿Se puede enviar el Previo al cliente?» en el Resumen y el aviso en rojo del Previo: la pregunta 5 decía el total a pagar aunque hubiera partidas sin identificar y excedentes que cambian ese total.
- La pregunta 4 mezclaba conteos con un importe («Pagos a COMISIONES sin CFDI» sumaba pesos); la etiqueta dice ahora que es un importe.
- Textos que citaban a la empresa, al banco y al mes del caso de origen (fuentes, nota del primer ejercicio, comparativo del analista) se llenan con los parámetros del diario.
- Hojas Acciones, Verificación y Bitácora, que en el caso de origen vivían en un segundo libro (`MLR_Plantilla_Conciliacion_Bancaria_Odoo.xlsx`). Un solo libro por diario evita que la aprobación y el análisis se desincronicen.

## Recalcular

`llenar_libro.py` recalcula con LibreOffice cuando está instalado y falla si alguna fórmula da error; deja una copia recalculada `.calc.xlsx` que `verificar.py` lee. Excel recalcula al abrir. Nunca usar XLOOKUP, FILTER, SORT, UNIQUE ni SEQUENCE en el libro.

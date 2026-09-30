# -*- coding: utf-8 -*-
from comun import *

ENT = {
 "contabilidad": [
  "Levantamiento contable, fiscal y de cobranza, con el flujo objetivo de facturación, cobro, depósito, conciliación y cierre, y el documento de criterios firmado antes de configurar.",
  "Depuración de los permisos de administrador, activación del doble factor y usuario propio para las integraciones.",
  "Catálogo de cuentas definido con el contador, con la fusión de las 136 cuentas 191.01 marcadas para eliminar con su cuenta correcta, el tipo corregido en 101 cuentas y la naturaleza en 79, el código agrupador del SAT, y diarios, impuestos y cuentas predeterminadas apuntando al catálogo final, con la corrección del impuesto «16» que calcula 0 % y las cuentas de los IEPS de venta.",
  "Póliza de apertura al 1 de enero de 2026 con la balanza validada por el contador y los saldos abiertos por cliente, que sustituye los saldos heredados de la carga histórica.",
  "Cancelación de los 1,461 cobros que el proceso externo registró en caja sin respaldo bancario, depuración de los cobros de más en 115 facturas, de los 98 pagos sin asiento y de los saldos a favor de 23 clientes, y reaplicación de los pagos a sus facturas.",
  "Importación de los extractos bancarios de 2026, reglas de conciliación automática y conciliación bancaria del periodo.",
  "Regularización de los movimientos contables contra los CFDI emitidos y recibidos en el SAT, con el registro de las facturas de gastos faltantes, la emisión de los complementos de las 356 facturas PPD cobradas sin complemento, y la forma de pago y los datos fiscales de los contactos, entre ellos los 92 RFC repetidos.",
  "Capacitación en tres temas, cada uno con una sesión teórica y una práctica de una hora, grabadas y acompañadas de la guía de operación, bloqueo de periodos y revisión del primer cierre mensual con el acta de aceptación.",
 ],
 "inventario": [
  "Levantamiento de inventario, compras y ventas, con el flujo objetivo de compra, recepción, venta, entrega y ajuste, y el documento de criterios firmado antes de configurar.",
  "Método de costeo y cuentas contables de las categorías, hoy apuntando a cuentas 191.01, retiro de las categorías de prueba y depuración por plantilla de los 25 productos sin categoría, de los precios y costos atípicos y de los productos físicos dados de alta como no almacenables.",
  "Una sola familia de peso con el kilogramo nativo, con el paso de los 35 productos en Kg y la restitución de las unidades originales archivadas el 27 de diciembre de 2025.",
  "Restitución de la ubicación de existencias convertida en WH/SCRAP y de las dos reglas de abastecimiento que apuntan a ella, seguimiento por lote con fecha de caducidad y salida FEFO en los 422 productos perecederos que hoy se manejan por cantidad, y corrección de los costes en destino repetidos o registrados contra la cuenta de inventario.",
  "Regularización de existencias con hojas de conteo y el conteo físico de Freshbox, corrección de las 14 existencias negativas y de los productos archivados con existencia, y cierre de las recepciones y entregas pendientes.",
  "Regularización de los históricos de compras, con la revisión de las 765 órdenes de 2026 recibidas sin factura, por 16,540,856.88 pesos, de sus recepciones y de sus facturas, el registro de las facturas de adquisición de mercancías con la carga del XML y el cierre de las 1,200 órdenes históricas sin recepción ligada.",
  "Regularización de los históricos de ventas, con la revisión de pedidos, entregas y facturas, el reverso del costo duplicado de enero de 2026, de alrededor de 7 millones de pesos, el costo faltante en 298 facturas, el timbrado o la cancelación de las 63 facturas sin folio fiscal y de las 28 ventas con dos comprobantes vigentes, y el estado de facturación de los pedidos.",
  "Valoración del inventario con la revaluación de las entradas sin costo o con costo atípico, inventario de apertura de 2026 y cierre con el cruce por producto contra la cuenta 115.01.01.",
  "Capacitación en tres temas, cada uno con una sesión teórica y una práctica de una hora, grabadas y acompañadas de la guía de operación, y revisión del primer cierre mensual con el acta de aceptación.",
 ],
}

OBS = {
 "contabilidad": [
  "El catálogo tiene 325 cuentas, de las que 136 llevan código 191.01, agrupado por el SAT como otros activos a largo plazo, aunque son la caja, los bancos, las ventas, el costo de venta, el IVA y el capital. La operación sigue registrándose en ellas: la cuenta de ventas 191.01.80 acumula 54,560,618.54 pesos y las cuentas correctas, como 102.01.01 BBVA, no tienen movimiento.",
  "La caja registra 35,047,132.29 pesos sin un solo traspaso a bancos. De esos cobros, 4,527 por 25.6 millones son la carga del histórico de abril de 2026 y 1,461 por 9,669,743.89 pesos los generó un proceso que corre fuera de Odoo con el usuario personal de un administrador y cuyo código no está en la base.",
  "Hay 115 facturas con cobros de más, 23 clientes con saldo a favor por 1,258,664.54 pesos y 98 pagos sin asiento por 1,193,316.26 pesos. La base solo tiene 27 líneas de estado de cuenta frente a 1,988 asientos de banco.",
  "De 382 facturas PPD de 2026 pagadas, 356 no tienen complemento de pago, por alrededor de 5.6 millones de pesos; 63 facturas de 2026 están sin timbrar por 902,214.41 pesos y 45 tienen una cancelación pendiente ante el SAT por 957,401.86 pesos.",
 ],
 "inventario": [
  "La cuenta 115.01.01 Inventario tiene un saldo de −21,565,632.89 pesos contra 2,952,805.45 pesos de existencias valuadas por Odoo. La diferencia se explica sobre todo por las compras que no se facturan en Odoo, por el costo duplicado de enero y por los ajustes y costos en destino que no llegaron a la contabilidad.",
  "En toda la base hay solo 25 facturas de proveedor, y después del 20 de abril de 2026 no se ha registrado ninguna, por lo que Odoo resta inventario con cada venta sin sumarlo con cada compra y no conoce las cuentas por pagar ni el IVA acreditable.",
  "Entre el 6 y el 26 de enero de 2026 la línea de costo de las facturas volvió a multiplicar por la cantidad un costo que ya era total, como en INV/2026/00056, con 3,384,000 pesos de costo contra 129,000 de venta. Ese mes todo el costo, por 8,254,611.68 pesos, se registró en otros gastos generales.",
  "La ubicación de existencias se convirtió en WH/SCRAP y se archivó el 12 de febrero de 2026, después de que 608 renglones de entrega salieron desde ahí. Conviven las unidades kg, de 1,000 gramos, y Kg, sin relación con ninguna otra, con 132 y 35 productos respectivamente.",
  "Hay 7,554 pedidos de venta por facturar, de los que 4,574 ya tienen factura sin ligar; el riesgo de facturarlos de nuevo ya se materializó el 26 de agosto de 2026, con quince notas de crédito timbradas.",
 ],
}

PROY_TXT = {"contabilidad": "el saneamiento de la contabilidad, la cobranza y la conciliación",
            "inventario": "el saneamiento del inventario, de los documentos de compra y venta y de la valoración",
            "integral": "el saneamiento conjunto de la contabilidad y el inventario"}

d = doc(["Plan de trabajo", "y alcance detallado"])
d.parrafo("Por medio del presente, MLR Consultores desarrolla para Freshbox el plan de trabajo y el alcance detallado "
          "de %s de su base de Odoo 19. El documento forma parte de la propuesta económica de la misma fecha y se lee "
          "junto con ella, ya que los importes y los esquemas de pago constan en esa propuesta y no se repiten aquí."
          % PROY_TXT[KEY])

d.seccion("1. Alcance del servicio propuesto")
d.parrafo("El proyecto se construye sobre la funcionalidad nativa de Odoo y sobre la configuración que Freshbox ya "
          "tiene en su base, de la que solo se corrige o completa lo que falta, y comprende los siguientes "
          "entregables:")
if KEY != "integral":
    d.vinetas(ENT[KEY])
else:
    d.subtitulo("Contabilidad, cobranza y conciliación")
    d.vinetas(ENT["contabilidad"][1:-1])
    d.subtitulo("Inventario, compras, ventas y valoración")
    d.vinetas(ENT["inventario"][1:-1])
    d.subtitulo("Común a ambos proyectos")
    d.vinetas([
     "Levantamiento por área con un solo flujo objetivo de compra, recepción, venta, facturación, cobro, conciliación y cierre, y el documento de criterios firmado antes de configurar.",
     "Capacitación en seis temas, cada uno con una sesión teórica y una práctica de una hora, grabadas y acompañadas de la guía de operación, bloqueo de periodos y revisión del primer cierre mensual con el acta de aceptación.",
    ])

d.seccion("2. Esfuerzo estimado")
d.parrafo("El esfuerzo comprometido asciende a %s horas efectivas de consultoría, distribuidas en seis etapas "
          "conforme al siguiente cuadro:" % h(C["tot"]))
filas = [[ETAPA[k], h(v)] for k, v in C["hitos"].items()] + [["Total", h(C["tot"])]]
d.cuadro(["Etapa", "Horas"], filas, [5700, 1360])
T = C["tipos"]; otros = C["tot"] - T["Configuración"] - T["Datos"]
if KEY == "integral":
    CA, CI = ruta.cifras("contabilidad"), ruta.cifras("inventario")
    d.parrafo("De ese total, %s horas son propias del frente contable, %s del frente de inventario y %s de las "
              "tareas comunes de levantamiento, capacitación y cierre, que se ejecutan como una sola tarea."
              % (h(C["proys"]["Contabilidad"]), h(C["proys"]["Inventario"]), h(C["proys"]["Común"])))
d.parrafo("Del total, %s horas corresponden a configuración de la funcionalidad nativa, %s a depuración y "
          "corrección de información, y %s al levantamiento, la conciliación, la documentación, la capacitación y "
          "el cierre. Son horas efectivas de consultoría y no días naturales de duración del proyecto. El desglose "
          "en %d tareas, con su descripción y su etapa, se acompaña en el anexo en hoja de cálculo."
          % (h(T["Configuración"]), h(T["Datos"]), h(otros), C["n"]))

d.seccion("3. Plazo de ejecución")
if KEY == "integral":
    d.parrafo("El proyecto se ejecuta en un plazo de entre 3 y 4 meses contados a partir de la orden de inicio, "
              "previsto de octubre de 2026 a enero de 2027, con los frentes contable y de inventario en paralelo "
              "después del descubrimiento. El plazo está condicionado a la oportunidad con que Freshbox entregue "
              "estados de cuenta, XML de proveedor y la balanza validada por su contador, y el conteo físico y el "
              "cierre de valoración se programan sobre la fecha de corte que Freshbox determine.")
elif KEY == "contabilidad":
    d.parrafo("El proyecto se ejecuta en un plazo de entre 2 y 3 meses contados a partir de la orden de inicio, previsto de "
              "octubre a diciembre de 2026, de modo que el cierre de diciembre ya se haga con bancos conciliados y "
              "periodos bloqueados. El plazo está condicionado a la oportunidad con que Freshbox entregue los "
              "estados de cuenta y la balanza al 31 de diciembre de 2025 validada por su contador.")
else:
    d.parrafo("El proyecto se ejecuta en un plazo de entre 2 y 3 meses contados a partir de la orden de inicio, previsto de "
              "octubre a diciembre de 2026. El plazo está condicionado a la oportunidad con que Freshbox entregue "
              "los XML de sus proveedores y disponga del personal de almacén, y el conteo físico y el cierre de "
              "valoración se programan sobre la fecha de corte que Freshbox determine.")

d.seccion("4. Observaciones sobre la base actual")
d.parrafo("El diagnóstico general de la base, entregado el 29 de septiembre de 2026, arrojó las siguientes "
          "observaciones, que son las que este plan corrige:")
if KEY != "integral":
    d.vinetas(OBS[KEY])
else:
    d.vinetas([OBS["contabilidad"][0], OBS["contabilidad"][1], OBS["contabilidad"][3],
               OBS["inventario"][0], OBS["inventario"][1], OBS["inventario"][2]])

d.seccion("5. Supuestos, exclusiones y condiciones")
sup = ["El alcance del apartado 1 es el alcance contratado. Cualquier requerimiento adicional se cotiza y se autoriza por escrito antes de ejecutarse.",
       "El proyecto no incluye desarrollos y se resuelve con la funcionalidad nativa de Odoo y con cargas por plantilla.",
       "La construcción y las pruebas se ejecutan sobre una copia vigente de la base de producción, que Freshbox solicita al arranque porque la copia actual vence el 4 de octubre de 2026. El paso a producción se realiza con la guía de operación que se entrega al cierre."]
if KEY in ("contabilidad", "integral"):
    sup += ["El contador de Freshbox valida el catálogo final, la balanza y la cartera de clientes al 31 de diciembre de 2025, y autoriza las pólizas que prepara MLR Consultores. Los periodos anteriores al 1 de enero de 2026, incluidos los cobros de la carga histórica, se resuelven en la póliza de apertura y no se corrigen documento por documento.",
            "La fusión de cuentas se prueba en una base de pruebas antes de ejecutarse. Freshbox revoca las llaves expuestas en la base, y el responsable del proceso externo de cobranza lo apaga cuando se le solicite; ese proceso no forma parte del alcance.",
            "Freshbox entrega los extractos bancarios del periodo en archivo importable y la descarga de sus CFDI emitidos y recibidos del SAT; los complementos se timbran con su proveedor de certificación."]
if KEY in ("inventario", "integral"):
    sup += ["El conteo físico lo realiza el personal de Freshbox con las hojas de conteo que entrega MLR Consultores, y Freshbox entrega completos y en lote los XML de las facturas de proveedor del periodo.",
            "Las correcciones de costo se registran en pólizas agrupadas por mes con un anexo por factura. Si Odoo no permite cambiar la unidad de medida de los productos con existencia y hay que darlos de alta de nuevo, ese trabajo se cotiza aparte."]
if KEY == "inventario":
    sup += ["La conciliación final de la cuenta de inventario se hace sobre el catálogo de cuentas que valide el contador de Freshbox. Si la propuesta contable de la misma fecha no se contrata, el catálogo, la póliza de apertura y la depuración de la caja quedan a cargo de Freshbox."]
sup += ["Quedan fuera del alcance la corrección documento por documento del histórico 2022–2025, la integración con Shopify, los tableros a medida, el servicio contable recurrente, las declaraciones fiscales, los timbres y la suscripción de Odoo, que se contratan por separado.",
        "Freshbox designa un responsable con capacidad de decisión sobre los procesos del apartado 1, pone a disposición al personal de cada área y a su contador en las fechas convenidas y mantiene el acceso a la base de pruebas durante el proyecto."]
d.vinetas(sup)
d.cierre()
d.guarda(os.path.join(OUT, N2 + ".docx"))
print("ok", N2)

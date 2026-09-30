# -*- coding: utf-8 -*-
from comun import *

DIAG = "considerando el diagnóstico general de su base entregado el 29 de septiembre de 2026"
d = doc(["Cotización", "Proyecto Odoo"])

if KEY == "contabilidad":
    d.parrafo("Por medio de la presente, MLR Consultores presenta a Freshbox la propuesta económica para el "
              "saneamiento de la contabilidad, la cobranza y la conciliación de su base de Odoo 19, "
              "%s y un corte contable al 1 de enero de 2026 validado por su contador." % DIAG)
elif KEY == "inventario":
    d.parrafo("Por medio de la presente, MLR Consultores presenta a Freshbox la propuesta económica para el "
              "saneamiento del inventario, de los documentos de compra y venta y de la valoración de su base de "
              "Odoo 19, %s y el conteo físico que realizará su personal." % DIAG)
else:
    d.parrafo("Por medio de la presente, MLR Consultores presenta a Freshbox la propuesta económica para el "
              "saneamiento de su base de Odoo 19, con tres opciones de alcance que pueden contratarse por "
              "separado o en conjunto, %s y un corte contable al 1 de enero de 2026 validado por su contador." % DIAG)
d.parrafo("La propuesta se acompaña del plan de trabajo y alcance detallado y del anexo en hoja de cálculo con el "
          "desglose de las %d tareas." % C["n"])

d.seccion("1. Alcance del servicio propuesto")
if KEY == "contabilidad":
    d.parrafo("El proyecto se construye sobre la funcionalidad nativa de Odoo, con un esfuerzo de %s horas "
              "efectivas de consultoría, y comprende el levantamiento contable, fiscal y de cobranza con los "
              "criterios de configuración; la depuración de usuarios y permisos; el catálogo de cuentas con la "
              "fusión de las cuentas duplicadas, los impuestos y la póliza de apertura al 1 de enero de 2026; la "
              "depuración de los cobros registrados sin respaldo y de los pagos duplicados; la conciliación bancaria "
              "del periodo; la regularización de los movimientos contables contra los CFDI del SAT, con las facturas "
              "de gastos y los complementos de pago, y la capacitación grabada con el bloqueo de periodos y la "
              "revisión del primer cierre mensual." % h(C["tot"]))
    d.parrafo("Esta fase no incluye desarrollos. Los documentos de compra y venta, con sus facturas, y la valoración "
              "del inventario se atienden en la propuesta de inventario de la misma fecha.")
elif KEY == "inventario":
    d.parrafo("El proyecto se construye sobre la funcionalidad nativa de Odoo, con un esfuerzo de %s horas "
              "efectivas de consultoría, y comprende el levantamiento con los criterios de configuración; la "
              "corrección de categorías, productos, unidades, ubicaciones, lotes y fechas de caducidad y costes en "
              "destino; la regularización de "
              "existencias con el conteo físico y de los históricos de compras y de ventas, con sus documentos "
              "primarios y sus facturas; la valoración conciliada contra la cuenta de inventario, y la capacitación "
              "grabada con la revisión del primer cierre mensual." % h(C["tot"]))
    d.parrafo("Esta fase no incluye desarrollos. Los movimientos registrados directamente en contabilidad, la "
              "cobranza y la conciliación bancaria se atienden en la propuesta contable de la misma fecha.")
else:
    CA, CI = ruta.cifras("contabilidad"), ruta.cifras("inventario")
    d.parrafo("El proyecto se construye sobre la funcionalidad nativa de Odoo y se presenta en tres opciones: "
              "contabilidad, cobranza y conciliación, con %s horas efectivas; inventario, compras, ventas y "
              "valoración, con %s horas; y la conjunta, con %s horas, que reúne ambas en un solo proyecto con un "
              "flujo objetivo, una capacitación y un cierre comunes." % (h(CA["tot"]), h(CI["tot"]), h(C["tot"])))
    d.parrafo("Ninguna de las opciones incluye desarrollos, y cada una cuenta con su propia propuesta, plan de "
              "trabajo y anexo de la misma fecha.")

d.seccion("2. Inversión")
if KEY != "integral":
    d.parrafo("MLR Consultores ofrece a Freshbox una tarifa de %s por hora, aplicable por igual a todo el trabajo y "
              "condicionada a la aceptación por escrito de esta cotización a más tardar el %s. Con esa tarifa, el alcance "
              "del apartado 1 importa %s antes del impuesto al valor agregado. La tarifa comprende el levantamiento, la "
              "configuración, la depuración de información, la capacitación y el acompañamiento del primer cierre, sin "
              "cargos adicionales por traslados."
              % (m(P["tarifa_pref"]), P["fecha_limite"], m(C["p"])))
else:
    d.parrafo("MLR Consultores ofrece a Freshbox una tarifa de %s por hora, aplicable por igual a todo el trabajo y "
              "condicionada a la aceptación por escrito de esta cotización a más tardar el %s. Con esa tarifa y antes del "
              "impuesto al valor agregado, la opción contable importa %s, la de inventario %s y la conjunta %s."
              % (m(P["tarifa_pref"]), P["fecha_limite"], m(CA["p"]), m(CI["p"]), m(C["p"])))

d.seccion("3. Esquemas de pago")
if KEY != "integral":
    d.parrafo("Los tres esquemas difieren únicamente en el calendario de desembolso. En el esquema A, el anticipo "
              "del 30%% se cubre a la firma y el 70%% de cada hito se factura al iniciarlo; en el B, cada uno de los "
              "%d pagos mensuales es de %s y se factura al inicio del mes que ampara; y en el C, el descuento por "
              "pago a la firma es de %s, con una tarifa efectiva de %s por hora."
              % (C["pagos_b"], m(C["b"]), m(C["desc"]), m(C["tarifa_c"])))
    d.cuadro(["Esquema", "Forma de pago", "Importe"], [
        ["A. Por hitos", "Anticipo y saldo por hito", m(C["p"])],
        ["B. Mensual", "%d pagos mensuales iguales" % C["pagos_b"], m(C["p"])],
        ["C. Pago único", "Un pago, 5% de descuento", m(C["c"])],
    ], [2400, 4000, 2800])
    fa = [["Anticipo a la firma", "", m(C["ant"])]]
    for k, hh in C["hitos"].items():
        fa.append(["%s. %s" % (k, ETAPA[k]), h(hh), m(C["hito_saldo"][k])])
    fa.append(["Total antes de IVA", h(C["tot"]), m(C["p"])])
    d.cuadro(["Esquema A — concepto", "Horas", "Importe"], fa, [6400, 900, 1900])
else:
    OP = [CA, CI, C]
    d.parrafo("Los tres esquemas difieren únicamente en el calendario de desembolso. En el esquema A, el anticipo del 30%% se cubre a la firma y el 70%% de cada hito se factura "
              "al iniciarlo; en el B, los pagos mensuales iguales se facturan al inicio del mes que amparan, en %d "
              "pagos para cada proyecto por separado y en %d para la opción conjunta; y en el C, el pago a la firma "
              "lleva un descuento del 5%%, de %s en la opción conjunta, con una tarifa efectiva de %s por hora. El calendario por hitos de cada proyecto consta en su propuesta."
              % (CA["pagos_b"], C["pagos_b"], m(C["desc"]), m(C["tarifa_c"])))
    d.cuadro(["Esquema", "Contabilidad", "Inventario", "Conjunta"], [
        ["A. Por hitos"] + [m(x["p"]) for x in OP],
        ["B. Mensual"] + ["%d pagos de %s" % (x["pagos_b"], m(x["b"])) for x in OP],
        ["C. Pago único"] + [m(x["c"]) for x in OP],
    ], [2000, 2400, 2400, 2400])
    fa = [["Anticipo a la firma", "", m(C["ant"])]]
    for k, hh in C["hitos"].items():
        fa.append(["%s. %s" % (k, ETAPA[k]), h(hh), m(C["hito_saldo"][k])])
    fa.append(["Total antes de IVA", h(C["tot"]), m(C["p"])])
    d.cuadro(["Esquema A de la opción conjunta", "Horas", "Importe"], fa, [6400, 900, 1900])

d.seccion("4. Condiciones esenciales")
d.vinetas([
 "Importes en pesos mexicanos (MXN), más IVA (16%%). La tarifa ofertada y el descuento del esquema C rigen hasta el %s." % P["fecha_limite"],
 "Toda factura se paga por anticipado, y MLR Consultores no inicia el trabajo de un mes o de un hito cuya factura no haya sido cubierta.",
 "Todo requerimiento adicional se cotiza a la misma tarifa; el servicio contable recurrente, los timbres del proveedor de certificación y la suscripción de Odoo se contratan por separado.",
 "Para dar inicio se requiere la aceptación por escrito con la opción y el esquema elegidos, una copia vigente de la base de producción en el entorno de pruebas y la designación de un responsable con capacidad de decisión." if KEY == "integral" else
 "Para dar inicio se requiere la aceptación por escrito con el esquema elegido, una copia vigente de la base de producción en el entorno de pruebas y la designación de un responsable con capacidad de decisión.",
])
d.parrafo("El alcance de esta propuesta admite ajuste en ambos sentidos. Si al revisarla identifican procesos que "
          "convenga incorporar, o partidas que su operación no requiera en esta etapa, se integran al plan y el "
          "importe se recalcula sobre la misma tarifa.", before=40)
d.cierre("Proponemos una sesión de revisión previa a la firma para precisar los puntos que consideren. De esa "
         "sesión sale la versión definitiva del alcance, y con su aprobación se programa el arranque del proyecto.")
d.guarda(os.path.join(OUT, N1 + ".docx"))
print("ok", N1)

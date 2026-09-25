# -*- coding: utf-8 -*-
# Single source of content for the Word and HTML versions of a functional guide.
# Example filled with the Acretex guide (25-sep-2026). Copy it next to the client's
# captures, replace the texts and keep the structure: both generators read only this.
TITULO = ["Venta sin factura", "Guía funcional"]
CLIENTE = "Acojinados y Recubrimientos Textiles"   # one line: the carátula check fails if it wraps
FECHA = "25 de septiembre de 2026"
SALUDO = "Estimado Sr. Alan Cohen:"
ATENCION = "Sr. Alan Cohen"            # cover of the HTML; in Word the addressee goes in SALUDO
SISTEMA = "Odoo 19 · Plataforma MLR"
BARRA = "Venta sin factura — Acretex — Odoo"          # text next to the logo in the top bar
TITULO_HTML = "Venta sin factura · Guía funcional · Acretex"
PORTADA = {
    "kicker": "Guía funcional · Venta sin factura, consignación y factura global",
    "titular": "Cada venta sin factura queda controlada desde la entrega hasta la factura global",
}
# Headline of each HTML sheet: a conclusion, not a topic label. Key = section id,
# or the step number ("3.1") for the sheets that come out of ("h", ...) subheadings.
TITULARES = {
    "resumen": "La mercancía, el cobro y el costo quedan amarrados a la orden",
    "preparacion": "El sistema hace solo los movimientos contables; el usuario solo opera ventas",
    "3.1": "Una casilla convierte la orden en venta sin factura",
    "3.2": "La entrega se desvía sola a consignación y deja su asiento",
    "3.3": "Una devolución corrige la orden y el asiento en un solo paso",
    "3.4": "El cobro en efectivo se liga a la orden y se ve en la lista",
    "3.5": "La factura global reúne las órdenes y conserva cada cantidad",
    "3.6": "Al publicar la factura sale la mercancía y se registra el costo",
    "3.7": "La factura global se paga como cualquier factura",
    "3.8": "Corregir la factura regresa la mercancía a consignación",
    "candados": "Los errores frecuentes quedan bloqueados con un mensaje que dice qué hacer",
    "pruebas": "El proceso completo pasó todas las pruebas y se instaló limpio en otra base",
    "produccion": "El desarrollo ya opera en producción y quedan cinco puntos por cerrar",
}
# Tests table and production paragraph: filled from datos.json when they depend on
# results that arrive late (installation logs). "__PRUEBAS__" / "__PRODUCCION__" in the blocks.
DATOS = {
 "pruebas": [
  ["Recorrido completo de la orden al pago de la factura global (21 validaciones)", "Pruebas Acretex", "Correcto"],
  ["Instalación desde la Plataforma MLR (65 elementos, 0 errores)", "Edu consultores", "Correcto"],
 ],
 "produccion": "La versión 1.3.8 quedó instalada en la base productiva la noche del 24 de septiembre de 2026, con 78 elementos correctos, sin avisos ni errores.",
}

INTRO = ("Por medio de la presente, MLR Consultores presenta a Acojinados y Recubrimientos Textiles la guía "
         "funcional del desarrollo de venta sin factura, consignación y factura global en Odoo, que explica paso a "
         "paso cómo se registra una venta que el cliente se lleva sin factura, cómo se cobra en efectivo y cómo se "
         "factura después en una factura global, con las pantallas reales del sistema tomadas de la base de pruebas.")

# Each section: (id, menu label, title, blocks). Blocks: ("p", text) | ("v", [items]) |
# ("fig", key, caption) | ("t", header, rows, widths) | ("kpi", [(big, label), ...]) | ("flujo", [(title, text), ...])
# ("h", "3.1 ...") inside a section splits it into one HTML sheet per subheading.
SECCIONES = [
 ("resumen", "Resumen", "1. Qué resuelve el desarrollo", [
  ("p", "Hasta ahora una venta que no se facturaba en el momento quedaba fuera de control, porque la mercancía salía "
        "del almacén, el cobro se registraba por separado y el costo no llegaba a la contabilidad hasta que alguien "
        "emitía la factura. Con el desarrollo basta marcar la orden como venta sin factura. La mercancía entregada queda "
        "registrada como mercancía en consignación y el cobro en efectivo se liga a la orden. Cuando se emite la factura global, la mercancía sale de la consignación y el costo de venta se "
        "registra una sola vez, en el mismo momento en que se reconoce el ingreso."),
  ("kpi", [("1", "casilla en la orden para indicar que es venta sin factura"),
           ("2", "acciones nuevas en el menú Acciones de ventas"),
           ("0", "capturas manuales de asientos contables"),
           ("21", "validaciones superadas en la prueba completa del proceso")]),
  ("p", "Todo ocurre en la empresa Acojinados y Recubrimientos Textiles; la empresa Mostrador queda fuera del desarrollo, "
        "de acuerdo con lo definido en la reunión del 5 de agosto, en la que se acordó centralizar la operación en una sola "
        "entidad y costear estas ventas con cuentas de orden."),
 ]),
 ("preparacion", "Antes de empezar", "2. Qué se configuró y quién lo usa", [
  ("p", "El desarrollo agrega a Odoo un almacén llamado Material Consignado, donde se guarda la mercancía entregada que "
        "todavía no se factura, la cuenta 115.01.03 Mercancía en Consignación, el diario Efectivo sin Factura para los "
        "cobros y la cuenta 9996 de cobro por orden. Ninguno de estos elementos requiere captura adicional por parte del "
        "usuario, porque el sistema los usa por sí solo en cada paso."),
  # ("flujo", ...) draws the numbered process line in the HTML; Word skips it.
  ("flujo", [("Orden", "se marca venta sin factura"), ("Entrega", "va a Material Consignado"),
             ("Cobro", "en efectivo, ligado a la orden"), ("Factura global", "una línea por línea de orden"),
             ("Salida y costo", "al publicar la factura"), ("Pago", "por transferencia")]),
  ("p", "Las órdenes marcadas como venta sin factura y sus cobros en efectivo solo son visibles para los usuarios del grupo "
        "Ventas sin factura; los movimientos de inventario y los asientos contables siguen visibles para contabilidad, de "
        "modo que el control del almacén y de los saldos no depende de quién pertenezca al grupo."),
 ]),
 ("orden", "Paso a paso", "3. El proceso paso a paso", [
  ("h", "3.1 Registrar la orden como venta sin factura"),
  ("p", "La orden se captura igual que cualquier otra venta, con el cliente, los productos y los precios, y antes de "
        "confirmarla se marca la casilla Venta sin factura registrada. Desde ese momento la orden muestra tres importes "
        "adicionales que acompañan todo el proceso: el importe no facturado, el total abonado y el pendiente de pago."),
  ("fig", "01", "Orden S07976 marcada como venta sin factura; al cierre del proceso muestra 315.52 pesos abonados y nada pendiente."),
  ("h", "3.2 Entregar la mercancía"),
  ("p", "Al confirmar la orden, la entrega se dirige automáticamente al almacén Material Consignado en lugar de salir al "
        "cliente. Cuando el almacén valida la entrega, Odoo registra el asiento que traslada el valor de la mercancía del "
        "inventario a la cuenta Mercancía en Consignación, con el cliente y la orden en cada línea para poder rastrearlo."),
  ("fig", "02", "Movimientos de la orden S07976: la entrega WHACR/OUT/02517 lleva la mercancía de WHACR/Stock a MCON/Existencias y la devolución WH/RET/00034 regresa 1 kg."),
  ("fig", "03", "Asiento de consignación STJ/2026/09/0183, que carga 267.46 pesos a la cuenta 115.01.03 Mercancía en Consignación."),
  ("h", "3.3 Registrar una devolución"),
  ("p", "Si el cliente regresa parte de la mercancía, la devolución se hace desde la propia entrega con el botón Devolver. "
        "Al validarla, el sistema reduce la cantidad de la orden, deja una nota en el historial con la cantidad anterior y "
        "la nueva, y registra el asiento inverso de consignación; en el ejemplo, la orden pasó de 6 a 5 kg del primer "
        "producto y el asiento STJ/2026/09/0184 regresó 29.89 pesos al inventario."),
  ("fig", "04", "Historial de la orden S07976 con la nota de la devolución WH/RET/00034 y la cantidad ajustada de 6 a 5 kg."),
  ("h", "3.4 Cobrar en efectivo"),
  ("p", "El cobro se registra desde la orden con el botón Aplicar pago o desde la lista de órdenes con Acciones, Aplicar pago en "
        "efectivo. El asistente propone el diario Efectivo sin Factura, la cuenta 9996 y el importe pendiente de cada orden. Al "
        "confirmarlo crea el pago con forma de pago 01 Efectivo ligado a la orden, sin relación con ninguna factura. Si se "
        "seleccionan varias órdenes del mismo cliente, la casilla Agrupar en un pago permite registrar un solo cobro por todas."),
  ("fig", "05", "Menú Acciones de la lista de órdenes con Generar factura global y Aplicar pago en efectivo al final."),
  ("fig", "06", "Asistente de pago en efectivo para S07977 y S07978, con el diario Efectivo sin Factura, la cuenta 9996 y 176.32 pesos pendientes."),
  ("fig", "07", "Pago PCSH2/2026/00018 por 315.52 pesos con forma de pago Efectivo, ligado a la orden S07976."),
  ("p", "La lista de órdenes muestra la columna Pendiente, de modo que el área de cobranza identifica de un vistazo qué "
        "ventas sin factura siguen sin pagarse, tal como se solicitó en la reunión del 5 de agosto."),
  ("fig", "08", "Lista de órdenes con la columna Pendiente: S07976 ya cobrada, S07977 y S07978 con saldo por cobrar."),
  ("h", "3.5 Generar la factura global"),
  ("p", "Cuando se decide facturar, se seleccionan las órdenes en la lista y se elige Acciones, Generar factura global. "
        "El asistente propone el cliente cuando todas las órdenes son del mismo, permite agregar las órdenes a una factura "
        "global que ya esté en borrador y, al confirmar, crea la factura con una línea por cada línea de orden, identificada "
        "con el número de la orden entre paréntesis para que cada venta conserve su cantidad."),
  ("fig", "09", "Asistente Generar factura global con las órdenes S07977 y S07978 y el cliente propuesto."),
  ("fig", "10", "Factura global INV/2026/00661 con una línea por cada línea de orden, identificada con la orden S07976, y política de pago PPD."),
  ("p", "La factura global nace con política de pago PPD. Con PPD Odoo no muestra la forma de pago en la factura, porque al "
        "timbrar emite la forma 99 que el SAT exige para ese método; el sistema deja registrada la Transferencia para que el "
        "asistente de pago la proponga cuando se cobre por banco."),
  ("h", "3.6 Publicar la factura global"),
  ("p", "Al publicar la factura, el sistema entrega al cliente desde Material Consignado exactamente lo facturado, con un "
        "albarán por orden, y Odoo registra el costo de venta en ese momento. Si la factura trae más cantidad de la que hay "
        "en consignación, por ejemplo porque una entrega quedó parcial, el sistema no permite publicarla hasta completar la "
        "entrega o ajustar la cantidad."),
  ("fig", "11", "Salida MCON/OUT/00085 desde MCON/Existencias, creada y validada al publicar la factura INV/2026/00661."),
  ("h", "3.7 Pagar la factura global"),
  ("p", "La factura global se paga como cualquier factura de cliente, con el botón Pagar y el banco correspondiente contra "
        "la cuenta de clientes. El cobro en efectivo del paso 3.4 no se aplica a esta factura, porque es un pago ligado a la "
        "orden y así quedó definido."),
  ("fig", "12", "Asistente Pagar de la factura INV/2026/00661 con la forma de pago Transferencia electrónica de fondos propuesta."),
  ("h", "3.8 Corregir una factura global"),
  ("p", "Si la factura global se regresa a borrador o se cancela, la mercancía vuelve a Material Consignado y la orden queda "
        "facturable de nuevo; al publicarla otra vez, el sistema vuelve a entregar desde consignación sin duplicar el costo."),
 ]),
 ("candados", "Protecciones", "4. Qué impide el sistema", [
  ("p", "El desarrollo incluye protecciones que evitan los errores más frecuentes del proceso, y en cada caso el sistema "
        "muestra un mensaje en español que indica qué hacer."),
  ("fig", "13", "Mensaje que aparece al confirmar una factura hecha con Crear facturas para la venta sin factura S07978."),
  ("t", ["Situación", "Qué hace el sistema"], [
     ["Facturar una venta sin factura con el botón nativo Crear facturas", "No permite publicar esa factura e indica eliminar el borrador y usar Generar factura global"],
     ["Publicar una factura global con más cantidad de la consignada", "Detiene la publicación hasta completar la entrega o ajustar la cantidad"],
     ["Devolver más de lo que la orden tiene en consignación", "Rechaza la devolución"],
     ["Generar la global con órdenes que ya están en un borrador", "Indica en qué factura están y si hay que publicarla o eliminarla"],
     ["Cobrar dos veces una orden o cobrar una orden normal", "Rechaza el cobro"],
     ["Generar la global de una cotización sin confirmar", "Pide confirmar la orden primero"],
   ], [4200, 5000]),
 ]),
 ("pruebas", "Pruebas", "5. Pruebas realizadas", [
  ("p", "El desarrollo se probó en la base de pruebas de Acojinados y Recubrimientos Textiles con un recorrido "
        "que ejecuta el proceso completo, desde la orden hasta el pago de la factura global, más las pruebas de cada "
        "protección. Después se instaló desde la Plataforma MLR en una base distinta para confirmar que funciona fuera de "
        "la base original."),
  ("p", "Durante las pruebas se verificó además que el saldo de la cuenta 115.01.03 Mercancía en Consignación coincide con "
        "el valor de la mercancía que permanece en el almacén Material Consignado."),
  ("p", "El recorrido completo se ejecuta dentro de una sola operación que el sistema revierte al terminar, por lo que "
        "puede repetirse cuantas veces se necesite sin dejar órdenes, pagos ni facturas en la base."),
  ("t", ["Prueba", "Base", "Resultado"], "__PRUEBAS__", [4600, 2700, 1900]),
 ]),
 ("produccion", "Producción", "6. Puesta en producción y pendientes", [
  ("p", "__PRODUCCION__"),
  ("v", ["Validar con el área contable el tratamiento de la mercancía en consignación y del costo de venta, conforme a lo acordado en la reunión del 23 de septiembre.",
         "Definir si en las ventas sin factura se usarán anticipos y cómo se descontarán en la factura global.",
         "Revisar las ventas sin factura que se entregaron antes de la instalación, porque su mercancía no pasó por Material Consignado.",
         "Depurar los productos duplicados POLSIL A 1564 y POLSIL A 1864 antes de migrar los inventarios.",
         "Agregar al grupo Ventas sin factura a los usuarios que registrarán estas ventas y sus cobros."]),
 ]),
]

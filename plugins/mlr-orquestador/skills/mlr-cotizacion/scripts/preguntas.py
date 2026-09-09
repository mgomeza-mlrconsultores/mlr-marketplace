# -*- coding: utf-8 -*-
"""
Cuestionario de descubrimiento MLR — origen unico de las preguntas.

De aqui salen el libro de captura en Excel y la guia de reunion en Word. Si una
pregunta cambia, cambia en los dos.

Estructura de cada bloque: (clave, nombre de la aplicacion, minutos, nucleo, preguntas)
  nucleo=True  -> se pregunta siempre
  nucleo=False -> solo se abre si el cliente lo menciona o si el alcance lo pide

Cada pregunta: (texto, tipo, opciones)
  tipo: "opcion" (lista cerrada), "numero", "texto", "si/no"
"""

# Estados que se repiten en casi toda aplicacion. La respuesta mueve el precio:
# lo que no existe se configura, lo que esta a medias se revisa y se corrige, y
# revisar suele costar mas que configurar de cero.
ESTADO = ["No existe", "En Excel o en papel", "En otro sistema",
          "En Odoo, a medias", "En Odoo, operando bien"]
MIGRA = ["No se migra", "Solo saldos a fecha de corte", "Catalogo sin histórico",
         "Catalogo con histórico", "Por definir"]

FICHA = [
    ("¿Sobre qué modalidad corre Odoo hoy?", "opcion",
     ["Odoo Online (SaaS)", "Odoo.sh", "On-premise (servidor propio)", "Todavía no tienen Odoo"]),
    ("¿Qué edición tienen contratada?", "opcion",
     ["Community", "Standard", "Enterprise", "Todavía no contratan"]),
    ("¿En qué versión exacta de Odoo están, mayor y menor?", "texto", []),
    ("¿Cuándo fue la última actualización de versión?", "texto", []),
    ("¿Tienen pendiente un salto de versión, y a cuál?", "texto", []),
    ("¿Cuántos usuarios internos van a entrar al sistema?", "numero", []),
    ("¿Cuántos usuarios de portal, para clientes o proveedores?", "numero", []),
    ("¿Cuántas razones sociales van a operar en el sistema?", "numero", []),
    ("¿Cuántas sedes físicas y cuántos almacenes tienen?", "texto", []),
    ("¿Quién administra Odoo hoy dentro de la empresa?", "texto", []),
    ("¿Hubo un implementador anterior, y sigue trabajando con ustedes?", "texto", []),
    ("¿Cuántos desarrollos o personalizaciones les hicieron ya?", "numero", []),
    ("¿Esos desarrollos están documentados y saben quién los hizo?", "opcion",
     ["Sí, documentados", "Sí, sin documentar", "No lo sabemos", "No hay desarrollos"]),
    ("¿En qué idiomas y monedas necesitan operar?", "texto", []),
    ("¿Con qué otros sistemas tiene que hablar Odoo?", "texto", []),
    ("¿Para qué fecha necesitan estar operando?", "texto", []),
    ("¿Quién decide y quién firma del lado de ustedes?", "texto", []),
]

# --- espina dorsal, igual en toda aplicacion ------------------------------
def espina(app, unidad, ejemplo_volumen):
    return [
        ("¿Dónde vive hoy %s?" % app, "opcion", ESTADO),
        ("¿Qué volumen manejan: %s?" % ejemplo_volumen, "numero", []),
        ("¿Cuántas personas trabajan en %s?" % unidad, "numero", []),
        ("¿Qué hay que migrar y desde dónde?", "opcion", MIGRA),
        ("¿Qué de todo esto NO se resuelve como lo hace Odoo de fábrica?", "texto", []),
    ]

BLOQUES = [
 ("contabilidad", "Contabilidad y Finanzas", 5, True,
  espina("la contabilidad", "contabilidad", "pólizas al mes") + [
   ("¿Quién lleva la contabilidad hoy, interno o despacho externo?", "texto", []),
   ("¿Usan el catálogo de cuentas del SAT o uno propio?", "opcion",
    ["Catálogo SAT", "Catálogo propio", "Mixto", "Por definir"]),
   ("¿Qué fecha de corte quieren para el saldo inicial?", "texto", []),
   ("¿Necesitan contabilidad analítica por obra, proyecto o línea de negocio?", "si/no", []),
   ("¿Van a llevar presupuesto y compararlo contra lo ejercido?", "si/no", []),
   ("¿Necesitan consolidar las razones sociales en un solo estado financiero?", "si/no", []),
   ("¿Qué reportes financieros entregan hoy y a quién?", "texto", []),
  ]),

 ("facturacion", "Facturación electrónica (CFDI)", 4, True,
  espina("la facturación", "facturación", "facturas al mes") + [
   ("¿Quién les timbra hoy y con qué proveedor?", "texto", []),
   ("¿Tienen los sellos digitales vigentes de cada razón social?", "si/no", []),
   ("¿Emiten complemento de pago, carta porte o comercio exterior?", "texto", []),
   ("¿Facturan al público en general con factura global?", "si/no", []),
   ("¿Emiten notas de crédito y con qué frecuencia?", "texto", []),
   ("¿Las razones sociales se facturan entre ellas?", "si/no", []),
  ]),

 ("ventas", "Ventas", 4, True,
  espina("el ciclo de venta", "ventas", "cotizaciones y pedidos al mes") + [
   ("¿Cómo cotizan hoy y con qué herramienta?", "texto", []),
   ("¿Manejan listas de precio distintas por cliente o por canal?", "si/no", []),
   ("¿Cobran anticipos antes de entregar?", "si/no", []),
   ("¿Necesitan que el cliente firme la cotización electrónicamente?", "si/no", []),
   ("¿Cuántos productos y servicios tiene el catálogo?", "numero", []),
   ("¿Manejan descuentos y quién los autoriza?", "texto", []),
  ]),

 ("compras", "Compras", 3, True,
  espina("las compras", "compras", "órdenes de compra al mes") + [
   ("¿Compran al extranjero y necesitan pedimento y arancel en el costo?", "si/no", []),
   ("¿El proveedor entrega directo al cliente o siempre entra a almacén?", "opcion",
    ["Siempre a almacén", "A veces directo a sitio", "Casi siempre directo", "Por definir"]),
   ("¿Autorizan las compras por monto y quién autoriza?", "texto", []),
   ("¿Cuántos proveedores activos tienen?", "numero", []),
   ("¿Reponen por mínimos o compran contra pedido?", "opcion",
    ["Contra pedido", "Por mínimos", "Ambos", "Por definir"]),
  ]),

 ("inventario", "Inventario y Almacén", 6, True,
  espina("el inventario", "almacén", "movimientos al mes") + [
   ("¿Cuántos productos tienen en existencia y cuánto vale el inventario?", "texto", []),
   ("¿Manejan ubicaciones dentro del almacén?", "si/no", []),
   ("¿Controlan lote o número de serie, y en qué productos?", "opcion",
    ["Ninguno", "Lote", "Número de serie", "Ambos"]),
   ("¿Con qué método valúan el inventario?", "opcion",
    ["Costo estándar", "Promedio ponderado", "PEPS", "No lo sabemos"]),
   ("¿La valuación es automática o manual en el sistema actual?", "opcion",
    ["Automática", "Manual", "No lo sabemos"]),
   ("¿Cada cuánto hacen conteo físico y cuándo fue el último?", "texto", []),
   ("¿Qué diferencia salió en el último conteo?", "texto", []),
   ("¿Quién autoriza un ajuste de inventario?", "texto", []),
   ("¿Tienen inventario en consignación o en poder de terceros?", "si/no", []),
   ("¿Manejan unidades de medida distintas para comprar y para vender?", "si/no", []),
   ("¿Hay producto sin movimiento o caducado que haya que castigar?", "si/no", []),
   ("¿Mueven mercancía entre almacenes o entre razones sociales?", "si/no", []),
  ]),

 ("fabricacion", "Fabricación y Listas de Materiales", 4, False,
  espina("la producción", "producción", "órdenes de fabricación al mes") + [
   ("¿Fabrican, ensamblan o solo arman kits para vender?", "opcion",
    ["Fabricación real", "Ensamble", "Kits", "Nada de esto"]),
   ("¿Cuántas listas de materiales tienen y de cuántos niveles?", "texto", []),
   ("¿Maquilan con terceros alguna etapa?", "si/no", []),
   ("¿Necesitan costo de producción por orden?", "si/no", []),
  ]),

 ("proyectos", "Proyectos", 3, False,
  espina("la gestión de proyectos", "proyectos", "proyectos abiertos") + [
   ("¿Registran horas del personal contra el proyecto?", "si/no", []),
   ("¿Necesitan ver el margen de cada proyecto u obra?", "si/no", []),
   ("¿Facturan por avance o por entregable?", "texto", []),
  ]),

 ("campo", "Servicio de Campo", 3, False,
  espina("el servicio en sitio", "servicio de campo", "servicios al mes") + [
   ("¿Cuántos técnicos salen a campo?", "numero", []),
   ("¿El técnico consume material en sitio y hay que descargarlo?", "si/no", []),
   ("¿Necesitan firma del cliente en sitio?", "si/no", []),
   ("¿Facturan desde la propia orden de servicio?", "si/no", []),
  ]),

 ("nomina", "Nómina y Recursos Humanos", 3, False,
  espina("la nómina", "recursos humanos", "colaboradores en plantilla") + [
   ("¿Con qué sistema procesan la nómina hoy?", "texto", []),
   ("¿Con qué periodicidad pagan?", "opcion", ["Semanal", "Quincenal", "Mensual", "Mixta"]),
   ("¿Quién hace los movimientos ante el IMSS?", "texto", []),
   ("¿Necesitan control de asistencia y vacaciones en el sistema?", "si/no", []),
  ]),

 ("crm", "CRM", 2, False,
  espina("el seguimiento comercial", "el área comercial", "oportunidades al mes") + [
   ("¿Cuántos vendedores tienen y cómo miden su desempeño?", "texto", []),
   ("¿De dónde llegan los prospectos?", "texto", []),
  ]),

 ("pos", "Punto de Venta", 2, False,
  espina("el punto de venta", "punto de venta", "tickets al día") + [
   ("¿Cuántas cajas o terminales tienen y en cuántas sucursales?", "texto", []),
   ("¿Qué formas de pago aceptan en mostrador?", "texto", []),
   ("¿Necesitan que el punto de venta opere sin internet?", "si/no", []),
  ]),

 ("ecommerce", "Comercio Electrónico y Sitio Web", 2, False,
  espina("la venta en línea", "la tienda en línea", "pedidos en línea al mes") + [
   ("¿Tienen tienda en línea hoy y en qué plataforma?", "texto", []),
   ("¿Con qué pasarela de pago cobran?", "texto", []),
   ("¿Quién les paqueteria y envíos?", "texto", []),
  ]),

 ("mantenimiento", "Mantenimiento", 2, False,
  espina("el mantenimiento de equipos", "mantenimiento", "equipos en el padrón") + [
   ("¿Llevan mantenimiento preventivo con calendario?", "si/no", []),
   ("¿Quién atiende las fallas, personal propio o externo?", "texto", []),
  ]),

 ("calidad", "Calidad", 2, False,
  espina("el control de calidad", "calidad", "inspecciones al mes") + [
   ("¿En qué punto del proceso inspeccionan?", "texto", []),
   ("¿Tienen certificación que obligue a dejar evidencia?", "si/no", []),
  ]),

 ("gastos", "Gastos y Viáticos", 2, False,
  espina("la comprobación de gastos", "administración", "comprobaciones al mes") + [
   ("¿Quién autoriza un gasto y hasta qué monto?", "texto", []),
   ("¿Los colaboradores suben su comprobante o lo entregan en papel?", "texto", []),
  ]),

 ("suscripciones", "Suscripciones y Contratos Recurrentes", 2, False,
  espina("la facturación recurrente", "administración", "contratos vigentes") + [
   ("¿Con qué periodicidad facturan el recurrente?", "texto", []),
   ("¿Cómo manejan altas, bajas y cambios a media vigencia?", "texto", []),
  ]),

 ("documentos", "Documentos y Firma Electrónica", 2, False,
  espina("la firma de documentos", "administración", "documentos a firmar al mes") + [
   ("¿Qué documentos necesitan que el cliente firme?", "texto", []),
   ("¿Usan alguna herramienta de firma hoy?", "texto", []),
  ]),
]

CIERRE = [
    ("¿Qué fecha de corte van a usar para el arranque?", "texto", []),
    ("¿Quién de su equipo va a entregar los datos a migrar?", "texto", []),
    ("¿En qué formato pueden entregar la información?", "texto", []),
    ("¿Qué personas van a recibir capacitación y de qué áreas?", "texto", []),
    ("¿Qué NO quieren tocar en esta etapa?", "texto", []),
    ("¿Hay alguna fecha fiscal o de negocio que condicione el calendario?", "texto", []),
]

# Detonantes de costo: lo que convierte una respuesta en horas.
DETONANTES = [
    "Cada aplicación en «No existe» se configura desde cero.",
    "Cada aplicación en «En Odoo, a medias» se revisa y se corrige, y eso "
    "normalmente cuesta más que configurarla de cero.",
    "Cada «no se resuelve de fábrica» es desarrollo y se cotiza como desarrollo, "
    "nunca como configuración.",
    "Cada razón social multiplica la configuración contable y fiscal.",
    "Cada catálogo con histórico multiplica el trabajo de migración frente a "
    "migrar solo saldos a fecha de corte.",
    "Cada desarrollo previo sin documentar es riesgo: hay que leerlo antes de tocar nada.",
]

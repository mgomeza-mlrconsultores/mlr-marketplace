# -*- coding: utf-8 -*-
"""Single source of truth for the three Freshbox quotations (accounting, inventory, integral).
Word and Excel are built from here. Amounts are always computed, never typed."""
from decimal import Decimal, ROUND_HALF_UP

PARAMS = {
    "cliente":         "GAPA LA BAJA, S.A. de C.V.",
    "corto":           "Freshbox",
    "atencion":        "Dirección general de Freshbox",
    "fecha_emision":   "29 de septiembre de 2026",
    "fecha_limite":    "viernes 16 de octubre de 2026",
    "tarifa_lista":    1500,
    "tarifa_pref":     900,
    "anticipo":        0.30,
    "descuento_unico": 0.05,
}

# (num, aplicacion, tarea, subtarea, tipo de trabajo, horas, hito, descripcion)
CONTABILIDAD = [
 ("1.1.1","Descubrimiento","Levantamiento operativo","Levantamiento contable y fiscal","Levantamiento",2,"Hito 1",
  "Con el contador de la empresa, catálogo de cuentas vigente, criterios de apertura, fecha de corte, cierre de periodos y proveedor de timbrado."),
 ("1.1.2","Descubrimiento","Levantamiento operativo","Levantamiento de cobranza y bancos","Levantamiento",1,"Hito 1",
  "Cuentas bancarias, formas de cobro, manejo y depósito del efectivo y extractos disponibles."),
 ("1.1.3","Descubrimiento","Levantamiento operativo","Flujo objetivo y criterios de configuración","Entregable",1.5,"Hito 1",
  "Diagrama del proceso de facturación, cobro, depósito, conciliación y cierre con el documento de Odoo que afecta cada paso, y criterios firmados antes de configurar."),
 ("2.1.1","Configuración general","Seguridad","Usuarios y permisos","Configuración",1,"Hito 1",
  "Depuración de los permisos de administrador por aplicación, doble factor de autenticación y usuario propio para integraciones."),
 ("3.1.1","Contabilidad","Configuración contable","Plan de cuentas","Datos",10,"Hito 2",
  "Definición del catálogo final con el contador, fusión de las cuentas duplicadas con su cuenta correcta, tipo, naturaleza y código agrupador del SAT, y archivo de las cuentas sobrantes."),
 ("3.1.2","Contabilidad","Configuración contable","Diarios y cuentas predeterminadas","Configuración",1.5,"Hito 2",
  "Cuentas de cada diario y cuentas predeterminadas de la compañía."),
 ("3.1.3","Contabilidad","Configuración contable","Impuestos","Configuración",2,"Hito 2",
  "Tasas, reparto de cuentas de cada impuesto, impuestos especiales sobre producción y servicios, impuestos duplicados y posiciones fiscales."),
 ("3.2.1","Contabilidad","Apertura","Saldos iniciales","Datos",9,"Hito 2",
  "Póliza de apertura a la fecha de corte con la balanza validada por el contador y saldos abiertos por cliente, que sustituyen los saldos heredados de la carga histórica."),
 ("3.3.1","Contabilidad","Cobranza y bancos","Pagos","Datos",14,"Hito 3",
  "Cancelación de los cobros registrados sin respaldo, depuración de los cobros de más, de los pagos sin asiento y de los saldos a favor, y reaplicación de los pagos a sus facturas."),
 ("3.3.2","Contabilidad","Cobranza y bancos","Extractos bancarios","Datos",2,"Hito 4",
  "Importación por archivo de los extractos del periodo de cada cuenta bancaria."),
 ("3.3.3","Contabilidad","Cobranza y bancos","Modelos de conciliación","Configuración",1.5,"Hito 4",
  "Reglas de conciliación automática para cobros, comisiones y movimientos recurrentes."),
 ("3.3.4","Contabilidad","Cobranza y bancos","Conciliación bancaria","Datos",15,"Hito 4",
  "Conciliación de los movimientos bancarios del periodo contra facturas y pagos, con las partidas sin identificar documentadas para el contador."),
 ("3.4.1","Contabilidad","Comprobantes fiscales","Regularización de movimientos contables contra CFDI del SAT","Datos",14,"Hito 5",
  "Cruce de los comprobantes emitidos y recibidos en el SAT contra lo registrado en Odoo, registro de las facturas de gastos faltantes, emisión de los complementos de pago de las facturas cobradas, y forma de pago y datos fiscales de los contactos."),
 ("4.1.1","Capacitación y cierre","Capacitación","Material de soporte","Entregable",1.5,"Hito 6",
  "Guía de operación por tema y fichas de consulta rápida que acompañan las grabaciones."),
 ("4.1.2","Capacitación y cierre","Capacitación","Sesiones teóricas y prácticas","Capacitación",6,"Hito 6",
  "Por tema, una sesión teórica y una práctica de una hora cada una, grabadas."),
 ("4.2.1","Capacitación y cierre","Cierre de alcance","Fechas de bloqueo y aceptación","Aceptación",3,"Hito 6",
  "Bloqueo de los periodos cerrados, revisión del primer cierre mensual y acta de aceptación."),
]

INVENTARIO = [
 ("1.1.1","Descubrimiento","Levantamiento operativo","Levantamiento de inventario","Levantamiento",1.5,"Hito 1",
  "Ubicaciones, conteos y unidades de venta por peso y, con el contador de la empresa, método de costeo y valoración."),
 ("1.1.2","Descubrimiento","Levantamiento operativo","Levantamiento de compras y ventas","Levantamiento",1.5,"Hito 1",
  "Proveedores, recepción, facturas, costes en destino, pedido, entrega, facturación global y devoluciones."),
 ("1.1.3","Descubrimiento","Levantamiento operativo","Flujo objetivo y criterios de configuración","Entregable",1.5,"Hito 1",
  "Diagrama del proceso de compra, recepción, venta, entrega y ajuste con el documento de Odoo que afecta cada paso, y criterios firmados antes de configurar."),
 ("2.1.1","Configuración general","Categorías y productos","Categorías de producto","Configuración",1.5,"Hito 2",
  "Método de costeo, valoración y cuentas contables de cada categoría, y retiro de las categorías de prueba o sin uso."),
 ("2.1.2","Configuración general","Categorías y productos","Productos","Datos",4,"Hito 2",
  "Depuración por plantilla de categoría asignada, tipo de producto, precios y costos atípicos y productos duplicados."),
 ("2.2.1","Configuración general","Unidades de medida","Unidades de medida","Configuración",1,"Hito 2",
  "Unificación de las unidades duplicadas y restitución de las unidades originales de Odoo con sus factores."),
 ("3.1.1","Inventario","Configuración general","Ubicaciones y rutas","Configuración",3,"Hito 3",
  "Restitución de la ubicación de existencias, reglas de abastecimiento y ubicaciones de ajuste duplicadas."),
 ("3.1.2","Inventario","Configuración general","Lotes y fechas de caducidad","Configuración",3,"Hito 3",
  "Seguimiento por lote en los productos perecederos, días de caducidad, de consumo preferente y de alerta por categoría, y salida por fecha de caducidad en el almacén."),
 ("3.1.3","Inventario","Configuración general","Costes en destino","Datos",1.5,"Hito 3",
  "Cuenta de los productos de coste en destino y corrección de los costes repetidos o sin asiento."),
 ("3.2.1","Inventario","Existencias y valoración","Regularización de existencias","Datos",8,"Hito 3",
  "Hojas de conteo, aplicación del conteo físico, corrección de existencias negativas y de productos archivados con existencia, y cierre de movimientos pendientes."),
 ("3.2.2","Inventario","Existencias y valoración","Valoración de inventario","Datos",8,"Hito 5",
  "Revaluación de las entradas registradas sin costo o con costo atípico y asiento de los ajustes de inventario que no lo generaron."),
 ("3.2.3","Inventario","Existencias y valoración","Cierre de valoración","Entregable",6.5,"Hito 6",
  "Cruce por producto de la valoración contra la cuenta de inventario y pólizas propuestas para el cuadre."),
 ("4.1.1","Compras","Regularización","Regularización de históricos de compras","Datos",16,"Hito 4",
  "Revisión de órdenes de compra, recepciones y facturas del periodo, registro de las facturas de adquisición de mercancías desde su orden con la carga del XML y cierre de las órdenes históricas."),
 ("4.1.2","Compras","Regularización","Control de facturas","Configuración",3.5,"Hito 4",
  "Diferencias de precio y cantidad entre lo recibido y lo facturado, y política de facturación sobre cantidades recibidas."),
 ("5.1.1","Ventas","Regularización","Regularización de históricos de ventas","Datos",13.5,"Hito 5",
  "Revisión de pedidos, entregas y facturas, corrección del costo registrado de más o faltante, timbrado o cancelación de las facturas sin folio fiscal o con más de un comprobante vigente, y estado de facturación de los pedidos."),
 ("5.1.2","Ventas","Regularización","Política de facturación","Configuración",1,"Hito 5",
  "Facturación sobre lo entregado y vínculo de la facturación global con sus pedidos."),
 ("6.1.1","Capacitación y cierre","Capacitación","Material de soporte","Entregable",1.5,"Hito 6",
  "Guía de operación por tema y fichas de consulta rápida que acompañan las grabaciones."),
 ("6.1.2","Capacitación y cierre","Capacitación","Sesiones teóricas y prácticas","Capacitación",6,"Hito 6",
  "Por tema, una sesión teórica y una práctica de una hora cada una, grabadas."),
 ("6.2.1","Capacitación y cierre","Cierre de alcance","Aceptación y cierre de alcance","Aceptación",2.5,"Hito 6",
  "Revisión del primer cierre mensual con el cuadre de inventario y acta de aceptación."),
]

HITOS = {
 "contabilidad": {
  "Hito 1": "Descubrimiento y seguridad",
  "Hito 2": "Catálogo, impuestos y saldos iniciales",
  "Hito 3": "Pagos",
  "Hito 4": "Extractos y conciliación bancaria",
  "Hito 5": "Regularización contra CFDI del SAT",
  "Hito 6": "Capacitación y cierre",
 },
 "inventario": {
  "Hito 1": "Descubrimiento y criterios",
  "Hito 2": "Categorías, productos y unidades de medida",
  "Hito 3": "Ubicaciones, costes en destino y regularización",
  "Hito 4": "Históricos de compras",
  "Hito 5": "Históricos de ventas y valoración",
  "Hito 6": "Cierre de valoración, capacitación y cierre",
 },
 "integral": {
  "Hito 1": "Descubrimiento y seguridad",
  "Hito 2": "Catálogo, apertura, productos y unidades",
  "Hito 3": "Pagos, ubicaciones y regularización de existencias",
  "Hito 4": "Conciliación bancaria e históricos de compras",
  "Hito 5": "CFDI del SAT, históricos de ventas y valoración",
  "Hito 6": "Cierre de valoración, capacitación y cierre",
 },
}

PROYECTO = {"contabilidad": "Contabilidad, cobranza y conciliación",
            "inventario": "Inventario, compras, ventas y valoración"}

# Tasks shared by both projects: when contracted together they are done once (integral hours).
COMUNES = {"Flujo objetivo y criterios de configuración": 3, "Material de soporte": 3,
           "Sesiones teóricas y prácticas": 12, "Fechas de bloqueo y aceptación": 5.5}
ALIAS = {"Aceptación y cierre de alcance": "Fechas de bloqueo y aceptación"}


def integral():
    """Integral route: accounting then inventory, shared tasks merged once, renumbered by application."""
    filas, vistas = [], set()
    orden = ["Descubrimiento", "Configuración general", "Contabilidad", "Inventario", "Compras", "Ventas",
             "Capacitación y cierre"]
    fuente = [("Contabilidad", x) for x in CONTABILIDAD] + [("Inventario", x) for x in INVENTARIO]
    for app in orden:
        grupos = []
        for proy, x in fuente:
            if x[1] != app:
                continue
            t = ALIAS.get(x[3], x[3])
            if t in COMUNES:
                if t in vistas:
                    continue
                vistas.add(t); proy = "Común"; x = x[:5] + (COMUNES[t],) + x[6:]
            grupos.append((proy, x))
        gord = []
        for proy, x in grupos:
            if x[2] not in gord: gord.append(x[2])
        grupos.sort(key=lambda px: gord.index(px[1][2]))
        # renumber: application index, task group index, subtask index
        ai = orden.index(app) + 1
        gidx = {}
        for proy, x in grupos:
            g = x[2]
            if g not in gidx: gidx[g] = [len(gidx) + 1, 0]
            gidx[g][1] += 1
            num = "%d.%d.%d" % (ai, gidx[g][0], gidx[g][1])
            filas.append((num,) + x[1:] + (proy,))
    return filas


def ruta(key):
    if key == "contabilidad": return [x + ("Contabilidad",) for x in CONTABILIDAD]
    if key == "inventario": return [x + ("Inventario",) for x in INVENTARIO]
    return integral()


def r2(x): return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

PAGOS_B = {"contabilidad": 2, "inventario": 2, "integral": 4}
PLAZO = {"contabilidad": "entre 2 y 3 meses", "inventario": "entre 2 y 3 meses", "integral": "entre 3 y 4 meses"}


def cifras(key):
    R = ruta(key)
    apps, hitos, tipos, proys = {}, {}, {}, {}
    for n, a, g, t, tw, h, hi, d, pr in R:
        apps[a] = apps.get(a, 0) + h; tipos[tw] = tipos.get(tw, 0) + h
        hitos[hi] = hitos.get(hi, 0) + h; proys[pr] = proys.get(pr, 0) + h
    hitos = {k: hitos[k] for k in sorted(hitos, key=lambda s: int(s.split()[1]))}
    P = PARAMS; tot = sum(apps.values()); pref, lista = P["tarifa_pref"], P["tarifa_lista"]
    c = {"apps": apps, "hitos": hitos, "tipos": tipos, "proys": proys, "tot": tot, "n": len(R),
         "pagos_b": PAGOS_B[key], "plazo": PLAZO[key]}
    imp = tot * pref
    c.update(p=imp, l=tot * lista, benef=tot * lista - imp, ant=r2(imp * P["anticipo"]),
             b=r2(imp / PAGOS_B[key]), desc=r2(imp * P["descuento_unico"]))
    c["c"] = r2(imp - c["desc"]); c["tarifa_c"] = r2(pref * (1 - P["descuento_unico"]))
    ks = list(hitos); saldo = {k: r2(hitos[k] * pref * (1 - P["anticipo"])) for k in ks}
    saldo[ks[-1]] = r2(imp - c["ant"] - sum(saldo[k] for k in ks[:-1]))  # last milestone absorbs rounding
    c["hito_saldo"] = saldo
    return c

# Internal only: contingency reserve, never shown to the client.
CONTINGENCIA_INTERNA = {"contabilidad": {"3.3.1": 2, "3.3.4": 3, "3.4.1": 2},
                        "inventario": {"4.1.1": 3, "5.1.1": 2, "3.2.3": 2}}

if __name__ == "__main__":
    for k in ("contabilidad", "inventario", "integral"):
        C = cifras(k)
        print(k, C["tot"], C["n"], C["hitos"], C["proys"], C["p"], C["l"], C["ant"], C["b"], C["c"])
        print("  ", C["hito_saldo"])
    for x in integral(): print(x[0], x[1], x[3], x[5], x[6], x[8])

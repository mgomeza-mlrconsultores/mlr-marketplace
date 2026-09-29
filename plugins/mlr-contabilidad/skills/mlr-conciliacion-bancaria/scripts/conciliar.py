# -*- coding: utf-8 -*-
"""Matching engine: bank statement x Odoo ledger x CFDI -> conciliacion.json (what fills the workbook).

    python3 conciliar.py <params.json> <banco.json> <odoo.json> <cfdi.json> <salida/conciliacion.json>
           [--decisiones decisiones.json] [--lista-69b lista.csv]

Two levels of matching, each documented in references/reglas-emparejamiento.md:
  1. Bank <-> Odoo: same signed amount, date inside the window, compatible text. One to one.
  2. Movement <-> CFDI, rules E01..E11 in order of confidence. A rule proposes a link; nothing is
     written to Odoo from here. Ties (E11) are never resolved alone.

decisiones.json keeps what the user already decided (a forced link, an accepted explanation), so a
new run after corrections in Odoo reproduces those decisions instead of asking again:
  {"enlaces": {"B-027": [{"uuid": "...", "importe": 11200.0}]}, "aceptados": {"B-069": "Pago registrado con fecha de la factura"}}

Every observation uses the fixed phrases the workbook formulas count (Alerta, PUE, omitida, COMISIONES).
"""
import argparse
import collections
import datetime
import itertools
import json
import re
import unicodedata

UUID_RE = re.compile(r"[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}", re.I)
SUFIJOS = r"\b(S\.?\s?A\.?\s?P\.?\s?I\.?|S\.?\s?A\.?\s?B\.?|S\.?\s?A\.?|S\.?\s?DE\s?R\.?\s?L\.?|DE\s?C\.?\s?V\.?|S\.?\s?C\.?|A\.?\s?C\.?|SOCIEDAD ANONIMA|CAPITAL VARIABLE)\b"

# bank codes that never need an individual CFDI (see references/codigos-banco.md)
NO_REQUIERE = {
    "V43": "Comisión bancaria", "V46": "Comisión bancaria", "S39": "Comisión bancaria",
    "V44": "IVA de comisión bancaria", "V47": "IVA de comisión bancaria", "S40": "IVA de comisión bancaria",
    "P14": "Pago de impuestos",
}
TERMINAL_VENTA = {"V42", "V45"}
# engine rule -> rule of the approval catalog (11_Catalogos, R01..R14) used in the Acciones sheet
RMAP = {"D": "R01", "E01": "R01", "E02": "R02", "E03": "R03", "E04": "R04", "E05": "R05", "E08": "R06", "E07": "R09",
        "E10": "R13", "E11": "R14", "E12": "R12"}
FORMAS_TARJETA = {"04", "28"}
KW = {"Arrendamiento": ["renta", "arrend", "alquiler"],
      "Fletes": ["flete", "autotransporte", "transporte de carga", "maniobra"],
      "Comisiones": ["comision"],
      "Honorarios": ["honorario", "servicios profesionales", "consultoria", "asesoria", "contable", "juridic", "auditoria"]}


def norm(t):
    t = unicodedata.normalize("NFKD", str(t or "")).encode("ascii", "ignore").decode().upper()
    t = re.sub(SUFIJOS, " ", t)
    return " ".join(re.sub(r"[^A-Z0-9 ]+", " ", t).split())


def d(s):
    return datetime.date.fromisoformat(str(s)[:10]) if s else None


def dias(a, b):
    return (d(a) - d(b)).days if a and b else None


def money(x):
    return "{:,.2f}".format(x)


def tokens(t):
    return {w for w in norm(t).split() if len(w) >= 4}


class Motor(object):
    def __init__(self, P, banco, odoo, cfdi, decisiones=None, lista69b=None):
        self.P, self.banco, self.odoo = P, banco, odoo
        self.cf = cfdi["cfdi"]
        self.rep_por_factura = cfdi.get("indices", {}).get("rep_por_factura", {})
        self.tol_imp = float(P.get("tolerancia_importe", 1.0))
        self.tol_dias = int(P.get("tolerancia_dias", 3))
        self.ventana = int(P.get("ventana_busqueda_dias", 45))
        self.dec = decisiones or {"enlaces": {}, "aceptados": {}}
        self.l69 = lista69b or set()
        self.rfc_empresa = (P.get("rfc_empresa") or odoo["compania"].get("rfc") or "").upper()
        self.es_moral = len(self.rfc_empresa) == 12
        self.aplicado = collections.defaultdict(float)     # uuid -> applied in this run
        self.aplicado_en = collections.defaultdict(list)   # uuid -> partidas
        self.facturas = {int(k): v for k, v in odoo["facturas"].items()}
        self.fact_por_uuid = {f["uuid"]: f for f in self.facturas.values() if f.get("uuid")}
        self.caja = odoo["diario"]["tipo"] == "cash"
        self.moneda = (odoo["diario"].get("moneda") or "MXN").upper()
        self.sl_pend = {x["id"] for x in odoo.get("lineas_extracto_sin_conciliar", [])}
        self.sin_cfdi = P.get("cuentas_sin_cfdi", {})       # account code prefix -> reason (partners' loans, own transfers...)
        # remaining balance at the start of the period, from Odoo: residual now + what the period's lines settled
        ligado = collections.defaultdict(float)
        for a in odoo["auxiliar"]:
            for f in a.get("facturas", []):
                ligado[f["id"]] += f["importe"]
        self.inicio = {}
        for f in self.facturas.values():
            if f.get("uuid") and f.get("pendiente") is not None and f["estado"] == "posted":
                self.inicio[f["uuid"]] = round(f["pendiente"] + ligado.get(f["id"], 0.0), 2)

    # ------------------------------------------------------------------ level 1
    def banco_vs_odoo(self):
        movs, aux = self.banco["movimientos"], self.odoo["auxiliar"]
        cand = []
        for i, m in enumerate(movs):
            a = round((m["abono"] or 0) - (m["cargo"] or 0), 2)
            tb = tokens(m["descripcion"]) | ({m["referencia"]} if m.get("referencia") else set())
            for j, o in enumerate(aux):
                b = round((o["abono"] or 0) - (o["cargo"] or 0), 2)
                if abs(a - b) > 0.005:
                    continue
                dd = abs(dias(o["fecha"], m["fecha"]) or 0)
                if dd > max(self.tol_dias * 3, 10):
                    continue
                texto = len(tb & (tokens(o["concepto"]) | {o["concepto"]}))
                ref = 1 if m.get("referencia") and m["referencia"] in o["concepto"] else 0
                cand.append((-(ref * 10 + texto), dd, i, j))
        cand.sort()
        usado_b, usado_o, par = set(), set(), {}
        for _, _, i, j in cand:
            if i in usado_b or j in usado_o:
                continue
            usado_b.add(i)
            usado_o.add(j)
            par[i] = j
        self.par = par
        self.odoo_solo = [j for j in range(len(aux)) if j not in usado_o]

    # ------------------------------------------------------------------ helpers level 2
    def pool(self, tipo):
        direccion = "emitido" if tipo == "Cobro" else "recibido"
        return [c for c in self.cf.values() if c.get("direccion") == direccion and c.get("tipo") in ("I", "E")]

    def en_diario(self, c, monto):
        """CFDI amount in the journal's currency; None when it cannot be converted (MXN CFDI in a USD journal)."""
        mc = (c.get("moneda") or "MXN").upper()
        if mc in (self.moneda, "XXX"):
            return monto
        if self.moneda == "MXN":
            return round(monto * (c.get("tipo_cambio") or 1.0), 2)
        return None

    def total_md(self, c):
        return self.en_diario(c, c.get("total") or 0.0)

    def restante(self, c):
        t = self.total_md(c)
        if t is None:
            return 0.0
        r = t - self.aplicado[c["uuid"]]
        ini = self.inicio.get(c["uuid"])
        if ini is not None and (c.get("moneda") or "MXN").upper() == self.moneda:
            r = min(r, ini - self.aplicado[c["uuid"]])   # invoices already paid before the period drop out
        return round(r, 2)

    def cerca(self, fb, c, tope):
        dd = dias(fb, c.get("fecha_pago_real") or c.get("fecha"))
        return dd is not None and abs(dd) <= tope

    def contraparte(self, c, tipo):
        return (c.get("nombre_receptor"), c.get("rfc_receptor")) if tipo == "Cobro" else (c.get("nombre_emisor"), c.get("rfc_emisor"))

    def vigente(self, c):
        return "cancel" not in norm(c.get("estado_sat")).lower()

    def subconjunto(self, objetivo, cands, max_n=6):
        """Bounded subset sum: combinations of up to max_n invoices whose remaining equals the amount."""
        cands = sorted(cands, key=lambda c: -self.restante(c))[:20]
        sols = []
        for n in range(2, min(max_n, len(cands)) + 1):
            for combo in itertools.combinations(cands, n):
                if abs(sum(self.restante(c) for c in combo) - objetivo) <= 0.005:
                    sols.append(combo)
                    if len(sols) > 1:
                        return sols
        return sols

    # ------------------------------------------------------------------ level 2
    def enlaza(self, m, o, tipo):
        """Return (enlace, [(cfdi, aplicado)], observaciones, regla)."""
        imp = round((m["abono"] or 0) + (m["cargo"] or 0), 2) if m else round((o["abono"] or 0) + (o["cargo"] or 0), 2)
        codigo = (m or {}).get("codigo", "")
        texto = " ".join(filter(None, [(m or {}).get("descripcion"), (o or {}).get("concepto")]))
        contacto = ((o or {}).get("contacto") or "").strip()
        partida = (m or {}).get("partida") or ("SB-" + o["renglon"])
        # forced decisions first
        if partida in self.dec.get("enlaces", {}):
            out = [(self.cf[e["uuid"]], e["importe"]) for e in self.dec["enlaces"][partida] if e["uuid"] in self.cf]
            if out:
                return self._clasifica(out, imp), out, ["Enlace confirmado por el usuario"], "D"
        if partida in self.dec.get("no_requiere", {}):
            return "No requiere CFDI", [], ["No requiere CFDI individual", "Criterio del usuario: %s" % self.dec["no_requiere"][partida]], "D"
        # E07 no individual CFDI needed, by bank code or by the Odoo counterpart
        cps = (o or {}).get("contrapartes") or []
        for cp in cps:
            for pref, motivo in self.sin_cfdi.items():
                if str(cp.get("codigo") or "").startswith(pref):
                    return "No requiere CFDI", [], ["No requiere CFDI individual", "%s (cuenta %s)" % (motivo, cp["codigo"])], "E07"
        if cps and all(cp.get("tipo") in ("asset_cash", "liability_credit_card") for cp in cps):
            return "No requiere CFDI", [], ["No requiere CFDI individual", "Traspaso entre cuentas propias (%s)" % ", ".join(cp["codigo"] for cp in cps)], "E12"
        if codigo in NO_REQUIERE:
            obs = {"Comisión bancaria": "Comisión bancaria: la ampara el CFDI mensual del banco",
                   "IVA de comisión bancaria": "IVA de comisión bancaria: lo ampara el CFDI mensual del banco",
                   "Pago de impuestos": "Pago de impuestos: se ampara con la declaración y su línea de captura"}[NO_REQUIERE[codigo]]
            if NO_REQUIERE[codigo] != "Pago de impuestos" and not self.P.get("banco_emite_cfdi_comisiones", True):
                obs = obs.split(":")[0] + ": sin CFDI del banco, el IVA no es acreditable (criterio por confirmar)"
            return "No requiere CFDI", [], ["No requiere CFDI individual", obs], "E07"
        if "NOMINA" in norm(contacto) or "NOMINA" in norm(texto).split():
            return "No requiere CFDI", [], ["No requiere CFDI individual", "Nómina: se ampara con los CFDI de nómina, fuera de este control"], "E07"
        if imp < 1.0 and tipo == "Cobro":
            return "No requiere CFDI", [], ["No requiere CFDI individual", "Depósito de validación de cuenta (%s)" % money(imp)], "E07"
        pool = [c for c in self.pool(tipo)]
        # E01 invoices settled by the Odoo line, or UUID / serie-folio in the text
        if o and o.get("facturas"):
            out = []
            for f in o["facturas"]:
                fac = self.facturas.get(f["id"])
                if fac and fac.get("uuid") in self.cf:
                    out.append((self.cf[fac["uuid"]], f["importe"]))
            if out:
                resto = round(imp - sum(a for _, a in out), 2)
                if codigo in TERMINAL_VENTA and resto > self.tol_imp:
                    ya = {c["uuid"] for c, _ in out}
                    extra = self.lote(resto, [c for c in pool if c["uuid"] not in ya], (m or o)["fecha"])
                    if extra:
                        out += extra
                        return "Varios CFDI", out, ["Lote de terminal: además de lo ligado en Odoo, %d cobros con tarjeta de la misma fecha" % len(extra)], "E08"
                return self._clasifica(out, imp), out, [], "E01"
        uu = [u.upper() for u in UUID_RE.findall(texto)]
        hits = [self.cf[u] for u in uu if u in self.cf]
        if not hits:
            nt = norm(texto).replace(" ", "")
            hits = [c for c in pool if c.get("folio") and len(str(c["folio"])) >= 3 and
                    (str(c.get("serie", "")) + str(c["folio"])).upper() in nt and self.restante(c) > 0]
        if len(hits) == 1:
            return self._uno(hits[0], imp, "E01")
        # E02 RFC in the bank text, same amount
        rfc = (m or {}).get("rfc") or ""
        if rfc:
            c2 = [c for c in pool if self.contraparte(c, tipo)[1] == rfc and abs(self.restante(c) - imp) <= self.tol_imp and self.vigente(c)]
            if len(c2) == 1:
                return self._uno(c2[0], imp, "E02")
            if len(c2) > 1:
                return self._empate(c2)
        nombre = norm(contacto)
        mismos = [c for c in pool if nombre and norm(self.contraparte(c, tipo)[0]) == nombre and self.vigente(c) and self.restante(c) > 0.005]
        fb = (m or o)["fecha"]
        # E03 exact amount, same contact, date inside the window
        c3 = [c for c in mismos if abs(self.restante(c) - imp) <= 0.005 and self.cerca(fb, c, self.ventana)]
        if len(c3) == 1:
            return self._uno(c3[0], imp, "E03")
        if len(c3) > 1:
            return self._empate(c3)
        # E08 card terminal batch: gross deposit settles invoices of several customers paid by card
        if codigo in TERMINAL_VENTA:
            out = self.lote(imp, pool, fb)
            if len(out) == 1:
                return self._uno(out[0][0], imp, "E08")
            if out:
                return "Varios CFDI", out, ["Lote de terminal: %d cobros con tarjeta de la misma fecha" % len(out)], "E08"
        # E04 one movement, several invoices of the same contact
        sols = self.subconjunto(imp, mismos)
        if len(sols) == 1:
            out = [(c, self.restante(c)) for c in sols[0]]
            return "Varios CFDI", out, [], "E04"
        # E05 partial payment of a single open invoice of the same contact
        mayores = [c for c in mismos if self.restante(c) > imp + self.tol_imp]
        if len(mayores) == 1:
            return self._uno(mayores[0], imp, "E05")
        # E10 nothing matched
        obs = ["Ningún CFDI vigente del mes coincide con este movimiento"]
        obs.append("contacto en Odoo: %s" % contacto.strip() if contacto.strip() else "sin contacto en Odoo")
        if contacto.strip() and tipo == "Pago" and not self.facturas_de_contacto(contacto):
            obs.append('Alerta: pago a "%s" sin comprobante' % contacto.strip())
        return "Sin CFDI", [], obs, "E10"

    def lote(self, objetivo, pool, fb):
        """Card terminal: one invoice or a unique combination of card-paid invoices that adds up to the amount."""
        tarj = [c for c in pool if c.get("forma_pago") in FORMAS_TARJETA and self.vigente(c) and self.restante(c) > 0.005
                and self.cerca(fb, c, self.tol_dias)]
        exacto = [c for c in tarj if abs(self.restante(c) - objetivo) <= 0.005]
        if len(exacto) == 1:
            return [(exacto[0], self.restante(exacto[0]))]
        sols = self.subconjunto(objetivo, tarj)
        return [(c, self.restante(c)) for c in sols[0]] if len(sols) == 1 else []

    def facturas_de_contacto(self, contacto):
        n = norm(contacto)
        return [f for f in self.facturas.values() if norm(f["partner"]) == n]

    def _empate(self, cs):
        return "Sin CFDI", [], ["Empate: %d CFDI con mismo importe y contacto (%s); se resuelve con folio u hora de timbrado, no se asigna solo"
                                % (len(cs), ", ".join(str(c.get("serie", "")) + str(c.get("folio", "")) for c in cs[:4]))], "E11"

    def _uno(self, c, imp, regla):
        rest = self.restante(c)
        apl = round(min(imp, rest), 2) if rest > 0 else imp
        return self._clasifica([(c, apl)], imp), [(c, apl)], [], regla

    def _clasifica(self, out, imp):
        if len(out) > 1:
            return "Varios CFDI"
        c, apl = out[0]
        if c.get("metodo_pago") == "PPD" and self.rep_por_factura.get(c["uuid"]):
            return "REP"
        if apl + self.tol_imp < (self.total_md(c) or 0):
            return "Parcial"
        return "1 a 1"

    # ------------------------------------------------------------------ fiscal classification
    def tipo_retencion(self, c, tipo):
        txt = norm(c.get("conceptos", "")).lower()
        reg = c.get("regimen_emisor") if tipo == "Pago" else c.get("regimen_receptor")
        kw = next((k for k, ws in KW.items() if any(w in txt for w in ws)), None)
        if (c.get("isr_ret") or 0) > 0 or (c.get("iva_ret") or 0) > 0:
            if reg == "626":
                return {"Arrendamiento": "RESICO arrendamiento", "Honorarios": "RESICO honorarios"}.get(kw, "RESICO actividad empresarial")
            return kw or "Otra retención"
        return "Sin retención"

    def alertas(self, c, apl, tipo, fb, partida):
        out = []
        verbo = "cobrada" if tipo == "Cobro" else "pagada"
        if c.get("metodo_pago") == "PUE" and c.get("fecha") and d(c["fecha"]).month != d(fb).month:
            out.append("Alerta: PUE %s en un mes distinto al de emisión: revisa el método de pago" % verbo)
        if c.get("metodo_pago") == "PUE" and (apl + self.tol_imp < (self.total_md(c) or 0) or len(self.aplicado_en[c["uuid"]]) > 1):
            out.append("Alerta: PUE %s en parcialidades" % verbo)
        if c.get("metodo_pago") == "PUE" and c.get("forma_pago") == "99":
            out.append("Alerta: PUE con forma de pago 99 (por definir)")
        if c.get("metodo_pago") == "PPD" and not self.rep_por_factura.get(c["uuid"]):
            out.append("Alerta: PPD %s sin complemento de pago en las exportaciones (el emisor tiene hasta el día 5 del mes siguiente)" % verbo)
        if not self.vigente(c):
            out.append("Alerta: CFDI cancelado ante el SAT")
        rfc_cp = self.contraparte(c, tipo)[1] or ""
        if rfc_cp and rfc_cp.upper() in self.l69:
            out.append("Alerta: RFC %s en la lista 69-B del SAT" % rfc_cp)
        if tipo == "Pago" and self.es_moral and len(rfc_cp) == 13 and not (c.get("isr_ret") or c.get("iva_ret")):
            txt = norm(c.get("conceptos", "")).lower()
            if c.get("regimen_emisor") == "626" or any(w in txt for w in KW["Honorarios"] + KW["Arrendamiento"] + KW["Fletes"]):
                out.append("Alerta: posible retención omitida")
        if tipo == "Pago" and self.caja and apl > 2000:
            out.append("Alerta: pago en efectivo mayor a 2,000 pesos (art. 27 fr. III LISR)")
        if self.aplicado[c["uuid"]] > (self.total_md(c) or 0) + self.tol_imp and len(self.aplicado_en[c["uuid"]]) > 1:
            out.append("Alerta: posible pago duplicado: el CFDI también se aplicó en %s" % ", ".join(p for p in self.aplicado_en[c["uuid"]] if p != partida))
        return out

    # ------------------------------------------------------------------ build rows
    def filas(self):
        self.banco_vs_odoo()
        movs, aux = self.banco["movimientos"], self.odoo["auxiliar"]
        grupos = [(m, aux[self.par[i]] if i in self.par else None) for i, m in enumerate(movs)]
        grupos += [(None, aux[j]) for j in self.odoo_solo]
        # E01 links first so that later rules see the right remaining balances
        orden = sorted(range(len(grupos)), key=lambda k: 0 if grupos[k][1] and grupos[k][1].get("facturas") else 1)
        res = {}
        for k in orden:
            m, o = grupos[k]
            tipo = "Cobro" if ((m or o)["abono"] or 0) > 0 else "Pago"
            enlace, out, obs, regla = self.enlaza(m, o, tipo)
            partida = m["partida"] if m else "SB-" + o["renglon"]
            for c, apl in out:
                self.aplicado[c["uuid"]] = round(self.aplicado[c["uuid"]] + apl, 2)
                self.aplicado_en[c["uuid"]].append(partida)
            res[k] = (tipo, enlace, out, obs, regla, partida)
        filas = []
        self.corrido = collections.defaultdict(float)  # applied so far, in bank order, for the "quedan X" phrase
        for k, (m, o) in enumerate(grupos):
            tipo, enlace, out, obs, regla, partida = res[k]
            fb = (m or o)["fecha"]
            imp = round(((m or o)["abono"] or 0) + ((m or o)["cargo"] or 0), 2)
            base = {"partida": partida, "fecha_banco": m["fecha"] if m else None, "concepto_banco": m["descripcion"] if m else "",
                    "cargo_banco": m["cargo"] if m else None, "abono_banco": m["abono"] if m else None,
                    "renglon_odoo": o["renglon"] if o else "", "statement_line_id": (o or {}).get("statement_line_id"), "fecha_odoo": o["fecha"] if o else None, "asiento": o["asiento"] if o else "",
                    "contacto": (o["contacto"] or "").strip() if o else "", "cargo_odoo": o["cargo"] if o else None, "abono_odoo": o["abono"] if o else None,
                    "enlace": enlace, "tipo": tipo, "primera": 1, "regla": regla, "codigo": (m or {}).get("codigo", "")}
            if o and o.get("statement_line_id") in self.sl_pend:
                obs = obs + ["Alerta: la línea de extracto sigue en la cuenta de suspenso en Odoo"]
            if not o:
                obs = obs + ["Está en el banco y no en Odoo"]
            if not m:
                obs = obs + ["Está en Odoo y no en el banco"]
            aceptado = self.dec.get("aceptados", {}).get(partida)
            if not out:
                f = dict(base, aplicado=imp, observacion=self._frase(obs, aceptado), dias_pago=None)
                filas.append(f)
                continue
            for n, (c, apl) in enumerate(out):
                mx = (c.get("tipo_cambio") or 1.0) if (c.get("moneda") or "MXN") != "MXN" else 1.0
                nombre, rfc = self.contraparte(c, tipo)
                pago = self._fecha_pago(c, apl) if enlace in ("1 a 1", "REP") else None
                self.corrido[c["uuid"]] = round(self.corrido[c["uuid"]] + apl, 2)
                o_extra = list(obs)
                if n == 0:
                    o_extra = self._informativas(c, apl, imp, fb, pago, enlace) + o_extra
                o_extra += self.alertas(c, apl, tipo, fb, partida)
                f = dict(base) if n == 0 else {"partida": partida, "fecha_banco": base["fecha_banco"], "concepto_banco": base["concepto_banco"],
                                               "enlace": enlace, "tipo": tipo, "primera": 0, "regla": regla}
                f.update({"uuid": c["uuid"], "folio": (str(c.get("serie") or "") + str(c.get("folio") or "")) or "",
                          "fecha_cfdi": c.get("fecha"), "contraparte": nombre, "rfc": rfc, "metodo": c.get("metodo_pago"),
                          "tipo_ret": self.tipo_retencion(c, tipo), "total_cfdi": self.total_md(c), "aplicado": apl,
                          "dias_pago": dias(pago, fb) if pago else 0,
                          "base_cfdi": round(((c.get("subtotal") or 0) - (c.get("descuento") or 0)) * mx, 2), "iva_cfdi": round((c.get("iva") or 0) * mx, 2),
                          "ivaret_cfdi": round((c.get("iva_ret") or 0) * mx, 2), "isrret_cfdi": round((c.get("isr_ret") or 0) * mx, 2),
                          "observacion": self._frase(o_extra, aceptado)})
                filas.append(f)
        for f in filas:
            f.setdefault("aplicado", 0.0)
        self._estatus(filas)
        return filas

    def _fecha_pago(self, c, apl):
        reps = self.rep_por_factura.get(c["uuid"]) or []
        cerca = [r for r in reps if abs(r["imp_pagado"] - apl) <= self.tol_imp]
        if cerca:
            return cerca[0]["fecha"]
        return c.get("fecha_pago_real")

    def _informativas(self, c, apl, imp, fb, pago, enlace):
        out = []
        dd = abs(dias(pago, fb)) if pago else None
        if enlace == "REP":
            rep = (self.rep_por_factura.get(c["uuid"]) or [{}])[0]
            out.append("Pago de factura PPD amparado con el REP %s" % rep.get("rep", ""))
        elif enlace == "Parcial" or apl + self.tol_imp < (self.total_md(c) or 0):
            rest = round(min(self.total_md(c) or 0, self.inicio.get(c["uuid"], 10 ** 12)) - self.corrido[c["uuid"]], 2)
            if rest > self.tol_imp:
                out.append("Abono parcial: quedan %s por aplicar de esta factura" % money(rest))
        if imp - apl > self.tol_imp and enlace != "Varios CFDI":
            out.append("El movimiento es mayor que el saldo de la factura por %s" % money(imp - apl))
        if dd is not None and dd > self.tol_dias:
            out.append("Mismo importe, pero %d días de diferencia contra la fecha de pago registrada" % dd)
        elif not out:
            out.append("Mismo importe y fecha dentro de %d días" % self.tol_dias)
        return out

    @staticmethod
    def _frase(obs, aceptado):
        info = [o for o in obs if not o.startswith("Alerta")]
        al = [o[len("Alerta: "):] if i else o for i, o in enumerate(x for x in obs if x.startswith("Alerta"))]
        s = "; ".join(info).replace("No requiere CFDI individual; ", "No requiere CFDI individual. ")
        if al:
            s = (s + ". " if s else "") + "; ".join(al)
        if aceptado:
            s += ". Explicación aceptada por el usuario: %s" % aceptado
        return s.strip()

    def _estatus(self, filas):
        """Same logic as the Estatus formula of the workbook, to report in the chat before opening Excel."""
        grupos = collections.defaultdict(list)
        for f in filas:
            grupos[f["partida"]].append(f)
        for p, fs in grupos.items():
            banco = sum((f.get("cargo_banco") or 0) + (f.get("abono_banco") or 0) for f in fs)
            dif_l = sum(((f.get("cargo_banco") or 0) + (f.get("abono_banco") or 0)) - ((f.get("cargo_odoo") or 0) + (f.get("abono_odoo") or 0))
                        for f in fs if f.get("renglon_odoo") and f["primera"])
            dif_m = sum(dias(f.get("fecha_odoo"), f.get("fecha_banco")) or 0 for f in fs if f.get("renglon_odoo") and f["primera"] and f.get("fecha_banco"))
            exced = round(banco - sum(f["aplicado"] for f in fs), 2)
            for f in fs:
                if banco == 0 or not any(x.get("renglon_odoo") for x in fs) or f["enlace"] == "Sin CFDI":
                    e = "No identificado"
                elif abs(dif_l) > self.tol_imp or abs(dif_m) > self.tol_dias or abs(exced) > self.tol_imp or abs(f.get("dias_pago") or 0) > self.tol_dias:
                    e = "Conciliado (revisar)"
                elif f["enlace"] in ("Varios CFDI", "Parcial"):
                    e = "Conciliado (validar)"
                else:
                    e = "Conciliado"
                f["estatus"] = e
                f["excedente"] = exced if f["primera"] else 0.0

    # ------------------------------------------------------------------ other sheets
    def facturas_vs_odoo(self):
        desde, hasta = self.odoo["periodo"]["desde"], self.odoo["periodo"]["hasta"]
        por_num = {re.sub(r"[^A-Z0-9]", "", f["numero"].upper()): f for f in self.facturas.values()}
        usadas, filas = set(), []
        for c in sorted(self.cf.values(), key=lambda c: (c.get("direccion", ""), c.get("fecha") or "")):
            if c.get("tipo") not in ("I", "E") or not c.get("fecha") or not (desde <= c["fecha"] <= hasta):
                continue
            emitida = c["direccion"] == "emitido"
            f = self.fact_por_uuid.get(c["uuid"])
            if not f and emitida:
                f = por_num.get(re.sub(r"[^A-Z0-9]", "", (str(c.get("serie") or "") + str(c.get("folio") or "")).upper()))
            obs = []
            if f:
                usadas.add(f["id"])
                if f.get("uuid") and f["uuid"] != c["uuid"]:
                    obs.append("Odoo tiene otro folio fiscal: %s" % f["uuid"])
                if not f.get("uuid"):
                    obs.append("La factura en Odoo no tiene el XML ligado")
            else:
                obs.append("CFDI sin registro en Odoo: regístralo o liga el XML")
            filas.append({"tipo": "Emitida" if emitida else "Recibida", "numero": f["numero"] if f else "", "uuid": c["uuid"],
                          "fecha": c["fecha"], "contraparte": c.get("nombre_receptor") if emitida else c.get("nombre_emisor"),
                          "estado_sat": "Cancelado" if not self.vigente(c) else "Vigente", "total_cfdi": c.get("total"),
                          "estado_odoo": {"posted": "Registrado", "cancel": "Cancelado", "draft": "Borrador"}.get(f["estado"], f["estado"]) if f else "",
                          "total_odoo": f["total"] if f else None, "pendiente": f["pendiente"] if f else None, "observacion": "; ".join(obs)})
        for f in self.facturas.values():
            if f["del_mes"] and f["id"] not in usadas and f["estado"] != "draft":
                filas.append({"tipo": "Emitida" if f["tipo"].startswith("out") else "Recibida", "numero": f["numero"], "uuid": f.get("uuid") or "",
                              "fecha": f["fecha"], "contraparte": f["partner"], "estado_sat": "", "total_cfdi": None,
                              "estado_odoo": {"posted": "Registrado", "cancel": "Cancelado"}.get(f["estado"], f["estado"]),
                              "total_odoo": f["total"], "pendiente": f["pendiente"],
                              "observacion": "Factura en Odoo sin CFDI en las exportaciones del mes"})
        return filas

    def impuestos(self):
        saldos, detalle = [], []
        caja = set(self.odoo.get("diarios_caja") or [])
        for bloque in self.odoo.get("iva", []):
            tras = bloque["clave"] == "iva_trasladado_cobrado"
            s = -1 if tras else 1
            saldos.append({"cuenta": bloque["cuenta"], "nombre": bloque["nombre"], "saldo_inicial": s * bloque["saldo_inicial"],
                           "saldo_final": round(s * (bloque["saldo_inicial"] + bloque["movimiento"]), 2)})
            for x in bloque["detalle"]:
                obs = []
                if x["reversiones"]:
                    obs.append("%d reversión(es) de flujo: el pago se desconcilió y se volvió a conciliar en Odoo" % x["reversiones"])
                if any(j in caja for j in x["diarios"].split("/")):
                    obs.insert(0, "Pagada por caja (diario %s): no pasa por el banco" % "/".join(j for j in x["diarios"].split("/") if j in caja))
                if not x.get("uuid"):
                    obs.append("Sin folio fiscal en las exportaciones: factura de otro mes")
                detalle.append({"iva": "Trasladado" if tras else "Acreditable", "cuenta": bloque["cuenta"], "factura": x.get("numero", ""),
                                "contacto": x.get("partner", ""), "uuid": x.get("uuid") or "", "iva_odoo": round(s * x["iva"], 2),
                                "observacion": "; ".join(obs), "diario": x["diarios"]})
        return saldos, detalle

    def acciones(self, filas, fvo):
        """Proposals for the Acciones sheet. Rules are those of the approval catalog (R01..R14)."""
        modo = self.P.get("modo_diario", "sin_estado")
        acc, n = [], 0
        cuentas = self.P.get("cuentas", {})
        R = lambda e: RMAP.get(e, e)

        def nueva(**k):
            nonlocal n
            n += 1
            k.setdefault("aprobado", "")
            k.setdefault("estado", "Pendiente")
            acc.append(dict(id="A%03d" % n, **k))
        for h in self.odoo.get("hallazgos", []):
            nueva(tipo="Configuración", partida="", importe=None, concepto=h["hallazgo"], propuesta=h["propuesta"], regla="Diagnóstico",
                  confianza="Alta", operacion=None, evidencia=h["evidencia"])
        for f in filas:
            if not f["primera"]:
                continue
            imp = (f.get("cargo_banco") or 0) + (f.get("abono_banco") or 0)
            firmado = imp if f["tipo"] == "Cobro" else -imp
            fac = self.fact_por_uuid.get(f.get("uuid") or "")
            comision = f.get("codigo") in NO_REQUIERE and NO_REQUIERE[f["codigo"]] != "Pago de impuestos"
            cta_com = (cuentas.get("iva_comisiones") if "IVA" in NO_REQUIERE.get(f.get("codigo"), "") else cuentas.get("comisiones")) if comision else None
            # statement line still parked in suspense (mode con_estado): reconcile it, whatever the workbook status says
            if f.get("statement_line_id") in self.sl_pend:
                op, prop = None, "La línea de extracto sigue en suspenso: indica la contrapartida"
                if comision and cta_com:
                    op = {"op": "linea_extracto", "statement_line_id": f["statement_line_id"],
                          "contrapartidas": [{"cuenta": cta_com, "importe": imp, "nombre": f["concepto_banco"][:60]}]}
                    prop = "Conciliar la línea contra %s" % cta_com
                elif fac and fac["estado"] == "posted" and fac.get("partner_id"):
                    cta = cuentas.get("clientes") if f["tipo"] == "Cobro" else cuentas.get("proveedores")
                    if cta:
                        op = {"op": "linea_extracto", "statement_line_id": f["statement_line_id"],
                              "contrapartidas": [{"cuenta": cta, "importe": f["aplicado"], "partner_id": fac["partner_id"], "nombre": fac["numero"]}],
                              "conciliar_con_factura_id": fac["id"]}
                        prop = "Conciliar la línea contra la factura %s de %s" % (fac["numero"], fac["partner"])
                nueva(tipo="Línea de extracto", partida=f["partida"], importe=firmado, concepto=f["concepto_banco"],
                      documentos=fac["numero"] if fac else "", propuesta=prop, regla=R(f["regla"]), confianza="Alta" if op else "Baja", operacion=op)
                continue
            if f["estatus"] in ("Conciliado", "Conciliado (validar)"):
                continue
            if f["partida"].startswith("SB-"):
                nueva(tipo="Revisión", partida=f["partida"], importe=(f.get("abono_odoo") or 0) - (f.get("cargo_odoo") or 0),
                      concepto=f.get("asiento", ""), propuesta="Registro de Odoo sin movimiento en el banco: confirmar si es de otro periodo o si sobra",
                      regla="R13", confianza="Baja", operacion=None)
                continue
            if not f.get("renglon_odoo"):
                if comision:
                    op = None
                    if cta_com:
                        op = {"op": "asiento_manual", "diario_id": self.P.get("diario_id"), "fecha": f["fecha_banco"], "referencia": f["concepto_banco"][:60],
                              "lineas": [{"cuenta": cta_com, "debe": imp}, {"cuenta": self.odoo["diario"]["cuenta"], "haber": imp}]}
                    nueva(tipo="Ajuste", partida=f["partida"], importe=-imp, concepto=f["concepto_banco"],
                          propuesta="Registrar %s contra %s" % (NO_REQUIERE[f["codigo"]].lower(), cta_com or "(cuenta por confirmar)"), regla="R09",
                          confianza="Alta" if cta_com else "Media", operacion=op)
                elif f.get("codigo") == "P14":
                    nueva(tipo="Impuesto", partida=f["partida"], importe=-imp, concepto=f["concepto_banco"],
                          propuesta="Desglosar contra el acuse (impuesto, recargos, actualización, redondeo) y registrar el asiento", regla="R08",
                          confianza="Media", operacion=None)
                elif f.get("uuid"):
                    nueva(tipo="Registrar pago", partida=f["partida"], importe=f["aplicado"] if f["tipo"] == "Cobro" else -f["aplicado"],
                          concepto=f["concepto_banco"], documentos=fac["numero"] if fac else f.get("folio"),
                          propuesta="Registrar el %s de %s en el diario, aplicado a la factura" % (f["tipo"].lower(), f.get("contraparte")),
                          regla=R(f["regla"]), confianza="Alta" if f["regla"] in ("E01", "E02") else "Media",
                          operacion={"op": "registrar_pago", "factura_ids": [fac["id"]], "importe": f["aplicado"], "fecha": f["fecha_banco"],
                                     "diario_id": self.P.get("diario_id"), "memo": f["concepto_banco"][:60]} if fac and fac["estado"] == "posted" else None)
                else:
                    nueva(tipo="Pregunta", partida=f["partida"], importe=firmado, concepto=f["concepto_banco"],
                          propuesta="%s sin documento: ¿de quién es y contra qué cuenta va? Si no se identifica, ¿va a %s?"
                                    % ("Depósito" if f["tipo"] == "Cobro" else "Cargo",
                                       cuentas.get("otros_ingresos", "otros ingresos") if f["tipo"] == "Cobro" else cuentas.get("no_deducibles", "no deducibles")),
                          regla="R13", confianza="Baja", operacion=None)
            elif f["estatus"] == "No identificado":
                nueva(tipo="Pedir CFDI", partida=f["partida"], importe=firmado, concepto=f["concepto_banco"],
                      propuesta="Pedir el CFDI a %s, o registrar con acciones.py que no requiere comprobante (traspaso, préstamo, reembolso)"
                                % (f.get("contacto") or "la contraparte"),
                      regla=R(f["regla"]), confianza="Baja", operacion=None)
            else:
                nueva(tipo="Revisión", partida=f["partida"], importe=firmado, concepto=f["concepto_banco"], propuesta=f.get("observacion", ""),
                      regla=R(f.get("regla")), confianza="Media", operacion=None)
        for x in fvo:
            if not x["numero"]:
                nueva(tipo="Ligar XML", partida="", importe=x["total_cfdi"], concepto="%s %s" % (x["tipo"], x["uuid"]),
                      propuesta="Registrar la factura en Odoo o ligar el XML a la ya registrada", regla="R01", confianza="Media", operacion=None)
        return acc


def resumen(filas, banco, odoo):
    primeras = [f for f in filas if f["primera"]]
    c = collections.Counter(f["estatus"] for f in primeras)
    dinero = collections.defaultdict(float)
    for f in filas:
        dinero[f["estatus"]] += f["aplicado"]
    alertas = sum(1 for f in filas if "Alerta" in (f.get("observacion") or ""))
    return {"partidas": len(primeras), "por_estatus": dict(c), "importe_por_estatus": {k: round(v, 2) for k, v in dinero.items()},
            "alertas": alertas, "pdf_cuadra": banco["control"].get("cuadra"),
            "saldo_final_banco": banco["caratula"].get("saldo_final"), "saldo_final_odoo": odoo.get("saldo_final"),
            "excedente": round(sum(f.get("excedente", 0) for f in filas), 2)}


def main():
    ap = argparse.ArgumentParser()
    for x in ("params", "banco", "odoo", "cfdi", "salida"):
        ap.add_argument(x)
    ap.add_argument("--decisiones")
    ap.add_argument("--lista-69b")
    a = ap.parse_args()
    P, B, O, C = (json.load(open(x)) for x in (a.params, a.banco, a.odoo, a.cfdi))
    if not B["control"].get("cuadra") and not P.get("forzar_sin_control"):
        raise SystemExit("El estado de cuenta no cuadra con su carátula. Corrige la lectura antes de conciliar.")
    dec = json.load(open(a.decisiones)) if a.decisiones else None
    l69 = set()
    if a.lista_69b:
        l69 = {w for w in re.findall(r"\b[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}\b", open(a.lista_69b, encoding="latin-1").read().upper())}
    M = Motor(P, B, O, C, dec, l69)
    filas = M.filas()
    fvo = M.facturas_vs_odoo()
    saldos, det = M.impuestos()
    acc = M.acciones(filas, fvo)
    out = {"params": {k: v for k, v in P.items() if "key" not in k.lower()}, "conciliacion": filas, "facturas_vs_odoo": fvo,
           "impuestos": {"saldos": saldos, "detalle": det}, "estado_cuenta": B, "auxiliar": {"saldo_inicial": O["saldo_inicial"], "renglones": O["auxiliar"]},
           "acciones": acc, "resumen": resumen(filas, B, O), "diarios_caja": O.get("diarios_caja", [])}
    json.dump(out, open(a.salida, "w"), ensure_ascii=False, indent=1, default=str)
    r = out["resumen"]
    print("%d partidas · %s · %d alertas · excedente %s · %d acciones propuestas"
          % (r["partidas"], ", ".join("%s %d" % kv for kv in sorted(r["por_estatus"].items())), r["alertas"], money(r["excedente"]), len(acc)))


if __name__ == "__main__":
    main()

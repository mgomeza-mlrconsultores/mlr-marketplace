# -*- coding: utf-8 -*-
"""Read-only extraction from Odoo for one journal and one period -> odoo.json.

    python3 extraer_odoo.py <params.json> <salida/odoo.json>

params.json (written by the guided start, never with the key):
  {"compania_id": 1, "diario_id": 13, "desde": "2026-08-01", "hasta": "2026-08-31",
   "cuentas": {"iva_acreditable_pagado": "118.01.01", "iva_trasladado_cobrado": "208.01.01"}, ...}

What it reads, in batches (no N+1):
  - journal, its default and suspense accounts, currency, and the company settings that decide
    whether the month can be trusted (cash-basis journal, lock dates, opening date);
  - the ledger of the journal's default account in the period plus the opening balance;
  - for every ledger line, the invoices it settles, following reconciliations up to two hops
    (bank line -> outstanding account -> payment -> receivable/payable -> invoice), which also
    covers payments reconciled straight from a statement line that never became account.payment;
  - invoices of the period and those settled in it, with UUID (ref when the UUID field is empty);
  - lines of the cash-basis VAT accounts with their origin invoice, reversals and journal;
  - unreconciled statement lines, suspense balance and partners' tax data.
Unknown fields are dropped with a warning, so the same script reads 17, 18 and 19.
"""
import collections
import json
import re
import sys

from odoo_client import Lectura

INV = ("out_invoice", "in_invoice", "out_refund", "in_refund")
UUID_RE = re.compile(r"[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}", re.I)


def m2o(v):
    return v[0] if isinstance(v, (list, tuple)) and v else (v or None)


def m2o_nombre(v):
    return v[1] if isinstance(v, (list, tuple)) and len(v) > 1 else ""


def main(params_path, salida):
    P = json.load(open(params_path))
    r = Lectura.desde_entorno(compania_id=P.get("compania_id"))
    avisos, hallazgos = [], []
    cia_dom = [("company_id", "=", P["compania_id"])] if P.get("compania_id") else []

    def campos(model, deseados):
        ok, faltan = r.campos_existentes(model, deseados)
        if faltan:
            avisos.append("%s sin campos %s en esta versión" % (model, ", ".join(faltan)))
        return ok

    ver = r.version().get("server_version")
    # ---------------------------------------------------------------- company and journal
    cia = r.call("res.company", "read", [P["compania_id"]], fields=campos("res.company", [
        "name", "vat", "currency_id", "tax_cash_basis_journal_id", "fiscalyear_lock_date", "tax_lock_date", "sale_lock_date",
        "purchase_lock_date", "hard_lock_date", "account_opening_date", "fiscalyear_last_month", "fiscalyear_last_day", "zip",
        "l10n_mx_edi_fiscal_regime"]))[0]
    dia = r.call("account.journal", "read", [P["diario_id"]], fields=campos("account.journal", [
        "name", "code", "type", "default_account_id", "suspense_account_id", "currency_id", "company_id", "bank_account_id"]))[0]
    cuenta_banco = m2o(dia["default_account_id"])
    cta = r.call("account.account", "read", [cuenta_banco], fields=campos("account.account", ["code", "name", "currency_id", "account_type"]))[0]

    caba = m2o(cia.get("tax_cash_basis_journal_id"))
    if caba:
        cj = r.call("account.journal", "read", [caba], fields=["name", "code", "type"])[0]
        if cj["type"] in ("cash", "bank", "credit"):
            hallazgos.append({"area": "Impuestos", "severidad": "Alta",
                              "hallazgo": "El diario de base de efectivo es %s (%s), un diario de %s" % (cj["name"], cj["code"], cj["type"]),
                              "evidencia": "res.company.tax_cash_basis_journal_id = %s" % caba,
                              "propuesta": "Usar un diario propio de tipo varios (CABA) para los asientos de IVA en flujo"})
    for campo in ("fiscalyear_lock_date", "tax_lock_date", "sale_lock_date", "purchase_lock_date", "hard_lock_date"):
        if cia.get(campo) and cia[campo] >= P["desde"]:
            hallazgos.append({"area": "Cierre", "severidad": "Alta", "hallazgo": "Fecha de bloqueo %s = %s dentro del periodo" % (campo, cia[campo]),
                              "evidencia": "res.company.%s" % campo, "propuesta": "Solo se reporta; la skill no mueve fechas de bloqueo"})
    moneda_cia = m2o(cia.get("currency_id"))
    moneda_dia = m2o(dia.get("currency_id")) or moneda_cia
    moneda_cta = m2o(cta.get("currency_id")) or moneda_cia
    if moneda_dia != moneda_cta:
        hallazgos.append({"area": "Bancos", "severidad": "Alta",
                          "hallazgo": "El diario está en %s y su cuenta %s en %s" % (m2o_nombre(dia.get("currency_id")) or "moneda de la compañía",
                                                                                    cta["code"], m2o_nombre(cta.get("currency_id")) or "moneda de la compañía"),
                          "evidencia": "account.journal.currency_id vs account.account.currency_id",
                          "propuesta": "Sin la misma moneda Odoo no calcula diferencia cambiaria; corregir antes de conciliar"})
    extranjera = moneda_dia != moneda_cia
    if P.get("inicio_operaciones") and cia.get("account_opening_date") and cia["account_opening_date"] != P["inicio_operaciones"]:
        hallazgos.append({"area": "Compañía", "severidad": "Media",
                          "hallazgo": "La fecha de apertura contable es %s y el inicio de operaciones %s" % (cia["account_opening_date"], P["inicio_operaciones"]),
                          "evidencia": "res.company.account_opening_date", "propuesta": "Igualar la apertura contable al inicio de operaciones"})
    # cash-basis taxes: transition account present, and never an asset account for a withholding
    imps = r.sr("account.tax", [("tax_exigibility", "=", "on_payment")] + cia_dom, ["name", "amount", "cash_basis_transition_account_id"])
    trans = sorted({m2o(t["cash_basis_transition_account_id"]) for t in imps if t["cash_basis_transition_account_id"]})
    ttipo = {a["id"]: a for a in (r.call("account.account", "read", trans, fields=["code", "account_type"]) if trans else [])}
    for t in imps:
        ta = ttipo.get(m2o(t["cash_basis_transition_account_id"]))
        if not ta:
            hallazgos.append({"area": "Impuestos", "severidad": "Alta", "hallazgo": "El impuesto en flujo «%s» no tiene cuenta de tránsito" % t["name"],
                              "evidencia": "account.tax %s" % t["id"], "propuesta": "Asignar la cuenta de tránsito antes de conciliar"})
        elif t["amount"] < 0 and ta["account_type"].startswith("asset"):
            hallazgos.append({"area": "Impuestos", "severidad": "Media",
                              "hallazgo": "La retención «%s» usa como tránsito la cuenta de activo %s" % (t["name"], ta["code"]),
                              "evidencia": "account.tax %s cash_basis_transition_account_id" % t["id"],
                              "propuesta": "Usar una cuenta de pasivo de retenciones pendientes; antes revisar que no haya facturas abiertas con ese impuesto"})

    # ---------------------------------------------------------------- ledger of the bank account
    f_aml = campos("account.move.line", ["date", "move_id", "move_name", "name", "ref", "partner_id", "debit", "credit", "balance",
                                         "amount_currency", "currency_id", "statement_line_id", "payment_id", "account_id",
                                         "journal_id", "matched_debit_ids", "matched_credit_ids", "reconciled", "parent_state"])
    dom_cta = [("account_id", "=", cuenta_banco), ("parent_state", "=", "posted")] + cia_dom
    previas = r.sr_todo("account.move.line", dom_cta + [("date", "<", P["desde"])], ["balance", "amount_currency"])
    campo_saldo = "amount_currency" if extranjera else "balance"
    saldo_ini = round(sum(x[campo_saldo] for x in previas), 2)
    aux = r.sr_todo("account.move.line", dom_cta + [("date", ">=", P["desde"]), ("date", "<=", P["hasta"])], f_aml)
    aux.sort(key=lambda x: (x["date"], x["move_name"] or "", x["id"]))

    # follow reconciliations: all lines of the ledger's moves, then partials, up to two hops
    moves = sorted({m2o(x["move_id"]) for x in aux})
    lineas = r.sr_todo("account.move.line", [("move_id", "in", moves)],
                       ["move_id", "account_id", "matched_debit_ids", "matched_credit_ids", "partner_id", "balance"]) if moves else []
    tipo_cta = {}

    def tipos(ids):
        falta = [i for i in ids if i not in tipo_cta]
        for a in (r.call("account.account", "read", falta, fields=["account_type", "code", "reconcile"]) if falta else []):
            tipo_cta[a["id"]] = a
    tipos(sorted({m2o(l["account_id"]) for l in lineas}))

    def contrapartes(ls):
        pids = sorted({p for l in ls for p in l["matched_debit_ids"] + l["matched_credit_ids"]})
        if not pids:
            return {}
        parts = r.call("account.partial.reconcile", "read", pids, fields=["debit_move_id", "credit_move_id", "amount"])
        por_linea = collections.defaultdict(list)
        for p in parts:
            d, c = m2o(p["debit_move_id"]), m2o(p["credit_move_id"])
            por_linea[d].append((c, p["amount"]))
            por_linea[c].append((d, p["amount"]))
        return por_linea

    facturas_de = collections.defaultdict(dict)   # ledger move -> {invoice move: amount}
    por_linea = contrapartes(lineas)
    otras_ids = sorted({o for ls in por_linea.values() for o, _ in ls})
    otras = {l["id"]: l for l in (r.call("account.move.line", "read", otras_ids,
                                         fields=["move_id", "account_id", "matched_debit_ids", "matched_credit_ids"]) if otras_ids else [])}
    tipos(sorted({m2o(l["account_id"]) for l in otras.values()}))
    # second hop: outstanding-account lines of payments
    hop2_src = [l for l in otras.values() if tipo_cta[m2o(l["account_id"])]["account_type"] not in ("asset_receivable", "liability_payable")]
    hop2_moves = sorted({m2o(l["move_id"]) for l in hop2_src})
    hop2_lines = r.sr_todo("account.move.line", [("move_id", "in", hop2_moves)],
                           ["move_id", "account_id", "matched_debit_ids", "matched_credit_ids"]) if hop2_moves else []
    tipos(sorted({m2o(l["account_id"]) for l in hop2_lines}))
    por_linea2 = contrapartes([l for l in hop2_lines if tipo_cta[m2o(l["account_id"])]["account_type"] in ("asset_receivable", "liability_payable")])
    fin_ids = sorted({o for ls in por_linea2.values() for o, _ in ls})
    fin = {l["id"]: l for l in (r.call("account.move.line", "read", fin_ids, fields=["move_id"]) if fin_ids else [])}
    lineas_de_move2 = collections.defaultdict(list)
    for l in hop2_lines:
        lineas_de_move2[m2o(l["move_id"])].append(l)

    for l in lineas:
        mv = m2o(l["move_id"])
        for o, amt in por_linea.get(l["id"], []):
            ol = otras.get(o)
            if not ol:
                continue
            if tipo_cta[m2o(ol["account_id"])]["account_type"] in ("asset_receivable", "liability_payable"):
                inv = m2o(ol["move_id"])
                if inv != mv:
                    facturas_de[mv][inv] = round(facturas_de[mv].get(inv, 0) + amt, 2)
            else:
                for l2 in lineas_de_move2.get(m2o(ol["move_id"]), []):
                    for o2, amt2 in por_linea2.get(l2["id"], []):
                        inv = m2o(fin[o2]["move_id"]) if o2 in fin else None
                        if inv and inv != m2o(ol["move_id"]):
                            facturas_de[mv][inv] = round(facturas_de[mv].get(inv, 0) + amt2, 2)

    # ---------------------------------------------------------------- invoices
    f_mov = campos("account.move", ["name", "ref", "move_type", "state", "payment_state", "amount_total", "amount_residual",
                                    "amount_total_signed", "amount_untaxed", "partner_id", "invoice_date", "date", "l10n_mx_edi_cfdi_uuid",
                                    "l10n_mx_edi_payment_policy", "l10n_mx_edi_cfdi_sat_state", "l10n_mx_edi_cfdi_state",
                                    "journal_id", "currency_id", "tax_cash_basis_origin_move_id", "reversed_entry_id",
                                    "reversal_move_ids"])
    ligadas = sorted({i for d in facturas_de.values() for i in d})
    del_mes = r.sr_todo("account.move", [("move_type", "in", INV), ("state", "!=", "draft"),
                                         ("invoice_date", ">=", P["desde"]), ("invoice_date", "<=", P["hasta"])] + cia_dom, f_mov)
    extra = [i for i in ligadas if i not in {m["id"] for m in del_mes}]
    todas = del_mes + (r.call("account.move", "read", extra, fields=f_mov) if extra else [])
    facturas = {}
    for m in todas:
        if m["move_type"] not in INV:
            continue
        uuid = (m.get("l10n_mx_edi_cfdi_uuid") or "").upper()
        if not uuid:
            u = UUID_RE.search(m.get("ref") or "")
            uuid = u.group(0).upper() if u else ""
        facturas[m["id"]] = {"id": m["id"], "numero": m["name"], "ref": m.get("ref") or "", "tipo": m["move_type"], "estado": m["state"],
                             "estado_pago": m.get("payment_state"), "total": m["amount_total"], "pendiente": m["amount_residual"],
                             "subtotal": m.get("amount_untaxed"), "partner_id": m2o(m["partner_id"]), "partner": m2o_nombre(m["partner_id"]),
                             "fecha": m.get("invoice_date"), "uuid": uuid, "politica": m.get("l10n_mx_edi_payment_policy"),
                             "estado_sat": m.get("l10n_mx_edi_cfdi_sat_state"), "del_mes": m in del_mes,
                             "diario": m2o_nombre(m.get("journal_id"))}

    # ---------------------------------------------------------------- partners
    pids = sorted({m2o(x["partner_id"]) for x in aux if x["partner_id"]} | {f["partner_id"] for f in facturas.values() if f["partner_id"]})
    contactos = {p["id"]: {"nombre": p["name"], "rfc": p.get("vat") or "", "cp": p.get("zip") or "",
                           "regimen": p.get("l10n_mx_edi_fiscal_regime") or "", "pais": m2o_nombre(p.get("country_id"))}
                 for p in (r.call("res.partner", "read", pids, fields=campos("res.partner", ["name", "vat", "zip", "l10n_mx_edi_fiscal_regime", "country_id"])) if pids else [])}

    contra = collections.defaultdict(list)
    for l in lineas:
        a = tipo_cta.get(m2o(l["account_id"]))
        if a and a["id"] != cuenta_banco:
            cp = {"codigo": a["code"], "tipo": a["account_type"]}
            if cp not in contra[m2o(l["move_id"])]:
                contra[m2o(l["move_id"])].append(cp)
    auxiliar = []
    for i, x in enumerate(aux, 1):
        mv = m2o(x["move_id"])
        monto = x["amount_currency"] if extranjera else x["balance"]
        auxiliar.append({"renglon": "O-%03d" % i, "line_id": x["id"], "move_id": mv, "fecha": x["date"], "asiento": x["move_name"],
                         "concepto": " ".join(filter(None, [x["move_name"], x.get("name") or "", x.get("ref") or ""])).strip(),
                         "contacto": m2o_nombre(x["partner_id"]), "partner_id": m2o(x["partner_id"]),
                         "abono": round(monto, 2) if monto > 0 else None, "cargo": round(-monto, 2) if monto < 0 else None,
                         "statement_line_id": m2o(x.get("statement_line_id")), "payment_id": m2o(x.get("payment_id")),
                         "facturas": [{"id": k, "importe": v} for k, v in facturas_de.get(mv, {}).items()],
                         "contrapartes": contra.get(mv, [])})

    # ---------------------------------------------------------------- cash-basis VAT accounts
    iva = []
    for clave in ("iva_acreditable_pagado", "iva_trasladado_cobrado"):
        codigo = P.get("cuentas", {}).get(clave)
        if not codigo:
            continue
        acc = r.sr("account.account", [("code", "=", codigo)], ["id", "code", "name"])
        if not acc:
            avisos.append("No existe la cuenta %s (%s)" % (codigo, clave))
            continue
        dom = [("account_id", "=", acc[0]["id"]), ("parent_state", "=", "posted")] + cia_dom
        ini = round(sum(x["balance"] for x in r.sr_todo("account.move.line", dom + [("date", "<", P["desde"])], ["balance"])), 2)
        ls = r.sr_todo("account.move.line", dom + [("date", ">=", P["desde"]), ("date", "<=", P["hasta"])],
                       ["move_id", "balance", "partner_id", "journal_id", "name"])
        mids = sorted({m2o(l["move_id"]) for l in ls})
        mvs = {m["id"]: m for m in (r.call("account.move", "read", mids, fields=campos("account.move", [
            "name", "tax_cash_basis_origin_move_id", "reversed_entry_id", "reversal_move_ids", "journal_id"])) if mids else [])}
        jids = sorted({m2o(m.get("journal_id")) for m in mvs.values() if m.get("journal_id")})
        jcod = {j["id"]: j["code"] for j in (r.call("account.journal", "read", jids, fields=["code"]) if jids else [])}
        detalle = collections.OrderedDict()
        for l in ls:
            mv = mvs[m2o(l["move_id"])]
            origen = m2o(mv.get("tax_cash_basis_origin_move_id")) or m2o(mv.get("reversed_entry_id")) or mv["id"]
            d = detalle.setdefault(origen, {"origen_id": origen, "iva": 0.0, "reversiones": 0, "diarios": set(), "partner": m2o_nombre(l["partner_id"])})
            d["iva"] = round(d["iva"] + l["balance"], 2)
            if mv.get("reversed_entry_id") or mv.get("reversal_move_ids"):
                d["reversiones"] += 1
            d["diarios"].add(jcod.get(m2o(mv.get("journal_id")), ""))
        orig_ids = [o for o in detalle if o not in facturas]
        for m in (r.call("account.move", "read", orig_ids, fields=["name", "l10n_mx_edi_cfdi_uuid", "ref", "move_type", "journal_id"]) if orig_ids else []):
            detalle[m["id"]]["numero"] = m["name"]
            detalle[m["id"]]["uuid"] = (m.get("l10n_mx_edi_cfdi_uuid") or "").upper()
        for o, d in detalle.items():
            if o in facturas:
                d["numero"], d["uuid"] = facturas[o]["numero"], facturas[o]["uuid"]
            d["reversiones"] = d["reversiones"] // 2  # a reversal pair = entry + its reversal
            d["diarios"] = "/".join(sorted(x for x in d["diarios"] if x))
        iva.append({"clave": clave, "cuenta": codigo, "nombre": acc[0]["name"], "saldo_inicial": ini,
                    "movimiento": round(sum(l["balance"] for l in ls), 2), "detalle": list(detalle.values())})

    # ---------------------------------------------------------------- statement lines and suspense
    sl = r.sr_todo("account.bank.statement.line", [("journal_id", "=", P["diario_id"]), ("is_reconciled", "=", False),
                                                    ("date", "<=", P["hasta"])],
                   campos("account.bank.statement.line", ["date", "amount", "payment_ref", "partner_id", "move_id"]))
    susp = m2o(dia.get("suspense_account_id"))
    saldo_susp = round(sum(x["balance"] for x in r.sr_todo("account.move.line", [("account_id", "=", susp), ("parent_state", "=", "posted"),
                                                                                    ("date", "<=", P["hasta"])] + cia_dom, ["balance"])), 2) if susp else None
    diarios_caja = [j["code"] for j in r.sr("account.journal", [("type", "=", "cash")] + cia_dom, ["code"])]

    out = {"version": ver, "compania": {"id": P["compania_id"], "nombre": cia["name"], "rfc": cia.get("vat"),
                                        "diario_caba": m2o_nombre(cia.get("tax_cash_basis_journal_id")),
                                        "fechas_bloqueo": {k: cia.get(k) for k in ("fiscalyear_lock_date", "tax_lock_date", "hard_lock_date")},
                                        "apertura": cia.get("account_opening_date")},
           "diario": {"id": dia["id"], "nombre": dia["name"], "codigo": dia["code"], "tipo": dia["type"], "cuenta": cta["code"],
                      "cuenta_nombre": cta["name"], "moneda_extranjera": extranjera, "cuenta_suspenso_id": susp,
                      "moneda": m2o_nombre(dia.get("currency_id")) or m2o_nombre(cia.get("currency_id")) or "MXN"},
           "periodo": {"desde": P["desde"], "hasta": P["hasta"]}, "saldo_inicial": saldo_ini,
           "saldo_final": round(saldo_ini + sum((a["abono"] or 0) - (a["cargo"] or 0) for a in auxiliar), 2),
           "auxiliar": auxiliar, "facturas": facturas, "contactos": contactos, "iva": iva,
           "lineas_extracto_sin_conciliar": [{"id": x["id"], "fecha": x["date"], "importe": x["amount"], "texto": x.get("payment_ref"),
                                              "contacto": m2o_nombre(x.get("partner_id"))} for x in sl],
           "saldo_suspenso": saldo_susp, "diarios_caja": diarios_caja, "hallazgos": hallazgos, "avisos": avisos}
    json.dump(out, open(salida, "w"), ensure_ascii=False, indent=1, default=str)
    print("Odoo %s · %s %s · %d renglones del auxiliar · %d facturas · saldo inicial %.2f final %.2f"
          % (ver, dia["code"], cta["code"], len(auxiliar), len(facturas), saldo_ini, out["saldo_final"]))
    for h in hallazgos:
        print("  hallazgo [%s] %s" % (h["severidad"], h["hallazgo"]))
    for a in avisos:
        print("  aviso:", a)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

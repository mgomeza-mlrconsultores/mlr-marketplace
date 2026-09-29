# -*- coding: utf-8 -*-
"""Odoo clients for bank reconciliation: a read-only client and a separate, gated write client.

Transport is JSON-RPC (/jsonrpc). Unlike XML-RPC it returns methods that answer None
(reconcile, action_merge, l10n_mx_edi_cfdi_try_sat) without the "cannot marshal None"
fault, so a successful write is never mistaken for a failure and retried blindly.

Credentials come only from the environment, never from a file that gets archived:
  ODOO_URL, ODOO_DB, ODOO_USER and ODOO_KEY (or ODOO_KEY_FILE pointing to a chmod 600 file).

Read client:
  from odoo_client import Lectura
  r = Lectura.desde_entorno()
  r.sr('account.move', [('move_type', '=', 'in_invoice')], ['name'], limit=5)

Write client (only from aplicar_acciones.py):
  w = Escritura(r, carpeta_trabajo, aprobacion='P001', entorno='pruebas')
  w.escribe('res.partner', [7], {'zip': '06600'}, campos_permitidos={'zip'})
Every write needs an approval id, a field whitelist, a JSON backup of the previous state
and leaves a line in bitacora.jsonl. Unknown methods are refused.
"""
import datetime
import json
import os
import re
import ssl
import urllib.request

LECTURA = {"search_read", "search_count", "read", "fields_get", "search", "name_search",
           "formatted_read_group", "web_read_group", "check_access_rights", "default_get"}

# write methods the skill knows how to verify afterwards; anything else is refused
ESCRITURA = {"write", "create", "action_post", "button_draft", "reconcile", "action_merge",
             "action_create_payments", "l10n_mx_edi_cfdi_try_sat", "message_post"}

# methods that must never be called by this skill, even with approval
PROHIBIDOS = {"unlink", "remove_move_reconcile", "action_unreconcile", "button_cancel",
              "action_undo_reconciliation", "action_reverse", "action_set_lock_date"}


class ErrorOdoo(Exception):
    pass


def _ctx_ssl():
    ca = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    return ssl.create_default_context(cafile=ca) if ca else ssl.create_default_context()


def valida_llave(llave):
    """Odoo API keys are 40 hex chars; a 39-char key makes authenticate() return False silently."""
    if not re.fullmatch(r"[0-9a-fA-F]{40}", llave or ""):
        raise SystemExit("La API key no tiene 40 caracteres hexadecimales (%d leídos). "
                         "Revisa que se copió completa." % len(llave or ""))


class Lectura(object):
    """Read-only client. Blocks any method outside LECTURA before it leaves the machine."""

    def __init__(self, url, db, usuario, llave, compania_id=None):
        valida_llave(llave)
        self.url, self.db, self.usuario, self._llave = url.rstrip("/"), db, usuario, llave
        self._ssl = _ctx_ssl()
        self._n = 0
        self.uid = self._rpc("common", "authenticate", [db, usuario, llave, {}])
        if not self.uid:
            raise SystemExit("authenticate() regresó False: revisa base, usuario y API key.")
        self.compania_id = compania_id

    @classmethod
    def desde_entorno(cls, compania_id=None):
        llave = os.environ.get("ODOO_KEY")
        if not llave and os.environ.get("ODOO_KEY_FILE"):
            ruta = os.path.expanduser(os.environ["ODOO_KEY_FILE"])
            if os.name == "posix" and os.stat(ruta).st_mode & 0o077:
                print("aviso: %s es legible por otros usuarios; ciérralo con chmod 600" % ruta)
            llave = open(ruta).read().strip()
        faltan = [v for v in ("ODOO_URL", "ODOO_DB", "ODOO_USER") if not os.environ.get(v)]
        if faltan or not llave:
            raise SystemExit("Faltan variables de entorno: %s" % ", ".join(faltan + ([] if llave else ["ODOO_KEY"])))
        return cls(os.environ["ODOO_URL"], os.environ["ODOO_DB"], os.environ["ODOO_USER"], llave,
                   compania_id or (int(os.environ["ODOO_COMPANY_ID"]) if os.environ.get("ODOO_COMPANY_ID") else None))

    # -- transport -------------------------------------------------------
    def _rpc(self, service, method, args):
        self._n += 1
        body = json.dumps({"jsonrpc": "2.0", "method": "call", "id": self._n,
                           "params": {"service": service, "method": method, "args": args}}).encode()
        req = urllib.request.Request(self.url + "/jsonrpc", body, {"Content-Type": "application/json"})
        with urllib.request.urlopen(req, context=self._ssl, timeout=180) as resp:
            data = json.loads(resp.read().decode())
        if data.get("error"):
            err = data["error"]
            msg = (err.get("data") or {}).get("message") or err.get("message")
            raise ErrorOdoo(msg)
        return data.get("result")

    def version(self):
        return self._rpc("common", "version", [])

    def _ctx(self, kw):
        ctx = dict(kw.pop("context", None) or {})
        if self.compania_id:
            ctx.setdefault("allowed_company_ids", [self.compania_id])
        if ctx:
            kw["context"] = ctx
        return kw

    def call(self, model, method, *args, **kw):
        if method not in LECTURA:
            raise PermissionError("Bloqueado (solo lectura): %s.%s" % (model, method))
        return self._rpc("object", "execute_kw", [self.db, self.uid, self._llave, model, method, list(args), self._ctx(kw)])

    # -- helpers ---------------------------------------------------------
    def sr(self, model, domain=None, fields=None, **kw):
        return self.call(model, "search_read", domain or [], fields=fields or [], **kw)

    def sr_todo(self, model, domain, fields, paso=2000, **kw):
        """search_read in pages; saas~19.4 has no read_group on account.move, group locally."""
        out, off = [], 0
        while True:
            lote = self.sr(model, domain, fields, limit=paso, offset=off, order="id", **kw)
            out += lote
            if len(lote) < paso:
                return out
            off += paso

    def cnt(self, model, domain=None, **kw):
        return self.call(model, "search_count", domain or [], **kw)

    def campos(self, model):
        return self.call(model, "fields_get", attributes=["type", "relation", "selection", "string"])

    def campos_existentes(self, model, deseados):
        """Keep only the fields this Odoo version has, so one script serves 17, 18 and 19."""
        fg = self.campos(model)
        return [f for f in deseados if f in fg], [f for f in deseados if f not in fg]


class Escritura(object):
    """Gated write client. Lives apart from Lectura on purpose; only aplicar_acciones.py uses it."""

    def __init__(self, lectura, carpeta, aprobacion, entorno, confirmo_produccion=False):
        if not aprobacion:
            raise PermissionError("Toda escritura necesita el ID de aprobación del libro o del chat.")
        if entorno not in ("pruebas", "produccion"):
            raise PermissionError("Entorno desconocido: %r" % entorno)
        if entorno == "produccion" and not confirmo_produccion:
            raise PermissionError("Base de producción: falta la confirmación explícita (--confirmo-produccion).")
        self.r, self.carpeta, self.aprobacion, self.entorno = lectura, carpeta, aprobacion, entorno
        os.makedirs(os.path.join(carpeta, "respaldos"), exist_ok=True)
        self.bitacora = os.path.join(carpeta, "bitacora.jsonl")

    def _respaldo(self, model, ids, campos):
        antes = self.r.call(model, "read", ids, fields=sorted(campos)) if ids and campos else []
        ruta = os.path.join(self.carpeta, "respaldos", "%s_%s_%s.json" % (
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), self.aprobacion, model.replace(".", "_")))
        json.dump({"modelo": model, "ids": ids, "antes": antes}, open(ruta, "w"), ensure_ascii=False, indent=1, default=str)
        return antes, ruta

    def _log(self, model, method, ids, antes, nuevos, resultado, respaldo):
        linea = {"fecha": datetime.datetime.now().isoformat(timespec="seconds"),
                 "fecha_utc": datetime.datetime.utcnow().isoformat(timespec="seconds"), "aprobacion": self.aprobacion,
                 "entorno": self.entorno, "modelo": model, "metodo": method, "ids": ids, "antes": antes,
                 "nuevos": nuevos, "resultado": resultado, "respaldo": respaldo, "usuario": self.r.usuario}
        with open(self.bitacora, "a") as f:
            f.write(json.dumps(linea, ensure_ascii=False, default=str) + "\n")

    def ejecuta(self, model, method, args, kw=None, ids=(), campos_respaldo=(), nuevos=None):
        if method in PROHIBIDOS:
            raise PermissionError("Prohibido por la skill: %s.%s" % (model, method))
        if method not in ESCRITURA:
            raise PermissionError("Método de escritura no previsto: %s.%s" % (model, method))
        ids = list(ids)
        antes, ruta = self._respaldo(model, ids, set(campos_respaldo))
        try:
            res = self.r._rpc("object", "execute_kw", [self.r.db, self.r.uid, self.r._llave, model, method,
                                                       list(args), self.r._ctx(dict(kw or {}))])
            self._log(model, method, ids, antes, nuevos, "OK" if res is None else res, ruta)
            return res
        except Exception as e:
            self._log(model, method, ids, antes, nuevos, "ERROR: %s" % e, ruta)
            raise

    def escribe(self, model, ids, vals, campos_permitidos, contexto=None):
        fuera = set(vals) - set(campos_permitidos)
        if fuera:
            raise PermissionError("Campos no aprobados para este paso: %s" % sorted(fuera))
        if any(isinstance(i, list) for i in ids):
            raise ValueError("IDs anidados: write([[id]]) truena en Odoo; usa write([id]).")
        kw = {"context": contexto} if contexto else {}
        return self.ejecuta(model, "write", [list(ids), vals], kw, ids=ids, campos_respaldo=vals.keys(), nuevos=vals)

    def crea(self, model, vals, campos_permitidos, contexto=None):
        fuera = set(vals) - set(campos_permitidos)
        if fuera:
            raise PermissionError("Campos no aprobados para este paso: %s" % sorted(fuera))
        kw = {"context": contexto} if contexto else {}
        return self.ejecuta(model, "create", [vals], kw, nuevos=vals)

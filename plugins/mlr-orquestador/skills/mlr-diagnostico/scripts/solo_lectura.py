"""Read-only XML-RPC client for Odoo diagnostics.

Every call goes through a whitelist of read methods; anything else raises.
Credentials come from environment variables, never from this file:
  ODOO_URL, ODOO_DB, ODOO_USER and ODOO_KEY (or ODOO_KEY_FILE, chmod 600).

Usage:
  from solo_lectura import sr, cnt, rg, call
  sr('stock.move', [('state', '=', 'done')], ['name', 'value'], limit=10)
"""
import os
import ssl
import xmlrpc.client

URL = os.environ["ODOO_URL"].rstrip("/")
DB = os.environ["ODOO_DB"]
USER = os.environ["ODOO_USER"]
KEY = os.environ.get("ODOO_KEY") or open(os.path.expanduser(os.environ["ODOO_KEY_FILE"])).read().strip()

_ca = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
_ctx = ssl.create_default_context(cafile=_ca) if _ca else ssl.create_default_context()
_common = xmlrpc.client.ServerProxy(URL + "/xmlrpc/2/common", context=_ctx, allow_none=True)
UID = _common.authenticate(DB, USER, KEY, {})
if not UID:
    raise SystemExit("Authentication failed")
_obj = xmlrpc.client.ServerProxy(URL + "/xmlrpc/2/object", context=_ctx, allow_none=True)

ALLOWED = {
    "search", "search_read", "read", "search_count", "read_group", "fields_get",
    "name_search", "check_access_rights", "formatted_read_group", "web_read_group",
    "get_views", "default_get",
}


def call(model, method, *args, **kwargs):
    """Execute a whitelisted read method; block everything else."""
    if method not in ALLOWED:
        raise PermissionError("BLOCKED (read-only): %s.%s" % (model, method))
    return _obj.execute_kw(DB, UID, KEY, model, method, list(args), kwargs)


def sr(model, domain=None, fields=None, **kwargs):
    return call(model, "search_read", domain or [], fields=fields or [], **kwargs)


def cnt(model, domain=None, **kwargs):
    return call(model, "search_count", domain or [], **kwargs)


def rg(model, domain, fields, groupby, **kwargs):
    return call(model, "read_group", domain, fields, groupby, lazy=False, **kwargs)


def version():
    return _common.version()

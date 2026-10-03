#!/usr/bin/env python3
"""Rúbrica automática de calidad para agentes, skills y plugins de un marketplace.

Uso: python3 revisar_agentes.py <raiz_plugins> [--estricto] [--json salida.json]
Revisa: frontmatter válido (name igual al archivo, description con <example>, model, color), secciones obligatorias
(Antes de empezar, Protocolo, Autoverificación, Salida, Vigencia y actualización), referencias a conocimiento
existentes, descargo profesional en dominios regulados, conciencia de versión en agentes técnicos, longitud mínima,
residuos de identidad, skills con frontmatter y agentes citados existentes, plugin.json válido.
Devuelve código 1 en --estricto si hay fallas obligatorias.
"""
import sys, re, json, pathlib

REGULADOS = {"fiscal-mexico": "contador público", "nomina-mexico": "contador público", "practica-contable": "contador público",
             "legal-mexico": "abogado"}
TECNICOS = {"consultoria-odoo", "personalizacion-odoo", "contabilidad-odoo", "despliegue-odoo", "desarrollo-odoo"}
RESIDUOS = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+|\bmlr\b|C:\\\\Users", re.I)
REF = re.compile(r"`conocimiento/([^`]+)`")
AGENTE_CIT = re.compile(r"`([a-z0-9][a-z0-9-]+)`")

def frontmatter(t):
    if not t.startswith("---"): return None, t
    partes = t.split("---", 2)
    if len(partes) < 3: return None, t
    fm, cuerpo = partes[1], partes[2]
    datos = {}
    try:
        import yaml
        datos = yaml.safe_load(fm) or {}
        if not isinstance(datos, dict): return None, cuerpo
    except ImportError:
        lineas = fm.splitlines(); i = 0
        while i < len(lineas):
            m = re.match(r"^([a-z_]+):\s*(.*)$", lineas[i])
            if not m: i += 1; continue
            clave, valor = m.group(1), m.group(2).strip()
            if valor in ("|", ">", ">-", "|-"):
                bloque = []; i += 1
                while i < len(lineas) and (lineas[i].startswith(" ") or lineas[i].strip() == ""):
                    bloque.append(lineas[i].strip()); i += 1
                datos[clave] = "\n".join(bloque).strip(); continue
            datos[clave] = valor.strip('"').strip("'"); i += 1
    except Exception:
        return None, cuerpo
    return datos, cuerpo

OPC = {"prefijo": "", "residuos": True}

def revisar_agente(p, plugin, todos_agentes):
    fallas, avisos = [], []
    t = p.read_text(encoding="utf-8-sig")
    fm, cuerpo = frontmatter(t)
    if fm is None: return [f"frontmatter inválido"], []
    nombre = str(fm.get("name") or "")
    if nombre != p.stem and OPC["prefijo"] + nombre != p.stem and nombre != p.stem[len(OPC["prefijo"]):]: fallas.append(f"name '{nombre}' distinto del archivo")
    d = str(fm.get("description") or "")
    if len(d) < 80: fallas.append("description corta o vacía")
    if "<example>" not in d: fallas.append("description sin <example>")
    if "model" not in fm: fallas.append("sin model")
    if "color" not in fm: avisos.append("sin color")
    for sec in ("## Antes de empezar", "## Protocolo", "## Salida"):
        if sec not in cuerpo: fallas.append(f"falta sección '{sec}'")
    if "Autoverificación" not in cuerpo and "autoverificación" not in cuerpo: fallas.append("sin paso de Autoverificación")
    if "## Vigencia y actualización" not in cuerpo and "## Actualización" not in cuerpo: fallas.append("sin sección de vigencia y actualización")
    if len(cuerpo) < 900: fallas.append(f"cuerpo corto ({len(cuerpo)} caracteres)")
    raiz_plugin = p.parent.parent
    for ref in REF.findall(cuerpo):
        if not (raiz_plugin / "conocimiento" / ref).exists(): fallas.append(f"referencia inexistente conocimiento/{ref}")
    if plugin in REGULADOS and REGULADOS[plugin] not in t: fallas.append(f"sin descargo profesional ('{REGULADOS[plugin]}')")
    PREF = ("app-", "auditor-", "migrador-", "configurador", "cargador", "arquitecto", "desarrollador", "revisor-codigo", "qa-", "upgrade", "onpremise", "odoo-", "rendimiento", "seguridad", "respaldo", "integrador", "analista-datos", "field-", "model-", "view-", "server-", "report-", "conciliador", "cierre", "investigador")
    if plugin in TECNICOS and p.stem.startswith(PREF) and "versi" not in t.lower(): avisos.append("no menciona versión de Odoo")
    if OPC["residuos"] and RESIDUOS.search(t): fallas.append("posible residuo de identidad o correo")
    if "{{" in d: avisos.append("marcador de identidad en description")
    return fallas, avisos

def revisar_skill(p, todos_agentes, conocidos=frozenset()):
    fallas, avisos = [], []
    t = p.read_text(encoding="utf-8-sig"); fm, cuerpo = frontmatter(t)
    if fm is None: return ["frontmatter inválido"], []
    nombre = str(fm.get("name") or "")
    if nombre != p.parent.name and OPC["prefijo"] + nombre != p.parent.name and nombre != p.parent.name[len(OPC["prefijo"]):]: fallas.append(f"name '{nombre}' distinto de la carpeta")
    if len(str(fm.get("description") or "")) < 60: fallas.append("description corta")
    for a in set(AGENTE_CIT.findall(cuerpo)):
        if "-" in a and a not in todos_agentes and a not in conocidos and not a.endswith("*") and a not in ("app-*", "auditor-*", "migrador-*"):
            # solo agentes con guion y sin extensión ni ruta
            if "/" not in a and "." not in a and a.islower() and len(a) > 6 and a.count("-") >= 1 and a not in {"pre-commit", "pylint-odoo", "es-mx", "l10n-mx"}:
                avisos.append(f"cita agente inexistente `{a}`")
    if OPC["residuos"] and RESIDUOS.search(t): fallas.append("posible residuo de identidad o correo")
    return fallas, avisos

def main():
    raiz = pathlib.Path(sys.argv[1]); estricto = "--estricto" in sys.argv
    if "--prefijo" in sys.argv: OPC["prefijo"] = sys.argv[sys.argv.index("--prefijo") + 1]
    if "--sin-residuos" in sys.argv: OPC["residuos"] = False
    salida_json = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
    plugins = [d for d in sorted(raiz.iterdir()) if d.is_dir() and (d / ".claude-plugin/plugin.json").exists()]
    todos = {a.stem for d in plugins for a in (d / "agents").glob("*.md") if (d / "agents").exists()}
    if OPC["prefijo"]: todos |= {a[len(OPC["prefijo"]):] for a in todos if a.startswith(OPC["prefijo"])}
    conocidos = frozenset({d.name for d in plugins} | {s.parent.name for d in plugins for s in d.glob("skills/*/SKILL.md")} | {"identidad-visual", "ui-ux-pro-max", "artifact-design", "system-ui", "data-nav", "sincronizar-genericos"})
    rep = {"agentes": {}, "skills": {}, "plugins": {}, "resumen": {}}
    nf = na = 0
    for d in plugins:
        try:
            pj = json.loads((d / ".claude-plugin/plugin.json").read_text(encoding="utf-8-sig"))
            if pj.get("name") != d.name: rep["plugins"][d.name] = [f"name '{pj.get('name')}' distinto de la carpeta"]; nf += 1
        except Exception as e:
            rep["plugins"][d.name] = [f"plugin.json inválido: {e}"]; nf += 1
        for a in sorted((d / "agents").glob("*.md")) if (d / "agents").exists() else []:
            f, v = revisar_agente(a, d.name, todos)
            if f or v: rep["agentes"][f"{d.name}/{a.name}"] = {"fallas": f, "avisos": v}
            nf += len(f); na += len(v)
        for s in sorted((d / "skills").glob("*/SKILL.md")) if (d / "skills").exists() else []:
            f, v = revisar_skill(s, todos, conocidos)
            if f or v: rep["skills"][f"{d.name}/{s.parent.name}"] = {"fallas": f, "avisos": v}
            nf += len(f); na += len(v)
    rep["resumen"] = {"plugins": len(plugins), "agentes": len(todos), "fallas": nf, "avisos": na}
    print(f"plugins {len(plugins)} | agentes {len(todos)} | fallas {nf} | avisos {na}")
    for k, v in rep["agentes"].items():
        for x in v["fallas"]: print(f"  FALLA {k}: {x}")
        for x in v["avisos"]: print(f"  aviso {k}: {x}")
    for k, v in rep["skills"].items():
        for x in v["fallas"]: print(f"  FALLA skill {k}: {x}")
        for x in v["avisos"]: print(f"  aviso skill {k}: {x}")
    for k, v in rep["plugins"].items():
        for x in v: print(f"  FALLA plugin {k}: {x}")
    if salida_json: pathlib.Path(salida_json).write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    sys.exit(1 if (estricto and nf) else 0)

if __name__ == "__main__":
    main()

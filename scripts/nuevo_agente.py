#!/usr/bin/env python3
"""Crea un agente especializado con la estructura y la rúbrica del marketplace a partir de una especificación JSON.

Uso: python3 nuevo_agente.py --plugin extras/consultoria-odoo --dominio gestion --spec agente.json [--enrutamiento "Texto de la línea"]
Dominios: fiscal | legal | tecnico | gestion (fijan la sección de vigencia y actualización).
La especificación JSON lleva: name, color, descripcion, ejemplo [contexto, usuario, acción, comentario], intro, conocimiento [archivos
relativos a conocimiento/], antes, pasos [[título, contenido], ...], auto, salida. Si se pasa --enrutamiento, la línea se agrega a
ENRUTAMIENTO-AMPLIADO.md del plugin de consultoría (extras) y se anota en MEJORAS.md si existe en la raíz.
"""
import argparse, json, pathlib, sys, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gen_agentes import escribir

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plugin", required=True); ap.add_argument("--dominio", default="gestion", choices=["fiscal", "legal", "tecnico", "gestion"])
    ap.add_argument("--spec", required=True); ap.add_argument("--enrutamiento", default="")
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding="utf-8"))
    plugin = pathlib.Path(a.plugin)
    for c in spec["conocimiento"]:
        if not (plugin / "conocimiento" / c).exists():
            sys.exit(f"conocimiento inexistente: {c} (créalo antes o quítalo de la especificación)")
    escribir(plugin, [spec], a.dominio)
    print("agente creado:", plugin / "agents" / (spec["name"] + ".md"))
    if a.enrutamiento:
        enr = plugin.parent / "consultoria-odoo" / "ENRUTAMIENTO-AMPLIADO.md"
        if enr.exists():
            t = enr.read_text(encoding="utf-8")
            marca = "\n## Regla: ningún agente genérico"
            linea = "- " + a.enrutamiento.strip() + "\n"
            t = t.replace(marca, linea + marca, 1) if marca in t else t.rstrip() + "\n" + linea
            enr.write_text(t, encoding="utf-8"); print("enrutamiento actualizado")
    mej = plugin.parent.parent / "MEJORAS.md"
    if mej.exists():
        with open(mej, "a", encoding="utf-8") as f:
            f.write(f"\n- {datetime.date.today().isoformat()}: agente nuevo `{spec['name']}` en {plugin.name} ({a.dominio}); necesidad: {spec.get('necesidad', 'no registrada')}.\n")
        print("MEJORAS.md anotado")

if __name__ == "__main__":
    main()

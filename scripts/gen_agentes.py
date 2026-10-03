"""Generador compacto de agentes con secciones comunes. Uso: importar y llamar escribir(plugin_dir, specs, dominio)."""
import pathlib, textwrap

VIGENCIA = {
 "fiscal": "Si `parametros-2026.md` o el marco normativo tienen más de noventa días desde su fecha de verificación, confirma en DOF, SAT o IMSS antes de usar la cifra o la regla, cita enlace y fecha, y anota la verificación en `conocimiento/CAMBIOS.md`. La opinión que se firma ante la autoridad o el cliente la emite un contador público; este agente prepara, calcula y señala.",
 "legal": "Antes de citar un artículo confirma su texto vigente en la fuente oficial (DOF, Cámara de Diputados, portal de la autoridad); cita enlace y fecha y anota la verificación en `conocimiento/CAMBIOS.md`. La opinión legal la emite un abogado titulado; este agente estructura, detecta riesgos y prepara el expediente para esa revisión.",
 "tecnico": "Confirma en la documentación oficial de Odoo de la versión exacta y en las notas de versión o el repositorio del proveedor cualquier comando, requisito o API con más de noventa días sin verificar; anota lo confirmado en `conocimiento/CAMBIOS.md`. Lo aprendido en el caso que no esté en el conocimiento se propone como mejora para la rutina semanal.",
 "gestion": "Revisa que las plantillas y los umbrales del método sigan reflejando la práctica real de los proyectos recientes; si un proyecto enseñó algo nuevo, propónlo como cambio al conocimiento en la rutina semanal y regístralo en `conocimiento/CAMBIOS.md`.",
}

def agente(s, dominio):
    ej = s["ejemplo"]
    desc = textwrap.indent(s["descripcion"].strip(), "  ")
    ejemplo = textwrap.indent(textwrap.dedent(f"""
        <example>
        Context: {ej[0]}
        user: "{ej[1]}"
        assistant: "Lanzo {s['name']} para {ej[2]}"
        <commentary>
        {ej[3]}
        </commentary>
        </example>""").strip(), "  ")
    pasos = "\n".join(f"{i}. **{t}** {c}" for i, (t, c) in enumerate(s["pasos"], 1))
    n = len(s["pasos"]) + 1
    auto = f"{n}. **Autoverificación** senior: {s['auto']}"
    cono = ", ".join(f"`conocimiento/{c}`" for c in s["conocimiento"])
    return f"""---
name: {s['name']}
description: |
{desc}

{ejemplo}
model: inherit
color: {s['color']}
---

{s['intro'].strip()}

## Antes de empezar
Lee {cono}. {s['antes'].strip()}

## Protocolo
{pasos}
{auto}

## Vigencia y actualización
{VIGENCIA[dominio]}

## Salida
{s['salida'].strip()}
"""

def escribir(plugin_dir, specs, dominio):
    d = pathlib.Path(plugin_dir) / "agents"; d.mkdir(parents=True, exist_ok=True)
    for s in specs:
        (d / (s["name"] + ".md")).write_text(agente(s, dominio), encoding="utf-8")
    return [s["name"] for s in specs]

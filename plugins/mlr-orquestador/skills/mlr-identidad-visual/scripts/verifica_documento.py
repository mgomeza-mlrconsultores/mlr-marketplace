# -*- coding: utf-8 -*-
"""
Verificador de entregables formales de MLR.

Compara el PDF exportado contra las medidas del documento aprobado por direccion
y contra las reglas de redaccion. Devuelve 0 si todo pasa; 1 si algo falla, con
el detalle de que falla y por cuanto.

**Ningun entregable sale sin que esto pase en verde.** Un fallo no se justifica,
se corrige.

    python3 verifica_documento.py "ruta/Documento.pdf" [--docx "ruta/Documento.docx"]

Requiere pymupdf. El .docx es opcional pero recomendado: sin el no se comprueban
la incrustacion de fuentes ni los margenes.
"""

import sys, os, re, zipfile, statistics, argparse

TOL = 2.0   # puntos de tolerancia contra las medidas de referencia

# --- medidas del documento aprobado ---------------------------------------
CARATULA = {"titulo 1": 130.1, "titulo 2": 182.7, "firmantes": 235.3,
            "metadato 1": 277.3, "metadato 2": 306.0, "saludo": 357.5}
# Un descendente en el ultimo renglon del titulo obliga a despejar 7.7 pt para
# que la cola no choque con los firmantes (274 tw); todo lo que va debajo baja igual.
DESCENDENTES = set("gjpqy")
DESPLAZA_DESCENDENTE = 13.7   # los 274 tw de holgura, en puntos
BAJAN_CON_DESCENDENTE = ("firmantes", "metadato 1", "metadato 2", "saludo")
# Bandas calibradas de modo que el DOCUMENTO APROBADO pase limpio. Ese es el
# contrato del verificador: si el archivo de direccion falla, el umbral esta mal.
BANDA_LINEA = (15.0, 16.1)    # interlineado exacto; el automatico da ~18.3
BANDA_VINETA = (18.4, 19.6)
# Se compara la MEDIANA, no la media ni una proporcion: las filas de cuadro y las
# lineas sueltas contaminan la muestra y la mediana las absorbe sin ruido.
OCUPACION_MIN = 70            # el aprobado tiene una plana al 75%
BANDA_PALABRAS = (14.0, 30.0)
TEAL = "#23656f"
PESOS = ["Lexend", "Lexend SemiBold", "Lexend ExtraBold"]
CAJA_SUP, CAJA_INF = 79.2, 691.2      # margenes 1584 / 2016 tw
ALTO_CONTACTO = 144.0                 # 2" que reserva el bloque de contacto

PROHIBIDO = [
    (r"no es [^.]{2,40}, es ", "antitesis de definicion «X no es Y, es Z»"),
    (r"no se trata de", "«no se trata de X, sino de Y»"),
    (r"no s[oó]lo [^.]{2,60} sino", "triada «no solo X, sino tambien Y»"),
    (r"La primera [a-záéíóúñ]+[:.].{0,400}?La segunda", "enumeracion paralela con verbo al frente"),
    (r"\b(proyecta|equipa|instala|propone|entrega|proporciona):", "dos puntos retoricos"),
    # «servicios integrales» y «parte integral» son terminos de negocio, no relleno
    (r"\b(robusto|hol[ií]stico|crucial|potente)\b", "adjetivacion vacia"),
    (r"\bintegral(es)?\b(?!\s+(de\s+esta|entre|a\s+las))(?<!servicios integral)"
     r"(?<!servicios integrales)", "adjetivacion vacia"),
    (r"\b(aprovechar|potenciar|impulsar|desbloquear|empoderar)\b", "verbo de folleto"),
    (r"(es importante senalar|es importante señalar|cabe destacar|en el panorama actual)", "formula de encuadre"),
    (r"\b(contingencia|colch[oó]n|buffer)\b", "termino interno que no puede salir al cliente"),
]

def zonas_de_cuadro(pagina):
    """Rectangulos que ocupan los cuadros. Sus renglones tienen su propio ritmo
    y contaminan la medida del interlineado del texto corrido."""
    try:
        return [t.bbox for t in pagina.find_tables().tables]
    except Exception:
        return []

def en_cuadro(l, zonas):
    return any(z[1] - 2 <= l["y0"] <= z[3] + 2 for z in zonas)

def lineas(pagina):
    out = []
    for b in pagina.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for l in b["lines"]:
            t = "".join(s["text"] for s in l["spans"]).strip()
            if t:
                out.append({"y0": l["bbox"][1], "y1": l["bbox"][3],
                            "sz": round(l["spans"][0]["size"], 1),
                            "color": "#%06x" % l["spans"][0]["color"], "t": t})
    return sorted(out, key=lambda d: d["y0"])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--docx")
    ap.add_argument("--sin-caratula", action="store_true",
                    help="para anexos y documentos que no llevan bloque de caratula")
    a = ap.parse_args()
    try:
        import pymupdf
    except ImportError:
        print("FALTA pymupdf: pip install pymupdf --break-system-packages"); return 1

    fallos, avisos = [], []
    d = pymupdf.open(a.pdf)
    pags = [lineas(p) for p in d]
    cuadros = [zonas_de_cuadro(p) for p in d]

    # 1. caratula ----------------------------------------------------------
    if not a.sin_caratula:
        p1 = pags[0]
        gordas = [l for l in p1 if l["sz"] >= 40]
        obtenido = {}
        if gordas:
            obtenido["titulo 1"] = gordas[0]["y0"]
            if len(gordas) > 1:
                obtenido["titulo 2"] = gordas[1]["y0"]
            if len(gordas) > 2:
                fallos.append("El titulo ocupa %d renglones. El maximo es 2: se acorta "
                              "el titulo, no se baja el tamano." % len(gordas))
        for l in p1:
            if 15.5 <= l["sz"] <= 16.5 and "firmantes" not in obtenido:
                obtenido["firmantes"] = l["y0"]
            elif l["sz"] == 13.0 and l["color"] == TEAL:
                k = "metadato 1" if "metadato 1" not in obtenido else "metadato 2"
                if k not in obtenido and not re.match(r"^\d+\.", l["t"]):
                    obtenido[k] = l["y0"]
            elif 14.5 <= l["sz"] <= 15.5 and "saludo" not in obtenido:
                obtenido["saludo"] = l["y0"]
        cola = bool(gordas) and bool(DESCENDENTES & set(gordas[-1]["t"].lower()))
        for k, ref in CARATULA.items():
            if k not in obtenido:
                fallos.append("Falta el bloque de caratula «%s»." % k); continue
            if cola and k in BAJAN_CON_DESCENDENTE:
                ref += DESPLAZA_DESCENDENTE
            dif = obtenido[k] - ref
            if abs(dif) > TOL:
                fallos.append("Caratula «%s» a %.1f pt; el aprobado la pone en %.1f "
                              "(%+.1f)." % (k, obtenido[k], ref, dif))
        n_meta = sum(1 for l in p1 if l["sz"] == 13.0 and l["color"] == TEAL
                     and not re.match(r"^\d+\.", l["t"]))
        if n_meta > 2:
            fallos.append("La caratula lleva %d metadatos. Solo van dos: Cliente y "
                          "Fecha." % n_meta)

    # 2. ritmo vertical ----------------------------------------------------
    dentro, entre_vin = [], []
    for pg, zc in zip(pags, cuadros):
        cuerpo = [l for l in pg if l["sz"] == 11.0 and l["y1"] < CAJA_INF
                  and not en_cuadro(l, zc)]
        for x, y in zip(cuerpo, cuerpo[1:]):
            dif = round(y["y0"] - x["y0"], 1)
            if 15.0 < dif < 17.0:   # por debajo de 15 son filas de cuadro
                dentro.append(dif)
            elif 18.0 < dif < 21.0:
                entre_vin.append(dif)
    if dentro:
        med = statistics.median(dentro)
        if not BANDA_LINEA[0] <= med <= BANDA_LINEA[1]:
            fallos.append("Interlineado con mediana de %.2f pt, fuera de la banda "
                          "%.1f-%.1f del documento aprobado. El automatico da ~18.3: "
                          "revisar w:lineRule." % (med, BANDA_LINEA[0], BANDA_LINEA[1]))
    else:
        avisos.append("No se pudo medir el interlineado del cuerpo.")
    if entre_vin:
        med = statistics.median(entre_vin)
        if not BANDA_VINETA[0] <= med <= BANDA_VINETA[1]:
            fallos.append("Separacion entre vinetas con mediana de %.2f pt; el "
                          "aprobado usa 19.0." % med)

    # 3. maquetacion -------------------------------------------------------
    for i, pg in enumerate(pags):
        cuerpo = [l for l in pg if l["y1"] < CAJA_INF]
        if not cuerpo:
            fallos.append("La plana %d no tiene texto de cuerpo: sobra." % (i + 1))
            continue
        ocupa = (max(l["y1"] for l in cuerpo) - CAJA_SUP) / (CAJA_INF - CAJA_SUP) * 100
        if i < len(pags) - 1 and ocupa < OCUPACION_MIN:
            fallos.append("La plana %d queda al %.0f%% de ocupacion. Minimo %d%% "
                          "salvo la ultima: acortar celdas o recolocar el cuadro, "
                          "no meter un salto." % (i + 1, ocupa, OCUPACION_MIN))
        secciones = [l for l in cuerpo if l["sz"] == 13.0 and re.match(r"^\d+\.", l["t"])]
        for s in secciones:
            if CAJA_INF - s["y0"] < 90 and i < len(pags) - 1:
                fallos.append("El encabezado «%s» arranca a %.0f pt del pie de la "
                              "plana %d: se queda colgado."
                              % (s["t"][:40], CAJA_INF - s["y0"], i + 1))
    ult = [l for l in pags[-1] if l["y1"] < CAJA_INF]
    if ult:
        libre = CAJA_INF - max(l["y1"] for l in ult)
        if libre < ALTO_CONTACTO:
            fallos.append("En la ultima plana quedan %.0f pt y el bloque de contacto "
                          "necesita %.0f. Se va a ir a una plana sola: hay que "
                          "recortar contenido." % (libre, ALTO_CONTACTO))
    if not any(b.get("type") == 1 for b in d[-1].get_text("dict")["blocks"]):
        fallos.append("La ultima plana no lleva el bloque de contacto.")

    # 4. redaccion ---------------------------------------------------------
    txt = re.sub(r"\s+", " ", " ".join(l["t"] for pg in pags for l in pg))
    for pat, nombre in PROHIBIDO:
        m = re.findall(pat, txt, re.I)
        if m:
            fallos.append("Construccion prohibida (%s): %s" % (nombre, m[:2]))
    frases = [f for f in re.split(r"(?<=[.:])\s", txt) if len(f.split()) > 4]
    if frases:
        media = statistics.mean(len(f.split()) for f in frases)
        if media < BANDA_PALABRAS[0]:
            fallos.append("Media de %.1f palabras por oracion. Por debajo de %.0f el "
                          "texto esta cortado en sentencias, que es lo que el cliente "
                          "lee como escritura de maquina." % (media, BANDA_PALABRAS[0]))
        elif media > BANDA_PALABRAS[1]:
            avisos.append("Media de %.1f palabras por oracion, por encima de %.0f. "
                          "Revisar que no haya frases enredadas." % (media, BANDA_PALABRAS[1]))

    # 5. paquete -----------------------------------------------------------
    if a.docx and os.path.exists(a.docx):
        z = zipfile.ZipFile(a.docx)
        nombres = set(z.namelist())

        # Validez OPC: toda parte necesita tipo de contenido, por Default de
        # extension o por Override propio. Una sola parte sin declarar invalida
        # el paquete y Word solo dice «contenido no legible», sin senalar cual.
        ct = z.read("[Content_Types].xml").decode("utf8")
        defaults = set(x.lower() for x in re.findall(r'<Default Extension="([^"]+)"', ct))
        overrides = set(re.findall(r'<Override PartName="/([^"]+)"', ct))
        huerfanas = [n for n in sorted(nombres)
                     if not n.endswith("/") and n != "[Content_Types].xml"
                     and n not in overrides
                     and n.rsplit(".", 1)[-1].lower() not in defaults]
        if huerfanas:
            fallos.append("Partes del paquete sin tipo de contenido declarado: %s. "
                          "Word abrira el archivo como danado." % huerfanas)

        # Toda relacion apunta a una parte que existe
        for rels in [n for n in nombres if n.endswith(".rels")]:
            base = rels.rsplit("_rels/", 1)[0]
            for tgt in re.findall(r'Target="([^"]+)"', z.read(rels).decode("utf8")):
                if tgt.startswith(("http", "mailto", "/")) or ".." in tgt:
                    continue
                if (base + tgt) not in nombres:
                    fallos.append("La relacion de %s apunta a «%s», que no esta en "
                                  "el paquete." % (rels, tgt))
        doc = z.read("word/document.xml").decode("utf8")
        ft = (z.read("word/fontTable.xml").decode("utf8")
              if "word/fontTable.xml" in nombres else "")
        rels = (z.read("word/_rels/fontTable.xml.rels").decode("utf8")
                if "word/_rels/fontTable.xml.rels" in nombres else "")
        for fam in PESOS:
            mm = re.search(r'<w:font w:name="%s">.*?<w:embedRegular r:id="([^"]+)" '
                           r'w:fontKey="([^"]+)"' % re.escape(fam), ft, re.S)
            if not mm:
                fallos.append("«%s» no esta incrustada. En una maquina sin Lexend "
                              "Word la sustituye por serif." % fam); continue
            rid, guid = mm.groups()
            tg = re.search(r'Id="%s"[^>]*Target="([^"]+)"' % rid, rels)
            if not tg:
                fallos.append("«%s» declara incrustacion sin relacion." % fam); continue
            k = bytes(reversed(bytes.fromhex(guid.strip("{}").replace("-", ""))))
            crudo = bytearray(z.read("word/" + tg.group(1)))
            for i in range(32):
                crudo[i] ^= k[i % 16]
            try:
                from fontTools.ttLib import TTFont
                import io as _io
                if TTFont(_io.BytesIO(bytes(crudo)), lazy=True)["name"].getDebugName(1) != fam:
                    fallos.append("La fuente incrustada para «%s» no es esa familia. "
                                  "Word ignora la incrustacion en silencio." % fam)
            except Exception as e:
                fallos.append("No se pudo validar la incrustacion de «%s»: %s" % (fam, e))
        pm = re.search(r"<w:pgMar[^>]*/>", doc)
        if pm and ('w:top="1584"' not in pm.group(0) or 'w:bottom="2016"' not in pm.group(0)):
            fallos.append("Margenes fuera de la plantilla calibrada: %s" % pm.group(0))
        if "<w:b/>" in doc:
            avisos.append("Hay <w:b/> en el documento. El peso se expresa con el "
                          "nombre de familia; combinarlos engorda el trazo.")

    # --- salida -----------------------------------------------------------
    print("Verificacion de %s — %d planas" % (os.path.basename(a.pdf), len(pags)))
    for x in avisos:
        print("  aviso   %s" % x)
    if fallos:
        print("\n%d FALLO(S):" % len(fallos))
        for x in fallos:
            print("  - %s" % x)
        print("\nNo se entrega hasta que esto salga limpio.")
        return 1
    print("  Todo conforme al documento aprobado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""Formato de solicitud de informacion para cotizar — MLR Consultores.

El molde es `Formato_Cotizacion_MLR.docx`, el archivo que direccion aprueba. No se
rehace la maqueta: se **clona el paquete** y solo se reemplaza `word/document.xml`.
Asi los estilos, el membrete de plana completa, los margenes y el bloque de contacto
quedan byte por byte identicos al aprobado, y no hay forma de desviarse del formato.

Uso:

    import formato_cotizacion as F
    import contenido_formato as C
    F.genera(C, "/ruta/Formato_Cotizacion_MLR_Cliente.docx")

El modulo de contenido expone TITULO, SUBTITULO, SALUDO, ENTRADA, CIERRE y BLOQUES,
una lista de pares (nombre del bloque, lista de puntos).

Despues, siempre: exportar a PDF, renderizar y mirar las planas.
"""

import os, re, zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
PLANTILLA = "Formato_Cotizacion_MLR.docx"
DIRS_PLANTILLA = [
    r"G:\Unidades compartidas\MMLR 2025\Hoja Membretada",
    r"C:\Users\mgome\Claude\Projects\MLR Odoo\Plantillas",
    os.path.join(AQUI, "..", "assets", "plantillas"),
]

# Medidos sobre el aprobado. No se tocan.
TEAL = "24646C"
SZ_TITULO = "42"        # medios puntos
SEP_NUMERO = "   "      # tres espacios entre el numero y el nombre del bloque


def _busca_plantilla():
    for d in DIRS_PLANTILLA:
        p = os.path.join(d, PLANTILLA)
        if os.path.exists(p):
            return p
        p = os.path.join(d, "Copia de " + PLANTILLA)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(
        "No se encontro %s. El formato no se reconstruye a mano: hay que localizar "
        "el archivo aprobado. Buscado en: %s" % (PLANTILLA, DIRS_PLANTILLA))


def _esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _titulo(t):
    return ('<w:p><w:pPr><w:pStyle w:val="Ttulo"/><w:spacing w:after="100"/></w:pPr>'
            '<w:r><w:rPr><w:sz w:val="%s"/></w:rPr><w:t>%s</w:t></w:r></w:p>'
            % (SZ_TITULO, _esc(t)))


def _subtitulo(t):
    return ('<w:p><w:pPr><w:spacing w:after="180"/></w:pPr><w:r><w:rPr><w:b/>'
            '<w:color w:val="%s"/><w:sz w:val="18"/></w:rPr><w:t>%s</w:t></w:r></w:p>'
            % (TEAL, _esc(t)))


def _saludo(t):
    return ('<w:p><w:pPr><w:spacing w:after="140"/></w:pPr><w:r><w:t>%s</w:t></w:r></w:p>'
            % _esc(t))


def _parrafo(t):
    return ('<w:p><w:pPr><w:spacing w:after="120"/><w:jc w:val="both"/></w:pPr>'
            '<w:r><w:t>%s</w:t></w:r></w:p>' % _esc(t))


def _seccion(n, t):
    # keepNext + keepLines: el encabezado nunca queda solo al pie de la plana.
    return ('<w:p><w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="100" w:after="100"/>'
            '</w:pPr><w:r><w:rPr><w:b/><w:color w:val="%s"/></w:rPr>'
            '<w:t xml:space="preserve">%02d%s%s</w:t></w:r></w:p>'
            % (TEAL, n, SEP_NUMERO, _esc(t)))


def _punto(t, une=True):
    # La vineta es un caracter con color, no una lista numerada: asi lo hace el aprobado.
    return ('<w:p><w:pPr>%s<w:keepLines/><w:spacing w:after="40"/>'
            '<w:ind w:left="245" w:hanging="245"/></w:pPr>'
            '<w:r><w:rPr><w:color w:val="%s"/></w:rPr>'
            '<w:t xml:space="preserve">\u2022  </w:t></w:r>'
            '<w:r><w:t>%s</w:t></w:r></w:p>'
            % ('<w:keepNext/>' if une else '', TEAL, _esc(t)))


def _cierre(t):
    return ('<w:p><w:pPr><w:spacing w:before="140" w:after="0"/><w:jc w:val="center"/></w:pPr>'
            '<w:r><w:rPr><w:b/><w:color w:val="%s"/></w:rPr><w:t>%s</w:t></w:r></w:p>'
            % (TEAL, _esc(t)))


def genera(contenido, salida, plantilla=None):
    """Escribe el .docx y devuelve su ruta."""
    base = plantilla or _busca_plantilla()

    cuerpo = [_titulo(contenido.TITULO), _subtitulo(contenido.SUBTITULO),
              _saludo(contenido.SALUDO), _parrafo(contenido.ENTRADA)]
    for i, (nombre, puntos) in enumerate(contenido.BLOQUES, 1):
        if not puntos:
            raise ValueError("El bloque %s no tiene puntos." % nombre)
        cuerpo.append(_seccion(i, nombre))
        for j, p in enumerate(puntos):
            # El encadenado de keepNext mantiene entero el bloque: un bloque que no
            # cabe arranca completo en la plana siguiente.
            cuerpo.append(_punto(p, une=(j < len(puntos) - 1)))
    cuerpo.append(_cierre(contenido.CIERRE))

    fuente = zipfile.ZipFile(base)
    doc = fuente.read("word/document.xml").decode("utf-8")
    cab = doc[:doc.index("<w:body>") + len("<w:body>")]
    sect = doc[doc.index("<w:sectPr "):doc.index("</w:body>")]
    sect = re.sub(r' w:rsid[A-Za-z]*="[^"]*"', "", sect)
    nuevo = cab + "".join(cuerpo) + sect + "</w:body></w:document>"

    carpeta = os.path.dirname(os.path.abspath(salida))
    if carpeta and not os.path.isdir(carpeta):
        os.makedirs(carpeta)
    with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as z:
        for it in fuente.infolist():
            datos = (nuevo.encode("utf-8") if it.filename == "word/document.xml"
                     else fuente.read(it.filename))
            z.writestr(it, datos)
    fuente.close()
    return salida

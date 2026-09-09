# -*- coding: utf-8 -*-
"""
Constructor de documentos formales de MLR Consultores.

Reproduce el documento aprobado por direccion —`referencia/Cotizacion aprobada.pdf`,
de la C.P. Monica Arellano— hasta la decima de punto: caratula, tipografia Lexend con
sus tres pesos, interlineado exacto, espacios entre bloques, cuadros que no se parten,
incrustacion de fuentes y cierre con el bloque de contacto.

**No se escribe OOXML a mano para un entregable de MLR. Se usa este modulo.**
Cada valor de aqui esta medido sobre ese PDF; cambiarlos a ojo rompe la equivalencia.

Uso:

    from documento_mlr import Documento
    d = Documento(titulo=["Cotización", "Proyecto Odoo"],
                  cliente="Grupo Haus — Atención: Sr. Luis Ponce de León",
                  fecha="8 de septiembre de 2026",
                  saludo="Estimado Sr. Luis Ponce de León:")
    d.parrafo("Por medio de la presente, MLR Consultores presenta ...")
    d.seccion("1. Alcance del servicio propuesto")
    d.vinetas(["Ventas y gestión comercial, ...", "Compras, ..."])
    d.cuadro(["Hito", "Se libera contra", "Importe"], filas, [700, 4600, 1760])
    d.cierre()                       # parrafo de cortesia + bloque de contacto
    d.guarda("/ruta/Propuesta.docx")

Despues, siempre: `verifica_documento.py` sobre el PDF exportado.
"""

import re, os, html, uuid, zipfile

# --------------------------------------------------------------------------
# Rutas. La plantilla y el PDF de referencia viven junto a la skill.
# --------------------------------------------------------------------------
AQUI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(AQUI, "..", "assets")
PLANTILLA_VARIAS = "Hoja Membretada MLR - varias paginas.docx"
PLANTILLA_UNA = "Hoja Membretada MLR - 1 pagina.docx"
DIRS_PLANTILLA = [
    r"C:\Users\mgome\Claude\Projects\MLR Odoo\Plantillas",
    r"G:\Unidades compartidas\MMLR 2025\Hoja Membretada",
    os.path.join(ASSETS, "plantillas"),
]

def _busca_plantilla(nombre=PLANTILLA_VARIAS):
    for d in DIRS_PLANTILLA:
        p = os.path.join(d, nombre)
        if os.path.exists(p):
            return p
        p = os.path.join(d, "Copia de " + nombre)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(
        "No se encontro la hoja membretada. No se reconstruye el membrete: "
        "hay que localizar la plantilla oficial. Buscado en: %s" % DIRS_PLANTILLA)

# --------------------------------------------------------------------------
# Constantes medidas sobre el documento aprobado. Todo en twips (1 pt = 20).
# --------------------------------------------------------------------------
TEAL, GRIS, BLANCO = "23656F", "595959", "FFFFFF"
REG, SEMI, XBOLD = "Lexend", "Lexend SemiBold", "Lexend ExtraBold"

# Tamanos en medios puntos
SZ_TITULO, SZ_FIRMANTES, SZ_META = 84, 32, 26
SZ_SALUDO, SZ_SECCION, SZ_CUERPO = 30, 26, 22
SZ_CAB_CUADRO, SZ_NOTA = 21, 20

# Ritmo vertical de la caratula
K_TITULO, K_FIRMANTES, K_META, K_SALUDO = 1180, 0, 140, 700
L_TITULO, L_FIRMANTES, L_META, L_SALUDO = 1060, 280, 440, 340

# Interlineado y espacio entre bloques
L_CUERPO, A_CUERPO = 317, 145   # 15.85 pt de linea, 7.25 pt despues
L_VINETA, A_VINETA = 308, 72    # 15.40 pt de linea, 3.60 pt despues
L_NOTA,   A_NOTA   = 288, 145   # 14.40 pt de linea
B_SECCION, A_SECCION = 240, 80  # 12 pt antes, 4 pt despues

# Sangria de vineta: guion a 400 tw del margen, texto a 1240
IND_VINETA, COLGANTE_VINETA = 1240, 840
IND_META, TAB_META = 260, 1480

PGMAR = ('<w:pgMar w:top="1584" w:right="1440" w:bottom="2016" w:left="1440" '
         'w:header="1138" w:footer="1512" w:gutter="0"/>')

# Con interlineado exacto de 53 pt, la cola de una g, j, p, q o y a 42 pt se sale
# de la caja y aterriza sobre la linea de firmantes. El documento aprobado no lo
# sufre porque «de Nómina Semanal» no lleva descendentes. Medido: el hueco de
# tinta entre el titulo y los firmantes es de 11.5 pt en el aprobado, y una «y»
# se come 7.7 de ellos. Se despeja solo cuando el ultimo renglon lo necesita.
DESCENDENTES = set("gjpqy")
HOLGURA_DESCENDENTE = 274      # twips

FIRMANTES_MLR = "C.P. MONICA ARELLANO | C.P. JUAN MARCOS LÓPEZ"
CORTESIA = ("Quedamos atentos a sus comentarios y esperamos contar con su aprobación "
            "para definir los siguientes pasos.")

# --------------------------------------------------------------------------
# Primitivas OOXML
# --------------------------------------------------------------------------
def esc(t):
    return html.escape(t, quote=False)

def run(t, fam=None, color=None, sz=None):
    """Un run. El peso se expresa con el NOMBRE DE FAMILIA, no con <w:b/>:
    asi lo hace el documento aprobado, y combinarlo con la negrita del
    procesador engorda el trazo de mas."""
    r = ""
    if fam:
        r += '<w:rFonts w:ascii="%s" w:hAnsi="%s" w:cs="%s"/>' % (fam, fam, fam)
    if color:
        r += '<w:color w:val="%s"/>' % color
    if sz:
        r += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (sz, sz)
    rpr = "<w:rPr>%s</w:rPr>" % r if r else ""
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, esc(t))

def par(inner, after=A_CUERPO, before=0, jc="both", ind=0, colgante=0,
        keep=False, juntas=False, line=None, tab=0):
    p = "<w:pPr>"
    if keep:
        p += "<w:keepNext/>"
    if juntas:
        p += "<w:keepLines/>"
    if tab:
        p += '<w:tabs><w:tab w:val="left" w:pos="%d"/></w:tabs>' % tab
    ln = ' w:line="%d" w:lineRule="exact"' % line if line else ""
    p += '<w:spacing w:before="%d" w:after="%d"%s/>' % (before, after, ln)
    if ind:
        p += ('<w:ind w:left="%d" w:hanging="%d"/>' % (ind, colgante)
              if colgante else '<w:ind w:left="%d"/>' % ind)
    p += '<w:jc w:val="%s"/>' % jc
    return "<w:p>%s</w:pPr>%s</w:p>" % (p, inner)

# --------------------------------------------------------------------------
# Incrustacion de fuentes (ECMA-376 17.8.1)
# --------------------------------------------------------------------------
FUENTES = [("Lexend", "Lexend.ttf"),
           ("Lexend SemiBold", "LexendSemiBold.ttf"),
           ("Lexend ExtraBold", "LexendExtraBold.ttf")]

def ofusca(datos, guid):
    """XOR de los 16 bytes de la clave, EN ORDEN INVERSO, sobre los primeros 32
    bytes del archivo. Involutiva: la misma funcion ofusca y desofusca."""
    k = bytes(reversed(bytes.fromhex(guid.strip("{}").replace("-", ""))))
    d = bytearray(datos)
    for i in range(32):
        d[i] ^= k[i % 16]
    return bytes(d)

def _incrusta(ft_xml, rels_xml, settings_xml):
    """Lexend no esta instalada en las maquinas de MLR ni en las de los clientes.
    Sin incrustar, Word cae en la fuente del tema —Cambria, serif— y el documento
    no se parece al modelo. El archivo aprobado incrusta las suyas."""
    partes = {}
    ft = ft_xml.decode("utf8")
    rl = rels_xml.decode("utf8")
    for i, (fam, arch) in enumerate(FUENTES):
        ruta = os.path.join(ASSETS, "fuentes", arch)
        if not os.path.exists(ruta):
            raise FileNotFoundError(
                "Falta %s. Sin las tres familias no se puede incrustar y el "
                "documento saldra en serif en cualquier maquina sin Lexend." % ruta)
        rid = "rIdLex%d" % i
        guid = "{%s}" % str(uuid.uuid4()).upper()
        partes["word/fonts/lexend%d.odttf" % i] = ofusca(open(ruta, "rb").read(), guid)
        decl = ('<w:font w:name="%s"><w:panose1 w:val="00000000000000000000"/>'
                '<w:charset w:val="00"/><w:family w:val="swiss"/>'
                '<w:pitch w:val="variable"/>'
                '<w:embedRegular r:id="%s" w:fontKey="%s"/></w:font>' % (fam, rid, guid))
        ft = re.sub(r'<w:font w:name="%s">.*?</w:font>' % re.escape(fam), '', ft, flags=re.S)
        ft = ft.replace("</w:fonts>", decl + "</w:fonts>")
        rl = rl.replace("</Relationships>",
            '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/'
            'officeDocument/2006/relationships/font" Target="fonts/lexend%d.odttf"/>'
            "</Relationships>" % (rid, i))
    st = settings_xml.decode("utf8")
    if "embedTrueTypeFonts" not in st:
        st = re.sub(r'(<w:settings[^>]*>)', r'\1<w:embedTrueTypeFonts/>', st, count=1)
    st = st.replace("<w:saveSubsetFonts/>", "")   # viaja la fuente completa
    return ft.encode("utf8"), rl.encode("utf8"), st.encode("utf8"), partes

CT_FUENTE = "application/vnd.openxmlformats-officedocument.obfuscatedFont"

def _declara_tipos(ct_xml, partes_fuente, con_pie):
    """Cada parte del paquete necesita su tipo de contenido declarado.

    Las fuentes incrustadas NO se cubren con `<Default Extension="odttf">`: la
    plantilla declara un `<Override>` por archivo, y hay que hacer lo mismo con
    cada fuente que se anada. Una sola parte sin declarar invalida el paquete
    entero y Word lo reporta como «contenido no legible», sin decir cual es.
    """
    x = ct_xml.decode("utf8")
    extra = "".join('<Override PartName="/%s" ContentType="%s"/>' % (n, CT_FUENTE)
                    for n in partes_fuente)
    if con_pie:
        extra += ('<Override PartName="/word/footer1.xml" ContentType="application/vnd.'
                  'openxmlformats-officedocument.wordprocessingml.footer+xml"/>')
    return x.replace("</Types>", extra + "</Types>").encode("utf8")

def _lexend_por_defecto(styles_xml):
    x = styles_xml.decode("utf8")
    return re.sub(
        r'<w:rPrDefault><w:rPr>.*?</w:rPr></w:rPrDefault>',
        '<w:rPrDefault><w:rPr><w:rFonts w:ascii="Lexend" w:hAnsi="Lexend" '
        'w:cs="Lexend" w:eastAsiaTheme="minorEastAsia"/><w:sz w:val="22"/>'
        '<w:szCs w:val="22"/><w:lang w:val="es-MX" w:eastAsia="en-US" '
        'w:bidi="ar-SA"/></w:rPr></w:rPrDefault>',
        x, count=1, flags=re.S).encode("utf8")

# --------------------------------------------------------------------------
class Documento(object):
    """Documento formal de MLR sobre la hoja membretada calibrada."""

    def __init__(self, titulo, cliente, fecha, saludo,
                 firmantes=FIRMANTES_MLR, plantilla=None, folio=True):
        if isinstance(titulo, str):
            titulo = [titulo]
        if len(titulo) > 2:
            raise ValueError("El titulo no pasa de dos renglones. Si no cabe a 42 pt "
                             "—unos 20 caracteres por renglon— se acorta el titulo, "
                             "no se baja el tamano.")
        self.src = plantilla or _busca_plantilla()
        self.folio = folio
        self.b = []
        for i, t in enumerate(titulo):
            ultimo = (i == len(titulo) - 1)
            holgura = (HOLGURA_DESCENDENTE
                       if ultimo and DESCENDENTES & set(t.lower()) else 0)
            self.b.append(par(run(t, fam=XBOLD, color=TEAL, sz=SZ_TITULO),
                              before=(K_TITULO if i == 0 else 0), after=holgura,
                              jc="center", line=L_TITULO))
        self.titulo_con_descendente = bool(DESCENDENTES & set(titulo[-1].lower()))
        self.b.append(par(run(firmantes, fam=SEMI, color=TEAL, sz=SZ_FIRMANTES),
                          before=K_FIRMANTES, after=320, jc="center", line=L_FIRMANTES))
        # Solo dos metadatos. Nueve etiquetas es lo que direccion rechazo.
        self.metadato("Cliente", cliente)
        self.metadato("Fecha", fecha)
        self.b.append(par(run(saludo, fam=XBOLD, color=TEAL, sz=SZ_SALUDO),
                          before=K_SALUDO, after=0, jc="left", line=L_SALUDO))

    # -- bloques ----------------------------------------------------------
    def metadato(self, etiqueta, valor):
        self.b.append(par(run(etiqueta + ":", fam=SEMI, color=TEAL, sz=SZ_META)
                          + "<w:r><w:tab/></w:r>"
                          + run(valor, fam=SEMI, sz=SZ_META),
                          after=K_META, ind=IND_META, jc="left",
                          line=L_META, tab=TAB_META))

    def parrafo(self, texto, before=0, after=A_CUERPO, keep=False):
        self.b.append(par(run(texto, fam=REG), before=before, after=after,
                          line=L_CUERPO, keep=keep))

    def seccion(self, titulo):
        """Encabezado numerado. keepNext + keepLines: nunca se queda solo al pie."""
        self.b.append(par(run(titulo, fam=XBOLD, color=TEAL, sz=SZ_SECCION),
                          before=B_SECCION, after=A_SECCION, jc="left",
                          keep=True, juntas=True))

    def vinetas(self, textos):
        """Guion simple, una o dos lineas por vineta. Sin topo teal y sin
        entradilla en negritas seguida de parrafo."""
        for t in textos:
            self.b.append(par(run("-", fam=REG) + "<w:r><w:tab/></w:r>"
                              + run(t, fam=REG),
                              after=A_VINETA, line=L_VINETA,
                              ind=IND_VINETA, colgante=COLGANTE_VINETA,
                              tab=IND_VINETA))

    def nota(self, texto, destacada=False):
        self.b.append(par(run(texto, fam=(XBOLD if destacada else REG),
                              color=(TEAL if destacada else GRIS), sz=SZ_NOTA),
                          after=A_NOTA, line=L_NOTA))

    def cuadro(self, cabecera, filas, anchos, ultima_columna_negrita=True, entero=True):
        """Cuadro de cifras. `entero=True` pone keepNext en todas las filas menos
        la ultima, de modo que la tabla no se parte entre planas. Si eso deja un
        hueco grande, NO se mete un salto: se acorta el texto de las celdas."""
        if len(cabecera) != len(anchos):
            raise ValueError("cabecera y anchos no coinciden")

        def celda(txt, w, cab=False, ultima=False, centro=True, pega=False):
            gordo = cab or (ultima and ultima_columna_negrita)
            r = run(txt, fam=(XBOLD if gordo else REG),
                    color=(BLANCO if cab else None),
                    sz=(SZ_CAB_CUADRO if cab else SZ_CUERPO))
            kn = "<w:keepNext/>" if pega else ""
            p = ('<w:p><w:pPr>%s<w:spacing w:before="40" w:after="40"/>'
                 '<w:jc w:val="%s"/></w:pPr>%s</w:p>'
                 % (kn, "center" if centro else "left", r))
            bd = "<w:tcBorders>" + "".join(
                '<w:%s w:val="single" w:sz="4" w:space="0" w:color="%s"/>' % (s, TEAL)
                for s in ("top", "left", "bottom", "right")) + "</w:tcBorders>"
            sh = '<w:shd w:val="clear" w:fill="%s"/>' % TEAL if cab else ""
            return ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s%s'
                    '<w:vAlign w:val="center"/></w:tcPr>%s</w:tc>' % (w, bd, sh, p))

        o = ('<w:tbl><w:tblPr><w:tblW w:w="%d" w:type="dxa"/><w:jc w:val="center"/>'
             '<w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid>%s</w:tblGrid>'
             % (sum(anchos), "".join('<w:gridCol w:w="%d"/>' % w for w in anchos)))
        o += "<w:tr><w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>" + "".join(
            celda(c, w, cab=True, pega=entero) for c, w in zip(cabecera, anchos)) + "</w:tr>"
        for j, f in enumerate(filas):
            pega = entero and j < len(filas) - 1
            o += "<w:tr><w:trPr><w:cantSplit/></w:trPr>" + "".join(
                celda(c, w, ultima=(i == len(f) - 1), centro=(i != 0), pega=pega)
                for i, (c, w) in enumerate(zip(f, anchos))) + "</w:tr>"
        self.b.append(o + "</w:tbl>" + par("", after=0))

    def cierre(self, texto=CORTESIA, before=40):
        """Parrafo de cortesia. El bloque de contacto lo anade guarda()."""
        self.b.append(par(run(texto, fam=REG), before=before, after=0, line=L_CUERPO))

    # -- ensamblado -------------------------------------------------------
    def guarda(self, destino):
        src = zipfile.ZipFile(self.src)
        doc = src.read("word/document.xml").decode("utf8")
        cab = doc[:doc.index("<w:body>") + len("<w:body>")]
        cuerpo_tpl = doc[doc.index("<w:body>") + len("<w:body>"):doc.index("<w:sectPr")]
        sect = re.search(r"<w:sectPr.*?</w:sectPr>", doc, re.S).group(0)
        sect = re.sub(r"<w:pgMar[^>]*/>", PGMAR, sect, count=1)

        # Parrafo que ancla el bloque de contacto: se conserva intacto.
        fin = cuerpo_tpl[cuerpo_tpl.rindex("<w:p ", 0, cuerpo_tpl.index("<w:drawing>")):]
        # La plantilla trae <w:spacing> despues de <w:rPr> dentro de <w:pPr>, orden
        # que el esquema no admite. Word lo tolera; otros motores ignoran el alto
        # exacto de 2" y mandan el bloque de contacto a una plana nueva.
        mp = re.search(r"<w:pPr>(.*?)</w:pPr>", fin, re.S)
        if mp:
            dentro = mp.group(1)
            def saca(etq):
                mm = re.search(r"<w:%s\b[^>]*(?:/>|>.*?</w:%s>)" % (etq, etq), dentro, re.S)
                return mm.group(0) if mm else ""
            # CT_PPrBase exige este orden; con jc antes de spacing Word rechaza el archivo
            fin = fin.replace(mp.group(0), "<w:pPr>" + saca("spacing") + saca("ind")
                              + saca("jc") + saca("rPr") + "</w:pPr>")

        extras = {}
        if self.folio:
            rid = "rIdPie"
            sect = sect.replace('<w:pgSz',
                '<w:footerReference w:type="default" r:id="%s"/><w:pgSz' % rid, 1)
            extras["word/footer1.xml"] = _pie_con_folio()

        ft, ftrels, settings, fuentes = _incrusta(
            src.read("word/fontTable.xml"),
            src.read("word/_rels/fontTable.xml.rels"),
            src.read("word/settings.xml"))

        os.makedirs(os.path.dirname(os.path.abspath(destino)), exist_ok=True)
        with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
            for it in src.infolist():
                n = it.filename
                if n == "word/document.xml":
                    z.writestr(it, cab + "".join(self.b) + fin + sect
                               + "</w:body></w:document>")
                elif n == "word/styles.xml":
                    z.writestr(it, _lexend_por_defecto(src.read(n)))
                elif n == "word/fontTable.xml":
                    z.writestr(it, ft)
                elif n == "word/_rels/fontTable.xml.rels":
                    z.writestr(it, ftrels)
                elif n == "word/settings.xml":
                    z.writestr(it, settings)
                elif n == "word/_rels/document.xml.rels" and self.folio:
                    z.writestr(it, src.read(n).decode("utf8").replace(
                        "</Relationships>",
                        '<Relationship Id="rIdPie" Type="http://schemas.openxml'
                        'formats.org/officeDocument/2006/relationships/footer" '
                        'Target="footer1.xml"/></Relationships>').encode("utf8"))
                elif n == "[Content_Types].xml":
                    z.writestr(it, _declara_tipos(src.read(n), fuentes.keys(), self.folio))
                else:
                    z.writestr(it, src.read(n))
            for n, d in list(extras.items()) + list(fuentes.items()):
                z.writestr(n, d)
        src.close()
        return destino


def _pie_con_folio():
    """Las plantillas no traen footer. El pie ya esta calibrado a 1512 tw, que
    situa el folio entre el fin del texto y el lema impreso."""
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<w:p><w:pPr><w:jc w:val="right"/><w:spacing w:after="0"/></w:pPr>'
            '<w:r><w:rPr><w:rFonts w:ascii="Lexend" w:hAnsi="Lexend"/>'
            '<w:sz w:val="14"/><w:color w:val="%s"/></w:rPr></w:r>'
            '<w:fldSimple w:instr=" PAGE "><w:r><w:rPr>'
            '<w:rFonts w:ascii="Lexend" w:hAnsi="Lexend"/><w:sz w:val="14"/>'
            '<w:color w:val="%s"/></w:rPr><w:t>1</w:t></w:r></w:fldSimple>'
            '</w:p></w:ftr>' % (GRIS, GRIS)).encode("utf8")

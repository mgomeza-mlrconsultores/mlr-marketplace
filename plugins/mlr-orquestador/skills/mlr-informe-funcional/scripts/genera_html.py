# -*- coding: utf-8 -*-
"""HTML version of an MLR functional guide, from the same contenido.py as the Word.

    python3 genera_html.py <carpeta_con_contenido_y_capturas> <salida.html> [datos.json]

Format approved by management (Reciservicios, 11-sep-2026): one idea per sheet,
headline as conclusion, Archivo + IBM Plex Mono, teal/red/amber/mist palette,
figure.shot + lightbox, dark mode, print at 13.333 x 7.5 in. On top of it, the
firm's deck bar: vector logo, group menu built from data-nav, progress bar,
counter, keyboard navigation and theme button. Self-contained: captures are
embedded as data URIs and fonts fall back to local families without internet.
"""
import base64, html, os, sys, json, re, importlib.util

E = lambda t: html.escape(t, quote=True)
FIRMA = [("Director General", "direccionjm@mlrconsultores.com", "55 6302 8143"),
         ("Directora Comercial", "m.arellano@mlrconsultores.com", "55 8772 9395"),
         ("MLR Consultores", "mlrconsultores.com", "Calle Eugenia 830, Col. Del Valle, C.P. 03100, Ciudad de México")]
CIERRE = "Quedamos atentos a sus comentarios y esperamos contar con su aprobación para definir los siguientes pasos."
LEMA = "Contadores que sí le entienden a Odoo"

LOGO_DARK = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 200" role="img" aria-label="MLR Consultores"><g><rect x="10" y="14" width="172" height="172" rx="6" fill="rgba(255,255,255,0.12)" stroke="#FFFFFF" stroke-width="2"/><rect x="26" y="30" width="140" height="140" fill="none" stroke="#FFFFFF" stroke-width="4"/><path d="M50 150 L50 64 L96 116 L142 64 L142 150" fill="none" stroke="#FFFFFF" stroke-width="9" stroke-linejoin="miter"/><path d="M74 150 L74 92 M74 150 L104 150" fill="none" stroke="#FFFFFF" stroke-width="9"/><path d="M118 150 L118 92 L134 92 Q146 92 146 104 Q146 116 134 116 L118 116 M130 116 L146 150" fill="none" stroke="#FFFFFF" stroke-width="8"/></g><text x="208" y="104" font-family="Oswald, Archivo, 'DejaVu Sans', sans-serif" font-weight="700" font-size="62" letter-spacing="6" fill="#FFFFFF">MLR</text><text x="210" y="140" font-family="Oswald, Archivo, 'DejaVu Sans', sans-serif" font-weight="600" font-size="27" letter-spacing="7" fill="#EAF1F2">CONSULTORES</text><text x="211" y="164" font-family="Inter, 'DejaVu Sans', sans-serif" font-weight="400" font-size="13" letter-spacing="1.2" fill="#CFE0E2">CONSULTORÍA FISCAL ESPECIALIZADA</text></svg>'''


CSS = r'''
:root{--teal:#22646E;--teal-d:#16313A;--teal-m:#4A97A8;--mist:#7EBFC9;--brown:#452E27;--amber:#9A6614;--red:#B03A2B;--ok:#2E7D5B;
--ink:#1F2A2E;--muted:#5A6B6E;--line:#DCE7EA;--paper:#FFFFFF;--bg:#F4F8F9;--soft:#E9F1F3;--hd:62px;
--f-head:'Archivo','Oswald','DejaVu Sans',system-ui,sans-serif;--f-body:'Archivo','Inter','DejaVu Sans',system-ui,sans-serif;--f-mono:'IBM Plex Mono','DejaVu Sans Mono',ui-monospace,monospace;
--e1:0 1px 1px rgba(22,49,58,.06),0 4px 10px rgba(22,49,58,.07),0 18px 40px rgba(22,49,58,.08)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--ink:#E3EEF0;--muted:#9FB5BA;--line:#2A4550;--paper:#12252C;--bg:#0C1A1F;--soft:#16323A;
--e1:0 1px 1px rgba(0,0,0,.3),0 6px 16px rgba(0,0,0,.35)}}
:root[data-theme="dark"]{--ink:#E3EEF0;--muted:#9FB5BA;--line:#2A4550;--paper:#12252C;--bg:#0C1A1F;--soft:#16323A;--e1:0 1px 1px rgba(0,0,0,.3),0 6px 16px rgba(0,0,0,.35)}
*{box-sizing:border-box}html{scroll-snap-type:y proximity;scroll-padding-top:var(--hd)}
body{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.6 var(--f-body)}
header.nav{position:fixed;inset:0 0 auto 0;height:var(--hd);background:var(--teal-d);color:#fff;z-index:20;box-shadow:0 1px 0 rgba(255,255,255,.06) inset,0 8px 24px rgba(0,0,0,.18)}
.bar{max-width:1320px;margin:0 auto;height:100%;display:flex;align-items:center;gap:18px;padding:0 20px}
.brand{display:flex;align-items:center;gap:12px;min-width:0}.brand svg{height:38px;width:auto;flex:none}
.brand span{font:500 12px/1.2 var(--f-mono);letter-spacing:.06em;text-transform:uppercase;color:#CFE0E2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#navbtns{margin-left:auto;display:flex;gap:4px;overflow-x:auto;scrollbar-width:none}
#navbtns button{font:600 13px/1 var(--f-head);letter-spacing:.02em;color:#DCEBEE;background:transparent;border:1px solid transparent;border-radius:999px;padding:9px 14px;cursor:pointer;white-space:nowrap}
#navbtns button:hover{background:rgba(255,255,255,.08)}#navbtns button.act{background:#fff;color:var(--teal-d)}
#progress{position:absolute;left:0;bottom:0;height:3px;background:var(--mist);width:0;transition:width .15s linear}
#pgtxt{font:500 12px var(--f-mono);color:#9FC3CA;min-width:64px;text-align:right}
#theme{background:none;border:1px solid rgba(255,255,255,.25);color:#fff;border-radius:8px;padding:6px 9px;cursor:pointer;font:500 12px var(--f-mono)}
.sheet{scroll-snap-align:start;min-height:calc(100vh - var(--hd));padding:calc(var(--hd) + 28px) 20px 36px;display:flex;align-items:center}
.sheet:first-child{padding-top:calc(var(--hd) + 20px)}
.wrap{width:100%;max-width:1320px;margin:0 auto;background:var(--paper);border-radius:14px;box-shadow:var(--e1);padding:34px 44px 38px;position:relative;overflow:hidden;
border-top:1px solid rgba(255,255,255,.5)}
.wrap::after{content:"";position:absolute;left:0;right:0;bottom:0;height:6px;background:linear-gradient(90deg,var(--teal) 0 62%,var(--mist) 62% 100%)}
.topline{display:flex;justify-content:space-between;gap:16px;font:500 11.5px/1 var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:22px}
.topline span:first-child{color:var(--teal-m);font-weight:600}
h1,h2,h3{font-family:var(--f-head);margin:0}
h2{font-size:clamp(26px,3.1vw,40px);line-height:1.08;font-weight:800;font-stretch:78%;letter-spacing:-.01em;color:var(--teal);margin-bottom:16px;max-width:22ch}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) h2{color:var(--mist)}}:root[data-theme="dark"] h2{color:var(--mist)}
h3{font-size:15px;text-transform:uppercase;letter-spacing:.06em;color:var(--brown);margin:14px 0 6px}
p{margin:0 0 12px;max-width:68ch;text-align:left}
.grid2{display:grid;grid-template-columns:1fr;gap:28px}
.split .grid2{grid-template-columns:minmax(300px,5fr) 7fr;align-items:start}
.figs{display:grid;gap:14px}.figs.n2,.figs.n3,.figs.n4{grid-template-columns:1fr 1fr}.figs.n3 figure:first-child{grid-column:1/-1}.figs.n2 figcaption,.figs.n3 figure:not(:first-child) figcaption,.figs.n4 figcaption{font-size:11.5px}
figure.shot{margin:0;background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:8px;cursor:zoom-in;box-shadow:var(--e1);transition:transform .15s ease}
figure.shot:hover,figure.shot:focus{transform:translateY(-2px);outline:none;border-color:var(--mist)}
figure.shot img{display:block;width:100%;height:auto;border-radius:6px;border:1px solid #BFD4DA}
.figs.n1 figure.shot img{width:auto;max-width:100%;max-height:calc(100vh - var(--hd) - 250px);margin:0 auto;object-fit:contain}
@media print{.figs.n1 figure.shot img{max-height:5.2in}}
figure.shot figcaption{font:400 12.5px/1.45 var(--f-body);color:var(--muted);padding:8px 4px 2px}
figure.shot figcaption b{color:var(--teal-m)}
.ph{display:grid;place-items:center;aspect-ratio:16/9;border:1px dashed var(--mist);border-radius:6px;color:var(--muted);font:500 13px var(--f-mono)}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:18px 0 20px}
.kpi{background:var(--soft);border-radius:10px;padding:16px 16px 14px;border-left:3px solid var(--teal)}
.big{display:block;font:800 clamp(40px,5vw,64px)/1 var(--f-head);font-stretch:70%;color:var(--teal)}
.lbl{display:block;font-size:13px;color:var(--muted);margin-top:8px;line-height:1.35}
ol.flow{list-style:none;counter-reset:f;display:grid;grid-template-columns:repeat(6,1fr);gap:0;padding:0;margin:18px 0 22px}
ol.flow li{counter-increment:f;position:relative;padding:40px 12px 12px;border-top:3px solid var(--teal);font-size:13px;line-height:1.35}
ol.flow li::before{content:counter(f);position:absolute;top:-17px;left:10px;width:30px;height:30px;border-radius:50%;background:var(--teal);color:#fff;display:grid;place-items:center;font:700 14px var(--f-head);box-shadow:0 0 0 4px var(--paper)}
ol.flow li b{display:block;font:700 15px var(--f-head);color:var(--ink)}ol.flow li span{color:var(--muted)}
ol.flow li:nth-child(5){border-top-color:var(--brown)}ol.flow li:nth-child(5)::before{background:var(--brown)}
ul.dash{list-style:none;padding:0;margin:6px 0 0;max-width:72ch}ul.dash li{position:relative;padding:0 0 9px 22px}ul.dash li::before{content:"–";position:absolute;left:4px;color:var(--teal-m);font-weight:700}
table.grid{width:100%;border-collapse:collapse;font-size:14px;margin:8px 0 16px}
table.grid th{background:var(--teal);color:#fff;text-align:left;font:700 12.5px var(--f-head);letter-spacing:.04em;text-transform:uppercase;padding:10px 12px}
table.grid td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}
table.grid tbody tr:nth-child(even){background:var(--bg)}table.grid td:first-child{font-weight:600;color:var(--teal)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) table.grid td:first-child{color:var(--mist)}}
td.res{white-space:nowrap}td.res::before{content:"";display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:8px;background:var(--ok)}td.res.pend::before{background:var(--amber)}
.cover .wrap{background:radial-gradient(120% 140% at 85% 10%,#2B7482 0%,var(--teal) 35%,var(--teal-d) 100%);color:#fff;padding:54px 56px 60px}
.cover .wrap::after{background:linear-gradient(90deg,var(--mist) 0 38%,rgba(255,255,255,.35) 38% 100%)}
.cover-logo svg{height:74px;width:auto}.cover-logo.sm svg{height:52px}
.kicker{font:500 12.5px var(--f-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--mist);margin:34px 0 12px}
.cover h1{font-size:clamp(34px,4.8vw,64px);line-height:1.02;font-weight:800;font-stretch:72%;max-width:20ch;letter-spacing:-.015em}
dl.meta{display:grid;grid-template-columns:repeat(5,auto);gap:10px 34px;margin:30px 0 26px;justify-content:start}
dl.meta dt{font:500 11px var(--f-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--mist)}dl.meta dd{margin:4px 0 0;font:600 15px var(--f-head)}
.cover .lead{color:#DCEBEE;max-width:78ch;font-size:15.5px}
.close .lead{font-size:20px;max-width:46ch;margin:26px 0 30px;color:#fff}
.contact{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;border-top:1px solid rgba(255,255,255,.2);padding-top:22px}
.contact div{display:flex;flex-direction:column;gap:3px;font-size:14px;color:#DCEBEE}.contact b{font:700 14px var(--f-head);color:#fff;text-transform:uppercase;letter-spacing:.05em}
.motto{font:700 18px var(--f-head);color:var(--mist);margin-top:30px;letter-spacing:.02em}
#lb{position:fixed;inset:0;background:rgba(8,20,24,.92);display:none;align-items:center;justify-content:center;flex-direction:column;z-index:50;padding:24px;cursor:zoom-out}
#lb.on{display:flex}#lb img{max-width:96vw;max-height:84vh;border-radius:8px;box-shadow:0 20px 60px rgba(0,0,0,.5);background:#fff}
#lb p{color:#DCEBEE;font-size:14px;margin-top:14px;max-width:90ch;text-align:center}#lb button{position:absolute;top:16px;right:20px;background:#fff;border:0;border-radius:999px;padding:8px 14px;font:700 13px var(--f-head);cursor:pointer}
@media (max-height:900px){.sheet{padding-top:calc(var(--hd) + 16px)}.wrap{padding:24px 34px 30px}h2{font-size:clamp(24px,2.6vw,34px)}}
@media (max-width:980px){.split .grid2{grid-template-columns:1fr}.kpis{grid-template-columns:repeat(2,1fr)}ol.flow{grid-template-columns:repeat(2,1fr);row-gap:26px}
dl.meta{grid-template-columns:repeat(2,auto)}.contact{grid-template-columns:1fr}.brand span{display:none}}
@media (max-width:560px){.wrap{padding:22px 18px 28px}.sheet{padding-left:10px;padding-right:10px}#pgtxt{display:none}}
@media print{@page{size:13.333in 7.5in;margin:0}header.nav,#lb{display:none}html{scroll-snap-type:none}
.sheet{min-height:7.5in;height:7.5in;padding:.3in;page-break-after:always;break-after:page}.wrap{box-shadow:none;height:100%}}
'''


JS = r'''
const groups=__GROUPS__;
const sheets=[...document.querySelectorAll('.sheet')];const nb=document.getElementById('navbtns');
groups.forEach(([g,i])=>{const b=document.createElement('button');b.textContent=g;b.onclick=()=>sheets[i].scrollIntoView({behavior:'smooth'});nb.appendChild(b)});
const btns=[...nb.children];let cur=0;
function mark(i){cur=i;let gi=0;groups.forEach(([g,s],k)=>{if(s<=i)gi=k});btns.forEach((b,k)=>b.classList.toggle('act',k===gi));
document.getElementById('pgtxt').textContent=String(i+1).padStart(2,'0')+' / '+String(sheets.length).padStart(2,'0');}
const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting&&e.intersectionRatio>.35)mark(sheets.indexOf(e.target))})},{threshold:[.35,.6]});
sheets.forEach(s=>io.observe(s));
addEventListener('scroll',()=>{const h=document.documentElement;document.getElementById('progress').style.width=(100*h.scrollTop/(h.scrollHeight-h.clientHeight||1))+'%'},{passive:true});
function go(d){const i=Math.max(0,Math.min(sheets.length-1,cur+d));sheets[i].scrollIntoView({behavior:'smooth'})}
addEventListener('keydown',e=>{if(lb.classList.contains('on')){if(e.key==='Escape')close();return}
if(['ArrowRight','PageDown'].includes(e.key)){e.preventDefault();go(1)}else if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();go(-1)}
else if(e.key==='Home'){e.preventDefault();sheets[0].scrollIntoView()}else if(e.key==='End'){e.preventDefault();sheets[sheets.length-1].scrollIntoView()}});
const lb=document.getElementById('lb'),lbi=lb.querySelector('img'),lbp=lb.querySelector('p');
function open(f){const im=f.querySelector('img');if(!im)return;lbi.src=im.src;lbp.textContent=f.dataset.cap;lb.classList.add('on')}
function close(){lb.classList.remove('on')}
document.querySelectorAll('figure.shot').forEach(f=>{f.addEventListener('click',()=>open(f));f.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open(f)}})});
lb.addEventListener('click',close);
document.getElementById('theme').onclick=()=>{const r=document.documentElement;const d=r.dataset.theme==='dark'||(!r.dataset.theme&&matchMedia('(prefers-color-scheme: dark)').matches);r.dataset.theme=d?'light':'dark'};
mark(0);
'''



def carga_contenido(carpeta):
    spec = importlib.util.spec_from_file_location("contenido", os.path.join(carpeta, "contenido.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class Hojas(object):
    def __init__(self, carpeta, C, datos):
        self.carpeta, self.C, self.datos, self.fign = carpeta, C, datos, {}

    def img(self, key):
        for ext in ("jpg", "png"):
            p = os.path.join(self.carpeta, "capturas", "%s.%s" % (key, ext))
            if os.path.exists(p):
                mime = "image/jpeg" if ext == "jpg" else "image/png"
                return "data:%s;base64,%s" % (mime, base64.b64encode(open(p, "rb").read()).decode())
        return None

    def figura(self, key, cap):
        # never loading="lazy": lazy images come out blank when the page is printed to PDF
        n = self.fign.setdefault(key, len(self.fign) + 1)
        src = self.img(key)
        inner = ('<img src="%s" alt="%s">' % (src, E(cap))) if src else \
                '<div class="ph">Captura %s pendiente</div>' % key
        return ('<figure class="shot" tabindex="0" data-cap="Figura %d. %s">%s'
                '<figcaption><b>Figura %d.</b> %s</figcaption></figure>' % (n, E(cap), inner, n, E(cap)))

    def bloque(self, b):
        k = b[0]
        if k == "p":
            t = self.datos.get("produccion", "") if b[1] == "__PRODUCCION__" else b[1]
            return "<p>%s</p>" % E(t)
        if k == "h":
            return "<h3>%s</h3>" % E(b[1])
        if k == "v":
            return '<ul class="dash">%s</ul>' % "".join("<li>%s</li>" % E(t) for t in b[1])
        if k == "fig":
            return self.figura(b[1], b[2])
        if k == "kpi":
            return '<div class="kpis">%s</div>' % "".join(
                '<div class="kpi"><span class="big">%s</span><span class="lbl">%s</span></div>' % (E(a), E(l))
                for a, l in b[1])
        if k == "flujo":
            return '<ol class="flow">%s</ol>' % "".join(
                "<li><b>%s</b><span>%s</span></li>" % (E(a), E(s)) for a, s in b[1])
        if k == "t":
            cab = b[1]
            filas = self.datos.get("pruebas", []) if b[2] == "__PRUEBAS__" else b[2]
            th = "".join("<th>%s</th>" % E(c) for c in cab)
            tr = "".join("<tr>%s</tr>" % "".join(
                '<td%s>%s</td>' % (' class="res %s"' % ("ok" if c.startswith("Correcto") else "pend")
                                   if (i == len(f) - 1 and len(cab) == 3) else "", E(c))
                for i, c in enumerate(f)) for f in filas)
            return '<table class="grid"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (th, tr)
        raise ValueError(k)

    def hoja(self, grupo, ceja, titular, cuerpo, figuras=(), cls=""):
        figs = "".join(figuras)
        lay = "split" if figuras else "solo"
        return ('<section class="sheet %s %s" data-nav="%s"><div class="wrap">'
                '<div class="topline"><span>%s</span><span>%s · Odoo</span></div>'
                '<div class="grid2"><div class="txt"><h2>%s</h2>%s</div>%s</div>'
                '</div></section>' % (lay, cls, E(grupo), E(ceja), E(self.C.CLIENTE), E(titular), cuerpo,
                                      ('<div class="figs n%d">%s</div>' % (len(figuras), figs)) if figs else ""))

    def seccion(self, bloques, grupo, ceja, titular):
        """Figures go to the right column; with no figures, tables go there."""
        figs = [b for b in bloques if b[0] == "fig"]
        der = figs or [b for b in bloques if b[0] == "t"]
        txt = [b for b in bloques if b not in der]
        return self.hoja(grupo, ceja, titular, "".join(self.bloque(b) for b in txt),
                         [self.bloque(b) for b in der], cls="step" if len(figs) < 3 else "step many")


PORTADA_HTML = ('<section class="sheet cover" data-nav="Inicio" data-bg="dark"><div class="wrap">'
                '<div class="cover-logo">%s</div><p class="kicker">%s</p><h1>%s</h1>'
                '<dl class="meta"><div><dt>Cliente</dt><dd>%s</dd></div>%s'
                '<div><dt>Plataforma</dt><dd>%s</dd></div><div><dt>Fecha</dt><dd>%s</dd></div>'
                '<div><dt>Emite</dt><dd>MLR Consultores</dd></div></dl><p class="lead">%s</p></div></section>')
CIERRE_HTML = ('<section class="sheet cover close" data-nav="%s" data-bg="dark"><div class="wrap">'
               '<div class="cover-logo sm">%s</div><p class="lead">%s</p><div class="contact">%s</div>'
               '<p class="motto">%s</p></div></section>')


def construye(carpeta, datos=None):
    C = carga_contenido(carpeta)
    H = Hojas(carpeta, C, datos or getattr(C, "DATOS", {}))
    T = getattr(C, "TITULARES", {})
    aten = getattr(C, "ATENCION", "")
    out = [PORTADA_HTML % (LOGO_DARK, E(C.PORTADA["kicker"]), E(C.PORTADA["titular"]), E(C.CLIENTE),
                           ('<div><dt>Atención</dt><dd>%s</dd></div>' % E(aten)) if aten else "",
                           E(getattr(C, "SISTEMA", "Odoo")), E(C.FECHA), E(C.INTRO))]
    for sid, menu, titulo, bloques in C.SECCIONES:
        num, _, nombre = titulo.partition(" ")
        num = num.rstrip(".")
        if any(b[0] == "h" for b in bloques):
            grupos, cur, previo = [], None, []
            for b in bloques:
                if b[0] == "h":
                    cur = [b[1], []]
                    grupos.append(cur)
                elif cur is None:
                    previo.append(b)
                else:
                    cur[1].append(b)
            if previo:
                out.append(H.seccion(previo, menu, "%s · %s" % (num, nombre), T.get(sid, nombre)))
            for h, bs in grupos:
                n = h.split(" ")[0]
                out.append(H.seccion(bs, menu, "Paso %s · %s" % (n, h[len(n) + 1:]), T.get(n, h[len(n) + 1:])))
        else:
            out.append(H.seccion(bloques, menu, "%s · %s" % (num, nombre), T.get(sid, nombre)))
    contacto = "".join("<div><b>%s</b><span>%s</span><span>%s</span></div>" % tuple(E(x) for x in f) for f in FIRMA)
    out.append(CIERRE_HTML % (E(C.SECCIONES[-1][1]), LOGO_DARK, E(CIERRE), contacto, E(LEMA)))
    return C, "\n".join(out)


PAGINA = ('<!doctype html><html lang="es-MX"><head><meta charset="utf-8">'
          '<meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title>'
          '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
          '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">'
          '<style>%s</style></head><body>'
          '<header class="nav"><div class="bar"><div class="brand">%s<span>%s</span></div>'
          '<nav id="navbtns" aria-label="Secciones"></nav><span id="pgtxt">01 / 01</span>'
          '<button id="theme" title="Cambiar tema claro u oscuro">Tema</button></div><div id="progress"></div></header>'
          '<main id="deck">%s</main>'
          '<div id="lb" role="dialog" aria-modal="true"><button type="button">Cerrar ✕</button><img alt=""><p></p></div>'
          '<script>%s</script></body></html>')


def pagina(carpeta, datos=None):
    C, cuerpo = construye(carpeta, datos)
    navs = re.findall(r'<section class="sheet[^"]*" data-nav="([^"]+)"', cuerpo)
    groups, seen = [], set()
    for i, g in enumerate(navs):
        if g not in seen:
            seen.add(g)
            groups.append([g, i])
    js = JS.replace("__GROUPS__", json.dumps(groups, ensure_ascii=False))
    return PAGINA % (E(C.TITULO_HTML), CSS, LOGO_DARK, E(C.BARRA), cuerpo, js)


if __name__ == "__main__":
    carpeta, out = sys.argv[1], sys.argv[2]
    datos = json.load(open(sys.argv[3], encoding="utf8")) if len(sys.argv) > 3 else None
    open(out, "w", encoding="utf8").write(pagina(carpeta, datos))
    print(out)

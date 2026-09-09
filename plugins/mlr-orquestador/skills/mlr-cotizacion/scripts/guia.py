# -*- coding: utf-8 -*-
"""Guía de la reunión de descubrimiento, en formato MLR."""
import sys, datetime
sys.path.insert(0, "/tmp/claude-0/-home-claude/e591a5e1-2d82-565a-89a1-461f10bb6a5f/scratchpad/skills/pkg/scripts")
sys.path.insert(0, "/tmp/claude-0/-home-claude/e591a5e1-2d82-565a-89a1-461f10bb6a5f/scratchpad/cuest")
from documento_mlr import Documento
import preguntas as Q

MESES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto",
         "septiembre","octubre","noviembre","diciembre"]
hoy = datetime.date(2026, 9, 9)
FECHA = "%d de %s de %d" % (hoy.day, MESES[hoy.month-1], hoy.year)

d = Documento(titulo=["Reunión de", "Descubrimiento"],
              cliente="Uso interno — equipo MLR Consultores",
              fecha=FECHA)

d.parrafo("Esta guía acompaña al libro de captura «Cuestionario de Descubrimiento Odoo - "
          "MLR.xlsx» y fija cómo se conduce la reunión de media hora de la que sale la "
          "cotización. El libro se llena en vivo, delante del cliente, y lo que no quede "
          "registrado ahí no se cotiza.", before=200)

d.seccion("1. Cómo se reparte la media hora")
d.parrafo("El recorrido obligatorio ocupa los 30 minutos completos y está calculado para "
          "que quepa. Los bloques marcados como núcleo se preguntan siempre y en este "
          "orden, porque cada uno condiciona al siguiente:")
nucleo = [(n, m) for _, n, m, nu, _ in Q.BLOQUES if nu]
d.cuadro(["Orden", "Bloque", "Minutos"],
         [["1", "Ficha del sistema", "5"]] +
         [[str(i + 2), n, str(m)] for i, (n, m) in enumerate(nucleo)] +
         [[str(len(nucleo) + 2), "Cierre y datos a migrar", "3"]] +
         [["", "Total", str(5 + sum(m for _, m in nucleo) + 3)]],
         [900, 5100, 1200])
d.parrafo("La contabilidad va primero y no al final. En México el comprobante fiscal, el "
          "catálogo de cuentas y el número de razones sociales condicionan la configuración "
          "de todo lo demás, y definirlos tarde obliga a rehacer trabajo ya hecho.")
d.parrafo("Los bloques restantes son condicionales y solo se abren si el cliente los "
          "menciona o si el alcance ya los contempla: fabricación, proyectos, servicio de "
          "campo, nómina, seguimiento comercial, punto de venta, comercio electrónico, "
          "mantenimiento, calidad, gastos, suscripciones y firma electrónica.")

d.seccion("2. Las cuatro preguntas que se repiten en cada aplicación")
d.parrafo("Todo bloque de aplicación arranca con la misma espina dorsal, porque son las "
          "cuatro respuestas que mueven el precio:")
d.vinetas([
    "Dónde vive hoy ese proceso, en una escala de cinco: no existe, en Excel o en papel, "
    "en otro sistema, en Odoo a medias, o en Odoo operando bien.",
    "Qué volumen manejan, en registros o documentos al mes, y cuántas personas lo tocan.",
    "Qué hay que migrar, desde dónde y con qué fecha de corte.",
    "Qué de todo eso no se resuelve como lo hace Odoo de fábrica. Esta es la pregunta que "
    "destapa el desarrollo, y es la que más se olvida.",
])
d.parrafo("Después de las cuatro vienen entre dos y seis preguntas propias de la aplicación. "
          "Si un bloque se pasa de su tiempo, se anota «profundizar» y se sigue: el detalle "
          "fino se define en la etapa de descubrimiento, que ya va cotizada.")

d.seccion("3. Lo que no se pregunta en la reunión")
d.parrafo("No se pregunta nada que se pueda resolver auditando la base por interfaz de "
          "programación una vez firmado el convenio de confidencialidad. Módulos instalados, "
          "campos personalizados, automatizaciones, volúmenes reales y estructura de "
          "compañías se leen, no se preguntan. Preguntar lo que uno mismo puede averiguar "
          "resta autoridad técnica y consume el tiempo de la reunión.")

d.seccion("4. Cuando la reunión corre con notas automáticas")
d.parrafo("Si la reunión se graba en Meet con Gemini tomando notas, quien conduce dice en "
          "voz alta el nombre del bloque antes de empezarlo, para que la transcripción quede "
          "segmentada por aplicación y después se pueda cruzar contra el libro de captura.")
d.parrafo("Las preguntas están redactadas para que la respuesta hablada se sostenga sola. "
          "Preguntar «¿en qué versión exacta de Odoo están?» hace que el cliente conteste "
          "«estamos en la 17.0», y esa línea sirve leída fuera de contexto. Preguntar «¿y de "
          "versión?» produce una nota inservible. Se leen como están escritas.")

d.seccion("5. Cómo se convierte el cuestionario en horas")
d.parrafo("La hoja de resumen del libro cuenta sola los detonantes de costo. La lectura es "
          "siempre la misma:")
d.vinetas(Q.DETONANTES)
d.parrafo("Con eso se arma la ruta por etapas y se calibra contra proyectos anteriores. Lo "
          "que quedó marcado como «profundizar» entra en la etapa de descubrimiento; lo que "
          "quedó como desarrollo se cotiza aparte y nunca como configuración.")

d.cierre("Cualquier pregunta que haga falta se agrega al libro de captura y no a una copia "
         "suelta, para que la siguiente reunión salga con la versión corregida.")
print(d.guarda("/mnt/user-data/outputs/Guía de Reunión de Descubrimiento - MLR.docx"))

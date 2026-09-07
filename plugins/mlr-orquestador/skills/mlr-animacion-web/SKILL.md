---
name: mlr-animacion-web
description: Anade movimiento profesional a paginas web, artifacts y tableros de MLR Consultores con criterio de estudio de diseno. Cargar cuando una pieza web lleve animacion, transicion, scroll con efecto o micro-interaccion.
---

# Animacion web MLR

## Herramienta por defecto: GSAP

Tras su adquisicion por Webflow es gratuita por completo, incluidos los plugins que antes eran de pago. Eso incluye ScrollTrigger, SplitText, MorphSVG y Flip, que son justamente las tecnicas que separan un resultado profesional de una plantilla.

Skills oficiales: `npx skills add https://github.com/greensock/gsap-skills`.

Si el proyecto es React o Next, Motion es la alternativa valida: sus muelles producen un ritmo fisicamente creible, lo contrario del suavizado de plantilla.

## Criterio

La animacion existe para explicar, no para adornar. Antes de animar algo, responde que informacion aporta ese movimiento. Si no aporta ninguna, no se anima.

## Reglas

- **Duracion**: entre 200 y 400 milisegundos para micro-interacciones; hasta 800 para transiciones de seccion. Por encima, la interfaz se siente lenta.
- **Curva**: nunca la lineal, nunca el suavizado simetrico por defecto. Salida rapida y entrada amortiguada.
- **Escalonado**: los elementos de una lista entran desfasados entre 40 y 80 milisegundos, no todos a la vez ni con retardos largos.
- **Origen coherente**: el movimiento parte del punto que lo provoca. Un panel que abre desde un boton nace en ese boton.
- **Una animacion protagonista por vista.** El resto acompana.
- **Respeta la preferencia de movimiento reducido** del sistema. Es accesibilidad, no un extra.

## Prohibido

- Rebotes exagerados y elasticidad en interfaces corporativas.
- Aparicion por desvanecimiento aplicada a todo por igual.
- Parallax en cada seccion.
- Contadores animados en cifras que no son el mensaje principal.
- Movimiento continuo en bucle que compite con la lectura.
- Animar propiedades que fuerzan recalculo de maquetacion. Trabajar sobre transformaciones y opacidad.

## Verificacion

Ver la pieza en movimiento antes de entregarla. Si en la segunda vista la animacion estorba, sobra.

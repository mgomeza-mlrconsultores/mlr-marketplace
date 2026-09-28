---
name: mlr-animacion-web
description: Añade movimiento profesional a páginas web, artifacts y tableros de MLR Consultores con criterio de estudio de diseño. Cargar cuando una pieza web lleve animación, transición, scroll con efecto o micro-interaccion.
---

# Animación web MLR

## Herramienta por defecto: GSAP

Tras su adquisición por Webflow es gratuita por completo, incluidos los plugins que antes eran de pago. Eso incluye ScrollTrigger, SplitText, MorphSVG y Flip, que son justamente las técnicas que separan un resultado profesional de una plantilla.

Skills oficiales: `npx skills add https://github.com/greensock/gsap-skills`.

Si el proyecto es React o Next, Motion es la alternativa valida: sus muelles producen un ritmo físicamente creíble, lo contrario del suavizado de plantilla.

## Criterio

La animación existe para explicar, no para adornar. Antes de animar algo, responde que información aporta ese movimiento. Si no aporta ninguna, no se anima.

## Reglas

- **Duración**: entre 200 y 400 milisegundos para micro-interacciones; hasta 800 para transiciones de sección. Por encima, la interfaz se siente lenta.
- **Curva**: nunca la lineal, nunca el suavizado simétrico por defecto. Salida rápida y entrada amortiguada.
- **Escalonado**: los elementos de una lista entran desfasados entre 40 y 80 milisegundos, no todos a la vez ni con retardos largos.
- **Origen coherente**: el movimiento parte del punto que lo provoca. Un panel que abre desde un botón nace en ese botón.
- **Una animación protagonista por vista.** El resto acompaña.
- **Respeta la preferencia de movimiento reducido** del sistema. Es accesibilidad, no un extra.

## Prohibido

- Rebotes exagerados y elasticidad en interfaces corporativas.
- Aparición por desvanecimiento aplicada a todo por igual.
- Parallax en cada sección.
- Contadores animados en cifras que no son el mensaje principal.
- Movimiento continuo en bucle que compite con la lectura.
- Animar propiedades que fuerzan recalculo de maquetación. Trabajar sobre transformaciones y opacidad.

## Verificación

Ver la pieza en movimiento antes de entregarla. Si en la segunda vista la animación estorba, sobra.

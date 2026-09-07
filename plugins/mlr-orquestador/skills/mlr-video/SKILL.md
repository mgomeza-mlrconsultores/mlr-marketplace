---
name: mlr-video
description: Produce video explicativo corporativo para MLR Consultores — recorridos de proceso, demostraciones de Odoo, animaciones de datos y piezas para presentaciones. Cargar ante cualquier peticion de generar, montar o animar video.
---

# Video MLR

Todo el flujo es gratuito y sin dependencia de servicios de pago.

## Herramienta por defecto: Motion Canvas

Licencia MIT, uso comercial sin restricciones ni umbrales de facturacion ni limite de personas. Esta pensada precisamente para contenido explicativo con control fino de la animacion, que es el caso de MLR.

Base tecnica: animacion por codigo sobre lienzo, con vista previa en vivo y exportacion de video.

**Alternativa: Remotion.** Composicion en React, ecosistema mayor y mejor para reutilizar capturas de Odoo como componentes. Su licencia no es libre: hay umbrales por facturacion de la empresa y por numero de personas, y las fuentes publicas no coinciden entre si. **Antes de usarla en un entregable facturable, verificar los terminos vigentes en la pagina de licencia de Remotion.** Si hay cualquier duda, Motion Canvas.

**Alternativa para contenido matematico: Manim.** MIT, gratuita. Mejor que las dos anteriores para animar formulas, algoritmos de planificacion o modelos de valoracion de inventario. Fuera de ese caso, no.

## Flujo de produccion

1. **Guion primero.** Redactarlo con `mlr-redaccion`. Un video sin guion aprobado no se produce.
2. **Material real.** Grabar la pantalla de Odoo con automatizacion de navegador en lugar de simular la interfaz. Una demostracion con capturas reales convence; una recreacion no.
3. **Composicion** con los tokens de `mlr-identidad-visual`.
4. **Montaje y audio** con FFmpeg, que es libre.
5. **Revision** viendo el render completo, nunca solo la vista previa.

## Reglas de forma

- Duracion objetivo entre 60 y 180 segundos. Por encima, dividir en capitulos.
- Una idea por escena. Transicion solo cuando cambia la idea.
- Texto en pantalla en la tipografia de la firma, nunca mas de siete palabras por rotulo.
- Ritmo sobrio. Nada de zooms nerviosos, barridos ni efectos de plantilla.
- Cierre con el membrete de la firma. Musica solo de fuente con licencia verificada, o sin musica.

## Animacion de datos

Usar la paleta y las reglas de la skill de visualizacion de datos. La cifra se anima desde cero solo cuando la magnitud es el mensaje; en los demas casos aparece completa.

## Cuando no usar video

Un proceso que se explica mejor en un diagrama estatico no lleva video. Antes de producir, confirmar que el movimiento aporta comprension y no solo vistosidad.

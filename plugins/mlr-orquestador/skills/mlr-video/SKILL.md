---
name: mlr-video
description: Produce video explicativo corporativo para MLR Consultores — recorridos de proceso, demostraciones de Odoo, animaciones de datos y piezas para presentaciones. Cargar ante cualquier petición de generar, montar o animar video.
---

# Video MLR

Todo el flujo es gratuito y sin dependencia de servicios de pago.

## Herramienta por defecto: Motion Canvas

Licencia MIT, uso comercial sin restricciones ni umbrales de facturación ni límite de personas. Está pensada precisamente para contenido explicativo con control fino de la animación, que es el caso de MLR.

Base técnica: animación por código sobre lienzo, con vista previa en vivo y exportación de video.

**Alternativa: Remotion.** Composición en React, ecosistema mayor y mejor para reutilizar capturas de Odoo como componentes. Su licencia no es libre: hay umbrales por facturación de la empresa y por número de personas, y las fuentes publicas no coinciden entre si. **Antes de usarla en un entregable facturable, verificar los términos vigentes en la página de licencia de Remotion.** Si hay cualquier duda, Motion Canvas.

**Alternativa para contenido matemático: Manim.** MIT, gratuita. Mejor que las dos anteriores para animar fórmulas, algoritmos de planificación o modelos de valoración de inventario. Fuera de ese caso, no.

## Flujo de producción

1. **Guion primero.** Redactarlo con `mlr-redaccion`. Un video sin guion aprobado no se produce.
2. **Material real.** Grabar la pantalla de Odoo con automatización de navegador en lugar de simular la interfaz. Una demostración con capturas reales convence; una recreación no.
3. **Composición** con los tokens de `mlr-identidad-visual`.
4. **Montaje y audio** con FFmpeg, que es libre.
5. **Revisión** viendo el render completo, nunca solo la vista previa.

## Reglas de forma

- Duración objetivo entre 60 y 180 segundos. Por encima, dividir en capítulos.
- Una idea por escena. Transición solo cuando cambia la idea.
- Texto en pantalla en la tipografía de la firma, nunca mas de siete palabras por rotulo.
- Ritmo sobrio. Nada de zooms nerviosos, barridos ni efectos de plantilla.
- Cierre con el membrete de la firma. Música solo de fuente con licencia verificada, o sin música.

## Animación de datos

Usar la paleta y las reglas de la skill de visualización de datos. La cifra se anima desde cero solo cuando la magnitud es el mensaje; en los demás casos aparece completa.

## Cuando no usar video

Un proceso que se explica mejor en un diagrama estático no lleva video. Antes de producir, confirmar que el movimiento aporta comprensión y no solo vistosidad.

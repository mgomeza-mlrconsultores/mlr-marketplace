---
name: mlr-diagramas-odoo
description: Produce diagramas de proceso, flujo, arquitectura, modelo de datos, secuencia y estados con la estética y la nomenclatura de la documentación técnica de ERP. Cargar ante cualquier petición de diagramar un proceso de negocio, un flujo de Odoo o una arquitectura de sistema.
---

# Diagramas MLR, estética ERP

## Punto de partida honesto

Odoo **no publica** un estándar de diagramas de flujo. Su documentación oficial es casi toda capturas de pantalla. Lo que si publica son reglas de nomenclatura de contenido. La convención de abajo toma esas reglas de nomenclatura y las combina con la paleta y la tipografía oficiales de MLR Consultores. **Al presentarla a un cliente, es la convención de diagramacion de MLR, nunca un estándar de Odoo.**

## Herramienta por defecto: Mermaid

Los artifacts renderizan Mermaid de forma nativa, sin cargar librerías. Va en texto plano, se versiona junto a la documentación y se entrega sin fricción.

Encabeza todo diagrama con este bloque de tema:

```
%%{init: {'theme':'base','themeVariables':{
  'primaryColor':'#24606C',
  'primaryTextColor':'#ffffff',
  'primaryBorderColor':'#18454E',
  'secondaryColor':'#452E27',
  'tertiaryColor':'#E6F3FB',
  'lineColor':'#6FA3AB',
  'fontFamily':'Inter, system-ui, sans-serif',
  'fontSize':'14px'
}}}%%
```

Reserva **D2** para flujos con muchos carriles que Mermaid no sepa organizar; exporta a SVG, PDF y PPTX. Reserva la pizarra tipo Excalidraw para co-disenar en reunión con el cliente; el entregable final siempre se pasa a Mermaid.

## Convención visual

- **Teal `#24606C`**: nodos del proceso principal, el camino feliz.
- **Café `#452E27`**: rutas alternativas y automatizaciones.
- **Teal medio `#6FA3AB`**: conectores y lineas.
- **Azul claro `#E6F3FB`**: relleno de nodos secundarios, estados terminales y sistemas de terceros.
- **Ámbar `#C9772E`** solo para señalar el punto donde ocurre el problema en un diagrama de diagnóstico. Un color de estado, no decorativo.
- **Sin degradados, sin sombras, sin volumen.** Un diagrama técnico no lleva efectos.
- **Rectángulos de esquina suave** para acciones y documentos. **Rombos** para decisiones. **Cilindros** para almacenamiento.
- **Inter** en todo el diagrama.
- Máximo tres colores por diagrama, mas el ámbar cuando haga falta marcar la falla.

## Nomenclatura de nodos

Derivada de las reglas de contenido de la documentación oficial de Odoo, con la paleta de MLR:

- **Modo imperativo y presente**: «Confirmar orden de venta», nunca «Confirmando la orden» ni «El usuario confirmara».
- **Sin pronombres**, especialmente segunda persona.
- **Sin preguntas** en los nodos de acción. Los rombos si formulan la condición en forma breve: «Stock disponible».
- **Mayúscula solo en la primera palabra** y en nombres propios.
- **Nombres de aplicación capitalizados**: Ventas, Inventario, Contabilidad. **Sustantivos comunes en minúscula**: orden de venta, lista de materiales.
- **Etiquetas de interfaz exactamente como aparecen en Odoo**, sin traducir por cuenta propia.
- **Nombres técnicos entre acentos graves** cuando el lector los necesita: `stock.move`, `picked`.

## Reglas de composición

- Un diagrama responde una pregunta. Si responde dos, son dos diagramas.
- Máximo doce nodos por vista. Por encima de eso, descomponer en subprocesos enlazados.
- Los carriles se usan cuando importa quien ejecuta cada paso, no por decoración.
- Toda flecha lleva etiqueta cuando la transición no es obvia.
- El flujo corre en una sola dirección dominante, de arriba abajo o de izquierda a derecha, nunca alternando.

## Nombres de archivo

Minúsculas, separadas por guion, descriptivas del contenido: `flujo-recepcion-mercancia.mmd`, `arquitectura-intercompany.mmd`.

## Verificación

- Cada nodo usa imperativo y presente.
- Ningún nodo excede una línea de texto.
- El diagrama muestra el mecanismo real con los nombres reales del proceso o del sistema. Un diagrama de cajas y flechas genéricas no aporta y no se entrega.
- Renderizarlo y mirarlo antes de entregarlo.

---
name: mlr-diagramas-odoo
description: Produce diagramas de proceso, flujo, arquitectura, modelo de datos, secuencia y estados con la estetica y la nomenclatura de la documentacion tecnica de ERP. Cargar ante cualquier peticion de diagramar un proceso de negocio, un flujo de Odoo o una arquitectura de sistema.
---

# Diagramas MLR, estetica ERP

## Punto de partida honesto

Odoo **no publica** un estandar de diagramas de flujo. Su documentacion oficial es casi toda capturas de pantalla. Lo que si publica son reglas de nomenclatura y una identidad de marca. La convencion de abajo se deriva de ambas. **Al presentarla a un cliente, declararla como convencion de MLR alineada a la identidad de Odoo, nunca como estandar oficial de Odoo.**

## Herramienta por defecto: Mermaid

Los artifacts renderizan Mermaid de forma nativa, sin cargar librerias. Va en texto plano, se versiona junto a la documentacion y se entrega sin friccion.

Encabeza todo diagrama con este bloque de tema:

```
%%{init: {'theme':'base','themeVariables':{
  'primaryColor':'#714B67',
  'primaryTextColor':'#ffffff',
  'primaryBorderColor':'#5A3C53',
  'secondaryColor':'#017E84',
  'tertiaryColor':'#F5F3F4',
  'lineColor':'#8F8F8F',
  'fontFamily':'Inter, system-ui, sans-serif',
  'fontSize':'14px'
}}}%%
```

Reserva **D2** para flujos con muchos carriles que Mermaid no sepa organizar; exporta a SVG, PDF y PPTX. Reserva la pizarra tipo Excalidraw para co-disenar en reunion con el cliente; el entregable final siempre se pasa a Mermaid.

## Convencion visual

- **Morado `#714B67`**: nodos del proceso principal, el camino feliz.
- **Verde azulado `#017E84`**: rutas alternativas y automatizaciones.
- **Gris `#8F8F8F`**: estados terminales, pasos externos y sistemas de terceros.
- **Relleno blanco o gris muy claro.** Sin degradados, sin sombras, sin volumen. Un diagrama tecnico no lleva efectos.
- **Rectangulos de esquina suave** para acciones y documentos. **Rombos** para decisiones. **Cilindros** para almacenamiento.
- **Inter** en todo el diagrama.
- Maximo tres colores por diagrama.

## Nomenclatura de nodos

Derivada de las reglas de contenido de la documentacion oficial de Odoo:

- **Modo imperativo y presente**: «Confirmar orden de venta», nunca «Confirmando la orden» ni «El usuario confirmara».
- **Sin pronombres**, especialmente segunda persona.
- **Sin preguntas** en los nodos de accion. Los rombos si formulan la condicion en forma breve: «Stock disponible».
- **Mayuscula solo en la primera palabra** y en nombres propios.
- **Nombres de aplicacion capitalizados**: Ventas, Inventario, Contabilidad. **Sustantivos comunes en minuscula**: orden de venta, lista de materiales.
- **Etiquetas de interfaz exactamente como aparecen en Odoo**, sin traducir por cuenta propia.
- **Nombres tecnicos entre acentos graves** cuando el lector los necesita: `stock.move`, `picked`.

## Reglas de composicion

- Un diagrama responde una pregunta. Si responde dos, son dos diagramas.
- Maximo doce nodos por vista. Por encima de eso, descomponer en subprocesos enlazados.
- Los carriles se usan cuando importa quien ejecuta cada paso, no por decoracion.
- Toda flecha lleva etiqueta cuando la transicion no es obvia.
- El flujo corre en una sola direccion dominante, de arriba abajo o de izquierda a derecha, nunca alternando.

## Nombres de archivo

Minusculas, separadas por guion, descriptivas del contenido: `flujo-recepcion-mercancia.mmd`, `arquitectura-intercompany.mmd`.

## Verificacion

- Cada nodo usa imperativo y presente.
- Ningun nodo excede una linea de texto.
- El diagrama muestra el mecanismo real con los nombres reales del proceso o del sistema. Un diagrama de cajas y flechas genericas no aporta y no se entrega.
- Renderizarlo y mirarlo antes de entregarlo.

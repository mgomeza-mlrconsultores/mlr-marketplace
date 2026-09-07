# Logotipo MLR en SVG

Version vectorial para piezas HTML. No depende de archivos externos y escala sin perdida.

## Version sobre fondo oscuro (barra superior y portada)

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 200" role="img" aria-label="MLR Consultores">
  <g>
    <rect x="10" y="14" width="172" height="172" rx="6" fill="rgba(255,255,255,0.12)" stroke="#FFFFFF" stroke-width="2"/>
    <rect x="26" y="30" width="140" height="140" fill="none" stroke="#FFFFFF" stroke-width="4"/>
    <path d="M50 150 L50 64 L96 116 L142 64 L142 150" fill="none" stroke="#FFFFFF" stroke-width="9" stroke-linejoin="miter"/>
    <path d="M74 150 L74 92 M74 150 L104 150" fill="none" stroke="#FFFFFF" stroke-width="9"/>
    <path d="M118 150 L118 92 L134 92 Q146 92 146 104 Q146 116 134 116 L118 116 M130 116 L146 150" fill="none" stroke="#FFFFFF" stroke-width="8"/>
  </g>
  <text x="208" y="104" font-family="Oswald, 'Archivo', 'DejaVu Sans', sans-serif" font-weight="700" font-size="62" letter-spacing="6" fill="#FFFFFF">MLR</text>
  <text x="210" y="140" font-family="Oswald, 'Archivo', 'DejaVu Sans', sans-serif" font-weight="600" font-size="27" letter-spacing="7" fill="#EAF1F2">CONSULTORES</text>
  <text x="211" y="164" font-family="Inter, 'Source Sans 3', 'DejaVu Sans', sans-serif" font-weight="400" font-size="13" letter-spacing="1.2" fill="#CFE0E2">CONSULTORÍA FISCAL ESPECIALIZADA</text>
</svg>
```

## Version sobre fondo claro

Misma geometria, sustituyendo los trazos y textos:

- `stroke="#FFFFFF"` pasa a `stroke="#24606C"`
- El relleno del cuadro exterior pasa a `rgba(36,96,108,0.08)`
- «MLR» y «CONSULTORES» en `fill="#24606C"`
- La bajada en `fill="#452E27"`

## Reglas

El monograma son tres trazos verticales tipo columnas. No alterar la geometria, los grosores ni el espaciado entre letras. Respetar el area de aislamiento equivalente a una pieza del isotipo.

Para piezas que no sean HTML, usar los PNG aprobados del manual en lugar de este SVG.

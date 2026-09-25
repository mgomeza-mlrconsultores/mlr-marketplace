# Capturas de Odoo para la guia funcional

Estandar de las figuras en Word: el de `mlr-identidad-visual` (en linea, centrada, keepNext con su pie, contorno 0.5 pt #BFD4DA, pie "Figura N." Lexend 9 pt #595959). Lo aplica `Documento.imagen()`.

## Que capturar

| Pantalla | Selector | Nota |
|---|---|---|
| Formulario completo con su historial | pagina entera (`body`) o `.o_action_manager` | incluye migas y botones de estado |
| Solo la hoja del formulario, a su altura natural | `.o_form_sheet` | para ver totales al pie sin desplazar |
| Lista con columnas | `.o_action_manager` | recortar el blanco de abajo |
| Menu desplegable abierto (Acciones) | `body` | el menu vive fuera de la vista; recortar despues |
| Asistente o mensaje | `.modal-content` | sin la pagina oscurecida detras |
| Historial (chatter) | `.o-mail-Chatter` | recortar el blanco de abajo |

Documentos reales de la base de pruebas, nunca datos inventados sobre la imagen.

## Metodo A: Chrome con la extension

`computer` con `screenshot` y `save_to_disk`. Llamar `tabs_context_mcp` justo antes de cada accion: el id de pestana cambia al navegar.

## Metodo B: panel de navegador de la app de escritorio

Sirve cuando la extension de Chrome no responde. Si el panel tiene sesion abierta en la base de pruebas:

1. `Claude_Browser__resize_window` a 1440x900. Con el panel oculto la vista mide 0x0 y Odoo no pinta.
2. Navegar al registro. Tomar una captura pequena (escala 0.2) para forzar el cuadro de animacion: OWL pinta en `requestAnimationFrame` y con el panel oculto no llega solo.
3. Cargar `scripts/captura_odoo.js` (guardado en `sessionStorage`) y llamar `__cap('NN', selector)`. Moverse con `__act({...})` dentro de Odoo para no recargar.
4. Desde la sesion en la nube, `descarga_capturas.py <carpeta>/capturas --rm` con la API key en variable de entorno.
5. Al terminar, `resize_window` con `preset: "desktop"`.

La captura del panel (`computer screenshot`) solo sirve para mirar, no guarda archivo, y ademas recorta a la parte visible del panel.

## Recortes

- Quitar el blanco sobrante abajo y a la derecha de forma automatica, comparando contra el color de fondo.
- Los recortes por coordenadas de una captura del panel no sirven para la imagen de `__cap`: la escala es distinta. Para un asistente, capturar el `.modal-content` en vez de recortar.
- Ocultar la franja roja de "base neutralizada"; `__cap` la retira.
- Formularios muy altos: componer cabecera + zona relevante en una sola imagen.

## Nombres

`capturas/01.jpg ... NN.jpg` en el orden en que aparecen en el texto. Al archivar en el PC: `<Cliente>/Capturas de Pantalla/AAAAMMDD/<Cliente>_<Tema>_Figura_NN.jpg`.

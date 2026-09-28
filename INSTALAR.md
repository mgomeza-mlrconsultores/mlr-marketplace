# Instalar el estándar MLR en tu Claude

Dos comandos la primera vez. Uno cada vez que haya versión nueva. Nada mas.

Funciona igual en Cowork y en Claude Code de escritorio: los comandos se escriben en el chat.

## Requisito previo

Ninguno. No hace falta cuenta de GitHub ni permisos.

En Claude Code de escritorio necesitas `git` instalado solo si instalas desde el repositorio; desde la unidad compartida no.

## Instalación, una sola vez

### Si trabajas en MLR: desde la unidad compartida

Es la vía recomendada. Trae ademas los originales que **no** están en el repositorio: la
cotización aprobada por dirección, que es el patrón de formato y redacción de la firma, y
las hojas membretadas calibradas.

```
/plugin marketplace add "G:\Unidades compartidas\MMLR 2025\Claude MLR\mlr-marketplace"
```

Si tu Google Drive monta la unidad en otra letra, ajusta la ruta.

### Desde fuera de MLR: desde el repositorio público

```
/plugin marketplace add mgomeza-mlrconsultores/mlr-marketplace
```

Trae el método y las fuentes, pero no los originales de marca ni el documento de
referencia, que no se publican.

```
/plugin install mlr-orquestador@mlr
/plugin install mlr-odoo@mlr
/plugin install mlr-design@mlr
```

También puedes escribir solo `/plugin`, entrar al catálogo `mlr` y activarlos desde ahí.

Instala los tres. `mlr-orquestador` es el que enruta todo; sin el, los otros dos se cargan pero nadie los llama en el momento correcto.

## Que queda instalado

**`mlr-orquestador`** — el estándar operativo. Al abrir cada sesión recupera las directrices vigentes, clasifica lo que pides y carga el flujo especializado en lugar de responder de forma genérica. Dentro trae diez skills: orquestación, memoria, redacción, identidad visual, cotización de proyectos Odoo, presentaciones, diagramas, video, animación web y actualización del entorno.

**`mlr-odoo`** — los agentes de personalización de Odoo: modelos, campos, vistas heredadas, acciones de servidor y automatizaciones, con verificación en navegador y captura, y el informe final en español.

**`mlr-design`** — skills de contenido, marketing y diseño.

## Actualizar

```
/plugin marketplace update mlr
```

Trae la última versión de los tres plugins. No hay que reinstalar ni desinstalar nada, y no se pierde configuración. Funciona igual instalado desde la unidad compartida o desde el repositorio.

Si quieres refrescar todos los catálogos que tengas, `/plugin marketplace update --all`.

## Publicar una versión nueva en la unidad compartida

Solo lo hace quien mantiene el estándar. Después de confirmar y subir los cambios al
repositorio, se refresca la copia de la unidad:

```
robocopy "C:\Users\mgome\Claude\mlr-marketplace" "G:\Unidades compartidas\MMLR 2025\Claude MLR\mlr-marketplace" /MIR /XD .git __pycache__
```

`/MIR` deja la copia idéntica al origen, y `/XD` excluye el historial de git y los archivos
temporales de Python. Los originales de marca —`assets/referencia/` y `assets/plantillas/`—
viven **solo** en la unidad, así que hay que reponerlos si `/MIR` los borra:

```
$a = "G:\Unidades compartidas\MMLR 2025\Claude MLR\mlr-marketplace\plugins\mlr-orquestador\skills\mlr-identidad-visual\assets"
New-Item -ItemType Directory -Force -Path "$a\referencia","$a\plantillas"
Copy-Item "G:\Unidades compartidas\MMLR 2025\Hoja Membretada\Cotizacion_Comband DTH_Maquila Nomina.pdf" "$a\referencia\Cotizacion aprobada por direccion.pdf" -Force
Copy-Item "C:\Users\mgome\Claude\Projects\MLR Odoo\Plantillas\Hoja Membretada MLR*.docx" "$a\plantillas\" -Force
Copy-Item "G:\Unidades compartidas\MMLR 2025\Hoja Membretada\Formato_Cotizacion_MLR.docx" "$a\plantillas\" -Force
```

## Primer arranque

La primera vez que el orquestador consulte la memoria en la nube, el navegador te pedirá autorizar el servidor. Es un gesto personal, se hace una sola vez y no se puede centralizar.

## Que NO viene en los plugins

Los plugins traen el **método**: como se trabaja, como se redacta, como se cotiza, como se entrega.

No traen el **contexto de los clientes** ni las correcciones acumuladas de cada proyecto. Eso vive en la memoria y en los documentos de proyecto de cada persona, y no se distribuye por el repositorio.

## Si algo no aparece

Comprueba que el catálogo esta dado de alta con `/plugin marketplace list`. Si `mlr` no sale, el primer comando no llego a completarse: vuelve a ejecutarlo.

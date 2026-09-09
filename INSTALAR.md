# Instalar el estandar MLR en tu Claude

Dos comandos la primera vez. Uno cada vez que haya version nueva. Nada mas.

Funciona igual en Cowork y en Claude Code de escritorio: los comandos se escriben en el chat.

## Requisito previo

Acceso de lectura al repositorio `mgomeza-mlrconsultores/mlr-marketplace`. Marcos lo concede desde GitHub. Si el repositorio es privado y no tienes acceso, el primer comando falla con un error de autenticacion: pidele el alta antes de seguir.

En Claude Code de escritorio hace falta ademas tener `git` con tus credenciales de GitHub ya configuradas, porque la descarga la hace tu maquina.

## Instalacion, una sola vez

```
/plugin marketplace add mgomeza-mlrconsultores/mlr-marketplace
```

```
/plugin install mlr-orquestador@mlr
/plugin install mlr-odoo@mlr
/plugin install mlr-design@mlr
```

Tambien puedes escribir solo `/plugin`, entrar al catalogo `mlr` y activarlos desde ahi.

Instala los tres. `mlr-orquestador` es el que enruta todo; sin el, los otros dos se cargan pero nadie los llama en el momento correcto.

## Que queda instalado

**`mlr-orquestador`** — el estandar operativo. Al abrir cada sesion recupera las directrices vigentes, clasifica lo que pides y carga el flujo especializado en lugar de responder de forma generica. Dentro trae diez skills: orquestacion, memoria, redaccion, identidad visual, cotizacion de proyectos Odoo, presentaciones, diagramas, video, animacion web y actualizacion del entorno.

**`mlr-odoo`** — los agentes de personalizacion de Odoo: modelos, campos, vistas heredadas, acciones de servidor y automatizaciones, con verificacion en navegador y captura, y el informe final en espanol.

**`mlr-design`** — skills de contenido, marketing y diseno.

## Actualizar

```
/plugin marketplace update mlr
```

Trae la ultima version de los tres plugins. No hay que reinstalar ni desinstalar nada, y no se pierde configuracion.

Si quieres refrescar todos los catalogos que tengas, `/plugin marketplace update --all`.

## Primer arranque

La primera vez que el orquestador consulte la memoria en la nube, el navegador te pedira autorizar el servidor. Es un gesto personal, se hace una sola vez y no se puede centralizar.

## Que NO viene en los plugins

Los plugins traen el **metodo**: como se trabaja, como se redacta, como se cotiza, como se entrega.

No traen el **contexto de los clientes** ni las correcciones acumuladas de cada proyecto. Eso vive en la memoria y en los documentos de proyecto de cada persona, y no se distribuye por el repositorio.

## Si algo no aparece

Comprueba que el catalogo esta dado de alta con `/plugin marketplace list`. Si `mlr` no sale, el primer comando no llego a completarse: casi siempre es falta de acceso al repositorio.

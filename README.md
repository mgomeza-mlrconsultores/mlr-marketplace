# Marketplace interno de MLR Consultores

Contiene todo el entorno de trabajo de la firma en un solo lugar. Se da de alta una vez por persona; a partir de ahi solo se actualiza.

## Qué contiene

- **mlr-orquestador** — El estándar operativo. Recupera contexto de cliente y directrices vigentes desde memoria en la nube al abrir cada sesión, enruta cada petición al flujo especializado y aplica las normas de la firma. Ocho módulos: orquestación, memoria, redacción, identidad visual, diagramas, video, animación web y actualización del entorno.
- **mlr-odoo** — Agentes y flujo para personalización de Odoo.
- **mlr-design** — Skills de contenido, marketing y diseño.

## Puesta en marcha, una sola vez

**Paso 1.** Subir el contenido de este paquete a un repositorio git privado de la organización. La ruta de ese repositorio es la dirección del marketplace.

**Paso 2.** Cada persona da de alta el marketplace y instala los tres plugins:

```
/plugin marketplace add <dirección-del-repositorio>
/plugin install mlr-orquestador@mlr
/plugin install mlr-odoo@mlr
/plugin install mlr-design@mlr
```

**Paso 3.** Pedir al asistente: «pon al día mi entorno MLR». La skill `mlr-actualizacion` se encarga del resto: conecta la memoria en la nube, instala las skills externas gratuitas y verifica que todo responda.

## Actualizaciones

Cuando se publica una versión nueva del estándar, nadie reinstala nada. Cada persona ejecuta:

```
/plugin marketplace update mlr
```

O simplemente pide al asistente que ponga al día su entorno MLR.

## Por qué un repositorio y no un archivo suelto

Un paquete suelto se instala una vez y queda congelado: para actualizarlo habría que volver a distribuirlo y que cada persona lo reinstale. Un marketplace en repositorio permite publicar una versión nueva en un solo sitio y que todo el equipo la reciba con una orden, conservando su configuración.

Si la organización no dispone de repositorio git, el paquete puede instalarse directamente como archivo, pero entonces cada actualización exige volver a distribuirlo.

## Costo

Cero. Todos los componentes son gratuitos o de licencia libre.

## Pendiente antes del despliegue

1. El membrete oficial en `MLR/00-Plantillas/` del Drive de la organización, en solo lectura para el equipo.
2. Confirmar los nombres de las tres subcarpetas de cliente.
3. Dar de alta la cuenta de memoria de la firma en su plan gratuito y crear el espacio con las primeras directrices.

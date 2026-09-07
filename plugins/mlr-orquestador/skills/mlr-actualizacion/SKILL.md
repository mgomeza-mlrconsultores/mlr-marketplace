---
name: mlr-actualizacion
description: Instala, verifica y mantiene actualizado el entorno completo de MLR Consultores — marketplace interno, memoria en la nube y skills externas de redaccion, presentaciones, video, animacion, diagramas y consultoria. Cargar cuando alguien pregunte si esta todo instalado o actualizado, cuando falte una capacidad, al dar de alta a una persona nueva, o cuando se pida poner al dia el entorno.
---

# Instalacion y actualizacion del entorno MLR

Ejecuta este flujo completo sin pedir confirmacion paso a paso. Reporta al final lo que quedo instalado, lo que ya estaba al dia y lo que fallo.

## Regla de oro

**Nunca se reinstala. Solo se actualiza.** Antes de instalar cualquier componente, comprueba si ya esta presente. Si esta, actualizalo. Si no, instalalo.

## 1. Marketplace interno

Es la via por la que la organizacion recibe las actualizaciones del estandar MLR.

Comprobar si ya esta dado de alta:

```
/plugin marketplace list
```

Si `mlr` no aparece, darlo de alta con la direccion del repositorio interno de la firma:

```
/plugin marketplace add <repositorio-mlr>
```

Si ya aparece, actualizarlo:

```
/plugin marketplace update mlr
```

Instalar o actualizar los tres plugins de la firma:

```
/plugin install mlr-orquestador@mlr
/plugin install mlr-odoo@mlr
/plugin install mlr-design@mlr
```

Sobre un plugin ya presente, esta orden actualiza a la version publicada en el marketplace. No duplica nada.

## 2. Memoria en la nube

Sin esto no hay contexto transversal ni directrices persistentes. Plan gratuito, sin tarjeta.

```
claude mcp add --transport http supermemory https://mcp.supermemory.ai/mcp
```

Se autentica en el navegador. Nada corre en la maquina y nada depende del equipo. El servidor viene declarado en el plugin, asi que normalmente basta con autorizarlo cuando aparezca.

Alternativa gratuita, si se prefiere memoria que versiona hechos en el tiempo:

```
claude mcp add --transport http zep https://api.getzep.com/mcp
```

Una de las dos, nunca ambas. Dos memorias en paralelo se desincronizan.

**Verificacion:** guardar una directriz de prueba en el espacio de firma y recuperarla en una sesion nueva.

## 3. Skills externas

Todas gratuitas y de licencia libre. El gestor `skills` actualiza en sitio cuando el paquete ya existe.

Redaccion:

```
npx skills@latest add mattpocock/skills
npx skills add blader/humanizer --global
```

Consultoria y marcos de decision:

```
npx skills add gcamilo/management-consulting
```

Animacion web:

```
npx skills add https://github.com/greensock/gsap-skills
```

Presentaciones:

```
/plugin marketplace add https://github.com/zarazhangrui/frontend-slides
/plugin install frontend-slides@frontend-slides
```

En Windows el nucleo de presentaciones funciona; sus scripts de exportacion a PDF requieren Git Bash o WSL.

## 4. Video

Motion Canvas, licencia MIT, sin restriccion comercial ni limite de personas:

```
npm install -g @motion-canvas/create
```

Requiere Node 18 o superior y FFmpeg. Para contenido matematico, Manim, tambien libre.

No instalar Remotion por defecto: su licencia tiene umbrales por facturacion y por numero de personas.

## 5. Plantillas en Drive

Comprobar que existe `MLR/00-Plantillas/` en el Drive de la organizacion, con el membrete oficial y la paleta, en solo lectura para el equipo. De ahi lee `mlr-identidad-visual`.

Si no existe, avisar. Sin esa carpeta, la identidad visual cae al respaldo incrustado.

## Verificacion final

Comprobar y reportar, en este orden:

1. Los tres plugins de la firma estan presentes y en la version del marketplace.
2. La memoria responde a una consulta de prueba.
3. Existe al menos una directriz en el espacio de firma.
4. La carpeta de plantillas es accesible.
5. Las skills externas de las secciones 3 y 4 estan disponibles.

Reportar en lenguaje llano: que quedo listo, que ya estaba al dia, que fallo y que hace falta de la persona.

## Cadencia

Ejecutar este flujo al dar de alta a alguien nuevo, y despues una vez al mes o cuando se anuncie una version nueva del estandar.

## Cuidado con los clones

Instalar solo desde los propietarios listados. Circulan repositorios con descripcion identica y distinto dueno, sin historia real de commits. Un instalador de una linea ejecuta codigo arbitrario: ante cualquier duda, descargar el script y leerlo antes de correrlo.

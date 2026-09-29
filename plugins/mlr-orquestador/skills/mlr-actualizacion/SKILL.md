---
name: mlr-actualizacion
description: Instala, verifica y mantiene actualizado el entorno completo de MLR Consultores — marketplace interno, memoria en la nube y skills externas de redacción, presentaciones, video, animación, diagramas y consultoría. Cargar cuando alguien pregunte si esta todo instalado o actualizado, cuando falte una capacidad, al dar de alta a una persona nueva, o cuando se pida poner al día el entorno.
---

# Instalación y actualización del entorno MLR

Ejecuta este flujo completo sin pedir confirmación paso a paso. Reporta al final lo que quedo instalado, lo que ya estaba al día y lo que fallo.

## Regla de oro

**Nunca se reinstala. Solo se actualiza.** Antes de instalar cualquier componente, comprueba si ya esta presente. Si esta, actualizalo. Si no, instalalo.

## 1. Marketplace interno

Es la vía por la que la organización recibe las actualizaciones del estándar MLR.

Comprobar si ya está dado de alta:

```
/plugin marketplace list
```

Si `mlr` no aparece, darlo de alta con la dirección del repositorio interno de la firma:

```
/plugin marketplace add <repositorio-mlr>
```

Si ya aparece, actualizarlo:

```
/plugin marketplace update mlr
```

Instalar o actualizar los cuatro plugins de la firma:

```
/plugin install mlr-orquestador@mlr
/plugin install mlr-odoo@mlr
/plugin install mlr-design@mlr
/plugin install mlr-contabilidad@mlr
```

Sobre un plugin ya presente, esta orden actualiza a la versión publicada en el marketplace. No duplica nada.

## 2. Memoria en la nube

Sin esto no hay contexto transversal ni directrices persistentes. Plan gratuito, sin tarjeta.

```
claude mcp add --transport http supermemory https://mcp.supermemory.ai/mcp
```

Se autentica en el navegador. Nada corre en la maquina y nada depende del equipo. El servidor viene declarado en el plugin, así que normalmente basta con autorizarlo cuando aparezca.

Alternativa gratuita, si se prefiere memoria que versiona hechos en el tiempo:

```
claude mcp add --transport http zep https://api.getzep.com/mcp
```

Una de las dos, nunca ambas. Dos memorias en paralelo se desincronizan.

**Verificación:** guardar una directriz de prueba en el espacio de firma y recuperarla en una sesión nueva.

## 3. Skills externas

Todas gratuitas y de licencia libre. El gestor `skills` actualiza en sitio cuando el paquete ya existe.

Redacción:

```
npx skills@latest add mattpocock/skills
npx skills add blader/humanizer --global
```

Consultoría y marcos de decisión:

```
npx skills add gcamilo/management-consulting
```

Animación web:

```
npx skills add https://github.com/greensock/gsap-skills
```

Presentaciones:

```
/plugin marketplace add https://github.com/zarazhangrui/frontend-slides
/plugin install frontend-slides@frontend-slides
```

En Windows el núcleo de presentaciones funciona; sus scripts de exportación a PDF requieren Git Bash o WSL.

## 4. Video

Motion Canvas, licencia MIT, sin restricción comercial ni límite de personas:

```
npm install -g @motion-canvas/create
```

Requiere Node 18 o superior y FFmpeg. Para contenido matemático, Manim, también libre.

No instalar Remotion por defecto: su licencia tiene umbrales por facturación y por número de personas.

## 5. Plantillas en Drive

Para la conciliación bancaria, comprobar además que la carpeta `MMLR 2025 > Hoja Membretada > Conciliación Bancaria` de la unidad compartida esté accesible, con sus dos plantillas. Sin ella, `mlr-conciliacion-bancaria` trabaja con las copias neutralizadas que trae el plugin. Revisar también que la máquina tenga Python con `openpyxl`, `lxml` y `pdfplumber`, y LibreOffice para recalcular el libro.


Comprobar que existe `MLR/00-Plantillas/` en el Drive de la organización, con el membrete oficial y la paleta, en solo lectura para el equipo. De ahí lee `mlr-identidad-visual`.

Si no existe, avisar. Sin esa carpeta, la identidad visual cae al respaldo incrustado.

## Verificación final

Comprobar y reportar, en este orden:

1. Los cuatro plugins de la firma están presentes y en la versión del marketplace.
2. La memoria responde a una consulta de prueba.
3. Existe al menos una directriz en el espacio de firma.
4. La carpeta de plantillas es accesible.
5. Las skills externas de las secciones 3 y 4 están disponibles.

Reportar en lenguaje llano: que quedo listo, que ya estaba al día, que fallo y que hace falta de la persona.

## Cadencia

Ejecutar este flujo al dar de alta a alguien nuevo, y después una vez al mes o cuando se anuncie una versión nueva del estándar.

## Cuidado con los clones

Instalar solo desde los propietarios listados. Circulan repositorios con descripción idéntica y distinto dueño, sin historia real de commits. Un instalador de una línea ejecuta código arbitrario: ante cualquier duda, descargar el script y leerlo antes de correrlo.

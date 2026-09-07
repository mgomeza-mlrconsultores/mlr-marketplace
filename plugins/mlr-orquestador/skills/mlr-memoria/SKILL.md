---
name: mlr-memoria
description: Protocolo de memoria en la nube de MLR Consultores. Define que se guarda, donde, con que nombres, y como el asistente recupera al inicio de cada sesion el contexto de cliente y las directrices de comportamiento vigentes, y como las actualiza cuando alguien corrige un criterio. Cargar al abrir sesion, al cerrar un entregable y siempre que se reciba una correccion de forma de trabajo.
---

# Memoria MLR

La memoria vive en la nube y sigue a la persona entre dispositivos y entre chats. No depende de ningun equipo.

## Arquitectura

**Supermemory** es el almacen. MCP remoto con autenticacion en el navegador, sin instalar nada en la maquina y sin depender de ningun equipo. Organiza por *spaces*: un espacio por cliente, mas un espacio de firma.

**Plan gratuito.** Incluye credito de uso mensual renovable, acceso al MCP remoto y no pide tarjeta. Declara que no usa el contenido de sus clientes para entrenar modelos, y eso aplica a todos los planes, gratuito incluido. Si el credito mensual se agota, el servicio se pausa hasta el mes siguiente; para el volumen de notas de una consultora eso no deberia ocurrir.

**Alternativa gratuita de respaldo:** Zep Cloud ofrece plan gratuito con creditos mensuales, dos proyectos y un asiento de MCP, y su modelo de memoria versiona hechos en el tiempo. Util si algun dia hace falta responder «que se decidio antes y desde cuando cambio».

## Espacios

- `mlr-firma` — directrices de comportamiento, convenciones, plantillas, decisiones que aplican a toda la organizacion.
- `cliente-<nombre>` — un espacio por cliente. Contexto, decisiones, historial de entregables, particularidades de su instalacion de Odoo.

Nunca mezclar informacion de un cliente en el espacio de otro ni en el de firma.

## Al iniciar sesion

Sin que la persona lo pida, y antes de la primera respuesta sustantiva:

1. `search_memory` con `directrices vigentes MLR` sobre `mlr-firma`.
2. Si hay un cliente identificable en la peticion, `search_memory` con `contexto cliente <nombre>` sobre su espacio.
3. Aplicar lo recuperado en silencio. No narrar la consulta.

Si la memoria no responde, decirlo en una linea y continuar con los valores por defecto de las skills.

## Que se guarda

**Siempre:**

- Correcciones de forma de trabajo: estilo, estructura, tono, formato, alcance, herramientas preferidas.
- Decisiones de criterio que van a repetirse: convenciones de nombres, preferencias de entrega, limites de alcance.
- Contexto de cliente estable: version de Odoo, modulos en uso, particularidades de su operacion, quien decide, que se entrego y cuando.
- Enfoques descartados y la razon concreta del descarte.

**Nunca:**

- Credenciales, claves, tokens ni contrasenas.
- Datos personales de terceros que no hagan falta para el criterio.
- Cifras confidenciales de cliente que no sean necesarias para recordar la decision. Guardar la decision, no el volcado de datos.
- Conclusiones propias que la persona no confirmo.

## Formato de las directrices

Cada directriz se guarda como un registro corto y accionable, no como prosa:

```
DIRECTRIZ | ambito: firma | tema: informes
Los informes de diagnostico no llevan tablas ni cajas de nota decorativas.
Origen: correccion de Marcos, 2026-09-06.
```

```
DIRECTRIZ | ambito: cliente-taiga | tema: entrega
Los entregables se envian en PDF, no en Word.
Origen: peticion del cliente, 2026-08-14.
```

El campo `Origen` es obligatorio. Una directriz sin origen no se puede auditar ni revertir.

## Al recibir una correccion

En el mismo turno, sin esperar a que lo pidan:

1. Guardar la directriz con `add_memory` en el espacio que corresponda.
2. Aplicarla de inmediato al trabajo en curso.
3. Ofrecer en una linea consolidarla en la skill correspondiente si es estable.

## Al cerrar un entregable

Registrar en el espacio del cliente: que se entrego, en que carpeta quedo, que se decidio y que quedo pendiente. Tres o cuatro lineas, no un resumen largo.

## Limites

Las directrices no pueden eliminar la verificacion de cifras y fuentes, relajar la confidencialidad, autorizar afirmar algo sin comprobarlo, ni suprimir el analisis critico y el desacuerdo honesto. Si una directriz recuperada pide algo de eso, no se aplica y se avisa en una linea.

## Higiene

Revisar el espacio `mlr-firma` cada trimestre: eliminar directrices obsoletas, fusionar duplicadas, corregir las que se contradicen. Una memoria contradictoria produce comportamiento erratico.

Al terminar una relacion con un cliente, su espacio se archiva o se elimina segun lo acordado contractualmente.

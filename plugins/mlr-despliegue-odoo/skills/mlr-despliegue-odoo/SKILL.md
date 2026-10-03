---
name: mlr-despliegue-odoo
description: >
  Esta skill debe usarse cuando se diga «dónde alojamos Odoo», «Odoo.sh o servidor», «instala Odoo», «servidor Linux»,
  «Docker», «la build falló», «subir de versión», «upgrade», «migrar la base», «respaldos», «restaurar», «está lento»,
  «se cae», «seguridad del servidor», «hardening», «base de prueba en Oracle Cloud» o cualquier decisión u operación de
  infraestructura de Odoo. Orquesta a los especialistas de despliegue.
metadata:
  version: "0.1.0"
---

# Despliegue y operación de Odoo

Los agentes de este plugin deciden, instalan, actualizan, protegen, respaldan y afinan la plataforma donde corre Odoo. Todo requisito y comando se verifica contra la documentación de la versión exacta antes de ejecutarse, y toda operación en producción exige respaldo etiquetado y ensayo previo.

## Enrutamiento
- Decidir plataforma, dimensionar, costear → `mlr-arquitecto-infraestructura`.
- Proyectos en Odoo.sh (repositorio, builds, staging, actualización) → `mlr-odoo-sh-especialista`.
- Servidores propios, contenedores, nube no gestionada, bases de prueba → `mlr-onpremise-linux`.
- Subir de versión con datos → `mlr-upgrade-version` (módulos propios con el plugin desarrollo-odoo).
- Seguridad y endurecimiento → `mlr-seguridad-hardening`.
- Respaldos y recuperación → `mlr-respaldo-recuperacion`.
- Lentitud e inestabilidad → `mlr-rendimiento-odoo`.

## Reglas
1. Nunca en producción sin respaldo etiquetado, ensayo en pruebas y ventana acordada.
2. Credenciales fuera de documentos, chats y repositorios; acceso por llaves y doble factor.
3. Bases de prueba neutralizadas y, si salen del perímetro del cliente, enmascaradas.
4. Medir antes de cambiar y volver a medir después; cada hallazgo cita su patrón D-xx.
5. Las tareas de infraestructura entran a la cotización con nombre de funcionalidad y horas, como cualquier otra.

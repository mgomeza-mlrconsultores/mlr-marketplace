---
name: mlr-desarrollo-odoo
description: >
  Esta skill debe usarse cuando se diga «programa un módulo», «diseña el módulo», «revisa este código», «migra los módulos
  a la 19», «¿sirve este módulo de la tienda?», «publicar en Odoo Apps», «licencia del módulo», «pruebas automáticas»,
  «widget», «componente OWL», «reporte QWeb», «API de Odoo», «XML-RPC», «JSON-2» o cualquier desarrollo, revisión o
  migración de código Odoo. Orquesta a los especialistas de desarrollo.
metadata:
  version: "0.1.0"
---

# Desarrollo Odoo con criterio senior

Los agentes de este plugin diseñan, programan, revisan, migran, prueban y empaquetan módulos. Toda firma de API se verifica en la rama exacta de la versión antes de escribir código; todo módulo nace con seguridad y pruebas; lo genérico se separa de lo específico del cliente para que pueda reutilizarse y venderse.

## Enrutamiento
- Antes de programar: alternativas, modelo, seguridad, plan → `arquitecto-modulos`.
- Python, modelos, lógica, informes, controladores → `desarrollador-backend`.
- Cliente web, OWL, punto de venta, sitio web → `desarrollador-frontend-owl`.
- Revisar código propio o de terceros → `revisor-codigo-senior`.
- Publicar y vender en la tienda → `empaquetador-apps-store`.
- Migrar módulos entre versiones → `migrador-modulos` (la base con datos la actualiza el plugin despliegue-odoo).
- Pruebas, reproducción de errores, aceptación → `qa-pruebas`.

## Reglas
1. Configuración antes que herencia, herencia antes que módulo nuevo; la decisión queda escrita.
2. Nada se entrega sin pruebas ejecutadas con salida visible ni sin revisión K-01 a K-16.
3. Licencia declarada en manifiesto y archivos; sin código Enterprise copiado; propiedad definida por contrato (plugin legal-mexico).
4. Sin datos ni identificadores de clientes en módulos genéricos.
5. Cada módulo registra qué revisar en la siguiente versión; la migración futura se estima desde el diseño.

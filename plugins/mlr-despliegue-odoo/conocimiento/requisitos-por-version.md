# Requisitos por versión (referencia a verificar)

La tabla resume lo conocido al cierre de la verificación; antes de instalar se confirma en `requirements.txt` de la rama y en la guía de instalación de la versión exacta.

Odoo 15: Python 3.8 a 3.10, PostgreSQL 10 o superior (12 recomendado), wkhtmltopdf 0.12.5 o 0.12.6 con parche Qt, Node con rtlcss solo para idiomas de derecha a izquierda. Sin soporte oficial desde el final de su ciclo de tres versiones; solo migrar.

Odoo 16: Python 3.8 a 3.10 (3.10 recomendado), PostgreSQL 12 o superior, wkhtmltopdf 0.12.6, OWL 2 en el cliente web, websocket en el puerto de gevent (8072) con ruta `/websocket`.

Odoo 17: Python 3.10 o superior, PostgreSQL 12 o superior, wkhtmltopdf 0.12.6; vistas sin `attrs` ni `states`; `tree` se acepta.

Odoo 18: Python 3.10 a 3.12, PostgreSQL 13 o superior (verificar), wkhtmltopdf 0.12.6; vistas `list` en lugar de `tree` y tarjetas kanban con la plantilla nueva.

Odoo 19: Python 3.10 o superior (3.12 recomendado; verificar límite superior), PostgreSQL 13 o superior (verificar), wkhtmltopdf 0.12.6; API JSON-2 nueva junto a XML-RPC; cambios profundos en valoración de inventario y en contratos de empleados (versiones del empleado), por lo que las integraciones y módulos propios se revisan antes de actualizar.

Reglas generales: la versión de PostgreSQL del servidor de base de datos debe ser la misma o superior a la usada para el respaldo que se restaura; una sola versión mayor de Odoo por servidor salvo contenedores; memoria mínima práctica de 2 GB por trabajador más la base de datos; disco con el doble del tamaño de la base y el filestore para permitir respaldos y actualizaciones; zona horaria del servidor en UTC y la de usuario en Odoo; locale es_MX.UTF-8 instalado para reportes.

Soporte: Odoo mantiene las tres últimas versiones mayores; una versión fuera de soporte no recibe parches de seguridad y se trata como riesgo alto en el diagnóstico.

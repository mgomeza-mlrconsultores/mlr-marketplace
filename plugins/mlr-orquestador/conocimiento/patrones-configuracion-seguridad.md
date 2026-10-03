# Catálogo de patrones: configuración, seguridad y automatizaciones

## S-01 Usuarios con permisos de administrador fuera del equipo técnico
Detección: `res.users` internos en el grupo de administración de ajustes o con todos los grupos; usuarios inactivos con sesiones recientes. Remediación: matriz de roles por puesto y revisión trimestral.

## S-02 Reglas de registro y multiempresa
Detección: `ir.rule` desactivadas o modificadas; usuarios con acceso a compañías que no les corresponden; compañía por defecto incorrecta. Remediación: revisión de reglas nativas y propias.

## S-03 Claves de API y accesos externos
Detección: `res.users.apikeys` por usuario con antigüedad y descripción; integraciones que usan usuarios administradores. Remediación: usuarios de integración con permisos mínimos y rotación.

## S-04 Automatizaciones y acciones de servidor con errores o sin dueño
Detección: `base.automation` y `ir.actions.server` propias con `ir.logging` de error reciente, sin descripción, con `sudo` innecesario, con identificadores numéricos fijos o que escriben `state` directamente. Remediación: catálogo de automatizaciones con responsable, pruebas y versión.

## S-05 Acciones planificadas fallando o desactivadas
Detección: `ir.cron` con `active = False` que deberían correr (por ejemplo, tipos de cambio), crons propios con fallas repetidas. Remediación: calendario de crons y monitoreo.

## S-06 Personalizaciones de Studio sin control
Detección: vistas y campos creados por Studio (`ir.ui.view` con origen Studio, campos `x_studio_`) sin documentación ni exportación; duplicidad con campos nativos. Remediación: inventario de personalizaciones y exportación periódica.

## S-07 Correo saliente y plantillas
Detección: servidor de correo saliente no configurado o con remitente genérico; plantillas que exponen datos; base de pruebas que envía correos reales. Remediación: configuración por entorno y neutralización de bases de prueba.

## S-08 Parámetros del sistema y ajustes de compañía
Detección: `ir.config_parameter` con URL base incorrecta, zona horaria y moneda de compañía inconsistentes, datos fiscales de la compañía incompletos. Remediación: lista de verificación de ajustes de compañía.

## S-09 Portal y exposición pública
Detección: sitio web o portal activos sin uso, documentos accesibles por enlace, usuarios portal con permisos ampliados. Remediación: cierre de lo que no se usa.

## S-10 Bases de pruebas y copias
Detección: copias de producción sin neutralizar (correo, crons, pasarelas fiscales activas), fecha de expiración de staging. Remediación: protocolo de neutralización al crear copias.

## S-11 Módulos instalados y no usados, o en desuso por versión
Detección: módulos con modelos sin registros; módulos de localización ajenos; dependencias que inflan la base. Remediación: desinstalación controlada en base de pruebas antes de producción.

## S-12 Código a medida frágil ante actualizaciones
Detección: vistas que editan el `arch` de vistas nativas en lugar de heredar; campos nativos reutilizados con otro significado; métodos nativos parchados; identificadores numéricos fijos. Remediación: refactorización a herencia no destructiva (ver plugin de personalización).

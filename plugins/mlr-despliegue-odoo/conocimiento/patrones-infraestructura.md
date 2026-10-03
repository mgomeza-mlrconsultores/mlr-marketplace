# Patrones de infraestructura (D-01 a D-14)

D-01 Versión fuera de soporte en producción. Detección: versión mayor anterior a las tres soportadas. Consecuencia: sin parches de seguridad; PAC y localización dejan de actualizarse. Corrección: plan de actualización prioritario.
D-02 Un solo trabajador o modo sin trabajadores en producción. Detección: configuración `workers = 0`. Consecuencia: bloqueos y lentitud con pocos usuarios. Corrección: trabajadores según CPU, proxy y gevent.
D-03 Sin proxy inverso ni TLS, o Odoo expuesto en el puerto 8069. Consecuencia: credenciales en claro, websocket roto. Corrección: nginx con TLS y proxy_mode.
D-04 `list_db` abierto, `admin_passwd` débil o por defecto, sin dbfilter. Consecuencia: cualquiera descarga o borra la base. Corrección: cerrar, rotar, filtrar.
D-05 Respaldo solo de la base sin filestore, o sin copia fuera del servidor, o nunca restaurado. Consecuencia: pérdida de adjuntos y XML; recuperación imposible de estimar. Corrección: política completa y prueba mensual.
D-06 Base de pruebas no neutralizada: envía correos reales, timbra en producción o corre acciones programadas. Corrección: neutralización al copiar.
D-07 Módulos de terceros y OCA sin control de versión ni rama de la versión. Detección: carpetas copiadas a mano. Consecuencia: actualizaciones imposibles de reproducir. Corrección: git con submódulos o manifiesto de versiones.
D-08 `-u all` o actualizaciones de código directo en producción sin ensayo ni respaldo previo. Corrección: procedimiento de despliegue.
D-09 Sin monitoreo de disco, memoria ni respaldos. Consecuencia: caídas por disco lleno y respaldos silenciosamente fallidos. Corrección: alertas básicas.
D-10 Límites de tiempo ampliados globalmente para ocultar lentitud. Corrección: diagnóstico de rendimiento y límites por proceso.
D-11 PostgreSQL con configuración por defecto en servidor grande, sin autovacuum efectivo en tablas grandes. Corrección: tuning y mantenimiento.
D-12 Usuarios administradores sin doble factor, cuentas genéricas compartidas, API keys sin vencimiento. Corrección: política de accesos.
D-13 Zona horaria o locale incorrectos: fechas de CFDI y reportes desplazados. Corrección: UTC en servidor, zona por usuario, locale instalado.
D-14 Datos reales en bases de demostración o en nubes gratuitas sin control. Consecuencia: fuga de datos personales y fiscales. Corrección: enmascarado y controles.

---
name: mlr-mejora-continua-semanal
description: >
  Esta skill debe usarse cuando se diga «ejecuta la mejora continua semanal», «mejora los agentes con lo que aprendimos»,
  «revisa el mercado y actualiza», «qué cambió esta semana en Odoo y en la autoridad» o cuando dispare la tarea programada
  semanal en la nube. Define el presupuesto de cuota, el orden de repositorios (primero la firma, después la versión
  genérica), la cosecha de contexto, la investigación, el diagnóstico con rúbrica, los cambios, la validación, el registro
  en MEJORAS.md y la mejora del propio proceso en cada corrida.
metadata:
  version: "0.2.0"
---

# Mejora continua semanal (en la nube, dos repositorios, autoevaluada)

La mejora solo cuenta si termina en los repositorios. Esta rutina corre en una sesión nueva en la nube, sin depender de ninguna computadora, con el agente `curador-mejora-continua` como ejecutor y este documento como procedimiento vigente. El procedimiento se mejora a sí mismo en cada corrida y la versión que vale es la que está en el repositorio.

## Presupuesto de cuota y límites
La corrida se programa justo después del reinicio semanal de la cuota (madrugada del jueves) para que arranque con la cuota casi íntegra. Reglas: no arranca si el uso de la cuota semanal supera el cincuenta por ciento; se detiene al llegar al cincuenta por ciento, terminando el paso en curso y registrando lo pendiente. Si la sesión no dispone de una forma de medir el uso, aplica el presupuesto fijo escrito en `MEJORAS.md` (por defecto ciento veinte acciones de herramienta y dos horas y media) y lo respeta como si fuera el umbral. Una sola conversación, sin subagentes, sin rondas ciegas; cambios compactos; investigación acotada a lo que puede aplicarse en esta corrida. Al final anota en `MEJORAS.md` cuántas acciones y cuánto tiempo consumió para calibrar el presupuesto siguiente.

## Acceso a los repositorios desde la nube
Se intenta, en este orden: `gh auth status` y clonación con `gh repo clone`; herramientas del conector de GitHub si la sesión las tiene (lectura y escritura de archivos y ramas por API); git por HTTPS con credenciales provistas por la plataforma. Las direcciones de los repositorios están en `MEJORAS.md` (sección Repositorios) y en la memoria de trabajo. Si ninguna vía funciona, la corrida no finge éxito: produce los cambios como archivos de parche en la carpeta de salidas de la sesión, los describe en el reporte y avisa que falta conectar GitHub en la nube. Nunca se piden ni se guardan tokens en archivos, memoria ni chat.

## Procedimiento
1. **Arranque.** Presupuesto verificado y anotado; clonación del repositorio de la firma (rama principal) y del personal (ramas `main` con los scripts y `genericos` con la versión genérica); `git log --since="8 days ago"` en ambos.
2. **Cosecha de contexto.** Memoria de trabajo del consultor (plan, directivas, bitácora de la semana), `MEJORAS.md` (última corrida, pendientes, métricas), `CAMBIOS.md` de cada plugin, bitácoras y casos de referencia nuevos, correcciones de criterio registradas. Resultado: lista corta de aprendizajes y fallos observados.
3. **Investigación acotada.** Fuentes primarias con enlace y fecha de consulta: notas de versión y hoja de ruta de Odoo, repositorios OCA del dominio, autoridad fiscal (DOF, SAT), laboral y de seguridad social (STPS, IMSS, INFONAVIT), autoridad de datos personales, plataforma de agentes y skills (cambios de formato o capacidades), prácticas y precios públicos de partners y despachos. Máximo diez búsquedas salvo que un cambio normativo exija más.
4. **Diagnóstico.** `python3 scripts/revisar_agentes.py <plugins> --estricto` en ambos repositorios; coherencia del conocimiento (duplicados, contradicciones, referencias rotas, vencimientos); agentes y skills nunca usados o con fallos reportados. Lista de mejoras priorizadas por impacto y esfuerzo; entre tres y ocho cambios por corrida.
5. **Cambios en el repositorio de la firma.** Editar agentes, skills, conocimiento y scripts con la identidad de la firma; subir versión de los plugins tocados; validar (rúbrica estricta, compilación, pruebas existentes). Commit `[MEJORA] <fecha> <resumen>` y push según el modo de `MEJORAS.md`: `pr` abre una rama `mejora/<fecha>` y un pull request con el resumen; `directo` empuja a la rama principal.
6. **Versión genérica.** En el clon personal: `bash scripts/construir_genericos.sh <clon de la firma>/plugins plugins extras` sobre la rama `genericos`; `scripts/genericizar.py --destino plugins --reporte` debe quedar sin residuos reales; rúbrica estricta en verde; lectura de confidencialidad de los archivos nuevos o cambiados (`revisor-confidencialidad`); commit y push a `genericos`. Los extras nuevos que nacieron en esta corrida se escriben en `extras/` del repositorio personal para que la reconstrucción sea reproducible.
7. **Mejora del propio proceso.** Comparar métricas de esta corrida con las anteriores; aplicar al menos un cambio a esta skill, al agente curador, a los scripts o al orden del procedimiento que reduzca acciones o aumente cambios útiles; si el prompt de la tarea programada debe cambiar, escribir el texto propuesto en `MEJORAS.md` (sección Propuestas al prompt) y señalarlo en el reporte: el prompt lo cambia el consultor desde su conversación.
8. **Registro y reporte.** Entrada en `MEJORAS.md` (fecha, acciones y tiempo, cambios con archivo, fuentes, mejoras al proceso, pendientes, errores exactos); línea de estado en la memoria de trabajo; reporte breve en prosa con enlaces a commits o pull requests.

## Mejorar lo existente y crear solo lo que hace falta
La prioridad es mejorar lo que ya existe. Cuando el contexto de la semana muestra una necesidad real (un tipo de tarea que se repite sin agente propio, un dominio donde un agente general falla, una etapa o aplicación sin especialista, una norma nueva que exige conocimiento propio), la rutina puede crear agentes, skills, conocimiento o incluso un plugin nuevo, siempre con esta regla: especializado antes que general, porque un agente especializado se mide y se mejora mejor; una creación por corrida como máximo salvo cambio normativo que exija más; cada agente nuevo con la misma estructura y rúbrica que los demás; y un volumen total que siga siendo manejable (si el marketplace supera lo que la rúbrica y el consultor pueden revisar, la rutina propone fusionar antes que crear). Lo creado se registra en `MEJORAS.md` con la necesidad que lo originó y se aplica en ambos repositorios: con identidad en el de la firma y en forma genérica, vía `extras/` y el pipeline, en el personal.

## Lo que nunca hace
Borrar conocimiento (marca obsoleto con fecha); tocar producción de ningún cliente; copiar identidad, clientes, rutas, tarifas o correos de la firma a la versión genérica; declarar vigente una norma sin publicación oficial; superar el presupuesto; ocultar un fallo de push o de clonación.

# MLR Orquestador

Estándar operativo de MLR Consultores. Sustituye el comportamiento genérico del asistente por el método de la firma: recupera el contexto de cliente y las directrices vigentes desde memoria en la nube al abrir cada sesión, enruta cada petición al flujo especializado y aplica las normas de redacción, identidad visual, diagramacion, entrega y archivo.

## Que instala

Once skills que se activan solas según lo que se pida.

**`mlr-orquestador`** — Se dispara al inicio de cualquier trabajo. Recupera memoria, clasifica la petición, carga las skills especializadas y aplica los innegociables. Es la pieza que impide la respuesta genérica.

**`mlr-memoria`** — Protocolo de memoria en la nube: que se guarda, en que espacio, con que formato, y como el asistente actualiza sus propias directrices cuando alguien corrige un criterio.

**`mlr-redaccion`** — Registro directivo de la firma. Estructura de conclusión primero, léxico controlado, glosario en línea y lista de patrones prohibidos que elimina el rastro de escritura generada por IA. Incluye verificación programática de cifras e identificadores.

**`mlr-identidad-visual`** — Membrete, paleta, tipografía, profundidad por elevación y lista negra de rasgos que delatan diseño automático. Lee la marca del Drive de la organización, con copia incrustada de respaldo.

**`mlr-cotizacion`** — Cotización y plan de implementación de Odoo. Fija el orden: cliente y base auditada, preguntas resueltas en casa antes de molestar al cliente, diagrama del proceso objetivo, ruta por etapas, horas calibradas contra proyectos reales y condiciones económicas. Nada se escribe en archivo antes de la aprobación en el chat. El formato y la redacción de los entregables los delega en `mlr-redaccion` e `mlr-identidad-visual`.

**`mlr-informe-funcional`** — Guía funcional de un desarrollo para el usuario del cliente: paso a paso, con capturas reales de la base de pruebas, en Word membretado y en HTML con el formato aprobado por dirección y la barra de menú de la firma. Trae el método de captura en Odoo, los generadores de Word y HTML desde una sola fuente de contenido y el revisor del HTML.

**`mlr-presentaciones`** — Patrón de deck de la firma en HTML autocontenido: barra con logotipo vectorial, menú de grupos, navegación por teclado y contador. Una idea por lamina, con el titular como conclusión.

**`mlr-diagramas-odoo`** — Diagramas con la estética y la nomenclatura de la documentación técnica de ERP. Tema Mermaid propio alineado a la identidad de Odoo.

**`mlr-video`** — Video explicativo corporativo con Remotion.

**`mlr-animacion-web`** — Movimiento en páginas y tableros con criterio de estudio, sobre GSAP.

**`mlr-actualizacion`** — Instala, verifica y mantiene al día todo el entorno: marketplace interno, memoria, skills externas y carpeta de plantillas. Nunca reinstala: actualiza.

## Memoria en la nube

El plugin declara un servidor MCP remoto. **No se instala nada en la maquina** y el contexto sigue a la persona entre dispositivos y entre chats.

**Supermemory** (`https://mcp.supermemory.ai/mcp`), plan gratuito. Grafo de memoria con espacios: uno por cliente, mas uno de firma. Crédito de uso mensual renovable, sin tarjeta. Certificación SOC 2 Type II, cumplimiento GDPR, cifrado en reposo, y no usa el contenido de sus clientes para entrenar modelos en ningún plan, gratuito incluido.

Al instalar el plugin aparece para autorizar en el navegador.

**Alternativa gratuita:** Zep Cloud (`https://api.getzep.com/mcp`), también con plan gratuito y memoria que versiona hechos en el tiempo. Usar una de las dos, no ambas.

## Como se carga en cada chat

Un servidor MCP no se consulta solo: la herramienta está disponible, pero el modelo debe decidir usarla. Por eso el paso 1 de `mlr-orquestador` es una instrucción explicita de buscar las directrices vigentes antes de la primera respuesta sustantiva de cada sesión. Ese es el mecanismo que hace real el contexto transversal.

## Directrices que se actualizan solas

Cuando alguien corrige un criterio, el asistente guarda esa corrección como directriz en el espacio de firma o del cliente, con su origen, y la aplica desde la siguiente sesión sin reinstalar nada.

**Limites.** Las directrices pueden cambiar formato, tono, alcance, herramientas y convenciones. No pueden eliminar la verificación de cifras y fuentes, relajar la confidencialidad, autorizar afirmar algo sin comprobarlo, ni suprimir el análisis crítico y el desacuerdo honesto.

## Dependencias externas

Ninguna para orquestación, memoria, redacción, identidad y diagramas.

El resto se instala y se actualiza con la skill `mlr-actualizacion`, que trae los comandos exactos: skills de redacción, presentaciones, video, animación web y consultoría.

**Todo el entorno es gratuito.** La única herramienta con licencia no libre es Remotion, que el plugin no usa por defecto: el módulo de video trabaja sobre Motion Canvas (MIT). Si alguien decide usar Remotion, debe verificar antes los términos vigentes en su página de licencia.

## Estructura de archivo

Cada persona trabaja en su unidad local bajo una carpeta raíz `Proyecto MLR`:

```
Proyecto MLR/
  <Cliente>/
    Informes/               20260821/  20260906/ ...
    Documentos extras/      20260821/ ...
    Capturas de pantalla/   20260821/ ...
```

Nombres fijos, fecha en formato `AAAAMMDD` dentro de cada una de las tres carpetas.

El membrete no vive en local: está en la unidad compartida de la empresa en Drive, carpeta `MLR > Hoja Membretada`. El plugin trae los identificadores exactos de la carpeta y de los tres archivos, así que nunca hay que indicarle donde están.

## Pendiente antes del despliegue general

1. **Extraer los tokens de color y tipografía** de la plantilla de membrete. Solo hacen falta para presentaciones, páginas y gráficas; los documentos formales ya se construyen sobre el archivo de Word.
2. **Dar de alta la memoria** en el plan gratuito y crear el espacio de firma con las primeras directrices.

## Mantenimiento

Dos niveles. Las correcciones entran en la memoria y aplican de inmediato. Cada trimestre, lo que resulto estable se consolida en las skills, se eliminan directrices obsoletas y se sube versión.

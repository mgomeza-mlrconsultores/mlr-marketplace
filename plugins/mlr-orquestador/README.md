# MLR Orquestador

Estandar operativo de MLR Consultores. Sustituye el comportamiento generico del asistente por el metodo de la firma: recupera el contexto de cliente y las directrices vigentes desde memoria en la nube al abrir cada sesion, enruta cada peticion al flujo especializado y aplica las normas de redaccion, identidad visual, diagramacion, entrega y archivo.

## Que instala

Ocho skills que se activan solas segun lo que se pida.

**`mlr-orquestador`** — Se dispara al inicio de cualquier trabajo. Recupera memoria, clasifica la peticion, carga las skills especializadas y aplica los innegociables. Es la pieza que impide la respuesta generica.

**`mlr-memoria`** — Protocolo de memoria en la nube: que se guarda, en que espacio, con que formato, y como el asistente actualiza sus propias directrices cuando alguien corrige un criterio.

**`mlr-redaccion`** — Registro directivo de la firma. Estructura de conclusion primero, lexico controlado, glosario en linea y lista de patrones prohibidos que elimina el rastro de escritura generada por IA. Incluye verificacion programatica de cifras e identificadores.

**`mlr-identidad-visual`** — Membrete, paleta, tipografia, profundidad por elevacion y lista negra de rasgos que delatan diseno automatico. Lee la marca del Drive de la organizacion, con copia incrustada de respaldo.

**`mlr-diagramas-odoo`** — Diagramas con la estetica y la nomenclatura de la documentacion tecnica de ERP. Tema Mermaid propio alineado a la identidad de Odoo.

**`mlr-video`** — Video explicativo corporativo con Remotion.

**`mlr-animacion-web`** — Movimiento en paginas y tableros con criterio de estudio, sobre GSAP.

**`mlr-actualizacion`** — Instala, verifica y mantiene al dia todo el entorno: marketplace interno, memoria, skills externas y carpeta de plantillas. Nunca reinstala: actualiza.

## Memoria en la nube

El plugin declara un servidor MCP remoto. **No se instala nada en la maquina** y el contexto sigue a la persona entre dispositivos y entre chats.

**Supermemory** (`https://mcp.supermemory.ai/mcp`), plan gratuito. Grafo de memoria con espacios: uno por cliente, mas uno de firma. Credito de uso mensual renovable, sin tarjeta. Certificacion SOC 2 Type II, cumplimiento GDPR, cifrado en reposo, y no usa el contenido de sus clientes para entrenar modelos en ningun plan, gratuito incluido.

Al instalar el plugin aparece para autorizar en el navegador.

**Alternativa gratuita:** Zep Cloud (`https://api.getzep.com/mcp`), tambien con plan gratuito y memoria que versiona hechos en el tiempo. Usar una de las dos, no ambas.

## Como se carga en cada chat

Un servidor MCP no se consulta solo: la herramienta esta disponible, pero el modelo debe decidir usarla. Por eso el paso 1 de `mlr-orquestador` es una instruccion explicita de buscar las directrices vigentes antes de la primera respuesta sustantiva de cada sesion. Ese es el mecanismo que hace real el contexto transversal.

## Directrices que se actualizan solas

Cuando alguien corrige un criterio, el asistente guarda esa correccion como directriz en el espacio de firma o del cliente, con su origen, y la aplica desde la siguiente sesion sin reinstalar nada.

**Limites.** Las directrices pueden cambiar formato, tono, alcance, herramientas y convenciones. No pueden eliminar la verificacion de cifras y fuentes, relajar la confidencialidad, autorizar afirmar algo sin comprobarlo, ni suprimir el analisis critico y el desacuerdo honesto.

## Dependencias externas

Ninguna para orquestacion, memoria, redaccion, identidad y diagramas.

El resto se instala y se actualiza con la skill `mlr-actualizacion`, que trae los comandos exactos: skills de redaccion, presentaciones, video, animacion web y consultoria.

**Todo el entorno es gratuito.** La unica herramienta con licencia no libre es Remotion, que el plugin no usa por defecto: el modulo de video trabaja sobre Motion Canvas (MIT). Si alguien decide usar Remotion, debe verificar antes los terminos vigentes en su pagina de licencia.

## Estructura de archivo

Cada persona trabaja en su unidad local bajo una carpeta raiz `Proyecto MLR`:

```
Proyecto MLR/
  <Cliente>/
    Informes/               20260821/  20260906/ ...
    Documentos extras/      20260821/ ...
    Capturas de pantalla/   20260821/ ...
```

Nombres fijos, fecha en formato `AAAAMMDD` dentro de cada una de las tres carpetas.

El membrete no vive en local: esta en la unidad compartida de la empresa en Drive, carpeta `MLR > Hoja Membretada`. El plugin trae los identificadores exactos de la carpeta y de los tres archivos, asi que nunca hay que indicarle donde estan.

## Pendiente antes del despliegue general

1. **Extraer los tokens de color y tipografia** de la plantilla de membrete. Solo hacen falta para presentaciones, paginas y graficas; los documentos formales ya se construyen sobre el archivo de Word.
2. **Dar de alta la memoria** en el plan gratuito y crear el espacio de firma con las primeras directrices.

## Mantenimiento

Dos niveles. Las correcciones entran en la memoria y aplican de inmediato. Cada trimestre, lo que resulto estable se consolida en las skills, se eliminan directrices obsoletas y se sube version.

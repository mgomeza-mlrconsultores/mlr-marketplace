# Archivo y entrega MLR

Esta es la regla única de dónde se guarda todo lo que se produce para un cliente. Todas las skills de MLR (diagnóstico, cotización, informe funcional, presentaciones, diagramas, conciliación, agentes de Odoo) remiten aquí y la aplican sin variantes.

## Raíz y carpeta del cliente

Todo se guarda en la carpeta del proyecto **`MLR Odoo`**, que en el equipo de Marcos es `C:\Users\mgome\Claude\Projects\MLR Odoo\` y en Cowork es la carpeta conectada con ese nombre. Debajo hay una carpeta por cliente y, dentro de cada cliente, tres carpetas fijas con la fecha dentro de cada una:

```
MLR Odoo\
  <Cliente>\
    Informes\
      20260929\                 lo que recibe el cliente: Word, PDF, HTML, Excel
    Documentos extras\
      20260929\                 lo que mandó el cliente y el trabajo de esa fecha
        Interno\                catálogos, bitácoras, scripts sin llave, salidas de agentes
          Versión reemplazada\  entregables sustituidos después de emitidos
    Capturas de pantalla\
      20260929\                 evidencia visual numerada en el orden del informe
    Contexto\                   ficha del cliente y memoria (opcional)
```

- Los tres nombres son fijos y se escriben tal cual, con tilde donde lleve y mayúscula solo en la primera palabra: `Informes`, `Documentos extras`, `Capturas de pantalla`.
- La carpeta de fecha es `AAAAMMDD` sin separadores (`20260929`), la del día de emisión. Nunca `2026-09-29` ni `29-09-2026`.
- **Si el cliente ya tiene carpeta, se usa la suya**, con su nombre tal cual; nunca se crea una paralela ni se inventa otro nombre.
- **Si la carpeta del cliente, cualquiera de las tres carpetas fijas o la carpeta de fecha no existen, se crean completas antes de guardar, sin preguntar**, incluidas todas las carpetas intermedias hasta llegar a la ruta final. Aunque el trabajo del día solo produzca informes, al crear un cliente nuevo se crean las tres carpetas.

## Qué va en cada carpeta

**Informes.** Solo los entregables que abre el cliente: diagnósticos, cotizaciones, guías funcionales, presentaciones HTML, anexos en Excel, memorandos. Construidos sobre el membrete de la firma. No se crean carpetas sueltas como `Propuesta` o `Diagnóstico`.

**Documentos extras.** Todo lo que acompaña sin ser el entregable: insumos que envió el cliente, extracciones de su base, hojas de trabajo y notas. El trabajo interno (catálogo de hallazgos, bitácora de rondas, origen único de datos, generadores, salidas de agentes) va en `Documentos extras\<AAAAMMDD>\Interno\`.

**Capturas de pantalla.** Toda la evidencia visual: las capturas que sustentan un informe, pantallas antes y después de un cambio, mensajes de error. **Las capturas nunca van dentro de `Informes`**: van en `Capturas de pantalla\<AAAAMMDD>\`, numeradas en el orden en que aparecen en el documento, con nombre `<Cliente>_<Tema>_Figura_NN.jpg`.

## Reglas

- Una carpeta de fecha por jornada de entrega o por hito, no por cada día trabajado. La fecha es la misma en las tres carpetas para un mismo entregable.
- Los entregables no se sobrescriben. Si se reemite, se abre una carpeta de fecha nueva y la anterior queda intacta, o la versión sustituida pasa a `Interno\Versión reemplazada\`.
- Los archivos de trabajo no se mezclan con los informes.
- Ningún archivo archivado lleva credenciales: la llave de API se lee de variable de entorno y se retira de cualquier script antes de guardarlo.
- Nombres de archivo legibles, con tildes y eñes, que digan qué es y de qué cliente: `Diagnóstico General Freshbox.docx`, `1. Propuesta Económica - <Cliente>.pdf`. Las skills que fijan un patrón de nombre propio lo conservan.
- Cuando el cliente tiene varios proyectos vivos a la vez, la estructura completa se repite dentro de una carpeta por proyecto dentro de la del cliente.

## Cómo se guarda desde una sesión de Cowork en la nube

1. Si la carpeta `MLR Odoo` no está conectada, se pide acceso con la herramienta de carpetas del equipo antes de producir nada.
2. Se arma en el área de salida la misma estructura (`<Cliente>\Informes\<AAAAMMDD>\...`) y se escribe cada archivo en su ruta final dentro de la carpeta conectada; la escritura crea las carpetas intermedias que falten.
3. Se comprueba al final, listando la carpeta del cliente, que cada archivo quedó en su carpeta y que no quedaron capturas dentro de `Informes`.

## Membrete

No vive en la carpeta del cliente. Está en `MLR Odoo\Plantillas\` y en la unidad compartida de la empresa, con los identificadores anotados en la skill `mlr-identidad-visual`. Se escribe dentro de la plantilla y el resultado se guarda en `Informes\<AAAAMMDD>\`.

## Al cerrar un trabajo

1. Entregable en `Informes\<AAAAMMDD>\`, capturas en `Capturas de pantalla\<AAAAMMDD>\` y trabajo interno en `Documentos extras\<AAAAMMDD>\Interno\`.
2. Registrar en la memoria del cliente qué se entregó, en qué carpeta quedó, qué se decidió y qué quedó pendiente.
3. Decir a la persona, en lenguaje llano, en qué carpeta quedó cada cosa.

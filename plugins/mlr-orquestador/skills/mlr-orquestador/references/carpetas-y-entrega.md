# Archivo y entrega MLR

## Estructura de trabajo

Cada persona trabaja en su unidad local, dentro de una carpeta raiz llamada **`Proyecto MLR`**. Debajo, una carpeta por cliente, y dentro de cada cliente tres carpetas fijas. La fecha va **dentro** de cada una de las tres.

```
Proyecto MLR/
  <Cliente>/
    Informes/
      20260821/
      20260906/
    Documentos extras/
      20260821/
    Capturas de pantalla/
      20260821/
```

Los tres nombres son fijos y se escriben tal cual: `Informes`, `Documentos extras`, `Capturas de pantalla`. La carpeta de fecha usa el formato `AAAAMMDD` sin separadores: `20260821`, nunca `2026-08-21` ni `21-08-2026`.

## Que va en cada carpeta

**Informes.** Los entregables formales que lee el cliente: diagnosticos, informes de avance, propuestas, memorandos. Construidos sobre el membrete de la firma.

**Documentos extras.** Todo lo que acompana sin ser el entregable: insumos que envio el cliente, extracciones de su base de datos, hojas de calculo de trabajo, notas y borradores.

**Capturas de pantalla.** Evidencia visual: pantallas de Odoo antes y despues de un cambio, mensajes de error, configuraciones. Es lo que sustenta lo que afirma el informe.

## Reglas

- Una carpeta de fecha por jornada de entrega o por hito, no por cada dia que se trabajo.
- Los entregables no se sobrescriben. Version nueva, carpeta de fecha nueva.
- Los archivos de trabajo no se mezclan con los informes. Para eso existe `Documentos extras`.
- El nombre de archivo lleva cliente, tema y fecha, en minusculas y separado por guiones.

## Membrete

No vive en la carpeta local. Esta en la unidad compartida de la empresa en Google Drive, carpeta `MLR > Hoja Membretada`, con los identificadores anotados en la skill `mlr-identidad-visual`. Se descarga la plantilla, se escribe dentro y el resultado se guarda en `Informes/<fecha>/`.

## Al cerrar un trabajo

1. Dejar el entregable en `Informes/<fecha>/`, y las capturas que lo sustentan en `Capturas de pantalla/<fecha>/`.
2. Registrar en la memoria del cliente: que se entrego, en que carpeta quedo, que se decidio y que quedo pendiente.
3. Decir a la persona, en lenguaje llano, en que carpeta quedo y que contiene.

Si la carpeta del cliente o la de fecha no existen todavia, crearlas siguiendo esta estructura sin preguntar.

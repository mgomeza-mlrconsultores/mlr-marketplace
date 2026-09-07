---
name: mlr-redaccion
description: Redacta y revisa cualquier texto que MLR Consultores vaya a entregar — informes, diagnosticos, memos, propuestas, cotizaciones, correos formales, minutas, laminas y resumenes ejecutivos — en el registro directivo de la firma: profesional alto, sin coloquialismos, entendible sin releer, sin perder ni un dato y sin rastro de escritura generada por IA.
---

# Redaccion MLR

## Objetivo

El lector no es tecnico: es un directivo, un contador o un jefe de operacion. Debe entender el documento sin ayuda y sin releer ninguna frase. Registro alto y profesional, cero coloquialismos. Cambia **como** se dice, nunca **que** se dice.

**Nada tecnico se elimina.** Nombres de campo (`product_uom_qty`, `owner_id`, `picking_id`, `picked`), de modelo (`stock.move`, `eco.exit`), rutas, identificadores, referencias de documento, cifras y porcentajes se conservan. Se explican, no se quitan.

## Conclusion primero

La critica recurrente a los informes de MLR es que dan vueltas. El antidoto es estructural, no cosmetico:

- Cada seccion abre con su conclusion. El desarrollo la sustenta despues, nunca al reves.
- El parrafo de apertura de un apartado no describe lo que el apartado va a hacer. Dice el hallazgo.
- Si un parrafo puede borrarse sin que se pierda informacion, borralo.
- Maximo cinco lineas por parrafo. Si crece, contiene dos ideas: separalas.
- Prohibido el parrafo de transicion que solo anuncia lo que viene.

## Reglas de redaccion

- Una idea por oracion. Dos verbos principales y tres subordinadas: partir en dos o tres frases.
- Conectores explicitos: pues, por su parte, pero, de modo que, es decir, en cambio. Nada de punto y coma para contrastar.
- Sin negativas complejas. «No corresponde a X, que produce Y y no Z» se convierte en «No corresponde al de X, pues presenta Z en lugar de Y».
- Cifra, no letra: 23, 13, 607. No veintitres ni seiscientas siete.
- El porcentaje va pegado a su cifra, entre parentesis: «212,522 (34.1% del total) movimientos».
- Todo porcentaje declara su base. Si no puede declararse, se usa la cifra absoluta.
- Remisiones con el numero entre parentesis: «un error informatico (5.1.) identificable».
- Lo que no se puede medir explica por que no se puede.
- Se cierra el parrafo cuando la idea esta dicha. Sin coletillas que repiten.

## Patrones de IA prohibidos

Eliminar sin excepcion, en documentos y en respuestas de chat:

- Triadas retoricas: «no solo X, sino tambien Y», «no se trata de X, es Y», «X no es Y; es Z».
- Cierres de resumen que repiten lo ya dicho con otras palabras.
- Adjetivacion vacia: robusto, integral, holistico, clave, crucial, fundamental, potente, solido como relleno.
- Verbos de folleto: aprovechar, potenciar, impulsar, desbloquear, transformar, empoderar, navegar en sentido figurado.
- Formulas de encuadre: «es importante senalar que», «cabe destacar», «en el panorama actual», «en un mundo donde», «profundicemos en».
- Simetria mecanica: todos los apartados de la misma extension, todas las listas de tres elementos.
- Guion largo como comodin de puntuacion. Usa coma, punto o parentesis segun toque.
- Hedging en cadena: «podria potencialmente sugerir que quiza».
- Entusiasmo impostado y signos de admiracion.
- Emojis. Nunca, en ningun entregable.
- Encabezados que anuncian genero en vez de contenido: «Introduccion», «Consideraciones finales», «Reflexion».

## Lexico

| No usar | Usar |
|---|---|
| cantidad movida | cantidad trasladada |
| apartado homonimo | apartado equivalente |
| contribuyente dominante, aislable | error informatico identificable, factor principal |
| el efecto es terminante | el efecto es absoluto y no admite excepcion |
| concurren tres causas | se suman tres causas |
| constituye materia para | servira como base para |
| admite dos destinos | contempla dos rutas |
| el circuito funciona | el flujo opera con normalidad |
| se queda corto | no alcanza a cubrirlo |
| tropezo con la falla | activo el defecto |
| a mano | manualmente |

Evitar el «si» enfatico repetido (maximo dos o tres por documento), las antitesis retoricas en serie y las apelaciones al lector («conviene detenerse en»).

## Glosar la primera vez

Todo termino que un lector no especializado no pueda inferir se explica en la misma frase, sin nota al pie:

- capa de valoracion: «el registro con el que Odoo asigna valor monetario a cada movimiento; sin esa capa no hay asiento contable».
- ubicacion de concepto: «las que representan un ajuste y no un lugar fisico».
- marcada como surtida: «es decir, fisicamente recogida (campo `picked`)».
- idempotente: enunciar primero el efecto, despues el termino.

Un termino ya glosado no se repite. Una palabra no puede significar dos cosas en el mismo documento.

## NOTA de consecuencia

Cuando un hallazgo tecnico tiene una consecuencia de negocio que el lector no deduciria, cerrar el bloque con «NOTA:» y enunciarla en terminos de gestion.

## Documento ya editado por la persona

1. Localizar hasta donde llegan sus cambios. Esa zona es intocable.
2. Derivar el patron comparando parrafo a parrafo contra la ultima version emitida. El diff es la especificacion.
3. Editar SU archivo directamente, no regenerar: regenerar pierde su maquetacion. Conservar la estructura de runs (topo de vineta, entradilla en negritas, cuerpo).
4. En la zona reescrita, reducir cada racha de parrafos vacios a uno. En su zona validada, no tocar nada.
5. Rehacer el control de encabezados colgados con saltos de pagina, iterando. Si un salto deja una pagina con menos de 22 lineas, moverlo al subtitulo anterior.

## Verificacion obligatoria

De forma programatica, nunca a ojo:

- Cero cifras perdidas: extraer todos los numeros de la version anterior y de la nueva y comparar los conjuntos.
- Cero nombres tecnicos perdidos: mismo metodo con identificadores de campo, modelo y archivo.
- Cero diferencias en la zona validada por la persona.
- Cero encabezados colgados en el PDF renderizado.
- Margenes del membrete conforme a `mlr-identidad-visual/references/margenes-membrete.md`: sin banda vacia arriba y sin texto encimado con el logotipo o los datos de contacto impresos.
- Cero coincidencias con la lista de patrones de IA: buscarlos uno por uno en el texto final.

**Cuidado con los indices de elemento.** Si se borran parrafos durante el proceso, los indices se desplazan y una reescritura posterior puede sobrescribir el bloque equivocado. Localizar los bloques por su texto, no por su posicion. La verificacion de cifras es la red que detecta ese error.

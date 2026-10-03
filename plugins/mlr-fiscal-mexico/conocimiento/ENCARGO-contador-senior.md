# Encargo abierto: agentes fiscales con criterio de contador senior

Estado: abierto desde el 3 de octubre de 2026. Lo cierra Marcos cuando los agentes estén publicados y probados.

## Qué se pide
Que los agentes del plugin fiscal trabajen como un contador senior con experiencia en la contabilidad mexicana, no como un repositorio de leyes. Alcance: previos de impuestos mensuales (IVA, ISR provisional, retenciones y pagos definitivos) a partir de los CFDI y de la contabilidad de cada cliente en Odoo; cierre anual y declaración anual; consejos fiscales y análisis de la situación fiscal de cada cliente, incluidas las decisiones de régimen (RESICO frente a persona moral y personas físicas con actividad empresarial) y el efecto de la legislación que entra en vigor el año siguiente; opiniones de cumplimiento y los procedimientos del despacho tal como se practican en MLR.

## Insumos de la firma
Los previos de impuestos ya elaborados en la base de Odoo de la firma, que se consultan con credenciales que Marcos entrega en la sesión de trabajo y que no se escriben nunca en este repositorio, en la memoria ni en los agentes. El archivo de fórmulas de la aplicación Documentos, carpeta de impuestos, que calcula el previo de IVA e ISR según el régimen fiscal del cliente y que ya se ha aplicado en varias empresas. Los documentos del Drive compartido sobre cierres de impuestos, XML, política de trabajo, entregables a clientes y opiniones de cumplimiento.

## Método
Estudiar los insumos y reconstruir la lógica de cálculo como conocimiento y procedimientos verificables en `conocimiento/`; probar los agentes contra casos reales hasta que el resultado coincida con los previos ya hechos; incorporar la legislación vigente y la que se aprueba para el ejercicio siguiente con fuente y fecha; publicar solo con la rúbrica en verde y el enrutamiento registrado en el orquestador. La versión genérica se reconstruye con el pipeline del repositorio personal, sin identidad de la firma ni datos de clientes.

## Ejecución
Sesión interactiva dedicada tras el reinicio de la cuota semanal, con las credenciales en mano. La rutina semanal recuerda este encargo mientras siga abierto y puede adelantar la parte normativa (fuentes primarias del SAT y del DOF, criterios y reformas publicadas), pero la lógica de cálculo se valida con los datos de la firma.

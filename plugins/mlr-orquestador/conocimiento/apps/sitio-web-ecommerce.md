# Sitio web y comercio electrónico

## Decisiones que gobiernan el resultado
Un sitio por marca o por país; catálogo publicado por producto y variante; precios por lista pública; pasarelas de pago y su conciliación; métodos de envío y conectores con operadores logísticos; impuestos por posición fiscal del comprador; facturación automática o a solicitud (en México, portal de autofacturación o factura global); conectores con tiendas externas (tiendas en línea de terceros) y qué sistema manda en inventario y precios; aviso de privacidad y términos (ver plugin legal); formularios y automatizaciones de prospectos.

## Patrones de error
Dos fuentes de verdad de inventario entre la tienda externa y Odoo; pedidos web sin impuestos correctos por posición fiscal; pagos capturados sin conciliar con la pasarela; envíos sin costo real; productos publicados sin existencia; aviso de privacidad inexistente o desactualizado.

## Por versión
16: constructor de sitios; 17: rediseño del constructor y del comercio electrónico; 18: mejoras en catálogo y pago (verificar); 19: funciones de IA para contenido (Enterprise, verificar). Conectores con tiendas externas: en SaaS vía integradores, en Odoo.sh o local con módulos.

## Lo que pregunta un senior
¿Quién manda en el precio y en la existencia: Odoo o la tienda externa? ¿Cómo se concilia lo cobrado por la pasarela con el banco? ¿Qué factura recibe el comprador y cuándo?

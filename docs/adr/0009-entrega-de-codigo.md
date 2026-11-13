# ADR-0009 · Entrega del código de un solo uso (ESC-61)

> Migrado el 2026-11-13 desde [Decisiones de diseño: MVP de constancias](https://claude.ai/artifact/BFv1HemHiY2yqZoTx7jqoc) (fecha del original: 2026-11-12). Texto copiado sin cambios.

**Estado:** aceptado, 2026-11-12 (Samuel). **Historias:** ESC-61, ESC-44. **Pruebas:** C-26 a C-30.

**Decisión:** un código de 6 dígitos, no un enlace mágico, que llega por correo en el MVP a través del puerto Notificador. SMS y WhatsApp entran después como otros adaptadores del mismo puerto, elegidos por configuración. En la demo el adaptador es un buzón simulado.

## Contexto

- ESP-CON ya fija el flujo: pedir código, canjearlo, sesión con JWT; expira a los 10 minutos y se bloquea al tercer intento. Falta decidir la forma del secreto y el canal.
- No hay contraseñas. El contacto registrado en el padrón (ESC-44) es la única prueba de identidad remota; cambiarlo solo se hace en persona.
- El alumno puede pedir la constancia desde una computadora del plantel y leer el código en su teléfono.
- Para la demo con la institución sintética de unos 800 alumnos no se debe mandar ningún mensaje real (principio 48).
- No se sabe aún qué contacto trae el padrón real ni si es del alumno o del tutor. Es un supuesto abierto antes del piloto.

## Opciones consideradas

**Forma del secreto**

| Opción | A favor | En contra |
| --- | --- | --- |
| Código de 6 dígitos (recomendada) | Funciona entre dispositivos: se pide en la PC y se lee en el teléfono. Sirve igual por correo, SMS o en persona. Ya está en ESP-CON. | El alumno lo teclea. |
| Enlace mágico | Un toque y entra. | Abre la sesión en el dispositivo donde se lee el correo, no donde se pidió. Los filtros de correo que abren enlaces lo pueden gastar. No sirve en persona. |

**Canal en el MVP**

| Canal | Costo por mensaje | Alcance probable | Notas |
| --- | --- | --- | --- |
| Correo (recomendado) | Casi nulo | Medio: no todos lo revisan | Solo requiere un servidor SMTP o un servicio de envío. |
| SMS | Se paga por mensaje | Alto | Pide contrato con un proveedor y presupuesto de la escuela. |
| WhatsApp | Se paga por mensaje de autenticación | Muy alto | Pide cuenta de WhatsApp Business verificada y plantilla aprobada. |
| Solo en persona | Nulo | Total | Ya existe como respaldo (C-30); no escala como canal principal. |

## Decisión

1. **Secreto.** Código de 6 dígitos generado con un generador criptográfico. Se guarda como HMAC con una llave del servidor, no como hash simple: un hash de un millón de valores posibles se revienta en segundos.
2. **Puerto Notificador** (principio 7). Una sola operación, `enviar_codigo(contacto, codigo, vence_en)`. Adaptadores:
   - `buzon_simulado`: guarda el mensaje y la demo lo muestra en una página de buzón. Es el único activo con la institución sintética.
   - `correo`: SMTP. Es el del MVP real.
   - `sms` y `whatsapp`: después, sin cambiar la API.
3. **Canal por configuración.** La institución elige el adaptador y su orden de respaldo en la capa de configuración (paquete, institución). El paquete «Estándar» trae `correo`.
4. **Respuesta sin filtrar el padrón.** `POST /v0/auth/codigo` responde siempre 202 con el mismo texto, exista o no la matrícula. Si existe, el texto muestra el contacto enmascarado (`a*****@c****.mx`). Así nadie puede sondear qué matrículas están inscritas.
5. **Límites.** Como mucho 3 códigos por matrícula cada 15 minutos y 20 por IP cada hora. Pedir un código nuevo invalida el anterior.
6. **Sesión.** El JWT de sesión dura 30 minutos (configurable). Cada solicitud y cada canje quedan como hechos con `ocurrio_en`.
7. **Sin contacto.** Se mantiene la activación en persona de ESP-CON (C-30).

## Consecuencias

- **Se gana:** la demo corre completa sin enviar nada, el MVP real cuesta casi nada por mensaje, y cambiar de canal es configuración, no código.
- **Se pierde:** alumnos que no revisan su correo dependen de la activación en persona hasta que haya SMS o WhatsApp.
- **Obliga a:** cambiar en ESP-CON el error `no-en-padron` de `POST /v0/auth/codigo` por la respuesta uniforme 202, y agregar pruebas de límites y de respuesta uniforme.
- **Depende de:** confirmar antes del piloto qué contacto trae el padrón y de quién es. Si es del tutor, ESC-61 necesita una regla para que el alumno no dependa del teléfono de su tutor.

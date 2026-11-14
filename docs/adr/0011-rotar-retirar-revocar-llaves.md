# ADR-0011 · Rotar, retirar y revocar una llave son tres cosas distintas

**Estado:** aceptada, 2026-11-13 (Samuel). **Precisa:** el punto 7 de [ADR-0008](0008-formato-de-constancia.md), que sigue aceptada. **Historias:** ESC-63, ESC-07. **Pruebas:** C-47, C-55.

**Decisión:** el estándar usa tres palabras con tres efectos distintos. **Rotar** cambia la llave que firma y deja la anterior publicada para verificar. **Retirar** quita una llave rotada cuando ya venció todo lo que firmó. **Revocar** quita de inmediato una llave perdida o robada, y lo firmado con ella deja de verificar. Todas las llaves publicadas llevan `use: "sig"`.

## Contexto

- ESC-63 decía: «Rotar una llave no invalida lo firmado antes; retirarla sí».
- ADR-0008 (punto 7) y C-47 decían lo contrario: una llave **retirada** se queda en el JWKS como solo verificación y la constancia sigue válida.
- La misma palabra, «retirar», tenía dos efectos opuestos. Una implementación no podía cumplir las dos.
- ESP-CON proponía publicar la llave vieja con `use: verify-only`. RFC 7517 solo define `sig` y `enc` para `use`, así que una biblioteca de JOSE podría rechazar ese valor.
- La credencial de ESP-PLA ya seguía la regla correcta para rotar: «la anterior DEBE seguir publicada hasta que venza la última credencial que firmó».

## Opciones consideradas

| Opción | A favor | En contra |
| --- | --- | --- |
| A. Rotar, retirar y revocar (elegida) | Cada palabra tiene un efecto. Cubre la salida normal de una llave y el robo. Coincide con ADR-0008 y C-47. | Tres términos que hay que aprender. |
| B. Solo rotar y revocar | Más corto. | No nombra el momento en que una llave rotada sale del JWKS; quedaría implícito. |
| C. Mantener `use: verify-only` | Dice en el JWKS qué llave ya no firma. | No es un valor válido en RFC 7517. |

## Consecuencias

- **Obliga a:** corregir ESC-63, ESP-CON (sección de llaves y pregunta abierta 3) y ESP-PLA (`GET /v0/llaves`). Agrega C-55.
- **Se pierde:** el JWKS ya no dice cuál llave firma hoy. Lo sabe solo el servidor. Para verificar no hace falta saberlo.
- **Revocar tiene costo:** todas las constancias firmadas con esa llave dejan de verificar, y control escolar debe reemitir las que se necesiten. Es el comportamiento correcto ante un robo.
- **Deja abierto:** la API para generar, rotar, retirar y revocar llaves (P-16 en [Pendientes conocidos](../especificaciones/pendientes.md)).

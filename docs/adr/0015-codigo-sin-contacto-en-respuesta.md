# ADR-0015 · Pedir un código responde un mensaje genérico, sin el contacto

**Estado:** aceptada, 2026-11-19 (Samuel). **Reemplaza:** el punto 4 de [ADR-0009](0009-entrega-de-codigo.md). **Historias:** ESC-61. **Pruebas:** C-26, C-48.

**Decisión:** `POST /v0/auth/codigo` responde siempre 202 con exactamente el mismo cuerpo, exista o no la matrícula. El cuerpo es un mensaje genérico y **no muestra el contacto**, ni enmascarado. El resto de ADR-0009 sigue igual.

## Contexto

El punto 4 de ADR-0009 pedía dos cosas que no pueden cumplirse a la vez:

- «Responde siempre 202 **con el mismo texto**, exista o no la matrícula.» C-48 lo comprueba: la respuesta a una matrícula que no está en el padrón es igual a la de una que sí está.
- «Si existe, el texto **muestra el contacto enmascarado** (`a*****@c****.mx`).» C-26 lo comprueba.

Si la respuesta trae el contacto solo cuando la matrícula existe, ya no es la misma, y cualquiera puede saber qué matrículas están inscritas con solo pedir un código. Eso es justo lo que el punto 4 quería evitar. Se encontró al escribir el esquema de la respuesta en el contrato OpenAPI (P-06).

## Opciones consideradas

| Opción | A favor | En contra |
| --- | --- | --- |
| A. Mensaje genérico, sin contacto (elegida) | La respuesta es igual siempre, sin trucos. No revela quién está inscrito ni a dónde llega el código. | El alumno no ve a qué contacto se envió. Si su contacto está mal, lo descubre porque no le llega nada y acude a control escolar (C-30). |
| B. Contacto enmascarado siempre; si la matrícula no existe, el servidor inventa uno con la misma forma | Conserva la ayuda al alumno. | El contacto inventado tiene que parecer real y ser estable para la misma matrícula, o se nota. Es más código y más fácil de hacer mal. |
| C. Dejarlo abierto como pendiente | No decide nada todavía. | El contrato no puede fijar el esquema de la respuesta, que era el motivo de P-06. |

## Consecuencias

- **Obliga a:** ESP-CON 0.5 quita el contacto enmascarado de «Entrega y límites» y de C-26. El esquema `CodigoSolicitado` del contrato no admite más campo que `mensaje`.
- **No cambia:** la activación en persona (`POST /v0/auth/activacion`) sí responde con el contacto enmascarado, porque la pide control escolar con sesión y rol, no cualquiera.
- **Deja abierto:** si los alumnos se confunden por no ver el contacto, se puede mostrar después de iniciar sesión, donde ya no revela nada.
- **Principios:** privacidad por defecto. Ante la duda, la respuesta pública no dice nada que dependa de la persona.

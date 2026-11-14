# ADR-0010 · Las llaves públicas se publican en `GET /v0/llaves`

**Estado:** aceptada, 2026-11-13 (Samuel). **Historias:** ESC-63, ESC-07, ESC-45. **Pruebas:** C-03, C-41, C-47.

**Decisión:** la ruta oficial del JWKS (RFC 7517) es `GET /v0/llaves`. Un documento de descubrimiento en `/.well-known/` se podrá agregar después, y si se agrega DEBE apuntar a esa ruta con su campo `jwks_uri`.

## Contexto

- ESP-PLA define `GET /v0/llaves` y ESP-CON la usa para verificar constancias (C-41, C-47). El esqueleto de `contratos/openapi.yaml` en `esp-con-v0.2.0` usa `/.well-known/jwks.json`. Las dos no pueden ser la oficial.
- `/.well-known/jwks.json` parece una convención, pero no es un estándar:
  - **RFC 8615** reserva `/.well-known/` para metadatos de todo el sitio, solo con nombres registrados en IANA. `jwks.json` no está registrado.
  - Lo que sí está registrado son documentos de descubrimiento: `openid-configuration` (OpenID Connect Discovery 1.0) y `oauth-authorization-server` (RFC 8414). Los dos anuncian las llaves con `jwks_uri`, que puede ser cualquier URL. Google, por ejemplo, las publica en `/oauth2/v3/certs`.
  - **RFC 7517** define el formato del JWKS, no la ruta donde se publica.
- Quienes leen estas llaves no son solo clientes de OAuth. Son los escáneres sin conexión (credenciales `credencial-*`), las páginas de verificación y los verificadores externos (constancias `constancia-*`).
- ADR-008 solo exige que el JWKS esté en una «URL estable».

## Opciones consideradas

| Opción | A favor | En contra |
| --- | --- | --- |
| A. `GET /v0/llaves` (elegida) | Se versiona con el resto de la API, así que un cambio de formato en v1 no rompe a los escáneres ya instalados. Es lo que dicen ESP-PLA y ESP-CON. La entienden clientes que no hablan OAuth. | Una biblioteca OIDC no la encuentra sola: necesita que le digan la URL o un documento de descubrimiento. |
| B. `/.well-known/jwks.json` | La reconocen muchos desarrolladores. | No es un nombre registrado. No se puede versionar. Obliga a cambiar ESP-PLA. |
| C. Las dos, como alias | Sirve a todos. | Dos rutas oficiales para lo mismo, que hay que mantener iguales y probar dos veces. |

## Consecuencias

- **Obliga a:** corregir el esqueleto de `contratos/openapi.yaml` en el PCE del contrato, y decir en ESP-PLA que `GET /v0/llaves` es pública y estable durante toda la versión mayor.
- **Deja abierto (qué revisar más adelante):**
  1. **Si la plataforma pasa a ser proveedor de identidad.** Hoy ESP-PLA dice que las personas entran con OpenID Connect contra un proveedor externo, y ESC-61 emite sesiones propias. Si un sistema externo tiene que validar esas sesiones, hará falta `/.well-known/openid-configuration` con `jwks_uri` apuntando a `/v0/llaves`. Eso se escribe en otra ADR y no cambia esta ruta.
  2. **Si cambia el formato de las llaves** (por ejemplo, un miembro que diga qué llave firma hoy, o el estado de una llave rotada o revocada). Entonces se publica `GET /v1/llaves` y `/v0/llaves` se mantiene mientras haya escáneres en v0.
  3. **Si aparece un verificador que solo acepte `/.well-known/jwks.json`.** Revisar la opción C solo con un caso real de por medio, no por si acaso.
- **Principios:** el estándar manda sobre la costumbre. Se sigue lo que dicen los RFC, no una convención de proveedor.

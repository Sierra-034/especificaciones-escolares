# Cambios

Formato: una sección por etiqueta publicada.

## esp-con-v0.3.1 — 2026-11-17

Corrección: no cambia comportamiento ni pruebas.

- #14 Agregar la guía de adopción a ESP-CON (ESP-CON 0.3.1):
  - Nueva sección «Guía de adopción»: dependencias entre las 8 historias, criterio de adopción (escuelas, sin cambios), ruta de implementación (desarrolladores, 8 pasos con sus pruebas) y avance para el radar.
  - ESC-61 también depende de ESC-19.
  - El plan de constancias del catálogo de historias apunta a la guía (una sola fuente).
  - Pendientes nuevos P-20 (#15) y P-21 (#16).

## esp-con-v0.3.0 · esp-idp-v0.2.0 · esp-pla-v0.2.0 — 2026-11-13

Tres etiquetas sobre el mismo commit.

- #4 Documentar el proceso (manual 0, A–D) y la retrospectiva del arranque.
- #5 Agregar al manual la lista de procedimientos por agregar (E–K).
- #6 Corregir incongruencias de ESP-CON v0.2:
  - ESP-CON 0.3: el alumno pide su código con la matrícula; nueva forma de responder de `GET /v0/verificar/{folio}`; versiones de plantilla con `PUT`; permisos de lectura de constancias; `no-en-padron` solo en activación; límite por IP en `/verificar`; anulación idempotente; activación presencial sin código aparte; supuestos del padrón; pruebas C-51 a C-57.
  - ESP-IDP 0.2: catálogo único de roles y token de sesión.
  - ESP-PLA 0.2: el campo `rol` de la credencial pasa a `tipo`.
  - ADR 0010 (JWKS en `GET /v0/llaves`), 0011 (rotar, retirar y revocar) y 0012 (catálogo de roles).
  - Nueva página «Pendientes conocidos» con P-06, P-13 y P-16 a P-19.
  - Esqueleto de `contratos/openapi.yaml`: la verificación pública pasa a `/v0/verificar/{folio}` y el JWKS a `/v0/llaves`.

## esp-con-v0.2.0 — 2026-11-13
- Primera versión publicada del estándar.
- ESP-CON v0.2 (constancias): 8 historias, pruebas C-26 a C-50 en texto.
- ESP-IDP 0.1 y ESP-PLA 0.1 en borrador.
- ADR 0001–0005, 0008 y 0009; historias del catálogo migradas a docs/historias/.
- Pendiente: contrato OpenAPI completo, pruebas de conformidad en código, separar ESP-IDP de ESP-PLA.

# Cambios

Formato: una sección por etiqueta publicada.

## esp-con-v0.5.0 — 2026-11-18

Versión menor: el contrato OpenAPI queda completo y ESP-CON fija lo que faltaba para escribirlo. Cambia C-26.

- #20 Publicar el estándar con la licencia AGPL-3.0:
  - LICENSE con el texto oficial de la AGPL v3.0 y ADR-0014 (todo el repositorio, AGPL-3.0-or-later).
  - README con encabezado SPDX y sección «Licencia». No cambia ninguna especificación.
- #21 Escribir el contrato OpenAPI del MVP de constancias (ESP-CON 0.5):
  - `contratos/openapi.yaml` (contrato 0.3.0, OpenAPI 3.1): las 12 operaciones de ESP-CON y `GET /v0/llaves`, con esquemas, errores y, en cada ruta, `x-especificacion`, `x-historias`, `x-pruebas` y `x-roles`. Cubre C-26 a C-60.
  - ADR-0015: pedir un código responde un mensaje genérico, sin el contacto; reemplaza el punto 4 de ADR-0009. Cambia C-26.
  - ESP-CON 0.5: emitir pide el rol `alumno`; errores nuevos `solicitud-invalida`, `token-invalido` y `plantilla-ya-existe`.
  - Resuelve P-06 y P-17. Pendientes nuevos P-22 y P-23.
  - El CI valida el contrato con `openapi-spec-validator`.

## esp-con-v0.4.0 — 2026-11-17

Versión menor: cambia qué pruebas pide cada nivel del criterio de adopción. No cambia lo que hace una implementación.

- #18 Separar el criterio de adopción de ESP-CON de la puerta (ESP-CON 0.4):
  - ADR-0013: las pruebas de un nivel solo usan historias de ese nivel o de los anteriores; una especificación pide de otro subsistema solo las historias que usa.
  - El criterio de ESP-CON ya no pide C-01 a C-07, C-19, C-20 ni C-24 (credencial y puerta). De Identidad solo pide C-18, en su parte del servidor.
  - Nivel 1 = ESC-44 y ESC-63. ESC-19 pasa al nivel 2.
  - Pruebas nuevas C-58 (llaves publicadas), C-59 (el rol `alumno` no puede activar) y C-60 (lo emitido con una versión anterior de la plantilla sigue válido). C-32 ya no comprueba la verificación; C-33 cita también ESC-05.
  - Ruta de implementación: ESC-63 es el paso 2 y ESC-19 el 3.
  - Resuelve P-20 (#15).

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

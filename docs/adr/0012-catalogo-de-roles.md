# ADR-0012 · Un solo catálogo de roles y un token de sesión definido

**Estado:** aceptada, 2026-11-13 (Samuel). **Historias:** ESC-19, ESC-61, ESC-08, ESC-62. **Pruebas:** C-19, C-27, C-51.

**Decisión:** ESP-IDP tiene la única lista de roles del estándar: `alumno`, `control_escolar`, `direccion`, `responsable_sistema` y `personal_acceso`. El token de sesión trae `iss`, `sub`, `roles` (lista), `plantel`, `iat`, `exp` y `jti`. En la credencial de ESP-PLA, el campo `rol` pasa a llamarse `tipo`.

## Contexto

Había tres listas que no coincidían:

- ESP-CON usaba `alumno`, `responsable` y `control_escolar`.
- La credencial de ESP-PLA usaba `rol` con `alumno`, `personal` y `visitante`.
- ESC-19 y C-19 hablaban de dirección, responsable del sistema y personal de acceso.

Además, ninguna especificación decía qué trae el JWT de sesión, así que no se podía escribir el esquema de seguridad del contrato OpenAPI.

En el fondo se mezclaban dos ideas. El **tipo de persona** (lo que dice la credencial al cruzar la puerta) no es lo mismo que el **rol** (lo que la persona puede hacer en la plataforma). Una maestra es de tipo `personal`, y además puede tener el rol `control_escolar`.

## Opciones consideradas

| Opción | A favor | En contra |
| --- | --- | --- |
| A. Catálogo en ESP-IDP y `rol` → `tipo` en la credencial (elegida) | Una palabra, un significado. Nadie implementa todavía, así que renombrar no rompe nada. | Cambia ESP-PLA. |
| B. Catálogo en ESP-IDP y dejar `rol` en la credencial con una aclaración | No toca el formato de la credencial. | La misma palabra seguiría significando dos cosas. |

## Consecuencias

- **Obliga a:** ESP-IDP v0.2 (catálogo y token), ESP-PLA v0.2 (`tipo`) y ESP-CON v0.3 (usa `control_escolar` donde decía `responsable`).
- **ESC-08** dice «responsable administrativo». Le toca el rol `control_escolar`, porque en los planteles del MVP las plantillas las maneja esa área (confirmado por Samuel, 2026-11-13). Si otro plantel lo hace distinto, se agrega un rol con un PCE.
- **`roles` es una lista**, porque una persona puede tener más de uno.
- **Deja abierto** (los dos están en [Pendientes conocidos](../especificaciones/pendientes.md)):
    - Cómo se asignan los roles distintos de `alumno` (P-18).
    - ESP-PLA dice que las personas entran con OpenID Connect, y ESC-61 con un código propio (P-19).

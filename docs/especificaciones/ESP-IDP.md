---
id: ESP-IDP
version: 0.2.0
estado: borrador
---
# ESP-IDP · Identidad y acceso a la plataforma (v0.2)

> El texto de ESP-IDP v0.1 vive por ahora dentro de [ESP-PLA.md](ESP-PLA.md), porque la fuente
> ([Especificación v0.1: subsistema de acceso escolar](https://claude.ai/artifact/7T3STEZ5im4PVvaH1LJSBQ))
> cubre los dos subsistemas en un solo documento. Separarlos queda pendiente como PCE.

**Versión 0.2 (2026-11-13).** Agrega el catálogo único de roles y el contenido del token de sesión
(ADR-0012). Fija la ruta del JWKS en `GET /v0/llaves` (ADR-0010) y separa rotar, retirar y revocar
una llave (ADR-0011).

## Qué le toca a ESP-IDP

- **Historias:** ESC-19, 38, 44, 45, 46 (y ESC-63 en su versión mínima).
- **Pruebas:** C-01 a C-07, C-18, C-19, C-20, C-24.
- **Secciones de ESP-PLA.md que son de ESP-IDP:** Alcance y convenciones, Credencial, la parte de
  Administración de la API (importar padrón, emitir y revocar credenciales, llaves), y las filas de
  Identidad del Criterio de adopción.

## Catálogo de roles

Un **rol** dice qué puede hacer una persona en la plataforma. Es la única lista de roles del estándar:
cualquier especificación que pida un rol DEBE usar uno de esta tabla, con este nombre exacto. Un rol
nuevo entra por PCE a esta tabla.

| Rol | Quién lo tiene | Lo usan |
| --- | --- | --- |
| `alumno` | Toda persona del padrón de alumnos vigente. Sale del padrón (ESC-44). | ESP-CON |
| `control_escolar` | Personal de control escolar: plantillas, activación presencial, anulación, lectura de constancias. | ESP-CON |
| `direccion` | Dirección del plantel: consulta del registro de entradas. | ESP-PLA (C-19) |
| `responsable_sistema` | Administra la plataforma: llaves de firma, dispositivos, configuración. | ESP-IDP, ESP-PLA |
| `personal_acceso` | Personal de la puerta: solo ve el resultado del escaneo en curso. | ESP-PLA (C-19) |

- Una persona PUEDE tener más de un rol.
- Un rol no es lo mismo que el **tipo de persona** de la credencial de ESP-PLA (`tipo`: `alumno`,
  `personal`, `visitante`). El tipo dice quién eres al cruzar la puerta; el rol dice qué puedes
  hacer en la plataforma.
- Cómo se asignan los roles distintos de `alumno` todavía no está especificado: ver P-18 en
  [Pendientes conocidos](pendientes.md).

## Token de sesión

El token de sesión es un JWT firmado por el servidor que se envía en `Authorization: Bearer {token}`.

| Claim | Tipo | Descripción | Obligatorio |
| --- | --- | --- | --- |
| `iss` | string | Id del plantel que emite. | DEBE |
| `sub` | string | Id opaco de la persona. | DEBE |
| `roles` | array de string | Roles del catálogo de arriba. | DEBE |
| `plantel` | string | Plantel en el que vale la sesión. | DEBE |
| `iat` | number | Emisión (epoch UTC). | DEBE |
| `exp` | number | Vencimiento (epoch UTC); 30 minutos por omisión (ADR-0009). | DEBE |
| `jti` | string | Id único de la sesión, para anotar y cerrar sesiones. | DEBE |

Una ruta que pide un rol que no está en `roles` DEBE responder 403 `sin-permiso`.

## Llaves públicas

- Las llaves públicas de firma se publican en `GET /v0/llaves`, en formato JWKS (RFC 7517). Es una
  ruta pública y estable durante toda la versión mayor de la API (ADR-0010).
- Todas las llaves llevan `use: "sig"`. Rotar, retirar y revocar son tres acciones distintas
  (ADR-0011); la tabla está en [ESP-CON](ESP-CON.md#la-constancia-firmada).

## Lo que ESP-CON especifica por ahora en nombre de ESP-IDP

ESC-61 (entrar sin contraseña, con código de un solo uso) y ESC-63 (llaves de firma `constancia-*`) se
especifican hoy dentro de [ESP-CON](ESP-CON.md), con las pruebas C-26 a C-30, C-48 a C-50, C-52 y C-57.
Pasan a ESP-IDP en su versión 0.3.

# Pendientes conocidos

Incongruencias y huecos que **ya se encontraron** en las especificaciones y **todavía no se
resuelven**. Están aquí para que no se pierdan: cada uno dice qué falta, por qué no se resolvió
todavía y en qué PCE se resuelve.

**Cómo se usa esta lista:**

- Un pendiente nuevo entra con un PCE, igual que cualquier cambio.
- El PCE que resuelve un pendiente **borra su fila** de esta tabla y lo menciona en el CHANGELOG.
- Cada pendiente tiene un *issue* en GitHub con el mismo ID (`P-NN`) en el título, para poder discutirlo.
- Los números P-06 a P-17 vienen de la [revisión de ESP-CON v0.2 para el contrato OpenAPI](https://claude.ai/artifact/Q3p2bdLkLhM34DU9qTHkkL)
  (2026-11-13), que numeró las incongruencias del 1 al 17. Las que se resolvieron en ESP-CON v0.3 ya
  no aparecen. Los pendientes nuevos siguen desde P-20. Un ID no se reutiliza.

| ID | Especificación | Qué falta | Por qué no entró en ESP-CON v0.3 | Se resuelve en | ¿Bloquea algo? |
| --- | --- | --- | --- | --- | --- |
| P-06 | ESP-CON | **Cuerpos de las respuestas sin definir.** 202 de `auth/codigo` (texto con el contacto enmascarado), 200 de `auth/sesion` (token y vencimiento), 201 de emisión (¿trae la JWS o solo folio y URL del PDF?), 200 de anulación y 200 de activación. | Son esquemas: su lugar es el contrato, no el texto. | PCE del contrato OpenAPI (`pce/contrato-openapi`) | Sí: el contrato OpenAPI. |
| P-13 | ESP-CON | **El vector de prueba contradice la especificación.** `jti` no es UUID (`CON-2026-000001`); `plantilla` es un objeto y no `{id}@{version}`; `datos` usa `nombre_completo`, `grado` y `ciclo_escolar` en vez de `nombre`, `semestre` y `ciclo`, y no trae CURP; lleva `anulada: false` dentro de la JWS; `sub` es igual a la matrícula; `iss` usa un dominio con forma de plantel real en vez de `especificacion.example`. La llave de prueba solo trae la parte pública (`x`) y para firmar hace falta la privada (`d`). | Hay que generar llaves y firmas nuevas con una herramienta, no solo editar texto. | PCE de vectores (`pce/vectores-esp-con`) | Sí: las pruebas de conformidad en código. ESP-CON ya advierte que no se use. |
| P-16 | ESP-IDP | **ESC-63 no tiene API de administración.** Generar, rotar, retirar y revocar llaves (ADR-0011) no tienen ruta. ESC-63 es del nivel 1. | Es una capacidad nueva, no una corrección. | PCE de llaves (`pce/api-de-llaves`), con su ADR si hace falta | Sí: el nivel 1 de ESP-CON. |
| P-17 | Contrato | **Un solo `openapi.yaml` para varias especificaciones** con versiones distintas (ESP-CON 0.3, ESP-IDP 0.2, ESP-PLA 0.2), mientras `info.version` dice 0.2.0. Propuesta: `info.version` es la versión del contrato, y cada ruta lleva `x-especificacion: ESP-CON@0.3` y las historias que cubre. | Se decide al escribir el contrato. | PCE del contrato OpenAPI (`pce/contrato-openapi`) | Sí: el contrato OpenAPI. |
| P-18 | ESP-IDP | **Asignación de roles.** El catálogo (ADR-0012) dice qué roles existen, pero no cómo recibe alguien `control_escolar`, `direccion`, `responsable_sistema` o `personal_acceso`, ni quién los quita. `alumno` sale del padrón. | Se vio al escribir el catálogo. Es una capacidad nueva. | PCE aparte en ESP-IDP | Sí: sin esto, en el servidor de referencia los roles se cargan a mano. |
| P-19 | ESP-PLA, ESP-IDP | **Dos formas de entrar.** ESP-PLA dice que «las personas DEBEN entrar con un proveedor de identidad (OpenID Connect)», y ESC-61 (en ESP-CON) define un código propio de 6 dígitos con un JWT emitido por la plataforma. Hay que decidir si conviven (por ejemplo, OIDC para el personal y código para alumnos) o si una reemplaza a la otra. Ver también ADR-0010, «Deja abierto», punto 1. | Toca ESP-PLA y decide la arquitectura de identidad; pide su propia ADR. | PCE con ADR en ESP-IDP (se puede juntar con P-18) | No para el MVP de constancias; sí para la puerta. |

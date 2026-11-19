---
id: ESP-CON
version: 0.5.0
estado: borrador
---
# ESP-CON · Constancias y verificación (v0.5)

> Migrado el 2026-11-13 desde [Especificación v0.2: constancias y verificación (ESP-CON)](https://claude.ai/artifact/HadS5sL44Nwt2atfCpnbQv) (fecha del original: 2026-11-12). Texto copiado sin cambios; la fuente de verdad desde ahora es este archivo.

**Versión 0.5 (2026-11-19).** El [contrato OpenAPI](https://github.com/Sierra-034/especificaciones-escolares/blob/main/contratos/openapi.yaml) (`contratos/openapi.yaml`) pasa de esqueleto a contrato completo: las 12 operaciones de esta especificación y `GET /v0/llaves`, con esquemas, errores y, en cada ruta, sus historias y pruebas. Resuelve P-06 (cuerpos de las respuestas) y P-17 (versiones del contrato). Pedir un código responde un mensaje genérico, sin el contacto ([ADR-0015](../adr/0015-codigo-sin-contacto-en-respuesta.md)); C-26 cambia. Emitir una constancia pide el rol `alumno`. Errores nuevos: `solicitud-invalida`, `token-invalido` y `plantilla-ya-existe`. Pendientes nuevos P-22 y P-23.

**Versión 0.4 (2026-11-18).** Resuelve P-20: cada nivel del [criterio de adopción](#criterio-de-adopcion) pide solo pruebas de las historias de ese nivel o de los anteriores ([ADR-0013](../adr/0013-pruebas-de-cada-nivel.md)). Una escuela que adopta solo constancias ya puede declarar cualquier nivel sin la credencial ni la puerta. ESC-19 pasa del nivel 1 al 2, porque su prueba necesita la sesión de ESC-61. Agrega C-58 (llaves publicadas, ESC-63), C-59 (el rol `alumno` no puede activar, ESC-19) y C-60 (lo emitido con una versión anterior de la plantilla sigue válido). C-32 ya no comprueba la verificación: eso pasó a C-60.

**Versión 0.3.1 (2026-11-17).** Agrega la [Guía de adopción](#guia-de-adopcion): separa el **criterio de adopción** (qué declara una escuela) de la **ruta de implementación** (en qué orden se construye y qué se prueba en cada paso), con las dependencias entre historias y cómo se mide el avance para el radar. Corrige la dependencia de ESC-61, que también depende de ESC-19. No cambia comportamiento ni pruebas.

**Versión 0.3 (2026-11-13).** Corrige las incongruencias de la [revisión para el contrato OpenAPI](https://claude.ai/artifact/Q3p2bdLkLhM34DU9qTHkkL): el alumno pide su código con la matrícula; `GET /v0/verificar/{folio}` responde con `resultado`; los roles y el token de sesión salen del catálogo único de ESP-IDP (ADR-0012); rotar, retirar y revocar una llave son tres cosas distintas (ADR-0011); el JWKS vive en `GET /v0/llaves` (ADR-0010). Aclara versiones de plantilla, permisos de lectura, límites, anulación repetida y activación presencial. Agrega C-51 a C-57. Lo que se dejó fuera está en [Pendientes conocidos](pendientes.md).

**Versión 0.2 (2026-11-12).** Aplica [ADR-008 y ADR-009](https://claude.ai/artifact/BFv1HemHiY2yqZoTx7jqoc), aceptados por Samuel: QR con URL y folio, PDF/A-2b con la JWS adjunta, datos visibles al verificar, y código de 6 dígitos por el puerto Notificador. Corrige C-35, C-42, C-43 y el paso 1 de la validación. Agrega C-45 a C-50.

## Alcance y convenciones

ESP-CON v0.5 cubre el subsistema **Constancias y verificación**: emitir constancias de estudios en autoservicio, verificarlas por QR e invalidarlas. Usa cuatro historias del subsistema **Identidad y acceso a la plataforma** (ESP-IDP): padrón importado (ESC-44), roles mínimos (ESC-19), llaves de firma (ESC-63) e identificación sin contraseña (ESC-61). No requiere la credencial ni la puerta: el [criterio de adopción](#criterio-de-adopcion) dice qué pruebas pide de Identidad.

**Palabras normativas** (con el sentido de RFC 2119): **DEBE** es obligatorio. **DEBERÍA** es recomendado. **PUEDE** es opcional.

**Convenciones**

- Los IDs de alumno (`sub`) son opacos: no incluyen nombre, CURP ni matrícula directamente.
- Los folios de constancia son globalmente únicos (UUIDv4 o equivalente) y opacos.
- Las fechas y horas van en UTC, formato ISO 8601 (`2026-11-12T03:00:00Z`).
- Los textos se normalizan a NFC (Unicode). Dos cadenas se comparan en NFC.
- El dominio `especificacion.example` es provisional; se reemplaza en la implementación.
- Los **roles** y el contenido del **token de sesión** se definen en el [catálogo de roles de ESP-IDP](ESP-IDP.md#catalogo-de-roles). ESP-CON usa `alumno` y `control_escolar`.
- El alumno se identifica ante la API con su **matrícula**, que sí conoce. El `sub` es interno y el alumno nunca lo escribe.
- Las **llaves de firma** se describen en ESP-IDP (ESC-63). ESP-CON usa llaves con `kid` que empieza por `constancia-` para distinguirlas de las llaves de credencial (`credencial-`).

## Modelo de datos

Cinco entidades principales.

| Entidad | Descripción | Llave natural |
| --- | --- | --- |
| Alumno | Persona del padrón vigente. Viene de ESC-44. | `sub` (opaco) |
| Plantilla | Formato oficial de un tipo de constancia, con vigencia y versión. | `plantilla_id` + `version` |
| Constancia | Documento firmado emitido para un alumno a partir de una plantilla. | `folio` (UUID, opaco) |
| SolicitudRevision | Solicitud cuya plantilla requiere aprobación de control escolar antes de emitirse. Fuera del MVP. | `solicitud_id` |
| AuditoriaEmision | Registro inmutable de cada emisión: quién, cuándo, folio, versión de plantilla. | `folio` |

**Reglas**

- Una constancia es inmutable una vez emitida; anularla la marca, no la borra.
- Una plantilla vencida (`vigencia_fin < ahora`) no PUEDE usarse para nuevas emisiones.
- Cada emisión anota quién la pidió (`sub` del solicitante) y cuándo; las verificaciones externas se cuentan sin anotar quién consultó.
- Los datos de la constancia (nombre, CURP, matrícula, semestre, grupo, turno, ciclo) DEBEN venir del padrón; nunca se capturan manualmente.

**Plantilla**

```json
{
  "id": "constancia-estudios",
  "version": 1,
  "tipo": "estudios",
  "nombre": "Constancia de estudios",
  "vigencia_inicio": "2026-08-01",
  "vigencia_fin": "2027-07-31",
  "requiere_revision": false,
  "activa": true,
  "campos": ["nombre", "curp", "matricula", "semestre", "grupo", "turno", "ciclo"]
}
```

**Versiones de plantilla**

- `POST /v0/plantillas` crea una plantilla con un `id` nuevo, en su versión 1.
- `PUT /v0/plantillas/{id}` crea la versión siguiente del mismo `id`. En la misma transacción, la versión anterior queda `activa: false`. Solo hay una versión activa por `id`.
- Una emisión nueva usa siempre la versión activa. Las constancias ya emitidas con una versión anterior siguen siendo válidas: su JWS dice con qué versión se emitieron.
- `GET /v0/plantillas` lista solo las versiones activas y vigentes.

## La constancia firmada

Una constancia es un JWS (JSON Web Signature) con algoritmo EdDSA, igual que la credencial de ESP-IDP, pero con distinto `typ` y llave. El PDF que recibe el alumno es solo la presentación de la constancia (ADR-008). La anulación se guarda en el servidor, nunca en la JWS.

**Encabezado JWS**

| Campo | Valor |
| --- | --- |
| `alg` | `EdDSA` |
| `kid` | id de la llave de firma, empieza por `constancia-` |
| `typ` | `constancia+jwt` |

**Contenido del payload**

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `jti` | string | Folio (UUID, opaco). También el id de la constancia. |
| `iss` | string | Id del plantel. |
| `iat` | number | Momento de emisión (epoch UTC). |
| `exp` | number | Vencimiento (fin del ciclo escolar, epoch UTC). |
| `typ` | string | Tipo de constancia. En v0.5 solo existe `estudios`. |
| `sub` | string | Id opaco del alumno. |
| `plantilla` | string | `{id}@{version}` de la plantilla usada. |
| `datos` | object | Campos del alumno según la plantilla (nombre, CURP, matrícula, semestre, grupo, turno, ciclo). |

**Validación**

El verificador (página pública, sin cuenta ni app) DEBE, en este orden:

1. Pedir `GET /v0/verificar/{folio}` (el QR solo trae la URL). La respuesta trae la JWS, el `resultado` y los datos visibles (ver [Respuesta de verificación](#respuesta-de-verificacion)). Decodificar la JWS y obtener el `kid`.
2. Buscar la llave pública del plantel con ese `kid` en `GET /v0/llaves`. Si no está (por ejemplo, porque la llave fue revocada), el resultado es «firma inválida».
3. Verificar la firma EdDSA.
4. Comprobar que `exp > ahora`.
5. Comprobar que `resultado` no sea `anulada` (respuesta 410).
6. Mostrar los datos visibles para que quien verifica los compare con el papel; DEBEN coincidir con `datos`.

Cualquier fallo en los pasos 1–5 DEBE mostrar el resultado correspondiente (firma inválida, vencida, anulada) y nunca silenciarlo. La verificación por QR no pide cuenta ni instala app: el QR contiene la URL `https://{plantel}/verificar/{folio}` y el navegador la abre directamente.

### Respuesta de verificación

El servidor calcula `resultado` con lo que sabe: si el folio existe, si está anulado y si `exp` ya pasó. La firma la comprueba la página (pasos 2 y 3), que es la que muestra «firma inválida».

| Caso | HTTP | Cuerpo |
| --- | --- | --- |
| Vigente | 200 | `resultado: "valida"`, `jws`, `datos_visibles` |
| Vencida (`exp` ya pasó) | 200 | `resultado: "vencida"`, `jws`, `datos_visibles` |
| Anulada | 410 | Problem Details `constancia-anulada` con los miembros de extensión `resultado: "anulada"`, `jws`, `datos_visibles` y `anulada_en` (RFC 9457 permite miembros de extensión) |
| No existe | 404 | Problem Details `folio-no-encontrado` |

```json
{
  "resultado": "valida",
  "jws": "eyJhbGciOiJFZERTQSIs...",
  "datos_visibles": {
    "nombre": "Ana López Martínez",
    "plantel": "Plantel de ejemplo",
    "semestre": 3,
    "grupo": "A",
    "ciclo": "2026-2027",
    "emitida_en": "2026-11-12T16:00:00Z",
    "curp_enmascarada": "LOMA******MX**"
  }
}
```

**PDF (ADR-008)**

- Formato PDF/A-2b. Lleva los datos de la plantilla, el folio en texto legible, el QR, la leyenda «Verifique en {plantel}/verificar» y el espacio para la firma autógrafa.
- El QR lleva solo la URL `https://{plantel}/verificar/{folio}`, con corrección de errores nivel M y al menos 2.5 cm de lado.
- La JWS va incrustada como archivo adjunto `constancia.jws`, idéntica a la guardada en el servidor. Permite agregar después verificación sin red o firma electrónica del PDF sin cambiar el QR ni el folio.

**Datos visibles al verificar (ADR-008)**

La página pública muestra uno de cuatro resultados (válida, vencida, anulada, no encontrada) y, si existe, nombre completo, plantel, semestre, grupo, ciclo, fecha de emisión y CURP enmascarada (solo los 4 primeros caracteres y los 2 de la homoclave). NO DEBE mostrar la matrícula ni la CURP completa. El servidor DEBE limitar `GET /v0/verificar/{folio}` a 60 consultas por IP por minuto (configurable); al pasarse responde 429 `demasiadas-solicitudes`.

**Rotar, retirar y revocar llaves (ADR-0011)**

| Acción | Cuándo | Qué pasa en `GET /v0/llaves` | Qué pasa con lo ya firmado |
| --- | --- | --- | --- |
| **Rotar** | Cambio programado de llave | La llave nueva firma lo nuevo. La anterior sigue publicada, solo para verificar. | Sigue válido (C-47). |
| **Retirar** | Venció la última constancia que firmó una llave rotada | La llave sale del JWKS. | Nada: ya no queda nada vigente firmado con ella. |
| **Revocar** | La llave se perdió o la robaron | La llave sale del JWKS en ese momento. Queda anotado quién y cuándo. | Deja de verificar: la página muestra «firma inválida» (C-55). Control escolar DEBE reemitir lo que el alumno necesite. |

Todas las llaves del JWKS llevan `use: "sig"`. Cuál de ellas firma hoy lo sabe solo el servidor; el JWKS no lo dice.

## Inicio de sesión con código (ESC-61)

El sistema no guarda contraseñas. Para identificarse, el usuario recibe un código de un solo uso en el contacto que la escuela tiene registrado.

**Flujo**

1. El usuario pide un código: `POST /v0/auth/codigo` con su matrícula.
2. El servidor genera un código de 6 dígitos, lo guarda como HMAC con una llave del servidor y lo envía al contacto registrado (correo o teléfono) a través del puerto **Notificador**.
3. El usuario canjea el código: `POST /v0/auth/sesion` con su matrícula y el código.
4. El servidor responde con un token de sesión (JWT firmado por el servidor) válido por el tiempo configurado. Su contenido lo define el [catálogo de roles de ESP-IDP](ESP-IDP.md#token-de-sesion).

**Reglas**

- Solo entra quien está en el padrón.
- El código expira a los **10 minutos** (configurable).
- Tras **3 intentos fallidos** con el mismo código, el código queda invalidado y se DEBE pedir uno nuevo.
- Si el alumno no tiene contacto registrado, acude a control escolar, que **registra su contacto en persona** con `POST /v0/auth/activacion`. Desde ese momento el alumno entra con el flujo normal; no hay un código de activación aparte.
- Cambiar el contacto registrado solo se hace en persona ante control escolar, con la misma ruta.
- En `POST /v0/auth/sesion`, una matrícula que no está en el padrón responde 401 `codigo-invalido`, con el mismo cuerpo que un código incorrecto, para no revelar quién está inscrito (C-52).
- Cada inicio de sesión queda anotado con quién y cuándo.

**Entrega y límites (ADR-009)**

- `POST /v0/auth/codigo` responde siempre 202 con exactamente el mismo cuerpo, exista o no la matrícula: un mensaje genérico que no muestra el contacto, ni enmascarado ([ADR-0015](../adr/0015-codigo-sin-contacto-en-respuesta.md), que reemplaza el punto 4 de ADR-0009). Así no se puede sondear el padrón.
- Como mucho 3 solicitudes por matrícula cada 15 minutos y 20 por IP cada hora; al pasarse responde 429 `demasiadas-solicitudes`.
- Pedir un código nuevo invalida el anterior.
- El JWT de sesión dura 30 minutos (configurable).
- El código se envía con la operación `enviar_codigo(contacto, codigo, vence_en)` del puerto Notificador. Adaptadores: `buzon_simulado` (demo con la institución sintética, no envía nada), `correo` (paquete «Estándar»), y después `sms` y `whatsapp`. La institución elige el adaptador y su orden de respaldo en la configuración.

**Nota sobre los tests de ESC-61:** las pruebas C-26 a C-30, C-48 a C-50, C-52 y C-57 se incluyen en este documento para cubrir el MVP de constancias. Cuando ESP-IDP se revise para incluir ESC-61 formalmente, esas pruebas migrarán a ese documento.

## API

La API tiene prefijo `/v0`. Todos los endpoints autenticados requieren el header `Authorization: Bearer {token}`; sin token, o con uno vencido, responden 401 `token-invalido`. Son públicas `POST /v0/auth/codigo`, `POST /v0/auth/sesion`, la verificación por QR (`GET /v0/verificar/{folio}`) y las llaves (`GET /v0/llaves`).

Las tablas de abajo resumen la API. Los cuerpos de cada solicitud y respuesta, y todos sus errores, están en el contrato `contratos/openapi.yaml`, que manda en el detalle: cada ruta dice ahí qué historias atiende (`x-historias`) y qué pruebas la llaman (`x-pruebas`).

**Auth**

| Método | Ruta | Descripción | Historia |
| --- | --- | --- | --- |
| `POST` | `/v0/auth/codigo` | Solicitar código de acceso. Responde siempre 202. Body: `{"matricula": "..."}` | ESC-61 |
| `POST` | `/v0/auth/sesion` | Canjear código por token de sesión. Body: `{"matricula": "...", "codigo": "123456"}` | ESC-61 |
| `POST` | `/v0/auth/activacion` | Control escolar registra en persona el contacto de un alumno. Body: `{"matricula": "...", "contacto": "..."}`. Responde 200; 404 `no-en-padron` si la matrícula no existe. Requiere rol `control_escolar`. | ESC-61 |

**Plantillas**

| Método | Ruta | Descripción | Historia |
| --- | --- | --- | --- |
| `GET` | `/v0/plantillas` | Listar plantillas vigentes. Requiere sesión, con cualquier rol. | ESC-08 |
| `POST` | `/v0/plantillas` | Crear plantilla con un `id` nuevo (versión 1). Requiere rol `control_escolar`. Si el `id` ya existe responde 409 `plantilla-ya-existe`. | ESC-08 |
| `GET` | `/v0/plantillas/{id}` | Obtener una plantilla (versión activa). Requiere sesión, con cualquier rol. | ESC-08 |
| `PUT` | `/v0/plantillas/{id}` | Crear la versión siguiente; la anterior queda `activa: false`. Requiere rol `control_escolar`. | ESC-08 |

**Constancias**

| Método | Ruta | Descripción | Historia |
| --- | --- | --- | --- |
| `POST` | `/v0/constancias` | Emitir constancia. Body: `{"plantilla_id": "constancia-estudios"}`. Requiere sesión con el rol `alumno`; el `sub` viene del token. | ESC-05 |
| `GET` | `/v0/constancias/{folio}` | Obtener la JWS de la constancia. Solo el alumno dueño del folio (el `sub` del token es el de la constancia) o el rol `control_escolar`; cualquier otro recibe 403 `sin-permiso`. | ESC-05 |
| `GET` | `/v0/constancias/{folio}/pdf` | Descargar el PDF firmado. Mismo permiso que la ruta anterior. | ESC-05 |
| `GET` | `/v0/verificar/{folio}` | Verificación pública. Sin autenticación. Respuestas en [Respuesta de verificación](#respuesta-de-verificacion). | ESC-07 |
| `POST` | `/v0/constancias/{folio}/anular` | Anular constancia. Body: `{"motivo": "..."}`. Requiere rol `control_escolar`. Es idempotente: anular un folio ya anulado responde 200 con la anulación original y no cambia el motivo, quién ni cuándo. | ESC-62 |

**Reglas comunes**

- Los errores van en Problem Details (RFC 9457), campo `type` con URL estable.
- Las respuestas exitosas de emisión incluyen el folio, la JWS y la URL de descarga del PDF.
- El servidor DEBE responder en menos de 60 segundos para ESC-05 (objetivo: menos de 5).
- Una plantilla vencida en `POST /v0/constancias` responde `422 plantilla-vencida`.
- Un alumno fuera del padrón en `POST /v0/constancias` responde `403 no-inscrito`.
- Las llaves públicas se publican en `GET /v0/llaves` (ADR-0010), definida en ESP-IDP.

## Errores

Todo error DEBE ir en formato Problem Details (RFC 9457). El campo `type` es una URL estable bajo `https://especificacion.example/errores/`.

```json
{
  "type": "https://especificacion.example/errores/codigo-expirado",
  "title": "El código ha expirado",
  "status": 401,
  "detail": "El código venció a las 2026-11-12T04:00:00Z."
}
```

| Tipo | HTTP | Significado |
| --- | --- | --- |
| `solicitud-invalida` | 400 | El cuerpo no cumple con el esquema del contrato: falta un campo, sobra uno o el tipo no es el correcto. |
| `token-invalido` | 401 | Falta el token de sesión, venció o no lo firmó este servidor. |
| `codigo-expirado` | 401 | El código de acceso ya venció. |
| `codigo-invalido` | 401 | Código incorrecto. |
| `codigo-bloqueado` | 429 | Demasiados intentos fallidos; pedir código nuevo. |
| `no-en-padron` | 404 | La matrícula no existe en el padrón. Solo sale en `POST /v0/auth/activacion`, que pide rol `control_escolar`. Ninguna ruta que se use sin sesión lo devuelve. |
| `no-inscrito` | 403 | El alumno existe pero no está inscrito en el ciclo vigente. |
| `plantilla-vencida` | 422 | La plantilla solicitada ya no está vigente. |
| `plantilla-no-encontrada` | 404 | El id de plantilla no existe. |
| `plantilla-ya-existe` | 409 | Se intentó crear con `POST` una plantilla cuyo `id` ya existe; una versión nueva se crea con `PUT`. |
| `folio-no-encontrado` | 404 | El folio no existe en este plantel. |
| `constancia-anulada` | 410 | La constancia existe pero fue anulada. |
| `sin-permiso` | 403 | El rol del solicitante no permite esta operación. |
| `demasiadas-solicitudes` | 429 | Se pasó un límite de solicitudes: códigos por matrícula o por IP, o verificaciones por IP. |

## Pruebas de conformidad

Las pruebas C-26 a C-60 cubren este subsistema. Las pruebas C-01 a C-25 pertenecen a ESP-IDP y ESP-PLA; de ellas, ESP-CON solo pide C-18, en su parte del servidor (ver [Criterio de adopción](#criterio-de-adopcion)).

| ID | Pieza | Dado | Se espera | Historia |
| --- | --- | --- | --- | --- |
| C-26 | POST /v0/auth/codigo | matrícula con contacto registrado en padrón | 202; código enviado al contacto registrado; la respuesta no muestra el contacto (ADR-0015) | ESC-61 |
| C-27 | POST /v0/auth/sesion | código correcto dentro de 10 min | 200; JWT de sesión con `roles: ["alumno"]` y los claims de ESP-IDP | ESC-61 |
| C-28 | POST /v0/auth/sesion | código correcto después de 10 min | 401 `codigo-expirado` | ESC-61 |
| C-29 | POST /v0/auth/sesion | código incorrecto en el 3.° intento | 429 `codigo-bloqueado` | ESC-61 |
| C-30 | POST /v0/auth/activacion | rol `control_escolar`, matrícula sin contacto, contacto nuevo | 200; el contacto queda registrado y un `POST /v0/auth/codigo` posterior lo envía ahí | ESC-61 |
| C-31 | GET /v0/plantillas | — | 200; lista de plantillas con vigencia y versión | ESC-08 |
| C-32 | PUT /v0/plantillas/{id} | plantilla existente en versión 1 | versión 2 queda `activa: true` y la 1 `activa: false` en la misma transacción; `GET /v0/plantillas/{id}` devuelve la 2. Lo ya emitido con la 1 se prueba en C-60 | ESC-08 |
| C-33 | POST /v0/constancias | plantilla cuya `vigencia_fin` ya pasó | 422 `plantilla-vencida` | ESC-08, ESC-05 |
| C-34 | POST /v0/constancias | alumno inscrito, plantilla vigente | 201; `folio` único, JWS con firma EdDSA válida | ESC-05 |
| C-35 | GET /v0/constancias/{folio} | folio existente | 200; JWS íntegro recuperable | ESC-05 |
| C-36 | GET /v0/constancias/{folio}/pdf | folio existente | 200; PDF con datos correctos y QR apuntando a `/verificar/{folio}` | ESC-05 |
| C-37 | POST /v0/constancias | alumno no inscrito en el ciclo activo | 403 `no-inscrito` | ESC-05 |
| C-38 | GET /v0/verificar/{folio} | folio existente, constancia vigente | 200; `resultado: "valida"`, `jws` y `datos_visibles`, sin autenticación | ESC-07 |
| C-39 | GET /v0/verificar/{folio} | folio inexistente | 404 `folio-no-encontrado` | ESC-07 |
| C-40 | GET /v0/verificar/{folio} | folio de constancia anulada | 410 `constancia-anulada` con `resultado: "anulada"` y `datos_visibles` | ESC-07 |
| C-41 | Verificación EdDSA | JWS con `kid: constancia-*`, clave pública disponible en JWKS | firma matemáticamente válida; payload decodifica correctamente | ESC-07 |
| C-42 | Verificación de estado | folio anulado en el servidor; JWS con firma válida | resultado «anulada» aunque la firma sea válida | ESC-07 |
| C-43 | POST /v0/constancias/{folio}/anular | funcionario con rol `control_escolar` | 200; `anulada: true` persiste en BD | ESC-62 |
| C-44 | GET /v0/verificar/{folio} | folio anulado en C-43 | 410 `constancia-anulada` | ESC-62 |
| C-45 | GET /v0/constancias/{folio}/pdf | folio existente | PDF/A-2b con adjunto constancia.jws idéntico a la JWS guardada y folio legible | ESC-05 |
| C-46 | GET /v0/verificar/{folio} | constancia vigente | 200; CURP enmascarada, sin matrícula en la respuesta | ESC-07 |
| C-47 | GET /v0/verificar/{folio} | constancia vigente firmada con una llave constancia-\* ya rotada | 200; `resultado: "valida"`; la llave sigue en `GET /v0/llaves` y la página verifica la firma | ESC-07, ESC-63 |
| C-48 | POST /v0/auth/codigo | matrícula que no está en el padrón | 202 con el mismo cuerpo que una matrícula existente; no se envía nada | ESC-61 |
| C-49 | POST /v0/auth/codigo | 4.ª solicitud de la misma matrícula en 15 minutos | 429 `demasiadas-solicitudes` | ESC-61 |
| C-50 | POST /v0/auth/sesion | código anterior, después de pedir uno nuevo | 401 `codigo-invalido` | ESC-61 |
| C-51 | GET /v0/constancias/{folio} y /pdf | sesión de un alumno que no es dueño del folio | 403 `sin-permiso`; con el alumno dueño o con rol `control_escolar` responde 200 | ESC-05, ESC-19 |
| C-52 | POST /v0/auth/sesion | matrícula que no está en el padrón, cualquier código | 401 `codigo-invalido`, con el mismo cuerpo que un código incorrecto | ESC-61 |
| C-53 | GET /v0/verificar/{folio} | 61.ª consulta de la misma IP en un minuto | 429 `demasiadas-solicitudes` | ESC-07 |
| C-54 | POST /v0/constancias/{folio}/anular | folio ya anulado, motivo distinto | 200 con la anulación original; motivo, quién y cuándo no cambian | ESC-62 |
| C-55 | Verificación de firma | constancia firmada con una llave constancia-\* revocada | el `kid` ya no está en `GET /v0/llaves`; la página muestra «firma inválida» | ESC-07, ESC-63 |
| C-56 | GET /v0/verificar/{folio} | constancia no anulada cuyo `exp` ya pasó | 200; `resultado: "vencida"` | ESC-07 |
| C-57 | POST /v0/auth/activacion | rol `control_escolar`, matrícula que no está en el padrón | 404 `no-en-padron` | ESC-61 |
| C-58 | GET /v0/llaves | servidor con su llave de constancias configurada; sin autenticación | 200; JWKS (RFC 7517) con al menos una llave cuyo `kid` empieza por `constancia-`, con `kty: "OKP"`, `crv: "Ed25519"` y `use: "sig"`; ninguna llave trae la parte privada (`d`) | ESC-63 |
| C-59 | POST /v0/auth/activacion | sesión cuyo token solo trae `roles: ["alumno"]`; matrícula del padrón y contacto nuevo | 403 `sin-permiso`; el contacto registrado no cambia | ESC-19 |
| C-60 | GET /v0/verificar/{folio} | constancia emitida con la versión 1 de una plantilla que después pasó a la versión 2 (C-32) | 200; `resultado: "valida"`; el `plantilla` de la JWS sigue siendo `{id}@1` | ESC-07, ESC-08 |

### Vectores de prueba

!!! warning "Este vector contradice la especificación"
    El payload de abajo no cumple con esta versión: `jti` no es UUID, `plantilla` es un objeto, los nombres de `datos` son otros, falta la CURP, lleva `anulada` dentro de la JWS, el `sub` es la matrícula y la llave no trae su parte privada. Se corrige en un PCE aparte: ver P-13 en [Pendientes conocidos](pendientes.md). No lo uses para probar.

**Clave Ed25519 de prueba** — sólo para tests, nunca en producción:

```json
{
  "kid": "constancia-test-2026",
  "alg": "EdDSA",
  "crv": "Ed25519",
  "x": "11qYAYKxCrfVS_7TyWQHOg7hcvPapiMlrwIaaPcHURo"
}
```

**Payload mínimo válido (C-34, C-41):**

```json
{
  "jti": "CON-2026-000001",
  "iss": "https://cbtis-001.edu.mx",
  "iat": 1762992000,
  "exp": 1794528000,
  "typ": "estudios",
  "sub": "12345678",
  "plantilla": { "id": "constancia-estudios", "version": 1 },
  "datos": {
    "nombre_completo": "Ana López Martínez",
    "matricula": "12345678",
    "grado": 3,
    "grupo": "A",
    "turno": "matutino",
    "ciclo_escolar": "2026-2027"
  },
  "anulada": false
}
```

> Las pruebas de integración DEBEN usar un servidor local con estas claves de prueba; nunca apuntar a un plantel real.

## Guía de adopción

Esta sección responde dos preguntas distintas que antes estaban juntas:

| Pregunta | Para quién | Dónde | ¿Obliga? |
| --- | --- | --- | --- |
| ¿Qué nivel puede declarar mi escuela y qué tiene que pasar para declararlo? | Escuelas | [Criterio de adopción](#criterio-de-adopcion) | Sí: es la regla para declararse en un nivel. |
| ¿En qué orden construyo las historias y qué pruebo al terminar cada una? | Desarrolladores | [Ruta de implementación](#ruta-de-implementacion) | No: es una guía. No agrega obligaciones a una implementación. |

Las dos salen del mismo grafo: el campo `depende_de` de cada historia en `docs/historias/`. Si el grafo cambia, cambian las dos en el mismo PCE.

### Dependencias entre historias

Solo dependencias directas, como en el catálogo. Una flecha `A ──► B` se lee «B depende de A».

```text
ESC-44 ──────────► ESC-61 ──┐
                      ▲     │
ESC-19 ───────┬───────┘     ├──► ESC-05 ──► ESC-07 ──► ESC-62
              └──► ESC-08 ──┤
ESC-63 ─────────────────────┘
```

| Historia | Subsistema dueño | Depende de | Por qué |
| --- | --- | --- | --- |
| [ESC-44](../historias/ESC-44.md) · Importar el padrón | Identidad | — | Es la fuente de los alumnos y de sus datos. |
| [ESC-19](../historias/ESC-19.md) · Acceso por rol | Identidad | — | Da los roles `alumno` y `control_escolar` del token de sesión. |
| [ESC-63](../historias/ESC-63.md) · Llaves de firma | Identidad | — | Da la llave `constancia-*` y su publicación en `GET /v0/llaves`. |
| [ESC-61](../historias/ESC-61.md) · Entrar con código | Identidad | ESC-44, ESC-19 | Solo entra quien está en el padrón. La activación presencial pide el rol `control_escolar` (C-30, C-57) y el token lleva roles. |
| [ESC-08](../historias/ESC-08.md) · Plantillas con vigencia | Constancias | ESC-19 | Crear y versionar plantillas pide el rol `control_escolar`. |
| [ESC-05](../historias/ESC-05.md) · Constancia en autoservicio | Constancias | ESC-08, ESC-61, ESC-63 | Emitir pide sesión (ESC-61), una plantilla vigente (ESC-08) y una llave para firmar (ESC-63). |
| [ESC-07](../historias/ESC-07.md) · Verificar por QR | Constancias | ESC-05 | Solo se verifica lo que ya se emitió. |
| [ESC-62](../historias/ESC-62.md) · Anular | Constancias | ESC-07 | Su criterio «al verificarla aparece como anulada» se comprueba con `/verificar` (C-44). |

ESC-44, ESC-19, ESC-61 y ESC-63 son de Identidad: ESP-CON las exige, no es su dueña.

### Criterio de adopción

**Para escuelas.** Cada nivel es un **conjunto cerrado bajo “depende de”**. El nivel 2 es el mínimo para declarar adopción del subsistema en el radar.

| Nivel | Nombre | Historias requeridas | Pruebas que DEBEN pasar |
| --- | --- | --- | --- |
| 0 | Sin sistema | — | — |
| 1 | Base | ESC-44, ESC-63 | C-18 (de ESP-IDP, solo la parte del servidor), C-58 |
| 2 | Adopción mínima | Nivel 1 + ESC-19, ESC-61, ESC-08, ESC-05 | Las del nivel 1 + C-26..C-37, C-45, C-48..C-52, C-57, C-59 |
| 3 | Adopción plena | Nivel 2 + ESC-07, ESC-62 | Las del nivel 1 + C-26..C-60 |
| 4 | *(no definido todavía)* | — | — |

Un plantel declara el nivel más alto cuyo conjunto completo de historias está implementado y cuyas pruebas pasan.

**Cada prueba de un nivel usa solo historias de ese nivel o de los anteriores** ([ADR-0013](../adr/0013-pruebas-de-cada-nivel.md)). Así cada nivel se puede comprobar por sí solo. Por eso ESC-19 está en el nivel 2 y no en el 1: su prueba (C-59) necesita la sesión de ESC-61.

!!! note "Lo que ESP-CON pide de Identidad"
    De ESP-IDP, ESP-CON pide cuatro historias (ESC-44, ESC-19, ESC-63 y ESC-61) y, de las pruebas C-01 a C-25, solo C-18 en su parte del servidor. No pide la credencial ni la puerta (C-01 a C-07, C-19, C-20, C-24): una escuela que adopta solo constancias puede llegar al nivel 3.

    El eje de Identidad del radar se mide aparte, con su propio criterio (hoy en [ESP-PLA](ESP-PLA.md)). Esa misma escuela puede tener Constancias en nivel 3 e Identidad por debajo del 2, y el radar lo muestra así.

**El demo de referencia alcanza nivel 3** con una institución sintética de \~800 alumnos, una plantilla «constancia de estudios» y una clave de firma Ed25519 local.

> El radar de adopción usa el nivel alcanzado (0–4) como valor del eje «Constancias y verificación». El avance hacia el siguiente nivel se mide con la ruta de implementación: ver [Avance para el radar](#avance-para-el-radar). El radar se describe en el [índice de especificaciones](index.md).

### Ruta de implementación

**Para desarrolladores. Es una guía:** no cambia lo que una implementación DEBE hacer; eso lo dicen las secciones de arriba y las pruebas.

La ruta se lee de arriba abajo. Las historias de una misma **etapa** no dependen entre sí: se pueden hacer en cualquier orden o al mismo tiempo. Una historia empieza cuando las historias de las que depende ya pasan sus pruebas.

Cada prueba aparece en el **primer paso en que existen todas las rutas que usa**, aunque cite otra historia. Por eso C-33 se corre en el paso de ESC-05, que es quien expone `POST /v0/constancias`, y C-59, la prueba de ESC-19, en el paso de ESC-61, que es quien da la sesión.

| Etapa | Paso | Historia | Depende de | Pruebas que se corren al terminar el paso | Completa el nivel | Qué se tiene al terminar |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | ESC-44 | — | C-18 | — | Padrón de la institución sintética cargado, con los textos en NFC. |
| 0 | 2 | ESC-63 | — | C-58 | 1 | Llave `constancia-*` publicada en `GET /v0/llaves`. |
| 0 | 3 | ESC-19 | — | Ninguna en este paso: su prueba, C-59, necesita la sesión y se corre en el paso 4. | — | Token de sesión con `roles`; 403 `sin-permiso` si falta el rol. |
| 1 | 4 | ESC-61 | ESC-44, ESC-19 | C-26..C-30, C-48..C-50, C-52, C-57, C-59 | — | El alumno entra con código; el adaptador `buzon_simulado` del Notificador basta para el demo. |
| 1 | 5 | ESC-08 | ESC-19 | C-31, C-32 | — | Plantilla «constancia de estudios» versionada. |
| 2 | 6 | ESC-05 | ESC-08, ESC-61, ESC-63 | C-33..C-37, C-45, C-51 | 2 | El alumno descarga su constancia en PDF/A-2b, firmada, con folio y QR. |
| 3 | 7 | ESC-07 | ESC-05 | C-38..C-42, C-46, C-47, C-53, C-55, C-56, C-60 | — | Cualquiera verifica una constancia abriendo su QR. |
| 4 | 8 | ESC-62 | ESC-07 | C-43, C-44, C-54 | 3 | Control escolar anula una constancia y la verificación lo muestra. |

**Camino crítico:** cinco pasos, por ejemplo ESC-44 → ESC-61 → ESC-05 → ESC-07 → ESC-62. Ninguna implementación puede llegar al nivel 3 en menos pasos seguidos, aunque tenga más personas: lo que sí se reparte son las etapas 0 y 1.

**Una sola persona** puede seguir los pasos en orden, del 1 al 8.

**Lo que la ruta necesita y la especificación todavía no define:**

- Administrar llaves (generar, rotar, retirar, revocar) no tiene API (P-16). Mientras tanto, el paso 2 crea la llave por configuración del servidor.
- Asignar los roles distintos de `alumno` no está especificado (P-18). Mientras tanto, el paso 3 los carga a mano para la institución sintética.

### Avance para el radar

El radar dibuja, en el eje «Constancias y verificación», el **nivel declarado** (0–4) del criterio de adopción. La ruta agrega el **avance hacia el siguiente nivel**:

```text
avance = pasos del siguiente nivel terminados ÷ pasos del siguiente nivel
```

- Un paso está **terminado** cuando pasan todas las pruebas de su fila en la ruta. El paso 3 (ESC-19) no tiene pruebas en su fila: está terminado cuando pasa C-59.
- Pasos de cada nivel: nivel 1 = pasos 1 y 2; nivel 2 = pasos 3 a 6; nivel 3 = pasos 7 y 8.
- **Ejemplo:** un plantel en nivel 2 con el paso 7 terminado y el 8 no está en nivel 2 con avance de 1 ÷ 2 = 50 % hacia el 3.

El avance no cambia el nivel declarado: un plantel sigue en nivel 2 hasta terminar todos los pasos del nivel 3.

## Fuera de v0.5 y preguntas abiertas

### No incluido en esta versión

| Elemento | Estado | Notas |
| --- | --- | --- |
| Firma autógrafa del director (imagen o e.firma SAT) | Horizonte | Requiere ADR propio; complejidad legal y técnica alta |
| Cola de revisión previa (ESC-06) | Horizonte | Activar con `requiere_revision: true` en la plantilla |
| Tipos adicionales: traslado, historial de calificaciones, conducta | Horizonte | Nuevas plantillas; misma infraestructura de firma |
| Tutores y padres solicitando constancias (ESC-21) | Horizonte | Rol `tutor`; requiere relación tutor-alumno en padrón |
| Expediente digital (ESC-10, ESC-11) | Otro subsistema | Pertenece a «Control escolar» |
| Firma múltiple director + secretario | No considerado | Esperar caso de uso real antes de diseñar |

### Pendientes conocidos

Las incongruencias que se encontraron y no se resolvieron en esta versión están en [Pendientes conocidos](pendientes.md), cada una con el PCE donde se resuelve.

### Supuestos del padrón

La especificación asume que `Alumno` incluye al menos: matrícula, nombre, CURP, contacto (correo o teléfono), semestre, grupo, turno y ciclo activo. Son los campos que lleva la plantilla. Si el padrón de la institución usa campos distintos, se requiere un adaptador antes del puerto `Padrón`.

### Preguntas abiertas

1. **Sin contacto en padrón:** ¿cómo se comunica el código a un alumno cuyo padrón no tiene correo ni teléfono? Hoy: activación presencial (C-30). ¿Se necesita un canal adicional?
2. **Migración de ESC-61 a ESP-IDP:** las pruebas C-26–C-30, C-48–C-50, C-52 y C-57 viven temporalmente en ESP-CON. Cuando ESP-IDP v0.3 incluya formalmente ESC-61, se mueven allá y aquí queda sólo la referencia cruzada. Lo mismo vale para C-58 (ESC-63) y C-59 (ESC-19).
3. **Rotación de clave de firma:** ¿qué pasa con constancias ya emitidas si se rota el par `constancia-*`? Resuelto en ADR-008 y precisado en ADR-0011: rotar deja la llave anterior publicada para verificar hasta que venza lo último que firmó; retirarla es quitarla después de eso; revocarla (robo) la quita de inmediato. Todas llevan `use: "sig"`, porque `verify-only` no es un valor válido de `use` en RFC 7517.
4. **Formato del PDF:** ADR-008 fija PDF/A-2b, la JWS adjunta y el QR; esta versión no prescribe márgenes, tipografía ni logotipo; eso queda como configuración de plantilla. Puede requerir un ADR si la SEP establece un formato oficial.

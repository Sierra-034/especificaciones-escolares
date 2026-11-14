---
id: ESP-PLA
version: 0.2.0
estado: borrador
---
# ESP-PLA · Acceso al plantel (v0.2, junto con ESP-IDP)

> Migrado el 2026-11-13 desde [Especificación v0.1: subsistema de acceso escolar](https://claude.ai/artifact/7T3STEZ5im4PVvaH1LJSBQ) (fecha del original: 2026-11-10). Texto copiado sin cambios; la fuente de verdad desde ahora es este archivo.

> **Nota de migración.** La fuente cubre ESP-IDP y ESP-PLA en un mismo documento y dice que se separan al pasar al repositorio. Separarlas cambia qué sección pertenece a cuál, así que se deja como decisión de Samuel (PCE aparte). Mientras tanto el texto completo vive aquí y [ESP-IDP](ESP-IDP.md) apunta a sus secciones.

**Versión 0.2 (2026-11-13).** El campo `rol` de la credencial pasa a llamarse `tipo`, para no confundirlo con los roles de la plataforma, que ahora viven en el [catálogo de roles de ESP-IDP](ESP-IDP.md#catalogo-de-roles) (ADR-0012). C-19 usa los nombres de ese catálogo. `GET /v0/llaves` queda como la ruta oficial del JWKS (ADR-0010).

## Alcance y convenciones

Esta especificación define los contratos que cualquier implementación del subsistema de acceso debe cumplir: el formato de la credencial, el hecho de entrada, la API entre dispositivos y servidor, la configuración y las pruebas que lo verifican. No dice cómo programarlo. Sus decisiones vienen del [Diseño del MVP](https://claude.ai/artifact/8z2qFXRnnrty1u4cJAGH4R).

**Cubre v0.1:** emisión y validación de credenciales, registro de entradas sin conexión, sincronización, revocación, importación del padrón, configuración en capas y horarios por grupo.

**Dos subsistemas en un documento.** Esta especificación cubre dos subsistemas que se adoptan por separado:

- **Identidad y acceso a la plataforma (ESP-IDP):** padrón, roles, formato de la credencial, llaves, revocación y cómo verifica una credencial cualquier verificador. Es la base de todos los subsistemas.
- **Acceso al plantel (ESP-PLA):** hecho de entrada, sincronización, puntos de acceso, dispositivos, latido, configuración y retardos. Es opcional y usa ESP-IDP.

Viven juntas mientras son borrador. Se separan en dos documentos cuando pasen al repositorio.

**Palabras normativas** (con el sentido de RFC 2119): **DEBE** es obligatorio para pasar las pruebas; **DEBERÍA** es recomendado y se puede omitir con una razón escrita; **PUEDE** es opcional.

**Convenciones**

- Fechas y horas DEBEN viajar en UTC con formato RFC 3339; la zona del plantel se guarda aparte como nombre IANA (`America/Mexico_City`).
- Todo texto DEBE normalizarse a Unicode NFC antes de guardarse o compararse.
- Los identificadores DEBEN ser opacos (UUID versión 7) y no revelar nombre, matrícula ni orden de alta.
- El intercambio es JSON en UTF-8 sobre HTTPS con TLS 1.2 o superior.
- La especificación usa versionado semántico. Un cambio que rompe contratos sube la versión mayor y lleva su ADR.

## Modelo de datos

Ocho entidades, todas dentro de un plantel. El hecho de entrada es el centro: todo lo demás lo explica (quién, con qué credencial, en qué punto) o lo produce (el dispositivo que lo anota).

> **Diagrama pendiente.** En la fuente aquí hay un diagrama del modelo de datos (8 entidades) que no se pudo exportar a Markdown. Por redibujar en Mermaid.

La línea punteada no es una referencia guardada: el horario del grupo solo se usa al calcular retardos. La lista de revocadas es un conjunto de `jti` de credenciales y por eso no aparece como entidad propia.

## Credencial

La credencial es un JWS compacto (RFC 7515) firmado por el servidor del plantel con Ed25519 (`alg: EdDSA`), que se muestra como código QR. Ed25519 da firmas de 64 bytes, así el QR sigue siendo legible en pantallas pequeñas. La credencial DEBE NO llevar nombre, CURP, matrícula ni foto.

**Encabezado**

| Campo | Valor | Obligatorio |
| --- | --- | --- |
| `alg` | `EdDSA` | DEBE |
| `typ` | `acceso-escolar+jwt` | DEBE |
| `kid` | Identificador de la llave que firmó | DEBE |

**Contenido**

| Campo | Significado | Obligatorio |
| --- | --- | --- |
| `iss` | ID del plantel que emite | DEBE |
| `sub` | ID opaco de la persona | DEBE |
| `jti` | ID de esta credencial; cambia si se repone | DEBE |
| `iat` | Fecha de emisión | DEBE |
| `nbf` | Válida desde (inicio del semestre) | DEBE |
| `exp` | Válida hasta (fin del semestre) | DEBE |
| `tipo` | Tipo de persona: `alumno`, `personal` o `visitante`. No es un rol de la plataforma (ESP-IDP). | DEBE |
| `v` | Versión de esta especificación | DEBE |

**Llaves.** El servidor guarda la llave privada; los dispositivos reciben solo las públicas, identificadas por `kid`. Una llave nueva DEBE publicarse antes de usarse para firmar, y la anterior DEBE seguir publicada hasta que venza la última credencial que firmó.

**Nombre y grupo en pantalla.** Como el QR no los lleva, el escáner DEBE tener un *padrón de puerta* local con solo `sub`, nombre y grupo, cifrado en el dispositivo. Si el `sub` no está en su copia, la pantalla DEBE decir «válida, sin datos locales» y no rechazarla.

**Validación en el escáner**, en este orden; el primer fallo da el resultado:

1. Se puede leer como JWS con `typ` correcto → si no, `no_legible`.
2. El `kid` es conocido y la firma verifica → si no, `firma_invalida`.
3. `iss` es el plantel del dispositivo → si no, `otro_plantel`.
4. `nbf` ≤ ahora ≤ `exp`, con 5 minutos de tolerancia por reloj desajustado → si no, `vencida`.
5. `jti` no está en la lista de revocadas → si no, `revocada`.
6. Todo bien → `valida`.

Cualquier resultado distinto de `valida` DEBE mostrarse como aviso y DEBE NO bloquear la entrada: decide la persona en la puerta (ADR-005).

## Hecho de entrada

Cada entrada, escaneada o manual, se guarda como un hecho inmutable en el dispositivo y después se sincroniza. Un hecho DEBE NO editarse ni borrarse; una corrección es un hecho nuevo que apunta al anterior.

```json
{
  "id": "0193a1c2-7f3e-7c11-9b2a-5d1e8f0a4b21",
  "tipo": "qr",
  "plantel": "0193a1b0-0000-7000-8000-000000000001",
  "punto_acceso": "0193a1b0-0000-7000-8000-0000000000a1",
  "dispositivo": "0193a1b0-0000-7000-8000-0000000000d1",
  "sub": "0193a1b5-2c4d-7e8f-9a0b-1c2d3e4f5a6b",
  "jti": "0193a1b6-3d4e-7f80-8a1b-2c3d4e5f6a7b",
  "resultado": "valida",
  "decision": "entra",
  "ocurrio_en": "2026-11-10T13:02:41Z",
  "reloj_dispositivo": "2026-11-10T13:02:43Z",
  "corrige_a": null
}
```

| Campo | Regla |
| --- | --- |
| `id` | UUID v7 generado en el dispositivo; es también la clave de idempotencia |
| `tipo` | `qr`, `manual` (alumno sin QR) o `visitante` |
| `sub`, `jti` | Del QR si `tipo` es `qr`; `sub` puede faltar en `manual` y `visitante` |
| `resultado` | El de la validación de la credencial; `sin_credencial` en `manual` y `visitante` |
| `decision` | Lo que decidió la persona en la puerta: `entra` o `no_entra` |
| `ocurrio_en` | Hora del escaneo según el dispositivo, en UTC |
| `reloj_dispositivo` | Hora del dispositivo al guardar; sirve para detectar relojes desajustados |
| `corrige_a` | `id` del hecho que corrige, o `null` |

Un visitante DEBE llevar además `visitante_nombre` y `visitante_motivo` como texto libre. El servidor agrega `recibido_en` al recibirlo; el dispositivo DEBE NO enviarlo.

**Reglas del servidor**

- Un hecho con un `id` ya recibido DEBE aceptarse sin duplicarse (respuesta igual a la primera).
- Los retardos DEBEN calcularse con `ocurrio_en`, nunca con `recibido_en`.
- Si `ocurrio_en` difiere de la hora del servidor en más de 24 horas al recibirlo, el hecho DEBE guardarse con una marca de revisión, no rechazarse.

## API

La API tiene operaciones para dos tipos de cliente: los dispositivos de la puerta y las personas que administran. El detalle de cada una se escribirá como archivo OpenAPI 3.1 derivado de esta tabla; las implementaciones se prueban contra ese archivo, no al revés.

**Dispositivos de la puerta**

| Operación | Ruta | Qué hace |
| --- | --- | --- |
| Enviar hechos | `POST /v0/hechos` | Recibe un lote de hasta 500 hechos; responde por cada uno `aceptado`, `duplicado`, `en_revision` o `rechazado` |
| Bajar revocadas | `GET /v0/revocadas?desde=<cursor>` | Devuelve los `jti` revocados desde el cursor y un cursor nuevo |
| Bajar llaves | `GET /v0/llaves` | Llaves públicas en formato JWKS (RFC 7517): las que firman hoy y las rotadas que aún tienen algo vigente firmado; nunca las revocadas. Ruta pública y estable (ADR-0010, ADR-0011) |
| Bajar padrón de puerta | `GET /v0/padron-puerta?desde=<cursor>` | Cambios de `sub`, nombre y grupo desde el cursor |
| Bajar configuración | `GET /v0/configuracion` | Configuración efectiva del punto de acceso del dispositivo |
| Latido | `POST /v0/latido` | El dispositivo avisa que está vivo, con su hora y hechos pendientes |

**Administración**

| Operación | Ruta | Qué hace |
| --- | --- | --- |
| Importar padrón | `POST /v0/padron/importaciones` | Recibe el CSV del plantel; responde con altas, cambios, bajas y errores por renglón |
| Emitir credencial | `POST /v0/credenciales` | Firma una credencial para un `sub` |
| Revocar credencial | `POST /v0/credenciales/{jti}/revocacion` | Agrega el `jti` a la lista de revocadas, con motivo |
| Consultar entradas | `GET /v0/entradas?fecha=&punto_acceso=` | Entradas del día, derivadas de los hechos |
| Consultar retardos | `GET /v0/retardos?fecha=&grupo=` | Retardos contra el horario de cada grupo |
| Cambiar configuración | `PATCH /v0/configuracion/{capa}` | Habilita o deshabilita elementos; queda registrado como hecho |

**Reglas comunes**

- Cada dispositivo DEBE registrarse una vez y usar un token propio que se puede revocar. Las personas DEBEN entrar con un proveedor de identidad (OpenID Connect); el sistema DEBE NO guardar contraseñas.
- Las listas DEBEN paginarse con cursores opacos, nunca con números de página.
- Toda escritura de administración DEBE aceptar una cabecera `Idempotency-Key`.
- Un cambio de configuración DEBE usar `If-Match` con el ETag leído, para no pisar el cambio de otra persona.

## Configuración y horarios

La configuración tiene tres capas: paquete, plantel y punto de acceso. La configuración efectiva se calcula aplicando cada capa sobre la anterior. Las capas de plantel y punto de acceso DEBEN guardar solo lo que cambian, nunca una copia del paquete.

```json
{
  "paquete": "estandar",
  "version_paquete": "0.1.0",
  "elementos": {
    "acceso_vehicular": { "habilitado": false },
    "lista_retardos": { "habilitado": true, "tolerancia_min": 10 },
    "visitantes": { "habilitado": true }
  }
}
```

El ejemplo es la capa de un plantel: solo trae los elementos que difieren del paquete Estándar. Cada cambio de una capa DEBE guardarse como hecho con quién lo hizo, cuándo, el valor anterior y el nuevo.

**Horario por grupo.** La hora de entrada no es una por turno. Cada grupo tiene un horario semanal y la primera clase de cada día define su hora de entrada; el turno solo agrupa.

```json
{
  "grupo": "3B",
  "turno": "matutino",
  "vigencia": { "desde": "2026-08-24", "hasta": "2027-01-15" },
  "primera_clase": { "lun": "07:00", "mar": "08:00", "mie": "07:00", "jue": "09:00", "vie": "07:00" }
}
```

Las horas del horario son locales del plantel. Para calcular un retardo, el servidor DEBE convertir `ocurrio_en` a la zona del plantel y compararlo con la primera clase del grupo del alumno ese día más la tolerancia. Un día sin primera clase para ese grupo DEBE NO generar retardos.

Este mismo horario es la entrada del modelo de llegadas: la curva λ(t) esperada sale de sumar las llegadas de cada grupo antes de su primera clase.

## Errores

Todo error de la API DEBE responderse con Problem Details (RFC 9457), con `type` estable para que el cliente decida qué hacer sin leer el texto.

```json
{
  "type": "https://especificacion.example/acceso/errores/configuracion-cambiada",
  "title": "La configuración cambió desde que la leíste",
  "status": 412,
  "detail": "Otra persona deshabilitó el acceso vehicular a las 08:14."
}
```

| `type` (último segmento) | Estado HTTP | Cuándo |
| --- | --- | --- |
| `token-invalido` | 401 | Token de dispositivo o persona ausente, vencido o revocado |
| `sin-permiso` | 403 | El rol no permite la operación |
| `lote-muy-grande` | 413 | Más de 500 hechos en un envío |
| `configuracion-cambiada` | 412 | El `If-Match` no coincide con el ETag actual |
| `padron-invalido` | 422 | El CSV no tiene las columnas obligatorias; los errores por renglón van en la respuesta normal |

El dominio `especificacion.example` es provisional hasta que la especificación tenga dónde publicarse.

Un hecho con datos inválidos dentro de un lote DEBE NO hacer fallar el lote completo: se responde `rechazado` con su motivo solo para ese hecho.

## Pruebas de conformidad

Una implementación cumple v0.1 si pasa todas estas pruebas. Cada prueba tiene un ID estable para citarla («falla C-07») y se ejecuta con datos sintéticos, nunca con datos reales.

| ID | Pieza | Dado | Se espera | Historia |
| --- | --- | --- | --- | --- |
| C-01 | Escáner | Credencial correcta y vigente | `valida`, con nombre y grupo del padrón de puerta | ESC-29 |
| C-02 | Escáner | Credencial con un byte del contenido alterado | `firma_invalida` | ESC-29 |
| C-03 | Escáner | Credencial firmada con un `kid` desconocido | `firma_invalida` | ESC-29, ESC-63 |
| C-04 | Escáner | Credencial de otro plantel | `otro_plantel` | ESC-29 |
| C-05 | Escáner | `exp` vencido hace 1 hora | `vencida` | ESC-29 |
| C-06 | Escáner | `exp` vencido hace 3 minutos | `valida` (dentro de la tolerancia) | ESC-29 |
| C-07 | Escáner | `jti` en la lista de revocadas | `revocada` | ESC-46, ESC-29 |
| C-08 | Escáner | Cualquier resultado que no sea `valida` | Aviso en pantalla; la entrada se puede registrar como `entra` | ESC-29 |
| C-09 | Escáner | Dispositivo sin red | Valida y guarda el hecho igual que con red | ESC-29 |
| C-10 | Escáner | `sub` válido que no está en el padrón local | «válida, sin datos locales» | ESC-29 |
| C-11 | Servidor | El mismo lote enviado dos veces | Un solo registro por `id`; la segunda respuesta dice `duplicado` | ESC-29 |
| C-12 | Servidor | Escaneo con `ocurrio_en` a las 07:12 recibido a las 11:00, grupo con primera clase a las 07:00 y tolerancia de 10 min | Retardo de 2 min, calculado con `ocurrio_en` | ESC-41 |
| C-13 | Servidor | Lote de 3 hechos con uno inválido | 2 `aceptado` y 1 `rechazado`; el lote no falla | ESC-29 |
| C-14 | Servidor | `ocurrio_en` 3 días atrás | `en_revision` | ESC-29 |
| C-15 | Servidor | Cambio de configuración con ETag viejo | 412 `configuracion-cambiada` | ESC-43 |
| C-16 | Servidor | Deshabilitar el acceso vehicular | El punto deja de aparecer en la configuración efectiva y el cambio queda registrado | ESC-43 |
| C-17 | Servidor | Exportación completa | Todos los hechos, el padrón y la configuración salen en JSON y CSV sin pérdida | ESC-48 |
| C-18 | Ambos | Nombre con acento compuesto de dos formas distintas | Se guardan y comparan igual tras normalizar a NFC | ESC-44 |
| C-19 | Servidor | Una persona con rol `personal_acceso` pide `GET /entradas` | 403 con Problem Details; con rol `direccion` responde y la consulta queda anotada con quién y cuándo | ESC-19 |
| C-20 | App del alumno | Credencial ya guardada y teléfono en modo avión | Muestra el QR y el escáner lo valida como `valida`; el QR no contiene nombre, CURP ni foto | ESC-38 |
| C-21 | Escáner | Alumno sin QR que pasa con la revisión de siempre | Hecho de tipo `manual` con decisión `entra`; no se exige credencial | ESC-39 |
| C-22 | Servidor | Punto de acceso sin latido por más del intervalo configurado y sin entradas | El tablero lo marca «sin señal», distinto de «nadie ha entrado» | ESC-40 |
| C-23 | Escáner | Registro de un visitante con nombre y motivo | Hecho de tipo `visitante` con nombre y motivo, sin `sub` | ESC-42 |
| C-24 | Servidor | Emitir la credencial de un alumno del padrón | JWS verificable con la llave publicada; sin nombre, CURP ni foto; `exp` al fin del semestre. Un alumno fuera del padrón da error | ESC-45 |
| C-25 | Servidor | Lote de hechos de un teléfono dado de baja | 403 con Problem Details; no se guarda ningún hecho del lote | ESC-47 |

### Vectores de prueba

Las pruebas del servidor (C-11 en adelante) se ejecutan por la API contra cualquier implementación. Las del escáner (C-01 a C-10) viven dentro de la app, así que la especificación publica **vectores de prueba**: un archivo con casos fijos y el resultado esperado de cada uno. Cada implementación pasa los casos por su propio verificador y compara.

**Reglas:**

- Los vectores se publican con cada versión de la especificación, en el mismo release que las pruebas (`vectores/acceso-v0.1.json`).
- Usan **llaves de prueba** publicadas con su llave privada, marcadas con un `kid` que empieza por `prueba-`. Una implementación DEBE rechazar llaves `prueba-` fuera del modo de pruebas.
- Cada caso fija el instante de evaluación (`ahora`), para que el resultado no dependa del reloj de quien lo corre.
- Cada caso cita la prueba de conformidad que cubre, y por medio de ella su historia.

**Forma de un caso:**

```json
{
  "id": "V-05",
  "prueba": "C-05",
  "descripcion": "exp vencido hace 1 hora",
  "ahora": "2026-08-20T13:00:00Z",
  "plantel": "plantel-sintetico-01",
  "credencial": "eyJhbGciOiJFZERTQSIsImtpZCI6InBydWViYS0xIn0...",
  "llaves": "jwks-prueba-1",
  "revocadas": [],
  "esperado": "vencida"
}
```

**Cobertura mínima en v0.1:** un caso por cada resultado posible de la validación (`valida`, `no_legible`, `firma_invalida`, `otro_plantel`, `vencida`, `revocada`), más el caso en el límite de la tolerancia (C-06), el `sub` fuera del padrón local (C-10) y los nombres en dos formas de Unicode (C-18). Los vectores de esta versión todavía no están generados; se producen junto con el servidor de referencia en el sprint 1.

## Criterio de adopción

Define qué debe cumplir una escuela para declarar un nivel de adopción de este subsistema. Cada nivel es un conjunto de historias **cerrado bajo «depende de»** más las pruebas que lo verifican, así que cualquier nivel se puede construir sin piezas faltantes. Los niveles siguen la escala de madurez 0 a 4 del [diseño del MVP](https://claude.ai/artifact/8z2qFXRnnrty1u4cJAGH4R) y alimentan el eje de acceso del radar.

| Subsistema | Nivel | Nombre | Historias requeridas | Pruebas que debe pasar |
| --- | --- | --- | --- | --- |
| Ambos | 0 | Ninguno | — | — |
| Ambos | 1 | Papel | Fuera de esta especificación: la escuela lleva registros en papel y lo declara | — |
| Identidad y acceso a la plataforma | 2 | Captura digital (**mínimo para declararse adoptado**) | ESC-44, 63, 45, 46, 38 y 19 en su versión mínima | C-01 a C-07, C-18, C-19, C-20, C-24 |
| Identidad y acceso a la plataforma | 3 | Integrado | Por definir; candidatas UNI-14 (inicio de sesión único) y ESC-21 (tutores sin contraseña) | — |
| Acceso al plantel | 2 | Captura digital (**mínimo para declararse adoptado**) | Requiere Identidad en nivel 2, más ESC-43, 47, 29 y 39 | C-08 a C-11, C-13 a C-16, C-21, C-25 |
| Acceso al plantel | 3 | Integrado | Todo el nivel 2 más ESC-40, 41, 42 y 48. ESC-41 usa la interfaz de horarios de control escolar | Las anteriores más C-12, C-17, C-22, C-23 |
| Ambos | 4 | Automatizado | Por definir (alertas, credencial RFID, verificación por terceros) | — |

Las pruebas C-01 a C-07 son de Identidad porque verifican la credencial: cualquier verificador debe pasarlas, sea el escáner de la puerta o un tercero como una universidad. Acceso al plantel las hereda porque requiere Identidad en nivel 2.

**Por qué el nivel 2 incluye ESC-46 y ESC-19:** sin revocación, una credencial perdida sigue siendo válida; y en cuanto existe un registro de entradas, debe protegerse por rol. Son el piso de seguridad y privacidad, no extras.

**El nivel no basta: también se mide cobertura.** Una escuela en nivel 2 con una sola puerta y pocos alumnos con credencial no es lo mismo que una con todas. La cobertura se calcula con los hechos, no se declara:

- Puntos de acceso habilitados entre los puntos de acceso del plantel.
- Alumnos del padrón con credencial emitida y vigente.
- Entradas registradas por QR entre todas las entradas registradas (QR y manuales).

La demo con la institución sintética llega al nivel 3 con la puerta peatonal como único punto habilitado.

## Fuera de v0.1 y preguntas abiertas

**Fuera de v0.1:** QR rotativo firmado por el teléfono, credencial impresa y tarjeta NFC, verificación por terceros, avisos a familias, salidas del plantel y varios planteles bajo una misma administración. Cada uno entra en una versión posterior con su sección y sus pruebas.

**Preguntas abiertas**

- [ ] ¿Qué columnas trae el padrón que exporta un plantel real? Hoy el CSV es un supuesto.
- [ ] ¿Cada cuánto debe bajar el dispositivo la lista de revocadas cuando hay red?
- [ ] ¿Cuánto tiempo se guardan los hechos? Lo decide la dirección (carpeta de confianza).
- [ ] ¿Se registran salidas en una versión futura, o solo entradas?
- [ ] ¿Dónde se publica la especificación y con qué licencia (por ejemplo, CC BY 4.0)?

# Índice de especificaciones

> Migrado el 2026-11-13 desde [Índice de especificaciones: sistema escolar](https://claude.ai/artifact/Hoy2yaSyLpSmd3doTDQnNz) (fecha del original: 2026-11-12). Texto copiado sin cambios; la fuente de verdad desde ahora es este archivo.

## En este repositorio

| ID | Archivo | Versión |
|---|---|---|
| ESP-IDP | [ESP-IDP.md](ESP-IDP.md) (el texto v0.1 vive por ahora en ESP-PLA.md) | 0.2 |
| ESP-PLA | [ESP-PLA.md](ESP-PLA.md) | 0.2 |
| ESP-CON | [ESP-CON.md](ESP-CON.md) | 0.3 |

Lo que se encontró y todavía no se resuelve está en [Pendientes conocidos](pendientes.md).

Los enlaces de las tablas de abajo apuntan todavía a las fuentes originales.

## Propósito

Este índice dice qué especificaciones existen, en qué versión están y qué historias cubren. Es la puerta de entrada para una escuela o un desarrollador que quiere saber qué está acordado.

Cómo se relaciona con los demás documentos:

- El [catálogo de historias](https://claude.ai/artifact/VpPd8871SMYP2wGqVQisJE) dice **qué** debe hacer el sistema.
- Cada **especificación** dice cómo debe comportarse un subsistema y cómo se verifica.
- Este **índice** solo apunta a ellas: no repite su contenido (principio 14).

Reglas básicas:

- Hay una especificación por subsistema, más una de convenciones comunes que todas citan.
- Ninguna especificación nace sin un paquete de historias seleccionado para construirse.
- Un subsistema depende de la interfaz publicada de otro en una versión concreta, no de cómo está hecho por dentro.

**Toda especificación incluye una sección «Criterio de adopción».** Ahí define, para los niveles 0 a 4, qué historias y qué pruebas de conformidad debe cumplir una escuela para declarar cada nivel, y cómo se mide la cobertura con los hechos. Cada nivel debe estar cerrado bajo «depende de». El nivel 2 es el mínimo para declararse adoptado. Ejemplo: la [especificación de acceso](https://claude.ai/artifact/7T3STEZ5im4PVvaH1LJSBQ).

## Especificaciones

| ID | Especificación | Subsistema | Versión | Estado | Editor | Historias que cubre | Pruebas |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ESP-IDP | [Identidad y acceso a la plataforma](https://claude.ai/artifact/7T3STEZ5im4PVvaH1LJSBQ) | Identidad y acceso a la plataforma (la base) | 0.1 | Borrador | Samuel Gómez | ESC-19, 38, 44, 45, 46 | C-01 a C-07, C-18, C-19, C-20, C-24 |
| ESP-PLA | [Acceso al plantel](https://claude.ai/artifact/7T3STEZ5im4PVvaH1LJSBQ) | Acceso al plantel | 0.1 | Borrador | Samuel Gómez | ESC-29, 39 a 43, 47, 48 | C-08 a C-17, C-21 a C-23, C-25 |
| ESP-CON | [Constancias y verificación](https://claude.ai/artifact/HadS5sL44Nwt2atfCpnbQv) | Constancias y verificación | 0.2 | Borrador | Samuel Gómez | ESC-05, 07, 08, 19, 44, 61, 62, 63 | C-26 a C-50 |
| ESP-COM | Convenciones comunes | Todos | — | Por separar | Samuel Gómez | — | — |

ESP-IDP y ESP-PLA viven por ahora en un mismo documento, «Especificación v0.1», y se separan al pasar al repositorio. Antes se llamaban juntas ESP-ACC. ESP-CON tiene documento propio.

**Criterio de adopción de ESP-CON:** nivel 2 = ESC-44, 19, 63, 61, 08, 05; nivel 3 = nivel 2 + ESC-07, 62. ESC-44, 19, 61 y 63 son de Identidad: ESP-CON las exige, no es su dueña. ESC-61 (identificación sin contraseña) y ESC-63 (llaves de firma) se especifican por ahora dentro de ESP-CON, con sus pruebas C-26 a C-30, C-48 a C-50, C-52 y C-57, y pasan a ESP-IDP en su versión 0.3.

**ESP-COM** todavía no es un documento aparte. Sus reglas (identidad y roles, IDs UUIDv7, horas en UTC, texto en NFC, errores Problem Details, autenticación OIDC, idempotencia, versiones) viven hoy en la sección «Alcance y convenciones» del documento de la especificación v0.1. ESP-CON, la segunda especificación con documento propio, ya repite varias de ellas (UTC, NFC) en sus convenciones: el disparador se cumplió y toca separarlas.

Las versiones 0.x son borradores: pueden cambiar sin periodo de transición. La 1.0 es la primera que una escuela puede declarar como vigente.

## Interfaces entre subsistemas

Una interfaz es la promesa que un subsistema publica: qué se le puede pedir y con qué formato responde. Quien la usa depende de esa promesa en una versión concreta, no de cómo está construido el otro lado.

| Interfaz | La publica | La usa | Versión usada | Hoy se cumple con |
| --- | --- | --- | --- | --- |
| Credencial, llaves (JWKS) y lista de revocadas | ESP-IDP | ESP-PLA hoy; verificadores externos después | 0.1 | Servidor de referencia |
| Roles e inicio de sesión | ESP-IDP | Todos los subsistemas | 0.1 | Servidor de referencia |
| Horario por grupo (primera clase por día) | Control escolar (sin especificación aún) | ESP-PLA, para ESC-41 | Formato definido provisionalmente en ESP-PLA 0.1 | Archivo de horarios de la institución sintética |
| Padrón de alumnos | Control escolar (sin especificación aún) | ESP-IDP, para ESC-44 | Formato de importación de ESP-IDP 0.1 | Archivo que la escuela ya tiene, con un adaptador |
| Llaves de firma de constancias (kid constancia-\*) | ESP-IDP (ESC-63) | ESP-CON y quien verifique una constancia | Definida provisionalmente en ESP-CON 0.2 | Por implementar |
| Identificación sin contraseña (código de un solo uso) | ESP-IDP (ESC-61) | ESP-CON, para la solicitud en autoservicio | Definida provisionalmente en ESP-CON 0.2 | Por implementar |

**Regla para los formatos provisionales:** cuando Control escolar tenga su propia especificación, los formatos de horario y padrón pasan a ella, y ESP-IDP y ESP-PLA solo los citan con su versión. Hasta entonces, el dueño provisional del padrón es ESP-IDP y el de los horarios es ESP-PLA.

La verificación por terceros («alumno vigente», ESC-07 y UNI-10) es de Constancias y verificación: ESP-CON 0.2 cubre ESC-07 y usa la interfaz de llaves. Los verificadores nunca ven el registro de entradas.

## Ciclo de vida

| Estado | Significa | Quién puede declararse conforme |
| --- | --- | --- |
| Borrador (0.x) | Se está construyendo con la primera escuela; puede cambiar sin aviso | Nadie todavía, solo la implementación de referencia |
| Vigente (1.0 en adelante) | Acordada; los cambios siguen las reglas de versión | Cualquier implementación que pase sus pruebas |
| Obsoleta | Reemplazada por una versión mayor nueva; se mantiene durante la transición | Quien aún no migra, hasta la fecha de retiro |

**Reglas de versión** (versionado semántico, como ya dice la especificación v0.1):

- **Parche (1.0.1):** aclara texto o corrige un ejemplo. No cambia comportamiento.
- **Menor (1.1):** agrega algo opcional. Una implementación de la 1.0 sigue funcionando.
- **Mayor (2.0):** rompe compatibilidad. La versión anterior pasa a obsoleta y se mantiene durante un periodo de transición acordado, por ejemplo un semestre, para que cada escuela migre a su ritmo.

Cada escuela declara con qué versión de cada especificación cumple. Ese dato alimenta el radar de adopción.

## Propuestas de cambio

Un cambio a una especificación vigente entra por una **propuesta de cambio (PCE)**, al estilo de los RFC de internet o los PEP de Python. Mientras una especificación es borrador, los cambios se anotan directo y se registran como ADR en el documento de diseño.

**Pasos:**

1. Cualquier escuela o desarrollador abre una PCE con ID, la especificación que toca, la historia que la justifica y el cambio propuesto.
2. Se discute en público. Con una sola escuela decide el editor; con varias, el comité (una persona por escuela).
3. Queda aceptada o rechazada, con la razón escrita.
4. Si se acepta, entra en la siguiente versión, junto con sus pruebas de conformidad.

Una PCE sin historia en el catálogo no se discute: primero se propone la historia.

**Registro**

| ID | Especificación | Historia | Cambio | Estado |
| --- | --- | --- | --- | --- |
| — | — | — | Ninguna todavía: ESP-IDP, ESP-PLA y ESP-CON siguen en borrador | — |

## Próximas especificaciones

Candidatas, en el orden en que probablemente se necesiten. Ninguna se escribe hasta que haya un paquete de historias seleccionado.

| Candidata | Por qué | Disparador |
| --- | --- | --- |
| ESP-COM, convenciones comunes | Evita repetir reglas en cada especificación | Ya se cumplió con ESP-CON (12 de noviembre de 2026) |
| ESP-CES, control escolar | Sería la dueña de los formatos de horario y padrón que hoy definen ESP-IDP y ESP-PLA | Migrar Control escolar e inscripción al catálogo y que una escuela elija un paquete |
| ESP-ADM, admisión | ESC-35 y 36 ya usan el escaneo de acceso el día del examen | Una escuela que quiera digitalizar su examen de admisión |

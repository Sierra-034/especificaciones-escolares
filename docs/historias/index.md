# Historias de usuario

Esta carpeta es la **fuente única** de las historias de usuario del sistema escolar (principio 14): una historia por archivo, con su ID como nombre (`ESC-05.md`). Las especificaciones citan en cada prueba la historia que verifica, y el documento de diseño del MVP cita solo IDs. Una historia nueva se agrega copiando `_plantilla.md` de esta carpeta, y todo cambio entra por PCE. `python herramientas/verificar_catalogo.py` revisa que cada `id` coincida con su archivo, que cada «depende de» exista y que no haya ciclos.

Migrado el 2026-11-13 desde el [Catálogo de historias de usuario](https://claude.ai/artifact/VpPd8871SMYP2wGqVQisJE), que deja de ser la fuente. El catálogo exploratorio [Sistema educativo](https://claude.ai/artifact/KSZ7BP3o9FMvjVi9VHave3) queda como referencia de origen de los subsistemas que faltan por migrar.

## Reglas

Cada historia es un bloque de funcionalidad, y el catálogo se lee como conjuntos y relaciones:

| Concepto | Estructura | Regla |
| --- | --- | --- |
| Catálogo | Conjunto H de historias | Cada historia tiene un ID estable que nunca se reutiliza. |
| Subsistemas | Partición de H | Cada historia tiene exactamente un subsistema dueño (principio 8). |
| MVP y paquetes | Subconjuntos de H | Un paquete es una selección de historias, no un producto aparte. |
| Depende de | Orden parcial en H | No puede tener ciclos. Su orden topológico es el orden de construcción. |
| Usa | Relación entre subsistemas | Una historia usa algo que pertenece a otro subsistema, sin volverse suya. |
| Trazabilidad | Relación historia ↔ prueba | Una historia aprobada sin prueba es una historia que nadie verifica. |
| Etiquetas | Cubierta de H | Vistas libres como «día del examen». Una historia puede tener varias. |

Los pilares transversales (accesibilidad, privacidad, conectividad) no son dueños de historias. Aparecen como criterios de aceptación dentro de cada una.

## Formato de una historia

Cada historia lleva estos campos. Los que forman relaciones apuntan a otros IDs y nunca copian su texto.

| Campo | Qué contiene | Ejemplo |
| --- | --- | --- |
| ID | Prefijo y número estable | ESC-41 |
| Historia | Como \[rol\], quiero \[acción\], para \[beneficio\] | Como dirección, quiero una lista diaria de retardos por grupo, para hablar a tiempo con el alumno o su familia |
| Criterios | Condiciones verificables | Se calcula con la hora del escaneo contra la primera clase del grupo ese día |
| Subsistema | Exactamente uno, el dueño | Identidad y acceso |
| Estado | propuesta, aprobada o implementada | propuesta |
| Depende de | IDs que deben existir antes (orden parcial) | ESC-29 |
| Usa | Algo de otro subsistema que se consume sin ser dueño | Horarios de grupo (control escolar) |
| Pruebas | IDs de pruebas de conformidad | C-12 |
| Origen | De dónde salió | Nueva, diseño del MVP |
| Etiquetas | Vistas libres, opcional | MVP, día del examen |

**Reglas del campo «depende de»:**

- Solo apunta a historias del catálogo. Si la dependencia es de otro subsistema todavía no migrado, va en «usa» hasta que tenga ID.
- Se anota la dependencia directa, no las heredadas. Si ESC-29 depende de ESC-45 y ESC-45 de ESC-44, ESC-29 no repite ESC-44.
- Una historia del MVP solo puede depender de historias del MVP. Si no, el MVP no se puede construir completo.
- Antes de aprobar una historia se revisa que no forme un ciclo.

En los archivos, los campos que lee la herramienta van en el encabezado YAML (`id`, `titulo`, `subsistema`, `estado`, `depende_de`). Los demás van en el cuerpo. El estado puede ser `propuesta`, `aprobada`, `implementada` o `retirada`; un ID retirado no se reutiliza.

## Subsistemas

Los 11 subsistemas salen de agrupar las 80 historias de Sistema educativo. La migración va de uno en uno, empezando por la base.

| # | Subsistema | Historias de origen | Migración |
| --- | --- | --- | --- |
| 1 | Identidad y acceso a la plataforma (la base) | ESC-19, 21, 38, 44 a 46, 61, 63; UNI-14 | **Migrado (9 historias)** |
| 2 | Acceso al plantel | ESC-29, 39 a 43, 47, 48 | **Migrado (8 historias)** |
| 3 | Admisión | ESC-01, 22 a 28, 30 a 32, 35 a 37 | Pendiente |
| 4 | Control escolar e inscripción | ESC-02 a 04, 20, 24; UNI-01, 17, 18 | Pendiente |
| 5 | Constancias y verificación | ESC-05 a 08, 54, 62; UNI-05, 09, 10; DOC-15 | **Migrado (9 historias; UNI-09 fusionada en ESC-05)** |
| 6 | Trayectoria académica | ESC-09 a 11; UNI-02, 12, 21, 22, 25 a 27 | Pendiente |
| 7 | Comunicación con familias | ESC-12 a 14 | Pendiente |
| 8 | Pagos y becas | ESC-15, 16, 26 | Pendiente |
| 9 | Trámites largos y titulación | UNI-03, 04, 06 a 08 | Pendiente |
| 10 | Personal docente | DOC-01 a 16; ESC-17; UNI-11, 13 | Pendiente |
| 11 | Gobierno institucional | ESC-18, 59; UNI-16, 20, 23, 24 | Pendiente |
| 12 | Integraciones | UNI-15 | Pendiente |
| 13 | Vinculación (servicio social, prácticas, bolsa de trabajo) | Ninguna todavía | **Propuesto** |
| 14 | Comunicación entre escuelas | ESC-49 a 53, 55 a 58, 60 | **Propuesto, con historias** |
| 15 | Emergencias y evacuación | Ninguna todavía; usaría los hechos de entrada | **Propuesto** |
| 16 | Bienestar y permanencia | Ninguna todavía; usaría los retardos como señal | **Propuesto** |
| 17 | Estadística para la autoridad (formato 911) | Ninguna todavía | **Propuesto** |
| 18 | Espacios y equipo | Ninguna todavía | **Propuesto** |
| 19 | Salud escolar básica | Ninguna todavía | **Propuesto** |

**Ajustes al aplicar la partición:** ESC-35 (registro en campus el día del examen) y ESC-36 (tablero del examen) estaban agrupadas con acceso, pero su dueño es Admisión, porque existen por el examen. Pasaron a Admisión con la relación «usa ESC-29». Después, la trazabilidad agregó ESC-48. Por último, el antiguo «Identidad y acceso» se separó en dos: **Identidad y acceso a la plataforma**, la base que usan todos los subsistemas, y **Acceso al plantel**, que es opcional. Una escuela puede adoptar el primero sin el segundo, pero no al revés.

## MVP de constancias: plan de construcción

Es el MVP elegido (2026-11-12). Su especificación es [ESP-CON](../especificaciones/ESP-CON.md).

| Adopción | Construcción | ID | Historia corta | Subsistema | Depende de |
| --- | --- | --- | --- | --- | --- |
| 2 | 0 | [ESC-44](ESC-44.md) | Importar el padrón | Plataforma | — |
| 2 | 0 | [ESC-19](ESC-19.md) | Acceso por rol (mínima) | Plataforma | — |
| 2 | 0 | [ESC-63](ESC-63.md) | Llaves de firma de la escuela | Plataforma | — |
| 2 | 1 | [ESC-61](ESC-61.md) | Identificarse con un código | Plataforma | [ESC-44](ESC-44.md) |
| 2 | 1 | [ESC-08](ESC-08.md) | Plantillas oficiales con vigencia | Constancias | [ESC-19](ESC-19.md) |
| 2 | 2 | [ESC-05](ESC-05.md) | Constancia de estudios en autoservicio | Constancias | [ESC-08](ESC-08.md), [ESC-61](ESC-61.md), [ESC-63](ESC-63.md) |
| 3 | 3 | [ESC-07](ESC-07.md) | Verificar una constancia por QR | Constancias | [ESC-05](ESC-05.md) |
| 3 | 4 | [ESC-62](ESC-62.md) | Anular una constancia | Constancias | [ESC-07](ESC-07.md) |

## MVP de puerta: plan de construcción

Va después del de constancias. Su especificación es [ESP-PLA](../especificaciones/ESP-PLA.md).

Las 14 historias del MVP de puerta pertenecen a dos subsistemas: **Identidad y acceso a la plataforma** y **Acceso al plantel**. Todas están en estado propuesta y todas tienen al menos una prueba de conformidad. Las fichas completas están en la sección de cada subsistema, más abajo.

La tabla se lee de arriba abajo como un plan. La columna **Adopción** dice qué nivel del criterio de adopción completa cada historia. La columna **Construcción** dice en qué nivel del diagrama de la sección Relaciones está: 0 no depende de nada, 1 depende solo de historias de nivel 0, y así sucesivamente. Las historias con el mismo número de construcción se pueden hacer en cualquier orden o al mismo tiempo.

| Adopción | Construcción | ID | Historia corta | Subsistema | Depende de | Pruebas |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 0 | [ESC-44](ESC-44.md) | Importar el padrón | Plataforma | — | C-18 |
| 2 | 0 | [ESC-43](ESC-43.md) | Habilitar o deshabilitar un punto de acceso | Plantel | — | C-15, C-16 |
| 2 | 0 | [ESC-19](ESC-19.md) | Acceso por rol a información sensible (mínima) | Plataforma | — | C-19 |
| 2 | 0 | [ESC-63](ESC-63.md) | Llaves de firma de la escuela | Plataforma | — | C-03 |
| 2 | 1 | [ESC-45](ESC-45.md) | Emitir la credencial | Plataforma | [ESC-44](ESC-44.md), [ESC-63](ESC-63.md) | C-24 |
| 2 | 1 | [ESC-47](ESC-47.md) | Registrar o dar de baja un teléfono de puerta | Plantel | [ESC-43](ESC-43.md) | C-25 |
| 2 | 2 | [ESC-38](ESC-38.md) | Mostrar mi credencial en el teléfono | Plataforma | [ESC-45](ESC-45.md) | C-20 |
| 2 | 2 | [ESC-46](ESC-46.md) | Revocar una credencial | Plataforma | [ESC-45](ESC-45.md) | C-07 |
| 2 | 2 | [ESC-29](ESC-29.md) | Validar la credencial con el teléfono | Plantel | [ESC-45](ESC-45.md), [ESC-47](ESC-47.md) | C-01 a C-11, C-13, C-14 |
| 2 | 2 | [ESC-39](ESC-39.md) | Entrada manual sin QR | Plantel | [ESC-47](ESC-47.md) | C-21 |
| 3 | 2 | [ESC-42](ESC-42.md) | Registrar a un visitante | Plantel | [ESC-47](ESC-47.md) | C-23 |
| 3 | 3 | [ESC-40](ESC-40.md) | Tablero de entradas del día | Plantel | [ESC-29](ESC-29.md), [ESC-39](ESC-39.md), [ESC-19](ESC-19.md) | C-22 |
| 3 | 3 | [ESC-41](ESC-41.md) | Retardos diarios por grupo | Plantel | [ESC-29](ESC-29.md) | C-12 |
| 3 | 3 | [ESC-48](ESC-48.md) | Exportar todos los registros | Plantel | [ESC-29](ESC-29.md), [ESC-19](ESC-19.md) | C-17 |
| Sin nivel | — | [ESC-21](ESC-21.md) | Acceso del tutor sin contraseña | Plataforma | — | — |
| Sin nivel | — | [UNI-14](UNI-14.md) | Inicio de sesión único | Plataforma | — | — |

El nivel 2 de cada subsistema es el mínimo para declararlo adoptado; el MVP de la demo cubre los niveles 2 y 3 de ambos. «Sin nivel» son historias que todavía no entran en ningún criterio de adopción. Los IDs no cambian aunque cambie el orden o el subsistema: el orden es una vista, el ID es la identidad.

## Dos MVP posibles

|  | MVP de puerta | MVP de constancias |
| --- | --- | --- |
| Historias | 14 | 8 |
| Base compartida | ESC-44, ESC-19, ESC-63 | ESC-44, ESC-19, ESC-63 |
| Además de la base | Credencial (ESC-45, 46, 38) y las 8 de Acceso al plantel | Inicio de sesión (ESC-61) y 4 de Constancias |
| Equipo | Un teléfono en cada puerta | Ninguno; el alumno usa su teléfono o una computadora |
| Carga | Hora pico de entrada, a veces sin red | Baja y repartida en el día |
| Quién ve el beneficio primero | Dirección y familias | Control escolar y alumnos |
| Riesgo principal | La operación diaria en la puerta | Bajo: la constancia sigue firmada a mano, y quitar esa firma es horizonte |
| Especificación | ESP-IDP y ESP-PLA, v0.1 escrita | ESP-IDP y ESP-CON, por escribir |

Lo que se construya primero no se tira, porque la base es la misma. Si se empieza por constancias, después el MVP de puerta solo agrega 11 historias (ESC-45, 46, 38 y las 8 de Acceso al plantel). Si se empieza por la puerta, después el de constancias agrega 5 (ESC-61 y las 4 de Constancias).

## Identidad y acceso a la plataforma

Es la base: quién es cada persona, cómo lo demuestra y qué puede hacer dentro del sistema. Todos los demás subsistemas la usan. Incluye la credencial, porque no sirve solo para la puerta: es la misma que podría verificar un tercero, como ADO o una universidad. Tiene 9 historias: 6 en el MVP de puerta y 4 en el de constancias (ESC-44, 19, 63 están en ambos).

| ID | Historia corta | Depende de | Pruebas |
| --- | --- | --- | --- |
| [ESC-19](ESC-19.md) | Acceso por rol a información sensible | — | C-19 |
| [ESC-21](ESC-21.md) | Acceso del tutor sin contraseña | [ESC-61](ESC-61.md) | — |
| [ESC-38](ESC-38.md) | Mostrar mi credencial en el teléfono | [ESC-45](ESC-45.md) | C-20 |
| [ESC-44](ESC-44.md) | Importar el padrón | — | C-18 |
| [ESC-45](ESC-45.md) | Emitir la credencial | [ESC-44](ESC-44.md), [ESC-63](ESC-63.md) | C-24 |
| [ESC-46](ESC-46.md) | Revocar una credencial | [ESC-45](ESC-45.md) | C-07 |
| [UNI-14](UNI-14.md) | Inicio de sesión único | [ESC-61](ESC-61.md) | — |
| [ESC-61](ESC-61.md) | Identificarse con un código, sin contraseña | [ESC-44](ESC-44.md) | C-26 a C-30, C-48 a C-50 |
| [ESC-63](ESC-63.md) | Llaves de firma de la escuela | — | C-03, C-47 |

## Acceso al plantel

Registra quién entra al plantel, por dónde y a qué hora. Es opcional: una escuela puede usar el resto del sistema sin él. Usa la credencial y los roles de Identidad y acceso a la plataforma. Tiene 8 historias, todas en el MVP.

| ID | Historia corta | Depende de | Pruebas |
| --- | --- | --- | --- |
| [ESC-29](ESC-29.md) | Validar la credencial con el teléfono | [ESC-45](ESC-45.md), [ESC-47](ESC-47.md) | C-01 a C-11, C-13, C-14 |
| [ESC-39](ESC-39.md) | Entrada manual sin QR | [ESC-47](ESC-47.md) | C-21 |
| [ESC-40](ESC-40.md) | Tablero de entradas del día | [ESC-29](ESC-29.md), [ESC-39](ESC-39.md), [ESC-19](ESC-19.md) | C-22 |
| [ESC-41](ESC-41.md) | Retardos diarios por grupo | [ESC-29](ESC-29.md) | C-12 |
| [ESC-42](ESC-42.md) | Registrar a un visitante | [ESC-47](ESC-47.md) | C-23 |
| [ESC-43](ESC-43.md) | Habilitar o deshabilitar un punto de acceso | — | C-15, C-16 |
| [ESC-47](ESC-47.md) | Registrar o dar de baja un teléfono de puerta | [ESC-43](ESC-43.md) | C-25 |
| [ESC-48](ESC-48.md) | Exportar todos los registros | [ESC-29](ESC-29.md), [ESC-19](ESC-19.md) | C-17 |

## Constancias y verificación

Emite documentos que la escuela firma y que cualquiera puede comprobar: constancias de estudios, laborales y de no adeudo. Usa el padrón, los roles, el inicio de sesión y las llaves de firma de Identidad y acceso a la plataforma. No necesita teléfonos en la puerta ni aguantar una hora pico. Tiene 9 historias, 4 de ellas en el MVP de constancias. UNI-09 (constancias en autoservicio para universidad) era la misma historia que ESC-05 y quedó fusionada en ella; su ID no se reutiliza.

**Adopción gradual.** En el nivel 2 la constancia sale del sistema con folio y QR, pero se sigue firmando a mano, así que nada cambia para quien la recibe. En el nivel 3 cualquiera la verifica con el QR y la escuela puede anularla. Desde ahí la firma electrónica puede reemplazar a la autógrafa, solo donde el receptor la acepte (supuesto por confirmar).

| ID | Historia corta | Depende de | Pruebas |
| --- | --- | --- | --- |
| [ESC-08](ESC-08.md) | Plantillas oficiales con vigencia | [ESC-19](ESC-19.md) | C-31 a C-33 |
| [ESC-05](ESC-05.md) | Constancia de estudios en autoservicio | [ESC-08](ESC-08.md), [ESC-61](ESC-61.md), [ESC-63](ESC-63.md) | C-34 a C-37, C-45 |
| [ESC-07](ESC-07.md) | Verificar una constancia por QR | [ESC-05](ESC-05.md) | C-38 a C-42, C-46, C-47 |
| [ESC-62](ESC-62.md) | Anular una constancia | [ESC-07](ESC-07.md) | C-43, C-44 |
| [ESC-06](ESC-06.md) | Bandeja de revisión para constancias especiales | [ESC-05](ESC-05.md) | — |
| [ESC-54](ESC-54.md) | Autenticidad de un documento de otra escuela | [ESC-07](ESC-07.md), [ESC-53](ESC-53.md) | — |
| [UNI-05](UNI-05.md) | Constancia de no adeudo automática | [ESC-05](ESC-05.md) | — |
| [UNI-10](UNI-10.md) | Verificación de certificados y grados | [ESC-07](ESC-07.md) | — |
| [DOC-15](DOC-15.md) | Constancias laborales en autoservicio | [ESC-05](ESC-05.md) | — |

## Comunicación entre escuelas (propuesto)

Subsistema propuesto el 2026-11-11, sin especificación todavía. **Es dueño del intercambio, no de los datos:** el expediente pertenece a Control escolar y la verificación de documentos a Constancias y verificación. Este subsistema solo se encarga de que viajen entre escuelas de forma segura. Como todos, se apoya en la versión mínima de Identidad y acceso a la plataforma.

**Criterios comunes a todas sus historias:** consentimiento explícito del alumno o tutor cuando hay datos personales, solo los datos necesarios, y registro de quién envió qué, a quién y cuándo.

Todas están en estado **propuesta**. Las historias ESC-49, 50, 51 y 53 juntas forman el traslado de expediente completo y son el primer paquete candidato.

| ID | Historia corta | Depende de | Pruebas |
| --- | --- | --- | --- |
| [ESC-53](ESC-53.md) | Registrar mi escuela en un directorio común con su llave pública | — | — |
| [ESC-49](ESC-49.md) | Solicitar el expediente de un alumno que viene de otra escuela | [ESC-53](ESC-53.md) | — |
| [ESC-50](ESC-50.md) | Autorizar o negar el envío de mi expediente a otra escuela | [ESC-49](ESC-49.md) | — |
| [ESC-51](ESC-51.md) | Atender una solicitud de expediente desde el sistema | [ESC-49](ESC-49.md), [ESC-50](ESC-50.md) | — |
| [ESC-52](ESC-52.md) | Enviar mi certificado a la universidad o la empresa que me lo pide | [ESC-53](ESC-53.md) | — |
| [ESC-55](ESC-55.md) | Consultar una tabla compartida de equivalencias entre planes de estudio | — | — |
| [ESC-56](ESC-56.md) | Cursar una actividad o materia en otra escuela de la red y que el resultado regrese a mi expediente | [ESC-53](ESC-53.md) | — |
| [ESC-57](ESC-57.md) | Compartir materiales con docentes de otras escuelas | — | — |
| [ESC-58](ESC-58.md) | Ver indicadores agregados de varias escuelas sin datos personales | [ESC-53](ESC-53.md) | — |
| [ESC-60](ESC-60.md) | Anunciar eventos y concursos interescolares | [ESC-53](ESC-53.md) | — |

## Gobierno institucional (por migrar)

| ID | Historia corta | Depende de | Pruebas |
| --- | --- | --- | --- |
| [ESC-59](ESC-59.md) | Publicar y votar propuestas de cambio a las especificaciones | — | — |

ESC-59 nació en Comunicación entre escuelas, pero su dueño es Gobierno institucional.

## Orden de construcción del MVP de puerta

**Orden topológico de construcción del MVP.** Dentro de un nivel el orden es libre; un nivel empieza cuando el anterior está listo.

| Nivel | Historias | Qué se tiene al terminar |
| --- | --- | --- |
| 0 | ESC-44, ESC-63, ESC-43, ESC-19 | Padrón cargado, llaves de firma, puntos de acceso y roles |
| 1 | ESC-45, ESC-47 | Credenciales emitidas y teléfonos de puerta autorizados |
| 2 | ESC-38, ESC-46, ESC-29, ESC-39, ESC-42 | Entradas registradas en la puerta: QR, manual y visitantes |
| 3 | ESC-40, ESC-41, ESC-48 | Tablero del día, retardos y exportación |

ESC-41 tiene una dependencia fuera del subsistema: los horarios de grupo. Para el MVP vienen del archivo de horarios de la institución sintética, y tendrán ID propio cuando se migre Control escolar e inscripción. ESC-21 y UNI-14 no aparecen porque están fuera del MVP y no dependen de nada del MVP.

## Trazabilidad

Cada historia lista sus pruebas de conformidad en su propio archivo, y cada prueba de una especificación cita su historia. Las tablas por subsistema de esta página resumen esa relación.

## Pendientes de migración

- [ ] Aprobar las 14 historias del MVP de puerta (pasar de propuesta a aprobada).
- [ ] Confirmar el rol de origen de UNI-14 en Sistema educativo.
- [ ] En el documento de diseño del MVP, dejar solo la lista de IDs con enlace a este catálogo.
- [ ] En Sistema educativo, agregar una nota que apunte a este catálogo como fuente vigente.
- [ ] Migrar Admisión (incluye ESC-35 y 36), luego Control escolar e inscripción, que trae los horarios de grupo.
- [ ] Al migrar cada subsistema: agregar «para» y criterios, y revisar que no aparezcan ciclos en «depende de».
- [ ] Retirar del catálogo lo que no aplica a escuela pública, como ESC-15 (colegiaturas), marcándolo como descartado sin borrar su ID.
- [x] Elegir entre el MVP de puerta y el de constancias: se eligió constancias (2026-11-12).
- [ ] Horizonte, no bloquea el MVP: confirmar con receptores (becas, empresas, otras escuelas) si aceptan una constancia sin firma autógrafa, solo con firma electrónica y QR.
- [ ] Antes del piloto, no del desarrollo (la institución sintética ya los trae): revisar que el padrón real (ESC-44) traiga los datos de la constancia: semestre, grupo, turno, ciclo y un contacto (correo o teléfono).
- [ ] Si se elige constancias: escribir ESP-CON con sus pruebas de conformidad y agregar ESC-61 y ESC-63 a ESP-IDP.

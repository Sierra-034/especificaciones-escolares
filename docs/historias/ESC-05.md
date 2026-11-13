---
id: ESC-05
titulo: Constancia de estudios en autoservicio
subsistema: constancias
estado: propuesta
depende_de: [ESC-08, ESC-61, ESC-63]
---

# ESC-05 · Constancia de estudios en autoservicio

Como **alumno o tutor**, quiero **descargar la constancia de estudios cuando la necesito**, para **no hacer fila ni esperar días en control escolar**.

## Criterios de aceptación

- Sale en menos de un minuto, con folio único, QR y firma de la escuela.
- Solo se emite si el alumno está inscrito en el padrón vigente.
- Los datos (nombre, CURP, matrícula, semestre, grupo, turno y ciclo) vienen del padrón y nunca se capturan.
- Cada emisión queda anotada con quién, cuándo y qué versión de plantilla.
- Funciona en un teléfono con conexión lenta.
- En el MVP la pide el alumno; el tutor podrá pedirla cuando exista ESC-21.

## Pruebas de conformidad

- C-34 a C-37, C-45 (de ESP-CON v0.2; el catálogo de origen decía «por definir»)

## Relaciones

- **Subsistema dueño:** Constancias y verificación.
- **Depende de:** [ESC-08](ESC-08.md), [ESC-61](ESC-61.md), [ESC-63](ESC-63.md).
- **Usa:** inscripción vigente (Control escolar e inscripción); en el MVP sale del padrón importado.

## Origen

- Sistema educativo.
- **Etiquetas:** MVP de constancias.

*Migrado el 2026-11-13 desde el [Catálogo de historias de usuario](https://claude.ai/artifact/VpPd8871SMYP2wGqVQisJE).*

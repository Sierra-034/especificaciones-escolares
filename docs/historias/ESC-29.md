---
id: ESC-29
titulo: Validar la credencial con el teléfono
subsistema: acceso-plantel
estado: propuesta
depende_de: [ESC-45, ESC-47]
---

# ESC-29 · Validar la credencial con el teléfono

Como **personal de acceso**, quiero **validar la credencial del alumno con el teléfono de la puerta**, para **registrar su entrada sin hacer fila**.

## Criterios de aceptación

- Resultado en 3 s o menos.
- Funciona sin red, porque la firma se verifica en el teléfono.
- Un resultado no válido solo advierte y nunca bloquea la entrada.
- El hecho guarda la hora del escaneo (ocurrio\_en), no la de sincronización.

## Pruebas de conformidad

- C-01 a C-11, C-13, C-14

## Relaciones

- **Subsistema dueño:** Acceso al plantel.
- **Depende de:** [ESC-45](ESC-45.md), [ESC-47](ESC-47.md).
- **Usa:** —.

## Origen

- Sistema educativo (día del examen), extendida al acceso diario.
- **Etiquetas:** MVP, día del examen.

*Migrado el 2026-11-13 desde el [Catálogo de historias de usuario](https://claude.ai/artifact/VpPd8871SMYP2wGqVQisJE).*

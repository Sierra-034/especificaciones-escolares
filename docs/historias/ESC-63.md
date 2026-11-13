---
id: ESC-63
titulo: Llaves de firma de la escuela
subsistema: identidad
estado: propuesta
depende_de: []
---

# ESC-63 · Llaves de firma de la escuela

Como **responsable del sistema**, quiero **generar, guardar y rotar las llaves con que la escuela firma**, para **que credenciales, constancias y pases se puedan verificar y una llave robada se pueda retirar**.

## Criterios de aceptación

- La llave privada nunca sale del servidor.
- Cada llave tiene un identificador (kid) y un solo uso (credencial o constancia).
- Las llaves públicas se publican para verificar sin conexión.
- Rotar una llave no invalida lo firmado antes; retirarla sí, y queda anotado con quién y cuándo.

## Pruebas de conformidad

- C-03, C-47 (de ESP-CON v0.2; el catálogo de origen decía «C-03»)

## Relaciones

- **Subsistema dueño:** Identidad y acceso a la plataforma.
- **Depende de:** ninguna.
- **Usa:** —.

## Origen

- Nueva, al migrar Constancias y verificación (antes vivía dentro de ESC-45).
- **Etiquetas:** MVP de puerta, MVP de constancias.

*Migrado el 2026-11-13 desde el [Catálogo de historias de usuario](https://claude.ai/artifact/VpPd8871SMYP2wGqVQisJE).*

# Contratos

`openapi.yaml` es el contrato HTTP del estándar (OpenAPI 3.1). Se escribe **antes** que el código
(principio 12). La implementación de referencia no guarda copia: lo lee desde su submódulo `estandar/`,
fijado a una versión etiquetada, y se prueba contra él.

## Qué cubre

Las 12 operaciones de ESP-CON y `GET /v0/llaves` de ESP-IDP. Las rutas de la puerta (ESP-PLA) y la
importación del padrón (P-22) todavía no están.

## Cómo se lee

- `info.version` es la versión **del contrato**. Sube cada vez que cambia una ruta, un esquema o un error.
- Cada operación dice de dónde sale y qué cubre:

| Campo | Qué dice | Ejemplo |
|---|---|---|
| `x-especificacion` | Especificación dueña de la ruta y su versión | `ESP-CON@0.5` |
| `x-historias` | Historias que la ruta atiende | `[ESC-05, ESC-08]` |
| `x-pruebas` | Pruebas de conformidad que llaman a la ruta | `[C-33, C-34, C-37]` |
| `x-roles` | Roles del catálogo de ESP-IDP que la ruta acepta; sin este campo, cualquier sesión basta | `[control_escolar]` |

## Cómo se comprueba

```bash
openapi-spec-validator contratos/openapi.yaml
```

Viene en `requirements.txt` y el CI lo corre en cada PR.

Si el contrato y el texto de una especificación no coinciden, es un error del estándar: se reporta
en [Pendientes conocidos](../docs/especificaciones/pendientes.md) y se corrige con un PCE.

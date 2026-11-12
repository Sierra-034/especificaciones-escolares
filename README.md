# Especificaciones escolares

Estándar abierto para el software de escuelas públicas de nivel medio superior y superior.
Aquí viven **qué** debe hacer el sistema y **cómo se comprueba**: historias de usuario,
especificaciones por subsistema, decisiones de diseño (ADR), el contrato OpenAPI,
las pruebas de conformidad y los vectores de prueba.

El código que cumple este estándar vive aparte, en
[plataforma-escolar](https://github.com/Sierra-034/plataforma-escolar) (implementación de referencia).
Cualquier otra implementación que pase las pruebas de conformidad cumple igual.

## Qué hay en cada carpeta

| Carpeta | Contenido |
|---|---|
| `docs/historias/` | Una historia por archivo (`ESC-05.md`), Markdown con encabezado corto. Fuente única del catálogo. |
| `docs/especificaciones/` | Una especificación por subsistema, versionada por separado (`ESP-CON.md`). |
| `docs/adr/` | Decisiones de diseño del estándar. Nunca se editan: se reemplazan por otra ADR. |
| `docs/principios.md` | Principios de diseño que aplican a todo. |
| `contratos/` | Contrato OpenAPI. Se escribe antes que el código. |
| `conformidad/` | Pruebas de conformidad (pytest) que corren contra cualquier implementación. |
| `vectores/` | Entradas y salidas fijas (JWS de ejemplo, llaves de prueba públicas) que usan las pruebas. |
| `herramientas/` | Verificador del catálogo: IDs únicos, dependencias existentes, sin ciclos. |

Nada generado se sube: el sitio se construye en GitHub Actions.

## Estado

| Especificación | Subsistema | Versión | Estado |
|---|---|---|---|
| ESP-IDP | Identidad y acceso a la plataforma | 0.1 | borrador, base de todo |
| ESP-CON | Constancias | 0.2 | borrador, **MVP en curso** |
| ESP-PLA | Acceso al plantel | 0.1 | borrador, va después de constancias |

Criterio de adopción de ESP-CON:
- **Nivel 2** = ESC-44, ESC-19, ESC-63, ESC-61, ESC-08, ESC-05 (folio y QR, todavía con firma autógrafa).
- **Nivel 3** = nivel 2 + ESC-07, ESC-62 (constancia verificable y anulable).

## Cómo proponer un cambio (PCE)

Una propuesta de cambio al estándar (PCE) es un *pull request*. Su número es el número del PR.

1. Crea una rama: `git switch -c pce/descripcion-corta`.
2. Cambia la historia, la especificación o la prueba. Si es una decisión, agrega una ADR nueva.
3. Abre el PR; la plantilla te pide qué cambia, por qué, y qué versión sube.
4. Al aprobarse se fusiona en `main`. Una versión publicada es una etiqueta.

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para el detalle. Las mismas reglas, escritas para Claude Code, están en [CLAUDE.md](CLAUDE.md).

## Versiones

Cada especificación se versiona por separado con etiquetas `esp-<id>-vX.Y.Z`,
por ejemplo `esp-con-v0.2.0`. Mientras una especificación esté en `0.x`, puede cambiar con una ADR.
Desde `1.0`, un cambio incompatible sube la versión mayor y trae un periodo de transición.

## Ver el sitio en tu máquina

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python herramientas/verificar_catalogo.py
mkdocs serve        # abre http://127.0.0.1:8000
```

## Correr las pruebas de conformidad contra una implementación

```bash
cd conformidad
pip install -e .
pytest --base-url http://localhost:8000
```

## Licencia

Pendiente de su ADR. Propuesta: CC BY 4.0 para los textos y una licencia libre para el código.

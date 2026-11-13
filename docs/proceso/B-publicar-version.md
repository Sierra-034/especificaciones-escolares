# B · Publicar una versión

**Cuándo:** se juntaron uno o más PCE en `main` y quieres que otros (la implementación, una escuela)
puedan fijarse en ese estado.

**Requisitos previos:**
- [Antes de cada sesión](0-preparar-equipo.md#antes-de-cada-sesion) hecho.
- Todos los PCE que deben entrar ya están unidos en `main`.
- Sabes **qué especificación** cambió (su ID va en el nombre de la etiqueta).

## 1 · Saber qué contiene la versión

Una versión es una foto de `main`. Lo que entra es todo lo unido desde la versión anterior.

| Comando | Qué te dice |
|---|---|
| `git tag --sort=-creatordate` | Las versiones existentes, la más nueva arriba. La primera es la anterior. |
| `git log --oneline esp-con-v0.2.0..main` | Los PCE que entran (cambia `esp-con-v0.2.0` por la versión anterior). Cada línea termina en `(#N)`. |
| `git diff --stat esp-con-v0.2.0..main` | Qué archivos cambiaron y cuánto. |

Si en la lista aparece algo que no quieres publicar todavía, **no etiquetes**: primero revierte ese PCE con otro PCE.

## 2 · Elegir el número

Formato: `esp-<id>-vMAYOR.MENOR.CORRECCIÓN`, por ejemplo `esp-con-v0.3.0`.

Mientras la versión sea `0.x`:

| Qué cambió | Sube | Ejemplo |
|---|---|---|
| Algo que obliga a cambiar una implementación (contrato, comportamiento, prueba nueva) | MENOR | `0.2.0` → `0.3.0` |
| Redacción, erratas, aclaraciones que no cambian el comportamiento | CORRECCIÓN | `0.2.0` → `0.2.1` |

Desde `1.0.0`, un cambio incompatible sube MAYOR y trae periodo de transición.

La etiqueta lleva el ID de la especificación que cambió, pero la foto incluye todo el repo.

## 3 · Escribir el CHANGELOG (es un PCE)

| Paso | Comando | Qué hace |
|---|---|---|
| 1 | `git switch -c pce/publicar-esp-con-v0.3.0` | Rama para la publicación. |
| 2 | *(edita `CHANGELOG.md`)* | Agrega arriba `## esp-con-v0.3.0 — AAAA-MM-DD` y **una línea por cada PCE del paso 1**, con su `#N`. |
| 3 | Procedimiento [A](A-proponer-cambio.md), pasos 5 a 10 | Commit, PR, pruebas, unir, `git pull`. |

**Comprobación antes de seguir:** cada `(#N)` de `git log --oneline <anterior>..main` aparece en el CHANGELOG.

## 4 · Etiquetar y publicar

| Paso | Comando | Qué hace |
|---|---|---|
| 1 | `git switch main && git pull` | La etiqueta debe caer sobre el commit del CHANGELOG. |
| 2 | `git log --oneline -1` | Debe decir `Publicar esp-con-v0.3.0 (#N)`. Si no, detente. |
| 3 | `git tag -a esp-con-v0.3.0 -m "ESP-CON v0.3"` | Crea la etiqueta anotada (guarda autor, fecha y mensaje). |
| 4 | `git push origin esp-con-v0.3.0` | Sube la etiqueta. `git push` normal no sube etiquetas. |
| 5 | `gh release create esp-con-v0.3.0 --prerelease --generate-notes` | Crea la página del release con la lista de PR unidos. Quita `--prerelease` desde `1.0.0`. |

## Cómo saber que salió bien

`gh release view esp-con-v0.3.0` muestra el release; la página del repo lo lista en *Releases*.

## Si algo falla

- **Etiquetaste el commit equivocado y todavía no hiciste `git push` de la etiqueta:** `git tag -d esp-con-v0.3.0` y repite. Mientras no se suba, no es pública.
- **Ya la subiste:** no la muevas. Usa el procedimiento [D](D-corregir-version.md).

## Siguiente

[C · Fijar la versión en la implementación](C-fijar-version.md).

# C · Fijar la versión en la implementación

**Cuándo:** se publicó una versión del estándar y `plataforma-escolar` debe construirse contra ella.

**Requisitos previos:**
- La etiqueta existe en GitHub (`gh release view <etiqueta>` en el estándar).
- En `plataforma-escolar`: [Antes de cada sesión](0-preparar-equipo.md#antes-de-cada-sesion) hecho, incluido `git submodule update`.

## Pasos (en `plataforma-escolar`)

| Paso | Comando | Qué hace |
|---|---|---|
| 1 | `git switch -c fijar-esp-con-v0.3.0` | Rama para este cambio. |
| 2 | `scripts/fijar-estandar.sh esp-con-v0.3.0` | Entra a `estandar/`, baja las etiquetas, se coloca en esa versión y hace `git add estandar`. |
| 3 | `git submodule status` | Debe mostrar `estandar` seguido de `(esp-con-v0.3.0)`. |
| 4 | `git commit -m "Fijar estándar en esp-con-v0.3.0"` | Guarda el cambio: una sola línea, el commit al que apunta `estandar/`. |
| 5 | `git push -u origin fijar-esp-con-v0.3.0` | Sube la rama. |
| 6 | `gh pr create --fill` | Abre el PR. |
| 7 | `gh pr checks --watch` | Espera las pruebas. |
| 8 | `gh pr merge --squash --delete-branch` | **Solo en verde.** Une y regresa a `main`. |

## Cómo saber que salió bien

En `main`, `git submodule status` muestra la etiqueta nueva.

## Si algo falla

- **El script dice «Falta estandar/»:** `git submodule update --init` y repite el paso 2.
- **Las pruebas fallan después de fijar:** es esperado si la versión subió MENOR. El PR queda abierto y el trabajo
  para cumplir la versión nueva se hace en esa misma rama o en PR que se unen antes.

# A · Proponer un cambio (PCE)

**Cuándo:** quieres cambiar cualquier cosa del estándar: una historia, una especificación, una ADR,
una prueba, un vector, el contrato o este manual.

**Requisitos previos:**
- [Antes de cada sesión](0-preparar-equipo.md#antes-de-cada-sesion) hecho: estás en `main`, al día y sin cambios.
- Sabes en una frase qué cambia y por qué. Si no cabe en una frase, probablemente son dos PCE.

## Pasos

| Paso | Comando | Qué hace |
|---|---|---|
| 1 | `git switch -c pce/descripcion-corta` | Crea una rama para este cambio y te pone en ella. `-c` = crear. |
| 2 | *(edita los archivos)* | Si cambias una decisión, crea una ADR nueva en `docs/adr/`. Si cambias un comportamiento, cambia también su prueba. |
| 3 | `python herramientas/verificar_catalogo.py` | Revisa IDs de historias, dependencias y ciclos. Debe terminar con `0 errores`. |
| 4 | `mkdocs build --strict` | Construye el sitio; falla si hay enlaces rotos. |
| 5 | `git add -A && git commit -m "Qué cambia, en una frase"` | Guarda el cambio. `add -A` incluye archivos nuevos y borrados. |
| 6 | `git push -u origin pce/descripcion-corta` | Sube la rama. `-u` la liga con GitHub para los siguientes `git push`. |
| 7 | `gh pr create --fill` | Abre el PR contra `main` con el mensaje del commit. Llena la plantilla en GitHub si falta algo. |
| 8 | `gh pr checks --watch` | Espera a que terminen las pruebas automáticas y muestra el resultado. |
| 9 | `gh pr merge --squash --delete-branch` | **Solo si el paso 8 salió en verde.** Une el PR en un commit, borra la rama y te regresa a `main`. |
| 10 | `git pull` | Baja el commit que acabas de unir. |

## Cómo saber que salió bien

`git log --oneline -1` muestra tu cambio con `(#N)` al final: ese `N` es el número del PCE.

## Si algo falla

- **El paso 3 o 4 marca errores:** corrígelos y repite desde el paso 3. No se sube nada que no pase.
- **El paso 8 sale en rojo:** `gh pr checks` da un enlace al registro; corrige, `git commit` y `git push` otra vez.
- **El PR dice que tiene conflictos:** `git pull origin main`, resuelve los archivos marcados, `git add -A && git commit && git push`.
- **Te equivocaste de rama antes del commit:** `git stash`, `git switch` a la correcta, `git stash pop`.

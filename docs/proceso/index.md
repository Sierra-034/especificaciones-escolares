# Manual del proceso

Este manual existe para que nada dependa de la memoria de nadie. Cada procedimiento dice
**cuándo** se usa, **qué necesitas antes**, **los pasos** con lo que hace cada comando,
**cómo saber que salió bien** y **qué hacer si algo falla**.

Si un procedimiento no funciona como está escrito, el procedimiento está mal, no tú:
corrígelo con un PCE (procedimiento A).

## ¿Qué quieres hacer?

| Situación | Procedimiento |
|---|---|
| Es la primera vez en una computadora, o algo de git/gh no responde | [0 · Preparar tu equipo](0-preparar-equipo.md) |
| Empiezas a trabajar (cada vez) | [0 · Preparar tu equipo → Antes de cada sesión](0-preparar-equipo.md#antes-de-cada-sesion) |
| Cambiar algo del estándar: una historia, una especificación, una ADR, una prueba, este manual | [A · Proponer un cambio (PCE)](A-proponer-cambio.md) |
| Publicar una versión del estándar | [B · Publicar una versión](B-publicar-version.md) |
| Hacer que la implementación use una versión nueva del estándar | [C · Fijar la versión en la implementación](C-fijar-version.md) |
| Encontraste un error en una versión ya publicada | [D · Corregir una versión publicada](D-corregir-version.md) |

## El ciclo completo

```
A. PCE (rama → PR → unir)  ──┐
A. otro PCE                ──┼──►  B. versión (CHANGELOG → etiqueta → release)  ──►  C. fijar en plataforma-escolar
A. otro PCE                ──┘                       │
                                                     └── si tenía un error ──► D. versión de corrección
```

Varios PCE se acumulan en `main`; una versión es una foto de `main` en un momento elegido.

## Glosario

| Término | Qué es |
|---|---|
| **PCE** | Propuesta de cambio al estándar. Siempre es un *pull request*; su número es el número del PR. |
| **Squash** | Forma de unir un PR: todos sus commits se vuelven uno solo en `main`. Así `main` se lee PCE por PCE. |
| **Etiqueta** (*tag*) | Nombre fijo que apunta a un commit, por ejemplo `esp-con-v0.2.0`. **Nunca se mueve.** |
| **Release** | Página en GitHub asociada a una etiqueta, con notas y un .zip. Es la forma visible de una versión. |
| **Pre-release** | Release marcado como «no estable». Lo usamos mientras todo esté en `0.x`. |
| **Submódulo** | Forma en que `plataforma-escolar` incluye al estándar en `estandar/`: guarda solo a qué commit apunta, no una copia. |
| **CHANGELOG** | Archivo `CHANGELOG.md`: lista, por versión, qué PCE entraron. Es la respuesta a «¿qué contiene esta versión?». |

## Reglas que no cambian

1. Nada entra a `main` sin PR.
2. Una etiqueta publicada nunca se mueve ni se borra. Si algo faltó, se publica otra versión (procedimiento D).
3. Antes de etiquetar, el CHANGELOG lista cada PCE que entra en la versión.
4. Una ADR aceptada no se edita: se escribe otra que la reemplaza.

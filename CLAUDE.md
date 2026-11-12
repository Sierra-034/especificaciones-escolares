# CLAUDE.md · especificaciones-escolares

Este repo es **el estándar**: qué debe hacer el sistema escolar y cómo se comprueba.
No hay código de la implementación aquí. La implementación de referencia
([plataforma-escolar](https://github.com/Sierra-034/plataforma-escolar)) lo consume como
submódulo de git en su carpeta `estandar/`, fijado a una versión. Lo que cambies aquí
lo verán todas las implementaciones cuando suban de versión, así que cada cambio se revisa.

## Todo cambio entra por PCE

Un PCE (propuesta de cambio al estándar) es un *pull request*. Nunca hagas commit directo a `main`.

1. Rama nueva: `git switch -c pce/descripcion-corta`.
2. Haz el cambio completo en esa rama (historia, especificación, prueba, vector, ADR: lo que toque).
3. Corre las verificaciones de abajo.
4. Abre el PR con la plantilla: qué especificación cambia, de qué versión a cuál, y el tipo
   (corrección, aclaración, nueva capacidad o cambio incompatible).
5. Tú preparas la rama y el PR; aprobar, fusionar y etiquetar lo hace una persona.

## Reglas

- **ADR.** Una ADR aceptada no se edita. Si una decisión cambia, escribe una ADR nueva
  (`docs/adr/NNNN-titulo.md`) que diga a cuál reemplaza. La numeración se comparte con
  plataforma-escolar: revisa el número más alto en los dos repos antes de elegir uno.
- **Comportamiento y prueba van juntos.** Si un PR cambia lo que el sistema debe hacer, cambia
  en el mismo PR la prueba de conformidad (`conformidad/`) y, si aplica, el vector (`vectores/`).
- **Contrato primero.** Un endpoint, esquema o error nuevo se escribe en `contratos/openapi.yaml`
  antes que cualquier código (principio 12).
- **IDs.** Historias `ESC-NN`, `UNI-NN`, `DOC-NN`; pruebas `C-NN`, únicas en todo el estándar
  (siguiente libre: C-51); ADR `NNNN`. Un ID retirado no se reutiliza.
- **Historias.** Un archivo por ID en `docs/historias/`, con el encabezado YAML de `_plantilla.md`.
  `depende_de` solo puede nombrar historias que existen, sin ciclos.
- **Versiones.** Cada especificación se etiqueta por separado: `esp-<id>-vX.Y.Z` (p. ej. `esp-con-v0.2.0`).
  En `0.x` puede cambiar con una ADR; desde `1.0`, un cambio incompatible sube la versión mayor.
- **Migración.** Los archivos que dicen «por migrar» enlazan a su fuente actual (artifacts de Claude).
  Al migrar, copia el texto fiel; si encuentras una incongruencia, repórtala en el PR en vez de
  resolverla por tu cuenta.
- **Sin datos reales.** Los vectores usan llaves de prueba; nunca llaves ni datos de un plantel real.
- Todo el texto del estándar va en español.

## Antes de abrir el PR

```bash
python herramientas/verificar_catalogo.py
mkdocs build --strict
```

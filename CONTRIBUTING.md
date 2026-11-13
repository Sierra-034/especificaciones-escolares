# Cómo contribuir

Paso a paso, con requisitos previos y qué hace cada comando: [Manual del proceso](docs/proceso/index.md).

## Proponer una historia nueva
Abre un *issue* con la plantilla «Historia de usuario» (Como / Quiero / Para).
No hace falta saber programar. Si se acepta, se le asigna el siguiente ID libre y entra como archivo en `docs/historias/`.

## Proponer un cambio al estándar (PCE)
Un PCE es un *pull request*. Reglas:
- Un PR = un cambio con sentido propio.
- Si cambia una decisión, agrega una ADR nueva (`docs/adr/NNNN-titulo.md`) que reemplace a la anterior. Las ADR no se editan.
- Si cambia el comportamiento, cambia también la prueba de conformidad y, si aplica, el vector.
- Indica en el PR qué especificación cambia y a qué versión sube.

## Antes de abrir el PR
```bash
python herramientas/verificar_catalogo.py
mkdocs build --strict
```

## IDs
- Historias: `ESC-NN` (escuela), `UNI-NN` (universidad), `DOC-NN` (docentes). Un ID retirado no se reutiliza.
- Pruebas: `C-NN`, numeración única en todo el estándar.
- ADR: `NNNN`, numeración compartida con la implementación de referencia.

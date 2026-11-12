"""Verifica el catálogo de historias: IDs únicos, nombre de archivo = id, dependencias existentes y sin ciclos.

Uso: python herramientas/verificar_catalogo.py
"""
import pathlib
import sys

import yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent / "docs" / "historias"


def leer(ruta):
    texto = ruta.read_text(encoding="utf-8")
    if not texto.startswith("---"):
        return None
    return yaml.safe_load(texto.split("---", 2)[1]) or {}


def main():
    errores, historias = [], {}
    for ruta in sorted(RAIZ.glob("*.md")):
        if ruta.name.startswith("_") or ruta.name == "index.md":
            continue
        meta = leer(ruta)
        if meta is None or "id" not in meta:
            errores.append(f"{ruta.name}: falta el encabezado con id")
            continue
        if meta["id"] != ruta.stem:
            errores.append(f"{ruta.name}: el id {meta['id']} no coincide con el nombre del archivo")
        if meta["id"] in historias:
            errores.append(f"{meta['id']}: id repetido")
        historias[meta["id"]] = meta.get("depende_de") or []

    for hid, deps in historias.items():
        for d in deps:
            if d not in historias:
                errores.append(f"{hid}: depende de {d}, que no existe")

    # ciclos (DFS con colores)
    color = {h: 0 for h in historias}

    def visitar(h, camino):
        color[h] = 1
        for d in historias[h]:
            if d not in color:
                continue
            if color[d] == 1:
                errores.append("ciclo: " + " → ".join(camino + [h, d]))
            elif color[d] == 0:
                visitar(d, camino + [h])
        color[h] = 2

    for h in historias:
        if color[h] == 0:
            visitar(h, [])

    for e in errores:
        print("ERROR", e)
    print(f"{len(historias)} historias revisadas, {len(errores)} errores")
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()

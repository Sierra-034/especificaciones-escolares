# D · Corregir una versión publicada

**Cuándo:** una versión ya subida tiene un error, le faltó algo, o la etiqueta cayó en el commit equivocado.

**Regla:** una etiqueta publicada **nunca** se mueve ni se borra. Alguien pudo haberse fijado en ella;
moverla le cambiaría el contenido sin avisar.

## Pasos

1. Corrige con uno o más PCE normales: procedimiento [A](A-proponer-cambio.md).
2. Publica una versión nueva con el procedimiento [B](B-publicar-version.md), subiendo CORRECCIÓN
   (`esp-con-v0.2.0` → `esp-con-v0.2.1`) si el arreglo no cambia el comportamiento, o MENOR si sí.
3. En el CHANGELOG, la sección nueva dice qué corrige: «Corrige: …».
4. Si la versión anterior no debe usarse: `gh release edit esp-con-v0.2.0 --notes "No usar: ver esp-con-v0.2.1"`.
   Se edita la nota del release; la etiqueta no se toca.
5. Fija la versión nueva en la implementación: procedimiento [C](C-fijar-version.md).

# ADR-0004 · El padrón oficial sigue siendo la fuente de verdad

- **Estado:** aceptada
- **Fecha:** 2026-11-10

> Migrado el 2026-11-13 desde [Diseño del MVP: control de acceso escolar](https://claude.ai/artifact/8z2qFXRnnrty1u4cJAGH4R). Texto copiado sin cambios.

## Contexto

La escuela ya tiene su registro de alumnos en otro sistema o en hojas de cálculo.

## Decisión

No somos el registro maestro. El padrón entra por un puerto `Padron` con un adaptador CSV para empezar (principios 7, 14 y 57).

## Consecuencias

Cambiar a una API después es cambiar el adaptador. Hay que definir cada cuánto se importa.


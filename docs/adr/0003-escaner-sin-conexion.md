# ADR-0003 · El escáner funciona sin conexión

- **Estado:** aceptada
- **Fecha:** 2026-11-10

> Migrado el 2026-11-13 desde [Diseño del MVP: control de acceso escolar](https://claude.ai/artifact/8z2qFXRnnrty1u4cJAGH4R). Texto copiado sin cambios.

## Contexto

La señal en la puerta no está garantizada.

## Decisión

Cada escaneo se guarda en el dispositivo como hecho inmutable con `ocurrio_en`, `recibido_en`, ID del dispositivo y una clave de idempotencia; se sincroniza cuando hay red (principios 17, 32 y 33).

## Consecuencias

Reenviar dos veces no duplica; el retardo se calcula con la hora real del escaneo. Fechas en UTC con zona `America/Mexico_City` (principio 20).


# ADR-0001 · La credencial es un documento firmado

- **Estado:** aceptada
- **Fecha:** 2026-11-10

> Migrado el 2026-11-13 desde [Diseño del MVP: control de acceso escolar](https://claude.ai/artifact/8z2qFXRnnrty1u4cJAGH4R). Texto copiado sin cambios.

## Contexto

La puerta no tiene red y el QR se puede fotografiar.

## Opciones

(a) un token aleatorio que se busca en el padrón descargado; (b) una credencial firmada con JWS que el escáner verifica con la llave pública.

## Decisión

(b). Lleva un ID opaco, el plantel y la vigencia; nunca nombre ni CURP (principios 21, 24 y 71).

## Consecuencias

Se verifica sin red y sin el padrón completo; las bajas viajan al escáner en una lista de revocación que se sincroniza. Deja abierta la verificación por terceros (ESC-07, UNI-10) sin cambiar nada.


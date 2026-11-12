# ADR-0008 · El JWS es la constancia; PDF y QR son el medio

- **Estado:** aceptada
- **Fecha:** por migrar
- **Fuente:** [Decisiones de diseño: MVP de constancias](https://claude.ai/artifact/BFv1HemHiY2yqZoTx7jqoc)

## Decisión
La constancia es un JWS. El QR lleva una URL con el folio (verificación en línea). El PDF/A-2b lleva el JWS adjunto. La página pública muestra nombre, plantel, semestre, grupo, ciclo y CURP enmascarada, sin matrícula. La anulación vive solo en el servidor. Las llaves retiradas quedan en el JWKS solo para verificar.

## Contexto y consecuencias
Por migrar desde la fuente.

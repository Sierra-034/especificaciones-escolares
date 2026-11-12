# ADR-0009 · Código de 6 dígitos para entrar

- **Estado:** aceptada
- **Fecha:** por migrar
- **Fuente:** [Decisiones de diseño: MVP de constancias](https://claude.ai/artifact/BFv1HemHiY2yqZoTx7jqoc)

## Decisión
Para entrar se envía un código de 6 dígitos (no enlace mágico), guardado como HMAC, a través del puerto Notificador. Adaptador del MVP: correo; demo: buzón simulado; SMS o WhatsApp después por configuración. `POST /v0/auth/codigo` responde siempre 202 para no revelar quién está en el padrón, con límite de solicitudes (429).

## Contexto y consecuencias
Por migrar desde la fuente.

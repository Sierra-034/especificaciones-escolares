---
id: ESP-IDP
version: 0.1.0
estado: borrador
---
# ESP-IDP · Identidad y acceso a la plataforma (v0.1)

> El texto de ESP-IDP v0.1 vive por ahora dentro de [ESP-PLA.md](ESP-PLA.md), porque la fuente
> ([Especificación v0.1: subsistema de acceso escolar](https://claude.ai/artifact/7T3STEZ5im4PVvaH1LJSBQ))
> cubre los dos subsistemas en un solo documento. Separarlos queda pendiente como PCE.

## Qué le toca a ESP-IDP

- **Historias:** ESC-19, 38, 44, 45, 46 (y ESC-63 en su versión mínima).
- **Pruebas:** C-01 a C-07, C-18, C-19, C-20, C-24.
- **Secciones de ESP-PLA.md que son de ESP-IDP:** Alcance y convenciones, Credencial, la parte de
  Administración de la API (importar padrón, emitir y revocar credenciales, llaves), y las filas de
  Identidad del Criterio de adopción.

## Lo que ESP-CON especifica por ahora en nombre de ESP-IDP

ESC-61 (entrar sin contraseña, con código de un solo uso) y ESC-63 (llaves de firma `constancia-*`) se
especifican hoy dentro de [ESP-CON](ESP-CON.md), con las pruebas C-26 a C-30 y C-48 a C-50.
Pasan a ESP-IDP en su versión 0.2.

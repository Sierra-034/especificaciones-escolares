# ADR-0013 · Las pruebas de un nivel solo usan historias de ese nivel o de los anteriores

**Estado:** aceptada, 2026-11-18 (Samuel). **Historias:** ESC-19, ESC-44, ESC-63. **Pruebas:** C-18, C-58, C-59, C-60.

**Decisión:** en el criterio de adopción de cualquier especificación, cada prueba que pide un nivel usa solo historias de ese nivel o de los anteriores. Si una prueba necesita otra historia, o esa historia entra al nivel o la prueba sube al primer nivel donde ya están todas. Una especificación pide de otro subsistema solo las historias que usa y las pruebas de esas historias, nunca un nivel completo de ese otro subsistema.

## Contexto

El criterio de adopción de ESP-CON 0.3 tenía dos problemas (P-20):

- Los niveles 1 a 3 pedían C-01 a C-07, C-19, C-20 y C-24 de ESP-IDP. Esas pruebas usan la credencial y el registro de entradas (ESC-29, ESC-38, ESC-45, ESC-46 y la puerta de ESP-PLA), que no están en ningún nivel de ESP-CON. Una escuela que adopta solo constancias, que es el caso del MVP, no podía declarar ningún nivel. El origen era la frase «requiere que ESP-IDP esté en nivel 2»: el nivel 2 de Identidad incluye la credencial.
- El nivel 1 (ESC-44, ESC-19, ESC-63) no se podía comprobar por sí solo: ESC-19 se probaba hasta C-51 (nivel 2) y ESC-63 hasta C-47 y C-55 (nivel 3).

La regla «cada nivel está cerrado bajo *depende de*» ya existía para las historias, pero nada decía lo mismo de las pruebas.

## Opciones consideradas

| Opción | A favor | En contra |
| --- | --- | --- |
| A. Regla general y pruebas nuevas; ESC-19 sube al nivel 2 (elegida) | Cada nivel se comprueba solo. El nivel 1 sigue existiendo y tiene sentido: padrón y llave listos. La regla sirve para las especificaciones que vengan. | ESC-19 cambia de nivel. Tres pruebas nuevas. |
| B. Juntar los niveles 1 y 2 de ESP-CON | Menos cambios: no hacen falta pruebas nuevas para el nivel 1. | Se pierde el escalón en que el plantel ya tiene padrón y llaves; el radar salta de 0 a 2. No arregla la causa para otras especificaciones. |
| C. Dejar las pruebas de la puerta y pedir la puerta para constancias | No cambia el criterio. | Obliga a construir la puerta para usar constancias, contra la decisión de hacer primero el MVP de constancias (2026-11-12). |

## Consecuencias

- **ESP-CON 0.4:** nivel 1 = ESC-44 y ESC-63, con C-18 (solo la parte del servidor) y C-58 (llaves publicadas). ESC-19 pasa al nivel 2, con C-59, que necesita la sesión de ESC-61. C-32 deja de comprobar la verificación y la nueva C-60 lo hace en el nivel 3.
- **El radar mide cada subsistema en su propio eje.** Una escuela solo de constancias puede tener Constancias en nivel 3 e Identidad por debajo del 2. Es un dato correcto, no un error.
- **Obliga a** toda especificación nueva: al escribir su criterio, revisar fila por fila qué historias usa cada prueba.
- **Deja abierto:** cuando ESP-IDP tenga su propio documento (versión 0.3), C-58 y C-59 se mueven allá con ESC-63 y ESC-19, igual que las pruebas de ESC-61.

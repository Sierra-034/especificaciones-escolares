# ADR-0014 · El estándar se publica con la licencia AGPL-3.0

**Estado:** aceptada, 2026-11-19 (Samuel). **Resuelve:** la mejora M2 de la [retrospectiva del 2026-11-13](../retrospectivas/2026-11-13.md).

**Decisión:** todo el repositorio `especificaciones-escolares` (historias, especificaciones, ADR, contrato OpenAPI, pruebas de conformidad, vectores y herramientas) se publica con la GNU Affero General Public License, versión 3 o cualquier versión posterior (identificador SPDX `AGPL-3.0-or-later`). El texto completo está en el archivo `LICENSE` de la raíz, copiado sin cambios de <https://www.gnu.org/licenses/agpl-3.0.txt>.

## Contexto

- El repositorio es público desde el 2026-11-12 y no tenía licencia. Sin licencia, la ley de derechos de autor reserva todos los derechos: nadie más puede copiar, modificar ni redistribuir el estándar, aunque lo pueda leer. Eso contradice el modelo del proyecto: software libre que no se vende, y se cobra por servicios y desarrollos específicos.
- El README proponía CC BY 4.0 para los textos y una licencia libre aparte para el código.
- El repositorio mezcla texto y código que van juntos: una prueba de conformidad cita la especificación, y el contrato OpenAPI es a la vez documento y entrada para generar código.

## Opciones consideradas

| Opción | A favor | En contra |
| --- | --- | --- |
| A. AGPL-3.0 para todo (elegida) | Una sola licencia para todo el repositorio. Es copyleft: quien modifique y redistribuya el estándar, o lo ofrezca como servicio en red, debe compartir sus cambios con la misma licencia. Encaja con el modelo de software libre del proyecto. | Es una licencia pensada para código; para los textos es menos común que CC BY-SA. Una implementación privativa no puede copiar el contrato ni las pruebas. |
| B. CC BY 4.0 para textos y una licencia libre aparte para el código | Lo habitual en estándares abiertos; cualquiera puede reutilizar el texto. | Dos licencias en un repositorio que mezcla texto y código; hay que decidir archivo por archivo. CC BY no obliga a compartir cambios: alguien puede publicar una variante cerrada del estándar. |
| C. Dejarlo sin licencia por ahora | Ningún trabajo hoy. | Legalmente nadie puede reutilizar el estándar, que es lo contrario de lo que se busca. |

## Consecuencias

- Cualquiera puede leer, usar, copiar, modificar y redistribuir el estándar, siempre que lo que redistribuya o sirva en red siga con AGPL-3.0 o posterior y conserve el aviso de licencia.
- **Implementaciones.** Las ideas y requisitos de una especificación no tienen derechos de autor: cualquiera puede escribir desde cero una implementación que pase las pruebas, con la licencia que quiera. Pero si una implementación copia archivos de aquí (por ejemplo `contratos/openapi.yaml`, código de `conformidad/` o los vectores), esa parte queda bajo AGPL-3.0. Correr las pruebas de conformidad contra un servidor no lo obliga a nada: solo le hablan por red.
- **Contribuciones.** Quien abre un PCE acepta que su aporte se publica con esta misma licencia (la licencia de entrada es la de salida). No se pide un acuerdo aparte.
- **«O posterior».** Si la FSF publica una AGPL versión 4, quien reutilice el estándar podrá elegir entre la 3 y la 4.
- **Deja abierto:** la licencia de `plataforma-escolar` (implementación de referencia), que se decide allá. La pregunta abierta de ESP-PLA sobre licencia se cierra cuando ESP-PLA tenga su siguiente versión.

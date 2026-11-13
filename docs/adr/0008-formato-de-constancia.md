# ADR-0008 · Formato de la constancia (PDF + QR de verificación)

> Migrado el 2026-11-13 desde [Decisiones de diseño: MVP de constancias](https://claude.ai/artifact/BFv1HemHiY2yqZoTx7jqoc) (fecha del original: 2026-11-12). Texto copiado sin cambios.

**Estado:** aceptado, 2026-11-12 (Samuel). **Historias:** ESC-05, ESC-07, ESC-62, ESC-63. **Pruebas:** C-34 a C-44.

**Decisión:** la constancia es la JWS firmada de ESP-CON; el PDF es solo su presentación. El QR lleva únicamente la URL `https://{plantel}/verificar/{folio}`, y la verificación se hace en línea contra el plantel.

## Contexto

- ESC-07 pide que un tercero (otra escuela, una empresa, una beca) compruebe una constancia sin cuenta ni app, desde el navegador.
- ESC-62 pide poder anular una constancia ya emitida, y la anulación debe verse al verificar.
- En el nivel 2 la constancia sigue con firma autógrafa; el QR y el folio se suman, no la sustituyen.
- La credencial de puerta (ADR-001) ya separa el documento firmado del medio que lo muestra. Aquí aplica lo mismo (principio 63): JWS = documento, PDF y QR = medio.
- A diferencia de la puerta, quien verifica una constancia casi siempre tiene red, y la verificación no tiene requisito de 3 s.

## Opciones consideradas

| Opción | Qué lleva el QR | A favor | En contra |
| --- | --- | --- | --- |
| A. Folio en URL (recomendada) | \~60 caracteres: `https://{plantel}/verificar/{folio}` | QR pequeño que se lee bien impreso o fotocopiado. Sin datos personales en el QR. La anulación siempre se ve. | Requiere red y que el servidor del plantel esté arriba. |
| B. JWS completa en el QR | 600 a 900 caracteres (nombre, CURP y demás datos) | Verifica la firma sin red. | QR denso que falla en fotocopia. Expone la CURP a cualquiera que lo escanee. Sin red no ve la anulación. |
| C. Folio + huella corta del contenido | URL + 8 caracteres de SHA-256 | Detecta un PDF alterado sin abrir la página. | Complica el formato y no aporta mucho sobre A, porque la página ya muestra los datos. |

## Decisión

1. **Documento.** La constancia es la JWS de ESP-CON (`typ: constancia+jwt`, EdDSA, `kid` que empieza por `constancia-`). Se guarda íntegra en el servidor y no cambia nunca.
2. **QR.** Lleva solo la URL con el folio (opción A), con corrección de errores nivel M y al menos 2.5 cm de lado.
3. **PDF.** Formato PDF/A-2b (archivable). Lleva los datos de la plantilla, el folio en texto legible, el QR, la leyenda «Verifique en {plantel}/verificar» y el espacio para la firma autógrafa. La JWS va incrustada como archivo adjunto del PDF (`constancia.jws`), para que una verificación sin red sea posible más adelante sin cambiar el formato.
4. **Página de verificación.** Pública, sin cuenta. El servidor devuelve la JWS y el estado; la página comprueba la firma contra el JWKS del plantel y muestra uno de cuatro resultados: válida, vencida, anulada o no encontrada.
5. **Datos visibles al tercero.** Nombre completo, plantel, semestre, grupo, ciclo, fecha de emisión y CURP enmascarada (`ABCD******XXX**`). Lo justo para compararlo con el papel. La matrícula no se muestra.
6. **Anulación.** Vive en el servidor, no en la JWS: una JWS firmada no se puede cambiar. Anular crea un hecho inmutable con motivo, quién y cuándo.
7. **Rotación de llaves.** Una llave `constancia-*` retirada se queda en el JWKS como solo verificación hasta que venza la última constancia que firmó.
8. **Folio no adivinable.** UUIDv4 (122 bits aleatorios): tener el folio equivale a tener el papel. La página limita consultas por IP para frenar barridos.

## Consecuencias

- **Se gana:** QR legible en cualquier impresión, sin datos personales en el QR, anulación inmediata y un formato que ya admite verificación sin red.
- **Se pierde:** sin red o con el servidor caído, el tercero no puede verificar. Se acepta en el MVP; la JWS incrustada en el PDF deja abierta la salida.
- **Obliga a:** publicar el JWKS del plantel en una URL estable y tener la página de verificación disponible todo el ciclo escolar.
- **Queda fuera:** firma electrónica del PDF (PAdES o e.firma SAT) y el formato oficial de la SEP, si lo hubiera. Cada uno pide su propio ADR.

## Agregar firmas más adelante

Sí, se pueden agregar sin cambiar el QR, el folio ni las constancias ya emitidas. Hay dos caminos, y ninguno cambia el formato:

1. **Verificación sin red.** La JWS firmada va adjunta en el PDF desde la primera versión. Un verificador posterior (la misma página leyendo el PDF, o una app) comprueba la firma con la llave pública del plantel, sin consultar el servidor. Solo se agrega el verificador.
2. **Firma electrónica del PDF** (PAdES o e.firma del director), para quitar la firma autógrafa donde se acepte. Se añade como una capa más sobre el mismo PDF. Pide su propio ADR por el tema legal.

El QR con URL y folio sigue sirviendo en ambos casos, porque la consulta en línea es la única que ve una anulación.

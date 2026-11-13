# Decisiones de diseño (ADR)

Una decisión por archivo. Una ADR aceptada no se edita: si cambia, se escribe otra que la reemplaza.
La numeración se comparte con la implementación de referencia. Las decisiones que solo afectan
a esa implementación (lenguaje, framework) viven allá.

| ADR | Decisión | Estado | Dónde |
|---|---|---|---|
| [0001](0001-credencial-documento-firmado.md) | La credencial es un documento firmado (JWS con EdDSA) | aceptada | aquí |
| [0002](0002-qr-fijo-en-mvp.md) | El QR del teléfono es fijo en el MVP | aceptada | aquí |
| [0003](0003-escaner-sin-conexion.md) | El escáner funciona sin conexión | aceptada | aquí |
| [0004](0004-padron-fuente-de-verdad.md) | El padrón oficial es la fuente de verdad | aceptada | aquí |
| [0005](0005-qr-invalido-solo-avisa.md) | Un QR inválido solo avisa | aceptada | aquí |
| 0006 | App multiplataforma con React Native | propuesta | plataforma-escolar |
| 0007 | Servidor y simulador en Python con FastAPI | aceptada | plataforma-escolar |
| [0008](0008-formato-de-constancia.md) | El JWS es la constancia; PDF y QR son el medio | aceptada | aquí |
| [0009](0009-entrega-de-codigo.md) | Código de 6 dígitos para entrar | aceptada | aquí |

Migradas el 2026-11-13 desde [Diseño del MVP](https://claude.ai/artifact/8z2qFXRnnrty1u4cJAGH4R) (0001–0007) y
[Decisiones de diseño: MVP de constancias](https://claude.ai/artifact/BFv1HemHiY2yqZoTx7jqoc) (0008–0009).

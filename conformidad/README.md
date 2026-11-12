# Pruebas de conformidad

Corren contra **cualquier** implementación por HTTP. Cada prueba lleva su ID de la especificación
con la marca `@pytest.mark.prueba("C-26")`, para poder decir «cumple ESP-CON v0.2 nivel 2».

```bash
pip install -e .
pytest --base-url http://localhost:8000
pytest --base-url http://localhost:8000 -m "not lenta"
```

Más adelante se publican como imagen de contenedor versionada, con la misma etiqueta que la especificación.

"""Pruebas de conformidad de ESP-CON v0.3 (C-26 a C-57). Por migrar desde la especificación."""
import pytest


@pytest.mark.prueba("C-26")
@pytest.mark.skip(reason="por migrar desde ESP-CON v0.3")
def test_c26(cliente):
    ...

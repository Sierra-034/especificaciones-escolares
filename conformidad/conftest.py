import httpx
import pytest


def pytest_addoption(parser):
    parser.addoption("--base-url", default="http://localhost:8000",
                     help="URL de la implementación bajo prueba")


@pytest.fixture(scope="session")
def cliente(request):
    with httpx.Client(base_url=request.config.getoption("--base-url"), timeout=10) as c:
        yield c

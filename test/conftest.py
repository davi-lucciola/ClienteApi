import pytest
from typing import Generator
from app import create_app
from fastapi.testclient import TestClient


@pytest.fixture(scope='function')
def test_client() -> Generator:
    with TestClient(create_app('Teste app', 'testando')) as test_client:
        yield test_client
import pytest
from pytest_mock import MockerFixture
from contextlib import asynccontextmanager
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine, Session as TestSession
from api import create_app
from api.utils.security import CryptService
from api.domain.services import UserService
from api.domain.interfaces import IUserRepository
from api.infra.entities import *
from api.infra.connections import get_db


# Integrated Tests Config
DATABASE_URL = 'sqlite:///:memory:'
test_engine = create_engine(
    DATABASE_URL,
    connect_args={
        'check_same_thread': False
    },
    poolclass=StaticPool
)


def get_test_db() -> Generator[TestSession, None, None]:
    global test_engine
    db = TestSession(bind=test_engine, autocommit=False)
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def test_lifespan(app):
    SQLModel.metadata.create_all(bind=test_engine)
    yield
    SQLModel.metadata.drop_all(bind=test_engine)


test_app = create_app('Teste app', 'App de Teste', test_lifespan)
test_app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(scope='module')
def test_client() -> Generator[TestClient, None, None]:
    with TestClient(test_app) as test_client:
        yield test_client


# Unit Tests Config
@pytest.fixture(scope='function')
def user_service(mocker: MockerFixture) -> Generator[UserService, None, None]:
    mock_user_repository = mocker.Mock(IUserRepository)
    yield UserService(CryptService(), mock_user_repository)

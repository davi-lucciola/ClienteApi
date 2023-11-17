import pytest
from typing import Generator
from pytest_mock import MockerFixture
from http import HTTPStatus
from api.utils.security import CryptService
from api.domain.services import UserService
from api.domain.exceptions import NoContentError, NotFoundError
from api.domain.interfaces.repositories import IUserRepository


@pytest.fixture(scope='function')
def user_service(mocker: MockerFixture) -> Generator[UserService, None, None]:
    mock_crypt_service = mocker.Mock(CryptService)
    mock_user_repository = mocker.Mock(IUserRepository)
    yield UserService(mock_crypt_service, mock_user_repository)


def test_users_no_content(user_service: UserService):
    user_service.user_repository.find_all.return_value = []

    with pytest.raises(NoContentError) as exception:
        users = user_service.find_all()
    
    assert exception.value.status_code == HTTPStatus.NO_CONTENT


def test_user_not_found(user_service: UserService):
    user_service.user_repository.find_by_id.return_value = None

    with pytest.raises(NotFoundError) as exception:
        users = user_service.find_by_id(1)
    
    assert exception.value.message == 'Usuário não encontrado.'
    assert exception.value.status_code == HTTPStatus.NOT_FOUND


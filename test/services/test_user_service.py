import pytest
from typing import Generator
from pytest_mock import MockerFixture
from http import HTTPStatus
from api.utils.security import CryptService
from api.domain.models import User
from api.domain.services import UserService
from api.domain.exceptions import DomainError, NoContentError, NotFoundError
from api.domain.interfaces.repositories import IUserRepository


# Tests Config
@pytest.fixture(scope='function')
def user_service(mocker: MockerFixture) -> Generator[UserService, None, None]:
    mock_crypt_service = mocker.Mock(CryptService)
    mock_user_repository = mocker.Mock(IUserRepository)
    yield UserService(mock_crypt_service, mock_user_repository)


@pytest.fixture(scope='function')
def valid_user():
    return User(**{
        'id': 1, 
        'email': 'teste@email.com', 
        'password': '1aA!', 
        'admin': False
    })


# Find All Tests
def test_users_no_content(user_service: UserService):
    user_service.user_repository.find_all.return_value = []

    with pytest.raises(NoContentError) as exception:
        users = user_service.find_all()
    
    assert exception.value.status_code == HTTPStatus.NO_CONTENT


# Find By Id Tests
def test_user_not_found(user_service: UserService):
    user_service.user_repository.find_by_id.return_value = None

    with pytest.raises(NotFoundError) as exception:
        users = user_service.find_by_id(1)
    
    assert exception.value.message == 'Usuário não encontrado.'
    assert exception.value.status_code == HTTPStatus.NOT_FOUND


# Create Tests
def test_user_password_less_then_4_chars(valid_user: User, user_service: UserService):
    valid_user.password = 'aa'

    with pytest.raises(ValueError) as exception:
        user_service.create(valid_user)
    
    assert exception.value.args[0] == 'Sua senha deve conter pelo menos 4 caracteres.'


def test_user_password_with_no_digits(valid_user: User, user_service: UserService):
    valid_user.password = 'aaaa'

    with pytest.raises(ValueError) as exception:
        user_service.create(valid_user)
    
    assert exception.value.args[0] == 'Sua senha deve conter numeros.'


def test_user_password_with_no_lowercase(valid_user: User, user_service: UserService):
    valid_user.password = '1AAA'

    with pytest.raises(ValueError) as exception:
        user_service.create(valid_user)
    
    assert exception.value.args[0] == 'Sua senha deve conter letras minúsculas.'


def test_user_password_with_no_uppercase(valid_user: User, user_service: UserService):
    valid_user.password = '1aaa'

    with pytest.raises(ValueError) as exception:
        user_service.create(valid_user)
    
    assert exception.value.args[0] == 'Sua senha deve conter letras maiúsculas.'


def test_user_password_with_no_special(valid_user: User, user_service: UserService):
    valid_user.password = '1Aaa'

    with pytest.raises(ValueError) as exception:
        user_service.create(valid_user)
    
    assert exception.value.args[0] == 'Sua senha deve conter caracteres especiais.'


def test_user_email_registered(valid_user: User, user_service: UserService):
    user_service.user_repository.find_by_email.return_value = valid_user.email

    with pytest.raises(DomainError) as exception:
        user_service.create(valid_user)
    
    assert exception.value.message == 'Email já cadastrado.'
    assert exception.value.status_code == HTTPStatus.BAD_REQUEST

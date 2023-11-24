from http import HTTPStatus
from fastapi.testclient import TestClient 


# Create User Schemas Tests
def test_create_public_user_invalid_email(test_client: TestClient) -> None:
    user_payload: dict = {'email':'emailinvalido', 'password':'aA12$', 'confirm_password':'aA12$'}
    response = test_client.post('/user/public', json=user_payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    
    body: dict = response.json()
    assert body.get('message') == 'Email Inválido, por favor digite um email válido.'


def test_create_public_user_passwords_does_not_match(test_client: TestClient) -> None:
    user_payload: dict = {'email':'valid@email.com', 'password':'aaaa', 'confirm_password':'bbbb'}
    response = test_client.post('/user/public', json=user_payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    
    body: dict = response.json()
    assert body.get('message') == 'A senha e a confirmação não são iguais.'


# Create User Success Test
def test_create_public_user_sucess(test_client: TestClient) -> None:
    user_payload: dict = {'email':'testcreate@email.com', 'password':'aA12$', 'confirm_password':'aA12$'}
    response = test_client.post('/user/public', json=user_payload)

    body: dict = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert body.get('message') == 'Usuário cadastrado com sucesso.'
    assert body.get('created_id') is not None


def test_create_public_user_invalid_email(test_client: TestClient) -> None:
    user_payload: dict = {'email':'emailinvalido', 'password':'aA12$', 'confirm_password':'aA12$'}
    response = test_client.post('/user/public', json=user_payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    
    body: dict = response.json()
    assert body.get('message') == 'Email Inválido, por favor digite um email válido.'


def test_create_public_user_passwords_does_not_match(test_client: TestClient) -> None:
    user_payload: dict = {'email':'valid@email.com', 'password':'aaaa', 'confirm_password':'bbbb'}
    response = test_client.post('/user/public', json=user_payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    
    body: dict = response.json()
    assert body.get('message') == 'A senha e a confirmação não são iguais.'


def test_create_public_user_sucess(test_client: TestClient) -> None:
    user_payload: dict = {'email':'testcreate@email.com', 'password':'aA12$', 'confirm_password':'aA12$'}
    response = test_client.post('/user/public', json=user_payload)

    body: dict = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert body.get('message') == 'Usuário cadastrado com sucesso.'
    assert body.get('created_id') is not None
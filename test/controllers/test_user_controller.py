from http import HTTPStatus
from fastapi.testclient import TestClient 

def test_find_all_users_sucess(test_client: TestClient) -> None:
    response = test_client.get('/user')
    
    assert response.status_code == HTTPStatus.OK
    
    users = response.json()
    assert len(users) > 0
    assert users[0].get('id') is not None
    assert users[0].get('email') is not None

def test_create_user_sucess(test_client: TestClient) -> None:
    user_payload: dict = {'email':'teste3@email.com', 'password':'1234', 'confirm_password':'1234'}
    response = test_client.post('/user/no-secure', json=user_payload)

    body: dict = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert body.get('message') == 'Usuário cadastrado com sucesso.'
    assert body.get('created_id') is not None
import pytest
from application import create_app


class TestApplication():

    @pytest.fixture
    def client(self):
        app = create_app('config.MockConfig')
        return app.test_client()
    
    @pytest.fixture
    def valid_user(self):
        return {
            "first_name": "James",
            "last_name": "Rhodes",
            "cpf": "425.403.090-89",
            "email": "warmachine@avengers.com",
            "birth_date": "1964-11-29"
        }

    @pytest.fixture
    def invalid_user(self):
        return {
            "first_name": "James",
            "last_name": "Rhodes",
            "cpf": "005.403.090-89",
            "email": "warmachine@avengers.com",
            "birth_date": "1964-11-29"
        }

    def test_get_users(self, client):
        response = client.get('/users')
        assert response.status_code == 200

    def test_post_users(self, client, valid_user, invalid_user):
        response = client.post('/user', json=valid_user)
        assert response.status_code == 200
        assert b"sucesso" in response.data

        response = client.post('/user', json=invalid_user)
        assert response.status_code == 400
        assert b"invalido" in response.data


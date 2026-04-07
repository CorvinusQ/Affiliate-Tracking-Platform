"""
API тесты аутентификации и авторизации
"""
import pytest
import requests
from datetime import datetime


BASE_URL = "https://api-test4-kassa.evropochta.by/api"


class TestAuthAPI:
    """Тестирование API авторизации"""

    def test_login_success(self):
        """
        API-001: Успешная авторизация
        
        Request:
        POST /auth/login
        Body: {email, password}
        
        Expected:
        Status: 200
        Response: {access_token, refresh_token, user}
        """
        payload = {
            "email": "test@example.com",
            "password": "Qwerty123!"
        }
        
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=payload
        )
        
        # Проверка статус-кода
        assert response.status_code == 200
        
        # Проверка структуры ответа
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "user" in data
        assert "id" in data["user"]
        assert "email" in data["user"]
        
        # Проверка формата токена (JWT)
        assert data["access_token"].startswith("eyJ")

    def test_login_invalid_credentials(self):
        """
        API-002: Авторизация с неверными данными
        
        Request:
        POST /auth/login
        Body: {email, wrong_password}
        
        Expected:
        Status: 401
        Response: {error: "Invalid credentials"}
        """
        payload = {
            "email": "test@example.com",
            "password": "WrongPassword123"
        }
        
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=payload
        )
        
        assert response.status_code == 401
        
        data = response.json()
        assert "error" in data
        assert "Неверный email или пароль" in data.get("message", "")

    def test_login_empty_email(self):
        """
        API-003: Авторизация без email
        
        Expected:
        Status: 400
        """
        payload = {
            "email": "",
            "password": "Qwerty123!"
        }
        
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=payload
        )
        
        assert response.status_code == 400

    def test_get_current_user(self):
        """
        API-004: Получение данных текущего пользователя
        
        Request:
        GET /auth/me
        Headers: {Authorization: Bearer <token>}
        
        Expected:
        Status: 200
        Response: {user}
        """
        # Сначала получаем токен
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": "test@example.com", "password": "Qwerty123!"}
        )
        token = login_response.json()["access_token"]
        
        # Делаем запрос к защищенному эндпоинту
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data
        assert "email" in data

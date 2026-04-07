"""
API тесты основных эндпоинтов
"""
import pytest
import requests


BASE_URL = "https://api-test4-kassa.evropochta.by/api"


def get_auth_token():
    """Вспомогательная функция для получения токена"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "test@example.com", "password": "Qwerty123!"}
    )
    return response.json()["access_token"]


class TestCampaignsAPI:
    """Тестирование API кампаний"""

    def test_get_campaigns_list(self):
        """
        API-010: Получение списка кампаний
        
        Expected:
        Status: 200
        Response: {campaigns: [], total: int}
        """
        token = get_auth_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(
            f"{BASE_URL}/campaigns",
            headers=headers
        )
        
        assert response.status_code == 200
        
        data = response.json()
        assert "campaigns" in data
        assert isinstance(data["campaigns"], list)

    def test_create_campaign(self):
        """
        API-011: Создание кампании
        
        Request:
        POST /campaigns
        Body: {name, budget, source}
        
        Expected:
        Status: 201
        Response: {campaign}
        """
        token = get_auth_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        payload = {
            "name": f"Test Campaign {int(__import__('time').time())}",
            "budget": 1000,
            "source": "facebook"
        }
        
        response = requests.post(
            f"{BASE_URL}/campaigns",
            headers=headers,
            json=payload
        )
        
        assert response.status_code == 201
        
        data = response.json()
        assert "id" in data
        assert data["name"] == payload["name"]
        assert data["budget"] == payload["budget"]

    def test_update_campaign(self):
        """
        API-012: Обновление кампании
        
        Request:
        PUT /campaigns/{id}
        Body: {name, budget}
        
        Expected:
        Status: 200
        """
        token = get_auth_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        # Сначала создаем кампанию
        create_response = requests.post(
            f"{BASE_URL}/campaigns",
            headers=headers,
            json={"name": "Test", "budget": 1000, "source": "facebook"}
        )
        campaign_id = create_response.json()["id"]
        
        # Обновляем
        update_payload = {"budget": 2000}
        response = requests.put(
            f"{BASE_URL}/campaigns/{campaign_id}",
            headers=headers,
            json=update_payload
        )
        
        assert response.status_code == 200
        assert response.json()["budget"] == 2000


class TestReportsAPI:
    """Тестирование API отчетов"""

    def test_get_report(self):
        """
        API-020: Получение отчета
        
        Expected:
        Status: 200
        Response: {metrics: {roi, conversions, spend}}
        """
        token = get_auth_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        params = {
            "from": "2025-01-01",
            "to": "2025-01-31"
        }
        
        response = requests.get(
            f"{BASE_URL}/reports",
            headers=headers,
            params=params
        )
        
        assert response.status_code == 200
        
        data = response.json()
        assert "metrics" in data
        assert "roi" in data["metrics"]
        assert "conversions" in data["metrics"]

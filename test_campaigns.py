"""
Тесты создания и управления кампаниями
"""
import pytest
from playwright.sync_api import sync_playwright, expect
from faker import Faker

fake = Faker()


class TestCampaigns:
    """Тестирование работы с рекламными кампаниями"""

    @pytest.fixture
    def authenticated_page(self):
        """Фикстура с авторизованной страницей"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            
            # Авторизация
            page.goto("https://app.evropochta.by/login")
            page.fill("#email", "test@example.com")
            page.fill("#password", "Qwerty123!")
            page.click("button[type='submit']")
            page.wait_for_url("*/dashboard")
            
            yield page
            
            browser.close()

    def test_create_campaign(self, authenticated_page):
        """
        TC-010: Создание новой кампании
        
        Шаги:
        1. Перейти в раздел "Кампании"
        2. Нажать "Создать кампанию"
        3. Заполнить обязательные поля
        4. Сохранить
        
        Ожидаемый результат:
        - Кампания создана
        - Отображается в списке
        """
        page = authenticated_page
        
        # Шаг 1: Перейти в кампании
        page.click("a[href='/campaigns']")
        page.wait_for_url("*/campaigns")
        
        # Шаг 2: Нажать создать
        page.click("button:has-text('Создать кампанию')")
        
        # Шаг 3: Заполнить форму
        campaign_name = f"Test Campaign {fake.uuid4()[:8]}"
        page.fill("#campaign-name", campaign_name)
        page.fill("#budget", "1000")
        page.select_option("#source", "facebook")
        
        # Шаг 4: Сохранить
        page.click("button[type='submit']")
        
        # Проверка: кампания создана
        page.wait_for_url("*/campaigns/*")
        assert campaign_name in page.inner_text(".campaign-header")

    def test_filter_campaigns(self, authenticated_page):
        """
        TC-011: Фильтрация кампаний по статусу
        
        Шаги:
        1. Открыть список кампаний
        2. Выбрать фильтр "Активные"
        3. Применить фильтр
        
        Ожидаемый результат:
        - Показаны только активные кампании
        """
        page = authenticated_page
        
        page.click("a[href='/campaigns']")
        page.wait_for_url("*/campaigns")
        
        # Выбрать фильтр
        page.select_option("#status-filter", "active")
        page.click("button:has-text('Применить')")
        
        # Проверка: все кампании активны
        campaigns = page.locator(".campaign-item").all()
        for campaign in campaigns:
            assert "active" in campaign.get_attribute("class")

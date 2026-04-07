"""
Тесты авторизации и работы с сессией
"""
import pytest
from playwright.sync_api import sync_playwright, expect


class TestLogin:
    """Тестирование процесса входа в систему"""

    @pytest.fixture
    def browser(self):
        """Фикстура для запуска браузера"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            yield browser
            browser.close()

    @pytest.fixture
    def page(self, browser):
        """Фикстура для создания страницы"""
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        yield page
        context.close()

    def test_login_success(self, page):
        """
        TC-001: Успешная авторизация
        
        Шаги:
        1. Открыть страницу входа
        2. Ввести корректный email и пароль
        3. Нажать кнопку "Войти"
        
        Ожидаемый результат:
        - Переход на дашборд
        - Отображение приветствия
        """
        # Шаг 1: Открыть страницу входа
        page.goto("https://app.evropochta.by/login")
        
        # Шаг 2: Ввести credentials
        page.fill("#email", "test@example.com")
        page.fill("#password", "Qwerty123!")
        
        # Шаг 3: Нажать кнопку входа
        page.click("button[type='submit']")
        
        # Проверка: перешли на дашборд
        expect(page).to_have_url("https://app.evropochta.by/dashboard")
        
        # Проверка: видим приветствие
        assert page.is_visible("#welcome-banner")
        assert "Добро пожаловать" in page.inner_text("#welcome-banner")

    def test_login_invalid_password(self, page):
        """
        TC-002: Вход с неверным паролем
        
        Шаги:
        1. Открыть страницу входа
        2. Ввести email и неверный пароль
        3. Нажать кнопку "Войти"
        
        Ожидаемый результат:
        - Ошибка авторизации
        - Сообщение "Неверный email или пароль"
        """
        page.goto("https://app.evropochta.by/login")
        
        page.fill("#email", "test@example.com")
        page.fill("#password", "WrongPassword123")
        page.click("button[type='submit']")
        
        # Проверка: остались на странице входа
        expect(page).to_have_url("https://app.evropochta.by/login")
        
        # Проверка: видим ошибку
        error_message = page.locator(".error-message")
        assert error_message.is_visible()
        assert "Неверный email или пароль" in error_message.inner_text()

    def test_login_empty_fields(self, page):
        """
        TC-003: Попытка входа с пустыми полями
        
        Шаги:
        1. Открыть страницу входа
        2. Не заполнять поля
        3. Нажать кнопку "Войти"
        
        Ожидаемый результат:
        - Валидация полей
        - Сообщение "Заполните обязательные поля"
        """
        page.goto("https://app.evropochta.by/login")
        page.click("button[type='submit']")
        
        # Проверка: поля подсвечены как обязательные
        email_field = page.locator("#email")
        assert email_field.get_attribute("required") is not None

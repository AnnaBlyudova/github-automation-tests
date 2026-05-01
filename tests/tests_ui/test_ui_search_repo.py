import pytest
import time
import os
from typing import Generator
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import allure

load_dotenv()


@pytest.mark.ui
class TestUISearchRepo:
    """Тест UI-5: Поиск репозитория."""

    @pytest.fixture(autouse=True)
    def setup(self) -> Generator[None, None, None]:
        """
        Подготовка перед тестом.

        Запускает браузер, настраивает ожидания.
        После теста закрывает браузер.
        """
        self.driver: webdriver.Chrome = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )
        self.driver.maximize_window()
        self.wait: WebDriverWait = WebDriverWait(self.driver, 20)
        yield
        self.driver.quit()

    @allure.title("UI-5: Поиск репозитория по названию")
    @allure.story("UI тесты - Поиск")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_repository(self) -> None:
        """
        Проверяет поиск репозитория через веб-интерфейс.

        Ожидаемый результат: репозиторий найден, открыта его страница.
        """
        search_term: str = "python-curse"
        username: str = os.getenv("GITHUB_USERNAME", "")
        password: str = os.getenv("GITHUB_PASSWORD", "")

        with allure.step("Авторизация на GitHub"):
            self.driver.get("https://github.com/login")

            поле_логин: WebElement = self.driver.find_element(
                By.ID, "login_field")
            поле_логин.send_keys(username)

            поле_пароль: WebElement = self.driver.find_element(
                By.ID, "password")
            поле_пароль.send_keys(password)

            кнопка_войти: WebElement = self.driver.find_element(
                By.NAME, "commit")
            кнопка_войти.click()
            time.sleep(3)

        with allure.step(f"Поиск репозитория '{search_term}'"):
            поле_поиска: WebElement = self.wait.until(
                EC.presence_of_element_located((
                    By.ID,
                    "dashboard-repos-filter-left"
                ))
            )
            поле_поиска.clear()
            поле_поиска.send_keys(search_term)
            time.sleep(2)

        with allure.step(f"Переход к репозиторию {search_term}"):
            ссылка: WebElement = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    f"//a[contains(@href, '/{search_term}')]"
                ))
            )
            ссылка.click()
            time.sleep(3)

        with allure.step("Проверка, что открылась страница репозитория"):
            assert search_term in self.driver.current_url, (
                f"Не перешли на страницу репозитория. URL: {
                    self.driver.current_url}"
            )

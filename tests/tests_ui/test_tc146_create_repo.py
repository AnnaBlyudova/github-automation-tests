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
from api.github_api import GitHubAPI
import allure

load_dotenv()


@pytest.mark.ui
class TestTC146:
    """Тест TC146: Создание публичного репозитория с README."""

    @pytest.fixture(autouse=True)
    def setup(self) -> Generator[None, None, None]:
        """
        Подготовка перед тестом.

        Создаёт клиент API, запускает браузер, настраивает ожидания.
        После теста закрывает браузер и удаляет все созданные репозитории.
        """
        self.api: GitHubAPI = GitHubAPI()
        self.driver: webdriver.Chrome = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )
        self.driver.maximize_window()
        self.wait: WebDriverWait = WebDriverWait(self.driver, 20)
        yield
        self.driver.quit()
        self.api.cleanup()

    @allure.title("TC146: Создание публичного репозитория с README через UI")
    @allure.story("UI тесты - Репозитории")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_public_repo_with_readme(self) -> None:
        """
        Проверяет создание публичного репозитория с README через веб-интерфейс.

        Ожидаемый результат: бейдж Public отображается,
        README.md присутствует, URL содержит имя репозитория.
        """
        repo_name: str = f"ui-test-{int(time.time())}"
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

        with allure.step("Переход на страницу создания репозитория"):
            self.driver.get("https://github.com/new")

        with allure.step(f"Ввод имени репозитория {repo_name}"):
            self.wait.until(
                EC.presence_of_element_located((
                    By.ID, "repository-name-input"))
            )
            поле_имени: WebElement = self.driver.find_element(
                By.ID, "repository-name-input"
            )
            поле_имени.send_keys(repo_name)

        with allure.step("Включение README"):
            переключатель: WebElement = self.driver.find_element(
                By.CSS_SELECTOR, "button[aria-labelledby='add-readme']"
            )
            if переключатель.get_attribute("data-checked") == "false":
                переключатель.click()
            time.sleep(1)

        with allure.step("Создание репозитория"):
            кнопка: WebElement = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//span[text()='Create repository']/ancestor::button"
                ))
            )
            кнопка.click()
            time.sleep(3)

        with allure.step("Проверка наличия бейджа Public"):
            assert "Public" in self.driver.page_source, (
                "Бейдж 'Public' не отображается"
            )

        with allure.step("Проверка наличия файла README.md"):
            assert "README.md" in self.driver.page_source, (
                "Файл README.md отсутствует"
            )

        with allure.step(f"Проверка URL содержит {repo_name}"):
            assert repo_name in self.driver.current_url, (
                f"URL не содержит {repo_name}"
            )

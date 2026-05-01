"""
Тест TC147: Создание новой ветки

Проверяет создание новой ветки через веб-интерфейс GitHub.
"""

import pytest
import time
import os
from typing import Generator
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from api.github_api import GitHubAPI
import allure

load_dotenv()


@pytest.mark.ui
class TestTC147:
    """Тест TC147: Создание новой ветки."""

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

    @allure.title("TC147: Создание новой ветки через UI")
    @allure.story("UI тесты - Ветки")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_new_branch(self) -> None:
        """
        Проверяет создание новой ветки через веб-интерфейс.

        Ожидаемый результат: новая ветка отображается на странице репозитория.
        """
        branch_name: str = f"test-branch-{int(time.time())}"
        repo_name: str = f"repo-for-branch-{int(time.time())}"
        username: str = os.getenv("GITHUB_USERNAME", "")

        with allure.step(f"Создание репозитория {repo_name} через API"):
            self.api.create_repository(
                repo_name, private=False, auto_init=True)

        with allure.step("Авторизация на GitHub"):
            self.driver.get("https://github.com/login")

            поле_логин: WebElement = self.driver.find_element(
                By.ID, "login_field")
            поле_логин.send_keys(username)

            поле_пароль: WebElement = self.driver.find_element(
                By.ID, "password")
            поле_пароль.send_keys(os.getenv("GITHUB_PASSWORD", ""))

            кнопка_войти: WebElement = self.driver.find_element(
                By.NAME, "commit")
            кнопка_войти.click()
            time.sleep(3)

        with allure.step(f"Открытие страницы репозитория {repo_name}"):
            self.driver.get(f"https://github.com/{username}/{repo_name}")
            time.sleep(3)

        with allure.step("Нажатие на кнопку выбора ветки"):
            кнопка_ветки: WebElement = self.wait.until(
                EC.element_to_be_clickable((
                    By.ID, "ref-picker-repos-header-ref-selector"))
            )
            кнопка_ветки.click()
            time.sleep(1)

        with allure.step(f"Ввод имени новой ветки {branch_name}"):
            поле_ввода: WebElement = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[aria-label='Filter branches']")
                )
            )
            поле_ввода.send_keys(branch_name)
            time.sleep(1)

        with allure.step("Создание ветки (нажатие Enter)"):
            поле_ввода.send_keys(Keys.ENTER)
            time.sleep(3)

        with allure.step(f"Проверка, что ветка {branch_name} создана"):
            assert branch_name in self.driver.page_source, (
                f"Ветка '{branch_name}' не найдена на странице"
            )

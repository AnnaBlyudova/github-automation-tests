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
class TestUIEditDescription:
    """Тест UI-4: Редактирование описания репозитория."""

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

    @allure.title("UI-4: Редактирование описания репозитория")
    @allure.story("UI тесты - Редактирование")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_repository_description(self) -> None:
        """
        Проверяет редактирование описания репозитория через интерфейс.

        Ожидаемый результат: новое описание отображается на странице.
        """
        repo_name: str = f"edit-test-{int(time.time())}"
        new_description: str = f"Updated description {int(time.time())}"
        username: str = os.getenv("GITHUB_USERNAME", "")
        password: str = os.getenv("GITHUB_PASSWORD", "")

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
            поле_пароль.send_keys(password)

            кнопка_войти: WebElement = self.driver.find_element(
                By.NAME, "commit")
            кнопка_войти.click()
            time.sleep(3)

        with allure.step(f"Открытие репозитория {repo_name}"):
            self.driver.get(f"https://github.com/{username}/{repo_name}")
            time.sleep(2)

        with allure.step("Нажатие на иконку шестерёнки"):
            кнопка_шестерёнка: WebElement = self.wait.until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR, "summary.float-right[role='button']"))
            )
            кнопка_шестерёнка.click()
            time.sleep(1)

        with allure.step(f"Ввод нового описания: {new_description}"):
            поле_описания: WebElement = self.wait.until(
                EC.visibility_of_element_located((
                    By.NAME, "repo_description"))
            )
            поле_описания.clear()
            поле_описания.send_keys(new_description)
            time.sleep(1)

        with allure.step("Сохранение изменений"):
            кнопка_сохранить: WebElement = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[@type='submit' and "
                    "contains(text(), 'Save changes')]"
                ))
            )
            кнопка_сохранить.click()
            time.sleep(2)

        with allure.step(f"Проверка, что описание '{new_description}' "
                         f"отображается"):
            assert new_description in self.driver.page_source, (
                f"Описание '{new_description}' не найдено"
            )

import pytest
import os
import requests
import time
from typing import Dict, Any
from dotenv import load_dotenv
import allure

load_dotenv()


@pytest.mark.api
class TestCreatePrivateRepo:
    """Тесты для создания приватного репозитория."""

    @allure.title("API-152: Создание приватного репозитория")
    @allure.story("API тесты - Репозитории")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_private_repository(self) -> None:
        """
        Проверяет создание приватного репозитория через API.

        Ожидаемый результат: статус 201, репозиторий приватный,
        имя совпадает, full_name содержит имя пользователя.
        """
        repo_name: str = f"private-test-{int(time.time())}"
        url: str = "https://api.github.com/user/repos"

        headers: Dict[str, str] = {
            "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN', '')}",
            "Accept": "application/vnd.github+json"
        }

        body: Dict[str, Any] = {
            "name": repo_name,
            "private": True,
            "description": "Test private repository"
        }

        step_text = f"Отправить POST запрос для создания репозитория {
            repo_name}"
        with allure.step(step_text):
            response = requests.post(url, json=body, headers=headers)

        with allure.step("Проверить статус ответа 201"):
            assert response.status_code == 201, (
                f"Ожидался 201, получен {response.status_code}"
            )

        with allure.step("Проверить имя репозитория"):
            assert response.json()["name"] == repo_name

        with allure.step("Проверить, что репозиторий приватный"):
            assert response.json()["private"] is True

        with allure.step("Проверить, что full_name содержит имя пользователя"):
            username = os.getenv("GITHUB_USERNAME", "")
            assert username in response.json()["full_name"]

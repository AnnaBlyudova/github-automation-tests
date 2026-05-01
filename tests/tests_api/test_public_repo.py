import pytest
import os
import requests
import time
from typing import Dict, Any
from dotenv import load_dotenv
import allure

load_dotenv()


@pytest.mark.api
class TestCreatePublicRepo:
    """Тесты для создания публичного репозитория."""

    @allure.title("API-151: Создание публичного репозитория")
    @allure.story("API тесты - Репозитории")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_public_repository(self) -> None:
        """
        Проверяет создание публичного репозитория через API.

        Ожидаемый результат: статус 201, репозиторий публичный,
        имя совпадает, URL содержит github.com.
        """
        repo_name: str = f"public-test-{int(time.time())}"
        url: str = "https://api.github.com/user/repos"

        headers: Dict[str, str] = {
            "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN', '')}",
            "Accept": "application/vnd.github+json"
        }

        body: Dict[str, Any] = {
            "name": repo_name,
            "private": False,
            "description": "Test public repository"
        }

        with allure.step(
            f"Отправить POST запрос "
            f"для создания репозитория {repo_name}"
        ):
            response = requests.post(url, json=body, headers=headers)

        with allure.step("Проверить статус ответа 201"):
            assert response.status_code == 201, f"Ожидался 201, получен {
                response.status_code}"

        with allure.step("Проверить имя репозитория"):
            assert response.json()["name"] == repo_name

        with allure.step("Проверить, что репозиторий публичный"):
            assert response.json()["private"] is False

        with allure.step("Проверить URL репозитория"):
            assert "github.com" in response.json()["html_url"]

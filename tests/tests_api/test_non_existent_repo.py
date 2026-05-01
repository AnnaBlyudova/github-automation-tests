import pytest
import os
import requests
import time
from typing import Dict
from dotenv import load_dotenv
import allure

load_dotenv()


@pytest.mark.api
class TestNonExistentRepo:
    """Тесты для получения несуществующего репозитория."""

    @allure.title(
            "API-157: Получение несуществующего репозитория (ошибка 404)")
    @allure.story("API тесты - Негативные сценарии")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_non_existent_repository(self) -> None:
        """
        Проверяет ошибку при запросе несуществующего репозитория.

        Ожидаемый результат: статус 404, сообщение 'Not Found'.
        """
        username = os.getenv("GITHUB_USERNAME", "")
        repo_name: str = f"not-exist-{int(time.time())}"
        url: str = f"https://api.github.com/repos/{username}/{repo_name}"

        headers: Dict[str, str] = {
            "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN', '')}",
            "Accept": "application/vnd.github+json"
        }

        with allure.step(
            f"Отправить GET запрос для несуществующего репозитория {repo_name}"
        ):
            response = requests.get(url, headers=headers)

        with allure.step("Проверить статус ответа 404"):
            assert response.status_code == 404, (
                f"Ожидался 404, получен {response.status_code}"
            )

        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            сообщение = response_data.get("message", "")
            assert сообщение == "Not Found", (
                f"Ожидалось 'Not Found', получено '{сообщение}'"
            )

        with allure.step("Проверить наличие ссылки на документацию"):
            assert "documentation_url" in response_data, (
                "Поле documentation_url отсутствует"
            )

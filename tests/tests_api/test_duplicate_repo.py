import pytest
import os
import requests
import time
from typing import Dict, Any
from dotenv import load_dotenv
import allure

load_dotenv()


@pytest.mark.api
class TestDuplicateRepo:
    """Тесты для создания репозитория с уже существующим именем."""

    @allure.title("API-156: Создание дубликата репозитория (ошибка 422)")
    @allure.story("API тесты - Негативные сценарии")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_duplicate_repository(self) -> None:
        """
        Проверяет ошибку при создании репозитория с именем,
        которое уже существует.

        Ожидаемый результат: статус 422, сообщение об ошибке
        'Repository creation failed' или 'Validation Failed'.
        """
        url: str = "https://api.github.com/user/repos"
        repo_name: str = f"duplicate-test-{int(time.time())}"

        headers: Dict[str, str] = {
            "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN', '')}",
            "Accept": "application/vnd.github+json"
        }

        body: Dict[str, Any] = {
            "name": repo_name,
            "private": False
        }

        with allure.step(f"Создать репозиторий {repo_name} первый раз"):
            response1 = requests.post(url, json=body, headers=headers)
            assert response1.status_code == 201, (
                f"Первый запрос: ожидался 201, получен {response1.status_code}"
            )

        with allure.step(
            f"Попробовать создать репозиторий {repo_name} повторно"
        ):
            response2 = requests.post(url, json=body, headers=headers)

        with allure.step("Проверить статус ответа 422"):
            assert response2.status_code == 422, (
                f"Ожидался 422, получен {response2.status_code}"
            )

        with allure.step("Проверить сообщение об ошибке"):
            response_data = response2.json()
            сообщение = response_data.get("message", "")
            assert (
                "Repository creation failed" in сообщение
                or "Validation Failed" in сообщение
            ), f"Неожиданное сообщение: {сообщение}"

        with allure.step("Проверить наличие списка errors"):
            assert "errors" in response_data, "Поле errors отсутствует"
            список_ошибок = response_data["errors"]
            assert isinstance(список_ошибок, list), (
                "Поле errors должно быть списком"
            )
            assert len(список_ошибок) > 0, "Список errors пуст"

import pytest
import os
import requests
from typing import Dict
from dotenv import load_dotenv
import allure

load_dotenv()


@pytest.mark.api
class TestCreateWithoutName:
    """Тесты для создания репозитория без указания имени."""

    @allure.title("API-154: Создание репозитория без имени (ошибка 422)")
    @allure.story("API тесты - Негативные сценарии")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_repository_without_name(self) -> None:
        """
        Проверяет ошибку при создании репозитория без поля name.

        Ожидаемый результат: статус 422, сообщение об ошибке содержит 'name',
        в ответе есть массив errors.
        """
        url: str = "https://api.github.com/user/repos"

        headers: Dict[str, str] = {
            "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN', '')}",
            "Accept": "application/vnd.github+json"
        }

        body: Dict[str, object] = {
            "private": False,
            "description": "Test repo without name"
        }

        with allure.step("Отправить POST запрос без поля name"):
            response = requests.post(url, json=body, headers=headers)

        with allure.step("Проверить статус ответа 422"):
            assert response.status_code == 422, (
                f"Ожидался 422, получен {response.status_code}"
            )

        with allure.step("Проверить, что сообщение об ошибке содержит 'name'"):
            response_data = response.json()
            message = response_data.get("message", "")
            assert "name" in message.lower(), (
                f"Сообщение '{message}' не содержит 'name'"
            )

        with allure.step("Проверить, что в ответе есть массив errors"):
            assert "errors" in response_data, "Поле errors отсутствует"
            assert isinstance(response_data["errors"], list), (
                "Поле errors должно быть списком"
            )
            assert len(response_data["errors"]) > 0, "Массив errors пуст"

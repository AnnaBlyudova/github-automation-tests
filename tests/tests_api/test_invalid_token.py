import pytest
import requests
from typing import Dict
import allure


@pytest.mark.api
class TestInvalidToken:
    """Тесты для проверки ошибки при неверном токене."""

    @allure.title(
            "API-155: Создание репозитория с неверным токеном (ошибка 401)")
    @allure.story("API тесты - Негативные сценарии")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_repository_invalid_token(self) -> None:
        """
        Проверяет ошибку авторизации при использовании неверного токена.

        Ожидаемый результат: статус 401, сообщение 'Bad credentials'.
        """
        url: str = "https://api.github.com/user/repos"

        headers: Dict[str, str] = {
            "Authorization": "Bearer invalid_token_12345",
            "Accept": "application/vnd.github+json"
        }

        body: Dict[str, object] = {
            "name": "token-test",
            "private": True,
            "description": "waiting for error"
        }

        with allure.step("Отправить POST запрос с неверным токеном"):
            response = requests.post(url, json=body, headers=headers)

        with allure.step("Проверить статус ответа 401"):
            assert response.status_code == 401, (
                f"Ожидался 401, получен {response.status_code}"
            )

        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            сообщение = response_data.get("message", "")
            assert сообщение == "Bad credentials", (
                f"Ожидалось 'Bad credentials', получено '{сообщение}'"
            )

        with allure.step("Проверить наличие документации"):
            assert "documentation_url" in response_data, (
                "Поле documentation_url отсутствует"
            )

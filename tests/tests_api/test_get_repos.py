import pytest
import os
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv
import allure

load_dotenv()


@pytest.mark.api
class TestGetRepositories:
    """Тесты для получения списка репозиториев."""

    @allure.title("API-153: Получение списка репозиториев")
    @allure.story("API тесты - Репозитории")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_repositories(self) -> None:
        """
        Проверяет получение списка репозиториев через API.

        Ожидаемый результат: статус 200, ответ в виде массива,
        массив содержит хотя бы один элемент.
        """
        url: str = "https://api.github.com/user/repos"

        headers: Dict[str, str] = {
            "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN', '')}",
            "Accept": "application/vnd.github+json"
        }

        with allure.step(
                "Отправить GET запрос для получения списка репозиториев"):
            response = requests.get(url, headers=headers)

        with allure.step("Проверить статус ответа 200"):
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}"
            )

        with allure.step("Проверить, что ответ является массивом"):
            repos: List[Dict[str, Any]] = response.json()
            assert isinstance(repos, list)

        with allure.step("Проверить, что массив не пустой"):
            assert len(repos) > 0, "Список репозиториев пуст"

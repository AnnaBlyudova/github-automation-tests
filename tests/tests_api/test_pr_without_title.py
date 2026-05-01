import pytest
import os
import requests
import time
from typing import Dict
from dotenv import load_dotenv
import allure

load_dotenv()


@pytest.mark.api
class TestPrWithoutTitle:
    """Тесты для создания Pull Request без заголовка."""

    @allure.title("API-158: Создание Pull Request без заголовка (ошибка 422)")
    @allure.story("API тесты - Негативные сценарии")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_pr_without_title(self) -> None:
        """
        Проверяет ошибку при создании Pull Request без поля title.

        Ожидаемый результат: статус 422.
        """
        username = os.getenv("GITHUB_USERNAME", "")
        token = os.getenv("GITHUB_TOKEN", "")

        headers: Dict[str, str] = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

        repo_name: str = f"pr-test-{int(time.time())}"
        branch_name: str = f"test-branch-{int(time.time())}"

        with allure.step(f"Создать репозиторий {repo_name}"):
            url_repo = "https://api.github.com/user/repos"
            repo_data = {
                "name": repo_name,
                "private": False,
                "auto_init": True
            }
            response = requests.post(url_repo, json=repo_data, headers=headers)
            assert response.status_code == 201, (
                f"Ожидался 201 при создании репозитория, "
                f"получен {response.status_code}"
            )

        with allure.step(f"Создать ветку {branch_name}"):
            commits_url = (
                f"https://api.github.com/repos/"
                f"{username}/{repo_name}/commits/main"
            )
            commits_response = requests.get(commits_url, headers=headers)
            sha = commits_response.json()["sha"]

            branch_url = (
                f"https://api.github.com/repos/{username}/{repo_name}/git/refs"
            )
            branch_data = {
                "ref": f"refs/heads/{branch_name}",
                "sha": sha
            }
            response = requests.post(
                branch_url, json=branch_data, headers=headers
            )
            assert response.status_code == 201, (
                f"Ожидался 201 при создании ветки, "
                f"получен {response.status_code}"
            )

        with allure.step("Отправить POST запрос на создание PR без title"):
            pr_url = (
                f"https://api.github.com/repos/"
                f"{username}/{repo_name}/pulls"
            )
            pr_data = {
                "body": "creation without title",
                "head": branch_name,
                "base": "main"
            }
            response = requests.post(pr_url, json=pr_data, headers=headers)

        with allure.step("Проверить статус ответа 422"):
            assert response.status_code == 422, (
                f"Ожидался 422, получен {response.status_code}"
            )

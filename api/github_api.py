import requests
import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

load_dotenv()


class GitHubAPI:
    """Класс для работы с GitHub API."""

    def __init__(self) -> None:
        """Настраивает подключение к API, берёт токен из .env."""
        self.base_url: str = "https://api.github.com"
        self.token: Optional[str] = os.getenv("GITHUB_TOKEN")
        self.username: Optional[str] = os.getenv("GITHUB_USERNAME")
        self.headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }
        self.created_repos: List[str] = []

    def create_repository(
        self,
        name: str,
        private: bool = False,
        auto_init: bool = True
    ) -> Dict[str, Any]:
        """
        Создаёт новый репозиторий через API.

        Параметры:
            name (str): Название репозитория.
            private (bool): Приватный или публичный. По умолчанию False.
            auto_init (bool): Добавить README. По умолчанию True.

        Возвращает:
            Dict[str, Any]: Ответ от GitHub API в виде словаря.
        """
        url: str = f"{self.base_url}/user/repos"
        data: Dict[str, Any] = {
            "name": name,
            "private": private,
            "auto_init": auto_init
        }
        response = requests.post(url, json=data, headers=self.headers)
        if response.status_code == 201:
            self.created_repos.append(name)
        return response.json()

    def delete_repository(self, name: str) -> bool:
        """
        Удаляет репозиторий через API.

        Параметры:
            name (str): Название репозитория.

        Возвращает:
            bool: True если удаление успешно, False если нет.
        """
        if not self.username:
            return False
        url: str = f"{self.base_url}/repos/{self.username}/{name}"
        response = requests.delete(url, headers=self.headers)
        return response.status_code == 204

    def cleanup(self) -> None:
        """Удаляет все репозитории, которые были созданы через этот клиент."""
        for repo_name in self.created_repos:
            self.delete_repository(repo_name)
        self.created_repos.clear()

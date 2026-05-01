import os
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Настройки окружения для тестов."""

    USERNAME: str = os.getenv("GITHUB_USERNAME", "")
    TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    PASSWORD: Optional[str] = os.getenv("GITHUB_PASSWORD")
    BASE_URL: str = os.getenv("BASE_URL", "https://api.github.com")
    UI_BASE_URL: str = os.getenv("UI_BASE_URL", "https://github.com")
    TEST_REPO_NAME: str = "Final-Project"

    @staticmethod
    def get_headers(token: Optional[str] = None) -> Dict[str, str]:
        """
        Возвращает заголовки для API запросов.

        Параметры:
        token (Optional[str]):
            Токен доступа.Если не указан, берётся из настроек.

        Возвращает:
        Dict[str, str]: Заголовки Authorization, Accept, X-GitHub-Api-Version.
        """
        token = token or Config.TOKEN
        return {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }

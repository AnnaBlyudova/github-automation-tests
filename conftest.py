import pytest
import os
from typing import Dict, Any, Generator
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from api.github_api import GitHubAPI

load_dotenv()


@pytest.fixture
def config() -> Dict[str, Any]:
    return {
        "username": os.getenv("GITHUB_USERNAME", ""),
        "token": os.getenv("GITHUB_TOKEN", ""),
        "password": os.getenv("GITHUB_PASSWORD", ""),
        "base_url": "https://api.github.com",
        "ui_url": "https://github.com"
    }


@pytest.fixture
def api_client() -> Generator[GitHubAPI, None, None]:
    client = GitHubAPI()
    yield client
    client.cleanup()


@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()

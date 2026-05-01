import pytest
import time
import os
import requests
from typing import Generator
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from api.github_api import GitHubAPI
import allure

load_dotenv()


@pytest.mark.ui
class TestTC148:

    @pytest.fixture(autouse=True)
    def setup(self) -> Generator[None, None, None]:
        self.api = GitHubAPI()
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 30)
        yield
        self.driver.quit()
        self.api.cleanup()

    @allure.title("TC148: Создание Pull Request через UI")
    @allure.story("UI тесты - Pull Requests")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_pull_request(self) -> None:
        pr_title = f"Test PR {int(time.time())}"
        repo_name = f"pr-test-repo-{int(time.time())}"
        branch_name = f"feature-branch-{int(time.time())}"
        username = os.getenv("GITHUB_USERNAME", "")
        token = os.getenv("GITHUB_TOKEN", "")

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

        with allure.step(f"Создание репозитория {repo_name} через API"):
            self.api.create_repository(
                repo_name, private=False, auto_init=True)

        with allure.step("Получение SHA последнего коммита из main"):
            commits_url = (
                f"https://api.github.com/repos/"
                f"{username}/{repo_name}/commits/main"
            )
            sha = requests.get(commits_url, headers=headers).json()["sha"]

        with allure.step(f"Создание ветки {branch_name} через API"):
            branch_url = (
                f"https://api.github.com/repos/"
                f"{username}/{repo_name}/git/refs"
            )
            branch_data = {"ref": f"refs/heads/{branch_name}", "sha": sha}
            requests.post(branch_url, json=branch_data, headers=headers)

        with allure.step("Создание коммита в новой ветке"):
            blob_url = (
                f"https://api.github.com/repos/"
                f"{username}/{repo_name}/git/blobs"
            )
            blob_data = {
                "content": f"Test\n{int(time.time())}",
                "encoding": "utf-8"
            }
            blob_sha = requests.post(
                blob_url, json=blob_data, headers=headers
            ).json()["sha"]

            new_tree_url = (
                f"https://api.github.com/repos/"
                f"{username}/{repo_name}/git/trees"
            )
            new_tree_data = {
                "base_tree": sha,
                "tree": [
                    {
                        "path": "file.txt",
                        "mode": "100644",
                        "type": "blob",
                        "sha": blob_sha
                    }
                ]
            }
            new_tree_sha = requests.post(
                new_tree_url, json=new_tree_data, headers=headers
                ).json()["sha"]

            commit_url = (
                f"https://api.github.com/repos/"
                f"{username}/{repo_name}/git/commits"
            )
            commit_data = {
                "message": "Test commit",
                "tree": new_tree_sha,
                "parents": [sha]
            }
            commit_response = requests.post(
                commit_url, json=commit_data, headers=headers
            )
            commit_sha = commit_response.json()["sha"]

            update_url = (
                f"https://api.github.com/repos/"
                f"{username}/{repo_name}/git/refs/heads/{branch_name}"
            )
            requests.patch(
                    update_url,
                    json={"sha": commit_sha, "force": True},
                    headers=headers
                    )
        time.sleep(3)

        with allure.step("Авторизация на GitHub"):
            self.driver.get("https://github.com/login")
            self.driver.find_element(By.ID, "login_field").send_keys(username)
            self.driver.find_element(By.ID, "password").send_keys(
                os.getenv("GITHUB_PASSWORD", ""))
            self.driver.find_element(By.NAME, "commit").click()
            time.sleep(3)

        with allure.step(
            f"Переход на страницу создания PR для ветки {branch_name}"
        ):
            self.driver.get(
                f"https://github.com/{username}/"
                f"{repo_name}/compare/{branch_name}?expand=1"
            )
            time.sleep(3)

        with allure.step(f"Заполнение заголовка PR: {pr_title}"):
            поле_заголовка = self.wait.until(EC.presence_of_element_located((
                By.NAME, "pull_request[title]")))
            поле_заголовка.send_keys(pr_title)
            time.sleep(1)

        with allure.step("Создание Pull Request"):
            кнопка = self.wait.until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, "button.hx_create-pr-button")))
            кнопка.click()
            time.sleep(4)

        with allure.step("Проверка статуса PR"):
            assert "Open" in self.driver.page_source, "Статус PR не 'Open'"
            assert pr_title in self.driver.page_source, (
                f"Заголовок '{pr_title}' не найден"
            )

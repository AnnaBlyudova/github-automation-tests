from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import allure


class RepositoryPage(BasePage):
    """Страница репозитория GitHub."""

    REPO_NAME_INPUT = (By.ID, "repository-name-input")
    README_SWITCH = (By.CSS_SELECTOR, "button[aria-labelledby='add-readme']")
    CREATE_REPO_BUTTON = (
        By.XPATH, "//span[text()='Create repository']/ancestor::button")
    PUBLIC_BADGE = (By.XPATH, "//span[contains(text(), 'Public')]")
    README_FILE = (By.XPATH, "//a[contains(@href, 'README.md')]")
    BRANCH_BUTTON = (By.ID, "ref-picker-repos-header-ref-selector")
    BRANCH_INPUT = (By.CSS_SELECTOR, "input[aria-label='Filter branches']")
    PR_TAB = (By.CSS_SELECTOR, "[data-tab-item='pull-requests']")
    NEW_PR_BUTTON = (By.CSS_SELECTOR, "a[href*='/compare']")
    COMPARE_SELECT = (
        By.CSS_SELECTOR, "button[data-testid='compare-dropdown']")
    PR_TITLE_INPUT = (By.NAME, "pull_request[title]")
    CREATE_PR_BUTTON = (By.CSS_SELECTOR, "button.hx_create-pr-button")

    @allure.step("Создать репозиторий с именем {repo_name}")
    def create_repository(self, repo_name: str) -> None:
        """
        Создаёт новый репозиторий через UI.

        Параметры:
            repo_name (str): Название репозитория.
        """
        self.open("https://github.com/new")
        self.wait.until(EC.presence_of_element_located(self.REPO_NAME_INPUT))
        self.input_text(self.REPO_NAME_INPUT, repo_name)

        readme_btn = self.find_element(self.README_SWITCH)
        if readme_btn.get_attribute("data-checked") == "false":
            readme_btn.click()

        self.click(self.CREATE_REPO_BUTTON)

    @allure.step("Открыть репозиторий {repo_name}")
    def open_repository(self, username: str, repo_name: str) -> None:
        """
        Открывает страницу репозитория.

        Параметры:
            username (str): Имя пользователя.
            repo_name (str): Название репозитория.
        """
        self.open(f"https://github.com/{username}/{repo_name}")

    @allure.step("Создать ветку {branch_name}")
    def create_branch(self, branch_name: str) -> None:
        """
        Создаёт новую ветку через интерфейс.

        Параметры:
            branch_name (str): Название новой ветки.
        """
        self.click(self.BRANCH_BUTTON)
        branch_input = self.wait.until(
            EC.presence_of_element_located(self.BRANCH_INPUT))
        branch_input.send_keys(branch_name)
        branch_input.send_keys(Keys.ENTER)

    @allure.step("Проверить, что ветка {branch_name} отображается")
    def is_branch_displayed(self, branch_name: str) -> bool:
        """
        Проверяет, отображается ли ветка на странице.

        Параметры:
            branch_name (str): Название ветки.

        Возвращает:
            bool: True если ветка есть на странице, иначе False.
        """
        return branch_name in self.driver.page_source

    @allure.step("Проверить, что бейдж Public отображается")
    def is_public_badge_displayed(self) -> bool:
        """
        Проверяет, есть ли бейдж Public на странице.

        Возвращает:
            bool: True если бейдж есть, иначе False.
        """
        return self.is_element_visible(self.PUBLIC_BADGE, timeout=10)

    @allure.step("Проверить, что README.md существует")
    def is_readme_exists(self) -> bool:
        """
        Проверяет, есть ли файл README.md в репозитории.

        Возвращает:
            bool: True если README.md есть, иначе False.
        """
        return self.is_element_visible(self.README_FILE, timeout=10)

    @allure.step("Перейти на вкладку Pull Requests")
    def go_to_pull_requests_tab(self) -> None:
        """Переходит на вкладку Pull Requests."""
        self.click(self.PR_TAB)

    @allure.step("Нажать New Pull Request")
    def click_new_pull_request(self) -> None:
        """Нажимает кнопку New Pull Request."""
        self.click(self.NEW_PR_BUTTON)

    @allure.step("Выбрать compare ветку {branch_name}")
    def select_compare_branch(self, branch_name: str) -> None:
        """
        Выбирает ветку для сравнения из выпадающего списка.

        Параметры:
            branch_name (str): Название ветки для сравнения.
        """
        self.click(self.COMPARE_SELECT)
        branch_option = (
            By.XPATH, f"//span[contains(text(), '{branch_name}')]")
        self.click(branch_option)

    @allure.step("Заполнить заголовок PR: {title}")
    def fill_pr_title(self, title: str) -> None:
        """
        Заполняет заголовок Pull Request.

        Параметры:
            title (str): Заголовок PR.
        """
        title_input = self.wait.until(EC.presence_of_element_located(
            self.PR_TITLE_INPUT))
        title_input.send_keys(title)

    @allure.step("Создать Pull Request")
    def click_create_pull_request(self) -> None:
        """Нажимает кнопку Create pull request."""
        self.click(self.CREATE_PR_BUTTON)

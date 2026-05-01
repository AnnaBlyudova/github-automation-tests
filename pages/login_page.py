from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import Config
from typing import Optional
import allure


class LoginPage(BasePage):
    """Страница входа в GitHub."""

    USERNAME_INPUT = (By.ID, "login_field")
    PASSWORD_INPUT = (By.ID, "password")
    SIGN_IN_BUTTON = (By.NAME, "commit")

    @allure.step("Авторизоваться на GitHub")
    def login(self, username: Optional[str] = None, password: Optional[str] =
              None) -> None:
        """
        Входит на сайт с логином и паролем.

        Параметры:
            username (Optional[str]): Логин. Если не указан, берётся из .env.
            password (Optional[str]): Пароль. Если не указан, берётся из .env.
        """
        if username is None:
            username = Config.USERNAME or ""
        if password is None:
            password = Config.PASSWORD or ""

        self.open("https://github.com/login")
        self.input_text(self.USERNAME_INPUT, str(username))
        self.input_text(self.PASSWORD_INPUT, str(password))
        self.click(self.SIGN_IN_BUTTON)

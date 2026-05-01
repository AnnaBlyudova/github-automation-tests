from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Tuple
import allure


class BasePage:
    """Базовый класс для всех страниц."""

    def __init__(self, driver: WebDriver) -> None:
        """
        Сохраняет драйвер и настраивает ожидания.

        Параметры:
            driver (WebDriver): Драйвер браузера.
        """
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 20)

    @allure.step("Открыть страницу: {url}")
    def open(self, url: str) -> None:
        """
        Открывает страницу по ссылке.

        Параметры:
            url (str): Адрес страницы.
        """
        self.driver.get(url)

    @allure.step("Найти элемент: {locator}")
    def find_element(self, locator: Tuple[str, str],
                     timeout: int = 20) -> WebElement:
        """
        Ищет элемент на странице. Ждёт, если нужно.

        Параметры:
            locator (Tuple[str, str]): Локатор элемента.
            timeout (int): Сколько секунд ждать. По умолчанию 20.

        Возвращает:
            WebElement: Найденный элемент.
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    @allure.step("Кликнуть на элемент: {locator}")
    def click(self, locator: Tuple[str, str]) -> None:
        """
        Нажимает на элемент.

        Параметры:
            locator (Tuple[str, str]): Локатор элемента.
        """
        element: WebElement = self.wait.until(
            EC.element_to_be_clickable(locator))
        element.click()

    @allure.step("Ввести текст '{text}' в поле {locator}")
    def input_text(self, locator: Tuple[str, str], text: str) -> None:
        """
        Печатает текст в поле.

        Параметры:
            locator (Tuple[str, str]): Локатор поля.
            text (str): Текст для ввода.
        """
        element: WebElement = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента: {locator}")
    def get_text(self, locator: Tuple[str, str]) -> str:
        """
        Забирает текст из элемента.

        Параметры:
            locator (Tuple[str, str]): Локатор элемента.

        Возвращает:
            str: Текст внутри элемента.
        """
        return self.find_element(locator).text

    @allure.step("Проверить видимость элемента: {locator}")
    def is_element_visible(self, locator:
                           Tuple[str, str], timeout: int = 10) -> bool:
        """
        Проверяет, виден ли элемент на странице.

        Параметры:
            locator (Tuple[str, str]): Локатор элемента.
            timeout (int): Сколько секунд ждать. По умолчанию 10.

        Возвращает:
            bool: True если виден, False если нет.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

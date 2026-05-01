# github-automation-tests


Автоматизация UI и API тестирования GitHub

## Ссылка на финальный проект

[Финальный проект по ручному тестированию](https://anna-qa.yonote.ru/doc/finalnyj-proekt-po-ruchnomu-testirovaniyu-0gt9N3Xq8E)

## Описание проекта

Проект содержит автоматизированные тесты для GitHub, разработанные на основе ручных тест-кейсов из курсовой работы.

### Объекты тестирования

1. Создание репозитория
2. Создание и управление ветками
3. Создание и слияние Pull Request

### Количество тестов

API тесты - 8 
UI тесты - 5 
Итого - 13


## Установка и запуск

### 1. Клонирование репозитория

git clone https://github.com/AnnaBlyudova/github-automation-tests.git
cd github-automation-tests

## Создание виртуального окружения

python -m venv venv
venv\Scripts\activate  # Windows

## Установка зависимостей

pip install -r requirements.txt

## Настройка переменных окружения

Создайте файл .env в корне проекта:

GITHUB_USERNAME=ваш_логин
GITHUB_TOKEN=ваш_токен
GITHUB_PASSWORD=ваш_пароль
BASE_URL=https://api.github.com
UI_BASE_URL=https://github.com

### Запуск тестов

# Все тесты
pytest -v

# Только API тесты
pytest -m api -v

# Только UI тесты
pytest -m ui -v

# С Allure отчётом
pytest --alluredir=allure-results
allure serve allure-results


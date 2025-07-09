# stud-iu-back

Бэкенд сайта «Стундеческого совета факультета ИУ»

## Необходимо

Пакетный менеджер Python - [Poetry](https://python-poetry.org/).

## Инструкция по запуску

1. Склонировать репозиторий и перейти в рабочую директорию.

    ```shell
    git clone https://github.com/bmstu-itstech/stud-iu-back.git

    cd stud-iu-back
    ```

2. Активировать виртуальное окружение Python (venv) через [Poetry](https://python-poetry.org/).

    ```shell
    poetry env use python3
    ```

    Или можно указать путь к python

    ```shell
    poetry env use /c/some_path/python.exe
    ```

3. Установить зависимости через [Poetry](https://python-poetry.org/).

    ```shell
    poetry install --no-root 
    ```

    Далее все команды нужно выполнять с помощью [poetry](https://python-poetry.org/)

4. Создать базу данных, применить существующие миграции.

    ```shell
    poetry run python manage.py migrate 
    ```

5. Создать супер-пользователя для страницы администратора.

    ```shell
    poetry run python manage.py createsuperuser
    ```

6. Запустить сервер. По умолчанию сервер будет запущен на http://localhost:8000/

    ```shell
    poetry run python manage.py runserver 
    ```

## Полезные страницы

- Страница администратора: http://localhost:8000/admin
- Документация в Swagger: http://localhost:8000/api/swagger

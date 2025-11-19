# stud-iu-back

Бэкенд сайта «Стундеческого совета факультета ИУ»

## Инструкция по запуску [разработка]

### Необходимо

- Пакетный менеджер Python - [Poetry](https://python-poetry.org/).

### Действия

1. Склонировать репозиторий и перейти в рабочую директорию

    ```shell
    git clone https://github.com/bmstu-itstech/stud-iu-back.git
    cd stud-iu-back
    ```

2. Активировать виртуальное окружение Python (venv) через [Poetry](https://python-poetry.org/)

    ```shell
    poetry env use python3
    ```

    > Можно указать путь к Python
    >
    > ```shell
    > poetry env use /c/some_path/python.exe
    > ```

3. Установить зависимости через [Poetry](https://python-poetry.org/)

    ```shell
    poetry install --no-root 
    ```

    Далее все команды нужно выполнять с помощью [poetry](https://python-poetry.org/)

4. Применить миграции

    ```shell
    poetry run python manage.py migrate 
    ```

5. Создать суперпользователя (опционально)

    ```shell
    poetry run python manage.py createsuperuser
    ```

6. Запустить сервер (по умолчанию сервер будет запущен на http://localhost:8000/)

    ```shell
    poetry run python manage.py runserver 
    ```

### Полезные страницы

- Страница администратора: http://localhost:8000/admin
- Документация в Swagger: http://localhost:8000/api/swagger

## Инструкция по запуску [продукт]

### Необходимо

- [Docker Compose](https://docs.docker.com/compose/);
- [Docker](https://docs.docker.com/).

### Действия

1. Создать файл `.env` и указать значения переменных окружения (пример значений расположен в файле `.env.example`)

2. Запустить контейнеры

    ```shell
    docker compose up -d
    ```

3. Создать суперпользователя (опционально)

    ```shell
    docker compose exec backend python manage.py createsuperuser
    ```

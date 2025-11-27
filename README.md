# django-admin-test

Тестовые сценарии проверки работы системы администрирования проекта.

# Технологии:
- Python 3.14.0
- Django 5.2.8
- behave
- python-dotenv

# Как развернуть проект локально:
Клонируйте проект из репозитория:

```
git clone https://github.com/aadgnv/django-admin-test.git
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать и выполнить миграции:

```
python manage.py makemigrations
python manage.py migrate
```

Создать суперпользователя и снова выполнить миграции:

```
python manage.py createsuperuser
python manage.py migrate
```

Записать в переменные окружения (файл .env) данные регистрации суперпользователя,
случайные данные для негативного тестирования авторизации.

- корректные username и password
- не корректные username и password

Запустить проект:

```
python manage.py runserver
```

Запустить тесты:

```
behave
```

import os
from behave import given, when, then
from dotenv import load_dotenv


load_dotenv()


@given('Открываем страницу admin')
def open_page(context):
    context.response = context.client.get('/admin/', follow=True)


@then('Видим форму входа')
def status_200(context):
    html = context.response.content.decode('utf-8')
    assert context.response.status_code == 200
    assert '<form' in html
    assert 'login' in html.lower()


@given('Дан администратор с корректными данными')
def admin(context):
    username = os.getenv('ADMIN_USER')
    password = os.getenv('ADMIN_PASS')

    if not username or not password:
        raise ValueError('Переменные ADMIN_USER или ADMIN_PASS не найдены.')

    context.admin_username = username
    context.admin_password = password


@when('Когда мы используем корректные данные для входа')
def login_admin(context):
    context.response = context.client.post('/admin/login/', {
        'username': context.admin_username,
        'password': context.admin_password,
        'this_is_the_login_form': '1',
        'next': '/admin/'
    }, follow=True)


@then('Тогда переходим на главную Django administration')
def check_dashboard(context):
    html = context.response.content.decode()
    assert context.response.status_code == 200
    assert context.response.request['PATH_INFO'].startswith('/admin/')
    assert 'Django administration' in html or 'Site administration' in html


@given('Мы забыли корректные данные')
def ivalid_admin(context):
    wrong_user = os.getenv('INVALID_USER')
    wrong_pass = os.getenv('INVALID_PASS')

    if not wrong_user or not wrong_pass:
        raise ValueError('INVALID_USER или INVALID_PASS не найдены.')

    context.invalid_username_attempt = wrong_user
    context.invalid_password_attempt = wrong_pass


@when('Когда мы используем неверные данные для входа')
def invalid_login_admin(context):
    context.response = context.client.post('/admin/login/', {
        'username': context.invalid_username_attempt,
        'password': context.invalid_password_attempt,
        'this_is_the_login_form': '1',
    }, follow=True)


@then('То получаем ошибку входа')
def fail(context):
    html = context.response.content.decode()
    assert 'Please enter the correct username and password' in html or \
           'Note that both fields may be case-sensitive' in html
    assert context.response.status_code == 200
    assert context.response.request['PATH_INFO'] == '/admin/login/'

import os
from behave import given, when, then
from django.contrib.auth.models import Group
from dotenv import load_dotenv


load_dotenv()


@given('Мы авторизованы как админ')
def authorized_as_admin(context):
    username = os.getenv('ADMIN_USER')
    password = os.getenv('ADMIN_PASS')

    if not username or not password:
        raise ValueError('Переменные ADMIN_USER или ADMIN_PASS не найдены.')
    login_success = context.client.login(username=username, password=password)
    assert login_success, (
       'Проверьте логин/пароль или существование пользователя.'
    )
    is_logged_in = context.client.session.get('_auth_user_id') is not None
    assert is_logged_in, 'Ошибка авторизации: Клиент не смог войти как админ.'


@when('Создаем группу "{group_name}"')
def create_group(context, group_name):
    context.response = context.client.post('/admin/auth/group/add/', {
        'name': group_name,
        '_save': 'Save'
    }, follow=True)


@then('Группа "{group_name}" отображается в Recent actions')
def verify_group_in_actions(context, group_name):
    assert Group.objects.filter(name=group_name).exists(), (
        f'Группа "{group_name}" не найдена в БД'
    )
    home_response = context.client.get('/admin/')
    html = home_response.content.decode('utf-8')
    assert group_name in html, (
        f'Название группы "{group_name}" не найдено в Recent actions '
        f'на главной странице админки.'
    )


@given('Мы авторизованы как админ и "{group_name}" существует')
def authorized_and_group(context, group_name):
    authorized_as_admin(context)

    if not Group.objects.filter(name=group_name).exists():
        Group.objects.create(name=group_name)

    context.group_to_delete_name = group_name


@when('удаляем "{group_name}" как админ')
def delete_group(context, group_name):
    try:
        group_id = Group.objects.get(name=group_name).id
    except Group.DoesNotExist:
        assert False, (
            f'Группа "{group_name}" не найдена.'
        )
    context.response = context.client.post(
        f'/admin/auth/group/{group_id}/delete/',
        {'post': 'yes'},  # Словарь можно оставить в одну строку
        follow=True
    )


@then('Группа "{group_name}" удалена')
def then_group_is_deleted(context, group_name):
    assert context.response.status_code == 200
    assert '/admin/auth/group/' in context.response.request['PATH_INFO']
    group_exists_after_deletion = (
        Group.objects.filter(name=group_name).exists()
    )
    assert not group_exists_after_deletion, (
        f'Ошибка: Группа "{group_name}" не удалена.'
    )

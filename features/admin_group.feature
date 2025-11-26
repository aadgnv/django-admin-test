Feature: Работа с группами

  Scenario: Добавление группы пользователей
    Given Мы авторизованы как админ
    When Создаем группу "{group_name}"
    Then Группа "{group_name}" отображается в Recent actions

  Scenario: Удаление группы пользователей
    Given Мы авторизованы как админ и "{group_name}" существует
    When удаляем "{group_name}" как админ
    Then Группа "{group_name}" удалена
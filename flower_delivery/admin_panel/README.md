**Приложение admin_panel**

**Описание**

Приложение admin_panel предназначено для администрирования сайта и предоставляет функции для управления заказами и пользователями через специальный интерфейс, доступный только администраторам.

**Основные функции**

1\. Управление заказами. Страница admin_orders.html позволяет администраторам просматривать все заказы, фильтровать их по статусу, изменять статус заказа и удалять заказы. Отображаются подробности заказа, такие как информация о получателе и список заказанных товаров.

2\. Управление пользователями. Администраторы могут просматривать список пользователей с возможностью фильтрации по роли (заказчик или сотрудник). Для каждого пользователя можно просмотреть детальную информацию и при необходимости удалить его.

3\. Детали пользователя user_detail.html - подробная информация о пользователе, включая email, имя, телефон, адрес и дату регистрации. Администраторы могут удалить пользователя через модальное окно с подтверждением.

4\. Общий макет административных страниц admin_layout.html, содержащий общие элементы интерфейса, включая навигацию, стили и поддержку дополнительных скриптов.

**Структура приложения**

**Представления** (views.py)

Управление заказами: Позволяет администраторам просматривать, фильтровать, изменять и удалять заказы.

Управление пользователями: Позволяет администратору управлять пользователями, включая просмотр и удаление.

Детали пользователя: Предоставляет полную информацию о пользователе с возможностью удаления.

**Тесты** (tests.py): Проверка функциональности управления заказами и пользователями, включая тестирование изменения статусов, фильтрации и удаления.

**Маршрутизация** (urls.py). Настроены маршруты для всех административных функций, включая управление заказами и пользователями.

Приложение использует модальные окна и скрипты для подтверждения действий, таких как удаление, и обеспечивает надежное администрирование сайта.

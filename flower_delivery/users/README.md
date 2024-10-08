**Приложение users**

**Описание**

Приложение users отвечает за управление пользователями на сайте и включает в себя функциональность для регистрации, авторизации и управления профилем пользователя.

**Основные функции**

1\. **Регистрация пользователей**. Страница регистрации register.html позволяет новым пользователям создать учетную запись, вводя свои данные (e-mail, пароль и т.д.). Включена валидация данных для обеспечения корректности введенной информации.

2. **Вход пользователей**. На странице авторизации login.html пользователь вводит свой e-mail и пароль для входа в систему. В случае ошибки отображается соответствующее сообщение.

3\. **Управление профилем**. Страница профиля пользователя profile.html, где можно просмотреть и обновить личные данные, такие как телефон и адрес. Все изменения сохраняются с использованием встроенной валидации.

**Структура приложения**

**Модели** (models.py). CustumUser расширяет стандартную модель Django для хранения дополнительной информации о пользователе (телефон, адрес и т.д.).

**Формы** (forms.py). Регистрационная форма создания нового пользователя.

Форма профиля для обновления личных данных пользователя.

**Представления** (views.py):

- Регистрация: Обработка регистрации новых пользователей.
- Авторизация: Обработка входа пользователя.
- Профиль: Отображение и редактирование данных профиля пользователя.

**Маршрутизация** (urls.py)

Настроены маршруты для регистрации, авторизации и профиля.

Тестирование. Файл tests.py проверяет корректность работы ключевых функций. Тестируется:

- форма регистрации: правильно ли работает и успешно сохраняются данные,
- вход в систему с правильными и неправильными данными,
- возможности изменения и сохранения личных данных.

Приложение использует Bootstrap для стилизации форм и страниц.

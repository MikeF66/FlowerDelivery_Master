Проект flower_delivery
Описание проекта
flower_delivery — это сайт для онлайн-доставки цветов, который предоставляет пользователям возможность выбирать и заказывать цветочные композиции с доставкой. Проект включает несколько приложений, каждое из которых отвечает за определенные функции, такие как управление пользователями, каталог товаров, оформление заказов, отзывы, административная панель, аналитика и интеграция с Telegram.

Основные приложения
1. users
Описание: Управление пользователями, включая регистрацию, авторизацию и профили.
Основные функции: Регистрация, вход, редактирование профиля.
2. catalog
Описание: Управление каталогом товаров, доступных для покупки.
Основные функции: Просмотр каталога, детальная информация о товаре, редактирование и добавление товаров (для администраторов).
3. orders
Описание: Обработка заказов, управление корзиной и оформление покупок.
Основные функции: Корзина, оформление заказа, просмотр истории заказов.
4. reviews
Описание: Управление отзывами пользователей о товарах.
Основные функции: Оставление отзывов, просмотр отзывов на товары.
5. admin_panel
Описание: Панель администрирования для управления заказами и пользователями.
Основные функции: Просмотр и управление заказами, управление пользователями.
6. analytics
Описание: Генерация и отображение отчетов о продажах.
Основные функции: Отчеты о продажах за день, месяц, управление сохраненными отчетами.
7. telegram_bot
Описание: Интеграция сайта с Telegram для взаимодействия с пользователями через бота.
Основные функции: Просмотр заказов, оформление заказов, получение информации о товарах.
8. Основное приложение flower_delivery
Описание: Центральное приложение, координирующее работу всех других приложений.
Основные файлы:
settings.py: Основные настройки проекта.
urls.py: Маршрутизация.
asgi.py и wsgi.py: Настройки для сервера приложений.
Установка и запуск
1. Клонирование репозитория
bash
Copy code
git clone https://github.com/yourusername/flower_delivery.git
cd flower_delivery
2. Установка зависимостей
Создайте и активируйте виртуальное окружение, затем установите зависимости:

bash
Copy code
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt
3. Настройка базы данных
Примените миграции для создания таблиц в базе данных:

bash
Copy code
python manage.py migrate
4. Запуск сервера
Для запуска локального сервера используйте:

bash
Copy code
python manage.py runserver
Сайт будет доступен по адресу http://127.0.0.1:8000/.

Дополнительно
Тестирование
Для запуска тестов используйте команду:

bash
Copy code
python manage.py test
Размещение на сервере
Для развертывания проекта в продакшн-среде настройте wsgi.py и используйте соответствующий сервер, например, Gunicorn или uWSGI.

Лицензия
Проект распространяется под [ваша лицензия]. Подробности см. в файле LICENSE.

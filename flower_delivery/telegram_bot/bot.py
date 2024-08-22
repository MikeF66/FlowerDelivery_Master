import os
import logging
import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN, CHAT_ID
from aiogram.types import FSInputFile
from django.utils.timezone import localtime



bot_token = TOKEN
bot = Bot(token=bot_token)
dp = Dispatcher()
chat_id = CHAT_ID

# Инициализация логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_sales_report_via_telegram(filepath, caption):
    try:
        if not os.path.exists(filepath):
            logger.error(f"Файл не найден: {filepath}")
            return

        bot = Bot(token=bot_token)

        # Отправка файла через FSInputFile
        file = FSInputFile(filepath)
        await bot.send_document(chat_id=chat_id, document=file, caption=caption)

        logger.info(f"Отчет отправлен: {os.path.basename(filepath)}")

    except FileNotFoundError:
        logger.error(f"Файл не найден: {filepath}")
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка сети при отправке файла: {e}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка при отправке файла: {e}")

    finally:
        await bot.session.close() # Закрываем сессию бота


async def send_order_notification(order):
    try:
        local_order_date = localtime(order.order_date)
        products_info = ', '.join([f"{item['product_name']}, {item['quantity']} шт." for item in order.products])
        message = (
            f"Новый заказ:\n"
            f"№ - {order.id} от {local_order_date.strftime('%d-%m-%Y %H:%M')}\n"
            f"{products_info}\n"
            f"Общая сумма: {order.total_cost} руб.\n"
            f"Получатель: {order.recipient_name}\n"
            f"Телефон: {order.recipient_phone}\n"
            f"Адрес доставки: {order.delivery_address}"
        )
        await bot.send_message(chat_id=chat_id, text=message)

    except aiohttp.ClientError as e:
        logger.error(f"Ошибка сети при отправке уведомления о заказе: {e}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка при отправке уведомления о заказе: {e}")

    finally:
        await bot.session.close()



def notify_order(order):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(send_order_notification(order))
    except Exception as e:
        logger.error(f"Ошибка при выполнении notify_order: {e}")
    finally:
        loop.close()


async def notify_status_order(order):
    try:
        bot = Bot(token=bot_token)
        message = (
            f"Статус заказа №{order.id} изменился:\n"
            f"Статус: {order.get_status_display()}\n"
            f"Получатель: {order.recipient_name}\n"
            f"Адрес доставки: {order.delivery_address}"
        )
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        logger.error(f"Неожиданная ошибка при отправке уведомления о статусе заказа: {e}")
    finally:
        await bot.session.close()

# Синхронная обертка для асинхронной функции
def sync_notify_status_order(order):
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(notify_status_order(order))
    except Exception as e:
        logger.error(f"Ошибка при выполнении sync_notify_status_order: {e}")
    finally:
        loop.close()



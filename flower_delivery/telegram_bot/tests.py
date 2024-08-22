import pytest
from unittest.mock import patch, AsyncMock
from telegram_bot.bot import send_sales_report_via_telegram, send_order_notification

@pytest.mark.asyncio
async def test_send_sales_report_via_telegram():
    with patch('bot.Bot') as mock_bot:
        mock_bot_instance = mock_bot.return_value
        mock_bot_instance.send_document = AsyncMock()

        await send_sales_report_via_telegram('test_file.xlsx', 'Test Report')

        mock_bot_instance.send_document.assert_called_once_with(
            chat_id='CHAT_ID', document=mock.ANY, caption='Test Report'
        )

@pytest.mark.asyncio
async def test_send_order_notification():
    with patch('bot.Bot') as mock_bot:
        mock_bot_instance = mock_bot.return_value
        mock_bot_instance.send_message = AsyncMock()

        order = AsyncMock()
        order.id = 1
        order.order_date = datetime(2023, 5, 1, 12, 0, 0)
        order.products = [{'product_name': 'Product 1', 'quantity': 2}]
        order.total_cost = 100
        order.recipient_name = 'John Doe'
        order.recipient_phone = '+1234567890'
        order.delivery_address = '123 Main St'

        await send_order_notification(order)

        mock_bot_instance.send_message.assert_called_once_with(
            chat_id='CHAT_ID', text=mock.ANY
        )

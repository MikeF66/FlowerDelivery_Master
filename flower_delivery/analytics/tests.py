from django.test import TestCase
from analytics.models import DailySalesReport
from datetime import date
from decimal import Decimal


class DailySalesReportTestCase(TestCase):
    def setUp(self):
        # Инициализация тестовых данных
        self.report_date = date.today()
        self.order_data = {'order_id': 1, 'total_cost': 100}
        self.expenses = Decimal('50.00')

        self.report = DailySalesReport.objects.create(
            report_date=self.report_date,
            order_data=self.order_data,
            expenses=self.expenses
        )

    def test_report_creation(self):
        # Проверяем, что отчет создается правильно
        self.assertEqual(self.report.report_date, self.report_date)
        self.assertEqual(self.report.order_data, self.order_data)
        self.assertEqual(self.report.expenses, self.expenses)

    def test_report_string_representation(self):
        # Проверяем строковое представление модели
        self.assertEqual(str(self.report), f"Отчёт за {self.report_date}")

    def test_default_expenses(self):
        # Проверяем, что расходы по умолчанию равны 0.00
        report = DailySalesReport.objects.create(
            report_date=self.report_date,
            order_data=self.order_data
        )
        self.assertEqual(report.expenses, Decimal('0.00'))

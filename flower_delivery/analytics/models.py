from django.db import models
from django.core.validators import MinValueValidator

class DailySalesReport(models.Model):
    report_date = models.DateField(auto_now_add=True, verbose_name="Дата отчёта")
    order_data = models.JSONField(verbose_name="Данные заказа")
    expenses = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Расходы",
        default=0.00,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"Отчёт за {self.report_date}"

    class Meta:
        verbose_name = "Ежедневный отчет о продажах"
        verbose_name_plural = "Ежедневные отчеты о продажах"

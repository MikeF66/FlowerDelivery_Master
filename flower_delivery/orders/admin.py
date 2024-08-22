from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'recipient_name', 'status', 'order_date', 'total_cost')
    list_filter = ('status', 'order_date')
    search_fields = ('customer__username', 'recipient_name', 'recipient_phone')
    ordering = ('-order_date',)


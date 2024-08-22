from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from telegram_bot.bot import sync_notify_status_order
from catalog.models import Product
from django.contrib import messages
from users.models import CustomUser
from django.utils.timezone import localtime
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.db import transaction


@staff_member_required
def admin_orders(request):
    try:
        status_filter = request.GET.get('status')
        if status_filter:
            orders = Order.objects.filter(status=status_filter).order_by('-order_date')
        else:
            orders = Order.objects.all().order_by('-order_date')
        for order in orders:
            order.order_date = localtime(order.order_date)

        statuses = Order.STATUS_CHOICES

        return render(request, 'admin_panel/admin_orders.html',
                  {'orders': orders, 'statuses': statuses, 'status_filter': status_filter})
    except Exception as e:
        messages.error(request, f"Произошла ошибка при загрузке заказов: {str(e)}")
        return redirect('analytics:report_dashboard')

@staff_member_required
def update_order_status(request, order_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)

    try:
        with transaction.atomic():
            order = get_object_or_404(Order, id=order_id)
            new_status = request.POST.get('status')
            if new_status in dict(order.STATUS_CHOICES):
                order.status = new_status
                order.save()
                sync_notify_status_order(order)
                messages.success(request, 'Статус заказа успешно обновлен.')
            else:
                messages.error(request, 'Недопустимый статус заказа.')
        return redirect('admin_panel:admin_orders')
    except Exception as e:
        messages.error(request, f"Ошибка при обновлении статуса заказа: {str(e)}")
        return redirect('admin_panel:admin_orders')

@staff_member_required
def delete_order(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)

    order_id = request.GET.get('order_id')
    try:
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        messages.success(request, 'Заказ успешно удален.')
    except Exception as e:
        messages.error(request, f"Ошибка при удалении заказа: {str(e)}")
    return redirect('admin_panel:admin_orders')

@staff_member_required
def admin_users(request):
    try:
        role_filter = request.GET.get('role', 'customer')
        if role_filter == 'staff':
            users = CustomUser.objects.filter(is_staff=True)
        else:
            users = CustomUser.objects.filter(is_staff=False)
        return render(request, 'admin_panel/admin_users.html', {'users': users, 'role_filter': role_filter})
    except Exception as e:
        messages.error(request, f"Ошибка при загрузке списка пользователей: {str(e)}")
        return redirect('admin_panel:admin_dashboard')

@staff_member_required
def user_detail(request, user_id):
    try:
        user = get_object_or_404(CustomUser, id=user_id)
        return render(request, 'admin_panel/user_detail.html', {'user': user})
    except Exception as e:
        messages.error(request, f"Ошибка при загрузке информации о пользователе: {str(e)}")
        return redirect('admin_panel:admin_users')



@staff_member_required
def delete_user(request, user_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)

    try:
        user = get_object_or_404(CustomUser, id=user_id)
        if user.is_superuser:
            raise PermissionDenied("Нельзя удалить суперпользователя")
        user.delete()
        messages.success(request, 'Пользователь успешно удален.')
    except PermissionDenied as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, f"Ошибка при удалении пользователя: {str(e)}")
    return redirect('admin_panel:admin_users')
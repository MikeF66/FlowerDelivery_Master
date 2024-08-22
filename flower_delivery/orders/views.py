from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.utils import timezone
from django.utils.timezone import localtime
from catalog.models import Product
from .models import Cart, CartItem, Order
from .forms import OrderForm
from django.db import DatabaseError, IntegrityError
from django.contrib import messages
from telegram_bot.bot import notify_order


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    page_number = request.GET.get('page', 1)  # Получаем номер страницы из GET-параметра
    context = {
        'cart': cart,
        'page_number': page_number
    }
    return render(request, 'orders/view_cart.html', context)


@login_required
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not item_created:
            cart_item.quantity += 1
        cart_item.save()
    except DatabaseError:
        messages.error(request, "Произошла ошибка при добавлении товара в корзину. Пожалуйста, попробуйте снова.")
        return redirect('catalog:home')

    page_number = request.GET.get('page', 1)  # Получаем номер страницы из GET-параметра
    return redirect(f'{reverse("orders:view_cart")}?page={page_number}')

@login_required
def remove_from_cart(request, item_id):
    try:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        return JsonResponse({'status': 'success'})
    except DatabaseError:
        return JsonResponse({'status': 'error', 'message': 'Ошибка при удалении товара из корзины.'})

@login_required
def update_cart(request):
    page_number = request.GET.get('page', 1)  # Получаем номер страницы из GET-параметра
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
            for item in cart.items.all():
                quantity_key = f'quantity_{item.id}'
                remove_key = f'remove_{item.id}'

                if remove_key in request.POST:
                    item.delete()
                elif quantity_key in request.POST:
                    new_quantity = int(request.POST[quantity_key])
                    if new_quantity > 0:
                        item.quantity = new_quantity
                        item.save()
                    else:
                        item.delete()
        except DatabaseError:
            messages.error(request, "Произошла ошибка при обновлении корзины. Пожалуйста, попробуйте снова.")

    return redirect(f'{reverse("orders:view_cart")}?page={page_number}')

@login_required
def update_cart_item(request, item_id, action):
    try:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()

        response_data = {
            'status': 'success',
            'quantity': cart_item.quantity,
            'total_price': cart_item.quantity * cart_item.product.price
        }
        return JsonResponse(response_data)
    except CartItem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Товар не найден в корзине.'}, status=404)
    except IntegrityError:
        return JsonResponse({'status': 'error', 'message': 'Ошибка целостности данных. Пожалуйста, попробуйте позже.'},
                            status=400)
    except DatabaseError:
        return JsonResponse({'status': 'error', 'message': 'Ошибка базы данных. Пожалуйста, попробуйте позже.'},
                            status=500)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Произошла непредвиденная ошибка: {str(e)}'}, status=500)


def is_late_order():
    current_time_utc = timezone.now()  # Время в UTC
    current_time = localtime(current_time_utc)
    print(current_time)
    return current_time.hour > 19 or (current_time.hour == 19 and current_time.minute > 0)

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.warning(request, "Ваша корзина пуста. Добавьте товары перед оформлением заказа.")
        return redirect('orders:view_cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                order = form.save(commit=False)
                order.customer = request.user
                order.status = 'new'
                order.order_date = timezone.now()   # order.order_date = datetime.now(moscow_tz)
                products = []
                total_cost = 0
                for item in cart.items.all():
                    product_info = {
                        "product_id": item.product.id,
                        "product_name": item.product.name,
                        "quantity": item.quantity,
                        "price": item.product.price,
                        "total_price": item.get_total_price()
                    }
                    products.append(product_info)
                    total_cost += item.get_total_price()

                order.products = products
                order.total_cost = total_cost
                order.save()
                # Отправка уведомления в Telegram
                notify_order(order)
                cart.items.all().delete()
                return redirect('orders:order_success', order_id=order.id)

            except IntegrityError:
                messages.error(request, "Ошибка базы данных при сохранении заказа.")
            except Exception as e:
                messages.error(request, f"Произошла ошибка: {str(e)}")

        else:
            messages.error(request, "Форма заполнена неверно. Пожалуйста, исправьте ошибки.")

    else:
        initial_data = {
            'delivery_address': request.user.address,
        }
        form = OrderForm(initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
        'is_late_order': is_late_order(),
    }

    return render(request, 'orders/checkout.html', context)

@login_required
def order_success(request, order_id):
    order = Order.objects.get(id=order_id)

    context = {
        'order': order,
        'is_late_order': is_late_order(),
    }
    return render(request, 'orders/order_success.html', context)

@login_required
def user_orders(request):
    try:
        orders = Order.objects.filter(customer=request.user).order_by('-order_date')
    except DatabaseError:
        # Добавляем сообщение об ошибке, которое будет отображено в шаблоне
        messages.error(request, "Произошла ошибка при загрузке ваших заказов. Пожалуйста, попробуйте позже.")
        orders = []  # В случае ошибки возвращаем пустой список заказов
    return render(request, 'orders/user_orders.html', {'orders': orders})


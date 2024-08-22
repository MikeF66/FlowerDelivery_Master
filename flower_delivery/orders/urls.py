from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_item/<int:item_id>/<str:action>/', views.update_cart, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),  # добавили параметр order_id
    path('my-orders/', views.user_orders, name='user_orders'),
 ]

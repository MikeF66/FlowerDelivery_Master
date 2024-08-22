from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('orders/', views.admin_orders, name='admin_orders'),
    path('admin/order/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('delete-order/', views.delete_order, name='delete_order'),
    path('users/', views.admin_users, name='admin_users'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]
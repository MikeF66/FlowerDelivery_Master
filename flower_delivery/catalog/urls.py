from django.urls import path
from . import views
from .views import delete_product
from reviews.views import product_reviews

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product/<int:pk>/delete/', delete_product, name='delete_product'),
    path('product/<int:product_id>/reviews/', product_reviews, name='product_reviews'),
    path('search/', views.product_search, name='product_search'),
]
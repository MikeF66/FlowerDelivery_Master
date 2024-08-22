from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('product/<int:product_id>/reviews/', views.product_reviews, name='product_reviews'),
    path('leave_review/<int:order_id>/<int:product_id>/', views.leave_review, name='leave_review'),
]
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('analytics/daily-sales-report/', views.daily_sales_report, name='daily_sales_report'),
    path('analytics/monthly_sales_report/', views.monthly_sales_report, name='monthly_sales_report'),
    path('dashboard/', views.report_dashboard, name='report_dashboard'),
    path('reports/', views.report_files_list, name='report_files_list'),
    path('reports/download/<str:file_name>/', views.download_report, name='download_report'),
    path('reports/delete/<str:file_name>/', views.delete_report, name='delete_report'),
]


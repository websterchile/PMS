from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sensors/', views.sensors, name='sensors'),
    path('sensors/<str:sensor_type>/', views.sensor_detail, name='sensor_detail'),
    path('predictions/', views.predictions, name='predictions'),
    path('maintenance/', views.maintenance, name='maintenance'),
    path('logs/', views.logs, name='logs'),
    path('logs/add/', views.add_log, name='add_log'),
    path('logs/edit/<int:log_id>/', views.edit_log, name='edit_log'),
    path('logs/delete/<int:log_id>/', views.delete_log, name='delete_log'),
    path('data-management/', views.data_management, name='data_management'),
    path('help/', views.help_page, name='help'),
]
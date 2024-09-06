from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Добавьте маршрут для корневого URL
    path('muss/templates/upload/', views.upload_pdf, name='upload_pdf'),
    path('muss/templates/register/', views.register, name='register'),
    path('muss/templates/profile/', views.profile, name='profile'),
    path('muss/templates/history/', views.history, name='history'),
    path('history/<int:history_id>/', views.history_detail, name='history_detail'),
]

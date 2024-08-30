# muss/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),
    path('history/<int:history_id>/', views.history_detail, name='history_detail'),
]

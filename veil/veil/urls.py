from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from muss import views  # Не забудьте добавить импорт views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('muss.urls')),  # Перенаправляем запросы к корневому URL на muss.urls

    # Путь для страницы входа
    path('login/', auth_views.LoginView.as_view(), name='login'),

    # Остальные URL маршруты для приложения muss
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),
    path('history/<int:history_id>/', views.history_detail, name='history_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

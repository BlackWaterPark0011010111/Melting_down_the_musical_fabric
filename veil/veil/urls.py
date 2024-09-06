from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from muss.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('', include('muss.urls')),  # Включение маршрутов из muss.urls
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

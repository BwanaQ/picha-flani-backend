# Version: 1.0
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path('admin/', admin.site.urls),
    path('home/', include('photos.urls')),
    path('payments/', include('payments.urls', namespace='payments')),
    path("", include("users.urls", namespace="users")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


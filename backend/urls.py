from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


from backend.itrabaho.urls import urlpatterns as ITRABAHO_URLS

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include([ITRABAHO_URLS]),
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

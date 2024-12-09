
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

app_name = 'core'
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("data.urls"), name="data"),
    path("api/", include("comments.urls"), name="comments"),
    path("api/auth/", include("authentication.urls"), name="authentication"),
    path("api/payment/", include("payment.urls"), name="payment"),
    path("api/", include("settings.urls"), name="settings"),

    # DEBUG

    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

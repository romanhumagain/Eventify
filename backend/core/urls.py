from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("authentication.urls")),
    path("api/events/", include("events.urls")),
    path("api/notifications/", include("notification.urls")),
    path("api/feedback/", include("feedback.urls")),
    path("api/tickets/", include("tickets.urls")),
    path("api/rsvps/", include("rsvp.urls")),
    path("api/payments/", include("payments.urls")),
    
    # JWT Token
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

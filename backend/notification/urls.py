from django.urls import path, include
from rest_framework import routers
from .views import NotificationViewSet, MarkAllAsReadView, MarkAsReadView

router = routers.DefaultRouter()
router.register(r'', NotificationViewSet)

urlpatterns = [
    path('mark-all-as-read/', MarkAllAsReadView.as_view(), name='markallread'),
    path('mark-as-read/<int:id>/', MarkAsReadView.as_view({'put': 'update'}), name='mark-as-read'),
]

urlpatterns += router.urls

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RSVPViewSet

router = DefaultRouter()
router.register(r'', RSVPViewSet, basename='rsvp')

urlpatterns = [
    path('', include(router.urls)), 
]

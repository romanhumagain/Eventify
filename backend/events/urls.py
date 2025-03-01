from django.urls import path
from rest_framework import routers
from .views import EventCategoryViewSet, EventListCreateAPIView, EventRetrieveUpdateDestroyView

router = routers.DefaultRouter()
router.register(r'event-categories', EventCategoryViewSet)


urlpatterns = [
    path('events/', EventListCreateAPIView.as_view(), name='event-list'),
    path('events/<int:id>/', EventRetrieveUpdateDestroyView.as_view(), name='event-retrieve-update-destroy'),
]

urlpatterns += router.urls
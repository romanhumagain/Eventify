from django.urls import path
from rest_framework import routers
from .views import EventCategoryViewSet, EventListCreateAPIView, EventRetrieveUpdateDestroyView, MyEventListAPIView, SavedEventListAPIView, SavedEventToggleAPIView

router = routers.DefaultRouter()
router.register(r'event-categories', EventCategoryViewSet)


urlpatterns = [
    path('', EventListCreateAPIView.as_view(), name='event-list'),
    path('<int:id>/', EventRetrieveUpdateDestroyView.as_view(), name='event-retrieve-update-destroy'),
    path('my-events/', MyEventListAPIView.as_view(), name='my-events'),
    
    path('saved/', SavedEventListAPIView.as_view(), name='saved-events-list'),
    path('saved/<int:event_id>/', SavedEventToggleAPIView.as_view(), name='toggle-save-event'),
]

urlpatterns += router.urls
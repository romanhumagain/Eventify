from django.urls import path
from rest_framework import routers
from .views import (EventCategoryViewSet, 
                    EventListCreateAPIView, 
                    EventRetrieveUpdateDestroyView, 
                    MyEventListAPIView, 
                    SavedEventListAPIView, 
                    SavedEventToggleAPIView, 
                    MyBookingAPIView, 
                    EventInvitationAPIView
)
router = routers.DefaultRouter()
router.register(r'categories', EventCategoryViewSet)


urlpatterns = [
    path('', EventListCreateAPIView.as_view(), name='event-list'),
    path('<int:id>/', EventRetrieveUpdateDestroyView.as_view(), name='event-retrieve-update-destroy'),
    path('my-events/', MyEventListAPIView.as_view(), name='my-events'),
    path('my-bookings/',MyBookingAPIView.as_view(), name ="my-bookings"),
    
    path('saved/', SavedEventListAPIView.as_view(), name='saved-events-list'),
    path('toggle-save/<int:event_id>/', SavedEventToggleAPIView.as_view(), name='toggle-save-event'),
    path('send-invitation/', EventInvitationAPIView.as_view(), name='send_invitation')
]

urlpatterns += router.urls
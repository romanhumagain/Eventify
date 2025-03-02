from django.urls import path
from .views import FeedbackListCreateAPIView, FeedbackRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('event/<int:event_id>/', FeedbackListCreateAPIView.as_view(), name='feedback-list-create'),
    path('<int:pk>/', FeedbackRetrieveUpdateDestroyAPIView.as_view(), name='feedback-retrieve-update-destroy'),
]

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Feedback
from .serializers import FeedbackSerializer
from events.models import Event
from authentication.models import User
from rest_framework.response import Response
from rest_framework import status

class FeedbackListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the event ID from URL parameter
        event_id = self.kwargs['event_id']
        event = Event.objects.get(id=event_id, is_approved = True)
        
        # Return all feedbacks for this event
        return Feedback.objects.filter(event=event).order_by('-created_at')

    def perform_create(self, serializer):
        # Get the event ID from URL parameter
        event_id = self.kwargs['event_id']
        event = Event.objects.get(id=event_id, is_approved = True)
        
        if event.organizer == self.request.user:
            raise PermissionDenied("You cannot add feedback to your own event.")
        
        # Associate the feedback with the event and the current user
        serializer.save(user=self.request.user, event=event)
        

class FeedbackRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        feedback = self.get_object()
        if feedback.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this feedback.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        feedback = self.get_object()
        if feedback.user != request.user:
            raise PermissionDenied("You do not have permission to delete this feedback.")

        self.perform_destroy(feedback)
        return Response(
            {"detail": "Feedback deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
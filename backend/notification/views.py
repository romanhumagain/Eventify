from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by("-created_at")

class MarkAsReadView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        notification = Notification.objects.filter(user=request.user, id=kwargs['id']).first()
        if notification:
            notification.is_read = True
            notification.save()
            return Response({"detail": "Notification marked as read."}, status=status.HTTP_200_OK)
        return Response({"detail": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)
     
class MarkAllAsReadView(APIView):
    permission_classes = [IsAuthenticated]
  
    def put(self, request):
        # Mark all unread notifications for the current user as read
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        print(f"Found {notifications.count()} unread notifications.")

        notifications.update(is_read=True)
        print("All notifications marked as read.")
        
        return Response({"detail": "All notifications marked as read."}, status=status.HTTP_200_OK)

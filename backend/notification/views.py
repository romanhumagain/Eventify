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
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        is_read = self.request.query_params.get('is_read', None)
        
        if is_read is not None:
            # Only filter by 'is_read' if it's explicitly provided as 'true' or 'false'
            if is_read.lower() == 'true':
                queryset = queryset.filter(is_read=True)
            elif is_read.lower() == 'false':
                queryset = queryset.filter(is_read=False)
        
        # Order by created_at in descending order
        return queryset.order_by("-created_at")
    
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
        notifications.update(is_read=True)
        return Response({"detail": "All notifications marked as read."}, status=status.HTTP_200_OK)

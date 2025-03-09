from .models import Notification
from rest_framework import serializers
from events.models import Event

class NotificationEventSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['banner', 'title']
        
class NotificationSerializer(serializers.ModelSerializer):
    event_details = NotificationEventSerialzer(source = 'event', read_only = True)
    
    class Meta:
        model = Notification
        fields = ['id', 'event', 'message', 'is_read', 'created_at', 'event_details']
        read_only_fields = ['id', 'created_at']
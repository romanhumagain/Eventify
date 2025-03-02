from rest_framework import serializers
from .models import Event, EventCategory, SavedEvent
from authentication.models import User
from django.utils import timezone


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = "__all__"
        
class OrganizerSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'profile_picture','username' ]
  
        
class EventSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField(read_only=True)
    organizer = OrganizerSerializer(read_only=True)

    is_upcoming = serializers.SerializerMethodField(read_only=True)
    is_active = serializers.SerializerMethodField(read_only=True)
    is_expired = serializers.SerializerMethodField(read_only=True)

    tickets_sold = serializers.IntegerField(read_only=True)
    tickets_available = serializers.IntegerField( read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'banner', 'title', 'subtitle', 'description', 'event_type', 'is_free', 'price',
            'start_date', 'end_date', 'booking_deadline', 'location', 'online_link', 
            'category', 'category_name', 'total_tickets', 'tickets_sold', 'tickets_available',
            'created_at', 'updated_at', 'organizer', 'is_upcoming', 'is_active', 'is_expired',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'organizer', 'category_name', 'tickets_sold', 'tickets_available']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_is_upcoming(self, obj):
        now = timezone.now()
        start_date = timezone.make_aware(obj.start_date) if obj.start_date.tzinfo is None else obj.start_date
        return start_date > now

    def get_is_active(self, obj):
        now = timezone.now() 
        start_date = timezone.make_aware(obj.start_date) if obj.start_date.tzinfo is None else obj.start_date
        end_date = timezone.make_aware(obj.end_date) if obj.end_date.tzinfo is None else obj.end_date
        return start_date <= now <= end_date

    def get_is_expired(self, obj):
        now = timezone.now() 
        end_date = timezone.make_aware(obj.end_date) if obj.end_date.tzinfo is None else obj.end_date
        return end_date < now
      
      
      
class SavedEventSerializer(serializers.ModelSerializer):
    event_details = EventSerializer(source = 'event', read_only=True)
    class Meta:
        model = SavedEvent
        fields = ['id', 'event', 'saved_at', 'event_details']
        read_only_fields = ['id', 'saved_at']
        
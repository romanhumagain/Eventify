from rest_framework import serializers
from .models import Event, EventCategory, SavedEvent
from authentication.models import User
from django.utils import timezone
from tickets.models import TicketQR


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = "__all__"
        
class OrganizerSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'profile_picture', 'username' ]
  
        
class EventSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(read_only=True)
    category_details = EventCategorySerializer(read_only = True, source = 'category')

    is_upcoming = serializers.SerializerMethodField(read_only=True)
    is_active = serializers.SerializerMethodField(read_only=True)
    is_expired = serializers.SerializerMethodField(read_only=True)
    tickets_available = serializers.IntegerField( read_only=True)
    
    attendees = serializers.SerializerMethodField(read_only = True)
    is_saved = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'banner', 'title', 'subtitle', 'details', 'event_type', 'is_free', 'ticket_price',
            'start_date', 'end_date', 'booking_deadline', 'venue', 
            'category','category_details', 'total_tickets', 'tickets_available',
            'created_at', 'updated_at', 'organizer', 'is_upcoming', 'is_active', 'is_expired','attendees','is_saved'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'organizer', 'tickets_available', 'category_details']
        extra_kwargs = {
            'category': {'write_only': True}  
        }
        
    # custom function to validate fields
    def validate_fields(self, validated_data):
        errors = {}

        if 'category' not in validated_data:
            errors["detail"] = "Event category is required."
            
        elif validated_data["start_date"] >= validated_data["end_date"]:
            errors["detail"] = "End date must be after the start date."

        elif validated_data.get("booking_deadline") and validated_data["booking_deadline"] >= validated_data["end_date"]:
            errors["detail"] = "Booking deadline must be before the event end date."

        if errors:
            raise serializers.ValidationError(errors)

    def create(self, validated_data):
        self.validate_fields(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        errors = {}
        
        if validated_data["start_date"] >= validated_data["end_date"]:
            errors["detail"] = "End date must be after the start date."

        elif validated_data.get("booking_deadline") and validated_data["booking_deadline"] >= validated_data["end_date"]:
            errors["detail"] = "Booking deadline must be before the event end date."

        if errors:
            raise serializers.ValidationError(errors)
        return super().update(instance, validated_data)
    
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
    
    def get_is_saved(self, obj):
        request = self.context.get('request', None)  # Get request safely
        if request and request.user and request.user.is_authenticated:
            return SavedEvent.objects.filter(event=obj, user=request.user).exists()
        return False
    
    def get_attendees(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user == obj.organizer:
            return [{"test_attendee": "test_attendee_detail"}]  
        return []


class EventDetailsForSavedEventSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(read_only=True)
    category_details = EventCategorySerializer(read_only = True, source = 'category')

    is_upcoming = serializers.SerializerMethodField(read_only=True)
    is_active = serializers.SerializerMethodField(read_only=True)
    is_expired = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'banner', 'title', 'subtitle', 'details', 'event_type', 'is_free', 'ticket_price',
            'start_date', 'end_date', 'booking_deadline', 'venue', 
            'category_details', 'organizer', 'is_upcoming', 'is_active', 'is_expired'
        ]

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
    event_details = EventDetailsForSavedEventSerializer(source = 'event', read_only=True)
    class Meta:
        model = SavedEvent
        fields = ['id', 'event', 'saved_at', 'event_details']
        read_only_fields = ['id', 'saved_at']
        extra_kwargs = {
            'event':{'write_only':True}
        }
        
    
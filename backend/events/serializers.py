from rest_framework import serializers
from .models import Event, EventCategory, SavedEvent
from authentication.models import User
from django.utils import timezone
from tickets.models import BookedTicket, Ticket
from feedback.models import Feedback
from django.db import models 


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = "__all__"
        
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'profile_picture', 'username' ]
  
        
class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    category_details = EventCategorySerializer(read_only = True, source = 'category')

    is_upcoming = serializers.SerializerMethodField(read_only=True)
    is_active = serializers.SerializerMethodField(read_only=True)
    is_expired = serializers.SerializerMethodField(read_only=True)
    tickets_available = serializers.IntegerField( read_only=True)
    
    attendees_count = serializers.SerializerMethodField(read_only = True)
    is_saved = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'banner', 'title', 'subtitle', 'details', 'event_type', 'is_free', 'ticket_price',
            'start_date', 'end_date', 'booking_deadline', 'venue', 
            'category','category_details', 'total_tickets', 'tickets_available',
            'created_at', 'updated_at', 'organizer', 'is_upcoming', 'is_active', 'is_expired','attendees_count','is_saved'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'organizer', 'tickets_available', 'category_details']
        extra_kwargs = {
            'category': {'write_only': True},   
            'total_tickets': {'write_only': True},   
            'details':{'write_only': True}
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
    
    def get_attendees_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user == obj.organizer:
            # Get all paid tickets for this event
            paid_tickets = Ticket.objects.filter(
                event=obj,
                status='paid'
            ).select_related('user')

            # Calculate total attendees count (sum of ticket quantities)
            attendees_count = paid_tickets.aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
            return attendees_count
        return 0

# Serializer for the event feedback serializer
class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = Feedback
        fields = ['id', 'message', 'created_at', 'user']
        read_only_fields = ['id', 'user']
    
class EventDetailsSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    category_details = EventCategorySerializer(read_only = True, source = 'category')
    is_upcoming = serializers.SerializerMethodField(read_only=True)
    is_active = serializers.SerializerMethodField(read_only=True)
    is_expired = serializers.SerializerMethodField(read_only=True)
    tickets_available = serializers.IntegerField( read_only=True)
    attendees = serializers.SerializerMethodField(read_only = True)
    feedbacks = serializers.SerializerMethodField(read_only = True)
    is_saved = serializers.SerializerMethodField(read_only = True)
    
    bookings = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Event
        fields = [
            'id', 'banner', 'title', 'subtitle', 'details', 'event_type', 'is_free', 'ticket_price',
            'start_date', 'end_date', 'booking_deadline', 'venue', 
            'category_details', 'total_tickets', 'tickets_available',
            'created_at', 'updated_at', 'organizer', 'is_upcoming', 'is_active', 'is_expired','attendees','is_saved', 'feedbacks', 'bookings'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'organizer', 'tickets_available', 'category_details']
        extra_kwargs = {
            'category': {'write_only': True}  
        }
        
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
            # Get all paid tickets for this event
            paid_tickets = Ticket.objects.filter(
                event=obj,
                status='paid'
            ).select_related('user')

            # Calculate total attendees count (sum of ticket quantities)
            attendees_count = paid_tickets.aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
            
            # Get all booked tickets with check-in information
            booked_tickets_map = {
                bt.ticket_id: bt.is_checked_in
                for bt in BookedTicket.objects.filter(
                    ticket__event=obj,
                    ticket__status='paid'
                )
            }
            
            # Build the attendees detail list
            attendees_detail = []
            for ticket in paid_tickets:
                attendees_detail.append({
                    'user_id': ticket.user.id,
                    'username': ticket.user.username,
                    'ticket_count': ticket.quantity,
                    'is_checked_in': booked_tickets_map.get(ticket.id, False)
                })
            
            # Return the data in the requested format
            return {
                'attendees_count': attendees_count,
                'attendees_detail': attendees_detail
            }

        return {
            'attendees_count': 0,
            'attendees_detail': []
        }

    
    def get_feedbacks(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user == obj.organizer:
            feedbacks = obj.feedbacks.all()  
            return FeedbackSerializer(feedbacks, many=True).data 
        return []
    
    def get_bookings(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            bookedTickets = []
            bookedTicketsInst = BookedTicket.objects.filter(ticket__user=request.user, ticket__event=obj, ticket__status="paid").order_by('-ticket__purchase_date')
            for booking in bookedTicketsInst:
                ticket = booking.ticket
                
                booking_details = {
                    'booking_id': booking.id,
                    'qr_code_data':booking.qr_code_data,
                    'booked_at':ticket.purchase_date,
                    'is_checked_in':booking.is_checked_in
                }
                bookedTickets.append(booking_details)
            return bookedTickets
        return []
        
        
class SavedEventSerializer(serializers.ModelSerializer):
    event_details = EventSerializer(source = 'event', read_only=True)
    class Meta:
        model = SavedEvent
        fields = ['id', 'event', 'saved_at', 'event_details']
        read_only_fields = ['id', 'saved_at']
        extra_kwargs = {
            'event':{'write_only':True}
        }
        
    
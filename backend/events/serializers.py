from rest_framework import serializers
from .models import Event, EventCategory
from authentication.models import User


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
  class Meta:
      model = Event
      fields = ['id','banner', 'title', 'subtitle', 'description', 'is_online', 'start_date', 'end_date', 'location', 'is_approved', 'price', 'created_at', 'updated_at', 'organizer', 'category_name']
      read_only_fields = ['id', 'is_approved', 'created_at', 'updated_at', 'organizer', 'category_name']
        
  def get_category_name(self, obj):
    return EventCategory.objects.get(id=obj.category.id).name
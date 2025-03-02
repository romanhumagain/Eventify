from rest_framework import serializers
from .models import Feedback
from authentication.models import User
from events.models import Event


class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_picture', 'username']
        
class FeedbackSerializer(serializers.ModelSerializer):
    user_details = UserFeedbackSerializer(source='user', read_only=True)
    class Meta:
        model = Feedback
        fields = ['id', 'event', 'user', 'rating', 'comment', 'created_at', 'user_details']
        read_only_fields = ['id', 'created_at', 'user_details','event', 'user']
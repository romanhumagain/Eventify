from rest_framework import serializers
from .models import Feedback
from authentication.models import User


class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','profile_picture', 'username']
        
class FeedbackSerializer(serializers.ModelSerializer):
    user = UserFeedbackSerializer(read_only=True)
    class Meta:
        model = Feedback
        fields = ['id', 'event', 'user', 'message', 'created_at']
        read_only_fields = ['id', 'created_at', 'user_details', 'event', 'user']
        
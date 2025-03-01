from django.db import models
from events.models import Event
from authentication.models import User

class Feedback(models.Model):
    rating_choices = [(1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="feedbacks")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks")
    rating = models.PositiveIntegerField(choices=rating_choices)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback for {self.event.title} by {self.user.username}"
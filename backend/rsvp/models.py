from django.db import models
from authentication.models import User
from events.models import Event


class RSVP(models.Model):
    RSVP_STATUS_CHOICES = [
        ("interested", "Interested"),
        ("going", "Going"),
        ("not_interested", "Not Interested"),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="rsvps")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rsvps")
    status = models.CharField(max_length=20, choices=RSVP_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        unique_together = ("user", "event")
        verbose_name = "RSVP"
        verbose_name_plural = "RSVPs"
        
    def __str__(self):
        return f"{self.user.username} RSVP for {self.event.title}: {self.status}"
        

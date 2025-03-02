from django.db import models
from authentication.models import User
from events.models import Event


class RSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="rsvps")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rsvps")
    status = models.CharField(
        max_length=20,
        choices=[
            ("Confirmed", "Confirmed"),
            ("Pending", "Pending"),
            ("Declined", "Declined"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")

    def __str__(self):
        return f"{self.user.first_name} RSVP for {self.event.title}: {self.status}"

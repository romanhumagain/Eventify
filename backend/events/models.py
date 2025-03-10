from django.db import models
from authentication.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db.models import Sum


class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Event Category"
        verbose_name_plural = "Event Categories"

    def __str__(self):
        return self.name
      
class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ("physical", "Physical"),
        ("remote", "Remote"),
    ]

    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="events")

    banner = models.ImageField(upload_to="events-banner/")
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    details = models.TextField(null=True, blank=True)

    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    venue = models.CharField(max_length=255, blank=True, null=True)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    booking_deadline = models.DateTimeField(null=True, blank=True)

    total_tickets = models.PositiveIntegerField()
    is_free = models.BooleanField(default=False)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organizer", "title", "start_date", "event_type" ],
                name="unique_event_per_organizer",
            )
        ]
          
    def save(self, *args, **kwargs):
        if self.pk:
            original = Event.objects.get(pk=self.pk)
            self._original_is_approved = original.is_approved
        else:
            self._original_is_approved = self.is_approved
            
        self.is_free = not self.ticket_price or self.ticket_price == 0

        if not self.booking_deadline:
            self.booking_deadline = self.end_date
            
        super(Event, self).save(*args, **kwargs)

    @property
    def tickets_sold(self):
        # Sum the quantity of "Paid" tickets
        sold_tickets = self.tickets.filter(status='paid').aggregate(total_sold=Sum('quantity'))['total_sold'] or 0
        return sold_tickets

    @property
    def tickets_available(self):
        available_tickets = self.total_tickets - self.tickets_sold
        return available_tickets

    def __str__(self):
        return f"{self.title} organized by {self.organizer.username}"




class SavedEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_events")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="saved_events")
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "event"]

    def __str__(self):
        return f"{self.user.username} saved {self.event.title}"

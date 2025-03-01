from django.db import models
from authentication.models import User
from django.core.exceptions import ValidationError
from datetime import datetime

class EventCategory(models.Model):
  name = models.CharField(max_length=200)
  descritpion = models.TextField(null=True, blank=True)

  class Meta:
    verbose_name = "Event Category"
    verbose_name_plural = "Event Categories"
    
  def __str__(self):
      return self.name
      
class Event(models.Model):
  organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
  category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name="events")
  banner = models.ImageField(upload_to="events/", null=True, blank=True)
  title = models.CharField(max_length=100)
  subtitle = models.CharField(max_length=100)
  description = models.TextField()
  location = models.CharField(max_length=255, blank=True, null=True)
  is_online = models.BooleanField(default=False)
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
  is_approved = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  # to check if the event is active or not
  @property
  def is_active(self):
      now = datetime.now()
      return self.start_date <= now <= self.end_date

  # Check if the event is upcoming 
  @property
  def is_upcoming(self):
      now = datetime.now()
      return self.start_date > now
  
  def clean(self):
    if self.start_date >= self.end_date:
      raise ValidationError("End date must be after the start date.")
    
  def save(self, *args, **kwargs):
        if self.pk: 
            original = Event.objects.get(pk=self.pk)
            self._original_is_approved = original.is_approved
        else:
            self._original_is_approved = self.is_approved
        super(Event, self).save(*args, **kwargs)
  
  def __str__(self):
      return f"{self.title} organized by {self.organizer.first_name} {self.organizer.last_name}"
    
  
class SavedEvent(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_events")
  event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="saved_events")
  saved_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    unique_together = ['user', 'event']
    
  def __str__(self):
      return f"{self.user.username} saved {self.event.title}"
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RSVP
from utils.send_email import send_event_reminder_mail

# Send email after user confirms the RSVP
@receiver(post_save, sender = RSVP)
def send_event_reminder(sender, instance, created, **kwargs):
      send_event_reminder_mail(instance.user.email, instance.user.username,  instance.event, instance.status)
      



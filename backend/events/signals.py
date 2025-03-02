from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event
from utils.send_email import send_event_approval_mail
from notification.models import Notification

@receiver(post_save, sender=Event)
def event_approved(sender, instance, created, **kwargs):
    if not created:  # Only trigger if the event is being updated, not created
        # Check if the `is_approved` field was previously False and is now True
        if instance.is_approved and hasattr(instance, '_original_is_approved'):
            if instance._original_is_approved is False:
                # Send notification to Organizer for event approval
                notification = Notification.objects.create(
                    user=instance.organizer,
                    message=f"Your event {instance.title} has been approved."
                )
                notification.save()
                # Send email to Organizer for event approval
                # send_event_approval_mail(instance.title, instance.organizer)

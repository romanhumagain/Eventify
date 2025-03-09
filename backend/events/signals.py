from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event
from utils.send_email import send_event_approval_mail, send_event_update_email
from notification.models import Notification


@receiver(post_save, sender=Event)
def event_approved(sender, instance, created, **kwargs):
    if not created:  # Only trigger if the event is being updated, not created
        
        # Check if the `is_approved` field was previously False and is now True
        if instance.is_approved and hasattr(instance, '_original_is_approved') and instance._original_is_approved is False:
            # Send notification to Organizer for event approval
            notification = Notification.objects.create(
                user=instance.organizer,
                event=instance,
                message=f"Your event {instance.title} has been approved."
            )
            notification.save()
            # Send email to Organizer for event approval
            send_event_approval_mail(instance.title, instance.organizer)
            
        else:
            # send mail for the event updates except sending after is_approved status updated
            tickets_with_qr = instance.tickets.select_related('user').filter(
                booked_ticket_qr__isnull=False  # Only tickets that have QR codes
            )

            # Track unique users to avoid duplicate emails
            notified_users = set()

            for ticket in tickets_with_qr:
                if ticket.user.id not in notified_users:
                    
                    notification = Notification.objects.create(
                        user=ticket.user,
                        event=instance,
                        message=f"The event {instance.title} has been updated. Please take a moment to review the changes."
                    )
                    notification.save()
                    
                    send_event_update_email(ticket.user, instance)
                    
                    notified_users.add(ticket.user.id)
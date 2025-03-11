from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event
from utils.send_email import send_event_approval_mail, send_event_update_email
from notification.models import Notification
import threading

def send_event_update_notifications(instance, users):
    # Function to send email & notification asynchronously 
    notified_users = set()
    
    
    for ticket in users:
        if ticket.user.id not in notified_users:
            # Create a notification
            Notification.objects.create(
                user=ticket.user,
                event=instance,
                message=f"The event {instance.title} has been updated. Please review the changes."
            )
             
             # Send email
            send_event_update_email(ticket.user, instance)
            notified_users.add(ticket.user.id)
             

@receiver(post_save, sender=Event)
def event_approved(sender, instance, created, **kwargs):
    if not created:  # Only trigger if the event is being updated, not created
        
        # Check if the `is_approved` field was previously False and is now True
        if instance.is_approved and hasattr(instance, '_original_is_approved') and instance._original_is_approved is False:
            # Send notification to Organizer for event approval
            Notification.objects.create(
                user=instance.organizer,
                event=instance,
                message=f"Your event {instance.title} has been approved."
            )
            
            # Run the approval email in a separate thread
            approval_email_thread = threading.Thread(target=send_event_approval_mail, args=(instance.title, instance.organizer))
            approval_email_thread.start()
            
        else:
            # Send mail for the event updates except sending after is_approved status updated
            tickets_with_qr = instance.tickets.select_related('user').filter(booked_ticket_qr__isnull=False)
            # Run the email sending in a separate thread
            email_thread = threading.Thread(target=send_event_update_notifications, args=(instance, tickets_with_qr))
            email_thread.start()

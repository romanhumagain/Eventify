import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BookedTicket
from notification.models import Notification
from utils.send_email import send_checked_in_email

def send_checked_in_email_async(instance):
    send_checked_in_email(instance)

# to notify after checked-in 
@receiver(post_save, sender=BookedTicket)
def ticket_purchased_qr(sender, instance, created, **kwargs):
    if not created and instance.is_checked_in:
        Notification.objects.create(
            user=instance.ticket.user,
            event=instance.ticket.event,
            message=f"Your ticket has been successfully checked in for {instance.ticket.event.title}."
        )
        # Send the checked-in email asynchronously
        email_thread = threading.Thread(target=send_checked_in_email_async, args=(instance,))
        email_thread.start()

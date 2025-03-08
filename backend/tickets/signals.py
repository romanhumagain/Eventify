
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TicketQR
from io import BytesIO
from django.core.files.storage import default_storage
from notification.models import Notification
from utils.send_email import send_checked_in_email

@receiver(post_save, sender=TicketQR)
def ticket_purchased_qr(sender, instance, created, **kwargs):
    if not created and instance.is_checked_in:
        Notification.objects.create(
            user=instance.ticket.user,
            event=instance.ticket.event,
            message=f"Your ticket has been successfully checked in for {instance.ticket.event.title}."
        )
        
    # send mail after successfull checked in 
    send_checked_in_email(instance)
    
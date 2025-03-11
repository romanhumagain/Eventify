import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from utils.send_email import send_welcome_email

def send_welcome_email_async(email, username):
    """Helper function to send the welcome email in a separate thread."""
    send_welcome_email(email, username)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Run the email sending in a separate thread
        email_thread = threading.Thread(target=send_welcome_email_async, args=(instance.email, instance.username))
        email_thread.start()

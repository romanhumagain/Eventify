from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
      # For handling email sending after user registration (optional)
      subject = "Welcome to Eventify!"
      message = "Thank you for registering with Eventify. We hope you enjoy our platform."
      
      send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [instance.email],
        fail_silently=False
        )
      
       

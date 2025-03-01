from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.core.mail import send_mail
from django.conf import settings
from utils.send_email import send_welcome_email

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
      send_welcome_email(instance.email, instance.first_name)
       

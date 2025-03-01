from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# for sending event approval mail
def send_event_approval_mail(event_title, organizer):
    """
    Sends an approval email to the event organizer.
    """
    subject = f"Your Event '{event_title}' Has Been Approved! 🎉"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [organizer.email]
    organizer_name = f"{organizer.first_name} {organizer.last_name}"

    text_content = f"Dear {organizer_name},\n\nWe are pleased to inform you that your event '{event_title}' has been approved. You can now proceed with the necessary arrangements.\n\nBest Regards,\nEvent Team"

    html_content = f"""
    <p>Dear {organizer_name},</p>
    <p>We are pleased to inform you that your event <strong>{event_title}</strong> has been approved. 🎉</p>
    <p>You can now proceed with the necessary arrangements.</p>
    <p>Best Regards,<br>Eventify Team</p>
    """

    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        print(f"Error: Failed to send approval email to {organizer.email}. Reason: {e}")


# for sending welcome message to user
def send_welcome_email(email, first_name):
    subject = "Welcome to Eventify! 🎉"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    text_content = f"Dear {first_name},\n\nWelcome to Eventify! We are excited to have you on board. You can now start exploring and creating amazing events.\n\nBest Regards,\nEventify Team"

    html_content = f"""
    <p>Dear {first_name},</p>
    <p>Welcome to Eventify! 🎉</p>
    <p>We are excited to have you on board. You can now start exploring and creating amazing events.</p>
    <p>Best Regards,<br>Eventify Team</p>
    """

    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        print(f"Error: Failed to send welcome email to {email}. Reason: {e}")
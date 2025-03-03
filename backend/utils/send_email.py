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


def send_event_reminder_mail(email, first_name, event, rsvp_status):
    subject = f"Reminder: Your Upcoming Event '{event.title}' 📅"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    # Formatting date & time for better readability
    event_start_date = event.start_date.strftime("%B %d, %Y")
    event_end_date = event.end_date.strftime("%B %d, %Y")
    event_time = event.start_date.strftime("%I:%M %p")

    # Custom message based on RSVP status
    if rsvp_status == "Confirmed":
        rsvp_message = (
            "✅ You have confirmed your attendance. We can't wait to see you there!"
        )
    elif rsvp_status == "Declined":
        rsvp_message = "❌ You have declined the invitation. If you change your mind, you can update your RSVP anytime."
    elif rsvp_status == "Pending":
        rsvp_message = (
            "🕒 Your RSVP is still pending. Please confirm your attendance .\n\n"
        )
    else:
        rsvp_message = "🔔 Please check your RSVP status in your Eventify dashboard."

    # Plain text version for better email client compatibility
    text_content = f"""
    Dear {first_name},

    This is a friendly reminder about your upcoming event, "{event.title}".

    📅 Start Date: {event_start_date}
    ⏳ End Date: {event_end_date}
    🕒 Time: {event_time}
    📍 Location: {event.location}

    {rsvp_message}

    We look forward to seeing you there!

    Best Regards,  
    Eventify Team
    """

    # HTML version with proper styling
    html_content = f"""
    <p>Dear {first_name},</p>
    <p>This is a friendly reminder about your upcoming event, <strong>{event.title}</strong>.</p>

    <ul>
        <li>📅 <strong>Start Date:</strong> {event_start_date}</li>
        <li>⏳ <strong>End Date:</strong> {event_end_date}</li>
        <li>🕒 <strong>Time:</strong> {event_time}</li>
        <li>📍 <strong>Location:</strong> {event.location}</li>
    </ul>

    <p>{rsvp_message}</p>

    <p>We look forward to seeing you there!</p>

    <p>Best Regards,<br><strong>Eventify Team</strong></p>
    """

    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        print(f"Error: Failed to send event reminder email to {email}. Reason: {e}")

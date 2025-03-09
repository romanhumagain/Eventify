from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# Sends an approval email to the event organizer when their event is approved.
def send_event_approval_mail(event_title, organizer):
    subject = f"🎉 Your Event '{event_title}' Has Been Approved!"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [organizer.email]
    organizer_name = organizer.username

    # Plain text version (fallback for email clients that don't support HTML)
    text_content = f"""
    Dear {organizer_name},

    We are pleased to inform you that your event '{event_title}' has been approved. 🎉
    
    You can now proceed with the necessary arrangements to make your event successful.

    Best Regards,
    Eventify Team
    """

    # HTML email content (attractive and visually appealing)
    html_content = f"""
    <html>
            <h2 style="color: #2E86C1;">🎉 Event Approved!</h2>
            <p>Dear <strong>{organizer_name}</strong>,</p>
            
            <p>We are thrilled to inform you that your event <strong>{event_title}</strong> has been approved! 🚀</p>
            
            <p>You can now proceed with the necessary arrangements to ensure a successful event.</p>
            
            <p style="margin-top: 20px;">
                <a href="{settings.VITE_BASE_URL}/dashboard" 
                style="background-color: #2E86C1; color: white; padding: 10px 20px; 
                text-decoration: none; border-radius: 5px; font-weight: bold;">
                    Manage Your Event
                </a>
            </p>
            <p style="margin-top: 30px;">Best Regards,</p>
            <p><strong>Eventify Team</strong></p>
    </html>
    """

    try:
        # Create an email message with both text and HTML versions
        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")  # Attach the HTML content
        msg.send()  # Send the email

    except Exception as e:
        print(f"Error: Failed to send approval email to {organizer.email}. Reason: {e}")


# for sending welcome message to user
def send_welcome_email(email, username):
   
    subject = "Welcome to Eventify! 🎉"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    # Text content for email
    text_content = f"""
    Dear {username},

    Welcome to Eventify! 🎉
    
    We are thrilled to have you on board. With Eventify, you can create and explore amazing events, connect with others, and much more.

    Start your journey with us and make the most of our platform!

    Best Regards,
    Eventify Team
    """

    # HTML content for email
    html_content = f"""
    <html>
            <h2 style="color: #2E86C1;">Welcome to Eventify, {username}! 🎉</h2>

            <p>Dear <strong>{username}</strong>,</p>

            <p>We are thrilled to have you on board. With Eventify, you can:</p>
            <ul style="list-style-type: none; padding-left: 0;">
                <li>🎟️ Create amazing events</li>
                <li>🌍 Explore a variety of events happening around you</li>
            </ul>
            
            <p>Start your journey with us and make the most of our platform!</p>

            <p style="margin-top: 20px;">
                <a href="{settings.VITE_BASE_URL}" style="background-color: #2E86C1; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                    Explore Now
                </a>
            </p>

            <p style="margin-top: 30px;">Best Regards,</p>
            <p><strong>The Eventify Team</strong></p>
    </html>
    """

    try:
        # Creating the email with both plain text and HTML alternatives
        msg = EmailMultiAlternatives(
            subject, 
            text_content, 
            from_email, 
            recipient_list
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    except Exception as e:
        print(f"Error: Failed to send welcome email to {email}. Reason: {str(e)}")


def send_event_reminder_mail(email, username, event, rsvp_status):
    subject = f"Reminder: Your Upcoming Event '{event.title}' 📅"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    # Formatting date & time for better readability
    event_start_date = event.start_date.strftime("%B %d, %Y")
    event_end_date = event.end_date.strftime("%B %d, %Y")
    event_time = event.start_date.strftime("%I:%M %p")

    # Custom message based on RSVP status
    if rsvp_status == "interested":
        rsvp_message = (
            "✅ You have marked your rsvp as interested."
        )
    elif rsvp_status == "not_interested":
        rsvp_message = "❌ You have declined the invitation. If you change your mind, you can update your RSVP anytime."
    elif rsvp_status == "going":
        rsvp_message = (
            "🕒 You have confirmed your rsvp status as going .\n\n"
        )
    else:
        rsvp_message = "🔔 Please check your RSVP status in your Eventify dashboard."

    # Plain text version for better email client compatibility
    text_content = f"""
    Dear {username},

    This is a friendly reminder about your upcoming event, "{event.title}".

    📅 Start Date: {event_start_date}
    ⏳ End Date: {event_end_date}
    🕒 Time: {event_time}
    📍 Location: {event.venue}

    {rsvp_message}

    We look forward to seeing you there!

    Best Regards,  
    Eventify Team
    """

    # HTML version with proper styling
    html_content = f"""
    <p>Dear {username},</p>
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


#  to send mail after successful checkedin
def send_checked_in_email(ticket_qr):
    try:
        user = ticket_qr.ticket.user
        event = ticket_qr.ticket.event

        subject = f"✅ Check-in Confirmed: {event.title}"

        # Format the check-in time properly
        check_in_time = ticket_qr.checked_in_time.strftime("%B %d, %Y at %I:%M %p")

        # Attractive HTML email content
        message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
            <div style="max-width: 600px; padding: 20px; border-radius: 10px; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); background: #f9f9f9;">
                <h2 style="color: #2E86C1; text-align: center;">🎉 Check-in Successful!</h2>
                
                <p>Dear <strong>{user.username}</strong>,</p>
                
                <p>We’re excited to confirm that your check-in for <strong>{event.title}</strong> was successful! 🏆</p>
                
                <p>🕒 <strong>Check-in Time:</strong> {check_in_time}</p>
                
                <p>📍 <strong>Venue:</strong> {event.venue}</p>
                
                <p>Enjoy the event and have a fantastic time! 🚀</p>
                
                <p style="margin-top: 20px;">
                   <a href="{settings.VITE_BASE_URL}/events/{event.id}/" style="background-color: #2E86C1; color: white; 
                    padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                        View Event Details
                    </a>
                </p>

                <p style="margin-top: 30px;">Best Regards,</p>
                <p><strong>{event.organizer.username}</strong></p>
            </div>
        </body>
        </html>
        """

        # Create email message object
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],
        )
        email.content_subtype = "html"  # Set the email format to HTML
        email.send()

    except Exception as e:
        print(f"❌ Failed to send check-in email to {user.email}: {str(e)}")

# to send mail after the email updates 
def send_event_update_email(user, event):
  
    subject = f"Your Event '{event.title}' Has Been Updated! ✨"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    
    event_url = f"{settings.VITE_BASE_URL}/events/{event.id}"

    # Text content for email
    text_content = f"""
    Dear {user.username},

    We wanted to inform you that the event '{event.title}' has been updated. Please take a moment to review the changes.

    You can now view the updated event details using the link below:

    Event Title: {event.title}
    View Event:  {event_url}

    Best Regards,
    {event.organizer.username}
    """

    # HTML content for email (Content not centered, left-aligned)
    html_content = f"""
    <html>
            <h2 style="color: #E74C3C;">Your Event '{event.title}' Has Been Updated! ✨</h2>

            <p>Dear <strong>{user.username}</strong>,</p>

            <p>We wanted to inform you that the event <strong>'{event.title}'</strong> has been updated. Please take a moment to review the changes.</p>

            <p>You can now view the updated event details using the link below:</p>

            <p style="margin-top: 20px;">
                <a href="{event_url}" style="background-color: #E74C3C; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                    View Updated Event
                </a>
            </p>

            <p style="margin-top: 30px;">Best Regards,</p>
            <p><strong>{event.organizer.username}</strong></p>

    </html>
    """

    try:
        # Creating the email with both plain text and HTML alternatives
        msg = EmailMultiAlternatives(
            subject, 
            text_content, 
            from_email, 
            recipient_list
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    except Exception as e:
        print(f"❌ Error: Failed to send event update email to {user.email}. Reason: {str(e)}")

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from events.models import Event
from tickets.models import BookedTicket


@shared_task
def send_event_reminder():
    """Sends event reminders to users 3 days before the event starts."""
    today = timezone.now().date()
    reminder_date = today + timedelta(days=3)

    events = Event.objects.filter(start_date__date=reminder_date)

    for event in events:
        booked_tickets = BookedTicket.objects.filter(ticket__event=event)
        users = [ticket.ticket.user for ticket in booked_tickets]
        recipient_emails = [user.email for user in users]

        for user in users:
            subject = f"Reminder: Your Event {event.title} is Almost Here! 🎉"
            message = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Event Reminder</title>
                <style>
                    @media only screen and (max-width: 600px) {{
                        .container {{
                            width: 100% !important;
                            padding: 20px !important;
                        }}
                        .content {{
                            padding: 20px !important;
                        }}
                        .details-box {{
                            padding: 20px !important;
                        }}
                        h2 {{
                            font-size: 20px !important;
                        }}
                    }}
                </style>
            </head>
            <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; background-color: #f9f9f9; padding: 20px; margin: 0;">
                <div class="container" style="background-color: #ffffff; border-radius: 10px; padding: 30px; box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1); max-width: 600px; margin: 0 auto;">
                    <h2 style="text-align: center; color: #1E90FF; font-size: 24px; font-weight: bold; margin-bottom: 25px;">🌟 Event Reminder from Eventify 🌟</h2>
                    
                    <p style="font-size: 18px; color: #555; margin-bottom: 20px;">
                        Dear <strong>{user.username}</strong>,
                    </p>
                    
                    <p style="font-size: 16px; color: #555; line-height: 1.6;">
                        This is a friendly reminder that your booked reservation for the upcoming event <strong style="color: #1E90FF;">{event.title}</strong> is fast approaching.
                    </p>
                    
                    <div class="details-box" style="margin: 25px 0; background-color: #f8fbff; padding: 25px; border-radius: 12px; border-left: 4px solid #1E90FF;">
                        <h3 style="font-size: 20px; color: #333; font-weight: bold; margin-top: 0; margin-bottom: 20px;">Event Details</h3>
                        
                        <div style="margin-bottom: 20px; display: block;">
                            <p style="font-size: 16px; color: #1E90FF; margin: 10px 0; font-weight: bold;">📅 Event Date</p>
                            <p style="font-size: 16px; color: #555; margin: 5px 0; padding-left: 10px; border-left: 2px solid #e0e0e0;">{event.start_date.strftime('%B %d, %Y - %I:%M %p')}</p>
                        </div>
                        
                        <div style="margin-bottom: 20px; display: block;">
                            <p style="font-size: 16px; color: #1E90FF; margin: 10px 0; font-weight: bold;">📍 Venue</p>
                            <p style="font-size: 16px; color: #555; margin: 5px 0; padding-left: 10px; border-left: 2px solid #e0e0e0;">{event.venue if event.event_type == "physical" else "Online Event"}</p>
                        </div>
                        
                        <div style="margin-bottom: 10px; display: block;">
                            <p style="font-size: 16px; color: #1E90FF; margin: 10px 0; font-weight: bold;">ℹ️ Event Details</p>
                            <p style="font-size: 16px; color: #555; margin: 5px 0; padding-left: 10px; border-left: 2px solid #e0e0e0;">{event.details if event.details else "No additional details provided."}</p>
                        </div>
                
                    </div>

                    <p style="font-size: 16px; color: #555; line-height: 1.6;">
                        We're excited to have you join us at the event! If you have any questions or need further information, feel free to reach out.
                    </p>
                    
                    <p style="font-size: 16px; color: #555; line-height: 1.6;">
                        We look forward to seeing you soon! 😊
                    </p>
                    
                    <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                        <p style="font-size: 14px; color: #777; margin-bottom: 5px;">Best regards,</p>
                        <p style="font-size: 16px; font-weight: bold; color: #1E90FF; margin-top: 0;">The Eventify Team</p>
                    </div>
                    
                    <footer style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #aaa;">
                        <p style="margin: 5px 0;">&copy; {timezone.now().year} Eventify. All rights reserved.</p>
                    </footer>
                </div>
            </body>
            </html>
            """
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
                html_message=message,
            )

    return f"Reminders sent for events on {reminder_date}"

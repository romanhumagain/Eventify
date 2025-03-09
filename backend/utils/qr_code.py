from tickets.models import BookedTicket
import secrets
import hashlib
from django.core.mail import EmailMessage
from django.conf import settings


def _generate_qr_codes(ticket):
        """Generate QR codes for a ticket and save the image."""
        unique_string = f"{ticket.id}:{ticket.ticket_code}:{ticket.event.id}:{ticket.user.id}:{secrets.token_hex(8)}"
        qr_code_data = hashlib.sha256(unique_string.encode()).hexdigest()

        # Create the QR code record
        ticket_qr = BookedTicket.objects.create(
            ticket=ticket,
            qr_code_data=qr_code_data,
            is_checked_in=False
        )

        # Generate and save the QR code image
        ticket_qr.generate_qr_code()
        ticket_qr.save()
        return ticket_qr
        
        
def send_qr_code_email(ticket_qr):
    """ Sends an email with the QR code attached after ticket booking. """

    ticket = ticket_qr.ticket
    user_email = ticket.user.email

    subject = f"Your Ticket QR Code for {ticket.event.title}"
    payment_message = ""
    if not ticket.event.is_free:
        payment_message = f"<p style='color: green; font-weight: bold;'>Your payment has been successfully made.</p>"


    message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #2E86C1;">Hello {ticket.user.username},</h2>
            <p>🎉 Thank you for booking your ticket for <strong>{ticket.event.title}</strong>!</p>
            {payment_message}
            <p>📲 <strong>Your QR Code is attached</strong>. Please present it at the event for entry.</p>
            <p>📅 <strong>Event Date:</strong> {ticket.event.start_date.strftime("%B %d, %Y at %I:%M %p")}<br>

            📍 <strong>Venue:</strong> {ticket.event.venue}</p>
            <p>We look forward to seeing you at the event! 🚀</p>
            <p style="margin-top:20px;">Best Regards,<br><strong>{ticket.event.organizer.username}</strong></p>
        </body>
    </html>
    """

    try:
        # Create email message object
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[user_email]
        )

        email.content_subtype = "html" 

        # Attach the QR code image if present
        if ticket_qr.qr_code_image:
            email.attach_file(ticket_qr.qr_code_image.path)

        # Send the email
        email.send()

    except Exception as e:
        print(e)
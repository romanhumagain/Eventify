from tickets.models import TicketQR
import secrets
import hashlib
from django.core.mail import EmailMessage
from django.conf import settings

def _generate_qr_codes(ticket):
        """Generate QR codes for a ticket and save the image."""
        unique_string = f"{ticket.id}:{ticket.ticket_code}:{ticket.event.id}:{ticket.user.id}:{secrets.token_hex(8)}"
        qr_code_data = hashlib.sha256(unique_string.encode()).hexdigest()

        # Create the QR code record
        ticket_qr = TicketQR.objects.create(
            ticket=ticket,
            qr_code_data=qr_code_data,
            is_checked_in=False
        )

        # Generate and save the QR code image
        ticket_qr.generate_qr_code()
        ticket_qr.save()
        return ticket_qr
        
        
def send_qr_code_email(ticket_qr):
        ticket = ticket_qr.ticket
        user_email = ticket.user.email
        
        subject = f"Your Ticket QR Code for event #{ticket.event.title}"
        message = f"Dear {ticket.user.username},\n\nThank you for booking the ticket for {ticket.event.title}. Please find your QR code attached for entry to the event."
        
        # Create the email message object
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[user_email]
        )
        
        # Check if the QR code image is present
        if ticket_qr.qr_code_image:
            # Attach the QR code image
            email.attach_file(ticket_qr.qr_code_image.path)
        
        # Send the email
        email.send()
from django.db import models
import uuid
from events.models import Event
from authentication.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import qrcode
import hashlib
import secrets
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils import timezone
class Ticket(models.Model):
    TICKET_STATUS_CHOICES = [
        ('Reserved', 'Reserved but not paid'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled'),
    ]
    
    ticket_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    
    purchase_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    status = models.CharField(max_length=10, choices=TICKET_STATUS_CHOICES, default='Reserved')
    


    def save(self, *args, **kwargs):
        if self.event.is_free:
            self.unit_price = 0
            self.total_price = 0
        else:
            if self.total_price is None:
                self.total_price = self.unit_price * self.quantity

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Ticket #{self.ticket_code} for {self.event.title}"
    
    class Meta:
        unique_together = ('user', 'event')



class TicketQR(models.Model):
    from tickets.models import Ticket
    
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='qr_codes')
    qr_code_data = models.CharField(max_length=255, unique=True) 
    qr_code_image = models.ImageField(upload_to="qr_codes/", blank=True, null=True)
    is_checked_in = models.BooleanField(default=False)
    checked_in_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_checked_in and not self.checked_in_time:
            self.checked_in_time = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"QR for Ticket #{self.ticket.id}"

    def generate_qr_code(self):
        """Generates a QR code image from `qr_code_data` and saves it."""
        qr = qrcode.make(self.qr_code_data)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        file_name = f"qr_{self.ticket.id}.png"
        self.qr_code_image.save(file_name, ContentFile(buffer.getvalue()), save=False)

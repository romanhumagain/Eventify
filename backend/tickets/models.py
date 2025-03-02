from django.db import models
import uuid
from events.models import Event
from authentication.models import User
from django.core.exceptions import ValidationError
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
    
    payment_id = models.CharField(max_length=100, blank=True, null=True)


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
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='qr_codes')
    qr_code_data = models.CharField(max_length=255, unique=True) 
    is_checked_in = models.BooleanField(default=False)
    checked_in_time = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.is_checked_in and not self.checked_in_time:
            self.checked_in_time = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"QR for Ticket #{self.ticket.ticket_code}"
    


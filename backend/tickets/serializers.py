from rest_framework.serializers import ModelSerializer
from .models import Ticket


class TicketSerializer(ModelSerializer):
  class Meta:
    model = Ticket
    fields = ['id', 'ticket_code', 'event', 'user', 'purchase_date', 'quantity', 'unit_price', 'total_price', 'status', 'payment_id']
    read_only_fields = ['user']
    
    
    
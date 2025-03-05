from rest_framework.serializers import ModelSerializer
from .models import Ticket, TicketQR
from rest_framework import serializers


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = [ "id", "ticket_code", "event", "user", "purchase_date", "quantity", "unit_price", "total_price", "status",]
        read_only_fields = ["user"]


class TicketQRSerializer(ModelSerializer):
    event_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TicketQR
        fields = ["id", "ticket", "qr_code_image", "is_checked_in", "event_details"]

    def get_event_details(self, obj):
        event = obj.ticket.event
        return {
            "id": event.id,
            "title": event.title,
            "subtitle": event.subtitle,
            "category": event.category.name if event.category else "Uncategorized",
            "event_type": event.event_type,
            "start_date": event.start_date.strftime("%Y-%m-%d %H:%M"),
            "end_date": event.end_date.strftime("%Y-%m-%d %H:%M"),
            "event_banner": event.banner.url if event.banner else None,
        }
